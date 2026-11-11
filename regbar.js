/* Sticky reg plate under the header on phones — one for every service and location page.
   The homepage already puts the reg card in its hero, so this file skips that one
   and gets out of the way. Everywhere else the reg plate was buried a screen or
   two down inside the booking widget; now it is the first thing a phone reader sees. */
(function () {
  'use strict';
  if (!window.matchMedia || !window.matchMedia('(max-width:720px)').matches) return;

  // Skip the homepage — it has its own reg card in the hero now.
  var path = (location.pathname || '').toLowerCase();
  if (path === '/' || path === '/index.html' || path === '/index') return;

  // Only run on pages that actually route the reg to a quote form (every service and location page).
  var target = document.getElementById('get-a-quote') || document.getElementById('quote') || document.querySelector('[data-quote]');
  if (!target) return;

  // If a reg bar is already present, don't double-stack it.
  if (document.querySelector('.kith-regbar')) return;

  // Build the bar.
  var bar = document.createElement('form');
  bar.className = 'kith-regbar';
  bar.setAttribute('aria-label', 'Get an instant price');
  bar.innerHTML =
    '<label class="kith-regbar-plate" aria-label="Vehicle registration">' +
      '<span class="kith-regbar-uk">UK</span>' +
      '<input type="text" name="reg" placeholder="AB12 CDE" maxlength="8" autocomplete="off" autocapitalize="characters" spellcheck="false" inputmode="text">' +
    '</label>' +
    '<button type="submit" class="kith-regbar-go">Get price →</button>';

  // Normalise: strip spaces, uppercase, re-insert single space mid-plate for readability.
  var input = bar.querySelector('input');
  input.addEventListener('input', function () {
    var v = (input.value || '').toUpperCase().replace(/[^A-Z0-9]/g, '');
    if (v.length > 4) v = v.slice(0, 4) + ' ' + v.slice(4);
    input.value = v;
  });

  // Submit: carry the reg value to the quote form's reg field if there is one, then scroll
  // to the quote section. Tries common names first, falls back to the first text input in
  // the quote section.
  bar.addEventListener('submit', function (e) {
    e.preventDefault();
    var reg = (input.value || '').trim();
    var section = document.getElementById('get-a-quote') || document.getElementById('quote');
    if (section && reg) {
      var dst =
        section.querySelector('input[name="reg"]') ||
        section.querySelector('input[name="r-reg"]') ||
        section.querySelector('input[name="plate"]') ||
        section.querySelector('input[name="vehicle_reg"]') ||
        section.querySelector('input[type="text"]');
      if (dst) {
        dst.value = reg;
        try { dst.dispatchEvent(new Event('input', { bubbles: true })); } catch (_) {}
      }
    }
    if (section && typeof section.scrollIntoView === 'function') {
      section.scrollIntoView({ behavior: 'smooth', block: 'start' });
      // After the scroll lands, focus the destination so the keyboard reopens.
      setTimeout(function () {
        var dst2 = (section.querySelector('input[name="reg"]') ||
                    section.querySelector('input[name="r-reg"]') ||
                    section.querySelector('input[type="text"]'));
        if (dst2 && reg) {
          try { dst2.focus({ preventScroll: true }); } catch (_) { dst2.focus(); }
        }
      }, 450);
    } else {
      // No quote section on this page — fall back to the homepage quote.
      location.href = '/#quote' + (reg ? '?reg=' + encodeURIComponent(reg) : '');
    }

    // Analytics parity with the rest of the funnel.
    if (typeof window.gtag === 'function') {
      window.gtag('event', 'regbar_submit', { reg_filled: reg.length > 0 });
    }
  });

  // Sit the bar RIGHT INSIDE the sticky/fixed header, as its last child, so it moves
  // with the header and no separate top-offset logic is needed. On service and
  // location pages the header is .site-header with `position: fixed`; appending
  // the bar to it makes the bar fixed too, below the logo row, always visible.
  var header = document.querySelector('.site-header') || document.querySelector('.hd') || document.querySelector('header');
  if (header) {
    header.appendChild(bar);
    // Tell the page's CSS that the reg bar is present so .page-hero can give its
    // top padding enough room for both the logo row and the reg bar (styles.css
    // has the `.has-regbar .page-hero` rule).
    document.body.classList.add('has-regbar');
  } else {
    document.body.insertBefore(bar, document.body.firstChild);
    document.body.classList.add('has-regbar');
  }
})();
