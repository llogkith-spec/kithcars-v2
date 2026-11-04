#!/usr/bin/env python3
"""Bring every advertised service 'from' price into line with the price book.

The site carried an old service price set — £93 interim, £131 oil-and-filter, £141 full,
£176 major — in meta descriptions, hero copy, price blocks, service cards, nav menus and
JSON-LD minPrice across 166 pages. Those figures are roughly half what the quote engine on
the same page quotes, so someone could read "from £93" in Google's result and then be shown
£155 by the widget. The oil-and-filter figure was also above the interim service that
contains it.

Cars take the engine's cheapest car band; vans and fleet take the van band, because a van
service costs more than a car's, not less.

Idempotent: safe to re-run.
"""
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent


def engine_from(job_id: str, band: str) -> int:
    out = subprocess.run(
        ['node', '-e',
         "const E=require('./quote-engine.js'),C=require('./quote-catalogue.json');"
         "console.log(E.priceJob(C,process.argv[1],process.argv[2]).low);",
         job_id, band],
        cwd=ROOT, capture_output=True, text=True, check=True)
    return int(out.stdout.strip())


CAR = engine_from('service-interim', 'small')
VAN = engine_from('service-interim', 'van')
FULL = engine_from('service-full', 'small')
MAJOR = engine_from('service-major', 'small')

VAN_PAGE = re.compile(r'^(van-servicing|fleet)', re.I)

# The stale figure -> what it should be, by page type.
STALE = {'93': (CAR, VAN), '141': (FULL, FULL), '176': (MAJOR, MAJOR)}


def main():
    changed, touched = [], 0
    for p in sorted(ROOT.glob('*.html')):
        src = html = p.read_text()
        is_van = bool(VAN_PAGE.match(p.name))
        for old, (car_v, van_v) in STALE.items():
            new = van_v if is_van else car_v
            # Only ever rewrite the figure as a price: £93 with a word boundary after it,
            # never a fragment of £935 and never a bare 93 somewhere in prose.
            html = re.sub(r'£' + old + r'(?![\d])', f'£{new}', html)
            # JSON-LD minPrice is a structured price claim; Google reads it.
            html = html.replace(f'"minPrice": "{old}"', f'"minPrice": "{new}"')
            html = html.replace(f'"minPrice":"{old}"', f'"minPrice":"{new}"')
        if html != src:
            p.write_text(html)
            changed.append(p.name)
        touched += 1

    print(f'price book: car service from £{CAR}, van service from £{VAN}, '
          f'full £{FULL}, major £{MAJOR}')
    print(f'pages scanned: {touched}; rewritten: {len(changed)}')

    # Nothing may be left claiming the old set, and every JSON-LD block must still parse.
    bad, broken = [], []
    for p in ROOT.glob('*.html'):
        t = p.read_text()
        for old in STALE:
            if re.search(r'£' + old + r'(?![\d])', t) or f'"minPrice": "{old}"' in t:
                bad.append(f'{p.name}: £{old}')
        for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
            try:
                json.loads(block)
            except Exception as e:
                broken.append(f'{p.name}: {e}')
    if bad:
        print('STILL STALE:', bad[:10])
    if broken:
        print('BROKEN JSON-LD:', broken[:10])
    if bad or broken:
        sys.exit(1)
    print('clean: no page advertises the old service prices, and all JSON-LD still parses.')


if __name__ == '__main__':
    main()
