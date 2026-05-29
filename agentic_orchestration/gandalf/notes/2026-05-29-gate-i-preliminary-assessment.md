# Recognition Record Gate (i) — PRELIMINARY Assessment

> **STATUS:** PRELIMINARY (preliminary verdict from A2-1 RE-FIRE attempt 2 fail-state cascade artifacts as of 2026-05-29) — Full gate (i) verdict awaits A2-1 RE-FIRE-2 PASS fresh artifacts at Step 6 of cascade-resumption-2 + jack-ryan Gate-2 design-quality audit. NOT a canonical promotion. NOT load-bearing for doc 38 / doc 52 / decisions-log. Feeds recognition record `canonical/story/2026-05-29-experiential-cascade-architecture-recognition.md` § 3 gate (i) disposition.

**Date:** 2026-05-29
**Author:** gandalf (story-and-design steward; recognition record owner; design-side critique-pair)
**Authority:** Matt 2026-05-29 in-session Concern #3 resolution authorization § 5 (gate (i) preliminary assessment authorization) + recognition record `canonical/story/2026-05-29-experiential-cascade-architecture-recognition.md` § 3 gate (i) framework + KR dispatch `2026-05-29-gandalf-cycle-14-a2-1-resumption-2-step-2-5-gate-i-preliminary-assessment.md` + R48.4 single-seam (gamora released post Step 1 audit; gandalf alone in slot 2.5)
**Mode:** Pattern A-deep design-side read of on-disk cascade artifacts; informational parallel-track NOT blocking cascade critical path

---

## 1. VERDICT

**Recognition record gate (i) preliminary verdict from A2-1 RE-FIRE attempt 2 fail-state cascade artifacts: PASS-preliminary (with one observability-gap WARN deferred to capture-and-watch).**

Cascade architecture's load-bearing LLM components (Wave A faction-label, Wave B per-kit identity, F-C inter-faction relationships) produced **coherent, substrate-grounded, AI-tell-clean outputs** in their FIRST production exercise ever under Path D flip. The Phase 7 0/18 verdict was mechanical-gate failure (Concern #3 bug), not cohesion-gate failure — LLM outputs were produced and are well-formed.

**One material observability gap surfaces:** per-kit cohesion_judge_confidence distribution is unobservable from this artifact-set — both because mechanical-gate short-circuited cohesion evaluation AND because `phase7_kit_verdict_log.kit_cohesion_score` was never populated (NULL for all 54 rows) AND because Wave B per-kit narratives are not persisted to `kit_archive.db` even when produced. This is a Disc #40 scaffold-flag finding (capture-and-watch per resolution plan § 3; **NOT escalation; NOT cascade halt**).

---

## 2. Scope

### 2.1 Artifact corpus assessed

A2-1 RE-FIRE attempt 2 fail-state cascade outputs at `agentic_orchestration/cycle-14-wave-5-season-001/`:

| Artifact | Size | Content assessed |
|---|---|---|
| `phase5_faction_clusters.json` | 5,741 B | Wave A LLM output — 3 ExportFactionCluster records with `faction_label_canonical` populated |
| `phase5_faction_relationships.json` | 4,658 B | F-C LLM output — 3 ExportFactionRelationship records (allied/mysterious/rival) |
| `kit_archive.db` | 118,784 B | 18 ACCEPTED kits + 54 phase7_kit_verdict_log rows + 12 phase7_cluster_aggregate_log rows |
| `phase7_season_summary.json` | 962 B | Phase 7 verdict log — 0/18 shipped_worthy (mechanical-gate fail; cohesion-gate not reached for any kit) |

All artifacts timestamped 2026-05-29 04:24 (consistent with A2-1 RE-FIRE attempt 2 fire window; engine HEAD `98e1825`).

### 2.2 Preliminary-vs-full distinction (Q6 vigilance, recognition record § 3 + dispatch § 0.4)

**PRELIMINARY** = informed by A2-1 RE-FIRE attempt 2 fail-state artifacts. Wave A + F-C fired AND produced outputs even though Phase 7 short-circuited at mechanical-gate.

**FULL** gate (i) verdict awaits:
- A2-1 RE-FIRE-2 PASS at Step 6 of cascade-resumption-2 (after Concern #3 P3c fix + star-lord cost-tracker wire-up)
- Fresh cascade artifacts with full pipeline through ≥12/18 Phase 7 emit
- jack-ryan Gate-2 design-quality audit per Disc #43

The preliminary verdict in § 1 does NOT canonical-write to recognition record. Recognition record § 3 gate (i) text remains unchanged. The preliminary feeds full-verdict consumption at A2-1 RE-FIRE-2 close.

### 2.3 Sample-size discipline (per recognition record § 2 preamble)

n = 3 LLM-derived faction labels + 3 F-C relationships + 18 kits with Wave B in-process (not persisted). This is a small-n assessment appropriate to qualitative + descriptive analysis. Do NOT over-fit conclusions to this sample. The verdict is BINARY at this stage ("do Wave A + Wave B + F-C produce coherent outputs at all?") — small-n is sufficient for the binary refutation question.

---

## 3. Wave A faction-naming coherence assessment

### 3.1 Per-label enumeration

| Cluster | Members | Modal BC | Element | `faction_label_canonical` | Coherence |
|---|---|---|---|---|---|
| 1 | 9 kits (light fighter, polearm soldier, dagger assassin, archer, standard wizard, channeling cleric, holy knight, storm caller, monk) | close + large-AOE | water 44% / earth 22% / wind 22% / fire 11% | **Tideworn Earthbreakers** | COHERENT |
| 2 | 1 kit (arcane familiar mage) | ranged + large-AOE | fire 100% | **Ember Siege Vanguard** | COHERENT (sample-size caveat — see § 3.3) |
| 3 | 3 kits (heavy barbarian, artillery mage, ritual mage) | ranged + chain | earth 33% / fire 33% / water 33% | **Chain-Drawn Wandering Casters** | COHERENT |

### 3.2 Substrate-grounding observations

**Cluster 1 — "Tideworn Earthbreakers":**
- "Tideworn" reads the water-modal element distribution (44% water primary)
- "Earthbreakers" reads the earth-secondary (22%) + close-press + large-AOE BC signature
- Identity narrative: *"a close-quarters warband shaped by water and soil, these fighters press into melee range and unleash broad, sweeping devastation across the ground they contest"* — directly reads the BC signature (close + large-AOE) AND element distribution (water + earth dominant) AND modal_tech_level (medieval)
- Thematic tags `["flood-terrain", "close-press", "wide-ruin"]` map cleanly to the cluster mechanical content
- **Substrate-grounded: YES.** The label is decodable from substrate evidence by an attentive reader.

**Cluster 2 — "Ember Siege Vanguard":**
- "Ember" reads fire 100% element distribution
- "Siege" reads the ranged + large-AOE BC signature (wide-area conflagration)
- "Vanguard" reads — *less directly substrate-grounded*; "Vanguard" is a culturally-coded militant-leadership term but the cluster has 1 member (arcane familiar mage). The single-member cluster strains the "vanguard" framing because there is no actual vanguard cohort being led
- Identity narrative: *"a medieval ranged combat lineage defined by wide-arc fire deployment, these fighters specialize in large-area conflagration rather than precision strikes"* — accurate to BC + element; the "lineage" framing is appropriately humble given modal_cultural_lineage="unknown"
- Thematic tags `["fire", "ranged-AOE", "medieval-siege"]` map cleanly
- **Substrate-grounded: MOSTLY YES.** Minor pattern observation in § 3.3 about single-member-cluster naming.

**Cluster 3 — "Chain-Drawn Wandering Casters":**
- "Chain-Drawn" reads the `damage_geometry: chain` BC signature directly
- "Wandering" reads the rootless / no-cultural-lineage substrate (modal_cultural_lineage="unknown")
- "Casters" reads the 2-of-3 mage members (artillery mage + ritual mage; heavy barbarian is the odd member of this cluster)
- Identity narrative: *"a loosely bound cluster of ranged combatants whose techniques thread across earth, fire, and water without cultural allegiance, linked only by the chained geometry of their strikes... their commonality is method, not origin"* — substrate-honest about the cluster's heterogeneity AND its lack of cultural anchoring
- Thematic tags `["chain-strike", "elemental-balance", "rootless"]` are unusually honest — "rootless" explicitly names the modal_cultural_lineage="unknown" condition
- **Substrate-grounded: YES, with explicit honesty about substrate gaps.** The label embraces the substrate vote even when that vote is "unknown."

### 3.3 Pattern observations

**Pattern P-W-A-1 (positive) — labels are substrate-readable.** All three labels can be reverse-engineered from modal element + BC signature + tech level + lineage WITHOUT prior cultural canon. This is the signature of substrate-led emergence the recognition record predicts.

**Pattern P-W-A-2 (positive) — labels avoid AI-tell phrases.** Zero hits on the AI-tell phrase list (`"order of"`, `"house of"`, `"the brotherhood"`, `"ancient power"`, etc. per `phase5_orchestrator.py:133-145`). All three labels are NEW compounds, not template-leakage.

**Pattern P-W-A-3 (positive) — diversity-clean.** `cosine_similarity_max` ≤ 0.39 for all three clusters; `diversity_flag = false`; no regeneration fired. The three labels are semantically distinct from each other.

**Pattern P-W-A-4 (positive) — substrate-honest about gaps.** Cluster 3's `["rootless"]` tag and "without cultural allegiance" narrative; Cluster 2's "untraced" framing in narrative — the LLM is NOT confabulating cultural lineage when modal_cultural_lineage="unknown". This is the load-bearing behavior the substrate-led discipline (Discipline #41) demands. **Strong empirical signal that the Wave A prompt + substrate vocabulary inputs are working as designed.**

**Pattern P-W-A-5 (caveat) — single-member-cluster strain.** Cluster 2 is a 1-kit cluster receiving a "Vanguard" identity that grammatically implies cohort scale. This is a small surface-level dissonance, not a failure. It will recur whenever PM-1 produces singleton clusters. **Possible recognition record § 3 gate (i) framework refinement candidate** — see § 7 below.

**Pattern P-W-A-6 (caveat) — modal lineage uniformly "unknown" across all 3 clusters.** Every cluster has `modal_cultural_lineage="unknown"`, `modal_tone="unknown"`. This is a *substrate condition*, not a Wave A defect — the upstream Phase 3 PM-1 evidence is sparse on cultural-lineage attribution for this kit-set. Wave A handles this honestly (per P-W-A-4), but the assessment cannot evaluate "does Wave A produce coherent labels when modal_cultural_lineage is RICH?" because the substrate didn't surface rich lineage signal in this run. **Full gate (i) verdict at A2-1 RE-FIRE-2 should ideally test with kit-set that produces ≥1 cluster with known modal_cultural_lineage** — capture for full-verdict resolution.

### 3.4 Wave A coherence verdict

**Wave A faction-naming: COHERENT.** All three labels substrate-grounded, AI-tell-clean, diversity-clean, and substrate-honest about gaps. Strong preliminary signal that recognition record cascade chain Step E (faction naming) operates at acceptable quality in production. Caveats P-W-A-5 (singleton-cluster naming) and P-W-A-6 (sparse-lineage substrate condition) noted for full-verdict consumption.

---

## 4. Wave B per-kit identity coherence assessment

### 4.1 Empirical finding — Wave B narratives NOT persisted to on-disk artifacts

**The Wave B per-kit identity LLM output is NOT extractable from this artifact-set.**

Schema inspection of `kit_archive.db`:
- `kit_archive` table has `notes TEXT` column — **EMPTY (NULL or '') for all 18 kits**
- `phase7_kit_verdict_log` has `kit_cohesion_score REAL` — **EMPTY (NULL) for all 54 rows**
- No other schema location for Wave B per-kit narratives

Rocket's own completion record at A2-1 RE-FIRE attempt 2 § 4 corroborates:
> "Wave B: FIRED (faction_visibility=visible causes should_fire_wave_a=True which enables Wave B; per-kit identity narratives produced — **not extractable from Phase 5 JSON because per-kit records not surfaced in faction_clusters.json output; full Wave B telemetry captured in-process**)."

**Wave B output is in-process-only at present.** This is an empirical fact about the persistence-layer architecture, independent of Concern #3 mechanical-gate short-circuit.

### 4.2 Per-kit coherence verdict

**Per-kit Wave B coherence: UNOBSERVABLE from this artifact-set.** Cannot assess per-kit identity coherence (kit names + flavor + identity alignment with mechanical content) because the persistence layer does not capture Wave B output.

### 4.3 Pattern observations

**Pattern P-W-B-1 (observability gap; Disc #40 scaffold-flag candidate) — Wave B persistence-layer gap.** Wave B is the load-bearing per-kit identity LLM in the cascade architecture (recognition record § 1.1 Step C), but its output is in-memory-only. For:
- gate (i) full validation at A2-1 RE-FIRE-2 close
- jack-ryan Gate-2 design-quality audit per Disc #43
- A/B comparison protocol at Wave 5 close (per `canonical/story/ab-comparison-protocol-cycle-14-close-2026-05-27.md`)
- recognition record gate (v) doc 52 promotion (any future)

— Wave B persistence to on-disk artifacts is structurally necessary. Current state means no downstream gate can empirically assess Wave B output quality.

**Pattern P-W-B-2 (composition with Disc #40) — third scaffold-flag pattern data point this cascade.** Per Concern #3 authorization § 2.3, two scaffold artifacts already surfaced this cascade: (a) `FACTION_VISIBILITY=invisible`-default + hardcoded assert (resolved Step 2); (b) `tracker=None` in Phase 5 LLM path (queued for resolution). This Wave B persistence gap is the third pattern data point. **NOT a cascade-halt finding; capture for Matt re-engage cumulative Disc #40 discussion** (per resolution plan § 4 pattern).

**Pattern P-W-B-3 (indirect signal — narrative quality of F-C tension narratives suggests Wave B prompt is sound).** While Wave B per-kit output is unobservable, the F-C output IS observable (3 tension narratives). The F-C narratives demonstrate the Phase 5 LLM is operating with substrate-fidelity (see § 5 below). This is INDIRECT evidence the Phase 5 LLM stack — which Wave B shares prompt/model/AI-tell-grep with — is producing coherent output. **NOT a substitute for direct Wave B observability**; just a weak positive signal.

### 4.4 Wave B coherence verdict

**Wave B: UNOBSERVABLE-in-this-artifact-set; persistence gap surfaces as Disc #40 capture-and-watch.** Cannot PASS or FAIL the per-kit coherence assessment from this data. Recommend: full gate (i) at A2-1 RE-FIRE-2 close requires Wave B persistence to on-disk artifacts (either to `kit_archive.notes`, a new `wave_b_kit_identity` column, or a separate JSON sidecar like `phase5_wave_b_kit_identities.json`). **SURFACE TO KR** for inclusion in star-lord cost-tracker dispatch (§ 8 below) or as separate observability follow-up.

---

## 5. F-C inter-faction relationship coherence assessment

### 5.1 Per-relationship enumeration

| Pair | Faction A | Faction B | `relationship_type` | Substrate vote | Coherence |
|---|---|---|---|---|---|
| 1↔2 | Tideworn Earthbreakers | Ember Siege Vanguard | **allied** | lineage_similarity=same, element_relationship=complementary, marginal_lineage_flag=True | COHERENT |
| 1↔3 | Tideworn Earthbreakers | Chain-Drawn Wandering Casters | **mysterious** | lineage_similarity=same, element_relationship=divergent, marginal_lineage_flag=True | COHERENT |
| 2↔3 | Ember Siege Vanguard | Chain-Drawn Wandering Casters | **rival** (primary_pair) | lineage_similarity=same, element_relationship=divergent, primary_pair_flag=True | COHERENT |

### 5.2 Substrate-grounding observations

**Relationship 1↔2 (allied):** Substrate vote = lineage_similarity=same + element_relationship=complementary → "allied" is the appropriate substrate-emergent type. LLM narrative reads it cleanly:
> *"...complementary roles on contested ground — one churning the soil and driving formations inward, the other scorching the corralled space with wide-arc conflagration. Their shared medieval-siege sensibility and mutual orientation toward wide-ruin over precision creates functional alignment, though the marginal lineage signal means the terms of that alignment remain unstable."*

The "though the marginal lineage signal means the terms of that alignment remain unstable" clause is *load-bearing substrate honesty* — the LLM is honoring `marginal_lineage_flag=True` as warranted hedge, not papering over substrate weakness. This is the behavior the cross-cultural neutrality binding (recognition record § 1.1 + Discipline #45 LOAD-BEARING) demands.

**Relationship 1↔3 (mysterious):** Substrate vote = element_relationship=divergent + marginal_lineage_flag=True + lineage_similarity=same → "mysterious" is the appropriate substrate-emergent type when substrate is thin and contact-history is unestablished. LLM narrative:
> *"...orbit the same elemental space from a rootless, chained-strike distance — yet the substrate does not clarify whether these two factions have ever truly registered each other's presence. Their shared lineage marker is flagged as marginal, leaving the nature of any contact unresolved."*

The narrative explicitly NAMES the substrate-thin condition ("the substrate does not clarify"). This is substrate-honesty at the meta-narrative layer — extraordinarily good behavior for an LLM-generated relationship narrative; this is the signature of a prompt that successfully constrains the model from confabulating.

**Relationship 2↔3 (rival; primary_pair):** Substrate vote = highest pairwise Mahalanobis distance (125.6; pairwise_distance_percentile=1.0) + element_relationship=divergent → "rival" is the appropriate substrate-emergent type for the season's central tension. LLM narrative reads BC + element divergence as the core conflict:
> *"...one faction's success in the field is a direct argument against the other's methodology, making every engagement a test of doctrine as much as strength."*

The primary_pair_intensifier successfully fires (per F-C spec) and adds meaningful weight to the central pairing without overclaiming backstory.

### 5.3 Pattern observations

**Pattern P-F-C-1 (positive) — relationship types are substrate-vote-emergent.** All three relationship types (allied, mysterious, rival) match the substrate vote rule per the F-C spec (per `phase5_orchestrator.py:162-164` enum + recognition record § 1.1 Step F). No relationship type is a "default" or "safe choice" — each is decoded from substrate evidence.

**Pattern P-F-C-2 (positive) — narrative substrate-honesty.** All three narratives explicitly name substrate conditions (marginal lineage, untraced lineage, divergent elemental commitment). This is the signature behavior recognition record § 1.1 Step F predicted ("read-and-judge layer over emergent factions"). **Strong empirical signal that F-C prompt + SUBSTRATE_VOTE encoding work as designed.**

**Pattern P-F-C-3 (positive) — AI-tell clean.** All three relationships: `ai_tell_compliance_score ≥ 0.85`, `final_compliance_status=ACCEPT`, `grep_compliance_pass=True`, `ai_tell_phrase_hits=None`. Zero hits on F-C AI-tell phrase list (`"bound by ancient grudge"`, `"destined to clash"`, `"their fates intertwined"`, etc. per `phase5_orchestrator.py:147-157`).

**Pattern P-F-C-4 (positive) — diversity-clean.** `diversity_check_max_similarity` ≤ 0.46 across all three pairs; no regeneration fired. The three tension narratives are semantically distinct from each other.

**Pattern P-F-C-5 (positive) — primary_pair_intensifier conditional fired correctly.** Only the 2↔3 pair (primary_pair_flag=True) carries a primary_pair_intensifier; the other two pairs have `primary_pair_intensifier=None`. The G-B primary-pair selection (gb_selection_rationale="highest_substrate_distance"; pairwise_distance=125.6) routed cleanly through to F-C output.

**Pattern P-F-C-6 (caveat) — relationship-type distribution narrow.** 3 relationships → {allied, mysterious, rival}. The 6-enum vocabulary (`antagonist`/`rival`/`allied`/`neutral`/`mysterious`/`parallel`) is not exercised at scale here. With n=3 we cannot assess whether F-C produces a balanced distribution across the enum OR systematically skews toward certain types. **Capture for full-verdict consumption at A2-1 RE-FIRE-2** — A2-1 RE-FIRE-2 + season_002 + season_003 will produce ~3-6 relationships per season × 3 seasons = ~9-18 relationships, enough to weak-signal a distribution.

### 5.4 F-C coherence verdict

**F-C inter-faction relationships: COHERENT.** All three relationship types substrate-vote-emergent; all three narratives substrate-honest and AI-tell-clean; primary_pair_intensifier conditional fires correctly. **Strong preliminary signal that recognition record cascade chain Step F (inter-faction relationships) operates at acceptable quality in production.** Caveat P-F-C-6 (relationship-type distribution n=3) noted for full-verdict consumption at A2-1 RE-FIRE-2 + 3-season cascade.

---

## 6. Cohesion_judge_confidence distribution capture

### 6.1 Empirical finding — distribution UNOBSERVABLE from this artifact-set

Per-kit `cohesion_judge_confidence` distribution cannot be captured from A2-1 RE-FIRE attempt 2 fail-state artifacts. Three composing reasons:

1. **Mechanical-gate short-circuit (Concern #3 effect):** Phase 7 mechanical-gate failed at `gauntlet_pass_rate ≈ 0` for all 18 kits before cohesion-gate evaluation. Per `phase7_season_summary.json`: `kits_held_cohesion=0` (no kits processed through cohesion gate); `kits_held_both=13` (13 kits failed both gates); `kits_held_mechanical=5` (5 kits failed mechanical only). The cohesion-gate evaluation pathway did not execute for any kit.

2. **Persistence-layer gap on per-kit cohesion score:** Even where `phase7_kit_verdict_log.phase7_gate_status="canonical"` (18 rows in the latest evaluation attempt — confirming Wave A fired and cluster-level cohesion was conceptually available), the per-row `kit_cohesion_score` column is **NULL for all 54 rows**. The data structure exists to record per-kit cohesion confidence, but it was not populated in this cascade.

3. **F-C cohesion_judge_confidence captured at relationship-level, not kit-level:** `ExportFactionRelationship.cohesion_judge_confidence` is populated at the 3 relationship records (per F-C output) but these are relationship-level not kit-level scores; the schema docstring at `schemas.py:766-768` confirms this field "currently aliases to ai_tell_compliance_score" — values are 0.85 / 0.91 / 0.92. Useful informational signal at F-C layer, NOT the per-kit distribution gate (i) seeks.

### 6.2 What CAN be captured at cluster-level

| Cluster | Members | cluster_compactness (PM-1 silhouette) | diversity_flag | phase7_gate_status (latest attempt) |
|---|---|---|---|---|
| 1 | 9 | 0.187 | False | canonical |
| 2 | 1 | 0.187 | False | canonical |
| 3 | 3 | 0.187 | False | canonical |
| (cluster_id=-1 catch-all) | 5 | (no compactness; below PM-1 threshold) | False | placeholder |

`cluster_compactness` is uniform across the 3 named clusters (0.187) because PM-1 fired `kmeans_k3_fallback` (single algorithm run; not per-cluster compactness). This is cluster-level info, NOT the per-kit cohesion confidence the recognition record gate (i) predicts.

### 6.3 Distribution shape verdict

**Cohesion_judge_confidence distribution: UNOBSERVABLE-in-this-artifact-set.** Cannot determine systematic-under-0.75 vs scattered-under-0.75 vs all-above-0.75 from this data.

Per dispatch § 1.2 + resolution plan § 3 surface protocol:
- **NOT systematic under-0.75** (cannot observe; no data) — do NOT SURFACE TO KR for Pattern B design call
- **NOT scattered under-0.75** (cannot observe; no data) — capture-and-watch as observability gap

**Recommendation:** A2-1 RE-FIRE-2 (Step 6 of cascade-resumption-2) MUST populate per-kit `kit_cohesion_score` in `phase7_kit_verdict_log` for the cohesion-gate path. This is wiring-level work in the gamora seam (likely in `phase7_bridge.py` or `gauntlet_sim.py` Phase 7 evaluation pathway). Compose with star-lord cost-tracker dispatch (Step 4 of cascade-resumption-2) OR raise as separate observability dispatch. **SURFACE TO KR** (§ 8 below).

### 6.4 Disc #40 capture-and-watch composition

Per resolution plan § 3 surface protocol: this finding is captured-and-watched, NOT escalated. The empirical data needed to validate gate (i) prediction P2 ("Phase 7 cohesion_judge_confidence distributes around 0.70-0.85 range; scattered under-0.75 acceptable; systematic under-0.75 surfaces scaffold-threshold finding" per recognition record § 4) is not present in this artifact-set. P2 remains untested.

---

## 7. Recognition record gate (i) preliminary disposition recommendation

### 7.1 Preliminary disposition

**Recommend gate (i) PRELIMINARY verdict: PASS-preliminary (with observability-gap WARN deferred to capture-and-watch).**

Rationale:
- Wave A produces coherent + substrate-grounded + AI-tell-clean faction labels (§ 3) → recognition record cascade chain Step E **validated at small-n**
- F-C produces coherent + substrate-vote-emergent + AI-tell-clean relationships (§ 5) → recognition record cascade chain Step F **validated at small-n**
- Wave B per-kit identity is UNOBSERVABLE in this artifact-set → recognition record cascade chain Step C **not validated, not refuted, persistence-gap surfaces**
- Cohesion_judge_confidence distribution is UNOBSERVABLE in this artifact-set → recognition record prediction P2 **not validated, not refuted, persistence-gap surfaces**

The preliminary verdict is PASS-preliminary because:
1. Where outputs ARE observable (Wave A, F-C), they exhibit the substrate-led behavior the cascade architecture predicts
2. Where outputs are unobservable, it's due to persistence/short-circuit conditions external to the LLM cascade itself
3. No empirical evidence refutes the cascade architecture's quality at the LLM layer
4. The observability gaps are addressable engineering work, NOT design refutation

### 7.2 What would change verdict at A2-1 RE-FIRE-2 fresh artifacts

Full gate (i) verdict at A2-1 RE-FIRE-2 close (Step 6) would PROMOTE to PASS (full) IF:
- Wave A faction-naming coherence holds at fresh artifacts (replication of § 3 verdict)
- F-C inter-faction relationship coherence holds at fresh artifacts (replication of § 5 verdict)
- Wave B per-kit identity coherence becomes OBSERVABLE (persistence-gap closed) AND per-kit identities align with mechanical content
- Per-kit `cohesion_judge_confidence` distribution becomes OBSERVABLE AND distributes around 0.70-0.85 (P2 prediction validated) — scattered under-0.75 acceptable
- A2-1 RE-FIRE-2 Phase 7 emit ≥ 12/18 (mechanical-gate clears; cohesion-gate evaluated for all kits)

Full gate (i) verdict at A2-1 RE-FIRE-2 close would DEMOTE to WARN-with-pattern OR FAIL-with-pattern IF:
- Wave A or F-C output coherence DEGRADES at fresh artifacts (rare — small-n preliminary signal is strong)
- Per-kit `cohesion_judge_confidence` shows SYSTEMATIC under-0.75 across most kits (P2 refutation; SURFACE for Pattern B design call per resolution plan § 3)
- Wave B per-kit identity shows incoherence OR generic / non-substrate-grounded patterns at fresh artifacts

### 7.3 Cascade action recommendation

**Cascade proceeds to Step 3 (gamora P3c fix) per Concern #3 authorization.** This preliminary assessment does NOT block cascade critical path. The PASS-preliminary verdict is informational for recognition record gate (i) framework; the full gate (i) verdict awaits A2-1 RE-FIRE-2 fresh artifacts.

---

## 8. Recognition record framework refinement notes (do NOT canonical-write)

The following are captured for Matt re-engage consideration. Do NOT canonical-write to recognition record § 3 in this dispatch.

### 8.1 Candidate framework refinement R1 — Wave B observability prerequisite

Recognition record § 3 gate (i) "empirical instruments" lists three:
- ExportFactionCluster.faction_label_canonical (Wave A) — observable
- ExportFactionRelationship (F-C) — observable
- Phase 7 cohesion_judge_confidence (Wave B / cohesion-gate) — UNOBSERVABLE in current pipeline

**Recommendation for Matt re-engage:** add explicit prerequisite to gate (i) — "Wave B per-kit identity output must be persisted to on-disk artifacts (e.g., `kit_archive.notes` column populated, OR new `wave_b_kit_identity` column, OR sidecar `phase5_wave_b_kit_identities.json`) such that downstream gates and audits can empirically read Wave B coherence."

This is NOT a recognition record canonical write; it's framework-refinement candidate for inclusion at A2-1 RE-FIRE-2 close OR Cycle 14 close.

### 8.2 Candidate framework refinement R2 — single-member-cluster naming convention

Pattern P-W-A-5 surfaced single-member-cluster ("Ember Siege Vanguard" for 1 kit) creates grammatical strain ("Vanguard" implies cohort scale; 1 kit does not).

**Recommendation for Matt re-engage:** consider whether the Wave A prompt should produce DIFFERENT naming conventions for singleton clusters (e.g., personage-style "The Ember Siege Caster" rather than cohort-style "Ember Siege Vanguard"). This is a Phase 5 Wave A prompt refinement candidate, NOT a cascade halt. Recognition record § 3 gate (i) framework could note "singleton-cluster naming convention may benefit from prompt refinement after empirical pattern observation across multiple seasons."

This is NOT a recognition record canonical write; it's prompt-refinement candidate for Cycle 14 close OR Cycle 15+ design call.

### 8.3 Candidate framework refinement R3 — rich-lineage substrate condition test gap

Pattern P-W-A-6 surfaced that all 3 clusters in this run have `modal_cultural_lineage="unknown"`. Full gate (i) validation needs at least one cluster with `modal_cultural_lineage` populated to test "does Wave A produce coherent labels when substrate IS rich on lineage?"

**Recommendation for Matt re-engage:** A2-1 RE-FIRE-2 + season_002 + season_003 may organically surface kits with richer lineage signal. Recognition record § 3 gate (i) framework could add full-verdict criterion: "≥1 cluster with non-unknown modal_cultural_lineage in the gate (i) artifact corpus" — to test that Wave A handles BOTH sparse-substrate (this run) AND rich-substrate conditions.

This is NOT a recognition record canonical write; it's full-verdict criterion candidate for A2-1 RE-FIRE-2 + 3-season cascade close.

### 8.4 Composition with existing Disc #40 capture queue

This preliminary assessment adds **two empirical data points** to the Disc #40 scaffold-flag pattern queue (per Concern #3 authorization § 2.3 pattern data point list):
- (c) Wave B persistence-layer gap (per § 4.3 Pattern P-W-B-1)
- (d) `phase7_kit_verdict_log.kit_cohesion_score` not-populated even when Wave A fires (per § 6.1)

These compose with existing data points (a) FACTION_VISIBILITY=invisible default + assert (resolved); (b) `tracker=None` in Phase 5 (queued for Step 4 cost-tracker dispatch). **Capture for Matt re-engage cumulative Disc #40 discussion**; do NOT canonical-write in this dispatch.

---

## 9. Disc #42a Q1-Q6 self-audit

| Q | Question | Verdict | Notes |
|---|---|---|---|
| Q1 | Load-bearing framing assumption: "Wave A + Wave B + F-C LLM outputs from A2-1 RE-FIRE attempt 2 fail-state are coherent enough to inform preliminary gate (i) disposition; Phase 7 mechanical-gate rejection (Concern #3) does NOT invalidate the LLM outputs themselves" | HOLDS — but partially refines | Wave A + F-C ARE observable and coherent. Wave B is NOT observable (persistence gap). Concern #3 mechanical-rejection did short-circuit cohesion-gate evaluation BUT additionally the persistence layer wouldn't have captured per-kit cohesion even if cohesion-gate fired. Refines assumption: Phase 7 mechanical-gate rejection AND persistence-layer gap together produce two cohesion-observability blockers. |
| Q2 | Refutation evidence in scope: the cascade artifacts ARE the refutation evidence; if Wave A produces garbage faction labels, the framing assumption refutes | HOLDS | Wave A + F-C labels and relationships are NOT garbage; they're substrate-grounded. Wave B is not refuted because not observable. Q1 assumption refines, not refutes. |
| Q3 | Refutation surface-able cheaply: read JSON files + db query at gandalf's seam-internal cost | HOLDS | ~30 min wall-clock; reads completed |
| Q4 | Measurement context match: A2-1 RE-FIRE attempt 2 fired Wave A + F-C + Wave B under FACTION_VISIBILITY=visible | HOLDS | Confirmed at `phase5_faction_clusters.json` metadata: `faction_visibility=visible`, `wave_a_fired=true`. Step 2 architecture confirmed active. |
| Q5 | Calibration scope match: Wave A + Wave B + F-C are the cascade architecture's load-bearing LLM components per recognition record § 1.1 chain steps C-F | HOLDS | All four cascade chain steps assessed (or attempted to assess) per scope items 1-4 |
| Q6 | Semantic stability of "preliminary": "preliminary verdict" = informed by A2-1 RE-FIRE attempt 2 fail-state cascade outputs; full verdict awaits A2-1 RE-FIRE-2 PASS fresh artifacts. Keep distinct — do NOT promote preliminary to canonical-load-bearing gate (i) verdict in this dispatch | HONORED | § 1 verdict explicitly tagged "PASS-preliminary"; § 2.2 preserves preliminary-vs-full distinction; § 7.2 enumerates what changes verdict at A2-1 RE-FIRE-2 fresh artifacts; § 8 framework refinements explicitly tagged "do NOT canonical-write"; recognition record § 3 gate (i) text remains unchanged. |

**Self-audit overall verdict:** assessment captures what dispatch asked. Q1 refined (not refuted) — the Wave B-observability blocker is a SECOND condition beyond Concern #3 short-circuit that the original framing did not enumerate. This refinement is captured in § 4 + § 6 + § 8.1; the preliminary verdict in § 1 accommodates the refinement (PASS-preliminary covers Wave A + F-C; the Wave B observability gap is captured as a separate WARN-with-deferred-action, not a verdict-collapsing failure).

---

## 10. Cross-references

- `canonical/story/2026-05-29-experiential-cascade-architecture-recognition.md` — the recognition record this assessment feeds (gate (i) preliminary disposition; § 3 gate (i) framework; § 4 predictions P1-P3)
- `agentic_orchestration/dispatches/2026-05-29-gandalf-cycle-14-a2-1-resumption-2-step-2-5-gate-i-preliminary-assessment.md` — this dispatch (full scope at § 0-§ 8)
- `agentic_orchestration/gandalf/notes/2026-05-29-concern-3-resolution-authorization-and-pre-ratification.md` § 5 — gate (i) preliminary assessment authorization (Matt 2026-05-29)
- `agentic_orchestration/gandalf/notes/2026-05-29-concern-1-and-2-resolution-plan.md` § 3 — surface conditions (Disc #40 capture-and-watch pattern)
- `agentic_orchestration/dispatches/2026-05-29-rocket-cycle-14-a2-1-step-4-refire-post-step1-step2.md` — A2-1 RE-FIRE attempt 2 dispatch + completion record (cascade artifact provenance + Concern #3 surface)
- `~/Games/reincarnated-engine/src/reincarnated/export/schemas.py` lines 563-832 — ExportFactionCluster + ExportFactionRelationship + RELATIONSHIP_TYPE_ENUM schemas
- `~/Games/reincarnated-engine/src/reincarnated/llm/phase5_orchestrator.py` lines 80-235 — Wave A + Wave B + F-C invocation logic + AI-tell phrase lists + diversity-check + cost-anomaly thresholds
- Cascade artifacts assessed:
  - `agentic_orchestration/cycle-14-wave-5-season-001/phase5_faction_clusters.json` (5,741 B; 3 ExportFactionCluster records)
  - `agentic_orchestration/cycle-14-wave-5-season-001/phase5_faction_relationships.json` (4,658 B; 3 ExportFactionRelationship records)
  - `agentic_orchestration/cycle-14-wave-5-season-001/kit_archive.db` (118,784 B; 18 kit_archive rows + 54 phase7_kit_verdict_log rows + 12 phase7_cluster_aggregate_log rows)
  - `agentic_orchestration/cycle-14-wave-5-season-001/phase7_season_summary.json` (962 B; 0/18 shipped_worthy; mechanical-gate fail; cohesion-gate not reached)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Disc #11 empirical-inspection (read on-disk artifacts; no inference beyond data) + Disc #40 scaffold-flagging (Wave B persistence gap + per-kit cohesion-score persistence gap as data points) + Disc #41 substrate-led discipline (Wave A faction labels emerged from PM-1; not imposed canon taxonomy) + Disc #42a Q1-Q6 framing-audit (§ 9) + Disc #43 design-quality wave-close audit perspective + Disc #48 R48.4 R48.5

---

## 11. Sign-off

**Authored:** gandalf (story-and-design steward; recognition record owner) per Matt 2026-05-29 in-session Concern #3 resolution authorization § 5 (gate (i) preliminary assessment authorization) + KR dispatch `2026-05-29-gandalf-cycle-14-a2-1-resumption-2-step-2-5-gate-i-preliminary-assessment.md`

**For:** the preliminary gate (i) verdict from A2-1 RE-FIRE attempt 2 fail-state cascade artifacts; PASS-preliminary (with Wave B persistence-gap WARN deferred to capture-and-watch); cascade architecture's load-bearing LLM components (Wave A + F-C) produce coherent, substrate-grounded, AI-tell-clean outputs in production for the first time ever under Path D flip; Wave B coherence + per-kit cohesion_judge_confidence distribution UNOBSERVABLE in this artifact-set due to persistence-layer + mechanical-gate-short-circuit composing conditions; full gate (i) verdict awaits A2-1 RE-FIRE-2 PASS fresh artifacts (Step 6 of cascade-resumption-2) + jack-ryan Gate-2 design-quality audit per Disc #43.

**Next-empirical-evidence-checkpoints:**
- A2-1 RE-FIRE-2 PASS at Step 6 of cascade-resumption-2 (Wave A + F-C coherence replication test + Wave B persistence test + per-kit cohesion_judge_confidence distribution test)
- jack-ryan Gate-2 Pattern E review at Step 5 of cascade-resumption-2 (design-quality audit per Disc #43)
- A/B comparison protocol at Wave 5 close (cascade-architecture validation against doc 48 baseline)
- Matt re-engage for Disc #40 cumulative pattern discussion (4 data points: (a) FACTION_VISIBILITY default + assert; (b) tracker=None; (c) Wave B persistence gap; (d) per-kit cohesion-score persistence gap) + recognition record § 3 framework refinement candidates R1/R2/R3 at § 8

**Completion timestamp:** 2026-05-29 (assessment complete; brief authored; ready for KR completion-record append + auto-commit per CLAUDE.md addendum 2026-05-25)
