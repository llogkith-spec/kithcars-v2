#!/usr/bin/env python3
"""The pages the rest of the set links to.

Every page here exists because another page promised it. A link to a page that does not exist is
a 404 in the crawl and a dead end for a reader, so the build fails on one - these close the set.

Two pairs were merged rather than written separately, because they would have been the same page
twice: "how long does an insurance repair take" folded into how-long-does-bodywork-take, and
"courtesy car vs credit hire" into credit-hire-explained.
"""

from bw_lib import page, HUB_PROCESS, CHOICE_NOTE, ADVICE_NOTE

PAGES = [

    page('is-my-car-worth-repairing-or-writing-off',
         'Is My Car Worth Repairing or Writing Off? | KITH Cars',
         'How to decide whether to repair a badly damaged car or take the settlement, with the '
         'sum that actually matters and the costs people forget.',
         'Repair It, or Let Them Write It Off?',
         'Insurance &amp; claims &middot; Deciding',
         'The insurer does this sum on their numbers. You should do it on yours, because the two '
         'are not the same and your answer is allowed to be different.',
         [
          ('The insurer&rsquo;s sum and yours', [
           'Theirs is simple: if repairing costs more than the car is worth less what the salvage '
           'fetches, write it off. They are comparing a repair bill against a market value.',
           'Yours is different, because replacing the car is not free and the thing you own is '
           'not an average. Your sum is: what you keep after retaining the salvage, minus the '
           'repair, against what it would cost to buy something equivalent.',
           ('steps', [
             '<strong>Get the settlement figure.</strong> <span>And challenge it first if it '
             'looks low &mdash; everything downstream depends on it.</span>',
             '<strong>Get the retention figure.</strong> <span>What you would be paid if you '
             'keep the car.</span>',
             '<strong>Get a real repair quote.</strong> <span>From us, on the actual car, not a '
             'guess from a photograph.</span>',
             '<strong>Price a replacement.</strong> <span>Four or five real adverts for '
             'something equivalent, today.</span>',
             '<strong>Compare.</strong> <span>Retention minus repair against settlement minus '
             'replacement cost.</span>',
           ]),
          ]),
          ('What tips it toward repairing', [
           ['You know the car. Full history, you have owned it years, nothing hidden.',
            'The spec is hard to replace &mdash; a manual in a sea of autos, a towbar, an '
            'unusual trim.',
            'You are keeping it for years, so the recorded category never actually costs you.',
            'The damage is cosmetic on a mechanically sound car.',
            'Replacing it means buying somebody else&rsquo;s unknown problem.'],
          ]),
          ('What tips it toward taking the money', [
           ['It is a Category S and you have no confidence in who would do the structural work.',
            'You were going to change the car within a year or two anyway.',
            'The repair quote lands close to the settlement &mdash; a lot of work to stand still.',
            'You need a car now, and retention plus repair takes weeks.',
            'You cannot get an insurance quote on it afterwards at a sensible price.'],
          ]),
          ('The costs people forget', [
           ('table', (['Forgotten cost', 'Which way it points'], [
             ['The value hit when you later sell', 'Against repairing'],
             ['Insuring a recorded write-off', 'Against repairing'],
             ['Buying costs on a replacement &mdash; the dealer margin you pay',
              'Against taking the money'],
             ['The unknown history of a replacement', 'Against taking the money'],
             ['Time without a car', 'Against repairing'],
           ])),
           ('note', ADVICE_NOTE),
          ]),
         ],
         [('Can you tell me which to do?',
           'We can give you the one number you are missing &mdash; what the repair actually '
           'costs, properly estimated. The decision is yours, and we have no stake in it either '
           'way because we are on no insurer panel.'),
          ('What if I repair it and find more damage?',
           'That is the real risk of retention, and it is why the quote should follow a proper '
           'look rather than photographs. We will tell you which parts of the estimate are '
           'uncertain and why.'),
          ('Will it ever be worth what it was?',
           'No. A recorded category is permanent and it costs value for the life of the car. '
           'Keeping it only makes sense if you are getting use rather than resale out of it.'),
          ('Can I challenge the write-off itself rather than the value?',
           'Yes, if you think the repair costs less than they assumed. A proper estimate that '
           'comes in under their figure is the document that does it.')],
         [('write-off-valuation-too-low-what-to-do', 'Challenging a low valuation'),
          ('can-i-keep-my-written-off-car', 'Keeping a written-off car'),
          ('car-write-off-categories-explained', 'All four categories'),
          ('selling-a-cat-s-or-cat-n-car', 'Selling a Cat S or N car')],
         key_points=[
          'Their sum compares <strong>repair against market value</strong>. Yours should compare '
          'it against <strong>replacement</strong>.',
          'Challenge the <strong>valuation first</strong> &mdash; everything else depends on it.',
          'Keeping it works if you keep it <strong>for years</strong>.',
          'Get an <strong>insurance quote before</strong> you commit to retention.',
         ]),

    page('credit-hire-explained',
         'Credit Hire Explained: The Replacement Car After a Non-Fault Accident | KITH Cars',
         'What credit hire is, how it differs from a courtesy car, what you are signing, and the '
         'one question to ask before you agree to it.',
         'Credit Hire, and What You Are Signing',
         'Insurance &amp; claims &middot; Replacement vehicles',
         'Credit hire gets you a proper replacement car with nothing to pay up front, and the '
         'cost is recovered from the at-fault insurer. It is legitimate. It is also a hire '
         'agreement in your name, and that is the part worth understanding.',
         [
          ('Credit hire against a courtesy car', [
           ('table', (['', 'Courtesy car', 'Credit hire'], [
             ['Where it comes from', 'Your policy or the repairer',
              'A hire company, arranged after a non-fault accident'],
             ['What you get', 'Usually a small hatchback', 'Like-for-like with your own car'],
             ['Who the contract is with', 'Nobody &mdash; it is a benefit',
              'You. You are the hirer.'],
             ['Who pays', 'Included', 'The at-fault insurer, on recovery'],
             ['If recovery fails', 'Not applicable', 'You can be liable for the charges'],
           ])),
           'That last row is the whole thing. A courtesy car is given to you; credit hire is '
           'lent to you against an expectation that someone else will pay. Usually they do.',
          ]),
          ('Why it exists', [
           'Before credit hire, a non-fault driver either paid for a hire car themselves and '
           'tried to recover it later, or went without. Neither is reasonable when someone else '
           'caused the damage.',
           'Credit hire fixed that by letting a company supply the car and pursue the at-fault '
           'insurer directly. The driver gets a proper replacement immediately and pays nothing. '
           'The model works, and it is well established in law.',
          ]),
          ('What to check before you sign', [
           ('steps', [
             '<strong>Ask what happens if liability is disputed.</strong> <span>This is the one '
             'question. Get the answer before you sign, not after.</span>',
             '<strong>Check the daily rate and the expected duration.</strong> <span>Credit hire '
             'rates are higher than ordinary hire, which is normal, but you should know the '
             'numbers.</span>',
             '<strong>Confirm the car is genuinely like-for-like.</strong> <span>You are entitled '
             'to a replacement that does your car&rsquo;s job.</span>',
             '<strong>Check the insurance and the excess on it.</strong> <span>You are driving '
             'somebody else&rsquo;s car on somebody else&rsquo;s policy.</span>',
             '<strong>Give it back when your car is ready.</strong> <span>Entitlement runs while '
             'yours is off the road, not afterwards.</span>',
           ]),
          ]),
          ('When to be careful', [
           'Credit hire is not a problem when liability is clear. It gets complicated when it is '
           'not, and the two situations that cause trouble are these: liability turns out to be '
           'split, so only part of the hire is recovered; or the at-fault insurer disputes the '
           'rate or the duration as unreasonable.',
           'In both cases there can be a balance, and the agreement you signed says who carries '
           'it. If liability is genuinely contested, a courtesy car through your own policy is '
           'the quieter option even if it is a smaller car.',
           ('note', CHOICE_NOTE),
          ]),
         ],
         [('Do I have to use the hire company the insurer suggests?',
           'No, and the same goes for the repairer. Both are your choice.'),
          ('Can I refuse credit hire and just claim the cost back?',
           'Yes. Hire a car yourself, keep the invoice, and claim it as part of your losses. You '
           'pay up front, which is exactly the problem credit hire was invented to solve.'),
          ('How long can I keep it?',
           'While your car is genuinely off the road. If a repair is delayed waiting for parts, '
           'that is covered. If you simply have not collected your car, it is not.'),
          ('Is it true credit hire pushes up everyone’s premiums?',
           'It is an argument insurers make, and there is something in it. It is also the '
           'mechanism that gets a non-fault driver a proper car without paying for someone '
           'else’s mistake. Both things can be true.')],
         [('am-i-entitled-to-a-courtesy-car', 'Courtesy car entitlement'),
          ('non-fault-accident-what-to-do', 'Non-fault accident: what to do'),
          ('third-party-capture-insurer-calling-you', 'Third party capture'),
          ('split-liability-explained', 'Split liability explained')],
         key_points=[
          'A proper like-for-like car with <strong>nothing to pay up front</strong>.',
          'The agreement is <strong>in your name</strong> &mdash; you are the hirer.',
          'Ask one question before signing: <strong>what happens if liability is '
          'disputed?</strong>',
          'If liability is genuinely contested, a <strong>courtesy car is quieter</strong>.',
         ]),

    page('how-long-does-bodywork-take',
         'How Long Does Bodywork Take? | Realistic Timescales | KITH Cars',
         'Honest timescales for body repairs by job, why curing cannot be rushed, and what '
         'actually causes the delays on an insurance job.',
         'How Long Will My Car Be Off the Road?',
         'The repair process &middot; Timescales',
         'Most of the time a car spends in a bodyshop, nobody is touching it. Paint has to cure, '
         'and on a claim an engineer has to authorise. Neither can be hurried, and both are why '
         'a day of work takes a week.',
         [
          ('By job', [
           ('table', (['Job', 'Typical', 'Why'], [
             ['Light scuff, polished out', 'Same day', 'No paint, no curing'],
             ['Localised repair, one panel', '1&ndash;2 days', 'Paint and bake'],
             ['One panel off, painted, refitted', '2&ndash;3 days', 'Strip, cure, polish, refit'],
             ['Two or three panels', '3&ndash;5 days', 'More paint, more blending'],
             ['Panel replacement', '3&ndash;5 days', 'Plus parts lead time'],
             ['Structural repair', '1&ndash;2 weeks', 'Measuring, welding, corrosion protection'],
           ])),
           'Those are working days with the car here, and they assume the parts are available '
           'and, on a claim, that authorisation is already in place.',
          ]),
          ('Why it cannot be compressed', [
           'Filler, primer and lacquer each need to harden before the next stage touches them. '
           'Baking accelerates it but does not remove it, and a repair pushed through faster '
           'than the materials allow keeps shrinking afterwards.',
           'That is the cause of a repair that looks perfect at handover and shows a faint '
           'outline of the repair area a few months later. Nothing was done wrong except the '
           'clock.',
          ]),
          ('What actually causes the delays on a claim', [
           ('table', (['Cause', 'Typical delay'], [
             ['Waiting for authorisation', '2&ndash;10 days'],
             ['Parts on back order', '1 day to several weeks'],
             ['Supplementary after strip-down', '2&ndash;7 days'],
             ['Engineer inspection backlog', '2&ndash;5 days'],
             ['Disputed labour times', 'Open-ended'],
           ])),
           'Add those up and a three-day repair becomes a three-week claim, with the car sitting '
           'stripped for most of it. None of that is workshop time, which is why "how long does '
           'the repair take" and "when do I get my car back" have different answers.',
          ]),
          ('What you can do', [
           ['Report it the same day and name your repairer immediately.',
            'Chase authorisation yourself if it stalls. A call from the policyholder moves things '
            'a call from the bodyshop does not.',
            'Say early if the car is needed by a particular date &mdash; sometimes the order of '
            'work can be arranged around it.',
            'Decide about a replacement car at the start rather than three days in.'],
           ('note', 'We will give you a real date rather than an optimistic one, and tell you '
                    'when it moves. An estimate that is always "tomorrow" for a week is worse '
                    'than an honest fortnight.'),
          ]),
         ],
         [('Can you do it faster if I pay more?',
           'Not the curing, no &mdash; that is chemistry. What can sometimes be arranged is where '
           'your car sits in the queue, and that is worth asking about if you have a real '
           'deadline.'),
          ('Can I drive it while I wait for parts?',
           'Often yes, if it is roadworthy and the damage is not going to get worse. We will tell '
           'you honestly if it should not be driven.'),
          ('Why was my car in for two weeks for a bumper?',
           'Almost certainly authorisation and parts rather than work. Ask for the dates: when '
           'the estimate went in, when it was authorised, when the parts arrived.'),
          ('Do you work weekends?',
           'Ring and ask. On a job where the timing genuinely matters we will do what we can.')],
         [('bodywork-repair-process', 'The repair process, step by step'),
          ('how-a-bodywork-insurance-claim-works-step-by-step', 'How a claim works'),
          ('supplementary-estimate-explained', 'Supplementary estimates'),
          ('what-happens-at-strip-down', 'What strip-down finds')],
         key_points=[
          'Most of the time, <strong>nobody is touching the car</strong>.',
          'Curing is <strong>chemistry</strong> &mdash; it cannot be paid to go faster.',
          'On a claim the delays are <strong>authorisation and parts</strong>, not the workshop.',
          'A real date beats an optimistic one. We will tell you when it <strong>moves</strong>.',
         ],
         hub=HUB_PROCESS, category='process', service_type='Vehicle body repair', note=None),

    page('metallic-pearl-and-three-stage-paint',
         'Metallic, Pearl and Three-Stage Paint Explained | KITH Cars',
         'The difference between solid, metallic, pearl and three-stage finishes, why each is '
         'harder to match than the last, and what it means for repairing your car.',
         'Metallic, Pearl and Three-Stage Paint',
         'The repair process &middot; Paint',
         'Four kinds of paint, each harder than the last, and the one on your car decides how '
         'much skill a repair takes. There is no surcharge for any of them on our rate card '
         '&mdash; there is a difference in the work.',
         [
          ('The four finishes', [
           ('table', (['Finish', 'How it is built', 'Difficulty'], [
             ['Solid', 'Colour, then lacquer', 'Straightforward'],
             ['Metallic', 'Colour with aluminium flake, then lacquer', 'Moderate'],
             ['Pearl', 'Colour with ceramic particles, then lacquer', 'Hard'],
             ['Three-stage', 'Base colour, translucent mid-coat, then lacquer', 'Hardest'],
           ])),
          ]),
          ('Why flake changes everything', [
           'A solid colour is the same colour from any angle, because it is pigment and nothing '
           'else. Add aluminium flake and the paint now reflects light directionally: the shade '
           'you see depends on how the flake is lying and where you are standing.',
           'That means spray technique matters as much as the mix. Two painters with the same tin '
           'can produce visibly different panels, because gun distance, air pressure and how the '
           'coats are laid down all change how the flake orients as the paint flashes off.',
           'It is also why a metallic is blended into the next panel even when the mix is '
           'perfect. A perfect mix sprayed slightly differently still reads as a different panel '
           'in raking light.',
          ]),
          ('Pearl and three-stage', [
           'Pearl uses ceramic particles rather than aluminium. They do not just reflect light, '
           'they refract it, which is where the colour shift comes from &mdash; a pearl white '
           'that goes faintly gold or pink depending on the angle.',
           'Three-stage takes that further: a solid base, then a translucent tinted mid-coat, '
           'then lacquer. The final colour depends on how many coats of the mid went on and how '
           'evenly. Two coats and three coats are different colours, and there is no correcting '
           'it after the lacquer goes on.',
           'This is why a three-stage repair is always sprayed out on a test card first, with the '
           'mid-coat applied in the same number of passes it will get on the car.',
          ]),
          ('What it means for your repair', [
           ['<strong>Solid white or black.</strong> Forgiving. A competent repair will match.',
            '<strong>Metallic silver or grey.</strong> The most common finish on the road and '
            'genuinely tricky, because silver shows flake orientation more than any other '
            'colour.',
            '<strong>Pearl white.</strong> Very common on modern cars and one of the hardest '
            'things in the trade.',
            '<strong>Three-stage reds and pearls.</strong> Where blending stops being good '
            'practice and becomes the only way.'],
           ('note', 'No surcharge on our rate card for metallic, pearl, three-stage or a colour '
                    'change. The work is harder; the price is the price.'),
          ]),
         ],
         [('How do I know which my car has?',
           'The paint code tells us. Broadly: if the colour looks different as you walk past it, '
           'there is flake or pearl in it. Pearl whites and three-stage reds are the usual ones '
           'people are surprised by.'),
          ('Is a pearl repair more likely to go wrong?',
           'It is less forgiving, which is not the same thing. Done with a spray-out card and a '
           'proper blend, it matches. Done from the code with no test card, it is the finish most '
           'likely to show.'),
          ('Can you repair a colour-change or wrapped car?',
           'Painted colour changes, yes &mdash; we match what is on the car now. A wrap is a '
           'different trade: we repair the panel underneath and you have it re-wrapped.'),
          ('Does a harder finish take longer?',
           'A little, mostly in the matching rather than the spraying. It is usually within the '
           'same timescale band.')],
         [('paint-colour-matching-explained', 'How paint matching works'),
          ('paint-blending-explained', 'Why we blend into the next panel'),
          ('why-repairs-dont-match', 'Why some repairs do not match'),
          ('bodywork-repair-process', 'The repair process, step by step')],
         key_points=[
          'Four finishes, each <strong>harder to match</strong> than the last.',
          'Flake means <strong>spray technique matters as much as the mix</strong>.',
          'Three-stage colour depends on <strong>how many mid-coats</strong> went on.',
          '<strong>No surcharge</strong> for any of them on our rate card.',
         ],
         hub=HUB_PROCESS, category='process', service_type='Vehicle paint', note=None),

    page('fault-accident-what-happens-next',
         'I Caused the Accident: What Happens Next? | KITH Cars',
         'What to do after an accident that was your fault — at the scene, with your insurer, '
         'and what it costs you in excess, no-claims and future premiums.',
         'It Was My Fault. What Happens Now?',
         'Insurance &amp; claims &middot; Fault and liability',
         'The practical steps are much the same as any accident. What differs is what it costs '
         'you, and the mistake people make is going quiet &mdash; which makes everything worse '
         'rather than better.',
         [
          ('At the scene, even when you know it was you', [
           ('steps', [
             '<strong>Stop and exchange details.</strong> <span>A legal requirement where there '
             'is damage or injury, regardless of fault.</span>',
             '<strong>Do not admit liability.</strong> <span>This sounds like advice to be '
             'dishonest and it is not. You may not know everything &mdash; a faulty brake light, '
             'their speed, a third vehicle. Be civil, apologise for the situation if you want '
             'to, and leave the fault finding to the insurers.</span>',
             '<strong>Photograph everything anyway.</strong> <span>Including their damage. It '
             'protects you against a claim for damage that was already there.</span>',
             '<strong>Get witness details.</strong> <span>Especially if you think liability might '
             'be shared.</span>',
           ]),
           ('note', 'Admitting fault at the scene can breach a condition of your policy. That is '
                    'the practical reason not to, quite apart from whether you are right.'),
          ]),
          ('What it costs you', [
           ('table', (['', 'What happens'], [
             ['Your excess', 'Payable, and not recoverable &mdash; there is nobody to recover '
              'from'],
             ['Your no-claims discount', 'Reduced, unless you have protected it'],
             ['Your premium', 'Rises at renewal, usually for several years'],
             ['Declaration', 'You declare the claim for around five years'],
             ['The other party', 'Their repair, hire car and any injury claim, paid by your '
              'insurer'],
           ])),
           'That bottom row is why not reporting a fault accident is a bad idea even on minor '
           'damage. Their claim against you exists whether you told your insurer or not, and the '
           'first your insurer hears of it should not be a solicitor&rsquo;s letter.',
          ]),
          ('Should you pay privately instead?', [
           'Sometimes, and the sum is the same as any other claim: the repair cost against your '
           'excess plus what the claim does to your premium over five years.',
           'The difference on a fault accident is that there is another party, and settling '
           'privately means settling with them. Get their damage properly estimated before '
           'agreeing a figure, because a bumper that looks scuffed can have a broken crash bar '
           'behind it, and you have no protection if the number turns out to be wrong.',
           'Notify your insurer either way. Most policies require notification of any incident '
           'even where you do not claim.',
          ]),
          ('If you think it might not have been entirely your fault', [
           'Say so, early, and in writing. Liability is frequently shared, and a split decision '
           'changes your excess recovery, your no-claims and your premium.',
           'Dashcam footage, a witness, the road layout, their lighting or their speed can all '
           'move it. The time to raise it is before your insurer concedes liability, not after.',
           ('note', CHOICE_NOTE),
          ]),
         ],
         [('Will my premium go up a lot?',
           'It depends on your history and how much discount you had. A first fault claim with '
           'several years of no-claims is usually absorbed better than people fear; a second '
           'within a few years is not.'),
          ('Can I pay the other driver and keep it off my insurance?',
           'You can try, and it sometimes works for genuinely minor damage. The risk is that they '
           'claim anyway later, and you have already paid out.'),
          ('Does protected no-claims mean nothing changes?',
           'It protects the discount, not the premium the discount comes off. Your renewal can '
           'still rise.'),
          ('Can you repair my car on a fault claim?',
           'Yes. The choice of repairer is yours on any claim, fault or not. Check whether your '
           'policy ties a courtesy car to their network before you decide.')],
         [('non-fault-accident-what-to-do', 'If it was not your fault'),
          ('split-liability-explained', 'Split liability explained'),
          ('should-i-claim-or-pay-myself', 'Claim or pay yourself?'),
          ('protected-no-claims-explained', 'Protected no-claims')],
         key_points=[
          '<strong>Do not admit liability</strong> at the scene &mdash; it can breach your '
          'policy.',
          'Your excess is payable and <strong>not recoverable</strong>.',
          '<strong>Notify even if you pay privately.</strong> Their claim exists either way.',
          'Think it was shared? <strong>Say so before your insurer concedes.</strong>',
         ]),

    page('split-liability-explained',
         'Split Liability Explained: When You Are Both Partly at Fault | KITH Cars',
         'What a split liability settlement means, the common splits, how it affects your excess '
         'and no-claims, and whether to accept one.',
         'Split Liability: Both Partly at Fault',
         'Insurance &amp; claims &middot; Fault and liability',
         'Plenty of accidents are not one person&rsquo;s fault. When insurers agree a split, '
         'everything downstream splits with it &mdash; your excess recovery, your no-claims, and '
         'what gets paid.',
         [
          ('What a split actually means', [
           'Liability is apportioned as a percentage between the drivers. The usual outcomes are '
           '50/50, 75/25 and 25/75, and each insurer pays the other&rsquo;s losses in proportion.',
           ('table', (['Split', 'What it means for you at 50/50'], [
             ['Your repair', 'Half recovered from them'],
             ['Your excess', 'Half returned to you'],
             ['Your no-claims', 'Usually partly affected'],
             ['Their repair', 'Half paid by your insurer'],
           ])),
           'A 50/50 is not "nobody was at fault". It is "both were, equally", and it is recorded '
           'as a claim against you as well as against them.',
          ]),
          ('When splits happen', [
           ['Both vehicles moving and both contributed &mdash; lane changes, roundabouts, '
            'junctions.',
            'No independent witness and two credible but incompatible accounts.',
            'One driver clearly at fault but the other was speeding, had a light out, or could '
            'have avoided it.',
            'Car parks, where right of way is often unmarked and ambiguous.',
            'Neither insurer wants the cost of litigating a modest claim.'],
           'That last one is worth naming. A 50/50 is sometimes a commercial settlement between '
           'two insurers rather than a finding about what happened, and it can be offered simply '
           'because arguing costs more than conceding.',
          ]),
          ('Should you accept one?', [
           ('steps', [
             '<strong>Ask what evidence they are relying on.</strong> <span>If the answer is '
             '"two conflicting accounts", your own evidence may still change it.</span>',
             '<strong>Produce what you have.</strong> <span>Dashcam footage, witness details, '
             'photographs of the road layout and final positions.</span>',
             '<strong>Say clearly that you do not accept it.</strong> <span>In writing. '
             'Insurers can and do settle on your behalf, and silence is taken as '
             'agreement.</span>',
             '<strong>Weigh the cost of fighting.</strong> <span>On a small claim the difference '
             'between 50/50 and 100% in your favour may be less than the time and stress of '
             'contesting it.</span>',
             '<strong>Complain if they conceded without asking you.</strong> <span>Your policy '
             'lets them settle, but a decision made without considering evidence you offered is '
             'worth challenging.</span>',
           ]),
          ]),
          ('The practical effects', [
           'Your excess comes back in proportion, so on a 50/50 expect half. Your no-claims is '
           'usually affected, because your insurer has paid out and only recovered part of it. '
           'And the claim is declarable like any other.',
           'If you had a credit hire car, a split is where that can leave a balance &mdash; the '
           'recovery only covers the proportion attributed to the other driver.',
           ('note', ADVICE_NOTE),
          ]),
         ],
         [('Can I refuse a 50/50?',
           'You can refuse to agree, and you should say so in writing if you believe it is wrong. '
           'Your insurer can still settle under the terms of your policy, but a documented '
           'objection with evidence attached makes that harder and gives you grounds to complain.'),
          ('Does a split count as a fault claim?',
           'Effectively yes for most pricing purposes, which is why it is worth contesting if the '
           'evidence is on your side.'),
          ('What if I have dashcam footage?',
           'Provide it immediately, before any decision is made. It is the single most effective '
           'thing at moving a split, and it is much less useful after a settlement has been '
           'agreed.'),
          ('Does the split affect my repair?',
           'Not the work itself. Your car is repaired properly either way. It affects who '
           'ultimately pays and how much of your excess comes back.')],
         [('non-fault-accident-what-to-do', 'Non-fault accident: what to do'),
          ('fault-accident-what-happens-next', 'If it was your fault'),
          ('recovering-your-excess-after-a-non-fault-accident', 'Recovering your excess'),
          ('credit-hire-explained', 'Credit hire explained')],
         key_points=[
          'Liability apportioned as a <strong>percentage</strong>, and everything splits with it.',
          'A 50/50 means <strong>both at fault</strong>, not neither.',
          'Sometimes a <strong>commercial settlement</strong> between insurers, not a finding.',
          '<strong>Object in writing</strong> &mdash; silence is taken as agreement.',
         ]),

    page('protected-no-claims-explained',
         'Protected No-Claims Discount: Is It Worth It? | KITH Cars',
         'What protecting your no-claims actually protects, what it does not, how many claims it '
         'covers and whether the extra premium is worth paying.',
         'Protected No-Claims: What It Really Covers',
         'Insurance &amp; claims &middot; No-claims',
         'It protects the discount. It does not protect the premium the discount comes off, and '
         'that distinction is the entire reason people feel misled by it.',
         [
          ('What you are actually buying', [
           'Your premium is calculated, then your no-claims discount is applied as a percentage '
           'off. Protection stops the <em>percentage</em> falling after a claim. It does nothing '
           'about the number it is subtracted from.',
           'So you can claim, keep your full discount, and still see your renewal rise &mdash; '
           'because the underlying premium was recalculated to reflect that you have claimed. '
           'Both things are true at once and neither is a trick.',
           ('table', (['', 'Without protection', 'With protection'], [
             ['Your discount after a claim', 'Falls', 'Stays'],
             ['Your underlying premium', 'Rises', 'Rises'],
             ['Your actual renewal', 'Rises more', 'Rises less'],
             ['Declaring the claim', 'Five years', 'Five years'],
           ])),
          ]),
          ('How many claims it covers', [
           'Usually a stated number within a period &mdash; commonly two claims in three years, '
           'or similar. Beyond that the protection is exhausted and the discount falls anyway.',
           'The exact terms vary considerably between insurers, and this is one of the few things '
           'genuinely worth reading in the policy booklet rather than the summary. Check the '
           'number, the period, and whether non-fault claims count toward it.',
          ]),
          ('Is it worth the money?', [
           ['<strong>Worth it</strong> if you have several years of discount built up, because '
            'that is real money and losing it costs more than the protection does.',
            '<strong>Worth it</strong> if you drive a lot of miles or park somewhere your car '
            'gets hit.',
            '<strong>Less worth it</strong> in the first couple of years, when there is little '
            'discount to protect.',
            '<strong>Not a substitute</strong> for deciding whether to claim at all. On small '
            'bodywork the better answer is often to pay directly regardless.'],
          ]),
          ('The thing worth doing at renewal', [
           'Ask your insurer for the premium with and without protection, and ask what your '
           'discount is worth in pounds. Both numbers are available and neither is usually '
           'offered.',
           'With those two figures the decision takes thirty seconds: if protection costs less '
           'than a meaningful fraction of what the discount saves you, it is cheap insurance on '
           'your insurance.',
           ('note', ADVICE_NOTE),
          ]),
         ],
         [('Does protection cover a non-fault claim?',
           'It protects the discount in either case. Whether a non-fault claim counts toward your '
           'allowance of protected claims varies by insurer, so check.'),
          ('If I change insurer, does my protection carry over?',
           'Your no-claims years carry over. The protection is a product of the policy you are '
           'leaving, so you buy it again with the new insurer if you want it.'),
          ('Can I protect it after a claim?',
           'Usually only at renewal, and some insurers will not offer it immediately after a '
           'claim. Ask.'),
          ('Is it worth it if I have maximum discount already?',
           'That is exactly when it is worth most, because you have the most to lose.')],
         [('will-a-non-fault-claim-affect-my-no-claims', 'Claims and your no-claims'),
          ('should-i-claim-or-pay-myself', 'Claim or pay yourself?'),
          ('fault-accident-what-happens-next', 'If it was your fault'),
          ('compulsory-vs-voluntary-excess', 'Compulsory vs voluntary excess')],
         key_points=[
          'Protects the <strong>discount</strong>, not the premium it comes off.',
          'You can keep full discount and <strong>still pay more</strong> at renewal.',
          'Covers a <strong>stated number of claims</strong> &mdash; check how many.',
          'Ask for the premium <strong>with and without</strong>, plus what your discount is '
          'worth.',
         ]),

    page('excess-protection-cover-worth-it',
         'Is Excess Protection Cover Worth It? | KITH Cars',
         'How excess protection works, what it actually reimburses, when it pays for itself and '
         'when it is a product sold rather than bought.',
         'Is Excess Protection Worth Buying?',
         'Insurance &amp; claims &middot; Excess',
         'It is a separate policy that pays your excess back after a claim. Whether it is worth '
         'it comes down to one comparison almost nobody makes at the point of sale.',
         [
          ('How it works', [
           'Excess protection is its own small insurance policy, usually sold alongside the motor '
           'cover. You still pay your excess to the bodyshop or have it deducted from a '
           'settlement; you then claim it back from the excess policy.',
           'It does not reduce your excess. It reimburses it, after the fact, on a successful '
           'claim.',
          ]),
          ('The comparison worth making', [
           ('steps', [
             '<strong>What does it cost per year?</strong> <span>Usually a modest annual '
             'premium.</span>',
             '<strong>What is the most it pays out?</strong> <span>There is a cap, and it may be '
             'lower than your total excess.</span>',
             '<strong>How many claims per year?</strong> <span>Often limited to one.</span>',
             '<strong>What is excluded?</strong> <span>This is the one that matters &mdash; see '
             'below.</span>',
             '<strong>Then divide.</strong> <span>Premium against payout. If you would need to '
             'claim more than once every few years for it to pay, it probably does not.</span>',
           ]),
          ]),
          ('What is usually excluded', [
           ['Claims where you were not at fault and the excess is recoverable anyway &mdash; '
            'which removes a large slice of the cases you imagined it covering.',
            'Glass and windscreen claims, which carry their own separate excess.',
            'Claims below a stated minimum.',
            'Anything your motor insurer declines.'],
           'That first exclusion is the important one, and it is rarely explained at the point of '
           'sale. On a non-fault claim your excess should come back from the at-fault '
           'insurer regardless, so excess protection is doing nothing you were not already '
           'entitled to.',
          ]),
          ('When it genuinely makes sense', [
           'If your excess is high &mdash; because you chose a large voluntary excess to bring '
           'the premium down, or because the car or your history forces a high compulsory one '
           '&mdash; and you would struggle to find that money at short notice, then it is buying '
           'certainty rather than value, and that is a legitimate reason.',
           'If your excess is modest and you could cover it without difficulty, it is usually a '
           'product sold rather than a product bought.',
           ('note', ADVICE_NOTE),
          ]),
         ],
         [('Does it cover the whole excess?',
           'Up to the cap on the policy, which may be less than your total excess. Check the cap '
           'against compulsory plus voluntary, not just one of them.'),
          ('Can I buy it separately from my motor insurance?',
           'Yes, standalone excess protection exists and is sometimes cheaper than the add-on.'),
          ('Does it work on a non-fault claim?',
           'Often it is excluded there, on the basis that your excess is recoverable from the '
           'other side anyway. Read that section specifically.'),
          ('Would it be cheaper just to lower my voluntary excess?',
           'Frequently, yes, and it is the comparison nobody offers you. Ask for the premium with '
           'a lower voluntary excess and compare it against the cost of protecting the higher '
           'one.')],
         [('who-pays-my-excess', 'Who pays my excess'),
          ('compulsory-vs-voluntary-excess', 'Compulsory vs voluntary excess'),
          ('recovering-your-excess-after-a-non-fault-accident', 'Recovering your excess'),
          ('should-i-claim-or-pay-myself', 'Claim or pay yourself?')],
         key_points=[
          'It <strong>reimburses</strong> your excess, it does not reduce it.',
          'Non-fault claims are <strong>often excluded</strong> &mdash; the excess is recoverable '
          'anyway.',
          'Check the <strong>cap</strong> against compulsory plus voluntary, not one of them.',
          'Often cheaper to <strong>lower your voluntary excess</strong> instead.',
         ]),

    page('paying-for-bodywork-yourself-vs-claiming',
         'Paying for Bodywork Yourself: What It Costs and When It Wins | KITH Cars',
         'What private bodywork repair costs, how it compares with claiming, what you keep by '
         'paying directly, and why you should still tell your insurer.',
         'Paying for Bodywork Yourself',
         'Insurance &amp; claims &middot; Deciding',
         'Most single-panel damage is cheaper to pay for than to claim for, and the reason is '
         'not the repair cost. It is the five years afterwards.',
         [
          ('What you keep by paying directly', [
           ['<strong>Your no-claims discount, untouched.</strong>',
            '<strong>Your renewal premium</strong>, which rises after a claim whether or not it '
            'was your fault.',
            '<strong>A clean five years.</strong> You declare claims for around five years, and '
            'every quote you get in that time is priced on them.',
            '<strong>Control of the job.</strong> No engineer deciding the method, no authorised '
            'labour rate, no supplementary round. We agree the work with you and do it.',
            '<strong>Speed.</strong> No waiting for authorisation, which is most of the delay on '
            'a claim.'],
          ]),
          ('How the sum usually falls', [
           'Take a typical single-panel repair against a typical total excess of a few hundred '
           'pounds. Claiming often nets you very little, and in exchange you lose discount, '
           'carry a declared claim, and wait for authorisation.',
           'The crossover is roughly one to three times your excess, and where it falls depends '
           'on how much no-claims you have built up. Below that, paying is obvious. Well above '
           'it, claiming is obvious. In between, the discount decides it.',
           ('note', 'Get the real figure before you phone anyone. Put your registration into the '
                    'quote box on this page and you will have a price band in a few seconds. '
                    'Then the comparison is real rather than a guess.'),
          ]),
          ('Tell your insurer anyway', [
           'This is the step people skip and it is the one that causes trouble. Most policies '
           'require you to notify any incident, even one you have no intention of claiming for.',
           'Notify, state plainly that you are paying privately and not claiming, and ask them to '
           'record it as notification only. Non-disclosure discovered later is a far bigger '
           'problem than a notified non-claim &mdash; it can affect a future claim entirely '
           'unrelated to this one.',
          ]),
          ('What you give up', [
           'Honesty cuts both ways. Paying privately means no courtesy car unless we can sort '
           'one, no engineer to catch something we missed, and the cost of any hidden damage '
           'found at strip-down falls to you rather than to an insurer.',
           'That last one is the real risk, and it is why we tell you at the estimate which parts '
           'of a job are uncertain. On a bumper where we cannot see the crash bar, you should '
           'know that before you commit rather than after.',
           ('note', CHOICE_NOTE),
          ]),
         ],
         [('Will you do an insurance-standard repair if I am paying myself?',
           'It is the same repair. We do not have a cheaper method we keep for private customers '
           '&mdash; the paint is blended either way and the guarantee is the same.'),
          ('Can I pay in instalments?',
           'Talk to us. We would rather agree something workable than have you driving around '
           'with damage.'),
          ('What if it turns out to be more than quoted?',
           'We stop and tell you before doing the extra work, with photographs. You decide '
           'whether to proceed. You are never handed a bill you did not agree to.'),
          ('Does paying privately mean no guarantee?',
           'No. One year on paint and three months on mechanical work, in writing, whoever is '
           'paying.')],
         [('should-i-claim-or-pay-myself', 'Claim or pay yourself?'),
          ('who-pays-my-excess', 'Who pays my excess'),
          ('will-a-non-fault-claim-affect-my-no-claims', 'Claims and your no-claims'),
          ('bodywork-repair-process', 'The repair process, step by step')],
         key_points=[
          'You keep your <strong>discount, your premium and a clean five years</strong>.',
          'The crossover is <strong>one to three times your excess</strong>.',
          '<strong>Notify anyway.</strong> Non-disclosure is the bigger risk.',
          'What you give up: <strong>hidden damage</strong> found at strip-down is yours.',
         ]),

    page('selling-a-cat-s-or-cat-n-car',
         'Selling a Cat S or Cat N Car | What to Expect | KITH Cars',
         'What you must disclose when selling a recorded write-off, how much value it costs, who '
         'buys them, and how to get the best price.',
         'Selling a Cat S or Cat N Car',
         'Insurance &amp; claims &middot; Write-offs',
         'You must disclose it, the buyer will find it anyway, and the price reflects it. What '
         'you can control is how much documentation goes with the car, and that is worth more '
         'than most sellers realise.',
         [
          ('What you have to disclose', [
           'A recorded write-off category is a material fact. Selling without disclosing it '
           'misrepresents the car, and a buyer who discovers it afterwards has a legitimate '
           'grievance and, potentially, a claim against you.',
           'It is also pointless to hide. Any buyer running a history check &mdash; which costs a '
           'few pounds and takes a minute &mdash; sees it immediately. A seller who did not '
           'mention it has just told the buyer something about themselves rather than about the '
           'car.',
          ]),
          ('What it costs you in value', [
           ('table', (['', 'Typical effect'], [
             ['Category N', 'A noticeable reduction, proportionally harsher on cheaper cars'],
             ['Category S', 'More than N, and more again on newer or desirable models'],
             ['Old Category C or D', 'Similar to S and N respectively, sometimes worse because '
              'the marker tells a buyer less'],
             ['Undocumented repair', 'Worst of all &mdash; the discount buyers apply for the '
              'unknown'],
           ])),
           'That bottom row is the one you can do something about. The difference between a '
           'recorded write-off with a full file of repair documentation and one with nothing is '
           'substantial, because buyers price uncertainty.',
          ]),
          ('How to get the best price', [
           ('steps', [
             '<strong>Gather every document.</strong> <span>The repair invoice, the itemised '
             'estimate, photographs of the damage and of the repair in progress.</span>',
             '<strong>Say it in the advert, near the top.</strong> <span>Not buried at the '
             'bottom. A buyer who finds it late feels misled; one who reads it first is already '
             'considering it.</span>',
             '<strong>Explain what the damage actually was.</strong> <span>"Cat N &mdash; rear '
             'bumper and boot lid, no structural damage, repaired at [bodyshop] with '
             'invoices" reads completely differently from "Cat N".</span>',
             '<strong>Offer an inspection.</strong> <span>Welcoming an independent inspection is '
             'the strongest signal you can send.</span>',
             '<strong>Price it realistically.</strong> <span>Against other recorded cars, not '
             'against clean ones.</span>',
           ]),
          ]),
          ('Who buys them', [
           'More people than sellers expect. Buyers who intend to keep a car long term care less '
           'about resale, and a well-documented Cat N at a fair discount is good value for '
           'someone doing high mileage or wanting more car than their budget otherwise buys.',
           'Trade buyers and auctions are the quick route and pay the least. A private sale with '
           'full documentation takes longer and gets more.',
           ('note', ADVICE_NOTE),
          ]),
         ],
         [('Do I have to tell a trade buyer?',
           'Yes. The obligation to describe the car accurately does not depend on who is buying, '
           'and a trade buyer will check regardless.'),
          ('Can the marker ever be removed?',
           'Not if it was correctly applied. If it was recorded in error, that is a correction '
           'through the insurer who recorded it, and you will need evidence.'),
          ('Does an MOT pass prove the repair was good?',
           'No, and it is worth being clear about with buyers. An MOT is a roadworthiness check '
           'at a point in time; it does not assess the quality of a structural repair.'),
          ('Will you provide documentation if you did the repair?',
           'Yes. Itemised invoice, the estimate, and the strip-down photographs. That file is '
           'genuinely worth money when you come to sell.')],
         [('car-write-off-categories-explained', 'All four categories'),
          ('category-n-write-off', 'Category N explained'),
          ('category-s-write-off', 'Category S explained'),
          ('can-i-keep-my-written-off-car', 'Keeping a written-off car')],
         key_points=[
          'You <strong>must disclose it</strong>, and a history check finds it anyway.',
          'The biggest discount buyers apply is for <strong>the unknown</strong>, not the '
          'category.',
          '<strong>Documentation is worth real money</strong> &mdash; invoices and strip-down '
          'photographs.',
          'Put it <strong>near the top of the advert</strong>, with what the damage actually was.',
         ]),

    page('flood-damage-and-your-car',
         'Flood Damage to a Car: What Happens Next | KITH Cars',
         'Why flooded cars are usually written off, the difference between fresh and salt water, '
         'what to do immediately, and why buying one is rarely a bargain.',
         'Flood Damage: What Happens to the Car',
         'Insurance &amp; claims &middot; Specific situations',
         'Water in a car is not like other damage. It does not stop when it dries, it is rarely '
         'confined to what you can see, and it is the main reason a car is written off as '
         'Category A rather than repaired.',
         [
          ('Why water is different', [
           'Most damage is where it looks. Water goes everywhere, sits in places that never dry, '
           'and keeps working for years &mdash; through wiring looms by capillary action, into '
           'connectors, inside sills and box sections, under carpet and sound deadening.',
           'The corrosion starts immediately and continues long after the car looks and smells '
           'fine. An electrical fault eighteen months later, in a circuit nothing has touched, is '
           'the classic signature.',
          ]),
          ('Fresh water against salt water', [
           ('table', (['', 'Fresh water', 'Salt water'], [
             ['Corrosion', 'Slower', 'Rapid and relentless'],
             ['Electrical damage', 'Serious', 'Usually terminal'],
             ['Likely outcome', 'Depends on depth and duration', 'Almost always Category A or B'],
           ])),
           'Salt water is effectively a death sentence for a modern car. It attacks connectors '
           'and circuit boards directly and it does not stop when the car dries out.',
          ]),
          ('What to do immediately', [
           ('steps', [
             '<strong>Do not try to start it.</strong> <span>If water has reached the air '
             'intake, cranking it draws water into the cylinders. Water does not compress, and '
             'the engine destroys itself in a second.</span>',
             '<strong>Disconnect the battery if it is safe to do so.</strong> <span>Powered '
             'circuits sitting in water corrode far faster.</span>',
             '<strong>Photograph the water line.</strong> <span>Inside and out, before anything '
             'is moved or dried. It is the single most important piece of evidence.</span>',
             '<strong>Note how long it was submerged.</strong> <span>And whether the water was '
             'fresh or salt.</span>',
             '<strong>Call your insurer.</strong> <span>Flood damage is covered by '
             'comprehensive cover. Get it recovered rather than driven.</span>',
           ]),
          ]),
          ('Why they get written off', [
           'The assessment is not about whether a flooded car can be made to work. It is about '
           'whether it can be made reliable and safe, and proving that is close to impossible '
           'once water has been through the electrics.',
           'Insurers therefore write off flooded cars readily and categorise them cautiously, '
           'frequently as A or B. That is why flood-damaged cars disappear from the market '
           'rather than circulating repaired &mdash; or should.',
          ]),
          ('Buying one is rarely a bargain', [
           'Flooded cars do appear for sale, often cleaned up and a long way from where they were '
           'flooded, sometimes after a flood event that made the news months earlier.',
           ['Damp or musty smell, particularly after the car has been shut up.',
            'Silt or a tide line in the spare wheel well, under the carpet, or in the seat rails.',
            'Mismatched or unusually clean carpet in an otherwise average car.',
            'Corrosion on unpainted metal under the dash, on seat frames or on seatbelt bolts.',
            'Electrical faults that come and go, or warning lights that clear themselves.'],
           ('note', 'Always run a history check, and be especially careful with a car being sold '
                    'far from where it is registered. A Category A or B car cannot legally '
                    'return to the road at all.'),
          ]),
         ],
         [('Is flood damage covered by insurance?',
           'By comprehensive cover, yes, as accidental damage. Third-party-only cover does not '
           'cover damage to your own car.'),
          ('My car was only in shallow water. Is it fine?',
           'Possibly, and it depends on what the water reached rather than how deep it looked. '
           'The critical levels are the air intake, the ECU and the door-mounted modules, and '
           'those are lower on some cars than people assume.'),
          ('Can a flooded car be repaired?',
           'A lightly affected one, sometimes &mdash; carpets out, dried properly, affected '
           'components replaced. One that was submerged to dash height is not an economic repair '
           'and often not a safe one.'),
          ('Can you assess mine?',
           'We can look at the bodywork and tell you what we see. A flooded car needs a proper '
           'electrical assessment as well, and we will be straight with you about where that sits '
           'relative to what we do.')],
         [('car-write-off-categories-explained', 'All four categories'),
          ('category-a-and-b-write-offs', 'Categories A and B'),
          ('car-rust-repair', 'Rust and corrosion repair'),
          ('write-off-valuation-too-low-what-to-do', 'Challenging a low valuation')],
         key_points=[
          '<strong>Do not try to start it.</strong> Cranking a flooded engine destroys it.',
          'Water <strong>keeps working for years</strong> after the car looks dry.',
          'Salt water is <strong>almost always terminal</strong> for a modern car.',
          'A cheap flood car is <strong>rarely a bargain</strong> &mdash; check the history.',
         ]),
]
