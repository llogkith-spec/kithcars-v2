/* KITH Cars Garage & Bodyworks — site analytics.
   One job: know which pages bring in work, and where people drop out of the instant quote.

   TO SWITCH ON: paste your GA4 Measurement ID (looks like G-ABC1234XYZ) into GA_ID below, and redeploy.
   With it blank, nothing is sent anywhere: every event still goes into window.dataLayer, so a tag
   manager (or the console) can see it, but no third-party script is loaded and no cookie is set.
   FB_ID is the Meta dataset (pixel) id and works the same way: blank it and no Meta script loads.

   Neither is gated on consent, because this site has no consent banner. Under UK PECR both of
   these need permission before they fire. Logan was told this when the pixel went in and chose
   to run it; the gate is a banner away if that changes, and ev() is the single place to hook it.

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
  var GA_ID = 'G-7NH2HFJWNQ';          // KITH Cars GA4 property "kith cars web"
  var FB_ID = '1431276708362160';      // Meta dataset (pixel) for the KITH Cars ad account
  var dl = (window.dataLayer = window.dataLayer || []);

  /* Our events, named for Meta. Only the ones Meta has a standard event for are sent: a custom
     event name cannot be optimised against or used to build a lookalike, so sending the rest
     would fill the account with noise that no campaign can act on.

     The point of the mapping is the money. A pixel that only sees PageView teaches Facebook to
     find people who visit websites; one that sees Purchase with a job value teaches it to find
     people who book work, which is a different thing entirely. */
  var FB_EVENTS = {
    /* The funnel as Logan reads it, which is also the standard shape: look the car up, see the
       price, start booking, leave details, book. Meta's names were a step ahead of the customer
       before - InitiateCheckout fired merely on seeing a price, when nothing had been started -
       so an audience of "began booking" was really an audience of "glanced at a figure". */
    vehicle_found: 'Search',           // reg looked up and a car came back
    quote_price: 'ViewContent',        // the estimate appeared, with its value
    quote_book_click: 'InitiateCheckout', // tapped through to book - checkout has begun
    generate_lead: 'Lead',             // details submitted
    booking_submit: 'Lead',            // the older booking form, same outcome
    // A booking is both of these. Purchase carries the job value and is what Meta optimises
    // hardest against; Schedule is the name Meta made for appointments and is what the account
    // will read naturally in a year. Sending both costs nothing and loses neither.
    quote_booked: ['Purchase', 'Schedule'],
    directions_click: 'FindLocation',  // they are working out how to get here
    call_click: 'Contact',
    whatsapp_click: 'Contact',
    quote_whatsapp: 'Contact',         // sent their quote through to us on WhatsApp
    email_click: 'Contact',
  };

  if (GA_ID) {
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(GA_ID);
    document.head.appendChild(s);
    window.gtag = window.gtag || function () { dl.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', GA_ID, { anonymize_ip: true });
  }

  if (FB_ID) {
    /* Meta's own loader, verbatim apart from the id. It defines fbq before the script arrives and
       queues anything fired in the meantime, so an event in the first second is not lost. */
    !function (f, b, e, v, n, t, s) {
      if (f.fbq) return; n = f.fbq = function () {
        n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments);
      };
      if (!f._fbq) f._fbq = n;
      n.push = n; n.loaded = !0; n.version = '2.0'; n.queue = [];
      t = b.createElement(e); t.async = !0; t.src = v;
      s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s);
    }(window, document, 'script', 'https://connect.facebook.net/en_US/fbevents.js');
    window.fbq('init', FB_ID);
    window.fbq('track', 'PageView');
  }

  function ev(name, params) {
    try {
      if (window.gtag && GA_ID) window.gtag('event', name, params || {});
      else dl.push(Object.assign({ event: name }, params || {}));
    } catch (e) {}
    try {
      // Sent separately rather than inside the block above: if Google is switched off or its
      // script is blocked, Meta must still get the conversion. They are two accounts, not one.
      var mapped = FB_ID && window.fbq && FB_EVENTS[name];
      if (!mapped) return;
      var p = params || {};
      var value = Number(p.value);
      var payload = (value > 0)
        ? { value: Math.round(value * 100) / 100, currency: p.currency || 'GBP' }
        : {};
      // One of ours can be two of theirs: a booking is a Purchase and a Schedule at once.
      var names = (typeof mapped === 'string') ? [mapped] : mapped;
      for (var i = 0; i < names.length; i++) window.fbq('track', names[i], payload);
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
