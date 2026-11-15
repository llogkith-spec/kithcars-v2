#!/usr/bin/env python3
"""Damage-type pages: one per kind of damage, across every panel it happens to.

These are deliberately built the other way up from the panel pages. A panel page opens with the
rate card for that panel and is organised around the object; a damage page opens with "is this
what I have?" and is organised around the method, with the price table running by panel rather
than by damage. Someone who has just walked out to their car does not know the panel is called a
quarter - they know there is a scratch and they want to know whether it is the bad kind.

That difference in shape is what keeps the two sets from reading as the same content sorted
differently, and the uniqueness check in build/bodywork.py is what proves it.
"""
import json
import pathlib

from bw_lib import page, HUB_DAMAGE

PRICES = json.loads((pathlib.Path(__file__).resolve().parent / 'bodyprices.json').read_text())

PANEL_LABEL = [
    ('front-bumper', 'Front bumper'), ('rear-bumper', 'Rear bumper'),
    ('front-wing', 'Front wing'), ('rear-quarter', 'Rear quarter'),
    ('door', 'Door'), ('bonnet', 'Bonnet'), ('boot', 'Boot lid'),
    ('roof', 'Roof'), ('trim', 'Trim and mirrors'),
]

METAL = {'front-wing', 'rear-quarter', 'door', 'bonnet', 'boot', 'roof'}
PLASTIC = {'front-bumper', 'rear-bumper', 'trim'}
LOW = {'front-bumper', 'rear-bumper', 'door', 'trim'}
HORIZONTAL = {'bonnet', 'roof', 'boot'}

DAMAGE = [
    dict(
        slug='light-scratch-repair', prices='smart', h1='Light Scratch Repair',
        label='Bodywork &middot; Scratches', panels='all',
        short='A scratch in the lacquer only. The cheapest paint damage to put right, and the '
              'one most often oversold as a full respray.',
        lead='If your fingernail does not catch in it, the scratch has not gone through the '
             'colour &mdash; and that is the cheap repair rather than the expensive one.',
        diagnose=[
         'Run a fingernail gently across the scratch, at a right angle to it.',
         'If it glides over, the damage is in the clear lacquer on top and the colour underneath '
         'is intact.',
         'If it catches, it has gone through to the primer or the metal, and that is a different '
         'and dearer job.',
         'Wet the scratch with a drop of water. If it disappears while wet and returns as it '
         'dries, it is lacquer-deep.'],
        method=['The area is flatted back with progressively finer abrasive until the edges of '
                'the scratch are level with the surrounding lacquer, then the lacquer is '
                'rebuilt over it and machine polished until the gloss matches the panel around '
                'it.',
                'The panel stays on the car and only the affected area is refinished, which is '
                'why this is the cheapest route out of any paint damage. There is no colour '
                'involved, so there is no colour to match.'],
        diy='A scratch remover from a motor factor is genuinely worth trying on lacquer damage, '
            'and it sometimes works. What it cannot do is add lacquer back, so it only helps '
            'where there is enough thickness left to flatten into. If two attempts have not '
            'shifted it, stop &mdash; the risk from here is going through the lacquer entirely '
            'and turning a cheap job into a panel respray.',
        when='Lacquer damage is not urgent. Nothing is corroding, because the colour and primer '
             'below are untouched. It is worth doing before you sell the car and worth doing if '
             'it irritates you, but there is no clock running.',
        faqs=[('Can you polish any scratch out?',
               'No, and anyone who says yes is going to disappoint you. Polishing removes a '
               'little lacquer to level the surface. If the scratch is deeper than the lacquer, '
               'there is nothing to level into.'),
              ('Will the polished area look different?',
               'Not when it is done properly. The area is polished and then the whole panel is '
               'brought to the same finish, so there is no bright patch where the work was.'),
              ('How long does it take?',
               'Usually the same day, and often while you wait for a single scratch.'),
              ('Is it worth claiming on insurance?',
               'Almost never. This is well under any normal excess.')]),

    dict(
        slug='deep-scratch-repair', prices='scuff', h1='Deep Scratch Repair',
        label='Bodywork &middot; Scratches', panels='all',
        short='A scratch through the colour, down to primer or bare metal. Needs refinishing, '
              'not polishing.',
        lead='Once your fingernail catches, polishing cannot bring it back. The panel has to be '
             'refinished, and on bare metal there is a clock running.',
        diagnose=[
         'Your fingernail catches in it when you draw it across.',
         'You can see a different colour in the bottom of the scratch &mdash; grey or white '
         'primer, or bright metal.',
         'It stays visible when the panel is wet.',
         'On a light-coloured car, look for a dark line; on a dark car, a pale one. Either way '
         'the colour in the groove is not your car&rsquo;s colour.'],
        method=['Anything raised along the edges of the scratch is flatted level, the groove is '
                'filled where it needs it, and the area is primed. Primer is flatted again, '
                'then the colour is sprayed and faded out into the panel and into its '
                'neighbours so there is no visible edge to the repair.',
                'Lacquer goes over the whole repaired area, it is baked, and then polished back '
                'to match the finish of the panels around it.'],
        diy='Touch-up paint from a pen has one legitimate use here, and it is not making the '
            'scratch invisible. It is sealing bare metal so it does not corrode while you decide '
            'what to do. Clean the groove, apply it thinly, and accept that it will look like a '
            'line of paint in a groove &mdash; because that is what it is.',
        when='If you can see bare metal, deal with it before a winter rather than after one. '
             'Salt and water in an open scratch start corrosion that spreads sideways underneath '
             'the paint film, and the repair stops being a paint job and becomes a metal one.',
        faqs=[('Why does the whole panel need painting for one scratch?',
               'It does not always &mdash; a short scratch in the middle of a large panel can '
               'sometimes be repaired locally. What it does need is the new colour faded out '
               'into the existing paint rather than stopped at a hard line, and that means '
               'spraying an area considerably larger than the scratch.'),
              ('Can you match the colour exactly?',
               'It is mixed to the paint code on your car. Two cars with the same code still '
               'differ after a few years of sun, which is why we blend into the adjacent panels '
               'rather than relying on the mix alone.'),
              ('What if the scratch crosses two panels?',
               'Then it is two panels. A scratch that runs across a shut line has to be treated '
               'as two repairs that are blended to meet, and we will price it that way rather '
               'than pretending it is one.'),
              ('Is a deep scratch an insurance job?',
               'Usually not on one panel &mdash; check your excess first. Across three or four '
               'panels, as with a key scratch, it starts to be worth claiming.')]),

    dict(
        slug='car-scuff-repair', prices='scuff', h1='Scuff Repair',
        label='Bodywork &middot; Scuffs', panels='all',
        short='A broad graze rather than a line, usually from brushing something slowly. Often '
              'carries transferred colour that is not yours.',
        lead='Half the scuffs we are asked to quote for are not damage to your paint at all '
             '&mdash; they are someone else&rsquo;s paint sitting on top of yours. It is worth '
             'five minutes finding out which you have.',
        diagnose=[
         'Look for a colour that is not your car&rsquo;s: white from a van, black from a '
         'bollard, yellow from a post.',
         'Transferred paint sits proud of the surface. Your own damage sits in it.',
         'Rub a small area with polish on a cloth. If the mark lifts and the gloss underneath is '
         'intact, it was transfer and the job is done.',
         'If a dull grey patch stays behind once the transfer is off, your lacquer has gone and '
         'the area needs refinishing.'],
        method=['The transferred material comes off first, with compound rather than abrasive, '
                'because there is no point refinishing paint that turns out to be undamaged.',
                'Where the lacquer has been taken off, the area is flatted, primed if the colour '
                'has gone too, then refinished and blended out into the panel. A scuff is '
                'usually wide and shallow, which makes it a good candidate for a localised '
                'repair rather than a full panel.'],
        diy='This is the one kind of damage where having a go yourself is genuinely worth it. A '
            'tub of paint cleaner or a mild cutting compound and a microfibre cloth will remove '
            'transferred paint without touching your own. Work in a small area, keep the cloth '
            'clean, and stop as soon as you stop seeing the other colour coming off.',
        when='Not urgent if the paint underneath is intact. If the scuff has taken the lacquer '
             'off over a wide area, it is worth doing before the exposed colour starts to fade '
             'and chalk, which happens faster than people expect on reds and dark blues.',
        faqs=[('I rubbed it and the colour came off. Was that safe?',
               'If you used polish or compound and a soft cloth, yes. What does damage is anything '
               'abrasive &mdash; a kitchen scourer, a magic sponge, or rubbing with a dry cloth '
               'full of grit.'),
              ('The scuff is on a textured plastic trim. Same answer?',
               'No. Textured plastic cannot be polished back &mdash; it goes shiny in patches and '
               'looks worse. That is a repaint or replace decision.'),
              ('How big does a scuff have to be before the whole panel needs doing?',
               'It is less about size than position. A scuff in the middle of a large flat panel '
               'can be repaired locally. One that runs to the edge of a panel usually means '
               'refinishing to the shut line.'),
              ('Can you do it while I wait?',
               'A polish-off, often yes. Anything needing paint needs to bake and cure, so that '
               'is a day or two.')]),

    dict(
        slug='stone-chip-repair-cost', prices='smart', h1='Stone Chip Repair',
        label='Bodywork &middot; Chips', panels='all',
        short='Small pits from grit at speed. Cosmetic until they start to rust, then not.',
        lead='Chips are the damage everybody ignores, and they are the one kind where ignoring '
             'it genuinely changes the bill. The moment you can see brown in the bottom of a '
             'chip, the clock has started.',
        diagnose=[
         'Small round or teardrop pits, usually grouped rather than single.',
         'Concentrated along the leading edge of the bonnet, the front of the roof, the mirror '
         'housings and the lower doors behind the front wheels.',
         'Look into each chip in good light. Grey or white at the bottom is primer, and that is '
         'fine for now. Brown is rust, and that is not.',
         'Run a fingertip over a suspicious chip. If the paint around it lifts or feels crisp, '
         'corrosion has already spread under the film.'],
        method=['Each chip is cleaned out, any corrosion removed back to clean metal, filled, '
                'flatted level and the area refinished and blended.',
                'On a panel carrying a lot of chips it is usually better value to refinish the '
                'whole panel than to chase twenty individual repairs, and we will say so rather '
                'than quoting per chip and arriving at a bigger number.'],
        diy='A touch-up pen is worth having for exactly this. It will not make the chip '
            'invisible &mdash; you will see a small dot of paint &mdash; but it seals the metal '
            'and stops the chip becoming a rust spot. Clean the chip first, build the paint up '
            'in thin layers rather than one blob, and let each one dry.',
        when='Before winter, every time. Salt sits in an open chip and works underneath the paint '
             'where you cannot see it. A bonnet caught in year one is a paint job; the same '
             'bonnet in year three needs the leading edge cut back to clean metal first.',
        faqs=[('How many chips before it is worth doing the whole panel?',
               'Roughly, once you stop being able to count them at a glance. Beyond that, '
               'individual repairs cost more in labour than refinishing the panel properly.'),
              ('Does paint protection film actually work?',
               'Yes, on the areas that take the worst of it &mdash; the bonnet leading edge and '
               'the mirror caps. It is far more effective applied to fresh paint than over a '
               'surface that already has chips in it, so the time to ask is when a panel has '
               'just been refinished.'),
              ('My chips are already brown. Is it too late?',
               'No, but it is now a metal repair rather than a paint one. The corrosion has to '
               'come out back to clean steel, because anything left under a new repair carries '
               'on working and pushes the paint off again within a year.'),
              ('Will the touch-up pen I used cause a problem later?',
               'Not at all. We flat it back as part of the preparation. Sealing the metal was the '
               'right call.')]),

    dict(
        slug='car-dent-repair', prices='dent', h1='Dent Repair',
        label='Bodywork &middot; Dents', panels='all',
        short='The panel is pushed in. We straighten and repaint it &mdash; we do not do '
              'paintless dent removal, and we are straight about that up front.',
        lead='Every dent we repair gets painted, because we do not offer paintless removal. That '
             'makes us more expensive than a PDR van for the dents PDR can fix, and it makes us '
             'the right answer for the ones it cannot.',
        diagnose=[
         'Look along the panel from the end of the car rather than straight at it. Dents hide '
         'from face-on and show badly at a shallow angle.',
         'Check whether the paint is broken. An unbroken dent means the metal stretched without '
         'the film cracking; a broken one means filler and primer as well as straightening.',
         'Press gently at the edge. A dent that pops slightly is shallow. One that feels solid '
         'has stretched the metal and will not simply come back.',
         'Look for a sharp line in it. A crease is a different and harder job than a smooth '
         'dent.'],
        method=['The metal is worked back in stages rather than pulled in one go, because metal '
                'forced out too fast oil-cans and never sits flat again. Where it will not come '
                'fully back, the remaining difference is filled and flatted level.',
                'Then primer, colour, lacquer and a blend into the neighbouring panels. The paint '
                'is not optional on our repairs: straightening alone leaves a panel that is the '
                'right shape and the wrong finish.'],
        diy='There is very little worth attempting on a dent, and the suction cups sold for it '
            'work on exactly one kind &mdash; a shallow, smooth, unbroken dent in the middle of '
            'a large flat panel. On anything creased, anything near an edge, and anything where '
            'the paint is broken, they either do nothing or stretch the metal further and make '
            'the professional repair harder.',
        when='A dent with unbroken paint is not urgent. A dent with the paint split is, because '
             'it is an open route to bare metal on a panel that now holds water in the bottom '
             'of the depression.',
        faqs=[('Do you do paintless dent removal?',
               'No. The panel is straightened and then painted and blended. We would rather tell '
               'you that now than quote a PDR price and find a reason it cannot be done once '
               'your car is in the workshop.'),
              ('Why is a small dent not a small price?',
               'Because the dent is the small part. On a door, the trim card comes off, the water '
               'shield is peeled back and resealed, the glass is lowered and supported, and then '
               'the panel is painted and blended. The metalwork is often the quickest bit.'),
              ('Can you give me a price from a photograph?',
               'A band, yes. The exact figure needs the car, because how deep the damage goes and '
               'whether the metal has stretched are the two things a photograph does not show, '
               'and they are the two things that move the number.'),
              ('Is it cheaper to replace the panel?',
               'Sometimes, and only on bolt-on panels &mdash; a wing, a bonnet, a boot lid, a '
               'door. On a welded panel like a rear quarter, straightening nearly always wins. '
               'We price both where it is a genuine choice.')]),

    dict(
        slug='creased-panel-repair', prices='dent', h1='Creased Panel Repair',
        label='Bodywork &middot; Dents', panels='all',
        short='A dent with a sharp fold in it. The metal has stretched, which is what makes this '
              'the point where straightening stops being the obvious answer.',
        lead='A crease is where a dent stops being a dent. The metal has folded rather than '
             'pushed, and folded metal is longer than it was &mdash; which is why it will not '
             'simply go back.',
        diagnose=[
         'There is a distinct line within the damage, not just a smooth depression.',
         'The paint is often cracked or lifted along the fold itself even where the rest of the '
         'panel is fine.',
         'Pressing it does nothing. A crease has no give in it.',
         'Sight along the panel: a crease throws a hard shadow line where a dent throws a soft '
         'one.'],
        method=['Worked back in stages with heat and careful shrinking rather than pulled, '
                'because a crease forced out quickly leaves the panel wavy and no amount of '
                'filler hides a wave on a flat surface in daylight.',
                'Once the shape is back as far as the metal allows, it is filled, flatted, '
                'primed and refinished with a blend into the panels either side.'],
        diy='Nothing. This is the damage type where attempting it yourself most reliably makes '
            'the professional repair more expensive, because a stretched panel that has been '
            'pulled further is sometimes past saving when it would not have been.',
        when='Not urgent unless the paint has split along the fold, which it often has. A split '
             'along a crease holds water in exactly the place the metal is already thinnest.',
        faqs=[('Why is a crease dearer than a dent the same size?',
               'Because size is not what drives it. A smooth dent is pushed back; a crease has '
               'stretched metal that has to be shrunk back, and that is slow, skilled work done '
               'in small increments.'),
              ('Should I just replace the panel?',
               'On a bolt-on panel &mdash; wing, bonnet, boot, door &mdash; a heavy crease is '
               'genuinely where replacement starts to win, and we will price both so you can '
               'choose. On a welded panel it is rarely the cheaper route.'),
              ('Will it be completely invisible?',
               'On a well-executed repair, yes. The honest caveat is that a crease across a sharp '
               'body line is the hardest thing in bodywork to make perfect, and we will tell you '
               'before we start if yours is one of those.'),
              ('How long does it take?',
               'Longer than a dent &mdash; usually three days rather than two, because the '
               'metalwork cannot be rushed without showing.')]),

    dict(
        slug='cracked-bumper-repair', prices='dent', h1='Cracked Bumper Repair',
        label='Bodywork &middot; Plastic', panels='plastic',
        short='Split plastic, welded from behind and reinforced. A cracked bumper is very rarely '
              'a scrap bumper.',
        lead='Plastic is the one material on the car that can be genuinely repaired rather than '
             'disguised. A crack is welded back together with matching plastic from behind, not '
             'filled over and hoped for.',
        diagnose=[
         'A visible split, usually starting at a corner or radiating from a mounting point.',
         'Check behind it as well as in front. The mounting tabs break far more often than the '
         'visible face, and they are what hold the bumper in line.',
         'An uneven panel gap with no visible crack almost always means broken tabs.',
         'Flex the area gently. If the crack opens and closes, it goes all the way through.'],
        method=['The crack is vee&rsquo;d out and welded from the back with plastic matched to '
                'the bumper&rsquo;s own material, then reinforced across the repair so it cannot '
                'open again under flex.',
                'Broken mounting tabs are rebuilt at the same time, because a bumper that is '
                'cosmetically perfect and only held on at three of its five points will sit '
                'wrong within a month. The face is then filled, primed, painted and blended.'],
        diy='Glue and the plastic repair kits sold for this are bonding the surface, not joining '
            'the material. They hold until the first cold morning or the first speed bump, and '
            'the crack reopens along exactly the same line. Cable ties behind a bumper are a '
            'recognised get-you-home and nothing more.',
        when='Before the crack grows. A split in a bumper propagates every time the panel flexes, '
             'and a repair across four inches is a different job from one across fourteen.',
        faqs=[('Is repairing cheaper than a new bumper?',
               'Usually, and the gap narrows as the damage gets worse. On heavy damage we price '
               'both, because at some point a new skin is the better value and we would rather '
               'say so.'),
              ('Will the repair show?',
               'Not from the outside. The weld is on the back, and the face is filled, primed and '
               'refinished like any other paint repair.'),
              ('What about the sensors and the radar?',
               'They come out before the work and get tested afterwards. On cars with forward '
               'radar for adaptive cruise or automatic braking, a bumper that comes off may need '
               'that radar recalibrated, and we tell you up front rather than at the end.'),
              ('Can a cracked bumper fail an MOT?',
               'It can, if it has a sharp edge that is a risk to other road users, or if it is '
               'insecure. A hairline crack in the middle of a bumper will not, but a broken '
               'corner hanging proud might.')]),

    dict(
        slug='car-rust-repair', prices='dent', h1='Rust and Corrosion Repair',
        label='Bodywork &middot; Corrosion', panels='metal',
        short='Cut back to clean metal, treated and repaired. Rust left under a repair carries '
              'on working and pushes the new paint off within a year.',
        lead='There is no painting over rust. Anything left underneath keeps corroding in the '
             'dark, and the repair lifts within a year or two looking exactly as it did before '
             'you paid for it.',
        diagnose=[
         'Paint bubbling or blistering, which means corrosion underneath has lifted the film.',
         'Brown staining weeping from a seam, an edge or a stone chip.',
         'Press it gently. If it gives, or sounds crisp rather than solid, the metal behind has '
         'already gone.',
         'Check the usual places: wheel arch lips, the bottom of doors, sills, the seam around '
         'the number plate lights, and under the fuel filler flap.'],
        method=['The affected area is cut back until there is clean, sound metal on every side of '
                'it &mdash; which is nearly always a larger area than the bubbling suggested, '
                'because corrosion spreads sideways under the paint where it cannot be seen.',
                'Where enough metal remains, it is treated, primed with an etch primer and '
                'filled. Where it does not, a section is let in and welded, then seam-sealed on '
                'both sides before paint. The inside face is treated as well as the outside, '
                'because that is usually where it started.'],
        diy='Converter products have a real but narrow use: they stabilise surface rust on '
            'something structural you are not about to repair properly. On a visible panel they '
            'do not restore metal that has gone, and painting over a converted patch leaves a '
            'lump that reappears as a stain within a season.',
        when='Now rather than next year, and this is the one damage type where that is not a '
             'sales line. Corrosion is the only kind of damage on this list that actively gets '
             'worse on its own, and the cost rises with the area, not with time.',
        faqs=[('Why is the repair area bigger than the rust I can see?',
               'Because what you can see is where the paint has lifted, not where the corrosion '
               'ends. It spreads under the film, and cutting back only to the visible edge '
               'guarantees it comes back.'),
              ('Can you just fill it?',
               'We can, and it will look right for about a year. We would rather tell you that '
               'and let you decide than take the money for a repair we know will fail.'),
              ('Is rust an MOT failure?',
               'It is where it is structural or within a prescribed distance of a structural or '
               'load-bearing component &mdash; sills, suspension mounts, subframe areas. '
               'Cosmetic corrosion on a wing or a door skin is not a failure, but it is still '
               'getting worse.'),
              ('Is it worth repairing on an old car?',
               'Sometimes honestly not, and we will say so. If the arches, sills and floor are '
               'all going at once, the sensible conversation is about the car rather than the '
               'panel.')]),

    dict(
        slug='kerb-damage-repair', prices='scuff', h1='Kerb Damage Repair',
        label='Bodywork &middot; Kerbing', panels='low',
        short='Long low grazes from kerbs, bollards and ramps. Usually looks worse at an angle '
              'than it does face-on.',
        lead='Kerb damage is the damage people live with longest, because it hides from face-on '
             'and most of us look at our cars from the front. Walk to the end of the car and '
             'look along it &mdash; that is the view everyone else gets.',
        diagnose=[
         'A long horizontal graze low on the panel, often with the paint back to primer in '
         'patches rather than evenly.',
         'Frequently carries grey or black transfer from the kerb or bollard itself.',
         'Check the wheel on the same corner. Kerbing a sill or a bumper corner usually kerbs '
         'the alloy as well, and the two are often quoted separately when they should not be.',
         'Look for cracking at the ends of the graze on a plastic sill cover, where it has been '
         'forced away from its clips.'],
        method=['The transferred material comes off first. The damaged run is then flatted, '
                'primed where the colour has gone, and refinished along its length, blended '
                'upward into the panel so the top edge of the repair does not read as a line in '
                'raking light.',
                'On a plastic sill cover or arch moulding, we check the clips and mounting points '
                'as well: a cover that has been dragged along a kerb is frequently no longer '
                'fully attached at the bottom edge.'],
        diy='Compound will take off the transferred kerb colour and sometimes that is most of '
            'what you can see. It will not restore primer-deep damage. Worth ten minutes before '
            'you decide whether to get it quoted.',
        when='Not urgent on plastic. On a metal sill or an arch lip it is worth dealing with '
             'before winter, because kerb damage sits exactly where road salt and standing water '
             'collect.',
        faqs=[('It also kerbed the alloy. Can you do both?',
               f'Yes, and it is worth doing together. Alloy refurbishment runs '
               f'&pound;{PRICES["_alloy_per_wheel_inc_vat"]["low"]} to '
               f'&pound;{PRICES["_alloy_per_wheel_inc_vat"]["high"]} per wheel including VAT, '
               f'depending on how badly the face is gouged and whether the finish is '
               f'diamond-cut.'),
              ('Can the sill cover be repaired or does it need replacing?',
               'Depends on the finish. A painted cover repairs well. A textured black one cannot '
               'be polished back without going shiny in patches, so it is repaint or replace, '
               'and on common cars a new moulding is sometimes the cheaper of the two.'),
              ('Will it happen again in the same place?',
               'If it is a ramp or a drive you use daily, honestly yes. It is worth considering '
               'protective film on that corner if it is a known pinch point.'),
              ('Does kerb damage affect the car structurally?',
               'Not usually &mdash; it is a surface graze. What is worth checking after a hard '
               'kerb strike is the wheel and the suspension geometry on that corner, which is a '
               'separate job from the paint.')]),

    dict(
        slug='key-scratch-vandalism-repair', prices='scuff', h1='Key Scratch and Vandalism Repair',
        label='Bodywork &middot; Vandalism', panels='all',
        short='A deliberate scratch, usually crossing several panels. Photograph it and get a '
              'crime reference before anything is touched.',
        lead='Before you book it in, photograph it and report it to the police for a crime '
             'reference. Your insurer will ask for the reference, and a vandalism claim without '
             'one is a harder conversation than it needs to be.',
        diagnose=[
         'A long, deliberate line, usually at a consistent height and crossing shut lines.',
         'Almost always through the colour rather than the lacquer, because it was done with '
         'something hard and sharp.',
         'Check both sides of the car and the bonnet and boot. Vandalism is rarely confined to '
         'one panel, and people often spot one side and miss the other.',
         'Photograph each panel separately and the whole car in one shot, in daylight, before '
         'anything is cleaned or touched.'],
        method=['Each affected panel is treated as its own repair and blended into the next, '
                'because a scratch that crosses a shut line is two repairs rather than one. Each '
                'is flatted, filled where it needs it, primed, refinished and blended.',
                'Where the damage crosses three or four panels down one side of the car, we '
                'refinish them as a set so the colour runs consistently along the whole flank '
                'rather than matching panel by panel.'],
        diy='Nothing, and in this case for a reason beyond the paint: do not clean or touch the '
            'damage until it has been photographed and reported. Once the evidence is recorded, '
            'the advice is the same as for any deep scratch &mdash; touch-up paint to seal bare '
            'metal if there will be a delay before the repair.',
        when='Report immediately. The repair itself can wait as long as any bare metal is sealed, '
             'but claims and crime references are easier the same week than the following month.',
        faqs=[('Will claiming for vandalism cost me my no-claims?',
               'It can, and this is where vandalism is frustrating: there is no third party to '
               'recover from, so your insurer carries the cost and most policies treat it as a '
               'fault-free but chargeable claim. Check your policy &mdash; some protect '
               'no-claims for vandalism specifically where a crime reference is supplied.'),
              ('The excess is more than one panel costs. What now?',
               'Then it depends how many panels. One panel is usually a pay-directly job. Three '
               'or four down one side almost always beats the excess, and that is the sum worth '
               'doing before you call anyone.'),
              ('Can you match the paint across four panels?',
               'Yes, and doing them as a set is the reason it works. Refinishing four panels '
               'individually to the same code can still leave them subtly different; refinishing '
               'them as a run does not.'),
              ('Do I have to tell my insurer even if I pay for it myself?',
               'Most policies require you to notify any incident, even one you do not claim for. '
               'Not notifying is the thing that causes problems later, not the damage itself.')]),
]


def _panels_for(kind):
    if kind == 'metal':
        return [(k, l) for k, l in PANEL_LABEL if k in METAL]
    if kind == 'plastic':
        return [(k, l) for k, l in PANEL_LABEL if k in PLASTIC]
    if kind == 'low':
        return [(k, l) for k, l in PANEL_LABEL if k in LOW]
    return PANEL_LABEL


def build():
    out = []
    for D in DAMAGE:
        panels = _panels_for(D['panels'])
        rows = []
        for key, label in panels:
            p = PRICES[f'{key}|{D["prices"]}|medium']
            rows.append([label, f'&pound;{p["low"]} &ndash; &pound;{p["high"]}'])
        cheapest = min(PRICES[f'{k}|{D["prices"]}|medium']['low'] for k, _ in panels)
        dearest = max(PRICES[f'{k}|{D["prices"]}|medium']['high'] for k, _ in panels)

        sections = [
            ('Is this what you have?', [
             'Four checks, in order. They take about two minutes in daylight and they decide '
             'which repair you are actually looking at.',
             ('steps', [f'<strong>{s.split(".")[0]}.</strong> '
                        f'<span>{".".join(s.split(".")[1:]).strip() or s}</span>'
                        for s in D['diagnose']])]),

            ('How we repair it', D['method']),

            ('What it costs, panel by panel', [
             'Including VAT, on an ordinary five-seater, with the paint blended into the '
             'neighbouring panels. Blending is included on our rate card rather than being an '
             'extra line.',
             ('table', (['Panel', 'Price inc VAT'], rows)),
             'SUVs and estates carry a small uplift and vans a larger one, because there is more '
             'panel to cover. Every band runs upward from the card figure rather than either '
             'side of it.']),

            ('What you can try yourself', [
             D['diy'],
             ('note', '<strong>When to stop.</strong> If two careful attempts have not improved '
                      'it, stop there. Almost every job we see that cost more than it should '
                      'have is one where a reasonable first attempt turned into a fourth.')]),

            ('How soon it needs doing', [D['when']]),
        ]

        out.append(page(
            D['slug'],
            f'{D["h1"]} - From £{cheapest} | KITH Cars',
            f'{D["short"]} What it costs by panel (£{cheapest}-£{dearest} inc VAT), how we do it, '
            f'and what is worth trying yourself first. Hackbridge bodyshop.',
            D['h1'], D['label'], D['lead'],
            sections, D['faqs'],
            [('body-panel-repairs', 'Every panel and what it costs'),
             ('bodywork-repair-process', 'How a repair runs, step by step'),
             ('paint-colour-matching-explained', 'How paint matching works'),
             ('should-i-claim-or-pay-myself', 'Claim or pay yourself?')],
            key_points=[
             f'<strong>&pound;{cheapest} to &pound;{dearest}</strong> inc VAT depending on the '
             f'panel.',
             D['short'],
             'Paint blended into the neighbouring panels &mdash; included, never an extra.',
             'One year on paint, in writing.'],
            hub=HUB_DAMAGE, category='damage',
            service_type='Vehicle body repair',
            quote_heading='Price your repair now',
            note=None))
    return out


PAGES = build()
