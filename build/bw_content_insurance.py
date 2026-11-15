#!/usr/bin/env python3
"""Insurance and claims pages.

Accuracy notes, because this is the one cluster on the site where being wrong costs the customer
money rather than just reading badly:

  * KITH is on no insurer panel and is not a manufacturer-approved repairer. Nothing here may
    imply otherwise. What is true, and is the spine of this cluster, is that the customer chooses
    the repairer - not the insurer.
  * Write-off categories are the post-October-2017 set: A, B, S, N. The older C and D appear only
    where a page explains what they used to mean.
  * Specific statutory figures and time limits are deliberately described rather than quoted,
    because they move and a wrong number on a published page is worse than no number.
  * Every page carries the standing note that this is general information rather than advice.
"""

ADVICE_NOTE = ('This is general information about how motor claims usually work, not legal or '
               'financial advice. Your own policy wording decides what you are entitled to, so '
               'read it, or ring us on <a href="tel:02046299469">020 4629 9469</a> and we will '
               'talk it through against the damage in front of us.')

CRUMB_HUB = ('Insurance &amp; claims', 'car-insurance-claims')


def _p(slug, title, desc, h1, label, lead, sections, faqs, related=(), job='panel-front-bumper',
       service_type='Accident repair', quote_heading='Price your repair now', key_points=()):
    return {
        'slug': slug, 'title': title, 'desc': desc, 'h1': h1, 'label': label, 'lead': lead,
        'key_points': list(key_points),
        'sections': sections + [('Before you act on any of this', [('note', ADVICE_NOTE)])],
        'faqs': faqs, 'related': list(related), 'job': job, 'flow': 'bodywork',
        'service_type': service_type, 'quote_heading': quote_heading,
        'crumbs': [CRUMB_HUB, (h1, None)],
        'category': 'insurance',
    }


PAGES = [

    _p('do-i-have-to-use-my-insurers-approved-repairer',
       'Do I Have to Use My Insurer\'s Approved Repairer? | KITH Cars',
       'No. You choose who repairs your car, not your insurer. What the approved network actually '
       'is, what your policy can and cannot do about it, and what to say on the phone.',
       'Do I Have to Use My Insurer&rsquo;s Approved Repairer?',
       'Insurance &amp; claims &middot; Choice of repairer',
       'No. The car is yours and you decide who repairs it. Insurers steer you towards their own '
       'network because it costs them less, and the script they use can sound like a rule. It '
       'is not one.',
       [
        ('What the approved network actually is', [
         'An insurer&rsquo;s &ldquo;approved repairer&rdquo; list is a commercial arrangement. '
         'Bodyshops on it have agreed discounted labour rates and, in most cases, to use the '
         'insurer&rsquo;s preferred parts and estimating method in exchange for a steady flow of '
         'work. It is a supply contract. It is not a quality badge, and no regulator audits entry '
         'to it.',
         'That does not make approved shops bad &mdash; plenty are excellent. It does mean the '
         'list was drawn up to serve the insurer&rsquo;s costs, and the discount has to come from '
         'somewhere: usually the labour time allowed on the job, and sometimes the grade of parts '
         'specified.',
        ]),
        ('What your insurer can and cannot do', [
         'Your insurer cannot force you to use their repairer. What they can do is write terms '
         'into the policy about what changes if you do not, and those terms are enforceable '
         'because you agreed to them when you bought the cover.',
         ('table', (['What they may do', 'Whether it is usually enforceable'], [
            ['Recommend their own network strongly', 'Yes &mdash; and they will'],
            ['Refuse to let you use your own repairer', 'No'],
            ['Apply a higher excess if you go elsewhere', 'Yes, if the policy says so'],
            ['Decline to guarantee work they did not arrange', 'Yes &mdash; we guarantee our own'],
            ['Withhold a courtesy car', 'Yes, if the courtesy car is tied to their network'],
            ['Pay only up to their own assessed cost', 'Yes &mdash; this is the common one'],
         ])),
         'That last row is the one that matters in practice. Rather than refusing outright, the '
         'insurer agrees the repair but authorises it at the rate they pay their own network. If '
         'your chosen bodyshop charges more, you can be asked to cover the gap. Check it before '
         'the car is booked in, not after.',
        ]),
        ('What to say when they push', [
         ('steps', [
            '<strong>Say it plainly.</strong> <span>&ldquo;I am using my own repairer. Please '
            'note that on the claim and send me the authorisation.&rdquo; You do not need to '
            'justify the choice.</span>',
            '<strong>Ask the cost question directly.</strong> <span>&ldquo;What labour rate are '
            'you authorising, and will there be any shortfall for me to pay?&rdquo; Get the '
            'answer in writing or by email.</span>',
            '<strong>Ask what you lose.</strong> <span>Usually the courtesy car and their repair '
            'guarantee. Ask whether your excess changes.</span>',
            '<strong>Give them our details.</strong> <span>They will want the bodyshop name, '
            'address and contact. We deal with the engineer and the estimate from there.</span>',
         ]),
         'If the handler insists it is not allowed, ask them to point you to the clause in your '
         'policy wording that says so. That usually ends the conversation.',
        ]),
        ('Why people come to us instead', [
         'We are not on any insurer&rsquo;s panel, and we are not trying to get on one. That '
         'means nobody has pre-agreed a labour time on your car&rsquo;s behalf. We estimate the '
         'job the way it actually needs doing, argue it with the engineer if we have to, and '
         'guarantee the paint ourselves for a year.',
         'We handle any insurer. We will do the estimate, deal with the engineer&rsquo;s '
         'inspection, raise a supplementary if the strip-down finds more than the photographs '
         'showed, and keep you updated rather than leaving you to chase.',
        ]),
       ],
       [
        ('My insurer says the warranty on my car will be affected. Is that right?',
         'That is a different thing and it is usually overstated. A manufacturer warranty covers '
         'defects in manufacture, not accident damage. Repairing crash damage at an independent '
         'bodyshop does not void it. What can matter is a separate anti-corrosion or paint '
         'warranty on a newer car, which may require the work to be done to a particular '
         'standard &mdash; worth checking if the car is under three years old.'),
        ('Will it slow the claim down?',
         'Usually not by much. The engineer still has to inspect and authorise either way. The '
         'one thing that does add time is the back and forth if the insurer authorises less than '
         'the job takes, which is why we settle the rate before starting.'),
        ('Can I change to you after their garage has already started?',
         'Yes, though it gets messier. The work already done has to be paid for and the car moved. '
         'If the repair has gone wrong, that is a complaint against the insurer and their '
         'repairer, and it is worth putting in writing before you move the car.'),
        ('Do you handle the claim for me?',
         'We deal with the estimate, the engineer and the supplementary. You still make the first '
         'call to report it, because the policy is yours. For non-fault claims we can take more of '
         'it off your hands.'),
       ],
       [('right-to-choose-your-own-bodyshop', 'Your right to choose a bodyshop'),
        ('non-fault-accident-what-to-do', 'Non-fault accident: what to do'),
        ('who-pays-my-excess', 'Who pays my excess'),
        ('how-a-bodywork-insurance-claim-works-step-by-step', 'How a claim works, step by step')],
       key_points=[
        '<strong>No.</strong> You choose who repairs your car. Your insurer cannot overrule that.',
        'The approved list is a <strong>discount arrangement</strong>, not a quality standard.',
        'You may give up <strong>their</strong> repair guarantee, and sometimes a courtesy car.',
        'The real catch: they authorise at <strong>their own labour rate</strong> and leave you '
        'the shortfall. Settle that before the car is booked in.',
       ],
       ),

    _p('category-n-write-off',
       'Category N Write-Off Explained | What It Means | KITH Cars',
       'What a Cat N write-off is, how it differs from Cat S, whether you can keep and repair the '
       'car, what it does to the value, and when repairing is worth it.',
       'Category N Write-Off: What It Actually Means',
       'Insurance &amp; claims &middot; Write-offs',
       'Category N means your insurer decided the repair cost more than the car was worth to '
       'them. It does not mean the car is unsafe, and it does not mean the damage is structural. '
       'Plenty of Cat N cars are back on the road and perfectly sound.',
       [
        ('What the categories mean', [
         'Since October 2017 insurers have used four categories. The first two end the car&rsquo;s '
         'life. The second two do not.',
         ('table', (['Category', 'What it means'], [
            ['A', 'Scrap only. The entire vehicle is crushed, parts included.'],
            ['B', 'The body shell is crushed. Serviceable parts may be removed and reused.'],
            ['S', 'Structurally damaged but repairable. Chassis, crumple zones, suspension mounts.'],
            ['N', 'Not structurally damaged. Repairable. Cosmetic, electrical or mechanical.'],
         ])),
         'N stands for non-structural, not for the severity of the bill. A car with a minor '
         'crumpled wing can be a Cat N if the car was only worth &pound;900 to begin with. A car '
         'with &pound;6,000 of damage might not be written off at all if it is worth &pound;40,000.',
        ]),
        ('Why cheap cars get written off for small damage', [
         'The decision is arithmetic, not engineering. The insurer compares the repair cost plus '
         'any hire and storage against the car&rsquo;s market value less what the salvage is '
         'worth. If repairing costs more, they write it off and pay you the value.',
         'This is why a ten-year-old hatchback with a damaged door, wing and mirror gets written '
         'off while the same damage on a three-year-old car is simply repaired. The damage is '
         'identical. The value either side of it is not.',
        ]),
        ('Can you keep the car?', [
         'Usually, yes. Ask the insurer for a <strong>buy-back</strong>, sometimes called '
         'retaining the salvage. They pay you the car&rsquo;s value less what they would have got '
         'from the salvage firm, and you keep the vehicle.',
         ('steps', [
            '<strong>Say you want to retain it before you accept the settlement.</strong> '
            '<span>Once the car has gone to salvage it is gone. Say it at the first call.</span>',
            '<strong>Get the buy-back figure.</strong> <span>Your settlement drops by roughly '
            'what the salvage was worth. Ask for both numbers.</span>',
            '<strong>Get a proper repair estimate first.</strong> <span>We will quote the real '
            'job. Compare that against what you keep after the deduction.</span>',
            '<strong>Expect the Cat N to be recorded.</strong> <span>It stays on the '
            'vehicle&rsquo;s history permanently. Any HPI check will show it.</span>',
         ]),
        ]),
        ('What it does to the value', [
         'A recorded Cat N typically knocks a meaningful amount off what the car will later sell '
         'for, and the effect is proportionally harsher on cheaper cars. Some buyers will not '
         'consider one at all, and some finance and insurance providers are more awkward about '
         'them.',
         'It is still often worth keeping a Cat N you intend to drive for years. It is rarely '
         'worth keeping one you plan to sell soon, because you take the value hit without getting '
         'the use.',
        ]),
        ('Repairing a Cat N properly', [
         'There is no mandatory inspection before a Cat N goes back on the road, which is exactly '
         'why the standard of repair matters. A Cat N repaired with filler over a crumpled panel '
         'and a mismatched respray is the reason the category has a poor reputation.',
         'We repair them the same way we repair anything else: damaged panels straightened or '
         'replaced, paint matched to the code and blended into the adjacent panels, everything '
         'refitted and the gaps set properly. If the damage touched anything with a sensor '
         'behind it, that gets tested before the car leaves.',
        ]),
       ],
       [
        ('Do I have to tell the DVLA?',
         'For Category N there is no requirement to notify the DVLA and you keep the same V5C. '
         'Category S is different &mdash; that one must be notified and the car is issued a new '
         'V5C. The write-off is recorded against the vehicle either way, so it will show on a '
         'history check.'),
        ('Can I insure a Cat N car?',
         'Yes, though not every insurer will quote and some charge more. It is worth getting a '
         'quote before you commit to the buy-back, so the running cost is in front of you when '
         'you decide.'),
        ('Is a Cat N car safe?',
         'Properly repaired, yes &mdash; by definition the structure was not damaged. The risk is '
         'not the category, it is whether the repair was done properly or patched to look right '
         'in photographs. Get it inspected before you buy one.'),
        ('I think the write-off valuation is too low. Can I argue?',
         'Yes, and people often win. The insurer owes you the market value, not the cheapest '
         'figure in a guide. Send them advertised prices for the same model, age, mileage and '
         'spec from dealers within a sensible distance, and put the challenge in writing.'),
        ('Can you tell me if mine is worth repairing before I decide?',
         'Yes. Bring it in or send photographs and we will estimate it properly. That gives you a '
         'real repair figure to set against the buy-back, instead of guessing.'),
       ],
       [('car-write-off-categories-explained', 'All four write-off categories'),
        ('category-s-write-off', 'Category S explained'),
        ('can-i-keep-my-written-off-car', 'Keeping a written-off car'),
        ('write-off-valuation-too-low-what-to-do', 'Challenging a low valuation')],
       key_points=[
        'N is for <strong>non-structural</strong>. The chassis and crumple zones are intact.',
        'It was written off on <strong>cost against value</strong>, not on safety.',
        'You can usually <strong>buy it back</strong> &mdash; but say so before you accept the '
        'settlement.',
        'The category is recorded <strong>permanently</strong> and will show on any history check.',
       ],
       ),

    _p('who-pays-my-excess',
       'Who Pays My Insurance Excess After an Accident? | KITH Cars',
       'When you pay your excess, when you get it back, and how to recover it after a non-fault '
       'accident. Compulsory and voluntary excess explained.',
       'Who Pays My Excess?',
       'Insurance &amp; claims &middot; Excess',
       'You do, up front, almost every time &mdash; even when the accident was not your fault. '
       'The question that matters is whether you get it back, and on a non-fault claim you '
       'usually should.',
       [
        ('The two halves of your excess', [
         'Your total excess is made of two parts, and people forget the second one until they '
         'claim.',
         ('table', (['Part', 'Who set it', 'Can you change it'], [
            ['Compulsory', 'The insurer, based on the car, your age and history',
             'No &mdash; it comes with the quote'],
            ['Voluntary', 'You, when you bought the policy, to lower the premium',
             'Only at renewal'],
         ])),
         'Both are payable on a claim. If you set a &pound;500 voluntary excess to shave the '
         'premium and the compulsory is &pound;250, you are paying &pound;750 before the insurer '
         'pays anything. That is worth remembering on small jobs.',
        ]),
        ('When you pay it', [
         'In practice the excess is deducted from the settlement, or the bodyshop collects it '
         'from you when you pick the car up. On a repair, the insurer pays us their share and you '
         'pay the excess directly. We will tell you the figure before we start so there is no '
         'surprise at handover.',
        ]),
        ('Getting it back after a non-fault accident', [
         'If the other driver was at fault, their insurer ultimately pays for everything &mdash; '
         'including your excess. Recovering it is normal and expected. It is simply not automatic '
         'or quick.',
         ('steps', [
            '<strong>Pay it and keep the receipt.</strong> <span>The repair should not wait on '
            'the liability argument. Get the car fixed.</span>',
            '<strong>Tell your insurer you want it recovered.</strong> <span>Say it explicitly. '
            'It is part of their claim against the third party, but it is worth stating.</span>',
            '<strong>Expect it to take months, not weeks.</strong> <span>It arrives when '
            'liability settles between the two insurers.</span>',
            '<strong>Chase it.</strong> <span>Excess recovery is the single most common thing '
            'people forget to follow up and quietly never get back.</span>',
         ]),
        ]),
        ('When paying privately beats claiming', [
         'If the repair costs anything close to your excess, claiming makes little sense: you pay '
         'most of the bill yourself, lose some no-claims discount, and carry a declared claim for '
         'years afterwards.',
         'A bumper scuff, a kerbed alloy, a door dent &mdash; these are frequently cheaper to pay '
         'for directly than to claim for. Get a real figure from us first, then compare it against '
         'your excess and what the claim does to your next renewal.',
        ]),
       ],
       [
        ('It was not my fault. Why am I paying anything?',
         'Because your own insurer is settling the repair now and recovering later. If the third '
         'party admits liability early, some insurers will waive it up front &mdash; always ask. '
         'If you claim directly against the other driver&rsquo;s insurer instead, there is no '
         'excess, but you give up the protection of your own policy if the claim goes sour.'),
        ('Does paying the excess mean I admitted fault?',
         'No. It is a term of your own policy, not an admission of anything.'),
        ('Do I pay the excess on a windscreen?',
         'Usually a separate, lower glass excess applies, and it is often lower again for a '
         'repair than a replacement. Check the glass section of your policy, not the main one.'),
        ('Can I pay the excess in instalments?',
         'With us, talk to us. We would rather agree something sensible than have you driving '
         'around with damage.'),
       ],
       [('recovering-your-excess-after-a-non-fault-accident', 'Recovering your excess'),
        ('should-i-claim-or-pay-myself', 'Claim or pay yourself?'),
        ('compulsory-vs-voluntary-excess', 'Compulsory vs voluntary excess'),
        ('non-fault-accident-what-to-do', 'Non-fault accident: what to do')],
       key_points=[
        'You pay it up front &mdash; <strong>even when the accident was not your fault</strong>.',
        'It is <strong>two figures added together</strong>: compulsory plus whatever voluntary '
        'excess you chose to lower the premium.',
        'On a non-fault claim it is <strong>recoverable</strong>, but it takes months and you '
        'have to chase it.',
        'If the repair costs near your excess, <strong>paying us directly is usually '
        'cheaper</strong> than claiming.',
       ],
       ),
]
