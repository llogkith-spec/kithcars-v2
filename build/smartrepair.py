#!/usr/bin/env python3
"""Bring the SMART repair pages onto the engine's figure.

They advertised "From £300" while the quote widget on the same page priced the cheapest SMART
repair on a painted panel at £140 — someone reading the page and then using the widget got two
answers more than twice apart. Logan's call: the engine is right.

Scoped to the smart-repairs pages only. £300 also appears on the bumper-repair pages, and that
is a separate price he has not said to move, so it is reported at the end rather than swept up.
"""
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

NEW = int(subprocess.run(
    ['node', '-e',
     "const E=require('./quote-engine.js'),C=require('./quote-catalogue.json');"
     "console.log(Math.min(...Object.keys(C.body_panels_ex_vat).filter(p=>p!=='trim')"
     ".map(p=>E.bodyLine(C,p,p,'smart','small').low)));"],
    cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip())

SCOPE = re.compile(r'^smart-repairs', re.I)

SUBS = [
    (re.compile(r'<div><dt>Price</dt><dd>From £300</dd></div>'),
     f'<div><dt>Price</dt><dd>From £{NEW}</dd></div>'),
    (re.compile(r'<div><b>From £300</b><span>'), f'<div><b>From £{NEW}</b><span>'),
    (re.compile(r'(SMART [Rr]epairs?[^<]{0,30}</span><span class="kh-svc-meta">From )£300'),
     rf'\g<1>£{NEW}'),
    (re.compile(r'SMART repair from £300'), f'SMART repair from £{NEW}'),
    (re.compile(r'SMART repairs from £300'), f'SMART repairs from £{NEW}'),
    (re.compile(r'A single bumper corner starts from £300'),
     f'A single bumper corner starts from £{NEW}'),
    (re.compile(r'(?<=<title>)([^<]{0,80}?)£300(?![\d.])'), rf'\g<1>£{NEW}'),
    (re.compile(r'"minPrice": "300"'), f'"minPrice": "{NEW}"'),
    (re.compile(r'from £300(?![\d.])'), f'from £{NEW}'),
    (re.compile(r'From £300(?![\d.])'), f'From £{NEW}'),
]


def main():
    pages = sorted(p for p in ROOT.glob('*.html') if SCOPE.match(p.name))
    print(f"cheapest SMART repair on a painted panel, per the price book: £{NEW}")
    print(f'smart-repairs pages: {len(pages)}')

    changed = 0
    for p in pages:
        t = s = p.read_text()
        for pat, rep in SUBS:
            t = pat.sub(rep, t)
        if t != s:
            p.write_text(t)
            changed += 1
    print(f'rewritten: {changed}')

    # Cross-link cards pointing at SMART repairs from elsewhere carry the same claim.
    card = re.compile(r'(SMART Repairs[^<]*</span><span class="kh-svc-meta">From )£300')
    elsewhere = 0
    for p in ROOT.glob('*.html'):
        t = s = p.read_text()
        t, n = card.subn(rf'\g<1>£{NEW}', t)
        if n:
            p.write_text(t)
            elsewhere += n
    print(f'cross-link cards corrected: {elsewhere}')

    stale, broken = [], []
    for p in ROOT.glob('*.html'):
        t = p.read_text()
        if SCOPE.match(p.name) and re.search(r'£300(?![\d.])', t):
            stale.append(p.name)
        for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
            try:
                json.loads(b)
            except Exception as e:
                broken.append(f'{p.name}: {e}')
    if stale:
        print('STILL £300 on smart pages:', stale[:5])
    if broken:
        print('BROKEN JSON-LD:', broken[:4])
    if stale or broken:
        sys.exit(1)
    print(f'clean: SMART repairs now advertise £{NEW}, matching the widget.')

    # Not touched, deliberately.
    bumper = sorted({p.name for p in ROOT.glob('bumper-repair*.html')
                     if re.search(r'£300(?![\d.])', p.read_text())})
    if bumper:
        print(f'\nNOT CHANGED: {len(bumper)} bumper-repair pages still say £300. The engine\'s')
        print("cheapest bumper repair is £140 too, but Logan has not said to move that one.")


if __name__ == '__main__':
    main()
