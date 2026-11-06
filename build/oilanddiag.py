#!/usr/bin/env python3
"""Fix two things the earlier sweeps left behind.

1. The 18 oil-filter-change pages advertise "From £45". They were missed because they never
   carried any of the old figures the other sweeps hunted for. The widget on those same pages
   now quotes £115-£165, so a visitor reads £45 and is told nearly three times that. Logan
   confirmed the £115 banding, so the pages come up to meet it.

2. "not just a code read" now contradicts the page it sits on. It was written when a code read
   was something KITH did not sell separately; it now does, at £36, and that is the figure beside
   this very sentence. Reworded to describe the two tiers instead of disparaging one of them.
"""
import json
import math
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent


def _advertised(raw):
    """Round an engine price up to the pound for display. Servicing lands on pennies now."""
    return math.ceil(float(raw))


def price(job_id, band='small'):
    return _advertised(subprocess.run(
        ['node', '-e',
         "const E=require('./quote-engine.js'),C=require('./quote-catalogue.json');"
         "console.log(E.priceJob(C,process.argv[1],process.argv[2]).low);", job_id, band],
        cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip())


OIL = price('oil-filter-change')
READ = price('diagnostic-code-read')
FULL = price('diagnostic-full')

OLD_BLURB = ('A proper diagnosis of warning lights, running faults and electrical problems, '
             'not just a code read.')
NEW_BLURB = (f'Codes read for £{READ}, or full fault-finding at £{FULL} where the codes '
             f'do not settle it. The £{READ} comes off if you go on to the full test.')

SUBS = [
    (re.compile(r'<div><dt>Price</dt><dd>From £45</dd></div>'),
     f'<div><dt>Price</dt><dd>From £{OIL}</dd></div>'),
    (re.compile(r'(<title>Oil &amp; Filter Change[^<]*?)From £45'), rf'\g<1>From £{OIL}'),
    (re.compile(r'Oil (?:&amp;|and) [Ff]ilter [Cc]hange from £45(?![\d])'),
     f'Oil and filter change from £{OIL}'),
    (re.compile(r'from £45(?![\d])'), f'from £{OIL}'),
    (re.compile(r'From £45(?![\d])'), f'From £{OIL}'),
    (re.compile(r'"minPrice": "45"'), f'"minPrice": "{OIL}"'),
    (re.compile(re.escape(OLD_BLURB)), NEW_BLURB),
]


def main():
    print(f'oil and filter from £{OIL} · code read £{READ} · full diagnostic £{FULL}')
    oil_pages = sorted(ROOT.glob('oil-filter-change*.html'))
    changed = 0
    for p in sorted(ROOT.glob('*.html')):
        t = s = p.read_text()
        for pat, rep in SUBS:
            # The £45 rules are only safe on the oil pages; £45 could mean something else
            # elsewhere, and guessing is how the last round of breakage happened.
            if '45' in pat.pattern and p not in oil_pages:
                continue
            t = pat.sub(rep, t)
        if t != s:
            p.write_text(t)
            changed += 1
    print(f'pages rewritten: {changed} (of which {len(oil_pages)} are oil pages)')

    stale, broken = [], []
    for p in ROOT.glob('*.html'):
        t = p.read_text()
        if p in oil_pages and re.search(r'£45(?![\d])', t):
            stale.append(f'{p.name}: £45')
        if OLD_BLURB in t:
            stale.append(f'{p.name}: code-read blurb')
        for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
            try:
                json.loads(b)
            except Exception as e:
                broken.append(f'{p.name}: {e}')
    if stale:
        print('STALE:', sorted(set(stale))[:8])
    if broken:
        print('BROKEN JSON-LD:', broken[:4])
    if stale or broken:
        sys.exit(1)
    print('clean: oil pages match the price book, diagnostics blurb matches its own price.')


if __name__ == '__main__':
    main()
