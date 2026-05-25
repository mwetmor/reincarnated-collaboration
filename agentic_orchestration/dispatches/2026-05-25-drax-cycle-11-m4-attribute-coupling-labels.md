# Dispatch — 2026-05-25 — drax — Cycle 11 M4 attribute coupling labels

**From:** knight-rider
**To:** drax
**Approved by:** Matt 2026-05-25 (P2c ratification — "Approved")
**Estimated effort:** ~0.25 day (~2 hours)
**Acceptance:** Loadout stats display surfaces attribute coupling labels in human-readable form; no schema work required

---

## Context

Cycle 10 closed with v1_scope = 2,293 items LOCKED. Cycle 11 v1 implementation push targets T4 post-mortem readiness milestone (~3 weeks wall-clock) via parallel multi-seam work. Loadout v1.0 M1-M6 is the loadout-app slice of this milestone.

M4 is the **zero-dependency** loadout item — attribute coupling labels in the stats display use data ALREADY PRESENT in the class JSON export. No star-lord schema extension required. Drax can fire this immediately while star-lord schema work (gating M1/M2/M5) and rocket § 8 work (gating M3/M6) proceed in parallel.

Per drax loadout scoping memo § 4.3 (drax authored 2026-05-25) + Matt P2c "Approved" ratification of all 5 drax recommendations Q1-Q5.

This is Cycle 11 Wave 1; fired in parallel with star-lord pre-migration mitigation + star-lord schema extensions + rocket § 8 + jack-ryan decisions-log batch.

## Required reading before starting

- `agentic_orchestration/drax/notes/2026-05-25-loadout-app-readiness-scoping.md` § M4 specification + § 4.3 effort estimate
- `agentic_orchestration/matt-log-back-decisions-2026-05-25.md` § P2c (Matt verbatim authorization + Q1-Q5 ratified)
- Current loadout app stats display component (`~/Games/reincarnated-loadout/` — drax knows the path; typically `src/components/StatsDisplay.tsx` or similar)
- Class JSON shape — verify attribute coupling data is already present (per drax memo claim "data already present")

## Math-before-code

No new math. Attribute coupling labels are display-layer translation:
- Raw data in class JSON: typically `attribute_coupling: ["STR", "DEX"]` or similar
- Display label: human-readable form (e.g., "Couples with Strength + Dexterity")

Drax judgment on exact label phrasing per loadout design language conventions.

## Cross-seam contract change? (Principle 6 gate)

**No.** Drax M4 consumes class JSON `attribute_coupling` field that ALREADY EXISTS per drax memo § 4.3. No schema change; no engine-side modification; no new field added. This is pure display-layer work in the loadout app.

Round-trip: not applicable — no cross-seam contract change in this dispatch (drax consumes existing class JSON field).

**Verification at execution:** drax confirms `attribute_coupling` field IS present in current class JSON output before implementation. If field is NOT present (drax memo claim was incorrect), this becomes a star-lord schema extension item and merges into the separate star-lord-schema-extensions dispatch. Drax flags to KR if found.

## Scope

- [ ] StatsDisplay component (or equivalent) renders attribute coupling labels in human-readable form
- [ ] Label styling consistent with existing stats display visual language
- [ ] Empty / missing coupling data gracefully handled (no broken render)
- [ ] Smoke: open loadout app, navigate to a class with coupling data, verify label renders correctly
- [ ] Tag: `drax/v0.0-cycle-11-m4-attribute-coupling-labels-2026-05-25`
- [ ] AGENT_STATE.md updated at session end

## Acceptance criteria

- [ ] Attribute coupling labels visible in stats display for classes that have coupling data
- [ ] Visual styling clean + consistent with existing UI patterns
- [ ] No regression in existing stats display for classes without coupling data
- [ ] Round-trip: not applicable — no cross-seam contract change

## Out of scope (explicit non-goals)

- DO NOT fire M1 / M2 / M3 / M5 / M6 (gated on dependencies; separate dispatches)
- DO NOT touch star-lord schema (M4 uses existing field)
- DO NOT fire Loadout v1.1+ items D1-D13 (deferred per drax memo § 4.2)
- DO NOT deploy to production Vercel — Q5 RATIFIED: preview-only for T4 post-mortem
- DO NOT design new analytics surfaces (Q4 `/the-work` analytics suite is post-T4-post-mortem)

## Open questions for the agent to resolve

- Exact label phrasing (drax design judgment per loadout language conventions)
- Whether coupling shows as inline-with-stat-block or separate-section (drax UI judgment)
- Confirm `attribute_coupling` field present in current class JSON before implementation — if not, escalate to KR for routing to star-lord schema extension dispatch

## References

- Matt verbatim: "Approved" (P2c — `agentic_orchestration/matt-log-back-decisions-2026-05-25.md` § P2c)
- Drax loadout scoping memo: `agentic_orchestration/drax/notes/2026-05-25-loadout-app-readiness-scoping.md`
- Cycle 11 scope-doc: `agentic_orchestration/cycles/cycle-11-hive-mind-scope.md` § 1
- Drax memo Q1-Q5 RATIFIED: Q1 (v1_scope flag internal; provenance badge visible); Q2 (T4 comparison toggle); Q3 (T4 post-mortem main-weapon only); Q4 (`/the-work` post-T4); Q5 (Vercel preview-only)

---

## Completion record

**Executed by:** drax
**Date:** 2026-05-25
**Result:** ESCALATION — `attribute_coupling` field NOT PRESENT in class JSON

### Pre-implementation verification

Per dispatch § "Cross-seam contract change? (Principle 6 gate)" and § "Open questions": drax confirmed `attribute_coupling` field presence BEFORE any implementation.

**Verification steps:**
1. Searched `attribute_coupling` across all 11 seasons in `reincarnated-loadout/data/` — ZERO matches
2. Searched across `reincarnated-engine/` source — ZERO matches
3. Inspected `src/data/types.ts` `ClassData` interface — no `attribute_coupling` field
4. Sampled class JSON keys from seasons 001001, 001005, 002015, 002328 — field absent in all seasons

**Class JSON top-level keys (current):** `id`, `name`, `title_completion`, `flavor_text`, `archetype_tag`, `energy_type`, `role_orientation`, `range_profile`, `dominant_element`, `color_palette`, `stat_distribution`, `skills`, `balance_metadata`, `convergence_report` (plus per-season additive fields such as `seasonal_dominant_element`, `is_act_boss`, `carried_gear`, `movement_speed`, `post_process_d10`).

No `attribute_coupling` field in any season, any class, or any engine source path.

### Conclusion

Drax memo § 4.3 claim that M4 has "no schema change needed" and "data already present" was incorrect. The `attribute_coupling` field does not exist in the current class JSON schema.

M4 is NOT zero-dependency. It requires a star-lord schema extension to emit an `attribute_coupling` field (or equivalent) from the engine's class JSON export. The display-layer work is trivially small once the field exists; the blocker is schema extension.

### Action taken

Per dispatch protocol: "If field is NOT present, this becomes a star-lord schema extension item and merges into the separate star-lord-schema-extensions dispatch. Drax flags to KR if found."

- NO implementation fired
- NO code changes committed
- NO tag cut
- `reincarnated-loadout/AGENT_STATE.md` updated with escalation record

### Routing recommendation

M4 merges into the star-lord schema extensions dispatch. Suggested field: `attribute_coupling: string[]` on `ClassData` — an array of stat names indicating which primary stats scale skills for this class (e.g., `["intelligence", "wisdom"]`). Once star-lord emits this field, drax M4 implementation is approximately 1-2 hours (display-only, no schema design work needed on drax side).

**Tag cut:** none (escalation; no implementation)
**Commit:** AGENT_STATE.md update + this completion record (auto-commit per CLAUDE.md addendum)
**Smoke:** not applicable (no implementation fired)
