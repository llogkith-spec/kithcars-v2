#!/usr/bin/env python3
"""Stop the full-service pages promising a cabin filter.

A customer read the full service's contents off the website and it listed a cabin filter. The
rate card prices the pollen filter into the MAJOR service only, so the page was selling a part
KITH does not fit at that level and is not paid for. The customer had it in writing and was
entitled to it.

Two kinds of mention, handled differently:

  A promise — "air filter and cabin filter replaced", "Cabin filter in the particle or activated
  carbon type your car was built with" — is wrong and comes out, or moves to naming the major
  service as where it happens.

  An explanation — why a saturated cabin filter smells, why it slows the demister — is true and
  useful, but on a full-service page it implies inclusion by sitting there. Those are reworded
  to say which service renews it rather than deleted, because the information sells the major.

build/promisesaudit.py checks the structured lists; this handles the prose, which no schema
covers.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

SCOPE = re.compile(r'^(full-service|car-servicing|interim-service)', re.I)

SUBS = [
    # Direct promises on the full service.
    ('Engine oil, oil filter, air filter and cabin filter replaced',
     'Engine oil, oil filter and air filter replaced'),
    ('<li>Cabin filter in the particle or activated carbon type your car was built with</li>',
     ''),
    # The interim-versus-full answer named the wrong filter.
    ('they do not renew the air and cabin filters or include the wheels-off measurements',
     'they do not renew the air filter or include the wheels-off measurements'),
    # Why it takes as long as it does: the cabin filter is not part of this job.
    ('It runs longer on cars where the cabin filter sits behind the glovebox or under the '
     'scuttle panel, and where seized wheel bolts hold up the brake measurements',
     'It runs longer where seized wheel bolts hold up the brake measurements'),
    # Explanations that now say where the work actually happens.
    ('A saturated cabin filter holds damp against the heater matrix and slows airflow, so the '
     'screen takes longer to clear and the car smells',
     'A saturated cabin filter holds damp against the heater matrix and slows airflow, so the '
     'screen takes longer to clear and the car smells. We renew it on the major service, and '
     'separately any time you ask'),
    ('Both are renewed as part of the',
     'The air filter is renewed as part of the'),
    ('The air filter and cabin filter that come with a full service take the brunt of it',
     'The air filter that comes with a full service takes the brunt of it, and the cabin '
     'filter can be added'),
    ('The cabin filter protects you, and when it saturates you get a slow blower',
     'The cabin filter protects you — it comes with the major service, or as an add-on to this '
     'one — and when it saturates you get a slow blower'),
    ('A full service renews it along with the air filter.',
     'A full service renews the air filter; the cabin filter comes with the major service, or '
     'as an add-on here.'),
    # Bespoke sentences on individual area pages, each written as though the full service
    # renews the cabin filter. Reworded to name the major, or to drop the claim.
    ('We renew the engine oil and oil filter, the air filter and the cabin filter in the type '
     'the car was built with',
     'We renew the engine oil and oil filter and the air filter'),
    ('Engine oil and oil filter, air filter and cabin filter are renewed',
     'Engine oil and oil filter and the air filter are renewed'),
    ('A full service renews both, and we fit a cabin filter in the particle or carbon type '
     'the car was built with',
     'A full service renews the air filter; the cabin filter is part of the major service, or '
     'an add-on to this one'),
    ('A full service renews both, and we fit a cabin filter in the particle o',
     'A full service renews the air filter, and the cabin filter is an add-on o'),
    ('Both are part of the full service, and we fit the cabin filter in the particle or carbon '
     'type the car was built with',
     'The air filter is part of the full service; the cabin filter comes with the major, or can '
     'be added to this one'),
    ('engine oil and oil filter, air filter, cabin filter, coolant strength',
     'engine oil and oil filter, air filter, coolant strength'),
    ('That combination is hard on the parts a full service renews. Cabin filters hold moisture '
     'and leaf debris',
     'That combination is hard on the parts a service renews. Cabin filters hold moisture and '
     'leaf debris'),
    ('A saturated cabin filter carries damp and smells into the car and slows the demister',
     'A saturated cabin filter carries damp and smells into the car and slows the demister, '
     'which is why it is renewed on the major service'),
]


def main():
    pages = sorted(p for p in ROOT.glob('*.html') if SCOPE.match(p.name))
    print(f'pages in scope: {len(pages)}')
    hits, changed = {}, 0
    for p in pages:
        t = s = p.read_text()
        for old, new in SUBS:
            if old in t:
                hits[old[:52]] = hits.get(old[:52], 0) + t.count(old)
                t = t.replace(old, new)
        if t != s:
            p.write_text(t)
            changed += 1
    print(f'rewritten: {changed}')
    for k, v in sorted(hits.items(), key=lambda x: -x[1]):
        print(f'  x{v:<4} {k}…')

    # Nothing in scope may still put a cabin filter inside the full service's contents, and the
    # JSON-LD FAQ answers these sentences also live in must still parse.
    bad, broken = [], []
    for p in pages:
        t = p.read_text()
        for m in re.finditer(r'[^<>]{0,200}cabin filters?[^<>]{0,200}', t, re.I):
            s = re.sub(r'\s+', ' ', m.group(0))
            # The claim only counts when the CABIN filter is its subject. A paragraph can
            # mention both filters and promise only the air one, which is now the correct
            # wording on several of these pages — matching on proximity alone flagged those.
            promise = (
                re.search(r'cabin filters?[^.]{0,60}?\b(is|are)\b[^.]{0,30}?'
                          r'(renewed|replaced|included|part of (the )?(full )?service)', s, re.I)
                or re.search(r'(full service (renews|includes)|part of the full service)'
                             r'[^.]{0,40}?cabin filter', s, re.I)
                or re.search(r'air filter and (the |a )?cabin filter[^.]{0,40}?'
                             r'(renew|replac|come|are part)', s, re.I)
                or re.search(r'we fit (a|the) cabin filter', s, re.I)
            )
            if promise and not re.search(r'\bmajor\b|add-on|add(ed)? to this|can be added', s, re.I):
                bad.append(f'{p.name}: …{s.strip()[:110]}…')
        for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
            try:
                json.loads(b)
            except Exception as e:
                broken.append(f'{p.name}: {e}')
    if bad:
        print(f'\nSTILL IMPLYING INCLUSION ({len(bad)}):')
        for x in bad[:8]:
            print('  ' + x)
    if broken:
        print('BROKEN JSON-LD:', broken[:4])
    if bad or broken:
        sys.exit(1)
    print('clean: no page in scope promises a cabin filter outside the major service')


if __name__ == '__main__':
    main()
