/* Export every bodywork price the pages quote, computed by the live quote engine.
   The pages must never carry a second implementation of the pricing: the site already had a
   bumper page reading "From £300" while the widget on the same page said £288, and that is
   exactly how it happens. Run this whenever quote-catalogue.json changes. */
const E = require('../quote-engine.js');
const cat = require('../quote-catalogue.json');
const out = {};
for (const panel of Object.keys(cat.body_panels_ex_vat))
  for (const band of ['small', 'medium', 'large', 'van', 'prestige'])
    for (const d of cat.bodywork_damage) {
      const line = E.bodyLine(cat, panel, panel, d.id, band);
      if (!line) continue;
      const t = E.bodyBand(cat, { low: line.low, high: line.high }, [line]);
      out[`${panel}|${d.id}|${band}`] = { low: t.low, high: t.high, part: !!line.part };
    }
out._alloy_per_wheel_inc_vat = {
  low: Math.round(cat.alloy_refurb_ex_vat.low * (1 + cat.vat_rate)),
  high: Math.round(cat.alloy_refurb_ex_vat.high * (1 + cat.vat_rate)),
};
require('fs').writeFileSync(__dirname + '/bodyprices.json', JSON.stringify(out, null, 1));
console.log('wrote', Object.keys(out).length - 1, 'price points to build/bodyprices.json');
