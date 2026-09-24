// Shared helpers for the /api functions.
const ALLOWED = ['https://www.kithcars.com', 'https://kithcars.com'];

export function allowedOrigin(request, env) {
  const origin = request.headers.get('Origin') || '';
  const extra = (env.ALLOWED_ORIGINS || '').split(',').map(s => s.trim()).filter(Boolean);
  if (!origin) return true; // same-origin navigations / server-side calls
  if (ALLOWED.concat(extra).includes(origin)) return true;
  // Preview deployments: only this project's own previews, and only when PAGES_PROJECT names it.
  // A bare *.pages.dev wildcard would let any Cloudflare Pages site spend our DVLA and Anthropic quota.
  const project = (env.PAGES_PROJECT || '').trim();
  if (!project) return false;
  return new RegExp('^https://[a-z0-9-]+\\.' + project.replace(/[^a-z0-9-]/gi, '') + '\\.pages\\.dev$').test(origin);
}

export function json(body, status = 200, headers = {}) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store', ...headers },
  });
}

// Light per-isolate throttle. Add a Cloudflare rate-limiting rule on /api/* for real protection.
const hits = new Map();
export function throttled(request, limit = 20, windowMs = 60_000) {
  const ip = request.headers.get('CF-Connecting-IP') || 'anon';
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
