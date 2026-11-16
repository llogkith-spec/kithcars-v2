#!/usr/bin/env python3
"""Retire dent-removal-<town> in favour of dent-repair-<town>.

The seventeen old pages measured 97.4% identical to each other - between the Croydon and Tooting
versions of an 1,865-word page the only differences were the town name, two road numbers and
"15" against "18" minutes. They have been rebuilt under a new slug rather than edited, because
the name was wrong as well as the content: KITH does not do paintless dent removal, and "dent
removal" is the exact phrase people use when they mean PDR.

This removes the old files, repoints the 85 internal links, and leaves the old URLs redirecting
so nothing that has been crawled or linked to is lost. The plain /dent-removal hub is untouched -
it is linked from 2,021 places and is a different question.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'build'))
from bw_towndata import TOWNS  # noqa: E402

OLD = re.compile(r'href="/dent-removal-([a-z-]+)"')


def main():
    towns = set(TOWNS)

    # 1. internal links
    repointed = pages = 0
    for p in sorted(ROOT.glob('*.html')):
        t = p.read_text()
        if '<html' not in t[:300] or 'dent-removal-' not in t:
            continue
        n = len(OLD.findall(t))
        if not n:
            continue
        new = OLD.sub(lambda m: f'href="/dent-repair-{m.group(1)}"'
                      if m.group(1) in towns else m.group(0), t)
        # the visible link text says "Dent Removal"; it should say what we actually do
        new = new.replace('>Dent Removal<', '>Dent Repair<')
        if new != t:
            p.write_text(new)
            repointed += n
            pages += 1
    print(f'internal links repointed: {repointed} across {pages} pages')

    # 2. remove the old files
    removed = []
    for t in towns:
        f = ROOT / f'dent-removal-{t}.html'
        if f.exists():
            f.unlink()
            removed.append(f.name)
    print(f'old pages removed: {len(removed)}')

    # 3. redirects. A splat rather than 34 blocks.
    toml = ROOT / 'netlify.toml'
    cfg = toml.read_text()
    block = '''
# The seventeen dent-removal town pages were 97.4% identical to each other and named for a
# service KITH does not offer - paintless dent removal. They were rebuilt as dent-repair-<town>,
# which is both accurate and what the work actually is. These URLs have been crawled and linked
# to, so they are kept alive and sent to the page that replaced them. 301, because the old ones
# are not coming back.
[[redirects]]
  from = "/dent-removal-:town"
  to = "/dent-repair-:town"
  status = 301
  force = true

[[redirects]]
  from = "/dent-removal-:town.html"
  to = "/dent-repair-:town"
  status = 301
  force = true
'''
    if 'dent-removal-:town' not in cfg:
        toml.write_text(cfg.rstrip() + '\n' + block)
        print('redirects added to netlify.toml')
    else:
        print('redirects already present')

    # --- verification ----------------------------------------------------------------------
    bad = []
    for t in towns:
        if (ROOT / f'dent-removal-{t}.html').exists():
            bad.append(f'dent-removal-{t}.html still exists')
        if not (ROOT / f'dent-repair-{t}.html').exists():
            bad.append(f'dent-repair-{t}.html was not built')
    left = sum(len(OLD.findall(p.read_text())) for p in ROOT.glob('*.html')
               if '<html' in p.read_text()[:300])
    if left:
        bad.append(f'{left} internal links still point at dent-removal-<town>')
    cfg = toml.read_text()
    if cfg.count('dent-removal-:town') != 2:
        bad.append('redirect rules not as expected')
    # the hub must be untouched
    if not (ROOT / 'dent-removal.html').exists():
        bad.append('the dent-removal hub was removed; it should not have been')

    if bad:
        print('\nPROBLEMS:')
        for x in bad[:10]:
            print('  ' + x)
        return 1
    print('\nclean: 17 pages replaced, every old URL redirects, the hub is untouched')
    return 0


if __name__ == '__main__':
    sys.exit(main())
