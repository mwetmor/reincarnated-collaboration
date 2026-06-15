// descent-hue-balance-iter2fix.mjs — the GOLD-OVER-GREEN measurement.
//
// WHY (Discipline #4 right-tool / #11 empirical-inspection): the similarity instrument's
// warm_pct counts only BRIGHT (V>150) warm POINTS. iter2fix's gold correction is largely a
// warm MID-VALUE floor/wall TINT (the warm sandy annulus + gold-raked walls), NOT just
// blown-out bright points. A bright-point counter is partially blind to a warm mid-value
// FLOOR — the same instrument-blindness class I caught with gray-luma last iteration.
// "Gold-over-green" is a BALANCE claim about the whole frame's hue mass, not a bright-point
// count. So this measures the FULL-FRAME warm-vs-green hue mass (S*V weighted, all values),
// and the dominant-hue-bin profile, to test the gold-over-green correction fairly.
//
// Definitions (S*V-weighted hue mass over ALL pixels, dark/grey down-weighted by low S*V):
//   warm mass  = hue in [0,70) OR [330,360)  (red/orange/amber/gold)  -- the LIGHT bed target
//   green mass = hue in [70,170)             (yellow-green..green..teal-green) -- the SHADOW bed
//   warm:green ratio  -> >1 = gold dominates (target); <1 = green dominates (the iter1 inversion)
// Reference centroid computed identically so the ratio is anchored to the actual target art.
//
// No silent transformation: raw captures preserved; reads them, writes nothing to them.

import sharp from 'sharp';
import { readdirSync, writeFileSync } from 'fs';
import { join } from 'path';

const TARGET_W = 960;
const DIR = '/Users/admin/Games/reincarnated-godot/harness_logs';
const REF_DIR = '/Users/admin/Games/reincarnated-godot/Assets/Synty/polygon-dark-fantasy-01/modular_asset_idea_pictures/maps';
const REF_FILES = readdirSync(REF_DIR).filter(f => f.endsWith('.png'));

const PAIRS = [
  { view: 'establish_primary', iter1: 'gal_descent_establish_primary_04.png', iter2fix: 'descent_iter2fix_establish_primary.png' },
  { view: 'zone0',             iter1: 'gal_descent_zone0_threshold_04.png',   iter2fix: 'descent_iter2fix_zone0.png' },
  { view: 'zone2',             iter1: 'gal_descent_zone2_warhall_04.png',      iter2fix: 'descent_iter2fix_zone2.png' },
];

function rgb2hsv(r, g, b) {
  r /= 255; g /= 255; b /= 255;
  const max = Math.max(r, g, b), min = Math.min(r, g, b), d = max - min;
  let h = 0;
  if (d !== 0) {
    if (max === r) h = ((g - b) / d) % 6;
    else if (max === g) h = (b - r) / d + 2;
    else h = (r - g) / d + 4;
    h *= 60; if (h < 0) h += 360;
  }
  const s = max === 0 ? 0 : d / max;
  return [h, s, max];
}

async function hueBalance(path) {
  const { data: rgb, info } = await sharp(path)
    .resize(TARGET_W, null, { fit: 'inside' }).removeAlpha().raw()
    .toBuffer({ resolveWithObject: true });
  const n = info.width * info.height;
  let warmMass = 0, greenMass = 0, totalMass = 0;
  // also a coarse value-banded warm tally: warm hue at MID value (60..150) vs BRIGHT (>150)
  let warmMid = 0, warmBright = 0;
  for (let i = 0; i < rgb.length; i += 3) {
    const r = rgb[i], g = rgb[i + 1], b = rgb[i + 2];
    const [hue, s, v] = rgb2hsv(r, g, b);
    const m = s * v;            // hue mass weight (dark/grey -> ~0)
    totalMass += m;
    const warm = (hue < 70 || hue >= 330);
    const green = (hue >= 70 && hue < 170);
    if (warm) warmMass += m;
    if (green) greenMass += m;
    const V = v * 255;
    if (warm && s > 0.15) {
      if (V > 60 && V <= 150) warmMid++;
      else if (V > 150) warmBright++;
    }
  }
  return {
    warm_mass_pct: +(100 * warmMass / totalMass).toFixed(2),
    green_mass_pct: +(100 * greenMass / totalMass).toFixed(2),
    warm_green_ratio: +(warmMass / Math.max(1e-9, greenMass)).toFixed(3),
    warm_mid_pct: +(100 * warmMid / n).toFixed(3),
    warm_bright_pct: +(100 * warmBright / n).toFixed(3),
  };
}

// reference centroid
const refRows = [];
for (const f of REF_FILES) { process.stderr.write(`ref ${f}...\n`); refRows.push({ f, ...(await hueBalance(join(REF_DIR, f))) }); }
const refMean = k => refRows.reduce((a, r) => a + r[k], 0) / refRows.length;
const ref = {
  warm_mass_pct: +refMean('warm_mass_pct').toFixed(2),
  green_mass_pct: +refMean('green_mass_pct').toFixed(2),
  warm_green_ratio: +refMean('warm_green_ratio').toFixed(3),
  warm_mid_pct: +refMean('warm_mid_pct').toFixed(3),
  warm_bright_pct: +refMean('warm_bright_pct').toFixed(3),
};

const rows = [];
for (const pr of PAIRS) {
  process.stderr.write(`pair ${pr.view}...\n`);
  rows.push({ view: pr.view, iter1: await hueBalance(join(DIR, pr.iter1)), iter2fix: await hueBalance(join(DIR, pr.iter2fix)) });
}

const out = { scored_at: new Date().toISOString(), purpose: 'gold-over-green full-frame hue-mass balance (S*V-weighted); tests the hue-INVERSION correction the bright-point counter is partially blind to', reference_centroid: ref, per_ref: refRows, pairs: rows };
writeFileSync(join(process.cwd(), 'descent-hue-balance-iter2fix.json'), JSON.stringify(out, null, 2));

console.log('=== GOLD-OVER-GREEN — full-frame hue-mass balance (S*V weighted, all values) ===\n');
console.log('REFERENCE centroid: warm_mass%=' + ref.warm_mass_pct + '  green_mass%=' + ref.green_mass_pct + '  warm:green=' + ref.warm_green_ratio + '  (>1 = gold dominates = TARGET)\n');
const cols = ['view / iter', 'warmMass%', 'greenMass%', 'warm:green', 'warmMid%', 'warmBright%'];
const w = [24, 11, 12, 12, 11, 12];
console.log(cols.map((c, i) => c.padEnd(w[i])).join(''));
console.log('-'.repeat(w.reduce((a, b) => a + b, 0)));
for (const r of rows) {
  const a = r.iter1, b = r.iter2fix;
  console.log([r.view + ' iter1', a.warm_mass_pct, a.green_mass_pct, a.warm_green_ratio, a.warm_mid_pct, a.warm_bright_pct].map((c, i) => String(c).padEnd(w[i])).join(''));
  console.log([r.view + ' iter2fix', b.warm_mass_pct, b.green_mass_pct, b.warm_green_ratio, b.warm_mid_pct, b.warm_bright_pct].map((c, i) => String(c).padEnd(w[i])).join(''));
  const d = (x, y) => (y - x >= 0 ? '+' : '') + (y - x).toFixed(2);
  console.log(['  Δ', d(a.warm_mass_pct, b.warm_mass_pct), d(a.green_mass_pct, b.green_mass_pct), d(a.warm_green_ratio, b.warm_green_ratio), d(a.warm_mid_pct, b.warm_mid_pct), d(a.warm_bright_pct, b.warm_bright_pct)].map((c, i) => String(c).padEnd(w[i])).join(''));
  console.log('-'.repeat(w.reduce((a, b) => a + b, 0)));
}
console.log('\nINTERPRETATION: iter1 inverted (warm:green < 1 = green dominates). TARGET warm:green = ' + ref.warm_green_ratio + ' (gold dominates).');
console.log('wrote descent-hue-balance-iter2fix.json');
