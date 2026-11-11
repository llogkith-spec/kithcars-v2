#!/usr/bin/env python3
"""Load Inter on every page instead of Barlow, so the whole site is set in one typeface.

The homepage loads Inter. The other 923 pages load Barlow, Barlow Condensed and JetBrains Mono,
and kith.css set headings in condensed Barlow - which is why the site read as two different
businesses depending on which page you landed on.

kith.css now asks for Inter (see its header), but asking is not enough: a page that never
downloads Inter falls through the stack to system-ui, so without this the inner pages would
silently render in Helvetica or Segoe UI and still not match. This swaps the Google Fonts request
itself, to exactly the one the homepage makes.

Three faces go and one arrives, so these pages also make one font request instead of three and
fetch noticeably less before first paint.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

# What the homepage asks for, character for character.
INTER = ('https://fonts.googleapis.com/css2?family=Inter:'
         'wght@400;500;600;700;800;900&amp;display=swap')

# Any Google Fonts stylesheet request that is not already the one above.
LINK = re.compile(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com/css2\?[^"]*"\s*/?>')


def main():
    changed = already = 0
    pages = sorted(ROOT.glob('*.html'))

    for p in pages:
        t = p.read_text()
        links = LINK.findall(t)
        if not links:
            continue
        if all(INTER in l for l in links):
            already += 1
            continue
        # Replace the first, drop any others: three separate requests collapse to one.
        t = LINK.sub(lambda m, c=iter(range(99)): (
            f'<link rel="stylesheet" href="{INTER}"/>' if next(c) == 0 else ''), t)
        p.write_text(t)
        changed += 1

    print(f'pages switched to Inter : {changed}')
    print(f'already on Inter        : {already}')

    # --- verification ----------------------------------------------------------------------
    # No page may still ask for a face we no longer use, every page that requests fonts must
    # request exactly one stylesheet, and it must be the homepage's.
    bad = []
    for p in pages:
        t = p.read_text()
        # google*.html is Search Console's verification token: one line of text that happens to
        # carry a .html extension. It is not a document and has no head to check.
        if '<html' not in t:
            continue
        for face in ('Barlow', 'JetBrains'):
            if face in t:
                bad.append(f'{p.name}: still asks for {face}')
        links = LINK.findall(t)
        if len(links) > 1:
            bad.append(f'{p.name}: {len(links)} font stylesheets, expected 1')
        if links and INTER not in links[0]:
            bad.append(f'{p.name}: font request is not the homepage\'s')
        if t.count('</head>') != 1:
            bad.append(f'{p.name}: markup damaged')

    if bad:
        print(f'\nPROBLEMS ({len(bad)}):')
        for x in bad[:12]:
            print('  ' + x)
        return 1

    with_fonts = sum(1 for p in pages if LINK.search(p.read_text()))
    print(f'\nclean: {with_fonts} pages, one typeface, one font request each')
    return 0


if __name__ == '__main__':
    sys.exit(main())
