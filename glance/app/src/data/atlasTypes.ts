// atlasTypes.ts — shapes for the interactive-atlas Glance package.
//
// These mirror the build-time derivative `public/atlas/atlas-interactive.json`
// produced by scripts/atlas/build-atlas-interactive.mjs. Every field is a copy
// (or mechanical derivation) of an EMITTED atlas-edition4.json field — no
// invention on the render side (drax render-faithfully discipline).
//
// v1.13 E4 SERVING CUTOVER (drax, Matt-ruled 2026-07-17): the source is now
// Edition-IV (Path-A supplementary admission into Edition-I's frozen basis).
// Point counts widen: 469 active + 93 supplementary = 562 total; the 93 supp
// split into 43 tombstones (37 legacy + 6 new; carry death_class) and 50 new
// POSITIVES (no death_class — Path-A admissions into the frozen basis but not
// death-classed). E4 emission points do NOT carry `cls`/`condensation`/
// `death_class` — those are DERIVED at slim-build time (never invented).
//
// Spec: agentic_orchestration/gandalf/notes/2026-07-15-atlas-interactive-glance-spec.md §5

/** Quadrant = sign pair of (x, y): EN / ES / WN / WS (region names, spec §5). */
export type Quadrant = 'EN' | 'ES' | 'WN' | 'WS';

/**
 * Kit class — E4 3-class model (spec E4 D8/D9/D10/D11):
 *   live (active 469; supplementary=false)
 *   graveyard (supplementary=true AND death_class != null; 43 = 37 legacy + 6 new)
 *   positive (supplementary=true AND death_class == null; 50 new — Path-A admissions
 *             into the frozen basis, not death-classed)
 * Derivation is honest: `supplementary` + `death_class` presence off the emission
 * are the sole discriminators (no invention). Legacy consumers only touching 'live'
 * and 'graveyard' work unchanged; 'positive' kits render as no-family/no-death rows.
 */
export type KitClass = 'live' | 'graveyard' | 'positive';

/** The four legend classes in Matt's vocabulary (spec §4). NOTE: the E4 render adds a
 *  `data-el="positive"` mark class (50 sat-blue dots) — highlighting them from the legend
 *  is a SEPARATE gated charge (islands-toggle wiring). Unknown data-el values are inert
 *  in the current highlight CSS (no per-mark rule = no touch). */
export type LegendClass = 'condensations' | 'live' | 'graveyard' | 'ghosts';

/** One live-or-graveyard kit row (INTERNAL id stays kit_id per Matt's split). */
export interface AtlasKitRow {
  kit_id: string;
  cls: KitClass;
  /** gateA_group: one of the 6 named condensation groups, or null for Single live. */
  condensation: string | null;
  /** death_class: a death-class string for graveyard kits; null for live. */
  death_class: string | null;
  x: number;
  y: number;
  quadrant: Quadrant;
  // ---- D1-h corpus provenance (joined at slim-build time from canon_corpus) ----
  // Every field is a copy of a corpus column; null renders nothing (zero invention).
  /** folk_name — the community-facing build name (atlas coverage 506/506). */
  folk_name: string | null;
  /** game slug (e.g. 'chronicon'); mechanically title-cased for display only. */
  game: string | null;
  /** era_year — release/era year; number or null (atlas coverage 506/506). */
  era_year: number | null;
  /** stabilization_patch — patch string, shown only where curated (atlas 15/506). */
  stabilization_patch: string | null;
  // ---- D2-a: the FULL 14-axis engine-key coordinate (cell_key split; joined at
  // slim-build time from canon_engine_key). Keys are the derived axis names; values are
  // the authoritative cell_key parts. `null` (== the `blank` sentinel) renders `—`;
  // `unknown` is a CURATED value preserved literally (D2-b). null for a kit with no key.
  engine_key: Record<string, string | null> | null;
}

/** One feasible ghost-cell row (the meso lattice). */
export interface AtlasGhostRow {
  /** Emitted 7-tuple, order == pole_vocabulary.core_order. */
  core: string[];
  depth: number;
  lit: boolean;
  kit_count: number;
  x: number;
  y: number;
  quadrant: Quadrant;
}

export interface AtlasCoreAxis {
  axis: string;
  values: string[];
}

/** D2-a: one derived engine-key axis (order + name + naming-column + grain + vocab). */
export interface AtlasEngineKeyAxis {
  pos: number;
  axis: string;
  column: string;
  grain: string;
  values: string[];
}

export interface AtlasPoleVocabulary {
  axis_names: { dim1: string; dim2: string };
  core_order: string[];
  core_axes: AtlasCoreAxis[];
  /** D2-a: the DERIVED 14-axis engine-key schema (order/name/column/grain). Optional so
   *  a pre-D2 JSON still type-checks; the column model degrades to ghost-only if absent. */
  engine_key_axes?: AtlasEngineKeyAxis[];
  quadrant_regions: Record<Quadrant, string>;
}

export interface AtlasInteractiveCounts {
  kits: number;
  kits_live: number;
  kits_graveyard: number;
  /** v1.13 E4: the 50 new-positive kits (Path-A supplementary admissions into the frozen
   *  basis, not death-classed). Optional so pre-E4 JSON still type-checks; a null/absent
   *  value is treated as 0 by the (few) consumers that read this field. */
  kits_positive?: number;
  kits_condensation_members: number;
  ghosts: number;
  ghosts_lit: number;
  /** v1.13 E4: the emitted tombstone + positive split, surfaced for the provenance panel. */
  legacy_tombstones?: number;
  new_tombstones?: number;
  new_positives?: number;
}

/** D2-a: engine-key join coverage receipt (surfaced in the provenance panel). */
export interface AtlasEngineKeyCoverage {
  kits_with_engine_key: number;
  per_axis: Record<string, number>;
  total: number;
  /** Carried-through sidecar derivation receipt (part-order + column correspondence). */
  derivation?: unknown;
}

export interface AtlasInteractiveData {
  schema_version: string;
  derived_from: {
    atlas_version: string;
    /** v1.13 E4: the emitted edition number (4 for the E4 cutover). Optional so pre-E4
     *  JSON still type-checks. */
    edition?: number;
    emitted_at: string;
    emitter_script: string;
    source_bytes: number;
    /** v1.13 E4: the Path-A basis stamp (edition + frozen flag), copied from the fat
     *  emission so consumers can cite the basis without opening the source. */
    basis?: { edition: number; frozen: boolean };
  };
  counts: AtlasInteractiveCounts;
  /** v1.13 E4: E3-carried Path-A additive floor receipt. Optional so pre-E4 JSON still
   *  type-checks; when present, `mismatches` MUST be 0 (asserted at build time). */
  e3_carried_check?: { checked: number; mismatches: number };
  /** D1-h provenance-join coverage (optional; pre-D1-h JSON omits it). */
  provenance_coverage?: Record<string, number>;
  /** D2-a engine-key join coverage (optional; pre-D2 JSON omits it). */
  engine_key_coverage?: AtlasEngineKeyCoverage;
  pole_vocabulary: AtlasPoleVocabulary;
  kits: AtlasKitRow[];
  ghosts: AtlasGhostRow[];
}

// ---- Skin / canvas binding (spec §6 + renderer §10.8e) ----
// NAMING TRUTH (caught + ratified 2026-07-15): the names are inverted vs intuition.
//   'instrument' = LIGHT canvas #f7f8fa
//   'archive'    = DARK  canvas #0e1016   <- the BLACK COPY that LEADS
// All skin selection binds to CANVAS, never to skin name.
export type SkinName = 'instrument' | 'archive';
export type CanvasKind = 'light' | 'dark';

export interface SkinCanvasEntry {
  canvas: CanvasKind;
  hex: string;
}

/**
 * P-DF-1 falsification verdict, carried in render-provenance.json (renderer law).
 * The page surfaces this at RUNTIME from the provenance JSON — never hardcoded
 * (spec §6, acceptance #35). Fields mirror the emitted `p_df_1` block verbatim.
 */
export interface PDf1Verdict {
  verdict: string;
  falsified: boolean;
  S_max: number;
  K_max_beyond_horizon: number;
  n_beyond_horizon_kits: number;
  statement: string;
}

export interface RenderProvenance {
  skin_canvas_map: Record<SkinName, SkinCanvasEntry>;
  skins: SkinName[];
  counts: { active: number; supplementary: number; total: number; grouped: number };
  /** P-DF-1 verdict (existing renderer law) — surfaced in the provenance panel. */
  p_df_1?: PDf1Verdict;
  /** Render + interactive-data lineage stamps (surfaced in the provenance panel). */
  render?: string;
  edition?: string;
  iteration?: string;
  emitted_at?: string;
  // (other provenance fields exist but are not consumed by the page)
  [k: string]: unknown;
}

/** The four quadrant labels, in a stable render order (NW-clockwise-ish). */
export const QUADRANT_ORDER: Quadrant[] = ['WN', 'EN', 'WS', 'ES'];

// ---- Legend entries (spec §4 vocabulary) ----
// Kept here (not in the component file) so the legend component stays
// components-only for react-refresh.
export interface LegendEntry {
  id: LegendClass;
  label: string;
  /** Swatch color — scaffold only; the real highlight is a stroke halo (r7). */
  swatch: string;
  hint: string;
}

/** Four entries, top-to-bottom order per spec §4. D1-i community vocabulary:
 *  kit(s) -> build(s); condensation(s) -> build family / build families. */
export const LEGEND_ENTRIES: LegendEntry[] = [
  {
    id: 'condensations',
    label: 'Build Families',
    swatch: 'bg-indigo-400',
    hint: 'the six named families (WHIRLWIND, TOTEM-SENTRY, TRAP-MINE, CHANNELED-BEAM, AURA, MINION-PET)',
  },
  {
    id: 'live',
    label: 'Live Builds',
    swatch: 'bg-emerald-400',
    hint: 'all live marks — singles + build-family members',
  },
  {
    id: 'graveyard',
    label: 'Graveyard',
    swatch: 'bg-rose-500/80',
    hint: 'the death-classed † builds',
  },
  {
    id: 'ghosts',
    label: 'Ghosts',
    swatch: 'bg-gray-500',
    hint: 'feasible-but-unlit lattice — meso + drill-in ground',
  },
];
