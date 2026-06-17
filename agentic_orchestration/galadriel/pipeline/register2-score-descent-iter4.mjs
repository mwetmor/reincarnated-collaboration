// register2-score-descent-iter4.mjs — galadriel register-2 BASELINE score across the
// iter4 connected descent (9 stills: 6 zones + 3 establishing views).
//
// Purpose: produce the per-zone register-2 CV substrate for the iter4 run-to-green baseline
// scorecard. The architectural-grammar dimension + the warm:green hue dimension were already
// re-scored for iter4 (commit ffae02b, 2026-06-15); the FULL register-2 6-axis composite vs
// the ~4.0 PASS bar was NOT (the architectural rescore §6 explicitly deferred it). This is that.
//
// Instrument defs BYTE-IDENTICAL to register-metrics.mjs / lifecycle-score-descent.mjs
// (960w inside-fit, gray luma for LDR/SHF/HLF/HFD/LMV, raw RGB for SAT; HLF>0.80 luma,
// SHF<0.12 luma, LDR=p95-p05). Values directly comparable to the boss-arena lifecycle scorer.
//
// *** CRITICAL METHOD CAVEAT — single-still vs windowed, the VFX-freeze read ***
// These iter4 captures are SINGLE COMBAT STILLS, and in the baked descent the hero SummonGlow
// is FROZEN AT CHARGE (render note in lifecycle-score-descent.mjs:16-19). A single still of a
// frozen-charge hero event under-reads VFX/bloom by construction (galadriel F1: stills
// under-represent VFX — the highest-leverage axis). The boss-arena PASS was won on a 100-frame
// LIFECYCLE (HLF peaked 4.01% mid-eruption), NOT a charge-still. So the HLF numbers here are a
// CAPTURE-STATE artifact of the frozen single still, not a clean read of VFX-presence-in-motion.
// The scorecard reports the raw still HLF honestly AND flags it as windowing-blocked: the VFX
// gate cannot be fairly adjudicated from these stills. This is the single biggest finding for
// the run-to-green: it needs a windowed (animating-eruption) capture per zone to fairly gate VFX.
//
// No silent transformation: raw captures preserved; this reads them, writes only JSON.

import sharp from 'sharp';
import { writeFileSync } from 'fs';
import { join } from 'path';

const TARGET_W = 960;
const DIR = '/Users/admin/Games/reincarnated-godot/harness_logs';

// iter4 stills in descent order. prior_* carried from the iter1 gal_descent windowed scorer
// (lifecycle-scores-descent.json) so the run-to-green can see what the windowed VFX peak WAS
// for the same zone identity (the number a fair iter4 windowed re-capture should approach).
const FRAMES = [
  { tag: 'zone0_threshold',   file: 'descent_iter4_zone0_04.png',  identity: 'threshold (graveyard)', footprint: 'open_arena 50x50',    kind: 'swarm', prior_windowed_HLF: 1.565 },
  { tag: 'zone1_arcane',      file: 'descent_iter4_zone1_05.png',  identity: 'arcane chamber',        footprint: 'magic_pack 32.7x14',  kind: 'near',  prior_windowed_HLF: 2.958 },
  { tag: 'zone2_warhall',     file: 'descent_iter4_zone2_06.png',  identity: 'war hall',              footprint: 'elite_pack 28x28',    kind: 'near',  prior_windowed_HLF: 4.063 },
  { tag: 'zone3_oubliette',   file: 'descent_iter4_zone3_07.png',  identity: 'oubliette (corridor)',  footprint: 'chokepoint 10x50',    kind: 'swarm', prior_windowed_HLF: 1.680 },
  { tag: 'zone4_antechamber', file: 'descent_iter4_zone4_08.png',  identity: 'antechamber (soulfire)',footprint: 'mini_boss 30x30',     kind: 'near',  prior_windowed_HLF: 3.047 },
  { tag: 'zone5_sanctum',     file: 'descent_iter4_zone5_09.png',  identity: 'sanctum (boss bloom)',  footprint: 'boss_with_adds 30x30',kind: 'near',  prior_windowed_HLF: 3.927 },
  { tag: 'establish_01',      file: 'descent_iter4_establish_01.png', identity: 'establishing spine (diagonal)', footprint: 'full ~247m spine', kind: 'establish', prior_windowed_HLF: null },
  { tag: 'establish_02',      file: 'descent_iter4_establish_02.png', identity: 'establishing spine (diagonal)', footprint: 'full ~247m spine', kind: 'establish', prior_windowed_HLF: null },
  { tag: 'establish_03',      file: 'descent_iter4_establish_03.png', identity: 'establishing spine (diagonal)', footprint: 'full ~247m spine', kind: 'establish', prior_windowed_HLF: null },
];

// ---- instruments (BYTE-IDENTICAL math to register-metrics.mjs) ----
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

// Gate logic — same thresholds as the boss-arena scorecard:
//   Lighting gate (CV-assist): LDR >= 115 AND SHF >= 30%
//   VFX gate (CV-assist): HLF >= 1.5%
// NOTE on SHF for establish/corridor: the dark-void frames (oubliette, establish) read SHF
// 58-60% — they PASS the >=30% shadow criterion trivially but for the OPPOSITE reason
// (void-heavy, not lit-volume-in-dark). SHF>=30 is a necessary-not-sufficient dark-mood proxy;
// the manual lighting score adjudicates whether the dark is DRAMATIC (lit volume punched out of
// dark) or merely UNDERLIT (flat dark with no key). The scorecard prose carries that distinction.
function gates(m) {
  return {
    LDR_pass_115: m.LDR >= 115,
    SHF_pass_30: m.SHF_pct >= 30,
    lighting_cv_pass: m.LDR >= 115 && m.SHF_pct >= 30,
    HLF_pass_1p5: m.HLF_pct >= 1.5,
    HLF_x_threshold: +(m.HLF_pct / 1.5).toFixed(2),
  };
}

const out = {
  scored_at: new Date().toISOString(),
  corpus: 'iter4 CONNECTED descent — descent_iter4_{zone0..5,establish_01..03}.png — 9 SINGLE STILLS (combat camera; hero VFX FROZEN AT CHARGE).',
  instrument_defs: 'BYTE-IDENTICAL to register-metrics.mjs / lifecycle-score-descent.mjs',
  method_caveat: 'SINGLE-STILL captures with hero SummonGlow frozen at charge UNDER-READ VFX by construction (galadriel F1). HLF here is a capture-state artifact, NOT a clean VFX-in-motion read. VFX gate is windowing-blocked on these stills; prior_windowed_HLF (iter1 gal_descent windowed peaks) carried per zone as the fair-capture reference. The boss-arena VFX PASS was won on a 100-frame lifecycle, not a charge-still.',
  thresholds: { lighting: 'LDR>=115 AND SHF>=30%', vfx: 'HLF>=1.5%', composite_bar: '~4.0 (boss-arena PASS bar); composite>=3.6 with lighting>=4 AND VFX>=4 mandatory' },
  frames: [],
};

for (const f of FRAMES) {
  process.stderr.write(`scoring ${f.tag}...\n`);
  const m = await measure(join(DIR, f.file));
  out.frames.push({ ...f, metrics: m, gates: gates(m) });
}

const outPath = join(process.cwd(), 'register2-scores-descent-iter4.json');
writeFileSync(outPath, JSON.stringify(out, null, 2));

// ---- console report ----
console.log('=== iter4 CONNECTED DESCENT — REGISTER-2 CV ROLL-UP (9 single stills) ===\n');
console.log('thresholds: LIGHTING = LDR>=115 AND SHF>=30% | VFX = HLF>=1.5% (windowing-blocked on stills)\n');
const cols = ['frame', 'kind', 'LDR', 'SHF%', 'HLF%', 'HLFx', 'priorW_HLF', 'LMV', 'SAT', 'LIGHT', 'VFX'];
const w = [18, 10, 7, 8, 8, 7, 12, 7, 7, 7, 6];
console.log(cols.map((c, i) => c.padEnd(w[i])).join(''));
console.log('-'.repeat(w.reduce((a, b) => a + b, 0)));
for (const f of out.frames) {
  const m = f.metrics, g = f.gates;
  const row = [
    f.tag, f.kind, m.LDR, m.SHF_pct, m.HLF_pct, g.HLF_x_threshold + 'x',
    f.prior_windowed_HLF === null ? '—' : f.prior_windowed_HLF,
    m.LMV, m.SAT_mean,
    g.lighting_cv_pass ? 'PASS' : 'fail', g.HLF_pass_1p5 ? 'PASS' : 'fail',
  ];
  console.log(row.map((c, i) => String(c).padEnd(w[i])).join(''));
}
console.log('\n=== GATE CHECK (CV-assist; manual scores authored in scorecard) ===');
for (const f of out.frames) {
  const m = f.metrics, g = f.gates;
  console.log(`${f.tag.padEnd(18)} LIGHT:${g.lighting_cv_pass ? 'PASS' : 'FAIL'}(LDR ${m.LDR}${g.LDR_pass_115 ? '' : '<115'}/SHF ${m.SHF_pct}%${g.SHF_pass_30 ? '' : '<30'})  VFX:${g.HLF_pass_1p5 ? 'PASS' : 'FAIL'}(HLF ${m.HLF_pct}%, ${g.HLF_x_threshold}x — STILL, frozen-charge)`);
}
console.log(`\nwrote ${outPath}`);
console.log('\nNOTE: VFX gate FAILs are EXPECTED on frozen-charge single stills (galadriel F1).');
console.log('A fair VFX gate requires windowed (animating-eruption) capture per zone — flagged for run-to-green.');
