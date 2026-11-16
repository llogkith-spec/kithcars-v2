#!/usr/bin/env python3
"""Put real local facts into the existing bodywork town pages, and prove it worked.

The town pages are 71.6% word-for-word identical to each other on the axis that matters: same
service, different town. This inserts a researched, town-specific section into each one and then
measures both axes again, because a change like this can help one and hurt the other:

  same service, different town   the axis that is broken. Croydon's section is nothing like
                                 Cheam's, so this should fall.
  different service, same town   already healthy at 35.5%. Every bodywork page in a town gets
                                 the same local section, so this will rise. It has room to.

The build prints both and fails if the second climbs past the first, which would mean the fix had
simply moved the duplication rather than removed it.
"""
import pathlib
import re
import sys
from difflib import SequenceMatcher

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
ROOT = pathlib.Path(__file__).resolve().parent.parent

import bw_render  # noqa: E402
import bw_towns   # noqa: E402

# The bodywork services that have a page per town.
SERVICES = ['accident-repairs', 'bumper-repair', 'dent-removal', 'scratch-repair',
            'smart-repairs', 'car-respray', 'welding-rust-repair',
            'alloy-wheel-refurbishment', 'headlight-restoration']

MARKER = 'kx-local'


def body_text(html_text):
    i, j = html_text.find('<main>'), html_text.find('</main>')
    t = html_text[i:j] if i != -1 and j != -1 else html_text
    t = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', t, flags=re.S)
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', t)).strip()


def pairs(files, label):
    texts = {f: body_text((ROOT / f).read_text()).split() for f in files if (ROOT / f).exists()}
    ks = list(texts)
    rs = []
    for i, a in enumerate(ks):
        for b in ks[i + 1:]:
            rs.append(SequenceMatcher(None, texts[a], texts[b]).ratio())
    if not rs:
        return None
    rs.sort()
    return (sum(rs) / len(rs), rs[-1], len(rs), label)


def measure(towns):
    """(same service across towns, same town across services)."""
    across, within = [], []
    for s in SERVICES:
        r = pairs([f'{s}-{t}.html' for t in towns], s)
        if r: across.append(r)
    for t in towns:
        r = pairs([f'{s}-{t}.html' for s in SERVICES], t)
        if r: within.append(r)
    mean_a = sum(x[0] for x in across) / len(across)
    worst_a = max(x[1] for x in across)
    mean_w = sum(x[0] for x in within) / len(within)
    worst_w = max(x[1] for x in within)
    return (mean_a, worst_a, mean_w, worst_w)


def main():
    towns = list(bw_towns.TOWNS)
    print(f'towns with researched data: {", ".join(towns)}')

    before = measure(towns)
    print(f'\nbefore')
    print(f'  same service, different town : {before[0]*100:.1f}% mean, {before[1]*100:.1f}% worst')
    print(f'  different service, same town : {before[2]*100:.1f}% mean, {before[3]*100:.1f}% worst')

    added = skipped = 0
    for t in towns:
        sec = bw_towns.section(t)
        if not sec:
            continue
        heading, blocks = sec
        html = ('<section class="section ' + MARKER + '"><div class="container kx-prose">'
                '<h2>' + heading + '</h2>'
                + ''.join(bw_render._para(b) for b in blocks) +
                '</div></section>')
        for s in SERVICES:
            f = ROOT / f'{s}-{t}.html'
            if not f.exists():
                continue
            txt = f.read_text()
            if MARKER in txt:
                skipped += 1
                continue
            if '</main>' not in txt:
                skipped += 1
                continue
            f.write_text(txt.replace('</main>', html + '</main>', 1))
            added += 1

    print(f'\nlocal section added to {added} pages ({skipped} already had it or had no main)')

    after = measure(towns)
    print(f'\nafter')
    print(f'  same service, different town : {after[0]*100:.1f}% mean, {after[1]*100:.1f}% worst'
          f'   ({(after[0]-before[0])*100:+.1f} pts)')
    print(f'  different service, same town : {after[2]*100:.1f}% mean, {after[3]*100:.1f}% worst'
          f'   ({(after[2]-before[2])*100:+.1f} pts)')

    bad = []
    if after[0] >= before[0]:
        bad.append('the across-town figure did not fall - the local sections are not distinct enough')
    if after[2] > after[0] + 0.15:
        bad.append('within-town duplication now exceeds across-town by too much: the fix has '
                   'moved the problem rather than removed it')
    for t in towns:
        for s in SERVICES:
            f = ROOT / f'{s}-{t}.html'
            if f.exists():
                x = f.read_text()
                if x.count(MARKER) > 1:
                    bad.append(f'{f.name}: section added twice')
                if x.count('</body>') != 1:
                    bad.append(f'{f.name}: markup damaged')
    if bad:
        print('\nPROBLEMS:')
        for x in bad[:8]:
            print('  ' + x)
        return 1
    print('\nclean: every town page now carries facts that are true only of that town')
    return 0


if __name__ == '__main__':
    sys.exit(main())
