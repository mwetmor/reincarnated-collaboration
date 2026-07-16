// r8-crop-receipts.mjs — Galadriel B-1 crop-receipt harness (Matt 2026-07-16 furniture rescale).
// Rasterizes each r8 plate SVG at the SIMULATED DISPLAY SCALE the reader actually sees post-D7
// (2560 viewport → the 1600px-viewBox plate displays at scale 1.6; 1440 viewport → 0.9), then crops
// the named furniture regions so the re-proportioned chrome can be judged BY EYE at the size Matt sees.
// Read-only inputs (the committed r8 SVGs); writes crop PNGs into the r8 capture folder /crops.
// Deterministic: fixed regions, fixed scales, no wall-clock.

import sharp from 'sharp';
import { readFileSync, mkdirSync } from 'node:fs';
import { resolve, join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const CAP = resolve(__dirname, '../captures/2026-07-16-atlas-edition3-r8-furniture');
const OUT = join(CAP, 'crops');
mkdirSync(OUT, { recursive: true });

const VB_W = 1600, VB_H = 1200;   // plate viewBox
// Simulated display widths: 2560 viewport → plate at 1.6× (Matt's monitor); 1440 → 0.9× (legibility floor).
const DISPLAYS = [
  { tag: '2560disp', px: Math.round(VB_W * 1.6) },   // 2560px-equiv plate width = 2560
  { tag: '1440disp', px: Math.round(VB_W * 0.9) },   // 1440px-equiv plate width = 1440
];

// Crop regions in SVG-coordinate space [x, y, w, h] — the furniture set the brief names.
// (Generous rectangles so each crop shows the furniture in context + a little surrounding ground.)
const REGIONS = [
  { tag: 'title-band',     x: 80,   y: 24,   w: 1000, h: 92  },   // title + RIDER banner + deriv gloss
  { tag: 'key-buildfam',   x: 1330, y: 130,  w: 260,  h: 150 },   // BUILD FAMILIES key (renamed), top-right
  { tag: 'rail-left',      x: 0,    y: 480,  w: 96,   h: 260 },   // DEPLOY rotated rail title + gloss (left)
  { tag: 'rail-right',     x: 1504, y: 480,  w: 96,   h: 260 },   // PERFORM rotated rail title + gloss (right)
  { tag: 'strip-launch',   x: 620,  y: 104,  w: 360,  h: 28  },   // LAUNCH top-strip title+gloss
  { tag: 'pocket-embody',  x: 640,  y: 1104, w: 320,  h: 62  },   // EMBODY bottom-pocket title + gloss rows
  { tag: 'grave-legend',   x: 96,   y: 900,  w: 200,  h: 200 },   // GRAVEYARD legend, bottom-left
  { tag: 'ledger-footer',  x: 80,   y: 1112, w: 1440, h: 88  },   // below-plane ledger (L+R cols) + footer
  { tag: 'plaque-horizon', x: 1180, y: 900,  w: 340,  h: 200 },   // charted-horizon leader label (ghost plaque region)
  { tag: 'centroid-plaques', x: 700, y: 380, w: 520,  h: 340 },   // on-plane condensation anchor plaques
];

async function run() {
  const results = [];
  for (const skin of ['instrument', 'archive']) {
    const svgPath = join(CAP, `atlas-edition3-${skin}.svg`);
    const svg = readFileSync(svgPath);
    for (const d of DISPLAYS) {
      const scale = d.px / VB_W;                 // SVG-coord → pixel
      const heightPx = Math.round(VB_H * scale);
      // Rasterize the WHOLE plate at the display width once, then crop from that buffer.
      const full = await sharp(svg, { density: Math.round(72 * scale) })
        .resize({ width: d.px, height: heightPx, fit: 'fill' })
        .png().toBuffer();
      for (const r of REGIONS) {
        const left = Math.max(0, Math.round(r.x * scale));
        const top = Math.max(0, Math.round(r.y * scale));
        const width = Math.min(d.px - left, Math.round(r.w * scale));
        const height = Math.min(heightPx - top, Math.round(r.h * scale));
        if (width <= 0 || height <= 0) continue;
        const outName = `${skin}-${d.tag}-${r.tag}.png`;
        await sharp(full).extract({ left, top, width, height }).png().toFile(join(OUT, outName));
        results.push(outName);
      }
    }
  }
  console.log(`[r8-crops] wrote ${results.length} crop receipts to ${OUT}`);
  for (const r of results) console.log(`  ${r}`);
}
run();
