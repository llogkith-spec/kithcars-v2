#!/usr/bin/env python3
"""Rewrite the dent pages around refinishing instead of paintless repair.

Run from the repo root:  python3 build/dentgen.py

KITH does not do paintless dent removal. Every dent is pulled or filled and the panel is then
painted. The existing pages were built around PDR -- paint depth gauges, rods behind the panel,
glue pulling, "no holes drilled" -- so they argued at length for a service that is not offered,
and headlined a price (£60) that only makes sense without paint.

This replaces each page's <main>, title, description and schema. The header, footer, booking
block and reviews are left alone: they are shared with every other page and are already correct.
Area pages keep their own travel time and road names so they stay locally specific.
"""
import glob, json, pathlib, re, sys

ROOT = pathlib.Path.cwd()
PRICE_FROM = '£260'          # cheapest painted panel + the lightest dent, inc VAT
PRICE_TO = '£650'            # a bumper with a bad dent, inc VAT

# Travel time and nearby roads, harvested from the pages these replace.
AREAS = {
    'beddington': ('Beddington', 6, 'the A232 and A237'),
    'carshalton': ('Carshalton', 5, 'the A232 and the B278'),
    'cheam': ('Cheam', 12, 'the A232 and the B277'),
    'coulsdon': ('Coulsdon', 17, 'the A237 and the B2030'),
    'croydon': ('Croydon', 15, 'the A232 and A237'),
    'mitcham': ('Mitcham', 8, 'the A217 and A239'),
    'morden': ('Morden', 12, 'the A237 and A239'),
    'norbury': ('Norbury', 18, 'the A236 and the A23'),
    'purley': ('Purley', 15, 'the A235 and A2022'),
    'rosehill': ('Rosehill', 9, 'the A217 and A297'),
    'streatham': ('Streatham', 20, 'the A216 and A217'),
    'sutton': ('Sutton', 10, 'the A232 and B278'),
    'thornton-heath': ('Thornton Heath', 15, 'the A236 and A237'),
    'tooting': ('Tooting', 18, 'the A217 and A239'),
    'wallington': ('Wallington', 6, 'the A232 and A237'),
    'wimbledon': ('Wimbledon', 20, 'the A218 and A219'),
    'worcester-park': ('Worcester Park', 14, 'the A2043 and A24'),
}

FAQ = [
    ("Do you do paintless dent removal?",
     "No. We pull or fill the dent and then paint the panel. Paintless repair is a specialist trade "
     "with its own kit and its own limits, and we would rather tell you plainly that we do not do it "
     "than take the car in and find out halfway through. What we do instead is the repair that works "
     "on any dent, whatever the paint is doing: straighten it, prepare it, paint it, blend it into "
     "the panels either side so there is no hard edge where new meets old."),
    ("So what does a dent actually cost?",
     "Two parts. Straightening the dent runs from 70 pounds plus VAT for a shallow ding to 300 pounds "
     "plus VAT for a deep crease or one on a braced edge. Painting the panel is then charged at the "
     "panel rate - 240 pounds plus VAT for a front bumper, 200 for a door, 150 for a wing. In practice "
     "that is " + PRICE_FROM + " to " + PRICE_TO + " including VAT for most dents. The spread is wide "
     "because dents genuinely are: a car park ding and a kerbed crease are not the same job."),
    ("Why is a dent more than a scratch, when it looks like less damage?",
     "Because a scratch only needs the panel painting, and a dent needs the metal made straight first. "
     "That is the part that takes the time: pulling, levelling, filling where the stretch will not come "
     "back, and flatting it true before any paint goes near it. The paint is then the same job it would "
     "have been anyway."),
    ("Will the colour match?",
     "We mix to your car's own paint code and spray a test card before anything goes near the panel. "
     "On metallics and pearls the repair is blended out into the surrounding panels rather than stopping "
     "at a hard line, because paint that has weathered for a few years no longer matches the factory "
     "code exactly. That blending is included, not an extra."),
    ("How long will the car be off the road?",
     "A single panel is usually one to two days, because the paint has to cure properly between stages "
     "and rushing that is what makes a repair fail six months later. We give you a date when we have "
     "seen the car, not before. A courtesy car is available at 30 pounds plus VAT a day, subject to "
     "availability."),
    ("Is it worth repairing at all?",
     "Sometimes not, and we will say so. On an older car a shallow door ding can cost more to put right "
     "than it takes off the value, and you are entitled to hear that before you spend anything. Where "
     "the dent has broken the paint it is a different matter: bare metal rusts, and a rust repair later "
     "costs considerably more than the dent does now."),
]


def body(area=None, mins=None, roads=None):
    where = f'{area} drivers' if area else 'drivers across South London'
    local = ''
    if area:
        local = (f'<section class="section section-alt"><div class="container kx-narrow">\n'
                 f'<h2>Coming from {area}</h2>\n'
                 f'<p>We are about {mins} minutes from {area} by {roads}, at Unit 1, Soho Mills on London '
                 f'Road in Hackbridge. Most {area} customers drop the car in the morning and we tell them '
                 f'that day what the dent needs and what it will cost. If the car is not safe or not '
                 f'convenient to drive we can collect it, and a courtesy car is available at '
                 f'&pound;36 a day while yours is with us.</p>\n'
                 f'</div></section>\n\n')

    h1 = (f'Dent repair for {area} drivers, straightened and repainted'
          if area else 'Dent repair in South London, straightened and repainted')

    return f'''<main>
<section class="page-hero"><div class="container kx-narrow">
<nav class="kx-crumbs" aria-label="Breadcrumb"><a href="/">Home</a> <span>&rsaquo;</span> <a href="/bodywork">Bodywork</a> <span>&rsaquo;</span> <span aria-current="page">Dent Repair</span></nav>
<span class="section-label">KITH Bodyworks &middot; Hackbridge SM6</span>
<h1>{h1}</h1>
<p class="lead">We do not do paintless dent removal, and we would rather say so up front than have
you find out halfway through. Every dent we take on is straightened, prepared and the panel
repainted, which is the repair that works whatever the paint is doing and whatever has been done
to the panel before. {PRICE_FROM} to {PRICE_TO} including VAT for most dents, confirmed in writing
once we have seen it.</p>
<p><a class="btn btn-primary" href="/#quote">Price my dent</a> <a class="btn btn-ghost" href="tel:02046299469">Call 020 4629 9469</a></p>
</div></section>

<section class="section"><div class="container kx-narrow">
<h2>What we do instead of paintless</h2>
<p>Paintless dent removal is a genuine trade, done well by people who do nothing else. It works by
pushing the metal back from behind while the original paint stays intact, and when the panel suits
it the result is excellent. It also has real limits: a dent on a doubled edge, over a brace, on a
panel that someone has already filled, or one where the paint has cracked, is not a paintless job
at all.</p>
<p>We are a bodyshop with our own spray booth, so we do the repair that has no such limits.
The metal is pulled or filled until it is true, the panel is prepared, primed and painted in your
car's own colour, and the new paint is blended out into the panels either side so there is no edge
where it stops. It costs more than a paintless repair would. It also works on every dent, and it
looks the same afterwards whichever kind of dent it was.</p>
</div></section>

<section class="section section-alt"><div class="container kx-narrow">
<h2>What a dent costs, and why</h2>
<p>A dent is two jobs charged as one, which is why a single headline figure would be misleading.</p>
<table class="kx-table">
<thead><tr><th>Part of the job</th><th>Cost</th></tr></thead>
<tbody>
<tr><td>Straightening a shallow ding</td><td>from &pound;70 + VAT</td></tr>
<tr><td>Straightening a deep crease, or one on a braced edge</td><td>up to &pound;300 + VAT</td></tr>
<tr><td>Painting a front bumper</td><td>&pound;240 + VAT</td></tr>
<tr><td>Painting a door</td><td>&pound;200 + VAT</td></tr>
<tr><td>Painting a wing, bonnet or rear quarter</td><td>&pound;150 + VAT</td></tr>
<tr><td>Blending into the neighbouring panels</td><td>included</td></tr>
</tbody></table>
<p class="kx-note">Most dents land between {PRICE_FROM} and {PRICE_TO} including VAT. The spread is
honest rather than cautious: a car park ding on a wing and a kerbed crease across a bumper are not
the same amount of work, and you cannot tell which you have from a photograph alone. Send one
anyway and we will narrow it down before you bring the car in.</p>
<p><a class="btn btn-primary" href="/#quote">Get my price</a></p>
</div></section>

<section class="section"><div class="container kx-narrow">
<h2>How we do it</h2>
<ol class="kx-steps">
<li><b>Look at the panel, not just the dent.</b> What is behind it decides the method: a door skin
with access behind it is a different job from a bonded quarter panel or a bumper over a bracket.</li>
<li><b>Tell you what it will take</b> before you commit, including the times it is not worth
doing. On an older car a shallow ding can cost more to put right than it takes off the value.</li>
<li><b>Straighten the metal.</b> Pulled from behind where there is access, pulled from the front
where there is not, and filled only where the metal has stretched and will not come back.</li>
<li><b>Prepare and prime.</b> Flatted true and guide-coated, so a high spot shows up now rather
than under the paint.</li>
<li><b>Paint in your car's colour</b>, mixed to the code and checked against the panel on a test
card, then blended into the panels either side.</li>
<li><b>Check it in the light</b> before you see it. 3-month workmanship warranty, no deposit, paid
on collection.</li>
</ol>
</div></section>

<section class="section"><div class="container kx-narrow">
<h2>The dents we see most, and what moves the price</h2>
<p>Almost every dent that comes through the door is one of five, and knowing which you have tells
you roughly where in the range you will land.</p>
<h3>The car park door ding</h3>
<p>Someone else's door, usually low on your own door skin or along the crease line. Shallow, round,
and the paint is often intact. There is normally access behind a door skin once the card and the
window regulator come out, so the metal comes back without much drama. This is the cheap end:
straightening at the bottom of the range, then the door at &pound;200 plus VAT. The thing that
pushes it up is position &mdash; a ding right on the swage line is held by the shape of the panel
either side and fights you.</p>
<h3>The kerbed or clipped bumper</h3>
<p>A bumper is plastic, not steel, so it behaves differently: it will often take a shape back with
heat, but it also cracks where a panel would simply bend. If the plastic has split, a repair means
welding it from behind before any filler goes near it, and that is where the hours go. Bumpers are
also the most expensive panel to paint at &pound;240 plus VAT, so a bad one sits at the top of the
range.</p>
<h3>The trolley or bike handlebar</h3>
<p>Small, deep, and usually through the paint. The dent itself is quick. What matters is that bare
metal has been sitting in the weather, so there may be rust under the edge of the surrounding paint
that only shows once it is flatted back. We will tell you if we find it rather than paint over it.</p>
<h3>The crease</h3>
<p>A long dent with a sharp line through it, from a post, a gatepost or another car's corner. The
metal has stretched along the crease and will not simply come back, so it is pulled as far as it
goes and then filled and levelled. Creases are the reason the straightening range runs to
&pound;300 plus VAT: a long one on a rear quarter is most of a day's work before paint.</p>
<h3>The braced or doubled panel</h3>
<p>Dents on a bonnet edge, a tailgate rib or anywhere the panel is doubled over or backed by a
brace have nowhere to move. These are the jobs where we will sometimes tell you the improvement is
not worth the money, and you are entitled to hear that before you spend it.</p>
</div></section>

<section class="section section-alt"><div class="container kx-narrow">
<h2>When a new panel is the cheaper answer</h2>
<p>Repairing is usually cheaper than replacing, but not always, and a bodyshop that never says so
is not being straight with you.</p>
<p>A new panel wins when the metal is torn rather than dented, when a crease runs across more than
about half the panel, when the damage sits on a bonded or structural section, or when a used panel
in your colour happens to be available cheaply for a common car. It also wins on some modern bumpers,
where the part is cheap and the hours to repair it are not.</p>
<p>Repairing wins almost everywhere else, and on a car you may sell it has a second advantage: a
repaired original panel keeps the car's original structure, where a replacement shows up on an
inspection as a panel that has been off. We price both where both are realistic and tell you which
we would choose, and why.</p>
</div></section>

{local}<section class="section"><div class="container kx-narrow">
<h2>See the work</h2>
<p>We photograph jobs as they go through our own booth &mdash; stripped, prepared, sprayed and
refitted. <a href="/bodywork-gallery">See photos of real jobs from our workshop</a>.</p>
</div></section>

<section class="section section-alt"><div class="container kx-narrow" id="faq">
<h2>Dent repair: your questions answered</h2>
<div class="kx-faqs">{"".join(
    '<details class="kx-faq"' + (' open' if i == 0 else '') + '><summary><h3>' + q +
    '</h3></summary><p>' + a + '</p></details>' for i, (q, a) in enumerate(FAQ))}</div>
</div></section>

<section class="section"><div class="container kx-narrow">
<h2>Related work we do</h2>
<p><a href="/bumper-repair">Bumper repair</a> &middot; <a href="/scratch-repair">Scratch repair</a>
&middot; <a href="/stone-chip-repair">Stone chip repair</a> &middot;
<a href="/smart-repairs">SMART repairs</a> &middot;
<a href="/car-respray">Panel and full resprays</a> &middot;
<a href="/accident-repairs">Accident repair</a></p>
</div></section>
</main>'''


def rewrite(path):
    slug = path[len('dent-removal'):-5].lstrip('-')
    area, mins, roads = AREAS.get(slug, (None, None, None))
    p = pathlib.Path(path)
    s = p.read_text()

    title = (f'Dent Repair {area} | Straightened and Repainted | KITH Cars'
             if area else f'Dent Repair South London | From {PRICE_FROM} | KITH Cars')
    desc = (f'Dent repair for {area} drivers at our Hackbridge bodyshop. We do not do paintless: '
            f'the dent is straightened and the panel repainted, {PRICE_FROM}–{PRICE_TO} inc VAT. '
            f'4.9 from 193 Google reviews.'
            if area else
            f'Dent repair in Hackbridge SM6. We do not do paintless: the dent is straightened and the '
            f'panel repainted and blended, {PRICE_FROM}–{PRICE_TO} inc VAT. 4.9 from 193 reviews.')

    head = s[:s.index('<main>')]
    tail = s[s.index('</main>') + len('</main>'):]

    head = re.sub(r'<title>.*?</title>', '<title>' + title + '</title>', head, count=1, flags=re.S)
    head = re.sub(r'(<meta name="description" content=")[^"]*(")', lambda m: m.group(1) + desc + m.group(2), head, count=1)
    head = re.sub(r'(<meta property="og:title" content=")[^"]*(")',
                  lambda m: m.group(1) + title.split(' | ')[0] + m.group(2), head, count=1)
    head = re.sub(r'(<meta property="og:description" content=")[^"]*(")', lambda m: m.group(1) + desc + m.group(2), head, count=1)

    def fix(m):
        data = json.loads(m.group(2))
        for node in data.get('@graph', []):
            if node.get('@type') == 'FAQPage':
                node['mainEntity'] = [
                    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                    for q, a in FAQ]
            elif node.get('@type') == 'Service':
                node['name'] = f'Dent repair{" " + area if area else ""}'
                node['serviceType'] = 'Dent repair'
                node['description'] = desc
            elif node.get('@type') == 'WebPage':
                node['name'] = title
        return m.group(1) + json.dumps(data, ensure_ascii=False) + m.group(3)

    head = re.sub(r'(<script type="application/ld\+json">)(.*?)(</script>)', fix, head, flags=re.S)

    page = head + body(area, mins, roads) + tail

    # Anything left over outside <main> that still sells the old service or the old price.
    page = re.sub(r'[Pp]aintless [Dd]ent [Rr]emoval', 'Dent repair', page)
    page = re.sub(r'[Pp]aintless [Dd]ent [Rr]epair', 'Dent repair', page)
    page = re.sub(r'[Pp]aintless', 'dent', page)
    page = page.replace('From £60', f'From {PRICE_FROM}').replace('from £60', f'from {PRICE_FROM}')
    p.write_text(page)

    left = len(re.findall(r'(?i)paintless|\bPDR\b', page))
    cheap = len(re.findall(r'£60\b', page))
    return f'{path:<36} {len(page):>7,}b  leftover PDR: {left}  "£60": {cheap}'


if __name__ == '__main__':
    files = sorted(glob.glob('dent-removal*.html'))
    for f in files:
        print(rewrite(f))
    print(f'\n{len(files)} dent pages rewritten')
