/* KITH simple quote form -> unified inbox.
   The short "quote-request" forms (about-us, faq) used to rely on Netlify Forms, which only works on
   Netlify. This sends them straight into the KITH inbox instead (the same door the instant quote uses),
   so they work on any host. On success the customer goes to the thank-you page; if the send fails,
   they are told to call or WhatsApp rather than being shown a thank-you for a lead that never arrived. */
(function () {
  var URL = 'https://mxyrxyhvjndgjqupgstu.supabase.co/functions/v1/inbox-ingest';
  var KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im14eXJ4eWh2am5kZ2pxdXBnc3R1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODIyMTMyNjgsImV4cCI6MjA5Nzc4OTI2OH0.z7F_sUqx56bIcBLxjWFJSP3rT1jhNPAL9_1SWZ7cUog';

  function val(f, n) { var el = f.querySelector('[name="' + n + '"]'); return el ? String(el.value || '').trim() : ''; }

  function bind(f) {
    f.removeAttribute('data-netlify');
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      if (val(f, 'bot-field')) return;                         // honeypot: bots fill it, people don't
      var btn = f.querySelector('[type="submit"]');
      var label = btn ? btn.textContent : '';
      if (btn) { btn.disabled = true; btn.textContent = 'Sending…'; }
      var wa = val(f, 'whatsapp');
      var lines = [
        'Service: ' + (val(f, 'service_required') || val(f, 'service') || 'General enquiry'),
        wa && wa !== val(f, 'phone') ? 'WhatsApp: ' + wa : '',
        val(f, 'notes') ? 'Notes: ' + val(f, 'notes') : '',
        'Sent from: ' + location.pathname
      ].filter(Boolean);
      fetch(URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', apikey: KEY, Authorization: 'Bearer ' + KEY, 'x-caller': 'kithcars_simple_form' },
        body: JSON.stringify({
          channel: 'website',
          sender_name: val(f, 'name'),
          sender_phone: wa || val(f, 'phone'),
          reg: val(f, 'registration').toUpperCase().replace(/\s+/g, ''),
          message_text: lines.join('\n')
        })
      }).then(function (r) {
        if (!r.ok) throw new Error('status ' + r.status);
        try { if (window.dataLayer) window.dataLayer.push({ event: 'generate_lead', form: 'quote-request' }); } catch (x) {}
        location.href = f.getAttribute('action') || '/thank-you';
      }).catch(function () {
        if (btn) { btn.disabled = false; btn.textContent = label; }
        alert('Sorry, that did not send. Please call 020 4629 9469 or WhatsApp 07923 688259 and we will sort your quote.');
      });
    });
  }

  function init() { Array.prototype.forEach.call(document.querySelectorAll('form[name="quote-request"]'), bind); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
