#!/usr/bin/env python3
"""Remove the old four-step booking form, and give the pages that only had it the real one.

78 pages still carry the previous booking wizard - SERVICE, DETAILS, YOUR INFO, BOOKING - as a
25KB section plus a 14.6KB script that drives it. On 71 of them the current quote widget is on the
same page, so the customer meets two different booking forms, is quoted by whichever they happen
to scroll to, and only one of those is wired to the pricing engine, the Meta events and the slot
calendar. The other seven have only the old one, so deleting it alone would leave them with no way
to book at all.

What happens here:

  71 pages   the old section and its script come out; the current widget already there stays
   7 pages   same removal, and the current widget goes in where the old one was, with the
             stylesheet and scripts it needs if the page was not already loading them

The seven are five mechanical blog posts, the stone-chip page and the bodywork gallery, so the
flow each one opens in is set accordingly rather than defaulting everything to mechanical.

Finding the right block is the whole difficulty, and the obvious way is wrong. Both funnels sit in
a section marked id="get-a-quote" - the id is duplicated on these pages, which is invalid markup
and the reason the in-page "get a quote" link has always jumped to whichever came first. The new
widget is the earlier of the two, so searching for that id finds the funnel we want to keep and
deletes it instead. The anchor here is therefore the old form's own wording, "Choose a service to
get started", with the enclosing section located by balancing <section> tags outward from it. The
block contains nested sections, so matching the first closing tag ends it in the wrong place, and
on a 25KB block that silently eats the rest of the page.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

MARKER = 'Choose a service to get started'

# The seven that need a replacement, and the flow each should open in.
NEEDS_WIDGET = {
    'blog-when-to-change-brake-pads.html': 'mechanical',
    'blog-mot-failure-common-reasons.html': 'mechanical',
    'blog-timing-chain-rattle-causes.html': 'mechanical',
    'blog-dpf-warning-light-what-to-do.html': 'mechanical',
    'blog-car-servicing-interval-guide.html': 'mechanical',
    'stone-chip-repair.html': 'bodywork',
    'bodywork-gallery.html': 'bodywork',
}

WIDGET = ('<section class="section section-alt" id="get-a-quote"><div class="container">'
          '<div style="text-align:center;margin-bottom:2rem">'
          '<span class="section-label">Instant quote</span>'
          '<h2>Get a price for your car</h2>'
          '<p class="lead" style="margin-top:.75rem;margin-inline:auto">Put your registration in '
          'and we will price the job. Or call <a href="tel:02046299469">020 4629 9469</a>.</p></div>'
          '<div id="kq" data-flow="{flow}"><div class="kq-loading">'
          '<span class="kq-spin"></span>Loading instant quote&hellip;</div></div>'
          '</div></section>')

ASSETS_CSS = '<link rel="stylesheet" href="/quote.css"/>'
ASSETS_JS = '<script src="/quote-engine.js" defer></script><script src="/quote.js" defer></script>'


def section_end(t, start):
    """End index of the <section> opening at `start`, balancing nested sections."""
    depth, i = 0, start
    while True:
        nxt_open = t.find('<section', i + 1)
        nxt_close = t.find('</section>', i + 1)
        if nxt_close == -1:
            return -1
        if nxt_open != -1 and nxt_open < nxt_close:
            depth += 1
            i = nxt_open
        else:
            if depth == 0:
                return nxt_close + len('</section>')
            depth -= 1
            i = nxt_close


def old_funnel_span(t):
    """(start, end) of the old form: the outermost section wrapping its marker text, plus the
    wizard script if that directly follows. (-1, -1) if the marker is not enclosed by a section."""
    mk = t.find(MARKER)
    if mk == -1:
        return -1, -1
    found = None
    for m in re.finditer(r'<section[^>]*>', t):
        e = section_end(t, m.start())
        if e != -1 and m.start() < mk < e and (found is None or m.start() < found[0]):
            found = (m.start(), e)
    if found is None:
        return -1, -1
    start, end = found

    s = t.find('<script', end)
    if s != -1 and s <= end + 40:              # must follow immediately, not pages later
        e = t.find('</script>', s)
        if e != -1 and 'booking-wizard' in t[s:e]:
            end = e + len('</script>')
    return start, end


def main():
    pages = [p for p in sorted(ROOT.glob('*.html')) if MARKER in p.read_text()]
    print(f'pages carrying the old funnel: {len(pages)}')

    stripped = replaced = assets = 0
    freed = 0
    failures = []
    doubled = set()

    for p in pages:
        t = p.read_text()
        start, end = old_funnel_span(t)
        if start == -1:
            failures.append(f'{p.name}: could not locate the old form')
            continue
        freed += end - start

        if p.name in NEEDS_WIDGET:
            t = t[:start] + WIDGET.format(flow=NEEDS_WIDGET[p.name]) + t[end:]
            replaced += 1
            if 'quote.css' not in t:
                t = t.replace('</head>', ASSETS_CSS + ASSETS_JS + '</head>', 1)
                assets += 1
            elif 'quote.js' not in t:
                t = t.replace('</head>', ASSETS_JS + '</head>', 1)
                assets += 1
        else:
            t = t[:start] + t[end:]
            stripped += 1

        # Five of the blog pages end with a doubled </html>. It predates this change and browsers
        # ignore it, but it is the kind of thing a validator flags, so it goes while we are here.
        while t.rstrip().endswith('</html>\n</html>') or t.rstrip().endswith('</html></html>'):
            t = t.rstrip()[: t.rstrip().rfind('</html>')].rstrip() + '\n'
            doubled.add(p.name)

        p.write_text(t)

    print(f'  old form removed        : {stripped + replaced}')
    print(f'  replaced with the widget: {replaced}')
    print(f'  assets added            : {assets}')
    print(f'  markup removed          : {freed / 1048576:.1f} MB across the site')
    print(f'  stray </html> fixed     : {len(doubled)}')

    # --- verification ------------------------------------------------------------------------
    # Nothing may still carry the old wizard, every page that had it must still offer a way to
    # book, the id must no longer be duplicated, and the markup must not have been truncated by a
    # mis-balanced tag.
    bad = []
    for p in pages:
        t = p.read_text()
        if MARKER in t or 'booking-wizard' in t:
            bad.append(f'{p.name}: old form still present')
        if 'id="kq"' not in t:
            bad.append(f'{p.name}: no booking route left')
        if t.count('id="get-a-quote"') != 1:
            bad.append(f'{p.name}: get-a-quote appears {t.count(chr(34).join(["id=", "get-a-quote", ""]))} times')
        if t.count('</body>') != 1 or t.count('</html>') != 1:
            bad.append(f'{p.name}: markup truncated')
        if 'quote.js' not in t or 'quote.css' not in t:
            bad.append(f'{p.name}: widget present but its code is not loaded')
        for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
            import json
            try:
                json.loads(m.group(1))
            except Exception as exc:
                bad.append(f'{p.name}: JSON-LD broken ({exc})')

    if failures:
        print('\nCOULD NOT PROCESS:')
        for x in failures:
            print('  ' + x)
    if bad:
        print(f'\nPROBLEMS ({len(bad)}):')
        for x in bad[:12]:
            print('  ' + x)
    if failures or bad:
        return 1

    print(f'\nclean: {len(pages)} pages now carry one booking form, and it is the one wired to the')
    print('       pricing engine, the Meta events and the slot calendar')
    return 0


if __name__ == '__main__':
    sys.exit(main())
