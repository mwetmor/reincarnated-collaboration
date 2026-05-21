# Dispatch — jack-ryan Gate-1: W0.7 LC-009 Ablation Experiment Design Review

**From:** gamora
**To:** jack-ryan (Gate-1 reviewer — measurement validity)
**Date:** 2026-05-20
**Status:** PENDING GATE-1
**Reference:** W0.7 dispatch + B14.5 sidecar finding #2 (hunter modifier range)
**Math note:** `reincarnated-engine/src/reincarnated/simulation/math/w0-7-lc-009-ablation-design.md`

---

## What this Gate-1 reviews

Per LC-002 pattern: empirical inspection FIRST (Discipline #11), then math note (Discipline #1), then Gate-1 before execution. Gamora has completed both steps. This Gate-1 reviews:

1. Whether the empirical inspection findings are methodologically sound (era exclusion, path determination)
2. Whether the resulting ablation scope revision (Option C — no ablation required) is correctly reasoned
3. Whether the historical B14.5 sidecar finding #2 can be closed as a data quality artifact

---

## LC-009 experiment design summary

**Original finding (B14.5 sidecar finding #2):** Hunter modifier range = 1.82, the highest of all archetypes. Labeled "least consistent shape across seeds."

**Empirical inspection result (Discipline #11, 2026-05-20):**

The 1.82 figure is a mixed-era artifact. When segmented by schema era:

| Era | n | modifier range |
|-----|---|----------------|
| Pre-range_profile-schema (seasons 000013–000700) | 8 | 1.8207 |
| Post-schema CONVERGED only (range_profile='long') | 7 | **0.6234** |

The pre-schema records predate B6 archetype templates (no `energy_type`, `skill_power_tier`, `range_profile`, or `geometry_bias` per-class telemetry). They represent a structurally different class construction path.

**Path B confirmed:** The historical 1.82 range does not reproduce under post-W0.10 conditions. The current CONVERGED hunter modifier range is 0.6234 — within the mid-range of archetypes (wind_controller: 3.575; fire_mage: 0.474 for comparison).

**Surface verification result:**

All three dispatch-identified template variables have low to zero ablation power over the observed 0.6234 range:

| Variable | Power | Rationale |
|----------|-------|-----------|
| `range_profile=long` | Zero | Deterministic (`energy_type="focus"` → always long). No cross-seed variance. |
| `geometry_bias` (8-entry dict) | Zero | Constant weights per template. Seed-driven geometry *selection within* the bias pool is the variance source, not the bias weights. |
| `kit_size` (12–13) | Low | ±1 skill range too narrow to explain 0.62 modifier variance. Other archetypes with wider kit_size show lower variance. |

**Gamora's recommendation: Option C — no ablation required.** The signal the ablation was designed to explain (1.82 range) was a data quality artifact. The current 0.6234 range reflects designed behavior: per-season gauntlet composition and per-class seed interaction drive legitimate modifier differences. No structural hunter imbalance exists in the current era.

---

## Gate-1 questions requiring jack-ryan verdict

**Q1 — Surface verification correctness:** Does Gate-1 agree that `range_profile` (deterministic for focus energy), `geometry_bias` (constant weights), and `kit_size` (12–13 range) have low to zero ablation power over the 0.6234 post-schema hunter modifier range? Or does jack-ryan's constraint inventory identify a structural mechanism gamora's code audit missed?

**Q2 — Era exclusion methodology:** Is the decision to exclude pre-range_profile-schema records (seasons 000013–000700) from the LC-009 analysis methodologically correct? The exclusion rationale: pre-schema records used a different class construction path (no skill_power_tier=58 compensation, no range_profile enforcement, no explicit energy_type). They are not representative of the current generation pipeline.

**Q3 — Option C endorsement:** Does Gate-1 endorse closing LC-009 without ablation execution, with this math note as the deliverable? The alternative (Option A, gauntlet variance attribution) would cost ~53 min wall time (10 hunter seasons × 2 runs) and produce a gauntlet-vs-kit-seed partition of the 0.6234 range — low design value unless gauntlet diversity decisions are pending.

**Q4 — OQ-6 closure confirmation:** OQ-6 ("physical hunter modifier=1.0000 saturated despite boss_wr=0.0") was closed in W0.9.6 and confirmed by W0.10.5 re-sweep (hunter at 0.6355 wins 100% across all 5 tiers post-boss-AI-fix). Does Gate-1 confirm OQ-6 is fully closed and does not re-open under LC-009?

**Q5 — B14.5 sidecar finding #2 archival:** Does Gate-1 agree that sidecar finding #2 should be archived as "resolved via era-correction + W0.10 boss-AI fix" rather than "resolved via ablation"? No code changes are required; the finding was a measurement artifact.

---

## gamora position

Option C. The 1.82 range was data quality, not structural imbalance. The three dispatch variables have no power over the current post-schema variance. LC-009 closes with the math note + empirical inspection as the complete deliverable. LC-011 (controller/mage iteration overhead) is cleared to begin immediately upon Gate-1 endorsement of Option C.

---

## If Gate-1 selects Option A instead

If Gate-1 prefers Option A (gauntlet variance attribution), gamora will execute the following after Gate-1 approval:

- Run 1: 10 hunter full-regen seasons (seed 500001–500010), standard gauntlets, record CONVERGED modifiers
- Run 2: Same 10 seeds, fixed gauntlet (serialized from seed 500001), record CONVERGED modifiers
- Wall time: ~53 min (160s/season × 20 seasons sequential)
- Measurement mode: full regen (same rationale as LC-002 — smoke-test may alter modifier precision)
- Attribution: `modifier_range(Run1) - modifier_range(Run2)` = gauntlet contribution; remainder = kit-seed contribution

Gate-1 must specify: APPROVE-Option-C or APPROVE-Option-A before gamora proceeds.
