# Dispatch — 2026-05-27 — jack-ryan — Cycle 14 SC-1 discipline candidate #33-#39 ratification

**From:** knight-rider
**To:** jack-ryan (analyst + QA gatekeeper; canonical-write authority for engineering-disciplines.md)
**Approved by:** Matt 2026-05-27 (framing brief Q5 ratified — sidecar list confirmed including SC-1; Q4 Discipline #39 emphatic lock load-bearing)
**Estimated effort:** ~4-8 hours per candidate; bundled ratification or per-candidate cadence at jack-ryan's discretion
**Acceptance:** discipline candidates #33-#39 ratified or NEEDS-REVISION verdicts authored per engineering-disciplines.md canonical-write protocol; verdict artifacts filed under `agentic_orchestration/jack-ryan/` or as additions to engineering-disciplines.md

## Context

Cycle 14 framing brief RATIFIED 2026-05-27 introduces 7 discipline candidates that need jack-ryan ratification:

- **#33 Stat-range bounds discipline** (doc 46 Layer 1) — bounded vs unbounded stat dimensions; algorithm enforcement at gen-time + runtime
- **#34 Concentration discipline** (doc 46 Layer 5) — concentration probability table by tier; capability vs triggered_passive XOR/AND patterns; sets-replace-individual-capability
- **#35 Layered cohesion discipline** (doc 46 Layer 6) — CORE identity from chain composition weighted toward lower tiers + ENDGAME nod additive; identity-at-L1-without-gear / T4-choice-independence / endgame-nod-additivity tests
- **#36 Substrate-as-keying-source discipline** (doc 46 Layer 8) — sets keyed to T4 strategy × element clusters; cross-character shareability; retires per-character bespoke pattern
- **#37 Class-agnostic drop discipline** (doc 46 Layer 9) — drops use spec keyed to substrate; class/build relevance emerges from spec match, not smart-loot filtering
- **#38 Damage-scaling-path discipline** (doc 47 § 6) — skills declare `damage_scaling_type`; physical / magical / hybrid routing; weapon role differs by attribute
- **#39 No-synthetic-stub-as-permanent-fallback discipline** (framing brief § 6; **LOAD-BEARING per Matt Q4 verbatim "extremely confirm.. retire it"**) — stopgaps that bypass empirical-validation gates must be RETIRED at the cycle-close gate that introduced them OR explicitly carry forward as documented WARN with retirement-trigger empirical criterion

This sidecar is **async** — non-blocking on wave progression. However:
- **#39 ratification is HIGH-PRIORITY** because Wave 0.5 close empirically verifies #39 (synthetic_mode RETIREMENT)
- **#33 + #34 ratification gates Wave 1 close** (concentration architecture Layers 1-4+7 land at Wave 1; close Gate-2 requires the discipline canonical-write per framing brief § 2 Wave 1 entry)
- **#35 ratification gates Wave 3 close** (Phase 5 cohesion-judge LLM)
- **#36 + #37 ratification gates Wave 2 close** (concentration architecture Layers 5+8+9)
- **#38 ratification gates Wave 0.5 close** (damage scaling routing)

Recommended cadence: **#38 + #39 first** (Wave 0.5 close gate); then **#33 + #34** (Wave 1 close gate); then **#36 + #37** (Wave 2 close gate); then **#35** (Wave 3 close gate). Jack-ryan adjusts cadence per his bandwidth + Wave timing.

## Required reading before starting

- `canonical/00-ground-state.md` — ground-state oracle
- `canonical/46-concentration-architecture-2026-05-27.md` — all 9 layers (#33-#37 source)
- `canonical/47-damage-scaling-architecture-2026-05-27.md` — § 6 (#38 source)
- `agentic_orchestration/gandalf/notes/2026-05-27-cycle-14-framing-brief.md` § 6 (#39 source — synthetic-sim regression risk lock) + § 1 L3 (7 candidates listed)
- `agentic_orchestration/cycles/cycle-14-cohesion-coalescence-scope.md` § 5.5 (composition with engineering disciplines)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — canonical authority; jack-ryan extends with #33-#39
- `.claude/skills/reincarnated-jack-ryan-operating-procedure` — discipline ratification mode
- `.claude/skills/reincarnated-engineering-disciplines` — current 32 disciplines + composition with candidates

## Math-before-code

Not applicable directly — discipline ratification is canonical-write work, not math/code. However, jack-ryan should validate that each candidate's load-bearing claim is grounded in empirical evidence (per Discipline #11 empirical inspection) — e.g., #34 concentration discipline is grounded in Cycle 13 empirical reference table surfacing capability-soup pattern; #39 is grounded in Cycle 13 close synthetic_mode failure mode.

## Cross-seam contract change?

**NO** — discipline canonical writes are engineering-disciplines.md amendments, not code or schema. Round-trip not applicable. (Downstream consumers — all agents — read engineering-disciplines.md as authoritative; cross-seam impact lands at agent-discipline-citation time, not at canonical-write time.)

## Scope

- [ ] For each of 7 candidates (#33-#39):
  - [ ] Verify candidate is well-formed per engineering-disciplines.md canonical-write protocol (load-bearing claim + empirical motivation + composition with existing disciplines + when-to-cite triggers + cross-references)
  - [ ] Issue verdict: RATIFIED / RATIFIED-WITH-REVISIONS / NEEDS-REVISION (route back to gandalf for re-framing if NEEDS-REVISION)
  - [ ] Canonical-write to engineering-disciplines.md (jack-ryan's authority per OP) for RATIFIED + RATIFIED-WITH-REVISIONS verdicts
- [ ] Cadence per framing brief Wave gating:
  - [ ] #38 + #39 first (Wave 0.5 gate)
  - [ ] #33 + #34 next (Wave 1 gate)
  - [ ] #36 + #37 next (Wave 2 gate)
  - [ ] #35 last (Wave 3 gate)
- [ ] File verdict artifacts under `agentic_orchestration/jack-ryan/` per OP convention
- [ ] Append completion record to this dispatch file per dispatches/README.md (per-candidate completion records or bundled at end)
- [ ] Round-trip: not applicable
- [ ] Commit + push per Matt 2026-05-27 per-cycle push pattern (auto-fire per CLAUDE.md addendum)

## Acceptance criteria

- [ ] All 7 candidates have verdicts (RATIFIED / RATIFIED-WITH-REVISIONS / NEEDS-REVISION)
- [ ] RATIFIED + RATIFIED-WITH-REVISIONS verdicts have canonical writes landed at `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`
- [ ] Engineering-disciplines.md updates cross-reference doc 46 / doc 47 / framing brief per discipline source
- [ ] NEEDS-REVISION verdicts (if any) route back to gandalf via knight-rider for re-framing
- [ ] #39 ratification has highest priority emphasis given Matt Q4 "extremely confirm.. retire it" verbatim
- [ ] Completion record appended

## Out of scope (explicit non-goals)

- Do NOT amend doc 46 or doc 47 — those are gandalf's canonical seam; if a candidate is mis-framed, route back via knight-rider for gandalf re-authoring
- Do NOT author new disciplines beyond the 7 candidates — that requires fresh Matt-authorization
- Do NOT touch decisions-log entries — discipline ratification is engineering-disciplines.md authority, not decisions-log
- Do NOT enter DEV-MODE Gate-2 review — this is canonical-write work in jack-ryan's discipline-ratification mode

## Open questions for jack-ryan to resolve

- **Q-SC1-1**: Discipline #39 references "stopgaps that bypass empirical-validation gates must be RETIRED at cycle-close gate that introduced them" — is this a new discipline OR an operationalization of existing Discipline #11 empirical inspection? Jack-ryan judgment: new top-level discipline, or sub-discipline #11.1 / similar?
- **Q-SC1-2**: Discipline #34 concentration spans Layer 5 (probability table) + Layer 1 (stat-range bounds prerequisite) + Layer 7 (synergy scan refined) + Layer 8 (set keying retiring per-character bespoke). Is this one discipline or multiple? Jack-ryan judgment + recommend canonical structure.
- **Q-SC1-3**: Discipline #35 layered cohesion has three testable sub-disciplines (identity-without-gear / T4-choice-independence / endgame-nod-additivity). Are these one composite discipline OR three? Jack-ryan judgment.
- **Q-SC1-4**: Discipline #38 damage-scaling-path composes with skill-system-2026-05-24.md composition pattern (which already implicitly excluded weapon damage per doc 47 § 1.3). Is this discipline net-new OR a clarification surfacing what was implicit? Jack-ryan judgment.

## References

- `canonical/46-concentration-architecture-2026-05-27.md` (#33-#37 source)
- `canonical/47-damage-scaling-architecture-2026-05-27.md` (#38 source)
- `agentic_orchestration/gandalf/notes/2026-05-27-cycle-14-framing-brief.md` § 1 L3 + § 6 (#39 source)
- `agentic_orchestration/cycles/cycle-14-cohesion-coalescence-scope.md` § 5.5
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — current canonical (jack-ryan extends)
- `.claude/skills/reincarnated-engineering-disciplines` — composition wrapper
- `.claude/skills/reincarnated-jack-ryan-operating-procedure` — discipline ratification mode
- Cycle 13 SC-2 jack-ryan discipline ratification dispatch precedent at `agentic_orchestration/dispatches/`
