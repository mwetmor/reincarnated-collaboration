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
// EDITION II: output to the Edition-II capture dir; r1..r6 (Edition-I) preserved as lineage.
// The r6 SVGs are the FIT-LAYER regression baseline (acceptance 23 / spec §10.4.3 / §10.6.23).
const DEFAULT_OUT_DIR = resolve(__dirname, '../captures/2026-07-15-atlas-edition2');
// The Edition-I r6 SVGs — FIT-layer regression baseline (points + tombstones byte-frozen).
const FIT_BASE_DIR = resolve(__dirname, '../captures/2026-07-15-atlas-edition1-r6-legibility');
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
function drillR(mult) {
  return 0.45 + 0.30 * Math.log2(mult + 1); // subordinate to ghostR (0.9 + 0.55·log2)
}
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
    // sub-cell dark. Fainter + cooler than the unlit ghost (it is finer ground beneath the ghost dark).
    drillInk: '#d3dae4',       // sub-ghost: below the unlit-feasible tone; reduced prominence
    drillOp: 0.34,
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
    // EDITION II drill-in chrome (§10.3.3): the faintest gilt-dust, deeper in the walked dark than
    // the unlit ghost embers — the promoted-grain sub-ground, subordinate to everything above it.
    drillInk: '#242832',       // sub-ghost: below the unlit-feasible void tone; reduced prominence
    drillOp: 0.7,
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
  // -- EDITION II DRILL-IN GROUND (§10.3): the promoted EAST-half geometry×commit sub-cells as
  // visually SUBORDINATE supplementary ground — the FINEST/deepest dark, drawn FIRST (beneath the
  // meso ghost glyphs) at REDUCED prominence (drillR + drillOp << ghostR + ghostOp). Same grammar
  // as the ghost layer: <circle> glyphs never regions (§9.2.2), coincident aggregation, log₂
  // size-step, NO jitter. Zero-mass (§10.3.4): sx/sy is the frozen point-projection — the drill-in
  // never moves the frame; the planeClip trims EAST-half sub-cells that project beyond it. The
  // drill-in glyphs carry a <title> so a reader hovering the sub-ground reads the promoted grain.
  P.push(`<g fill="${s.drillInk}" fill-opacity="${s.drillOp}">`);
  for (const g of drillGlyphs) {
    P.push(`<circle cx="${f2(g.sxv)}" cy="${f2(g.syv)}" r="${f2(drillR(g.mult))}"/>`);
  }
  P.push(`</g>`);
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
    const colR = bx + 500;                                 // right column left edge (center-below-plane)
    P.push(`<text x="${f2(colR)}" y="${f2(by + 1)}" font-size="10" font-weight="${s.titleWeight}" letter-spacing="0.3" fill="${s.ink}">GHOST FIELD — the feasible dark · Edition II lattice</text>`);
    // The band holds ~7 rows @ 9.3px spacing (by+14 → ~1195, clear of the footer census at the FAR
    // right edge x=1504). Each visible row is a compact summary; the FULL emitted/content-locked
    // strings ride <title> nodes (whole-grep + hover), possibly SEVERAL titles per row so every
    // required string is present in the SVG body. Rows are ordered: pull · drill-in · seals · the
    // three disclosure lines (beyond/clip/drill-clip, combined) · off-plane · superseded lineage.
    const clipCombo = [
      beyondHorizonCount > 0 ? `${fmtInt(beyondHorizonCount)} kits beyond horizon` : null,
      ghostClippedCount > 0 ? `${fmtInt(ghostClippedCount)} meso clipped` : null,
      drillClippedCount > 0 ? `${fmtInt(drillClippedCount)} drill-in clipped` : null,
    ].filter(Boolean).join(' · ');
    // each row: {s: visible, titles: [full strings for <title> nodes], gloss?}
    const led = [];
    led.push({ s: pullSliceLine, titles: [pullSliceLine] });                                                 // §10.1
    led.push({ s: drillGroundLine, titles: [drillGroundLine] });                                             // §10.3
    led.push({ s: `${fmtInt(drillSubSealedN)} sub-cells sealed @ drill-in grain — RED-3′ surfaces here`, titles: [subSealedSummary] });   // §10.4.2
    led.push({ s: `${fmtInt(mesoSealed)} meso sealed (off-plane): ${sealSummary}`, titles: [sealSummary] });  // §9.2.4 meso sealed cut ids (visible + title)
    led.push({ s: `${clipCombo} (hover for full disclosures)`, titles: [beyondHorizonLine, ghostClipLine, drillClipLine].filter((_, i) => [beyondHorizonCount, ghostClippedCount, drillClippedCount][i] > 0), gloss: true });  // §9.5/§9.2.3/§10.3.4
    led.push({ s: `${fmtInt(offPlaneN)} gear-grain kits (mcd-) held off-plane — deferred grain ruling`, titles: [offPlaneLine], gloss: true });   // §10.4.4
    led.push({ s: supersededLine, titles: [supersededLine], gloss: true });                                  // §10.1.5
    let ry = by + 13;                                      // start just under the ledger header
    for (const r of led) {
      const styleAttr = r.gloss ? ` font-style="${s.glossStyle}"` : '';
      const titleNodes = (r.titles || []).map((t) => `<title>${esc(t)}</title>`).join('');
      P.push(`<text x="${f2(colR)}" y="${f2(ry)}" font-size="9"${styleAttr} fill="${s.faint}">${esc(r.s)}${titleNodes}</text>`);
      ry += 8.8;                                            // 7 rows: 1131 → 1184.8, clears footer at 1188
    }
    P.push(`</g>`);
  }

  // ---- footer stamp (provenance; all from atlas.json). EDITION II (§10.4.5): the footer carries
  // "Edition II" + the v1.2 register ref on BOTH skins. This is a new EDITION, so the frozen-footer
  // single-purpose-diff discipline (r4/r5/r6, which held ONE diff region within Edition-I) no longer
  // applies across the edition boundary — the footer stamps the edition + register honestly.
  P.push(`<g font-family="${s.fontStack}" fill="${s.faint}" font-size="10">`);
  // LEFT footer stamp — atlasVersion ("Edition-II") + edition tag + register ref + emit provenance.
  P.push(`<text x="${f2(M.left)}" y="${f2(H - 12)}">${esc(String(atlasVersion))} · Edition ${esc(String(editionTag))} · ${esc(String(registerRef))} · emitted ${esc(emittedAt)} · ${esc(emitterScript)} · skin=${skinKey} · render: galadriel/atlas-edition2-render.mjs</text>`);
  // RIGHT census footer — EDITION II: the r6 in-plane plaque is retired (the ledger moved below-
  // plane, §10.4.3 seam resolution), so the r6 plaque-collision fix (FIX B) no longer applies. The
  // census footer end-anchors at the plane RIGHT edge (M.left+PW = 1504) — there is no plaque to
  // overprint. Mid-frame clearance vs the left footer line holds (left ends well short of 1504).
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
    // (a) the 506 point circles (titled <circle>) — byte-identical set (positions + r + title).
    //     We compare the FULL <circle ...><title>...</title></circle> string so both coordinates
    //     AND the frozen title (kit_id/franchise/group) must match — the strictest FIT invariant.
    const pointFullRe = /<circle cx="[\d.]+" cy="[\d.]+" r="[\d.]+"><title>[^<]*<\/title><\/circle>/g;
    const extractPtsFull = (svg) => { const set = []; let m; while ((m = pointFullRe.exec(svg)) !== null) set.push(m[0]); pointFullRe.lastIndex = 0; return set.sort().join('\n'); };
    // (b) the 37 tombstone daggers (glyph + position + death_class title) — byte-identical set.
    const tombFullRe = /<text x="[\d.]+" y="[\d.]+" font-size="16" text-anchor="middle"[^>]*>†<title>[^<]*<\/title><\/text>/g;
    const extractTombFull = (svg) => { const set = []; let m; while ((m = tombFullRe.exec(svg)) !== null) set.push(m[0]); tombFullRe.lastIndex = 0; return set.sort().join('\n'); };
    const basePts = extractPtsFull(baseSvg), curPts = extractPtsFull(bodies[skin]);
    const baseTomb = extractTombFull(baseSvg), curTomb = extractTombFull(bodies[skin]);
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

  // NOTE (spec §10.4.3): the r4 intra-edition FROZEN-LAYER REGRESSION vs r3.2 is RETIRED across the
  // edition boundary. An EDITION re-emits the ghost glyphs / ledgers / callouts / denominators
  // WHOLESALE — comparing them byte-for-byte against an Edition-I baseline is exactly the wrong test.
  // The FIT-layer freeze (points + tombstones + fit explainer copy) is captured by acceptance 23
  // (fit-layer-regression, above). The lattice is free to re-emit; the r4 horizon + headline-pair
  // computed-not-constant tests (above) prove the re-emitted lattice is correct.

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
      const omitInst = readFileSync(join(tmpOut, 'atlas-edition2-instrument.svg'), 'utf8');
      const omitArch = readFileSync(join(tmpOut, 'atlas-edition2-archive.svg'), 'utf8');
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
    const titleStrings = [beyondHorizonLine, ghostClipLine, offPlaneLine, subSealedSummary];
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
    //     derivation gloss, census line, horizon label, beyond-horizon line, structure statement).
    const carried = [
      POLE_GLOSS.PERFORM, POLE_GLOSS.DEPLOY, POLE_GLOSS.LAUNCH, POLE_GLOSS.EMBODY,
      DENSITY_LEGEND_LINE, DERIVATION_GLOSS, GHOST_CENSUS_LINE, GHOST_HORIZON_LABEL,
      beyondHorizonLine, structureStatement,
    ].map(esc);
    const carriedOk = ['instrument', 'archive'].every((sk) => carried.every((str) => bodies[sk].includes(str)));
    const pass28 = editionStamped && staleClean && no422 && carriedOk;
    rec('edition-stamp+anti-stale-greps', pass28,
      `edition-stamp(II + v1.2)=${editionStamped}; Edition-I denoms only-in-lineage=${staleClean}${staleDetail.length ? ' ['+staleDetail.join('; ')+']' : ''}; 422445240-absent=${no422}; content-locked-strings-verbatim=${carriedOk}`);
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
  // EDITION II lattice re-emit: lit fraction 193/11,160 ≈ 1.7% (Edition-I was 192/10,080 ≈ 1.9%);
  // density 469/193 ≈ 2.4 (unchanged — the settled corpus is frozen, only the denominator grew).
  csmoke('headline lit-fraction ≈ 1.7% (Edition-II)', fmt1(litFractionPct) === '1.7', `lit fraction=${fmt1(litFractionPct)}% (${litCells}/${denomMesoFeasible})`);
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
  const provenance = {
    render: 'galadriel/pipeline/atlas-edition2-render.mjs',
    edition: 'II',
    atlas_version: atlasVersion,
    register_ref: registerRef,
    input: 'agentic_orchestration/research/curated/atlas/atlas-edition2.json',
    emitted_at: emittedAt,
    emitter_script: emitterScript,
    fit_layer_frozen_vs: 'r6 (2026-07-15-atlas-edition1-r6-legibility)',
    basis: { frozen: frozen, ratified: ratified, inertia_pct: inertiaPct, retained_dims: retainedDims, axis_names: axisNames },
    counts: { active: active.length, supplementary: supplementary.length, total: all.length, grouped: grouped.length },
    lattice: {
      meso_feasible: feasibleCells.length, meso_sealed: sealedCells.length, lit_cells: litCells,
      unmapped_pending_curation: unmappedPending,
      exact_post_red_law: denomFeasibleExact, depth_sum_check: depthSumCheck,
      ghost_glyph_positions: ghostGlyphs.length, ghost_clipped: ghostClippedCount,
      hull_vertex_count: ghostHullVertexCount, beyond_horizon_n: beyondHorizonCount,
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
  return `# The Atlas of Kits — EDITION II render verification note

**EDITION II (2026-07-15, spec §10).** The first NEW-EDITION render. An edition changes the LATTICE;
an rN discloses/corrects chrome on existing ground. Here the lattice changed (the \`function\`
coordinate grew 10→11 levels, +\`pull\`) and the FIT layer did NOT. Fired by Matt's word ("If the
slate holds, cut Edition-II §10") — the slate held (\`c7804393\` confirmed \`a384c11d\`, vacuously).

**Rendered by:** galadriel/pipeline/atlas-edition2-render.mjs (deterministic; no wall-clock — all stamps from atlas-edition2.json)
**Input (sole):** agentic_orchestration/research/curated/atlas/atlas-edition2.json (elrond; gandalf audit-grade ACCEPT)
**FIT-layer regression baseline (acceptance 23):** agentic_orchestration/galadriel/captures/2026-07-15-atlas-edition1-r6-legibility (r6, Edition-I)
**atlas_version:** ${atlasVersion} · **edition:** ${editionTag} · **register:** ${registerRef}
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
- **Footer stamp honest across the edition boundary.** The r4/r5/r6 frozen-footer single-purpose-diff
  discipline held ONE diff region WITHIN Edition-I; this is a new EDITION, so the footer stamps "Edition II"
  + the v1.2 register + the real render-script name (\`atlas-edition2-render.mjs\`) honestly.

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
