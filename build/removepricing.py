#!/usr/bin/env python3
"""Take the pricing page off the site, without handing Google 936 dead ends.

Logan wants it gone. Deleting the file alone would not do that: 923 pages carry a "Pricing" link
in the header nav, thirteen more link to it in the body, and it sits in the sitemap. Left as they
are, every one of those becomes a 404 - which is exactly the fault the link audit cleared earlier,
recreated on purpose.

So four things happen together:

  1. the page is deleted
  2. every link to it is removed from the markup
  3. /pricing is redirected to the instant quote, because a page linked from 923 of its own pages
     has almost certainly been crawled, and anyone arriving from a search result or an old
     bookmark should land on the thing that replaced it rather than an error
  4. it comes out of the sitemap

The redirect is 301 rather than 302: this is permanent, and a 301 passes on whatever ranking the
page had accumulated instead of stranding it.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

LINKS = [
    re.compile(r'\s*<li[^>]*>\s*<a href="/pricing">Pricing</a>\s*</li>', re.I),
    re.compile(r'\s*<li[^>]*>\s*<a href="pricing\.html"[^>]*>[^<]*</a>\s*</li>', re.I),
    re.compile(r'\s*<a href="/pricing">Pricing</a>', re.I),
    re.compile(r'\s*<a href="pricing\.html"[^>]*>[^<]*</a>', re.I),
]

REDIRECT = '''
# The pricing page was removed. It was linked from 923 pages and had been crawled, so the URL is
# kept alive and sent to the instant quote - which answers the same question with a real number
# for the customer's own car. 301, because it is not coming back.
[[redirects]]
  from = "/pricing"
  to = "/#quote"
  status = 301
  force = true

[[redirects]]
  from = "/pricing.html"
  to = "/#quote"
  status = 301
  force = true
'''


def main():
    page = ROOT / 'pricing.html'
    existed = page.exists()
    if existed:
        page.unlink()

    changed = 0
    for p in sorted(ROOT.glob('*.html')):
        t = s = p.read_text()
        for rx in LINKS:
            t = rx.sub('', t)
        if t != s:
            p.write_text(t)
            changed += 1

    # Sitemap: drop the <url> block containing the pricing page.
    sm = ROOT / 'sitemap.xml'
    if sm.exists():
        x = sm.read_text()
        x2 = re.sub(r'\s*<url>(?:(?!</url>).)*?pricing(?:(?!</url>).)*?</url>', '', x, flags=re.S)
        if x2 != x:
            sm.write_text(x2)

    # Redirects, added once.
    nt = ROOT / 'netlify.toml'
    cfg = nt.read_text()
    if 'from = "/pricing"' not in cfg:
        cfg = cfg.rstrip() + '\n' + REDIRECT
        nt.write_text(cfg)

    print(f'pricing.html deleted : {existed}')
    print(f'pages delinked       : {changed}')

    # Nothing may still point at it, and the redirect must be in place so the URL still answers.
    left = []
    for p in ROOT.glob('*.html'):
        t = p.read_text()
        if re.search(r'href="/?pricing(\.html)?"', t):
            left.append(p.name)
    sm_left = 'pricing' in (sm.read_text() if sm.exists() else '')
    red = 'from = "/pricing"' in nt.read_text()

    print(f'links remaining      : {len(left)}')
    print(f'still in sitemap     : {sm_left}')
    print(f'redirect in place    : {red}')
    if left or sm_left or not red:
        for x in left[:8]:
            print('  still links:', x)
        return 1
    print('\nclean: the page is gone, nothing links to it, and /pricing still answers with a 301')
    return 0


if __name__ == '__main__':
    sys.exit(main())
