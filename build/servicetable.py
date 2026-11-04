#!/usr/bin/env python3
"""Render the "what's included in each service" table onto the servicing pages.

Run from the repo root:  python3 build/servicetable.py

The three services were described as three prose lists, which is fine to read and useless to
compare: a customer deciding between a full and a major has to hold both lists in their head.
The table puts the same rows side by side, which is how everyone else in the market presents it
and how the customer is already thinking about it.

The rows come from quote-catalogue.json so the table and the quote widget cannot drift apart.
"""
import json, pathlib, sys, html

ROOT = pathlib.Path.cwd()
CAT = ROOT / 'quote-catalogue.json'
START = '<!-- KC-SERVICETABLE:start -->'
END = '<!-- KC-SERVICETABLE:end -->'

PAGES = ['car-servicing.html', 'full-service.html', 'interim-service.html', 'major-service.html',
         'pricing.html', 'mechanical.html']


def esc(s):
    return html.escape(str(s), quote=True)


def table(cat):
    m = cat.get('service_matrix')
    if not m:
        return None
    cols = m['columns']

    head = ('<tr><th scope="col">What you get</th>' +
            ''.join('<th scope="col">' + esc(c['label']) + '</th>' for c in cols) + '</tr>')

    meta = (
        '<tr class="kc-st-meta"><th scope="row">How often</th>' +
        ''.join('<td>' + esc(c['interval']) + '</td>' for c in cols) + '</tr>'
        '<tr class="kc-st-meta"><th scope="row">Inspection</th>' +
        ''.join('<td>' + esc(c['checks']) + '</td>' for c in cols) + '</tr>'
    )

    body = ''
    for g in m['groups']:
        body += ('<tr class="kc-st-group"><th scope="rowgroup" colspan="' + str(len(cols) + 1) + '">' +
                 esc(g['label']) + '</th></tr>')
        for row in g['rows']:
            cells = ''
            for c in cols:
                yes = c['id'] in row['in']
                cells += ('<td class="' + ('kc-yes' if yes else 'kc-no') + '">' +
                          ('<span aria-hidden="true">&#10003;</span><span class="kc-sr">Included</span>'
                           if yes else
                           '<span aria-hidden="true">&ndash;</span><span class="kc-sr">Not included</span>') +
                          '</td>')
            body += '<tr><th scope="row">' + esc(row['label']) + '</th>' + cells + '</tr>'

    return (
        '<div class="kc-servicetable">'
        '<h2>What is included in each service</h2>'
        '<p class="kc-st-lead">The same rows for all three, so you can see exactly what the extra '
        'money buys. Oil grade, plugs and filters are always to your own vehicle manufacturer&rsquo;s '
        'specification &mdash; we do not fit a generic service kit and call it a service.</p>'
        '<div class="kc-st-scroll"><table class="kc-st">'
        '<thead>' + head + '</thead><tbody>' + meta + body + '</tbody></table></div>'
        '<p class="kc-st-foot">Anything we find is written down and priced before it is done, and '
        'you decide. Nothing is replaced without asking you first.</p>'
        '</div>'
    )


def insert(path, block):
    p = ROOT / path
    if not p.exists():
        return f'{path}: not on disk, skipped'
    s = p.read_text()

    if START in s and END in s:
        head, rest = s.split(START, 1)
        _, tail = rest.split(END, 1)
        p.write_text(head + START + block + END + tail)
        return f'{path}: table refreshed'

    # First time: put it just before the FAQ section if there is one, else before </main>.
    marker = s.find('<section class="section section-alt"><div class="container kx-narrow" id="faq"')
    if marker == -1:
        marker = s.find('</main>')
    if marker == -1:
        return f'{path}: nowhere obvious to put it, SKIPPED'
    wrapped = ('<section class="section"><div class="container kx-narrow">' +
               START + block + END + '</div></section>\n')
    p.write_text(s[:marker] + wrapped + s[marker:])
    return f'{path}: table added'


def main():
    cat = json.loads(CAT.read_text())
    block = table(cat)
    if not block:
        print('no service_matrix in the catalogue', file=sys.stderr)
        return 1
    targets = sys.argv[1:] or PAGES
    for t in targets:
        print(' ', insert(t, block))
    rows = sum(len(g['rows']) for g in cat['service_matrix']['groups'])
    print(f'\n{rows} rows across {len(cat["service_matrix"]["groups"])} groups')
    return 0


if __name__ == '__main__':
    sys.exit(main())
