#!/usr/bin/env python3
"""Hub pages.

Without these, every page in this set is an orphan: reachable from a search result and from its
siblings' related links, but with no path down from the site's own navigation and nothing
gathering the cluster into a topic. That is bad for the crawl and worse for a reader who arrives
on "what is a Cat N" and wants to know what else is here.

The hubs are generated from the page list rather than hand-written, so a page added later appears
on its hub automatically instead of being quietly left off - which is how link rot starts in a set
this size.

Each hub is also a real page in its own right, not just a list of links. A bare directory of
links ranks for nothing and helps nobody.
"""
import importlib

from bw_lib import page

# Sub-groupings within each hub, matched against the page's `label`. The order here is the order
# they appear on the hub, which is deliberately the order someone works through the problem:
# what happened, who pays, what it costs, what the car needs.
INSURANCE_GROUPS = [
    ('Just had an accident', ['Fault and liability']),
    ('Who pays, and how much', ['Excess', 'Deciding', 'No-claims']),
    ('Getting your car back', ['Replacement vehicles', 'The process']),
    ('Choosing who repairs it', ['Choice of repairer']),
    ('If they write it off', ['Write-offs']),
    ('When the repair goes wrong', ['When it goes wrong']),
    ('Particular situations', ['Specific situations']),
]

GUIDE_GROUPS = [
    ('How a repair actually works', ['The repair process', 'Assessment', 'Timescales',
                                     'Choosing']),
    ('Paint and colour', ['Paint']),
    ('Sensors, aluminium and electric cars', ['Electronics', 'Sensors and calibration',
                                              'Materials', 'Electric and hybrid']),
    ('Damage with nobody to claim from', ['Untraced drivers', 'Uninsured drivers',
                                          'Car park damage', 'Vandalism', 'Storm and flood']),
    ('What it is worth doing', ['Claim decisions', 'Lease and company cars', 'Selling', 'Wheels',
                                'Buying a used car']),
]

DAMAGE_GROUPS = [
    ('By panel', ['Front bumper', 'Rear bumper', 'Front wing', 'Rear quarter panel', 'Door',
                  'Bonnet', 'Roof', 'Boot lid', 'Trim']),
    ('By kind of damage', ['Scratches', 'Scuffs', 'Chips', 'Dents', 'Plastic', 'Corrosion',
                           'Kerbing', 'Vandalism']),
]

# Taken from the build's own module list rather than repeated here. Keeping a second copy is
# how a page gets written, linked from its siblings, and silently left off its hub - which is
# exactly what happened to the four "when it goes wrong" pages the first time round.
def CONTENT_MODULES():
    import bodywork
    return [m for m in bodywork.MODULES if m != 'bw_hubs']


def _all_pages():
    out = []
    for name in CONTENT_MODULES():
        mod = importlib.import_module(name)
        importlib.reload(mod)
        out.extend(mod.PAGES)
    return out


def _subtopic(p):
    """The bit after the middot in the page's label, which is its sub-topic."""
    label = p['label']
    return label.split('&middot;')[-1].strip() if '&middot;' in label else label.strip()


def _grouped(pages, groups, categories):
    """[(heading, [(slug, h1, one-line)])] in the order the groups are declared."""
    pool = [p for p in pages if p.get('category') in categories]
    used, out = set(), []
    for heading, subtopics in groups:
        rows = []
        for p in pool:
            if p['slug'] in used:
                continue
            if _subtopic(p) in subtopics:
                used.add(p['slug'])
                rows.append(p)
        if rows:
            out.append((heading, rows))
    leftover = [p for p in pool if p['slug'] not in used]
    if leftover:
        out.append(('Everything else', leftover))
    return out


def _summary(p):
    """One line for the hub listing: the page's own key point, stripped of markup."""
    import re
    if p.get('key_points'):
        return re.sub(r'<[^>]+>', '', p['key_points'][0])
    return re.sub(r'<[^>]+>', '', p['lead'])[:150]


def _listing(groups):
    """The hub's own body: a heading and a described link list per group."""
    blocks = []
    for heading, rows in groups:
        items = ''.join(
            f'<li><a href="/{p["slug"]}"><strong>{p["h1"]}</strong></a><span>{_summary(p)}</span></li>'
            for p in rows)
        blocks.append((heading, [('rawlist', items)]))
    return blocks


def build():
    pages = _all_pages()
    hubs = []

    # ---- insurance -------------------------------------------------------------------------
    ins_groups = _grouped(pages, INSURANCE_GROUPS, {'insurance'})
    ins_count = sum(len(r) for _, r in ins_groups)
    hubs.append(page(
        'car-insurance-claims',
        'Car Insurance Claims and Bodywork: The Complete Guide | KITH Cars',
        f'{ins_count} guides to motor bodywork claims: your right to choose a repairer, excess, '
        f'write-off categories, courtesy cars, no-claims and how a claim actually runs.',
        'Car Insurance Claims, Explained',
        'Insurance &amp; claims',
        'Everything we get asked after an accident, written out properly. Start with whichever '
        'applies to you &mdash; and if you only read one thing, read the bit about choosing your '
        'own repairer, because most people do not know they can.',
        [('The one thing worth knowing first', [
            'You choose who repairs your car. Not your insurer. They will steer you toward their '
            'own network because it costs them less, and the script can sound like a rule, but '
            'the car is yours and the choice is yours.',
            'KITH is on no insurer&rsquo;s panel and no manufacturer scheme. That means no labour '
            'time has been pre-agreed on your car&rsquo;s behalf &mdash; we estimate the job as '
            'it needs doing, argue it with the engineer where we have to, and guarantee the '
            'paint for a year ourselves.',
          ])] + _listing(ins_groups),
        [('Do you deal with my insurer?',
          'Any of them. We handle the estimate, the engineer and any supplementary. You make the '
          'first notification call, because the policy is yours.'),
         ('Is it cheaper to pay you directly than to claim?',
          'On most single-panel damage, yes, once you count your excess and what a claim does to '
          'five years of premiums. Put your registration in the box above for a real figure, then '
          'compare.'),
         ('Are you an approved repairer?',
          'No, and deliberately not. Approved networks are discount arrangements negotiated '
          'before your accident. We would rather price the job in front of us.'),
         ('What is guaranteed?',
          'One year on paint, three months on mechanical work, in writing, whoever is paying.')],
        [('bodywork-repair-process', 'The repair process, step by step'),
         ('body-panel-repairs', 'Every panel and what it costs'),
         ('bodywork', 'Bodywork and accident repair'),
         ('accident-repairs', 'Accident repairs')],
        key_points=[
          f'<strong>{ins_count} guides</strong> covering claims end to end.',
          '<strong>You choose the repairer</strong> &mdash; not your insurer.',
          'We are on <strong>no insurer panel</strong>, so no labour time is pre-agreed.',
          'One year on paint, in writing.'],
        hub=None, category='hub',
        service_type='Accident repair', quote_heading='Price your repair now', note=None))

    # ---- panels and damage -----------------------------------------------------------------
    dmg_groups = _grouped(pages, DAMAGE_GROUPS, {'panel', 'damage'})
    dmg_count = sum(len(r) for _, r in dmg_groups)
    hubs.append(page(
        'body-panel-repairs',
        'Car Body Panel Repairs: Every Panel and What It Costs | KITH Cars',
        f'{dmg_count} guides covering every panel on your car and every kind of damage, with '
        f'real prices from our rate card. Hackbridge bodyshop, any insurer.',
        'Every Panel, and What It Costs',
        'Bodywork',
        'Pick the panel, or pick the damage. Every price here comes from the same rate card the '
        'quote box uses, so what you read is what you get quoted.',
        [('How our bodywork pricing works', [
            'Three things decide a bodywork price: which panel, how bad the damage is, and how '
            'big the car is. Nothing else &mdash; there is no surcharge on our rate card for '
            'metallic, pearl, aluminium or a colour change.',
            'Every figure is shown as a band, and the band runs <em>upward</em> from the card '
            'price rather than either side of it. The card figure is the floor. What we cannot '
            'know before seeing the car is how much more the job is, never how much less.',
            'Blending the paint into the neighbouring panels is included in every figure. It is '
            'the first thing cut from a cheap quote and the main reason a repair shows in '
            'daylight, so we do not price it separately or leave it out.',
          ])] + _listing(dmg_groups),
        [('Can I get a price without bringing the car in?',
          'Yes. Put your registration into the box above and pick the panel and the damage. '
          'You will get a band immediately, and we confirm the exact figure when we see it.'),
         ('Do you do paintless dent removal?',
          'No. Every dent we repair is straightened and then painted and blended. On the dents '
          'PDR can fix, a PDR specialist will be cheaper, and we would rather say so.'),
         ('Is blending really included?',
          'Yes, on every figure. Ask anyone else quoting you the same question &mdash; the '
          'answers will tell you more than the prices.'),
         ('How long will it take?',
          'A localised repair is often same or next day. A panel off, painted and refitted is '
          'two to three days, because paint has to cure.')],
        [('bodywork-repair-process', 'The repair process, step by step'),
         ('car-insurance-claims', 'Insurance claims explained'),
         ('paint-colour-matching-explained', 'How paint matching works'),
         ('bodywork', 'Bodywork and accident repair')],
        key_points=[
          f'<strong>{dmg_count} guides</strong> &mdash; every panel, every kind of damage.',
          'Prices come from the <strong>same rate card the quote box uses</strong>.',
          'Bands run <strong>upward</strong> from the card figure, never below it.',
          '<strong>Blending is included</strong> in every price.'],
        hub=None, category='hub',
        service_type='Vehicle body repair', quote_heading='Price your panel now', note=None))

    # ---- guides ----------------------------------------------------------------------------
    # Everything that explains rather than prices. Without this hub these pages are reachable
    # only from each other, which is how a page gets written and never crawled.
    gd_groups = _grouped(pages, GUIDE_GROUPS, {'process', 'tech', 'value', 'scenario'})
    gd_count = sum(len(r) for _, r in gd_groups)
    hubs.append(page(
        'bodywork-guides',
        f'Car Bodywork Guides: {gd_count} Questions Answered | KITH Cars',
        f'{gd_count} guides on how bodywork actually works &mdash; paint matching, sensor '
        f'calibration, aluminium and electric cars, lease handback charges, and what to do when '
        f'there is nobody to claim from.',
        'Bodywork, Explained Properly',
        'Bodywork &middot; Guides',
        'Everything here answers a question rather than selling a job. If you want prices '
        'instead, the panel guides have our whole rate card.',
        [('What this is', [
            'These are the questions we get asked across the counter, written out properly. Some '
            'of them have exact answers that are worth knowing before you spend any money '
            '&mdash; the millimetre thresholds on a lease handback, for instance, or the fact '
            'that the national untraced drivers scheme does not pay for your car unless somebody '
            'was significantly injured.',
            'Where an answer depends on something we cannot know from here, the page says so '
            'rather than guessing. Where we do not do the work ourselves, it says that too.',
          ])] + _listing(gd_groups),
        [('Do I have to use my insurer&rsquo;s repairer?',
          'No. The repairer is your choice on any claim. We are on no insurer panel and no '
          'manufacturer scheme, so nothing here is steered by an arrangement.'),
         ('Can I get a price from these pages?',
          'The panel guides carry the rate card, and the box on every page gives you a band from '
          'your registration. These pages explain the why rather than the how much.'),
         ('Do you do paintless dent removal?',
          'No. Every dent we repair is straightened and then painted and blended. On the dents '
          'PDR can fix, a PDR specialist will be cheaper, and we would rather tell you.'),
         ('Something here is out of date.',
          'Tell us and we will fix it. The figures on these pages come from published sources and '
          'our own rate card, and both move.')],
        [('body-panel-repairs', 'Every panel, and what it costs'),
         ('car-insurance-claims', 'Insurance claims explained'),
         ('bodywork-repair-process', 'The repair process, step by step'),
         ('bodywork', 'Bodywork and accident repair')],
        key_points=[
          f'<strong>{gd_count} guides</strong> on how bodywork and claims actually work.',
          'Published <strong>sources and figures</strong>, not generalities.',
          'We are on <strong>no insurer panel</strong> and no manufacturer scheme.',
          'Where we do not do the work, the page <strong>says so</strong>.'],
        hub=None, category='hub',
        service_type='Vehicle body repair', quote_heading='Price your repair now', note=None))

    return hubs


PAGES = build()
