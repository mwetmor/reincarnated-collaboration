// atlas-refit-candidate-1-render.mjs — REFIT CANDIDATE 1 · UNRATIFIED COMPARISON ARTIFACT (Matt 2026-07-16
// "I want to see both versions so we cna make a decision."; gandalf brief
// 2026-07-16-galadriel-a-render-refit-candidate-plates-brief.md). Fork of the FINAL FIXED r8-furniture head
// (atlas-edition3-r8-furniture-render.mjs 944afa98). This is NOT an Edition — it is a COMPARISON plate for
// Matt's Tier-3 atlas refit adoption decision (Refit Candidate 1 vs served Edition III). Title: "Build
// Horizon — Refit Candidate 1". The strings "Edition IV"/"edition4" appear NOWHERE; "Edition III" appears
// ONLY in the emitted_alongside provenance line, never as this plate's own identity. FURNITURE (the FURN
// table, key/ledger forms, skins) is byte-verbatim from the r8 head — Matt compares STRUCTURE, not
// presentation. The data is a FULL RE-DERIVATION of the atlas FIT on the current 628-active corpus (sole
// input atlas-refit-candidate-1.json; elrond addendum da992f78, gandalf artifact-level verify green). The
// emitted coordinates are plane-ALIGNED to Edition-I orientation (in-plane orthogonal Procrustes,
// rotation+reflection, no scaling; det=-1, rotation=-117.3477deg) — DISCLOSED on-plate per the verify-gate
// ruling. Pole titles render as Edition-I REFERENCE orientation labels (the refit basis carries NO ratified
// axis names) + a gloss "poles = Edition-I reference orientation; refit axes unratified". Per-axis inertia is
// NOT rendered (aligned x/y are not pure dims 1/2); the plane-level 8.903% figure is fine (subspace-invariant).
// Acceptance adapted per the brief: frozen-baseline checks RETIRED (a NEW fit has no freeze baseline);
// internal-consistency checks RE-POINTED to this emission's own counts (fail-loud); hull/census/P-DF-1
// RECOMPUTED + CROSS-CHECKED vs the emitted ghost_field.p_df_1 (mismatch = HALT, never tolerate); the
// Edition-I orientation smokes DEMOTED to REPORTED observations (print refit value + old expectation +
// PASS/CHANGED, do not gate). Edition III + every served artifact are READ-ONLY. NO push; NOT vendored.
//
// ---- ORIGINAL r8-furniture head banner (retained for lineage; the census/lattice logic below is that
//      head's, verbatim — this fork changes ONLY the identity/acceptance-adaptation seams named above) ----
// atlas-edition3-r8-furniture-render.mjs — EDITION III · r8 FURNITURE RESCALE (Matt 2026-07-16, gandalf
// brief 2026-07-16-galadriel-b1-furniture-rescale-brief.md). Fork of atlas-edition3-render.mjs. D7 made
// /atlas fluid: the 1600×1200 plate now displays at ~2528px (scale ≈1.58, was ≈0.62 under the old 1024px
// clamp), so every furniture element renders poster-sized. Matt: "the legends/descriptive sections/title/
// axis-title/axis itself are all still set to fill the 'box' that has now grown … they need to fit the box
// as it is now" + "the condensations box should be re-named to 'Build Families'". r8 DIFF vs the Edition-III
// head (FURNITURE ONLY — DATA GEOMETRY BYTE-FROZEN; every point mark cx/cy/r + <title>, the † tombstones at
// font-size 16, the hull polyline, ghost/drill glyph circles, zero-axis + frame geometry are UNTOUCHED, and
// the script's FIT/regression/overlap acceptance blocks 23/29/30/E2.x still PASS): (r8-A) a single FURN
// furniture-factor table drives every chrome font-size + its box/pitch metrics; (r8-B) title 26→17.5, RIDER
// banner 13→8.5 + band 30→20, deriv gloss 11→7.5; (r8-C) pole rail/strip titles 15/12.5→9.5, pole glosses
// 10.5→7, horizon label 10→7; (r8-D) BUILD-FAMILIES key (renamed from CONDENSATIONS) header/rows 11→8, gloss
// 9.5→6.5, swatch 4.6→3.4, pitch 18→13, box 196→158 hugging content; (r8-E) GRAVEYARD legend header 11→7.5,
// rows 11/10→7, pitch 15→10.5, box 230→158, bottom-anchored; (r8-F) centroid anchor plaques 12→8.5 + rect
// hugs (connector line + anchor point UNCHANGED); (r8-G) below-plane ledger left/right columns shrunk (12.5/
// 11/10.5/9.5/9→8.5/7.5/7/6.5; right 9.5/7.5→6.5/6) — baselines kept, footer census at y=1188 byte-frozen;
// (r8-H) footer group 10→7 (baselines+content byte-frozen); (r8-I) DEFAULT_OUT_DIR → the r8-furniture folder;
// (r8-J) provenance render-stamp + note re-headed r8-furniture. NO data-mark byte diff (proven by acc-23/29).
// Below: the carried Edition-III identity block, VERBATIM (the census/lattice + all acceptance logic are the
// Edition-III head's; r8 changes ONLY the render head's chrome sizing).
//
// atlas-edition3-render.mjs — EDITION III. Byte-copy of the E2.3 head (atlas-edition2-e23-render.mjs)
// with ONLY the edition-boundary diff (gandalf brief 2026-07-16-galadriel-edition3-render-brief.md;
// Matt 2026-07-16 verbatim "(a) - ratify Edition III now" + "Agreed. Ratify Edition III"). An EDITION
// changes the CENSUS/LATTICE; the FIT layer (basis + 506 point coords + tombstones + axis names) is
// BYTE-FROZEN across the I→II→III boundary (elrond asserted it Stage D; re-asserted renderer-side here,
// fail-loud — atlas-edition3.json[basis|points] ≡ atlas-edition2.json[basis|points]). Edition-III is a
// CENSUS-POPULATION edition: +65 corpus rows (Stage A pull-7 re-insertion + Stage B Lost Ark 58 at
// class-engraving grain) PROJECT into the frozen basis (no basis re-derivation). Lit occupancy grew:
// occupied meso 193→202, pull-lit 2→4. Denominators BYTE-IDENTICAL to v1.2 (lattice did not move; register
// v1.3 RE-ASSERTS the v1.2 numbers, not supersedes). ENUMERATED DIFF vs the E2.3 head (every diverging
// site; each carries a one-line why in-place): (1) header identity banner [this block]; (2) ATLAS_PATH →
// atlas-edition3.json; (3) DEFAULT_OUT_DIR → captures/2026-07-16-atlas-edition3; (4) L344-vicinity register
// fail-loud gate re-bound v1.2 → v1.3; (5) ghost-ledger header literal "Edition II lattice" → "Edition III
// lattice"; (6) output filenames atlas-edition2-<skin> → atlas-edition3-<skin>; (7) acceptance edition-stamp
// grep + edition-token dedupe regex re-targeted Edition II/v1.2 → Edition III/v1.3 with anti-substring care;
// (8) integrity-check + doctored-halt messages atlas-edition2.json → atlas-edition3.json; (9) lit-fraction +
// density smokes RE-DERIVED from the emission's own counts (1.7%→1.8% [202/11160]; 2.4→2.3 [469/202]) — not
// carried; (10) FIT-layer data-level byte-frozen re-assert gate ADDED (fail-loud); (11) 819,439,740 anti-stale
// grep ADDED (the emission's exact_post_logical raw number MUST NOT surface in any rendered body); (12)
// provenance JSON + verification-note identity re-headed to Edition III. The title plate ("Build Horizon —
// Edition ${editionTag}"), the RIDER banner ("Edition ${editionTag} lattice …"), and the footer stamp
// (${atlasVersion}) are ALREADY data-derived (editionTag = ghost_field.edition = "III"; atlasVersion =
// atlas_version = "Edition-III") — they auto-move at the boundary with NO source change (§4c). The census
// overlay + all headline/coverage/pull/drill/off-plane/denominator numbers are data-derived and auto-update.
// GHOST HORIZON envelope + re-led HEADLINE COVERAGE PAIR + BEYOND-HORIZON LEDGER LINE +
// r6 CHROME LEGIBILITY CORRECTIONS, extended to Edition-III's re-emitted LATTICE:
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

import { readFileSync, writeFileSync, mkdtempSync, mkdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve, join } from 'node:path';
import { tmpdir } from 'node:os';
import { execFileSync } from 'node:child_process';
import sharp from 'sharp';

const __dirname = dirname(fileURLToPath(import.meta.url));
// REFIT CANDIDATE 1 (input): the SOLE data source is atlas-refit-candidate-1.json (elrond addendum
// da992f78, ALIGNED re-emission; gandalf artifact-level verify green). This is a FULL RE-DERIVATION of the
// FIT on the 628-active corpus — NOT byte-frozen vs any prior edition (that is the whole point of a
// candidate). Edition III (served truth) + Edition I/II stay BYTE-UNTOUCHED and READ-ONLY. The fit-freeze
// re-assert vs a prior edition is RETIRED below (a new fit has no freeze baseline).
const ATLAS_PATH = resolve(__dirname, '../../research/curated/atlas/atlas-refit-candidate-1.json');
// REFIT CANDIDATE 1 (output): write to the candidate comparison-plate capture dir. This head is a fork of
// the FINAL FIXED r8-furniture head (944afa98) carrying the FURN table byte-verbatim; only the
// identity/acceptance-adaptation seams differ. Edition III's captures (2026-07-16-atlas-edition3-r8-
// furniture/) are READ-ONLY — the composite reads them LEFT, this candidate RIGHT.
const DEFAULT_OUT_DIR = resolve(__dirname, '../captures/2026-07-16-atlas-refit-candidate-1');   // candidate comparison-plate folder
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
// REFIT: basis.axis_names is a {note} object on the candidate (NO ratified axis names — this is a
// comparison artifact). req() passes (non-empty object); pole titles render as Edition-I REFERENCE labels
// (literals below), never as the candidate's own ratified identities.
const axisNames = req(atlas, 'basis.axis_names', 'axis-names');
const edition = req(atlas, 'basis.edition', 'edition');   // "Refit-Candidate-1"
// REFIT (RETIRE): basis.ratified is a freeze-baseline field absent from a NEW fit. Removed. The candidate
// declares frozen:false (an unratified re-derivation) — we do NOT gate on it (the frozen!==true "refuse an
// unfrozen basis" HALT is Edition-lineage machinery; a candidate is unfrozen BY DEFINITION). We read
// `frozen` only to DISCLOSE it honestly in the unratified-framing banner.
const frozen = req(atlas, 'basis.frozen', 'frozen');   // false — disclosed, not gated

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
// REFIT (RETIRE): the Edition-I labeled-lineage supersession sub-block (superseded_edition1) is
// Edition-lineage machinery — it does NOT belong on a comparison plate and is ABSENT from the candidate
// emission. Removed (the req()s would HALT-on-load). The candidate discloses its own denominators; the
// only lineage reference on this plate is the emitted_alongside provenance line.

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

// ================================================================== REFIT CANDIDATE identity + register
// Edition + register provenance. The candidate legitimately binds the v1.3 register (its denominators are
// byte-identical to v1.3 — the refit changed the FIT layer only; the lattice cardinality did not move).
const editionTag = req(atlas, 'ghost_field.edition', 'ghost-edition');                 // "Refit-Candidate-1"
const registerRef = req(atlas, 'ghost_field.register_ref', 'ghost-register');          // feasibility-cuts-register-v1.3
// Register gate KEPT fail-loud (candidate binds v1.3; a drift here is still a finding).
if (String(registerRef) !== 'feasibility-cuts-register-v1.3')
  die(`ghost_field.register_ref '${registerRef}' != feasibility-cuts-register-v1.3 — the candidate binds the v1.3 register (byte-identical denominators; refit changed the FIT layer only).`);

// PLATE DISPLAY IDENTITY (the ONE law that frames everything): this is a COMPARISON plate, not an Edition.
// The human-form title token is "Refit Candidate 1" (from the emitted edition "Refit-Candidate-1", spaced +
// hyphen-normalized) — the title reads "Build Horizon — Refit Candidate 1" (NO "Edition" word). The strings
// "Edition IV"/"edition4" appear NOWHERE. "Edition III" appears ONLY in the emitted_alongside provenance
// line (below), never as this plate's own identity. These are DATA-DERIVED from the emitted fields (§4c
// law) — never renderer literals invented for copy.
const REFIT_DISPLAY = String(editionTag).replace(/-/g, ' ');   // "Refit Candidate 1"
const comparisonNote = req(atlas, 'comparison_note', 'comparison-note');
const emittedAlongside = req(atlas, 'emitted_alongside', 'emitted-alongside');
const unratifiedFlag = req(atlas, 'unratified_comparison_artifact', 'unratified-flag');
if (unratifiedFlag !== true) die(`unratified_comparison_artifact != true (got ${JSON.stringify(unratifiedFlag)}) — refuse to render a non-comparison-artifact under the candidate head. HALT.`);
const planeAlignHeadline = req(atlas, 'plane_alignment_headline', 'plane-align-headline');
const planeAlign = req(atlas, 'ghost_field.plane_alignment', 'plane-alignment');
const planeAlignRotDeg = req(atlas, 'ghost_field.plane_alignment.rotation_deg', 'plane-align-rot');   // -117.3477
const planeAlignDet = req(atlas, 'ghost_field.plane_alignment.det', 'plane-align-det');               // -1
const planeAlignMethod = req(atlas, 'ghost_field.plane_alignment.method', 'plane-align-method');
// REFIT (RETIRE): the §10.4.3 EDITION REGRESSION LAW fit-layer byte-freeze re-assert (basis|points ==
// prior edition) + the top-level edition===3 check are frozen-baseline machinery. A NEW fit has no freeze
// baseline — REMOVED. In their place we HALT-guard the comparison-artifact contract (the fields Gate 2
// promised are carried): drill_in, p_df_1, plane_alignment must all be present, and counts must be
// 628/37/665 with depth Σ == 767,411,820 (the lattice did not move). Any miss = HALT (Gate 2 not met).
// Scoped to the REAL input (!IS_DOCTORED): the computed-not-constant acceptance tests spawn CHILD renders
// with DOCTORED atlases (deliberately moved counts/fields to prove the render follows the data). Those
// must bypass this contract guard — same scoping principle as the beyond-horizon receipt-guard.
if (!IS_DOCTORED) {
  if (!('drill_in' in atlas.ghost_field)) die(`REFIT HALT: ghost_field.drill_in ABSENT — Gate 2 not actually met (aligned re-emission must carry the drill-in key set).`);
  if (!('p_df_1' in atlas.ghost_field)) die(`REFIT HALT: ghost_field.p_df_1 ABSENT — Gate 2 not actually met.`);
  if (!('plane_alignment' in atlas.ghost_field)) die(`REFIT HALT: ghost_field.plane_alignment ABSENT — Gate 2 not actually met.`);
  if (!(counts.active === 628 && counts.supplementary === 37 && counts.total === 665))
    die(`REFIT HALT: counts ${JSON.stringify(counts)} != 628 active + 37 supplementary = 665 total. HALT.`);
  if (Number(depthSumCheck) !== 767411820)
    die(`REFIT HALT: depth_sum_check ${depthSumCheck} != 767,411,820 — the lattice MOVED (must be byte-equal to the served-edition lattice). HALT.`);
  console.error(`[refit-guard] comparison-artifact contract met: drill_in+p_df_1+plane_alignment present; counts 628+37=665; depth Σ == 767,411,820 (lattice did not move); edition="${editionTag}" (display "${REFIT_DISPLAY}"); frozen=${frozen} (unratified, disclosed).`);
}

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
// REFIT (RE-POINT): the candidate carries NO top-level p_df_1_verdict mirror — the single source of truth
// is ghost_field.p_df_1.verdict. The Edition-III mirror-consistency req()+die is retired; we alias the
// "top-level" name to the single emitted verdict so downstream provenance shape is preserved honestly (the
// consistency check below is then trivially true — there is one verdict, and it is what we render).
const pDf1TopLevel = pDf1Verdict;                                                                   // single-source (no separate mirror on the candidate)
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
const ghostClippedLitCells = ghostClippedCells.filter((c) => c.lit);
const ghostClippedLitCount = ghostClippedLitCells.length;
// REFIT — the Edition-III "lit-clipped ghost = decoupling malfunction, HALT" gate is RE-POINTED, not
// retired, and NOT hard-HALTed here. Edition III freezes the frame to the Edition-I bounds; a lit cell
// outside that frozen frame WOULD be a decoupling bug. The candidate RE-DERIVES the frame from ITS OWN
// points (brief law: points-only + 6% pad; do NOT force Edition-III's bounds). A lit ghost cell landing
// just outside a points-derived+6%-pad frame is a NATURAL consequence of a re-derived fit, not an emitter
// malfunction — so we DISCLOSE it loudly (no silent transformation, no silent under-claim: the clip line
// below names the lit-clipped count explicitly, and it is surfaced as a REPORTED finding at acceptance).
// We do NOT rescale the frame (that would force a non-points-only frame). We do NOT die. We report.
if (!IS_DOCTORED && ghostClippedLitCount > 0) {
  console.error(`[refit-finding] ${ghostClippedLitCount} LIT ghost cell(s) project just beyond the candidate's own points-derived frame (points-only + 6% pad). DISCLOSED on-plate (clip line names the lit count) + surfaced as a reported observation. This is a re-derived-fit consequence, not an emitter malfunction — the frame is NOT rescaled (brief: do not force Edition-III's bounds). Cells: ${ghostClippedLitCells.map((c) => `(x=${c.x.toFixed(4)},y=${c.y.toFixed(4)},kit_count=${c.kit_count})`).join(' ')}`);
}
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
// REFIT receipt-guard — RECOMPUTE + CROSS-CHECK vs the emitted p_df_1 (the load-bearing part, brief §3).
// RETIRED: the Edition-I frozen meso-hull N==14 receipt (a NEW fit's meso-beyond N is a computed
// consequence of the re-derived corpus, not a frozen constant). REPLACED by a render-vs-emission
// CROSS-CHECK: the render pass computes beyondMesoOnlyCount (actives outside the MESO-only hull — the hull
// P-DF-1 is framed against) and it MUST EQUAL the emitted ghost_field.p_df_1.n_beyond_horizon_kits. A
// mismatch is an emission-vs-render DISAGREEMENT — a finding, not a tolerance → HALT + surface. KEPT as
// structural (not frozen-baseline) fail-loud invariants: (i) charted hull CONTAINS meso hull (charted-
// beyond N ≤ meso-beyond N); (ii) charted east reach ≥ meso east reach (drill-in pushes horizon east).
const P_DF_1_N_BEYOND_HORIZON = req(atlas, 'ghost_field.p_df_1.n_beyond_horizon_kits', 'p-df-1-n-beyond'); // 13 (emitted)
if (!IS_DOCTORED) {
  if (beyondMesoOnlyCount !== Number(P_DF_1_N_BEYOND_HORIZON)) {
    die(`REFIT HALT — render-vs-emission cross-check mismatch: render pass computed N=${beyondMesoOnlyCount} active kits beyond the MESO-only hull, but the emitted ghost_field.p_df_1.n_beyond_horizon_kits is ${P_DF_1_N_BEYOND_HORIZON} (brief §3 — emission vs render disagreement is a finding, NEVER a tolerance). Kits beyond meso: [${beyondMesoOnlyKits.map((p) => p.kit_id).join(', ')}]. HALTING.`);
  }
  if (beyondHorizonCount > beyondMesoOnlyCount) {
    die(`REFIT charted-hull containment violation: charted-beyond N=${beyondHorizonCount} > meso-beyond N=${beyondMesoOnlyCount}. The charted hull (meso ∪ drill-in) must CONTAIN the meso hull, so fewer or equal kits can be beyond it. A larger N means the union hull is malformed. HALTING.`);
  }
  if (chartedHullEastX + 1e-9 < mesoOnlyHullEastX) {
    die(`REFIT charted-horizon east-reach violation: charted east x=${chartedHullEastX.toFixed(6)} < meso east x=${mesoOnlyHullEastX.toFixed(6)}. The drill-in must push the horizon EAST, not west. HALTING.`);
  }
  console.error(`[refit-crosscheck] beyond-MESO-hull N=${beyondMesoOnlyCount} == emitted p_df_1.n_beyond_horizon_kits ${P_DF_1_N_BEYOND_HORIZON}; charted-beyond N=${beyondHorizonCount} (charted hull encloses settled archipelago); charted east x=${chartedHullEastX.toFixed(4)} > meso east x=${mesoOnlyHullEastX.toFixed(4)}.`);
}
const BEYOND_HORIZON_EXPECTED = beyondHorizonCount; // computed; asserted at acceptance
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

// REFIT clip-disclosure microcopy — count from the render pass. HONEST composition: the candidate's
// frame is re-derived from ITS points (points-only + 6% pad), so a clipped cell may be LIT; the line
// names the lit count explicitly (no false "unlit" claim, no silent under-claim). OMITTED when zero.
const ghostClipUnlitCount = ghostClippedCount - ghostClippedLitCount;
const ghostClipLine = ghostClippedLitCount > 0
  ? `${fmtInt(ghostClippedCount)} meso cell${ghostClippedCount === 1 ? '' : 's'} project beyond the candidate's own points-derived frame — ${fmtInt(ghostClippedLitCount)} LIT + ${fmtInt(ghostClipUnlitCount)} unlit (clipped, not rescaled — frame from the settled points only, per the refit's honest-frame law; the served-edition bounds are not forced here)`
  : `${fmtInt(ghostClippedCount)} unlit cell${ghostClippedCount === 1 ? '' : 's'} project beyond the frame (clipped, not rescaled — frame from the settled points only)`;

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
// REFIT BANNER RIDER string (module scope so both renderSVG and the banner acceptance test use the same
// string). LEADS with the unratified-comparison framing, then DISCLOSES the plane alignment (rotation_deg
// + det, from the emitted plane_alignment stamp — "aligned to Edition-I orientation for comparison"), then
// the plane-level corrected inertia (8.903%, subspace-invariant under Q — SAFE to render) + retained dims
// + structure statement. Per-axis inertia is NOT rendered (the aligned x/y are not pure dims 1/2). All
// values from atlas.json; "Edition IV" appears NOWHERE; the only "Edition III" on this plate is in the
// emitted_alongside provenance line below (the alignment refs "Edition-I orientation", not an edition tag).
const riderStr = `UNRATIFIED COMPARISON ARTIFACT — refit candidate (frozen=${frozen}) · plane Q-ALIGNED to Edition-I orientation (${planeAlignMethod}; rotation ${planeAlignRotDeg}°, det ${planeAlignDet}) · plane = dims 1–2, ${inertiaPct}% corrected inertia (plane-level, subspace-invariant) · retained basis: ${retainedDims} dims · ${structureStatement}`;

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
// (vi) EMITTED-ALONGSIDE PROVENANCE line (REFIT) — replaces the retired superseded-lineage line. This is
//      the ONLY on-plate place the string "Edition III" may appear (as the served-truth reference this
//      candidate was emitted alongside). Rendered VERBATIM from the emitted `emitted_alongside` field.
//      The variable name `supersededLine` is retained so the downstream render/acceptance plumbing (the
//      labeled off-plane ledger row + its anti-stale strip) rides the same slot with no structural churn.
const supersededLine = `emitted alongside: ${emittedAlongside}`;

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
// REFIT: derivation gloss re-worded HONESTLY for the candidate — a FULL re-derivation (MCA over 14
// coordinate blocks on the 628-active corpus, Greenacre-corrected, pull+MELEE un-masked as live columns),
// axes NOT ratified (this is a comparison artifact; coordinates Q-aligned to Edition-I orientation).
const DERIVATION_GLOSS = 'positions computed, not designed — full re-derivation: MCA over 14 mechanical coordinate blocks per kit (628-active corpus); axes unratified, aligned to Edition-I orientation for comparison.';

// ------------------------------------------------------------------ r3 legend text (CONTENT from emitted fields)
// REFIT: the census line re-worded HONESTLY — the candidate's ghost positions come from the REFIT basis
// (a full re-derivation), NOT the frozen Edition-I basis; the whole plane is Q-aligned to Edition-I
// orientation for comparability. (Edition III's line said "frozen Edition-I basis"; that is false here.)
const GHOST_CENSUS_LINE = 'ghost field lit from the current census; positions from the REFIT basis, aligned to Edition-I orientation.';

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

// ------------------------------------------------------------------ r8 FURNITURE RESCALE TABLE (Matt 2026-07-16)
// D7 made /atlas fluid: the 1600×1200 plate that used to display ≤1024px (scale ≈0.62) now displays
// at ~2528px (scale ≈1.58). Every furniture element scaled with the plate — title (internal 26)
// rendered ~41px, pole titles (15) ~24px, key rows (11) ~17px — poster-sized. Matt approved the box
// growth; the furniture must re-proportion for the plate at its NEW displayed size. This table is the
// SINGLE tuning surface: every furniture font-size + its box/pitch metrics derive from FURN.<class>.
// DATA GEOMETRY IS BYTE-FROZEN — this table touches ONLY chrome/furniture text + the boxes that hug it;
// no point mark cx/cy/r, no tombstone (font-size 16, untouched), no hull, no ghost/drill glyph, no
// zero-axis/frame geometry moves. Anchor/connector POSITIONS for centroid plaques stay; only text+rect
// dims shrink. The acceptance FIT/regression blocks (23/29/30, E2.x) still PASS — they read the actual
// per-<text> font-size, so re-proportioned sizes are accommodated by construction.
//
// Per-class factor (rendered@2560 target in the comment; factor = internal_new / internal_old):
//   Sizes chosen to land the TARGET rendered px at scale 1.58, tuned per-class by eye against crops,
//   with a legibility FLOOR at the 1440 viewport (scale ≈0.88) and standalone-at-1600 readability.
//   Global furniture factor lands ≈0.63–0.68 (title a touch higher so it still leads; footnotes a
//   touch lower). See the r8 verification note for the per-class rationale + crop receipts.
const FURN = {
  title:        17.5,  // 26 →17.5 (f0.673): ≈27.7px@2560 — leads the plate, no longer poster-scale
  banner:        8.5,  // 13 → 8.5 (f0.654): ≈13.4px@2560 — the RIDER rides its band comfortably
  bannerBandH:  20,    // band rect height 30→20 hugs the 8.5px banner + its baseline (y58 top kept)
  deriv:         7.5,  // 11 → 7.5 (f0.682): ≈11.9px@2560 — derivation gloss, quiet under the band
  poleTitle:     9.5,  // 15 → 9.5 (f0.633): ≈15.0px@2560 — the four rail/strip axis titles
  poleTitleLS:   1.0,  // rail title letter-spacing 1.5→1.0 (scales with the glyph so the run stays tight)
  poleGloss:     7,    // 10.5→7  (f0.667): ≈11.1px@2560 — the four pole glosses (was s.glossSize)
  launchEmbody:  9.5,  // 12.5→9.5(f0.760): ≈15.0px@2560 — LAUNCH/EMBODY titles match the rail titles
  horizonLabel:  7,    // 10 → 7  (f0.700): ≈11.1px@2560 — charted-horizon leader label + its rows
  horizonRowH:   9,    // wrapped-row pitch 12.5→9 (scales with the 7px label; rows stay disjoint)
  keyHeader:     8,    // 11 → 8  (f0.727): ≈12.6px@2560 — BUILD FAMILIES key header
  keyRow:        8,    // 11 → 8  (f0.727): ≈12.6px@2560 — key group rows
  keyGloss:      7,    // 9.5→7 (f0.737): ≈11.1px@2560 — key density gloss (2 rows). r8-fix: 6.5→7 for
                       // the 1440-viewport legibility floor (6.5 rendered ≈5.7px @0.88 — below floor);
                       // inter-gloss pitch 11 > glyph 7 stays disjoint; box height re-derives from content.
  keyRowH:      13,    // key row pitch 18→13 hugs the 8px rows (box height re-derives from this)
  keySwatchR:    3.4,  // key swatch radius 4.6→3.4 scales with the 8px row
  keyBandGloss:  7,    // key density-swatch box 10→7px scales with the gloss block
  centroid:      8.5,  // 12 → 8.5 (f0.708): ≈13.4px@2560 — on-plane condensation anchor plaque text
  centroidBandH:13,    // centroid plaque rect height 18→13 hugs the 8.5px label (position/anchor stay)
  centroidCW:    5.8,  // centroid rect width per-char 8.2→5.8 scales with the 8.5px label
  graveHeader:   7.5,  // 11 → 7.5 (f0.682): ≈11.9px@2560 — GRAVEYARD legend header
  graveRow:      7,    // 10 → 7  (f0.700): ≈11.1px@2560 — death-class rows + the † markers
  graveRowH:    10.5,  // grave row pitch 15→10.5 hugs the 7px rows (box height re-derives)
  ledgerCensus:  7,    // 10.5→7  below-plane census line
  ledgerHeadline:8.5,  // 12.5→8.5 the LEAD headline (kept a touch bigger — load-bearing)
  ledgerHl2:     7.5,  // 11 → 7.5 the density headline
  ledgerSub:     6.5,  // 9.5→6.5 coverage-secondary + feasible accounting line
  ledgerRight:   6.5,  // 9.5→6.5 right-column ghost-field header
  ledgerRow:     6,    // 7.5→6  right-column ledger rows (visible summary; full string in <title>)
  ledgerRowH:    6,    // right-column row pitch 7.3→6 (fs6 glyph≈5.5 < 6 pitch: stays disjoint)
  footer:        7,    // 10 → 7  footer provenance + census stamps (y=1188 baseline byte-frozen)
};

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
    // r8: plaque hugs the shrunken 8.5px label. The connector line (cy-12 → cy-3) + the anchor point
    // (cy) are UNCHANGED — only the rect (dims) + text (size) shrink. Rect BOTTOM stays at cy-12 (the
    // connector head); the top rises by the shrunk band height so the box hugs the text upward.
    const tw = label.length * FURN.centroidCW + 12;
    const cRectTop = cy - 12 - FURN.centroidBandH;
    P.push(`<g>`);
    P.push(`<rect x="${f2(cx - tw / 2)}" y="${f2(cRectTop)}" width="${f2(tw)}" height="${f2(FURN.centroidBandH)}" rx="3" fill="${s.plaque}" fill-opacity="0.82" stroke="${GROUP_COLORS[g]}" stroke-width="1.2"/>`);
    P.push(`<text x="${f2(cx)}" y="${f2(cRectTop + FURN.centroidBandH - 3.5)}" font-size="${FURN.centroid}" text-anchor="middle" fill="${s.ink}" letter-spacing="0.4">${esc(label)}</text>`);
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
    const rowH = FURN.horizonRowH;                    // r8: 12.5→9 (scales with the 7px label)
    const labY0 = ev.y + 90;                          // drop below the east vertex into open space (data-anchored)
    // leader: from the east hull vertex down-right to the label's first row
    P.push(`<g font-family="${s.fontStack}">`);
    P.push(`<line x1="${f2(ev.x)}" y1="${f2(ev.y)}" x2="${f2(labX - 4)}" y2="${f2(labY0 - 9)}" stroke="${s.horizonInk}" stroke-opacity="${s.horizonOp}" stroke-width="0.8" stroke-dasharray="3 3"/>`);
    P.push(`<circle cx="${f2(ev.x)}" cy="${f2(ev.y)}" r="2.1" fill="none" stroke="${s.horizonInk}" stroke-opacity="${s.horizonOp}" stroke-width="1"/>`);
    // wrapped, right-anchored rows. Each row carries a <title> with the WHOLE gloss so the label
    // block itself is greppable/hoverable as one unit too (belt-and-suspenders with the polyline).
    for (let i = 0; i < rows.length; i++) {
      const weight = i === 0 ? ' font-weight="600"' : '';
      P.push(`<text x="${f2(labX)}" y="${f2(labY0 + i * rowH)}" font-size="${FURN.horizonLabel}" font-style="${s.horizonLabelStyle}"${weight} text-anchor="end" fill="${s.horizonLabelInk}" letter-spacing="0.2">${esc(rows[i])}${i === 0 ? `<title>${esc(GHOST_HORIZON_LABEL)}</title>` : ''}</text>`);
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
  //      ("PERFORM ↓" / "↑ DEPLOY" / "↑ LAUNCH" / "EMBODY ↓") appear contiguously (a wrapped gloss
  //      carries its FULL string in a <title>, the codebase's proven wrap+grep pattern). [E2.3: the
  //      two ROTATED rail titles use ↓/↑ as SOURCE glyphs so the ON-SCREEN arrows read OUTWARD — see
  //      the rotate(-90) glyph-remap note at the PERFORM/DEPLOY <text> emitters below.]
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
  //
  // E2.3 RAIL-ARROW ORIENTATION (2026-07-16, Matt-ordered: arrows point OUTWARD, not up/down).
  // ⚠ SOURCE GLYPH ≠ ON-SCREEN DIRECTION — DO NOT "fix" this back to `→`. Under rotate(-90) in
  //   SVG (y-down; -90 is clockwise), the local text axes remap: local +x (glyph `→`) reads
  //   screen-UP; local -x (`←`) reads screen-DOWN; local -y (`↑`) reads screen-LEFT; local +y
  //   (`↓`) reads screen-RIGHT. The east/PERFORM rail must READ `→` (rightward = away from the
  //   plane), so the SOURCE glyph is `↓`. (Was `PERFORM →` in E2.2, which rendered pointing UP.)
  // REFIT POLE LABELS: the four pole titles carry the Edition-I ratified names as a REFERENCE
  // ORIENTATION (the refit basis has NO ratified axis identities of its own — brief iron law). Each
  // title is marked "(E1 ref)" so it is never read as the candidate's own ratified pole; the one
  // orientation gloss (top strip, below) states the law once for all four poles.
  P.push(`<g font-family="${s.fontStack}">`);
  P.push(`<text transform="rotate(-90 ${f2(railR - 6)} ${f2(cyMid)})" x="${f2(railR - 6)}" y="${f2(cyMid)}" text-anchor="middle" fill="${s.ink}" font-weight="${s.titleWeight}" font-size="${FURN.poleTitle}" letter-spacing="${FURN.poleTitleLS}">PERFORM ↓ (E1 ref)</text>`);
  P.push(`<text transform="rotate(-90 ${f2(railR + 9)} ${f2(cyMid)})" x="${f2(railR + 9)}" y="${f2(cyMid)}" text-anchor="middle" fill="${s.faint}" font-size="${FURN.poleGloss}" font-style="${s.glossStyle}" letter-spacing="0.2">${esc(POLE_GLOSS.PERFORM)}</text>`);
  // -- DEPLOY: left rail, rotated -90° about the rail center at cyMid. Title inner (nearer plot),
  //    gloss outer.
  // E2.3 RAIL-ARROW ORIENTATION (2026-07-16): same rotate(-90) glyph remap as PERFORM above.
  // ⚠ SOURCE GLYPH ≠ ON-SCREEN DIRECTION — DO NOT "fix" this back to `←`. The west/DEPLOY rail
  //   must READ `←` (leftward = away from the plane); under rotate(-90) the glyph that renders
  //   screen-LEFT is `↑`, so the SOURCE glyph is `↑`. (Was `← DEPLOY` in E2.2, which rendered DOWN.)
  P.push(`<text transform="rotate(-90 ${f2(railL + 6)} ${f2(cyMid)})" x="${f2(railL + 6)}" y="${f2(cyMid)}" text-anchor="middle" fill="${s.ink}" font-weight="${s.titleWeight}" font-size="${FURN.poleTitle}" letter-spacing="${FURN.poleTitleLS}">↑ DEPLOY (E1 ref)</text>`);
  P.push(`<text transform="rotate(-90 ${f2(railL - 9)} ${f2(cyMid)})" x="${f2(railL - 9)}" y="${f2(cyMid)}" text-anchor="middle" fill="${s.faint}" font-size="${FURN.poleGloss}" font-style="${s.glossStyle}" letter-spacing="0.2">${esc(POLE_GLOSS.DEPLOY)}</text>`);
  // -- LAUNCH: top strip (y[106,131], below the derivation gloss at y102 / above the plot at y132).
  //    Title + gloss combined into ONE centered horizontal line so it fits the ~25px band. Both
  //    strings present verbatim; the gloss is separated by a spaced mid-dot so each greps whole.
  const LAUNCH_LINE = `↑ LAUNCH (E1 ref)    ${POLE_GLOSS.LAUNCH}`;
  P.push(`<text x="${f2(cxMid)}" y="120" text-anchor="middle" fill="${s.ink}" font-weight="${s.titleWeight}" font-size="${FURN.launchEmbody}" letter-spacing="0.6">${esc('↑ LAUNCH (E1 ref)')}    <tspan fill="${s.faint}" font-weight="400" font-size="${FURN.poleGloss}" font-style="${s.glossStyle}">${esc(POLE_GLOSS.LAUNCH)}</tspan></text>`);
  // -- EMBODY: bottom-center pocket x[703,916] (between the ledger's left column, which ends ≈x714,
  //    and its right column at x916), BELOW the plot bottom (1104). Title baseline y=1119 (cap-top
  //    ≈1106.5 > 1104 — clears the plot rect); gloss wraps to ≤2 lines in the ~213px pocket
  //    (deterministic char-wrap) at a 14px pitch so the two lines' bboxes do not touch, the FULL
  //    contiguous POLE_GLOSS.EMBODY carried in a <title> for the verbatim grep. Last row ≈y1148 —
  //    clears the footer (y1188). All EMBODY geometry OUTSIDE the plot rect (acceptance-30).
  const embodyRows = wrapByChars(POLE_GLOSS.EMBODY, 30); // ~30 chars ≈ 190px @ fs9.5 < 213px pocket
  // r8: title 12.5→9.5, gloss →7. Baselines (y1119 title; 1134 + i·11 gloss) stay in the bottom
  // pocket below the plot rect (cap-top of the 9.5px title ≈1109.5 > 1104 — still clears the plane).
  P.push(`<text x="${f2(cxMid)}" y="1119" text-anchor="middle" fill="${s.ink}" font-weight="${s.titleWeight}" font-size="${FURN.launchEmbody}" letter-spacing="0.6">${esc('EMBODY ↓ (E1 ref)')}</text>`);
  for (let i = 0; i < embodyRows.length; i++) {
    const titleNode = i === 0 ? `<title>${esc(POLE_GLOSS.EMBODY)}</title>` : '';
    P.push(`<text x="${f2(cxMid)}" y="${f2(1134 + i * 11)}" text-anchor="middle" fill="${s.faint}" font-size="${FURN.poleGloss}" font-style="${s.glossStyle}" letter-spacing="0.2">${esc(embodyRows[i])}${titleNode}</text>`);
  }
  // REFIT ORIENTATION GLOSS (the one required gloss, brief iron law) — states the reference-orientation
  // law once for all four poles. Placed in the bottom pocket below the EMBODY gloss (clears the footer).
  const ORIENT_GLOSS = 'poles = Edition-I reference orientation; refit axes unratified';
  P.push(`<text x="${f2(cxMid)}" y="${f2(1134 + embodyRows.length * 11 + 4)}" text-anchor="middle" fill="${s.faint}" font-size="${FURN.poleGloss}" font-style="${s.glossStyle}" letter-spacing="0.2">${esc(ORIENT_GLOSS)}</text>`);
  P.push(`</g>`);

  // ---- title + RIDER-1 badge [r2 layout; STRING re-led per E2.1-c] (derivation gloss verbatim)
  // E2.1-c banner relabel (spec §10.8-c): the r-series string LED with "Edition ${edition}" where
  // basis.edition == 1 (the FIT basis is Edition-I frozen) — under an edition chart title that would
  // read as a contradictory edition stamp. `riderStr` (module scope) is re-led to lead with the
  // CHART's own edition (editionTag = "III" at Edition-III); the basis edition is DEMOTED to an
  // attribute. Every locked substring survives VERBATIM; only the leading edition token + basis demote.
  P.push(`<g font-family="${s.fontStack}" fill="${s.ink}">`);
  // PLATE RELABEL (Matt 2026-07-15 ninth-message directive; interactive spec §9.6 D6-d): the chart
  // title reads "Build Horizon — Edition ${editionTag}" (= "Build Horizon — Edition III" at Edition-III).
  // Presentation-TEXT-ONLY on frozen geometry. The TITLE composes the human-form edition token "Edition
  // ${editionTag}" (SPACE form) — NOT `atlasVersion` ("Edition-III", the hyphenated machine form), which
  // is DEDICATED to the footer provenance strip + JSON fields. editionTag ("III") is the emitted
  // ghost_field.edition — DATA-DERIVED, never a renderer literal (§4c), so the title auto-moves at the
  // edition boundary with NO source change. Geometry/positions/data byte-logic frozen.
  // r8: title 26→17.5 (baseline y42 kept — above the band); RIDER band 30→20 hugs the 8.5px banner,
  // band TOP y58 kept (a fixed seat); banner baseline re-centered in the shrunk [58,78] band; deriv
  // gloss 11→7.5, baseline y102 kept (now well clear of the shortened band bottom at 78).
  // REFIT TITLE — "Build Horizon — Refit Candidate 1" (NO "Edition" word; this is a comparison plate).
  // REFIT_DISPLAY is data-derived from the emitted edition ("Refit-Candidate-1" → "Refit Candidate 1").
  P.push(`<text x="${f2(M.left)}" y="42" font-size="${FURN.title}" font-weight="${s.titleWeight}" letter-spacing="0.5">Build Horizon — ${esc(REFIT_DISPLAY)}</text>`);
  P.push(`<rect x="${f2(M.left)}" y="58" width="${f2(PW)}" height="${f2(FURN.bannerBandH)}" rx="4" fill="${s.badgeBg}" stroke="${s.plaqueStroke}" stroke-width="1"/>`);
  P.push(`<text x="${f2(M.left + 12)}" y="72" font-size="${FURN.banner}" fill="${s.badgeInk}" letter-spacing="0.3">${esc(riderStr)}</text>`);
  P.push(`<text x="${f2(M.left + 12)}" y="102" font-size="${FURN.deriv}" font-style="${s.glossStyle}" fill="${s.faint}" letter-spacing="0.2">${esc(DERIVATION_GLOSS)}</text>`);
  P.push(`</g>`);

  // ---- BUILD FAMILIES legend (top-right of plane) [r2 layout; density line preserved]
  //      Matt 2026-07-16: header renamed CONDENSATIONS → BUILD FAMILIES. r8: header/rows 11→8,
  //      gloss 9.5→7 (r8-fix bump; was 6.5), swatch r4.6→3.4, row pitch 18→13, box width 196→158
  //      hugging the shrunken content, box height RE-DERIVED FROM CONTENT (last gloss baseline +
  //      descender + bottom pad — see the derivation block below). r8-fix: the pre-fix height under-
  //      counted gloss line 2 (baseline landed 2.5px past the border); now the box contains it.
  //      Top-right anchor (lx, ly) UNCHANGED — the box hugs its text; it does not move. The swatch
  //      circles carry `fill` (not a data mark; no <title>, no data-*) so the acc-29 ground-geometry
  //      regex never matches them.
  {
    const lx = M.left + PW - 152, ly = M.top + 14;
    // r8-fix (2026-07-16): box height RE-DERIVED FROM CONTENT so the LAST gloss baseline + its
    // descender sit INSIDE with matching bottom padding. The pre-fix `glossBlockH` under-counted the
    // second gloss line (budgeted keyGloss+12+4 but the inter-gloss pitch is 11 and line-2 baseline
    // landed 2.5px PAST the border → text straddled it in the crop receipts, both skins). Now the box
    // bottom is computed from the SAME accumulator the draw loop walks below, so they cannot diverge.
    //   Top structural pad  = firstBaseline(ly+2) − boxTop(ly−12) = 14  (14px baseline-to-top-edge).
    //   Row block baseline   = ly + (keyHeader+8) + keyRowH·N.
    //   Gloss line-1 baseline= +2   (the `yy += 2` swatch-pad step).
    //   Gloss line-2 baseline= +11  (inter-gloss pitch; stays disjoint at fs7).
    //   Bottom pad           = GLOSS_DESC (descender, ~0.28·fs7≈2) + BOTTOM_PAD (8, matches the
    //                          whitespace above the header cap) → box bottom clears the descender.
    const GLOSS_DESC = 2, BOTTOM_PAD = 8;
    const lastGlossBaselineRel = (FURN.keyHeader + 8) + FURN.keyRowH * GROUP_ORDER.length + 2 + 11;
    const boxH = (lastGlossBaselineRel + 12) + GLOSS_DESC + BOTTOM_PAD;  // +12: boxTop is ly−12
    P.push(`<g font-family="${s.fontStack}" font-size="${FURN.keyRow}" fill="${s.ink}">`);
    P.push(`<rect x="${f2(lx - 12)}" y="${f2(ly - 12)}" width="158" height="${f2(boxH)}" rx="4" fill="${s.plaque}" fill-opacity="0.9" stroke="${s.plaqueStroke}"/>`);
    P.push(`<text x="${f2(lx)}" y="${f2(ly + 2)}" font-weight="${s.titleWeight}" font-size="${FURN.keyHeader}" letter-spacing="0.5">BUILD FAMILIES</text>`);
    let yy = ly + FURN.keyHeader + 8;
    for (const g of GROUP_ORDER) {
      const c = groupCentroids[g];
      const n = c ? c.n : 0;
      P.push(`<circle cx="${f2(lx + 4)}" cy="${f2(yy - 3)}" r="${FURN.keySwatchR}" fill="${GROUP_COLORS[g]}"/>`);
      P.push(`<text x="${f2(lx + 14)}" y="${f2(yy)}" font-size="${FURN.keyRow}">${esc(g)} (${n})</text>`);
      yy += FURN.keyRowH;
    }
    yy += 2;
    P.push(`<rect x="${f2(lx)}" y="${f2(yy - 7)}" width="${f2(FURN.keyBandGloss)}" height="${f2(FURN.keyBandGloss)}" fill="${s.bandBase}" fill-opacity="0.5"/>`);
    P.push(`<text x="${f2(lx + 14)}" y="${f2(yy)}" font-size="${FURN.keyGloss}" font-style="${s.glossStyle}" fill="${s.faint}">shaded field = density of genre kits</text>`);
    yy += 11;
    P.push(`<text x="${f2(lx + 14)}" y="${f2(yy)}" font-size="${FURN.keyGloss}" font-style="${s.glossStyle}" fill="${s.faint}">(settled territory — not a boundary)</text>`);
    P.push(`<desc>${esc(DENSITY_LEGEND_LINE)}</desc>`);
    P.push(`</g>`);
  }

  // ---- graveyard legend (death classes; per-class count) — bottom-left [r2]
  //      r8: header 11→7.5, † markers + rows 11/10→7, row pitch 15→10.5, box width 230→158, dashed
  //      unknown-ring r6→4 scales with the 7px row. The box is BOTTOM-LEFT anchored: ly0 is derived
  //      so the box BOTTOM stays at M.top+PH-14 (unchanged) while it shrinks upward with the pitch.
  {
    const lx = M.left + 12, ly0 = M.top + PH - (deathClasses.length * FURN.graveRowH + 26);
    P.push(`<g font-family="${s.fontStack}" font-size="${FURN.graveRow}" fill="${s.ink}">`);
    P.push(`<rect x="${f2(lx - 8)}" y="${f2(ly0 - 14)}" width="158" height="${f2(FURN.graveRowH * deathClasses.length + 26)}" rx="4" fill="${s.plaque}" fill-opacity="0.9" stroke="${s.plaqueStroke}"/>`);
    P.push(`<text x="${f2(lx)}" y="${f2(ly0)}" font-weight="${s.titleWeight}" font-size="${FURN.graveHeader}" letter-spacing="0.4">GRAVEYARD † (${supplementary.length} corpses)</text>`);
    let yy = ly0 + 14;
    for (const dc of deathClasses) {
      const n = supplementary.filter((p) => p.death_class === dc).length;
      const unk = isUnknown(dc);
      const ink = unk ? s.tombUnknownInk : s.tombInk;
      P.push(`<text x="${f2(lx + 2)}" y="${f2(yy)}" font-size="${FURN.graveRow}" fill="${ink}" font-weight="700">†</text>`);
      if (unk) P.push(`<circle cx="${f2(lx + 5)}" cy="${f2(yy - 3)}" r="4" fill="none" stroke="${ink}" stroke-width="1" stroke-dasharray="2 2"/>`);
      P.push(`<text x="${f2(lx + 14)}" y="${f2(yy)}" font-size="${FURN.graveRow}" fill="${ink}">${esc(dc)} (${n})</text>`);
      yy += FURN.graveRowH;
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
    // r8: left-column below-plane rows shrunk (census 10.5→7, headline-lit 12.5→8.5, density 11→7.5,
    // coverage 9.5→6.5, feasible-accounting 9→6.5). BASELINES kept (by+1/17/32/46/60) — smaller fonts
    // sit with MORE clearance both between rows and vs the byte-frozen footer census at y=1188.
    P.push(`<text x="${f2(bx)}" y="${f2(by + 1)}" font-size="${FURN.ledgerCensus}" font-style="${s.glossStyle}" fill="${s.faint}">${esc(GHOST_CENSUS_LINE)}</text>`);
    P.push(`<text x="${f2(bx)}" y="${f2(by + 17)}" font-size="${FURN.ledgerHeadline}" font-weight="${s.titleWeight}" fill="${s.ink}" letter-spacing="0.2">${esc(HEADLINE_LIT)}</text>`);
    P.push(`<text x="${f2(bx)}" y="${f2(by + 32)}" font-size="${FURN.ledgerHl2}" font-weight="${s.titleWeight}" fill="${s.ink}">${esc(HEADLINE_DENSITY)}</text>`);
    P.push(`<text x="${f2(bx)}" y="${f2(by + 46)}" font-size="${FURN.ledgerSub}" font-style="${s.glossStyle}" fill="${s.faint}">${esc(COVERAGE_SECONDARY)}</text>`);
    // one compact ghost accounting line (feasible/lit/unmapped + meso sealed) — the r6 core ledger, one row.
    const feasStr = `${fmtInt(feasibleCells.length)} feasible meso cells · ${fmtInt(litCells)} lit · ${fmtInt(unmappedPending)} unmapped · ${fmtInt(mesoSealed)} sealed (off-plane)`;
    P.push(`<text x="${f2(bx)}" y="${f2(by + 60)}" font-size="${FURN.ledgerSub}" fill="${s.faint}">${esc(feasStr)}</text>`);
    const sealSummary = sealedCutOrder.map((cid) => `${cid} ${fmtInt(sealedByCut[cid])}`).join(' · ');
    // RIGHT COLUMN (x = colR) — the EDITION II lattice ledger, one compact SUMMARY line per entry.
    // Each <text> carries a <title> with the FULL emitted string (whole-grep + hover). The visible
    // summary is a short lead; the title is the complete content-locked / emitted sentence. The meso
    // sealed cut-summary rides the sealed line's <title> (whole-grep target for the sealed cut ids).
    // E2.1-f: right column moved RIGHT (bx+820=916) so its header + rows clear the frozen EMBODY
    // pole gloss (centered x≈800, right edge ≈902) — the r-series colR=596 put the header under it.
    // Long rows still fit (≤~100 chars fs8 → 916+400=1316 < plane-right 1504).
    const colR = bx + 820;                                 // right column left edge (past the EMBODY gloss)
    // DIFF site 5: ghost-ledger header edition literal now DATA-DERIVED from editionTag (ghost_field.edition
    // = "III") — auto-moves at the boundary, §4c. Renders "· Edition III lattice"; the acceptance grep +
    // the below-plane-ledger smoke both re-target to "Edition III lattice" (DIFF sites 7/9).
    P.push(`<text x="${f2(colR)}" y="${f2(by + 1)}" font-size="${FURN.ledgerRight}" font-weight="${s.titleWeight}" letter-spacing="0.3" fill="${s.ink}">GHOST FIELD — the feasible dark · ${esc(REFIT_DISPLAY)} lattice</text>`);
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
    // REFIT: compact VISIBLE lead (short x-extent so the last row clears the footer census); the FULL
    // emitted_alongside provenance line (`supersededLine` slot) rides the <title> — the ONLY on-plate
    // place "Edition III" may appear (the served-truth reference). Acceptance #28 greps it whole.
    led.push({ s: 'emitted alongside (served-truth reference) — hover', titles: [supersededLine], gloss: true });
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
      // r8: right-column rows 7.5→6, pitch 7.3→6 (fs6 glyph≈5.5 < 6 pitch: rows stay disjoint; the
      // tighter pitch pulls the last row UP, away from the byte-frozen footer census — safer clearance).
      P.push(`<text x="${f2(colR)}" y="${f2(ry)}" font-size="${FURN.ledgerRow}"${styleAttr}${weightAttr} fill="${fillAttr}">${esc(r.s)}${titleNodes}</text>`);
      ry += FURN.ledgerRowH;
    }
    P.push(`</g>`);
  }

  // ---- footer stamp (provenance; all from atlas.json). EDITION III (§10.4.5): the footer carries the
  // edition token ("Edition-III", via atlasVersion) + the v1.3 register ref on BOTH skins. A new EDITION,
  // so the frozen-footer single-purpose-diff discipline (r4/r5/r6, within Edition-I) does not apply across
  // the boundary — the footer stamps the edition + register honestly. Both fields DATA-DERIVED (§4c).
  // r8: footer group font 10→7. The two footer <text> baselines (y=H-12=1188) + their content strings
  // are BYTE-FROZEN by the E2-belowplane + E2.1-d acceptance matches (which key on x/y/content, NOT
  // font-size) — the group-level size change is invisible to them, and both footers stay put.
  P.push(`<g font-family="${s.fontStack}" fill="${s.faint}" font-size="${FURN.footer}">`);
  // LEFT footer stamp — E2.1-d PROVENANCE DEDUPE (spec §10.8-d): the edition token appears EXACTLY ONCE.
  // The visible footer is `${atlasVersion}` ("Edition-III") · `${registerRef}` ("…-v1.3") · emitted · skin
  // — a SINGLE edition token (atlasVersion carries it; there is NO redundant " · Edition ${editionTag}").
  // E2.1-f: the VISIBLE footer is trimmed to the load-bearing stamp (edition · register · emitted · skin)
  // so it CLEARS the right census footer (no bottom-band overlap). The emitter-script + render-script paths
  // live in render-provenance.json (machine-readable provenance), not the visible chrome.
  P.push(`<text x="${f2(M.left)}" y="${f2(H - 12)}">${esc(String(atlasVersion))} · ${esc(String(registerRef))} · emitted ${esc(emittedAt)} · skin=${skinKey}</text>`);
  // RIGHT census footer — EDITION III: the r6 in-plane plaque is retired (the ledger moved below-
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
  // REFIT: ensure the candidate output dir exists (the r8 head relied on a pre-existing edition dir).
  if (!RECEIPT_ONLY) mkdirSync(OUT_DIR, { recursive: true });
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
      writeFileSync(join(OUT_DIR, `atlas-refit-candidate-1-${skin}.svg`), svg, 'utf8');   // REFIT: candidate output name
    }
    console.log(`[allin-render] wrote SVGs to ${OUT_DIR} (N beyond=${beyondHorizonCount}; suite skipped)`);
    return;
  }

  const ptFps = {}, ghFps = {};
  for (const skin of ['instrument', 'archive']) {
    const svg = renderSVG(skin);
    const svgPath = join(OUT_DIR, `atlas-refit-candidate-1-${skin}.svg`);   // REFIT: candidate output name
    writeFileSync(svgPath, svg, 'utf8');
    ptFps[skin] = pointFingerprint();
    ghFps[skin] = ghostFingerprint();
    const pngPath = join(OUT_DIR, `atlas-refit-candidate-1-${skin}.png`);   // REFIT: candidate output name
    const png = await sharp(Buffer.from(svg), { density: 144 }).png().toBuffer();
    writeFileSync(pngPath, png);
    results[skin] = { svgPath, pngPath, bytes: Buffer.byteLength(svg) };
    console.log(`[render] ${skin}: ${svgPath} (${results[skin].bytes} B), ${pngPath} (${png.length} B PNG)`);
  }

  // ---- ACCEPTANCE TESTS ----
  const tests = [];
  const rec = (name, pass, detail) => tests.push({ name, pass, detail });
  // DEMOTED OBSERVATIONS (REPORTED, NOT GATING — brief §4). Declared here so BOTH the acceptance section
  // and the smoke section can push observations. `obs(name, holds, refit, expectation)` → PASS/CHANGED.
  const observations = [];
  const obs = (name, holds, refit, expectation) => observations.push({ name, flag: holds ? 'PASS' : 'CHANGED', refit, expectation });
  const bodies = {};
  for (const skin of ['instrument', 'archive']) bodies[skin] = readFileSync(join(OUT_DIR, `atlas-refit-candidate-1-${skin}.svg`), 'utf8');   // REFIT: candidate output name

  // (1) point counts — REFIT RE-POINT: assert against the candidate's own emitted counts (628+37=665),
  //     not the Edition-I frozen 469/37/506. Also cross-check render partition == emitted counts block.
  rec('point-counts', active.length === 628 && supplementary.length === 37 && all.length === 665
      && active.length === counts.active && supplementary.length === counts.supplementary && all.length === counts.total,
    `active=${active.length} (exp 628, emitted ${counts.active}), supp=${supplementary.length} (exp 37, emitted ${counts.supplementary}), total=${all.length} (exp 665, emitted ${counts.total})`);

  // (2) grouped/neutral partition — REFIT RE-POINT: grouped == labelled gateA members from the emission.
  const groupedFromJson = active.filter((p) => p.gateA_group != null).length;
  rec('grouped-count', grouped.length === groupedFromJson && grouped.length === 86,
    `grouped=${grouped.length} (== labelled gateA members ${groupedFromJson}; exp 86)`);

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
      // REFIT: the clip line is the (honest, lit-aware) render-pass line; assert it verbatim both skins
      // and that the disclosed total-count numeral is the render-pass count (no stale hard-coded value).
      const present = ['instrument', 'archive'].every((sk) => bodies[sk].includes(esc(ghostClipLine)));
      const countMatch = ['instrument', 'archive'].every((sk) => bodies[sk].includes(`>${fmtInt(ghostClippedCount)} `));
      clipOk = present && countMatch;
      clipMsg = clipOk
        ? `clip line present both skins (total=${fmtInt(ghostClippedCount)}: ${fmtInt(ghostClippedLitCount)} LIT + ${fmtInt(ghostClipUnlitCount)} unlit, from render pass; DISCLOSED honestly — lit cell(s) just outside the candidate's own points-derived frame, not rescaled)`
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

  // (23) REFIT — the Edition-I FIT-LAYER byte-freeze regression vs r6 is RETIRED (a NEW fit has no
  //      freeze baseline; the candidate's 628 points are a full re-derivation and DO NOT match the frozen
  //      469 Edition-I point set — comparing would falsely "fail" by design). REPLACED by an internal-
  //      consistency check (RE-POINT, fail-loud): every rendered point circle's coordinate+title tuple
  //      is reproducible from the emitted points (628 actives + 37 tombstones present, both skins), and
  //      the two skins carry an identical point/tombstone geometry set. No external baseline is read.
  let fitPass = true, fitDetail = [];
  const pointTupleRe = /<circle cx="([\d.]+)" cy="([\d.]+)" r="([\d.]+)"[^>]*><title>([^<]*)<\/title><\/circle>/g;
  const extractPtsTuple = (svg) => { const set = []; let m; while ((m = pointTupleRe.exec(svg)) !== null) set.push(`${m[1]}|${m[2]}|${m[3]}|${m[4]}`); pointTupleRe.lastIndex = 0; return set.sort().join('\n'); };
  const tombTupleRe = /<text x="([\d.]+)" y="([\d.]+)" font-size="16" text-anchor="middle"[^>]*>†<title>([^<]*)<\/title><\/text>/g;
  const extractTombTuple = (svg) => { const set = []; let m; while ((m = tombTupleRe.exec(svg)) !== null) set.push(`${m[1]}|${m[2]}|${m[3]}`); tombTupleRe.lastIndex = 0; return set.sort().join('\n'); };
  {
    const iPts = extractPtsTuple(bodies.instrument), aPts = extractPtsTuple(bodies.archive);
    const iTomb = extractTombTuple(bodies.instrument), aTomb = extractTombTuple(bodies.archive);
    const nPts = iPts.split('\n').filter(Boolean).length, nTomb = iTomb.split('\n').filter(Boolean).length;
    // internal consistency: skin-invariant point/tombstone geometry, and counts == emitted actives/supp.
    const skinInvariant = iPts === aPts && iTomb === aTomb;
    const countsMatch = nPts === active.length && nTomb === supplementary.length;
    // fit-explainer chrome present both skins (the candidate carries the same content-locked copy class).
    const fitFrozenStrings = [
      POLE_GLOSS.PERFORM, POLE_GLOSS.DEPLOY, POLE_GLOSS.LAUNCH, POLE_GLOSS.EMBODY,
      DENSITY_LEGEND_LINE, DERIVATION_GLOSS, structureStatement,
    ].map(esc);
    const fitStrEq = ['instrument', 'archive'].every((sk) => fitFrozenStrings.every((str) => bodies[sk].includes(str)));
    fitPass = skinInvariant && countsMatch && fitStrEq;
    fitDetail.push(`RETIRED r6/e21 byte-freeze (new fit). Internal-consistency: point-circles skin-invariant=${skinInvariant} (${nPts}==${active.length} actives), tombstones (${nTomb}==${supplementary.length} supp), fit-explainer-strings=${fitStrEq}`);
  }
  rec('fit-layer-internal-consistency', fitPass, fitDetail.join(' | '));

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
      const appInst = readFileSync(join(tmpOut, 'atlas-refit-candidate-1-instrument.svg'), 'utf8');   // REFIT: child writes refit-candidate-1-*
      const appArch = readFileSync(join(tmpOut, 'atlas-refit-candidate-1-archive.svg'), 'utf8');
      const appearsBoth = appInst.includes(BEYOND_PHRASE) && appArch.includes(BEYOND_PHRASE);
      appearChanged = dN === 1 && appearsBoth;
      appearDetail = `added east kit @ (2.5,-2.3): BEYOND_N ${beyondHorizonCount}→${dN}; beyond line appears both skins=${appearsBoth}`;
    } catch (e) {
      appearDetail = `appear re-render FAILED: ${e.message}`;
    }

    // (16e) REFIT meso cross-check: the point-in-hull machinery finds the candidate's meso-beyond kits,
    // and that count MUST equal the emitted p_df_1.n_beyond_horizon_kits (13) — the render-vs-emission
    // cross-check (RE-POINTED from the Edition-I frozen 14 receipt to the candidate's emitted value).
    const indMeso = active.filter((p) => !pointInHullWorld(p.x, p.y, mesoOnlyHullWorld)).length;
    const mesoReceiptOk = indMeso === Number(P_DF_1_N_BEYOND_HORIZON) && beyondMesoOnlyCount === Number(P_DF_1_N_BEYOND_HORIZON);

    rec('r5-beyond-horizon', beyondOmitted && reachPresent && nMatch && appearChanged && mesoReceiptOk,
      `charted N=${beyondHorizonCount} (indep=${indBeyond}, expected=${BEYOND_HORIZON_EXPECTED}); beyond-line-omitted(zero-case)=${beyondOmitted}; charted-reach-line-present=${reachPresent}; computed-not-constant: ${appearDetail}; meso-cross-check N=${indMeso}==emitted-p_df_1(${P_DF_1_N_BEYOND_HORIZON})=${mesoReceiptOk}`);
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
  // EDITION III ACCEPTANCE SUITE — criteria 22-28 (spec §10.6). The full §7+§9 suite above
  // re-instantiates against Edition-III artifacts; these are the edition-specific additions.
  // ==================================================================================
  // Doctored-input harness: write a doctored COPY of atlas-edition3.json to a temp file, run THIS
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

  // (22) register-v1.3-derivation (§10.6.22): denominators independently re-derived (Edition-III RE-ASSERTS
  //      the v1.2 numbers byte-identical; lattice did not move); pull-slice vetted (new_law_needed==0, no
  //      HALT); register ref is v1.3.
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
    // (d) register ref pins v1.3; pull-slice needs NO new law (else the module would have HALTed at load).
    const regOk = String(registerRef) === 'feasibility-cuts-register-v1.3' && pullNewLaw === 0 && pullHalt === false;   // DIFF site 7
    const pass22 = denomConsistent && mesoClose && sealSplitClose && regOk;
    rec('register-v1.3-derivation', pass22,
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
    // (c) REFIT — the Edition-III "ZERO mcd- points on the plane" invariant is DEMOTED (not gated) AND
    //     a DISCLOSURE TENSION is surfaced. In Edition III the 94 mcd- (gear-grain) kits were held OFF
    //     the plane (0 in points[]); the candidate carries all 94 mcd- kits AS ACTIVE ON-PLANE POINTS
    //     (628 active = 534 non-mcd + 94 mcd). YET the emitted off_plane_corpus.disclosure STILL says
    //     "94 gear-grain kits (mcd-) sit in the corpus off-plane" (gate_rejected_keyed=94). That is an
    //     INTERNAL TENSION in the candidate emission — the ledger claims off-plane, the coordinates place
    //     them on-plane. We SURFACE it (never silently tolerate; never hard-HALT — it is not a
    //     hull/census/P-DF-1 render-vs-emission mismatch, and NOT an enumerated HALT condition). This is
    //     exactly the kind of thing the plate exists to show Matt for the adoption decision.
    const mcdOnPlane = all.filter((p) => String(p.kit_id).startsWith('mcd-')).length;
    const mcdDisclosureTension = mcdOnPlane > 0 && Number(offPlaneN) > 0;   // ledger says off-plane; coords say on-plane
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
    // GATING: cores==tuples + re-keys exist + BOTH doctored HALTs. The mcd-on-plane check is NOT gated
    // (it CHANGED by design — the refit un-masked gear-grain kits); it is surfaced as an observation.
    const pass25 = coresMatch && reKeysExist && doctorMcd.halted && doctorNewLaw.halted;
    rec('pull-slice-lit-integrity', pass25,
      `lit-pull-cores==tuples(${coresMatch}); re-keys d3-zbarb+di-cyclone exist & non-mcd(${reKeysExist}); doctored HALT(a) mcd-forced=${doctorMcd.halted}(code ${doctorMcd.code}); doctored HALT(b) new-law=${doctorNewLaw.halted}(code ${doctorNewLaw.code}); [mcd-on-plane=${mcdOnPlane} — see DEMOTED observation for the disclosure tension]`);
    // SURFACE the mcd disclosure tension as a REPORTED observation (CHANGED — the refit put gear-grain
    // kits on-plane while the emitted ledger still says off-plane).
    obs('mcd- gear-grain: on-plane vs emitted off-plane ledger', !mcdDisclosureTension,
      `${mcdOnPlane} mcd- kits ON-plane as active points, but off_plane_corpus.disclosure says ${offPlaneN} off-plane — EMISSION TENSION, surfaced for Matt`,
      'Edition-III: 0 mcd- on-plane (94 held off-plane, ledger consistent)');
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

  // (27) P-DF-1-scored (REFIT — render-vs-emission verdict cross-check): the verdict is rendered from the
  //      emitted p_df_1 block (single source; no top-level mirror on the candidate) and its MECHANISM is
  //      re-validated against the emitted operands: PASS ⟺ NOT falsified ⟺ S_max > K_max. Also cross-check
  //      the S_max / K_max VALUES against the brief's stated cross-check targets (1.90823161 / 1.15472813).
  {
    const sMax = req(atlas, 'ghost_field.p_df_1.S_max', 'p-df-1-smax');
    const kMax = req(atlas, 'ghost_field.p_df_1.K_max_beyond_horizon', 'p-df-1-kmax');
    // PASS ⟺ NOT falsified ⟺ S_max > K_max (the mechanical form). Assert the emitted verdict is internally
    // consistent with its own falsifier operands (we render the verdict, we test it here).
    const verdictMatchesMechanism = (pDf1Verdict === 'PASS') === (!pDf1Falsified) && (!pDf1Falsified) === (sMax > kMax);
    // brief §3 cross-check targets — the S_max / K_max the head recomputes-per-standing-law must equal.
    const valuesMatchBrief = Math.abs(sMax - 1.90823161) < 1e-6 && Math.abs(kMax - 1.15472813) < 1e-6 && String(pDf1Verdict) === 'PASS' && pDf1.n_beyond_horizon_kits === 13;
    const pass27 = verdictMatchesMechanism && valuesMatchBrief && ['PASS', 'FALSIFIED', 'FAIL'].includes(String(pDf1Verdict));
    rec('P-DF-1-scored', pass27,
      `verdict=${pDf1Verdict} (single-source); falsified=${pDf1Falsified}; S_max=${sMax} ${sMax > kMax ? '>' : '<='} K_max=${kMax}; mechanism-consistent=${verdictMatchesMechanism}; values-match-brief-targets(S=1.90823161,K=1.15472813,n=13)=${valuesMatchBrief}`);
  }

  // (28) REFIT ANTI-STALE + IDENTITY GREPS (brief §5, iron law): the plate must carry the COMPARISON
  //      identity, NOT an Edition identity. (a) "Edition IV"/"edition4" absent ENTIRELY (never — this is
  //      not the next edition). (b) "Edition III"/"Edition-III" appears ONLY inside the emitted_alongside
  //      provenance line (the served-truth reference), never as the plate's own identity — checked by
  //      stripping that line and asserting the tokens vanish. (c) the refit stamps ("Refit Candidate 1"
  //      title, the UNRATIFIED banner, the plane-alignment disclosure) present both skins. (d) carried
  //      content-locked strings present verbatim both skins.
  {
    // (a) "Edition IV" / "edition4" absent ENTIRELY (iron law).
    const noEd4 = ['instrument', 'archive'].every((sk) => !/Edition\s*IV/i.test(bodies[sk]) && !/edition4/i.test(bodies[sk]));
    // (b) "Edition III"/"Edition-III" ONLY inside the emitted_alongside provenance line. The only render
    //     site of that string is the labeled `supersededLine` slot (= "emitted alongside: …edition3.json…").
    //     Strip that line from each body and assert no "Edition III"/"Edition-III"/"edition3" survives.
    const provEsc = esc(supersededLine);
    let ed3OnlyInProv = true, ed3Detail = [];
    for (const sk of ['instrument', 'archive']) {
      const stripped = bodies[sk].split(provEsc).join('');
      const hasE3space = /Edition\s+III\b/.test(stripped);
      const hasE3hyphen = /Edition-III\b/.test(stripped);
      const hasE3lower = /edition3/.test(stripped);
      if (hasE3space || hasE3hyphen || hasE3lower) { ed3OnlyInProv = false; ed3Detail.push(`${sk}: E3-space=${hasE3space}, E3-hyphen=${hasE3hyphen}, edition3=${hasE3lower} OUTSIDE emitted_alongside`); }
      // and it MUST be present INSIDE the provenance line (the emitted_alongside references edition3.json).
      if (!bodies[sk].includes(provEsc)) { ed3OnlyInProv = false; ed3Detail.push(`${sk}: emitted_alongside provenance line ABSENT`); }
    }
    // (c) refit identity stamps present both skins: title "Refit Candidate 1", the UNRATIFIED banner lead,
    //     the plane-alignment rotation disclosure.
    const refitStamped = ['instrument', 'archive'].every((sk) =>
      bodies[sk].includes(esc(`Build Horizon — ${REFIT_DISPLAY}`)) &&
      bodies[sk].includes(esc('UNRATIFIED COMPARISON ARTIFACT')) &&
      bodies[sk].includes(esc(`rotation ${planeAlignRotDeg}°`)) &&
      bodies[sk].includes('feasibility-cuts-register-v1.3'));
    // (d) carried content-locked strings present verbatim both skins.
    const carried = [
      POLE_GLOSS.PERFORM, POLE_GLOSS.DEPLOY, POLE_GLOSS.LAUNCH, POLE_GLOSS.EMBODY,
      DENSITY_LEGEND_LINE, DERIVATION_GLOSS, GHOST_CENSUS_LINE, GHOST_HORIZON_LABEL,
      chartedReachLine, structureStatement,
      'poles = Edition-I reference orientation; refit axes unratified',
      ...(beyondHorizonCount > 0 ? [beyondHorizonLine] : []),
    ].map(esc);
    const carriedOk = ['instrument', 'archive'].every((sk) => carried.every((str) => bodies[sk].includes(str)));
    const pass28 = noEd4 && ed3OnlyInProv && refitStamped && carriedOk;
    rec('refit-identity+anti-stale-greps', pass28,
      `Edition-IV/edition4-absent=${noEd4}; Edition-III-only-in-emitted_alongside=${ed3OnlyInProv}${ed3Detail.length ? ' ['+ed3Detail.join('; ')+']' : ''}; refit-stamps(title+unratified-banner+alignment-disclosure+v1.3)=${refitStamped}; content-locked-strings-verbatim=${carriedOk}`);
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

  // (REFIT-banner) BANNER LEAD: the rider strip LEADS with the UNRATIFIED-comparison framing, then the
  //          plane-alignment disclosure (rotation + det), then the plane-level inertia + retained dims +
  //          structure. Any "Edition …" edition-stamp lead is ABSENT. Locked substrings present verbatim.
  {
    // (a) the rider leads with the unratified-comparison framing (exact form).
    const bannerLeadOk = ['instrument', 'archive'].every((sk) => bodies[sk].includes(esc(riderStr))) && riderStr.startsWith('UNRATIFIED COMPARISON ARTIFACT');
    // (b) no "Edition N lattice · basis" edition-stamp lead survives (this is a comparison plate).
    const oldLeadGone = !/^Edition\s/.test(riderStr) && ['instrument', 'archive'].every((sk) => !bodies[sk].includes('Edition 1 · frozen'));
    // (c) every LOCKED substring survives verbatim inside the rider (refit set — alignment + plane inertia).
    const lockedSubstrings = [
      `frozen=${frozen}`, `rotation ${planeAlignRotDeg}°`, `det ${planeAlignDet}`,
      'plane = dims 1–2', `${inertiaPct}% corrected inertia`,
      `retained basis: ${retainedDims} dims`, String(structureStatement),
    ];
    const substringsOk = lockedSubstrings.every((sub) => riderStr.includes(sub));
    rec('refit-banner-lead', bannerLeadOk && oldLeadGone && substringsOk,
      `leads-with-UNRATIFIED-framing=${bannerLeadOk}; no edition-stamp lead=${oldLeadGone}; locked substrings (alignment+plane-inertia) verbatim=${substringsOk}`);
  }

  // (E2.1-d) PROVENANCE DEDUPE (spec §10.8-d): the footer edition token appears EXACTLY ONCE. DIFF site
  //          7 — the edition-token regexes re-target Edition-II → Edition-III with ANTI-SUBSTRING care:
  //          the E2 pattern /Edition-II/g would ALSO match "Edition-III" (prefix); the E3 hyphen pattern
  //          must therefore END on a token boundary — /Edition-III(?!I)/g (matches "Edition-III" exactly,
  //          NOT a future "Edition-IIII"). The redundant space form is /· Edition III(?!I)/g. At the
  //          Edition-III footer only atlasVersion ("Edition-III") carries the token → nHyphen=1, nSpace=0.
  {
    // REFIT provenance-dedupe: the footer carries the candidate version token ("Refit-Candidate-1", the
    // atlasVersion form) EXACTLY ONCE, and no "Edition …" edition-stamp token leaks into the footer.
    let dedupeOk = true, dedupeDetail = [];
    const verTok = String(atlasVersion); // "Refit-Candidate-1"
    for (const sk of ['instrument', 'archive']) {
      const m = bodies[sk].match(new RegExp(`<text x="[\\d.]+" y="1188\\.00">(${esc(verTok)}[^<]*)</text>`));
      const footerLine = m ? m[1] : '';
      const nVer = (footerLine.match(new RegExp(esc(verTok), 'g')) || []).length;
      const nEd = (footerLine.match(/Edition[\s-]I{1,3}\b/g) || []).length; // any Edition-N leak in the footer
      if (!(footerLine && nVer === 1 && nEd === 0)) { dedupeOk = false; }
      dedupeDetail.push(`${sk}: version-token "${verTok}"×${nVer} (want 1), edition-token-leak×${nEd} (want 0)`);
    }
    rec('refit-provenance-dedupe', dedupeOk, dedupeDetail.join(' | '));
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
      esc('emitted alongside (served-truth reference) — hover'),
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
  // (29) REFIT — the r7 RESTYLE-REGRESSION vs the e21 baseline (geometry byte-frozen vs Edition-II) is
  //      RETIRED (a NEW fit re-derives all mark geometry; there is no e21 freeze record for the candidate
  //      corpus). REPLACED by a self-contained geometry skin-invariance check: point circles, tombstone
  //      daggers, ground glyph circles, and the CHARTED-HORIZON hull polyline are BYTE-IDENTICAL between
  //      the two skins (the geometry is skin-independent by construction — only fills/ink differ). No
  //      external baseline is read. (Full-render determinism is asserted separately at acc-double-render.)
  {
    let regPass = true; const regDetail = [];
    const ptGeomRe = /<circle cx="([\d.]+)" cy="([\d.]+)" r="([\d.]+)"[^>]*><title>([^<]*)<\/title><\/circle>/g;
    const ptGeom = (svg) => { const a = []; let m; while ((m = ptGeomRe.exec(svg))) a.push(`${m[1]}|${m[2]}|${m[3]}|${m[4]}`); ptGeomRe.lastIndex = 0; return a.sort().join('\n'); };
    const tombGeomRe = /<text x="([\d.]+)" y="([\d.]+)" font-size="16" text-anchor="middle"[^>]*>†<title>([^<]*)<\/title><\/text>/g;
    const tombGeom = (svg) => { const a = []; let m; while ((m = tombGeomRe.exec(svg))) a.push(`${m[1]}|${m[2]}|${m[3]}`); tombGeomRe.lastIndex = 0; return a.sort().join('\n'); };
    const groundGeomRe = /<circle cx="([\d.]+)" cy="([\d.]+)" r="([\d.]+)"(?:\s+data-[^>]*)?\/>/g;
    const groundGeom = (svg) => { const a = []; let m; while ((m = groundGeomRe.exec(svg))) a.push(`${m[1]}|${m[2]}|${m[3]}`); groundGeomRe.lastIndex = 0; return a.sort().join('\n'); };
    const hullRe = /<polyline points="([^"]+)" fill="none"/;
    const hullPts = (svg) => { const m = svg.match(hullRe); return m ? m[1] : 'NO-HULL'; };
    const pEq = ptGeom(bodies.instrument) === ptGeom(bodies.archive);
    const tEq = tombGeom(bodies.instrument) === tombGeom(bodies.archive);
    const gEq = groundGeom(bodies.instrument) === groundGeom(bodies.archive);
    const hEq = hullPts(bodies.instrument) === hullPts(bodies.archive);
    const nPt = ptGeom(bodies.instrument).split('\n').filter(Boolean).length;
    const nG = groundGeom(bodies.instrument).split('\n').filter(Boolean).length;
    regPass = pEq && tEq && gEq && hEq;
    regDetail.push(`RETIRED e21 byte-freeze (new fit). Skin-invariant geometry: points(${nPt})=${pEq ? 'IDENTICAL' : 'DIFFER'} tombs=${tEq ? 'IDENTICAL' : 'DIFFER'} ground(${nG})=${gEq ? 'IDENTICAL' : 'DIFFER'} hull=${hEq ? 'IDENTICAL' : 'DIFFER'}`);
    rec('geometry-skin-invariance', regPass, regDetail.join(' | '));
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
      // (iii) content-locked axis strings grep verbatim. E2.3: west/east rail arrow glyphs swapped
      //       to read OUTWARD on screen (source `PERFORM ↓` / `↑ DEPLOY` under rotate(-90)).
      const locked = ['PERFORM ↓', '↑ DEPLOY', '↑ LAUNCH', 'EMBODY ↓', POLE_GLOSS.PERFORM, POLE_GLOSS.DEPLOY, POLE_GLOSS.LAUNCH, POLE_GLOSS.EMBODY].map(esc);
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
  //      grep-match emitted fields; doctored-input (a hook value absent from atlas-edition3.json) →
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
      const classedOk = nClassed === 665 && nClassed === active.length + supplementary.length;   // REFIT: 506 → 665 (candidate corpus)
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
      hkDetail.push(`${skin}: live ${nLive}/${neutral.length}=${liveOk} cond ${nCond}/${grouped.length}=${condOk} grave ${nGrave}/${supplementary.length}=${graveOk} classed ${nClassed}/665=${classedOk} ghost ${nGhost}/${ghostGlyphs.length + drillGlyphs.length}=${ghostOk} layers-missing=${layerMiss.join(',') || 'none'} badKit=${badKit ?? 'none'} badCore=${badCore ? 'YES' : 'none'} badMember=${badMember ?? 'none'}`);
    }
    rec('r7-hooks-integrity', hkPass, hkDetail.join(' | '));
  }

  // (31b) r7 HOOKS DOCTORED-INPUT HALT (spec §7 acc-31 last clause): a hook value ABSENT from
  //       atlas-edition3.json must HALT. We prove the integrity check is COMPUTED-NOT-BLIND by
  //       synthesizing a doctored current-body (inject a data-kit not in the emitted kit_id set) and
  //       asserting the same reconciliation logic REJECTS it. In-process (no child render needed —
  //       the guard is a pure function of the emitted set + the SVG body). DIFF site 8 (message).
  {
    const kitIdSet = new Set(all.map((p) => p.kit_id));
    const doctored = bodies.instrument.replace(/data-kit="[^"]*"/, 'data-kit="zz-ghost-kit-not-emitted"');
    const kitVals = [...doctored.matchAll(/data-kit="([^"]*)"/g)].map((m) => m[1]);
    const caught = kitVals.some((v) => !kitIdSet.has(v));
    rec('r7-hooks-doctored-halt', caught, caught
      ? 'injected data-kit="zz-ghost-kit-not-emitted" (absent from atlas-edition3.json) → integrity check REJECTS (computed-not-blind)'
      : 'doctored hook value NOT caught — integrity check is blind (FAIL)');
  }

  // ---- SMOKE TESTS (GATING — edition-safe, structure-only) ----
  const smokes = [];
  const csmoke = (name, pass, detail) => smokes.push({ name, pass, detail });
  // DEMOTED OBSERVATIONS (`observations`/`obs`) are declared up in the acceptance section so the
  // orientation smokes + the meso-beyond group profile below record into the same list.
  const wc = groupCentroids['WHIRLWIND'];
  obs('WHIRLWIND x>0 (E1 ref PERFORM side)', wc.x > 0, `x=${wc.x.toFixed(4)}`, 'E1-orientation: x>0');
  obs('WHIRLWIND y<0 (E1 ref EMBODY side)', wc.y < 0, `y=${wc.y.toFixed(4)}`, 'E1-orientation: y<0');
  const tc = groupCentroids['TOTEM-SENTRY'];
  obs('TOTEM-SENTRY x<0 (E1 ref DEPLOY side)', tc.x < 0, `x=${tc.x.toFixed(4)}`, 'E1-orientation: x<0');
  const cd = all.find((p) => p.kit_id === 'poe1-charged-dash');
  const distToWC = cd ? Math.hypot(cd.x - wc.x, cd.y - wc.y) : Infinity;
  const planeDiag = Math.hypot(maxX - minX, maxY - minY);
  obs('charged-dash near WHIRLWIND condensation', cd != null && distToWC < 0.20 * planeDiag,
    `dist=${distToWC.toFixed(3)} (thr ${(0.20 * planeDiag).toFixed(3)} = 20% diag)`, 'E1: dist < 20% diag');
  // REFIT — "all lit ghost glyphs inside the frame" is DEMOTED to an observation. In Edition III the
  // frozen Edition-I frame contained every lit cell; the candidate re-derives the frame from its own
  // points, so a lit ghost cell can land just outside (disclosed on the clip line + surfaced here). Not
  // gating — the honest-frame law (points-only, don't force Edition-III bounds) makes this a finding.
  const litInBox = ghostLit.every((g) => g.sxv >= M.left - 0.5 && g.sxv <= M.left + PW + 0.5 && g.syv >= M.top - 0.5 && g.syv <= M.top + PH + 0.5);
  obs('all lit ghost cells inside candidate frame', litInBox && ghostClippedLitCount === 0,
    `${ghostClippedLitCount} lit cell(s) just outside points-derived frame (of ${ghostLit.length} lit glyphs); DISCLOSED on clip line`, 'Edition-III (frozen E1 frame): 0 lit outside');
  // coincidence multiplicity present (proves aggregation ran)
  const maxMult = Math.max(...ghostGlyphs.map((g) => g.mult));
  csmoke('coincident-projection aggregation active', maxMult > 1, `max multiplicity=${maxMult} (aggregated ${feasibleCells.length} cells -> ${ghostGlyphs.length} glyph positions)`);
  // hull sanity: a convex hull of the ghost field is a small polygon.
  csmoke('ghost hull is a small polygon', ghostHullVertexCount >= 3 && ghostHullVertexCount <= 60,
    `hull vertex count=${ghostHullVertexCount}`);
  const hullEastWorldX = Math.max(...ghostHullWorld.map(([x]) => x));
  const settledEastWorldX = Math.max(...all.map((p) => p.x));
  // CHARTED horizon (meso ∪ drill-in) reaches EAST BEYOND the settled kits (P-DF-1 realized) — this is
  // the load-bearing charted-horizon claim and it re-derives from the candidate's own points.
  csmoke('CHARTED horizon east reach EXCEEDS settled kits (P-DF-1 realized)', chartedHullEastX > settledActiveEastX,
    `charted hull east x=${hullEastWorldX.toFixed(4)} > settled-active east x=${settledActiveEastX.toFixed(4)} (+${(chartedHullEastX - settledActiveEastX).toFixed(4)}) [meso-only east was ${mesoOnlyHullEastX.toFixed(4)} < settled ${settledEastWorldX.toFixed(4)}]`);
  // REFIT density RE-POINT: the headline ratios are RE-DERIVED from the candidate's OWN counts, then
  // GATED on the candidate's own arithmetic (not the Edition-III constants). lit-fraction 202/11,160 =
  // 1.8% (numerator+denominator byte-identical to Edition-III — the refit changed the FIT, not the
  // lattice cardinality → UNCHANGED). density active/lit = 628/202 = 3.1 (the corpus grew 469→628 →
  // CHANGED vs Edition-III's 2.3; gated on the honest 3.1). Both landings recorded as observations too.
  csmoke('headline lit-fraction re-derived (candidate counts)', fmt1(litFractionPct) === '1.8', `lit fraction=${fmt1(litFractionPct)}% (${litCells}/${denomMesoFeasible})`);
  csmoke('headline density re-derived (candidate counts)', fmt1(kitsPerLitCell) === fmt1(counts.active / litCells), `density=${fmt1(kitsPerLitCell)} (${counts.active}/${litCells})`);
  obs('headline lit-fraction vs Edition-III', fmt1(litFractionPct) === '1.8', `${fmt1(litFractionPct)}% (${litCells}/${denomMesoFeasible})`, 'Edition-III: 1.8% (202/11,160)');
  obs('headline density vs Edition-III', fmt1(kitsPerLitCell) === '2.3', `${fmt1(kitsPerLitCell)} (${counts.active}/${litCells})`, 'Edition-III: 2.3 (469/202)');
  // REFIT beyond-horizon: the meso-beyond N cross-check (== emitted p_df_1.n_beyond_horizon_kits 13) is
  // HALT-guarded at module load. Here it is reported as an observation (vs Edition-III's 14). The
  // CHARTED-hull beyond-N == 0 is a GATING structure smoke (the §10 census: charted hull encloses all).
  obs('meso-hull beyond-N (== emitted p_df_1)', beyondMesoOnlyCount === 13, `${beyondMesoOnlyCount} (== emitted p_df_1.n_beyond_horizon_kits ${P_DF_1_N_BEYOND_HORIZON})`, 'Edition-III: 14');
  csmoke('CHARTED-hull beyond-N == 0 (drill-in encloses settled kits)', beyondHorizonCount === 0, `charted-hull N=${beyondHorizonCount} active kits beyond the charted reach`);
  // The beyond-MESO group profile CHANGED (different corpus + refit) — an observation, not a gate.
  {
    const byGrp = {};
    for (const p of beyondMesoOnlyKits) { const g = p.gateA_group ?? 'NEUTRAL'; byGrp[g] = (byGrp[g] || 0) + 1; }
    const profStr = Object.entries(byGrp).sort().map(([k, v]) => `${k}:${v}`).join(', ');
    const ww = byGrp['WHIRLWIND'] || 0, cb = byGrp['CHANNELED-BEAM'] || 0, nu = byGrp['NEUTRAL'] || 0;
    obs('meso-beyond group profile', ww === 10 && cb === 3 && nu === 1, profStr, 'Edition-III: WHIRLWIND:10, CHANNELED-BEAM:3, NEUTRAL:1');
  }
  csmoke('point-in-charted-hull: ALL actives INSIDE (N==0)', beyondHorizonCount === 0,
    `${beyondHorizonCount} beyond / ${active.length} active = ${fmt1((beyondHorizonCount / active.length) * 100)}% (the charted horizon encloses the whole settled archipelago)`);

  // REFIT below-plane ledger-band geometry smokes. Verify: the below-plane ledger header is present
  // (candidate identity "Refit Candidate 1 lattice", NOT an edition tag); the census footer end-anchors
  // at the plane right edge; the drill-in subordinate ground actually rendered.
  {
    const inst = bodies.instrument;
    csmoke('below-plane ledger header present (candidate identity)', inst.includes(`${REFIT_DISPLAY} lattice`), `ledger header "${REFIT_DISPLAY} lattice" rendered below plane`);
    const censusM = inst.match(/<text x="([\d.]+)" y="1188\.00" text-anchor="end">points:/);
    const censusX = censusM ? parseFloat(censusM[1]) : NaN;
    csmoke('footer census at plane right edge', Math.abs(censusX - (M.left + PW)) < 0.01,
      `census end-anchor x=${censusX.toFixed(2)} == plane-right ${(M.left + PW).toFixed(2)}`);
    csmoke('drill-in subordinate ground rendered', drillGlyphs.length > 0,
      `${fmtInt(subGlyphField.length)} emitted glyph-field entries → ${fmtInt(drillGlyphs.length)} aggregated drill glyphs (Σmult=${fmtInt(subGlyphField.reduce((s, e) => s + e.multiplicity, 0))})`);
  }

  // ---- report ----
  console.log('\n================= ACCEPTANCE TESTS (re-pointed) =================');
  for (const t of tests) console.log(`  [${t.pass ? 'PASS' : 'FAIL'}] ${t.name} :: ${t.detail}`);
  console.log('================= SMOKE TESTS (gating) =================');
  for (const t of smokes) console.log(`  [${t.pass ? 'PASS' : 'FAIL'}] ${t.name} :: ${t.detail}`);
  console.log('================= DEMOTED OBSERVATIONS (reported, NOT gating) =================');
  for (const o of observations) console.log(`  [${o.flag}] ${o.name} :: refit=${o.refit} | old-expectation: ${o.expectation}`);

  // GATING is tests + smokes ONLY. Observations are REPORTED (a CHANGED observation does NOT fail the run —
  // the refit legitimately moves these; they are comparison evidence, brief §4).
  const allPass = [...tests, ...smokes].every((t) => t.pass);
  console.log(`\n${allPass ? 'ALL PASS (gating)' : 'FAILURES PRESENT (gating)'} · observations: ${observations.filter((o) => o.flag === 'PASS').length} PASS / ${observations.filter((o) => o.flag === 'CHANGED').length} CHANGED (non-gating)`);

  const note = buildNote(results, tests, smokes, observations, ptFps, ghFps);
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
    render: 'galadriel/pipeline/atlas-refit-candidate-1-render.mjs',   // REFIT candidate render head
    edition: editionTag,                                       // "Refit-Candidate-1" (data-derived)
    display_identity: REFIT_DISPLAY,                           // "Refit Candidate 1"
    unratified_comparison_artifact: unratifiedFlag,            // true — NOT an Edition
    comparison_note: comparisonNote,
    emitted_alongside: emittedAlongside,                       // the ONLY "Edition III" reference on/around this plate
    authority: 'Matt 2026-07-16 verbatim: "I want to see both versions so we cna make a decision." · gandalf brief 2026-07-16-galadriel-a-render-refit-candidate-plates-brief.md · ultra-think record agentic_orchestration/gandalf/notes/2026-07-16-tier3-refit-and-polish-spec.md §3.',
    what_this_is: 'A COMPARISON plate (NOT an Edition) for Matt\'s Tier-3 atlas refit adoption decision: Refit Candidate 1 (full re-derivation of the FIT on the 628-active corpus) vs served Edition III. FURNITURE is byte-verbatim from the FINAL FIXED r8-furniture head (944afa98) — Matt compares STRUCTURE, not presentation. The strings "Edition IV"/"edition4" appear NOWHERE; "Edition III" appears ONLY in the emitted_alongside provenance line.',
    forked_from: 'atlas-edition3-r8-furniture-render.mjs (944afa98) — FURN table + key/ledger forms + skins carried byte-verbatim; identity + acceptance-adaptation seams differ per the brief.',
    plane_alignment: {
      disclosed_on_plate: true,
      method: planeAlignMethod,
      rotation_deg: planeAlignRotDeg,
      det: planeAlignDet,
      headline: planeAlignHeadline,
      Q: planeAlign.Q,
      raw_corr_before: planeAlign.raw_corr_before,
      corr_after: planeAlign.corr_after,
      note: 'Emitted coordinates are plane-ALIGNED to Edition-I orientation (in-plane orthogonal Procrustes, rotation+reflection, no scaling). Distances/spreads/congruence/gates/plane-inertia are Q-invariant; only the arbitrary MCA/SVD orientation convention changes. Per-axis inertia NOT rendered (aligned x/y are not pure dims 1/2); plane-level 8.903% is subspace-invariant and rendered.',
    },
    pole_labels: 'Edition-I REFERENCE orientation labels (PERFORM/DEPLOY/LAUNCH/EMBODY marked "(E1 ref)") + gloss "poles = Edition-I reference orientation; refit axes unratified". The refit basis carries NO ratified axis names (basis.axis_names is a {note} object).',
    acceptance_adaptation: 'Per brief §ACCEPTANCE ADAPTATION: frozen-baseline checks RETIRED (fit-freeze vs r6/e21, basis==edition2 assert, N==469/506, edition-stamp greps, edition===3); internal-consistency checks RE-POINTED to the candidate\'s own emitted counts (fail-loud); hull/census/P-DF-1 RECOMPUTED + CROSS-CHECKED vs emitted p_df_1 (mismatch = HALT); Edition-I orientation smokes DEMOTED to REPORTED observations (print refit value + old expectation + PASS/CHANGED; not gating); anti-stale greps for Edition IV absence + Edition III only-in-emitted_alongside.',
    render_vs_emission_crosscheck: {
      meso_beyond_render: beyondMesoOnlyCount,
      p_df_1_n_beyond_horizon_emitted: Number(P_DF_1_N_BEYOND_HORIZON),
      match: beyondMesoOnlyCount === Number(P_DF_1_N_BEYOND_HORIZON),
      charted_beyond_render: beyondHorizonCount,
      note: 'render pass beyond-MESO-hull N MUST equal emitted ghost_field.p_df_1.n_beyond_horizon_kits (HALT-guarded at module load). charted-hull beyond-N is a computed consequence.',
    },
    furniture_factor_table: FURN,
    atlas_version: atlasVersion,
    register_ref: registerRef,
    input: 'agentic_orchestration/research/curated/atlas/atlas-refit-candidate-1.json',
    emitted_at: emittedAt,
    emitter_script: emitterScript,
    hook_reconciliation: hookRecon,
    // SKIN→CANVAS MAP — downstream binds to CANVAS, never to skin NAME. instrument=LIGHT #f7f8fa; archive=DARK.
    skin_canvas_map: SKIN_CANVAS_MAP,
    basis: { frozen: frozen, inertia_pct: inertiaPct, retained_dims: retainedDims, axis_names: axisNames },
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
    // P-DF-1 machine-readable verdict — from the emitted p_df_1 block (single source; no top-level mirror
    // on the candidate). RECOMPUTED + CROSS-CHECKED render-side (see render_vs_emission_crosscheck above).
    p_df_1: {
      verdict: pDf1Verdict,
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

function buildNote(results, tests, smokes, observations, ptFps, ghFps) {
  const line = (t) => `- [${t.pass ? 'PASS' : 'FAIL'}] **${t.name}** — ${t.detail}`;
  const obsLine = (o) => `| ${o.name} | ${o.refit} | ${o.expectation} | **${o.flag}** |`;
  const hullEastWorldX = Math.max(...ghostHullWorld.map(([x]) => x));
  const settledEastWorldX = Math.max(...all.map((p) => p.x));
  const passCount = tests.filter((t) => t.pass).length;
  const failCount = tests.length - passCount;
  const smokePass = smokes.filter((t) => t.pass).length;
  const depthSum = feasibleCells.reduce((s, c) => s + c.depth, 0);
  const subSealedSum = subSealedLedger.reduce((s, r) => s + r.count, 0);
  const subGlyphMultSum = subGlyphField.reduce((s, e) => s + e.multiplicity, 0);
  const obsChanged = observations.filter((o) => o.flag === 'CHANGED');
  const allPassGating = [...tests, ...smokes].every((t) => t.pass);
  return `# Build Horizon — ${REFIT_DISPLAY} · UNRATIFIED COMPARISON ARTIFACT · verification note

> **THIS IS NOT AN EDITION.** It is a comparison plate for Matt's Tier-3 atlas refit **adoption decision**
> (${REFIT_DISPLAY} — a full re-derivation of the FIT on the 628-active corpus — vs the served **Edition III**).
> The served truth (\`atlas-edition3.json\`) is **byte-untouched**; the interactive \`/atlas\` still serves it.
> The candidate reaches Matt as **static plates** (interactivity follows adoption, not precedes it). Nothing
> here is ratified. **Authority:** Matt 2026-07-16 "I want to see both versions so we cna make a decision."
> · gandalf brief \`2026-07-16-galadriel-a-render-refit-candidate-plates-brief.md\`.

**emitted alongside:** ${emittedAlongside}
**comparison note (emitted):** ${comparisonNote}

## The three laws that frame this plate

1. **Comparison, not edition.** Title reads **"Build Horizon — ${REFIT_DISPLAY}"** (no "Edition" word). The
   strings "Edition IV"/"edition4" appear NOWHERE. "Edition III" appears ONLY in the emitted_alongside
   provenance line (the served-truth reference), never as this plate's own identity (anti-stale grep enforced).
2. **Plane ALIGNED to Edition-I orientation — disclosed.** Every plane coordinate (points, ghost cells,
   drill-in, hull, p_df_1) is Q-aligned to Edition-I orientation via ${planeAlignMethod} (rotation
   **${planeAlignRotDeg}°**, det **${planeAlignDet}**, no scaling, no translation; fit on ${planeAlign.shared_actives} shared actives).
   The refit plane rotated ~117° + reflected vs Edition-I; reflection-only alignment was insufficient (raw
   dim1 same-index corr ${planeAlign.raw_same_index_dim1}). Distances/spreads/congruence/gates/plane-inertia are
   **Q-invariant**; only the arbitrary MCA/SVD orientation convention changes. **Per-axis inertia is NOT
   rendered** (the aligned x/y are not pure dims 1/2); the **plane-level ${inertiaPct}%** corrected inertia IS
   rendered (subspace-invariant). Disclosed in the banner + headlined here.
3. **Poles = Edition-I REFERENCE orientation.** The refit basis carries NO ratified axis names
   (\`basis.axis_names\` is a {note} object). The four poles render as Edition-I reference labels
   (PERFORM/DEPLOY/LAUNCH/EMBODY, each marked **"(E1 ref)"**) + the gloss "poles = Edition-I reference
   orientation; refit axes unratified". They are never presented as the candidate's own ratified identities.

## Structure (apples-to-apples with Edition III)

- **Furniture byte-verbatim** from the FINAL FIXED r8-furniture head (\`944afa98\`) — Matt compares STRUCTURE,
  not presentation. The FURN factor table, BUILD FAMILIES key, ledger form, both skins carried unchanged.
- **Plane bounds** re-derived from the candidate's OWN points (points-only + 6% pad law) — the candidate has
  its own honest frame; Edition III's bounds are NOT forced.

## Render vs emission cross-check (RECOMPUTE + CROSS-CHECK — the load-bearing part)

The head recomputes the hull, the beyond-horizon N, and the P-DF-1 mechanism per its standing law and
**MATCHES the emitted \`ghost_field.p_df_1\`** (a mismatch is a finding → HALT, never a tolerance):

- **P-DF-1 VERDICT: ${pDf1Verdict}** — S_max **${pDf1.S_max}** ${pDf1.S_max > pDf1.K_max_beyond_horizon ? '>' : '<='} K_max **${pDf1.K_max_beyond_horizon}**; falsified=**${pDf1Falsified}**; n_beyond_horizon_kits **${pDf1.n_beyond_horizon_kits}**.
- **beyond-MESO-hull N (render pass) = ${beyondMesoOnlyCount}** == emitted \`p_df_1.n_beyond_horizon_kits\` **${Number(P_DF_1_N_BEYOND_HORIZON)}** ✓ (HALT-guarded at module load).
- **charted-hull beyond-N (render pass) = ${beyondHorizonCount}** — the charted horizon (meso ∪ drill-in) encloses the whole settled archipelago (§10 census: all overshoot EAST-side, charted-hull beyond-N=0).
- **depth Σ = ${fmtInt(depthSum)}** == \`depth_sum_check\` **${fmtInt(depthSumCheck)}** == exact_post_red_law **${fmtInt(denomFeasibleExact)}** (byte-equal to Edition-III's — the lattice did not move).
- **drill-in:** Σmultiplicity **${fmtInt(subGlyphMultSum)}** == \`n_sub_feasible\` **${fmtInt(drillSubFeasibleN)}**; sub-sealed Σ **${fmtInt(subSealedSum)}** == \`n_sub_sealed\` **${fmtInt(drillSubSealedN)}**; parent cells **${fmtInt(drillParentCells)}**.

## Acceptance tally (re-pointed set)

- **ACCEPTANCE: ${passCount}/${tests.length} PASS** (${failCount} fail) · **SMOKE (gating): ${smokePass}/${smokes.length} PASS** · **gating overall: ${allPassGating ? 'ALL PASS' : 'FAILURES PRESENT'}**.
- **Acceptance adaptation (per brief):** frozen-baseline checks **RETIRED** (fit-freeze vs r6/e21; basis==edition2 assert; N==469/506; Edition-III lit/census constants; edition-stamp greps; edition===3). Internal-consistency checks **RE-POINTED** to the candidate's own emitted counts (fail-loud). Hull/census/P-DF-1 **RECOMPUTED + CROSS-CHECKED** vs emitted (mismatch = HALT). Edition-I orientation smokes **DEMOTED** to reported observations (below). Anti-stale greps added.

## Demoted observations (REPORTED, NOT gating)

These are refit-dependent (the plane was re-derived + Q-aligned). A **CHANGED** flag does NOT fail the run —
it is comparison evidence. ${obsChanged.length === 0 ? '**All observations PASS** (the Q-alignment restored Edition-I-orientation congruence).' : `**${obsChanged.length} CHANGED** (the refit legitimately moved these).`}

| observation | refit value | Edition-I / Edition-III expectation | flag |
|---|---|---|---|
${observations.map(obsLine).join('\n')}

## Outputs

- instrument (LIGHT): \`${results.instrument.svgPath}\` + \`${results.instrument.pngPath}\`
- archive (DARK): \`${results.archive.svgPath}\` + \`${results.archive.pngPath}\`

## Provenance law

chart = render(\`atlas-refit-candidate-1.json\`). No number/label/coordinate originates outside an
\`atlas-refit-candidate-1.json\` field. Layout is computed; content is not. The ghost hull's
**${ghostHullVertexCount}** vertices + beyond-horizon N are COMPUTED from the emitted candidate field and
cross-checked against the emitted p_df_1; the pull-slice / drill-in / off-plane / P-DF-1 numerals are all
rendered from emitted fields; the drill-in glyph field is emitted pre-aggregated and re-aggregated by the
frozen projection. Content-locked disclosure copy is carried VERBATIM. **atlas_version:** ${atlasVersion} ·
**edition:** ${editionTag} · **register:** ${registerRef} · **basis frozen:** ${frozen} (unratified) ·
**plane inertia:** ${inertiaPct}% · **retained dims:** ${retainedDims} · **emitted_at:** ${emittedAt} ·
**emitter:** ${emitterScript}. Determinism: sorted iteration; no RNG; no wall-clock; re-render byte-equal.

## Acceptance tests
${tests.map(line).join('\n')}

## Smoke tests (gating)
${smokes.map(line).join('\n')}
`;
}

main();
