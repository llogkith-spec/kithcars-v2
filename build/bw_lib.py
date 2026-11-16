#!/usr/bin/env python3
"""Shared helpers for the bodywork content modules.

One place for the page constructor and the standing notes, so a change to the disclaimer or to
the breadcrumb hub does not have to be made in nine content files.
"""

ADVICE_NOTE = ('This is general information about how motor claims usually work, not legal or '
               'financial advice. Your own policy wording decides what you are entitled to, so '
               'read it, or ring us on <a href="tel:02046299469">020 4629 9469</a> and we will '
               'talk it through against the damage in front of us.')

CHOICE_NOTE = ('Whoever you claim through, the repairer is your choice. KITH is on no '
               'insurer&rsquo;s panel, which means no labour time has been pre-agreed on your '
               'car&rsquo;s behalf &mdash; we estimate the job as it needs doing and argue it '
               'with the engineer if we have to.')

HUB_INSURANCE = ('Insurance &amp; claims', 'car-insurance-claims')
HUB_PROCESS = ('The repair process', 'bodywork-repair-process')
HUB_DAMAGE = ('Damage &amp; panels', 'body-panel-repairs')
HUB_MAKES = ('By make', 'bodywork-by-make')

# No self-reported star rating here. Google does not use a rating a business publishes about
# itself, and in structured data it is self-serving review content. The real reviews are on the
# Business Profile.
TRUST_DEFAULT = [
    'Hackbridge SM6 7HN',
    'Any insurer &middot; your choice of repairer',
]


def page(slug, title, desc, h1, label, lead, sections, faqs, related=(), key_points=(),
         hub=HUB_INSURANCE, job='panel-front-bumper', flow='bodywork',
         service_type='Accident repair', quote_heading='Price your repair now',
         note=ADVICE_NOTE, note_heading='Before you act on any of this', trust=None,
         category='insurance'):
    """One page. `note` is appended as a final section; pass note=None to leave it off."""
    secs = list(sections)
    if note:
        secs.append((note_heading, [('note', note)]))
    return {
        'slug': slug, 'title': title, 'desc': desc, 'h1': h1, 'label': label, 'lead': lead,
        'sections': secs, 'faqs': list(faqs), 'related': list(related),
        'key_points': list(key_points), 'job': job, 'flow': flow,
        'service_type': service_type, 'quote_heading': quote_heading,
        'trust': trust or TRUST_DEFAULT,
        # hub=None means this page IS a hub, so there is no intermediate crumb - otherwise the
        # breadcrumb would link to the page you are already on.
        'crumbs': ([hub] if hub else []) + [(h1, None)],
        'category': category,
    }
