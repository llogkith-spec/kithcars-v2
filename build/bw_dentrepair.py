#!/usr/bin/env python3
"""Dent repair, one page per town, rebuilt from scratch.

Replaces dent-removal-<town>, seventeen pages that measured 97.4% identical to each other. The
old ones are not edited: they are regenerated under a new slug and the old URLs are redirected,
because the name was wrong as well as the content. KITH does not do paintless dent removal, and
"dent removal" is the exact phrase people use when they mean PDR. "Dent repair" is what actually
happens here - the panel is straightened and then painted and blended.

The local half of each page comes from bw_towndata and leads, rather than being a paragraph
appended to a template. The shared half - what a dent repair involves, what it costs, the
guarantee - is kept deliberately short, because on the old pages it was the whole page.

The build's uniqueness check measures the result. Target is under 50%, which is where the guide
pages sit, rather than the 62% the gate allows.
"""
import json
import pathlib

from bw_lib import page, HUB_DAMAGE
from bw_towndata import TOWNS, BOROUGH
from bw_townextra import EXTRA, FAQ, PANELS

PRICES = json.loads((pathlib.Path(__file__).resolve().parent / 'bodyprices.json').read_text())

CREDIT = ('Collision figures are DfT STATS19 road casualty data as presented by crashview.co.uk, '
          'counted by postcode district over the full recorded period. Parking figures are the '
          'London Borough of Sutton&rsquo;s own ward parking surveys.')


def money(panel, band='medium'):
    p = PRICES[f'{panel}|dent|{band}']
    return f'&pound;{p["low"]}', f'&pound;{p["high"]}'


def build():
    out = []
    for key, T in TOWNS.items():
        name = T['name']
        b = BOROUGH.get(T['borough']) if T['borough'] else None

        # ---- the local half, which is what makes this page worth having -------------------
        local = [T['character']]

        if T['pc_n']:
            shared = (' That district also covers ' + T['shared'] + '.') if T.get('shared') else ''
            local.append(
                '<strong>' + T['pc'] + ' has ' + T['pc_n'] + ' recorded collisions.</strong>' +
                shared + (' Across the London Borough of ' + T['borough'] + ' the total is ' +
                          b['collisions'] + ', with ' + b['serious'] + ' of them serious.'
                          if b else ''))
            # The borough roads table is identical for every town in that borough, so it only
            # appears on the town the borough is named after. Everywhere else the postcode
            # figure above is the town-specific number and the table added nothing but overlap.
            if b and T['name'] == T['borough']:
                local.append(('table', (['Busiest roads in ' + T['borough'], 'Collisions'],
                                        [[r, n] for r, n in b['roads']])))
        else:
            local.append('<strong>' + T['pc'] + '.</strong> We have not quoted a collision count '
                         'for ' + name + ' because the published figures for that district are '
                         'split across boroughs and any single number would be misleading.')

        local.append(T['damage'])

        if T.get('parking'):
            P = T['parking']
            local.append(
                '<strong>What the council&rsquo;s parking survey found in ' + P['ward'] +
                '.</strong> ' + P['problem'] + ' per cent of residents said their street has a '
                'parking problem, ' + P['two_cars'] + ' per cent of households run two or more '
                'cars and ' + P['on_street'] + ' per cent park at least one on the road. The '
                'streets that responded most were ' + P['streets'] + '.')

        if EXTRA.get(key):
            local.append(EXTRA[key])
        local.append(('note', CREDIT))

        # ---- the shared half, kept short ---------------------------------------------------
        d_lo, d_hi = money('door')
        w_lo, w_hi = money('front-wing')
        b_lo, b_hi = money('front-bumper')
        q_lo, q_hi = money('rear-quarter')

        sections = [
            ('Dents in ' + name + ', and where they come from', local),

            ('How we do it', [
             'We straighten the panel and then paint it, blending into the panels either side. '
             'We do not do paintless dent removal &mdash; on a shallow dent with unbroken paint a '
             'PDR specialist will be cheaper, and on a crease, a dent near an edge or anything '
             'with the paint split, PDR cannot do it at all. '
             '<a href="/car-dent-repair">The full method is here</a>.']),
            ('What it costs in ' + name, [
             'The panels ' + name + ' damages most, repaired and painted, including VAT and '
             'blending into the neighbouring panels on an ordinary five-seater.',
             ('table', (['Panel', 'Dent repaired and painted'],
                        [[lbl, money(pk)[0] + ' &ndash; ' + money(pk)[1]]
                         for pk, lbl in PANELS[key]])),
             'Your own car and panel: put the registration into the box below. '
             '<a href="/body-panel-repairs">Every panel is priced here</a>.']),
            ('Getting it to us from ' + name, [
             'Unit 1, Soho Mills, London Road, Hackbridge SM6 7HN &mdash; about ' + T['mins'] +
             ' minutes from ' + name + '. ' +
             ('Most cars from this close come to us the same week.' if int(T['mins']) <= 10
              else 'Ask about collection when you book if the trip is awkward.') +
             ' A dent with the paint split is worth getting in before a winter rather than '
             'after one: bare metal in the bottom of a depression holds water.']),
        ]

        # Two shared questions, because they genuinely apply everywhere, and two written for
        # this town. The old pages carried five identical ones, which on seventeen pages was the
        # single largest block of shared text on each of them.
        faqs = [
            ('Do you do paintless dent removal?',
             'No. The panel is straightened and then painted and blended. On a shallow dent with '
             'unbroken paint a PDR specialist will be cheaper than us; on a crease, a dent near '
             'an edge, or anything with the paint broken, PDR cannot do it at all. We would '
             'rather tell you that now than after your car is here.'),
            FAQ[key],
            ('How long will my car be with you, coming from ' + name + '?',
             'A single panel is two to three days, because the paint has to cure before it is '
             'polished and refitted. At ' + T['mins'] + ' minutes away ' +
             ('you can drop it and collect it easily enough.' if int(T['mins']) <= 12
              else 'it is worth asking about collection when you book, rather than making the '
                   'trip twice.')),
        ]

        out.append(page(
            'dent-repair-' + key,
            'Dent Repair in ' + name + ' &ndash; From ' + d_lo.replace('&pound;', '£') +
            ' | KITH Cars',
            'Dent repair in ' + name + ': what it costs, what the job involves, and why we '
            'straighten and paint rather than doing paintless removal. ' + T['mins'] +
            ' minutes from ' + name + '.',
            'Dent Repair in ' + name,
            'Bodywork &middot; ' + name,
            T['character'],
            sections, faqs,
            # Pointed at the panels this town actually damages, rather than the same four
            # links on all seventeen pages.
            [(PANELS[key][0][0] + '-repair-cost', PANELS[key][0][1] + ' repair'),
             (PANELS[key][1][0] + '-repair-cost', PANELS[key][1][1] + ' repair'),
             ('car-dent-repair', 'Dent repair, in detail'),
             ('body-panel-repairs', 'Every panel and what it costs')],
            key_points=[
             '<strong>' + money(PANELS[key][0][0])[0] + ' to ' + money(PANELS[key][0][0])[1] +
             '</strong> for a ' + PANELS[key][0][1].lower() + ', inc VAT and blending.',
             'The panel ' + name + ' damages most is the <strong>' +
             PANELS[key][0][1].lower() + '</strong>.',
             (T['pc'] + ': <strong>' + T['pc_n'] + ' recorded collisions</strong>.'
              if T['pc_n'] else 'Covering ' + T['pc'] + ' and the roads around it.'),
             '<strong>' + T['mins'] + ' minutes</strong> from ' + name + ' to Hackbridge.'],
            hub=HUB_DAMAGE, job='panel-door', category='town',
            service_type='Vehicle body repair',
            quote_heading='Price your dent now',
            note=None))
    return out


PAGES = build()
