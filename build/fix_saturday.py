#!/usr/bin/env python3
"""Correct the Saturday closing time wherever a page says we are open until 8pm on a Saturday.

We close at 5pm on Saturday. Most of the site already says so - 1,053 pages carry the correct
opening hours in their structured data and there are over two thousand correct "Sat 8am-5pm"
lines. The error is narrower than it looked and sits in two places:

  prose        52 pages say things like "open 8am to 8pm Monday to Saturday" or "open until 8pm
               Monday to Saturday", usually twice over - once in the visible FAQ answer and once
               in the JSON-LD copy of the same answer. Both are fixed, because the structured
               copy is what an assistant reads out.
  schema        6 blog pages list Saturday inside the Monday-to-Friday 20:00 group rather than
               in its own 17:00 one.

Phrases that are already correct are left alone. "Monday to Friday 8am to 8pm and Saturday 8am to
5pm" is right and appears on most of the site; a blunt find-and-replace on "8pm" would have
broken all of it, which is why every pattern here names Saturday explicitly.

Wrong opening hours are worth fixing carefully rather than quickly: somebody driving across
London at six on a Saturday evening because a page said we were open is a worse outcome than any
ranking problem.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Longest first, so a broader pattern cannot eat a more specific one.
PROSE = [
    (r'open 8am to 8pm,? Monday to Saturday',
     'open 8am to 8pm Monday to Friday and 8am to 5pm on Saturday'),
    (r'8am to 8pm,? Monday to Saturday',
     '8am to 8pm Monday to Friday and 8am to 5pm on Saturday'),
    (r'8am&ndash;8pm,? Monday to Saturday',
     '8am&ndash;8pm Monday to Friday and 8am&ndash;5pm on Saturday'),
    (r'open until 8pm,? Monday to Saturday',
     'open until 8pm Monday to Friday and until 5pm on Saturday'),
    (r'until 8pm,? Monday to Saturday',
     'until 8pm Monday to Friday and until 5pm on Saturday'),
    (r'8am to 8pm,? six days a week',
     '8am to 8pm Monday to Friday and 8am to 5pm on Saturday'),
    (r'until 8pm,? six days a week',
     'until 8pm Monday to Friday and until 5pm on Saturday'),
    (r'up to 8pm,? Monday to Saturday',
     'up to 8pm Monday to Friday and 5pm on Saturday'),
    (r'close at 8pm,? Monday to Saturday',
     'close at 8pm Monday to Friday and 5pm on Saturday'),
    (r'Saturdays and evenings up to 8pm',
     'weekday evenings up to 8pm and Saturdays until 5pm'),
    (r'Open 8am to 8pm,? six days', 'Open 8am to 8pm weekdays, 5pm Saturdays'),
    (r'Open until 8pm,? six days', 'Open until 8pm weekdays, 5pm Saturdays'),
    (r'Open 8am to 8pm,? Saturdays too', 'Open to 8pm weekdays, 5pm Saturdays'),
    (r'8am to 8pm,? six days\.', '8am to 8pm weekdays and 8am to 5pm Saturdays.'),
    (r'running to 8pm six days a week',
     'running to 8pm on weekdays and to 5pm on Saturdays'),
    (r'open until 8pm on weekdays and Saturdays',
     'open until 8pm on weekdays and until 5pm on Saturdays'),
    (r"open until 8pm on Saturdays as well as weekdays",
     "open until 8pm on weekdays and until 5pm on Saturdays"),
    (r'Long opening hours six days a week', 'Long opening hours, six days a week'),
    (r'collected up to 8pm,? six days a week',
     'collected up to 8pm on weekdays and up to 5pm on Saturdays'),
    (r'up to 8pm,? six days a week',
     'up to 8pm on weekdays and up to 5pm on Saturdays'),
    (r'Saturday opening until 8pm', 'Saturday opening until 5pm'),
    (r'open 8am to 8pm on a Saturday', 'open 8am to 5pm on a Saturday'),
]

# Anything matching this after the pass is still claiming Saturday evening opening.
STILL_WRONG = re.compile(
    r'8pm[^.<]{0,40}(Saturday|six days|every day|seven days)'
    r'|Saturday[^.<]{0,40}(until|to)\s*8pm', re.I)


def fix_schema(html):
    """Move Saturday out of any opening-hours group that closes at 20:00."""
    def one(m):
        try:
            d = json.loads(m.group(1))
        except Exception:
            return m.group(0)
        changed = False
        for node in d.get('@graph', [d]):
            spec = node.get('openingHoursSpecification')
            if not isinstance(spec, list):
                continue
            out = []
            for s in spec:
                days = s.get('dayOfWeek')
                if (isinstance(days, list) and 'Saturday' in days
                        and len(days) > 1 and s.get('closes') == '20:00'):
                    weekdays = [x for x in days if x != 'Saturday']
                    out.append({**s, 'dayOfWeek': weekdays})
                    out.append({'@type': 'OpeningHoursSpecification',
                                'dayOfWeek': ['Saturday'],
                                'opens': s.get('opens', '08:00'), 'closes': '17:00'})
                    changed = True
                else:
                    out.append(s)
            if changed:
                node['openingHoursSpecification'] = out
        if not changed:
            return m.group(0)
        return ('<script type="application/ld+json">'
                + json.dumps(d, ensure_ascii=False) + '</script>')

    return re.sub(r'<script type="application/ld\+json">(.*?)</script>', one, html, flags=re.S)


def main():
    prose_pages = schema_pages = 0
    replacements = 0
    for f in sorted(ROOT.glob('*.html')):
        html = original = f.read_text()
        if '<html' not in html:
            continue
        before = html
        for pat, rep in PROSE:
            html, n = re.subn(pat, rep, html, flags=re.I)
            replacements += n
        if html != before:
            prose_pages += 1
        after_schema = fix_schema(html)
        if after_schema != html:
            schema_pages += 1
        html = after_schema
        if html != original:
            f.write_text(html)

    print(f'prose:  {replacements} phrases fixed across {prose_pages} pages')
    print(f'schema: {schema_pages} pages had Saturday in the weekday group')

    # --- verify ------------------------------------------------------------------------------
    bad_prose, bad_schema = [], []
    for f in sorted(ROOT.glob('*.html')):
        html = f.read_text()
        if '<html' not in html:
            continue
        for m in STILL_WRONG.finditer(html):
            seg = html[max(0, m.start() - 70):m.end() + 40]
            # "8pm Monday to Friday and until 5pm on Saturday" is correct and will match the
            # loose pattern above, so accept anything that names Friday before Saturday.
            # Correct copy either names Friday/weekdays, or states the 5pm Saturday beside it.
            if re.search(r'Friday|weekday', seg, re.I) or re.search(r'5pm', seg):
                continue
            bad_prose.append(f'{f.name}: ...{seg.strip()[-100:]}...')
        for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
            try:
                d = json.loads(m.group(1))
            except Exception:
                bad_schema.append(f'{f.name}: JSON-LD will not parse')
                continue
            for node in d.get('@graph', [d]):
                for s in node.get('openingHoursSpecification', []) or []:
                    days = s.get('dayOfWeek') or []
                    if 'Saturday' in days and s.get('closes') != '17:00':
                        bad_schema.append(f'{f.name}: Saturday closes {s.get("closes")}')

    print(f'\nremaining prose problems : {len(bad_prose)}')
    for b in bad_prose[:8]:
        print('  ' + b)
    print(f'remaining schema problems: {len(bad_schema)}')
    for b in bad_schema[:8]:
        print('  ' + b)
    return 1 if (bad_prose or bad_schema) else 0


if __name__ == '__main__':
    sys.exit(main())
