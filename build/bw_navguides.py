#!/usr/bin/env python3
"""Put the guides hub into the bodywork dropdown on every page.

A hub nothing links to is not a hub. The other two bodywork hubs are in this dropdown, so the
third goes beside them, immediately after Insurance Claims. Anything already carrying the link is
skipped so this is safe to run twice.

The generated bodywork pages slice their chrome from bumper-repair-croydon.html at build time, so
that file has to be updated here too or the next build quietly reverts the nav on 96 pages.
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
ANCHOR = '<a href="/car-insurance-claims">Insurance Claims</a>'
LINK = '<a href="/bodywork-guides">Bodywork Guides</a>'


def main():
    changed, skipped, no_nav = 0, 0, 0
    for f in sorted(ROOT.glob('*.html')):
        html = f.read_text()
        if '<html' not in html:
            continue                      # Search Console token files and the like
        if LINK in html:
            skipped += 1
            continue
        if ANCHOR not in html:
            no_nav += 1
            continue
        # Only the dropdown occurrence, which is the first - the footer copy uses other wording.
        f.write_text(html.replace(ANCHOR, ANCHOR + LINK, 1))
        changed += 1

    print(f'nav: {changed} changed, {skipped} already had it, {no_nav} have no bodywork dropdown')

    # Verify the slice source carries it, or the next build undoes this.
    src = ROOT / 'bumper-repair-croydon.html'
    if LINK not in src.read_text():
        print('FAIL: the chrome slice source does not carry the link')
        return 1
    # And that nothing ended up with it twice.
    dupes = [f.name for f in ROOT.glob('*.html') if f.read_text().count(LINK) > 1]
    if dupes:
        print(f'FAIL: duplicated on {len(dupes)} pages: {dupes[:5]}')
        return 1
    print('ok: slice source carries it, no duplicates')
    return 0


if __name__ == '__main__':
    sys.exit(main())
