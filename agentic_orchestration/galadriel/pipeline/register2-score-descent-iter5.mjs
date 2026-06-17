// register2-score-descent-iter5.mjs — galadriel register-2 ROUND-2 RE-SCORE across the
// iter5 RELIT descent (6 relit zones + 3 recomposed establish), PLUS the zone2 erupt VFX
// validator (3 baked-replay frames), for the descent run-to-green Round-2.
//
// CONTEXT: drax landed Round-2 (iter5, commit 7ce990e in reincarnated-godot) — a per-chamber
// KEY lighting lift (NOT fill) + establish recompose, in response to the iter4 baseline
// (commit 4d6efd2: composite mean 3.14/5, 0/9 PASS — flat-dim-mid-grey lighting deficit).
//
// THE ACCEPTANCE CRITERION (gandalf design call — Round-2 brief §3):
//   The fix was "key not fill." So the lift must show LDR lifted toward ~176 (the boss-arena
//   PASS profile) AND SHF deepened — BOTH axes simultaneously, per zone. A zone that raised LDR
//   but FLATTENED SHF means drax raised the fill, not restored the key → REJECT. Target =
//   lit-volume-IN-dark (bright pool + deep surround), never a brighter uniform wash.
//   This scorer reports LDR and SHF SEPARATELY per zone + the iter4->iter5 delta on BOTH axes,
//   and flags any zone that moved only one axis.
//
// NORTH-STAR (boss-arena PASS, lifecycle-scores-boss.json): LDR mean 175.97 / SHF mean 42.74%
//   / HLF peak 4.013%. The relight target LDR~176 is the EXACT profile the boss column popped at.
//
// Instrument defs BYTE-IDENTICAL to register-metrics.mjs / register2-score-descent-iter4.mjs
// (960w inside-fit, gray luma for LDR/SHF/HLF/HFD/LMV, raw RGB for SAT; HLF>0.80 luma,
// SHF<0.12 luma, LDR=p95-p05). Values directly comparable to iter4 + the boss-arena scorer.
//
// *** METHOD CAVEAT — single-still vs windowed, the VFX read (UNCHANGED from iter4) ***
// The 9 relit stills are SINGLE COMBAT STILLS with hero SummonGlow FROZEN AT CHARGE — they
// UNDER-READ VFX by construction (galadriel F1). The LIGHTING gate (LDR+SHF) is correctly read
// on these stills (it measures the AMBIENT mood between fires — gandalf canon call). The VFX
// gate is INHERITED-PASS (gandalf canon call, zone-invariant column proven 4.01% in boss arena);
// the zone2_erupt_* baked-replay frames are the inheritance VALIDATOR on the hardest-lit case.
//   *** VFX-MEASUREMENT RECONCILIATION (galadriel's instrument, this scorer's job) ***
//   drax's zone2 erupt validator reads ~0.2% HLF (baked-replay) vs boss-arena live ~4%. The
//   question I own: is 0.2%-baked-vs-4%-live a FAIR comparison, or is the baked-replay harness
//   UNDERCOUNTING the eruption? I measure all 3 erupt frames here + the relit zone2 ambient as
//   the baseline-against-which-the-column-pops, and adjudicate the comparison in the scorecard.
//
// No silent transformation: raw captures preserved; this reads them, writes only JSON.

import sharp from 'sharp';
import { writeFileSync } from 'fs';
import { join } from 'path';

const TARGET_W = 960;
const DIR = '/Users/admin/Games/reincarnated-godot/harness_logs';

// North-star (boss-arena PASS) for inline reference.
const BOSS = { LDR_mean: 175.97, SHF_mean: 42.74, HLF_peak: 4.013 };

// iter5 RELIT stills in descent order. iter4_* = the iter4 baseline metrics (from
// register2-scores-descent-iter4.json) carried per-frame so the scorer emits the
// iter4->iter5 delta on BOTH LDR and SHF inline. drax_key = drax's exact key lever for this
// zone (energy/range) for the lever->measurement correlation. prior_windowed_HLF = iter1
// windowed HLF peak for the same zone identity (the fair-capture VFX reference).
const FRAMES = [
  { tag: 'zone0_threshold',   file: 'descent_iter5_zone0_04.png', identity: 'threshold (graveyard)', footprint: 'open_arena 50x50',     kind: 'swarm',     drax_key: '1.9 / range 38',          prior_windowed_HLF: 1.565, iter4: { LDR: 122, SHF: 16.57, HLF: 0.14,  LMV: 28.72, SAT: 0.460 } },
  { tag: 'zone1_arcane',      file: 'descent_iter5_zone1_05.png', identity: 'arcane chamber',        footprint: 'magic_pack 32.7x14',   kind: 'near',      drax_key: '2.3 / range 38',          prior_windowed_HLF: 2.958, iter4: { LDR: 108, SHF: 18.07, HLF: 0.09,  LMV: 28.05, SAT: 0.445 } },
  { tag: 'zone2_warhall',     file: 'descent_iter5_zone2_06.png', identity: 'war hall',              footprint: 'elite_pack 28x28',     kind: 'near',      drax_key: '3.4 / range 40 (brightest)', prior_windowed_HLF: 4.063, iter4: { LDR: 103, SHF: 12.76, HLF: 0.132, LMV: 23.46, SAT: 0.425 } },
  { tag: 'zone3_oubliette',   file: 'descent_iter5_zone3_07.png', identity: 'oubliette (corridor)',  footprint: 'chokepoint 10x50',     kind: 'swarm',     drax_key: '4.2 / torch-line',        prior_windowed_HLF: 1.680, iter4: { LDR: 105, SHF: 58.15, HLF: 0.059, LMV: 16.66, SAT: 0.696 } },
  { tag: 'zone4_antechamber', file: 'descent_iter5_zone4_08.png', identity: 'antechamber (soulfire)',footprint: 'mini_boss 30x30',      kind: 'near',      drax_key: '2.1 / range 36',          prior_windowed_HLF: 3.047, iter4: { LDR: 116, SHF: 12.95, HLF: 0.056, LMV: 23.26, SAT: 0.443 } },
  { tag: 'zone5_sanctum',     file: 'descent_iter5_zone5_09.png', identity: 'sanctum (boss bloom)',  footprint: 'boss_with_adds 30x30', kind: 'near',      drax_key: '2.2 / range 38',          prior_windowed_HLF: 3.927, iter4: { LDR: 118, SHF: 11.41, HLF: 0.063, LMV: 24.29, SAT: 0.436 } },
  { tag: 'establish_01',      file: 'descent_iter5_establish_01.png', identity: 'establishing spine (recomposed)', footprint: 'cam 31m/fov50', kind: 'establish', drax_key: 'recompose 40->31m/fov60->50', prior_windowed_HLF: null, iter4: { LDR: 94, SHF: 59.64, HLF: 0.079, LMV: 12.82, SAT: 0.746 } },
  { tag: 'establish_02',      file: 'descent_iter5_establish_02.png', identity: 'establishing spine (recomposed)', footprint: 'cam 31m/fov50', kind: 'establish', drax_key: 'recompose 40->31m/fov60->50', prior_windowed_HLF: null, iter4: { LDR: 94, SHF: 59.64, HLF: 0.081, LMV: 12.85, SAT: 0.746 } },
  { tag: 'establish_03',      file: 'descent_iter5_establish_03.png', identity: 'establishing spine (recomposed)', footprint: 'cam 31m/fov50', kind: 'establish', drax_key: 'recompose 40->31m/fov60->50', prior_windowed_HLF: null, iter4: { LDR: 94, SHF: 59.64, HLF: 0.076, LMV: 12.74, SAT: 0.746 } },
];

// zone2 erupt VFX validator (baked-replay, circle-off column capture). The inheritance-PASS
// validator on the hardest-lit case. drax reads ~0.2% HLF here; I measure all 3 + compare to
// the relit zone2 AMBIENT (above) as the backdrop-against-which-the-column-pops, and to the
// boss-arena live 4.01% peak. The reconciliation question: fair comparison or undercount?
const ERUPT_FRAMES = [
  { tag: 'zone2_erupt_78', file: 'descent_iter5_zone2_erupt_78.png', note: 'baked-replay eruption sample' },
  { tag: 'zone2_erupt_82', file: 'descent_iter5_zone2_erupt_82.png', note: 'baked-replay eruption sample (drax-cited)' },
  { tag: 'zone2_erupt_84', file: 'descent_iter5_zone2_erupt_84.png', note: 'baked-replay eruption sample' },
];

// ---- instruments (BYTE-IDENTICAL math to register-metrics.mjs / iter4 scorer) ----
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
  // full percentile spread for the luma-distribution diagnostic (flat-mid vs lit-volume-in-dark proof)
  const p05 = percentile(lumaSorted, 0.05), p25 = percentile(lumaSorted, 0.25);
  const p50 = percentile(lumaSorted, 0.50), p75 = percentile(lumaSorted, 0.75);
  const p95 = percentile(lumaSorted, 0.95);
  const ldr = p95 - p05;
  let hi = 0, lo = 0, mid = 0, drk = 0, brt = 0;
  for (let i = 0; i < gray.length; i++) {
    const v = gray[i];
    if (v > 204) hi++;          // > 0.80*255  (HLF highlight)
    if (v < 31) lo++;           // < 0.12*255  (SHF shadow)
    if (v >= 60 && v <= 150) mid++;  // dim mid-band (the "flat dim grey wash" signature)
    if (v < 31) drk++;          // deep dark mass
    if (v > 180) brt++;         // bright-key mass
  }
  const hlf = (100 * hi) / gray.length;
  const shf = (100 * lo) / gray.length;
  const { data: rgb, info: ri } = await sharp(path)
    .resize(TARGET_W, null, { fit: 'inside' }).removeAlpha().raw()
    .toBuffer({ resolveWithObject: true });
  let satSum = 0, satSS = 0, np = ri.width * ri.height;
  // warm:cool channel ratio — the hue-register check (warm key vs cool wash)
  let rSum = 0, gSum = 0, bSum = 0;
  for (let i = 0; i < rgb.length; i += 3) {
    const r = rgb[i] / 255, gg = rgb[i + 1] / 255, b = rgb[i + 2] / 255;
    const max = Math.max(r, gg, b), min = Math.min(r, gg, b);
    const s = max === 0 ? 0 : (max - min) / max;
    satSum += s; satSS += s * s;
    rSum += rgb[i]; gSum += rgb[i + 1]; bSum += rgb[i + 2];
  }
  const satMean = satSum / np;
  const satStd = Math.sqrt(Math.max(0, satSS / np - satMean * satMean));
  const warmCool = +((rSum + gSum * 0.5) / (bSum + gSum * 0.5)).toFixed(3); // >1 = warm-dominant
  return {
    HFD: +hfd.toFixed(2), LMV: +lmv.toFixed(2), LDR: +ldr.toFixed(1),
    SAT_mean: +satMean.toFixed(3), SAT_std: +satStd.toFixed(3),
    HLF_pct: +hlf.toFixed(3), SHF_pct: +shf.toFixed(2),
    warmCool,
    p05, p25, p50, p75, p95,
    mid_pct: +((100 * mid) / gray.length).toFixed(1),
    dark_pct: +((100 * drk) / gray.length).toFixed(1),
    bright_pct: +((100 * brt) / gray.length).toFixed(2),
    dims: `${w}x${h}`,
  };
}

// Gate logic — same thresholds as the boss-arena + iter4 scorers:
//   Lighting gate (CV-assist): LDR >= 115 AND SHF >= 30%
//   VFX gate (CV-assist): HLF >= 1.5%
function gates(m) {
  return {
    LDR_pass_115: m.LDR >= 115,
    SHF_pass_30: m.SHF_pct >= 30,
    lighting_cv_pass: m.LDR >= 115 && m.SHF_pct >= 30,
    HLF_pass_1p5: m.HLF_pct >= 1.5,
    HLF_x_threshold: +(m.HLF_pct / 1.5).toFixed(2),
  };
}

// the ACCEPTANCE-CRITERION adjudicator: did BOTH axes move the right way?
//   key_restored  = LDR rose AND SHF rose (lit-volume-in-dark — the "key not fill" target)
//   fill_raised    = LDR rose but SHF fell/flat (raised the fill — REJECT signature)
function axisVerdict(m, iter4) {
  const dLDR = +(m.LDR - iter4.LDR).toFixed(1);
  const dSHF = +(m.SHF_pct - iter4.SHF).toFixed(2);
  const ldrUp = dLDR > 2;            // meaningful LDR rise (>2 luma)
  const shfUp = dSHF > 1.0;          // meaningful SHF deepen (>1 pt)
  const shfFlatOrDown = dSHF <= 1.0; // flattened or barely moved
  let verdict;
  if (ldrUp && shfUp) verdict = 'KEY_RESTORED (both axes up — lit-volume-in-dark)';
  else if (ldrUp && shfFlatOrDown) verdict = 'FILL_RAISED? (LDR up, SHF flat/down — REJECT signature)';
  else if (!ldrUp && shfUp) verdict = 'SHF_ONLY (deepened dark, LDR did not rise)';
  else verdict = 'NEITHER (no meaningful move on either axis)';
  return { dLDR, dSHF, ldrUp, shfUp, verdict };
}

const out = {
  scored_at: new Date().toISOString(),
  corpus: 'iter5 RELIT descent — descent_iter5_{zone0..5}.png (6 relit) + descent_iter5_establish_{01..03}.png (3 recomposed) — 9 SINGLE STILLS (combat camera; hero VFX FROZEN AT CHARGE). PLUS descent_iter5_zone2_erupt_{78,82,84}.png (baked-replay eruption VFX validator).',
  build: 'drax Round-2 iter5, commit 7ce990e (reincarnated-godot): per-chamber KEY lighting lift + establish recompose.',
  baseline: 'iter4, commit 4d6efd2: composite mean 3.14/5, 0/9 PASS — flat-dim-mid-grey lighting deficit.',
  instrument_defs: 'BYTE-IDENTICAL to register-metrics.mjs / register2-score-descent-iter4.mjs',
  north_star_boss_arena: BOSS,
  acceptance_criterion: 'gandalf design call (Round-2 brief §3): per zone, LDR lifted toward ~176 AND SHF deepened — BOTH axes simultaneously. LDR-up-but-SHF-flat = fill-raised (REJECT). Target = lit-volume-in-dark, not a brighter uniform wash.',
  method_caveat: 'SINGLE-STILL relit captures with hero SummonGlow frozen at charge UNDER-READ VFX by construction (galadriel F1). The LIGHTING gate (LDR+SHF) IS correctly read on these stills (ambient mood between fires — gandalf canon call). VFX gate = inherited-PASS (zone-invariant column, boss-arena 4.01% proof); the zone2_erupt_* baked-replay frames are the inheritance VALIDATOR on the hardest-lit case. The 0.2%-baked-vs-4%-live HLF reconciliation is adjudicated in the scorecard.',
  thresholds: { lighting: 'LDR>=115 AND SHF>=30%', vfx: 'HLF>=1.5%', composite_bar: '~4.0 (boss-arena PASS bar)' },
  frames: [],
  erupt_validator: [],
};

for (const f of FRAMES) {
  process.stderr.write(`scoring ${f.tag}...\n`);
  const m = await measure(join(DIR, f.file));
  out.frames.push({ ...f, metrics: m, gates: gates(m), axisVerdict: axisVerdict(m, f.iter4) });
}
for (const f of ERUPT_FRAMES) {
  process.stderr.write(`scoring ${f.tag} (erupt validator)...\n`);
  const m = await measure(join(DIR, f.file));
  out.erupt_validator.push({ ...f, metrics: m, gates: gates(m) });
}

const outPath = join(process.cwd(), 'register2-scores-descent-iter5.json');
writeFileSync(outPath, JSON.stringify(out, null, 2));

// ---- console report ----
console.log('=== iter5 RELIT DESCENT — REGISTER-2 CV ROLL-UP (9 stills) + iter4->iter5 DELTA ===\n');
console.log(`north-star (boss-arena PASS): LDR ${BOSS.LDR_mean} / SHF ${BOSS.SHF_mean}% / HLF peak ${BOSS.HLF_peak}%`);
console.log('thresholds: LIGHTING = LDR>=115 AND SHF>=30% | VFX = HLF>=1.5% (windowing-blocked on stills)\n');
const cols = ['frame', 'kind', 'LDR', 'dLDR', 'SHF%', 'dSHF', 'LIGHT', 'verdict'];
const w = [18, 10, 6, 7, 7, 8, 6, 46];
console.log(cols.map((c, i) => c.padEnd(w[i])).join(''));
console.log('-'.repeat(w.reduce((a, b) => a + b, 0)));
for (const f of out.frames) {
  const m = f.metrics, g = f.gates, a = f.axisVerdict;
  const row = [
    f.tag, f.kind, m.LDR,
    (a.dLDR >= 0 ? '+' : '') + a.dLDR,
    m.SHF_pct, (a.dSHF >= 0 ? '+' : '') + a.dSHF,
    g.lighting_cv_pass ? 'PASS' : 'fail',
    a.verdict,
  ];
  console.log(row.map((c, i) => String(c).padEnd(w[i])).join(''));
}

console.log('\n=== LUMA-DISTRIBUTION DIAGNOSTIC (flat-dim-mid vs lit-volume-in-dark proof) ===');
const dcols = ['frame', 'p05', 'p50', 'p95', 'mid%', 'dark%', 'bright%', 'warmCool'];
const dw = [18, 6, 6, 6, 7, 7, 8, 9];
console.log(dcols.map((c, i) => c.padEnd(dw[i])).join(''));
console.log('-'.repeat(dw.reduce((a, b) => a + b, 0)));
for (const f of out.frames) {
  const m = f.metrics;
  console.log([f.tag, m.p05, m.p50, m.p95, m.mid_pct, m.dark_pct, m.bright_pct, m.warmCool]
    .map((c, i) => String(c).padEnd(dw[i])).join(''));
}

console.log('\n=== GATE CHECK (CV-assist; manual scores authored in scorecard) ===');
for (const f of out.frames) {
  const m = f.metrics, g = f.gates;
  console.log(`${f.tag.padEnd(18)} LIGHT:${g.lighting_cv_pass ? 'PASS' : 'FAIL'}(LDR ${m.LDR}${g.LDR_pass_115 ? '' : '<115'}/SHF ${m.SHF_pct}%${g.SHF_pass_30 ? '' : '<30'})  VFX:${g.HLF_pass_1p5 ? 'PASS' : 'FAIL'}(HLF ${m.HLF_pct}%, ${g.HLF_x_threshold}x — STILL, frozen-charge)  key:${f.drax_key}`);
}

console.log('\n=== zone2 ERUPT VFX VALIDATOR (baked-replay; the inheritance-PASS hardest-lit case) ===');
console.log(`boss-arena live HLF peak = ${BOSS.HLF_peak}% | relit zone2 AMBIENT HLF (frozen-charge still) = ${out.frames[2].metrics.HLF_pct}%`);
const ecols = ['frame', 'HLF%', 'HLFx', 'LDR', 'SHF%', 'p95', 'bright%'];
const ew = [18, 8, 7, 6, 7, 6, 8];
console.log(ecols.map((c, i) => c.padEnd(ew[i])).join(''));
console.log('-'.repeat(ew.reduce((a, b) => a + b, 0)));
for (const f of out.erupt_validator) {
  const m = f.metrics, g = f.gates;
  console.log([f.tag, m.HLF_pct, g.HLF_x_threshold + 'x', m.LDR, m.SHF_pct, m.p95, m.bright_pct]
    .map((c, i) => String(c).padEnd(ew[i])).join(''));
}
const eruptHLF = out.erupt_validator.map(f => f.metrics.HLF_pct);
const eruptBright = out.erupt_validator.map(f => f.metrics.bright_pct);
const z2ambHLF = out.frames[2].metrics.HLF_pct;
const z2ambBright = out.frames[2].metrics.bright_pct;
console.log(`\nerupt HLF range: ${Math.min(...eruptHLF)}–${Math.max(...eruptHLF)}% | erupt bright%(>180) range: ${Math.min(...eruptBright)}–${Math.max(...eruptBright)}%`);
console.log(`zone2 ambient (no-erupt) HLF: ${z2ambHLF}% | ambient bright%(>180): ${z2ambBright}%`);
console.log(`POP RATIO (erupt-bright / ambient-bright): ${(Math.max(...eruptBright) / Math.max(z2ambBright, 0.001)).toFixed(1)}x — does the column pop against the relit backdrop?`);

console.log(`\nwrote ${outPath}`);
console.log('\nNOTE: VFX gate FAILs on frozen-charge stills are EXPECTED (galadriel F1); VFX gate is inherited-PASS (gandalf canon).');
console.log('The erupt-validator HLF reconciliation (0.2%-baked vs 4%-live) is adjudicated in the scorecard prose.');
