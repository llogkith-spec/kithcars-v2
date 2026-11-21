// Runs a Netlify-style function (request, context) => Response on Cloudflare Pages.
// The /api code lives once, in netlify/functions/, and reads its keys from process.env.
// Cloudflare hands keys over as context.env instead, so they are copied across on each request.
export function adapt(handler) {
  return async ({ request, env }) => {
    const g = globalThis;
    if (!g.process) g.process = { env: {} };
    if (!g.process.env) g.process.env = {};
    for (const k in env) if (typeof env[k] === 'string') g.process.env[k] = env[k];
    const ip = request.headers.get('CF-Connecting-IP') || 'anon';
    return handler(request, { ip, site: { name: '' } });
  };
}
