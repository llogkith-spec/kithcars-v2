// /api/estimate on Cloudflare Pages: the Netlify function, unchanged, through the adapter.
import handler from '../../netlify/functions/estimate.mjs';
import { adapt } from '../_lib/netlify-adapter.js';
export const onRequest = adapt(handler);
