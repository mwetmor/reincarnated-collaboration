# Gate-1 Review — W0.7 LC-009 Ablation Design

**Reviewer:** jack-ryan (DESIGN-MODE Gate-1)
**Date:** 2026-05-21
**Severity:** APPROVE-OPTION-C (with advisories)
**Math note reviewed:** `reincarnated-engine/src/reincarnated/simulation/math/w0-7-lc-009-ablation-design.md`
**Dispatch reviewed:** `agentic_orchestration/dispatches/2026-05-20-jack-ryan-gate1-w0-7-lc-009-ablation-design.md`
**Principles applied:** Discipline #1, #2, #10, #11, #13b; Review Principles 1-5

**Filed by:** knight-rider (jack-ryan returned review inline per agent rules; knight-rider preserves canonical record).

---

## Top-line verdict

**APPROVE-OPTION-C.**

The empirical inspection is methodologically sound. The surface verification is correct for all three dispatch-identified variables. The historical 1.82 range is a mixed-era artifact with two independently-validated causes. Option C (no ablation required) is a valid Discipline #13b closure — the signal the dispatch was designed to explain does not exist in the current-era data. LC-011 is cleared to proceed immediately.

---

## Per-question answers

### Q1 — Pre-schema vs post-schema exclusion validity

**Exclusion is correct and the 0.6234 figure is defensible.**

Pre-schema records (seasons 000013-000700) are structurally disqualified on three independent grounds:

1. No `skill_power_tier=58` compensation — hunter's damage density baseline was different
2. No `range_profile` enforcement — `_pick_range_profile()` at `season_orchestrator.py:137` hardcodes `energy_type == "focus" → "long"`; field not recorded per-class at that era
3. No `energy_type` per-class in telemetry — column entirely NULL; balance loop operated without the energy-type lever now forming the 4th recompose lever; pre-W0.10 boss-floor artifact compounds

These are different class construction paths yielding a different balance surface. Mixing them with post-schema records is a type error on the data, not a measurement choice. **Exclusion valid.**

### Q2 — Surface power verification

**All three variables correctly assessed as low/zero ablation power.** Direct code verification:

- **`range_profile=long`:** `season_orchestrator.py:137-138` — unconditional branch for `energy_type=focus`, no RNG. Zero cross-seed variance. Ablating would test different archetype, not explain existing variance.
- **`geometry_bias`:** 8-entry dict; weights are constants in `b6_archetype_templates.py`. Cross-seed variance comes from `rng_pick` within selection, not bias template.
- **`kit_size` (12/13/13):** 1-skill range; narrowest of any archetype. Cannot explain 0.62 modifier range.

LC-002 precision-of-attribution standard met or exceeded — gamora identifies actual variance drivers (kit-seed, gauntlet composition, target WR, sampling noise) rather than just ruling out dispatch surfaces.

### Q3 — Option C disposition rigor

**Option C is a valid Discipline #13b closure pattern when the signal the ablation was designed to explain is refuted by empirical inspection.**

Two conditions for Option C without confirmatory baseline:
1. Artifact claim has two+ independent supporting mechanisms (gamora provides: era mixing + boss-tier floor artifact)
2. Post-era signal has plausible structural explanation (Drivers 1 + 3: kit-seed + gauntlet variance — designed properties)

**Both conditions met. No confirmatory baseline run required.**

### Q4 — Sample size (n=7)

**Sufficient for artifact-refutation claim; not sufficient for full distributional characterization.**

Option C claim is "historical 1.82 is mixed-era artifact; current signal does not meet threshold of concern" — different claim than "hunter modifier range is X with Y% CI." n=7 sufficient for the former; insufficient for the latter. If distributional characterization needed later, Option B (n=20+) is appropriate standalone workstream.

### Q5 — B14.5 sidecar #2 reinterpretation

**YES — mark as REINTERPRETED-BY-LC-009 (2026-05-21).**

- **What stands:** 1.82 measurement was real at time of measurement; accurate for the data population observed
- **What is revised:** interpretation that 1.82 reflects structural inconsistency in current-era balance system; revised to "mixed-era data quality artifact (pre-B6-schema records + pre-W0.10 boss-floor)"

**Matt auto-memory update required.** Updated framing: "Hunter 1.82 modifier range was mixed-era artifact; post-schema CONVERGED range = 0.6234 as of W0.7 LC-009 (n=7, 2026-05-21). Hunter is not current-era outlier."

---

## Additional review points

### ARP-6 — LC-002 precedent comparison

**Option C is repeatable. LC-002 was not the "normal case"; Option C is equally canonical.**

Decision tree:
```
Discipline #11 empirical inspection
    ├── Signal confirmed present → design/revise ablation to attribute (LC-002 path)
    ├── Signal shrunk but non-zero → design ablation for actual signal
    └── Signal refuted as artifact → no ablation; close with empirical note (LC-009 / Option C)
```

All three branches are valid Discipline #11 outcomes. Knight-rider should document both LC-002 and LC-009 as canonical Discipline #11 exit patterns.

### ARP-7 — W0.7 acceptance criterion amendment

**RECOMMENDED.** Add to W0.7 dispatch acceptance criteria:

> Where Discipline #11 empirical inspection refutes the precondition for ablation (signal is a data quality artifact, not a current-era structural signal), the LC may close with empirical inspection + math note + structural reinterpretation as the deliverable. This constitutes meta-attribution under Discipline #13b and satisfies the LC's closure requirement. Ablation runs are not required.

Per ADR-002, acceptance criteria amendments are architectural scope. Knight-rider carries to Matt; Matt decides. *(Per Matt's autonomous-operation directive 2026-05-21: knight-rider may apply autonomously and surface at session close.)*

### ARP-8 — LC-011 forward-looking guidance

LC-011 should follow Discipline #11 pre-inspection pattern. **Option C unlikely for LC-011 but should not be excluded a priori:**

- Iteration-overhead signal is documented across post-schema era; not era-mixed
- Variance drivers (multi-skill synergies, larger recompose search space) are structural properties
- LC-002 path (revised ablation, runs executed) is expected outcome
- Pre-inspection must still run; query post-schema convergence iteration data stratified by archetype

---

## Discipline compliance attestation

- **#1 math-before-code:** PASS (math note before runs proposed)
- **#2 smoke-test:** N/A (Option C produces no runs)
- **#10 right-tool-for-question:** PASS (empirical inspection is the right tool to test signal reproducibility)
- **#11 empirical-inspection-over-assumption:** PASS — and this is the canonical Option C example
- **#13b outcome-attribution-opacity:** PASS (attribution provided even under Option C: historical range attributed to era mixing + boss-floor artifact, not template variables)

---

## Disposition summary

| Item | Verdict |
|------|---------|
| Option C endorsement | APPROVED |
| Pre-schema exclusion validity | VALID |
| Surface verification (3 variables) | CORRECT — zero/low power confirmed by code audit |
| n=7 sufficient for Option C closure | YES (artifact-refutation; not distributional characterization) |
| Confirmatory baseline run required | NO — two independent artifact causes satisfy rigor threshold |
| OQ-6 re-opens under LC-009 | NO — confirmed closed by W0.10.5 (hunter at 0.6355 wins 100% all tiers) |
| B14.5 sidecar #2 reinterpretation | YES — mark REINTERPRETED-BY-LC-009 |
| W0.7 acceptance criteria amendment | RECOMMENDED — knight-rider carries to Matt |
| LC-011 Discipline #11 pre-inspection | REQUIRED — Option C unlikely but not excluded |

---

## Advisories (non-blocking)

**Advisory 1 — Option B as future hygiene:** if W0.8+ work produces additional CONVERGED hunter records naturally, note against 0.6234 range. Target n=15 over time for distributional validation. Does not block LC-009 closure.

**Advisory 2 — Matt auto-memory update required.** Knight-rider flags at session close (per Q5 framing).

**Advisory 3 — W0.7 dispatch amendment is Matt-tier per ADR-002.** Knight-rider carries; Matt decides. *(Per autonomous-operation directive, knight-rider may apply and surface; Matt may revise at intervention point.)*

---

## Files reviewed

- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/math/w0-7-lc-009-ablation-design.md`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/dispatches/2026-05-20-jack-ryan-gate1-w0-7-lc-009-ablation-design.md`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/dispatches/2026-05-21-gamora-w0-7-ablation-experiments.md`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/math/w0-7-lc-002-ablation-design.md`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md` (W0.10.5 vs W0.9.6 empirical-close artifact)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/season_orchestrator.py` (lines 116-150, 1490-1501)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/b6_archetype_templates.py` (lines 145-167)
- `/Users/admin/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (Discipline #13b section)

---

**Signed:** jack-ryan (DESIGN-MODE Gate-1)
**Verdict:** APPROVE-OPTION-C
**LC-009 closure pathway:** empirical inspection + math note + structural reinterpretation as deliverable; no ablation runs; intermediate tag `qd-rebuild/v0.7-ablation-lc-009` fires on closure commit; LC-011 cleared to proceed.
