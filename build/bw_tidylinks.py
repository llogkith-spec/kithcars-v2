#!/usr/bin/env python3
"""Normalise relative .html links to the absolute pretty URLs the rest of the site uses.

Eleven pages - about-us, faq, blog and the blog posts - link to "mechanical.html" where every
other page links to "/mechanical". Netlify serves the site at pretty URLs, so those two are
different addresses for the same page, and a crawler that finds both splits the signals between
them instead of pooling them on one.

It also meant these pages were invisible to the nav rebalance, which matches on the absolute
form, so they kept a mechanical-first nav while the other 982 pages moved.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
LINK = re.compile(r'href="(?!https?://|/|#|mailto:|tel:)([a-z0-9][a-z0-9-]*)\.html(#[a-z0-9-]*)?"', re.I)


def main():
    changed, total = 0, 0
    for p in sorted(ROOT.glob('*.html')):
        t = p.read_text()
        if '<html' not in t[:300]:
            continue
        n = len(LINK.findall(t))
        if not n:
            continue
        new = LINK.sub(lambda m: 'href="/%s%s"' % (m.group(1), m.group(2) or ''), t)
        p.write_text(new)
        changed += 1
        total += n
        print(f'  {p.name:44} {n} links')

    print(f'\npages fixed: {changed}, links rewritten: {total}')

    bad = []
    for p in ROOT.glob('*.html'):
        t = p.read_text()
        if '<html' not in t[:300]:
            continue
        left = LINK.findall(t)
        if left:
            bad.append(f'{p.name}: {len(left)} relative links remain')
        if t.count('</body>') != 1:
            bad.append(f'{p.name}: markup damaged')
    if bad:
        print('\nPROBLEMS:')
        for x in bad[:10]:
            print('  ' + x)
        return 1
    print('clean: every internal link on the site is now the absolute pretty URL')
    return 0


if __name__ == '__main__':
    sys.exit(main())
