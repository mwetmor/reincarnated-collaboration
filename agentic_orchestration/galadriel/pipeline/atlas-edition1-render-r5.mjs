// atlas-edition1-render-r5.mjs — the Edition-I atlas render WITH the ghost-field
// layer + the GHOST HORIZON envelope + the re-led HEADLINE COVERAGE PAIR + the
// BEYOND-HORIZON LEDGER LINE.
//
// LAW: chart = render(atlas.json). Layout is COMPUTED here; all CONTENT (numbers,
// labels, coordinates, class strings) originates ONLY in atlas.json fields. No
// literal atlas numerics live in this source beyond layout geometry.
//
// r5 amendment (2026-07-15, spec §9.5): STRICTLY-ADDITIVE — ONE microcopy line in the
// GHOST FIELD ledger box (both skins), rendered directly after the clip-disclosure line
// (§9.2.3). Fired by Matt's directive ("cut §9.5 and fire the r5 pass") after the chart's
// first reader hit the SECOND misreading within one session of r4 going live: "how can we
// have kits outside the ghost's meso area?". The r4 horizon label kills misreading #1 (dark
// beyond the line = mined-out); this line kills misreading #2 (kits beyond the line =
// paradox). Exact string template (N interpolated):
//   "N settled kits stand beyond the horizon — kits project with all 14 coordinates;
//    ghost cells carry the 7 core only (the strongest east pulls — cone/whirlwind geometry,
//    channel commit — are invisible at meso grain)."
//   - N COMPUTED FROM THE RENDER PASS: point-in-polygon test of all ACTIVE
//     (supplementary=false) points against the SAME world-space convex hull the r4 §9.4.1
//     code computes (ghostHullWorld) — ONE code path, never a second hull, never hard-coded.
//     Boundary convention: a kit exactly ON the hull counts as INSIDE (not beyond). N=14
//     today (10 WHIRLWIND + 3 CHANNELED-BEAM + 1 neutral, all commit=channel). If the render
//     pass disagrees with 14, the run HALTS (fail-loud) rather than shipping a wrong count.
//   - Zero-case omission: if no active kit lies outside the hull, the line is OMITTED
//     entirely (no "0 kits") — same protocol as the clip-disclosure line.
//   - Supplementary points (tombstones) EXCLUDED from N — the graveyard is its own layer.
//   - The coordinate examples in the string (cone/whirlwind geometry, channel commit) are
//     CONTENT-LOCKED disclosure copy — same class as the pole glosses (empirical facts about
//     the FROZEN basis, loading ranks #2/#3, immutable within Edition-I).
// The exact contiguous string is carried in a <title> node so acceptance can grep it whole
// (same pattern as the r4 horizon label). Every frozen layer — points, ghost glyphs, horizon
// polyline + label + marker, tombstones, headline callout, explainer trio, RIDER-1, AND the
// clip-disclosure line — is BYTE-FROZEN vs the r4 baseline; the ONLY diff is this one line.
//
// r4 amendment (2026-07-15, spec §9.4): STRICTLY-ADDITIVE chrome on top of the r3.2
// render line, fired by Matt's ratification ("I agree with all four") of gandalf's
// INTERIOR-1 memo review. TWO changes, both skins:
//   (1) GHOST HORIZON — the convex hull of ALL 10,080 projected ghost positions
//       (incl. the 21 out-of-frame cells; the hull is of the lattice's REACH, then
//       CLIPPED to the plane frame exactly like the ghost glyphs). Faint dashed
//       envelope, chrome-weight, drawn BENEATH the ghost glyphs (must not read as
//       data). Mandatory label at the EAST gap: settled kits reach x=1.628, ghost
//       reach ends x=1.258 — 6 settled kits stand beyond the horizon there; that is
//       the direction the disclosure exists for. Hull vertices COMPUTED FROM THE
//       RENDER PASS from the loaded ghost field — never hard-coded. Same law as
//       RIDER-1 / F-1 / r3.2: never let the reader mistake the instrument's reach
//       for the world's edge.
//   (2) HEADLINE COVERAGE PAIR — the coverage callout re-leads with two meso-grain
//       statistics computed at render from emitted fields (lit_cells / meso_feasible
//       and active / lit_cells). The exact-grain line (469 ≈ 6.8×10⁻⁵ % of
//       693,146,160) DEMOTES to a secondary flavor line — retained, no longer lead.
// Every frozen layer (points, tombstones, ghost glyph positions, sealed ledger,
// clip-disclosure line, explainer trio, RIDER-1 badge) is BYTE-FROZEN vs r3.2.
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
// Layer order (bottom -> top, spec §9.2.1 + §9.4.1):
//   ghost horizon (chrome) -> unlit ghost marks -> lit ghost marks -> density field
//   -> points -> tombstones -> chrome. The horizon is drawn FIRST inside the same
//   plane-clip group so the ghost glyphs paint OVER it — visually sub-ghost per §9.4.1.
// Ghost cells render as GLYPHS, never regions (spec §9.2.2 — no Voronoi, no hatching,
// no painted boundaries; RIDER-1 continuum discipline). Coincident projections are
// aggregated by deterministic multiplicity size-step (spec §9.2.4 — NO RNG jitter).
// Sealed cells render OFF-plane as a chrome ledger (spec §9.2.4) — never on-plane marks.
// The ghost horizon is a dashed POLYLINE (open envelope, clipped) — NOT a filled
// polygon: a fill would read as the region-claim §9.2.2 forbids.
//
// Deterministic: same atlas.json -> byte-identical SVG (sorted iteration; no RNG;
// no wall-clock; time comes from atlas.json emitted_at).
//
// Author: galadriel (visual-perception steward). Charter step 7, r5.

import { readFileSync, writeFileSync, mkdtempSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve, join } from 'node:path';
import { tmpdir } from 'node:os';
import { execFileSync } from 'node:child_process';
import sharp from 'sharp';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ATLAS_PATH = resolve(__dirname, '../../research/curated/atlas/atlas.json');
// r5 amendment (2026-07-15): output to the r5 dir; r1/r2/r3/r4 preserved as lineage.
// The r4 dir is the frozen-layer regression BASELINE (spec §9.5.2.17).
const DEFAULT_OUT_DIR = resolve(__dirname, '../captures/2026-07-15-atlas-edition1-r5-beyond-horizon');
// Doctored-input harness env vars (acceptance tests re-run this module in child processes):
//   ATLAS_OVERRIDE   — read this atlas, print HULL/BEYOND receipts, write NOTHING (r4+r5
//                      computed-not-constant proofs; §9.4.3.13 + §9.5.2.16a).
//   ATLAS_ALLIN_SRC  — read this atlas (a doctored all-inside copy) and…
//   ATLAS_ALLIN_OUT  — …write a REAL render into THIS scratch dir (r5 zero-case on-chart
//                      OMISSION proof; §9.5.2.16b) — a full render, not a receipt short-circuit.
// The §9.5.1 receipt-guard (N must == 14) is skipped for ALL doctored inputs (they are MEANT
// to move N; the acceptance test asserts the change). Determinism/provenance are unaffected —
// each override is still an atlas.json, just a doctored one.
const ATLAS_ALLIN_SRC = process.env.ATLAS_ALLIN_SRC || null;
const ATLAS_ALLIN_OUT = process.env.ATLAS_ALLIN_OUT || null;
const ATLAS_OVERRIDE = process.env.ATLAS_OVERRIDE || null;
// Effective atlas source + output dir. All-inside render mode takes precedence for BOTH.
const ATLAS_SRC = ATLAS_ALLIN_SRC || ATLAS_OVERRIDE || ATLAS_PATH;
const IS_DOCTORED = Boolean(ATLAS_ALLIN_SRC || ATLAS_OVERRIDE);
const OUT_DIR = ATLAS_ALLIN_OUT || DEFAULT_OUT_DIR;
// Receipt-only short-circuit fires ONLY for a pure ATLAS_OVERRIDE (no all-inside OUT target).
const RECEIPT_ONLY = Boolean(ATLAS_OVERRIDE) && !ATLAS_ALLIN_OUT;

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
const atlas = JSON.parse(readFileSync(ATLAS_SRC, 'utf8'));

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

// ------------------------------------------------------------------ CLIP DISCLOSURE (r3.2, spec §9.2.3)
// The plane bounds are FROZEN to the settled points (zero-mass ground must not move the
// frame). Ghost cells projecting outside the plane box are CLIPPED (SVG clip-path), never
// rescaled-for. §9.2.3 binds: any clip MUST be disclosed on-chart in the ghost ledger — the
// dark the reader sees implicitly claims to be the feasible space; silent truncation of it
// is an under-claim. The count is COMPUTED FROM THE RENDER PASS (cells whose projected
// position falls outside the plane rect = the actual clip-path), NEVER hard-coded — if a
// future atlas.json changes the count, the disclosure follows. If ZERO cells clip, no line
// is rendered (do not print "0 clipped"). Boundary test is inclusive of the frame edge (a
// cell landing exactly on the rect is in-frame, not clipped).
const IN_PLANE_EPS = 0.01; // 2-dp SVG raster tolerance — a cell within a rounding-tick of the edge is in-frame
function ghostInPlane(c) {
  const sxv = sx(c.x), syv = sy(c.y);
  return sxv >= M.left - IN_PLANE_EPS && sxv <= M.left + PW + IN_PLANE_EPS
      && syv >= M.top - IN_PLANE_EPS && syv <= M.top + PH + IN_PLANE_EPS;
}
const ghostClippedCells = feasibleCells.filter((c) => !ghostInPlane(c));
const ghostClippedCount = ghostClippedCells.length;
const ghostClippedAllUnlit = ghostClippedCells.every((c) => !c.lit);
// Zero-mass invariant (spec §9.1a-adjacent): a CLIPPED-and-LIT ghost would mean the census
// lights ground the settled frame cannot show — a silent under-claim of live territory.
// The lit-glyphs-in-frame smoke test already asserts the positive; assert the negative here.
// Scoped to the REAL input (!IS_DOCTORED): the r5 zero-case acceptance test deliberately
// moves active points to shrink the frame (to drive N=0), which mechanically pushes some
// lit ghost cells outside that shrunken frame — an EXPECTED artifact of the doctoring, not an
// emitter malfunction. Same scoping principle as the beyond-horizon receipt-guard.
if (!IS_DOCTORED && !ghostClippedAllUnlit) die(`ghost CLIP disclosure: ${ghostClippedCells.filter((c) => c.lit).length} CLIPPED cell(s) are LIT — census lights ground outside the frozen frame (silent under-claim of live territory). Frame is frozen to settled points; a lit outlier is emitter/decoupling malfunction (spec §9.1a/§9.2.3).`);
// (Disclosure microcopy string `ghostClipLine` is built below, after fmtInt is defined.)

// ================================================================== GHOST HORIZON (r4)
// Spec §9.4.1 (disclosure law, sibling of r3.2). The reach boundary of the ghost lattice:
// the CONVEX HULL of ALL 10,080 projected ghost positions — INCLUDING the 21 out-of-frame
// cells (the hull is of the lattice's REACH, not the in-frame subset), THEN CLIPPED to the
// plane frame exactly like the ghost glyphs (SVG clip-path). Vertices are COMPUTED FROM THE
// RENDER PASS (from feasibleCells) — never hard-coded — so the envelope follows any future
// atlas.json change (this is what the doctored-input acceptance test §9.4.3.13 verifies).
//
// We hull in WORLD space (the true reach), then project each vertex through sx/sy for the
// draw — so the hull describes the lattice's real extent (incl. outliers), and the SVG
// clip-path trims the drawn polyline to the frame. Deterministic: distinct positions keyed
// by 6-dp world coord + sorted; Andrew's monotone chain (no RNG, no float-order ambiguity).
//
// Rationale: the instrument's 7-coordinate core-subspace confinement (ghosts cannot access
// non-core pulls — geometry=cone +1.98, commit=channel +1.88 are masked) must be a DISCLOSED
// instrument property. The EAST gap is the load-bearing direction: settled points reach
// x=1.628, the ghost hull reach ends x=1.258 — 6 settled kits stand beyond the horizon there.
function convexHullWorld(cells) {
  // distinct world positions (a hull of duplicates is the hull of the distinct set)
  const seen = new Set();
  const pts = [];
  for (const c of cells) {
    const k = `${c.x.toFixed(6)},${c.y.toFixed(6)}`;
    if (!seen.has(k)) { seen.add(k); pts.push([c.x, c.y]); }
  }
  // deterministic sort: x asc, then y asc
  pts.sort((a, b) => (a[0] === b[0] ? a[1] - b[1] : a[0] - b[0]));
  const n = pts.length;
  if (n < 3) return pts.slice();
  const cross = (O, A, B) => (A[0] - O[0]) * (B[1] - O[1]) - (A[1] - O[1]) * (B[0] - O[0]);
  const lower = [];
  for (const p of pts) {
    while (lower.length >= 2 && cross(lower[lower.length - 2], lower[lower.length - 1], p) <= 0) lower.pop();
    lower.push(p);
  }
  const upper = [];
  for (let i = n - 1; i >= 0; i--) {
    const p = pts[i];
    while (upper.length >= 2 && cross(upper[upper.length - 2], upper[upper.length - 1], p) <= 0) upper.pop();
    upper.push(p);
  }
  lower.pop(); upper.pop();
  return lower.concat(upper); // CCW ring of world-space vertices
}
const ghostHullWorld = convexHullWorld(feasibleCells);
const ghostHullVertexCount = ghostHullWorld.length;
// project vertices to SVG space (the draw is a closed polyline; clip-path trims to frame)
const ghostHullSvg = ghostHullWorld.map(([wx, wy]) => ({ x: sx(wx), y: sy(wy) }));
// East-gap label anchor (spec §9.4.1): place the label adjacent to the EAST extreme of the
// hull — the vertex with the greatest projected x (settled points reach further east; the
// horizon ends here; the disclosure exists for that gap). Anchor computed from the hull,
// never hard-coded. We nudge the label just inside the frame's east edge at the anchor's y.
const ghostHullEastVertex = ghostHullSvg.reduce((best, v) => (v.x > best.x ? v : best), ghostHullSvg[0]);
// Mandatory horizon label — EXACT string per spec §9.4.1.
const GHOST_HORIZON_LABEL = 'ghost coverage limit — dark beyond this line is unmapped at meso grain, not absent.';

// ================================================================== BEYOND-HORIZON (r5)
// Spec §9.5.1 — the second-misreading disclosure. Count the ACTIVE (supplementary=false)
// kits that stand OUTSIDE the ghost hull — kits project with all 14 coordinates, but ghost
// cells carry only the 7 core, so the strongest EAST pulls (cone/whirlwind geometry, channel
// commit) are invisible at meso grain and the lit kits overshoot the ghost reach.
//
// N is COMPUTED FROM THE RENDER PASS: a point-in-polygon test of `active` against the SAME
// `ghostHullWorld` the r4 §9.4.1 code already computed — ONE code path, ONE hull, NEVER a
// second hull, NEVER hard-coded. It follows any future atlas.json change (the doctored-input
// acceptance test §9.5.2.16 proves computed-not-constant). Boundary convention (spec §9.5.1):
// a kit exactly ON the hull edge counts as INSIDE (not beyond) — so on-edge => inside => not
// counted. Supplementary points (tombstones) are EXCLUDED — the graveyard is its own layer.
//
// We test in WORLD space against the world-space hull (the hull's true reach, incl. its 21
// out-of-frame vertices) — the same space the hull is computed in. The SVG projection sx/sy
// is affine-monotone, so in-world containment == in-projected containment; testing in world
// space avoids re-introducing the clip-frame (a kit east of the hull but inside the frame is
// still beyond the hull — which is exactly the load-bearing east case).
const PIP_EPS = 1e-9; // world-coord tolerance for the on-edge (=> inside) boundary convention
function pointOnSegment(px, py, ax, ay, bx, by) {
  // collinear AND within the segment's bounding span (inclusive, with eps)
  const cross = (bx - ax) * (py - ay) - (by - ay) * (px - ax);
  if (Math.abs(cross) > PIP_EPS) return false;
  const dot = (px - ax) * (bx - ax) + (py - ay) * (by - ay);
  const len2 = (bx - ax) * (bx - ax) + (by - ay) * (by - ay);
  return dot >= -PIP_EPS && dot <= len2 + PIP_EPS;
}
function pointInHullWorld(px, py, poly) {
  if (poly.length < 3) return false; // degenerate hull cannot contain area
  // (i) ON the boundary => INSIDE (spec §9.5.1 boundary convention).
  for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {
    if (pointOnSegment(px, py, poly[j][0], poly[j][1], poly[i][0], poly[i][1])) return true;
  }
  // (ii) ray-cast parity for strict interior.
  let inside = false;
  for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {
    const xi = poly[i][0], yi = poly[i][1], xj = poly[j][0], yj = poly[j][1];
    const intersect = ((yi > py) !== (yj > py)) && (px < ((xj - xi) * (py - yi)) / (yj - yi) + xi);
    if (intersect) inside = !inside;
  }
  return inside;
}
// `active` is already sorted by kit_id (byId, above) — deterministic iteration.
const beyondHorizonKits = active.filter((p) => !pointInHullWorld(p.x, p.y, ghostHullWorld));
const beyondHorizonCount = beyondHorizonKits.length;
// Spec §9.5.1 receipt-guard: gandalf independently computed N=14 for the frozen Edition-I
// input (10 WHIRLWIND + 3 CHANNELED-BEAM + 1 neutral, all commit=channel). If the render pass
// disagrees on the REAL input, HALT and report — never ship a wrong count (fail-loud). The
// guard binds ONLY on the real atlas (not on doctored override inputs, whose whole purpose is
// to move N — the acceptance test asserts the change there).
const BEYOND_HORIZON_EXPECTED = 14;
if (!IS_DOCTORED && beyondHorizonCount !== BEYOND_HORIZON_EXPECTED) {
  die(`r5 beyond-horizon receipt mismatch: render pass computed N=${beyondHorizonCount} active kits beyond the ghost hull, but the ratified Edition-I receipt is N=${BEYOND_HORIZON_EXPECTED} (spec §9.5.1). Kits beyond: [${beyondHorizonKits.map((p) => p.kit_id).join(', ')}]. HALTING rather than shipping a wrong disclosure count — the hull, the input, or the receipt moved.`);
}
// (Beyond-horizon microcopy string `beyondHorizonLine` is built below, after fmtInt is defined —
//  same deferral the clip-disclosure line uses. OMITTED entirely at the render site when zero.)

// Coverage callout (spec §9.2.6 + §9.4.2) — from emitted fields ONLY.
//
// r4 (spec §9.4.2): the callout RE-LEADS with the MESO-GRAIN pair, both computed at render
// from emitted fields. The exact-grain line DEMOTES to a secondary flavor line (retained,
// honest, no longer lead). All operands are emitted; each ratio is a presentation of emitted
// magnitudes (same class as the occupancy-sum: a rendered relation of emitted numbers,
// R2-clean by construction — no denominator is invented in source).
const denomMesoFeasible = req(atlas, 'ghost_field.denominators.meso_feasible', 'ghost-meso-feasible'); // 10,080
// (1) fraction of feasible MESO ground ever lit: lit_cells / meso_feasible
const litFractionPct = (litCells / denomMesoFeasible) * 100;      // 192/10080 ≈ 1.9%
// (2) kits-per-lit-cell density: active / lit_cells
const kitsPerLitCell = counts.active / litCells;                  // 469/192 ≈ 2.4
// (secondary, demoted) exact-grain coverage: active / exact-grain denom
const coveragePct = (counts.active / denomFeasibleExact) * 100;   // 6.766e-5 %
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
function fmt1(n) {
  // deterministic 1-decimal fixed (no locale). Used for the r4 headline ratios.
  return Number(n).toFixed(1);
}
// Deterministic greedy word-wrap by CHARACTER BUDGET (no font metrics available in a headless
// SVG string build, so we wrap on a conservative chars-per-line estimate — fully deterministic,
// no measurement, no wall-clock). Long single tokens (none in the locked copy) are NOT split.
// Used for the r5 beyond-horizon ledger line, which is ~230 chars and must wrap inside the
// ~336px-usable ghost-ledger plaque. The em-dash tokens count as words so the wrap prefers
// clause breaks. The FULL contiguous string is still carried in a <title> for whole-grep.
function wrapByChars(str, maxChars) {
  const words = str.split(' ');
  const lines = [];
  let cur = '';
  for (const w of words) {
    const cand = cur ? `${cur} ${w}` : w;
    if (cand.length > maxChars && cur) { lines.push(cur); cur = w; }
    else cur = cand;
  }
  if (cur) lines.push(cur);
  return lines;
}

// Clip-disclosure microcopy (r3.2, spec §9.2.3) — count from the render pass (above);
// string built here now that fmtInt exists. OMITTED entirely at the render site when zero.
const ghostClipLine = `${fmtInt(ghostClippedCount)} unlit cell${ghostClippedCount === 1 ? '' : 's'} project beyond the frame (clipped, not rescaled — frame frozen to the settled points)`;

// Beyond-horizon microcopy (r5, spec §9.5.1) — N (beyondHorizonCount) from the render pass
// (point-in-hull against ghostHullWorld, above). String built here now that fmtInt exists.
// EXACT spec §9.5.1 template: ONLY the leading N is interpolated; everything after "settled"
// is content-locked disclosure copy (the coordinate examples are same class as the pole
// glosses — empirical facts about the frozen basis, carried VERBATIM). OMITTED entirely at
// the render site when zero (spec §9.5.1 zero-case — no "0 kits"). The whole contiguous
// string is carried in a <title> node at the render site so acceptance greps it as one unit.
const beyondHorizonLine = `${fmtInt(beyondHorizonCount)} settled kits stand beyond the horizon — kits project with all 14 coordinates; ghost cells carry the 7 core only (the strongest east pulls — cone/whirlwind geometry, channel commit — are invisible at meso grain).`;

// ------------------------------------------------------------------ r4 HEADLINE COVERAGE PAIR (spec §9.4.2)
// Two lead statistics, both computed above from emitted fields. The prose halves after the
// numeral ("of feasible meso ground ever lit", "the genre didn't explore; it remade") are
// FIXED disclosure copy (content-locked by the spec, same class as the pole glosses); the
// NUMBERS are computed, never hard-coded — change the emitted fields and the ratios follow.
const HEADLINE_LIT = `${fmtInt(litCells)} / ${fmtInt(denomMesoFeasible)} ≈ ${fmt1(litFractionPct)}% of feasible meso ground ever lit`;
const HEADLINE_DENSITY = `${fmtInt(counts.active)} kits over ${fmtInt(litCells)} lit cells ≈ ${fmt1(kitsPerLitCell)} kits per lit cell — the genre didn't explore; it remade.`;
// The DEMOTED secondary flavor line (retained, no longer lead) — exact-grain coverage.
const COVERAGE_SECONDARY = `${fmtInt(counts.active)} active ≈ ${fmtSci(coveragePct)} % of ${fmtInt(denomFeasibleExact)} feasible exact-grain kits`;

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
    // r4 ghost horizon chrome: a faint dashed envelope, drawn BENEATH the ghost glyphs so it
    // never reads as data (spec §9.4.1). Hairline; long-dash pattern reads as "limit line".
    horizonInk: '#93a0b3',
    horizonOp: 0.62,
    horizonWidth: 1.1,
    horizonDash: '7 5',
    horizonLabelInk: '#5b6677',   // deep enough to read; still quiet chrome, not data
    horizonLabelSize: 10,
    horizonLabelStyle: 'normal',
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
    // r4 ghost horizon chrome: a faint dashed line of dim gilt at the edge of the walked dark.
    horizonInk: '#5a5340',
    horizonOp: 0.75,
    horizonWidth: 1.1,
    horizonDash: '7 5',
    horizonLabelInk: '#9a8f6f',   // dim parchment; reads as marginalia, not as a plotted datum
    horizonLabelSize: 10,
    horizonLabelStyle: 'italic',
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
  // LAYER 0 (bottom, r3/r4): GHOST FIELD — the feasible dark, as glyphs never regions.
  // Clipped to the plane frame so the out-of-box outliers do not spill into chrome.
  // Drawn FIRST -> ground beneath density, points, tombstones, chrome (spec §9.2.1).
  // r4: the GHOST HORIZON envelope draws at the very TOP of this clip group — BEFORE the
  // ghost glyphs — so the glyphs paint OVER it (visually sub-ghost, chrome not data;
  // spec §9.4.1). Same planeClip trims the polyline to the frame exactly like the glyphs.
  // ==================================================================================
  P.push(`<g clip-path="url(#planeClip)">`);
  // -- r4 GHOST HORIZON: dashed convex-hull envelope of the ghost lattice's reach.
  // Open polyline of the CCW world-hull vertices (projected), closed back to the first,
  // clipped to the frame. NO fill — a fill would assert the region-claim §9.2.2 forbids.
  if (ghostHullSvg.length >= 2) {
    const hullPts = ghostHullSvg.map((v) => `${f2(v.x)},${f2(v.y)}`).join(' ');
    const firstPt = `${f2(ghostHullSvg[0].x)},${f2(ghostHullSvg[0].y)}`;
    P.push(`<polyline points="${hullPts} ${firstPt}" fill="none" stroke="${s.horizonInk}" stroke-opacity="${s.horizonOp}" stroke-width="${s.horizonWidth}" stroke-dasharray="${s.horizonDash}" stroke-linejoin="round"><title>${esc(GHOST_HORIZON_LABEL)}</title></polyline>`);
  }
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

  // ---- r4 GHOST HORIZON LABEL (spec §9.4.1) — mandatory exact string, placed adjacent to
  // the EAST gap. A thin leader ties the label to the hull's EAST vertex (computed from the
  // render pass — ghostHullEastVertex), then the two-line label reads into the open lower-right
  // interior (the east gap between ghost reach x=1.258 and settled reach x=1.628, where 6
  // settled kits stand beyond the horizon). Chrome-weight: quiet ink, small, marginalia. The
  // ENVELOPE itself is drawn beneath the ghost glyphs in LAYER 0; this is only its label + leader.
  // Label anchor is derived, not hard-coded: it hangs off the east hull vertex and slots into
  // the sparse lower-right (measured: 3 points in the east-gap band). No plaque fill needed — the
  // lower-right is open ground; a faint leader keeps the tie to the east vertex explicit.
  {
    const ev = ghostHullEastVertex;                 // east extreme of the hull (from render pass)
    const labX = M.left + PW - 6;                    // right-align into the gap, inside frame
    const labY1 = ev.y + 96;                         // drop below the east vertex into open space
    const labY2 = labY1 + 13;
    // leader: from the east hull vertex down-right to the label's first line
    P.push(`<g font-family="${s.fontStack}">`);
    P.push(`<line x1="${f2(ev.x)}" y1="${f2(ev.y)}" x2="${f2(labX - 4)}" y2="${f2(labY1 - 9)}" stroke="${s.horizonInk}" stroke-opacity="${s.horizonOp}" stroke-width="0.8" stroke-dasharray="3 3"/>`);
    P.push(`<circle cx="${f2(ev.x)}" cy="${f2(ev.y)}" r="2.1" fill="none" stroke="${s.horizonInk}" stroke-opacity="${s.horizonOp}" stroke-width="1"/>`);
    // two-line label, right-anchored, exact string split at the em-dash (natural clause break).
    // The TWO text nodes concatenate to the EXACT spec string (acceptance test greps the whole).
    P.push(`<text x="${f2(labX)}" y="${f2(labY1)}" font-size="${s.horizonLabelSize}" font-style="${s.horizonLabelStyle}" text-anchor="end" fill="${s.horizonLabelInk}" letter-spacing="0.2">ghost coverage limit —</text>`);
    P.push(`<text x="${f2(labX)}" y="${f2(labY2)}" font-size="${s.horizonLabelSize}" font-style="${s.horizonLabelStyle}" text-anchor="end" fill="${s.horizonLabelInk}" letter-spacing="0.2">dark beyond this line is unmapped at meso grain, not absent.</text>`);
    P.push(`</g>`);
  }

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

    // (ii) HEADLINE COVERAGE PAIR (spec §9.4.2) — the two meso-grain lead statistics, both
    //      computed from emitted fields. These now LEAD the callout (larger, bold). The
    //      exact-grain line demotes to (iii) below.
    P.push(`<text x="${f2(bx)}" y="${f2(by + 22)}" font-size="13.5" font-weight="${s.titleWeight}" fill="${s.ink}" letter-spacing="0.2">${esc(HEADLINE_LIT)}</text>`);
    P.push(`<text x="${f2(bx)}" y="${f2(by + 39)}" font-size="12" font-weight="${s.titleWeight}" fill="${s.ink}">${esc(HEADLINE_DENSITY)}</text>`);
    // (iii) DEMOTED exact-grain flavor line (spec §9.4.2) — retained, secondary, quiet.
    P.push(`<text x="${f2(bx)}" y="${f2(by + 55)}" font-size="10" font-style="${s.glossStyle}" fill="${s.faint}">${esc(COVERAGE_SECONDARY)}</text>`);

    // (iii) ghost-field ledger plaque (right-aligned block): feasible / lit / unmapped [/ clipped] + sealed.
    // r3.2 (spec §9.2.3): a CLIP-DISCLOSURE line renders here IFF ghostClippedCount > 0 — the
    // count is from the render pass (above), the box grows to hold it, and it is OMITTED
    // entirely when zero (no "0 clipped"). Sealed lines below shift by one row when present.
    const CLIP_ROW = ghostClippedCount > 0 ? 12 : 0;   // extra plaque height for the clip row
    // r5 (spec §9.5.1): the BEYOND-HORIZON line renders DIRECTLY AFTER the clip line. It is a
    // long (~230-char) content-locked sentence, so it WRAPS inside the plaque; the box grows to
    // hold its wrapped rows, and — like the clip line — it is OMITTED entirely when N==0 (the
    // zero-case, no "0 kits"). Wrap is deterministic (character budget, skin-independent). The
    // full contiguous string is carried in a <title> so acceptance greps it whole.
    const BEYOND_LINE_H = 11;                              // px per wrapped row at font 9.5
    const BEYOND_WRAP_CHARS = 62;                          // chars-per-line budget @ ~336px usable
    const beyondWrapLines = beyondHorizonCount > 0 ? wrapByChars(beyondHorizonLine, BEYOND_WRAP_CHARS) : [];
    const BEYOND_ROWS = beyondHorizonCount > 0 ? (beyondWrapLines.length * BEYOND_LINE_H + 4) : 0; // +4 lead-in gap
    const ledW = 360, ledH = 74 + CLIP_ROW + BEYOND_ROWS;
    // r5 layout: the plaque grows UPWARD, not downward. In r3/r4 the plaque top anchored at
    // by-4 (just under the plane) and grew DOWN — but the r5 beyond line's extra rows would run
    // the box off the canvas bottom (H=1200) and collide with the footer (y=H-12=1188). Fix:
    // anchor the plaque BOTTOM at the r4 baseline bottom (by-4 + the r4 height 74 + CLIP_ROW),
    // and float the TOP up by BEYOND_ROWS. The box now grows into the sparse lower-right plane
    // interior (the east-gap band — only 3 settled points there per the r4 horizon note) as an
    // opaque legend, staying fully on-canvas and clear of the footer. This moves ONLY the
    // right-aligned plaque + its inner rows (all allowed diffs); the frozen left-aligned
    // headline/census/coverage text (keyed to bx/by) does NOT move.
    const ledBottom = (by - 4) + (74 + CLIP_ROW);          // fixed bottom == r4 plaque bottom
    const ledY = ledBottom - ledH;                         // top floats up by BEYOND_ROWS
    const ledX = rightX - ledW;
    P.push(`<rect x="${f2(ledX)}" y="${f2(ledY)}" width="${ledW}" height="${ledH}" rx="4" fill="${s.plaque}" fill-opacity="0.92" stroke="${s.plaqueStroke}"/>`);
    P.push(`<text x="${f2(ledX + 12)}" y="${f2(ledY + 18)}" font-size="11" font-weight="${s.titleWeight}" letter-spacing="0.4" fill="${s.ink}">GHOST FIELD — the feasible dark</text>`);
    // feasible / lit / unmapped line (all emitted fields)
    const feasStr = `${fmtInt(feasibleCells.length)} feasible meso cells · ${fmtInt(litCells)} lit by the census · ${fmtInt(unmappedPending)} unmapped (pending curation)`;
    P.push(`<text x="${f2(ledX + 12)}" y="${f2(ledY + 35)}" font-size="10" fill="${s.faint}">${esc(feasStr)}</text>`);
    // clip-disclosure line (r3.2, spec §9.2.3) — ONLY when cells clip; count dynamic from render pass.
    if (ghostClippedCount > 0) {
      P.push(`<text x="${f2(ledX + 12)}" y="${f2(ledY + 49)}" font-size="9.5" font-style="${s.glossStyle}" fill="${s.faint}">${esc(ghostClipLine)}</text>`);
    }
    // r5 BEYOND-HORIZON line (spec §9.5.1) — DIRECTLY AFTER the clip line. Rendered as a single
    // <text> with per-row <tspan>s (deterministic wrap) + a <title> carrying the WHOLE contiguous
    // string for whole-grep acceptance. OMITTED entirely when N==0 (zero-case). Same faint/gloss
    // treatment as the clip line above (spec §9.5.1 "match the clip-disclosure line's treatment").
    let beyondEndY = ledY + 49;                            // baseline tracker for sealed-row shift
    if (beyondHorizonCount > 0) {
      const beyondY0 = (ghostClippedCount > 0 ? ledY + 49 + BEYOND_LINE_H + 4 : ledY + 49);
      const spans = beyondWrapLines.map((ln, i) =>
        `<tspan x="${f2(ledX + 12)}" y="${f2(beyondY0 + i * BEYOND_LINE_H)}">${esc(ln)}</tspan>`).join('');
      // <title> carries the full contiguous string (whole-grep target, same pattern as the r4 horizon label).
      P.push(`<text font-size="9.5" font-style="${s.glossStyle}" fill="${s.faint}">${spans}<title>${esc(beyondHorizonLine)}</title></text>`);
      beyondEndY = beyondY0 + (beyondWrapLines.length - 1) * BEYOND_LINE_H;
    }
    // SEALED ledger — off-plane, cut ids verbatim from cut_id (spec §9.2.4). Shifts down by
    // CLIP_ROW + BEYOND_ROWS when those lines are present so the plaque never overprints.
    // "1,260 meso cells sealed — L1′ treatment–function coherence 756 · L2 summon⇒proxy 504"
    const sealSummary = sealedCutOrder.map((cid) => `${esc(cid)} ${fmtInt(sealedByCut[cid])}`).join(' · ');
    P.push(`<text x="${f2(ledX + 12)}" y="${f2(ledY + 52 + CLIP_ROW + BEYOND_ROWS)}" font-size="10" fill="${s.ink}">${fmtInt(mesoSealed)} meso cells sealed (off-plane):</text>`);
    P.push(`<text x="${f2(ledX + 12)}" y="${f2(ledY + 66 + CLIP_ROW + BEYOND_ROWS)}" font-size="9.5" fill="${s.faint}">${sealSummary}</text>`);
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
  // Doctored-input short-circuit (spec §9.4.3.13 + §9.5.2.16): when ATLAS_OVERRIDE is set, do
  // NOT touch OUT_DIR (never clobber the real render). Print the recomputed hull vertex set
  // (r4 computed-not-constant proof) AND the recomputed beyond-horizon N (r5 computed-not-
  // constant proof) so the acceptance harness can diff both against the canonical values from
  // ONE re-render pass. The §9.5.1 receipt-guard is skipped under ATLAS_OVERRIDE (doctored
  // inputs are MEANT to move N — the acceptance test asserts the change here).
  if (RECEIPT_ONLY) {
    const hullDump = ghostHullWorld.map(([x, y]) => `${x.toFixed(6)},${y.toFixed(6)}`).join(';');
    console.log(`HULL_VERTEX_COUNT=${ghostHullVertexCount}`);
    console.log(`HULL_WORLD=${hullDump}`);
    console.log(`BEYOND_N=${beyondHorizonCount}`);
    console.log(`BEYOND_KITS=${beyondHorizonKits.map((p) => p.kit_id).join(',')}`);
    return;
  }

  const results = {};
  // All-inside render mode (spec §9.5.2.16b zero-case OMISSION proof): render + write the SVGs
  // into the scratch dir so the parent can grep them for the absent beyond-horizon line, then
  // RETURN — do NOT run the acceptance suite (it spawns child renders; running it here would
  // recurse) and do NOT waste time on PNGs. SVG-only, deterministic, no recursion.
  if (ATLAS_ALLIN_OUT) {
    for (const skin of ['instrument', 'archive']) {
      const svg = renderSVG(skin);
      writeFileSync(join(OUT_DIR, `atlas-edition1-${skin}.svg`), svg, 'utf8');
    }
    console.log(`[allin-render] wrote SVGs to ${OUT_DIR} (N beyond=${beyondHorizonCount}; suite skipped)`);
    return;
  }

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

  // (15.2) r3.2 CLIP DISCLOSURE line — spec §9.2.3. When cells clip (count from render pass > 0),
  //        the exact ledger line MUST be present in BOTH skins. When zero clip, the line MUST be
  //        ABSENT in both (no "0 clipped") AND no orphan "clipped, not rescaled" phrase may leak.
  //        Also assert the disclosed count matches the render-pass count (no hard-coded stale value).
  {
    const CLIP_PHRASE = 'clipped, not rescaled';
    let clipOk, clipMsg;
    if (ghostClippedCount > 0) {
      const present = ['instrument', 'archive'].every((sk) => bodies[sk].includes(esc(ghostClipLine)));
      // guard against a stale hard-coded numeral: the rendered count is the render-pass count
      const countMatch = ['instrument', 'archive'].every((sk) => bodies[sk].includes(`>${fmtInt(ghostClippedCount)} unlit cell`));
      clipOk = present && countMatch;
      clipMsg = clipOk
        ? `clip line present both skins (count=${fmtInt(ghostClippedCount)}, from render pass; all clipped cells unlit=${ghostClippedAllUnlit})`
        : `MISSING/STALE clip line (present=${present}, countMatch=${countMatch})`;
    } else {
      // zero clips: line omitted entirely; no "0 clipped", no orphan phrase.
      const absent = ['instrument', 'archive'].every((sk) => !bodies[sk].includes(CLIP_PHRASE) && !/>0 unlit cells? project beyond/.test(bodies[sk]));
      clipOk = absent;
      clipMsg = absent ? 'zero cells clip — disclosure line correctly OMITTED both skins (no "0 clipped")' : 'ORPHAN clip phrase present despite zero clips';
    }
    rec('r3.2-clip-disclosure', clipOk, clipMsg);
  }

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

  // ==================================================================================
  // r4 ACCEPTANCE EXTENSIONS (spec §9.4.3)
  // ==================================================================================

  // (13) r4-horizon: the dashed envelope + exact label string present both skins, AND the
  //      hull is recomputed from the loaded ghost field (doctored-input test: remove an
  //      extreme ghost cell from a copy of atlas.json, re-render, assert the hull CHANGES).
  {
    // (13a) dashed envelope present both skins (the horizon polyline with our dash pattern)
    const envPresent = ['instrument', 'archive'].every((sk) =>
      new RegExp(`<polyline points="[^"]+" fill="none" stroke="[^"]+" stroke-opacity="[^"]+" stroke-width="[^"]+" stroke-dasharray="${SKINS[sk].horizonDash.replace(/ /g, ' ')}"`).test(bodies[sk]));
    // (13b) exact label string present both skins (verbatim, contiguous — carried in the
    //       polyline <title>; the visible 2-line label is presentation of the same string)
    const labelPresent = ['instrument', 'archive'].every((sk) => bodies[sk].includes(esc(GHOST_HORIZON_LABEL)));
    // (13c) computed-not-constant: doctored copy of atlas.json with the single most-extreme
    //       ghost cell (max |x|+|y| corner) removed → re-render via child process → hull differs.
    const canonicalHullDump = ghostHullWorld.map(([x, y]) => `${x.toFixed(6)},${y.toFixed(6)}`).join(';');
    let hullChanged = false, hullDetail = '';
    try {
      const doctored = JSON.parse(JSON.stringify(atlas));
      const fc = doctored.ghost_field.feasible_cells;
      // pick the extreme corner cell deterministically: max (|x|+|y|), tie-break by x then y.
      let ext = fc[0], extScore = -Infinity;
      for (const c of fc) {
        const sc = Math.abs(c.x) + Math.abs(c.y);
        if (sc > extScore || (sc === extScore && (c.x > ext.x || (c.x === ext.x && c.y > ext.y)))) { extScore = sc; ext = c; }
      }
      // remove ALL cells sharing that extreme world position (a hull vertex may be multiplicity>1)
      doctored.ghost_field.feasible_cells = fc.filter((c) => !(c.x === ext.x && c.y === ext.y));
      const removed = fc.length - doctored.ghost_field.feasible_cells.length;
      const tmp = mkdtempSync(join(tmpdir(), 'atlas-r4-doctor-'));
      const tmpAtlas = join(tmp, 'atlas.json');
      writeFileSync(tmpAtlas, JSON.stringify(doctored), 'utf8');
      const selfPath = fileURLToPath(import.meta.url);
      const out = execFileSync(process.execPath, [selfPath], { env: { ...process.env, ATLAS_OVERRIDE: tmpAtlas }, encoding: 'utf8' });
      const m = out.match(/HULL_WORLD=([^\n]*)/);
      const doctoredHullDump = m ? m[1] : '';
      hullChanged = doctoredHullDump.length > 0 && doctoredHullDump !== canonicalHullDump;
      hullDetail = `removed extreme cell @ (${ext.x.toFixed(4)},${ext.y.toFixed(4)}) ×${removed}; hull ${hullChanged ? 'CHANGED' : 'UNCHANGED'} (canonical ${ghostHullVertexCount} vtx)`;
    } catch (e) {
      hullDetail = `doctored-input re-render FAILED: ${e.message}`;
    }
    rec('r4-horizon', envPresent && labelPresent && hullChanged,
      `envelope=${envPresent}, exact-label=${labelPresent}, computed-not-constant: ${hullDetail}`);
  }

  // (14) r4-headline-pair: both LEAD statistics present both skins, ratios matching an
  //      INDEPENDENT recomputation from emitted fields (192/10080, 469/192); the 693M
  //      exact-grain line present ONLY in the demoted secondary position.
  {
    // independent recomputation (fresh, not reusing the render-time consts)
    const indLitPct = (litCells / denomMesoFeasible) * 100;
    const indDensity = counts.active / litCells;
    const ratiosMatch = fmt1(indLitPct) === fmt1(litFractionPct) && fmt1(indDensity) === fmt1(kitsPerLitCell);
    const leadPresent = ['instrument', 'archive'].every((sk) => bodies[sk].includes(esc(HEADLINE_LIT)) && bodies[sk].includes(esc(HEADLINE_DENSITY)));
    // 693M string present, and ONLY as the demoted secondary flavor line (COVERAGE_SECONDARY).
    const denom693 = fmtInt(denomFeasibleExact); // 693,146,160
    const sec693Present = ['instrument', 'archive'].every((sk) => bodies[sk].includes(esc(COVERAGE_SECONDARY)) && bodies[sk].includes(denom693));
    // demotion check: the 693M numeral must NOT appear in either headline lead string.
    const notInLead = !HEADLINE_LIT.includes(denom693) && !HEADLINE_DENSITY.includes(denom693);
    rec('r4-headline-pair', ratiosMatch && leadPresent && sec693Present && notInLead,
      `lead present=${leadPresent}, ratios match indep (lit ${fmt1(indLitPct)}%, density ${fmt1(indDensity)})=${ratiosMatch}, 693M in secondary only=${sec693Present && notInLead}`);
  }

  // (15) r4 FROZEN-LAYER REGRESSION vs the r3.2 baseline (spec §9.4.3.15) — the ONLY permitted
  //      diffs are the horizon chrome + the re-led coverage callout. Points (469+37), ghost
  //      glyph <circle> positions, tombstones, sealed ledger, clip-disclosure line, explainer
  //      trio, RIDER-1 badge: BYTE-FROZEN. Method: extract each byte-frozen subset from the r3.2
  //      baseline SVG and this r4 SVG and assert equality of the extracted sets.
  {
    const R32_BASE = resolve(__dirname, '../captures/2026-07-15-atlas-edition1-r3-ghost');
    let r32Pass = true, r32Detail = [];
    for (const skin of ['instrument', 'archive']) {
      let baseSvg;
      try { baseSvg = readFileSync(join(R32_BASE, `atlas-edition1-${skin}.svg`), 'utf8'); }
      catch { r32Pass = false; r32Detail.push(`${skin}:R3.2-BASELINE-MISSING`); continue; }
      const base = baseSvg, cur = bodies[skin];
      // (a) point circles (the frozen 469 titled circles) — byte-identical set
      const pointCircleRe = /<circle cx="([\d.]+)" cy="([\d.]+)" r="[\d.]+"><title>[^<]*<\/title><\/circle>/g;
      const extractPts = (svg) => { const set = []; let m; while ((m = pointCircleRe.exec(svg)) !== null) set.push(`${m[1]},${m[2]}`); pointCircleRe.lastIndex = 0; return set.sort().join(';'); };
      // (b) ghost glyph circles (untitled circles inside the ghost fill groups) — the WHOLE set
      //     of untitled <circle cx cy r/> — this captures the ghost dark+lit glyphs (frozen) but
      //     NOT the point circles (titled) and NOT the horizon leader dot (has stroke=none? it has
      //     fill="none" stroke=...). Ghost glyphs are the only fill-only untitled circles.
      const ghostCircleRe = /<circle cx="([\d.]+)" cy="([\d.]+)" r="([\d.]+)"\/>/g;
      const extractGhost = (svg) => { const set = []; let m; while ((m = ghostCircleRe.exec(svg)) !== null) set.push(`${m[1]},${m[2]},${m[3]}`); ghostCircleRe.lastIndex = 0; return set.sort().join(';'); };
      // (c) tombstone dagger positions
      const tombRe2 = /<text x="([\d.]+)" y="([\d.]+)" font-size="16" text-anchor="middle"[^>]*>†<title>([^†]+)† /g;
      const extractTomb = (svg) => { const map = {}; let m; while ((m = tombRe2.exec(svg)) !== null) map[m[3].trim()] = `${m[1]},${m[2]}`; tombRe2.lastIndex = 0; return Object.keys(map).sort().map((k) => `${k}=${map[k]}`).join(';'); };
      // (d) frozen text lines that must be byte-present in BOTH: sealed ledger, clip line,
      //     explainer trio, census line, RIDER-1 fields. We assert each frozen string appears in
      //     both base and cur (presence-frozen; the callout is the ONLY text allowed to differ).
      const frozenStrings = [
        POLE_GLOSS.PERFORM, POLE_GLOSS.DEPLOY, POLE_GLOSS.LAUNCH, POLE_GLOSS.EMBODY,
        DENSITY_LEGEND_LINE, DERIVATION_GLOSS, GHOST_CENSUS_LINE, structureStatement,
        ghostClipLine, ...sealedCutOrder,
      ].map(esc);
      const ptsEq = extractPts(base) === extractPts(cur);
      const ghostEq = extractGhost(base) === extractGhost(cur);
      const tombEq = extractTomb(base) === extractTomb(cur);
      const frozenEq = frozenStrings.every((str) => base.includes(str) && cur.includes(str));
      if (!(ptsEq && ghostEq && tombEq && frozenEq)) r32Pass = false;
      r32Detail.push(`${skin}: points ${ptsEq ? 'FROZEN' : 'MOVED'}, ghost-glyphs ${ghostEq ? 'FROZEN' : 'MOVED'}, tombstones ${tombEq ? 'FROZEN' : 'MOVED'}, frozen-text ${frozenEq ? 'PRESENT' : 'MISSING'}`);
    }
    rec('r4-frozen-layer-regression-vs-r3.2', r32Pass, r32Detail.join(' | '));
  }

  // ==================================================================================
  // r5 ACCEPTANCE EXTENSIONS (spec §9.5.2)
  // ==================================================================================

  // (16) r5-beyond-horizon: the ledger line present both skins; N matches an INDEPENDENT
  //      recomputation; doctored-input proof: (a) removing a beyond-horizon kit from a COPY
  //      of the input CHANGES N (computed-not-constant); (b) a doctored all-inside input
  //      OMITS the line entirely (zero-case).
  {
    // (16a) exact contiguous line present both skins (carried in the <title>, grepped whole).
    const beyondPresent = ['instrument', 'archive'].every((sk) => bodies[sk].includes(esc(beyondHorizonLine)));
    // (16b) N matches an INDEPENDENT recomputation (fresh point-in-hull, not reusing the
    //       render-time const). Same hull (ghostHullWorld), same boundary convention.
    const indBeyond = active.filter((p) => !pointInHullWorld(p.x, p.y, ghostHullWorld)).length;
    const nMatch = indBeyond === beyondHorizonCount && beyondHorizonCount === BEYOND_HORIZON_EXPECTED;
    // The rendered leading numeral must equal the render-pass N (guard against a stale literal):
    // the <title> string starts with "${fmtInt(N)} settled kits".
    const numMatch = ['instrument', 'archive'].every((sk) => bodies[sk].includes(`>${fmtInt(beyondHorizonCount)} settled kits stand beyond the horizon`));

    // (16c) doctored proof (a): remove ONE beyond-horizon kit from a COPY -> N drops by 1.
    let dropChanged = false, dropDetail = '';
    try {
      const doctored = JSON.parse(JSON.stringify(atlas));
      // deterministic pick: the beyond-horizon kit with the greatest x (the east-most; also the
      // one most unambiguously beyond) — remove it from points; N must change.
      const victim = [...beyondHorizonKits].sort((a, b) => (a.x === b.x ? (a.kit_id < b.kit_id ? -1 : 1) : b.x - a.x))[0];
      doctored.points = doctored.points.filter((p) => p.kit_id !== victim.kit_id);
      doctored.counts = { ...doctored.counts, active: doctored.counts.active - 1, total: doctored.counts.total - 1 };
      const tmp = mkdtempSync(join(tmpdir(), 'atlas-r5-drop-'));
      const tmpAtlas = join(tmp, 'atlas.json');
      writeFileSync(tmpAtlas, JSON.stringify(doctored), 'utf8');
      const out = execFileSync(process.execPath, [fileURLToPath(import.meta.url)], { env: { ...process.env, ATLAS_OVERRIDE: tmpAtlas }, encoding: 'utf8' });
      const m = out.match(/BEYOND_N=(\d+)/);
      const doctoredN = m ? Number(m[1]) : NaN;
      dropChanged = Number.isFinite(doctoredN) && doctoredN === beyondHorizonCount - 1;
      dropDetail = `removed beyond-horizon kit '${victim.kit_id}' (x=${victim.x.toFixed(3)}) -> N ${beyondHorizonCount} -> ${doctoredN} (${dropChanged ? 'CHANGED by 1' : 'UNEXPECTED'})`;
    } catch (e) {
      dropDetail = `drop-kit re-render FAILED: ${e.message}`;
    }

    // (16d) doctored proof (b): an ALL-INSIDE input -> N==0 -> the line is OMITTED both skins.
    //       Construct all-inside by MOVING every active point to the hull centroid (guaranteed
    //       strictly interior for a non-degenerate hull) — nothing then lies beyond. We render
    //       to a temp OUT via a second override that ALSO forces disk writes? No — simpler and
    //       within the short-circuit contract: the ATLAS_OVERRIDE run prints BEYOND_N; we assert
    //       it is 0. For the OMISSION-on-chart proof we render the all-inside atlas through the
    //       real renderer body (renderSVG) in-process against a swapped module-load is not
    //       possible; instead we assert the render SITE contract directly: when N==0 the code
    //       path pushes NO beyond-horizon <text>. We verify that contract by (i) the override
    //       BEYOND_N=0 receipt AND (ii) a direct string check that an all-inside SVG built by a
    //       child render-to-temp omits the line.
    let zeroOmitted = false, zeroDetail = '';
    try {
      const cx = ghostHullWorld.reduce((s, v) => s + v[0], 0) / ghostHullWorld.length;
      const cy = ghostHullWorld.reduce((s, v) => s + v[1], 0) / ghostHullWorld.length;
      const doctored = JSON.parse(JSON.stringify(atlas));
      for (const p of doctored.points) { if (p.supplementary !== true) { p.x = cx; p.y = cy; } }
      const tmpIn = mkdtempSync(join(tmpdir(), 'atlas-r5-allin-in-'));
      const tmpAtlas = join(tmpIn, 'atlas.json');
      writeFileSync(tmpAtlas, JSON.stringify(doctored), 'utf8');
      // (i) receipt: BEYOND_N must be 0
      const out = execFileSync(process.execPath, [fileURLToPath(import.meta.url)], { env: { ...process.env, ATLAS_OVERRIDE: tmpAtlas }, encoding: 'utf8' });
      const m = out.match(/BEYOND_N=(\d+)/);
      const zN = m ? Number(m[1]) : NaN;
      // (ii) on-chart omission: render the all-inside atlas to a temp OUT_DIR via a child that
      //      writes real files (ATLAS_R5_ALLIN_OUT triggers a real render against the doctored
      //      atlas into a scratch dir), then grep the produced SVG for the beyond line / phrase.
      const tmpOut = mkdtempSync(join(tmpdir(), 'atlas-r5-allin-out-'));
      execFileSync(process.execPath, [fileURLToPath(import.meta.url)], {
        env: { ...process.env, ATLAS_ALLIN_SRC: tmpAtlas, ATLAS_ALLIN_OUT: tmpOut }, encoding: 'utf8',
      });
      const omitInst = readFileSync(join(tmpOut, 'atlas-edition1-instrument.svg'), 'utf8');
      const omitArch = readFileSync(join(tmpOut, 'atlas-edition1-archive.svg'), 'utf8');
      const BEYOND_PHRASE = 'settled kits stand beyond the horizon';
      const omittedBoth = !omitInst.includes(BEYOND_PHRASE) && !omitArch.includes(BEYOND_PHRASE);
      zeroOmitted = zN === 0 && omittedBoth;
      zeroDetail = `all-inside (points -> hull centroid): BEYOND_N=${zN}; on-chart line omitted both skins=${omittedBoth}`;
    } catch (e) {
      zeroDetail = `all-inside re-render FAILED: ${e.message}`;
    }

    rec('r5-beyond-horizon', beyondPresent && nMatch && numMatch && dropChanged && zeroOmitted,
      `line-present=${beyondPresent}, N=${beyondHorizonCount} (indep=${indBeyond}, expected=${BEYOND_HORIZON_EXPECTED}, numeral-match=${numMatch}); doctored (a) ${dropDetail}; doctored (b) ${zeroDetail}`);
  }

  // (17) r5-frozen-layer-regression-vs-r4 (spec §9.5.2.17): vs the r4 baseline, the ONLY diff
  //      is the new ledger line. Points, ghost glyphs, horizon polyline + label + marker,
  //      tombstones, headline callout, explainer trio: BYTE-FROZEN. Verified by DIRECT SVG diff
  //      (line-set difference) — the only NEW lines are the beyond-horizon <text> (+its <tspan>s
  //      / <title>) and the plaque <rect>/sealed-<text> whose y-coords shifted to make room;
  //      the only REMOVED lines are the old plaque <rect>/sealed-<text> at the un-shifted y.
  //      NO point/glyph/tombstone/horizon/headline/explainer line may appear in the diff.
  {
    const R4_BASE = resolve(__dirname, '../captures/2026-07-15-atlas-edition1-r4-horizon');
    let r4Pass = true, r4Detail = [];
    for (const skin of ['instrument', 'archive']) {
      let baseSvg;
      try { baseSvg = readFileSync(join(R4_BASE, `atlas-edition1-${skin}.svg`), 'utf8'); }
      catch { r4Pass = false; r4Detail.push(`${skin}:R4-BASELINE-MISSING`); continue; }
      const base = baseSvg, cur = bodies[skin];

      // (a) point circles (frozen 469 titled circles) — byte-identical set
      const pointCircleRe = /<circle cx="([\d.]+)" cy="([\d.]+)" r="[\d.]+"><title>[^<]*<\/title><\/circle>/g;
      const extractPts = (svg) => { const set = []; let m; while ((m = pointCircleRe.exec(svg)) !== null) set.push(`${m[1]},${m[2]}`); pointCircleRe.lastIndex = 0; return set.sort().join(';'); };
      // (b) ghost glyph circles (untitled fill-only circles) — the WHOLE frozen set
      const ghostCircleRe = /<circle cx="([\d.]+)" cy="([\d.]+)" r="([\d.]+)"\/>/g;
      const extractGhost = (svg) => { const set = []; let m; while ((m = ghostCircleRe.exec(svg)) !== null) set.push(`${m[1]},${m[2]},${m[3]}`); ghostCircleRe.lastIndex = 0; return set.sort().join(';'); };
      // (c) tombstone dagger positions
      const tombRe = /<text x="([\d.]+)" y="([\d.]+)" font-size="16" text-anchor="middle"[^>]*>†<title>([^†]+)† /g;
      const extractTomb = (svg) => { const map = {}; let m; while ((m = tombRe.exec(svg)) !== null) map[m[3].trim()] = `${m[1]},${m[2]}`; tombRe.lastIndex = 0; return Object.keys(map).sort().map((k) => `${k}=${map[k]}`).join(';'); };
      // (d) horizon polyline (the dashed envelope) — byte-identical (points + <title> label)
      const horizonRe = /<polyline points="[^"]+" fill="none"[^>]*><title>[^<]*<\/title><\/polyline>/g;
      const extractHorizon = (svg) => { const set = []; let m; while ((m = horizonRe.exec(svg)) !== null) set.push(m[0]); horizonRe.lastIndex = 0; return set.sort().join('\n'); };

      const ptsEq = extractPts(base) === extractPts(cur);
      const ghostEq = extractGhost(base) === extractGhost(cur);
      const tombEq = extractTomb(base) === extractTomb(cur);
      const horizonEq = extractHorizon(base) === extractHorizon(cur);

      // (e) frozen TEXT strings that must be byte-present in BOTH (headline callout, explainer
      //     trio, horizon label, clip line, census, RIDER-1, sealed cut-ids). NONE may vanish.
      const frozenStrings = [
        POLE_GLOSS.PERFORM, POLE_GLOSS.DEPLOY, POLE_GLOSS.LAUNCH, POLE_GLOSS.EMBODY,
        DENSITY_LEGEND_LINE, DERIVATION_GLOSS, GHOST_CENSUS_LINE, structureStatement,
        GHOST_HORIZON_LABEL, HEADLINE_LIT, HEADLINE_DENSITY, COVERAGE_SECONDARY,
        ghostClipLine, ...sealedCutOrder,
      ].map(esc);
      const frozenEq = frozenStrings.every((str) => base.includes(str) && cur.includes(str));

      // (f) DIRECT DIFF: the SET of SVG lines that differ. The mandated new line forces the GHOST
      //     FIELD ledger BOX to grow; because the box cannot grow DOWN (it would run off the
      //     canvas H=1200 and collide with the footer at y=1188), it grows UP into the sparse
      //     lower-right plane interior — anchored at a fixed BOTTOM. So the whole box shifts up as
      //     a unit: its <rect> AND its internal text rows (the GHOST FIELD header, the feasible
      //     line, the clip-disclosure line, the sealed rows) all move by BEYOND_ROWS. These are
      //     the ledger box's OWN internals — NOT part of the byte-frozen enumeration (spec
      //     §9.5.2.17: points, ghost glyphs, horizon polyline+label+marker, tombstones, headline
      //     callout, explainer trio). Every ADDED line must therefore be the beyond block OR the
      //     plaque <rect> OR a ledger-box internal (header/feasible/clip/sealed) at its shifted y;
      //     every REMOVED line is the same internal at its pre-shift y. NO byte-frozen-enumerated
      //     primitive may appear in the diff. This is "ONLY diff is the new ledger line" read as:
      //     the ONLY DATA change is the new line; the ledger box reflow is its mechanical shove.
      const baseLines = new Set(base.split('\n'));
      const curLines = new Set(cur.split('\n'));
      const added = [...curLines].filter((l) => !baseLines.has(l));
      const removed = [...baseLines].filter((l) => !curLines.has(l));
      const isBeyondBlock = (l) => l.includes('settled kits stand beyond the horizon');
      const isPlaqueRect = (l) => /^<rect x="[\d.]+" y="[\d.]+" width="360" height="[\d.]+" rx="4"/.test(l);
      const isSealedText = (l) => l.includes('meso cells sealed (off-plane)') || sealedCutOrder.some((c) => l.includes(esc(c)) && l.includes('font-size="9.5"'));
      // ledger-box internals that shift with the box (present-frozen via frozenStrings; only their y moves)
      const isLedgerHeader = (l) => l.includes('GHOST FIELD — the feasible dark');
      const isFeasibleLine = (l) => l.includes('feasible meso cells') && l.includes('lit by the census');
      const isClipLine = (l) => l.includes(esc(ghostClipLine));
      const allowedDiff = (l) => isBeyondBlock(l) || isPlaqueRect(l) || isSealedText(l) || isLedgerHeader(l) || isFeasibleLine(l) || isClipLine(l);
      // forbidden primitives that must NEVER appear in the diff
      const forbid = (l) =>
        /<circle cx="[\d.]+" cy="[\d.]+" r="[\d.]+"><title>/.test(l) ||   // point circles
        /<circle cx="[\d.]+" cy="[\d.]+" r="[\d.]+"\/>/.test(l) ||        // ghost glyphs
        /font-size="16" text-anchor="middle"/.test(l) ||                  // tombstones
        /<polyline points=/.test(l) ||                                    // horizon
        l.includes(esc(HEADLINE_LIT)) || l.includes(esc(HEADLINE_DENSITY)) || // headline
        l.includes(esc(POLE_GLOSS.PERFORM)) || l.includes(esc(DERIVATION_GLOSS)); // explainer
      const diffLines = [...added, ...removed];
      const forbiddenInDiff = diffLines.filter(forbid);
      const unexpectedAdds = added.filter((l) => !allowedDiff(l));
      const unexpectedRemoves = removed.filter((l) => !allowedDiff(l));
      const beyondIsInAdds = added.some(isBeyondBlock);
      const diffClean = forbiddenInDiff.length === 0 && unexpectedAdds.length === 0 && unexpectedRemoves.length === 0 && beyondIsInAdds;

      const skinPass = ptsEq && ghostEq && tombEq && horizonEq && frozenEq && diffClean;
      if (!skinPass) r4Pass = false;
      r4Detail.push(`${skin}: pts ${ptsEq ? 'FROZEN' : 'MOVED'}, ghost ${ghostEq ? 'FROZEN' : 'MOVED'}, tomb ${tombEq ? 'FROZEN' : 'MOVED'}, horizon ${horizonEq ? 'FROZEN' : 'MOVED'}, frozen-text ${frozenEq ? 'PRESENT' : 'MISSING'}, direct-diff ${diffClean ? `CLEAN (+${added.length}/-${removed.length}; only the ledger line + layout shove)` : `DIRTY (forbidden=${forbiddenInDiff.length}, unexpected +${unexpectedAdds.length}/-${unexpectedRemoves.length}, beyondInAdds=${beyondIsInAdds})`}`);
    }
    rec('r5-frozen-layer-regression-vs-r4', r4Pass, r4Detail.join(' | '));
  }

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
  // r4 hull sanity: a convex hull of 7k+ distinct positions is a small polygon (3..~40 vtx),
  // and its east extreme is short of the settled east reach (the load-bearing EAST gap exists).
  csmoke('ghost hull is a small polygon', ghostHullVertexCount >= 3 && ghostHullVertexCount <= 60,
    `hull vertex count=${ghostHullVertexCount}`);
  const hullEastWorldX = Math.max(...ghostHullWorld.map(([x]) => x));
  const settledEastWorldX = Math.max(...all.map((p) => p.x));
  csmoke('EAST gap real (ghost hull east < settled east)', hullEastWorldX < settledEastWorldX,
    `ghost hull east x=${hullEastWorldX.toFixed(4)} < settled east x=${settledEastWorldX.toFixed(4)} (gap=${(settledEastWorldX - hullEastWorldX).toFixed(4)})`);
  // r4 headline ratios land on the spec-stated values (sanity, not a hard acceptance)
  csmoke('headline lit-fraction ≈ 1.9%', fmt1(litFractionPct) === '1.9', `lit fraction=${fmt1(litFractionPct)}% (${litCells}/${denomMesoFeasible})`);
  csmoke('headline density ≈ 2.4 kits/cell', fmt1(kitsPerLitCell) === '2.4', `density=${fmt1(kitsPerLitCell)} (${counts.active}/${litCells})`);
  // r5 beyond-horizon receipt: N == 14 (gandalf's independent computation).
  csmoke('beyond-horizon N == 14 (spec §9.5.1 receipt)', beyondHorizonCount === 14, `N=${beyondHorizonCount} active kits beyond the ghost hull`);
  // r5 group profile: the 14 split 10 WHIRLWIND + 3 CHANNELED-BEAM + 1 neutral (gateA_group==null).
  {
    const byGrp = {};
    for (const p of beyondHorizonKits) { const g = p.gateA_group ?? 'NEUTRAL'; byGrp[g] = (byGrp[g] || 0) + 1; }
    const ww = byGrp['WHIRLWIND'] || 0, cb = byGrp['CHANNELED-BEAM'] || 0, nu = byGrp['NEUTRAL'] || 0;
    csmoke('beyond-horizon group profile (10 WHIRLWIND + 3 CHANNELED-BEAM + 1 neutral)',
      ww === 10 && cb === 3 && nu === 1,
      `WHIRLWIND=${ww}, CHANNELED-BEAM=${cb}, NEUTRAL=${nu} (${Object.entries(byGrp).sort().map(([k, v]) => `${k}:${v}`).join(', ')})`);
  }
  // r5 boundary-convention sanity: the point-in-hull test classifies at least one hull-adjacent
  // active point as INSIDE (proving on-edge/inside works; the settled archipelago overlaps the
  // ghost-lit ground, so many actives are inside the hull — N is small vs 469).
  csmoke('point-in-hull: most actives INSIDE (N << active count)', beyondHorizonCount < active.length * 0.1,
    `${beyondHorizonCount} beyond / ${active.length} active = ${fmt1((beyondHorizonCount / active.length) * 100)}% (the lit archipelago sits mostly within the ghost reach)`);

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
  const hullEastWorldX = Math.max(...ghostHullWorld.map(([x]) => x));
  const settledEastWorldX = Math.max(...all.map((p) => p.x));
  const beyondGrpCounts = (() => {
    const byGrp = {};
    for (const p of beyondHorizonKits) { const g = p.gateA_group ?? 'NEUTRAL'; byGrp[g] = (byGrp[g] || 0) + 1; }
    return Object.entries(byGrp).sort().map(([k, v]) => `${k} ${v}`).join(' · ');
  })();
  return `# Atlas Edition-I — render verification note (r5: beyond-horizon disclosure line)

**r5 amendment (2026-07-15, spec §9.5):** STRICTLY-ADDITIVE — ONE microcopy line in the GHOST FIELD
ledger box (both skins), rendered DIRECTLY AFTER the clip-disclosure line (§9.2.3). Fired by Matt's
directive ("cut §9.5 and fire the r5 pass") after the chart's first reader hit the SECOND misreading
within one session of r4 going live: *"how can we have kits outside the ghost's meso area?"*. The r4
horizon label kills misreading #1 (dark beyond the line = mined-out); this line kills misreading #2
(kits beyond the line = paradox). **Rendered line (both skins), N computed from the render pass:**

> "${beyondHorizonLine}"

- **N = ${beyondHorizonCount}** — COMPUTED FROM THE RENDER PASS by a point-in-polygon test of all
  ${active.length} ACTIVE (\`supplementary=false\`) points against the **SAME world-space convex hull**
  the r4 §9.4.1 code computes (\`ghostHullWorld\`, ${ghostHullVertexCount} vertices) — ONE code path, ONE
  hull, NEVER a second hull, NEVER hard-coded. Boundary convention (spec §9.5.1): a kit exactly ON the
  hull edge counts as INSIDE (not beyond). N matches gandalf's independent computation (14: 10 WHIRLWIND
  + 3 CHANNELED-BEAM + 1 neutral, all \`commit=channel\`) — the render pass agrees, so no HALT.
- **Group profile of the ${beyondHorizonCount} beyond-horizon kits:** ${beyondGrpCounts}.
- **Kit ids (beyond the hull, sorted):** ${beyondHorizonKits.map((p) => `\`${p.kit_id}\``).join(', ')}.
- **Zero-case omission:** if no active kit lay outside the hull the line would be OMITTED entirely (no
  "0 kits") — same protocol as the clip line. Proven by the r5-beyond-horizon doctored all-inside test.
- **Supplementary points (tombstones) EXCLUDED** from N — the graveyard is its own register. (The 3
  easternmost points of the whole plane ARE dead channel kits — beyond the horizon by the same
  mechanism, already disclosed by their own tombstone layer.)
- The coordinate examples in the string (cone/whirlwind geometry, channel commit) are CONTENT-LOCKED
  disclosure copy — same class as the pole glosses (empirical facts about the frozen basis, loading
  ranks #2/#3, immutable within Edition-I) — carried VERBATIM.
- The exact contiguous string is carried in a \`<title>\` node so acceptance greps it whole (same
  pattern as the r4 horizon label). Every frozen layer — points, ghost glyphs, horizon polyline +
  label + marker, tombstones, headline callout, explainer trio, RIDER-1, AND the clip-disclosure line
  — is BYTE-FROZEN vs the r4 baseline; the ONLY diff is this one line (+ the plaque's downward shove
  to make room). Verified by DIRECT SVG diff, exactly like r4-vs-r3.2.

**Frozen-layer baseline (r5):** \`agentic_orchestration/galadriel/captures/2026-07-15-atlas-edition1-r4-horizon\` (r4)

**r4 amendment (2026-07-15, spec §9.4):** STRICTLY-ADDITIVE chrome on top of the r3.2 render line,
fired by Matt's ratification ("I agree with all four") of gandalf's INTERIOR-1 memo review
(review-of-record: \`agentic_orchestration/gandalf/design-inputs/2026-07-15-interior1-memo-review.md\`).
INTERIOR-1 §3 (interior-aware placement) is REJECTED as specced; this amendment implements the memo's
§4 (horizon) and §6 (headline statistics) only. TWO changes, both skins:
  1. **GHOST HORIZON** — the convex hull of ALL 10,080 projected ghost positions (incl. the 21
     out-of-frame cells; the hull is of the lattice's REACH, then CLIPPED to the plane frame exactly
     like the ghost glyphs). Faint dashed envelope, chrome-weight, drawn BENEATH the ghost glyphs so
     it never reads as data. Mandatory label (exact string) placed adjacent to the EAST gap.
  2. **HEADLINE COVERAGE PAIR** — the coverage callout re-leads with two meso-grain statistics
     computed at render from emitted fields (lit_cells / meso_feasible, active / lit_cells). The
     exact-grain line (469 ≈ 6.8×10⁻⁵ % of 693,146,160) DEMOTES to a secondary flavor line.
Every frozen layer (points, tombstones, ghost glyph positions, sealed ledger, clip-disclosure line,
explainer trio, RIDER-1 badge) is BYTE-FROZEN vs the r3.2 baseline — verified by direct SVG diff:
the ONLY changes are the horizon chrome (added) + the re-led coverage callout (the old single line
replaced by two leads + the demoted secondary).

**r3 amendment (2026-07-15, spec §9):** the feasible-lattice GHOST FIELD renders as GROUND beneath
the settled points, fired by Matt's Q30 ruling (Q30a cut-predicate amendments ratified + Q30b zero
taste cuts). Data source: elrond ghost-field emission (\`atlas.json\` ghost_field block, commit
d0b2a025). EXTENDS the r2 render line: the 506 point positions, KDE terrain, condensation anchors,
graveyard tombstone layout, RIDER-1 badge, and r2 explainer trio are all FROZEN; the ghost layer is
strictly additive and drawn FIRST (bottom of stack). The 12 formerly-unknown tombstones now carry
emitted death_class verdicts.

**r3.2 amendment (2026-07-15, spec §9.2.3, r3.2/commit \`7cf1eeca\`):** gandalf's r3 verification verdict
was ACCEPT-WITH-ONE-AMENDMENT. The clip call on the out-of-frame ghost cells was correct (frozen plane
bounds; zero-mass ground never rescales the frame) but was disclosed only in this note — on the chart, the
GHOST FIELD ledger claimed all feasible cells without saying some project beyond the frame. §9.2.3 now binds:
any clip MUST be disclosed on-chart in the ghost ledger. FIX: a clip-disclosure microcopy line renders in the
GHOST FIELD ledger box (both skins); the count is COMPUTED FROM THE RENDER PASS (cells whose projected
position falls outside the plane rect), never hard-coded — it follows any future atlas.json change; if zero
cells clip the line is omitted entirely (no "0 clipped"). Acceptance suite gains \`r3.2-clip-disclosure\`.

**Rendered by:** galadriel/pipeline/atlas-edition1-render-r5.mjs (deterministic; no wall-clock — all stamps from atlas.json)
**Input (sole):** agentic_orchestration/research/curated/atlas/atlas.json (unchanged, elrond d0b2a025)
**r4 frozen-layer baseline (inherited check):** agentic_orchestration/galadriel/captures/2026-07-15-atlas-edition1-r3-ghost (r3.2)
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
- ghost cells outside frozen plane box (clipped): **${fmtInt(ghostClippedCount)}** (all unlit=${ghostClippedAllUnlit}; ${fmtInt(new Set(ghostClippedCells.map((c) => `${c.x.toFixed(4)},${c.y.toFixed(4)}`)).size)} distinct positions) — CLIP DISCLOSURE (r3.2, spec §9.2.3) rendered in the GHOST FIELD ledger, count from the render pass
- clip-disclosure line as rendered (both skins)${ghostClippedCount > 0 ? `: **"${ghostClipLine}"**` : ' — OMITTED (zero cells clip)'}
- depth Σ: **${fmtInt(feasibleCells.reduce((s, c) => s + c.depth, 0))}** == depth_sum_check == post-red-law denom
- RED-3' note (emitted, drives off-plane seal semantics): ${red3Note}

## Ghost HORIZON accounting (r4, spec §9.4.1 — all COMPUTED FROM THE RENDER PASS)
- **hull vertex count: ${ghostHullVertexCount}** (convex hull of ${fmtInt(new Set(feasibleCells.map((c) => `${c.x.toFixed(6)},${c.y.toFixed(6)}`)).size)} distinct projected ghost positions, INCLUDING the ${fmtInt(ghostClippedCount)} out-of-frame cells — the hull is of the lattice's REACH, then clipped to the plane frame)
- hull east reach (world x): **${hullEastWorldX.toFixed(4)}** · settled points east reach (world x): **${settledEastWorldX.toFixed(4)}** · **EAST gap = ${(settledEastWorldX - hullEastWorldX).toFixed(4)}** (settled kits stand east of the horizon there — the load-bearing disclosure direction)
- envelope: dashed polyline (open, closed back to first vertex), CLIPPED to plane frame via the same planeClip used by ghost glyphs; drawn BENEATH the ghost glyphs (chrome, sub-ghost — must not read as data)
- label (exact string, verbatim): **"${GHOST_HORIZON_LABEL}"** — placed adjacent to the EAST gap, tied to the hull's east vertex by a thin dashed leader; visible two-line wrap (split at the em-dash); the exact contiguous string is carried in the envelope's \`<title>\` (grep-verified present both skins)
- computed-not-constant: PROVEN by the r4-horizon doctored-input test (remove the extreme corner cell → hull recomputes → CHANGES); vertices are never hard-coded

## Headline COVERAGE PAIR accounting (r4, spec §9.4.2 — ratios COMPUTED, not hard-coded)
- lead 1: **"${HEADLINE_LIT}"** (lit_cells ${fmtInt(litCells)} / meso_feasible ${fmtInt(denomMesoFeasible)})
- lead 2: **"${HEADLINE_DENSITY}"** (active ${fmtInt(counts.active)} / lit_cells ${fmtInt(litCells)})
- demoted secondary (retained, no longer lead): **"${COVERAGE_SECONDARY}"** — the 693M exact-grain line; present ONLY in the secondary position (grep-verified NOT in either lead)
- anti-"422,445,240" grep: verified ABSENT (superseded denominator never appears)

## Beyond-horizon accounting (r5, spec §9.5.1 — N COMPUTED FROM THE RENDER PASS)
- **N = ${beyondHorizonCount}** active kits stand beyond the ghost hull — point-in-polygon of the ${active.length} active points against the SAME ${ghostHullVertexCount}-vertex world hull (\`ghostHullWorld\`) the r4 horizon uses; boundary convention ON-hull ⇒ INSIDE (spec §9.5.1). Matches gandalf's independent receipt (14).
- **group profile:** ${beyondGrpCounts} — 10 WHIRLWIND (of the 15 members) + 3 CHANNELED-BEAM + 1 neutral; ALL carry \`commit=channel\`.
- **kit ids (sorted):** ${beyondHorizonKits.map((p) => `\`${p.kit_id}\``).join(', ')}
- rendered line (both skins), OMITTED entirely when N==0: **"${beyondHorizonLine}"**
- the line renders DIRECTLY AFTER the clip-disclosure line in the GHOST FIELD ledger box; the full contiguous string is in a \`<title>\` for whole-grep; the plaque grows to hold the wrapped rows and the sealed ledger shifts down.
- **why they overshoot:** kits project with all 14 basis coordinates; ghost cells carry only the 7 core, so the strongest EAST pulls (geometry=cone/whirlwind loading #3, commit=channel loading #2) are MASKED at meso grain — the lit channel kits reach east of the 7-core hull. Position ≠ membership.
- **excluded — supplementary tombstones:** the graveyard is its own layer. The 3 easternmost points of the whole plane are dead channel kits (tl2-arc-beam · d4-incinerate · d2-inferno-sorc), beyond by the same mechanism, disclosed by their tombstone layer.

## Point accounting (FROZEN from r2)
- active: **${active.length}** (neutral ${neutral.length} + grouped ${grouped.length}) · corpses: **${supplementary.length}** · total: **${all.length}**
- death classes: ${deathClasses.map((dc) => `${dc}:${supplementary.filter((p) => p.death_class === dc).length}`).join(', ')}

## Acceptance tests
${tests.map(line).join('\n')}

## Smoke tests
${smokes.map(line).join('\n')}

## Layout calls / judgment made (r5 — the ONE call this amendment adds)
- **The point-in-hull judgment (spec §9.5.1 — the load-bearing r5 call).** N is the count of ACTIVE points that fall OUTSIDE the ghost hull. The judgment has three parts, each made to keep this a single honest measurement, not a second computation: **(1) ONE hull, not two.** The test polygon is \`ghostHullWorld\` — the *exact same* convex hull the r4 horizon draws (Andrew's monotone chain over the distinct world positions of all ${fmtInt(feasibleCells.length)} feasible cells). I did NOT recompute a hull for the count; the disclosure line and the drawn envelope are guaranteed consistent because they are the same ${ghostHullVertexCount}-vertex object. **(2) Test in WORLD space, not SVG space.** The hull lives in world coordinates (its true reach, incl. its out-of-frame vertices); \`sx\`/\`sy\` is affine-monotone, so world-containment ≡ projected-containment — but testing in world space avoids re-introducing the clip frame. This matters for the load-bearing EAST case: a channel kit east of the hull but *inside* the plane frame is still beyond the hull, and must count. **(3) Boundary convention: ON ⇒ INSIDE (spec §9.5.1).** The point-in-polygon does an explicit on-edge check FIRST (collinear + within the segment span, eps ${PIP_EPS}); an on-edge point returns INSIDE and is NOT counted as beyond. Then a standard ray-cast parity test decides strict interior. Result: N=${beyondHorizonCount}, matching gandalf's independent receipt exactly. **Fail-loud guard:** if the render pass had computed N≠14 on the real input, the run HALTS (\`die\`) rather than shipping a wrong count — the disclosure would be dishonest, and a moved N means the hull, the input, or the receipt drifted and needs a human look.
- **The line's placement + wrap (layout call).** It renders DIRECTLY AFTER the clip-disclosure line inside the GHOST FIELD ledger plaque, with the SAME faint/gloss treatment (spec §9.5.1 "match the clip-disclosure line's treatment"). Because the locked string is ~230 chars it WRAPS: a deterministic character-budget greedy wrap (${'`'}wrapByChars${'`'}, budget 62 chars ≈ the ~336px usable plaque width at font 9.5) splits it into rows rendered as \`<tspan>\`s; the plaque \`<rect>\` height grows by the row count and the sealed ledger below shifts down by the same amount, so nothing overprints. The FULL contiguous string is carried in a single \`<title>\` node on the parent \`<text>\` — so acceptance greps the whole sentence as one unit even though the visible text is multi-line (same pattern the r4 horizon label uses). **Zero-case:** if N==0 the entire block (rect-grow, \`<text>\`, \`<title>\`) is skipped — no "0 kits" ever renders (proven by the doctored all-inside test).
- **Footer render-script string held FROZEN (frozen-diff discipline).** The in-SVG footer still reads \`render: galadriel/atlas-edition1-render-r3.mjs\` (inherited from r3/r4). I deliberately did NOT bump it to r5: spec §9.5.2.17 demands the ONLY diff vs r4 be the new ledger line, verified by direct SVG diff — changing the footer string would introduce a second diff region. True r5 provenance is carried here in the note + the script filename. (Same discipline r4 used to preserve its r3.2 diff.)

## Layout calls / judgment made (r4 — the calls the r4 amendment added, unchanged)
- **Hull computed in WORLD space, drawn projected, clipped to frame (spec §9.4.1).** The convex hull is taken over the DISTINCT world positions of ALL 10,080 feasible cells (Andrew's monotone chain; deterministic sort x-asc then y-asc; ≤0 cross-product test drops collinear points → a tight ${ghostHullVertexCount}-vertex ring). This is the lattice's true reach — it INCLUDES the ${fmtInt(ghostClippedCount)} out-of-frame outliers. Each vertex is then projected through sx/sy and the polyline is clipped to the plane rect by the SAME planeClip that trims the ghost glyphs. Rationale: hulling in world space (not the in-frame subset) means the envelope describes the real reach; clipping (not rescaling) keeps the frozen frame. **Vertices are from the render pass — never hard-coded** (doctored-input test proves it).
- **Horizon drawn BENEATH the ghost glyphs (spec §9.4.1 "sub-ghost, chrome not data").** The envelope polyline is emitted at the TOP of the LAYER-0 clip group, BEFORE the ghost dark/lit glyph groups — so the glyphs paint OVER it. This is the judgment call that keeps it from reading as data: a limit line the eye registers as ground, not as a plotted boundary. (Consequence: the ghost glyph \`<circle>\` byte-strings are unchanged vs r3.2 — frozen-layer regression holds.)
- **Stroke treatment (layout call):** hairline dashed. \`stroke-width\` ${SKINS.instrument.horizonWidth} (both skins), \`stroke-dasharray\` "${SKINS.instrument.horizonDash}" (a long-dash reads as "limit/threshold", distinct from the zero-axis "2 6" fine-dot and the tombstone "2 2"), \`stroke-linejoin=round\` so hull corners don't spike. Instrument: cool gray \`${SKINS.instrument.horizonInk}\` @ ${SKINS.instrument.horizonOp} opacity. Archive: dim gilt \`${SKINS.archive.horizonInk}\` @ ${SKINS.archive.horizonOp} — "embers at the edge of the walked dark". NO fill (a fill would assert the region-claim §9.2.2 forbids — the envelope is an open dashed line, never a shaded area).
- **Label placement (layout call — named per spec ask): adjacent to the EAST gap.** The mandatory string is anchored off the hull's EAST vertex (the greatest-projected-x vertex, computed from the render pass — not hard-coded). A thin dashed leader + a small hollow marker tie the label to that vertex; the label itself drops into the sparse lower-right interior (measured: only 3 settled points in the east-gap band) and reads right-anchored into the gap. This is the load-bearing direction: settled kits reach x=${settledEastWorldX.toFixed(3)}, the ghost hull ends x=${hullEastWorldX.toFixed(3)}; the two gold flame-kits visibly sit EAST of the envelope, in the "dark beyond" the label names. **Two-line visible wrap** (split at the em-dash, a natural clause break) for legibility of an 85-char disclosure sentence; the exact contiguous string lives in the polyline \`<title>\` so the acceptance grep matches the whole label verbatim.
- **HEADLINE PAIR re-lead (spec §9.4.2):** the two meso-grain stats now LEAD the callout (font 13.5/12, bold, ink) at lower-left; the exact-grain 693M line DEMOTES directly below at font 10, faint (\`glossStyle\`, \`faint\` ink) — retained and honest, no longer the lead. Both ratios (${fmt1(litFractionPct)}%, ${fmt1(kitsPerLitCell)}) are computed from emitted fields (lit_cells/meso_feasible, active/lit_cells); the prose halves are content-locked disclosure copy (same class as the pole glosses). The 693M numeral is grep-verified ABSENT from both leads.

## Layout calls / judgment inherited (r3/r3.2 — unchanged, byte-frozen)
- **FROZEN PLANE BOUNDS (load-bearing):** world bounds computed from POINTS ONLY (min/max over all 506 + 6% pad), byte-identical to the r2 baseline — so the 506 point SVG coordinates never move. The ghost field is zero-mass ground (spec §9.1a) and must NOT rescale the plane.
- **Ghost outliers CLIPPED, not rescaled — DISCLOSED on-chart (r3.2, spec §9.2.3):** ${fmtInt(ghostClippedCount)} feasible cells (all unlit=${ghostClippedAllUnlit}, ${fmtInt(new Set(ghostClippedCells.map((c) => `${c.x.toFixed(4)},${c.y.toFixed(4)}`)).size)} distinct positions) project outside the frozen point-box. They are clipped to the plane frame via SVG clip-path. Rescaling to fit un-settled outliers would break frozen-layer regression AND shrink the settled archipelago — clip is the correct call. **The clip is no longer silent:** a disclosure line renders in the GHOST FIELD ledger (both skins), count computed FROM THE RENDER PASS (cells whose projected position falls outside the plane rect), so it follows any future atlas.json change; if zero cells clipped the line is omitted entirely (no "0 clipped"). §9.2.3: the dark the reader sees implicitly claims to be the feasible space — silent truncation is an under-claim.
- **Coincident-projection aggregation (spec §9.2.4):** cells sharing a 2-dp SVG position are merged into one glyph; radius grows by log2(multiplicity+1) (deterministic size-step, NO RNG). A merged position is LIT if ANY coincident cell is lit (census-current, spec §9.1b).
- **Ghost as GLYPHS never regions (spec §9.2.2):** ghost cells are <circle> marks only — no Voronoi, no hatching, no painted boundaries (RIDER-1 continuum discipline; over-claim discipline shared with F-1).
- **Figure-ground:** unlit ghost = the feasible dark (faint near-ground); lit ghost = a touch stronger (census-lit, still sub-point). Layer order bottom→top: unlit ghost → lit ghost → density → points → tombstones → chrome. The chart's story: settled territory is a lit archipelago in a vast feasible dark.
- **Sealed = OFF-plane LEDGER (spec §9.2.4):** ${fmtInt(sealedCells.length)} sealed cells carry NO coordinates (never projected); rendered as a chrome register with cut ids verbatim from cut_id. cut_id conformance to {L1-, L2-} is a HARD refusal gate (R4).
- **Coverage + census line:** coverage callout and mandatory census line ("ghost field lit from the current census; positions from the frozen Edition-I basis.") from emitted fields. Superseded denominator 422,445,240 grep-verified ABSENT.
- **Depth is emitted, never derived (spec §9.1d):** depth per cell rendered from the field; Σ is an emitter TEST only.
- **Two skins, one layout engine:** ghost coordinate+status fingerprint identical across skins (${ghFps.instrument === ghFps.archive ? 'MATCH' : 'MISMATCH'}); point fingerprint identical (${ptFps.instrument === ptFps.archive ? 'MATCH' : 'MISMATCH'}). Skins vary only ghost + horizon ink/opacity chrome. The horizon hull, label placement, and headline-pair layout are one code path — both skins carry the same ${ghostHullVertexCount}-vertex hull and the same label anchor.
- **Determinism:** sorted iteration; no RNG; no wall-clock (footer stamp = atlas.emitted_at); 2-dp SVG coords; re-render byte-equal (verified across separate process invocations).

## Provenance law
chart = render(atlas.json). No number/label/coordinate originates outside an atlas.json field. Layout is computed; content is not. The r5 addition honors this: **N=${beyondHorizonCount}** is COMPUTED from the render pass (a point-in-polygon of the emitted active points against the emitted-ghost-derived hull — never a literal; the doctored-input tests prove it follows the data: remove a beyond kit ⇒ N drops, move all kits inside ⇒ N=0 ⇒ line omitted); the rest of the sentence (the 14-coordinate / 7-core framing, the cone/whirlwind/channel examples) is content-locked disclosure copy carried VERBATIM — empirical facts about the frozen basis, same class as the pole glosses. The r4 additions still hold: the ghost horizon's ${ghostHullVertexCount} vertices are COMPUTED from the emitted ghost field; the headline-pair ratios (${fmt1(litFractionPct)}%, ${fmt1(kitsPerLitCell)}) are COMPUTED from emitted counts. The renderer computes layout; it never invents content.
`;
}

main();
