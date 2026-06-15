// descent-colorfair-iter2fix.mjs — register-2 COLOR-FAIR gate read on the iter2fix static frames.
//
// SAME measure() as descent-colorfair-diagnostic.mjs (the iter1 instrument — byte-identical
// per-channel HLF + value-channel LDR + warm/green/redbloom fractions). The ONLY change:
// reads SINGLE static frames (descent_iter2fix_<view>.png) instead of multi-frame windows,
// and pairs each against its matched iter1 single frame for an exact delta.
//
// Gate basis reminder (from the iter1 scorecard, validated): gray-luma is BLIND to saturated
// COLORED light. LIGHTING-drama gate = value-channel LDR (lit-pool vs shadow contrast) + warm
// light presence, NOT absolute gray brightness. VFX gate = prominent hero bloom = value-channel
// or per-channel HLF peak. These 3 static frames are establish + zone0 + zone2 (NOT the
// lifecycle PEAK-VFX hero bloom) -> this run scores the LIGHTING gate on the corrected scene;
// the VFX hero-bloom PEAK is captured separately from the running scene (per the brief).
//
// No silent transformation: raw captures preserved; reads them, writes nothing to them.

import sharp from 'sharp';
import { writeFileSync } from 'fs';
import { join } from 'path';

const TARGET_W = 960;
const DIR = '/Users/admin/Games/reincarnated-godot/harness_logs';

const PAIRS = [
  { view: 'establish_primary', iter1: 'gal_descent_establish_primary_04.png', iter2fix: 'descent_iter2fix_establish_primary.png' },
  { view: 'zone0',             iter1: 'gal_descent_zone0_threshold_04.png',   iter2fix: 'descent_iter2fix_zone0.png' },
  { view: 'zone2',             iter1: 'gal_descent_zone2_warhall_04.png',      iter2fix: 'descent_iter2fix_zone2.png' },
];

function percentile(sorted, p) {
  const idx = Math.min(sorted.length - 1, Math.max(0, Math.floor(p * sorted.length)));
  return sorted[idx];
}
async function measure(path) {
  const { data: rgb, info } = await sharp(path)
    .resize(TARGET_W, null, { fit: 'inside' }).removeAlpha().raw()
    .toBuffer({ resolveWithObject: true });
  const n = info.width * info.height;
  const gray = new Float64Array(n), val = new Float64Array(n);
  let hiGray = 0, hiVal = 0, hiR = 0, hiG = 0, hiB = 0;
  let warmPts = 0, greenPts = 0, redBloom = 0;
  for (let i = 0, p = 0; i < rgb.length; i += 3, p++) {
    const r = rgb[i], g = rgb[i + 1], b = rgb[i + 2];
    const lum = 0.299 * r + 0.587 * g + 0.114 * b;
    const v = Math.max(r, g, b);
    gray[p] = lum; val[p] = v;
    if (lum > 204) hiGray++;
    if (v > 204) hiVal++;
    if (r > 204) hiR++;
    if (g > 204) hiG++;
    if (b > 204) hiB++;
    if (v > 150 && r > g + 25 && r > b + 25) warmPts++;
    if (v > 130 && g > r + 20 && g > b + 20) greenPts++;
    if (v > 160 && r > 150 && r > b + 40 && g < r - 20) redBloom++;
  }
  const gSorted = gray.slice().sort(), vSorted = val.slice().sort();
  const ldrGray = percentile(gSorted, 0.95) - percentile(gSorted, 0.05);
  const ldrVal = percentile(vSorted, 0.95) - percentile(vSorted, 0.05);
  let shfVal = 0; for (let p = 0; p < n; p++) if (val[p] < 31) shfVal++;
  return {
    LDR_gray: +ldrGray.toFixed(1), LDR_val: +ldrVal.toFixed(1),
    SHF_val: +(100 * shfVal / n).toFixed(2),
    HLF_gray: +(100 * hiGray / n).toFixed(3), HLF_val: +(100 * hiVal / n).toFixed(3),
    HLF_R: +(100 * hiR / n).toFixed(3), HLF_G: +(100 * hiG / n).toFixed(3), HLF_B: +(100 * hiB / n).toFixed(3),
    warm_pct: +(100 * warmPts / n).toFixed(3), green_pct: +(100 * greenPts / n).toFixed(3),
    redbloom_pct: +(100 * redBloom / n).toFixed(3),
  };
}

const rows = [];
for (const pr of PAIRS) {
  process.stderr.write(`measure ${pr.view}...\n`);
  rows.push({ view: pr.view, iter1: await measure(join(DIR, pr.iter1)), iter2fix: await measure(join(DIR, pr.iter2fix)) });
}
const out = { scored_at: new Date().toISOString(), purpose: 'register-2 color-fair LIGHTING gate read on iter2fix static frames (establish/zone0/zone2) vs matched iter1 frames; VFX hero-bloom PEAK captured separately', pairs: rows };
writeFileSync(join(process.cwd(), 'descent-colorfair-iter2fix.json'), JSON.stringify(out, null, 2));

console.log('=== COLOR-FAIR register-2 — iter2fix static frames vs iter1 (LIGHTING-gate basis) ===\n');
const cols = ['view / iter', 'LDRgray', 'LDRval', 'SHFval%', 'HLFgray', 'HLFval', 'HLF_R', 'warm%', 'green%', 'redbloom%'];
const w = [22, 9, 8, 9, 9, 9, 8, 8, 9, 10];
console.log(cols.map((c, i) => c.padEnd(w[i])).join(''));
console.log('-'.repeat(w.reduce((a, b) => a + b, 0)));
for (const r of rows) {
  const a = r.iter1, b = r.iter2fix;
  console.log([r.view + ' iter1', a.LDR_gray, a.LDR_val, a.SHF_val, a.HLF_gray, a.HLF_val, a.HLF_R, a.warm_pct, a.green_pct, a.redbloom_pct].map((c, i) => String(c).padEnd(w[i])).join(''));
  console.log([r.view + ' iter2fix', b.LDR_gray, b.LDR_val, b.SHF_val, b.HLF_gray, b.HLF_val, b.HLF_R, b.warm_pct, b.green_pct, b.redbloom_pct].map((c, i) => String(c).padEnd(w[i])).join(''));
  const d = (x, y) => (y - x >= 0 ? '+' : '') + (y - x).toFixed(2);
  console.log(['  Δ', d(a.LDR_gray, b.LDR_gray), d(a.LDR_val, b.LDR_val), d(a.SHF_val, b.SHF_val), d(a.HLF_gray, b.HLF_gray), d(a.HLF_val, b.HLF_val), d(a.HLF_R, b.HLF_R), d(a.warm_pct, b.warm_pct), d(a.green_pct, b.green_pct), d(a.redbloom_pct, b.redbloom_pct)].map((c, i) => String(c).padEnd(w[i])).join(''));
  console.log('-'.repeat(w.reduce((a, b) => a + b, 0)));
}
console.log('\nwrote descent-colorfair-iter2fix.json');
