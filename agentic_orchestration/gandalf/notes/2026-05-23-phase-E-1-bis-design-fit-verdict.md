# Gandalf Design-Fit Verdict — Phase E-1-bis Remediation Options

**Authored by:** gandalf (Pattern-A in-session subagent return, captured by knight-rider for durability — gandalf's environment policy prevented direct file write)
**Date:** 2026-05-23
**For:** Matt (knight-rider routing); decision input on Phase E-1-bis path
**Authority anchor:** gandalf canonical authoring at `canonical/story/hive-mind-protocol-weapon-library-import-2026-05-22.md` (§ 6.4 Pattern 6 operationalization), `canonical/story/cleaning-policy-design-2026-05-22.md` (§ 4 math anchors; § 5.4 stratified-sampling contingency; § 7 hybrid sequencing rationale), `canonical/story/variant-cluster-policy-assignments-2026-05-23.md` (cluster-policy framework), `canonical/story/gear-heavy-promotion-2026-05-22.md` (§ 6 15-entry catalogue retirement as Pattern 6).

---

## Top-line

**A1 is correct. It is not undersized. The undersizing perception comes from confusing the dispatch's predicted output shape ("8–12 axes") with a design requirement of Pattern 6, which is the opposite — Pattern 6 *commands* no pre-imposition.** Concurring with knight-rider's STRONG lean on A1.

**But knight-rider's option set is missing the load-bearing finding: 94.46% fantasy_generic is a Phase D lineage-mapper artifact, not a substrate property.** Royal Armouries (38,127 rows, ~22% of pre-cleaning substrate, gandalf cleaning-policy § 5.2 mapping rule = `european`) appears to have fallen through to a `fantasy_generic` default rather than resolving to `european` or `unknown`. That is a Phase D bug. Until it is fixed or known-not-to-be-a-bug, every option that tries to rescue *lineage-structured* variance (B1/B2/B4/C1/C2) is operating on a substrate where 94.46% of rows carry a wrong cultural-lineage label. **I want this surfaced to Matt before any B-family remediation fires.** I am calling it E1 — Phase-D-bis lineage normalizer audit + re-fire — and adding it to the option set.

**B1 is not free — it is methodology tourism if A1 is accepted in parallel.** Knight-rider's MEDIUM lean on B1 as a 10-min spike is acceptable IF and only IF the spike is framed as "do we get axes 2-4 to stabilize at all, or is the structure genuinely thin." If the spike returns "still unstable," we are done; don't chain to B2/B3 looking for axes that aren't there.

**Two options knight-rider missed:**
- **E1 — Phase-D-bis lineage normalizer audit.** Investigate the 94.46% fantasy_generic and confirm or fix the Phase D mapper. (Surfaced above.)
- **B4-prime — stratified sub-sample by `source_library` rather than by `cultural_lineage_canonical`.** Because the lineage labels are corrupt, lineage-stratification compounds the corruption. Source-library stratification matches the substrate's *actual* structural origins (museums × encyclopedias × TRPG × MMO × soulslike × modern-military) and is robust to the Phase D mapping issue.

---

## Question-by-question

### Q1 — Design-intent fidelity per option

Authority anchor: hive-mind-protocol § 6.4.1 ("the aesthetic axes ... must be DERIVED from a statistically significant sample, NOT pre-imposed") and gear-heavy-promotion § 6.4 (15-entry catalogue retired from "canonical taxonomy" to "clustering hypothesis").

| Option | Pattern-6 fidelity | Notes |
|---|---|---|
| **A1** | HIGHEST | Literally the operational definition of "no axis pre-imposition." If 1 axis is what the data says, 1 axis is what we lock. |
| **B1** | HIGH | F5 honored; F2 parameter sweep is within-lock. Spike-cost ≈ correct. |
| **B2** | MEDIUM | Breaks F2 lock language. Defensible because F2's amplification factor at the singleton tail (1518×) is amplifying within-row noise, not lineage structure. Procedurally requires lock revisit. |
| **B3** | LOW | Pure ablation tourism. Zero evidence text features are the problem (all 4 axes load purely-structured in top-5). |
| **B4** | HIGH (with caveat) | Honors my own cleaning-policy § 5.4 contingency *explicitly*: "if Phase A audit reveals that 50%+ of substrate maps to `cultural_lineage=european`, the cultural axis loadings will be skewed. Optional Phase D-pre-Phase-2 step: stratified sampling." We're at 94.46% (lineage label corrupted or not, the imbalance is real). **The caveat is that lineage-stratification on corrupt labels compounds corruption** — see B4-prime below. |
| **B4-prime (new)** | HIGHEST among B-family | Stratify by `source_library` instead. Robust to Phase D mapping issues. |
| **C1 (NMF)** | HIGH (as supplement to A1) | NMF on TF-IDF + non-negative one-hot features is *theoretically better-suited* than PCA: components are additive topics, not orthogonal axes; topical structure of a monocultural-dominated substrate naturally fits NMF's strengths. Methodologically a clean F5 lock-revisit. |
| **C2 (mixed-effects)** | MEDIUM | Exotic; F5 lock-revisit warranted; build cost too high for current stage. Hold reserve. |
| **D1 (skip axes)** | MEDIUM | Throws away Axis 1, which is a real finding. **A1+D1 hybrid is the actual correct shape** — keep Axis 1 as the canonical anchor, cluster freely in the full feature space without trying to extract additional axes. Knight-rider already named this; it should be promoted to a named option. |
| **E1 (new) — Phase-D-bis lineage audit** | LOAD-BEARING PRE-REQUISITE | Until we know why 94.46% of the substrate is labeled fantasy_generic when ~22% of the substrate is museum holdings that should be european, we are running PCA on a misrepresented substrate. |

### Q2 — Goal of the exercise

**Discovery, primarily. Engine-feature production via clusters + canonical taxonomy, secondarily.**

The hive-mind protocol commits Pattern 6 to "no axis pre-imposition" (§ 6.4.1) and the gear-heavy-promotion retires the 15-entry catalogue *as a pre-imposed enumeration* (§ 6) — Pattern 6's entire reason for existing is to *replace pre-imposed taxonomies with data-derived ones*.

The engine's actual feature consumption is:
- **Clusters** as the gear-catalogue replacement (gear-heavy-promotion § 6 + variant-cluster-policy framework)
- **Canonical taxonomy categorical features** (lineage × period × register × weapon_kind × wieldable_humanoid — these are *already locked* in cleaning-policy § 5; PCA does not produce them, PCA *rediscovers* them)
- **BDI ω-scoring** on derived axes (W2.2; separate workstream from W2.1; can operate on whatever axis basis we end up with, including a 1-axis basis)

**The dispatch's "8-12 canonical axes" was a numeric expectation drawn from PCA-literature defaults for a richly-varianced substrate — not a design requirement.** When the substrate turns out to be monocultural (whether that's a real substrate property or a Phase D artifact), the data-derived axis count is whatever the data says it is. Pattern 6's contract is *honored*, not *violated*, by accepting 1 axis.

**The most important re-frame:** Axis 1 IS the `register_canonical` variable from my own cleaning-policy § 5 taxonomy. PCA rediscovered it as the dominant signal. That is a *positive empirical validation* of the canonical taxonomy I authored a day ago — the substrate's dominant axis of variance is precisely the axis the design *already committed to*. We should celebrate that, not treat it as failure.

### Q3 — Is 1 canonical axis sufficient for downstream Phase E-4 substrate-density?

**Yes.**

Phase E-4 substrate-density operates on `(element × range × gear_catalogue_id)` tuples (hive-mind-protocol § 6 Phase 5; selection-patterns schema). The cluster_id replaces gear_catalogue_id in the post-Pattern-6 architecture. Element comes from BDI ω-scoring (W2.2), which operates against *any* axis basis. Range is structured.

**Density precomputation needs:**
1. Clusters (primary discriminator)
2. Canonical taxonomy categoricals (lineage × period × register — already locked)
3. Element ω-affinity (separate W2.2 workstream)

It does **not** need ≥N discovered axes. The discovered axes are *orientation devices* for cluster interpretation, not density-bucket inputs. Density buckets are categorical (cluster_id + element + range). One discovered axis (register) is more than enough orientation to disambiguate ambiguous clusters.

**Conclusion:** A1's 1-axis output is downstream-sufficient. We do not need to chase axes 2-4 for E-4's sake.

### Q4 — F5 lock posture

**F5 is a methodology preference, not a load-bearing design commitment.** The lock has a built-in empirical escape clause ("If empirical evidence shows PCA insufficient ... document as Phase E-1-bis flag for Matt review — do NOT switch methods unilaterally"). That escape is being exercised correctly here.

Design-side locks that ARE load-bearing:
- **F2** (cultural-lineage inverse-frequency weighting principle) — operationally important; parameter-sweepable (B1 honors); should not be abandoned (B2 requires explicit revisit)
- **Cleaning-policy § 4 thresholds** (FP rate ≤3%, dedup recall ≥92%, etc.) — load-bearing for downstream cluster purity
- **Cleaning-policy § 5 canonical taxonomy** (lineage × period × register; already locked) — load-bearing for engine consumption
- **No-axis-pre-imposition discipline** (Pattern 6 itself) — load-bearing for design-fidelity

F5 (PCA-primary) can be relaxed if data demands. From the design-side seat, the path is:
- A1 (accept PCA's empirical answer) honors both F5 and Pattern 6 — preferred
- C1 (NMF as supplement) requires F5 revisit but is methodologically motivated by the empirical evidence (substrate doesn't have linear-orthogonal structure beyond Axis 1; NMF's additive-topic structure may surface meaningful sub-structure within the monoculture)

**My posture: defend F5 as starting-method default, but accept that it has been empirically tested and one of two things follows — A1 (lock the empirical result) or C1 (try NMF as method-switch with Matt approval).**

### Q5 — Ranked recommendation

**Tier 1 — Pre-requisite (must precede or run in parallel):**

**E1. Phase-D-bis lineage normalizer audit.** Confirm or fix the 94.46% fantasy_generic figure. Specifically: (a) for each source_library, query the post-Phase-D distribution of cultural_lineage_canonical; (b) verify that royal_armouries rows (~38K pre-cleaning, ~3.5K-8K post-canonical-merge) map predominantly to `european`, not `fantasy_generic`; (c) similarly verify met-museum, wikipedia, wikidata, modern-military source rows. If the mapper is broken, fix and re-fire Step 6.5 canonical normalization (Phase D math note §2.7) before re-running Phase E-1. **Cost:** ~1-2 hours of elrond Mode A diagnostic; potentially 0.5-1 day of mapper fix + Phase E-1 re-run. **Reasoning:** without this, B-family options are running on corrupt labels.

This is not a remediation option in knight-rider's sense — it is *prior work* that may obviate or reshape several B-family options.

**Tier 2 — Primary path (regardless of E1 outcome):**

**1. A1 — Accept-and-reframe (with A1+D1 hybrid implementation).** Lock Axis 1 (register: historical-vs-fantasy) as the one canonical discovered axis. Run HDBSCAN on the full 160-d (or 60-d structured-only, ablation-tested) feature space — *not* on the failed 4-axis projection. Phase E-2 designer-labels Axis 1 + the emergent clusters. Phase E-4 consumes cluster_id + canonical taxonomy categoricals.

Pattern 6 fidelity: highest. Cost: lowest (re-run Deliverable 3 only). Risk: none methodologically.

**Tier 3 — Optional refinements (only if A1+D1 surfaces something unsatisfying):**

**2. C1 — NMF supplemental.** *Not as a replacement* for A1 — as a complementary view. NMF on the same feature matrix may surface additive topical structure within the fantasy_generic monoculture that PCA cannot, because NMF doesn't require orthogonality. Treat as a "second method confirms / extends" rather than a "PCA failed, NMF rescues" reframe.

**3. B4-prime — Stratified sample by source_library.** Run if A1+D1 clusters look thin or fantasy_generic-dominated. Source-stratify (~1,000-2,000 rows per source_library bucket) and re-do PCA on the balanced sub-substrate to see if axes 2-4 surface within the balanced view. Robust to E1 issues.

**Tier 4 — Conditional / spike (only if specific evidence demands):**

**4. B1 — Cap F2 at 100×.** Acceptable as a 10-min spike *if framed* as "does capped F2 stabilize axes 2-4 at all" — knight-rider's MEDIUM lean is fine *if and only if* the spike does not chain into B2/B3 hunting for axes that aren't there. If B1 returns "still unstable," stop. Do not iterate.

**5. B4 (as knight-rider authored — stratify by lineage).** Only if E1 confirms lineage labels are *correct* (i.e., the 94.46% fantasy_generic is real, not a mapper artifact). B4-prime (source-stratification) is dominant in the meantime.

**Tier 5 — Reserve / hold:**

**6. B2 (drop F2).** Hold for if A1+B1+B4-prime+C1 all surface nothing.
**7. C2 (mixed-effects PCA).** Hold reserve; build cost too high for present stage.
**8. B3 (drop LSA text).** Reject. Pure ablation tourism. Top-5 loadings are already structured-dominated; removing text features on speculation costs information for no benefit.
**9. D1 in pure form.** Reject in pure form (throws Axis 1 away). Use A1+D1 hybrid as Tier 2.

---

## What I am pushing back on (vs knight-rider's lean)

1. **Concur on A1 STRONG lean.** Same authority anchor (my own canonical authoring on Pattern 6 non-pre-imposition). I argue more aggressively than knight-rider: A1 is not just "possibly THE answer" — it *is* the answer the methodology was designed to honor.

2. **Push back on B1 MEDIUM-lean framing.** B1's 10-min spike is fine as a tightly-bounded test of "does capped F2 stabilize axes 2-4 at all." It is methodology tourism if it becomes a slippery slope to B2/B3/C1 chained-attempts at squeezing axes out of a substrate that already told us it has one canonical axis.

3. **Surface a load-bearing finding knight-rider missed.** 94.46% fantasy_generic is almost certainly a Phase D mapper artifact (Royal Armouries 38K rows should resolve to european, not fantasy_generic). This is more important than choosing between A1/B1/C1 — it is *prior to* the methodology question. **I want Matt to see this finding explicitly, not buried inside the option-set framing.**

4. **Add E1 and B4-prime to the option set.** E1 is Phase-D-bis prerequisite work. B4-prime is the lineage-corruption-robust alternative to B4.

5. **The "what survived" framing already provided by knight-rider deserves louder celebration.** Axis 1's top loadings (`register_historical +0.39 / register_fantasy −0.39 / period_fictional −0.37 / kind_category +0.36 / kind_named_template −0.36`) are PCA *empirically validating the canonical taxonomy I locked in cleaning-policy § 5 a day ago.* The substrate's strongest axis of variance is the register × kind interaction — which is exactly what the design predicted matters. This is a *positive* signal, not a salvage operation. Treat it as such in the framing to Matt.

---

## Player-experience anchor (Pattern-A required)

The engine produces gear-substrate via cluster sampling + canonical-taxonomy filtering. The player experiences this as: "this kit feels like a historical-medieval kit" vs "this kit feels like a fantasy-mythic kit" vs "this kit feels like a fantasy-comic kit." That is the register axis the player perceives.

**A1 gives the engine exactly one orthogonal slider — register — for the player's coarsest aesthetic-coherence experience, plus N clusters for finer-grained shape-coherence.** That is enough. Diablo II shipped with effectively two aesthetic registers (dark-gothic-medieval × dark-Eastern) and N weapon clusters; the register slider × cluster matrix produced kits that felt thematically coherent without 12 axes.

The risk of chasing 12 axes through B/C-family remediation is producing axes that *cluster algorithms can extract* but *players cannot perceive*. The discipline-#18 warning in hive-mind-protocol § 6.5 ("looks-correct-but-subtly-wrong" — clusters that pass cluster-validation metrics but don't carry design-meaningful weight) applies *in reverse*: axes that pass numerical-variance criteria but don't carry player-perceptible weight. PCA giving us 1 axis that perfectly aligns with the player's coarsest register-perception is a *finding*, not a failure.

---

## Bottom line for knight-rider

1. **Surface E1 (Phase-D-bis lineage audit) to Matt before any remediation fires.** This is the load-bearing finding hiding under the option-set framing.
2. **If E1 confirms 94.46% is a Phase D bug, fix and re-fire Phase E-1.** The post-fix axis discovery may surface axes 2-4 stably without any methodology change.
3. **If E1 confirms 94.46% is real (substrate genuinely is that fantasy-monocultural):** proceed to A1+D1 as Tier 2. The substrate has one canonical axis + clusters, and that is the truth of the substrate.
4. **B1 spike is acceptable as bounded confirmation, not as the start of a B/C-family chain.** One spike; if it doesn't move stability into PASS, stop and commit to A1.
5. **C1 (NMF) is held as a real second-method supplement, not as a PCA-rescue.** Only fire if A1+D1 produces clusters that gandalf Phase E-2 cannot label meaningfully.
6. **Reject B3 outright.** Methodology tourism.

— gandalf
