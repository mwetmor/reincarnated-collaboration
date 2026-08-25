// glance/parser/fleet.mjs — the U-1 flight-recorder tape → pre-aggregated `fleet` node.
//
// Spec: gandalf/notes/2026-08-24-fleet-flightrecorder-board-spec-DRAFT.md § 12.4 (Matt:
// "stage it in") + § 13 AM-1 (grok parity). One tape, two windows:
//
//   local fleet board (factory/ui/board.py) = the WINDSHIELD — live lanes, auth, unpushed,
//     staleness. Minute-fresh, pre-push, Mac-local facts a Vercel build can never see.
//   Glance fleet card (this file)           = the REAR-VIEW MIRROR — history only:
//     per-workstream cost, per-model scorecards, per-lane rollups, month trend, verdict
//     history, window-meter history. History does not stale, so a push-fresh render of it
//     is honest by construction.
//
// REAR-VIEW SCOPE, ENFORCED HERE: this module emits NO live lane, NO IN-FLIGHT list, NO
// HEALTH. `units_total` / `units_sealed` ship only as DENOMINATORS so no rollup can read as
// a census — never as a state lane. A structurally-impossible-pre-push fact must not appear
// on a surface that can only see pushed state.
//
// ROLLUPS, NOT RAW ROWS (§ 12.4): the fold happens here, server-side-of-push, so state.json
// carries a few KB of aggregates instead of the tape. No LLM anywhere — deterministic parse,
// same law as the rest of Glance.
//
// FOLD SEMANTICS ARE STAR-LORD'S, MIRRORED: corrections drop superseded rows from the VIEW
// (never from disk); a unit's identity is folded from its own ENQUEUE/START rows first and
// its CLOSE row only fills what they left null (a gatekeeper who judged one event does not
// thereby own the run); SEALED means a terminal event is present. Where this file and
// `flight/schema.py` disagree, `flight/schema.py` is right and this is the bug.

import { existsSync, readdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

// Event ordering for the intra-timestamp tiebreak — schema.py EVENTS, verbatim.
const EVENTS = ['ENQUEUE', 'START', 'GATE', 'HALT', 'CURATION', 'SNAPSHOT', 'CLOSE'];
const TERMINAL = new Set(['CLOSE']);

// AM-1 grok parity: these two lanes are rendered WHENEVER the card renders, even with zero
// rows, so "the grok lane exists and has done nothing yet" is visibly different from "the
// grok lane is not a thing here". `grok-judge` is the frozen-v1 spelling of the same stream
// (v1.1 renames it `grok-serial`); both fold onto one card so the node is correct against a
// pre-amendment tape, a post-amendment tape, and a tape carrying both.
const VENDOR_LANES = [
  { lane: 'codex-serial', provider: 'openai', aliases: ['codex-serial'] },
  { lane: 'grok-serial', provider: 'xai', aliases: ['grok-serial', 'grok-judge'] },
];

const IDENTITY_FIELDS = [
  'provider', 'lane', 'pin', 'model_echo', 'harness', 'harness_version', 'currency',
  'operator', 'seam', 'repo', 'workstream',
];

function median(values) {
  if (!values.length) return null;
  const v = [...values].sort((a, b) => a - b);
  const n = v.length;
  return n % 2 ? v[(n - 1) / 2] : (v[n / 2 - 1] + v[n / 2]) / 2;
}

function tsSeconds(ts) {
  const ms = Date.parse(ts);
  return Number.isNaN(ms) ? null : ms / 1000;
}

/** Read every monthly tape in a directory. Malformed lines are COUNTED, never guessed at. */
export function readTape(dir) {
  const out = { rows: [], files: [], unparseable: 0 };
  if (!dir || !existsSync(dir)) return { ...out, present: false };
  const files = readdirSync(dir)
    .filter((f) => /^records-\d{4}-\d{2}\.jsonl$/.test(f))
    .sort();
  out.files = files;
  for (const f of files) {
    const text = readFileSync(join(dir, f), 'utf8');
    for (const line of text.split('\n')) {
      const s = line.trim();
      if (!s) continue;
      try {
        out.rows.push(JSON.parse(s));
      } catch {
        out.unparseable += 1;
      }
    }
  }
  return { ...out, present: true };
}

/** Drop rows superseded by a later row carrying `corrects`. Disk is untouched. */
export function applyCorrections(rows) {
  const corrected = new Set(rows.filter((r) => r.corrects).map((r) => r.corrects));
  return rows.filter((r) => !corrected.has(r.row_id));
}

export function fold(rows) {
  const byUnit = new Map();
  for (const r of rows) {
    if (r.unit_id == null) continue;
    if (!byUnit.has(r.unit_id)) byUnit.set(r.unit_id, []);
    byUnit.get(r.unit_id).push(r);
  }
  const units = [];
  for (const [unit_id, rs] of byUnit) {
    rs.sort((a, b) => {
      const t = String(a.ts).localeCompare(String(b.ts));
      if (t !== 0) return t;
      const ai = EVENTS.indexOf(a.event); const bi = EVENTS.indexOf(b.event);
      return (ai < 0 ? 99 : ai) - (bi < 0 ? 99 : bi);
    });
    const kinds = new Set(rs.map((r) => r.event));
    let state = 'OPEN';
    if ([...kinds].some((k) => TERMINAL.has(k))) state = 'SEALED';
    else if (kinds.has('START')) state = 'IN-FLIGHT';
    else if (kinds.has('ENQUEUE')) state = 'QUEUED';

    // identity: ENQUEUE/START win; CLOSE fills only what they left null.
    const ident = {};
    for (const events of [['ENQUEUE', 'START'], ['CLOSE']]) {
      for (const r of rs) {
        if (!events.includes(r.event)) continue;
        for (const f of IDENTITY_FIELDS) {
          if (ident[f] == null && r[f] != null) ident[f] = r[f];
        }
      }
    }
    const close = rs.find((r) => r.event === 'CLOSE') || null;
    const start = rs.find((r) => r.event === 'START') || null;
    const duration = (start && close)
      ? (tsSeconds(close.ts) - tsSeconds(start.ts)) : null;
    units.push({ unit_id, rows: rs, state, ident, close, first_ts: rs[0].ts,
      last_ts: rs[rs.length - 1].ts, duration });
  }
  return units;
}

const ZERO_TOKENS = {
  input: 0, cached_input: 0, cache_write: 0, output: 0, reasoning: 0,
};

function addTokens(acc, close) {
  acc.input += close.tokens_input || 0;
  acc.cached_input += close.tokens_cached_input || 0;
  acc.cache_write += close.tokens_cache_write || 0;
  acc.output += close.tokens_output || 0;
  acc.reasoning += close.tokens_reasoning || 0;
}

/**
 * Cost accumulator with its DENOMINATOR carried (#63: unmeasured is not zero).
 * `cost_usd` is the v1.1 CLOSE-only optional field — vendor-REPORTED dollars, copied
 * verbatim. It is summed only over rows that carry it, and `n_cost` says how many did, so a
 * partial sum can never be read as a total.
 */
function costOf(closes) {
  const withCost = closes.filter((c) => c && c.cost_usd != null);
  return {
    cost_usd: withCost.reduce((n, c) => n + c.cost_usd, 0),
    n_cost: withCost.length,
  };
}

function bucket(closes, units) {
  const tokens = { ...ZERO_TOKENS };
  let n_tokens = 0;
  for (const c of closes) {
    if (!c) continue;
    if (c.tokens_input != null) n_tokens += 1;
    addTokens(tokens, c);
  }
  const rcs = closes.filter((c) => c && c.rc != null).map((c) => c.rc);
  const verdicts = {};
  for (const c of closes) {
    if (c && c.verdict) verdicts[c.verdict] = (verdicts[c.verdict] || 0) + 1;
  }
  const durations = units.map((u) => u.duration).filter((d) => d != null);
  return {
    units: units.length,
    tokens,
    n_tokens,
    rc_zero: rcs.filter((r) => r === 0).length,
    rc_total: rcs.length,
    verdicts,
    ...costOf(closes),
    median_wall_s: median(durations),
    currencies: [...new Set(closes.filter((c) => c && c.currency).map((c) => c.currency))].sort(),
  };
}

/**
 * Build the pre-aggregated `fleet` node. Returns null when there is no tape directory at all
 * (absence is never an error — Glance must not break on a repo without flight/).
 */
export function buildFleet(flightDir, { repoRelative = 'agentic_orchestration/flight' } = {}) {
  const tape = readTape(flightDir);
  if (!tape.present) return null;

  const raw = tape.rows;
  const rows = applyCorrections(raw);
  const units = fold(rows);
  const sealed = units.filter((u) => u.state === 'SEALED');

  // ---- per workstream (the run cost card, § 3.6-2)
  const wsMap = new Map();
  for (const u of sealed) {
    const key = u.ident.workstream || '(no workstream)';
    if (!wsMap.has(key)) wsMap.set(key, []);
    wsMap.get(key).push(u);
  }
  const curationByWs = new Map();
  for (const r of rows) {
    if (r.event !== 'CURATION') continue;
    const key = r.workstream || '(no workstream)';
    const cur = curationByWs.get(key) || { rows: 0, warns: 0 };
    cur.rows += 1;
    cur.warns += r.warn_count || 0;
    curationByWs.set(key, cur);
  }
  const workstreams = [...wsMap.entries()].map(([workstream, us]) => {
    const closes = us.map((u) => u.close);
    const firsts = us.map((u) => tsSeconds(u.first_ts)).filter((x) => x != null);
    const lasts = us.map((u) => tsSeconds(u.close ? u.close.ts : u.last_ts))
      .filter((x) => x != null);
    const cur = curationByWs.get(workstream) || { rows: 0, warns: 0 };
    return {
      workstream,
      ...bucket(closes, us),
      curation_rows: cur.rows,
      warns: cur.warns,
      first_ts: us.reduce((a, u) => (a && a < u.first_ts ? a : u.first_ts), null),
      last_ts: us.reduce((a, u) => (a && a > u.last_ts ? a : u.last_ts), null),
      // A RUN DURATION (first start → last close), NOT enqueue→seal: the founding corpus
      // records no ENQUEUE events, so enqueue→seal is not derivable for it.
      span_s: (firsts.length && lasts.length) ? Math.max(...lasts) - Math.min(...firsts) : null,
    };
  }).sort((a, b) => a.workstream.localeCompare(b.workstream));

  // ---- per (provider, pin) — the scorecard across time (§ 3.6-1)
  const SC_SEP = String.fromCharCode(0);   // same convention as parse.mjs COMMIT_FIELD_SEP
  const scMap = new Map();
  for (const u of sealed) {
    // The group key is joined on a byte that CANNOT occur inside a field: a pin may
    // legitimately contain a space (`model @ effort` spellings exist), and a separator
    // that can appear inside a field silently merges two models into one scorecard row.
    const key = `${u.ident.provider || '—'}${SC_SEP}${u.ident.pin || ''}`;
    if (!scMap.has(key)) scMap.set(key, []);
    scMap.get(key).push(u);
  }
  const scorecards = [...scMap.entries()].map(([key, us]) => {
    const [provider, pin] = key.split(SC_SEP);
    const closes = us.map((u) => u.close);
    return {
      provider,
      pin: pin || null,
      ...bucket(closes, us),
      artifacts: closes.reduce((n, c) => n + ((c && c.artifacts) ? c.artifacts.length : 0), 0),
    };
  }).sort((a, b) => (a.provider + a.pin).localeCompare(b.provider + b.pin));

  // ---- per vendor lane — AM-1 parity: both cards ALWAYS present, honest when empty
  const lanes = VENDOR_LANES.map(({ lane, provider, aliases }) => {
    const us = sealed.filter((u) => aliases.includes(u.ident.lane));
    const closes = us.map((u) => u.close).filter(Boolean);
    closes.sort((a, b) => String(a.ts).localeCompare(String(b.ts)));
    const last = closes.length ? closes[closes.length - 1] : null;
    const spellings = [...new Set(us.map((u) => u.ident.lane))].sort();
    return {
      lane,
      provider,
      on_tape: us.length > 0,
      spellings_seen: spellings,
      pins: [...new Set(us.map((u) => u.ident.pin).filter(Boolean))].sort(),
      ...bucket(closes, us),
      last_close: last ? {
        unit_id: last.unit_id, ts: last.ts,
        rc: last.rc == null ? null : last.rc,
        tokens_input: last.tokens_input == null ? null : last.tokens_input,
        tokens_output: last.tokens_output == null ? null : last.tokens_output,
        cost_usd: last.cost_usd == null ? null : last.cost_usd,
        workstream: last.workstream || null,
      } : null,
    };
  });
  // Claude lanes summarised — F-7 says their token fields are null by design, so they get a
  // count and an honest caption rather than a scorecard row pretending to depth.
  const claudeUnits = sealed.filter((u) => ['claude-agent', 'claude-subagent']
    .includes(u.ident.lane));
  const claude = {
    units: claudeUnits.length,
    closes: claudeUnits.filter((u) => u.close).length,
    with_tokens: claudeUnits.filter((u) => u.close && u.close.tokens_input != null).length,
  };

  // ---- month trend (the cost-over-time series; window-burn's coarse sibling)
  const monthMap = new Map();
  for (const u of sealed) {
    if (!u.close) continue;
    const m = String(u.close.ts).slice(0, 7);
    if (!monthMap.has(m)) monthMap.set(m, []);
    monthMap.get(m).push(u);
  }
  const months = [...monthMap.entries()].map(([month, us]) => ({
    month, ...bucket(us.map((u) => u.close), us),
  })).sort((a, b) => a.month.localeCompare(b.month));

  // ---- verdict history: GATE + CURATION + CLOSE verdicts, by filer. Verdicts enter rows
  // only from named gatekeepers (§ 7), so the filer is carried, never inferred.
  const verdictRows = rows
    .filter((r) => r.verdict && ['GATE', 'CURATION', 'CLOSE'].includes(r.event))
    .map((r) => ({
      ts: r.ts, event: r.event, unit_id: r.unit_id || null,
      workstream: r.workstream || null, verdict: r.verdict,
      gate_id: r.gate_id || null, gatekeeper: r.gatekeeper || null,
    }))
    .sort((a, b) => String(b.ts).localeCompare(String(a.ts)));
  const verdictTotals = {};
  for (const v of verdictRows) verdictTotals[v.verdict] = (verdictTotals[v.verdict] || 0) + 1;

  // ---- window meters: SNAPSHOT rows, meter vocabulary preserved RAW (§ 5)
  const snapshots = rows.filter((r) => r.event === 'SNAPSHOT')
    .map((r) => ({ ts: r.ts, currency: r.currency || null, meter_raw: r.meter_raw ?? null }))
    .sort((a, b) => String(b.ts).localeCompare(String(a.ts)));

  const tsAll = rows.map((r) => r.ts).filter(Boolean).sort();

  return {
    source: repoRelative,
    tape_files: tape.files,
    rows_on_disk: raw.length,
    rows_after_corrections: rows.length,
    unparseable_lines: tape.unparseable,
    schema_versions: [...new Set(rows.map((r) => r.v).filter((v) => v != null))].sort(),
    coverage: { first_ts: tsAll[0] || null, last_ts: tsAll[tsAll.length - 1] || null },
    // DENOMINATORS, not lanes. Glance shows no live state by construction (§ 12.4).
    units_total: units.length,
    units_sealed: sealed.length,
    workstreams,
    scorecards,
    lanes,
    claude,
    months,
    verdicts: { totals: verdictTotals, recent: verdictRows.slice(0, 40) },
    snapshots: snapshots.slice(0, 40),
  };
}
