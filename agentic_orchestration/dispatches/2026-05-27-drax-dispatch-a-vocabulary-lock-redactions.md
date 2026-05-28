# Dispatch — 2026-05-27 — drax — Dispatch A: Vocabulary lock redactions (~0.5 days; IMMEDIATE no gate)

**From:** knight-rider
**To:** drax (loadout/demo seam owner)
**Approved by:** Matt 2026-05-27 verbatim "Dispatch A — RATIFY IMMEDIATE (~0.5 days; mechanical vocab fixes; closes 5 #45 violations; no gate)"
**Estimated effort:** ~0.5 days (5 player-facing string replacements per drax Cycle 14 tab integration Pattern-A verification at `agentic_orchestration/drax/notes/2026-05-27-cycle-14-tab-integration-pattern-a-response.md` § Discipline #45 violation inventory)
**Acceptance:** All 5 player-facing #45 violations remediated; Discipline #45 vocabulary lock CLEAN at player-facing player-surface; commit + push per Matt's per-cycle push pattern

## Quality criterion (Move 1)

**Game-quality goal this dispatch serves:** close 5 player-facing Discipline #45 vocabulary violations in loadout web app. Without this dispatch, player-facing surface leaks `class` vocabulary that contradicts the architectural no-classes recommitment. Composes "Engine first. Game second. Phase third." — player-surface vocabulary integrity is game-layer infrastructure flowing from engine-layer no-classes architecture.

**Refutation conditions:**
- Any of 5 string locations is NOT player-facing (e.g., comment, internal variable) — confirm at edit time
- Replacement vocabulary creates UX confusion (e.g., "kits" reads less natural to players than "classes" — design judgment)
- Vocabulary lock requires THEMATIC_REGISTRY consultation for some terms

## Context

Per drax Cycle 14 tab integration Pattern-A response § Discipline #45 violation inventory:

**5 player-facing #45 violations:**
1. `Analytics.tsx:30` — `StatBadge label="Classes"` (player-facing stat card)
2. `Encounters.tsx:454` — "Per-class" button label
3. `Encounters.tsx:469-470` — 2 description strings using "class" vocabulary
4. `Pitch.tsx:22` — `StatBadge label="Classes: 55"` (stale count + #45 violation)

**Recommended vocabulary remapping (drax judgment + Discipline #45 canonical at engine `b576727`):**
- "Classes" → "Kits" (engine vocabulary; consistent with kit_archive + ExportFactionCluster + Wave 1.5 Stage 3 Option α emergence model)
- "Per-class" → "Per-kit" OR "Per-faction" (drax judgment per UI context)
- "class" in descriptions → "kit" OR "build" OR "archetype" (drax judgment; archetype EXEMPT per #45 canonical at engineering-disciplines.md if used as narrative-role-label not generative-input-label)

**Discipline #45 carve-outs (per engine `b576727` § 1715-1716):**
- `proxy_*_class` substrate field names EXEMPT
- `canonical/story/` narrative vocabulary EXEMPT
- Player-facing narrative output EXEMPT (the redactions here are player-facing UI LABELS, not narrative output — labels stay engine-vocabulary)

## Required reading

- `agentic_orchestration/drax/notes/2026-05-27-cycle-14-tab-integration-pattern-a-response.md` § Discipline #45 violation inventory
- `~/Games/reincarnated-loadout/src/components/Analytics.tsx` (line 30)
- `~/Games/reincarnated-loadout/src/components/Encounters.tsx` (lines 454, 469-470)
- `~/Games/reincarnated-loadout/src/components/Pitch.tsx` (line 22)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § Discipline #45 (vocabulary lock canonical)
- `.claude/skills/reincarnated-drax-operating-procedure`

## Discipline #46 compliance

- N/A — UI string changes; no DB queries

## Discipline #42 framing-audit

- **Q1:** (1) drax verification identified exactly 5 player-facing #45 violations; (2) "Classes" → "Kits" remapping doesn't create UX confusion; (3) Pitch.tsx:22 stale count fix is part of #45 violation scope (not separate stale-data fix)
- **Q2:** verify each location IS player-facing (not internal/comment); verify replacement reads natural in UI context
- **Q3:** if any location is NOT player-facing OR replacement breaks UX, invoke #44 framing-refusal + surface back to KR

## Scope

For each of 5 locations:

- [ ] Read in context (verify player-facing)
- [ ] Apply vocabulary remapping per drax judgment
- [ ] For Pitch.tsx:22 specifically: fix stale "55" count (verify current correct value OR remove count entirely if hardcoded numbers are problematic at static marketing page)
- [ ] Build verification (no TypeScript errors)
- [ ] Visual verification (if possible per drax tooling)

### Closure

- [ ] Update `~/Games/reincarnated-loadout/AGENT_STATE.md`
- [ ] Grep audit verification: `grep -rni "class" src/components/Analytics.tsx src/components/Encounters.tsx src/components/Pitch.tsx` shows zero player-facing string violations post-edit
- [ ] Append completion record to this dispatch
- [ ] Commit + push per Matt 2026-05-27 per-cycle push pattern

## Acceptance criteria

- [ ] All 5 #45 violations remediated
- [ ] Player-facing vocabulary CLEAN per Discipline #45 canonical
- [ ] No TypeScript errors
- [ ] AGENT_STATE.md updated
- [ ] Completion record + commit + push

## Out of scope

- Do NOT touch non-player-facing strings (comments, internal variables, etc.)
- Do NOT touch Loadout.tsx (Dispatch B scope)
- Do NOT touch Summary tab faction-grouped re-architecture (Dispatch C scope; gated)
- Do NOT touch Sample tab committed-state display (Dispatch D scope; gated)
- Do NOT touch substrate field names (`proxy_*_class` EXEMPT)

## Open questions for drax

- **Q-DA-1:** "Classes: 55" Pitch.tsx:22 — fix to current value OR remove the count entirely (count is stale by construction at static page; recommend remove)
- **Q-DA-2:** Vocabulary remapping per location — your judgment per UI context (engine vocabulary "kits" recommended but drax UX judgment final)

## References

- Drax Pattern-A response `a0a449e`
- Discipline #45 canonical at engine `b576727`
- Matt 2026-05-27 verbatim ratification (above)

---

## Completion record

(append on completion)
