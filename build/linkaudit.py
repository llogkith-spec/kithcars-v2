#!/usr/bin/env python3
"""Check that every internal link on the site actually goes somewhere.

Found by accident: 923 pages carried a "Contact" nav link to /#contact and the homepage had no
such anchor, so the link dumped the visitor at the top of the page; the 17 dent-removal area
pages linked to a #get-a-quote section that a regeneration had deleted, so their main call to
action did nothing and the quote widget was missing entirely; and the FAQ page's contents list
jumped to ids its own headings never carried.

None of those show up as an error anywhere. The page loads, the link is clickable, and nothing
happens. This is the only thing that catches them.

Checks three kinds of link:
  href="#x"            -> the page must contain id="x"
  href="/#x"           -> the homepage must contain id="x"
  href="/page"         -> page.html must exist

Exit code 1 if anything is dead, so it can gate a deploy.
"""
import pathlib
import re
import sys
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Links that leave the site, or that the server handles rather than a file.
EXTERNAL = re.compile(r'^(https?:|mailto:|tel:|wa\.me|//|#$|javascript:)', re.I)


def main():
    pages = {p.name: p.read_text() for p in ROOT.glob('*.html')}
    ids = {n: set(re.findall(r'id="([\w-]+)"', t)) for n, t in pages.items()}
    home = ids.get('index.html', set())
    # Every file in the repo, by its path relative to the root, so links into img/ and the like
    # are checked against the real file rather than reported as missing.
    files = {str(p.relative_to(ROOT)) for p in ROOT.rglob('*')
             if p.is_file() and '.git' not in p.parts}

    dead = defaultdict(list)

    for name, text in pages.items():
        for href in re.findall(r'href="([^"]+)"', text):
            if EXTERNAL.match(href):
                continue

            # Same-page anchor.
            if href.startswith('#'):
                anchor = href[1:]
                if anchor and anchor not in ids[name]:
                    dead[f'#{anchor}'].append(name)
                continue

            path, _, anchor = href.partition('#')

            # Homepage anchor: "/#x" or "index.html#x".
            if path in ('/', '', 'index.html') and anchor:
                if anchor not in home:
                    dead[f'/#{anchor}'].append(name)
                continue

            if path in ('/', ''):
                continue

            # Internal page. Netlify serves /foo from foo.html, so try both spellings.
            target = path.lstrip('/')
            if target.endswith('/'):
                target = target[:-1]
            if target in files or f'{target}.html' in files:
                if anchor and anchor not in ids.get(f'{target}.html', ids.get(target, set())):
                    dead[f'/{target}#{anchor}'].append(name)
                continue
            dead[f'/{target}'].append(name)

    print(f'checked internal links across {len(pages)} pages')
    if not dead:
        print('every internal link resolves')
        return 0

    for target, pages_with in sorted(dead.items(), key=lambda kv: -len(kv[1])):
        print(f'  DEAD {target:<34} linked from {len(pages_with)} page(s), '
              f'e.g. {", ".join(sorted(pages_with)[:3])}')
    print(f'\n{sum(len(v) for v in dead.values())} dead links across {len(dead)} targets')
    return 1


if __name__ == '__main__':
    sys.exit(main())
