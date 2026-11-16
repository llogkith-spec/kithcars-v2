#!/usr/bin/env python3
"""Build /hackbridge, the town landing page, and put Hackbridge in the site-wide footer list.

The 49 generated service pages link to /hackbridge, so without this they point at a 404. The
page is cut from /carshalton the same way the service pages are, with every section that is about
getting here replaced, because there is no journey from Hackbridge to Hackbridge.

The footer "Serving ..." list appears on about a thousand pages and did not include the place the
workshop is in, which is the same gap in miniature.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
ROOT = pathlib.Path(__file__).resolve().parent.parent
import hb_content as HB  # noqa: E402
from hb_build import split_sections, label_of, body_text  # noqa: E402

SRC_TOWN, SRC_SLUG = 'Carshalton', 'carshalton'

SEEN_H2 = 'What we see on cars from Hackbridge'
SEEN = """
<p>Almost everything that comes to us from Hackbridge itself arrived under its own steam from a
few streets away, and it shows in what the damage looks like. It is parked damage, not road
damage.</p>
<p>Sutton Council&rsquo;s ward parking survey for Wandle ward, which is Hackbridge, found 67 per
cent of residents saying their street has a parking problem, 39 per cent parking on the road, and
74 per cent saying the trouble is on weekdays. On top of that, the old Felnex estate &mdash; about
a million square feet of former industry &mdash; was approved in 2016 for 725 homes plus a
supermarket, a surgery, a care home and a bus interchange, and New Mill Quarter adds another 440.
Over eleven hundred new homes, going into a suburb whose central parade is Edwardian.</p>
<p>So: streets parked solid on both sides, years of contractor and delivery traffic squeezing
through them, and roads that were drawn for a fraction of it. Scuffed bumper corners, creased
doors, mirrors taken off by passing vans, kerbed alloys.</p>
<p>The mechanical side has its own local signature, and it comes from the station. Hackbridge is
Zone 4 and about 25 minutes from Victoria, so a great many cars here exist to cover one mile
twice a day. That is the hardest duty cycle you can give a modern car: diesel particulate filters
that never get hot enough to clear, batteries that never fully recharge, exhausts that rot from
the inside, brakes that corrode between uses. We see more of all four from Hackbridge than from
anywhere else we cover.</p>
"""

WHY_H2 = 'Why being the garage in the village actually matters'
WHY = """
<p>Most garages describe themselves as local. We are on London Road, which for a good deal of
Hackbridge is a walk rather than a drive, and that has practical consequences rather than
sentimental ones.</p>
<ul class="kx-list">
<li><strong>You can bring it down and have it looked at.</strong> Not booked in for a fortnight
on Thursday so somebody can hear you describe a noise.</li>
<li><strong>You can leave it and walk home.</strong> No lift to arrange, no waiting room.</li>
<li><strong>We can see it before we quote.</strong> Where a job needs the car on a ramp to price
honestly, that is a short detour rather than a second trip across town.</li>
<li><strong>We have to live with what we tell you.</strong> In a suburb this size, selling
somebody four tyres when they needed two is the last work you get from them or anyone they
know.</li>
</ul>
<p>That last one is the real difference and it cuts against us as often as for us. We tell people
their car is not worth repairing, that the dent they are worried about will cost more to fix than
it takes off the value, and that a PDR specialist down the road will do a particular job cheaper
than we will, because every one of those conversations happens again in the Co-op.</p>
"""

FAQS = [
 ('Where are you exactly?',
  'Unit 1, Soho Mills, London Road, Hackbridge SM6 7HN &mdash; a couple of minutes from Hackbridge '
  'station and the parade, with room to leave a car.'),
 ('Can I walk in without booking?',
  'To have something looked at, yes. For work that needs a ramp and a slot, call or put your '
  'registration into the box on this page first so we can give you a time.'),
 ('Do you do both mechanical work and bodywork?',
  'Both, on the same site. Garage and bodyshop, so a car that needs paint and a clutch does not '
  'have to go to two places.'),
 ('Are you on any insurer panel?',
  'No, and we are on no manufacturer scheme either. On a claim the repairer is your choice, and '
  'nothing we tell you is steered by an arrangement with an insurer.'),
 ('Do you do paintless dent removal?',
  'No. Every dent we repair is straightened and then painted and blended. On the dents PDR can '
  'fix, a specialist will be cheaper and we would rather tell you that.'),
 ('My car barely does any miles. Does it still need servicing?',
  'Usually yes, on the time interval rather than the mileage one. Short local journeys are harder '
  'on oil, brakes and batteries than the odometer suggests, which is the single most common thing '
  'we explain to people in Hackbridge.'),
]


def main():
    src = (ROOT / f'{SRC_SLUG}.html').read_text()
    i, j = src.find('<main'), src.find('</main>')
    head, main, tail = src[:i], src[i:j], src[j:]
    rebuilt, done = main, []

    for _, _, block in split_sections(main):
        h2m = re.search(r'<h2[^>]*>(.*?)</h2>', block, re.S)
        h2 = re.sub(r'<[^>]+>', '', h2m.group(1)).strip() if h2m else ''
        label = label_of(block)

        if h2 == f'What we see on cars from {SRC_TOWN}':
            rebuilt = rebuilt.replace(block, (
                f'<section class="section section-alt"><div class="container kx-narrow">'
                f'<span class="section-label">{HB.NAME} drivers</span><h2>{SEEN_H2}</h2>'
                f'<div class="kx-prose">{SEEN.strip()}</div></div></section>'), 1)
            done.append('seen')
        elif h2 == f'Why {SRC_TOWN} drivers use KITH':
            rebuilt = rebuilt.replace(block, (
                f'<section class="section"><div class="container kx-narrow">'
                f'<h2>{WHY_H2}</h2><div class="kx-prose">{WHY.strip()}</div>'
                f'</div></section>'), 1)
            done.append('why')
        elif label == 'The route' or h2 == f'From {SRC_TOWN} to Soho Mills':
            rebuilt = rebuilt.replace(block, (
                f'<section class="section section-alt"><div class="container kx-narrow">'
                f'<span class="section-label">Finding us</span>'
                f'<h2>{HB.HERE_HEADING}</h2>'
                f'<div class="kx-prose">{HB.HERE.strip()}</div></div></section>'), 1)
            done.append('route')
        elif label == 'Questions':
            items = ''.join(
                f'<details class="kx-faq"{" open" if n == 0 else ""}><summary><h3>{q}</h3>'
                f'</summary><p>{a}</p></details>' for n, (q, a) in enumerate(FAQS))
            rebuilt = rebuilt.replace(block, (
                f'<section class="section"><div class="container kx-narrow">'
                f'<span class="section-label">Questions</span>'
                f'<h2>{HB.NAME}: your questions answered</h2>'
                f'<div class="kx-faqs">{items}</div></div></section>'), 1)
            done.append('faq')

    html = head + rebuilt + tail
    html = re.sub(r'(<h1[^>]*>).*?(</h1>)',
                  lambda m: m.group(1) + 'Your Garage and Bodyshop in Hackbridge' + m.group(2),
                  html, count=1, flags=re.S)
    html = re.sub(r'(<p class="lead">).*?(</p>)', lambda m: m.group(1) + (
        'We are at Unit 1 Soho Mills on London Road &mdash; not near Hackbridge, in it. '
        'Mechanical repairs, servicing, MOT, bodywork, accident repair and recovery, on one '
        'site, a few minutes from the station.') + m.group(2), html, count=1, flags=re.S)

    html = html.replace(f'/{SRC_SLUG}"', f'/{HB.SLUG}"')
    html = html.replace(f'-{SRC_SLUG}', f'-{HB.SLUG}')
    html = html.replace(SRC_TOWN, HB.NAME).replace(SRC_SLUG, HB.SLUG)
    html = re.sub(r'\bSM5\b', HB.PC, html)
    html = re.sub(r'(\d+|five|ten|couple of)\s+minutes?\s+(away\s+)?(from|to)\s+Hackbridge'
                  r'(?!\s+station)', 'here in Hackbridge', html, flags=re.I)

    problems = []
    for need in ('seen', 'why', 'route', 'faq'):
        if need not in done:
            problems.append(f'did not replace the {need} section')
    if re.search(rf'\b{SRC_TOWN}\b', html):
        problems.append(f'still mentions {SRC_TOWN}')
    if problems:
        print('PROBLEMS:')
        for p in problems:
            print('  ' + p)
        return 1

    (ROOT / f'{HB.SLUG}.html').write_text(html)
    print(f'wrote /{HB.SLUG} ({len(body_text(html).split())} words)')

    # --- footer "Serving ..." list, site-wide ------------------------------------------------
    anchor = '<a href="/croydon">Croydon</a>'
    link = '<a href="/hackbridge">Hackbridge</a> &middot; '
    changed = skipped = 0
    for f in sorted(ROOT.glob('*.html')):
        h = f.read_text()
        if '<html' not in h or anchor not in h:
            continue
        if 'href="/hackbridge">Hackbridge</a>' in h:
            skipped += 1
            continue
        f.write_text(h.replace(anchor, anchor + ' &middot; ' + link.rstrip(' &middot; '), 1))
        changed += 1
    print(f'footer: {changed} pages updated, {skipped} already listed Hackbridge')
    return 0


if __name__ == '__main__':
    sys.exit(main())
