/* KITH instant quote: pricing engine.
   Pure functions, no dependencies. Used by the website (window.KithQuoteEngine),
   the Cloudflare function (import) and the tests (require). The catalogue JSON holds the numbers. */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.KithQuoteEngine = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  var PRESTIGE = ['BMW', 'MERCEDES-BENZ', 'MERCEDES', 'AUDI', 'LAND ROVER', 'RANGE ROVER', 'PORSCHE', 'JAGUAR', 'LEXUS',
    'VOLVO', 'TESLA', 'MASERATI', 'BENTLEY', 'ASTON MARTIN', 'ALFA ROMEO', 'GENESIS', 'INFINITI', 'MINI', 'CUPRA'];

  function roundDown5(x) { return Math.floor(x / 5) * 5; }
  function roundUp5(x) { return Math.ceil(x / 5) * 5; }

  /* Look-ups are keyed by ids that come from the page and the estimate API, so only ever accept a key the
     table really owns: cat.bands['__proto__'] and cat.bands['constructor'] are truthy and would price at NaN. */
  function has(table, key) { return Object.prototype.hasOwnProperty.call(table, String(key)); }

  /* A quantity the customer picked: whole, at least 1, never more than max. */
  function count(n, dflt, max) {
    var q = Math.round(Number(n));
    return isFinite(q) && q >= 1 ? Math.min(max, q) : dflt;
  }

  /* A [low, high] pair we are willing to put a price on. Nothing we quote is remotely near a million
     hours or a million pounds, and anything that big overflows to Infinity once multiplied out. */
  function pair(v) {
    if (!Array.isArray(v) || v.length !== 2) return null;
    var a = Number(v[0]), b = Number(v[1]);
    if (!isFinite(a) || !isFinite(b) || a < 0 || b < 0 || a > b || b > 1e6) return null;
    return [a, b];
  }

  /* SOP v8 retail labour: hours x multiplier x tier rate. x2 below threshold, x1.5 at/over it; always-x2 jobs stay x2. */
  function labourCost(cat, hours, tier, alwaysX2) {
    var rate = cat.rates_inc_vat[tier];
    if (!rate) throw new Error('Unknown tier ' + tier);
    var mult = alwaysX2 ? 2 : (hours < cat.threshold_hours ? 2 : 1.5);
    return hours * mult * rate;
  }

  /* Guess a size band from DVLA data. The customer can always change it. */
  function guessBand(v) {
    if (!v) return 'medium';
    var make = String(v.make || '').toUpperCase();
    var ta = String(v.typeApproval || '').toUpperCase();
    if (ta.indexOf('N1') === 0 || ta.indexOf('N2') === 0) return 'van';
    if (PRESTIGE.indexOf(make) !== -1) return 'prestige';
    var cc = Number(v.engineCapacity || 0);
    if (cc && cc < 1400) return 'small';
    if (cc && cc > 2000) return 'large';
    return 'medium';
  }

  /* London ULEZ rule of thumb: petrol Euro 4 (most from 2006), diesel Euro 6 (most from late 2015), electric exempt. */
  function ulezLikely(v) {
    if (!v) return null;
    var fuel = String(v.fuelType || '').toUpperCase();
    var euro = String(v.euroStatus || '').toUpperCase().replace(/\s/g, '');
    var yr = Number(v.yearOfManufacture || 0);
    if (fuel.indexOf('ELECTRIC') === 0) return true;
    var n = (euro.match(/EURO(\d)/) || [])[1];
    if (fuel.indexOf('DIESEL') !== -1 || fuel.indexOf('HEAVY OIL') !== -1) {
      if (n) return Number(n) >= 6;
      return yr ? yr >= 2016 : null;
    }
    if (n) return Number(n) >= 4;
    return yr ? yr >= 2006 : null;
  }

  function findJob(cat, id) {
    for (var i = 0; i < cat.jobs.length; i++) if (cat.jobs[i].id === id) return cat.jobs[i];
    return null;
  }

  /* Price one job for one band. `ai` (optional) = {hours:[lo,hi], parts:[lo,hi], note, confidence} from the estimate API,
     already clamped server-side. Returns {kind, low, high, label, dealer, note, ...}. */
  function priceJob(cat, jobId, band, opts) {
    opts = opts || {};
    var job = findJob(cat, jobId);
    if (!job) throw new Error('Unknown job ' + jobId);
    band = has(cat.bands, band) ? String(band) : 'medium';
    var out = { id: job.id, name: job.name, cat: job.cat, type: job.type, note: job.note || '', band: band };

    if (job.type === 'fixed') { out.kind = 'fixed'; out.low = out.high = job.price; out.label = job.label; return out; }
    if (job.type === 'fixed-range') { out.kind = 'range'; out.low = job.low; out.high = job.high; return out; }
    if (job.type === 'tyres') {
      var q = count(opts.qty, 2, 6);
      out.kind = 'fitting'; out.qty = q; out.low = out.high = q * job.fit_each;
      out.label = '£' + (q * job.fit_each) + ' fitting'; return out;
    }
    if (job.type === 'panel') {
      var base = cat.body_panels_ex_vat[job.panel] + (cat.body_band_surcharge_ex_vat[band] || 0);
      var blend = job.panel === 'door' ? cat.body_blend_ex_vat.door : cat.body_blend_ex_vat['default'];
      out.kind = 'range';
      out.low = Math.round(base * 1.2);
      out.high = Math.round((base + blend * 2) * 1.2);
      out.note = 'From £' + out.low + '. The upper figure allows for blending the paint into the panels either side, which we only do if the colour needs it.';
      return out;
    }
    if (job.type === 'photo' || job.type === 'diagnose' || job.type === 'enquiry') { out.kind = job.type; return out; }

    // labour jobs. `opts.ai` is clamped server-side, but never price anything it sends that isn't a usable
    // pair of numbers: a stray NaN or a reversed range here reaches the customer as "£NaN".
    var ai = opts.ai || null;
    var aiH = ai && pair(ai.hours), aiP = ai && pair(ai.parts);
    var h = aiH || job.hours[band];
    var p = job.labour_only ? [0, 0] : (aiP || job.parts[band]);
    // The range the customer sees: the bottom is the rate-card figure for a typical job on their car,
    // the top sits mech_headroom above it. That gap is what lets the site say the final price lands
    // inside the range. Without a headroom set, fall back to the low-to-high book-time spread.
    var headroom = Number(cat.mech_headroom);
    var lo, hi;
    if (isFinite(headroom) && headroom > 0) {
      var anchor = labourCost(cat, (h[0] + h[1]) / 2, job.tier, !!job.x2) + (p[0] + p[1]) / 2;
      lo = anchor; hi = anchor * (1 + headroom);
    } else {
      var lr = labourRange(cat, h, job.tier, !!job.x2);
      lo = lr[0] + p[0]; hi = lr[1] + p[1];
    }
    out.kind = 'range';
    out.low = roundDown5(lo);
    out.high = roundUp5(hi);
    out.hours = h; out.parts = p;
    var conf = ai && ['high', 'medium', 'low'].indexOf(ai.confidence) !== -1 ? ai.confidence : null;
    out.confidence = conf || job.confidence || 'medium';
    if (ai && typeof ai.note === 'string' && ai.note) out.note = ai.note;
    out.source = (aiH || aiP) ? 'ai' : 'catalogue';

    // Typical main dealer figure: book hours at the dealer rate plus dealer parts pricing. Only shown when clearly dearer.
    if (!job.labour_only && cat.dealer) {
      var midH = (h[0] + h[1]) / 2, midP = (p[0] + p[1]) / 2;
      var dealer = midH * cat.dealer.labour_rate_inc_vat + midP * cat.dealer.parts_factor;
      var ours = (out.low + out.high) / 2;
      if (dealer >= ours * (1 + cat.dealer.show_if_saving_at_least)) out.dealer = roundUp5(dealer);
    }
    return out;
  }

  function totals(lines) {
    // Only real numbers count: one NaN line would otherwise turn the whole basket total into "£NaN".
    var priced = lines.filter(function (l) {
      return l && typeof l.low === 'number' && isFinite(l.low) && isFinite(l.high) && l.low >= 0 && l.high >= l.low;
    });
    var t = { low: 0, high: 0, dealer: 0, count: priced.length, unpriced: lines.length - priced.length };
    priced.forEach(function (l) { t.low += l.low; t.high += l.high; t.dealer += (l.dealer || (l.low + l.high) / 2); });
    t.low = Math.round(t.low); t.high = Math.round(t.high); t.dealer = roundUp5(t.dealer);
    t.showDealer = priced.some(function (l) { return l.dealer; });
    return t;
  }

  /* A model-written note is shown to a customer as our own advice. Keep it to a plain sentence and drop
     anything that could carry a link, a phone number or an instruction to contact someone else. Applied
     server-side when the estimate is built and again in the browser before it is shown. */
  function safeNote(s) {
    if (typeof s !== 'string') return '';
    var n = s.replace(/[<>{}|\\^~`\u0000-\u001f]/g, ' ').replace(/\s+/g, ' ').trim().slice(0, 200);
    return /https?:|www\.|@|\d{7,}|\bcall\b|\bwhatsapp\b|\bemail\b/i.test(n) ? '' : n;
  }

  /* Accept an AI estimate only if it sits inside sane bounds for that job (60% of the smallest band to 180% of the largest);
     otherwise return null so the price book is used instead. */
  function clampAi(cat, jobId, ai) {
    var job = findJob(cat, jobId);
    if (!job || job.type !== 'labour' || !ai) return null;
    function bounds(table) {
      var lo = Infinity, hi = 0;
      Object.keys(table).forEach(function (b) { lo = Math.min(lo, table[b][0]); hi = Math.max(hi, table[b][1]); });
      return [lo * 0.6, hi * 1.8];
    }
    function fix(pair, b, step) {
      if (!Array.isArray(pair) || pair.length !== 2) return null;
      var a = Number(pair[0]), c = Number(pair[1]);
      if (!isFinite(a) || !isFinite(c)) return null;
      if (a > c) { var t = a; a = c; c = t; }
      // Anything outside sane bounds means the AI has misread the job: reject it and fall back to the price book.
      if (a < b[0] || c > b[1]) return null;
      if (c < a * 1.1) c = a * 1.1; // always show a real range
      return [Math.round(a / step) * step, Math.round(c / step) * step];
    }
    var hours = fix(ai.hours, bounds(job.hours), 0.1);
    var parts = job.labour_only ? [0, 0] : fix(ai.parts, bounds(job.parts), 5);
    if (!hours || !parts) return null;
    hours = [Number(hours[0].toFixed(1)), Number(hours[1].toFixed(1))];
    var conf = ['high', 'medium', 'low'].indexOf(ai.confidence) !== -1 ? ai.confidence : 'medium';
    var note = safeNote(ai.note);
    return { hours: hours, parts: parts, confidence: conf, note: note };
  }

  /* Labour for an hours range. The SOP multiplier steps down at 2.0 hrs, so a range that straddles it is
     not monotonic (1.99 hrs costs more than 2.0): check both sides and take the true low and high. */
  function labourRange(cat, hours, tier, alwaysX2) {
    var pts = [labourCost(cat, hours[0], tier, alwaysX2), labourCost(cat, hours[1], tier, alwaysX2)];
    if (!alwaysX2 && hours[0] < cat.threshold_hours && hours[1] >= cat.threshold_hours) {
      pts.push(labourCost(cat, cat.threshold_hours - 0.01, tier, alwaysX2));
      pts.push(labourCost(cat, cat.threshold_hours, tier, alwaysX2));
    }
    return [Math.min.apply(null, pts), Math.max.apply(null, pts)];
  }

  /* One tyre, inc VAT, before fitting. Wider tyres cost more than the rim size alone suggests.
     Returns null for a size we have no price for (a rim outside mid_by_rim, a width that isn't a sensible
     number): better to say nothing than to quote a made-up figure. Callers handle null, as they do for bodyLine. */
  function tyrePrice(cat, size, tierId) {
    var T = cat.tyres, tier = T.tiers.filter(function (t) { return t.id === tierId; })[0] || T.tiers[1];
    if (!size) return null;
    // A real supplier price for this exact size beats the model: exact figure, no give-or-take.
    var key = size.width + '/' + size.profile + 'R' + size.rim;
    if (T.price_list && has(T.price_list, key) && T.price_list[key] && has(T.price_list[key], tier.id)) {
      var listed = Number(T.price_list[key][tier.id]) * (size.runflat ? T.runflat_multiplier : 1);
      if (isFinite(listed) && listed > 0) {
        var each = Math.round(listed);
        return { lo: each, hi: each, fit: T.fit_each, tier: tier, listed: true };
      }
    }
    if (!has(T.mid_by_rim, size.rim)) return null;
    var width = Number(size.width);
    if (!isFinite(width) || width <= 0) return null;
    var base = T.mid_by_rim[String(size.rim)] * (1 + (width - 205) * T.width_factor_per_mm) *
               tier.mult * (size.runflat ? T.runflat_multiplier : 1);
    if (!(base > 0)) return null; // a width far below the 205mm reference would price a tyre at less than nothing
    return { lo: roundDown5(base * 0.9), hi: roundUp5(base * 1.1), fit: T.fit_each, tier: tier };
  }
  function tyreLine(cat, size, tierId, qty) {
    var p = tyrePrice(cat, size, tierId), q = count(qty, 4, 6);
    if (!p) return null;
    return { id: 'tyres', name: q + ' × ' + size.width + '/' + size.profile + ' R' + size.rim + ' ' + p.tier.label.toLowerCase() + ' tyres, fitted',
             kind: 'range', low: (p.lo + p.fit) * q, high: (p.hi + p.fit) * q, each: { lo: p.lo + p.fit, hi: p.hi + p.fit },
             note: 'Includes fitting, balancing and a new valve at £' + p.fit + ' a tyre.' +
                   (p.listed ? '' : ' The tyre itself follows our supplier’s price on the day, so we confirm the exact tyre and price with you.') };
  }

  /* One damaged panel: paint (with blending at the top of the range) and/or dent work. */
  function bodyLine(cat, panelKey, panelLabel, damageId, band) {
    var d = null, list = cat.bodywork_damage;
    for (var i = 0; i < list.length; i++) if (list[i].id === damageId) d = list[i];
    if (!d || !has(cat.body_panels_ex_vat, panelKey)) return null;
    // A SMART repair is a flat price: it's localised work, so the panel it's on barely moves the figure.
    if (isFinite(Number(d.flat)) && Number(d.flat) > 0) {
      return { id: 'panel-' + panelKey, name: panelLabel + ': ' + d.label.toLowerCase(), kind: 'range',
               low: Number(d.flat), high: Number(d.flat), part: false, note: d.hint || '' };
    }
    var add = has(cat.body_band_surcharge_ex_vat, band) ? cat.body_band_surcharge_ex_vat[band] : 0, lo = 0, hi = 0;
    if (d.paint) {
      var base = cat.body_panels_ex_vat[panelKey] + add;
      lo += base; hi += base + (panelKey === 'door' ? cat.body_blend_ex_vat.door : cat.body_blend_ex_vat['default']);
    }
    if (d.dent) { lo += cat.jobs.filter(function (j) { return j.id === 'dent'; })[0].low / 1.2; hi += cat.jobs.filter(function (j) { return j.id === 'dent'; })[0].high / 1.2; }
    return { id: 'panel-' + panelKey, name: panelLabel + ': ' + d.label.toLowerCase(), kind: 'range',
             low: roundDown5(lo * 1.2), high: roundUp5(hi * 1.2), part: !!d.part,
             note: d.part ? 'The panel itself is priced once we have seen it and know the part cost.' : '' };
  }

  /* Tuning: stage price and the power it typically adds. Gains are a percentage of standard bhp. */
  function tuneLines(cat, fuelId, bhp, stageId, addonIds) {
    var T = cat.tuning, fuel = T.fuels.filter(function (f) { return f.id === fuelId; })[0] || T.fuels[0];
    var stage = T.stages.filter(function (s) { return s.id === stageId; })[0] || T.stages[0];
    var g = fuel[stage.id] || fuel.s1, out = [];
    out.push({ id: stage.id, name: stage.label + ' remap', kind: 'range', low: stage.price[0], high: stage.price[1], note: stage.text });
    (Array.isArray(addonIds) ? addonIds : []).forEach(function (id) {
      var a = T.addons.filter(function (x) { return x.id === id; })[0];
      if (!a) return;
      if (a.quote_after) out.push({ id: a.id, name: a.label, kind: 'enquiry', note: a.sub });
      else out.push({ id: a.id, name: a.label, kind: 'range', low: a.price[0], high: a.price[1], note: a.sub });
    });
    // Only quote a power figure for a real standard bhp: a negative or non-numeric one gives nonsense gains.
    var std = Number(bhp);
    var power = isFinite(std) && std > 0 ? { stock: std, low: Math.round(std * (1 + g[0])), high: Math.round(std * (1 + g[1])) } : null;
    return { lines: out, power: power };
  }

  /* £50 web offer. It has to be worth it: the job must price at or above the minimum spend, or be one we
     can't price online at all yet (accident damage, a remap, a body kit), where the job is always a big one. */
  function couponEligible(cat, totals, hasUnpriced) {
    if (!cat.coupon) return false;
    var min = Number(cat.coupon.min_spend) || 0;
    if (totals && isFinite(totals.high) && totals.high >= min) return true;
    return !!hasUnpriced && !!totals && totals.count === 0;
  }

  /* Bookable days for a calendar ('mechanical' or 'bodywork'), from tomorrow. */
  function bookableDays(cat, calendar, max) {
    var B = cat.booking, out = [], d = new Date();
    if (!has(B.slots, calendar)) return out; // an unknown calendar has no days, rather than throwing
    d.setHours(0, 0, 0, 0);
    for (var i = 1; out.length < (max || 12) && i <= B.book_ahead_days; i++) {
      var x = new Date(d); x.setDate(d.getDate() + i);
      if (B.open_days.indexOf(x.getDay()) === -1) continue;
      var slots = (x.getDay() === 6 ? B.slots[calendar].saturday : B.slots[calendar].weekday) || [];
      if (!slots.length) continue;
      var key = x.getFullYear() + '-' + String(x.getMonth() + 1).padStart(2, '0') + '-' + String(x.getDate()).padStart(2, '0'); // local date, not UTC
      out.push({ key: key, dow: x.toLocaleDateString('en-GB', { weekday: 'short' }),
                 dom: x.getDate(), mon: x.toLocaleDateString('en-GB', { month: 'short' }),
                 long: x.toLocaleDateString('en-GB', { weekday: 'long', day: 'numeric', month: 'long' }), slots: slots });
    }
    return out;
  }

  return { labourCost: labourCost, labourRange: labourRange, guessBand: guessBand, ulezLikely: ulezLikely,
           priceJob: priceJob, totals: totals, clampAi: clampAi, findJob: findJob, tyrePrice: tyrePrice,
           tyreLine: tyreLine, bodyLine: bodyLine, tuneLines: tuneLines, couponEligible: couponEligible,
           bookableDays: bookableDays, safeNote: safeNote };
});
