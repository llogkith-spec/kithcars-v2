#!/usr/bin/env python3
"""Make the engine-size question one a customer can actually answer, and give the estimate a range.

The reg lookup used to fill the engine capacity in, so the question was a confirmation. DVSA's
API is refusing connections at the TLS layer - their end, nothing to do with this site - so every
servicing customer now meets "How big is the engine?" cold, with six cc bands and no way in.
Nobody knows their car in cc. They know it as "a 1.6", because that is how cars are badged, sold,
insured and talked about. So the pills lead with litres, carry example cars people will recognise,
and keep the cc band as small print for anyone reading it off a V5C.

The examples are the common UK fitments for each band, chosen so that a customer scanning the
list finds either their own car or something obviously like it.

Also adds estimate_spread. Once a customer has given engine size, oil grade and parts grade the
rate card produces one exact figure, which is why the estimate showed a single number while the
copy underneath promised a range. Logan wants a range. This defines one that runs UPWARDS from
the exact price: that figure is what we would charge for the job as quoted, so it is the floor,
and the ceiling covers what genuinely varies once the car is on the ramp. A floor below the price
we would actually charge is an advertised number no customer ever gets.
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CAT = ROOT / 'quote-catalogue.json'

# band id -> (how the customer thinks of it, cars they will recognise)
BANDS = {
    'cc1200': ('Up to 1.2 litre',
               'Corsa 1.0 or 1.2, Fiesta 1.0, Polo 1.0, Aygo, C1, Up!, i10, Picanto, Panda'),
    'cc1500': ('1.3 – 1.5 litre',
               'Focus 1.5, Golf 1.4 TSI, Astra 1.4, Qashqai 1.3, Clio 1.5 dCi, Juke 1.5, Yaris 1.5'),
    'cc2000': ('1.6 – 2.0 litre',
               'Golf 2.0 TDI, Focus 1.6, BMW 320d, A4 2.0 TDI, Astra 1.6 CDTi, Insignia 2.0, '
               'Civic 1.8 — most family cars'),
    'cc2400': ('2.1 – 2.4 litre',
               'Transit 2.2, Sprinter 2.1, Vito, Mazda6 2.2, Accord 2.4, Avensis 2.2'),
    'cc3500': ('2.5 – 3.5 litre',
               'X5 3.0d, Discovery 3.0, Touareg 3.0, A6 3.0 TDI, Hilux 2.8, Amarok 3.0'),
    'ccbig': ('3.5 litre and above',
              'Range Rover 5.0, M3 or M5, AMG, Mustang 5.0, big American V8s'),
}

SPREAD = {
    'pct': 0.1,
    'min': 15,
    'round_to': 5,
    '_note': 'The estimate runs from the exact rate-card price UPWARDS. The low end is the figure '
             'we would charge for the job as quoted; the high end covers an engine that takes more '
             'oil than its band, a non-standard filter, or a seized bolt. Never pad downwards: a '
             'low end below our real price is a number no customer ever actually pays.',
}


def main():
    cat = json.loads(CAT.read_text())
    bands = cat['servicing']['bands']

    ids = [b['id'] for b in bands]
    missing = [k for k in BANDS if k not in ids]
    unknown = [i for i in ids if i not in BANDS]
    if missing or unknown:
        print(f'band ids do not match the rate card. missing={missing} unknown={unknown}')
        return 1

    for b in bands:
        pick, examples = BANDS[b['id']]
        b['pick'] = pick
        b['examples'] = examples
        # label stays as it is: it is the cc wording used when the lookup DOES give us a capacity
        # ("Priced for your 1598cc engine (1501-2000cc)"), and that reads correctly there.

    cat['estimate_spread'] = SPREAD

    CAT.write_text(json.dumps(cat, indent=2, ensure_ascii=False) + '\n')

    print('engine size bands now read:')
    for b in bands:
        print(f'  {b["id"]:<8} {b["pick"]:<20} {b["label"]:<17} {b["litres"]}L')
        print(f'           {b["examples"][:78]}')

    # Every band must be answerable without a V5C, and the cc label must still be there for
    # anyone who has one.
    bad = [b['id'] for b in bands if not b.get('pick') or not b.get('examples') or not b.get('label')]
    if bad:
        print('bands missing a customer-facing label:', bad)
        return 1
    print('\nestimate spread: +%d%% (min £%d, rounded up to £%d)'
          % (SPREAD['pct'] * 100, SPREAD['min'], SPREAD['round_to']))
    print('clean: every band leads with litres and names cars people recognise')
    return 0


if __name__ == '__main__':
    sys.exit(main())
