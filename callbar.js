/* Sticky call bar for phones. Injected rather than written into 934 pages, so the markup and the
   tracking live in one file. Appears once the reader has committed to the page, not instantly:
   a bar that slides up before anyone has read a line is just an obstruction. */
(function () {
  'use strict';
  if (window.matchMedia && !window.matchMedia('(max-width:760px)').matches) return;
  if (document.querySelector('.kc-bar')) return;

  var PHONE = '020 4629 9469';
  var TEL = '+442046299469';
  var WA = 'https://wa.me/447923688259';

  var icon = {
    phone: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>',
    wa: '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M17.5 14.4c-.3-.2-1.7-.9-2-1-.3-.1-.5-.1-.7.1-.2.3-.7 1-.9 1.2-.2.2-.3.2-.6.1-1.7-.9-2.9-1.6-4-3.6-.3-.5.3-.5.9-1.6.1-.2 0-.4 0-.5s-.7-1.6-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.2.2 2.1 3.3 5.2 4.6 1.9.8 2.7.9 3.6.8.6-.1 1.7-.7 1.9-1.4.2-.7.2-1.2.2-1.4-.1-.1-.3-.2-.6-.3z"/><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2c-1.5 0-3-.4-4.3-1.2l-.3-.2-3.1.8.8-3-.2-.3A8.2 8.2 0 1 1 12 20.2z"/></svg>',
    // A pound sign, not a dollar. The stock "price" glyph in most icon sets is $, which on a
    // South London garage reads as somebody else's website.
    quote: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 5.5a4 4 0 0 0-7 2.6V13a4 4 0 0 1-2 3.5M6.5 12.5h7M6 19h12"/></svg>',
  };

  // Point at the quote widget if this page has one, otherwise at the homepage's.
  var quoteHref = document.querySelector('#kq, #quote, [data-quote]') ? '#quote' : '/#quote';

  var bar = document.createElement('nav');
  bar.className = 'kc-bar';
  bar.setAttribute('aria-label', 'Contact KITH Cars');
  bar.innerHTML =
    '<a href="tel:' + TEL + '" data-track="call" class="kc-bar-call">' + icon.phone + '<span>Call us</span></a>' +
    '<a href="' + WA + '" target="_blank" rel="noopener" data-track="whatsapp" class="kc-bar-wa">' + icon.wa + '<span>WhatsApp</span></a>' +
    '<a href="' + quoteHref + '" data-track="quote" class="kc-bar-quote">' + icon.quote + '<span>Get a price</span></a>';
  document.body.appendChild(bar);

  // Show it once the reader has committed to the page. 2026-11-11: dropped
  // from "60% of viewport or 420px" to "25% of viewport or 180px" — the
  // floating WhatsApp bubble used to cover the first-screen contact need,
  // but it was hiding body text on service/location pages, so it's gone on
  // phones now and the sticky bar has to carry the first-screen CTA instead.
  var shown = false;
  function check() {
    var past = window.scrollY > Math.min(window.innerHeight * 0.25, 180);
    if (past === shown) return;
    shown = past;
    bar.classList.toggle('on', past);
  }
  check();
  window.addEventListener('scroll', check, { passive: true });

  // Feed the same funnel events analytics.js already listens for, when it is switched on.
  bar.addEventListener('click', function (e) {
    var a = e.target.closest('a[data-track]');
    if (!a || typeof window.gtag !== 'function') return;
    window.gtag('event', a.dataset.track + '_click', { source: 'sticky_bar' });
  });
})();
