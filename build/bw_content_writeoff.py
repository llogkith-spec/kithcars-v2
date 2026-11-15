#!/usr/bin/env python3
"""Insurance cluster: write-offs.

Categories are the post-October-2017 set - A, B, S, N. The older C and D appear only where a page
explains what they used to mean, because cars carrying those markers are still being sold.

A and B share a page rather than having one each. They are both "the car does not go back on the
road" and differ only in whether parts may be salvaged, so two pages would have been the same page
twice - which is exactly the failure this content set is built to avoid.
"""

from bw_lib import page, ADVICE_NOTE

PAGES = [

    page('car-write-off-categories-explained',
         'Car Write-Off Categories Explained: A, B, S and N | KITH Cars',
         'What each write-off category means, which ones can go back on the road, what happens '
         'to the V5C, and what it does to the value. The current A/B/S/N set and the old C/D.',
         'Write-Off Categories Explained',
         'Insurance &amp; claims &middot; Write-offs',
         'Four categories, and the only thing that matters first is which side of the line yours '
         'falls on. Two mean the car is finished. Two mean it is repairable and the decision is '
         'yours.',
         [
          ('All four, in one table', [
           ('table', (['Category', 'Structural damage', 'Back on the road?', 'What happens'], [
             ['A', 'Irrelevant', 'Never', 'Entire vehicle crushed, parts included'],
             ['B', 'Severe', 'Never', 'Body shell crushed; serviceable parts may be reused'],
             ['S', 'Yes', 'Yes, if repaired', 'Structurally damaged but repairable'],
             ['N', 'No', 'Yes, if repaired', 'Non-structural damage; repairable'],
           ])),
           'A and B are disposal decisions and there is nothing to discuss. S and N are financial '
           'decisions, and that is where people have options they do not realise they have.',
          ]),
          ('The thing nobody explains', [
           'A write-off is not a safety verdict. It is arithmetic. The insurer compares what the '
           'repair costs against what the car is worth, less what the salvage is worth, and '
           'writes it off when repairing costs more than paying you out.',
           'That is why a ten-year-old car with a damaged wing and door can be written off while '
           'identical damage on a three-year-old car is simply repaired. The damage is the same. '
           'The value either side of it is not.',
          ]),
          ('S and N, the difference that matters', [
           '<strong>S is structural.</strong> The chassis, crumple zones, suspension mounting '
           'points or something else that carries load has been damaged. It can be repaired '
           'properly, but it has to be done properly, and the DVLA must be notified &mdash; the '
           'car is issued a new V5C.',
           '<strong>N is non-structural.</strong> Panels, lights, electrics, cosmetics. The '
           'shell is sound. There is no DVLA notification and you keep the same V5C, though the '
           'category is still recorded against the vehicle.',
           'Both show on a history check for ever, and both knock money off what the car will '
           'later sell for.',
          ]),
          ('The old C and D', [
           'Before October 2017 the repairable categories were C and D, split on cost rather '
           'than on structure. Plenty of cars on the road still carry those markers and they '
           'have not been reclassified.',
           ('table', (['Old', 'Roughly equivalent to', 'Note'], [
             ['C', 'S', 'Repair cost exceeded value &mdash; said nothing about structure'],
             ['D', 'N', 'Cheaper damage, written off on economics alone'],
           ])),
           'If you are buying a car marked C or D, the marker tells you less than S or N would. '
           'Get it inspected rather than assuming.',
          ]),
          ('What to do if yours has been written off', [
           ('steps', [
             '<strong>Ask which category, in writing.</strong> <span>It changes everything that '
             'follows.</span>',
             '<strong>Do not accept the settlement yet.</strong> <span>Once the car goes to '
             'salvage it is gone, and so is the option to keep it.</span>',
             '<strong>Check the valuation.</strong> <span>They owe you market value, not the '
             'cheapest figure in a guide.</span>',
             '<strong>Get a real repair quote.</strong> <span>Then you can compare keeping it '
             'against taking the money, with numbers rather than guesses.</span>',
           ]),
          ]),
         ],
         [('Can I refuse to let them write it off?',
           'You cannot force them to pay for a repair that costs more than the car is worth. You '
           'can ask to retain the salvage and repair it yourself, which is a different thing and '
           'usually possible.'),
          ('Does a write-off always mean a payout?',
           'On a comprehensive policy for a fault or non-fault accident, yes &mdash; the market '
           'value less any excess. Third-party-only cover does not pay for your own car.'),
          ('Will I be told the category straight away?',
           'Not always. It is set after the engineer assesses the car, so ask explicitly rather '
           'than waiting to be told.'),
          ('Is a Cat S car safe to buy?',
           'It can be, if it was repaired properly, and that is the whole question. Get an '
           'independent inspection. The category tells you what was damaged, not how well it was '
           'put right.')],
         [('category-n-write-off', 'Category N explained'),
          ('category-s-write-off', 'Category S explained'),
          ('category-a-and-b-write-offs', 'Categories A and B'),
          ('can-i-keep-my-written-off-car', 'Keeping a written-off car')],
         key_points=[
          '<strong>A and B never return to the road.</strong> S and N can.',
          'A write-off is <strong>arithmetic, not a safety verdict</strong>.',
          'S is <strong>structural</strong> and needs DVLA notification; N is not and does not.',
          'Say you want to <strong>keep the car before you accept the settlement</strong>.',
         ]),

    page('category-s-write-off',
         'Category S Write-Off Explained | Structural Damage | KITH Cars',
         'What Cat S means, how it differs from Cat N, the DVLA notification, buying one, and '
         'what a proper structural repair involves.',
         'Category S Write-Off: Structural Damage',
         'Insurance &amp; claims &middot; Write-offs',
         'S means something that carries load was damaged &mdash; chassis, crumple zone, '
         'suspension mounting. It is repairable. It is also the category where <em>how</em> it '
         'was repaired matters more than anything else.',
         [
          ('What counts as structural', [
           'Not the panels you can see. The structure is what holds the car together and what is '
           'designed to deform in a crash to protect you.',
           ['Chassis legs and the front or rear crash structure.',
            'Crumple zones designed to collapse in a controlled way.',
            'Suspension mounting points and subframe mounts.',
            'The A, B and C pillars, the sills and the floor pan.',
            'Anything welded into the shell that carries load.'],
           'A rear quarter panel is welded to the shell but is not, on its own, structural. A '
           'sill is. That distinction is what separates an S from an N.',
          ]),
          ('Why it matters more than N', [
           'Crumple zones only work once, and they only work as designed if they are rebuilt as '
           'designed. A structure that has been straightened without being measured, or welded '
           'with the wrong method, can look perfect and behave differently in the next impact.',
           'That is the real reason a Cat S carries more stigma and more value loss than a Cat N. '
           'It is not that the damage was worse in a general sense &mdash; it is that the part '
           'that protects you was involved.',
          ]),
          ('The DVLA step', [
           'Category S must be notified to the DVLA, and the vehicle is issued a new V5C. That is '
           'the practical difference in paperwork from a Cat N, which keeps its original V5C.',
           'Either way the category is recorded against the vehicle permanently and will appear '
           'on any history check, so neither is something that quietly goes away.',
          ]),
          ('What a proper structural repair involves', [
           ('steps', [
             '<strong>Measured, not eyeballed.</strong> <span>The shell is measured against '
             'manufacturer dimensions before and after, on a jig or with an electronic measuring '
             'system.</span>',
             '<strong>Pulled on a jig.</strong> <span>The structure is drawn back to the correct '
             'dimensions under controlled tension rather than forced.</span>',
             '<strong>Sections replaced where specified.</strong> <span>Some structural parts are '
             'designed to be cut at defined points and replaced, not straightened.</span>',
             '<strong>Welded to the right method.</strong> <span>Modern high-strength steels and '
             'aluminium need specific techniques. The wrong weld weakens the area around '
             'it.</span>',
             '<strong>Corrosion protection restored.</strong> <span>Cutting and welding destroys '
             'the factory coatings. They have to be rebuilt or the repair rusts from inside.</span>',
           ]),
          ]),
          ('Buying one', [
           'A properly repaired Cat S can be a sound car at a real discount. A badly repaired one '
           'is a car you do not want at any price, and you cannot tell which is which from the '
           'advert.',
           'Pay for an independent inspection, specifically of the structure rather than a '
           'general once-over. Ask for the repair invoices. Look at panel gaps on both sides and '
           'at whether the car tracks straight. If the seller cannot say who repaired it, that is '
           'the answer.',
          ]),
         ],
         [('Is a Cat S car legal to drive?',
           'Yes, once repaired and with a valid MOT. There is no mandatory structural inspection '
           'before it returns to the road, which is precisely why the quality of the repair '
           'matters so much.'),
          ('How much does Cat S knock off the value?',
           'More than Cat N, and the effect is sharper on newer and more desirable cars. Some '
           'buyers will not consider one at all.'),
          ('Can I insure a Cat S car?',
           'Yes, though fewer insurers will quote and some charge more. Get a quote before you '
           'commit to buying or retaining one.'),
          ('My car is Cat S. Can you repair it?',
           'We will look at it and tell you honestly. Structural work has to be measured and '
           'rebuilt to the manufacturer&rsquo;s dimensions, and if a job needs equipment or '
           'certification we do not have, we will say so rather than taking it on.')],
         [('car-write-off-categories-explained', 'All four categories'),
          ('category-n-write-off', 'Category N explained'),
          ('can-i-keep-my-written-off-car', 'Keeping a written-off car'),
          ('selling-a-cat-s-or-cat-n-car', 'Selling a Cat S or N car')],
         key_points=[
          'S means <strong>something that carries load</strong> was damaged.',
          'Crumple zones <strong>work once</strong>, and only if rebuilt as designed.',
          'Must be <strong>notified to the DVLA</strong>; the car gets a new V5C.',
          'Buying one? <strong>Pay for a structural inspection.</strong> The advert tells you '
          'nothing.',
         ]),

    page('category-a-and-b-write-offs',
         'Category A and B Write-Offs: What They Mean | KITH Cars',
         'The two categories that end a car permanently, the difference between them, why they '
         'exist, and what it means if a car you are looking at is marked A or B.',
         'Category A and B Write-Offs',
         'Insurance &amp; claims &middot; Write-offs',
         'These are the two that are not a decision. A and B cars do not go back on the road, '
         'ever, and the only difference between them is whether anything can be taken off first.',
         [
          ('The difference, which is narrower than people think', [
           ('table', (['', 'Category A', 'Category B'], [
             ['The shell', 'Crushed', 'Crushed'],
             ['The parts', 'Crushed with it', 'May be removed and resold'],
             ['Back on the road', 'Never', 'Never'],
             ['Typical cause', 'Fire, flood, total destruction',
              'Severe structural damage'],
           ])),
           'Both end the vehicle. The only thing B allows is salvage of serviceable components '
           '&mdash; an engine, a gearbox, doors, seats &mdash; before the shell is destroyed.',
          ]),
          ('Why Category A exists at all', [
           'If B allows parts to be reused, why have a category that forbids it? Because some '
           'damage makes the parts themselves unsafe or untraceable.',
           ['<strong>Fire.</strong> Heat changes the properties of metal and plastic in ways you '
            'cannot see. A component that looks fine may have been weakened.',
            '<strong>Flood, particularly salt water.</strong> Corrosion gets everywhere, '
            'including inside wiring looms and connectors, and it keeps working for years.',
            '<strong>Severe contamination.</strong> Chemical spills and some incidents leave '
            'components that cannot safely be reused.',
            '<strong>Total destruction.</strong> Nothing worth salvaging.'],
          ]),
          ('If a car you are looking at is marked A or B', [
           'Walk away, and then think about why it was advertised at all. A Category A or B '
           'vehicle cannot legally return to the road. If someone is selling one as a runner, '
           'either the identity has been changed or the record belongs to a different car.',
           'That is not a bargain, it is a serious problem: an insurance policy on a vehicle '
           'whose identity does not match the record is not worth the paper it is on, and the car '
           'can be seized.',
           ('note', 'A history check costs a few pounds and takes a minute. On any used car '
                    'that is worth doing; on a car with an unusually low price it is essential. '
                    'If the check and the seller disagree, trust the check.'),
          ]),
          ('If yours has been categorised A or B', [
           'There is nothing to repair and nothing to retain. What there is to do is make sure '
           'you are paid properly.',
           ['Check the valuation. They owe you market value, and the category does not change '
            'that.',
            'Take your belongings out, including anything in the boot, the glovebox and the '
            'parcel shelf.',
            'Remove the private plate if you have one, before the car goes.',
            'Cancel or transfer the insurance and tell the DVLA once the insurer confirms '
            'disposal.'],
          ]),
         ],
         [('Can a Category B car be repaired?',
           'No. The shell must be destroyed. Only parts may be salvaged, and only by those '
           'entitled to do so.'),
          ('I have been offered Cat B parts. Is that legal?',
           'Salvaging and selling serviceable parts from a Category B vehicle is legitimate. '
           'Buying a Category B shell to rebuild is not.'),
          ('My car was written off as Cat A but only the interior burned.',
           'Fire damage is categorised cautiously for good reason &mdash; heat affects structure '
           'and wiring well beyond the visible burn. If you think the category is wrong, ask for '
           'the engineer&rsquo;s report and challenge it in writing.'),
          ('Does the category affect what I get paid?',
           'No. The settlement is the market value of the car before the damage, less any excess, '
           'whichever category it ends up in. What the category affects is whether you have the '
           'option to keep it.')],
         [('car-write-off-categories-explained', 'All four categories'),
          ('category-s-write-off', 'Category S explained'),
          ('write-off-valuation-too-low-what-to-do', 'Challenging a low valuation'),
          ('flood-damage-and-your-car', 'Flood damage')],
         key_points=[
          'Both mean the car <strong>never returns to the road</strong>.',
          'The only difference: <strong>B allows parts to be salvaged</strong>, A does not.',
          'A car advertised as a runner but marked A or B is a <strong>serious problem</strong>, '
          'not a bargain.',
          'The category <strong>does not change what you are paid</strong> &mdash; that is market '
          'value either way.',
         ]),

    page('can-i-keep-my-written-off-car',
         'Can I Keep My Written-Off Car? | Salvage Retention | KITH Cars',
         'How to keep a car your insurer has written off, what it costs you from the settlement, '
         'when it is worth doing and when it is not.',
         'Can I Keep My Written-Off Car?',
         'Insurance &amp; claims &middot; Write-offs',
         'Usually yes, if it is a Category S or N and you say so before you accept the '
         'settlement. After the car has gone to salvage, it has gone.',
         [
          ('How retention works', [
           'The insurer pays you the market value, then deducts what they would have received '
           'from the salvage company. You keep the car and the reduced payout.',
           'So the question is not really &ldquo;can I keep it&rdquo;. It is whether what you '
           'keep, after that deduction, is worth more to you than the deduction costs.',
           ('steps', [
             '<strong>Say it early.</strong> <span>At the first mention of a write-off. Once it '
             'is collected for salvage, retention is off the table.</span>',
             '<strong>Ask for both figures.</strong> <span>The full settlement, and the '
             'settlement after the salvage deduction.</span>',
             '<strong>Get a real repair quote.</strong> <span>Bring it to us or send '
             'photographs. Guessing at this stage is how people end up with a car they cannot '
             'afford to fix.</span>',
             '<strong>Then do the sum.</strong> <span>Reduced payout, minus repair cost, against '
             'the full payout. Add the value hit when you later sell.</span>',
           ]),
          ]),
          ('When it is worth it', [
           ['The damage looks worse than it is &mdash; cosmetic panels on an otherwise sound car.',
            'The car is worth more to you than to the market: unusual spec, low mileage, you know '
            'its history.',
            'You intend to keep it for years, so the resale hit never actually lands on you.',
            'Replacing it with something equivalent would cost more than the settlement.'],
          ]),
          ('When it is not', [
           ['You plan to sell within a couple of years. You take the value hit without getting '
            'the use.',
            'It is a Category S and you do not know who will do the structural work.',
            'The repair quote is close to the settlement. At that point you are doing a lot of '
            'work to stand still.',
            'You need the car now. Retaining and repairing takes time that a payout does not.'],
          ]),
          ('The things people forget', [
           'Retaining the salvage does not remove the category. It is recorded permanently and '
           'will appear on every history check from then on.',
           'You will also need to insure it afterwards, and not every insurer quotes on a '
           'recorded write-off. Get an insurance quote <em>before</em> you commit to retention, '
           'not after &mdash; it is the step most often done in the wrong order.',
           ('note', ADVICE_NOTE),
          ]),
         ],
         [('Can the insurer refuse to let me keep it?',
           'On Category A or B, yes &mdash; those cannot return to the road and retention is not '
           'an option. On S and N it is usually allowed, though it is their salvage to sell and '
           'not an absolute right.'),
          ('Do I have to repair it straight away?',
           'No. It is your car. It does need to be roadworthy and have a valid MOT before you '
           'drive it, and an MOT does not check structural repair quality.'),
          ('Will my insurance continue on it?',
           'Not automatically. The policy usually ends on a total loss settlement, so you will be '
           'arranging new cover, on a vehicle with a recorded category.'),
          ('Can you tell me if mine is worth retaining?',
           'Yes, and it is the most useful thing we do at this stage. Bring it in or send '
           'photographs and the registration, and we will give you a proper repair figure to set '
           'against the numbers the insurer gave you.')],
         [('car-write-off-categories-explained', 'All four categories'),
          ('category-n-write-off', 'Category N explained'),
          ('write-off-valuation-too-low-what-to-do', 'Challenging a low valuation'),
          ('is-my-car-worth-repairing-or-writing-off', 'Repair or write off?')],
         key_points=[
          'Say it <strong>before you accept the settlement</strong>. After salvage collection it '
          'is gone.',
          'You get the <strong>payout less the salvage value</strong>, and keep the car.',
          'Get an <strong>insurance quote first</strong> &mdash; not every insurer covers a '
          'recorded write-off.',
          'Worth it if you are <strong>keeping the car for years</strong>; rarely if you are '
          'selling soon.',
         ]),

    page('write-off-valuation-too-low-what-to-do',
         'Write-Off Valuation Too Low? How to Challenge It | KITH Cars',
         'What your insurer actually owes you after a total loss, why the first offer is often '
         'low, and how to build a challenge that works.',
         'Your Write-Off Valuation Is Too Low',
         'Insurance &amp; claims &middot; Write-offs',
         'The first offer is frequently low, challenges frequently succeed, and almost nobody '
         'makes one. What you are owed is the market value of your car &mdash; not the cheapest '
         'number in a trade guide.',
         [
          ('What they actually owe you', [
           'The obligation is to put you back where you were: enough to buy a comparable vehicle '
           'of the same make, model, age, mileage, specification and condition. That is what '
           '&ldquo;market value&rdquo; means, and it is a real-world figure rather than a '
           'notional one.',
           'Insurers typically start from trade valuation guides. Those guides are averages, and '
           'averages are below what you will actually pay a dealer for a specific car this week.',
          ]),
          ('Building the challenge', [
           ('steps', [
             '<strong>Find four or five genuine adverts.</strong> <span>Same model, same engine, '
             'similar age and mileage, from dealers within a reasonable distance. Screenshot '
             'them with the date showing.</span>',
             '<strong>Note everything yours had that the average does not.</strong> <span>Full '
             'service history, optional extras, recent cambelt or tyres, long MOT, one '
             'owner.</span>',
             '<strong>Put it in writing.</strong> <span>Not on the phone. A short email with the '
             'adverts attached and a figure you are asking for.</span>',
             '<strong>Ask what they based theirs on.</strong> <span>Which guides, what mileage '
             'and condition they assumed. Errors here are common and easy to '
             'correct.</span>',
             '<strong>Escalate if needed.</strong> <span>Formal complaint, then the Financial '
             'Ombudsman Service. Both free, and valuation disputes are a routine part of their '
             'work.</span>',
           ]),
          ]),
          ('What moves the figure and what does not', [
           ('table', (['Worth arguing', 'Not worth arguing'], [
             ['Comparable adverts at higher prices', 'What you paid for it'],
             ['Documented full service history', 'Sentimental value'],
             ['Genuine optional extras on the spec', 'Money you still owe on finance'],
             ['Recent major work &mdash; cambelt, clutch, tyres', 'The cost of insuring the next car'],
             ['Mileage below average for the age', 'How inconvenient the whole thing is'],
           ])),
           'Finance is the one that surprises people. If you owe more than the car is worth, the '
           'shortfall is between you and the finance company, and it is what gap insurance '
           'exists for. It does not increase what the motor insurer owes.',
          ]),
          ('If the car can be repaired instead', [
           'Sometimes the better answer is not a higher valuation but no write-off at all. If the '
           'repair genuinely costs less than the insurer assumed, that is worth establishing '
           'before you argue about value.',
           'We will quote the repair properly, and if the figure comes in below their assessment '
           'that is a document worth sending them.',
          ]),
         ],
         [('How long do I have to challenge?',
           'Do not accept the offer while you are disputing it &mdash; acceptance is usually '
           'taken as settlement. Say in writing that you are not accepting and are gathering '
           'evidence.'),
          ('Can I keep driving it while we argue?',
           'Only if it is roadworthy and still insured. Many total-loss cars are not, and some '
           'will already have been collected.'),
          ('They say the guides are binding.',
           'They are not. Guides are evidence of value, not a definition of it, and the Ombudsman '
           'has consistently treated real advertised prices as better evidence.'),
          ('Does challenging delay payment?',
           'It can add a few weeks. On a meaningful gap that is usually time well spent.')],
         [('car-write-off-categories-explained', 'All four categories'),
          ('can-i-keep-my-written-off-car', 'Keeping a written-off car'),
          ('is-my-car-worth-repairing-or-writing-off', 'Repair or write off?'),
          ('category-n-write-off', 'Category N explained')],
         key_points=[
          'They owe you <strong>market value</strong> &mdash; enough to buy a comparable car.',
          'The first offer comes from <strong>trade guides</strong>, which sit below real prices.',
          '<strong>Four or five dated adverts</strong> is the evidence that works.',
          '<strong>Do not accept</strong> while you are disputing &mdash; acceptance usually ends '
          'it.',
         ]),
]
