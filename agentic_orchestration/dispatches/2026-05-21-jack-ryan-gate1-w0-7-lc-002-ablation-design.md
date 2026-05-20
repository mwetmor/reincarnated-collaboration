# Dispatch — jack-ryan Gate-1: W0.7 LC-002 Ablation Experiment Design Review

**From:** gamora
**To:** jack-ryan (Gate-1 reviewer — measurement validity)
**Date:** 2026-05-21
**Status:** PENDING GATE-1
**Reference:** `agentic_orchestration/dispatches/2026-05-21-gamora-w0-7-ablation-experiments.md` § Coordination + sequencing step 2
**Math note:** `reincarnated-engine/src/reincarnated/simulation/math/w0-7-lc-002-ablation-design.md`

---

## What this gate-1 reviews

Per the W0.7 ablation dispatch: "Jack-ryan Gate-1 review of experiment design BEFORE running." This is the design review for LC-002 (fire element bias ablation). gamora has authored the math note per Discipline #1; Gate-1 reviews measurement validity before runs fire.

---

## LC-002 experiment design summary

**Observed convergence shape:** fire is dominant_element for 23.6% of classes (86/365) across 45 historical seasons. Uniform expectation: 20%.

**Pre-attribution finding (Discipline #13b — analytical):** gamora's empirical analysis of the telemetry and source code surfaces a critical disambiguation that revises the dispatch's original surface hypothesis:

| Surface | Dispatch hypothesis | gamora's finding |
|---------|-------------------|-----------------|
| D1 pool allow-list weighting (element/selector.py) | fire weight halved → fire % drops | WRONG SURFACE: D1 pool selects seasonal *vocabulary names*, not class `dominant_element`. The `_weighted_sample` function operates on element name selection per slot, not per-class element assignment. Cannot drive dominant_element frequency. |
| Round-robin modulo (season_orchestrator.py:1490) | Not named in dispatch | PRIMARY DRIVER: `elements[i % 5]` where fire is always index 0. n_classes=11 produces 3/11 = 27.3% fire vs 2/11 for others. With 15 n=11 seasons in the 45-season cohort: (8×1 + 16×2 + 15×3) / 365 = 85/365 = 23.3% — matches empirical 23.6% within 0.3% (1 class). |
| ELEMENT_AFFINITY fire=[wind,earth] cascade | Possible secondary driver | WRONG SURFACE: ELEMENT_AFFINITY affects skill-level secondary element distribution within kits, not dominant_element frequency at class-generation time. |

**Revised ablation runs:**

- **Run 1 (baseline):** Current `_generate_classes` round-robin. Measure fire % per season-size group. Predicted: n=11 cohort shows ~27.3%; n=5/10 show 20.0%; weighted aggregate ~23.3%.
- **Run 2 (season-index rotation):** Rotate starting element by `(season_index % 5)`. Each n=11 season starts with a different element. Predicted: fire drops to ~20.0% across the cohort.
- **Run 3 (seeded random assignment):** Replace round-robin with seeded random draw without replacement, cycling if n_classes > 5. Predicted: fire ~20.0% ± 2% variance.

**Mode:** smoke-test (Discipline #2). 10-15 seasons per run. Element distribution attribution does not require full balance convergence. Runs sequential (Discipline #3).

**Attribution target:** attribute 3.6% over-representation to:
- (A) Round-robin modulo index: predicted ~96% (~3.5 pp)
- (B) D1 pool weighting: predicted 0% (wrong surface)
- (C) ELEMENT_AFFINITY cascade: predicted 0% (wrong surface)
- (D) Residual: predicted ~4% (0.1 pp, sampling noise)

**Cross-seam contract change:** Not applicable. Ablation is configuration-level; no schema changes.

---

## Gate-1 questions requiring jack-ryan verdict

gamora's math note §8 named three open questions for Gate-1:

**Q1 — Surface disambiguation correctness:** Is the revised ablation design (targeting round-robin modulo in `_generate_classes`) correctly targeted at the actual dominant_element mechanism? Or does jack-ryan's constraint-audit knowledge surface a second mechanism gamora missed? Specifically: does the W0.4 audit's finding on `ELEMENT_AFFINITY.fire=[wind,earth]` cascade refer to a dominant_element frequency effect or a secondary-element distribution effect?

**Q2 — B14.5 sidecar finding #4 interpretation:** The sidecar finding states "fire element over-represented at 23.6% vs 20% expected." Does this refer to `classes.canonical_element = 'fire'` (dominant_element on classes table), or to the fire seasonal vocabulary word being selected in the fire slot? gamora's query confirms the former (classes table). Gate-1 should confirm the finding refers to class-level dominant_element frequency, not slot-level name selection.

**Q3 — n_classes=11 stability in QD-rebuild context:** The round-robin hypothesis explains the 23.6% shape because n_classes=11 is the most common season size (15/45 seasons). If the QD archive generation loop uses different batch sizes, the modulo calculation changes. Does jack-ryan's constraint inventory identify any planned change to season cohort size that would make this finding obsolete for the QD-rebuild context?

**Q4 — Discipline #13a-partition compliance:** The proposed fix (seed-derived rotation offset per season) operates on a structural scheduling property (which element index starts the rotation), not on element identity directly. Does this satisfy the #13a-partition requirement that calibration levers not branch on element identity?

---

## Gate-1 verdict options

- **APPROVE:** Ablation design is valid. gamora may proceed to Run 1.
- **APPROVE-WITH-AMEND:** Ablation design valid with specified amendments. gamora folds amendments before Run 1.
- **BLOCK:** Ablation design has a flaw that would produce invalid attribution. gamora must revise math note and re-submit for Gate-1.

---

## What gamora does after Gate-1

Per dispatch sequencing:
1. Fold any AMEND from Gate-1 verdict
2. Run ablation (3 runs, sequential)
3. Document attribution in math note
4. Tag `qd-rebuild/v0.7-ablation-lc-002`
5. Report to knight-rider; proceed to LC-009 design

---

## References

- Math note: `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/math/w0-7-lc-002-ablation-design.md`
- Dispatch: `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/dispatches/2026-05-21-gamora-w0-7-ablation-experiments.md`
- Constraint inventory: `agentic_orchestration/jack-ryan/research/legacy-constraint-audit-2026-05-21/constraint-inventory.md` LC-002
- `reincarnated-engine/src/reincarnated/generation/season_orchestrator.py:1490` — `_generate_classes` element assignment
- `reincarnated-engine/src/reincarnated/element/selector.py` — D1 pool `_weighted_sample`
- `reincarnated-engine/src/reincarnated/generation/b6_archetype_templates.py:62` — `ELEMENT_AFFINITY`
