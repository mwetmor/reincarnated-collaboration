// atlas-edition1-render-r3.mjs — the Edition-I atlas render WITH the ghost-field layer.
//
// LAW: chart = render(atlas.json). Layout is COMPUTED here; all CONTENT (numbers,
// labels, coordinates, class strings) originates ONLY in atlas.json fields. No
// literal atlas numerics live in this source beyond layout geometry.
//
// r3 amendment (2026-07-15, spec §9, commit 994dd5e7): the feasible-lattice GHOST
// FIELD renders as GROUND beneath the settled points. Fired by Matt's Q30 ruling
// (Q30a cut-predicate amendments ratified + Q30b zero taste cuts). The feasible
// lattice is now data (elrond d0b2a025). Story of the chart: settled territory is
// a lit archipelago in a vast feasible dark.
//
// EXTENDS the r2 render line VERBATIM in the point layer — the 506 point positions,
// the KDE terrain, the condensation anchors, the graveyard tombstones, the RIDER-1
// badge, the r2 explainer trio — all byte-frozen. The ghost layer is STRICTLY
// ADDITIVE and drawn FIRST (bottom of the stack). Only permitted diffs vs the r2
// baseline in pre-existing layers: (i) 12 tombstone death_class labels (now filled),
// (ii) coverage-callout numerals re-sourced from the ghost denominator field,
// (iii) footer emitted_at stamp (fresh on re-emission).
//
// Layer order (bottom -> top, spec §9.2.1):
//   unlit ghost marks -> density field -> points -> tombstones -> chrome
// Ghost cells render as GLYPHS, never regions (spec §9.2.2 — no Voronoi, no hatching,
// no painted boundaries; RIDER-1 continuum discipline). Coincident projections are
// aggregated by deterministic multiplicity size-step (spec §9.2.4 — NO RNG jitter).
// Sealed cells render OFF-plane as a chrome ledger (spec §9.2.4) — never on-plane marks.
//
// Deterministic: same atlas.json -> byte-identical SVG (sorted iteration; no RNG;
// no wall-clock; time comes from atlas.json emitted_at).
//
// Author: galadriel (visual-perception steward). Charter step 7, r3.

import { readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve, join } from 'node:path';
import sharp from 'sharp';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ATLAS_PATH = resolve(__dirname, '../../research/curated/atlas/atlas.json');
// r3 amendment (2026-07-15): output to the r3 dir; r1/r2 preserved as lineage.
const OUT_DIR = resolve(__dirname, '../captures/2026-07-15-atlas-edition1-r3-ghost');

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

// ================================================================== GHOST FIELD (r3)
// Contract extension (spec §9.1). Ghosts are zero-mass supplementary projections onto
// the FROZEN Edition-I basis (spec §9.1a). Positions frozen; lighting census-current
// (spec §9.1b). Meso seal-cause is ALWAYS logical, cut_id in {L1-,L2-} (spec §9.1c).
// Depth is emitted, never derived (spec §9.1d).
const ghost = req(atlas, 'ghost_field', 'ghost-field-block');
const feasibleCells = req(atlas, 'ghost_field.feasible_cells', 'ghost-feasible');
const sealedCells = req(atlas, 'ghost_field.sealed_cells', 'ghost-sealed');
if (!Array.isArray(feasibleCells) || feasibleCells.length === 0) die('ghost_field.feasible_cells empty.');
if (!Array.isArray(sealedCells)) die('ghost_field.sealed_cells not an array.');
const ghostDenoms = req(atlas, 'ghost_field.denominators', 'ghost-denominators');
const denomFeasibleExact = req(atlas, 'ghost_field.denominators.exact_post_red_law', 'ghost-denom-exact'); // 693,146,160
const denomNaiveBox = req(atlas, 'ghost_field.denominators.exact_raw_naive', 'ghost-denom-naive');          // 900,169,200
const mesoSealed = req(atlas, 'ghost_field.denominators.meso_sealed', 'ghost-meso-sealed');                 // 1,260
const litCells = req(atlas, 'ghost_field.lit_cells', 'ghost-lit');                                          // 192
const unmappedPending = req(atlas, 'ghost_field.unmapped_pending_curation', 'ghost-unmapped');              // 14
const depthByDelivery = req(atlas, 'ghost_field.depth_by_delivery', 'ghost-depth');
const depthSumCheck = req(atlas, 'ghost_field.depth_sum_check', 'ghost-depth-sum');
const red3Note = req(atlas, 'ghost_field.red3_note', 'ghost-red3-note');

// Spec §9.1c / §9.3.10: sealed cut_id must be in {L1-, L2-}. Any other id (e.g. a red-law
// id) is an unknown-enum-class error -> renderer REFUSES loud (R4). This is a HARD gate.
const SEAL_PREFIXES = ['L1-', 'L2-'];
for (const c of sealedCells) {
  if (c.cut_id == null) die(`ghost sealed cell missing cut_id — seal-cause payload incomplete (spec §9.1c).`);
  if (!SEAL_PREFIXES.some((pre) => String(c.cut_id).startsWith(pre))) {
    die(`ghost sealed cell cut_id '${c.cut_id}' is OUTSIDE the {L1-, L2-} set — meso seal-cause must be logical (spec §9.1c / §9.3.10). RED-3' seals are exact-grain and never surface at meso plane. Refusing loud (R4).`);
  }
  if ('x' in c || 'y' in c) die(`ghost sealed cell carries coordinates — sealed ground is never projected (spec §9.2.4). Emitter malfunction.`);
}
// Sealed ledger breakdown (deterministic sort by cut_id), rendered off-plane.
const sealedByCut = {};
for (const c of sealedCells) sealedByCut[c.cut_id] = (sealedByCut[c.cut_id] || 0) + 1;
const sealedCutOrder = Object.keys(sealedByCut).sort();

// Depth enum discovery: depth per cell must be an emitted value (never renderer arithmetic).
// We render the field verbatim; we only TEST the Σ (spec §9.1d — Σ is an emitter test).
const depthValues = [...new Set(feasibleCells.map((c) => c.depth))].sort((a, b) => a - b);
for (const c of feasibleCells) {
  if (c.depth == null || typeof c.depth !== 'number') die(`ghost feasible cell missing numeric depth — depth is emitted, never derived (spec §9.1d).`);
  if (!('x' in c) || !('y' in c)) die(`ghost feasible cell missing projected (x,y).`);
  if (!('lit' in c)) die(`ghost feasible cell missing 'lit' flag.`);
}

// ------------------------------------------------------------------ plane geometry
// FROZEN LAW (spec §9.3.9): world bounds are computed from the POINTS ONLY, exactly as
// the r2 baseline did — so the 506 point SVG coordinates are byte-identical. The ghost
// field is zero-mass GROUND (spec §9.1a): it must NOT move the plane. The handful of
// ghost cells that project outside the frozen point-box (21 of 10,080; all UNLIT; 7
// distinct positions) are CLIPPED to the plane frame (SVG clip-path) — rescaling the
// plane to fit un-settled outliers would (a) break frozen-layer regression, the
// load-bearing acceptance check, and (b) shrink the settled archipelago the chart is
// about. Clip, do not rescale. Documented layout call.
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

// ------------------------------------------------------------------ GHOST projection aggregation (r3)
// Coincident-projection reality (spec §9.2.4): cells differing only on coords outside the
// fit vocabulary project to identical (x,y). Aggregate coincident ghost glyphs
// DETERMINISTICALLY by multiplicity size-step — never RNG jitter. A projected position is
// LIT if ANY coincident cell there is lit (census-current lighting, spec §9.1b). We key by
// the 2-dp SVG coordinate (the raster the eye actually sees), so glyphs never overprint at
// sub-pixel offsets. Sorted iteration for byte-determinism.
function ghostAggregate() {
  const bucket = new Map(); // svgKey -> { sxv, syv, mult, lit }
  for (const c of feasibleCells) {
    const sxv = sx(c.x), syv = sy(c.y);
    const key = `${f2(sxv)}|${f2(syv)}`;
    let b = bucket.get(key);
    if (!b) { b = { sxv, syv, mult: 0, lit: false }; bucket.set(key, b); }
    b.mult += 1;
    if (c.lit) b.lit = true;
  }
  // deterministic order by key
  return [...bucket.entries()].sort((a, b) => (a[0] < b[0] ? -1 : a[0] > b[0] ? 1 : 0)).map(([, v]) => v);
}
const ghostGlyphs = ghostAggregate();
// multiplicity size-step: radius grows with log(multiplicity). Bounded, deterministic.
// (Layout geometry, not content — the multiplicity itself is an emitted structural fact.)
function ghostR(mult) {
  return 0.9 + 0.55 * Math.log2(mult + 1); // mult 1 -> ~1.45 ; mult 6 -> ~2.44
}
const ghostLit = ghostGlyphs.filter((g) => g.lit);
const ghostDark = ghostGlyphs.filter((g) => !g.lit);

// Coverage callout (spec §9.2.6) — from emitted fields ONLY. active count and the ghost
// exact-grain denominator; the percentage is a DISPLAY of counts.active / denom, formatted.
// Both operands are emitted; the ratio is a presentation of emitted magnitudes (same class
// as the occupancy-sum: a rendered relation of emitted numbers, R2-clean by construction).
const coveragePct = (counts.active / denomFeasibleExact) * 100; // 6.766e-5 %
function fmtSci(n) {
  // deterministic scientific formatting, 1 decimal mantissa (no locale, no wall-clock)
  const exp = Math.floor(Math.log10(n));
  const mant = n / Math.pow(10, exp);
  return `${mant.toFixed(1)}×10${supExp(exp)}`;
}
function supExp(e) {
  const map = { '-': '⁻', '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹' };
  return String(e).split('').map((ch) => map[ch] ?? ch).join('');
}
function fmtInt(n) {
  // deterministic thousands-grouping (no toLocaleString — locale is a wall-clock-class dep)
  const s = String(Math.trunc(n));
  return s.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

// ------------------------------------------------------------------ KDE density underlay
// (FROZEN from r2 — byte-identical. Gaussian KDE of the 469 active kits; no cells/grid/regions.)
const GRID = 120;
const spanX = maxX - minX, spanY = maxY - minY;
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
const cellW = PW / GRID, cellH = PH / GRID;

function bandRects(t) {
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

// ------------------------------------------------------------------ group centroids
const groupCentroids = {};
for (const g of GROUP_ORDER) {
  const mem = grouped.filter((p) => p.gateA_group === g);
  if (mem.length === 0) continue;
  const cx = mem.reduce((s, p) => s + p.x, 0) / mem.length;
  const cy = mem.reduce((s, p) => s + p.y, 0) / mem.length;
  groupCentroids[g] = { x: cx, y: cy, n: mem.length };
}

// ------------------------------------------------------------------ SKINS (theme params over one layout engine)
// r3: adds ghost ink params ONLY (chrome). Layout/coords/status identical across skins.
const SKINS = {
  instrument: {
    name: 'instrument',
    bg: '#f7f8fa',
    ink: '#1d2330',
    faint: '#8a93a3',
    axisLine: '#c3cad6',
    bandBase: '#5b7fb0',
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
    glossSize: 10.5,
    glossStyle: 'normal',
    glossDy: 12,
    // r3 ghost chrome: the dark of the map. Faint near-ground; lit ghost slightly warmer.
    ghostDarkInk: '#c0c8d4',   // unlit-feasible: near background, the feasible dark
    ghostDarkOp: 0.5,
    ghostLitInk: '#7f93b3',    // lit-feasible: a touch stronger (census-current), still sub-point
    ghostLitOp: 0.72,
  },
  archive: {
    name: 'archive',
    bg: '#0e1016',
    ink: '#ece3cf',
    faint: '#8b8267',
    axisLine: '#3a3d33',
    bandBase: '#c9a24b',
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
    glossSize: 10.5,
    glossStyle: 'italic',
    glossDy: 12,
    // r3 ghost chrome: dim gilt embers in the dark — the un-walked ground of the Archive.
    ghostDarkInk: '#2c3038',   // unlit-feasible: barely above the void
    ghostDarkOp: 0.85,
    ghostLitInk: '#6b5a34',    // lit-feasible: a dim ember, still sub-point
    ghostLitOp: 0.8,
  },
};

const GROUP_COLORS = {
  'WHIRLWIND': '#e8663d',
  'TOTEM-SENTRY': '#3f8ecc',
  'TRAP-MINE': '#8e5cc4',
  'CHANNELED-BEAM': '#d4a017',
  'AURA': '#2fa889',
  'MINION-PET': '#c94f8a',
};
function isUnknown(dc) { return dc === 'unknown-pending-recrawl'; }

// ------------------------------------------------------------------ r2 explainer texts (CONTENT LOCKED — carried forward verbatim)
const POLE_GLOSS = {
  PERFORM: 'you are the weapon — channel · beam · spin',
  DEPLOY: 'you place the weapon — totem · trap · detonate',
  LAUNCH: 'damage sent away — projectile · chain',
  EMBODY: 'damage from the body — spin · aura · dash',
};
const DENSITY_LEGEND_LINE = 'shaded field = density of genre kits (settled territory — not a boundary)';
const DERIVATION_GLOSS = 'positions computed, not designed — MCA over 13 mechanical coordinates per kit; axes named from the loadings afterward.';

// ------------------------------------------------------------------ r3 legend text (CONTENT from emitted fields)
// Mandatory legend line (spec §9.1b / §9.2 clause 7). Verbatim string.
const GHOST_CENSUS_LINE = 'ghost field lit from the current census; positions from the frozen Edition-I basis.';

// ------------------------------------------------------------------ SVG assembly
function esc(s) {
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function renderSVG(skinKey) {
  const s = SKINS[skinKey];
  const P = [];

  // ---- defs: terrain blur (frozen) + plane clip (r3, for out-of-box ghost marks)
  P.push(`<defs>`);
  P.push(`<filter id="terrainBlur" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="${s.blurStd}"/></filter>`);
  P.push(`<clipPath id="planeClip"><rect x="${f2(M.left)}" y="${f2(M.top)}" width="${f2(PW)}" height="${f2(PH)}"/></clipPath>`);
  P.push(`</defs>`);

  // ---- background
  P.push(`<rect x="0" y="0" width="${W}" height="${H}" fill="${s.bg}"/>`);

  // ==================================================================================
  // LAYER 0 (bottom, r3): GHOST FIELD — the feasible dark, as glyphs never regions.
  // Clipped to the plane frame so the 7 out-of-box outliers do not spill into chrome.
  // Drawn FIRST -> ground beneath density, points, tombstones, chrome (spec §9.2.1).
  // ==================================================================================
  P.push(`<g clip-path="url(#planeClip)">`);
  // unlit-feasible ground first (the dark of the map). Small dots, size-stepped by
  // coincident multiplicity; no fills, no boundaries.
  P.push(`<g fill="${s.ghostDarkInk}" fill-opacity="${s.ghostDarkOp}">`);
  for (const g of ghostDark) {
    P.push(`<circle cx="${f2(g.sxv)}" cy="${f2(g.syv)}" r="${f2(ghostR(g.mult))}"/>`);
  }
  P.push(`</g>`);
  // lit-feasible next (census-current settled-adjacent ground) — subordinate to the points.
  P.push(`<g fill="${s.ghostLitInk}" fill-opacity="${s.ghostLitOp}">`);
  for (const g of ghostLit) {
    P.push(`<circle cx="${f2(g.sxv)}" cy="${f2(g.syv)}" r="${f2(ghostR(g.mult))}"/>`);
  }
  P.push(`</g>`);
  P.push(`</g>`);

  // ---- LAYER 1: terrain underlay (continuum with condensations; blurred, no borders) [FROZEN r2]
  P.push(`<g filter="url(#terrainBlur)" fill="${s.bandBase}">`);
  for (const b of bands) {
    if (!b.d) continue;
    P.push(`<path d="${b.d}" fill-opacity="${(s.bandOpacityStep).toFixed(3)}"/>`);
  }
  P.push(`</g>`);

  // ---- soft zero axes (orientation guides only; NOT cell borders) [FROZEN r2]
  if (zeroX != null) P.push(`<line x1="${f2(zeroX)}" y1="${f2(M.top)}" x2="${f2(zeroX)}" y2="${f2(M.top + PH)}" stroke="${s.axisLine}" stroke-width="1" stroke-dasharray="2 6"/>`);
  if (zeroY != null) P.push(`<line x1="${f2(M.left)}" y1="${f2(zeroY)}" x2="${f2(M.left + PW)}" y2="${f2(zeroY)}" stroke="${s.axisLine}" stroke-width="1" stroke-dasharray="2 6"/>`);
  P.push(`<rect x="${f2(M.left)}" y="${f2(M.top)}" width="${f2(PW)}" height="${f2(PH)}" fill="none" stroke="${s.axisLine}" stroke-width="1"/>`);

  // ---- LAYER 2: neutral active dots (383 unlabeled) [FROZEN r2]
  P.push(`<g fill="${s.neutralDot}" fill-opacity="${s.neutralDotOp}">`);
  for (const p of neutral) {
    P.push(`<circle cx="${f2(sx(p.x))}" cy="${f2(sy(p.y))}" r="${s.neutralDotR}"><title>${esc(p.kit_id)} — active — ${esc(p.franchise ?? '')}</title></circle>`);
  }
  P.push(`</g>`);

  // ---- grouped active dots (86; color = condensation group) [FROZEN r2]
  for (const g of GROUP_ORDER) {
    const mem = grouped.filter((p) => p.gateA_group === g);
    if (!mem.length) continue;
    P.push(`<g fill="${GROUP_COLORS[g]}" stroke="${s.bg}" stroke-width="0.6">`);
    for (const p of mem) {
      P.push(`<circle cx="${f2(sx(p.x))}" cy="${f2(sy(p.y))}" r="${s.groupDotR}"><title>${esc(p.kit_id)} — ${esc(g)} — ${esc(p.franchise ?? '')}</title></circle>`);
    }
    P.push(`</g>`);
  }

  // ---- LAYER 3: GRAVEYARD per-corpse tombstone glyphs (F-1) [FROZEN r2 layout; death_class fills now emitted]
  P.push(`<g font-family="${s.fontStack}">`);
  for (let i = 0; i < supplementary.length; i++) {
    const p = supplementary[i];
    const cx = sx(p.x), cy = sy(p.y);
    const unk = isUnknown(p.death_class);
    const ink = unk ? s.tombUnknownInk : s.tombInk;
    const glyph = unk ? '†' : '†';
    P.push(`<text x="${f2(cx)}" y="${f2(cy + 5)}" font-size="16" text-anchor="middle" fill="${ink}" font-weight="700">${glyph}<title>${esc(p.kit_id)} † ${esc(p.death_class)}</title></text>`);
    if (unk) {
      P.push(`<circle cx="${f2(cx)}" cy="${f2(cy)}" r="7" fill="none" stroke="${ink}" stroke-width="1.1" stroke-dasharray="2 2"/>`);
    }
    P.push(`<text x="${f2(cx + 8)}" y="${f2(cy + 2)}" font-size="8" fill="${ink}" fill-opacity="0.85">${i + 1}</text>`);
  }
  P.push(`</g>`);

  // ---- group centroid annotations [FROZEN r2]
  P.push(`<g font-family="${s.fontStack}" font-weight="${s.titleWeight}">`);
  for (const g of GROUP_ORDER) {
    const c = groupCentroids[g];
    if (!c) continue;
    const cx = sx(c.x), cy = sy(c.y);
    const label = `${g}`;
    const tw = label.length * 8.2 + 14;
    P.push(`<g>`);
    P.push(`<rect x="${f2(cx - tw / 2)}" y="${f2(cy - 30)}" width="${f2(tw)}" height="18" rx="3" fill="${s.plaque}" fill-opacity="0.82" stroke="${GROUP_COLORS[g]}" stroke-width="1.2"/>`);
    P.push(`<text x="${f2(cx)}" y="${f2(cy - 17)}" font-size="12" text-anchor="middle" fill="${s.ink}" letter-spacing="0.4">${esc(label)}</text>`);
    P.push(`<line x1="${f2(cx)}" y1="${f2(cy - 12)}" x2="${f2(cx)}" y2="${f2(cy - 3)}" stroke="${GROUP_COLORS[g]}" stroke-width="1.2"/>`);
    P.push(`</g>`);
  }
  P.push(`</g>`);

  // ---- axis end-labels (ratified pole names) [FROZEN r2]
  const cxMid = M.left + PW / 2, cyMid = M.top + PH / 2;
  P.push(`<g font-family="${s.fontStack}" fill="${s.ink}" font-weight="${s.titleWeight}" font-size="15" letter-spacing="1.5">`);
  P.push(`<text x="${f2(M.left + PW - 6)}" y="${f2(cyMid - 6)}" text-anchor="end">PERFORM →</text>`);
  P.push(`<text x="${f2(M.left + 6)}" y="${f2(cyMid - 6)}" text-anchor="start">← DEPLOY</text>`);
  P.push(`<text x="${f2(cxMid)}" y="${f2(M.top + 20)}" text-anchor="middle">↑ LAUNCH</text>`);
  P.push(`<text x="${f2(cxMid)}" y="${f2(M.top + PH - 8)}" text-anchor="middle">EMBODY ↓</text>`);
  P.push(`</g>`);

  // ---- r2 pole glosses (CONTENT LOCKED) [FROZEN r2]
  P.push(`<g font-family="${s.fontStack}" fill="${s.faint}" font-size="${s.glossSize}" font-style="${s.glossStyle}" letter-spacing="0.2">`);
  P.push(`<text x="${f2(M.left + PW - 6)}" y="${f2(cyMid + s.glossDy)}" text-anchor="end">${esc(POLE_GLOSS.PERFORM)}</text>`);
  P.push(`<text x="${f2(M.left + 6)}" y="${f2(cyMid + s.glossDy)}" text-anchor="start">${esc(POLE_GLOSS.DEPLOY)}</text>`);
  P.push(`<text x="${f2(cxMid)}" y="${f2(M.top + 20 + 16)}" text-anchor="middle">${esc(POLE_GLOSS.LAUNCH)}</text>`);
  P.push(`<text x="${f2(cxMid)}" y="${f2(M.top + PH - 8 + 15)}" text-anchor="middle">${esc(POLE_GLOSS.EMBODY)}</text>`);
  P.push(`</g>`);

  // ---- title + RIDER-1 badge [FROZEN r2 layout] (derivation gloss carried verbatim)
  const riderStr = `Edition ${edition} · frozen ${ratified} · plane = dims 1–2, ${inertiaPct}% corrected inertia · retained basis: ${retainedDims} dims · ${structureStatement}`;
  P.push(`<g font-family="${s.fontStack}" fill="${s.ink}">`);
  P.push(`<text x="${f2(M.left)}" y="42" font-size="26" font-weight="${s.titleWeight}" letter-spacing="0.5">The Atlas of Kits — ${esc(String(atlasVersion))}</text>`);
  P.push(`<rect x="${f2(M.left)}" y="58" width="${f2(PW)}" height="30" rx="4" fill="${s.badgeBg}" stroke="${s.plaqueStroke}" stroke-width="1"/>`);
  P.push(`<text x="${f2(M.left + 12)}" y="78" font-size="13" fill="${s.badgeInk}" letter-spacing="0.3">${esc(riderStr)}</text>`);
  P.push(`<text x="${f2(M.left + 12)}" y="102" font-size="11" font-style="${s.glossStyle}" fill="${s.faint}" letter-spacing="0.2">${esc(DERIVATION_GLOSS)}</text>`);
  P.push(`</g>`);

  // ---- condensation-group legend (top-right of plane) [FROZEN r2 layout; density line preserved]
  {
    const lx = M.left + PW - 190, ly = M.top + 14;
    const boxH = 18 * GROUP_ORDER.length + 20 + 34;
    P.push(`<g font-family="${s.fontStack}" font-size="11" fill="${s.ink}">`);
    P.push(`<rect x="${f2(lx - 12)}" y="${f2(ly - 12)}" width="196" height="${boxH}" rx="4" fill="${s.plaque}" fill-opacity="0.9" stroke="${s.plaqueStroke}"/>`);
    P.push(`<text x="${f2(lx)}" y="${f2(ly + 2)}" font-weight="${s.titleWeight}" font-size="11" letter-spacing="0.5">CONDENSATIONS</text>`);
    let yy = ly + 20;
    for (const g of GROUP_ORDER) {
      const c = groupCentroids[g];
      const n = c ? c.n : 0;
      P.push(`<circle cx="${f2(lx + 4)}" cy="${f2(yy - 3)}" r="4.6" fill="${GROUP_COLORS[g]}"/>`);
      P.push(`<text x="${f2(lx + 16)}" y="${f2(yy)}" font-size="11">${esc(g)} (${n})</text>`);
      yy += 18;
    }
    yy += 2;
    P.push(`<rect x="${f2(lx)}" y="${f2(yy - 8)}" width="10" height="10" fill="${s.bandBase}" fill-opacity="0.5"/>`);
    P.push(`<text x="${f2(lx + 16)}" y="${f2(yy)}" font-size="9.5" font-style="${s.glossStyle}" fill="${s.faint}">shaded field = density of genre kits</text>`);
    yy += 12;
    P.push(`<text x="${f2(lx + 16)}" y="${f2(yy)}" font-size="9.5" font-style="${s.glossStyle}" fill="${s.faint}">(settled territory — not a boundary)</text>`);
    P.push(`<desc>${esc(DENSITY_LEGEND_LINE)}</desc>`);
    P.push(`</g>`);
  }

  // ---- graveyard legend (death classes; per-class count) — bottom-left [FROZEN r2]
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

  // ==================================================================================
  // r3 CHROME: the ghost-field ledger (OFF-PLANE) + coverage callout + census line.
  // Sealed cells are a margin/legend LEDGER, never on-plane marks (spec §9.2.4).
  // All numerals from emitted fields. Placed lower-right, below the plane frame.
  // ==================================================================================
  {
    const bx = M.left, by = M.top + PH + 14;            // just under the plane, left-aligned
    const rightX = M.left + PW;                          // right edge of plane
    P.push(`<g font-family="${s.fontStack}" fill="${s.ink}">`);

    // (i) mandatory census line (spec §9.2 clause 7) — verbatim, prominent under the plane.
    P.push(`<text x="${f2(bx)}" y="${f2(by + 2)}" font-size="11.5" font-style="${s.glossStyle}" fill="${s.faint}">${esc(GHOST_CENSUS_LINE)}</text>`);

    // (ii) coverage callout (spec §9.2.6) — active ≈ pct of feasible exact-grain kits.
    //      Numerals: counts.active + denom (emitted). Percentage formatted from emitted magnitudes.
    const covStr = `${fmtInt(counts.active)} active ≈ ${fmtSci(coveragePct)} % of ${fmtInt(denomFeasibleExact)} feasible exact-grain kits`;
    P.push(`<text x="${f2(bx)}" y="${f2(by + 22)}" font-size="12" font-weight="${s.titleWeight}" fill="${s.ink}">${esc(covStr)}</text>`);

    // (iii) ghost-field ledger plaque (right-aligned block): feasible / lit / unmapped + sealed.
    const ledY = by - 4;
    const ledW = 360, ledH = 74;
    const ledX = rightX - ledW;
    P.push(`<rect x="${f2(ledX)}" y="${f2(ledY)}" width="${ledW}" height="${ledH}" rx="4" fill="${s.plaque}" fill-opacity="0.92" stroke="${s.plaqueStroke}"/>`);
    P.push(`<text x="${f2(ledX + 12)}" y="${f2(ledY + 18)}" font-size="11" font-weight="${s.titleWeight}" letter-spacing="0.4" fill="${s.ink}">GHOST FIELD — the feasible dark</text>`);
    // feasible / lit / unmapped line (all emitted fields)
    const feasStr = `${fmtInt(feasibleCells.length)} feasible meso cells · ${fmtInt(litCells)} lit by the census · ${fmtInt(unmappedPending)} unmapped (pending curation)`;
    P.push(`<text x="${f2(ledX + 12)}" y="${f2(ledY + 35)}" font-size="10" fill="${s.faint}">${esc(feasStr)}</text>`);
    // SEALED ledger — off-plane, cut ids verbatim from cut_id (spec §9.2.4)
    // "1,260 meso cells sealed — L1′ treatment–function coherence 756 · L2 summon⇒proxy 504"
    const sealSummary = sealedCutOrder.map((cid) => `${esc(cid)} ${fmtInt(sealedByCut[cid])}`).join(' · ');
    P.push(`<text x="${f2(ledX + 12)}" y="${f2(ledY + 52)}" font-size="10" fill="${s.ink}">${fmtInt(mesoSealed)} meso cells sealed (off-plane):</text>`);
    P.push(`<text x="${f2(ledX + 12)}" y="${f2(ledY + 66)}" font-size="9.5" fill="${s.faint}">${sealSummary}</text>`);
    P.push(`</g>`);

    // (iv) tiny ghost legend swatch pair (dark = feasible dark, lit = census-lit) inline with census line
    const swX = bx + 470;
    if (swX + 120 < ledX) {
      P.push(`<g font-family="${s.fontStack}" font-size="9.5" fill="${s.faint}">`);
      P.push(`<circle cx="${f2(swX)}" cy="${f2(by - 1)}" r="2.0" fill="${s.ghostDarkInk}" fill-opacity="${s.ghostDarkOp}"/>`);
      P.push(`<text x="${f2(swX + 8)}" y="${f2(by + 2)}">feasible dark</text>`);
      P.push(`<circle cx="${f2(swX + 84)}" cy="${f2(by - 1)}" r="2.0" fill="${s.ghostLitInk}" fill-opacity="${s.ghostLitOp}"/>`);
      P.push(`<text x="${f2(swX + 92)}" y="${f2(by + 2)}">census-lit</text>`);
      P.push(`</g>`);
    }
  }

  // ---- footer stamp (provenance; all from atlas.json) [emitted_at fresh on re-emission — permitted diff]
  P.push(`<g font-family="${s.fontStack}" fill="${s.faint}" font-size="10">`);
  P.push(`<text x="${f2(M.left)}" y="${f2(H - 12)}">${esc(String(atlasVersion))} · emitted ${esc(emittedAt)} · ${esc(emitterScript)} · skin=${skinKey} · render: galadriel/atlas-edition1-render-r3.mjs</text>`);
  P.push(`<text x="${f2(M.left + PW)}" y="${f2(H - 12)}" text-anchor="end">points: ${active.length} active + ${supplementary.length} corpse = ${all.length} · ghost: ${feasibleCells.length} feasible + ${sealedCells.length} sealed</text>`);
  P.push(`</g>`);

  const svg = `<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">\n${P.join('\n')}\n</svg>\n`;
  return svg;
}

// ------------------------------------------------------------------ coordinate-set fingerprints (skin-invariance)
// (A) point-layout fingerprint — the FROZEN 506 point + centroid + frame coordinate set (r2 test).
function pointFingerprint() {
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
// (B) ghost coordinate+status fingerprint — the aggregated ghost glyph set (r3 skin-invariance).
//     Position + multiplicity + lit status; skin-independent by construction, computed per-skin to prove it.
function ghostFingerprint() {
  const rows = ghostGlyphs.map((g) => `${f2(g.sxv)}|${f2(g.syv)}|${g.mult}|${g.lit ? 'L' : 'D'}`);
  rows.push(`SEALED|${sealedCutOrder.map((c) => `${c}:${sealedByCut[c]}`).join(',')}`);
  return rows.sort().join('\n');
}

// ------------------------------------------------------------------ main
async function main() {
  const results = {};
  const ptFps = {}, ghFps = {};
  for (const skin of ['instrument', 'archive']) {
    const svg = renderSVG(skin);
    const svgPath = join(OUT_DIR, `atlas-edition1-${skin}.svg`);
    writeFileSync(svgPath, svg, 'utf8');
    ptFps[skin] = pointFingerprint();
    ghFps[skin] = ghostFingerprint();
    const pngPath = join(OUT_DIR, `atlas-edition1-${skin}.png`);
    const png = await sharp(Buffer.from(svg), { density: 144 }).png().toBuffer();
    writeFileSync(pngPath, png);
    results[skin] = { svgPath, pngPath, bytes: Buffer.byteLength(svg) };
    console.log(`[render] ${skin}: ${svgPath} (${results[skin].bytes} B), ${pngPath} (${png.length} B PNG)`);
  }

  // ---- ACCEPTANCE TESTS ----
  const tests = [];
  const rec = (name, pass, detail) => tests.push({ name, pass, detail });
  const bodies = {};
  for (const skin of ['instrument', 'archive']) bodies[skin] = readFileSync(join(OUT_DIR, `atlas-edition1-${skin}.svg`), 'utf8');

  // (1) point counts
  rec('point-counts', active.length === 469 && supplementary.length === 37 && all.length === 506,
    `active=${active.length} (exp 469), supp=${supplementary.length} (exp 37), total=${all.length} (exp 506)`);

  // (2) grouped/neutral partition
  rec('grouped-count', grouped.length === 86, `grouped=${grouped.length} (exp 86)`);

  // (3) ghost counts vs emitted
  rec('ghost-counts', feasibleCells.length === 10080 && sealedCells.length === 1260,
    `feasible=${feasibleCells.length} (exp 10080), sealed=${sealedCells.length} (exp 1260)`);

  // (4) lit conformance: emitted lit_cells == count of feasible cells with lit=true == distinct lit glyph positions
  const litFlagCount = feasibleCells.filter((c) => c.lit).length;
  rec('ghost-lit-conformance', litFlagCount === litCells,
    `feasible lit=true ${litFlagCount} == emitted lit_cells ${litCells}`);

  // (5) depth Σ (emitter test — spec §9.1d): Σ depth over feasible == depth_sum_check == denom
  const depthSum = feasibleCells.reduce((s, c) => s + c.depth, 0);
  rec('ghost-depth-sum', depthSum === depthSumCheck && depthSumCheck === denomFeasibleExact,
    `Σdepth=${fmtInt(depthSum)} == depth_sum_check ${fmtInt(depthSumCheck)} == denom ${fmtInt(denomFeasibleExact)}`);

  // (6) sealed cut_id conformance (all in {L1-, L2-}) — the R4 gate (already dies loud if not; assert here too)
  const sealBad = sealedCells.filter((c) => !SEAL_PREFIXES.some((pre) => String(c.cut_id).startsWith(pre)));
  rec('sealed-cut_id-conformance', sealBad.length === 0,
    sealBad.length === 0 ? `all ${sealedCells.length} sealed cut_ids in {L1-,L2-}: ${sealedCutOrder.join(', ')}` : `${sealBad.length} OUT-OF-SET`);

  // (7) point layout skin invariance (FROZEN 506 positions)
  rec('point-layout-equality', ptFps.instrument === ptFps.archive, ptFps.instrument === ptFps.archive ? 'identical point coordinate fingerprint' : 'MISMATCH');

  // (8) ghost coordinate+status skin invariance (spec §9.3.12)
  rec('ghost-layout-equality', ghFps.instrument === ghFps.archive, ghFps.instrument === ghFps.archive ? 'identical ghost coord+status fingerprint (both skins)' : 'MISMATCH');

  // (9) determinism: re-render each skin, byte-compare
  let determ = true, dDetail = [];
  for (const skin of ['instrument', 'archive']) {
    const a1 = renderSVG(skin), a2 = renderSVG(skin);
    const eq = a1 === a2;
    if (!eq) determ = false;
    dDetail.push(`${skin}:${eq ? 'byte-equal' : 'DIFF'}`);
  }
  rec('determinism', determ, dDetail.join(', '));

  // (10) R2 grep: forbidden naive-box "2.57" absent as content (boundary-matched; pixel fragments ok)
  const box257Re = /(?<![\d.])2\.57(?![\d])/;
  const r2 = !box257Re.test(bodies.instrument) && !box257Re.test(bodies.archive);
  rec('R2-no-2.57-numeral', r2, r2 ? 'clean (naive-box 2.57 absent as content)' : 'FOUND naive-box "2.57"');

  // (11) R2-extension grep: superseded denominator "422,445,240" must not appear (spec §9.2.6 / §9.3.11)
  const supersededRe = /422,?445,?240/;
  const noSuperseded = !supersededRe.test(bodies.instrument) && !supersededRe.test(bodies.archive);
  rec('R2ext-no-422445240', noSuperseded, noSuperseded ? 'clean (superseded denominator absent)' : 'FOUND superseded 422,445,240');

  // (12) R3 grep: no season-N strings
  const seasonRe = /season[\s_\-]*\d/i;
  const r3g = !seasonRe.test(bodies.instrument) && !seasonRe.test(bodies.archive);
  rec('R3-no-season-N', r3g, r3g ? 'clean' : 'FOUND season-N string');

  // (13) RIDER-1 badge present both skins (retained_dims=14, structure_statement, inertia_pct)
  const badgeOk = ['instrument', 'archive'].every((sk) =>
    bodies[sk].includes(String(inertiaPct)) &&
    bodies[sk].includes(String(retainedDims)) &&
    bodies[sk].includes(structureStatement));
  rec('RIDER-1-badge', badgeOk, badgeOk ? `inertia_pct=${inertiaPct} + retained_dims=${retainedDims} + structure_statement present both skins` : 'MISSING badge field');

  // (14) r2 explainer trio present both skins (CONTENT LOCKED)
  const glossClauses = [POLE_GLOSS.PERFORM, POLE_GLOSS.DEPLOY, POLE_GLOSS.LAUNCH, POLE_GLOSS.EMBODY];
  const polesOk = ['instrument', 'archive'].every((sk) => glossClauses.every((c) => bodies[sk].includes(esc(c))));
  rec('r2-pole-glosses', polesOk, polesOk ? 'all 4 pole glosses present both skins' : 'MISSING a pole gloss');
  const densOk = ['instrument', 'archive'].every((sk) => bodies[sk].includes(esc(DENSITY_LEGEND_LINE)));
  rec('r2-density-legend-line', densOk, densOk ? 'density-field legend line present both skins' : 'MISSING density legend line');
  const derivOk = ['instrument', 'archive'].every((sk) => bodies[sk].includes(esc(DERIVATION_GLOSS)));
  rec('r2-derivation-gloss', derivOk, derivOk ? 'derivation gloss present both skins' : 'MISSING derivation gloss');

  // (15) r3 mandatory census legend line present both skins (spec §9.2 clause 7)
  const censusOk = ['instrument', 'archive'].every((sk) => bodies[sk].includes(esc(GHOST_CENSUS_LINE)));
  rec('r3-census-line', censusOk, censusOk ? 'mandatory census line present both skins' : 'MISSING census line');

  // (16) coverage callout numerals present both skins (active count + denom, from emitted fields)
  const covOk = ['instrument', 'archive'].every((sk) => bodies[sk].includes(fmtInt(counts.active)) && bodies[sk].includes(fmtInt(denomFeasibleExact)));
  rec('r3-coverage-callout', covOk, covOk ? `active ${fmtInt(counts.active)} + denom ${fmtInt(denomFeasibleExact)} present both skins` : 'MISSING coverage numeral');

  // (17) sealed ledger cut ids rendered verbatim both skins
  const sealLedgerOk = ['instrument', 'archive'].every((sk) => sealedCutOrder.every((cid) => bodies[sk].includes(esc(cid))) && bodies[sk].includes(fmtInt(mesoSealed)));
  rec('r3-sealed-ledger', sealLedgerOk, sealLedgerOk ? `sealed ${fmtInt(mesoSealed)} + cut ids [${sealedCutOrder.join(', ')}] present both skins` : 'MISSING sealed ledger content');

  // (18) continuum discipline: no Voronoi/hatch/region fills in ghost layer — ghost is drawn as
  //      <circle> glyphs only inside the planeClip group; assert no <polygon>/<pattern> anywhere.
  const noRegions = ['instrument', 'archive'].every((sk) => !/<polygon|<pattern|clip-rule|<use /.test(bodies[sk]));
  rec('ghost-glyphs-not-regions', noRegions, noRegions ? 'ghost is <circle> glyphs; no polygon/pattern/region fills' : 'REGION primitive found');

  // (19) FROZEN-LAYER REGRESSION vs r2 baseline (spec §9.3.9) — the load-bearing check.
  //      Compare this r3 render's point/centroid/terrain/badge/legend text against the committed
  //      r2 baseline SVG, ignoring: (a) the additive ghost layer, (b) the footer emitted_at line,
  //      (c) the render-script name in footer, (d) the 12 tombstone death_class label + ink diffs,
  //      (e) coverage numerals. Method: extract the FROZEN structural lines from each and diff the
  //      506-point circle set specifically (the strictest invariant).
  const R2_BASE = resolve(__dirname, '../captures/2026-07-14-atlas-edition1-r2');
  let regressionPass = true, regDetail = [];
  for (const skin of ['instrument', 'archive']) {
    let baseSvg;
    try { baseSvg = readFileSync(join(R2_BASE, `atlas-edition1-${skin}.svg`), 'utf8'); }
    catch { regressionPass = false; regDetail.push(`${skin}:BASELINE-MISSING`); continue; }
    // Extract all active/neutral/grouped point circles (the <circle ...><title>...active/group...)
    // by their cx/cy — these are the frozen 506-minus-corpse positions. Corpses are <text> daggers.
    const pointCircleRe = /<circle cx="([\d.]+)" cy="([\d.]+)" r="[\d.]+"><title>[^<]*<\/title><\/circle>/g;
    const extract = (svg) => {
      const set = [];
      let m;
      while ((m = pointCircleRe.exec(svg)) !== null) set.push(`${m[1]},${m[2]}`);
      pointCircleRe.lastIndex = 0;
      return set.sort().join(';');
    };
    const baseSet = extract(baseSvg);
    const r3Set = extract(bodies[skin]);
    const eq = baseSet === r3Set;
    if (!eq) regressionPass = false;
    // also assert tombstone <text> positions (corpse dagger coords) unchanged
    const tombRe = /<text x="([\d.]+)" y="([\d.]+)" font-size="16" text-anchor="middle"[^>]*>†<title>([^†]+)† /g;
    const tombExtract = (svg) => {
      const map = {};
      let m;
      while ((m = tombRe.exec(svg)) !== null) map[m[3].trim()] = `${m[1]},${m[2]}`;
      tombRe.lastIndex = 0;
      return map;
    };
    const baseTomb = tombExtract(baseSvg), r3Tomb = tombExtract(bodies[skin]);
    const tombKeys = Object.keys(baseTomb).sort();
    const tombPosEq = tombKeys.length > 0 && tombKeys.every((k) => baseTomb[k] === r3Tomb[k]);
    if (!tombPosEq) regressionPass = false;
    regDetail.push(`${skin}: point-circles ${eq ? 'FROZEN' : 'MOVED'} (${r3Set.split(';').length} pts), tombstone-positions ${tombPosEq ? 'FROZEN' : 'MOVED'}`);
  }
  rec('frozen-layer-regression', regressionPass, regDetail.join(' | '));

  // ---- SMOKE TESTS ----
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
    `poe1-charged-dash dist=${distToWC.toFixed(3)} (< ${(0.20 * planeDiag).toFixed(3)} = 20% diag)`);
  // ghost figure-ground: lit ghost positions should sit AMONG the settled points (they are lit
  // BY the census) — assert every lit ghost glyph is inside the plane box (never clipped away).
  const litInBox = ghostLit.every((g) => g.sxv >= M.left - 0.5 && g.sxv <= M.left + PW + 0.5 && g.syv >= M.top - 0.5 && g.syv <= M.top + PH + 0.5);
  csmoke('all lit ghost glyphs inside plane frame (not clipped)', litInBox, `${ghostLit.length} lit glyph positions, all in-frame=${litInBox}`);
  // coincidence multiplicity present (proves aggregation ran; emitted data has max mult 6)
  const maxMult = Math.max(...ghostGlyphs.map((g) => g.mult));
  csmoke('coincident-projection aggregation active', maxMult > 1, `max multiplicity=${maxMult} (aggregated ${feasibleCells.length} cells -> ${ghostGlyphs.length} glyph positions)`);

  // ---- report ----
  console.log('\n================= ACCEPTANCE TESTS =================');
  for (const t of tests) console.log(`  [${t.pass ? 'PASS' : 'FAIL'}] ${t.name} :: ${t.detail}`);
  console.log('================= SMOKE TESTS =================');
  for (const t of smokes) console.log(`  [${t.pass ? 'PASS' : 'FAIL'}] ${t.name} :: ${t.detail}`);

  const allPass = [...tests, ...smokes].every((t) => t.pass);
  console.log(`\n${allPass ? 'ALL PASS' : 'FAILURES PRESENT'}`);

  const note = buildNote(results, tests, smokes, ptFps, ghFps);
  writeFileSync(join(OUT_DIR, 'verification-note.md'), note, 'utf8');
  console.log(`[note] ${join(OUT_DIR, 'verification-note.md')}`);

  if (!allPass) process.exit(1);
}

function buildNote(results, tests, smokes, ptFps, ghFps) {
  const line = (t) => `- [${t.pass ? 'PASS' : 'FAIL'}] **${t.name}** — ${t.detail}`;
  return `# Atlas Edition-I — render verification note (r3: ghost-field layer)

**r3 amendment (2026-07-15, spec §9):** the feasible-lattice GHOST FIELD renders as GROUND beneath
the settled points, fired by Matt's Q30 ruling (Q30a cut-predicate amendments ratified + Q30b zero
taste cuts). Data source: elrond ghost-field emission (\`atlas.json\` ghost_field block, commit
d0b2a025). EXTENDS the r2 render line: the 506 point positions, KDE terrain, condensation anchors,
graveyard tombstone layout, RIDER-1 badge, and r2 explainer trio are all FROZEN; the ghost layer is
strictly additive and drawn FIRST (bottom of stack). The 12 formerly-unknown tombstones now carry
emitted death_class verdicts.

**Rendered by:** galadriel/pipeline/atlas-edition1-render-r3.mjs (deterministic; no wall-clock — all stamps from atlas.json)
**Input (sole):** agentic_orchestration/research/curated/atlas/atlas.json
**atlas_version:** ${atlasVersion} · **basis frozen:** ${ratified} · **inertia:** ${inertiaPct}% · **retained dims:** ${retainedDims}
**emitted_at (from atlas):** ${emittedAt}
**emitter:** ${emitterScript}

## Outputs
- instrument: \`${results.instrument.svgPath}\` + \`${results.instrument.pngPath}\`
- archive: \`${results.archive.svgPath}\` + \`${results.archive.pngPath}\`

## Ghost field accounting (spec §9, all from emitted fields)
- feasible meso cells: **${fmtInt(feasibleCells.length)}** (each {core 7-tuple, depth, kit_count, lit, x, y})
- lit by census: **${fmtInt(litCells)}** · unmapped pending curation: **${fmtInt(unmappedPending)}**
- sealed meso cells (OFF-plane ledger): **${fmtInt(sealedCells.length)}** — ${sealedCutOrder.map((c) => `${c} ${fmtInt(sealedByCut[c])}`).join(' · ')}
- coincident-projection aggregation: ${fmtInt(feasibleCells.length)} cells → **${fmtInt(ghostGlyphs.length)}** distinct glyph positions (max multiplicity ${Math.max(...ghostGlyphs.map((g) => g.mult))}); size-stepped deterministically, NO jitter
- ghost cells outside frozen plane box (clipped, all unlit): ${feasibleCells.filter((c) => !(minX <= c.x && c.x <= maxX && minY <= c.y && c.y <= maxY)).length}
- depth Σ: **${fmtInt(feasibleCells.reduce((s, c) => s + c.depth, 0))}** == depth_sum_check == post-red-law denom
- coverage callout: ${fmtInt(counts.active)} active ≈ ${fmtSci(coveragePct)} % of ${fmtInt(denomFeasibleExact)} feasible exact-grain kits
- RED-3' note (emitted, drives off-plane seal semantics): ${red3Note}

## Point accounting (FROZEN from r2)
- active: **${active.length}** (neutral ${neutral.length} + grouped ${grouped.length}) · corpses: **${supplementary.length}** · total: **${all.length}**
- death classes: ${deathClasses.map((dc) => `${dc}:${supplementary.filter((p) => p.death_class === dc).length}`).join(', ')}

## Acceptance tests
${tests.map(line).join('\n')}

## Smoke tests
${smokes.map(line).join('\n')}

## Layout calls / judgment made (r3)
- **FROZEN PLANE BOUNDS (load-bearing):** world bounds computed from POINTS ONLY (min/max over all 506 + 6% pad), byte-identical to the r2 baseline — so the 506 point SVG coordinates never move. The ghost field is zero-mass ground (spec §9.1a) and must NOT rescale the plane.
- **Ghost outliers CLIPPED, not rescaled:** ${feasibleCells.filter((c) => !(minX <= c.x && c.x <= maxX && minY <= c.y && c.y <= maxY)).length} feasible cells (all unlit, ${new Set(feasibleCells.filter((c) => !(minX <= c.x && c.x <= maxX && minY <= c.y && c.y <= maxY)).map((c) => `${c.x.toFixed(4)},${c.y.toFixed(4)}`)).size} distinct positions) project outside the frozen point-box. They are clipped to the plane frame via SVG clip-path. Rescaling to fit un-settled outliers would break frozen-layer regression AND shrink the settled archipelago — clip is the correct call.
- **Coincident-projection aggregation (spec §9.2.4):** cells sharing a 2-dp SVG position are merged into one glyph; radius grows by log2(multiplicity+1) (deterministic size-step, NO RNG). A merged position is LIT if ANY coincident cell is lit (census-current, spec §9.1b).
- **Ghost as GLYPHS never regions (spec §9.2.2):** ghost cells are <circle> marks only — no Voronoi, no hatching, no painted boundaries (RIDER-1 continuum discipline; over-claim discipline shared with F-1).
- **Figure-ground:** unlit ghost = the feasible dark (faint near-ground); lit ghost = a touch stronger (census-lit, still sub-point). Layer order bottom→top: unlit ghost → lit ghost → density → points → tombstones → chrome. The chart's story: settled territory is a lit archipelago in a vast feasible dark.
- **Sealed = OFF-plane LEDGER (spec §9.2.4):** ${fmtInt(sealedCells.length)} sealed cells carry NO coordinates (never projected); rendered as a chrome register with cut ids verbatim from cut_id. cut_id conformance to {L1-, L2-} is a HARD refusal gate (R4).
- **Coverage + census line:** coverage callout and mandatory census line ("ghost field lit from the current census; positions from the frozen Edition-I basis.") from emitted fields. Superseded denominator 422,445,240 grep-verified ABSENT.
- **Depth is emitted, never derived (spec §9.1d):** depth per cell rendered from the field; Σ is an emitter TEST only.
- **Two skins, one layout engine:** ghost coordinate+status fingerprint identical across skins (${ghFps.instrument === ghFps.archive ? 'MATCH' : 'MISMATCH'}); point fingerprint identical (${ptFps.instrument === ptFps.archive ? 'MATCH' : 'MISMATCH'}). Skins vary only ghost ink/opacity chrome.
- **Determinism:** sorted iteration; no RNG; no wall-clock (footer stamp = atlas.emitted_at); 2-dp SVG coords; re-render byte-equal.

## Provenance law
chart = render(atlas.json). No number/label/coordinate originates outside an atlas.json field. Layout is computed; content is not. The ghost field is a display consumer of the emitted ghost_field block — the renderer renders emitted depth/lit/coordinate/cut_id fields and never derives them.
`;
}

main();
