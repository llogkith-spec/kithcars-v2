#!/usr/bin/env python3
"""Remove the self-reported 4.9/193 star rating from the pages.

Google does not use a rating a business publishes about itself. In structured data it is worse
than useless: aggregateRating on your own LocalBusiness markup, sourced from nothing a crawler
can verify, is self-serving review content and is what manual actions get issued for. The real
reviews are on the Business Profile and show there regardless of what the site claims.

Four things go:

  aggregateRating   the JSON-LD block, on 1,059 pages. This is the one that matters.
  trust row         "4.9/5 from 193 Google reviews" in the hero
  footer link       the numbers in the Google Maps link, keeping the link itself
  stat tile         the "4.9 / 193 Google reviews" tile in the stats strip
  section lead      "Rated 4.9 on Google - 193+ reviews" above the testimonials

What stays is the individual customer testimonials with names against them. Those are quoted
reviews rather than a rating we have awarded ourselves, they are what the section is for, and
removing them was not asked for. The route to the real reviews stays too - the Maps link is kept
and reworded, so anyone who wants the rating can see the actual one.

A hardcoded "193" was going to drift anyway. There is no version of this that stays true without
somebody editing a thousand pages every time a review lands.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

HTML_FIXES = [
    # Hero trust row item - drop it; the other items in the row stand on their own.
    (r'<li>★★★★★ 4\.9/5 from 193 Google reviews</li>', ''),
    # Footer Google link - keep the link, drop the self-reported figures.
    (r'<span>★★★★★ 4\.9 from 193 reviews · View on Google Maps</span>',
     '<span>Read our reviews on Google Maps</span>'),
    # Stats tile.
    (r'<div><b>4\.9★</b><span>193 Google reviews</span></div>', ''),
    # Lead line above the testimonials.
    (r'Rated 4\.9 &#9733; on Google &mdash; 193\+ reviews',
     'What customers have said about us'),
    (r'Rated 4\.9 ★ on Google &mdash; 193\+ reviews',
     'What customers have said about us'),
]


def strip_rating(html):
    """Drop aggregateRating from every JSON-LD node that carries one."""
    def one(m):
        try:
            d = json.loads(m.group(1))
        except Exception:
            return m.group(0)
        changed = False
        for node in d.get('@graph', [d]):
            if isinstance(node, dict) and node.pop('aggregateRating', None) is not None:
                changed = True
        if not changed:
            return m.group(0)
        return ('<script type="application/ld+json">'
                + json.dumps(d, ensure_ascii=False) + '</script>')
    return re.sub(r'<script type="application/ld\+json">(.*?)</script>', one, html, flags=re.S)


def main():
    schema_pages = html_pages = 0
    counts = {p: 0 for p, _ in HTML_FIXES}
    for f in sorted(ROOT.glob('*.html')):
        html = original = f.read_text()
        if '<html' not in html:
            continue
        before = html
        for pat, rep in HTML_FIXES:
            html, n = re.subn(pat, rep, html)
            counts[pat] += n
        if html != before:
            html_pages += 1
        after = strip_rating(html)
        if after != html:
            schema_pages += 1
        html = after
        if html != original:
            f.write_text(html)

    print(f'aggregateRating removed from {schema_pages} pages')
    print(f'visible rating text changed on {html_pages} pages')
    for p, n in counts.items():
        print(f'  {n:5}  {p[:62]}')

    # --- verify ------------------------------------------------------------------------------
    bad = []
    for f in sorted(ROOT.glob('*.html')):
        html = f.read_text()
        if '<html' not in html:
            continue
        if 'aggregateRating' in html:
            bad.append(f'{f.name}: aggregateRating still present')
        for m in re.finditer(r'.{0,60}(4\.9|193\s*(\+)?\s*(Google\s*)?review).{0,60}', html):
            s = m.group(0)
            if 'path d' in s or 'svg' in s or re.search(r'4\.9\d{2,}', s):
                continue        # SVG path data, not a rating
            bad.append(f'{f.name}: {re.sub(chr(92)+"s+", " ", s).strip()[:110]}')
        for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
            try:
                json.loads(m.group(1))
            except Exception as e:
                bad.append(f'{f.name}: JSON-LD broken ({e})')

    print(f'\nremaining rating references: {len(bad)}')
    for b in bad[:10]:
        print('  ' + b)
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
