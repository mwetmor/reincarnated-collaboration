// lifecycle-strip-cathedral.mjs — labeled contact strip across the Cathedral fire lifecycle
// + a luma-threshold overlay (HLF highlight mask + SHF shadow mask) on the HLF-peak frame (26),
// so the CV reads are visually defensible (no number without a picture).
//
// Same instruments / same overlay math as lifecycle-strip.mjs; only PREFIX + anchor frames +
// peak-frame change (cathedral hero-event timing: braziers from f0, charge ~30, erupt ~52,
// CV-HLF-peak f26). Outputs into galadriel/reports/ (raw captures preserved).

import sharp from 'sharp';
import { join } from 'path';

const DIR = '/Users/admin/Games/reincarnated-godot/harness_logs';
const OUT = '/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/reports';
const PREFIX = '12_cathedral_capture_';

// 8 lifecycle anchor frames spanning pre-ignition -> waning-settle
const anchors = [5, 20, 30, 52, 60, 80, 90, 100];
const labels = ['05 pre-ign', '20 charge', '30 charge-pk', '52 ERUPT', '60 PEAK', '80 burn', '90 wane', '100 settle'];

const THUMB_W = 280;

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
await strip.composite(comps).png().toFile(join(OUT, '12_cathedral_lifecycle_strip.png'));
console.log('wrote 12_cathedral_lifecycle_strip.png');

// ---- luma-threshold overlay on HLF-PEAK frame (26): highlight (red) + shadow (blue) masks ----
const peakFrame = 26;
const peakPath = join(DIR, `${PREFIX}${peakFrame}.png`);
const W = 576;
const { data: gray, info } = await sharp(peakPath).resize(W, null, { fit: 'inside' })
  .grayscale().raw().toBuffer({ resolveWithObject: true });
const w = info.width, h = info.height;
const overlay = Buffer.alloc(w * h * 4, 0);
let hi = 0, lo = 0;
for (let i = 0; i < gray.length; i++) {
  const o = i * 4;
  if (gray[i] > 204) { overlay[o] = 255; overlay[o + 3] = 130; hi++; }
  else if (gray[i] < 31) { overlay[o + 2] = 255; overlay[o + 3] = 90; lo++; }
}
const base = await sharp(peakPath).resize(W, null, { fit: 'inside' }).png().toBuffer();
await sharp(base).composite([{ input: overlay, raw: { width: w, height: h, channels: 4 }, left: 0, top: 0 }])
  .composite([{
    input: Buffer.from(
      `<svg width="${w}" height="44"><rect width="100%" height="100%" fill="black" fill-opacity="0.55"/>` +
      `<text x="6" y="18" font-family="monospace" font-size="13" fill="#ff6666">RED = HLF highlight (luma &gt; 0.80): ${(100 * hi / gray.length).toFixed(1)}%  [f${peakFrame} CV-peak]</text>` +
      `<text x="6" y="36" font-family="monospace" font-size="13" fill="#6699ff">BLUE = SHF shadow (luma &lt; 0.12): ${(100 * lo / gray.length).toFixed(1)}%</text></svg>`),
    gravity: 'northwest',
  }])
  .png().toFile(join(OUT, '12_cathedral_peak26_lumamask.png'));
console.log(`wrote 12_cathedral_peak26_lumamask.png  (HLF=${(100 * hi / gray.length).toFixed(1)}% SHF=${(100 * lo / gray.length).toFixed(1)}%)`);
