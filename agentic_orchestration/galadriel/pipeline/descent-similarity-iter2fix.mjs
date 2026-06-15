// descent-similarity-iter2fix.mjs — iter2fix re-score of dark-fantasy similarity vs the
// Synty reference art, with EXACT per-frame deltas vs the iter1 baseline.
//
// SAME 4-axis method + SAME reference centroid as descent-similarity-vs-reference.mjs
// (the iter1 instrument — byte-identical profile() + cosine + reference set). The ONLY
// change: DEMO_FRAMES point at the 3 iter2fix static frames AND the matched iter1 frames,
// so the comparison is APPLES-TO-APPLES per VIEW (establish_primary / zone0 / zone2):
//   - iter1 frames: gal_descent_<view>_04.png (my prior harness peak frame)
//   - iter2fix frames: descent_iter2fix_<view>.png (drax's corrected-scene static frame)
// Per-frame delta is the rigorous read (same camera, same view). Scene-mean is NOT
// directly comparable (iter1 mean was over 7 views; iter2fix has 3) — reported with caveat.
//
// No silent transformation: raw captures preserved; reads them, writes nothing to them.

import sharp from 'sharp';
import { readdirSync, writeFileSync } from 'fs';
import { join } from 'path';

const TARGET_W = 960;
const DIR = '/Users/admin/Games/reincarnated-godot/harness_logs';
const REF_DIR = '/Users/admin/Games/reincarnated-godot/Assets/Synty/polygon-dark-fantasy-01/modular_asset_idea_pictures/maps';
const REF_FILES = readdirSync(REF_DIR).filter(f => f.endsWith('.png'));

// matched pairs: same VIEW, iter1 vs iter2fix
const PAIRS = [
  { view: 'establish_primary', iter1: 'gal_descent_establish_primary_04.png', iter2fix: 'descent_iter2fix_establish_primary.png' },
  { view: 'zone0',             iter1: 'gal_descent_zone0_threshold_04.png',   iter2fix: 'descent_iter2fix_zone0.png' },
  { view: 'zone2',             iter1: 'gal_descent_zone2_warhall_04.png',      iter2fix: 'descent_iter2fix_zone2.png' },
];

function rgb2hsv(r, g, b) {
  r /= 255; g /= 255; b /= 255;
  const max = Math.max(r, g, b), min = Math.min(r, g, b), d = max - min;
  let h = 0;
  if (d !== 0) {
    if (max === r) h = ((g - b) / d) % 6;
    else if (max === g) h = (b - r) / d + 2;
    else h = (r - g) / d + 4;
    h *= 60; if (h < 0) h += 360;
  }
  const s = max === 0 ? 0 : d / max;
  return [h, s, max];
}
const HUE_BINS = 36;
function laplacianEdgeDensity(gray, w, h, thresh = 18) {
  let cnt = 0, n = 0;
  for (let y = 1; y < h - 1; y++) for (let x = 1; x < w - 1; x++) {
    const i = y * w + x;
    const lap = Math.abs(-4 * gray[i] + gray[i - 1] + gray[i + 1] + gray[i - w] + gray[i + w]);
    if (lap > thresh) cnt++; n++;
  }
  return (100 * cnt) / n;
}
async function profile(path) {
  const { data: rgb, info } = await sharp(path)
    .resize(TARGET_W, null, { fit: 'inside' }).removeAlpha().raw()
    .toBuffer({ resolveWithObject: true });
  const w = info.width, h = info.height, n = w * h;
  const hist = new Float64Array(HUE_BINS);
  const gray = new Float64Array(n);
  const valArr = new Float64Array(n);
  let warmPts = 0, greenPts = 0, brightPts = 0, satSum = 0;
  for (let i = 0, p = 0; i < rgb.length; i += 3, p++) {
    const r = rgb[i], g = rgb[i + 1], b = rgb[i + 2];
    const [hue, s, v] = rgb2hsv(r, g, b);
    gray[p] = 0.299 * r + 0.587 * g + 0.114 * b;
    valArr[p] = v * 255;
    satSum += s;
    const bin = Math.min(HUE_BINS - 1, Math.floor(hue / (360 / HUE_BINS)));
    hist[bin] += s * v;
    if (v * 255 > 150) {
      brightPts++;
      if (r > g + 25 && r > b + 25) warmPts++;
      if (g > r + 20 && g > b + 20) greenPts++;
    }
  }
  let hs = 0; for (let i = 0; i < HUE_BINS; i++) hs += hist[i];
  if (hs > 0) for (let i = 0; i < HUE_BINS; i++) hist[i] /= hs;
  const vSorted = valArr.slice().sort();
  const ldrVal = vSorted[Math.floor(0.95 * n)] - vSorted[Math.floor(0.05 * n)];
  let shadow = 0; for (let p = 0; p < n; p++) if (valArr[p] < 31) shadow++;
  const edge = laplacianEdgeDensity(gray, w, h);
  return {
    hist, warm_pct: (100 * warmPts) / n, green_pct: (100 * greenPts) / n,
    bright_pct: (100 * brightPts) / n, sat_mean: satSum / n,
    ldr_val: ldrVal, shadow_pct: (100 * shadow) / n, edge_pct: edge,
  };
}
function cosine(a, b) {
  let dot = 0, na = 0, nb = 0;
  for (let i = 0; i < a.length; i++) { dot += a[i] * b[i]; na += a[i] * a[i]; nb += b[i] * b[i]; }
  return (na === 0 || nb === 0) ? 0 : dot / (Math.sqrt(na) * Math.sqrt(nb));
}

// reference centroid (identical to iter1 instrument)
const refProfiles = [];
for (const f of REF_FILES) { process.stderr.write(`ref ${f}...\n`); refProfiles.push({ f, ...(await profile(join(REF_DIR, f))) }); }
const refHist = new Float64Array(HUE_BINS);
for (const r of refProfiles) for (let i = 0; i < HUE_BINS; i++) refHist[i] += r.hist[i] / refProfiles.length;
const refMean = k => refProfiles.reduce((a, r) => a + r[k], 0) / refProfiles.length;
const refStats = {
  warm_pct: refMean('warm_pct'), green_pct: refMean('green_pct'), bright_pct: refMean('bright_pct'),
  sat_mean: refMean('sat_mean'), ldr_val: refMean('ldr_val'), shadow_pct: refMean('shadow_pct'), edge_pct: refMean('edge_pct'),
};
const warmGreenRef = refStats.warm_pct + refStats.green_pct;

async function scoreFrame(path) {
  const p = await profile(path);
  return {
    hueCos: +cosine(p.hist, refHist).toFixed(4),
    warm_pct: +p.warm_pct.toFixed(3), green_pct: +p.green_pct.toFixed(3), bright_pct: +p.bright_pct.toFixed(3),
    sat_mean: +p.sat_mean.toFixed(3), ldr_val: +p.ldr_val.toFixed(1), shadow_pct: +p.shadow_pct.toFixed(2), edge_pct: +p.edge_pct.toFixed(3),
    r_lightpoint: +(((p.warm_pct + p.green_pct)) / warmGreenRef).toFixed(3),
    r_dressing: +(p.edge_pct / refStats.edge_pct).toFixed(3),
    r_contrast: +(p.ldr_val / refStats.ldr_val).toFixed(3),
  };
}

const rows = [];
for (const pr of PAIRS) {
  process.stderr.write(`pair ${pr.view}...\n`);
  const a = await scoreFrame(join(DIR, pr.iter1));
  const b = await scoreFrame(join(DIR, pr.iter2fix));
  rows.push({ view: pr.view, iter1: a, iter2fix: b });
}

const mean = (arr, sel) => arr.reduce((s, r) => s + sel(r), 0) / arr.length;
const sceneIter1 = {
  hueCos: +mean(rows, r => r.iter1.hueCos).toFixed(4),
  warm_pct: +mean(rows, r => r.iter1.warm_pct).toFixed(3),
  r_lightpoint: +mean(rows, r => r.iter1.r_lightpoint).toFixed(3),
  r_dressing: +mean(rows, r => r.iter1.r_dressing).toFixed(3),
  r_contrast: +mean(rows, r => r.iter1.r_contrast).toFixed(3),
};
const sceneIter2fix = {
  hueCos: +mean(rows, r => r.iter2fix.hueCos).toFixed(4),
  warm_pct: +mean(rows, r => r.iter2fix.warm_pct).toFixed(3),
  r_lightpoint: +mean(rows, r => r.iter2fix.r_lightpoint).toFixed(3),
  r_dressing: +mean(rows, r => r.iter2fix.r_dressing).toFixed(3),
  r_contrast: +mean(rows, r => r.iter2fix.r_contrast).toFixed(3),
};

const out = {
  scored_at: new Date().toISOString(),
  note: 'iter2fix vs iter1 — APPLES-TO-APPLES per VIEW (3 matched views). Scene-mean over these 3 views ONLY (NOT comparable to the iter1 7-view scene-mean in descent-similarity-vs-reference.json).',
  reference_set: { dir: REF_DIR, files: REF_FILES, n: refProfiles.length },
  reference_stats: Object.fromEntries(Object.entries(refStats).map(([k, v]) => [k, +v.toFixed(3)])),
  pairs: rows,
  scene_mean_3view: { iter1: sceneIter1, iter2fix: sceneIter2fix },
};
writeFileSync(join(process.cwd(), 'descent-similarity-iter2fix.json'), JSON.stringify(out, null, 2));

console.log('=== iter2fix SIMILARITY vs REFERENCE — per-view delta vs iter1 ===\n');
console.log('REFERENCE centroid: warm%=' + refStats.warm_pct.toFixed(2) + '  green%=' + refStats.green_pct.toFixed(2) + '  edge%=' + refStats.edge_pct.toFixed(2) + '  LDRval=' + refStats.ldr_val.toFixed(1) + '\n');
const cols = ['view / iter', 'hueCos', 'warm%', 'green%', 'edge%', 'rLight', 'rDress', 'rContr'];
const w = [22, 9, 8, 8, 8, 9, 9, 9];
console.log(cols.map((c, i) => c.padEnd(w[i])).join(''));
console.log('-'.repeat(w.reduce((a, b) => a + b, 0)));
for (const r of rows) {
  const a = r.iter1, b = r.iter2fix;
  console.log([r.view + ' iter1', a.hueCos, a.warm_pct, a.green_pct, a.edge_pct, a.r_lightpoint, a.r_dressing, a.r_contrast].map((c, i) => String(c).padEnd(w[i])).join(''));
  console.log([r.view + ' iter2fix', b.hueCos, b.warm_pct, b.green_pct, b.edge_pct, b.r_lightpoint, b.r_dressing, b.r_contrast].map((c, i) => String(c).padEnd(w[i])).join(''));
  const d = (x, y) => (y - x >= 0 ? '+' : '') + (y - x).toFixed(3);
  console.log(['  Δ', d(a.hueCos, b.hueCos), d(a.warm_pct, b.warm_pct), d(a.green_pct, b.green_pct), d(a.edge_pct, b.edge_pct), d(a.r_lightpoint, b.r_lightpoint), d(a.r_dressing, b.r_dressing), d(a.r_contrast, b.r_contrast)].map((c, i) => String(c).padEnd(w[i])).join(''));
  console.log('-'.repeat(w.reduce((a, b) => a + b, 0)));
}
console.log('\n3-VIEW SCENE MEAN (these 3 views only):');
console.log('  iter1   : hueCos=' + sceneIter1.hueCos + '  warm%=' + sceneIter1.warm_pct + '  rLight=' + sceneIter1.r_lightpoint + '  rDress=' + sceneIter1.r_dressing + '  rContr=' + sceneIter1.r_contrast);
console.log('  iter2fix: hueCos=' + sceneIter2fix.hueCos + '  warm%=' + sceneIter2fix.warm_pct + '  rLight=' + sceneIter2fix.r_lightpoint + '  rDress=' + sceneIter2fix.r_dressing + '  rContr=' + sceneIter2fix.r_contrast);
console.log('\nwrote descent-similarity-iter2fix.json');
