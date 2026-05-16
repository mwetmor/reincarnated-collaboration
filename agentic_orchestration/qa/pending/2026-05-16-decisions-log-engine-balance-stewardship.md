# Decisions-log entry drafts — Engine-balance stewardship (View A lock + divergence framework + movement-modeling approach) + B10.2 supersession

**Author:** knight-rider
**Date drafted:** 2026-05-16
**Source:** Gandalf's session-3 deliverable `canonical/story/engine-balance-stewardship.md` (461 lines) covering Gates 1-3 per knight-rider's 2026-05-16 commission. Companion entry supersedes the 2026-05-14 B10.2 Two-Gauntlet Pattern's "Convergence = full fidelity" clause per the Option 2 implementation path locked in jack-ryan's 2026-05-15 Gate 1 review.
**Process:** Knight-rider drafts → Matt approval → commit to `reincarnated-engine/design/decisions/decisions-log.md`. Same pattern as the five entries committed 2026-05-15 + 2026-05-16.

**Target location:** before the "Recently considered, not yet decided" section, after the 2026-05-16 research.db retirement entry.

---

## Entry 1 — Engine-balance stewardship: View A locked + divergence framework + movement-modeling approach

### 2026-05-16: View A locked as AOE balance philosophy; multi-dimensional divergence framework adopted; movement-modeling abstraction limitation named

**Decision:** Three load-bearing engine-balance design decisions are locked, addressing what Gandalf's drift-audit names as Drift-7 (View A/B/C unanalyzed-as-system), Drift-8 (Q1 divergence floor/ceiling never operationalized), and Drift-9 (Q2 movement speed in simulation empirically unknown). Per Gandalf's session-3 `canonical/story/engine-balance-stewardship.md` deliverable.

#### Lock 1 — View A is the canonical AOE-philosophy

AOE classes earn pack-clear-identity as **genre-correct archetype payoff**, not as a balance debt that requires numeric compensation. The locked position:

- **AOE classes:** carry pack-clear identity as their archetype payoff. No damage-ratio compensation required at the per-skill or per-class level.
- **Single-target classes:** retain a playable floor via **encounter-distribution**, not via per-skill damage scaling. The ~30% non-pack content in the gauntlet (boss / mini-boss / elite slots) is their natural home; pack content is reduced-efficiency, not helpless.
- **Compensating axis is content-distribution, NOT damage-ratio.** Per Legolas Pass-4 ARPG-community discourse: encounter design is the real lever, not flat damage ratios. PoE / Diablo II / D4 all converged on this. Reincarnated follows.
- **View B (pure damage-ratio compensation) is rejected.** It re-introduces the numeric-scaling anti-pattern that file 29's "shaped balance over numeric scaling" philosophy already locks against.
- **Q1 playable-floor constraint is satisfied** by the empirical jack-ryan finding (B10.4 sim: single-target classes show -25% non-pack KPM, not zero KPM). "Less-efficient against packs" is acceptable; "helpless" is not. The framing is preserved.

#### Lock 2 — Multi-dimensional divergence framework

Q1's divergence floor + ceiling + experienced-cost-parity framing becomes operational via a multi-dimensional check, NOT via a single-metric reading of the convergence framework's aggregate win rate:

| Constraint | Operational measure | Status |
|---|---|---|
| **Divergence floor** (distinct enough to feel like its own thing) | Player-behavior axis variance — 6 axes; ≥2 differing per archetype-mate pair | Active |
| **Divergence ceiling** (no helpless matchups) | Minimum win-rate per (class, content-type) pair ≥ 25% | Active |
| **Experienced-cost parity** | Deferred — future B-series item | Deferred |

The convergence framework's single-number aggregate win rate remains ONE input. The two additional checks layer on top:

- **Divergence floor (player-behavior axis variance):** per any two archetype-mates within the same class lineage, the engine must produce ≥2 differing values across 6 player-behavior axes (geometry mix / resource regen pattern / sustain expenditure / target prioritization / range engagement profile / cooldown rhythm). Operational check: at generation-validation time, the validator computes axis differences per archetype-mate pair and rejects classes that fail the floor.
- **Divergence ceiling (minimum WR per content-type):** the per-class win rate against EACH content-type slot (swarm / magic / trash / elite / mini-boss / boss / trial) must be ≥ 25%. Below that, the class is "helpless" against that content. Operational check: B10.4-style per-content-type win-rate tracking; reject classes that fall below the floor.
- **Experienced-cost parity** (total time × resource expenditure normalized per content slot per class): deferred to a future B-series item. The metric isn't structurally needed for v1 balance; it's a refinement that can land later.

#### Lock 3 — Movement-modeling abstraction limitation named; B-series item scheduled

Gandalf's Gate-3 empirical finding: the simulation is **NOT** fully movement-blind. It has positional state (`range_profile`, `at_melee_range`, `CLOSE_TO_MELEE_TIME=0.5s`, teleport range-closure). But it IS **movement-speed-blind** in the way Q2 framing requires (no `movement_speed` parameter consumed; no kiting modeling; no L1-vs-L50 movement-speed differentiation).

**Three-part decision:**

- **(3a) Name the abstraction limitation explicitly** in engine-design or equivalent canonical doc. Closes Drift-9 by naming it. Done by this decisions-log entry.
- **(3b) Movement-speed-aware sim extension scheduled as Stage A2 B-series item.** ~2-4 weeks gamora work covering: 4-band distance spectrum (close / mid-close / mid-far / far); kiting AI (single-target classes mitigate via distance); `movement_speed` parameter consumption (per-class baseline + per-level scaling); empirical re-validation of View A's -25% non-pack KPM finding under movement-speed-aware sim.
- **(3c) Implementation timing:** Stage A2 alongside B14.5 calibration work. Acceptable to defer if gamora's bandwidth is constrained; lock the position for now.

**Critical implication for Lock 1:** the View A finding's -25% non-pack KPM is from a movement-speed-blind sim. Real gameplay would have movement-speed-aware kiting (genre-standard mitigation per Legolas Pass-2 + Pass-3). The "less-efficient, not helpless" reading from Lock 1 is therefore **conservative** — real gameplay closes the gap further. Lock 1 holds; the empirical margin is wider than the sim suggests.

**Reasoning:** Per Gandalf's three-doc canonical-story sequence (`season-feel-rubric.md` → `drift-audit.md` → `engine-balance-stewardship.md`) commissioned 2026-05-16. Drift-7 / Drift-8 / Drift-9 are P5-pattern instances per drift-audit § 5 — multi-parameter system drift without joint analysis. The three locks address them as a cluster (not as isolated decisions). Resolving them together is the corrective per Gandalf's cross-gate synthesis.

The View A lock honors file 29's "shaped balance over numeric scaling" philosophy: classes differ by COMPOSITION first (archetype role + kit composition), NUMBERS last (per-class damage_modifier in tight 0.85-1.15 range). View B's damage-ratio compensation would re-introduce numeric scaling at the per-skill level; rejected.

**Alternatives considered:**

- **View B (damage-ratio compensation for AOE skills):** rejected. Conflicts with shaped-balance philosophy; introduces numeric-scaling anti-pattern at per-skill granularity; Legolas Pass-4 finding confirms genre consensus that content-distribution is the real lever.
- **View C (cost-mediated balance — AOE has same damage but higher cost / cooldown):** Gandalf's analysis surfaced that current sim has compound View-A-with-partial-View-B-damage-reduction (per jack-ryan Gate-1 empirical finding). The compound state is operative because the partial damage reduction (0.6×) is overwhelmed by lower cost + shorter cooldown + N=8× pack multiplier. Pure View C would require re-tuning all three compensating mechanisms; substantial work for ambiguous benefit. Rejected.
- **Single-metric divergence (convergence WR only):** rejected. Q1's three-constraint framing (floor + ceiling + cost-parity) cannot be captured by a single aggregate metric. Multi-dimensional check is the operational form.
- **Defer all movement-modeling work indefinitely:** rejected for (3a) and (3b) but accepted for (3c) timing flexibility. Naming the limitation now (Drift-9 close) is cheap and protects against future drift; the implementation can wait for gamora bandwidth.

**Status:** Active. Implementation cascades:

- **Gamora:** B10.4 milestone tag (`v1.3-b10-4-swarm-calibration`) unblocks. Option 2 implementation (per jack-ryan Gate-1 PASS WITH FLAGS finding) proceeds with View A as the locked AOE philosophy. Decisions-log entry sibling (below) supersedes B10.2's "Convergence = full fidelity" clause. Stage A2 B-series item added: movement-speed-aware sim extension.
- **Drax:** v0.7-encounter-analytics dispatch can now be authored. Viz interpretation bound to locked View A + multi-dimensional divergence framework as visualizable axes (player-behavior axis variance per pair; per-content-type win-rate distribution per class).
- **Rocket:** Future generation work uses divergence-floor as a generation-validation gate (axis variance check at class-generation time).
- **Star-lord:** Telemetry tier-1 fields (`duration_seconds`, `a_heals_received`, `a_potions_used`) feed the multi-dimensional divergence framework; no additional schema work for v1.

**Related:**
- `reincarnated-collaboration/canonical/story/engine-balance-stewardship.md` (Gandalf's full session-3 deliverable; 461 lines covering all three gates)
- `reincarnated-collaboration/canonical/story/drift-audit.md` § Drift-7 / Drift-8 / Drift-9 + § Pattern P5
- `reincarnated-collaboration/canonical/story/season-feel-rubric.md` (Gate-2 grounding)
- `reincarnated-collaboration/agentic_orchestration/qa/findings/2026-05-15-b10-4-option-2-and-aoe-philosophy.md` (jack-ryan Gate-1 empirical finding — View A operative)
- `reincarnated-collaboration/agentic_orchestration/dispatches/2026-05-16-gandalf-engine-balance-stewardship.md` (the commission)
- `canonical/29-design-overview.md` § "shaped balance over numeric scaling" (the philosophy this lock honors)
- `canonical/37-form-bias-diagnosis-and-recovery.md` § 10.1 (Q1 + Q2 + Drift-7/8/9 cross-references)
- 2026-05-14 B10.2 entries (Two-Gauntlet Pattern + B10.4 entries; superseded by sibling entry below)

---

## Entry 2 — B10.2 Two-Gauntlet Pattern supersession

### 2026-05-16: B10.2 Two-Gauntlet Pattern superseded — Option 2 (exclude pack fights from convergence binary search) is the canonical pattern

**Decision:** The 2026-05-14 B10.2 Two-Gauntlet Pattern entry's clause **"Convergence = full fidelity"** is superseded. The canonical convergence pattern is **Option 2** per jack-ryan's 2026-05-15 Gate-1 PASS WITH FLAGS review (`qa/findings/2026-05-15-b10-4-option-2-and-aoe-philosophy.md`): **convergence binary-search excludes pack fights**; the operative modifier definition is **non-pack WR = 50%**.

The two-gauntlet structure (recompose vs convergence) remains valid but the convergence side narrows: it now matches the recompose side in being proxy-free 1v1 for the purposes of binary-search target-finding. Pack fights still simulate (their telemetry still captures); they are not part of the convergence target calculation.

**Reasoning:** Jack-ryan's Gate-1 empirical finding showed that pack-fight WR ≈ 100% at any moderate modifier creates a structural win-rate floor of ~50% for the aggregate gauntlet. Binary-search target of 50% (the original B10.2 design) is mathematically unreachable for most classes — the class would need to lose 100% of non-pack fights, requiring a degenerate modifier. The B10.2 design's "Convergence = full fidelity" clause was correct in design intent (convergence should reflect actual play) but mathematically broken (50% target with a 50% pack floor cannot converge for sensible modifiers).

Option 2 (the locked replacement) preserves modifier semantic clarity — *"value at which class wins 50% of canonical 1v1 balance encounters"* — and aligns convergence with recompose's proxy-free 1v1 pattern. Pack fights become a separate diagnostic surface (not a convergence target). The two-gauntlet pattern's "convergence + diagnostic" framing is the corrective.

This entry is the supersession in decisions-log per the format convention ("When superseding or reversing an earlier decision, update its status and add a new decision explaining the change. Don't delete or rewrite — preserve the history of how thinking evolved."). The companion update: B10.2's status line should be updated from "Active" to "Superseded by 2026-05-16: B10.2 Two-Gauntlet Pattern superseded — Option 2."

**Alternatives considered (per jack-ryan's Gate-1 review):**

- **Option 1 (adjust convergence target from 50% to ~75% aggregate):** simple but muddies `modifier` semantics. What does "modifier = 0.94" mean if 0.94 calibrates against a variable 75% target that shifts with pack composition? The number loses interpretability. Rejected.
- **Reduce pack-slot count from 6 to 3 to lower the floor:** rejected. Changes gauntlet composition for sim-tuning rather than design reasons; obscures rather than solves the convergence-math problem. Pack-slot count should be set by gauntlet design intent, not by convergence-math considerations.

**Status:** Active. Supersedes the 2026-05-14 "B10.2 — Two-Gauntlet Pattern: Recompose vs. Convergence" entry's convergence-side clause.

**Cross-seam follow-on (in flight):** Gamora B10.4 milestone tag (`v1.3-b10-4-swarm-calibration`) is held pending Option 2 implementation + this entry landing. Per the engine-balance-stewardship entry above, Option 2 implementation can now proceed with View A as the operative AOE philosophy. After implementation + full regen confirms convergence works under Option 2, the milestone tag cuts.

**Related:**
- `reincarnated-engine/design/decisions/decisions-log.md` 2026-05-14 "B10.2 — Two-Gauntlet Pattern: Recompose vs. Convergence" (superseded by this entry)
- `reincarnated-collaboration/agentic_orchestration/qa/findings/2026-05-15-b10-4-option-2-and-aoe-philosophy.md` (jack-ryan's Gate-1 PASS WITH FLAGS finding)
- Companion entry above: 2026-05-16 engine-balance stewardship (the View A lock that informs the Option 2 path)

---

## Companion action — update 2026-05-14 B10.2 entry status

When the two new entries above commit, update the 2026-05-14 "B10.2 — Two-Gauntlet Pattern: Recompose vs. Convergence" entry's Status line from "Active" to **"Superseded by 2026-05-16: B10.2 Two-Gauntlet Pattern superseded — Option 2"**. Preserves history per the decisions-log format convention.
