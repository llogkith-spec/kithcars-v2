#!/usr/bin/env python3
"""Render a bodywork page that is indistinguishable from the hand-built ones.

The chrome - the head links, the header, the quote section and the footer - is sliced out of a
real page on the site at build time rather than copied into this file as a string. That matters:
the header has been changed four times this month, and a template with its own frozen copy would
have quietly drifted from the rest of the site by the second change. Slicing it means these pages
inherit whatever the donor page currently has, including any future change.

The donor is bumper-repair-croydon.html, chosen because it is an ordinary bodywork page with
every piece of chrome present: breadcrumbs, the trust list, the quote widget set to the bodywork
flow, and the full four-node JSON-LD graph.
"""
import html
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
DONOR = ROOT / 'bumper-repair-croydon.html'
BASE = 'https://www.kithcars.com'


def _donor():
    return DONOR.read_text()


def chrome():
    """The parts of a page that every page shares, taken from the donor."""
    t = _donor()

    # head: from the font preconnect to </head>, with the donor's own JSON-LD removed
    h0 = t.find('<link rel="preconnect"')
    h1 = t.find('</head>')
    head_tail = re.sub(r'<script type="application/ld\+json">.*?</script>\s*', '', t[h0:h1], flags=re.S)

    # header: the whole element, plus the <main> that follows it
    g0 = t.find('<header')
    g1 = t.find('</header>') + len('</header>')
    header = t[g0:g1]

    # footer: from <footer> to the end of the document
    f0 = t.find('<footer')
    footer = t[f0:]

    return {'head_tail': head_tail.strip(), 'header': header, 'footer': footer}


CH = chrome()


def esc(s):
    return html.escape(s, quote=True)


def _para(block):
    """A content block: a string is a paragraph, a list is a bulleted list, a tuple is a note."""
    if isinstance(block, list):
        return '<ul class="kx-list">' + ''.join(f'<li>{b}</li>' for b in block) + '</ul>'
    if isinstance(block, tuple):
        kind, body = block
        if kind == 'note':
            return f'<div class="kx-note"><p>{body}</p></div>'
        if kind == 'steps':
            return '<ol class="kx-steps">' + ''.join(f'<li>{b}</li>' for b in body) + '</ol>'
        if kind == 'table':
            head, rows = body
            th = ''.join(f'<th>{c}</th>' for c in head)
            tr = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)
            return f'<div class="kx-table-wrap"><table class="kx-table"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'
    return f'<p>{block}</p>'


def _sections(sections):
    out = []
    for i, (heading, blocks) in enumerate(sections):
        cls = 'section section-alt' if i % 2 == 0 else 'section'
        body = ''.join(_para(b) for b in blocks)
        out.append(f'<section class="{cls}"><div class="container kx-prose">'
                   f'<h2>{heading}</h2>{body}</div></section>')
    return '\n'.join(out)


def _faq_html(faqs):
    # The markup kx.css expects: an h3 inside the summary, the answer as a sibling p.
    items = ''.join(
        f'<details class="kx-faq"><summary><h3>{q}</h3></summary><p>{a}</p></details>'
        for q, a in faqs)
    return ('<section class="section section-alt"><div class="container kx-prose">'
            f'<h2>Your questions answered</h2><div class="kx-faqs">{items}</div></div></section>')


def _quote_html(page):
    job = page.get('job', 'panel-front-bumper')
    flow = page.get('flow', 'bodywork')
    return ('<section class="section" id="get-a-quote"><div class="container">'
            '<div style="text-align:center;margin-bottom:2rem">'
            '<span class="section-label">Instant quote</span>'
            f'<h2>{page.get("quote_heading", "Price this job now")}</h2>'
            '<p class="lead" style="margin-top:.75rem;margin-inline:auto">Put your registration '
            'in and we will price it. Prefer to talk? Call '
            '<a href="tel:02046299469">020 4629 9469</a> or '
            '<a href="https://wa.me/447923688259" target="_blank" rel="noopener">WhatsApp us</a>.</p></div>'
            f'<div id="kq" data-flow="{flow}" data-job="{job}">'
            '<div class="kq-loading"><span class="kq-spin"></span>Loading instant quote&hellip;</div>'
            '</div></div></section>')


def _related_html(related):
    if not related:
        return ''
    links = ' &middot; '.join(f'<a href="/{s}">{t}</a>' for s, t in related)
    return ('<section class="section section-alt"><div class="container kx-prose">'
            f'<h2>Related guides</h2><p>{links}</p></div></section>')


def _crumbs(page):
    parts = ['<a href="/">Home</a>']
    for name, href in page['crumbs'][:-1]:
        parts.append(f'<a href="/{href}">{name}</a>')
    parts.append(f'<span aria-current="page">{page["crumbs"][-1][0]}</span>')
    return '<nav class="kx-crumbs" aria-label="Breadcrumb">' + '<span>&rsaquo;</span>'.join(parts) + '</nav>'


def _schema(page):
    url = f'{BASE}/{page["slug"]}'
    business = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',
                                    _donor(), re.S).group(1))['@graph'][0]
    graph = [business]

    graph.append({
        '@type': 'Service',
        '@id': url + '#service',
        'name': page['h1'],
        'serviceType': page.get('service_type', 'Vehicle body repair'),
        'description': page['desc'],
        'provider': {'@id': f'{BASE}/#business'},
        'areaServed': {'@type': 'Place', 'name': 'South London and Surrey'},
    })

    if page.get('faqs'):
        graph.append({
            '@type': 'FAQPage',
            '@id': url + '#faq',
            'mainEntity': [
                {'@type': 'Question', 'name': re.sub(r'<[^>]+>', '', q),
                 'acceptedAnswer': {'@type': 'Answer', 'text': re.sub(r'<[^>]+>', '', a)}}
                for q, a in page['faqs']],
        })

    crumbs = [{'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': BASE + '/'}]
    for i, (name, href) in enumerate(page['crumbs'], start=2):
        crumbs.append({'@type': 'ListItem', 'position': i, 'name': name,
                       'item': f'{BASE}/{href}' if href else url})
    graph.append({'@type': 'BreadcrumbList', 'itemListElement': crumbs})

    return ('<script type="application/ld+json">'
            + json.dumps({'@context': 'https://schema.org', '@graph': graph},
                         ensure_ascii=False, separators=(',', ':'))
            + '</script>')


def render(page):
    url = f'{BASE}/{page["slug"]}'
    trust = page.get('trust', [
        '★★★★★ 4.9/5 from 193 Google reviews',
        'Hackbridge SM6 7HN',
        'Any insurer &middot; your choice of repairer',
    ])
    trust_html = '<ul class="kx-trust">' + ''.join(f'<li>{t}</li>' for t in trust) + '</ul>'

    # The second column of page-hero-grid. The donor puts a workshop photo here, which works on a
    # service page but would mean the same stock image on all 800 of these. A short answer card
    # is both unique to the page and more use to someone who arrived from a search looking for
    # one specific fact.
    if page.get('key_points'):
        aside = ('<aside class="kx-keycard"><h2>The short answer</h2><ul>'
                 + ''.join(f'<li>{k}</li>' for k in page['key_points'])
                 + '</ul></aside>')
    else:
        aside = ('<div class="page-hero-img"><picture><source srcset="/22.webp" type="image/webp"/>'
                 '<img src="/22.jpg" alt="Panel masked and prepared for paint in the bodyshop at '
                 'KITH Cars Garage &amp; Bodyworks, Hackbridge" width="800" height="1000" '
                 'loading="eager"/></picture></div>')

    hero = ('<section class="page-hero"><div class="container page-hero-grid"><div>'
            + _crumbs(page)
            + f'<span class="section-label">{page["label"]}</span>'
            + f'<h1>{page["h1"]}</h1>'
            + f'<p class="lead">{page["lead"]}</p>'
            + '<div class="page-hero-actions" style="margin-top:2rem">'
              '<a class="btn btn-primary" href="#get-a-quote">Get an instant price</a>'
              '<a class="btn btn-outline" href="tel:02046299469">Call 020 4629 9469</a></div>'
            + trust_html
            + '</div>' + aside + '</div></section>')

    body = '\n'.join(x for x in [
        hero,
        _sections(page['sections']),
        _quote_html(page),
        _faq_html(page['faqs']) if page.get('faqs') else '',
        _related_html(page.get('related')),
    ] if x)

    return (
        '<!DOCTYPE html>\n<html lang="en-GB">\n<head>\n'
        '<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>\n'
        f'<title>{esc(page["title"])}</title>\n'
        f'<meta name="description" content="{esc(page["desc"])}"/>\n'
        '<meta name="robots" content="index,follow,max-image-preview:large"/>\n'
        f'<link rel="canonical" href="{url}"/>\n'
        '<meta property="og:type" content="article"/>'
        '<meta property="og:site_name" content="KITH Cars Garage &amp; Bodyworks"/>'
        '<meta property="og:locale" content="en_GB"/>\n'
        f'<meta property="og:title" content="{esc(page["h1"])}"/>\n'
        f'<meta property="og:description" content="{esc(page["desc"])}"/>\n'
        f'<meta property="og:url" content="{url}"/>\n'
        '<meta property="og:image" content="https://www.kithcars.com/22.jpg"/>\n'
        '<meta name="twitter:card" content="summary_large_image"/>\n'
        '<meta name="geo.region" content="GB-LND"/>\n'
        + CH['head_tail'] + '\n'
        + _schema(page) + '\n'
        '</head>\n<body>\n'
        + CH['header'] + '\n<main>\n'
        + body
        + '\n</main>\n'
        + CH['footer']
    )
