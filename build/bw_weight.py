#!/usr/bin/env python3
"""Shift the site's internal link weight toward bodywork.

A Google search for "kith cars" returns sitelinks for About Us, Car Servicing Streatham, Car
Servicing in Cheam, Car Servicing in Coulsdon and Full Service Wallington. Not one bodywork page.
Sitelinks are chosen from internal link prominence, and measured across the site the vote is:

    mechanical   31,038 internal links   35.0%
    bodywork     21,730 internal links   24.5%

    nav          14 mechanical items, all of them above the first bodywork one
    homepage     19 mechanical links against 11 bodywork
    pages        437 mechanical against 131 live bodywork

So Google is reading the site correctly. It is a servicing site that also does bodywork, because
that is what the site says about itself.

Three changes, all reversible:

  nav order     Bodywork moves ahead of Mechanical. The strongest single signal on the site,
                because the nav repeats on all 993 pages and order within it carries weight.
  nav depth     The bodywork dropdown gains the two hubs and the repair-process page, taking it
                from 8 items to 11 and putting the hubs on every page of the site.
  homepage      A bodywork block, so the page that carries the most authority spends some of it
                on bodywork rather than 19-to-11 against.

What this does NOT do is reduce mechanical. Nothing is removed - 437 mechanical pages and their
links all stay. The balance shifts because bodywork gains, which is the version of this that
cannot cost existing rankings.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

MECH_NAV = re.compile(
    r'<div class="nav-item-dropdown"><a href="/mechanical" class="nav-parent">Mechanical</a>'
    r'<div class="nav-dropdown-menu">.*?</div></div>', re.S)
BODY_NAV = re.compile(
    r'<div class="nav-item-dropdown"><a href="/bodywork" class="nav-parent">Bodywork</a>'
    r'<div class="nav-dropdown-menu">(.*?)</div></div>', re.S)

# Added to the bodywork dropdown, in front of what is already there.
NEW_ITEMS = ('<a href="/body-panel-repairs">Repair Costs by Panel</a>'
             '<a href="/car-insurance-claims">Insurance Claims</a>'
             '<a href="/bodywork-repair-process">The Repair Process</a>')

HOMEPAGE_BLOCK = (
    '<section class="section section-alt"><div class="container kx-prose">'
    '<h2>Bodywork and accident repair</h2>'
    '<p>Panel work, paint and accident repair from our own bodyshop in Hackbridge. We are on no '
    'insurer&rsquo;s panel, which means you choose who repairs your car &mdash; not them. Prices '
    'below come from the same rate card the quote box uses.</p>'
    '<ul class="kx-hublist">'
    '<li><a href="/body-panel-repairs"><strong>Every panel, and what it costs</strong></a>'
    '<span>Bumpers, wings, doors, quarters, bonnets and roofs, with real prices and what the '
    'repair actually involves.</span></li>'
    '<li><a href="/car-insurance-claims"><strong>Insurance claims, explained</strong></a>'
    '<span>Your right to choose a repairer, excess, write-off categories, courtesy cars and how '
    'a claim actually runs.</span></li>'
    '<li><a href="/bodywork-repair-process"><strong>What actually happens to your car</strong></a>'
    '<span>Ten stages from estimate to collection, and the corners that get cut where you cannot '
    'see them.</span></li>'
    '<li><a href="/accident-repairs"><strong>Accident repair</strong></a>'
    '<span>Any insurer, any car. We deal with the estimate, the engineer and the '
    'supplementary.</span></li>'
    '<li><a href="/car-respray"><strong>Respray and paint</strong></a>'
    '<span>Colour matched to your paint code and blended into the neighbouring panels, which is '
    'what makes a repair invisible.</span></li>'
    '</ul></div></section>')


def main():
    pages = [p for p in sorted(ROOT.glob('*.html')) if '<html' in p.read_text()[:300]]
    reordered = deepened = 0
    skipped = []

    for p in pages:
        t = p.read_text()
        mech = MECH_NAV.search(t)
        body = BODY_NAV.search(t)
        if not mech or not body:
            skipped.append(p.name)
            continue

        changed = False

        # Deepen the bodywork dropdown first, so the reorder moves the finished block.
        if '/body-panel-repairs' not in body.group(1):
            t = (t[:body.start(1)] + NEW_ITEMS + body.group(1) + t[body.end(1):])
            deepened += 1
            changed = True
            body = BODY_NAV.search(t)
            mech = MECH_NAV.search(t)

        # Move bodywork in front of mechanical, but only where it is still behind.
        if body.start() > mech.start():
            mech_html, body_html = mech.group(), body.group()
            t = t.replace(body_html, '', 1).replace(mech_html, body_html + mech_html, 1)
            reordered += 1
            changed = True

        if changed:
            p.write_text(t)

    print(f'nav: bodywork moved ahead of mechanical on {reordered} pages')
    print(f'nav: bodywork dropdown deepened on {deepened} pages')
    if skipped:
        print(f'     skipped {len(skipped)} without the expected nav '
              f'({", ".join(skipped[:3])}{"..." if len(skipped) > 3 else ""})')

    # Homepage block
    home = ROOT / 'index.html'
    ht = home.read_text()
    if 'Bodywork and accident repair</h2>' in ht:
        print('homepage: block already present')
    elif '</main>' in ht:
        home.write_text(ht.replace('</main>', HOMEPAGE_BLOCK + '</main>', 1))
        print('homepage: bodywork block added')
    else:
        print('homepage: no </main>, block NOT added')

    # --- verification ------------------------------------------------------------------------
    bad = []
    BODY_RX = re.compile(r'bumper|dent|scratch|paint|panel|bodywork|accident|respray|alloy|'
                         r'smart-repair|chip|rust|welding|insurance|claim', re.I)
    MECH_RX = re.compile(r'servic|mot|brake|clutch|timing|diagnostic|exhaust|battery|suspension|'
                         r'cambelt|dpf|gearbox|bearing|tyre', re.I)
    b = m = 0
    for p in pages:
        t = p.read_text()
        # kpi.html is the internal dashboard and carries no site chrome at all, so it is
        # correctly skipped above. Only pages that have a nav can have a damaged one.
        has_nav = 'class="site-nav"' in t
        if t.count('<h4>Guides</h4>') > 1 or (has_nav and t.count('</nav>') < 1):
            bad.append(f'{p.name}: nav damaged')
        if t.count('nav-parent">Bodywork') > 1 or t.count('nav-parent">Mechanical') > 1:
            bad.append(f'{p.name}: duplicated nav item')
        if t.count('</body>') != 1:
            bad.append(f'{p.name}: markup damaged')
        for href in re.findall(r'href="/([a-z0-9-]+)"', t):
            if BODY_RX.search(href): b += 1
            elif MECH_RX.search(href): m += 1
    for slug in ('body-panel-repairs', 'car-insurance-claims', 'bodywork-repair-process'):
        if not (ROOT / f'{slug}.html').exists():
            bad.append(f'nav links to /{slug}, which does not exist')

    tot = b + m
    print(f'\nlink balance now: bodywork {b:,} ({b/tot*100:.1f}%)  mechanical {m:,} ({m/tot*100:.1f}%)')

    if bad:
        print(f'\nPROBLEMS ({len(bad)}):')
        for x in bad[:10]:
            print('  ' + x)
        return 1
    print('clean: bodywork leads the nav on every page and the hubs are on all of them')
    return 0


if __name__ == '__main__':
    sys.exit(main())
