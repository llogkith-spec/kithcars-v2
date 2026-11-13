// POST /api/vehicle  {reg}  ->  vehicle details, from whichever source is configured.
//
// First choice is the DVLA Vehicle Enquiry Service (DVLA_API_KEY). DVLA closed new VES
// registrations while they upgrade, so the fallback is the DVSA MOT History API, which is open
// and carries the same details we price from. Either one alone is enough; with neither set the
// page asks the customer for the car by hand, which still prices correctly.
// Netlify version. Keys go in Site configuration -> Environment variables.
import { allowedOrigin, json, throttled, readJson, cacheGet, cacheSet } from './_shared.mjs';
import { motConfigured, motLookup, motDiagnose } from './_mot.mjs';

const DVLA_URL = 'https://driver-vehicle-licensing.api.gov.uk/vehicle-enquiry/v1/vehicles';
const FIELDS = ['registrationNumber', 'make', 'colour', 'yearOfManufacture', 'monthOfFirstRegistration', 'engineCapacity',
  'fuelType', 'motStatus', 'motExpiryDate', 'taxStatus', 'euroStatus', 'typeApproval', 'wheelplan', 'co2Emissions'];

// Which credentials this deploy can actually see. Names and true/false only -- never a value,
// not even a prefix. A 503 is indistinguishable from the outside whether one variable is missing
// or all four are, and chasing that down by guesswork cost an evening.
function credentialHealth() {
  const names = ['MOT_CLIENT_ID', 'MOT_CLIENT_SECRET', 'MOT_API_KEY', 'MOT_TOKEN_URL', 'DVLA_API_KEY'];
  const present = {};
  for (const n of names) present[n] = !!process.env[n];
  return {
    ready: !!process.env.DVLA_API_KEY || motConfigured(),
    present,
    missing: names.filter(n => n.startsWith('MOT_') && !present[n]),
    hint: 'Environment variables are baked in at build time: after adding them, redeploy.',
  };
}

// The staff intake app (GitHub Pages) uses this same lookup so staff never type the car in.
// Only that one origin is let in, and only for lookups — it is named, not a wildcard.
const STAFF_ORIGINS = ['https://llogkith-spec.github.io'];
function staffCors(request) {
  const o = request.headers.get('origin') || '';
  return STAFF_ORIGINS.includes(o) ? { 'access-control-allow-origin': o, 'vary': 'Origin' } : {};
}

export default async (request, context) => {
  const cors = staffCors(request);
  if (request.method === 'OPTIONS') {
    if (!cors['access-control-allow-origin']) return new Response(null, { status: 403 });
    return new Response(null, { status: 204, headers: { ...cors,
      'access-control-allow-methods': 'POST', 'access-control-allow-headers': 'content-type', 'access-control-max-age': '86400' } });
  }
  const res = await handle(request, context, !!cors['access-control-allow-origin']);
  if (cors['access-control-allow-origin']) for (const k in cors) res.headers.set(k, cors[k]);
  return res;
};

async function handle(request, context, staff) {
  // GET /api/vehicle?health=1 says which credentials are visible, so a 503 can be diagnosed
  // without opening a support thread. It exposes no secret, only whether each name is set.
  if (request.method === 'GET') {
    const url = new URL(request.url);
    if (url.searchParams.has('health')) return json(credentialHealth(), 200);
    // GET /api/vehicle?diag=AB12CDE runs a real lookup and reports which step failed and what
    // the provider said. Names, status codes and the provider's own error code only.
    if (url.searchParams.has('diag')) {
      const reg = String(url.searchParams.get('diag') || '').toUpperCase().replace(/[^A-Z0-9]/g, '');
      if (!/^[A-Z0-9]{2,8}$/.test(reg)) return json({ error: 'invalid_reg' }, 400);
      if (!motConfigured()) return json({ error: 'not_configured', ...credentialHealth() }, 503);
      // A diagnostic that can itself fail silently is no use: the first version returned a blank
      // page and told us nothing. Anything thrown in here comes back as readable text.
      try {
        const report = await motDiagnose(reg);
        return json(report && Object.keys(report).length ? report
                    : { error: 'diagnose_returned_nothing' }, 200);
      } catch (e) {
        return json({ error: 'diagnose_threw', name: e && e.name,
                      message: String((e && e.message) || e).slice(0, 300) }, 200);
      }
    }
  }
  if (request.method !== 'POST') return json({ error: 'method_not_allowed' }, 405);
  if (!staff && !allowedOrigin(request, context)) return json({ error: 'forbidden' }, 403);
  if (throttled(context, 15)) return json({ error: 'slow down' }, 429);
  // Say what is missing rather than only that something is: the page still falls back to asking
  // for the car by hand, so naming the gap costs the customer nothing and saves us the hunt.
  if (!process.env.DVLA_API_KEY && !motConfigured()) {
    return json({ error: 'lookup_unavailable', ...credentialHealth() }, 503);
  }

  let reg;
  try { reg = String((await readJson(request)).reg || '').toUpperCase().replace(/[^A-Z0-9]/g, ''); }
  catch { return json({ error: 'bad_request' }, 400); }
  if (!/^[A-Z0-9]{2,8}$/.test(reg)) return json({ error: 'invalid_reg' }, 400);

  const cached = cacheGet('veh:' + reg);
  if (cached) return json({ vehicle: cached }, 200, { 'cache-control': 'public, max-age=86400' });

  // No VES key: straight to the MOT History API.
  if (!process.env.DVLA_API_KEY) {
    try {
      const vehicle = await motLookup(reg);
      if (!vehicle) return json({ error: 'not_found' }, 404);
      cacheSet('veh:' + reg, vehicle, 86400000);
      return json({ vehicle }, 200, { 'cache-control': 'public, max-age=86400' });
    } catch { return json({ error: 'lookup_failed' }, 502); }
  }

  // The DVLA can go down, time out, or answer with an HTML error page: none of that escapes as a 500.
  let data;
  try {
    const res = await fetch(DVLA_URL, {
      method: 'POST',
      headers: { 'x-api-key': process.env.DVLA_API_KEY, 'content-type': 'application/json' },
      body: JSON.stringify({ registrationNumber: reg }),
    });
    if (res.status === 404) return json({ error: 'not_found' }, 404);
    if (!res.ok) throw new Error('ves_failed');
    data = await res.json();
    if (!data || typeof data !== 'object' || Array.isArray(data)) throw new Error('ves_shape');
  } catch {
    // VES is down or the key has stopped working. If the MOT API is configured, use it rather
    // than sending the customer to the manual form.
    if (motConfigured()) {
      try {
        const vehicle = await motLookup(reg);
        if (!vehicle) return json({ error: 'not_found' }, 404);
        cacheSet('veh:' + reg, vehicle, 86400000);
        return json({ vehicle }, 200, { 'cache-control': 'public, max-age=86400' });
      } catch { /* fall through to the error below */ }
    }
    return json({ error: 'lookup_failed' }, 502);
  }

  const vehicle = {};
  FIELDS.forEach(k => { if (data[k] !== undefined) vehicle[k] = data[k]; });
  cacheSet('veh:' + reg, vehicle, 86400000);
  return json({ vehicle }, 200, { 'cache-control': 'public, max-age=86400' });
}

export const config = { path: '/api/vehicle' };
