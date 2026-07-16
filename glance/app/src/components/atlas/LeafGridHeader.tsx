// LeafGridHeader — the ONE shared header row per leaf block (D1-g core, D2-c grouping).
//
// Renders the column labels for the UNION leaf grid: build cols (Build/Family/Death-class)
// · axis cols grouped shared(5) → meso-only(2) → kit-only(9) · metric cols
// (Depth/Lit/Builds). Sticky at the top of a virtualized block so it stays visible while
// the ghost rows scroll.
//
// D2-c: a GROUPED super-header names the axis families (Shared · Ghost · Build) above the
// per-axis labels; each axis-header tint reads its grain (shared=sky, ghost/meso=violet,
// build/kit=amber). Column-header tooltips carry the DERIVED axis name + grain verbatim.

import { memo, type CSSProperties } from 'react';
import type { AtlasColumn, AxisGrain } from '../../utils/atlasColumns';

/** Per-grain header text tint (subtle; reads as a band). */
function grainTint(grain: AxisGrain | undefined): string {
  switch (grain) {
    case 'shared':
      return 'text-sky-400/70';
    case 'meso':
      return 'text-violet-300/70';
    case 'kit':
      return 'text-amber-300/70';
    default:
      return 'text-sky-400/70';
  }
}

/** The D2-c group label + tint for a column (used by the grouped super-header). */
function groupOf(col: AtlasColumn): { key: string; label: string; tint: string } {
  if (col.group === 'build') return { key: 'build-meta', label: 'Build', tint: 'text-gray-600' };
  if (col.group === 'metric') return { key: 'metric', label: 'Ghost metrics', tint: 'text-gray-600' };
  return {
    key: `axis-${col.axisGrain}`,
    label:
      col.axisGrain === 'shared'
        ? 'Shared axes'
        : col.axisGrain === 'meso'
          ? 'Ghost-only (meso)'
          : 'Build-only (14-axis key)',
    tint: grainTint(col.axisGrain),
  };
}

/**
 * v1.12: per-column super-header cells — the D2-c group label rides the FIRST column of
 * each contiguous group and is blank on the rest, so the super-header renders column-by-
 * column with the EXACT SAME widths as the per-column-label row + the body rows. This keeps
 * the header pixel-aligned with the (now fixed-width) name column with zero span-width math.
 */
function superHeaderCells(columns: AtlasColumn[]): { label: string; tint: string }[] {
  let prevKey: string | null = null;
  return columns.map((col) => {
    const g = groupOf(col);
    const first = g.key !== prevKey;
    prevKey = g.key;
    return { label: first ? g.label : '', tint: g.tint };
  });
}

/** v1.12: the shared per-column width style — fixedPx (name column, whole render) or the
 *  flex-basis share (all other columns). Identical logic to LeafRow so header+body align. */
function colWidthStyle(col: AtlasColumn, totalGrow: number): CSSProperties {
  return col.fixedPx != null
    ? { flex: `0 0 ${col.fixedPx}px`, width: col.fixedPx }
    : { flexBasis: `${(col.grow / totalGrow) * 100}%` };
}

function LeafGridHeaderImpl({
  columns,
  totalGrow,
  indent,
  minWidthPx,
}: {
  columns: AtlasColumn[];
  totalGrow: number;
  indent: number;
  minWidthPx: number;
}) {
  // v1.12: per-column super-header cells (group label on the first column of each group)
  // so both header rows share the body's exact per-column widths (incl. the fixed name col).
  const superCells = superHeaderCells(columns);
  return (
    <div
      style={{ minWidth: minWidthPx }}
      className="sticky top-0 z-10 border-b border-gray-800 bg-gray-950/95 backdrop-blur-sm"
    >
      {/* D2-c grouped super-header: axis-family labels above the per-column labels. */}
      <div
        style={{ paddingLeft: indent + 16 }}
        className="flex w-full items-center gap-2 pr-2 pt-1 font-mono text-[8px] uppercase tracking-widest"
      >
        <span className="h-1.5 w-1.5 shrink-0" />
        {columns.map((col, i) => {
          const isFixed = col.fixedPx != null;
          return (
            <span
              key={col.id}
              style={colWidthStyle(col, totalGrow)}
              className={[
                isFixed ? 'shrink-0 whitespace-nowrap' : 'min-w-0 shrink-0 truncate',
                superCells[i].tint,
              ].join(' ')}
              title={superCells[i].label || undefined}
            >
              {superCells[i].label}
            </span>
          );
        })}
      </div>
      {/* Per-column labels. */}
      <div
        style={{ paddingLeft: indent + 16 }}
        className="flex w-full items-center gap-2 py-1 pr-2 font-mono text-[9px] uppercase tracking-wider text-gray-500"
      >
        {/* Spacer matching the row's leading dot (h-1.5 w-1.5 + gap). */}
        <span className="h-1.5 w-1.5 shrink-0" />
        {columns.map((col) => {
          const isFixed = col.fixedPx != null;
          return (
            <span
              key={col.id}
              style={colWidthStyle(col, totalGrow)}
              className={[
                isFixed ? 'shrink-0 whitespace-nowrap' : 'min-w-0 shrink-0 truncate',
                col.numeric ? 'text-right' : '',
                col.group === 'axis' ? grainTint(col.axisGrain) : 'text-gray-500',
              ].join(' ')}
              // D2-c: tooltip carries the DERIVED axis name + grain verbatim.
              title={col.tooltip ?? col.label}
            >
              {col.label}
            </span>
          );
        })}
      </div>
    </div>
  );
}

export const LeafGridHeader = memo(LeafGridHeaderImpl);
