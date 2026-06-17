// register2-score-descent-iter6.mjs — drax SELF-MEASURE of the iter6 GLOBAL-RIG-MATCH
// descent against galadriel's COMMITTED scorer math (byte-identical instruments to
// register2-score-descent-iter5.mjs / register-metrics.mjs). This is drax's probe-first
// read before galadriel's independent re-score (gandalf Round-3 brief §1.1 + §4.4).
//
// WHAT CHANGED iter5 -> iter6: the GLOBAL env rig only (gandalf Round-3 §1.1) — the descent
// abandoned the proven register-2 rig; iter6 restores it while KEEPING the green fog identity:
//   tonemap_mode FILMIC(2) -> ACES(3) | tonemap_white 6.0 -> 8.0 | tonemap_exposure 1.0 -> 0.95
//   ambient_light_energy 0.24 -> 0.17 (the SHF lever) | fog_density 0.0052 -> 0.010 (green color kept)
// NO per-chamber key retune in this pass (clean attribution — one change at a time).
//
// ACCEPTANCE (gandalf §1.1 read): zone2 LDR jumps toward ~176 + SHF deepens (bright%>180 climbs
// off ~0.2%, p95 climbs off ~125). If so, the global rig WAS the suppressor — apply globally, do
// NOT also retune keys. Probe-first: drax reads ZONE2 ONLY to decide before judging the rest.
//
// NORTH-STAR (boss-arena PASS): LDR 175.97 / SHF 42.74% / HLF peak 4.013%.
// iter5 baseline carried per-frame inline (from register2-scores-descent-iter5.json) for the delta.
// Synty-derivative captures local-only, git-ignored — this reads them, writes only JSON.

import sharp from 'sharp';
import { writeFileSync } from 'fs';
import { join } from 'path';

const TARGET_W = 960;
const DIR = '/Users/admin/Games/reincarnated-godot/harness_logs';
const BOSS = { LDR_mean: 175.97, SHF_mean: 42.74, HLF_peak: 4.013 };

// iter6 RELIT stills in descent order. iter5 = the iter5 baseline metrics (from
// register2-scores-descent-iter5.json) carried per-frame so the scorer emits the
// iter5->iter6 delta on BOTH LDR and SHF inline.
const FRAMES = [
  { tag: 'zone0_threshold',   file: 'descent_iter6_zone0_04.png',     kind: 'swarm',     iter5: { LDR: 122, SHF: 16.65 } },
  { tag: 'zone1_arcane',      file: 'descent_iter6_zone1_05.png',     kind: 'near',      iter5: { LDR: 107, SHF: 17.73 } },
  { tag: 'zone2_warhall',     file: 'descent_iter6_zone2_06.png',     kind: 'near',      iter5: { LDR: 103, SHF: 12.70 } },
  { tag: 'zone3_oubliette',   file: 'descent_iter6_zone3_07.png',     kind: 'swarm',     iter5: { LDR: 105, SHF: 57.89 } },
  { tag: 'zone4_antechamber', file: 'descent_iter6_zone4_08.png',     kind: 'near',      iter5: { LDR: 107, SHF: 16.55 } },
  { tag: 'zone5_sanctum',     file: 'descent_iter6_zone5_09.png',     kind: 'near',      iter5: { LDR: 118, SHF: 12.43 } },
  { tag: 'establish_01',      file: 'descent_iter6_establish_01.png', kind: 'establish', iter5: { LDR: 97,  SHF: 48.56 } },
  { tag: 'establish_02',      file: 'descent_iter6_establish_02.png', kind: 'establish', iter5: { LDR: 97,  SHF: 48.56 } },
  { tag: 'establish_03',      file: 'descent_iter6_establish_03.png', kind: 'establish', iter5: { LDR: 97,  SHF: 48.56 } },
];

// ---- instruments (BYTE-IDENTICAL math to register2-score-descent-iter5.mjs) ----
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
  const p05 = percentile(lumaSorted, 0.05), p25 = percentile(lumaSorted, 0.25);
  const p50 = percentile(lumaSorted, 0.50), p75 = percentile(lumaSorted, 0.75);
  const p95 = percentile(lumaSorted, 0.95);
  const ldr = p95 - p05;
  let hi = 0, lo = 0, mid = 0, drk = 0, brt = 0;
  for (let i = 0; i < gray.length; i++) {
    const v = gray[i];
    if (v > 204) hi++;          // > 0.80*255  (HLF highlight)
    if (v < 31) lo++;           // < 0.12*255  (SHF shadow)
    if (v >= 60 && v <= 150) mid++;
    if (v < 31) drk++;
    if (v > 180) brt++;         // bright-key mass
  }
  const hlf = (100 * hi) / gray.length;
  const shf = (100 * lo) / gray.length;
  const { data: rgb, info: ri } = await sharp(path)
    .resize(TARGET_W, null, { fit: 'inside' }).removeAlpha().raw()
    .toBuffer({ resolveWithObject: true });
  let satSum = 0, satSS = 0, np = ri.width * ri.height;
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
  const warmCool = +((rSum + gSum * 0.5) / (bSum + gSum * 0.5)).toFixed(3);
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

function gates(m) {
  return {
    LDR_pass_115: m.LDR >= 115,
    SHF_pass_30: m.SHF_pct >= 30,
    lighting_cv_pass: m.LDR >= 115 && m.SHF_pct >= 30,
    HLF_pass_1p5: m.HLF_pct >= 1.5,
    HLF_x_threshold: +(m.HLF_pct / 1.5).toFixed(2),
  };
}

function axisVerdict(m, base) {
  const dLDR = +(m.LDR - base.LDR).toFixed(1);
  const dSHF = +(m.SHF_pct - base.SHF).toFixed(2);
  const ldrUp = dLDR > 2;
  const shfUp = dSHF > 1.0;
  const shfFlatOrDown = dSHF <= 1.0;
  let verdict;
  if (ldrUp && shfUp) verdict = 'KEY_RESTORED (both axes up — lit-volume-in-dark)';
  else if (ldrUp && shfFlatOrDown) verdict = 'FILL_RAISED? (LDR up, SHF flat/down)';
  else if (!ldrUp && shfUp) verdict = 'SHF_ONLY (deepened dark, LDR did not rise)';
  else verdict = 'NEITHER (no meaningful move on either axis)';
  return { dLDR, dSHF, ldrUp, shfUp, verdict };
}

const out = {
  scored_at: new Date().toISOString(),
  corpus: 'iter6 GLOBAL-RIG-MATCH descent — descent_iter6_{zone0..5}.png (6) + establish_{01..03}.png (3).',
  build: 'drax Round-3 iter6 (reincarnated-godot): _build_global_environment matched to proven register-2 rig (ACES/0.95/8.0/ambient0.17/fog0.010), green fog identity kept. NO key retune.',
  baseline: 'iter5, commit 7ce990e: per-chamber KEY lift — galadriel REJECTED 0/6 (global env was the suppressor).',
  north_star_boss_arena: BOSS,
  frames: [],
};

for (const f of FRAMES) {
  process.stderr.write(`scoring ${f.tag}...\n`);
  const m = await measure(join(DIR, f.file));
  out.frames.push({ ...f, metrics: m, gates: gates(m), axisVerdict: axisVerdict(m, f.iter5) });
}

const outPath = join(process.cwd(), 'register2-scores-descent-iter6.json');
writeFileSync(outPath, JSON.stringify(out, null, 2));

console.log('=== iter6 GLOBAL-RIG-MATCH DESCENT — REGISTER-2 CV ROLL-UP (drax self-measure) + iter5->iter6 DELTA ===\n');
console.log(`north-star (boss-arena PASS): LDR ${BOSS.LDR_mean} / SHF ${BOSS.SHF_mean}% / HLF peak ${BOSS.HLF_peak}%`);
console.log('thresholds: LIGHTING = LDR>=115 AND SHF>=30%  (zone3 judged on CONTRAST criterion, not LDR-176)\n');
const cols = ['frame', 'kind', 'LDR', 'dLDR', 'SHF%', 'dSHF', 'LIGHT', 'verdict'];
const w = [18, 10, 6, 8, 7, 9, 6, 46];
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

console.log(`\nwrote ${outPath}`);
