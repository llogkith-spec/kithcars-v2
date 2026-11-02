/* Before/after comparison sliders for the bodywork gallery.
   Drag the handle, click anywhere on the image, or use the arrow keys.

   Markup it enhances (works without JS: both images just stack):
     <div class="kc-compare" data-label-before="Before" data-label-after="After">
       <img class="kc-before" src="..." alt="...">
       <img class="kc-after"  src="..." alt="...">
     </div>

   No dependencies, no build step. */
(function () {
  'use strict';

  var clamp = function (n, lo, hi) { return n < lo ? lo : n > hi ? hi : n; };

  function build(el) {
    if (el.dataset.kcReady) return;
    var before = el.querySelector('.kc-before');
    var after = el.querySelector('.kc-after');
    if (!before || !after) return;
    el.dataset.kcReady = '1';

    // The "after" image is clipped from the left; the handle sets how much shows.
    var wrap = document.createElement('div');
    wrap.className = 'kc-clip';
    el.insertBefore(wrap, after);
    wrap.appendChild(after);

    var handle = document.createElement('button');
    handle.type = 'button';
    handle.className = 'kc-handle';
    handle.setAttribute('role', 'slider');
    handle.setAttribute('aria-label', 'Reveal the repaired side');
    handle.setAttribute('aria-valuemin', '0');
    handle.setAttribute('aria-valuemax', '100');
    handle.innerHTML = '<span class="kc-grip" aria-hidden="true"></span>';
    el.appendChild(handle);

    var tagB = document.createElement('span');
    tagB.className = 'kc-tag kc-tag-b';
    tagB.textContent = el.dataset.labelBefore || 'Before';
    var tagA = document.createElement('span');
    tagA.className = 'kc-tag kc-tag-a';
    tagA.textContent = el.dataset.labelAfter || 'After';
    el.appendChild(tagB);
    el.appendChild(tagA);

    // Keep the clipped image the width of the whole card, so the halves stay aligned at any handle
    // position and at any screen size.
    function sizeToCard() { el.style.setProperty('--kc-w', el.getBoundingClientRect().width + 'px'); }
    sizeToCard();
    if ('ResizeObserver' in window) new ResizeObserver(sizeToCard).observe(el);
    else window.addEventListener('resize', sizeToCard);
    // Images can settle after layout; re-measure once each has loaded.
    [before, after].forEach(function (im) {
      if (!im.complete) im.addEventListener('load', sizeToCard, { once: true });
    });

    var pos = Number(el.dataset.start) || 50;
    function set(p, announce) {
      pos = clamp(p, 0, 100);
      wrap.style.width = pos + '%';
      handle.style.left = pos + '%';
      handle.setAttribute('aria-valuenow', Math.round(pos));
      // Hide a label once the handle has covered it, so the two don't overlap.
      tagB.style.opacity = pos > 88 ? '0' : '1';
      tagA.style.opacity = pos < 12 ? '0' : '1';
      if (announce) handle.setAttribute('aria-valuetext', Math.round(pos) + '% repaired');
    }
    set(pos);

    var dragging = false;
    function fromEvent(e) {
      var r = el.getBoundingClientRect();
      var x = (e.touches ? e.touches[0].clientX : e.clientX) - r.left;
      return (x / r.width) * 100;
    }
    function move(e) {
      if (!dragging) return;
      // Stop the page scrolling under a finger that is dragging the handle.
      if (e.cancelable) e.preventDefault();
      set(fromEvent(e), true);
    }
    function stop() { dragging = false; el.classList.remove('kc-dragging'); }

    function start(e) {
      dragging = true;
      el.classList.add('kc-dragging');
      set(fromEvent(e), true);
    }
    el.addEventListener('mousedown', start);
    el.addEventListener('touchstart', start, { passive: true });
    window.addEventListener('mousemove', move);
    window.addEventListener('touchmove', move, { passive: false });
    window.addEventListener('mouseup', stop);
    window.addEventListener('touchend', stop);

    handle.addEventListener('keydown', function (e) {
      var step = e.shiftKey ? 10 : 2;
      if (e.key === 'ArrowLeft') { set(pos - step, true); e.preventDefault(); }
      if (e.key === 'ArrowRight') { set(pos + step, true); e.preventDefault(); }
      if (e.key === 'Home') { set(0, true); e.preventDefault(); }
      if (e.key === 'End') { set(100, true); e.preventDefault(); }
    });

    // A nudge on first view, so it reads as draggable rather than as one odd photo.
    if ('IntersectionObserver' in window && !el.dataset.noHint) {
      var seen = false;
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (!en.isIntersecting || seen) return;
          seen = true; io.disconnect();
          var t0 = null;
          requestAnimationFrame(function hop(ts) {
            if (!t0) t0 = ts;
            var k = (ts - t0) / 900;
            if (k >= 1 || dragging) { if (!dragging) set(50); return; }
            set(50 + Math.sin(k * Math.PI * 2) * 14);
            requestAnimationFrame(hop);
          });
        });
      }, { threshold: 0.4 });
      io.observe(el);
    }
  }

  function filter(group) {
    var bar = group.querySelector('.kc-filter');
    if (!bar) return;
    bar.addEventListener('click', function (e) {
      var b = e.target.closest('[data-filter]');
      if (!b) return;
      var want = b.dataset.filter;
      bar.querySelectorAll('[data-filter]').forEach(function (x) {
        x.classList.toggle('on', x === b);
        x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
      });
      var shown = 0;
      group.querySelectorAll('.kc-item').forEach(function (it) {
        var match = want === 'all' || (it.dataset.type || '').split(' ').indexOf(want) !== -1;
        it.hidden = !match;
        if (match) shown++;
      });
      var empty = group.querySelector('.kc-empty');
      if (empty) empty.hidden = shown > 0;
    });
  }

  function init() {
    document.querySelectorAll('.kc-compare').forEach(build);
    document.querySelectorAll('.kc-gallery').forEach(filter);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
  window.KithCompare = { init: init };
})();
