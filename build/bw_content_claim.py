#!/usr/bin/env python3
"""Insurance cluster: how a claim actually runs, and no-claims."""

from bw_lib import page, CHOICE_NOTE, ADVICE_NOTE

PAGES = [

    page('how-a-bodywork-insurance-claim-works-step-by-step',
         'How a Bodywork Insurance Claim Works, Step by Step | KITH Cars',
         'Every stage of a motor bodywork claim from the phone call to collecting the car: '
         'notification, engineer, authorisation, strip-down, supplementary, repair and settlement.',
         'How a Bodywork Claim Works, Step by Step',
         'Insurance &amp; claims &middot; The process',
         'Nine stages, and the two that cause nearly all the delay are the ones nobody warns you '
         'about: the engineer&rsquo;s inspection and the supplementary after strip-down.',
         [
          ('The whole thing, in order', [
           ('steps', [
             '<strong>You notify your insurer.</strong> <span>Promptly, whatever you intend to '
             'do. Late notification is one of the few things that genuinely damages a '
             'claim.</span>',
             '<strong>You name your repairer.</strong> <span>Say it on this first call, before '
             'the car gets booked into their network and then has to be moved.</span>',
             '<strong>The car comes to us and we estimate it.</strong> <span>On the same '
             'industry systems insurers use, so the figures are directly comparable.</span>',
             '<strong>An engineer inspects.</strong> <span>Sometimes in person, increasingly from '
             'photographs. They are checking the damage matches the estimate and that the '
             'method and times are reasonable.</span>',
             '<strong>The insurer authorises.</strong> <span>Nothing is ordered or started before '
             'this. Chasing authorisation is most of what the first week consists of.</span>',
             '<strong>Parts ordered, car stripped.</strong> <span>The panel comes off and we see '
             'what the photographs could not.</span>',
             '<strong>Supplementary, if needed.</strong> <span>If strip-down finds more, we raise '
             'it and the engineer authorises it. This is the second pause.</span>',
             '<strong>Repair, paint, refit and check.</strong> <span>Including testing anything '
             'electrical that came out, and recalibrating sensors where the job needs it.</span>',
             '<strong>You pay the excess and collect.</strong> <span>The insurer settles their '
             'share with us directly.</span>',
           ]),
          ]),
          ('Where the time actually goes', [
           ('table', (['Stage', 'Typical', 'What slows it'], [
             ['Notification to estimate', '1&ndash;3 days', 'Getting the car to us'],
             ['Estimate to authorisation', '2&ndash;10 days', 'Engineer backlog, disputed times'],
             ['Parts', '1&ndash;10 days', 'Back orders on newer or rarer cars'],
             ['Repair and paint', '2&ndash;5 days', 'Curing time, which cannot be rushed'],
             ['Supplementary, if raised', '+2&ndash;7 days', 'A second authorisation round'],
           ])),
           'A straightforward bumper can be in and out inside a week. A multi-panel job with a '
           'supplementary and a part on back order can be a month, and almost none of that month '
           'is the car being worked on.',
          ]),
          ('The two bits nobody explains', [
           '<strong>The engineer is not inspecting the car for your benefit.</strong> They act '
           'for the insurer, and their job includes checking the repair method and labour times '
           'are reasonable. A good estimate written in the right format gets authorised faster, '
           'which is a large part of why it matters who writes it.',
           '<strong>Strip-down is where estimates change.</strong> No photograph shows a bent '
           'crash bar behind an intact bumper or a cracked mounting behind a straight panel. '
           'Finding more at strip-down is normal, not a sign anything went wrong &mdash; but it '
           'means a second authorisation round, and that is the pause people find frustrating '
           'because the car is already in pieces.',
          ]),
          ('What you can do to speed it up', [
           ['Report it the same day and name your repairer immediately.',
            'Send photographs of everything, including the bits that look undamaged.',
            'Get the authorised labour rate confirmed in writing at the start.',
            'Give us the claim number and the engineer&rsquo;s details so we can deal with them '
            'directly rather than through you.',
            'Chase authorisation yourself if it stalls. A call from the policyholder moves things '
            'that a call from the bodyshop does not.'],
           ('note', CHOICE_NOTE),
          ]),
         ],
         [('Do I pay anything up front?',
           'No. You pay the excess when you collect, and the insurer settles their share with us '
           'directly.'),
          ('Can I see the estimate?',
           'Yes, and you should. Ask us for a copy and ask the insurer for the engineer&rsquo;s '
           'assessment if it differs.'),
          ('What if the engineer cuts the estimate?',
           'Then we discuss it with them. Sometimes they are right and there is a cheaper method '
           'that is still correct. Sometimes they are working to a time that does not match the '
           'car in front of us, and we say so. We do not quietly absorb it by doing less work.'),
          ('Will you deal with the insurer so I do not have to?',
           'From the estimate onward, yes. The first notification has to come from you, because '
           'the policy is yours.')],
         [('non-fault-accident-what-to-do', 'Non-fault accident: what to do'),
          ('supplementary-estimate-explained', 'Supplementary estimates'),
          ('what-the-engineer-does', 'What the engineer does'),
          ('how-long-an-insurance-repair-takes', 'How long it takes')],
         key_points=[
          'Nine stages. <strong>Name your repairer on the first call.</strong>',
          'The delays are <strong>authorisation</strong> and <strong>the supplementary</strong>, '
          'not the repair.',
          'The engineer acts for <strong>the insurer</strong>, not for you.',
          'You pay the excess <strong>at collection</strong> &mdash; nothing up front.',
         ]),

    page('what-the-engineer-does',
         'What Does the Insurance Engineer Do? | KITH Cars',
         'Who the motor engineer works for, what they are actually checking, how photo '
         'assessments differ from in-person ones, and what to do when they cut the estimate.',
         'What the Insurance Engineer Actually Does',
         'Insurance &amp; claims &middot; The process',
         'They work for the insurer, not for you, and that is not a criticism &mdash; it is the '
         'single most useful thing to understand about the stage of the claim that decides what '
         'gets paid for.',
         [
          ('Who they are and who pays them', [
           'A motor engineer is a qualified assessor instructed by the insurer to look at the '
           'damage and the estimate and say whether the two match. Some are employed by the '
           'insurer, many work for assessment firms contracted to several.',
           'They are not an independent arbiter between you and the insurer, and they are not '
           'inspecting the car on your behalf. Their job is to make sure the insurer pays for '
           'the damage from this accident, repaired by a reasonable method, in a reasonable time.',
          ]),
          ('What they are actually checking', [
           ['<strong>Does the damage match the account?</strong> A rear-end shunt that has '
            'damaged a front wing raises a question.',
            '<strong>Is any of it pre-existing?</strong> Old damage on the same panel is '
            'excluded, and this is a common source of argument.',
            '<strong>Is the method right?</strong> Repair against replace, and whether a panel '
            'that could be straightened is being replaced instead.',
            '<strong>Are the labour times reasonable?</strong> Measured against published times '
            'for that operation on that vehicle.',
            '<strong>Is the parts grade appropriate?</strong> Genuine, matching-quality or '
            'recycled, and what the policy entitles you to.',
            '<strong>Is it economical to repair at all?</strong> This is where a write-off '
            'decision comes from.'],
          ]),
          ('Photo assessment versus in person', [
           'Most straightforward claims are now assessed from photographs, which is faster and '
           'works perfectly well for visible damage. It has one weakness, and it is the reason '
           'supplementaries exist: a photograph shows the face of a panel and nothing behind it.',
           'An in-person inspection is more likely on larger claims, on suspected structural '
           'damage, and where the estimate and the photographs seem to disagree. If you think '
           'yours needs seeing rather than photographing, you can ask &mdash; particularly where '
           'there is a reason to think the damage goes deeper than it looks.',
          ]),
          ('When they cut the estimate', [
           'It happens, and it is not automatically wrong. Sometimes there is a cheaper method '
           'that is genuinely correct, and a good bodyshop will accept that rather than argue for '
           'the sake of it.',
           'What should not happen is the difference being absorbed by doing less work &mdash; '
           'skipping the blend into the next panel, filling over something that needed replacing, '
           'or not recalibrating a sensor that came out. That is where a pre-agreed network rate '
           'and a squeezed labour time quietly turn into a visibly worse repair.',
           ('steps', [
             '<strong>Ask for the reduction in writing.</strong> <span>With the reason and the '
             'times they have applied.</span>',
             '<strong>We respond with evidence.</strong> <span>Photographs from strip-down, '
             'manufacturer method, published times.</span>',
             '<strong>If it is still wrong, you complain.</strong> <span>It is your claim and '
             'your policy. A complaint from the policyholder carries weight a bodyshop&rsquo;s '
             'does not.</span>',
           ]),
          ]),
         ],
         [('Can I get my own independent engineer?',
           'Yes. You pay for it, and on a disputed total loss or a significant structural '
           'disagreement it can be money well spent. On a bumper it is not.'),
          ('The engineer says some damage is pre-existing.',
           'Ask which, and ask what they based it on. Photographs from before the accident, '
           'service records or an MOT advisory history can settle it either way.'),
          ('How long does the engineer stage take?',
           'Anything from a day to a couple of weeks. Backlogs are the usual reason, and chasing '
           'as the policyholder genuinely helps.'),
          ('Do you deal with the engineer or do I?',
           'We do, from the estimate onward. You are better placed to chase authorisation when it '
           'stalls, because you are the customer and we are not.')],
         [('how-a-bodywork-insurance-claim-works-step-by-step', 'How a claim works'),
          ('supplementary-estimate-explained', 'Supplementary estimates'),
          ('insurer-approved-repairer-vs-independent-bodyshop', 'Approved vs independent'),
          ('write-off-valuation-too-low-what-to-do', 'Challenging a valuation')],
         key_points=[
          'They are instructed by <strong>the insurer</strong>, not by you.',
          'They check method, <strong>labour times</strong>, parts grade and whether it is '
          'economical to repair.',
          'Most claims are now assessed <strong>from photographs</strong>, which cannot show what '
          'is behind a panel.',
          'A cut estimate should change the <strong>price</strong>, never the amount of work '
          'done.',
         ]),

    page('supplementary-estimate-explained',
         'Supplementary Estimate Explained: Why the Price Changed | KITH Cars',
         'Why repair costs rise after strip-down, what a supplementary is, who authorises it, '
         'and why it is normal rather than a sign something went wrong.',
         'Supplementary Estimates: Why the Price Went Up',
         'Insurance &amp; claims &middot; The process',
         'Your car is in pieces and the price has changed. That is a supplementary, it is normal, '
         'and it happens because no photograph has ever shown what is behind a panel.',
         [
          ('What a supplementary is', [
           'A revised estimate raised after the original was authorised, covering damage that '
           'could not be seen until the car was stripped. It goes back to the engineer for a '
           'second authorisation before the extra work is done.',
           'It is not a bodyshop changing its mind or finding a way to charge more. The first '
           'estimate is written from what is visible with the panels on, and that is a genuine '
           'limit rather than a failure of effort.',
          ]),
          ('What turns up at strip-down', [
           ['A bent crash bar behind an apparently intact bumper.',
            'Broken mounting tabs and brackets, which hold the panel in line and are invisible '
            'from the front.',
            'Damaged sensor wiring and connectors, pulled rather than cut.',
            'Corrosion underneath the damaged area, which has to come out before any repair.',
            'Impact carried further than it looked &mdash; a door hit that moved the pillar, a '
            'rear shunt that reached the boot floor.',
            'Previous repairs nobody mentioned, including filler over something that should have '
            'been replaced.'],
           'That last one is more common than people expect on used cars, and it is nobody’s '
           'fault in the current claim. It still has to be dealt with before new paint goes on.',
          ]),
          ('How it runs', [
           ('steps', [
             '<strong>We photograph everything as it is found.</strong> <span>Before anything '
             'moves, with the damage visible and in context.</span>',
             '<strong>The supplementary is raised.</strong> <span>Itemised, with the photographs '
             'attached, on the same system as the original.</span>',
             '<strong>The engineer reviews it.</strong> <span>Sometimes a second inspection, '
             'more often from the photographs.</span>',
             '<strong>It is authorised, queried or reduced.</strong> <span>Queries are normal '
             'and usually settled in a call.</span>',
             '<strong>We tell you either way.</strong> <span>Including what it does to the '
             'timescale, which is usually the part that matters to you.</span>',
           ]),
          ]),
          ('Does it cost you more?', [
           'Normally not. Your excess is a fixed figure set by your policy and it does not rise '
           'because the repair did. The supplementary is between the bodyshop and the insurer.',
           'Where it can affect you is on a borderline claim: enough additional damage can tip a '
           'repair into a total loss, and then the conversation changes from repairing your car '
           'to valuing it.',
           ('note', ADVICE_NOTE),
          ]),
          ('Why it is worth insisting on', [
           'A supplementary is the mechanism that gets hidden damage paid for. The alternative is '
           'a repairer who absorbs it by not doing the work &mdash; refitting a bumper onto broken '
           'tabs, painting over corrosion, leaving a sensor untested.',
           'All of those look fine at handover. They show up months later, after the claim is '
           'closed and the paperwork says the car was repaired.',
          ]),
         ],
         [('Can the insurer refuse a supplementary?',
           'They can query or reduce it. A properly evidenced one with photographs taken at '
           'strip-down is hard to refuse outright, which is why we photograph everything before '
           'touching it.'),
          ('How much does it delay things?',
           'Usually two to seven days for the second authorisation. The car sits stripped during '
           'that, which is the frustrating part.'),
          ('Will I be told before the work is done?',
           'Yes. We tell you what was found, what it means for the timescale, and whether it '
           'changes anything for you.'),
          ('What if I am paying privately rather than claiming?',
           'Same principle, simpler process. We stop, show you what we found, and agree the '
           'revised figure with you before carrying on. We do not do extra work and present the '
           'bill afterwards.')],
         [('how-a-bodywork-insurance-claim-works-step-by-step', 'How a claim works'),
          ('what-the-engineer-does', 'What the engineer does'),
          ('how-long-an-insurance-repair-takes', 'How long it takes'),
          ('is-my-car-worth-repairing-or-writing-off', 'Repair or write off?')],
         key_points=[
          'A <strong>revised estimate</strong> for damage only visible once the panel came off.',
          'Normal, not a sign anything went wrong.',
          'Your <strong>excess does not rise</strong> because the repair did.',
          'Enough extra damage can <strong>tip a repair into a write-off</strong>.',
         ]),

    page('will-a-non-fault-claim-affect-my-no-claims',
         'Will a Non-Fault Claim Affect My No-Claims Discount? | KITH Cars',
         'What happens to your no-claims bonus after an accident that was not your fault, why '
         'your premium can still rise, and what to ask your insurer.',
         'Will a Non-Fault Claim Affect My No-Claims?',
         'Insurance &amp; claims &middot; No-claims',
         'If your insurer recovers everything from the other side, your discount should survive '
         'intact. Your premium can still go up, and those two facts confuse almost everybody.',
         [
          ('Discount and premium are different things', [
           'Your no-claims discount is a percentage off. Your premium is the number it comes off. '
           'Keeping the discount while the underlying premium rises leaves you paying more, and '
           'that is exactly what happens after a non-fault claim.',
           'Insurers price on claim frequency as well as fault. Statistically, a driver who has '
           'been involved in one accident is more likely to be involved in another, whoever '
           'caused it. Whether that feels fair is a separate question from whether it is what '
           'happens.',
          ]),
          ('The bit that actually decides it', [
           'What matters is whether your insurer gets its money back from the at-fault '
           'driver&rsquo;s insurer. Until it does, the claim sits on your record as an outlay '
           'they have not recovered.',
           ('table', (['Outcome', 'Effect on your discount'], [
             ['Fully recovered from the third party', 'Should be unaffected'],
             ['Partly recovered, split liability', 'Usually reduced proportionally'],
             ['Not recovered &mdash; untraced or uninsured driver',
              'Often treated as a fault claim'],
             ['Still open at your renewal', 'Treated as unrecovered until it settles'],
           ])),
           'That last row catches people every year. If the claim has not settled by renewal, you '
           'can be quoted as though it were a fault claim. Ask for it to be reviewed once it '
           'settles, and ask for the premium to be adjusted retrospectively.',
          ]),
          ('What to ask, and when', [
           ('steps', [
             '<strong>At the start:</strong> <span>&ldquo;Will this be recorded as non-fault, and '
             'will you be recovering from the third party?&rdquo;</span>',
             '<strong>At three months:</strong> <span>&ldquo;Has liability been settled? Has my '
             'excess been returned?&rdquo;</span>',
             '<strong>At renewal:</strong> <span>&ldquo;Is this claim showing as settled in my '
             'favour? If not, why not?&rdquo;</span>',
             '<strong>After settlement:</strong> <span>&ldquo;Please review my premium now the '
             'claim has settled and refund any difference.&rdquo;</span>',
           ]),
          ]),
          ('Where it goes wrong', [
           ['The claim settles and nobody updates your record. Ask for written confirmation.',
            'You move insurer mid-claim and the new one prices it as unresolved.',
            'The other driver was uninsured, so there is nobody to recover from.',
            'Liability is split, and so is the recovery.'],
          ]),
         ],
         [('Should I claim through the other driver’s insurer instead?',
           'It avoids your excess and keeps the claim off your own policy, which can help. You '
           'give up the protection of your own insurer if it turns awkward, and you negotiate '
           'alone. On a clear-cut claim with liability admitted it is worth considering.'),
          ('Does protected no-claims cover a non-fault claim?',
           'It protects the discount, yes. It does not stop the underlying premium rising, which '
           'is the part people are actually annoyed about.'),
          ('How long does a claim stay on my record?',
           'You will generally be asked to declare claims for around five years, and most '
           'insurers price on the last five.'),
          ('My premium went up despite non-fault. Can I argue?',
           'You can ask for an explanation and you should. If the claim is settled in your favour '
           'and still being priced as unresolved, that is a straightforward correction.')],
         [('non-fault-accident-what-to-do', 'Non-fault accident: what to do'),
          ('protected-no-claims-explained', 'Protected no-claims'),
          ('should-i-claim-or-pay-myself', 'Claim or pay yourself?'),
          ('recovering-your-excess-after-a-non-fault-accident', 'Recovering your excess')],
         key_points=[
          '<strong>Discount and premium are different.</strong> You can keep one and still pay '
          'more.',
          'What decides it: whether your insurer <strong>recovers from the other side</strong>.',
          'A claim <strong>still open at renewal</strong> is priced as if it were your fault.',
          'Ask for a <strong>retrospective review</strong> once it settles.',
         ]),

    page('third-party-capture-insurer-calling-you',
         "Third Party Capture: The Other Driver's Insurer Called Me | KITH Cars",
         'Why the at-fault driver\'s insurer rings you directly after an accident, what they are '
         'offering, what you give up by accepting, and how to handle the call.',
         "The Other Driver's Insurer Called Me Directly",
         'Insurance &amp; claims &middot; Fault and liability',
         'It is called third party capture, it is legal, and it is not done for your benefit. '
         'They are trying to control the cost of a claim they expect to pay, and the cheapest way '
         'to do that is to handle it before you involve anyone else.',
         [
          ('What is actually happening', [
           'The at-fault driver has reported the accident to their own insurer. That insurer can '
           'see they are likely to pay, and they know the bill is lower if they handle it '
           'directly than if you go through your own insurer and a credit hire company.',
           'So they ring you, often within a day, sound helpful, and offer to sort the repair and '
           'a car. All of which may be perfectly fine. It is simply worth knowing whose interests '
           'the call serves.',
          ]),
          ('What you keep either way', [
           ['<strong>Your choice of repairer.</strong> Accepting their help does not oblige you '
            'to use their bodyshop.',
            '<strong>A like-for-like replacement vehicle.</strong> Not whatever is cheapest on '
            'their list.',
            '<strong>Your out-of-pocket costs.</strong> Recovery, storage, loss of earnings.',
            '<strong>The right to involve your own insurer instead.</strong> At any point.'],
          ]),
          ('What to say on the call', [
           ('steps', [
             '<strong>Take their details rather than giving yours.</strong> <span>Company, claim '
             'reference, name, direct number. Then say you will come back to them.</span>',
             '<strong>Do not discuss how the accident happened.</strong> <span>Not in detail, and '
             'not on a recorded line, before liability is settled.</span>',
             '<strong>Do not accept any offer on the first call.</strong> <span>Particularly not '
             'a cash settlement figure, which is usually below the real repair cost.</span>',
             '<strong>Tell your own insurer it happened.</strong> <span>Even if you end up going '
             'direct. They need to know.</span>',
             '<strong>Get a real repair figure first.</strong> <span>Then you can judge whether '
             'what they are offering covers it.</span>',
           ]),
          ]),
          ('The cash offer', [
           'A common move is an offer to settle in cash rather than repair the car. It can be '
           'genuinely convenient, particularly on an older car you are happy to live with as it '
           'is.',
           'The catch is that the figure is usually built from their assessment rather than a '
           'real quote, and once you accept it the claim is closed. If the damage turns out to be '
           'worse than it looked &mdash; which is what strip-down is for &mdash; that is now your '
           'problem.',
           ('note', 'Get the car estimated properly before accepting any cash figure. If the '
                    'offer covers it, take it with confidence. If it does not, you now have a '
                    'document that says so.'),
          ]),
         ],
         [('Do I have to speak to them at all?',
           'No. You can decline and tell them to deal with your insurer. That is often the '
           'simplest answer if you find the call uncomfortable.'),
          ('They said using my own insurer will cost me my excess. True?',
           'Usually true in the short term, and recoverable once liability settles. It is a fair '
           'point rather than a trick &mdash; but it is being made because it suits them.'),
          ('Is it a scam?',
           'No, it is a recognised and lawful practice. The thing to be alert to is pressure to '
           'decide quickly, and any suggestion you do not have a choice of repairer.'),
          ('Can I use you if I go through them?',
           'Yes. The choice of repairer is yours whoever is paying, and we deal with any insurer.')],
         [('non-fault-accident-what-to-do', 'Non-fault accident: what to do'),
          ('am-i-entitled-to-a-courtesy-car', 'Courtesy car entitlement'),
          ('credit-hire-explained', 'Credit hire explained'),
          ('right-to-choose-your-own-bodyshop', 'Your right to choose')],
         key_points=[
          'Legal, common, and <strong>not done for your benefit</strong>.',
          'You keep your <strong>choice of repairer</strong> and your right to a like-for-like '
          'car.',
          '<strong>Never accept a cash offer</strong> before the car has been properly estimated.',
          'Tell your own insurer it happened, <strong>even if you go direct</strong>.',
         ]),
]
