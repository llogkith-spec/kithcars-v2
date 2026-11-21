# kithcars.com on Cloudflare Pages

Moved from Netlify (Nov 2026) after Netlify's credit limit paused every production deploy.
The site is still plain HTML with no build step. Nothing about Netlify has been removed, so either host works.

## How it fits together
- `functions/api/vehicle.js` and `functions/api/estimate.js` are Cloudflare's entry points. They run the
  same code as Netlify (`netlify/functions/*.mjs`) through `functions/_lib/netlify-adapter.js`, so the
  reg lookup and the estimate live in one place.
- `_redirects` and `_headers` carry the same rules as `netlify.toml`.
- `leadform.js` replaces Netlify Forms on the short quote form (about-us, faq): it posts to the KITH inbox.
- Pretty URLs (`/brake-repairs` serves `brake-repairs.html`) are built into Cloudflare Pages.

## Setting up the project (one time)
1. dash.cloudflare.com → Workers & Pages → Create → Pages → Connect to Git → `llogkith-spec/kithcars-v2`.
2. Project name `kithcars`. Production branch `main`. Framework preset: None. Build command: leave empty.
   Build output directory: `/`.
3. Settings → Variables and Secrets (Production), copied from Netlify → Site configuration → Environment variables:
   - `DVLA_API_KEY`, and/or `MOT_CLIENT_ID`, `MOT_CLIENT_SECRET`, `MOT_API_KEY`, `MOT_TOKEN_URL`
     (optional `MOT_SCOPE`, `MOT_API_URL`)
   - `ANTHROPIC_API_KEY` (optional `ANTHROPIC_MODEL`)
   - `PAGES_PROJECT` = `kithcars` (lets kithcars.pages.dev use the API while testing)
   Then Deployments → Retry deployment, so the functions see them.
4. Test on https://kithcars.pages.dev: `/api/vehicle?health=1` should say `"ready": true`; run a quote end to end.
5. Custom domains → add `kithcars.com` and `www.kithcars.com`, and follow Cloudflare's DNS steps.
   Only once the domain answers from Cloudflare, cancel the Netlify plan.
