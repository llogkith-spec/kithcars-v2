#!/usr/bin/env python3
"""Damage, money and handing a car back.

The lease page is built on the BVRLA Fair Wear and Tear standard, which is the document inspectors
actually work to and which states its thresholds in millimetres. That makes it the rare bodywork
topic with exact answers: 25mm of scratch, 10mm of dent, two per panel, 50mm of alloy scuffing.
Anyone facing a handback wants those numbers and almost nobody publishes them plainly.

The alloy page deliberately does not state how many times a diamond-cut wheel can be re-cut or
why the lacquer fails, because the sources checked did not say and inventing a number on a page
that people will plan around would be worse than leaving it out.
"""
import json
import pathlib

from bw_lib import page, HUB_PROCESS, ADVICE_NOTE, CHOICE_NOTE

PRICES = json.loads((pathlib.Path(__file__).resolve().parent / 'bodyprices.json').read_text())
A = PRICES['_alloy_per_wheel_inc_vat']


def m(panel, dmg='dent', band='medium'):
    p = PRICES[f'{panel}|{dmg}|{band}']
    return f'&pound;{p["low"]}', f'&pound;{p["high"]}'


sl, sh = m('door', 'smart')
dl, dh = m('door')
bl, bh = m('front-bumper', 'scuff')

BVRLA = ('<a href="https://www.bvrla.co.uk" target="_blank" rel="noopener">BVRLA</a> Fair Wear '
         'and Tear standard')

PAGES = [

    page('lease-return-damage-charges',
         'Lease Return Damage Charges: What Is Actually Chargeable | KITH Cars',
         'The exact BVRLA fair wear and tear thresholds in millimetres, what gets charged at '
         'handback, and the sum that decides whether to repair first.',
         'What Gets Charged When You Hand a Lease Car Back',
         'Bodywork &middot; Lease and company cars',
         'There are actual numbers for this, and they are smaller than most people assume. A '
         'scratch is fine up to 25mm. A dent is fine up to 10mm, and only two per panel. Over '
         'those, you pay.',
         [
          ('The thresholds, in millimetres', [
           'Inspectors work to the ' + BVRLA + ', and it is specific. These are its limits.',
           ('table', (['Damage', 'Acceptable', 'Chargeable'], [
             ['Scratches', 'Up to 25mm, with no primer or bare metal showing',
              'Over 25mm, or anything through to primer or metal'],
             ['Dents', 'Up to 10mm, maximum two per panel, paint unbroken',
              'Over 10mm, more than two per panel, or paint broken'],
             ['Dents on the roof or a swage line', 'None', 'Any'],
             ['Alloy wheels', 'Scuffs totalling up to 50mm around the circumference',
              'Over 50mm, dents or holes in the rim, any damage to spokes or hub'],
             ['Chips', 'Small chips, including door edge chipping',
              'Anything needing the whole panel or bumper repainted'],
             ['Rust or corrosion', 'None', 'Any, on any painted area'],
             ['Previous repairs', 'Good ones',
              'Flaking paint, rippled finish or mismatched colour'],
           ])),
           'Two of those catch people out more than the rest. <strong>A swage line</strong> is the '
           'styling crease that runs along the flank of most cars &mdash; a dent on it is '
           'chargeable at any size, because it is the hardest place on the car to repair '
           'invisibly. And <strong>any</strong> rust is chargeable, however small.',
          ]),
          ('The sum worth doing', [
           'Handback charges are set by the leasing company and are frequently more than having '
           'the same damage repaired beforehand, because they are pricing a main-dealer repair '
           'plus their own administration.',
           ('steps', [
             '<strong>Inspect it yourself, early.</strong> <span>Eight to ten weeks before '
             'handback, in daylight, with a tape measure. Not the week before.</span>',
             '<strong>Measure, do not estimate.</strong> <span>The difference between 22mm and '
             '28mm of scratch is the difference between nothing and a charge.</span>',
             '<strong>List what is over.</strong> <span>Only the items past the thresholds '
             'matter. Everything under is free.</span>',
             '<strong>Get those priced.</strong> <span>Put the registration into the box below, '
             'or bring it in. Then you have a real figure.</span>',
             '<strong>Compare against the estimated charges.</strong> <span>Most leasing '
             'companies publish an indicative charge list. Ask for it.</span>',
           ]),
          ]),
          ('Where repairing first usually wins', [
           ['<strong>Kerbed alloys.</strong> The commonest handback charge there is, and '
            f'refurbishment runs &pound;{A["low"]} to &pound;{A["high"]} per wheel including VAT '
            f'&mdash; normally well under what is charged.',
            f'<strong>A single scuffed bumper.</strong> {bl} to {bh} with us, and bumpers are the '
            'most-charged panel because they are the most scuffed.',
            '<strong>Several small scratches on one panel.</strong> Individually fine, but a '
            'panel needing a repaint is chargeable, and the charge is for the panel either way.',
            '<strong>Anything with rust starting.</strong> Chargeable at any size, and it gets '
            'worse while you wait.'],
          ]),
          ('Where it does not', [
           'Be even-handed about this: do not repair damage that is already within the standard. '
           'A 15mm scratch with no primer showing costs you nothing at handback, and repairing it '
           'is money spent for no reason.',
           'And a poor repair is explicitly chargeable &mdash; flaking, rippled or mismatched '
           'paint is on the not-acceptable list. A cheap job done badly before handback can cost '
           'you more than the original damage would have.',
           ('note', CHOICE_NOTE),
          ]),
          ('Company cars and fleets', [
           'The same standard is normally used, but who pays varies with your employer&rsquo;s '
           'policy. Some pass handback charges to the driver, some absorb them, and many have a '
           'threshold.',
           'Worth asking before you decide anything, because if your employer absorbs it there is '
           'no reason to repair anything at your own expense.',
           ('note', ADVICE_NOTE),
          ]),
         ],
         [('How long before handback should I check?',
           'Eight to ten weeks. That leaves time to get work done without paying a premium for '
           'speed, and time to challenge the inspection if you disagree with it.'),
          ('Can I challenge the charges?',
           'Yes. Ask for the inspection report with photographs and measurements, and check them '
           'against the standard. Charges for damage within the thresholds should be withdrawn, '
           'and inspectors do make mistakes.'),
          ('Will they notice a repair?',
           'A good one, no. A bad one, immediately &mdash; and a poor repair is itself chargeable. '
           'That is the argument for having it done properly rather than cheaply.'),
          ('What about a chipped windscreen?',
           'Usually assessed separately against glass criteria rather than the paint ones, and '
           'often covered by your insurance with a low or nil excess for a repair. Worth checking '
           'before you pay for it.'),
          ('Do I need to fix every chip?',
           'No. Small chips including door edge chipping are explicitly acceptable. Only chips '
           'that would need a whole panel repainted are chargeable.')],
         [('kerbed-alloy-wheel-repair', 'Kerbed alloy repair'),
          ('is-it-worth-repairing-before-selling', 'Repair before selling?'),
          ('light-scratch-repair', 'Light scratch repair'),
          ('car-dent-repair', 'Dent repair')],
         key_points=[
          'Scratches: <strong>25mm</strong>, with no primer showing.',
          'Dents: <strong>10mm, two per panel</strong>, paint unbroken.',
          'Alloys: <strong>50mm</strong> of scuffing around the circumference.',
          '<strong>Any</strong> rust is chargeable, and so is a <strong>bad repair</strong>.',
         ],
         hub=HUB_PROCESS, category='value', service_type='Vehicle body repair', note=None),

    page('kerbed-alloy-wheel-repair',
         'Kerbed Alloy Wheel Repair Cost | KITH Cars',
         'What alloy refurbishment costs per wheel, repair against replacement, the finishes that '
         'behave differently, and the 50mm threshold that matters on a lease car.',
         'Kerbed Alloy Wheel Repair',
         'Bodywork &middot; Wheels',
         f'&pound;{A["low"]} to &pound;{A["high"]} per wheel including VAT, depending on how far '
         f'into the face the damage goes and what finish the wheel has.',
         [
          ('What it costs and what moves it', [
           ('table', (['', 'Per wheel, inc VAT'], [
             ['Standard painted or powder-coated finish',
              f'&pound;{A["low"]} &ndash; &pound;{A["high"]}'],
             ['Gouged into the face rather than scuffed', 'Toward the upper figure'],
             ['Diamond-cut finish', 'Quoted separately &mdash; see below'],
             ['Buckled or cracked rim', 'Not a refurbishment job'],
           ])),
           'The two things that move the price are how deep the damage goes and what the wheel is '
           'finished in. A scuff through the lacquer is quick. A gouge that has taken metal out '
           'has to be filled and reprofiled before anything else happens.',
          ]),
          ('Refurbish or replace', [
           'Refurbishment nearly always wins on a kerbed wheel, and for a reason that is not '
           'obvious: a refurbished wheel can be finished to match the other three, and a new one '
           'cannot be made to look older.',
           'If you replace one wheel on a four-year-old car, you now have three weathered wheels '
           'and one bright one, and on a set that cannot be matched the usual settlement approach '
           'is the damaged wheel plus about half the cost of doing the rest. Refurbishing sides '
           'the problem completely.',
           'Replacement is the answer where the wheel is structurally damaged &mdash; buckled, '
           'cracked, or with a chunk missing from the rim flange. Those are safety items and we '
           'will say so rather than cosmetically tidying them.',
          ]),
          ('Diamond-cut wheels are different', [
           'A diamond-cut wheel has been turned on a lathe so the metal face is exposed and '
           'polished, then lacquered. You can see the fine machined grain lines in the face if '
           'you look closely.',
           'They are repaired differently &mdash; the face has to be re-cut on a lathe rather '
           'than simply filled and painted &mdash; and that is specialist equipment rather than '
           'something every bodyshop has.',
           'We quote diamond-cut separately rather than giving a band here, and if a wheel has '
           'reached the point where re-cutting is not the right answer we will tell you and talk '
           'through painting it instead. What we will not do is give you a number on a web page '
           'for a job that varies this much.',
          ]),
          ('The 50mm rule, if the car is leased', [
           'The ' + BVRLA + ' allows scuffs totalling up to 50mm around the circumference of an '
           'alloy. Over that is chargeable, and so is any dent or hole in the rim, or any damage '
           'to the spokes or the hub.',
           'Kerbed alloys are the single commonest end-of-lease charge, and refurbishment at '
           f'&pound;{A["low"]} to &pound;{A["high"]} a wheel is normally well under what gets '
           f'charged. If you have a handback coming, measure the scuffing before you decide.',
          ]),
          ('While the wheel is off', [
           'A kerb strike hard enough to mark an alloy is usually hard enough to be worth '
           'checking the rest of that corner. Tyre sidewall damage, tracking knocked out, and in '
           'a heavy strike a bent suspension component.',
           'We look at the tyre and the geometry on anything that has been kerbed properly rather '
           'than just making the wheel look right. A refurbished alloy on a car that now pulls to '
           'one side is half a job.',
          ]),
         ],
         [('Can you do it while I wait?',
           'Not usually &mdash; the finish needs to cure properly. Most wheels are a day or two, '
           'and we can often do them in pairs so the car stays usable.'),
          ('Will it match my other wheels?',
           'That is the main argument for refurbishing rather than replacing. We finish to match '
           'what is on the car now, not to what the wheel looked like new.'),
          ('My wheel is buckled, not scuffed.',
           'That is a different job and not a cosmetic one. A buckled rim can hold air and still '
           'be unsafe. Bring it in and we will tell you honestly whether it is repairable or '
           'needs replacing.'),
          ('Is it worth claiming on insurance?',
           'Rarely for one wheel &mdash; it is well under most excesses. For all four, after '
           'vandalism or a serious kerb strike, it starts to be worth the sum.'),
          ('Do you do them mobile?',
           'No. Wheels are done here, where there is a booth and a proper cure. A finish applied '
           'on a driveway in wind is the one that peels at the lip within a year.')],
         [('lease-return-damage-charges', 'Lease return charges'),
          ('kerb-damage-repair', 'Kerb damage repair'),
          ('mismatched-parts-after-a-repair', 'Mismatched parts'),
          ('trim-repair-cost', 'Trim and mirror repair')],
         key_points=[
          f'<strong>&pound;{A["low"]} to &pound;{A["high"]} per wheel</strong> inc VAT on a '
          f'standard finish.',
          '<strong>Refurbish beats replace</strong> &mdash; a new wheel cannot be made to look '
          'older.',
          '<strong>Diamond-cut is quoted separately</strong>; it needs a lathe, not filler.',
          'Leased? The threshold is <strong>50mm of scuffing</strong> before it is chargeable.',
         ],
         hub=HUB_PROCESS, category='value', service_type='Alloy wheel refurbishment', note=None),

    page('is-it-worth-repairing-before-selling',
         'Is It Worth Repairing Bodywork Before Selling a Car? | KITH Cars',
         'When cosmetic repair returns more than it costs at sale, when it does not, and the '
         'three kinds of damage that cost you more than the repair would.',
         'Repair It, or Sell It As It Is?',
         'Bodywork &middot; Selling',
         'It depends on who is buying. A trade buyer prices damage at what it costs them to fix '
         'and deducts it either way. A private buyer prices it at what they imagine it costs, '
         'and that number is nearly always higher.',
         [
          ('Trade against private', [
           ('table', (['', 'Trade or part-exchange', 'Private sale'], [
             ['How damage is priced', 'At their cost to repair', 'At what the buyer guesses'],
             ['Typical guess', 'Accurate', 'Two to three times the real figure'],
             ['Effect of repairing first', 'Small &mdash; you both pay the same cost',
              'Larger &mdash; you remove the guess'],
             ['What they really want', 'The margin', 'To not inherit a problem'],
           ])),
           'That is the whole thing in one table. Against a dealer, repairing first mostly moves '
           'money from one pocket to another. Against a private buyer, it removes the thing they '
           'are mentally charging you three times over for.',
          ]),
          ('The three worth doing every time', [
           ['<strong>Anything that suggests a crash.</strong> A misaligned panel gap, a slightly '
            'different shade on one wing, a bumper sitting proud. Buyers do not think "scuff", '
            'they think "what else is wrong with it", and that discount is open-ended.',
            '<strong>Rust, however small.</strong> It is the one kind of damage that gets visibly '
            'worse while the car sits on a forecourt, and it is the thing buyers inspect for.',
            '<strong>Kerbed alloys, all round.</strong> Disproportionately visible, cheap to put '
            f'right at &pound;{A["low"]} to &pound;{A["high"]} a wheel, and the first thing anyone '
            f'notices walking up to a car.'],
          ]),
          ('The ones to leave', [
           'A single small scratch or stone chips on a car of some age. They read as normal use, '
           'and a car with no marks at all on a ten-year-old body sometimes raises more questions '
           'than it answers.',
           'And anything where the repair costs more than the damage is taking off the price. '
           'That is a sum you can only do with a real figure, which is what the box below is for.',
          ]),
          ('Get the order right', [
           ('steps', [
             '<strong>Price the car both ways first.</strong> <span>Look at advertised prices for '
             'the same model in good condition and in marked condition.</span>',
             '<strong>Get the repair priced.</strong> <span>A real figure, not a guess.</span>',
             '<strong>Repair only where the gap is bigger than the cost.</strong> '
             '<span>Including the three above, where the gap is usually invisible but '
             'real.</span>',
             '<strong>Photograph it properly afterwards.</strong> <span>In daylight, clean, from '
             'the angles that show the panels. Half the value of repairing is in the '
             'advert.</span>',
           ]),
          ]),
          ('If the car has a recorded write-off', [
           'Different question, and the answer changes. A Category S or N is recorded permanently '
           'and the buyer will find it, so the discount is coming regardless of how the car looks.',
           'What helps there is documentation rather than cosmetics: the repair invoice, the '
           'itemised estimate, photographs of the work. The biggest discount buyers apply to a '
           'recorded car is for the unknown, and a full file removes most of it.',
           ('note', ADVICE_NOTE),
          ]),
         ],
         [('How much does a scuffed bumper take off the price?',
           'Privately, usually far more than the repair costs, because the buyer is guessing. '
           f'A bumper scuff is {bl} to {bh} with us; the mental deduction is often several times '
           f'that.'),
          ('Should I tell a buyer about a repair I had done?',
           'If asked, yes, and having the invoice helps rather than hurts. A documented repair '
           'reads better than an undocumented one that a paint gauge finds anyway.'),
          ('Is it worth a full respray before selling?',
           'Almost never. The cost rarely comes back, and a freshly resprayed older car makes '
           'buyers wonder what was underneath.'),
          ('What about a lease car I am handing back?',
           'Different rules entirely &mdash; there are published thresholds in millimetres and '
           'anything under them is free. See the lease return page.'),
          ('Can you tell me what is worth doing?',
           'Bring it in and we will walk round it with you and say which marks a buyer will '
           'notice and which they will not. We would rather do two panels that matter than five '
           'that do not.')],
         [('lease-return-damage-charges', 'Lease return charges'),
          ('kerbed-alloy-wheel-repair', 'Kerbed alloy repair'),
          ('selling-a-cat-s-or-cat-n-car', 'Selling a recorded write-off'),
          ('how-to-tell-if-a-car-has-been-resprayed', 'Spotting a previous respray')],
         key_points=[
          'Trade buyers price damage <strong>accurately</strong>. Private buyers price it '
          '<strong>two to three times too high</strong>.',
          'Always fix: anything that <strong>suggests a crash</strong>, any <strong>rust</strong>, '
          'and <strong>kerbed alloys</strong>.',
          'Leave: a single scratch or stone chips on an older car.',
          'Recorded write-off? <strong>Documentation beats cosmetics.</strong>',
         ],
         hub=HUB_PROCESS, category='value', service_type='Vehicle body repair', note=None),
]
