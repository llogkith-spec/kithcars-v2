#!/usr/bin/env python3
"""Insurance cluster, part 3: excess, and replacement vehicles."""

from bw_lib import page, CHOICE_NOTE

PAGES = [

    page('recovering-your-excess-after-a-non-fault-accident',
         "Recovering Your Excess After a Non-Fault Accident | KITH Cars",
         'How to get your excess back when the accident was not your fault, how long it takes, '
         'and why it is the single most commonly forgotten money in motor claims.',
         'Recovering Your Excess After a Non-Fault Accident',
         'Insurance &amp; claims &middot; Excess',
         'It is yours to get back and almost nobody chases it. Excess recovery is the quietest '
         'leak in motor claims &mdash; paid out at the start, forgotten by the time liability '
         'settles six months later.',
         [
          ('Why you paid it at all', [
           'Your own insurer settles the repair first and argues about who pays later. That is '
           'the point of the cover: you get your car fixed now rather than waiting for two '
           'insurers to finish disagreeing. The excess is your contribution under your own '
           'policy, and it applies whoever caused the accident.',
           'Once liability is settled against the other driver, their insurer reimburses yours '
           'for everything &mdash; the repair, the hire car, the recovery, and your excess. That '
           'last part is supposed to come back to you.',
          ]),
          ('How to actually get it back', [
           ('steps', [
             '<strong>Say it at the first call.</strong> <span>&ldquo;I want my excess recovered '
             'from the third party. Please record that on the claim.&rdquo;</span>',
             '<strong>Keep the proof.</strong> <span>The receipt or the bank entry showing what '
             'you paid and when.</span>',
             '<strong>Diarise it for three months.</strong> <span>Put a reminder in your phone '
             'now. This is the step everyone skips and it is the reason the money goes '
             'missing.</span>',
             '<strong>Chase in writing.</strong> <span>&ldquo;Please confirm the status of my '
             'claim and when my excess will be refunded.&rdquo; Email, so there is a record.</span>',
             '<strong>Escalate if it stalls.</strong> <span>A formal complaint, then the '
             'Financial Ombudsman Service if the final response is unreasonable. Both are '
             'free.</span>',
           ]),
          ]),
          ('What the timeline actually looks like', [
           ('table', (['Stage', 'Typical timing'], [
             ['You pay the excess', 'At collection'],
             ['Liability admitted or disputed', 'Weeks to months'],
             ['Insurers settle between themselves', 'Months'],
             ['Excess refunded to you', 'After settlement &mdash; only if chased'],
           ])),
           'If liability is admitted early the whole thing can run in a couple of months. If it '
           'is disputed, or there is injury involved, it can take considerably longer, and that '
           'is the gap in which people forget the money exists.',
          ]),
          ('When you should not have paid it at all', [
           'If the other driver admitted fault immediately and their insurer accepted liability '
           'at the outset, ask your own insurer to waive the excess rather than collect and '
           'refund it. Some will. It is always worth the question, and the answer costs you one '
           'phone call.',
           'The other route is claiming directly against the at-fault insurer rather than your '
           'own. There is no excess that way because it is not your policy paying. The trade is '
           'that you give up the protection of your own insurer if the claim turns awkward, and '
           'you are negotiating on your own.',
           ('note', CHOICE_NOTE),
          ]),
         ],
         [('How long do I have to claim it back?',
           'There is no separate deadline for the excess &mdash; it travels with the claim. What '
           'matters is that the claim itself is settled and that you have told them you want it '
           'back. Chase at three months, not at twelve.'),
          ('They have refunded the repair but not my excess.',
           'That happens, and it is usually an oversight rather than a refusal. Email, quote the '
           'claim number, state the amount and the date you paid it, and ask for a payment date.'),
          ('Can I claim the excess from the other driver directly?',
           'You can, if their insurer has accepted liability and your own insurer is not already '
           'pursuing it. Doing both at once causes confusion, so tell your insurer which route '
           'you are taking.'),
          ('What if liability is split?',
           'Then recovery is usually split the same way. On a 50/50 you would typically get half '
           'your excess back, which is worth knowing before you expect the full amount.')],
         [('who-pays-my-excess', 'Who pays my excess'),
          ('non-fault-accident-what-to-do', 'Non-fault accident: what to do'),
          ('split-liability-explained', 'Split liability explained'),
          ('third-party-capture-insurer-calling-you', 'Third party capture')],
         key_points=[
          'It comes back to you <strong>only if you chase it</strong>.',
          'Say you want it recovered on the <strong>first call</strong>, and keep the receipt.',
          'Expect <strong>months</strong>, not weeks &mdash; it arrives when liability settles.',
          'On a <strong>50/50</strong> split you usually get half back, not all of it.',
         ]),

    page('compulsory-vs-voluntary-excess',
         'Compulsory vs Voluntary Excess: What is the Difference? | KITH Cars',
         'The two halves of your excess, who sets each one, how they add together on a claim, '
         'and how to pick a voluntary excess that does not backfire.',
         'Compulsory vs Voluntary Excess',
         'Insurance &amp; claims &middot; Excess',
         'Your excess is two numbers added together, and people routinely forget the second one '
         'until they claim. The one you chose to save money is usually the bigger of the two.',
         [
          ('The two halves', [
           ('table', (['', 'Compulsory', 'Voluntary'], [
             ['Who sets it', 'The insurer', 'You'],
             ['Why', 'Your car, age, licence and claims history',
              'To bring the premium down'],
             ['Can you change it', 'No', 'At renewal'],
             ['Payable on a claim', 'Yes', 'Yes'],
           ])),
           'Both are payable, and they stack. A £250 compulsory with a £500 voluntary means £750 '
           'out of your pocket before the insurer contributes anything.',
          ]),
          ('The trap with a high voluntary excess', [
           'Raising your voluntary excess lowers your premium, which feels like free money at '
           'renewal. It is a bet: you are wagering that you will not claim, and the stake is the '
           'difference.',
           'The arithmetic that catches people is that most bodywork claims are small. A bumper, '
           'a door, a wing &mdash; these are frequently in the hundreds rather than the '
           'thousands. Set a voluntary excess of £500 and you have effectively uninsured yourself '
           'against the most common damage there is, while still paying for cover against the '
           'rare expensive sort.',
          ]),
          ('Picking a sensible figure', [
           ['Work out what you could pay tomorrow without it being a problem. That is your '
            'ceiling.',
            'Compare the premium saving against the extra excess. Saving £40 a year to add £250 '
            'of excess takes six years to break even, and only if you never claim.',
            'Remember the compulsory figure sits underneath it. Ask what it is before you choose '
            'the voluntary one &mdash; it is often not on the summary page.',
            'If you drive somewhere your car gets knocked regularly, a low excess earns its keep.'],
          ]),
          ('Where it actually matters', [
           'It is not the big crash that tests your excess choice, because at that point you are '
           'claiming regardless. It is the £400 bumper. With a £150 total excess you claim '
           'without thinking; with a £750 total excess you pay for it yourself, and the question '
           'becomes whether the premium you saved covered it.',
           'That is also the honest case for getting a direct price before you call your insurer '
           'at all. We will tell you the figure, and then the comparison is a real one rather '
           'than a guess.',
          ]),
         ],
         [('Does the voluntary excess apply to every claim?',
           'Usually yes on accidental damage. Windscreen claims almost always carry a separate '
           'and lower glass excess instead, so check that section specifically.'),
          ('Can I lower my voluntary excess mid-policy?',
           'Not normally &mdash; it is set for the policy term. You change it at renewal.'),
          ('Is a £0 voluntary excess ever worth it?',
           'Occasionally, on a cheap-to-insure car where the premium barely moves. Mostly the '
           'premium difference is small enough that the middle ground is better value.'),
          ('Do I pay both halves even on a non-fault claim?',
           'Yes, and then you recover the lot once liability settles &mdash; if you chase it.')],
         [('who-pays-my-excess', 'Who pays my excess'),
          ('should-i-claim-or-pay-myself', 'Claim or pay yourself?'),
          ('excess-protection-cover-worth-it', 'Is excess protection worth it?'),
          ('recovering-your-excess-after-a-non-fault-accident', 'Recovering your excess')],
         key_points=[
          'Your excess is <strong>two numbers added together</strong>, and both are payable.',
          'The voluntary half is the one <strong>you chose</strong>, and usually the bigger one.',
          'A high voluntary excess <strong>uninsures you against small bodywork</strong>, which '
          'is most bodywork.',
          'Glass claims normally carry a <strong>separate, lower</strong> excess.',
         ]),

    page('should-i-claim-or-pay-myself',
         'Should I Claim on Insurance or Pay for the Repair Myself? | KITH Cars',
         'How to work out whether a bodywork repair is worth claiming for: excess, no-claims, '
         'premium effect and the five-year declaration. With the actual arithmetic.',
         'Should I Claim, or Pay for It Myself?',
         'Insurance &amp; claims &middot; Deciding',
         'The honest answer is that most single-panel bodywork is not worth claiming for, and '
         'the sum that proves it takes about two minutes.',
         [
          ('The arithmetic', [
           'Four numbers decide it, and only the first is obvious.',
           ('steps', [
             '<strong>The repair cost.</strong> <span>Get a real figure, not a guess. Put your '
             'registration in the box on this page.</span>',
             '<strong>Your total excess.</strong> <span>Compulsory plus voluntary. Both.</span>',
             '<strong>What the claim does to your renewal.</strong> <span>Lost no-claims '
             'discount plus the loading for having claimed, across several years.</span>',
             '<strong>The declaration period.</strong> <span>You declare the claim for around '
             'five years, and it affects quotes for all of them.</span>',
           ]),
           'If the repair is less than the excess, there is nothing to decide. If it is a little '
           'more, it is still usually cheaper to pay &mdash; because the third and fourth numbers '
           'are the ones that keep costing.',
          ]),
          ('Worked through', [
           'Take a £420 bumper repair against a £400 total excess. Claiming nets you £20 toward '
           'it. In exchange you lose part of your no-claims discount, your renewal rises, and you '
           'declare the claim for five years.',
           'Now take a £3,000 repair against the same excess. Claiming is obvious and nobody '
           'needs a table to see it.',
           'The grey zone is roughly one to three times your excess, and the answer there depends '
           'on how much no-claims you have built up. Several years of discount is worth real '
           'money and worth protecting over a small claim.',
          ]),
          ('When to claim regardless', [
           ['Anyone was injured. Always report and always claim.',
            'Another vehicle or property was damaged. Their claim against you exists whether you '
            'claim or not.',
            'The damage might be structural. What looks like a bumper can be a crash bar and a '
            'chassis leg.',
            'Several panels, as with vandalism or hail. The total climbs past the excess faster '
            'than people expect.'],
          ]),
          ('The thing people get wrong', [
           'Deciding not to claim is not the same as not telling your insurer. Most policies '
           'require you to notify <em>any</em> incident, even one you pay for yourself. Not '
           'notifying is what causes problems at the next renewal or the next claim &mdash; not '
           'the damage.',
           'Notify, say clearly that you are not claiming and are paying privately, and ask them '
           'to record it as notification only.',
           ('note', CHOICE_NOTE),
          ]),
         ],
         [('Will notifying without claiming affect my premium?',
           'It can show as a notified incident, and some insurers price for it. It is still the '
           'right thing to do, because non-disclosure is a far bigger problem than a notified '
           'non-claim.'),
          ('How much is my no-claims discount actually worth?',
           'Several years of it is typically a substantial share of the premium. Your renewal '
           'notice shows the discount applied &mdash; that figure is what you are risking.'),
          ('Can I claim and then change my mind?',
           'Sometimes, if nothing has been paid out. Once the insurer has incurred cost, '
           'withdrawing usually means repaying it. Decide before you open the claim.'),
          ('Do you charge differently depending on which way I go?',
           'No. The price is the price. We are on no insurer panel, so we have no reason to push '
           'you toward a claim or away from one.')],
         [('who-pays-my-excess', 'Who pays my excess'),
          ('compulsory-vs-voluntary-excess', 'Compulsory vs voluntary excess'),
          ('will-a-non-fault-claim-affect-my-no-claims', 'Claims and your no-claims'),
          ('paying-for-bodywork-yourself-vs-claiming', 'Paying privately')],
         key_points=[
          'Under your excess? <strong>Nothing to decide.</strong>',
          'Between one and three times your excess is the <strong>grey zone</strong>, and '
          'no-claims usually tips it.',
          'You declare a claim for about <strong>five years</strong>, not one.',
          '<strong>Notify even when you do not claim</strong> &mdash; non-disclosure is the '
          'bigger risk.',
         ]),

    page('am-i-entitled-to-a-courtesy-car',
         'Am I Entitled to a Courtesy Car? | KITH Cars',
         'When a courtesy car is included, when it is not, and what you are actually entitled to '
         'after a non-fault accident — which is more than a small hatchback.',
         'Am I Entitled to a Courtesy Car?',
         'Insurance &amp; claims &middot; Replacement vehicles',
         'It depends entirely on whose fault it was, and the two answers are very different. On '
         'a non-fault claim you are entitled to a like-for-like replacement, not whatever is '
         'spare.',
         [
          ('The two situations', [
           ('table', (['', 'Your fault', 'Not your fault'], [
             ['Where the car comes from', 'Your policy, if it includes one',
              'The at-fault driver&rsquo;s insurer'],
             ['What you get', 'Usually a small hatchback',
              'Like-for-like with your own car'],
             ['How long', 'While yours is being repaired',
              'While yours is off the road'],
             ['Who pays', 'Included in your premium', 'The at-fault insurer'],
             ['If your policy has no courtesy car', 'Nothing', 'Still entitled'],
           ])),
           'That bottom row is the one worth knowing. A courtesy car on your own policy is an '
           'optional extra. A replacement after someone else hits you is a loss they caused, and '
           'it does not depend on what you bought.',
          ]),
          ('What like-for-like actually means', [
           'If you drive a seven-seater because you have five children, a three-door hatchback is '
           'not a replacement. If you drive an estate for work, neither is a city car. '
           'Like-for-like means a vehicle that does the job yours was doing.',
           'Insurers do not always offer that first. Say what you actually need and why &mdash; '
           'seats, load space, towing, an automatic if you can only drive one &mdash; and say it '
           'at the start rather than after you have accepted something unsuitable.',
          ]),
          ('Where it goes wrong', [
           ['<strong>Accepting the first offer.</strong> It is usually the cheapest vehicle, not '
            'the right one.',
            '<strong>Not asking because your policy has no courtesy car.</strong> On a non-fault '
            'claim that is irrelevant.',
            '<strong>Signing a credit hire agreement without reading it.</strong> Legitimate, '
            'but you are the one who signs for the cost if recovery fails.',
            '<strong>Keeping it longer than the repair.</strong> Entitlement runs while your car '
            'is genuinely off the road, not afterwards.'],
          ]),
          ('If you are using your own repairer', [
           'Some policies tie the courtesy car to the insurer&rsquo;s own network, so choosing '
           'your own bodyshop can mean losing it on a fault claim. Ask before you book the car '
           'in, because it is the one consequence of choosing your own garage that genuinely '
           'inconveniences people.',
           'On a non-fault claim it does not arise, because the replacement comes from the other '
           'side rather than from your policy.',
           ('note', CHOICE_NOTE),
          ]),
         ],
         [('My policy does not include a courtesy car. Am I stuck?',
           'On a fault claim, largely yes &mdash; though some repairers have their own. On a '
           'non-fault claim, no: the entitlement comes from the other driver having caused your '
           'loss, not from your policy.'),
          ('How long can I keep it?',
           'While your car is genuinely off the road. If the repair is delayed waiting for parts '
           'that is still covered; if you simply have not collected your car, it is not.'),
          ('Who insures the courtesy car?',
           'Usually the provider, but check what you are signing. Confirm the cover and the '
           'excess on the replacement before you drive it away.'),
          ('Is credit hire a trap?',
           'Not inherently &mdash; it exists so non-fault drivers get a proper replacement '
           'without paying up front. The thing to understand is that you are the hirer, and if '
           'the costs are not recovered from the at-fault insurer you can be liable. Read it, '
           'and ask what happens if liability is disputed.')],
         [('courtesy-car-vs-credit-hire', 'Courtesy car vs credit hire'),
          ('credit-hire-explained', 'Credit hire explained'),
          ('non-fault-accident-what-to-do', 'Non-fault accident: what to do'),
          ('what-happens-if-i-use-a-non-approved-garage', 'Using your own garage')],
         key_points=[
          'Fault claim: <strong>only if your policy includes one</strong>.',
          'Non-fault: <strong>entitled regardless</strong> of what your policy includes.',
          'Like-for-like means <strong>a car that does your car&rsquo;s job</strong>, not '
          'whatever is spare.',
          'Choosing your own repairer can cost you the courtesy car on a <strong>fault</strong> '
          'claim. Ask first.',
         ]),
]
