// lifecycle-score-corpus.mjs — galadriel CV instrument across drax's 6-room PARAMETRIC corpus
//
// Purpose: score the SINGLE parametric ArenaRoom (godot 3855b6b) rendering all 6
// arena.py::ALL_SCENARIOS footprints off ONE constant lift rig, against galadriel's
// register-2 rubric (composite >=3.6; lighting >=4 AND VFX >=4 MANDATORY), lifecycle-
// sampled over all 100 frames per room. The design claim under test: "one spec-driven
// room holds the register across EVERY footprint."
//
// Instrument definitions BYTE-IDENTICAL to register-metrics.mjs / lifecycle-score*.mjs
// (960w inside-fit, gray luma for LDR/SHF/HLF/HFD/LMV, raw RGB for SAT; HLF>0.80 luma,
// SHF<0.12 luma, LDR=p95-p05). Same instruments => values directly comparable to the
// graybox lift (4.50), Synty cathedral (5.00), and Build #1 boss-arena (4.00).
//
// Gate-relevant reads are WHOLE-SEQUENCE means + peaks/floors (NOT per-scenario hand-
// segmented phases): lighting gate = LDR mean/floor + SHF mean/floor; VFX gate = HLF peak
// (>=1 hero bloom). The HLF curve markers (ignition / peak / collapse capture-frames) are
// reported per scenario for transparency + lifecycle honesty (each room votes its own).
//
// WHY motion not still (galadriel F1): stills under-represent VFX (highest-leverage axis).
// Each room's hero-VFX is a windowed event (sigil ember -> charge -> erupt -> collapse).
// MARKETING-RENDER CAVEAT (carried 1:1): Synty marketing frames are a MOOD/CALIBRATION
// anchor, NOT a pass bar. We score the BUILD against the RUBRIC. Prior scorecards (lift
// 4.50, cathedral 5.00) are CALIBRATION baselines only, not pass bars.
//
// No silent transformation: raw captures preserved; this reads them, writes nothing to them.

import sharp from 'sharp';
import { readdirSync, writeFileSync } from 'fs';
import { join } from 'path';

const TARGET_W = 960;
const DIR = '/Users/admin/Games/reincarnated-godot/harness_logs';
// scored in footprint-class order: near-square calibration anchor first, risky two last.
const SCENARIOS = [
  { id: 'boss_with_adds', footprint: '30x30', cls: 'near-square', anchor: 'boss(15,8)' },
  { id: 'elite_pack', footprint: '28x28', cls: 'near-square', anchor: 'elite(14,6)' },
  { id: 'mini_boss', footprint: '30x30', cls: 'near-square', anchor: 'mini-boss(15,6)' },
  { id: 'open_arena', footprint: '50x50', cls: 'large near-square', anchor: 'room-center (all-swarm)' },
  { id: 'magic_pack', footprint: '32.7x14', cls: 'wide-shallow (RISKY)', anchor: 'caster(16.35,3)' },
  { id: 'chokepoint_corridor', footprint: '10x50', cls: 'long-corridor (RISKY)', anchor: 'room-center (all-swarm)' },
];

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

async function scoreScenario(s) {
  const PREFIX = `arena_${s.id}_`;
  const files = readdirSync(DIR)
    .filter(f => f.startsWith(PREFIX) && f.endsWith('.png') && /^[0-9]+$/.test(f.slice(PREFIX.length, -4)))
    .map(f => ({ f, n: parseInt(f.slice(PREFIX.length, -4), 10) }))
    .filter(x => Number.isFinite(x.n))
    .sort((a, b) => a.n - b.n);
  if (files.length === 0) return { ...s, error: 'no frames' };

  const rows = [];
  for (const { f, n } of files) rows.push({ frame: n, ...(await measure(join(DIR, f))) });

  const whole = agg(rows);
  // HLF lifecycle markers (each room votes its own): ignition = first frame HLF crosses
  // 1.5% (the bloom threshold) rising; peak = argmax HLF; collapse = last frame >=1.5%.
  const hlfPeak = Math.max(...rows.map(r => r.HLF_pct));
  const hlfPeakFrame = rows.find(r => r.HLF_pct === hlfPeak).frame;
  const above = rows.filter(r => r.HLF_pct >= 1.5).map(r => r.frame);
  const ignitionFrame = above.length ? Math.min(...above) : null;
  const collapseFrame = above.length ? Math.max(...above) : null;
  const ldrFloor = Math.min(...rows.map(r => r.LDR));
  const ldrFloorFrame = rows.find(r => r.LDR === ldrFloor).frame;
  const shfFloor = Math.min(...rows.map(r => r.SHF_pct));
  // dark-mood window = the non-bloom frames (HLF < 1.5%) — atmosphere-dominant; verifies
  // the dark-mood holds independent of the hero bloom flooding the frame.
  const darkFrames = rows.filter(r => r.HLF_pct < 1.5);
  const darkAgg = darkFrames.length ? agg(darkFrames) : null;

  const extracts = {
    LDR_mean: whole.LDR.mean, LDR_floor: +ldrFloor.toFixed(1), LDR_floor_frame: ldrFloorFrame,
    LDR_pass_115: whole.LDR.mean >= 115 && ldrFloor >= 115,
    SHF_mean: whole.SHF_pct.mean, SHF_floor: +shfFloor.toFixed(2),
    SHF_pass_30: whole.SHF_pct.mean >= 30,
    HLF_peak: +hlfPeak.toFixed(3), HLF_peak_frame: hlfPeakFrame,
    HLF_peak_pass_1p5: hlfPeak >= 1.5, HLF_peak_x_threshold: +(hlfPeak / 1.5).toFixed(2),
    LMV_mean: whole.LMV.mean,
    ignition_frame: ignitionFrame, collapse_frame: collapseFrame,
    bloom_active_frames: above.length,
  };
  return { ...s, n_frames: rows.length, whole, dark_window: darkAgg, extracts, frames: rows };
}

const out = { scored_at: new Date().toISOString(), corpus: 'arena_<scenario>_01..100 (godot 3855b6b, parametric ArenaRoom)', instrument_defs: 'BYTE-IDENTICAL to register-metrics.mjs / lifecycle-score*.mjs', scenarios: [] };
for (const s of SCENARIOS) {
  process.stderr.write(`scoring ${s.id}...\n`);
  out.scenarios.push(await scoreScenario(s));
}

const outPath = join(process.cwd(), 'lifecycle-scores-corpus.json');
writeFileSync(outPath, JSON.stringify(out, null, 2));

// ---- console report ----
console.log('=== 6-ROOM PARAMETRIC CORPUS — CV ROLL-UP (lifecycle-sampled, 100 frames/room) ===\n');
const cols = ['scenario', 'class', 'LDR_mean', 'LDR_floor', 'SHF_mean', 'HLF_peak', 'HLFx', 'LMV', 'ign', 'pk', 'col'];
const w = [20, 22, 9, 10, 8, 9, 6, 7, 5, 4, 4];
console.log(cols.map((c, i) => c.padEnd(w[i])).join(''));
console.log('-'.repeat(w.reduce((a, b) => a + b, 0)));
for (const s of out.scenarios) {
  if (s.error) { console.log(`${s.id.padEnd(20)}${s.cls.padEnd(22)}ERROR: ${s.error}`); continue; }
  const e = s.extracts;
  const row = [s.id, s.cls, e.LDR_mean, e.LDR_floor, e.SHF_mean, e.HLF_peak, e.HLF_peak_x_threshold + 'x', e.LMV_mean, e.ignition_frame, e.HLF_peak_frame, e.collapse_frame];
  console.log(row.map((c, i) => String(c).padEnd(w[i])).join(''));
}
console.log('\n=== GATE CHECK (CV-assisted; manual scores authored in scorecard) ===');
console.log('thresholds: LDR mean&floor >=115 | SHF mean >=30% | HLF peak >=1.5%');
for (const s of out.scenarios) {
  if (s.error) continue;
  const e = s.extracts;
  console.log(`${s.id.padEnd(20)} LDR:${e.LDR_pass_115 ? 'PASS' : 'FAIL'}  SHF:${e.SHF_pass_30 ? 'PASS' : 'FAIL'}  HLF-bloom:${e.HLF_peak_pass_1p5 ? 'PASS' : 'FAIL'} (${e.HLF_peak_x_threshold}x)`);
}
console.log(`\nwrote ${outPath}`);
