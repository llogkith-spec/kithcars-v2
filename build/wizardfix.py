#!/usr/bin/env python3
"""Reconcile the booking wizard with the price book, and give it the registration lookup.

The wizard (the Book Your Visit flow, .svc-option-grid) predates the quote engine and carries its
own hard-coded service prices. They were both internally wrong — the oil-and-filter-only job was
priced above the interim service that contains it — and roughly half what the quote engine on the
same page quotes, so a customer could read "from £93" and then be quoted £180.

This rewrites those prices from quote-catalogue.json, so there is one price book and not two,
drops the oil-and-filter option (no real price for it yet; the interim service already includes
an oil and filter change), aligns the inspection-point counts with the catalogue, and adds
reglookup.js so the wizard's registration fields check the car against DVLA/DVSA.

Idempotent: safe to re-run.
"""
import json
import math
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CAT = json.loads((ROOT / 'quote-catalogue.json').read_text())


def from_price(job_id: str) -> int:
    """Cheapest band the engine will quote for this job — the only honest 'from'."""
    out = subprocess.run(
        ['node', '-e', '''
const E=require('./quote-engine.js'),C=require('./quote-catalogue.json');
let min=1e9;
for(const b of Object.keys(C.bands)){const r=E.priceJob(C,process.argv[1],b);if(r.low<min)min=r.low;}
console.log(min);''', job_id],
        cwd=ROOT, capture_output=True, text=True, check=True)
    return math.ceil(float(out.stdout.strip()))


PRICES = {
    'Interim Service': from_price('service-interim'),
    'Full Service': from_price('service-full'),
    'Major Service': from_price('service-major'),
}

CHECKS = {j['id']: j.get('check', '') for j in CAT['jobs']}

# Descriptions, so the wizard says the same thing as the comparison table and the quote engine.
BLURB = {
    'Interim Service': f"Every 6 months — oil, filter &amp; {CHECKS['service-interim']} check",
    'Full Service': f"Comprehensive annual — {CHECKS['service-full']} inspection",
    'Major Service': 'Full service + spark plugs, belts &amp; more',
}

# The whole <label> for the oil-and-filter card, in both grids.
OIL_CARD = re.compile(
    r'\s*<label class="svc-option-card">\s*'
    r'<input type="radio" name="(?:svc-type|mot-svc-type)" value="Oil &amp; Filter Service"[^>]*/>\s*'
    r'<span class="svc-option-inner">.*?</span>\s*</label>',
    re.S)

SCRIPT_TAG = '<script src="/reglookup.js" defer></script>'
ANCHOR = '<script src="/quote.js" defer></script>'


def fix_card(html: str, label: str) -> str:
    """Rewrite the price and the blurb inside one option card."""
    pat = re.compile(
        r'(<input type="radio" name="svc-type" value="' + re.escape(label) + r'"[^>]*/>\s*'
        r'<span class="svc-option-inner">\s*<strong>[^<]*</strong>\s*<span>)'
        r'([^<]*)'
        r'(</span>\s*<span class="svc-from">from £)(\d+)(</span>)', re.S)

    def sub(m):
        return m.group(1) + BLURB[label] + m.group(3) + str(PRICES[label]) + m.group(5)

    return pat.sub(sub, html)


def main():
    pages = sorted(p for p in ROOT.glob('*.html') if 'svc-option-grid' in p.read_text())
    changed = []
    for p in pages:
        src = html = p.read_text()
        html = OIL_CARD.sub('', html)
        for label in PRICES:
            html = fix_card(html, label)
        # The MOT add-on cards carry blurbs but no prices; keep their wording in step.
        html = html.replace('<strong>Interim Service</strong><span>Oil, filter &amp; 30-point check</span>',
                            f"<strong>Interim Service</strong><span>Oil, filter &amp; {CHECKS['service-interim']} check</span>")
        html = html.replace('<strong>Full Service</strong><span>60-point annual inspection</span>',
                            f"<strong>Full Service</strong><span>{CHECKS['service-full']} annual inspection</span>")
        if SCRIPT_TAG not in html and ANCHOR in html:
            html = html.replace(ANCHOR, ANCHOR + '\n' + SCRIPT_TAG, 1)
        if html != src:
            p.write_text(html)
            changed.append(p.name)

    print(f'from-prices taken from the price book: '
          f'{", ".join(f"{k} £{v}" for k, v in PRICES.items())}')
    print(f'pages with the wizard: {len(pages)}; rewritten: {len(changed)}')

    # Nothing should be left claiming the old figures or the removed option.
    stale = []
    for p in pages:
        t = p.read_text()
        for bad in ('from £93', 'from £131', 'from £141', 'from £176', 'Oil &amp; Filter Service'):
            if bad in t:
                stale.append(f'{p.name}: {bad}')
    if stale:
        print('STILL STALE:')
        for s in stale[:20]:
            print('  ' + s)
        sys.exit(1)
    print('clean: no page carries the old service prices or the oil-and-filter option.')
    missing = [p.name for p in pages if SCRIPT_TAG not in p.read_text()]
    print('reglookup.js present on all wizard pages'
          if not missing else f'MISSING reglookup.js on {len(missing)}: {missing[:5]}')


if __name__ == '__main__':
    main()
