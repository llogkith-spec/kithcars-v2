#!/usr/bin/env python3
"""Insurance cluster, part 2: choice of repairer (remainder) and fault/liability."""

from bw_lib import page, CHOICE_NOTE

PAGES = [

    page('right-to-choose-your-own-bodyshop',
         'Your Right to Choose Your Own Bodyshop | KITH Cars',
         'Where the right to pick your own repairer comes from, what insurers are allowed to put '
         'in the policy, and how to exercise it without the claim stalling.',
         'Your Right to Choose Your Own Bodyshop',
         'Insurance &amp; claims &middot; Choice of repairer',
         'The car belongs to you. The contract with the insurer obliges them to put it back the '
         'way it was, not to decide whose hands do the work. Knowing where that line sits makes '
         'the phone call much shorter.',
         [
          ('Where the right comes from', [
           'It is not a special motoring rule &mdash; it is ordinary contract and property law. '
           'Your policy is a promise to indemnify you: to restore your position after a loss. It '
           'is not a promise to deliver a repair through a particular supplier, unless the policy '
           'explicitly says so and you accepted that when you bought it.',
           'That is why the honest answer to &ldquo;am I allowed?&rdquo; is that the question is '
           'the wrong way round. You do not need permission to choose. The insurer needs a term '
           'in the contract to restrict you, and most restrict the <em>consequences</em> rather '
           'than the choice itself.',
          ]),
          ('What a policy can legitimately say', [
           'Read the claims-handling or repairs section, not the summary document. Common terms '
           'that are perfectly enforceable:',
           ['A higher excess applies if you use a repairer outside their network.',
            'The courtesy car is only provided through their network.',
            'Their repair guarantee only covers work their network carried out.',
            'They will pay no more than the cost they would have incurred themselves.'],
           'None of those stop you. They change what the choice costs you, which is a different '
           'thing, and the last one is the only one that usually matters financially.',
          ]),
          ('Doing it without the claim stalling', [
           ('steps', [
             '<strong>Report the incident first.</strong> <span>Do that promptly whatever you '
             'decide about the garage. Late notification is the one thing that genuinely '
             'prejudices a claim.</span>',
             '<strong>Name your repairer at the same time.</strong> <span>Doing it on the first '
             'call avoids the car being booked into their network and then moved.</span>',
             '<strong>Get the authorised rate in writing.</strong> <span>One email. &ldquo;Please '
             'confirm the labour rate authorised and any shortfall payable by me.&rdquo;</span>',
             '<strong>Send us the claim reference.</strong> <span>We take it from there with the '
             'engineer.</span>',
           ]),
          ]),
          ('If they will not budge', [
           'Occasionally a handler simply repeats the script. Ask for it in writing: &ldquo;Please '
           'confirm in writing that you are refusing to allow my chosen repairer, and quote the '
           'policy clause.&rdquo; Almost nobody puts that in writing, because the clause usually '
           'does not exist.',
           'If it genuinely goes nowhere, insurers have a complaints procedure and a final '
           'response, after which the Financial Ombudsman Service will look at it for free. That '
           'is rarely needed over the choice of garage, but knowing the route exists changes the '
           'tone of the conversation.',
          ]),
         ],
         [('Will using you cost me more?',
           'Only if your insurer authorises less than the job takes, and we settle that before '
           'starting rather than presenting you with a shortfall at the end. On many claims there '
           'is no difference to you at all.'),
          ('Do I lose the courtesy car?',
           'Possibly, if your policy ties the courtesy car to their network. Ask. If it is tied, '
           'weigh it against what you gain &mdash; and on a non-fault claim there is usually a '
           'replacement vehicle available regardless.'),
          ('What about the repair guarantee?',
           'Theirs covers their network. We guarantee our own paint for a year and the bodywork '
           'we carry out, which is the guarantee that matters on your car.'),
          ('Does this apply to a lease or company car?',
           'Not always. If you do not own the car, the lease or fleet agreement may specify where '
           'it gets repaired, and that contract binds you. Check with the lease company first.')],
         [('do-i-have-to-use-my-insurers-approved-repairer', 'Do I have to use their repairer?'),
          ('insurer-approved-repairer-vs-independent-bodyshop', 'Approved vs independent'),
          ('what-happens-if-i-use-a-non-approved-garage', 'Using a non-approved garage'),
          ('how-a-bodywork-insurance-claim-works-step-by-step', 'How a claim works')],
         key_points=[
          'The choice is <strong>yours by default</strong>. The insurer needs a policy term to '
          'restrict it.',
          'Terms usually change <strong>what the choice costs</strong>, not whether you have it.',
          'Name your repairer on the <strong>first call</strong>, before the car is booked in '
          'anywhere.',
          'Get the <strong>authorised labour rate in writing</strong>.',
         ]),

    page('insurer-approved-repairer-vs-independent-bodyshop',
         'Approved Repairer vs Independent Bodyshop: Which Is Better? | KITH Cars',
         'An honest comparison of insurer-approved networks and independent bodyshops: speed, '
         'parts, labour times, guarantees and who the arrangement is really built to suit.',
         'Approved Repairer or Independent Bodyshop?',
         'Insurance &amp; claims &middot; Choice of repairer',
         'Both can do good work and both can do bad work. The difference is not skill, it is who '
         'the commercial arrangement was designed to suit &mdash; and that shows up in the labour '
         'time allowed and the grade of parts specified.',
         [
          ('The comparison, honestly', [
           ('table', (['', 'Approved network', 'Independent'], [
             ['Who negotiated the rate', 'The insurer, before your accident', 'Us, on your job'],
             ['Parts normally specified', 'Often matching-quality or recycled',
              'Your call &mdash; we quote both'],
             ['Courtesy car', 'Usually included', 'Depends on your policy'],
             ['Repair guarantee', 'The insurer&rsquo;s', 'Ours &mdash; paint guaranteed a year'],
             ['Who they answer to', 'The insurer who sends the work',
              'You, because you chose us'],
             ['Speed', 'Can be quicker to authorise', 'Comparable once authorised'],
           ])),
           'The row that does the work is the last-but-one. An approved shop depends on the '
           'insurer for its workflow. That is not corruption, it is just where the pressure '
           'points. If an engineer disputes two hours of labour, the shop that needs next '
           'month&rsquo;s referrals has a different incentive to the shop that does not.',
          ]),
          ('Where approved networks are genuinely good', [
           'Volume brings real advantages: dedicated insurer liaison, faster authorisation, '
           'courtesy cars on tap and well-drilled processes. For a straightforward bumper and '
           'wing on a three-year-old car, a good approved shop is a perfectly sensible choice, '
           'and the admin is lighter for you.',
           'Worth saying plainly: we are not claiming the network is a scam. It is a supply '
           'arrangement that suits some jobs and some owners.',
          ]),
          ('Where it goes wrong', [
           ['<strong>Labour time squeezed.</strong> Pre-agreed rates mean the shop absorbs the '
            'gap or works to the allowed time. Blending paint into adjacent panels is often the '
            'first thing cut, and it is the thing you will see in sunlight.',
            '<strong>Parts grade.</strong> &ldquo;Matching quality&rdquo; non-genuine panels fit '
            'well on common cars and badly on others. On a car still under manufacturer paint '
            'warranty this is worth checking.',
            '<strong>Nobody argues for you.</strong> If the strip-down reveals more damage, '
            'someone has to raise a supplementary and defend it.'],
          ]),
          ('How to choose for your car', [
           'A rough rule: the newer, rarer or more expensively painted the car, the more the '
           'choice matters. A solid-white fleet hatchback is hard to get wrong. A three-stage '
           'pearl, a metallic that shifts in the light, or an aluminium panel is not.',
           ('note', CHOICE_NOTE),
          ]),
         ],
         [('Are independents cheaper?',
           'Not necessarily, and that is not the pitch. We are often the same or slightly more '
           'per hour than a pre-negotiated network rate, because the rate has not been discounted '
           'in advance. What you get for it is the time the job needs.'),
          ('Will the insurer trust an independent estimate?',
           'Yes. The engineer inspects and authorises the same way regardless. We produce '
           'estimates on the same industry systems insurers use.'),
          ('Can I get genuine parts?',
           'You can ask for them. The insurer may only authorise the cost of matching-quality '
           'equivalents, in which case you can pay the difference. We will show you both figures.'),
          ('How do I judge any bodyshop?',
           'Ask what paint system they use, whether they blend into adjacent panels, what the '
           'paint guarantee is and in writing, and ask to see a car they are working on. A shop '
           'proud of its work will show you.')],
         [('do-i-have-to-use-my-insurers-approved-repairer', 'Do I have to use their repairer?'),
          ('right-to-choose-your-own-bodyshop', 'Your right to choose'),
          ('what-happens-if-i-use-a-non-approved-garage', 'Using a non-approved garage'),
          ('paint-colour-matching-explained', 'How paint matching works')],
         key_points=[
          'Both can be good. The difference is <strong>whose costs the rate was built to '
          'suit</strong>.',
          'The squeeze usually shows in <strong>labour time</strong> and <strong>parts '
          'grade</strong>.',
          'Approved networks are genuinely <strong>faster on admin</strong> and usually include '
          'a courtesy car.',
          'The choice matters most on <strong>newer cars and difficult paint</strong>.',
         ]),

    page('what-happens-if-i-use-a-non-approved-garage',
         'What Happens If I Use a Non-Approved Garage? | KITH Cars',
         'The real consequences of going outside your insurer\'s network: excess, courtesy car, '
         'guarantee, authorised rates and shortfalls. What to check before you commit.',
         'What Happens If I Use a Non-Approved Garage?',
         'Insurance &amp; claims &middot; Choice of repairer',
         'Four things can change, and only one of them usually costs you money. Knowing which is '
         'which before you book the car in is the whole trick.',
         [
          ('The four things that can change', [
           ('table', (['What changes', 'How likely', 'What to do about it'], [
             ['Higher excess', 'Occasional &mdash; policy dependent',
              'Check the repairs clause before you commit'],
             ['No courtesy car', 'Common if the car is tied to their network',
              'Ask; on a non-fault claim there are other routes'],
             ['No insurer guarantee', 'Standard',
              'Get your repairer&rsquo;s own guarantee in writing'],
             ['Authorised at their rate, you pay the gap', 'The one that bites',
              'Settle the rate in writing before work starts'],
           ])),
          ]),
          ('The shortfall, in plain terms', [
           'Insurers indemnify you for a reasonable cost of repair, and they treat their own '
           'negotiated rate as the benchmark for reasonable. If your repairer charges more per '
           'hour, the insurer may authorise only up to their figure and leave the balance to you.',
           'On a small job the gap is often tens of pounds or nothing. On a large job with a lot '
           'of labour it can be a few hundred. That is exactly why we get the authorised rate '
           'confirmed before the car comes in, rather than discovering it at handover.',
          ]),
          ('What does not change', [
           ['Your right to claim at all.',
            'The insurer&rsquo;s duty to put the car back as it was.',
            'Your no-claims position &mdash; that follows fault, not the choice of garage.',
            'Your manufacturer warranty on mechanical parts.'],
          ]),
          ('A sensible order of operations', [
           ('steps', [
             '<strong>Report it.</strong> <span>Promptly. Do not wait while you decide on a '
             'garage.</span>',
             '<strong>Read the repairs clause.</strong> <span>In the policy wording, not the '
             'certificate. Look for excess and courtesy car wording.</span>',
             '<strong>Ask the two questions.</strong> <span>&ldquo;What rate are you authorising, '
             'and does my excess change?&rdquo; In writing.</span>',
             '<strong>Then decide.</strong> <span>With the numbers in front of you rather than '
             'the handler&rsquo;s script.</span>',
           ]),
          ]),
         ],
         [('Can they refuse the claim entirely?',
           'Not because of your choice of garage. They can decline a claim for non-disclosure, '
           'late notification or a policy breach &mdash; none of which is picking your own '
           'repairer.'),
          ('What if the work is done and they then underpay?',
           'That is why the rate goes in writing first. If it has already happened, put a '
           'complaint in writing and escalate to the Financial Ombudsman Service if their final '
           'response is unreasonable.'),
          ('Is it worth it for a small job?',
           'If the repair is close to your excess, the better question is whether to claim at '
           'all. Get a direct price from us and compare.'),
          ('Do you handle the insurer side?',
           'Yes &mdash; the estimate, the engineer, and any supplementary if the strip-down finds '
           'more than the photographs showed. You make the first notification call.')],
         [('do-i-have-to-use-my-insurers-approved-repairer', 'Do I have to use their repairer?'),
          ('right-to-choose-your-own-bodyshop', 'Your right to choose'),
          ('who-pays-my-excess', 'Who pays my excess'),
          ('should-i-claim-or-pay-myself', 'Claim or pay yourself?')],
         key_points=[
          'Four things can change &mdash; excess, courtesy car, guarantee and the '
          '<strong>authorised rate</strong>.',
          'Only the <strong>rate</strong> usually costs you anything.',
          'Your claim, your no-claims and the insurer&rsquo;s duty to repair <strong>do not '
          'change</strong>.',
          'Get the rate and the excess <strong>confirmed in writing</strong> before booking in.',
         ]),

    page('non-fault-accident-what-to-do',
         'Non-Fault Accident: What to Do Step by Step | KITH Cars',
         'What to do after an accident that was not your fault — at the scene, in the first 48 '
         'hours, and through the claim. Excess, replacement car and choice of repairer.',
         'Non-Fault Accident: What to Do',
         'Insurance &amp; claims &middot; Fault and liability',
         'Someone else hit you. Handled properly this costs you nothing and your no-claims should '
         'survive intact. Handled badly it costs you your excess, your discount and a fortnight '
         'without a car.',
         [
          ('At the scene', [
           ('steps', [
             '<strong>Stop, and swap details.</strong> <span>Name, address, vehicle registration '
             'and insurer. Failing to exchange details after an accident involving injury or '
             'damage to someone else&rsquo;s property is an offence.</span>',
             '<strong>Photograph before anything moves.</strong> <span>Both cars, both '
             'registrations, the damage close up, and a wide shot showing the position of the '
             'vehicles and the road layout.</span>',
             '<strong>Get a witness.</strong> <span>A name and number from anyone who saw it. '
             'This is the single most valuable thing at the scene and the most commonly '
             'skipped.</span>',
             '<strong>Do not accept blame.</strong> <span>Not at the scene, not in a text '
             'afterwards. You may not know what happened yet. Be civil, say nothing about '
             'fault.</span>',
           ]),
          ]),
          ('The first 48 hours', [
           'Report it to your own insurer even if you do not intend to claim through them. Most '
           'policies require notification of any incident, and late notification is one of the '
           'few things that genuinely damages a claim.',
           'Expect a call from the <em>other</em> driver&rsquo;s insurer. This is third party '
           'capture: they ring you directly, offer to sort the repair and a car, and in doing so '
           'keep the cost down and keep you away from a credit hire claim. You are under no '
           'obligation to accept, and you still choose the repairer.',
           ('note', CHOICE_NOTE),
          ]),
          ('What you should not be paying for', [
           'On a genuine non-fault claim, properly handled, you should end up out of pocket for '
           'nothing. In practice:',
           ['<strong>Excess.</strong> Often payable up front and recovered later. Ask whether it '
            'can be waived given liability.',
            '<strong>Replacement vehicle.</strong> You are entitled to a like-for-like '
            'replacement while yours is off the road, not a token city car if you drive an '
            'estate.',
            '<strong>Recovery and storage.</strong> Recoverable from the at-fault insurer.',
            '<strong>Loss of earnings and out-of-pocket costs.</strong> Keep receipts.'],
          ]),
          ('Where non-fault claims leak money', [
           'Three places, consistently. The excess that nobody chased. The no-claims discount '
           'lost because the insurer never recovered its outlay and recorded the claim as '
           'unsettled. And the repair squeezed to a budget because nobody argued the labour time.',
           'Ask your insurer, in writing, for confirmation when the claim settles and when your '
           'excess is returned. If it has not moved in three months, chase it.',
          ]),
         ],
         [('Should I claim through my insurer or theirs?',
           'Through yours is usually safer: you keep the protection of your own policy if '
           'liability turns out to be disputed. Claiming directly against the other insurer '
           'avoids your excess but leaves you on your own if it goes sour.'),
          ('Will my premium go up even though it was not my fault?',
           'It can. Insurers price on claim frequency as well as fault. A fully recovered '
           'non-fault claim should not cost you your no-claims discount, but it may still appear '
           'at renewal. Ask for it to be recorded as settled in your favour.'),
          ('The other driver asked to settle privately. Should I?',
           'Be careful. It can work for a small scuff, but you lose all protection if the damage '
           'turns out to be worse at strip-down or if they stop answering the phone. Get a proper '
           'estimate first so you know the real figure.'),
          ('Do I have to use the car hire company their insurer suggests?',
           'No. And be clear about what you are signing &mdash; credit hire agreements are '
           'legitimate but you are the one who signs for the cost if recovery fails.'),
          ('Can you deal with the other side for me?',
           'Yes. Send us the registration and we will estimate the damage and handle the engineer '
           'and the estimate with whichever insurer is paying.')],
         [('fault-accident-what-happens-next', 'If it was your fault'),
          ('recovering-your-excess-after-a-non-fault-accident', 'Recovering your excess'),
          ('third-party-capture-insurer-calling-you', 'Third party capture'),
          ('will-a-non-fault-claim-affect-my-no-claims', 'Non-fault and no-claims')],
         key_points=[
          'Photograph <strong>before anything moves</strong>, and get a witness name.',
          '<strong>Say nothing about fault</strong>, at the scene or afterwards.',
          'Report it to your own insurer <strong>even if you will not claim through them</strong>.',
          'You are entitled to a <strong>like-for-like</strong> replacement car, and your excess '
          'back.',
         ]),
]
