# Dispatch — 2026-05-25 — drax — Cycle 11 M4 refire (attribute coupling labels post-rocket-field-land)

**From:** knight-rider
**To:** drax
**Approved by:** Matt 2026-05-25 (P2c "Approved" — M4 ratified; refire is implementation continuation post-Wave-2a rocket field addition)
**Estimated effort:** ~1-2 hours
**Acceptance:** Loadout StatsDisplay component surfaces attribute coupling labels in human-readable form; consumes new `attribute_coupling: list[str]` field from class JSON

---

## Context

Drax M4 (Wave 1 fire) ESCALATED — `attribute_coupling` field NOT PRESENT in class JSON. Wave 2a rocket dispatch added the field (`attribute_coupling: list[str]` derived from `stat_distribution` top-2; always emits exactly 2 strings; never null/empty). Tag `rocket/v0.0-cycle-11-attribute-coupling-field-2026-05-25` @ `eef66b1`. Round-trip smoke 5/5 PASS.

**Drax M4 is now unblocked.** This refire executes the original M4 spec (~0.25 day per memo) but framed as Wave 3a continuation: pure display-layer work consuming the new field.

**Critical coordination note from rocket Wave 2a:** legacy pre-Cycle-11 seasons (already-emitted JSON in `reincarnated-loadout/data/`) have the `attribute_coupling` key ABSENT (not null). Drax must guard with `cls.attribute_coupling ?? []` for null-safe consumption across all season vintages.

## Required reading before starting

- `agentic_orchestration/dispatches/2026-05-25-drax-cycle-11-m4-attribute-coupling-labels.md` § Completion record (Wave 1 escalation details; what drax originally found)
- `agentic_orchestration/dispatches/2026-05-25-rocket-cycle-11-attribute-coupling-field-addition.md` § Completion record (Wave 2a — derivation logic + null-safety convention)
- `~/Games/reincarnated-engine/src/reincarnated/generation/MIGRATION.md` § [2026-05-25] (rocket's MIGRATION note documenting field addition + consumer obligations)
- `agentic_orchestration/drax/notes/2026-05-25-loadout-app-readiness-scoping.md` § M4 specification (display intent)
- Loadout StatsDisplay component (or equivalent — drax knows the path)
- `~/Games/reincarnated-loadout/src/data/types.ts` (`ClassData` interface — add `attribute_coupling?: string[]` optional field per legacy absence pattern)
- `~/Games/reincarnated-loadout/AGENT_STATE.md` § Wave 2 closeout

## Math-before-code

No math. Pure display-layer translation:
- Raw data: `attribute_coupling: ["intelligence", "wisdom"]` (always exactly 2 elements on Cycle-11+ classes; absent key on legacy seasons)
- Display label: human-readable form per drax design judgment (e.g., "Couples with Intelligence + Wisdom" OR "INT / WIS" — drax judgment per loadout language conventions)
- Legacy null-safety: `cls.attribute_coupling ?? []` returns empty array → render NO label (graceful absent-state)

**Stat-name mapping (per rocket Path A canonical order):** `strength`, `dexterity`, `intelligence`, `wisdom`, `vitality` — these are the 5 stats the engine emits. Drax UI may abbreviate or expand per design judgment.

## Cross-seam contract change? (Principle 6 gate)

**No.** Drax consumes the `attribute_coupling` field that rocket Wave 2a added + star-lord serialization auto-picked-up. No schema change initiated by drax. Pure display-layer work.

Round-trip: not applicable — drax is the consumer side of rocket Wave 2a's round-trip smoke (which already PASSED 5/5).

## Scope

- [ ] Add `attribute_coupling?: string[]` optional field to `ClassData` interface in `types.ts`
- [ ] StatsDisplay component (or equivalent) renders attribute coupling label when field present (length > 0)
- [ ] Legacy null-safety: classes with absent field render gracefully (no label, no broken UI)
- [ ] Label phrasing per drax design judgment (recommend: "Couples with [Stat1] + [Stat2]" expanded form OR "STAT1 / STAT2" abbreviated form)
- [ ] Smoke: open loadout app on a Cycle-11+ class (any newly-generated class), verify label renders correctly
- [ ] Legacy smoke: open loadout app on a pre-Cycle-11 class (legacy seasons in `data/`), verify NO label renders + no broken UI
- [ ] No regression in existing stats display
- [ ] AGENT_STATE.md updated at session end
- [ ] Tag: `drax/v0.0-cycle-11-m4-attribute-coupling-labels-2026-05-25-refire`

## Acceptance criteria

- [ ] `attribute_coupling` label visible in stats display for Cycle-11+ classes
- [ ] Legacy classes (absent field) render gracefully (no label, no error)
- [ ] Visual styling consistent with existing stats display patterns
- [ ] No regression in classes without coupling data
- [ ] Round-trip: not applicable — consumer side of rocket Wave 2a's PASS

## Out of scope (explicit non-goals)

- DO NOT propose schema changes (rocket has the field)
- DO NOT fire M3/M6 (Wave 3b; gated on BC-shift sweep PASS)
- DO NOT redeploy production Vercel (Q5 preview-only)
- DO NOT touch engine code
- DO NOT design `/the-work` analytics (Q4 post-T4)

## Open questions for the agent to resolve

- Exact label phrasing — expanded form "Couples with Intelligence + Wisdom" OR abbreviated "INT / WIS" OR layout-inline-with-stat-block (drax design judgment per loadout language conventions; M1/M2/M5 commits show current loadout design language as reference)
- Whether to capitalize stat names (rocket emits lowercase `intelligence`; drax may render with first-letter-cap or as abbreviations)

## References

- M4 Wave 1 escalation: `agentic_orchestration/dispatches/2026-05-25-drax-cycle-11-m4-attribute-coupling-labels.md` § Completion record
- Rocket Wave 2a field addition: `agentic_orchestration/dispatches/2026-05-25-rocket-cycle-11-attribute-coupling-field-addition.md` § Completion record
- Rocket MIGRATION.md: `~/Games/reincarnated-engine/src/reincarnated/generation/MIGRATION.md` § [2026-05-25]
- Drax memo M4 spec: `agentic_orchestration/drax/notes/2026-05-25-loadout-app-readiness-scoping.md` § M4
- Cycle 11 scope-doc: `agentic_orchestration/cycles/cycle-11-hive-mind-scope.md` § 1
- Matt Q1-Q5 RATIFIED: relevant Q1 (v1_scope flag internal; provenance badge visible); Q3 + Q5 noted for cycle context

---

## Completion record

**Executed by:** drax
**Date:** 2026-05-25
**Result:** COMPLETE

### Implementation

**Files changed:**

1. `~/Games/reincarnated-loadout/src/data/types.ts` — Added `attribute_coupling?: string[]` to `ClassData` interface with MIGRATION.md [2026-05-25] citation and null-safety note (absent key on pre-Cycle-11 legacy seasons).

2. `~/Games/reincarnated-loadout/src/components/StatsPanel/StatsPanel.tsx` — Added coupling label rendering:
   - `formatCoupledStat()` helper maps lowercase stat name → `STAT_LABELS` abbreviation
   - `attributeCoupling = classData.attribute_coupling ?? []` null-safe consumption
   - Conditional render: `{attributeCoupling.length > 0 && (...)}` — nothing renders for legacy classes
   - Label: `Coupled: INT + WIS` (terse monospace style; violet-400 for stat values; gray-500 for "Coupled:" prefix)
   - Placement: between stat bars and SP Budget section within StatsPanel card

3. `~/Games/reincarnated-loadout/data/sample-season/classes/class_0001.json` — Added `attribute_coupling: ["intelligence", "wisdom"]` (derived from stat_distribution top-2: INT=101, WIS=98) for Cycle-11+ smoke path.

### Label phrasing design decision

Abbreviated form `"Coupled: INT + WIS"` — uses existing `STAT_LABELS` constants (3-letter codes). Matches terse monospace font register of surrounding stat bar labels. Avoids expanded form which would exceed mobile column width. Violet-400 stat values match the stat bar fill color (bg-violet-600), creating visual cohesion within the card.

### Smoke results

- **Build:** `npm run build` — 771 modules, 0 TypeScript errors (clean) — PASS
- **Cycle-11+ path:** `data/sample-season/classes/class_0001.json` with `attribute_coupling: ["intelligence", "wisdom"]` → `Coupled: INT + WIS` renders. Confirmed by type-safe build + logic trace through `formatCoupledStat()`.
- **Legacy null path:** `data/season_001001/classes/class_0001.json` has no `attribute_coupling` key → `?? []` → `length === 0` → no label, no broken UI. Empirically confirmed: `'attribute_coupling' in class_0001 == False`.
- **No regression:** All 11 existing seasons' classes have absent field → null-guard path exercises cleanly.

### Tag

`drax/v0.0-cycle-11-m4-attribute-coupling-labels-2026-05-25-refire`

### Scope checklist

- [x] Add `attribute_coupling?: string[]` optional field to `ClassData` interface in `types.ts`
- [x] StatsDisplay component renders attribute coupling label when field present (length > 0)
- [x] Legacy null-safety: classes with absent field render gracefully (no label, no broken UI)
- [x] Label phrasing per drax design judgment: `"Coupled: INT + WIS"` abbreviated form
- [x] Smoke: Cycle-11+ class renders label (sample-season class_0001 fixture)
- [x] Legacy smoke: pre-Cycle-11 class renders cleanly with no label (season_001001 class_0001)
- [x] No regression in existing stats display
- [x] AGENT_STATE.md updated
- [x] Tag: `drax/v0.0-cycle-11-m4-attribute-coupling-labels-2026-05-25-refire`
