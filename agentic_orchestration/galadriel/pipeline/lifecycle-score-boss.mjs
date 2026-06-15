// lifecycle-score-boss.mjs — galadriel CV instrument across the Godot BOSS-ARENA lifecycle
//
// Purpose: score drax's SPEC-FAITHFUL BATTLE ROOM #1 — SCENARIO_BOSS_WITH_ADDS (30x30),
// commit 53e6c3c in reincarnated-godot — against galadriel's register-2 rubric (composite
// >=3.6; lighting >=4 AND VFX >=4 MANDATORY), lifecycle-sampled over all 100 frames.
//
// drax replicated the engine spec EXACTLY (arena 30x30; player(15,25) boss(15,8)
// adds(3,26)&(27,26)); Dark Fantasy art dresses the fixed footprint (Diablo procedural-
// dungeon contract). Hero VFX = boss-anchored red ritual sigil that CHARGES then ERUPTS a
// GPUParticles3D fire column. A "CombatFill" cool overhead pool lifts the four figures out
// of the dark floor — the explicit register-2-vs-fight-readability lever.
//
// Instrument definitions are BYTE-IDENTICAL to register-metrics.mjs / lifecycle-score.mjs /
// lifecycle-score-cathedral.mjs (960w inside-fit, gray luma for LDR/SHF/HLF/HFD/LMV, raw RGB
// for SAT; HLF>0.80 luma, SHF<0.12 luma, LDR=p95-p05). Only two things change vs the cathedral
// scorer:
//   (1) PREFIX -> '13_boss_arena_capture_'
//   (2) phase boundaries RE-DERIVED from THIS capture's own HLF curve (NOT reused from the
//       cathedral). drax sim-frame timing (charge ~30, erupt ~52, collapse ~320) is in SIM
//       frames; the 100 captured PNGs sample the lifecycle, so the eruption lands at a
//       DIFFERENT capture-frame index than the cathedral. Phase boundaries are set from the
//       empirical HLF peak location below (substrate votes; § 3.6 OP discipline).
// Same instruments => values directly comparable to the cathedral (5.00) and lift (4.50).
//
// WHY motion not still (galadriel F1): stills under-represent VFX (highest-leverage axis).
// THE LOAD-BEARING CAVEAT: the Synty marketing render is a MOOD/CALIBRATION anchor, NOT a
// pass bar. We score our BUILD against the RUBRIC. drax self-sanity CV (LDR 172.7 / SHF 43.8%
// / HLF peak 4.02%) is NOT a score — re-derived independently here.
//
// No silent transformation: raw captures preserved; this reads them, writes nothing to them.

import sharp from 'sharp';
import { readdirSync, writeFileSync } from 'fs';
import { join } from 'path';

const TARGET_W = 960;
const DIR = '/Users/admin/Games/reincarnated-godot/harness_logs';
const PREFIX = '13_boss_arena_capture_';

// ---- instruments (identical math to register-metrics.mjs / lifecycle-score*.mjs) ----
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

// ---- lifecycle phase segmentation ----
// RE-DERIVED from this capture's own HLF curve (capture-frame space; substrate votes).
// Boss-summon shape: ember -> CHARGE -> ERUPT -> peak-bloom -> live-burn -> COLLAPSE/ember.
// Phase boundaries set from empirical HLF peak (printed below). If the eruption frame
// differs materially from these constants, ADJUST here and re-run (documented inline).
// EMPIRICALLY RE-DERIVED from this capture's HLF curve (NOT inherited from cathedral):
//   ember         01-08 : sigil ember only; HLF~0.4, LDR~150 (deepest dark-mood)
//   ignition-rise 09-20 : sharp ignition at f9 (HLF 0.52->2.79); ramps to peak
//   peak-bloom    21-34 : HLF peak f21 (4.01%); column at full bloom
//   sustained-burn 35-86: long flat burn plateau; HLF ~3.3-3.8 (the boss-summon hold)
//   waning-settle 87-100: collapse f87-88 (HLF 2.9->1.36->0.6); residual ember/re-reveal
const PHASES = [
  ['ember', 1, 8],
  ['ignition-rise', 9, 20],
  ['peak-bloom', 21, 34],
  ['sustained-burn', 35, 86],
  ['waning-settle', 87, 100],
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
const hlfFloor = Math.min(...rows.map(r => r.HLF_pct));
const hlfFloorFrame = rows.find(r => r.HLF_pct === hlfFloor).frame;
const ldrPeak = Math.max(...rows.map(r => r.LDR));
const ldrPeakFrame = rows.find(r => r.LDR === ldrPeak).frame;
const ldrFloor = Math.min(...rows.map(r => r.LDR));
const ldrFloorFrame = rows.find(r => r.LDR === ldrFloor).frame;
const shfFloor = Math.min(...rows.map(r => r.SHF_pct));
const shfFloorFrame = rows.find(r => r.SHF_pct === shfFloor).frame;
// dark-mood window = ember + waning-settle (atmosphere-dominant, figure-readable, NOT
// the fire-flooded burn plateau) — the honest dark-mood phases for the SHF/LDR threshold check.
const darkWindow = rows.filter(r => (r.frame <= 8) || (r.frame >= 87));
const darkAgg = agg(darkWindow);

const summary = {
  capture_set: '13_boss_arena_capture (Godot Movie Maker, 1152x648, 100 frames)',
  scene: "SCENARIO_BOSS_WITH_ADDS 30x30 spec-faithful (player(15,25) boss(15,8) adds(3,26)&(27,26)) + lift recipe + CombatFill readability pool + boss-anchored red ritual-sigil CHARGE->ERUPT GPUParticles3D fire column",
  commit: '53e6c3c (reincarnated-godot)',
  scored_at: new Date().toISOString(),
  instrument_defs: 'BYTE-IDENTICAL to register-metrics.mjs / lifecycle-score.mjs / lifecycle-score-cathedral.mjs (960w inside-fit, gray luma, raw RGB sat; HLF>0.80, SHF<0.12, LDR=p95-p05)',
  drax_sim_timing: 'sim frames: charge ~30, erupt ~52, collapse ~320 — capture subsamples the lifecycle so capture-frame eruption index differs',
  n_frames: rows.length,
  rubric_extracts: {
    HLF_peak_pct: +hlfPeak.toFixed(3), HLF_peak_frame: hlfPeakFrame,
    HLF_floor_pct: +hlfFloor.toFixed(3), HLF_floor_frame: hlfFloorFrame,
    HLF_threshold_pct: 1.5, HLF_peak_passes: hlfPeak >= 1.5,
    LDR_peak: +ldrPeak.toFixed(1), LDR_peak_frame: ldrPeakFrame,
    LDR_floor: +ldrFloor.toFixed(1), LDR_floor_frame: ldrFloorFrame,
    LDR_threshold: 115,
    LDR_whole_mean: whole.LDR.mean, LDR_whole_mean_passes: whole.LDR.mean >= 115,
    LDR_darkwindow_mean: darkAgg.LDR.mean, LDR_darkwindow_passes: darkAgg.LDR.mean >= 115,
    SHF_threshold_pct: 30,
    SHF_floor_pct: +shfFloor.toFixed(2), SHF_floor_frame: shfFloorFrame,
    SHF_whole_mean: whole.SHF_pct.mean, SHF_whole_mean_passes: whole.SHF_pct.mean >= 30,
    SHF_darkwindow_mean: darkAgg.SHF_pct.mean, SHF_darkwindow_passes: darkAgg.SHF_pct.mean >= 30,
  },
  whole_sequence: whole,
  dark_mood_window: { frames: 'pre-ignition(1-22)+waning-settle(89-100)', ...darkAgg },
  phases: phaseAgg,
};

const outPath = join(process.cwd(), 'lifecycle-scores-boss.json');
writeFileSync(outPath, JSON.stringify({ summary, frames: rows }, null, 2));

// ---- console report ----
console.log('=== LIFECYCLE CV SCORE — 13_boss_arena_capture (100 frames) ===\n');
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

// ---- HLF curve dump (every 5th frame) to verify/re-derive phase boundaries ----
console.log('\n=== HLF / LDR / SHF curve (every 5th frame; for phase re-derivation) ===');
for (const r of rows) {
  if (r.frame % 5 === 1 || r.frame === hlfPeakFrame) {
    console.log(`f${String(r.frame).padStart(3)}  HLF=${String(r.HLF_pct).padStart(7)}  LDR=${String(r.LDR).padStart(6)}  SHF=${String(r.SHF_pct).padStart(6)}  LMV=${r.LMV}`);
  }
}
console.log(`\nwrote ${outPath}`);
