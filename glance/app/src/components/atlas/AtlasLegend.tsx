// AtlasLegend — basic legend, moved INSIDE the chart box (spec §4, §6, §9.6 D6-b).
//
// Four entries in D1-i community vocabulary: Build Families, Live Builds, Graveyard, Ghosts
// (the display strings live in LEGEND_ENTRIES; LegendClass ids + data keys stay internal).
// Multi-select. The selected Set drives the page-injected class-highlight CSS
// (atlasHighlight.buildHighlightCss) that targets the r7 SVG's data-el hooks:
// a stroke halo <= 0.75px, NO fill change, NO dimming of non-selected marks
// ("very slim, almost non-existent; dots never obscured"). (spec §3, §4; acc #32)
//
// D6-b (spec §9.6, Matt 2026-07-15): "the legend needs to be moved INTO the Atlas box
// (not above the Atlas itself)." The D1-a normal-flow band RETIRES (its "NEVER overlays
// the SVG" law is superseded by Matt's order). This component is an ABSOLUTELY POSITIONED
// overlay INSIDE the chart region.
//
// D6-b OCCLUSION LAW v2 (spec §9.6, gandalf verify-gate finding 2026-07-15 — SUPERSEDES
// the earlier corner-enumeration law; UNCHANGED by the v3 seat move — only the SEAT moves).
// The v1 bottom-LEFT placement passed every enumerated check (title / poles / key / dots)
// yet OCCLUDED the leading words of the in-artifact footer honesty block. Corner enumeration
// protects a LIST when the invariant is a CLASS. The v2 binding set: the overlay may
// intersect the screen-space bbox of NO in-artifact `<text>` node (±4px pad) and no drill-in
// dot — one rule over ALL text (title, poles, BUILD FAMILIES key, footer honesty block,
// points-denominator line, GHOST FIELD + graveyard annotations, all current and future).
// Non-binding for the translucent panel: ghost-lattice speckle + dashed boundary curves (a
// blurred backdrop over a segment of a long dashed curve leaves it inferable; text under a
// panel is information DESTROYED).
//
// PLACEMENT v3 (spec §9.6 D6-b; Matt 2026-07-16 verbatim: "the clickable legend should fit
// inside the box on the upper-left-hand side, opposite to the 'Condensations' box" [now
// renamed BUILD FAMILIES]). The seat moves BOTTOM-RIGHT → TOP-LEFT, the MIRROR of the
// top-right BUILD FAMILIES key. The seat was DERIVED BY PROBE against the post-R8 furniture
// geometry (drax B-2 top-left inspector, 5 widths × 2 skins), NOT assumed. The top-left
// interior landscape is stable in FRACTIONS across every width (region-proportional scaling):
//   - Plate TITLE BAND (title + subtitle + gloss + top ↑LAUNCH pole gloss) bottom ≈ 10.5%
//     region-height at wide widths, ≈ 11.1% at 375 (proportionally tallest at the narrow
//     region). The panel TOP must clear it (+4px pad). The title text is LEFT-anchored
//     (L≈9.5%), so — unlike the right side where the key sits high — a left-seated panel
//     CANNOT ride to the very top; it seats BELOW the band. This is the "opposite" seat's
//     real geometry (the key clears its top only because the title is on the left).
//   - Left-rail ROTATED titles ("you place the weapon…" gloss + "↑ DEPLOY") hug the left
//     edge but are VERTICALLY CENTERED (T≈40.7%–50.5%) — they do NOT reach the top-left
//     corner, so they bound the panel only from BELOW (the panel bottom must stay above
//     40.7%; trivially met by a short panel).
//   - First INTERIOR data text below the band: †d3-firebomb at L≈47.3%/T≈26.1% (near
//     center, far right of a narrow left panel) and †poe2-perfect-strike-01 at L≈23.4%/
//     T≈28.4% (the first LEFT-side interior column). The panel RIGHT edge must clear the
//     23.4% column; the panel BOTTOM must clear the first interior row in its own x-band.
// FRACTION-ANCHORED SEAT (load-bearing — the panel AND the plate text both scale with the
// region, so fractional insets/caps hold at every width):
//   - LEFT inset `left-2` (8px, the mirror of the old `right-2`). At 1280 (narrowest desktop)
//     the panel spans L≈0.7%–15.2% — clears the 23.4% interior column with margin.
//   - DESKTOP TOP `sm:top-[12%]`. Binding case is 1280 (the panel is proportionally TALLEST
//     there: ≈20% region-height): top 12% + 20% = bottom ≈32% clears the first below-band
//     interior row in the panel's x-band (†d2-impale-zon ≈32.6%) AND top 12% clears the band
//     bottom (10.6%) — the lawful desktop window is top ∈ (≈11.1%, ≈12.6%); 12% sits centered
//     in it. Probe-asserted 0 <text> hits at 2560/1920/1440/1280 × both skins.
//   - WIDTH CAP `sm:max-w-[14.5%]` (unchanged value; RE-DERIVED denominator). The old 14.5%
//     was derived against the bottom-right points-denominator tail (retired — that seat is
//     gone). The NEW binding denominator is the first LEFT-side interior column at L≈23.4%:
//     a left-anchored panel clears it iff panel-right < 23.4% − pad, i.e. width ≲ 22% region.
//     14.5% is well under that AND is exactly the fixed content's natural width at 1440
//     (measured 14.48%, no squeeze) — so 14.5% stays lawful and conservative on the new seat.
//
// A translucent plate-toned backdrop; `pointer-events` scoped so chart clicks pass
// everywhere OUTSIDE the legend's own bounds (the wrapper is pointer-events-none; the panel
// re-enables them).
//
// Mobile (375): same overlay, TOP-LEFT (v3), COLLAPSED-by-default (the parent passes
// `defaultCollapsed`) — a compact toggle chip that expands to the full legend. The chip's
// size is UNCHANGED by the seat move (a11y touch-target invariant is never shrunk — only the
// seat relocates). The 375 chip seat is RE-DERIVED: `top-[15%]` is the ONE lawful top-left
// chip seat at 375. The % is load-bearing — the band bottom is proportionally TALLEST at 375
// (11.1%), so the chip must seat LOWER than the desktop 12% to clear it (+4px pad ≈ 1.75% at
// 375), while its bottom (15% + ≈11% chip height ≈ 26%) still clears the first below-band
// interior column (†poe2-perfect-strike-01 at T≈28.4%). Probe-asserted 0 <text> hits at 375
// × both skins. (If no lawful top-left chip seat existed at 375 → HALT-don't-shrink; one does.)

import { useState } from 'react';
import type { LegendClass } from '../../data/atlasTypes';
import { LEGEND_ENTRIES } from '../../data/atlasTypes';

interface AtlasLegendProps {
  /** Currently multi-selected classes. */
  selected: Set<LegendClass>;
  onToggle: (id: LegendClass) => void;
  /** Canvas the chart is on — drives swatch/backdrop contrast (dark vs light). */
  canvas: 'light' | 'dark';
  /**
   * Start collapsed (mobile 375 — the expanded legend would cover >25% of the region).
   * The user can still expand it; the collapse is only the initial state per breakpoint.
   */
  defaultCollapsed?: boolean;
}

export function AtlasLegend({ selected, onToggle, canvas, defaultCollapsed = false }: AtlasLegendProps) {
  const dark = canvas === 'dark';
  // Collapsed state — initialized per breakpoint (mobile starts collapsed). Keyed on
  // defaultCollapsed so a viewport change across the breakpoint re-seeds the initial state.
  const [expanded, setExpanded] = useState(!defaultCollapsed);

  // Translucent PLATE-TONED backdrop (§9.6 D6-b): dark canvas → dark glass; light → light
  // glass. Kept fairly opaque (/80 dark, /90 light) so whatever plate texture sits behind
  // the panel (ghost-lattice speckle / a dashed-curve segment — both NON-binding under the
  // v2 law) doesn't bleed through and read muddy, while still reading as an overlay ON the
  // plate. Under v2 the panel intersects NO in-artifact <text> bbox (the binding invariant),
  // so opacity is purely a legibility choice over non-text texture, not an occlusion crutch.
  const panelTone = dark
    ? 'border-white/10 bg-black/80 text-gray-200'
    : 'border-black/10 bg-white/90 text-gray-800';

  return (
    // WRAPPER (v3): absolutely positioned in the TOP-LEFT of the chart REGION (the region is
    // `relative`), per the D6-b v2 law + Matt's "upper-left, opposite the BUILD FAMILIES key"
    // order. pointer-events-none so chart clicks pass THROUGH the empty wrapper area (§9.6
    // D6-b) — only the panel/chip below re-enables pointer events on its own bounds.
    // `justify-start` left-aligns the inner panel/chip so it grows RIGHTWARD from the region's
    // left edge (the mirror of the old `justify-end`).
    //
    // WIDTH CAP — `sm:max-w-[14.5%]` of the REGION, NOT a fixed px, load-bearing. RE-DERIVED
    // denominator for the top-left seat (the old bottom-right points-denominator tail is
    // retired with that seat): the first LEFT-side interior data column sits at L≈23.4% region
    // (probe, all widths), so a LEFT-anchored panel clears it (±4px pad) iff its width ≲ 22%
    // region. 14.5% is well under that AND is exactly the fixed content's natural width at 1440
    // (measured 14.48%, no squeeze). Both the panel's left inset AND that interior column are
    // fixed FRACTIONS of the region, so a fractional cap holds at EVERY desktop width. Probe-
    // asserted 0 text hits at 2560/1920/1440/1280.
    //
    // VERTICAL — desktop `sm:top-[12%]` seats the panel just below the plate title band (band
    // bottom ≈10.6% at wide widths). Binding case 1280: the panel is proportionally TALLEST
    // there (≈20% region-height), so top 12% + 20% = bottom ≈32% must clear the first below-
    // band interior row in the panel's x-band (†d2-impale-zon ≈32.6%) — the lawful desktop
    // window is top ∈ (≈11.1%, ≈12.6%); 12% centers it. MOBILE `top-[15%]` is the ONE lawful
    // top-left chip seat at 375: the title band is proportionally TALLEST there (11.1%), so the
    // chip must seat LOWER than the desktop 12% to clear it (+4px pad ≈1.75% at 375), while its
    // bottom (15% + ≈11% chip ≈26%) still clears the first below-band interior column
    // (†poe2-perfect-strike-01 at T≈28.4%). Chip SIZE unchanged from the bottom-right seat
    // (a11y touch-target invariant never shrunk — only the seat moved). No shrink, no drop,
    // no scroll; probe-asserted 0 text hits at 375 × both skins. (Eyes-verify.)
    <div className="pointer-events-none absolute top-[15%] left-2 z-10 flex max-w-[45%] justify-start sm:top-[12%] sm:max-w-[14.5%]">
      {expanded ? (
        <div
          className={[
            'pointer-events-auto inline-flex flex-col gap-1 rounded-lg border p-2 shadow-lg backdrop-blur-md',
            panelTone,
          ].join(' ')}
        >
          <div
            className={[
              'mb-0.5 flex items-center justify-between gap-2 text-[10px] font-mono uppercase tracking-wider',
              dark ? 'text-gray-400' : 'text-gray-500',
            ].join(' ')}
          >
            <span className="flex items-center gap-1.5">
              Legend
              {selected.size > 0 && (
                <span className={dark ? 'text-indigo-300' : 'text-indigo-600'}>
                  {selected.size} on
                </span>
              )}
            </span>
            {/* Collapse control — lets a mobile user re-hide, and a desktop user tuck it
                away if it ever crowds a mark they're inspecting. */}
            <button
              onClick={() => setExpanded(false)}
              aria-label="Collapse legend"
              className={[
                'rounded px-1 leading-none',
                dark ? 'text-gray-500 hover:text-gray-300' : 'text-gray-400 hover:text-gray-600',
              ].join(' ')}
            >
              −
            </button>
          </div>
          {LEGEND_ENTRIES.map((e) => {
            const on = selected.has(e.id);
            return (
              <button
                key={e.id}
                onClick={() => onToggle(e.id)}
                title={e.hint}
                aria-pressed={on}
                className={[
                  'group flex items-center gap-2 rounded px-1.5 py-1 text-left text-[11px] font-mono transition-colors',
                  on
                    ? dark
                      ? 'bg-white/10 ring-1 ring-inset ring-indigo-400/60'
                      : 'bg-black/5 ring-1 ring-inset ring-indigo-500/50'
                    : dark
                      ? 'hover:bg-white/5'
                      : 'hover:bg-black/5',
                ].join(' ')}
              >
                <span
                  className={[
                    'h-2.5 w-2.5 shrink-0 rounded-full',
                    e.swatch,
                    on ? 'opacity-100' : 'opacity-50',
                  ].join(' ')}
                />
                <span className={dark ? 'text-gray-200' : 'text-gray-800'}>{e.label}</span>
              </button>
            );
          })}
          <p
            className={[
              'mt-0.5 max-w-[180px] text-[9px] leading-tight',
              dark ? 'text-gray-600' : 'text-gray-400',
            ].join(' ')}
          >
            Toggle to halo a class. Slim stroke only — dots never obscured.
          </p>
        </div>
      ) : (
        // COLLAPSED chip — a compact toggle that reveals the full legend. Same plate-toned
        // glass; the "N on" badge keeps active state visible while collapsed.
        <button
          onClick={() => setExpanded(true)}
          aria-label="Expand legend"
          aria-expanded={false}
          className={[
            'pointer-events-auto inline-flex items-center gap-1.5 rounded-lg border px-2 py-1 text-[10px] font-mono uppercase tracking-wider shadow-lg backdrop-blur-md',
            panelTone,
          ].join(' ')}
        >
          <span
            className={[
              'h-2 w-2 rounded-full',
              dark ? 'bg-indigo-400/70' : 'bg-indigo-500/70',
            ].join(' ')}
          />
          Legend
          {selected.size > 0 && (
            <span className={dark ? 'text-indigo-300' : 'text-indigo-600'}>{selected.size} on</span>
          )}
        </button>
      )}
    </div>
  );
}
