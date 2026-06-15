// lifecycle-score-cathedral.mjs — galadriel CV instrument across the Godot Cathedral lifecycle
//
// Purpose: re-validate "register-2 A-holds" on REAL curated Synty content. drax instanced
// Synty's OWN Demo_Cathedral_01.tscn (Cathedral section isolated), applied the SAME lift
// recipe 1:1 (near-black warm ambient + warm key rake + cold rim + filmic tonemap +
// glow/SSAO/warm-fog), and added a body-anchored hero VFX: a red pentagram that CHARGES
// then ERUPTS a GPUParticles3D summon fire column.
//
// Instrument definitions are BYTE-IDENTICAL to lifecycle-score.mjs / register-metrics.mjs
// (960w inside-fit, gray luma for LDR/SHF/HLF/HFD/LMV, raw RGB for SAT; HLF>0.80 luma,
// SHF<0.12 luma, LDR=p95-p05). Only two things change vs the lift scorer:
//   (1) PREFIX -> '12_cathedral_capture_'
//   (2) phase boundaries reshaped to drax's hero-event timing (charge ~30, erupt ~52)
// Same instruments => values directly comparable to the lift (which is the whole point:
// "same register band as the lift" is the claim under test).
//
// WHY motion not still (galadriel F1): stills under-represent VFX (the highest-leverage
// axis). The fire column is a windowed event; a single still samples one arbitrary point.
// THE LOAD-BEARING CAVEAT (carried from the invocation): the Synty marketing render is a
// MOOD/CALIBRATION anchor, NOT a pass bar. We score our BUILD against the RUBRIC, not a
// pixel-match to Synty's Unity post. VFX is scored on its own register merits (body-anchored
// hero bloom present? HLF magnitude? clean lifecycle?), NOT fidelity to the Synty sigil.
//
// No silent transformation: raw captures preserved; this reads them, writes nothing to them.

import sharp from 'sharp';
import { readdirSync, writeFileSync } from 'fs';
import { join } from 'path';

const TARGET_W = 960;
const DIR = '/Users/admin/Games/reincarnated-godot/harness_logs';
const PREFIX = '12_cathedral_capture_';

// ---- instruments (identical math to register-metrics.mjs / lifecycle-score.mjs) ----
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

// ---- lifecycle phase segmentation (drax hero-event timing: charge ~30, erupt ~52) ----
// braziers burn from frame 0; fog/dust always-on. So even pre-charge is a lit dark volume.
//   pre-ignition  01-22 : braziers + atmosphere only; pentagram not yet charging hard
//   charge        23-44 : red pentagram charging; warm under-bloom building at body
//   eruption-rise 45-55 : summon fire column erupts (~52) and climbs
//   peak-bloom    56-72 : full column, scene-wide warm spill
//   live-burn     73-88 : sustained burn
//   waning-settle 89-100: column collapses to residual ember; scene re-revealed
const PHASES = [
  ['pre-ignition', 1, 22],
  ['charge', 23, 44],
  ['eruption-rise', 45, 55],
  ['peak-bloom', 56, 72],
  ['live-burn', 73, 88],
  ['waning-settle', 89, 100],
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
// dark-mood window = pre-ignition + waning-settle (figure/scene-readable, atmosphere-dominant
// phases) — NOT eruption/peak where the column floods the frame with fire-light.
const darkWindow = rows.filter(r => (r.frame <= 22) || (r.frame >= 89));
const darkAgg = agg(darkWindow);

const summary = {
  capture_set: '12_cathedral_capture (Godot Movie Maker, 1152x648, 100 frames)',
  scene: "Synty Demo_Cathedral_01.tscn (Cathedral section isolated) + lift recipe 1:1 + red pentagram CHARGE->ERUPT GPUParticles3D summon fire column",
  scored_at: new Date().toISOString(),
  instrument_defs: 'BYTE-IDENTICAL to register-metrics.mjs / lifecycle-score.mjs (960w inside-fit, gray luma, raw RGB sat; HLF>0.80, SHF<0.12, LDR=p95-p05)',
  drax_hero_timing: 'braziers burn from frame 0; pentagram charges ~30; erupts summon fire column ~52',
  n_frames: rows.length,
  rubric_extracts: {
    HLF_peak_pct: +hlfPeak.toFixed(3), HLF_peak_frame: hlfPeakFrame,
    HLF_threshold_pct: 1.5, HLF_peak_passes: hlfPeak >= 1.5,
    LDR_peak: +ldrPeak.toFixed(1), LDR_peak_frame: ldrPeakFrame,
    LDR_threshold: 115,
    LDR_whole_mean: whole.LDR.mean, LDR_whole_mean_passes: whole.LDR.mean >= 115,
    LDR_darkwindow_mean: darkAgg.LDR.mean, LDR_darkwindow_passes: darkAgg.LDR.mean >= 115,
    SHF_threshold_pct: 30,
    SHF_whole_mean: whole.SHF_pct.mean, SHF_whole_mean_passes: whole.SHF_pct.mean >= 30,
    SHF_darkwindow_mean: darkAgg.SHF_pct.mean, SHF_darkwindow_passes: darkAgg.SHF_pct.mean >= 30,
  },
  whole_sequence: whole,
  dark_mood_window: { frames: 'pre-ignition(1-22)+waning-settle(89-100)', ...darkAgg },
  phases: phaseAgg,
};

const outPath = join(process.cwd(), 'lifecycle-scores-cathedral.json');
writeFileSync(outPath, JSON.stringify({ summary, frames: rows }, null, 2));

// ---- console report ----
console.log('=== LIFECYCLE CV SCORE — 12_cathedral_capture (100 frames) ===\n');
console.log('Per-phase aggregates (mean [min..max]):');
const ph = ['LDR', 'SHF_pct', 'HLF_pct', 'LMV', 'HFD', 'SAT_mean'];
const head = 'phase'.padEnd(15) + 'range'.padEnd(8) + ph.map(k => k.padEnd(22)).join('');
console.log(head);
console.log('-'.repeat(head.length));
for (const [name] of PHASES) {
  const a = phaseAgg[name]; if (!a) continue;
  const cells = ph.map(k => `${a[k].mean} [${a[k].min}..${a[k].max}]`.padEnd(22)).join('');
  console.log(name.padEnd(15) + a.range.padEnd(8) + cells);
}
console.log('\nWhole-sequence: ' + ph.map(k => `${k}=${whole[k].mean}`).join('  '));
console.log('Dark-mood window (1-22 + 89-100): ' + ph.map(k => `${k}=${darkAgg[k].mean}`).join('  '));
console.log('\n=== RUBRIC EXTRACTS ===');
console.log(JSON.stringify(summary.rubric_extracts, null, 2));
console.log(`\nwrote ${outPath}`);
