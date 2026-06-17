// register2-score-descent-iter7-establish.mjs — drax SELF-MEASURE of the iter7 CAMERA-ONLY establish
// RECOMPOSE against galadriel's COMMITTED scorer math (byte-identical instruments to
// register2-score-descent-iter6.mjs / register2-score-descent-iter5.mjs). This is drax's probe-first
// read before galadriel's independent re-score (gandalf Round-4 establish RECOMPOSE brief).
//
// WHAT CHANGED iter6 -> iter7: ONLY `_build_establishing_camera` (+ the capture harness's camera-walk).
// CAMERA-ONLY katabasis recompose — the GREEN chamber rig (_build_global_environment) is UNTOUCHED, so
// the 6 chambers held GREEN (zone metrics byte-identical to iter6). The 3 establish views are now 3
// GENUINELY DISTINCT warm beats (cam1 HERO / cam2 ElevatedLookDown / cam3 GroundIntimate), each LOW +
// short-aim + small-offset — the ONLY warm-dominant vantage (empirical: any high/steep/deep/broadside
// framing reads cool because the cool-fill-lit 9 m walls dominate by frame-area).
//
// ACCEPTANCE (gandalf §4): COMPOSITION is the PRIMARY gate (gandalf's eye on the stills — blue-slab
// dominance killed? warm-foreground hero? felt descent? magenta withheld?). LIGHT is secondary: LDR off
// the 102 floor + warmCool toward warm-dominant (>=1.0). This scorer reads the LIGHT axis only.
//
// iter6 establish baseline (FAIL): LDR 102 / warmCool 0.988 (faintly cool; blue-slab dominance).
// Synty-derivative captures local-only, git-ignored — this reads them, writes only JSON.

import sharp from 'sharp';
import { writeFileSync } from 'fs';
import { join } from 'path';

const TARGET_W = 960;
const DIR = '/Users/admin/Games/reincarnated-godot/harness_logs';
const ITER6_ESTABLISH = { LDR: 102, warmCool: 0.988, SHF: 49.9 };

const FRAMES = [
  { tag: 'establish_01_HERO',           file: 'descent_iter7_establish_01.png' },
  { tag: 'establish_02_ElevatedLookDown', file: 'descent_iter7_establish_02.png' },
  { tag: 'establish_03_GroundIntimate',  file: 'descent_iter7_establish_03.png' },
];

function percentile(sorted, p) {
  const idx = Math.min(sorted.length - 1, Math.max(0, Math.floor(p * sorted.length)));
  return sorted[idx];
}

async function measure(path) {
  const g = sharp(path).resize(TARGET_W, null, { fit: 'inside' }).grayscale();
  const { data: gray, info } = await g.raw().toBuffer({ resolveWithObject: true });
  const w = info.width, h = info.height;
  const lumaSorted = Float64Array.from(gray).slice().sort();
  const p05 = percentile(lumaSorted, 0.05), p50 = percentile(lumaSorted, 0.50);
  const p95 = percentile(lumaSorted, 0.95);
  const ldr = p95 - p05;
  let lo = 0, brt = 0;
  for (let i = 0; i < gray.length; i++) {
    if (gray[i] < 31) lo++;          // < 0.12*255 (SHF shadow)
    if (gray[i] > 180) brt++;        // bright-key mass
  }
  const shf = (100 * lo) / gray.length;
  const { data: rgb, info: ri } = await sharp(path)
    .resize(TARGET_W, null, { fit: 'inside' }).removeAlpha().raw()
    .toBuffer({ resolveWithObject: true });
  let rSum = 0, gSum = 0, bSum = 0;
  for (let i = 0; i < rgb.length; i += 3) { rSum += rgb[i]; gSum += rgb[i + 1]; bSum += rgb[i + 2]; }
  const warmCool = +((rSum + gSum * 0.5) / (bSum + gSum * 0.5)).toFixed(3);
  return {
    LDR: +ldr.toFixed(1), SHF_pct: +shf.toFixed(2),
    bright_pct: +((100 * brt) / gray.length).toFixed(2),
    warmCool, p05, p50, p95, dims: `${w}x${h}`,
  };
}

const out = {
  scored_at: new Date().toISOString(),
  corpus: 'iter7 CAMERA-ONLY establish recompose — descent_iter7_establish_{01,02,03}.png (3 distinct katabasis beats).',
  build: 'drax Round-4 iter7 (reincarnated-godot): _build_establishing_camera recompose ONLY (3 low/short-aim/small-offset warm beats) + harness camera-walk. GREEN chamber rig UNTOUCHED.',
  iter6_establish_baseline: ITER6_ESTABLISH,
  acceptance: 'COMPOSITION primary (gandalf eye on stills). LIGHT secondary: LDR off 102 floor + warmCool >=1.0 (this scorer = LIGHT axis only).',
  frames: [],
};

for (const f of FRAMES) {
  process.stderr.write(`scoring ${f.tag}...\n`);
  const m = await measure(join(DIR, f.file));
  out.frames.push({ ...f, metrics: m });
}

const outPath = join(process.cwd(), 'register2-scores-descent-iter7-establish.json');
writeFileSync(outPath, JSON.stringify(out, null, 2));

console.log('=== iter7 CAMERA-ONLY ESTABLISH RECOMPOSE — LIGHT-AXIS SELF-MEASURE (drax) ===\n');
console.log(`iter6 establish baseline (FAIL): LDR ${ITER6_ESTABLISH.LDR} / warmCool ${ITER6_ESTABLISH.warmCool} (blue-slab dominance)`);
console.log('LIGHT target: LDR off the 102 floor + warmCool >= 1.0 (warm-dominant). COMPOSITION is the primary gate (gandalf eye).\n');
const cols = ['frame', 'LDR', 'dLDR', 'SHF%', 'warmCool', 'dWC', 'bright%'];
const cw = [30, 6, 7, 7, 9, 8, 8];
console.log(cols.map((c, i) => c.padEnd(cw[i])).join(''));
console.log('-'.repeat(cw.reduce((a, b) => a + b, 0)));
for (const f of out.frames) {
  const m = f.metrics;
  const dLDR = +(m.LDR - ITER6_ESTABLISH.LDR).toFixed(1);
  const dWC = +(m.warmCool - ITER6_ESTABLISH.warmCool).toFixed(3);
  console.log([
    f.tag, m.LDR, (dLDR >= 0 ? '+' : '') + dLDR, m.SHF_pct,
    m.warmCool, (dWC >= 0 ? '+' : '') + dWC, m.bright_pct,
  ].map((c, i) => String(c).padEnd(cw[i])).join(''));
}
console.log(`\nwrote ${outPath}`);
