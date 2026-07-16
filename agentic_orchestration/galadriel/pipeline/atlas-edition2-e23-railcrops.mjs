// atlas-edition2-e23-railcrops.mjs
// -----------------------------------------------------------------------------
// EYES-ACCEPTANCE check crops for the E2.3 rail-arrow-orientation fix-pass.
// Extracts the WEST (DEPLOY) and EAST (PERFORM) rail strips from each skin's
// rendered PNG so a human/galadriel can confirm the ON-SCREEN arrows point
// OUTWARD (west arrow reads screen-LEFT; east arrow reads screen-RIGHT).
//
// Geometry (SVG user space 1600x1200; PNG rasterized at 2x → 3200x2400):
//   scale = 2.0  (density 144 / 72)
//   left rail center  x_user = 48   → px 96
//   right rail center x_user = 1552 → px 3104
//   pole labels centered at cyMid = 618 → px 1236 (rotated text spans vertically)
// Crop a tall, narrow strip on each rail covering the rotated title + gloss.
// Also emit a 3x-upscaled zoom of the arrow-glyph neighborhood for legibility.
// -----------------------------------------------------------------------------
import sharp from 'sharp';
import { mkdirSync } from 'node:fs';

const E23_DIR = new URL('../captures/2026-07-16-atlas-edition2-e23/', import.meta.url).pathname;
const OUT_DIR = `${E23_DIR}check-crops/`;
mkdirSync(OUT_DIR, { recursive: true });

const SCALE = 2; // px per user unit
const cyMidPx = 618 * SCALE; // 1236

// Rail strips: x window in px, and a vertical window around cyMid covering the
// rotated title+gloss (title ~15px + gloss + arrow → give ±160 user units → ±320 px).
const STRIPS = {
  west: { xUser0: 0, xUser1: 100, label: 'DEPLOY (west/left rail) — arrow must read screen-LEFT' },
  east: { xUser0: 1500, xUser1: 1600, label: 'PERFORM (east/right rail) — arrow must read screen-RIGHT' },
};
const yHalfUser = 170; // ± around cyMid

for (const skin of ['archive', 'instrument']) {
  const src = `${E23_DIR}atlas-edition2-${skin}.png`;
  const meta = await sharp(src).metadata();
  for (const [side, s] of Object.entries(STRIPS)) {
    const left = Math.max(0, Math.round(s.xUser0 * SCALE));
    const width = Math.min(meta.width - left, Math.round((s.xUser1 - s.xUser0) * SCALE));
    const top = Math.max(0, Math.round((618 - yHalfUser) * SCALE));
    const height = Math.min(meta.height - top, Math.round(2 * yHalfUser * SCALE));
    const out = `${OUT_DIR}railcrop-${skin}-${side}.png`;
    await sharp(src).extract({ left, top, width, height }).toFile(out);
    // 3x zoom for arrow legibility
    const outZoom = `${OUT_DIR}railcrop-${skin}-${side}-3x.png`;
    await sharp(src).extract({ left, top, width, height })
      .resize({ width: width * 3, kernel: 'nearest' }).toFile(outZoom);
    console.log(`[crop] ${skin} ${side}: ${out}  (extract left=${left} top=${top} w=${width} h=${height})  ${s.label}`);
  }
}

// Also a combined full-width horizontal band across cyMid so both rails appear in ONE
// image side-by-side with the plane between them (context: are the arrows pointing AWAY
// from the plane on BOTH sides?).
for (const skin of ['archive', 'instrument']) {
  const src = `${E23_DIR}atlas-edition2-${skin}.png`;
  const meta = await sharp(src).metadata();
  const top = Math.max(0, Math.round((618 - 60) * SCALE));
  const height = Math.min(meta.height - top, Math.round(120 * SCALE));
  const out = `${OUT_DIR}railband-${skin}-full.png`;
  await sharp(src).extract({ left: 0, top, width: meta.width, height }).toFile(out);
  console.log(`[band] ${skin}: ${out} (full-width band across cyMid — both rails + plane)`);
}
console.log(`\ncheck-crops written to ${OUT_DIR}`);
