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

  /* Work the size band out of whatever the customer typed ("ford focus 1.0", "VW Transit Custom"), so the
     fallback never has to ask them whether their own car is an estate. Returns null when we genuinely can't
     tell, which is the only time the page should ask. Longest key first: TRANSIT CUSTOM beats TRANSIT. */
  function norm(x) {
    return ' ' + String(x || '').toUpperCase().replace(/[^A-Z0-9]+/g, ' ').replace(/\s+/g, ' ').trim() + ' ';
  }

  /* Keys are sorted here rather than trusted in file order: JavaScript hoists integer-like keys such as
     "308" to the front of an object, which would otherwise undo the longest-first ordering. */
  var bandKeys = null, bandKeysFor = null;
  function modelKeys(table) {
    if (bandKeys && bandKeysFor === table) return bandKeys;
    bandKeys = Object.keys(table).sort(function (a, b) {
      var at = a.split(' ').length, bt = b.split(' ').length;
      return bt - at || b.length - a.length || (a < b ? -1 : 1);
    });
    bandKeysFor = table;
    return bandKeys;
  }

  function bandFromText(cat, text) {
    var s = norm(text);
    if (s.length < 4) return null;
    var table = (cat && cat.model_bands) || {};
    var keys = modelKeys(table), hit = null;
    for (var i = 0; i < keys.length; i++) {
      if (s.indexOf(norm(keys[i])) !== -1) { hit = table[keys[i]]; break; }
    }
    // A van is a van whoever made it: a Mercedes Sprinter is not a prestige car.
    if (hit === 'van') return 'van';
    for (var j = 0; j < PRESTIGE.length; j++) {
      if (s.indexOf(norm(PRESTIGE[j])) !== -1) return 'prestige';
    }
    return hit;
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
  /* Servicing moved to its own engine-size rate card, but the four service jobs are referenced
     by id all over the site and the build scripts. Rather than rewrite every caller, those ids
     are answered from the new model here. Callers that pass an engine-size band get that band;
     callers still passing an old size band get the engine size that size usually means. */
  /* Body size is the only thing we can count on knowing, so it has to stand in for engine size.
     It is a weak proxy and the old values leaned far too high: "prestige" meant a 2401-3500cc
     engine, which priced a BMW 118i - a 1.6 - as a three litre. Most prestige cars through the
     door are 2.0 diesels, most mid-size SUVs are 1.5 to 2.0, and the catalogue's own examples for
     a family car (Focus 1.5, Golf 1.4, Astra 1.4, Qashqai 1.3) sit in the 1201-1500 band.

     These are therefore the commonest fitment for each body size, not the largest. The customer
     is always shown what we assumed and can change it in one tap, which is what makes a guess
     here acceptable at all. */
  function ccFromCarSize(band) { return LEGACY_BAND_TO_CC[band] || 'cc2000'; }

  var LEGACY_BAND_TO_CC = {
    small: 'cc1200', medium: 'cc1500', large: 'cc2000', prestige: 'cc2000',
    // Vans price by engine size like everything else now; a working van is typically a 2.0.
    van: 'cc2000'
  };
  var SERVICE_JOB_TO_LEVEL = {
    'service-interim': 'interim', 'service-full': 'full', 'service-major': 'major',
    'oil-filter-change': 'oil-change'
  };

  function priceJob(cat, jobId, band, opts) {
    opts = opts || {};
    if (cat.servicing && SERVICE_JOB_TO_LEVEL[jobId]) {
      var lvl = SERVICE_JOB_TO_LEVEL[jobId];
      var ccBand = svcBandById(cat, band) ? band : (LEGACY_BAND_TO_CC[band] || 'cc2000');
      var line = svcLine(cat, lvl, ccBand, opts);
      if (line) { line.band = ccBand; return line; }
    }
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
    // What the figure is built from, so the page can show its working rather than asking the
    // customer to take the number on trust.
    out.rate = cat.rates_inc_vat[job.tier];
    out.multiplier = job.x2 ? 2 : ((h[0] + h[1]) / 2 < cat.threshold_hours ? 2 : 1.5);
    if (job.includes) out.includes = job.includes;
    if (job.check) out.check = job.check;
    var conf = ai && ['high', 'medium', 'low'].indexOf(ai.confidence) !== -1 ? ai.confidence : null;
    out.confidence = conf || job.confidence || 'medium';
    if (ai && typeof ai.note === 'string' && ai.note) out.note = ai.note;
    out.source = (aiH || aiP) ? 'ai' : 'catalogue';

    // Typical main dealer figure: book hours at the dealer rate plus dealer parts pricing. Only shown when clearly dearer.
    if (!job.labour_only && cat.dealer) {
      var midH = (h[0] + h[1]) / 2, midP = (p[0] + p[1]) / 2;
      // The dealer rate can be one figure for everything, or one per size band: a prestige main
      // dealer in London charges well above a volume-brand one, and a single average flatters
      // neither comparison.
      var ours = (out.low + out.high) / 2, dealer;
      if (cat.dealer.use_multiplier && Number(cat.dealer.multiplier) > 1) {
        // A flat multiple of our own price. Simpler and always shows the gap, which the book-hours
        // model did not: at a real dealer rate a short job comes out barely dearer, so the
        // comparison vanished on most of the list. Presented as a typical average, never as a
        // quote for any particular garage.
        dealer = ours * Number(cat.dealer.multiplier);
      } else {
        // The dealer rate can be one figure for everything, or one per size band: a prestige main
        // dealer in London charges well above a volume-brand one, and a single average flatters
        // neither comparison.
        var dr = cat.dealer.labour_rate_inc_vat;
        var dRate = (dr && typeof dr === 'object') ? Number(dr[band]) : Number(dr);
        if (!isFinite(dRate) || dRate <= 0) dRate = 0;
        dealer = midH * dRate + midP * cat.dealer.parts_factor;
      }
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

  /* Bodywork can't be priced to the pound off a diagram: the same scrape is a different job depending on
     how deep it is and what's behind it. So the bodywork total is shown as a band around the worked-out
     figure — plus or minus body_range.band_inc_vat — and the estimator confirms the exact price after
     looking at the car. The bottom is held at a fraction of the figure so a small job doesn't read as
     nearly free. Returns the total unchanged when no band is configured. */
  function bodyBand(cat, t, lines) {
    var cfg = cat && cat.body_range;
    var band = cfg ? Number(cfg.band_inc_vat) : 0;
    if (!t || !isFinite(band) || band <= 0 || !isFinite(t.low) || !isFinite(t.high)) return t;
    // A job that already comes out as a spread is carrying its own uncertainty -- a dent is £70 to
    // £300 of straightening on top of the panel, because severity genuinely varies that much. Adding
    // the band on top of that would stack one allowance on another and quote a range nobody believes.
    // The band is for the jobs that price to a single figure and still need headroom.
    if (t.high > t.low) return t;
    // Otherwise every bodywork job gets it, not only the obviously uncertain ones. Even a straight
    // panel respray moves with how far the colour has to be blended into the panels either side and
    // what the prep turns up, so a single hard figure claims a precision the job does not have.
    // The band only ever goes up. What we don't know is how much MORE the job is, never how much
    // less: the rate-card figure is the floor. Banding both ways quoted a dented bumper at £165 when
    // a plain respray of the same bumper is £240.
    var cap = cfg && isFinite(Number(cfg.max_fraction)) ? Number(cfg.max_fraction) : 0.5;
    var use = Math.min(band, t.high * cap);
    var out = {};
    for (var k in t) if (Object.prototype.hasOwnProperty.call(t, k)) out[k] = t[k];
    out.low = roundDown5(t.low);
    out.high = roundUp5(t.high + use);
    out.banded = true;
    return out;
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

  /* A kerbed alloy, priced per wheel. It is not a panel -- there is no paint-the-panel figure
     behind it and no blending -- so it gets its own line rather than being bent into bodyLine. */
  function alloyLine(cat, wheels) {
    var a = cat && cat.alloy_refurb_ex_vat;
    var n = Math.max(1, Math.min(4, Number(wheels) || 0));
    if (!a || !isFinite(Number(a.low)) || !isFinite(Number(a.high))) return null;
    return {
      id: 'alloy', kind: 'range',
      name: n === 1 ? 'Alloy wheel refurbished' : n + ' alloy wheels refurbished',
      low: roundDown5(Number(a.low) * n * 1.2),
      high: roundUp5(Number(a.high) * n * 1.2),
      part: false, uncertain: true, inspect: true,
      note: 'Per wheel, by how far gone the rim is: a kerb scuff tidied and refinished at the ' +
            'lower end, a badly gouged or diamond-cut face at the top. Confirmed when we see them.'
    };
  }

  function bodyLine(cat, panelKey, panelLabel, damageId, band) {
    var d = null, list = cat.bodywork_damage;
    for (var i = 0; i < list.length; i++) if (list[i].id === damageId) d = list[i];
    if (!d || !has(cat.body_panels_ex_vat, panelKey)) return null;
    // A localised repair is priced as a share of painting the whole panel, so it is always the cheaper
    // of the two on every panel. A flat figure could not do that: it undercut a roof and came out dearer
    // than respraying a bonnet.
    if (isFinite(Number(d.panel_fraction)) && Number(d.panel_fraction) > 0) {
      var addP = has(cat.body_band_surcharge_ex_vat, band) ? cat.body_band_surcharge_ex_vat[band] : 0;
      var smart = (cat.body_panels_ex_vat[panelKey] + addP) * Number(d.panel_fraction);
      return { id: 'panel-' + panelKey, name: panelLabel + ': ' + d.label.toLowerCase(), kind: 'range',
               low: roundDown5(smart * 1.2), high: roundDown5(smart * 1.2), part: false, note: d.hint || '' };
    }
    // Older forms: an explicit range, or a single flat figure.
    if (isFinite(Number(d.low)) && isFinite(Number(d.high))) {
      return { id: 'panel-' + panelKey, name: panelLabel + ': ' + d.label.toLowerCase(), kind: 'range',
               low: Number(d.low), high: Number(d.high), part: false, note: d.hint || '' };
    }
    if (isFinite(Number(d.flat)) && Number(d.flat) > 0) {
      return { id: 'panel-' + panelKey, name: panelLabel + ': ' + d.label.toLowerCase(), kind: 'range',
               low: Number(d.flat), high: Number(d.flat), part: false, note: d.hint || '' };
    }
    var add = has(cat.body_band_surcharge_ex_vat, band) ? cat.body_band_surcharge_ex_vat[band] : 0, lo = 0, hi = 0;
    if (d.paint) {
      var base = cat.body_panels_ex_vat[panelKey] + add;
      lo += base; hi += base + (panelKey === 'door' ? cat.body_blend_ex_vat.door : cat.body_blend_ex_vat['default']);
    }
    // A dent on a panel being painted anyway is an uplift on the panel price, not a standalone dent
    // job: the SOP puts it at +£50 small, +£100 big. Using the standalone range put the top at +£500.
    if (d.dent) {
      var up = cat.body_dent_uplift_ex_vat;
      if (up && isFinite(Number(up.low)) && isFinite(Number(up.high))) { lo += Number(up.low); hi += Number(up.high); }
      else {
        var dentJob = cat.jobs.filter(function (j) { return j.id === 'dent'; })[0];
        lo += dentJob.low / 1.2; hi += dentJob.high / 1.2;
      }
    }
    // A fixed rate-card price must not be split into a range by rounding: 240 ex VAT is 288 inc, and
    // rounding the two ends apart showed it as "£285-£290". Round once, upward, when there is no spread.
    var incLo = lo * 1.2, incHi = hi * 1.2;
    var outLo = incLo === incHi ? roundUp5(incLo) : roundDown5(incLo);
    return { id: 'panel-' + panelKey, name: panelLabel + ': ' + d.label.toLowerCase(), kind: 'range',
             low: outLo, high: roundUp5(incHi), part: !!d.part,
             // A dent's depth and whether a panel can be saved are only known with the car here.
             uncertain: !!(d.dent || d.part),
             inspect: !!d.inspect,
             // A merged "dent or damaged panel" is both: it needs seeing, and it may need a new
             // panel. Showing only the part sentence lost the explanation of why it is a range.
             note: [d.inspect ? (d.hint || '') : '',
                    d.part ? 'If the panel cannot be saved, the cost of the replacement is confirmed once we have seen it.' : '']
                   .filter(Boolean).join(' ') };
  }

  /* Recovery: a fixed price by road miles from the workshop, in two sets of bands — the truck for a car
     that won't move, a driver for one that will. Roadside help (jump start, wheel change) and anything past
     the last band, or going anywhere other than our workshop, is priced on the phone rather than guessed. */
  /* How far a postcode is from the workshop. Straight-line great-circle distance, then a road
     factor, because nobody tows in a straight line. Returned in miles. */
  function milesFrom(cat, lat, lon) {
    var o = cat.recovery && cat.recovery.origin;
    if (!o || !isFinite(lat) || !isFinite(lon)) return NaN;
    var R = 3958.8, rad = Math.PI / 180;
    var dLat = (lat - o.lat) * rad, dLon = (lon - o.lon) * rad;
    var h = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
            Math.cos(o.lat * rad) * Math.cos(lat * rad) * Math.sin(dLon / 2) * Math.sin(dLon / 2);
    var crow = 2 * R * Math.asin(Math.min(1, Math.sqrt(h)));
    return crow * (Number(cat.recovery.road_factor) || 1.3);
  }

  /* `where` is either an area id from the catalogue, or a measured location:
     { miles: 4.2, label: 'SM4 5DA' } from a postcode lookup. */
  function recoveryLine(cat, situationId, where) {
    var R = cat.recovery;
    if (!R) return null;
    var s = R.situations.filter(function (x) { return x.id === situationId; })[0];
    var a = (where && typeof where === 'object')
      ? { miles: isFinite(where.miles) ? where.miles : null, label: where.label || 'your postcode' }
      : R.areas.filter(function (x) { return x.id === where; })[0];
    if (!s || !a) return null;
    var name = s.label + (a.miles === null ? '' : ' — ' + a.label);
    if (s.mode === 'roadside') {
      return { id: 'recovery-' + s.id, name: name, kind: 'enquiry',
               note: 'Roadside help is priced when you ring, because it depends on what the car needs at the kerb.' };
    }
    // "somewhere further out" carries no mileage at all, and Number(null) is 0, not NaN: without this an
    // unknown distance would price as if the car were on our doorstep.
    var miles = (a.miles === null || a.miles === undefined || a.miles === '') ? NaN : Number(a.miles);
    if (!isFinite(miles) || miles < 0 || miles > R.max_miles) {
      return { id: 'recovery-' + s.id, name: name, kind: 'enquiry',
               note: 'Past ' + R.max_miles + ' miles we price it on the phone, so you get a real figure rather than a guess.' };
    }
    var bands = s.mode === 'pickup' ? R.pickup_bands_inc_vat : R.recovery_bands_inc_vat;
    var price = null, band = null;
    for (var i = 0; i < bands.length; i++) {
      if (price === null && miles <= bands[i].max) { price = bands[i].price; band = bands[i]; }
    }
    if (price === null) return { id: 'recovery-' + s.id, name: name, kind: 'enquiry', note: R.note };
    // Show the ex-VAT figure too where the rate card is set that way, so the price on screen can
    // be matched against what the customer was quoted on the phone.
    var vat = band && band.ex_vat ? ' (£' + band.ex_vat + ' plus VAT)' : '';
    return { id: 'recovery-' + s.id, name: name, kind: 'fixed', low: price, high: price,
             miles: miles, label: '£' + price + ' fixed',
             note: s.mode === 'pickup'
               ? 'One of us drives it back to the workshop, inc VAT.'
               : 'Fixed price to our workshop' + vat + ', whatever the traffic does.' };
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


  /* ---- Servicing, on Logan's own rate card -------------------------------------------------
     Banded by engine size, because that is what decides how much oil goes in and which filters
     fit. Everything is costed rather than looked up, so changing the labour rate or the price of
     a litre of oil reprices all 24 cells the way it does in his own system. */

  function svcBand(cat, cc) {
    var bands = cat.servicing.bands;
    cc = Number(cc);
    if (!isFinite(cc) || cc <= 0) return null;
    for (var i = 0; i < bands.length; i++) {
      if (bands[i].max === null || cc <= bands[i].max) return bands[i];
    }
    return bands[bands.length - 1];
  }

  function svcBandById(cat, id) {
    var b = cat.servicing.bands.filter(function (x) { return x.id === id; });
    return b.length ? b[0] : null;
  }

  function svcLevel(cat, id) {
    var l = cat.servicing.levels.filter(function (x) { return x.id === id; });
    return l.length ? l[0] : null;
  }

  function partsGrade(cat, id) {
    var g = (cat.servicing.parts_grade.grades || []).filter(function (x) { return x.id === id; });
    return g.length ? g[0] : cat.servicing.parts_grade.grades[0];
  }

  /* One exact figure, for a known band, level, parts grade and oil grade.

     The parts grade sets both the parts multiplier and the oil the service runs on — an OEM
     service uses a dearer oil as well as dearer filters. Asking for the Castrol specialist grade
     lifts the oil above whichever floor the parts grade set, so the two choices compose rather
     than one quietly overriding the other. */
  function svcPrice(cat, levelId, bandId, oilGrade, isEv, partsGradeId) {
    var S = cat.servicing, band = svcBandById(cat, bandId), lvl = svcLevel(cat, levelId);
    if (!band || !lvl) return null;
    var grade = partsGrade(cat, partsGradeId || S.parts_grade.default);
    var rate = isEv ? S.ev_rate_ex_vat : S.rate_ex_vat;
    var parts = 0;
    for (var i = 0; i < lvl.parts.length; i++) parts += Number(band[lvl.parts[i]]) || 0;
    parts = parts * (Number(grade.parts_multiplier) || 1);
    /* Castrol is an uplift per litre, not a flat rate. As a flat £16/l it cost £4 a litre more
       than standard but only £1 more than the OEM grade, so an OEM customer was offered the
       upgrade for about £6 on a fill - which is not what the oil costs. An uplift makes the
       promise on screen true whichever parts grade is underneath it: £5 a litre more, every time. */
    var base = Number(grade.oil_ex_vat_per_litre) || S.oil.standard_ex_vat_per_litre;
    var perLitre = oilGrade === 'specialist'
      ? base + Number(S.oil.specialist_uplift_ex_vat_per_litre)
      : base;
    var ex = rate * lvl.hours[bandId] + parts + band.litres * perLitre;
    return Math.round(ex * (1 + cat.vat_rate) * 100) / 100;
  }

  /* The same service at a main dealer: the identical book hours at their labour rate, and their
     markup on the same parts and oil. Built from the job rather than a flat multiple, because on
     a service the hours and the parts list are known exactly, so the comparison is arithmetic
     rather than assertion.

     Returned only when the gap clears show_if_saving_at_least. A comparison that saves somebody
     four pounds is not a reason to choose a garage, and printing it reads as though we had to
     scrape to find one. */
  function svcDealer(cat, levelId, bandId, oilGrade, partsGradeId, ours) {
    var D = cat.dealer, S = cat.servicing;
    if (!D || !ours) return null;
    var band = svcBandById(cat, bandId), lvl = svcLevel(cat, levelId);
    if (!band || !lvl) return null;

    var dr = D.labour_rate_inc_vat;
    var rate = (dr && typeof dr === 'object') ? Number(dr[bandId] || dr.medium) : Number(dr);
    if (!rate) return null;

    var grade = partsGrade(cat, partsGradeId || S.parts_grade.default);
    var parts = 0;
    for (var i = 0; i < lvl.parts.length; i++) parts += Number(band[lvl.parts[i]]) || 0;
    var base = Number(grade.oil_ex_vat_per_litre) || S.oil.standard_ex_vat_per_litre;
    var perLitre = oilGrade === 'specialist'
      ? base + Number(S.oil.specialist_uplift_ex_vat_per_litre) : base;

    // A dealer fits its own parts at its own markup; labour is already inclusive of VAT.
    var factor = Number(D.parts_factor) || 1;
    var ex = (parts + band.litres * perLitre) * factor;
    var dealer = rate * lvl.hours[bandId] + ex * (1 + cat.vat_rate);

    var floor = ours * (1 + (Number(D.show_if_saving_at_least) || 0));
    return dealer >= floor ? Math.round(dealer / 5) * 5 : null;
  }

  /* What the widget shows. Before the customer picks an oil grade the honest answer is a range:
     standard oil at the bottom, specialist at the top. Once they choose, low and high are the
     same number and the range collapses to a price. */
  function svcLine(cat, levelId, bandId, opts) {
    opts = opts || {};
    var lvl = svcLevel(cat, levelId), band = svcBandById(cat, bandId);
    if (!lvl || !band) return null;
    var grades = cat.servicing.parts_grade.grades;
    var cheapest = grades[0].id, dearest = grades[grades.length - 1].id;
    var std = svcPrice(cat, levelId, bandId, 'standard', opts.ev, cheapest);
    var spec = svcPrice(cat, levelId, bandId, 'specialist', opts.ev, dearest);
    // A price is settled only once BOTH choices are made.
    var chosen = (opts.oil && opts.parts)
      ? svcPrice(cat, levelId, bandId, opts.oil, opts.ev, opts.parts) : null;

    return {
      id: 'service-' + levelId,
      name: lvl.label,
      kind: chosen === null ? 'range' : 'fixed',
      low: chosen === null ? std : chosen,
      high: chosen === null ? spec : chosen,
      oil: opts.oil || null,
      partsGrade: opts.parts || null,
      band: band.id,
      bandLabel: band.label,
      litres: band.litres,
      hours: lvl.hours[bandId],
      check: lvl.check,
      parts: lvl.parts.slice(),
      /* What the price is made of, so the estimate can show its working the way it already does
         for a repair. Named apart from hours/parts above, which carry the rate card's own shapes
         and are read by other callers. Dealer figure only once a price is actually settled -
         comparing a range to a single number tells the customer nothing. */
      rateIncVat: Math.round(cat.servicing.rate_ex_vat * (1 + cat.vat_rate) * 100) / 100,
      hoursCharged: lvl.hours[bandId],
      // Absent, not null, when there is no comparison worth printing: every caller and the test
      // suite read "no dealer key" as "no gap to show", and a null is not the same statement.
      dealer: chosen === null ? undefined
        : (svcDealer(cat, levelId, bandId, opts.oil, opts.parts, chosen) || undefined),
      // The two ends of the range, kept so the widget can explain what moves the price.
      standard: std,
      specialist: spec,
      note: chosen === null
        ? 'Lower figure is aftermarket parts and standard oil; upper is OEM parts with ' +
          cat.servicing.oil.specialist_brand + ' specialist grade. Choose both and this becomes ' +
          'a single price.'
        // Some grade labels already end in the word ("OEM parts"), some do not ("Quality
        // aftermarket"). Appending it blindly produced "OEM parts parts".
        : (partsGrade(cat, opts.parts).label.replace(/\s+parts$/i, '') + ' parts, ' +
           (opts.oil === 'specialist' ? cat.servicing.oil.specialist_brand + ' specialist' : 'standard') +
           ' oil, ' + band.litres + ' litres.')
    };
  }


  /* Service add-ons.

     The cabin filter is inside the major and sold alongside the cheaper services; spark plugs
     and the fuel filter were promised by the major and costed by nothing, so they are chosen
     and quoted rather than assumed. Anything with a part in the band data prices from the same
     numbers as the services themselves, so it tracks the rate card. Anything that varies too
     much per engine says so rather than inventing a figure. */
  function svcAddon(cat, addonId) {
    var a = (cat.servicing.addons || []).filter(function (x) { return x.id === addonId; });
    return a.length ? a[0] : null;
  }

  function addonLine(cat, addonId, bandId, opts) {
    opts = opts || {};
    var a = svcAddon(cat, addonId), band = svcBandById(cat, bandId);
    if (!a || !band) return null;

    // Already covered by the service they've chosen — offer it as included, not as a charge.
    if (a.included_in && opts.levels &&
        opts.levels.some(function (l) { return a.included_in.indexOf(l) !== -1; })) {
      return { id: a.id, name: a.label, kind: 'included', low: 0, high: 0,
               label: 'included', note: 'Part of the ' + opts.levels[0] + ' service already.' };
    }

    if (a.quote) {
      return { id: a.id, name: a.label, kind: 'enquiry', note: a.note };
    }

    var grade = partsGrade(cat, opts.parts || cat.servicing.parts_grade.default);
    var part = (Number(band[a.part]) || 0) * (Number(grade.parts_multiplier) || 1);
    var ex = part + cat.servicing.rate_ex_vat * (Number(a.hours) || 0);
    var price = Math.round(ex * (1 + cat.vat_rate) * 100) / 100;
    return { id: a.id, name: a.label, kind: 'fixed', low: price, high: price,
             label: '£' + price.toFixed(2), note: a.note };
  }

  /* Which add-ons to put in front of someone, given what they have chosen and what fuel the car
     runs on. A petrol car is never offered a diesel fuel filter. */
  function addonsFor(cat, levels, fuel) {
    var f = String(fuel || '').toLowerCase();
    return (cat.servicing.addons || []).filter(function (a) {
      if (a.fuel && f && f.indexOf(a.fuel) === -1) return false;
      // Don't offer what the chosen service already contains.
      if (a.included_in && (levels || []).some(function (l) { return a.included_in.indexOf(l) !== -1; })) return false;
      return true;
    }).map(function (a) { return a.id; });
  }

  /* An MOT costs less bought alongside a full or major service. */
  function motWithService(cat, levelIds) {
    var S = cat.servicing;
    if (!S || !S.mot_with_service_inc_vat) return null;
    var qualifies = (levelIds || []).some(function (id) {
      return S.mot_bundle_levels.indexOf(id) !== -1;
    });
    if (!qualifies) return null;
    var full = priceJob(cat, 'mot', 'small');
    var standalone = full ? full.low : null;
    return {
      id: 'mot-bundle',
      // The condition is part of the name, so it survives into the confirmation, the email and
      // anywhere else the line is printed. A line reading just "MOT £21" is what got booked
      // on its own.
      name: 'MOT (£' + S.mot_with_service_inc_vat + ' with a full or major service)',
      kind: 'fixed',
      low: S.mot_with_service_inc_vat, high: S.mot_with_service_inc_vat,
      label: '£' + S.mot_with_service_inc_vat,
      was: standalone,
      note: 'This price applies only alongside a full or major service. On its own an MOT is £' +
            standalone + ', and that is what it reverts to if the service comes off the booking.'
    };
  }

  return { labourCost: labourCost, labourRange: labourRange, guessBand: guessBand, bandFromText: bandFromText,
           ulezLikely: ulezLikely,
           priceJob: priceJob, totals: totals, bodyBand: bodyBand, clampAi: clampAi, findJob: findJob, tyrePrice: tyrePrice,
           tyreLine: tyreLine, bodyLine: bodyLine, alloyLine: alloyLine, tuneLines: tuneLines, recoveryLine: recoveryLine, milesFrom: milesFrom,
           svcLine: svcLine, svcPrice: svcPrice, partsGrade: partsGrade, svcAddon: svcAddon, addonLine: addonLine, addonsFor: addonsFor, svcBand: svcBand, svcBandById: svcBandById, svcLevel: svcLevel, motWithService: motWithService,
           ccFromCarSize: ccFromCarSize,
           couponEligible: couponEligible, bookableDays: bookableDays, safeNote: safeNote };
});
