#!/usr/bin/env python3
"""Panel pages and damage pages.

This file used to generate a 9 x 10 crossing of panels and damage types - 76 pages. It was
measured and thrown away: 80% of every page was vocabulary shared with all the others, the median
pair was 65% identical and the worst was 90%. That is as duplicative as the town pages already on
the site, and the arithmetic is why: in a 9 x 10 grid each page shares its panel facts with nine
siblings and its damage facts with eight, so the genuinely unique part is only the intersection -
about 180 words out of 900.

What replaced it:

  9 panel pages    one per panel, covering every kind of damage that panel takes, written around
                   what that panel actually is - a bolted wing against a welded quarter is a
                   different job, not a different noun
  10 damage pages  one per damage type, covering every panel it happens to, written around the
                   method rather than the location
  crossings        only where the combination is a real search in its own right

The two sets are structured differently on purpose, not just worded differently, so a panel page
and a damage page have little to be similar about.

Prices come from build/bodyprices.json, produced by build/bodyprices.js running the live quote
engine over the catalogue. The pages never recompute a price themselves: the site already shipped
a bumper page saying "From £300" beside a widget saying £288, and a second implementation of the
pricing is how that happens.

KITH does not do paintless dent removal. Every dent here is straightened and the panel then
painted and blended, because that is what actually happens in the workshop.
"""
import json
import pathlib

from bw_lib import page, HUB_DAMAGE

PRICES = json.loads((pathlib.Path(__file__).resolve().parent / 'bodyprices.json').read_text())


def money(panel, damage_id, band='medium'):
    p = PRICES[f'{panel}|{damage_id}|{band}']
    return f'&pound;{p["low"]}', f'&pound;{p["high"]}', p


# ---------------------------------------------------------------------------------------------
# The panels, written as objects. Everything here is a fact about that specific panel: what it is
# made of, whether it comes off, what is behind it, what goes wrong with it, and what the repair
# actually costs against replacing it.
# ---------------------------------------------------------------------------------------------
PANELS = {
    'front-bumper': dict(
        name='front bumper', slug='front-bumper', job='panel-front-bumper',
        material='moulded thermoplastic over a crash bar',
        off='It unclips and unbolts, so it comes off the car and is worked flat on a stand.',
        neighbours='both front wings and the lower edge of the bonnet',
        behind='parking sensors, the radar for adaptive cruise and autonomous braking on a lot of '
               'cars, a forward camera, washer jets, fog lights and the main crash bar',
        causes=['Queue shunts, which push the centre in and break the upper mounting tabs.',
                'Kerbs and car park blocks, which scrape the lower lip and crack the corners.',
                'Multi-storey ramps, which take the splitter off the bottom edge.',
                'Supermarket trolleys and door openings, which chip the leading corners.'],
        quirk='Plastic is the part that works in your favour. A crack can be welded from behind '
              'with matching plastic and reinforced, so a split bumper is very rarely a scrap '
              'bumper. What is not in your favour is everything mounted in it: a bumper that '
              'looks straight but sits with an uneven gap has almost always broken its mounting '
              'tabs, and those are what hold it in line.',
        risk='The sensors and the radar. A bumper refitted without the radar being checked can '
             'leave adaptive cruise and automatic braking misreading the road, and on most cars '
             'that needs a proper recalibration rather than a reset.',
        replace='A new painted bumper skin is often not far off the cost of repairing a badly '
                'broken one, so on heavy damage we price both. On light damage repair wins every '
                'time, because a repaired original still has its original fit.',
        time='A corner scuff is often same day. A bumper off the car, repaired, painted and '
             'refitted is usually two days.',
        damages=['smart', 'scuff', 'dent'],
        extra=('Why bumpers are the most common job we do',
               ['Bumpers take more damage than any other panel on the car for a reason that has '
                'nothing to do with driving: they are the lowest, widest, most forward and most '
                'rearward thing on the vehicle, and they are made of a material chosen to deform '
                'rather than resist. That is the design working. A bumper that absorbs a '
                'low-speed shunt and cracks has done its job, and the crash bar behind it has '
                'stayed straight.',
                'It is also why a bumper is the panel most often repaired badly. It is the '
                'easiest to make look right in a photograph and the hardest to make right in '
                'sunlight, because plastic flexes and a filler that does not flex with it cracks '
                'along the repair line within a year.']),
        extra2=('The radar behind it, and why it has to be recalibrated',
                ['Most cars built in the last decade carry the forward radar for adaptive cruise '
                 'and autonomous emergency braking behind the front bumper, usually behind the '
                 'badge or a blanked section of grille. It is aimed, not just mounted. A bracket '
                 'that goes back a degree out points the beam at the wrong part of the road.',
                 'A car that has had a front bumper off and refitted without that radar being '
                 'checked can brake for things that are not there, or fail to see a car that is. '
                 'It is not something you will notice on the drive home, which is exactly the '
                 'problem. We check what is fitted to your car before the bumper comes off, and '
                 'we tell you up front if recalibration is part of the job rather than adding it '
                 'as a surprise at the end.',
                 'Some cars also carry a forward camera behind the windscreen that works with '
                 'that radar, and a parking camera in the grille. Those get checked too.'])),

    'rear-bumper': dict(
        name='rear bumper', slug='rear-bumper', job='panel-rear-bumper',
        material='moulded thermoplastic over a rear crash bar',
        off='It unclips and unbolts, though the boot trim usually has to come out to reach the '
            'top fixings.',
        neighbours='both rear quarters and the lower edge of the boot lid',
        behind='reversing sensors, usually a reversing camera, the reflectors, the rear crash '
               'bar, and on many cars a cut-out around a towbar or the exhaust tips',
        causes=['Reversing into posts and bollards, which cracks one corner rather than the centre.',
                'Being reversed into while parked, which pushes the centre in.',
                'Towbar loading and trailer work, which stresses the area around the mount.',
                'Tight parallel parking, which scuffs the full width at bumper height.'],
        quirk='Rear bumpers take two completely different kinds of damage and they want different '
              'work. A shunt from behind pushes the centre in and usually only needs the skin '
              'repaired and repainted. Reversing into something cracks a corner, and the corner '
              'is exactly where the mounting bracket lives, so the repair has to rebuild the '
              'fixing as well as the face.',
        risk='The towbar area, if there is one. Damage around a towbar mount can have pushed the '
             'rear crash bar, and that is structural rather than cosmetic. It is also the one '
             'place where an insurer will want it properly inspected before authorising.',
        replace='Rear bumpers on common cars are cheap enough that replacement is sometimes the '
                'sensible answer on heavy corner damage. On anything with a parking camera or an '
                'unusual finish, repair is normally better value once the parts are priced.',
        time='A corner repair is a day or two. A full bumper off, repaired and painted is two to '
             'three days.',
        damages=['smart', 'scuff', 'dent'],
        extra=('The reversing sensor problem',
               ['Almost every rear bumper now carries sensors, and they are bonded into holes '
                'moulded at specific positions. That matters for repair in a way it does not at '
                'the front: a rear bumper that has been repaired by someone who filled over a '
                'sensor aperture, or refitted a sensor at a slightly different angle, will read '
                'the ground as an obstacle and beep at nothing.',
                'We test every sensor on the car before it goes back, not just refit them. If a '
                'sensor was already failing before the accident we will tell you, rather than '
                'leaving you to find out in a car park.']),
        extra2=('Towbars, and the thing nobody checks',
                ['If your car has a towbar, the rear of the shell is a different structure. The '
                 'towbar mounts to the chassis legs through the rear crash bar, and a shunt into '
                 'a towed car or a post transmits straight into that mounting rather than being '
                 'absorbed by the bumper the way it would be on a car without one.',
                 'The bumper skin can look like the whole story and not be. We check the crash '
                 'bar and the towbar mounting on any rear impact where a towbar is fitted, '
                 'because a bent mounting is both a structural repair and a towing safety '
                 'problem, and it is the single most commonly missed thing on a rear-end job.',
                 'It also matters for the claim. An insurer will want structural damage '
                 'identified and documented properly, and finding it after the bumper has '
                 'already been painted means raising a supplementary and starting again.'])),

    'front-wing': dict(
        name='front wing', slug='front-wing', job='panel-front-wing',
        material='pressed steel on most cars, aluminium on a growing number',
        off='It unbolts. That single fact makes it one of the cheaper panels on the car to deal '
            'with, and it is why a wing and a rear quarter are not comparable jobs.',
        neighbours='the front bumper, the bonnet and the leading edge of the front door',
        behind='the arch liner, the indicator repeater on older cars, and on one side the washer '
               'bottle and often part of the air intake',
        causes=['Clipping gateposts and wing mirrors, which creases the top edge.',
                'Supermarket car parks, which dent the flat face at door height.',
                'Kerbing at an angle, which damages the lower arch lip.',
                'Corrosion along the arch lip and the bottom seam on older cars.'],
        quirk='The wing is bolted rather than welded, and that changes the economics completely. '
              'If it is beyond straightening, a replacement bolts straight on and the panel gaps '
              'can be set properly on refit. None of the welded panels on the car give you that '
              'option, which is why a wing that looks as bad as a quarter costs considerably '
              'less to put right.',
        risk='The A-pillar shut line. If the impact has pushed the back edge of the wing, check '
             'whether the door still opens and closes cleanly before anyone calls it a wing-only '
             'job. A door that catches means the damage went past the panel.',
        replace='Because it unbolts, replacement is a genuine option on a wing in a way it is not '
                'elsewhere. On a common car a new wing plus paint is sometimes cheaper than '
                'hours of straightening, and we will price both rather than assuming.',
        time='Usually two days: off the car, repaired or replaced, painted, blended into the door '
             'and bumper, refitted and the gaps set.',
        damages=['smart', 'scuff', 'dent'],
        extra=('Steel or aluminium, and why it changes the bill',
               ['A growing number of cars use aluminium wings to save weight, and an aluminium '
                'panel is a different repair. It needs different filler, different preparation, '
                'and it has to be isolated from steel tooling and steel dust, because steel '
                'particles left in aluminium start a corrosion reaction that shows up as '
                'blistering months after the car left the workshop.',
                'There is no surcharge on our rate card for aluminium. There is a difference in '
                'how it is handled, and a shop that treats the two the same is the reason some '
                'repairs bubble a year later.'])),

    'rear-quarter': dict(
        name='rear quarter panel', slug='rear-quarter', job='panel-rear-quarter',
        material='pressed steel, welded into the body shell',
        off='It does not come off. There is no unbolting a quarter panel: the work is done on the '
            'car, or a section is cut out and a replacement welded in.',
        neighbours='the roof, the rear door, the sill and the rear bumper',
        behind='the fuel filler neck on one side, the boot side trim, the rear speaker on many '
               'cars, and the seatbelt reel',
        causes=['Being hit in the rear three-quarter while parked or pulling out.',
                'Scraping along a wall or a gatepost on a tight drive.',
                'Corrosion around the arch lip and under the fuel filler flap.',
                'Damage carried through from a rear bumper impact.'],
        quirk='This is the panel people underestimate, and it is the one most often quoted wrong. '
              'A front wing unbolts; a quarter is part of the shell. It is straightened in place '
              'or cut and welded, and because it meets four other panels the paint has to blend '
              'into all of them for the repair to vanish. A quarter that has been painted up to '
              'the shut lines and no further shows as a different colour from twenty feet away '
              'on a sunny day.',
        risk='The structure behind it. A quarter takes impact into the rear of the shell, so the '
             'boot floor and the rear suspension mounting area both want checking before anyone '
             'talks about paint. This is also the panel most likely to turn a repair into a '
             'write-off decision on an older car.',
        replace='Replacement means cutting the old panel out and welding a new section in, then '
                'sealing and painting it. It is a proper job rather than a bolt-on, which is why '
                'straightening wins far more often here than on a wing.',
        time='Three to five days is normal, and more if a section has to be let in. The welding, '
             'sealing and paint all have to cure properly in sequence.',
        damages=['smart', 'scuff', 'dent'],
        extra=('Why we blend a quarter into the roof',
               ['A rear quarter is the hardest panel on the car to make disappear, because it '
                'meets more neighbours than any other panel and one of those neighbours is the '
                'roof. Stopping the paint at the join between quarter and roof puts a hard edge '
                'in the most visible place on the car, so the colour is carried up into the roof '
                'and faded out where the eye cannot find the transition.',
                'That blending is included in our figure. It is not an optional extra and we do '
                'not quote a cheaper number by leaving it out, which is worth knowing when you '
                'are comparing estimates that look different for no obvious reason.'])),

    'door': dict(
        name='door', slug='door', job='panel-door',
        material='pressed steel, with a separate outer skin on a lot of cars',
        off='It unbolts at the hinges, and on many cars the outer skin can be replaced on its own '
            'without changing the whole door.',
        neighbours='the wing or quarter ahead of it, the next door, and the sill below',
        behind='the window glass and regulator, the lock and handle mechanism, the speaker, the '
               'side impact bar, the side airbag sensor on most modern cars, and the mirror on a '
               'front door',
        causes=['Car park door dings, which are the single most common bodywork damage there is.',
                'Being opened onto a post or a high kerb.',
                'Side impacts from other vehicles pulling out.',
                'Key scratches, which usually run across more than one door.'],
        quirk='A door is the panel you look at every day, and the one where a slightly imperfect '
              'repair shows most. The shut lines either side are visible at the same time and the '
              'eye reads them against each other, so a door that sits a millimetre proud reads as '
              'wrong even to someone who could not say why.',
        risk='The side impact bar and the airbag sensor. A door that has taken a real hit rather '
             'than a car park ding needs both checked: one is structural, and the other decides '
             'whether the airbag fires when you need it to.',
        replace='A separate outer skin is the useful middle option on a door, because it replaces '
                'the damaged face without disturbing the mechanism, the wiring or the alignment. '
                'A complete door means moving everything across and setting the gaps again.',
        time='A ding is usually two days with paint. A door that needs stripping and reskinning '
             'is three.',
        damages=['smart', 'scuff', 'dent'],
        extra=('Why a door ding is not a cheap job, and why that is annoying',
               ['The most common question we get is why a dent the size of a ten pence piece '
                'costs what it does. The answer is that the dent is the small part. The trim card '
                'comes off, the water shield is peeled back and has to be resealed properly or '
                'the door leaks, the glass is lowered and supported, the metal is worked back, '
                'and then the panel is painted and blended into the wing or quarter beside it.',
                'We do not do paintless dent removal, which is the one technique that would skip '
                'most of that. We are straight about it rather than quoting a PDR price and then '
                'finding a reason it cannot be done once your car is here.'])),

    'bonnet': dict(
        name='bonnet', slug='bonnet', job='panel-bonnet',
        material='pressed steel, and aluminium on a lot of newer and premium cars',
        off='It unbolts at the hinges and goes onto a stand, which gives a flat horizontal '
            'surface to work and to paint.',
        neighbours='both front wings and the top edge of the front bumper',
        behind='the sound insulation pad, the catch and release mechanism, and the washer '
               'pipework',
        causes=['Stone chips along the leading edge, which is the most common bonnet job by far.',
                'Falling branches and garage doors, which dent the flat centre.',
                'Being leant on or sat on, which creases it in a way that is hard to pull out.',
                'Corrosion along the front edge where chips have been left to work.'],
        quirk='The bonnet is a large flat horizontal panel in full daylight, which makes it the '
              'second hardest panel on the car to match after the roof. Metallics show any '
              'difference in how the flake has laid down, and they show it from across a car '
              'park rather than up close. A bonnet is painted complete and blended into both '
              'wings for exactly that reason.',
        risk='Whether it is steel or aluminium. Aluminium needs different filler, different '
             'preparation and isolation from steel tooling, and getting that wrong causes '
             'corrosion that appears months later as blistering under the paint.',
        replace='Bonnets are available cheaply for common cars and replacement is often sensible '
                'on heavy damage. On anything where the panel is aluminium or the colour is '
                'difficult, repairing the original is usually the better outcome.',
        time='Two days for most work. A bonnet with a lot of chips is often better refinished '
             'complete than chased chip by chip, and that is still two days.',
        damages=['smart', 'scuff', 'dent'],
        extra=('Stone chips, and when to stop ignoring them',
               ['Every bonnet picks up chips along its leading edge. They are cosmetic right up '
                'until the moment they are not: once you can see brown staining in the bottom of '
                'a chip, the steel underneath has started to corrode and it spreads sideways '
                'under the paint film where you cannot see it.',
                'Caught early, chips are filled, flatted level and the area refinished. Left for '
                'a couple of winters, the same bonnet needs the leading edge cut back to clean '
                'metal first, and that is a materially bigger job. If you can see brown, it is '
                'worth doing this year rather than next.']),
        extra2=('Worth doing while the bonnet is off',
                ['A bonnet that has been refinished has a brand new paint surface on the one '
                 'panel of the car that takes the most stone damage, and it will start collecting '
                 'chips again from the first motorway run. If you are having the work done '
                 'anyway, a clear protection film along the leading edge is worth asking about, '
                 'because applying it to fresh paint is both easier and more effective than '
                 'applying it over a surface that already has chips in it.',
                 'The other thing worth doing with the bonnet off is the catch and the hinges. '
                 'They are accessible for about an hour a decade, and a bonnet that has been in '
                 'an impact frequently sits a fraction high on one side afterwards because the '
                 'hinge has moved rather than the panel. Setting the gaps properly on refit is '
                 'part of the job for us; it is also the thing most often skipped elsewhere, '
                 'because it takes time and does not show in a photograph.'])),

    'roof': dict(
        name='roof', slug='roof', job='panel-roof',
        material='pressed steel, welded to the shell along the gutters',
        off='It does not come off. Everything is done on the car.',
        neighbours='both rear quarters, both A-pillars and the windscreen surround',
        behind='the headlining, the aerial base, the interior lights and grab handles, the '
               'curtain airbags down the sides, and the sunroof mechanism where one is fitted',
        causes=['Hail, which dents the whole panel at once rather than in one place.',
                'Falling branches and masonry.',
                'Loading roof bars badly, or something sliding off them.',
                'Carrying something through a low garage opening.'],
        quirk='The largest single panel on the car and the hardest to get right. There is nowhere '
              'for a colour difference to hide on a flat horizontal surface that size, which is '
              'why a roof is painted complete and blended into both quarters rather than patched '
              'in the middle. It is also the most expensive panel on our rate card, and that is '
              'the reason why.',
        risk='The sunroof, if there is one. A dented roof around a sunroof aperture can distort '
             'the frame enough to stop it sealing, and a roof that leaks after a repair is a '
             'considerably bigger problem than the dent that started it. The curtain airbags run '
             'down the sides of the roof lining too.',
        replace='Replacing a roof skin means cutting the old one off the gutters and welding a '
                'new one on. It is done, but it is a last resort rather than a cost option, and '
                'on most cars heavy roof damage is where a write-off conversation starts.',
        time='Three to four days. The headlining often has to come down to work a dent from '
             'inside, and that adds a day on its own.',
        damages=['smart', 'scuff', 'dent'],
        extra=('Hail damage is a different problem',
               ['Hail does not make one dent, it makes two hundred small ones spread across '
                'every horizontal surface: roof, bonnet, boot lid and the tops of the wings. '
                'Counting and pricing them individually is meaningless, so hail is assessed by '
                'panel and by density rather than by dent.',
                'It is also the one kind of damage where the right answer is frequently an '
                'insurance claim even on an older car, because the total across four or five '
                'panels adds up fast. Photograph it in raking light rather than straight on, '
                'because hail is close to invisible in a flat photograph and insurers assess '
                'from photographs first.'])),

    'boot': dict(
        name='boot lid', slug='boot', job='panel-boot',
        material='pressed steel, and composite on some models',
        off='It unbolts at the hinges, though the wiring is disconnected at the plug rather than '
            'pulled through the loom.',
        neighbours='both rear quarters and the top edge of the rear bumper',
        behind='the lock mechanism, the number plate lights, the wiring loom running through the '
               'hinge, and the wiper motor on a hatchback',
        causes=['Being reversed into, which pushes the lower edge in.',
                'Closing it onto luggage, which creases the inner skin.',
                'Corrosion around the number plate lights and the lower seam.',
                'Damage carried up from a rear bumper impact.'],
        quirk='Boot lids and tailgates are mostly a question of alignment. The panel has to sit '
              'flush with two quarters and close onto a seal the whole way round, so the repair '
              'is only finished when the gaps are even and it shuts without being pushed. A boot '
              'that needs a shove is a boot that will leak.',
        risk='Water sealing. The boot is where a poor repair announces itself, because any gap in '
             'the seal puts water into the spare wheel well, and you will not find out until '
             'something in there starts to smell. We water-test a boot repair before it goes back.',
        replace='Boot lids are straightforward to replace on common cars and the alignment is '
                'easier to set on a new panel than to recover on a badly creased one. We price '
                'both where the damage is heavy.',
        time='Two to three days, including the time to set the gaps and check the seal properly.',
        damages=['smart', 'scuff', 'dent'],
        extra=('The number plate light seam',
               ['Almost every boot lid that rusts starts in the same place: the seam around the '
                'number plate lights. Water gets behind the lamp housings, sits in the lip of the '
                'seam, and works outward from the inside. By the time it bubbles on the outside '
                'face the metal behind is already thin.',
                'If your boot is bubbling along that line, it is a cut-and-repair job rather than '
                'a paint job, and filling over it buys about a year. Worth knowing before you '
                'accept a cheap quote that only addresses the face.']),
        extra2=('Hatchback tailgates are a bigger job than saloon boot lids',
                ['They get quoted as the same thing and they are not. A saloon boot lid is a '
                 'small panel with a lock and two lights on it. A hatchback tailgate carries the '
                 'rear glass, a wiper motor and its wiring, the high-level brake light, the '
                 'heated rear screen element and its connections, and a pair of gas struts that '
                 'have to be sized to the weight of the panel.',
                 'All of it comes out before paint and goes back afterwards, and the glass has '
                 'to be resealed properly or you get exactly the water problem described above. '
                 'If you are comparing quotes on a hatchback and one is noticeably cheaper, it is '
                 'worth asking whether the glass is coming out or being masked around &mdash; '
                 'masking is quicker and it leaves a paint edge at the rubber that shows as soon '
                 'as the seal moves.'])),

    'trim': dict(
        name='trim', slug='trim', job='panel-trim',
        material='plastic, sometimes textured, sometimes painted to match the body',
        off='It clips off and is prepared separately, which is why it is the cheapest bodywork on '
            'our rate card.',
        neighbours='whichever panel it is mounted on',
        behind='usually only clips and a foam pad, though a mirror housing holds the glass, the '
               'motor, the heater element and often an indicator and a camera',
        causes=['Mirror housings clipped on gateposts and in car parks.',
                'Sill covers scraped on kerbs and ramps.',
                'Arch mouldings scuffed on parking posts.',
                'Grilles cracked by stones and low-speed shunts.'],
        quirk='Trim covers a lot of small jobs that are easy to put off: mirror caps, sill '
              'covers, arch mouldings, grilles and spoilers. The main decision is almost always '
              'repair against replace, and on a common car a new moulding is sometimes cheaper '
              'than preparing and painting the old one. We check the part price before quoting a '
              'repair.',
        risk='The finish. Textured black trim cannot be polished back the way paint can, so a '
             'scuff on a textured moulding is a replace-or-repaint decision rather than a '
             'machine-polish one. Anyone who tells you they will buff a textured sill cover is '
             'going to leave it shiny in patches.',
        replace='Replacement is genuinely competitive on trim in a way it is not on panels. We '
                'price the part first and tell you honestly when buying new beats repairing.',
        time='Often same day, and next day where a painted part needs to cure.',
        damages=['smart', 'scuff', 'dent'],
        extra=('Mirror housings, which are their own little job',
               ['A wing mirror is the most commonly damaged piece of trim on any car, and it is '
                'three separate things in one housing: the painted cap, the glass, and the motor '
                'and heater behind them. Often only the cap is damaged, and a cap alone is a '
                'cheap part that takes paint well.',
                'It is worth asking specifically rather than accepting a quote for a complete '
                'mirror assembly. We will tell you which of the three actually needs replacing, '
                'and if the glass is intact and the motor still works we will say so.'])),
}

DAMAGE_LABEL = {'smart': 'Light scuff or scratch', 'scuff': 'Scuff or scratch',
                'dent': 'Dent or damaged panel'}
DAMAGE_SIZE = {'smart': 'Smaller than your phone, paint not broken through',
               'scuff': 'Bigger than your phone, or through to primer',
               'dent': 'Pushed in, creased, cracked or split'}


def panel_pages():
    out = []
    for key, P in PANELS.items():
        rows = []
        for d in P['damages']:
            lo, hi, _ = money(key, d)
            rows.append([DAMAGE_LABEL[d], DAMAGE_SIZE[d], f'{lo} &ndash; {hi}'])
        smart_lo, _, _ = money(key, 'smart')
        _, dent_hi, _ = money(key, 'dent')
        l_lo, l_hi, _ = money(key, 'dent', 'large')
        v_lo, v_hi, _ = money(key, 'dent', 'van')

        sections = [
            (f'What {P["name"]} damage costs', [
             f'Everything below is inclusive of VAT, for an ordinary five-seater, and includes '
             f'blending the paint into {P["neighbours"]}. Blending is not an extra on our rate '
             f'card.',
             ('table', (['Damage', 'What that means', 'Price inc VAT'], rows)),
             f'An SUV or estate runs {l_lo} to {l_hi} on the heaviest of those, and a van '
             f'{v_lo} to {v_hi}. Every band runs upward from the rate card rather than either '
             f'side of it: the card figure is the floor, and what we cannot know before seeing '
             f'the car is how much <em>more</em> the job is, never how much less.']),

            (f'What {P["name"]} actually is', [
             f'{P["name"].capitalize()} is {P["material"]}. {P["off"]}',
             f'Behind it sits {P["behind"]}. All of that comes out or gets protected before any '
             f'paint goes near the car, and anything electrical is tested again before you '
             f'collect it.',
             P['quirk']]),

            (f'How {P["name"]}s get damaged', [
             'Four causes account for most of what comes through the door:',
             P['causes'],
             f'<strong>The thing worth checking.</strong> {P["risk"]}']),

            ('Repair or replace', [
             P['replace'],
             f'<strong>How long it takes.</strong> {P["time"]}']),

            P['extra'],
        ]
        # Some panels carry a second long-form section, where there is a genuinely separate thing
        # worth saying. The two bumpers both have one, because without it they are the same page
        # with the word "front" swapped for "rear" - the uniqueness check flagged exactly that.
        if P.get('extra2'):
            sections.append(P['extra2'])

        faqs = [
            (f'Can you repair {P["name"]} without painting it?',
             'Only where the damage is in the lacquer alone, and we will tell you if yours is one '
             'of those rather than selling you a respray. Once it is through the colour, '
             'refinishing is the only repair that lasts. On dents there is no paint-free option '
             'at all &mdash; we do not do paintless dent removal, so the panel is straightened '
             'and then painted.'),
            (f'Will the colour match?',
             f'It is mixed to the paint code on your car, then sprayed into {P["neighbours"]} '
             f'rather than stopped at the shut line. Two cars with the same code are rarely '
             f'identical after a few years of sun, and blending is what makes the difference '
             f'invisible instead of nearly right.'),
            ('Is it guaranteed?',
             'One year on paint, three months on mechanical work, in writing.'),
            (f'Should I claim on insurance?',
             f'At {smart_lo} to {dent_hi} it is worth checking your excess first. Plenty of '
             f'single-panel jobs cost less than the excess, and paying directly avoids declaring '
             f'a claim for five years. We will price it either way and we are not on any '
             f'insurer&rsquo;s panel, so we have no reason to push you one way.'),
            ('Do you need to see the car first?',
             'Not to give you a price band &mdash; put your registration in the box above. We '
             'confirm the exact figure when we see it, because how far the damage goes is the one '
             'thing photographs do not show reliably.'),
        ]

        out.append(page(
            f'{P["slug"]}-repair-cost',
            f'{P["name"].capitalize()} Repair Cost - From £{PRICES[key + "|smart|medium"]["low"]} '
            f'| KITH Cars',
            f'What it costs to repair {P["name"]} damage, what the job involves, how long it '
            f'takes and when replacing beats repairing. Hackbridge bodyshop, any insurer.',
            f'{P["name"].capitalize()} Repair',
            f'Bodywork &middot; {P["name"].capitalize()}',
            f'{P["name"].capitalize()} is {P["material"]}, and that decides most of what a repair '
            f'costs. Here is the rate card, what we actually do to it, and when replacing is the '
            f'better answer.',
            sections, faqs,
            [('bodywork-repair-process', 'How a repair runs, step by step'),
             ('paint-colour-matching-explained', 'How paint matching works'),
             ('body-panel-repairs', 'Every panel and what it costs'),
             ('should-i-claim-or-pay-myself', 'Claim or pay yourself?')],
            key_points=[
             f'<strong>{smart_lo} to {dent_hi}</strong> inc VAT on an ordinary five-seater.',
             f'{P["off"].split(".")[0]}.',
             f'Paint blended into {P["neighbours"]} &mdash; included, never an extra.',
             'One year on paint, in writing.'],
            hub=HUB_DAMAGE, job=P['job'], category='panel',
            service_type='Vehicle body repair',
            quote_heading=f'Price your {P["name"]} now',
            note=None))
    return out


PAGES = panel_pages()
