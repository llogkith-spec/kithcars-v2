#!/usr/bin/env python3
"""Make every diagnostics price on the site match the two tiers that actually exist.

The site was quoting three different things at once: "£30+VAT" for a code read inside an FAQ
answer, "£122+VAT" for a complex diagnostic a few paragraphs later, and "Diagnostics from £122"
in the meta descriptions and service cards on 69 pages. If a £36 code read is a real product —
and Logan confirms it is — then "from £122" is not the from-price, and quoting either figure
plus VAT to a private customer understates it.

So: the from-price becomes the code read, the full diagnostic is named separately, and both are
shown inc VAT, which is what a consumer price has to be.
"""
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent


def price(job_id):
    return int(subprocess.run(
        ['node', '-e',
         "const E=require('./quote-engine.js'),C=require('./quote-catalogue.json');"
         "console.log(E.priceJob(C,process.argv[1],'small').low);", job_id],
        cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip())


READ = price('diagnostic-code-read')
FULL = price('diagnostic-full')

SUBS = [
    # Service cards and spec rows: the from-price is the cheaper tier.
    (re.compile(r'(Diagnostics[^<]*</span><span class="kh-svc-meta">From )£122'), rf'\g<1>£{READ}'),
    (re.compile(r'<div><dt>Price</dt><dd>From £122</dd></div>'),
     f'<div><dt>Price</dt><dd>£{READ} code read &middot; £{FULL} full</dd></div>'),
    (re.compile(r'<div><b>From £122</b><span>Written quote first</span></div>'),
     f'<div><b>From £{READ}</b><span>Full diagnostic £{FULL}</span></div>'),
    # Prose and meta descriptions.
    (re.compile(r'Diagnostics from £122\.'), f'Code read £{READ}, full diagnostics £{FULL}.'),
    (re.compile(r'Engine diagnostics from £122\.'), f'Code read £{READ}, full diagnostics £{FULL}.'),
    (re.compile(r'Diagnostics from £122'), f'Diagnostics from £{READ}'),
    (re.compile(r'complex diagnostic at £122\+VAT'), f'full diagnostic at £{FULL} inc VAT'),
    (re.compile(r'The diagnostic at £30\+VAT'), f'The £{READ} code read'),
    (re.compile(r'diagnostic at £30\+VAT'), f'£{READ} code read'),
    (re.compile(r'£122\+VAT'), f'£{FULL} inc VAT'),
    (re.compile(r'£30\+VAT'), f'£{READ} inc VAT'),
    (re.compile(r'from £122(?![\d])'), f'from £{READ}'),
    # Page titles carry the figure too, and Google shows the title.
    (re.compile(r'(<title>[^<]*?)From £122(?![\d.])'), rf'\g<1>From £{READ}'),
    (re.compile(r'(<title>[^<]*?)– £122(?![\d.])'), rf'\g<1>– From £{READ}'),
    (re.compile(r'<li>From £122(?![\d.]) &middot; 1–2 hours</li>'),
     f'<li>£{READ} code read &middot; £{FULL} full diagnostic</li>'),
    (re.compile(r'<div><b>From £122(?![\d.])</b><span>Written quote before we start</span></div>'),
     f'<div><b>From £{READ}</b><span>Full diagnostic £{FULL}</span></div>'),
    # The pricing list states it plus VAT; a consumer price includes VAT.
    (re.compile(r'(<span>Deep / Complex Diagnostic</span><span>)£122 \+ VAT(</span>)'),
     rf'\g<1>£{FULL}\g<2>'),
]


def main():
    print(f'code read £{READ} · full diagnostic £{FULL}')
    changed = 0
    for p in sorted(ROOT.glob('*.html')):
        t = s = p.read_text()
        for pat, rep in SUBS:
            t = pat.sub(rep, t)
        if t != s:
            p.write_text(t)
            changed += 1
    print(f'pages rewritten: {changed}')

    stale, broken = [], []
    for p in ROOT.glob('*.html'):
        t = p.read_text()
        for m in re.finditer(r'£122(?![\d.])|£30\+VAT', t):
            stale.append(f'{p.name}: {m.group(0)}')
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
    print('clean: one diagnostics story, both tiers inc VAT.')


if __name__ == '__main__':
    main()
