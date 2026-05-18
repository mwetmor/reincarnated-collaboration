# 2026-05-18 — jack-ryan — Decisions-log RETIRE hybrid_mage + Discipline #17 amendment (smoke environment fidelity)

**Authority:** Matt L3 verdict 2026-05-18 — RETIRE hybrid_mage from canonical-7. D11.2 Phase B failure surfaced smoke environment fidelity bug; Discipline #17 needs amendment to prevent recurrence.
**Type:** Pattern A — decisions-log entry + discipline doc amendment; ~45-60 min.
**Status:** 🟢 **ACTIVE — fire immediately.**

---

## Why this matters

Two interlocking captures from the D11.2 cycle:

**Decision capture (RETIRE):** Matt L3 chose Option 3 from rocket's Phase B escalation. Canonical-7 → canonical-6. This decision needs canonical capture so future agents don't try to re-introduce hybrid_mage without re-litigating the underlying decision.

**Discipline #17 amendment (smoke environment fidelity):** Phase A smoke (no gear_catalog) returned 5/5 PASS at scale=0.75. Phase B (with gear_catalog) returned 0/17 PASS. The smoke environment did not mirror production environment; the false positive triggered a full Phase B salvage that was doomed. This is a clean case-study addition to Discipline #17's lineage — the smoke gate's ONLY job is to predict full-run outcome; if the gate's environment is leaner than production, it leaks false positives.

---

## Required reading

1. **Gandalf canonical-6 design doc** — `canonical/story/canonical-6-transition-retire-hybrid-mage-2026-05-18.md` (read AFTER gandalf ships; informs decisions-log rationale wording + your cross-canon strip-pass list)
2. **D11.2 Phase B failure dispatch** — `agentic_orchestration/dispatches/2026-05-17-rocket-d11-2-phase-b-full-salvage-scale-0-75.md` § completion record (root-cause analysis; verdict; decision file path)
3. **D11.2 Phase B decision file** — `reincarnated-engine/output/d11_2_phase_b_decision.json` (per-instance data; diagnostic; 4-option escalation list)
4. **Your D11.2 Gate-1 verdict** — `agentic_orchestration/dispatches/2026-05-17-jack-ryan-d11-2-gate1-math-note-plus-smoke-soundness.md` (Discipline #17 ADOPTED with ⌈N/2⌉ amendment; canonical wording from hive-log)
5. **decisions-log.md** — `reincarnated-engine/design/decisions/decisions-log.md`
6. **engineering-disciplines.md** — `reincarnated-engine/design/working-agreement/engineering-disciplines.md`

---

## Scope — two deliverables

### Deliverable 1 — decisions-log.md RETIRE entry

Append new entry capturing:
- **Title:** "2026-05-18: RETIRE hybrid_mage from canonical-7 — #160 verdict"
- **Decision:** Drop hybrid_mage from canonical archetype list; canonical-7 → canonical-6; 6 archetypes are the new canonical set
- **Date:** 2026-05-18
- **Authority:** Matt L3 verdict
- **Context:** D11.0 (α tax recalibration; 6% convergence MISS) → D11.1 (ceiling-primary; 0% MISS) → D11.2 (Lever B DPS density scale; smoke 5/5 PASS at scale=0.75; Phase B 0/17 FAIL due to gear-environment fidelity bug). Three structural attempts, all failed.
- **Rationale (per Matt):** Fastest path to "develop a completely new LLM generated season once we feel those issues are resolved and converge many classes from it" is removing the broken archetype, not iterating further on it. Identity at scale<0.5 would be shell-of-self.
- **Alternatives considered:**
  - Option 1 (re-run smoke with gear; sweep deeper {0.55, 0.45, 0.35}): rejected — identity-preservation risk below 0.5 + uncertain whether any scale converges
  - Option 2 (composite B+D at scale=0.65 + 5% HP penalty in full gear environment): rejected — incremental, not structural
  - Option 4 (D12+ structural redesign of hybrid_mage kit composition): rejected — multi-day cycle with uncertain payoff
- **Implications:**
  - Engine generation drops to 6 archetypes (rocket implementation)
  - Existing 17 hybrid_mage classes in 002011-015 receive `is_retired: true` flag; demo+loadout filter them (drax + rocket joint)
  - Cross-canon strip pass (your Deliverable 3 below) removes hybrid_mage references from design docs
  - Future seasons start at 002016 with canonical-6
  - Alternative-resurrection paths (gandalf's deliverable 4 list) parked for future design consideration
- **Forward pointers:** gandalf canonical-6 transition doc; rocket archetype-list removal; drax classes filter

### Deliverable 2 — Discipline #17 doc amendment

Land Discipline #17 canonical wording in `engineering-disciplines.md` per your ADR-002 doc-only authority. Use the wording from your Gate-1 hive-log STATE entry, **PLUS the new amendment for environment fidelity:**

> **Discipline #17 — Empirical-calibration smoke gate before full-regen / full-salvage with a new lever.**
> 
> Before applying a new balance-loop lever (parameter scaling, ceiling adjustment, archetype-tax recalibration) across a full season cohort, run a small parametric sweep (3 sweep points × ⌈N/2⌉ acceptance threshold over N representative instances; typically N=5) to empirically locate the lever's effective magnitude. Sweep cost ~10-15 min per point.
> 
> **Amendment (D11.2 Phase B failure case-study):** smoke environments MUST mirror production environment dimensions. Specifically: balance_loop construction in the smoke runner must include gear_catalog, monster_pool, archetype generation parameters, and any other inputs that materially affect the balance computation. Environment-mismatch is a smoke-positive-false-flag failure mode — a smoke runner that lacks gear_catalog will systematically over-estimate lever effectiveness (gear-buffed instances win more fights even at floor modifier). Verify smoke environment == production environment in code-review before sweep.
> 
> **Case-study lineage:**
> - D11.0: magnitude-by-analogy projection (50-60% projected; 6% actual) — pre-Discipline-#17 era
> - D11.1: dual-mode failure (Mode A non-damage skills + Mode B ceiling-doesn't-bite) — pre-Discipline-#17 era
> - D11.2 Phase A: smoke 5/5 PASS at scale=0.75 — false positive due to no-gear smoke environment
> - D11.2 Phase B: 0/17 FAIL in full-gear production environment — confirmed environment-mismatch as the false-positive driver
> 
> **Cross-references:** B14.5 V1 primary loop architecture (smoke-test discipline #2 is the precursor); ADR-002 (gate authority); canonical-6 transition doc (the case-study outcome).

Tag the amendment as `jack-ryan/v1.6-discipline-17-canonicalization-plus-env-fidelity-amendment-1`.

### Deliverable 3 (deferred to next dispatch; knight-rider fires post-gandalf) — cross-canon strip pass

You'll receive gandalf's cleanup list. Strip pass = remove hybrid_mage references from canonical docs. Not in scope here — separate Pattern A dispatch.

---

## Acceptance criteria

- [ ] decisions-log.md entry authored with full RETIRE rationale + alternative-considered breakdown
- [ ] engineering-disciplines.md Discipline #17 canonical entry landed
- [ ] Discipline #17 environment-fidelity amendment included
- [ ] Case-study lineage (D11.0/D11.1/D11.2 Phase A/B) cited
- [ ] All three docs cross-reference each other (decisions-log ↔ engineering-disciplines ↔ canonical-6)
- [ ] Hive-log STATE entry appended (PRE-SIGNAL § 14.1.1)
- [ ] AGENT_STATE STATE entry
- [ ] Tag `jack-ryan/v1.6-discipline-17-canonicalization-plus-env-fidelity-amendment-1` AND `jack-ryan/v1.7-decisions-log-retire-hybrid-mage-1` (two separable tags for two separable deliverables; both local)

---

## Out of scope (DO NOT)

- ❌ DO NOT execute cross-canon strip pass (separate dispatch)
- ❌ DO NOT modify D11.2 advisory or math note (those are historical record now)
- ❌ DO NOT re-litigate RETIRE
- ❌ DO NOT push tag (ADR-006)

---

## Coordination

- **Parallel-safe with:** gandalf canonical-6 doc (your decisions-log RETIRE entry depends on gandalf's rationale wording for full polish — but you can author the structure now and refine after gandalf ships, OR wait for gandalf and do both deliverables in one pass); rocket archetype-list removal; drax v1.16.2 audio; elrond dungeon-objects audit
- **Triggers downstream:** cross-canon strip-pass dispatch (knight-rider fires post-gandalf list)
- **PRE-SIGNAL § 14.1.1** before hive-log appends

Recommendation: author Discipline #17 amendment first (independent of gandalf); pause for gandalf's canonical-6 doc; then author decisions-log entry citing both gandalf doc + Discipline #17 amendment.

---

*Dispatched 2026-05-18 by knight-rider per Matt L3 RETIRE verdict. ~45-60 min total. Append completion records when done.*

---

## Completion record

**Completed:** 2026-05-18
**Agent:** jack-ryan
**Time:** ~45 min
**Tags:** `jack-ryan/v1.6-discipline-17-canonicalization-plus-env-fidelity-amendment-1` (engine main `8919233`), `jack-ryan/v1.7-decisions-log-retire-hybrid-mage-1` (engine main `b59a88b`)

### Deliverable 1 — Discipline #17 canonical entry + environment-fidelity amendment (v1.6)

Landed in `reincarnated-engine/design/working-agreement/engineering-disciplines.md` as Discipline #17. Core wording: 3-sweep-point × ⌈N/2⌉ acceptance threshold gate (adopted at Gate-1 v1.5 with ⌈N/2⌉ amendment).

Environment-fidelity amendment added from D11.2 Phase B failure case-study. Full wording per dispatch template § Deliverable 2. Gate-1 triggerable question added. Anatomy note updated to #1-#17. Cross-references updated.

### Deliverable 2 — decisions-log RETIRE entry (v1.7)

New entry "2026-05-18: RETIRE hybrid_mage from canonical-7 — #160 verdict" appended to `reincarnated-engine/design/decisions/decisions-log.md`. Full D11 cycle context, four alternatives-considered breakdown, Matt rationale, implications section, forward pointers.

Cross-reference to `canonical/story/canonical-6-transition-retire-hybrid-mage-2026-05-18.md` included at known path (gandalf doc in-flight; path correct).

### Acceptance criteria status

- [x] decisions-log.md entry authored with full RETIRE rationale + alternative-considered breakdown
- [x] engineering-disciplines.md Discipline #17 canonical entry landed
- [x] Discipline #17 environment-fidelity amendment included
- [x] Case-study lineage (D11.0/D11.1/D11.2 Phase A/B) cited
- [x] All three docs cross-reference each other (decisions-log ↔ engineering-disciplines ↔ canonical-6 path)
- [x] Hive-log STATE entry appended (PRE-SIGNAL § 14.1.1 performed)
- [x] AGENT_STATE STATE entry (simulation/AGENT_STATE.md header updated)
- [x] Tag `jack-ryan/v1.6-discipline-17-canonicalization-plus-env-fidelity-amendment-1` (local; push gated per ADR-006)
- [x] Tag `jack-ryan/v1.7-decisions-log-retire-hybrid-mage-1` (local; push gated per ADR-006)

### Note on sequencing

Authored per dispatch recommendation: Discipline #17 first (independent of gandalf), then decisions-log entry citing both. Gandalf canonical-6 doc not yet available at authoring time; cross-reference included at known path. Decisions-log entry does not require amendment when gandalf ships (path is correct; content is already sourced from Phase B decision file + dispatch spec).

### Downstream triggers

- Rocket: archetype-list removal; `is_retired: true` on 17 hybrid_mage classes in 002011-015
- Drax + rocket joint: demo + loadout filter for `is_retired: true`
- Knight-rider: cross-canon strip-pass dispatch (Deliverable 3 in this dispatch; fires post-gandalf canonical-6)

— jack-ryan
