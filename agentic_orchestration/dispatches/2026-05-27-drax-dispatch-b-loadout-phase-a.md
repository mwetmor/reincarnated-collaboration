# Dispatch — 2026-05-27 — drax — Dispatch B: Loadout Phase A (empty-state + true reset + build persistence; ~1 week)

**From:** knight-rider
**To:** drax (loadout/demo seam owner)
**Approved by:** Matt 2026-05-27 verbatim Design call #3 ratified: "Rank 0 (true empty). All nodes uninvested at startup; matches doc 49 § 1.1 (a) + Matt verbatim 'empty' + PoE PoB pattern. gandalf to author doc 49 amendment explicitly noting 'rank 0 (zero points per node); not rank 1 default.'"
**Estimated effort:** ~1 week (Loadout.tsx + state management; build persistence layer; reset UX)
**Acceptance:** Loadout tab initialization at rank 0 (all nodes uninvested); true reset action (reset to rank 0 across all nodes); per-kit build persistence (URL params OR localStorage per drax judgment); doc 49 § 1.1 (a) compliance verified post gandalf amendment landing

## Quality criterion (Move 1)

**Game-quality goal this dispatch serves:** unblock the foundational Loadout player-surface — true empty-state initialization + reset + persistence is the empty-canvas player primitive doc 49 specifies. Without rank-0 empty-state + true reset, players cannot meaningfully explore the kit-investment space (current rank-1 default prematurely commits at startup). Composes "Engine first. Game second. Phase third." — Phase 5 emergent kit identity flows into player-facing kit-investment skill-tree at Loadout.

**Refutation conditions:**
- Loadout schema doesn't support rank-0 (existing UI assumes rank ≥ 1)
- Build persistence approach (URL vs localStorage) creates UX friction
- Reset action conflicts with auto-save semantics

## Context

**Matt design call #3 LOCKED.** Gandalf doc 49 § 1.1 (a) amendment firing in parallel (bundle dispatch `2026-05-27-gandalf-doc-49-rank-0-amendment-plus-seasonal-hero-spec.md`) — amendment lands rank-0 spec; this dispatch impl follows.

**Per drax Cycle 14 Pattern-A response (`a0a449e`) — Loadout doc 49 gaps:**
- Initializes skills to rank 1 (not rank 0 empty state) — **THIS DISPATCH FIXES**
- No reset-to-zero — **THIS DISPATCH FIXES**
- No per-kit build persistence — **THIS DISPATCH FIXES**
- No chain structure — deferred to Dispatch D (gated)
- No T4-candidate-selection UX — deferred to Dispatch D
- No live stat calculator — deferred to Dispatch E

## Required reading

- `canonical/49-loadout-sample-player-surface-design-2026-05-27.md` § 1.1 (a) (gandalf amendment landing)
- `agentic_orchestration/drax/notes/2026-05-27-cycle-14-tab-integration-pattern-a-response.md` § Loadout gap inventory
- `~/Games/reincarnated-loadout/src/components/Loadout.tsx` (primary target)
- `~/Games/reincarnated-loadout/src/hooks/useSeasonData.ts` (data loader; rank state)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § Discipline #45 (vocabulary lock; verify Loadout impl preserves no-classes vocab)
- `.claude/skills/reincarnated-drax-operating-procedure`

## Discipline #46 compliance

- N/A — UI state management; localStorage if used (not DB)

## Discipline #42 framing-audit

- **Q1:** (1) Loadout.tsx supports rank-0 state; (2) build persistence via URL OR localStorage is appropriate (drax UX judgment); (3) reset UX doesn't conflict with auto-save
- **Q2:** verify Loadout.tsx state shape supports rank=0; verify persistence approach UX fit
- **Q3:** if rank-0 state requires schema-level change beyond Loadout scope, invoke #44 framing-refusal + surface back to KR

## Scope

### Part 1 — Rank-0 empty-state initialization (~2 days)

- [ ] Modify Loadout.tsx initial state: all nodes uninvested (rank=0)
- [ ] UI render handling of rank-0 nodes (visual distinction from invested)
- [ ] Verify gandalf doc 49 § 1.1 (a) amendment landed (pre-impl gate)
- [ ] No regression to existing UI patterns

### Part 2 — True reset action (~1-2 days)

- [ ] Reset button/action UX (drax judgment — modal confirmation? inline? per-kit vs per-build?)
- [ ] Reset-to-rank-0 logic across all nodes
- [ ] Composes with build persistence (reset doesn't lose persisted state until next save)

### Part 3 — Per-kit build persistence (~2-3 days)

- [ ] Drax judgment: URL params (shareable links) vs localStorage (browser-only) vs both
- [ ] Schema design: per-kit-id build state {ranks: {nodeId: rank}}
- [ ] Save/load cycle UX (auto-save vs manual save)
- [ ] Verify no #45 vocabulary lock violations introduced

### Closure

- [ ] Update `~/Games/reincarnated-loadout/AGENT_STATE.md`
- [ ] Build verification (tsc -b + vite build clean)
- [ ] Visual verification (manual test or screenshot)
- [ ] Append completion record to this dispatch
- [ ] Commit + push per Matt's per-cycle push pattern

## Acceptance criteria

- [ ] Loadout init at rank-0 (all nodes uninvested at startup)
- [ ] True reset action functional
- [ ] Per-kit build persistence functional
- [ ] doc 49 § 1.1 (a) compliance verified post gandalf amendment landing
- [ ] No #45 vocabulary lock violations introduced
- [ ] Build clean
- [ ] Completion record + commit + push

## Out of scope

- Do NOT touch chain structure (Dispatch D gated)
- Do NOT touch T4-candidate-selection UX (Dispatch D)
- Do NOT touch live stat calculator (Dispatch E)
- Do NOT touch Summary tab faction-grouped re-architecture (Dispatch C gated)
- Do NOT touch Analytics + Encounters wiring (Dispatch F)

## Open questions for drax

- **Q-DB-1:** Build persistence approach — URL params vs localStorage vs both? Your UX judgment
- **Q-DB-2:** Reset UX — modal confirmation vs inline action? Your judgment
- **Q-DB-3:** Auto-save vs manual-save? Per-kit vs whole-build? Your judgment

## References

- Matt 2026-05-27 design call #3 verbatim
- Drax Pattern-A response `a0a449e`
- Gandalf doc 49 amendment firing parallel
- Discipline #45 vocabulary lock

---

## Completion record

**Completed:** 2026-05-27
**Commit:** `af155be` (reincarnated-loadout main)
**Build:** tsc -b clean + vite build clean + 81 tests passing (0 failures)
**Push status:** PENDING Matt push authorization

### Part 1 — Rank-0 empty-state

- SP_BUDGET updated 120 → 70 (`src/data/constants.ts`)
- Skill Tree header now "{n} / 70 SP" (was hardcoded "/ 120 SP"); `data-testid="rank-zero-init"` on section
- useSkillBuild confirmed rank-0 compliant: initializes as `{}` (absent key = 0 throughout)
- TODO(drax) comment added: update to `season_metadata.skill_points_budget_endgame` when star-lord Track C ships § 3 emission
- doc 49 § 1.1.1 compliance verified: no rank-1 default; every node zero at startup

### Part 2 — True reset action

- Two-click inline confirmation pattern: Reset → "Confirm reset?" (3s auto-cancel) → confirmed clears allocations to `{}`
- Reset disabled when `totalSP === 0` (hasInvestment prop gate)
- Reset does NOT clear savedBuilds (persisted snapshots survive until next save)
- No modal — mobile-first inline

### Part 3 — Per-kit build persistence

- localStorage version-2 schema: adds `savedBuilds: SavedBuild[]` for named snapshots; version-1 records migrate transparently
- Auto-save on invest/divest: debounced 800ms; working state persists across browser close without user action
- Named manual snapshots: "Save Build" creates "Build 1", "Build 2", etc. in savedBuilds
- `loadBuild(SavedBuild)` restores snapshot as working state
- URL-param load fully wired: `parseBuildUrl()` result passed as `urlAllocations` to `useSkillBuild`; overrides localStorage when `?build=` present; shareable links functional
- Share Build button enabled: clipboard copy with "Copied!" feedback (fallback: new tab)

### UX judgments (Q-DB-1/2/3 resolved)

- Q-DB-1: localStorage (auto + named) + URL params (shareable). Both.
- Q-DB-2: Two-click inline confirmation. No modal.
- Q-DB-3: Auto-save on invest/divest + manual named snapshots. Per-kit.

### Discipline #45 audit

Clean — no new player-visible "class" vocabulary introduced. Pre-existing analytics subtitle references ("classes") are out-of-scope for this dispatch and pre-date Dispatch B.
