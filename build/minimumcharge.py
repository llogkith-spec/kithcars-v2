#!/usr/bin/env python3
"""Present £60 as the minimum charge it is, not as a from-price.

Logan's answer: "£60 is my minimum charge." That is a different claim from "scratch repair from
£60". A from-price advertises a job somebody actually buys at that price; a minimum charge is the
floor below which a job is not worth booking, and the work itself starts higher — the engine's
cheapest scratch on a painted panel is £140.

Advertising the floor as though it were the price is the thing that gets a garage into trouble
with the CPRs and, more immediately, generates calls from people expecting £60 and leaving
disappointed. So the pages now say both numbers and what each one means.

Scratch and stone-chip pages only. The £60 figures in the recovery prose are the collection
bands and are correct.
"""
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

REAL = int(subprocess.run(
    ['node', '-e',
     "const E=require('./quote-engine.js'),C=require('./quote-catalogue.json');"
     "console.log(Math.min(...Object.keys(C.body_panels_ex_vat).filter(p=>p!=='trim')"
     ".map(p=>E.bodyLine(C,p,p,'smart','small').low)));"],
    cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip())

# Only pages about the work £60 is the floor for.
SCOPE = re.compile(r'^(scratch-repair|stone-chip-repair|smart-repairs)', re.I)

SUBS = [
    ('<div><dt>Price</dt><dd>From £60</dd></div>',
     f'<div><dt>Price</dt><dd>£60 minimum &middot; most from £{REAL}</dd></div>'),
    ('<div><b>From £60</b><span>Written quote first</span></div>',
     f'<div><b>From £{REAL}</b><span>£60 minimum charge</span></div>'),
    ('<span class="kh-svc-meta">From £60 &middot;',
     f'<span class="kh-svc-meta">From £{REAL} &middot;'),
]

# Meta descriptions and prose: "from £60" becomes the real figure, because that is what the
# reader is being quoted.
PROSE = re.compile(r'from £60(?![\d])')


def main():
    pages = [p for p in sorted(ROOT.glob('*.html')) if SCOPE.match(p.name)]
    print(f'cheapest scratch on a painted panel, per the price book: £{REAL}')
    print(f'pages in scope: {len(pages)}')

    changed = 0
    for p in pages:
        t = s = p.read_text()
        for old, new in SUBS:
            t = t.replace(old, new)
        t = PROSE.sub(f'from £{REAL}', t)
        if t != s:
            p.write_text(t)
            changed += 1
    print(f'rewritten: {changed}')

    # The service cards that point AT these pages from elsewhere carry the same claim.
    card = re.compile(r'((?:Scratch Repair|Stone Chip Repair|SMART Repairs)[^<]*</span>'
                      r'<span class="kh-svc-meta">From )£60')
    elsewhere = 0
    for p in ROOT.glob('*.html'):
        t = s = p.read_text()
        t, n = card.subn(rf'\g<1>£{REAL}', t)
        if n:
            p.write_text(t)
            elsewhere += n
    print(f'cross-link cards corrected: {elsewhere}')

    stale, broken = [], []
    for p in ROOT.glob('*.html'):
        t = p.read_text()
        if card.search(t) or (SCOPE.match(p.name) and PROSE.search(t)):
            stale.append(p.name)
        for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
            try:
                json.loads(b)
            except Exception as e:
                broken.append(f'{p.name}: {e}')
    if stale:
        print('STILL CLAIMING "from £60":', stale[:6])
    if broken:
        print('BROKEN JSON-LD:', broken[:4])
    if stale or broken:
        sys.exit(1)
    print(f'clean: £60 now reads as a minimum, with £{REAL} as the price.')


if __name__ == '__main__':
    main()
