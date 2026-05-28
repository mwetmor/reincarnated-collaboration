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

(append on completion)
