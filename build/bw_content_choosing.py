#!/usr/bin/env python3
"""The questions people actually ask before they book a bodyshop.

Sourced from what UK drivers are asking on car forums rather than from keyword tools - the
quote-difference thread on SEAT Cupra, the bonnet repair thread on Overclockers, the respray
threads on MB Club and the Mini Forum. The figures quoted in those threads are other people's
quotes and are not repeated as fact. Where a price appears here it is ours, from the rate card.

Written to be answerable at a glance: the lead is the answer, the short-answer card carries the
specifics, and the detail follows. That shape is also what gets a page quoted rather than merely
listed.
"""
import json
import pathlib

from bw_lib import page, HUB_PROCESS, CHOICE_NOTE

PRICES = json.loads((pathlib.Path(__file__).resolve().parent / 'bodyprices.json').read_text())


def m(panel, dmg='dent', band='medium'):
    p = PRICES[f'{panel}|{dmg}|{band}']
    return f'&pound;{p["low"]}', f'&pound;{p["high"]}'


bl, bh = m('front-bumper')
bsl, bsh = m('front-bumper', 'scuff')
bnl, bnh = m('bonnet')

PAGES = [

    page('why-do-bodyshop-quotes-differ-so-much',
         'Why Do Bodyshop Quotes Differ So Much? | KITH Cars',
         'One quote £330, another £200 for the same bumper. The five things that actually differ, '
         'what each is worth, and the two questions that tell you which quote is real.',
         'Why Is One Quote Half the Price of the Other?',
         'The repair process &middot; Choosing',
         'Because they are usually quoting different work. Five things vary between bodyshop '
         'quotes, and four of them are invisible on the day you collect the car.',
         [
          ('The five things that differ', [
           ('table', (['What varies', 'Cheaper quote', 'What you lose'], [
             ['Panel on or off the car', 'Left on, masked around',
              'A paint edge at the masking line that shows when the seal moves'],
             ['Blending into next panel', 'Stopped at the shut line',
              'A visible step in shade, worst in sunlight on a metallic'],
             ['Where it is sprayed', 'Outdoors or on a driveway',
              'Dust and insects in the lacquer; overspray on the rest of the car'],
             ['Repair or replace', 'Filled rather than replaced',
              'Filler over a split flexes and cracks along the line within a year'],
             ['Behind the panel', 'Not looked at',
              'Broken mounting tabs, a bent crash bar, an untested sensor'],
           ])),
           'None of those show at handover. All of them show within a year, which is why the '
           'comparison people make on the day is not the comparison that matters.',
          ]),
          ('The two questions worth asking both shops', [
           ('steps', [
             '<strong>&ldquo;Does that include blending into the panels either side?&rdquo;</strong> '
             '<span>This single question separates most quotes. Blending is extra material, extra '
             'masking and time spent on panels that are not damaged, and leaving it out is '
             'invisible until the sun comes out.</span>',
             '<strong>&ldquo;Are you taking the bumper off or masking around it?&rdquo;</strong> '
             '<span>Off means the edges and the back get painted and the mounting tabs get '
             'checked. Masked means a line where the new paint stops.</span>',
           ]),
           'Two answers tell you more than two prices do. If one shop says yes to both and the '
           'other says no, you are not comparing like with like and the cheaper one is cheaper '
           'for a reason rather than out of generosity.',
          ]),
          ('Spraying outdoors', [
           'This is the one people underestimate. Paint is sprayed in a booth because the booth '
           'controls three things at once: dust, temperature and airflow. Outdoors you get none '
           'of them.',
           ['<strong>Dust and insects</strong> land in wet lacquer and stay there.',
            '<strong>Wind carries overspray</strong> onto the rest of your car, which is a '
            'second job to put right.',
            '<strong>Temperature</strong> decides how the paint flows and how the flake in a '
            'metallic lies down. A cold morning and a warm afternoon give different colours from '
            'the same tin.',
            '<strong>Nothing bakes.</strong> Lacquer that air-dries keeps shrinking for weeks, '
            'which is why the outline of the repair sometimes appears a month later.'],
          ]),
          ('When the cheaper quote is the right one', [
           'Not every job needs a booth, and we would rather say so than pretend otherwise.',
           'A small scuff in the middle of a bumper, on a car you are not precious about, '
           'repaired on your drive for less than half what we would charge, is a perfectly '
           'rational choice. Mobile repairers do a lot of that work and some of them do it well.',
           'What it does not suit is a crack, a panel edge, a metallic that has to match its '
           'neighbours, or anything where the mounting points may have gone. Those are the jobs '
           'where the cheap quote becomes the expensive one.',
          ]),
          ('What our figures include', [
           f'A bumper scuff runs {bsl} to {bsh} and a dented or cracked bumper {bl} to {bh}, '
           f'including VAT. Both include taking the bumper off the car, blending into both front '
           f'wings, baking, and checking the mounting tabs and any sensors behind it.',
           'We do not quote a lower number by leaving the blend out and explaining afterwards. '
           'If you get a quote from us and a cheaper one from someone else, ask them the two '
           'questions above and you will usually find the difference.',
           ('note', CHOICE_NOTE),
          ]),
         ],
         [('Is a £130 difference worth it?',
           'It depends entirely which of the five things above the £130 buys. If it buys blending '
           'and the panel coming off, yes. If both shops are doing the same work and one is '
           'simply cheaper, no.'),
          ('They quoted from photographs. Is that reliable?',
           'For a price band, yes. For a firm figure, less so &mdash; no photograph shows a bent '
           'crash bar behind an intact bumper or a broken mounting tab. A shop that has seen the '
           'car is quoting on more information.'),
          ('Should I just get more quotes?',
           'Three is plenty, and ask all three the same two questions. More quotes without those '
           'questions just gives you more numbers that are not comparable.'),
          ('Why is a main dealer so much more?',
           'Higher labour rates and genuine parts at list price. The work is usually good; you '
           'are paying for the overhead as much as the repair.'),
          ('Can I see where the work gets done?',
           'Ask. A shop proud of its booth will show you it. That is a reasonable request and how '
           'it is received tells you something.')],
         [('mobile-smart-repair-or-bodyshop', 'Mobile repair or bodyshop?'),
          ('paint-blending-explained', 'Why we blend into the next panel'),
          ('bodywork-repair-process', 'The repair process, step by step'),
          ('front-bumper-repair-cost', 'Front bumper repair')],
         key_points=[
          'They are usually <strong>quoting different work</strong>, not the same work at '
          'different prices.',
          'Ask both: <strong>does that include blending?</strong> and <strong>is the panel coming '
          'off?</strong>',
          'Spraying outdoors means <strong>dust, overspray and nothing baked</strong>.',
          'Sometimes the cheap quote is right &mdash; a small scuff on a car you are not precious '
          'about.',
         ],
         hub=HUB_PROCESS, category='process', service_type='Vehicle body repair', note=None),

    page('mobile-smart-repair-or-bodyshop',
         'Mobile SMART Repair or a Bodyshop? | KITH Cars',
         'What SMART repair actually is, the damage it suits, the damage it does not, and how to '
         'tell which one yours is before you book either.',
         'Mobile SMART Repair, or a Bodyshop?',
         'The repair process &middot; Choosing',
         'SMART repair is a real technique with a real limit: small areas, away from edges, where '
         'the panel is sound underneath. Inside that limit it is excellent value. Outside it, it '
         'is a repair you pay for twice.',
         [
          ('What SMART actually stands for', [
           'Small to Medium Area Repair Technique. The point is in the name: it refinishes the '
           'damaged area and blends into the surrounding original paint, rather than painting the '
           'whole panel. Less material, less masking, less time, lower price.',
           'It is not a lesser version of a full repair. On the right damage it is the correct '
           'answer and a full panel respray would be overkill.',
          ]),
          ('The limit, in one table', [
           ('table', (['Damage', 'SMART', 'Why'], [
             ['Scuff on a bumper face', 'Good', 'Small, flat, away from edges'],
             ['Kerbed alloy', 'Good', 'Self-contained, standard process'],
             ['Scratch on a door, mid-panel', 'Good', 'Original paint all around it to blend into'],
             ['Dent in the middle of a bonnet', 'No', 'Large flat panel in daylight; a localised '
              'repair shows'],
             ['Anything to a panel edge', 'No', 'Nothing to blend into at the edge'],
             ['Cracked bumper', 'No', 'Needs welding from behind and reinforcing'],
             ['Rust', 'No', 'Has to be cut back to clean metal first'],
             ['Damage across two panels', 'No', 'Two repairs blended to meet'],
           ])),
          ]),
          ('The bonnet question specifically', [
           'A dented bonnet is the single most common thing people are offered a mobile repair '
           'for, and it is the one where we would most firmly say no.',
           'A bonnet is a large, flat, horizontal panel in full daylight &mdash; the second '
           'hardest panel on the car to match after the roof. A localised repair in the middle of '
           'it has nothing to hide behind. Metallics in particular show the join from across a '
           'car park, because the flake in the repaired area has not laid down the same way as '
           'the flake around it.',
           f'A bonnet done properly runs {bnl} to {bnh} including VAT on an ordinary five-seater, '
           f'painted complete and blended into both wings.',
          ]),
          ('Where it is done matters as much as how', [
           'A mobile repair happens on your driveway. That means no booth, so no control over '
           'dust, temperature or airflow, and wind carries overspray onto the rest of your car.',
           'For a small bumper scuff on a solid colour, that is often fine and thousands of them '
           'are done every week. For anything where the colour has to match across a large area, '
           'it is the difference between a repair you cannot find and one you can.',
          ]),
          ('How to tell which yours is', [
           ('steps', [
             '<strong>Is it smaller than your hand?</strong> <span>If not, SMART is already '
             'marginal.</span>',
             '<strong>Is it at least a hand&rsquo;s width from any edge or shut line?</strong> '
             '<span>A blend needs original paint all around it.</span>',
             '<strong>Is the panel sound underneath?</strong> <span>No crack, no rust, no '
             'previous filler.</span>',
             '<strong>Is it a flat horizontal panel in daylight?</strong> <span>Bonnet, roof or '
             'boot lid &mdash; if yes, be cautious whatever the size.</span>',
             '<strong>Is your paint a metallic, pearl or three-stage?</strong> <span>The harder '
             'the finish, the smaller the damage has to be for SMART to work.</span>',
           ]),
           'Four yeses and a solid colour: a mobile SMART repair is good value and we will tell '
           'you so. Any no: it is a bodyshop job, and doing it twice costs more than doing it '
           'once.',
           ('note', CHOICE_NOTE),
          ]),
         ],
         [('Do you do SMART repairs?',
           'Yes, in the workshop rather than on a driveway, which means a booth and a bake. For '
           'damage that genuinely suits the technique it is the cheapest thing on our rate card.'),
          ('A mobile repairer quoted half your price.',
           'For a small bumper scuff they may well be right and we will say so. Ask them what '
           'happens if it rains, where the overspray goes, and whether they can do it if the '
           'paint is cracked.'),
          ('Will a SMART repair last as long?',
           'On the right damage, yes &mdash; same primer, same basecoat, same two-pack lacquer. '
           'What fails is a SMART repair used on damage it does not suit.'),
          ('Can a SMART repair be done over a previous one?',
           'Sometimes, and it is worth telling whoever quotes that the panel has been done '
           'before. A paint depth gauge will show it anyway, and it changes the preparation.'),
          ('What if I have it done and it shows?',
           'Then it gets done properly, and you have paid twice. That is the whole case for '
           'matching the technique to the damage first.')],
         [('why-do-bodyshop-quotes-differ-so-much', 'Why quotes differ so much'),
          ('bonnet-repair-cost', 'Bonnet repair'),
          ('light-scratch-repair', 'Light scratch repair'),
          ('paint-blending-explained', 'Why we blend into the next panel')],
         key_points=[
          '<strong>Small to Medium Area Repair Technique</strong> &mdash; the limit is in the '
          'name.',
          'Good for: bumper scuffs, kerbed alloys, <strong>mid-panel</strong> scratches.',
          'No for: <strong>bonnets</strong>, panel edges, cracks, rust, damage across two panels.',
          'The harder your paint &mdash; metallic, pearl, three-stage &mdash; the <strong>smaller '
          'the damage has to be</strong>.',
         ],
         hub=HUB_PROCESS, category='process', service_type='SMART repair', note=None),

    page('how-to-tell-if-a-car-has-been-resprayed',
         'How to Tell if a Car Has Been Resprayed | KITH Cars',
         'Seven checks that reveal previous paintwork on a used car, what a paint depth gauge '
         'reading actually means, and which findings matter and which do not.',
         'How to Tell if a Car Has Been Resprayed',
         'The repair process &middot; Buying a used car',
         'Seven checks, and you can do five of them in a supermarket car park in ten minutes. '
         'A resprayed panel is not automatically a problem &mdash; what matters is what it was '
         'hiding.',
         [
          ('The five you can do with your eyes', [
           ('steps', [
             '<strong>Look along the car, not at it.</strong> <span>Crouch at one corner and '
             'sight down the flank. Ripples, waves and a change in how the light runs along the '
             'panel show up at an angle and vanish face-on.</span>',
             '<strong>Check the colour panel to panel in daylight.</strong> <span>Not under '
             'cover. A repainted panel that was matched indoors is often a shade out '
             'outside.</span>',
             '<strong>Look at the shut lines and rubbers.</strong> <span>Overspray on door '
             'seals, window rubbers, or a hard paint edge at the edge of a seal means the panel '
             'was masked rather than removed.</span>',
             '<strong>Open everything and look at the edges.</strong> <span>Door shuts, under '
             'the bonnet lip, inside the boot. Factory paint runs round the edge; a repaint '
             'often stops.</span>',
             '<strong>Look for texture.</strong> <span>Orange peel that is heavier on one panel '
             'than its neighbours, or a gloss that is slightly different, is a repainted '
             'panel.</span>',
           ]),
          ]),
          ('The two that need a tool', [
           '<strong>A paint depth gauge.</strong> They are inexpensive and they settle the '
           'question. Factory paint is usually fairly consistent around a car; a panel reading '
           'noticeably thicker than the others has been painted again, and a reading several '
           'times the others usually means filler underneath.',
           'What a gauge cannot tell you is why. A thicker reading on one wing might be a stone '
           'chip repair done well, or it might be filler over a crumpled panel. The number '
           'starts the conversation rather than finishing it.',
           '<strong>A magnet.</strong> Crude but free. It sticks to steel and not to filler, so '
           'a spot where it will not hold on an otherwise steel panel is worth a closer look. It '
           'tells you nothing on an aluminium panel or a plastic bumper, which is most of the '
           'front and rear of a modern car.',
          ]),
          ('What matters and what does not', [
           ('table', (['What you found', 'How worried to be'], [
             ['One bumper repainted', 'Barely. Bumpers get scuffed; it is the most repainted '
              'part on any car'],
             ['One wing or door repainted, neatly', 'Low. Bolt-on panels, often a car park '
              'repair'],
             ['A rear quarter repainted', 'Higher. It is welded to the shell, so the impact '
              'reached the body'],
             ['Several panels down one side', 'Higher. That is a collision, not a scuff'],
             ['Overspray on rubbers and shuts', 'A sign of a cheap repair, whatever was '
              'underneath'],
             ['Filler-thick readings on a structural area', 'Walk away or get it inspected '
              'properly'],
           ])),
          ]),
          ('The checks that come before all of this', [
           'A history check costs a few pounds and tells you whether the car has an insurance '
           'write-off recorded against it. That is a more reliable signal than anything you can '
           'see, because a Category S or N marker is recorded permanently.',
           'The MOT history on gov.uk is free and worth five minutes. Advisories about corrosion, '
           'and gaps in testing, tell their own story.',
           'If the car is worth it, pay for an inspection. We look at paint depth panel by panel, '
           'at the structure on a ramp, and at whether the shut lines are even on both sides '
           '&mdash; and we have no interest in whether you buy it.',
          ]),
         ],
         [('Does a respray mean the car was crashed?',
           'Not necessarily. The commonest reasons are a car park scuff, a kerbed bumper and '
           'vandalism. What tells you it was a collision is several panels on the same side, or a '
           'welded panel like a rear quarter.'),
          ('Is a repainted car worth less?',
           'A neatly repainted bumper, barely. A recorded write-off, considerably &mdash; and '
           'that is recorded whether or not you can see the repair.'),
          ('What depth reading is normal?',
           'It varies by manufacturer, so the useful comparison is between panels on the same '
           'car rather than against a universal number. Consistency is the signal.'),
          ('The seller says it was a stone chip repair.',
           'Plausible, and easy to check: stone chip repairs are on the leading edge of the '
           'bonnet and the front of the roof. A thick reading in the middle of a door is not a '
           'stone chip.'),
          ('Can you inspect a car before I buy it?',
           'Yes. Paint depth panel by panel, structure on a ramp, cold start, and a written '
           'report with photographs. We are not selling you the car, which is the point.')],
         [('why-repairs-dont-match', 'Why some repairs do not match'),
          ('car-write-off-categories-explained', 'Write-off categories explained'),
          ('selling-a-cat-s-or-cat-n-car', 'Selling a recorded write-off'),
          ('paint-colour-matching-explained', 'How paint matching works')],
         key_points=[
          '<strong>Sight along the car</strong>, do not look at it. Ripples show at an angle.',
          '<strong>Overspray on rubbers and shuts</strong> means the panel was masked, not '
          'removed.',
          'A depth gauge compares <strong>panel to panel on the same car</strong>, not to a '
          'universal number.',
          'A repainted bumper is normal. A repainted <strong>rear quarter</strong> is a '
          'collision.',
         ],
         hub=HUB_PROCESS, category='process', service_type='Pre-purchase inspection', note=None),
]
