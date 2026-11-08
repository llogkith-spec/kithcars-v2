#!/usr/bin/env python3
"""Check that what each service PROMISES matches what it is PRICED for.

A customer read the full service's list back to Logan over WhatsApp and it included a cabin
filter. The rate card prices the pollen filter into the major only, so the website was selling a
part that was neither fitted nor paid for — and the customer was right, because the website said
so.

The cause is that the same fact lives in three places that have no connection to each other:

  servicing.levels[].parts   what the price is actually built from
  jobs[].includes            the list the quote widget shows
  service_matrix             the comparison table on six pages

Changing the price model does not touch the other two. Nothing was checking them against each
other, and a wrong promise costs more than a wrong price: the customer has it in writing.

This maps each physical part to the words used for it and asserts the three agree. Labour and
inspection items are not checked — they carry no part cost, so there is nothing to check them
against; they are listed at the end so it is clear what this does and does not cover.

Exit code 1 on any disagreement.
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CAT = json.loads((ROOT / 'quote-catalogue.json').read_text())

# The level ids the three lists use for the same service.
LEVELS = [
    # (rate-card level, job id, matrix column key)
    ('interim', 'service-interim', 'i'),
    ('full', 'service-full', 'f'),
    ('major', 'service-major', 'm'),
]

# Each costed part, and how it is worded in the two customer-facing lists.
PARTS = {
    'oil_filter': {'includes': ['oil filter'], 'matrix': ['Oil filter']},
    'air_filter': {'includes': ['air filter'], 'matrix': ['Air filter']},
    'pollen_filter': {'includes': ['cabin or pollen filter', 'cabin filter', 'pollen filter'],
                      'matrix': ['Cabin / pollen filter']},
}


def inherits(job_id):
    """Services describe themselves as 'everything in the X', so a part fitted at a lower level
    is promised at the higher one without being named again."""
    return {'service-full': 'service-interim', 'service-major': 'service-full'}.get(job_id)


def promised_in_includes(job_id, part, seen=None):
    seen = seen or set()
    if job_id in seen:
        return False
    seen.add(job_id)
    job = next(j for j in CAT['jobs'] if j['id'] == job_id)
    text = ' | '.join(job.get('includes', [])).lower()
    if any(w.lower() in text for w in PARTS[part]['includes']):
        return True
    # "Everything in the interim service" carries the lower level's promises up.
    parent = inherits(job_id)
    if parent and any('everything in the' in l.lower() for l in job.get('includes', [])):
        return promised_in_includes(parent, part, seen)
    return False


def promised_in_matrix(col, part):
    for g in CAT['service_matrix']['groups']:
        for r in g['rows']:
            if r['label'] in PARTS[part]['matrix']:
                return col in r.get('in', [])
    return False


def main():
    problems = []
    print('part            level     priced  quote-widget  comparison-table')
    for part in PARTS:
        for level_id, job_id, col in LEVELS:
            lvl = next(l for l in CAT['servicing']['levels'] if l['id'] == level_id)
            priced = part in lvl['parts']
            inc = promised_in_includes(job_id, part)
            mat = promised_in_matrix(col, part)
            tick = lambda b: ' yes  ' if b else ' NO   '
            flag = '' if (priced == inc == mat) else '   <-- MISMATCH'
            print(f'  {part:<14} {level_id:<9}{tick(priced)}{tick(inc):>13}{tick(mat):>17}{flag}')
            if priced != inc:
                problems.append(f'{part} on {level_id}: priced={priced} but the quote widget '
                                f'says {inc}')
            if priced != mat:
                problems.append(f'{part} on {level_id}: priced={priced} but the comparison '
                                f'table says {mat}')

    if problems:
        print('\nA service promises a part it is not priced for, or is priced for one it does')
        print('not promise. Either way a customer can hold us to the words:')
        for x in problems:
            print('  ' + x)
        return 1

    print('\nevery costed part is promised by exactly the services that pay for it')
    print('(labour and inspection items carry no part cost and are not checked here)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
