#!/usr/bin/env python3
"""Rewrite the recovery and collection price sentences from the price book.

These figures were spelled out in prose on 54 pages and in their JSON-LD answers, so a rate-card
change left them behind. Worse, a blanket find-and-replace of the old £108 lifted only the first
number in each list, leaving "£144 up to 3 miles, £132 up to 5 miles" — a price list that goes
down before it goes up.

Rebuild the whole sentence from quote-catalogue.json instead of patching numbers inside it.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CAT = json.loads((ROOT / 'quote-catalogue.json').read_text())
R = CAT['recovery']


def band_phrase(bands, lead='up to'):
    """'£144 up to 3 miles, £192 up to 5 miles and £264 up to 10 miles'."""
    parts = [f"£{b['price']} {lead} {b['max']} miles" for b in bands]
    return ', '.join(parts[:-1]) + ' and ' + parts[-1]


TRUCK = band_phrase(R['recovery_bands_inc_vat'])
DRIVE = band_phrase(R['pickup_bands_inc_vat'])
MAX = R['max_miles']

# Each pattern spans the whole claim, so nothing stale can survive inside it.
RULES = [
    (re.compile(r'it is £\d+ up to 3 miles,.*?up to 10 miles\.', re.S),
     f'it is {TRUCK}.'),
    (re.compile(r'on the truck, £\d+ up to three miles,.*?up to ten, VAT included\.', re.S),
     f'on the truck, {TRUCK}, VAT included.'),
    (re.compile(r'the same distances are £\d+, £\d+, £\d+ and £\d+\.', re.S),
     f'it is {DRIVE}.'),
    (re.compile(r'those bands are £\d+, £\d+, £\d+ and £\d+\.', re.S),
     f'those bands are {DRIVE}.'),
]


def main():
    changed = 0
    for p in sorted(ROOT.glob('*.html')):
        t = s = p.read_text()
        for pat, rep in RULES:
            t = pat.sub(rep, t)
        if t != s:
            p.write_text(t)
            changed += 1

    print(f'truck:      {TRUCK}')
    print(f'driven back: {DRIVE}')
    print(f'pages rewritten: {changed}')

    # Nothing may still quote a figure that is not on the current rate card, and the JSON-LD
    # these sentences sit inside must still parse.
    live = {str(b['price']) for b in R['recovery_bands_inc_vat']} | \
           {str(b['price']) for b in R['pickup_bands_inc_vat']}
    stale, broken = [], []
    for p in ROOT.glob('*.html'):
        t = p.read_text()
        for m in re.finditer(r'£(\d+) up to \d+ miles|£(\d+) up to (?:three|five|seven|ten)', t):
            n = m.group(1) or m.group(2)
            if n not in live:
                stale.append(f'{p.name}: £{n}')
        for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
            try:
                json.loads(block)
            except Exception as e:
                broken.append(f'{p.name}: {e}')
    if stale:
        print('STALE FIGURES:', sorted(set(stale))[:8])
    if broken:
        print('BROKEN JSON-LD:', broken[:5])
    if stale or broken:
        sys.exit(1)
    print('clean: every quoted recovery figure is on the current rate card, JSON-LD all valid.')


if __name__ == '__main__':
    main()
