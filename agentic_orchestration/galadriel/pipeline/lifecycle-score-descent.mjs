// lifecycle-score-descent.mjs — galadriel register-2 RE-SCORE across the CONNECTED descent.
//
// Purpose: re-score drax's 6 battle footprints AFTER they were (a) migrated into ONE
// connected "arena descent" scene (corridors, ~247m spine, stepped down in Y) and (b)
// given a MOOD-LIFT pass (global ambient 0.5->0.26, floor albedo *0.40, saturated green
// fog, denser dressing, magenta-square artifact removed). The question: do the register-2
// gates STILL HOLD now that the scene is connected + DARKER + denser dressing?
//   - Does the DARKER atmosphere HURT the LIGHTING axis (gate >=4) anywhere?
//   - Does it HELP the VFX axis (hero bloom should pop MORE against a darker frame)?
//
// Instrument defs BYTE-IDENTICAL to register-metrics.mjs / lifecycle-score-corpus.mjs
// (960w inside-fit, gray luma for LDR/SHF/HLF/HFD/LMV, raw RGB for SAT; HLF>0.80 luma,
// SHF<0.12 luma, LDR=p95-p05). Values directly comparable to ADDENDUM B (6 SEPARATE rooms,
// 84098c6): the prior pass to which this is the connected-scene successor.
//
// CAPTURE NOTE: in the baked descent the hero SummonGlow light is FROZEN at charge
// (render_descent_scene.gd:456), but FX_Fire_Large_01 / FX_Fog_01 / FX_Smoke_01 are
// GPUParticles that animate, so each zone was sampled over a windowed dwell (6 frames).
// Gate read = HLF PEAK across the zone's window (the particle-plume peak frame), per
// galadriel F1 (stills under-represent VFX). LDR/SHF read as window mean + floor.
//
// No silent transformation: raw captures preserved; this reads them, writes nothing to them.

import sharp from 'sharp';
import { readdirSync, writeFileSync } from 'fs';
import { join } from 'path';

const TARGET_W = 960;
const DIR = '/Users/admin/Games/reincarnated-godot/harness_logs';

// Connected-descent zones in descent order. Tag = the brief's zone0..zone5 label +
// footprint identity. ADDENDUM-B prior values (the 6 SEPARATE rooms, 84098c6) carried
// for delta. "kind": near = near-square marquee (entity-anchored bloom); swarm =
// swarm-centroid bloom (footprint-diluted HLF, manual prominence read resolves).
const ZONES = [
  { tag: 'zone0_threshold',    footprint: 'open_arena 50x50',   identity: 'threshold (graveyard)',  kind: 'swarm', prior_HLF: 1.565, prior_LDR: 132.3, prior_L: 4, prior_V: 4, prior_M: 3, prior_G: 4 },
  { tag: 'zone1_arcane',       footprint: 'magic_pack 32.7x14', identity: 'arcane chamber',          kind: 'near',  prior_HLF: 2.958, prior_LDR: 170.3, prior_L: 4, prior_V: 4, prior_M: 3, prior_G: 4 },
  { tag: 'zone2_warhall',      footprint: 'elite_pack 28x28',   identity: 'war hall',                kind: 'near',  prior_HLF: 4.063, prior_LDR: 180.7, prior_L: 4, prior_V: 4, prior_M: 4, prior_G: 4 },
  { tag: 'zone3_oubliette',    footprint: 'chokepoint 10x50',   identity: 'oubliette (corridor)',    kind: 'swarm', prior_HLF: 1.680, prior_LDR: 136.1, prior_L: 4, prior_V: 4, prior_M: 3, prior_G: 4 },
  { tag: 'zone4_antechamber',  footprint: 'mini_boss 30x30',    identity: 'antechamber (soulfire)',  kind: 'near',  prior_HLF: 3.047, prior_LDR: 172.8, prior_L: 4, prior_V: 4, prior_M: 4, prior_G: 4 },
  { tag: 'zone5_sanctum',      footprint: 'boss_with_adds 30x30',identity: 'sanctum (boss bloom)',   kind: 'near',  prior_HLF: 3.927, prior_LDR: 177.4, prior_L: 4, prior_V: 4, prior_M: 4, prior_G: 4 },
];

// ---- instruments (identical math to register-metrics.mjs / lifecycle-score-corpus.mjs) ----
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

async function scoreZone(z) {
  const PREFIX = `gal_descent_${z.tag}_`;
  const files = readdirSync(DIR)
    .filter(f => f.startsWith(PREFIX) && f.endsWith('.png'))
    .map(f => ({ f, n: parseInt(f.slice(PREFIX.length, -4), 10) }))
    .filter(x => Number.isFinite(x.n))
    .sort((a, b) => a.n - b.n);
  if (files.length === 0) return { ...z, error: 'no frames' };

  const rows = [];
  for (const { f, n } of files) rows.push({ frame: n, ...(await measure(join(DIR, f))) });

  const whole = agg(rows);
  const hlfPeak = Math.max(...rows.map(r => r.HLF_pct));
  const hlfPeakFrame = rows.find(r => r.HLF_pct === hlfPeak).frame;
  const ldrFloor = Math.min(...rows.map(r => r.LDR));
  const ldrPeak = Math.max(...rows.map(r => r.LDR));
  const shfFloor = Math.min(...rows.map(r => r.SHF_pct));

  const extracts = {
    LDR_mean: whole.LDR.mean, LDR_floor: +ldrFloor.toFixed(1), LDR_peak: +ldrPeak.toFixed(1),
    LDR_pass_115: whole.LDR.mean >= 115 && ldrFloor >= 115,
    SHF_mean: whole.SHF_pct.mean, SHF_floor: +shfFloor.toFixed(2),
    SHF_pass_30: whole.SHF_pct.mean >= 30,
    HLF_peak: +hlfPeak.toFixed(3), HLF_peak_frame: hlfPeakFrame,
    HLF_peak_pass_1p5: hlfPeak >= 1.5, HLF_peak_x_threshold: +(hlfPeak / 1.5).toFixed(2),
    LMV_mean: whole.LMV.mean, SAT_mean: whole.SAT_mean.mean,
    // deltas vs ADDENDUM B (6 separate rooms, 84098c6)
    dHLF_peak: +(hlfPeak - z.prior_HLF).toFixed(3),
    dLDR_mean: +(whole.LDR.mean - z.prior_LDR).toFixed(1),
    dHLFx: +((hlfPeak / 1.5) - (z.prior_HLF / 1.5)).toFixed(2),
  };
  return { ...z, n_frames: rows.length, whole, extracts, frames: rows };
}

const out = {
  scored_at: new Date().toISOString(),
  corpus: 'CONNECTED descent — gal_descent_<zone>_01..06 (scenes/arena_descent.tscn, iter1 mood-lift). 6 frames/zone windowed for particle peak.',
  instrument_defs: 'BYTE-IDENTICAL to register-metrics.mjs / lifecycle-score-corpus.mjs',
  prior_baseline: 'ADDENDUM B (6 SEPARATE rooms, godot 84098c6) — 6/6 PASS, mean composite 3.875',
  zones: [],
};
for (const z of ZONES) {
  process.stderr.write(`scoring ${z.tag}...\n`);
  out.zones.push(await scoreZone(z));
}

const outPath = join(process.cwd(), 'lifecycle-scores-descent.json');
writeFileSync(outPath, JSON.stringify(out, null, 2));

// ---- console report ----
console.log('=== CONNECTED DESCENT — REGISTER-2 CV ROLL-UP (windowed, 6 frames/zone) ===\n');
console.log('thresholds: LDR mean&floor >=115 | SHF mean >=30% | HLF peak >=1.5x (gate)\n');
const cols = ['zone', 'kind', 'LDRmean', 'dLDR', 'LDRfloor', 'SHF%', 'HLFpk', 'HLFx', 'dHLFx', 'LMV', 'SAT'];
const w = [18, 6, 9, 8, 10, 8, 8, 7, 8, 7, 6];
console.log(cols.map((c, i) => c.padEnd(w[i])).join(''));
console.log('-'.repeat(w.reduce((a, b) => a + b, 0)));
for (const z of out.zones) {
  if (z.error) { console.log(`${z.tag.padEnd(18)}ERROR: ${z.error}`); continue; }
  const e = z.extracts;
  const row = [z.tag, z.kind, e.LDR_mean, (e.dLDR_mean >= 0 ? '+' : '') + e.dLDR_mean, e.LDR_floor, e.SHF_mean, e.HLF_peak, e.HLF_peak_x_threshold + 'x', (e.dHLFx >= 0 ? '+' : '') + e.dHLFx, e.LMV_mean, e.SAT_mean];
  console.log(row.map((c, i) => String(c).padEnd(w[i])).join(''));
}
console.log('\n=== GATE CHECK (CV-assist; manual scores authored in scorecard) ===');
for (const z of out.zones) {
  if (z.error) continue;
  const e = z.extracts;
  console.log(`${z.tag.padEnd(18)} LDR:${e.LDR_pass_115 ? 'PASS' : 'FAIL'}(mean ${e.LDR_mean}/floor ${e.LDR_floor})  SHF:${e.SHF_pass_30 ? 'PASS' : 'FAIL'}(${e.SHF_mean}%)  VFX-bloom:${e.HLF_peak_pass_1p5 ? 'PASS' : 'FAIL'}(${e.HLF_peak_x_threshold}x, d${(e.dHLFx >= 0 ? '+' : '') + e.dHLFx})`);
}
console.log(`\nwrote ${outPath}`);
