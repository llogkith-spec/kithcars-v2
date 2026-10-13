/* KITH Cars Garage & Bodyworks — site analytics.
   One job: know which pages bring in work, and where people drop out of the instant quote.

   TO SWITCH ON: paste your GA4 Measurement ID (looks like G-ABC1234XYZ) into GA_ID below, and redeploy.
   With it blank, nothing is sent anywhere: every event still goes into window.dataLayer, so a tag
   manager (or the console) can see it, but no third-party script is loaded and no cookie is set.

   Events sent (all from the customer's own browser, no personal data in any of them):
     page_view          automatic, GA4
     quote_cta_click    someone clicked an "instant quote" button        {page, label}
     quote_start        reg entered in the quote                          {flow}     (quote.js)
     quote_flow         picked mechanical / tyres / bodywork / tuning     {flow}     (quote.js)
     vehicle_found      DVLA lookup returned their car                               (quote.js)
     quote_price        a price was shown                                 {value}    (quote.js)
     quote_book_click   moved from the price to the booking form                     (quote.js)
     generate_lead      details submitted                                 {value}    (quote.js)
     quote_booked       a slot was taken                                  {value}    (quote.js)
     call_click         tapped a phone number                             {page}
     whatsapp_click     tapped WhatsApp                                   {page}
     email_click        tapped the email address                          {page}
     directions_click   opened Google Maps directions                     {page}
     booking_submit     the older booking form was sent                   {page}
     scroll_50 / _90    read half / nearly all of the page                {page}
   The funnel that matters: quote_cta_click -> quote_start -> quote_price -> generate_lead -> quote_booked.
*/
(function () {
  'use strict';
  var GA_ID = '';                      // <-- your GA4 Measurement ID goes here
  var dl = (window.dataLayer = window.dataLayer || []);

  if (GA_ID) {
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(GA_ID);
    document.head.appendChild(s);
    window.gtag = window.gtag || function () { dl.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', GA_ID, { anonymize_ip: true });
  }

  function ev(name, params) {
    try {
      if (window.gtag && GA_ID) window.gtag('event', name, params || {});
      else dl.push(Object.assign({ event: name }, params || {}));
    } catch (e) {}
  }
  window.kithTrack = ev;                // quote.js falls back to dataLayer on its own; this is for anything else

  var page = location.pathname;
  function closest(el, sel) {
    while (el && el.nodeType === 1) { if (el.matches && el.matches(sel)) return el; el = el.parentElement; }
    return null;
  }
  function label(el) { return (el.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 60); }

  document.addEventListener('click', function (e) {
    var a = closest(e.target, 'a,button');
    if (!a) return;
    var href = a.getAttribute('href') || '';
    if (/^tel:/i.test(href)) return ev('call_click', { page: page, label: label(a) });
    if (/wa\.me|api\.whatsapp\.com/i.test(href)) return ev('whatsapp_click', { page: page });
    if (/^mailto:/i.test(href)) return ev('email_click', { page: page });
    if (/google\.[a-z.]+\/maps/i.test(href)) return ev('directions_click', { page: page });
    if (a.hasAttribute('data-quote') || href === '#quote' || href.indexOf('#get-a-quote') > -1)
      return ev('quote_cta_click', { page: page, label: label(a) });
  }, true);

  document.addEventListener('submit', function (e) {
    var f = e.target;
    if (f && (f.id === 'booking-wizard' || (f.closest && f.closest('#booking-wizard'))))
      ev('booking_submit', { page: page });
  }, true);

  var hit = {};
  function depth() {
    var h = document.documentElement;
    var total = Math.max(h.scrollHeight - h.clientHeight, 1);
    var pct = ((window.pageYOffset || h.scrollTop) / total) * 100;
    if (pct >= 50 && !hit[50]) { hit[50] = 1; ev('scroll_50', { page: page }); }
    if (pct >= 90 && !hit[90]) { hit[90] = 1; ev('scroll_90', { page: page }); window.removeEventListener('scroll', throttled); }
  }
  var waiting = false, throttled = function () {
    if (waiting) return;
    waiting = true;
    setTimeout(function () { waiting = false; depth(); }, 400);
  };
  window.addEventListener('scroll', throttled, { passive: true });
})();
