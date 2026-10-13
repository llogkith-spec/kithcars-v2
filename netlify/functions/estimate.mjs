// POST /api/estimate  {vehicle, model, band, jobs:[ids]}  ->  per-job labour hours and parts range from Claude,
// clamped to the price book. The price itself is always worked out from quote-catalogue.json; the model never
// sets a price. Netlify version. Needs ANTHROPIC_API_KEY; optional ANTHROPIC_MODEL (default claude-sonnet-5).
import { createRequire } from 'module';
import { allowedOrigin, json, throttled, readJson, cacheGet, cacheSet } from './_shared.mjs';

// quote-engine.js is UMD and quote-catalogue.json is plain JSON: require handles both without build flags.
const require = createRequire(import.meta.url);
const catalogue = require('../../quote-catalogue.json');
const Engine = require('../../quote-engine.js');

const SYSTEM = `You estimate workshop book times and retail parts prices for a UK independent garage (KITH Cars Garage & Bodyworks, South London).
For each job you are given, estimate for THIS specific vehicle:
- hours: [low, high] manufacturer/Autodata-style book labour time in hours, the raw time, no multipliers.
- parts: [low, high] UK retail parts price in GBP including VAT for OE or OE-equivalent quality parts from a motor factor.
- confidence: "high" | "medium" | "low"
- note: one short plain-English sentence for the customer (max 160 characters) ONLY if something specific to this vehicle matters (e.g. a timing chain at the back of the engine, an electronic parking brake, a dual mass flywheel, run-flat tyres). Otherwise an empty string.
Rules: never give a total price; never say the car is safe to drive; don't mention other garages; British English; if the vehicle details are too vague, widen the range and set confidence "low".
Reply with JSON only: {"jobs": {"<job id>": {"hours": [x, y], "parts": [x, y], "confidence": "...", "note": "..."}}}`;

export default async (request, context) => {
  if (request.method !== 'POST') return json({ error: 'method_not_allowed' }, 405);
  if (!allowedOrigin(request, context)) return json({ error: 'forbidden' }, 403);
  if (throttled(context, 10)) return json({ error: 'slow down' }, 429);
  if (!process.env.ANTHROPIC_API_KEY) return json({ error: 'estimate_unavailable' }, 503);

  let body;
  try { body = (await readJson(request)) || {}; } catch { return json({ error: 'bad_request' }, 400); }
  const v = body.vehicle || {};
  // Match the band against the real band ids only: catalogue.bands['__proto__'] is truthy and would come
  // back to the page, which then prices every job at NaN.
  const band = Object.keys(catalogue.bands).includes(body.band) ? body.band : Engine.guessBand(v);
  const jobs = (Array.isArray(body.jobs) ? body.jobs : [])
    .map(String).filter(id => { const j = Engine.findJob(catalogue, id); return j && j.ai; }).slice(0, 6);
  if (!jobs.length) return json({ band, jobs: {} });

  const clean = s => String(s || '').replace(/[^\w\s.\-/()]/g, '').slice(0, 60);
  const vehicle = {
    make: clean(v.make), model: clean(body.model), year: Number(v.yearOfManufacture) || null,
    engine_cc: Number(v.engineCapacity) || null, fuel: clean(v.fuelType), size: catalogue.bands[band].label,
  };

  const key = 'est:' + [catalogue.version, vehicle.make, vehicle.model, vehicle.year, vehicle.engine_cc,
    vehicle.fuel, band, jobs.slice().sort().join('+')].join('|').toUpperCase();
  const cached = cacheGet(key);
  if (cached) return json(cached, 200, { 'cache-control': 'public, max-age=2592000' });

  const jobList = jobs.map(id => {
    const j = Engine.findJob(catalogue, id);
    return `- ${id}: ${j.name} (typical for this size: ${j.hours[band][0]}-${j.hours[band][1]} hrs, parts £${j.parts[band][0]}-£${j.parts[band][1]})`;
  }).join('\n');

  let parsed;
  try {
    const res = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: { 'x-api-key': process.env.ANTHROPIC_API_KEY, 'anthropic-version': '2023-06-01', 'content-type': 'application/json' },
      body: JSON.stringify({
        model: process.env.ANTHROPIC_MODEL || 'claude-sonnet-5',
        max_tokens: 800,
        system: SYSTEM,
        messages: [{ role: 'user', content: `Vehicle: ${JSON.stringify(vehicle)}\nJobs:\n${jobList}` }],
      }),
    });
    if (!res.ok) return json({ error: 'estimate_failed' }, 502);
    const data = await res.json();
    if (data.stop_reason === 'max_tokens') return json({ error: 'estimate_failed' }, 502);
    const text = (data.content || []).map(c => c.text || '').join('');
    parsed = JSON.parse(text.slice(text.indexOf('{'), text.lastIndexOf('}') + 1));
  } catch {
    return json({ error: 'estimate_failed' }, 502);
  }

  const out = {};
  jobs.forEach(id => {
    const c = Engine.clampAi(catalogue, id, parsed.jobs && parsed.jobs[id]);
    if (c) out[id] = c;
  });
  const payload = { band, jobs: out };
  cacheSet(key, payload, 2592000000);
  return json(payload, 200, { 'cache-control': 'public, max-age=2592000' });
};

export const config = { path: '/api/estimate' };
