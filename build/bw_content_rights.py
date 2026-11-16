#!/usr/bin/env python3
"""Insurance cluster: what happens when the repair itself goes wrong.

Sourced from the Financial Ombudsman Service's published approach to vehicle repair complaints
and from its decisions, rather than from general knowledge. That matters for this cluster in a way
it does not elsewhere: these pages tell someone what they are entitled to when a repair has failed,
and being confidently wrong would cost them money.

Where the Ombudsman has stated an approach, the page says so and links to it. Where a figure is a
rule of thumb rather than a rule, it is described as one. Nothing here is presented as legal
advice, and every page carries the standing note.

Source: financial-ombudsman.org.uk, guidance on vehicle repairs, plus published decisions
DRN-3868671 (poor paint preparation, upheld) and DRN-4674146 (paint guarantee, not upheld).
"""

from bw_lib import page, ADVICE_NOTE, CHOICE_NOTE

FOS = ('<a href="https://www.financial-ombudsman.org.uk/businesses/complaints-deal/insurance/'
       'motor-insurance/vehicle-repairs" target="_blank" rel="noopener">'
       'the Financial Ombudsman Service</a>')

PAGES = [

    page('bad-insurance-repair-what-are-my-rights',
         'My Insurance Repair Was Done Badly: What Are My Rights? | KITH Cars',
         'What you are entitled to when an insurance repair has been done poorly, who is '
         'responsible, what evidence wins, and how to escalate. Based on the Ombudsman\'s own '
         'published approach.',
         'The Repair Was Done Badly. Now What?',
         'Insurance &amp; claims &middot; When it goes wrong',
         'If your insurer arranged the repair, your insurer is answerable for it. That single '
         'fact is the one most people do not know, and it is the one that settles most of these '
         'complaints.',
         [
          ('Who is actually responsible', [
           'This is the part that decides everything else, and it turns on who chose the garage.',
           ('table', (['Who arranged the repair', 'Who answers for it'], [
             ['Your insurer&rsquo;s approved repairer', 'Your insurer'],
             ['A garage your insurer told you to use', 'Your insurer'],
             ['Your own choice, with the insurer saying clearly it would not be responsible',
              'The garage'],
             ['Your own choice, with no such warning given',
              'Possibly still your insurer'],
             ['Your own choice, but the insurer took control of the repair',
              'Possibly still your insurer'],
           ])),
           'That is ' + FOS + '&rsquo;s stated approach. The practical upshot: if the work came '
           'through your insurer, complain to your insurer. Do not let them point you at the '
           'bodyshop and step back.',
          ]),
          ('What the repair is supposed to achieve', [
           'The test is not whether the repair looks acceptable. It is whether the car has been '
           'put back to the condition it was in before the damage.',
           'If it has not, the Ombudsman may require the insurer to have it put right by their '
           'repairer, to pay for you to use a repairer of your own, or &mdash; where the car '
           'cannot be properly restored &mdash; to write it off and pay you its pre-accident '
           'market value.',
          ]),
          ('The evidence that actually wins', [
           'These complaints turn on evidence, and one kind beats all the others.',
           ('steps', [
             '<strong>An independent engineer&rsquo;s report.</strong> <span>The Ombudsman '
             'describes independent expert evidence as what it often finds most persuasive. '
             'Yours will cost you, and it is frequently the thing that decides it.</span>',
             '<strong>Contemporaneous evidence beats later evidence.</strong> <span>In one '
             'upheld decision the insurer&rsquo;s paint specialist report was written after the '
             'event to record findings nobody had documented at the time, and little weight was '
             'given to it.</span>',
             '<strong>Photographs of the car before the damage.</strong> <span>The condition it '
             'was in beforehand is half the test, and almost nobody has this. Old MOT '
             'photographs, sale adverts and service records all help.</span>',
             '<strong>A written opinion from another bodyshop.</strong> <span>Cheaper than an '
             'engineer and still useful. Ask for the cause, not just the fault.</span>',
             '<strong>Dates.</strong> <span>When the car went in, when it came back, when you '
             'first complained. Timelines decide arguments about whether a fault was present on '
             'return.</span>',
           ]),
          ]),
          ('The "you should have spotted it sooner" argument', [
           'Insurers sometimes argue a paint fault would have been visible within days of '
           'collection, so a complaint months later must be about something new.',
           'It is not automatically wrong &mdash; fresh stone chips and kerbing genuinely do '
           'cause bubbling, and one Ombudsman decision went against the customer for exactly '
           'that reason. But it depends on the timeline, and in another the argument failed '
           'because the final inspection had happened only six days after the car was painted '
           'and other paint on the same car needed redoing within two months.',
           'If that argument is put to you, ask for the dates it relies on and check them '
           'against your own.',
          ]),
          ('How to escalate', [
           ('steps', [
             '<strong>Complain to the insurer in writing.</strong> <span>Not the bodyshop, if '
             'the insurer arranged it. Set out the fault, the dates and what you want '
             'done.</span>',
             '<strong>Ask for their final response.</strong> <span>That is the formal document '
             'that opens the next door.</span>',
             '<strong>Get your own evidence while you wait.</strong> <span>An inspection, '
             'photographs in daylight, a second opinion.</span>',
             '<strong>Take it to the Ombudsman.</strong> <span>Free, and they routinely handle '
             'repair-quality complaints. Normally within six months of the final '
             'response.</span>',
             '<strong>Keep driving it or not?</strong> <span>If it is unsafe, stop. If it is '
             'cosmetic, carry on and photograph it as it changes.</span>',
           ]),
           ('note', ADVICE_NOTE),
          ]),
          ('What we can do', [
           'We inspect repairs other people have done and tell you what we find, in writing, '
           'with photographs. Not a sales exercise &mdash; sometimes the answer is that the work '
           'is acceptable and the colour difference is one you will stop seeing.',
           'Where it is not acceptable, a written report naming the fault and its cause is '
           'exactly the evidence that moves a complaint. We are on no insurer&rsquo;s panel, so '
           'we have no relationship with whoever did the work to protect.',
           ('note', CHOICE_NOTE),
          ]),
         ],
         [('The bodyshop says it is within tolerance.',
           'Ask to see it with them, outside, in daylight. "Within tolerance" is reasonable for a '
           'measured difference and not for something you can see from across the road. If the '
           'insurer arranged the repair, put the complaint to the insurer regardless of what the '
           'bodyshop says.'),
          ('Can I just take it somewhere else and send the bill?',
           'Not safely. Tell the insurer the repair has failed and give them the chance to put it '
           'right first. The Ombudsman can require them to pay for another repairer, but that '
           'normally follows a complaint rather than a bill arriving unannounced.'),
          ('How long do I have to complain?',
           'Raise it with the insurer as soon as you notice. For the Ombudsman, it is normally '
           'six months from the insurer’s final response, and generally six years from the '
           'event. Sooner is always stronger, because paint faults are easier to attribute early.'),
          ('Does it cost anything to go to the Ombudsman?',
           'Not to you. It is free for consumers. You may choose to pay for an engineer’s '
           'report, and that is usually the money worth spending.'),
          ('What if the car cannot be properly repaired at all?',
           'Then the Ombudsman may require the insurer to write it off and pay the pre-accident '
           'market value. That is the remedy where a car cannot be restored to its previous '
           'condition.')],
         [('mismatched-parts-after-a-repair', 'Mismatched parts after a repair'),
          ('repair-delays-and-loss-of-use', 'Delays and loss of use'),
          ('second-hand-parts-on-an-insurance-repair', 'Second-hand parts'),
          ('why-repairs-dont-match', 'Why some repairs do not match')],
         key_points=[
          'If your <strong>insurer arranged it</strong>, your insurer answers for it.',
          'The test is whether the car is back to its <strong>pre-accident condition</strong>.',
          'An <strong>independent engineer&rsquo;s report</strong> is what usually decides it.',
          'The Ombudsman is <strong>free</strong>, and handles these routinely.',
         ]),

    page('mismatched-parts-after-a-repair',
         'Mismatched Parts After a Repair: What You Are Owed | KITH Cars',
         'What happens when a replacement part does not match the rest of the car, including the '
         'Ombudsman\'s approach of paying for the damaged part plus half the cost of the set.',
         'When the Replacement Does Not Match',
         'Insurance &amp; claims &middot; When it goes wrong',
         'One new alloy among three old ones. A replacement trim that is a different shade. There '
         'is an established way this gets settled, and almost nobody is told about it.',
         [
          ('The rule of thumb nobody mentions', [
           'Where a part cannot be matched to the rest of a set, ' + FOS + ' describes an '
           'approach of paying for the damaged part <em>plus half the cost of replacing the rest '
           'of the set</em>.',
           'The logic is that replacing the whole set leaves you better off than before the '
           'accident, and replacing only one leaves you worse off. Splitting the difference on '
           'the remainder is the compromise.',
           ('table', (['Situation', 'Typical outcome'], [
             ['A matching part is available', 'It is fitted. No issue.'],
             ['A reasonably close part is available', 'That is normally considered enough'],
             ['Nothing matches &mdash; one of a set',
              'The damaged part, plus around half the cost of the rest'],
             ['Paint cannot be matched', 'A respray, or the cash equivalent'],
           ])),
          ]),
          ('Where this comes up', [
           ['<strong>Alloy wheels.</strong> The classic case. One kerbed wheel on a set of four, '
            'a discontinued design, and no match available.',
            '<strong>Trim and mouldings.</strong> Faded by years of sun, so a new one is visibly '
            'darker even in the correct colour.',
            '<strong>Headlights.</strong> One new clear unit beside one yellowed with age.',
            '<strong>Paint.</strong> Where the original has faded beyond what blending can '
            'bridge.'],
          ]),
          ('What to do about it', [
           ('steps', [
             '<strong>Raise it before the work is signed off.</strong> <span>Much easier than '
             'afterwards.</span>',
             '<strong>Ask what was searched.</strong> <span>Whether a matching part was looked '
             'for new, used and from the manufacturer, and what came back.</span>',
             '<strong>Photograph the mismatch in daylight.</strong> <span>Alongside the '
             'unmatched items, so the difference is visible in one frame.</span>',
             '<strong>Ask for the set to be addressed.</strong> <span>Naming the half-cost '
             'approach. It is their own trade body&rsquo;s territory, not something you have '
             'invented.</span>',
             '<strong>Complain and escalate if refused.</strong> <span>This is well-trodden '
             'ground at the Ombudsman.</span>',
           ]),
           ('note', ADVICE_NOTE),
          ]),
          ('The honest caveat', [
           'A reasonably close match is normally considered sufficient, and "reasonably close" '
           'does a lot of work in that sentence. If a replacement is marginally different in a '
           'way you notice and most people would not, you are unlikely to get far.',
           'The argument is strongest where the difference is obvious to anyone looking &mdash; '
           'one bright wheel among three dull ones, a headlight that is visibly a different '
           'colour from its partner.',
          ]),
          ('What we do about it', [
           'On alloys we refurbish rather than replace wherever the wheel allows it, which sides '
           'the problem entirely: a refurbished wheel can be finished to match its neighbours, '
           'and a new one cannot be made older.',
           'Where a part genuinely cannot be matched we say so at the estimate rather than at '
           'handover, so the conversation with your insurer happens before the car is in pieces.',
          ]),
         ],
         [('Can I insist on all four wheels being done?',
           'You can ask. The usual landing point is the damaged one plus a contribution toward '
           'the rest, rather than the full set, because a full set would leave you better off '
           'than before the accident.'),
          ('They fitted a used part. Is that allowed?',
           'Generally second-hand parts are not considered fair unless the car is very old, a '
           'classic, or a limited edition where new parts are not available. See the separate '
           'page on that.'),
          ('The new bumper is a slightly different white.',
           'That is a paint matching question rather than a parts one, and it usually has a '
           'better answer: blending into the neighbouring panels. If it was not blended, that is '
           'the complaint to make.'),
          ('Does this apply if I paid privately?',
           'The Ombudsman approach is about insurers. Paying privately, it is a contract matter '
           'between you and the bodyshop &mdash; which is why we tell you before the work if a '
           'part cannot be matched.')],
         [('bad-insurance-repair-what-are-my-rights', 'When a repair is done badly'),
          ('second-hand-parts-on-an-insurance-repair', 'Second-hand parts'),
          ('why-repairs-dont-match', 'Why some repairs do not match'),
          ('kerb-damage-repair', 'Kerb damage repair')],
         key_points=[
          'Unmatched part in a set? The approach is <strong>the damaged part plus about half '
          'the cost of the rest</strong>.',
          'A <strong>reasonably close</strong> match is normally considered enough.',
          'Where <strong>paint</strong> cannot be matched, a respray or the cash equivalent may '
          'be fair.',
          '<strong>Raise it before sign-off.</strong> Far easier than afterwards.',
         ]),

    page('second-hand-parts-on-an-insurance-repair',
         'Can My Insurer Use Second-Hand Parts? | KITH Cars',
         'When used or recycled parts are acceptable on an insurance repair and when they are '
         'not, what betterment means, and what to do if you object.',
         'Can They Fit Second-Hand Parts?',
         'Insurance &amp; claims &middot; When it goes wrong',
         'Generally not, and that is firmer than most people expect. Used parts are normally only '
         'considered fair on a car old enough, classic enough or rare enough that new ones are '
         'not realistically available.',
         [
          ('The general position', [
           ' ' + FOS + ' takes the view that using second-hand parts is generally not fair, with '
           'the exception of vehicles that are very old, classic, or limited edition.',
           'The reasoning runs through the whole of motor claims: the insurer owes you the car '
           'you had, not a cheaper approximation of it. A used part of unknown history is not '
           'the same thing as the part that was on your car.',
          ]),
          ('Where used parts are reasonable', [
           ['<strong>Classics and older cars</strong> where new panels simply are not made any '
            'more.',
            '<strong>Limited editions</strong> where a used original is closer to correct than a '
            'modern replacement.',
            '<strong>Discontinued trim and fittings</strong> that cannot be bought new at any '
            'price.',
            '<strong>Where you ask for it</strong>, because it is cheaper and you would rather '
            'have the money.'],
           'The thread through all of those is availability, not cost. "We can get a used one '
           'cheaper" is not on the list.',
          ]),
          ('Betterment, the argument in the other direction', [
           'The mirror of this is betterment: where a repair leaves you better off than before. '
           'A new exhaust on a fifteen-year-old car, a new battery, new tyres with full tread '
           'where the old ones were nearly worn out.',
           'Insurers sometimes ask you to contribute in those cases, and that can be reasonable '
           '&mdash; you are getting a new item in place of a worn one. What it is not is a '
           'general licence to fit used parts, and the two arguments get conflated more often '
           'than they should.',
           ('note', ADVICE_NOTE),
          ]),
          ('If you object', [
           ('steps', [
             '<strong>Say so before the parts are ordered.</strong> <span>Once they are fitted '
             'the conversation is much harder.</span>',
             '<strong>Ask what grade is specified, in writing.</strong> <span>Genuine, '
             'matching-quality, or recycled. The estimate will say.</span>',
             '<strong>Ask why.</strong> <span>If the answer is availability, that is a reason. '
             'If it is cost, say that you do not accept it.</span>',
             '<strong>Offer to pay the difference if you want better.</strong> <span>Often the '
             'quickest route to the part you actually want.</span>',
             '<strong>Complain and escalate if it is refused.</strong> <span>Through the '
             'insurer’s complaints process first.</span>',
           ]),
          ]),
          ('What we fit', [
           'New, unless you ask otherwise or the part is genuinely not available new. Where your '
           'insurer authorises only matching-quality equivalents and you want genuine, we will '
           'show you both figures and you can pay the difference if you want to.',
           'If a used part is the sensible answer &mdash; and on an older car it sometimes is '
           '&mdash; we will say so and tell you what we know about its origin.',
           ('note', CHOICE_NOTE),
          ]),
         ],
         [('What is a "matching quality" part?',
           'A new part made by someone other than the original manufacturer to equivalent '
           'specification. It is not second-hand. On common cars they fit well; on some they do '
           'not, which is the argument for genuine.'),
          ('They want me to contribute for betterment. Is that fair?',
           'It can be, where you are genuinely getting a new item in place of a worn one &mdash; '
           'tyres and exhausts are the usual examples. Ask for the calculation rather than '
           'accepting a round number.'),
          ('My car is twelve years old. Does that count as "very old"?',
           'Probably not on its own. The test is closer to whether new parts are realistically '
           'available than to a specific age, and for a twelve-year-old mainstream car they '
           'usually are.'),
          ('Can I ask for used parts to keep the cost down?',
           'Yes, and on an older car paid for privately that is often a sensible choice. We will '
           'tell you where we would and would not do it &mdash; safety-related parts are a no.')],
         [('bad-insurance-repair-what-are-my-rights', 'When a repair is done badly'),
          ('mismatched-parts-after-a-repair', 'Mismatched parts after a repair'),
          ('insurer-approved-repairer-vs-independent-bodyshop', 'Approved vs independent'),
          ('what-happens-if-i-use-a-non-approved-garage', 'Using your own garage')],
         key_points=[
          '<strong>Generally not fair</strong>, except on very old, classic or limited-edition '
          'cars.',
          'The test is <strong>availability</strong>, not cost.',
          '<strong>Betterment</strong> is the opposite argument and gets conflated with this one.',
          'Object <strong>before the parts are ordered</strong>.',
         ]),

    page('repair-delays-and-loss-of-use',
         'Repair Delays: What You Can Claim for Loss of Use | KITH Cars',
         'What counts as an unreasonable repair delay, what you can claim while the car is off '
         'the road, and the Ombudsman\'s approach to courtesy cars and hire costs.',
         'The Repair Is Taking Too Long',
         'Insurance &amp; claims &middot; When it goes wrong',
         'There is a remedy for this, and it has a name: loss of use. Most people put up with '
         'the delay because nobody tells them it exists.',
         [
          ('What counts as unreasonable', [
           'There is no fixed number of days. ' + FOS + ' looks at what a reasonable repair time '
           'would have been for that job, who caused any delay beyond it, and &mdash; this is '
           'the part people miss &mdash; how the insurer set your expectations in the first place.',
           'A four-week repair is not unreasonable if the car needed a panel that was on back '
           'order and you were told so at the start. The same four weeks is a different matter '
           'if you were promised a week and chased it yourself for the other three.',
          ]),
          ('What you can be owed', [
           ('table', (['Remedy', 'When it applies'], [
             ['A courtesy car', 'You were entitled to one and did not get it'],
             ['Loss of use payment', 'You had no vehicle and no replacement was provided'],
             ['Hire costs covered', 'You hired reasonably and at standard commercial rates'],
             ['Compensation for inconvenience', 'The handling itself caused distress or trouble'],
           ])),
           'On hire, the test is whether you acted reasonably and whether the price matches '
           'standard commercial rates for a like-for-like vehicle. Hiring something grander than '
           'your own car, or at a premium rate when ordinary rates were available, weakens it.',
          ]),
          ('Loss of use, the one nobody claims', [
           'If you were entitled to a replacement vehicle and did not get one, you can be '
           'compensated for not having had a car &mdash; even if you did not hire anything.',
           'Whether it applies, and how much, depends on your circumstances: whether you had '
           'another vehicle available, and whether you could reasonably have reduced your costs. '
           'Someone with a second car in the drive has a weaker claim than someone who took '
           'taxis to work for a fortnight.',
           ('steps', [
             '<strong>Keep a diary.</strong> <span>Dates the car was off the road, and what you '
             'did instead.</span>',
             '<strong>Keep receipts.</strong> <span>Taxis, trains, hire, anything the lack of a '
             'car cost you.</span>',
             '<strong>Note every promised date and every time it moved.</strong> <span>This is '
             'the record that establishes expectations were not met.</span>',
             '<strong>Ask for a courtesy car in writing.</strong> <span>A refused written '
             'request is far better evidence than a forgotten phone call.</span>',
           ]),
          ]),
          ('Who actually caused the delay', [
           'Worth being even-handed: not every delay is the insurer&rsquo;s fault, and a '
           'bodyshop waiting on a part from a manufacturer is not stalling.',
           'What does count against them is authorisation that sat on a desk, a supplementary '
           'that took three weeks to approve, an engineer who did not attend, and dates promised '
           'that were never realistic. Those are handling failures rather than supply problems, '
           'and they are the ones that carry weight.',
           ('note', ADVICE_NOTE),
          ]),
          ('How we try not to be the cause', [
           'We book a car in once the parts are on the shelf wherever we can, so it is not '
           'standing stripped waiting for something on back order. When a part is delayed '
           'mid-repair we tell you as soon as we know rather than letting the promised date drift.',
           'And we give you a real date rather than an optimistic one. An estimate that is always '
           '&ldquo;tomorrow&rdquo; for a week is worse than an honest fortnight.',
          ]),
         ],
         [('How long should a repair take?',
           'A localised repair is often same or next day; a panel off, painted and refitted two '
           'to three days; structural work one to two weeks. On a claim, authorisation and parts '
           'usually add more than the work itself.'),
          ('They gave me a courtesy car but it is far smaller than mine.',
           'On a fault claim you usually get what the policy specifies. On a non-fault claim you '
           'are entitled to like-for-like. If you have specific needs — seats, towing, an '
           'automatic — say so explicitly and in writing.'),
          ('Can I just hire a car and send them the bill?',
           'Tell them first and give them the chance to provide one. If you do hire, keep it '
           'reasonable and like-for-like, and keep the invoice.'),
          ('Does loss of use apply if I never hired anything?',
           'It can. That is precisely what it is for — being without a car you were entitled '
           'to have replaced. How much depends on your circumstances.')],
         [('how-long-does-bodywork-take', 'How long bodywork takes'),
          ('am-i-entitled-to-a-courtesy-car', 'Courtesy car entitlement'),
          ('credit-hire-explained', 'Credit hire explained'),
          ('bad-insurance-repair-what-are-my-rights', 'When a repair is done badly')],
         key_points=[
          'There is no fixed number of days &mdash; it turns on <strong>what was '
          'reasonable</strong> and <strong>what you were told</strong>.',
          '<strong>Loss of use</strong> can apply even if you never hired anything.',
          'Keep a <strong>diary of dates</strong> and every promised date that moved.',
          'Ask for a courtesy car <strong>in writing</strong>. A refused written request is '
          'evidence.',
         ]),
]
