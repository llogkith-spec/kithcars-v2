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
    tuning:     { label: 'Tuning',     sub: 'Remaps, lowering, wheels',        cal: 'mechanical' }
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

  var S = {
    flow: '', step: 'flow', reg: '', vehicle: null, manual: false, model: '', band: 'medium',
    mech: [], tyre: { w: 205, p: 55, r: 16, qty: 4, tier: 'mid', rf: false },
    body: {}, tune: { fuel: 'tp', bhp: '', stage: 's1', addons: [] },
    ai: {}, lines: [], totals: null, power: null, expires: 0, offerGone: false,
    lead: null, day: null, time: null, sent: false
  };

  /* ---------- helpers ---------- */
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function money(n) { return '£' + Number(n).toLocaleString('en-GB', { minimumFractionDigits: n % 1 ? 2 : 0, maximumFractionDigits: 2 }); }
  function range(lo, hi) { return lo === hi ? money(lo) : money(lo) + ' – ' + money(hi); }
  function $(s) { return root.querySelector(s); }
  function $$(s) { return [].slice.call(root.querySelectorAll(s)); }
  function title(s) { s = String(s || ''); if (s.length <= 3) return s.toUpperCase(); return s.toLowerCase().replace(/\b[\w']/g, function (c) { return c.toUpperCase(); }); }
  function save() { try { sessionStorage.setItem('kq2', JSON.stringify(S)); } catch (e) {} }
  function load() { try { var s = JSON.parse(sessionStorage.getItem('kq2') || 'null'); if (s && !s.sent) { Object.keys(s).forEach(function (k) { S[k] = s[k]; }); } } catch (e) {} }
  function track(n, p) { try { if (window.gtag) window.gtag('event', n, p || {}); else (window.dataLayer = window.dataLayer || []).push(Object.assign({ event: n }, p || {})); } catch (e) {} }
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
    var shown = STEPS.filter(function (s) { return s !== 'flow' && s !== 'done'; });
    var i = shown.indexOf(S.step);
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
      var ulez = E.ulezLikely(v), mot = v.motExpiryDate ? new Date(v.motExpiryDate) : null;
      var days = mot ? Math.round((mot - new Date()) / 864e5) : null;
      h += '<div class="kq-car"><div class="kq-car-plate">' + esc(v.registrationNumber || S.reg) + '</div><div><strong>' +
        esc([v.yearOfManufacture, title(v.make)].filter(Boolean).join(' ')) + '</strong><span>' +
        esc([v.engineCapacity ? v.engineCapacity + 'cc' : '', title(v.fuelType), title(v.colour)].filter(Boolean).join(' · ')) + '</span></div></div>' +
        '<ul class="kq-facts">' +
        (mot ? '<li class="' + (days < 45 ? 'warn' : '') + '">MOT ' + (days < 0 ? 'expired ' : 'due ') + mot.toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' }) + '</li>' : '') +
        (mot && days < 45 && S.flow === 'mechanical' && S.mech.indexOf('mot') === -1 ? '<li class="kq-add"><button type="button" class="kq-link" data-act="add-mot">+ Add the MOT</button></li>' : '') +
        (ulez === true ? '<li>Likely ULEZ compliant</li>' : ulez === false ? '<li class="warn">Likely not ULEZ compliant · <a href="https://tfl.gov.uk/modes/driving/check-your-vehicle/" target="_blank" rel="noopener">check with TfL</a></li>' : '') +
        '</ul><label class="kq-label" for="kq-model">Model <span class="kq-opt">(optional, sharpens the price)</span></label>' +
        '<input class="kq-input" id="kq-model" maxlength="40" placeholder="e.g. 320d, Focus 1.0 EcoBoost" value="' + esc(S.model) + '"/>';
    } else {
      h += '<p class="kq-note">' + (S.reg ? 'The lookup is busy, so tell us about the car instead.' : 'Tell us about the car.') + '</p><div class="kq-row">' +
        '<div><label class="kq-label" for="kq-make">Make &amp; model</label><input class="kq-input" id="kq-make" maxlength="40" placeholder="e.g. Ford Focus" value="' + esc([v.make, S.model].filter(Boolean).join(' ')) + '"/></div>' +
        '<div><label class="kq-label" for="kq-year">Year</label><input class="kq-input" id="kq-year" inputmode="numeric" maxlength="4" placeholder="2016" value="' + esc(v.yearOfManufacture || '') + '"/></div></div>';
    }
    h += '<fieldset class="kq-bands"><legend class="kq-label">Which fits best?</legend>' + Object.keys(C.bands).map(function (b) {
      return '<label class="kq-chip' + (S.band === b ? ' on' : '') + '"><input type="radio" name="band" value="' + b + '"' + (S.band === b ? ' checked' : '') + '/><b>' + esc(C.bands[b].label) + '</b><small>' + esc(C.bands[b].hint) + '</small></label>';
    }).join('') + '</fieldset>';
    return h + nav('flow', 'to-build', 'Next');
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
    if (S.flow === 'tyres') return viewTyres();
    if (S.flow === 'bodywork') return viewBody();
    if (S.flow === 'tuning') return viewTune();
    return viewMech();
  }

  function viewMech() {
    var groups = [{ id: 'servicing', label: 'Servicing & MOT' }, { id: 'mechanical', label: 'Repairs' }];
    var h = '<h2 class="kq-h">Build your job card</h2><p class="kq-help">Tick everything you need. Prices are for ' + esc(vehicleName()) + '.</p>';
    groups.forEach(function (g) {
      var jobs = C.jobs.filter(function (j) { return j.cat === g.id; });
      if (!jobs.length) return;
      h += '<h3 class="kq-sub">' + esc(g.label) + '</h3><div class="kq-jobs">' + jobs.map(function (j) {
        var on = S.mech.indexOf(j.id) !== -1, p = E.priceJob(C, j.id, S.band, { ai: S.ai[j.id] });
        var hint = p.kind === 'fixed' ? p.label : typeof p.low === 'number' ? 'from ' + money(p.low) : p.kind === 'diagnose' ? 'check first' : 'we’ll quote';
        return '<label class="kq-job' + (on ? ' on' : '') + '"><input type="checkbox" value="' + j.id + '"' + (on ? ' checked' : '') + '/><span>' + esc(j.name) + '</span><em>' + esc(hint) + '</em></label>';
      }).join('') + '</div>';
    });
    return h + nav('car', 'to-estimate', S.mech.length ? 'Show my price (' + S.mech.length + ')' : 'Pick at least one', !S.mech.length);
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

  function viewBody() {
    var picked = Object.keys(S.body);
    var h = '<h2 class="kq-h">Tap where it hurts</h2><p class="kq-help">Tap each damaged panel, then tell us what happened to it.</p>' +
      '<div class="kq-bodywrap"><svg class="kq-carsvg" viewBox="0 0 260 516" role="group" aria-label="Car diagram: choose the damaged panels">' +
      '<rect x="18" y="8" width="224" height="500" rx="70" fill="#f7f8fa" stroke="#dde1e8" stroke-width="2"/>' +
      '<path class="kq-glass" d="M66 154 L194 154 L188 192 L72 192 Z"/><path class="kq-glass" d="M72 322 L188 322 L194 358 L66 358 Z"/>' +
      CAR_PANELS.map(function (p) {
        return '<path class="kq-panel' + (S.body[p.id] ? ' on' : '') + '" d="' + p.d + '" data-act="panel" data-v="' + p.id + '" tabindex="0" role="button" aria-pressed="' + !!S.body[p.id] + '"><title>' + esc(p.label) + '</title></path>';
      }).join('') + '</svg><div class="kq-bodyside">' +
      (picked.length ? picked.map(function (id) {
        var p = CAR_PANELS.filter(function (x) { return x.id === id; })[0];
        return '<div class="kq-dmg"><div class="kq-dmg-h"><b>' + esc(p.label) + '</b><button type="button" class="kq-x" data-act="unpanel" data-v="' + id + '" aria-label="Remove ' + esc(p.label) + '">×</button></div>' +
          '<div class="kq-pills">' + C.bodywork_damage.map(function (d) {
            return '<button type="button" class="kq-pill' + (S.body[id] === d.id ? ' on' : '') + '" data-act="dmg" data-v="' + id + ':' + d.id + '">' + esc(d.label) + '</button>';
          }).join('') + '</div></div>';
      }).join('') : '<p class="kq-note">Nothing selected yet. Tap a panel on the car.</p>') +
      '<p class="kq-small">Photos help us price it properly. You can send them on WhatsApp after you book.</p></div></div>';
    return h + nav('car', 'to-estimate', picked.length ? 'Show my price (' + picked.length + ')' : 'Tap a panel first', !picked.length);
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
    if (S.flow === 'mechanical') lines = S.mech.map(function (id) { return E.priceJob(C, id, S.band, { ai: S.ai[id] }); });
    else if (S.flow === 'tyres') lines = [E.tyreLine(C, { width: S.tyre.w, profile: S.tyre.p, rim: S.tyre.r, runflat: S.tyre.rf }, S.tyre.tier, S.tyre.qty)];
    else if (S.flow === 'bodywork') lines = Object.keys(S.body).map(function (id) {
      var p = CAR_PANELS.filter(function (x) { return x.id === id; })[0];
      return E.bodyLine(C, p.key, p.label, S.body[id], S.band);
    }).filter(Boolean);
    else if (S.flow === 'tuning') {
      var t = E.tuneLines(C, S.tune.fuel, Number(S.tune.bhp) || 0, S.tune.stage, S.tune.addons);
      lines = t.lines; S.power = t.power;
    }
    S.lines = lines; S.totals = E.totals(lines);
  }
  function fetchAi() {
    if (S.flow !== 'mechanical') return Promise.resolve();
    var want = S.mech.filter(function (id) { var j = E.findJob(C, id); return j && j.ai && !S.ai[id]; });
    if (!want.length || !S.vehicle || !S.vehicle.make) return Promise.resolve();
    return post('/api/estimate', { vehicle: S.vehicle, model: S.model, band: S.band, jobs: want }, 12000).then(function (r) {
      if (r && r.jobs) Object.keys(r.jobs).forEach(function (id) {
        var a = r.jobs[id];
        if (a && typeof a === 'object') { a.note = E.safeNote(a.note); S.ai[id] = a; }   // filtered again here, not just server-side
      });
    });
  }

  /* ---------- step: estimate ---------- */
  function viewEstimate() {
    if (!S.lines.length) return '<div class="kq-loading" role="status"><span class="kq-spin"></span>Working out your price…</div>';
    var t = S.totals, coupon = C.coupon, eligible = E.couponEligible(C, t, t.unpriced > 0) && !S.offerGone;
    var h = '<div class="kq-result">';
    if (S.power) h += gauge(S.power);
    h += '<p class="kq-for">Your estimate for <strong>' + esc(vehicleName()) + '</strong>' + (S.vehicle && S.vehicle.registrationNumber ? ' <span class="kq-mini-plate">' + esc(S.vehicle.registrationNumber) + '</span>' : '') + '</p>' +
      '<ul class="kq-lines">' + S.lines.map(function (l) {
        var price = typeof l.low === 'number' ? '<b>' + range(l.low, l.high) + '</b>' : '<b class="kq-tbc">' + (l.kind === 'photo' ? 'Send photos' : l.kind === 'diagnose' ? 'Check first' : 'We’ll quote') + '</b>';
        var tags = [];
        if (l.source === 'ai') tags.push('Priced for your car');
        if (l.confidence === 'low') tags.push('Wide range, confirmed before any work');
        if (l.part) tags.push('Panel cost confirmed after we see it');
        return '<li class="kq-line"><div><strong>' + esc(l.name) + '</strong>' + (l.note ? '<p>' + esc(l.note) + '</p>' : '') +
          (tags.length ? '<small>' + tags.join(' · ') + '</small>' : '') + '</div>' + price + '</li>';
      }).join('') + '</ul>';
    if (t.count) {
      h += '<div class="kq-total"><span>Your estimate' + (t.unpriced ? ' so far' : '') + '</span><b>' + range(t.low, t.high) + '</b></div>';
      if (t.showDealer) h += '<div class="kq-dealer"><span>Typical main dealer</span><s>~' + money(t.dealer) + '</s><em>Around ' + money(Math.max(0, Math.round((t.dealer - (t.low + t.high) / 2) / 5) * 5)) + ' less</em></div>';
    }
    if (eligible) {
      h += '<div class="kq-offer"><div><b>' + money(coupon.amount) + ' off if you book online now</b>' +
        '<span>Book a slot in the next <i id="kq-timer">' + fmtLeft() + '</i> and we&rsquo;ll take ' + money(coupon.amount) + ' off this job. Code ' + esc(coupon.code) + '.</span></div></div>';
    }
    h += '<p class="kq-small">Includes VAT, parts and labour. It&rsquo;s an estimate: we confirm a fixed written price before any work starts and nothing is done without your OK. If the real price lands outside this range, you decide whether to go ahead, and you owe us nothing for looking. 12-month workmanship warranty.</p></div>' +
      '<div class="kq-nav"><button type="button" class="kq-btn kq-btn-ghost" data-act="back" data-v="build">Change the job</button>' +
      '<button type="button" class="kq-btn kq-btn-main" data-act="to-details">' + (eligible ? 'Book and save ' + money(coupon.amount) : 'Book this in') + '</button></div>' +
      '<p class="kq-or">or <a href="' + waLink() + '" target="_blank" rel="noopener" data-act="wa">send it to us on WhatsApp</a> · <a href="tel:' + PHONE_TEL + '">call ' + PHONE + '</a></p>';
    return h;
  }
  function fmtLeft() {
    var left = Math.max(0, S.expires - Date.now());
    return String(Math.floor(left / 60000)).padStart(2, '0') + ':' + String(Math.floor(left % 60000 / 1000)).padStart(2, '0');
  }
  function startTimer() {
    clearInterval(TICK);
    if (!S.expires) S.expires = Date.now() + (C.coupon.hold_minutes || 15) * 60000;
    TICK = setInterval(function () {
      var el = $('#kq-timer');
      if (!el) return;
      el.textContent = fmtLeft();
      if (S.expires - Date.now() <= 0) { clearInterval(TICK); S.offerGone = true; save(); render(); }
    }, 1000);
  }

  /* ---------- step: details ---------- */
  function viewDetails() {
    return '<h2 class="kq-h">Where shall we send it?</h2><p class="kq-help">We&rsquo;ll check the detail for your car and send the full written estimate. Then pick your slot.</p>' +
      summaryStrip() +
      '<form class="kq-lead" novalidate><div class="kq-row">' +
      '<div><label class="kq-label" for="kq-name">Name</label><input class="kq-input" id="kq-name" name="name" autocomplete="name" required maxlength="60"/></div>' +
      '<div><label class="kq-label" for="kq-phone">Mobile</label><input class="kq-input" id="kq-phone" name="phone" type="tel" inputmode="tel" autocomplete="tel" required maxlength="20"/></div></div>' +
      '<div class="kq-row"><div><label class="kq-label" for="kq-email">Email <span class="kq-opt">(optional)</span></label><input class="kq-input" id="kq-email" name="email" type="email" autocomplete="email" maxlength="80"/></div>' +
      '<div><label class="kq-label" for="kq-reg2">Reg</label><input class="kq-input" id="kq-reg2" name="reg" maxlength="10" value="' + esc((S.vehicle && S.vehicle.registrationNumber) || S.reg) + '"/></div></div>' +
      '<label class="kq-check"><input type="checkbox" name="collect"/> Please collect and return my car</label>' +
      '<button class="kq-btn kq-btn-main" type="submit">Next: pick my slot</button>' +
      '<p class="kq-err" role="alert" hidden></p>' +
      '<p class="kq-small">We only use your details to arrange this job.</p></form>' +
      '<div class="kq-nav"><button type="button" class="kq-btn kq-btn-ghost" data-act="back" data-v="estimate">Back to the price</button></div>';
  }
  function summaryStrip() {
    var t = S.totals;
    return '<div class="kq-strip"><div><b>' + esc(FLOWS[S.flow].label) + '</b><span>' + esc(vehicleName()) + '</span></div>' +
      (t && t.count ? '<div class="kq-strip-p"><b>' + range(t.low, t.high) + '</b>' + (!S.offerGone && E.couponEligible(C, t, t.unpriced > 0) ? '<span>less ' + money(C.coupon.amount) + ' if booked now <i id="kq-timer">' + fmtLeft() + '</i></span>' : '') + '</div>' : '') + '</div>';
  }

  /* ---------- step: calendar ---------- */
  function viewCalendar() {
    var cal = FLOWS[S.flow].cal, days = E.bookableDays(C, cal);
    var day = S.day ? days.filter(function (d) { return d.key === S.day; })[0] : null;
    return '<h2 class="kq-h">Pick your ' + (cal === 'bodywork' ? 'drop-off' : 'slot') + '</h2>' +
      '<p class="kq-help">' + (cal === 'bodywork' ? 'Bodywork stays with us, so this is when you drop it off.' : 'Most mechanical jobs are done the same day.') + '</p>' +
      summaryStrip() +
      '<div class="kq-days">' + days.map(function (d) {
        return '<button type="button" class="kq-day' + (S.day === d.key ? ' on' : '') + '" data-act="day" data-v="' + d.key + '"><i>' + d.dow + '</i><b>' + d.dom + '</b><span>' + d.mon + '</span></button>';
      }).join('') + '</div>' +
      (day ? '<label class="kq-label">' + esc(day.long) + '</label><div class="kq-pills">' +
        day.slots.map(function (s) { return '<button type="button" class="kq-pill' + (S.time === s ? ' on' : '') + '" data-act="time" data-v="' + s + '">' + s + '</button>'; }).join('') + '</div>' : '') +
      '<div class="kq-nav"><button type="button" class="kq-btn kq-btn-ghost" data-act="skip-slot">I&rsquo;ll sort the time later</button>' +
      '<button type="button" class="kq-btn kq-btn-main" data-act="confirm"' + (S.day && S.time ? '' : ' disabled') + '>Confirm my booking</button></div>';
  }

  /* ---------- step: done ---------- */
  function viewDone() {
    var booked = S.day && S.time, cal = FLOWS[S.flow].cal;
    var when = booked ? new Date(S.day).toLocaleDateString('en-GB', { weekday: 'long', day: 'numeric', month: 'long' }) + ' at ' + S.time : null;
    return '<div class="kq-done"><h2 class="kq-h">' + (booked ? 'You&rsquo;re booked in.' : 'Your estimate is on its way.') + '</h2>' +
      (booked ? '<p class="kq-big-when">' + esc(when) + '</p><p>' + (cal === 'bodywork' ? 'Drop the car to us at Unit 1, Soho Mills, Hackbridge SM6 7HN.' : 'Bring it to Unit 1, Soho Mills, Hackbridge SM6 7HN.') + ' We&rsquo;ll call to confirm and send the written price first.</p>'
        : '<p>We&rsquo;ve got your details and will be in touch, usually within 30 minutes during opening hours (Mon–Sat 8am–8pm).</p>') +
      (booked && !S.offerGone ? '<p class="kq-saved"><b>' + money(C.coupon.amount) + ' online booking discount applied</b> · code ' + esc(C.coupon.code) + '</p>' : '') +
      (S.flow === 'bodywork' ? '<p>Send us photos of the damage and we can have the parts ready:</p>' : '') +
      '<div class="kq-nav-wrap"><a class="kq-btn kq-btn-wa" href="' + waLink() + '" target="_blank" rel="noopener">' + (S.flow === 'bodywork' ? 'Send photos on WhatsApp' : 'Message us on WhatsApp') + '</a> ' +
      '<a class="kq-btn kq-btn-ghost" href="tel:' + PHONE_TEL + '">Call ' + PHONE + '</a></div></div>';
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
      priority: S.day && S.time ? 'hot' : 'warm',
      source: 'Website instant quote',
      stage: 'intake',
      name: S.lead.name, phone: S.lead.phone, email: S.lead.email || '',
      reg: S.lead.reg || v.registrationNumber || '',
      vehicle: { make: v.make || '', model: S.model || '', year: v.yearOfManufacture || '', engine_cc: v.engineCapacity || '', fuel: v.fuelType || '', size: C.bands[S.band].label, motExpiry: v.motExpiryDate || '' },
      service: FLOWS[S.flow].label,
      jobs: S.lines.map(function (l) { return { name: l.name, low: l.low, high: l.high, source: l.source || l.kind, hours: l.hours || null, parts: l.parts || null }; }),
      webEstimate: t && t.count ? { lo: t.low, hi: t.high } : null,
      requestedSlot: S.day && S.time ? { calendar: FLOWS[S.flow].cal, date: S.day, time: S.time } : null,
      collection: !!S.lead.collect,
      coupon: (S.day && S.time && !S.offerGone) ? { code: C.coupon.code, amount: C.coupon.amount, minSpend: C.coupon.min_spend } : null,
      priceBookVersion: C.version,
      log: [{ at: new Date().toISOString(), by: 'Website', text: (S.day && S.time ? 'HOT: accepted the range and booked ' + S.day + ' ' + S.time : 'Estimate sent, no slot picked') }]
    };
  }
  function sendLead() {
    var d = leadPayload(), id = S.lead.id || (S.lead.id = 'web-' + Date.now().toString(36));
    var fd = new FormData();
    fd.append('access_key', WEB3FORMS_KEY);
    fd.append('subject', (d.priority === 'hot' ? 'BOOKED' : 'Estimate') + ': ' + d.service + ' · ' + vehicleName() + (d.webEstimate ? ' · ' + range(d.webEstimate.lo, d.webEstimate.hi) : ''));
    fd.append('from_name', 'KITH website instant quote');
    fd.append('Name', d.name); fd.append('Phone', d.phone);
    if (d.email) { fd.append('email', d.email); fd.append('Email', d.email); }
    fd.append('Registration', d.reg || '-');
    fd.append('Vehicle', [d.vehicle.year, d.vehicle.make, d.vehicle.model].filter(Boolean).join(' ') + ' · ' + d.vehicle.size);
    fd.append('Service', d.service);
    fd.append('Quote', d.jobs.map(function (j) { return '• ' + j.name + (typeof j.low === 'number' ? ': ' + range(j.low, j.high) : ': to confirm'); }).join('\n') + (d.webEstimate ? '\nEstimate: ' + range(d.webEstimate.lo, d.webEstimate.hi) : ''));
    fd.append('Slot', d.requestedSlot ? d.requestedSlot.date + ' ' + d.requestedSlot.time + ' (' + d.requestedSlot.calendar + ')' : 'not picked');
    fd.append('Collection', d.collection ? 'Yes, please collect' : 'No');
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
        if (r.vehicle) { S.vehicle = r.vehicle; S.manual = false; S.band = E.guessBand(r.vehicle); track('vehicle_found'); render(); save(); }
        else if (r._status === 404) { b.disabled = false; b.textContent = 'Find my car'; err.innerHTML = 'We couldn’t find that reg. Check it, or <button type="button" class="kq-link" data-act="manual">enter the car yourself</button>.'; err.hidden = false; }
        else { S.vehicle = { registrationNumber: reg }; S.manual = true; render(); save(); }
      });
    });
    $$('input[name=band]').forEach(function (r) {
      r.addEventListener('change', function () { S.band = r.value; $$('.kq-chip').forEach(function (c) { c.classList.toggle('on', c.querySelector('input').checked); }); save(); });
    });
  }
  function bindBuild() {
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
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var err = f.querySelector('.kq-err'), name = f.name.value.trim(), phone = f.phone.value.replace(/[^\d+]/g, '');
      if (!name || phone.length < 10) { err.textContent = 'Please add your name and a mobile number so we can confirm.'; err.hidden = false; return; }
      S.lead = { id: S.lead && S.lead.id, name: name, phone: phone, email: f.email.value.trim(), reg: f.reg.value.toUpperCase().trim(), collect: f.collect.checked };
      var b = f.querySelector('button[type=submit]'); b.disabled = true; b.textContent = 'Saving…';
      sendLead().then(function (res) {
        track('generate_lead', { value: S.totals ? S.totals.low : 0, currency: 'GBP', flow: S.flow });
        if (!res.emailed && res.crm !== 'sent') { b.disabled = false; b.textContent = 'Next: pick my slot'; err.innerHTML = 'That didn’t send. Please <a href="tel:' + PHONE_TEL + '">call ' + PHONE + '</a> or <a href="' + waLink() + '" target="_blank" rel="noopener">WhatsApp us</a>.'; err.hidden = false; return; }
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
    else if (a === 'add-mot') { if (S.mech.indexOf('mot') === -1) S.mech.push('mot'); track('quote_add_mot'); save(); render(); }
    else if (a === 'to-build') { readCar(); go('build'); }
    else if (a === 'to-estimate') {
      readBuild(); S.lines = []; go('estimate');
      fetchAi().then(function () {
        compute();
        if (!S.expires) S.expires = Date.now() + (C.coupon.hold_minutes || 15) * 60000;
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
    else if (a === 'unpanel') { delete S.body[v]; save(); render(); }
    else if (a === 'dmg') { var p = v.split(':'); S.body[p[0]] = p[1]; save(); render(); }
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
  root.addEventListener('keydown', function (e) {
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
    if (S.sent) { S.sent = false; S.lines = []; S.mech = []; S.body = {}; S.expires = 0; S.offerGone = false; S.day = S.time = null; }
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
