#!/usr/bin/env node
// build-atlas-interactive.mjs
// Build-time data-slim script for the interactive-atlas Glance package.
//
// PURPOSE: produce `public/atlas/atlas-interactive.json` FROM the in-repo
// `agentic_orchestration/research/curated/atlas/atlas-edition4.json` by COPY / GROUP
// of emitted fields ONLY. No invention. Every field emitted here is a direct copy (or
// a mechanical derivation — quadrant sign-pair, or the E4 3-class cls derived from
// `supplementary` + `death_class` presence per the E4 renderer's own discriminator) of
// an EMITTED atlas field.
//
// The full 7.5MB atlas JSON must NEVER ship to the client bundle. This script is the
// seam: the fat source stays in `research/curated/` (never imported, never in
// `public/`), and only the ~1.9MB derivative lands in `public/atlas/`.
//
// v1.13 E4 SERVING CUTOVER (drax, Matt-ruled 2026-07-17): flipped to Edition-IV.
// Key schema differences from E3 (adapted mechanically here):
//   (1) E4 points do NOT carry `cls`/`condensation`/`death_class` — those were
//       derived-at-render for E3 too, but the render head had access to E3-carried
//       classification. Here we derive the SAME way galadriel's render head did:
//       cls = supplementary=false ? 'live'
//           : death_class!=null   ? 'graveyard'
//           : 'positive'
//       (43 tombstones = 37 legacy + 6 new; 50 positives; 469 live active.)
//   (2) supplementary=true is NOT synonymous with graveyard in E4 (positives are
//       supplementary=true with no death_class). This is a Path-A distinction, not a
//       bug; we CANNOT collapse it. counts.supplementary=93 splits into 43+50.
//   (3) basis.edition===1 && basis.frozen===true (Path-A supplementary admission
//       into the FROZEN Edition-I basis). This is CORRECT per Matt-ratified law —
//       we ASSERT on it (do NOT "fix").
//   (4) A new `data-el="positive"` mark class appears in the plate SVGs (50 marks)
//       + a reserved empty <g id="layer-family-candidates"> — those are RENDER-side
//       artifacts; the interactive JSON's job is to expose the 50 as cls='positive'
//       kits + the 6 new tombstones as cls='graveyard'.
//   (5) E4 points may carry OPTIONAL new fields: `franchise`, `cos2`,
//       `edition_admitted`, `level_flattened`. None are read here (we render
//       faithfully off the emitted x/y/kit_id + derived cls); unknown-key inertness
//       preserves the never-invent floor.
//
// BUILD-FAIL GUARD: if any expected emitted field is missing or renamed in the
// source atlas, this script FAILS LOUDLY (non-zero exit) rather than emitting a
// silently-degraded derivative. Same guard class as the render-provenance JSON
// (spec §5). Demonstrate with a doctored field-rename: the guard fires.
//
// Spec: agentic_orchestration/operating-procedures/glance-contract-spec-2026-07-03.md §7.8
// Data of record: atlas-edition4.json (Edition-IV, emitted 2026-07-17T02:42:46Z;
// galadriel-verified 52/52 acceptance, G-3 anchoring PASS 0-moved/0-missing.)
//
// Run: node scripts/atlas/build-atlas-interactive.mjs
//   Optional first arg: alternate source path (used by the doctored-field test).
//   Optional --out: alternate output path (used by the doctored-field test).

import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const __dirname = dirname(fileURLToPath(import.meta.url));
// glance/app/scripts/atlas → glance/app is two up; the collab meta-repo root is four up.
const REPO_ROOT = resolve(__dirname, '..', '..');
const COLLAB_ROOT = resolve(__dirname, '..', '..', '..', '..');

// The fat Edition-IV emission — in-repo BUILD INPUT ONLY (never client-shipped).
const DEFAULT_SOURCE = resolve(
  COLLAB_ROOT,
  'agentic_orchestration/research/curated/atlas/atlas-edition4.json'
);
// v1.13: the prior-edition E3 emission — READ-ONLY SECONDARY INPUT. E4 points don't
// carry `cls`/`condensation`/`death_class`; galadriel's render head discriminated new-
// vs-carried marks via the E3 kit_id set + death_class presence. For carried E3 rows
// we cross-reference E3 to validate our derivation (the classification is derivable
// from E4 alone — supplementary + death_class + gateA_group — but the E3 file gives
// us a byte-level assert that we haven't drifted the 506 carried classifications).
// Fail-loud if absent (the guard is: E3 must be reachable at the ratified path).
const DEFAULT_PRIOR_SOURCE = resolve(
  COLLAB_ROOT,
  'agentic_orchestration/research/curated/atlas/atlas-edition3.json'
);
const DEFAULT_OUT = resolve(REPO_ROOT, 'public/atlas/atlas-interactive.json');

// D1-h: the READ-ONLY corpus provenance sidecar, vendored as a build input. Joined
// on kit_id to add folk_name/game/era_year/stabilization_patch to kit rows so the
// pivot's build leaf rows read `folk_name — game year (patch)` instead of the slug.
// Exported by scripts/atlas/export-kit-provenance-sidecar.mjs; carries its own
// provenance header. The FROZEN atlas-edition4.json is UNTOUCHED — this join happens
// at slim-build time.
const DEFAULT_SIDECAR = resolve(__dirname, 'kit-provenance-sidecar.json');

// D2-a: the READ-ONLY 14-axis ENGINE-KEY sidecar, vendored as a build input. Joined on
// kit_id to add the FULL 14-axis coordinate (cell_key split) to build rows so the pivot
// grid shows real per-build axis codes (not `—`, which D1-g emitted before this pass
// superseded it). Exported one-shot from corpus.db canon_engine_key (+ canon_corpus
// naming columns) by scripts/atlas/export-engine-key-sidecar.mjs; carries its own
// provenance + derivation-receipt header. The FROZEN atlas-edition4.json is UNTOUCHED.
const DEFAULT_ENGINE_KEY_SIDECAR = resolve(__dirname, 'engine-key-sidecar.json');

// ---- CLI ----
const argv = process.argv.slice(2);
let sourcePath = DEFAULT_SOURCE;
let priorSourcePath = DEFAULT_PRIOR_SOURCE;
let outPath = DEFAULT_OUT;
let sidecarPath = DEFAULT_SIDECAR;
let engineKeySidecarPath = DEFAULT_ENGINE_KEY_SIDECAR;
for (let i = 0; i < argv.length; i++) {
  const a = argv[i];
  if (a === '--out') {
    outPath = resolve(argv[++i]);
  } else if (a === '--sidecar') {
    sidecarPath = resolve(argv[++i]);
  } else if (a === '--engine-key-sidecar') {
    engineKeySidecarPath = resolve(argv[++i]);
  } else if (a === '--prior') {
    priorSourcePath = resolve(argv[++i]);
  } else if (!a.startsWith('--')) {
    sourcePath = resolve(argv[i]);
  }
}

// ---- Build-fail guard machinery ----
class BuildFailError extends Error {}

/** Assert `obj` has own property `key`; else HALT loudly. */
function requireField(obj, key, ctx) {
  if (obj == null || !Object.prototype.hasOwnProperty.call(obj, key)) {
    throw new BuildFailError(
      `BUILD-FAIL GUARD: expected emitted field '${key}' missing in ${ctx}. ` +
        `The atlas source schema changed (field renamed or dropped). ` +
        `Refusing to emit a silently-degraded derivative. ` +
        `Reconcile scripts/atlas/build-atlas-interactive.mjs against the new emit, ` +
        `then re-run.`
    );
  }
  return obj[key];
}

/**
 * Read an OPTIONAL emitted field that is present on only one point-kind.
 * Returns the value if the key exists, else the provided default (null).
 * These are kind-specific in the emit: `death_class` only on graveyard points,
 * `gateA_group` only on live points. Absence is legal; a RENAME is caught by the
 * downstream presence-floor assertions (see build()).
 */
function readOptional(obj, key, dflt = null) {
  return Object.prototype.hasOwnProperty.call(obj, key) ? obj[key] : dflt;
}

/** Assert `obj` is an array of expected length (or non-empty if len omitted). */
function requireArray(obj, key, ctx, expectedLen) {
  const v = requireField(obj, key, ctx);
  if (!Array.isArray(v)) {
    throw new BuildFailError(
      `BUILD-FAIL GUARD: emitted field '${key}' in ${ctx} is ${typeof v}, expected array.`
    );
  }
  if (expectedLen != null && v.length !== expectedLen) {
    throw new BuildFailError(
      `BUILD-FAIL GUARD: emitted array '${key}' in ${ctx} has length ${v.length}, ` +
        `expected ${expectedLen}. Lattice/point count drift — reconcile before emit.`
    );
  }
  return v;
}

// ---- Quadrant: sign pair of (x, y) under region names EN / ES / WN / WS ----
// x >= 0 => EAST, x < 0 => WEST ; y >= 0 => NORTH, y < 0 => SOUTH.
// (Region-name convention per spec §5; PERFORM side = EAST, EMBODY side = NORTH.)
function quadrant(x, y) {
  return (x >= 0 ? 'E' : 'W') + (y >= 0 ? 'N' : 'S');
}

/**
 * Build a kit_id -> provenance-row map from the vendored corpus sidecar (D1-h).
 * The sidecar is `{ __provenance__, rows: [{kit_id, folk_name, game, era_year,
 * stabilization_patch}] }`. Every atlas kit_id MUST resolve a row WITH a folk_name
 * (build HALT otherwise — extends the verify:atlas-guard pattern). Other fields are
 * optional; missing => null => the renderer shows nothing (zero invention).
 */
function loadProvenanceIndex(sidecar) {
  const rows = requireArray(sidecar, 'rows', 'kit-provenance-sidecar');
  const index = new Map();
  for (const r of rows) {
    const kitId = requireField(r, 'kit_id', 'kit-provenance-sidecar.rows[]');
    // folk_name/game/era_year/stabilization_patch are read defensively — a MISSING
    // key on a row is legal (the row simply carries less), but a full-column rename
    // is caught by the atlas-side coverage floor (every atlas kit needs folk_name).
    index.set(kitId, {
      folk_name: readOptional(r, 'folk_name'),
      game: readOptional(r, 'game'),
      era_year: readOptional(r, 'era_year'),
      stabilization_patch: readOptional(r, 'stabilization_patch'),
    });
  }
  return index;
}

/**
 * Build a kit_id -> engine-key-values map from the D2-a engine-key sidecar.
 * The sidecar is `{ __provenance__, axes:[{pos,axis,column,grain}], rows:[{kit_id,
 * cell_key, values:{<axis>:<value|null>}}] }`. Returns { axes, index } where index is
 * kit_id -> { cell_key, values }. Not every atlas kit need have an engine key (kits
 * absent show `—` per D2-b) — this is a SOFT join (unlike the D1-h folk_name floor).
 * The `axes` schema is carried through to pole_vocabulary so the client renders the
 * DERIVED axis names/order (never a hand-typed client constant).
 */
function loadEngineKeyIndex(sidecar) {
  const axes = requireArray(sidecar, 'axes', 'engine-key-sidecar');
  // Guard: the axes schema must carry pos/axis/column for each of the 14 (derivation
  // truth). A missing/renamed field => the sidecar is malformed => HALT (never emit a
  // silently-degraded axis schema).
  for (const a of axes) {
    requireField(a, 'pos', 'engine-key-sidecar.axes[]');
    requireField(a, 'axis', 'engine-key-sidecar.axes[]');
    requireField(a, 'column', 'engine-key-sidecar.axes[]');
  }
  const rows = requireArray(sidecar, 'rows', 'engine-key-sidecar');
  const index = new Map();
  for (const r of rows) {
    const kitId = requireField(r, 'kit_id', 'engine-key-sidecar.rows[]');
    const values = requireField(r, 'values', 'engine-key-sidecar.rows[]');
    const cellKey = readOptional(r, 'cell_key');
    index.set(kitId, { cell_key: cellKey, values });
  }
  // Carry the derivation receipt through for the provenance panel (audit trail).
  const provenance = readOptional(sidecar, '__provenance__');
  return { axes, index, provenance };
}

/**
 * Build a kit_id -> E3-point map for the E3-carried classification cross-reference.
 * Only used to validate the derived cls for the 506 carried E3 kit_ids (byte-level
 * floor: E3 marked N as supplementary => E4 must mark the SAME N as supplementary
 * WITH the same death_class). Ghost/basis fields are ignored — only per-point
 * (supplementary, death_class, gateA_group) are compared.
 */
function loadE3Index(source) {
  const pts = requireArray(source, 'points', 'atlas-edition3 root');
  const idx = new Map();
  for (const p of pts) {
    idx.set(p.kit_id, {
      supplementary: p.supplementary === true,
      death_class: readOptional(p, 'death_class'),
      gateA_group: readOptional(p, 'gateA_group'),
    });
  }
  return idx;
}

function build(source, provenanceIndex, engineKey, e3Index) {
  // --- Top-level fields we depend on (copy, never invent) ---
  // v1.13 E4: assert edition + Path-A basis at the top of build (guard trip HALTs).
  const edition = requireField(source, 'edition', 'atlas root');
  if (edition !== 4) {
    throw new BuildFailError(
      `BUILD-FAIL GUARD: expected edition===4 (Edition-IV serving), got ${edition}. ` +
        `The source is not the ratified E4 emission — HALT.`
    );
  }
  const atlasVersion = requireField(source, 'atlas_version', 'atlas root');
  if (atlasVersion !== 'Edition-IV') {
    throw new BuildFailError(
      `BUILD-FAIL GUARD: expected atlas_version==="Edition-IV", got "${atlasVersion}". HALT.`
    );
  }
  const emittedAt = requireField(source, 'emitted_at', 'atlas root');
  const emitterScript = requireField(source, 'emitter_script', 'atlas root');
  const counts = requireField(source, 'counts', 'atlas root');
  const basis = requireField(source, 'basis', 'atlas root');
  // Path-A guard: E4 admits new points into E1's FROZEN basis; asserting this is the
  // whole point of the Path-A ratification. A shift here would falsify the E4 story
  // (a re-fit hiding as a supplementary admission) and MUST HALT.
  const basisEdition = requireField(basis, 'edition', 'atlas.basis');
  const basisFrozen = requireField(basis, 'frozen', 'atlas.basis');
  if (basisEdition !== 1 || basisFrozen !== true) {
    throw new BuildFailError(
      `BUILD-FAIL GUARD: Path-A basis violated. Expected basis.edition===1 && basis.frozen===true ` +
        `(E4 admits into E1's frozen basis), got basis.edition=${basisEdition}, basis.frozen=${basisFrozen}. HALT.`
    );
  }
  const axisNames = requireField(basis, 'axis_names', 'atlas.basis');
  const points = requireArray(source, 'points', 'atlas root');
  const ghostField = requireField(source, 'ghost_field', 'atlas root');

  // --- Ghost sub-structure ---
  const coreOrder = requireArray(ghostField, 'core_order', 'atlas.ghost_field', 7);
  const feasibleCells = requireArray(ghostField, 'feasible_cells', 'atlas.ghost_field');

  // --- Emitted counts we reconcile against (fail-fast on drift) ---
  // E4 counts: {active, supplementary, total, legacy_tombstones, new_tombstones,
  //             new_positives, held_out_dossier_owed, new_supplementary_edition4,
  //             null_death_class_sentineled}. We reconcile against the four we USE.
  const nActive = requireField(counts, 'active', 'atlas.counts');
  const nSupplementary = requireField(counts, 'supplementary', 'atlas.counts');
  const nTotal = requireField(counts, 'total', 'atlas.counts');
  const nLegacyTombstones = requireField(counts, 'legacy_tombstones', 'atlas.counts');
  const nNewTombstones = requireField(counts, 'new_tombstones', 'atlas.counts');
  const nNewPositives = requireField(counts, 'new_positives', 'atlas.counts');

  // ============================================================
  // PER-KIT ROWS — E4 3-class derivation (spec E4 D8/D9/D10):
  //   class: live | graveyard | positive  (see AtlasKitRow docs; derived here)
  //     live       = supplementary=false                (469 active)
  //     graveyard  = supplementary=true  && death_class != null  (37 legacy + 6 new = 43)
  //     positive   = supplementary=true  && death_class == null  (50 new — Path-A
  //                                                                admissions, not death-classed)
  //   condensation membership: gateA_group (one of 6 named groups) or null (LIVE ONLY —
  //     positives + graveyard rows do not carry a family in E4).
  //   x, y: emitted point coords (signed, origin-centred projection space)
  //   quadrant: derived sign-pair
  // ============================================================
  const kits = [];
  let seenActive = 0;
  let seenSupplementary = 0;
  let seenGrouped = 0;
  let seenGraveyardWithDeathClass = 0;
  let seenPositives = 0;
  let seenGraveyardTotal = 0;
  // E3-cross-check counters: for the 506 E3-carried kit_ids, our derived cls MUST match
  // E3's supplementary flag (E4 never re-classes a carried E3 point; Path-A is additive).
  let e3CarriedChecked = 0;
  const e3ClsMismatch = [];
  // D1-h provenance-join coverage counters (reported; folk_name is a HARD floor).
  let covFolkName = 0;
  let covGame = 0;
  let covYear = 0;
  let covPatch = 0;
  const missingFolkName = [];
  // D2-a engine-key join coverage (SOFT — kits absent show `—`). Per-axis non-null
  // coverage on the atlas set is reported (acceptance 50). `blank`->null is already
  // applied in the sidecar; `unknown` is a curated non-null value (counts as covered).
  const engineAxes = engineKey?.axes ?? [];
  let covEngineKey = 0; // kits that resolved ANY engine key
  const covPerAxis = new Map(engineAxes.map((a) => [a.axis, 0]));
  for (const p of points) {
    // Universal fields — STRICT: a rename of any of these HALTS the build.
    const kitId = requireField(p, 'kit_id', 'atlas.points[]');
    const supplementary = requireField(p, 'supplementary', 'atlas.points[]');
    const x = requireField(p, 'x', 'atlas.points[]');
    const y = requireField(p, 'y', 'atlas.points[]');
    // Kind-specific fields — OPTIONAL per point-kind (present on only one kind).
    // A rename across ALL points is caught by the presence-floor asserts below.
    const gateAGroup = readOptional(p, 'gateA_group'); // live points only
    const deathClass = readOptional(p, 'death_class'); // graveyard points only

    // v1.13 E4: 3-class derivation. supplementary=false => live; supplementary=true
    // splits on death_class presence (graveyard vs positive). This mirrors galadriel's
    // render-head discriminator (D8: "new supplementary marks classify via prior-atlas
    // kit_id set + death_class field presence"). We do NOT need the E3-carried set to
    // classify — the two E4 fields alone are sufficient — but we cross-check the 506
    // carried rows against E3 as an integrity floor (below).
    let cls;
    if (!supplementary) {
      cls = 'live';
      seenActive++;
    } else if (deathClass != null) {
      cls = 'graveyard';
      seenSupplementary++;
      seenGraveyardWithDeathClass++;
      seenGraveyardTotal++;
    } else {
      cls = 'positive';
      seenSupplementary++;
      seenPositives++;
    }
    if (gateAGroup != null) seenGrouped++;

    // E3 cross-check: any kit_id present in E3 must have the SAME supplementary +
    // death_class in E4 (Path-A additive law). This is a byte-level floor on the 506
    // carried rows — a mismatch here means E4 re-classed an E3-carried point, which
    // would falsify the Path-A story. HALT on ANY drift.
    if (e3Index && e3Index.has(kitId)) {
      e3CarriedChecked++;
      const e3 = e3Index.get(kitId);
      if (
        e3.supplementary !== supplementary ||
        (e3.death_class ?? null) !== (deathClass ?? null)
      ) {
        e3ClsMismatch.push({
          kit_id: kitId,
          e3: { supplementary: e3.supplementary, death_class: e3.death_class },
          e4: { supplementary, death_class: deathClass },
        });
      }
    }

    // D1-h: JOIN the corpus provenance row on kit_id. folk_name is MANDATORY per the
    // atlas coverage floor (probed 562/562 on E4); a missing folk_name => build HALT.
    const prov = provenanceIndex.get(kitId) ?? null;
    const folkName = prov?.folk_name ?? null;
    if (folkName != null && folkName !== '') covFolkName++;
    else missingFolkName.push(kitId);
    const game = prov?.game ?? null;
    if (game != null && game !== '') covGame++;
    const eraYear = prov?.era_year ?? null;
    if (eraYear != null && eraYear !== '') covYear++;
    const patch = prov?.stabilization_patch ?? null;
    if (patch != null && patch !== '') covPatch++;

    // D2-a: JOIN the 14-axis engine key on kit_id (SOFT — absent => null => renders —).
    const ek = engineKey?.index?.get(kitId) ?? null;
    const engineKeyValues = ek?.values ?? null; // { <axis>: <value|null> } or null
    if (engineKeyValues != null) {
      covEngineKey++;
      for (const a of engineAxes) {
        const v = engineKeyValues[a.axis];
        // covered = a non-null value (blank was already normalised to null in the
        // sidecar; 'unknown' is a curated value and DOES count as covered).
        if (v != null && v !== '') covPerAxis.set(a.axis, covPerAxis.get(a.axis) + 1);
      }
    }

    kits.push({
      kit_id: kitId,
      cls, // 'live' | 'graveyard' | 'positive'  (E4 3-class derivation)
      condensation: gateAGroup, // null for Single live + positives + graveyard rows
      death_class: deathClass, // string for graveyard; null for live + positives
      x,
      y,
      quadrant: quadrant(x, y),
      // D1-h corpus provenance (copies of canon_corpus fields; null renders nothing).
      folk_name: folkName,
      game, // slug (e.g. 'chronicon'); title-cased for DISPLAY only, string traces to corpus
      era_year: eraYear, // number|null
      stabilization_patch: patch, // string|null
      // D2-a engine-key: the full 14-axis coordinate (cell_key split, blank->null).
      // null when the kit has no engine key; individual axes null when that part was
      // `blank`; 'unknown' preserved literally (curated value, D2-b).
      engine_key: engineKeyValues,
    });
  }

  // D1-h HARD FLOOR: every atlas kit must resolve a sidecar folk_name (E4: 562/562).
  // A miss means the sidecar is stale vs the atlas point set — HALT rather than ship
  // slug fallbacks (extends the verify:atlas-guard never-degrade contract).
  if (missingFolkName.length > 0) {
    throw new BuildFailError(
      `BUILD-FAIL GUARD: ${missingFolkName.length} atlas kit_id(s) resolved NO folk_name in the ` +
        `corpus provenance sidecar (e.g. ${missingFolkName.slice(0, 5).join(', ')}). ` +
        `The sidecar is stale vs the atlas point set. Re-export ` +
        `scripts/atlas/kit-provenance-sidecar.json from corpus.db (via export-kit-provenance-sidecar.mjs), ` +
        `then re-run. HALT.`
    );
  }

  // E3 CARRIED-CLASSIFICATION FLOOR: the 506 E3-carried kit_ids MUST retain their E3
  // supplementary+death_class in E4 (Path-A additive law — this is the derivation
  // guard for the render-side discriminator). HALT on ANY drift.
  if (e3ClsMismatch.length > 0) {
    throw new BuildFailError(
      `BUILD-FAIL GUARD: ${e3ClsMismatch.length} E3-carried kit_id(s) have DRIFTED supplementary/death_class ` +
        `between E3 and E4 (Path-A violated: E4 must be additive, never re-class carried rows). ` +
        `First 3: ${JSON.stringify(e3ClsMismatch.slice(0, 3))}. HALT.`
    );
  }

  // Reconcile against emitted counts — drift => HALT (guard extends to counts).
  if (seenActive !== nActive) {
    throw new BuildFailError(
      `BUILD-FAIL GUARD: derived live-kit count ${seenActive} != emitted counts.active ${nActive}.`
    );
  }
  if (seenSupplementary !== nSupplementary) {
    throw new BuildFailError(
      `BUILD-FAIL GUARD: derived supplementary-kit count ${seenSupplementary} != emitted counts.supplementary ${nSupplementary}.`
    );
  }
  if (kits.length !== nTotal) {
    throw new BuildFailError(
      `BUILD-FAIL GUARD: kit row count ${kits.length} != emitted counts.total ${nTotal}.`
    );
  }
  // E4-specific: the 43 graveyard split (37 legacy + 6 new) and the 50 positives must
  // both reconcile against emitted counts. The split isn't discoverable from a single
  // point (we can't tell "legacy" from "new" without the E3 set, which we DO have) —
  // but the TOTAL graveyard count and the TOTAL positives are direct derivations.
  const nGraveyardExpected = nLegacyTombstones + nNewTombstones;
  if (seenGraveyardTotal !== nGraveyardExpected) {
    throw new BuildFailError(
      `BUILD-FAIL GUARD: derived graveyard count ${seenGraveyardTotal} != emitted ` +
        `counts.legacy_tombstones(${nLegacyTombstones})+counts.new_tombstones(${nNewTombstones})=${nGraveyardExpected}. HALT.`
    );
  }
  if (seenPositives !== nNewPositives) {
    throw new BuildFailError(
      `BUILD-FAIL GUARD: derived positives count ${seenPositives} != emitted counts.new_positives ${nNewPositives}. HALT.`
    );
  }

  // Presence-floor asserts — catch a RENAME of a kind-specific field even though
  // that field is legally absent on the OTHER kind. If `gateA_group` were renamed
  // across all live points, seenGrouped collapses to 0; if `death_class` were
  // renamed across all graveyard points, seenGraveyardWithDeathClass collapses.
  if (seenGrouped === 0) {
    throw new BuildFailError(
      `BUILD-FAIL GUARD: zero condensation members found — the 'gateA_group' field ` +
        `appears renamed or dropped across all live points (expected 6 named groups). HALT.`
    );
  }
  const distinctGroups = new Set(
    kits.filter((k) => k.condensation != null).map((k) => k.condensation)
  );
  if (distinctGroups.size !== 6) {
    throw new BuildFailError(
      `BUILD-FAIL GUARD: found ${distinctGroups.size} distinct condensation groups ` +
        `(${[...distinctGroups].join(', ')}), expected 6. Group vocabulary drift — HALT.`
    );
  }
  // E4: graveyard is a STRICT SUBSET of supplementary now (positives share the flag),
  // so the presence-floor for death_class shifts: every GRAVEYARD row carries a
  // death_class, but supplementary rows split (43 with, 50 without). Assert the "with"
  // count matches the graveyard total (== 43). A total rename would collapse this to 0.
  if (seenGraveyardWithDeathClass !== seenGraveyardTotal) {
    throw new BuildFailError(
      `BUILD-FAIL GUARD: ${seenGraveyardWithDeathClass}/${seenGraveyardTotal} graveyard kits ` +
        `carry a death_class — the 'death_class' field appears renamed or dropped. HALT.`
    );
  }

  // ============================================================
  // PER-GHOST-CELL ROWS
  //   core: emitted 7-tuple (order == core_order)
  //   depth: emitted denominator depth
  //   lit / kit_count: emitted (used by pivot leaf + legend Ghosts branch)
  //   x, y, quadrant: emitted coords + derived sign-pair
  // ============================================================
  const ghosts = [];
  for (const c of feasibleCells) {
    const core = requireField(c, 'core', 'atlas.ghost_field.feasible_cells[]');
    if (!Array.isArray(core) || core.length !== coreOrder.length) {
      throw new BuildFailError(
        `BUILD-FAIL GUARD: ghost cell 'core' arity ${
          Array.isArray(core) ? core.length : 'not-array'
        } != core_order arity ${coreOrder.length}.`
      );
    }
    const depth = requireField(c, 'depth', 'atlas.ghost_field.feasible_cells[]');
    const lit = requireField(c, 'lit', 'atlas.ghost_field.feasible_cells[]');
    const kitCount = requireField(c, 'kit_count', 'atlas.ghost_field.feasible_cells[]');
    const x = requireField(c, 'x', 'atlas.ghost_field.feasible_cells[]');
    const y = requireField(c, 'y', 'atlas.ghost_field.feasible_cells[]');

    ghosts.push({
      core,
      depth,
      lit,
      kit_count: kitCount,
      x,
      y,
      quadrant: quadrant(x, y),
    });
  }

  // ============================================================
  // POLE VOCABULARY
  //   axis_names: the two projection-plane axis pole strings (verbatim)
  //   core_axes: for each ghost core axis, its name + the emitted distinct
  //     value set (derived by scan of feasible_cells; used as pivot levels).
  //     These VALUE SETS are pure copies of what the emit contains — no synthesis.
  // ============================================================
  const coreAxisValues = coreOrder.map(() => new Set());
  for (const c of feasibleCells) {
    for (let i = 0; i < coreOrder.length; i++) {
      coreAxisValues[i].add(c.core[i]);
    }
  }
  // D2-a: derive the engine-key axis VALUE vocabularies on the atlas set (scan of the
  // joined engine_key values) so the client renders DERIVED names/order + can show the
  // vocabulary without shipping the corpus. `null` values (blank sentinel) are skipped;
  // `unknown` (curated) is included.
  const engineAxisValues = new Map(engineAxes.map((a) => [a.axis, new Set()]));
  for (const k of kits) {
    if (k.engine_key == null) continue;
    for (const a of engineAxes) {
      const v = k.engine_key[a.axis];
      if (v != null && v !== '') engineAxisValues.get(a.axis).add(v);
    }
  }

  const poleVocabulary = {
    axis_names: axisNames, // { dim1: "PERFORM <-> DEPLOY", dim2: "EMBODY <-> LAUNCH" }
    core_order: coreOrder,
    core_axes: coreOrder.map((name, i) => ({
      axis: name,
      values: [...coreAxisValues[i]].sort(),
    })),
    // D2-a: the DERIVED 14-axis engine-key schema (order + name + naming-column + grain)
    // carried verbatim from the sidecar's receipt so the client NEVER hand-types axis
    // names/order. Values are the derived-on-atlas vocabularies (audit + column headers).
    engine_key_axes: engineAxes.map((a) => ({
      pos: a.pos,
      axis: a.axis,
      column: a.column,
      grain: a.grain ?? 'kit',
      values: [...(engineAxisValues.get(a.axis) ?? new Set())].sort(),
    })),
    // Region-name legend so the pivot / quadrant labels never re-derive convention.
    quadrant_regions: {
      EN: 'EAST-NORTH',
      ES: 'EAST-SOUTH',
      WN: 'WEST-NORTH',
      WS: 'WEST-SOUTH',
    },
  };

  return {
    // --- provenance stamp: this derivative's lineage back to the fat source ---
    schema_version: '1.1', // v1.13 E4: KitClass widened to 3-class ('positive' added)
    derived_from: {
      atlas_version: atlasVersion,
      edition,
      emitted_at: emittedAt,
      emitter_script: emitterScript,
      source_bytes: null, // filled in by caller (post-read)
      // Path-A basis stamp — the interactive JSON surfaces the frozen basis so any
      // client-side receipt (or future audit) can cite it without opening the fat file.
      basis: {
        edition: basisEdition,
        frozen: basisFrozen,
      },
    },
    counts: {
      kits: kits.length,
      kits_live: seenActive,
      kits_graveyard: seenGraveyardTotal, // 43 (37 legacy + 6 new)
      // v1.13 E4: the 50 new-positive marks (Path-A supplementary admissions, no death).
      kits_positive: seenPositives,
      kits_condensation_members: seenGrouped,
      ghosts: ghosts.length,
      ghosts_lit: ghosts.reduce((n, g) => n + (g.lit ? 1 : 0), 0),
      // Provenance-side counts (surface the E4 emitted split so the receipt panel can
      // cite it verbatim — never hand-typed).
      legacy_tombstones: nLegacyTombstones,
      new_tombstones: nNewTombstones,
      new_positives: nNewPositives,
    },
    // D1-h provenance-join coverage on the atlas kit set (receipts; folk_name is a floor).
    provenance_coverage: {
      folk_name: covFolkName,
      game: covGame,
      era_year: covYear,
      stabilization_patch: covPatch,
      total: kits.length,
    },
    // D2-a engine-key join coverage on the atlas kit set (receipts; SOFT join).
    // per_axis = kits with a NON-NULL value on that axis ('unknown' counts; blank/null
    // does not). Reported for acceptance 50 (per-axis coverage on the atlas set).
    engine_key_coverage: {
      kits_with_engine_key: covEngineKey,
      per_axis: Object.fromEntries(engineAxes.map((a) => [a.axis, covPerAxis.get(a.axis)])),
      total: kits.length,
      // The derivation receipt from the sidecar (part-order + column correspondence),
      // carried through so the provenance panel + audits can cite it without the corpus.
      derivation: engineKey?.provenance ?? null,
    },
    // v1.13 E4: E3 cross-check receipt (the byte-level Path-A additivity floor).
    e3_carried_check: {
      checked: e3CarriedChecked, // 506 (all E3 kit_ids re-appear in E4)
      mismatches: e3ClsMismatch.length, // must be 0 (PASS)
    },
    pole_vocabulary: poleVocabulary,
    kits,
    ghosts,
  };
}

// ---- Main ----
function main() {
  if (!existsSync(sourcePath)) {
    console.error(
      `BUILD-FAIL: source atlas not found at ${sourcePath}. ` +
        `Expected the in-repo Edition-IV emission at ` +
        `agentic_orchestration/research/curated/atlas/atlas-edition4.json.`
    );
    process.exit(2);
  }

  const raw = readFileSync(sourcePath, 'utf8');
  let source;
  try {
    source = JSON.parse(raw);
  } catch (e) {
    console.error(`BUILD-FAIL: source atlas is not valid JSON — ${e.message}`);
    process.exit(2);
  }

  // v1.13 E4: load the READ-ONLY prior-edition (E3) atlas for the Path-A additive
  // cross-check on the 506 carried kit_ids. Absent => HALT (this is the ratified path;
  // a missing E3 file means the working tree is not on the E4 cutover baseline).
  if (!existsSync(priorSourcePath)) {
    console.error(
      `BUILD-FAIL: prior-edition (E3) atlas not found at ${priorSourcePath}. ` +
        `E4 build requires it for the Path-A additive floor (E3-carried classification check). HALT.`
    );
    process.exit(2);
  }
  let priorSource;
  try {
    priorSource = JSON.parse(readFileSync(priorSourcePath, 'utf8'));
  } catch (e) {
    console.error(`BUILD-FAIL: prior-edition atlas is not valid JSON — ${e.message}`);
    process.exit(2);
  }

  // D1-h: load the READ-ONLY corpus provenance sidecar (build HALT if absent —
  // the build names depend on it; degrading to slugs is not allowed).
  if (!existsSync(sidecarPath)) {
    console.error(
      `BUILD-FAIL: corpus provenance sidecar not found at ${sidecarPath}. ` +
        `Export it from corpus.db (scripts/atlas/export-kit-provenance-sidecar.mjs) before building.`
    );
    process.exit(2);
  }
  let sidecar;
  try {
    sidecar = JSON.parse(readFileSync(sidecarPath, 'utf8'));
  } catch (e) {
    console.error(`BUILD-FAIL: provenance sidecar is not valid JSON — ${e.message}`);
    process.exit(2);
  }

  // D2-a: load the READ-ONLY 14-axis engine-key sidecar (build HALT if absent — builds
  // must show their real axis codes; the D1-g `—` state is superseded). This is a SOFT
  // JOIN per kit (a kit absent from the sidecar shows `—`), but the sidecar FILE must
  // exist and be well-formed, or the axis schema cannot be derived => HALT.
  if (!existsSync(engineKeySidecarPath)) {
    console.error(
      `BUILD-FAIL: engine-key sidecar not found at ${engineKeySidecarPath}. ` +
        `Export it from corpus.db (scripts/atlas/export-engine-key-sidecar.mjs) before building.`
    );
    process.exit(2);
  }
  let engineKeySidecar;
  try {
    engineKeySidecar = JSON.parse(readFileSync(engineKeySidecarPath, 'utf8'));
  } catch (e) {
    console.error(`BUILD-FAIL: engine-key sidecar is not valid JSON — ${e.message}`);
    process.exit(2);
  }

  let out;
  try {
    const provenanceIndex = loadProvenanceIndex(sidecar);
    const engineKey = loadEngineKeyIndex(engineKeySidecar);
    const e3Index = loadE3Index(priorSource);
    out = build(source, provenanceIndex, engineKey, e3Index);
  } catch (e) {
    if (e instanceof BuildFailError) {
      console.error(e.message);
      process.exit(1);
    }
    throw e;
  }

  out.derived_from.source_bytes = Buffer.byteLength(raw, 'utf8');

  const minified = JSON.stringify(out);
  writeFileSync(outPath, minified);

  const outBytes = Buffer.byteLength(minified, 'utf8');
  const srcBytes = out.derived_from.source_bytes;
  console.log('atlas-interactive.json built (Edition-IV):');
  console.log(`  source : ${sourcePath}`);
  console.log(`  prior  : ${priorSourcePath}  (E3 cross-check: ${out.e3_carried_check.checked} kit_ids, ${out.e3_carried_check.mismatches} mismatches)`);
  console.log(`  out    : ${outPath}`);
  console.log(
    `  kits   : ${out.counts.kits} (live ${out.counts.kits_live}, graveyard ${out.counts.kits_graveyard} = ${out.counts.legacy_tombstones}+${out.counts.new_tombstones}, positive ${out.counts.kits_positive}, condensation-members ${out.counts.kits_condensation_members})`
  );
  console.log(`  ghosts : ${out.counts.ghosts} (lit ${out.counts.ghosts_lit})`);
  const pc = out.provenance_coverage;
  console.log(
    `  provenance (D1-h corpus join, /${pc.total}): folk_name ${pc.folk_name}, game ${pc.game}, ` +
      `era_year ${pc.era_year}, stabilization_patch ${pc.stabilization_patch}`
  );
  const ec = out.engine_key_coverage;
  console.log(
    `  engine-key (D2-a 14-axis join, /${ec.total}): kits_with_key ${ec.kits_with_engine_key}`
  );
  console.log(
    '    per-axis coverage: ' +
      Object.entries(ec.per_axis)
        .map(([ax, n]) => `${ax}=${n}`)
        .join(' ')
  );
  console.log(
    `  size   : ${outBytes.toLocaleString()} B (${(outBytes / 1024 / 1024).toFixed(2)} MB) ` +
      `vs source ${srcBytes.toLocaleString()} B (${(srcBytes / 1024 / 1024).toFixed(2)} MB) ` +
      `= ${((outBytes / srcBytes) * 100).toFixed(1)}%`
  );
}

main();
