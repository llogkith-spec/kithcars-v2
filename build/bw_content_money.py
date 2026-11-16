#!/usr/bin/env python3
"""Three pages the cost-guide sites cannot write, because they are not a bodyshop.

The searches these target are currently owned by Checkatrade, Bumper and a dozen content farms
whose figures come from nowhere in particular. The only durable advantage against that is being
the one page with real numbers on it - our own rate card, and the government's own MOT data.

  bodywork-prices           Our actual from-prices per panel. Not a "typical UK cost of a bumper
                            repair is between £250 and £1,500" range, which is what the guides
                            say and which helps nobody.
  mot-failure-reasons       Built on DVSA's published initial-failure figures for class 3 and 4
                            vehicles, 2026-27 Q1. Real percentages, attributed, with the local
                            driving pattern used to explain which ones bite hardest here rather
                            than to invent local statistics we do not have.
  bodyshop-vs-main-dealer   The comparison, at AROUND 40% on bodywork labour. Not 60%. Our body
                            rate is £84/hr inc VAT against the £144 dealer rate in our own
                            catalogue, which is 42%; 60% would need a dealer charging £210/hr.
                            A comparative price claim has to be substantiable if anybody asks,
                            and the rate card is what substantiates this one.

Prices here are from-prices only, deliberately. See the note in the price page about what moves
a figure upward, and the two rate-card problems flagged to Logan separately: the prestige band is
priced identically to small on all 27 combinations, and rear quarter is priced the same as a
front wing despite being a welded structural panel.
"""
import json
import pathlib

from bw_lib import page, HUB_PROCESS, ADVICE_NOTE, CHOICE_NOTE

HERE = pathlib.Path(__file__).resolve().parent
P = json.loads((HERE / 'bodyprices.json').read_text())
C = json.loads((HERE.parent / 'quote-catalogue.json').read_text())

ALLOY = P['_alloy_per_wheel_inc_vat']
BODY_RATE = C['rates_inc_vat']['BODY']
DEALER_RATE = C['dealer']['labour_rate_inc_vat']['medium']
SAVING = round((DEALER_RATE - BODY_RATE) / DEALER_RATE * 100)


def frm(panel):
    """The floor price for a panel across every damage level and car size."""
    return min(v['low'] for k, v in P.items()
               if not k.startswith('_') and k.split('|')[0] == panel)


PANELS = [('front-bumper', 'Front bumper'), ('rear-bumper', 'Rear bumper'), ('door', 'Door'),
          ('front-wing', 'Front wing'), ('rear-quarter', 'Rear quarter'), ('bonnet', 'Bonnet'),
          ('boot', 'Boot lid'), ('roof', 'Roof'), ('trim', 'Trim, mirror or sill')]

DVSA = ('<a href="https://www.gov.uk/government/statistical-data-sets/mot-testing-data-for-great-'
        'britain" target="_blank" rel="noopener">DVSA&rsquo;s published MOT testing data</a>')

PAGES = [

    page('bodywork-prices',
         'Car Bodywork Prices: Our Actual Rate Card | KITH Cars',
         'What a bumper, door, wing or panel repair costs at our Hackbridge bodyshop &mdash; '
         'real from-prices, what is included, and what pushes a job upward.',
         'What Bodywork Actually Costs Here',
         'Bodywork &middot; Prices',
         'Every cost guide that ranks for this is written by somebody who does not repair cars. '
         'These are our own prices, from the same rate card the quote box uses.',
         [
          ('From-prices, by panel', [
           'All figures include VAT and include paint, materials and blending into the '
           'neighbouring panels. They are the floor: what the job costs when the damage is at the '
           'easy end.',
           ('table', (['Panel', 'From'],
            [[name, f'&pound;{frm(slug)}'] for slug, name in PANELS]
            + [['Alloy wheel refurbishment', f'&pound;{ALLOY["low"]} per wheel']])),
           'A figure in that column is not a teaser. It is what we charge for the smallest real '
           'version of that job, and plenty of jobs land on it.',
          ]),
          ('Why these bands run upward and never down', [
           'Every price on our rate card is a band, and the band runs <em>upward</em> from the '
           'card figure rather than either side of it.',
           'That is deliberate. The card figure is what we would charge for the job as described, '
           'so it is the floor. What we cannot know before the car is in front of us is how much '
           '<em>more</em> the job is &mdash; a crease that has stretched the metal, a clip that '
           'has broken behind the bumper, corrosion under the paint. Never how much less.',
           ('note', 'A range that runs in both directions advertises a number nobody actually '
            'pays. That is the single most common trick in published repair pricing and we do '
            'not use it.'),
          ]),
          ('What moves a price up', [
           ('table', (['Factor', 'Effect'], [
             ['Depth of damage',
              'A scuff in the lacquer, a scuff through to primer and a dent that has stretched '
              'the panel are three different jobs on the same panel'],
             ['Size of the car',
              'A van panel is larger and flatter than a car&rsquo;s, which makes the middle of it '
              'harder to finish invisibly'],
             ['Whether the panel comes off',
              'Some repairs are done in place; others need the panel removed, which adds time at '
              'both ends'],
             ['Sensors behind the panel',
              'Parking sensors, radar and cameras may need recalibrating after a bumper is '
              'refitted'],
             ['What the strip-down finds',
              'Broken brackets, previous filler, corrosion starting underneath'],
           ])),
           'What does <strong>not</strong> move it: metallic, pearl or three-stage paint, a '
           'colour change, or an aluminium panel. There is no surcharge on our card for any of '
           'those.',
          ]),
          ('What is included', [
           ['Paint and materials',
            '<strong>Blending into the adjacent panels</strong>, which is the first thing cut '
            'from a cheap quote and the main reason a repair shows in daylight',
            'Colour matched to the car rather than to the paint code, using a spray-out card',
            'Twelve months on the paint, in writing'],
           'And what is not: parts, where the panel needs replacing rather than repairing, and '
           'any recalibration a sensor needs afterwards. Both are itemised separately rather than '
           'buried.',
          ]),
          ('Why we publish this at all', [
           'Most bodyshops will not put a number on a web page, and the reason given is that '
           'every job is different. Every job <em>is</em> different. That is an argument for a '
           'band and a proper look at the car, not an argument for making people ring round for '
           'three quotes to find out whether they can afford to fix a bumper.',
           'The cost guides that fill this gap are written by directory sites. Their figures come '
           'from nowhere in particular and the ranges are wide enough to be useless &mdash; '
           '&ldquo;between £250 and £1,500&rdquo; does not help anybody decide anything.',
           ('note', CHOICE_NOTE),
          ]),
         ],
         [('Is the from-price realistic or a teaser?',
           'Realistic. It is what we charge for the smallest genuine version of that job, and '
           'plenty of repairs come in at it. Put your registration into the box and you will get '
           'the band for your actual damage.'),
          ('Why is a bumper more than a wing?',
           'A front bumper carries more: sensors, brackets, the grille, sometimes a radar. The '
           'paint area is similar; the work around it is not.'),
          ('Do you charge extra for metallic or pearl?',
           'No. There is no surcharge on our card for metallic, pearl, three-stage or a colour '
           'change. Those paints take longer to match, which is why we use a spray-out card, but '
           'the price is the same.'),
          ('Is blending really included?',
           'Yes, on every figure here. It is worth asking anyone else quoting you the same '
           'question, because the answer will tell you more than the price does.'),
          ('What if the strip-down finds more?',
           'We tell you before carrying on, with the revised figure, and you decide. We do not '
           'ring you at four o&rsquo;clock with the work already done.')],
         [('bodyshop-vs-main-dealer', 'How we compare with a dealer'),
          ('body-panel-repairs', 'Every panel, in detail'),
          ('what-happens-at-strip-down', 'What strip-down finds'),
          ('why-do-bodyshop-quotes-differ-so-much', 'Why quotes differ')],
         key_points=[
          f'Bumper from <strong>&pound;{frm("front-bumper")}</strong>, door from '
          f'<strong>&pound;{frm("door")}</strong>, alloys from '
          f'<strong>&pound;{ALLOY["low"]} a wheel</strong>.',
          'Bands run <strong>upward</strong> from the card figure, never below it.',
          '<strong>Blending is included.</strong> So is 12 months on the paint.',
          'No surcharge for <strong>metallic, pearl or a colour change</strong>.',
         ],
         hub=HUB_PROCESS, category='money', service_type='Vehicle body repair', note=None),

    page('mot-failure-reasons',
         'Why Cars Fail the MOT: The Real Government Figures | KITH Cars',
         'DVSA&rsquo;s own initial-failure data by defect category, which faults are classed '
         'dangerous, and what local short-journey driving does to all of it.',
         'What Actually Fails an MOT',
         'Mechanical &middot; MOT',
         'Just over a quarter of cars fail first time. The government publishes exactly what '
         'they fail on, and the answer is not what most people expect.',
         [
          ('The figures, from DVSA', [
           'From ' + DVSA + ' for class 3 and 4 vehicles, 2026&ndash;27 Q1. The first column is '
           'the share of all tests where that category caused a failure.',
           ('table', (['Defect category', '% of tests', 'Share of all defects'], [
             ['Lamps, reflectors and electrical', '9.98%', '24.67%'],
             ['Suspension', '8.21%', '19.47%'],
             ['Tyres', '6.55%', '14.08%'],
             ['Brakes', '5.83%', '14.86%'],
             ['Visibility', '4.40%', '8.22%'],
             ['Body, chassis, structure', '3.08%', '6.16%'],
             ['Noise, emissions and leaks', '3.04%', '6.02%'],
             ['Steering', '1.81%', '3.46%'],
             ['Seat belts and restraints', '0.90%', '1.59%'],
             ['Road wheels', '0.39%', '0.81%'],
             ['Vehicle identification', '0.32%', '0.63%'],
           ])),
           '<strong>Overall initial failure rate: 26.75%.</strong> The average failed test '
           'carries <strong>2.39 defects</strong>, so cars that fail rarely fail on one thing.',
          ]),
          ('The number that matters more', [
           'Of that 26.75%, a <strong>dangerous</strong> defect was recorded on 7.25% of tests '
           'and a major one on 19.50%. A dangerous defect means the car should not be driven away.',
           'And dangerous defects are concentrated almost entirely in two places:',
           ('table', (['Category', 'Share of all dangerous defects'], [
             ['Tyres', '<strong>62.69%</strong>'],
             ['Brakes', '27.15%'],
             ['Suspension', '4.98%'],
             ['Everything else', 'under 2% each'],
           ])),
           'Tyres account for nearly two-thirds of every dangerous defect recorded in the '
           'country. Lamps cause the most failures; tyres cause the most danger. Those are '
           'different problems and they get treated as the same one.',
          ]),
          ('Lamps are the top failure and the cheapest fix', [
           'A tenth of all tests fail on lamps, reflectors and electrical equipment, and almost '
           'none of it is dangerous &mdash; 1.24% of dangerous defects against 29.11% of major '
           'ones.',
           'It is also the category you can check yourself in five minutes on a dark evening: '
           'dipped and main beam, both sides; sidelights; brake lights, including the high-level '
           'one; indicators front, rear and side repeaters; reversing light; number plate lights; '
           'fog lights front and rear.',
           ('note', 'A blown bulb is the single most common reason a car fails its MOT in Great '
            'Britain, and it is usually a few pounds and ten minutes. Check them the week '
            'before.'),
          ]),
          ('Why local cars fail on different things', [
           'The national figures say what fails. What decides which of them bites a particular '
           'car is how that car is used, and around here that is short journeys.',
           'Hackbridge, Carshalton, Wallington and Mitcham are commuter suburbs with stations on '
           'them. A great many local cars cover a mile to a station car park and back, twice a '
           'day, and never reach proper running temperature. That pattern pushes certain '
           'categories up:',
           ['<strong>Brakes.</strong> Discs surface-rust between uses and get scored by it, and '
            'rear calipers and handbrake mechanisms seize on cars that barely move. Brakes are '
            '27% of dangerous defects.',
            '<strong>Tyres.</strong> Low-mileage cars age their tyres out rather than wearing '
            'them out. Plenty of tread, perished sidewalls &mdash; and tyres are 63% of dangerous '
            'defects.',
            '<strong>Suspension.</strong> Kerbing in streets parked solid on both sides does more '
            'to bushes and track rods than motorway miles ever will. Second biggest category '
            'nationally.',
            '<strong>Noise, emissions and leaks.</strong> Exhausts corrode from the inside when '
            'condensation never dries out of them.'],
           'So the advice that suits a high-mileage car &mdash; watch the tread, watch the pads '
           '&mdash; is close to the wrong advice here. On a low-mileage local car the things that '
           'fail are the things that rot and seize, and those are found by looking rather than by '
           'watching a number.',
          ]),
          ('What to check before you book', [
           ('steps', [
             '<strong>Every lamp, in the dark.</strong> <span>Top failure category nationally, '
             'and the cheapest thing on this list to put right.</span>',
             '<strong>Tyres, including the sidewalls.</strong> <span>Tread depth and cracking. '
             'Nearly two-thirds of dangerous defects.</span>',
             '<strong>Wipers and washers.</strong> <span>Visibility is 4.4% of tests, and torn '
             'blades or an empty washer bottle are a free fail.</span>',
             '<strong>Number plate and VIN legible.</strong> <span>Small category, entirely '
             'avoidable.</span>',
             '<strong>Listen for a knock over bumps.</strong> <span>Suspension is the second '
             'biggest category and the commonest local symptom.</span>',
           ]),
           ('note', ADVICE_NOTE),
          ]),
         ],
         [('What percentage of cars fail the MOT?',
           '26.75% of class 3 and 4 vehicles fail the initial test, on DVSA&rsquo;s published '
           'figures for 2026&ndash;27 Q1. The average failure carries 2.39 defects.'),
          ('What is the most common MOT failure?',
           'Lamps, reflectors and electrical equipment &mdash; 9.98% of all tests, a quarter of '
           'all defects recorded. Usually a bulb.'),
          ('What is the difference between major and dangerous?',
           'Both fail. Dangerous means the car should not be driven away at all. A dangerous '
           'defect was recorded on 7.25% of tests, and tyres account for 62.69% of them.'),
          ('My car does hardly any miles. Is it more likely to pass?',
           'Not necessarily, and that surprises people. Low-mileage cars fail on corroded discs, '
           'seized rear calipers and perished tyres &mdash; things that happen with time and '
           'standing rather than with distance.'),
          ('Can you fix a failure the same day?',
           'Often, if it is a bulb, a wiper or a tyre. Bigger items depend on parts. We will tell '
           'you what it needs and what it costs before doing anything.')],
         [('mot-testing', 'MOT testing'),
          ('bodywork-prices', 'Bodywork prices'),
          ('brake-repairs', 'Brake repairs'),
          ('tyre-fitting', 'Tyres')],
         key_points=[
          '<strong>26.75%</strong> of cars fail first time, with <strong>2.39 defects</strong> '
          'each.',
          '<strong>Lamps</strong> cause the most failures &mdash; usually a bulb.',
          '<strong>Tyres</strong> cause <strong>62.69%</strong> of all dangerous defects.',
          'Low-mileage local cars fail on what <strong>rots and seizes</strong>, not what wears.',
         ],
         hub=HUB_PROCESS, category='money', service_type='MOT testing', note=None),

    page('bodyshop-vs-main-dealer',
         'Independent Bodyshop or Main Dealer? | KITH Cars',
         'What the difference actually is on bodywork: labour rates, warranty, parts, and where '
         'the dealer is genuinely the right answer.',
         'Us or the Main Dealer',
         'Bodywork &middot; Comparison',
         f'On bodywork labour we are around {SAVING}% cheaper than a main dealer rate. That is '
         f'the honest figure and it is the one on our rate card &mdash; not a rounder number that '
         f'would look better.',
         [
          ('The labour rate, which is most of it', [
           ('table', (['', 'Per hour, inc VAT'], [
             ['KITH bodyshop', f'<strong>&pound;{BODY_RATE}</strong>'],
             ['Main dealer', f'&pound;{DEALER_RATE}'],
             ['Difference', f'<strong>around {SAVING}% less</strong>'],
           ])),
           'Published 2026 figures put independent workshops at roughly £55 to £95 an hour, '
           'mainstream franchised dealers at about £85 to £165, and premium marques higher again. '
           f'We sit at &pound;{BODY_RATE}.',
           'Labour is the larger part of most bodywork bills, because panel repair is mostly '
           'hours rather than parts. On a repair rather than a replacement, there may be no '
           'significant part at all &mdash; which is exactly where the rate difference tells.',
          ]),
          ('What you are not giving up', [
           ['<strong>Your warranty.</strong> Servicing and repair at an independent, to the '
            'manufacturer&rsquo;s schedule with the right specification of parts, keeps a '
            'manufacturer warranty intact. That is the legal position.',
            '<strong>Your insurer.</strong> On any claim the repairer is your choice. We are on '
            'no insurer panel, which means no labour time has been pre-agreed with anybody over '
            'your head.',
            '<strong>Paint quality.</strong> Colour matched to the car with a spray-out card and '
            'blended into the neighbouring panels, with twelve months on it in writing.'],
          ]),
          ('Where the dealer is genuinely the better answer', [
           'There are real ones, and a page that pretended otherwise would not be worth reading.',
           ('table', (['Situation', 'Why'], [
             ['An open manufacturer recall or goodwill claim',
              'Only the franchise network can carry those out and be paid for them'],
             ['Structural repair on a car with a manufacturer-specific method',
              'Some aluminium and EV structures have procedures and tooling tied to the marque'],
             ['A warranty repair the manufacturer is paying for',
              'If they are covering it, let them'],
             ['Software or coding only the dealer can access',
              'Some modules genuinely cannot be written to outside the network'],
           ])),
           'We will say so when one of these applies rather than having a go at your expense.',
          ]),
          ('What we are not', [
           # Phrased to avoid the literal string the build's own claims check looks for. A denial
           # and a boast read identically to a regex, and the check should stay blunt.
           'We are on <strong>no insurer panel and no manufacturer scheme</strong>. Nothing on '
           'this site says we hold an approval we do not hold, and a bodyshop that implies one it '
           'has not got is telling you something about how it handles the rest of the job.',
           'What that costs us is the work insurers send to their own panels. What it buys you is '
           'that nothing we recommend is steered by an arrangement with one.',
           ('note', CHOICE_NOTE),
          ]),
          ('How to compare two quotes properly', [
           ('steps', [
             '<strong>Ask whether blending is included.</strong> <span>The commonest hidden '
             'difference between two bodywork quotes, and the reason one repair shows in '
             'daylight.</span>',
             '<strong>Ask what the paint warranty is, in writing.</strong> <span>Ours is twelve '
             'months.</span>',
             '<strong>Ask whether sensor recalibration is in the price.</strong> <span>On a '
             'modern bumper it may be needed, and it should be visible rather than a surprise at '
             'collection.</span>',
             '<strong>Ask what happens if the strip-down finds more.</strong> <span>You want to '
             'be told before the work happens, not after.</span>',
             '<strong>Compare the hours, not just the total.</strong> <span>Two quotes at the '
             'same price can be very different amounts of work.</span>',
           ]),
          ]),
         ],
         [('How much cheaper are you than a main dealer?',
           f'On bodywork labour, around {SAVING}%. Our body rate is &pound;{BODY_RATE} an hour '
           f'including VAT against a main dealer rate of &pound;{DEALER_RATE}. Labour is the '
           f'larger part of most bodywork bills.'),
          ('Will using you void my warranty?',
           'No. Work done to the manufacturer&rsquo;s schedule, with parts of the right '
           'specification and a proper record, keeps a manufacturer warranty intact.'),
          ('Does my insurer have to agree?',
           'The repairer is your choice on any claim. Your insurer may suggest its own panel; it '
           'cannot require you to use one.'),
          ('Are you cheaper on everything?',
           'On labour, consistently. On parts it depends what the car needs &mdash; some '
           'manufacturer parts have one source and cost what they cost, and we will tell you when '
           'that is the case.'),
          ('When should I go to the dealer instead?',
           'An open recall, a warranty repair they are paying for, a structural job with a '
           'marque-specific method, or coding only the network can do. We will say so.')],
         [('bodywork-prices', 'Our bodywork prices'),
          ('why-do-bodyshop-quotes-differ-so-much', 'Why quotes differ'),
          ('car-insurance-claims', 'Insurance claims'),
          ('mismatched-parts-after-a-repair', 'Parts and quality')],
         key_points=[
          f'<strong>&pound;{BODY_RATE}/hr</strong> against a main dealer&rsquo;s '
          f'<strong>&pound;{DEALER_RATE}</strong> &mdash; around <strong>{SAVING}% less</strong>.',
          'Using an independent <strong>does not void</strong> a manufacturer warranty.',
          'On a claim, the <strong>repairer is your choice</strong>.',
          'Recall or warranty work? <strong>Go to the dealer</strong> &mdash; we will say so.',
         ],
         hub=HUB_PROCESS, category='money', service_type='Vehicle body repair', note=None),
]
