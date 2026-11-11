#!/usr/bin/env python3
"""Load the house style on the four customer pages that were missing it.

kith.css is the layer that carries the house palette, the typeface and the header sizing. 929
pages load it. about-us, blog, faq and thank-you never did - they load styles.css and nothing
else - so they were a third variant: the same red accent and Inter as everywhere else, because
those now come from styles.css and the font link, but none of the header work. The "Get a Quote"
button was still running off the right edge of the window on all three of the public ones, and
the nav still did not collapse on a tablet.

index.html is left alone on purpose: it is the design everything else is being matched to, and it
has its own stylesheet. kpi.html is an internal dashboard with no customer-facing chrome.

Their stylesheet was also linked as "styles.css" rather than "/styles.css". That resolves
correctly from /about-us but not from /about-us/, so a visitor arriving with a trailing slash got
an unstyled page. Made absolute while here.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

TARGETS = ['about-us.html', 'blog.html', 'faq.html', 'thank-you.html']
THEME = '<link rel="stylesheet" href="/kith.css"/>'


def main():
    added = absolute = 0
    missing = []

    for name in TARGETS:
        p = ROOT / name
        if not p.exists():
            missing.append(name)
            continue
        t = p.read_text()

        # styles.css -> /styles.css, however the link is spaced or self-closed
        new = re.sub(r'(<link rel="stylesheet" href=")styles\.css(")', r'\1/styles.css\2', t)
        if new != t:
            absolute += 1
            t = new

        # kith.css loads last of the stylesheets, which is what makes it able to restyle the rest
        if 'kith.css' not in t:
            t = t.replace('</head>', THEME + '</head>', 1)
            added += 1

        p.write_text(t)

    print(f'house style added   : {added}')
    print(f'paths made absolute : {absolute}')
    if missing:
        print(f'not found           : {", ".join(missing)}')

    # --- verification --------------------------------------------------------------------
    bad = list(f'{n}: file not found' for n in missing)
    for name in TARGETS:
        p = ROOT / name
        if not p.exists():
            continue
        t = p.read_text()
        if 'kith.css' not in t:
            bad.append(f'{name}: house style still missing')
        if re.search(r'href="styles\.css"', t):
            bad.append(f'{name}: stylesheet still linked relatively')
        if t.count('</head>') != 1 or t.count('</html>') != 1:
            bad.append(f'{name}: markup damaged')
        # kith.css must come after styles.css or it cannot restyle it
        if t.index('kith.css') < t.index('/styles.css'):
            bad.append(f'{name}: house style loads before the base stylesheet')

    if bad:
        print(f'\nPROBLEMS ({len(bad)}):')
        for x in bad:
            print('  ' + x)
        return 1

    print('\nclean: every customer-facing page now loads the same house style')
    return 0


if __name__ == '__main__':
    sys.exit(main())
