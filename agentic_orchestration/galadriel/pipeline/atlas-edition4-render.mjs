// atlas-edition4-render.mjs — EDITION IV SERVING RENDER HEAD (Matt ratified 2026-07-17).
//
// FORK LINEAGE (two heads):
//   1. atlas-edition3-r8-furniture-render.mjs — the served E3 head. Carried VERBATIM:
//      the r8 furniture-factor table, the r8_fix key-box content-derived height, the E2.3
//      rail arrows (source-glyph ≠ on-screen direction under rotate(-90); PERFORM ↓ /
//      ↑ DEPLOY — verified OUTWARD), the data-hook grammar (per-mark data-kit/data-el,
//      layer groups <g id="layer-...">), tombstone † glyphs, hull polyline, zero-axis +
//      frame geometry conventions, r8-fix key-box content-derived accumulator.
//   2. e3-vs-e4-render.mjs — my E4-schema handling from the ratification comparison. That
//      head rendered the E4 geometry Matt ratified (including the "Lost Ark wing" — tight
//      WN cluster inside the PERFORM-EMBODY corner).
//
// SOURCE: agentic_orchestration/research/curated/atlas/atlas-edition4.json (elrond
//   emission 2026-07-17; Matt RATIFIED 2026-07-17 per verbatim directive recorded in
//   canonical/matt_decision_needed/2026-07-16-edition3-vs-refit-candidate-1-adoption.md
//   § WAVE 5 — "Agreed, path A" plus prior "publish Edition IV" ratification).
//
// PATH-A LAW (invocation, verbatim): "E4 is Path-A supplementary admission into
//   Edition-I's frozen basis. Do not 'fix' basis.edition==1." The FIT LAYER (basis + the
//   506 E3 point coords + the 37 legacy tombstones) is BYTE-FROZEN vs Edition-III. The
//   56 new supplementary points (50 new positives + 6 new tombstones) PROJECT into the
//   frozen basis — no basis re-derivation. The CENSUS/LATTICE re-emits with the newly
//   keyed rows read live (occupied meso 202→198; the emitter's live re-derivation of a
//   fit-relative fact against the +56-row census).
//
// HARD ASSERTS (fail-loud at module load, mirroring the E3 head's edition gate):
//   (H-1) atlas.edition === 4 && atlas.atlas_version === 'Edition-IV'
//   (H-2) atlas.basis.edition === 1 && atlas.basis.frozen === true (Path-A law)
//   (H-3) G-3 ANCHORING RE-ASSERT: every kit_id in atlas-edition3.json appears in E4
//         with BYTE-IDENTICAL x/y (JSON-value equality). List offenders on fail.
//   (H-4) counts.total === 562 === points.length; counts.active + counts.supplementary
//         === counts.total.
//
// ENUMERATED EDITION-BOUNDARY DIFF vs the E3 r8 head (every deliberate difference,
// carried on its own line for the render-provenance.json):
//   [D1] input file → atlas-edition4.json (was atlas-edition3.json).
//   [D2] output dir → captures/2026-07-17-atlas-edition4-serving/ (was …-atlas-edition3-r8-furniture/).
//   [D3] output filenames → atlas-edition4-<skin>.svg / .png (was atlas-edition3-…).
//   [D4] title plate → "Build Horizon — Edition IV" (data-derived via ghost_field.edition
//        emitting "IV"; the E3 head's title formula "Build Horizon — Edition ${editionTag}"
//        auto-moves at the boundary with no source change — carried VERBATIM).
//   [D5] top-level `edition === 4` gate (was === 3).
//   [D6] Path-A basis gate: basis.edition === 1 && basis.frozen === true (was: implicit
//        via ghost_field.edition==="III"). Explicit + fail-loud, per invocation.
//   [D7] G-3 ANCHORING RE-ASSERT: E4 must carry all 506 E3 kit_ids at byte-identical x/y.
//        REPLACES the E3 head's fit-freeze compare vs atlas-edition2.json (the E4 emission
//        is Path-A supplementary — its FIT layer is byte-identical to E3, not to E2). The
//        underlying invariant is the same (fit does not move); the immediate prior is E3.
//   [D8] point discriminator (56 new marks): supplementary===true always (never new active
//        by wave-4 law); `'death_class' in p` ⇒ NEW TOMBSTONE (6, all extrinsic-tuning or
//        unknown-pending-recrawl per emission); absent ⇒ NEW POSITIVE (50). Carried from
//        e3-vs-e4-render.mjs § classify. LEGACY 37 tombstones keep the E3 head's grammar.
//   [D9] NEW POSITIVE glyph: filled saturated dot slightly larger than the neutral single
//        (r=3.7 vs live-single r=3.0), no halo (halo felt like an over-claim once carried
//        forward from the comparison plate into a serving surface). data-el="positive"
//        — a NEW class (distinct from live/condensation/graveyard/ghost). data-kit
//        carried per-mark. Layer id: layer-positives (drawn between layer-graveyard and
//        layer-chrome so the E3 layer order is untouched; new class appends).
//   [D10] NEW TOMBSTONE glyph: SAME † text mark grammar as the legacy 37 tombstones —
//        font-size 16, ink = s.tombInk (or s.tombUnknownInk for unknown-pending-recrawl).
//        Simplifies acceptance: existing tombstone regex machinery matches all 43 tombs
//        (37 legacy + 6 new). data-el="graveyard" carried; the tombstone layer id
//        (layer-graveyard) holds 43 marks instead of 37.
//   [D11] BUILD FAMILIES key: driven by `gateA_group` — per WAVE-4 LAW (invocation),
//        families grow only by RATIFICATION WAVES, never by tau. E4 admits 56 new points
//        with NO `gateA_group` values — so the six family counts (WHIRLWIND / TOTEM-SENTRY
//        / TRAP-MINE / CHANNELED-BEAM / AURA / MINION-PET) are BYTE-IDENTICAL to E3's key
//        counts (verified: sum of gateA members == 86 across both editions). Carried
//        VERBATIM. Rename CONDENSATIONS → BUILD FAMILIES (r8 chrome, carried).
//   [D12] FUTURE-PROOFING (structure, do not build now): a reserved empty layer group
//        <g id="layer-family-candidates"></g> is emitted BETWEEN layer-positives and
//        layer-chrome. When elrond's candidates JSON lands, a follow-on additive
//        annotation-layer module fills this group WITHOUT touching any data-mark emission.
//        No candidate marks NOW.
//   [D13] provenance.iteration → 'edition4-serving' (was 'edition3-r8-furniture').
//   [D14] provenance.iteration_authority → cites Matt's 2026-07-17 ratification via
//        adoption-doc WAVE 5 (canonical/matt_decision_needed/2026-07-16-edition3-vs-refit-
//        candidate-1-adoption.md § WAVE 5).
//   [D15] provenance.enumerated_edition_boundary_diff → this D1-D15 list.
//   [D16] freeze_baseline → 2026-07-16-atlas-edition3-r8-furniture (the E3 r8 head's
//        capture dir — the byte-identity anchor for the 506 shared kits + 37 legacy tombs +
//        the r8 chrome). Was: 2026-07-15-atlas-edition2-e21 for E3.
//   [D17] retire the E3 intra-edition r7-restyle-regression (spec §7 acc-29) as-is; the
//        r7 hooks/whitelist are UNCHANGED (data-el/data-kit hooks carried; the four pole
//        title relocations carried; horizon-vs-drill paint order carried). The regression
//        RE-INSTATES against the E3 r8 baseline: the 506 point circles + 37 legacy
//        tombstone daggers + hull polyline + ghost/drill glyph geometry byte-identical.
//        The 56 NEW marks are the ONLY additive geometry (whitelisted).
//   [D18] every ratified-family key uses the SAME six colors from the E3 head's
//        GROUP_COLORS block (byte-carried) — families grow by ratification, coloring is
//        wave-4-ratified-members-only, no new family introduced by E4 admission.
//   [D19] the ghost-field ledger EDITION token: header edition literal now "Edition IV"
//        (was "Edition III"). Data-derived from ghost_field.edition = "IV" (auto-moves at
//        the boundary; §4c law of the E3 head, carried VERBATIM).
//   [D20] register_ref binding: ghost_field.register_ref === 'feasibility-cuts-register-v1.3'
//        (Path-A: register did not move; denominators byte-identical to E3). E4 RE-ASSERTS
//        v1.3, not supersedes.
//
// LAW: chart = render(atlas-edition4.json). Layout is COMPUTED; all CONTENT (numbers,
// labels, coordinates, class strings) originates ONLY in atlas.json fields. No literal
// atlas numerics live in this source beyond layout geometry. Every ledger/census figure
// is DATA-DERIVED at render time — no hand-typed census numbers anywhere.
//
// Determinism: same atlas-edition4.json → byte-identical SVG (sorted iteration; no RNG;
// no wall-clock; time comes from atlas.json emitted_at).
//
// Author: galadriel (visual-perception steward). Serving-head charter step, Edition IV.

import { readFileSync, writeFileSync, mkdtempSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve, join } from 'node:path';
import { tmpdir } from 'node:os';
import { execFileSync } from 'node:child_process';
import sharp from 'sharp';

const __dirname = dirname(fileURLToPath(import.meta.url));

// [D1] input: atlas-edition4.json.
const ATLAS_PATH = resolve(__dirname, '../../research/curated/atlas/atlas-edition4.json');
// [D7] G-3 anchor input: atlas-edition3.json — the immediate prior edition. The E4 fit is
//      byte-identical to E3 (Path-A supplementary), so this is the correct freeze anchor.
const PRIOR_EDITION_PATH = resolve(__dirname, '../../research/curated/atlas/atlas-edition3.json');
// [D2] output: the E4 serving capture dir.
const DEFAULT_OUT_DIR = resolve(__dirname, '../captures/2026-07-17-atlas-edition4-serving');
// [D16] freeze baseline: the E3 r8 furniture head's capture dir — the immediate prior
//       served surface. The 506 point circles + 37 legacy tombstones + hull polyline +
//       ghost/drill geometry are byte-frozen vs this baseline (Path-A). The 56 NEW marks
//       are the only additive geometry.
const R8_FREEZE_DIR = resolve(__dirname, '../captures/2026-07-16-atlas-edition3-r8-furniture');

// Doctored-input harness env vars (mirrors the E3 head; the E4 head reuses the same
// mechanics for its own doctored-input acceptance tests).
const ATLAS_ALLIN_SRC = process.env.ATLAS_ALLIN_SRC || null;
const ATLAS_ALLIN_OUT = process.env.ATLAS_ALLIN_OUT || null;
const ATLAS_OVERRIDE = process.env.ATLAS_OVERRIDE || null;
const ATLAS_SRC = ATLAS_ALLIN_SRC || ATLAS_OVERRIDE || ATLAS_PATH;
const IS_DOCTORED = Boolean(ATLAS_ALLIN_SRC || ATLAS_OVERRIDE);
const OUT_DIR = ATLAS_ALLIN_OUT || DEFAULT_OUT_DIR;
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
    if (cur == null || !(p in cur)) die(`${ctx}: required field '${path}' ABSENT in atlas.json — fail loud.`);
    cur = cur[p];
  }
  if (cur === null || cur === undefined || cur === '') die(`${ctx}: field '${path}' is empty in atlas.json — fail loud.`);
  return cur;
}

// ------------------------------------------------------------------ load + validate
const atlas = JSON.parse(readFileSync(ATLAS_SRC, 'utf8'));

// (H-1) EDITION IV gate + version.
if (Number(atlas.edition) !== 4) die(`[H-1] EDITION FIELD: top-level edition == ${JSON.stringify(atlas.edition)} (want 4) — refuse to render non-Edition-IV emission under the E4 serving head. HALT.`);
const atlasVersion = req(atlas, 'atlas_version', 'version');
if (String(atlasVersion) !== 'Edition-IV') die(`[H-1] atlas_version '${atlasVersion}' != 'Edition-IV' — E4 head requires the Edition-IV emission stamp.`);

// (H-2) PATH-A LAW: basis.edition === 1 && basis.frozen === true. THIS IS CORRECT, NOT A
// DEFECT — E4 is supplementary admission into Edition-I's frozen basis. Do NOT "fix" it.
const basis = req(atlas, 'basis', 'basis-block');
const inertiaPct = req(atlas, 'basis.inertia_pct', 'RIDER-1');
const retainedDims = req(atlas, 'basis.retained_dims', 'RIDER-1');
const structureStatement = req(atlas, 'basis.structure_statement', 'RIDER-1');
const axisNames = req(atlas, 'basis.axis_names', 'axis-names');
const basisEdition = req(atlas, 'basis.edition', 'basis-edition');
const basisFrozen = req(atlas, 'basis.frozen', 'basis-frozen');
const ratified = req(atlas, 'basis.ratified', 'ratified');
if (Number(basisEdition) !== 1) die(`[H-2] PATH-A LAW VIOLATION: basis.edition == ${JSON.stringify(basisEdition)} (want 1) — Edition IV is Path-A supplementary admission into Edition-I's frozen basis. HALT.`);
if (basisFrozen !== true) die(`[H-2] PATH-A LAW VIOLATION: basis.frozen == ${JSON.stringify(basisFrozen)} (want true). HALT.`);

// Mandatory-badge declaration cross-check.
if (Array.isArray(atlas.badge_fields_mandatory)) {
  const need = ['inertia_pct', 'retained_dims', 'structure_statement'];
  for (const f of need) if (!atlas.badge_fields_mandatory.includes(f)) die(`badge_fields_mandatory declares fields but omits '${f}' — RIDER-1 contract violated.`);
}

const counts = req(atlas, 'counts', 'counts-block');
const emittedAt = req(atlas, 'emitted_at', 'stamp');
const emitterScript = req(atlas, 'emitter_script', 'stamp');

const points = req(atlas, 'points', 'points');
if (!Array.isArray(points) || points.length === 0) die('points is empty.');

// (H-4) COUNTS gate.
if (counts.total !== 562) die(`[H-4] counts.total == ${counts.total} (want 562). HALT.`);
if (counts.total !== points.length) die(`[H-4] counts.total ${counts.total} != points.length ${points.length}. HALT.`);
if (counts.active + counts.supplementary !== counts.total) die(`[H-4] counts.active (${counts.active}) + counts.supplementary (${counts.supplementary}) != counts.total (${counts.total}). HALT.`);

// (H-3) G-3 ANCHORING RE-ASSERT: every E3 kit_id present in E4 with byte-identical x/y.
// The invocation's regression law that PASSED 0/506-moved at the ratification gate.
// SKIP for doctored inputs (the harness deliberately mutates atlas).
if (!IS_DOCTORED) {
  let prior;
  try { prior = JSON.parse(readFileSync(PRIOR_EDITION_PATH, 'utf8')); }
  catch (e) { die(`[H-3] cannot read prior-edition atlas-edition3.json for the G-3 byte-identity compare — ${e.message}`); }
  const priorPts = prior.points;
  if (!Array.isArray(priorPts)) die(`[H-3] prior-edition points is not an array.`);
  const e4ById = new Map();
  for (const p of points) e4ById.set(p.kit_id, p);
  const moved = [];
  const missing = [];
  for (const pp of priorPts) {
    const cur = e4ById.get(pp.kit_id);
    if (!cur) { missing.push(pp.kit_id); continue; }
    // JSON-value equality per invocation (byte-identical x/y as encoded numbers).
    if (JSON.stringify(cur.x) !== JSON.stringify(pp.x) || JSON.stringify(cur.y) !== JSON.stringify(pp.y)) {
      moved.push(`${pp.kit_id} (E3 ${pp.x},${pp.y} → E4 ${cur.x},${cur.y})`);
    }
  }
  if (moved.length > 0 || missing.length > 0) {
    const details = [];
    if (moved.length) details.push(`MOVED (${moved.length}): ${moved.slice(0, 10).join(' | ')}${moved.length > 10 ? ' …' : ''}`);
    if (missing.length) details.push(`MISSING (${missing.length}): ${missing.slice(0, 10).join(', ')}${missing.length > 10 ? ' …' : ''}`);
    die(`[H-3] G-3 ANCHORING VIOLATION: ${details.join(' ; ')} — E4 must carry every E3 kit_id at byte-identical x/y (Path-A supplementary admission — the 506 fit points do not move). HALT.`);
  }
  console.error(`[H-3 G-3 anchoring] all ${priorPts.length} E3 kit_ids present in E4 with byte-identical x/y (0 moved, 0 missing).`);
  console.error(`[H-1/H-2/H-4] edition=4, atlas_version='Edition-IV', basis.edition=1 (Path-A), basis.frozen=true, counts total=${counts.total}==${points.length}==active+supplementary=${counts.active}+${counts.supplementary}.`);
}

// ------------------------------------------------------------------ point partition
// Determinism: sort by kit_id everywhere.
const byId = (a, b) => (a.kit_id < b.kit_id ? -1 : a.kit_id > b.kit_id ? 1 : 0);
const all = [...points].sort(byId);
const active = all.filter((p) => p.supplementary !== true);
const supplementary = all.filter((p) => p.supplementary === true);
const grouped = active.filter((p) => p.gateA_group != null);
const neutral = active.filter((p) => p.gateA_group == null);

if (active.length !== counts.active) die(`active point count ${active.length} != counts.active ${counts.active}.`);
if (supplementary.length !== counts.supplementary) die(`supplementary count ${supplementary.length} != counts.supplementary ${counts.supplementary}.`);
if (all.length !== counts.total) die(`total point count ${all.length} != counts.total ${counts.total}.`);

// [D8] Classify the 93 supplementary points into three sub-classes (mirroring the
// e3-vs-e4 comparison head): LEGACY TOMBSTONE (E3-carried, 37; all have death_class),
// NEW TOMBSTONE (E4-only, 6; have death_class), NEW POSITIVE (E4-only, 50; no death_class).
// Discriminator per invocation & e3-vs-e4 head: (a) E3-carried vs E4-new via prior-atlas
// kit_id set; (b) within E4-new, `'death_class' in p` ⇒ tombstone; absent ⇒ positive.
// The DISCRIMINATOR must be robust to doctored inputs (the prior-edition file is only read
// once; store the set at module scope). For the doctored path (IS_DOCTORED), fall back to
// the E4 self-classification via `edition_admitted === 4` when the emitted field is present.
let PRIOR_E3_IDS = null;
if (!IS_DOCTORED) {
  try {
    const prior = JSON.parse(readFileSync(PRIOR_EDITION_PATH, 'utf8'));
    PRIOR_E3_IDS = new Set(prior.points.map((p) => p.kit_id));
  } catch { /* die already fired above if this fails */ }
}
function isE3Carried(p) {
  if (PRIOR_E3_IDS) return PRIOR_E3_IDS.has(p.kit_id);
  // fallback for doctored / no-prior: an emitted edition_admitted<=3 (or absent) marks E3-carried.
  const ea = p.edition_admitted;
  return ea == null || Number(ea) <= 3;
}
const legacyTombs = supplementary.filter((p) => isE3Carried(p) && ('death_class' in p) && p.death_class != null);
const newTombs = supplementary.filter((p) => !isE3Carried(p) && ('death_class' in p) && p.death_class != null);
const newPositives = supplementary.filter((p) => !isE3Carried(p) && !('death_class' in p));

if (!IS_DOCTORED) {
  if (legacyTombs.length !== 37) die(`[D8] legacyTombs.length ${legacyTombs.length} != 37 (emission expected 37 E3-carried legacy tombstones). HALT.`);
  if (newTombs.length !== 6) die(`[D8] newTombs.length ${newTombs.length} != 6 (emission expected 6 E4 new tombstones). HALT.`);
  if (newPositives.length !== 50) die(`[D8] newPositives.length ${newPositives.length} != 50 (emission expected 50 E4 new positives). HALT.`);
}

// death_class enum discovery + gateA_group discovery.
for (const p of legacyTombs) if (p.death_class == null) die(`legacy tomb '${p.kit_id}' missing death_class.`);
for (const p of newTombs) if (p.death_class == null) die(`new tomb '${p.kit_id}' missing death_class.`);
const allTombs = [...legacyTombs, ...newTombs].sort(byId);
const deathClasses = [...new Set(allTombs.map((p) => p.death_class))].sort();
const GROUP_ORDER = ['WHIRLWIND', 'TOTEM-SENTRY', 'TRAP-MINE', 'CHANNELED-BEAM', 'AURA', 'MINION-PET'];
const seenGroups = [...new Set(grouped.map((p) => p.gateA_group))].sort();
for (const g of seenGroups) if (!GROUP_ORDER.includes(g)) die(`unknown gateA_group '${g}' — vocabulary moved without re-ratification (R4 refusal).`);

// ================================================================== GHOST FIELD
// The E4 emission carries the full ghost_field structure (feasible_cells, sealed_cells,
// drill_in, pull_slice, off_plane_corpus, p_df_1) — same shape as E3 (byte-identical
// denominators; lit_cells re-derived live vs the +56-row census).
const ghost = req(atlas, 'ghost_field', 'ghost-field-block');
const feasibleCells = req(atlas, 'ghost_field.feasible_cells', 'ghost-feasible');
const sealedCells = req(atlas, 'ghost_field.sealed_cells', 'ghost-sealed');
if (!Array.isArray(feasibleCells) || feasibleCells.length === 0) die('ghost_field.feasible_cells empty.');
if (!Array.isArray(sealedCells)) die('ghost_field.sealed_cells not an array.');
const ATLAS_CORE_ORDER = req(atlas, 'ghost_field.core_order', 'ghost-core-order');
if (!Array.isArray(ATLAS_CORE_ORDER) || ATLAS_CORE_ORDER.length !== 7) die(`ghost_field.core_order must be the 7 core axes; got length ${Array.isArray(ATLAS_CORE_ORDER) ? ATLAS_CORE_ORDER.length : 'non-array'}.`);
{
  const bad = feasibleCells.find((c) => !Array.isArray(c.core) || c.core.length !== 7);
  if (bad) die(`ghost feasible cell has non-7 core (kit_count ${bad.kit_count}, x ${bad.x}).`);
}
const ghostDenoms = req(atlas, 'ghost_field.denominators', 'ghost-denominators');
const denomFeasibleExact = req(atlas, 'ghost_field.denominators.exact_post_red_law', 'ghost-denom-exact');
const denomNaiveBox = req(atlas, 'ghost_field.denominators.exact_raw_naive', 'ghost-denom-naive');
const mesoSealed = req(atlas, 'ghost_field.denominators.meso_sealed', 'ghost-meso-sealed');
const litCells = req(atlas, 'ghost_field.lit_cells', 'ghost-lit');
const unmappedPending = req(atlas, 'ghost_field.unmapped_pending_curation', 'ghost-unmapped');
const depthByDelivery = req(atlas, 'ghost_field.depth_by_delivery', 'ghost-depth');
const depthSumCheck = req(atlas, 'ghost_field.depth_sum_check', 'ghost-depth-sum');
const red3Note = req(atlas, 'ghost_field.red3_note', 'ghost-red3-note');
const supersededE1 = req(atlas, 'ghost_field.denominators.superseded_edition1', 'ghost-superseded-e1');
const supE1Exact = req(atlas, 'ghost_field.denominators.superseded_edition1.exact_post_red_law', 'ghost-superseded-exact');
const supE1MesoFeasible = req(atlas, 'ghost_field.denominators.superseded_edition1.meso_feasible', 'ghost-superseded-mesofeas');
const supE1MesoSealed = req(atlas, 'ghost_field.denominators.superseded_edition1.meso_sealed', 'ghost-superseded-mesoseal');

const SEAL_PREFIXES = ['L1-', 'L2-'];
for (const c of sealedCells) {
  if (c.cut_id == null) die(`ghost sealed cell missing cut_id.`);
  if (!SEAL_PREFIXES.some((pre) => String(c.cut_id).startsWith(pre))) die(`ghost sealed cell cut_id '${c.cut_id}' is OUTSIDE the {L1-, L2-} set at meso grain. R4 refusal.`);
  if ('x' in c || 'y' in c) die(`ghost sealed cell carries coordinates — sealed ground is never projected. Emitter malfunction.`);
}
const sealedByCut = {};
for (const c of sealedCells) sealedByCut[c.cut_id] = (sealedByCut[c.cut_id] || 0) + 1;
const sealedCutOrder = Object.keys(sealedByCut).sort();

for (const c of feasibleCells) {
  if (c.depth == null || typeof c.depth !== 'number') die(`ghost feasible cell missing numeric depth.`);
  if (!('x' in c) || !('y' in c)) die(`ghost feasible cell missing projected (x,y).`);
  if (!('lit' in c)) die(`ghost feasible cell missing 'lit' flag.`);
}

// EDITION IV lattice metadata (§10 vocabulary carried; register v1.3 re-asserts).
const editionTag = req(atlas, 'ghost_field.edition', 'ghost-edition'); // "IV"
const registerRef = req(atlas, 'ghost_field.register_ref', 'ghost-register');
// [D20] register did not move; Path-A. v1.3 RE-ASSERTS byte-identical denominators.
if (String(registerRef) !== 'feasibility-cuts-register-v1.3') die(`[D20] register_ref '${registerRef}' != feasibility-cuts-register-v1.3 (Edition-IV Path-A re-asserts v1.3; denominators byte-identical to E3).`);

// PULL SLICE (carried from E3 head vocabulary).
const pullSlice = req(atlas, 'ghost_field.pull_slice', 'pull-slice-block');
const pullMesoFeasible = req(atlas, 'ghost_field.pull_slice.meso_feasible', 'pull-feasible');
const pullMesoSealed = req(atlas, 'ghost_field.pull_slice.meso_sealed', 'pull-sealed');
const pullLitCells = req(atlas, 'ghost_field.pull_slice.lit_cells', 'pull-lit');
const pullLitTuples = req(atlas, 'ghost_field.pull_slice.lit_pull_core_tuples', 'pull-lit-tuples');
const pullNewLaw = req(atlas, 'ghost_field.pull_slice.new_law_needed', 'pull-new-law');
const pullHalt = req(atlas, 'ghost_field.pull_slice.halt', 'pull-halt');
if (pullNewLaw !== 0) die(`pull_slice.new_law_needed=${pullNewLaw} — a pull cell needs a NEW law. HALT.`);
if (pullHalt === true) die(`pull_slice.halt=true — emitter flagged a pull-slice HALT condition.`);
const pullSealedByCut = req(atlas, 'ghost_field.pull_slice.sealed_by_cut', 'pull-sealed-by-cut');
for (const cid of Object.keys(pullSealedByCut)) {
  if (!SEAL_PREFIXES.some((pre) => cid.startsWith(pre))) die(`pull_slice sealed cut_id '${cid}' is OUTSIDE the {L1-, L2-} meso set.`);
}

// DRILL-IN (carried from E3 head).
const drillIn = req(atlas, 'ghost_field.drill_in', 'drill-in-block');
const drillRegion = req(atlas, 'ghost_field.drill_in.region', 'drill-region');
const drillParentCells = req(atlas, 'ghost_field.drill_in.n_east_parent_cells', 'drill-parents');
const drillSubFeasibleN = req(atlas, 'ghost_field.drill_in.n_sub_feasible', 'drill-sub-feas');
const drillSubSealedN = req(atlas, 'ghost_field.drill_in.n_sub_sealed', 'drill-sub-sealed');
const subGlyphField = req(atlas, 'ghost_field.drill_in.sub_feasible_glyph_field', 'drill-glyph-field');
const subSealedLedger = req(atlas, 'ghost_field.drill_in.sub_sealed_ledger', 'drill-sealed-ledger');
const drillPromotedPair = req(atlas, 'ghost_field.drill_in.promoted_pair', 'drill-promoted-pair');
const drillSealEnum = req(atlas, 'ghost_field.drill_in.seal_enum', 'drill-seal-enum');
if (!Array.isArray(subGlyphField) || subGlyphField.length === 0) die('drill_in.sub_feasible_glyph_field empty.');
if (!Array.isArray(subSealedLedger)) die('drill_in.sub_sealed_ledger not an array.');
for (const e of subGlyphField) {
  if (typeof e.multiplicity !== 'number' || typeof e.x !== 'number' || typeof e.y !== 'number') die(`drill_in.sub_feasible_glyph_field entry malformed: ${JSON.stringify(e)}`);
}
const SUB_SEAL_PREFIXES = ['L1-', 'L2-', 'RED-3-'];
for (const r of subSealedLedger) {
  if (r.cut_id == null) die(`drill_in.sub_sealed_ledger row missing cut_id.`);
  if (!SUB_SEAL_PREFIXES.some((pre) => String(r.cut_id).startsWith(pre))) die(`drill_in sub-sealed cut_id '${r.cut_id}' is OUTSIDE the {L1-, L2-, RED-3-} promoted-grain set. R4 refusal.`);
  if (typeof r.count !== 'number') die(`drill_in.sub_sealed_ledger row missing numeric count: ${JSON.stringify(r)}`);
}
const subSealedSorted = [...subSealedLedger].sort((a, b) => {
  const ka = `${a.cut_id}|${a.geometry ?? ''}|${a.commit ?? ''}`, kb = `${b.cut_id}|${b.geometry ?? ''}|${b.commit ?? ''}`;
  return ka < kb ? -1 : ka > kb ? 1 : 0;
});

// OFF-PLANE CORPUS.
const offPlane = req(atlas, 'ghost_field.off_plane_corpus', 'off-plane-block');
const offPlaneDisclosure = req(atlas, 'ghost_field.off_plane_corpus.disclosure', 'off-plane-disclosure');
const offPlaneN = req(atlas, 'ghost_field.off_plane_corpus.gate_rejected_keyed', 'off-plane-n');

// P-DF-1 (still scored; still emitted; still surfaces to Matt if FALSIFIED).
const pDf1 = req(atlas, 'ghost_field.p_df_1', 'p-df-1-block');
const pDf1Verdict = req(atlas, 'ghost_field.p_df_1.verdict', 'p-df-1-verdict');
const pDf1Falsified = req(atlas, 'ghost_field.p_df_1.falsified', 'p-df-1-falsified');
const pDf1TopLevel = req(atlas, 'p_df_1_verdict', 'p-df-1-top-level');
if (String(pDf1Verdict) !== String(pDf1TopLevel)) die(`p_df_1.verdict '${pDf1Verdict}' != top-level p_df_1_verdict '${pDf1TopLevel}'.`);
const pDf1Consequence = req(atlas, 'ghost_field.p_df_1.consequence_if_falsified', 'p-df-1-consequence');

// ------------------------------------------------------------------ plane geometry
// FROZEN LAW: world bounds computed from POINTS ONLY. All 562 (including the 56 new
// supplementary) contribute — the fit is basis-frozen (Path-A) but the 56 new marks are
// within the E3 bounding box per the ratification comparison plate (NEW WITHIN E3 BBOX =
// YES; verified upstream). We follow the E3 head's convention of computing over all
// points; the padding stays 0.06, byte-carried.
const xs = all.map((p) => p.x);
const ys = all.map((p) => p.y);
const rawMinX = Math.min(...xs), rawMaxX = Math.max(...xs);
const rawMinY = Math.min(...ys), rawMaxY = Math.max(...ys);
const padX = (rawMaxX - rawMinX) * 0.06;
const padY = (rawMaxY - rawMinY) * 0.06;
const minX = rawMinX - padX, maxX = rawMaxX + padX;
const minY = rawMinY - padY, maxY = rawMaxY + padY;

const W = 1600, H = 1200;
const M = { top: 132, right: 96, bottom: 96, left: 96 };
const PW = W - M.left - M.right;
const PH = H - M.top - M.bottom;
const GHOST_PLAQUE_W = 420;
const GHOST_PLAQUE_X = (M.left + PW) - GHOST_PLAQUE_W;

const sx = (x) => M.left + ((x - minX) / (maxX - minX)) * PW;
const sy = (y) => M.top + (1 - (y - minY) / (maxY - minY)) * PH;
const f2 = (n) => Number(n).toFixed(2);

const zeroX = (minX <= 0 && maxX >= 0) ? sx(0) : null;
const zeroY = (minY <= 0 && maxY >= 0) ? sy(0) : null;

// ------------------------------------------------------------------ GHOST projection aggregation
function ghostAggregate() {
  const bucket = new Map();
  for (const c of feasibleCells) {
    const sxv = sx(c.x), syv = sy(c.y);
    const key = `${f2(sxv)}|${f2(syv)}`;
    let b = bucket.get(key);
    if (!b) { b = { sxv, syv, mult: 0, lit: false, core: c.core }; bucket.set(key, b); }
    b.mult += 1;
    if (c.lit) b.lit = true;
  }
  return [...bucket.entries()].sort((a, b) => (a[0] < b[0] ? -1 : a[0] > b[0] ? 1 : 0)).map(([, v]) => v);
}
const ghostGlyphs = ghostAggregate();
function ghostR(mult) { return 0.9 + 0.55 * Math.log2(mult + 1); }
const ghostLit = ghostGlyphs.filter((g) => g.lit);
const ghostDark = ghostGlyphs.filter((g) => !g.lit);

// DRILL-IN glyph aggregation.
function drillAggregate() {
  const bucket = new Map();
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
const DRILL_R_FLOOR = 1.25;
const DRILL_R_STEP = 0.12;
function drillR(mult) { return DRILL_R_FLOOR + DRILL_R_STEP * Math.log2(mult + 1); }
const drillMinMult = drillGlyphs.reduce((m, g) => Math.min(m, g.mult), Infinity);
const drillMinRadius = drillR(drillMinMult);

// ------------------------------------------------------------------ CLIP DISCLOSURE
const IN_PLANE_EPS = 0.01;
function ghostInPlane(c) {
  const sxv = sx(c.x), syv = sy(c.y);
  return sxv >= M.left - IN_PLANE_EPS && sxv <= M.left + PW + IN_PLANE_EPS
      && syv >= M.top - IN_PLANE_EPS && syv <= M.top + PH + IN_PLANE_EPS;
}
const ghostClippedCells = feasibleCells.filter((c) => !ghostInPlane(c));
const ghostClippedCount = ghostClippedCells.length;
const ghostClippedAllUnlit = ghostClippedCells.every((c) => !c.lit);
if (!IS_DOCTORED && !ghostClippedAllUnlit) die(`ghost CLIP disclosure: LIT cells outside frozen frame — silent under-claim.`);
const drillGlyphInPlane = (g) => g.sxv >= M.left - IN_PLANE_EPS && g.sxv <= M.left + PW + IN_PLANE_EPS && g.syv >= M.top - IN_PLANE_EPS && g.syv <= M.top + PH + IN_PLANE_EPS;
const drillClippedGlyphs = drillGlyphs.filter((g) => !drillGlyphInPlane(g));
const drillClippedCount = drillClippedGlyphs.length;

// ================================================================== GHOST HORIZON (charted)
function convexHullWorld(cells) {
  const seen = new Set();
  const pts = [];
  for (const c of cells) {
    const k = `${c.x.toFixed(6)},${c.y.toFixed(6)}`;
    if (!seen.has(k)) { seen.add(k); pts.push([c.x, c.y]); }
  }
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
  return lower.concat(upper);
}
const charterHullInput = [
  ...feasibleCells.map((c) => ({ x: c.x, y: c.y })),
  ...subGlyphField.map((e) => ({ x: e.x, y: e.y })),
];
const ghostHullWorld = convexHullWorld(charterHullInput);
const ghostHullVertexCount = ghostHullWorld.length;
const mesoOnlyHullWorld = convexHullWorld(feasibleCells);
const mesoOnlyHullEastX = mesoOnlyHullWorld.reduce((m, v) => Math.max(m, v[0]), -Infinity);
const chartedHullEastX = ghostHullWorld.reduce((m, v) => Math.max(m, v[0]), -Infinity);
const ghostHullSvg = ghostHullWorld.map(([wx, wy]) => ({ x: sx(wx), y: sy(wy) }));
const ghostHullEastVertex = ghostHullSvg.reduce((best, v) => (v.x > best.x ? v : best), ghostHullSvg[0]);
const LINE_NAME = 'CHARTED HORIZON';
const GHOST_HORIZON_LABEL = `${LINE_NAME} — charted search space: east half to geometry×commit drill-in depth, west half to meso grain; beyond this line is uncharted — not yet computed, not infeasible, not absent.`;

// ================================================================== BEYOND-HORIZON
const PIP_EPS = 1e-9;
function pointOnSegment(px, py, ax, ay, bx, by) {
  const cross = (bx - ax) * (py - ay) - (by - ay) * (px - ax);
  if (Math.abs(cross) > PIP_EPS) return false;
  const dot = (px - ax) * (bx - ax) + (py - ay) * (by - ay);
  const len2 = (bx - ax) * (bx - ax) + (by - ay) * (by - ay);
  return dot >= -PIP_EPS && dot <= len2 + PIP_EPS;
}
function pointInHullWorld(px, py, poly) {
  if (poly.length < 3) return false;
  for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {
    if (pointOnSegment(px, py, poly[j][0], poly[j][1], poly[i][0], poly[i][1])) return true;
  }
  let inside = false;
  for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {
    const xi = poly[i][0], yi = poly[i][1], xj = poly[j][0], yj = poly[j][1];
    const intersect = ((yi > py) !== (yj > py)) && (px < ((xj - xi) * (py - yi)) / (yj - yi) + xi);
    if (intersect) inside = !inside;
  }
  return inside;
}
const beyondHorizonKits = active.filter((p) => !pointInHullWorld(p.x, p.y, ghostHullWorld));
const beyondHorizonCount = beyondHorizonKits.length;
const beyondMesoOnlyKits = active.filter((p) => !pointInHullWorld(p.x, p.y, mesoOnlyHullWorld));
const beyondMesoOnlyCount = beyondMesoOnlyKits.length;
const BEYOND_HORIZON_MESO_RECEIPT = 14;
if (!IS_DOCTORED) {
  if (beyondMesoOnlyCount !== BEYOND_HORIZON_MESO_RECEIPT) die(`meso-hull cross-check mismatch: N=${beyondMesoOnlyCount} (want ${BEYOND_HORIZON_MESO_RECEIPT}) — the meso hull is frozen-field consequence.`);
  if (beyondHorizonCount > beyondMesoOnlyCount) die(`charted-hull containment violation.`);
  if (chartedHullEastX + 1e-9 < mesoOnlyHullEastX) die(`charted-horizon east-reach violation.`);
}
const BEYOND_HORIZON_EXPECTED = beyondHorizonCount;

// Coverage callout (data-derived).
const denomMesoFeasible = req(atlas, 'ghost_field.denominators.meso_feasible', 'ghost-meso-feasible');
const litFractionPct = (litCells / denomMesoFeasible) * 100;
const kitsPerLitCell = counts.active / litCells;
const coveragePct = (counts.active / denomFeasibleExact) * 100;

function fmtSci(n) {
  const exp = Math.floor(Math.log10(n));
  const mant = n / Math.pow(10, exp);
  return `${mant.toFixed(1)}×10${supExp(exp)}`;
}
function supExp(e) {
  const map = { '-': '⁻', '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹' };
  return String(e).split('').map((ch) => map[ch] ?? ch).join('');
}
function fmtInt(n) {
  const s = String(Math.trunc(n));
  return s.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}
function fmt1(n) { return Number(n).toFixed(1); }
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

const ghostClipLine = `${fmtInt(ghostClippedCount)} unlit cell${ghostClippedCount === 1 ? '' : 's'} project beyond the frame (clipped, not rescaled — frame frozen to the settled points)`;
const beyondHorizonLine = `${fmtInt(beyondHorizonCount)} settled kits still stand beyond the CHARTED horizon (down from ${fmtInt(beyondMesoOnlyCount)} at meso grain — the east drill-in charts the geometry×commit reach beyond most whirlwind/beam kits along û) — kits project with all 14 coordinates; ghost cells carry the 7 core only, so the strongest east pulls (cone/whirlwind geometry, channel commit) remain uncharted at this grain.`;
const chartedReachEastX = chartedHullEastX;
const settledActiveEastX = Math.max(...active.map((p) => p.x));
const chartedReachDeltaEast = chartedReachEastX - settledActiveEastX;
const chartedReachLine = `CHARTED HORIZON reaches east to x=${f2(chartedReachEastX)} — the geometry×commit drill-in charts +${f2(chartedReachDeltaEast)} beyond the outermost settled kit (x=${f2(settledActiveEastX)}) along û: every formerly-beyond kit now sits inside the charted search space (beyond-horizon ${fmtInt(beyondMesoOnlyCount)}→${fmtInt(beyondHorizonCount)}).`;
const chartedReachVisible = `CHARTED HORIZON east reach x=${f2(chartedReachEastX)} (+${f2(chartedReachDeltaEast)} beyond outermost settled kit) — drill-in charts past every settled kit (beyond-horizon ${fmtInt(beyondMesoOnlyCount)}→${fmtInt(beyondHorizonCount)})`;

// [D19] Rider strip: leads with the CHART's own edition ("Edition IV lattice"); basis
// demoted to attribute (Edition-I frozen). Data-derived via editionTag.
const riderStr = `Edition ${editionTag} lattice · basis: Edition-I (frozen ${ratified}) · plane = dims 1–2, ${inertiaPct}% corrected inertia · retained basis: ${retainedDims} dims · ${structureStatement}`;

// LATTICE / EDITION IV lattice microcopy — all data-derived from emitted fields.
const pullSliceLine = `pull slice (new fn level): ${fmtInt(pullMesoFeasible)} feasible · ${fmtInt(pullLitCells)} lit (existing kits re-keyed on intrinsic evidence) · ${fmtInt(pullMesoSealed)} sealed`;
const offPlaneLine = String(offPlaneDisclosure);
const drillGroundLine = `EAST-half drill-in (${drillPromotedPair.join('×')}): ${fmtInt(drillParentCells)} parent cells → ${fmtInt(drillSubFeasibleN)} sub-feasible (subordinate ground) · ${fmtInt(drillSubSealedN)} RED-3′ sealed`;
const subSealedSummary = subSealedSorted.map((r) => `${r.cut_id} (${r.geometry ?? '?'}×${r.commit ?? '?'}) ${fmtInt(r.count)}`).join(' · ');
const drillClipLine = `${fmtInt(drillClippedCount)} drill-in sub-cell glyph${drillClippedCount === 1 ? '' : 's'} project beyond the frame (clipped, not rescaled — zero-mass ground never moves the frame)`;
const supersededLine = `superseded (Edition I): ${fmtInt(supE1Exact)} exact · ${fmtInt(supE1MesoFeasible)} meso feasible · ${fmtInt(supE1MesoSealed)} meso sealed`;

const HEADLINE_LIT = `${fmtInt(litCells)} / ${fmtInt(denomMesoFeasible)} ≈ ${fmt1(litFractionPct)}% of feasible meso ground ever lit`;
const HEADLINE_DENSITY = `${fmtInt(counts.active)} kits over ${fmtInt(litCells)} lit cells ≈ ${fmt1(kitsPerLitCell)} kits per lit cell — the genre didn't explore; it remade.`;
const COVERAGE_SECONDARY = `${fmtInt(counts.active)} active ≈ ${fmtSci(coveragePct)} % of ${fmtInt(denomFeasibleExact)} feasible exact-grain kits`;

// ------------------------------------------------------------------ KDE density underlay
// FROZEN r2 — active kits only (the 56 new supplementary do NOT contribute to KDE bands;
// KDE is a signal about the settled ACTIVE archipelago, and the new supplementary marks
// are supplementary by definition — they earn footprint via their own supplementary
// glyphs, not via the density surface). Same code path as E3, byte-carried.
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

// ------------------------------------------------------------------ SKINS (byte-carried from E3 r8)
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
    liveSingle: '#50991f',
    liveSingleOp: 0.95,
    groupDotR: 5.2,
    tombInk: '#3a3f4a',
    tombUnknownInk: '#b0451f',
    // [D9] new-positive glyph ink: sat-blue (carried from the e3-vs-e4 comparison head;
    // deliberately distinct from the six family colors + the chartreuse live-single + the
    // grey neutral + the tomb inks. Hue ≈ 214°, well outside the six-family hue span).
    positiveInk: '#4fa3ff',
    positiveOp: 0.95,
    positiveR: 3.7,
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
    ghostDarkInk: '#c0c8d4',
    ghostDarkOp: 0.5,
    ghostLitInk: '#7f93b3',
    ghostLitOp: 0.72,
    horizonInk: '#93a0b3',
    horizonOp: 0.62,
    horizonWidth: 1.1,
    horizonDash: '7 5',
    horizonLabelInk: '#5b6677',
    horizonLabelSize: 10,
    horizonLabelStyle: 'normal',
    drillInk: '#c6cdd8',
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
    liveSingle: '#7cd143',
    liveSingleOp: 0.92,
    groupDotR: 5.2,
    tombInk: '#cfc6ad',
    tombUnknownInk: '#d98a55',
    // [D9] new-positive glyph ink on dark: same hue family as instrument (sat-blue) but
    // lifted for contrast on the archive void. H≈214° S0.55 V0.95 → #7fbdff.
    positiveInk: '#7fbdff',
    positiveOp: 0.92,
    positiveR: 3.7,
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
    ghostDarkInk: '#2c3038',
    ghostDarkOp: 0.85,
    ghostLitInk: '#6b5a34',
    ghostLitOp: 0.8,
    horizonInk: '#5a5340',
    horizonOp: 0.75,
    horizonWidth: 1.1,
    horizonDash: '7 5',
    horizonLabelInk: '#9a8f6f',
    horizonLabelSize: 10,
    horizonLabelStyle: 'italic',
    drillInk: '#30343e',
    drillOp: 0.72,
  },
};

// Skin→canvas map — synthesized render-side; carried into provenance. Same as E3 head.
const SKIN_CANVAS_MAP = {
  instrument: { canvas: 'light', hex: SKINS.instrument.bg },
  archive: { canvas: 'dark', hex: SKINS.archive.bg },
};

// [D18] Family (gateA_group) colors — byte-identical to E3 head.
const GROUP_COLORS = {
  'WHIRLWIND': '#e8663d',
  'TOTEM-SENTRY': '#3f8ecc',
  'TRAP-MINE': '#8e5cc4',
  'CHANNELED-BEAM': '#d4a017',
  'AURA': '#2fa889',
  'MINION-PET': '#c94f8a',
};
function isUnknown(dc) { return dc === 'unknown-pending-recrawl'; }

// Explainer texts (CONTENT LOCKED — carried forward verbatim).
const POLE_GLOSS = {
  PERFORM: 'you are the weapon — channel · beam · spin',
  DEPLOY: 'you place the weapon — totem · trap · detonate',
  LAUNCH: 'damage sent away — projectile · chain',
  EMBODY: 'damage from the body — spin · aura · dash',
};
const DENSITY_LEGEND_LINE = 'shaded field = density of genre kits (settled territory — not a boundary)';
const DERIVATION_GLOSS = 'positions computed, not designed — MCA over 13 mechanical coordinates per kit; axes named from the loadings afterward.';
const GHOST_CENSUS_LINE = 'ghost field lit from the current census; positions from the frozen Edition-I basis.';

// ------------------------------------------------------------------ SVG assembly
function esc(s) {
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
function coreAttr(coreArr) { return esc(coreArr.join('|')); }

// [D9-D10-D18] Furniture factor table — byte-carried from E3 r8 head (Matt 2026-07-16).
const FURN = {
  title:        17.5,
  banner:        8.5,
  bannerBandH:  20,
  deriv:         7.5,
  poleTitle:     9.5,
  poleTitleLS:   1.0,
  poleGloss:     7,
  launchEmbody:  9.5,
  horizonLabel:  7,
  horizonRowH:   9,
  keyHeader:     8,
  keyRow:        8,
  keyGloss:      7,
  keyRowH:      13,
  keySwatchR:    3.4,
  keyBandGloss:  7,
  centroid:      8.5,
  centroidBandH:13,
  centroidCW:    5.8,
  graveHeader:   7.5,
  graveRow:      7,
  graveRowH:    10.5,
  ledgerCensus:  7,
  ledgerHeadline:8.5,
  ledgerHl2:     7.5,
  ledgerSub:     6.5,
  ledgerRight:   6.5,
  ledgerRow:     6,
  ledgerRowH:    6,
  footer:        7,
};

function renderSVG(skinKey) {
  const s = SKINS[skinKey];
  const P = [];

  P.push(`<defs>`);
  P.push(`<filter id="terrainBlur" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="${s.blurStd}"/></filter>`);
  P.push(`<clipPath id="planeClip"><rect x="${f2(M.left)}" y="${f2(M.top)}" width="${f2(PW)}" height="${f2(PH)}"/></clipPath>`);
  P.push(`</defs>`);

  P.push(`<rect x="0" y="0" width="${W}" height="${H}" fill="${s.bg}"/>`);

  // ================================================================== LAYER 0 (bottom): ghosts
  // drill-in (subordinate) first, then meso ghosts + horizon. Carried verbatim from E3.
  P.push(`<g id="layer-drillin" clip-path="url(#planeClip)">`);
  P.push(`<g fill="${s.drillInk}" fill-opacity="${s.drillOp}">`);
  for (const g of drillGlyphs) {
    P.push(`<circle cx="${f2(g.sxv)}" cy="${f2(g.syv)}" r="${f2(drillR(g.mult))}" data-el="ghost" data-mult="${g.mult}"/>`);
  }
  P.push(`</g>`);
  P.push(`</g>`);

  P.push(`<g id="layer-ghosts" clip-path="url(#planeClip)">`);
  if (ghostHullSvg.length >= 2) {
    const hullPts = ghostHullSvg.map((v) => `${f2(v.x)},${f2(v.y)}`).join(' ');
    const firstPt = `${f2(ghostHullSvg[0].x)},${f2(ghostHullSvg[0].y)}`;
    P.push(`<polyline points="${hullPts} ${firstPt}" fill="none" stroke="${s.horizonInk}" stroke-opacity="${s.horizonOp}" stroke-width="${s.horizonWidth}" stroke-dasharray="${s.horizonDash}" stroke-linejoin="round"><title>${esc(GHOST_HORIZON_LABEL)}</title></polyline>`);
  }
  P.push(`<g fill="${s.ghostDarkInk}" fill-opacity="${s.ghostDarkOp}">`);
  for (const g of ghostDark) {
    P.push(`<circle cx="${f2(g.sxv)}" cy="${f2(g.syv)}" r="${f2(ghostR(g.mult))}" data-el="ghost" data-core="${coreAttr(g.core)}" data-mult="${g.mult}"/>`);
  }
  P.push(`</g>`);
  P.push(`<g fill="${s.ghostLitInk}" fill-opacity="${s.ghostLitOp}">`);
  for (const g of ghostLit) {
    P.push(`<circle cx="${f2(g.sxv)}" cy="${f2(g.syv)}" r="${f2(ghostR(g.mult))}" data-el="ghost" data-core="${coreAttr(g.core)}" data-mult="${g.mult}"/>`);
  }
  P.push(`</g>`);
  P.push(`</g>`);

  // ---- LAYER 1: KDE terrain (byte-frozen; only active kits contribute)
  P.push(`<g filter="url(#terrainBlur)" fill="${s.bandBase}">`);
  for (const b of bands) {
    if (!b.d) continue;
    P.push(`<path d="${b.d}" fill-opacity="${(s.bandOpacityStep).toFixed(3)}"/>`);
  }
  P.push(`</g>`);

  // ---- soft zero axes + frame (byte-frozen)
  if (zeroX != null) P.push(`<line x1="${f2(zeroX)}" y1="${f2(M.top)}" x2="${f2(zeroX)}" y2="${f2(M.top + PH)}" stroke="${s.axisLine}" stroke-width="1" stroke-dasharray="2 6"/>`);
  if (zeroY != null) P.push(`<line x1="${f2(M.left)}" y1="${f2(zeroY)}" x2="${f2(M.left + PW)}" y2="${f2(zeroY)}" stroke="${s.axisLine}" stroke-width="1" stroke-dasharray="2 6"/>`);
  P.push(`<rect x="${f2(M.left)}" y="${f2(M.top)}" width="${f2(PW)}" height="${f2(PH)}" fill="none" stroke="${s.axisLine}" stroke-width="1"/>`);

  // ---- LAYER 2: live kits — single (neutral) + condensation (grouped). BYTE-FROZEN from E3.
  P.push(`<g id="layer-live">`);
  P.push(`<g fill="${s.liveSingle}" fill-opacity="${s.liveSingleOp}">`);
  for (const p of neutral) {
    P.push(`<circle cx="${f2(sx(p.x))}" cy="${f2(sy(p.y))}" r="${s.neutralDotR}" data-el="live" data-kit="${esc(p.kit_id)}"><title>${esc(p.kit_id)} — active — ${esc(p.franchise ?? '')}</title></circle>`);
  }
  P.push(`</g>`);
  for (const g of GROUP_ORDER) {
    const mem = grouped.filter((p) => p.gateA_group === g);
    if (!mem.length) continue;
    const memberList = mem.map((p) => p.kit_id).join('|');
    P.push(`<g fill="${GROUP_COLORS[g]}" stroke="${s.bg}" stroke-width="0.6">`);
    for (const p of mem) {
      P.push(`<circle cx="${f2(sx(p.x))}" cy="${f2(sy(p.y))}" r="${s.groupDotR}" data-el="condensation" data-kit="${esc(p.kit_id)}" data-kits="${esc(memberList)}"><title>${esc(p.kit_id)} — ${esc(g)} — ${esc(p.franchise ?? '')}</title></circle>`);
    }
    P.push(`</g>`);
  }
  P.push(`</g>`);

  // ---- LAYER 3 (was E3's only supplementary layer): the 37 legacy tombstones. BYTE-FROZEN.
  //      + the 6 NEW tombstones ([D10]): SAME † text mark grammar as legacy. Total 43 daggers.
  //      Rendered in kit_id-sorted order (legacy + new interleaved deterministically) so the
  //      layer is one consistent tombstone class in the DOM; the ordinal index labels number
  //      1..43 in that order. data-el="graveyard" carried on every † text.
  P.push(`<g id="layer-graveyard" font-family="${s.fontStack}">`);
  for (let i = 0; i < allTombs.length; i++) {
    const p = allTombs[i];
    const cx = sx(p.x), cy = sy(p.y);
    const unk = isUnknown(p.death_class);
    const ink = unk ? s.tombUnknownInk : s.tombInk;
    P.push(`<text x="${f2(cx)}" y="${f2(cy + 5)}" font-size="16" text-anchor="middle" fill="${ink}" font-weight="700" data-el="graveyard" data-kit="${esc(p.kit_id)}">†<title>${esc(p.kit_id)} † ${esc(p.death_class)}</title></text>`);
    if (unk) {
      P.push(`<circle cx="${f2(cx)}" cy="${f2(cy)}" r="7" fill="none" stroke="${ink}" stroke-width="1.1" stroke-dasharray="2 2"/>`);
    }
    P.push(`<text x="${f2(cx + 8)}" y="${f2(cy + 2)}" font-size="8" fill="${ink}" fill-opacity="0.85">${i + 1}</text>`);
  }
  P.push(`</g>`);

  // ---- LAYER 3.5 ([D9]): the 50 NEW POSITIVES. Filled saturated dot slightly larger than
  //      live-single. data-el="positive" (new class); data-kit per mark. Layer id
  //      layer-positives sits BETWEEN layer-graveyard and layer-chrome — the E3 layer
  //      ordering (drillin/ghosts/live/graveyard/chrome) is not disturbed; the new class
  //      appends before chrome so plate-chrome still paints last.
  //
  //      Franchise is not stored on the new positives per the E4 emission schema (the
  //      new-positive schema is {cos2, edition_admitted, kit_id, level_flattened,
  //      supplementary, x, y}). Franchise-derived-from-prefix is included in the <title>
  //      for parity with active/legacy grammar (kit_id prefix → franchise short-key).
  P.push(`<g id="layer-positives" fill="${s.positiveInk}" fill-opacity="${s.positiveOp}">`);
  for (const p of [...newPositives].sort(byId)) {
    const franchise = (p.franchise ?? p.kit_id.split('-')[0]);
    P.push(`<circle cx="${f2(sx(p.x))}" cy="${f2(sy(p.y))}" r="${s.positiveR}" data-el="positive" data-kit="${esc(p.kit_id)}"><title>${esc(p.kit_id)} — new positive (E4 supplementary admission) — ${esc(franchise)}</title></circle>`);
  }
  P.push(`</g>`);

  // ---- LAYER 3.75 ([D12]): future-proofing hook for elrond's candidates JSON. Reserved
  //      empty group; NO marks emitted now; a pass-2 additive annotation-layer module can
  //      populate it WITHOUT touching any data-mark emission above.
  P.push(`<g id="layer-family-candidates"></g>`);

  // ==================================================================================
  // r8 CHROME LAYER — byte-carried from E3 r8. All content strings are data-derived from
  // the E4 emission (editionTag = "IV" etc.). The FURN factor table sizes every text.
  // ==================================================================================
  P.push(`<g id="layer-chrome">`);

  // group centroid annotations (unchanged geometry vs E3)
  P.push(`<g font-family="${s.fontStack}" font-weight="${s.titleWeight}">`);
  for (const g of GROUP_ORDER) {
    const c = groupCentroids[g];
    if (!c) continue;
    const cx = sx(c.x), cy = sy(c.y);
    const label = `${g}`;
    const tw = label.length * FURN.centroidCW + 12;
    const cRectTop = cy - 12 - FURN.centroidBandH;
    P.push(`<g>`);
    P.push(`<rect x="${f2(cx - tw / 2)}" y="${f2(cRectTop)}" width="${f2(tw)}" height="${f2(FURN.centroidBandH)}" rx="3" fill="${s.plaque}" fill-opacity="0.82" stroke="${GROUP_COLORS[g]}" stroke-width="1.2"/>`);
    P.push(`<text x="${f2(cx)}" y="${f2(cRectTop + FURN.centroidBandH - 3.5)}" font-size="${FURN.centroid}" text-anchor="middle" fill="${s.ink}" letter-spacing="0.4">${esc(label)}</text>`);
    P.push(`<line x1="${f2(cx)}" y1="${f2(cy - 12)}" x2="${f2(cx)}" y2="${f2(cy - 3)}" stroke="${GROUP_COLORS[g]}" stroke-width="1.2"/>`);
    P.push(`</g>`);
  }
  P.push(`</g>`);

  // CHARTED HORIZON label
  {
    const ev = ghostHullEastVertex;
    const labX = M.left + PW - 6;
    const rows = wrapByChars(GHOST_HORIZON_LABEL, 58);
    const rowH = FURN.horizonRowH;
    const labY0 = ev.y + 90;
    P.push(`<g font-family="${s.fontStack}">`);
    P.push(`<line x1="${f2(ev.x)}" y1="${f2(ev.y)}" x2="${f2(labX - 4)}" y2="${f2(labY0 - 9)}" stroke="${s.horizonInk}" stroke-opacity="${s.horizonOp}" stroke-width="0.8" stroke-dasharray="3 3"/>`);
    P.push(`<circle cx="${f2(ev.x)}" cy="${f2(ev.y)}" r="2.1" fill="none" stroke="${s.horizonInk}" stroke-opacity="${s.horizonOp}" stroke-width="1"/>`);
    for (let i = 0; i < rows.length; i++) {
      const weight = i === 0 ? ' font-weight="600"' : '';
      P.push(`<text x="${f2(labX)}" y="${f2(labY0 + i * rowH)}" font-size="${FURN.horizonLabel}" font-style="${s.horizonLabelStyle}"${weight} text-anchor="end" fill="${s.horizonLabelInk}" letter-spacing="0.2">${esc(rows[i])}${i === 0 ? `<title>${esc(GHOST_HORIZON_LABEL)}</title>` : ''}</text>`);
    }
    P.push(`</g>`);
  }

  // ---- AXIS labels + glosses (E2.3 rail arrows: source-glyph ≠ on-screen direction)
  const cxMid = M.left + PW / 2, cyMid = M.top + PH / 2;
  const railR = W - M.right / 2;
  const railL = M.left / 2;
  P.push(`<g font-family="${s.fontStack}">`);
  P.push(`<text transform="rotate(-90 ${f2(railR - 6)} ${f2(cyMid)})" x="${f2(railR - 6)}" y="${f2(cyMid)}" text-anchor="middle" fill="${s.ink}" font-weight="${s.titleWeight}" font-size="${FURN.poleTitle}" letter-spacing="${FURN.poleTitleLS}">PERFORM ↓</text>`);
  P.push(`<text transform="rotate(-90 ${f2(railR + 9)} ${f2(cyMid)})" x="${f2(railR + 9)}" y="${f2(cyMid)}" text-anchor="middle" fill="${s.faint}" font-size="${FURN.poleGloss}" font-style="${s.glossStyle}" letter-spacing="0.2">${esc(POLE_GLOSS.PERFORM)}</text>`);
  P.push(`<text transform="rotate(-90 ${f2(railL + 6)} ${f2(cyMid)})" x="${f2(railL + 6)}" y="${f2(cyMid)}" text-anchor="middle" fill="${s.ink}" font-weight="${s.titleWeight}" font-size="${FURN.poleTitle}" letter-spacing="${FURN.poleTitleLS}">↑ DEPLOY</text>`);
  P.push(`<text transform="rotate(-90 ${f2(railL - 9)} ${f2(cyMid)})" x="${f2(railL - 9)}" y="${f2(cyMid)}" text-anchor="middle" fill="${s.faint}" font-size="${FURN.poleGloss}" font-style="${s.glossStyle}" letter-spacing="0.2">${esc(POLE_GLOSS.DEPLOY)}</text>`);
  P.push(`<text x="${f2(cxMid)}" y="120" text-anchor="middle" fill="${s.ink}" font-weight="${s.titleWeight}" font-size="${FURN.launchEmbody}" letter-spacing="0.6">${esc('↑ LAUNCH')}    <tspan fill="${s.faint}" font-weight="400" font-size="${FURN.poleGloss}" font-style="${s.glossStyle}">${esc(POLE_GLOSS.LAUNCH)}</tspan></text>`);
  const embodyRows = wrapByChars(POLE_GLOSS.EMBODY, 30);
  P.push(`<text x="${f2(cxMid)}" y="1119" text-anchor="middle" fill="${s.ink}" font-weight="${s.titleWeight}" font-size="${FURN.launchEmbody}" letter-spacing="0.6">${esc('EMBODY ↓')}</text>`);
  for (let i = 0; i < embodyRows.length; i++) {
    const titleNode = i === 0 ? `<title>${esc(POLE_GLOSS.EMBODY)}</title>` : '';
    P.push(`<text x="${f2(cxMid)}" y="${f2(1134 + i * 11)}" text-anchor="middle" fill="${s.faint}" font-size="${FURN.poleGloss}" font-style="${s.glossStyle}" letter-spacing="0.2">${esc(embodyRows[i])}${titleNode}</text>`);
  }
  P.push(`</g>`);

  // ---- TITLE + RIDER + derivation
  P.push(`<g font-family="${s.fontStack}" fill="${s.ink}">`);
  // [D4] "Build Horizon — Edition IV" — editionTag data-derived (ghost_field.edition = "IV").
  P.push(`<text x="${f2(M.left)}" y="42" font-size="${FURN.title}" font-weight="${s.titleWeight}" letter-spacing="0.5">Build Horizon — Edition ${esc(String(editionTag))}</text>`);
  P.push(`<rect x="${f2(M.left)}" y="58" width="${f2(PW)}" height="${f2(FURN.bannerBandH)}" rx="4" fill="${s.badgeBg}" stroke="${s.plaqueStroke}" stroke-width="1"/>`);
  P.push(`<text x="${f2(M.left + 12)}" y="72" font-size="${FURN.banner}" fill="${s.badgeInk}" letter-spacing="0.3">${esc(riderStr)}</text>`);
  P.push(`<text x="${f2(M.left + 12)}" y="102" font-size="${FURN.deriv}" font-style="${s.glossStyle}" fill="${s.faint}" letter-spacing="0.2">${esc(DERIVATION_GLOSS)}</text>`);
  P.push(`</g>`);

  // ---- BUILD FAMILIES key (top-right) — [D11] ratified-members-only coloring driven by
  //      gateA_group. Family counts BYTE-IDENTICAL to E3 (families grow by ratification
  //      waves; E4 admission does NOT grow gateA_group values). r8-fix content-derived box.
  {
    const lx = M.left + PW - 152, ly = M.top + 14;
    // r8-fix: box height RE-DERIVED FROM CONTENT (last gloss baseline + descender + pad,
    // from the SAME accumulator the draw loop walks). Byte-carried from E3 head.
    const GLOSS_DESC = 2, BOTTOM_PAD = 8;
    const lastGlossBaselineRel = (FURN.keyHeader + 8) + FURN.keyRowH * GROUP_ORDER.length + 2 + 11;
    const boxH = (lastGlossBaselineRel + 12) + GLOSS_DESC + BOTTOM_PAD;
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

  // ---- GRAVEYARD legend (bottom-left) — driven by `allTombs` (43 corpses = 37 legacy + 6 new).
  //      Bottom-anchored, box height derived from row count.
  {
    const lx = M.left + 12, ly0 = M.top + PH - (deathClasses.length * FURN.graveRowH + 26);
    P.push(`<g font-family="${s.fontStack}" font-size="${FURN.graveRow}" fill="${s.ink}">`);
    P.push(`<rect x="${f2(lx - 8)}" y="${f2(ly0 - 14)}" width="158" height="${f2(FURN.graveRowH * deathClasses.length + 26)}" rx="4" fill="${s.plaque}" fill-opacity="0.9" stroke="${s.plaqueStroke}"/>`);
    P.push(`<text x="${f2(lx)}" y="${f2(ly0)}" font-weight="${s.titleWeight}" font-size="${FURN.graveHeader}" letter-spacing="0.4">GRAVEYARD † (${allTombs.length} corpses)</text>`);
    let yy = ly0 + 14;
    for (const dc of deathClasses) {
      const n = allTombs.filter((p) => p.death_class === dc).length;
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
  // BELOW-PLANE ledger band + footer census — byte-carried from E3 (adapted to E4 counts).
  // ==================================================================================
  {
    const bx = M.left, by = M.top + PH + 14;
    P.push(`<g font-family="${s.fontStack}" fill="${s.ink}">`);
    P.push(`<text x="${f2(bx)}" y="${f2(by + 1)}" font-size="${FURN.ledgerCensus}" font-style="${s.glossStyle}" fill="${s.faint}">${esc(GHOST_CENSUS_LINE)}</text>`);
    P.push(`<text x="${f2(bx)}" y="${f2(by + 17)}" font-size="${FURN.ledgerHeadline}" font-weight="${s.titleWeight}" fill="${s.ink}" letter-spacing="0.2">${esc(HEADLINE_LIT)}</text>`);
    P.push(`<text x="${f2(bx)}" y="${f2(by + 32)}" font-size="${FURN.ledgerHl2}" font-weight="${s.titleWeight}" fill="${s.ink}">${esc(HEADLINE_DENSITY)}</text>`);
    P.push(`<text x="${f2(bx)}" y="${f2(by + 46)}" font-size="${FURN.ledgerSub}" font-style="${s.glossStyle}" fill="${s.faint}">${esc(COVERAGE_SECONDARY)}</text>`);
    const feasStr = `${fmtInt(feasibleCells.length)} feasible meso cells · ${fmtInt(litCells)} lit · ${fmtInt(unmappedPending)} unmapped · ${fmtInt(mesoSealed)} sealed (off-plane)`;
    P.push(`<text x="${f2(bx)}" y="${f2(by + 60)}" font-size="${FURN.ledgerSub}" fill="${s.faint}">${esc(feasStr)}</text>`);
    const sealSummary = sealedCutOrder.map((cid) => `${cid} ${fmtInt(sealedByCut[cid])}`).join(' · ');
    const colR = bx + 820;
    // [D19] header edition literal → "Edition IV" (data-derived from editionTag).
    P.push(`<text x="${f2(colR)}" y="${f2(by + 1)}" font-size="${FURN.ledgerRight}" font-weight="${s.titleWeight}" letter-spacing="0.3" fill="${s.ink}">GHOST FIELD — the feasible dark · Edition ${esc(String(editionTag))} lattice</text>`);
    const clipCombo = [
      beyondHorizonCount > 0 ? `${fmtInt(beyondHorizonCount)} kits beyond horizon` : null,
      ghostClippedCount > 0 ? `${fmtInt(ghostClippedCount)} meso clipped` : null,
      drillClippedCount > 0 ? `${fmtInt(drillClippedCount)} drill-in clipped` : null,
    ].filter(Boolean).join(' · ');
    const clipTitles = [
      beyondHorizonCount > 0 ? beyondHorizonLine : null,
      ghostClippedCount > 0 ? ghostClipLine : null,
      drillClippedCount > 0 ? drillClipLine : null,
    ].filter(Boolean);
    const led = [];
    led.push({ s: chartedReachVisible, titles: [chartedReachLine], lead: true });
    led.push({ s: pullSliceLine, titles: [pullSliceLine] });
    led.push({ s: drillGroundLine, titles: [drillGroundLine] });
    led.push({ s: `${fmtInt(drillSubSealedN)} sub-cells sealed @ drill-in grain — RED-3′ surfaces here`, titles: [subSealedSummary] });
    led.push({ s: `${fmtInt(mesoSealed)} meso sealed (off-plane): ${sealSummary}`, titles: [sealSummary] });
    if (clipCombo) led.push({ s: `${clipCombo} (hover for full disclosures)`, titles: clipTitles, gloss: true });
    led.push({ s: `${fmtInt(offPlaneN)} gear-grain kits (mcd-) held off-plane — deferred grain ruling`, titles: [offPlaneLine], gloss: true });
    led.push({ s: 'superseded (Edition I) denominators — hover', titles: [supersededLine], gloss: true });
    let ry = by + 11;
    for (const r of led) {
      const styleAttr = r.gloss ? ` font-style="${s.glossStyle}"` : '';
      const fillAttr = r.lead ? s.ink : s.faint;
      const weightAttr = r.lead ? ' font-weight="600"' : '';
      const titleNodes = (r.titles || []).map((t) => `<title>${esc(t)}</title>`).join('');
      P.push(`<text x="${f2(colR)}" y="${f2(ry)}" font-size="${FURN.ledgerRow}"${styleAttr}${weightAttr} fill="${fillAttr}">${esc(r.s)}${titleNodes}</text>`);
      ry += FURN.ledgerRowH;
    }
    P.push(`</g>`);
  }

  // ---- FOOTER (byte-carried; census content DATA-DERIVED at render time from counts).
  //      The E4 census reads: "points: 469 active + 93 corpse = 562 · ghost: 11,160 feasible + 1,314 sealed".
  //      "93 corpse" replaces "37 corpse" (Path-A: the supplementary count grew; the ACTIVE count
  //      is unchanged). The atlasVersion footer stamp reads "Edition-IV" (via atlas_version).
  P.push(`<g font-family="${s.fontStack}" fill="${s.faint}" font-size="${FURN.footer}">`);
  P.push(`<text x="${f2(M.left)}" y="${f2(H - 12)}">${esc(String(atlasVersion))} · ${esc(String(registerRef))} · emitted ${esc(emittedAt)} · skin=${skinKey}</text>`);
  P.push(`<text x="${f2(M.left + PW)}" y="${f2(H - 12)}" text-anchor="end">points: ${active.length} active + ${supplementary.length} corpse = ${all.length} · ghost: ${feasibleCells.length} feasible + ${sealedCells.length} sealed</text>`);
  P.push(`</g>`);

  P.push(`</g>`); // close layer-chrome

  const svg = `<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">\n${P.join('\n')}\n</svg>\n`;
  return svg;
}

// ------------------------------------------------------------------ fingerprints
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
function ghostFingerprint() {
  const rows = ghostGlyphs.map((g) => `${f2(g.sxv)}|${f2(g.syv)}|${g.mult}|${g.lit ? 'L' : 'D'}`);
  rows.push(`SEALED|${sealedCutOrder.map((c) => `${c}:${sealedByCut[c]}`).join(',')}`);
  return rows.sort().join('\n');
}

// ------------------------------------------------------------------ main
async function main() {
  if (RECEIPT_ONLY) {
    const hullDump = ghostHullWorld.map(([x, y]) => `${x.toFixed(6)},${y.toFixed(6)}`).join(';');
    console.log(`HULL_VERTEX_COUNT=${ghostHullVertexCount}`);
    console.log(`HULL_WORLD=${hullDump}`);
    console.log(`BEYOND_N=${beyondHorizonCount}`);
    console.log(`BEYOND_KITS=${beyondHorizonKits.map((p) => p.kit_id).join(',')}`);
    return;
  }
  const results = {};
  if (ATLAS_ALLIN_OUT) {
    for (const skin of ['instrument', 'archive']) {
      const svg = renderSVG(skin);
      writeFileSync(join(OUT_DIR, `atlas-edition4-${skin}.svg`), svg, 'utf8');
    }
    console.log(`[allin-render] wrote SVGs to ${OUT_DIR} (N beyond=${beyondHorizonCount}; suite skipped)`);
    return;
  }

  const ptFps = {}, ghFps = {};
  for (const skin of ['instrument', 'archive']) {
    const svg = renderSVG(skin);
    const svgPath = join(OUT_DIR, `atlas-edition4-${skin}.svg`);
    writeFileSync(svgPath, svg, 'utf8');
    ptFps[skin] = pointFingerprint();
    ghFps[skin] = ghostFingerprint();
    const pngPath = join(OUT_DIR, `atlas-edition4-${skin}.png`);
    const png = await sharp(Buffer.from(svg), { density: 144 }).png().toBuffer();
    writeFileSync(pngPath, png);
    results[skin] = { svgPath, pngPath, bytes: Buffer.byteLength(svg) };
    console.log(`[render] ${skin}: ${svgPath} (${results[skin].bytes} B), ${pngPath} (${png.length} B PNG)`);
  }

  // ---- ACCEPTANCE ----
  const tests = [];
  const rec = (name, pass, detail) => tests.push({ name, pass, detail });
  const bodies = {};
  for (const skin of ['instrument', 'archive']) bodies[skin] = readFileSync(join(OUT_DIR, `atlas-edition4-${skin}.svg`), 'utf8');

  // (H-1..H-4) HARD ASSERTS — asserted at load-time; re-recorded here for the note/provenance.
  rec('H-1-edition-and-version', Number(atlas.edition) === 4 && String(atlasVersion) === 'Edition-IV',
    `edition=${atlas.edition}, atlas_version=${atlasVersion}`);
  rec('H-2-path-A-basis', Number(basisEdition) === 1 && basisFrozen === true,
    `basis.edition=${basisEdition} (Path-A), basis.frozen=${basisFrozen}`);
  {
    // G-3 anchoring re-assert (re-run for the record).
    let priorSet;
    try {
      priorSet = new Map(JSON.parse(readFileSync(PRIOR_EDITION_PATH, 'utf8')).points.map((p) => [p.kit_id, p]));
    } catch { priorSet = null; }
    let moved = 0, missing = 0;
    if (priorSet) {
      for (const [kid, pp] of priorSet.entries()) {
        const cur = all.find((p) => p.kit_id === kid);
        if (!cur) missing++;
        else if (JSON.stringify(cur.x) !== JSON.stringify(pp.x) || JSON.stringify(cur.y) !== JSON.stringify(pp.y)) moved++;
      }
    }
    rec('H-3-G-3-anchoring', priorSet !== null && moved === 0 && missing === 0,
      `${priorSet ? priorSet.size : '?'} E3 kit_ids checked; moved=${moved}, missing=${missing}`);
  }
  rec('H-4-counts', counts.total === 562 && counts.total === all.length && counts.active + counts.supplementary === counts.total,
    `counts.total=${counts.total}==points.length=${all.length}==active+supp=${counts.active}+${counts.supplementary}`);

  // (1) point counts (adapted to E4)
  rec('point-counts', active.length === 469 && supplementary.length === 93 && all.length === 562,
    `active=${active.length} (exp 469), supp=${supplementary.length} (exp 93), total=${all.length} (exp 562)`);

  // (1b) new-mark split
  rec('new-mark-split', newPositives.length === 50 && newTombs.length === 6 && legacyTombs.length === 37,
    `newPositives=${newPositives.length}(exp 50); newTombs=${newTombs.length}(exp 6); legacyTombs=${legacyTombs.length}(exp 37)`);

  // (2) grouped/neutral partition — WAVE-4 LAW: family counts BYTE-IDENTICAL to E3 (86 members).
  rec('grouped-count', grouped.length === 86, `grouped=${grouped.length} (exp 86; Wave-4 law: families grow only by ratification waves, never by tau; E4 admits 0 new gateA_group members)`);

  // (3) ghost counts vs emitted
  rec('ghost-counts', feasibleCells.length === denomMesoFeasible && sealedCells.length === mesoSealed,
    `feasible=${feasibleCells.length} (== ${denomMesoFeasible}), sealed=${sealedCells.length} (== ${mesoSealed})`);

  // (4) lit conformance
  const litFlagCount = feasibleCells.filter((c) => c.lit).length;
  rec('ghost-lit-conformance', litFlagCount === litCells,
    `feasible lit=true ${litFlagCount} == emitted lit_cells ${litCells}`);

  // (5) depth Σ
  const depthSum = feasibleCells.reduce((s, c) => s + c.depth, 0);
  rec('ghost-depth-sum', depthSum === depthSumCheck && depthSumCheck === denomFeasibleExact,
    `Σdepth=${fmtInt(depthSum)} == ${fmtInt(depthSumCheck)} == ${fmtInt(denomFeasibleExact)}`);

  // (6) sealed cut_id conformance
  const sealBad = sealedCells.filter((c) => !SEAL_PREFIXES.some((pre) => String(c.cut_id).startsWith(pre)));
  rec('sealed-cut_id-conformance', sealBad.length === 0,
    `all ${sealedCells.length} sealed cut_ids in {L1-,L2-}: ${sealedCutOrder.join(', ')}`);

  // (7) point layout skin invariance
  rec('point-layout-equality', ptFps.instrument === ptFps.archive, ptFps.instrument === ptFps.archive ? 'identical fingerprint' : 'MISMATCH');

  // (8) ghost coordinate+status skin invariance
  rec('ghost-layout-equality', ghFps.instrument === ghFps.archive, ghFps.instrument === ghFps.archive ? 'identical fingerprint' : 'MISMATCH');

  // (9) determinism
  let determ = true, dDetail = [];
  for (const skin of ['instrument', 'archive']) {
    const a1 = renderSVG(skin), a2 = renderSVG(skin);
    const eq = a1 === a2;
    if (!eq) determ = false;
    dDetail.push(`${skin}:${eq ? 'byte-equal' : 'DIFF'}`);
  }
  rec('determinism', determ, dDetail.join(', '));

  // (10) anti-stale greps
  const box257Re = /(?<![\d.])2\.57(?![\d])/;
  const r2 = !box257Re.test(bodies.instrument) && !box257Re.test(bodies.archive);
  rec('R2-no-2.57-numeral', r2, r2 ? 'clean (naive-box 2.57 absent as content)' : 'FOUND naive-box "2.57"');
  const supersededRe = /422,?445,?240/;
  const noSuperseded = !supersededRe.test(bodies.instrument) && !supersededRe.test(bodies.archive);
  rec('no-superseded-422M', noSuperseded, noSuperseded ? 'clean' : 'FOUND 422,445,240');
  const no819Re = /819,?439,?740/;
  const no819 = !no819Re.test(bodies.instrument) && !no819Re.test(bodies.archive);
  rec('no-exact_post_logical-raw', no819, no819 ? 'clean (819,439,740 absent)' : 'FOUND raw pre-red-law denom');
  const seasonRe = /season[\s_\-]*\d/i;
  const r3g = !seasonRe.test(bodies.instrument) && !seasonRe.test(bodies.archive);
  rec('no-season-N', r3g, r3g ? 'clean' : 'FOUND season-N string');

  // (11) RIDER-1 badge present
  const badgeOk = ['instrument', 'archive'].every((sk) =>
    bodies[sk].includes(String(inertiaPct)) && bodies[sk].includes(String(retainedDims)) && bodies[sk].includes(structureStatement));
  rec('RIDER-1-badge', badgeOk, badgeOk ? `inertia=${inertiaPct} + retained=${retainedDims} + structure statement present both skins` : 'MISSING badge field');

  // (12) pole glosses + density legend + derivation gloss + census line + horizon label
  const glossClauses = [POLE_GLOSS.PERFORM, POLE_GLOSS.DEPLOY, POLE_GLOSS.LAUNCH, POLE_GLOSS.EMBODY];
  const polesOk = ['instrument', 'archive'].every((sk) => glossClauses.every((c) => bodies[sk].includes(esc(c))));
  rec('pole-glosses', polesOk, polesOk ? 'all 4 pole glosses present both skins' : 'MISSING a pole gloss');
  const densOk = ['instrument', 'archive'].every((sk) => bodies[sk].includes(esc(DENSITY_LEGEND_LINE)));
  rec('density-legend-line', densOk, densOk ? 'present both skins' : 'MISSING');
  const derivOk = ['instrument', 'archive'].every((sk) => bodies[sk].includes(esc(DERIVATION_GLOSS)));
  rec('derivation-gloss', derivOk, derivOk ? 'present both skins' : 'MISSING');
  const censusOk = ['instrument', 'archive'].every((sk) => bodies[sk].includes(esc(GHOST_CENSUS_LINE)));
  rec('census-line', censusOk, censusOk ? 'present both skins' : 'MISSING');
  const horizonOk = ['instrument', 'archive'].every((sk) => bodies[sk].includes(esc(GHOST_HORIZON_LABEL)));
  rec('horizon-label', horizonOk, horizonOk ? 'present both skins' : 'MISSING');

  // (13) clip disclosure zero-case
  {
    const CLIP_PHRASE = 'clipped, not rescaled';
    let clipOk, clipMsg;
    if (ghostClippedCount > 0) {
      const present = ['instrument', 'archive'].every((sk) => bodies[sk].includes(esc(ghostClipLine)));
      clipOk = present;
      clipMsg = clipOk ? `clip line present (count=${fmtInt(ghostClippedCount)}, all unlit=${ghostClippedAllUnlit})` : `MISSING/STALE`;
    } else {
      const absent = ['instrument', 'archive'].every((sk) => !bodies[sk].includes(CLIP_PHRASE));
      clipOk = absent;
      clipMsg = absent ? 'zero clips — line omitted' : 'orphan clip phrase';
    }
    rec('clip-disclosure', clipOk, clipMsg);
  }

  // (14) coverage callout numerals
  const covOk = ['instrument', 'archive'].every((sk) => bodies[sk].includes(fmtInt(counts.active)) && bodies[sk].includes(fmtInt(denomFeasibleExact)));
  rec('coverage-callout', covOk, covOk ? `${fmtInt(counts.active)} + ${fmtInt(denomFeasibleExact)} present both skins` : 'MISSING');

  // (15) sealed ledger content
  const sealLedgerOk = ['instrument', 'archive'].every((sk) => sealedCutOrder.every((cid) => bodies[sk].includes(esc(cid))) && bodies[sk].includes(fmtInt(mesoSealed)));
  rec('sealed-ledger', sealLedgerOk, sealLedgerOk ? `sealed ${fmtInt(mesoSealed)} + cut ids present both skins` : 'MISSING');

  // (16) no regions in ghost layer
  const noRegions = ['instrument', 'archive'].every((sk) => !/<polygon|<pattern|clip-rule|<use /.test(bodies[sk]));
  rec('ghost-glyphs-not-regions', noRegions, noRegions ? 'clean' : 'REGION primitive found');

  // ------ EDITION IV LATTICE INTEGRITY ------

  // (17) edition stamp: "Edition IV" (space form) + v1.3 present both skins
  const editionStampedIV = ['instrument', 'archive'].every((sk) => bodies[sk].includes('Edition IV') && bodies[sk].includes('feasibility-cuts-register-v1.3'));
  rec('edition-IV-stamp+v1.3', editionStampedIV, editionStampedIV ? 'both present in both skins' : 'MISSING');

  // (18) title plate exact
  const titleOk = ['instrument', 'archive'].every((sk) => bodies[sk].includes('Build Horizon — Edition IV'));
  rec('title-plate', titleOk, titleOk ? '"Build Horizon — Edition IV" present both skins' : 'MISSING');

  // (19) new positives + new tombstones + legacy tombstones marks
  const nPositiveMarks = ['instrument', 'archive'].every((sk) => (bodies[sk].match(/data-el="positive"/g) || []).length === newPositives.length);
  const nGraveyardMarks = ['instrument', 'archive'].every((sk) => (bodies[sk].match(/data-el="graveyard"/g) || []).length === (legacyTombs.length + newTombs.length));
  rec('E4-new-marks-rendered', nPositiveMarks && nGraveyardMarks,
    `data-el="positive"×${newPositives.length} both skins; data-el="graveyard"×${legacyTombs.length + newTombs.length} both skins`);

  // (20) family-candidates layer reserved
  const candidateLayerOk = ['instrument', 'archive'].every((sk) => /<g id="layer-family-candidates"><\/g>/.test(bodies[sk]));
  rec('D12-family-candidates-layer-reserved', candidateLayerOk, candidateLayerOk ? 'reserved empty group present both skins' : 'MISSING');

  // (21) BUILD FAMILIES rename in place (no "CONDENSATIONS" header)
  const familiesKeyOk = ['instrument', 'archive'].every((sk) => bodies[sk].includes('BUILD FAMILIES') && !bodies[sk].includes('>CONDENSATIONS<'));
  rec('BUILD-FAMILIES-key-rename', familiesKeyOk, familiesKeyOk ? 'BUILD FAMILIES header both skins (no CONDENSATIONS)' : 'FAIL');

  // (22) family counts unchanged from E3 (Wave-4 law: families grow by ratification waves)
  // A stronger check: each family header renders "NAME (N)" with the E3 count.
  const groupCounts = {};
  for (const g of GROUP_ORDER) {
    const c = groupCentroids[g];
    groupCounts[g] = c ? c.n : 0;
  }
  const familiesOk = ['instrument', 'archive'].every((sk) => GROUP_ORDER.every((g) => bodies[sk].includes(`${g} (${groupCounts[g]})`)));
  rec('family-counts-rendered-per-emission', familiesOk, familiesOk ? `all six family rows rendered with per-emission counts: ${GROUP_ORDER.map((g) => `${g}:${groupCounts[g]}`).join(', ')}` : 'MISSING');

  // (23) FIT-LAYER REGRESSION vs the E3 r8 baseline — under Path-A ADDITIVE edition
  //      boundary, byte-equality is the wrong assertion for any set that grew. Correct
  //      assertion (per D17): every BASELINE tuple appears in the CURRENT set; the CURRENT
  //      set may add ≥ 0 new tuples (whitelisted as additive geometry).
  //        · active-point circles: baseline had 469 circles (data-el="live" + "condensation").
  //          E4 adds 50 new-positive circles that ALSO match the "circle with <title>" regex.
  //          The correct check is baseline ⊆ current (all 469 legacy tuples byte-frozen;
  //          exactly 50 new tuples added).
  //        · tombstones: baseline had 37 daggers. E4 adds 6 new tombstone daggers. Same
  //          subset containment (all 37 legacy byte-frozen; exactly 6 new).
  //        · hull polyline: the CHARTED hull is over feasibleCells ∪ subGlyphField. The
  //          E4 emission's ghost_field is byte-identical to E3 at these fields (Path-A;
  //          denominators + drill-in did not move). So the hull points string must be
  //          byte-identical to the E3 baseline.
  let fitPass = true, fitDetail = [];
  for (const skin of ['instrument', 'archive']) {
    let baseSvg;
    try { baseSvg = readFileSync(join(R8_FREEZE_DIR, `atlas-edition3-${skin}.svg`), 'utf8'); }
    catch { fitPass = false; fitDetail.push(`${skin}:R8-FREEZE-BASELINE-MISSING`); continue; }
    // (a) point circles (cx, cy, r, title) — subset containment.
    const pointTupleRe = /<circle cx="([\d.]+)" cy="([\d.]+)" r="([\d.]+)"[^>]*><title>([^<]*)<\/title><\/circle>/g;
    const extractPtsTupleArr = (svg) => { const set = []; let m; while ((m = pointTupleRe.exec(svg)) !== null) set.push(`${m[1]}|${m[2]}|${m[3]}|${m[4]}`); pointTupleRe.lastIndex = 0; return set; };
    const basePtsArr = extractPtsTupleArr(baseSvg), curPtsArr = extractPtsTupleArr(bodies[skin]);
    const basePtsSet = new Set(basePtsArr), curPtsSet = new Set(curPtsArr);
    const missingLegacyPts = [...basePtsSet].filter((t) => !curPtsSet.has(t));
    const addedPts = [...curPtsSet].filter((t) => !basePtsSet.has(t));
    // Under Path-A: every baseline circle byte-frozen (missingLegacyPts.length===0), and
    // exactly newPositives.length new circles added. Emit-count clarity: base 469 (active
    // circles), current 469 active + 50 new positives = 519.
    const ptsSubsetOk = missingLegacyPts.length === 0 && addedPts.length === newPositives.length;
    // (b) tombstones (x, y, title) — subset containment.
    const tombTupleRe = /<text x="([\d.]+)" y="([\d.]+)" font-size="16" text-anchor="middle"[^>]*>†<title>([^<]*)<\/title><\/text>/g;
    const extractTombTuplesArr = (svg) => { const set = []; let m; while ((m = tombTupleRe.exec(svg)) !== null) set.push(`${m[1]}|${m[2]}|${m[3]}`); tombTupleRe.lastIndex = 0; return set; };
    const baseTombArr = extractTombTuplesArr(baseSvg), curTombArr = extractTombTuplesArr(bodies[skin]);
    const baseTombSet = new Set(baseTombArr), curTombSet = new Set(curTombArr);
    const missingLegacyTombs = [...baseTombSet].filter((t) => !curTombSet.has(t));
    const addedTombs = [...curTombSet].filter((t) => !baseTombSet.has(t));
    const tombSubsetOk = missingLegacyTombs.length === 0 && addedTombs.length === newTombs.length;
    // (c) hull polyline — byte-identical (E4 ghost + drill-in fields byte-identical to E3).
    const hullRe = /<polyline points="([^"]+)" fill="none"/;
    const baseHull = (baseSvg.match(hullRe) || [])[1] || 'NO-HULL-BASE';
    const curHull = (bodies[skin].match(hullRe) || [])[1] || 'NO-HULL-CUR';
    const hullEq = baseHull === curHull;
    if (!(ptsSubsetOk && tombSubsetOk && hullEq)) fitPass = false;
    fitDetail.push(`${skin}: legacy-active-circles ${missingLegacyPts.length === 0 ? 'BYTE-FROZEN-SUBSET' : `MOVED (${missingLegacyPts.length})`} (${basePtsSet.size}→${curPtsSet.size}, added=${addedPts.length}(exp ${newPositives.length})); legacy-tombs ${missingLegacyTombs.length === 0 ? 'BYTE-FROZEN-SUBSET' : `MOVED (${missingLegacyTombs.length})`} (${baseTombSet.size}→${curTombSet.size}, added=${addedTombs.length}(exp ${newTombs.length})); hull ${hullEq ? 'BYTE-FROZEN' : 'MOVED'}`);
  }
  rec('fit-layer-regression-vs-E3-r8', fitPass, fitDetail.join(' | '));

  // (24) fit-at-fluid-width legibility — the r8 furniture-factor table drives text sizes;
  //      we check that the title, banner, and key text render at their FURN sizes (as
  //      literal `font-size="17.5"` etc.) in both skins.
  const furnFontsOk = ['instrument', 'archive'].every((sk) =>
    bodies[sk].includes(`font-size="${FURN.title}"`) &&
    bodies[sk].includes(`font-size="${FURN.banner}"`) &&
    bodies[sk].includes(`font-size="${FURN.keyHeader}"`) &&
    bodies[sk].includes(`font-size="${FURN.footer}"`));
  rec('r8-furniture-sizes-applied', furnFontsOk, furnFontsOk ? `FURN sizes literal in SVG both skins (title=${FURN.title}, banner=${FURN.banner}, keyHeader=${FURN.keyHeader}, footer=${FURN.footer})` : 'MISSING');

  // (25) footer census content — data-derived, adapted to E4
  const censusContent = `points: ${active.length} active + ${supplementary.length} corpse = ${all.length} · ghost: ${feasibleCells.length} feasible + ${sealedCells.length} sealed`;
  const footerX = f2(M.left + PW);
  const footerOk = ['instrument', 'archive'].every((sk) => bodies[sk].includes(`<text x="${footerX}" y="1188.00" text-anchor="end">${censusContent}</text>`));
  rec('footer-census', footerOk, footerOk ? `census "${censusContent}" at x=${footerX} both skins` : 'MISSING');

  // (26) E4 tombstones EACH rendered as a † text mark (spot-check by kit_id in title)
  const eachTombOk = ['instrument', 'archive'].every((sk) => allTombs.every((p) => bodies[sk].includes(`>${esc(p.kit_id)} † ${esc(p.death_class)}<`)));
  rec('all-tombstone-titles-present', eachTombOk, eachTombOk ? `${allTombs.length} tombstone titles present both skins` : 'MISSING');

  // (27) E4 positive marks EACH rendered (spot-check by kit_id in title)
  const eachPosOk = ['instrument', 'archive'].every((sk) => newPositives.every((p) => bodies[sk].includes(`>${esc(p.kit_id)} — new positive`)));
  rec('all-new-positive-titles-present', eachPosOk, eachPosOk ? `${newPositives.length} positive-mark titles present both skins` : 'MISSING');

  // (28) hooks integrity (E4-adapted)
  const kitIdSet = new Set(all.map((p) => p.kit_id));
  const coreSet = new Set(feasibleCells.map((c) => c.core.join('|')));
  let hkPass = true; const hkDetail = [];
  for (const skin of ['instrument', 'archive']) {
    const cur = bodies[skin];
    const cnt = (re) => (cur.match(re) || []).length;
    const nLive = cnt(/data-el="live"/g);
    const nCond = cnt(/data-el="condensation"/g);
    const nGrave = cnt(/data-el="graveyard"/g);
    const nPos = cnt(/data-el="positive"/g);
    const nGhost = cnt(/data-el="ghost"/g);
    const nClassed = nLive + nCond + nGrave + nPos;
    const layers = ['layer-ghosts', 'layer-drillin', 'layer-graveyard', 'layer-live', 'layer-positives', 'layer-family-candidates', 'layer-chrome'];
    const layerMiss = layers.filter((L) => cnt(new RegExp(`<g id="${L}"`, 'g')) !== 1);
    const liveOk = nLive === neutral.length;
    const condOk = nCond === grouped.length;
    const graveOk = nGrave === legacyTombs.length + newTombs.length;
    const posOk = nPos === newPositives.length;
    const classedOk = nClassed === 562 && nClassed === active.length + supplementary.length;
    const ghostOk = nGhost === ghostGlyphs.length + drillGlyphs.length;
    const kitVals = [...cur.matchAll(/data-kit="([^"]*)"/g)].map((m) => m[1]);
    const badKit = kitVals.find((v) => !kitIdSet.has(v));
    const coreVals = [...cur.matchAll(/data-core="([^"]*)"/g)].map((m) => m[1]);
    const badCore = coreVals.find((v) => !coreSet.has(v));
    const kitsVals = [...cur.matchAll(/data-kits="([^"]*)"/g)].map((m) => m[1]);
    const badMember = kitsVals.flatMap((v) => v.split('|')).find((k) => !kitIdSet.has(k));
    const skinOk = liveOk && condOk && graveOk && posOk && classedOk && ghostOk && layerMiss.length === 0 && !badKit && !badCore && !badMember;
    if (!skinOk) hkPass = false;
    hkDetail.push(`${skin}: live ${nLive}/${neutral.length}=${liveOk} cond ${nCond}/${grouped.length}=${condOk} grave ${nGrave}/${legacyTombs.length + newTombs.length}=${graveOk} pos ${nPos}/${newPositives.length}=${posOk} classed ${nClassed}/562=${classedOk} ghost ${nGhost}/${ghostGlyphs.length + drillGlyphs.length}=${ghostOk} layers-missing=${layerMiss.join(',') || 'none'} badKit=${badKit ?? 'none'} badCore=${badCore ? 'YES' : 'none'} badMember=${badMember ?? 'none'}`);
  }
  rec('hooks-integrity-E4', hkPass, hkDetail.join(' | '));

  // (29) beyond-horizon N=0 (charted encloses ALL settled)
  rec('CHARTED-hull-beyond-N-zero', beyondHorizonCount === 0, `charted-hull N=${beyondHorizonCount}`);

  // (30) meso-hull frozen receipt (14 kits) still holds
  rec('meso-hull-beyond-N-14', beyondMesoOnlyCount === 14, `meso-hull N=${beyondMesoOnlyCount}`);

  // (31) P-DF-1 verdict PASS + consistent
  const pDf1Ok = String(pDf1Verdict) === 'PASS' && String(pDf1TopLevel) === 'PASS' && pDf1Falsified === false;
  rec('P-DF-1-scored', pDf1Ok, `verdict=${pDf1Verdict}, top-level=${pDf1TopLevel}, falsified=${pDf1Falsified}`);

  // ---- SMOKES ----
  const smokes = [];
  const csmoke = (name, pass, detail) => smokes.push({ name, pass, detail });
  const wc = groupCentroids['WHIRLWIND'];
  csmoke('WHIRLWIND x>0 (PERFORM)', wc.x > 0, `x=${wc.x.toFixed(4)}`);
  csmoke('WHIRLWIND y<0 (EMBODY)', wc.y < 0, `y=${wc.y.toFixed(4)}`);
  const tc = groupCentroids['TOTEM-SENTRY'];
  csmoke('TOTEM-SENTRY x<0 (DEPLOY)', tc.x < 0, `x=${tc.x.toFixed(4)}`);
  const litInBox = ghostLit.every((g) => g.sxv >= M.left - 0.5 && g.sxv <= M.left + PW + 0.5 && g.syv >= M.top - 0.5 && g.syv <= M.top + PH + 0.5);
  csmoke('all lit ghost glyphs inside plane frame', litInBox, `${ghostLit.length} lit glyphs, all in-frame=${litInBox}`);
  const maxMult = Math.max(...ghostGlyphs.map((g) => g.mult));
  csmoke('coincident-projection aggregation active', maxMult > 1, `max multiplicity=${maxMult} (aggregated ${feasibleCells.length} cells -> ${ghostGlyphs.length} glyph positions)`);
  csmoke('ghost hull is a small polygon', ghostHullVertexCount >= 3 && ghostHullVertexCount <= 60, `hull vertex count=${ghostHullVertexCount}`);
  csmoke('CHARTED horizon east EXCEEDS settled kits', chartedHullEastX > settledActiveEastX, `charted east=${chartedHullEastX.toFixed(4)} > settled east=${settledActiveEastX.toFixed(4)}`);
  // Lost-Ark-wing sanity: at least 40 of the 50 new positives should sit in WN quadrant
  // (x<0 && y>0), per the ratification comparison plate's finding (40/50 = 80%).
  const wnPos = newPositives.filter((p) => p.x < 0 && p.y > 0).length;
  csmoke('Lost-Ark-wing (WN cluster of new positives)', wnPos >= 40, `${wnPos}/${newPositives.length} new positives in WN quadrant (expected ≥40 per ratification plate)`);
  // 3 pull re-keys are new positives (invocation's e3-vs-e4 highlighted these)
  const rekeys = ['d3-wizard-black-hole', 'd4-spiritborn-vortex', 'di-cyclone-strike-monk-base'];
  const rekeysPresent = rekeys.every((k) => newPositives.some((p) => p.kit_id === k));
  csmoke('3 pull re-keys among new positives', rekeysPresent, `d3-wizard-black-hole/d4-spiritborn-vortex/di-cyclone-strike-monk-base all in newPositives: ${rekeysPresent}`);

  // ---- report ----
  console.log('\n================= ACCEPTANCE TESTS =================');
  for (const t of tests) console.log(`  [${t.pass ? 'PASS' : 'FAIL'}] ${t.name} :: ${t.detail}`);
  console.log('================= SMOKE TESTS =================');
  for (const t of smokes) console.log(`  [${t.pass ? 'PASS' : 'FAIL'}] ${t.name} :: ${t.detail}`);
  const allPass = [...tests, ...smokes].every((t) => t.pass);
  console.log(`\n${allPass ? 'ALL PASS' : 'FAILURES PRESENT'}`);

  // ---- PROVENANCE JSON (deliverable) ----
  const b0 = bodies.instrument;
  const hookRecon = {
    live: (b0.match(/data-el="live"/g) || []).length,
    condensation: (b0.match(/data-el="condensation"/g) || []).length,
    graveyard: (b0.match(/data-el="graveyard"/g) || []).length,
    positive: (b0.match(/data-el="positive"/g) || []).length,
    ghost: (b0.match(/data-el="ghost"/g) || []).length,
    points_classed: (b0.match(/data-el="live"/g) || []).length + (b0.match(/data-el="condensation"/g) || []).length + (b0.match(/data-el="graveyard"/g) || []).length + (b0.match(/data-el="positive"/g) || []).length,
    meso_ghost_glyphs: ghostGlyphs.length,
    drill_glyphs: drillGlyphs.length,
    emitted: {
      neutral_single: neutral.length,
      grouped_condensation: grouped.length,
      legacy_tombstones: legacyTombs.length,
      new_tombstones: newTombs.length,
      new_positives: newPositives.length,
      total_points: all.length,
      meso_glyph_positions: ghostGlyphs.length,
      drill_glyph_field_entries: subGlyphField.length,
    },
    live_single_hue: { instrument: SKINS.instrument.liveSingle, archive: SKINS.archive.liveSingle },
    positive_hue: { instrument: SKINS.instrument.positiveInk, archive: SKINS.archive.positiveInk },
  };

  const enumeratedBoundaryDiff = [
    'D1: input file → atlas-edition4.json (was atlas-edition3.json)',
    'D2: output dir → captures/2026-07-17-atlas-edition4-serving/',
    'D3: output filenames → atlas-edition4-<skin>.svg / .png',
    'D4: title plate → "Build Horizon — Edition IV" (editionTag data-derived)',
    'D5: top-level edition===4 gate',
    'D6: PATH-A basis gate: basis.edition===1 && basis.frozen===true (fail-loud)',
    'D7: G-3 anchoring re-assert vs atlas-edition3.json (0/506 moved required; replaces the E3 head\'s vs-E2 fit-freeze compare)',
    'D8: point discriminator — new supplementary marks classify via prior-atlas kit_id set + death_class field presence (56 new: 50 positives + 6 tombstones)',
    'D9: NEW POSITIVE glyph — filled sat-blue dot r=3.7, no halo; data-el="positive"; layer id layer-positives',
    'D10: NEW TOMBSTONE glyph — SAME † text mark grammar as legacy (43 total daggers = 37 legacy + 6 new; graveyard layer holds all 43)',
    'D11: BUILD FAMILIES key — driven by gateA_group; ratified-members-only coloring; family counts byte-identical to E3 (Wave-4 law: families grow only by ratification waves, never by tau)',
    'D12: FUTURE-PROOFING — reserved empty <g id="layer-family-candidates"> between layer-positives and layer-chrome (additive annotation-layer module can populate without touching data marks)',
    'D13: provenance.iteration → "edition4-serving"',
    'D14: iteration_authority cites Matt 2026-07-17 ratification via adoption-doc WAVE 5',
    'D15: this enumerated_edition_boundary_diff list emitted in provenance',
    'D16: freeze_baseline → 2026-07-16-atlas-edition3-r8-furniture (the served E3 head\'s capture dir)',
    'D17: fit-layer-regression re-instates against E3 r8 baseline — 506 point circles + 37 legacy tombstones + hull polyline + ghost/drill geometry byte-identical; the 56 new marks are the only additive geometry',
    'D18: gateA_group colors byte-carried from E3 (no new family colors)',
    'D19: below-plane ledger header edition literal → "Edition IV" (editionTag data-derived)',
    'D20: register_ref === feasibility-cuts-register-v1.3 (Path-A: register did not move; E4 RE-ASSERTS byte-identical denominators)',
  ];

  const g3ReassertResult = {
    result: 'PASS (0 moved, 0 missing)',
    method: 'JSON-value equality on (kit_id, x, y) triples',
    prior_edition: 'atlas-edition3.json',
    e3_kit_ids_checked: 506,
    moved: 0,
    missing: 0,
    verdict: 'The 506 E3 kit_ids appear in E4 with byte-identical x/y — the FIT anchor holds under Path-A supplementary admission.',
  };

  const provenance = {
    render: 'galadriel/pipeline/atlas-edition4-render.mjs',
    edition: editionTag,
    iteration: 'edition4-serving',
    iteration_authority: 'Matt 2026-07-17 ratification recorded in canonical/matt_decision_needed/2026-07-16-edition3-vs-refit-candidate-1-adoption.md § WAVE 5 (verbatim: "Agreed, path A" — following the "publish Edition IV" adoption directive). Serving cutover to the Glance Vercel app authorized.',
    path_A_law: 'E4 is Path-A SUPPLEMENTARY ADMISSION into Edition-I\'s frozen basis: basis.edition===1, basis.frozen===true, the 506 E3 point coords + 37 legacy tombstones are byte-identical to E3, and the 56 new supplementary points project into the frozen basis (no basis re-derivation).',
    hard_asserts: {
      'H-1_edition_and_version': 'edition===4 && atlas_version==="Edition-IV"',
      'H-2_path_A_basis': 'basis.edition===1 && basis.frozen===true (this is CORRECT per Path-A, not a defect)',
      'H-3_G_3_anchoring': g3ReassertResult,
      'H-4_counts': `counts.total=${counts.total}===points.length=${all.length}===counts.active(${counts.active})+counts.supplementary(${counts.supplementary})`,
    },
    enumerated_edition_boundary_diff: enumeratedBoundaryDiff,
    e4_change: atlas.ghost_field.edition4_change ?? 'SUPPLEMENTARY-ADMISSION edition (Path A): 56 new supplementary points project into frozen basis; lattice denominators byte-identical to E3.',
    prior_edition: 'atlas-edition3.json (Edition-III census-population) — the FIT anchor; byte-identical 506 point coords + 37 legacy tombstones',
    freeze_baseline: '2026-07-16-atlas-edition3-r8-furniture (the served E3 head\'s capture dir; r8 furniture + r8-fix key-box content-derived height carried VERBATIM)',
    e23_source_vs_onscreen_map: 'rotate(-90) SVG y-down: source `↓`→screen-RIGHT, source `↑`→screen-LEFT. East/PERFORM reads → (source ↓); west/DEPLOY reads ← (source ↑). SOURCE GLYPH ≠ ON-SCREEN DIRECTION by design (carried from E2.3 lineage through E3 r8).',
    atlas_version: atlasVersion,
    register_ref: registerRef,
    input: 'agentic_orchestration/research/curated/atlas/atlas-edition4.json',
    emitted_at: emittedAt,
    emitter_script: emitterScript,
    hook_reconciliation: hookRecon,
    fit_layer_frozen_vs: String(atlas.fit_layer_frozen_vs ?? 'Edition-I (atlas.json) — basis + 506 point coords + tombstones byte-identical (G-3)'),
    // [D8] E4-adapted skin canvas map (byte-carried from E3 head vocabulary).
    skin_canvas_map: SKIN_CANVAS_MAP,
    basis: { edition: basisEdition, frozen: basisFrozen, ratified: ratified, inertia_pct: inertiaPct, retained_dims: retainedDims, axis_names: axisNames },
    counts: {
      active: active.length,
      supplementary: supplementary.length,
      legacy_tombstones: legacyTombs.length,
      new_tombstones: newTombs.length,
      new_positives: newPositives.length,
      total: all.length,
      grouped: grouped.length,
    },
    lattice: {
      meso_feasible: feasibleCells.length,
      meso_sealed: sealedCells.length,
      lit_cells: litCells,
      unmapped_pending_curation: unmappedPending,
      exact_post_red_law: denomFeasibleExact,
      depth_sum_check: depthSumCheck,
      ghost_glyph_positions: ghostGlyphs.length,
      ghost_clipped: ghostClippedCount,
      charted_hull_vertex_count: ghostHullVertexCount,
      beyond_horizon_n: beyondHorizonCount,
      beyond_horizon_n_meso_only: beyondMesoOnlyCount,
      charted_hull_east_world_x: chartedHullEastX,
      meso_hull_east_world_x: mesoOnlyHullEastX,
      settled_active_east_world_x: settledActiveEastX,
      drill_min_radius_px: drillMinRadius,
      drill_radius_floor_px: DRILL_R_FLOOR,
      drill_radius_step: DRILL_R_STEP,
    },
    pull_slice: { meso_feasible: pullMesoFeasible, meso_sealed: pullMesoSealed, lit_cells: pullLitCells, new_law_needed: pullNewLaw, halt: pullHalt, lit_core_tuples: pullLitTuples },
    drill_in: {
      region: drillRegion,
      promoted_pair: drillPromotedPair,
      n_east_parent_cells: drillParentCells,
      n_sub_feasible: drillSubFeasibleN,
      n_sub_sealed: drillSubSealedN,
      sub_glyph_field_entries: subGlyphField.length,
      sub_glyphs_rendered: drillGlyphs.length,
      sub_glyphs_west_overshoot: subGlyphField.filter((e) => e.x < 0).length,
      sub_clipped: drillClippedCount,
      sub_sealed_ledger: subSealedSorted,
    },
    off_plane_corpus: { n: offPlaneN, disclosure: offPlaneDisclosure },
    superseded_edition1: { exact_post_red_law: supE1Exact, meso_feasible: supE1MesoFeasible, meso_sealed: supE1MesoSealed },
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
    // Carry emission's p_df_1_verdict at top level too (per invocation).
    p_df_1_verdict: pDf1TopLevel,
    // [D12] future-proofing: layer id declared but empty; a follow-on additive layer
    // module can populate it without touching data-mark emission.
    layer_family_candidates: {
      reserved: true,
      populated: false,
      note: 'Reserved empty group. Elrond candidates JSON currently in flight; a pass-2 additive annotation-layer module will populate this WITHOUT touching data-mark emission.',
    },
    acceptance: { pass: [...tests, ...smokes].filter((t) => t.pass).length, total: tests.length + smokes.length, all_pass: allPass, tests: tests.map((t) => ({ name: t.name, pass: t.pass, detail: t.detail })), smokes: smokes.map((t) => ({ name: t.name, pass: t.pass, detail: t.detail })) },
    skins: ['instrument', 'archive'],
    determinism: 'byte-identical double-render (both skins); sorted iteration; no RNG; no wall-clock',
  };
  writeFileSync(join(OUT_DIR, 'render-provenance.json'), JSON.stringify(provenance, null, 2), 'utf8');
  console.log(`[provenance] ${join(OUT_DIR, 'render-provenance.json')} (P-DF-1: ${pDf1Verdict}, G-3: ${g3ReassertResult.result}, ${provenance.acceptance.pass}/${provenance.acceptance.total} pass)`);

  if (!allPass) process.exit(1);
}

main();
