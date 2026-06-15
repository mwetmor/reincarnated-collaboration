// lifecycle-strip.mjs — build a labeled contact strip across the fire lifecycle +
// a luma-threshold overlay (HLF highlight mask + SHF shadow mask) for one peak frame,
// so the CV instrument reads are visually defensible (no number without a picture).
//
// Outputs into galadriel/reports/ (NOT into the godot capture dir — raw captures preserved).

import sharp from 'sharp';
import { join } from 'path';

const DIR = '/Users/admin/Games/reincarnated-godot/harness_logs';
const OUT = '/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/reports';
const PREFIX = '11_lift_capture_';

// 8 lifecycle anchor frames spanning pre-ignition -> settle
const anchors = [1, 12, 22, 28, 45, 60, 80, 100];
const labels = ['01 pre-ign', '12 rise', '22 rise-pk', '28 PEAK', '45 burn', '60 burn', '80 wane', '100 settle'];

const THUMB_W = 280;

// ---- contact strip (2 rows x 4) ----
const cells = [];
for (let i = 0; i < anchors.length; i++) {
  const p = join(DIR, `${PREFIX}${String(anchors[i]).padStart(2, '0')}.png`);
  const buf = await sharp(p).resize(THUMB_W, null, { fit: 'inside' })
    .composite([{
      input: Buffer.from(
        `<svg width="${THUMB_W}" height="22"><rect width="100%" height="100%" fill="black" fill-opacity="0.55"/>` +
        `<text x="6" y="16" font-family="monospace" font-size="14" fill="white">${labels[i]}</text></svg>`),
      gravity: 'southwest',
    }])
    .png().toBuffer();
  cells.push(buf);
}
const meta = await sharp(cells[0]).metadata();
const cw = meta.width, ch = meta.height;
const cols = 4, rows = 2;
const strip = sharp({ create: { width: cw * cols, height: ch * rows, channels: 3, background: { r: 10, g: 10, b: 12 } } });
const comps = cells.map((b, i) => ({ input: b, left: (i % cols) * cw, top: Math.floor(i / cols) * ch }));
await strip.composite(comps).png().toFile(join(OUT, '11_lift_lifecycle_strip.png'));
console.log('wrote 11_lift_lifecycle_strip.png');

// ---- luma-threshold overlay on PEAK frame (28): highlight (red) + shadow (blue) masks ----
const peakPath = join(DIR, `${PREFIX}28.png`);
const W = 576;
const { data: gray, info } = await sharp(peakPath).resize(W, null, { fit: 'inside' })
  .grayscale().raw().toBuffer({ resolveWithObject: true });
const w = info.width, h = info.height;
const overlay = Buffer.alloc(w * h * 4, 0); // RGBA transparent
let hi = 0, lo = 0;
for (let i = 0; i < gray.length; i++) {
  const o = i * 4;
  if (gray[i] > 204) { overlay[o] = 255; overlay[o + 3] = 130; hi++; }       // HLF -> red
  else if (gray[i] < 31) { overlay[o + 2] = 255; overlay[o + 3] = 90; lo++; } // SHF -> blue
}
const base = await sharp(peakPath).resize(W, null, { fit: 'inside' }).png().toBuffer();
await sharp(base).composite([{ input: overlay, raw: { width: w, height: h, channels: 4 }, left: 0, top: 0 }])
  .composite([{
    input: Buffer.from(
      `<svg width="${w}" height="44"><rect width="100%" height="100%" fill="black" fill-opacity="0.55"/>` +
      `<text x="6" y="18" font-family="monospace" font-size="13" fill="#ff6666">RED = HLF highlight (luma &gt; 0.80): ${(100 * hi / gray.length).toFixed(1)}%</text>` +
      `<text x="6" y="36" font-family="monospace" font-size="13" fill="#6699ff">BLUE = SHF shadow (luma &lt; 0.12): ${(100 * lo / gray.length).toFixed(1)}%</text></svg>`),
    gravity: 'northwest',
  }])
  .png().toFile(join(OUT, '11_lift_peak28_lumamask.png'));
console.log(`wrote 11_lift_peak28_lumamask.png  (HLF=${(100 * hi / gray.length).toFixed(1)}% SHF=${(100 * lo / gray.length).toFixed(1)}%)`);
