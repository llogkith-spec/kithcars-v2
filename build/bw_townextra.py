#!/usr/bin/env python3
"""A second substantial local passage per town.

bw_towndata carries the facts; this carries the advice that follows from them. Together they are
the majority of each town page, which is the point: the first rebuild of these pages still
measured 78-85% identical because the shared half outweighed the local half. A page about Purley
has to be mostly about Purley.

Each passage is genuinely specific - what that town's damage profile means for the repair, the
claim, or the decision - rather than general advice with a place name attached.
"""

EXTRA = {
 'croydon':
  "Croydon is also where we most often end up having the write-off conversation, and not because "
  "the damage is worse. It is because the borough&rsquo;s car park is older and cheaper than "
  "Wimbledon&rsquo;s, and a write-off is arithmetic rather than a safety verdict: repair cost "
  "against what the car is worth. The same creased door that gets repaired on a three-year-old "
  "car in SW19 earns a Category N marker on a twelve-year-old one in CR0. If that happens to you, "
  "ask to retain the salvage before you accept anything, and get a real repair figure to set "
  "against the buy-back deduction. We will give you one whether or not you use us.",

 'thornton-heath':
  "The other thing CR7 sends us is damage nobody saw happen. On a street where every space is "
  "taken by eight in the evening and freed again at seven, the car that clipped yours is long "
  "gone. That makes most Thornton Heath dents an uninsured loss rather than a claim, and it "
  "changes the sensible answer: with no third party to recover from, claiming costs you your "
  "excess and some of your no-claims for a repair that is often less than the excess anyway. "
  "Worth doing that sum before you ring anyone.",

 'purley':
  "Purley also brings us a disproportionate share of alloy work alongside the panel damage, and "
  "the two usually happen together. A car pushed into a kerb on a cambered hill takes the wheel "
  "and the sill in the same movement. We price them together because they happen together, and "
  "refurbishing a kerbed alloy is nearly always better value than replacing it &mdash; a "
  "refurbished wheel can be finished to match the other three, and a new one cannot be made to "
  "look older.",

 'coulsdon':
  "Because Coulsdon damage is more often part of a real collision, it is also more often an "
  "insurance job: an engineer, an authorisation, and sometimes a supplementary after strip-down. "
  "That last one catches people out. The car is in pieces, the price has changed, and there is a "
  "pause while someone else approves it. It is normal rather than a sign anything went wrong. No "
  "photograph taken with the panels on has ever shown a bent crash bar behind an intact bumper, "
  "which is exactly why we photograph everything at strip-down before anything moves.",

 'norbury':
  "Norbury&rsquo;s other speciality is the repair that has been left too long. A dent with the "
  "paint split, on a car parked on the A23, collects road salt and standing water in the bottom "
  "of the depression all winter. Caught in the autumn it is a paint job. Left until spring, the "
  "metal underneath has started to corrode and it becomes a cut-and-treat job, which is a "
  "materially bigger bill. If you can see brown in the bottom of a dent, that is the clock "
  "running.",

 'sutton':
  "Sutton is also the town where we are most often asked whether it is worth claiming, and the "
  "answer is usually no. Multi-storey damage is nearly always a single panel, and a single panel "
  "on our rate card frequently lands below a typical total excess once the compulsory and "
  "voluntary halves are added together. Claiming for it costs you most of the bill anyway, loses "
  "some no-claims discount, and gets declared for about five years. Get a real figure first and "
  "then compare &mdash; it is a two-minute sum that saves people a lot.",

 'carshalton':
  "What we see less of from Carshalton is high-speed damage, and that is worth saying because it "
  "changes the repair. A dent put in at walking pace by a car door has not stretched the metal "
  "the way an impact does, so it comes back closer to its original shape and needs less filler. "
  "Those are the repairs that disappear completely. The ones that do not are creases, where the "
  "metal has folded rather than pushed, and on a bolt-on panel like a door skin we will price "
  "replacing against straightening so you can choose.",

 'cheam':
  "Driveway damage also tends to arrive later than street damage, because you see it every day "
  "and it stops registering. By the time a Cheam car comes in, the gatepost scrape down the "
  "nearside has often been there a year and has begun to lift at the edges. That is still "
  "repairable, but the preparation is longer: anything lifting has to come back to sound paint "
  "before anything new goes on, or the new edge lifts in the same place within a season.",

 'wallington':
  "Being on the doorstep means we can do something for Wallington customers we cannot always "
  "offer further out: look at it today and tell you honestly whether it needs us at all. A fair "
  "number of dents turn out to be scuffs with transferred paint sitting on top, and those come "
  "off with compound in ten minutes. We would rather tell you that than book in a repaint. Bring "
  "it down and we will look at it in daylight with you.",

 'beddington':
  "Van work also runs to a different timetable, and we try to work with it. A van off the road is "
  "a day&rsquo;s earnings rather than an inconvenience, so where the damage allows we will prep "
  "and paint a panel while the vehicle is still working and fit it in one visit, rather than "
  "keeping the van for three days. It is not always possible &mdash; a panel that has to come off "
  "to be worked flat has to come off &mdash; but it is worth asking about when you book.",

 'rosehill':
  "A crease down a flank is also the damage most often underquoted elsewhere, because from the "
  "front of the car it looks like one panel. Sight along it from the back and you usually find it "
  "runs through a shut line into the next one, and a crease crossing a shut is two repairs "
  "blended to meet rather than one. We tell you that at the estimate rather than after the car is "
  "stripped, because it is the commonest single reason a quote changes. Rosehill is also the only place on our patch where the damage is dominated by a single junction rather than by a kind of street. That makes it unusually predictable: if you tell us it happened at the roundabout, we already know to sight along the flank for a shut line before quoting, because side-swipes there run into the next panel more often than not.",

 'worcester-park':
  "Garage door and gatepost damage has one useful characteristic: it is almost always on a "
  "bolt-on panel &mdash; a front wing, a bumper, a door. Those unbolt, which means they can come "
  "off the car and be worked flat on a stand, and it means replacement is a genuine alternative "
  "we can price against repair. The panels where that is not true, the rear quarters and the "
  "sills and the roof, are welded into the shell, and they are the ones that cost real money.",

 'mitcham':
  "Nearside front corner damage has a specific tell worth knowing. The bumper often looks "
  "straight while the gap between it and the wing has opened up by a few millimetres. That means "
  "the mounting tabs behind it have broken, and the tabs are what hold a bumper in line. A repair "
  "that fixes the paint and not the tabs looks perfect at handover and sits wrong within a month. "
  "We check them on every bumper that comes off and rebuild them as part of the job rather than "
  "as an extra.",

 'morden':
  "Because so much Morden damage is nobody-saw-it, it is also the town where we most often "
  "suggest checking the policy before doing anything. Plenty of comprehensive policies carry a "
  "separate and lower excess for some kinds of damage, and some protect no-claims where there is "
  "a police reference. Neither is worth much on a single door ding, but both are worth two "
  "minutes of reading before you decide whether this is a claim or a job you pay for yourself. Morden also sits on the boundary between two boroughs for parking enforcement, and the SM4 figure above counts only the Merton side. Cars registered a street away in Sutton appear in a different column entirely, which is worth knowing if you are comparing numbers for where you actually live rather than where you park.",

 'wimbledon':
  "Aluminium is the one that catches people out on newer Wimbledon cars. A growing number use "
  "aluminium bonnets and wings to save weight, and an aluminium panel is a different repair "
  "&mdash; different filler, different preparation, and it has to be isolated from steel tooling "
  "and steel dust, because steel particles left in aluminium start a corrosion reaction that "
  "shows up as blistering months after the car left the workshop. There is no surcharge on our "
  "rate card for it. There is a difference in how it is handled.",

 'streatham':
  "Mirror damage is also the repair most often done badly, because a wing mirror is three things "
  "in one housing: the painted cap, the glass, and the motor and heater behind them. Often only "
  "the cap is damaged, and a cap alone is a cheap part that takes paint well. It is worth asking "
  "specifically rather than accepting a quote for a complete mirror assembly &mdash; we will tell "
  "you which of the three actually needs replacing, and if the glass is intact and the motor "
  "still works we will say so.",

 'tooting':
  "Damage left for months is its own repair problem rather than a bigger version of the same one. "
  "Paint open to the weather since the summer has usually lifted at the edges, and anything "
  "lifting has to come back to sound paint before new material goes on. A dent repaired in week "
  "one is a straighten, fill, prime and blend. The same dent in month eight often needs the "
  "surrounding area cut back first, which is more preparation, more paint, and a bigger blend "
  "into the panels either side.",
}


# One question per town, in the words people from that town actually ask it.
FAQ = {
 'croydon': ('My car has been written off and I think it is repairable.',
   'That is a common one in CR0, because a write-off is cost against value rather than a safety verdict. Ask to retain the salvage before you accept the settlement, and bring us the car or the photographs. A real repair figure set against the buy-back deduction is the only way to know whether keeping it makes sense.'),
 'thornton-heath': ('Nobody saw who hit my car. Is it still worth doing anything?',
   'Yes, and it is the commonest situation we see from CR7. With no third party there is nobody to recover from, so claiming costs you your excess and some no-claims for a repair that is often less than the excess. Get a price first, then decide.'),
 'purley': ('The kerb got the wheel as well as the sill. Do I need two places?',
   "No. We do both, and they are nearly always the same incident on Purley's cambered hills. Refurbishing the alloy beats replacing it, because a refurbished wheel can be finished to match the other three."),
 'coulsdon': ('Why did the price change after you took the bumper off?',
   'Because no photograph taken with the panels on shows what is behind them. Coulsdon damage is more often a real collision, and a bent crash bar behind an intact bumper is the classic find. We photograph everything at strip-down before anything moves, so the supplementary is evidenced rather than asserted.'),
 'norbury': ('There is brown in the bottom of the dent. Does that change things?',
   'Yes, and it is worth acting on. Brown means the metal has started to corrode under the paint, which it does quickly on a car parked on the A23 through a winter. Caught early it is a paint job; left, it becomes a cut-and-treat job and a bigger bill.'),
 'sutton': ('It happened in the multi-storey. Does that make it a claim?',
   'Rarely worth it. Car park damage is almost always a single panel, and a single panel often lands below a typical total excess once the compulsory and voluntary halves are added together. Two-minute sum, and it usually says pay directly.'),
 'carshalton': ('A car door did it. Will the repair be invisible?',
   'Usually yes. A dent put in at walking pace has not stretched the metal the way an impact does, so it comes back close to its original shape and needs little filler. Those are the repairs that disappear completely.'),
 'cheam': ('The scrape has been on the car for a year. Is it too late?',
   'Not too late, but it is more work than it was. Paint that has been open that long usually lifts at the edges, and anything lifting has to come back to sound paint first or the new edge lifts in the same place within a season.'),
 'wallington': ('Can you look at it today?',
   'Usually, yes - you are five minutes away and we are in SM6 ourselves. Bring it down and we will look at it in daylight with you. A fair number turn out to be transferred paint sitting on top of yours, which comes off with compound in ten minutes.'),
 'beddington': ('The van cannot be off the road for three days.',
   "Say so when you book. Where the damage allows we prep and paint the panel while the vehicle is still working and fit it in one visit. It is not always possible, but it often is, and it is the difference between one day's lost earnings and three."),
 'rosehill': ('The scrape looks like one panel. Why are you quoting two?',
   'Sight along it from the back of the car. Roundabout side-swipes nearly always run through a shut line into the next panel, and a crease crossing a shut is two repairs blended to meet. We tell you at the estimate rather than after the car is stripped.'),
 'worcester-park': ('I reversed into my own garage door frame. Cheaper than a road accident?',
   'Often, yes, because driveway damage is almost always on a bolt-on panel - a wing, a bumper, a door. Those come off the car and are worked flat on a stand, and replacement is a genuine alternative we can price against repair.'),
 'mitcham': ('The bumper looks straight but the gap has opened up.',
   'Then the mounting tabs behind it have broken, which is the classic nearside-corner find. Tabs hold a bumper in line, and a repair that fixes the paint and not the tabs looks perfect at handover and sits wrong within a month.'),
 'morden': ('It happened in the station car park while I was at work.',
   'The Morden standard. Before you decide anything, read the excess section of your policy - some carry a lower excess for certain damage, and some protect no-claims where there is a police reference. Two minutes of reading changes the answer more often than people expect.'),
 'wimbledon': ('The bonnet is aluminium. Does that cost more?',
   'Not on our rate card. It is handled differently - different filler, different preparation, and isolated from steel tooling, because steel particles left in aluminium start a corrosion reaction that blisters months later. The difference is in the method, not the price.'),
 'streatham': ('A bus took my mirror off on the A23.',
   'The most Streatham repair there is. Ask specifically what needs replacing: a mirror is the painted cap, the glass, and the motor behind them, and often only the cap is damaged. A cap alone is a cheap part that takes paint well.'),
 'tooting': ('I have left it months because I cannot be without the car.',
   'Understood, and it is the commonest reason Tooting damage arrives late. It does mean more preparation - paint open to the weather lifts at the edges and has to be cut back to sound material - so it is worth getting a price now even if the booking is later.'),
}


# The panels each town actually damages, so the price table says something about the place.
PANELS = {'croydon': [('rear-bumper', 'Rear bumper'), ('rear-quarter', 'Rear quarter'), ('boot', 'Boot lid')], 'thornton-heath': [('door', 'Door'), ('trim', 'Wing mirror'), ('front-wing', 'Front wing')], 'purley': [('door', 'Door'), ('trim', 'Sill cover'), ('front-bumper', 'Front bumper')], 'coulsdon': [('front-bumper', 'Front bumper'), ('front-wing', 'Front wing'), ('bonnet', 'Bonnet')], 'norbury': [('trim', 'Wing mirror'), ('front-wing', 'Front wing'), ('door', 'Door')], 'sutton': [('front-bumper', 'Front bumper'), ('rear-bumper', 'Rear bumper'), ('trim', 'Sill cover')], 'carshalton': [('door', 'Door'), ('trim', 'Wing mirror'), ('rear-quarter', 'Rear quarter')], 'cheam': [('front-wing', 'Front wing'), ('rear-bumper', 'Rear bumper'), ('door', 'Door')], 'wallington': [('door', 'Door'), ('front-bumper', 'Front bumper'), ('trim', 'Wing mirror')], 'beddington': [('door', 'Van side panel'), ('rear-quarter', 'Rear corner'), ('trim', 'Sill')], 'rosehill': [('door', 'Door'), ('rear-quarter', 'Rear quarter'), ('front-wing', 'Front wing')], 'worcester-park': [('front-wing', 'Front wing'), ('front-bumper', 'Front bumper'), ('door', 'Door')], 'mitcham': [('front-bumper', 'Front bumper'), ('front-wing', 'Front wing'), ('trim', 'Wing mirror')], 'morden': [('door', 'Door'), ('trim', 'Wing mirror'), ('rear-bumper', 'Rear bumper')], 'wimbledon': [('bonnet', 'Bonnet'), ('front-wing', 'Front wing'), ('door', 'Door')], 'streatham': [('trim', 'Wing mirror'), ('front-wing', 'Front wing'), ('door', 'Door')], 'tooting': [('front-bumper', 'Bumper corner'), ('rear-quarter', 'Rear quarter'), ('door', 'Door')]}
