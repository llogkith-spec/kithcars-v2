#!/usr/bin/env python3
"""The repair process cluster: what actually happens to the car, in order.

This is the half of the request that is not about insurers - "the whole process of how things
work and the steps". Written from the workshop outward rather than from the claim inward, so it
reads as someone explaining their own trade rather than as more claims guidance.

The commercial point of this cluster is that it is the honest answer to "why is one quote half
the price of another". Nearly every corner that can be cut in bodywork is invisible at handover
and obvious a year later, and describing the work properly is the only way to show the
difference without rubbishing anyone.
"""

from bw_lib import page, HUB_PROCESS, CHOICE_NOTE

PAGES = [

    page('bodywork-repair-process',
         'The Bodywork Repair Process, Step by Step | KITH Cars',
         'What actually happens to your car in a bodyshop: estimate, strip-down, metalwork, '
         'filler, primer, paint, bake, polish, refit and checks. Every stage and why it matters.',
         'What Actually Happens to Your Car',
         'The repair process',
         'Ten stages, and the ones that decide whether the repair is still invisible in two '
         'years are mostly the ones you never see.',
         [
          ('The ten stages', [
           ('steps', [
             '<strong>Estimate.</strong> <span>The damage is assessed and written up with the '
             'method, the parts and the labour times. This is also where repair against replace '
             'is decided.</span>',
             '<strong>Strip-down.</strong> <span>Panels, trim, lights and anything electrical '
             'come off. This is where hidden damage appears and where the estimate sometimes '
             'changes.</span>',
             '<strong>Metalwork.</strong> <span>The panel is straightened, or a replacement is '
             'fitted and the gaps set. Done in stages, because metal forced back too fast never '
             'sits flat again.</span>',
             '<strong>Filler and flatting.</strong> <span>The small difference the metalwork '
             'could not recover is filled and flatted level. Thin, over sound metal.</span>',
             '<strong>Primer.</strong> <span>Sealing the repair and giving the colour something '
             'consistent to sit on. Flatted again once it has cured.</span>',
             '<strong>Masking.</strong> <span>Everything that is not being painted is covered, '
             'and the blend areas on the neighbouring panels are prepared.</span>',
             '<strong>Colour.</strong> <span>Mixed to your paint code, sprayed in coats, and '
             'faded out into the adjacent panels rather than stopped at the shut line.</span>',
             '<strong>Lacquer and bake.</strong> <span>Clear coat over the whole area, then baked '
             'so it cures properly. This cannot be rushed and it is why bodywork takes '
             'days.</span>',
             '<strong>Flatting and polishing.</strong> <span>Any texture in the fresh lacquer is '
             'flatted out and the panel polished to match the finish of the rest of the '
             'car.</span>',
             '<strong>Refit and check.</strong> <span>Everything back on, gaps set, electrics '
             'tested, sensors checked and recalibrated where the job needs it.</span>',
           ]),
          ]),
          ('Where the time goes, and why it cannot be compressed', [
           'People are often surprised that a day of work takes three days. Most of the '
           'difference is curing. Filler, primer and lacquer each need time to harden before the '
           'next stage can touch them, and a repair pushed through faster than the materials '
           'allow shrinks afterwards.',
           'That is what causes a repair to look perfect at handover and show a faint outline of '
           'the repair area a few months later. The shape was right; the materials had not '
           'finished moving.',
           ('table', (['Stage', 'Hands-on', 'Waiting'], [
             ['Strip-down', 'Hours', '&mdash;'],
             ['Metalwork', 'Hours to days', '&mdash;'],
             ['Filler and primer', 'Hours', 'Cure time between coats'],
             ['Paint and lacquer', 'Hours', 'Bake and cure'],
             ['Polish and refit', 'Hours', '&mdash;'],
           ])),
          ]),
          ('The corners that get cut, and how to spot them', [
           'Almost everything that separates a good repair from a cheap one is invisible on the '
           'day you collect the car.',
           ['<strong>Not blending.</strong> Paint stopped at the shut line instead of faded into '
            'the next panel. Looks fine indoors, shows as two shades in daylight.',
            '<strong>Filler instead of metalwork.</strong> Quicker, and it cracks along the edges '
            'as the panel flexes.',
            '<strong>Skipping corrosion protection.</strong> Cutting and welding destroys the '
            'factory coatings. If they are not rebuilt, it rusts from the inside out.',
            '<strong>Masking glass instead of removing it.</strong> Leaves a paint edge at the '
            'rubber that shows the moment the seal moves.',
            '<strong>Not recalibrating sensors.</strong> Nothing visible at all, which is '
            'precisely the problem.'],
           ('note', 'If you are comparing two quotes with a big gap between them, the useful '
                    'question is not "why are you more expensive". It is "what is included that '
                    'the other one has not listed". Ask both.'),
          ]),
          ('What we do differently, and what we do not', [
           'We blend into the neighbouring panels as standard and it is not a separate line on '
           'the estimate. We photograph strip-down before anything moves. We guarantee paint for '
           'a year in writing.',
           'We do not do paintless dent removal, so every dent we repair is straightened and then '
           'painted. On the dents PDR can fix, a PDR specialist will be cheaper than us, and we '
           'would rather say that than quote and then find a reason it cannot be done.',
           ('note', CHOICE_NOTE),
          ]),
         ],
         [('How long will my car be off the road?',
           'A localised scuff repair is often same or next day. A panel off, painted and refitted '
           'is two to three days. Multiple panels, or anything structural, is longer and we will '
           'tell you the real figure rather than an optimistic one.'),
          ('Can I see the car part way through?',
           'Yes. Ask when you book it in and we will arrange it. We would rather you saw the '
           'strip-down than wondered about it.'),
          ('Do you use genuine parts?',
           'If that is what you want and the insurer authorises it. Where they will only '
           'authorise matching-quality equivalents, you can pay the difference and we will show '
           'you both figures.'),
          ('What happens if you find more damage?',
           'We stop, photograph it, and tell you before doing anything. On a claim that means a '
           'supplementary to the insurer. Paying privately, it means a revised figure agreed with '
           'you first. Either way you are not presented with a bill you did not expect.')],
         [('what-happens-at-strip-down', 'What strip-down finds'),
          ('paint-colour-matching-explained', 'How paint matching works'),
          ('paint-blending-explained', 'Why we blend into the next panel'),
          ('how-long-does-bodywork-take', 'How long bodywork takes')],
         key_points=[
          'Ten stages, and <strong>most of the time is curing</strong>, not working.',
          'The corners that get cut are <strong>invisible at handover</strong>.',
          'Blending into the neighbouring panels is <strong>included, never an extra</strong>.',
          'We do not do paintless dent removal &mdash; <strong>every dent gets painted</strong>.',
         ],
         hub=HUB_PROCESS, category='process', service_type='Vehicle body repair', note=None),

    page('paint-colour-matching-explained',
         'How Car Paint Colour Matching Works | KITH Cars',
         'Why your paint code is only the starting point, what a spray-out card is, why two cars '
         'with the same code look different, and how a match is actually achieved.',
         'How Paint Colour Matching Actually Works',
         'The repair process &middot; Paint',
         'Your paint code gets us close and almost never gets us right. Every car on the road is '
         'a slightly different colour from the one it left the factory, and matching the code '
         'alone is how you end up with a repair that is visibly newer than the car.',
         [
          ('Why the code is not enough', [
           'The code tells us the formula the manufacturer used. It does not tell us what '
           'happened to your car afterwards, and three things always have.',
           ['<strong>Sun.</strong> Ultraviolet light fades every paint, unevenly. The roof and '
            'bonnet have had more of it than the lower doors.',
            '<strong>Factory variation.</strong> The same code sprayed at two plants, or in two '
            'batches, is not identical to begin with. Manufacturers publish variant formulas for '
            'exactly this reason.',
            '<strong>Previous repairs.</strong> If a panel has been painted before, it is '
            'matching somebody else&rsquo;s interpretation of the code rather than the factory.'],
          ]),
          ('What we actually do', [
           ('steps', [
             '<strong>Read the code from the car.</strong> <span>Not from the model year. The '
             'plate is usually in the door shut, under the bonnet or in the boot.</span>',
             '<strong>Pull the variants.</strong> <span>Most codes have several published '
             'variants, sometimes a dozen, covering factory and batch differences.</span>',
             '<strong>Spray out test cards.</strong> <span>The likely variants are sprayed onto '
             'cards, lacquered and dried, because wet paint is not the colour it will '
             'be.</span>',
             '<strong>Compare against the car, in daylight.</strong> <span>Held against the '
             'actual panel, outside. Workshop lighting lies, and metallics lie worse than '
             'anything.</span>',
             '<strong>Adjust if nothing matches.</strong> <span>The mix is tinted by eye and '
             'sprayed out again.</span>',
             '<strong>Blend anyway.</strong> <span>Even a good match is faded into the '
             'neighbouring panels, because good is not the same as identical.</span>',
           ]),
          ]),
          ('Metallics, pearls and three-stage', [
           ('table', (['Finish', 'What makes it hard'], [
             ['Solid', 'Straightforward. Colour is colour.'],
             ['Metallic', 'Aluminium flake has to lie the same way, or it reads as a different '
                          'shade from an angle'],
             ['Pearl', 'A tinted mid-coat over a base. Thickness changes the colour.'],
             ['Three-stage', 'Base, translucent mid, lacquer. Each coat has to be the right '
                             'thickness, and there is no correcting it afterwards.'],
           ])),
           'Spray technique matters as much as the mix on anything with flake in it. Two painters '
           'using the same tin can produce visibly different panels, because how the paint is '
           'laid down decides how the flake orients. That is why a metallic is blended rather '
           'than butted up to the next panel even when the mix is perfect.',
           'There is no surcharge on our rate card for metallic, pearl or a colour change. There '
           'is more work, and we would rather do it than price it as an extra.',
          ]),
          ('Where to find your paint code', [
           'It is on a plate or sticker on the car, and the usual places are the driver&rsquo;s '
           'door shut, under the bonnet on the slam panel, in the boot under the carpet, or '
           'inside the fuel filler flap. It is usually three or four characters, sometimes with a '
           'colour name beside it.',
           'If you cannot find it, we will. The registration is enough for us to look up what '
           'should be there, and then we confirm it against the car.',
          ]),
         ],
         [('Will the repair be a perfect match?',
           'On a properly blended repair, yes, to the eye. What we will not claim is that the new '
           'paint is chemically identical to eleven-year-old paint, because it is not. Blending '
           'is what bridges that.'),
          ('My car is white. Is that easier?',
           'Solid white is one of the easier finishes. Pearl white, which a lot of modern cars '
           'use, is one of the hardest, because it is a three-stage finish and the mid-coat '
           'thickness changes the colour.'),
          ('Can you match a faded red?',
           'Yes, by matching what the car is now rather than what the code says it was. Reds fade '
           'more visibly than most colours, so this comes up often.'),
          ('What if I do not like the match?',
           'Tell us before you leave. We would far rather redo a panel than have you drive around '
           'unhappy with it, and that is what the guarantee is for.')],
         [('paint-blending-explained', 'Why we blend into the next panel'),
          ('bodywork-repair-process', 'The repair process, step by step'),
          ('why-repairs-dont-match', 'Why some repairs do not match'),
          ('metallic-pearl-and-three-stage-paint', 'Metallic, pearl and three-stage')],
         key_points=[
          'The code is a <strong>starting point</strong>, not an answer.',
          'Most codes have <strong>several published variants</strong> for factory and batch '
          'differences.',
          'Test cards are compared <strong>against your car, in daylight</strong>.',
          'No surcharge for <strong>metallic, pearl or colour change</strong> on our rate card.',
         ],
         hub=HUB_PROCESS, category='process', service_type='Vehicle paint', note=None),

    page('paint-blending-explained',
         'Why Bodyshops Blend Paint Into the Next Panel | KITH Cars',
         'What blending is, why stopping paint at the shut line shows, how far the blend goes, '
         'and why a quote without blending is cheaper for a reason.',
         'Why We Blend Into the Next Panel',
         'The repair process &middot; Paint',
         'Blending is the difference between a repair you cannot find and one you can see from '
         'the far side of a car park. It is also the first thing cut from a cheap quote, because '
         'nobody can see it missing until the sun comes out.',
         [
          ('What blending actually is', [
           'Instead of painting the damaged panel up to its edges and stopping, the new colour is '
           'carried a little way into the panels either side and faded out so there is no line '
           'where old meets new.',
           'The eye is extremely good at finding a hard edge between two similar colours and '
           'very bad at finding a gradual transition. Blending exploits that. It does not make '
           'the match better &mdash; it makes the difference impossible to locate.',
          ]),
          ('Why stopping at the shut line shows', [
           'A shut line is exactly where the eye goes looking. Two panels meeting at a crisp gap '
           'invite comparison, and any difference in shade, in how metallic flake has laid down, '
           'or in gloss level reads immediately.',
           'It is worst on metallics, worst again in direct sunlight, and worst of all on a car a '
           'few years old where the original paint has faded unevenly. All three of which '
           'describe most cars we see.',
          ]),
          ('How far the blend goes', [
           ('table', (['Repaired panel', 'Blended into'], [
             ['Front bumper', 'Both front wings'],
             ['Front wing', 'The bonnet and the front door'],
             ['Door', 'The next door, and the wing or quarter'],
             ['Rear quarter', 'The roof, the rear door and the sill'],
             ['Bonnet', 'Both front wings'],
             ['Roof', 'Both rear quarters'],
           ])),
           'A rear quarter is the extreme case, because it meets four other panels and one of '
           'them is the roof. Carrying colour up into the roof and fading it out is the only way '
           'to make a quarter repair disappear, and it is a large part of why a quarter costs '
           'what it does.',
          ]),
          ('The quote difference nobody explains', [
           'If one quote is noticeably cheaper than another on the same damage, blending is the '
           'single most likely reason. It is extra material, extra masking and extra time on '
           'panels that are not damaged, and leaving it out is invisible on the day.',
           'Blending is included in every figure on our rate card. It is not a line item, it is '
           'not an upsell, and we do not quote a lower number by leaving it out and then '
           'explaining afterwards.',
           ('note', 'If you are comparing quotes, ask each one directly: "does that include '
                    'blending into the adjacent panels?" The answers will tell you more than the '
                    'prices do.'),
          ]),
         ],
         [('Does blending mean painting undamaged panels?',
           'Partly, yes &mdash; a section of them. That sounds wasteful and it is the opposite: '
           'it is what stops the repaired panel standing out against them.'),
          ('Will the blended area wear differently?',
           'No. It is the same paint and the same lacquer, applied over properly prepared '
           'surface, and it is covered by the same one-year paint guarantee.'),
          ('Can you repair a panel without blending if I want it cheaper?',
           'We would rather not, and we will tell you why. On solid white or a very new car you '
           'might get away with it. On a metallic or anything more than a couple of years old, '
           'you will see it, and then it has to be done again properly.'),
          ('Why did my last repair not match, then?',
           'Most commonly because it was not blended. The second most common reason is a code '
           'match with no variant check and no spray-out card.')],
         [('paint-colour-matching-explained', 'How paint matching works'),
          ('why-repairs-dont-match', 'Why some repairs do not match'),
          ('bodywork-repair-process', 'The repair process, step by step'),
          ('rear-quarter-repair-cost', 'Rear quarter repair')],
         key_points=[
          'Colour carried into the <strong>neighbouring panels</strong> and faded out.',
          'The eye finds a <strong>hard edge</strong> easily and a gradual transition not at all.',
          'It is the <strong>first thing cut</strong> from a cheap quote, and invisible on the '
          'day.',
          '<strong>Included</strong> in every figure on our rate card.',
         ],
         hub=HUB_PROCESS, category='process', service_type='Vehicle paint', note=None),

    page('what-happens-at-strip-down',
         'What Strip-Down Finds: Hidden Accident Damage | KITH Cars',
         'Why the panel comes off before the real estimate, what commonly turns up underneath, '
         'and why finding more is normal rather than a sign something went wrong.',
         'What Strip-Down Finds',
         'The repair process &middot; Assessment',
         'Every estimate written with the panels on is a best guess about what is behind them. '
         'Strip-down is where the guessing stops, and it is the stage that most often changes '
         'the number.',
         [
          ('Why it has to happen first', [
           'A photograph shows the face of a panel. It cannot show a crash bar bent behind an '
           'intact bumper, a mounting bracket snapped behind a straight wing, or corrosion that '
           'starts on the inside face and has not yet reached the paint.',
           'So the first estimate is written from what is visible, authorised on that basis, and '
           'then tested against reality the moment the panel comes off. That sequence is not a '
           'flaw in the process &mdash; it is the process.',
          ]),
          ('What commonly turns up', [
           ['<strong>Broken mounting tabs.</strong> The most common find by far. A bumper can '
            'look perfect and be held on at three of its five points.',
            '<strong>A bent crash bar.</strong> Behind a bumper that absorbed the hit exactly as '
            'designed.',
            '<strong>Pulled wiring and connectors.</strong> Sensor looms stretched rather than '
            'cut, which fails intermittently rather than outright.',
            '<strong>Corrosion under the damage.</strong> Particularly on older cars and around '
            'arch lips and seams.',
            '<strong>Previous repairs.</strong> Filler over something that should have been '
            'replaced, or a panel bonded where it should have been welded.',
            '<strong>Impact carried further than it looked.</strong> A door hit that moved the '
            'pillar, a rear shunt that reached the boot floor.'],
          ]),
          ('What we do when we find something', [
           ('steps', [
             '<strong>Photograph it before anything moves.</strong> <span>In place, in context, '
             'with the surrounding area visible. A photograph taken after the part has been '
             'removed proves much less.</span>',
             '<strong>Stop.</strong> <span>No extra work happens before it is agreed, whether you '
             'are claiming or paying directly.</span>',
             '<strong>Raise it properly.</strong> <span>A supplementary to the insurer, or a '
             'revised figure to you, itemised rather than as a lump.</span>',
             '<strong>Tell you what it means for the timescale.</strong> <span>Usually the part '
             'you actually care about.</span>',
           ]),
          ]),
          ('The honest frustration', [
           'Strip-down findings arrive at the worst possible moment: your car is in pieces, you '
           'have already been told a price, and now there is a pause while someone else '
           'authorises more money. There is no way to make that pleasant.',
           'What we can do is make sure it is not a surprise twice. We tell you at the point of '
           'the original estimate which parts of the job are uncertain and why &mdash; a dent '
           'where we cannot see how far the metal has stretched, a bumper where the crash bar is '
           'hidden &mdash; so that if a supplementary comes, it comes from a conversation you '
           'have already had.',
          ]),
         ],
         [('Does strip-down cost me anything if I decide not to proceed?',
           'We will tell you before we start what happens if you walk away at that point. On most '
           'jobs the answer is a modest charge for the time, and we would rather state it up '
           'front than surprise you with it.'),
          ('Can you estimate accurately without stripping it?',
           'We can give you a band, and that is what the quote box on this page does. The exact '
           'figure needs the panel off on anything more than surface damage.'),
          ('Is finding more damage a sign the first estimate was bad?',
           'No. It is a sign the first estimate was written from the outside, which every first '
           'estimate is. A shop that never raises a supplementary is either very lucky or not '
           'looking.'),
          ('Who pays for the extra?',
           'On a claim, the insurer, once the supplementary is authorised. Your excess does not '
           'rise because the repair did. Paying privately, we agree the revised figure with you '
           'before continuing.')],
         [('supplementary-estimate-explained', 'Supplementary estimates'),
          ('bodywork-repair-process', 'The repair process, step by step'),
          ('what-the-engineer-does', 'What the engineer does'),
          ('how-long-does-bodywork-take', 'How long bodywork takes')],
         key_points=[
          'Every estimate written <strong>with the panels on</strong> is a best guess.',
          'The most common find is <strong>broken mounting tabs</strong> behind an intact panel.',
          'We <strong>photograph before anything moves</strong>, and stop before doing extra work.',
          'Your <strong>excess does not rise</strong> because the repair did.',
         ],
         hub=HUB_PROCESS, category='process', service_type='Vehicle body repair', note=None),

    page('adas-recalibration-after-bodywork',
         'ADAS Recalibration After Bodywork: Why It Matters | KITH Cars',
         'Why cameras and radar need recalibrating after a repair, which jobs trigger it, what '
         'happens if it is skipped, and how to tell whether your car needs it.',
         'ADAS Recalibration After a Repair',
         'The repair process &middot; Electronics',
         'Your car probably has a radar behind the front bumper and a camera behind the '
         'windscreen, and both are aimed rather than just mounted. Refit them a degree out and '
         'the car reads the road wrongly &mdash; with nothing on the dashboard to tell you.',
         [
          ('What ADAS actually is on your car', [
           'Advanced driver assistance systems: the features that watch the road for you. Most '
           'cars built in the last decade have at least one, and they rely on sensors mounted in '
           'exactly the places bodywork damage happens.',
           ('table', (['System', 'Usually sensed by', 'Mounted'], [
             ['Autonomous emergency braking', 'Radar, sometimes with a camera',
              'Behind the front bumper or grille badge'],
             ['Adaptive cruise control', 'Forward radar', 'Behind the front bumper'],
             ['Lane keeping and traffic signs', 'Forward camera', 'Behind the windscreen'],
             ['Blind spot monitoring', 'Rear corner radars', 'Behind the rear bumper corners'],
             ['Parking sensors and cameras', 'Ultrasonic sensors, cameras',
              'In both bumpers and the tailgate'],
           ])),
           'Every one of those positions is a panel that comes off for a routine repair.',
          ]),
          ('Why refitting is not enough', [
           'These sensors are aimed at the road from a known position. The calibration tells the '
           'car where the sensor is pointing relative to the vehicle&rsquo;s centre line and the '
           'ground, and the software interprets everything it sees through that.',
           'A bracket that goes back a fraction out, or a bumper sitting a few millimetres '
           'differently, moves the aim. At ten metres that is nothing. At a hundred and fifty '
           'metres, which is where adaptive cruise is looking, it is a different lane.',
          ]),
          ('What happens when it is skipped', [
           'Nothing, on the drive home. That is the whole problem.',
           ['Emergency braking that activates for something in the next lane.',
            'Emergency braking that does not activate when it should.',
            'Adaptive cruise that locks onto the wrong vehicle or loses the one in front.',
            'Lane keeping that nudges you toward the line rather than away from it.',
            'Parking sensors reading the ground as an obstacle and beeping continuously.'],
           'A miscalibrated system usually throws no warning light, because as far as the car is '
           'concerned the sensor is working perfectly. It is simply looking somewhere slightly '
           'different from where the software thinks.',
          ]),
          ('Which jobs trigger it', [
           ('steps', [
             '<strong>Front bumper off.</strong> <span>Forward radar on most cars. Nearly always '
             'needs checking.</span>',
             '<strong>Windscreen out or replaced.</strong> <span>Forward camera. Always.</span>',
             '<strong>Rear bumper off.</strong> <span>Blind spot radars on cars that have '
             'them.</span>',
             '<strong>Suspension or geometry work.</strong> <span>Changes the car&rsquo;s '
             'attitude, which changes where everything points.</span>',
             '<strong>Anything that moved a mounting point.</strong> <span>Including structural '
             'repair near a sensor location.</span>',
           ]),
           'We check what is fitted to your car before the panel comes off, not after. If '
           'recalibration is part of the job you will be told at the estimate rather than at '
           'collection.',
          ]),
         ],
         [('How do I know if my car has these systems?',
           'If it has adaptive cruise, lane assist, automatic emergency braking or blind spot '
           'warning, it has sensors that can need recalibrating. The handbook lists them. Give us '
           'the registration and we will tell you.'),
          ('Is recalibration expensive?',
           'It varies considerably by manufacturer and by which system. What it is not is '
           'optional on a car that needs it, and the honest version is telling you the cost at '
           'the estimate rather than discovering it at the end.'),
          ('Will a warning light come on if it is wrong?',
           'Usually not, and that is the point. The sensor reports itself as healthy. It is the '
           'aim that is out, and the car has no way to know.'),
          ('My insurer has not included it in the authorisation.',
           'Then we raise it. It is a necessary part of returning the car to the condition it was '
           'in, and an engineer who understands the system will authorise it.')],
         [('bodywork-repair-process', 'The repair process, step by step'),
          ('front-bumper-repair-cost', 'Front bumper repair'),
          ('what-happens-at-strip-down', 'What strip-down finds'),
          ('supplementary-estimate-explained', 'Supplementary estimates')],
         key_points=[
          'Sensors are <strong>aimed</strong>, not just mounted.',
          'A miscalibrated system usually throws <strong>no warning light</strong>.',
          'Front bumper off, windscreen out or suspension work can all <strong>trigger '
          'it</strong>.',
          'We check what is fitted <strong>before</strong> the panel comes off.',
         ],
         hub=HUB_PROCESS, category='process', service_type='ADAS recalibration', note=None),

    page('why-repairs-dont-match',
         "Why Some Body Repairs Don't Match | KITH Cars",
         'The six reasons a repaired panel ends up a visibly different shade, how to tell which '
         'one happened to your car, and what can be done about it.',
         "Why Some Repairs Don't Match",
         'The repair process &middot; Paint',
         'A repair that does not match almost always failed at one of six points, and five of '
         'them are preventable. Knowing which one went wrong tells you whether it can be put '
         'right.',
         [
          ('The six reasons', [
           ('table', (['What went wrong', 'How it looks', 'Fixable?'], [
             ['No blending', 'A visible step in shade at the shut line', 'Yes &mdash; redo with '
              'a blend'],
             ['Code used without variant check', 'Close but consistently off across the panel',
              'Yes &mdash; rematch and respray'],
             ['No spray-out card', 'Wrong from the moment it dried', 'Yes'],
             ['Matched under workshop light', 'Right indoors, wrong in daylight', 'Yes'],
             ['Flake laid down differently', 'Shifts shade as you walk past it', 'Yes, with '
              'technique'],
             ['Panel was already a different shade', 'The repair matches the code, not the car',
              'Yes &mdash; match the car'],
           ])),
          ]),
          ('How to tell which one happened', [
           ('steps', [
             '<strong>Look at it in daylight, outside.</strong> <span>Not in a garage, not under '
             'a streetlight. If it only shows outdoors, it was matched under the wrong '
             'light.</span>',
             '<strong>Walk past it at an angle.</strong> <span>If the shade shifts as you move, '
             'it is a metallic flake problem rather than a colour problem.</span>',
             '<strong>Find the edge.</strong> <span>If there is a clean line at the shut and the '
             'panel is uniformly different, it was not blended. If the difference fades out, it '
             'was blended and the mix was off.</span>',
             '<strong>Compare with the panel two along.</strong> <span>If the repaired panel '
             'matches its neighbour but both differ from the rest of the car, the original '
             'panel had already been painted before.</span>',
           ]),
          ]),
          ('What to do about it', [
           'If we did the work, tell us. The paint guarantee covers a year and a match we are not '
           'happy with is not a match we expect you to live with. Bring it back and we will look '
           'at it in daylight with you.',
           'If someone else did it, the position depends who paid. On an insurance repair through '
           'the insurer&rsquo;s own network, the insurer guarantees the work and the complaint '
           'goes to them. On a repair you paid for directly, it is between you and that '
           'bodyshop, and a clear photograph in daylight is worth more than any description.',
           ('note', CHOICE_NOTE),
          ]),
          ('The one that is genuinely hard', [
           'There is an honest exception in the list above. A car with badly faded original paint '
           '&mdash; a red that has gone pink on the roof, a dark blue that has chalked &mdash; '
           'can be matched to the car as it is now, and the match will be good. What it cannot do '
           'is stay good, because the repaired panel has fresh pigment and the rest of the car '
           'does not. It will diverge again over the next few years.',
           'We say that up front on a car in that condition, because the alternative is you '
           'discovering it in two summers and thinking we got it wrong.',
          ]),
         ],
         [('Can a bad match be corrected without a full respray?',
           'Usually, yes. Most of the six causes are fixed by redoing the panel properly with a '
           'blend, rather than painting the whole car.'),
          ('How long do I have to complain?',
           'With us, the paint guarantee is a year, and sooner is better for a colour issue '
           'because it is easiest to assess before the new paint has weathered at all.'),
          ('The bodyshop says it is within tolerance.',
           'Ask to see it with them, outside, in daylight. "Within tolerance" is a reasonable '
           'phrase for a measured difference and an unreasonable one for something you can see '
           'from across the road.'),
          ('Does a mismatched repair affect the car’s value?',
           'It can, because a visible repair invites questions about what else was done. It is '
           'worth putting right before selling.')],
         [('paint-colour-matching-explained', 'How paint matching works'),
          ('paint-blending-explained', 'Why we blend into the next panel'),
          ('metallic-pearl-and-three-stage-paint', 'Metallic, pearl and three-stage'),
          ('bodywork-repair-process', 'The repair process, step by step')],
         key_points=[
          'Six causes, and <strong>five are preventable</strong>.',
          'Only shows <strong>outdoors</strong>? It was matched under workshop light.',
          'A <strong>clean line at the shut</strong> means it was not blended.',
          'Badly faded original paint is the <strong>honest exception</strong> &mdash; it will '
          'diverge again.',
         ],
         hub=HUB_PROCESS, category='process', service_type='Vehicle paint', note=None),
]
