#!/usr/bin/env python3
"""Regenerate the bodywork gallery's filter row and card grid from gallery_items.json.

Run from the repo root:  python3 build/gallerygen.py

It rewrites only the block between the two KC-GALLERY markers in bodywork-gallery.html, so the
page's header, intro, footer and scripts are left exactly as they are. Everything this needs is
inside the repo, which is the point: an earlier version of this script lived outside it and the
gallery was lost when that working copy went away.
"""
import json, pathlib, sys, html

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / 'build' / 'gallery_items.json'
PAGE = ROOT / 'bodywork-gallery.html'
START = '<!-- KC-GALLERY:start -->'
END = '<!-- KC-GALLERY:end -->'


def esc(s):
    return html.escape(s or '', quote=True)


def alt(item, side=None):
    """Alt text describes the photograph, not the marketing around it."""
    bits = [item['title']]
    if item.get('car'):
        bits.append(item['car'])
    if side:
        bits.append(side)
    return ', '.join(bits)


def caption(item):
    h = '<figcaption class="kc-cap"><strong>' + esc(item['title']) + '</strong>'
    if item.get('car'):
        h += '<span>' + esc(item['car']) + '</span>'
    if item.get('note'):
        h += '<span>' + esc(item['note']) + '</span>'
    if item.get('price'):
        # Only ever a figure the owner has confirmed against a real invoice.
        h += '<span class="kc-price">' + esc(item['price']) + ' inc VAT</span>'
    return h + '</figcaption>'


def card(item):
    t = esc(item.get('type', ''))
    if item.get('before') and item.get('after'):
        lb = item.get('labelBefore', 'Before')
        la = item.get('labelAfter', 'After')
        media = (
            '<div class="kc-compare" data-label-before="' + esc(lb) + '" data-label-after="' + esc(la) + '">'
            '<img class="kc-before" src="' + esc(item['before']) + '" alt="' + esc(alt(item, lb.lower())) + '" '
            'loading="lazy" decoding="async" width="900" height="1600"/>'
            '<img class="kc-after" src="' + esc(item['after']) + '" alt="' + esc(alt(item, la.lower())) + '" '
            'loading="lazy" decoding="async" width="900" height="1600"/></div>'
        )
    else:
        media = (
            '<div class="kc-single"><img src="' + esc(item['image']) + '" alt="' + esc(alt(item)) + '" '
            'loading="lazy" decoding="async" width="900" height="1600"/></div>'
        )
    return '<figure class="kc-item" data-type="' + t + '">' + media + caption(item) + '</figure>'


def main():
    data = json.loads(DATA.read_text())
    items = data['items']

    filters = ''.join(
        '<button type="button" data-filter="' + esc(f['id']) + '"' +
        (' class="on" aria-pressed="true"' if f['id'] == 'all' else ' aria-pressed="false"') +
        '>' + esc(f['label']) + '</button>'
        for f in data['filters']
    )

    block = (
        '<div class="kc-filter" role="group" aria-label="Filter repairs by type">' + filters + '</div>\n'
        '<div class="kc-grid">\n' + '\n'.join(card(i) for i in items) + '\n</div>\n'
        '<p class="kc-empty" hidden>No repairs of that type here yet.</p>'
    )

    page = PAGE.read_text()
    if START not in page or END not in page:
        print(f'ERROR: markers {START} / {END} not found in {PAGE.name}', file=sys.stderr)
        return 1
    head, rest = page.split(START, 1)
    _, tail = rest.split(END, 1)
    PAGE.write_text(head + START + '\n' + block + '\n' + END + tail)

    missing = []
    for i in items:
        for p in filter(None, [i.get('image'), i.get('before'), i.get('after')]):
            if not (ROOT / p.lstrip('/')).exists():
                missing.append(p)
    pairs = sum(1 for i in items if i.get('before'))
    print(f'{len(items)} cards written ({pairs} sliders, {len(items)-pairs} singles)')
    print('missing image files:', ', '.join(missing) if missing else 'none')
    priced = sum(1 for i in items if i.get('price'))
    print(f'cards showing a price: {priced} of {len(items)}')
    return 1 if missing else 0


if __name__ == '__main__':
    sys.exit(main())
