// Fleet — the U-1 flight-recorder REAR-VIEW (`#/fleet`).
//
// Spec: gandalf/notes/2026-08-24-fleet-flightrecorder-board-spec-DRAFT.md §12.4 (Matt
// 2026-08-24, verbatim: "stage it in") + §13 AM-1 (vendor lane parity, grok alongside codex).
//
// TWO WINDOWS, ONE TAPE:
//   local board (agentic_orchestration/factory/ui/board.py) = the WINDSHIELD — live lanes,
//     auth, unpushed commits, staleness. Minute-fresh, Mac-local, pre-push.
//   this page                                              = the REAR-VIEW MIRROR — history.
//     Per-workstream cost, per-model scorecards, per-lane rollups, verdict + window-meter
//     history. History does not stale, so a push-fresh render of it is honest.
//
// WHAT IS DELIBERATELY ABSENT, AND WHY: no IN-FLIGHT list, no lane liveness, no HEALTH.
// A Vercel build can only ever see PUSHED state; rendering "codex lane: open" from a tape
// snapshot would be a green pixel over an unknown exit code — the named ancestor bug. Those
// facts are structurally local and stay on the local board.
//
// THE LAW (U-1 / Discipline #74) as it binds this page: it is a VIEW. Zero authority, zero
// write verbs, never in the data path, no LLM anywhere, honest nulls, one data path (the
// same committed tape the local board folds). Nobody rules from this page.

import type {
  Fleet, FleetBucket, FleetLane, FleetMonth, FleetScorecard, FleetWorkstream,
} from '../state';
import { cacheRate, fmtSpan, fmtTokens } from '../state';

// ---------------------------------------------------------------------------
// honest-null primitives — a declared null is a fact; a zero in its place is a lie
// ---------------------------------------------------------------------------
function Null({ children }: { children: React.ReactNode }) {
  return <span className="italic text-slate-500">— {children}</span>;
}

function Denom({ n, of, unit }: { n: number; of: number; unit: string }) {
  return (
    <span className="text-[0.65rem] text-slate-500">
      {' '}({n}/{of} {unit})
    </span>
  );
}

function TokenCell({ b }: { b: FleetBucket }) {
  if (!b.n_tokens) return <Null>tokens null on {b.units}/{b.units} units</Null>;
  const rate = cacheRate(b.tokens);
  return (
    <span className="tabular-nums">
      {fmtTokens(b.tokens.input)} in
      <Denom n={b.n_tokens} of={b.units} unit="units" />
      {rate != null && <> · <span className="text-emerald-400">{rate.toFixed(1)}% cache</span></>}
      {' '}· {fmtTokens(b.tokens.output)} out
    </span>
  );
}

function CostCell({ b }: { b: FleetBucket }) {
  // v1.1 `cost_usd` is CLOSE-only and optional. Vendors that do not report dollars leave it
  // absent, and absent is stated — never summed as zero (#63: unmeasured is not zero).
  if (!b.n_cost) return <Null>no vendor-reported cost on these rows</Null>;
  return (
    <span className="tabular-nums text-amber-300">
      ${b.cost_usd.toFixed(5)}
      <Denom n={b.n_cost} of={b.units} unit="rows report one" />
    </span>
  );
}

function RcCell({ b }: { b: FleetBucket }) {
  if (!b.rc_total) return <Null>no exit code recorded</Null>;
  return (
    <span className="tabular-nums">
      {b.rc_zero}/{b.rc_total} rc=0
    </span>
  );
}

function Card({ title, sub, children }: {
  title: string; sub?: React.ReactNode; children: React.ReactNode;
}) {
  return (
    <section className="mb-4 rounded border border-slate-800 bg-slate-900/60">
      <header className="border-b border-slate-800 px-3 py-2">
        <h2 className="text-sm font-semibold text-slate-200">{title}</h2>
        {sub && <div className="mt-0.5 text-[0.7rem] leading-snug text-slate-500">{sub}</div>}
      </header>
      <div className="p-3">{children}</div>
    </section>
  );
}

/** Phone-first table: horizontally scrollable rather than squeezed or truncated. */
function Scroll({ children }: { children: React.ReactNode }) {
  return <div className="-mx-3 overflow-x-auto px-3">{children}</div>;
}

const TH = 'whitespace-nowrap border-b border-slate-800 px-2 py-1 text-left font-medium text-slate-400';
const TD = 'whitespace-nowrap border-b border-slate-900 px-2 py-1 align-top text-slate-300';

// ---------------------------------------------------------------------------
export function FleetPage({ fleet }: { fleet: Fleet | null }) {
  if (!fleet) {
    return (
      <Card
        title="Fleet — no flight recorder in this repo"
        sub="ABSENCE IS NEVER AN ERROR (parse contract §7.6)."
      >
        <p className="text-sm text-slate-400">
          No <code>agentic_orchestration/flight/</code> directory was present at the last
          push, so there is no tape to fold. This page renders the moment one exists.
        </p>
      </Card>
    );
  }

  const empty = fleet.rows_on_disk === 0;

  return (
    <div>
      <Card
        title="FLEET — rear-view mirror"
        sub={
          <>
            <span className="rounded border border-slate-700 px-1 text-[0.6rem] tracking-wider text-slate-400">
              SHOP-ONLY
            </span>{' '}
            <span className="rounded border border-slate-700 px-1 text-[0.6rem] tracking-wider text-slate-400">
              VIEW ONLY
            </span>{' '}
            history folded from <code>{fleet.source}/records-*.jsonl</code> —{' '}
            {fleet.tape_files.length ? fleet.tape_files.join(', ') : 'no monthly tape yet'} ·{' '}
            {fleet.rows_on_disk} rows on disk, {fleet.rows_after_corrections} after
            corrections{' '}
            {fleet.unparseable_lines > 0 && (
              <span className="text-rose-400">
                · {fleet.unparseable_lines} unparseable line(s)
              </span>
            )}
            {fleet.schema_versions.length > 0 && (
              <> · rows stamped v{fleet.schema_versions.join('/')}</>
            )}
          </>
        }
      >
        <p className="text-xs leading-relaxed text-slate-400">
          <b className="text-slate-300">This is the rear-view mirror, not the windshield.</b>{' '}
          Everything here is HISTORY, folded from the tape as of the last push. Live lanes,
          auth health, unpushed commits and staleness are <i>structurally</i> invisible to a
          static build and live on the local fleet board instead
          (<code>agentic_orchestration/factory/ui/board.py</code>). Nothing on this page is
          authority: rule from the ledgers, dispatches and queues.
        </p>
        <p className="mt-2 text-xs leading-relaxed text-slate-500">
          <b>COVERAGE:</b>{' '}
          {fleet.coverage.first_ts
            ? <>the tape begins {fleet.coverage.first_ts} and ends {fleet.coverage.last_ts}. Every
              unit that ran before the recorder existed is invisible here — a count is a count of
              RECORDED units, never a census of the fleet.</>
            : <>the tape carries no rows yet, so every rollup below is empty by fact, not by
              filter.</>}{' '}
          Denominators: <b className="tabular-nums text-slate-400">{fleet.units_sealed}</b> sealed
          of <b className="tabular-nums text-slate-400">{fleet.units_total}</b> units on tape
          (denominators for the rollups — <i>not</i> lanes; this page renders no live state).
        </p>
      </Card>

      {empty && (
        <Card title="No rows on the tape yet" sub="An empty recorder is a fact, not a failure.">
          <p className="text-sm text-slate-400">
            The recorder is installed and has recorded nothing. Every card below stays empty
            and honest until a lane appends its first row.
          </p>
        </Card>
      )}

      <LaneCards lanes={fleet.lanes} claude={fleet.claude} />
      <WorkstreamCard rows={fleet.workstreams} />
      <ScorecardCard rows={fleet.scorecards} />
      <MonthCard rows={fleet.months} />
      <VerdictCard verdicts={fleet.verdicts} />
      <SnapshotCard snapshots={fleet.snapshots} />
    </div>
  );
}

// ---------------------------------------------------------------------------
// Vendor lanes — AM-1 parity: grok renders wherever codex does, and says
// "no rows on tape" honestly rather than vanishing when it has done nothing yet.
// ---------------------------------------------------------------------------
function LaneCards({ lanes, claude }: {
  lanes: FleetLane[]; claude: { units: number; closes: number; with_tokens: number };
}) {
  return (
    <Card
      title="Vendor lanes — historical rollup per lane"
      sub={
        <>
          One card per vendor lane, always rendered (AM-1 §13.1 parity). This is what the lane
          HAS DONE. What the lane is doing RIGHT NOW is a local-only fact: the busy check is
          the truth and the local board renders it.
        </>
      }
    >
      <div className="grid gap-3 sm:grid-cols-2">
        {lanes.map((l) => (
          <div key={l.lane} className="rounded border border-slate-800 bg-slate-950/50 p-2">
            <div className="flex items-baseline justify-between gap-2">
              <h3 className="text-xs font-semibold text-slate-200">
                <code>{l.lane}</code>{' '}
                <span className="font-normal text-slate-500">· {l.provider}</span>
              </h3>
              <span
                className={`rounded px-1.5 py-0.5 text-[0.6rem] ${
                  l.on_tape ? 'bg-slate-800 text-slate-300' : 'bg-slate-900 text-slate-500'
                }`}
              >
                {l.on_tape ? `${l.units} sealed unit(s)` : 'no rows on tape'}
              </span>
            </div>
            {!l.on_tape ? (
              <p className="mt-1 text-[0.7rem] leading-snug text-slate-500">
                This lane exists in the fleet's vocabulary and has recorded nothing yet. That is
                a different fact from "this lane does not exist", and it is rendered as such.
              </p>
            ) : (
              <dl className="mt-1.5 grid grid-cols-[5.5rem_1fr] gap-x-2 gap-y-1 text-[0.7rem]">
                <dt className="text-slate-500">rc</dt>
                <dd><RcCell b={l} /></dd>
                <dt className="text-slate-500">tokens</dt>
                <dd><TokenCell b={l} /></dd>
                <dt className="text-slate-500">reported cost</dt>
                <dd><CostCell b={l} /></dd>
                <dt className="text-slate-500">median wall</dt>
                <dd>{l.median_wall_s != null ? fmtSpan(l.median_wall_s)
                  : <Null>no START→CLOSE pair on this lane</Null>}</dd>
                <dt className="text-slate-500">pin</dt>
                <dd>{l.pins.length ? <code>{l.pins.join(', ')}</code>
                  : <Null>no row on this lane carries a pin</Null>}</dd>
                <dt className="text-slate-500">currency</dt>
                <dd>{l.currencies.length ? l.currencies.join(' / ')
                  : <Null>none recorded</Null>}</dd>
                <dt className="text-slate-500">last close</dt>
                <dd>
                  {l.last_close ? (
                    <span className="break-all">
                      <code>{l.last_close.unit_id}</code>
                      <span className="text-slate-500"> · {l.last_close.ts}</span>
                      {l.last_close.cost_usd != null && (
                        <span className="text-amber-300"> · ${l.last_close.cost_usd.toFixed(5)}</span>
                      )}
                    </span>
                  ) : <Null>no CLOSE row</Null>}
                </dd>
                {l.spellings_seen.length > 1 && (
                  <>
                    <dt className="text-slate-500">spellings</dt>
                    <dd className="text-slate-400">
                      {l.spellings_seen.join(', ')}{' '}
                      <span className="text-slate-500">
                        (v1 <code>grok-judge</code> and v1.1 <code>grok-serial</code> are the
                        same stream and fold onto one card)
                      </span>
                    </dd>
                  </>
                )}
              </dl>
            )}
          </div>
        ))}

        <div className="rounded border border-slate-800 bg-slate-950/50 p-2">
          <h3 className="text-xs font-semibold text-slate-200">
            claude lanes <span className="font-normal text-slate-500">· summarised</span>
          </h3>
          <dl className="mt-1.5 grid grid-cols-[5.5rem_1fr] gap-x-2 gap-y-1 text-[0.7rem]">
            <dt className="text-slate-500">sealed units</dt>
            <dd className="tabular-nums">{claude.units} ({claude.closes} CLOSE)</dd>
            <dt className="text-slate-500">tokens</dt>
            <dd>
              {claude.with_tokens > 0
                ? <span className="tabular-nums">{claude.with_tokens} unit(s) report tokens</span>
                : <Null>
                    F-7: interactive sessions surface no per-turn usage, so token fields stay
                    null until hooks + SNAPSHOT brackets deepen. A null is a fact; an estimate
                    in a truth-of-record stream is a fabrication
                  </Null>}
            </dd>
          </dl>
        </div>
      </div>
    </Card>
  );
}

// ---------------------------------------------------------------------------
function WorkstreamCard({ rows }: { rows: FleetWorkstream[] }) {
  return (
    <Card
      title="Run cost card — per workstream"
      sub={<>What each run cost, in each currency. <code>span</code> is first-start →
        last-close, a RUN DURATION — not enqueue→seal, which the founding corpus cannot
        derive (it records no ENQUEUE events).</>}
    >
      {!rows.length ? (
        <p className="text-sm"><Null>no sealed unit on the tape yet</Null></p>
      ) : (
        <Scroll>
          <table className="w-full text-[0.7rem]">
            <thead>
              <tr>
                <th className={TH}>workstream</th>
                <th className={TH}>units</th>
                <th className={TH}>rc</th>
                <th className={TH}>curation</th>
                <th className={TH}>tokens</th>
                <th className={TH}>reported cost</th>
                <th className={TH}>currency</th>
                <th className={TH}>span</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((r) => (
                <tr key={r.workstream}>
                  <td className={TD}><b className="text-slate-200">{r.workstream}</b></td>
                  <td className={`${TD} tabular-nums`}>{r.units}</td>
                  <td className={TD}><RcCell b={r} /></td>
                  <td className={TD}>
                    {r.curation_rows
                      ? <span className="tabular-nums">{r.warns} WARN / {r.curation_rows} row(s)</span>
                      : <Null>no curation row</Null>}
                  </td>
                  <td className={TD}><TokenCell b={r} /></td>
                  <td className={TD}><CostCell b={r} /></td>
                  <td className={TD}>{r.currencies.join(' / ') || <Null>none</Null>}</td>
                  <td className={`${TD} tabular-nums`}>{fmtSpan(r.span_s)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </Scroll>
      )}
    </Card>
  );
}

// ---------------------------------------------------------------------------
function ScorecardCard({ rows }: { rows: FleetScorecard[] }) {
  return (
    <Card
      title="Per-model scorecard — one row per (provider, pin)"
      sub={<>The U-4 A/B template as a query: every banked lane statistic is measured AT A
        PIN, so the pin is the row key. WARN / fabrication-check columns are omitted rather
        than zero-filled — a CURATION row binds to a unit, so a per-model WARN rate is
        derivable only when the curated unit is itself a lane unit.</>}
    >
      {!rows.length ? (
        <p className="text-sm"><Null>no sealed unit to score</Null></p>
      ) : (
        <Scroll>
          <table className="w-full text-[0.7rem]">
            <thead>
              <tr>
                <th className={TH}>provider / pin</th>
                <th className={TH}>units</th>
                <th className={TH}>first-pass</th>
                <th className={TH}>tokens</th>
                <th className={TH}>tok-in / artifact</th>
                <th className={TH}>reported cost</th>
                <th className={TH}>median wall</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((r) => (
                <tr key={`${r.provider}/${r.pin ?? ''}`}>
                  <td className={TD}>
                    <b className="text-slate-200">{r.provider}</b>
                    {' / '}
                    {r.pin ? <code>{r.pin}</code> : <Null>no pin recorded</Null>}
                  </td>
                  <td className={`${TD} tabular-nums`}>{r.units}</td>
                  <td className={TD}>
                    {r.rc_total
                      ? <span className="tabular-nums">
                          {Math.round((100 * r.rc_zero) / r.rc_total)}% ({r.rc_zero}/{r.rc_total} rc=0)
                        </span>
                      : <Null>no exit code recorded</Null>}
                  </td>
                  <td className={TD}><TokenCell b={r} /></td>
                  <td className={TD}>
                    {r.n_tokens && r.artifacts
                      ? <span className="tabular-nums">
                          {fmtTokens(Math.round(r.tokens.input / r.artifacts))}
                        </span>
                      : <Null>no artifact rows</Null>}
                  </td>
                  <td className={TD}><CostCell b={r} /></td>
                  <td className={`${TD} tabular-nums`}>
                    {r.median_wall_s != null ? fmtSpan(r.median_wall_s)
                      : <Null>no START→CLOSE pair</Null>}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </Scroll>
      )}
    </Card>
  );
}

// ---------------------------------------------------------------------------
function MonthCard({ rows }: { rows: FleetMonth[] }) {
  return (
    <Card
      title="Cost trend — by month of close"
      sub="The series that answers 'is this getting cheaper or more expensive over time'. One
           month is not a trend; it is the first point of one."
    >
      {!rows.length ? (
        <p className="text-sm"><Null>no closed unit on the tape yet</Null></p>
      ) : (
        <Scroll>
          <table className="w-full text-[0.7rem]">
            <thead>
              <tr>
                <th className={TH}>month</th>
                <th className={TH}>units</th>
                <th className={TH}>tokens</th>
                <th className={TH}>reported cost</th>
                <th className={TH}>currencies</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((m) => (
                <tr key={m.month}>
                  <td className={TD}><b className="text-slate-200">{m.month}</b></td>
                  <td className={`${TD} tabular-nums`}>{m.units}</td>
                  <td className={TD}><TokenCell b={m} /></td>
                  <td className={TD}><CostCell b={m} /></td>
                  <td className={TD}>{m.currencies.join(' / ') || <Null>none</Null>}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </Scroll>
      )}
    </Card>
  );
}

// ---------------------------------------------------------------------------
function VerdictCard({ verdicts }: {
  verdicts: { totals: Record<string, number>; recent: Fleet['verdicts']['recent'] };
}) {
  const totals = Object.entries(verdicts.totals).sort((a, b) => b[1] - a[1]);
  return (
    <Card
      title="Verdict history"
      sub={<>Verdicts enter the tape only from NAMED gatekeepers and curators (GATE / CURATION
        rows) — never from the executing lane's self-assessment. The filer is carried, never
        inferred.</>}
    >
      {!totals.length ? (
        <p className="text-sm"><Null>no verdict on the tape yet</Null></p>
      ) : (
        <>
          <div className="mb-2 flex flex-wrap gap-1">
            {totals.map(([v, n]) => (
              <span key={v} className="rounded bg-slate-800 px-1.5 py-0.5 text-[0.65rem] text-slate-300">
                {v} <span className="font-semibold tabular-nums">{n}</span>
              </span>
            ))}
          </div>
          <Scroll>
            <table className="w-full text-[0.7rem]">
              <thead>
                <tr>
                  <th className={TH}>when</th>
                  <th className={TH}>event</th>
                  <th className={TH}>unit</th>
                  <th className={TH}>verdict</th>
                  <th className={TH}>gate / gatekeeper</th>
                </tr>
              </thead>
              <tbody>
                {verdicts.recent.map((r, i) => (
                  <tr key={`${r.ts}-${i}`}>
                    <td className={`${TD} tabular-nums`}>{r.ts}</td>
                    <td className={TD}>{r.event}</td>
                    <td className={TD}><code className="break-all">{r.unit_id ?? '—'}</code></td>
                    <td className={TD}><b className="text-slate-200">{r.verdict}</b></td>
                    <td className={TD}>
                      {r.gate_id ?? <Null>no gate id</Null>}
                      {r.gatekeeper && <span className="text-slate-500"> · {r.gatekeeper}</span>}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </Scroll>
        </>
      )}
    </Card>
  );
}

// ---------------------------------------------------------------------------
function SnapshotCard({ snapshots }: { snapshots: Fleet['snapshots'] }) {
  return (
    <Card
      title="Window-meter history"
      sub={<>SNAPSHOT rows: the subscription meters as the meters themselves reported them.
        The recorder MEASURES windows, it does not model them — so the vocabulary below is the
        vendor's, preserved raw.</>}
    >
      {!snapshots.length ? (
        <p className="text-sm">
          <Null>
            no SNAPSHOT row on the tape — window burn is not derivable yet, which is a gap in
            capture, not a reading of zero
          </Null>
        </p>
      ) : (
        <Scroll>
          <table className="w-full text-[0.7rem]">
            <thead>
              <tr>
                <th className={TH}>when</th>
                <th className={TH}>currency</th>
                <th className={TH}>meter (raw)</th>
              </tr>
            </thead>
            <tbody>
              {snapshots.map((s, i) => (
                <tr key={`${s.ts}-${i}`}>
                  <td className={`${TD} tabular-nums`}>{s.ts}</td>
                  <td className={TD}>{s.currency ?? <Null>none</Null>}</td>
                  <td className={`${TD} break-all`}>
                    <code>{JSON.stringify(s.meter_raw)}</code>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </Scroll>
      )}
    </Card>
  );
}
