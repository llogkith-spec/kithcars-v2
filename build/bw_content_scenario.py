#!/usr/bin/env python3
"""Damage where there is nobody to claim from.

The MIB pages carry the fact that almost nobody publishes plainly: under the Untraced Drivers
Agreement, your car damage is only recoverable where somebody was significantly injured. A
no-injury hit and run means no MIB money for the car, full stop. That is corroborated by two
independent legal sources (Harper Macleod and the Law Society Gazette) and it is the single most
useful thing we can tell someone who comes back to a damaged car in a car park.

The uninsured-driver excess figure is deliberately absent. The £400 is the untraced agreement's
figure and I have no current sourced figure for the uninsured one, so the page says an excess
applies and sends people to MIB rather than printing a number that might be wrong.

All five pages share one category so the uniqueness gate compares every pair - these scenarios
rhyme with each other and that is exactly what should be caught.
"""
import json
import pathlib

from bw_lib import page, HUB_PROCESS, ADVICE_NOTE, CHOICE_NOTE

PRICES = json.loads((pathlib.Path(__file__).resolve().parent / 'bodyprices.json').read_text())


def m(panel, dmg='dent', band='medium'):
    p = PRICES[f'{panel}|{dmg}|{band}']
    return f'&pound;{p["low"]}', f'&pound;{p["high"]}'


dl, dh = m('door', 'scuff')
dsl, dsh = m('door', 'smart', 'small')
MIB = '<a href="https://www.mib.org.uk" target="_blank" rel="noopener">Motor Insurers&rsquo; Bureau</a>'

PAGES = [

    page('hit-and-run-untraced-driver-car-damage',
         'Hit and Run: Can You Claim for Car Damage? | KITH Cars',
         'The Untraced Drivers Agreement only pays for vehicle damage where somebody was '
         'significantly injured. What that means if your car was hit and nobody stopped.',
         'Nobody Stopped. Who Pays for the Car?',
         'Bodywork &middot; Untraced drivers',
         'There is a national scheme for untraced drivers, and most people assume it covers their '
         'car. For damage only, with no injury, it does not. This is the rule worth knowing before '
         'you spend a week chasing it.',
         [
          ('The rule, stated plainly', [
           'The ' + MIB + ' runs the Untraced Drivers Agreement, which is the scheme for when the '
           'driver who hit you cannot be identified. Under it, damage to your vehicle is only '
           'recoverable where the same accident caused a <strong>significant injury</strong>.',
           ('table', (['', 'Under the Untraced Drivers Agreement'], [
             ['Injury claim', 'Recoverable'],
             ['Vehicle damage, with a significant injury in the same accident', 'Recoverable'],
             ['Vehicle damage, nobody injured', '<strong>Not recoverable</strong>'],
             ['Excess applied to property damage', '&pound;400'],
             ['Reporting to police', 'As soon as reasonably practicable, if MIB asks'],
           ])),
           'A significant injury means death, or injury needing two or more nights of inpatient '
           'treatment, or three or more outpatient sessions. A sore neck for a fortnight does not '
           'meet it.',
           ('note', 'So: car park shunt, nobody hurt, no note left, driver never identified. '
            'There is no MIB route for the repair. That is not us being unhelpful, it is the '
            'agreement.'),
          ]),
          ('What is actually left, then', [
           ('steps', [
             '<strong>Try hard to identify the driver first.</strong> <span>If you can, this '
             'becomes an ordinary third-party claim and everything changes. The next page covers '
             'where to look.</span>',
             '<strong>Check whether you are comprehensive.</strong> <span>If so, your own policy '
             'will repair the car, subject to your excess.</span>',
             '<strong>Work out whether claiming is worth it.</strong> <span>With no third party '
             'to recover from, your insurer cannot get its money back, so it is recorded as a '
             'fault claim and your no-claims takes the hit.</span>',
             '<strong>Get it priced for paying yourself.</strong> <span>On smaller damage this is '
             'very often the cheaper answer once the excess and the lost discount are counted. Put '
             'the registration in below.</span>',
           ]),
          ]),
          ('The sum most people get wrong', [
           'A scuffed door is ' + dl + ' to ' + dh + ' with us. Suppose your excess is £350 and '
           'claiming costs you two years of no-claims discount.',
           ('table', (['', 'Claim', 'Pay yourself'], [
             ['Excess', '£350', '—'],
             ['Repair', 'Insurer pays the rest', dl + ' – ' + dh],
             ['No-claims discount', 'Reduced, as a fault claim', 'Untouched'],
             ['Declarable on renewal', 'Yes, for five years', 'No claim to declare'],
           ])),
           'On a single panel the arithmetic usually says pay for it. On a car with damage down '
           'one whole side it usually says claim. Get the real number before deciding, because '
           'both answers are right in different circumstances.',
          ]),
          ('If somebody was hurt', [
           'Then the agreement does apply to the car as well, with a £400 excess on the property '
           'damage. Report it to the police, keep the crime reference, and make the MIB claim on '
           'their own form, which is now compulsory.',
           'That is a personal injury claim with a vehicle damage element attached, and it is '
           'worth taking proper advice rather than handling it off a web page.',
           ('note', ADVICE_NOTE),
          ]),
         ],
         [('Does my comprehensive policy cover a hit and run?',
           'Yes, for the damage, subject to your excess. The question is whether claiming costs '
           'you more than the repair, because with no third party it is recorded as a fault '
           'claim.'),
          ('Do I have to report it to the police?',
           'For an MIB claim, yes, if they ask, and as soon as reasonably practicable. For your '
           'own insurer, a crime reference number makes the claim go more smoothly whether or not '
           'it is required.'),
          ('What if I find the driver later?',
           'Then it stops being an untraced claim and becomes an ordinary third-party one, which '
           'is a much better position. Tell your insurer immediately.'),
          ('Will the MIB pay my excess back?',
           'Under the untraced agreement there is a £400 excess on property damage, and that '
           'applies to the claim itself. It is not a route to recovering your own policy excess '
           'on a no-injury claim, because that claim is not recoverable at all.'),
          ('Can I claim for the hire car I had to get?',
           'Only as part of a claim that is itself recoverable. If the vehicle damage is not '
           'recoverable because nobody was injured, the associated costs are not either.')],
         [('hit-by-uninsured-driver', 'Hit by an uninsured driver'),
          ('car-park-damage-no-note-left', 'Car park damage, no note'),
          ('non-fault-accident-what-to-do', 'Non-fault accidents'),
          ('door-repair-cost', 'Door repair cost')],
         key_points=[
          'No injury means <strong>no MIB claim for your car</strong>.',
          'Significant injury = <strong>2+ nights inpatient or 3+ outpatient sessions</strong>.',
          'Property damage excess under the scheme is <strong>£400</strong>.',
          'With no third party, an insurance claim is recorded as <strong>fault</strong>.',
         ],
         hub=HUB_PROCESS, category='scenario', service_type='Vehicle body repair', note=None),

    page('hit-by-uninsured-driver',
         'Hit by an Uninsured Driver: How to Get Your Car Repaired | KITH Cars',
         'The Uninsured Drivers Agreement is a different scheme from the untraced one, and it does '
         'cover vehicle damage. What to do, in order.',
         'The Other Driver Has No Insurance',
         'Bodywork &middot; Uninsured drivers',
         'Good news relative to a hit and run: you know who they are, so this is the uninsured '
         'scheme rather than the untraced one, and vehicle damage is recoverable under it.',
         [
          ('Two schemes, often confused', [
           ('table', (['', 'Uninsured driver', 'Untraced driver'], [
             ['You know who hit you', 'Yes', 'No'],
             ['Scheme', 'Uninsured Drivers Agreement', 'Untraced Drivers Agreement'],
             ['Vehicle damage covered', 'Yes', 'Only with a significant injury'],
             ['First thing to do', 'Get their details and check the MID',
              'Hunt for evidence of who they were'],
           ])),
           'People use &ldquo;MIB claim&rdquo; for both and the difference matters enormously. If '
           'you have a name and a registration, you are in the left-hand column and your car '
           'damage is recoverable.',
          ]),
          ('At the scene, in order', [
           ('steps', [
             '<strong>Get the details anyway.</strong> <span>Name, address, registration, and the '
             'make and colour. Legally they must give you their name and address. Photograph the '
             'car and the plate yourself rather than relying on what you are told.</span>',
             '<strong>Photograph everything.</strong> <span>Both cars, the positions, the wider '
             'scene, the road layout. Do it before anything is moved.</span>',
             '<strong>Get a witness if there is one.</strong> <span>A name and number. Uninsured '
             'drivers dispute liability more often than insured ones, because they have more to '
             'lose.</span>',
             '<strong>Report it to the police.</strong> <span>Driving without insurance is an '
             'offence, and you want the report.</span>',
             '<strong>Check the Motor Insurance Database.</strong> <span>The askMID service tells '
             'you whether a registration was insured. It is the difference between suspecting and '
             'knowing.</span>',
           ]),
          ]),
          ('Then pick your route', [
           ['<strong>Through your own comprehensive insurer.</strong> Usually the fastest. They '
            'repair the car, then pursue the uninsured driver themselves. Ask explicitly whether '
            'your excess and no-claims will be restored once liability is established &mdash; '
            'they often are, but get the answer before you commit.',
            '<strong>Through the MIB.</strong> The route if you are third-party only, or if your '
            'insurer will not pursue it. Vehicle damage is covered and an excess applies to it.',
            '<strong>Directly against the driver.</strong> Possible, and often not worth it. '
            'Someone driving uninsured frequently has nothing to recover from.'],
           ('note', CHOICE_NOTE),
          ]),
          ('The bit to watch on your own policy', [
           'An uninsured-driver claim can sit on your record as a fault claim while liability is '
           'being established, because your insurer has not recovered its money yet. That can '
           'affect a renewal that falls in the middle.',
           'Ask your insurer to confirm in writing what happens to your no-claims and your excess '
           'if recovery succeeds, and keep that confirmation. It is the thing people wish they '
           'had eighteen months later.',
           ('note', ADVICE_NOTE),
          ]),
         ],
         [('How do I check if a car is insured?',
           'The askMID service checks a registration against the Motor Insurance Database. Do it '
           'the same day &mdash; it tells you which scheme you are in.'),
          ('They gave me details but no insurance certificate.',
           'That is common and not conclusive either way. Check the MID rather than taking their '
           'word, and do not accept a promise to sort it privately before you have.'),
          ('Will my no-claims be affected?',
           'Possibly while liability is being settled, and often restored once your insurer '
           'recovers. Get the answer in writing before you claim.'),
          ('Can I use any bodyshop?',
           'Yes. Whichever route you go down, choosing the repairer is yours. We are on no '
           'insurer panel, so there is no arrangement pushing you anywhere.'),
          ('They have offered me cash to keep it quiet.',
           'Your call, but price the repair properly first. Cash offers at the roadside are '
           'reliably below what the job costs, and once you have accepted it the route back is '
           'hard.')],
         [('hit-and-run-untraced-driver-car-damage', 'Hit and run, nobody traced'),
          ('non-fault-accident-what-to-do', 'Non-fault accidents'),
          ('car-park-damage-no-note-left', 'Car park damage'),
          ('accident-repairs', 'Accident repairs')],
         key_points=[
          'Knowing who hit you puts you in the <strong>uninsured</strong> scheme, not the untraced '
          'one.',
          'Under it, <strong>vehicle damage is recoverable</strong>.',
          'Check the registration on <strong>askMID</strong> the same day.',
          'Get your insurer&rsquo;s position on <strong>excess and no-claims in writing</strong>.',
         ],
         hub=HUB_PROCESS, category='scenario', service_type='Vehicle body repair', note=None),

    page('car-park-damage-no-note-left',
         'Someone Hit My Car in a Car Park and Left | KITH Cars',
         'Where to find evidence in the first 48 hours, why CCTV has a clock on it, and how to '
         'decide between claiming and paying.',
         'Came Back to a Damaged Car and No Note',
         'Bodywork &middot; Car park damage',
         'The first two days decide whether you ever identify who did it, because footage gets '
         'overwritten and memories go. Everything on this page is ordered by how fast it '
         'disappears.',
         [
          ('Today, before anything else', [
           ('steps', [
             '<strong>Photograph it where it stands.</strong> <span>Wide shot showing the bay and '
             'the cars either side, then close shots of the damage, then the height of the damage '
             'against something for scale. Do not move the car first.</span>',
             '<strong>Note the exact time and bay number.</strong> <span>Anyone searching footage '
             'needs a window and a location, and &ldquo;Tuesday afternoon&rdquo; is not one.</span>',
             '<strong>Find the cameras.</strong> <span>Look up, properly. Car park cameras, shop '
             'cameras pointing at the entrance, cash machines, buses that stop alongside, and any '
             'nearby vehicle with a dashcam.</span>',
             '<strong>Ask the operator the same day.</strong> <span>Footage retention is often '
             'weeks rather than months, and the request has to be in before it cycles. Ask in '
             'writing and keep the reply.</span>',
             '<strong>Look for the paint.</strong> <span>Transferred paint on your panel tells '
             'you the other car&rsquo;s colour, and the height tells you roughly what kind of '
             'vehicle. Photograph it before anyone cleans it.</span>',
           ]),
          ]),
          ('What the damage itself tells you', [
           ('table', (['What you see', 'What it usually means'], [
             ['Horizontal scrape at bumper height', 'Another car reversing or manoeuvring'],
             ['Round dent at waist height, no scrape', 'A door being opened into yours'],
             ['Scuff high on the rear quarter', 'A larger vehicle, van or 4x4'],
             ['Paint transfer of a different colour', 'The other vehicle&rsquo;s colour, directly'],
             ['Long low scrape along the sill', 'A kerb or a bollard, not another car'],
           ])),
           'That last row is worth being honest with yourself about. Some car park damage is not '
           'somebody else.',
          ]),
          ('If you cannot identify them', [
           'Then you are in the untraced position, and the thing to know is that the national '
           'untraced drivers scheme does not pay for vehicle damage unless somebody was '
           'significantly injured. A no-injury car park shunt has no route through it.',
           'Which leaves your own comprehensive policy, or paying. And because there is nobody to '
           'recover from, an insurance claim here is recorded as a fault claim with the effect on '
           'your no-claims that implies.',
           ('table', (['Damage', 'Typical with us', 'Worth claiming?'], [
             ['Light scuff, paint not broken', dsl + ' – ' + dsh,
              'No &mdash; under most excesses'],
             ['Scuffed door or bumper', dl + ' – ' + dh, 'Usually not, once no-claims is counted'],
             ['Two or more panels', 'Needs looking at', 'Do the sum properly'],
             ['Anything structural or a door that will not shut', 'Needs looking at',
              'Probably yes'],
           ])),
          ]),
          ('Reporting it', [
           'Report it to the police for a crime reference number if you intend to claim, and '
           'because it helps if the driver is later identified. Note that the police will not '
           'normally pursue a damage-only car park incident with no witness, so treat the '
           'reference as paperwork rather than an investigation.',
           'Tell your insurer even if you decide not to claim. Most policies require notification '
           'of any incident, and failing to mention one can cause problems with an unrelated '
           'claim later.',
           ('note', ADVICE_NOTE),
          ]),
         ],
         [('How long does car park CCTV last?',
           'It varies by operator and is often weeks rather than months. That is why the request '
           'goes in the same day rather than after you have thought about it.'),
          ('Can I get the footage myself?',
           'You can ask, and operators vary. If they will not release it to you they will often '
           'release it to the police or to an insurer, so a crime reference helps.'),
          ('The supermarket says it is not their responsibility.',
           'Generally correct &mdash; they are not liable for what another customer does in their '
           'car park. The reason to ask them is the footage, not a claim against them.'),
          ('Is it worth claiming on my insurance?',
           'Below your excess, no. Above it, do the sum including the no-claims effect, because '
           'with no third party this counts as a fault claim. We will price it so you have a real '
           'number.'),
          ('There is paint from the other car on mine. Is that useful?',
           'Yes. It gives you their colour, and with the height and shape of the mark it narrows '
           'the vehicle. Photograph it before it is washed off.')],
         [('hit-and-run-untraced-driver-car-damage', 'Untraced drivers and the MIB'),
          ('door-repair-cost', 'Door repair cost'),
          ('light-scratch-repair', 'Light scratch repair'),
          ('is-it-worth-claiming-on-insurance', 'Claim or pay yourself?')],
         key_points=[
          '<strong>Ask for CCTV the same day</strong> &mdash; retention is often weeks.',
          'Photograph the <strong>paint transfer</strong> before anything is cleaned.',
          'Untraced with no injury means <strong>no national scheme for your car</strong>.',
          'With no third party, a claim is a <strong>fault claim</strong>.',
         ],
         hub=HUB_PROCESS, category='scenario', service_type='Vehicle body repair', note=None),

    page('vandalism-keyed-car-repair',
         'Keyed or Vandalised Car: Repair or Claim? | KITH Cars',
         'Why a keyed panel usually needs painting rather than polishing, the crime reference your '
         'insurer will want, and the no-claims trap on vandalism claims.',
         'Keyed, Scratched or Vandalised',
         'Bodywork &middot; Vandalism',
         'Two things surprise people. A key scratch almost never polishes out, and a vandalism '
         'claim normally costs you your no-claims even though you did nothing wrong.',
         [
          ('Why it will not polish out', [
           'Paint is layered: primer, then colour, then lacquer on top. Polishing works by taking '
           'a very small amount off the lacquer, so it can remove something sitting <em>in</em> '
           'the lacquer and cannot touch anything deeper.',
           ('table', (['Depth', 'Test', 'Repair'], [
             ['In the lacquer only', 'Your fingernail does not catch',
              'Machine polish, sometimes'],
             ['Through to the colour', 'Fingernail catches, no colour change in the line',
              'Paint repair'],
             ['Through to primer', 'The line looks pale or grey', 'Paint repair'],
             ['Through to metal', 'The line looks silver or brown',
              'Paint repair, and soon &mdash; this is where rust starts'],
           ])),
           'A deliberate key scratch is almost always at least the third row, because it is done '
           'with weight behind it. Anyone promising to buff out a keyed panel is either going to '
           'fail or going to thin your lacquer trying.',
          ]),
          ('The claim sum, including the part people miss', [
           'Vandalism is covered by comprehensive insurance. The catch is that there is no third '
           'party to recover from, so the claim is recorded as a fault claim and your no-claims '
           'discount is affected, exactly as if you had caused it.',
           ('steps', [
             '<strong>Get a crime reference number.</strong> <span>Report it to the police. Most '
             'insurers require it for a vandalism claim and will ask for it.</span>',
             '<strong>Get the repair priced.</strong> <span>One keyed panel is often close to a '
             'typical excess. Two or three panels is not.</span>',
             '<strong>Find out what claiming costs you.</strong> <span>Ask your insurer what '
             'happens to your discount and what the renewal effect is. Get it in writing.</span>',
             '<strong>Then decide.</strong> <span>Single panel, usually pay. Several panels or '
             'slashed tyres and broken glass alongside, usually claim.</span>',
           ]),
          ]),
          ('Act faster if it is through to metal', [
           'A scratch that has reached bare metal is an open invitation to corrosion, and once '
           'rust is established under the paint around the line it spreads outward and the repair '
           'gets bigger.',
           'Days and weeks are fine. Leaving it over a winter is how a one-panel job becomes a '
           'two-panel job with rust treatment in the middle.',
           ('note', 'If you are not repairing it immediately and it is down to metal, at minimum '
            'keep it clean and dry and get some protection on the line. It buys you time, it is '
            'not a repair.'),
          ]),
          ('Evidence, in case it matters later', [
           ['Photograph the whole car, not just the worst panel &mdash; vandalism is often '
            'multiple panels and people claim for one and find another later',
            'Note where it was parked and the window of time',
            'Ask neighbours and nearby businesses about cameras, and ask quickly',
            'Keep the crime reference number with the photographs and the estimate'],
           'If the same car is targeted repeatedly, that pattern is worth reporting as a pattern '
           'rather than as separate incidents.',
           ('note', ADVICE_NOTE),
          ]),
         ],
         [('Can a keyed scratch be polished out?',
           'Only if your fingernail does not catch in it. A deliberate key scratch almost always '
           'goes deeper than the lacquer, which means paint rather than polish.'),
          ('Will claiming for vandalism affect my no-claims?',
           'Usually yes, because there is no third party for your insurer to recover from, so it '
           'is recorded as a fault claim. It is the thing people find unfair and it is how it '
           'works.'),
          ('Do I need a police report?',
           'Most insurers require a crime reference number for vandalism. Get one even if you end '
           'up paying yourself.'),
          ('They keyed three panels. Is that one repair?',
           'It is one job but three panels of paint, and the price reflects that. It is also the '
           'situation where claiming usually does make sense.'),
          ('How soon do I need to do something?',
           'If the line shows bare metal, sooner. Corrosion starting along the scratch turns a '
           'paint job into a paint job plus rust treatment.')],
         [('light-scratch-repair', 'Light scratch repair'),
          ('car-park-damage-no-note-left', 'Car park damage'),
          ('is-it-worth-claiming-on-insurance', 'Claim or pay yourself?'),
          ('car-paint-code-colour-match', 'Paint codes and matching')],
         key_points=[
          'If your <strong>fingernail catches</strong>, it needs paint, not polish.',
          'Vandalism claims are normally recorded as <strong>fault claims</strong>.',
          'Insurers usually require a <strong>crime reference number</strong>.',
          '<strong>Bare metal</strong> showing means do not leave it over a winter.',
         ],
         hub=HUB_PROCESS, category='scenario', service_type='Vehicle paint repair', note=None),

    page('storm-flood-tree-damage-car',
         'Storm, Flood and Falling Tree Damage to a Car | KITH Cars',
         'What comprehensive insurance covers in bad weather, the one thing that can void a flood '
         'claim, and why flood-damaged cars get written off.',
         'Weather Damage',
         'Bodywork &middot; Storm and flood',
         'Comprehensive policies generally cover storm, flood and falling objects. The exception '
         'that catches people is driving into water you could see.',
         [
          ('What is normally covered', [
           ('table', (['Event', 'Usually'], [
             ['Tree or branch down on the car', 'Covered under comprehensive'],
             ['Fence panel, tile or debris blown into it', 'Covered'],
             ['Hail denting panels', 'Covered'],
             ['Flood water rising around a parked car', 'Covered'],
             ['Driving into standing water despite warnings',
              '<strong>Often refused</strong> &mdash; see below'],
           ])),
           'Third party only or third party fire and theft does not cover any of the first four. '
           'Weather damage to your own car is a comprehensive-only benefit, which is worth knowing '
           'before the storm rather than after.',
          ]),
          ('The thing that voids a flood claim', [
           'Driving through flood water that you could see, particularly past a road closure or a '
           'warning sign, is the one weather scenario insurers regularly decline. The argument is '
           'that the damage was not an accident but the predictable result of a choice.',
           'Water drawn into an engine hydrolocks it, and that is frequently terminal rather than '
           'expensive. If water is deeper than you can confidently judge, the car is worth less '
           'than the detour.',
           ('note', 'If you have already driven into deep water and the engine stopped, do not '
            'try to restart it. Attempting to restart a hydrolocked engine is what turns a '
            'recoverable situation into a replacement engine.'),
          ]),
          ('Why flooded cars get written off', [
           'Standing water in a modern car reaches places that cannot be dried or replaced '
           'economically:',
           ['Control modules and wiring looms, which are routed low and through the floor',
            'Seat frames, belt mechanisms and airbag components, which are safety items',
            'Carpet underlay and sound deadening, which hold water and smell indefinitely',
            'Cavities inside sills and floor sections, which corrode from the inside out'],
           'Which is why a car that looks fine after a flood is routinely categorised as a '
           'write-off. The visible interior is the cheap part. Also worth knowing: salt water is '
           'considerably worse than fresh, and the depth the water reached matters more than how '
           'long it was there.',
          ]),
          ('If a tree came down on it', [
           ('steps', [
             '<strong>Photograph before anything is moved.</strong> <span>Including the tree, '
             'where it stood, and what it fell from.</span>',
             '<strong>Find out who owned the tree.</strong> <span>Council, a neighbour, a '
             'landowner. It matters for the next step.</span>',
             '<strong>Ask whether it was known to be dangerous.</strong> <span>A healthy tree in '
             'a storm is nobody&rsquo;s fault. A tree somebody had already been told about is a '
             'different conversation, and a potential claim against them rather than your own '
             'policy.</span>',
             '<strong>Claim on comprehensive meanwhile.</strong> <span>Do not wait on the '
             'liability question to get the car moving.</span>',
           ]),
           ('note', ADVICE_NOTE),
          ]),
          ('Hail', [
           'Hail puts a large number of small dents across horizontal panels &mdash; roof, bonnet, '
           'boot lid &mdash; with the paint usually unbroken. It is a volume job rather than a '
           'difficult one, and the price follows the number of dents and the panels affected.',
           'Every dent we repair is straightened and then painted. We do not offer paintless dent '
           'removal, so on a widely hail-dented car the honest answer is that it is a panel-by-'
           'panel repair, and we will tell you what that comes to before you commit to anything.',
          ]),
         ],
         [('Is storm damage covered by my insurance?',
           'By comprehensive, normally yes. By third party fire and theft, no &mdash; that covers '
           'damage you cause to others, plus fire and theft of your own car.'),
          ('Will claiming for storm damage affect my no-claims?',
           'Often yes, because there is no third party to recover from. Ask your insurer before '
           'you commit, and do the sum against the repair cost.'),
          ('My car was in a flood but starts fine.',
           'Starting fine is not the test. Get the floor, the loom routing and the modules looked '
           'at, because flood problems appear over months rather than immediately.'),
          ('Can I claim against the council for a fallen tree?',
           'Potentially, if the tree was known to be dangerous and nothing was done. A healthy '
           'tree in a severe storm generally is not anyone&rsquo;s liability. Claim on your own '
           'policy to get moving either way.'),
          ('How much does hail damage cost to repair?',
           'It depends entirely on how many dents and across how many panels. Bring it in and we '
           'will count them and give you a figure rather than a guess.')],
         [('car-write-off-categories-explained', 'Write-off categories'),
          ('car-dent-repair', 'Dent repair'),
          ('is-it-worth-claiming-on-insurance', 'Claim or pay yourself?'),
          ('vehicle-recovery', 'Recovery')],
         key_points=[
          'Weather damage is a <strong>comprehensive-only</strong> benefit.',
          '<strong>Driving into visible flood water</strong> is the claim insurers decline.',
          'Never <strong>restart a hydrolocked engine</strong>.',
          'Flooded cars are written off for the <strong>wiring and corrosion</strong>, not the '
          'carpets.',
         ],
         hub=HUB_PROCESS, category='scenario', service_type='Vehicle body repair', note=None),
]

# The decision page the three pages above all want to point at. It is the most-asked question in
# bodywork and the answer is arithmetic, so the page does the arithmetic rather than hedging.
PAGES.append(
    page('is-it-worth-claiming-on-insurance',
         'Is It Worth Claiming on Insurance for Car Damage? | KITH Cars',
         'The four numbers that decide it, worked through with real repair prices, and the two '
         'situations where you should claim regardless of the sum.',
         'Claim, or Pay for It Yourself?',
         'Bodywork &middot; Claim decisions',
         'It is arithmetic, and most people only count one of the four numbers. The excess is the '
         'obvious one. The lost no-claims discount is usually the bigger one.',
         [
          ('The four numbers', [
           ('table', (['', 'Where to get it'], [
             ['1. The repair cost', 'A real estimate &mdash; the box below, or bring the car in'],
             ['2. Your excess',
              'Your policy schedule. Add compulsory and voluntary together, because both apply'],
             ['3. What losing your no-claims costs',
              'Ask your insurer what your renewal becomes with the claim on it'],
             ['4. Five years of slightly higher premiums',
              'Claims are declarable for five years, not one'],
           ])),
           'Numbers three and four are the ones people skip, and together they are frequently '
           'larger than the excess. An insurer will tell you number three if you ask directly '
           'enough: &ldquo;what would my renewal be with this claim on it?&rdquo;',
          ]),
          ('Fault and non-fault change everything', [
           'If there is an identified third party at fault, your insurer recovers its money from '
           'theirs, your no-claims is restored and your excess usually comes back. Numbers three '
           'and four largely drop out, and claiming is normally the right answer.',
           'If there is nobody to recover from &mdash; vandalism, a hit and run, weather, your own '
           'mistake, a car park shunt where the driver was never found &mdash; it is recorded as a '
           'fault claim, your discount takes the hit, and all four numbers count.',
           ('table', (['Situation', 'Recovered from a third party?', 'Usually'], [
             ['Non-fault, other driver identified and insured', 'Yes', 'Claim'],
             ['Uninsured driver, identified', 'Pursued, often successfully', 'Claim'],
             ['Hit and run, never identified', 'No', 'Do the sum'],
             ['Vandalism', 'No', 'Do the sum'],
             ['Storm, flood, falling tree', 'No', 'Do the sum'],
             ['Your own mistake', 'No', 'Do the sum'],
           ])),
          ]),
          ('Worked through', [
           'Say a scuffed door and wing, your excess is £350, and your insurer tells you the '
           'claim puts about £180 a year on your renewal.',
           ('steps', [
             '<strong>Repair cost, priced properly.</strong> <span>Not a guess. A real figure for '
             'the actual damage.</span>',
             '<strong>Add the excess to what claiming costs over time.</strong> <span>£350 plus '
             'roughly £180 a year while the claim is declarable. That is well over £1,000 of real '
             'cost before the insurer pays anything.</span>',
             '<strong>Compare.</strong> <span>If the repair comes in under that, paying is '
             'cheaper and your record stays clean.</span>',
             '<strong>Remember the excess is not a discount.</strong> <span>Claiming on a £500 '
             'repair with a £350 excess buys you £150 of help and costs you years of '
             'discount.</span>',
           ]),
           'That last point is where most of the bad decisions live. People claim on jobs barely '
           'above their excess because the claim feels free.',
          ]),
          ('Claim regardless of the sum when', [
           ['<strong>Anyone was injured, however slightly.</strong> Injury claims have long tails '
            'and you do not want to have handled it privately.',
            '<strong>There is any question about structure or safety.</strong> A door that will '
            'not shut properly, a suspicious panel gap, anything that was a real impact rather '
            'than a scrape.',
            '<strong>A third party is involved at all.</strong> Even if you intend to pay, tell '
            'your insurer. Settling privately and then having the other party claim anyway is a '
            'genuinely bad position.',
            '<strong>The repair is a large fraction of the car&rsquo;s value.</strong> That is '
            'what insurance is for.'],
          ]),
          ('Tell your insurer either way', [
           'Almost every policy requires you to notify an incident whether or not you claim. '
           'Notifying is not claiming, and saying so explicitly on the call &mdash; '
           '&ldquo;notification only, I am not claiming&rdquo; &mdash; is worth doing.',
           'Not mentioning an incident is how people find an unrelated claim refused later for '
           'non-disclosure. The notification costs you nothing; the omission can cost you a lot.',
           ('note', CHOICE_NOTE),
          ]),
         ],
         [('Does my excess get refunded on a non-fault claim?',
           'Usually, once your insurer recovers from the other side. Ask how long that takes, '
           'because it can be months.'),
          ('Will one claim really raise my premium for five years?',
           'Claims are normally declarable for five years and most insurers ask about three. The '
           'effect fades but it is not one renewal.'),
          ('What if I claim and then withdraw?',
           'A notified-and-withdrawn incident can still appear on your record. Ask before you '
           'start the claim rather than after.'),
          ('Is protected no-claims the answer?',
           'It protects the discount, not the premium &mdash; your underlying rate can still rise. '
           'It helps, and it is not a free pass.'),
          ('Can you tell me which is cheaper?',
           'We can give you the repair figure, which is the number you are missing. The other '
           'three come from your insurer, and asking them directly is the only way to get them '
           'right.')],
         [('hit-and-run-untraced-driver-car-damage', 'Hit and run'),
          ('vandalism-keyed-car-repair', 'Vandalism and keying'),
          ('will-a-non-fault-claim-affect-my-no-claims', 'Non-fault and no-claims'),
          ('compulsory-vs-voluntary-excess', 'How excess works')],
         key_points=[
          'Four numbers, not one: <strong>repair, excess, lost discount, five years of '
          'premiums</strong>.',
          '<strong>Non-fault with a traced third party</strong> &mdash; claim.',
          'Nobody to recover from &mdash; it is a <strong>fault claim</strong>, so do the sum.',
          '<strong>Notify either way.</strong> Notifying is not claiming.',
         ],
         hub=HUB_PROCESS, category='scenario', service_type='Vehicle body repair', note=None)
)
