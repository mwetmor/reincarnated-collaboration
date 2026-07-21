// CorpusIndex — the browsable/filterable per-kit index (`#/corpus`).
//
// Reads public/kits/index.json (the thin browse list) and offers filter-by game / tier /
// grade + a free-text name filter, showing each kit's _row_counts density. Every row taps
// through to `#/corpus/<kit_id>` (the full detail page).
//
// This is the DISCOVERY surface for the per-kit "single source of truth" (spec:
// 2026-07-20-glance-per-kit-join-spec.md · drax deliverable). Static only — no DB, no
// server, no API (glance's founding law). The route name `corpus` (NOT `kits`) is
// deliberate: glance's `/kits` is already the PART-F serial roster; this is a distinct
// surface — every corpus row for one kit — so it gets its own name. Flagged for Matt.

import { useMemo, useState } from 'react';
import { useKitIndex } from '../hooks/useKits';
import {
  displayGame,
  gradeTone,
  rowCountTotal,
  type KitIndexRow,
} from '../data/kitTypes';

/** Navigate to a kit's detail route (hash-router; App.tsx parses `#/corpus/<id>`). */
export function goKit(id: string) {
  window.location.hash = `#/corpus/${encodeURIComponent(id)}`;
}

const ALL = '__all__';

function uniqueSorted(values: (string | null)[]): string[] {
  return Array.from(new Set(values.filter((v): v is string => !!v))).sort();
}

/** A compact density strip — the five _row_counts as labeled mini-badges. */
function DensityStrip({ row }: { row: KitIndexRow }) {
  const rc = row._row_counts;
  const cells: { k: string; label: string; n: number }[] = [
    { k: 'cit', label: 'cites', n: rc.citations },
    { k: 'dos', label: 'dossier', n: rc.dossier_facts },
    { k: 'ver', label: 'verify', n: rc.verify_claims },
    { k: 'mint', label: 'mints', n: rc.mints_anchored },
    { k: 'dock', label: 'dockets', n: rc.dockets },
  ];
  return (
    <div className="flex flex-wrap gap-1">
      {cells.map((c) => (
        <span
          key={c.k}
          title={`${c.n} ${c.label}`}
          className={`rounded px-1.5 py-0.5 text-[0.62rem] tabular-nums ${
            c.n > 0
              ? 'bg-slate-800 text-slate-300'
              : 'bg-slate-900 text-slate-600'
          }`}
        >
          {c.label} <span className="font-semibold">{c.n}</span>
        </span>
      ))}
    </div>
  );
}

function FilterSelect({
  label,
  value,
  options,
  onChange,
  render = (o) => o,
}: {
  label: string;
  value: string;
  options: string[];
  onChange: (v: string) => void;
  render?: (o: string) => string;
}) {
  return (
    <label className="flex flex-col gap-1">
      <span className="text-[0.62rem] uppercase tracking-wide text-slate-500">{label}</span>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="rounded border border-slate-700 bg-slate-900 px-2 py-1 text-xs text-slate-200 focus:border-sky-600 focus:outline-none"
      >
        <option value={ALL}>All</option>
        {options.map((o) => (
          <option key={o} value={o}>
            {render(o)}
          </option>
        ))}
      </select>
    </label>
  );
}

export function CorpusIndex() {
  const { index, provenance, status, error } = useKitIndex();

  const [game, setGame] = useState(ALL);
  const [tier, setTier] = useState(ALL);
  const [grade, setGrade] = useState(ALL);
  const [q, setQ] = useState('');

  const games = useMemo(() => uniqueSorted((index ?? []).map((r) => r.game)), [index]);
  const tiers = useMemo(() => uniqueSorted((index ?? []).map((r) => r.tier)), [index]);
  const grades = useMemo(() => uniqueSorted((index ?? []).map((r) => r.grade)), [index]);

  const filtered = useMemo(() => {
    const rows = index ?? [];
    const needle = q.trim().toLowerCase();
    return rows
      .filter((r) => game === ALL || r.game === game)
      .filter((r) => tier === ALL || r.tier === tier)
      .filter((r) => grade === ALL || r.grade === grade)
      .filter(
        (r) =>
          !needle ||
          r.kit_id.toLowerCase().includes(needle) ||
          (r.folk_name ?? '').toLowerCase().includes(needle),
      )
      .sort((a, b) => rowCountTotal(b._row_counts) - rowCountTotal(a._row_counts));
  }, [index, game, tier, grade, q]);

  if (status === 'loading' || status === 'idle') {
    return (
      <div className="flex items-center justify-center py-24">
        <div className="flex flex-col items-center gap-3">
          <div className="h-8 w-8 animate-spin rounded-full border-2 border-sky-500 border-t-transparent" />
          <p className="font-mono text-sm text-slate-500">Loading corpus index…</p>
        </div>
      </div>
    );
  }

  if (status === 'error' || !index) {
    return (
      <div className="mx-auto max-w-2xl rounded-lg border border-rose-800/50 bg-rose-950/20 p-6 text-sm text-rose-300">
        <p className="font-semibold">Corpus index failed to load.</p>
        <p className="mt-1 font-mono text-xs text-rose-400/80">{error ?? 'index.json missing'}</p>
        <p className="mt-3 text-xs text-slate-500">
          public/kits/index.json is staged at build time by scripts/stage-kits.mjs. If this
          is a preview, check that the staging step ran.
        </p>
      </div>
    );
  }

  const total = index.length;
  const shown = filtered.length;

  return (
    <div className="space-y-5">
      <div className="flex flex-wrap items-baseline justify-between gap-2">
        <div>
          <h1 className="text-xl font-bold text-slate-100">Kit corpus</h1>
          <p className="mt-0.5 text-xs text-slate-500">
            Every corpus row for one kit, on one page — the single source of truth
            (D-11 kit_master consolidation). Tap a kit for its full record.
          </p>
        </div>
        <span className="font-mono text-[0.7rem] text-slate-500">
          {shown === total ? `${total} kits` : `${shown} / ${total} kits`}
        </span>
      </div>

      {/* filter bar — game / tier / grade + free-text (kit_id or folk_name) */}
      <div className="flex flex-wrap items-end gap-3 rounded-lg border border-slate-800 bg-slate-900/40 p-3">
        <FilterSelect label="Game" value={game} options={games} onChange={setGame} render={displayGame} />
        <FilterSelect label="Tier" value={tier} options={tiers} onChange={setTier} />
        <FilterSelect label="Grade" value={grade} options={grades} onChange={setGrade} />
        <label className="flex min-w-[10rem] flex-1 flex-col gap-1">
          <span className="text-[0.62rem] uppercase tracking-wide text-slate-500">Search</span>
          <input
            value={q}
            onChange={(e) => setQ(e.target.value)}
            placeholder="kit id or folk name…"
            className="rounded border border-slate-700 bg-slate-900 px-2 py-1 text-xs text-slate-200 placeholder:text-slate-600 focus:border-sky-600 focus:outline-none"
          />
        </label>
        {(game !== ALL || tier !== ALL || grade !== ALL || q) && (
          <button
            onClick={() => {
              setGame(ALL);
              setTier(ALL);
              setGrade(ALL);
              setQ('');
            }}
            className="rounded border border-slate-700 bg-slate-900 px-2 py-1 text-xs text-slate-400 hover:border-slate-500 hover:text-slate-200"
          >
            clear
          </button>
        )}
      </div>

      {/* the kit list — one card per kit, tap-through to detail */}
      {shown === 0 ? (
        <div className="rounded-lg border border-slate-800 bg-slate-900/40 p-6 text-sm text-slate-500">
          No kits match these filters.
        </div>
      ) : (
        <ul className="grid grid-cols-1 gap-2 sm:grid-cols-2">
          {filtered.map((r) => (
            // min-w-0 on the grid cell + the button lets the truncating folk-name block
            // actually shrink (a flex/grid child defaults to min-width:auto, which would
            // otherwise let a long name force the track wider than the 375px viewport).
            <li key={r.kit_id} className="min-w-0">
              <button
                onClick={() => goKit(r.kit_id)}
                className="flex w-full min-w-0 flex-col gap-2 rounded-lg border border-slate-800 bg-slate-900/40 p-3 text-left transition hover:border-sky-700 hover:bg-slate-900"
              >
                <div className="flex w-full min-w-0 items-start justify-between gap-2">
                  <div className="min-w-0 flex-1">
                    <div className="truncate font-semibold text-slate-100">
                      {r.folk_name ?? <span className="text-slate-500">(unnamed)</span>}
                    </div>
                    <div className="truncate font-mono text-[0.68rem] text-slate-500">{r.kit_id}</div>
                  </div>
                  {r.grade && (
                    <span
                      className={`shrink-0 rounded border px-1.5 py-0.5 text-[0.6rem] font-bold uppercase ${gradeTone(
                        r.grade,
                      )}`}
                    >
                      {r.grade}
                    </span>
                  )}
                </div>
                <div className="flex flex-wrap items-center gap-1.5 text-[0.65rem] text-slate-400">
                  <span className="rounded bg-slate-800 px-1.5 py-0.5">{displayGame(r.game)}</span>
                  {r.tier && <span className="rounded bg-slate-800 px-1.5 py-0.5">{r.tier}</span>}
                  {r.terminal_state && (
                    <span className="rounded bg-slate-800 px-1.5 py-0.5">{r.terminal_state}</span>
                  )}
                </div>
                <DensityStrip row={r} />
              </button>
            </li>
          ))}
        </ul>
      )}

      {/* provenance footer — the git-derived source stamp (never hand-typed) */}
      {provenance && (
        <p className="pt-2 text-[0.65rem] text-slate-600">
          {provenance.source_mode === 'sample-5kit' && (
            <span className="mr-1 rounded bg-amber-950/40 px-1.5 py-0.5 font-semibold text-amber-400">
              SAMPLE
            </span>
          )}
          {provenance.kit_count} kits · derived {provenance.derivation} · source{' '}
          <span className="font-mono">{provenance.source_commit.slice(0, 8)}</span>
          {provenance.note ? ` · ${provenance.note}` : ''}
        </p>
      )}
    </div>
  );
}
