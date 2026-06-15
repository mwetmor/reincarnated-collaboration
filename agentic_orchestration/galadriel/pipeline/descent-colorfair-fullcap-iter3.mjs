// descent-colorfair-diagnostic.mjs — galadriel measurement-validity check on the descent.
//
// WHY THIS EXISTS (Discipline #4 right-tool / #11 empirical-inspection):
// The register-2 instruments (lifecycle-score-corpus.mjs) read GRAY-LUMA
// (0.299R+0.587G+0.114B). They were CALIBRATED on the prior brighter, less-saturated
// register (Addendum B). The iter1 MOOD-LIFT deliberately shifted to a DARKER, MORE-
// SATURATED, colored-light register (green atmosphere + saturated red/green/amber blooms
// on a dark floor). A saturated-RED bloom (high R, low G/B) has a high MAX-CHANNEL value
// but a MODERATE gray-luma -> it does NOT cross the gray-luma >0.80 HLF gate even when it
// is visually a prominent hero bloom. So a naive gray-luma re-score reads the DELIBERATE
// darkening + saturation as a "failure." That is the classic looks-wrong-but-is-an-
// instrument-artifact trap. This diagnostic measures BOTH:
//   - GRAY-LUMA metrics (continuity with the prior baseline; the "old gate")
//   - VALUE-CHANNEL (HSV V = max(R,G,B)) metrics (the register-FAIR read for colored light)
//   - per-channel highlight fractions (where does the bloom actually blow out?)
// so the LIGHTING + VFX gates can be judged correctly for the NEW register, not the old one.
//
// No silent transformation: raw captures preserved; reads them, writes nothing to them.

import sharp from 'sharp';
import { readdirSync, writeFileSync } from 'fs';
import { join } from 'path';

const TARGET_W = 960;
const DIR = "/Users/admin/Games/reincarnated-godot/harness_logs/iter3_fullcap";

const ZONES = [
  { tag: 'zone0_threshold',    kind: 'swarm' },
  { tag: 'zone1_arcane',       kind: 'near'  },
  { tag: 'zone2_warhall',      kind: 'near'  },
  { tag: 'zone3_oubliette',    kind: 'swarm' },
  { tag: 'zone4_antechamber',  kind: 'near'  },
  { tag: 'zone5_sanctum',      kind: 'near'  },
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

  const gray = new Float64Array(n);   // 0..255 gray luma (the OLD instrument)
  const val = new Float64Array(n);    // 0..255 HSV V = max(R,G,B) (register-fair)
  let hiGray = 0;                     // gray-luma > 204 (old HLF gate)
  let hiVal = 0;                      // value > 204 (any channel bright -> colored bloom)
  let hiR = 0, hiG = 0, hiB = 0;      // per-channel > 204
  // "warm-point" + "green-glow" fractions: saturated bright points that read as motivated
  // light. warm = bright AND R dominates G,B (brazier/torch). green = bright AND G dominates.
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
    // motivated-light point classes (bright value + clear hue dominance)
    if (v > 150 && r > g + 25 && r > b + 25) warmPts++;         // amber/red warm point
    if (v > 130 && g > r + 20 && g > b + 20) greenPts++;        // green soul-glow
    if (v > 160 && r > 150 && r > b + 40 && g < r - 20) redBloom++; // saturated red/orange bloom
  }

  const gSorted = gray.slice().sort();
  const vSorted = val.slice().sort();
  const ldrGray = percentile(gSorted, 0.95) - percentile(gSorted, 0.05);   // OLD LDR
  const ldrVal = percentile(vSorted, 0.95) - percentile(vSorted, 0.05);    // value-channel LDR (fair)
  // shadow fraction on value channel (true shadow = dark in ALL channels)
  let shfVal = 0;
  for (let p = 0; p < n; p++) if (val[p] < 31) shfVal++;
  let shfGray = 0;
  for (let p = 0; p < n; p++) if (gray[p] < 31) shfGray++;

  return {
    LDR_gray: +ldrGray.toFixed(1), LDR_val: +ldrVal.toFixed(1),
    SHF_gray: +(100 * shfGray / n).toFixed(2), SHF_val: +(100 * shfVal / n).toFixed(2),
    HLF_gray: +(100 * hiGray / n).toFixed(3),   // the OLD VFX-gate proxy
    HLF_val: +(100 * hiVal / n).toFixed(3),     // register-FAIR bloom proxy (any-channel bright)
    HLF_R: +(100 * hiR / n).toFixed(3), HLF_G: +(100 * hiG / n).toFixed(3), HLF_B: +(100 * hiB / n).toFixed(3),
    warm_pct: +(100 * warmPts / n).toFixed(3), green_pct: +(100 * greenPts / n).toFixed(3),
    redbloom_pct: +(100 * redBloom / n).toFixed(3),
  };
}

async function scoreZone(z) {
  const PREFIX = `gal_descent_${z.tag}_`;
  const files = readdirSync(DIR)
    .filter(f => f.startsWith(PREFIX) && f.endsWith('.png'))
    .map(f => ({ f, n: parseInt(f.slice(PREFIX.length, -4), 10) }))
    .filter(x => Number.isFinite(x.n)).sort((a, b) => a.n - b.n);
  if (files.length === 0) return { ...z, error: 'no frames' };
  const rows = [];
  for (const { f, n } of files) rows.push({ frame: n, ...(await measure(join(DIR, f))) });
  // gate reads: bloom = PEAK across window; lighting = window mean + floor
  const peakOf = k => Math.max(...rows.map(r => r[k]));
  const meanOf = k => rows.reduce((a, r) => a + r[k], 0) / rows.length;
  const minOf = k => Math.min(...rows.map(r => r[k]));
  const ext = {
    LDR_gray_mean: +meanOf('LDR_gray').toFixed(1), LDR_gray_floor: +minOf('LDR_gray').toFixed(1),
    LDR_val_mean: +meanOf('LDR_val').toFixed(1), LDR_val_floor: +minOf('LDR_val').toFixed(1),
    SHF_gray_mean: +meanOf('SHF_gray').toFixed(1), SHF_val_mean: +meanOf('SHF_val').toFixed(1),
    HLF_gray_peak: +peakOf('HLF_gray').toFixed(3), HLF_val_peak: +peakOf('HLF_val').toFixed(3),
    HLF_R_peak: +peakOf('HLF_R').toFixed(3), HLF_G_peak: +peakOf('HLF_G').toFixed(3), HLF_B_peak: +peakOf('HLF_B').toFixed(3),
    warm_peak: +peakOf('warm_pct').toFixed(3), green_peak: +peakOf('green_pct').toFixed(3),
    redbloom_peak: +peakOf('redbloom_pct').toFixed(3),
  };
  return { ...z, n_frames: rows.length, extracts: ext, frames: rows };
}

const out = { scored_at: new Date().toISOString(), purpose: 'measurement-validity: gray-luma (old gate) vs value-channel (register-fair) on the iter1 mood-lift descent', zones: [] };
for (const z of ZONES) { process.stderr.write(`diag ${z.tag}...\n`); out.zones.push(await scoreZone(z)); }
writeFileSync(join(process.cwd(), 'descent-colorfair-fullcap-iter3.json'), JSON.stringify(out, null, 2));

console.log('=== COLOR-FAIR DIAGNOSTIC — gray-luma (OLD gate) vs VALUE-channel (register-fair) ===\n');
console.log('VFX gate question: is there a prominent hero bloom? gray-luma misses SATURATED-color blooms.\n');
const cols = ['zone', 'LDRgray', 'LDRval', 'SHFval%', 'HLFgray', 'HLFval', 'HLF_R', 'warm%', 'green%', 'redbloom%'];
const w = [18, 9, 8, 9, 9, 9, 8, 8, 9, 10];
console.log(cols.map((c, i) => c.padEnd(w[i])).join(''));
console.log('-'.repeat(w.reduce((a, b) => a + b, 0)));
for (const z of out.zones) {
  if (z.error) { console.log(`${z.tag}: ERROR`); continue; }
  const e = z.extracts;
  console.log([z.tag, e.LDR_gray_mean, e.LDR_val_mean, e.SHF_val_mean, e.HLF_gray_peak, e.HLF_val_peak, e.HLF_R_peak, e.warm_peak, e.green_peak, e.redbloom_peak].map((c, i) => String(c).padEnd(w[i])).join(''));
}
console.log('\nINTERPRETATION KEY:');
console.log('  HLFgray << HLFval  => bloom IS bright but COLORED (gray-luma gate blind to it) -> instrument artifact, not VFX failure');
console.log('  HLF_R high in sanctum/warhall => the red/amber bloom blows out the RED channel even when gray-luma does not');
console.log('  LDRval >> LDRgray => colored-light DRAMA the gray instrument compresses');
console.log('  warm%/green% => motivated golden/green light-point density (the reference look)');
