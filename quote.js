/* KITH instant quote.
   Four flows, each built for what that customer actually knows:
     mechanical  pick the jobs off a card          tyres  read your sidewall
     bodywork    tap the damaged panel on the car  tuning pick a stage, see the power
   Then: estimate (with the £50 book-online offer and its hold timer) -> details -> pick a slot -> booked.
   Prices always come from quote-catalogue.json. Reg lookup (/api/vehicle) and the AI book-time estimate
   (/api/estimate) are optional; with neither, everything still prices from the price book.
   Leads go to Web3Forms by email, and to the CRM's jobs table when crm keys are filled in. */
(function () {
  'use strict';
  var E = window.KithQuoteEngine, root = document.getElementById('kq');
  if (!E || !root) return;

  var WEB3FORMS_KEY = 'db31da4b-5331-453a-9b9c-d6fb1fbbd264';
  var PHONE = '020 4629 9469', PHONE_TEL = '02046299469', WA = '447923688259';
  var C = null, TICK = null, PENDING = null;   // PENDING: a click that landed before the price book finished loading

  var FLOWS = {
    mechanical: { label: 'Mechanical', sub: 'Servicing, MOT, brakes, repairs', cal: 'mechanical' },
    tyres:      { label: 'Tyres',      sub: 'Priced by your tyre size',        cal: 'mechanical' },
    bodywork:   { label: 'Bodywork',   sub: 'Bumpers, panels, dents, paint',   cal: 'bodywork' },
    tuning:     { label: 'Tuning',     sub: 'Remaps, lowering, wheels',        cal: 'mechanical' },
    recovery:   { label: 'Recovery',   sub: 'Broken down, or needs collecting', cal: 'mechanical' }
  };
  var STEPS = ['flow', 'car', 'build', 'estimate', 'details', 'calendar', 'done'];
  var STEP_LABEL = { flow: 'Service', car: 'Your car', build: 'The work', estimate: 'Your price', details: 'Details', calendar: 'Your slot', done: 'Booked' };

  /* Panels of a car seen from above. key = the price-book panel it charges as. */
  var CAR_PANELS = [
    { id: 'fbumper', key: 'front-bumper', label: 'Front bumper', d: 'M62 14 Q130 -2 198 14 L204 46 L56 46 Z' },
    { id: 'bonnet', key: 'bonnet', label: 'Bonnet', d: 'M60 50 L200 50 L196 150 L64 150 Z' },
    { id: 'roof', key: 'roof', label: 'Roof', d: 'M70 196 L190 196 L190 318 L70 318 Z' },
    { id: 'boot', key: 'boot', label: 'Boot / tailgate', d: 'M64 362 L196 362 L200 448 L60 448 Z' },
    { id: 'rbumper', key: 'rear-bumper', label: 'Rear bumper', d: 'M56 452 L204 452 L198 486 Q130 500 62 486 Z' },
    { id: 'lfwing', key: 'front-wing', label: 'Left front wing', d: 'M22 60 Q30 40 56 46 L60 150 L22 150 Z' },
    { id: 'rfwing', key: 'front-wing', label: 'Right front wing', d: 'M238 60 Q230 40 204 46 L200 150 L238 150 Z' },
    { id: 'lfdoor', key: 'door', label: 'Left front door', d: 'M22 154 L62 154 L66 256 L22 256 Z' },
    { id: 'rfdoor', key: 'door', label: 'Right front door', d: 'M238 154 L198 154 L194 256 L238 256 Z' },
    { id: 'lrdoor', key: 'door', label: 'Left rear door', d: 'M22 260 L66 260 L66 350 L22 350 Z' },
    { id: 'rrdoor', key: 'door', label: 'Right rear door', d: 'M238 260 L194 260 L194 350 L238 350 Z' },
    { id: 'lrq', key: 'rear-quarter', label: 'Left rear quarter', d: 'M22 354 L62 354 L56 452 Q30 460 22 440 Z' },
    { id: 'rrq', key: 'rear-quarter', label: 'Right rear quarter', d: 'M238 354 L198 354 L204 452 Q230 460 238 440 Z' }
  ];


  /* Where the damage sits on the panel, and what that means for blending.

     A dent near the middle of a panel is painted and that is the end of it. A dent near an edge
     has to have the new colour carried into the panel next door, or the repair stops at a hard
     line that catches the light -- so the customer is asked to show us where it is and roughly
     how big, and we work the rest out rather than asking them to judge it. Everything here is in
     the car diagram's own units; PANEL_BOX is each panel's bounding box, read off its path. */
  var PANEL_BOX = {};
  function panelBox(id) {
    if (PANEL_BOX[id]) return PANEL_BOX[id];
    var p = CAR_PANELS.filter(function (x) { return x.id === id; })[0];
    if (!p) return null;
    // Pull every coordinate pair out of the path and take the extremes. The paths are simple
    // enough (lines and one quadratic each) that the control points sit inside the real bounds.
    var nums = (p.d.match(/-?\d+(?:\.\d+)?/g) || []).map(Number), xs = [], ys = [];
    for (var i = 0; i + 1 < nums.length; i += 2) { xs.push(nums[i]); ys.push(nums[i + 1]); }
    var box = { x: Math.min.apply(null, xs), y: Math.min.apply(null, ys),
                w: Math.max.apply(null, xs) - Math.min.apply(null, xs),
                h: Math.max.apply(null, ys) - Math.min.apply(null, ys) };
    PANEL_BOX[id] = box;
    return box;
  }

  // Dent sizes the customer can actually picture, with the radius each draws on the panel.
  var MARK_SIZES = [
    { id: 's', label: 'Coin', hint: 'up to 5cm', r: 7 },
    { id: 'm', label: 'Phone', hint: 'up to 15cm', r: 13 },
    { id: 'l', label: 'Dinner plate', hint: 'up to 30cm', r: 22 },
    { id: 'xl', label: 'Bigger', hint: 'more than 30cm', r: 34 }
  ];
  function markSize(id) {
    for (var i = 0; i < MARK_SIZES.length; i++) if (MARK_SIZES[i].id === id) return MARK_SIZES[i];
    return MARK_SIZES[1];
  }

  /* Does this mark reach close enough to an edge that the repair has to be blended out?
     Measured as the gap between the edge of the dent and the edge of the panel: inside about a
     fifth of the panel's smaller dimension, the paint has nowhere to fade out. */
  function needsBlend(panelId, mark) {
    var box = panelBox(panelId);
    if (!box || !mark) return false;
    var r = markSize(mark.size).r;
    var gap = Math.min(mark.x - box.x, box.x + box.w - mark.x, mark.y - box.y, box.y + box.h - mark.y) - r;
    return gap < Math.min(box.w, box.h) * 0.2;
  }


  /* The wheels sit outside the body outline on the diagram, because a kerbed alloy is a
     different job from a damaged panel and should not look like one. Tapping a wheel counts it;
     the price is per wheel. */
  var CAR_WHEELS = [
    { id: 'wfl', label: 'Front left alloy',  x: 10,  y: 92,  w: 22, h: 54 },
    { id: 'wfr', label: 'Front right alloy', x: 228, y: 92,  w: 22, h: 54 },
    { id: 'wrl', label: 'Rear left alloy',   x: 10,  y: 360, w: 22, h: 54 },
    { id: 'wrr', label: 'Rear right alloy',  x: 228, y: 360, w: 22, h: 54 }
  ];

  var S = {
    flow: '', step: 'flow', reg: '', vehicle: null, manual: false, model: '', band: 'medium',
    mark: {},   // panelId -> {x, y, size} in car-diagram units: where the dent is and how big
    wheels: {}, // wheelId -> true for each kerbed alloy the customer taps
    collectBand: '', // which distance band for collection and return, '' until asked
    bandAuto: false, bandOpen: false,   // bandAuto: we worked the size out; bandOpen: they asked to change it
    mech: [], tyre: { w: 205, p: 55, r: 16, qty: 4, tier: 'mid', rf: false },
    body: {}, tune: { fuel: 'tp', bhp: '', stage: 's1', addons: [] }, rec: { what: '', where: '', when: 'book' },
    ai: {}, lines: [], totals: null, power: null, expires: 0, offerGone: false,
    lead: null, day: null, time: null, sent: false, wantMot: false,
    cc: null, ccBand: null, oil: null, parts: null, addons: []
  };

  /* ---------- helpers ---------- */
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function money(n) { return '£' + Number(n).toLocaleString('en-GB', { minimumFractionDigits: n % 1 ? 2 : 0, maximumFractionDigits: 2 }); }
  function range(lo, hi) { return lo === hi ? money(lo) : money(lo) + ' – ' + money(hi); }

  /* An estimate shown as a range, which is what the small print under it has always promised.
     Once engine size, oil and parts are all answered the rate card produces one exact figure and
     the range collapsed to a single number, contradicting the copy beside it.

     The range runs UPWARDS from that figure, never downwards. The exact price is what we would
     charge for the job as quoted, so it is the floor; the ceiling covers what genuinely varies
     once the car is on the ramp - an engine that takes more oil than its band allows, a
     non-standard filter, a bolt that has seized. Padding downwards would advertise a number no
     customer ever actually pays, which is the one thing a price range must not do. */
  function spread(t) {
    if (!t || typeof t.low !== 'number' || typeof t.high !== 'number') return t;
    if (t.high > t.low) return t;                       // a genuine range already
    var s = C.estimate_spread;
    if (!s) return t;
    var step = s.round_to || 5;
    var pad = Math.max(s.min || 0, Math.round(t.low * (s.pct || 0)));
    // Capped. On a big job 10% runs away with itself, and a range wider than £50 stops reading
    // as an estimate and starts reading as a refusal to quote.
    if (s.max) pad = Math.min(pad, s.max);
    return { low: t.low, high: Math.ceil((t.low + pad) / step) * step };
  }
  function rangeOf(t) { var r = spread(t); return range(r.low, r.high); }
  function $(s) { return root.querySelector(s); }
  function $$(s) { return [].slice.call(root.querySelectorAll(s)); }
  function title(s) { s = String(s || ''); if (s.length <= 3) return s.toUpperCase(); return s.toLowerCase().replace(/\b[\w']/g, function (c) { return c.toUpperCase(); }); }
  function save() { try { sessionStorage.setItem('kq2', JSON.stringify(S)); } catch (e) {} }
  function load() { try { var s = JSON.parse(sessionStorage.getItem('kq2') || 'null'); if (s && !s.sent) { Object.keys(s).forEach(function (k) { S[k] = s[k]; }); } } catch (e) {} }
  /* Through analytics.js where it is loaded, not straight to Google. That file is the one place
     that knows every destination an event has to reach - Google, the Meta pixel, and whatever
     comes next - so an event sent past it arrives at one of them and silently misses the rest.
     This widget raises the only events worth paying for (a price shown, details submitted, a slot
     booked), and those were going to Google alone. gtag and the dataLayer remain the fallback for
     a page that loads the widget without analytics.js. */
  function track(n, p) {
    try {
      if (window.kithTrack) return window.kithTrack(n, p || {});
      if (window.gtag) return window.gtag('event', n, p || {});
      (window.dataLayer = window.dataLayer || []).push(Object.assign({ event: n }, p || {}));
    } catch (e) {}
  }

  /* The make, for the main-dealer comparison. "An Audi main dealer" lands where "a main dealer"
     does not, because the reader is picturing the garage they would otherwise be ringing. It
     comes from the reg lookup where there is one, and from what they typed otherwise: the model
     list in the price book is keyed on make and model, so the first word of a known key is the
     make. Falls back to no brand at all rather than guessing wrong. */
  var MAKES = ['AUDI','BMW','MERCEDES-BENZ','MERCEDES','VOLKSWAGEN','VW','FORD','VAUXHALL','TOYOTA',
    'HONDA','NISSAN','HYUNDAI','KIA','PEUGEOT','CITROEN','RENAULT','SEAT','SKODA','FIAT','MAZDA',
    'MINI','VOLVO','LAND ROVER','RANGE ROVER','JAGUAR','LEXUS','PORSCHE','SUZUKI','SUBARU','DACIA',
    'MITSUBISHI','ALFA ROMEO','TESLA','CUPRA','SSANGYONG','ISUZU','JEEP','CHEVROLET','SMART','ABARTH'];

  function vehicleMake() {
    var v = S.vehicle || {};
    var raw = String(v.make || S.model || '').toUpperCase();
    if (!raw) return '';
    for (var i = 0; i < MAKES.length; i++) {
      if (raw.indexOf(MAKES[i]) !== -1) {
        var m = MAKES[i];
        if (m === 'VW') m = 'VOLKSWAGEN';
        if (m === 'MERCEDES') m = 'MERCEDES-BENZ';
        return title(m);
      }
    }
    return '';
  }

  // "An Audi main dealer" / "A Ford main dealer" / "A main dealer" when we do not know.
  function dealerLabel() {
    var mk = vehicleMake();
    if (!mk) return { a: 'A', text: 'main dealer' };
    return { a: /^[AEIOU]/i.test(mk) ? 'An' : 'A', text: mk + ' main dealer' };
  }

  function vehicleName() { var v = S.vehicle || {}; return [v.yearOfManufacture, title(v.make), S.model].filter(Boolean).join(' ') || 'your vehicle'; }
  function post(url, body, ms) {
    var ctrl = window.AbortController ? new AbortController() : null, t = setTimeout(function () { if (ctrl) ctrl.abort(); }, ms || 9000);
    return fetch(url, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(body), signal: ctrl && ctrl.signal })
      .then(function (r) { clearTimeout(t); return r.json().then(function (j) { j._status = r.status; return j; }); })
      .catch(function () { clearTimeout(t); return { _status: 0, error: 'network' }; });
  }
  function go(step) { S.step = step; save(); render(); var t = root.getBoundingClientRect().top; if (t < -40 || t > window.innerHeight * 0.6) root.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
  function chips(items, current, act) {
    return items.map(function (i) {
      return '<button type="button" class="kq-pill' + (String(i.id) === String(current) ? ' on' : '') + '" data-act="' + act + '" data-v="' + esc(i.id) + '">' + esc(i.label) + '</button>';
    }).join('');
  }

  /* ---------- progress ---------- */
  function progress() {
    var urgent = S.flow === 'recovery' && S.rec.when === 'now';
    var shown = STEPS.filter(function (s) { return s !== 'flow' && s !== 'done' && !(urgent && s === 'calendar'); });
    // "How you want it done" is a second page of the same step, not a sixth dot on the bar: the
    // customer is still answering "the work", and a bar that grows mid-flow reads as going backwards.
    var i = shown.indexOf(S.step === 'options' ? 'build' : S.step);
    if (S.step === 'done') i = shown.length;
    return '<ol class="kq-steps">' + shown.map(function (s, n) {
      return '<li class="' + (n < i ? 'done' : n === i ? 'on' : '') + '"><span>' + (n + 1) + '</span>' + STEP_LABEL[s] + '</li>';
    }).join('') + '</ol>';
  }

  /* ---------- step: choose a service ---------- */
  function viewFlow() {
    return '<h2 class="kq-h">What does your car need?</h2><p class="kq-help">Pick one. You&rsquo;ll have a price in under a minute.</p>' +
      '<div class="kq-picks">' + Object.keys(FLOWS).map(function (f) {
        return '<button type="button" class="kq-pick" data-act="flow" data-v="' + f + '"><b>' + esc(FLOWS[f].label) + '</b><small>' + esc(FLOWS[f].sub) + '</small></button>';
      }).join('') + '</div>';
  }

  /* ---------- step: the car ---------- */
  function viewCar() {
    var v = S.vehicle || {}, found = !S.manual && v.make;
    var h = '<h2 class="kq-h">' + (S.flow === 'tyres' ? 'Which car are the tyres for?' : 'Which car is it?') + '</h2>';
    if (!found && !S.manual) {
      return h + '<form class="kq-reg" novalidate><label class="kq-label" for="kq-plate">Enter your registration</label>' +
        '<div class="kq-plate"><span class="kq-gb">UK</span><input id="kq-plate" name="reg" maxlength="8" autocomplete="off" autocapitalize="characters" spellcheck="false" placeholder="AB12 CDE" value="' + esc(S.reg) + '"/></div>' +
        '<button class="kq-btn kq-btn-main" type="submit">Find my car</button>' +
        '<p class="kq-help">We look up the make, engine, fuel and MOT date. <button type="button" class="kq-link" data-act="manual">No reg to hand?</button></p>' +
        '<p class="kq-err" role="alert" hidden></p></form>';
    }
    if (found) {
      var ulez = E.ulezLikely(v), mot = motDate(v);
      var days = motDays(v);
      h += '<div class="kq-car"><div class="kq-car-plate">' + esc(v.registrationNumber || S.reg) + '</div><div><strong>' +
        esc([v.yearOfManufacture, title(v.make)].filter(Boolean).join(' ')) + '</strong><span>' +
        esc([v.engineCapacity ? v.engineCapacity + 'cc' : '', title(v.fuelType), title(v.colour)].filter(Boolean).join(' · ')) + '</span></div></div>' +
        '<ul class="kq-facts">' +
        (mot ? '<li class="' + (days < 45 ? 'warn' : '') + '">' + motPhrase(v) + '</li>' : '') +
        // The nudge used to appear only on the mechanical flow, so someone booking bodywork with
        // three weeks of MOT left was told the date and then nothing. Offer it in every flow:
        // on mechanical it adds the job, elsewhere it flags it for the call.
        (mot && days < 45
          ? (S.flow === 'mechanical'
              ? (S.mech.indexOf('mot') === -1 ? '<li class="kq-add"><button type="button" class="kq-link" data-act="add-mot">+ Add the MOT (' + money(E.priceJob(C, 'mot', S.band).low) + ')</button></li>' : '')
              : '<li class="kq-add"><button type="button" class="kq-link" data-act="flag-mot"' + (S.wantMot ? ' disabled' : '') + '>' + (S.wantMot ? '✓ We&rsquo;ll sort the MOT at the same visit' : '+ Do the MOT at the same visit (' + money(E.priceJob(C, 'mot', S.band).low) + ')') + '</button></li>')
          : '') +
        (ulez === true ? '<li>Likely ULEZ compliant</li>' : ulez === false ? '<li class="warn">Likely not ULEZ compliant · <a href="https://tfl.gov.uk/modes/driving/check-your-vehicle/" target="_blank" rel="noopener">check with TfL</a></li>' : '') +
        '</ul><label class="kq-label" for="kq-model">Model <span class="kq-opt">(optional, sharpens the price)</span></label>' +
        '<input class="kq-input" id="kq-model" maxlength="40" placeholder="e.g. 320d, Focus 1.0 EcoBoost" value="' + esc(S.model) + '"/>';
    } else {
      h += '<p class="kq-note">' + (S.reg ? 'We couldn’t check that reg just now — tell us about the car and we’ll price it from that.' : 'Tell us about the car.') + '</p><div class="kq-row">' +
        '<div><label class="kq-label" for="kq-make">Make &amp; model</label><input class="kq-input" id="kq-make" maxlength="40" placeholder="e.g. Ford Focus" value="' + esc([v.make, S.model].filter(Boolean).join(' ')) + '"/></div>' +
        '<div><label class="kq-label" for="kq-year">Year</label><input class="kq-input" id="kq-year" inputmode="numeric" maxlength="4" placeholder="2016" value="' + esc(v.yearOfManufacture || '') + '"/></div></div>';
    }
    h += '<div class="kq-size">' + viewSize(found) + '</div>';
    return h + nav('flow', 'to-build', 'Next');
  }
  /* The size band decides the labour time, but a customer has no reason to know whether their car counts as
     an estate. So we work it out — from the DVLA record when we have one, otherwise from the make and model
     they typed — and only ask when we genuinely can't tell. They can always correct it. */
  /* What the price is made of, and what the job covers. Folded away by default so the estimate
     still reads as a price rather than an invoice, but there for anyone who wants to check it. */
  /* What a service actually buys, listed on the estimate rather than only on the page that sold
     it. A customer reading "£247" with nothing under it has to take the number on trust; the same
     number above a list of eight jobs is obviously a fair one. It also means the promise and the
     price are read together, which is how the cabin-filter mix-up got as far as it did. */
  function includesFor(l) {
    var job = E.findJob(C, l.id);
    var items = job && job.includes;
    if (!items || !items.length) return '';
    return '<details class="kq-incl"><summary>What&rsquo;s included</summary><ul>' +
      items.map(function (i) { return '<li>' + esc(i) + '</li>'; }).join('') +
      '</ul></details>';
  }

  function breakdown(l) {
    // A service shows its working the same way a repair does, from the rate card's own figures.
    if (typeof l.low === 'number' && l.rateIncVat && l.hoursCharged) {
      var v = isFinite(Number(C.vat_rate)) ? Number(C.vat_rate) : 0.2;
      var ex = Math.round((l.rateIncVat / (1 + v)) * 100) / 100;
      var r = ['<li><span>Labour</span><em>' + l.hoursCharged + ' hrs at ' + money(ex) + ' an hour plus VAT</em></li>'];
      if (l.litres) r.push('<li><span>Oil</span><em>' + l.litres + ' litres' +
        (l.oil === 'specialist' ? ', ' + esc(C.servicing.oil.specialist_brand) + ' specialist' : '') + '</em></li>');
      if (l.dealer) { var sd = dealerLabel(); r.push('<li><span>' + esc(sd.a + ' ' + sd.text) +
        ', same service</span><em>around ' + money(l.dealer) + '</em></li>'); }
      return '<details class="kq-breakdown"><summary>How this is worked out</summary><ul>' + r.join('') + '</ul></details>';
    }
    if (typeof l.low !== 'number' || !l.hours || !l.rate) return '';
    // Hours as charged, which is the book time times the multiplier - that is what the price is
    // built from, so this is the figure that reconciles with it.
    var m = l.multiplier || 1;
    var round1 = function (x) { return Math.round(x * m * 10) / 10; };
    var lo = round1(l.hours[0]), hi = round1(l.hours[1]);
    var hrs = lo === hi ? lo + ' hrs' : lo + '–' + hi + ' hrs';
    // KITH quote the rate ex VAT, the way the workshop says it: "£50 an hour plus VAT".
    var vat = isFinite(Number(C.vat_rate)) ? Number(C.vat_rate) : 0.2;
    var exRate = Math.round((l.rate / (1 + vat)) * 100) / 100;
    var rows = ['<li><span>Labour</span><em>' + hrs + ' at ' + money(exRate) + ' an hour plus VAT</em></li>'];
    if (l.parts && (l.parts[0] || l.parts[1])) {
      rows.push('<li><span>Parts and oil</span><em>' + range(l.parts[0], l.parts[1]) + '</em></li>');
    }
    if (l.dealer) { var dl = dealerLabel(); rows.push('<li><span>' + esc(dl.a + ' ' + dl.text) + ', same job</span><em>around ' + money(l.dealer) + '</em></li>'); }
    var items = (l.includes || []).map(function (x) { return '<li>' + esc(x) + '</li>'; }).join('');
    return '<details class="kq-break"><summary>' + (l.includes ? 'What’s included' : 'How this is worked out') + '</summary>' +
      (items ? '<ul class="kq-inc">' + items + '</ul>' : '') +
      '<ul class="kq-calc">' + rows.join('') + '</ul></details>';
  }

  function viewSize(found) {
    var known = found || S.bandAuto;
    if (known && !S.bandOpen) {
      return '<p class="kq-note kq-sized">Priced as a <b>' + esc(C.bands[S.band].label).toLowerCase() + '</b>. ' +
        '<button type="button" class="kq-link" data-act="band-open">Not right?</button></p>';
    }
    return '<fieldset class="kq-bands"><legend class="kq-label">' +
      (known ? 'Pick the closest' : 'Which is closest? <span class="kq-opt">(so we can price the labour)</span>') + '</legend>' +
      Object.keys(C.bands).map(function (b) {
        return '<label class="kq-chip' + (S.band === b ? ' on' : '') + '"><input type="radio" name="band" value="' + b + '"' +
          (S.band === b ? ' checked' : '') + '/><b>' + esc(C.bands[b].label) + '</b><small>' + esc(C.bands[b].hint) + '</small></label>';
      }).join('') + '</fieldset>';
  }
  function readCar() {
    var m = $('#kq-model'), mk = $('#kq-make'), yr = $('#kq-year');
    if (m) S.model = m.value.trim();
    if (mk) {
      var parts = mk.value.trim().split(' ');
      S.vehicle = Object.assign({}, S.vehicle || {}, { make: parts[0] || '', yearOfManufacture: yr && Number(yr.value) || undefined });
      S.model = parts.slice(1).join(' ');
    }
  }

  /* ---------- step: build (per flow) ---------- */
  function viewBuild() {
    if (S.flow === 'recovery') return viewRecovery();
    if (S.flow === 'tyres') return viewTyres();
    if (S.flow === 'bodywork') return viewBody();
    if (S.flow === 'tuning') return viewTune();
    return viewMech();
  }

  /* Recovery: what happened, where the car is, and whether it needs someone now. Price is a fixed band,
     so the customer sees the figure before they ring rather than after. */
  function viewRecovery() {
    var R = C.recovery, rec = S.rec;
    var sit = R.situations.filter(function (s) { return s.id === rec.what; })[0];
    var line = rec.what && rec.where ? E.recoveryLine(C, rec.what, rec.where) : null;
    var h = '<h2 class="kq-h">What has happened?</h2><p class="kq-help">Fixed prices to our Hackbridge workshop, by distance.</p>' +
      '<div class="kq-picks kq-picks-sm">' + R.situations.map(function (s) {
        return '<button type="button" class="kq-pick' + (rec.what === s.id ? ' on' : '') + '" data-act="rwhat" data-v="' + s.id + '"><b>' + esc(s.label) + '</b><small>' + esc(s.sub) + '</small></button>';
      }).join('') + '</div>';
    if (rec.what) {
      // A postcode gives a real distance, which is what the price is actually based on. The area
      // buttons stay underneath for anyone who doesn't know the postcode they're standing in —
      // broken down on a slip road, that is most people.
      var pc = rec.pc || {};
      h += '<label class="kq-label" for="kq-pc">Where is the car?</label>' +
        '<div class="kq-pcrow">' +
        '<input id="kq-pc" class="kq-pcinput" type="text" inputmode="text" autocomplete="postal-code" ' +
        'placeholder="Postcode, e.g. CR0 2RF" value="' + esc(pc.typed || '') + '"/>' +
        '<button type="button" class="kq-pcbtn" data-act="rpc">Work out my price</button></div>';
      if (pc.state === 'busy') h += '<p class="kq-pcout">Measuring the distance…</p>';
      else if (pc.state === 'bad') h += '<p class="kq-pcout kq-pcbad">We couldn’t find that postcode. Check it, or pick the nearest area below.</p>';
      else if (pc.state === 'off') h += '<p class="kq-pcout kq-pcbad">The postcode lookup isn’t responding. Pick the nearest area below and we’ll confirm on the call.</p>';
      else if (pc.state === 'ok') h += '<p class="kq-pcout kq-pcok"><b>' + esc(pc.label) + '</b> — ' +
        (pc.miles < 1 ? 'under a mile' : 'about ' + pc.miles.toFixed(1) + ' miles') + ' by road from the workshop.</p>';
      h += '<p class="kq-help kq-pcor">Or pick the nearest area:</p><div class="kq-pills">' +
        R.areas.map(function (a) {
          var on = typeof rec.where === 'string' && rec.where === a.id;
          return '<button type="button" class="kq-pill' + (on ? ' on' : '') + '" data-act="rwhere" data-v="' + a.id + '">' + esc(a.label) + '</button>';
        }).join('') + '</div>';
    }
    if (line) {
      h += '<div class="kq-recprice">' + (line.kind === 'fixed'
        ? '<b>' + money(line.low) + '</b><span>' + esc(line.note) + '</span>'
        : '<b>We price this one on the phone</b><span>' + esc(line.note) + '</span>') + '</div>' +
        '<label class="kq-label">When do you need us?</label><div class="kq-pills">' +
        '<button type="button" class="kq-pill' + (rec.when === 'now' ? ' on' : '') + '" data-act="rwhen" data-v="now">Right now</button>' +
        '<button type="button" class="kq-pill' + (rec.when === 'book' ? ' on' : '') + '" data-act="rwhen" data-v="book">Book a time</button></div>' +
        (rec.when === 'now' ? '<p class="kq-note">We will take your details and ring you straight back. Stay with the car if it is safe to, and put your hazards on.</p>' : '');
    }
    return h + nav('car', 'to-estimate', line ? 'Continue' : 'Tell us where the car is', !line);
  }

  /* Postcode -> distance -> price. postcodes.io is the Ordnance Survey's open postcode data, free
     and keyless, so there is nothing to break when a key expires. If it is unreachable the area
     buttons still price the job, which is why they stay on the page. */
  function lookupPostcode() {
    var box = $('#kq-pc');
    if (!box) return;
    var typed = box.value.trim();
    var pc = typed.toUpperCase().replace(/[^A-Z0-9]/g, '');
    if (pc.length < 5 || pc.length > 7) {
      S.rec.pc = { typed: typed, state: 'bad' }; save(); render(); return;
    }
    S.rec.pc = { typed: typed, state: 'busy' }; save(); render();

    var ctrl = typeof AbortController === 'function' ? new AbortController() : null;
    var timer = setTimeout(function () { ctrl && ctrl.abort(); }, 7000);
    fetch('https://api.postcodes.io/postcodes/' + encodeURIComponent(pc), { signal: ctrl && ctrl.signal })
      .then(function (r) { return r.json(); })
      .then(function (j) {
        clearTimeout(timer);
        var res = j && j.result;
        if (!res || !isFinite(res.latitude) || !isFinite(res.longitude)) {
          S.rec.pc = { typed: typed, state: 'bad' }; save(); render(); return;
        }
        var miles = E.milesFrom(C, res.latitude, res.longitude);
        S.rec.pc = { typed: typed, state: 'ok', label: res.postcode, miles: miles };
        // The measured distance becomes the thing the price is worked out from.
        S.rec.where = { miles: miles, label: res.postcode };
        track('recovery_postcode', { miles: Math.round(miles * 10) / 10 });
        save(); render();
      })
      .catch(function () {
        clearTimeout(timer);
        S.rec.pc = { typed: typed, state: 'off' }; save(); render();
      });
  }

  /* MOT expiry comes back with the reg lookup, so the customer never has to remember it. Saying
     only the date leaves them to do the arithmetic; saying how long is what actually makes
     someone book both in one visit. */
  /* £50 off most work, £20 on servicing. A booking that is nothing but servicing takes the
     smaller one; mix in any other work and the £50 applies, because that work is what carries
     it. Every place the offer is shown reads this, so they cannot drift apart. */
  var SERVICE_IDS = ['service-interim', 'service-full', 'service-major', 'oil-filter-change'];
  function coupon() {
    var base = C.coupon;
    if (!base.servicing) return base;
    var jobs = (S.mech || []);
    // An MOT taken alongside a service is still a service booking, so it must not tip the
    // customer into the larger offer. It is kept out of SERVICE_IDS because that list decides
    // engine-size pricing, and an MOT is a flat fee.
    var servicingish = SERVICE_IDS.concat(['mot']);
    var hasOther = S.flow !== 'mechanical' ||
      jobs.some(function (id) { return servicingish.indexOf(id) === -1; }) ||
      Object.keys(S.body || {}).length > 0 ||
      Object.keys(S.wheels || {}).length > 0;
    var hasRealService = jobs.some(function (id) { return SERVICE_IDS.indexOf(id) !== -1; });
    var onlyServicing = hasRealService && !hasOther;
    return stampReg(onlyServicing
      ? { amount: base.servicing.amount, code: base.servicing.code,
          min_spend: base.min_spend, hold_minutes: base.hold_minutes }
      : base);
  }

  /* The code carries the car's registration - KITHPO13VFL rather than KITHSERV20 - so a code
     read out at the counter names the booking it came from, and Logan can see who the discount
     actually went to. Where there is no registration (the customer entered the car by hand) the
     generic code stands, because a code still has to be sayable down a phone. */
  function stampReg(c) {
    var reg = ((S.vehicle || {}).registrationNumber || S.reg || '')
      .toUpperCase().replace(/[^A-Z0-9]/g, '');
    return reg ? Object.assign({}, c, { code: 'KITH' + reg }) : c;
  }

  function motDate(v) {
    var d = (v || {}).motExpiryDate ? new Date(v.motExpiryDate) : null;
    return d && !isNaN(d) ? d : null;
  }
  function motDays(v) {
    var d = motDate(v);
    return d ? Math.round((d - new Date()) / 864e5) : null;
  }
  function motWhen(v) {
    var d = motDate(v);
    return d ? d.toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' }) : '';
  }
  function motHowLong(days) {
    if (days < 0) return '';
    if (days === 0) return 'today';
    if (days === 1) return 'tomorrow';
    if (days < 14) return 'in ' + days + ' days';
    if (days < 60) return 'in ' + Math.round(days / 7) + ' weeks';
    return 'in ' + Math.round(days / 30) + ' months';
  }
  /* One line on the confirmation screen. Nothing is claimed that the DVSA data does not say,
     and an MOT already booked in this job is not nagged about again. */
  function motReminder() {
    var days = motDays(S.vehicle);
    if (days === null) return '';
    var booking = S.mech.indexOf('mot') !== -1 || S.wantMot;
    if (days < 0) {
      return '<p class="kq-motnote warn"><b>Your MOT ran out on ' + motWhen(S.vehicle) + '.</b> ' +
        (booking ? 'We are doing it at this visit.'
                 : 'Until it is retested the car can only be driven to a booked appointment &mdash; tell us and we will test it while it is here.') + '</p>';
    }
    if (booking) {
      return '<p class="kq-motnote"><b>MOT:</b> due ' + motWhen(S.vehicle) + ', and we are doing it at this visit.</p>';
    }
    if (days < 90) {
      return '<p class="kq-motnote"><b>Your MOT is due ' + motWhen(S.vehicle) + ', ' + motHowLong(days) + '.</b> ' +
        'We can do it on the same visit for ' + money(E.priceJob(C, 'mot', S.band).low) + ' &mdash; just say when we call.</p>';
    }
    return '<p class="kq-motnote"><b>MOT:</b> due ' + motWhen(S.vehicle) + ', ' + motHowLong(days) + '. We will remind you nearer the time.</p>';
  }

  function motPhrase(v) {
    var days = motDays(v);
    if (days === null) return '';
    if (days < 0) {
      var over = Math.abs(days);
      return 'MOT expired ' + motWhen(v) + ' &mdash; ' + over + ' day' + (over === 1 ? '' : 's') +
             ' ago. The car can only be driven to a booked test.';
    }
    return 'MOT due ' + motWhen(v) + ' &mdash; ' + motHowLong(days);
  }

  /* Servicing prices off engine size, not body size. The lookup usually hands us the exact
     capacity; where it doesn't, the customer picks a band and we say so rather than guessing a
     price from the model name. */
  /* Engine size, best source first: what the customer picked, then the capacity the lookup gave
     us, then the commonest engine for the body size they already told us. The last of those is a
     guess, so it is never silent - engineSizeUI shows what was assumed and offers to change it. */
  function svcBandId() {
    if (S.ccBand) return S.ccBand;
    var b = S.cc ? E.svcBand(C, S.cc) : null;
    if (b) return b.id;
    return E.ccFromCarSize(S.band);
  }
  function ccIsGuess() { return !S.ccBand && !S.cc; }
  function svcBandKnown() { return !!svcBandId(); }

  /* Engine size. Shown as a confirmation when the lookup gave it to us, as a question when it
     didn't — never silently guessed, because it moves the price by up to £100. */
  function engineSizeUI() {
    var id = svcBandId();
    if (id && S.cc && !S.ccBand) {
      var b = E.svcBandById(C, id);
      return '<p class="kq-ccnote">Priced for your <b>' + S.cc + 'cc</b> engine (' + esc(b.label) + '). ' +
        '<button type="button" class="kq-link" data-act="cc-edit">Not right?</button></p>';
    }
    // Answered or inferred, so it stays a single line. Six options with example cars is a tall
    // list; opened by default it buries everything under it. "Not right?" opens it for the
    // customer whose car is a 1.0 or a 3.0 and whose price would otherwise be wrong.
    if (!S.ccOpen) {
      var cb = E.svcBandById(C, svcBandId());
      return '<p class="kq-ccnote">' + (ccIsGuess() ? 'Priced as a ' : 'Priced as a ') +
        '<b>' + esc(cb.pick || cb.label) + '</b> engine' +
        (ccIsGuess() ? ', going by the size of the car' : ' (' + esc(cb.label) + ')') + '. ' +
        '<button type="button" class="kq-link" data-act="cc-edit">Not right?</button></p>';
    }
    var chosen = S.ccBand;
    return '<div class="kq-ccpick"><label class="kq-label">What size is the engine?</label>' +
      '<p class="kq-help">Pick the one your car is sold as &mdash; a &ldquo;1.6&rdquo; or a &ldquo;2.0 TDI&rdquo;. ' +
      'It is on the boot badge, your insurance, or your V5C. It sets how much oil goes in, so it moves the price.</p>' +
      '<div class="kq-pills kq-ccopts">' + C.servicing.bands.map(function (b) {
        return '<button type="button" class="kq-pill kq-ccopt' + (chosen === b.id ? ' on' : '') +
          '" data-act="ccband" data-v="' + b.id + '">' +
          '<b>' + esc(b.pick || b.label) + '</b>' +
          (b.examples ? '<small>' + esc(b.examples) + '</small>' : '') +
          '<i>' + esc(b.label) + '</i></button>';
      }).join('') + '</div></div>';
  }

  /* Service add-ons. Only shown once a service is chosen, because they only make sense
     alongside one, and never offering what that service already contains. */
  function addonUI() {
    var picked = S.mech.filter(function (id) { return SERVICE_IDS.indexOf(id) !== -1; });
    if (!picked.length || !svcBandKnown()) return '';
    var levels = picked.map(function (id) {
      return { 'service-interim': 'interim', 'service-full': 'full',
               'service-major': 'major', 'oil-filter-change': 'oil-change' }[id];
    }).filter(Boolean);
    var fuel = (S.vehicle || {}).fuelType || '';
    var ids = E.addonsFor(C, levels, fuel);
    if (!ids.length) return '';

    var h = '<div class="kq-addons"><label class="kq-label">Anything else while it is in?</label>';
    h += '<div class="kq-addonlist">' + ids.map(function (id) {
      var l = E.addonLine(C, id, svcBandId(), { parts: S.parts, levels: levels });
      if (!l) return '';
      var on = (S.addons || []).indexOf(id) !== -1;
      var price = l.kind === 'enquiry' ? 'we price it' : l.label;
      return '<label class="kq-addon' + (on ? ' on' : '') + '">' +
        '<input type="checkbox" class="kq-svcaddon" data-svcaddon="' + id + '"' + (on ? ' checked' : '') + '/>' +
        '<span><b>' + esc(l.name) + '</b><small>' + esc(l.note || '') + '</small></span>' +
        '<em>' + esc(price) + '</em></label>';
    }).join('') + '</div></div>';
    return h;
  }

  /* Parts grade. OEM costs 40% more on parts and runs a dearer oil with it; aftermarket is what
     the headline figures assume. Both choices have to be made before a single price exists, so
     the range stays on screen until they are. */
  /* Which service a delta is quoted against. Asked up front, nothing is ticked yet, so the full
     service stands in: it is the one most people are here for and the difference is honest for it. */
  function svcLevelOf(id) {
    return { 'service-interim': 'interim', 'service-full': 'full',
             'service-major': 'major', 'oil-filter-change': 'oil-change' }[id];
  }
  function basisLevel() {
    var picked = S.mech.filter(function (id) { return SERVICE_IDS.indexOf(id) !== -1; });
    return picked.length ? svcLevelOf(picked[0]) : 'full';
  }
  function basisIsGuess() {
    return !S.mech.some(function (id) { return SERVICE_IDS.indexOf(id) !== -1; });
  }

  function partsUI() {
    if (!svcBandKnown()) return '';
    var grades = C.servicing.parts_grade.grades;
    var band = E.svcBandById(C, svcBandId());
    var lvl = basisLevel();
    var base = E.svcPrice(C, lvl, band.id, S.oil || 'standard', false, 'aftermarket');
    var oem = E.svcPrice(C, lvl, band.id, S.oil || 'standard', false, 'oem');
    var diff = Math.round(oem - base);
    var h = '<div class="kq-parts"><label class="kq-label">Which parts?</label>' +
      '<div class="kq-pills kq-choice">' + grades.map(function (g) {
        var best = g.id === 'oem';
        var extra = best && diff > 0 ? '<i>+' + money(diff) + (basisIsGuess() ? ' on a full service' : '') + '</i>' : '';
        return '<button type="button" class="kq-pill kq-ccopt' + (S.parts === g.id ? ' on' : '') +
          '" data-act="parts" data-v="' + g.id + '">' +
          '<b>' + esc(g.label) + (best ? ' <span class="kq-rec">what we’d fit</span>' : '') + '</b>' +
          '<small>' + esc(g.note || '') + '</small>' + extra + '</button>';
      }).join('') + '</div>';
    // The case for OEM is made to the person who has not taken it, and made once. Anyone who has
    // already chosen it is told what they are getting instead of sold it a second time.
    if (S.parts === 'oem') {
      h += '<p class="kq-partsnote">OEM parts throughout, and we run the ' +
        esc(C.servicing.oil.specialist_brand) + ' grade with them.</p>';
    } else if (S.parts === 'aftermarket') {
      h += '<p class="kq-partsadvice"><b>Worth ' + money(diff) + ' to think about.</b> ' +
        'OEM is the same part your car left the factory with, so it fits first time and lasts the ' +
        'interval it was designed for. It also keeps the service record clean if you sell the car ' +
        'or the warranty gets looked at. The aftermarket parts we fit are good ones and we stand ' +
        'behind them &mdash; this is a choice, not a warning.</p>';
    } else {
      h += '<p class="kq-help">Pick one to firm up your price.</p>';
    }
    return h + '</div>';
  }

  /* Oil grade. Logan wants the choice offered, and wants anyone picking standard to hear the
     case for the specialist grade — so the advice appears on that choice, not as a nag before
     they have chosen anything. */
  function oilUI() {
    if (!svcBandKnown()) return '';
    var O = C.servicing.oil, band = E.svcBandById(C, svcBandId());
    var lvlId = basisLevel();
    var pg = S.parts || 'aftermarket';
    var diff = Math.round(E.svcPrice(C, lvlId, band.id, 'specialist', false, pg) -
                          E.svcPrice(C, lvlId, band.id, 'standard', false, pg));
    var on = basisIsGuess() ? ' on a full service' : '';
    var h = '<div class="kq-oil"><label class="kq-label">Which oil?</label>' +
      '<div class="kq-pills kq-choice">' +
      '<button type="button" class="kq-pill kq-ccopt' + (S.oil === 'standard' ? ' on' : '') +
      '" data-act="oil" data-v="standard"><b>Standard</b>' +
      '<small>Matched to your engine&rsquo;s grade and meets the manufacturer&rsquo;s minimum. ' +
      'A perfectly good service.</small></button>' +
      '<button type="button" class="kq-pill kq-ccopt' + (S.oil === 'specialist' ? ' on' : '') +
      '" data-act="oil" data-v="specialist"><b>' + esc(O.specialist_brand) +
      ' specialist <span class="kq-rec">what we&rsquo;d use</span></b>' +
      '<small>Holds its protection longer between services. It is what we run in our own ' +
      'vehicles, and all we put in a KITH service.</small>' +
      '<i>+' + money(Math.round(diff)) + esc(on) + '</i></button></div>';
    if (S.oil === 'standard') {
      h += '<p class="kq-oiladvice"><b>We\u2019d point you at the ' + esc(O.specialist_brand) + ' grade.</b> ' +
        'It holds its protection longer between services, which matters most on turbocharged and ' +
        'direct-injection engines \u2014 most cars built in the last ten years. It is ' +
        money(O.specialist_uplift_ex_vat_per_litre) + ' a litre more, so ' + money(Math.round(diff)) +
        ' on your ' + band.litres + '-litre fill, and it is what we run in our own vehicles. ' +
        'Standard oil is a perfectly safe service and meets the manufacturer\u2019s minimum.</p>';
    } else if (S.oil === 'specialist') {
      h += '<p class="kq-oilnote">' + esc(O.specialist_brand) + ' specialist grade, ' + band.litres + ' litres. ' +
        'We confirm the exact specification your engine needs before we fill it.</p>';
    }
    // No prompt in this block: the parts question above already carries one, and the same
    // sentence twice on a page this short reads as a mistake.
    return h + '</div>';
  }

  /* An MOT is £21 alongside a full or major service. Offer it there and nowhere else. */
  function motBundleUI() {
    var levels = S.mech.map(function (id) {
      return { 'service-full': 'full', 'service-major': 'major' }[id];
    }).filter(Boolean);
    var bundle = E.motWithService(C, levels);
    if (!bundle) return '';
    var on = S.mech.indexOf('mot') !== -1;
    return '<div class="kq-motbundle' + (on ? ' on' : '') + '">' +
      '<button type="button" class="kq-motbtn" data-act="bundle-mot">' +
      (on ? '\u2713 MOT added at ' + money(bundle.low) + ' with this service'
          : '+ Add an MOT for ' + money(bundle.low) + ' with this service') +
      '</button><span>' + money(bundle.low) + ' is the price <b>alongside a full or major service</b>. ' +
      'On its own an MOT is ' + money(bundle.was) + ', so if you drop the service the MOT goes back to ' +
      money(bundle.was) + '.</span></div>';
  }

  function viewMech() {
    var groups = [{ id: 'servicing', label: 'Servicing & MOT' }, { id: 'mechanical', label: 'Repairs' }];
    var h = '<h2 class="kq-h">Build your job card</h2><p class="kq-help">Tick everything you need. Prices are for ' + esc(vehicleName()) + '.</p>';
    groups.forEach(function (g) {
      var jobs = C.jobs.filter(function (j) { return j.cat === g.id; });
      if (!jobs.length) return;
      h += '<h3 class="kq-sub">' + esc(g.label) + '</h3>';
      h += '<div class="kq-jobs">' + jobs.map(function (j) {
        var isSvc = SERVICE_IDS.indexOf(j.id) !== -1;
        var on = S.mech.indexOf(j.id) !== -1;
        var band = isSvc ? svcBandId() : S.band;
        var hint;
        if (isSvc && !band) {
          hint = 'tell us your engine size';
        } else {
          var p = E.priceJob(C, j.id, band, { ai: S.ai[j.id], oil: isSvc ? S.oil : undefined, parts: isSvc ? S.parts : undefined });
          hint = p.kind === 'fixed' ? (p.label || money(p.low))
               : typeof p.low === 'number'
                 ? (isSvc && !S.oil ? range(p.low, p.high) : 'from ' + money(p.low))
                 : p.kind === 'diagnose' ? 'check first' : 'we’ll quote';
        }
        return '<label class="kq-job' + (on ? ' on' : '') + '"><input type="checkbox" value="' + j.id + '"' + (on ? ' checked' : '') + '/><span>' + esc(j.name) + '</span><em>' + esc(hint) + '</em></label>';
      }).join('') + '</div>';
      if (g.id === 'servicing') h += addonUI() + motBundleUI();
    });
    // No gate on engine size any more: it is derived from the car size the customer has already
    // given, and confirmed on the next page. The guard that used to sit here existed because an
    // unknown engine size silently dropped the service and left a £21 MOT standing on its own -
    // which cannot happen now the size is always known.
    var label = !S.mech.length ? 'Pick at least one' : 'Next (' + S.mech.length + ')';
    return h + nav('car', 'to-estimate', label, !S.mech.length);
  }

  /* How the work gets done, on a page of its own after the job card.
     This lived inline twice and was wrong both times: buried under the job list it was missed,
     and hoisted above it the customer met three questions before the thing they came to read.
     On its own page, after Next, each question gets asked once and the job list stays clean. */
  /* Only servicing prices move on oil, parts and engine size, so only a service earns this page.
     Someone here for brake pads goes straight from the job card to their price. */
  function optionsNeeded() {
    return S.flow === 'mechanical' &&
      S.mech.some(function (id) { return SERVICE_IDS.indexOf(id) !== -1; });
  }

  function viewOptions() {
    return '<h2 class="kq-h">How would you like it done?</h2>' +
      '<p class="kq-help">Two quick choices, then your price.</p>' +
      '<div class="kq-basis">' + engineSizeUI() + partsUI() + oilUI() + '</div>' +
      nav('build', 'to-estimate', 'Show my price');
  }

  function viewTyres() {
    var T = C.tyres, sz = S.tyre;
    var num = function (arr) { return arr.map(function (n) { return { id: n, label: n }; }); };
    var h = '<h2 class="kq-h">Read your sidewall, get your price</h2>' +
      '<p class="kq-help">The numbers are moulded into the side of your tyre, like <b>205/55 R16</b>.</p>' +
      '<div class="kq-sidewall"><span>' + sz.w + '</span><i>/</i><span>' + sz.p + '</span><i>R</i><span>' + sz.r + '</span></div>' +
      '<label class="kq-label">Width</label><div class="kq-pills">' + chips(num(T.widths), sz.w, 'tw') + '</div>' +
      '<label class="kq-label">Profile</label><div class="kq-pills">' + chips(num(T.profiles), sz.p, 'tp') + '</div>' +
      '<label class="kq-label">Rim</label><div class="kq-pills">' + chips(num(T.rims), sz.r, 'tr') + '</div>' +
      '<div class="kq-row"><div><label class="kq-label">How many?</label><div class="kq-pills">' + chips([1, 2, 3, 4].map(function (n) { return { id: n, label: n }; }), sz.qty, 'tq') + '</div></div>' +
      '<div><label class="kq-label">Run-flat?</label><div class="kq-pills">' + chips([{ id: 'no', label: 'No' }, { id: 'yes', label: 'Yes' }], sz.rf ? 'yes' : 'no', 'trf') + '</div></div></div>' +
      '<label class="kq-label">Choose your tyre</label><div class="kq-tiers">' + T.tiers.map(function (t) {
        var p = E.tyrePrice(C, { width: sz.w, profile: sz.p, rim: sz.r, runflat: sz.rf }, t.id);
        return '<button type="button" class="kq-tier' + (sz.tier === t.id ? ' on' : '') + '" data-act="tt" data-v="' + t.id + '"><b>' + esc(t.label) + '</b><small>' + esc(t.sub) + '</small>' +
          '<span><strong>' + range(p.lo + p.fit, p.hi + p.fit) + '</strong><small>per tyre, fitted</small></span></button>';
      }).join('') + '</div>';
    return h + nav('car', 'to-estimate', 'Show my price');
  }


  /* Show us where it is, and roughly how big.

     Only asked for damage where the answer changes something -- a dent or a damaged panel. The
     customer taps the panel, drawn on its own and large enough to aim at on a phone, and picks a
     size they can picture. From that we work out whether the repair reaches an edge and has to be
     blended into the panel next door, which is a judgement they should not have to make. */
  function markUI(id, p) {
    var d = S.body[id];
    var dmg = C.bodywork_damage.filter(function (x) { return x.id === d; })[0];
    if (!dmg || !dmg.dent) return '';
    var box = panelBox(id);
    if (!box) return '';
    var pad = Math.max(box.w, box.h) * 0.12;
    var vb = (box.x - pad) + ' ' + (box.y - pad) + ' ' + (box.w + pad * 2) + ' ' + (box.h + pad * 2);
    var m = S.mark[id];
    var r = m ? markSize(m.size).r : 0;
    var blend = m && needsBlend(id, m);

    return '<div class="kq-mark" data-panel="' + id + '">' +
      '<p class="kq-mark-h"><b>Where is it, and how big?</b> Tap the panel to drop a marker.</p>' +
      '<svg class="kq-mark-svg" viewBox="' + vb + '" data-act="mark" data-v="' + id + '" role="button" tabindex="0" ' +
        'aria-label="Tap to show where the damage is on the ' + esc(p.label).toLowerCase() + '">' +
        '<path class="kq-mark-panel" d="' + p.d + '"/>' +
        (m ? '<circle class="kq-mark-ring" cx="' + m.x + '" cy="' + m.y + '" r="' + r + '"/>' +
             '<circle class="kq-mark-dot" cx="' + m.x + '" cy="' + m.y + '" r="2.5"/>' : '') +
      '</svg>' +
      '<div class="kq-mark-sizes">' + MARK_SIZES.map(function (sz) {
        return '<button type="button" class="kq-sizebtn' + (m && m.size === sz.id ? ' on' : '') +
          '" data-act="marksize" data-v="' + id + ':' + sz.id + '"' + (m ? '' : ' disabled') + '>' +
          '<b>' + esc(sz.label) + '</b><small>' + esc(sz.hint) + '</small></button>';
      }).join('') + '</div>' +
      (m
        ? '<p class="kq-mark-out' + (blend ? ' blend' : '') + '">' + (blend
            ? '<b>Close to the edge.</b> The new colour will be carried into the panel next door so the repair does not stop at a hard line. That blending is included.'
            : '<b>Well inside the panel.</b> The repair stays on this panel, so there is nothing to blend into the next one.') + '</p>'
        : '<p class="kq-mark-out kq-mark-wait">Tap the panel above and we will work out whether it needs blending into the next one.</p>') +
      '</div>';
  }


  function wheelsUI() {
    var n = Object.keys(S.wheels).length;
    if (!n) return '';
    var names = CAR_WHEELS.filter(function (w) { return S.wheels[w.id]; })
      .map(function (w) { return w.label.replace(' alloy', ''); });
    return '<div class="kq-dmg kq-dmg-wheel"><div class="kq-dmg-h"><b>' +
      (n === 1 ? '1 alloy wheel' : n + ' alloy wheels') + '</b>' +
      '<button type="button" class="kq-x" data-act="unwheels" data-v="all" aria-label="Clear the wheels">×</button></div>' +
      '<p class="kq-note">' + esc(names.join(', ')) + '. Refinished per wheel &mdash; the price depends on how far gone the rim is, which we confirm when we see them.</p></div>';
  }

  function viewBody() {
    var picked = Object.keys(S.body);
    var h = '<h2 class="kq-h">Tap where it hurts</h2><p class="kq-help">Tap each damaged panel, then tell us what happened to it. Kerbed an alloy? Tap the wheels down the sides.</p>' +
      '<div class="kq-bodywrap"><svg class="kq-carsvg" viewBox="0 0 260 516" role="group" aria-label="Car diagram: choose the damaged panels">' +
      '<rect x="18" y="8" width="224" height="500" rx="70" fill="#f7f8fa" stroke="#dde1e8" stroke-width="2"/>' +
      '<path class="kq-glass" d="M66 154 L194 154 L188 192 L72 192 Z"/><path class="kq-glass" d="M72 322 L188 322 L194 358 L66 358 Z"/>' +
      CAR_PANELS.map(function (p) {
        return '<path class="kq-panel' + (S.body[p.id] ? ' on' : '') + '" d="' + p.d + '" data-act="panel" data-v="' + p.id + '" tabindex="0" role="button" aria-pressed="' + !!S.body[p.id] + '"><title>' + esc(p.label) + '</title></path>';
      }).join('') +
      CAR_WHEELS.map(function (w) {
        return '<rect class="kq-wheel' + (S.wheels[w.id] ? ' on' : '') + '" x="' + w.x + '" y="' + w.y + '" width="' + w.w +
          '" height="' + w.h + '" rx="8" data-act="wheel" data-v="' + w.id + '" tabindex="0" role="button" aria-pressed="' +
          !!S.wheels[w.id] + '"><title>' + esc(w.label) + '</title></rect>';
      }).join('') + '</svg><div class="kq-bodyside">' +
      wheelsUI() +
      (picked.length ? picked.map(function (id) {
        var p = CAR_PANELS.filter(function (x) { return x.id === id; })[0];
        return '<div class="kq-dmg"><div class="kq-dmg-h"><b>' + esc(p.label) + '</b><button type="button" class="kq-x" data-act="unpanel" data-v="' + id + '" aria-label="Remove ' + esc(p.label) + '">×</button></div>' +
          // What the damage looks like, not what we'll do about it — the repair method is our call.
          '<div class="kq-pills">' + C.bodywork_damage.map(function (d) {
            return '<button type="button" class="kq-pill' + (S.body[id] === d.id ? ' on' : '') + '" data-act="dmg" data-v="' + id + ':' + d.id + '"><b>' + esc(d.label) + '</b>' +
              (d.size ? '<small>' + esc(d.size) + '</small>' : '') + '</button>';
          }).join('') + '</div>' + markUI(id, p) + '</div>';
      }).join('') : '<p class="kq-note">Nothing selected yet. Tap a panel on the car.</p>') +
      // A photo settles bodywork faster than any form does, and the customer wants to show us
      // before they commit, not after. So this is an action here, not a note about later.
      (picked.length
        ? '<p class="kq-small kq-photo"><b>Send us a photo and we&rsquo;ll confirm the exact price.</b> ' +
          'It is the quickest way to be sure of the method and the figure. ' +
          '<a href="' + waPhotoLink(picked) + '" target="_blank" rel="noopener" data-act="wa-photo">Send a photo on WhatsApp →</a></p>'
        : '<p class="kq-small">Photos help us price it properly &mdash; you can send one as soon as you have picked a panel.</p>') +
      '</div></div>';
    // The count has to include the wheels, or a customer who picked two alloys and a door is told
    // we are pricing one thing.
    var items = picked.length + Object.keys(S.wheels).length;
    return h + nav('car', 'to-estimate', items ? 'Show my price (' + items + ')' : 'Tap a panel or a wheel', !items);
  }

  function viewTune() {
    var T = C.tuning;
    var h = '<h2 class="kq-h">Put it on the map</h2><p class="kq-help">Pick your engine and stage. Gains are typical for that engine type, and we confirm on the car.</p>' +
      '<label class="kq-label">Engine</label><div class="kq-pills">' + chips(T.fuels.map(function (f) { return { id: f.id, label: f.label }; }), S.tune.fuel, 'tf') + '</div>' +
      '<label class="kq-label" for="kq-bhp">Standard power <span class="kq-opt">(bhp, optional)</span></label>' +
      '<input class="kq-input kq-narrow-in" id="kq-bhp" inputmode="numeric" maxlength="4" placeholder="e.g. 150" value="' + esc(S.tune.bhp) + '"/>' +
      (S.power ? gauge(S.power) : '') +
      '<label class="kq-label">Choose your stage</label><div class="kq-tiers">' + T.stages.map(function (s) {
        return '<button type="button" class="kq-tier' + (S.tune.stage === s.id ? ' on' : '') + '" data-act="ts" data-v="' + s.id + '">' +
          '<b>' + esc(s.label) + (s.flag ? ' <i class="kq-flag">' + esc(s.flag) + '</i>' : '') + '</b><small>' + esc(s.text) + '</small>' +
          '<span><strong>' + range(s.price[0], s.price[1]) + '</strong></span></button>';
      }).join('') + '</div>' +
      '<label class="kq-label">Add to the build</label><div class="kq-jobs">' + T.addons.map(function (a) {
        var on = S.tune.addons.indexOf(a.id) !== -1;
        return '<label class="kq-job' + (on ? ' on' : '') + '"><input type="checkbox" data-addon value="' + a.id + '"' + (on ? ' checked' : '') + '/><span>' + esc(a.label) + '<small>' + esc(a.sub) + '</small></span><em>' + (a.quote_after ? 'we’ll quote' : 'from ' + money(a.price[0])) + '</em></label>';
      }).join('') + '</div>';
    return h + nav('car', 'to-estimate', 'Show my price');
  }
  function gauge(p) {
    var max = Math.max(200, Math.ceil(p.high * 1.15 / 50) * 50), cx = 120, cy = 118, r = 92;
    function pt(v) { var a = Math.PI * (1 - v / max); return [cx + r * Math.cos(a), cy - r * Math.sin(a)]; }
    function arc(v) { var q = pt(v); return 'M' + (cx - r) + ' ' + cy + ' A' + r + ' ' + r + ' 0 0 1 ' + q[0].toFixed(1) + ' ' + q[1].toFixed(1); }
    return '<div class="kq-gauge"><svg viewBox="0 0 240 140" aria-label="Power before and after">' +
      '<path d="' + arc(max) + '" fill="none" stroke="#e4e6ea" stroke-width="14" stroke-linecap="round"/>' +
      '<path d="' + arc(p.stock) + '" fill="none" stroke="#9aa1ad" stroke-width="14" stroke-linecap="round"/>' +
      '<path d="' + arc(p.high) + '" fill="none" stroke="#dc2626" stroke-width="6" stroke-linecap="round" opacity=".35"/>' +
      '<path d="' + arc(p.low) + '" fill="none" stroke="#dc2626" stroke-width="14" stroke-linecap="round"/>' +
      '</svg><div><b>' + p.low + '–' + p.high + ' bhp</b><span>from ' + p.stock + ' bhp standard</span></div></div>';
  }

  function nav(back, act, label, disabled) {
    return '<div class="kq-nav"><button type="button" class="kq-btn kq-btn-ghost" data-act="back" data-v="' + back + '">Back</button>' +
      '<button type="button" class="kq-btn kq-btn-main" data-act="' + act + '"' + (disabled ? ' disabled' : '') + '>' + esc(label) + '</button></div>';
  }

  /* ---------- build the lines ---------- */
  function compute() {
    var lines = [];
    if (S.flow === 'mechanical') {
      // Service levels price off engine size and the chosen oil; everything else off body size.
      // And an MOT costs £21 rather than £50 when it rides along with a full or major service,
      // so the figure in the total has to match the one the button offered.
      // Two passes, deliberately. A service line is dropped when we don't know the engine
      // size, and the first version of this worked the MOT discount out from what was TICKED
      // rather than from what actually priced. A customer whose lookup returned no engine
      // capacity therefore lost the service from their quote and kept the £21 MOT — and booked
      // a £21 MOT on its own. The discount is now derived from the lines that survived.
      var priced = S.mech.map(function (id) {
        if (id === 'mot') return null;                       // second pass
        var isSvc = SERVICE_IDS.indexOf(id) !== -1;
        if (isSvc && !svcBandKnown()) return null;
        return E.priceJob(C, id, isSvc ? svcBandId() : S.band,
                          { ai: S.ai[id], oil: isSvc ? S.oil : undefined, parts: isSvc ? S.parts : undefined });
      }).filter(Boolean);

      var svcLevels = priced.map(function (l) {
        return { 'service-service-full': 'full', 'service-service-major': 'major',
                 'service-full': 'full', 'service-major': 'major' }[l.id];
      }).filter(Boolean);
      var bundle = E.motWithService(C, svcLevels);

      // Chosen add-ons become lines of their own, priced off the same band data.
      var svcLevelsAll = S.mech.map(function (id) {
        return { 'service-interim': 'interim', 'service-full': 'full',
                 'service-major': 'major', 'oil-filter-change': 'oil-change' }[id];
      }).filter(Boolean);
      var addonLines = (S.addons || []).map(function (id) {
        return E.addonLine(C, id, svcBandId(), { parts: S.parts, levels: svcLevelsAll });
      }).filter(function (l) { return l && l.kind !== 'included'; });

      lines = S.mech.map(function (id) {
        if (id !== 'mot') {
          return priced.filter(function (l) { return l.id === id || l.id === 'service-' + id; })[0] || null;
        }
        if (bundle) {
          return { id: 'mot', name: bundle.name, kind: 'fixed', low: bundle.low, high: bundle.low,
                   label: money(bundle.low), note: bundle.note, conditional: true,
                   standalone: bundle.was };
        }
        return E.priceJob(C, 'mot', S.band, { ai: S.ai.mot });
      }).filter(Boolean).concat(addonLines);
    }
    else if (S.flow === 'tyres') lines = [E.tyreLine(C, { width: S.tyre.w, profile: S.tyre.p, rim: S.tyre.r, runflat: S.tyre.rf }, S.tyre.tier, S.tyre.qty)];
    else if (S.flow === 'bodywork') lines = Object.keys(S.body).map(function (id) {
      var p = CAR_PANELS.filter(function (x) { return x.id === id; })[0];
      var line = E.bodyLine(C, p.key, p.label, S.body[id], S.band);
      // What the marker told us about this panel travels with the price, so the estimate can
      // explain the blending rather than leaving the customer to wonder what they paid for.
      if (line && S.mark[id]) {
        line.blend = needsBlend(id, S.mark[id]);
        line.markSize = markSize(S.mark[id].size).label.toLowerCase();
      }
      return line;
    }).filter(Boolean).concat(
      // Kerbed alloys are priced per wheel, alongside whatever the panels come to.
      Object.keys(S.wheels).length ? [E.alloyLine(C, Object.keys(S.wheels).length)].filter(Boolean) : []
    );
    else if (S.flow === 'recovery') {
      var rl = S.rec.what && S.rec.where ? E.recoveryLine(C, S.rec.what, S.rec.where) : null;
      lines = rl ? [rl] : [];
    }
    else if (S.flow === 'tuning') {
      var t = E.tuneLines(C, S.tune.fuel, Number(S.tune.bhp) || 0, S.tune.stage, S.tune.addons);
      lines = t.lines; S.power = t.power;
    }
    S.lines = lines;
    // Bodywork carries a confirmed band around the total: the same scrape is a different job once it's
    // been looked at, so we show the span we stand behind rather than a figure that will move.
    S.totals = S.flow === 'bodywork' ? E.bodyBand(C, E.totals(lines), lines) : E.totals(lines);
  }
  function fetchAi() {
    if (S.flow !== 'mechanical') return Promise.resolve();
    var want = S.mech.filter(function (id) { var j = E.findJob(C, id); return j && j.ai && !S.ai[id]; });
    if (!want.length || !S.vehicle || !S.vehicle.make) return Promise.resolve();
    /* Eight seconds, not twelve. This call only sharpens the wording on a few jobs, and the
       customer is watching a spinner for every second of it. Long enough for a healthy answer,
       short enough that a sick endpoint is a pause rather than an abandonment. */
    return post('/api/estimate', { vehicle: S.vehicle, model: S.model, band: S.band, jobs: want }, 8000).then(function (r) {
      if (r && r.jobs) Object.keys(r.jobs).forEach(function (id) {
        var a = r.jobs[id];
        if (a && typeof a === 'object') { a.note = E.safeNote(a.note); S.ai[id] = a; }   // filtered again here, not just server-side
      });
    });
  }

  /* ---------- step: estimate ---------- */
  function viewEstimate() {
    if (!S.lines.length) return '<div class="kq-loading" role="status"><span class="kq-spin"></span>Working out your price…</div>';
    var t = S.totals, offer = coupon(), eligible = E.couponEligible(C, t, t.unpriced > 0) && !S.offerGone;
    var h = '<div class="kq-result">';
    if (S.power) h += gauge(S.power);
    h += '<p class="kq-for">Your estimate for <strong>' + esc(vehicleName()) + '</strong>' + (S.vehicle && S.vehicle.registrationNumber ? ' <span class="kq-mini-plate">' + esc(S.vehicle.registrationNumber) + '</span>' : '') + '</p>' +
      '<ul class="kq-lines">' + S.lines.map(function (l) {
        var price = typeof l.low === 'number' ? '<b>' + range(l.low, l.high) + '</b>' : '<b class="kq-tbc">' + (l.kind === 'photo' ? 'Send photos' : l.kind === 'diagnose' ? 'Check first' : 'We’ll quote') + '</b>';
        var tags = [];
        if (l.source === 'ai') tags.push('Priced for your car');
        if (l.confidence === 'low') tags.push('Wide range, confirmed before any work');
        if (l.part) tags.push('Panel cost confirmed after we see it');
        // What the customer told us with the marker, said back to them so the price is explained.
        if (l.markSize) tags.push('About the size of a ' + l.markSize);
        if (l.blend === true) tags.push('Near the edge, so blended into the next panel');
        else if (l.blend === false) tags.push('Well inside the panel, no blending needed');
        return '<li class="kq-line"><div><strong>' + esc(l.name) + '</strong>' + (l.note ? '<p>' + esc(l.note) + '</p>' : '') +
          (tags.length ? '<small>' + tags.join(' · ') + '</small>' : '') + includesFor(l) + breakdown(l) + '</div>' + price + '</li>';
      }).join('') + '</ul>';
    if (t.count) {
      h += '<div class="kq-total"><span>Your estimate' + (t.unpriced ? ' so far' : '') + '</span><b>' + rangeOf(t) + '</b></div>';
      if (t.showDealer) {
        var dl2 = dealerLabel();
        h += '<div class="kq-dealer"><span>' + esc(dl2.a + ' ' + dl2.text) + ', typically</span><s>~' + money(t.dealer) + '</s><em>Around ' +
          money(Math.max(0, Math.round((t.dealer - (t.low + t.high) / 2) / 5) * 5)) + ' less with us</em></div>' +
          '<p class="kq-dealer-note">A typical franchised dealer figure for the same work, not a quote from any particular garage. ' +
          'Main dealer labour in London runs around half as much again as ours, and their parts carry a bigger margin.</p>';
      }
    }
    if (eligible) {
      h += '<div class="kq-offer"><div><b>' + money(offer.amount) + ' off if you book online now</b>' +
        '<span>Book a slot in the next <i id="kq-timer">' + fmtLeft() + '</i> and we take ' + money(offer.amount) + ' off your <b>final bill</b>, whatever the job turns out to be. Code ' + esc(offer.code) + '. ' +
        'The figure above is an estimate, not the final price &mdash; we confirm that in writing once we have seen the car, and the ' + money(offer.amount) + ' comes off it.</span></div></div>';
    }
    h += (S.flow === 'recovery'
        ? '<p class="kq-small">A fixed price, inc VAT, to bring the car to our workshop. Nothing is added for traffic or waiting time. Anything we then do to the car is quoted separately, in writing, before it starts.</p>'
        : S.flow === 'bodywork'
        ? '<p class="kq-small"><b>This is an estimate, not the final price</b> &mdash; parts, labour, paint and VAT included, worked out from the same rate card our estimators use. We confirm the exact figure in writing once we have seen the car, and you decide then whether to go ahead. If what we find is more than the photos showed, we tell you before we touch anything &mdash; you owe us nothing for looking. ' +
          (t.low === t.high
            ? 'This is a fixed-method repair, so it is one figure rather than a span.'
            : 'Bodywork moves with how deep the damage goes and what sits behind the panel, which is why we give you the span we stand behind rather than a figure that changes later.') +
          ' We also decide the repair method, so you don&rsquo;t have to. No deposit, paid on collection. 12-month workmanship warranty. Courtesy car available at &pound;36 a day while your car is with us.</p>'
        : '<p class="kq-small">Includes VAT, parts and labour, and it&rsquo;s worked out with the same pricing rules our estimators use, so <b>your job will land inside this range</b>. Book in and we&rsquo;ll send the exact figure for your reg in writing before any work starts. If anything we find changes it, you decide whether to go ahead, and you owe us nothing for looking. 3-month workmanship warranty.</p>') +
      '</div>' +
      '<div class="kq-nav"><button type="button" class="kq-btn kq-btn-ghost" data-act="back" data-v="build">Change the job</button>' +
      '<button type="button" class="kq-btn kq-btn-main" data-act="to-details">' + (eligible ? 'Book and save ' + money(offer.amount) : 'Book this in') + '</button></div>' +
      '<p class="kq-or">or <a href="' + waLink() + '" target="_blank" rel="noopener" data-act="wa">send it to us on WhatsApp</a> · <a href="tel:' + PHONE_TEL + '">call ' + PHONE + '</a></p>';
    return h;
  }
  function fmtLeft() {
    var left = Math.max(0, S.expires - Date.now());
    return String(Math.floor(left / 60000)).padStart(2, '0') + ':' + String(Math.floor(left % 60000 / 1000)).padStart(2, '0');
  }
  function startTimer() {
    clearInterval(TICK);
    if (!S.expires) S.expires = Date.now() + (coupon().hold_minutes || 15) * 60000;
    TICK = setInterval(function () {
      var el = $('#kq-timer');
      if (!el) return;
      el.textContent = fmtLeft();
      if (S.expires - Date.now() <= 0) { clearInterval(TICK); S.offerGone = true; save(); render(); }
    }, 1000);
  }

  /* ---------- step: details ---------- */

  /* Collection and return, charged by distance.

     Asked for only once the box is ticked, so a customer who is driving in is never shown it.
     The bands are the customer's own judgement of how far away they are, which is the only thing
     available without sending their postcode to a mapping service: naming the nearest towns
     against each band makes that judgement easy to get right. */
  function collectBands() {
    return ((C.collection_inc_vat && C.collection_inc_vat.bands) || []);
  }
  function collectBand(id) {
    var b = collectBands().filter(function (x) { return x.id === id; });
    return b.length ? b[0] : null;
  }
  /* S.lead stays null until the customer submits the details form, so everything that reads it
     before then has to tolerate that. Missing this threw on the first render of the details
     step, which took the whole booking form down with it. */
  function lead() { return S.lead || {}; }
  function collectUI() {
    if (!lead().collect || !collectBands().length) return '';
    var chosen = collectBand(S.collectBand);
    return '<div class="kq-collect">' +
      '<p class="kq-collect-h"><b>How far are you from the workshop?</b> We collect and bring it back; ' +
      'the charge covers both journeys.</p>' +
      '<div class="kq-collect-opts">' + collectBands().map(function (b) {
        return '<button type="button" class="kq-collect-opt' + (S.collectBand === b.id ? ' on' : '') +
          '" data-act="collectband" data-v="' + b.id + '"><b>' + esc(b.label) + '</b>' +
          '<small>' + esc(b.hint) + '</small>' +
          '<em>' + (b.price ? money(b.price) : 'We\u2019ll price it') + '</em></button>';
      }).join('') + '</div>' +
      (chosen
        ? '<p class="kq-collect-out">' + (chosen.price
            ? '<b>' + money(chosen.price) + '</b> added for collection and return, there and back.'
            : '<b>We\u2019ll price this for you.</b> Further than 10 miles is quoted rather than guessed, and we tell you before we set off.') + '</p>'
        : '<p class="kq-collect-out kq-collect-wait">Pick the one that fits and we will add it to the job.</p>') +
      '</div>';
  }

  function viewDetails() {
    return '<h2 class="kq-h">Where shall we send it?</h2><p class="kq-help">We&rsquo;ll check the detail for your car and send the full written estimate. Then pick your slot.</p>' +
      summaryStrip() +
      '<form class="kq-lead" novalidate><div class="kq-row">' +
      '<div><label class="kq-label" for="kq-name">Name</label><input class="kq-input" id="kq-name" value="' + esc(lead().name || '') + '" name="name" autocomplete="name" required maxlength="60"/></div>' +
      '<div><label class="kq-label" for="kq-phone">Mobile</label><input class="kq-input" id="kq-phone" value="' + esc(lead().phone || '') + '" name="phone" type="tel" inputmode="tel" autocomplete="tel" required maxlength="20"/></div></div>' +
      '<div class="kq-row"><div><label class="kq-label" for="kq-email">Email <span class="kq-opt">(optional)</span></label><input class="kq-input" id="kq-email" value="' + esc(lead().email || '') + '" name="email" type="email" autocomplete="email" maxlength="80"/></div>' +
      '<div><label class="kq-label" for="kq-reg2">Reg</label><input class="kq-input" id="kq-reg2" name="reg" maxlength="10" value="' + esc((S.vehicle && S.vehicle.registrationNumber) || S.reg) + '"/></div></div>' +
      '<label class="kq-check"><input type="checkbox" name="collect"' + (lead().collect ? ' checked' : '') + ' data-act="collect-toggle"/> Please collect and return my car</label>' +
      collectUI() +
      '<button class="kq-btn kq-btn-main" type="submit">' + (S.flow === 'recovery' && S.rec.when === 'now' ? 'Send this and call me back' : 'Next: pick my slot') + '</button>' +
      '<p class="kq-err" role="alert" hidden></p>' +
      '<p class="kq-small">We only use your details to arrange this job.</p></form>' +
      '<div class="kq-nav"><button type="button" class="kq-btn kq-btn-ghost" data-act="back" data-v="estimate">Back to the price</button></div>';
  }
  function summaryStrip() {
    var t = S.totals;
    return '<div class="kq-strip"><div><b>' + esc(FLOWS[S.flow].label) + '</b><span>' + esc(vehicleName()) + '</span></div>' +
      (t && t.count ? '<div class="kq-strip-p"><b>' + rangeOf(t) + '</b>' + (!S.offerGone && E.couponEligible(C, t, t.unpriced > 0) ? '<span>less ' + money(coupon().amount) + ' if booked now <i id="kq-timer">' + fmtLeft() + '</i></span>' : '') + '</div>' : '') + '</div>';
  }

  /* ---------- step: calendar ---------- */
  function viewCalendar() {
    var cal = FLOWS[S.flow].cal, days = E.bookableDays(C, cal);
    var day = S.day ? days.filter(function (d) { return d.key === S.day; })[0] : null;
    // The soonest slot the workshop actually has. This is the honest version of urgency: it is
    // true, it is checkable, and when the next free slot is two days out it does the same job
    // that marking slots "full" would — without telling anyone something that isn't so.
    var first = days[0];
    var next = '';
    if (first && first.slots.length) {
      var today = new Date(); today.setHours(0, 0, 0, 0);
      var when = new Date(first.key + 'T00:00:00');
      var gap = Math.round((when - today) / 86400000);
      var label = gap === 1 ? 'tomorrow' : first.long.replace(/,.*$/, '');
      next = '<p class="kq-next"><b>Next free ' + (cal === 'bodywork' ? 'drop-off' : 'slot') +
        ':</b> ' + esc(label) + ' at ' + esc(first.slots[0]) +
        (gap > 2 ? ' &mdash; we are booked up until then' : '') + '</p>';
    }
    return '<h2 class="kq-h">Pick your ' + (cal === 'bodywork' ? 'drop-off' : 'slot') + '</h2>' +
      '<p class="kq-help">' + (cal === 'bodywork' ? 'Bodywork stays with us, so this is when you drop it off.' : 'Most mechanical jobs are done the same day.') + '</p>' +
      next +
      summaryStrip() +
      '<div class="kq-days">' + days.map(function (d) {
        return '<button type="button" class="kq-day' + (S.day === d.key ? ' on' : '') + '" data-act="day" data-v="' + d.key + '"><i>' + d.dow + '</i><b>' + d.dom + '</b><span>' + d.mon + '</span></button>';
      }).join('') + '</div>' +
      (day ? '<label class="kq-label">' + esc(day.long) + '</label><div class="kq-pills">' +
        day.slots.map(function (s) { return '<button type="button" class="kq-pill' + (S.time === s ? ' on' : '') + '" data-act="time" data-v="' + s + '">' + s + '</button>'; }).join('') + '</div>' : '') +
      '<div class="kq-nav"><button type="button" class="kq-btn kq-btn-ghost" data-act="skip-slot">I&rsquo;ll sort the time later</button>' +
      '<button type="button" class="kq-btn kq-btn-main" data-act="confirm"' + (S.day && S.time ? '' : ' disabled') + '>Confirm my booking</button></div>' +
      // Last step before booking, and the one where people remember the panel they forgot.
      // Without this the only way back is the browser button, which drops the whole widget.
      '<div class="kq-nav kq-nav-amend"><button type="button" class="kq-btn kq-btn-link" data-act="back" data-v="' +
      (S.flow === 'recovery' ? 'car' : 'build') + '">&larr; Add or change something on the job</button></div>';
  }

  /* ---------- step: done ---------- */
  function viewDone() {
    var booked = S.day && S.time, cal = FLOWS[S.flow].cal;
    var when = booked ? new Date(S.day).toLocaleDateString('en-GB', { weekday: 'long', day: 'numeric', month: 'long' }) + ' at ' + S.time : null;
    var urgent = S.flow === 'recovery' && S.rec.when === 'now';
    if (urgent) {
      return '<div class="kq-done"><h2 class="kq-h">We&rsquo;ve got it. Sit tight.</h2>' +
        '<p>Your details are with us now and you are at the top of the queue. We&rsquo;ll ring you straight back on the number you gave us.</p>' +
        '<p class="kq-small">If you are on a live carriageway, get out of the car and stand behind the barrier. If you feel unsafe, ring 999 first, then us.</p>' +
        '<div class="kq-nav-wrap"><a class="kq-btn kq-btn-main" href="tel:' + PHONE_TEL + '">Call us now on ' + PHONE + '</a> ' +
        '<a class="kq-btn kq-btn-wa" href="' + waLink() + '" target="_blank" rel="noopener">Send our location on WhatsApp</a></div></div>';
    }
    return '<div class="kq-done"><h2 class="kq-h">' + (booked ? 'You&rsquo;re booked in.' : 'Your estimate is on its way.') + '</h2>' +
      (booked ? '<p class="kq-big-when">' + esc(when) + '</p><p>' + (cal === 'bodywork' ? 'Drop the car to us at Unit 1, Soho Mills, Hackbridge SM6 7HN.' : 'Bring it to Unit 1, Soho Mills, Hackbridge SM6 7HN.') + ' We&rsquo;ll call to confirm and send the written price first.</p>'
        : '<p>We&rsquo;ve got your details and will be in touch, usually within 30 minutes during opening hours (Mon–Sat 8am–8pm).</p>') +
      (booked && !S.offerGone ? '<p class="kq-saved"><b>' + money(coupon().amount) + ' off your final bill</b> · code ' + esc(coupon().code) + ' · applied when we invoice, whatever the job comes to</p>' : '') +
      // They came for a repair; the MOT date is something we happen to know and they often don't.
      // Worth one line on the way out, whichever flow they used.
      motReminder() +
      (S.flow === 'bodywork' ? '<p>Send us photos of the damage and we can have the parts ready:</p>' : '') +
      '<div class="kq-nav-wrap"><a class="kq-btn kq-btn-wa" href="' + waLink() + '" target="_blank" rel="noopener">' + (S.flow === 'bodywork' ? 'Send photos on WhatsApp' : 'Message us on WhatsApp') + '</a> ' +
      '<a class="kq-btn kq-btn-ghost" href="tel:' + PHONE_TEL + '">Call ' + PHONE + '</a></div></div>';
  }
  // Opens WhatsApp with the panels the customer has tapped already written out, so all they have
  // to add is the photograph. Used before a price exists, which is why it does not touch S.lines.
  function waPhotoLink(picked) {
    var names = (picked || []).map(function (id) {
      var p = CAR_PANELS.filter(function (x) { return x.id === id; })[0];
      return p ? p.label : id;
    });
    var msg = 'Hi KITH, I would like a price for bodywork on my ' + vehicleName() +
      (S.vehicle && S.vehicle.registrationNumber ? ' (' + S.vehicle.registrationNumber + ')' : '') + '.\n' +
      (names.length ? 'Damage to: ' + names.join(', ') + '.\n' : '') +
      'Photo attached.';
    return 'https://wa.me/' + WA + '?text=' + encodeURIComponent(msg);
  }

  function waLink() {
    var msg = 'Hi KITH, I got an online estimate for ' + vehicleName() + (S.vehicle && S.vehicle.registrationNumber ? ' (' + S.vehicle.registrationNumber + ')' : '') + ':\n' +
      S.lines.map(function (l) { return '• ' + l.name + (typeof l.low === 'number' ? ': ' + range(l.low, l.high) : ''); }).join('\n') +
      (S.day && S.time ? '\nSlot: ' + S.day + ' ' + S.time : '');
    return 'https://wa.me/' + WA + '?text=' + encodeURIComponent(msg);
  }

  /* ---------- lead out: email always, CRM when configured ---------- */
  function leadPayload() {
    var v = S.vehicle || {}, t = S.totals;
    return {
      priority: (S.flow === 'recovery' && S.rec.when === 'now') ? 'urgent' : (S.day && S.time ? 'hot' : 'warm'),
      source: 'Website instant quote',
      stage: 'intake',
      name: lead().name, phone: lead().phone, email: lead().email || '',
      reg: lead().reg || v.registrationNumber || '',
      vehicle: { make: v.make || '', model: S.model || '', year: v.yearOfManufacture || '', engine_cc: v.engineCapacity || '', fuel: v.fuelType || '', size: C.bands[S.band].label, motExpiry: v.motExpiryDate || '' },
      service: FLOWS[S.flow].label,
      jobs: S.lines.map(function (l) { return { name: l.name, low: l.low, high: l.high, source: l.source || l.kind, hours: l.hours || null, parts: l.parts || null }; }),
      webEstimate: t && t.count ? { lo: t.low, hi: t.high } : null,
      requestedSlot: S.day && S.time ? { calendar: FLOWS[S.flow].cal, date: S.day, time: S.time } : null,
      collection: !!lead().collect,
      wantMot: !!S.wantMot,
      coupon: (S.day && S.time && !S.offerGone) ? { code: coupon().code, amount: coupon().amount, minSpend: coupon().min_spend } : null,
      priceBookVersion: C.version,
      log: [{ at: new Date().toISOString(), by: 'Website', text: ((S.flow === 'recovery' && S.rec.when === 'now') ? 'URGENT: needs recovery now, call straight back' : S.day && S.time ? 'HOT: accepted the range and booked ' + S.day + ' ' + S.time : 'Estimate sent, no slot picked') }]
    };
  }
  function sendLead() {
    var d = leadPayload(), id = S.lead.id || (S.lead.id = 'web-' + Date.now().toString(36));
    var fd = new FormData();
    fd.append('access_key', WEB3FORMS_KEY);
    fd.append('subject', (d.priority === 'urgent' ? 'URGENT RECOVERY' : d.priority === 'hot' ? 'BOOKED' : 'Estimate') + ': ' + d.service + ' · ' + vehicleName() + (d.webEstimate ? ' · ' + range(d.webEstimate.lo, d.webEstimate.hi) : ''));
    fd.append('from_name', 'KITH website instant quote');
    fd.append('Name', d.name); fd.append('Phone', d.phone);
    if (d.email) { fd.append('email', d.email); fd.append('Email', d.email); }
    fd.append('Registration', d.reg || '-');
    fd.append('Vehicle', [d.vehicle.year, d.vehicle.make, d.vehicle.model].filter(Boolean).join(' ') + ' · ' + d.vehicle.size);
    fd.append('Service', d.service);
    fd.append('Quote', d.jobs.map(function (j) { return '• ' + j.name + (typeof j.low === 'number' ? ': ' + range(j.low, j.high) : ': to confirm'); }).join('\n') + (d.webEstimate ? '\nEstimate: ' + range(d.webEstimate.lo, d.webEstimate.hi) : ''));
    fd.append('Slot', d.requestedSlot ? d.requestedSlot.date + ' ' + d.requestedSlot.time + ' (' + d.requestedSlot.calendar + ')' : 'not picked');
    fd.append('Collection', d.collection ? 'Yes, please collect' : 'No');
    if (d.vehicle.motExpiry) {
      var md = motDays(S.vehicle);
      fd.append('MOT', d.vehicle.motExpiry + (md === null ? '' :
        md < 0 ? ' — EXPIRED ' + Math.abs(md) + ' days ago' : ' — ' + motHowLong(md)) +
        (d.wantMot ? ' · CUSTOMER WANTS THE MOT DOING THIS VISIT' : ''));
    }
    fd.append('Discount', d.coupon ? d.coupon.code + ' · £' + d.coupon.amount : 'none');
    fd.append('Price book', d.priceBookVersion);
    var email = fetch('https://api.web3forms.com/submit', { method: 'POST', body: fd }).then(function (r) { return r.json(); }).then(function (j) { return !!j.success; }).catch(function () { return false; });
    var crm = Promise.resolve('not connected');
    if (C.crm && C.crm.supabase_url && C.crm.anon_key) {
      crm = fetch(C.crm.supabase_url.replace(/\/$/, '') + '/rest/v1/' + (C.crm.table || 'jobs') + '?on_conflict=id', {
        method: 'POST',
        headers: { apikey: C.crm.anon_key, Authorization: 'Bearer ' + C.crm.anon_key, 'Content-Type': 'application/json', Prefer: 'resolution=merge-duplicates,return=minimal' },
        body: JSON.stringify({ id: id, data: d, updated_at: new Date().toISOString() })
      }).then(function (r) { return r.ok ? 'sent' : 'failed ' + r.status; }).catch(function () { return 'failed'; });
    }
    return Promise.all([email, crm]).then(function (r) { return { emailed: r[0], crm: r[1] }; });
  }

  /* ---------- render + events ---------- */
  function render() {
    var body = S.step === 'flow' ? viewFlow() : S.step === 'car' ? viewCar() : S.step === 'build' ? viewBuild() :
      S.step === 'options' ? viewOptions() :
      S.step === 'estimate' ? viewEstimate() : S.step === 'details' ? viewDetails() : S.step === 'calendar' ? viewCalendar() : viewDone();
    root.innerHTML = (C.draft ? '<p class="kq-draft">Draft prices: still being checked by KITH.</p>' : '') +
      (S.step === 'flow' ? '' : progress()) + '<div class="kq-body">' + body + '</div>';
    if (S.step === 'car') bindCar();
    if (S.step === 'build') bindBuild();
    if (S.step === 'details') bindDetails();
    if ((S.step === 'estimate' || S.step === 'details' || S.step === 'calendar') && !S.offerGone && S.expires) startTimer(); else clearInterval(TICK);
  }
  function bindCar() {
    var f = $('.kq-reg');
    if (f) f.addEventListener('submit', function (e) {
      e.preventDefault();
      var reg = f.reg.value.toUpperCase().replace(/[^A-Z0-9]/g, ''), err = $('.kq-err');
      if (!/^[A-Z0-9]{2,8}$/.test(reg)) { err.textContent = 'Please check the registration.'; err.hidden = false; return; }
      S.reg = reg; track('quote_start', { flow: S.flow });
      var b = f.querySelector('button[type=submit]'); b.disabled = true; b.textContent = 'Finding your car…';
      post('/api/vehicle', { reg: reg }, 8000).then(function (r) {
        if (r.vehicle) {
          S.vehicle = r.vehicle; S.manual = false;
          // The MOT History API gives the model name, which the DVLA's does not. Use it: it sharpens
          // the estimate and saves the customer typing it.
          if (r.vehicle.model && !S.model) S.model = r.vehicle.model;
          // Band from the engine size when we have it, otherwise from the make and model.
          S.band = E.bandFromText(C, [r.vehicle.make, r.vehicle.model].filter(Boolean).join(' ')) || E.guessBand(r.vehicle);
          if (r.vehicle.engineCapacity) S.cc = Number(r.vehicle.engineCapacity) || null;
          S.bandAuto = true; S.bandOpen = false;
          track('vehicle_found'); render(); save();
        }
        else if (r._status === 404) { b.disabled = false; b.textContent = 'Find my car'; err.innerHTML = 'We couldn’t find that reg. Check it, or <button type="button" class="kq-link" data-act="manual">enter the car yourself</button>.'; err.hidden = false; }
        else { S.vehicle = { registrationNumber: reg }; S.manual = true; render(); save(); }
      });
    });
    $$('input[name=band]').forEach(function (r) {
      r.addEventListener('change', function () {
        S.band = r.value; S.bandAuto = false;   // their choice stands; stop guessing over it
        $$('.kq-chip').forEach(function (c) { c.classList.toggle('on', c.querySelector('input').checked); });
        save();
      });
    });
    // Work the size out of the make and model as they type, so the question never has to be asked.
    var mk = $('#kq-make'), box = $('.kq-size');
    if (mk && box) mk.addEventListener('input', function () {
      if (S.bandOpen) return;                   // they've opened the picker; leave their choice alone
      var b = E.bandFromText(C, mk.value);
      var next = b || '', was = S.bandAuto ? S.band : '';
      if (next === was) return;
      if (b) { S.band = b; S.bandAuto = true; } else { S.bandAuto = false; }
      box.innerHTML = viewSize(false);
      bindSize();
      save();
    });
    bindSize();
  }
  function bindSize() {
    var open = $('[data-act="band-open"]');
    if (open) open.addEventListener('click', function () {
      S.bandOpen = true;
      var box = $('.kq-size');
      if (box) { box.innerHTML = viewSize(false); bindSize(); }
      $$('input[name=band]').forEach(function (r) {
        r.addEventListener('change', function () {
          S.band = r.value; S.bandAuto = false;
          $$('.kq-chip').forEach(function (c) { c.classList.toggle('on', c.querySelector('input').checked); });
          save();
        });
      });
    });
  }
  function bindBuild() {
    // Service add-ons are their own checkboxes with their own list; data-addon is the tuning
    // flow's and is read differently, so they are deliberately kept apart.
    $$('.kq-addon input[data-svcaddon]').forEach(function (c) {
      c.addEventListener('change', function () {
        var id = c.getAttribute('data-svcaddon');
        S.addons = S.addons || [];
        var i = S.addons.indexOf(id);
        if (c.checked && i === -1) { S.addons.push(id); track('quote_addon', { id: id }); }
        if (!c.checked && i !== -1) S.addons.splice(i, 1);
        save(); render();
      });
    });
    $$('.kq-job input[type=checkbox]').forEach(function (c) {
      c.addEventListener('change', function () {
        readBuild();
        var list = c.hasAttribute('data-addon') ? S.tune.addons : S.mech, i = list.indexOf(c.value);
        if (c.checked && i === -1) list.push(c.value);
        if (!c.checked && i !== -1) list.splice(i, 1);
        save(); render();
      });
    });
    var bhp = $('#kq-bhp');
    if (bhp) bhp.addEventListener('change', function () { S.tune.bhp = bhp.value.replace(/\D/g, ''); var t = E.tuneLines(C, S.tune.fuel, Number(S.tune.bhp) || 0, S.tune.stage, S.tune.addons); S.power = t.power; save(); render(); });
  }
  function readBuild() { var b = $('#kq-bhp'); if (b) S.tune.bhp = b.value.replace(/\D/g, ''); }
  function bindDetails() {
    var f = $('.kq-lead');
    var box = f.querySelector('input[name=collect]');
    if (box) box.addEventListener('change', function () {
      // Keep whatever has been typed so far: render() rebuilds the form from state, and losing a
      // half-typed phone number because someone ticked a box is the kind of thing nobody reports,
      // they just leave.
      S.lead = {
        id: S.lead && S.lead.id, name: f.name.value, phone: f.phone.value,
        email: f.email.value, reg: f.reg.value, collect: box.checked,
      };
      if (!box.checked) S.collectBand = '';
      save(); render();
    });
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var err = f.querySelector('.kq-err'), name = f.name.value.trim(), phone = f.phone.value.replace(/[^\d+]/g, '');
      if (!name || phone.length < 10) { err.textContent = 'Please add your name and a mobile number so we can confirm.'; err.hidden = false; return; }
      S.lead = { id: S.lead && S.lead.id, name: name, phone: phone, email: f.email.value.trim(), reg: f.reg.value.toUpperCase().trim(), collect: f.collect.checked, collectBand: S.collectBand };
      var b = f.querySelector('button[type=submit]'); b.disabled = true; b.textContent = 'Saving…';
      sendLead().then(function (res) {
        track('generate_lead', { value: S.totals ? S.totals.low : 0, currency: 'GBP', flow: S.flow });
        if (!res.emailed && res.crm !== 'sent') { b.disabled = false; b.textContent = S.flow === 'recovery' && S.rec.when === 'now' ? 'Send this and call me back' : 'Next: pick my slot'; err.innerHTML = 'That didn’t send. Please <a href="tel:' + PHONE_TEL + '">call ' + PHONE + '</a> or <a href="' + waLink() + '" target="_blank" rel="noopener">WhatsApp us</a>.'; err.hidden = false; return; }
        if (S.flow === 'recovery' && S.rec.when === 'now') { S.sent = true; track('quote_urgent'); try { sessionStorage.removeItem('kq2'); } catch (x) {} go('done'); return; }
        go('calendar');
      });
    });
  }

  root.addEventListener('click', function (e) {
    var el = e.target.closest ? e.target.closest('[data-act]') : null;
    if (!el || !root.contains(el)) return;
    var a = el.dataset.act, v = el.dataset.v;
    if (a === 'flow') { S.flow = v; track('quote_flow', { flow: v }); go(S.vehicle && !S.manual ? 'build' : 'car'); }
    else if (a === 'manual') { S.manual = true; S.vehicle = S.vehicle || {}; render(); }
    else if (a === 'back') { if (S.step === 'build') readBuild(); if (S.step === 'car') readCar(); go(v); }
    else if (a === 'rwhat') { S.rec.what = v; save(); render(); }
    else if (a === 'rwhere') { S.rec.where = v; S.rec.pc = null; save(); render(); }
    else if (a === 'rpc') { lookupPostcode(); }
    else if (a === 'rwhen') { S.rec.when = v; save(); render(); }
    else if (a === 'add-mot') { if (S.mech.indexOf('mot') === -1) S.mech.push('mot'); track('quote_add_mot'); save(); render(); }
    // Outside the mechanical flow there is no job card to add it to, so record the intent and
    // put it on the booking the workshop receives.
    else if (a === 'ccband') { S.ccBand = v; S.ccOpen = false; save(); render(); }
    // Opens the picker rather than wiping what we have: the customer is checking an assumption,
    // and clearing it first would blank the prices they are standing in front of.
    else if (a === 'cc-edit') { S.ccOpen = true; save(); render(); }
    else if (a === 'oil') { S.oil = v; track('quote_oil', { grade: v }); save(); render(); }
    else if (a === 'parts') { S.parts = v; track('quote_parts', { grade: v }); save(); render(); }
    else if (a === 'bundle-mot') {
      var i = S.mech.indexOf('mot');
      if (i === -1) { S.mech.push('mot'); track('quote_mot_bundle'); } else { S.mech.splice(i, 1); }
      save(); render();
    }
    else if (a === 'flag-mot') { S.wantMot = true; track('quote_add_mot', { flow: S.flow }); save(); render(); }
    else if (a === 'to-build') { readCar(); go('build'); }
    else if (a === 'to-estimate') {
      readBuild();
      // One page between the job card and the price, and only where it has something to ask.
      if (S.step === 'build' && optionsNeeded()) { go('options'); return; }
      S.lines = []; go('estimate');
      /* The AI pass sharpens a few job notes; it is not where the price comes from. When it was
         allowed to reject - the endpoint down, a timeout, anything - nothing after it ran, so
         compute() never happened and the customer sat on "Working out your price..." forever with
         a perfectly good rate-card figure sitting uncalculated. Swallowing the failure here means
         the price always arrives, with or without the embellishment. */
      fetchAi().catch(function () {}).then(function () {
        compute();
        if (!S.expires) S.expires = Date.now() + (coupon().hold_minutes || 15) * 60000;
        track('quote_price', { value: S.totals.low, currency: 'GBP', flow: S.flow });
        save(); render();
      });
    }
    else if (a === 'to-details') { track('quote_book_click'); go('details'); }
    else if (a === 'day') { S.day = v; S.time = null; save(); render(); }
    else if (a === 'time') { S.time = v; save(); render(); }
    else if (a === 'skip-slot') { S.day = null; S.time = null; S.sent = true; save(); go('done'); }
    else if (a === 'confirm') {
      el.disabled = true; el.textContent = 'Booking…';
      sendLead().then(function () { S.sent = true; track('quote_booked', { value: S.totals ? S.totals.low : 0, currency: 'GBP' }); try { sessionStorage.removeItem('kq2'); } catch (x) {} go('done'); });
    }
    else if (a === 'panel') { if (S.body[v]) delete S.body[v]; else S.body[v] = C.bodywork_damage[0].id; save(); render(); }
    else if (a === 'unpanel') { delete S.body[v]; delete S.mark[v]; save(); render(); }
    else if (a === 'dmg') { var p = v.split(':'); S.body[p[0]] = p[1]; save(); render(); }
    else if (a === 'collectband') { S.collectBand = v; save(); render(); }
    else if (a === 'wheel') { if (S.wheels[v]) delete S.wheels[v]; else S.wheels[v] = true; S.lines = []; save(); render(); }
    else if (a === 'unwheels') { S.wheels = {}; S.lines = []; save(); render(); }
    else if (a === 'marksize') { var ms = v.split(':'); if (S.mark[ms[0]]) { S.mark[ms[0]].size = ms[1]; S.lines = []; save(); render(); } }
    else if (a === 'tw') { S.tyre.w = Number(v); save(); render(); }
    else if (a === 'tp') { S.tyre.p = Number(v); save(); render(); }
    else if (a === 'tr') { S.tyre.r = Number(v); save(); render(); }
    else if (a === 'tq') { S.tyre.qty = Number(v); save(); render(); }
    else if (a === 'trf') { S.tyre.rf = v === 'yes'; save(); render(); }
    else if (a === 'tt') { S.tyre.tier = v; save(); render(); }
    else if (a === 'tf') { S.tune.fuel = v; readBuild(); var t1 = E.tuneLines(C, v, Number(S.tune.bhp) || 0, S.tune.stage, S.tune.addons); S.power = t1.power; save(); render(); }
    else if (a === 'ts') { S.tune.stage = v; readBuild(); var t2 = E.tuneLines(C, S.tune.fuel, Number(S.tune.bhp) || 0, v, S.tune.addons); S.power = t2.power; save(); render(); }
    else if (a === 'wa') track('quote_whatsapp');
  });

  /* Placing the marker. The click arrives in screen pixels; the panel is drawn in the diagram's
     units, so it goes back through the SVG's own transform rather than being approximated from
     the bounding rectangle, which is wrong as soon as the viewBox is not square. */
  root.addEventListener('click', function (e) {
    var svg = e.target.closest ? e.target.closest('.kq-mark-svg') : null;
    if (!svg) return;
    var id = svg.getAttribute('data-v');
    var box = panelBox(id);
    if (!box) return;
    var pt, x, y;
    if (svg.createSVGPoint && svg.getScreenCTM) {
      pt = svg.createSVGPoint(); pt.x = e.clientX; pt.y = e.clientY;
      var loc = pt.matrixTransform(svg.getScreenCTM().inverse());
      x = loc.x; y = loc.y;
    } else {
      var r = svg.getBoundingClientRect(), vb = svg.viewBox.baseVal;
      x = vb.x + (e.clientX - r.left) / r.width * vb.width;
      y = vb.y + (e.clientY - r.top) / r.height * vb.height;
    }
    // Keep it on the panel: a tap just outside still reads as "about here".
    x = Math.max(box.x, Math.min(box.x + box.w, x));
    y = Math.max(box.y, Math.min(box.y + box.h, y));
    var had = S.mark[id];
    S.mark[id] = { x: Math.round(x * 10) / 10, y: Math.round(y * 10) / 10, size: had ? had.size : 'm' };
    S.lines = [];
    track('quote_mark_placed', { panel: id });
    save(); render();
  });

  root.addEventListener('keydown', function (e) {
    // Enter in the postcode box should price the job, not submit whatever form is around it.
    if (e.target && e.target.id === 'kq-pc' && e.key === 'Enter') {
      e.preventDefault(); lookupPostcode(); return;
    }
    var el = e.target.closest ? e.target.closest('.kq-panel') : null;
    if (el && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); el.dispatchEvent(new MouseEvent('click', { bubbles: true })); }
  });

  /* Anything on the page with data-quote="bodywork" (etc.) opens that flow. */
  document.addEventListener('click', function (e) {
    var t = e.target.closest ? e.target.closest('[data-quote]') : null;
    if (!t) return;
    e.preventDefault();
    var f = t.dataset.quote;
    if (!C) { PENDING = { flow: f }; root.scrollIntoView({ behavior: 'smooth', block: 'start' }); return; }
    if (S.sent) { S.sent = false; S.lines = []; S.mech = []; S.body = {}; S.mark = {}; S.wheels = {}; S.expires = 0; S.offerGone = false; S.day = S.time = null; }
    if (FLOWS[f]) { S.flow = f; S.step = (S.vehicle && !S.manual) ? 'build' : 'car'; }
    else if (!S.flow) S.step = 'flow';
    save(); render();
    root.scrollIntoView({ behavior: 'smooth', block: 'start' });
    var p = $('#kq-plate'); if (p) setTimeout(function () { p.focus({ preventScroll: true }); }, 400);
  });
  var hero = document.getElementById('hero-reg');
  if (hero) hero.addEventListener('submit', function (e) {
    e.preventDefault();
    var reg = hero.querySelector('input').value.trim();
    if (!C) { PENDING = { flow: 'mechanical', reg: reg.toUpperCase() }; root.scrollIntoView({ behavior: 'smooth', block: 'start' }); return; }
    S.reg = reg.toUpperCase(); S.step = S.flow ? 'car' : 'flow';
    if (!S.flow) { S.flow = 'mechanical'; S.step = 'car'; }
    render(); root.scrollIntoView({ behavior: 'smooth', block: 'start' });
    var f = $('.kq-reg'); if (f && reg) { f.requestSubmit ? f.requestSubmit() : f.querySelector('button[type=submit]').click(); }
  });

  fetch(root.dataset.catalogue || '/quote-catalogue.json').then(function (r) { return r.json(); }).then(function (c) {
    C = c; load();
    var pf = root.dataset.flow, pj = root.dataset.job;
    if (FLOWS[pf] && !S.sent) { S.flow = pf; if (S.step === 'flow') S.step = 'car'; }
    if (pj && E.findJob(C, pj) && S.mech.indexOf(pj) === -1 && !S.sent) { S.mech.push(pj); S.lines = []; if (S.step === 'estimate') S.step = 'build'; }
    if (PENDING) {
      if (FLOWS[PENDING.flow]) { S.flow = PENDING.flow; S.step = (S.vehicle && !S.manual) ? 'build' : 'car'; }
      if (PENDING.reg) S.reg = PENDING.reg;
    }
    if (!S.flow) S.step = 'flow';
    if (S.step === 'estimate' && !S.lines.length) S.step = 'build';
    render();
    if (PENDING && PENDING.reg) { var rf = $('.kq-reg'); if (rf) { rf.requestSubmit ? rf.requestSubmit() : rf.querySelector('button[type=submit]').click(); } }
    PENDING = null;
  }).catch(function () {
    root.innerHTML = '<p class="kq-note">Instant quotes are unavailable right now. Please <a href="tel:' + PHONE_TEL + '">call ' + PHONE + '</a> or <a href="https://wa.me/' + WA + '">WhatsApp us</a>.</p>';
  });
})();
