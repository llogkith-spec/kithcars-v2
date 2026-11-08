// The DVSA MOT History API, used when the DVLA Vehicle Enquiry Service is not available.
//
// DVLA closed new VES registrations while they upgrade their systems, so a new site cannot get a
// VES key at all right now. The MOT History API is open, and for our purposes it carries the same
// information: make, model, engine size, fuel and the MOT expiry date. It does not carry tax status,
// Euro status or the type approval we used to spot a van - the make and model cover that instead.
//
// Credentials, from the registration email, set in Netlify -> Environment variables:
//   MOT_CLIENT_ID, MOT_CLIENT_SECRET, MOT_API_KEY, MOT_TOKEN_URL
// MOT_SCOPE and MOT_API_URL only need setting if DVSA change them.
import { cacheGet, cacheSet } from './_shared.mjs';

const SCOPE = () => process.env.MOT_SCOPE || 'https://tapi.dvsa.gov.uk/.default';
const API = () => process.env.MOT_API_URL || 'https://history.mot.api.gov.uk/v1/trade/vehicles/registration';

export function motConfigured() {
  return !!(process.env.MOT_CLIENT_ID && process.env.MOT_CLIENT_SECRET &&
            process.env.MOT_API_KEY && process.env.MOT_TOKEN_URL);
}

/* Netlify gives a function about ten seconds. A fetch with no deadline of its own can eat all
   of it and return nothing at all, which is exactly what a blank page is. */
async function fetchWithTimeout(url, opts, ms) {
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), ms || 4000);
  try {
    return await fetch(url, { ...(opts || {}), signal: ctrl.signal });
  } finally {
    clearTimeout(timer);
  }
}

/* Node reports every network-level failure as the same two words, "fetch failed", and hangs the
   actual reason off e.cause: ENOTFOUND for a name that does not resolve, ECONNREFUSED for a
   refusal, UND_ERR_CONNECT_TIMEOUT for a connection that never completes, a CERT_ code for TLS.
   Reading only e.message cost two rounds of guessing at a problem the error already named. */
function why(e) {
  const c = (e && e.cause) || null;
  const bits = [String((e && e.message) || e)];
  const code = c && (c.code || c.errno);
  if (code) bits.push(String(code));
  if (c && c.message && c.message !== (e && e.message)) bits.push(String(c.message));
  return bits.join(' / ').slice(0, 160);
}

/* One retry on a network-level failure. A connect that never completes is the commonest transient
   fault against this API, and the customer is sitting watching the registration field. A timeout
   we imposed ourselves is not retried - that way lies running out of Netlify's ten seconds. */
async function fetchTwice(url, opts, ms) {
  try {
    return await fetchWithTimeout(url, opts, ms);
  } catch (e) {
    if (e && e.name === 'AbortError') throw e;
    return await fetchWithTimeout(url, opts, ms);
  }
}

/* Tokens last an hour. Cached for 55 minutes so a token is never used in the minute it expires. */
async function token() {
  const hit = cacheGet('mot:token');
  if (hit) return hit;
  const body = new URLSearchParams({
    grant_type: 'client_credentials',
    client_id: process.env.MOT_CLIENT_ID,
    client_secret: process.env.MOT_CLIENT_SECRET,
    scope: SCOPE(),
  });
  const res = await fetchWithTimeout(process.env.MOT_TOKEN_URL, {
    method: 'POST',
    headers: { 'content-type': 'application/x-www-form-urlencoded' },
    body: body.toString(),
  }, 4000);
  if (!res.ok) throw new Error('token_failed');
  const data = await res.json();
  if (!data.access_token) throw new Error('token_missing');
  cacheSet('mot:token', data.access_token, 55 * 60 * 1000);
  return data.access_token;
}

const year = (...dates) => {
  for (const d of dates) {
    const y = Number(String(d || '').slice(0, 4));
    if (y > 1900 && y < 2100) return y;
  }
  return undefined;
};

/* Map the MOT answer onto the same shape the page already expects from the DVLA, so nothing
   downstream has to know which source it came from. */
function toVehicle(v, reg) {
  const tests = Array.isArray(v.motTests) ? v.motTests.slice() : [];
  // Newest first: the API's order is not guaranteed, and an old test's expiry would read as overdue.
  tests.sort((a, b) => String(b.completedDate || '').localeCompare(String(a.completedDate || '')));
  const latest = tests.find(t => t && t.expiryDate) || null;

  const out = {
    registrationNumber: v.registration || reg,
    make: v.make || '',
    model: v.model || '',
    colour: v.primaryColour || '',
    fuelType: v.fuelType || '',
    yearOfManufacture: year(v.manufactureDate, v.firstUsedDate, v.registrationDate),
    engineCapacity: Number(v.engineSize) || undefined,
    source: 'mot',
  };
  if (latest) {
    out.motExpiryDate = latest.expiryDate;
    const days = (new Date(latest.expiryDate) - new Date()) / 864e5;
    out.motStatus = isFinite(days) ? (days >= 0 ? 'Valid' : 'Not valid') : undefined;
  }
  // Undefined keys would serialise as missing anyway; drop them so the page's checks stay simple.
  Object.keys(out).forEach(k => (out[k] === undefined || out[k] === '') && delete out[k]);
  return out;
}

/* Returns the vehicle, or null when DVSA has no record of that registration.
   Throws for anything else, so the caller answers 502 rather than "not found". */
export async function motLookup(reg) {
  const t = await token();
  const res = await fetchTwice(`${API()}/${encodeURIComponent(reg)}`, {
    headers: { authorization: `Bearer ${t}`, 'x-api-key': process.env.MOT_API_KEY, accept: 'application/json' },
  }, 3500);
  if (res.status === 404) return null;
  if (res.status === 401 || res.status === 403) {
    // Most likely a token that went stale early; drop it so the next call fetches a fresh one.
    cacheSet('mot:token', null, 0);
    throw new Error('mot_auth');
  }
  if (!res.ok) throw new Error('mot_failed');
  const data = await res.json();
  const v = Array.isArray(data) ? data[0] : data;
  if (!v || typeof v !== 'object') throw new Error('mot_shape');
  return toVehicle(v, reg);
}

/* Why a lookup failed, in enough detail to fix it without another round trip.

   The ordinary path deliberately swallows errors so a customer never sees a stack trace — but
   that left "it doesn't work" as the only signal, and the health check only proves the four
   variables EXIST, not that DVSA accepts them. A wrong secret and a wrong scope look identical
   from outside.

   This reports the HTTP status of each step and the provider's own error code. Azure's
   AADSTS codes name the problem exactly (7000215 is a bad secret, 700016 a bad client id,
   500011 a scope the tenant doesn't know). No secret or token is ever included — only the
   length of the secret, which catches the commonest fault of all: a value pasted with the
   trailing character missing or a line break in the middle. */
export async function motDiagnose(reg) {
  const out = {
    step: 'start',
    secretLength: (process.env.MOT_CLIENT_SECRET || '').length,
    secretHasWhitespace: /\s/.test(process.env.MOT_CLIENT_SECRET || ''),
    tokenUrlHasWhitespace: /\s/.test(process.env.MOT_TOKEN_URL || ''),
    apiKeyLength: (process.env.MOT_API_KEY || '').length,
    apiKeyHasWhitespace: /\s/.test(process.env.MOT_API_KEY || ''),
    scope: SCOPE(),
    // Echoed because MOT_API_URL overrides the default: a value set here by mistake, or pasted
    // with a line break, fails exactly like an unreachable host and looks nothing like its cause.
    apiUrl: API(),
    apiUrlFromEnv: !!process.env.MOT_API_URL,
  };

  let access;
  try {
    out.step = 'token';
    const res = await fetchWithTimeout(process.env.MOT_TOKEN_URL, {
      method: 'POST',
      headers: { 'content-type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({
        grant_type: 'client_credentials',
        client_id: process.env.MOT_CLIENT_ID,
        client_secret: process.env.MOT_CLIENT_SECRET,
        scope: SCOPE(),
      }).toString(),
    }, 4000);
    out.tokenStatus = res.status;
    const body = await res.text();
    if (!res.ok) {
      try {
        const j = JSON.parse(body);
        out.tokenError = j.error;
        // Trim to the AADSTS code and its sentence; the rest is trace ids.
        out.tokenDetail = String(j.error_description || '').split('\r')[0].slice(0, 200);
      } catch { out.tokenDetail = body.slice(0, 200); }
      return out;
    }
    access = JSON.parse(body).access_token;
    out.tokenOk = !!access;
    if (!access) { out.tokenDetail = 'response had no access_token'; return out; }
  } catch (e) {
    out.tokenDetail = (e && e.name === 'AbortError')
      ? 'the token endpoint did not answer within 4 seconds — check MOT_TOKEN_URL for a stray space or line break'
      : 'could not reach the token endpoint: ' + why(e);
    out.tokenUrlStart = String(process.env.MOT_TOKEN_URL || '').slice(0, 42);
    return out;
  }

  try {
    out.step = 'api';
    const res = await fetchWithTimeout(`${API()}/${encodeURIComponent(reg)}`, {
      headers: { authorization: `Bearer ${access}`, 'x-api-key': process.env.MOT_API_KEY,
                 accept: 'application/json' },
    }, 4000);
    out.apiStatus = res.status;
    if (!res.ok) { out.apiDetail = (await res.text()).slice(0, 200); return out; }
    const data = await res.json();
    out.step = 'done';
    out.found = !!data;
    out.make = data && data.make;
    out.engineSize = data && (data.engineSize || data.engineCapacity);
  } catch (e) {
    out.apiDetail = why(e);
    out.apiErrorName = e && e.name;
  }
  return out;
}
