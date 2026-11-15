#!/usr/bin/env python3
"""Insurance cluster: the scene, the evidence, and uninsured or untraced drivers.

These are the pages someone reads standing at the roadside or that evening. They are written to
be usable in that state - short imperative steps near the top, detail underneath - rather than as
essays with the instruction buried.

Legal duties are described rather than quoted with section numbers, and the specific figures and
time limits under the MIB agreements are deliberately not stated, because they change and a wrong
number on a published page is worse than no number. Every page points at the real source.
"""

from bw_lib import page, ADVICE_NOTE, CHOICE_NOTE

PAGES = [

    page('what-to-do-at-the-scene-of-an-accident',
         'What to Do at the Scene of an Accident | KITH Cars',
         'Your legal duties after a crash, what to photograph, what never to say, and the one '
         'thing most people forget to get. A checklist you can work through at the roadside.',
         'What to Do at the Scene',
         'Insurance &amp; claims &middot; Fault and liability',
         'Work down this list in order. It takes about five minutes and it decides how the next '
         'six months go.',
         [
          ('The first two minutes', [
           ('steps', [
             '<strong>Stop.</strong> <span>Failing to stop after an accident involving injury or '
             'damage to another person&rsquo;s vehicle or property is a criminal offence, not a '
             'civil one.</span>',
             '<strong>Hazards on, engine off.</strong> <span>If the car is in a live lane and '
             'anyone can get out safely, get out and behind a barrier.</span>',
             '<strong>Check for injuries.</strong> <span>Yours, your passengers&rsquo;, theirs. '
             'Call 999 if anyone is hurt, if the road is blocked, or if anyone appears to be '
             'under the influence.</span>',
             '<strong>Do not move the vehicles yet.</strong> <span>Unless they are dangerous '
             'where they are. Final positions are evidence and photographs of them settle '
             'arguments that nothing else will.</span>',
           ]),
          ]),
          ('What you are legally required to do', [
           'The duty after an accident involving injury or damage to another vehicle, property, '
           'or certain animals is to stop and give your name and address, and the name and '
           'address of the vehicle&rsquo;s owner along with its registration, to anyone with '
           'reasonable grounds to ask.',
           'If you do not exchange those details at the scene &mdash; which includes the case '
           'where there is nobody there to exchange them with &mdash; the accident must be '
           'reported to the police as soon as reasonably practicable, and in any event within '
           'twenty-four hours. Reporting it later than that, or not at all, is itself an offence.',
           ('note', 'Reporting to the police and claiming on insurance are completely separate '
                    'things. Reporting does not start a claim and claiming does not report it.'),
          ]),
          ('What to photograph', [
           'Photographs settle liability more often than accounts do, because two honest people '
           'remember the same collision differently. Take more than you think you need.',
           ['<strong>Wide shot showing both vehicles where they stopped.</strong> This is the '
            'most valuable photograph and the one people skip because they go straight to the '
            'damage.',
            '<strong>Both registration plates</strong>, clearly readable.',
            '<strong>The damage on both cars</strong>, close up and from a few feet back.',
            '<strong>The road layout</strong> &mdash; markings, give way lines, signals, signs, '
            'the junction from the direction you approached.',
            '<strong>Skid marks, debris and broken glass</strong>, which show where the impact '
            'actually happened.',
            '<strong>Conditions</strong> &mdash; wet road, low sun, darkness, obstructed view.',
            '<strong>The other driver&rsquo;s documents</strong> if they will let you '
            'photograph them, rather than writing details down wrongly.'],
          ]),
          ('What to get from the other driver', [
           ('table', (['Get', 'Why'], [
             ['Full name and address', 'Legal requirement, and you will need it to claim'],
             ['Registration number', 'Photograph it rather than writing it'],
             ['Insurer and policy number', 'Speeds everything up enormously'],
             ['Phone number', 'Not a legal requirement, but ask'],
             ['Who owns the car', 'Often not the driver &mdash; worth establishing at the scene'],
           ])),
           'If they will not give details, do not escalate it. Photograph the car, the plate and '
           'the person if you safely can, note the time and place, and report it to the police.',
          ]),
          ('The thing most people forget', [
           'A witness. It is the single most valuable thing available at the scene and the thing '
           'most reliably not collected, because everyone is focused on the cars.',
           'Look around. Other drivers who stopped, pedestrians, someone at a bus stop, a shop '
           'with a doorway onto the street. A name and a mobile number is enough. An independent '
           'witness turns a disputed 50/50 into a settled claim more often than any other piece '
           'of evidence.',
           'Also look up and around for cameras: a dashcam in a car behind, a shop CCTV, a bus '
           'camera, a doorbell camera on a house opposite. Footage is usually overwritten within '
           'days, so asking the same day matters.',
          ]),
          ('What never to say', [
           'Do not admit liability, apologise in a way that sounds like admitting it, or agree a '
           'version of events while you are still shaking.',
           'This is not advice to be dishonest. It is that you do not yet know what happened: '
           'whether their brake lights worked, how fast they were going, whether a third vehicle '
           'was involved, whether their tyres were legal. Be civil and say nothing about fault. '
           'Admitting it can also breach a condition of your own policy.',
           ('note', ADVICE_NOTE),
          ]),
         ],
         [('Do I have to call the police?',
           'Only if someone is injured, the road is blocked or obstructed, you suspect an '
           'offence, or details were not exchanged. Otherwise you do not, though you can report '
           'it for a reference number.'),
          ('The other driver wants to settle in cash. Should I?',
           'Take their details anyway and get the damage estimated before agreeing anything. A '
           'scuffed bumper can have a broken crash bar behind it, and once you have taken cash '
           'you have no route back.'),
          ('What if nobody was around and I hit a parked car?',
           'Leave a note with your details, and report it to the police within twenty-four hours. '
           'A note alone does not discharge the duty if you did not exchange details in person.'),
          ('I feel fine. Do I need to see a doctor?',
           'Neck and back injuries routinely appear a day or two later. If anything hurts the '
           'next morning, see someone and have it recorded.'),
          ('When should I tell my insurer?',
           'As soon as you reasonably can, even if you do not intend to claim. Most policies '
           'require notification of any incident, and late notification is one of the few things '
           'that genuinely damages a claim.')],
         [('photos-to-take-after-a-crash', 'Photographs that actually help'),
          ('non-fault-accident-what-to-do', 'Non-fault accident: what to do'),
          ('fault-accident-what-happens-next', 'If it was your fault'),
          ('dashcam-footage-for-a-claim', 'Using dashcam footage')],
         key_points=[
          '<strong>Stop</strong> &mdash; not stopping is a criminal offence.',
          'Photograph the <strong>wide shot of final positions</strong> before anything moves.',
          'Get a <strong>witness name and number</strong>. Almost nobody does, and it is the most '
          'valuable thing there.',
          '<strong>Say nothing about fault.</strong> Admitting it can breach your policy.',
         ]),

    page('photos-to-take-after-a-crash',
         'What Photos to Take After a Car Accident | KITH Cars',
         'The fifteen photographs that decide a liability dispute, in the order to take them, '
         'and the three most people miss.',
         'The Photographs That Actually Help',
         'Insurance &amp; claims &middot; Fault and liability',
         'Most people take four photographs of the dent and none of anything that decides '
         'liability. Here is the full list, in the order to take it, with the three that matter '
         'most marked.',
         [
          ('Before anything moves', [
           'These are the ones you cannot go back for, and they are the ones that settle '
           'arguments. Take them first, even though the instinct is to photograph the damage.',
           ('steps', [
             '<strong>Wide shot, both cars, from behind yours.</strong> <span>The single most '
             'useful photograph there is. Show the gap between the vehicles and their angle to '
             'each other.</span>',
             '<strong>Wide shot from the other direction.</strong> <span>The same scene from the '
             'opposite approach, so neither version of events can rely on a blind spot.</span>',
             '<strong>Straight down the road from your approach.</strong> <span>What you could '
             'actually see coming up to it.</span>',
             '<strong>The same from their approach.</strong> <span>What they could see.</span>',
           ]),
          ]),
          ('The damage', [
           ['Each damaged area close up, in focus, with something for scale if it is small.',
            'The same areas from six feet back, so the position on the car is clear.',
            '<strong>Their</strong> damage as well as yours. This protects you against a claim '
            'for damage that was already on their car.',
            'Any damage on either car that was there before, photographed deliberately so it is '
            'on record as pre-existing.'],
          ]),
          ('The context, which is where claims are won', [
           ('table', (['Photograph', 'What it proves'], [
             ['Road markings and give way lines', 'Who had priority'],
             ['Traffic signals and signs', 'What the rules were at that spot'],
             ['Skid marks and debris', 'Where the impact actually happened'],
             ['Broken glass and plastic on the road', 'Point of impact, not final resting place'],
             ['Weather and light', 'Wet road, low sun, darkness'],
             ['Obstructions', 'A parked van, a hedge, a skip blocking the view'],
           ])),
          ]),
          ('The three most people miss', [
           '<strong>The wide shot before the cars move.</strong> Everyone photographs the dent. '
           'Almost nobody photographs where the two cars came to rest relative to the lane '
           'markings, and that is the photograph an engineer or a solicitor actually wants.',
           '<strong>The other car&rsquo;s tyres.</strong> Tread depth and condition. If their '
           'tyres were illegal, that is relevant to liability and it will be fixed within the '
           'week.',
           '<strong>Anything that might have a camera.</strong> A shop frontage, a bus, a car '
           'behind with a visible dashcam, a house with a doorbell camera. Photograph the '
           'premises so you can ask later. Footage is usually overwritten in days.',
          ]),
          ('Practical points', [
           ['Take far more than you think you need. Storage is free, a second visit is not '
            'possible.',
            'Keep the originals. Do not crop, rotate or filter them &mdash; the file metadata '
            'carries the time and often the location, and that has value.',
            'Back them up that evening. Phones get lost and claims run for months.',
            'If it is dark, use the flash and take extra. A grainy photograph of a road layout '
            'still shows the road layout.',
            'Photograph the other driver&rsquo;s documents rather than copying details by hand. '
            'Transcription errors cause real delays.'],
           ('note', 'If you have a dashcam, save the file that evening. Most overwrite on a loop '
                    'and the footage you need will be gone within a day or two of normal '
                    'driving.'),
          ]),
         ],
         [('Can I take photos of the other driver?',
           'You can photograph their vehicle and documents. Photographing the person is more '
           'sensitive &mdash; reasonable if they are refusing details or appear impaired, and '
           'not worth a confrontation otherwise.'),
          ('Do photos actually change liability decisions?',
           'Frequently, yes. Where the only evidence is two conflicting accounts, insurers tend '
           'toward a split. Photographs of final positions and road markings are what breaks '
           'that.'),
          ('What if I only remembered afterwards?',
           'Go back and photograph the location anyway &mdash; markings, signs, sight lines. It '
           'is less good than the scene but much better than nothing, and it is still '
           'contemporaneous.'),
          ('Should I send them to my insurer straight away?',
           'Send them, and keep your originals. Never send your only copy of anything.')],
         [('what-to-do-at-the-scene-of-an-accident', 'What to do at the scene'),
          ('dashcam-footage-for-a-claim', 'Using dashcam footage'),
          ('witness-details-why-they-matter', 'Why witnesses matter'),
          ('split-liability-explained', 'Split liability explained')],
         key_points=[
          'The <strong>wide shot before the cars move</strong> is the one that matters.',
          'Photograph <strong>their damage too</strong> &mdash; it protects you from a padded '
          'claim.',
          'Road markings and signals prove <strong>who had priority</strong>.',
          '<strong>Save your dashcam file that evening.</strong> Most overwrite within days.',
         ]),

    page('dashcam-footage-for-a-claim',
         'Using Dashcam Footage for an Insurance Claim | KITH Cars',
         'How to save and submit dashcam footage, whether it is admissible, when it helps and '
         'when it hurts, and the mistake that loses it.',
         'Using Dashcam Footage',
         'Insurance &amp; claims &middot; Fault and liability',
         'Dashcam footage is the most effective thing there is for settling liability, and most '
         'of it is lost within forty-eight hours because nobody saved the file.',
         [
          ('Save it tonight', [
           'Almost every dashcam records on a loop and overwrites the oldest footage once the '
           'card is full. Depending on card size and quality settings, that can be a few hours '
           'of driving.',
           ('steps', [
             '<strong>Stop using that card.</strong> <span>Ideally take it out of the camera '
             'before you drive home.</span>',
             '<strong>Copy the file to a computer.</strong> <span>Not just to your phone. Two '
             'copies in two places.</span>',
             '<strong>Save more than the impact.</strong> <span>Several minutes before and '
             'after. Context matters &mdash; how they were driving for the previous mile is '
             'often the point.</span>',
             '<strong>Do not edit, trim or compress it.</strong> <span>Submit the original file '
             'with its metadata intact. An edited clip invites an argument about what was cut '
             'out.</span>',
             '<strong>Note the camera&rsquo;s clock accuracy.</strong> <span>Many run minutes or '
             'hours out. Say so rather than letting it be found.</span>',
           ]),
          ]),
          ('Is it admissible?', [
           'Yes. Insurers accept dashcam footage routinely and courts accept it as evidence. '
           'There is no special rule against it and no requirement for a particular camera or '
           'format.',
           'What is sometimes challenged is whether a clip is complete and unaltered, which is '
           'the reason for submitting the original file rather than something you trimmed.',
          ]),
          ('When it helps most', [
           ['Disputed liability with no witness &mdash; the single best use.',
            'Being pushed toward a 50/50 you do not accept.',
            'The other driver&rsquo;s account changing between the scene and the claim.',
            'A staged or induced accident, where the braking pattern in front of you is the '
            'evidence.',
            'Hit and run, where the plate may be readable even if the car is gone.'],
          ]),
          ('When it does not help you', [
           'Worth being straight about: footage shows what you were doing as well as what they '
           'were. If you were over the limit, following too close, or looking at your phone, the '
           'camera recorded that too.',
           'You are not obliged to volunteer footage that harms you. If it is requested as part '
           'of a claim or proceedings, that is different, and deleting it at that point is a '
           'serious matter. If your own footage genuinely goes against you, that is worth taking '
           'advice on rather than deciding alone.',
           ('note', ADVICE_NOTE),
          ]),
          ('Getting someone else&rsquo;s footage', [
           'Other people&rsquo;s cameras are often the answer, and they are time-limited.',
           ['Ask any driver who stopped whether they have a dashcam, there and then.',
            'Note shops, offices and houses facing the scene, and ask the same day.',
            'Buses and taxis carry cameras. Note the fleet number and route.',
            'Most CCTV is overwritten within a short period, so a polite request on day one is '
            'worth far more than a formal one on day ten.'],
           'They are not obliged to hand it over, and data protection rules affect what they can '
           'share, but a lot of people will help if asked quickly and politely.',
          ]),
         ],
         [('Does having a dashcam lower my premium?',
           'Some insurers offer a discount, many do not. It is worth asking at renewal rather '
           'than assuming.'),
          ('My camera clock was wrong. Does that ruin it?',
           'No. Say so up front and explain the offset. Footage with an acknowledged clock error '
           'is far better received than footage where the error is discovered.'),
          ('Can I post it online?',
           'Think carefully. It may identify people, it can prejudice a claim, and insurers and '
           'solicitors take a dim view of evidence being published while a matter is live.'),
          ('The footage shows the other driver on their phone.',
           'Then say so explicitly when you submit it, with the timestamp of that moment. Do not '
           'assume an adjuster will watch every minute and spot it.')],
         [('photos-to-take-after-a-crash', 'Photographs that actually help'),
          ('what-to-do-at-the-scene-of-an-accident', 'What to do at the scene'),
          ('split-liability-explained', 'Split liability explained'),
          ('disputing-a-fault-decision', 'Disputing a fault decision')],
         key_points=[
          '<strong>Save the file tonight.</strong> Most cameras overwrite within days.',
          'Submit the <strong>original</strong>, unedited, with several minutes either side.',
          'Routinely accepted by insurers and admissible in court.',
          'Other people&rsquo;s cameras are <strong>time-limited</strong> &mdash; ask the same '
          'day.',
         ]),

    page('witness-details-why-they-matter',
         'Why Witness Details Matter After an Accident | KITH Cars',
         'What an independent witness is worth in a liability dispute, what to ask them for, and '
         'why almost nobody collects this.',
         'Why a Witness Changes Everything',
         'Insurance &amp; claims &middot; Fault and liability',
         'A name and a mobile number, taken in thirty seconds at the scene, is worth more than '
         'everything else you do that day. It is also the thing almost nobody gets.',
         [
          ('What a witness actually does', [
           'Most disputed claims come down to two accounts that cannot both be true, given by '
           'two people who each believe theirs. Neither is lying. Memory under stress is simply '
           'unreliable, and insurers know it.',
           'Faced with two irreconcilable accounts and nothing else, insurers frequently settle '
           'at 50/50 &mdash; not because that is what happened, but because establishing what '
           'happened costs more than conceding half. An independent witness breaks that '
           'deadlock, because they have no stake in the outcome.',
          ]),
          ('Who counts', [
           ('table', (['Witness', 'Weight'], [
             ['A stranger who stopped', 'Highest &mdash; genuinely independent'],
             ['Another driver who saw it', 'High, and often has a dashcam too'],
             ['A pedestrian or shopkeeper', 'High, and easy to find again'],
             ['Your passenger', 'Lower &mdash; not independent, but still worth recording'],
             ['The other driver&rsquo;s passenger', 'Worth noting they exist'],
           ])),
           'Your own passenger is not worthless. They are simply discounted as an interested '
           'party, so take their account too and do not rely on it alone.',
          ]),
          ('What to ask for', [
           ('steps', [
             '<strong>Name and mobile number.</strong> <span>That is the minimum and it is '
             'enough.</span>',
             '<strong>Where they were standing or driving.</strong> <span>It establishes what '
             'they could actually see.</span>',
             '<strong>One sentence on what they saw.</strong> <span>Write it down there and '
             'then, in their words.</span>',
             '<strong>Whether they have a dashcam.</strong> <span>Ask explicitly. People do not '
             'volunteer it.</span>',
             '<strong>Whether they are willing to be contacted.</strong> <span>Most are. Some '
             'will give a number and prefer not to be involved further, which is still '
             'useful.</span>',
           ]),
          ]),
          ('Why people do not do it', [
           'Because the minutes after a collision are taken up with the cars, the other driver, '
           'and the adrenaline. By the time anyone thinks about witnesses, the people who saw it '
           'have driven on or walked away.',
           'The fix is simply to do it first, before you start photographing damage. Look around '
           'and ask, out loud: &ldquo;Did anyone see that?&rdquo; Thirty seconds, and it is the '
           'highest-value thing available to you at that moment.',
           ('note', 'If you did not get anyone at the scene, it is still worth going back. A '
                    'shop or a regular commuter may have seen it, and a note left at a nearby '
                    'business sometimes finds someone.'),
          ]),
         ],
         [('Will the witness have to go to court?',
           'Almost certainly not. The overwhelming majority of motor claims settle between '
           'insurers on the paperwork. A written statement is usually the end of their '
           'involvement.'),
          ('They gave a number but now will not answer.',
           'It happens. Pass the details to your insurer anyway &mdash; a letter from an insurer '
           'gets answered more often than a call from a stranger.'),
          ('Does a witness help if liability is already admitted?',
           'Not really, and you do not need one then. Keep the details until liability is '
           'confirmed in writing, though.'),
          ('Can my partner be a witness if they were in the car?',
           'They can give an account and it should be recorded. It carries less weight because '
           'they are not independent, which is why an unconnected witness matters so much.')],
         [('what-to-do-at-the-scene-of-an-accident', 'What to do at the scene'),
          ('split-liability-explained', 'Split liability explained'),
          ('photos-to-take-after-a-crash', 'Photographs that actually help'),
          ('who-decides-who-is-at-fault', 'Who decides who is at fault')],
         key_points=[
          'Two honest accounts that conflict usually settle at <strong>50/50</strong>.',
          'An independent witness <strong>breaks that deadlock</strong>.',
          'Ask <strong>first</strong>, before photographing damage &mdash; witnesses leave.',
          'Always ask whether they have a <strong>dashcam</strong>. People do not volunteer it.',
         ]),

    page('hit-by-an-uninsured-driver',
         'Hit by an Uninsured Driver: What to Do | KITH Cars',
         'How to claim when the other driver has no insurance, what the Motor Insurers Bureau '
         'does, what it costs you, and how to check whether they were insured at all.',
         'Hit by an Uninsured Driver',
         'Insurance &amp; claims &middot; Uninsured and untraced',
         'There is a route, and it works, but it is slower than a normal claim and it can cost '
         'you more than it should. Knowing which of the three options applies to you is the '
         'first thing to sort out.',
         [
          ('Check first whether they really were uninsured', [
           'People say they are insured when they are not, and occasionally say they are not when '
           'they are &mdash; usually because they are driving someone else&rsquo;s car and do not '
           'understand the policy.',
           'The askMID database will tell you whether a vehicle was insured, and it is free for '
           'the registered keeper or a party to an accident. Do that before assuming you are in '
           'uninsured-driver territory, because a normal claim is far better for you than the '
           'alternative.',
          ]),
          ('Your three options', [
           ('table', (['Route', 'Works when', 'Downside'], [
             ['Your own comprehensive policy', 'You have comprehensive cover',
              'You pay your excess, and your no-claims may suffer'],
             ['The Motor Insurers Bureau', 'The driver is identified but uninsured',
              'Slower; conditions apply'],
             ['Claim against the driver personally', 'They have money and will pay',
              'Usually they do not, and you are enforcing it yourself'],
           ])),
           'Most people use the first if they have comprehensive cover and the second if they do '
           'not, or where their insurer declines.',
          ]),
          ('What the MIB is', [
           'The Motor Insurers&rsquo; Bureau is funded by a levy on every insurance policy in the '
           'country, which means by every insured driver including you. It exists to compensate '
           'victims of uninsured and untraced drivers.',
           'It is not an insurer and it is not a regulator. It is a compensation body of last '
           'resort, and its agreements carry conditions &mdash; notably about reporting to the '
           'police, cooperating with their investigation, and time limits for bringing a claim. '
           'Those conditions and the applicable excesses change, so take them from the MIB '
           'directly rather than from any third party.',
           ('note', 'Report it to the police. Driving without insurance is an offence, and MIB '
                    'claims normally require that the matter has been reported. This is the step '
                    'most often missed and it is the one that causes claims to be rejected.'),
          ]),
          ('The no-claims problem', [
           'This is the part that feels most unfair. If you claim on your own policy and your '
           'insurer cannot recover from anyone &mdash; because the other driver has no insurer '
           'and no money &mdash; the claim sits on your record as an unrecovered outlay.',
           'In practice that often means your no-claims discount is affected and your premium '
           'rises, despite you having done nothing wrong. Ask your insurer directly how they '
           'will record it, and whether they will pursue the driver. Some do, some do not.',
           'It is also worth asking whether they will waive your excess given the circumstances. '
           'Some will. It costs one phone call to find out.',
          ]),
          ('What to do, in order', [
           ('steps', [
             '<strong>Get everything at the scene.</strong> <span>Name, address, registration, '
             'photographs, witnesses. All of it matters more than usual because there is no '
             'insurer to fill the gaps.</span>',
             '<strong>Report it to the police.</strong> <span>Get the reference number and keep '
             'it.</span>',
             '<strong>Check askMID.</strong> <span>Before you accept they were uninsured.</span>',
             '<strong>Tell your own insurer.</strong> <span>Even if you do not intend to claim '
             'through them.</span>',
             '<strong>Go to the MIB if that is the route.</strong> <span>Direct, and read their '
             'conditions and time limits yourself.</span>',
             '<strong>Keep every receipt.</strong> <span>Recovery, storage, hire, loss of '
             'earnings.</span>',
           ]),
           ('note', CHOICE_NOTE),
          ]),
         ],
         [('Will I get my excess back?',
           'Usually not from the other driver, because if they could pay they would have been '
           'insured. Ask your own insurer to waive it, and ask whether they will pursue recovery.'),
          ('How long does an MIB claim take?',
           'Longer than a normal claim &mdash; months rather than weeks. Keep every document and '
           'expect to chase.'),
          ('They gave me details that turned out to be false.',
           'That is a different situation and a police matter. The MIB untraced driver route may '
           'apply if the driver cannot be identified at all.'),
          ('Can I still choose my own repairer?',
           'Yes. However the repair is funded, where it is done is your choice.'),
          ('My insurer says I have to claim through them first.',
           'That is usually right if you have comprehensive cover, and it is normally the faster '
           'route. The MIB is there for where that is not available.')],
         [('hit-and-run-what-to-do', 'Hit and run'),
          ('non-fault-accident-what-to-do', 'Non-fault accident: what to do'),
          ('what-to-do-at-the-scene-of-an-accident', 'What to do at the scene'),
          ('will-a-non-fault-claim-affect-my-no-claims', 'Claims and your no-claims')],
         key_points=[
          '<strong>Check askMID first</strong> &mdash; a normal claim is much better for you.',
          '<strong>Report it to the police.</strong> MIB claims normally require it, and this '
          'is the step most often missed.',
          'Your no-claims <strong>can suffer</strong> even though you did nothing wrong.',
          'Ask your insurer to <strong>waive the excess</strong>. Some will.',
         ]),

    page('hit-and-run-what-to-do',
         'Hit and Run: What to Do if the Driver Drove Off | KITH Cars',
         'What to do when the other driver leaves the scene, how untraced driver claims work, '
         'and the evidence that matters most in the first twenty-four hours.',
         'They Drove Off. What Now?',
         'Insurance &amp; claims &middot; Uninsured and untraced',
         'The first twenty-four hours decide this one. Cameras get overwritten, witnesses '
         'disperse, and the reporting window is short.',
         [
          ('The first hour', [
           ('steps', [
             '<strong>Write down everything you can remember, now.</strong> <span>Make, model, '
             'colour, any part of the plate, the direction they went, anything about the driver. '
             'Memory degrades fast and the first account is the most accurate one you will '
             'ever give.</span>',
             '<strong>Ask everyone around.</strong> <span>Someone may have the plate. Get names '
             'and numbers.</span>',
             '<strong>Look for cameras immediately.</strong> <span>Shops, houses, buses, parked '
             'cars with dashcams. Note the addresses so you can ask today.</span>',
             '<strong>Photograph everything.</strong> <span>Your damage, the scene, any debris '
             'they left &mdash; a broken indicator lens or a piece of trim can identify a '
             'vehicle.</span>',
             '<strong>Report it to the police.</strong> <span>Failing to stop is an offence, and '
             'you need the reference number for any claim.</span>',
           ]),
          ]),
          ('Why the clock matters so much', [
           'Everything that could identify the driver is on a timer. CCTV is commonly overwritten '
           'within days. Dashcam loops are measured in hours. People who saw it will have '
           'forgotten the detail by the weekend.',
           'A polite request on the same day gets footage. A formal request two weeks later gets '
           'an apology. If you do only one thing beyond reporting it, knock on the doors '
           'overlooking the scene today.',
          ]),
          ('If the driver is never identified', [
           'The Motor Insurers&rsquo; Bureau operates a route for untraced drivers as well as '
           'uninsured ones. It is funded by a levy on every insurance policy, including yours.',
           'The untraced route carries its own conditions, time limits and excess arrangements, '
           'and they differ from the uninsured route. They also change, so take them from the MIB '
           'directly rather than from anyone else &mdash; including us.',
           ('note', 'Reporting to the police is normally a condition. Do it even if you think '
                    'nothing will come of it, and keep the reference number.'),
          ]),
          ('Claiming on your own policy instead', [
           'If you have comprehensive cover this is usually faster, and for many people it is the '
           'right answer despite the cost.',
           ('table', (['', 'What happens'], [
             ['Your excess', 'Payable, and with nobody to recover from, usually not returned'],
             ['Your no-claims', 'Often affected, because nothing is recovered'],
             ['Speed', 'Much faster than an untraced claim'],
             ['Certainty', 'High &mdash; your own insurer, your own policy'],
           ])),
           'It is worth asking whether your policy treats a reported hit and run differently. '
           'Some protect no-claims where there is a police reference. Most do not, but ask.',
          ]),
          ('Hit while parked', [
           'The most common version of this, and the most frustrating, because there is no '
           'account of what happened at all.',
           'Check for a note under the wiper before anything else. Then look at what is around '
           'you: in a car park, there is usually CCTV and usually a time-stamped record of which '
           'vehicles were present. Ask the operator the same day and ask in writing as well, so '
           'there is a record of the request before the footage is overwritten.',
          ]),
         ],
         [('Is it worth reporting if I have no plate?',
           'Yes. Debris, CCTV and other reports can connect it later, and the reference number is '
           'required for most claim routes.'),
          ('Someone gave me a partial plate. Useful?',
           'Very. Combined with make, model, colour and location, a partial plate is often enough '
           'for the police to identify a vehicle.'),
          ('Will my insurance go up for a hit and run I did not cause?',
           'It can, because there is nobody to recover from. Ask how it will be recorded and '
           'whether a police reference changes anything.'),
          ('How long do I have to claim through the MIB?',
           'There are time limits and they differ between the uninsured and untraced routes. '
           'Check them with the MIB directly and do not rely on a second-hand figure.')],
         [('hit-by-an-uninsured-driver', 'Hit by an uninsured driver'),
          ('what-to-do-at-the-scene-of-an-accident', 'What to do at the scene'),
          ('dashcam-footage-for-a-claim', 'Using dashcam footage'),
          ('vandalism-claim-guide', 'Vandalism claims')],
         key_points=[
          '<strong>Write down everything now</strong> &mdash; your first account is your best '
          'one.',
          '<strong>Knock on doors today.</strong> CCTV is overwritten within days.',
          '<strong>Report it to the police</strong> and keep the reference.',
          'Hit while parked? <strong>Ask the car park operator in writing, the same day.</strong>',
         ]),
]
