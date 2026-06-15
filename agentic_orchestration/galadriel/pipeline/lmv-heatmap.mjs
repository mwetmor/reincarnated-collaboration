// lmv-heatmap.mjs — per-tile Local Material Variance heatmap on a single frame.
// Purpose: make the material-shading axis defensible. A FLAT per-face graybox would show
// near-zero per-tile luma std across surface interiors (variance only at face boundaries).
// A light-responsive material (procedural roughness + filmic lighting) shows DISTRIBUTED
// per-tile variance across surface interiors. The heatmap shows WHERE the variance lives.
//
// Uses a finer 24x14 tile grid (vs the 8x8 scoring grid) for spatial resolution.
// Outputs to galadriel/reports/.

import sharp from 'sharp';
import { join } from 'path';

const SRC = process.argv[2] || '/Users/admin/Games/reincarnated-godot/harness_logs/11_lift_capture_99.png';
const OUTNAME = process.argv[3] || '11_lift_settle99_lmv_heatmap.png';
const OUT = '/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/reports';
const W = 576;
const GX = 24, GY = 14;

const { data: gray, info } = await sharp(SRC).resize(W, null, { fit: 'inside' })
  .grayscale().raw().toBuffer({ resolveWithObject: true });
const w = info.width, h = info.height;
const tw = Math.floor(w / GX), th = Math.floor(h / GY);

const stds = [];
for (let ty = 0; ty < GY; ty++) {
  for (let tx = 0; tx < GX; tx++) {
    let s = 0, ss = 0, cnt = 0;
    for (let y = ty * th; y < (ty + 1) * th && y < h; y++) {
      for (let x = tx * tw; x < (tx + 1) * tw && x < w; x++) {
        const v = gray[y * w + x]; s += v; ss += v * v; cnt++;
      }
    }
    const m = s / cnt;
    stds.push(Math.sqrt(Math.max(0, ss / cnt - m * m)));
  }
}
const maxStd = Math.max(...stds);
const meanStd = stds.reduce((a, b) => a + b, 0) / stds.length;

// build RGBA heat overlay (green=low variance/flat, red=high variance/light-responsive)
const overlay = Buffer.alloc(w * h * 4, 0);
for (let ty = 0; ty < GY; ty++) {
  for (let tx = 0; tx < GX; tx++) {
    const v = stds[ty * GX + tx] / maxStd; // 0..1
    const r = Math.round(255 * v), g = Math.round(180 * (1 - v));
    for (let y = ty * th; y < (ty + 1) * th && y < h; y++) {
      for (let x = tx * tw; x < (tx + 1) * tw && x < w; x++) {
        const o = (y * w + x) * 4;
        overlay[o] = r; overlay[o + 1] = g; overlay[o + 2] = 0; overlay[o + 3] = 95;
      }
    }
  }
}
const base = await sharp(SRC).resize(W, null, { fit: 'inside' }).png().toBuffer();
await sharp(base).composite([{ input: overlay, raw: { width: w, height: h, channels: 4 }, left: 0, top: 0 }])
  .composite([{
    input: Buffer.from(
      `<svg width="${w}" height="40"><rect width="100%" height="100%" fill="black" fill-opacity="0.6"/>` +
      `<text x="6" y="16" font-family="monospace" font-size="12" fill="white">LMV per-tile luma std (24x14): red=high(light-responsive) green=low(flat)</text>` +
      `<text x="6" y="33" font-family="monospace" font-size="12" fill="white">mean=${meanStd.toFixed(1)}  max=${maxStd.toFixed(1)}  src=${SRC.split('/').pop()}</text></svg>`),
    gravity: 'northwest',
  }])
  .png().toFile(join(OUT, OUTNAME));
console.log(`wrote ${OUTNAME}  meanStd=${meanStd.toFixed(2)} maxStd=${maxStd.toFixed(2)}`);
