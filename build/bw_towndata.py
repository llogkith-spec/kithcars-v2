#!/usr/bin/env python3
"""Per-town facts for the seventeen towns, researched rather than invented.

All seventeen dent pages were 97.4% identical to each other - between the Croydon and Tooting
versions of an 1,865-word page the only differences were the town name, "15" against "18"
minutes, and two road numbers. This is the data that makes them genuinely different pages.

Collision figures are DfT STATS19 data as presented by crashview.co.uk, taken at postcode-district
and borough level. Per-address counts from that source are deliberately unused: a single address
showing thousands of collisions is a geocoding artefact.

An honest caveat that appears on the pages themselves: postcode districts do not map exactly onto
towns. SW16 covers Streatham and Norbury; SM6 covers Wallington and Beddington. Where two towns
share a district the page says so rather than implying the figure is the town's alone.

Parking figures are the London Borough of Sutton's own ward-level parking surveys, which exist
for the Sutton towns only.

`character` and `damage` are the parts that carry each page. They describe what the place is
physically like and what that does to cars - a dense Victorian terrace with no driveways produces
different damage from a 1930s semi with one, and both differ from an arterial road with bus lanes.
"""

# borough totals, for context on each page
BOROUGH = {
    'Croydon': dict(collisions='35,329', casualties='43,163', serious='4,628',
                    roads=[('A23', '4,571'), ('A235', '3,011'), ('A212', '2,586')]),
    'Sutton': dict(collisions='11,569', casualties='14,236', serious='1,588',
                   roads=[('A232', '1,438'), ('A217', '1,025'), ('B2230', '992')]),
    'Merton': dict(collisions='12,428', casualties='14,665', serious='1,671',
                   roads=[('A217', '1,434'), ('A24', '1,373'), ('A238', '1,104')]),
}

TOWNS = {
    'hackbridge': dict(
        name='Hackbridge', borough='Sutton',
        pc='SM6', pc_n='2,543', shared='Wallington and Beddington, so the figure covers all three',
        mins='0',
        character='Hackbridge is where our workshop is. Unit 1 Soho Mills sits on London Road, a '
                  'couple of minutes from the station, so the damage we see from here is not '
                  'damage that travelled to us.',
        damage='It is almost entirely low-speed and almost entirely parked. Sutton Council&rsquo;s '
               'ward parking survey for Wandle ward, which is Hackbridge, found 67 per cent of '
               'residents saying their street has a parking problem, 39 per cent parking on the '
               'road and 74 per cent saying the trouble is on weekdays. Add the Felnex and New '
               'Mill Quarter schemes putting over eleven hundred new homes into a suburb whose '
               'central parade is Edwardian, and the result is streets parked solid and years of '
               'delivery and contractor traffic squeezing through them.',
        parking={'ward': 'Wandle', 'problem': '67', 'two_cars': '37',
                 'on_street': '39',
                 'streets': 'London Road, Hackbridge Road, Nightingale Road and Corbet Close'}),
    'croydon': dict(
        name='Croydon', borough='Croydon', pc='CR0', pc_n='11,524', shared=None, mins='15',
        character=(
            'Croydon is the busiest place on our patch for collisions by a wide margin, and CR0 '
            'alone records more than the whole of the London Borough of Sutton. The A23 running '
            'through it carries more collisions than any other road in the borough.'),
        damage=(
            'What that means for dents is stop-start traffic damage: low-speed shunts on the '
            'Brighton Road, creased rear quarters from the Fiveways and Lombard roundabouts, and '
            'a steady run of multi-storey damage from the Whitgift and Centrale car parks. The '
            'shunts are the ones worth taking seriously - a rear bumper pushed in at walking pace '
            'can still have bent the crash bar behind it.'),
    ),

    'thornton-heath': dict(
        name='Thornton Heath', borough='Croydon', pc='CR7', pc_n='2,752', shared=None, mins='18',
        character=(
            'CR7 is the second busiest postcode district in the borough for collisions after CR0 '
            'itself. Thornton Heath is dense, largely Victorian and Edwardian terraces, and the '
            'High Street and London Road carry heavy bus traffic through it.'),
        damage=(
            'Terraced streets with no off-road parking are where the everyday dent comes from: '
            'doors opened into the car alongside, mirrors clipped by passing vans, and the long '
            'crease down a flank that comes from squeezing past a parked car on a road that is '
            'really only wide enough for one. Pond-area traffic adds the low-speed shunt.'),
    ),

    'purley': dict(
        name='Purley', borough='Croydon', pc='CR8', pc_n='2,428', shared=None, mins='20',
        character=(
            'Purley sits in a valley with the A23 running through the middle of it and steep '
            'residential roads climbing away on both sides. CR8 records the third highest '
            'collision count in the borough.'),
        damage=(
            'The hills matter more than people expect. Cars parked on a camber get doors opened '
            'downhill into them with real weight behind the swing, which is a deeper dent than '
            'the flat-ground equivalent. Steep driveways produce bumper and sill damage on the '
            'way out, and the descents into the valley put brake dust onto lower panels, which '
            'is a separate paint problem we often find alongside the dent.'),
    ),

    'coulsdon': dict(
        name='Coulsdon', borough='Croydon', pc='CR5', pc_n='1,159', shared=None, mins='25',
        character=(
            'Coulsdon is the quietest of the Croydon postcodes on our patch, with CR5 recording '
            'about a tenth of CR0. It is also the most open - the Brighton Road runs south '
            'towards the downs and the roads out of the town carry faster traffic than anywhere '
            'else we cover.'),
        damage=(
            'Fewer collisions but a different profile when they happen. Faster roads mean more '
            'genuine impact damage and less car park scuffing, so a Coulsdon dent is more often '
            'part of a wider repair with structural questions behind it. The lanes towards '
            'Farthing Downs also bring in hedge and verge damage down one side, which is '
            'scratching as much as denting.'),
    ),

    'norbury': dict(
        name='Norbury', borough='Croydon', pc='SW16', pc_n='1,553',
        shared='Streatham, so the figure covers both', mins='20',
        character=(
            'Norbury sits on the A23 London Road with the railway running alongside it, and '
            'shares the SW16 postcode with Streatham. It is terraced, tightly parked and bisected '
            'by one of the busiest roads in south London.'),
        damage=(
            'The A23 frontage produces a particular kind of damage: cars parked on the main road '
            'being clipped by traffic that is moving faster than the gap allows. Nearside mirrors '
            'and front wings take most of it. Behind the main road the side streets are classic '
            'terrace parking, which means door dings and the slow scrape of getting into a space '
            'that is a foot too short.'),
    ),

    'sutton': dict(
        name='Sutton', borough='Sutton', pc='SM1', pc_n='2,742', shared=None, mins='10',
        character=(
            'SM1 records the highest collision count in the borough, and Sutton town centre is '
            'the densest concentration of car parks on our patch. The A232 is the road that '
            'collects most of the borough&rsquo;s collisions.'),
        damage=(
            'Town centre parking damage dominates: the St Nicholas and Times Square multi-storeys '
            'come up by name more than anywhere else. Tight bays, concrete pillars and ramps that '
            'catch a lower bumper edge. The upside is that almost all of it happens slowly, so it '
            'is paint and panel rather than structure - which is the cheaper end of our rate '
            'card and often a same-week job.'),
        parking=None),

    'carshalton': dict(
        name='Carshalton', borough='Sutton', pc='SM5', pc_n='1,706', shared=None, mins='8',
        character=(
            'Carshalton sits between the A232 and the B2230, and most of the damage we see from '
            'there comes from neither. It comes from the streets in between.'),
        damage=(
            'The council&rsquo;s own survey found 55 per cent of residents saying their street '
            'has a parking problem, 56 per cent parking at least one car on the road, and the '
            'commonest complaint being non-residents - commuters, school runs and football. A '
            'street full of cars parked by people in a hurry is exactly where doors get opened '
            'into the car alongside and mirrors get taken off.'),
        parking=dict(ward='Carshalton Central', problem='55', two_cars='41', on_street='56',
                     streets='Carshalton Park Road, Wallace Crescent, Blakehall Road and Ruskin '
                             'Road'),
    ),

    'cheam': dict(
        name='Cheam', borough='Sutton', pc='SM3', pc_n='1,850', shared=None, mins='12',
        character=(
            'Cheam runs the opposite way to what you would guess, and the council&rsquo;s own '
            'figures show it.'),
        damage=(
            'Cheam households own <em>more</em> cars than Carshalton ones - 61 per cent have two '
            'or more against 41 per cent - and yet only 34 per cent park on the street against 56 '
            'per cent in Carshalton. Cheam has driveways. That changes the damage completely: far '
            'less door-to-door contact and fewer clipped mirrors, and instead gatepost scrapes on '
            'the nearside and reversing damage on drives that were laid out for one car in 1935 '
            'and now hold two.'),
        parking=dict(ward='Cheam', problem='44', two_cars='61', on_street='34',
                     streets='Matlock Crescent, Burdon Lane, Kingsdown Road and Tilehurst Road'),
    ),

    'wallington': dict(
        name='Wallington', borough='Sutton', pc='SM6', pc_n='2,543',
        shared='Beddington, so the figure covers both', mins='5',
        character=(
            'Wallington is our own postcode - the workshop is in SM6 - and it is the second '
            'busiest district in the borough for collisions after Sutton itself. Woodcote Road '
            'and Stafford Road carry the traffic.'),
        damage=(
            'Being five minutes away, we see more Wallington cars than anywhere else, and the mix '
            'is the broadest: station parking damage around the Woodcote Road end, terrace door '
            'dings off the side streets, and supermarket car park work. It is also the town where '
            'people most often bring us a dent the same day they get it, which genuinely matters '
            'on a dent with the paint broken - sealed quickly, it does not start rusting while '
            'you decide.'),
    ),

    'beddington': dict(
        name='Beddington', borough='Sutton', pc='SM6', pc_n='2,543',
        shared='Wallington, so the figure covers both', mins='5',
        character=(
            'Beddington shares SM6 with Wallington, but it is a different place to drive in. The '
            'industrial estate and the Croydon Road corridor dominate it, and there is far more '
            'commercial traffic than residential parking pressure.'),
        damage=(
            'That shows in what arrives: more vans than cars, and van damage is its own category. '
            'Sliding door tracks, rear corners taken out on loading bays, and sill damage from '
            'kerbing at delivery stops. A van panel is usually larger and flatter than a '
            'car&rsquo;s, which makes a dent in the middle of one harder to make invisible and is '
            'why our rate card carries a van band rather than pretending it is the same job.'),
    ),

    'rosehill': dict(
        name='Rosehill', borough='Sutton', pc='SM4', pc_n='762', shared=None, mins='10',
        character=(
            'Rosehill is built around its roundabout, where the A217 meets the A297, and SM4 on '
            'the Sutton side records the lowest collision count of any district we cover apart '
            'from Worcester Park.'),
        damage=(
            'The roundabout is the thing. Multi-lane roundabouts produce side-swipes rather than '
            'head-on damage - a long crease down a flank where someone changed lanes into the '
            'space you were occupying. That is a harder repair than a straightforward dent, '
            'because a crease has stretched the metal and it crosses more than one panel more '
            'often than not.'),
    ),

    'worcester-park': dict(
        name='Worcester Park', borough='Sutton', pc='KT4', pc_n='375', shared=None, mins='15',
        character=(
            'KT4 records the fewest collisions of any district on our patch, by some distance. '
            'Worcester Park is largely interwar suburban housing with the station and the Central '
            'Road shops as the only real congestion.'),
        damage=(
            'Low collision numbers and plenty of driveways mean the dents we see are domestic '
            'rather than road-traffic: garage door frames, gateposts, and the slow reverse into '
            'something that was always there. Station parking around Central Road is the one '
            'exception and produces the usual commuter car park damage.'),
    ),

    'mitcham': dict(
        name='Mitcham', borough='Merton', pc='CR4', pc_n='3,229', shared=None, mins='15',
        character=(
            'CR4 is the second busiest district in Merton after Wimbledon, with 3,229 recorded '
            'collisions. Mitcham has the A217 and the A236 running through it and a large amount '
            'of through traffic for its size.'),
        damage=(
            'A lot of Mitcham work arrives via the tram and the Common - roads that are wide '
            'enough to feel fast and narrow enough to catch you out where they pinch. The damage '
            'skews towards nearside front corners, which is the classic signature of misjudging a '
            'gap rather than being hit. There is also a steady run of commercial vehicle work off '
            'the industrial estates.'),
    ),

    'morden': dict(
        name='Morden', borough='Merton', pc='SM4', pc_n='1,683', shared=None, mins='15',
        character=(
            'Morden is the end of the Northern Line, and that single fact shapes the driving. SM4 '
            'records 1,683 collisions on the Merton side, and the town centre carries the '
            'traffic of everyone who drives to the tube and leaves the car there.'),
        damage=(
            'Station car park damage is the Morden signature: cars left all day in tightly '
            'marked bays, with every other driver in a hurry at both ends of the day. Door dings '
            'and mirror damage dominate, and because the car sat there for ten hours nobody ever '
            'sees who did it. That makes most Morden dents an uninsured-loss conversation rather '
            'than a claim, which usually means paying directly is the better answer.'),
    ),

    'wimbledon': dict(
        name='Wimbledon', borough='Merton', pc='SW19', pc_n='4,493', shared=None, mins='20',
        character=(
            'SW19 records 4,493 collisions, the highest of any district in Merton and more than '
            'any Sutton district. Wimbledon carries town-centre congestion, the A219 and A238, '
            'and two weeks a year when the traffic is unlike anywhere else in the country.'),
        damage=(
            'Wimbledon cars are on average newer, more expensive and more difficult to paint than '
            'the rest of our patch - more metallics, more pearls, more aluminium panels. That '
            'does not change the dent, but it changes the repair: matching and blending matter '
            'more, aluminium needs different preparation and isolation from steel tooling, and a '
            'three-stage pearl has to be sprayed out on a test card before it goes near the car.'),
    ),

    'streatham': dict(
        name='Streatham', borough=None, pc='SW16', pc_n=None,
        shared='Norbury', mins='22',
        character=(
            'Streatham is the A23 for most of its length - one of the busiest roads in south '
            'London running straight through the middle of a dense, tightly parked, largely '
            'Victorian area. It shares the SW16 postcode with Norbury.'),
        damage=(
            'Bus lanes are the thing that makes Streatham different. A bus lane puts large '
            'vehicles close to parked cars for miles, and the nearside mirror is the first thing '
            'to go. Behind the High Road the side streets are terraces with no off-road parking, '
            'so the everyday damage is door-to-door. Between the two, Streatham sends us more '
            'mirror and front-wing work than anywhere else we cover.'),
    ),

    'tooting': dict(
        name='Tooting', borough=None, pc='SW17', pc_n=None,
        shared=None, mins='25',
        character=(
            'Tooting is the furthest town we cover and the densest. Victorian terraces almost '
            'throughout, very little off-road parking, controlled parking zones across most of '
            'it, and a high street that is busy at every hour.'),
        damage=(
            'Parking density is everything here. Where nearly every household parks on the road '
            'and spaces are fought over, cars get into gaps they do not really fit, and the '
            'damage follows: bumper corners, creased rear quarters from reversing onto a dropped '
            'kerb, and doors opened into the car behind. It is also the town where we most often '
            'see damage that has been left for months, because finding somewhere to be without '
            'the car is itself difficult.'),
    ),
}
