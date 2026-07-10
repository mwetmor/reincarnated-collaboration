import { useEffect, useMemo, useState, type ReactNode } from 'react';
import {
  type State, type Tracker, type TrackerId, type StatusToken, type QueueRow,
  type Queue, type FlowStage, type PageId,
  TRACKER_LABEL, STATUS_LABEL, STATUS_SYMBOL, STATUS_COLOR,
  FLOW_SEGMENT_COLOR, FLOW_DOMINANT_LABEL,
  PAGE_ORDER, PAGE_LABEL, PAGE_TRACKER,
  WATERMARK_KEY, maxDeltaDate, commitAge, githubLink, counterTotal,
} from './state';
import { InlineMd, BlockMd } from './md';
import { RowLine } from './components';

// ---------------------------------------------------------------------------
// Routing — hash-based, zero dependency (§7.4). The SPA rewrite in vercel.json
// already funnels every path to index.html, so hash routes work identically in
// preview + prod with no 404 risk (the May-12 lesson). Routes (v1.5 — five pages):
//   #/                     → the slim six-card landing index (the original glance)
//   #/engine #/story #/game #/content-emission #/kits  → the five domain pages
// ---------------------------------------------------------------------------
type Route = { kind: 'landing' } | { kind: 'page'; page: PageId };

function parseHash(): Route {
  const h = window.location.hash.replace(/^#\/?/, '').trim();
  const p = PAGE_ORDER.find((x) => x === h);
  return p ? { kind: 'page', page: p } : { kind: 'landing' };
}

function useRoute(): Route {
  const [route, setRoute] = useState<Route>(() => parseHash());
  useEffect(() => {
    const on = () => setRoute(parseHash());
    window.addEventListener('hashchange', on);
    return () => window.removeEventListener('hashchange', on);
  }, []);
  return route;
}

function go(page: PageId | null) {
  window.location.hash = page ? `#/${page}` : '#/';
}

const COUNTER_ORDER: StatusToken[] = [
  'open', 'in_flight', 'blocked', 'awaiting_ruling', 'parked', 'closed',
];

export default function App() {
  const [state, setState] = useState<State | null>(null);
  const [err, setErr] = useState<string | null>(null);
  const [watermark, setWatermark] = useState<string | null>(null);
  const route = useRoute();

  useEffect(() => {
    fetch(`${import.meta.env.BASE_URL}state.json`, { cache: 'no-store' })
      .then((r) => {
        if (!r.ok) throw new Error(`state.json ${r.status}`);
        return r.json();
      })
      .then((s: State) => setState(s))
      .catch((e) => setErr(String(e)));
  }, []);

  useEffect(() => {
    try { setWatermark(localStorage.getItem(WATERMARK_KEY)); } catch { /* ignore */ }
  }, []);

  // advance the watermark to the newest delta seen on any load
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

  return (
    <div className="min-h-full">
      {/* the global header strip + five-tab nav ride on EVERY page (§7.4.1 — the
          one-screen glance survives the split). */}
      <HeaderStrip state={state} route={route} />
      <main className="mx-auto max-w-5xl px-3 pb-24 pt-4 sm:px-4">
        {route.kind === 'landing' ? (
          <Landing state={state} watermark={watermark} />
        ) : (
          <DomainPage state={state} page={route.page} />
        )}
      </main>
      <Footer state={state} />
    </div>
  );
}

// ---------------------------------------------------------------------------
// Global header strip — the your-move number + counters + five-tab nav + the
// surface-ledger drawer. Present on landing AND every domain page (§7.4.1).
// ---------------------------------------------------------------------------
function HeaderStrip({ state, route }: { state: State; route: Route }) {
  const [ledgerOpen, setLedgerOpen] = useState(false);
  const openDecisions = state.matt_decision_needed.filter((x) => !x.resolved);
  const openTodos = state.matt_to_do.filter((x) => !x.resolved);
  const sa = state.surfaces_agreed;
  const gateClosed = sa != null && sa.total > 0 && sa.agreed === sa.total;
  const ledger = state.trackers.find((t) => t.id === 'surface-ledger');
  const activePage = route.kind === 'page' ? route.page : null;

  return (
    <header className="sticky top-0 z-20 border-b border-slate-800 bg-slate-950/95 backdrop-blur">
      <div className="mx-auto max-w-5xl px-3 py-2 sm:px-4">
        {/* title row */}
        <div className="flex items-center justify-between">
          <button onClick={() => go(null)} className="flex items-baseline gap-2 text-left">
            <span className="text-lg font-bold tracking-tight text-slate-100">Glance</span>
            <span className="hidden text-xs text-slate-500 sm:inline">
              the true state, derived from canon
            </span>
          </button>
          <span className="text-[0.7rem] text-slate-500" title={state.generated_at}>
            built {commitAge(state.generated_at)}
          </span>
        </div>

        {/* the pixel strip — always visible; the your-move number never drops (§7.3 refutation) */}
        <div className="mt-2 grid grid-cols-3 gap-1.5 sm:grid-cols-5">
          <PixelCell
            big
            value={openDecisions.length}
            label="Your move"
            sub="matt_decision_needed"
            tone={openDecisions.length > 0 ? 'urgent' : 'calm'}
            href={githubLink(state.gh_blob_base, 'canonical/matt_decision_needed/README.md', 1)}
          />
          <PixelCell
            value={openTodos.length}
            label="Matt to-do"
            sub="human-action queue"
            tone="neutral"
            href={githubLink(state.gh_blob_base, 'canonical/matt_to_do/README.md', 1)}
          />
          {sa != null && (
            <PixelCell
              value={`✓${sa.agreed} / ${sa.total}`}
              label="Surfaces agreed"
              sub={gateClosed ? 'GATE1 closes' : 'demo gate (GATE1)'}
              tone={gateClosed ? 'calm' : 'warn'}
              onClick={() => setLedgerOpen((v) => !v)}
            />
          )}
          <PixelCell
            value={commitAge(state.last_commit.date)}
            label={state.last_commit.date_is_build_time_proxy ? 'Last build' : 'Last commit'}
            sub={state.last_commit.author ? `@${state.last_commit.author}` : '—'}
            tone="neutral"
            href={state.last_commit.sha ? `${state.gh_blob_base.replace('/blob/main', '')}/commit/${state.last_commit.sha}` : undefined}
          />
          <PixelCell
            value={state.dangling_gates.length + state.dangling_flow_refs.length}
            label="Dangling"
            sub="gates + flow-refs"
            tone={state.dangling_gates.length + state.dangling_flow_refs.length > 0 ? 'warn' : 'calm'}
          />
        </div>

        {/* five-tab nav */}
        <nav className="mt-2 flex flex-wrap items-center gap-1 text-xs">
          <TabButton label="Overview" active={activePage === null} onClick={() => go(null)} />
          {PAGE_ORDER.map((p) => (
            <TabButton
              key={p}
              label={PAGE_LABEL[p]}
              active={activePage === p}
              onClick={() => go(p)}
            />
          ))}
          {ledger && (
            <button
              onClick={() => setLedgerOpen((v) => !v)}
              className="ml-auto rounded border border-slate-700 bg-slate-900 px-2 py-1 text-slate-400 hover:border-amber-600 hover:text-amber-300">
              {ledgerOpen ? '▾' : '▸'} surface ledger
              {sa != null && <span className="ml-1 text-amber-400">✓{sa.agreed}/{sa.total}</span>}
            </button>
          )}
        </nav>

        {/* surface-ledger drawer — compact on every page (it's the demo gate; it belongs
            everywhere, §7.3.2). Expands to a full ledger view in place. */}
        {ledgerOpen && ledger && (
          <SurfaceLedgerDrawer ledger={ledger} ghBase={state.gh_blob_base} />
        )}
      </div>
    </header>
  );
}

function TabButton({ label, active, onClick }: { label: string; active: boolean; onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      className={`rounded px-2.5 py-1 font-medium transition ${
        active
          ? 'bg-sky-600 text-white'
          : 'bg-slate-900 text-slate-400 hover:bg-slate-800 hover:text-slate-200'
      }`}>
      {label}
    </button>
  );
}

function PixelCell({
  value, label, sub, tone, big, href, onClick,
}: {
  value: ReactNode;
  label: string;
  sub?: string;
  tone: 'urgent' | 'warn' | 'calm' | 'neutral';
  big?: boolean;
  href?: string;
  onClick?: () => void;
}) {
  const toneRing =
    tone === 'urgent' ? 'ring-2 ring-rose-500/70 bg-rose-950/30'
    : tone === 'warn' ? 'ring-1 ring-amber-600/50 bg-amber-950/20'
    : tone === 'calm' ? 'ring-1 ring-emerald-700/40 bg-emerald-950/10'
    : 'ring-1 ring-slate-700/60 bg-slate-900/40';
  const inner = (
    <div className={`flex h-full flex-col justify-between rounded-lg p-2 ${toneRing}`}>
      <div className={`font-bold tabular-nums text-slate-100 ${big ? 'text-2xl sm:text-3xl' : 'text-lg sm:text-xl'}`}>
        {value}
      </div>
      <div className="mt-0.5">
        <div className="text-[0.7rem] font-medium leading-tight text-slate-300">{label}</div>
        {sub && <div className="text-[0.62rem] leading-tight text-slate-500">{sub}</div>}
      </div>
    </div>
  );
  if (href) {
    return <a href={href} target="_blank" rel="noreferrer" className="block">{inner}</a>;
  }
  if (onClick) {
    return <button onClick={onClick} className="block w-full text-left">{inner}</button>;
  }
  return inner;
}

// ---------------------------------------------------------------------------
// The surface-ledger drawer — compact rows, deep-linked. Reuses the tracker's
// modeled queue rows (§7.2 shapes).
// ---------------------------------------------------------------------------
function SurfaceLedgerDrawer({ ledger, ghBase }: { ledger: Tracker; ghBase: string }) {
  return (
    <div className="mt-2 max-h-72 overflow-y-auto rounded-lg border border-amber-800/40 bg-amber-950/10 p-3">
      <div className="mb-1 flex items-center justify-between">
        <span className="text-xs font-semibold text-amber-300">
          Surface Ledger <span className="font-normal text-amber-500/70">— the demo gate (GATE1)</span>
        </span>
        {ledger.surfaces_agreed && (
          <span className="text-xs text-amber-400">
            ✓{ledger.surfaces_agreed.agreed} agreed / {ledger.surfaces_agreed.total} total
          </span>
        )}
      </div>
      {ledger.queues.map((q) => (
        <div key={q.line} className="mt-2">
          <a
            href={githubLink(ghBase, ledger.path, q.line)}
            target="_blank" rel="noreferrer"
            className="text-[0.72rem] font-semibold text-amber-200 hover:text-amber-100">
            {q.title}
          </a>
          {q.rows.map((r) => (
            <RowLine key={r.id + r.line} row={r} ghBase={ghBase} path={ledger.path} />
          ))}
        </div>
      ))}
    </div>
  );
}

// ---------------------------------------------------------------------------
// LANDING (`/`) — the slim index in current Tier-0 form. The ORIGINAL one-screen
// glance, preserved (§7.4.1): the tracker cards, each tapping through to its page
// (surface ledger opens the drawer), PLUS the SIXTH card — Kits — whose face is the
// PART F roster tallies (25 K + 6 H, per-status counts). Plus "since you last looked".
// ---------------------------------------------------------------------------
function Landing({ state, watermark }: { state: State; watermark: string | null }) {
  const serial = state.trackers.find((t) => t.id === 'serial-content-emission');
  return (
    <div className="space-y-6">
      <section className="grid grid-cols-1 gap-3 sm:grid-cols-2">
        {state.trackers.map((t) => (
          <IndexCard key={t.id} tracker={t} />
        ))}
        {/* sixth card slot — Kits (§7.4.1). Card face = PART F roster tallies. */}
        {serial && <KitsIndexCard tracker={serial} />}
      </section>
      <SinceYouLastLooked state={state} watermark={watermark} />
    </div>
  );
}

// The sixth landing card (§7.4.1) — the Kits roster tallies as the card face, tapping
// through to /kits. Reuses the PART-F pin (partFTally) so the face is DERIVED from the
// serial tracker's PART F rows, never hand-authored.
function KitsIndexCard({ tracker }: { tracker: Tracker }) {
  const t = partFTally(tracker);
  if (!t) return null;
  return (
    <button
      onClick={() => go('kits')}
      className="flex flex-col rounded-lg border border-sky-800/50 bg-sky-950/20 p-3 text-left transition hover:border-sky-600 hover:bg-sky-950/40">
      <div className="flex items-center justify-between">
        <h2 className="font-semibold text-slate-100">Kits</h2>
        <span className="rounded bg-slate-800 px-1.5 py-0.5 text-[0.65rem] font-medium text-slate-400">
          ROSTER OF RECORD
        </span>
      </div>
      <div className="mt-2 text-xs text-slate-400">
        the demo-curation denominator — PART F, {t.kCount} K + {t.hCount} H ={' '}
        <span className="text-slate-200">{t.total} kits</span>
      </div>
      <div className="mt-2 flex flex-wrap gap-1.5">
        {COUNTER_ORDER.map((k) => {
          const n = t.tally[k];
          if (n === 0) return null;
          const c = STATUS_COLOR[k];
          return (
            <span key={k} className={`rounded border px-1.5 py-0.5 text-[0.7rem] ${c.chip}`}>
              {STATUS_SYMBOL[k]} {n}
            </span>
          );
        })}
      </div>
      <span className="mt-2 text-[0.7rem] text-sky-500">open roster →</span>
    </button>
  );
}

// A slim tracker card on the landing index. Taps through to its page (or, for the
// surface-ledger, its own compact card that jumps to the drawer via the header).
function IndexCard({ tracker }: { tracker: Tracker }) {
  const isLedger = tracker.id === 'surface-ledger';
  const page = PAGE_ORDER.find((p) => PAGE_TRACKER[p] === tracker.id) ?? null;
  const latest = tracker.deltas[0];
  const onOpen = () => {
    if (page) go(page);
    else window.location.hash = '#/'; // ledger has no page; landing shows it via drawer
  };
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

      {/* flow-bar as the card lead (§2.7) when the tracker declares FLOW */}
      {tracker.flow && <FlowBar flow={tracker.flow} compact />}

      {latest && (
        <div className="mt-2 text-xs text-slate-400">
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
      <span className="mt-2 text-[0.7rem] text-sky-500">
        {isLedger ? 'open ledger drawer ↑' : 'open page →'}
      </span>
    </button>
  );
}

// ---------------------------------------------------------------------------
// FLOW BAR (§2.7) — the ordered stages as a compact segmented bar, each segment
// colored by its dominant token. Tapping a segment scrolls to that stage's queues
// (in-page Tier-1). Segment width ∝ modeled-row count (min floor so quiet stages
// stay visible).
// ---------------------------------------------------------------------------
function FlowBar({
  flow, compact, onStage,
}: {
  flow: NonNullable<Tracker['flow']>;
  compact?: boolean;
  onStage?: (stage: FlowStage) => void;
}) {
  const totals = flow.stages.map((s) => Math.max(1, counterTotal(s.counters)));
  const sum = totals.reduce((a, b) => a + b, 0);
  return (
    <div className={compact ? 'mt-2' : ''}>
      <div className={`flex w-full overflow-hidden rounded ${compact ? 'h-2' : 'h-3'} bg-slate-800`}>
        {flow.stages.map((s, i) => (
          <div
            key={s.n}
            className={FLOW_SEGMENT_COLOR[s.dominant]}
            style={{ width: `${(totals[i] / sum) * 100}%` }}
            title={`${s.n}. ${s.name} — ${FLOW_DOMINANT_LABEL[s.dominant]} (${counterTotal(s.counters)} rows)`}
          />
        ))}
      </div>
      {!compact && (
        <ol className="mt-2 grid grid-cols-2 gap-1.5 sm:grid-cols-3">
          {flow.stages.map((s) => {
            const total = counterTotal(s.counters);
            const clickable = !!onStage;
            return (
              <li key={s.n}>
                <button
                  disabled={!clickable}
                  onClick={() => onStage?.(s)}
                  className={`flex w-full items-center gap-2 rounded border border-slate-800 bg-slate-900/40 px-2 py-1.5 text-left text-xs ${
                    clickable ? 'hover:border-slate-600' : ''
                  }`}>
                  <span className={`h-2.5 w-2.5 shrink-0 rounded-sm ${FLOW_SEGMENT_COLOR[s.dominant]}`} />
                  <span className="min-w-0">
                    <span className="block truncate font-medium text-slate-200">
                      {s.n}. {s.name}
                    </span>
                    <span className="text-[0.65rem] text-slate-500">
                      {total > 0 ? `${total} rows · ${FLOW_DOMINANT_LABEL[s.dominant]}` : 'quiet'}
                      {!s.resolved && <span className="ml-1 text-amber-400">⚠ ref</span>}
                    </span>
                  </span>
                </button>
              </li>
            );
          })}
        </ol>
      )}
    </div>
  );
}

// ---------------------------------------------------------------------------
// DOMAIN PAGE (§7.4) — the tracker's Tier-0 card EXPANDED IN PLACE:
//   flow-bar → STATUS → latest delta (full) + older (collapsed) → counters →
//   queue tables. All under the §4 supersession law (delta before body). Tier-1
//   drill is in-page; Tier-2 source deep-links unchanged (every claim → file+line).
//
// v1.5: BOTH process pages (/engine + /content-emission) now lead flow-bar-first.
// The KIT ROSTER moved OUT to its own /kits page (KitsPage below) — v1.4's rule that
// content-emission leads with the roster is DEAD.
// ---------------------------------------------------------------------------
function DomainPage({ state, page }: { state: State; page: PageId }) {
  const trackerId = PAGE_TRACKER[page];
  const tracker = state.trackers.find((t) => t.id === trackerId);
  if (!tracker) {
    return <div className="p-8 text-slate-500">No modeled tracker for “{PAGE_LABEL[page]}”.</div>;
  }
  const ghBase = state.gh_blob_base;

  // /kits is the roster home — a distinct page off the same serial tracker (§7.4.2).
  if (page === 'kits') {
    return <KitsPage tracker={tracker} ghBase={ghBase} />;
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-baseline justify-between gap-2">
        <h1 className="text-xl font-bold text-slate-100">{PAGE_LABEL[page]}</h1>
        <a
          href={githubLink(ghBase, tracker.path, 1)}
          target="_blank" rel="noreferrer"
          className="text-xs text-sky-400 hover:text-sky-300">
          open tracker on GitHub ↗
        </a>
      </div>

      {/* flow-bar lead (§2.7) — the abstracted end-to-end process view */}
      {tracker.flow && (
        <section>
          <h2 className="mb-2 text-sm font-semibold text-slate-300">
            Process flow <span className="font-normal text-slate-500">(end-to-end, derived)</span>
          </h2>
          <FlowBar
            flow={tracker.flow}
            onStage={(s) => {
              const el = document.getElementById(`stage-${s.n}`);
              el?.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }}
          />
        </section>
      )}

      {/* §4 supersession law: STATUS banner → latest delta (full) → older (collapsed) */}
      {tracker.status_banner && (
        <a
          href={githubLink(ghBase, tracker.path, tracker.status_banner.line)}
          target="_blank" rel="noreferrer"
          className="block rounded border border-slate-800 bg-slate-900/40 px-3 py-2 text-xs text-slate-400 hover:border-slate-600">
          <span className="font-semibold text-slate-300">{tracker.status_banner.stamp}</span>
          {tracker.status_banner.date && <span className="ml-2 font-mono">{tracker.status_banner.date}</span>}
          <div className="mt-1"><InlineMd src={tracker.status_banner.raw.replace(/^>\s*/, '')} /></div>
        </a>
      )}

      <DeltaTimeline tracker={tracker} ghBase={ghBase} />

      {/* counters */}
      <div className="flex flex-wrap gap-1.5">
        {COUNTER_ORDER.map((k) => {
          const n = tracker.counters[k];
          if (n === 0) return null;
          const c = STATUS_COLOR[k];
          return (
            <span key={k} className={`rounded border px-2 py-0.5 text-xs ${c.chip}`}>
              {STATUS_SYMBOL[k]} {STATUS_LABEL[k]} {n}
            </span>
          );
        })}
      </div>

      {/* queues as in-page Tier-1 tables (sortable/filterable) */}
      <QueueTables tracker={tracker} ghBase={ghBase} />
    </div>
  );
}

// ---------------------------------------------------------------------------
// KIT ROSTER OF RECORD (§7.4) — PART F, promoted to the /kits page lead by
// SECTION-NAME PIN. The pin: the serial tracker's queues titled `F.1…` / `F.2…`
// (the PART F sub-tables). Rendered as the authored 5-column table:
//   ID · ARPG Genre Canon kit · BC cell/hypothesis · status · blockers/held rules.
// Roster row count + status tallies join the page header block. gates-on tokens
// dangle as §2.6 warning badges (visible debt) — never a build failure.
//
// v1.5: the roster's HOME is now /kits (KitsPage). content-emission no longer
// renders it (v1.4's lead-element rule is DEAD).
// ---------------------------------------------------------------------------
function isPartFQueue(q: Queue): boolean {
  // section-name pin: PART F's authored sub-tables are titled "F.1 …" / "F.2 …".
  return /^F\.\d/.test(q.title.trim());
}

// PART-F tally, DERIVED from the pinned rows (never hand-authored). Used by both the
// /kits page header and the landing sixth card's face. null when no PART F is modeled.
function partFTally(tracker: Tracker): {
  kCount: number; hCount: number; total: number; tally: Record<StatusToken, number>;
} | null {
  const partF = tracker.queues.filter(isPartFQueue);
  if (partF.length === 0) return null;
  const rows = partF.flatMap((q) => q.rows);
  const kCount = rows.filter((r) => /^K\d/.test(r.id)).length;
  const hCount = rows.filter((r) => /^H\d/.test(r.id)).length;
  const tally = { open: 0, in_flight: 0, blocked: 0, awaiting_ruling: 0, parked: 0, closed: 0 } as Record<StatusToken, number>;
  for (const r of rows) tally[r.status.token] += 1;
  return { kCount, hCount, total: rows.length, tally };
}

// ---------------------------------------------------------------------------
// KITS PAGE (§7.4.2) — the roster's own page. LEADS with the PART F table (the
// NOUN-list: what kits exist), then a thin footer note. Named future consumer of
// the §7.1 feed-2 registry snapshot: per-kit cert truth auto-joins these rows when
// star-lord's export lands (SEAM WIRED below — v1 renders doc truth only).
// ---------------------------------------------------------------------------
function KitsPage({ tracker, ghBase }: { tracker: Tracker; ghBase: string }) {
  const hasRoster = tracker.queues.some(isPartFQueue);
  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-baseline justify-between gap-2">
        <h1 className="text-xl font-bold text-slate-100">{PAGE_LABEL.kits}</h1>
        <a
          href={githubLink(ghBase, tracker.path, 1)}
          target="_blank" rel="noreferrer"
          className="text-xs text-sky-400 hover:text-sky-300">
          open serial tracker on GitHub ↗
        </a>
      </div>

      {hasRoster ? (
        <KitRoster tracker={tracker} ghBase={ghBase} />
      ) : (
        <div className="rounded-lg border border-slate-800 bg-slate-900/40 p-6 text-sm text-slate-500">
          No PART F roster is modeled in the serial tracker yet. The roster renders here
          once the <span className="font-mono">## PART F</span> sub-tables (F.1 / F.2) parse.
        </div>
      )}

      {/* §7.1 feed-2 SEAM (wired, not blocked): when star-lord's registry-snapshot export
          lands at agentic_orchestration/run-registry/emission-runs-snapshot.json, per-kit
          cert truth (emission runs, gauntlet results) auto-joins the roster rows as machine
          truth. v1 renders doc truth only. TODO(drax): join snapshot rows when feed-2 ships. */}
      <p className="text-[0.7rem] text-slate-600">
        Per-kit cert status will auto-fill from emission runs when the run-registry snapshot
        feed lands (§7.1 feed-2). Today this roster reflects doc truth only.
      </p>
    </div>
  );
}

function KitRoster({ tracker, ghBase }: { tracker: Tracker; ghBase: string }) {
  const partF = tracker.queues.filter(isPartFQueue);
  if (partF.length === 0) return null;

  const t = partFTally(tracker)!;
  const { kCount, hCount, tally } = t;

  return (
    <section className="rounded-lg border border-sky-800/50 bg-sky-950/20 p-3">
      <div className="mb-2 flex flex-wrap items-baseline justify-between gap-2">
        <h2 className="text-sm font-bold text-slate-100">
          KIT ROSTER OF RECORD
          <span className="ml-2 font-normal text-slate-500">first glance — PART F</span>
        </h2>
        {/* roster tallies in the page header block (§7.4): 25 K + 6 H, per-status counts */}
        <div className="flex flex-wrap items-center gap-1.5 text-[0.7rem]">
          <span className="rounded bg-slate-800 px-1.5 py-0.5 text-slate-300">
            {kCount} K + {hCount} H = {t.total}
          </span>
          {COUNTER_ORDER.map((k) => {
            if (tally[k] === 0) return null;
            const c = STATUS_COLOR[k];
            return (
              <span key={k} className={`rounded border px-1.5 py-0.5 ${c.chip}`}>
                {STATUS_SYMBOL[k]} {tally[k]}
              </span>
            );
          })}
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full border-collapse text-left text-xs">
          <thead>
            <tr className="border-b border-slate-700 text-[0.7rem] uppercase tracking-wide text-slate-500">
              <th className="py-1 pr-2">ID</th>
              <th className="py-1 pr-2">ARPG Genre Canon kit</th>
              <th className="py-1 pr-2">BC cell / hypothesis</th>
              <th className="py-1 pr-2">Status</th>
              <th className="py-1 pr-2">Blockers / held rules</th>
            </tr>
          </thead>
          <tbody>
            {partF.map((q) =>
              q.rows.map((r) => <KitRosterRow key={r.id + r.line} row={r} tracker={tracker} ghBase={ghBase} />)
            )}
          </tbody>
        </table>
      </div>
    </section>
  );
}

function KitRosterRow({ row, tracker, ghBase }: { row: QueueRow; tracker: Tracker; ghBase: string }) {
  const c = STATUS_COLOR[row.status.token];
  // authored columns: [ID, kit, BC cell, status, blockers]. Prefer the real cells;
  // fall back gracefully if a row is short.
  const kit = row.cells_md[1] ?? '';
  const bc = row.cells_md[2] ?? '';
  const blockers = row.cells_md[4] ?? row.cells_md.slice(4).join(' · ') ?? '';
  return (
    <tr className="border-b border-slate-800/60 align-top">
      <td className="py-1.5 pr-2">
        <a
          href={githubLink(ghBase, tracker.path, row.line)}
          target="_blank" rel="noreferrer"
          className="rounded bg-slate-800 px-1.5 py-0.5 font-mono text-slate-300 hover:bg-slate-700 hover:text-sky-300">
          {row.id}
        </a>
      </td>
      <td className="py-1.5 pr-2 text-slate-200"><InlineMd src={kit} /></td>
      <td className="py-1.5 pr-2 text-slate-400"><InlineMd src={bc} /></td>
      <td className="py-1.5 pr-2">
        <span className={`inline-flex items-center gap-1 whitespace-nowrap rounded border px-1.5 py-0.5 text-[0.68rem] ${c.chip}`}>
          {STATUS_SYMBOL[row.status.token]} {STATUS_LABEL[row.status.token]}
        </span>
      </td>
      <td className="py-1.5 pr-2 text-slate-400">
        <InlineMd src={blockers} />
        {/* dangling cross-doc gates-on (E6, totem-probe, proxy-P0/P1/P2) → warning badges */}
        {row.gates_on.filter((g) => g.dangling).length > 0 && (
          <span className="mt-1 flex flex-wrap gap-1">
            {row.gates_on.filter((g) => g.dangling).map((g, i) => (
              <span
                key={i}
                title="Dangling cross-doc gate: resolves to no modeled row (visible debt, not a build failure)"
                className="inline-flex items-center gap-1 rounded border border-amber-700 bg-amber-900/30 px-1 py-0.5 text-[0.62rem] text-amber-300">
                ⚠ {g.token}{g.qualifier ? ` (${g.qualifier})` : ''}
              </span>
            ))}
          </span>
        )}
      </td>
    </tr>
  );
}

// ---------------------------------------------------------------------------
// Queue tables — in-page Tier-1. On the content-emission page the PART F tables
// are already shown as the roster lead, so they are excluded here (no double render).
// ---------------------------------------------------------------------------
function QueueTables({ tracker, ghBase }: { tracker: Tracker; ghBase: string }) {
  const [statusFilter, setStatusFilter] = useState<StatusToken | 'all'>('all');
  const [ownerFilter, setOwnerFilter] = useState<string | 'all'>('all');
  const [sortBy, setSortBy] = useState<'board' | 'status' | 'owner'>('board');

  const owners = useMemo(() => {
    const set = new Set<string>();
    for (const q of tracker.queues) for (const r of q.rows) if (r.owner) set.add(r.owner);
    return Array.from(set).sort();
  }, [tracker]);

  // exclude the PART F sub-tables on the content-emission page — they lead the page.
  const queues = tracker.id === 'serial-content-emission'
    ? tracker.queues.filter((q) => !isPartFQueue(q))
    : tracker.queues;

  if (queues.length === 0) return null;

  return (
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

      {queues.map((q) => {
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
        // stage anchor: if any FLOW stage maps to this queue's board, tag it so the
        // flow-bar segment can scroll here. Best-effort by title-substring.
        const stage = tracker.flow?.stages.find((s) =>
          s.refs.some((ref) => q.title.includes(ref)));
        return (
          <div
            key={q.line}
            id={stage ? `stage-${stage.n}` : undefined}
            className="mb-4 scroll-mt-40 rounded-lg border border-slate-800 bg-slate-900/30 p-3">
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
          className="font-mono text-xs text-sky-400 hover:text-sky-300">
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
                    className="font-mono text-xs text-slate-500 hover:text-sky-300">
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
// "Since you last looked" — the four delta logs merged, newest first; entries
// newer than the localStorage watermark highlighted. (§5 — ~60% of the value.)
// ---------------------------------------------------------------------------
function SinceYouLastLooked({ state, watermark }: { state: State; watermark: string | null }) {
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
          const page = PAGE_ORDER.find((p) => PAGE_TRACKER[p] === d.tracker) ?? null;
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
                  onClick={() => go(page)}
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
