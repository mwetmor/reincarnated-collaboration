// The state.json contract (§3). Kept in lockstep with parser/parse.mjs output.
// The parser is the source of truth; this type mirrors what it emits.

export type StatusToken =
  | 'open'
  | 'in_flight'
  | 'blocked'
  | 'awaiting_ruling'
  | 'parked'
  | 'closed';

export interface GatesOn {
  token: string;
  qualifier: string | null;
  resolved: boolean;
  dangling?: boolean;
}

export interface QueueRow {
  id: string;
  cells_md: string[];
  owner: string | null;
  status: { token: StatusToken; prose: string };
  gates_on: GatesOn[];
  line: number;
}

export interface Queue {
  title: string;
  line: number;
  kind: 'table' | 'bullet';
  rows: QueueRow[];
}

export interface Delta {
  date: string;
  headline: string;
  body_md: string;
  line: number;
}

export interface StatusBanner {
  stamp: string | null;
  date: string | null;
  raw: string;
  line: number;
}

export interface Counters {
  open: number;
  in_flight: number;
  blocked: number;
  awaiting_ruling: number;
  parked: number;
  closed: number;
}

// §2.7 FLOW — a stage's derived state. `dominant` is a StatusToken OR 'quiet'
// (a stage whose mapped sections carry no modeled rows).
export type FlowDominant = StatusToken | 'quiet';

export interface FlowStage {
  n: number;
  name: string;
  refs: string[];
  resolved: boolean;
  counters: Counters;
  dominant: FlowDominant;
  line: number;
  // §2.7 drill-through — line of the first resolved `##` heading this stage claims
  // (its stage sub-heading, e.g. `## S0` / `## E5`). null when the ref dangles.
  heading_line?: number | null;
}

export interface Flow {
  line: number;
  stages: FlowStage[];
}

export interface DanglingFlowRef {
  ref: string;
  // the source id — a TrackerId for tracker FLOW blocks, a PipelineId for the
  // MATT-FACING pipeline docs (§7.5 v1.6). Kept loose (string) since both feed it.
  tracker: string;
  stage: number;
  path: string;
  line: number;
}

// §7.5 v1.6 — the MATT-FACING product pipeline docs. NOT trackers (no page/card of
// their own): they are FLOW-source + verbatim-ASCII drill docs. The /engine and
// /content-emission pages render THESE FLOW bars as their lead (see PAGE_FLOW_SOURCE).
export type PipelineId = 'battle-sim' | 'serial-emission' | 'game' | 'story' | 'arcade';

export interface Pipeline {
  id: PipelineId;
  path: string;
  // §2.7 FLOW — always present for a well-formed pipeline doc; null if the doc
  // declares no `## FLOW`.
  flow: Flow | null;
  // the fenced ASCII flow diagram, rendered VERBATIM as a <pre> (never parsed).
  ascii: { text: string; line: number } | null;
  // §7.6 rule 3 — the `SCOPE RIDER — POST-LAUNCH:` blockquote (arcade pipeline). A
  // targeted verbatim string grab, NOT a legislated parse shape. null when absent.
  scope_rider?: { text: string; line: number } | null;
}

// §7.7 v1.9 — the kit-design reference TRIO. MATT-FACING FLOW-led verbatim-payload
// docs (same doc class as the pipelines); NOT trackers, NOT pipelines. Each backs one
// page (/coordinates · /mechanics · /atlas). Their FLOW bars are quiet-by-design
// (reference registers — no modeled queue rows); the bar is navigation, not state.
export type ReferenceId = 'coordinates' | 'mechanics' | 'atlas';

// One `## §N` payload section, carried VERBATIM (rendered, never parsed). `ref` is the
// leading section token (`§0`, `§1`, …) — the FLOW-stage drill-through target.
export interface ReferenceSection {
  ref: string;
  title: string;
  body: string; // raw markdown — the payload (lattice/resolver/projection tables); NOT parsed
  heading_line: number;
}

export interface Reference {
  id: ReferenceId;
  path: string;
  status_banner: StatusBanner | null;
  // §2.7 FLOW — quiet-by-design (all stages derive `quiet`); null if no `## FLOW`.
  flow: Flow | null;
  // the verbatim `## §N` payload sections, in document order.
  sections: ReferenceSection[];
}

export type TrackerId =
  | 'engine'
  | 'story'
  | 'game'
  | 'serial-content-emission'
  | 'surface-ledger';

export interface SurfacesAgreed {
  agreed: number;
  total: number;
}

export interface Tracker {
  id: TrackerId;
  path: string;
  status_banner: StatusBanner | null;
  deltas: Delta[];
  queues: Queue[];
  counters: Counters;
  // §2.7 — present ONLY when the tracker declares a `## FLOW` section.
  flow?: Flow;
  // §7.2 — present ONLY on the surface-ledger card: surfaces agreed vs. total.
  surfaces_agreed?: SurfacesAgreed;
}

export interface MattItem {
  id: string;
  title: string;
  resolved: boolean;
  path: string;
  line: number;
}

export interface DanglingGate {
  token: string;
  row: string;
  path: string;
  line: number;
}

export interface State {
  generated_at: string;
  repo_sha: string | null;
  gh_blob_base: string;
  last_commit: {
    sha: string | null;
    author: string | null;
    date: string | null;
    subject: string | null;
    // true when `date` is the build timestamp (generated_at) used as an honest
    // proxy because the Vercel build container had no true commit date. The UI
    // labels the age as build-time in that case rather than claiming commit-time.
    date_is_build_time_proxy?: boolean;
  };
  trackers: Tracker[];
  // §7.5 v1.6 — the MATT-FACING product pipeline docs (battle-sim + serial-emission).
  pipelines: Pipeline[];
  // §7.7 v1.9 — the kit-design reference TRIO (coordinates + mechanics + atlas).
  references: Reference[];
  // §5 header strip — the demo-gate counter, derived from the surface-ledger card.
  // null when the ledger doesn't parse (absence-legal).
  surfaces_agreed: SurfacesAgreed | null;
  matt_decision_needed: MattItem[];
  matt_to_do: MattItem[];
  dangling_gates: DanglingGate[];
  // §2.7 — FLOW section-refs that resolve to no `##` heading (visible debt, not a failure).
  dangling_flow_refs: DanglingFlowRef[];
  // U-1 §12.4 — the flight-recorder tape, pre-aggregated by parser/fleet.mjs.
  // `null` = this repo has no agentic_orchestration/flight/ at all (absence is legal, and
  // OPTIONAL here so a state.json produced before this field existed still type-checks).
  fleet?: Fleet | null;
}

// ---------------------------------------------------------------------------
// U-1 fleet flight-recorder — the REAR-VIEW node (§12.4)
//
// History only, by construction. There is no in-flight list, no lane liveness and no
// health here, because a Vercel build can only ever see PUSHED state — those facts live
// on the local board (factory/ui/board.py), which can read the disk it runs on.
// `units_total` / `units_sealed` are DENOMINATORS so no rollup reads as a census; they
// are not state lanes.
// ---------------------------------------------------------------------------

export interface FleetTokens {
  input: number;
  cached_input: number;
  cache_write: number;
  output: number;
  reasoning: number;
}

/** Every aggregate carries its own denominator: unmeasured is never zero. */
export interface FleetBucket {
  units: number;
  tokens: FleetTokens;
  /** how many CLOSE rows actually reported tokens — the tokens' denominator */
  n_tokens: number;
  rc_zero: number;
  rc_total: number;
  verdicts: Record<string, number>;
  /** v1.1 CLOSE-only optional field: vendor-REPORTED dollars, summed only where present */
  cost_usd: number;
  /** how many CLOSE rows carried cost_usd — the cost's denominator */
  n_cost: number;
  median_wall_s: number | null;
  currencies: string[];
}

export interface FleetWorkstream extends FleetBucket {
  workstream: string;
  curation_rows: number;
  warns: number;
  first_ts: string | null;
  last_ts: string | null;
  /** first-start → last-close: a RUN DURATION, not enqueue→seal */
  span_s: number | null;
}

export interface FleetScorecard extends FleetBucket {
  provider: string;
  pin: string | null;
  artifacts: number;
}

export interface FleetLaneClose {
  unit_id: string;
  ts: string;
  rc: number | null;
  tokens_input: number | null;
  tokens_output: number | null;
  cost_usd: number | null;
  workstream: string | null;
}

export interface FleetLane extends FleetBucket {
  lane: string;
  provider: string;
  /** AM-1 parity: the card renders whether or not this is true; false says so honestly */
  on_tape: boolean;
  /** which spellings of this lane the tape actually carries (v1 `grok-judge` → v1.1 `grok-serial`) */
  spellings_seen: string[];
  pins: string[];
  last_close: FleetLaneClose | null;
}

export interface FleetVerdictRow {
  ts: string;
  event: string;
  unit_id: string | null;
  workstream: string | null;
  verdict: string;
  gate_id: string | null;
  gatekeeper: string | null;
}

export interface FleetSnapshot {
  ts: string;
  currency: string | null;
  /** the meter's own vocabulary, preserved RAW (§5) — never normalised into a percentage */
  meter_raw: unknown;
}

export interface FleetMonth extends FleetBucket {
  month: string;
}

export interface Fleet {
  source: string;
  tape_files: string[];
  rows_on_disk: number;
  rows_after_corrections: number;
  unparseable_lines: number;
  schema_versions: number[];
  coverage: { first_ts: string | null; last_ts: string | null };
  units_total: number;
  units_sealed: number;
  workstreams: FleetWorkstream[];
  scorecards: FleetScorecard[];
  lanes: FleetLane[];
  claude: { units: number; closes: number; with_tokens: number };
  months: FleetMonth[];
  verdicts: { totals: Record<string, number>; recent: FleetVerdictRow[] };
  snapshots: FleetSnapshot[];
}

// ---- fleet display helpers (pure, no state) ----

export function fmtTokens(n: number | null | undefined): string {
  if (n == null) return '—';
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `${Math.round(n / 1000)}K`;
  return String(n);
}

export function fmtSpan(s: number | null | undefined): string {
  if (s == null) return '—';
  if (s < 5400) return `${Math.round(s / 60)}m`;
  if (s < 172800) return `${(s / 3600).toFixed(1)}h`;
  return `${(s / 86400).toFixed(1)}d`;
}

/** Cache hit-rate is DERIVED, never stored — and null when there is no denominator. */
export function cacheRate(t: FleetTokens): number | null {
  return t.input > 0 ? (100 * t.cached_input) / t.input : null;
}

// ---- shared display helpers ----

export const TRACKER_LABEL: Record<TrackerId, string> = {
  engine: 'Engine',
  story: 'Story',
  game: 'Game',
  'serial-content-emission': 'Serial Content Emission',
  'surface-ledger': 'Surface Ledger',
};

export const STATUS_LABEL: Record<StatusToken, string> = {
  open: 'Open',
  in_flight: 'In-flight',
  blocked: 'Blocked',
  awaiting_ruling: 'Awaiting ruling',
  parked: 'Parked',
  closed: 'Closed',
};

export const STATUS_SYMBOL: Record<StatusToken, string> = {
  open: '○',
  in_flight: '◐',
  blocked: '⛔',
  awaiting_ruling: '⚖',
  parked: '⏸',
  closed: '✓',
};

// Tailwind color class per status (safelisted in tailwind.config.js).
export const STATUS_COLOR: Record<StatusToken, { chip: string; dot: string }> = {
  open: { chip: 'bg-slate-800 text-slate-300 border-slate-600', dot: 'bg-slate-500' },
  in_flight: { chip: 'bg-sky-900/40 text-sky-300 border-sky-700', dot: 'bg-sky-500' },
  blocked: { chip: 'bg-rose-900/40 text-rose-300 border-rose-700', dot: 'bg-rose-500' },
  awaiting_ruling: { chip: 'bg-amber-900/40 text-amber-300 border-amber-700', dot: 'bg-amber-500' },
  parked: { chip: 'bg-violet-900/40 text-violet-300 border-violet-700', dot: 'bg-violet-500' },
  closed: { chip: 'bg-emerald-900/40 text-emerald-300 border-emerald-700', dot: 'bg-emerald-500' },
};

// §2.7 flow-bar segment color per dominant token (+ the row-less `quiet` neutral).
// The bg-* classes are safelisted in tailwind.config.js.
export const FLOW_SEGMENT_COLOR: Record<FlowDominant, string> = {
  blocked: 'bg-rose-500/80',
  awaiting_ruling: 'bg-amber-500/80',
  in_flight: 'bg-sky-500/80',
  open: 'bg-slate-500/70',
  parked: 'bg-violet-500/70',
  closed: 'bg-emerald-500/80',
  quiet: 'bg-slate-700/50',
};

export const FLOW_DOMINANT_LABEL: Record<FlowDominant, string> = {
  blocked: 'blocked',
  awaiting_ruling: 'awaiting ruling',
  in_flight: 'in-flight',
  open: 'open',
  parked: 'parked',
  closed: 'closed',
  quiet: 'quiet (no rows)',
};

// ---- the five domain pages (§7.4 — v1.5) ----
// A "page" maps to a tracker. The surface-ledger is NOT a page (it renders as a
// drawer on every page + full on whichever page expands it); it is deliberately absent
// from PAGE_ORDER so the five-tab nav shows exactly five tabs (§7.4.1).
//
// `kits` and `content-emission` BOTH back the serial-content-emission tracker (§7.4):
//   - `/kits`             leads with (and shows only) the PART F roster — the NOUN-list.
//   - `/content-emission` leads flow-bar-first, roster GONE — the PROCESS-flow.
// The roster moved OUT of content-emission (v1.4's lead-element law is DEAD).
export type PageId =
  | 'engine' | 'story' | 'game' | 'content-emission' | 'kits' | 'minigames'
  // §7.7 v1.9 — the reference TRIO. Seated ADJACENT in the read-as-one-instrument
  // order: sample the coordinate (/coordinates) → project the fields (/atlas) →
  // verify the surfaces (/mechanics) — the dispatch's recommended nav adjacency.
  | 'coordinates' | 'atlas' | 'mechanics';

export const PAGE_ORDER: PageId[] = [
  'engine', 'story', 'game', 'content-emission', 'kits', 'minigames',
  'coordinates', 'atlas', 'mechanics',
];

// §7.7 v1.9 — the three reference pages (a distinct kind from the tracker pages). Kept
// as a set so the nav can group them visually and the landing tiles iterate just these.
export const REFERENCE_PAGES: PageId[] = ['coordinates', 'atlas', 'mechanics'];
export function isReferencePage(p: PageId): boolean {
  return REFERENCE_PAGES.includes(p);
}

export const PAGE_LABEL: Record<PageId, string> = {
  engine: 'Engine',
  story: 'Story',
  game: 'Game',
  'content-emission': 'Content Emission',
  kits: 'Kits',
  minigames: 'Minigames',
  coordinates: 'Coordinates',
  atlas: 'Atlas',
  mechanics: 'Mechanics',
};

// §7.7 v1.9 — the page ↔ reference-doc binding, and the TRIPLE-LAW cross-link
// metadata. Each reference page links the OTHER TWO, labeled by layer.
export const PAGE_REFERENCE: Partial<Record<PageId, ReferenceId>> = {
  coordinates: 'coordinates',
  atlas: 'atlas',
  mechanics: 'mechanics',
};

// The three-layer identity for the TRIPLE-LAW cross-links (§7.7 rule 4).
export interface TripleLaw {
  page: PageId;
  ref: ReferenceId;
  layer: string;   // LATTICE / PROJECTION / CODEX
  role: string;    // the load-bearing one-liner
}
export const TRIPLE_LAW: Record<ReferenceId, TripleLaw> = {
  coordinates: { page: 'coordinates', ref: 'coordinates', layer: 'LATTICE', role: 'WHERE a kit can sit' },
  atlas:       { page: 'atlas',       ref: 'atlas',       layer: 'PROJECTION', role: 'how the two map' },
  mechanics:   { page: 'mechanics',   ref: 'mechanics',   layer: 'CODEX', role: 'WHAT the engine expresses' },
};
// The two siblings each reference page cross-links to (the other two layers).
export const TRIPLE_LAW_SIBLINGS: Record<ReferenceId, ReferenceId[]> = {
  // /atlas is the connective page; its two links are the most load-bearing.
  coordinates: ['atlas', 'mechanics'],
  atlas: ['coordinates', 'mechanics'],
  mechanics: ['coordinates', 'atlas'],
};

// the tracker id backing each page. Both content-emission and kits are backed by the
// serial-content-emission tracker (they render different leads off the same doc). The
// reference-trio pages (§7.7 v1.9) have NO backing tracker — they are NOT in this map;
// consumers gate on isReferencePage() before any PAGE_TRACKER lookup.
export const PAGE_TRACKER: Partial<Record<PageId, TrackerId>> = {
  engine: 'engine',
  story: 'story',
  game: 'game',
  'content-emission': 'serial-content-emission',
  kits: 'serial-content-emission',
  // §7.6 v1.8 — /minigames has NO tracker of its own; the arcade doc is a pipeline,
  // not a tracker. Its build-gate lives in the game tracker (B6 / taxonomy §9.1
  // endgame fork), so /minigames backs the game tracker for card/delta home purposes
  // but leads flow-bar-first off the arcade PIPELINE (see PAGE_FLOW_SOURCE). The page
  // renders pipeline-lead-only — it does NOT surface the game tracker's queues/deltas.
  minigames: 'game',
};

// §7.5 v1.6 — the lead FLOW-bar source for each page, ONE config line per page.
//   { kind: 'tracker' }              → render the backing tracker's own `## FLOW`.
//   { kind: 'pipeline', id }         → render the MATT-FACING pipeline doc's FLOW.
// The two PROCESS pages repoint to the product pipelines; the rest keep their
// tracker FLOW. When the story/game pipeline docs land, flip those two lines here.
export type FlowSource =
  | { kind: 'tracker' }
  | { kind: 'pipeline'; id: PipelineId };

// The reference-trio pages (§7.7 v1.9) lead off their reference doc's OWN `## FLOW`
// (quiet-by-design), handled directly in the ReferencePage component — they are NOT
// in this map (consumers gate on isReferencePage first).
export const PAGE_FLOW_SOURCE: Partial<Record<PageId, FlowSource>> = {
  engine: { kind: 'pipeline', id: 'battle-sim' },        // S0–S8 product pipeline
  story: { kind: 'pipeline', id: 'story' },               // N0–N5 product pipeline (v1.7)
  game: { kind: 'pipeline', id: 'game' },                 // G0–G8 product pipeline (v1.7)
  'content-emission': { kind: 'pipeline', id: 'serial-emission' }, // E0–E8 product pipeline
  kits: { kind: 'tracker' },                              // /kits has no lead FLOW bar
  minigames: { kind: 'pipeline', id: 'arcade' },          // A0–A7 product pipeline (v1.8)
};

// The canonical "home page" for a tracker's card/deltas. For the serial tracker this
// is content-emission (the PROCESS page); /kits is a second view of the same tracker but
// is NOT the tracker's delta/card home. First-match in PAGE_ORDER yields content-emission.
export function pageForTracker(id: TrackerId): PageId | null {
  const found = (Object.keys(PAGE_TRACKER) as PageId[]).find((p) => PAGE_TRACKER[p] === id);
  return found ?? null;
}

export function githubLink(base: string, path: string, line: number): string {
  return `${base}/${path}#L${line}`;
}

// Sum of the six status counts (excludes nothing — the modeled-row total).
export function counterTotal(c: Counters): number {
  return c.open + c.in_flight + c.blocked + c.awaiting_ruling + c.parked + c.closed;
}

// "Since you last looked" watermark = max delta-date seen (§5, localStorage).
export const WATERMARK_KEY = 'glance:last-seen-delta-date';

export function maxDeltaDate(trackers: Tracker[]): string | null {
  let max: string | null = null;
  for (const t of trackers) {
    for (const d of t.deltas) {
      if (!max || d.date > max) max = d.date;
    }
  }
  return max;
}

export function commitAge(iso: string | null): string {
  if (!iso) return 'unknown';
  const then = new Date(iso).getTime();
  const now = Date.now();
  const s = Math.max(0, Math.floor((now - then) / 1000));
  if (s < 60) return `${s}s ago`;
  const m = Math.floor(s / 60);
  if (m < 60) return `${m}m ago`;
  const h = Math.floor(m / 60);
  if (h < 24) return `${h}h ago`;
  const d = Math.floor(h / 24);
  return `${d}d ago`;
}
