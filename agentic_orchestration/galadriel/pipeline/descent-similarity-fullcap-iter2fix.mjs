// descent-similarity-vs-reference.mjs — dark-fantasy visual-similarity vs the Synty reference art.
//
// JOB (2) of the galadriel descent brief: an OBJECTIVE similarity read of the connected
// scene's frames against the reference dark-fantasy map art, AND ranked residual-gap
// callouts (most-off-reference axis first). Matt's target: the scene should "look like"
// the reference = DARK-with-vivid-COLORED-LIGHT (luminous green atmosphere rising from
// the ground, golden brazier/lantern points that POP, dense gothic dressing, deep shadows).
//
// METHOD (Discipline #4 right-tool — one instrument per question axis):
//   AXIS 1  color/atmosphere-hue   -> HSV-hue HISTOGRAM cosine similarity (36-bin H, value-
//                                     and saturation-weighted) demo-frame vs reference-frame.
//                                     Answers: does the scene sit in the same hue family
//                                     (green-dominant atmosphere + warm accents)?
//   AXIS 2  light-point density    -> "motivated bright point" fraction: bright (V>150) +
//                                     hue-dominant (warm OR green) pixels. Answers: does the
//                                     scene have the reference's density of golden/green light
//                                     points popping out of the dark?
//   AXIS 3  dressing density       -> Canny-style edge density (Laplacian-threshold proxy):
//                                     dense gothic dressing = high edge energy. demo vs ref.
//   AXIS 4  contrast/shadow depth  -> value-channel p95-p05 spread + shadow fraction (V<31).
//                                     Answers: deep shadows + strong lit-vs-dark contrast?
//
// Each axis -> a ratio/cosine vs the reference MEAN, and a ranked residual gap.
// Reference set is the Matt-named maps art (license-clean: Synty's own marketing/idea art,
// shipped IN the purchased pack — internal benchmark use). raw images untouched.

import sharp from 'sharp';
import { readdirSync, writeFileSync } from 'fs';
import { join } from 'path';

const TARGET_W = 960;
const DEMO_DIR = "/Users/admin/Games/reincarnated-godot/harness_logs/iter2fix_fullcap";
const REF_DIR = '/Users/admin/Games/reincarnated-godot/Assets/Synty/polygon-dark-fantasy-01/modular_asset_idea_pictures/maps';

// The reference frames Matt named (8.36.17 the primary green-atmosphere target) + the
// other maps frames for a robust reference centroid. All are the green/red dark-fantasy
// crypt-cathedral register the descent targets.
const REF_FILES = readdirSync(REF_DIR).filter(f => f.endsWith('.png'));

// Demo frames: one representative peak frame per zone (the mid-window grab) + the
// establishing primary (the scene's "wow"). One per view so each is a fair single read.
const DEMO_FRAMES = [
  { tag: 'zone0_threshold',   file: 'gal_descent_zone0_threshold_04.png' },
  { tag: 'zone1_arcane',      file: 'gal_descent_zone1_arcane_04.png' },
  { tag: 'zone2_warhall',     file: 'gal_descent_zone2_warhall_04.png' },
  { tag: 'zone3_oubliette',   file: 'gal_descent_zone3_oubliette_04.png' },
  { tag: 'zone4_antechamber', file: 'gal_descent_zone4_antechamber_04.png' },
  { tag: 'zone5_sanctum',     file: 'gal_descent_zone5_sanctum_04.png' },
  { tag: 'establish_primary', file: 'gal_descent_establish_primary_04.png' },
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
  return [h, s, max]; // max = V in 0..1
}

const HUE_BINS = 36;
function laplacianEdgeDensity(gray, w, h, thresh = 18) {
  let cnt = 0, n = 0;
  for (let y = 1; y < h - 1; y++) {
    for (let x = 1; x < w - 1; x++) {
      const i = y * w + x;
      const lap = Math.abs(-4 * gray[i] + gray[i - 1] + gray[i + 1] + gray[i - w] + gray[i + w]);
      if (lap > thresh) cnt++;
      n++;
    }
  }
  return (100 * cnt) / n; // % of pixels that are edges
}

async function profile(path) {
  const { data: rgb, info } = await sharp(path)
    .resize(TARGET_W, null, { fit: 'inside' }).removeAlpha().raw()
    .toBuffer({ resolveWithObject: true });
  const w = info.width, h = info.height, n = w * h;
  const hist = new Float64Array(HUE_BINS);
  const gray = new Float64Array(n);
  const valArr = new Float64Array(n);
  let warmPts = 0, greenPts = 0, brightPts = 0;
  let satSum = 0;
  for (let i = 0, p = 0; i < rgb.length; i += 3, p++) {
    const r = rgb[i], g = rgb[i + 1], b = rgb[i + 2];
    const [hue, s, v] = rgb2hsv(r, g, b);
    gray[p] = 0.299 * r + 0.587 * g + 0.114 * b;
    valArr[p] = v * 255;
    satSum += s;
    // hue histogram weighted by S*V (so dark/grey pixels don't dominate the hue read)
    const bin = Math.min(HUE_BINS - 1, Math.floor(hue / (360 / HUE_BINS)));
    hist[bin] += s * v;
    // motivated light points
    if (v * 255 > 150) {
      brightPts++;
      if (r > g + 25 && r > b + 25) warmPts++;
      if (g > r + 20 && g > b + 20) greenPts++;
    }
  }
  // normalize hue histogram
  let hs = 0; for (let i = 0; i < HUE_BINS; i++) hs += hist[i];
  if (hs > 0) for (let i = 0; i < HUE_BINS; i++) hist[i] /= hs;
  const vSorted = valArr.slice().sort();
  const ldrVal = vSorted[Math.floor(0.95 * n)] - vSorted[Math.floor(0.05 * n)];
  let shadow = 0; for (let p = 0; p < n; p++) if (valArr[p] < 31) shadow++;
  const edge = laplacianEdgeDensity(gray, w, h);
  return {
    hist,
    warm_pct: (100 * warmPts) / n,
    green_pct: (100 * greenPts) / n,
    bright_pct: (100 * brightPts) / n,
    sat_mean: satSum / n,
    ldr_val: ldrVal,
    shadow_pct: (100 * shadow) / n,
    edge_pct: edge,
  };
}

function cosine(a, b) {
  let dot = 0, na = 0, nb = 0;
  for (let i = 0; i < a.length; i++) { dot += a[i] * b[i]; na += a[i] * a[i]; nb += b[i] * b[i]; }
  return (na === 0 || nb === 0) ? 0 : dot / (Math.sqrt(na) * Math.sqrt(nb));
}

// ---- build reference centroid ----
const refProfiles = [];
for (const f of REF_FILES) { process.stderr.write(`ref ${f}...\n`); refProfiles.push({ f, ...(await profile(join(REF_DIR, f))) }); }
const refHist = new Float64Array(HUE_BINS);
for (const r of refProfiles) for (let i = 0; i < HUE_BINS; i++) refHist[i] += r.hist[i] / refProfiles.length;
const refMean = k => refProfiles.reduce((a, r) => a + r[k], 0) / refProfiles.length;
const refStats = {
  warm_pct: refMean('warm_pct'), green_pct: refMean('green_pct'), bright_pct: refMean('bright_pct'),
  sat_mean: refMean('sat_mean'), ldr_val: refMean('ldr_val'), shadow_pct: refMean('shadow_pct'), edge_pct: refMean('edge_pct'),
};

// ---- score each demo frame ----
const demoScored = [];
for (const d of DEMO_FRAMES) {
  process.stderr.write(`demo ${d.tag}...\n`);
  const p = await profile(join(DEMO_DIR, d.file));
  const hueCos = cosine(p.hist, refHist);
  demoScored.push({
    tag: d.tag, file: d.file, hueCos: +hueCos.toFixed(4),
    warm_pct: +p.warm_pct.toFixed(3), green_pct: +p.green_pct.toFixed(3), bright_pct: +p.bright_pct.toFixed(3),
    sat_mean: +p.sat_mean.toFixed(3), ldr_val: +p.ldr_val.toFixed(1), shadow_pct: +p.shadow_pct.toFixed(2), edge_pct: +p.edge_pct.toFixed(3),
    // per-axis ratio vs reference (1.0 = matches reference; <1 below, >1 above)
    r_lightpoint: +(((p.warm_pct + p.green_pct)) / (refStats.warm_pct + refStats.green_pct)).toFixed(3),
    r_dressing: +(p.edge_pct / refStats.edge_pct).toFixed(3),
    r_contrast: +(p.ldr_val / refStats.ldr_val).toFixed(3),
    r_shadow: +(p.shadow_pct / Math.max(0.01, refStats.shadow_pct)).toFixed(3),
  });
}

// scene-level means
const sMean = k => demoScored.reduce((a, d) => a + d[k], 0) / demoScored.length;
const scene = {
  hueCos: +sMean('hueCos').toFixed(4),
  r_lightpoint: +sMean('r_lightpoint').toFixed(3),
  r_dressing: +sMean('r_dressing').toFixed(3),
  r_contrast: +sMean('r_contrast').toFixed(3),
  warm_pct: +sMean('warm_pct').toFixed(3), green_pct: +sMean('green_pct').toFixed(3),
  sat_mean: +sMean('sat_mean').toFixed(3), shadow_pct: +sMean('shadow_pct').toFixed(2), edge_pct: +sMean('edge_pct').toFixed(3),
};

const out = {
  scored_at: new Date().toISOString(),
  reference_set: { dir: REF_DIR, files: REF_FILES, n: refProfiles.length },
  reference_stats: Object.fromEntries(Object.entries(refStats).map(([k, v]) => [k, +v.toFixed(3)])),
  demo_frames: demoScored, scene_means: scene,
  per_ref_profiles: refProfiles.map(r => ({ f: r.f, warm_pct: +r.warm_pct.toFixed(3), green_pct: +r.green_pct.toFixed(3), sat_mean: +r.sat_mean.toFixed(3), ldr_val: +r.ldr_val.toFixed(1), shadow_pct: +r.shadow_pct.toFixed(2), edge_pct: +r.edge_pct.toFixed(3) })),
};
writeFileSync(join(process.cwd(), 'descent-similarity-fullcap-iter2fix.json'), JSON.stringify(out, null, 2));

console.log('=== DARK-FANTASY VISUAL-SIMILARITY vs REFERENCE ART ===\n');
console.log(`reference set: ${refProfiles.length} maps frames. Target = DARK + vivid COLORED LIGHT (green atmosphere, golden points, dense dressing, deep shadows).\n`);
console.log('REFERENCE centroid:  warm%=' + refStats.warm_pct.toFixed(3) + '  green%=' + refStats.green_pct.toFixed(3) + '  sat=' + refStats.sat_mean.toFixed(3) + '  LDRval=' + refStats.ldr_val.toFixed(1) + '  shadow%=' + refStats.shadow_pct.toFixed(2) + '  edge%=' + refStats.edge_pct.toFixed(3) + '\n');
const cols = ['demo frame', 'hueCos', 'warm%', 'green%', 'sat', 'LDRval', 'shadow%', 'edge%', 'rLight', 'rDress', 'rContr'];
const w = [18, 8, 7, 8, 7, 8, 9, 8, 8, 8, 8];
console.log(cols.map((c, i) => c.padEnd(w[i])).join(''));
console.log('-'.repeat(w.reduce((a, b) => a + b, 0)));
for (const d of demoScored) {
  console.log([d.tag, d.hueCos, d.warm_pct, d.green_pct, d.sat_mean, d.ldr_val, d.shadow_pct, d.edge_pct, d.r_lightpoint, d.r_dressing, d.r_contrast].map((c, i) => String(c).padEnd(w[i])).join(''));
}
console.log('-'.repeat(w.reduce((a, b) => a + b, 0)));
console.log(['SCENE MEAN', scene.hueCos, scene.warm_pct, scene.green_pct, scene.sat_mean, '-', scene.shadow_pct, scene.edge_pct, scene.r_lightpoint, scene.r_dressing, scene.r_contrast].map((c, i) => String(c).padEnd(w[i])).join(''));

console.log('\n=== RANKED RESIDUAL GAPS (most-off-reference first; ratio 1.0 = matches ref) ===');
const gaps = [
  { axis: 'light-point density (golden/green points popping)', ratio: scene.r_lightpoint },
  { axis: 'dressing density (gothic clutter / edge energy)', ratio: scene.r_dressing },
  { axis: 'contrast / shadow depth (value LDR vs ref)', ratio: scene.r_contrast },
  { axis: 'color/atmosphere hue (cosine vs ref hue family)', ratio: scene.hueCos },
];
gaps.sort((a, b) => Math.abs(1 - a.ratio) - Math.abs(1 - b.ratio));   // closest-to-1 last? no: most-off first
gaps.sort((a, b) => (a.axis.includes('hue') ? (1 - a.ratio) : Math.abs(1 - a.ratio)) < (b.axis.includes('hue') ? (1 - b.ratio) : Math.abs(1 - b.ratio)) ? 1 : -1);
for (const g of gaps) {
  const off = g.axis.includes('hue') ? (1 - g.ratio) : Math.abs(1 - g.ratio);
  const dir = g.ratio < 1 ? 'BELOW ref' : (g.ratio > 1 ? 'ABOVE ref' : 'matches');
  console.log(`  ${(off * 100).toFixed(0).padStart(3)}% off | ${g.axis.padEnd(50)} ratio=${g.ratio.toFixed(3)} (${dir})`);
}
console.log('\nwrote descent-similarity-vs-reference.json');
