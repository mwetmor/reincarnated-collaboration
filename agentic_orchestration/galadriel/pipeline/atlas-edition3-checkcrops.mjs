// atlas-edition3-checkcrops.mjs
// -----------------------------------------------------------------------------
// EYES-ACCEPTANCE check crops for the Edition-III census-population render
// (gandalf brief 2026-07-16 deliverable 3). Extracts, from each skin's rendered
// PNG (3200x2400 = 1600x1200 @ 2x):
//   (a) both RAIL strips ON-SCREEN (west/DEPLOY reads screen-LEFT; east/PERFORM
//       reads screen-RIGHT) + UN-ROTATED variants (crop the rail label region,
//       rotate 90° CW so the letters read UPRIGHT — the arrow glyph is then
//       unambiguous: west must read "↑ DEPLOY", east "PERFORM ↓").
//   (b) the TITLE plate ("Build Horizon — Edition III").
//   (c) NEW-CONTENT cells — the two black-hole ROOTED/ZONE pull cells that lit
//       this edition (pull-lit went 2→4). Located from the emission's frozen
//       point-bounds transform (identical to Edition-II; the fit is frozen).
//   (d) the FOOTER stamp / denominator line (right census + left provenance).
//   + a full-width rail BAND (both rails + plane in one frame, for context).
//
// Geometry replicated EXACTLY from the head (atlas-edition3-render.mjs):
//   W=1600 H=1200; M={top:132,right:96,bottom:96,left:96}; PW=1408 PH=972.
//   world→svg: sx=M.left+((x-minX)/(maxX-minX))*PW ; sy=M.top+(1-(y-minY)/(maxY-minY))*PH
//   bounds from ALL 506 frozen points + 6% pad (byte-identical to Edition-II).
//   rail centers: west x_user=48, east x_user=1552; pole labels rotated(-90) at cyMid=618.
//   PNG scale = 2.0 (density 144 / 72).
// Rotate direction: rail text is rendered rotate(-90) (90° CCW). To un-rotate so
// letters read upright, rotate the crop +90° CW. sharp .rotate(90) is clockwise.
// -----------------------------------------------------------------------------
import sharp from 'sharp';
import { readFileSync, mkdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve, join } from 'node:path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ATLAS_PATH = resolve(__dirname, '../../research/curated/atlas/atlas-edition3.json');
const OUT_BASE = resolve(__dirname, '../captures/2026-07-16-atlas-edition3/');
const OUT_DIR = join(OUT_BASE, 'check-crops');
mkdirSync(OUT_DIR, { recursive: true });

const SCALE = 2; // px per user unit (PNG rasterized at density 144)

// --- replicate the head's world→svg transform from the frozen points ---
const atlas = JSON.parse(readFileSync(ATLAS_PATH, 'utf8'));
const pts = atlas.points;
const xs = pts.map((p) => p.x), ys = pts.map((p) => p.y);
const rawMinX = Math.min(...xs), rawMaxX = Math.max(...xs);
const rawMinY = Math.min(...ys), rawMaxY = Math.max(...ys);
const padX = (rawMaxX - rawMinX) * 0.06, padY = (rawMaxY - rawMinY) * 0.06;
const minX = rawMinX - padX, maxX = rawMaxX + padX;
const minY = rawMinY - padY, maxY = rawMaxY + padY;
const W = 1600, H = 1200, M = { top: 132, right: 96, bottom: 96, left: 96 };
const PW = W - M.left - M.right, PH = H - M.top - M.bottom;
const sx = (x) => M.left + ((x - minX) / (maxX - minX)) * PW;
const sy = (y) => M.top + (1 - (y - minY) / (maxY - minY)) * PH;
const px = (u) => Math.round(u * SCALE);

// --- locate the two ROOTED/ZONE pull cells that lit this edition (from pull_slice) ---
// pull-lit went 2→4; the two NEW ones are the ROOTED/ZONE pulls. We resolve their (x,y)
// from ghost_field.feasible_cells (lit + core[3]=='pull' + core[0]=='ROOTED' + core[1]=='ZONE').
const rootedZonePulls = atlas.ghost_field.feasible_cells.filter(
  (c) => c.lit && c.core[3] === 'pull' && c.core[0] === 'ROOTED' && c.core[1] === 'ZONE'
);

function clampExtract(meta, left, top, width, height) {
  const l = Math.max(0, Math.min(left, meta.width - 1));
  const t = Math.max(0, Math.min(top, meta.height - 1));
  const w = Math.max(1, Math.min(width, meta.width - l));
  const h = Math.max(1, Math.min(height, meta.height - t));
  return { left: l, top: t, width: w, height: h };
}

const cyMid = M.top + PH / 2; // 618 world; the rail labels center here

for (const skin of ['archive', 'instrument']) {
  const src = join(OUT_BASE, `atlas-edition3-${skin}.png`);
  const meta = await sharp(src).metadata();

  // ---- (a) RAIL STRIPS on-screen (tall narrow window on each rail) ----
  const yHalf = 175; // ± world units around cyMid (covers rotated title + gloss + arrow)
  const RAILS = {
    west: { xU0: 0, xU1: 100, txt: 'DEPLOY (west/left rail) — on-screen arrow must read screen-LEFT (OUTWARD)' },
    east: { xU0: 1500, xU1: 1600, txt: 'PERFORM (east/right rail) — on-screen arrow must read screen-RIGHT (OUTWARD)' },
  };
  for (const [side, r] of Object.entries(RAILS)) {
    const reg = clampExtract(meta, px(r.xU0), px(cyMid - yHalf), px(r.xU1 - r.xU0), px(2 * yHalf));
    // extract ONCE to a buffer, then derive the variants from it (avoids extract-area re-parse issues)
    const stripBuf = await sharp(src).extract(reg).png().toBuffer();
    // on-screen strip
    await sharp(stripBuf).toFile(join(OUT_DIR, `rail-${skin}-${side}-onscreen.png`));
    // 3x zoom for arrow legibility
    await sharp(stripBuf).resize({ width: reg.width * 3, kernel: 'nearest' })
      .toFile(join(OUT_DIR, `rail-${skin}-${side}-onscreen-3x.png`));
    // UN-ROTATED: rotate the strip +90° CW so the rotate(-90) label reads UPRIGHT, then 3x-upscale
    const rotBuf = await sharp(stripBuf).rotate(90).png().toBuffer();
    const rotMeta = await sharp(rotBuf).metadata();
    await sharp(rotBuf).resize({ width: rotMeta.width * 3, kernel: 'nearest' })
      .toFile(join(OUT_DIR, `rail-${skin}-${side}-unrotated-cw90.png`));
    console.log(`[rail] ${skin} ${side}: onscreen + 3x + unrotated-cw90  (extract ${JSON.stringify(reg)})  ${r.txt}`);
  }

  // ---- (a2) full-width rail BAND across cyMid (both rails + plane in one frame) ----
  {
    const reg = clampExtract(meta, 0, px(cyMid - 55), meta.width, px(110));
    await sharp(src).extract(reg).toFile(join(OUT_DIR, `railband-${skin}-full.png`));
    console.log(`[band] ${skin}: railband-full (both rails + plane; arrows must point AWAY from plane on BOTH sides)`);
  }

  // ---- (b) TITLE PLATE ("Build Horizon — Edition III") — top-left, x=M.left y≈42, badge to y≈102 ----
  {
    const reg = clampExtract(meta, px(M.left - 8), px(20), px(760), px(96));
    const buf = await sharp(src).extract(reg).png().toBuffer();
    await sharp(buf).toFile(join(OUT_DIR, `title-plate-${skin}.png`));
    await sharp(buf).resize({ width: reg.width * 2, kernel: 'lanczos3' })
      .toFile(join(OUT_DIR, `title-plate-${skin}-2x.png`));
    console.log(`[title] ${skin}: title-plate (must read "Build Horizon — Edition III")`);
  }

  // ---- (c) NEW-CONTENT ROOTED/ZONE pull cells (lit this edition; pull-lit 2→4) ----
  let idx = 0;
  for (const c of rootedZonePulls) {
    const cx = sx(c.x), cy = sy(c.y);
    const half = 90; // world-unit half-window around the lit cell
    const reg = clampExtract(meta, px(cx - half), px(cy - half), px(2 * half), px(2 * half));
    const tag = c.core.join('_').replace(/[^A-Za-z0-9]+/g, '-');
    const buf = await sharp(src).extract(reg).png().toBuffer();
    await sharp(buf).resize({ width: reg.width * 3, kernel: 'nearest' })
      .toFile(join(OUT_DIR, `newcell-rooted-zone-pull-${idx}-${skin}.png`));
    console.log(`[newcell] ${skin} #${idx}: ROOTED/ZONE pull [${c.core.join(',')}] @ world(${c.x.toFixed(4)},${c.y.toFixed(4)}) → svg(${cx.toFixed(1)},${cy.toFixed(1)}) → px(${px(cx)},${px(cy)})  ${tag}`);
    idx++;
  }

  // ---- (d) FOOTER stamp / denominator line — bottom band (y≈1188), full width ----
  {
    const buf = await sharp(src).extract(clampExtract(meta, 0, px(H - 12 - 22), meta.width, px(40))).png().toBuffer();
    await sharp(buf).toFile(join(OUT_DIR, `footer-stamp-${skin}.png`));
    // right-half zoom (the census/denominator end-anchored at plane-right x=1504)
    const regR = clampExtract(meta, px(880), px(H - 12 - 22), px(720), px(40));
    const bufR = await sharp(src).extract(regR).png().toBuffer();
    await sharp(bufR).resize({ width: regR.width * 2, kernel: 'lanczos3' })
      .toFile(join(OUT_DIR, `footer-denominator-${skin}-2x.png`));
    // left provenance zoom (atlasVersion · register · emitted · skin, left-anchored at x=96)
    const regL = clampExtract(meta, px(80), px(H - 12 - 22), px(720), px(40));
    const bufL = await sharp(src).extract(regL).png().toBuffer();
    await sharp(bufL).resize({ width: regL.width * 2, kernel: 'lanczos3' })
      .toFile(join(OUT_DIR, `footer-provenance-${skin}-2x.png`));
    console.log(`[footer] ${skin}: footer-stamp + denominator-2x (must show 767,411,820; NOT 819,439,740) + provenance-2x (Edition-III · v1.3)`);
  }
}

console.log(`\nEdition-III check-crops written to ${OUT_DIR}`);
console.log(`ROOTED/ZONE pull cells located (new this edition): ${rootedZonePulls.length}`);
for (const c of rootedZonePulls) console.log(`  [${c.core.join(',')}] @ (${c.x.toFixed(4)},${c.y.toFixed(4)})`);
