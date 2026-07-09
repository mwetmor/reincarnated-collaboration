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
  // §5 header strip — the demo-gate counter, derived from the surface-ledger card.
  // null when the ledger doesn't parse (absence-legal).
  surfaces_agreed: SurfacesAgreed | null;
  matt_decision_needed: MattItem[];
  matt_to_do: MattItem[];
  dangling_gates: DanglingGate[];
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

export function githubLink(base: string, path: string, line: number): string {
  return `${base}/${path}#L${line}`;
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
