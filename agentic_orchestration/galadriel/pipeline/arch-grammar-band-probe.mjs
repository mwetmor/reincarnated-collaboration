#!/usr/bin/env node
// arch-grammar-band-probe.mjs
// Objective BACKING measurement for the WS2 architectural-grammar GAP review (2026-06-15).
//
// NOT a pixel-similarity instrument (the frames are different camera framings — see caveat).
// This is a STRUCTURE-DISTRIBUTION proxy backing two manual reads:
//   (1) "scattered verticals vs coherent load-path" — measures how much built edge-structure
//        lives in vertical columns across the frame; a coherent arcade/pier rhythm concentrates
//        vertical edges into regular bands, scattered verticals spread thin + irregular.
//   (2) "storey/gallery presence" — splits the frame into an UPPER band (where a raised gallery
//        storey reads, in an iso ARPG framing) vs a LOWER band (the fighting floor). The reference
//        carries dense BUILT structure in the upper band (gallery + arcade + pier-arch); a flat-walled
//        box carries mostly empty wall / sky-void up top.
//
// Method: Sobel-magnitude edge map (luma), then:
//   - upper-third vs lower-two-thirds mean edge density (the storey proxy)
//   - per-column edge-density profile -> coefficient of variation + autocorrelation-peak count
//     in the upper band (the arcade-rhythm proxy: regular colonnade => periodic peaks)
// All values are PROXIES that BACK the manual rubric; the manual score is the gate (Discipline #4).

import sharp from 'sharp';

const args = process.argv.slice(2);
if (args.length === 0) {
  console.error('usage: node arch-grammar-band-probe.mjs <img1> [img2] ...');
  process.exit(1);
}

function sobelEdges(gray, W, H) {
  // returns Float array of gradient magnitude, same dims
  const out = new Float32Array(W * H);
  const gx = [-1, 0, 1, -2, 0, 2, -1, 0, 1];
  const gy = [-1, -2, -1, 0, 0, 0, 1, 2, 1];
  for (let y = 1; y < H - 1; y++) {
    for (let x = 1; x < W - 1; x++) {
      let sx = 0, sy = 0, k = 0;
      for (let dy = -1; dy <= 1; dy++) {
        for (let dx = -1; dx <= 1; dx++) {
          const v = gray[(y + dy) * W + (x + dx)];
          sx += gx[k] * v;
          sy += gy[k] * v;
          k++;
        }
      }
      out[y * W + x] = Math.sqrt(sx * sx + sy * sy);
    }
  }
  return out;
}

function stats(arr) {
  let s = 0, s2 = 0, n = arr.length;
  for (const v of arr) { s += v; s2 += v * v; }
  const mean = s / n;
  const variance = Math.max(0, s2 / n - mean * mean);
  return { mean, std: Math.sqrt(variance), cv: mean > 0 ? Math.sqrt(variance) / mean : 0 };
}

// count significant periodic peaks in a 1D profile via simple autocorrelation
function autocorrPeaks(profile) {
  const n = profile.length;
  const m = profile.reduce((a, b) => a + b, 0) / n;
  const c = profile.map(v => v - m);
  const denom = c.reduce((a, b) => a + b * b, 0) || 1;
  const acf = [];
  for (let lag = 1; lag < Math.floor(n / 2); lag++) {
    let s = 0;
    for (let i = 0; i + lag < n; i++) s += c[i] * c[i + lag];
    acf.push(s / denom);
  }
  // count local maxima above 0.2 (a real periodic rhythm produces clear ACF side-lobes)
  let peaks = 0;
  for (let i = 1; i < acf.length - 1; i++) {
    if (acf[i] > 0.2 && acf[i] > acf[i - 1] && acf[i] >= acf[i + 1]) peaks++;
  }
  const maxAcf = acf.length ? Math.max(...acf) : 0;
  return { periodicPeaks: peaks, maxAcf: +maxAcf.toFixed(3) };
}

for (const path of args) {
  try {
    const img = sharp(path).removeAlpha().grayscale();
    const { data, info } = await img.raw().toBuffer({ resolveWithObject: true });
    const W = info.width, H = info.height;
    const gray = new Float32Array(W * H);
    for (let i = 0; i < W * H; i++) gray[i] = data[i];

    const edges = sobelEdges(gray, W, H);

    // edge threshold to separate built-structure edges from texture noise
    const thr = 40; // gradient magnitude

    // band split: upper third vs lower two-thirds
    const upperEnd = Math.floor(H / 3);
    let upperSum = 0, upperCnt = 0, lowerSum = 0, lowerCnt = 0;
    const colProfileUpper = new Float64Array(W);
    for (let y = 0; y < H; y++) {
      for (let x = 0; x < W; x++) {
        const e = edges[y * W + x];
        const on = e > thr ? 1 : 0;
        if (y < upperEnd) { upperSum += on; upperCnt++; colProfileUpper[x] += on; }
        else { lowerSum += on; lowerCnt++; }
      }
    }
    const upperDens = upperSum / upperCnt;   // fraction of upper-band pixels that are strong edges
    const lowerDens = lowerSum / lowerCnt;
    const storeyRatio = lowerDens > 0 ? upperDens / lowerDens : 0;

    // arcade-rhythm proxy: column profile of upper-band edge counts
    // downsample columns to ~120 bins to suppress per-pixel noise
    const BINS = 120;
    const binProfile = new Float64Array(BINS);
    for (let x = 0; x < W; x++) {
      const b = Math.min(BINS - 1, Math.floor((x / W) * BINS));
      binProfile[b] += colProfileUpper[x];
    }
    const cvUpper = stats(Array.from(binProfile)).cv;
    const { periodicPeaks, maxAcf } = autocorrPeaks(Array.from(binProfile));

    const name = path.split('/').pop();
    console.log(JSON.stringify({
      frame: name,
      dims: `${W}x${H}`,
      upperBand_edgeDensity: +upperDens.toFixed(4),
      lowerBand_edgeDensity: +lowerDens.toFixed(4),
      storeyRatio_upperOverLower: +storeyRatio.toFixed(3),
      upperBand_columnProfile_CV: +cvUpper.toFixed(3),
      upperBand_arcadeRhythm_periodicPeaks: periodicPeaks,
      upperBand_arcadeRhythm_maxAutocorr: maxAcf,
    }));
  } catch (e) {
    console.error(`ERR ${path}: ${e.message}`);
  }
}
