// Shared helpers for the Netlify versions of the /api functions.
// Netlify runs these on Node, not on Cloudflare's runtime, so the two things Cloudflare gave us for free —
// caches.default and the env object — are done by hand here. Everything else behaves the same.

const ALLOWED = ['https://www.kithcars.com', 'https://kithcars.com'];

export function allowedOrigin(request, context) {
  const origin = request.headers.get('origin') || '';
  if (!origin) return true;                       // same-origin navigations and server-side calls
  const extra = (process.env.ALLOWED_ORIGINS || '').split(',').map(s => s.trim()).filter(Boolean);
  if (ALLOWED.concat(extra).includes(origin)) return true;
  // Our own Netlify URLs: the site itself, and its branch and deploy previews. Not a bare *.netlify.app
  // wildcard, which would let any site on Netlify spend our DVLA and Anthropic quota.
  const site = (context && context.site && context.site.name) || process.env.SITE_NAME || '';
  if (!site) return false;
  const safe = site.replace(/[^a-z0-9-]/gi, '');
  return new RegExp('^https://([a-z0-9-]+--)?' + safe + '\\.netlify\\.app$').test(origin);
}

export function json(body, status = 200, headers = {}) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store', ...headers },
  });
}

const hits = new Map();
export function throttled(context, limit = 20, windowMs = 60000) {
  const ip = (context && context.ip) || 'anon';
  const now = Date.now();
  const rec = hits.get(ip) || { n: 0, t: now };
  if (now - rec.t > windowMs) { rec.n = 0; rec.t = now; }
  rec.n++; hits.set(ip, rec);
  if (hits.size > 5000) hits.clear();
  return rec.n > limit;
}

export async function readJson(request, maxBytes = 4000) {
  const text = await request.text();
  if (text.length > maxBytes) throw new Error('too large');
  return JSON.parse(text || '{}');
}

/* A small in-process cache, standing in for Cloudflare's. It only lives as long as this function
   instance, so it saves repeat lookups within a warm instance and nothing more — which is the point:
   the DVLA answer for a registration does not change during a browsing session. */
const store = new Map();
export function cacheGet(key) {
  const hit = store.get(key);
  if (!hit) return null;
  if (Date.now() > hit.until) { store.delete(key); return null; }
  return hit.value;
}
export function cacheSet(key, value, ttlMs) {
  if (store.size > 500) store.clear();
  store.set(key, { value, until: Date.now() + ttlMs });
}
