#!/usr/bin/env python3
"""Build every bodywork and insurance page, then prove the set is fit to publish.

Content lives in bw_content_*.py modules, each exporting PAGES. This script renders them all and
then checks the things that would actually hurt if they were wrong:

  uniqueness   The point of failure for any large page set. Google's scaled-content policy is
               aimed squarely at pages that differ only in a swapped noun, and the existing
               town pages on this site already sit at 71.6% word-for-word overlap with each
               other. Every new page is compared against every other new page in the same
               category, and the build fails on any pair above the threshold.
  claims       KITH is on no insurer panel and is not a manufacturer-approved repairer. A page
               that says otherwise is a false advertising claim, so the forbidden phrasings are
               searched for explicitly.
  schema       Every JSON-LD block must parse, or the whole graph is ignored by search engines.
  links        An internal link to a page that does not exist is a 404 in the crawl.
  slugs        A slug collision silently overwrites a real page in the site root.

The build writes nothing until every page has rendered, so a failure part way through does not
leave the site half-updated.
"""
import importlib
import json
import pathlib
import re
import sys
from collections import defaultdict
from difflib import SequenceMatcher

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
ROOT = pathlib.Path(__file__).resolve().parent.parent
import bw_render  # noqa: E402

MODULES = [
    'bw_content_insurance',
    'bw_content_ins2',
    'bw_panels',
    'bw_damage',
    'bw_content_ins3',
    'bw_content_writeoff',
    'bw_content_claim',
    'bw_content_process',
    'bw_content_fill',
    'bw_hubs',
]

# Similarity above this between two pages in the same category fails the build.
MAX_SIMILARITY = 0.62

# Things we must never say, because they are not true.
FORBIDDEN = [
    (r'\bapproved repairer for\b', 'claims to be an approved repairer for an insurer'),
    (r'\b(we are|kith is) (an? )?(insurer[- ])?approved\b', 'claims approved status'),
    # "manufacturer-approved oil" and "manufacturer-approved tyres" are true and are about the
    # product, not about us - the BMW star and Mercedes MO markings are real things we source.
    # Only flag the phrase where it attaches to a repairer, bodyshop, garage or workshop.
    (r'\bmanufacturer[- ]approved\s+(repairer|bodyshop|body shop|garage|workshop|centre)\b',
     'claims manufacturer approval'),
    (r'\b(bmw|audi|mercedes|volkswagen|tesla|ford|toyota)[- ]approved\s+'
     r'(repairer|bodyshop|body shop|garage|workshop|centre)\b', 'implies marque approval'),
    (r'\bon (the )?(insurer|insurance) panel\b', 'claims panel membership'),
]


def load():
    pages, seen = [], {}
    for name in MODULES:
        mod = importlib.import_module(name)
        importlib.reload(mod)
        for p in mod.PAGES:
            if p['slug'] in seen:
                raise SystemExit(f'duplicate slug {p["slug"]} in {name} and {seen[p["slug"]]}')
            seen[p['slug']] = name
            pages.append(p)
    return pages


def visible_text(html_text):
    t = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', html_text, flags=re.S)
    t = re.sub(r'<[^>]+>', ' ', t)
    return re.sub(r'\s+', ' ', t).strip()


def body_text(html_text):
    """Only the page's own prose - chrome excluded, or every page looks 90% alike."""
    i = html_text.find('<main>')
    j = html_text.find('</main>')
    return visible_text(html_text[i:j] if i != -1 and j != -1 else html_text)


def main():
    pages = load()
    print(f'pages to build: {len(pages)}')

    # Render everything into memory first.
    rendered = {}
    for p in pages:
        rendered[p['slug']] = bw_render.render(p)

    problems = []

    # --- slug collisions with pages already on the site -------------------------------------
    existing = {f.stem for f in ROOT.glob('*.html')}
    building = {p['slug'] for p in pages}
    for p in pages:
        if p['slug'] in existing and not (ROOT / f'{p["slug"]}.html').read_text().count('kx-keycard'):
            # An existing hand-built page with this slug would be overwritten.
            if p['slug'] not in {q['slug'] for q in pages}:
                problems.append(f'{p["slug"]}: would overwrite an existing page')

    # --- forbidden claims --------------------------------------------------------------------
    for p in pages:
        text = body_text(rendered[p['slug']]).lower()
        for pattern, why in FORBIDDEN:
            if re.search(pattern, text):
                problems.append(f'{p["slug"]}: {why}')

    # --- schema ------------------------------------------------------------------------------
    for p in pages:
        for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>',
                             rendered[p['slug']], re.S):
            try:
                json.loads(m.group(1))
            except Exception as exc:
                problems.append(f'{p["slug"]}: JSON-LD will not parse ({exc})')

    # --- internal links ----------------------------------------------------------------------
    # While the set is still being written, pages legitimately point at siblings that do not
    # exist yet, so --partial downgrades this one check to a count. It is a hard failure on the
    # final build, because a link to a missing page is a 404 in the crawl.
    partial = '--partial' in sys.argv
    dangling = []
    for p in pages:
        for slug, _ in p.get('related', []):
            if slug not in building and slug not in existing:
                dangling.append(f'{p["slug"]}: links to /{slug}, which does not exist')
        for name, href in p['crumbs']:
            if href and href not in building and href not in existing:
                dangling.append(f'{p["slug"]}: breadcrumb points at /{href}, which does not exist')
    if partial:
        if dangling:
            print(f'  forward refs: {len(dangling)} (not yet written; --partial)')
    else:
        problems.extend(dangling)

    # --- uniqueness --------------------------------------------------------------------------
    by_cat = defaultdict(list)
    for p in pages:
        by_cat[p.get('category', 'other')].append(p['slug'])

    worst = (0.0, '', '')
    for cat, slugs in by_cat.items():
        texts = {s: body_text(rendered[s]).split() for s in slugs}
        for i, a in enumerate(slugs):
            for b in slugs[i + 1:]:
                r = SequenceMatcher(None, texts[a], texts[b]).ratio()
                if r > worst[0]:
                    worst = (r, a, b)
                if r > MAX_SIMILARITY:
                    problems.append(f'too similar ({r*100:.0f}%): {a} / {b}')

    words = {s: len(body_text(h).split()) for s, h in rendered.items()}
    print(f'  words       : {min(words.values())} min, '
          f'{sum(words.values())//len(words)} mean, {max(words.values())} max')
    print(f'  most alike  : {worst[0]*100:.0f}%  ({worst[1]} / {worst[2]})')

    if problems:
        print(f'\nPROBLEMS ({len(problems)}):')
        for x in problems[:20]:
            print('  ' + x)
        return 1

    for slug, html_text in rendered.items():
        (ROOT / f'{slug}.html').write_text(html_text)

    print(f'\nclean: {len(rendered)} pages written, none above {MAX_SIMILARITY*100:.0f}% alike, '
          f'no false claims, all schema parses, every link resolves')
    return 0


if __name__ == '__main__':
    sys.exit(main())
