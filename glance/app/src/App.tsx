import { useEffect, useMemo, useState, type ReactNode } from 'react';
import {
  type State, type Tracker, type TrackerId, type StatusToken, type QueueRow,
  TRACKER_LABEL, STATUS_LABEL, STATUS_SYMBOL, STATUS_COLOR,
  WATERMARK_KEY, maxDeltaDate, commitAge, githubLink,
} from './state';
import { InlineMd, BlockMd } from './md';
import { RowLine } from './components';

type View =
  | { kind: 'glance' }
  | { kind: 'drill'; tracker: TrackerId }
  | { kind: 'source'; tracker: TrackerId };

const COUNTER_ORDER: StatusToken[] = [
  'open', 'in_flight', 'blocked', 'awaiting_ruling', 'parked', 'closed',
];

export default function App() {
  const [state, setState] = useState<State | null>(null);
  const [err, setErr] = useState<string | null>(null);
  const [view, setView] = useState<View>({ kind: 'glance' });
  const [watermark, setWatermark] = useState<string | null>(null);

  useEffect(() => {
    fetch(`${import.meta.env.BASE_URL}state.json`, { cache: 'no-store' })
      .then((r) => {
        if (!r.ok) throw new Error(`state.json ${r.status}`);
        return r.json();
      })
      .then((s: State) => setState(s))
      .catch((e) => setErr(String(e)));
  }, []);

  // read watermark on mount
  useEffect(() => {
    try { setWatermark(localStorage.getItem(WATERMARK_KEY)); } catch { /* ignore */ }
  }, []);

  // advance watermark to the newest delta seen when the glance loads
  useEffect(() => {
    if (!state) return;
    const newest = maxDeltaDate(state.trackers);
    if (newest) {
      try {
        const prev = localStorage.getItem(WATERMARK_KEY);
        if (!prev || newest > prev) localStorage.setItem(WATERMARK_KEY, newest);
      } catch { /* ignore */ }
    }
  }, [state]);

  if (err) {
    return (
      <div className="mx-auto max-w-2xl p-8 text-rose-300">
        <h1 className="mb-2 text-xl font-semibold">Glance failed to load state</h1>
        <p className="text-sm text-slate-400">{err}</p>
        <p className="mt-4 text-sm text-slate-500">
          state.json is emitted by the parser at build time. If this is a preview
          with malformed rows, the parser still writes state — check the CI log.
        </p>
      </div>
    );
  }
  if (!state) {
    return <div className="p-8 text-slate-500">Loading canon…</div>;
  }

  const activeTracker =
    view.kind !== 'glance'
      ? state.trackers.find((t) => t.id === view.tracker)
      : undefined;

  return (
    <div className="min-h-full">
      <TopBar
        state={state}
        view={view}
        onHome={() => setView({ kind: 'glance' })}
      />
      <main className="mx-auto max-w-5xl px-3 pb-24 pt-4 sm:px-4">
        {view.kind === 'glance' && (
          <Glance
            state={state}
            watermark={watermark}
            onOpenTracker={(id) => setView({ kind: 'drill', tracker: id })}
          />
        )}
        {view.kind === 'drill' && activeTracker && (
          <Drill
            tracker={activeTracker}
            ghBase={state.gh_blob_base}
            onSource={() => setView({ kind: 'source', tracker: activeTracker.id })}
          />
        )}
        {view.kind === 'source' && activeTracker && (
          <Source tracker={activeTracker} ghBase={state.gh_blob_base} />
        )}
      </main>
      <Footer state={state} />
    </div>
  );
}

// ---------------------------------------------------------------------------
// Top bar + breadcrumb
// ---------------------------------------------------------------------------
function TopBar({ state, view, onHome }: { state: State; view: View; onHome: () => void }) {
  return (
    <header className="sticky top-0 z-10 border-b border-slate-800 bg-slate-950/90 backdrop-blur">
      <div className="mx-auto flex max-w-5xl items-center justify-between px-3 py-2 sm:px-4">
        <button onClick={onHome} className="flex items-center gap-2 text-left">
          <span className="text-lg font-bold tracking-tight text-slate-100">Glance</span>
          <span className="hidden text-xs text-slate-500 sm:inline">
            the true state, derived from canon
          </span>
        </button>
        <div className="flex items-center gap-3 text-xs text-slate-500">
          {view.kind !== 'glance' && (
            <button onClick={onHome} className="text-sky-400 hover:text-sky-300">← glance</button>
          )}
          <span title={state.generated_at}>
            built {commitAge(state.generated_at)}
          </span>
        </div>
      </div>
    </header>
  );
}

// ---------------------------------------------------------------------------
// TIER 0 — the glance
// ---------------------------------------------------------------------------
function Glance({
  state, watermark, onOpenTracker,
}: {
  state: State;
  watermark: string | null;
  onOpenTracker: (id: TrackerId) => void;
}) {
  const openDecisions = state.matt_decision_needed.filter((x) => !x.resolved);
  const openTodos = state.matt_to_do.filter((x) => !x.resolved);

  return (
    <div className="space-y-6">
      {/* header strip */}
      <section className="grid grid-cols-2 gap-2 sm:grid-cols-4">
        <PixelCard
          big
          value={openDecisions.length}
          label="Your move"
          sub="matt_decision_needed"
          tone={openDecisions.length > 0 ? 'urgent' : 'calm'}
          href={githubLink(state.gh_blob_base, 'canonical/matt_decision_needed/README.md', 1)}
        />
        <PixelCard
          value={openTodos.length}
          label="Matt to-do"
          sub="human-action queue"
          tone="neutral"
          href={githubLink(state.gh_blob_base, 'canonical/matt_to_do/README.md', 1)}
        />
        <PixelCard
          value={commitAge(state.last_commit.date)}
          label={state.last_commit.date_is_build_time_proxy ? 'Last build' : 'Last commit'}
          sub={state.last_commit.author ? `@${state.last_commit.author}` : '—'}
          tone="neutral"
          href={state.last_commit.sha ? `${state.gh_blob_base.replace('/blob/main', '')}/commit/${state.last_commit.sha}` : undefined}
        />
        <PixelCard
          value={state.dangling_gates.length}
          label="Dangling gates"
          sub="unresolved gates-on"
          tone={state.dangling_gates.length > 0 ? 'warn' : 'calm'}
        />
      </section>

      {/* four tracker cards */}
      <section className="grid grid-cols-1 gap-3 sm:grid-cols-2">
        {state.trackers.map((t) => (
          <TrackerCard key={t.id} tracker={t} onOpen={() => onOpenTracker(t.id)} />
        ))}
      </section>

      {/* since you last looked */}
      <SinceYouLastLooked state={state} watermark={watermark} onOpenTracker={onOpenTracker} />
    </div>
  );
}

function PixelCard({
  value, label, sub, tone, big, href,
}: {
  value: ReactNode;
  label: string;
  sub?: string;
  tone: 'urgent' | 'warn' | 'calm' | 'neutral';
  big?: boolean;
  href?: string;
}) {
  const toneRing =
    tone === 'urgent' ? 'ring-2 ring-rose-500/70 bg-rose-950/30'
    : tone === 'warn' ? 'ring-1 ring-amber-600/50 bg-amber-950/20'
    : tone === 'calm' ? 'ring-1 ring-emerald-700/40 bg-emerald-950/10'
    : 'ring-1 ring-slate-700/60 bg-slate-900/40';
  const inner = (
    <div className={`flex h-full flex-col justify-between rounded-lg p-3 ${toneRing}`}>
      <div className={`font-bold tabular-nums text-slate-100 ${big ? 'text-4xl' : 'text-2xl'}`}>
        {value}
      </div>
      <div className="mt-1">
        <div className="text-xs font-medium text-slate-300">{label}</div>
        {sub && <div className="text-[0.7rem] text-slate-500">{sub}</div>}
      </div>
    </div>
  );
  return href ? (
    <a href={href} target="_blank" rel="noreferrer" className="block">{inner}</a>
  ) : inner;
}

function TrackerCard({ tracker, onOpen }: { tracker: Tracker; onOpen: () => void }) {
  const latest = tracker.deltas[0];
  // top-3 open items = first three non-closed rows by board order
  const openRows: QueueRow[] = [];
  for (const q of tracker.queues) {
    for (const r of q.rows) {
      if (r.status.token !== 'closed') openRows.push(r);
      if (openRows.length >= 3) break;
    }
    if (openRows.length >= 3) break;
  }
  return (
    <button
      onClick={onOpen}
      className="flex flex-col rounded-lg border border-slate-800 bg-slate-900/50 p-3 text-left transition hover:border-slate-600 hover:bg-slate-900">
      <div className="flex items-center justify-between">
        <h2 className="font-semibold text-slate-100">{TRACKER_LABEL[tracker.id]}</h2>
        {tracker.status_banner?.stamp && (
          <span className="rounded bg-slate-800 px-1.5 py-0.5 text-[0.65rem] font-medium text-slate-400">
            {tracker.status_banner.stamp}
          </span>
        )}
      </div>
      {latest && (
        <div className="mt-1 text-xs text-slate-400">
          <span className="font-mono text-slate-500">{latest.date}</span>{' '}
          <span className="text-slate-300"><InlineMd src={latest.headline} /></span>
        </div>
      )}
      <div className="mt-2 flex flex-wrap gap-1.5">
        {COUNTER_ORDER.map((k) => {
          const n = tracker.counters[k];
          if (n === 0) return null;
          const c = STATUS_COLOR[k];
          return (
            <span key={k} className={`rounded border px-1.5 py-0.5 text-[0.7rem] ${c.chip}`}>
              {STATUS_SYMBOL[k]} {n}
            </span>
          );
        })}
      </div>
      {openRows.length > 0 && (
        <ul className="mt-2 space-y-0.5 text-xs text-slate-400">
          {openRows.map((r) => (
            <li key={r.id} className="truncate">
              <span className="font-mono text-slate-500">{r.id}</span>{' '}
              {r.cells_md.length > 1 ? r.cells_md[1].replace(/\*\*|`|~~/g, '').slice(0, 70) : ''}
            </li>
          ))}
        </ul>
      )}
      <span className="mt-2 text-[0.7rem] text-sky-500">drill in →</span>
    </button>
  );
}

function SinceYouLastLooked({
  state, watermark, onOpenTracker,
}: {
  state: State;
  watermark: string | null;
  onOpenTracker: (id: TrackerId) => void;
}) {
  // merge all deltas, newest first
  const merged = useMemo(() => {
    const all: { tracker: TrackerId; date: string; headline: string; line: number }[] = [];
    for (const t of state.trackers) {
      for (const d of t.deltas) {
        all.push({ tracker: t.id, date: d.date, headline: d.headline, line: d.line });
      }
    }
    all.sort((a, b) => (a.date < b.date ? 1 : a.date > b.date ? -1 : 0));
    return all.slice(0, 24);
  }, [state]);

  return (
    <section>
      <div className="mb-2 flex items-baseline justify-between">
        <h2 className="text-sm font-semibold text-slate-300">Since you last looked</h2>
        {watermark && (
          <span className="text-[0.7rem] text-slate-500">watermark {watermark}</span>
        )}
      </div>
      <ol className="space-y-1">
        {merged.map((d, i) => {
          const isNew = !watermark || d.date > watermark;
          return (
            <li
              key={i}
              className={`rounded border px-2 py-1.5 text-xs ${
                isNew
                  ? 'border-sky-700/60 bg-sky-950/30'
                  : 'border-slate-800 bg-slate-900/30'
              }`}>
              <div className="flex items-center gap-2">
                {isNew && <span className="rounded bg-sky-600 px-1 text-[0.6rem] font-bold text-white">NEW</span>}
                <span className="font-mono text-slate-500">{d.date}</span>
                <button
                  onClick={() => onOpenTracker(d.tracker)}
                  className="rounded bg-slate-800 px-1 text-[0.65rem] text-slate-400 hover:text-sky-300">
                  {TRACKER_LABEL[d.tracker]}
                </button>
              </div>
              <div className="mt-0.5 text-slate-300">
                <InlineMd src={d.headline} />
              </div>
            </li>
          );
        })}
      </ol>
    </section>
  );
}

// ---------------------------------------------------------------------------
// TIER 1 — the drill (queues + delta timeline + PART list under §4)
// ---------------------------------------------------------------------------
function Drill({
  tracker, ghBase, onSource,
}: { tracker: Tracker; ghBase: string; onSource: () => void }) {
  const [statusFilter, setStatusFilter] = useState<StatusToken | 'all'>('all');
  const [ownerFilter, setOwnerFilter] = useState<string | 'all'>('all');
  const [sortBy, setSortBy] = useState<'board' | 'status' | 'owner'>('board');

  const owners = useMemo(() => {
    const set = new Set<string>();
    for (const q of tracker.queues) for (const r of q.rows) if (r.owner) set.add(r.owner);
    return Array.from(set).sort();
  }, [tracker]);

  return (
    <div className="space-y-6">
      {/* §4 supersession law: STATUS banner → latest delta (full) → older (collapsed) → PARTs */}
      <div>
        <div className="flex flex-wrap items-center justify-between gap-2">
          <h1 className="text-xl font-bold text-slate-100">{TRACKER_LABEL[tracker.id]}</h1>
          <button onClick={onSource} className="text-xs text-sky-400 hover:text-sky-300">
            view source →
          </button>
        </div>
        {tracker.status_banner && (
          <a
            href={githubLink(ghBase, tracker.path, tracker.status_banner.line)}
            target="_blank" rel="noreferrer"
            className="mt-1 block rounded border border-slate-800 bg-slate-900/40 px-3 py-2 text-xs text-slate-400 hover:border-slate-600">
            <span className="font-semibold text-slate-300">{tracker.status_banner.stamp}</span>
            {tracker.status_banner.date && <span className="ml-2 font-mono">{tracker.status_banner.date}</span>}
            <div className="mt-1"><InlineMd src={tracker.status_banner.raw.replace(/^>\s*/, '')} /></div>
          </a>
        )}
      </div>

      {/* delta timeline: latest full, older collapsed */}
      <DeltaTimeline tracker={tracker} ghBase={ghBase} />

      {/* queues as sortable/filterable tables */}
      <section>
        <h2 className="mb-2 text-sm font-semibold text-slate-300">Queues</h2>
        <div className="mb-3 flex flex-wrap gap-2 text-xs">
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value as StatusToken | 'all')}
            className="rounded border border-slate-700 bg-slate-900 px-2 py-1 text-slate-300">
            <option value="all">all statuses</option>
            {COUNTER_ORDER.map((s) => <option key={s} value={s}>{STATUS_LABEL[s]}</option>)}
          </select>
          {owners.length > 0 && (
            <select
              value={ownerFilter}
              onChange={(e) => setOwnerFilter(e.target.value)}
              className="rounded border border-slate-700 bg-slate-900 px-2 py-1 text-slate-300">
              <option value="all">all owners</option>
              {owners.map((o) => <option key={o} value={o}>@{o}</option>)}
            </select>
          )}
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as 'board' | 'status' | 'owner')}
            className="rounded border border-slate-700 bg-slate-900 px-2 py-1 text-slate-300">
            <option value="board">sort: board order</option>
            <option value="status">sort: status</option>
            <option value="owner">sort: owner</option>
          </select>
        </div>

        {tracker.queues.map((q) => {
          let rows = q.rows.filter((r) =>
            (statusFilter === 'all' || r.status.token === statusFilter) &&
            (ownerFilter === 'all' || r.owner === ownerFilter)
          );
          if (sortBy === 'status') {
            rows = [...rows].sort((a, b) =>
              COUNTER_ORDER.indexOf(a.status.token) - COUNTER_ORDER.indexOf(b.status.token));
          } else if (sortBy === 'owner') {
            rows = [...rows].sort((a, b) => (a.owner || '~').localeCompare(b.owner || '~'));
          }
          if (rows.length === 0) return null;
          return (
            <div key={q.line} className="mb-4 rounded-lg border border-slate-800 bg-slate-900/30 p-3">
              <a
                href={githubLink(ghBase, tracker.path, q.line)}
                target="_blank" rel="noreferrer"
                className="text-sm font-semibold text-slate-200 hover:text-sky-300">
                {q.title}
              </a>
              <div className="mt-1">
                {rows.map((r) => (
                  <RowLine key={r.id + r.line} row={r} ghBase={ghBase} path={tracker.path} />
                ))}
              </div>
            </div>
          );
        })}
      </section>
    </div>
  );
}

function DeltaTimeline({ tracker, ghBase }: { tracker: Tracker; ghBase: string }) {
  const [showAll, setShowAll] = useState(false);
  if (tracker.deltas.length === 0) return null;
  const [latest, ...older] = tracker.deltas;
  return (
    <section>
      <h2 className="mb-2 text-sm font-semibold text-slate-300">
        Delta timeline <span className="font-normal text-slate-500">(latest governs)</span>
      </h2>
      <div className="rounded-lg border border-sky-800/50 bg-sky-950/20 p-3">
        <a
          href={githubLink(ghBase, tracker.path, latest.line)}
          target="_blank" rel="noreferrer"
          className="text-xs font-mono text-sky-400 hover:text-sky-300">
          {latest.date} · L{latest.line}
        </a>
        <div className="mt-1 font-semibold text-slate-100">
          <InlineMd src={latest.headline} />
        </div>
        <div className="mt-2 text-sm text-slate-300">
          <BlockMd src={latest.body_md} />
        </div>
      </div>

      {older.length > 0 && (
        <div className="mt-2">
          <button
            onClick={() => setShowAll((s) => !s)}
            className="text-xs text-slate-400 hover:text-slate-200">
            {showAll ? '▾' : '▸'} {older.length} older delta{older.length > 1 ? 's' : ''}
          </button>
          {showAll && (
            <ol className="mt-2 space-y-2">
              {older.map((d) => (
                <li key={d.line} className="rounded border border-slate-800 bg-slate-900/30 p-2">
                  <a
                    href={githubLink(ghBase, tracker.path, d.line)}
                    target="_blank" rel="noreferrer"
                    className="text-xs font-mono text-slate-500 hover:text-sky-300">
                    {d.date} · L{d.line}
                  </a>
                  <div className="mt-0.5 text-sm text-slate-300">
                    <InlineMd src={d.headline} />
                  </div>
                </li>
              ))}
            </ol>
          )}
        </div>
      )}
    </section>
  );
}

// ---------------------------------------------------------------------------
// TIER 2 — the source (full modeled render + deep links + client search)
// ---------------------------------------------------------------------------
function Source({ tracker, ghBase }: { tracker: Tracker; ghBase: string }) {
  const [q, setQ] = useState('');
  const needle = q.trim().toLowerCase();

  const match = (s: string) => !needle || s.toLowerCase().includes(needle);

  return (
    <div className="space-y-5">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <h1 className="text-xl font-bold text-slate-100">
          {TRACKER_LABEL[tracker.id]} <span className="text-sm font-normal text-slate-500">source</span>
        </h1>
        <a
          href={githubLink(ghBase, tracker.path, 1)}
          target="_blank" rel="noreferrer"
          className="text-xs text-sky-400 hover:text-sky-300">
          open raw on GitHub ↗
        </a>
      </div>
      <input
        type="search"
        value={q}
        onChange={(e) => setQ(e.target.value)}
        placeholder="search this tracker…"
        className="w-full rounded border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-slate-200 placeholder:text-slate-500"
      />

      {/* every modeled claim deep-links to file+line */}
      <section>
        <h2 className="mb-1 text-sm font-semibold text-slate-300">Deltas</h2>
        {tracker.deltas.filter((d) => match(d.headline) || match(d.body_md)).map((d) => (
          <div key={d.line} className="mb-3 border-l-2 border-slate-700 pl-3">
            <a href={githubLink(ghBase, tracker.path, d.line)} target="_blank" rel="noreferrer"
               className="font-mono text-xs text-sky-400 hover:text-sky-300">
              {d.date} · L{d.line}
            </a>
            <div className="font-semibold text-slate-100"><InlineMd src={d.headline} /></div>
            <div className="mt-1 text-sm text-slate-300"><BlockMd src={d.body_md} /></div>
          </div>
        ))}
      </section>

      <section>
        <h2 className="mb-1 text-sm font-semibold text-slate-300">Queue rows</h2>
        {tracker.queues.map((qq) => {
          const rows = qq.rows.filter((r) => match(r.cells_md.join(' ')) || match(r.id));
          if (rows.length === 0) return null;
          return (
            <div key={qq.line} className="mb-3">
              <a href={githubLink(ghBase, tracker.path, qq.line)} target="_blank" rel="noreferrer"
                 className="text-xs font-semibold text-slate-300 hover:text-sky-300">
                {qq.title}
              </a>
              {rows.map((r) => <RowLine key={r.id + r.line} row={r} ghBase={ghBase} path={tracker.path} />)}
            </div>
          );
        })}
      </section>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Footer — provenance + CC-BY note seam
// ---------------------------------------------------------------------------
function Footer({ state }: { state: State }) {
  return (
    <footer className="border-t border-slate-800 px-4 py-6 text-center text-[0.7rem] text-slate-600">
      <div>
        Glance — derived from canon, authored by no one.{' '}
        <span className="font-mono">{state.repo_sha?.slice(0, 7) ?? '—'}</span>
      </div>
      <div className="mt-1">
        No DB · no server · no LLM in the truth path. Parser reads canonical/** only.
      </div>
    </footer>
  );
}
