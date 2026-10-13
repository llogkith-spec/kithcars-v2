// POST /api/estimate  {vehicle, model, band, jobs:[ids]}  ->  per-job labour hours + parts range from Claude,
// clamped to the price book. The price itself is always calculated from quote-catalogue.json, never by the AI.
// Needs ANTHROPIC_API_KEY. Optional: ANTHROPIC_MODEL (default claude-sonnet-5).
import { allowedOrigin, json, throttled, readJson } from '../_lib/http.js';
import catalogue from '../../quote-catalogue.json';
import Engine from '../../quote-engine.js';

const SYSTEM = `You estimate workshop book times and retail parts prices for a UK independent garage (KITH Cars Garage & Bodyworks, South London).
For each job you are given, estimate for THIS specific vehicle:
- hours: [low, high] manufacturer/Autodata-style book labour time in hours, the raw time, no multipliers.
- parts: [low, high] UK retail parts price in GBP including VAT for OE or OE-equivalent quality parts from a motor factor.
- confidence: "high" | "medium" | "low"
- note: one short plain-English sentence for the customer (max 160 characters) ONLY if something specific to this vehicle matters (e.g. a timing chain at the back of the engine, an electronic parking brake, a dual mass flywheel, run-flat tyres). Otherwise an empty string.
Rules: never give a total price; never say the car is safe to drive; don't mention other garages; British English; if the vehicle details are too vague, widen the range and set confidence "low".
Reply with JSON only: {"jobs": {"<job id>": {"hours": [x, y], "parts": [x, y], "confidence": "...", "note": "..."}}}`;

export async function onRequestPost({ request, env }) {
  if (!allowedOrigin(request, env)) return json({ error: 'forbidden' }, 403);
  if (throttled(request, 10)) return json({ error: 'slow down' }, 429);
  if (!env.ANTHROPIC_API_KEY) return json({ error: 'estimate_unavailable' }, 503);

  let body;
  try { body = (await readJson(request)) || {}; } catch { return json({ error: 'bad_request' }, 400); }
  const v = body.vehicle || {};
  // Match the band against the real band ids only: catalogue.bands['__proto__'] is truthy and would be echoed
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

  const cacheKey = new Request('https://cache.kithcars.internal/estimate/' + encodeURIComponent(
    [catalogue.version, vehicle.make, vehicle.model, vehicle.year, vehicle.engine_cc, vehicle.fuel, band, jobs.slice().sort().join('+')].join('|').toUpperCase()));
  const hit = await caches.default.match(cacheKey).catch(() => null);
  if (hit) return hit;

  const jobList = jobs.map(id => {
    const j = Engine.findJob(catalogue, id);
    return `- ${id}: ${j.name} (typical for this size: ${j.hours[band][0]}-${j.hours[band][1]} hrs, parts £${j.parts[band][0]}-£${j.parts[band][1]})`;
  }).join('\n');

  let parsed;
  try {
    const res = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: { 'x-api-key': env.ANTHROPIC_API_KEY, 'anthropic-version': '2023-06-01', 'content-type': 'application/json' },
      body: JSON.stringify({
        model: env.ANTHROPIC_MODEL || 'claude-sonnet-5',
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
  const resp = json({ band, jobs: out }, 200, { 'cache-control': 'public, max-age=2592000' });
  await caches.default.put(cacheKey, resp.clone()).catch(() => {});
  return resp;
}
