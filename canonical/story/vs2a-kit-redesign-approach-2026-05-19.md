# VS2a Kit-Redesign Approach — Path Decision

> **STATUS:** HISTORICAL-INFORMATIVE (pre-Epoch-4; consult for lineage only — not current truth) — see `canonical/00-ground-state.md` for current truth

**Status:** **DECIDED.** Authored 2026-05-19 by gandalf under autonomous-operation L2-equivalent authority (Matt directive 2026-05-19; protocol § 4.0; F2 dispatch).
**Tag fires on this disposition:** `vs2a/v0.5-kit-redesign-approach-decided`.
**Predecessors:** `r1-kit-redesign-queue-2026-05-19.md` (§ 5 path alternatives); `R1-blocker-3-disposition-2026-05-19.md` (encounter recalibration); `r8-disposition-2026-05-19.md` (Sub-case 3 / `inverted` default committed); `r2-h1-disposition-2026-05-19.md` (category-of-completion precedent).
**Gates:** S1 (kit-redesign sprint; rocket + gandalf consult) AND S2 (B6 main work; rocket pre-work + gamora main).

---

## § 0 — TL;DR

**Path (b) — full R8-inversion regeneration, with first-batch validation gate.** The shipped catalogue is regenerated end-to-end under the `inverted` pipeline (R8 disposition default). A 3-class first-batch validation runs before commitment to the full 51-class regen. The R1 sprint re-run is the canonical completion metric, applied at first-batch (≥ 1 boss kill at boss_kill_rate ≥ 0.10 + ≥ 2 of 3 classes acceptable) then at full-catalogue (70-85% per-tier pass-rate target). Curated identity is preserved through the coalescence layer — R8 Test 1 demonstrated +0.20 cohesion above baseline, and the 3-season R8 A/B already produced more boss-tier-functional kits than the entire 51-class shipped catalogue.

**One-paragraph rationale:** The shipped catalogue's pathology — archetype-mechanic mismatch (lightning_mage at melee range), single-vector defensive layer, range-collapse — is an *artifact of theme-driving-mechanic* under the legacy `baseline` pipeline. R8 inverts that ordering: mechanic converges first, theme coalesces around it. The empirical 3-season R8 A/B already produced classes (Saltfire Keeper at boss_kr 0.14; Saltwise water_mage at boss_kr 0.22 / mini_kr 0.24) that exceed every shipped class on boss-tier viability, with diverse geometry palettes (multi_projectile + teleport + dash_attack + self_buff coexisting in one kit) that the shipped catalogue lacks structurally. Hand-redesign of 30-40 classes (path a) is 4-6 weeks of rocket bandwidth fighting against a generator that is, post-R8, no longer the one that produced the pathology. Hybrid (path c) leaves a permanent two-generation-mode archaeology in the catalogue and creates dual-shape coordination overhead with no offsetting benefit — the kit-acceptable subset will be subsumed by R8-inversion regeneration that is, in the cohesion + boss-viability sense, *strictly better than the shipped baseline*. The decision is to regenerate the catalogue under the engine's now-committed default, with a first-batch test to confirm the empirical signal scales.

---

## § 1 — Decision criteria applied

### § 1.1 — Empirical kit-viability comparison (R8 A/B vs shipped sprint v2)

Direct comparison of the 3-season R8-inverted A/B output (seed 99002, Drowned Lighthouse, brine) against shipped-catalogue sprint v2 (51 classes, 5 seasons, baseline pipeline):

| Metric | Shipped catalogue (51 classes) | R8-inverted seed 99002 (10 classes) |
|---|---|---|
| Best boss_kill_rate | 0.033 (class_0019 only) | **0.22** (class_0007 water_mage) |
| Classes with boss_kill_rate ≥ 0.10 | 0 / 51 (0.0%) | **2 / 10 (20.0%)** |
| Classes with mini_boss_kill_rate ≥ 0.15 | 0 / 51 (0.0%) | **3 / 10 (30.0%)** |
| Kits with diverse geometry palette (≥ 4 distinct geometry_types in skills) | rare (lightning_mage class_0016 has 1 effective — chain_lightning) | **majority** (class_0001 has 5; class_0006 has 7; class_0007 has 6) |
| Kits with multi-vector defensive layer (≥ 2 distinct survival mechanisms) | rare (most have 1 self_buff shield) | **majority** (teleport + shield + buff_dodge in class_0001; blink + self_buff + vortex_pull in class_0002) |

**Inference:** R8-inverted, even under the *old encounter calibration* (pre-disposition-3), already outperforms the shipped catalogue on the metrics that define R1's per-tier gate. This is the strongest empirical signal that the pathology is generator-shape, not modifier-tuning.

### § 1.2 — Substrate-identity invariance (R8 Test 4)

R8 disposition § 2d: substrate-identity is invariant at the canonical-element level across baseline and inverted pipelines. `inverted` with per-entity LLM naming preserves substrate-mode-of-action in ~90% of player-facing names. This is *equal to* the shipped baseline's preservation rate. **There is no substrate-identity loss from regenerating the catalogue under the committed default.** The mechanical substrate (canonical element distributions per seed) is byte-identical; what changes is the surface naming — and R8 Test 1 demonstrated that coalescence-derived naming reads as *more cohesive* (+0.20 above baseline) than input-themed naming.

### § 1.3 — Curated-identity preservation argument (refuted at scale)

The strongest argument for path (a) hand-redesign was preservation of curated kit identity — "Chartbound Stormscribe" has a name, a flavor, a position in the cosmology. The R8 A/B output rebuts this empirically: "Saltfire Keeper", "Keeper of the Drowned Flame", "Barnacled Warden", "Drowned Beacon Seep" are all R8-inverted productions. They are not less curated; they are *more* internally coherent (cohesion +0.20 above baseline) because the theme coalesced around mechanical convergence rather than being imposed as input.

Concrete examples from R8 inverted seed 99002:
- **class_0001 "Saltfire Keeper"** — fire_mage / range_profile=medium. Flavor text: "the old lighthouse burned for three hundred years before the sea finally swallowed it." Skills span burst_damage (single_target), area_damage (multi_projectile), mobility (teleport ×2), defensive (self_buff). This is a *better-realized* fire-mage-with-water-coupling than anything in the shipped catalogue.
- **class_0007 (water_mage, medium)** — boss_kr 0.22, mini_kr 0.24. Diverse geometries: blink, circle, multi_projectile, self_buff, single_target, vortex_pull. This kit *beats every shipped class on both boss and mini-boss tiers* and has 6 distinct geometry types.

The curated-identity worry is reframed: **the shipped catalogue's curated identity is partially fictional** — lightning_mage class_0016 has a great name (Chartbound Stormscribe) but a melee-range kit that doesn't honor the name. Hand-redesigning to honor the name forces a kit that the legacy generator did not produce; R8-inversion produces kits that honor their generated names by construction.

### § 1.4 — Cost (rocket bandwidth + LLM)

| Lever | Path (a) hand-redesign | Path (b) R8-inversion regen | Path (c) hybrid |
|---|---|---|---|
| Rocket effort | 4-6 weeks (per-class judgment for 30-40 classes) | 1-2 weeks regen orchestration + 0.5 wk gandalf cohesion judging at first-batch | 3-4 weeks (combined per-class + regen sub-batches) |
| LLM cost | ~$0 (no regen) | 5-6 seasons × ~$3.20/season = ~$16-19 | ~3 seasons regen × $3.20 = ~$10 + per-class hand work |
| Risk profile | low generator risk; high curation drift; per-class hand-tuning may not generalize | empirically validated at 3 seasons; first-batch gate de-risks scale | dual-mode catalogue archaeology persists; coordination overhead |

Cost is *not* the deciding factor; rocket bandwidth is. Path (b) frees 3-4 weeks of rocket bandwidth that can advance S2 (B6 main work) earlier, which is the next gate after S1.

### § 1.5 — Hybrid (path c) explicit rejection

Path (c) was tempting because it preserves the ~5-10 kit-acceptable shipped classes. Three reasons it fails:

1. **Catalogue archaeology cost.** A mixed-mode catalogue carries a permanent "this class is from the pre-R8 pipeline; this class is from the post-R8 pipeline" lineage burden. Drift-14 already documents the catalogue's drift surface; mixing modes deepens that surface, doesn't resolve it.
2. **kit-acceptable identification is provisional.** The 5-10 "kit-acceptable" classes are only acceptable under disposition-3 encounter recalibration; the disposition-3 calibration has not yet shipped (gamora sprint v3 not yet run). The kit-acceptable subset can't be enumerated until v3 lands; freezing path-decision against an unknown subset is premature.
3. **R8-inversion is not worse than acceptable-shipped at scale.** R8 Test 1 demonstrated coalescence-cohesion +0.20 above baseline. The kit-acceptable shipped classes are passing the *recalibrated* gate, not winning a cohesion contest. Regeneration under R8 produces kits with substrate-identity preservation + cohesion gain + viability gain by construction.

**The hybrid path's curated-preservation value is dominated by R8-inversion's cohesion + viability + uniformity gains.** Reject path (c).

### § 1.6 — Decision criteria summary

| Criterion | Weight | Path (a) | Path (b) | Path (c) |
|---|---|---|---|---|
| Empirical boss-viability evidence | HIGH | uncertain; depends on per-class judgment generalization | **proven 20% rate in 3-season A/B** | partial |
| Cohesion preservation | HIGH | uncertain; hand-redesign may drift from theme | **proven +0.20 above baseline** | partial |
| Substrate-identity preservation | HIGH | preserved | **preserved (R8 Test 4)** | preserved |
| Rocket bandwidth efficiency | HIGH | 4-6 wk | **1-2 wk + 0.5 wk gandalf** | 3-4 wk |
| Catalogue uniformity | MEDIUM | uniform (legacy) | **uniform (R8-inversion)** | mixed-mode archaeology |
| Risk profile | MEDIUM | low generator risk; high per-class judgment risk | **moderate, de-risked by first-batch gate** | dual coordination overhead |
| Cost (LLM) | LOW | ~$0 | ~$16-19 | ~$10 |
| First-principles alignment with R8 disposition § 2a | HIGH | leaves legacy classes in tension with new default | **commits to engine default** | undermines disposition |

**Path (b) dominates on every HIGH-weight criterion. Decision: path (b) full R8-inversion regeneration with first-batch validation.**

---

## § 2 — Path (b) implementation shape

### § 2.1 — Scope of regeneration

**Full catalogue regenerate.** All 51 shipped classes across 5 seasons (002011-002015) are replaced by newly regenerated seasons under the `inverted` pipeline (post-R8-disposition CLI default).

**Seed strategy:** new seeds in the `vs2a/` range (e.g., seed 100001-100005 or similar; rocket chooses; the specific seed range is rocket-seam authority). **Old seeds are retired**, not preserved. This is the cleanest cut: the regenerated catalogue is a new generation, not an attempted re-roll of the existing one. R8 substrate-identity invariance is at the *seed × engine-version* level — different seeds produce different substrate distributions, so attempting "re-roll the same seed" is not the operational frame; the frame is "ship new content under the new default."

**Number of seasons:** rocket determines per VS2a season count goal — likely 5 seasons to match the current shipped count, or potentially 4-6 depending on convergence-failure rate observed in regen (R8 A/B showed 5-9 convergence_failures per 10-11-class season; rocket may need more season-iterations to reach 51 kit-acceptable classes).

**Class count target:** ~51 viable classes shipped at the end (matching current count). If R8-inversion produces ~45 viable across 5 seasons, rocket may regenerate a 6th season to backfill; gandalf review at the time.

### § 2.2 — Manifest continuity

Old `season_002011` through `season_002015` are *replaced*, not augmented. The shipped catalogue prior to S1 is preserved in git history under the engine-rebuild closure tag `hive-rebuild/v1.0-engine-rebuild-complete`; rollback to pre-VS2a catalogue is git-walkable if ever needed.

The new seasons take new IDs (e.g., `season_100001` through `season_100005`). Manifest.json files reflect new `season_id`, new `generation_seed`, new `engine_version` (per F1 `geometry_type` schema field landing concurrently). MIGRATION.md at the generation seam (rocket appends) captures: old seasons deprecated; new seasons under new IDs; downstream consumers (sim balance loop, demo, loadout app) read whatever the current manifest.json declares as the latest catalogue.

### § 2.3 — Prompt-augmentation: does kit-redesign-queue § 3 enter the regen?

**No prompt-augmentation at the LLM coalescence layer.** The R8 disposition committed `inverted` as a mechanical-first + theme-coalesces-after pipeline. Injecting the kit-redesign-queue criteria (range diversity, defensive-layer, burst-window, archetype-alignment, energy-cycling) as LLM prompt constraints would *un-invert* the pipeline — it would re-introduce theme-as-input under a different name.

**Instead: validate the criteria post-hoc at the validation gate.** R1 sprint re-run measures whether the regenerated catalogue passes the per-tier gates; that is the empirical surfacing of the criteria (a kit with no range diversity, no defensive layer, no burst-window cannot pass boss-tier — the criteria are *implicit* in the R1 measurement). If regenerated kits systematically fail one criterion (e.g., universal range-collapse persists), that surfaces as an R1 failure pattern and gandalf authors a follow-on disposition — but the prompt itself stays clean.

This is the same architectural discipline as R8 § 2a: trust the coalescence; measure the output; do not pre-constrain it.

### § 2.4 — First-batch validation (CRITICAL gate before scale)

**Before committing to full 5-season regen, rocket regenerates 1 season (a "first-batch" containing ~10-11 classes) under the new pipeline + concurrent F1 `geometry_type` schema landing.** Gandalf reviews the first-batch under explicit cohesion-judging protocol (same as R8 § 4 / R8-cohesion-judging-protocol-2026-05-19.md). Gamora runs R1 sprint against the first-batch classes.

**First-batch PASS criteria (all must hold):**

1. **≥ 1 class achieves boss_kill_rate ≥ 0.10 under disposition-3 calibration.** This is reachability evidence — the regenerated catalogue produces at least one boss-tier-viable kit.
2. **≥ 2 of the first-batch classes achieve mini_boss_kill_rate ≥ 0.15 under disposition-3 calibration.** This is mid-tier-functional evidence.
3. **Gandalf cohesion judgment: ≥ 4.0 mean cohesion across 6 facets** (per R8 cohesion-judging-protocol). Matches the inverted-arm performance in R8 Test 1.
4. **No "Unknown" or template-debris in player-facing names** (the failure mode that disqualified `inverted_no_naming` per R8 disposition § 2b). The committed `inverted` mode does not produce this, but verify in the first-batch.
5. **Substrate-identity preservation at canonical-element level: invariant** (R8 Test 4 pattern; gandalf samples 2-3 skills against pre-regen substrate references).

If all 5 PASS: rocket proceeds to full 5-season regen. If any FAIL: gandalf authors a follow-on disposition per R8 / R2 precedent pattern (regen-PARTIAL-PASS, identify gaps, decide whether to amend pipeline or fall back to path (a) hand-redesign).

**First-batch validation cost:** ~1 season regen ($3.20 LLM) + 0.5 day gandalf cohesion judging + 1 day gamora R1 sprint = ~3 days wall.

### § 2.5 — Concurrent prerequisites (gating)

- **F1 (`geometry_type` schema field) must ship before regen.** Path (b) requires F1's explicit geometry_type field at generation time so the redesigned kits express their geometric character cleanly (multi_projectile, teleport, vortex_pull, etc.). R8 A/B already shows this field populated in the inverted output (geometry_type field is present in the JSON), confirming F1 is partially in place — but the schema landing makes it *authoritative* rather than an emergent generator artifact.
- **F2 (this decision) is the path commitment.**
- **R1 disposition-3 encounter recalibration** must be landed in gamora's R1 sprint v3 before the first-batch validation runs (otherwise the boss-kr ≥ 0.10 threshold is measured against the pre-disposition encounter that we've already proven unreachable). This is upstream of S1 in the DAG; knight-rider sequences.

### § 2.6 — First-batch class selection criteria

**Not "which existing classes to regenerate first" — there's no existing-class-to-regen mapping in path (b).** The first-batch is *one fresh regenerated season* under the `inverted` pipeline; the classes that emerge are whatever the converged pipeline produces.

**What gandalf reviews in the first-batch (analogous to "first-batch class selection criteria"):**

- **Archetype-tag coverage in the emergent batch.** If all 10 emergent classes are *_mage / *_controller (typical R8-inverted bias toward magical kits per Test 2 entropy data), surface to gandalf for follow-on disposition; may need a "second seed to fill warrior/hunter coverage" sub-step. The shipped catalogue has 15+ hybrid_mage classes; the R8-inverted seed 99002 had only 2 fire_mage entries (better diversity). gandalf checks: does the first-batch cover *_mage + *_warrior + *_caster + *_controller + hunter + grappler + experimental?
- **Range_profile distribution.** All-close kits in the batch reproduce the shipped pathology; mixed close/medium/long is the desired distribution. R8-inverted seed 99002 produced 1 close + 6 medium + 2 long + 1 close — already healthy. gandalf checks the first-batch matches this distribution profile or better.
- **Defensive-layer composition.** Per R8 A/B sample, the inverted classes already produce multi-vector defensive layers (teleport + self_buff + buff_dodge). gandalf samples 3 classes from the first-batch; verifies each has ≥ 2 distinct survival mechanisms.
- **Geometry-type diversity per kit.** R8-inverted seed 99002 produced kits with 4-7 distinct geometry_types per kit. Confirm first-batch matches this profile.
- **The kit-broken extreme pathology (shadow_mage class_0018/0045 saturated-modifier-AND-floor-failing pattern) does NOT reappear.** This is the strongest test of whether the regen path resolves the deepest pathology. If the first-batch produces a class that saturates modifier 4.0 with multi-tier failure, that surfaces as a failure mode worth design dispatch — but the R8 A/B already shows this pattern is absent under `inverted` (worst class in seed 99002 sits at modifier 0.05 floor with bottom-tier kits, not at ceiling).

### § 2.7 — Full-catalogue regen post-first-batch

Once first-batch passes the § 2.4 gate:

1. **rocket regenerates 4 more seasons** in sequence (or parallel if compute permits) under same `inverted` pipeline. Total: 5 seasons × ~10-11 classes = ~50-55 emergent classes.
2. **gamora runs full R1 sprint** against the regenerated 50-55 class catalogue.
3. **gandalf reviews full output** for cohesion + diversity + archetype coverage + identity continuity (post-VS2a-shipped catalogue should feel like a coherent set; gandalf samples 8-10 classes for the cohesion review).
4. **Acceptance metric:** R1 sprint achieves 70-85% per-tier pass-rate (per R1 disposition-3 PASS criterion § 7.2 sub-claim) under the disposition-3 encounter calibration. This is the gandalf-stewardship's commitment to the R1 hypothesis-test threshold being genuinely met at the catalogue level (the kit-redesign-queue § 5.1 promise).

---

## § 3 — B6 / S2 main-work implications

Per scope-of-work-vs2a § 2.3: "if F2 chooses R8-inversion path, B6 main work may shape differently (skill tree emerges from converged class composition; not authored as constraint-input)."

### § 3.1 — Shape change: skill tree authored against the *regenerated* catalogue

S2 (B6 main work; rocket pre-work + gamora main) reshapes as follows:

**Before F2 path (b):** B6 pre-work assumed energy-type-aware tier assignment against the shipped catalogue's 51 classes; B6 main work was authored as a constraint-input layer on existing class kits.

**Under path (b):** B6 pre-work waits for first-batch validation (or runs against the first-batch as a smoke); B6 main work is authored against the regenerated catalogue. Skill-tree structures emerge from the converged class composition rather than being pre-authored as inputs to it.

**Operational implication:** S2 main work shifts ~1-2 weeks later in the sequence (waits for first-batch gate + initial regen seasons). The net schedule impact is minimal because S1 itself completes faster under path (b) (1-2 wk regen + first-batch vs 4-6 wk hand-redesign) — the time saved on S1 is roughly the time deferred to S2.

**Rocket pre-work directive:** B6 pre-work (energy-type-aware tier assignment) should be parameterized to run against *any* catalogue shape — pre-work outputs should not encode class-specific class IDs as hard references. This is the implicit prerequisite for path (b); confirmation should be in rocket's AGENT_STATE before S2 fires.

### § 3.2 — S1 + S2 sequencing under path (b)

Refined DAG (replaces coordination-matrix-vs2a.md § 2 sub-graph at the S1 + S2 nexus):

```
F1 (geometry_type schema) ──┐
                            ├──► First-batch regen (1 season; rocket)
                            ├──► Gandalf cohesion judging (0.5 day)
F2 (this decision) ─────────┤    Gamora R1 sprint v3 first-batch (1 day)
                            │
R1 disposition-3 sprint v3  ┤    │
(gamora) ──────────────────┘    │
                                 ▼
                            First-batch PASS gate (§ 2.4 criteria)
                                 │
                                 ├─── PASS ──► rocket regenerates 4 more seasons
                                 │            (full catalogue ~50-55 classes)
                                 │                  │
                                 │                  ▼
                                 │            Full R1 sprint (gamora)
                                 │            70-85% pass-rate target
                                 │                  │
                                 │                  ▼
                                 │            S1 ships (tag vs2a/v0.7)
                                 │                  │
                                 │                  ▼
                                 │            S2 B6 main work begins
                                 │            (against regenerated catalogue)
                                 │
                                 └─── FAIL ──► gandalf authors follow-on
                                              disposition; path-decision re-opens
```

### § 3.3 — B6 skill-tree UI (F4) — no change

F4 (drax B6 skill-tree UI surface decomposition) is unaffected. The UI surface is authored against the skill-tree data contract (S2 emits the data; F4 renders it). The contract shape is the same regardless of catalogue origin.

---

## § 4 — Validation gate (S1 + R1 sprint re-run)

### § 4.1 — Two-stage validation

**Stage 1 (first-batch; ~1 season regen):** § 2.4 PASS criteria (5 sub-claims). Stops the path if regen-at-scale would fail; ~3 days investment de-risks ~$13-16 of LLM cost + 1-2 weeks rocket bandwidth.

**Stage 2 (full catalogue; ~5 seasons regen):** R1 sprint achieves 70-85% per-tier pass-rate under disposition-3 calibration. This is the canonical metric per kit-redesign queue § 5.1. The 70% threshold is the original R1 hypothesis-test target; recovering it at the catalogue level was the kit-redesign queue's promise; this disposition commits to that promise.

### § 4.2 — PASS / PARTIAL / FAIL re-disposition framework

Same shape as R1 disposition-3 § 7.2 and R8 disposition Sub-case classification:

**PASS (70-85% per-tier pass-rate; cohesion ≥ 4.0; substrate-identity preserved; first-batch gate cleanly passed):**
- Tag `vs2a/v0.7-kit-redesign-sprint-complete` fires
- S2 dispatch unblocks against regenerated catalogue
- Decisions-log entry authored by jack-ryan capturing path-decision + R1 hypothesis-test recovery

**PARTIAL (one of: 50-70% pass-rate, OR cohesion 3.5-4.0, OR one archetype-tag coverage gap):**
- gandalf authors follow-on disposition (same shape as R2 H1 disposition partial-pass)
- May commit a 6th regen season to fill coverage gap, or accept a sub-70% pass-rate as the achievable bar against disposition-3 calibration, or surface a deeper pipeline question (e.g., template-distribution-deferred surfaces as relevant)

**FAIL (any of: < 50% pass-rate, OR cohesion < 3.5, OR substrate-identity erosion):**
- gandalf authors disposition: revert to path (a) hand-redesign, OR pause for deeper R8 pipeline work (template-distribution repair surfaces as VS2b territory)
- Path-decision re-opens; not a sunk cost (R1 disposition-3 calibration + F1 geometry_type schema are still independently valuable)

### § 4.3 — Cross-reference with R1 + R2 + R8 dispositions

| Disposition | Disposition class | PASS criterion | Re-disposition trigger |
|---|---|---|---|
| R1 disposition-3 (§ 7.2) | category-of-completion (relaxed 70% → 4 sub-claims) | gate works + reachable + kit-broken surface + queue exists | sub-claim missing |
| R2 H1 disposition (§ 3.2) | instrument-limited PASS | re-test under explicit field gates | variance ≥ 0.10 under original threshold |
| R8 disposition (Sub-case 3) | commit-what's-proven; defer-what-isn't | `inverted` cohesion within 0.5 of baseline + substrate-identity invariant | inverted_no_naming cohesion drop > 0.5 → defer |
| **This F2 disposition** | **two-stage validation: first-batch gate + full catalogue R1 sprint** | first-batch PASS § 2.4 + full R1 70-85% under disposition-3 | first-batch FAIL → re-disposition; full FAIL → revert/extend |

---

## § 5 — Risk + watchpoints

### § 5.1 — Path (b) risks (and mitigations)

| Risk | Severity | Mitigation |
|---|---|---|
| R8 inverted at scale (51 classes vs 3-class A/B sample) surfaces emergent failure modes | 🟡 MEDIUM | **First-batch validation gate (§ 2.4)** catches this at 1-season regen before full investment. If first-batch fails, path-decision re-opens. |
| Archetype-tag coverage gaps in emergent catalogue (e.g., no hunter or no grappler emerges across 5 seasons) | 🟡 MEDIUM | gandalf review at first-batch + post-full-catalogue; surfaces "regenerate 1 more season for coverage" if needed |
| Convergence-failure rate per season higher than expected (R8 A/B had 5-9 of 10-11 classes converging) | 🟡 MEDIUM | Already factored into rocket sizing (5 seasons → ~50-55 classes after convergence failure attrition; matches target 51) |
| Naming fixedness at 51-class scale (R8 A/B had limited diversity at 10-class scale; 51 may amplify) | 🟡 MEDIUM | gandalf cohesion-judging protocol at full-catalogue review; sample 10-15 classes; if naming-vocabulary saturation pattern observed (e.g., 5+ "Saltfire ___" repetitions across seasons) authors follow-on disposition; rocket may need to vary seasonal vocabulary or salt naming inputs |
| Substrate-identity erosion at scale (R8 Test 4 was 3-season sample; 51-class scale may surface different invariance properties) | 🟢 LOW | gandalf samples 5-8 skills at full-catalogue review against pre-regen canonical-element references; substrate-identity at canonical-element level is byte-equal per Test 4 (architectural property, not sample-dependent) |
| Demo regen (L1) slips due to S1 regenerating to a new manifest | 🟢 LOW | Demo regen is *expected* to consume new manifest; L1 is downstream of S1 by design; no slip introduced |
| LLM cost overrun (multiple regen iterations if first-batch needs re-runs) | 🟢 LOW | Worst-case ~$30-40 LLM total; absorbable within project budget; rocket logs spend in CHANGELOG for transparency |

### § 5.2 — Path (a) hand-redesign risk for comparison (what we're NOT taking)

For the record: path (a) carries 4-6 weeks of rocket bandwidth as its primary risk; per-class judgment generalization is uncertain (a redesign rule that works for lightning_mage class_0016 may not generalize to all *_mage classes); and the underlying pathology (theme-driving-mechanic) remains in the generator going forward, so future regenerations would re-create the pathology unless R8-inversion is also adopted as the engine default. **Path (a) without also adopting R8-inversion is a band-aid; with R8-inversion adopted, path (a) is redundant work.** This is the deepest reason path (a) loses to path (b).

### § 5.3 — Watchpoints for `watchpoints-engine-rebuild-2026-05-19.md` (or new VS2a watchpoints file)

Knight-rider adds the following to the watchpoints file:

1. **First-batch regen archetype-coverage drift** — if first-batch produces all-mage or all-controller, surfaces follow-on disposition need
2. **Naming-vocabulary saturation at 5-season scale** — sample sentinel: if "Beacon ___" pattern repeats across ≥ 8 classes in different seasons, surface to gandalf
3. **R1 sprint pass-rate plateau** — if full-catalogue regen hits 60-70% pass-rate, do NOT auto-fire `vs2a/v0.7`; surface to gandalf for partial-pass disposition (per R2 H1 precedent)
4. **R8 disposition § 5a (template-distribution repair) re-opens** if `inverted` at 51-class scale surfaces template-fixedness pattern → may need to escalate template repair as VS2a-blocking instead of VS2b-deferred
5. **B6 main-work shape change** — S2 dispatch awaits regenerated-catalogue manifest; rocket pre-work must be parameterized to work against new manifest (status check at AGENT_STATE)

### § 5.4 — Cross-disposition watchpoint coordination

Knight-rider may surface (during VS2a coordination):
- **Decisions-log entry candidate** (jack-ryan authors): "F2 path-decision: full R8-inversion regeneration committed under disposition Path (b); shipped catalogue retired; new manifest under post-R8 default"
- **Discipline #18 candidate** (engineering-disciplines.md): "Generator-shape changes that affect catalogue identity require empirical small-batch validation gate before full regeneration" — if jack-ryan judges this as a generalizable principle from F2 + R8 sequence

---

## § 6 — Open question dispositions (from F2 dispatch)

Answering the open questions surfaced by knight-rider in the F2 dispatch:

### § 6.1 — Sprint v3 dependency?

**Sprint v3 is required upstream of the first-batch validation gate** (so that R1 sprint runs against the disposition-3 encounter calibration; otherwise the boss_kr ≥ 0.10 threshold is measured against an unreachable encounter and the gate-PASS criterion is uncalibrated). It is NOT required for *this decision*; F2 fires under sprint v2 evidence + R8 A/B empirics + design judgment. Knight-rider sequences: gamora R1 sprint v3 runs (disposition-3 implementation) → first-batch regen runs → first-batch R1 sprint runs against v3-calibrated encounter.

### § 6.2 — S1 dispatch amendment for regen LLM budget?

**Yes — S1 dispatch should include LLM regen budget rationale.** Estimate: ~$3.20 per season × 5-6 seasons = ~$16-19 total. Worst-case (first-batch FAIL + re-runs): ~$30-40. This is absorbable within project bounds; rocket logs the spend in CHANGELOG for transparency. Knight-rider files in CHANGELOG when S1 dispatches.

### § 6.3 — S2 dispatch shape change?

**Yes.** S2 (B6 main work) shifts to "authored against regenerated catalogue" — rocket pre-work must be parameterized to work against any catalogue shape (no hard class_id references); main work begins against the post-S1 catalogue. Schedule impact: ~1-2 weeks deferred from current expectations; offset by S1 completing faster than path (a) hand-redesign would have. Net VS2a wall time: similar to path (a) estimate or slightly faster.

### § 6.4 — Substrate-identity declaration amendment?

**No amendment in this commit.** R8 disposition § 3b already amended `substrate-identity-declarations-2026-05-17.md` with the surface-readability subsection. The 51-class scale finding would only require amendment if first-batch validation surfaces a substrate-mode-preservation regression below the 90% R8 benchmark — that's a discovery to be made at first-batch, not pre-judged here. **If full-catalogue review surfaces an invariance property worth recording, gandalf authors an amendment then.**

### § 6.5 — `inverted_no_naming` template-distribution opt-in dependency?

**No dependency.** Path (b) operates under `inverted` (per-entity LLM naming retained), the committed default. The template-distribution repair is deferred per R8 disposition § 5a and remains deferred under this decision. **F2 does NOT depend on the deferred path.** If at any point the template-distribution opt-in becomes operationally relevant (e.g., budget pressure makes per-entity LLM naming infeasible), that's a separate VS2b disposition; not a path (b) prerequisite.

---

## § 7 — Cross-references

### § 7.1 — Precedent dispositions (sequence-of-thought builds on)

- `canonical/story/r1-kit-redesign-queue-2026-05-19.md` § 5 (path alternatives surfaced; this disposition commits path (b))
- `reincarnated-engine/design/working-agreement/R1-blocker-3-disposition-2026-05-19.md` § 7.2 (category-of-completion PASS criterion precedent)
- `canonical/story/r8-disposition-2026-05-19.md` Sub-case 3 (committed `inverted` default; substrate-identity invariance proven; cohesion +0.20 above baseline proven)
- `canonical/story/r2-h1-disposition-2026-05-19.md` § 3.2 (instrument-limited PASS structural precedent; explicit re-test gate)
- `canonical/story/substrate-identity-declarations-2026-05-17.md` § 9.5 (R8 surface-readability amendment; pipeline-dependent preservation rates)
- `canonical/story/v1.0-engine-rebuild-complete-disposition-2026-05-19.md` § 5.1 (forward routing: engine-rebuild → VS2a)

### § 7.2 — Inputs synthesized

- R1 sprint v2 per-class evidence: `reincarnated-engine/output/R1-class-retune-2026-05-19/summary.md` (51/51 boss_kr=0.000 across shipped catalogue)
- R8 A/B 3-season output: `reincarnated-engine/output/R8-ab-run-2026-05-19/inverted/season_099002/` (Drowned Lighthouse, brine — 10 emergent classes, best boss_kr 0.22 at class_0007)
- R8 Test 4 substrate-identity finding: `reincarnated-engine/output/R8-test4-substrate-identity.md` (canonical-element invariance)
- R8 Test 1 cohesion finding: `reincarnated-engine/output/R8-test1-cohesion.md` (+0.20 cohesion above baseline for `inverted`)
- R8 Test 5 multi-shot stability: `reincarnated-engine/output/R8-test5-stability.md` (Jaccard 1.00 on inverted/season_099002)
- VS2a scope-of-work: `agentic_orchestration/hive-mind/scope-of-work-vs2a.md` § 1.2 (F2 framing) + § 2.2 (S1) + § 2.3 (S2)
- VS2a coordination matrix: `agentic_orchestration/hive-mind/coordination-matrix-vs2a.md` § 1 + § 2 DAG
- LLM call map (post-R8 amendment): `canonical/19-llm-call-map.md` (Phase A theme_coalescence + Phase B per-entity naming under `inverted`)
- Engineering disciplines: `reincarnated-engine/design/working-agreement/engineering-disciplines.md` #1 (math-before-code applies as design-before-build) + #12 (semantic-shift; the path-decision is a generator-shape semantic shift) + #17 (semantic-shifting)
- Hive-mind protocol: `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 (autonomous-operation) + § 4.3 (tag-firing) + § 4.9 (Matt-only-at-wind-down)

### § 7.3 — Forward routing (downstream of this disposition)

- S1 dispatch — knight-rider authors after F2 + F1 land; rocket executes (regen orchestration) + gandalf consults (first-batch review)
- S2 dispatch — knight-rider authors after S1 lands or in parallel under rocket pre-work parameterization; gamora main work executes against regenerated catalogue
- Decisions-log entry — jack-ryan authors at S1 close capturing F2 + S1 outcomes per R1 disposition-3 § 9.6 pattern
- R1 kit-redesign queue § 5 — amend with § 5.4 addendum (this commit; see § 8 below)
- VS2a coordination matrix § 2 DAG — update S1 + S2 sub-graph per § 3.2 (knight-rider authors as live document; this disposition surfaces the change but does not edit coordination matrix directly)

---

## § 8 — Reciprocal canonical-doc amendment (R1 kit-redesign queue § 5.4 addendum)

Per F2 dispatch acceptance criterion "R1 queue doc updated (if amendment chosen) + roadmap updated (if amendment chosen)": authored in same commit as this disposition.

Amendment to `canonical/story/r1-kit-redesign-queue-2026-05-19.md`: append § 5.4.

---

## § 9 — Provenance

Authored 2026-05-19 by gandalf under autonomous-operation L2-equivalent authority (Matt directive 2026-05-19; protocol § 4.0; F2 dispatch).

**Authority basis:** F2 dispatch text: "you decide; no Matt-wait." + protocol § 4.0 autonomous-operation: gandalf decides cross-cutting design / canonical / architectural decisions. F2 falls squarely here.

**Decision-only:** no production code touched; no schema change carried by this disposition (F1 carries the geometry_type schema; this disposition references it as prerequisite).

**Cross-seam contract:** S1 implementation dispatch (knight-rider authors after F2 + F1 land) carries the MIGRATION.md + manifest-continuity work per ADR-004 + Principle 6 round-trip smoke.

**Tag:** `vs2a/v0.5-kit-redesign-approach-decided` fires on the commit landing this disposition + R1 queue § 5.4 amendment. Knight-rider executes tag-firing per autonomous-operation protocol § 4.3.

---

*Filed 2026-05-19 by gandalf. The catalogue's pathology was a generator-shape problem; the generator was reshaped at R8; the catalogue regenerates under the new shape. Three seasons of empirical evidence already produced kits the shipped catalogue cannot match. The first-batch gate de-risks scale; the R1 sprint re-run carries the hypothesis-test promise to its catalogue-level conclusion. The old seasons sleep in git history; the new ones emerge from converged mechanic. Mithrandir signs.*
