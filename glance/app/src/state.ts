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
export type PipelineId = 'battle-sim' | 'serial-emission';

export interface Pipeline {
  id: PipelineId;
  path: string;
  // §2.7 FLOW — always present for a well-formed pipeline doc; null if the doc
  // declares no `## FLOW`.
  flow: Flow | null;
  // the fenced ASCII flow diagram, rendered VERBATIM as a <pre> (never parsed).
  ascii: { text: string; line: number } | null;
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
  // §5 header strip — the demo-gate counter, derived from the surface-ledger card.
  // null when the ledger doesn't parse (absence-legal).
  surfaces_agreed: SurfacesAgreed | null;
  matt_decision_needed: MattItem[];
  matt_to_do: MattItem[];
  dangling_gates: DanglingGate[];
  // §2.7 — FLOW section-refs that resolve to no `##` heading (visible debt, not a failure).
  dangling_flow_refs: DanglingFlowRef[];
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
export type PageId = 'engine' | 'story' | 'game' | 'content-emission' | 'kits';

export const PAGE_ORDER: PageId[] = ['engine', 'story', 'game', 'content-emission', 'kits'];

export const PAGE_LABEL: Record<PageId, string> = {
  engine: 'Engine',
  story: 'Story',
  game: 'Game',
  'content-emission': 'Content Emission',
  kits: 'Kits',
};

// the tracker id backing each page. Both content-emission and kits are backed by the
// serial-content-emission tracker (they render different leads off the same doc).
export const PAGE_TRACKER: Record<PageId, TrackerId> = {
  engine: 'engine',
  story: 'story',
  game: 'game',
  'content-emission': 'serial-content-emission',
  kits: 'serial-content-emission',
};

// §7.5 v1.6 — the lead FLOW-bar source for each page, ONE config line per page.
//   { kind: 'tracker' }              → render the backing tracker's own `## FLOW`.
//   { kind: 'pipeline', id }         → render the MATT-FACING pipeline doc's FLOW.
// The two PROCESS pages repoint to the product pipelines; the rest keep their
// tracker FLOW. When the story/game pipeline docs land, flip those two lines here.
export type FlowSource =
  | { kind: 'tracker' }
  | { kind: 'pipeline'; id: PipelineId };

export const PAGE_FLOW_SOURCE: Record<PageId, FlowSource> = {
  engine: { kind: 'pipeline', id: 'battle-sim' },        // S0–S8 product pipeline
  story: { kind: 'tracker' },                             // (pipeline doc TBD)
  game: { kind: 'tracker' },                              // (pipeline doc TBD)
  'content-emission': { kind: 'pipeline', id: 'serial-emission' }, // E0–E8 product pipeline
  kits: { kind: 'tracker' },                              // /kits has no lead FLOW bar
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
