import {
  type QueueRow, type GatesOn, type StatusToken,
  STATUS_LABEL, STATUS_SYMBOL, STATUS_COLOR, githubLink,
} from './state';
import { InlineMd } from './md';

export function StatusChip({ token }: { token: StatusToken }) {
  const c = STATUS_COLOR[token];
  return (
    <span className={`inline-flex items-center gap-1 whitespace-nowrap rounded border px-1.5 py-0.5 text-[0.7rem] font-medium ${c.chip}`}>
      <span aria-hidden>{STATUS_SYMBOL[token]}</span>
      {STATUS_LABEL[token]}
    </span>
  );
}

export function GatesBadge({ g }: { g: GatesOn }) {
  if (g.dangling) {
    return (
      <span
        title="Dangling: this gates-on token resolves to no row (visible debt, not a build failure)"
        className="inline-flex items-center gap-1 rounded border border-amber-700 bg-amber-900/30 px-1.5 py-0.5 text-[0.7rem] text-amber-300">
        ⚠ gates-on {g.token}{g.qualifier ? ` (${g.qualifier})` : ''}
      </span>
    );
  }
  return (
    <span
      title={g.resolved ? 'Gate closed (the row it depends on is ✓)' : 'Gate open (waiting on its dependency)'}
      className={`inline-flex items-center gap-1 rounded border px-1.5 py-0.5 text-[0.7rem] ${
        g.resolved
          ? 'border-emerald-800 bg-emerald-900/20 text-emerald-400'
          : 'border-slate-700 bg-slate-800/60 text-slate-400'
      }`}>
      {g.resolved ? '✓' : '⤷'} gates-on {g.token}{g.qualifier ? ` (${g.qualifier})` : ''}
    </span>
  );
}

// A single queue row rendered for the drill table (Tier 1).
export function RowLine({
  row, ghBase, path,
}: { row: QueueRow; ghBase: string; path: string }) {
  // The descriptive cell: prefer the last non-id cell, else the id cell prose.
  const desc =
    row.cells_md.length > 1
      ? row.cells_md.slice(1).join('  ·  ')
      : row.status.prose || row.cells_md[0];
  return (
    <div className="border-t border-slate-800 py-2 first:border-t-0">
      <div className="flex flex-wrap items-center gap-2">
        <a
          href={githubLink(ghBase, path, row.line)}
          target="_blank" rel="noreferrer"
          title={`${path}#L${row.line} — open on GitHub`}
          className="rounded bg-slate-800 px-1.5 py-0.5 font-mono text-xs text-slate-300 hover:bg-slate-700 hover:text-sky-300">
          {row.id}
        </a>
        <StatusChip token={row.status.token} />
        {row.owner && (
          <span className="rounded bg-slate-800/60 px-1.5 py-0.5 text-[0.7rem] text-slate-400">
            @{row.owner}
          </span>
        )}
        {row.gates_on.map((g, i) => <GatesBadge key={i} g={g} />)}
      </div>
      <div className="mt-1 text-sm text-slate-300">
        <InlineMd src={desc} />
      </div>
    </div>
  );
}
