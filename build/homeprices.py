#!/usr/bin/env python3
"""Reconcile the homepage's quick-price strip with the price book.

The homepage carried its own figures — interim £130, pads £90, clutch £610, cambelt £385,
battery £140 — every one of them below what the quote engine on the same page will quote.
A visitor reading "Clutch from £610" and then being shown £735 has been misled by the site
itself, and the homepage is the page most of them land on.

Each entry is tied to a catalogue job id, so the strip can never drift from the price book
again: re-run this after any price change and it rewrites itself.
"""
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Homepage link -> the catalogue job whose cheapest band is the honest "from", and the
# wording around the figure.
STRIP = {
    '/car-servicing':     ('service-interim',   'Interim from £{}'),
    '/mot-testing':       ('mot',               '£{} fixed'),
    '/brake-repairs':     ('brake-pads-front',  'Pads from £{}'),
    '/clutch-replacement': ('clutch',           'From £{}'),
    '/cambelt-replacement': ('cambelt',         'From £{}'),
    '/battery-electrical': ('battery',          'Batteries from £{}'),
}


def from_price(job_id):
    out = subprocess.run(
        ['node', '-e',
         "const E=require('./quote-engine.js'),C=require('./quote-catalogue.json');"
         "let m=1e9;for(const b of Object.keys(C.bands)){const r=E.priceJob(C,process.argv[1],b);"
         "if(r.low<m)m=r.low;}console.log(m);", job_id],
        cwd=ROOT, capture_output=True, text=True, check=True)
    return int(out.stdout.strip())


def main():
    p = ROOT / 'index.html'
    html = src = p.read_text()
    report = []

    for href, (job, tpl) in STRIP.items():
        price = from_price(job)
        want = tpl.format(price)
        pat = re.compile(r'(<a href="' + re.escape(href) + r'"><b>[^<]+</b><span>)([^<]*)(</span></a>)')
        m = pat.search(html)
        if not m:
            report.append(f'  NOT FOUND  {href}')
            continue
        if m.group(2) != want:
            report.append(f'  {href}: "{m.group(2)}" -> "{want}"')
            html = pat.sub(lambda mm: mm.group(1) + want + mm.group(3), html, count=1)

    # The two summary captions carry the same figures.
    interim = from_price('service-interim')
    mot = from_price('mot')
    old_cap = re.search(r'<span class="from">Services from £\d+[^<]*</span>', html)
    if old_cap:
        new_cap = f'<span class="from">Services from £{interim} &middot; MOT £{mot} fixed</span>'
        if old_cap.group(0) != new_cap:
            report.append(f'  caption: "{old_cap.group(0)}" -> "{new_cap}"')
            html = html.replace(old_cap.group(0), new_cap, 1)

    # Oil is Castrol, and the homepage never said so.
    OLD_MECH = ('<h3>Mechanical &amp; servicing</h3><p>Brakes, clutches, timing chains, '
                'diagnostics, servicing and MOT on all makes.</p>')
    NEW_MECH = ('<h3>Mechanical &amp; servicing</h3><p>Brakes, clutches, timing chains, '
                'diagnostics, servicing and MOT on all makes. Every service is filled with '
                'Castrol oil in the grade your engine&rsquo;s maker specifies.</p>')
    if OLD_MECH in html:
        html = html.replace(OLD_MECH, NEW_MECH, 1)
        report.append('  homepage now names Castrol oil')

    if html != src:
        p.write_text(html)

    print('homepage price strip reconciled with quote-catalogue.json')
    for line in report:
        print(line)
    if not report:
        print('  (already in step)')

    # Verify: every figure in the strip now matches the price book.
    html = p.read_text()
    bad = []
    for href, (job, tpl) in STRIP.items():
        want = tpl.format(from_price(job))
        m = re.search(r'<a href="' + re.escape(href) + r'"><b>[^<]+</b><span>([^<]*)</span></a>', html)
        if not m or m.group(1) != want:
            bad.append(f'{href}: {m.group(1) if m else "missing"} != {want}')
    if bad:
        print('MISMATCH:', bad)
        sys.exit(1)
    print('verified: every homepage figure matches the price book.')


if __name__ == '__main__':
    main()
