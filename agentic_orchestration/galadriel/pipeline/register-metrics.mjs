// register-metrics.mjs — galadriel visual-register decomposition metrics
//
// Purpose: produce DEFENSIBLE, REPRODUCIBLE numbers for the 2026-06-14 3D-stylized-ARPG
// register benchmark. Tests gandalf's design thesis that "low-poly" bundles two independent
// axes (geometry density vs texture/material richness) and that premium-feel is carried
// primarily by texture+lighting+VFX rather than polygon count.
//
// Metrics (all on downscaled-normalized grayscale + HSV, so resolution/compression-robust):
//   1. HFD  — High-Frequency Detail density (Laplacian edge energy / px). Texture+VFX busyness.
//   2. LMV  — Local Material Variance (mean per-tile luminance std-dev over an 8x8 tile grid).
//             Proxy for "is each surface flat-shaded (low) or richly-shaded/painted (high)".
//   3. LDR  — Luminance Dynamic Range (p95 - p05 of luma). Proxy for lighting drama
//             (lit-volume-in-darkness => high; evenly-flat-lit => low).
//   4. SAT  — Mean HSV saturation + saturation std-dev. Color register vividness.
//   5. HLF  — Highlight Fraction (% px with luma > 0.80). Proxy for VFX/bloom/glow presence.
//   6. SHF  — Shadow Fraction (% px with luma < 0.12). Proxy for dramatic-dark atmosphere.
//
// Method notes (no silent transformation per galadriel discipline):
//   - All images resized to 960px wide (preserve aspect), grayscale for HFD/LMV/LDR/HLF/SHF.
//   - Laplacian = 3x3 kernel [0,1,0; 1,-4,1; 0,1,0]; HFD = mean(|laplacian|) over interior px,
//     normalized to 0-255 luma scale. Compression (JPEG) suppresses HFD somewhat — reported
//     as a known caveat; all reference imagery is comparable-compression Steam JPEG so the
//     RELATIVE ordering is the load-bearing read, not absolute values.
//   - LMV computed on an 8x8 grid of tiles (120x67 px each at 960x540-ish); per-tile std,
//     then mean across tiles. UI-chrome regions are NOT masked in v1 (caveat noted in report).

import sharp from 'sharp';
import { readFileSync } from 'fs';

const TARGET_W = 960;

function laplacianEnergy(gray, w, h) {
  let sum = 0, n = 0;
  for (let y = 1; y < h - 1; y++) {
    for (let x = 1; x < w - 1; x++) {
      const i = y * w + x;
      const lap = -4 * gray[i] + gray[i - 1] + gray[i + 1] + gray[i - w] + gray[i + w];
      sum += Math.abs(lap);
      n++;
    }
  }
  return sum / n; // mean |laplacian| in 0-255 luma units
}

function localMaterialVariance(gray, w, h, gx = 8, gy = 8) {
  const tw = Math.floor(w / gx), th = Math.floor(h / gy);
  const tileStds = [];
  for (let ty = 0; ty < gy; ty++) {
    for (let tx = 0; tx < gx; tx++) {
      let s = 0, ss = 0, cnt = 0;
      for (let y = ty * th; y < (ty + 1) * th; y++) {
        for (let x = tx * tw; x < (tx + 1) * tw; x++) {
          const v = gray[y * w + x];
          s += v; ss += v * v; cnt++;
        }
      }
      const mean = s / cnt;
      const variance = ss / cnt - mean * mean;
      tileStds.push(Math.sqrt(Math.max(0, variance)));
    }
  }
  const mean = tileStds.reduce((a, b) => a + b, 0) / tileStds.length;
  return mean;
}

function percentile(sortedArr, p) {
  const idx = Math.min(sortedArr.length - 1, Math.max(0, Math.floor(p * sortedArr.length)));
  return sortedArr[idx];
}

async function measure(path) {
  // Grayscale path
  const g = sharp(path).resize(TARGET_W, null, { fit: 'inside' }).grayscale();
  const { data: gray, info } = await g.raw().toBuffer({ resolveWithObject: true });
  const w = info.width, h = info.height;

  const hfd = laplacianEnergy(gray, w, h);
  const lmv = localMaterialVariance(gray, w, h);

  // luma stats
  const lumaSorted = Float64Array.from(gray).slice().sort();
  const ldr = (percentile(lumaSorted, 0.95) - percentile(lumaSorted, 0.05));
  let hi = 0, lo = 0;
  for (let i = 0; i < gray.length; i++) {
    if (gray[i] > 204) hi++;        // > 0.80 * 255
    if (gray[i] < 31) lo++;         // < 0.12 * 255
  }
  const hlf = (100 * hi) / gray.length;
  const shf = (100 * lo) / gray.length;

  // saturation path (HSV via raw RGB)
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
    HFD: +hfd.toFixed(2),
    LMV: +lmv.toFixed(2),
    LDR: +ldr.toFixed(1),
    SAT_mean: +satMean.toFixed(3),
    SAT_std: +satStd.toFixed(3),
    HLF_pct: +hlf.toFixed(2),
    SHF_pct: +shf.toFixed(2),
    dims: `${w}x${h}`,
  };
}

const args = process.argv.slice(2);
if (args.length === 0) {
  console.error('usage: node register-metrics.mjs <label=path> [label=path ...]');
  process.exit(1);
}

const rows = [];
for (const a of args) {
  const eq = a.indexOf('=');
  const label = eq > 0 ? a.slice(0, eq) : a;
  const path = eq > 0 ? a.slice(eq + 1) : a;
  try {
    const m = await measure(path);
    rows.push({ label, ...m });
  } catch (e) {
    rows.push({ label, error: String(e.message || e) });
  }
}

// pretty table
const cols = ['label', 'HFD', 'LMV', 'LDR', 'SAT_mean', 'SAT_std', 'HLF_pct', 'SHF_pct'];
const widths = cols.map(c => Math.max(c.length, ...rows.map(r => String(r[c] ?? '').length)));
const fmt = (r) => cols.map((c, i) => String(r[c] ?? '').padEnd(widths[i])).join('  ');
console.log(cols.map((c, i) => c.padEnd(widths[i])).join('  '));
console.log(widths.map(w => '-'.repeat(w)).join('  '));
for (const r of rows) console.log(fmt(r));
console.log('\nJSON:');
console.log(JSON.stringify(rows, null, 2));
