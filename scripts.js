/* ============================================
   MOBILE NAV
   ============================================ */
const navToggle = document.querySelector('.nav-toggle');
const siteNav   = document.querySelector('.site-nav');

if (navToggle && siteNav) {
  navToggle.addEventListener('click', () => {
    const isOpen = siteNav.classList.toggle('is-open');
    navToggle.setAttribute('aria-expanded', isOpen);
  });

  siteNav.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      siteNav.classList.remove('is-open');
      navToggle.setAttribute('aria-expanded', 'false');
    });
  });

  document.addEventListener('click', e => {
    if (!siteNav.contains(e.target) && !navToggle.contains(e.target)) {
      siteNav.classList.remove('is-open');
      navToggle.setAttribute('aria-expanded', 'false');
    }
  });
}

/* ============================================
   SCROLL REVEAL
   ============================================ */
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('is-visible');
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 });

document.querySelectorAll('[data-reveal]').forEach(el => {
  revealObserver.observe(el);
});

/* ============================================
   HERO BOOKING WIZARD
   ============================================ */
(function () {
  const wizard = document.getElementById('hero-wizard');
  if (!wizard) return;

  /* ── Service lists per category ── */
  const SERVICES = {
    mechanical: [
      'Full Service', 'Interim Service', 'Oil & Filter Change',
      'MOT Test', 'Brake Inspection & Repair', 'Tyre Supply & Fitting',
      'Timing Chain / Timing Belt', 'Suspension Work', 'Clutch Replacement',
      'Engine Diagnostics', 'Wheel Alignment', 'Exhaust Repair', 'Other Mechanical',
    ],
    bodywork: [
      'Scratch Repair', 'Dent Removal (PDR)', 'Panel Repair',
      'Bumper Repair & Replacement', 'Full Respray', 'Partial Respray',
      'Paint Correction', 'Windscreen Repair', 'Other Bodywork',
    ],
    fleet: [
      'Fleet Servicing Contract', 'Priority Maintenance Plan',
      'Multi-Vehicle Booking', 'Fleet MOT', 'Tyre Management', 'Other Fleet Enquiry',
    ],
    recovery: [
      'Vehicle Recovery', 'Courtesy Car Hire', 'Short-Term Vehicle Hire',
      'Other Recovery / Hire Enquiry',
    ],
  };

  const GC_BOOKING_URL = 'https://calendar.app.google/gGozwbiFEm5xxNvCA';

  /* ── State ── */
  let step       = 1;
  let selCat     = null;
  let selService = null;

  /* ── Panel map ── */
  const panels = {
    1: document.getElementById('hw-panel-1'),
    2: document.getElementById('hw-panel-2'),
    3: document.getElementById('hw-panel-3'),
    4: document.getElementById('hw-panel-4'),
    5: document.getElementById('hw-panel-5'),
    success: document.getElementById('hw-success'),
  };
  const dots  = wizard.querySelectorAll('.hw-dot');
  const lines = wizard.querySelectorAll('.hw-line');

  /* ── Helpers ── */
  function showPanel(n) {
    Object.values(panels).forEach(p => { if (p) p.classList.add('hw-panel--hidden'); });
    const target = (n === 'success') ? panels.success : panels[n];
    if (target) target.classList.remove('hw-panel--hidden');
    step = (n === 'success') ? 6 : n;
    updateDots();
    wizard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  function updateDots() {
    dots.forEach((dot, i) => {
      const n = i + 1;
      dot.classList.remove('hw-dot--active', 'hw-dot--done');
      if (n < step)       dot.classList.add('hw-dot--done');
      else if (n === step) dot.classList.add('hw-dot--active');
    });
    lines.forEach((ln, i) => {
      ln.classList.toggle('hw-line--done', i + 1 < step);
    });
  }

  function markErr(el) { if (el) el.classList.add('field-error'); }

  wizard.querySelectorAll('input, textarea').forEach(el => {
    el.addEventListener('input', () => el.classList.remove('field-error'));
  });

  /* ── STEP 1: Next ── */
  document.getElementById('hw-next-1').addEventListener('click', () => {
    const reg   = document.getElementById('hw-reg');
    const phone = document.getElementById('hw-phone-1');
    let ok = true;
    if (!reg.value.trim())   { markErr(reg);   ok = false; }
    if (!phone.value.trim()) { markErr(phone); ok = false; }
    if (!ok) return;
    /* Pre-fill phone in step 4 */
    document.getElementById('hw-phone-4').value = phone.value.trim();
    showPanel(2);
  });

  /* ── STEP 2: Category cards ── */
  wizard.querySelectorAll('.hw-cat-card').forEach(card => {
    card.addEventListener('click', () => {
      selCat = card.dataset.cat;
      selService = null;

      /* Title */
      const titles = { mechanical: 'Mechanical Services', bodywork: 'Bodywork Services', fleet: 'Fleet Services', recovery: 'Recovery & Hire' };
      document.getElementById('hw-svc-title').textContent = titles[selCat] || 'Choose a service';

      /* Bodywork note */
      document.getElementById('hw-bodywork-note').style.display = (selCat === 'bodywork') ? '' : 'none';

      /* Build service pills */
      const grid = document.getElementById('hw-svc-grid');
      grid.innerHTML = '';
      (SERVICES[selCat] || []).forEach(svc => {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'hw-svc-pill';
        btn.textContent = svc;
        btn.addEventListener('click', () => {
          grid.querySelectorAll('.hw-svc-pill').forEach(p => p.classList.remove('hw-svc-pill--selected'));
          btn.classList.add('hw-svc-pill--selected');
          selService = svc;
          document.getElementById('hw-next-3').disabled = false;
        });
        grid.appendChild(btn);
      });

      document.getElementById('hw-next-3').disabled = true;
      setTimeout(() => showPanel(3), 150);
    });
  });

  document.getElementById('hw-back-2').addEventListener('click', () => showPanel(1));

  /* ── STEP 3: Back / Next ── */
  document.getElementById('hw-back-3').addEventListener('click', () => showPanel(2));
  document.getElementById('hw-next-3').addEventListener('click', () => {
    if (!selService) return;
    /* Show/hide photo upload for bodywork */
    document.getElementById('hw-photos-wrap').style.display = (selCat === 'bodywork') ? '' : 'none';
    showPanel(4);
  });

  /* ── STEP 4: Back / Next ── */
  document.getElementById('hw-back-4').addEventListener('click', () => showPanel(3));
  document.getElementById('hw-next-4').addEventListener('click', () => {
    const name  = document.getElementById('hw-name');
    const phone = document.getElementById('hw-phone-4');
    const email = document.getElementById('hw-email');
    let ok = true;
    if (!name.value.trim())  { markErr(name);  ok = false; }
    if (!phone.value.trim()) { markErr(phone); ok = false; }
    if (!email.value.trim()) { markErr(email); ok = false; }
    if (!ok) return;

    /* Populate Step 5 summary */
    const catLabel = { mechanical:'Mechanical', bodywork:'Bodywork', fleet:'Fleet', recovery:'Recovery & Hire' }[selCat] || selCat;
    document.getElementById('hw-sum-reg').textContent     = document.getElementById('hw-reg').value.trim().toUpperCase();
    document.getElementById('hw-sum-svc').textContent     = `${catLabel} — ${selService}`;
    document.getElementById('hw-sum-name').textContent    = name.value.trim();
    document.getElementById('hw-sum-contact').textContent = `${phone.value.trim()} · ${email.value.trim()}`;

    showPanel(5);
  });

  /* Photo text update */
  const hwPhotos   = document.getElementById('hw-photos');
  const hwPhotoTxt = document.getElementById('hw-photo-text');
  if (hwPhotos && hwPhotoTxt) {
    hwPhotos.addEventListener('change', () => {
      const n = hwPhotos.files.length;
      hwPhotoTxt.textContent = n > 0 ? `${n} photo${n > 1 ? 's' : ''} selected` : 'Click to upload or drag & drop';
    });
  }

  /* ── STEP 5: Back ── */
  document.getElementById('hw-back-5').addEventListener('click', () => showPanel(4));

  /* ── SUBMIT: send email details + open Google Calendar ── */
  document.getElementById('hw-submit').addEventListener('click', async () => {
    const btnText = document.getElementById('hw-submit-text');
    const errEl   = document.getElementById('hw-error');
    if (errEl) errEl.style.display = 'none';
    btnText.textContent = 'Sending…';
    document.getElementById('hw-submit').disabled = true;

    const name     = document.getElementById('hw-name').value.trim();
    const phone    = document.getElementById('hw-phone-4').value.trim();
    const email    = document.getElementById('hw-email').value.trim();
    const reg      = document.getElementById('hw-reg').value.trim();
    const notes    = document.getElementById('hw-notes').value.trim();
    const catLabel = { mechanical:'Mechanical', bodywork:'Bodywork', fleet:'Fleet', recovery:'Recovery & Hire' }[selCat] || selCat;

    const fd = new FormData();
    fd.append('access_key', 'db31da4b-5331-453a-9b9c-d6fb1fbbd264');
    fd.append('from_name',  'KITHCARS');
    fd.append('redirect',   'false');
    fd.append('replyto',    email);
    fd.append('cc',         email);
    fd.append('subject',    `Booking Request — ${catLabel}: ${selService} — KITHCARS`);
    fd.append('Vehicle Registration', reg);
    fd.append('Category',   catLabel);
    fd.append('Service',    selService);
    fd.append('Name',       name);
    fd.append('Phone',      phone);
    fd.append('Email',      email);
    if (notes) fd.append('Notes', notes);
    if (hwPhotos && hwPhotos.files.length > 0) {
      for (const file of hwPhotos.files) fd.append('attachment', file);
    }

    try {
      const res  = await fetch('https://api.web3forms.com/submit', { method:'POST', body: fd });
      const json = await res.json();
      if (json.success) {
        /* Open Google Calendar booking page */
        window.open(GC_BOOKING_URL, '_blank', 'noopener,noreferrer');

        /* Build WhatsApp link */
        const waMsg = encodeURIComponent(
          `Hi KITHCARS, I've just submitted a booking request:\nReg: ${reg}\nService: ${catLabel} — ${selService}\nName: ${name}`
        );
        document.getElementById('hw-wa-link').href = `https://wa.me/447923688259?text=${waMsg}`;
        showPanel('success');
      } else {
        throw new Error(json.message || 'Failed');
      }
    } catch (err) {
      console.error('Hero wizard submit error:', err);
      btnText.textContent = 'Confirm & Book Slot';
      document.getElementById('hw-submit').disabled = false;
      if (errEl) errEl.style.display = 'flex';
    }
  });

})();

/* ============================================
   BOOKING WIZARD
   ============================================ */
(function () {
  const wizard = document.getElementById('booking-wizard');
  if (!wizard) return;

  /* ---- State ---- */
  let currentStep  = 1;
  let selectedSvc  = null;
  let selectedDate = null; // Date object
  let selectedTime = null; // string e.g. "9:00am"
  let tyreQty      = null;

  /* Calendar state */
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  let calYear  = today.getFullYear();
  let calMonth = today.getMonth();

  /* ---- Element references ---- */
  const panels = {
    1: document.getElementById('bw-panel-1'),
    2: document.getElementById('bw-panel-2'),
    3: document.getElementById('bw-panel-3'),
    4: document.getElementById('bw-panel-4'),
    success: document.getElementById('bw-success'),
  };
  const steps = wizard.querySelectorAll('.bw-step');
  const connectors = wizard.querySelectorAll('.bw-connector');

  /* ---- Helpers ---- */
  function showPanel(num) {
    Object.values(panels).forEach(p => {
      if (p) p.classList.add('bw-panel--hidden');
    });
    const target = panels[num] || panels.success;
    if (target) target.classList.remove('bw-panel--hidden');
    currentStep = (num === 'success') ? 5 : num;
    updateProgress();
    wizard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  function updateProgress() {
    steps.forEach((step, i) => {
      const n = i + 1;
      step.classList.remove('bw-step--active', 'bw-step--done');
      if (n < currentStep)      step.classList.add('bw-step--done');
      else if (n === currentStep) step.classList.add('bw-step--active');
    });
    connectors.forEach((c, i) => {
      c.classList.toggle('bw-connector--done', i + 1 < currentStep);
    });
  }

  function showError(msg) {
    const el = document.getElementById('bw-error');
    if (!el) return;
    el.style.display = 'flex';
    el.querySelector('svg + *') || (el.innerHTML += '');
    el.lastChild.textContent = msg || 'Something went wrong. Please call 020 4629 9469.';
  }

  function markError(el) {
    if (el) el.classList.add('field-error');
  }
  function clearErrors() {
    wizard.querySelectorAll('.field-error').forEach(e => e.classList.remove('field-error'));
  }

  /* ---- STEP 1: Service type cards ---- */
  wizard.querySelectorAll('.svc-type-card').forEach(card => {
    card.addEventListener('click', () => {
      wizard.querySelectorAll('.svc-type-card').forEach(c => c.classList.remove('svc-type-card--selected'));
      card.classList.add('svc-type-card--selected');
      selectedSvc = card.dataset.svc;

      /* Show the right detail panel in step 2 */
      wizard.querySelectorAll('.svc-detail').forEach(d => d.style.display = 'none');
      const detail = document.getElementById('svc-detail-' + selectedSvc);
      if (detail) detail.style.display = '';

      setTimeout(() => showPanel(2), 180);
    });
  });

  /* ---- STEP 2: Back / Next ---- */
  document.getElementById('bw-back-2').addEventListener('click', () => showPanel(1));

  document.getElementById('bw-next-2').addEventListener('click', () => {
    clearErrors();
    if (!validateStep2()) return;
    showPanel(3);
  });

  function validateStep2() {
    let ok = true;
    if (selectedSvc === 'repairs') {
      const reg   = document.getElementById('r-reg');
      const issue = document.getElementById('r-issue');
      if (!reg.value.trim())   { markError(reg);   ok = false; }
      if (!issue.value.trim()) { markError(issue);  ok = false; }
    }
    if (selectedSvc === 'servicing') {
      const reg     = document.getElementById('s-reg');
      const checked = wizard.querySelector('input[name="svc-type"]:checked');
      if (!reg.value.trim()) { markError(reg); ok = false; }
      if (!checked) {
        wizard.querySelectorAll('.svc-option-card .svc-option-inner').forEach(el => el.classList.add('field-error'));
        ok = false;
      }
    }
    if (selectedSvc === 'tyres') {
      const reg  = document.getElementById('t-reg');
      const size = document.getElementById('t-size');
      if (!size.value.trim()) { markError(size); ok = false; }
      if (!reg.value.trim())  { markError(reg);  ok = false; }
      if (!tyreQty) {
        document.getElementById('tyre-qty-group').classList.add('field-error');
        ok = false;
      }
    }
    if (selectedSvc === 'mot') {
      const reg = document.getElementById('m-reg');
      if (!reg.value.trim()) { markError(reg); ok = false; }
    }
    if (selectedSvc === 'bodywork') {
      const reg = document.getElementById('bw-reg');
      if (!reg.value.trim()) { markError(reg); ok = false; }
    }
    return ok;
  }

  /* ---- STEP 3: Back / Next ---- */
  document.getElementById('bw-back-3').addEventListener('click', () => showPanel(2));

  document.getElementById('bw-next-3').addEventListener('click', () => {
    clearErrors();
    const name  = document.getElementById('c-name');
    const phone = document.getElementById('c-phone');
    const email = document.getElementById('c-email');
    let ok = true;
    if (!name.value.trim())  { markError(name);  ok = false; }
    if (!phone.value.trim()) { markError(phone); ok = false; }
    if (!email.value.trim()) { markError(email); ok = false; }
    if (!ok) return;
    showPanel(4);
    renderCalendar();
  });

  /* ---- STEP 4: Back ---- */
  document.getElementById('bw-back-4').addEventListener('click', () => showPanel(3));

  /* ---- Tyre quantity buttons ---- */
  document.querySelectorAll('.qty-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.qty-btn').forEach(b => b.classList.remove('qty-btn--selected'));
      btn.classList.add('qty-btn--selected');
      tyreQty = btn.dataset.qty;
      document.getElementById('tyre-qty-group').classList.remove('field-error');
    });
  });

  /* ---- MOT add-service toggle ---- */
  const motToggle = document.getElementById('mot-add-svc');
  if (motToggle) {
    motToggle.addEventListener('change', () => {
      const wrap = document.getElementById('mot-svc-options');
      if (wrap) wrap.style.display = motToggle.checked ? '' : 'none';
    });
  }

  /* ---- Bodywork file input ---- */
  const bwPhotos   = document.getElementById('bw-photos');
  const bwFileText = document.getElementById('bw-file-text');
  if (bwPhotos && bwFileText) {
    bwPhotos.addEventListener('change', () => {
      const n = bwPhotos.files.length;
      bwFileText.textContent = n > 0 ? `${n} photo${n > 1 ? 's' : ''} selected` : 'Click to upload or drag & drop';
    });
  }

  /* ---- Clear field-error on input ---- */
  wizard.querySelectorAll('input, textarea, select').forEach(el => {
    el.addEventListener('input', () => el.classList.remove('field-error'));
  });

  /* ============ CALENDAR ============ */
  const MONTH_NAMES = ['January','February','March','April','May','June','July','August','September','October','November','December'];

  function renderCalendar() {
    const label = document.getElementById('cal-month-label');
    const grid  = document.getElementById('cal-grid');
    if (!label || !grid) return;

    label.textContent = `${MONTH_NAMES[calMonth]} ${calYear}`;
    grid.innerHTML = '';

    const firstDay = new Date(calYear, calMonth, 1);
    const daysInMonth = new Date(calYear, calMonth + 1, 0).getDate();
    let startDow = firstDay.getDay(); // 0=Sun
    startDow = startDow === 0 ? 6 : startDow - 1; // shift to Mon=0

    /* Empty cells before first day */
    for (let i = 0; i < startDow; i++) {
      const cell = document.createElement('button');
      cell.type = 'button';
      cell.className = 'cal-day cal-day--empty';
      cell.setAttribute('aria-hidden', 'true');
      grid.appendChild(cell);
    }

    for (let d = 1; d <= daysInMonth; d++) {
      const date = new Date(calYear, calMonth, d);
      const dow  = date.getDay(); // 0=Sun
      const isPast   = date < today;
      const isSunday = dow === 0;
      const isToday  = date.getTime() === today.getTime();
      const isSelected = selectedDate && date.getTime() === selectedDate.getTime();

      const cell = document.createElement('button');
      cell.type = 'button';
      cell.textContent = d;

      const classes = ['cal-day'];
      if (isSunday)    classes.push('cal-day--sunday');
      else if (isPast) classes.push('cal-day--past');
      else             classes.push('cal-day--available');
      if (isToday)     classes.push('cal-day--today');
      if (isSelected)  classes.push('cal-day--selected');

      cell.className = classes.join(' ');

      if (!isPast && !isSunday) {
        cell.addEventListener('click', () => {
          selectedDate = date;
          selectedTime = null;
          renderCalendar();
          renderTimeSlots(date);
        });
      } else {
        cell.disabled = true;
      }
      grid.appendChild(cell);
    }
  }

  function renderTimeSlots(date) {
    const wrap  = document.getElementById('time-slots-wrap');
    const grid  = document.getElementById('time-slots-grid');
    const lbl   = document.getElementById('cal-selected-label');
    if (!wrap || !grid || !lbl) return;

    const dow = date.getDay(); // 0=Sun,6=Sat
    const isSat = dow === 6;

    const slots = isSat
      ? ['9:00am','10:00am','11:00am','12:00pm','1:00pm','2:00pm']
      : ['8:00am','9:00am','10:00am','11:00am','12:00pm','1:00pm','2:00pm','3:00pm','4:00pm'];

    lbl.textContent = date.toLocaleDateString('en-GB', { weekday: 'long', day: 'numeric', month: 'long' });
    grid.innerHTML = '';

    slots.forEach(slot => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.textContent = slot;
      btn.className = 'time-slot' + (selectedTime === slot ? ' time-slot--selected' : '');
      btn.addEventListener('click', () => {
        selectedTime = slot;
        grid.querySelectorAll('.time-slot').forEach(b => b.classList.remove('time-slot--selected'));
        btn.classList.add('time-slot--selected');
        document.getElementById('bw-submit').disabled = false;
      });
      grid.appendChild(btn);
    });

    wrap.style.display = '';
    document.getElementById('bw-submit').disabled = !(selectedDate && selectedTime);
  }

  /* Calendar prev / next */
  document.getElementById('cal-prev').addEventListener('click', () => {
    calMonth--;
    if (calMonth < 0) { calMonth = 11; calYear--; }
    renderCalendar();
  });
  document.getElementById('cal-next').addEventListener('click', () => {
    calMonth++;
    if (calMonth > 11) { calMonth = 0; calYear++; }
    renderCalendar();
  });

  /* ============ SUBMIT ============ */
  document.getElementById('bw-submit').addEventListener('click', async () => {
    if (!selectedDate || !selectedTime) return;

    const btnText = document.getElementById('bw-submit-text');
    const errEl   = document.getElementById('bw-error');
    if (errEl) errEl.style.display = 'none';

    btnText.textContent = 'Sending…';
    document.getElementById('bw-submit').disabled = true;

    /* Build form data */
    const fd = new FormData();
    fd.append('access_key', 'db31da4b-5331-453a-9b9c-d6fb1fbbd264');
    fd.append('from_name',  'KITHCARS');
    fd.append('redirect',   'false');

    const svcLabel = {
      repairs:   'Repairs',
      servicing: 'Servicing',
      tyres:     'Tyres',
      mot:       'MOT',
      bodywork:  'Bodywork',
    }[selectedSvc] || selectedSvc;

    const cEmail = document.getElementById('c-email').value.trim();
    fd.append('replyto',  cEmail);
    fd.append('cc',       cEmail);
    fd.append('subject', `Booking Request Received — ${svcLabel} — KITHCARS`);
    fd.append('Service Type', svcLabel);

    /* Service-specific fields */
    if (selectedSvc === 'repairs') {
      fd.append('Vehicle Registration', document.getElementById('r-reg').value.trim());
      const make = document.getElementById('r-make').value.trim();
      if (make) fd.append('Make & Model', make);
      fd.append('Fault Description', document.getElementById('r-issue').value.trim());
    }
    if (selectedSvc === 'servicing') {
      const type = wizard.querySelector('input[name="svc-type"]:checked');
      fd.append('Service Package', type ? type.value : '');
      fd.append('Vehicle Registration', document.getElementById('s-reg').value.trim());
      const make = document.getElementById('s-make').value.trim();
      if (make) fd.append('Make & Model', make);
    }
    if (selectedSvc === 'tyres') {
      fd.append('Tyre Size',         document.getElementById('t-size').value.trim());
      fd.append('Brand Preference',  document.getElementById('t-brand').value);
      fd.append('Quantity',          tyreQty || '');
      fd.append('Vehicle Registration', document.getElementById('t-reg').value.trim());
    }
    if (selectedSvc === 'mot') {
      fd.append('Vehicle Registration', document.getElementById('m-reg').value.trim());
      if (motToggle && motToggle.checked) {
        const addSvc = wizard.querySelector('input[name="mot-svc-type"]:checked');
        fd.append('Add-On Service', addSvc ? addSvc.value : 'Yes (not specified)');
      }
    }
    if (selectedSvc === 'bodywork') {
      fd.append('Fault Description', document.getElementById('bw-desc').value.trim());
      fd.append('Vehicle Registration', document.getElementById('bw-reg').value.trim());
      if (bwPhotos && bwPhotos.files.length > 0) {
        for (const file of bwPhotos.files) {
          fd.append('attachment', file);
        }
      }
    }

    /* Contact details */
    fd.append('Name',     document.getElementById('c-name').value.trim());
    fd.append('Phone',    document.getElementById('c-phone').value.trim());
    fd.append('Email',    document.getElementById('c-email').value.trim());
    const postcode = document.getElementById('c-postcode').value.trim();
    if (postcode) fd.append('Postcode', postcode);

    /* Preferred slot */
    const dateStr = selectedDate.toLocaleDateString('en-GB', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' });
    fd.append('Preferred Date', dateStr);
    fd.append('Preferred Time', selectedTime);

    try {
      const res  = await fetch('https://api.web3forms.com/submit', { method: 'POST', body: fd });
      const json = await res.json();
      if (json.success) {
        showPanel('success');
      } else {
        throw new Error(json.message || 'Failed');
      }
    } catch (err) {
      console.error('Booking submit error:', err);
      btnText.textContent = 'Confirm Booking Request';
      document.getElementById('bw-submit').disabled = false;
      if (errEl) errEl.style.display = 'flex';
    }
  });

})();
