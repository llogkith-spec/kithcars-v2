#!/usr/bin/env python3
"""Split the workmanship warranty by division: 3 months mechanical, 12 months bodywork.

The site carried a single blanket claim - "3-month workmanship warranty" - on 931 pages, which
undersold the bodyshop by nine months on every page it appeared. KITH warrants bodywork for a
year.

Which division a page belongs to is not guessed from its name. Every page already declares the
flow its quote widget opens in, and that declaration is the classifier:

    data-flow="bodywork"    146 pages  ->  12-month
    data-flow="mechanical"  720 pages  ->  unchanged
    data-flow="tyres"        18 pages  ->  unchanged
    data-flow="tuning"       18 pages  ->  unchanged
    data-flow="recovery"     19 pages  ->  unchanged (recovery carries no workmanship warranty)

Ten pages declare no flow and are classified here by hand, because two of them are bodywork, five
are mechanical blog posts, and three are hub pages that speak for the whole business and so have
to name both terms rather than pick one.

The replacement is a noun phrase in every single instance - "carries our 3-month workmanship
warranty", "the repair has our 3-month workmanship warranty" - so swapping the number leaves the
grammar intact. That was checked across the bodywork pages before this was written, and it is
checked again at the end. "12-month" rather than "1-year" because it is the form that drops into
those sentences without rewriting them.

A previous blanket find-and-replace on this site turned recovery prices into a list that went
down and then up again, so nothing here is replaced site-wide: every substitution is scoped to a
classified page, and the verification pass refuses to finish if a page ends up claiming the
wrong term for its division.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Pages that declare no data-flow, classified by what they actually sell.
NO_FLOW_BODYWORK = {'bodywork-gallery.html', 'stone-chip-repair.html'}
NO_FLOW_MECHANICAL = {
    'blog-car-servicing-interval-guide.html', 'blog-dpf-warning-light-what-to-do.html',
    'blog-mot-failure-common-reasons.html', 'blog-timing-chain-rattle-causes.html',
    'blog-when-to-change-brake-pads.html',
}
# Hub pages that speak for the whole business: they must name both terms, not choose one.
HUB = {'index.html', 'faq.html', 'about-us.html'}

# Every shape the claim takes on a bodywork page. These are regexes rather than plain strings
# because the phrase wraps across a line break in the source on at least one page, so a literal
# "3-month workmanship warranty" with single spaces silently misses it. \s+ keeps whatever
# whitespace was there, newline included, so the file's formatting survives the edit.
BODY_SUBS = [
    (re.compile(r'3-month(\s+)workmanship(\s+)warranty'), r'12-month\1workmanship\2warranty'),
    (re.compile(r'<b>3-month</b>(\s+)workmanship(\s+)warranty'), r'<b>12-month</b>\1workmanship\2warranty'),
    (re.compile(r'3-month(\s+)warranty'), r'12-month\1warranty'),
]

# The hub pages, reworded by hand so each reads naturally while carrying both terms.
HUB_SUBS = [
    ('<div><b>3-month warranty</b><span>On our workmanship, on every repair.</span></div>',
     '<div><b>Workmanship warranty</b><span>3 months on mechanical, 12 months on bodywork.</span></div>'),
    ('<li><b>3-month</b> workmanship warranty</li>',
     '<li><b>3-month</b> mechanical &middot; <b>12-month</b> bodywork warranty</li>'),
    ('Dealer-level diagnostics, OE-quality parts and a 3-month workmanship warranty, at '
     'independent prices.',
     'Dealer-level diagnostics, OE-quality parts, and a workmanship warranty of 3 months on '
     'mechanical work and 12 months on bodywork &mdash; at independent prices.'),
]


def flow_of(text):
    m = re.search(r'data-flow="([a-z]+)"', text)
    return m.group(1) if m else None


def main():
    pages = sorted(ROOT.glob('*.html'))
    counts = {'bodywork': 0, 'hub': 0, 'left alone': 0}
    changed = 0

    for p in pages:
        src = p.read_text()
        if 'warranty' not in src:
            continue
        flow = flow_of(src)
        name = p.name

        if flow == 'bodywork' or name in NO_FLOW_BODYWORK:
            kind, subs = 'bodywork', BODY_SUBS
        elif name in HUB:
            kind, subs = 'hub', HUB_SUBS
        else:
            # mechanical, tyres, tuning, recovery and the mechanical blog posts: 3 months stands
            counts['left alone'] += 1
            continue

        out = src
        for old, new in subs:
            out = old.sub(new, out) if hasattr(old, 'sub') else out.replace(old, new)
        counts[kind] += 1
        if out != src:
            p.write_text(out)
            changed += 1

    print(f'rewritten: {changed} pages')
    for k, v in counts.items():
        print(f'  {k:<12} {v}')

    # --- verification -------------------------------------------------------------------------
    # A page must never claim the other division's term, and the structured data on it must still
    # parse. Either failure means the sweep did damage, so it exits non-zero.
    wrong, broken = [], []
    for p in pages:
        t = p.read_text()
        if 'warranty' not in t:
            continue
        flow, name = flow_of(t), p.name
        is_body = flow == 'bodywork' or name in NO_FLOW_BODYWORK
        is_hub = name in HUB

        if is_body and re.search(r'3-month\s*(</b>)?\s*(workmanship\s*)?warranty', t):
            wrong.append(f'{name}: bodywork page still claims 3 months')
        if not is_body and not is_hub and '12-month' in t:
            wrong.append(f'{name}: {flow} page claims 12 months')

        for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
            try:
                json.loads(b)
            except Exception as e:
                broken.append(f'{name}: {e}')

    if wrong:
        print(f'\nWRONG TERM ({len(wrong)}):')
        for x in wrong[:10]:
            print('  ' + x)
    if broken:
        print(f'\nBROKEN JSON-LD ({len(broken)}):')
        for x in broken[:5]:
            print('  ' + x)
    if wrong or broken:
        return 1

    body = sum(1 for p in pages if '12-month workmanship warranty' in p.read_text())
    mech = sum(1 for p in pages
               if '3-month workmanship warranty' in p.read_text() and p.name not in HUB)
    print(f'\nclean: {body} pages now say 12 months, {mech} still say 3 months,')
    print('       and no page claims the term belonging to the other division')
    return 0


if __name__ == '__main__':
    sys.exit(main())
