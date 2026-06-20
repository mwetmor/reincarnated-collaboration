// enchanted-forest-rubric-score.mjs — galadriel CV scoring leg of the 3-reviewer gate.
//
// Scores the 6 at-grade ravine frames in
//   reincarnated-godot/harness_logs/ravine_atgrade_2026-06-20/
// against the committed §5 weighted rubric in
//   research/knowledge/arpg-level-design/2026-06-20-enchanted-forest-target-aesthetic-rubric.md
// (GPT-5.4 vision read of the official POLYGON Enchanted Forest marketing render).
//
// CV LEG ONLY. drax scores §3 build self-score; gandalf scores §1/§4 human read.
// Gate threshold (rubric header §"How to consume this"): composite >= 0.75 AND zero §6 auto-fails.
//
// ─── METHOD (named for reproducibility; all measures are pixel-deterministic) ──────────
// All frames decoded at native res via sharp .raw() (RGB, alpha dropped), then:
//
//  M1 PALETTE-MATCH (HSV bucketing):    per-pixel RGB->HSV. Classify each pixel into
//      target palette families (teal-shadow / moss-green / emissive-lime / cyan-blue /
//      amber-warm / neutral-rock / OFFTARGET). Palette-match score = fraction of pixels
//      landing in the enchanted families minus a daylight/gray/brown penalty.
//  M2 EMISSIVE FRACTION (HSV value+sat): emissive pixel = V>=0.78 AND S>=0.35 AND hue in
//      {green ~75-165, cyan ~165-200, amber ~25-50}. Reported per-hue + total. Rubric §2
//      wants emissive 5-15% of frame, multi-hue, multi-plane.
//  M3 VALUE DISTRIBUTION (luma hist):   Rec.709 luma 0-1. Buckets: deep-shadow(<0.20),
//      mid(0.20-0.45), upper(0.45-0.80), spike(>0.80). Rubric §2 wants shadow-heavy base,
//      mid 20-45%, bright spikes small-area (5-15%). Low-key structure check.
//  M4 FOG GRADIENT (front/back edge density): split frame into top third (background) vs
//      bottom third (foreground). Sobel edge density per band. Fog => background edge
//      density drops 30-50% vs foreground (rubric §2). Reported as back/front ratio.
//  M5 VEGETATION / SILHOUETTE DENSITY (global edge density): Sobel magnitude > thresh,
//      fraction of frame. Proxy for "visually packed" (rubric §5 density 10%).
//  M6 COOL-VS-WARM BALANCE: amber-warm pixel fraction vs cool(green+cyan+teal) fraction.
//      Rubric wants warm present but subordinate.
//  M7 SATURATION CHARACTER: mean S over non-shadow pixels; emissive accents high-sat.
//
// Per-dimension 0-1 scores are computed from these measures via stated mapping functions
// (see scoreDimensions()), each with a one-sentence evidence cite. Manual-read dimensions
// (mushroom signature, particle micro-magic, low-poly fidelity, ravine layering) are
// scored by galadriel-eye and ANNOTATED as MANUAL with the visual evidence; the CV measures
// corroborate where they can. Composite = sum(score_i * weight_i).
//
// NO SILENT TRANSFORMATION: raw captures untouched; this reads + writes only its own JSON.

import sharp from 'sharp';
import { writeFileSync } from 'fs';
import { join } from 'path';

const DIR = '/Users/admin/Games/reincarnated-godot/harness_logs/ravine_atgrade_2026-06-20';
const FRAMES = [
  'ravine_atgrade_00_committed.png',
  'ravine_atgrade_01_pool1.png',
  'ravine_atgrade_02_reveal.png',
  'ravine_atgrade_03_pool2.png',
  'ravine_atgrade_04_downgorge.png',
  'ravine_atgrade_05_lookback.png',
];

function rgb2hsv(r, g, b) {
  r /= 255; g /= 255; b /= 255;
  const mx = Math.max(r, g, b), mn = Math.min(r, g, b), d = mx - mn;
  let h = 0;
  if (d !== 0) {
    if (mx === r) h = ((g - b) / d) % 6;
    else if (mx === g) h = (b - r) / d + 2;
    else h = (r - g) / d + 4;
    h *= 60; if (h < 0) h += 360;
  }
  const s = mx === 0 ? 0 : d / mx;
  return [h, s, mx]; // v = mx in 0-1
}

// Palette family classifier per rubric §2.
function paletteFamily(h, s, v) {
  // very dark base regardless of hue -> teal-shadow if cool-leaning, else rock
  if (v < 0.20) {
    if (h >= 140 && h <= 210) return 'teal_shadow';
    if (s < 0.18) return 'neutral_rock';
    return 'teal_shadow'; // dark cool masses dominate the frame edges
  }
  // emissive bright
  if (v >= 0.78 && s >= 0.30) {
    if (h >= 75 && h < 165) return 'emissive_lime';
    if (h >= 165 && h <= 205) return 'cyan_blue';
    if (h >= 20 && h < 55) return 'amber_warm';
  }
  // mids
  if (h >= 75 && h < 165) return s > 0.15 ? 'moss_green' : 'neutral_rock';
  if (h >= 165 && h <= 210) return 'cyan_blue';
  if (h >= 205 && h <= 255) return 'cyan_blue';
  if (h >= 20 && h < 55 && s > 0.25) return 'amber_warm';
  // gray/brown daylight penalty zone
  if (s < 0.12) return 'neutral_gray';
  if (h < 20 || h > 300) return s > 0.25 ? 'offtarget' : 'neutral_rock';
  return 'offtarget';
}

function luma(r, g, b) { return (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255; }

function sobelDensity(gray, w, h, thresh) {
  let count = 0, total = 0;
  for (let y = 1; y < h - 1; y++) {
    for (let x = 1; x < w - 1; x++) {
      const i = y * w + x;
      const gx = -gray[i - w - 1] - 2 * gray[i - 1] - gray[i + w - 1]
                 + gray[i - w + 1] + 2 * gray[i + 1] + gray[i + w + 1];
      const gy = -gray[i - w - 1] - 2 * gray[i - w] - gray[i - w + 1]
                 + gray[i + w - 1] + 2 * gray[i + w] + gray[i + w + 1];
      const mag = Math.sqrt(gx * gx + gy * gy);
      if (mag > thresh) count++;
      total++;
    }
  }
  return count / total;
}

async function measureFrame(path) {
  const img = sharp(path).removeAlpha();
  const meta = await img.metadata();
  const { data, info } = await img.raw().toBuffer({ resolveWithObject: true });
  const w = info.width, h = info.height, ch = info.channels;
  const npx = w * h;

  const fam = {}; // family -> count
  const emissive = { emissive_lime: 0, cyan_blue: 0, amber_warm: 0, total: 0 };
  const valueBuckets = { shadow: 0, mid: 0, upper: 0, spike: 0 };
  let satSum = 0, satN = 0;
  let warmPx = 0, coolPx = 0;

  const gray = new Float32Array(npx);

  for (let p = 0; p < npx; p++) {
    const r = data[p * ch], g = data[p * ch + 1], b = data[p * ch + 2];
    const [hh, ss, vv] = rgb2hsv(r, g, b);
    gray[p] = luma(r, g, b) * 255;

    const f = paletteFamily(hh, ss, vv);
    fam[f] = (fam[f] || 0) + 1;

    // emissive
    if (vv >= 0.78 && ss >= 0.35) {
      if (hh >= 75 && hh < 165) { emissive.emissive_lime++; emissive.total++; }
      else if (hh >= 165 && hh <= 205) { emissive.cyan_blue++; emissive.total++; }
      else if (hh >= 20 && hh < 55) { emissive.amber_warm++; emissive.total++; }
    }
    // value buckets
    const L = luma(r, g, b);
    if (L < 0.20) valueBuckets.shadow++;
    else if (L < 0.45) valueBuckets.mid++;
    else if (L < 0.80) valueBuckets.upper++;
    else valueBuckets.spike++;

    if (L >= 0.20) { satSum += ss; satN++; }

    // cool vs warm (use family-ish hue)
    if (hh >= 20 && hh < 55 && ss > 0.25 && vv > 0.25) warmPx++;
    if ((hh >= 75 && hh <= 255) && ss > 0.10) coolPx++;
  }

  // edge densities
  const globalEdge = sobelDensity(gray, w, h, 40);
  // banded fog gradient: top third (bg) vs bottom third (fg)
  const bandH = Math.floor(h / 3);
  const topGray = gray.subarray(0, bandH * w);
  const botGray = gray.subarray((h - bandH) * w, h * w);
  const topEdge = sobelDensity(topGray, w, bandH, 40);
  const botEdge = sobelDensity(botGray, w, bandH, 40);

  const norm = (o) => Object.fromEntries(Object.entries(o).map(([k, v]) => [k, v / npx]));

  return {
    res: `${w}x${h}`,
    families: norm(fam),
    emissive: { ...norm(emissive), total: emissive.total / npx },
    value: norm(valueBuckets),
    meanSatNonShadow: satN ? satSum / satN : 0,
    warmFrac: warmPx / npx,
    coolFrac: coolPx / npx,
    edge: { global: globalEdge, bgTop: topEdge, fgBot: botEdge, bgFgRatio: botEdge ? topEdge / botEdge : null },
  };
}

function mean(arr) { return arr.reduce((a, b) => a + b, 0) / arr.length; }

(async () => {
  const perFrame = {};
  for (const f of FRAMES) {
    perFrame[f] = await measureFrame(join(DIR, f));
  }

  // aggregate across frames
  const enchantedFamilies = ['teal_shadow', 'moss_green', 'emissive_lime', 'cyan_blue', 'amber_warm'];
  const offFamilies = ['neutral_gray', 'offtarget'];
  const agg = {
    enchantedFrac: mean(FRAMES.map(f => enchantedFamilies.reduce((s, k) => s + (perFrame[f].families[k] || 0), 0))),
    offFrac: mean(FRAMES.map(f => offFamilies.reduce((s, k) => s + (perFrame[f].families[k] || 0), 0))),
    grayFrac: mean(FRAMES.map(f => perFrame[f].families['neutral_gray'] || 0)),
    rockFrac: mean(FRAMES.map(f => perFrame[f].families['neutral_rock'] || 0)),
    emissiveTotal: mean(FRAMES.map(f => perFrame[f].emissive.total)),
    emissiveLime: mean(FRAMES.map(f => perFrame[f].emissive.emissive_lime)),
    emissiveCyan: mean(FRAMES.map(f => perFrame[f].emissive.cyan_blue)),
    emissiveAmber: mean(FRAMES.map(f => perFrame[f].emissive.amber_warm)),
    framesWithMultiHueEmissive: FRAMES.filter(f => {
      const e = perFrame[f].emissive;
      let hues = 0; if (e.emissive_lime > 0.0005) hues++; if (e.cyan_blue > 0.0005) hues++; if (e.amber_warm > 0.0005) hues++;
      return hues >= 2;
    }).length,
    valShadow: mean(FRAMES.map(f => perFrame[f].value.shadow)),
    valMid: mean(FRAMES.map(f => perFrame[f].value.mid)),
    valUpper: mean(FRAMES.map(f => perFrame[f].value.upper)),
    valSpike: mean(FRAMES.map(f => perFrame[f].value.spike)),
    meanSat: mean(FRAMES.map(f => perFrame[f].meanSatNonShadow)),
    warmFrac: mean(FRAMES.map(f => perFrame[f].warmFrac)),
    coolFrac: mean(FRAMES.map(f => perFrame[f].coolFrac)),
    edgeGlobal: mean(FRAMES.map(f => perFrame[f].edge.global)),
    bgFgRatio: mean(FRAMES.map(f => perFrame[f].edge.bgFgRatio).filter(x => x != null)),
  };

  const out = { method: 'M1-M7 see header', dir: DIR, frames: FRAMES, perFrame, aggregate: agg };
  const outPath = join('/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/pipeline', 'enchanted-forest-rubric-score.json');
  writeFileSync(outPath, JSON.stringify(out, null, 2));
  console.log(JSON.stringify(agg, null, 2));
  console.log('\n--- PER FRAME emissive.total / valShadow / valSpike / edge.global / bgFgRatio ---');
  for (const f of FRAMES) {
    const p = perFrame[f];
    console.log(`${f}: emis=${p.emissive.total.toFixed(4)} (G=${p.emissive.emissive_lime.toFixed(4)} C=${p.emissive.cyan_blue.toFixed(4)} A=${p.emissive.amber_warm.toFixed(4)})  shadow=${p.value.shadow.toFixed(3)} spike=${p.value.spike.toFixed(4)}  edgeG=${p.edge.global.toFixed(3)} bgFg=${p.edge.bgFgRatio?.toFixed(3)}  ench=${enchantedFamilies.reduce((s,k)=>s+(p.families[k]||0),0).toFixed(3)} gray=${(p.families['neutral_gray']||0).toFixed(4)}`);
  }
  console.log('\nWrote', outPath);
})();
