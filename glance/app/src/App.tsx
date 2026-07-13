import { useEffect, useMemo, useState, type ReactNode } from 'react';
import {
  type State, type Tracker, type TrackerId, type StatusToken, type QueueRow,
  type Queue, type Flow, type FlowStage, type Pipeline, type PageId,
  type Reference, type ReferenceId,
  TRACKER_LABEL, STATUS_LABEL, STATUS_SYMBOL, STATUS_COLOR,
  FLOW_SEGMENT_COLOR, FLOW_DOMINANT_LABEL,
  PAGE_ORDER, PAGE_LABEL, PAGE_TRACKER, PAGE_FLOW_SOURCE,
  REFERENCE_PAGES, isReferencePage, PAGE_REFERENCE, TRIPLE_LAW, TRIPLE_LAW_SIBLINGS,
  WATERMARK_KEY, maxDeltaDate, commitAge, githubLink, counterTotal,
} from './state';
import { InlineMd, BlockMd, SectionMd } from './md';
import { RowLine } from './components';

// ---------------------------------------------------------------------------
// Routing — hash-based, zero dependency (§7.4). The SPA rewrite in vercel.json
// already funnels every path to index.html, so hash routes work identically in
// preview + prod with no 404 risk (the May-12 lesson). Routes (v1.8 — six pages):
//   #/                     → the slim seven-card landing index (the original glance)
//   #/engine #/story #/game #/content-emission #/kits #/minigames  → six domain pages
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

        {/* nav — nine tabs (§7.7 v1.9). The reference TRIO is seated adjacent at the
            end (coordinates → atlas → mechanics) behind a subtle divider: they are a
            distinct kind (kit-design reference registers), not domain/process pages. */}
        <nav className="mt-2 flex flex-wrap items-center gap-1 text-xs">
          <TabButton label="Overview" active={activePage === null} onClick={() => go(null)} />
          {PAGE_ORDER.map((p, i) => {
            const isFirstRef = REFERENCE_PAGES[0] === p;
            return (
              <span key={p} className="flex items-center gap-1">
                {isFirstRef && i > 0 && (
                  <span
                    aria-hidden
                    title="kit-design reference"
                    className="mx-1 hidden h-4 w-px bg-slate-700 sm:inline-block"
                  />
                )}
                <TabButton
                  label={PAGE_LABEL[p]}
                  active={activePage === p}
                  onClick={() => go(p)}
                />
              </span>
            );
          })}
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
  const arcade = state.pipelines.find((p) => p.id === 'arcade') ?? null;
  return (
    <div className="space-y-6">
      <section className="grid grid-cols-1 gap-3 sm:grid-cols-2">
        {state.trackers.map((t) => (
          <IndexCard key={t.id} tracker={t} pipelines={state.pipelines} />
        ))}
        {/* sixth card slot — Kits (§7.4.1). Card face = PART F roster tallies. */}
        {serial && <KitsIndexCard tracker={serial} />}
        {/* seventh card slot — Minigames (§7.6 v1.8). Card face = arcade A0–A7 FLOW
            preview; reads PARTIAL·GAP·GATED honestly until the arcade build fires. */}
        {arcade && <MinigamesIndexCard pipeline={arcade} />}
      </section>

      {/* §7.7 v1.9 rule 5 — the kit-design reference TRIO as a LEAN grouped tile row
          (drax layout call). An all-quiet FLOW-bar state card would spend Tier-0 pixels
          on no information; compact LINK TILES read better. Full state cards deliberately
          NOT used here. */}
      {state.references.length > 0 && (
        <ReferenceTileRow references={state.references} />
      )}

      <SinceYouLastLooked state={state} watermark={watermark} />
    </div>
  );
}

// §7.7 v1.9 rule 5 — the grouped "kit-design reference" tile row. Lean by design: one
// tile per reference page, each carrying its TRIPLE-LAW layer label + one-line role +
// stage count — navigation, not state (the bars would be all-quiet, so we don't spend
// pixels rendering them here). /atlas (the connective PROJECTION layer) is centered.
function ReferenceTileRow({ references }: { references: Reference[] }) {
  // render in the read-as-one-instrument order: coordinates → atlas → mechanics.
  const order: ReferenceId[] = ['coordinates', 'atlas', 'mechanics'];
  const byId = new Map(references.map((r) => [r.id, r]));
  return (
    <section>
      <h2 className="mb-2 text-sm font-semibold text-slate-300">
        Kit-design reference{' '}
        <span className="font-normal text-slate-500">
          (the TRIPLE LAW — sample the coordinate → project the fields → verify the surfaces)
        </span>
      </h2>
      <div className="grid grid-cols-1 gap-2 sm:grid-cols-3">
        {order.map((id) => {
          const ref = byId.get(id);
          if (!ref) return null;
          const law = TRIPLE_LAW[id];
          const stages = ref.flow?.stages.length ?? 0;
          const connective = id === 'atlas';
          return (
            <button
              key={id}
              onClick={() => go(law.page)}
              className={`flex flex-col rounded-lg border p-3 text-left transition ${
                connective
                  ? 'border-teal-700/60 bg-teal-950/20 hover:border-teal-500 hover:bg-teal-950/40'
                  : 'border-slate-700/60 bg-slate-900/40 hover:border-slate-500 hover:bg-slate-900'
              }`}>
              <div className="flex items-center justify-between">
                <span className="font-semibold text-slate-100">{PAGE_LABEL[law.page]}</span>
                <span className={`rounded px-1.5 py-0.5 text-[0.6rem] font-bold uppercase tracking-wide ${
                  connective ? 'bg-teal-800/60 text-teal-200' : 'bg-slate-800 text-slate-400'
                }`}>
                  {law.layer}
                </span>
              </div>
              <div className="mt-1 text-xs text-slate-400">{law.role}</div>
              <div className="mt-2 text-[0.65rem] text-slate-500">
                {stages} stages · reference register (quiet bars)
                {connective && <span className="ml-1 text-teal-400">· the map</span>}
              </div>
              <span className="mt-2 text-[0.7rem] text-sky-500">open reference →</span>
            </button>
          );
        })}
      </div>
    </section>
  );
}

// The seventh landing card (§7.6 v1.8) — the arcade pipeline's A0–A7 FLOW preview as
// the card face, tapping through to /minigames. Card face reads the honest PARTIAL·GAP·
// GATED stamp (POST-LAUNCH mode factory) — that honest read is the point; nothing masks
// it. The FLOW segments derive `quiet` neutral (no modeled rows) — faithful to the doc.
function MinigamesIndexCard({ pipeline }: { pipeline: Pipeline }) {
  return (
    <button
      onClick={() => go('minigames')}
      className="flex flex-col rounded-lg border border-violet-800/50 bg-violet-950/20 p-3 text-left transition hover:border-violet-600 hover:bg-violet-950/40">
      <div className="flex items-center justify-between">
        <h2 className="font-semibold text-slate-100">Minigames</h2>
        <span className="rounded bg-violet-900/50 px-1.5 py-0.5 text-[0.65rem] font-medium text-violet-300">
          POST-LAUNCH
        </span>
      </div>
      {/* the arcade A0–A7 FLOW as the card lead (§2.7); segments quiet until build fires */}
      {pipeline.flow && <FlowBar flow={pipeline.flow} compact />}
      <div className="mt-2 text-xs text-slate-400">
        the machine-run mode factory — A0–A7,{' '}
        <span className="text-slate-200">PARTIAL · GAP · GATED</span> until the arcade build fires
      </div>
      <span className="mt-2 text-[0.7rem] text-violet-400">open pipeline →</span>
    </button>
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
function IndexCard({ tracker, pipelines }: { tracker: Tracker; pipelines: Pipeline[] }) {
  const isLedger = tracker.id === 'surface-ledger';
  const page = PAGE_ORDER.find((p) => PAGE_TRACKER[p] === tracker.id) ?? null;
  // §7.5 v1.6 — the card face's FLOW preview follows the SAME repoint as the page
  // lead: if the tracker's page repoints to a product pipeline, preview THAT flow;
  // else preview the tracker's own (demoted) FLOW. Keeps card ↔ page consistent.
  const cardFlow: Flow | null = (() => {
    if (!page) return tracker.flow ?? null;
    const src = PAGE_FLOW_SOURCE[page];
    if (src && src.kind === 'pipeline') {
      return pipelines.find((p) => p.id === src.id)?.flow ?? null;
    }
    return tracker.flow ?? null;
  })();
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

      {/* flow-bar as the card lead (§2.7) — the pipeline flow when the page repoints
          to a product pipeline (§7.5 v1.6), else the tracker's own FLOW */}
      {cardFlow && <FlowBar flow={cardFlow} compact />}

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
  const ghBase = state.gh_blob_base;

  // §7.7 v1.9 — the reference TRIO (/coordinates · /atlas · /mechanics). These have NO
  // backing tracker (they're FLOW-led verbatim-payload reference docs, like the
  // pipelines). Short-circuit BEFORE the tracker lookup — they render pipeline-class,
  // not tracker-class (FLOW bar quiet-by-design → TRIPLE-LAW cross-links → per-stage
  // `## §N` drill → verbatim payload sections). No queues, no deltas.
  if (isReferencePage(page)) {
    const refId = PAGE_REFERENCE[page]!;
    const reference = state.references.find((r) => r.id === refId) ?? null;
    return <ReferencePage reference={reference} page={page} ghBase={ghBase} />;
  }

  const trackerId = PAGE_TRACKER[page]!;
  const tracker = state.trackers.find((t) => t.id === trackerId);
  if (!tracker) {
    return <div className="p-8 text-slate-500">No modeled tracker for “{PAGE_LABEL[page]}”.</div>;
  }

  // /kits is the roster home — a distinct page off the same serial tracker (§7.4.2).
  if (page === 'kits') {
    return <KitsPage tracker={tracker} ghBase={ghBase} />;
  }

  // §7.6 v1.8 — /minigames is the arcade-pipeline home. It has NO tracker of its own
  // (the arcade doc is a pipeline); it leads flow-bar-first off the arcade PIPELINE and
  // renders pipeline-lead-only. It deliberately does NOT surface the (backing) game
  // tracker's queues/deltas — the page is a MATT-FACING product-flow view + scope rider.
  if (page === 'minigames') {
    const arcade = state.pipelines.find((p) => p.id === 'arcade') ?? null;
    return <MinigamesPage pipeline={arcade} ghBase={ghBase} />;
  }

  // §7.5 v1.6 — the lead FLOW source is ONE config line per page (PAGE_FLOW_SOURCE):
  // the two PROCESS pages (/engine + /content-emission) lead with a MATT-FACING
  // product pipeline doc (S0–S8 / E0–E8); /story + /game keep their tracker FLOW.
  const flowSource = PAGE_FLOW_SOURCE[page] ?? { kind: 'tracker' as const };
  const leadPipeline = flowSource.kind === 'pipeline'
    ? state.pipelines.find((p) => p.id === flowSource.id) ?? null
    : null;

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

      {/* LEAD FLOW (§2.7 / §7.5 v1.6). When this page repoints to a product pipeline
          doc, that pipeline's FLOW (S0–S8 / E0–E8) + verbatim ASCII is the lead. Else
          the tracker's own FLOW leads (story/game, until their pipeline docs land). */}
      {leadPipeline
        ? <PipelineFlowLead pipeline={leadPipeline} ghBase={ghBase} />
        : tracker.flow && (
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

      {/* §7.5 v1.6 change #3 — the tracker's own `## FLOW` is DEMOTED to doc-nav:
          still parsed, still derived, but rendered below-the-fold (Tier-1) because
          it answers "which PART to read," not product flow. Only shown when a
          product pipeline leads the page (else the tracker FLOW IS the lead above). */}
      {leadPipeline && tracker.flow && (
        <TrackerFlowDocNav flow={tracker.flow} tracker={tracker} ghBase={ghBase} />
      )}
    </div>
  );
}

// §7.5 v1.6 change #3 — the demoted tracker FLOW as below-the-fold doc navigation.
// Collapsed by default; expands to the non-compact FLOW bar whose segments scroll to
// the in-page queue tables (the existing stage-N anchors). It's PART-navigation.
function TrackerFlowDocNav({
  flow, tracker, ghBase,
}: { flow: Flow; tracker: Tracker; ghBase: string }) {
  const [open, setOpen] = useState(false);
  return (
    <section className="rounded-lg border border-slate-800 bg-slate-900/30 p-3">
      <button
        onClick={() => setOpen((v) => !v)}
        className="flex w-full items-center justify-between text-left">
        <span className="text-sm font-semibold text-slate-300">
          {open ? '▾' : '▸'} Doc navigation{' '}
          <span className="font-normal text-slate-500">
            (which PART to read — the tracker's own flow, not product flow)
          </span>
        </span>
        <a
          href={githubLink(ghBase, tracker.path, flow.line)}
          target="_blank" rel="noreferrer"
          onClick={(e) => e.stopPropagation()}
          className="text-xs text-sky-400 hover:text-sky-300">
          source ↗
        </a>
      </button>
      {open && (
        <div className="mt-3">
          <FlowBar
            flow={flow}
            onStage={(s) => {
              const el = document.getElementById(`stage-${s.n}`);
              el?.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }}
          />
        </div>
      )}
    </section>
  );
}

// ---------------------------------------------------------------------------
// PIPELINE FLOW LEAD (§7.5 v1.6) — the MATT-FACING product data-flow doc as the
// lead of a PROCESS page. Three parts, top to bottom:
//   1. the §2.7 FLOW bar (S0–S8 / E0–E8), each segment clicking to its stage strip;
//   2. per-stage `##` drill strip — the FLOW-segment → stage sub-heading targets,
//      each deep-linking to the `## S#`/`## E#` heading on GitHub (drill-through);
//   3. the fenced ASCII flow diagram, rendered VERBATIM in a <pre> (NEVER parsed).
// Stage state derives `quiet` for these process docs (they carry no modeled rows),
// which the FLOW bar renders neutral — faithful to the substrate.
// ---------------------------------------------------------------------------
function PipelineFlowLead({ pipeline, ghBase }: { pipeline: Pipeline; ghBase: string }) {
  if (!pipeline.flow) {
    return (
      <section className="rounded-lg border border-slate-800 bg-slate-900/40 p-4 text-sm text-slate-500">
        The product pipeline doc declares no <span className="font-mono">## FLOW</span> yet.
      </section>
    );
  }
  const flow = pipeline.flow;
  return (
    <section>
      <div className="mb-2 flex flex-wrap items-baseline justify-between gap-2">
        <h2 className="text-sm font-semibold text-slate-300">
          Product pipeline <span className="font-normal text-slate-500">(end-to-end — the actual data-flow)</span>
        </h2>
        <a
          href={githubLink(ghBase, pipeline.path, 1)}
          target="_blank" rel="noreferrer"
          className="text-xs text-sky-400 hover:text-sky-300">
          open pipeline doc ↗
        </a>
      </div>

      {/* 1 — the FLOW bar; segments scroll to the per-stage drill strip below */}
      <FlowBar
        flow={flow}
        onStage={(s) => {
          const el = document.getElementById(`pipe-stage-${s.n}`);
          el?.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }}
      />

      {/* 2 — per-stage `##` drill targets (FLOW segment → stage sub-heading) */}
      <ol className="mt-3 grid grid-cols-1 gap-1.5 sm:grid-cols-2">
        {flow.stages.map((s) => (
          <li key={s.n} id={`pipe-stage-${s.n}`} className="scroll-mt-40">
            <a
              href={s.heading_line != null ? githubLink(ghBase, pipeline.path, s.heading_line) : githubLink(ghBase, pipeline.path, s.line)}
              target="_blank" rel="noreferrer"
              className="flex items-start gap-2 rounded border border-slate-800 bg-slate-900/40 px-2 py-1.5 text-xs hover:border-slate-600">
              <span className={`mt-0.5 h-2.5 w-2.5 shrink-0 rounded-sm ${FLOW_SEGMENT_COLOR[s.dominant]}`} />
              <span className="min-w-0">
                <span className="block font-medium text-slate-200">
                  {s.n}. {s.name}
                </span>
                <span className="text-[0.65rem] text-slate-500">
                  {s.resolved ? 'stage detail ↗' : <span className="text-amber-400">⚠ ref — no `##` heading</span>}
                </span>
              </span>
            </a>
          </li>
        ))}
      </ol>

      {/* 3 — the fenced ASCII flow diagram, VERBATIM (§7.5: render, do NOT parse) */}
      {pipeline.ascii && (
        <div className="mt-3">
          <a
            href={githubLink(ghBase, pipeline.path, pipeline.ascii.line)}
            target="_blank" rel="noreferrer"
            className="mb-1 block text-[0.7rem] text-slate-500 hover:text-sky-300">
            the visual flow (verbatim) ↗
          </a>
          <pre className="overflow-x-auto rounded-lg border border-slate-800 bg-slate-950/70 p-3 text-[0.6rem] leading-tight text-slate-300 sm:text-[0.7rem]">
            {pipeline.ascii.text}
          </pre>
        </div>
      )}
    </section>
  );
}

// ---------------------------------------------------------------------------
// MINIGAMES PAGE (§7.6 v1.8) — the arcade-pipeline home. Pipeline-lead-only: the
// arcade product FLOW (A0–A7) + per-stage drill + verbatim ASCII, PLUS the doc's
// POST-LAUNCH scope rider rendered PROMINENTLY near the FLOW bar (§7.6 rule 3) so the
// page never reads as a current build obligation. No tracker queues/deltas — the
// arcade is a pipeline, not a tracker. The A0–A7 stage stamps read PARTIAL·GAP·GATED
// honestly (the stages carry no modeled rows → derive `quiet` neutral); that honest
// read is the point (§7.6 rule 1) — nothing masks it.
// ---------------------------------------------------------------------------
function MinigamesPage({ pipeline, ghBase }: { pipeline: Pipeline | null; ghBase: string }) {
  if (!pipeline) {
    return (
      <div className="space-y-6">
        <h1 className="text-xl font-bold text-slate-100">{PAGE_LABEL.minigames}</h1>
        <div className="rounded-lg border border-slate-800 bg-slate-900/40 p-6 text-sm text-slate-500">
          The arcade product-pipeline doc (<span className="font-mono">pipeline-arcade.md</span>) is
          not modeled yet. The A0–A7 FLOW renders here once the doc parses.
        </div>
      </div>
    );
  }
  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-baseline justify-between gap-2">
        <h1 className="text-xl font-bold text-slate-100">{PAGE_LABEL.minigames}</h1>
        <a
          href={githubLink(ghBase, pipeline.path, 1)}
          target="_blank" rel="noreferrer"
          className="text-xs text-sky-400 hover:text-sky-300">
          open arcade pipeline on GitHub ↗
        </a>
      </div>

      {/* §7.6 rule 3 — the POST-LAUNCH scope rider, rendered PROMINENTLY near the FLOW
          bar (immediately above it) so the page never reads as a current build obligation. */}
      {pipeline.scope_rider && (
        <a
          href={githubLink(ghBase, pipeline.path, pipeline.scope_rider.line)}
          target="_blank" rel="noreferrer"
          className="block rounded-lg border-2 border-violet-700/60 bg-violet-950/25 px-4 py-3 transition hover:border-violet-500">
          <div className="mb-1 flex items-center gap-2">
            <span className="rounded bg-violet-800/60 px-1.5 py-0.5 text-[0.65rem] font-bold uppercase tracking-wide text-violet-200">
              POST-LAUNCH
            </span>
            <span className="text-xs font-semibold text-violet-300">
              scope rider — nothing on this page gates the demo or launch
            </span>
          </div>
          <div className="text-sm text-slate-300">
            <BlockMd src={pipeline.scope_rider.text} />
          </div>
        </a>
      )}

      {/* the arcade product FLOW (A0–A7) + per-stage drill + verbatim ASCII (reused). */}
      <PipelineFlowLead pipeline={pipeline} ghBase={ghBase} />
    </div>
  );
}

// ---------------------------------------------------------------------------
// REFERENCE PAGE (§7.7 v1.9) — one of the kit-design reference TRIO (/coordinates ·
// /atlas · /mechanics). A MATT-FACING FLOW-led verbatim-payload doc (pipeline doc
// class), NOT a tracker. Render order, top to bottom:
//   1. TRIPLE-LAW cross-link banner — links the OTHER TWO layers (§7.7 rule 4). On
//      /atlas (the connective PROJECTION page) the two links are the most load-bearing.
//   2. the lead FLOW bar (§2.7) — QUIET-BY-DESIGN (reference register, no modeled rows).
//      A tap scrolls to that stage's `## §N` drill target. Navigation, not state — we
//      do NOT invent coloring (§7.7 rule 3).
//   3. per-stage `## §N` drill strip — the FLOW-segment → section targets, each also
//      deep-linking to the `## §N` heading on GitHub (Tier-2 provenance).
//   4. the verbatim `## §N` payload sections — the lattice tables / resolver walkers /
//      projection table rendered UNPARSED via SectionMd (display fidelity, no semantic
//      parse). On /atlas: NO occupancy numbers — the §2 projection table is rendered
//      verbatim exactly as authored; the REALIZED ATLAS harness is not built (§7.7 rule 7).
// ---------------------------------------------------------------------------
function ReferencePage({
  reference, page, ghBase,
}: { reference: Reference | null; page: PageId; ghBase: string }) {
  if (!reference) {
    return (
      <div className="space-y-6">
        <h1 className="text-xl font-bold text-slate-100">{PAGE_LABEL[page]}</h1>
        <div className="rounded-lg border border-slate-800 bg-slate-900/40 p-6 text-sm text-slate-500">
          The reference doc for this page is not modeled yet. Its FLOW bar + verbatim
          sections render once the source doc parses.
        </div>
      </div>
    );
  }
  const law = TRIPLE_LAW[reference.id];
  const connective = reference.id === 'atlas';
  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-baseline justify-between gap-2">
        <h1 className="flex items-baseline gap-2 text-xl font-bold text-slate-100">
          {PAGE_LABEL[page]}
          <span className={`rounded px-1.5 py-0.5 text-[0.6rem] font-bold uppercase tracking-wide ${
            connective ? 'bg-teal-800/60 text-teal-200' : 'bg-slate-800 text-slate-400'
          }`}>
            {law.layer}
          </span>
          <span className="text-xs font-normal text-slate-500">{law.role}</span>
        </h1>
        <a
          href={githubLink(ghBase, reference.path, 1)}
          target="_blank" rel="noreferrer"
          className="text-xs text-sky-400 hover:text-sky-300">
          open reference doc on GitHub ↗
        </a>
      </div>

      {/* RULED V1.2 Stratified Plane View (Q19 LOCKED 2026-07-13) — the REALIZED
          projection, rendered as a DB-derived static asset. Contract v1.10 §7.7 render-
          adjacent addition (see AtlasPlaneView). ONLY on /atlas (the connective PROJECTION
          page); the LATTICE + CODEX layers have no realized plane. LEADS the page — the
          plane is the payload /atlas exists to surface, so it sits above the TRIPLE-LAW
          nav and STATUS banner (a scroll should not be required to see it). */}
      {connective && <AtlasPlaneView ghBase={ghBase} />}

      {/* 1 — the TRIPLE-LAW cross-link banner (§7.7 rule 4). Links the OTHER TWO layers. */}
      <TripleLawLinks refId={reference.id} />

      {/* STATUS banner (MATT-FACING purge-exempt stamp) — deep-linked. */}
      {reference.status_banner && (
        <a
          href={githubLink(ghBase, reference.path, reference.status_banner.line)}
          target="_blank" rel="noreferrer"
          className="block rounded border border-slate-800 bg-slate-900/40 px-3 py-2 text-xs text-slate-400 hover:border-slate-600">
          <span className="font-semibold text-slate-300">{reference.status_banner.stamp}</span>
          {reference.status_banner.date && <span className="ml-2 font-mono">{reference.status_banner.date}</span>}
          <div className="mt-1"><InlineMd src={reference.status_banner.raw.replace(/^>\s*/, '')} /></div>
        </a>
      )}

      {/* 2 + 3 — the QUIET-BY-DESIGN FLOW bar + per-stage `## §N` drill strip. */}
      <ReferenceFlowLead reference={reference} ghBase={ghBase} />

      {/* 4 — the verbatim `## §N` payload sections (rendered, NEVER parsed). */}
      <ReferenceSections reference={reference} ghBase={ghBase} />
    </div>
  );
}

// ---------------------------------------------------------------------------
// AtlasPlaneView — the RULED V1.2 Stratified Plane View (Q19 LOCKED 2026-07-13).
//
// PROVENANCE-CLEAN DERIVED ARTIFACT. This is chart = render(corpus.db): the plane's
// occupancy is DB-derived by render_v1_2_stratified.py, NOT hand-drawn. It is staged
// as a static SVG by scripts/stage-assets.mjs (single source of truth = gandalf's
// committed render; a re-render upstream flows through on the next push). The
// provenance stamp (source commit + generator) is git-derived at stage time and read
// from plane-provenance.json — never hand-typed.
//
// CONTRACT NOTE (v1.10 §7.7 render-adjacent addition): §7.7 rule 7 forbids HAND-derived
// occupancy on /atlas (that would recreate the dual-source-of-truth failure the page
// exists to prevent). This raster is DB-DERIVED (render(DB), same class as
// chart = render(atlas.json)), so it honors the provenance law. It is a static
// generated asset with a provenance stamp — a render/layout call. If a §2/§7.7 GRAMMAR
// question arises, that routes to jack-ryan via KR; embedding a provenance-stamped
// derived image does not touch the parse contract (zero new parse shapes).
//
// Phone-first: vector SVG scales to container width; a full-size link opens it
// standalone for pinch-zoom on the dense 3×7 stratified grid.
// ---------------------------------------------------------------------------
type PlaneProvenance = {
  asset: string; title: string; ruling: string; generator: string;
  source_path: string; source_commit: string; derivation: string; staged_at: string;
};

function AtlasPlaneView({ ghBase }: { ghBase: string }) {
  const [meta, setMeta] = useState<PlaneProvenance | null>(null);
  const [missing, setMissing] = useState(false);
  const base = import.meta.env.BASE_URL;
  const svgUrl = `${base}atlas/plane_view_v1_2_stratified.svg`;

  useEffect(() => {
    fetch(`${base}atlas/plane-provenance.json`, { cache: 'no-store' })
      .then((r) => (r.ok ? r.json() : Promise.reject(new Error(String(r.status)))))
      .then((m: PlaneProvenance) => setMeta(m))
      .catch(() => setMissing(true));
  }, [base]);

  // Fallback stamp values (known constants) if the provenance JSON is unavailable —
  // the asset is still the committed derived render; only the git-derived hash is absent.
  const m: PlaneProvenance = meta ?? {
    asset: svgUrl,
    title: 'RULED V1.2 Stratified Plane View',
    ruling: 'Q19 LOCKED 2026-07-13',
    generator: 'render_v1_2_stratified.py',
    source_path: 'agentic_orchestration/gandalf/views/v1-plane/plane_view_v1_2_stratified.svg',
    source_commit: '',
    derivation: 'render(corpus.db)',
    staged_at: '',
  };
  const shortSha = m.source_commit ? m.source_commit.slice(0, 8) : 'unknown';

  return (
    <section className="rounded-lg border-2 border-teal-700/60 bg-teal-950/20 p-3">
      <div className="mb-2 flex flex-wrap items-baseline justify-between gap-2">
        <div className="flex items-baseline gap-2">
          <span className="text-sm font-semibold text-teal-200">{m.title}</span>
          <span className="rounded bg-teal-800/60 px-1.5 py-0.5 text-[0.6rem] font-bold uppercase tracking-wide text-teal-200">
            {m.ruling}
          </span>
        </div>
        <a
          href={svgUrl} target="_blank" rel="noreferrer"
          className="text-xs text-sky-400 hover:text-sky-300">
          open full-size ↗
        </a>
      </div>

      <p className="mb-2 text-[0.7rem] leading-snug text-slate-400">
        The REALIZED atlas — 3 movement rows × 7 delivery columns × amp-tempo strata.
        <span className="ml-1 text-teal-300/90">
          DB-derived occupancy (<span className="font-mono">{m.derivation}</span>), not
          hand-drawn — honors the provenance law (§7.7 r7 forbids only hand-derived counts).
        </span>
      </p>

      {/* the vector plane — scales to container width; horizontal scroll guard for
          very narrow phones so nothing clips. */}
      <div className="overflow-x-auto rounded border border-slate-800 bg-slate-950/40">
        {missing ? (
          <div className="p-6 text-center text-xs text-slate-500">
            Plane asset not staged. Run <span className="font-mono">npm run stage-assets</span>{' '}
            (fires automatically in <span className="font-mono">npm run build</span>).
          </div>
        ) : (
          <img
            src={svgUrl}
            alt="RULED V1.2 Stratified Plane View — DB-derived occupancy atlas"
            className="mx-auto block h-auto w-full min-w-[640px] max-w-full"
            loading="lazy"
          />
        )}
      </div>

      {/* provenance stamp — the seeing-stone's answer: no true image without provenance. */}
      <div className="mt-2 flex flex-wrap items-center gap-x-2 gap-y-1 text-[0.65rem] text-slate-500">
        <span>RULED V1.2</span><span className="text-slate-700">·</span>
        <span className="text-teal-400/80">{m.ruling}</span><span className="text-slate-700">·</span>
        <span>generator <span className="font-mono text-slate-400">{m.generator}</span></span>
        <span className="text-slate-700">·</span>
        <span>source commit{' '}
          <a
            href={`${ghBase.replace(/\/blob\/[^/]+$/, '')}/commit/${m.source_commit}`}
            target="_blank" rel="noreferrer"
            className={m.source_commit ? 'font-mono text-sky-400 hover:text-sky-300' : 'font-mono text-slate-500'}>
            {shortSha}
          </a>
        </span>
      </div>
    </section>
  );
}

// §7.7 rule 4 — the TRIPLE-LAW cross-link banner. Each reference page links the OTHER
// TWO, labeled by layer. /atlas is the connective page (its two links are the most
// load-bearing) — rendered with the teal accent + a "the map" framing.
function TripleLawLinks({ refId }: { refId: ReferenceId }) {
  const siblings = TRIPLE_LAW_SIBLINGS[refId];
  const connective = refId === 'atlas';
  return (
    <section className={`rounded-lg border-2 p-3 ${
      connective ? 'border-teal-700/60 bg-teal-950/20' : 'border-slate-700/60 bg-slate-900/40'
    }`}>
      <div className="mb-2 flex items-center gap-2 text-xs font-semibold">
        <span className={connective ? 'text-teal-300' : 'text-slate-300'}>THE TRIPLE LAW</span>
        <span className="font-normal text-slate-500">
          {connective
            ? 'the connective PROJECTION — how the LATTICE and the CODEX map across each other'
            : 'read as one instrument — this layer links the other two'}
        </span>
      </div>
      <div className="grid grid-cols-1 gap-2 sm:grid-cols-2">
        {siblings.map((sid) => {
          const law = TRIPLE_LAW[sid];
          const sibConnective = sid === 'atlas';
          return (
            <button
              key={sid}
              onClick={() => go(law.page)}
              className={`flex items-center justify-between rounded-lg border px-3 py-2 text-left transition ${
                sibConnective
                  ? 'border-teal-700/50 bg-teal-950/20 hover:border-teal-500'
                  : 'border-slate-700 bg-slate-900/60 hover:border-slate-500'
              }`}>
              <span className="min-w-0">
                <span className="block font-semibold text-slate-100">{PAGE_LABEL[law.page]}</span>
                <span className="text-[0.7rem] text-slate-400">{law.role}</span>
              </span>
              <span className={`ml-2 shrink-0 rounded px-1.5 py-0.5 text-[0.6rem] font-bold uppercase tracking-wide ${
                sibConnective ? 'bg-teal-800/60 text-teal-200' : 'bg-slate-800 text-slate-400'
              }`}>
                {law.layer}
              </span>
            </button>
          );
        })}
      </div>
    </section>
  );
}

// §7.7 rule 3 — the QUIET-BY-DESIGN FLOW bar lead + per-stage `## §N` drill strip.
// The bar is phone-first navigation (tap → section scroll), NOT state: these are
// reference registers with no modeled rows, so every stage derives `quiet` neutral.
// That is correct; nothing invents coloring.
function ReferenceFlowLead({ reference, ghBase }: { reference: Reference; ghBase: string }) {
  const flow = reference.flow;
  if (!flow) {
    return (
      <section className="rounded-lg border border-slate-800 bg-slate-900/40 p-4 text-sm text-slate-500">
        This reference doc declares no <span className="font-mono">## FLOW</span> yet.
      </section>
    );
  }
  // map each FLOW stage's leading `§N` ref to its verbatim section (for in-page scroll).
  const secByRef = new Map(reference.sections.map((s) => [s.ref, s]));
  return (
    <section>
      <div className="mb-2 flex flex-wrap items-baseline justify-between gap-2">
        <h2 className="text-sm font-semibold text-slate-300">
          Reference map{' '}
          <span className="font-normal text-slate-500">(navigation — quiet bars by design, not state)</span>
        </h2>
        <a
          href={githubLink(ghBase, reference.path, flow.line)}
          target="_blank" rel="noreferrer"
          className="text-xs text-sky-400 hover:text-sky-300">
          FLOW source ↗
        </a>
      </div>

      {/* the FLOW bar — segments scroll to the per-stage `## §N` sections below */}
      <FlowBar
        flow={flow}
        onStage={(s) => {
          const el = document.getElementById(`ref-stage-${s.n}`);
          el?.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }}
      />

      {/* per-stage `## §N` drill targets — scroll in-page + deep-link to GitHub */}
      <ol className="mt-3 grid grid-cols-1 gap-1.5 sm:grid-cols-2">
        {flow.stages.map((s) => {
          const leadRef = s.refs[0];
          const sec = leadRef ? secByRef.get(leadRef) : undefined;
          const ghLine = s.heading_line ?? s.line;
          return (
            <li key={s.n}>
              <div className="flex items-stretch gap-1">
                <button
                  onClick={() => {
                    const el = document.getElementById(`ref-stage-${s.n}`);
                    el?.scrollIntoView({ behavior: 'smooth', block: 'start' });
                  }}
                  className="flex min-w-0 flex-1 items-start gap-2 rounded border border-slate-800 bg-slate-900/40 px-2 py-1.5 text-left text-xs hover:border-slate-600">
                  <span className={`mt-0.5 h-2.5 w-2.5 shrink-0 rounded-sm ${FLOW_SEGMENT_COLOR[s.dominant]}`} />
                  <span className="min-w-0">
                    <span className="block font-medium text-slate-200">{s.n}. {s.name}</span>
                    <span className="text-[0.65rem] text-slate-500">
                      {sec ? `${sec.ref} · jump to section` : (s.resolved ? 'section' : <span className="text-amber-400">⚠ ref — no `##` heading</span>)}
                    </span>
                  </span>
                </button>
                <a
                  href={githubLink(ghBase, reference.path, ghLine)}
                  target="_blank" rel="noreferrer"
                  title="open this section on GitHub"
                  className="flex shrink-0 items-center rounded border border-slate-800 bg-slate-900/40 px-1.5 text-[0.65rem] text-slate-500 hover:border-slate-600 hover:text-sky-300">
                  ↗
                </a>
              </div>
            </li>
          );
        })}
      </ol>
    </section>
  );
}

// §7.7 — the verbatim `## §N` payload sections. Each section's raw markdown body is
// rendered via SectionMd (display fidelity: tables → HTML tables, fences → <pre>,
// prose → paragraphs) — NEVER parsed into the state model. The section HEADING is the
// FLOW-stage drill target (id `ref-stage-N` matches by `§N` ref) + a GitHub deep-link.
function ReferenceSections({ reference, ghBase }: { reference: Reference; ghBase: string }) {
  // build ref → stage number so a section heading can carry the scroll anchor.
  const refToStageN = new Map<string, number>();
  for (const s of reference.flow?.stages ?? []) {
    if (s.refs[0]) refToStageN.set(s.refs[0], s.n);
  }
  return (
    <section className="space-y-4">
      {reference.sections.map((sec) => {
        const stageN = refToStageN.get(sec.ref);
        return (
          <div
            key={sec.heading_line}
            id={stageN != null ? `ref-stage-${stageN}` : undefined}
            className="scroll-mt-40 rounded-lg border border-slate-800 bg-slate-900/30 p-3">
            <a
              href={githubLink(ghBase, reference.path, sec.heading_line)}
              target="_blank" rel="noreferrer"
              className="mb-2 block text-sm font-semibold text-slate-200 hover:text-sky-300">
              {sec.title}
            </a>
            <div className="text-sm">
              <SectionMd src={sec.body} />
            </div>
          </div>
        );
      })}
    </section>
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
// section-name pin: the 31-DENOMINATOR roster is PART F's F.1 + F.2 sub-tables only.
// F.3 (the bench, B-series) is EXPLICITLY NOT in the 31 — it renders separately below.
function isPartFQueue(q: Queue): boolean {
  return /^F\.[12]\b/.test(q.title.trim());
}
// §7.5 v1.6 change #4 — the blocked/held bench: PART F's F.3 sub-table (rows B1–B13).
function isBenchQueue(q: Queue): boolean {
  return /^F\.3\b/.test(q.title.trim());
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
  const benchQueues = tracker.queues.filter(isBenchQueue);
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

      {/* §7.5 v1.6 change #4 — the F.3 blocked/held bench, BELOW F.2, under a visible
          divider making the "not in the 31" law loud. Absent-legal: no bench, no section. */}
      {benchQueues.length > 0 && (
        <KitBench queues={benchQueues} tracker={tracker} ghBase={ghBase} />
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

// §7.5 v1.6 change #4 — the F.3 blocked/held bench, rendered BELOW F.2 under a loud
// "NOT in the 31 denominator — promotes on unblock" divider. The bench uses the F.3
// authored columns: ID · kit · what-blocks · status · named re-entry. Its status is
// AUTHORED TEXT (BLOCKED / HELD / PENDING RE-CERT / LAUNCH-SCOPE) — those literals are
// not §2.3 status prefixes, so we render the authored status cell verbatim (faithful),
// not a parsed token. Row count is the bench size (13), explicitly NOT the 31.
function KitBench({ queues, tracker, ghBase }: { queues: Queue[]; tracker: Tracker; ghBase: string }) {
  const rows = queues.flatMap((q) => q.rows);
  return (
    <section className="rounded-lg border border-amber-800/40 bg-amber-950/10 p-3">
      {/* the divider — makes the "not in the 31" law loud (change #4 acceptance) */}
      <div className="mb-2 border-t-2 border-dashed border-amber-700/50 pt-2">
        <div className="flex flex-wrap items-baseline justify-between gap-2">
          <h2 className="text-sm font-bold text-amber-200">
            The bench <span className="font-normal text-amber-500/80">— blocked / held forms (PART F.3)</span>
          </h2>
          <span className="rounded bg-amber-900/40 px-1.5 py-0.5 text-[0.7rem] font-semibold text-amber-200">
            {rows.length} benched
          </span>
        </div>
        <p className="mt-1 text-[0.72rem] font-medium text-amber-300/90">
          NOT in the 31 denominator — promotes on unblock.
        </p>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full border-collapse text-left text-xs">
          <thead>
            <tr className="border-b border-amber-800/40 text-[0.7rem] uppercase tracking-wide text-amber-500/70">
              <th className="py-1 pr-2">ID</th>
              <th className="py-1 pr-2">ARPG Genre Canon kit</th>
              <th className="py-1 pr-2">What blocks / holds it</th>
              <th className="py-1 pr-2">Status</th>
              <th className="py-1 pr-2">Named re-entry</th>
            </tr>
          </thead>
          <tbody>
            {queues.map((q) =>
              q.rows.map((r) => <KitBenchRow key={r.id + r.line} row={r} tracker={tracker} ghBase={ghBase} />)
            )}
          </tbody>
        </table>
      </div>
    </section>
  );
}

function KitBenchRow({ row, tracker, ghBase }: { row: QueueRow; tracker: Tracker; ghBase: string }) {
  // F.3 authored columns: [ID, kit, what-blocks, status, named re-entry].
  const kit = row.cells_md[1] ?? '';
  const blocks = row.cells_md[2] ?? '';
  const statusText = row.cells_md[3] ?? '';
  const reentry = row.cells_md[4] ?? '';
  return (
    <tr className="border-b border-amber-900/30 align-top">
      <td className="py-1.5 pr-2">
        <a
          href={githubLink(ghBase, tracker.path, row.line)}
          target="_blank" rel="noreferrer"
          className="rounded bg-amber-900/40 px-1.5 py-0.5 font-mono text-amber-200 hover:bg-amber-800/60 hover:text-amber-100">
          {row.id}
        </a>
      </td>
      <td className="py-1.5 pr-2 text-slate-200"><InlineMd src={kit} /></td>
      <td className="py-1.5 pr-2 text-slate-400"><InlineMd src={blocks} /></td>
      <td className="py-1.5 pr-2">
        <span className="inline-flex items-center whitespace-nowrap rounded border border-amber-700 bg-amber-900/30 px-1.5 py-0.5 text-[0.68rem] text-amber-200">
          <InlineMd src={statusText} />
        </span>
      </td>
      <td className="py-1.5 pr-2 text-slate-400"><InlineMd src={reentry} /></td>
    </tr>
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

  // exclude ALL PART F sub-tables (roster F.1/F.2 + bench F.3) on the serial tracker —
  // they render on the /kits page, not as content-emission queues.
  const queues = tracker.id === 'serial-content-emission'
    ? tracker.queues.filter((q) => !isPartFQueue(q) && !isBenchQueue(q))
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
