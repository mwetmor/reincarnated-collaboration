// enchanted-forest-rubric-score-carved-r1.mjs — galadriel CV scoring leg, CARVED (Revision 1) re-score.
//
// Re-scores the CARVED + Revision-1 ravine frames in
//   reincarnated-godot/harness_logs/ravine_carved_2026-06-21/
// against the same committed §5 weighted rubric used for the at-grade score
//   research/knowledge/arpg-level-design/2026-06-20-enchanted-forest-target-aesthetic-rubric.md
//
// METHOD identical to enchanted-forest-rubric-score.mjs (M1-M7); see that file's header.
// ADDITIONS for the R1 register-survival question:
//   - per-frame VALUE MEDIAN (Rec.709 luma, 0-1) — confirm gameplay frames stay in the ~5-20% dark-first band
//   - per-frame EMISSIVE p99 (luma of emissive-classified pixels) — confirm emissive hotspots remain the brightest elements
//   - per-frame brightest-element check: median value vs p99-of-all-pixels (lit-from-within delta)
//   - GAMEPLAY vs DIAGNOSTIC frame partition (diagnostics camera-aimed UP the shaft; excluded from gameplay composite)
//
// NO SILENT TRANSFORMATION: raw captures untouched; reads + writes only its own JSON.

import sharp from 'sharp';
import { writeFileSync } from 'fs';
import { join } from 'path';

const DIR = '/Users/admin/Games/reincarnated-godot/harness_logs/ravine_carved_2026-06-21';

// Gameplay/ARPG framings — these drive the composite + §6 + register-survival verdict.
const GAMEPLAY = [
  'ravine_carved_00_committed.png',
  'ravine_carved_01_pool1.png',
  'ravine_carved_02_reveal.png',
  'ravine_carved_03_pool2.png',
  'ravine_carved_04_downgorge.png',
  'ravine_carved_05_lookback.png',
  'ravine_carved_10_carve_floor_downgorge.png',
];

// Look-UP-the-shaft diagnostics — NOT gameplay framings. Scored separately, do NOT enter composite.
const DIAGNOSTIC = [
  'ravine_carved_06_carve_up_pool1.png',
  'ravine_carved_07_carve_up_pool2.png',
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
  return [h, s, mx];
}

function paletteFamily(h, s, v) {
  if (v < 0.20) {
    if (h >= 140 && h <= 210) return 'teal_shadow';
    if (s < 0.18) return 'neutral_rock';
    return 'teal_shadow';
  }
  if (v >= 0.78 && s >= 0.30) {
    if (h >= 75 && h < 165) return 'emissive_lime';
    if (h >= 165 && h <= 205) return 'cyan_blue';
    if (h >= 20 && h < 55) return 'amber_warm';
  }
  if (h >= 75 && h < 165) return s > 0.15 ? 'moss_green' : 'neutral_rock';
  if (h >= 165 && h <= 210) return 'cyan_blue';
  if (h >= 205 && h <= 255) return 'cyan_blue';
  if (h >= 20 && h < 55 && s > 0.25) return 'amber_warm';
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

function percentile(sortedArr, p) {
  if (sortedArr.length === 0) return null;
  const idx = Math.min(sortedArr.length - 1, Math.floor(p * sortedArr.length));
  return sortedArr[idx];
}

async function measureFrame(path) {
  const img = sharp(path).removeAlpha();
  const { data, info } = await img.raw().toBuffer({ resolveWithObject: true });
  const w = info.width, h = info.height, ch = info.channels;
  const npx = w * h;

  const fam = {};
  const emissive = { emissive_lime: 0, cyan_blue: 0, amber_warm: 0, total: 0 };
  const valueBuckets = { shadow: 0, mid: 0, upper: 0, spike: 0 };
  let satSum = 0, satN = 0;
  let warmPx = 0, coolPx = 0;

  const gray = new Float32Array(npx);
  const allLuma = new Float32Array(npx);
  const emissiveLuma = []; // luma of emissive-classified pixels

  for (let p = 0; p < npx; p++) {
    const r = data[p * ch], g = data[p * ch + 1], b = data[p * ch + 2];
    const [hh, ss, vv] = rgb2hsv(r, g, b);
    const L = luma(r, g, b);
    gray[p] = L * 255;
    allLuma[p] = L;

    const f = paletteFamily(hh, ss, vv);
    fam[f] = (fam[f] || 0) + 1;

    if (vv >= 0.78 && ss >= 0.35) {
      let isEmis = false;
      if (hh >= 75 && hh < 165) { emissive.emissive_lime++; isEmis = true; }
      else if (hh >= 165 && hh <= 205) { emissive.cyan_blue++; isEmis = true; }
      else if (hh >= 20 && hh < 55) { emissive.amber_warm++; isEmis = true; }
      if (isEmis) { emissive.total++; emissiveLuma.push(L); }
    }

    if (L < 0.20) valueBuckets.shadow++;
    else if (L < 0.45) valueBuckets.mid++;
    else if (L < 0.80) valueBuckets.upper++;
    else valueBuckets.spike++;

    if (L >= 0.20) { satSum += ss; satN++; }

    if (hh >= 20 && hh < 55 && ss > 0.25 && vv > 0.25) warmPx++;
    if ((hh >= 75 && hh <= 255) && ss > 0.10) coolPx++;
  }

  const globalEdge = sobelDensity(gray, w, h, 40);
  const bandH = Math.floor(h / 3);
  const topGray = gray.subarray(0, bandH * w);
  const botGray = gray.subarray((h - bandH) * w, h * w);
  const topEdge = sobelDensity(topGray, w, bandH, 40);
  const botEdge = sobelDensity(botGray, w, bandH, 40);

  // value median + percentiles
  const sortedAll = Float32Array.from(allLuma).sort();
  const valueMedian = percentile(sortedAll, 0.50);
  const valueP90 = percentile(sortedAll, 0.90);
  const valueP99 = percentile(sortedAll, 0.99);
  // emissive p99 (brightest emissive pixels)
  const sortedEmis = emissiveLuma.slice().sort((a, b) => a - b);
  const emissiveP99 = sortedEmis.length ? percentile(sortedEmis, 0.99) : null;
  const emissiveP50 = sortedEmis.length ? percentile(sortedEmis, 0.50) : null;

  const norm = (o) => Object.fromEntries(Object.entries(o).map(([k, v]) => [k, v / npx]));

  return {
    res: `${w}x${h}`,
    families: norm(fam),
    emissive: { ...norm(emissive), total: emissive.total / npx },
    value: norm(valueBuckets),
    valueMedian, valueP90, valueP99,
    emissiveP50, emissiveP99,
    litFromWithinDelta: emissiveP99 != null ? (emissiveP99 - valueMedian) : null,
    meanSatNonShadow: satN ? satSum / satN : 0,
    warmFrac: warmPx / npx,
    coolFrac: coolPx / npx,
    edge: { global: globalEdge, bgTop: topEdge, fgBot: botEdge, bgFgRatio: botEdge ? topEdge / botEdge : null },
  };
}

function mean(arr) { return arr.reduce((a, b) => a + b, 0) / arr.length; }

const ENCH = ['teal_shadow', 'moss_green', 'emissive_lime', 'cyan_blue', 'amber_warm'];
const OFF = ['neutral_gray', 'offtarget'];

function aggregate(frames, perFrame) {
  return {
    enchantedFrac: mean(frames.map(f => ENCH.reduce((s, k) => s + (perFrame[f].families[k] || 0), 0))),
    offFrac: mean(frames.map(f => OFF.reduce((s, k) => s + (perFrame[f].families[k] || 0), 0))),
    grayFrac: mean(frames.map(f => perFrame[f].families['neutral_gray'] || 0)),
    rockFrac: mean(frames.map(f => perFrame[f].families['neutral_rock'] || 0)),
    emissiveTotal: mean(frames.map(f => perFrame[f].emissive.total)),
    emissiveLime: mean(frames.map(f => perFrame[f].emissive.emissive_lime)),
    emissiveCyan: mean(frames.map(f => perFrame[f].emissive.cyan_blue)),
    emissiveAmber: mean(frames.map(f => perFrame[f].emissive.amber_warm)),
    framesWithMultiHueEmissive: frames.filter(f => {
      const e = perFrame[f].emissive;
      let hues = 0; if (e.emissive_lime > 0.0005) hues++; if (e.cyan_blue > 0.0005) hues++; if (e.amber_warm > 0.0005) hues++;
      return hues >= 2;
    }).length,
    valShadow: mean(frames.map(f => perFrame[f].value.shadow)),
    valMid: mean(frames.map(f => perFrame[f].value.mid)),
    valUpper: mean(frames.map(f => perFrame[f].value.upper)),
    valSpike: mean(frames.map(f => perFrame[f].value.spike)),
    valueMedian: mean(frames.map(f => perFrame[f].valueMedian)),
    emissiveP99: mean(frames.map(f => perFrame[f].emissiveP99).filter(x => x != null)),
    meanSat: mean(frames.map(f => perFrame[f].meanSatNonShadow)),
    warmFrac: mean(frames.map(f => perFrame[f].warmFrac)),
    coolFrac: mean(frames.map(f => perFrame[f].coolFrac)),
    edgeGlobal: mean(frames.map(f => perFrame[f].edge.global)),
    bgFgRatio: mean(frames.map(f => perFrame[f].edge.bgFgRatio).filter(x => x != null)),
  };
}

(async () => {
  const perFrame = {};
  for (const f of [...GAMEPLAY, ...DIAGNOSTIC]) {
    perFrame[f] = await measureFrame(join(DIR, f));
  }

  const gameplayAgg = aggregate(GAMEPLAY, perFrame);
  const diagAgg = aggregate(DIAGNOSTIC, perFrame);

  const out = {
    method: 'M1-M7 + valueMedian/emissiveP99/litFromWithinDelta; see header',
    dir: DIR,
    gameplayFrames: GAMEPLAY,
    diagnosticFrames: DIAGNOSTIC,
    perFrame,
    gameplayAggregate: gameplayAgg,
    diagnosticAggregate: diagAgg,
  };
  const outPath = join('/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/pipeline', 'enchanted-forest-rubric-score-carved-r1.json');
  writeFileSync(outPath, JSON.stringify(out, null, 2));

  console.log('=== GAMEPLAY AGGREGATE ===');
  console.log(JSON.stringify(gameplayAgg, null, 2));
  console.log('\n=== DIAGNOSTIC AGGREGATE (look-up-shaft; excluded from composite) ===');
  console.log(JSON.stringify(diagAgg, null, 2));

  console.log('\n--- PER FRAME: valueMedian | emisP99 | litDelta | shadow% | spike% | ench% | gray% | emisTotal% | warm% | cool% ---');
  for (const f of [...GAMEPLAY, ...DIAGNOSTIC]) {
    const p = perFrame[f];
    const ench = ENCH.reduce((s, k) => s + (p.families[k] || 0), 0);
    const tag = GAMEPLAY.includes(f) ? 'PLAY' : 'DIAG';
    console.log(`[${tag}] ${f}: medV=${p.valueMedian.toFixed(3)} emisP99=${(p.emissiveP99 ?? 0).toFixed(3)} litΔ=${(p.litFromWithinDelta ?? 0).toFixed(3)} shadow=${p.value.shadow.toFixed(3)} spike=${p.value.spike.toFixed(4)} ench=${ench.toFixed(3)} gray=${(p.families['neutral_gray'] || 0).toFixed(5)} emis=${p.emissive.total.toFixed(4)} warm=${p.warmFrac.toFixed(4)} cool=${p.coolFrac.toFixed(3)}`);
  }
  console.log('\nWrote', outPath);
})();
