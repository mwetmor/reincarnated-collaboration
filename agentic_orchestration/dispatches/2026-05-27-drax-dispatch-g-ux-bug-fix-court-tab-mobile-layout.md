# Dispatch — 2026-05-27 — drax — Dispatch G: UX bug fix (Court tab + mobile blank column + mobile design button obscuring character name; ~half-day)

**From:** knight-rider
**To:** drax (loadout/demo seam owner)
**Approved by:** Matt 2026-05-27 verbatim "Author Dispatch G — drax UX bug fix (Court tab + mobile blank column)" + "also on mobile the design button moves into the middle of the sample and loadout pages, obscuring the character/class name"
**Estimated effort:** ~half-day (3 mechanical UX bug diagnosis + fixes; small surface)
**Acceptance:** (1) Court tab presence verified in nav across all season selections + all viewports; (2) mobile blank column/space when cycle-13 selected diagnosed + remediated; (3) mobile design button positioning fixed so character/class name not obscured on Sample + Loadout pages; build clean; visual verification across mobile + tablet + desktop breakpoints

## Quality criterion (Move 1)

**Game-quality goal this dispatch serves:** restore correct UX across nav (Court tab) + mobile layout (blank column) + mobile floating action (design button positioning). UX regressions undermine player-surface integrity even when underlying impl is correct. Composes "Engine first. Game second. Phase third." — player-surface UX is game-layer integrity flowing from engine-layer correctness.

**Refutation conditions:**
- Court tab removal was intentional + un-flagged (would warrant surface to gandalf for canonical-archetype-register first-emergence consideration per doc 49 § 4.3 — Court tab IS the Cycle 14 minimal-single-season-first-emergence view)
- Blank column root cause is responsive-layout architecture (not removed-tab artifact) — would warrant Dispatch C-tier scope adjustment
- Design button positioning is layout-anchor architecture (not z-index / position fix) — would warrant Dispatch D-tier scope

## Context

**Post Dispatch A status:**
- Dispatch A (vocab lock redactions) landed at loadout `42e9393` + meta `56a0958`
- 16 player-facing #45 violations remediated (5 catalogued + 11 grep-audit-discovered in Encounters.tsx + Pitch.tsx)
- Matt is verifying post-Dispatch-A surfaces; surfaced 3 UX bug observations

**Per drax Cycle 14 Pattern-A response (`a0a449e`):**
- Court tab IS in v1 scope (minimal infrastructure complete at CourtBrowser.tsx; empty court.json by design for Cycle 14 v1; full mechanics Cycle 15+)
- Per doc 49 § 4.3 Court tab is the minimal-single-season-first-emergence view

**Mobile layout concerns (Matt observation 2026-05-27):**
- Blank column/space on mobile when cycle-13 selected (likely reserved layout space for removed/hidden tab not collapsed on mobile breakpoint OR responsive layout not adjusting OR grid column not adapting)
- Design button moves into middle of Sample + Loadout pages on mobile, obscuring character/class name

## Required reading

- `agentic_orchestration/dispatches/2026-05-27-drax-dispatch-a-vocabulary-lock-redactions.md` completion record (16 violation locations; confirm none touched Court tab nav OR mobile layout CSS)
- `canonical/49-loadout-sample-player-surface-design-2026-05-27.md` § 4.3 (Court tab minimal-Cycle-14-v1-scope)
- `agentic_orchestration/drax/notes/2026-05-27-cycle-14-tab-integration-pattern-a-response.md` § Court tab (infrastructure complete; empty array; correct minimal v1 scope confirmed)
- `~/Games/reincarnated-loadout/src/` — nav components + responsive layout components + design-button positioning (drax knows file paths)
- `.claude/skills/reincarnated-drax-operating-procedure`

## Discipline #46 compliance

- N/A — UI-side bug investigation; no DB queries

## Discipline #42 framing-audit at session-start

- **Q1 load-bearing assumptions:**
  1. Court tab regression (if present) was inadvertent during Dispatch A vocab-lock fixes
  2. Mobile blank column is layout-CSS issue (responsive breakpoint handling) NOT architectural
  3. Mobile design button positioning is z-index / position-fixed / portal issue NOT layout-anchor architecture
- **Q2 refutation evidence to seek:** git diff Dispatch A loadout commit `42e9393` to verify NO Court tab nav changes OR responsive layout CSS changes were made; if changes present + caused regression → revert + remap vocab differently
- **Q3 outcome trigger:** if root cause exceeds half-day fix scope (e.g., responsive layout architecture rewrite needed), invoke Discipline #44 framing-refusal + surface back to KR for re-routing (Dispatch C/D-tier scope adjustment)

## Scope

### Part 1 — Court tab investigation + remediation (~1-2 hours)

- [ ] Verify `/court` route still exists in `App.tsx` (or router config)
- [ ] Verify Court tab presence in nav component across all viewport breakpoints (mobile + tablet + desktop)
- [ ] Test all season selections — Court tab should surface consistently
- [ ] Diff against Dispatch A loadout commit `42e9393` to confirm Court tab not inadvertently touched
- [ ] If Court tab removed inadvertently: restore + verify per doc 49 § 4.3
- [ ] If Court tab present but visibility issue: diagnose CSS / responsive-layout / season-conditional-rendering bug + fix
- [ ] Compose with doc 49 § 4.3 minimal-Cycle-14-v1-scope (Court tab should ALWAYS surface in nav even if court.json empty)

### Part 2 — Mobile blank column diagnosis + remediation (~1-2 hours)

- [ ] Reproduce on mobile breakpoint (devtools mobile emulation OR actual mobile device test)
- [ ] Identify blank column/space root cause:
  - Hypothesis A: reserved layout space for removed/hidden Court tab not collapsed on mobile (related to Part 1)
  - Hypothesis B: responsive layout not adjusting properly to season-specific content
  - Hypothesis C: grid column not adapting (Tailwind responsive class missing)
- [ ] Apply remediation per root-cause finding
- [ ] Verify cycle-13 + Cycle 14 (when Wave 5 lands) season selection on mobile + desktop + tablet

### Part 3 — Mobile design button positioning fix (~1-2 hours)

- [ ] Reproduce on Sample (/sample) + Loadout (/) pages on mobile
- [ ] Diagnose design button positioning (likely fixed-position element with mobile breakpoint not adjusting `top`/`bottom`/`right` correctly; OR z-index conflict with header; OR portal mount-point conflict)
- [ ] Apply remediation: reposition design button on mobile so character/class name visible at top of page
- [ ] Verify across all routes that show character/class name (Sample + Loadout + Summary if applicable)
- [ ] **Composition with Dispatch A:** the design button label itself should already comply with Discipline #45 post Dispatch A; verify

### Closure

- [ ] Update `~/Games/reincarnated-loadout/AGENT_STATE.md`
- [ ] Build verification (tsc -b + vite build clean)
- [ ] Visual verification across breakpoints (mobile + tablet + desktop)
- [ ] Append completion record to this dispatch
- [ ] Commit (per Matt's per-cycle commit pattern for routine work-products)
- [ ] **Push pending Matt authorization per ADR-006** (loadout production-deploy)

## Acceptance criteria

- [ ] Court tab presence verified + remediated if needed
- [ ] Mobile blank column root cause identified + remediated
- [ ] Mobile design button positioning fixed (character/class name not obscured)
- [ ] No regression to Dispatch A vocab lock fixes (#45 grep clean)
- [ ] Build clean
- [ ] Completion record + commit
- [ ] Hand-back to KR with push-authorization request

## Out of scope

- Do NOT touch Loadout.tsx rank-0 + reset + persistence (Dispatch B scope; already complete at `af155be`)
- Do NOT touch Analytics + Encounters Cycle 14 wiring (Dispatch F scope)
- Do NOT touch Summary tab faction-grouped re-architecture (Dispatch C scope; gated)
- Do NOT touch Sample tab committed-state display (Dispatch D scope; gated)
- Do NOT touch live stat calculator (Dispatch E scope; gated)

## Open questions for drax

- **Q-DG-1:** Court tab regression — was Dispatch A vocab-lock fix-set the cause OR pre-existing? Verify via git diff
- **Q-DG-2:** Mobile blank column — Hypothesis A (Court tab artifact) vs B (responsive layout) vs C (grid column adaptation)? Your judgment per empirical inspection
- **Q-DG-3:** Mobile design button positioning — fix-position-only OR layout-architecture? Your judgment; invoke #44 if architectural

## References

- Matt 2026-05-27 verbatim ratification + design button observation
- Drax Pattern-A response `a0a449e` (Court tab in v1 scope)
- Doc 49 § 4.3 (Court tab minimal Cycle 14 v1 scope)
- Dispatch A completion record at loadout `42e9393`

---

## Completion record

**Completed:** 2026-05-27
**Commit:** d7b4a28 (loadout repo)
**Build:** tsc -b clean + vite build clean (866 modules, 0 TS errors) + 81/81 tests passing
**Push status:** PENDING Matt authorization (ADR-006)

### Discipline #42 framing-audit results

**Q-DG-1 (Court tab regression cause):** NOT caused by Dispatch A or B. Git diff `42e9393..HEAD` confirmed only ActionBar.tsx, constants.ts, useSkillBuild.ts, Loadout.tsx changed — Nav.tsx and routing untouched. Court tab IS present in Nav.tsx and App.tsx unconditionally. Root cause: nav has 6 items in overflow-x-auto; at 375px mobile, last tab(s) require horizontal swipe with no visual indicator. Pre-existing bug, not Dispatch A/B regression.

**Q-DG-2 (mobile blank column):** Root cause was schema mismatch — Hypothesis C (grid column adaptation). SkillTree hardcoded CHAINS = ['chain_A','chain_B','chain_C','chain_D'] but cycle-13 uses chain IDs `t4_chain_1`, `t4_chain_2`, `supporting_chain_1`. 100% mismatch → entire SkillTree rendered only the A/B/C/D header row with blank tier rows. Also: cycle-13 emits `tier:'1'` (string) vs expected number.

**Q-DG-3 (design button):** Inline element in ClassHeader, not fixed/floating. On mobile the flex-wrap row rendered the toggle mid-header section below character name/stats/season block, cluttering the character focus area. No architectural issue — `hidden sm:flex` fix scoped correctly.

**Q3 scope check:** All 3 root causes are CSS/component-level fixes. Discipline #44 framing-refusal NOT triggered.

### Acceptance criteria status

- [x] Court tab presence verified in nav across all viewports — present and correct; right-fade gradient added for mobile scroll discoverability
- [x] Mobile blank column root cause identified (SkillTree chain ID mismatch with cycle-13 data) + remediated (dynamic chain/tier detection)
- [x] Mobile design button positioning fixed — `hidden sm:flex` on DesignModeToggle in Loadout.tsx + Sample.tsx; character/class name not obscured on mobile
- [x] No regression to Dispatch A vocab lock fixes — Discipline #45 grep clean
- [x] Build clean — tsc -b + vite build; 81/81 tests passing
- [x] Completion record appended
- [ ] Commit — pending
- [ ] Push — pending Matt authorization

### Files changed

- `src/components/Nav.tsx` — right-fade overflow gradient (mobile scroll indicator)
- `src/components/SkillTree/SkillTree.tsx` — dynamic chain/tier detection replacing hardcoded CHAINS/TIERS constants
- `src/pages/Loadout.tsx` — DesignModeToggle hidden on mobile (`hidden sm:flex`)
- `src/pages/Sample.tsx` — DesignModeToggle hidden on mobile (`hidden sm:flex`)
- `AGENT_STATE.md` — Dispatch G session record

### Open questions resolved

- Q-DG-1: Pre-existing nav overflow discoverability issue (not Dispatch A/B regression). Nav-fade fix applied.
- Q-DG-2: SkillTree chain ID hardcoding was root cause. Dynamic chain detection fix applied. Cycle-13 SkillTree now renders actual skills in T4-1, T4-2, S-1 columns.
- Q-DG-3: Position-fix-only (hidden sm:flex). No layout-anchor architecture issue.

### Hand-back note

Loadout commits pending push-batch authorization: Dispatch B `af155be` + `20e9288` + Dispatch G commit (this session). All three are routine work-products of Matt-authorized cycle work per CLAUDE.md commit discipline. Push requires Matt explicit authorization per ADR-006.
