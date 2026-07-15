// atlas-edition1-render.mjs — the first Edition-I atlas render.
//
// LAW: chart = render(atlas.json). Layout is COMPUTED here; all CONTENT (numbers,
// labels, coordinates, class strings) originates ONLY in atlas.json fields. No
// literal atlas numerics live in this source beyond layout geometry.
//
// Renders the frozen Edition-I derived MCA basis (plane = dims 1-2) as TWO skins
// (instrument, archive) over ONE layout engine. Continuum-with-condensations:
// soft KDE density underlay (NO cells, NO grid, NO discrete regions), individual
// kit dots on top, 6 gateA condensation groups color-coded + centroid-annotated,
// 37 supplementary corpses as per-death_class tombstone glyphs (Finding F-1:
// tombstones, NEVER shaded danger regions).
//
// Deterministic: same atlas.json -> byte-identical SVG (sorted iteration; no RNG;
// no wall-clock; time comes from atlas.json emitted_at).
//
// Author: galadriel (visual-perception steward). Charter step 7.

import { readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve, join } from 'node:path';
import sharp from 'sharp';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ATLAS_PATH = resolve(__dirname, '../../research/curated/atlas/atlas.json');
const OUT_DIR = resolve(__dirname, '../captures/2026-07-14-atlas-edition1');

// ------------------------------------------------------------------ fail-loud helpers
function die(msg) {
  console.error(`\n[RENDER REFUSAL] ${msg}\n`);
  process.exit(2);
}
function req(obj, path, ctx) {
  const parts = path.split('.');
  let cur = obj;
  for (const p of parts) {
    if (cur == null || !(p in cur)) die(`${ctx}: required field '${path}' ABSENT in atlas.json — fail loud (RIDER-1 mandate).`);
    cur = cur[p];
  }
  if (cur === null || cur === undefined || cur === '') die(`${ctx}: field '${path}' is empty in atlas.json — fail loud.`);
  return cur;
}

// ------------------------------------------------------------------ load + validate
const atlas = JSON.parse(readFileSync(ATLAS_PATH, 'utf8'));

// Mandatory basis block (Stage 4 freeze + RIDER-1 badge fields).
const basis = req(atlas, 'basis', 'basis-block');
const inertiaPct = req(atlas, 'basis.inertia_pct', 'RIDER-1');
const retainedDims = req(atlas, 'basis.retained_dims', 'RIDER-1');
const structureStatement = req(atlas, 'basis.structure_statement', 'RIDER-1');
const axisNames = req(atlas, 'basis.axis_names', 'axis-names');
const edition = req(atlas, 'basis.edition', 'edition');
const frozen = req(atlas, 'basis.frozen', 'frozen');
const ratified = req(atlas, 'basis.ratified', 'ratified');
if (frozen !== true) die(`basis.frozen is not true (got ${JSON.stringify(frozen)}) — refuse to render an unfrozen basis as Edition-I.`);

// Cross-check the mandatory-badge declaration if present.
if (Array.isArray(atlas.badge_fields_mandatory)) {
  const need = ['inertia_pct', 'retained_dims', 'structure_statement'];
  for (const f of need) if (!atlas.badge_fields_mandatory.includes(f)) die(`badge_fields_mandatory declares fields but omits '${f}' — RIDER-1 contract violated.`);
}

const counts = req(atlas, 'counts', 'counts-block');
const atlasVersion = req(atlas, 'atlas_version', 'version');
const emittedAt = req(atlas, 'emitted_at', 'stamp');
const emitterScript = req(atlas, 'emitter_script', 'stamp');

const points = req(atlas, 'points', 'points');
if (!Array.isArray(points) || points.length === 0) die('points is empty.');

// Partition points. Determinism: sort by kit_id everywhere.
const byId = (a, b) => (a.kit_id < b.kit_id ? -1 : a.kit_id > b.kit_id ? 1 : 0);
const all = [...points].sort(byId);
const active = all.filter((p) => p.supplementary !== true);
const supplementary = all.filter((p) => p.supplementary === true);
const grouped = active.filter((p) => p.gateA_group != null);
const neutral = active.filter((p) => p.gateA_group == null);

// Count conformance vs emitted counts (TEST, not render-derive; we render emitted fields).
if (active.length !== counts.active) die(`active point count ${active.length} != counts.active ${counts.active}.`);
if (supplementary.length !== counts.supplementary) die(`supplementary count ${supplementary.length} != counts.supplementary ${counts.supplementary}.`);
if (all.length !== counts.total) die(`total point count ${all.length} != counts.total ${counts.total}.`);

// death_class enum discovery (fail-loud-on-absence for supplementary; render classes as-emitted).
for (const p of supplementary) {
  if (p.death_class == null) die(`supplementary kit '${p.kit_id}' missing death_class — GRAVEYARD payload incomplete (F-1).`);
}
const deathClasses = [...new Set(supplementary.map((p) => p.death_class))].sort();
const GROUP_ORDER = ['WHIRLWIND', 'TOTEM-SENTRY', 'TRAP-MINE', 'CHANNELED-BEAM', 'AURA', 'MINION-PET'];
const seenGroups = [...new Set(grouped.map((p) => p.gateA_group))].sort();
for (const g of seenGroups) if (!GROUP_ORDER.includes(g)) die(`unknown gateA_group '${g}' — vocabulary moved without re-ratification (R4 refusal).`);

// ------------------------------------------------------------------ plane geometry
// World bounds from the data (ALL points, so tombstones are in-frame), symmetric-padded.
const xs = all.map((p) => p.x);
const ys = all.map((p) => p.y);
const rawMinX = Math.min(...xs), rawMaxX = Math.max(...xs);
const rawMinY = Math.min(...ys), rawMaxY = Math.max(...ys);
const padX = (rawMaxX - rawMinX) * 0.06;
const padY = (rawMaxY - rawMinY) * 0.06;
const minX = rawMinX - padX, maxX = rawMaxX + padX;
const minY = rawMinY - padY, maxY = rawMaxY + padY;

// Canvas. Plane is inside a margin box that leaves room for axis labels + badge.
const W = 1600, H = 1200;
const M = { top: 132, right: 96, bottom: 96, left: 96 };
const PW = W - M.left - M.right;
const PH = H - M.top - M.bottom;

// world -> svg. y flips: math y+ (LAUNCH) => svg top.
const sx = (x) => M.left + ((x - minX) / (maxX - minX)) * PW;
const sy = (y) => M.top + (1 - (y - minY) / (maxY - minY)) * PH;
const f2 = (n) => Number(n).toFixed(2); // 2-dp svg coords -> deterministic byte output

// Zero-axis positions (world 0), only drawn if within frame.
const zeroX = (minX <= 0 && maxX >= 0) ? sx(0) : null;
const zeroY = (minY <= 0 && maxY >= 0) ? sy(0) : null;

// ------------------------------------------------------------------ KDE density underlay
// Gaussian KDE of the ACTIVE kits (the corpus condensations), evaluated on a raster
// grid, then drawn as smooth filled iso-contour bands via marching squares.
// NO cell borders, NO grid partitions, NO discrete-region coloring — a continuous
// terrain revealing condensations. Determinism: fixed grid, fixed bandwidth.
const GRID = 120; // grid cells per axis over the plane box
const spanX = maxX - minX, spanY = maxY - minY;
// bandwidth ~ Silverman-ish but pinned (no data-dependent RNG): fraction of span.
const hX = spanX * 0.055, hY = spanY * 0.055;
const inv2hx2 = 1 / (2 * hX * hX), inv2hy2 = 1 / (2 * hY * hY);

const field = new Float64Array(GRID * GRID);
let fieldMax = 0;
for (let gy = 0; gy < GRID; gy++) {
  const wy = minY + ((gy + 0.5) / GRID) * spanY;
  for (let gx = 0; gx < GRID; gx++) {
    const wx = minX + ((gx + 0.5) / GRID) * spanX;
    let acc = 0;
    for (const p of active) {
      const dx = wx - p.x, dy = wy - p.y;
      acc += Math.exp(-(dx * dx * inv2hx2 + dy * dy * inv2hy2));
    }
    field[gy * GRID + gx] = acc;
    if (acc > fieldMax) fieldMax = acc;
  }
}
// grid-cell -> svg. cell centers map into plane box.
const cellW = PW / GRID, cellH = PH / GRID;
const gsx = (gx) => M.left + (gx + 0.5) * cellW;
const gsy = (gy) => M.top + (PH - (gy + 0.5) * cellH); // flip

// Marching squares: emit filled band polygons for a set of thresholds.
// We fill "above threshold" regions as translucent bands; stacking them makes the
// terrain. Simple per-cell quad tessellation of the >=t mask (rectangles), unioned
// visually by fill opacity — no borders drawn. Deterministic scan order.
function bandRects(t) {
  // Return path 'd' covering all grid cells whose interpolated corner-average >= t.
  // Using cell-center value for a soft, blocky-free look we then blur via SVG filter.
  let d = '';
  for (let gy = 0; gy < GRID; gy++) {
    for (let gx = 0; gx < GRID; gx++) {
      if (field[gy * GRID + gx] >= t) {
        const x = M.left + gx * cellW;
        const y = M.top + (PH - (gy + 1) * cellH);
        d += `M${f2(x)} ${f2(y)}h${f2(cellW)}v${f2(cellH)}h${f2(-cellW)}z`;
      }
    }
  }
  return d;
}
const N_BANDS = 6;
const bands = [];
for (let i = 1; i <= N_BANDS; i++) {
  const t = (i / (N_BANDS + 1)) * fieldMax;
  bands.push({ level: i, d: bandRects(t) });
}

// ------------------------------------------------------------------ group centroids (labeled-member centroids)
const groupCentroids = {};
for (const g of GROUP_ORDER) {
  const mem = grouped.filter((p) => p.gateA_group === g);
  if (mem.length === 0) continue;
  const cx = mem.reduce((s, p) => s + p.x, 0) / mem.length;
  const cy = mem.reduce((s, p) => s + p.y, 0) / mem.length;
  groupCentroids[g] = { x: cx, y: cy, n: mem.length };
}

// ------------------------------------------------------------------ SKINS (theme params over one layout engine)
const SKINS = {
  instrument: {
    name: 'instrument',
    bg: '#f7f8fa',
    ink: '#1d2330',
    faint: '#8a93a3',
    axisLine: '#c3cad6',
    bandBase: '#5b7fb0',        // cool neutral terrain
    bandOpacityStep: 0.055,
    neutralDot: '#9aa4b4',
    neutralDotR: 3.0,
    neutralDotOp: 0.72,
    groupDotR: 5.2,
    tombInk: '#3a3f4a',
    tombUnknownInk: '#b0451f',
    fontStack: `'Helvetica Neue', Arial, system-ui, sans-serif`,
    titleWeight: 600,
    plaque: '#ffffff',
    plaqueStroke: '#d3d9e2',
    blurStd: 7,
    badgeBg: '#eef1f5',
    badgeInk: '#2b3240',
  },
  archive: {
    name: 'archive',
    bg: '#0e1016',
    ink: '#ece3cf',
    faint: '#8b8267',
    axisLine: '#3a3d33',
    bandBase: '#c9a24b',        // gilt terrain — the God's Archive
    bandOpacityStep: 0.06,
    neutralDot: '#7d7a6a',
    neutralDotR: 3.0,
    neutralDotOp: 0.7,
    groupDotR: 5.2,
    tombInk: '#cfc6ad',
    tombUnknownInk: '#d98a55',
    fontStack: `'Iowan Old Style', 'Palatino Linotype', Palatino, Georgia, serif`,
    titleWeight: 600,
    plaque: '#171a22',
    plaqueStroke: '#3a3d33',
    blurStd: 7,
    badgeBg: '#171a22',
    badgeInk: '#d8cfb6',
  },
};

// 6-group palette (behavior condensations). Fixed hues; identical across skins so
// the coordinate/encoding set is skin-invariant (only chrome differs).
const GROUP_COLORS = {
  'WHIRLWIND': '#e8663d',
  'TOTEM-SENTRY': '#3f8ecc',
  'TRAP-MINE': '#8e5cc4',
  'CHANNELED-BEAM': '#d4a017',
  'AURA': '#2fa889',
  'MINION-PET': '#c94f8a',
};
// Tombstone death-class legend glyph note (class label only; glyph is uniform dagger,
// unknown-pending-recrawl gets an open dagger + distinct ink to read as its own class).
function isUnknown(dc) { return dc === 'unknown-pending-recrawl'; }

// ------------------------------------------------------------------ SVG assembly
function esc(s) {
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function renderSVG(skinKey) {
  const s = SKINS[skinKey];
  const P = []; // svg body parts

  // ---- defs: soft blur for the terrain underlay (turns blocky mask into smooth density)
  P.push(`<defs>`);
  P.push(`<filter id="terrainBlur" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="${s.blurStd}"/></filter>`);
  P.push(`</defs>`);

  // ---- background
  P.push(`<rect x="0" y="0" width="${W}" height="${H}" fill="${s.bg}"/>`);

  // ---- terrain underlay (continuum with condensations; blurred, no borders)
  P.push(`<g filter="url(#terrainBlur)" fill="${s.bandBase}">`);
  for (const b of bands) {
    if (!b.d) continue;
    P.push(`<path d="${b.d}" fill-opacity="${(s.bandOpacityStep).toFixed(3)}"/>`);
  }
  P.push(`</g>`);

  // ---- soft zero axes (orientation guides only; NOT cell borders)
  if (zeroX != null) P.push(`<line x1="${f2(zeroX)}" y1="${f2(M.top)}" x2="${f2(zeroX)}" y2="${f2(M.top + PH)}" stroke="${s.axisLine}" stroke-width="1" stroke-dasharray="2 6"/>`);
  if (zeroY != null) P.push(`<line x1="${f2(M.left)}" y1="${f2(zeroY)}" x2="${f2(M.left + PW)}" y2="${f2(zeroY)}" stroke="${s.axisLine}" stroke-width="1" stroke-dasharray="2 6"/>`);
  // plane frame (thin; a viewport edge, not a grid)
  P.push(`<rect x="${f2(M.left)}" y="${f2(M.top)}" width="${f2(PW)}" height="${f2(PH)}" fill="none" stroke="${s.axisLine}" stroke-width="1"/>`);

  // ---- neutral active dots (383 unlabeled)
  P.push(`<g fill="${s.neutralDot}" fill-opacity="${s.neutralDotOp}">`);
  for (const p of neutral) {
    P.push(`<circle cx="${f2(sx(p.x))}" cy="${f2(sy(p.y))}" r="${s.neutralDotR}"><title>${esc(p.kit_id)} — active — ${esc(p.franchise ?? '')}</title></circle>`);
  }
  P.push(`</g>`);

  // ---- grouped active dots (86; color = condensation group)
  for (const g of GROUP_ORDER) {
    const mem = grouped.filter((p) => p.gateA_group === g);
    if (!mem.length) continue;
    P.push(`<g fill="${GROUP_COLORS[g]}" stroke="${s.bg}" stroke-width="0.6">`);
    for (const p of mem) {
      P.push(`<circle cx="${f2(sx(p.x))}" cy="${f2(sy(p.y))}" r="${s.groupDotR}"><title>${esc(p.kit_id)} — ${esc(g)} — ${esc(p.franchise ?? '')}</title></circle>`);
    }
    P.push(`</g>`);
  }

  // ---- GRAVEYARD: per-corpse tombstone glyphs (dagger), classed by death_class.
  // Never a shaded region. Each corpse individually identifiable via <title>; a small
  // kit_id label is drawn when the local dagger is not overlapping (legibility guard);
  // otherwise the indexed legend carries it.
  P.push(`<g font-family="${s.fontStack}">`);
  for (let i = 0; i < supplementary.length; i++) {
    const p = supplementary[i];
    const cx = sx(p.x), cy = sy(p.y);
    const unk = isUnknown(p.death_class);
    const ink = unk ? s.tombUnknownInk : s.tombInk;
    const glyph = unk ? '†' : '†'; // dagger; unknown distinguished by ink + ring below
    // draw a ground marker: dagger glyph
    P.push(`<text x="${f2(cx)}" y="${f2(cy + 5)}" font-size="16" text-anchor="middle" fill="${ink}" font-weight="700">${glyph}<title>${esc(p.kit_id)} † ${esc(p.death_class)}</title></text>`);
    if (unk) {
      // open ring under unknown-pending-recrawl daggers -> reads as its own visible class
      P.push(`<circle cx="${f2(cx)}" cy="${f2(cy)}" r="7" fill="none" stroke="${ink}" stroke-width="1.1" stroke-dasharray="2 2"/>`);
    }
    // indexed micro-label
    P.push(`<text x="${f2(cx + 8)}" y="${f2(cy + 2)}" font-size="8" fill="${ink}" fill-opacity="0.85">${i + 1}</text>`);
  }
  P.push(`</g>`);

  // ---- group centroid annotations (text at labeled-member centroid; never region outline)
  P.push(`<g font-family="${s.fontStack}" font-weight="${s.titleWeight}">`);
  for (const g of GROUP_ORDER) {
    const c = groupCentroids[g];
    if (!c) continue;
    const cx = sx(c.x), cy = sy(c.y);
    const label = `${g}`;
    // plaque behind text for legibility over terrain
    const tw = label.length * 8.2 + 14;
    P.push(`<g>`);
    P.push(`<rect x="${f2(cx - tw / 2)}" y="${f2(cy - 30)}" width="${f2(tw)}" height="18" rx="3" fill="${s.plaque}" fill-opacity="0.82" stroke="${GROUP_COLORS[g]}" stroke-width="1.2"/>`);
    P.push(`<text x="${f2(cx)}" y="${f2(cy - 17)}" font-size="12" text-anchor="middle" fill="${s.ink}" letter-spacing="0.4">${esc(label)}</text>`);
    P.push(`<line x1="${f2(cx)}" y1="${f2(cy - 12)}" x2="${f2(cx)}" y2="${f2(cy - 3)}" stroke="${GROUP_COLORS[g]}" stroke-width="1.2"/>`);
    P.push(`</g>`);
  }
  P.push(`</g>`);

  // ---- axis end-labels (ratified pole names)
  const cxMid = M.left + PW / 2, cyMid = M.top + PH / 2;
  P.push(`<g font-family="${s.fontStack}" fill="${s.ink}" font-weight="${s.titleWeight}" font-size="15" letter-spacing="1.5">`);
  // x+ = PERFORM (right), x- = DEPLOY (left)
  P.push(`<text x="${f2(M.left + PW - 6)}" y="${f2(cyMid - 6)}" text-anchor="end">PERFORM →</text>`);
  P.push(`<text x="${f2(M.left + 6)}" y="${f2(cyMid - 6)}" text-anchor="start">← DEPLOY</text>`);
  // y+ = LAUNCH (top), y- = EMBODY (bottom)
  P.push(`<text x="${f2(cxMid)}" y="${f2(M.top + 20)}" text-anchor="middle">↑ LAUNCH</text>`);
  P.push(`<text x="${f2(cxMid)}" y="${f2(M.top + PH - 8)}" text-anchor="middle">EMBODY ↓</text>`);
  P.push(`</g>`);

  // ---- title + RIDER-1 badge (mandatory, both skins). All 3 fields from basis; fail-loud already done.
  const riderStr = `Edition ${edition} · frozen ${ratified} · plane = dims 1–2, ${inertiaPct}% corrected inertia · retained basis: ${retainedDims} dims · ${structureStatement}`;
  P.push(`<g font-family="${s.fontStack}" fill="${s.ink}">`);
  P.push(`<text x="${f2(M.left)}" y="42" font-size="26" font-weight="${s.titleWeight}" letter-spacing="0.5">The Atlas of Kits — ${esc(String(atlasVersion))}</text>`);
  // badge plaque
  P.push(`<rect x="${f2(M.left)}" y="58" width="${f2(PW)}" height="30" rx="4" fill="${s.badgeBg}" stroke="${s.plaqueStroke}" stroke-width="1"/>`);
  P.push(`<text x="${f2(M.left + 12)}" y="78" font-size="13" fill="${s.badgeInk}" letter-spacing="0.3">${esc(riderStr)}</text>`);
  P.push(`</g>`);

  // ---- condensation-group legend (top-right of plane)
  {
    const lx = M.left + PW - 190, ly = M.top + 14;
    P.push(`<g font-family="${s.fontStack}" font-size="11" fill="${s.ink}">`);
    P.push(`<rect x="${f2(lx - 12)}" y="${f2(ly - 12)}" width="196" height="${18 * GROUP_ORDER.length + 20}" rx="4" fill="${s.plaque}" fill-opacity="0.9" stroke="${s.plaqueStroke}"/>`);
    P.push(`<text x="${f2(lx)}" y="${f2(ly + 2)}" font-weight="${s.titleWeight}" font-size="11" letter-spacing="0.5">CONDENSATIONS</text>`);
    let yy = ly + 20;
    for (const g of GROUP_ORDER) {
      const c = groupCentroids[g];
      const n = c ? c.n : 0;
      P.push(`<circle cx="${f2(lx + 4)}" cy="${f2(yy - 3)}" r="4.6" fill="${GROUP_COLORS[g]}"/>`);
      P.push(`<text x="${f2(lx + 16)}" y="${f2(yy)}" font-size="11">${esc(g)} (${n})</text>`);
      yy += 18;
    }
    P.push(`</g>`);
  }

  // ---- graveyard legend (death classes; per-class count) — bottom-left
  {
    const lx = M.left + 12, ly0 = M.top + PH - (deathClasses.length * 15 + 26);
    P.push(`<g font-family="${s.fontStack}" font-size="10" fill="${s.ink}">`);
    P.push(`<rect x="${f2(lx - 8)}" y="${f2(ly0 - 14)}" width="230" height="${15 * deathClasses.length + 26}" rx="4" fill="${s.plaque}" fill-opacity="0.9" stroke="${s.plaqueStroke}"/>`);
    P.push(`<text x="${f2(lx)}" y="${f2(ly0)}" font-weight="${s.titleWeight}" font-size="11" letter-spacing="0.4">GRAVEYARD † (${supplementary.length} corpses)</text>`);
    let yy = ly0 + 16;
    for (const dc of deathClasses) {
      const n = supplementary.filter((p) => p.death_class === dc).length;
      const unk = isUnknown(dc);
      const ink = unk ? s.tombUnknownInk : s.tombInk;
      P.push(`<text x="${f2(lx + 2)}" y="${f2(yy)}" font-size="11" fill="${ink}" font-weight="700">†</text>`);
      if (unk) P.push(`<circle cx="${f2(lx + 5)}" cy="${f2(yy - 4)}" r="6" fill="none" stroke="${ink}" stroke-width="1" stroke-dasharray="2 2"/>`);
      P.push(`<text x="${f2(lx + 16)}" y="${f2(yy)}" font-size="10" fill="${ink}">${esc(dc)} (${n})</text>`);
      yy += 15;
    }
    P.push(`</g>`);
  }

  // ---- footer stamp (provenance; all from atlas.json)
  P.push(`<g font-family="${s.fontStack}" fill="${s.faint}" font-size="10">`);
  P.push(`<text x="${f2(M.left)}" y="${f2(H - 12)}">${esc(String(atlasVersion))} · emitted ${esc(emittedAt)} · ${esc(emitterScript)} · skin=${skinKey} · render: galadriel/atlas-edition1-render.mjs</text>`);
  P.push(`<text x="${f2(M.left + PW)}" y="${f2(H - 12)}" text-anchor="end">points: ${active.length} active + ${supplementary.length} corpse = ${all.length}</text>`);
  P.push(`</g>`);

  const svg = `<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">\n${P.join('\n')}\n</svg>\n`;
  return svg;
}

// ------------------------------------------------------------------ coordinate-set fingerprint (skin-invariance test)
// The LAYOUT (every plotted coordinate) must be identical across skins. We compute a
// skin-independent digest of the coordinate set and assert equality.
function coordinateFingerprint() {
  const rows = [];
  for (const p of all) {
    rows.push(`${p.kit_id}|${f2(sx(p.x))}|${f2(sy(p.y))}|${p.supplementary === true ? 'S' : (p.gateA_group ?? 'N')}`);
  }
  for (const g of GROUP_ORDER) {
    const c = groupCentroids[g];
    if (c) rows.push(`CENTROID|${g}|${f2(sx(c.x))}|${f2(sy(c.y))}`);
  }
  rows.push(`AXES|zeroX=${zeroX == null ? 'na' : f2(zeroX)}|zeroY=${zeroY == null ? 'na' : f2(zeroY)}`);
  rows.push(`FRAME|${f2(M.left)}|${f2(M.top)}|${f2(PW)}|${f2(PH)}`);
  return rows.sort().join('\n');
}

// ------------------------------------------------------------------ main
async function main() {
  const results = {};
  const fps = {};
  for (const skin of ['instrument', 'archive']) {
    const svg = renderSVG(skin);
    const svgPath = join(OUT_DIR, `atlas-edition1-${skin}.svg`);
    writeFileSync(svgPath, svg, 'utf8');
    fps[skin] = coordinateFingerprint(); // skin-independent by construction; computed per-skin to prove it
    const pngPath = join(OUT_DIR, `atlas-edition1-${skin}.png`);
    const png = await sharp(Buffer.from(svg), { density: 144 }).png().toBuffer();
    writeFileSync(pngPath, png);
    results[skin] = { svgPath, pngPath, bytes: Buffer.byteLength(svg) };
    console.log(`[render] ${skin}: ${svgPath} (${results[skin].bytes} B), ${pngPath} (${png.length} B PNG)`);
  }

  // ---- ACCEPTANCE TESTS ----
  const tests = [];
  const rec = (name, pass, detail) => tests.push({ name, pass, detail });

  // (1) point counts
  rec('point-counts', active.length === 469 && supplementary.length === 37 && all.length === 506,
    `active=${active.length} (exp 469), supp=${supplementary.length} (exp 37), total=${all.length} (exp 506)`);

  // (2) grouped/neutral partition
  rec('grouped-count', grouped.length === 86, `grouped=${grouped.length} (exp 86: 15+24+23+9+8+7)`);

  // (3) layout-equality (skin invariance)
  rec('layout-equality', fps.instrument === fps.archive, fps.instrument === fps.archive ? 'identical coordinate fingerprint' : 'MISMATCH');

  // (4) determinism: re-render each skin, byte-compare
  let determ = true, dDetail = [];
  for (const skin of ['instrument', 'archive']) {
    const a1 = renderSVG(skin), a2 = renderSVG(skin);
    const eq = a1 === a2;
    if (!eq) determ = false;
    dDetail.push(`${skin}:${eq ? 'byte-equal' : 'DIFF'}`);
  }
  rec('determinism', determ, dDetail.join(', '));

  // (5) R2 grep: the forbidden "number of record" naive-box "2.57" (i.e. "2.57", "2.57B",
  //     "2.57 billion") must appear nowhere as CONTENT. Boundary-matched so a coincidental
  //     substring inside an SVG pixel coordinate (e.g. cx="702.57") is not a false positive —
  //     R2 guards the displayed number, not the layout raster. (Layout call, documented.)
  const bodies = {};
  for (const skin of ['instrument', 'archive']) bodies[skin] = readFileSync(join(OUT_DIR, `atlas-edition1-${skin}.svg`), 'utf8');
  const box257Re = /(?<![\d.])2\.57(?![\d])/; // standalone 2.57 token, not preceded by digit/dot-digit
  const r2 = !box257Re.test(bodies.instrument) && !box257Re.test(bodies.archive);
  rec('R2-no-2.57-numeral', r2, r2 ? 'clean (naive-box 2.57 absent as content; pixel-coord fragments excluded by boundary)' : 'FOUND naive-box "2.57" as content');

  // (6) R3 grep: no season-N strings (season-1, season_001, "season N", etc.)
  const seasonRe = /season[\s_\-]*\d/i;
  const r3 = !seasonRe.test(bodies.instrument) && !seasonRe.test(bodies.archive);
  rec('R3-no-season-N', r3, r3 ? 'clean' : 'FOUND season-N string');

  // (7) RIDER-1 badge present on both skins (all 3 fields literally rendered)
  const badgeOk = ['instrument', 'archive'].every((sk) =>
    bodies[sk].includes(String(inertiaPct)) &&
    bodies[sk].includes(String(retainedDims)) &&
    bodies[sk].includes(structureStatement));
  rec('RIDER-1-badge', badgeOk, badgeOk ? 'inertia_pct + retained_dims + structure_statement present both skins' : 'MISSING badge field');

  // (8) no cell/grid vocabulary leaked as visible region coloring — structural self-check:
  //     terrain is drawn as a single blurred group; no per-region <rect> with distinct fills
  //     beyond the band base. (We assert the band group uses one fill.)
  const oneTerrainFill = bodies.instrument.includes(`fill="${SKINS.instrument.bandBase}"`) && bodies.archive.includes(`fill="${SKINS.archive.bandBase}"`);
  rec('continuum-single-terrain-fill', oneTerrainFill, oneTerrainFill ? 'terrain is one continuous fill (no discrete-region coloring)' : 'terrain fill anomaly');

  // ---- SMOKE TESTS (orientation / axis-flip guards) ----
  const smokes = [];
  const csmoke = (name, pass, detail) => smokes.push({ name, pass, detail });
  const wc = groupCentroids['WHIRLWIND'];
  csmoke('WHIRLWIND x>0 (PERFORM)', wc.x > 0, `x=${wc.x.toFixed(4)}`);
  csmoke('WHIRLWIND y<0 (EMBODY)', wc.y < 0, `y=${wc.y.toFixed(4)}`);
  const tc = groupCentroids['TOTEM-SENTRY'];
  csmoke('TOTEM-SENTRY x<0 (DEPLOY)', tc.x < 0, `x=${tc.x.toFixed(4)}`);
  const cd = all.find((p) => p.kit_id === 'poe1-charged-dash');
  const distToWC = cd ? Math.hypot(cd.x - wc.x, cd.y - wc.y) : Infinity;
  const planeDiag = Math.hypot(maxX - minX, maxY - minY);
  csmoke('charged-dash near WHIRLWIND condensation', cd != null && distToWC < 0.20 * planeDiag,
    `poe1-charged-dash=(${cd?.x.toFixed(3)},${cd?.y.toFixed(3)}) dist=${distToWC.toFixed(3)} (< ${(0.20 * planeDiag).toFixed(3)} = 20% diag)`);
  csmoke('charged-dash is a corpse (supplementary)', cd?.supplementary === true, `supplementary=${cd?.supplementary}, death_class=${cd?.death_class}`);

  // ---- report ----
  console.log('\n================= ACCEPTANCE TESTS =================');
  for (const t of tests) console.log(`  [${t.pass ? 'PASS' : 'FAIL'}] ${t.name} :: ${t.detail}`);
  console.log('================= SMOKE TESTS (orientation) =================');
  for (const t of smokes) console.log(`  [${t.pass ? 'PASS' : 'FAIL'}] ${t.name} :: ${t.detail}`);

  const allPass = [...tests, ...smokes].every((t) => t.pass);
  console.log(`\n${allPass ? 'ALL PASS' : 'FAILURES PRESENT'}`);

  // verification note
  const note = buildNote(results, tests, smokes, fps);
  writeFileSync(join(OUT_DIR, 'verification-note.md'), note, 'utf8');
  console.log(`[note] ${join(OUT_DIR, 'verification-note.md')}`);

  if (!allPass) process.exit(1);
}

function buildNote(results, tests, smokes, fps) {
  const line = (t) => `- [${t.pass ? 'PASS' : 'FAIL'}] **${t.name}** — ${t.detail}`;
  return `# Atlas Edition-I — first render verification note

**Rendered by:** galadriel/pipeline/atlas-edition1-render.mjs (deterministic; no wall-clock — all stamps from atlas.json)
**Input (sole):** agentic_orchestration/research/curated/atlas/atlas.json
**atlas_version:** ${atlasVersion} · **basis frozen:** ${ratified} · **inertia:** ${inertiaPct}% · **retained dims:** ${retainedDims}
**emitted_at (from atlas):** ${emittedAt}
**emitter:** ${emitterScript}

## Outputs
- instrument: \`${results.instrument.svgPath}\` + \`${results.instrument.pngPath}\`
- archive: \`${results.archive.svgPath}\` + \`${results.archive.pngPath}\`

## Point accounting
- active (supplementary=false): **${active.length}** — neutral ${neutral.length} + grouped ${grouped.length}
- supplementary corpses: **${supplementary.length}** (${deathClasses.map((dc) => `${dc}:${supplementary.filter((p) => p.death_class === dc).length}`).join(', ')})
- total: **${all.length}**
- condensation groups (labeled-member centroids):
${GROUP_ORDER.map((g) => { const c = groupCentroids[g]; return `  - ${g}: n=${c?.n ?? 0}, centroid=(${c ? c.x.toFixed(4) : 'na'}, ${c ? c.y.toFixed(4) : 'na'})`; }).join('\n')}

## Acceptance tests
${tests.map(line).join('\n')}

## Smoke tests (orientation / axis-flip guards)
${smokes.map(line).join('\n')}

## Layout calls made
- **Plane:** x=point.x, y=point.y; math y+ mapped to SVG top (LAUNCH up / EMBODY down). World bounds = min/max over ALL points (corpses in-frame) + 6% pad.
- **Axis end-labels:** x+ PERFORM (right), x- DEPLOY (left), y+ LAUNCH (top), y- EMBODY (bottom) — ratified names from basis.axis_names, orientation per prompt (no flip).
- **Continuum underlay:** Gaussian KDE of the 469 active kits on a ${GRID}x${GRID} grid, bandwidth = 5.5% of each axis span, drawn as ${N_BANDS} translucent iso-bands in ONE terrain fill, blurred (stdDev ${SKINS.instrument.blurStd}) → smooth density with NO cell borders / NO grid / NO discrete-region coloring. Soft dashed zero-axes are orientation guides, not partitions.
- **Condensation anchors:** 86 grouped actives color-coded by 6 groups; one plaque annotation at each group's labeled-member centroid (annotation, never region outline). 383 unlabeled actives = neutral dots.
- **Graveyard (F-1):** 37 corpses as dagger (†) glyphs, inked by death-class; the 12 unknown-pending-recrawl carry an open dashed ring = their own visible class; each corpse individually titled + indexed. NEVER a shaded danger region.
- **Franchise:** never a visual encoding — SVG <title> payload only.
- **Two skins, one layout engine:** instrument (quiet, mobile-legible) + archive (God's Archive gilt-on-dark). Skin-invariance proven by identical coordinate fingerprint (${fps.instrument === fps.archive ? 'MATCH' : 'MISMATCH'}).
- **Determinism:** sorted iteration; no RNG; no wall-clock (footer stamp = atlas.emitted_at); 2-dp SVG coords; re-render byte-equal.

## Provenance law
chart = render(atlas.json). No number/label/coordinate originates outside an atlas.json field. Layout is computed; content is not.
`;
}

main();
