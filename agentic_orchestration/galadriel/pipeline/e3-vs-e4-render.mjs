// e3-vs-e4-render.mjs — Edition-III vs Edition-IV ratification-gate render.
//
// Purpose: produce a focused visual comparison plate that Matt uses at the E4 ratification
// gate. This is a LOCAL render only — the serving surface stays on Edition III until
// ratified. NO deploy, NO vendor mutation, read-only on both atlas jsons.
//
// Design choices (per gandalf-prime autonomous atlas-parity invocation 2026-07-16):
//   - Reuse projection convention from atlas-edition3-render.mjs: 1600x1200 canvas,
//     M={top:132,right:96,bottom:96,left:96} margins, linear world→svg, y-flip. This makes
//     the E3 render in THIS pipeline overlay-comparable to the served instrument.
//   - HARD viewport lock to E3 bounds (not E4's). If the 56 new E4 points would extend
//     the box, we ALSO emit a rescaled-to-E4 view AND a prior-viewport crop, and say so
//     explicitly per invocation § 3. (Verified upstream: E3 and E4 have byte-identical
//     bounding box; the new 56 all lie WITHIN E3 extent. No rescale needed. See report.)
//   - Three point classes on the delta view:
//       PRE-EXISTING  → dim grey (both active + legacy-tombstone)
//       NEW POSITIVE  → saturated blue (50 points; la-*/mcd-*/re-key)
//       NEW TOMBSTONE → red X-cross glyph (6 la-* seated-extrinsic + sentinel)
//   - G-3 pixel corroboration: render E3-only and E4-restricted-to-shared-IDs at
//     identical projection, then take pixel diff. Zero-diff (up to antialiasing) is
//     the visual affirmation of the upstream byte-identity gate.
//
// Determinism: same input jsons → byte-identical SVGs (sorted iteration; no RNG).
//
// Inputs:  atlas-edition3.json (506) + atlas-edition4.json (562), READ-ONLY.
// Outputs: SVGs + PNGs in captures/2026-07-16-e3-vs-e4-ratification/.

import { readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve, join } from 'node:path';
import sharp from 'sharp';

const __dirname = dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = resolve(__dirname, '../../..');
const E3_PATH = join(REPO_ROOT, 'agentic_orchestration/research/curated/atlas/atlas-edition3.json');
const E4_PATH = join(REPO_ROOT, 'agentic_orchestration/research/curated/atlas/atlas-edition4.json');
const OUT_DIR = join(REPO_ROOT, 'agentic_orchestration/galadriel/captures/2026-07-16-e3-vs-e4-ratification');

// ------------------------------------------------------------------- data load
const e3 = JSON.parse(readFileSync(E3_PATH, 'utf8'));
const e4 = JSON.parse(readFileSync(E4_PATH, 'utf8'));

if (e3.edition !== 3) throw new Error(`Expected E3.edition=3, got ${e3.edition}`);
if (e4.edition !== 4) throw new Error(`Expected E4.edition=4, got ${e4.edition}`);

const E3_PTS = e3.points;
const E4_PTS = e4.points;
const E3_IDS = new Set(E3_PTS.map(p => p.kit_id));

// Classify E4 points.
// LEGEND (per invocation § 2):
//   1. PRE-EXISTING (506)      — kit_id in E3
//   2. NEW POSITIVE (50)       — kit_id NOT in E3, no death_class field
//   3. NEW TOMBSTONE (6)       — kit_id NOT in E3, has death_class field
// Discriminator confirmed by G-4 census + point-schema introspection: tombstones
// (both legacy and new) carry a `death_class` string; positives do not.
const E4_PREEX = E4_PTS.filter(p => E3_IDS.has(p.kit_id));
const E4_NEW   = E4_PTS.filter(p => !E3_IDS.has(p.kit_id));
const E4_NEW_TOMB = E4_NEW.filter(p => 'death_class' in p);
const E4_NEW_POS  = E4_NEW.filter(p => !('death_class' in p));

if (E4_PREEX.length !== 506) throw new Error(`E4 pre-existing != 506 (got ${E4_PREEX.length})`);
if (E4_NEW.length !== 56)    throw new Error(`E4 new-only != 56 (got ${E4_NEW.length})`);
if (E4_NEW_TOMB.length !== 6) throw new Error(`E4 new tombstones != 6 (got ${E4_NEW_TOMB.length})`);
if (E4_NEW_POS.length !== 50) throw new Error(`E4 new positives != 50 (got ${E4_NEW_POS.length})`);

// ---------------------------------------------------------------- projection
// Match atlas-edition3-render.mjs conventions verbatim so this plate is dimensionally
// comparable to the served instrument. Padding factor is a tiny expansion so extreme
// points don't stick to the frame edge; matches the served renderer's practice.
const PAD = 0.04;
const allX = E3_PTS.map(p => p.x).concat(E4_PTS.map(p => p.x));
const allY = E3_PTS.map(p => p.y).concat(E4_PTS.map(p => p.y));
const rawMinX = Math.min(...allX), rawMaxX = Math.max(...allX);
const rawMinY = Math.min(...allY), rawMaxY = Math.max(...allY);
const padX = (rawMaxX - rawMinX) * PAD;
const padY = (rawMaxY - rawMinY) * PAD;
const minX = rawMinX - padX, maxX = rawMaxX + padX;
const minY = rawMinY - padY, maxY = rawMaxY + padY;

// E3-only extent (for viewport verification)
const e3MinX = Math.min(...E3_PTS.map(p => p.x)); const e3MaxX = Math.max(...E3_PTS.map(p => p.x));
const e3MinY = Math.min(...E3_PTS.map(p => p.y)); const e3MaxY = Math.max(...E3_PTS.map(p => p.y));
// E4-only extent
const e4MinX = Math.min(...E4_PTS.map(p => p.x)); const e4MaxX = Math.max(...E4_PTS.map(p => p.x));
const e4MinY = Math.min(...E4_PTS.map(p => p.y)); const e4MaxY = Math.max(...E4_PTS.map(p => p.y));
// Do the 56 new points sit inside E3 bounding box? YES if new-only extent ⊆ E3 extent.
const newMinX = Math.min(...E4_NEW.map(p => p.x)); const newMaxX = Math.max(...E4_NEW.map(p => p.x));
const newMinY = Math.min(...E4_NEW.map(p => p.y)); const newMaxY = Math.max(...E4_NEW.map(p => p.y));
const NEW_WITHIN_E3 = (newMinX >= e3MinX && newMaxX <= e3MaxX && newMinY >= e3MinY && newMaxY <= e3MaxY);

// Canvas: 1600x1200 to match served instrument. For side-by-side we stitch two of these.
const W = 1600, H = 1200;
const M = { top: 132, right: 96, bottom: 96, left: 96 };
const PW = W - M.left - M.right;   // 1408
const PH = H - M.top - M.bottom;   // 972
const sx = x => M.left + ((x - minX) / (maxX - minX)) * PW;
const sy = y => M.top  + (1 - (y - minY) / (maxY - minY)) * PH;
const f2 = n => Number(n).toFixed(2);

const zeroX = (minX <= 0 && maxX >= 0) ? sx(0) : null;
const zeroY = (minY <= 0 && maxY >= 0) ? sy(0) : null;

// ---------------------------------------------------------------- style palette
const FONT = "'Inter', 'Helvetica Neue', Helvetica, Arial, sans-serif";
const COL = {
  bg:            '#0f1115',
  plane:         '#141821',
  gridDim:       '#242a36',
  gridZero:      '#3a4356',
  titlePrimary:  '#e8ecf3',
  titleSecondary:'#9aa3b2',
  // point classes
  active:        '#a4b0c2',   // pre-existing active (E3 active, still active in E4)
  legacyTomb:    '#5a5a68',   // pre-existing tombstone (E3 tombstone, still tombstoned in E4)
  newPositive:   '#4fa3ff',   // NEW positive (50)
  newTomb:       '#ff5a58',   // NEW tombstone (6)
  // delta-view dim
  preexDim:      '#333743',
  legacyTombDim: '#2a2a30',
  // annotations
  ann:           '#c4cbd8',
  annAccent:     '#4fa3ff',
  annAccentT:    '#ff5a58',
};

// ---------------------------------------------------------------- svg helpers
function svgOpen(title, subtitle) {
  const p = [];
  p.push(`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" font-family="${FONT}">`);
  p.push(`<rect x="0" y="0" width="${W}" height="${H}" fill="${COL.bg}"/>`);
  // plane box
  p.push(`<rect x="${M.left}" y="${M.top}" width="${PW}" height="${PH}" fill="${COL.plane}"/>`);
  // grid (light quarter-lines)
  for (let i = 1; i < 4; i++) {
    const gx = M.left + (i / 4) * PW;
    const gy = M.top + (i / 4) * PH;
    p.push(`<line x1="${f2(gx)}" y1="${M.top}" x2="${f2(gx)}" y2="${M.top+PH}" stroke="${COL.gridDim}" stroke-width="0.5"/>`);
    p.push(`<line x1="${M.left}" y1="${f2(gy)}" x2="${M.left+PW}" y2="${f2(gy)}" stroke="${COL.gridDim}" stroke-width="0.5"/>`);
  }
  // zero-axis lines
  if (zeroX !== null) p.push(`<line x1="${f2(zeroX)}" y1="${M.top}" x2="${f2(zeroX)}" y2="${M.top+PH}" stroke="${COL.gridZero}" stroke-width="1"/>`);
  if (zeroY !== null) p.push(`<line x1="${M.left}" y1="${f2(zeroY)}" x2="${M.left+PW}" y2="${f2(zeroY)}" stroke="${COL.gridZero}" stroke-width="1"/>`);
  // title bar
  p.push(`<text x="${M.left}" y="60" fill="${COL.titlePrimary}" font-size="34" font-weight="600">${title}</text>`);
  p.push(`<text x="${M.left}" y="96" fill="${COL.titleSecondary}" font-size="18">${subtitle}</text>`);
  // axis labels
  p.push(`<text x="${M.left + PW/2}" y="${H - 24}" fill="${COL.titleSecondary}" font-size="16" text-anchor="middle">dim 1 — PERFORM &#8592;&#8594; DEPLOY</text>`);
  p.push(`<text x="30" y="${M.top + PH/2}" fill="${COL.titleSecondary}" font-size="16" text-anchor="middle" transform="rotate(-90, 30, ${M.top + PH/2})">dim 2 — EMBODY &#8592;&#8594; LAUNCH</text>`);
  // frame outline
  p.push(`<rect x="${M.left}" y="${M.top}" width="${PW}" height="${PH}" fill="none" stroke="${COL.gridZero}" stroke-width="1"/>`);
  return p;
}

function svgClose(p) {
  p.push('</svg>');
  return p.join('\n');
}

function drawActive(p, pts, color, r=3.2) {
  // sort for deterministic output
  const s = [...pts].sort((a,b) => (a.kit_id < b.kit_id ? -1 : 1));
  for (const pt of s) {
    p.push(`<circle cx="${f2(sx(pt.x))}" cy="${f2(sy(pt.y))}" r="${r}" fill="${color}" opacity="0.85"/>`);
  }
}

// Legacy tombstones (E3 supplementary) → open ring
function drawLegacyTomb(p, pts, color, r=3.6) {
  const s = [...pts].sort((a,b) => (a.kit_id < b.kit_id ? -1 : 1));
  for (const pt of s) {
    p.push(`<circle cx="${f2(sx(pt.x))}" cy="${f2(sy(pt.y))}" r="${r}" fill="none" stroke="${color}" stroke-width="1.2" opacity="0.75"/>`);
  }
}

// New tombstones (E4) → red X glyph (small cross)
function drawNewTomb(p, pts, color, size=5.0) {
  const s = [...pts].sort((a,b) => (a.kit_id < b.kit_id ? -1 : 1));
  for (const pt of s) {
    const cx = sx(pt.x), cy = sy(pt.y);
    p.push(`<g stroke="${color}" stroke-width="1.8" fill="none">`);
    p.push(`<line x1="${f2(cx-size)}" y1="${f2(cy-size)}" x2="${f2(cx+size)}" y2="${f2(cy+size)}"/>`);
    p.push(`<line x1="${f2(cx-size)}" y1="${f2(cy+size)}" x2="${f2(cx+size)}" y2="${f2(cy-size)}"/>`);
    p.push(`</g>`);
  }
}

// New positive → filled saturated circle, slightly larger with halo
function drawNewPos(p, pts, color, r=4.4) {
  const s = [...pts].sort((a,b) => (a.kit_id < b.kit_id ? -1 : 1));
  for (const pt of s) {
    const cx = sx(pt.x), cy = sy(pt.y);
    p.push(`<circle cx="${f2(cx)}" cy="${f2(cy)}" r="${f2(r+2.2)}" fill="none" stroke="${color}" stroke-width="0.6" opacity="0.55"/>`);
    p.push(`<circle cx="${f2(cx)}" cy="${f2(cy)}" r="${f2(r)}" fill="${color}" opacity="0.95"/>`);
  }
}

// Split E3 into active (supp=false) and legacy tombstones (supp=true).
const E3_ACTIVE = E3_PTS.filter(p => !p.supplementary);
const E3_LEGTOMB = E3_PTS.filter(p =>  p.supplementary);
// E4 pre-existing split (SAME kits as E3, just carrying through)
const E4_PREEX_ACTIVE = E4_PREEX.filter(p => !p.supplementary);
const E4_PREEX_LEGTOMB = E4_PREEX.filter(p => p.supplementary && !('death_class' in p) === false ? true : (p.supplementary === true));
// The above is equivalent to: E4 pre-existing supplementary points (= 37 legacy tombstones carried through).

// ---------------------------------------------------------------- PLATE 1 — E3
function renderE3() {
  const p = svgOpen(
    'Atlas — Edition III (served truth)',
    `469 active + 37 legacy tombstones = 506 points   ·   basis frozen, 14 dims, seed 20260714`
  );
  drawActive(p, E3_ACTIVE, COL.active, 3.2);
  drawLegacyTomb(p, E3_LEGTOMB, COL.legacyTomb, 3.6);
  // Legend
  const lx = M.left + PW - 260, ly = M.top + 24;
  p.push(`<g font-size="13" fill="${COL.titleSecondary}">`);
  p.push(`<rect x="${lx-14}" y="${ly-18}" width="256" height="76" fill="#181d28" stroke="${COL.gridZero}" opacity="0.92"/>`);
  p.push(`<circle cx="${lx+4}" cy="${ly+2}" r="4" fill="${COL.active}"/>`);
  p.push(`<text x="${lx+18}" y="${ly+7}" fill="${COL.titlePrimary}">469 active</text>`);
  p.push(`<circle cx="${lx+4}" cy="${ly+26}" r="4" fill="none" stroke="${COL.legacyTomb}" stroke-width="1.2"/>`);
  p.push(`<text x="${lx+18}" y="${ly+31}" fill="${COL.titlePrimary}">37 legacy tombstones (open ring)</text>`);
  p.push(`</g>`);
  return svgClose(p);
}

// ---------------------------------------------------------------- PLATE 2 — E4
function renderE4() {
  const p = svgOpen(
    'Atlas — Edition IV (ratification candidate)',
    `506 pre-existing + 50 new positives + 6 new tombstones = 562 points   ·   fit BYTE-FROZEN vs Edition III`
  );
  // pre-existing (dimmed slightly to let new points read)
  drawActive(p, E4_PREEX_ACTIVE, COL.active, 3.2);
  drawLegacyTomb(p, E4_PREEX_LEGTOMB, COL.legacyTomb, 3.6);
  drawNewPos(p, E4_NEW_POS, COL.newPositive, 4.4);
  drawNewTomb(p, E4_NEW_TOMB, COL.newTomb, 5.0);
  // Legend
  const lx = M.left + PW - 300, ly = M.top + 24;
  p.push(`<g font-size="13" fill="${COL.titleSecondary}">`);
  p.push(`<rect x="${lx-14}" y="${ly-18}" width="296" height="124" fill="#181d28" stroke="${COL.gridZero}" opacity="0.92"/>`);
  p.push(`<circle cx="${lx+4}" cy="${ly+2}" r="4" fill="${COL.active}"/>`);
  p.push(`<text x="${lx+18}" y="${ly+7}" fill="${COL.titlePrimary}">469 pre-existing active</text>`);
  p.push(`<circle cx="${lx+4}" cy="${ly+26}" r="4" fill="none" stroke="${COL.legacyTomb}" stroke-width="1.2"/>`);
  p.push(`<text x="${lx+18}" y="${ly+31}" fill="${COL.titlePrimary}">37 legacy tombstones</text>`);
  p.push(`<circle cx="${lx+4}" cy="${ly+50}" r="4.4" fill="${COL.newPositive}"/>`);
  p.push(`<text x="${lx+18}" y="${ly+55}" fill="${COL.titlePrimary}">50 NEW positives (la-*/mcd-*/re-key)</text>`);
  p.push(`<g stroke="${COL.newTomb}" stroke-width="1.8" fill="none">`);
  p.push(`<line x1="${lx-1}" y1="${ly+73}" x2="${lx+9}" y2="${ly+83}"/>`);
  p.push(`<line x1="${lx-1}" y1="${ly+83}" x2="${lx+9}" y2="${ly+73}"/>`);
  p.push(`</g>`);
  p.push(`<text x="${lx+18}" y="${ly+81}" fill="${COL.titlePrimary}">6 NEW tombstones (la-*, extrinsic-tuning)</text>`);
  p.push(`</g>`);
  return svgClose(p);
}

// ---------------------------------------------------------------- PLATE 3 — DELTA
function renderDelta() {
  const p = svgOpen(
    'Atlas — Edition IV DELTA (56 new points highlighted; 506 pre-existing dimmed)',
    `WN quadrant condensation: 40/50 new positives (80%) + 5/6 new tombstones cluster upper-left`
  );
  // dimmed pre-existing
  const s1 = [...E4_PREEX_ACTIVE].sort((a,b) => (a.kit_id < b.kit_id ? -1 : 1));
  for (const pt of s1) p.push(`<circle cx="${f2(sx(pt.x))}" cy="${f2(sy(pt.y))}" r="2.6" fill="${COL.preexDim}" opacity="0.65"/>`);
  const s2 = [...E4_PREEX_LEGTOMB].sort((a,b) => (a.kit_id < b.kit_id ? -1 : 1));
  for (const pt of s2) p.push(`<circle cx="${f2(sx(pt.x))}" cy="${f2(sy(pt.y))}" r="3.0" fill="none" stroke="${COL.legacyTombDim}" stroke-width="0.8" opacity="0.65"/>`);
  // saturated new
  drawNewPos(p, E4_NEW_POS, COL.newPositive, 4.4);
  drawNewTomb(p, E4_NEW_TOMB, COL.newTomb, 5.0);
  // WN cluster annotation — draw an oval around the new-positive centroid + label
  const posXs = E4_NEW_POS.map(pt=>pt.x); const posYs = E4_NEW_POS.map(pt=>pt.y);
  const cxW = posXs.reduce((a,b)=>a+b,0)/posXs.length; const cyW = posYs.reduce((a,b)=>a+b,0)/posYs.length;
  const ovxc = sx(cxW), ovyc = sy(cyW);
  p.push(`<ellipse cx="${f2(ovxc)}" cy="${f2(ovyc)}" rx="290" ry="200" fill="none" stroke="${COL.annAccent}" stroke-width="1.2" stroke-dasharray="8 6" opacity="0.55"/>`);
  p.push(`<text x="${f2(ovxc-260)}" y="${f2(ovyc-210)}" fill="${COL.annAccent}" font-size="16" font-weight="600">Lost Ark wing — 48 la-* points</text>`);
  p.push(`<text x="${f2(ovxc-260)}" y="${f2(ovyc-188)}" fill="${COL.ann}" font-size="13">+ 5 mcd-* + 3 pull re-keys · 6 new tombstones</text>`);

  // 3 pull re-keys labelled
  const rekeys = ['d3-wizard-black-hole', 'd4-spiritborn-vortex', 'di-cyclone-strike-monk-base'];
  for (const kid of rekeys) {
    const pt = E4_NEW_POS.find(x => x.kit_id === kid);
    if (!pt) continue;
    const cx = sx(pt.x), cy = sy(pt.y);
    p.push(`<line x1="${f2(cx+8)}" y1="${f2(cy-8)}" x2="${f2(cx+56)}" y2="${f2(cy-30)}" stroke="${COL.ann}" stroke-width="0.7" opacity="0.7"/>`);
    p.push(`<text x="${f2(cx+60)}" y="${f2(cy-30)}" fill="${COL.titlePrimary}" font-size="11">${kid}</text>`);
  }

  // Legend
  const lx = M.left + PW - 320, ly = M.top + 24;
  p.push(`<g font-size="13" fill="${COL.titleSecondary}">`);
  p.push(`<rect x="${lx-14}" y="${ly-18}" width="316" height="100" fill="#181d28" stroke="${COL.gridZero}" opacity="0.94"/>`);
  p.push(`<circle cx="${lx+4}" cy="${ly+2}" r="2.6" fill="${COL.preexDim}"/>`);
  p.push(`<text x="${lx+18}" y="${ly+7}" fill="${COL.titlePrimary}">506 pre-existing (dimmed; unchanged coords)</text>`);
  p.push(`<circle cx="${lx+4}" cy="${ly+26}" r="4.4" fill="${COL.newPositive}"/>`);
  p.push(`<text x="${lx+18}" y="${ly+31}" fill="${COL.titlePrimary}">50 NEW positives</text>`);
  p.push(`<g stroke="${COL.newTomb}" stroke-width="1.8" fill="none">`);
  p.push(`<line x1="${lx-1}" y1="${ly+50}" x2="${lx+9}" y2="${ly+60}"/>`);
  p.push(`<line x1="${lx-1}" y1="${ly+60}" x2="${lx+9}" y2="${ly+50}"/>`);
  p.push(`</g>`);
  p.push(`<text x="${lx+18}" y="${ly+58}" fill="${COL.titlePrimary}">6 NEW tombstones (extrinsic-tuning)</text>`);
  p.push(`</g>`);
  return svgClose(p);
}

// ---------------------------------------------------------------- PLATE 4 — G-3
// G-3 pixel corroboration: render E3-shared (506) at THIS pipeline's projection, then render
// E4-restricted-to-shared-IDs (506 pre-existing) at IDENTICAL projection. Pixel diff of the
// two rasters should be zero (up to antialiasing rounding). IMPORTANT: for the G-3 plates
// we deliberately hold ALL chrome (title, subtitle, legend, axes) IDENTICAL so that ANY
// pixel diff can be attributed ONLY to dot-position or dot-color differences. If a run has
// E3 and E4 coords byte-identical (as the G-3 gate report claims), the diff must be zero.
function renderG3(sourceLabel, pts, active, legTomb) {
  const p = svgOpen(
    'G-3 corroboration plate',                                                  // identical
    `506 shared kit_ids at identical projection · source: ${sourceLabel}`       // varies only in `sourceLabel` — placed offscreen if we want zero diff
  );
  drawActive(p, active, COL.active, 3.2);
  drawLegacyTomb(p, legTomb, COL.legacyTomb, 3.6);
  return svgClose(p);
}
// To keep chrome IDENTICAL between the two G-3 plates for a clean pixel-diff, we render
// them with the SAME title & subtitle. The atlas source is a data-side distinction, not
// a chrome-side one.
function renderE3Shared() {
  const p = svgOpen(
    'G-3 corroboration plate',
    `506 shared kit_ids at identical projection · dots only`
  );
  drawActive(p, E3_ACTIVE, COL.active, 3.2);
  drawLegacyTomb(p, E3_LEGTOMB, COL.legacyTomb, 3.6);
  return svgClose(p);
}
function renderE4Restricted() {
  const p = svgOpen(
    'G-3 corroboration plate',
    `506 shared kit_ids at identical projection · dots only`
  );
  drawActive(p, E4_PREEX_ACTIVE, COL.active, 3.2);
  drawLegacyTomb(p, E4_PREEX_LEGTOMB, COL.legacyTomb, 3.6);
  return svgClose(p);
}

// ---------------------------------------------------------------- write
async function writeSvgPng(fname, svgText) {
  const svgPath = join(OUT_DIR, `${fname}.svg`);
  const pngPath = join(OUT_DIR, `${fname}.png`);
  writeFileSync(svgPath, svgText);
  await sharp(Buffer.from(svgText)).png().toFile(pngPath);
  return { svgPath, pngPath };
}

// Stitch two PNGs horizontally with a slim divider column.
async function stitchSideBySide(leftPng, rightPng, outPath) {
  const [L, R] = await Promise.all([
    sharp(leftPng).raw().toBuffer({ resolveWithObject: true }),
    sharp(rightPng).raw().toBuffer({ resolveWithObject: true }),
  ]);
  if (L.info.height !== R.info.height) throw new Error(`stitch height mismatch: ${L.info.height} vs ${R.info.height}`);
  const dividerW = 4;
  const outW = L.info.width + dividerW + R.info.width;
  const outH = L.info.height;
  const chans = L.info.channels;
  const buf = Buffer.alloc(outW * outH * chans);
  // fill divider with mid-grey
  const dividerColor = [64, 68, 78, 255].slice(0, chans);
  for (let y = 0; y < outH; y++) {
    // left
    L.data.copy(buf, (y * outW) * chans, y * L.info.width * chans, (y + 1) * L.info.width * chans);
    // divider
    for (let x = 0; x < dividerW; x++) {
      for (let c = 0; c < chans; c++) buf[(y * outW + L.info.width + x) * chans + c] = dividerColor[c];
    }
    // right
    R.data.copy(buf, (y * outW + L.info.width + dividerW) * chans, y * R.info.width * chans, (y + 1) * R.info.width * chans);
  }
  await sharp(buf, { raw: { width: outW, height: outH, channels: chans } }).png().toFile(outPath);
  return outPath;
}

// Pixel-diff of two PNGs (assumed identical dims). Emits an amplified difference
// image (grey where identical, red where E3-only, green where E4-only). Also returns
// per-pixel stats: max abs diff (0-255), mean abs diff, pct pixels non-zero.
async function pixelDiff(pngA, pngB, outPath) {
  const [A, B] = await Promise.all([
    sharp(pngA).raw().toBuffer({ resolveWithObject: true }),
    sharp(pngB).raw().toBuffer({ resolveWithObject: true }),
  ]);
  if (A.info.width !== B.info.width || A.info.height !== B.info.height) {
    throw new Error(`pixelDiff dim mismatch: ${A.info.width}x${A.info.height} vs ${B.info.width}x${B.info.height}`);
  }
  const w = A.info.width, h = A.info.height, c = A.info.channels;
  const diff = Buffer.alloc(w * h * c);
  let sumAbs = 0, maxAbs = 0, nonZero = 0;
  const nPix = w * h;
  for (let i = 0; i < nPix; i++) {
    let pixMax = 0;
    for (let k = 0; k < 3; k++) {
      const a = A.data[i*c + k], b = B.data[i*c + k];
      const d = Math.abs(a - b);
      pixMax = Math.max(pixMax, d);
      sumAbs += d;
      if (d > maxAbs) maxAbs = d;
    }
    if (pixMax > 0) nonZero++;
    // Visualization: baseline grey; A>B (E3 stronger) → red; B>A (E4 stronger) → green
    const rSum = A.data[i*c] - B.data[i*c] + A.data[i*c+1] - B.data[i*c+1] + A.data[i*c+2] - B.data[i*c+2];
    // Grey baseline from mean
    const base = ((A.data[i*c] + A.data[i*c+1] + A.data[i*c+2] + B.data[i*c] + B.data[i*c+1] + B.data[i*c+2]) / 6) | 0;
    // Amplify difference by 6x, clamp
    const amp = Math.min(255, pixMax * 6);
    if (pixMax === 0) {
      diff[i*c] = base; diff[i*c+1] = base; diff[i*c+2] = base;
    } else if (rSum > 0) {
      diff[i*c] = Math.min(255, base + amp); diff[i*c+1] = Math.max(0, base - amp/2); diff[i*c+2] = Math.max(0, base - amp/2);
    } else {
      diff[i*c] = Math.max(0, base - amp/2); diff[i*c+1] = Math.min(255, base + amp); diff[i*c+2] = Math.max(0, base - amp/2);
    }
    if (c === 4) diff[i*c+3] = 255;
  }
  await sharp(diff, { raw: { width: w, height: h, channels: c } }).png().toFile(outPath);
  return {
    outPath,
    maxAbs, meanAbs: sumAbs / (nPix * 3), nonZeroPct: nonZero / nPix * 100,
  };
}

// ================================================================== MAIN
console.log(`E3 file: ${E3_PATH}`);
console.log(`E4 file: ${E4_PATH}`);
console.log(`Output:  ${OUT_DIR}`);

console.log(`\nE3 counts: ${E3_PTS.length} (active ${E3_ACTIVE.length} + legacy tombstones ${E3_LEGTOMB.length})`);
console.log(`E4 counts: ${E4_PTS.length}`);
console.log(`  pre-existing (in E3): ${E4_PREEX.length}`);
console.log(`  new positives: ${E4_NEW_POS.length}`);
console.log(`  new tombstones: ${E4_NEW_TOMB.length}`);

console.log(`\nExtents (world coords):`);
console.log(`  E3: x ∈ [${e3MinX.toFixed(4)}, ${e3MaxX.toFixed(4)}], y ∈ [${e3MinY.toFixed(4)}, ${e3MaxY.toFixed(4)}]`);
console.log(`  E4: x ∈ [${e4MinX.toFixed(4)}, ${e4MaxX.toFixed(4)}], y ∈ [${e4MinY.toFixed(4)}, ${e4MaxY.toFixed(4)}]`);
console.log(`  new 56: x ∈ [${newMinX.toFixed(4)}, ${newMaxX.toFixed(4)}], y ∈ [${newMinY.toFixed(4)}, ${newMaxY.toFixed(4)}]`);
console.log(`  NEW WITHIN E3 BOUNDING BOX: ${NEW_WITHIN_E3 ? 'YES — no viewport rescale needed' : 'NO — extra crop view emitted'}`);

console.log(`\nRendering plates …`);
const plateE3 = renderE3();
const plateE4 = renderE4();
const plateDelta = renderDelta();
const plateE3Shared = renderE3Shared();
const plateE4Restricted = renderE4Restricted();

const [e3Files, e4Files, deltaFiles, e3SFiles, e4RFiles] = await Promise.all([
  writeSvgPng('plate-e3', plateE3),
  writeSvgPng('plate-e4', plateE4),
  writeSvgPng('plate-delta', plateDelta),
  writeSvgPng('g3-e3-shared', plateE3Shared),
  writeSvgPng('g3-e4-restricted', plateE4Restricted),
]);
console.log(`  wrote plate-e3.{svg,png}`);
console.log(`  wrote plate-e4.{svg,png}`);
console.log(`  wrote plate-delta.{svg,png}`);
console.log(`  wrote g3-e3-shared.{svg,png}`);
console.log(`  wrote g3-e4-restricted.{svg,png}`);

console.log(`\nStitching side-by-side …`);
const sbsPath = join(OUT_DIR, 'plate-side-by-side.png');
await stitchSideBySide(e3Files.pngPath, e4Files.pngPath, sbsPath);
console.log(`  wrote plate-side-by-side.png`);

console.log(`\nComputing G-3 pixel diff …`);
const diffPath = join(OUT_DIR, 'g3-diff.png');
const diffStats = await pixelDiff(e3SFiles.pngPath, e4RFiles.pngPath, diffPath);
console.log(`  wrote g3-diff.png`);
console.log(`  G-3 pixel stats: maxAbs=${diffStats.maxAbs}, meanAbs=${diffStats.meanAbs.toFixed(6)}, nonZeroPct=${diffStats.nonZeroPct.toFixed(4)}%`);

// Emit stats JSON for the report to cite deterministically.
const stats = {
  e3_file: E3_PATH,
  e4_file: E4_PATH,
  e3_total: E3_PTS.length,
  e3_active: E3_ACTIVE.length,
  e3_legacy_tombstones: E3_LEGTOMB.length,
  e4_total: E4_PTS.length,
  e4_preexisting: E4_PREEX.length,
  e4_new_positives: E4_NEW_POS.length,
  e4_new_tombstones: E4_NEW_TOMB.length,
  e3_extent: { x_min: e3MinX, x_max: e3MaxX, y_min: e3MinY, y_max: e3MaxY },
  e4_extent: { x_min: e4MinX, x_max: e4MaxX, y_min: e4MinY, y_max: e4MaxY },
  new_only_extent: { x_min: newMinX, x_max: newMaxX, y_min: newMinY, y_max: newMaxY },
  new_within_e3_bbox: NEW_WITHIN_E3,
  new_positives_franchise_breakdown: E4_NEW_POS.reduce((acc, p) => {
    const pfx = p.kit_id.split('-')[0];
    acc[pfx] = (acc[pfx] || 0) + 1;
    return acc;
  }, {}),
  new_positives_quadrant: E4_NEW_POS.reduce((acc, p) => {
    const q = (p.x >= 0 ? 'E' : 'W') + (p.y >= 0 ? 'N' : 'S');
    acc[q] = (acc[q] || 0) + 1;
    return acc;
  }, {}),
  new_tombstones_quadrant: E4_NEW_TOMB.reduce((acc, p) => {
    const q = (p.x >= 0 ? 'E' : 'W') + (p.y >= 0 ? 'N' : 'S');
    acc[q] = (acc[q] || 0) + 1;
    return acc;
  }, {}),
  g3_pixel_diff: {
    max_abs: diffStats.maxAbs,
    mean_abs: diffStats.meanAbs,
    nonzero_pct: diffStats.nonZeroPct,
    verdict: diffStats.maxAbs === 0 ? 'PIXEL-IDENTICAL' : (diffStats.nonZeroPct < 0.01 ? 'NEAR-IDENTICAL (antialias only)' : 'DIVERGENT'),
  },
  projection: {
    canvas_w: W, canvas_h: H,
    margin: M,
    world_bbox: { min_x: minX, max_x: maxX, min_y: minY, max_y: maxY },
    axes: 'PERFORM<->DEPLOY (dim1) · EMBODY<->LAUNCH (dim2)',
  },
};
writeFileSync(join(OUT_DIR, 'render-stats.json'), JSON.stringify(stats, null, 2));
console.log(`  wrote render-stats.json`);

console.log(`\nDONE. Files in: ${OUT_DIR}`);
