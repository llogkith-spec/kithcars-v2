#!/usr/bin/env python3
"""The three modern bodywork questions: sensors, aluminium and electric cars.

These are explainers, not service pages. None of them claims KITH does the work in-house, because
nobody has told me whether we calibrate here or sublet it, whether we hold the aluminium kit, or
what our high-voltage position is. A page that quietly implies any of those is the kind of claim
that costs you a customer at the counter. Every CTA here is "bring it in and we will tell you",
which is true, and the content earns its ranking by explaining the thing properly rather than by
claiming to do it.

Trigger lists for ADAS are corroborated across two independent trade sources. No calibration
speeds or target distances appear here, because neither source stated them and a number invented
for a safety system is worse than no number.
"""
import json
import pathlib

from bw_lib import page, HUB_PROCESS, ADVICE_NOTE

PRICES = json.loads((pathlib.Path(__file__).resolve().parent / 'bodyprices.json').read_text())


def m(panel, dmg='dent', band='medium'):
    p = PRICES[f'{panel}|{dmg}|{band}']
    return f'&pound;{p["low"]}', f'&pound;{p["high"]}'


fbl, fbh = m('front-bumper', 'scuff')

ASK_NOTE = ('Bring the car in, or put the registration in below, and we will tell you which of '
            'these apply to your repair before anything is agreed. Where a job needs work we do '
            'not carry out ourselves, we say so rather than finding out halfway through.')

PAGES = [

    page('aluminium-body-repair',
         'Aluminium Body Panel Repair: Why It Is a Different Job | KITH Cars',
         'Why aluminium panels cannot be repaired like steel, what galvanic corrosion is, and '
         'which cars have aluminium bodies.',
         'Aluminium Panels Are Not Thin Steel',
         'Bodywork &middot; Materials',
         'Aluminium does not dent like steel, does not spring back like steel, and corrodes if it '
         'so much as meets steel dust. It is a genuinely different repair, and knowing whether '
         'your car has it matters before anyone quotes.',
         [
          ('Which cars have it', [
           'Aluminium turns up three ways: a full aluminium body, selected panels on an otherwise '
           'steel car, or mixed structure.',
           ('table', (['', 'Typical examples'], [
             ['Largely aluminium bodies',
              'Jaguar XE, XF and F-Pace; Range Rover and Range Rover Sport; Audi A8; Tesla '
              'Model S'],
             ['Aluminium bonnets or wings on steel cars',
              'Common across premium marques from the 2010s, and on some mainstream models for '
              'weight saving'],
             ['Mixed structure',
              'Increasingly normal &mdash; aluminium outer panels over a steel or high-strength '
              'steel shell'],
           ])),
           'The middle row is the one that catches people. A car can have an aluminium bonnet and '
           'steel everything else, so the same dent is two different jobs depending on which '
           'panel it landed on. A magnet settles it in two seconds.',
          ]),
          ('Why the repair differs', [
           ['<strong>No memory.</strong> Steel has a degree of spring to it and wants to return '
            'toward its original shape. Aluminium does not. It stays where it is pushed, which '
            'changes how a dent is worked out.',
            '<strong>It work-hardens.</strong> Every time aluminium is moved it gets harder and '
            'more brittle in that spot. Work it too much and it cracks rather than straightens, '
            'and a crack in a panel is not recoverable.',
            '<strong>Heat is unforgiving.</strong> Aluminium loses strength at lower temperatures '
            'than steel and gives you almost no visual warning, because it does not glow through '
            'colours as it heats. Too much heat and the panel is weaker than it looks.',
            '<strong>It is joined differently.</strong> A great deal of aluminium structure is '
            'riveted and bonded rather than spot welded, so a structural repair follows the '
            'manufacturer&rsquo;s procedure for rivet type and adhesive rather than a welder '
            'setting.'],
          ]),
          ('Steel dust is the real hazard', [
           'Put steel filings on aluminium, add moisture, and you get galvanic corrosion: the two '
           'metals in contact with an electrolyte form a cell and the aluminium corrodes. It '
           'starts as pinprick blisters under the paint and it does not stop.',
           'This is why aluminium work is kept away from steel work &mdash; separate area, '
           'separate tools, separate extraction. Not fussiness. A shop that grinds steel in the '
           'same bay with the same kit is seeding corrosion into the panel it just repaired, and '
           'it will not show up for a year.',
           ('note', 'If your car has aluminium panels, ask any bodyshop how they keep steel and '
            'aluminium apart. It is a fair question and the answer tells you a lot.'),
          ]),
          ('What it means for cost and time', [
           'Expect both to be higher than the equivalent steel repair, for reasons that are '
           'structural rather than opportunistic: the work is slower, the margin for error is '
           'smaller, the consumables differ, and more jobs end at replacement rather than repair '
           'because a work-hardened or cracked panel cannot be saved.',
           'The honest version is that an aluminium wing with a sharp crease is more often a '
           'replacement than the same damage in steel. That is not a sales position, it is what '
           'the metal does.',
           ('note', ASK_NOTE),
          ]),
         ],
         [('How do I know if my panel is aluminium?',
           'A fridge magnet. It will not stick to aluminium. Try the bonnet and a door separately '
           'on the same car, because they are often different.'),
          ('Can an aluminium dent be pushed out?',
           'Sometimes, carefully, and with the knowledge that the metal gets harder each time it '
           'moves. It is not the repeated gentle persuasion that works on steel.'),
          ('Why is my quote higher than my friend&rsquo;s for the same dent?',
           'If one car has an aluminium panel and the other does not, that is why. Same damage, '
           'different metal, different job.'),
          ('Is aluminium weaker?',
           'No &mdash; it is used because it is light and strong. It is less forgiving to repair, '
           'which is a different thing from being weak.'),
          ('Does it rust?',
           'Not like steel, but it corrodes, particularly where it has met steel or had steel '
           'dust on it. The result looks like blistering under the paint rather than brown '
           'bubbling.')],
         [('bodywork-repair-process', 'The repair process'),
          ('adas-recalibration-after-bodywork', 'Sensors and calibration'),
          ('car-dent-repair', 'Dent repair'),
          ('supplementary-estimate-explained', 'Supplementary estimates')],
         key_points=[
          'A <strong>magnet</strong> tells you in two seconds, and panels differ on one car.',
          'Aluminium <strong>work-hardens and cracks</strong> rather than springing back.',
          '<strong>Steel dust causes galvanic corrosion</strong> &mdash; the work has to be kept '
          'separate.',
          'More jobs end at <strong>replacement</strong> than the same damage in steel.',
         ],
         hub=HUB_PROCESS, category='tech', service_type='Vehicle body repair', note=None),

    page('electric-car-body-repair',
         'Electric Car Body Repair: What Changes | KITH Cars',
         'High-voltage isolation, structural battery packs, why underside impacts matter more, '
         'and why EVs get written off at damage levels that would be repaired on a petrol car.',
         'Electric Cars and Bodywork',
         'Bodywork &middot; Electric and hybrid',
         'Most panel damage on an EV is an ordinary panel repair. The three things that are not '
         'ordinary are the high-voltage system, the floor, and what an insurer does when the pack '
         'is involved.',
         [
          ('The parts that are just bodywork', [
           'A scuffed bumper, a dented door, a kerbed alloy, a creased wing on an electric car is '
           'the same repair as on anything else. Same panel, same preparation, same paint, same '
           'price band. There is no electric surcharge on a door skin.',
           'What changes is everything that routes near or through the floor, and what happens '
           'when the impact was underneath.',
          ]),
          ('High voltage, in plain terms', [
           'An EV carries a battery pack at several hundred volts, and the cabling that connects '
           'it is sheathed in bright orange so that nobody can claim they did not notice. The '
           'rules are straightforward:',
           ['Orange cable is live until the system has been formally isolated',
            'Isolation is a procedure with a sequence and a waiting period, not a switch',
            'Anyone working near the pack, the cabling or the orange-marked components needs the '
            'training for it',
            'Welding and heat near a pack has its own restrictions'],
           'For a bumper scuff none of this comes into it. For anything that touches the floor, '
           'the sills, or the underside, all of it does.',
          ]),
          ('The floor is structural', [
           'On a purpose-built EV platform the battery pack is not a box bolted under the car. It '
           'is a structural member that the body is built around, and it contributes stiffness.',
           'Two consequences follow. A side impact at sill height is a more serious event than '
           'the same impact on a petrol car, because the sill is protecting the pack. And any '
           'underside impact &mdash; a kerb taken hard, a high verge, debris, flooding &mdash; '
           'needs the pack looked at rather than assumed to be fine.',
           ('note', 'If you have grounded an electric car hard enough to hear it, get the '
            'underside inspected even if nothing looks wrong and no warning appeared. Pack damage '
            'is not always visible and not always immediate.'),
          ]),
          ('Why EVs get written off sooner', [
           'This is the part owners find out at the worst moment. A damaged battery pack is '
           'frequently a large fraction of what the whole car is worth, so an impact that would '
           'be an economical repair on a petrol car can total an EV.',
           ('steps', [
             '<strong>The pack gets inspected.</strong> <span>Where the manufacturer requires '
             'replacement rather than repair, that is the figure.</span>',
             '<strong>Pack cost goes into the estimate.</strong> <span>And it can exceed the '
             'remaining value of the car on its own.</span>',
             '<strong>The insurer compares that to the market value.</strong> <span>The same sum '
             'as any other write-off decision.</span>',
             '<strong>It is categorised.</strong> <span>Usually S or N depending on whether '
             'structure was involved. Our write-off pages cover what each means.</span>',
           ]),
           'Worth knowing before you decide whether to claim at all: on an EV the threshold for a '
           'write-off is nearer than it feels.',
          ]),
          ('Weight, and what it does to damage', [
           'An electric car of a given size weighs noticeably more than its petrol equivalent, '
           'and that weight has to go somewhere in an impact. The practical effect is more damage '
           'from the same shunt &mdash; deeper deformation, more components involved, and brakes '
           'and tyres that wear differently.',
           'It also matters for recovery. An EV with a damaged pack has its own handling and '
           'parking requirements, and it is not a car to leave in a tight space on a whim.',
           ('note', ASK_NOTE),
          ]),
         ],
         [('Can you repair the panels on my EV?',
           'Panel and paint work on an electric car is ordinary panel and paint work. Where a job '
           'requires high-voltage isolation or pack involvement we will tell you straight what we '
           'will and will not be doing ourselves.'),
          ('I scraped the underside on a kerb. Is that serious?',
           'On an EV, get it looked at. The pack is down there and it is structural. No warning '
           'light does not mean no damage.'),
          ('Is bodywork more expensive on an electric car?',
           'Not for ordinary panels. It becomes more expensive the moment the floor, the sills or '
           'the pack are involved.'),
          ('My EV was written off after a small-looking knock. Why?',
           'Almost always the pack. If replacement was specified, that cost alone can exceed what '
           'the car is worth, and the write-off follows arithmetic rather than appearance.'),
          ('Does a hybrid count?',
           'It has a high-voltage system and orange cabling, so the isolation rules apply, but '
           'the pack is usually smaller and not structural. Less of the above applies, but not '
           'none of it.')],
         [('bodywork-repair-process', 'The repair process'),
          ('category-s-write-off', 'Category S explained'),
          ('category-n-write-off', 'Category N explained'),
          ('adas-recalibration-after-bodywork', 'Sensors and calibration')],
         key_points=[
          'Ordinary panel damage is an <strong>ordinary repair</strong>, at ordinary prices.',
          '<strong>Orange cable is live</strong> until the system is formally isolated.',
          'The <strong>pack is structural</strong>, so underside and sill impacts are serious.',
          'Pack cost means EVs are <strong>written off sooner</strong> than petrol equivalents.',
         ],
         hub=HUB_PROCESS, category='tech', service_type='Vehicle body repair', note=None),

    page('car-paint-code-colour-match',
         'Find Your Car Paint Code and Why Colours Are Hard to Match | KITH Cars',
         'Where the paint code sticker lives on common marques, why the code alone is not enough, '
         'and which colours give bodyshops trouble.',
         'Paint Codes, and Why the Code Is Only the Start',
         'Bodywork &middot; Paint',
         'Your car has a paint code on a sticker somewhere. It is necessary and it is not '
         'sufficient, because the paint on your car is no longer the colour it left the factory.',
         [
          ('Where the sticker usually is', [
           'It varies by marque and by model year, so treat this as where to look first rather '
           'than gospel.',
           ('table', (['Marque', 'Usually'], [
             ['Volkswagen, Audi, Skoda, SEAT',
              'Boot &mdash; in the spare wheel well, under the floor panel, or on the service book'],
             ['BMW and Mini', 'Under the bonnet, on the strut tower or slam panel'],
             ['Mercedes-Benz', 'Under the bonnet, or on the driver&rsquo;s door shut'],
             ['Ford', 'Driver&rsquo;s door shut, on the B-pillar sticker'],
             ['Vauxhall', 'Under the bonnet, or in the boot'],
             ['Toyota, Honda, Nissan, Mazda',
              'Door shut or door jamb sticker, driver&rsquo;s side'],
             ['Anything else', 'Door shuts first, then under the bonnet, then the boot'],
           ])),
           'The code is usually two or three characters, sometimes with a name beside it. If you '
           'cannot find it, the reliable fallback is the registration or the VIN &mdash; put the '
           'registration in the box below and we can look it up rather than you crawling round '
           'the car with a torch.',
          ]),
          ('Why the code is not enough on its own', [
           'Two reasons, and both are about time rather than about paint.',
           ['<strong>Your car has faded.</strong> Ultraviolet light, washing and weather move the '
            'colour. A five-year-old car in a factory-correct colour is not the factory colour '
            'any more, and mixing exactly to the code produces a panel that is visibly newer than '
            'its neighbours.',
            '<strong>One code can have several variants.</strong> Manufacturers change supplier '
            'or batch mid-production, so the same code can exist in two or three recorded '
            'versions. The code narrows it down; it does not finish the job.'],
           'This is why a proper job involves a spray-out card &mdash; a test panel sprayed and '
           'held against the car in daylight &mdash; rather than mixing to the code and going '
           'straight onto the wing.',
          ]),
          ('Blending, and why a repair can cross panel lines', [
           'If one wing is painted to the exact edge of the panel and the door beside it is not '
           'touched, the join between them is where the eye goes. So paint is blended into the '
           'adjacent panel and faded out, which makes the transition gradual rather than a line.',
           'That is not padding the job. It is the reason you cannot see the repair afterwards, '
           'and an estimate that includes blending into neighbouring panels on a metallic is '
           'usually being honest rather than greedy.',
          ]),
          ('The colours that cause trouble', [
           ('table', (['Colour type', 'Why'], [
             ['Solid white, solid red', 'Straightforward, usually fine'],
             ['Silver and grey metallics',
              'The flake has to lie the same way or the panel changes shade with the light'],
             ['Pearls and three-stage',
              'Built in multiple coats, so the match depends on coat thickness as well as colour'],
             ['Bright reds that have aged',
              'Red pigment fades hardest of all, so an older red is often a long way from its '
              'code'],
             ['Factory matt and satin finishes',
              'Cannot be polished to correct a flaw, so the spray has to be right first time'],
           ])),
           'None of these are reasons not to repair. They are reasons a metallic or pearl repair '
           'takes longer and needs a spray-out, and reasons to be suspicious of anyone quoting a '
           'three-stage pearl at the same rate as a solid white.',
          ]),
         ],
         [('Can you match my colour exactly?',
           'We match to the car rather than to the code, using a spray-out card checked in '
           'daylight. On a faded metallic that means blending into the next panel so there is no '
           'edge to see.'),
          ('My code has worn off the sticker.',
           'The registration or VIN will get us there. Bring it in or put the reg in the box '
           'below.'),
          ('Why does a small repair need two panels painted?',
           'Because the paint is blended out rather than stopped at the panel edge. Stopping at '
           'the edge is what makes a repair visible.'),
          ('Is touch-up paint from the code any good?',
           'For a stone chip on a solid colour, it is fine and worth doing before rust starts. On '
           'a metallic or a faded panel it will not match, because it is mixed to the code and '
           'your car has moved on.'),
          ('How long until the paint is fully hard?',
           'Handling-hard quickly, fully cured over following weeks. We will tell you when to '
           'avoid polishing or waxing, which matters more than people think on fresh paint.')],
         [('bodywork-repair-process', 'The repair process'),
          ('how-to-tell-if-a-car-has-been-resprayed', 'Spotting a previous respray'),
          ('light-scratch-repair', 'Light scratch repair'),
          ('mismatched-parts-after-a-repair', 'Quality disputes')],
         key_points=[
          'Look in the <strong>door shuts, under the bonnet, then the boot</strong>.',
          'The code is a <strong>starting point</strong> &mdash; your paint has faded since.',
          'A proper job uses a <strong>spray-out card</strong> checked in daylight.',
          '<strong>Blending into the next panel</strong> is why you cannot see the repair.',
         ],
         hub=HUB_PROCESS, category='tech', service_type='Vehicle paint repair', note=None),
]
