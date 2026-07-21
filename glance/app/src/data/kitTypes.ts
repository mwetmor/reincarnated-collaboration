// kitTypes.ts — shapes for the per-kit "single source of truth" Glance page.
//
// These mirror the build-time static assets public/kits/index.json + public/kits/<id>.json,
// which are the MATT-APPROVED, FROZEN interface contract (spec:
// agentic_orchestration/gandalf/notes/2026-07-20-glance-per-kit-join-spec.md · sample:
// 2026-07-20-glance-per-kit-sample.json). Elrond emits EXACTLY this shape at scale (all
// 574 kits); drax renders EXACTLY this shape. Any field change requires a re-sync between
// both owners before it lands (drax render-faithfully discipline — zero invention here).
//
// The 10 sections per kit (§ interface contract):
//   spine · mapping · mints_anchored[] · dockets[] · atlas_group · lineage_enrichment ·
//   citations[] · verify_ledger[] · dossier{} · _row_counts
//
// EVERYTHING is defensively nullable. The unlinked/unplaced/silent states are COMMON and
// MEANINGFUL (a feature — this page is also a diagnostic for mechanical sparseness), never
// an error: mints_anchored can be [], atlas_group / lineage_enrichment can be null, dossier
// rows can be `abstained` (source silent), verify verdicts can be UNSUPPORTED. Render all
// gracefully; render `quarantined` citations + `abstained` dossier rows VISUALLY FLAGGED.

// ── shared ───────────────────────────────────────────────────────────────────────────

/** Per-kit density summary — drives the index badges + the detail header chips. */
export interface RowCounts {
  citations: number;
  dossier_facts: number;
  verify_claims: number;
  mints_anchored: number;
  dockets: number;
}

/** Verify verdicts observed in the corpus (per-claim adjudication). */
export type Verdict = 'CONFIRMED' | 'CONTRADICTED' | 'UNSUPPORTED' | string;

// ── the browse/filter index (public/kits/index.json) ───────────────────────────────────

/** One thin row in the browsable index — spine header fields + density counts. */
export interface KitIndexRow {
  kit_id: string;
  folk_name: string | null;
  game: string | null;
  tier: string | null;
  grade: string | null;
  terminal_state: string | null;
  _row_counts: RowCounts;
}

// ── section 1 · spine (kit_master VIEW — the 25-field header) ───────────────────────────

export interface KitSpine {
  kit_id: string;
  folk_name: string | null;
  game: string | null;
  corpus_bucket: string | null;
  tier: string | null;
  canon_tier: string | null;
  eras: string | null;
  negative: number | null;
  is_system: number | null;
  lineage: string | null;
  gx: string | null;
  source: string | null;
  provenance_tag: string | null;
  source_date: string | null;
  grade: string | null;
  terminal_state: string | null;
  deviation_notes: string | null;
  mapping_provenance: string | null;
  /** normalized to arrays by the generator (comma-string → []); [] renders "none attested". */
  elements_attested: string[];
  ailments_attested: string[];
  citation_count: number | null;
  verify_confirmed: number | null;
  verify_contradicted: number | null;
  verify_unsupported: number | null;
  dossier_rows: number | null;
}

// ── section 2 · mapping (kit_mapping — grade + parsed mapping_json) ─────────────────────

export interface MappingSkill {
  source_skill: string | null;
  geometry_value: string | null;
  element_primary: string | null;
  element_secondary: string | null;
  ailments: string[] | null;
  delivery_notes: string | null;
}

/** mapping_json is a parsed payload; its inner shape varies by kit. We type the fields the
 *  render surfaces directly and keep the rest as unknown-ish (rendered as key/value where
 *  present). Never invented — only read what the emission carries. */
export interface MappingJson {
  skills?: MappingSkill[];
  motion_frame?: string | null;
  resource_economy?: Record<string, unknown> | null;
  trigger_grammar?: Record<string, unknown> | null;
  t4_doors?: string[] | null;
  scaffold?: {
    chain_count?: number | null;
    support_lanes?: Record<string, string[]> | null;
  } | null;
  option_c_substrate_flags?: unknown;
  fidelity_notes?: string | null;
  [k: string]: unknown;
}

export interface KitMapping {
  grade: string | null;
  terminal_state: string | null;
  deviation_notes: string | null;
  mapping_provenance: string | null;
  /** parsed JSON; may be a string if the source was non-JSON (generator leaves raw). */
  mapping_json: MappingJson | string | null;
}

// ── section 3 · mints_anchored[] (mint_ledger — mints this kit forced; may be []) ───────

export interface MintAnchored {
  mint_id: number;
  evidence_tier: string | null;
  mint_class: string | null;
  build_authorized: number | null;
  description: string | null;
}

// ── section 4 · dockets[] (mechanic_gap_docket — gaps citing this kit; sample shows []) ──

export interface Docket {
  docket_id: number | string;
  mechanism_class: string | null;
  docket_family: string | null;
  destination: string | null;
  disposition: string | null;
  status: string | null;
}

// ── section 5 · atlas_group (atlas_gateA_labels_* — plane group; may be null) ───────────

export interface AtlasGroup {
  group: string | null;
  group_intent_rationale: string | null;
}

// ── section 6 · lineage_enrichment (roster_lineage_enrichment — null when unplaced) ─────
// Shape is the full roster_lineage_enrichment row; null for corpus kits not yet placed in
// roster_atlas (expected + common). Kept as an open record — rendered as key/value pairs.
export type LineageEnrichment = Record<string, unknown>;

// ── section 7 · citations[] (kit_citations — every source; quarantined flagged) ─────────

export interface Citation {
  url: string | null;
  archive_url: string | null;
  site: string | null;
  author_handle: string | null;
  title: string | null;
  cite_class: string | null;
  rank_class: string | null;
  /** 1 = quarantined (recorded but NOT authoritative) → render visually flagged. */
  quarantined: number;
}

// ── section 8 · verify_ledger[] (verify_ledger — per-claim verdicts) ────────────────────

export interface VerifyClaim {
  claim_family: string | null;
  verdict: Verdict;
  claim_text: string | null;
  anchor_quote: string | null;
  source_url: string | null;
  run_tag: string | null;
}

// ── section 9 · dossier{} (kit_dossier — grouped by 6 families; abstained = source silent) ─

export interface DossierRow {
  /** parsed payload; null when the row abstained (source silent for this family). */
  payload: unknown;
  source_url: string | null;
  anchor_quote: string | null;
  /** 1 = abstained (source silent) → render as "source silent", visually flagged. */
  abstained: number;
  conf: number | null;
}

/** The 6 dossier families (spec). The generator emits a keyed object; a family may be
 *  absent (no rows) or present with a single abstained row. */
export type DossierFamily =
  | 'author_credit'
  | 'capstone_alterations'
  | 'item_alterations'
  | 'skill_geometry'
  | 'skill_loop'
  | 'variants';

export type Dossier = Partial<Record<DossierFamily, DossierRow[]>> &
  Record<string, DossierRow[] | undefined>;

/** The canonical family render order + human labels (spec: "grouped by 6 families"). */
export const DOSSIER_FAMILY_ORDER: DossierFamily[] = [
  'skill_geometry',
  'skill_loop',
  'variants',
  'capstone_alterations',
  'item_alterations',
  'author_credit',
];

export const DOSSIER_FAMILY_LABEL: Record<DossierFamily, string> = {
  skill_geometry: 'Skill geometry',
  skill_loop: 'Skill loop',
  variants: 'Variants',
  capstone_alterations: 'Capstone alterations',
  item_alterations: 'Item alterations',
  author_credit: 'Author credit',
};

// ── the full per-kit object (public/kits/<kit_id>.json) ────────────────────────────────

export interface KitDetail {
  kit_id: string;
  spine: KitSpine;
  mapping: KitMapping | null;
  mints_anchored: MintAnchored[];
  dockets: Docket[];
  atlas_group: AtlasGroup | null;
  lineage_enrichment: LineageEnrichment | null;
  citations: Citation[];
  verify_ledger: VerifyClaim[];
  dossier: Dossier;
  _row_counts: RowCounts;
  /** present only when the generator couldn't find the kit in kit_master. */
  _error?: string;
}

// ── provenance stamp (public/kits/kits-provenance.json) ────────────────────────────────

export interface KitsProvenance {
  title: string;
  derivation: string;
  source_mode: 'sample-5kit' | 'full-corpus' | string;
  source_path: string;
  source_commit: string;
  kit_count: number;
  staged_at: string;
  note?: string;
}

// ── display helpers ────────────────────────────────────────────────────────────────────

/** Title-case a game slug for display only (never mutates the underlying value). */
export function displayGame(slug: string | null): string {
  if (!slug) return '—';
  return slug
    .split(/[-_]/)
    .map((w) => (w.length <= 3 ? w.toUpperCase() : w[0].toUpperCase() + w.slice(1)))
    .join(' ');
}

/** Grade → tone chip classes (static — safelist-safe, no dynamic construction). */
export function gradeTone(grade: string | null): string {
  switch (grade) {
    case 'EXACT':
      return 'border-emerald-700 bg-emerald-900/40 text-emerald-300';
    case 'CLOSE':
      return 'border-sky-700 bg-sky-900/40 text-sky-300';
    case 'APPROX':
      return 'border-amber-700 bg-amber-900/40 text-amber-300';
    case 'GAPPED':
      return 'border-rose-700 bg-rose-900/40 text-rose-300';
    default:
      return 'border-slate-600 bg-slate-800 text-slate-300';
  }
}

/** Verdict → tone chip classes (static). */
export function verdictTone(v: Verdict): string {
  switch (v) {
    case 'CONFIRMED':
      return 'border-emerald-700 bg-emerald-900/40 text-emerald-300';
    case 'CONTRADICTED':
      return 'border-rose-700 bg-rose-900/40 text-rose-300';
    case 'UNSUPPORTED':
      return 'border-amber-700 bg-amber-900/40 text-amber-300';
    default:
      return 'border-slate-600 bg-slate-800 text-slate-300';
  }
}

/** Sum the five density counts (the kit's total corpus-row weight). */
export function rowCountTotal(rc: RowCounts): number {
  return rc.citations + rc.dossier_facts + rc.verify_claims + rc.mints_anchored + rc.dockets;
}
