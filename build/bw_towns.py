#!/usr/bin/env python3
"""Real local facts per town, and the section they build.

The 111 bodywork town pages measure 71.6% word-for-word identical to each other. They are not
badly written - several carry a genuinely local paragraph - but the local part is garnish and the
template is the meal, so they read as one page with the town name swapped. That is the pattern
Google's scaled-content policy is aimed at, and it is why bodywork is not ranking locally.

The fix is not more town pages. There are already around fifty per town across seventeen towns.
It is to give the existing ones something true that is different in every one.

Sources, all public:

  collisions   crashview.co.uk, which presents DfT STATS19 road casualty data by region, town,
               road and postcode district. Road-level and postcode-level figures are used. The
               per-address counts on that site are not: a single address showing 2,365 collisions
               is a geocoding artefact, not a fact about that address, and publishing it would be
               wrong.
  parking      London Borough of Sutton's own ward-level parking surveys, which record how many
               households report a parking problem, how many cars they have and how many park on
               the street.

Every figure below is attributed on the page itself, so a reader can check it rather than take
our word, and so it is obvious this is researched rather than invented.
"""

TOWNS = {
    'croydon': dict(
        name='Croydon', borough='Croydon',
        collisions='35,329', casualties='43,163', serious='4,628',
        road='A23', road_n='4,571',
        road2='A235', road2_n='3,011',
        postcode='CR0', postcode_n='11,524',
        source='crashview.co.uk, from DfT STATS19 data',
        colour=(
            'Croydon is the busiest place on our patch for collisions by a wide margin, and the '
            'A23 running through it carries more of them than any other road in the borough. '
            'That shows up in the work: more genuine accident damage, more claims, and more cars '
            'arriving with structural questions behind what looks like a bumper job.'),
        parking=None,
        note=(
            'Croydon also means the Fiveways and Lombard roundabouts, and a lot of stop-start '
            'traffic on the Brighton Road. Low-speed shunts are the signature damage - rear '
            'bumper pushed in, crash bar behind it bent, and an insurer who wants photographs '
            'before anyone touches it.')),

    'sutton': dict(
        name='Sutton', borough='Sutton',
        collisions='11,569', casualties='14,236', serious='1,588',
        road='A232', road_n='1,438',
        road2='A217', road2_n='1,025',
        postcode='SM1', postcode_n='2,742',
        source='crashview.co.uk, from DfT STATS19 data',
        colour=(
            'Sutton records roughly a third of Croydon&rsquo;s collisions, and the A232 is the '
            'road that collects most of them. The High Street end and the multi-storeys behind '
            'it generate a different kind of damage from the main roads: corner scrapes, kerbed '
            'alloys and the long low graze that comes from a parking ramp.'),
        parking=None,
        note=(
            'The St Nicholas and Times Square car parks are the two we hear named most often. '
            'Tight bays and a ramp that catches lower bumper edges, and because it happens slowly '
            'the damage is usually paint and plastic rather than anything structural.')),

    'carshalton': dict(
        name='Carshalton', borough='Sutton',
        collisions='11,569', casualties='14,236', serious='1,588',
        road='A232', road_n='1,438',
        road2='B2230', road2_n='992',
        postcode='SM5', postcode_n='1,706',
        source='crashview.co.uk, from DfT STATS19 data',
        colour=(
            'Carshalton sits on the A232 and the B2230, and the damage we see from there is '
            'mostly not from either of them. It comes from the streets in between.'),
        parking=dict(
            ward='Carshalton Central',
            problem='55', two_cars='41', on_street='56',
            streets='Carshalton Park Road, Wallace Crescent, Blakehall Road, Ruskin Road and '
                    'Salisbury Road',
            source='London Borough of Sutton parking survey, Carshalton Central ward report'),
        note=(
            'Fifty-six per cent of households there park at least one car on the road, and the '
            'commonest complaint in the council&rsquo;s own survey was non-residents parking - '
            'commuters, school runs and football. A street full of cars parked by people in a '
            'hurry is where wing mirrors go and where doors get opened into the car alongside.')),

    'cheam': dict(
        name='Cheam', borough='Sutton',
        collisions='11,569', casualties='14,236', serious='1,588',
        road='A232', road_n='1,438',
        road2='A217', road2_n='1,025',
        postcode='SM3', postcode_n='1,850',
        source='crashview.co.uk, from DfT STATS19 data',
        colour=(
            'Cheam is the interesting one, because the numbers run the opposite way to what you '
            'would guess.'),
        parking=dict(
            ward='Cheam',
            problem='44', two_cars='61', on_street='34',
            streets='Matlock Crescent, Burdon Lane, Kingsdown Road, Peaches Close and Tilehurst '
                    'Road',
            source='London Borough of Sutton parking survey, Cheam ward report'),
        note=(
            'Cheam households own <em>more</em> cars than Carshalton ones - 61 per cent have two '
            'or more against 41 per cent - and yet only a third park on the street, against more '
            'than half in Carshalton. Cheam has driveways. That changes the damage: less '
            'door-to-door contact and fewer clipped mirrors, more gatepost scrapes on the '
            'nearside and more reversing damage on driveways that were laid out for one car and '
            'now hold two.')),
}


def section(key):
    """The local block for a town page. Returns (heading, [blocks]) or None."""
    T = TOWNS.get(key)
    if not T:
        return None

    blocks = [T['colour']]

    rows = [
        ['Recorded collisions in ' + T['borough'], T['collisions']],
        ['Casualties', T['casualties']],
        ['Serious collisions', T['serious']],
        ['Busiest road', T['road'] + ' &mdash; ' + T['road_n']],
        ['Next busiest', T['road2'] + ' &mdash; ' + T['road2_n']],
        ['Postcode district', T['postcode'] + ' &mdash; ' + T['postcode_n']],
    ]
    blocks.append(('table', (['', 'Figure'], rows)))
    blocks.append('<small>Road casualty figures from ' + T['source'] + '. Counts are for the '
                  'borough rather than the town alone, and cover the full recorded period.</small>')

    if T['parking']:
        P = T['parking']
        blocks.append(
            '<strong>What the council&rsquo;s own parking survey found in ' + P['ward'] +
            '.</strong> ' + P['problem'] + ' per cent of residents said their street has a '
            'parking problem, ' + P['two_cars'] + ' per cent of households have two or more cars, '
            'and ' + P['on_street'] + ' per cent park at least one of them on the road. The '
            'streets that answered in the greatest numbers were ' + P['streets'] + '.')
        blocks.append('<small>' + P['source'] + '.</small>')

    blocks.append(T['note'])
    return ('What we actually see from ' + T['name'], blocks)
