// lifecycle-score.mjs — galadriel CV instrument across a motion-sequence lifecycle
//
// Purpose: score a windowed-VFX motion sequence (the 2026-06-14 Godot "lift" capture:
// dark POLYGON dungeon + composed Synty knight + FX_Fire_Large_01 hero-skill bloom that
// ignites mid-sequence) against the register-2 rubric instruments.
//
// WHY motion, not a single still: per galadriel F1 finding, stills under-represent VFX
// (the highest-leverage axis). The fire is a *windowed event*; a single frame samples
// one arbitrary point in [pre-ignition .. peak .. burn .. settle]. The rubric instruments
// LDR / SHF / HLF must be read across the lifecycle and reported per-phase + aggregate.
//
// Instruments (reuse the exact definitions from register-metrics.mjs — same kernels,
// same thresholds, so values are directly comparable to the 2026-06-14 register baseline):
//   LDR — Luminance Dynamic Range (p95 - p05 of luma).      Lighting-drama instrument.
//   SHF — Shadow Fraction (% px luma < 0.12).               Dark-mood instrument.
//   HLF — Highlight Fraction (% px luma > 0.80).            VFX/bloom/glow instrument.
//   HFD — High-Frequency Detail (mean |Laplacian|).         Supporting (busyness; NOT a target).
//   LMV — Local Material Variance (mean 8x8-tile luma std). Supporting material context.
//   SAT — mean HSV saturation + std.                        Supporting color register.
//
// No silent transformation: resize to 960w inside-fit, grayscale for luma instruments,
// raw RGB for SAT. Raw captures preserved; this reads them, writes nothing to them.
//
// Output: per-frame JSON rows + per-lifecycle-phase aggregates + whole-sequence aggregates,
// + the rubric-relevant peak/representative values (HLF peak for hero-bloom proof; LDR/SHF
// dark-mood-window means).

import sharp from 'sharp';
import { readdirSync, writeFileSync } from 'fs';
import { join, basename } from 'path';

const TARGET_W = 960;
const DIR = '/Users/admin/Games/reincarnated-godot/harness_logs';
const PREFIX = '11_lift_capture_';

// ---- instruments (identical math to register-metrics.mjs) ----
function laplacianEnergy(gray, w, h) {
  let sum = 0, n = 0;
  for (let y = 1; y < h - 1; y++) {
    for (let x = 1; x < w - 1; x++) {
      const i = y * w + x;
      const lap = -4 * gray[i] + gray[i - 1] + gray[i + 1] + gray[i - w] + gray[i + w];
      sum += Math.abs(lap); n++;
    }
  }
  return sum / n;
}
function localMaterialVariance(gray, w, h, gx = 8, gy = 8) {
  const tw = Math.floor(w / gx), th = Math.floor(h / gy);
  const tileStds = [];
  for (let ty = 0; ty < gy; ty++) {
    for (let tx = 0; tx < gx; tx++) {
      let s = 0, ss = 0, cnt = 0;
      for (let y = ty * th; y < (ty + 1) * th; y++) {
        for (let x = tx * tw; x < (tx + 1) * tw; x++) {
          const v = gray[y * w + x]; s += v; ss += v * v; cnt++;
        }
      }
      const mean = s / cnt;
      tileStds.push(Math.sqrt(Math.max(0, ss / cnt - mean * mean)));
    }
  }
  return tileStds.reduce((a, b) => a + b, 0) / tileStds.length;
}
function percentile(sorted, p) {
  const idx = Math.min(sorted.length - 1, Math.max(0, Math.floor(p * sorted.length)));
  return sorted[idx];
}

async function measure(path) {
  const g = sharp(path).resize(TARGET_W, null, { fit: 'inside' }).grayscale();
  const { data: gray, info } = await g.raw().toBuffer({ resolveWithObject: true });
  const w = info.width, h = info.height;
  const hfd = laplacianEnergy(gray, w, h);
  const lmv = localMaterialVariance(gray, w, h);
  const lumaSorted = Float64Array.from(gray).slice().sort();
  const ldr = percentile(lumaSorted, 0.95) - percentile(lumaSorted, 0.05);
  let hi = 0, lo = 0;
  for (let i = 0; i < gray.length; i++) {
    if (gray[i] > 204) hi++;   // > 0.80*255
    if (gray[i] < 31) lo++;    // < 0.12*255
  }
  const hlf = (100 * hi) / gray.length;
  const shf = (100 * lo) / gray.length;
  const { data: rgb, info: ri } = await sharp(path)
    .resize(TARGET_W, null, { fit: 'inside' }).removeAlpha().raw()
    .toBuffer({ resolveWithObject: true });
  let satSum = 0, satSS = 0, np = ri.width * ri.height;
  for (let i = 0; i < rgb.length; i += 3) {
    const r = rgb[i] / 255, gg = rgb[i + 1] / 255, b = rgb[i + 2] / 255;
    const max = Math.max(r, gg, b), min = Math.min(r, gg, b);
    const s = max === 0 ? 0 : (max - min) / max;
    satSum += s; satSS += s * s;
  }
  const satMean = satSum / np;
  const satStd = Math.sqrt(Math.max(0, satSS / np - satMean * satMean));
  return {
    HFD: +hfd.toFixed(2), LMV: +lmv.toFixed(2), LDR: +ldr.toFixed(1),
    SAT_mean: +satMean.toFixed(3), SAT_std: +satStd.toFixed(3),
    HLF_pct: +hlf.toFixed(3), SHF_pct: +shf.toFixed(2), dims: `${w}x${h}`,
  };
}

// ---- frame discovery + numeric ordering (NOT lexical — _100 must follow _99) ----
const files = readdirSync(DIR)
  .filter(f => f.startsWith(PREFIX) && f.endsWith('.png'))
  .map(f => ({ f, n: parseInt(f.slice(PREFIX.length, -4), 10) }))
  .filter(x => Number.isFinite(x.n))
  .sort((a, b) => a.n - b.n);

if (files.length === 0) { console.error('no frames found'); process.exit(1); }

const rows = [];
for (const { f, n } of files) {
  const m = await measure(join(DIR, f));
  rows.push({ frame: n, file: f, ...m });
}

// ---- lifecycle phase segmentation (frame-indexed; visually anchored) ----
// Boundaries derived from manual inspection of frames 01/15/30/45/60/80/100:
//   pre-ignition  01-08 : fire not yet bloomed; warm under-glow building
//   ignition-rise 09-22 : flame climbing
//   peak-bloom    23-40 : full vertical column, scene-wide warm spill
//   live-burn     41-70 : sustained licking flame
//   waning-drift  71-94 : flame collapsing, smoke drift
//   settle        95-100: residual flame, figure fully re-revealed
const PHASES = [
  ['pre-ignition', 1, 8],
  ['ignition-rise', 9, 22],
  ['peak-bloom', 23, 40],
  ['live-burn', 41, 70],
  ['waning-drift', 71, 94],
  ['settle', 95, 100],
];
const NUMERIC = ['HFD', 'LMV', 'LDR', 'SAT_mean', 'SAT_std', 'HLF_pct', 'SHF_pct'];
function agg(subset) {
  const out = {};
  for (const k of NUMERIC) {
    const vals = subset.map(r => r[k]);
    const mean = vals.reduce((a, b) => a + b, 0) / vals.length;
    out[k] = { mean: +mean.toFixed(3), min: +Math.min(...vals).toFixed(3), max: +Math.max(...vals).toFixed(3) };
  }
  out.n_frames = subset.length;
  return out;
}

const phaseAgg = {};
for (const [name, lo, hi] of PHASES) {
  const sub = rows.filter(r => r.frame >= lo && r.frame <= hi);
  if (sub.length) phaseAgg[name] = { range: `${lo}-${hi}`, ...agg(sub) };
}
const whole = agg(rows);

// ---- rubric-relevant extracts ----
const hlfPeak = Math.max(...rows.map(r => r.HLF_pct));
const hlfPeakFrame = rows.find(r => r.HLF_pct === hlfPeak).frame;
const ldrPeak = Math.max(...rows.map(r => r.LDR));
const ldrPeakFrame = rows.find(r => r.LDR === ldrPeak).frame;
// dark-mood window = pre-ignition + settle (figure-readable, atmosphere-dominant phases),
// since peak-bloom floods the frame with fire-light and is NOT where dark-mood is read.
const darkWindow = rows.filter(r => (r.frame <= 8) || (r.frame >= 95));
const darkAgg = agg(darkWindow);

const summary = {
  capture_set: '11_lift_capture (Godot Movie Maker, 1152x648, 100 frames)',
  scored_at: new Date().toISOString(),
  instrument_defs: 'identical to register-metrics.mjs (960w inside-fit, gray luma, raw RGB sat)',
  n_frames: rows.length,
  rubric_extracts: {
    HLF_peak_pct: +hlfPeak.toFixed(3), HLF_peak_frame: hlfPeakFrame,
    HLF_threshold_pct: 1.5, HLF_peak_passes: hlfPeak >= 1.5,
    LDR_peak: +ldrPeak.toFixed(1), LDR_peak_frame: ldrPeakFrame,
    LDR_threshold: 115,
    LDR_whole_mean: whole.LDR.mean, LDR_whole_mean_passes: whole.LDR.mean >= 115,
    LDR_darkwindow_mean: darkAgg.LDR.mean, LDR_darkwindow_passes: darkAgg.LDR.mean >= 115,
    SHF_threshold_pct: 30,
    SHF_whole_mean: whole.SHF_pct.mean,
    SHF_darkwindow_mean: darkAgg.SHF_pct.mean, SHF_darkwindow_passes: darkAgg.SHF_pct.mean >= 30,
  },
  whole_sequence: whole,
  dark_mood_window: { frames: 'pre-ignition(1-8)+settle(95-100)', ...darkAgg },
  phases: phaseAgg,
};

const outPath = join(process.cwd(), 'lifecycle-scores.json');
writeFileSync(outPath, JSON.stringify({ summary, frames: rows }, null, 2));

// ---- console report ----
console.log('=== LIFECYCLE CV SCORE — 11_lift_capture (100 frames) ===\n');
console.log('Per-phase aggregates (mean [min..max]):');
const ph = ['LDR', 'SHF_pct', 'HLF_pct', 'LMV', 'HFD', 'SAT_mean'];
const head = 'phase'.padEnd(14) + 'range'.padEnd(8) + ph.map(k => k.padEnd(20)).join('');
console.log(head);
console.log('-'.repeat(head.length));
for (const [name] of PHASES) {
  const a = phaseAgg[name]; if (!a) continue;
  const cells = ph.map(k => `${a[k].mean} [${a[k].min}..${a[k].max}]`.padEnd(20)).join('');
  console.log(name.padEnd(14) + a.range.padEnd(8) + cells);
}
console.log('\nWhole-sequence: ' + ph.map(k => `${k}=${whole[k].mean}`).join('  '));
console.log('Dark-mood window (1-8 + 95-100): ' + ph.map(k => `${k}=${darkAgg[k].mean}`).join('  '));
console.log('\n=== RUBRIC EXTRACTS ===');
console.log(JSON.stringify(summary.rubric_extracts, null, 2));
console.log(`\nwrote ${outPath}`);
