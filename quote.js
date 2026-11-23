/* KITH instant quote.
   Four flows, each built for what that customer actually knows:
     mechanical  pick the jobs off a card          tyres  read your sidewall
     bodywork    tap the damaged panel on the car  tuning pick a stage, see the power
   Then: estimate (with the £50 book-online offer and its hold timer) -> details -> pick a slot -> booked.
   Prices always come from quote-catalogue.json. Reg lookup (/api/vehicle) and the AI book-time estimate
   (/api/estimate) are optional; with neither, everything still prices from the price book.
   Leads go out three ways: Web3Forms by email, the unified inbox (always), and the CRM's jobs
   table when the crm keys in the catalogue are filled in - which they are not yet. */
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
    recovery:   { label: 'Recovery',   sub: 'Broken down, or needs collecting', cal: 'mechanical' },
    // Not priced from the rate card: a claim is handled, not quoted. This one collects the
    // incident and gets a callback booked, which is what a non-fault claim actually needs.
    accident:   { label: 'Accident management', sub: 'Non-fault claim handled end to end', cal: 'bodywork' }
  };

  /* Flows that have no rate-card price and go straight from the intake to taking details. */
  function callbackFlow() { return S.flow === 'accident' || (S.flow === 'recovery' && S.rec.when === 'now'); }
  /* The registration comes first, then what they want done. It used to be the other way round,
     and on a service page the flow was taken from the page's data-flow attribute, so someone who
     entered a reg on the bumper page was dropped straight into the bodywork questions and never
     got asked what they actually wanted. If they had come for a service and a bumper, there was
     no way to say so. The page's own flow is now a suggestion that arrives pre-selected on the
     choice step rather than something that skips it. */
  /* Details before the price, 22 Nov 2026. The funnel used to hand the estimate over and only
     then ask who you are, so anyone who looked at the figure and left took their details with
     them - and at the volume this site runs at, that is most of them. The lead is now captured
     at the point the customer has done the work of describing the job, and the price is what
     they get back for it. The copy that promised a price in thirty seconds was changed with it;
     promising an instant price and then asking for a phone number first is bait. */
  var STEPS = ['car', 'flow', 'build', 'details', 'estimate', 'calendar', 'done'];
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
    flow: '', suggest: '', step: 'car', reg: '', vehicle: null, manual: false, model: '', band: 'medium',
    acc: { fault: '', drivable: '', replacement: '', reported: '' },  // accident management intake
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
  /* Prices are shown in whole pounds.

     The catalogue holds no pence - every figure in it is a round number - but the servicing
     prices are built by multiplying an ex-VAT rate by 1.2, and that lands on pence. The result
     was a job list where "Full service £210 - £270" sat directly above "Major service £248.30 -
     £312.11". Pence on a price read as a spreadsheet leaking onto the page rather than a price
     somebody set, and it only happened to three lines, so it looked like a fault rather than a
     convention.

     Rounded UP at both ends, not to nearest. The house rule everywhere else is that a quoted
     figure is a floor we will honour, so the displayed number must never sit under what the
     arithmetic actually produced. 48p is immaterial either way; the principle is not.

     Only range() does this. money() is left alone because it also prints per-litre oil rates,
     where the pence are the point. */
  function range(lo, hi) {
    var l = isFinite(lo) ? Math.ceil(lo) : lo, h = isFinite(hi) ? Math.ceil(hi) : hi;
    return l === h ? money(l) : money(l) + ' – ' + money(h);
  }

  /* An estimate shown as a range, which is what the small print under it has always promised.
     Once engine size, oil and parts are all answered the rate card produces one exact figure and
     the range collapsed to a single number, contradicting the copy beside it.

     The range runs UPWARDS from that figure, never downwards. The exact price is what we would
     charge for the job as quoted, so it is the floor; the ceiling covers what genuinely varies
     once the car is on the ramp - an engine that takes more oil than its band allows, a
     non-standard filter, a bolt that has seized. Padding downwards would advertise a number no
     customer ever actually pays, which is the one thing a price range must not do. */
  /* True when every priced line is a genuinely fixed price rather than a figure that could move.
     An MOT is a statutory test at a fixed fee, a code read is a fixed fee, wheel fitting is a
     fixed fee. Nothing in those jobs varies with what we find. */
  function allLinesFixed(lines) {
    var priced = (lines || []).filter(function (l) {
      return l && typeof l.low === 'number' && isFinite(l.low) && isFinite(l.high);
    });
    return priced.length > 0 && priced.every(function (l) {
      return l.kind === 'fixed' && l.high === l.low;
    });
  }

  function spread(t, lines) {
    if (!t || typeof t.low !== 'number' || typeof t.high !== 'number') return t;
    if (t.high > t.low) return t;                       // a genuine range already
    /* A fixed price is not an estimate and must not be padded into one.

       The spread exists to cover "an engine that takes more oil than its band, a non-standard
       filter, or a seized bolt", which is sound for labour. It is nonsense on a fixed fee, and on
       the MOT it was actively damaging: the line note says "MOT is outside VAT, so £50 is the
       whole price. The DVSA maximum is £54.85", and the total directly beneath it read
       "£50 - £65". Three problems at the moment a customer decides whether to trust the price -
       it contradicts the sentence above it, it quotes a top end above the legal maximum the same
       sentence cites, and it does it on the commonest reason anyone rings a garage.

       The other three fixed jobs were doing the same quietly: a £36 code read shown as £36-£55,
       £146 diagnostics as £146-£165, £80 wheel fitting as £80-£95. */
    if (allLinesFixed(lines)) return t;
    var s = C.estimate_spread;
    if (!s) return t;
    var step = s.round_to || 5;
    var pad = Math.max(s.min || 0, Math.round(t.low * (s.pct || 0)));
    // Capped. On a big job 10% runs away with itself, and a range wider than £50 stops reading
    // as an estimate and starts reading as a refusal to quote.
    if (s.max) pad = Math.min(pad, s.max);
    return { low: t.low, high: Math.ceil((t.low + pad) / step) * step };
  }
  function rangeOf(t, lines) { var r = spread(t, lines); return range(r.low, r.high); }
  function $(s) { return root.querySelector(s); }
  function $$(s) { return [].slice.call(root.querySelectorAll(s)); }
  function title(s) { s = String(s || ''); if (s.length <= 3) return s.toUpperCase(); return s.toLowerCase().replace(/\b[\w']/g, function (c) { return c.toUpperCase(); }); }
  /* The shape of the saved state, taken from the defaults above before anything touches them.
     State is restored by copying every stored key over S, with no check that the two agree. That
     is fine until the widget changes shape - which it does on most deploys - and then a visitor
     whose tab still holds yesterday's state gets a half-populated S and a widget that throws,
     which the customer reads as "Instant quotes are unavailable right now. Please call us."
     Nobody reports that; they just ring, or they don't.

     Deriving the stamp from the keys rather than a hand-bumped number means it invalidates
     itself whenever a field is added or removed, with nothing to remember. */
  var STATE_SHAPE = Object.keys(S).sort().join(',');

  function save() {
    try { sessionStorage.setItem('kq2', JSON.stringify(Object.assign({ __shape: STATE_SHAPE }, S))); } catch (e) {}
  }
  function load() {
    try {
      var s = JSON.parse(sessionStorage.getItem('kq2') || 'null');
      if (!s || s.sent) return;
      // Saved by a different version of this widget: start clean rather than merge two shapes.
      // A customer losing a half-filled quote is a small cost; a dead widget is the whole booking.
      if (s.__shape !== STATE_SHAPE) { try { sessionStorage.removeItem('kq2'); } catch (e) {} return; }
      Object.keys(s).forEach(function (k) { if (k !== '__shape') S[k] = s[k]; });
    } catch (e) {}
  }
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
  /* Keep the widget in one place.

     This used to scroll only when the widget had drifted outside a window - top above -40px or
     below 60% of the viewport - and leave it alone otherwise. The effect was that the funnel
     moved for some steps and not others, and since each step is a different height, the card
     appeared to walk down the page as you went through it. Reported as "step two is moving
     down".

     Now every step lands the top of the widget in the same place, so the funnel sits still and
     the next question is always where the last one was. Instant rather than smooth: a smooth
     scroll on each step is the movement being complained about. */
  /* Where the funnel runs.
     ----------------------------------------------------------------------------------------
     The funnel lives in its own section well down the page, so starting it from the hero used
     to mean throwing the reader down there, and then nudging the page on every step after. If
     the page offers a hero slot, the funnel is moved into it the first time it is opened and
     runs in the spot the reader is already looking at - and once it is docked there, nothing
     scrolls at all. Pages with no slot keep the old behaviour. */
  var HOST = document.getElementById('kq-hero-host');

  function docked() { return !!(HOST && HOST.contains(root)); }

  function dock() {
    if (!HOST || docked()) return;
    HOST.appendChild(root);
    HOST.hidden = false;
    var card = document.querySelector('.qcard, .kx-qcard');
    if (card) card.hidden = true;
    var note = document.getElementById('kq-moved');
    if (note) note.hidden = false;
    document.documentElement.classList.add('kq-docked');
  }

  /* Put the funnel where it can be seen. Docking counts as showing it, so there is no scroll. */
  function reveal() {
    dock();
    if (docked()) return;
    reveal();
  }

  function go(step) {
    S.step = step; save(); render();
    if (docked()) return;
    var top = root.getBoundingClientRect().top + window.pageYOffset;
    var header = document.querySelector('header');
    var offset = (header ? header.getBoundingClientRect().height : 0) + 12;
    window.scrollTo({ top: Math.max(0, top - offset), behavior: 'auto' });
  }
  function chips(items, current, act) {
    return items.map(function (i) {
      return '<button type="button" class="kq-pill' + (String(i.id) === String(current) ? ' on' : '') + '" data-act="' + act + '" data-v="' + esc(i.id) + '">' + esc(i.label) + '</button>';
    }).join('');
  }

  /* ---------- progress ---------- */
  function progress() {
    var urgent = callbackFlow();
    var shown = STEPS.filter(function (s) { return s !== 'done' && !(urgent && s === 'calendar') && !(urgent && s === 'estimate'); });
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
    var v = S.vehicle || {};
    // Name the car back to them. They have just typed the reg and this is the step that confirms
    // we found the right vehicle, so the choice is made against a car rather than in the abstract.
    var car = (!S.manual && v.make)
      ? '<div class="kq-car kq-car-sm"><div class="kq-car-plate">' + esc(v.registrationNumber || S.reg) + '</div><div><strong>' +
        esc([v.yearOfManufacture, title(v.make)].filter(Boolean).join(' ')) + '</strong><span>' +
        esc([v.engineCapacity ? v.engineCapacity + 'cc' : '', title(v.fuelType), title(v.colour)].filter(Boolean).join(' · ')) + '</span></div></div>'
      : '';
    var sel = S.flow || S.suggest;
    return '<h2 class="kq-h">What does it need?</h2>' + car +
      '<p class="kq-help">Pick one to get started. You can add more once we have priced the first.</p>' +
      '<div class="kq-picks">' + Object.keys(FLOWS).map(function (f) {
        return '<button type="button" class="kq-pick' + (sel === f ? ' on' : '') + '" data-act="flow" data-v="' + f + '"><b>' +
          esc(FLOWS[f].label) + '</b><small>' + esc(FLOWS[f].sub) + '</small></button>';
      }).join('') + '</div>' +
      '<div class="kq-nav"><button type="button" class="kq-btn kq-btn-ghost" data-act="back" data-v="car">Back</button></div>';
  }

  /* ---------- step: accident management ---------- */
  function viewAccident() {
    var a = S.acc;
    function row(label, key, opts) {
      return '<label class="kq-label">' + label + '</label><div class="kq-pills">' + opts.map(function (o) {
        return '<button type="button" class="kq-pill' + (a[key] === o[0] ? ' on' : '') +
          '" data-act="acc" data-v="' + key + ':' + o[0] + '">' + esc(o[1]) + '</button>';
      }).join('') + '</div>';
    }
    var h = '<h2 class="kq-h">Tell us what happened</h2>' +
      '<p class="kq-help">Four questions, then we ring you back. We are on no insurer&rsquo;s panel, ' +
      'which means you choose who repairs the car &mdash; not them.</p>' +
      row('Whose fault was it?', 'fault', [['theirs', 'Not my fault'], ['mine', 'My fault'], ['unsure', 'Not sure yet']]) +
      row('Is the car drivable?', 'drivable', [['yes', 'Yes'], ['no', 'No']]) +
      row('Do you need a car in the meantime?', 'replacement', [['yes', 'Yes'], ['no', 'No']]) +
      row('Told your insurer yet?', 'reported', [['yes', 'Yes'], ['no', 'Not yet'], ['noclaim', 'Not claiming']]);

    if (a.drivable === 'no') {
      h += '<p class="kq-note">If the car cannot be driven we can collect it. Pick <b>Recovery</b> ' +
        'instead if you need it moved today, or carry on here and we will sort collection on the call.</p>';
    }
    if (a.fault === 'theirs') {
      h += '<p class="kq-note">On a non-fault claim you are entitled to a like-for-like replacement ' +
        'vehicle and your excess back. Both get missed if nobody asks for them. ' +
        '<a href="/non-fault-accident-what-to-do" target="_blank" rel="noopener">What to do next</a>.</p>';
    }
    var ready = a.fault && a.drivable && a.replacement && a.reported;
    return h + nav('flow', 'to-details', ready ? 'Next: your details' : 'Answer the four above', !ready);
  }

  /* ---------- step: the car ---------- */
  function viewCar() {
    var v = S.vehicle || {}, found = !S.manual && v.make;
    /* The heading asks for the reg and says what you get back for it. "Which car is it?" asked
       the customer to do something without telling them why, on the one step the whole funnel
       depends on. Once the car is known the heading goes back to naming the step, because by
       then the price has been promised and the question is whether we got the car right. */
    var heading = found ? (S.flow === 'tyres' ? 'Which car are the tyres for?' : 'Which car is it?')
      : S.manual ? 'Tell us about the car'
      : 'Enter your reg for a price';
    var h = '<h2 class="kq-h">' + heading + '</h2>';
    if (!found && !S.manual) {
      /* The site stopped promising a price in seconds on 22 Nov, because details now come
         before the price. This label was the last place still promising it, and it sat on
         the first step of every funnel on the site. */
      return h + '<form class="kq-reg" novalidate><label class="kq-label" for="kq-plate">A couple of minutes &mdash; no obligation</label>' +
        '<div class="kq-plate"><span class="kq-gb">UK</span><input id="kq-plate" name="reg" maxlength="8" autocomplete="off" autocapitalize="characters" spellcheck="false" placeholder="AB12 CDE" value="' + esc(S.reg) + '"/></div>' +
        '<button class="kq-btn kq-btn-main" type="submit">Get my price</button>' +
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
    // The car step is now the first step, so Back has nowhere to go. It does the thing someone
    // actually wants here instead: clear the car and let them type the plate again, which is
    // what you need when the lookup returned the wrong vehicle or you mistyped it.
    return h + '<div class="kq-nav"><button type="button" class="kq-btn kq-btn-ghost" data-act="recar">' +
      (found ? 'Not my car' : 'Use a registration') + '</button>' +
      '<button type="button" class="kq-btn kq-btn-main" data-act="to-build">Next</button></div>';
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
      /* "Parts and oil" was hardcoded, so a brake job listed oil it does not use - and a customer
         reading a breakdown line by line is exactly the one who notices. None of the 33 repair
         jobs in the catalogue involve oil today, but the test is on the job rather than a flat
         rename, so one that does will still say so. */
      var oily = /\boils?\b|\bfluid\b/i.test([l.name || '', (l.includes || []).join(' ')].join(' '));
      rows.push('<li><span>' + (oily ? 'Parts and oil' : 'Parts') + '</span><em>' + range(l.parts[0], l.parts[1]) + '</em></li>');
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
    if (S.flow === 'accident') return viewAccident();
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
    return h + nav('flow', 'to-estimate', line ? 'Continue' : 'Tell us where the car is', !line);
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
    var grades = C.servicing.parts_grade.grades;
    // The uplift quoted is what OEM adds to everything ticked, not just to the service. It used
    // to be the servicing difference alone, which understated it on any basket with a repair in
    // it - and the repair parts did not actually change anyway.
    var diff = partsUplift();
    if (!diff) return '';
    var h = '<div class="kq-parts"><label class="kq-label">Which parts?</label>' +
      '<div class="kq-pills kq-choice">' + grades.map(function (g) {
        var best = g.id === 'oem';
        var extra = best && diff > 0 ? '<i>+' + money(diff) + ' on this job' + (S.mech.length > 1 ? ' card' : '') + '</i>' : '';
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
    // No service in the basket means no oil change, so the question has nothing to change.
    if (!hasService() || !svcBandKnown()) return '';
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
    return h + nav('flow', 'to-estimate', label, !S.mech.length);
  }

  /* How the work gets done, on a page of its own after the job card.
     This lived inline twice and was wrong both times: buried under the job list it was missed,
     and hoisted above it the customer met three questions before the thing they came to read.
     On its own page, after Next, each question gets asked once and the job list stays clean. */
  /* Only servicing prices move on oil, parts and engine size, so only a service earns this page.
     Someone here for brake pads goes straight from the job card to their price. */
  /* True when there is a service in the basket. The oil question only makes sense then. */
  function hasService() {
    return S.mech.some(function (id) { return SERVICE_IDS.indexOf(id) !== -1; });
  }

  /* What picking OEM actually adds across everything currently ticked - the service and the
     repairs together. Priced by running the basket twice rather than by quoting the servicing
     difference and hoping it covers the rest, which is what it used to do. */
  function partsUplift() {
    var lo = 0;
    ['aftermarket', 'oem'].forEach(function (grade, i) {
      var sum = 0;
      S.mech.forEach(function (id) {
        try {
          var l = E.priceJob(C, id, svcBandId() || S.band,
            { parts: grade, oil: S.oil || 'standard', ai: (S.ai || {})[id] });
          sum += l.low || 0;
        } catch (e) { /* an unknown job must not take the whole page down */ }
      });
      if (i === 0) lo = sum; else lo = sum - lo;
    });
    return Math.max(0, Math.round(lo));
  }

  function optionsNeeded() {
    if (S.flow !== 'mechanical' || !S.mech.length) return false;
    // Ask whenever either question has something to change: a service for the oil, or any job
    // carrying parts for the grade. A repair-only basket used to skip this page entirely, so
    // there was no way to ask for OEM brake pads.
    return hasService() || partsUplift() > 0;
  }

  function viewOptions() {
    // These two choices change the SERVICING price and nothing else: partsGrade is only read by
    // svcPrice in the engine, so a brake job's parts figure is unaffected by picking OEM here.
    // The page used to ask "Which parts?" with no scope at all, which on a basket holding a
    // service and a repair reads as though it covered both - someone choosing OEM would
    // reasonably expect OEM brake pads and not get them.
    // The parts choice now covers the whole job card rather than the service alone, so the page
    // no longer has to carve out an exception for repairs. The oil question still only appears
    // where there is a service, because nothing else on the card takes oil.
    var n = S.mech.length;
    var scope = hasService()
      ? '<p class="kq-help">' + (oilUI() ? 'Two quick choices' : 'One quick choice') +
        ', then your price.</p>'
      : '<p class="kq-help">One quick choice about the parts we fit' +
        (n > 1 ? ' on all ' + n + ' jobs' : '') + ', then your price.</p>';

    return '<h2 class="kq-h">How would you like it done?</h2>' + scope +
      '<div class="kq-basis">' + engineSizeUI() + partsUI() + oilUI() + '</div>' +
      nav('build', 'to-estimate', 'Show my price');
  }

  function jobName(id) {
    var j = E.findJob(C, id);
    return j ? j.name.toLowerCase() : 'your service';
  }
  function listNames(ids) {
    var n = ids.map(jobName);
    return n.length === 1 ? n[0] : n.slice(0, -1).join(', ') + ' and ' + n[n.length - 1];
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
    return h + nav('flow', 'to-estimate', 'Show my price');
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
    return h + nav('flow', 'to-estimate', items ? 'Show my price (' + items + ')' : 'Tap a panel or a wheel', !items);
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
    return h + nav('flow', 'to-estimate', 'Show my price');
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
        // Oil stays service-only, because nothing else on the card takes any. Parts do not:
        // the grade applies to a brake job's pads as much as to a service's filters, and
        // withholding it here was why ticking OEM changed the service price and left every
        // repair exactly where it was.
        return E.priceJob(C, id, isSvc ? svcBandId() : S.band,
                          { ai: S.ai[id], oil: isSvc ? S.oil : undefined, parts: S.parts });
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
          // jobId first: it is what the line was priced FROM. The two id comparisons are kept for
          // the non-service lines, which carry no jobId.
          return priced.filter(function (l) {
            return l.jobId === id || l.id === id || l.id === 'service-' + id;
          })[0] || null;
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
    lines = applyPromo(lines);
    S.lines = lines;
    // Bodywork carries a confirmed band around the total: the same scrape is a different job once it's
    // been looked at, so we show the span we stand behind rather than a figure that will move.
    S.totals = S.flow === 'bodywork' ? E.bodyBand(C, E.totals(lines), lines) : E.totals(lines);
  }

  /* The campaign discount, taken off the price rather than announced next to it.
     ------------------------------------------------------------------------------------------
     The funnel has been showing a "30% off all bodywork" banner over undiscounted figures: the
     customer read the banner, saw £288 for a front bumper, and nothing anywhere took the 30%
     off. A price that contradicts the offer beside it is worse than no offer.

     The campaign lives in quote-catalogue.json under "promo", so it ends by editing one date and
     comes off by deleting one block. Each discounted line keeps its original in .was, which is
     what the summary strikes through, so the saving is checkable rather than asserted. */
  function promoOn() {
    var p = C && C.promo;
    if (!p || !p.percent) return null;
    if (p.ends && new Date(p.ends).getTime() < Date.now()) return null;
    if (p.flows && p.flows.indexOf(S.flow) === -1) return null;
    // The insurer pays the rate card on a claim, so a retail discount does not belong on it.
    if (p.insurance_work === false && S.flow === 'accident') return null;
    return p;
  }

  function applyPromo(lines) {
    var p = promoOn();
    if (!p || !lines || !lines.length) return lines || [];
    var k = (100 - p.percent) / 100;
    return lines.map(function (l) {
      if (!l || typeof l.low !== 'number' || !isFinite(l.low) || !isFinite(l.high)) return l;
      var out = {};
      for (var key in l) out[key] = l[key];
      out.was = { low: l.low, high: l.high };
      out.low = Math.round(l.low * k);
      out.high = Math.round(l.high * k);
      out.promo = p.name;
      return out;
    });
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
  // The KITH pricing Brain — HaynesPro SRTs + SOP v8.0 + AI fallback. Mechanical
  // flow only (bodywork / recovery / tuning use their own catalogue bands).
  // We still compute the local estimate first so the customer sees a number
  // instantly; the Brain's result overwrites S.brainRange + swaps into the
  // headline figure when it lands (usually 3–10s). If Brain fails or the flow
  // isn't mechanical, local estimate stays as the authoritative on-page figure.
  var BRAIN_URL = 'https://mxyrxyhvjndgjqupgstu.supabase.co/functions/v1/brain';
  var BRAIN_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im14eXJ4eWh2am5kZ2pxdXBnc3R1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODIyMTMyNjgsImV4cCI6MjA5Nzc4OTI2OH0.z7F_sUqx56bIcBLxjWFJSP3rT1jhNPAL9_1SWZ7cUog';
  function brainComplaint() {
    // Build a natural-language complaint from the picked jobs + model, so the
    // Brain's identify step has what it needs.
    var bits = S.lines && S.lines.length
      ? S.lines.map(function (l) { return l.name; }).filter(Boolean)
      : [];
    return bits.join(', ') || (FLOWS[S.flow] ? FLOWS[S.flow].label : 'mechanical work');
  }
  function fetchBrain() {
    if (S.flow !== 'mechanical') { S.brainRange = null; S.brainTried = true; return Promise.resolve(); }
    if (!S.vehicle || !S.vehicle.make) { S.brainRange = null; S.brainTried = true; return Promise.resolve(); }
    var complaint = brainComplaint();
    if (!complaint) { S.brainRange = null; S.brainTried = true; return Promise.resolve(); }
    S.brainLoading = true;
    S.brainTried = true;
    S.brainStartedAt = Date.now();
    S.brainTargetSeconds = 8;
    /* A hard deadline on the Brain. Without one, a call that never answers left the countdown
       sitting on "Almost there…" and the customer playing Snake indefinitely - no price, no
       booking, and nothing on screen admitting anything had gone wrong. Tested by holding the
       request open: it stalls at one second and stays there.

       The local rate-card figure is already computed by the time this runs, so when the deadline
       passes there is a real price to fall back to. Twelve seconds: comfortably past the eight
       the countdown promises, short enough that nobody is still waiting. */
    var brainCtl = (typeof AbortController !== 'undefined') ? new AbortController() : null;
    var brainTimer = setTimeout(function () {
      if (brainCtl) brainCtl.abort();
      if (S.brainLoading) {
        S.brainLoading = false; S.brainRange = null;
        save(); render();                 // falls through to the local estimate
      }
    }, 12000);
    var vehicle = [S.vehicle.yearOfManufacture, S.vehicle.make, S.model || '', S.vehicle.fuelType || ''].filter(Boolean).join(' ');
    return fetch(BRAIN_URL, {
      method: 'POST',
      signal: brainCtl ? brainCtl.signal : undefined,
      headers: {
        'Content-Type': 'application/json',
        'apikey': BRAIN_KEY, 'Authorization': 'Bearer ' + BRAIN_KEY,
        'x-caller': 'website'
      },
      body: JSON.stringify({
        customer_type: 'retail',
        vehicle: vehicle,
        reg: (S.vehicle && S.vehicle.registrationNumber) || '',
        complaint: complaint
      })
    }).then(function (r) {
      if (!r.ok) { console.warn('[KITH Brain] HTTP ' + r.status); return null; }
      return r.json();
    }).then(function (d) {
      clearTimeout(brainTimer);
      S.brainLoading = false;
      if (d && d.error) console.warn('[KITH Brain] error:', d.error);
      if (d && d.total_range && d.total_range.hi > 0) {
        S.brainRange = { lo: Math.round(d.total_range.lo), hi: Math.round(d.total_range.hi), confidence: d.confidence || 'low', allFirm: !!d.all_firm, usedFallback: !!d.used_ai_fallback };
      } else { S.brainRange = null; }
    }).catch(function (e) {
      clearTimeout(brainTimer);
      console.warn('[KITH Brain] network:', e && e.message);
      S.brainLoading = false; S.brainRange = null;
    });
  }

  // Countdown view shown while the Brain works out the price (mechanical only).
  // Starts at 8 seconds. If the Brain takes longer, the number holds at 1 and
  // the copy switches to "almost there". If Brain finally returns, viewEstimate
  // re-renders normally; if it fails, we fall back to the local estimate.
  var BRAIN_TICK = null;
  function startBrainTicker() {
    if (BRAIN_TICK) return;
    BRAIN_TICK = setInterval(function () {
      if (!S.brainLoading) { stopBrainTicker(); render(); return; }
      var elapsed = Math.floor((Date.now() - (S.brainStartedAt || Date.now())) / 1000);
      var left = Math.max(0, (S.brainTargetSeconds || 8) - elapsed);
      var n = document.getElementById('kq-countdown-n');
      var l = document.getElementById('kq-countdown-label');
      if (n) n.textContent = left > 0 ? left : 1;
      if (l && left <= 0) l.textContent = 'Almost there…';
    }, 250);
  }
  function stopBrainTicker() { if (BRAIN_TICK) { clearInterval(BRAIN_TICK); BRAIN_TICK = null; } stopSnake(); }
  function brainCountdownView() {
    var elapsed = S.brainStartedAt ? Math.floor((Date.now() - S.brainStartedAt) / 1000) : 0;
    var left = Math.max(0, (S.brainTargetSeconds || 8) - elapsed);
    // Kick off the ticker AND the mini-game after the DOM is painted.
    setTimeout(function () { startBrainTicker(); startSnake(); }, 50);
    return '<div class="kq-brain-count" role="status">' +
             '<p class="kq-brain-count-lead">Working out your estimate for <strong>' + esc(vehicleName()) + '</strong>' +
               (S.vehicle && S.vehicle.registrationNumber ? ' <span class="kq-mini-plate">' + esc(S.vehicle.registrationNumber) + '</span>' : '') +
             '</p>' +
             '<div class="kq-game-wrap">' +
               '<div class="kq-game-head">' +
                 '<div class="kq-game-timer"><span id="kq-countdown-n">' + (left > 0 ? left : 1) + '</span><small>sec</small></div>' +
                 '<div class="kq-game-title"><strong>Pit-stop Snake</strong><span id="kq-game-score">Score 0</span></div>' +
                 '<div class="kq-game-best"><span>Best</span><strong id="kq-game-best">' + (S.snakeBest || 0) + '</strong></div>' +
               '</div>' +
               '<canvas id="kq-snake" width="320" height="320" tabindex="0" aria-label="Snake mini-game — swipe or use arrow keys"></canvas>' +
               '<div class="kq-game-help" id="kq-countdown-label">Swipe or use ← ↑ ↓ → to collect the bolts while we price your car</div>' +
             '</div>' +
           '</div>';
  }

  // ── PIT-STOP SNAKE (plays during the Brain wait) ────────────────────────
  // Tiny, no-framework canvas snake. Auto-plays if the customer doesn't
  // touch anything — a demo snake wandering so the screen doesn't feel dead.
  // Takes over on first input. Cleans up on view change.
  var SNAKE = null;
  function stopSnake() {
    if (!SNAKE) return;
    cancelAnimationFrame(SNAKE.raf);
    if (SNAKE.onkey) document.removeEventListener('keydown', SNAKE.onkey);
    SNAKE = null;
  }
  function startSnake() {
    stopSnake();
    var c = document.getElementById('kq-snake'); if (!c) return;
    var ctx = c.getContext('2d');
    var GRID = 16, CELLS = 20, W = GRID * CELLS;  // canvas 320x320
    // Resize for retina
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    c.width = W * dpr; c.height = W * dpr; c.style.width = W + 'px'; c.style.height = W + 'px';
    ctx.scale(dpr, dpr);

    var s = SNAKE = {
      snake: [{x:10,y:10},{x:9,y:10},{x:8,y:10}],
      dir: {x:1,y:0}, nextDir: {x:1,y:0},
      food: spawnFood([{x:10,y:10},{x:9,y:10},{x:8,y:10}]),
      score: 0, best: S.snakeBest || 0, auto: true, lastStep: 0,
      stepMs: 140, dead: false, raf: 0
    };
    function spawnFood(snake){ var p, tries=0; do { p = {x:(Math.random()*CELLS)|0, y:(Math.random()*CELLS)|0}; tries++; } while (snake.some(seg=>seg.x===p.x&&seg.y===p.y) && tries<200); return p; }

    function turn(dx,dy){ if (dx === -s.dir.x && dy === -s.dir.y) return; s.nextDir = {x:dx,y:dy}; s.auto = false; }
    s.onkey = function(e){
      var k = e.key;
      if (k==='ArrowUp'||k==='w'||k==='W') { turn(0,-1); e.preventDefault(); }
      else if (k==='ArrowDown'||k==='s'||k==='S') { turn(0,1); e.preventDefault(); }
      else if (k==='ArrowLeft'||k==='a'||k==='A') { turn(-1,0); e.preventDefault(); }
      else if (k==='ArrowRight'||k==='d'||k==='D') { turn(1,0); e.preventDefault(); }
    };
    document.addEventListener('keydown', s.onkey);
    c.addEventListener('click', function(){ c.focus(); });
    // Touch: swipe
    var tStart = null;
    c.addEventListener('touchstart', function(e){ var t = e.touches[0]; tStart = {x:t.clientX,y:t.clientY}; }, {passive:true});
    c.addEventListener('touchend', function(e){
      if (!tStart) return;
      var t = e.changedTouches[0], dx = t.clientX - tStart.x, dy = t.clientY - tStart.y;
      if (Math.abs(dx) > Math.abs(dy)) { if (Math.abs(dx) > 15) turn(dx>0?1:-1, 0); }
      else { if (Math.abs(dy) > 15) turn(0, dy>0?1:-1); }
      tStart = null;
    }, {passive:true});

    function step() {
      // Auto-pilot: wander toward food so the snake isn't dead on screen
      if (s.auto) {
        var head = s.snake[0], best = s.dir, bestD = Infinity;
        [[1,0],[-1,0],[0,1],[0,-1]].forEach(function(d){
          if (d[0]===-s.dir.x&&d[1]===-s.dir.y) return;
          var nx = head.x+d[0], ny = head.y+d[1];
          if (nx<0||nx>=CELLS||ny<0||ny>=CELLS) return;
          if (s.snake.some(seg=>seg.x===nx&&seg.y===ny)) return;
          var dd = Math.abs(nx - s.food.x) + Math.abs(ny - s.food.y);
          if (dd < bestD) { bestD = dd; best = {x:d[0],y:d[1]}; }
        });
        s.nextDir = best;
      }
      s.dir = s.nextDir;
      var head = s.snake[0], nx = head.x + s.dir.x, ny = head.y + s.dir.y;
      // Wrap on walls (friendlier than game over)
      if (nx<0) nx = CELLS-1; if (nx>=CELLS) nx = 0;
      if (ny<0) ny = CELLS-1; if (ny>=CELLS) ny = 0;
      // Self-hit → reset with current score as best
      if (s.snake.some(function(seg){ return seg.x===nx && seg.y===ny; })) {
        if (s.score > s.best) { s.best = s.score; S.snakeBest = s.best; try { localStorage.setItem('kq_snake_best', String(s.best)); } catch(e){} }
        s.snake = [{x:10,y:10},{x:9,y:10},{x:8,y:10}]; s.dir = {x:1,y:0}; s.nextDir = {x:1,y:0};
        s.food = spawnFood(s.snake); s.score = 0; s.auto = true; return;
      }
      s.snake.unshift({x:nx,y:ny});
      if (nx === s.food.x && ny === s.food.y) {
        s.score++;
        s.food = spawnFood(s.snake);
        s.stepMs = Math.max(70, s.stepMs - 2);
      } else {
        s.snake.pop();
      }
      // HUD
      var sc = document.getElementById('kq-game-score'); if (sc) sc.textContent = 'Score ' + s.score;
      var bs = document.getElementById('kq-game-best'); if (bs) bs.textContent = s.best;
    }

    function draw() {
      ctx.fillStyle = '#1B1E24'; ctx.fillRect(0,0,W,W);
      // Grid dots
      ctx.fillStyle = 'rgba(216,163,43,0.08)';
      for (var i=0;i<CELLS;i++) for (var j=0;j<CELLS;j++) ctx.fillRect(i*GRID+GRID/2-1, j*GRID+GRID/2-1, 2, 2);
      // Food — gold bolt
      ctx.fillStyle = '#D8A32B';
      ctx.beginPath();
      ctx.arc(s.food.x*GRID + GRID/2, s.food.y*GRID + GRID/2, GRID/2 - 3, 0, Math.PI*2);
      ctx.fill();
      // Snake — darker gold body, brighter head
      s.snake.forEach(function(seg, i) {
        ctx.fillStyle = i === 0 ? '#F0C04A' : 'rgba(216,163,43,' + (0.95 - Math.min(0.55, i*0.015)) + ')';
        var pad = i === 0 ? 1 : 2;
        var r = 3;
        var x = seg.x*GRID + pad, y = seg.y*GRID + pad, w = GRID - pad*2, h = GRID - pad*2;
        ctx.beginPath();
        ctx.moveTo(x+r, y); ctx.lineTo(x+w-r, y); ctx.quadraticCurveTo(x+w, y, x+w, y+r);
        ctx.lineTo(x+w, y+h-r); ctx.quadraticCurveTo(x+w, y+h, x+w-r, y+h);
        ctx.lineTo(x+r, y+h); ctx.quadraticCurveTo(x, y+h, x, y+h-r);
        ctx.lineTo(x, y+r); ctx.quadraticCurveTo(x, y, x+r, y); ctx.closePath(); ctx.fill();
      });
    }

    function loop(t) {
      if (!SNAKE) return;
      if (!s.lastStep) s.lastStep = t;
      if (t - s.lastStep >= s.stepMs) { step(); s.lastStep = t; }
      draw();
      s.raf = requestAnimationFrame(loop);
    }
    // Restore best from localStorage
    try { var b = parseInt(localStorage.getItem('kq_snake_best') || '0', 10); if (b > s.best) s.best = b; } catch(e){}
    S.snakeBest = s.best;
    s.raf = requestAnimationFrame(loop);
  }

  /* ---------- step: estimate ---------- */
  function viewEstimate() {
    if (!S.lines.length) return '<div class="kq-loading" role="status"><span class="kq-spin"></span>Working out your price…</div>';
    // For mechanical, the Brain is the only source of the headline figure.
    // While it's thinking, show a countdown rather than the local estimate —
    // one number the customer sees, no flash.
    if (S.flow === 'mechanical' && !S.brainRange && (S.brainLoading || !S.brainTried)) {
      return brainCountdownView();
    }
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
      /* Two pricing systems meet here, and which one speaks depends on whether the rate card
         already knows the answer.

         Where the catalogue prices a job exactly - the four services, built from Logan's own
         engine-size rate card - that figure stands. It is not an estimate to be improved on. The
         Brain was overriding it, and a full service the rate card puts at £247 was being quoted
         at £387-£537: a 45-100% overquote against the garage's own price list, on the line item
         the customer can see for themselves. Any total that disagrees with the lines above it is
         wrong however clever the thing that produced it.

         Where the catalogue cannot price firmly - repairs quoted "from", anything leaning on the
         AI tags - the Brain is the better answer, because it is reading KITH's actual job history
         rather than a generic book time. So it keeps the total there, and keeps its badge. */
      var firmLocally = t.count > 0 && !t.unpriced;
      var bRange = (!firmLocally && S.brainRange && S.brainRange.hi > 0) ? S.brainRange : null;
      var shown = bRange ? { low: bRange.lo, high: bRange.hi } : spread(t, S.lines);
      var hLabel = 'Your estimate' + (!bRange && t.unpriced ? ' so far' : '');
      var hTag = bRange ? '<small class="kq-brain-tag">Priced using KITH’s live pricing system' + (bRange.allFirm ? ' (all lines firm from our history)' : '') + '</small>' : '';
      h += '<div class="kq-total"><span>' + hLabel + '</span><b>' + range(shown.low, shown.high) + '</b>' + hTag + '</div>';
      /* Compared against the figure actually on screen, and only when the dealer beats the TOP of
         it. This was measuring the dealer against t.low/t.high - the raw local total - while the
         headline showed something else entirely, so a £781-£1,085 estimate sat above "an Audi
         main dealer, typically £830" and "around £285 less with us". Three numbers, no two of
         them agreeing, and the one a customer checks says we are the dearer option.

         The saving is quoted from our high end, so it holds however the job lands rather than
         only at its cheapest. And if the dealer does not clear our top end by the catalogue's
         margin, nothing is shown: there are jobs where a franchised dealer is genuinely
         competitive, and the honest move there is to say nothing rather than to find a number
         that flatters us. A comparison a customer can disprove costs more than it wins. */
      var saving = t.showDealer ? Math.round((t.dealer - shown.high) / 5) * 5 : 0;
      var dealerWorthShowing = t.showDealer && t.dealer > shown.high && saving >= (C.dealer.min_saving_shown || 0);
      if (dealerWorthShowing) {
        var dl2 = dealerLabel();
        h += '<div class="kq-dealer"><span>' + esc(dl2.a + ' ' + dl2.text) + ', typically</span><s>~' + money(t.dealer) + '</s><em>At least ' +
          money(saving) + ' less with us</em></div>' +
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
      '<button type="button" class="kq-btn kq-btn-main" data-act="to-slot">' + (eligible ? 'Book and save ' + money(offer.amount) : 'Book this in') + '</button></div>' +
      /* Was a thin line of grey text under the buttons. The people who reach a price and
         do not book are overwhelmingly the ones with a question the page has not answered, and
         they want a human now rather than a form. Given the weight it deserves. */
      '<a class="kq-wa-box kq-wa-urgent" href="' + waLink() + '" target="_blank" rel="noopener" '
      + 'data-act="wa"><span class="kq-wa-ico" aria-hidden="true">' + WA_ICON + '</span>'
      + '<span class="kq-wa-txt"><b>Or WhatsApp us now</b>'
      + '<em>If it&rsquo;s urgent &mdash; instant response, 24/7.</em></span></a>'
      + '<p class="kq-or">or <a href="tel:' + PHONE_TEL + '">call ' + PHONE + '</a></p>';
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
    /* This step now comes BEFORE the price, so it must not show one. summaryStrip() carries the
       figure and the struck-through was-price, which gave the estimate away on the step that
       exists to earn it. The car and the job stay - the customer should see we have understood
       what they asked for - but no numbers until the details are in.

       The copy says plainly what the exchange is. Asking for a phone number while implying the
       price is already on its way, or burying why we want it, is the kind of thing that gets a
       funnel a reputation. We ask, we say what for, and the price appears on the next screen. */
    var v = S.vehicle || {};
    // The job in words, taken from the priced lines themselves so it always matches what was
    // actually costed. No figures - that is the whole point of this step.
    var jobs = (S.lines || []).map(function (l) { return l && l.name; }).filter(Boolean);
    var jobText = jobs.length ? jobs.join(' · ') : 'Your job';
    var carLine = (!S.manual && v.make)
      ? '<div class="kq-car kq-car-sm"><div class="kq-car-plate">' + esc(v.registrationNumber || S.reg) + '</div><div><strong>' +
        esc([v.yearOfManufacture, title(v.make), S.model].filter(Boolean).join(' ')) + '</strong><span>' +
        esc(jobText) + '</span></div></div>'
      : '<p class="kq-note">' + esc(jobText) + '</p>';
    return '<h2 class="kq-h">Your price is ready</h2>' +
      '<p class="kq-help">Tell us where to send it and we&rsquo;ll show you the figure on the next screen, ' +
      'then follow it up with the full written estimate. No deposit, and nothing starts until you say so.</p>' +
      carLine +
      '<form class="kq-lead" novalidate><div class="kq-row">' +
      '<div><label class="kq-label" for="kq-name">Name</label><input class="kq-input" id="kq-name" value="' + esc(lead().name || '') + '" name="name" autocomplete="name" required maxlength="60"/></div>' +
      '<div><label class="kq-label" for="kq-phone">Mobile</label><input class="kq-input" id="kq-phone" value="' + esc(lead().phone || '') + '" name="phone" type="tel" inputmode="tel" autocomplete="tel" required maxlength="20"/></div></div>' +
      '<div class="kq-row"><div><label class="kq-label" for="kq-email">Email <span class="kq-opt">(optional)</span></label><input class="kq-input" id="kq-email" value="' + esc(lead().email || '') + '" name="email" type="email" autocomplete="email" maxlength="80"/></div>' +
      '<div><label class="kq-label" for="kq-reg2">Reg</label><input class="kq-input" id="kq-reg2" name="reg" maxlength="10" value="' + esc((S.vehicle && S.vehicle.registrationNumber) || S.reg) + '"/></div></div>' +
      '<label class="kq-check"><input type="checkbox" name="collect"' + (lead().collect ? ' checked' : '') + ' data-act="collect-toggle"/> Please collect and return my car</label>' +
      collectUI() +
      '<button class="kq-btn kq-btn-main" type="submit">' + (callbackFlow() ? 'Send this and call me back' : 'Show me my price') + '</button>' +
      '<p class="kq-err" role="alert" hidden></p>' +
      '<p class="kq-small">We only use your details to arrange this job.</p></form>' +
      // The price is no longer behind us, so Back goes to the job, which is the thing a customer
      // at this step might actually want to change.
      '<div class="kq-nav"><button type="button" class="kq-btn kq-btn-ghost" data-act="back" data-v="build">Change the job</button></div>';
  }
  /* On the booking step the service name and the car are the two things the customer is least
     unsure about - they have just chosen both - so that half of the strip was spending the best
     position on the page telling them what they already knew. The price stays; the left half
     carries the current offer instead. */
  /* What the job cost before the campaign came off, struck through beside the new figure. Built
     from the lines' own .was values rather than by dividing the total back up, so it always adds
     up to what the customer was actually quoted. */
  function wasStrike() {
    var p = promoOn();
    if (!p || !S.lines || !S.lines.length) return '';
    var lo = 0, hi = 0, any = false;
    S.lines.forEach(function (l) {
      if (l && l.was) { lo += l.was.low; hi += l.was.high; any = true; }
      else if (l && typeof l.low === 'number' && isFinite(l.low)) { lo += l.low; hi += l.high; }
    });
    if (!any) return '';
    return '<s class="kq-was">' + range(Math.round(lo), Math.round(hi)) + '</s> ';
  }

  function summaryStrip(promo) {
    var t = S.totals;
    return '<div class="kq-strip' + (promo ? ' kq-strip-promo' : '') + '">' +
      (promo ? '<div class="kq-bf"><b>30% off all bodywork</b><span>Black Friday &mdash; book it in '
             + 'before the end of the month</span></div>'
             : '<div><b>' + esc(FLOWS[S.flow].label) + '</b><span>' + esc(vehicleName()) + '</span></div>') +
      (t && t.count ? '<div class="kq-strip-p">' + (promo ? '<i>Your price</i>' : '') +
        wasStrike() + '<b>' + rangeOf(t, S.lines) + '</b>' +
        (couponOn() || (!S.offerGone && !promoOn() && E.couponEligible(C, t, t.unpriced > 0))
          ? '<span>less ' + money(coupon().amount) + ' if booked now <i id="kq-timer">' + fmtLeft() + '</i></span>'
          : '') + '</div>' : '') + '</div>';
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
    if (first && (first.free || first.slots).length) {
      var today = new Date(); today.setHours(0, 0, 0, 0);
      var when = new Date(first.key + 'T00:00:00');
      var gap = Math.round((when - today) / 86400000);
      var label = gap === 1 ? 'tomorrow' : first.long.replace(/,.*$/, '');
      next = '<p class="kq-next"><b>Next free ' + (cal === 'bodywork' ? 'drop-off' : 'slot') +
        ':</b> ' + esc(label) + ' at ' + esc((first.free || first.slots)[0]) +
        (gap > 2 ? ' &mdash; we are booked up until then' : '') + '</p>';
    }
    return '<h2 class="kq-h">Pick your ' + (cal === 'bodywork' ? 'drop-off' : 'slot') + '</h2>' +
      '<p class="kq-help">' + (cal === 'bodywork' ? 'Bodywork stays with us, so this is when you drop it off.' : 'Most mechanical jobs are done the same day.') + '</p>' +
      next +
      summaryStrip(true) +
      '<div class="kq-days">' + days.map(function (d) {
        return '<button type="button" class="kq-day' + (S.day === d.key ? ' on' : '') + '" data-act="day" data-v="' + d.key + '"><i>' + d.dow + '</i><b>' + d.dom + '</b><span>' + d.mon + '</span></button>';
      }).join('') + '</div>' +
      (day ? '<label class="kq-label">' + esc(day.long) + '</label><div class="kq-pills">' +
        day.slots.map(function (s) { var gone = (day.taken || []).indexOf(s) !== -1; return '<button type="button" class="kq-pill' + (gone ? ' kq-pill-gone' : (S.time === s ? ' on' : '')) + '" data-act="time" data-v="' + s + '"' + (gone ? ' disabled aria-label="' + s + ' - already booked"' : '') + '>' + s + (gone ? '<i>Booked</i>' : '') + '</button>'; }).join('') + '</div>' : '') +
      '<div class="kq-nav"><button type="button" class="kq-btn kq-btn-main" data-act="confirm"' +
      (S.day && S.time ? '' : ' disabled') + '>Confirm my booking</button></div>' +
      /* "I'll sort the time later" was a dead end: it took the booking without a slot and left
         the customer with nothing to do next. The people who tap it are the ones who cannot
         commit to a time from their phone, which is exactly who WhatsApp is for. */
      '<a class="kq-wa-box" href="' + waLink() + '" target="_blank" rel="noopener">' +
      '<span class="kq-wa-ico" aria-hidden="true">' + WA_ICON + '</span>' +
      '<span class="kq-wa-txt"><b>Don&rsquo;t know what time suits yet?</b>' +
      '<em>Message us on WhatsApp and we&rsquo;ll sort the slot with you.</em></span></a>' +
      // Last step before booking, and the one where people remember the panel they forgot.
      // Without this the only way back is the browser button, which drops the whole widget.
      '<div class="kq-nav kq-nav-amend"><button type="button" class="kq-btn kq-btn-link" data-act="back" data-v="' +
      (S.flow === 'recovery' ? 'flow' : 'build') + '">&larr; Add or change something on the job</button></div>';
  }

  /* ---------- step: done ---------- */
  function viewDone() {
    var booked = S.day && S.time, cal = FLOWS[S.flow].cal;
    var when = booked ? new Date(S.day).toLocaleDateString('en-GB', { weekday: 'long', day: 'numeric', month: 'long' }) + ' at ' + S.time : null;
    var urgent = callbackFlow();
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
      (couponOn() ? '<p class="kq-saved"><b>' + money(coupon().amount) + ' off your final bill</b> · code ' + esc(coupon().code) + ' · applied when we invoice, whatever the job comes to</p>' : '') +
      // They came for a repair; the MOT date is something we happen to know and they often don't.
      // Worth one line on the way out, whichever flow they used.
      motReminder() +
      (S.flow === 'bodywork' ? '<p>Send us photos of the damage and we can have the parts ready:</p>' : '') +
      (booked ? '<p class="kq-small">We&rsquo;ve sent this to you on WhatsApp so you have it in writing.</p>' + '<div class="kq-nav-wrap"><a class="kq-btn kq-btn-ghost" href="' + icsHref() + '" download="kith-cars-booking.ics">Add to my calendar</a></div>' : '') +
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

  /* Inline so the box renders with no network round trip - it sits on the booking step and a
     late-loading icon there reads as a broken button. */
  var WA_ICON = '<svg viewBox="0 0 24 24" width="26" height="26" fill="currentColor" ' +
    'aria-hidden="true"><path d="M17.47 14.38c-.3-.15-1.75-.86-2.02-.96-.27-.1-.47-.15-.67.15' +
    '-.2.3-.77.96-.94 1.16-.17.2-.35.22-.64.07-.3-.15-1.25-.46-2.38-1.47-.88-.78-1.47-1.75' +
    '-1.65-2.05-.17-.3-.02-.46.13-.6.13-.13.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.02' +
    '-.52-.08-.15-.67-1.6-.92-2.2-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.8.37-.27.3-1.04' +
    '1.02-1.04 2.48s1.07 2.88 1.22 3.08c.15.2 2.1 3.2 5.08 4.49.71.3 1.26.49 1.69.63.71.22' +
    '1.36.19 1.87.12.57-.09 1.75-.72 2-1.41.25-.69.25-1.28.17-1.41-.07-.13-.27-.2-.57-.35z"/>' +
    '<path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.46 1.32 4.96L2 22l5.25-1.38a9.9 ' +
    '9.9 0 0 0 4.79 1.22h.01c5.46 0 9.91-4.45 9.91-9.91C21.96 6.45 17.5 2 12.04 2zm0 18.15h-.01' +
    'a8.2 8.2 0 0 1-4.19-1.15l-.3-.18-3.12.82.83-3.04-.2-.31a8.22 8.22 0 0 1-1.26-4.38c0-4.54 ' +
    '3.7-8.23 8.25-8.23 2.2 0 4.27.86 5.83 2.42a8.19 8.19 0 0 1 2.41 5.82c0 4.54-3.7 8.23-8.24 ' +
    '8.23z"/></svg>';

  function waLink() {
    var msg = 'Hi KITH, I got an online estimate for ' + vehicleName() + (S.vehicle && S.vehicle.registrationNumber ? ' (' + S.vehicle.registrationNumber + ')' : '') + ':\n' +
      S.lines.map(function (l) { return '• ' + l.name + (typeof l.low === 'number' ? ': ' + range(l.low, l.high) : ''); }).join('\n') +
      (S.day && S.time ? '\nSlot: ' + S.day + ' ' + S.time : '');
    return 'https://wa.me/' + WA + '?text=' + encodeURIComponent(msg);
  }

  /* ---------- lead out: email + unified inbox always, CRM board when configured ---------- */
  function leadPayload() {
    var v = S.vehicle || {}, t = S.totals;
    return {
      priority: (S.flow === 'recovery' && S.rec.when === 'now') ? 'urgent' : (S.flow === 'accident' ? 'hot' : (S.day && S.time ? 'hot' : 'warm')),
      source: 'Website instant quote',
      stage: 'intake',
      name: lead().name, phone: lead().phone, email: lead().email || '',
      reg: lead().reg || v.registrationNumber || '',
      vehicle: { make: v.make || '', model: S.model || '', year: v.yearOfManufacture || '', engine_cc: v.engineCapacity || '', fuel: v.fuelType || '', size: C.bands[S.band].label, motExpiry: v.motExpiryDate || '' },
      service: FLOWS[S.flow].label,
      jobs: S.lines.map(function (l) { return { name: l.name, low: l.low, high: l.high, source: l.source || l.kind, hours: l.hours || null, parts: l.parts || null }; }),
      webEstimate: t && t.count ? { lo: t.low, hi: t.high } : null,
      requestedSlot: S.day && S.time ? { calendar: FLOWS[S.flow].cal, date: S.day, time: S.time } : null,
      accident: S.flow === 'accident' ? { fault: S.acc.fault, drivable: S.acc.drivable, replacement: S.acc.replacement, reportedToInsurer: S.acc.reported } : null,
      collection: !!lead().collect,
      wantMot: !!S.wantMot,
      coupon: (S.day && S.time && !S.offerGone) ? { code: coupon().code, amount: coupon().amount, minSpend: coupon().min_spend } : null,
      priceBookVersion: C.version,
      log: [{ at: new Date().toISOString(), by: 'Website', text: (S.flow === 'accident' ? ('ACCIDENT: ' + (S.acc.fault === 'theirs' ? 'non-fault' : S.acc.fault === 'mine' ? 'at fault' : 'liability unclear') + ', car ' + (S.acc.drivable === 'no' ? 'NOT drivable' : 'drivable') + ', ' + (S.acc.replacement === 'yes' ? 'needs a car' : 'no car needed') + ' - call back') : (S.flow === 'recovery' && S.rec.when === 'now') ? 'URGENT: needs recovery now, call straight back' : S.day && S.time ? 'HOT: accepted the range and booked ' + S.day + ' ' + S.time : 'Estimate sent, no slot picked') }]
    };
  }
  /* The offer has a minimum spend. The estimate screen checked it; the done screen did not,
     and neither did the confirmation, so a £50 MOT was being promised £50 off - in writing, to
     the customer, on a job with a £150 minimum. That is either money given away or an argument
     at the counter, and the counter always loses it. */
  function couponOn() {
    // The campaign discount replaces the online-booking £50 rather than stacking on top of it,
    // unless the catalogue says otherwise. Offering both would take 30% and then another £50 off
    // the same job, which is not what the campaign was priced at.
    var p = promoOn();
    if (p && !p.stacks_with_coupon) return false;
    return !!(S.day && S.time) && !S.offerGone && S.totals &&
      E.couponEligible(C, S.totals, S.totals.unpriced > 0);
  }

  /* The booking confirmation, written once and used for the WhatsApp message, the calendar
     file and nothing else. Whatever the customer is told on screen, this is what they keep. */
  function confirmationText() {
    if (!(S.day && S.time)) return '';
    var when = new Date(S.day).toLocaleDateString('en-GB',
      { weekday: 'long', day: 'numeric', month: 'long' });
    var t = S.totals;
    return 'Your booking with KITH Cars is confirmed.\n\n'
      + when + ' at ' + S.time + '\n'
      + (FLOWS[S.flow].cal === 'bodywork' ? 'Drop off at: ' : 'Bring it to: ')
      + 'Unit 1, Soho Mills, London Road, Hackbridge SM6 7HN\n'
      + 'Vehicle: ' + vehicleName()
      + (S.vehicle && S.vehicle.registrationNumber ? ' (' + S.vehicle.registrationNumber + ')' : '')
      + '\nWork: ' + S.lines.map(function (l) { return l.name; }).join(', ')
      + (t && t.count ? '\nEstimate: ' + rangeOf(t, S.lines) : '')
      + (couponOn() ? '\nDiscount: ' + money(coupon().amount)
          + ' off your final bill, code ' + coupon().code : '')
      + '\n\nWe will call to confirm and send the written price before any work starts. '
      + 'Reply here if you need to change the time.\n'
      + 'KITH Cars ' + PHONE;
  }

  /* A calendar file so the booking survives the tab being closed. Built in the browser from
     state we already hold - no server, nothing to configure, works offline. */
  function icsHref() {
    if (!(S.day && S.time)) return '';
    var p = S.time.split(':');
    var start = S.day.replace(/-/g, '') + 'T' + p[0] + p[1] + '00';
    var endH = String(Math.min(23, Number(p[0]) + 1)).padStart(2, '0');
    var end = S.day.replace(/-/g, '') + 'T' + endH + p[1] + '00';
    var fold = function (t) { return String(t).replace(/\\/g, '\\\\').replace(/\n/g, '\\n').replace(/,/g, '\\,').replace(/;/g, '\\;'); };
    var ics = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//KITH Cars//Booking//EN',
      'BEGIN:VEVENT', 'UID:' + (S.lead.id || 'kith-' + Date.now()) + '@kithcars.com',
      'DTSTAMP:' + new Date().toISOString().replace(/[-:]/g, '').replace(/\.\d+/, ''),
      'DTSTART;TZID=Europe/London:' + start, 'DTEND;TZID=Europe/London:' + end,
      'SUMMARY:' + fold('KITH Cars - ' + FLOWS[S.flow].label),
      'LOCATION:' + fold('Unit 1, Soho Mills, London Road, Hackbridge, SM6 7HN'),
      'DESCRIPTION:' + fold(confirmationText()),
      'END:VEVENT', 'END:VCALENDAR'].join('\r\n');
    return 'data:text/calendar;charset=utf-8,' + encodeURIComponent(ics);
  }

  /* Did the lead actually reach anybody?

     This replaces "if (!res.emailed && res.crm !== 'sent')", which could never fire. res.emailed
     was the STRING 'disabled' while the email send was switched off, and a non-empty string is
     truthy, so !res.emailed was permanently false and the whole check was dead. res.inbox - at
     that point the only channel still live - was not looked at. Email is back as of 21 Nov, so
     there are two live routes again, but the check stays written this way on purpose: it asks
     whether anything actually succeeded, rather than whether a particular channel is switched on.

     The result: every booking walked through to "You're booked in" whether or not a single thing
     had been delivered, and nobody found out. The customer thinks they have a slot, the workshop
     never hears, and the first anyone knows is a car arriving that nobody expected, or more
     likely a customer who never arrives at all.

     Only 'sent' counts. 'disabled', 'not connected' and 'failed 500' are all failures to
     deliver, whatever they say about why. */
  function leadDelivered(res) {
    if (!res) return false;
    return res.emailed === 'sent' || res.crm === 'sent' || res.inbox === 'sent';
  }

  function sendLead() {
    var d = leadPayload(), id = S.lead.id || (S.lead.id = 'web-' + Date.now().toString(36));
    /* Email restored 21 Nov 2026. It was dropped on the 11th on the basis that the triage AI's
       WhatsApp ping plus the CRM board entry had replaced it. In practice neither half was
       carrying it: the CRM push is still unconfigured (empty keys below, so that fetch never
       runs), which left the inbox POST as the single route out of this funnel, and Logan has
       had nothing by email in the ten days since. One route with no fallback is how leads go
       missing quietly, so the email goes back as a second, independent path.

       NOTE: this resolves to the STRING 'sent', not true. leadDelivered() compares against
       'sent', so returning a boolean here would make every successful email read as a failure
       and show the customer "that didn't send" after their details had gone through. */
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
    // The campaign discount did not exist when this block was written. Without it the email
    // shows the discounted figure with no sign that 30% has already come off, and whoever
    // writes the firm quote has no way of knowing the customer was promised that.
    var ep = promoOn();
    fd.append('Promotion', ep ? ep.name + ' · ' + ep.percent + '% already deducted from the figures above' : 'none');
    fd.append('Discount', d.coupon ? d.coupon.code + ' · £' + d.coupon.amount : 'none');
    fd.append('Price book', d.priceBookVersion);
    var email = fetch('https://api.web3forms.com/submit', { method: 'POST', body: fd })
      .then(function (r) { return r.json(); })
      .then(function (j) { return (j && j.success) ? 'sent' : 'failed'; })
      .catch(function () { return 'failed'; });
    var crm = Promise.resolve('not connected');
    if (C.crm && C.crm.supabase_url && C.crm.anon_key) {
      crm = fetch(C.crm.supabase_url.replace(/\/$/, '') + '/rest/v1/' + (C.crm.table || 'jobs') + '?on_conflict=id', {
        method: 'POST',
        headers: { apikey: C.crm.anon_key, Authorization: 'Bearer ' + C.crm.anon_key, 'Content-Type': 'application/json', Prefer: 'resolution=merge-duplicates,return=minimal' },
        body: JSON.stringify({ id: id, data: d, updated_at: new Date().toISOString() })
      }).then(function (r) { return r.ok ? 'sent' : 'failed ' + r.status; }).catch(function () { return 'failed'; });
    }
    // ── Parallel POST to KITH's unified inbox (triage AI picks it up and
    // fires the rapid-fire SRT-informed range on WhatsApp within seconds).
    // The page-side range above is still shown instantly from the client
    // catalogue; the Brain's range lands on the customer's WhatsApp.
    var jobsBrief = d.jobs.map(function (j) { return '• ' + j.name + (typeof j.low === 'number' ? ': ' + range(j.low, j.high) : ''); }).join('\n');
    var combinedText = d.service + '\n' + jobsBrief +
      (d.webEstimate ? '\nWebsite estimate: ' + range(d.webEstimate.lo, d.webEstimate.hi) : '') +
      (d.requestedSlot ? '\nWants: ' + d.requestedSlot.date + ' ' + d.requestedSlot.time + ' (' + d.requestedSlot.calendar + ')' : '');
    var inbox = fetch('https://mxyrxyhvjndgjqupgstu.supabase.co/functions/v1/inbox-ingest', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im14eXJ4eWh2am5kZ2pxdXBnc3R1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODIyMTMyNjgsImV4cCI6MjA5Nzc4OTI2OH0.z7F_sUqx56bIcBLxjWFJSP3rT1jhNPAL9_1SWZ7cUog',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im14eXJ4eWh2am5kZ2pxdXBnc3R1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODIyMTMyNjgsImV4cCI6MjA5Nzc4OTI2OH0.z7F_sUqx56bIcBLxjWFJSP3rT1jhNPAL9_1SWZ7cUog',
        'x-caller': 'kithcars_website_form'
      },
      body: JSON.stringify({
        channel: 'website',
        sender_name: d.name,
        sender_phone: d.phone,
        sender_email: d.email || '',
        reg: d.reg || '',
        year: d.vehicle.year || null,
        make: d.vehicle.make || '',
        model: d.vehicle.model || '',
        message_text: combinedText + (d.requestedSlot ? '\n\n' + confirmationText() : ''),
        /* When a slot has actually been taken the customer needs a CONFIRMATION, not a quote.
           They have seen the date, the time and the address on screen and then closed the tab,
           and until this they were left with no record of any of it. The exact wording to send
           is written out here rather than described, so the triage step has nothing to compose
           and nothing to get wrong. */
        intent: d.requestedSlot ? 'booking_confirmation' : 'estimate_follow_up',
        confirmation_text: d.requestedSlot ? confirmationText() : '',
        context_hints: d.requestedSlot
          ? 'BOOKING TAKEN. Send the confirmation_text to the customer on WhatsApp now, as a '
            + 'confirmation of the slot they just booked. Do not open with a price range - they '
            + 'have already accepted the estimate of '
            + (d.webEstimate ? range(d.webEstimate.lo, d.webEstimate.hi) : '(none)')
            + ' and the written price follows separately.'
          : 'Customer has already seen a website estimate of '
            + (d.webEstimate ? range(d.webEstimate.lo, d.webEstimate.hi) : '(not yet calculated)')
            + '. Rapid-fire a brain-based range on WhatsApp to confirm.'
      })
    }).then(function (r) { return r.ok ? 'sent' : 'failed ' + r.status; }).catch(function () { return 'failed'; });

    return Promise.all([email, crm, inbox]).then(function (r) { return { emailed: r[0], crm: r[1], inbox: r[2] }; });
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
  /* The registration of the car we are actually holding - not S.reg, which the homepage hero box
     sets for itself before handing over, so a guard on S.reg compares a plate with itself. */
  function heldReg() {
    return ((S.vehicle && S.vehicle.registrationNumber) || '').toUpperCase().replace(/[^A-Z0-9]/g, '');
  }

  /* A different plate is a different car, so everything inferred from the last one goes.
     Without this the previous vehicle survived a second lookup, and the line that reads
     "if (model && !S.model)" actively preferred the old car's model to the new car's - which is
     why a quote could come back showing the reg typed before this one.

     The job selections stay: what someone wants doing does not change because they corrected a
     typo in their plate, only the car it is priced against. */
  function resetCar() {
    S.vehicle = null; S.model = ''; S.manual = false;
    S.cc = null; S.ccBand = null; S.ccOpen = false;
    S.band = null; S.bandAuto = true; S.bandOpen = false;
    S.ai = {}; S.brainRange = null; S.brainTried = false;
    S.lines = []; S.totals = null;
  }

  /* Everything the customer chose for the PREVIOUS car.

     resetCar above throws away the vehicle and the pricing but deliberately kept the job
     selections, on the reasoning that correcting a typo in a plate should not lose your choices.
     That reasoning was wrong in practice, because the registration is the FIRST step: at the
     moment someone types a plate they have not chosen anything yet unless they went forward and
     came back, and if they went forward, came back and changed the plate, it is a different car
     and a different job.

     What it produced was the reported fault - put in a reg, pick MOT, come back, put in another
     reg, and the new car is still on MOT. Same for a dent marked on the diagram, a tyre size, a
     remap, an accident intake. All of it belonged to a car that is no longer being quoted.

     Contact details are kept. The person is usually the same person even when the car is not,
     and making them retype a name and number is a separate annoyance with no safety argument. */
  function resetJob() {
    S.flow = ''; S.suggest = ''; S.wantMot = false;
    S.mech = []; S.body = {}; S.mark = {}; S.wheels = {};
    S.tyre = { w: 205, p: 55, r: 16, qty: 4, tier: 'mid', rf: false };
    S.tune = { fuel: 'tp', bhp: '', stage: 's1', addons: [] };
    S.rec = { what: '', where: '', when: 'book' };
    S.acc = { fault: '', drivable: '', replacement: '', reported: '' };
    S.addons = []; S.collectBand = ''; S.oil = null; S.parts = null;
    S.power = null; S.expires = 0; S.offerGone = false;
    S.day = null; S.time = null; S.sent = false;
  }

  function bindCar() {
    var f = $('.kq-reg');
    if (f) f.addEventListener('submit', function (e) {
      e.preventDefault();
      var reg = f.reg.value.toUpperCase().replace(/[^A-Z0-9]/g, ''), err = $('.kq-err');
      if (!/^[A-Z0-9]{2,8}$/.test(reg)) { err.textContent = 'Please check the registration.'; err.hidden = false; return; }
      /* A different registration is a different car, so everything inferred from the last one is
         thrown away before we look this one up. Without this the previous vehicle survived: a
         failed or ambiguous lookup left it standing whole, and on a successful one the line
         below - "if (model && !S.model)" - actively preferred the old car's model to the new
         car's. That is the quote showing the reg you typed before this one.

         The job selections stay. What someone wants doing does not change because they corrected
         a typo in their plate; only the car it is priced against does. */
      /* Compared against the car we are actually holding, not S.reg. The hero box on the homepage
         sets S.reg itself before handing over to this form, so a guard on S.reg compares the new
         plate with itself and never fires - which is the path most people take. */
      if (heldReg() && heldReg() !== reg) { resetCar(); resetJob(); }
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
          track('vehicle_found');
          /* The lookup answered, so the confirmation screen has nothing to ask. It showed the
             customer their own car and a Next button, which is a step that costs a tap and
             returns nothing. Go straight on: the car stays visible as a strip on every step
             after this, with "Not my car" on it, so a wrong lookup is still one tap to fix.
             And where the page already declares its service - a bodywork landing page, a
             servicing page - the service picker is skipped too. Asking someone who clicked a
             bodywork ad what they came for is asking a question we were told the answer to. */
          save();
          go(S.flow ? 'build' : 'flow');
          return;
        }
        // Saved even though nothing was found: the previous car has just been cleared, and
        // without writing that away a reload would bring it back under the new registration.
        else if (r._status === 404) { save(); b.disabled = false; b.textContent = 'Find my car'; err.innerHTML = 'We couldn’t find that reg. Check it, or <button type="button" class="kq-link" data-act="manual">enter the car yourself</button>.'; err.hidden = false; }
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
        if (!leadDelivered(res)) { b.disabled = false; b.textContent = callbackFlow() ? 'Send this and call me back' : 'Show me my price'; err.innerHTML = 'That didn’t send. Please <a href="tel:' + PHONE_TEL + '">call ' + PHONE + '</a> or <a href="' + waLink() + '" target="_blank" rel="noopener">WhatsApp us</a>.'; err.hidden = false; return; }
        if (callbackFlow()) { S.sent = true; track('quote_urgent'); try { sessionStorage.removeItem('kq2'); } catch (x) {} go('done'); return; }
        go('estimate');
      });
    });
  }

  root.addEventListener('click', function (e) {
    var el = e.target.closest ? e.target.closest('[data-act]') : null;
    if (!el || !root.contains(el)) return;
    var a = el.dataset.act, v = el.dataset.v;
    if (a === 'flow') {
      /* Switching service starts that service's funnel clean.
         ------------------------------------------------------------------------------------
         It used to only swap S.flow and leave every answer in place, so somebody who picked
         bodywork, tapped two panels, then went back and chose Servicing arrived at the service
         job card still carrying the panels - and they came through on the quote. The car is
         kept, because it is the same car; only the job goes. */
      if (S.flow && S.flow !== v) {
        var car = S.vehicle, manual = S.manual, model = S.model, band = S.band, reg = S.reg;
        resetJob();
        S.vehicle = car; S.manual = manual; S.model = model; S.band = band; S.reg = reg;
        S.lines = [];
      }
      S.flow = v; track('quote_flow', { flow: v }); go('build');
    }
    else if (a === 'manual') { S.manual = true; S.vehicle = S.vehicle || {}; render(); }
    else if (a === 'back') { if (S.step === 'build') readBuild(); if (S.step === 'car') readCar(); go(v); }
    // Clear the held vehicle and go back to the plate. Also clears the flow, because a
    // different car may well want a different job.
    else if (a === 'recar') { resetCar(); resetJob(); S.reg = ''; save(); go('car'); }
    else if (a === 'acc') { var kv = v.split(':'); S.acc[kv[0]] = kv[1]; save(); render(); }
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
    else if (a === 'to-build') { readCar(); go(S.flow ? 'build' : 'flow'); }
    else if (a === 'to-estimate') {
      readBuild();
      // One page between the job card and the price, and only where it has something to ask:
      // engine size, oil and parts all move the servicing figure, so they are settled before a
      // price is shown rather than underneath it.
      if (S.step === 'build' && optionsNeeded()) { go('options'); return; }
      /* Compute from the local catalogue FIRST so S.lines is populated and the estimate renders
         straight away, then fire the Brain and fetchAi in parallel - neither blocks the view.
         This shape is the right one: it is why a price always appears even when a remote call is
         slow or dead, which is the failure that used to leave a customer on "Working out your
         price..." indefinitely. Both calls re-render when they land. */
      S.brainRange = null; S.brainTried = false;
      compute();
      if (!S.expires) S.expires = Date.now() + (coupon().hold_minutes || 15) * 60000;
      track('quote_price', { value: S.totals ? S.totals.low : 0, currency: 'GBP', flow: S.flow });
      go('details');
      fetchBrain().then(function () { save(); render(); }).catch(function () {});
      fetchAi().then(function () { compute(); save(); render(); }).catch(function () {});
    }
    // Carries the value: this is the start of checkout, and a conversion event without a figure
    // on it is one Meta cannot optimise against.
    else if (a === 'to-details') {
      track('quote_book_click', { value: S.totals ? S.totals.low : 0, currency: 'GBP', flow: S.flow });
      go('details');
    }
    // From the estimate. The details are already in, so this goes straight to the calendar.
    else if (a === 'to-slot') {
      track('quote_book_click', { value: S.totals ? S.totals.low : 0, currency: 'GBP', flow: S.flow });
      go('calendar');
    }
    else if (a === 'day') { S.day = v; S.time = null; save(); render(); }
    else if (a === 'time') { S.time = v; save(); render(); }
    else if (a === 'skip-slot') { S.day = null; S.time = null; S.sent = true; save(); go('done'); }
    else if (a === 'confirm') {
      el.disabled = true; el.textContent = 'Booking…';
      /* The booking confirm checked nothing at all: it declared success and moved on. If
         delivery fails here the customer must not be shown "You're booked in" for a booking the
         workshop has never heard of - they get told to WhatsApp instead, and the state is kept
         so nothing they entered is lost. */
      sendLead().then(function (res) {
        if (!leadDelivered(res)) {
          var cb = root.querySelector('[data-act="confirm"]');
          if (cb) { cb.disabled = false; cb.textContent = 'Confirm my booking'; }
          var ce = root.querySelector('.kq-err');
          if (!ce) {
            ce = document.createElement('p');
            ce.className = 'kq-err';
            var nav = root.querySelector('.kq-nav');
            if (nav && nav.parentNode) nav.parentNode.insertBefore(ce, nav);
          }
          ce.innerHTML = 'That did not reach us &mdash; your slot is <b>not</b> booked yet. ' +
            'Please <a href="' + waLink() + '" target="_blank" rel="noopener">message us on ' +
            'WhatsApp</a> or <a href="tel:' + PHONE_TEL + '">call ' + PHONE + '</a> and we will ' +
            'put it in for you.';
          ce.hidden = false;
          track('quote_booking_failed');
          return;
        }
        S.sent = true;
        track('quote_booked', { value: S.totals ? S.totals.low : 0, currency: 'GBP' });
        try { sessionStorage.removeItem('kq2'); } catch (x) {}
        go('done');
      });
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
    if (!C) { PENDING = { flow: f }; reveal(); return; }
    if (S.sent) { S.sent = false; S.lines = []; S.mech = []; S.body = {}; S.mark = {}; S.wheels = {}; S.expires = 0; S.offerGone = false; S.day = S.time = null; }
    if (FLOWS[f]) { S.suggest = f; S.flow = f; S.step = (S.vehicle || S.manual) ? 'build' : 'car'; }
    else S.step = (S.vehicle || S.manual) ? 'flow' : 'car';
    save(); render();
    reveal();
    var p = $('#kq-plate'); if (p) setTimeout(function () { p.focus({ preventScroll: true }); }, 400);
  });
  var hero = document.getElementById('hero-reg');
  if (hero) hero.addEventListener('submit', function (e) {
    e.preventDefault();
    var reg = hero.querySelector('input').value.trim();
    if (!C) { PENDING = { reg: reg.toUpperCase() }; reveal(); return; }
    /* A new plate here has to clear the old car before we render, or the car step shows the
       confirmation for the car we already hold instead of the registration form - and with no
       form on the page there is nothing to submit, so the plate just typed is never looked up.
       That is the bug where a second registration appears to do nothing at all. */
    var typed = reg.toUpperCase().replace(/[^A-Z0-9]/g, '');
    // A different plate here is a different enquiry, so the previous car's job selections go with
    // the car. Otherwise someone who priced an MOT, left the page and came back with another
    // registration gets the new car already sitting on the old car's job.
    if (heldReg() && heldReg() !== typed) { resetCar(); resetJob(); }
    // Always the car step: the plate has just been typed and needs looking up. What they want
    // doing is asked immediately afterwards, on the choice step, rather than assumed here.
    S.reg = reg.toUpperCase(); S.step = 'car';
    render(); reveal();
    var f = $('.kq-reg'); if (f && reg) { f.requestSubmit ? f.requestSubmit() : f.querySelector('button[type=submit]').click(); }
  });

  fetch(root.dataset.catalogue || '/quote-catalogue.json').then(function (r) { return r.json(); }).then(function (c) {
    C = c; load();
    var pf = root.dataset.flow, pj = root.dataset.job;
    /* A page that declares a flow starts that flow.
       --------------------------------------------------------------------------------------
       This used to only pre-select the flow on the generic "What does it need?" chooser, so
       somebody who had just read the accident-repairs page, understood what we do, and typed
       their registration was then asked what they wanted - having already said so by being on
       that page. Each service asks different questions (the accident flow asks fault, drivable,
       replacement vehicle and whether it is reported; bodywork asks which panels; servicing
       asks which jobs), and none of them were being reached without that extra tap.

       It sets the flow only when none is already held, so somebody returning mid-quote stays
       on the job they were building. The build step's Back button still goes to the chooser,
       so anyone who wants something else can switch. */
    if (FLOWS[pf] && !S.sent) { S.suggest = pf; if (!S.flow) S.flow = pf; }
    if (pj && E.findJob(C, pj) && S.mech.indexOf(pj) === -1 && !S.sent) { S.mech.push(pj); S.lines = []; if (S.step === 'estimate') S.step = 'build'; }
    if (PENDING) {
      if (FLOWS[PENDING.flow]) { S.suggest = PENDING.flow; S.flow = PENDING.flow; }
      if (PENDING.reg) S.reg = PENDING.reg;
    }
    // Reg first, then the choice. Anything already answered is kept, so someone returning
    // mid-quote lands where they left off rather than back at the plate.
    if (!S.sent) {
      if (!S.vehicle && !S.manual) S.step = 'car';
      else if (!S.flow) S.step = 'flow';
    }
    if (S.step === 'estimate' && !S.lines.length) S.step = 'build';
    render();
    if (PENDING && PENDING.reg) { var rf = $('.kq-reg'); if (rf) { rf.requestSubmit ? rf.requestSubmit() : rf.querySelector('button[type=submit]').click(); } }
    PENDING = null;
  }).catch(function () {
    root.innerHTML = '<p class="kq-note">Instant quotes are unavailable right now. Please <a href="tel:' + PHONE_TEL + '">call ' + PHONE + '</a> or <a href="https://wa.me/' + WA + '">WhatsApp us</a>.</p>';
  });
})();
