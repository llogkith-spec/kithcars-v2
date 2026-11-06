#!/usr/bin/env python3
"""Move every advertised service price onto the new engine-size rate card.

Servicing used to price off body size (small/medium/large/prestige/van) with figures derived
from a labour-hours model. It now prices off engine capacity using Logan's own BookMyGarage cost
inputs, and the headline figures have moved in both directions:

    interim   £155 -> £182     full    £230 -> £210
    major     £305 -> £249     oil     £115 -> £163
    van       £215 -> £182     (vans now price by engine size like everything else)

Two of those went down and two went up, so this is not a sweep that can be waved through: a page
left behind now either undersells the job or overcharges on paper against a widget that quotes
something else.

The from-price is the cheapest cell on the rate card with standard oil, rounded UP to the pound,
so the advertised figure is never below anything the widget can quote.
"""
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

LEVELS = {'service-interim': 'interim', 'service-full': 'full',
          'service-major': 'major', 'oil-filter-change': 'oil-change'}


def cheapest(level):
    out = subprocess.run(
        ['node', '-e',
         "const E=require('./quote-engine.js'),C=require('./quote-catalogue.json');"
         "console.log(Math.min(...C.servicing.bands.map(b=>"
         "E.svcPrice(C,process.argv[1],b.id,'standard'))));", level],
        cwd=ROOT, capture_output=True, text=True, check=True)
    import math
    return math.ceil(float(out.stdout.strip()))


NEW = {job: cheapest(level) for job, level in LEVELS.items()}
INTERIM, FULL, MAJOR, OIL = (NEW['service-interim'], NEW['service-full'],
                             NEW['service-major'], NEW['oil-filter-change'])

# Old advertised figure -> new one. Vans fold into the car price because they are now banded by
# engine size like everything else.
MOVES = [(155, INTERIM), (215, INTERIM), (230, FULL), (305, MAJOR), (115, OIL)]

# Only rewrite a figure where it is unambiguously a service price. £155 and £115 in particular
# could mean something else elsewhere on a 936-page site, and guessing is what broke the
# recovery prose last time.
SHAPES = [
    r'<div><dt>Price</dt><dd>From £{old}</dd></div>',
    r'<span class="kh-svc-meta">From £{old} &middot;',
    r'(?<=[Ss]ervic)(?:e|ing)([^.<]{{0,40}}?)from £{old}(?![\d])',
    r'(?<![\d])From £{old} \| KITH Cars',
    r'"minPrice": "{old}"',
    r'<li>Interim from £{old}</li>',
    # The hero price badge, which carries the figure a third time.
    r'<div><b>From £{old}</b><span>',
    # Nav list entries and area-page prose, which carry it a fourth and fifth time.
    r'<li>From £{old} &middot;',
    r'(?<=change)([^.<]{{0,60}}?)from £{old}(?![\d])',
    r'(?<=service)([^.<]{{0,60}}?)from £{old}(?![\d])',
    # Loose prose on the area pages: "work here starts from £155", "from £305 is the
    # starting point". Only on pages this script already scopes to servicing.
    r'starts from £{old}(?![\d])',
    r'from £{old} is the starting point',
    r'workshop, from £{old}(?![\d])',
    # Titles and the FAQ answers that quote the figure back at the reader. Google shows
    # the title, and the FAQ sits inside JSON-LD, so both have to move together.
    r'(?<=<title>)([^<]{{0,80}}?)£{old}(?![\d])',
    r'the from £{old} actually include',
    r'From £{old} covers',
    # The pricing page's own list, where the service name sits next to the figure.
    r'(?<=<span>)(Interim Service|Full Service|Major Service|Oil [&a-z; ]*Filter[^<]*)</span><span>from £{old}',
    r'and from £{old} we can put that right',
    r'Services from £{old}',
]


def main():
    print('new advertised from-prices (cheapest band, standard oil, rounded up):')
    print(f'  interim £{INTERIM} · full £{FULL} · major £{MAJOR} · oil and filter £{OIL}')

    # Which pages are allowed to carry which figure, so a £155 clutch part never gets rewritten.
    service_page = re.compile(
        r'^(car-servicing|interim-service|full-service|major-service|oil-filter-change|'
        r'van-servicing|fleet-servicing|fleet|[a-z-]+-(garage|specialist)|pricing|mechanical|index)',
        re.I)

    changed, hits = 0, {}
    for p in sorted(ROOT.glob('*.html')):
        if not service_page.match(p.name):
            continue
        t = s = p.read_text()
        for old, new in MOVES:
            for shape in SHAPES:
                pat = shape.format(old=old)
                t, n = re.subn(pat, lambda m: m.group(0).replace(f'£{old}', f'£{new}')
                                                      .replace(f'"{old}"', f'"{new}"'), t)
                if n:
                    hits[f'£{old} -> £{new}'] = hits.get(f'£{old} -> £{new}', 0) + n
        if t != s:
            p.write_text(t)
            changed += 1

    print(f'pages rewritten: {changed}')
    for k, v in sorted(hits.items()):
        print(f'  x{v:<5} {k}')

    broken = []
    for p in ROOT.glob('*.html'):
        for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', p.read_text(), re.S):
            try:
                json.loads(b)
            except Exception as e:
                broken.append(f'{p.name}: {e}')
    if broken:
        print('BROKEN JSON-LD:', broken[:5])
        sys.exit(1)
    print('JSON-LD still valid everywhere')


if __name__ == '__main__':
    main()
