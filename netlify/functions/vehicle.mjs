// POST /api/vehicle  {reg}  ->  vehicle details from the DVLA Vehicle Enquiry Service.
// Netlify version. Needs the environment variable DVLA_API_KEY, set in
// Site configuration -> Environment variables. Free key: https://register-for-ves.driver-vehicle-licensing.api.gov.uk/
import { allowedOrigin, json, throttled, readJson, cacheGet, cacheSet } from './_shared.mjs';

const DVLA_URL = 'https://driver-vehicle-licensing.api.gov.uk/vehicle-enquiry/v1/vehicles';
const FIELDS = ['registrationNumber', 'make', 'colour', 'yearOfManufacture', 'monthOfFirstRegistration', 'engineCapacity',
  'fuelType', 'motStatus', 'motExpiryDate', 'taxStatus', 'euroStatus', 'typeApproval', 'wheelplan', 'co2Emissions'];

export default async (request, context) => {
  if (request.method !== 'POST') return json({ error: 'method_not_allowed' }, 405);
  if (!allowedOrigin(request, context)) return json({ error: 'forbidden' }, 403);
  if (throttled(context, 15)) return json({ error: 'slow down' }, 429);
  if (!process.env.DVLA_API_KEY) return json({ error: 'lookup_unavailable' }, 503);

  let reg;
  try { reg = String((await readJson(request)).reg || '').toUpperCase().replace(/[^A-Z0-9]/g, ''); }
  catch { return json({ error: 'bad_request' }, 400); }
  if (!/^[A-Z0-9]{2,8}$/.test(reg)) return json({ error: 'invalid_reg' }, 400);

  const cached = cacheGet('veh:' + reg);
  if (cached) return json({ vehicle: cached }, 200, { 'cache-control': 'public, max-age=86400' });

  // The DVLA can go down, time out, or answer with an HTML error page: none of that escapes as a 500.
  let data;
  try {
    const res = await fetch(DVLA_URL, {
      method: 'POST',
      headers: { 'x-api-key': process.env.DVLA_API_KEY, 'content-type': 'application/json' },
      body: JSON.stringify({ registrationNumber: reg }),
    });
    if (res.status === 404) return json({ error: 'not_found' }, 404);
    if (!res.ok) return json({ error: 'lookup_failed' }, 502);
    data = await res.json();
  } catch { return json({ error: 'lookup_failed' }, 502); }
  if (!data || typeof data !== 'object' || Array.isArray(data)) return json({ error: 'lookup_failed' }, 502);

  const vehicle = {};
  FIELDS.forEach(k => { if (data[k] !== undefined) vehicle[k] = data[k]; });
  cacheSet('veh:' + reg, vehicle, 86400000);
  return json({ vehicle }, 200, { 'cache-control': 'public, max-age=86400' });
};

export const config = { path: '/api/vehicle' };
