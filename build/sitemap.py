#!/usr/bin/env python3
"""Rebuild sitemap.xml from what is actually on disk.

The old one was hand-maintained and had drifted: 932 urls against 935 pages, a lastmod a week
stale, and - the part that matters - no homepage. The most important url on the site was the one
missing, because index.html does not follow the same name-to-path rule as everything else: it is
served at "/" rather than "/index".

Three pages are left out deliberately, and each for its own reason:

  google*.html   Search Console's verification file. Listing it invites Google to index a token.
  kpi.html       an internal dashboard. Nothing about it is for the public.
  thank-you.html only reachable after booking. Indexed, it collects visitors who have booked
                 nothing and reads to Google as a thin page.

Anything carrying a noindex robots tag is skipped too: telling Google to index a page in the
sitemap while telling it not to in the markup is a contradiction it resolves by trusting neither.

lastmod comes from git - the date that file was last committed - rather than a blanket "today",
which tells a crawler nothing and trains it to ignore the field.
"""
import datetime
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = 'https://www.kithcars.com'

SKIP_EXACT = {'kpi.html', 'thank-you.html'}
SKIP_MATCH = [re.compile(r'^google[0-9a-f]+\.html$', re.I)]


def git_dates():
    """file -> date of the commit that last touched it, in one pass."""
    out = subprocess.run(
        ['git', 'log', '--name-only', '--no-merges', '--date=short', '--format=%cd'],
        cwd=ROOT, capture_output=True, text=True).stdout
    dates, cur = {}, None
    for line in out.splitlines():
        line = line.strip()
        if not line:
            continue
        if re.fullmatch(r'\d{4}-\d{2}-\d{2}', line):
            cur = line
        elif cur and line.endswith('.html') and line not in dates:
            dates[line] = cur          # log is newest first, so the first sighting wins
    return dates


def main():
    dates = git_dates()
    today = datetime.date.today().isoformat()
    rows, skipped = [], []

    for p in sorted(ROOT.glob('*.html')):
        name = p.name
        if name in SKIP_EXACT or any(rx.match(name) for rx in SKIP_MATCH):
            skipped.append(name)
            continue
        head = p.read_text()[:4000]
        if re.search(r'<meta[^>]+name=["\']robots["\'][^>]*noindex', head, re.I):
            skipped.append(name + ' (noindex)')
            continue
        # index.html is served at the root, not at /index.
        loc = BASE + '/' if name == 'index.html' else BASE + '/' + name[:-5]
        rows.append((loc, dates.get(name, today)))

    # Homepage first, then alphabetical: a crawler reads top-down and should meet it first.
    rows.sort(key=lambda r: (r[0] != BASE + '/', r[0]))

    body = '\n'.join(f'  <url><loc>{loc}</loc><lastmod>{d}</lastmod></url>' for loc, d in rows)
    (ROOT / 'sitemap.xml').write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + body + '\n</urlset>\n')

    print(f'pages on disk : {len(list(ROOT.glob("*.html")))}')
    print(f'in sitemap    : {len(rows)}')
    print(f'left out      : {len(skipped)}  ({", ".join(skipped)})')
    print(f'homepage first: {rows[0][0]}')

    # The homepage must be there, nothing may be listed twice, and the removed pricing page must
    # not have crept back.
    locs = [r[0] for r in rows]
    bad = []
    if BASE + '/' not in locs:
        bad.append('homepage missing')
    if len(set(locs)) != len(locs):
        bad.append('duplicate urls')
    if any('pricing' in l for l in locs):
        bad.append('pricing page still listed')
    if bad:
        print('\nPROBLEMS:', '; '.join(bad))
        return 1
    print('\nclean: homepage first, no duplicates, nothing listed that should not be')
    return 0


if __name__ == '__main__':
    sys.exit(main())
