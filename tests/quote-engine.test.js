// node tests/quote-engine.test.js
const assert = require('assert');
const E = require('../quote-engine.js');
const cat = require('../quote-catalogue.json');
let n = 0; const t = (name, fn) => { fn(); n++; };

t('LOW tier x2 under 2 hrs', () => assert.strictEqual(E.labourCost(cat, 1.0, 'LOW'), 120));
t('TOP tier x1.5 at exactly 2.0 hrs', () => assert.strictEqual(E.labourCost(cat, 2.0, 'TOP'), 252));
t('TOP x2 at 1.99', () => assert.ok(Math.abs(E.labourCost(cat, 1.99, 'TOP') - 334.32) < 1e-9));
t('always-x2 stays x2 over threshold', () => assert.strictEqual(E.labourCost(cat, 2.5, 'TOP', true), 420));
t('panel door small: 300 ex -> 360 inc, blend both sides +100 each ex', () => {
  const r = E.priceJob(cat, 'panel-door', 'small'); assert.strictEqual(r.low, 360); assert.strictEqual(r.high, 600); });
t('panel SUV surcharge +40 ex', () => assert.strictEqual(E.priceJob(cat, 'panel-front-bumper', 'large').low, Math.round(360 * 1.2)));
t('van surcharge +100 ex', () => assert.strictEqual(E.priceJob(cat, 'panel-rear-bumper', 'van').low, Math.round(375 * 1.2)));
t('tyres £20 each', () => assert.strictEqual(E.priceJob(cat, 'tyres', 'small', { qty: 4 }).low, 80));
t('mot fixed', () => assert.strictEqual(E.priceJob(cat, 'mot', 'medium').low, 54.85));
t('labour job rounds outward to £5', () => {
  const r = E.priceJob(cat, 'brake-pads-front', 'small'); // 0.5x2x60=60+30=90 ; 0.7x2x60=84+55=139 -> 140
  assert.strictEqual(r.low, 90); assert.strictEqual(r.high, 140); });
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
  const r = E.priceJob(cat, 'clutch', 'medium'); assert.ok(r.dealer > (r.low + r.high) / 2); });
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
  const b = E.bodyLine(cat, 'door', 'Left front door', 'dentp', 'medium');
  assert.ok(b.low === Math.floor((300 + 50) * 1.2 / 5) * 5, 'door paint + dent low');
  assert.strictEqual(E.bodyLine(cat, 'door', 'x', 'nonsense', 'medium'), null);
  const t = E.tuneLines(cat, 'td', 150, 's1', ['springs', 'bodykit']);
  assert.strictEqual(t.lines.length, 3);
  assert.ok(t.power.low === 180 && t.power.high === 195, 'diesel stage 1 gains');
  assert.ok(t.lines.some(l => l.kind === 'enquiry'), 'body kit quoted after');
  assert.strictEqual(E.couponEligible(cat, { high: 200 }, false), true);
  assert.strictEqual(E.couponEligible(cat, { high: 60 }, false), false);
  console.log('flow pricing tests passed');
})();
