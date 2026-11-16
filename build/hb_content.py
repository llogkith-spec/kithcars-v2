#!/usr/bin/env python3
"""Hackbridge local content, by service group.

Hackbridge had no pages at all, which is the biggest local gap on the site: the workshop is at
Unit 1 Soho Mills on London Road and we rank for nothing in the place we physically occupy.

These pages are not town-swaps of the Carshalton ones and must not read like them. Hackbridge is
where we are, so there is no journey to describe - that whole section is replaced rather than
reworded. What goes in its place is the thing only we can write: the street, the yard, and what
walking in actually looks like.

Facts used, all public and all attributed on the page:

  development   Wikipedia on Hackbridge: the former Felnex industrial estate, about a million
                square feet, approved by the GLA in 2016 for 725 homes plus a supermarket,
                surgery, care home and bus interchange; the neighbouring New Mill Quarter adds
                440. That is 1,165 homes into a suburb whose central parade is Edwardian.
  parking       London Borough of Sutton's ward parking survey for Wandle ward, which is
                Hackbridge: 67% say their street has a parking problem, 39% park on the street,
                and 74% say the problem is on weekdays.
  station       Hackbridge is Zone 4, about 25 minutes to Victoria, on Thameslink and Southern.
                This is the load-bearing fact for DPFs, batteries and exhausts: a suburb full of
                people driving a mile to a station and leaving the car there is a suburb full of
                engines that never reach temperature.
  collisions    DfT STATS19 via crashview.co.uk, at borough and road level only. Sutton: 11,569
                collisions and 1,588 serious. Per-address counts on that site are a geocoding
                artefact and are not used.

The station fact is the one worth leaning on, because it is true, checkable, specific to a
commuter suburb, and it explains a real pattern of failure rather than decorating the page.
"""

NAME = 'Hackbridge'
SLUG = 'hackbridge'
PC = 'SM6'
BOROUGH = 'Sutton'

# Short attributions, used inline so a reader can check rather than take our word.
SRC_PARK = ('<a href="https://www.sutton.gov.uk/w/parking-review" target="_blank" '
            'rel="noopener">Sutton Council&rsquo;s own ward parking survey</a>')
SRC_DEV = ('<a href="https://en.wikipedia.org/wiki/Hackbridge" target="_blank" '
           'rel="noopener">the published figures for the Felnex and New Mill schemes</a>')

# ---------------------------------------------------------------------------------------------
# The local section. One per service group, each built on a different true fact about the place
# rather than the same paragraph with a noun swapped.
# ---------------------------------------------------------------------------------------------

LOCAL = {

 'emissions': ('Why Hackbridge is hard on diesels', """
<p>Hackbridge is a commuter suburb with a Zone 4 station on it. The train takes about 25 minutes
to Victoria, and Thameslink and Southern between them run to Blackfriars, London Bridge, Sutton,
Wimbledon and up to St Albans and Luton. A great many cars around here exist to cover the mile
between a front door and that station car park, twice a day.</p>
<p>That is the single worst duty cycle you can give a modern diesel. A diesel particulate filter
clears itself by running hot enough to burn off what it has collected, and it only gets there on
a sustained run. A one-mile crawl to the station never gets the exhaust to temperature, so the
filter fills, the car starts a regeneration it cannot finish, and the soot load climbs until a
light comes on. The same journey leaves unburnt fuel in the oil and rots exhaust sections from
the inside, because condensation never dries out of them.</p>
<p>It is why we see far more blocked filters from a mile of Hackbridge than from cars that do
thirty miles of A217 a day, and why the honest first question we ask is what the car actually
does in a week rather than what it is capable of. A filter cleaned without changing anything
about the driving is a filter that blocks again.</p>
<p>The flat ground does not help either. The Wandle valley floor through here is level, so
nothing in normal local driving puts the engine under sustained load. Load is what generates
heat, and heat is what keeps the system clear.</p>"""),

 'servicing': ('What Hackbridge driving does between services', """
<p>The typical Hackbridge car does short journeys. The station is a few minutes away and takes
about 25 minutes off you to Victoria, the shops on the London Road parade are walkable, and the
rest is a run to Sutton or Wallington and back. Very little of that gets an engine properly warm.</p>
<p>Short-hop driving changes what wears. Oil stays contaminated for longer because it never gets
hot enough to drive off the moisture and fuel that collect in it, which is why a car doing 4,000
short miles a year can need its oil changed on time rather than on mileage. Batteries never fully
recover their charge. Brake discs surface-rust between uses and get scored by it. Exhausts corrode
from the inside out.</p>
<p>None of that is a reason to service more often for the sake of it. It is a reason to service
on the right schedule for how the car is actually used, which for a lot of cars around here is
the time interval rather than the mileage one. We will tell you which applies to yours rather
than defaulting to whichever is further away.</p>
<p>It also means the inspection matters more than the oil. On a low-mileage local car the things
that fail are the things that rot and seize rather than the things that wear out, and those are
found by looking.</p>"""),

 'bodywork': ('Why Hackbridge produces the damage it does', """
<p>Two things are happening to this place at once, and both end up on panels.</p>
<p>The first is the building. The old Felnex estate was about a million square feet of industry
and, per {dev}, was approved in 2016 for 725 homes plus a supermarket, a surgery, a care home and
a bus interchange. New Mill Quarter adds another 440. That is over eleven hundred homes going
into a suburb whose central parade is Edwardian and was laid out for a fraction of the traffic,
and it brings years of construction vehicles, delivery vans and contractor pickups through
streets that were not drawn for them.</p>
<p>The second is where all those cars end up overnight. {park} for Wandle ward, which is
Hackbridge, found 67 per cent of residents saying their street has a parking problem, 39 per cent
parking on the street, and 74 per cent saying the trouble is on weekdays. A street parked solid
on both sides is where mirrors get clipped, where doors get opened into the car alongside, and
where a van reversing to a door takes a corner off something.</p>
<p>Which is why the bulk of what comes through our door from a hundred yards away is low-speed
and cosmetic rather than dramatic. Scuffed bumpers, creased doors, kerbed wheels, mirror casings.
Not motorway damage. Parked-up, built-up, somebody-was-in-a-hurry damage.</p>"""),

 'drivetrain': ('Short runs, flat ground and what gives out first', """
<p>Hackbridge sits on the floor of the Wandle valley, and the river runs about four hundred
metres south of the station. Flat ground, short distances, and a railway station that puts you in
Victoria in around 25 minutes, so a lot of local cars cover one mile at a time and spend the rest
of the day parked.</p>
<p>That pattern decides what fails. It is not the long-mileage wear you get on a car doing the
A217 every day. It is the stop-start count: every junction on London Road, every queue at the
level crossing, every three-point turn out of a packed residential street. A clutch wears by
slipping, and slipping happens at low speed in traffic rather than at seventy in sixth.</p>
<p>The same goes for anything that is cycled rather than simply rotated. Dual-mass flywheels take
their punishment from repeated take-up, not from distance. Gearbox synchros suffer in traffic.
Engine mounts tire from being loaded and unloaded at junctions. A ten-year-old Hackbridge car with
forty thousand miles on it has done far more work than the number suggests.</p>
<p>So when we quote on something in this category we look at how the car is used rather than only
at the odometer, because on a local car the two tell different stories.</p>"""),

 'electrical': ('The battery problem in a commuter suburb', """
<p>Hackbridge is a station town. Zone 4, about 25 minutes to Victoria, Thameslink and Southern,
and a great many residents who drive a mile to the station and leave the car standing until the
evening. In winter that car is started cold, run for four minutes, and parked.</p>
<p>A four-minute run does not put back what starting takes out, particularly with heated screens,
lights and a blower all on. The battery sits slightly flat, and a battery that sits slightly flat
sulphates and loses capacity permanently. That is why batteries around here fail at three years
rather than five, and why the failure arrives in the first properly cold week rather than
gradually.</p>
<p>It also disguises other faults. A small parasitic drain, an alternator that is not quite
charging, a dying earth, all of them look exactly like a tired battery on a car that never gets a
decent run. Replacing the battery makes the symptom go away for a few weeks and then it comes
back, which is why the test matters more than the part.</p>
<p>We check the charging side and the drain before selling anybody a battery, because on this
driving pattern the battery is as often the victim as the culprit.</p>"""),

 'chassis': ('The roads immediately around us', """
<p>Across the borough, DfT collision data published through crashview.co.uk records 11,569
collisions in Sutton, 14,236 casualties and 1,588 serious ones, with the A232 at 1,438 and the
A217 at 1,025 the two that carry the most. Hackbridge sits off that main network rather than on
it, and the local driving is the slow sort: London Road, the parade, the level crossing, and
residential streets parked solid on both sides.</p>
<p>Slow driving is not kind to suspension and steering. It is kerbs that do the damage &mdash;
pulling into a gap barely longer than the car, squeezing past something double-parked, mounting a
kerb to let a delivery lorry through. A hard kerb strike at five miles an hour puts a shock into
a wishbone, a track rod and a wheel bearing that thirty miles of dual carriageway never will.</p>
<p>Add the building traffic from the Felnex and New Mill sites and the surface of the local roads
has taken a beating with it. Potholes, patched trenches and sunken ironwork all land through the
same components.</p>
<p>So the symptom we hear most around here is not a vague motorway wobble. It is a knock over the
bumps on a residential street, or a car that has pulled to one side ever since a kerb.</p>"""),

 'tyres': ('Kerbs, not mileage', """
<p>{park} for Wandle ward, which covers Hackbridge, found 67 per cent of residents reporting a
parking problem on their street, 39 per cent parking on the road and nearly nine in ten households
with at least one car. The Edwardian streets off London Road were laid out before any of that,
and the result is parking spaces that are exactly as long as a car and no longer.</p>
<p>Tyres and wheels pay for it. Kerbing a sidewall while reversing into a tight gap is the single
commonest thing we see on local cars, and a kerbed sidewall is not a cosmetic matter: the cords
inside it are what hold the tyre together and a scuff deep enough to show them is a tyre that
needs replacing rather than watching.</p>
<p>The alignment goes the same way. A kerb hard enough to mark an alloy is usually hard enough to
move the tracking, and once the tracking is out the tyre wears across its width instead of evenly.
People replace a worn tyre, do not check why it wore, and replace the next one early too.</p>
<p>Which is why on anything that has been kerbed we would rather look at the geometry than just
sell a tyre. The tyre is the symptom.</p>"""),

 'marque': ('{marque} drivers in Hackbridge', """
<p>Hackbridge has more newer cars in it than it did five years ago, and the reason is on the
ground: per {dev}, the old Felnex estate was approved in 2016 for 725 homes plus a supermarket,
surgery, care home and bus interchange, and New Mill Quarter adds another 440. Over eleven hundred
new homes bring newer cars, finance agreements and warranties with them.</p>
<p>Which raises the question people ask us most about a car still under warranty: does an
independent garage void it? It does not. Servicing to the manufacturer&rsquo;s schedule, with
parts of matching quality and the work recorded, keeps the warranty intact. That is the position
in law and it has been for years.</p>
<p>What we do not do is pretend to be something we are not. We are on no manufacturer scheme and
no insurer panel, and we will say so before you ask. What we do is diagnose properly, use the
right specification of part and oil for the car rather than whatever is on the shelf, and record
the work so the service history stands up when you sell it.</p>
<p>And we are a few minutes away rather than a trip to a dealer on a ring road somewhere, which
on a routine service is most of the point.</p>"""),

 'recovery': ('Based on London Road, not dispatched to it', """
<p>Our yard is on London Road in Hackbridge, which puts us a couple of minutes from the station,
the parade and the level crossing, and a short run from the A237 and the A217 beyond it.</p>
<p>That matters more for recovery than for anything else we do, because recovery is the one
service where the distance to you is the service. We are not a call centre passing your job to
whoever is nearest and taking a cut. If you have broken down in Hackbridge, Wallington, Carshalton
or Mitcham, the truck coming to you is ours and it is starting from here.</p>
<p>It also means a car can come straight back to our own workshop rather than to a compound to
wait. If the fault is something we can put right, it is already in the right place and nobody is
paying twice to move it.</p>
<p>And if you are local and the car will not start, it is worth a phone call before a recovery at
all. A fair number of the jobs we get called out for around here are a flat battery on a car that
only ever does the station run, which is a jump and a conversation rather than a tow.</p>"""),
}

# Which group each service belongs to. Anything not listed falls back to 'servicing'.
GROUP = {
 'dpf-cleaning': 'emissions', 'adblue-solutions': 'emissions', 'exhaust-repairs': 'emissions',
 'car-servicing': 'servicing', 'full-service': 'servicing', 'interim-service': 'servicing',
 'major-service': 'servicing', 'van-servicing': 'servicing', 'fleet-servicing': 'servicing',
 'oil-filter-change': 'servicing', 'air-filter-replacement': 'servicing',
 'cabin-filter-replacement': 'servicing', 'mot-testing': 'servicing',
 'pre-purchase-inspection': 'servicing', 'ac-regas': 'servicing',
 'accident-repairs': 'bodywork', 'bumper-repair': 'bodywork', 'car-respray': 'bodywork',
 'dent-repair': 'bodywork', 'scratch-repair': 'bodywork', 'smart-repairs': 'bodywork',
 'headlight-restoration': 'bodywork', 'welding-rust-repair': 'bodywork',
 'clutch-replacement': 'drivetrain', 'cambelt-replacement': 'drivetrain',
 'timing-chain-replacement': 'drivetrain', 'head-gasket-replacement': 'drivetrain',
 'engine-replacement': 'drivetrain', 'gearbox-services': 'drivetrain',
 'turbo-replacement': 'drivetrain', 'oil-leak-repair': 'drivetrain', 'ecu-remap': 'drivetrain',
 'engine-diagnostics': 'electrical', 'battery-electrical': 'electrical',
 'alternator-replacement': 'electrical', 'abs-sensor-replacement': 'electrical',
 'brake-repairs': 'chassis', 'suspension-repairs': 'chassis', 'wheel-bearings': 'chassis',
 'tyre-fitting': 'tyres', 'wheel-alignment': 'tyres',
 'alloy-wheel-refurbishment': 'tyres',
 'alfa-romeo-garage': 'marque', 'audi-garage': 'marque', 'bmw-garage': 'marque',
 'bmw-specialist': 'marque', 'citroen-garage': 'marque', 'fiat-garage': 'marque',
 'vehicle-recovery': 'recovery', 'vehicle-hire': 'recovery',
}

MARQUE = {'alfa-romeo-garage': 'Alfa Romeo', 'audi-garage': 'Audi', 'bmw-garage': 'BMW',
          'bmw-specialist': 'BMW', 'citroen-garage': 'Citro&euml;n', 'fiat-garage': 'Fiat'}


def local_section(slug, svc_name):
    """(heading, html) for this service's Hackbridge section."""
    g = GROUP.get(slug, 'servicing')
    heading, body = LOCAL[g]
    fields = dict(svc=svc_name, svc_low=svc_name.lower(), park=SRC_PARK, dev=SRC_DEV,
                  marque=MARQUE.get(slug, svc_name))
    return heading.format(**fields), body.strip().format(**fields)


# ---------------------------------------------------------------------------------------------
# Replaces the "From <Town> to our Hackbridge workshop" section, which makes no sense here.
# ---------------------------------------------------------------------------------------------

HERE = """
<p>There is no journey to describe. We are at Unit 1 Soho Mills on London Road, which is the road
you are already on &mdash; a couple of minutes from the station, the parade and the level
crossing, and inside the SM6 postcode rather than a drive away from it.</p>
<p>That changes how you can use us, and it is worth saying plainly:</p>
<ul class="kx-list">
<li><strong>You can walk in.</strong> If something is making a noise, bring it down and we will
look at it rather than booking you in for a week on Thursday to hear a description of it.</li>
<li><strong>You can leave the car and walk home.</strong> Most of Hackbridge is ten minutes on
foot from the yard, which removes the whole business of arranging a lift or waiting in a
reception.</li>
<li><strong>You can get to the station from us.</strong> If the car has to stay in, you are a few
minutes from the platform rather than stranded.</li>
<li><strong>We can look at it before quoting.</strong> Where a job needs the car on a ramp to
price honestly, being local means that is a short detour rather than a second trip across
town.</li>
</ul>
<p>Being the workshop in the place rather than the workshop near it is most of why people use us.
It is also why we would rather tell you something is not worth repairing than take the work &mdash;
we are going to see you in the Co-op.</p>
"""

HERE_HEADING = 'We are on London Road, which is the point'


# ---------------------------------------------------------------------------------------------
# FAQs. Two are shared because they are the two questions everybody actually asks a local garage;
# the rest are specific to the group, so no two groups carry the same set.
# ---------------------------------------------------------------------------------------------

FAQ_COMMON = [
 ('Where exactly are you in Hackbridge?',
  'Unit 1 Soho Mills, London Road, SM6 7HN &mdash; a couple of minutes from Hackbridge station '
  'and the parade. There is room to leave a car with us.'),
 ('Can I just turn up?',
  'For a look at something, yes. For work that needs a ramp and a slot, call or put your '
  'registration into the box on this page first so we can give you a time rather than keep you '
  'waiting.'),
]

FAQ_GROUP = {
 'emissions': [
  ('My car only does the station run. Will the filter just block again?',
   'On that pattern, yes, unless something changes. Cleaning buys you time; a longer run at '
   'sustained speed once a week is what actually keeps it clear. We will tell you that rather '
   'than booking you in again in six months.'),
  ('Is a DPF delete an option?',
   'No. Removing one is an MOT failure and makes the car illegal to use on the road. We will not '
   'do it and we would be suspicious of anyone offering to.'),
  ('How do I know it is the filter and not something else?',
   'We read the soot load and the pressure differential rather than guessing from the light. A '
   'blocked filter and a failing sensor present almost identically and cost very different '
   'amounts to put right.'),
 ],
 'servicing': [
  ('My mileage is tiny. Do I still need a service?',
   'Usually yes, on time rather than on mileage. Short local journeys contaminate oil faster than '
   'long ones and are harder on brakes and batteries, so a low-mileage Hackbridge car often needs '
   'the time interval rather than the distance one.'),
  ('Will servicing here affect my warranty?',
   'No. Servicing to the manufacturer&rsquo;s schedule with the right parts and a proper record '
   'keeps a warranty intact. That is the legal position and has been for years.'),
  ('Can I wait while it is done?',
   'For shorter jobs, yes. For a full service most local customers leave the car and walk home, '
   'which is ten minutes from most of Hackbridge.'),
 ],
 'bodywork': [
  ('Someone hit my car on my street and drove off.',
   'Photograph it before you move it, ask about CCTV the same day, and look for paint transfer. '
   'Be aware the national untraced drivers scheme does not pay for vehicle damage unless somebody '
   'was significantly injured, so a no-injury hit and run usually comes down to your own policy '
   'or paying. Our guide pages go through it.'),
  ('Do I have to use my insurer&rsquo;s repairer?',
   'No. The repairer is your choice on any claim. We are on no insurer panel, so nothing we tell '
   'you is steered by an arrangement with one.'),
  ('Do you do paintless dent removal?',
   'No. Every dent we repair is straightened and then painted and blended. On the dents PDR can '
   'fix a PDR specialist will be cheaper, and we would rather say so than take the work.'),
 ],
 'drivetrain': [
  ('My mileage is low but the car feels tired.',
   'That is the local pattern. Clutches, flywheels and mounts wear by being cycled rather than by '
   'distance, so a car that has done forty thousand miles of short Hackbridge journeys has worked '
   'harder than the number suggests.'),
  ('Will you quote before doing the work?',
   'Always, and if the job needs stripping to price honestly we will tell you what that costs '
   'before we start rather than after.'),
  ('Can you do it while I wait?',
   'Not on this kind of work &mdash; it is a day or more with the car on a ramp. Being local, '
   'most people leave it and walk home.'),
 ],
 'electrical': [
  ('My battery keeps going flat. Is it just old?',
   'Maybe, and maybe not. On cars that only do the station run a battery never fully recharges, '
   'but a parasitic drain or a weak alternator looks identical. We test the charging and the '
   'drain before selling you a battery.'),
  ('The light is on but the car drives fine.',
   'Still worth reading. A stored fault that has not yet become a symptom is the cheap version of '
   'the same problem.'),
  ('Do you clear codes without fixing anything?',
   'No. Clearing a code without finding what set it is selling you a few quiet days, and it comes '
   'back.'),
 ],
 'chassis': [
  ('It knocks over bumps on my road but seems fine otherwise.',
   'That is the commonest local symptom and it is worth looking at. Around here it is usually a '
   'kerb strike or a pothole rather than mileage, and a worn bush or a tired drop link is cheap '
   'next to what it takes out if it is left.'),
  ('The car pulls to one side since I kerbed it.',
   'Almost certainly the geometry. We would check the alignment and the components behind it '
   'rather than just resetting the tracking, because something that moved can be something that '
   'bent.'),
  ('Is it an MOT failure?',
   'Depends what it is. We will tell you plainly whether it fails now, will fail next time, or is '
   'simply annoying &mdash; those are three different conversations and three different bills.'),
 ],
 'tyres': [
  ('I kerbed it reversing into a space. Is the tyre still safe?',
   'If the scuff is deep enough to show the cords in the sidewall, no. A sidewall is not '
   'repairable and the cords are what hold the tyre together. Bring it down and we will look.'),
  ('Do I need the alignment doing as well?',
   'If the kerb was hard enough to mark the wheel, usually yes. Tracking knocked out by a kerb '
   'wears the new tyre unevenly and you end up buying another one early.'),
  ('Can you do all four while I wait?',
   'Usually, if we know you are coming. Put your registration in above so we have the right sizes '
   'on the shelf rather than ordering them while you sit there.'),
 ],
 'marque': [
  ('Will using you void my warranty?',
   'No. Servicing to the manufacturer&rsquo;s schedule with matching-quality parts and a proper '
   'record keeps a warranty intact.'),
  ('Are you an approved repairer for the marque?',
   'No, and we will not pretend otherwise. We are on no manufacturer scheme and no insurer panel. '
   'What we offer is the right parts and oil specification for the car, proper diagnosis and a '
   'recorded history.'),
  ('Do you have the right diagnostic equipment?',
   'Tell us the model and what it is doing and we will say honestly whether it is a job for us or '
   'one for a dealer. There are cars and faults where the answer is the dealer and we will say '
   'so.'),
 ],
 'recovery': [
  ('How quickly can you get to me?',
   'If you are local, quickly &mdash; the truck starts from London Road in Hackbridge rather than '
   'from a dispatcher somewhere else. Call and we will give you a real time rather than a '
   'window.'),
  ('Can the car come straight to your workshop?',
   'Yes, and it usually should. It saves moving it twice and it is already where it needs to be '
   'if the fault is something we can put right.'),
  ('It will not start. Do I need recovery or a jump?',
   'Often a jump, around here. A lot of local cars only ever do the station run and the battery '
   'never recovers. Worth a phone call before you pay for a tow.'),
 ],
}


def faqs(slug):
    g = GROUP.get(slug, 'servicing')
    return FAQ_GROUP[g] + FAQ_COMMON


# Replaces the extra "What we actually see from <Town>" block that the bodywork services carry.
SEEN = """
<p>The damage that comes to us from a hundred yards away is overwhelmingly low-speed. Parked-car
damage, in a suburb where 67 per cent of residents told the council their street has a parking
problem and 39 per cent park on it.</p>
<ul class="kx-list">
<li><strong>Bumper corners and scuffed ends.</strong> Reversing into a gap on an Edwardian street
that was laid out before anyone owned a car.</li>
<li><strong>Door edge dings and creased doors.</strong> Cars parked close enough on both sides
that there is no safe arc to open into.</li>
<li><strong>Mirror casings.</strong> Taken off by a passing van on a road narrowed to one lane by
parking.</li>
<li><strong>Kerbed alloys.</strong> The commonest thing on the list, and the one most people put
off longest.</li>
<li><strong>Scrapes down one side.</strong> Usually a squeeze past something double-parked or a
delivery lorry at the parade.</li>
</ul>
<p>What we see far less of is the high-speed structural damage that comes off the A217 and the
A232. Hackbridge sits off the main network rather than on it, which is good news for the severity
of what happens here and no help at all to the state of the paint.</p>
"""


# Hero lead. Varied by group so the 49 pages do not open with one sentence and a swapped noun.
LEAD = {
 'emissions': ('{svc} at our own workshop on London Road. We are in Hackbridge rather than a '
               'drive from it, and on a suburb full of one-mile station runs we will tell you '
               'what is actually causing it before we quote to clear it.'),
 'servicing': ('{svc} at our own workshop on London Road, a few minutes from the station. Most '
               'cars around here do short local journeys, which changes what needs doing &mdash; '
               'so we service to how the car is used rather than to a generic list.'),
 'bodywork':  ('{svc} at our own bodyshop on London Road in Hackbridge. We are on no insurer '
               'panel, so the repairer is your choice and nothing we tell you is steered by an '
               'arrangement with one.'),
 'drivetrain': ('{svc} at our own workshop on London Road. Written quote before anything is '
                'started, and if the job needs stripping to price honestly we tell you what that '
                'costs first rather than afterwards.'),
 'electrical': ('{svc} at our own workshop on London Road. We test before we sell you anything '
                '&mdash; on cars that only ever do the station run, a flat battery is as often '
                'the symptom as the cause.'),
 'chassis':   ('{svc} at our own workshop on London Road. Around here it is usually a kerb or a '
               'pothole rather than mileage, so we look at what moved rather than only at what '
               'is worn.'),
 'tyres':     ('{svc} at our own workshop on London Road. Put your registration in and we will '
               'have the right sizes on the shelf before you arrive rather than ordering them '
               'while you wait.'),
 'marque':    ('{svc} at our own workshop on London Road in Hackbridge. Servicing here keeps a '
               'manufacturer warranty intact, and we are on no manufacturer scheme &mdash; we '
               'will say so rather than imply otherwise.'),
 'recovery':  ('{svc} from our yard on London Road in Hackbridge. The truck that comes to you is '
               'ours and it starts from here, not from a dispatcher taking a cut somewhere else.'),
}


def lead(slug, svc_name, price=''):
    g = GROUP.get(slug, 'servicing')
    t = LEAD[g].format(svc=svc_name, svc_low=svc_name.lower())
    return t + (f' {price}.' if price else '')


# An extra section the other towns' pages do not have. It exists partly because the Hackbridge
# pages have to be substantially more than a reworded Carshalton page to be worth publishing, and
# partly because it is the most useful thing we can tell a local reader: here is what we actually
# find on cars that live here, as opposed to what a generic page about the service would say.
COMMON = {
 'emissions': ('What we find on local diesels', """
<ul class="kx-list">
<li><strong>Regenerations that never complete.</strong> The car starts one, you arrive at the
station four minutes later and switch off. Soot load climbs a little every time until a light
comes on.</li>
<li><strong>Oil above the full mark.</strong> Diesel washing past the rings during failed
regenerations and collecting in the sump. It is a warning sign, not an overfill, and on some
engines it is how they destroy themselves.</li>
<li><strong>Rotten rear boxes on low-mileage cars.</strong> Condensation never dries out of an
exhaust that only runs for four minutes, so it corrodes from the inside while the car looks
almost new.</li>
<li><strong>EGR valves sooted solid.</strong> Same cause. Low load, low temperature, no sustained
run to clear anything.</li>
<li><strong>AdBlue crystallising.</strong> Short runs and long stands are exactly the conditions
for it.</li>
</ul>
<p>If a car has to live on one-mile journeys, the honest advice is sometimes that a diesel is the
wrong car for it. We would rather say that once than clean the same filter every eighteen
months.</p>"""),

 'servicing': ('What we find on low-mileage local cars', """
<ul class="kx-list">
<li><strong>Oil that is past it on time rather than mileage.</strong> Short journeys leave fuel
and moisture in it, and no amount of low mileage fixes that.</li>
<li><strong>Brake discs corroded at the edges.</strong> A car that sits for days between four-
minute runs surface-rusts and never wears it back off.</li>
<li><strong>Seized rear calipers and handbrake mechanisms.</strong> The classic low-mileage
failure and a common MOT advisory around here.</li>
<li><strong>Tyres aged out rather than worn out.</strong> Plenty of tread, sidewalls cracking.
Age matters as much as depth.</li>
<li><strong>Coolant and brake fluid never changed.</strong> Both degrade on time, not on
distance, and both get forgotten on a car that barely moves.</li>
</ul>
<p>Which is why the inspection matters more than the oil change on a car like this. What fails
locally is what rots and seizes, and the only way to find those is to look.</p>"""),

 'bodywork': ('Before you decide whether to claim', """
<ul class="kx-list">
<li><strong>Price it first.</strong> A single scuffed panel is often close to a typical excess,
and claiming costs you the no-claims discount on top.</li>
<li><strong>Check who you are claiming against.</strong> If nobody is identified, your insurer
has nobody to recover from, so it goes down as a fault claim even though it was not your
fault.</li>
<li><strong>Notify either way.</strong> Most policies require it. Notifying is not claiming, and
saying so on the call is worth doing.</li>
<li><strong>Do not accept a roadside cash offer before you have a figure.</strong> They are
reliably below what the job costs, and once accepted the way back is hard.</li>
</ul>
<p>We will give you the repair number so you can do that sum properly. The other half of it comes
from your insurer, and asking them directly is the only way to get it right.</p>"""),

 'drivetrain': ('What we check before quoting', """
<ul class="kx-list">
<li><strong>Whether the symptom is actually the component.</strong> A judder on take-up can be a
clutch, a flywheel or an engine mount, and they are very different bills.</li>
<li><strong>What the car is used for.</strong> A local car on short journeys wears by cycle count
rather than mileage, so the odometer understates how hard it has worked.</li>
<li><strong>What else is coming.</strong> If the gearbox is out anyway, the things that are cheap
now and expensive later get listed so you can decide, not so we can add to the bill.</li>
<li><strong>Whether it is worth it at all.</strong> On an older low-value car we will say plainly
if the repair costs more than the car is worth.</li>
</ul>
<p>Written quote before anything is started, and if the job needs stripping before it can be
priced honestly, we tell you what the strip costs first.</p>"""),

 'electrical': ('The tests we run before selling you a part', """
<ul class="kx-list">
<li><strong>Battery state of health, not just voltage.</strong> A battery can read 12.5 volts and
still be unable to turn the engine on a cold morning.</li>
<li><strong>Charging output under load.</strong> An alternator that charges at idle and not under
load looks exactly like a tired battery.</li>
<li><strong>Parasitic drain.</strong> Measured properly, with time for the modules to go to
sleep. This is where aftermarket alarms and trackers usually show up.</li>
<li><strong>Earths and connections.</strong> Corroded earth straps cause faults all over a car
and cost almost nothing to put right.</li>
</ul>
<p>On the local driving pattern the battery is as often the victim as the culprit, so replacing
it first and testing afterwards is how people end up buying two.</p>"""),

 'chassis': ('What a kerb actually does', """
<ul class="kx-list">
<li><strong>Bends a track rod or moves the tracking.</strong> The car pulls, and the new tyre
wears across its width.</li>
<li><strong>Shocks a wheel bearing.</strong> It may not hum for months, and then it does.</li>
<li><strong>Splits a suspension bush.</strong> The knock over bumps that everybody describes as
coming from the road rather than the car.</li>
<li><strong>Buckles the rim slightly.</strong> A vibration that people blame on tyre balance and
chase for a year.</li>
<li><strong>Marks the sidewall.</strong> If the cords show, the tyre is finished regardless of
tread depth.</li>
</ul>
<p>So on anything that has been kerbed properly we would rather look at the whole corner than
reset the tracking and hand it back.</p>"""),

 'tyres': ('Before you come down', """
<ul class="kx-list">
<li><strong>Put your registration in above.</strong> It gives us your sizes so the tyres are
here rather than on order while you sit in reception.</li>
<li><strong>Check all four, not just the bad one.</strong> Tyres age as well as wear, and a set
bought together tends to need replacing together.</li>
<li><strong>Mention any kerb strike.</strong> It changes whether this is a tyre job or an
alignment job, and the alignment is what stops you buying another tyre early.</li>
<li><strong>Look at the inner edges.</strong> Wear you cannot see from outside the car is the
wear that tells you the geometry is out.</li>
</ul>
<p>We will tell you if a tyre has life left in it. Selling four when you needed two is the
quickest way to never see somebody again in a suburb this size.</p>"""),

 'marque': ('What we will and will not take on', """
<ul class="kx-list">
<li><strong>Routine servicing and repair to the manufacturer&rsquo;s schedule.</strong> With the
correct oil and part specification for the car, recorded properly so the history stands up.</li>
<li><strong>Diagnosis before parts.</strong> Reading the fault, testing what it points at, and
telling you what it is rather than replacing components in sequence.</li>
<li><strong>Honest limits.</strong> There are models and faults where the dealer has tooling or
software access we do not. Where that is the case we say so instead of having a go at your
expense.</li>
</ul>
<p>We are on no manufacturer scheme and no insurer panel. Using us does not affect a warranty,
and we will never tell you we are approved by somebody we are not.</p>"""),

 'recovery': ('What to do while you wait', """
<ul class="kx-list">
<li><strong>Get everyone somewhere safe.</strong> Out of the car and off the carriageway if you
are on a fast road, behind a barrier if there is one.</li>
<li><strong>Hazards on, and a warning triangle if it is safe to place one.</strong> Not on a
motorway.</li>
<li><strong>Tell us what the car is doing.</strong> Whether it rolls, steers and has a working
handbrake decides which truck comes, and getting that right first time saves an hour.</li>
<li><strong>Say if it is electric or hybrid.</strong> A damaged high-voltage car has its own
handling requirements and we would rather know before we arrive.</li>
<li><strong>Check it is not just the battery.</strong> Around here it often is.</li>
</ul>
<p>We will give you a real time rather than a window, and the car can come straight back to our
own workshop rather than sitting in a compound.</p>"""),
}


def common_section(slug):
    g = GROUP.get(slug, 'servicing')
    heading, body = COMMON[g]
    return heading, body.strip()


# A per-service Hackbridge paragraph for the pages where the shared service content is long
# enough to dominate - the services with the biggest "what's included" lists. Without these the
# gate fails them at 62-64%, which is the correct result: on those pages the local content was
# genuinely too thin a share of the page to justify a separate URL.
EXTRA = {
 'full-service': """
<p>One local note on a full service. A great many Hackbridge cars will not reach the mileage
interval in a year &mdash; the station is a few minutes away, the parade is walkable, and the car
does a mile at a time. Those cars still need the service, on the time interval, and the reason is
not the oil. It is that the brakes corrode, the rear calipers seize, the coolant and brake fluid
degrade on time regardless of distance, and the tyres age out before they wear out.</p>
<p>So on a low-mileage local car we spend proportionally more of the time inspecting and less of
it draining, and we will tell you which of the two intervals yours is actually on rather than
quietly defaulting to whichever is further away.</p>
<p>The other local point is what a full service is worth to you when you sell. Hackbridge is a
small place and a lot of cars here change hands privately or go back at the end of a finance
agreement. A complete, stamped, itemised history is worth real money in both situations, and a
gap in it is worth real money off. We itemise what was done and what was fitted rather than
stamping a book and leaving you to remember.</p>
<p>And if something on the schedule does not need doing yet, we will say so and write down why.
A service record that shows judgement being applied reads better to the next owner than one that
shows everything replaced every year regardless.</p>""",

 'major-service': """
<p>Whether a major is the right service for a Hackbridge car is worth a conversation rather than
an assumption. The items that separate a major from an interim &mdash; fluids, plugs, the bigger
filters &mdash; are mostly time-based rather than distance-based, which means a low-mileage local
car reaches them on the calendar even though the odometer says otherwise.</p>
<p>The flip side is that a car doing one-mile station runs is not accumulating the kind of wear a
major is partly designed to catch. We will go through which items yours actually needs now and
which can honestly wait, rather than selling the whole list because it is the one with the
biggest number next to it.</p>""",

 'interim-service': """
<p>An interim suits a lot of Hackbridge cars better than people expect, and for an unusual
reason: the local driving pattern is hard on oil without putting miles on the car. Short journeys
leave fuel and moisture in the sump that a longer run would boil off, so oil ages by time and use
rather than by distance.</p>
<p>What an interim will not do is find the things that go wrong on cars that sit. Seized rear
calipers, corroded discs, perished tyres and degraded fluids are inspection items, not oil
items. If your car does very few miles we will say which of those need looking at now, and if the
answer is none we will say that too.</p>""",

 'oil-filter-change': """
<p>Oil and filter is the job where the local driving pattern matters most and gets mentioned
least. A car doing one-mile runs to Hackbridge station never gets its oil hot enough to drive off
the fuel and water that collect in it, so the oil degrades on a timescale that has nothing to do
with the mileage on the dipstick.</p>
<p>If your car does four thousand miles a year in short hops, changing the oil annually is not
over-servicing &mdash; it is the correct interval for how it is used. And if the oil comes out
smelling of fuel or sitting above the full mark, that is worth investigating rather than
replacing and forgetting, particularly on a diesel doing short journeys.</p>
<p>Two things we check while the oil is out, because they cost nothing and tell you a lot. The
first is what comes out on the magnetic sump plug: a light grey paste is normal, metallic
glitter is not. The second is the old filter itself, cut open if there is any doubt, because
debris in the pleats is the earliest warning of something wearing inside the engine that nobody
would otherwise find for another year.</p>
<p>Neither of those is a sales opportunity. Most of the time the answer is that everything looks
as it should, and we will tell you that rather than inventing something to worry about.</p>""",

 'head-gasket-replacement': """
<p>A head gasket is the job where we are most likely to tell a local customer not to do it. On an
older, low-value car doing one-mile station runs, the repair can cost more than the car is worth,
and the honest answer is to say so before anything comes apart rather than after.</p>
<p>When it is worth doing, the thing that decides whether the repair lasts is what caused the
failure in the first place. A gasket that went because of a slow coolant loss nobody noticed, or
a cooling fan that stopped working, will go again if only the gasket is replaced. We check the
head for flatness and the cooling system as a whole, and we will tell you what we found rather
than handing the car back with a new gasket and the original problem.</p>""",

 'turbo-replacement': """
<p>Turbos and short journeys are a bad combination, which makes this a more common job around
here than the mileage on local cars would suggest. A turbo runs at very high speed and relies on
clean oil fed under pressure; short runs leave the oil contaminated and never get it properly
hot, and a car switched off immediately after a run gives the bearing no chance to cool.</p>
<p>So before quoting a replacement we look at why the old one failed. A blocked breather, a
partly blocked oil feed, a collapsed intercooler hose or oil that has not been changed often
enough on a short-journey car will all take out a new turbo as surely as they took out the old
one. Fitting a turbo without finding that is an expensive way to buy a second turbo.</p>""",

 'oil-leak-repair': """
<p>Oil leaks are over-represented on low-mileage local cars, and the reason is seals rather than
wear. Rubber hardens with age and with heat cycling, and a car that is started cold, run for four
minutes and parked is heat-cycling constantly without ever reaching a steady temperature. Seals
that would survive a motorway life perish on a station-run life.</p>
<p>The job is finding which one. Oil tracks along the underside of an engine and appears a long
way from where it left, so the drip on your driveway tells you very little about the source. We
clean the area, run it, and look rather than guessing from where it lands &mdash; a rocker cover
gasket and a rear crank seal look identical on the floor and are very different bills.</p>""",

 'audi-garage': """
<p>There are more newer Audis in Hackbridge than there were, which is what over eleven hundred
new homes at Felnex and New Mill Quarter does to a suburb. Most arrive with a finance agreement
and a warranty attached, and the question is always the same: does using an independent affect
it?</p>
<p>It does not, provided the car is serviced to Audi's own schedule, with oil and parts of the
specification the car calls for, and the work is recorded. The specification part matters more on
these cars than on most &mdash; the oil standard is not a suggestion, and using the wrong one on
a long-life schedule is how engines get damaged slowly. We use what the car asks for and put it
on the invoice so you can check.</p>""",
}


def extra_for(slug):
    return EXTRA.get(slug, '').strip()
