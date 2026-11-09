#!/usr/bin/env python3
"""Add the Meta pixel's <noscript> fallback to every page.

The pixel itself lives in analytics.js, where it can hang off the events the quote widget already
raises - a price shown, details submitted, a slot booked - which is the half worth having. But
Meta's snippet also carries a plain <img> for visitors with JavaScript turned off, and that cannot
come from a script by definition. It has to be in the markup.

It is worth very little on its own: a visitor without JavaScript cannot use the quote widget, so
they will never reach a conversion. It costs one tag, it is what Meta's own snippet asks for, and
without it the page view from those visitors is simply lost. So it goes in.

Idempotent - it will not add a second copy to a page that already has one.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PIXEL_ID = '1431276708362160'

TAG = ('<noscript><img height="1" width="1" style="display:none" alt="" '
       'src="https://www.facebook.com/tr?id=' + PIXEL_ID + '&amp;ev=PageView&amp;noscript=1"></noscript>')


def main():
    pages = sorted(ROOT.glob('*.html'))
    added = skipped = nobody = 0

    for p in pages:
        t = p.read_text()
        if PIXEL_ID in t:
            skipped += 1
            continue
        if '</body>' not in t:
            nobody += 1
            continue
        # Last thing before </body>: it renders nothing, so it cannot disturb the layout, and it
        # is out of the way of anything that measures the document while loading.
        p.write_text(t.replace('</body>', '  ' + TAG + '\n</body>', 1))
        added += 1

    print(f'pages:        {len(pages)}')
    print(f'  added:      {added}')
    print(f'  already in: {skipped}')
    print(f'  no </body>: {nobody}')

    # Every page must end up with exactly one, and the ampersands must be escaped - a bare & in
    # an attribute is an HTML parse error that some validators and crawlers will trip on.
    bad = []
    for p in pages:
        t = p.read_text()
        n = t.count('facebook.com/tr?id=')
        if '</body>' in t and n != 1:
            bad.append(f'{p.name}: {n} copies')
        if 'tr?id=' in t and re.search(r'tr\?id=\d+&(?!amp;)', t):
            bad.append(f'{p.name}: unescaped & in the pixel url')
    if bad:
        print(f'\nPROBLEMS ({len(bad)}):')
        for x in bad[:8]:
            print('  ' + x)
        return 1
    print('\nclean: one escaped noscript pixel on every page that has a body')
    return 0


if __name__ == '__main__':
    sys.exit(main())
