#!/usr/bin/env python3
"""Compare every bodywork price claim on the site against the price book.

Two stale price lists have already been found by accident -- one on the homepage card, one in a
more prominent block further down the same page. This looks for all of them at once rather than
waiting for the next one to surface in front of a customer.
"""
import glob, json, re, subprocess, sys, collections

c = json.load(open('quote-catalogue.json'))
panels = c['body_panels_ex_vat']
uplift = c['body_dent_uplift_ex_vat']

def inc(ex): return round(ex * 1.2)

def engine(expr):
    """Ask quote-engine.js rather than redoing its arithmetic here.

    Doing the sum independently looked like a stronger check and was actually a weaker one: the
    engine rounds a low down to the nearest £5, this file rounded to nearest, and the audit then
    reported a correct page as wrong (£260 against its own £264). The figure that matters is the
    one the customer is shown, so that is the one to compare against."""
    out = subprocess.run(
        ['node', '-e',
         "const E=require('./quote-engine.js'),C=require('./quote-catalogue.json');"
         "console.log(" + expr + ");"],
        capture_output=True, text=True, check=True)
    return int(out.stdout.strip())

# What each phrase should say, as a "from" price: cheapest band, so ex VAT plus VAT.
EXPECT = {
    'front bumper': inc(panels['front-bumper']),
    'rear bumper': inc(panels['rear-bumper']),
    'bumper': inc(panels['rear-bumper']),          # unqualified: cheapest bumper
    'door': inc(panels['door']),
    'front wing': inc(panels['front-wing']),
    'wing': inc(panels['front-wing']),
    'bonnet': inc(panels['bonnet']),
    'rear quarter': inc(panels['rear-quarter']),
    'roof': inc(panels['roof']),
    'boot': inc(panels['boot']),
    # Cheapest dent on a painted panel; trim is a plastic moulding, not what anyone calls a dent.
    'dent': engine("Math.min(...Object.keys(C.body_panels_ex_vat).filter(p=>p!=='trim')"
                   ".map(p=>E.bodyLine(C,p,p,'dent','small').low))"),
}

# "<phrase> ... from £N" or "from £N ... <phrase>", within a short window so unrelated text
# on the same line does not produce false matches.
PAT = re.compile(r'([A-Za-z ]{3,18}?)\s*(?:<[^>]+>)?\s*from\s*£([\d,]+)', re.I)

def main():
    hits = collections.defaultdict(list)
    for f in sorted(glob.glob('*.html')):
        s = open(f).read()
        text = re.sub(r'<script.*?</script>', ' ', s, flags=re.S)
        for m in PAT.finditer(text):
            phrase = ' '.join(m.group(1).split()).lower().strip(' .,:;—-')
            # keep only the last words, which is where the panel name sits
            key = next((k for k in sorted(EXPECT, key=len, reverse=True) if phrase.endswith(k)), None)
            if not key:
                continue
            got = int(m.group(2).replace(',', ''))
            want = EXPECT[key]
            if got != want:
                hits[f].append((key, got, want))

    if not hits:
        print('every bodywork "from" price matches the price book')
        return 0
    total = sum(len(v) for v in hits.values())
    print(f'{total} price claim(s) out of step with the price book, on {len(hits)} page(s):\n')
    for f, rows in sorted(hits.items())[:25]:
        for key, got, want in rows:
            print(f'  {f:<34} {key:<14} says £{got:<5} book says £{want}')
    return 1


if __name__ == '__main__':
    sys.exit(main())
