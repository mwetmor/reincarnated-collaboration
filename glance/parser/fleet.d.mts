// glance/parser/fleet.d.mts — the TYPE CONTRACT of fleet.mjs.
//
// Why this file exists: fleet.mjs is plain ESM JavaScript, and the app typechecks under
// `strict` (`tsc -b`, run by CI and by the Vercel build). Any TypeScript importer of an
// untyped .mjs module is TS7016 — and every callback fed from its return values is then
// TS7006. Declaring the module's real shape here fixes the cause once; suppressing at the
// import site would have hidden four true findings behind one `any`.
//
// SCOPE: declaration only. It adds no runtime code and changes no emitted value. Where this
// file and fleet.mjs disagree, fleet.mjs is right and this is the bug — exactly as fleet.mjs
// itself defers to `flight/schema.py`.
//
// RELATION TO app/src/state.ts: `Fleet` and its members there are the CONSUMER mirror — what
// the app reads back out of state.json after the JSON round-trip. The names here match it
// deliberately, so the two stay diff-able and a later consolidation is a re-export away.
//
// REAR-VIEW ONLY: there is no in-flight list, no lane liveness and no health type here,
// because the node carries none. A type that cannot be spelled is a scope that cannot drift.

/** One row of the flight-recorder tape, as parsed from JSONL. Unknown keys are legal: the
 *  tape is append-only and forward-compatible, so the reader must tolerate fields it has
 *  never heard of rather than reject the row. */
export interface TapeRow {
  row_id: string;
  ts: string;
  event: string;
  unit_id?: string | null;
  /** row_id of the row this one supersedes (view-level only; disk is untouched) */
  corrects?: string | null;
  rc?: number | null;
  verdict?: string | null;
  gate_id?: string | null;
  gatekeeper?: string | null;
  workstream?: string | null;
  warn_count?: number | null;
  currency?: string | null;
  cost_usd?: number | null;
  tokens_input?: number | null;
  tokens_cached_input?: number | null;
  tokens_cache_write?: number | null;
  tokens_output?: number | null;
  tokens_reasoning?: number | null;
  artifacts?: unknown[] | null;
  meter_raw?: unknown;
  v?: number | null;
  [key: string]: unknown;
}

/** Identity folded from a unit's own ENQUEUE/START rows; CLOSE only fills what they left
 *  null. A gatekeeper who filed one event does not thereby own the run. */
export interface FleetIdent {
  provider?: string;
  lane?: string;
  pin?: string;
  model_echo?: string;
  harness?: string;
  harness_version?: string;
  currency?: string;
  operator?: string;
  seam?: string;
  repo?: string;
  workstream?: string;
}

export type FleetUnitState = 'OPEN' | 'QUEUED' | 'IN-FLIGHT' | 'SEALED';

export interface FleetUnit {
  unit_id: string;
  /** the unit's own rows, time-then-event ordered */
  rows: TapeRow[];
  state: FleetUnitState;
  ident: FleetIdent;
  close: TapeRow | null;
  first_ts: string;
  last_ts: string;
  /** START → CLOSE seconds; null unless BOTH are on the tape */
  duration: number | null;
}

export interface TapeRead {
  rows: TapeRow[];
  files: string[];
  /** malformed lines are COUNTED, never guessed at */
  unparseable: number;
  present: boolean;
}

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
  n_tokens: number;
  rc_zero: number;
  rc_total: number;
  verdicts: Record<string, number>;
  cost_usd: number;
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
  on_tape: boolean;
  spellings_seen: string[];
  pins: string[];
  last_close: FleetLaneClose | null;
}

export interface FleetMonth extends FleetBucket {
  month: string;
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
  /** the meter's own vocabulary, preserved RAW — never normalised into a percentage */
  meter_raw: unknown;
}

/** The pre-aggregated rear-view node. `units_total` / `units_sealed` are DENOMINATORS. */
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

/** Read every monthly tape in a directory. */
export function readTape(dir: string | null | undefined): TapeRead;

/** Drop rows superseded by a later row carrying `corrects`. Disk is untouched. */
export function applyCorrections(rows: TapeRow[]): TapeRow[];

/** Fold tape rows into per-unit records. */
export function fold(rows: TapeRow[]): FleetUnit[];

/** Build the `fleet` node. `null` when there is no tape directory at all — absence is never
 *  an error. */
export function buildFleet(
  flightDir: string | null | undefined,
  options?: { repoRelative?: string },
): Fleet | null;
