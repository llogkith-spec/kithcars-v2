#!/usr/bin/env python3
"""Check every page family's advertised headline price against the price book.

The same bug kept coming back all day in different clothes: a figure lives in several places on
a page — the spec row, the service card, the meta description, the title, the JSON-LD — and a
sweep written for one shape misses the others. Oil and filter said £45 while the widget on the
same page quoted £115; alloys said £65 in the spec row after the cards had been corrected to
£105.

Hunting individual strings will never finish. This instead reads the one headline price each
page family advertises and compares it against the job the quote engine prices for that family.
A family listed in UNPRICED has no engine equivalent, so there is nothing to compare it to —
those are listed at the end so they stay visible rather than silently trusted.

Exit code 1 on any mismatch, so it can gate a deploy.
"""
import math
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

AREAS = ('beddington|carshalton|cheam|coulsdon|croydon|mitcham|morden|norbury|purley|rosehill|'
         'streatham|sutton|thornton-heath|tooting|wallington|wimbledon|worcester-park')

# Page family -> (catalogue job id, band). Band matters: a van service is not a car service.
PRICED = {
    'car-servicing': ('service-interim', 'small'),
    'interim-service': ('service-interim', 'small'),
    'full-service': ('service-full', 'small'),
    'major-service': ('service-major', 'small'),
    'oil-filter-change': ('oil-filter-change', 'small'),
    'van-servicing': ('service-interim', 'van'),
    'fleet-servicing': ('service-interim', 'van'),
    'mot-testing': ('mot', 'small'),
    'brake-repairs': ('brake-pads-front', 'small'),
    'clutch-replacement': ('clutch', 'small'),
    'cambelt-replacement': ('cambelt', 'small'),
    'battery-electrical': ('battery', 'small'),
}
# Brand pages all advertise the interim service.
BRANDS = ('alfa-romeo', 'audi', 'bmw', 'citroen', 'fiat', 'ford', 'honda', 'hyundai', 'jaguar',
          'kia', 'land-rover', 'mazda', 'mercedes', 'mini', 'nissan', 'peugeot', 'renault',
          'seat', 'skoda', 'toyota', 'vauxhall', 'volkswagen', 'volvo')
for b in BRANDS:
    PRICED[f'{b}-garage'] = ('service-interim', 'small')
    PRICED[f'{b}-specialist'] = ('service-interim', 'small')

# Real prices with no engine equivalent. Listed so they are visibly unchecked, not forgotten.
UNPRICED = {
    'accident-repairs', 'adblue-solutions', 'air-filter-replacement', 'cabin-filter-replacement',
    'ac-regas', 'abs-sensor-replacement', 'alternator-replacement', 'bumper-repair',
    'car-respray', 'dpf-cleaning', 'ecu-remap', 'engine-replacement', 'exhaust-repairs',
    'gearbox-services', 'head-gasket-replacement', 'headlight-restoration', 'oil-leak-repair',
    'pre-purchase-inspection', 'smart-repairs', 'suspension-repairs', 'timing-chain-replacement',
    'turbo-replacement', 'tyre-fitting', 'vehicle-hire', 'welding-rust-repair',
    'wheel-alignment', 'wheel-bearings', 'engine-diagnostics', 'scratch-repair',
    'alloy-wheel-refurbishment', 'vehicle-recovery', 'stone-chip-repair', 'dent-removal',
}


SERVICE_LEVELS = {'service-interim': 'interim', 'service-full': 'full',
                  'service-major': 'major', 'oil-filter-change': 'oil-change'}


def engine_price(job_id, band):
    """The figure a page may advertise as its "from".

    Servicing prices off engine size now and lands on pennies, so the advertised figure is the
    cheapest cell on the rate card with standard oil, rounded UP to the pound — never below
    anything the widget can quote. The band argument is ignored for servicing, because the
    cheapest band is the honest "from" whatever size car the page is about."""
    if job_id in SERVICE_LEVELS:
        expr = ("Math.min(...C.servicing.bands.map(b=>E.svcPrice(C,'"
                + SERVICE_LEVELS[job_id] + "',b.id,'standard')))")
    else:
        expr = "E.priceJob(C,'" + job_id + "','" + band + "').low"
    out = subprocess.run(
        ['node', '-e',
         "const E=require('./quote-engine.js'),C=require('./quote-catalogue.json');"
         "console.log(" + expr + ");"],
        cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    return math.ceil(float(out))


def family(name):
    return re.sub(r'-(' + AREAS + r')$', '', name.replace('.html', ''))


def main():
    seen, bad = {}, []
    for p in sorted(ROOT.glob('*.html')):
        m = re.search(r'<div><dt>Price</dt><dd>([^<]+)</dd></div>', p.read_text())
        if not m:
            continue
        seen.setdefault(family(p.name), []).append((p.name, m.group(1).strip()))

    checked = 0
    for fam, rows in sorted(seen.items()):
        if fam not in PRICED:
            continue
        job, band = PRICED[fam]
        want = f'From £{engine_price(job, band)}'
        checked += 1
        for name, shown in rows:
            if shown != want:
                bad.append(f'{name}: shows "{shown}", price book says "{want}"')

    print(f'{checked} page families checked against the price book, '
          f'{sum(len(v) for k, v in seen.items() if k in PRICED)} pages')
    if bad:
        for line in bad[:15]:
            print('  MISMATCH ' + line)
        print(f'\n{len(bad)} pages disagree with the price book')
        return 1

    unknown = sorted(f for f in seen if f not in PRICED and f not in UNPRICED)
    if unknown:
        print('  families with no price-book mapping and not on the unpriced list:')
        for f in unknown:
            print(f'    {f}: {seen[f][0][1]}')
    print('every mapped family matches the price book')
    print(f'({len(UNPRICED)} families priced outside the engine and not checked here)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
