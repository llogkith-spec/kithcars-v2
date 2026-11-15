#!/usr/bin/env python3
"""Give the new guide pages a way in from the rest of the site.

Without this they are orphans. A search engine can reach them from the sitemap and a reader can
reach them from a search result, but nothing on kithcars.com links down to them, so they get none
of the site's existing authority and nobody browsing the bodywork pages ever finds them.

Two changes, both small and both site-wide:

  footer     a "Guides" column beside Mechanical, Bodywork and Contact, on all 975 pages. Three
             links - the two hubs and the repair-process page - so every page on the site is two
             clicks from any guide.
  bodywork   a block on bodywork.html and accident-repairs.html pointing at the hubs, because
             those are the pages someone lands on when they are actually thinking about this.

The footer column is inserted after the Bodywork column by matching its closing markup rather
than by position, so it does not depend on the footer's exact shape staying the same.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

ANCHOR = ('<a href="/alloy-wheel-refurbishment">Alloy Wheels</a></nav></div>')

COLUMN = ('<div class="footer-col"><h4>Guides</h4><nav class="footer-links">'
          '<a href="/car-insurance-claims">Insurance Claims</a>'
          '<a href="/body-panel-repairs">Panel Repair Costs</a>'
          '<a href="/bodywork-repair-process">The Repair Process</a>'
          '</nav></div>')

PROMO = (
    '<section class="section section-alt"><div class="container kx-prose">'
    '<h2>Before you ring your insurer</h2>'
    '<p>Most single-panel damage costs less than your excess, and a claim follows you for about '
    'five years. We have written out everything we get asked - what you are entitled to, what it '
    'costs, and the one thing most people do not know, which is that you choose the repairer '
    'rather than your insurer.</p>'
    '<ul class="kx-hublist">'
    '<li><a href="/car-insurance-claims"><strong>Car insurance claims, explained</strong></a>'
    '<span>Your right to choose a repairer, excess, write-off categories, courtesy cars and how '
    'a claim actually runs.</span></li>'
    '<li><a href="/body-panel-repairs"><strong>Every panel, and what it costs</strong></a>'
    '<span>Real prices from the same rate card the quote box uses, panel by panel and damage by '
    'damage.</span></li>'
    '<li><a href="/bodywork-repair-process"><strong>What actually happens to your car</strong></a>'
    '<span>Ten stages from estimate to collection, and the corners that get cut where you cannot '
    'see them.</span></li>'
    '</ul></div></section>'
)

PROMO_AFTER = '</main>'


def main():
    # ---- footer column, every page ---------------------------------------------------------
    touched = skipped = 0
    for p in sorted(ROOT.glob('*.html')):
        t = p.read_text()
        if '<html' not in t:                      # the Search Console token file
            continue
        if 'href="/car-insurance-claims"' in t and '<h4>Guides</h4>' in t:
            skipped += 1
            continue
        if ANCHOR not in t:
            skipped += 1
            continue
        t = t.replace(ANCHOR, ANCHOR + COLUMN, 1)
        p.write_text(t)
        touched += 1
    print(f'footer column added : {touched}')
    print(f'  skipped           : {skipped} (already had it, or no bodywork column)')

    # ---- promo block on the two bodywork landing pages -------------------------------------
    promoted = []
    for name in ('bodywork.html', 'accident-repairs.html'):
        f = ROOT / name
        if not f.exists():
            continue
        t = f.read_text()
        if 'Before you ring your insurer' in t:
            continue
        if PROMO_AFTER not in t:
            continue
        t = t.replace(PROMO_AFTER, PROMO + PROMO_AFTER, 1)
        f.write_text(t)
        promoted.append(name)
    print(f'guide block added   : {", ".join(promoted) if promoted else "none"}')

    # ---- verification ----------------------------------------------------------------------
    bad = []
    pages = [p for p in ROOT.glob('*.html') if '<html' in p.read_text()[:200]]
    for p in pages:
        t = p.read_text()
        if t.count('<h4>Guides</h4>') > 1:
            bad.append(f'{p.name}: Guides column added twice')
        # kpi.html is the internal dashboard and carries no site chrome at all - no header, no
        # footer. It is correctly skipped above, so only check the footer where there is one.
        if t.count('<footer') != t.count('</footer>'):
            bad.append(f'{p.name}: footer damaged')
        if t.count('</body>') != 1:
            bad.append(f'{p.name}: markup damaged')
    # the three targets must exist
    for slug in ('car-insurance-claims', 'body-panel-repairs', 'bodywork-repair-process'):
        if not (ROOT / f'{slug}.html').exists():
            bad.append(f'footer links to /{slug}, which does not exist')

    with_col = sum(1 for p in pages if '<h4>Guides</h4>' in p.read_text())
    print(f'pages now linking in: {with_col} of {len(pages)}')

    if bad:
        print(f'\nPROBLEMS ({len(bad)}):')
        for x in bad[:10]:
            print('  ' + x)
        return 1
    print('\nclean: every guide is reachable from the footer of every page')
    return 0


if __name__ == '__main__':
    sys.exit(main())
