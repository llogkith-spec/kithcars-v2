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
  const res = await fetch(process.env.MOT_TOKEN_URL, {
    method: 'POST',
    headers: { 'content-type': 'application/x-www-form-urlencoded' },
    body: body.toString(),
  });
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
  const res = await fetch(`${API()}/${encodeURIComponent(reg)}`, {
    headers: { authorization: `Bearer ${t}`, 'x-api-key': process.env.MOT_API_KEY, accept: 'application/json' },
  });
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
