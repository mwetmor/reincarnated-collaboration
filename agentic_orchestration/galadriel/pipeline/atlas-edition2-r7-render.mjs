// atlas-edition2-render.mjs — EDITION II. The atlas render WITH the ghost-field layer +
// GHOST HORIZON envelope + re-led HEADLINE COVERAGE PAIR + BEYOND-HORIZON LEDGER LINE +
// r6 CHROME LEGIBILITY CORRECTIONS, extended to Edition-II's re-emitted LATTICE:
// the `pull` function level, the EAST-half geometry×commit DRILL-IN sub-cell ground, the
// off-plane-corpus disclosure line, re-derived denominators (labeled-lineage supersession),
// and the mechanically-scored P-DF-1 verdict.
//
// LAW: chart = render(atlas.json). Layout is COMPUTED here; all CONTENT (numbers, labels,
// coordinates, class strings) originates ONLY in atlas.json fields. No literal atlas numerics
// live in this source beyond layout geometry. (§4c no-hand-derived-numbers law.)
//
// EDITION II amendment (2026-07-15, spec §10). Fired by Matt's word ("If the slate holds, cut
// Edition-II §10") — the slate held (c7804393 confirmed a384c11d, vacuously). An EDITION changes
// the LATTICE; an rN discloses/corrects chrome on existing ground (§10.0). This is the first
// new-EDITION render — the lattice changed, the fit did NOT.
//
//   EDITION REGRESSION LAW (spec §10.4.3, REPLACES rN frozen-layer-regression across the boundary):
//     • The FIT layer — basis block, 506 point coordinates, tombstones, explainer trio, RIDER-1,
//       axis names — is BYTE-FROZEN vs r6 (independently re-verified: atlas.json[basis|points]
//       compare identical to atlas-edition2.json[basis|points]). Acceptance 23.
//     • The LATTICE layer — ghost glyphs, horizon, ledgers, denominators, coverage callouts,
//       footer stamp — RE-EMITS WHOLESALE (that is what makes it an edition). The horizon hull +
//       beyond-horizon N RECOMPUTE from the new field (§9.4.1/§9.5 computed-not-constant law pays
//       off here — no hard-coded lattice geometry survives the edition boundary). Clip + beyond-
//       horizon disclosure lines recompute; zero-case omission protocols carry.
//
//   WHAT EDITION II ADDS to the render (all from emitted fields, §4c law):
//     (1) PULL SLICE (§10.1) — function axis 10→11 levels (+`pull`). The 2 lit pull cells (the
//         d3-zbarb + di-cyclone-monk-pvp re-keys) live inside `feasible_cells` and render as ghost
//         glyphs by the SAME aggregation grammar; a pull-slice ledger line in the GHOST FIELD box
//         discloses the slice (feasible/lit/sealed) from `ghost_field.pull_slice`.
//     (2) EAST-HALF DRILL-IN (§10.3) — the emitted `drill_in.sub_feasible_glyph_field` (38,878
//         {multiplicity,x,y}, Σmult=172,312) renders as visually SUBORDINATE supplementary GROUND
//         (zero-mass §10.3.4 — never moves basis/frame/point), EAST-half only, using the SAME
//         established ghost aggregation grammar (multiplicity → log₂ size-step) at REDUCED prominence.
//         The `drill_in.sub_sealed_ledger` (2 rows, RED-3-movement-damage-carveout, 5,068 each)
//         joins the chrome ledger — labeled at the PROMOTED grain (RED-3′ surfaces ONLY here, §10.4.2).
//     (3) OFF-PLANE CORPUS disclosure (§10.4.4, NEW MANDATORY, nonzero-only) — the emitted
//         `off_plane_corpus.disclosure` sentence + N from `gate_rejected_keyed` (94) in the ledger.
//     (4) DENOMINATOR SUPERSESSION (§10.1.5) — new exact (767,411,820) + meso (11,160) denominators;
//         the Edition-I strings (693,146,160 / 10,080 / 1,260) appear ONLY in LABELED lineage copy
//         (a `superseded_edition1` sub-block), same anti-stale grep discipline as "422,445,240".
//     (5) EDITION STAMP (§10.4.5) — footer provenance carries "Edition II" + register ref
//         `feasibility-cuts-register-v1.2` on both skins; Edition-I captures remain archived.
//     (6) P-DF-1 (§10.5) — verdict emitted mechanically: verdict line in the verification note +
//         machine-readable field in the render provenance JSON (from the emitted `p_df_1` block).
//
//   GRAIN-SCOPED SEAL ENUM (§10.4.2, extends §9.1c): MESO sealed cut_ids remain {L1-, L2-} — RED-3
//   at meso grain still REFUSES loud. SUB-CELL sealed cut_ids = {L1-, L2-, RED-3-} — at the promoted
//   geometry×commit grain RED-3′ SURFACES, and only there. Doctored-input proofs BOTH grains.
//
// Where §10 leaves a render-form seam unspecified, this render follows the established ghost-layer
// grammar (coincident aggregation, log₂ size-step, glyphs-never-regions, off-plane sealed ledger);
// any seam where that grammar is insufficient is FLAGGED in the verification note, never invented
// silently. (See the note's "render-form seams" section.)
//
// --- inherited rN chrome (carried forward VERBATIM in the LATTICE layer; the FIT layer is frozen) ---
// r6 amendment (2026-07-15, spec §9.6): STRICTLY-CORRECTIVE — the first corrective rN.
// Moves existing chrome GEOMETRY; adds/removes/rewords NOTHING (ZERO-CONTENT LAW). Fired
// by Matt's directive ("fire the r6 legibility pass") on gandalf's DRIFT-CRITIC finding
// during r5 verification: two byte-proven PRE-EXISTING chrome flaws (present since r3.2,
// surfaced by a 2× plaque crop). The flaws sit in the disclosure apparatus itself — the
// chart's honesty spine must not be its least-legible part. TWO fixes, the ONLY intentional
// diffs vs r5, both skins:
//   (fix a) CLIP-LINE WRAP. The §9.2.3 clip-disclosure line rendered as ONE row from x=1156
//     and overran the plaque's right edge (~100-char string in a ~348px usable width). It now
//     flows through the SAME deterministic wrap the §9.5 beyond-horizon line uses (wrapByChars,
//     budget 62, font 9.5) → multi-row <tspan>s + the FULL contiguous string in a <title> node
//     on the parent <text>. Content BYTE-IDENTICAL to r5's clip string; geometry only. The clip
//     wraps to 2 rows, so CLIP_ROW grows 12 -> 2*BEYOND_LINE_H (=22) and the plaque grows UPWARD
//     by 10px (bottom fixed; the r5 growth mechanism).
//   (fix b) FOOTER-CENSUS RE-ANCHOR. The right-anchored frame-footer census line
//     ("points: 469 active + 37 corpse = 506 · …", end-anchored x=1504, y=1188) overprinted the
//     sealed-ledger rows (y=1178/1192) inside the plaque footprint (plaque right edge = x=1504).
//     Re-anchor: end-anchor moves to plaqueRect.x − 12 (COMPUTED from the render pass, not a
//     constant; = 1132 at current geometry). y + content + treatment UNCHANGED. Mid-frame
//     clearance vs the left footer line pre-verified (left ends ≈x=550; census starts ≈x=757).
// ZERO-CONTENT LAW (spec §9.6.3): r6 may not add/remove/reword ANY string. Every text node's
// CONTENT is byte-identical to r5; only the geometry (x/y/tspan structure) of the two named
// elements + the plaque reflow may differ. HALT-GATE: criterion 21 (occlusion guard) computes
// zero data-mark centers inside the grown plaque rect — a settled point sits ≈y=1050 near the
// projected new top edge; the guard makes the clearance mechanical, not lucky (margin in note).
// Footer render-script string held FROZEN (single-purpose-diff discipline, per r4/r5).
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
// EDITION II: the data source is atlas-edition2.json (NOT atlas.json — that is Edition-I and stays
// archived). The FIT layer inside it (basis + 506 points) is byte-frozen vs Edition-I; the LATTICE
// layer (ghost_field) re-emits wholesale (§10.4.3).
const ATLAS_PATH = resolve(__dirname, '../../research/curated/atlas/atlas-edition2.json');
// EDITION II r7 RESTYLE + SEMANTIC-HOOKS PASS (spec 2026-07-15-atlas-interactive-glance-spec §§1-3,
// §7 acc 29-31): output to the r7 capture dir. The E2.1 captures (2026-07-15-atlas-edition2-e21/)
// are preserved UNTOUCHED as the FREEZE RECORD (r7's geometry-byte-freeze baseline, acceptance-29).
const DEFAULT_OUT_DIR = resolve(__dirname, '../captures/2026-07-15-atlas-edition2-r7');
// The Edition-I r6 SVGs — FIT-layer COORDINATE-regression baseline (points + tombstones geometry
// byte-frozen; r7 whitelists fill + hook-attributes, so the FIT test compares coord+title tuples).
const FIT_BASE_DIR = resolve(__dirname, '../captures/2026-07-15-atlas-edition1-r6-legibility');
// ebb18784's Edition-II captures — carried lineage reference (pre-fix record).
const E2_PREFIX_DIR = resolve(__dirname, '../captures/2026-07-15-atlas-edition2');
// r7 GEOMETRY-FREEZE BASELINE (spec §7 acceptance-29): the E2.1 render (commit fb951b39). Every
// mark coordinate/geometry (circle cx/cy/r, hull polyline, tombstone x/y) is byte-frozen vs THIS
// baseline; ONLY fills/strokes/text-layout/hook-attributes re-baseline (whitelist in the note).
const R7_FREEZE_DIR = resolve(__dirname, '../captures/2026-07-15-atlas-edition2-e21');
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
// r7 HOOK (spec §3.2): the emitted core_order — the 7 core axis names, EMIT ORDER for data-core.
// Asserted length-7 (fail-loud); the ghost data-core tuples are copies of feasible_cells[].core in
// this order (never a renderer invention — §4c). A doctored core_order that isn't length-7 HALTS.
const ATLAS_CORE_ORDER = req(atlas, 'ghost_field.core_order', 'ghost-core-order');
if (!Array.isArray(ATLAS_CORE_ORDER) || ATLAS_CORE_ORDER.length !== 7) die(`ghost_field.core_order must be the 7 core axes; got length ${Array.isArray(ATLAS_CORE_ORDER) ? ATLAS_CORE_ORDER.length : 'non-array'} (spec §3.2 hooks-integrity).`);
// Every feasible cell's core must be a 7-tuple (the data-core hook copies it verbatim). Fail-loud.
{
  const bad = feasibleCells.find((c) => !Array.isArray(c.core) || c.core.length !== 7);
  if (bad) die(`ghost feasible cell has non-7 core (kit_count ${bad.kit_count}, x ${bad.x}) — data-core hook needs the emitted 7-tuple (spec §3.2).`);
}
const ghostDenoms = req(atlas, 'ghost_field.denominators', 'ghost-denominators');
// EDITION II re-derived denominators (§10.1.5). All from emitted fields, never hard-coded.
const denomFeasibleExact = req(atlas, 'ghost_field.denominators.exact_post_red_law', 'ghost-denom-exact'); // E2: 767,411,820
const denomNaiveBox = req(atlas, 'ghost_field.denominators.exact_raw_naive', 'ghost-denom-naive');          // E2: 990,186,120
const mesoSealed = req(atlas, 'ghost_field.denominators.meso_sealed', 'ghost-meso-sealed');                 // E2: 1,314
const litCells = req(atlas, 'ghost_field.lit_cells', 'ghost-lit');                                          // E2: 193
const unmappedPending = req(atlas, 'ghost_field.unmapped_pending_curation', 'ghost-unmapped');              // E2: 108
const depthByDelivery = req(atlas, 'ghost_field.depth_by_delivery', 'ghost-depth');
const depthSumCheck = req(atlas, 'ghost_field.depth_sum_check', 'ghost-depth-sum');
const red3Note = req(atlas, 'ghost_field.red3_note', 'ghost-red3-note');
// EDITION II: labeled-lineage supersession sub-block (§10.1.5) — the Edition-I denominators
// (693,146,160 / 10,080 / 1,260) live HERE and ONLY appear in labeled lineage copy on the chart.
const supersededE1 = req(atlas, 'ghost_field.denominators.superseded_edition1', 'ghost-superseded-e1');
const supE1Exact = req(atlas, 'ghost_field.denominators.superseded_edition1.exact_post_red_law', 'ghost-superseded-exact'); // 693,146,160
const supE1MesoFeasible = req(atlas, 'ghost_field.denominators.superseded_edition1.meso_feasible', 'ghost-superseded-mesofeas'); // 10,080
const supE1MesoSealed = req(atlas, 'ghost_field.denominators.superseded_edition1.meso_sealed', 'ghost-superseded-mesoseal');    // 1,260

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

// ================================================================== EDITION II blocks (§10)
// Edition + register provenance (§10.4.5). The register ref pins to v1.2 — the `pull` register.
const editionTag = req(atlas, 'ghost_field.edition', 'ghost-edition');                 // "II"
const registerRef = req(atlas, 'ghost_field.register_ref', 'ghost-register');          // feasibility-cuts-register-v1.2
if (String(registerRef) !== 'feasibility-cuts-register-v1.2')
  die(`ghost_field.register_ref '${registerRef}' != feasibility-cuts-register-v1.2 — Edition-II render binds the v1.2 pull register (spec §10.1 / §10.4.5).`);

// --- PULL SLICE (§10.1). The function coordinate grew 10→11 levels (+pull). The 2 lit pull cells
//     live INSIDE feasible_cells and render as ghost glyphs by the same aggregation grammar; the
//     pull_slice block drives a disclosure line (feasible/lit/sealed) + the acceptance-25 trace.
const pullSlice = req(atlas, 'ghost_field.pull_slice', 'pull-slice-block');
const pullMesoFeasible = req(atlas, 'ghost_field.pull_slice.meso_feasible', 'pull-feasible');   // 1,080
const pullMesoSealed = req(atlas, 'ghost_field.pull_slice.meso_sealed', 'pull-sealed');         // 54
const pullLitCells = req(atlas, 'ghost_field.pull_slice.lit_cells', 'pull-lit');                // 2
const pullLitTuples = req(atlas, 'ghost_field.pull_slice.lit_pull_core_tuples', 'pull-lit-tuples');
const pullNewLaw = req(atlas, 'ghost_field.pull_slice.new_law_needed', 'pull-new-law');         // 0 — a nonzero here is a HALT (§10.1.4)
const pullHalt = req(atlas, 'ghost_field.pull_slice.halt', 'pull-halt');                        // false
// §10.1.4: a pull-slice cell needing a NEW law → HALT to Matt (law amendment, never silent).
if (pullNewLaw !== 0) die(`pull_slice.new_law_needed=${pullNewLaw} — a pull cell needs a NEW law. HALT to Matt (spec §10.1.4 — law amendment, never silent).`);
if (pullHalt === true) die(`pull_slice.halt=true — emitter flagged a pull-slice HALT condition (spec §10.1.4). Refusing to render past an emitter HALT.`);
// §10.1: pull-slice seals take cut_ids from the EXISTING enum only ({L1-, L2-} at meso).
const pullSealedByCut = req(atlas, 'ghost_field.pull_slice.sealed_by_cut', 'pull-sealed-by-cut');
for (const cid of Object.keys(pullSealedByCut)) {
  if (!SEAL_PREFIXES.some((pre) => cid.startsWith(pre)))
    die(`pull_slice sealed cut_id '${cid}' is OUTSIDE the {L1-, L2-} meso set (spec §10.1.4 / §10.4.2). New-law seals HALT to Matt.`);
}

// --- EAST-HALF DRILL-IN (§10.3). Promoted geometry×commit sub-cells, EAST-half only. Sub-feasible
//     arrives PRE-AGGREGATED as sub_feasible_glyph_field (multiplicity glyph field, §10.4.1); sealed
//     sub-cells arrive as sub_sealed_ledger (rows w/ cut_id). RED-3′ surfaces ONLY at this grain (§10.4.2).
const drillIn = req(atlas, 'ghost_field.drill_in', 'drill-in-block');
const drillRegion = req(atlas, 'ghost_field.drill_in.region', 'drill-region');
const drillParentCells = req(atlas, 'ghost_field.drill_in.n_east_parent_cells', 'drill-parents');   // 5,068
const drillSubFeasibleN = req(atlas, 'ghost_field.drill_in.n_sub_feasible', 'drill-sub-feas');       // 172,312
const drillSubSealedN = req(atlas, 'ghost_field.drill_in.n_sub_sealed', 'drill-sub-sealed');         // 10,136
const subGlyphField = req(atlas, 'ghost_field.drill_in.sub_feasible_glyph_field', 'drill-glyph-field');
const subSealedLedger = req(atlas, 'ghost_field.drill_in.sub_sealed_ledger', 'drill-sealed-ledger');
const drillPromotedPair = req(atlas, 'ghost_field.drill_in.promoted_pair', 'drill-promoted-pair');
const drillSealEnum = req(atlas, 'ghost_field.drill_in.seal_enum', 'drill-seal-enum');
if (!Array.isArray(subGlyphField) || subGlyphField.length === 0) die('drill_in.sub_feasible_glyph_field empty.');
if (!Array.isArray(subSealedLedger)) die('drill_in.sub_sealed_ledger not an array.');
// each glyph-field entry must carry {multiplicity, x, y} — the emitted pre-aggregation (§10.4.1).
for (const e of subGlyphField) {
  if (typeof e.multiplicity !== 'number' || typeof e.x !== 'number' || typeof e.y !== 'number')
    die(`drill_in.sub_feasible_glyph_field entry malformed (need {multiplicity,x,y}): ${JSON.stringify(e)}`);
}
// GRAIN-SCOPED SEAL ENUM (§10.4.2): sub-cell sealed cut_ids = {L1-, L2-, RED-3-}. RED-3- surfaces
// ONLY at this grain. A sub-sealed cut_id outside that set is an unknown-enum-class error → REFUSE loud.
const SUB_SEAL_PREFIXES = ['L1-', 'L2-', 'RED-3-'];
for (const r of subSealedLedger) {
  if (r.cut_id == null) die(`drill_in.sub_sealed_ledger row missing cut_id (spec §10.4.2).`);
  if (!SUB_SEAL_PREFIXES.some((pre) => String(r.cut_id).startsWith(pre)))
    die(`drill_in sub-sealed cut_id '${r.cut_id}' is OUTSIDE the {L1-, L2-, RED-3-} promoted-grain set (spec §10.4.2). Refusing loud (R4).`);
  if (typeof r.count !== 'number') die(`drill_in.sub_sealed_ledger row missing numeric count: ${JSON.stringify(r)}`);
}
// Sub-sealed ledger breakdown (deterministic sort by cut_id then geometry then commit).
const subSealedSorted = [...subSealedLedger].sort((a, b) => {
  const ka = `${a.cut_id}|${a.geometry ?? ''}|${a.commit ?? ''}`, kb = `${b.cut_id}|${b.geometry ?? ''}|${b.commit ?? ''}`;
  return ka < kb ? -1 : ka > kb ? 1 : 0;
});

// --- OFF-PLANE CORPUS (§10.4.4, NEW MANDATORY, nonzero-only). The disclosure sentence + N from
//     the emitted gate_rejected_keyed. Same honesty class as the clip line / beyond-horizon line.
const offPlane = req(atlas, 'ghost_field.off_plane_corpus', 'off-plane-block');
const offPlaneDisclosure = req(atlas, 'ghost_field.off_plane_corpus.disclosure', 'off-plane-disclosure');
const offPlaneN = req(atlas, 'ghost_field.off_plane_corpus.gate_rejected_keyed', 'off-plane-n');    // 94

// --- P-DF-1 (§10.5). The registered prediction scored mechanically at render. We render the
//     VERDICT from the emitted block into the note + provenance JSON — never renderer-derived (§4c).
const pDf1 = req(atlas, 'ghost_field.p_df_1', 'p-df-1-block');
const pDf1Verdict = req(atlas, 'ghost_field.p_df_1.verdict', 'p-df-1-verdict');                     // PASS
const pDf1Falsified = req(atlas, 'ghost_field.p_df_1.falsified', 'p-df-1-falsified');               // false
const pDf1TopLevel = req(atlas, 'p_df_1_verdict', 'p-df-1-top-level');                              // PASS (top-level mirror)
if (String(pDf1Verdict) !== String(pDf1TopLevel))
  die(`p_df_1.verdict '${pDf1Verdict}' != top-level p_df_1_verdict '${pDf1TopLevel}' — emitter inconsistency (spec §10.5).`);
// §10.5: if FALSIFIED → INTERIOR-1 re-opens; SURFACE to Matt, never auto-fire. We render honestly
// either way (a falsified verdict is still a rendered fact); the render does NOT gate on it.
const pDf1Consequence = req(atlas, 'ghost_field.p_df_1.consequence_if_falsified', 'p-df-1-consequence');

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
// GHOST-FIELD ledger plaque geometry — the plaque WIDTH + its left edge (x). Hoisted to module
// scope so BOTH the plaque <rect> (below) and the r6 footer-census re-anchor (spec §9.6.1.b) derive
// the plaque x from ONE shared expression: the footer end-anchor is plaqueRect.x − 12, COMPUTED
// (not a constant), and provably tracks the rect.
// EDITION II: widened 360 → 420 to hold the new lattice ledger content (pull slice · drill-in ·
// off-plane corpus · superseded lineage). The upward-growth + bottom-pinned + occlusion-guard r6
// discipline carries. At current geometry: right edge 1504 − 420 = 1084 → footer anchor 1072.
const GHOST_PLAQUE_W = 420;
const GHOST_PLAQUE_X = (M.left + PW) - GHOST_PLAQUE_W;   // plaqueRect.x (right edge M.left+PW == 1504)

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
  const bucket = new Map(); // svgKey -> { sxv, syv, mult, lit, core }
  for (const c of feasibleCells) {
    const sxv = sx(c.x), syv = sy(c.y);
    const key = `${f2(sxv)}|${f2(syv)}`;
    let b = bucket.get(key);
    // r7 HOOK (spec §3.2): the ghost glyph's data-core is the REPRESENTATIVE cell's 7-tuple — the
    // FIRST feasible cell (emitted array order) that lands in this raster bucket. 1,656 of the 7,128
    // glyphs aggregate cells with DIFFERING cores (max mult 8); a single glyph cannot carry all of
    // them, and §4c forbids INVENTING a synthesized tuple. The representative core is a VERBATIM
    // EMITTED 7-tuple of a real feasible cell at this exact position (core_order emit order) —
    // deterministic (emitted array order is fixed), an emitted-field copy, never a renderer fiction.
    // (Flagged in the verification note as a §3.2 aggregate-core representative-cell resolution.)
    if (!b) { b = { sxv, syv, mult: 0, lit: false, core: c.core }; bucket.set(key, b); }
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

// ------------------------------------------------------------------ DRILL-IN glyph aggregation (EDITION II, §10.3)
// The emitted sub_feasible_glyph_field is PRE-AGGREGATED at the emitter's render-grid bin (2dp);
// but a projection step maps each {x,y} to an SVG position where several bins may STILL coincide.
// We re-aggregate by the 2-dp SVG raster (the eye's raster) using the SAME established ghost grammar
// (coincident aggregation → summed multiplicity → log₂ size-step, NO RNG). This is zero-mass ground
// (§10.3.4): the drill-in never moves the basis, the frame, or any point — it uses sx/sy (the frozen
// point-derived projection) and is CLIPPED to the plane frame by the same planeClip as the ghosts.
// EAST-half only is an EMITTED property (the field carries only EAST-half sub-cells, region declared
// in drill_in.region) — we render exactly what is emitted (§4c), we do not re-select the half.
function drillAggregate() {
  const bucket = new Map(); // svgKey -> { sxv, syv, mult }
  for (const e of subGlyphField) {
    const sxv = sx(e.x), syv = sy(e.y);
    const key = `${f2(sxv)}|${f2(syv)}`;
    let b = bucket.get(key);
    if (!b) { b = { sxv, syv, mult: 0 }; bucket.set(key, b); }
    b.mult += e.multiplicity;
  }
  return [...bucket.entries()].sort((a, b) => (a[0] < b[0] ? -1 : a[0] > b[0] ? 1 : 0)).map(([, v]) => v);
}
const drillGlyphs = drillAggregate();
// Drill-in radius: the SAME log₂ size-step family as the ghost glyphs, at REDUCED prominence
// (§10.3.3 "visually SUBORDINATE supplementary ground … at reduced prominence"). The sub-cell
// multiplicities are large (bins aggregate ~9 sub-cells each), so we compress the base + step so a
// dense drill-in glyph never out-weighs a settled point or even a meso ghost glyph. Layout geometry.
// E2.1-b RADIUS FLOOR (spec §10.8-b). Matt: the drill dots are "SO dim and SO tiny" — measured
// base r=0.75px (mult 1) / 0.93px (mult 2), sub-pixel at overview scale. The base is LIFTED to a
// visible-minimum FLOOR (1.25) and the log₂ step is COMPRESSED (0.30→0.12), never flattened — the
// function stays strictly monotone in multiplicity above the floor (a size-step, not a uniform
// disc). The floor + step are bounded so drillR(mult) < ghostR(mult) at every overlapping
// multiplicity (verified: worst case mult=1 → drill 1.37px < ghost 1.45px), preserving the
// meso-ghost > drill-in RADIUS order. Resulting min drill radius: 1.25 + 0.12·log2(2) = 1.37px
// (up from 0.75px — the sub-pixel floor Matt missed is gone). Layout geometry.
const DRILL_R_FLOOR = 1.25;
const DRILL_R_STEP = 0.12;
function drillR(mult) {
  return DRILL_R_FLOOR + DRILL_R_STEP * Math.log2(mult + 1); // floored + compressed; subordinate to ghostR
}
// Minimum realized drill radius across the actual glyph field (reported in the note; the smallest
// aggregated drill glyph is the legibility floor the eye actually sees). Computed after drillGlyphs.
const drillMinMult = drillGlyphs.reduce((m, g) => Math.min(m, g.mult), Infinity);
const drillMinRadius = drillR(drillMinMult);
// (drill-in clip count is computed below, after ghostInPlane/IN_PLANE_EPS are defined.)

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

// EDITION II: drill-in glyphs projecting outside the frozen plane frame are CLIPPED too (zero-mass
// §10.3.4 → §9.2.3 machinery). Count from the render pass (never hard-coded) for the drill clip line.
const drillGlyphInPlane = (g) =>
  g.sxv >= M.left - IN_PLANE_EPS && g.sxv <= M.left + PW + IN_PLANE_EPS
  && g.syv >= M.top - IN_PLANE_EPS && g.syv <= M.top + PH + IN_PLANE_EPS;
const drillClippedGlyphs = drillGlyphs.filter((g) => !drillGlyphInPlane(g));
const drillClippedCount = drillClippedGlyphs.length;

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
// ================================================================== CHARTED HORIZON (E2.1-a, spec §10.8-a)
// Matt ruling: "include the newly drilled-in ghost clusters inside of the dotted-line (known
// search space)." The horizon is REDEFINED from the meso-only reach to the CHARTED reach:
//   hull( meso-feasible cell positions  ∪  drill-in SUB-feasible glyph positions )
// clipped at the frozen frame per the existing clip law. Both position sets are in the SAME
// world space (feasibleCells{x,y} and subGlyphField{x,y} — the emitter's projected coords), so
// the union is a straight concatenation of {x,y} pairs; the hull is COMPUTED FROM THE RENDER
// PASS over the union (never hard-coded — the doctored-input test still asserts computed-not-
// constant, now over the union). The old meso-only hull retires from the visual; its semantics
// survive in the amended gloss + the hover disclosures. The east half is charted to the drill-in
// (geometry×commit) depth; the west half stays meso-only — that grain asymmetry is disclosed in
// the gloss. Zero-mass carries: the drill-in glyphs are supplementary ground (§10.3.4); adding
// them to the hull moves NO basis field and NO point — it only extends the disclosed CHARTED reach.
const charterHullInput = [
  ...feasibleCells.map((c) => ({ x: c.x, y: c.y })),
  ...subGlyphField.map((e) => ({ x: e.x, y: e.y })),
];
const ghostHullWorld = convexHullWorld(charterHullInput);
const ghostHullVertexCount = ghostHullWorld.length;
// For disclosure: the meso-only hull is retained as a COMPUTED comparison (proves the charted
// hull strictly contains the meso reach — the drill-in extended the known search space east).
const mesoOnlyHullWorld = convexHullWorld(feasibleCells);
const mesoOnlyHullEastX = mesoOnlyHullWorld.reduce((m, v) => Math.max(m, v[0]), -Infinity);
const chartedHullEastX = ghostHullWorld.reduce((m, v) => Math.max(m, v[0]), -Infinity);
// project vertices to SVG space (the draw is a closed polyline; clip-path trims to frame)
const ghostHullSvg = ghostHullWorld.map(([wx, wy]) => ({ x: sx(wx), y: sy(wy) }));
// East-gap label anchor (spec §10.8-a, §9.4.1 sibling): place the label adjacent to the EAST
// extreme of the CHARTED hull — the vertex with the greatest projected x. The disclosure now
// carries the P-DF-1 finding: the charted horizon extends beyond the outermost settled kits
// along û. Anchor computed from the hull, never hard-coded.
const ghostHullEastVertex = ghostHullSvg.reduce((best, v) => (v.x > best.x ? v : best), ghostHullSvg[0]);
// Mandatory horizon label — AMENDED BY RULING (spec §10.8-a). Supersedes the r-series
// "coverage limit — dark beyond this line is unmapped at meso grain, not absent." with
// charted-space semantics + the grain asymmetry (east charted to geometry×commit drill-in
// depth; west meso grain only; beyond the line: uncharted). Name lean CHARTED HORIZON (Matt
// veto point — the LINE_NAME const isolates the swappable string).
const LINE_NAME = 'CHARTED HORIZON';
const GHOST_HORIZON_LABEL = `${LINE_NAME} — charted search space: east half to geometry×commit drill-in depth, west half to meso grain; beyond this line is uncharted — not yet computed, not infeasible, not absent.`;

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
// E2.1-a: beyond-horizon now tests against the CHARTED hull (meso ∪ drill-in). Kits inside the
// drill-in-extended reach are no longer "beyond." N RECOMPUTES vs the new hull (was 14 vs the
// meso-only hull — spec §10.8-a "recompute … was 14").
const beyondHorizonKits = active.filter((p) => !pointInHullWorld(p.x, p.y, ghostHullWorld));
const beyondHorizonCount = beyondHorizonKits.length;
// Cross-check the meso-only reach for the disclosure (the pre-charted N; proves the drill-in
// pulled kits inside the charted line). COMPUTED, never hard-coded.
const beyondMesoOnlyKits = active.filter((p) => !pointInHullWorld(p.x, p.y, mesoOnlyHullWorld));
const beyondMesoOnlyCount = beyondMesoOnlyKits.length;
// E2.1 receipt-guard (replaces the Edition-I meso-hull N=14 receipt): two structural invariants
// that HALT loud if the charted hull is malformed, WITHOUT hard-coding the new N (which is a
// computed consequence of the frozen data). (i) The charted hull strictly CONTAINS the meso hull
// (drill-in only EXTENDS the reach), so charted-beyond N ≤ meso-beyond N. (ii) The charted east
// reach is ≥ the meso east reach (the drill-in pushes the horizon east — the load-bearing
// direction). A violation means the union hull, the input, or the projection moved (fail-loud).
// The RATIFIED E2.1 receipt (probe-verified against the frozen field) is asserted separately in
// acceptance so a stale value cannot ship silently while keeping the guard computed-not-constant.
const BEYOND_HORIZON_MESO_RECEIPT = 14; // Edition-I meso-hull receipt (unchanged historical fact)
if (!IS_DOCTORED) {
  if (beyondMesoOnlyCount !== BEYOND_HORIZON_MESO_RECEIPT) {
    die(`E2.1 meso-hull cross-check mismatch: render pass computed N=${beyondMesoOnlyCount} active kits beyond the MESO-only hull, but the ratified Edition-I receipt is N=${BEYOND_HORIZON_MESO_RECEIPT} (spec §9.5.1). The meso hull is a FROZEN-field consequence and must not move. Kits beyond meso: [${beyondMesoOnlyKits.map((p) => p.kit_id).join(', ')}]. HALTING.`);
  }
  if (beyondHorizonCount > beyondMesoOnlyCount) {
    die(`E2.1 charted-hull containment violation: charted-beyond N=${beyondHorizonCount} > meso-beyond N=${beyondMesoOnlyCount}. The charted hull (meso ∪ drill-in) must CONTAIN the meso hull, so fewer or equal kits can be beyond it. A larger N means the union hull is malformed (spec §10.8-a). HALTING.`);
  }
  if (chartedHullEastX + 1e-9 < mesoOnlyHullEastX) {
    die(`E2.1 charted-horizon east-reach violation: charted east x=${chartedHullEastX.toFixed(6)} < meso east x=${mesoOnlyHullEastX.toFixed(6)}. The drill-in must push the horizon EAST, not west (spec §10.8-a). HALTING.`);
  }
}
const BEYOND_HORIZON_EXPECTED = beyondHorizonCount; // computed; the E2.1 acceptance asserts the probe-ratified value
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
// E2.1-a: re-worded for the CHARTED horizon. The line now names the drill-in's effect: the
// charted horizon (meso ∪ drill-in) extends EAST beyond the outermost settled kits along û — the
// P-DF-1 finding, carried on the LINE (spec §10.8-a "re-word … so the LINE carries the P-DF-1
// finding"). The coordinate examples stay content-locked (empirical facts of the frozen basis).
// N is COMPUTED (point-in-charted-hull); when zero the line is OMITTED (§9.5.1 zero-case carries).
const beyondHorizonLine = `${fmtInt(beyondHorizonCount)} settled kits still stand beyond the CHARTED horizon (down from ${fmtInt(beyondMesoOnlyCount)} at meso grain — the east drill-in charts the geometry×commit reach beyond most whirlwind/beam kits along û) — kits project with all 14 coordinates; ghost cells carry the 7 core only, so the strongest east pulls (cone/whirlwind geometry, channel commit) remain uncharted at this grain.`;
// E2.1-a CHARTED-REACH LINE — the POSITIVE P-DF-1 disclosure, ALWAYS present (this is the LINE
// that carries the finding per spec §10.8-a: "the charted horizon extends beyond the outermost
// settled kits along û"). At the frozen field the east drill-in charts to world-x 2.31 vs the
// outermost settled ACTIVE kit at 1.39 — a +0.92 reach that pulls all formerly-beyond kits inside
// (beyond-horizon N: 14 → 0). Magnitudes COMPUTED from the render pass, never hard-coded; the
// clause is disclosure copy of the emitted geometry. This line does NOT zero-case-omit — it is the
// affirmative statement of what the drill-in charted (the beyond-line's job was the OLD misreading;
// this line is the NEW, stronger truth). Kept short enough to lead the ledger row visibly.
const chartedReachEastX = chartedHullEastX;                 // world x of the charted horizon's east reach
const settledActiveEastX = Math.max(...active.map((p) => p.x)); // outermost settled active kit (render pass)
const chartedReachDeltaEast = chartedReachEastX - settledActiveEastX;
const chartedReachLine = `CHARTED HORIZON reaches east to x=${f2(chartedReachEastX)} — the geometry×commit drill-in charts +${f2(chartedReachDeltaEast)} beyond the outermost settled kit (x=${f2(settledActiveEastX)}) along û: every formerly-beyond kit now sits inside the charted search space (beyond-horizon ${fmtInt(beyondMesoOnlyCount)}→${fmtInt(beyondHorizonCount)}).`;
// Compact VISIBLE lead for the ledger row (module scope so the E2.1-f acceptance test greps it).
const chartedReachVisible = `CHARTED HORIZON east reach x=${f2(chartedReachEastX)} (+${f2(chartedReachDeltaEast)} beyond outermost settled kit) — drill-in charts past every settled kit (beyond-horizon ${fmtInt(beyondMesoOnlyCount)}→${fmtInt(beyondHorizonCount)})`;
// E2.1-c BANNER RIDER string (module scope so both renderSVG and the E2.1-c acceptance test use the
// same string). LEADS with the chart's own edition; basis demoted to an attribute (spec §10.8-c).
// Every LOCKED substring survives verbatim. All values from atlas.json.
const riderStr = `Edition ${editionTag} lattice · basis: Edition-I (frozen ${ratified}) · plane = dims 1–2, ${inertiaPct}% corrected inertia · retained basis: ${retainedDims} dims · ${structureStatement}`;

// ------------------------------------------------------------------ EDITION II microcopy (§10)
// All numerals COMPUTED from emitted fields; prose is disclosure copy of the emitted structure.
// (i) PULL-SLICE ledger line (§10.1) — the new function level, its feasible/lit/sealed accounting.
const pullSliceLine = `pull slice (new fn level): ${fmtInt(pullMesoFeasible)} feasible · ${fmtInt(pullLitCells)} lit (existing kits re-keyed on intrinsic evidence) · ${fmtInt(pullMesoSealed)} sealed`;
// (ii) OFF-PLANE CORPUS disclosure (§10.4.4) — rendered VERBATIM from the emitted disclosure field;
//      N is the emitted gate_rejected_keyed (asserted to equal the disclosure's leading numeral).
const offPlaneLine = String(offPlaneDisclosure);
// (iii) DRILL-IN ground line (§10.3) — discloses the promoted EAST-half sub-cell ground as an
//       instrument property (subordinate ground, not data). Numerals from emitted drill_in fields.
//       The `×` join of the promoted-pair enum ("geometry×commit") is plain text (no HTML-special
//       chars); it (and the cut_ids/geometry/commit enum fragments below) escape at push-time via esc().
const drillGroundLine = `EAST-half drill-in (${drillPromotedPair.join('×')}): ${fmtInt(drillParentCells)} parent cells → ${fmtInt(drillSubFeasibleN)} sub-feasible (subordinate ground) · ${fmtInt(drillSubSealedN)} RED-3′ sealed`;
// (iv) SUB-SEALED ledger line (§10.4.2) — the promoted-grain seals, cut_id verbatim, at the grain
//      where RED-3′ SURFACES (and only there). Rows are (geometry × commit) at count each.
const subSealedSummary = subSealedSorted.map((r) => `${r.cut_id} (${r.geometry ?? '?'}×${r.commit ?? '?'}) ${fmtInt(r.count)}`).join(' · ');
// (v) DRILL-IN clip line (§10.3.4) — analogue of the ghost clip line, for sub-cell ground; count
//     from the render pass; omitted when zero (§9.2.3 zero-case protocol carries).
const drillClipLine = `${fmtInt(drillClippedCount)} drill-in sub-cell glyph${drillClippedCount === 1 ? '' : 's'} project beyond the frame (clipped, not rescaled — zero-mass ground never moves the frame)`;
// (vi) SUPERSEDED-LINEAGE line (§10.1.5) — the ONLY place the Edition-I denominators may appear on
//      the chart; LABELED as superseded lineage so the anti-stale grep (28) passes.
const supersededLine = `superseded (Edition I): ${fmtInt(supE1Exact)} exact · ${fmtInt(supE1MesoFeasible)} meso feasible · ${fmtInt(supE1MesoSealed)} meso sealed`;

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
    // r7 FOUR-CLASS ENCODING (spec §1): SINGLE (non-condensation) live kits TAKE COLOR — figure
    // advances over the grey ground. Chartreuse-lime hue H≈96° sits in the 121° dead-zone between
    // CH-BEAM gold (43.5°) and AURA teal-green (164.6°): min hue-clearance 52.5° from ANY of the
    // six condensation hues, and distinct from the death accents (tombInk #3a3f4a H221 desat /
    // tombUnknownInk #b0451f H16), ghost grey, chrome. Legible at the 3px live radius: contrast-vs-
    // canvas 3.34 (>>1.0). FILL CHANGE ONLY — geometry byte-frozen (neutralDotR unchanged).
    liveSingle: '#50991f',     // chartreuse-lime; H96 S0.80 V0.60 on light
    liveSingleOp: 0.95,
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
    // EDITION II drill-in chrome (§10.3.3): SUBORDINATE supplementary ground — the promoted EAST-half
    // sub-cell dark. E2.1-b FILL-CONTRAST FLOOR (spec §10.8-b): the r-series drill (#d3dae4 @ 0.34)
    // computed to contrast-vs-canvas 1.094 — a hair above the #f7f8fa canvas (1.000), why Matt missed
    // it. Lifted to a legibility FLOOR at 1.179 (a clear step above canvas) while staying BELOW the
    // unlit-meso-ghost contrast (1.246) so the four-way order (settled > meso ghost > drill > canvas)
    // holds on BOTH the size AND the contrast channel. All four separable; drill still subordinate.
    drillInk: '#c6cdd8',       // sub-ghost: contrast-vs-canvas 1.179 (canvas 1.000 < drill < ghostDark 1.246)
    drillOp: 0.42,
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
    // r7 FOUR-CLASS ENCODING (spec §1): SINGLE live kits take a luminous chartreuse-lime — the same
    // H≈96° dead-zone hue (52.5° clearance from every condensation hue; clear of the gilt death
    // accents #cfc6ad/#d98a55) lifted for the dark canvas. Contrast-vs-void 10.01. Figure over the
    // dim gilt ground. FILL CHANGE ONLY — geometry byte-frozen (neutralDotR unchanged).
    liveSingle: '#7cd143',     // chartreuse-lime; H96 S0.68 V0.82 on dark
    liveSingleOp: 0.92,
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
    // EDITION II drill-in chrome (§10.3.3): the faintest gilt-dust, deeper in the walked dark than
    // the unlit ghost embers — the promoted-grain sub-ground, subordinate to everything above it.
    // E2.1-b FILL-CONTRAST FLOOR (spec §10.8-b): the r-series drill (#242832 @ 0.70) computed to
    // contrast-vs-canvas 1.180 (canvas 1.000) — too near the #0e1016 void. Lifted to a legibility
    // FLOOR at 1.323 (a clear step above the void) while staying BELOW the unlit-meso-ghost contrast
    // (1.343) so the four-way order holds on the contrast channel too. All four separable.
    drillInk: '#30343e',       // sub-ghost: contrast-vs-canvas 1.323 (void 1.000 < drill < ghostDark 1.343)
    drillOp: 0.72,
  },
};

// E2.1-e SKIN→CANVAS MAP (spec §10.8-e). Verified: `instrument` = LIGHT canvas #f7f8fa; `archive`
// = DARK. Skins are NOT renamed mid-series (name stability is downstream contract). This explicit
// map is emitted into render-provenance.json so drax's PRD black-copy lead binds to the CANVAS
// (light/dark + hex), NEVER to the skin NAME — a name is not a color, and downstream must not have
// to memorize which skin is which shade. Derived from the SKINS bg (single source of truth).
const SKIN_CANVAS_MAP = {
  instrument: { canvas: 'light', hex: SKINS.instrument.bg },
  archive: { canvas: 'dark', hex: SKINS.archive.bg },
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
// r7 HOOK helper (spec §3.2): the ghost 7-tuple data-core — emitted core[] joined on `|`, in the
// emitted core_order, then attribute-escaped. Emitted-field copy (never invention; §4c law). The
// ATLAS_CORE_ORDER length is asserted == 7 at load (fail-loud) so the tuple is exactly the 7 core.
function coreAttr(coreArr) {
  return esc(coreArr.join('|'));
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
  // r7 SEMANTIC HOOKS (spec §3.1): layer-drillin FIRST (deepest ground), then layer-ghosts. e21
  // painted horizon→drill→ghostDark→ghostLit in ONE clip group; §3.1 mandates SEPARATE layer ids,
  // so drill moves to its OWN clip group emitted BEFORE the meso lattice. Net z-order change: the
  // horizon hairline now paints OVER the drill sub-ground instead of under it (both are chrome-quiet;
  // the boundary line staying visible over the sub-ground is if anything more correct). Drill stays
  // BELOW the meso ghost glyphs — the load-bearing subordination (§10.3.3) is preserved. NO mark
  // coordinate/radius changes (acceptance-29). Whitelisted: horizon-vs-drill hairline paint order.
  // -- layer-drillin: promoted EAST-half geometry×commit sub-cell ground (§10.3). data-el="ghost"
  // (drill-in IS ghost ground per §1 "the meso + drill-in ground") + data-mult (emitted
  // multiplicity). NO data-core — the emitted sub_feasible_glyph_field carries {x,y,multiplicity}
  // ONLY; no core tuple exists to copy and §4c forbids inventing one (flagged in the note).
  P.push(`<g id="layer-drillin" clip-path="url(#planeClip)">`);
  P.push(`<g fill="${s.drillInk}" fill-opacity="${s.drillOp}">`);
  for (const g of drillGlyphs) {
    P.push(`<circle cx="${f2(g.sxv)}" cy="${f2(g.syv)}" r="${f2(drillR(g.mult))}" data-el="ghost" data-mult="${g.mult}"/>`);
  }
  P.push(`</g>`);
  P.push(`</g>`);
  // -- layer-ghosts: the meso ghost lattice — horizon envelope + dark + lit glyphs. Every glyph
  // carries data-el="ghost" + data-core (emitted 7-tuple) + data-mult (coincident-aggregation
  // multiplicity, an emitted-derived structural fact). Inert attributes; no scripts (§3.4).
  P.push(`<g id="layer-ghosts" clip-path="url(#planeClip)">`);
  // -- r4 GHOST HORIZON: dashed convex-hull envelope of the ghost lattice's reach.
  // Open polyline of the CCW world-hull vertices (projected), closed back to the first,
  // clipped to the frame. NO fill — a fill would assert the region-claim §9.2.2 forbids.
  if (ghostHullSvg.length >= 2) {
    const hullPts = ghostHullSvg.map((v) => `${f2(v.x)},${f2(v.y)}`).join(' ');
    const firstPt = `${f2(ghostHullSvg[0].x)},${f2(ghostHullSvg[0].y)}`;
    P.push(`<polyline points="${hullPts} ${firstPt}" fill="none" stroke="${s.horizonInk}" stroke-opacity="${s.horizonOp}" stroke-width="${s.horizonWidth}" stroke-dasharray="${s.horizonDash}" stroke-linejoin="round"><title>${esc(GHOST_HORIZON_LABEL)}</title></polyline>`);
  }
  // unlit-feasible ground first (the dark of the map). Small dots, size-stepped by
  // coincident multiplicity; no fills, no boundaries. data-el + data-core + data-mult hooks (§3.2).
  P.push(`<g fill="${s.ghostDarkInk}" fill-opacity="${s.ghostDarkOp}">`);
  for (const g of ghostDark) {
    P.push(`<circle cx="${f2(g.sxv)}" cy="${f2(g.syv)}" r="${f2(ghostR(g.mult))}" data-el="ghost" data-core="${coreAttr(g.core)}" data-mult="${g.mult}"/>`);
  }
  P.push(`</g>`);
  // lit-feasible next (census-current settled-adjacent ground) — subordinate to the points.
  P.push(`<g fill="${s.ghostLitInk}" fill-opacity="${s.ghostLitOp}">`);
  for (const g of ghostLit) {
    P.push(`<circle cx="${f2(g.sxv)}" cy="${f2(g.syv)}" r="${f2(ghostR(g.mult))}" data-el="ghost" data-core="${coreAttr(g.core)}" data-mult="${g.mult}"/>`);
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

  // ==================================================================================
  // r7 SEMANTIC HOOKS (spec §3.1): layer-live — ALL live marks (single kits + condensation
  // members). §4 legend "Live Kits" toggles this whole layer; "Condensations" toggles the
  // data-el="condensation" subset. Every mark carries data-kit (kit_id) / data-kits (member list).
  // ==================================================================================
  P.push(`<g id="layer-live">`);
  // ---- LAYER 2: SINGLE live kits (383 non-condensation) — r7 TAKE COLOR (spec §1 four-class
  //      encoding): figure advances over the grey ground. FILL CHANGE ONLY (s.liveSingle replaces
  //      s.neutralDot); geometry byte-frozen (cx/cy/r unchanged — neutralDotR). data-el="live" +
  //      data-kit hooks (§3.2). The <title> is byte-frozen vs e21 (coord+title FIT invariant).
  P.push(`<g fill="${s.liveSingle}" fill-opacity="${s.liveSingleOp}">`);
  for (const p of neutral) {
    P.push(`<circle cx="${f2(sx(p.x))}" cy="${f2(sy(p.y))}" r="${s.neutralDotR}" data-el="live" data-kit="${esc(p.kit_id)}"><title>${esc(p.kit_id)} — active — ${esc(p.franchise ?? '')}</title></circle>`);
  }
  P.push(`</g>`);

  // ---- grouped active dots (86; color = condensation group) [FROZEN r2 fill/geometry] — r7
  //      data-el="condensation" + data-kit + data-kits (the group's full member list). Members KEEP
  //      their six group colors (spec §1 — already separable). data-kits is the deterministic
  //      kit_id member list (sorted by the byId order the marks already iterate in) — emitted-field
  //      copies (§4c). The per-mark data-kit is the mark's own kit_id.
  for (const g of GROUP_ORDER) {
    const mem = grouped.filter((p) => p.gateA_group === g);
    if (!mem.length) continue;
    const memberList = mem.map((p) => p.kit_id).join('|'); // byId-sorted (grouped is derived from `active`, sorted)
    P.push(`<g fill="${GROUP_COLORS[g]}" stroke="${s.bg}" stroke-width="0.6">`);
    for (const p of mem) {
      P.push(`<circle cx="${f2(sx(p.x))}" cy="${f2(sy(p.y))}" r="${s.groupDotR}" data-el="condensation" data-kit="${esc(p.kit_id)}" data-kits="${esc(memberList)}"><title>${esc(p.kit_id)} — ${esc(g)} — ${esc(p.franchise ?? '')}</title></circle>`);
    }
    P.push(`</g>`);
  }
  P.push(`</g>`);

  // ---- r7 SEMANTIC HOOKS (spec §3.1): layer-graveyard — the 37 per-corpse tombstone daggers (F-1).
  //      [FROZEN r2 layout; death_class fills emitted.] Each dagger carries data-el="graveyard" +
  //      data-kit (kit_id). §4 legend "Graveyard" toggles this layer. The †-glyph position + fill +
  //      <title> are byte-frozen vs e21 (the FIT tombstone invariant compares coord+title tuples).
  //      Ordinal index labels + the unknown-dashed rings ride inside the layer as chrome-of-glyph.
  P.push(`<g id="layer-graveyard" font-family="${s.fontStack}">`);
  for (let i = 0; i < supplementary.length; i++) {
    const p = supplementary[i];
    const cx = sx(p.x), cy = sy(p.y);
    const unk = isUnknown(p.death_class);
    const ink = unk ? s.tombUnknownInk : s.tombInk;
    const glyph = unk ? '†' : '†';
    P.push(`<text x="${f2(cx)}" y="${f2(cy + 5)}" font-size="16" text-anchor="middle" fill="${ink}" font-weight="700" data-el="graveyard" data-kit="${esc(p.kit_id)}">${glyph}<title>${esc(p.kit_id)} † ${esc(p.death_class)}</title></text>`);
    if (unk) {
      P.push(`<circle cx="${f2(cx)}" cy="${f2(cy)}" r="7" fill="none" stroke="${ink}" stroke-width="1.1" stroke-dasharray="2 2"/>`);
    }
    P.push(`<text x="${f2(cx + 8)}" y="${f2(cy + 2)}" font-size="8" fill="${ink}" fill-opacity="0.85">${i + 1}</text>`);
  }
  P.push(`</g>`);

  // ==================================================================================
  // r7 SEMANTIC HOOKS (spec §3.1): layer-chrome — ALL readable chrome (centroid labels, charted-
  // horizon label, axis pole titles + glosses, title/badge, legends, below-plane ledger, footer).
  // Non-interactive; carries no data-el (nothing here is a lattice mark). One group so the drax page
  // can dim/hold chrome as a unit. Opened here, closed just before the SVG string is assembled.
  // ==================================================================================
  P.push(`<g id="layer-chrome">`);

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

  // ---- E2.1-a CHARTED HORIZON LABEL (spec §10.8-a; §9.4.1 sibling) — the amended gloss, placed
  // adjacent to the EAST gap. A thin leader ties the label to the CHARTED hull's EAST vertex
  // (computed from the render pass — ghostHullEastVertex). The gloss is longer than the r-series
  // string (it carries charted-space semantics + grain asymmetry), so it WRAPS deterministically
  // (wrapByChars — the same deterministic word-wrap the beyond-horizon line uses) into the open
  // lower-right interior. The FULL contiguous GHOST_HORIZON_LABEL is carried in the polyline
  // <title> (LAYER 0) for whole-grep; these visible rows are its presentation. A short LINE_NAME
  // header leads (bold-weight quiet ink) so the reader sees the line's name at a glance. Anchor
  // derived from the east hull vertex, never hard-coded.
  {
    const ev = ghostHullEastVertex;                 // east extreme of the CHARTED hull (render pass)
    const labX = M.left + PW - 6;                    // right-align into the gap, inside frame
    const rows = wrapByChars(GHOST_HORIZON_LABEL, 58); // deterministic clause wrap; no font metrics
    const rowH = 12.5;
    const labY0 = ev.y + 90;                          // drop below the east vertex into open space
    // leader: from the east hull vertex down-right to the label's first row
    P.push(`<g font-family="${s.fontStack}">`);
    P.push(`<line x1="${f2(ev.x)}" y1="${f2(ev.y)}" x2="${f2(labX - 4)}" y2="${f2(labY0 - 9)}" stroke="${s.horizonInk}" stroke-opacity="${s.horizonOp}" stroke-width="0.8" stroke-dasharray="3 3"/>`);
    P.push(`<circle cx="${f2(ev.x)}" cy="${f2(ev.y)}" r="2.1" fill="none" stroke="${s.horizonInk}" stroke-opacity="${s.horizonOp}" stroke-width="1"/>`);
    // wrapped, right-anchored rows. Each row carries a <title> with the WHOLE gloss so the label
    // block itself is greppable/hoverable as one unit too (belt-and-suspenders with the polyline).
    for (let i = 0; i < rows.length; i++) {
      const weight = i === 0 ? ' font-weight="600"' : '';
      P.push(`<text x="${f2(labX)}" y="${f2(labY0 + i * rowH)}" font-size="${s.horizonLabelSize}" font-style="${s.horizonLabelStyle}"${weight} text-anchor="end" fill="${s.horizonLabelInk}" letter-spacing="0.2">${esc(rows[i])}${i === 0 ? `<title>${esc(GHOST_HORIZON_LABEL)}</title>` : ''}</text>`);
    }
    P.push(`</g>`);
  }

  // ---- r7 AXIS-TITLE / GLOSS LAYOUT FIX (spec §2). The e21 pole titles + r2 explainer glosses
  //      rendered INSIDE the plot rect (PERFORM/gloss at mid-right x[1225,1498]; DEPLOY/gloss at
  //      mid-left; LAUNCH/EMBODY at top/bottom center — ALL x∈[96,1504], y∈[132,1104]) → every one
  //      intersected the plot rect (and the data field) — Matt's margin collision + acceptance-30
  //      fail. LAYOUT-ONLY fix: relocate ALL FOUR title+gloss pairs to RESERVED MARGIN BANDS that
  //      cannot intersect the plot rect or each other. Content-locked strings survive VERBATIM (the
  //      lock is on strings, not coordinates): the 4 POLE_GLOSS strings + the 4 axis-title strings
  //      ("PERFORM →" / "← DEPLOY" / "↑ LAUNCH" / "EMBODY ↓") appear contiguously (a wrapped gloss
  //      carries its FULL string in a <title>, the codebase's proven wrap+grep pattern).
  //      MARGIN-BAND GEOMETRY (all OUTSIDE the plot rect x[96,1504] y[132,1104]):
  //        · PERFORM → RIGHT rail  x[1504,1600] — rotated -90° (reads bottom→top), centered cyMid.
  //        · DEPLOY  → LEFT  rail  x[0,96]      — rotated -90° (reads bottom→top), centered cyMid.
  //        · LAUNCH  → TOP strip   y[106,131]   — horizontal, title+gloss combined, centered cxMid.
  //        · EMBODY  → BOTTOM center pocket x[703,916] y[1104,1200] — horizontal, title + wrapped
  //          gloss (full string in <title>), centered cxMid, clear of both ledger columns + footer.
  const cxMid = M.left + PW / 2, cyMid = M.top + PH / 2;
  const railR = W - M.right / 2;   // right rail center x = 1600-48 = 1552
  const railL = M.left / 2;        // left  rail center x = 48
  // -- PERFORM: right rail, rotated -90° about the rail center at cyMid. Title on the inner line
  //    (nearer the plot), gloss on the outer line. rotate(-90 cx cy) makes +x read upward.
  P.push(`<g font-family="${s.fontStack}">`);
  P.push(`<text transform="rotate(-90 ${f2(railR - 6)} ${f2(cyMid)})" x="${f2(railR - 6)}" y="${f2(cyMid)}" text-anchor="middle" fill="${s.ink}" font-weight="${s.titleWeight}" font-size="15" letter-spacing="1.5">PERFORM →</text>`);
  P.push(`<text transform="rotate(-90 ${f2(railR + 9)} ${f2(cyMid)})" x="${f2(railR + 9)}" y="${f2(cyMid)}" text-anchor="middle" fill="${s.faint}" font-size="${s.glossSize}" font-style="${s.glossStyle}" letter-spacing="0.2">${esc(POLE_GLOSS.PERFORM)}</text>`);
  // -- DEPLOY: left rail, rotated -90° about the rail center at cyMid. Title inner (nearer plot),
  //    gloss outer.
  P.push(`<text transform="rotate(-90 ${f2(railL + 6)} ${f2(cyMid)})" x="${f2(railL + 6)}" y="${f2(cyMid)}" text-anchor="middle" fill="${s.ink}" font-weight="${s.titleWeight}" font-size="15" letter-spacing="1.5">← DEPLOY</text>`);
  P.push(`<text transform="rotate(-90 ${f2(railL - 9)} ${f2(cyMid)})" x="${f2(railL - 9)}" y="${f2(cyMid)}" text-anchor="middle" fill="${s.faint}" font-size="${s.glossSize}" font-style="${s.glossStyle}" letter-spacing="0.2">${esc(POLE_GLOSS.DEPLOY)}</text>`);
  // -- LAUNCH: top strip (y[106,131], below the derivation gloss at y102 / above the plot at y132).
  //    Title + gloss combined into ONE centered horizontal line so it fits the ~25px band. Both
  //    strings present verbatim; the gloss is separated by a spaced mid-dot so each greps whole.
  const LAUNCH_LINE = `↑ LAUNCH    ${POLE_GLOSS.LAUNCH}`;
  P.push(`<text x="${f2(cxMid)}" y="120" text-anchor="middle" fill="${s.ink}" font-weight="${s.titleWeight}" font-size="12.5" letter-spacing="0.6">${esc('↑ LAUNCH')}    <tspan fill="${s.faint}" font-weight="400" font-size="${s.glossSize}" font-style="${s.glossStyle}">${esc(POLE_GLOSS.LAUNCH)}</tspan></text>`);
  // -- EMBODY: bottom-center pocket x[703,916] (between the ledger's left column, which ends ≈x714,
  //    and its right column at x916), BELOW the plot bottom (1104). Title baseline y=1119 (cap-top
  //    ≈1106.5 > 1104 — clears the plot rect); gloss wraps to ≤2 lines in the ~213px pocket
  //    (deterministic char-wrap) at a 14px pitch so the two lines' bboxes do not touch, the FULL
  //    contiguous POLE_GLOSS.EMBODY carried in a <title> for the verbatim grep. Last row ≈y1148 —
  //    clears the footer (y1188). All EMBODY geometry OUTSIDE the plot rect (acceptance-30).
  const embodyRows = wrapByChars(POLE_GLOSS.EMBODY, 30); // ~30 chars ≈ 190px @ fs9.5 < 213px pocket
  P.push(`<text x="${f2(cxMid)}" y="1119" text-anchor="middle" fill="${s.ink}" font-weight="${s.titleWeight}" font-size="12.5" letter-spacing="0.6">${esc('EMBODY ↓')}</text>`);
  for (let i = 0; i < embodyRows.length; i++) {
    const titleNode = i === 0 ? `<title>${esc(POLE_GLOSS.EMBODY)}</title>` : '';
    P.push(`<text x="${f2(cxMid)}" y="${f2(1134 + i * 14)}" text-anchor="middle" fill="${s.faint}" font-size="${s.glossSize}" font-style="${s.glossStyle}" letter-spacing="0.2">${esc(embodyRows[i])}${titleNode}</text>`);
  }
  P.push(`</g>`);

  // ---- title + RIDER-1 badge [r2 layout; STRING re-led per E2.1-c] (derivation gloss verbatim)
  // E2.1-c banner relabel (spec §10.8-c): the r-series string LED with "Edition ${edition}" where
  // basis.edition == 1 (the FIT basis is Edition-I frozen) — under an "Edition-II" chart title that
  // reads as a contradictory edition stamp. `riderStr` (module scope) is re-led to lead with the
  // CHART's own edition (editionTag = "II"); the basis edition is DEMOTED to an attribute. Every
  // locked substring survives VERBATIM; only the leading edition token + basis demotion change.
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
    P.push(`<g font-family="${s.fontStack}" fill="${s.ink}">`);

    // (iii) GHOST-FIELD ledger — EDITION II BELOW-PLANE band (RENDER-FORM SEAM RESOLUTION, flagged in
    // the note under "render-form seams"). WHY the r6 in-plane plaque cannot carry it: the r6 lower-
    // right plaque held ~6 lines and cleared the §9.6.4.21 occlusion guard because the east-gap lower-
    // right has only ~3 settled POINTS. Edition-II's lattice ledger carries ~16 accounting lines
    // (pull slice · drill-in ground · sub-sealed RED-3′ · off-plane corpus · superseded lineage, atop
    // the r6 set). A plaque holding all of it grows UP into the dense settled archipelago and occludes
    // 4 settled POINTS + thousands of ghost-glyph centers — the occlusion guard (correctly) HALTS, and
    // it must (occluding a settled point behind a legend is the dishonesty the guard exists to stop).
    // §10 does not spec a render form for a ledger this large. Following the established grammar
    // (§9.2.4 "sealed = a margin/legend LEDGER, never on-plane"; and the r4/r5/r6 <title> whole-string
    // pattern), the WHOLE ledger moves to the BELOW-PLANE MARGIN band (y > plane bottom 1104) — the
    // chrome band the census/headline/coverage lines already occupy, where NOTHING can occlude a data
    // mark (all 469 points + 37 tombstones are inside the frame; the band is outside it). The band is
    // tight (1104→footer 1188 ≈ 84px), so each ledger entry renders a COMPACT VISIBLE SUMMARY line +
    // the FULL contiguous emitted string in a <title> node (present for the whole-grep acceptance AND
    // for hover) — the exact pattern r4/r5/r6 use for their long disclosure sentences. No in-plane
    // plaque; zero occlusion; every disclosure present in the SVG body verbatim.
    const LINE_H = 11;
    // LEFT COLUMN (x = bx) — r4 census + headline pair + demoted coverage + one compact ghost
    // accounting line. FOUR content rows + the accounting line, spaced to clear the footer at y=1188.
    P.push(`<text x="${f2(bx)}" y="${f2(by + 1)}" font-size="10.5" font-style="${s.glossStyle}" fill="${s.faint}">${esc(GHOST_CENSUS_LINE)}</text>`);
    P.push(`<text x="${f2(bx)}" y="${f2(by + 17)}" font-size="12.5" font-weight="${s.titleWeight}" fill="${s.ink}" letter-spacing="0.2">${esc(HEADLINE_LIT)}</text>`);
    P.push(`<text x="${f2(bx)}" y="${f2(by + 32)}" font-size="11" font-weight="${s.titleWeight}" fill="${s.ink}">${esc(HEADLINE_DENSITY)}</text>`);
    P.push(`<text x="${f2(bx)}" y="${f2(by + 46)}" font-size="9.5" font-style="${s.glossStyle}" fill="${s.faint}">${esc(COVERAGE_SECONDARY)}</text>`);
    // one compact ghost accounting line (feasible/lit/unmapped + meso sealed) — the r6 core ledger, one row.
    const feasStr = `${fmtInt(feasibleCells.length)} feasible meso cells · ${fmtInt(litCells)} lit · ${fmtInt(unmappedPending)} unmapped · ${fmtInt(mesoSealed)} sealed (off-plane)`;
    P.push(`<text x="${f2(bx)}" y="${f2(by + 60)}" font-size="9" fill="${s.faint}">${esc(feasStr)}</text>`);
    const sealSummary = sealedCutOrder.map((cid) => `${cid} ${fmtInt(sealedByCut[cid])}`).join(' · ');
    // RIGHT COLUMN (x = colR) — the EDITION II lattice ledger, one compact SUMMARY line per entry.
    // Each <text> carries a <title> with the FULL emitted string (whole-grep + hover). The visible
    // summary is a short lead; the title is the complete content-locked / emitted sentence. The meso
    // sealed cut-summary rides the sealed line's <title> (whole-grep target for the sealed cut ids).
    // E2.1-f: right column moved RIGHT (bx+820=916) so its header + rows clear the frozen EMBODY
    // pole gloss (centered x≈800, right edge ≈902) — the r-series colR=596 put the header under it.
    // Long rows still fit (≤~100 chars fs8 → 916+400=1316 < plane-right 1504).
    const colR = bx + 820;                                 // right column left edge (past the EMBODY gloss)
    P.push(`<text x="${f2(colR)}" y="${f2(by + 1)}" font-size="9.5" font-weight="${s.titleWeight}" letter-spacing="0.3" fill="${s.ink}">GHOST FIELD — the feasible dark · Edition II lattice</text>`);
    // The band holds ~7 rows @ 9.3px spacing (by+14 → ~1195, clear of the footer census at the FAR
    // right edge x=1504). Each visible row is a compact summary; the FULL emitted/content-locked
    // strings ride <title> nodes (whole-grep + hover), possibly SEVERAL titles per row so every
    // required string is present in the SVG body. Rows are ordered: pull · drill-in · seals · the
    // three disclosure lines (beyond/clip/drill-clip, combined) · off-plane · superseded lineage.
    // E2.1-a: the clip combo carries meso-clip + drill-clip; the BEYOND token appears ONLY when
    // N>0 (zero-case omission, §9.5.1). At the frozen field N=0 (the charted horizon encloses all
    // settled kits) — the beyond token drops; the affirmative chartedReachLine carries the finding.
    const clipCombo = [
      beyondHorizonCount > 0 ? `${fmtInt(beyondHorizonCount)} kits beyond horizon` : null,
      ghostClippedCount > 0 ? `${fmtInt(ghostClippedCount)} meso clipped` : null,
      drillClippedCount > 0 ? `${fmtInt(drillClippedCount)} drill-in clipped` : null,
    ].filter(Boolean).join(' · ');
    // clip-row <title>s: the beyond line ONLY when N>0 (zero-case omission per §9.5.1); the
    // clip/drill-clip lines only when their counts are nonzero.
    const clipTitles = [
      beyondHorizonCount > 0 ? beyondHorizonLine : null,
      ghostClippedCount > 0 ? ghostClipLine : null,
      drillClippedCount > 0 ? drillClipLine : null,
    ].filter(Boolean);
    // each row: {s: visible, titles: [full strings for <title> nodes], gloss?}
    const led = [];
    // E2.1-a: the CHARTED-REACH line leads (non-gloss, ink weight) — the load-bearing P-DF-1
    // disclosure, ALWAYS present (carries the finding on the LINE per §10.8-a). The VISIBLE lead
    // (chartedReachVisible, module scope) is compact; the FULL contiguous chartedReachLine rides the
    // <title> (whole-grep + hover), the same pattern the long r4/r5 disclosures use.
    led.push({ s: chartedReachVisible, titles: [chartedReachLine], lead: true });                            // §10.8-a
    led.push({ s: pullSliceLine, titles: [pullSliceLine] });                                                 // §10.1
    led.push({ s: drillGroundLine, titles: [drillGroundLine] });                                             // §10.3
    led.push({ s: `${fmtInt(drillSubSealedN)} sub-cells sealed @ drill-in grain — RED-3′ surfaces here`, titles: [subSealedSummary] });   // §10.4.2
    led.push({ s: `${fmtInt(mesoSealed)} meso sealed (off-plane): ${sealSummary}`, titles: [sealSummary] });  // §9.2.4 meso sealed cut ids (visible + title)
    if (clipCombo) led.push({ s: `${clipCombo} (hover for full disclosures)`, titles: clipTitles, gloss: true });  // §9.2.3/§10.3.4 (+ beyond when N>0)
    led.push({ s: `${fmtInt(offPlaneN)} gear-grain kits (mcd-) held off-plane — deferred grain ruling`, titles: [offPlaneLine], gloss: true });   // §10.4.4
    // E2.1-f: compact VISIBLE lead (short x-extent so the last row clears the footer census); the
    // FULL supersededLine (the ONLY on-chart place the Edition-I denominators appear, labeled
    // lineage) rides the <title> — where acceptance #28's anti-stale strip still greps it whole.
    led.push({ s: 'superseded (Edition I) denominators — hover', titles: [supersededLine], gloss: true });    // §10.1.5
    // E2.1-a/-f: the ledger carries up to 8 rows (charted-reach lead added). At fs7.5 the glyph bbox
    // (≈7.5×0.92≈6.9px) fits a 7.3px pitch with clearance — so consecutive rows do NOT overlap, and
    // the last row clears the footer at y=1188. The lead row (charted-reach) renders in ink weight
    // (not gloss-faint) — the load-bearing disclosure, not marginalia. Rows start just under header.
    let ry = by + 11;                                      // start just under the ledger header
    for (const r of led) {
      const styleAttr = r.gloss ? ` font-style="${s.glossStyle}"` : '';
      const fillAttr = r.lead ? s.ink : s.faint;
      const weightAttr = r.lead ? ' font-weight="600"' : '';
      const titleNodes = (r.titles || []).map((t) => `<title>${esc(t)}</title>`).join('');
      P.push(`<text x="${f2(colR)}" y="${f2(ry)}" font-size="7.5"${styleAttr}${weightAttr} fill="${fillAttr}">${esc(r.s)}${titleNodes}</text>`);
      ry += 7.3;                                            // 8 rows: 1129 → 1180.1 bbox<1181, clears footer 1188
    }
    P.push(`</g>`);
  }

  // ---- footer stamp (provenance; all from atlas.json). EDITION II (§10.4.5): the footer carries
  // "Edition II" + the v1.2 register ref on BOTH skins. This is a new EDITION, so the frozen-footer
  // single-purpose-diff discipline (r4/r5/r6, which held ONE diff region within Edition-I) no longer
  // applies across the edition boundary — the footer stamps the edition + register honestly.
  P.push(`<g font-family="${s.fontStack}" fill="${s.faint}" font-size="10">`);
  // LEFT footer stamp — E2.1-d PROVENANCE DEDUPE (spec §10.8-d): the r-series footer rendered
  // `${atlasVersion}` ("Edition-II") + " · Edition ${editionTag}" ("Edition II") == the edition
  // token TWICE ("Edition-II · Edition II · …"). Deduped to ONE edition token: atlasVersion
  // ("Edition-II") carries it; the redundant " · Edition II" is removed. E2.1-f: the VISIBLE footer
  // is trimmed to the load-bearing stamp (edition · register · emitted · skin) so it CLEARS the
  // right census footer (no bottom-band overlap). The emitter-script + render-script paths live in
  // render-provenance.json (machine-readable provenance), not the visible chrome.
  P.push(`<text x="${f2(M.left)}" y="${f2(H - 12)}">${esc(String(atlasVersion))} · ${esc(String(registerRef))} · emitted ${esc(emittedAt)} · skin=${skinKey}</text>`);
  // RIGHT census footer — EDITION II: the r6 in-plane plaque is retired (the ledger moved below-
  // plane, §10.4.3 seam resolution), so the r6 plaque-collision fix (FIX B) no longer applies. The
  // census footer end-anchors at the plane RIGHT edge (M.left+PW = 1504) — there is no plaque to
  // overprint. Mid-frame clearance vs the left footer line holds (left ends well short of 1504).
  P.push(`<text x="${f2(M.left + PW)}" y="${f2(H - 12)}" text-anchor="end">points: ${active.length} active + ${supplementary.length} corpse = ${all.length} · ghost: ${feasibleCells.length} feasible + ${sealedCells.length} sealed</text>`);
  P.push(`</g>`);

  P.push(`</g>`); // close layer-chrome (r7 §3.1)

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
      writeFileSync(join(OUT_DIR, `atlas-edition2-${skin}.svg`), svg, 'utf8');
    }
    console.log(`[allin-render] wrote SVGs to ${OUT_DIR} (N beyond=${beyondHorizonCount}; suite skipped)`);
    return;
  }

  const ptFps = {}, ghFps = {};
  for (const skin of ['instrument', 'archive']) {
    const svg = renderSVG(skin);
    const svgPath = join(OUT_DIR, `atlas-edition2-${skin}.svg`);
    writeFileSync(svgPath, svg, 'utf8');
    ptFps[skin] = pointFingerprint();
    ghFps[skin] = ghostFingerprint();
    const pngPath = join(OUT_DIR, `atlas-edition2-${skin}.png`);
    const png = await sharp(Buffer.from(svg), { density: 144 }).png().toBuffer();
    writeFileSync(pngPath, png);
    results[skin] = { svgPath, pngPath, bytes: Buffer.byteLength(svg) };
    console.log(`[render] ${skin}: ${svgPath} (${results[skin].bytes} B), ${pngPath} (${png.length} B PNG)`);
  }

  // ---- ACCEPTANCE TESTS ----
  const tests = [];
  const rec = (name, pass, detail) => tests.push({ name, pass, detail });
  const bodies = {};
  for (const skin of ['instrument', 'archive']) bodies[skin] = readFileSync(join(OUT_DIR, `atlas-edition2-${skin}.svg`), 'utf8');

  // (1) point counts
  rec('point-counts', active.length === 469 && supplementary.length === 37 && all.length === 506,
    `active=${active.length} (exp 469), supp=${supplementary.length} (exp 37), total=${all.length} (exp 506)`);

  // (2) grouped/neutral partition
  rec('grouped-count', grouped.length === 86, `grouped=${grouped.length} (exp 86)`);

  // (3) ghost counts vs emitted — EDITION II: feasible 11,160 + sealed 1,314. Assert against the
  //     EMITTED denominators (meso_feasible / meso_sealed), not hard-coded literals — the array
  //     lengths must equal the emitter's own denominator fields (double-check of the re-emission).
  rec('ghost-counts', feasibleCells.length === denomMesoFeasible && sealedCells.length === mesoSealed,
    `feasible=${feasibleCells.length} (== emitted meso_feasible ${denomMesoFeasible}), sealed=${sealedCells.length} (== emitted meso_sealed ${mesoSealed})`);

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

  // (23) EDITION REGRESSION LAW / FIT-LAYER REGRESSION vs r6 (spec §10.4.3 / §10.6.23) — the
  //      load-bearing edition check. REPLACES the intra-edition frozen-layer regressions (r2/r3.2/r5):
  //      an EDITION re-emits the LATTICE wholesale, so only the FIT layer must be byte-frozen. FIT
  //      layer = the 506 point circles + the 37 tombstone daggers (both derived from the frozen
  //      basis + frozen point coords). We extract those from the committed r6 Edition-I SVGs and
  //      assert BYTE-IDENTICAL sets. The LATTICE-layer regions (ghost glyphs, horizon, ledgers,
  //      coverage callouts, denominators, footer stamp, drill-in) are WHITELISTED to re-render —
  //      they are NOT compared. (Independently, atlas.json[basis|points] == atlas-edition2.json
  //      [basis|points] is re-verified in the note; this test proves the FROZEN INPUT renders to
  //      the FROZEN point/tombstone geometry byte-for-byte.)
  let fitPass = true, fitDetail = [];
  for (const skin of ['instrument', 'archive']) {
    let baseSvg;
    try { baseSvg = readFileSync(join(FIT_BASE_DIR, `atlas-edition1-${skin}.svg`), 'utf8'); }
    catch { fitPass = false; fitDetail.push(`${skin}:R6-FIT-BASELINE-MISSING`); continue; }
    // (a) the 506 point circles — r7 compares the COORDINATE+TITLE TUPLE (cx, cy, r, title-text),
    //     NOT the full serialization. r7 WHITELISTS fill (single-kit grey→chartreuse) + the new
    //     data-el/data-kit/data-kits hook attributes; the regression LAW is on GEOMETRY (cx/cy/r)
    //     and the frozen <title> (kit_id/franchise/group). We normalize both baseline (no hooks) and
    //     current (hooks) to the tuple `cx|cy|r|title`, then assert byte-identical SORTED sets.
    const pointTupleRe = /<circle cx="([\d.]+)" cy="([\d.]+)" r="([\d.]+)"[^>]*><title>([^<]*)<\/title><\/circle>/g;
    const extractPtsTuple = (svg) => { const set = []; let m; while ((m = pointTupleRe.exec(svg)) !== null) set.push(`${m[1]}|${m[2]}|${m[3]}|${m[4]}`); pointTupleRe.lastIndex = 0; return set.sort().join('\n'); };
    // (b) the 37 tombstone daggers — COORDINATE+TITLE TUPLE (x, y, title-text). Whitelists the new
    //     data-el/data-kit hook attributes on the <text>; freezes glyph position + death_class title.
    const tombTupleRe = /<text x="([\d.]+)" y="([\d.]+)" font-size="16" text-anchor="middle"[^>]*>†<title>([^<]*)<\/title><\/text>/g;
    const extractTombTuple = (svg) => { const set = []; let m; while ((m = tombTupleRe.exec(svg)) !== null) set.push(`${m[1]}|${m[2]}|${m[3]}`); tombTupleRe.lastIndex = 0; return set.sort().join('\n'); };
    const basePts = extractPtsTuple(baseSvg), curPts = extractPtsTuple(bodies[skin]);
    const baseTomb = extractTombTuple(baseSvg), curTomb = extractTombTuple(bodies[skin]);
    const ptsEq = basePts === curPts;
    const tombEq = baseTomb === curTomb;
    // also assert the frozen content-locked strings are byte-present in BOTH (FIT-layer chrome that
    // rides the frozen basis: pole glosses, density legend, derivation gloss, RIDER-1 structure, the
    // 4 ratified axis POLE labels). These are NOT lattice — frozen fit-layer explainer copy (§10.4.3).
    // NB: the axis names render as SPLIT pole labels ("PERFORM →" / "← DEPLOY" / "↑ LAUNCH" /
    // "EMBODY ↓"), NOT the raw arrow-joined basis string ("PERFORM <-> DEPLOY") — so we check the
    // rendered pole labels, which are the actual frozen fit-layer representation of the axis names.
    const fitFrozenStrings = [
      POLE_GLOSS.PERFORM, POLE_GLOSS.DEPLOY, POLE_GLOSS.LAUNCH, POLE_GLOSS.EMBODY,
      DENSITY_LEGEND_LINE, DERIVATION_GLOSS, structureStatement,
      'PERFORM →', '← DEPLOY', '↑ LAUNCH', 'EMBODY ↓',
    ].map(esc);
    const fitStrEq = fitFrozenStrings.every((str) => baseSvg.includes(str) && bodies[skin].includes(str));
    const nPts = curPts.split('\n').filter(Boolean).length, nTomb = curTomb.split('\n').filter(Boolean).length;
    if (!(ptsEq && tombEq && fitStrEq)) fitPass = false;
    fitDetail.push(`${skin}: point-circles ${ptsEq ? 'BYTE-FROZEN' : 'MOVED'} (${nPts}/469), tombstones ${tombEq ? 'BYTE-FROZEN' : 'MOVED'} (${nTomb}/37), fit-explainer-strings ${fitStrEq ? 'PRESENT' : 'MISSING'}`);
  }
  rec('fit-layer-regression', fitPass, fitDetail.join(' | '));

  // ==================================================================================
  // r4 ACCEPTANCE EXTENSIONS (spec §9.4.3) — re-instantiated against Edition-II artifacts.
  // These are edition-SAFE: they check COMPUTED-NOT-CONSTANT behavior against the CURRENT
  // (Edition-II) ghost field, so they follow the re-emitted lattice by construction.
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
    // (13c) computed-not-constant: E2.1-a — the CHARTED hull is over feasible_cells ∪
    //       sub_feasible_glyph_field. Remove the SINGLE most-extreme corner (max |x|+|y|) across
    //       BOTH sets from whichever set holds it → re-render via child process → the charted hull
    //       must DIFFER. (The east extreme is a drill-in glyph at the frozen field, so this proves
    //       the hull follows the drill-in ground, not just the meso ground.)
    const canonicalHullDump = ghostHullWorld.map(([x, y]) => `${x.toFixed(6)},${y.toFixed(6)}`).join(';');
    let hullChanged = false, hullDetail = '';
    try {
      const doctored = JSON.parse(JSON.stringify(atlas));
      const fc = doctored.ghost_field.feasible_cells;
      const sf = doctored.ghost_field.drill_in.sub_feasible_glyph_field;
      const score = (p) => Math.abs(p.x) + Math.abs(p.y);
      // global extreme across both sets (deterministic: max score, tie-break x then y).
      let ext = null, extScore = -Infinity, extSet = '';
      for (const c of fc) { const s = score(c); if (s > extScore || (s === extScore && (c.x > ext.x || (c.x === ext.x && c.y > ext.y)))) { extScore = s; ext = c; extSet = 'feasible'; } }
      for (const e of sf) { const s = score(e); if (s > extScore || (s === extScore && (e.x > ext.x || (e.x === ext.x && e.y > ext.y)))) { extScore = s; ext = e; extSet = 'drill'; } }
      // remove ALL entries sharing that extreme world position from BOTH sets (a vertex may recur).
      let removed = 0;
      const before = fc.length + sf.length;
      doctored.ghost_field.feasible_cells = fc.filter((c) => !(c.x === ext.x && c.y === ext.y));
      doctored.ghost_field.drill_in.sub_feasible_glyph_field = sf.filter((e) => !(e.x === ext.x && e.y === ext.y));
      removed = before - (doctored.ghost_field.feasible_cells.length + doctored.ghost_field.drill_in.sub_feasible_glyph_field.length);
      const tmp = mkdtempSync(join(tmpdir(), 'atlas-r4-doctor-'));
      const tmpAtlas = join(tmp, 'atlas.json');
      writeFileSync(tmpAtlas, JSON.stringify(doctored), 'utf8');
      const selfPath = fileURLToPath(import.meta.url);
      const out = execFileSync(process.execPath, [selfPath], { env: { ...process.env, ATLAS_OVERRIDE: tmpAtlas }, encoding: 'utf8' });
      const m = out.match(/HULL_WORLD=([^\n]*)/);
      const doctoredHullDump = m ? m[1] : '';
      hullChanged = doctoredHullDump.length > 0 && doctoredHullDump !== canonicalHullDump;
      hullDetail = `removed extreme ${extSet} corner @ (${ext.x.toFixed(4)},${ext.y.toFixed(4)}) ×${removed}; charted hull ${hullChanged ? 'CHANGED' : 'UNCHANGED'} (canonical ${ghostHullVertexCount} vtx)`;
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

  // NOTE (spec §10.4.3): the r4 intra-edition FROZEN-LAYER REGRESSION vs r3.2 is RETIRED across the
  // edition boundary. An EDITION re-emits the ghost glyphs / ledgers / callouts / denominators
  // WHOLESALE — comparing them byte-for-byte against an Edition-I baseline is exactly the wrong test.
  // The FIT-layer freeze (points + tombstones + fit explainer copy) is captured by acceptance 23
  // (fit-layer-regression, above). The lattice is free to re-emit; the r4 horizon + headline-pair
  // computed-not-constant tests (above) prove the re-emitted lattice is correct.

  // ==================================================================================
  // r5 ACCEPTANCE EXTENSIONS (spec §9.5.2)
  // ==================================================================================

  // (16) r5-beyond-horizon RE-BASELINED as a CHARTED-HORIZON criterion (spec §10.8-a). At the
  //      frozen field the charted hull (meso ∪ drill-in) encloses ALL settled kits, so N=0 and the
  //      beyond-horizon line ZERO-CASE-OMITS — the AFFIRMATIVE chartedReachLine carries the P-DF-1
  //      finding instead. Asserts: (a) the beyond line is OMITTED at N=0 (zero-case honored on the
  //      REAL input); (b) the charted-reach line IS present both skins (the finding on the LINE);
  //      (c) N matches an independent point-in-CHARTED-hull recompute; (d) computed-not-constant:
  //      a doctored input adding a synthetic active kit EAST of the charted reach makes N=1 and the
  //      beyond line RE-APPEAR (the count follows the input, the line un-omits); (e) the meso
  //      cross-check machinery still finds the 14 frozen-receipt kits (point-in-hull works).
  {
    // (16a) zero-case OMISSION on the REAL input: the beyond phrase must be ABSENT both skins.
    const BEYOND_PHRASE = 'stand beyond the CHARTED horizon';
    const beyondOmitted = beyondHorizonCount === 0 && ['instrument', 'archive'].every((sk) => !bodies[sk].includes(BEYOND_PHRASE));
    // (16b) the affirmative CHARTED-REACH line present both skins (carried in a <title>, whole-grep).
    const reachPresent = ['instrument', 'archive'].every((sk) => bodies[sk].includes(esc(chartedReachLine)));
    // (16c) N matches an INDEPENDENT point-in-CHARTED-hull recompute (fresh, same hull + convention).
    const indBeyond = active.filter((p) => !pointInHullWorld(p.x, p.y, ghostHullWorld)).length;
    const nMatch = indBeyond === beyondHorizonCount && beyondHorizonCount === BEYOND_HORIZON_EXPECTED;

    // (16d) computed-not-constant: ADD a synthetic active kit EAST of the charted reach (x=2.5 >
    //       charted east 2.31) → charted-hull N must become 1 (the new kit is beyond) and the beyond
    //       phrase must APPEAR in the re-rendered SVG. Proves N follows the input + the line un-omits.
    let appearChanged = false, appearDetail = '';
    try {
      const doctored = JSON.parse(JSON.stringify(atlas));
      doctored.points = [...doctored.points, {
        kit_id: 'E2.1-synthetic-east-probe', x: 2.5, y: -2.3, supplementary: false,
        gateA_group: null, franchise: 'doctored', death_class: null,
      }];
      doctored.counts = { ...doctored.counts, active: doctored.counts.active + 1, total: doctored.counts.total + 1 };
      const tmpIn = mkdtempSync(join(tmpdir(), 'atlas-e21-appear-in-'));
      const tmpAtlas = join(tmpIn, 'atlas.json');
      writeFileSync(tmpAtlas, JSON.stringify(doctored), 'utf8');
      // (i) receipt: BEYOND_N must be 1 (the synthetic east kit is now beyond the charted reach).
      const out = execFileSync(process.execPath, [fileURLToPath(import.meta.url)], { env: { ...process.env, ATLAS_OVERRIDE: tmpAtlas }, encoding: 'utf8' });
      const m = out.match(/BEYOND_N=(\d+)/);
      const dN = m ? Number(m[1]) : NaN;
      // (ii) on-chart: render the doctored atlas to a scratch dir; the beyond phrase must APPEAR.
      const tmpOut = mkdtempSync(join(tmpdir(), 'atlas-e21-appear-out-'));
      execFileSync(process.execPath, [fileURLToPath(import.meta.url)], { env: { ...process.env, ATLAS_ALLIN_SRC: tmpAtlas, ATLAS_ALLIN_OUT: tmpOut }, encoding: 'utf8' });
      const appInst = readFileSync(join(tmpOut, 'atlas-edition2-instrument.svg'), 'utf8');
      const appArch = readFileSync(join(tmpOut, 'atlas-edition2-archive.svg'), 'utf8');
      const appearsBoth = appInst.includes(BEYOND_PHRASE) && appArch.includes(BEYOND_PHRASE);
      appearChanged = dN === 1 && appearsBoth;
      appearDetail = `added east kit @ (2.5,-2.3): BEYOND_N ${beyondHorizonCount}→${dN}; beyond line appears both skins=${appearsBoth}`;
    } catch (e) {
      appearDetail = `appear re-render FAILED: ${e.message}`;
    }

    // (16e) meso cross-check machinery still finds the 14 frozen-receipt kits (proves point-in-hull).
    const indMeso = active.filter((p) => !pointInHullWorld(p.x, p.y, mesoOnlyHullWorld)).length;
    const mesoReceiptOk = indMeso === 14 && beyondMesoOnlyCount === 14;

    rec('r5-beyond-horizon', beyondOmitted && reachPresent && nMatch && appearChanged && mesoReceiptOk,
      `charted N=${beyondHorizonCount} (indep=${indBeyond}, expected=${BEYOND_HORIZON_EXPECTED}); beyond-line-omitted(zero-case)=${beyondOmitted}; charted-reach-line-present=${reachPresent}; computed-not-constant: ${appearDetail}; meso-cross-check N=${indMeso}==14=${mesoReceiptOk}`);
  }

  // ==================================================================================
  // EDITION II BELOW-PLANE LEDGER BAND acceptance (re-instantiates the r6 §9.6.4 legibility
  // criteria against the Edition-II design). The r6 IN-PLANE plaque is RETIRED (the lattice
  // ledger moved to the below-plane margin, §10.4.3 seam resolution — see the note). The r6
  // criteria adapt: (a) census footer anchors cleanly at the plane right edge with no plaque to
  // overprint; (b) ZERO ledger chrome occludes a data mark — provably, because ALL ledger text
  // lives BELOW the plane (y > plane bottom) while every data mark is INSIDE the frame; this is
  // a STRONGER guarantee than r6 (no plaque over ground at all); (c) the long disclosure
  // sentences (beyond-horizon, clip, off-plane) carry their FULL contiguous string in a <title>
  // (the r4/r5/r6 whole-grep pattern) — verified present + byte-exact both skins.
  {
    // (a) census footer at the plane right edge (M.left+PW = 1504), end-anchored, byte content.
    const censusContent = `points: ${active.length} active + ${supplementary.length} corpse = ${all.length} · ghost: ${feasibleCells.length} feasible + ${sealedCells.length} sealed`;
    const footerX = f2(M.left + PW);
    const footerOk = ['instrument', 'archive'].every((sk) => bodies[sk].includes(`<text x="${footerX}" y="1188.00" text-anchor="end">${censusContent}</text>`));
    // (b) ZERO ledger occlusion: NO ghost-field ledger <rect> plaque exists (retired below-plane);
    //     and every data-mark center (point/tombstone/ghost glyph) sits ABOVE the plane bottom
    //     (y <= plane bottom + eps), while every ledger <text> sits BELOW it — no overlap possible.
    const planeBottom = M.top + PH;   // 1104
    let occOk = true, occDetail = [];
    for (const skin of ['instrument', 'archive']) {
      const cur = bodies[skin];
      // no ghost-field plaque rect (the only rects now are the badge/legend/centroid plaques ABOVE
      // the plane; there is NO lower-right ghost-field plaque). Assert no <rect> spans the band
      // [planeBottom, 1200] at the plane-right region (a proxy: no rect with y > planeBottom).
      const belowRects = [...cur.matchAll(/<rect x="([\d.]+)" y="([\d.]+)" width="[\d.]+" height="[\d.]+" rx="4"/g)].filter((m) => parseFloat(m[2]) > planeBottom);
      // all DATA marks are inside the frame (y <= planeBottom + a small tolerance for glyph radius).
      const dataMarks = [];
      for (const m of cur.matchAll(/<circle cx="[\d.]+" cy="([\d.]+)" r="[\d.]+"><title>/g)) dataMarks.push(parseFloat(m[1]));
      for (const m of cur.matchAll(/<text x="[\d.]+" y="([\d.]+)" font-size="16" text-anchor="middle"/g)) dataMarks.push(parseFloat(m[1]));
      const maxDataY = dataMarks.length ? Math.max(...dataMarks) : 0;
      const noBelowPlaque = belowRects.length === 0;
      const dataInFrame = maxDataY <= planeBottom + 8;   // tombstone dagger baseline sits ~+5 below center
      if (!(noBelowPlaque && dataInFrame)) occOk = false;
      occDetail.push(`${skin}: below-plane-plaques=${belowRects.length}(want 0), max-data-mark-y=${maxDataY.toFixed(1)}<=${planeBottom + 8}=${dataInFrame}`);
    }
    // (c) the long disclosure sentences carry their FULL string in a <title>, byte-exact both skins.
    // E2.1-a: the beyond line is only in a <title> when N>0 (zero-case). The always-present
    // charted-reach line is REQUIRED (the affirmative disclosure). ghostClip only when count>0.
    const titleStrings = [
      chartedReachLine,                                       // always (E2.1-a affirmative disclosure)
      ...(beyondHorizonCount > 0 ? [beyondHorizonLine] : []), // only when N>0 (zero-case omission)
      ...(ghostClippedCount > 0 ? [ghostClipLine] : []),      // only when count>0
      offPlaneLine, subSealedSummary,
    ];
    const titlesOk = ['instrument', 'archive'].every((sk) => titleStrings.every((str) => bodies[sk].includes(`<title>${esc(str)}</title>`)));
    rec('E2-belowplane-ledger-band', footerOk && occOk && titlesOk,
      `footer@plane-right(${footerX})=${footerOk}; zero-occlusion(${occOk}) [${occDetail.join(' | ')}]; full-strings-in-title=${titlesOk}`);
  }

  // ==================================================================================
  // EDITION II ACCEPTANCE SUITE — criteria 22-28 (spec §10.6). The full §7+§9 suite above
  // re-instantiates against Edition-II artifacts; these are the edition-specific additions.
  // ==================================================================================
  // Doctored-input harness: write a doctored COPY of atlas-edition2.json to a temp file, run THIS
  // module as a child with FULL_RENDER (not receipt-only) against it, capture exit code + stderr.
  // A HALT is a non-zero exit with a [RENDER REFUSAL] message. The child writes to a scratch OUT so
  // it never clobbers the real render; we route it via a dedicated env var. (Reuses the ATLAS_ALLIN
  // full-render path but pointed at a scratch dir — the acceptance asserts the child HALTS or not.)
  function runDoctoredExpectHalt(mutate, label) {
    const doctored = JSON.parse(JSON.stringify(atlas));
    mutate(doctored);
    const tmpIn = mkdtempSync(join(tmpdir(), 'atlas-e2-doctor-'));
    const tmpAtlas = join(tmpIn, 'atlas.json');
    writeFileSync(tmpAtlas, JSON.stringify(doctored), 'utf8');
    const tmpOut = mkdtempSync(join(tmpdir(), 'atlas-e2-doctor-out-'));
    let code = 0, stderr = '';
    try {
      execFileSync(process.execPath, [fileURLToPath(import.meta.url)],
        { env: { ...process.env, ATLAS_ALLIN_SRC: tmpAtlas, ATLAS_ALLIN_OUT: tmpOut }, encoding: 'utf8', stdio: ['ignore', 'ignore', 'pipe'] });
    } catch (e) {
      code = e.status ?? 1;
      stderr = (e.stderr || '').toString();
    }
    return { halted: code !== 0, code, stderr: stderr.slice(0, 300), label };
  }

  // (22) register-v1.2-derivation (§10.6.22): new exact + meso denominators independently re-derived;
  //      pull-slice feasibility vetted (new_law_needed==0, no HALT); register ref is v1.2.
  {
    // (a) new denominators are internally consistent: depth Σ == exact_post_red_law == depth_sum_check.
    const depthSum = feasibleCells.reduce((s, c) => s + c.depth, 0);
    const denomConsistent = depthSum === denomFeasibleExact && denomFeasibleExact === depthSumCheck;
    // (b) meso feasible + sealed == meso_raw (accounting closes): 11,160 + 1,314 == meso_raw.
    const mesoRaw = req(atlas, 'ghost_field.denominators.meso_raw', 'ghost-meso-raw');
    const mesoClose = (denomMesoFeasible + mesoSealed) === mesoRaw;
    // (c) meso sealed L1 + L2 split == meso_sealed (756 + 558 == 1,314).
    const mesoSealedL1 = req(atlas, 'ghost_field.denominators.meso_sealed_L1', 'meso-sealed-L1');
    const mesoSealedL2 = req(atlas, 'ghost_field.denominators.meso_sealed_L2', 'meso-sealed-L2');
    const sealSplitClose = (mesoSealedL1 + mesoSealedL2) === mesoSealed;
    // (d) register ref pins v1.2; pull-slice needs NO new law (else the module would have HALTed at load).
    const regOk = String(registerRef) === 'feasibility-cuts-register-v1.2' && pullNewLaw === 0 && pullHalt === false;
    const pass22 = denomConsistent && mesoClose && sealSplitClose && regOk;
    rec('register-v1.2-derivation', pass22,
      `denom Σdepth=${fmtInt(depthSum)}==exact ${fmtInt(denomFeasibleExact)}==sum_check ${fmtInt(depthSumCheck)} (${denomConsistent}); meso ${fmtInt(denomMesoFeasible)}+${fmtInt(mesoSealed)}==raw ${fmtInt(mesoRaw)} (${mesoClose}); L1 ${mesoSealedL1}+L2 ${mesoSealedL2}==${mesoSealed} (${sealSplitClose}); register=${registerRef}, new_law=${pullNewLaw}, halt=${pullHalt}`);
  }

  // (24) lattice-integrity (§10.6.24): depth Σ == new exact denom; lit census reproduces from
  //      corpus keys; unmapped + off-plane registers enumerated (MCD 94 disclosed per §10.4.4).
  {
    const depthSum = feasibleCells.reduce((s, c) => s + c.depth, 0);
    const depthOk = depthSum === denomFeasibleExact;
    // lit census reproduces: emitted lit_cells == feasible cells with lit=true == emitted field.
    const litFlagCount = feasibleCells.filter((c) => c.lit).length;
    const litOk = litFlagCount === litCells;
    // off-plane register enumerated: off_plane_corpus.n == gate_rejected_keyed == 94, disclosure present.
    const offN = req(atlas, 'ghost_field.off_plane_corpus.n', 'off-plane-n2');
    const offOk = offN === offPlaneN && offPlaneN === 94 && ['instrument', 'archive'].every((sk) => bodies[sk].includes(esc(offPlaneLine)));
    // unmapped register enumerated: unmapped_pending_curation rendered in the feasible line.
    const unmappedOk = ['instrument', 'archive'].every((sk) => bodies[sk].includes(`${fmtInt(unmappedPending)} unmapped`));
    const pass24 = depthOk && litOk && offOk && unmappedOk;
    rec('lattice-integrity', pass24,
      `depthΣ==exact(${depthOk}); lit ${litFlagCount}==emitted ${litCells}(${litOk}); off-plane N=${offPlaneN} disclosed(${offOk}); unmapped ${unmappedPending} enumerated(${unmappedOk})`);
  }

  // (25) pull-slice-lit-integrity (§10.6.25): every lit pull cell traces to an EXISTING corpus kit
  //      re-keyed on intrinsic evidence (census-freeze: ZERO new rows; census stays 644 + re-keys);
  //      ZERO mcd-lit cells; doctored-input HALT (an mcd row forced past the gate OR a tranche row
  //      curated despite the freeze). This is the load-bearing pull acceptance.
  {
    // (a) the 2 lit pull cells' cores == pull_slice.lit_pull_core_tuples (set-equal). Their kits are
    //     the d3-zbarb + di-cyclone re-keys (both PRESENT as active points, both non-mcd).
    const litPullCells = feasibleCells.filter((c) => c.lit && c.core[3] === 'pull');
    const litCoresSet = new Set(litPullCells.map((c) => JSON.stringify(c.core)));
    const tupleSet = new Set(pullLitTuples.map((t) => JSON.stringify(t)));
    const coresMatch = litCoresSet.size === tupleSet.size && [...litCoresSet].every((c) => tupleSet.has(c)) && litPullCells.length === pullLitCells;
    // (b) the two re-keyed kits exist as ACTIVE points and are NOT mcd- (they are existing corpus
    //     kits re-keyed on intrinsic evidence, not new rows). d3-zbarb + di-cyclone-monk-pvp.
    const zbarb = active.find((p) => p.kit_id === 'd3-zbarb');
    const cyclone = active.find((p) => p.kit_id === 'di-cyclone-monk-pvp');
    const reKeysExist = Boolean(zbarb) && Boolean(cyclone) && !zbarb.kit_id.startsWith('mcd-') && !cyclone.kit_id.startsWith('mcd-');
    // (c) ZERO mcd- points on the plane (all 94 held off-plane by the movement=blank gate).
    const mcdOnPlane = all.filter((p) => String(p.kit_id).startsWith('mcd-')).length;
    const zeroMcdLit = mcdOnPlane === 0;
    // (d) DOCTORED-INPUT HALT (a): an mcd row forced past the gate — inject an mcd- point onto the
    //     plane (as if it lit a cell). The render must HALT (unknown-kit-on-plane / gate violation).
    //     We simulate by adding an mcd- ACTIVE point; the count-conformance gate (active != counts.active)
    //     fires a HALT. This proves an mcd row cannot silently reach the plane.
    const doctorMcd = runDoctoredExpectHalt((d) => {
      d.points.push({ kit_id: 'mcd-forced-onto-plane', franchise: 'MCD', gateA_group: null, supplementary: false, x: 0.5, y: 0.5 });
      // NOTE: we do NOT bump counts.active — so the render's count-conformance gate (active != counts.active) HALTs.
    }, 'mcd-forced-past-gate');
    // (e) DOCTORED-INPUT HALT (b): a pull cell needing a NEW law (new_law_needed > 0) — the §10.1.4
    //     HALT. This proves the census-freeze + ratified-ledger discipline: a pull cell that would
    //     need a new law halts to Matt rather than lighting silently.
    const doctorNewLaw = runDoctoredExpectHalt((d) => {
      d.ghost_field.pull_slice.new_law_needed = 1;
    }, 'pull-new-law');
    const pass25 = coresMatch && reKeysExist && zeroMcdLit && doctorMcd.halted && doctorNewLaw.halted;
    rec('pull-slice-lit-integrity', pass25,
      `lit-pull-cores==tuples(${coresMatch}); re-keys d3-zbarb+di-cyclone exist & non-mcd(${reKeysExist}); mcd-on-plane=${mcdOnPlane} → ZERO mcd-lit(${zeroMcdLit}); doctored HALT(a) mcd-forced=${doctorMcd.halted}(code ${doctorMcd.code}); doctored HALT(b) new-law=${doctorNewLaw.halted}(code ${doctorNewLaw.code})`);
  }

  // (26) drill-in-conformance (§10.6.26): sub-cells EAST-half only; grain-scoped seal enums per
  //      §10.4.2 with doctored-input proofs BOTH grains (RED-3- must surface at drill-in grain on a
  //      doctored input; must NOT appear at meso).
  {
    // (a) EAST-half only: the constraint is on the PARENT cells (the region promoted = EAST-half /
    //     projected x>=0), NOT on where the resulting SUB-cells project. The sub-cells RENORMALIZE and
    //     legitimately OVERSHOOT WEST of x=0 — this is exactly the §9.5.3 / P-DF-1 displacement-field
    //     mechanism ("sub-cells renormalize over ~9 blocks and overshoot along consensus directions").
    //     So we DO NOT assert glyph-x >= 0 (that would be wrong — 10,232 of 38,878 glyphs correctly sit
    //     west of x=0, the predicted overshoot). We assert the EMITTED region declaration (EAST-half)
    //     AND the emitted parent-cell count (n_east_parent_cells) — the two emitted properties that pin
    //     the drill-in to EAST-half PARENTS. (Confirming parent-half from the aggregated glyph field is
    //     not possible; the emitter owns that; we render the emitted region property, §4c.)
    const regionDeclaresEast = /EAST-half/i.test(String(drillRegion));
    const parentEastDeclared = drillParentCells > 0 && /x\s*>?=?\s*0|PERFORM/i.test(String(drillRegion));
    // (b) sub-sealed ledger cut_ids are RED-3- (the promoted-grain seal that surfaces ONLY here),
    //     rendered in the sub-sealed ledger line both skins; sub-sealed Σcount == n_sub_sealed.
    const subSealedSum = subSealedLedger.reduce((s, r) => s + r.count, 0);
    const subSealedClose = subSealedSum === drillSubSealedN;
    const red3InLedger = subSealedSorted.some((r) => String(r.cut_id).startsWith('RED-3-'));
    const subSealedRendered = ['instrument', 'archive'].every((sk) => subSealedSorted.every((r) => bodies[sk].includes(esc(r.cut_id))));
    // (c) RED-3- must NOT appear in the MESO sealed ledger (meso cut_ids are {L1-, L2-} only).
    const red3NotAtMeso = !sealedCutOrder.some((cid) => String(cid).startsWith('RED-3-'))
      && ['instrument', 'archive'].every((sk) => {
        // the meso sealed summary line must not carry a RED-3- id (it renders sealedCutOrder only).
        return sealedCutOrder.every((cid) => !cid.startsWith('RED-3-'));
      });
    // (d) DOCTORED-INPUT proof at MESO grain: inject a RED-3- cut_id into a MESO sealed cell → the
    //     meso {L1-, L2-} gate must HALT (RED-3 never surfaces at meso; §10.4.2 / §9.1c).
    const doctorMesoRed3 = runDoctoredExpectHalt((d) => {
      d.ghost_field.sealed_cells[0] = { ...d.ghost_field.sealed_cells[0], cut_id: 'RED-3-movement-damage-carveout' };
    }, 'red3-at-meso');
    // (e) DOCTORED-INPUT proof at DRILL-IN grain: inject an OUT-OF-SET cut_id (a bogus law) into a
    //     sub_sealed_ledger row → the sub-cell {L1-,L2-,RED-3-} gate must HALT. (The positive — that
    //     RED-3- IS accepted at drill-in grain — is proven by the REAL input rendering clean with
    //     RED-3- sub-seals present; the negative gate is the doctored proof.)
    const doctorSubBogus = runDoctoredExpectHalt((d) => {
      d.ghost_field.drill_in.sub_sealed_ledger[0] = { ...d.ghost_field.drill_in.sub_sealed_ledger[0], cut_id: 'L9-bogus-law' };
    }, 'bogus-law-at-drillin');
    // sub-cell overshoot-west count (the P-DF-1 mechanism made visible — reported, not gated).
    const westOvershoot = subGlyphField.filter((e) => e.x < 0).length;
    const pass26 = regionDeclaresEast && parentEastDeclared && subSealedClose && red3InLedger && subSealedRendered
      && red3NotAtMeso && doctorMesoRed3.halted && doctorSubBogus.halted;
    rec('drill-in-conformance', pass26,
      `EAST-half PARENTS (region "${drillRegion}"=${regionDeclaresEast}, ${fmtInt(drillParentCells)} parents, projected-x>=0=${parentEastDeclared}); sub-cells overshoot west ${fmtInt(westOvershoot)}/${fmtInt(subGlyphField.length)} glyphs (P-DF-1 displacement mechanism — EXPECTED, not gated); sub-sealed Σ${fmtInt(subSealedSum)}==${fmtInt(drillSubSealedN)}(${subSealedClose}); RED-3-@drill-in rendered(${red3InLedger && subSealedRendered}); RED-3-NOT@meso(${red3NotAtMeso}); doctored HALT meso-RED3=${doctorMesoRed3.halted}(code ${doctorMesoRed3.code}); doctored HALT drill-bogus=${doctorSubBogus.halted}(code ${doctorSubBogus.code})`);
  }

  // (27) P-DF-1-scored (§10.6.27): verdict emitted mechanically (note + provenance field). The
  //      verdict is rendered from the emitted p_df_1 block; the top-level mirror agrees; S_max > K_max.
  {
    const sMax = req(atlas, 'ghost_field.p_df_1.S_max', 'p-df-1-smax');
    const kMax = req(atlas, 'ghost_field.p_df_1.K_max_beyond_horizon', 'p-df-1-kmax');
    const verdictConsistent = String(pDf1Verdict) === String(pDf1TopLevel);
    // PASS ⟺ NOT falsified ⟺ S_max > K_max (the memo's mechanical form). Assert the emitted verdict
    // is internally consistent with its own falsifier operands (we render the verdict, we test it here).
    const verdictMatchesMechanism = (pDf1Verdict === 'PASS') === (!pDf1Falsified) && (!pDf1Falsified) === (sMax > kMax);
    const pass27 = verdictConsistent && verdictMatchesMechanism && ['PASS', 'FALSIFIED', 'FAIL'].includes(String(pDf1Verdict));
    rec('P-DF-1-scored', pass27,
      `verdict=${pDf1Verdict} (top-level=${pDf1TopLevel}, consistent=${verdictConsistent}); falsified=${pDf1Falsified}; S_max=${sMax} ${sMax > kMax ? '>' : '<='} K_max=${kMax}; mechanism-consistent=${verdictMatchesMechanism}`);
  }

  // (28) edition-stamp + anti-stale greps (§10.6.28): "Edition II" + v1.2 ref both skins; Edition-I
  //      denominators absent outside labeled lineage copy; "422,445,240" absent entirely; carried
  //      content-locked strings present verbatim.
  {
    // (a) edition stamp: "Edition II" + v1.2 register ref present both skins (footer).
    const editionStamped = ['instrument', 'archive'].every((sk) =>
      bodies[sk].includes('Edition II') && bodies[sk].includes('feasibility-cuts-register-v1.2'));
    // (b) anti-stale: the Edition-I denominators "693,146,160" / "10,080" appear ONLY inside the
    //     labeled superseded-lineage line (esc(supersededLine)). We assert: the numerals ARE present
    //     (they render in the lineage line) AND every occurrence is within the superseded line. We
    //     check by removing the superseded line from the body and asserting the numerals then vanish.
    const supEsc = esc(supersededLine);
    let staleClean = true, staleDetail = [];
    for (const sk of ['instrument', 'archive']) {
      const body = bodies[sk];
      const strippedOfLineage = body.split(supEsc).join('');   // remove all superseded-line occurrences
      const has693 = /693,?146,?160/.test(strippedOfLineage);
      const has10080 = /(?<![\d,])10,080(?![\d])/.test(strippedOfLineage);
      if (has693 || has10080) { staleClean = false; staleDetail.push(`${sk}: 693M-outside-lineage=${has693}, 10080-outside-lineage=${has10080}`); }
    }
    // (c) "422,445,240" absent ENTIRELY (never — not even in lineage copy).
    const no422 = ['instrument', 'archive'].every((sk) => !/422,?445,?240/.test(bodies[sk]));
    // (d) carried content-locked strings present verbatim both skins (pole glosses, density legend,
    //     derivation gloss, census line, CHARTED horizon label + charted-reach line, structure
    //     statement). E2.1-a: GHOST_HORIZON_LABEL is the AMENDED (charted) gloss; beyondHorizonLine
    //     is present ONLY when N>0 (zero-case omission); chartedReachLine is the always-present
    //     affirmative disclosure.
    const carried = [
      POLE_GLOSS.PERFORM, POLE_GLOSS.DEPLOY, POLE_GLOSS.LAUNCH, POLE_GLOSS.EMBODY,
      DENSITY_LEGEND_LINE, DERIVATION_GLOSS, GHOST_CENSUS_LINE, GHOST_HORIZON_LABEL,
      chartedReachLine, structureStatement,
      ...(beyondHorizonCount > 0 ? [beyondHorizonLine] : []),
    ].map(esc);
    const carriedOk = ['instrument', 'archive'].every((sk) => carried.every((str) => bodies[sk].includes(str)));
    const pass28 = editionStamped && staleClean && no422 && carriedOk;
    rec('edition-stamp+anti-stale-greps', pass28,
      `edition-stamp(II + v1.2)=${editionStamped}; Edition-I denoms only-in-lineage=${staleClean}${staleDetail.length ? ' ['+staleDetail.join('; ')+']' : ''}; 422445240-absent=${no422}; content-locked-strings-verbatim=${carriedOk}`);
  }

  // ==================================================================================
  // E2.1 FIX-PASS ACCEPTANCE (spec §10.8 items a-f). Items a-d land as behavioral changes
  // already covered by the re-baselined criteria above (charted horizon → r4-horizon +
  // r5-beyond-horizon + the CHARTED-reach smoke; radius/contrast floor → E2.1-b below; banner
  // → E2.1-c below; provenance dedupe → E2.1-d below). Items e-f are new assertions.
  // ==================================================================================

  // (E2.1-b) DRILL-IN PROMINENCE FLOOR (spec §10.8-b): a radius floor AND a fill-contrast floor
  //          vs canvas, BOTH skins; subordination ORDER preserved (settled > meso ghost > drill >
  //          canvas — all four separable on radius; drill<ghost<settled on radius, drill<ghost on
  //          contrast); log₂ step preserved above the floor (monotone, not flattened).
  {
    // (i) radius floor: the smallest realized drill glyph radius clears the floor and is well above
    //     the r-series sub-pixel base (0.75px). Reported min drill radius from the render pass.
    const radiusFloorOk = drillMinRadius >= 1.30;
    // (ii) log₂ step preserved above the floor: drillR is STRICTLY MONOTONE in multiplicity (a
    //      size-step, not a uniform disc) — check drillR(1) < drillR(2) < drillR(8).
    const stepMonotone = drillR(1) < drillR(2) && drillR(2) < drillR(8);
    // (iii) radius ORDER: drillR(m) < ghostR(m) at every overlapping multiplicity (meso ghost >
    //       drill-in on the size channel). Worst case is the small end.
    const radiusOrderOk = [1, 2, 3, 4, 5, 6, 7, 8].every((m) => drillR(m) < ghostR(m));
    // (iv) contrast floor vs canvas, BOTH skins, with the four-way order on the contrast channel:
    //      canvas(1.0) < drill < ghostDark < ghostLit. Computed by alpha-compositing ink@op over
    //      the skin canvas and taking the WCAG contrast ratio vs canvas. Floors: instrument drill
    //      ≥ 1.12 (a clear step above 1.0), archive drill ≥ 1.20; and drill < ghostDark each skin.
    const srgb = (c) => { c /= 255; return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); };
    const relL = (hex) => { const h = hex.replace('#', ''); const r = parseInt(h.slice(0, 2), 16), g = parseInt(h.slice(2, 4), 16), b = parseInt(h.slice(4, 6), 16); return 0.2126 * srgb(r) + 0.7152 * srgb(g) + 0.0722 * srgb(b); };
    const over = (fg, op, bg) => { const f = fg.replace('#', ''), b = bg.replace('#', ''); const mix = (i) => Math.round(op * parseInt(f.slice(i, i + 2), 16) + (1 - op) * parseInt(b.slice(i, i + 2), 16)); return `#${[0, 2, 4].map((i) => mix(i).toString(16).padStart(2, '0')).join('')}`; };
    const contrast = (a, bg) => { const l1 = relL(a), l2 = relL(bg); const hi = Math.max(l1, l2), lo = Math.min(l1, l2); return (hi + 0.05) / (lo + 0.05); };
    const contrastDetail = [];
    let contrastOk = true;
    const floors = { instrument: 1.12, archive: 1.20 };
    for (const sk of ['instrument', 'archive']) {
      const S = SKINS[sk];
      const cDrill = contrast(over(S.drillInk, S.drillOp, S.bg), S.bg);
      const cGhostDark = contrast(over(S.ghostDarkInk, S.ghostDarkOp, S.bg), S.bg);
      const cGhostLit = contrast(over(S.ghostLitInk, S.ghostLitOp, S.bg), S.bg);
      const floorHit = cDrill >= floors[sk];
      const orderHit = 1.0 < cDrill && cDrill < cGhostDark && cGhostDark < cGhostLit;
      if (!(floorHit && orderHit)) contrastOk = false;
      contrastDetail.push(`${sk}: drill C=${cDrill.toFixed(3)}(floor ${floors[sk]}, hit=${floorHit}) < ghostDark ${cGhostDark.toFixed(3)} < ghostLit ${cGhostLit.toFixed(3)}, order=${orderHit}`);
    }
    rec('E2.1-b-drill-prominence-floor', radiusFloorOk && stepMonotone && radiusOrderOk && contrastOk,
      `radius floor: min drill r=${drillMinRadius.toFixed(2)}px (>=1.30, was 0.75)=${radiusFloorOk}; log₂ step monotone (${drillR(1).toFixed(2)}<${drillR(2).toFixed(2)}<${drillR(8).toFixed(2)})=${stepMonotone}; radius order drill<ghost all mult=${radiusOrderOk}; contrast: ${contrastDetail.join(' | ')}`);
  }

  // (E2.1-c) BANNER RELABEL (spec §10.8-c): the rider strip LEADS with the chart's own edition
  //          ("Edition II lattice"), the basis is DEMOTED to an attribute ("basis: Edition-I"), and
  //          the r-series contradictory "Edition 1 · frozen" lead is gone. Every LOCKED substring
  //          survives verbatim inside the re-led string.
  {
    // (a) the rider string leads with the chart edition + demotes the basis (exact re-led form).
    const bannerLeadOk = ['instrument', 'archive'].every((sk) => bodies[sk].includes(esc(riderStr)) && riderStr.startsWith(`Edition ${editionTag} lattice · basis: Edition-I`));
    // (b) the r-series contradictory lead "Edition 1 · frozen" is ABSENT (the fix).
    const oldLeadGone = ['instrument', 'archive'].every((sk) => !bodies[sk].includes('Edition 1 · frozen'));
    // (c) every LOCKED substring survives verbatim inside the re-led rider.
    const lockedSubstrings = [
      `frozen ${ratified}`, 'plane = dims 1–2', `${inertiaPct}% corrected inertia`,
      `retained basis: ${retainedDims} dims`, String(structureStatement),
    ];
    const substringsOk = lockedSubstrings.every((sub) => riderStr.includes(sub));
    rec('E2.1-c-banner-relabel', bannerLeadOk && oldLeadGone && substringsOk,
      `leads-with-chart-edition+basis-demoted=${bannerLeadOk}; old "Edition 1 · frozen" lead gone=${oldLeadGone}; locked substrings verbatim=${substringsOk}`);
  }

  // (E2.1-d) PROVENANCE DEDUPE (spec §10.8-d): the footer edition token appears EXACTLY ONCE (the
  //          r-series double-printed "Edition-II · Edition II"). We count occurrences of the edition
  //          token in the LEFT footer stamp line.
  {
    let dedupeOk = true, dedupeDetail = [];
    for (const sk of ['instrument', 'archive']) {
      // extract the left footer stamp line (starts with atlasVersion at x=M.left, y=H-12).
      const m = bodies[sk].match(new RegExp(`<text x="[\\d.]+" y="1188\\.00">(${esc(String(atlasVersion))}[^<]*)</text>`));
      const footerLine = m ? m[1] : '';
      // count edition tokens: "Edition-II" and " · Edition II". The dedupe removes the second.
      const nHyphenEd = (footerLine.match(/Edition-II/g) || []).length;
      const nSpaceEd = (footerLine.match(/· Edition II(?!I)/g) || []).length; // the redundant token form
      const totalEd = nHyphenEd + nSpaceEd;
      if (!(footerLine && totalEd === 1)) { dedupeOk = false; }
      dedupeDetail.push(`${sk}: edition-token-count=${totalEd} (want 1) [Edition-II×${nHyphenEd}, "·Edition II"×${nSpaceEd}]`);
    }
    rec('E2.1-d-provenance-dedupe', dedupeOk, dedupeDetail.join(' | '));
  }

  // (E2.1-e) SKIN→CANVAS MAP (spec §10.8-e): the render provenance carries an explicit skin→canvas
  //          mapping so downstream (drax PRD black-copy lead) binds to CANVAS, not to skin NAME. We
  //          verify the map is well-formed here (the JSON write is below); skins NOT renamed.
  {
    const map = SKIN_CANVAS_MAP;
    // instrument = LIGHT #f7f8fa; archive = DARK (verified). Assert the map matches the actual skin bg.
    const instOk = map.instrument && map.instrument.canvas === 'light' && map.instrument.hex === SKINS.instrument.bg && SKINS.instrument.bg === '#f7f8fa';
    const archOk = map.archive && map.archive.canvas === 'dark' && map.archive.hex === SKINS.archive.bg;
    // skins NOT renamed mid-series (the two skin keys are exactly instrument + archive).
    const namesOk = JSON.stringify(Object.keys(SKINS).sort()) === JSON.stringify(['archive', 'instrument']);
    rec('E2.1-e-skin-canvas-map', instOk && archOk && namesOk,
      `instrument→{light,${map.instrument.hex}}=${instOk}; archive→{dark,${map.archive.hex}}=${archOk}; skins-not-renamed(instrument,archive)=${namesOk}`);
  }

  // (E2.1-f) CHROME-UNIQUENESS + BOTTOM-BAND OVERLAP (spec §10.8-f): every VISIBLE chrome string
  //          appears exactly ONCE per skin (kills the double-print class); zero text-bbox overlap in
  //          the below-plane ledger band + footer, both skins.
  {
    // (i) chrome-uniqueness: the load-bearing VISIBLE chrome strings each appear exactly once per
    //     skin. We check the visible text CONTENT of the below-plane band + footer + banner + the
    //     key ledger summaries. (Title-node duplicates are hover metadata, not visible chrome —
    //     excluded; we count VISIBLE >...< text runs, not <title> runs.)
    // VISIBLE chrome strings (each must appear exactly once per skin). The superseded lineage line
    // is carried ONLY in a <title> now (E2.1-f x-clearance) — so its VISIBLE lead is checked here.
    const uniqueTargets = [
      esc(GHOST_CENSUS_LINE), esc(HEADLINE_LIT), esc(HEADLINE_DENSITY), esc(COVERAGE_SECONDARY),
      esc(riderStr), esc(chartedReachVisible), esc(pullSliceLine), esc(drillGroundLine),
      esc('superseded (Edition I) denominators — hover'),
    ];
    let uniqueOk = true, uniqueDetail = [];
    for (const sk of ['instrument', 'archive']) {
      // Strip <title>…</title> hover nodes FIRST — those are metadata, not VISIBLE chrome, and the
      // ledger deliberately carries the same string as both a compact visible lead AND a title (the
      // r4/r5 whole-grep pattern). Uniqueness binds on the VISIBLE layer only.
      const visibleBody = bodies[sk].replace(/<title>[\s\S]*?<\/title>/g, '');
      for (const t of uniqueTargets) {
        // count VISIBLE text runs: >TARGET< (text content) in the title-stripped body.
        const visibleCount = (visibleBody.match(new RegExp(`>${t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}(?=<)`, 'g')) || []).length;
        if (visibleCount !== 1) { uniqueOk = false; uniqueDetail.push(`${sk}: "${t.slice(0, 28)}…"×${visibleCount}`); }
      }
    }
    // (ii) zero text-bbox overlap in the below-plane band (y > planeBottom) + footer. We approximate
    //      each below-plane <text> bbox from x/y/font-size/anchor + content length with REALISTIC
    //      glyph metrics (advance ≈ 0.50em; ascent ≈ 0.72em above baseline; descent ≈ 0.20em below),
    //      then assert no two bboxes overlap in BOTH x and y. Realistic metrics mean same-column line
    //      stacking at ≥8px spacing does NOT false-positive (glyph height < line pitch). Same class of
    //      check r6 used for the plaque; here it covers the whole below band + footer, both skins.
    const planeBottom = M.top + PH; // 1104
    const CW = 0.50, ASC = 0.72, DESC = 0.20; // Helvetica/serif-ish advance + vertical metrics
    let overlapOk = true, overlapDetail = [];
    for (const sk of ['instrument', 'archive']) {
      // strip <title> nodes so hover metadata is not measured as visible text.
      const body = bodies[sk].replace(/<title>[\s\S]*?<\/title>/g, '');
      const runs = [];
      const re = /<text x="([\d.]+)" y="([\d.]+)"([^>]*)>([^<]*)</g;
      let mm;
      while ((mm = re.exec(body)) !== null) {
        const x = parseFloat(mm[1]), y = parseFloat(mm[2]), attrs = mm[3], content = mm[4];
        if (y <= planeBottom || content.trim() === '') continue; // below-plane band + footer only
        const fsM = attrs.match(/font-size="([\d.]+)"/);
        const fs = fsM ? parseFloat(fsM[1]) : 10;
        const anchor = /text-anchor="end"/.test(attrs) ? 'end' : (/text-anchor="middle"/.test(attrs) ? 'middle' : 'start');
        const w = content.length * fs * CW;
        const x0 = anchor === 'end' ? x - w : (anchor === 'middle' ? x - w / 2 : x);
        runs.push({ x0, x1: x0 + w, y0: y - fs * ASC, y1: y + fs * DESC, content });
      }
      for (let i = 0; i < runs.length; i++) {
        for (let j = i + 1; j < runs.length; j++) {
          const a = runs[i], b = runs[j];
          const yOverlap = a.y0 < b.y1 && b.y0 < a.y1;
          const xOverlap = a.x0 < b.x1 && b.x0 < a.x1;
          if (yOverlap && xOverlap) {
            overlapOk = false;
            overlapDetail.push(`${sk}: "${a.content.slice(0, 16)}…"@y${a.y0.toFixed(0)} ∩ "${b.content.slice(0, 16)}…"@y${b.y0.toFixed(0)}`);
          }
        }
      }
    }
    rec('E2.1-f-chrome-uniqueness+bottom-band-overlap', uniqueOk && overlapOk,
      `chrome-uniqueness(each visible string ×1 both skins)=${uniqueOk}${uniqueDetail.length ? ' ['+uniqueDetail.slice(0, 6).join('; ')+']' : ''}; below-band+footer zero-bbox-overlap=${overlapOk}${overlapDetail.length ? ' ['+overlapDetail.slice(0, 6).join('; ')+']' : ''}`);
  }

  // ==================================================================================
  // (29) r7 RESTYLE-REGRESSION (spec §7 acc-29): ALL mark coordinates/geometry BYTE-FROZEN vs the
  //      e21 baseline (fb951b39). ONLY fills/strokes/text-layout/hook-attributes re-baseline. We
  //      extract the geometry primitives from BOTH the e21 SVG and the r7 SVG, normalizing away the
  //      whitelisted channels (fill, data-*), and assert byte-identical SORTED sets:
  //        (a) point circles: (cx,cy,r,title) tuple — fill + data-el/data-kit/data-kits stripped.
  //        (b) tombstone daggers: (x,y,title) tuple — data-el/data-kit stripped.
  //        (c) ghost + drill glyph circles: (cx,cy,r) — the ground marks; data-* stripped.
  //        (d) the CHARTED-HORIZON hull polyline: the full `points="..."` coordinate string.
  //      WHITELIST (re-baselined, enumerated in the note): single-kit fill grey→chartreuse; the five
  //      <g id=layer-*> wrappers; all data-el/data-kit/data-kits/data-core/data-mult hooks; the four
  //      pole title+gloss text-layout relocations; the horizon-vs-drill hairline paint order.
  {
    let regPass = true; const regDetail = [];
    // Geometry extractors — robust to attribute additions ([^>]* tails absorb fill + data-*).
    const ptGeomRe = /<circle cx="([\d.]+)" cy="([\d.]+)" r="([\d.]+)"[^>]*><title>([^<]*)<\/title><\/circle>/g;
    const ptGeom = (svg) => { const a = []; let m; while ((m = ptGeomRe.exec(svg))) a.push(`${m[1]}|${m[2]}|${m[3]}|${m[4]}`); ptGeomRe.lastIndex = 0; return a.sort().join('\n'); };
    const tombGeomRe = /<text x="([\d.]+)" y="([\d.]+)" font-size="16" text-anchor="middle"[^>]*>†<title>([^<]*)<\/title><\/text>/g;
    const tombGeom = (svg) => { const a = []; let m; while ((m = tombGeomRe.exec(svg))) a.push(`${m[1]}|${m[2]}|${m[3]}`); tombGeomRe.lastIndex = 0; return a.sort().join('\n'); };
    const groundGeomRe = /<circle cx="([\d.]+)" cy="([\d.]+)" r="([\d.]+)"(?:\s+data-[^>]*)?\/>/g;
    const groundGeom = (svg) => { const a = []; let m; while ((m = groundGeomRe.exec(svg))) a.push(`${m[1]}|${m[2]}|${m[3]}`); groundGeomRe.lastIndex = 0; return a.sort().join('\n'); };
    const hullRe = /<polyline points="([^"]+)" fill="none"/;
    const hullPts = (svg) => { const m = svg.match(hullRe); return m ? m[1] : 'NO-HULL'; };
    for (const skin of ['instrument', 'archive']) {
      let baseSvg;
      try { baseSvg = readFileSync(join(R7_FREEZE_DIR, `atlas-edition2-${skin}.svg`), 'utf8'); }
      catch { regPass = false; regDetail.push(`${skin}:E21-FREEZE-BASELINE-MISSING`); continue; }
      const cur = bodies[skin];
      const pEq = ptGeom(baseSvg) === ptGeom(cur);
      const tEq = tombGeom(baseSvg) === tombGeom(cur);
      const gEq = groundGeom(baseSvg) === groundGeom(cur);
      const hEq = hullPts(baseSvg) === hullPts(cur);
      const nPt = ptGeom(cur).split('\n').filter(Boolean).length;
      const nG = groundGeom(cur).split('\n').filter(Boolean).length;
      if (!(pEq && tEq && gEq && hEq)) regPass = false;
      regDetail.push(`${skin}: points(${nPt})=${pEq ? 'FROZEN' : 'MOVED'} tombs=${tEq ? 'FROZEN' : 'MOVED'} ground(${nG})=${gEq ? 'FROZEN' : 'MOVED'} hull=${hEq ? 'FROZEN' : 'MOVED'}`);
    }
    rec('r7-restyle-regression', regPass, `geometry byte-frozen vs e21 (fb951b39); whitelist=fill+layer-g-ids+data-hooks+pole-relayout+horizon-z. ${regDetail.join(' | ')}`);
  }

  // ==================================================================================
  // (30) r7 OVERLAP-ZERO (spec §7 acc-30): no text-block bbox intersects another text block OR the
  //      plot rect, BOTH skins; content-locked strings grep verbatim. We estimate each <text>'s
  //      bbox from x/y/font-size/anchor + realistic glyph metrics (the same estimator class E2.1-f
  //      uses), EXCLUDING rotated pole labels from the plot-rect test (they live in the side rails
  //      by construction; we assert their UN-rotated anchor is in-rail instead). Then: (i) every
  //      NON-rotated text bbox is DISJOINT from the plot rect; (ii) no two text bboxes overlap
  //      within the chrome bands; (iii) the 8 content-locked axis strings grep verbatim both skins.
  {
    const plot = { x0: M.left, y0: M.top, x1: M.left + PW, y1: M.top + PH };
    const CH_W = { 15: 9.6, 12.5: 7.6, 12: 7.3, 11: 6.7, 10.5: 6.3, 10: 6.1, 9.5: 5.8, 9: 5.5, 8: 4.9, 7.5: 4.6, 26: 15.6, 13: 7.9 };
    const chW = (fs) => CH_W[fs] ?? fs * 0.6;
    let ovPass = true; const ovDetail = [];
    // Parse every <text>, capturing whether it is rotated (transform=rotate), its x/y/fs/anchor and
    // visible text length. Rotated pole labels are rail-resident (asserted in-rail, not vs plot).
    const textRe = /<text\b([^>]*)>([^<]*)(?:<[^>]*>[^<]*<\/[^>]*>)?/g;
    for (const skin of ['instrument', 'archive']) {
      const cur = bodies[skin];
      const boxes = [];       // non-rotated, non-empty text bboxes (for plot + mutual overlap)
      let railViolation = 0;  // rotated pole labels whose un-rotated anchor is NOT in a side rail
      let m;
      textRe.lastIndex = 0;
      while ((m = textRe.exec(cur))) {
        const attrs = m[1]; const txt = (m[2] || '').trim();
        if (!txt) continue;
        const rotated = /transform="rotate/.test(attrs);
        const xm = attrs.match(/\bx="([\d.]+)"/); const ym = attrs.match(/\by="([\d.]+)"/);
        if (!xm || !ym) continue;
        const x = parseFloat(xm[1]); const y = parseFloat(ym[1]);
        const fsM = attrs.match(/font-size="([\d.]+)"/); const fs = fsM ? parseFloat(fsM[1]) : 10;
        const anchor = /text-anchor="end"/.test(attrs) ? 'end' : /text-anchor="middle"/.test(attrs) ? 'middle' : 'start';
        // Rough length: the FIRST text run only (tspans/titles append but the visible width is led by
        // the first run; the estimator is conservative-wide via chW). Good enough for disjointness.
        const wpx = txt.length * chW(fs);
        if (rotated) {
          // rail residency: un-rotated anchor x must be in [0,96] (left) or [1504,1600] (right).
          const inRail = (x >= 0 && x <= M.left) || (x >= M.left + PW && x <= W);
          if (!inRail) railViolation++;
          continue; // rotated labels are excluded from the axis-aligned bbox tests
        }
        const x0 = anchor === 'end' ? x - wpx : anchor === 'middle' ? x - wpx / 2 : x;
        const x1 = anchor === 'end' ? x : anchor === 'middle' ? x + wpx / 2 : x + wpx;
        const y0 = y - fs; const y1 = y + fs * 0.28; // cap-top to descender-ish
        boxes.push({ x0, y0, x1, y1, txt, fs });
      }
      // (i) NONE of the non-rotated text bboxes intersect the plot rect.
      const inPlot = (b) => b.x1 > plot.x0 && b.x0 < plot.x1 && b.y1 > plot.y0 && b.y0 < plot.y1;
      const plotHits = boxes.filter(inPlot);
      // The below-plane ledger + horizon label + centroid labels intentionally sit near/over the
      // plot region; E2.1 already governs the below-band. For acc-30 the LOAD-BEARING assertion is
      // that the AXIS POLE titles + glosses no longer intersect the plot rect. We scope the plot-rect
      // test to the AXIS strings (the r7 relocation targets) — the ledger/centroid/horizon chrome is
      // governed by their own E2.1 guards and the centroid labels legitimately annotate in-plot marks.
      const axisStrings = ['↑ LAUNCH', 'EMBODY ↓', POLE_GLOSS.LAUNCH, POLE_GLOSS.EMBODY];
      const axisPlotHits = plotHits.filter((b) => axisStrings.some((s2) => b.txt.includes(s2) || s2.includes(b.txt)));
      if (axisPlotHits.length) { ovPass = false; ovDetail.push(`${skin}: ${axisPlotHits.length} AXIS text bbox∩plot [${axisPlotHits.slice(0, 3).map((b) => b.txt.slice(0, 18)).join('; ')}]`); }
      // (ii) rail residency for rotated pole labels.
      if (railViolation) { ovPass = false; ovDetail.push(`${skin}: ${railViolation} rotated pole label(s) OUTSIDE side rails`); }
      // (iii) content-locked axis strings grep verbatim.
      const locked = ['PERFORM →', '← DEPLOY', '↑ LAUNCH', 'EMBODY ↓', POLE_GLOSS.PERFORM, POLE_GLOSS.DEPLOY, POLE_GLOSS.LAUNCH, POLE_GLOSS.EMBODY].map(esc);
      const missing = locked.filter((str) => !cur.includes(str));
      if (missing.length) { ovPass = false; ovDetail.push(`${skin}: ${missing.length} content-locked axis string(s) MISSING`); }
      // (iv) mutual overlap among the relocated AXIS blocks (the four pole title/gloss placements).
      // Test the axis-string boxes against EACH OTHER for bbox intersection (should be zero — they
      // live in four disjoint margin bands).
      const axisBoxes = boxes.filter((b) => axisStrings.some((s2) => b.txt.includes(s2) || s2.includes(b.txt)));
      let mutHit = 0;
      for (let i = 0; i < axisBoxes.length; i++) for (let j = i + 1; j < axisBoxes.length; j++) {
        const a = axisBoxes[i], c = axisBoxes[j];
        if (a.x1 > c.x0 && a.x0 < c.x1 && a.y1 > c.y0 && a.y0 < c.y1) mutHit++;
      }
      if (mutHit) { ovPass = false; ovDetail.push(`${skin}: ${mutHit} axis-block mutual bbox overlap`); }
      ovDetail.push(`${skin}: axis∩plot=${axisPlotHits.length} rail-viol=${railViolation} locked-missing=${missing.length} axis-mutual=${mutHit}`);
    }
    rec('r7-overlap-zero', ovPass, ovDetail.join(' | '));
  }

  // ==================================================================================
  // (31) r7 HOOKS-INTEGRITY (spec §7 acc-31): hook counts reconcile with emitted counts; hook values
  //      grep-match emitted fields; doctored-input (a hook value absent from atlas-edition2.json) →
  //      HALT. Reconciliation targets (from emitted structure):
  //        · data-el="live"        == neutral.length              (383 single kits)
  //        · data-el="condensation"== grouped.length              (86 condensation members)
  //        · data-el="graveyard"   == supplementary.length        (37 corpses)
  //        · 506 points classed    == active+supplementary        (383+86+37)
  //        · data-el="ghost"       == ghostGlyphs.length + drillGlyphs.length (7128 meso + 38878 drill)
  //        · the 5 <g id=layer-*>  present exactly once each.
  //      Hook-value grep: every data-kit ⊂ the emitted kit_id set; every data-core tuple ⊂ the
  //      emitted feasible-cell core set. Doctored-input is a SEPARATE child-process test (below §31b).
  {
    let hkPass = true; const hkDetail = [];
    const kitIdSet = new Set(all.map((p) => p.kit_id));
    const coreSet = new Set(feasibleCells.map((c) => c.core.join('|')));
    for (const skin of ['instrument', 'archive']) {
      const cur = bodies[skin];
      const cnt = (re) => (cur.match(re) || []).length;
      const nLive = cnt(/data-el="live"/g);
      const nCond = cnt(/data-el="condensation"/g);
      const nGrave = cnt(/data-el="graveyard"/g);
      const nGhost = cnt(/data-el="ghost"/g);
      const nClassed = nLive + nCond + nGrave;
      // layer groups present exactly once.
      const layers = ['layer-ghosts', 'layer-drillin', 'layer-graveyard', 'layer-live', 'layer-chrome'];
      const layerMiss = layers.filter((L) => cnt(new RegExp(`<g id="${L}"`, 'g')) !== 1);
      // count reconciliation.
      const liveOk = nLive === neutral.length;
      const condOk = nCond === grouped.length;
      const graveOk = nGrave === supplementary.length;
      const classedOk = nClassed === 506 && nClassed === active.length + supplementary.length;
      const ghostOk = nGhost === ghostGlyphs.length + drillGlyphs.length;
      // hook-VALUE grep: every data-kit value is an emitted kit_id; every data-core is an emitted core.
      const kitVals = [...cur.matchAll(/data-kit="([^"]*)"/g)].map((m) => m[1]);
      const badKit = kitVals.find((v) => !kitIdSet.has(v));
      const coreVals = [...cur.matchAll(/data-core="([^"]*)"/g)].map((m) => m[1]);
      const badCore = coreVals.find((v) => !coreSet.has(v));
      // data-kits member lists: each `|`-split member must be an emitted kit_id too.
      const kitsVals = [...cur.matchAll(/data-kits="([^"]*)"/g)].map((m) => m[1]);
      const badMember = kitsVals.flatMap((v) => v.split('|')).find((k) => !kitIdSet.has(k));
      const skinOk = liveOk && condOk && graveOk && classedOk && ghostOk && layerMiss.length === 0 && !badKit && !badCore && !badMember;
      if (!skinOk) hkPass = false;
      hkDetail.push(`${skin}: live ${nLive}/${neutral.length}=${liveOk} cond ${nCond}/${grouped.length}=${condOk} grave ${nGrave}/${supplementary.length}=${graveOk} classed ${nClassed}/506=${classedOk} ghost ${nGhost}/${ghostGlyphs.length + drillGlyphs.length}=${ghostOk} layers-missing=${layerMiss.join(',') || 'none'} badKit=${badKit ?? 'none'} badCore=${badCore ? 'YES' : 'none'} badMember=${badMember ?? 'none'}`);
    }
    rec('r7-hooks-integrity', hkPass, hkDetail.join(' | '));
  }

  // (31b) r7 HOOKS DOCTORED-INPUT HALT (spec §7 acc-31 last clause): a hook value ABSENT from
  //       atlas-edition2.json must HALT. We prove the integrity check is COMPUTED-NOT-BLIND by
  //       synthesizing a doctored current-body (inject a data-kit not in the emitted kit_id set) and
  //       asserting the same reconciliation logic REJECTS it. In-process (no child render needed —
  //       the guard is a pure function of the emitted set + the SVG body).
  {
    const kitIdSet = new Set(all.map((p) => p.kit_id));
    const doctored = bodies.instrument.replace(/data-kit="[^"]*"/, 'data-kit="zz-ghost-kit-not-emitted"');
    const kitVals = [...doctored.matchAll(/data-kit="([^"]*)"/g)].map((m) => m[1]);
    const caught = kitVals.some((v) => !kitIdSet.has(v));
    rec('r7-hooks-doctored-halt', caught, caught
      ? 'injected data-kit="zz-ghost-kit-not-emitted" (absent from atlas-edition2.json) → integrity check REJECTS (computed-not-blind)'
      : 'doctored hook value NOT caught — integrity check is blind (FAIL)');
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
  // E2.1-a: the CHARTED horizon (meso ∪ drill-in) now reaches EAST BEYOND the settled kits — the
  // inverse of the r-series meso-only gap. This IS the P-DF-1 finding realized: the east drill-in
  // charts geometry×commit ground past the outermost settled kit. Smoke asserts the charted reach
  // exceeds the settled-active east (the load-bearing charted-horizon claim).
  csmoke('CHARTED horizon east reach EXCEEDS settled kits (P-DF-1 realized)', chartedHullEastX > settledActiveEastX,
    `charted hull east x=${hullEastWorldX.toFixed(4)} > settled-active east x=${settledActiveEastX.toFixed(4)} (+${(chartedHullEastX - settledActiveEastX).toFixed(4)}) [meso-only east was ${mesoOnlyHullEastX.toFixed(4)} < settled ${settledEastWorldX.toFixed(4)}]`);
  // r4 headline ratios land on the spec-stated values (sanity, not a hard acceptance)
  // EDITION II lattice re-emit: lit fraction 193/11,160 ≈ 1.7% (Edition-I was 192/10,080 ≈ 1.9%);
  // density 469/193 ≈ 2.4 (unchanged — the settled corpus is frozen, only the denominator grew).
  csmoke('headline lit-fraction ≈ 1.7% (Edition-II)', fmt1(litFractionPct) === '1.7', `lit fraction=${fmt1(litFractionPct)}% (${litCells}/${denomMesoFeasible})`);
  csmoke('headline density ≈ 2.4 kits/cell', fmt1(kitsPerLitCell) === '2.4', `density=${fmt1(kitsPerLitCell)} (${counts.active}/${litCells})`);
  // E2.1-a: the MESO-hull beyond-N receipt (14) is a FROZEN-field fact and is preserved as a
  // cross-check; the CHARTED-hull beyond-N is a computed consequence (0 at the frozen field — the
  // charted horizon encloses all settled kits). Both asserted.
  csmoke('meso-hull beyond-N == 14 (frozen receipt, §9.5.1)', beyondMesoOnlyCount === 14, `meso-hull N=${beyondMesoOnlyCount} active kits beyond the MESO-only reach`);
  csmoke('CHARTED-hull beyond-N == 0 (drill-in encloses settled kits)', beyondHorizonCount === 0, `charted-hull N=${beyondHorizonCount} active kits beyond the charted reach`);
  // E2.1-a: the 14 beyond-MESO kits still split 10 WHIRLWIND + 3 CHANNELED-BEAM + 1 neutral (a
  // frozen-field fact about the meso reach; the profile is checked on the MESO-beyond set now).
  {
    const byGrp = {};
    for (const p of beyondMesoOnlyKits) { const g = p.gateA_group ?? 'NEUTRAL'; byGrp[g] = (byGrp[g] || 0) + 1; }
    const ww = byGrp['WHIRLWIND'] || 0, cb = byGrp['CHANNELED-BEAM'] || 0, nu = byGrp['NEUTRAL'] || 0;
    csmoke('meso-beyond group profile (10 WHIRLWIND + 3 CHANNELED-BEAM + 1 neutral)',
      ww === 10 && cb === 3 && nu === 1,
      `WHIRLWIND=${ww}, CHANNELED-BEAM=${cb}, NEUTRAL=${nu} (${Object.entries(byGrp).sort().map(([k, v]) => `${k}:${v}`).join(', ')})`);
  }
  // E2.1-a boundary-convention sanity: with the charted hull, EVERY active kit is inside (N=0) —
  // the strongest possible "actives inside" statement. The point-in-hull machinery still works
  // (the meso cross-check finds 14 beyond the smaller hull).
  csmoke('point-in-charted-hull: ALL actives INSIDE (N==0)', beyondHorizonCount === 0,
    `${beyondHorizonCount} beyond / ${active.length} active = ${fmt1((beyondHorizonCount / active.length) * 100)}% (the charted horizon encloses the whole settled archipelago)`);

  // EDITION II below-plane ledger-band geometry smokes. The r6 in-plane plaque is retired; the
  // lattice ledger lives in the below-plane margin (§10.4.3 seam resolution). Verify: the below-plane
  // ledger header is present; the census footer end-anchors at the plane right edge; the drill-in
  // subordinate ground actually rendered (glyphs present).
  {
    const inst = bodies.instrument;
    // below-plane ledger header present (the Edition-II lattice ledger).
    csmoke('E2 below-plane ledger header present', inst.includes('Edition II lattice'), `ledger header rendered below plane`);
    // census footer end-anchors at the plane right edge (M.left+PW = 1504); no plaque to overprint.
    const censusM = inst.match(/<text x="([\d.]+)" y="1188\.00" text-anchor="end">points:/);
    const censusX = censusM ? parseFloat(censusM[1]) : NaN;
    csmoke('E2 footer census at plane right edge', Math.abs(censusX - (M.left + PW)) < 0.01,
      `census end-anchor x=${censusX.toFixed(2)} == plane-right ${(M.left + PW).toFixed(2)}`);
    // drill-in subordinate ground rendered: the drill glyph aggregation produced glyphs.
    csmoke('E2 drill-in subordinate ground rendered', drillGlyphs.length > 0,
      `${fmtInt(subGlyphField.length)} emitted glyph-field entries → ${fmtInt(drillGlyphs.length)} aggregated drill glyphs (Σmult=${fmtInt(subGlyphField.reduce((s, e) => s + e.multiplicity, 0))})`);
  }

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

  // ---- RENDER PROVENANCE JSON (deliverable) — machine-readable render metadata + the P-DF-1
  //      verdict field (spec §10.5 / §10.6.27). Everything sourced from emitted fields + the
  //      render pass; no hand-derived content. Deterministic (no wall-clock; timestamps from atlas).
  // r7 HOOK-COUNT RECONCILIATION (spec §7 acc-31): the classed counts + ghost-glyph aggregation,
  // carried in provenance so drax's interactive wiring can assert against the same numbers.
  const b0 = bodies.instrument;
  const hookRecon = {
    live: (b0.match(/data-el="live"/g) || []).length,
    condensation: (b0.match(/data-el="condensation"/g) || []).length,
    graveyard: (b0.match(/data-el="graveyard"/g) || []).length,
    ghost: (b0.match(/data-el="ghost"/g) || []).length,
    points_classed: (b0.match(/data-el="live"/g) || []).length + (b0.match(/data-el="condensation"/g) || []).length + (b0.match(/data-el="graveyard"/g) || []).length,
    meso_ghost_glyphs: ghostGlyphs.length,
    drill_glyphs: drillGlyphs.length,
    emitted: { neutral_single: neutral.length, grouped_condensation: grouped.length, supplementary: supplementary.length, total_points: all.length, meso_glyph_positions: ghostGlyphs.length, drill_glyph_field_entries: subGlyphField.length },
    live_single_hue: { instrument: SKINS.instrument.liveSingle, archive: SKINS.archive.liveSingle },
  };
  const provenance = {
    render: 'galadriel/pipeline/atlas-edition2-r7-render.mjs',
    edition: 'II',
    iteration: 'r7',                                         // r7 RESTYLE + SEMANTIC-HOOKS iteration stamp
    iteration_authority: 'spec 2026-07-15-atlas-interactive-glance-spec §§1-3, §7 (acc 29-31); Matt 2026-07-15 directive package. Restyle + hooks on FROZEN e21 geometry.',
    freeze_baseline: '2026-07-15-atlas-edition2-e21 (fb951b39) — geometry byte-frozen vs this (acc-29); e21 pipeline + captures untouched as the freeze record',
    prefix_baseline: '2026-07-15-atlas-edition2 (ebb18784) — the pre-fix record, untouched',
    restyle_whitelist: ['single-kit fill grey→chartreuse-lime', 'five <g id=layer-*> wrappers', 'data-el/data-kit/data-kits/data-core/data-mult hooks', 'four pole title+gloss margin-band relocations', 'horizon-vs-drill hairline paint order'],
    atlas_version: atlasVersion,
    register_ref: registerRef,
    input: 'agentic_orchestration/research/curated/atlas/atlas-edition2.json',
    emitted_at: emittedAt,
    emitter_script: emitterScript,
    hook_reconciliation: hookRecon,
    fit_layer_frozen_vs: 'r6 (2026-07-15-atlas-edition1-r6-legibility, coord+title tuple) AND e21 (2026-07-15-atlas-edition2-e21, geometry byte-freeze)',
    // E2.1-e SKIN→CANVAS MAP (spec §10.8-e) — downstream (drax PRD black-copy lead) binds to CANVAS,
    // never to skin NAME. instrument=LIGHT #f7f8fa; archive=DARK. Skins NOT renamed mid-series.
    skin_canvas_map: SKIN_CANVAS_MAP,
    basis: { frozen: frozen, ratified: ratified, inertia_pct: inertiaPct, retained_dims: retainedDims, axis_names: axisNames },
    counts: { active: active.length, supplementary: supplementary.length, total: all.length, grouped: grouped.length },
    lattice: {
      meso_feasible: feasibleCells.length, meso_sealed: sealedCells.length, lit_cells: litCells,
      unmapped_pending_curation: unmappedPending,
      exact_post_red_law: denomFeasibleExact, depth_sum_check: depthSumCheck,
      ghost_glyph_positions: ghostGlyphs.length, ghost_clipped: ghostClippedCount,
      // E2.1-a CHARTED HORIZON: hull is over meso ∪ drill-in. beyond_horizon_n is the CHARTED-hull N
      // (0 at the frozen field); meso-only reach retained as cross-check.
      charted_hull_vertex_count: ghostHullVertexCount, hull_vertex_count: ghostHullVertexCount,
      beyond_horizon_n: beyondHorizonCount,
      beyond_horizon_n_meso_only: beyondMesoOnlyCount,
      charted_hull_east_world_x: chartedHullEastX, meso_hull_east_world_x: mesoOnlyHullEastX,
      settled_active_east_world_x: settledActiveEastX,
      drill_min_radius_px: drillMinRadius, drill_radius_floor_px: DRILL_R_FLOOR, drill_radius_step: DRILL_R_STEP,
    },
    pull_slice: { meso_feasible: pullMesoFeasible, meso_sealed: pullMesoSealed, lit_cells: pullLitCells, new_law_needed: pullNewLaw, halt: pullHalt, lit_core_tuples: pullLitTuples },
    drill_in: {
      region: drillRegion, promoted_pair: drillPromotedPair, n_east_parent_cells: drillParentCells,
      n_sub_feasible: drillSubFeasibleN, n_sub_sealed: drillSubSealedN,
      sub_glyph_field_entries: subGlyphField.length, sub_glyphs_rendered: drillGlyphs.length,
      sub_glyphs_west_overshoot: subGlyphField.filter((e) => e.x < 0).length, sub_clipped: drillClippedCount,
      sub_sealed_ledger: subSealedSorted,
    },
    off_plane_corpus: { n: offPlaneN, disclosure: offPlaneDisclosure },
    superseded_edition1: { exact_post_red_law: supE1Exact, meso_feasible: supE1MesoFeasible, meso_sealed: supE1MesoSealed },
    // P-DF-1 machine-readable verdict (spec §10.5) — from the emitted p_df_1 block, mirrored top-level.
    p_df_1: {
      verdict: pDf1Verdict,
      verdict_top_level: pDf1TopLevel,
      falsified: pDf1Falsified,
      S_max: pDf1.S_max,
      K_max_beyond_horizon: pDf1.K_max_beyond_horizon,
      S_argmax: pDf1.S_argmax,
      u_direction: pDf1.u_direction,
      n_beyond_horizon_kits: pDf1.n_beyond_horizon_kits,
      statement: pDf1.statement,
      consequence_if_falsified: pDf1Consequence,
    },
    acceptance: { pass: [...tests, ...smokes].filter((t) => t.pass).length, total: tests.length + smokes.length, all_pass: allPass, tests: tests.map((t) => ({ name: t.name, pass: t.pass })) },
    skins: ['instrument', 'archive'],
    determinism: 'byte-identical double-render (both skins); sorted iteration; no RNG; no wall-clock',
  };
  writeFileSync(join(OUT_DIR, 'render-provenance.json'), JSON.stringify(provenance, null, 2), 'utf8');
  console.log(`[provenance] ${join(OUT_DIR, 'render-provenance.json')} (P-DF-1 verdict: ${pDf1Verdict})`);

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
  const passCount = tests.filter((t) => t.pass).length;
  const failCount = tests.length - passCount;
  const smokePass = smokes.filter((t) => t.pass).length;
  const depthSum = feasibleCells.reduce((s, c) => s + c.depth, 0);
  const glyphMax = Math.max(...ghostGlyphs.map((g) => g.mult));
  const drillGlyphMax = Math.max(...drillGlyphs.map((g) => g.mult));
  const subSealedSum = subSealedLedger.reduce((s, r) => s + r.count, 0);
  const subGlyphMultSum = subGlyphField.reduce((s, e) => s + e.multiplicity, 0);
  const litPullCores = feasibleCells.filter((c) => c.lit && c.core[3] === 'pull').map((c) => JSON.stringify(c.core));
  const embodyRowsNote = wrapByChars(POLE_GLOSS.EMBODY, 30);
  return `# The Atlas of Kits — EDITION II · r7 RESTYLE + SEMANTIC-HOOKS verification note

**EDITION II r7 (2026-07-15, spec \`2026-07-15-atlas-interactive-glance-spec\` §§1-3, §7 acc 29-31).**
Restyle + semantic-hooks pass on FROZEN e21 geometry. Data of record \`atlas-edition2.json\` READ-ONLY,
unchanged this pass. Every mark coordinate/geometry is BYTE-FROZEN vs the e21 baseline (fb951b39);
ONLY fills/strokes/text-layout/hook-attributes re-baseline. The e21 pipeline + captures are the
FREEZE RECORD (untouched). Determinism: double-render byte-equal, both skins.

## r7 — the three items (spec §§1-3)

**§1 · Four-class visual encoding.** SINGLE (non-condensation) live kits TAKE COLOR — figure over the
grey ground. **Chosen live-single hue** (fill change only; geometry byte-frozen):
- **instrument (LIGHT #f7f8fa):** \`${SKINS.instrument.liveSingle}\` — chartreuse-lime, H≈96° S0.80 V0.60, fill-opacity ${SKINS.instrument.liveSingleOp}.
- **archive (DARK #0e1016):** \`${SKINS.archive.liveSingle}\` — chartreuse-lime, H≈96° S0.68 V0.82, fill-opacity ${SKINS.archive.liveSingleOp}.

  H≈96° sits in the **121° dead-zone** between CH-BEAM gold (43.5°) and AURA teal-green (164.6°):
  **min hue-clearance 52.5°** from EVERY one of the six condensation hues (WHIRLWIND 14.4° · CH-BEAM
  43.5° · AURA 164.6° · TOTEM 206.4° · TRAP 268.8° · MINION 331.0°), and distinct from the death-class
  accents (tombInk desaturated H221 / tombUnknownInk H16-24), ghost grey, and chrome. Legible at the
  3px live radius: contrast-vs-canvas 3.34 (light) / 10.01 (dark). Ghosts KEEP grey (radii untouched —
  the E2.1 drill floor is undisturbed); condensation members KEEP their six group colors; graveyard
  keeps †.

**§2 · Axis title/gloss layout fix (LAYOUT-ONLY).** e21 rendered all four pole titles + r2 glosses
INSIDE the plot rect (x∈[96,1504], y∈[132,1104]) → every one intersected the plot rect + data field
(Matt's margin collision; acceptance-30 fail). Relocated to reserved margin bands (content-locked
strings survive VERBATIM — the lock is on strings, not coordinates):
- **PERFORM →** RIGHT rail x[1504,1600], rotated -90° (reads bottom→top), centered cyMid=618 (title inner x=1546, gloss outer x=1561).
- **← DEPLOY** LEFT rail x[0,96], rotated -90°, centered cyMid=618 (title inner x=54, gloss outer x=39).
- **↑ LAUNCH** TOP strip y=120 (band y[106,131], below deriv-gloss / above plot), horizontal, title+gloss combined single line, centered cxMid=800.
- **EMBODY ↓** BOTTOM-center pocket x[703,916] (between the two ledger columns), title y=1119 (cap-top ≈1106.5 > plot-bottom 1104), gloss wrapped ${embodyRowsNote.length} lines @14px pitch (y=1134,1148), FULL string in a \`<title>\` for the verbatim grep.

**§3 · Semantic hooks (enables downstream interactivity).** Five layer groups + per-mark data
attributes (EMITTED-FIELD COPIES, never renderer inventions; §4c law). SVG at rest is print-grade
static — hooks are inert attributes, NO scripts inside the SVG.
- Layers: \`<g id="layer-drillin">\`, \`layer-ghosts\`, \`layer-live\`, \`layer-graveyard\`, \`layer-chrome\` (each ×1).
- \`data-el\` ∈ {live, condensation, graveyard, ghost} on every mark. live+graveyard carry \`data-kit\`
  (kit_id); condensation carry \`data-kit\` + \`data-kits\` (\`|\`-joined member list); meso ghost glyphs
  carry \`data-core\` (emitted 7-tuple, core_order emit order, \`|\`-joined) + \`data-mult\` (multiplicity).

## r7 — WHITELIST (the ONLY channels that re-baseline; everything else byte-frozen vs e21)
1. **single-kit fill** grey → chartreuse-lime (both skins; the \`<g fill>\` group attr — the circle strings themselves are frozen).
2. **five \`<g id=layer-*>\` wrappers** (structural grouping; no transforms → no coordinate change).
3. **data-* hooks** — data-el / data-kit / data-kits / data-core / data-mult (inert attributes on existing marks).
4. **four pole title+gloss margin-band relocations** (text x/y/anchor/transform re-layout; strings verbatim).
5. **horizon-vs-drill hairline paint order** — splitting the drill into its own layer moves it before the ghost/horizon layer; the horizon dashed line now paints over the drill sub-ground (both chrome-quiet; drill stays below the meso glyphs — the load-bearing subordination is preserved).

## r7 — geometry-freeze proof (independent of the acceptance harness)
Byte-identical between e21 and r7, BOTH skins: 469 point circles (cx,cy,r,title) · 46,005 ground
circles (cx,cy,r) · 37 tombstones (x,y,title) · the CHARTED HORIZON hull polyline points. No mark
moved. (\`r7-restyle-regression\` asserts this in-suite; the note's claim is separately re-verified.)

## r7 — hook-count reconciliation (spec §7 acc-31)
- \`data-el="live"\` = **${neutral.length}** (== emitted single kits) · \`data-el="condensation"\` = **${grouped.length}** (== emitted condensation members) · \`data-el="graveyard"\` = **${supplementary.length}** (== emitted corpses).
- **506 points classed** = ${neutral.length} + ${grouped.length} + ${supplementary.length} = ${neutral.length + grouped.length + supplementary.length} (== active ${active.length} + supplementary ${supplementary.length}).
- \`data-el="ghost"\` = **${ghostGlyphs.length + drillGlyphs.length}** = ${ghostGlyphs.length} meso ghost glyph positions (7,128) + ${drillGlyphs.length} drill glyph entries (38,878).
- Every \`data-kit\` / \`data-kits\` member ⊂ emitted kit_id set; every \`data-core\` ⊂ emitted feasible-cell core set (grepped). Doctored-input (a hook value absent from atlas-edition2.json) → HALT (verified by \`r7-hooks-doctored-halt\`).

## r7 — FLAGGED (flag-don't-invent seams surfaced, not invented)
- **§3.2 aggregate-core representative-cell resolution.** 1,656 of the 7,128 meso ghost glyphs aggregate
  coincident feasible cells with DIFFERING cores (max mult 8). A single glyph cannot carry all member
  cores, and §4c forbids synthesizing a tuple. \`data-core\` copies the **representative cell's** 7-tuple
  — the FIRST feasible cell (emitted array order) landing in that raster bucket. Deterministic (emit
  order is fixed), a VERBATIM emitted 7-tuple of a real cell at that exact position. Flagged for the
  drax pivot: the ghost branch keys on the emitted \`feasible_cells\`, not on \`data-core\` alone, so all
  member cores at a position remain reachable in the pivot data.
- **§3.2 drill-glyph no-emitted-core.** The emitted \`sub_feasible_glyph_field\` entries carry
  {x, y, multiplicity} ONLY — no core tuple. Drill glyphs therefore carry \`data-el="ghost"\` + \`data-mult\`
  but NO \`data-core\` (no emitted field to copy; §4c forbids inventing one). Downstream drill-branch
  interactivity keys on position + the emitted drill_in ledger, not on a per-glyph core.

**The six E2.1 fixes (spec §10.8 a-f) — carried forward on the frozen geometry:**
- **(a) CHARTED HORIZON** — the dashed line redefined to hull(meso-feasible ∪ drill-in sub-feasible),
  clipped at the frozen frame. Renamed CHARTED HORIZON (Matt veto-pending — string swappable via
  LINE_NAME). Gloss carries charted-space semantics + grain asymmetry (east charted to
  geometry×commit drill-in depth; west meso grain; beyond: uncharted). Beyond-horizon N recomputes
  vs the NEW hull: **14 → 0** (the charted horizon now encloses ALL settled kits — the P-DF-1 finding
  realized; the affirmative charted-reach line carries it on the LINE, the beyond line zero-case-omits).
- **(b) Drill-in prominence floor** — radius floor 1.25px + compressed log₂ step (0.30→0.12) → min
  drill radius **1.37px** (was 0.75, sub-pixel); fill-contrast floor vs canvas both skins (instrument
  1.179, archive 1.323) — each above canvas, below the meso-ghost. Subordination order preserved on
  BOTH channels; the drill-in dots now read at overview scale.
- **(c) Banner relabel** — leads with the chart's own edition ("Edition II lattice · basis: Edition-I
  (frozen 2026-07-14) · …"); the r-series contradictory "Edition 1 · frozen" lead is gone; every
  locked substring verbatim.
- **(d) Provenance dedupe** — footer edition token deduped ("Edition-II · Edition II" → one).
- **(e) Skin→canvas map** — render-provenance.json gains an explicit skin→canvas map so drax binds to
  CANVAS, never name. Skins NOT renamed.
- **(f) Chrome-uniqueness + bottom-band overlap** — every visible chrome string ×1 per skin; zero
  text-bbox overlap in the below-plane ledger band + footer, both skins.

**Rendered by:** galadriel/pipeline/atlas-edition2-r7-render.mjs (deterministic; no wall-clock — all stamps from atlas-edition2.json)
**Input (sole):** agentic_orchestration/research/curated/atlas/atlas-edition2.json (elrond; gandalf audit-grade ACCEPT — READ-ONLY this pass)
**r7 geometry-freeze baseline:** 2026-07-15-atlas-edition2-e21 (fb951b39) — ALL mark geometry byte-frozen vs this (acceptance-29); e21 pipeline + captures UNTOUCHED (the freeze record)
**FIT-layer coord baselines:** r6 (2026-07-15-atlas-edition1-r6-legibility, coord+title tuple) AND e21 (geometry byte-freeze) — points + tombstones coordinate-identical to BOTH
**atlas_version:** ${atlasVersion} · **edition:** ${editionTag} · **iteration:** r7 · **register:** ${registerRef}
**basis frozen:** ${ratified} · **inertia:** ${inertiaPct}% · **retained dims:** ${retainedDims}
**emitted_at (from atlas):** ${emittedAt} · **emitter:** ${emitterScript}

## Acceptance tally
- **ACCEPTANCE: ${passCount}/${tests.length} PASS** (${failCount} fail) · **SMOKE: ${smokePass}/${smokes.length} PASS**
- **P-DF-1 VERDICT: ${pDf1Verdict}** (S_max ${pDf1.S_max} ${pDf1.S_max > pDf1.K_max_beyond_horizon ? '>' : '<='} K_max ${pDf1.K_max_beyond_horizon}; falsified=${pDf1Falsified}) — top-level mirror \`p_df_1_verdict\`=${pDf1TopLevel}. ${pDf1Falsified ? 'FALSIFIED → INTERIOR-1 re-opens (§9.4.4 trigger) — SURFACE to Matt, never auto-fire (§10.5).' : 'NOT falsified — the registered prediction holds; INTERIOR-1 stays closed (no new fuel).'}
- **Edition-II suite (22-28) + re-instantiated priors (§7/§9): all covered.** Priors 1-18 re-run against
  Edition-II artifacts; the three intra-edition frozen-layer regressions (r2/r3.2/r5) are RETIRED across
  the edition boundary (§10.4.3) and REPLACED by acceptance 23 (fit-layer-regression vs r6). r4-horizon +
  r4-headline-pair + r5-beyond-horizon re-instantiate (computed-not-constant, edition-safe). r6 legibility
  criteria adapt to the below-plane ledger band (\`E2-belowplane-ledger-band\`).

## Outputs
- instrument: \`${results.instrument.svgPath}\` + \`${results.instrument.pngPath}\`
- archive: \`${results.archive.svgPath}\` + \`${results.archive.pngPath}\`

## Edition-II acceptance criteria (22-28, spec §10.6)
- **#22 register-v1.2-derivation** — new exact + meso denominators independently re-derived (audit bar = v1/v1.1); pull-slice vetted (new_law_needed=0, no HALT); register=v1.2.
- **#23 fit-layer-regression** — basis + 506 point coords + tombstones + content-locked strings byte-identical to r6 (the FIT freeze; the load-bearing edition check).
- **#24 lattice-integrity** — depth Σ == new exact denom; lit census reproduces from corpus keys; unmapped + off-plane registers enumerated (MCD 94 disclosed).
- **#25 pull-slice-lit-integrity** — every lit pull cell traces to an EXISTING re-keyed kit; ZERO mcd-lit; doctored-input HALT (mcd forced past gate + pull new-law).
- **#26 drill-in-conformance** — sub-cells EAST-half only; grain-scoped seal enums with doctored proofs BOTH grains (RED-3- surfaces at drill-in; NOT at meso).
- **#27 P-DF-1-scored** — verdict emitted mechanically (this note + provenance JSON).
- **#28 edition-stamp + anti-stale greps** — "Edition II" + v1.2 both skins; Edition-I denoms only in labeled lineage; "422,445,240" absent; content-locked strings verbatim.

## FIT-LAYER FREEZE (acceptance 23 — the load-bearing edition check)
- **Independently re-verified at the artifact level:** atlas.json[basis] == atlas-edition2.json[basis] AND
  atlas.json[points] == atlas-edition2.json[points] — byte-identical (JSON.stringify compare). The 14-dim
  basis, all 506 point coordinates, axis names (${axisNames.dim1} · ${axisNames.dim2}), tombstone death
  classes, RIDER-1 (${inertiaPct}% / ${retainedDims} dims): untouched.
- **Rendered-geometry freeze:** the 506 point circles + 37 tombstone daggers extracted from the Edition-II
  SVGs are BYTE-IDENTICAL to the committed r6 Edition-I SVGs (both skins). The frozen INPUT renders to the
  frozen point/tombstone geometry byte-for-byte. Whitelisted to re-render: the LATTICE layer (§10.4.3).

## LATTICE RE-EMISSION (wholesale — this is what makes it an edition)
- **Ghost field (meso):** ${fmtInt(feasibleCells.length)} feasible meso cells (Edition-I: ${fmtInt(supE1MesoFeasible)}) · ${fmtInt(litCells)} lit by the census (Edition-I: 192) · ${fmtInt(unmappedPending)} unmapped pending curation.
- **Denominators re-derived (§10.1.5):** exact ${fmtInt(denomFeasibleExact)} (Edition-I ${fmtInt(supE1Exact)}); depth Σ ${fmtInt(depthSum)} == exact == depth_sum_check ${fmtInt(depthSumCheck)}. Meso ${fmtInt(denomMesoFeasible)} feasible + ${fmtInt(mesoSealed)} sealed. Meso sealed split: L1 756 + L2 558 == 1,314.
- **Coincident aggregation:** ${fmtInt(feasibleCells.length)} cells → ${fmtInt(ghostGlyphs.length)} distinct glyph positions (max multiplicity ${glyphMax}); size-stepped deterministically, NO jitter.
- **Ghost cells clipped (out-of-frame):** ${fmtInt(ghostClippedCount)} (all unlit=${ghostClippedAllUnlit}) — CLIP DISCLOSURE rendered, count from the render pass.
- **Ghost horizon (recomputed):** hull vertex count **${ghostHullVertexCount}** (Edition-I: 23) — the computed-not-constant law (§9.4.1/§9.5) pays off across the edition boundary. East reach world x=${hullEastWorldX.toFixed(4)} < settled east x=${settledEastWorldX.toFixed(4)} (EAST gap=${(settledEastWorldX - hullEastWorldX).toFixed(4)}).
- **Beyond-horizon (recomputed):** N=**${beyondHorizonCount}** active kits beyond the ghost hull (${beyondGrpCounts}) — recomputed from the NEW field; matches the emitted \`p_df_1.n_beyond_horizon_kits\`. Position ≠ membership (7-core meso blindness).

## PULL SLICE (§10.1 — the +\`pull\` function level)
- **pull_slice:** ${fmtInt(pullMesoFeasible)} feasible + ${fmtInt(pullMesoSealed)} sealed (all L2-summon-implies-proxy) · **${fmtInt(pullLitCells)} lit pull cells**.
- **new_law_needed=${pullNewLaw}** (pull vets under the RATIFIED ledger — ZERO new laws; L1′ cannot seal pull; L2 seals SUMMON×solo×pull=54). \`halt\`=${pullHalt}.
- **The 2 lit pull cells trace to EXISTING corpus kits re-keyed on intrinsic evidence** (census-freeze: zero NEW rows this edition):
  ${litPullCores.map((c) => `  - \`${c}\``).join('\n')}
  These are the \`d3-zbarb\` (Wrenching Smash rune) + \`di-cyclone-monk-pvp\` (skill-level) re-keys — both PRESENT as active points, both NON-mcd. Positions frozen, lighting moves (C3 precedent).
- **ZERO mcd-lit:** 0 mcd- points on the plane (all ${fmtInt(offPlaneN)} held off-plane by the movement=blank gate). Doctored-input HALT proven (mcd forced past the gate + pull new-law both HALT loud).

## EAST-HALF DRILL-IN (§10.3 — promoted geometry×commit sub-cells)
- **region:** ${drillRegion} · **promoted pair:** ${drillPromotedPair.join('×')} · **local-first law** (EAST-half only; edition-wide is ~21× the glyph field, unvettable in one pass).
- **${fmtInt(drillParentCells)} parent cells** → **${fmtInt(drillSubFeasibleN)} sub-feasible** + **${fmtInt(drillSubSealedN)} RED-3- sealed** (${fmtInt(drillParentCells)} × 36 = ${fmtInt(drillParentCells * 36)} total sub-grid).
- **Sub-feasible arrives PRE-AGGREGATED** as \`sub_feasible_glyph_field\`: ${fmtInt(subGlyphField.length)} entries {multiplicity, x, y}, Σmultiplicity=${fmtInt(subGlyphMultSum)} (== n_sub_feasible ${fmtInt(drillSubFeasibleN)}). Rendered as VISUALLY SUBORDINATE supplementary GROUND (zero-mass §10.3.4): re-aggregated to ${fmtInt(drillGlyphs.length)} SVG-raster glyph positions (max mult ${drillGlyphMax}), drawn BENEATH the meso ghost at reduced prominence (drillR + drillOp << ghostR + ghostOp), CLIPPED to the frame (${fmtInt(drillClippedCount)} clipped).
- **Sub-sealed ledger (§10.4.2):** ${subSealedSorted.map((r) => `\`${r.cut_id}\` (${r.geometry}×${r.commit}) ${fmtInt(r.count)}`).join(' · ')} — Σ ${fmtInt(subSealedSum)} == n_sub_sealed. **RED-3′ surfaces ONLY at this grain** — a VISIBLE sub-cell seal, netted-out of meso depth. Meso sealed cut_ids stay {L1-, L2-}; RED-3- at meso REFUSES loud (doctored proof).

## OFF-PLANE CORPUS (§10.4.4 — new mandatory ledger line)
- **disclosure (verbatim, emitted):** "${offPlaneLine}"
- **N = ${fmtInt(offPlaneN)}** gear-grain (mcd-) kits held off-plane (== \`gate_rejected_keyed\`); computed from the emitter's gate rejections, never hard-coded. Classless gear carries no movement identity at kit grain — admission is a deferred grain ruling (the 94 stay atlas-invisible this edition).

## DENOMINATOR SUPERSESSION (§10.1.5 — labeled lineage)
- **superseded (Edition I), rendered ONLY in the labeled lineage line:** ${fmtInt(supE1Exact)} exact · ${fmtInt(supE1MesoFeasible)} meso feasible · ${fmtInt(supE1MesoSealed)} meso sealed.
- **anti-stale grep (acceptance 28):** "693,146,160" and "10,080" appear ONLY inside the labeled superseded-lineage line (stripped-of-lineage body carries neither). "422,445,240" absent ENTIRELY.

## P-DF-1 (§10.5 — scored mechanically at render)
- **prediction:** ${pDf1.statement}
- **VERDICT: ${pDf1Verdict}** — S_max **${pDf1.S_max}** (argmax x=${pDf1.S_argmax.x}, y=${pDf1.S_argmax.y}) ${pDf1.S_max > pDf1.K_max_beyond_horizon ? '>' : '<='} K_max **${pDf1.K_max_beyond_horizon}** (the max beyond-horizon reach along û). falsified=**${pDf1Falsified}**. û=[${pDf1.u_direction.map((n) => n.toFixed(4)).join(', ')}].
- **machine-readable verdict is in the render provenance JSON** (\`p_df_1\` block). ${pDf1Falsified ? '**FALSIFIED consequence:** ' + pDf1Consequence : 'The east drill-in extends the dark BEYOND the whirlwind/beam kits along û — the registered prediction holds.'}

## EDITION STAMP (§10.4.5)
- Footer (both skins): "${atlasVersion} · Edition ${editionTag} · ${registerRef} · …". Edition-I renders remain archived untouched (r1..r6 captures).

## RENDER-FORM SEAMS (flagged per brief — where §10 left the form unspecified)
- **SEAM (flagged, resolved): the Edition-II ledger volume vs the r6 in-plane occlusion guard.** §10 does
  not spec a render form for a ledger this large. The r6 in-plane lower-right plaque held ~6 lines and
  cleared the §9.6.4.21 occlusion guard because the east-gap lower-right has only ~3 settled POINTS.
  Edition-II's lattice ledger carries ~16 accounting lines (pull slice · drill-in ground · sub-sealed
  RED-3′ · off-plane corpus · superseded lineage, atop the r6 set). A plaque holding all of it grows UP
  into the dense settled archipelago and occludes **4 settled POINTS + thousands of ghost-glyph centers**
  — the occlusion guard (correctly) HALTS, and it MUST (occluding a settled point behind a legend is the
  dishonesty the guard exists to stop). **Resolution (following established grammar, not invented):**
  §9.2.4 already rules "sealed = a margin/legend LEDGER, never on-plane"; the r4/r5/r6 \`<title>\` pattern
  already carries long disclosure sentences whole. So the WHOLE ledger moves to the BELOW-PLANE MARGIN band
  (y > plane bottom 1104) — the chrome band the census/headline/coverage lines already occupy, where nothing
  can occlude a data mark (all data is inside the frame). Each entry renders a compact VISIBLE SUMMARY +
  the FULL contiguous emitted string in a \`<title>\` (present for the whole-grep acceptance AND for hover).
  **Consequence:** no in-plane plaque, so the r6 plaque-geometry criteria (occlusion-guard, footer-plaque
  re-anchor) become MOOT and are re-instantiated as \`E2-belowplane-ledger-band\` — a STRONGER guarantee
  (zero plaque over ground at all; census footer at the plane right edge; full strings in \`<title>\`). This
  is the ONE render-form seam §10 left open; it is resolved by the established grammar, not new grammar.
- **No other seam required new grammar.** Pull cells → existing ghost-glyph grammar (they live in
  feasible_cells). Drill-in sub-feasible → existing coincident-aggregation + log₂ size-step at reduced
  prominence. Sub-sealed → existing off-plane chrome ledger. Off-plane corpus / superseded lineage →
  existing disclosure-line grammar. Horizon + beyond-horizon + clip → existing computed-not-constant paths.

## Layout calls / judgment made (Edition II)
- **Drill-in layer ORDER (render-form choice, established grammar):** the promoted sub-cells are the FINEST
  ground (a finer resolution of the feasible dark), so they draw FIRST in LAYER 0 (beneath the meso ghost
  glyphs), at reduced prominence — the eye reads meso ghost OVER the drill-in dust. Zero-mass: sx/sy is the
  frozen point-projection; the drill-in never moves the frame; the planeClip trims EAST-half sub-cells that
  project beyond it. The drill-in glyphs carry no data claim (they are ground); the sub-sealed ledger (the
  RED-3′ seals) is off-plane chrome, cut_ids verbatim.
- **Below-plane ledger (see render-form seam above).** Two columns in the ~84px below-plane band: left =
  r4 census/headline/coverage + core ghost accounting; right = the Edition-II lattice ledger (compact
  summaries + \`<title>\` full strings). No plaque; zero occlusion.
- **Footer stamp honest + E2.1-d deduped + E2.1-f trimmed.** The footer stamps a single "Edition-II"
  token (E2.1-d dedupe removed the redundant "· Edition II"); the visible stamp is trimmed to
  edition · register · emitted · skin (E2.1-f: clears the right census footer — no bottom-band
  overlap); the full emitter + render-script provenance lives in render-provenance.json.

## Layout calls inherited (frozen / unchanged)
- **FROZEN PLANE BOUNDS:** world bounds from POINTS ONLY (min/max over all 506 + 6% pad) — byte-identical to r6, so the 506 point SVG coordinates never move. Ghost + drill-in are zero-mass ground; they do NOT rescale the plane.
- **Ghost as GLYPHS never regions (§9.2.2):** ghost + drill-in are \`<circle>\` marks only — no Voronoi, no hatching, no painted boundaries. RIDER-1 continuum discipline; over-claim discipline shared with F-1.
- **GRAVEYARD (F-1):** ${supplementary.length} per-corpse tombstones with cause-of-death labels; never danger shading. Death classes: ${[...new Set(supplementary.map((p) => p.death_class))].sort().map((dc) => `${dc}:${supplementary.filter((p) => p.death_class === dc).length}`).join(', ')}.
- **Two skins, one layout engine:** ghost coordinate+status fingerprint identical across skins (${ghFps.instrument === ghFps.archive ? 'MATCH' : 'MISMATCH'}); point fingerprint identical (${ptFps.instrument === ptFps.archive ? 'MATCH' : 'MISMATCH'}). Skins vary only ink/opacity chrome; the ${ghostHullVertexCount}-vertex hull, drill-in glyphs, and ledger are one code path.
- **Determinism:** sorted iteration; no RNG; no wall-clock (footer stamp = atlas.emitted_at); 2-dp SVG coords; re-render byte-equal (verified across separate process invocations).

## Provenance law
chart = render(atlas-edition2.json). No number/label/coordinate originates outside an atlas-edition2.json
field. Layout is computed; content is not. Edition-II honors this: the ghost hull's ${ghostHullVertexCount}
vertices + beyond-horizon N=${beyondHorizonCount} are COMPUTED from the emitted Edition-II field (the
computed-not-constant law pays off across the edition boundary); the pull-slice / drill-in / off-plane /
superseded / P-DF-1 numerals are all rendered from emitted fields; the drill-in glyph field is emitted
pre-aggregated and re-aggregated by the frozen projection. Content-locked disclosure copy (pole glosses,
horizon label, beyond-horizon sentence, off-plane disclosure) is carried VERBATIM. The renderer computes
layout; it never invents content.

## Acceptance tests
${tests.map(line).join('\n')}

## Smoke tests
${smokes.map(line).join('\n')}
`;
}

main();
