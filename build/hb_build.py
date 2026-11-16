#!/usr/bin/env python3
"""Generate the 50 Hackbridge service pages, then prove they are not town-swaps.

Hackbridge had no pages at all. The workshop is at Unit 1 Soho Mills on London Road and the site
ranked for nothing in the suburb it physically occupies, which is the largest local gap on it.

The method is surgery on the Carshalton page for the same service rather than a fresh write. The
service content on those pages - what a clutch replacement involves, the signs, the steps, the
parts - is correct, already written and already published, and rewriting it from scratch would
produce worse copy and a different set of facts for no reason. What gets replaced is everything
that is about the town:

    hero          h1, lead, breadcrumb and labels
    local         the whole "<local thing> and what it does to a <service>" section
    travel        deleted outright. There is no journey from Hackbridge to Hackbridge, so the
                  section is replaced with what being on the same road actually gets you.
    faqs          group-specific, from hb_content
    links         the related and area blocks
    head          title, description, canonical, og, JSON-LD areaServed and breadcrumbs

The gate at the end is the point of the file. The existing town pages measure about 69% identical
to each other for the same service, which is the scaled-content pattern that stops them ranking.
Anything generated here has to come in under 62% against every other town's version of the same
service, or the build writes nothing. If these 50 pages were 90% copies of Carshalton's they
would be worse than useless - they would be evidence of templating across the whole site.
"""
import json
import pathlib
import re
import sys
from difflib import SequenceMatcher

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
ROOT = pathlib.Path(__file__).resolve().parent.parent
import hb_content as HB  # noqa: E402

SRC_TOWN, SRC_SLUG = 'Carshalton', 'carshalton'
MAX_SIMILARITY = 0.62
BASE = 'https://www.kithcars.com'

# dent-repair is excluded on purpose. Those 17 pages were rebuilt earlier with a different
# structure and are generated natively by bw_dentrepair from bw_towndata, so Hackbridge's version
# is produced there rather than cut out of a page this script does not understand.
NATIVE = {'dent-repair'}
SERVICES = sorted(p.name[:-len(f'-{SRC_SLUG}.html')] for p in ROOT.glob(f'*-{SRC_SLUG}.html')
                  if p.name[:-len(f'-{SRC_SLUG}.html')] not in NATIVE)


def label_of(block):
    m = re.search(r'<span class="section-label">(.*?)</span>', block, re.S)
    return re.sub(r'<[^>]+>', '', m.group(1)).strip() if m else ''


def visible(html):
    t = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', html, flags=re.S)
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', t)).strip()


def body_text(html):
    i, j = html.find('<main'), html.find('</main>')
    return visible(html[i:j] if i != -1 and j != -1 else html)


def split_sections(main):
    """<section ...>...</section> blocks, which are not nested on these pages."""
    out, pos = [], 0
    for m in re.finditer(r'<section\b', main):
        if m.start() < pos:
            continue
        end = main.find('</section>', m.start())
        if end == -1:
            continue
        end += len('</section>')
        out.append((m.start(), end, main[m.start():end]))
        pos = end
    return out


def service_name(html):
    """The service's display name.

    Taken from the "<Service> for <Town> drivers" section label, not from the h1. The h1s vary
    far more than they look: abs-sensor-replacement leads with "ABS Warning Light", full-service
    with "Full Service for Carshalton Cars", bmw-specialist with "BMW Diesel Specialist for
    Carshalton: EGR". The label is consistent across all 49 and is what the local section has to
    match anyway.
    """
    # [^<]* rather than .*? - with re.S the lazy form starts at the hero's label and swallows the
    # whole page up to the match further down.
    m = re.search(r'<span class="section-label">([^<]*?)\s+for\s+' + SRC_TOWN
                  + r'\s+drivers</span>', html)
    if m:
        return re.sub(r'<[^>]+>', '', m.group(1)).strip()
    h1 = re.sub(r'<[^>]+>', '', re.search(r'<h1[^>]*>(.*?)</h1>', html, re.S).group(1)).strip()
    return re.split(r',| in | &ndash;| from ', re.sub(rf'^{SRC_TOWN}\s+', '', h1))[0].strip()


def price_from_title(html):
    m = re.search(r'<title>.*?(&ndash;|–|-)\s*(From\s*&pound;[\d,]+)', html)
    return m.group(2).replace('&pound;', '£') if m else ''


def build_page(slug):
    src = (ROOT / f'{slug}-{SRC_SLUG}.html').read_text()
    svc = service_name(src)
    heading, local_html = HB.local_section(slug, svc)

    i, j = src.find('<main'), src.find('</main>')
    head, main, tail = src[:i], src[i:j], src[j:]

    secs = split_sections(main)
    rebuilt, replaced = main, {'local': 0, 'travel': 0, 'faq': 0}

    for _, _, block in secs:
        h2 = re.search(r'<h2[^>]*>(.*?)</h2>', block, re.S)
        h2txt = re.sub(r'<[^>]+>', '', h2.group(1)) if h2 else ''
        label = label_of(block)

        # The section-label is the only reliable discriminator: "for <Town> drivers" also appears
        # as a link inside the travel section, which is how the first attempt replaced the wrong
        # block three times and left the travel copy in place.

        # --- the local-character section -----------------------------------------------------
        if label == f'{svc} for {SRC_TOWN} drivers':
            new = (f'<section class="section section-alt"><div class="container">'
                   f'<div class="kx-split"><article class="kx-prose">'
                   f'<span class="section-label">{svc} for {HB.NAME} drivers</span>'
                   f'<h2>{heading}</h2>{local_html}{HB.extra_for(slug)}'
                   f'</article></div></div></section>')
            ch, cb = HB.common_section(slug)
            new += (f'<section class="section"><div class="container kx-narrow">'
                    f'<h2>{ch}</h2><div class="kx-prose">{cb}</div></div></section>')
            rebuilt = rebuilt.replace(block, new, 1)
            replaced['local'] += 1
            continue

        # --- the travel section, which makes no sense from Hackbridge ------------------------
        if label == f'Getting here from {SRC_TOWN}':
            new = (f'<section class="section"><div class="container kx-narrow">'
                   f'<span class="section-label">Finding us</span>'
                   f'<h2>{HB.HERE_HEADING}</h2>'
                   f'<div class="kx-prose">{HB.HERE.strip()}</div>'
                   f'<p style="margin-top:1rem"><a class="btn btn-outline" '
                   f'href="https://www.google.com/maps/dir/?api=1&amp;destination='
                   f'KITH+Cars%2C+Soho+Mills%2C+London+Road%2C+Hackbridge+SM6+7HN" '
                   f'target="_blank" rel="noopener">Open in Maps</a></p>'
                   f'</div></section>')
            rebuilt = rebuilt.replace(block, new, 1)
            replaced['travel'] += 1
            continue

        # --- the FAQs ------------------------------------------------------------------------
        if label == 'Questions' and 'your questions answered' in h2txt:
            items = ''.join(
                f'<details class="kx-faq"{" open" if n == 0 else ""}><summary><h3>{q}</h3>'
                f'</summary><p>{a}</p></details>'
                for n, (q, a) in enumerate(HB.faqs(slug)))
            new = (f'<section class="section section-alt"><div class="container kx-narrow">'
                   f'<span class="section-label">Questions</span>'
                   f'<h2>{svc} in {HB.NAME}: your questions answered</h2>'
                   f'<div class="kx-faqs">{items}</div></div></section>')
            rebuilt = rebuilt.replace(block, new, 1)
            replaced['faq'] += 1
            continue

        # --- the extra "what we see from <Town>" block some services carry -------------------
        if h2txt.strip() == f'What we actually see from {SRC_TOWN}':
            new = (f'<section class="section"><div class="container kx-narrow">'
                   f'<h2>What we actually see from {HB.NAME}</h2>'
                   f'<div class="kx-prose">{HB.SEEN.strip()}</div></div></section>')
            rebuilt = rebuilt.replace(block, new, 1)
            replaced['seen'] = replaced.get('seen', 0) + 1

    html = head + rebuilt + tail

    # --- hero copy ---------------------------------------------------------------------------
    price = price_from_title(src)
    html = re.sub(r'(<h1[^>]*>).*?(</h1>)',
                  lambda m: f'{m.group(1)}{svc} in {HB.NAME}, SM6{m.group(2)}', html, count=1,
                  flags=re.S)
    html = re.sub(r'(<p class="lead">).*?(</p>)',
                  lambda m: m.group(1) + HB.lead(slug, svc, price) + m.group(2), html,
                  count=1, flags=re.S)
    # "~5 min from <Town>" is meaningless when the town is where we are.
    html = re.sub(r'<li>~?\s*\d+\s*min(utes)? from [^<]*</li>',
                  '<li>On London Road, SM6 &mdash; walk in</li>', html, count=1)

    # --- the JSON-LD graph -------------------------------------------------------------------
    def fix_schema(m):
        try:
            d = json.loads(m.group(1))
        except Exception:
            return m.group(0)
        for node in d.get('@graph', [d]):
            if 'areaServed' in node:
                node['areaServed'] = {
                    '@type': 'Place', 'name': f'{HB.NAME}, London',
                    'address': {'@type': 'PostalAddress', 'addressLocality': HB.NAME,
                                'postalCode': HB.PC, 'addressCountry': 'GB'}}
            if node.get('@type') == 'FAQPage':
                node['mainEntity'] = [
                    {'@type': 'Question', 'name': re.sub(r'<[^>]+>', '', q),
                     'acceptedAnswer': {'@type': 'Answer',
                                        'text': re.sub(r'<[^>]+>', '', a)}}
                    for q, a in HB.faqs(slug)]
            if node.get('@type') == 'BreadcrumbList':
                for el in node.get('itemListElement', []):
                    if isinstance(el.get('name'), str):
                        el['name'] = el['name'].replace(SRC_TOWN, HB.NAME)
                    if isinstance(el.get('item'), str):
                        el['item'] = el['item'].replace(SRC_SLUG, HB.SLUG)
        return ('<script type="application/ld+json">'
                + json.dumps(d, ensure_ascii=False) + '</script>')

    html = re.sub(r'<script type="application/ld\+json">(.*?)</script>', fix_schema, html,
                  flags=re.S)

    # --- head and any remaining town references ----------------------------------------------
    title = f'{svc} {HB.NAME} SM6{" – " + price if price else ""} | KITH Cars'
    html = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', html, count=1, flags=re.S)
    desc = (f'{svc} in {HB.NAME} SM6 at our own workshop on London Road &mdash; not a drive away, '
            f'the garage in the village. '
            f'{price + ". " if price else ""}Walk in, or book online in about 30 seconds.')
    html = re.sub(r'(<meta name="description" content=")(.*?)(")',
                  lambda m: m.group(1) + desc + m.group(3), html, count=1, flags=re.S)
    html = re.sub(r'(property="og:title" content=")(.*?)(")',
                  lambda m: m.group(1) + f'{svc} in {HB.NAME}, SM6' + m.group(3), html,
                  count=1, flags=re.S)
    html = re.sub(r'(property="og:description" content=")(.*?)(")',
                  lambda m: m.group(1) + desc + m.group(3), html, count=1, flags=re.S)

    # Slugs first, then prose mentions, so URLs do not get half-rewritten.
    html = html.replace(f'{slug}-{SRC_SLUG}', f'{slug}-{HB.SLUG}')
    html = html.replace(f'/{SRC_SLUG}"', f'/{HB.SLUG}"')
    html = html.replace(SRC_TOWN, HB.NAME).replace(SRC_SLUG, HB.SLUG)
    html = re.sub(r'\bSM5\b', HB.PC, html)
    # "five minutes from Hackbridge" and friends are nonsense on a Hackbridge page.
    html = re.sub(r',?\s*(just )?(five|5|ten|10) minutes from Hackbridge', '', html,
                  flags=re.I)
    html = re.sub(r'\bminutes (away )?in Hackbridge\b', 'here in Hackbridge', html, flags=re.I)

    return html, replaced


def main():
    write = '--write' in sys.argv
    pages, problems = {}, []

    for slug in SERVICES:
        try:
            html, rep = build_page(slug)
        except Exception as exc:
            problems.append(f'{slug}: failed to build ({exc})')
            continue
        for k, n in rep.items():
            # 'seen' is optional - only the bodywork services carry that block.
            if n != 1 and not (k == 'seen' and n == 0):
                problems.append(f'{slug}: replaced {n} {k} sections, expected 1')
        pages[slug] = html

    print(f'pages built: {len(pages)} of {len(SERVICES)}')

    # --- no stray source-town references -----------------------------------------------------
    for slug, html in pages.items():
        if re.search(rf'\b{SRC_TOWN}\b', html) or f'{SRC_SLUG}' in html:
            problems.append(f'{slug}: still mentions {SRC_TOWN}')
        # "a couple of minutes from Hackbridge station" is true and wanted. What must not
        # survive is the travel-to-Hackbridge phrasing the source pages open with.
        if re.search(r'(\d+|five|ten|couple of)\s+minutes?\s+(away\s+)?(from|to)\s+Hackbridge'
                     r'(?!\s+station)', html, re.I):
            problems.append(f'{slug}: still claims to be minutes from Hackbridge')

    # --- schema parses -----------------------------------------------------------------------
    for slug, html in pages.items():
        for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
            try:
                json.loads(m.group(1))
            except Exception as exc:
                problems.append(f'{slug}: JSON-LD will not parse ({exc})')

    # --- the gate: against every other town's version of the same service --------------------
    # Hackbridge itself is excluded, or every page is compared against the copy of itself this
    # script wrote on the previous run and scores 100%.
    towns = sorted({p.name.rsplit('-', 1)[1][:-5]
                    for p in ROOT.glob('accident-repairs-*.html')} - {HB.SLUG})
    worst = (0.0, '', '')
    for slug, html in pages.items():
        mine = body_text(html).split()
        for t in towns:
            other = ROOT / f'{slug}-{t}.html'
            if not other.exists():
                continue
            r = SequenceMatcher(None, mine, body_text(other.read_text()).split()).ratio()
            if r > worst[0]:
                worst = (r, f'{slug}-hackbridge', f'{slug}-{t}')
            if r > MAX_SIMILARITY:
                problems.append(f'too similar ({r*100:.0f}%): {slug}-hackbridge / {slug}-{t}')

    words = {s: len(body_text(h).split()) for s, h in pages.items()}
    if words:
        print(f'  words       : {min(words.values())} min, '
              f'{sum(words.values())//len(words)} mean, {max(words.values())} max')
    print(f'  most alike  : {worst[0]*100:.0f}%  ({worst[1]} / {worst[2]})')

    if problems:
        print(f'\nPROBLEMS ({len(problems)}):')
        for x in problems[:20]:
            print('  ' + x)
        return 1

    if not write:
        print('\nclean, but --write not given: nothing written')
        return 0
    for slug, html in pages.items():
        (ROOT / f'{slug}-{HB.SLUG}.html').write_text(html)
    print(f'\nclean: {len(pages)} Hackbridge pages written, '
          f'none above {MAX_SIMILARITY*100:.0f}% alike to another town')
    return 0


if __name__ == '__main__':
    sys.exit(main())
