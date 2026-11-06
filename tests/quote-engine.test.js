// node tests/quote-engine.test.js
const assert = require('assert');
const E = require('../quote-engine.js');
const cat = require('../quote-catalogue.json');
let n = 0; const t = (name, fn) => { fn(); n++; };

t('LOW tier x2 under 2 hrs', () => assert.strictEqual(E.labourCost(cat, 1.0, 'LOW'), 120));
t('TOP tier x1.5 at exactly 2.0 hrs', () => assert.strictEqual(E.labourCost(cat, 2.0, 'TOP'), 252));
t('TOP x2 at 1.99', () => assert.ok(Math.abs(E.labourCost(cat, 1.99, 'TOP') - 334.32) < 1e-9));
t('always-x2 stays x2 over threshold', () => assert.strictEqual(E.labourCost(cat, 2.5, 'TOP', true), 420));
// Panel prices are the SOP's own figures, hard-coded here on purpose: if the catalogue drifts
// away from the rate card again these fail, which is the whole point of the test.
t('panel door: SOP £200 ex -> £240 inc, blend free so no spread', () => {
  const r = E.priceJob(cat, 'panel-door', 'small');
  assert.strictEqual(r.low, 240); assert.strictEqual(r.high, 240); });
t('every panel matches the SOP inc VAT', () => {
  const sop = { 'front-bumper': 288, 'rear-bumper': 180, bonnet: 180, door: 240, 'front-wing': 180,
                'rear-quarter': 180, roof: 360, boot: 300 };
  for (const [panel, inc] of Object.entries(sop)) {
    const r = E.priceJob(cat, 'panel-' + panel, 'small');
    assert.strictEqual(r.low, inc, `${panel}: expected £${inc} inc VAT, got £${r.low}`);
  } });
t('trim priced off the diagram matches the SOP £120 inc', () => {
  const r = E.bodyLine(cat, 'trim', 'Trim', 'scuff', 'small');
  assert.strictEqual(r.low, 120); });
t('blends are free, per the SOP', () => {
  assert.strictEqual(cat.body_blend_ex_vat.default, 0);
  assert.strictEqual(cat.body_blend_ex_vat.door, 0); });
t('SUV surcharge +40 ex: front bumper 240+40 -> £336 inc', () =>
  assert.strictEqual(E.priceJob(cat, 'panel-front-bumper', 'large').low, Math.round(280 * 1.2)));
t('van surcharge +100 ex: rear bumper 150+100 -> £300 inc', () =>
  assert.strictEqual(E.priceJob(cat, 'panel-rear-bumper', 'van').low, Math.round(250 * 1.2)));
t('tyres £20 each', () => assert.strictEqual(E.priceJob(cat, 'tyres', 'small', { qty: 4 }).low, 80));
t('mot fixed at £50', () => assert.strictEqual(E.priceJob(cat, 'mot', 'medium').low, 50));
t('labour job: rate-card anchor, +35% headroom, rounded outward to £5', () => {
  // small front pads: mid 0.6h x2 x £60 = £72 labour + mid parts £42.50 = £114.50 anchor
  const r = E.priceJob(cat, 'brake-pads-front', 'small');
  const anchor = 0.6 * 2 * 60 + (30 + 55) / 2;
  assert.strictEqual(r.low, Math.floor(anchor / 5) * 5);
  assert.strictEqual(r.high, Math.ceil(anchor * 1.35 / 5) * 5);
  assert.ok(r.high > r.low); });
t('every labour job sits inside its own headroom', () => {
  cat.jobs.filter(j => j.type === 'labour').forEach(j => Object.keys(cat.bands).forEach(b => {
    const r = E.priceJob(cat, j.id, b);
    assert.ok(r.high >= r.low && r.high <= r.low * (1 + cat.mech_headroom) + 12, j.id + ' ' + b); })); });
t('remaps are a fixed price, hardware is quoted', () => {
  const r = E.tuneLines(cat, 'tp', 150, 's1', ['s2hw', 'coilovers']);
  assert.strictEqual(r.lines[0].low, 240); assert.strictEqual(r.lines[0].high, 240);
  assert.strictEqual(E.tuneLines(cat, 'tp', 150, 's2', []).lines[0].low, 360);
  r.lines.slice(1).forEach(l => assert.strictEqual(l.kind, 'enquiry')); });
t('recovery is a fixed price by distance, and priced on the phone past the bands', () => {
  // Read the expected figures off the rate card rather than freezing them here, so changing a
  // price in the catalogue doesn't fail a test that was only ever checking the banding.
  const truck = m => cat.recovery.recovery_bands_inc_vat.find(b => m <= b.max).price;
  const driver = m => cat.recovery.pickup_bands_inc_vat.find(b => m <= b.max).price;
  assert.strictEqual(E.recoveryLine(cat, 'breakdown', 'local').low, truck(2));   // 2 miles, truck
  assert.strictEqual(E.recoveryLine(cat, 'accident', 'croydon').low, truck(5));  // 5 miles, truck
  assert.strictEqual(E.recoveryLine(cat, 'move', 'local').low, driver(2));       // 2 miles, driver
  assert.strictEqual(E.recoveryLine(cat, 'move', 'tooting').low, driver(7));     // 7 miles, driver
  assert.strictEqual(E.recoveryLine(cat, 'breakdown', 'further').kind, 'enquiry');
  assert.strictEqual(E.recoveryLine(cat, 'battery', 'local').kind, 'enquiry'); // roadside, priced when you ring
  assert.strictEqual(E.recoveryLine(cat, 'nonsense', 'local'), null);
  assert.strictEqual(E.recoveryLine(cat, 'breakdown', 'nonsense'), null); });
t('every recovery situation and area pair either prices or asks', () => {
  cat.recovery.situations.forEach(s => cat.recovery.areas.forEach(a => {
    const l = E.recoveryLine(cat, s.id, a.id);
    assert.ok(l && (l.kind === 'enquiry' || (l.low > 0 && l.low === l.high)), s.id + ' ' + a.id); })); });
t('a listed tyre size prices exactly, an unlisted one gives a range', () => {
  const withList = JSON.parse(JSON.stringify(cat));
  withList.tyres.price_list = { '205/55R16': { budget: 58, mid: 79, premium: 112 } };
  const exact = E.tyrePrice(withList, { width: 205, profile: 55, rim: 16 }, 'mid');
  assert.strictEqual(exact.lo, 79); assert.strictEqual(exact.hi, 79);
  const modelled = E.tyrePrice(withList, { width: 225, profile: 45, rim: 17 }, 'mid');
  assert.ok(modelled.hi > modelled.lo); });
t('labour-only tuning has no parts', () => { const r = E.priceJob(cat, 'coilovers', 'medium'); assert.deepStrictEqual(r.parts, [0, 0]); assert.ok(!r.dealer); });
t('diagnose jobs have no price', () => assert.strictEqual(E.priceJob(cat, 'dpf', 'medium').low, undefined));
t('every labour job prices on every band, low<high', () => {
  cat.jobs.filter(j => j.type === 'labour').forEach(j => Object.keys(cat.bands).forEach(b => {
    const r = E.priceJob(cat, j.id, b); assert.ok(r.low > 0 && r.high >= r.low, j.id + ' ' + b); })); });
t('clampAi rejects wild AI numbers (falls back to price book)', () => {
  assert.strictEqual(E.clampAi(cat, 'clutch', { hours: [0.1, 99], parts: [200, 400] }), null);
  assert.strictEqual(E.clampAi(cat, 'timing-chain', { hours: [40, 60], parts: [1, 2] }), null); });
t('clampAi accepts sane numbers, cleans note and confidence', () => {
  const c = E.clampAi(cat, 'clutch', { hours: [6.5, 8], parts: [500, 900], confidence: 'weird', note: '<b>x</b>' });
  assert.deepStrictEqual(c.hours, [6.5, 8]); assert.strictEqual(c.confidence, 'medium'); assert.ok(!/[<>]/.test(c.note)); });
t('clampAi widens a zero-width range', () => { const c = E.clampAi(cat, 'battery', { hours: [0.5, 0.5], parts: [150, 150] }); assert.ok(c.hours[1] > c.hours[0] && c.parts[1] > c.parts[0]); });
t('clampAi swaps reversed ranges and rejects garbage', () => {
  assert.deepStrictEqual(E.clampAi(cat, 'battery', { hours: [0.6, 0.4], parts: [200, 150] }).hours, [0.4, 0.6]);
  assert.strictEqual(E.clampAi(cat, 'battery', { hours: 'x', parts: [1, 2] }), null);
  assert.strictEqual(E.clampAi(cat, 'mot', { hours: [1, 2], parts: [1, 2] }), null); });
t('band guess', () => {
  assert.strictEqual(E.guessBand({ make: 'FORD', engineCapacity: 998 }), 'small');
  assert.strictEqual(E.guessBand({ make: 'BMW', engineCapacity: 1995 }), 'prestige');
  assert.strictEqual(E.guessBand({ make: 'FORD', typeApproval: 'N1' }), 'van');
  assert.strictEqual(E.guessBand({ make: 'KIA', engineCapacity: 2199 }), 'large'); });
t('ULEZ rule of thumb', () => {
  assert.strictEqual(E.ulezLikely({ fuelType: 'DIESEL', yearOfManufacture: 2014 }), false);
  assert.strictEqual(E.ulezLikely({ fuelType: 'DIESEL', euroStatus: 'EURO 6' }), true);
  assert.strictEqual(E.ulezLikely({ fuelType: 'PETROL', yearOfManufacture: 2008 }), true);
  assert.strictEqual(E.ulezLikely({ fuelType: 'ELECTRICITY' }), true); });
t('dealer figure only when clearly dearer', () => {
  // The rule, not a particular job: a dealer figure is only ever shown when it clears our own
  // mid-price by the configured margin. At the real dealer rate (£120 + VAT) that is true of very
  // few jobs, and the comparison correctly stays hidden on the rest rather than claiming a saving.
  const dr = cat.dealer.labour_rate_inc_vat;
  const rateFor = b => (dr && typeof dr === 'object') ? dr[b] : dr;
  let shown = 0;
  for (const j of cat.jobs) {
    if (j.type !== 'labour' || j.labour_only) continue;
    for (const band of Object.keys(cat.bands)) {
      const r = E.priceJob(cat, j.id, band, {});
      if (typeof r.low !== 'number') continue;
      if (r.dealer === undefined) continue;
      shown++;
      const mid = (r.low + r.high) / 2;
      assert.ok(r.dealer >= mid * (1 + cat.dealer.show_if_saving_at_least),
        `${j.id}/${band}: dealer ${r.dealer} does not clear ${mid} by the margin`);
      // Two ways of arriving at the dealer figure, and the catalogue decides which is in use.
      // The test follows the configuration rather than hard-coding one of them, so switching
      // between a flat multiple and the book-hours model does not silently go unchecked.
      let want;
      if (cat.dealer.use_multiplier && Number(cat.dealer.multiplier) > 1) {
        want = mid * Number(cat.dealer.multiplier);
      } else {
        const midH = (r.hours[0] + r.hours[1]) / 2, midP = (r.parts[0] + r.parts[1]) / 2;
        want = midH * rateFor(band) + midP * cat.dealer.parts_factor;
      }
      assert.ok(Math.abs(r.dealer - want) <= 5,
        `${j.id}/${band}: dealer figure ${r.dealer} does not match the configured model (${Math.round(want)})`);
    }
  }
  assert.ok(shown > 0, 'no job anywhere shows a dealer comparison - check the dealer rate'); });
t('totals', () => { const l = [E.priceJob(cat, 'mot', 'small'), E.priceJob(cat, 'dpf', 'small'), E.priceJob(cat, 'tyres', 'small', { qty: 2 })];
  const s = E.totals(l); assert.strictEqual(s.count, 2); assert.strictEqual(s.unpriced, 1); });
console.log(n + ' tests passed');
// print a sample price sheet for review
for (const id of ['service-interim','service-full','brake-discs-front','clutch','cambelt','timing-chain','panel-front-bumper','panel-door'])
  console.log(id.padEnd(20), Object.keys(cat.bands).map(b => { const r = E.priceJob(cat, id, b); return b + ' £' + r.low + '–£' + r.high + (r.dealer ? ' (dealer ~£' + r.dealer + ')' : ''); }).join(' | '));

// booking calendar
(function () {
  const days = E.bookableDays(cat, 'mechanical', 5);
  const today = new Date(); today.setHours(0, 0, 0, 0);
  assert.ok(days.length > 0, 'days returned');
  days.forEach(d => {
    const [y, m, dd] = d.key.split('-').map(Number);
    const dt = new Date(y, m - 1, dd);
    assert.ok(dt > today, 'slot date is in the future: ' + d.key);
    assert.ok(cat.booking.open_days.includes(dt.getDay()), 'only open days: ' + d.key);
    assert.strictEqual(dt.getDate(), d.dom, 'day number matches key');
  });
  assert.ok(E.bookableDays(cat, 'bodywork', 3).every(d => d.slots.every(s => s < '11:00')), 'bodywork drop-offs are mornings');
  console.log('calendar tests passed');
})();
// tyres, bodywork, tuning
(function () {
  const p = E.tyrePrice(cat, { width: 225, profile: 45, rim: 17 }, 'premium');
  assert.ok(p.hi > p.lo && p.fit === 20);
  assert.ok(E.tyrePrice(cat, { width: 225, profile: 45, rim: 17, runflat: true }, 'premium').lo > p.lo, 'run-flats cost more');
  assert.ok(E.tyreLine(cat, { width: 205, profile: 55, rim: 16 }, 'mid', 4).low > E.tyreLine(cat, { width: 205, profile: 55, rim: 16 }, 'budget', 4).low);
  // There is one dent option now: we do not do paintless repair, so a dent is always
  // straightening plus painting the panel. Expected figures come off the price book.
  const b = E.bodyLine(cat, 'door', 'Left front door', 'dent', 'medium');
  const door = cat.body_panels_ex_vat.door, up = cat.body_dent_uplift_ex_vat, vat = 1 + cat.vat_rate;
  // The engine rounds a low down to the nearest £5 and a high up, so a quoted range never
  // reads narrower than the real one.
  const down5 = n => Math.floor(n / 5) * 5, up5 = n => Math.ceil(n / 5) * 5;
  assert.strictEqual(b.low, down5((door + up.low) * vat), 'door paint + lightest dent, inc VAT');
  assert.strictEqual(b.high, up5((door + up.high) * vat), 'door paint + worst dent, inc VAT');
  assert.ok(b.high > b.low, 'a dent is a range, because severity is');
  assert.strictEqual(E.bodyLine(cat, 'door', 'x', 'dentp', 'medium'), null, 'paintless dent repair is gone');
  assert.strictEqual(E.bodyLine(cat, 'door', 'x', 'nonsense', 'medium'), null);
  const t = E.tuneLines(cat, 'td', 150, 's1', ['springs', 'bodykit']);
  assert.strictEqual(t.lines.length, 3);
  assert.ok(t.power.low === 180 && t.power.high === 195, 'diesel stage 1 gains');
  assert.ok(t.lines.some(l => l.kind === 'enquiry'), 'body kit quoted after');
  assert.strictEqual(E.couponEligible(cat, { high: 200 }, false), true);
  assert.strictEqual(E.couponEligible(cat, { high: 60 }, false), false);
  console.log('flow pricing tests passed');
})();

/* ---- Servicing rate card ------------------------------------------------------------------
   These 24 figures come off Logan's own BookMyGarage setup. They are asserted literally and on
   purpose: if a change to the labour rate, the oil price or a filter cost moves any cell, that
   is something he needs to have decided, not something that should slip through. */
{
  const EXPECT = {
    'oil-change': [162.48, 162.48, 164.88, 179.28, 185.28, 214.08],
    'interim':    [181.20, 181.20, 183.60, 198.00, 204.00, 232.80],
    'full':       [210.00, 212.40, 214.80, 229.20, 236.40, 277.20],
    'major':      [248.30, 250.70, 253.10, 291.60, 298.80, 332.40],
  };
  const bands = cat.servicing.bands.map(b => b.id);
  for (const level of Object.keys(EXPECT)) {
    bands.forEach((b, i) => {
      assert.strictEqual(E.svcPrice(cat, level, b, 'standard'), EXPECT[level][i],
        `${level} on ${b} should be £${EXPECT[level][i]}`);
    });
  }

  // Engine capacity from the DVLA lookup picks the band; boundaries land on the lower one.
  assert.strictEqual(E.svcBand(cat, 1200).id, 'cc1200');
  assert.strictEqual(E.svcBand(cat, 1201).id, 'cc1500');
  assert.strictEqual(E.svcBand(cat, 1968).id, 'cc2000');
  assert.strictEqual(E.svcBand(cat, 9999).id, 'ccbig', 'anything huge falls in the top band');
  assert.strictEqual(E.svcBand(cat, 0), null, 'no capacity means no guess');

  // Before the oil is chosen the quote is a range; choosing collapses it to one figure.
  const open = E.svcLine(cat, 'interim', 'cc2000', {});
  assert.strictEqual(open.kind, 'range');
  assert.ok(open.high > open.low, 'specialist oil sits above standard');
  assert.strictEqual(open.low, E.svcPrice(cat, 'interim', 'cc2000', 'standard'));
  assert.strictEqual(open.high, E.svcPrice(cat, 'interim', 'cc2000', 'specialist'));

  const std = E.svcLine(cat, 'interim', 'cc2000', { oil: 'standard' });
  assert.strictEqual(std.kind, 'fixed');
  assert.strictEqual(std.low, std.high);
  assert.ok(std.low >= open.low && std.low <= open.high,
    'whatever they pick must land inside the range they were first shown');

  const spec = E.svcLine(cat, 'interim', 'cc2000', { oil: 'specialist' });
  assert.ok(spec.low >= open.low && spec.low <= open.high, 'same for the specialist grade');

  // The specialist uplift is only ever the oil, priced per litre.
  const band = E.svcBandById(cat, 'ccbig');
  const uplift = (cat.servicing.oil.specialist_ex_vat_per_litre
                - cat.servicing.oil.standard_ex_vat_per_litre) * band.litres * (1 + cat.vat_rate);
  assert.ok(Math.abs((spec.low - std.low) - uplift * (5 / band.litres)) < 0.01 ||
            Math.abs(E.svcPrice(cat, 'interim', 'ccbig', 'specialist')
                   - E.svcPrice(cat, 'interim', 'ccbig', 'standard') - uplift) < 0.01,
    'the gap between grades is the oil and nothing else');

  // An MOT is £21 alongside a full or major service, and not otherwise.
  assert.strictEqual(E.motWithService(cat, ['full']).low, 21);
  assert.strictEqual(E.motWithService(cat, ['major']).low, 21);
  assert.strictEqual(E.motWithService(cat, ['interim']), null, 'interim does not earn it');
  assert.strictEqual(E.motWithService(cat, ['oil-change']), null);
  assert.strictEqual(E.motWithService(cat, []), null);
  assert.ok(E.motWithService(cat, ['full']).was > 21, 'and it is cheaper than a standalone MOT');

  // The old job ids are referenced across the site and the build scripts; they must keep
  // answering, and answer from the new rate card.
  for (const id of ['service-interim', 'service-full', 'service-major', 'oil-filter-change']) {
    const legacy = E.priceJob(cat, id, 'small');
    assert.ok(legacy && legacy.low > 0, `${id} still prices through priceJob`);
  }
  assert.strictEqual(E.priceJob(cat, 'service-full', 'cc2400', { oil: 'standard' }).low,
                     E.svcPrice(cat, 'full', 'cc2400', 'standard'),
                     'priceJob and the rate card cannot disagree');

  console.log('servicing rate card tests passed');
}
