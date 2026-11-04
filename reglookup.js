/* reglookup.js — adds the DVLA/DVSA registration lookup to the booking wizard's reg fields.
   The wizard predates the quote engine and asked people to type their reg blind. This attaches the
   same /api/vehicle lookup the quote widget uses, so the customer sees their car confirmed back to
   them before they book — and where the form has a Make & Model box, it fills it in for them.

   Self-initialising: no markup changes needed on the 78 pages that carry the wizard. It finds the
   reg inputs by id, or any input carrying data-reg-lookup.

   If the credentials aren't live the lookup fails quietly and the form still works exactly as it
   did — typing the reg by hand was always the fallback. */
(function () {
  'use strict';

  var FIELDS = [
    { reg: 'r-reg',  make: 'r-make'  },   // Repairs
    { reg: 's-reg',  make: 's-make'  },   // Servicing
    { reg: 't-reg',  make: null      },   // Tyres
    { reg: 'm-reg',  make: null      },   // MOT
    { reg: 'bw-reg', make: null      }    // Bodywork
  ];

  var CSS = [
    '.rl-wrap{margin-top:.45rem}',
    '.rl-btn{appearance:none;border:1px solid var(--gold,#B8862A);background:var(--gold,#B8862A);',
    'color:#16120A;font:600 .82rem/1 inherit;padding:.6rem .95rem;border-radius:999px;cursor:pointer}',
    '.rl-btn[disabled]{opacity:.55;cursor:default}',
    '.rl-out{display:none;margin-top:.5rem;padding:.6rem .75rem;border-radius:10px;font-size:.86rem;line-height:1.45}',
    '.rl-out.on{display:block}',
    '.rl-ok{background:#f3f8f1;border-left:3px solid #2f7d32;color:#1f4620}',
    '.rl-ok b{display:block;font-size:.95rem;margin-bottom:.1rem}',
    '.rl-no{background:#fdf5f3;border-left:3px solid #b3402b;color:#7d2c1c}',
    '.rl-meta{opacity:.8}',
    '.rl-again{background:none;border:0;padding:0;font:inherit;color:inherit;',
    'text-decoration:underline;cursor:pointer}'
  ].join('');

  function styles() {
    if (document.getElementById('rl-css')) return;
    var s = document.createElement('style');
    s.id = 'rl-css'; s.textContent = CSS;
    document.head.appendChild(s);
  }

  function clean(v) { return String(v || '').toUpperCase().replace(/[^A-Z0-9]/g, ''); }

  function titled(s) {
    return String(s || '').toLowerCase().replace(/\b[a-z]/g, function (c) { return c.toUpperCase(); });
  }

  /* "2.0 litre petrol · Blue · 2019" — only the parts the API actually returned. */
  function describe(v) {
    var bits = [];
    if (v.engineCapacity) bits.push((Math.round(v.engineCapacity / 100) / 10).toFixed(1) + ' litre');
    if (v.fuelType) bits.push(titled(v.fuelType));
    if (v.colour) bits.push(titled(v.colour));
    if (v.yearOfManufacture) bits.push(v.yearOfManufacture);
    return bits.join(' · ');
  }

  function headline(v) {
    var n = [titled(v.make), v.model ? titled(v.model) : ''].filter(Boolean).join(' ');
    return n || 'Vehicle found';
  }

  /* MOT expiry is worth surfacing: someone booking a service often needs the MOT too, and someone
     booking an MOT sometimes books one they don't need yet. */
  function motLine(v) {
    if (!v.motExpiryDate) return '';
    var d = new Date(v.motExpiryDate);
    if (isNaN(d)) return '';
    var days = Math.round((d - new Date()) / 86400000);
    var when = d.toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' });
    if (days < 0) return 'MOT expired ' + when + '.';
    if (days <= 60) return 'MOT runs out ' + when + ' — worth booking both together.';
    return 'MOT valid to ' + when + '.';
  }

  function attach(spec) {
    var input = document.getElementById(spec.reg);
    if (!input || input.dataset.rlBound) return;
    input.dataset.rlBound = '1';

    var wrap = document.createElement('div');
    wrap.className = 'rl-wrap';
    var btn = document.createElement('button');
    btn.type = 'button'; btn.className = 'rl-btn'; btn.textContent = 'Check my car';
    var out = document.createElement('div');
    out.className = 'rl-out';
    out.setAttribute('role', 'status');
    wrap.appendChild(btn); wrap.appendChild(out);
    input.parentNode.insertBefore(wrap, input.nextSibling);

    function show(cls, html) {
      out.className = 'rl-out on ' + cls;
      out.innerHTML = html;
    }

    function manual() {
      out.className = 'rl-out';
      btn.disabled = false; btn.textContent = 'Check my car';
      input.focus();
    }

    out.addEventListener('click', function (e) {
      if (e.target.classList.contains('rl-again')) manual();
    });

    function look() {
      var reg = clean(input.value);
      if (!/^[A-Z0-9]{2,8}$/.test(reg)) {
        show('rl-no', 'That doesn’t look like a UK registration — have another look.');
        return;
      }
      input.value = reg;
      btn.disabled = true; btn.textContent = 'Checking…';
      show('rl-ok rl-meta', 'Looking up ' + reg + '…');

      var ctrl = typeof AbortController === 'function' ? new AbortController() : null;
      var timer = setTimeout(function () { ctrl && ctrl.abort(); }, 8000);

      fetch('/api/vehicle', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ reg: reg }),
        signal: ctrl && ctrl.signal
      })
        .then(function (r) { return r.json().then(function (j) { j._status = r.status; return j; }); })
        .then(function (r) {
          clearTimeout(timer);
          btn.disabled = false;
          if (r && r.vehicle) {
            var v = r.vehicle;
            btn.textContent = 'Check a different reg';
            var meta = [describe(v), motLine(v)].filter(Boolean).join('<br>');
            show('rl-ok', '<b>' + headline(v) + '</b>' +
              (meta ? '<span class="rl-meta">' + meta + '</span>' : '') +
              '<br><button type="button" class="rl-again">Not your car? Enter it yourself</button>');
            if (spec.make) {
              var mk = document.getElementById(spec.make);
              // Don't overwrite something they've typed themselves.
              if (mk && !mk.value.trim()) {
                mk.value = [headline(v), v.yearOfManufacture].filter(Boolean).join(' ');
              }
            }
            if (window.kcTrack) window.kcTrack('vehicle_found', { where: 'wizard' });
            return;
          }
          btn.textContent = 'Try again';
          if (r && r._status === 404) {
            show('rl-no', 'We couldn’t find that registration. Check it, or just carry on and ' +
              'type the make and model — we’ll confirm the car when you arrive.');
          } else {
            // 503 (credentials not live), 502, 429, network. Never block the booking over it.
            show('rl-no', 'The lookup isn’t responding right now. Carry on and book — ' +
              'we’ll check the registration at our end.');
          }
        })
        .catch(function () {
          clearTimeout(timer);
          btn.disabled = false; btn.textContent = 'Try again';
          show('rl-no', 'The lookup isn’t responding right now. Carry on and book — ' +
            'we’ll check the registration at our end.');
        });
    }

    btn.addEventListener('click', look);
    input.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') { e.preventDefault(); look(); }
    });
  }

  function init() {
    styles();
    FIELDS.forEach(attach);
    [].forEach.call(document.querySelectorAll('input[data-reg-lookup]'), function (el) {
      if (el.id) attach({ reg: el.id, make: el.dataset.regMake || null });
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
