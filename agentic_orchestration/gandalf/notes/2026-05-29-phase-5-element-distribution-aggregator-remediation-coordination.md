# Phase 5 element_distribution Aggregator Remediation Coordination

> **STATUS:** CURRENT (load-bearing as of 2026-05-29) — Cascade-r4 follow-on coordination per Matt 2026-05-29 verbatim (two-message composition: lightning-themed-faction retroactive fix + season-name retroactive refresh). Resolves Q1-Q6 design questions surfaced by rocket forensics (commit `57cbdc5`) + jack-ryan framing-audit (commit `baf6c46`) under hive-mind decision-routing.

**Date:** 2026-05-29
**Author:** gandalf (story-and-design steward)
**Authority:**
- Matt 2026-05-29 message 1 verbatim: *"please investigate the root cause of all factions receiving lightning-related names when the actual elemental make-up of the faction clusters is not lightning-dominant or modal. Let's fix this retroactively."*
- Matt 2026-05-29 message 2 verbatim: *"once the lightning-themed faction issue has been resolved, please retroactively refresh the season names as well."*
- Hive-mind decision-routing (Matt 2026-05-23): seam-owner decides in-scope; gandalf coordinates design questions; auto-commit per CLAUDE.md addendum 2026-05-25
- Companion: Matt 2026-05-29 hive-mind-state line 5408 "NOT v1 blocking"

**Companion docs:**
- `agentic_orchestration/rocket/notes/2026-05-29-phase-5-element-distribution-aggregator-forensics.md` — root cause confirmed; 1-line fix scoped
- `agentic_orchestration/qa/pending/2026-05-29-jack-ryan-phase-5-element-distribution-aggregator-framing-audit.md` — Instance 6 #8; vocabulary-staleness-vs-substrate-expansion sub-case named; Disc #42a Q7 candidate
- `canonical/story/2026-05-29-designer-writes-substrate-player-names-experience-principle.md` — § 4.1 extension target (aggregator-layer drift)
- `agentic_orchestration/gandalf/notes/2026-05-29-wave-s-season-naming-design-spec.md` — Wave-S spec § 6 sequencing + § 8 retroactive backfill plan
- `canonical/47-damage-scaling-architecture-2026-05-27.md` § 4.6.5 ELEMENT_CONVERSION Layer 2 — STR→physical canonical commitment
- (Amendment 7 substrate spec) — STAT_ELEMENT_POOLS STR→{physical}

---

## § 0 TL;DR

**Recommended option: B (existing clusters + all-LLM-waves refresh).**

Three-season aggregate cost: **~$1.45** (Wave A 3 × $0.02 + Wave-S 3 × $0.015 + Wave B 100 × $0.01 = $1.05; F-C re-fire 3 × $0.02 = $0.06; buffer ≈ $0.34). Well below $5 KR escalation threshold; ~2.9% of $50 cap.

**Sequencing (chronological, retroactive backfill order):**
1. Rocket applies `_ELEMENT_MAP["physical"] = 1.0` 1-line fix at `phase5_pm1_multimodal_clustering.py:310-313`
2. Rocket re-runs Phase 5 PM-1 reps computation ONLY (skip GMM re-cluster; preserve cluster membership per Option B)
3. Re-fire Wave A (4+4+3 clusters across 3 seasons) — produces corrected faction_label_canonical + faction_thematic_tags
4. Re-fire {Wave-S, F-C} parallel post-Wave-A per Wave-S spec § 6 — chronological order S001 → S002 → S003 (W-S7 Jaccard distinctness gate operates against forward-coherent prior names)
5. Re-fire Wave B (100 kits across 3 seasons) — consumes corrected faction_label_canonical + season_name as SUBSTRATE_CONTEXT
6. Drax data-refresh fires post-rocket (auto via JSON re-read)
7. Cycle 14 v1 tag ratification pathway: aggregator-fix lands → retroactive refresh fires → drax data-refresh → v1 tag (NOT ship-then-refresh; coherent v1 ships with corrected names per Matt directive)

**Q1-Q6 resolved:** Q1=Option B; Q2=Wave B MUST re-fire; Q3=chronological Jaccard preserved; Q4=Option B honors aggregator-layer Designer-writes-substrate extension; Q5=Wanderer surface is OUT OF SCOPE (Cycle 15+); Q6=v1 ships post-refresh (NOT pre-).

---

## § 1 Election rationale — Q1-Q6 resolved with reasoning

### Q1 — Cluster-membership stability (Option A vs B vs C)

**Election: OPTION B — preserve existing GMM cluster membership; re-fire all 4 LLM wave surfaces (Wave A + Wave-S + F-C + Wave B).**

**Reasoning anchored on substrate-led discipline:**

The substrate-led discipline (Disc #41) says: substrate votes; designer doesn't pre-impose taxonomy. The question is WHICH substrate is voting.

The GMM clustering decision (k=3/4 selection + membership assignment) is the substrate's vote on **mechanical-vector adjacency** — kits cluster by BC tuple + cultural-lineage + element_encoded + primary_stat_encoded + tech_level + tone (the full 23-dim PM1KitVector). Adding "physical" to `_ELEMENT_MAP` changes 1 dimension of the 23-dim vector: STR→physical kits move from `element_encoded=0.5` to `element_encoded=1.0`. The other 22 dimensions are unaffected.

**The mechanical-vector adjacency vote is largely STABLE because:**
- STR-physical kits already cluster with STR kits via `primary_stat_encoded=0.0` (the strong vote)
- BC tuple + cultural lineage + tech level + tone are unchanged (the dominant clustering signals per PM-1 § 8.2)
- Element-vector dimension is ONE feature among 23; the GMM BIC selection prefers cluster geometries dominated by the strongest-signal dimensions
- Empirically (rocket forensics § Q1): the 3 physical kits in C1 are already-clustered with the earth-dominant + lightning-dominant + chain-strike-ranged STR cohort; moving them from 0.5→1.0 may shift centroids marginally but unlikely to change k or break membership

**The element_distribution aggregator vote is the SEPARATE, BROKEN vote.** That vote is at the cluster-rep computation layer (lines 678-686) — it reads `element_encoded` per member and decodes to nearest `_ELEMENT_MAP` key. Adding physical to the map fixes the decode. This is a vocabulary fix, NOT a cluster-membership fix.

**Option A (full re-cluster) trades substrate-led purity for unnecessary churn.** Re-clustering across 3 seasons may shift k=3↔4 selection per-season + break Phase 7 shipped_worthy decisions made on existing cluster membership (the 22+21+22=65 shipped-worthy kits across 3 seasons were Phase-7-gate-PASSED against existing cluster compositions; re-clustering re-fires Phase 7 against new compositions; Phase 7 acceptance rate may shift; Amendment 1 Wanderer architecture's SINGLETON classification may shift; cascade architecture integrity is destabilized). The substrate-led discipline does NOT require re-clustering when the substrate-encoding bug is at the AGGREGATOR LAYER (cluster-rep computation), not the CLUSTERING LAYER (centroid + membership assignment).

**Option C (Wave A + Wave-S only) under-honors the principle by leaving downstream Wave B narratives that quote the BIASED Wave A faction names un-refreshed.** Wave B narratives quote faction_label_canonical extensively ("Within the Stormbreak Vanguard..."; "anchor the Stormcallers' close-range pressure"). If Wave A re-fires and Stormbreak Vanguard becomes (e.g.) "Earthen Vanguard," Wave B narratives referencing "Stormbreak Vanguard" become DRIFT-MISMATCHED with their parent faction. Player-experience: reading the kit narrative does not match the faction tile name. Substrate-honest design surface FAILS. F-C also re-fires because F-C reads faction-pair names; biased pair names produce biased relationship narratives.

**Verdict: Option B preserves cluster-membership substrate-vote (stable + Phase-7-tested) while refreshing the entire LLM-narrative substrate-aggregation-to-player-experience handoff (corrected vocabulary).** This is the substrate-led discipline at the right scope: respect the geometry-layer vote (cluster membership); refresh the semantic-layer vote (faction + season + kit naming/narrative) because the aggregator vocabulary was broken at the semantic-layer handoff.

### Q2 — Wave B re-fire necessity

**Election: Wave B MUST re-fire across all 100 kits in 3 seasons.**

**Reasoning:** Wave B prompt receives `faction_label_canonical` from Wave A as SUBSTRATE_CONTEXT (per phase5_orchestrator.py:71 + canonical doc on Phase 5 LLM prompts). Empirical evidence from `wave_b_identities.json` shows Wave B narratives QUOTE faction names directly:
- "Within the Stormbreak Vanguard, this fighter is the ember that does not gust" (cluster 2)
- "anchor the Stormcallers' close-range pressure before the lightning and shadow currents ignite" (cluster 3)
- "Stormbreak Vanguard Thunderstrike Warden" (the kit_name_canonical itself bakes faction context)

If Wave A re-fires with corrected (less lightning-biased) faction names, Wave B narratives become:
- Lexically drift-mismatched ("Within the Stormbreak Vanguard..." but the faction is now "Earthen Vanguard")
- Thematically drift-mismatched ("lightning and shadow currents ignite" but the corrected faction has earth as dominant element)
- Player-experience-incoherent (faction tile reads X; kit narrative references Y)

The Wave B SUBSTRATE_CONTEXT field also now includes `{season_name}` per Wave-S spec § 6; if Wave-S re-fires with corrected dominant_element, kit narratives that compose season context become drift-mismatched too.

**Cost analysis (3-season Wave B re-fire):** 100 kits × ~$0.01 per Wave B call = ~$1.00. Plus star-lord's retry-on-parse-failure logic (recently fixed) prevents the 34-nameless-kit regression.

**Verdict: Wave B re-fire is mandatory for Option B coherence. Skipping Wave B re-fire (Option C trade-off) produces drift-mismatch between faction-tile names and kit-narrative quotes.**

### Q3 — Wave-S retroactive sequencing

**Election: Wave-S re-fires AFTER Wave A re-fire, in chronological season order (S001 → S002 → S003), parallel-OK with F-C.**

**Reasoning anchored on Wave-S spec § 6 + § 8:**

Wave-S consumes Wave A faction_name_set as PRIMARY substrate (per spec § 2 substrate inputs table row 1) + Wave A faction_thematic_tags_aggregate as PRIMARY substrate (row 2). Chronological dependency: Wave A re-fire MUST complete BEFORE Wave-S re-fire per season.

**Within-season:** {Wave-S, F-C} parallel-OK per spec § 6 (no inter-dependency). Wave-S fires AFTER Wave A; F-C fires AFTER Wave A; neither blocks the other; both block Wave B.

**Across-season:** Wave-S W-S7 distinctness gate operates Jaccard <0.5 against `PRIOR_SEASON_NAMES` (Wave-S spec § 5 W-S7 + § 8 backfill ordering). Chronological order required for the gate to operate forward-coherently:
- S001 fires FIRST with `PRIOR_SEASON_NAMES=[]` (empty list; gate trivially PASS)
- S002 fires SECOND with `PRIOR_SEASON_NAMES=["<S001 name>"]` (gate operates against S001 corrected name)
- S003 fires THIRD with `PRIOR_SEASON_NAMES=["<S001 name>", "<S002 name>"]` (gate operates against both prior)

**Why NOT parallel across seasons:** if Wave-S fires S001+S002+S003 in parallel, all three see empty `PRIOR_SEASON_NAMES` and may produce lexically-collidng names (the actually-observed lightning-storm substrate homogeneity across 3 seasons would otherwise produce "Season of the Storm-X" / "Season of the Stormbreak-X" / "Season of the Stormveil-X" — distinctness fails). Chronological forced.

**Composition with existing post-fix Wave-S outputs (currently in `season_summary.json`):** existing outputs ("Season of the Lightning-Scorched Chain" / "Season of the Storm-Shadowed Siege" / "Season of the Grounded Arcs") were produced from BIASED Wave A faction names (e.g., "Stormfield Chain Wardens" which over-reported lightning at 31% when earth was actual dominant at 38%). The W-S7 distinctness gate was PASSED against ITSELF (chronological order honored); but the lightning over-reporting in faction names + element_distribution biased the substrate INPUT to Wave-S, producing lightning-themed season names that misrepresent substrate truth. Re-fire produces forward-coherent corrected names.

**Verdict: chronological order required; Jaccard W-S7 distinctness preserved through forward-coherent re-fire; existing Wave-S outputs overwritten by re-fire (cache-key by season_id per spec § 8 enables idempotent overwrite).**

### Q4 — Composition with Designer-writes-substrate principle

**Election: Option B HONORS the principle at the aggregator-layer extension that jack-ryan named.**

**Reasoning anchored on Designer-writes-substrate § 4.1 + jack-ryan extension:**

Per Designer-writes-substrate § 4.1: *"Designer-fiat impositions of player-experience taxonomy at this layer are violations of substrate-led discipline + this principle."* The principle locates substrate-led discipline at TWO layers:
1. **Generative-input layer** (substrate-led; designer codifies from external evidence; no fiat impositions)
2. **Player-experience layer** (player-names emerges from community; engine consumes post-emergence)

Jack-ryan framing-audit § 5 EXTENDS this to a THIRD locus: **aggregator-vocabulary-staleness at the substrate→LLM-input handoff layer.** Jack-ryan verbatim § 5: *"Instance 6 #8 is the first confirmed case where Disc #41 (substrate-led discipline) drift occurs NOT at the substrate-generation layer but at the substrate-aggregation-to-LLM-input layer. The Designer-Writes-Substrate principle extends Disc #41 to this handoff boundary — the aggregator must faithfully represent what the substrate contains."*

The substrate truth at season_001 C1 is: earth=5, physical=3, fire=2, wind=1, lightning=1, holy=1. The aggregator reported: earth=38%, lightning=31%, fire=15%, wind=8%, holy=8%, physical=0%. The aggregator misrepresented substrate truth. The LLM is doing its job correctly given biased input.

**Option A** (full re-cluster) is substrate-led PURE but RE-VOTES on the geometry layer unnecessarily (the geometry-layer vote is correct; only the vocabulary at the aggregation-layer was broken). Option A applies substrate-led discipline at the wrong scope.

**Option B** corrects the substrate-led DRIFT at the right scope: the substrate-aggregation-to-LLM-input handoff (Wave A faction-naming + Wave-S season-naming + F-C relationship-naming + Wave B kit-naming all receive substrate-truth-respecting input now).

**Option C** partially honors the principle (Wave A + Wave-S corrected) but leaves Wave B with drift-mismatched narratives quoting biased Wave A names — the player-experience-layer surface (kit-tile-content reading the faction-tile-content) breaks. Principle violation at the player-experience presentation layer.

**Verdict: Option B is the canonical substrate-led discipline application at the aggregator-vocabulary-staleness scope jack-ryan named.**

### Q5 — Wanderer surface composition

**Election: WANDERER surface is OUT OF SCOPE for this remediation. Cycle 15+ separate investigation.**

**Reasoning anchored on substrate-tag-vs-cluster-membership disjoint:**

The drax-discovered 2 Wanderer-tagged kits (season_001 + season_002) at substrate level vs gamora Amendment 1 SINGLETON classification at cluster level is a SEPARATE design surface from the element_distribution aggregator vocabulary bug. The two operate on different layers:

| Layer | What this remediation touches |
|---|---|
| Substrate kit-tag layer (Wanderer tag at kit-data level) | UNTOUCHED |
| GMM cluster-membership layer (SINGLETON classification) | UNTOUCHED (Option B preserves) |
| Aggregator vocabulary layer (`_ELEMENT_MAP`) | FIXED |
| LLM-naming layer (Wave A/Wave-S/F-C/Wave B) | RE-FIRED |

**Verification:** Wave B output across all 3 seasons shows ZERO Wanderer references in kit narratives (`grep -c Wanderer` returns 0 per file). The current `phase5_faction_clusters.json` has no SINGLETON cluster_id either. Drax's loadout fallback renders "Wanderers" tile directly from wave_b data when the Wanderer-tag-at-substrate-level exists without a matching SINGLETON cluster (drax `Cycle14SeasonSection.tsx` line 121-122: *"Wanderer kits exist in wave_b but no SINGLETON cluster in faction JSON — render a Wanderer tile directly from wave_b data."*).

**Cluster-shift risk under Option B:** Option B does NOT re-cluster; Wanderer count from the SINGLETON-classification path is INVARIANT under this remediation. Drax's substrate-tag-fallback path is invariant too (substrate kit-tags unchanged). The drift-mismatch (substrate-tag Wanderer vs cluster-SINGLETON Wanderer) is the SAME design surface before and after this remediation.

**Why Cycle 15+:** the Wanderer-tag-vs-SINGLETON-classification disjoint requires:
- Substrate-curation analysis (when does a kit-tag-level Wanderer NOT become a cluster-SINGLETON?)
- Amendment 1 architectural amendment if needed (gamora seam)
- Drax data-contract refinement (galadriel-drax hero pair Amendment 2 § 12.1 composition)
- Substrate-led discipline application at the kit-tag layer

This is a substantial Cycle 15+ workstream. It is NOT a vocabulary-staleness bug.

**Verdict: Wanderer surface composition is OUT OF SCOPE. Surface for Cycle 15+ wave-close as a separate investigation candidate.**

### Q6 — Cycle 14 v1 close pathway

**Election: aggregator-fix lands → retroactive refresh fires → drax data-refresh → Cycle 14 v1 tag ratification (Matt-surface).**

**Reasoning:** Matt verbatim message 1 says "Let's fix this retroactively"; message 2 says "once the lightning-themed faction issue has been resolved, please retroactively refresh the season names as well." The intent is unambiguously: fix BEFORE shipping. Matt did NOT say "ship v1 with biased names then fix later."

**The "NOT v1 blocking" classification (Matt hive-mind-state line 5408) modulates the SEVERITY of the surface, not the SEQUENCING:**
- INFO severity = does not block v1 tag from being achievable
- BUT the retroactive fix is in-flight per Matt directive
- Sequencing question is: does v1 tag happen BEFORE the fix lands (ship-then-refresh) OR AFTER (refresh-then-ship)?

The substrate-led discipline (and the Designer-writes-substrate principle § 4.4 player-facing surface integrity) argues for refresh-then-ship:
- Player-facing surface is the loadout app summary tab + faction tiles + kit narratives + season-name headers
- v1 = first player-facing release of Cycle 14 substrate
- Shipping v1 with player-facing-surface contamination ("Season of the Lightning-Scorched Chain" misrepresenting an earth-dominant season; faction tile "Stormbreak Vanguard" mismatched to kit narrative quoting it) violates the principle's § 4.4 player-experience-coherence requirement
- The fix cost (~$1.45) is trivially in-envelope; the time-cost (rocket dispatch + retroactive fire + drax auto-refresh) is small relative to the v1 tag importance

**Composition with the Cycle 14 v1 close sequencing (post-drax close per hive-mind-state):** v1 tag ratification was already on the "post-drax close" pathway. This remediation adds a 1-step prerequisite: rocket fix-and-refire fires BEFORE drax data-refresh (drax consumes corrected data). Net change: drax data-refresh sequencing moves from "after star-lord nameless-kit close" to "after rocket aggregator-fix-and-refire" (still 1 step before v1 tag ratification).

**Verdict: refresh-then-ship. v1 ships post-refresh with coherent player-facing surface. Cycle 14 v1 close pathway: rocket aggregator-fix dispatch → retroactive re-fire (all 4 LLM waves × 3 seasons) → drax data-refresh → Matt-surface v1 tag ratification.**

---

## § 2 Cluster-membership stability disposition (Q1 detailed)

**Option elected: B.**

**What Option B preserves:**
- GMM BIC k selection per season (k=4 for S001, k=4 for S002, k=3 for S003)
- Cluster membership assignments (which kit goes to which cluster_id)
- Phase 7 shipped_worthy decisions (22+21+22=65 kits across 3 seasons; gauntlet sim results stable)
- Amendment 1 Wanderer architecture (SINGLETON classification rules)
- Cascade architecture integrity (Phase 4 → Phase 5 → Phase 7 chain unchanged at the geometry layer)
- `pairwise_distance_distribution` per cluster (G-B telemetry stable)
- `primary_pair_flag` + `gb_selection_rationale` per cluster (G-B selection stable)

**What Option B re-runs (the targeted fix):**
- `_compute_cluster_reps()` aggregator at lines 635-736 (cluster-rep recomputation against corrected `_ELEMENT_MAP`)
- Output fields per cluster: `element_distribution`, `dominant_element`, `element_token`, `faction_label_placeholder` (the four cluster-rep fields that consume `_ELEMENT_MAP` decode)
- Wave A LLM call per cluster (4+4+3=11 calls) with corrected element_distribution + dominant_element + element_token in USER prompt
- Wave-S LLM call per season (3 calls) with corrected Wave A outputs as primary substrate
- F-C LLM call per faction-pair (6+6+3=15 calls) with corrected modal_cultural_lineage + dominant_element decoding
- Wave B LLM call per kit (34+33+33=100 calls) with corrected faction_label_canonical + season_name as SUBSTRATE_CONTEXT

**Implementation note for rocket:** the re-run path can be implemented as a Phase-5-rep-recompute-only-with-fixed-ELEMENT_MAP dispatch (skip Phase 5 PM-1 GMM re-cluster; re-run cluster-reps + LLM waves only). Cluster membership preserved by reading existing kit→cluster assignments from `phase5_faction_clusters.json` (member_kit_ids array per cluster_id). Cleaner than `start_from_phase=5` (which would re-cluster); cleaner than full Phase 5 re-fire (which would re-cluster too).

**Acceptance verification for Option B:**
- Each existing season's `cluster_id` set must match pre-fix `cluster_id` set (1, 2, 3, 4 for S001/S002; 1, 2, 3 for S003)
- Each existing `member_kit_ids` array must match pre-fix `member_kit_ids` array (membership stable)
- `element_distribution` per cluster must NOW include `physical` as a key when STR-physical kits are members (vocabulary corrected)
- `dominant_element` per cluster may shift (e.g., season_001 C1 should now report `earth` at 5/13 = 38.5%; lightning at 1/13 = 7.7%; physical at 3/13 = 23.1%) — corrected from prior `earth` 38.5% / `lightning` 30.8%
- Wave A faction_label_canonical may shift (LLM elects different epithets given corrected element_distribution)
- Wave B kit_name_canonical may shift (LLM elects different epithets given corrected faction context)

---

## § 3 Wave B re-fire necessity (Q2 detailed)

See § 1 Q2 reasoning. Verdict: MANDATORY.

**Cost:** 100 kits × ~$0.01 = ~$1.00. Star-lord's retry-on-parse-failure logic (recent fix per hive-mind-state cascade-r4 follow-on) prevents the 34-nameless-kit regression.

**Acceptance verification:**
- All 100 kits produce non-empty `kit_name_canonical` post-re-fire (100% coverage matching the post-star-lord-Scope-3 close)
- Wave B narratives quoting parent faction names match the NEW faction_label_canonical (not the old lightning-biased names)
- Wave B narratives composing season_name as context match the NEW Wave-S season name (not the old lightning-biased one)
- No regression in `final_compliance_status: ACCEPT` rate vs current state

---

## § 4 Wave-S retroactive sequencing (Q3 detailed)

See § 1 Q3 reasoning. Verdict: chronological S001 → S002 → S003; W-S7 Jaccard distinctness preserved.

**Concrete fire-order per season (Wave-S spec § 6 within-season):**
```
[per season, sequentially S001 → S002 → S003]:
  1. Wave A re-fire (parallel within-season for all clusters per season)
  2. {Wave-S, F-C} parallel re-fire (consumes Wave A; Wave-S adds prior_season_names from completed prior seasons)
  3. Wave B re-fire (parallel within-season for all kits per season; consumes faction_label_canonical + season_name)
```

**Across-season Wave-S distinctness verification:**
- S001 Wave-S re-fires with `PRIOR_SEASON_NAMES=[]`; gate trivially PASS
- S002 Wave-S re-fires with `PRIOR_SEASON_NAMES=["<S001 corrected>"]`; gate Jaccard >0.5
- S003 Wave-S re-fires with `PRIOR_SEASON_NAMES=["<S001 corrected>", "<S002 corrected>"]`; gate Jaccard >0.5 against both

**Failure-mode handling per Wave-S spec § 5 W-S7:** if W-S7 fails on first re-fire of S002 or S003, orchestrator passes `diversity_penalty_preamble` with enumerated prior season names to regeneration; max 1 regeneration per call.

**Why this matters now (post-correction):** under biased aggregator, all 3 seasons received lightning-themed substrate inputs to Wave-S; lightning-themed names emerged across all 3 ("Lightning-Scorched", "Storm-Shadowed", "Grounded Arcs" all lightning-coded). With corrected aggregator showing season-specific dominant elements (S001 earth-dominant; S002 likely shadow-or-earth dominant; S003 mixed-shadow-water-dominant), the corrected Wave-S outputs will be naturally MORE distinct (substrate-honest variance > biased homogeneity). W-S7 gate likely PASSES easily under correction.

---

## § 5 Composition with principles (Q4 detailed)

See § 1 Q4 reasoning. Verdict: Option B honors Designer-writes-substrate § 4.1 + jack-ryan aggregator-layer extension.

**Cross-doc composition map:**

| Principle / discipline | Composition with Option B |
|---|---|
| Disc #41 (substrate-led discipline) | Option B applies discipline at aggregator-vocabulary-staleness scope (the correct scope per jack-ryan extension) |
| Designer-writes-substrate § 4.1 (aggregator must faithfully represent substrate) | Option B fixes the aggregator vocabulary so substrate truth (physical kits) is represented |
| Designer-writes-substrate § 4.4 (player-experience-coherence requirement) | Option B re-fires Wave B narratives so player-experience surface (kit-tile reading faction-tile + season-name) is coherent |
| Wave-S spec § 6 (sequencing) | Option B fires Wave-S per spec sequencing (post-Wave-A, parallel-OK F-C, pre-Wave-B) |
| Wave-S spec § 8 (retroactive backfill) | Option B uses chronological season order per spec; cache-key by season_id enables overwrite |
| Doc 47 § 4.6.5 ELEMENT_CONVERSION Layer 2 (STR→physical via weapon damage) | Option B re-encodes physical at the aggregator vocabulary so this canonical commitment is honored at the LLM-input layer (currently it is HONORED at substrate-truth layer but DROPPED at aggregator-vocab layer) |
| Amendment 7 STAT_ELEMENT_POOLS (STR→{physical}) | Same as above — substrate honors; aggregator fix propagates to LLM-naming surface |
| Discipline #45 (vocabulary lock) | Option B does NOT touch Discipline #45 vocabulary; Wave A/Wave-S/F-C/Wave B substrate-purity preconditions (Wave A § 2.5 / Wave-S § 5 W-S8) still enforced at re-fire |

**Aggregator-layer extension to Designer-writes-substrate principle (proposed canonical update):**

Per jack-ryan framing-audit § 5 + this remediation's empirical confirmation, the Designer-writes-substrate principle § 4.1 should be EXTENDED to explicitly name the aggregator layer:

> "Designer-fiat impositions of player-experience taxonomy at the generative-input layer are violations of substrate-led discipline + this principle. **Aggregator-vocabulary-staleness at the substrate→LLM-input handoff layer (e.g., a categorical encoding map that was authored with N values where the canonical catalog has been since expanded to N+1) is ALSO a violation: the aggregator misrepresents substrate truth to the LLM, producing player-facing surfaces that are substrate-dishonest even when the LLM is operating correctly given its inputs.** Aggregator vocabulary completeness must be audited at any Amendment that expands a categorical catalog."

This is the canonical-write candidate for wave-close per § 9 below.

---

## § 6 Wanderer surface composition (Q5 detailed)

See § 1 Q5 reasoning. Verdict: OUT OF SCOPE. Cycle 15+ separate investigation.

**Surface for Cycle 15+ investigation:**

| Question | Cycle 15+ scope |
|---|---|
| When does substrate-level Wanderer-tag NOT become cluster-level SINGLETON? | Substrate-tag rules + GMM clustering interaction with kit-level Wanderer marker |
| Should Wanderer-tagged kits force SINGLETON cluster classification? | Amendment 1 architectural amendment candidate (gamora seam) |
| How does drax render the disjoint cleanly? | Drax data-contract: substrate-tag-fallback vs cluster-SINGLETON-primary rendering rules |
| Does galadriel-drax hero pair (Amendment 2 § 12.1) elect Wanderer-as-hero from substrate-tag OR cluster-SINGLETON? | Amendment 2 § 12.1 composition refinement |

**This remediation's contract with Wanderer surface:** Option B PRESERVES current state (substrate-tag Wanderer kits + zero cluster-SINGLETON + drax fallback rendering). The element_distribution aggregator fix DOES NOT touch Wanderer-tag substrate; DOES NOT touch GMM cluster membership; DOES NOT touch drax rendering rules. Post-fix Wanderer surface IS-IDENTICAL to pre-fix.

---

## § 7 Cycle 14 v1 close sequencing (Q6 detailed)

See § 1 Q6 reasoning. Verdict: refresh-then-ship. v1 ships post-refresh.

**Concrete sequencing dispatch chain:**

```
1. KR fires rocket aggregator-fix-and-refire dispatch
   - Apply _ELEMENT_MAP physical addition (1-line)
   - Re-run cluster-rep computation per Option B (preserve membership)
   - Re-fire Wave A across 3 seasons (11 LLM calls)
   - Re-fire {Wave-S, F-C} per spec sequencing across 3 seasons (18 LLM calls)
   - Re-fire Wave B across 3 seasons (100 LLM calls)
   - Update phase5_faction_clusters.json + season_summary.json + wave_b_identities.json artifacts
   - MIGRATION.md §v1.66 entry (additive; element_distribution semantic correction)
   - Cost: ~$1.45 (well below $5 KR threshold)

2. Drax data-refresh auto-fires post-rocket close
   - Re-read JSON artifacts; loadout app re-renders with corrected names
   - No drax code change required; data-contract stable; auto-propagation
   - Drax surface verification: season-name header + faction tiles + kit narratives all coherent post-refresh

3. Jack-ryan Gate-2 verification (per critique-pair Pattern E if KR elects)
   - Wave B narratives quote NEW faction_label_canonical (no lexical drift)
   - Wave-S season names substrate-honest against corrected element_distribution
   - Phase 7 shipped_worthy count unchanged (cluster membership preserved per Option B)
   - element_distribution per cluster includes physical key for STR-physical clusters

4. KR surfaces Cycle 14 v1 tag ratification to Matt (Matt-surface; user-facing surface coherent + corrected; v1 tag fires)
```

**Composition with prior cascade-r4 work (cycle-14-hive-mind-state.md):**
- This remediation IS the final pre-v1 quality gate identified by Matt's two-message directive
- Star-lord nameless-kit remediation (recently closed) already produced 100% kit coverage
- Drax loadout refresh authorization is gated on aggregator-fix-and-refire per this remediation (NOT on the prior nameless-kit-remediation which has already closed)
- The drax loadout refresh post-rocket-aggregator-fix is the new sequencing

---

## § 8 Wave-S spec amendment (if any)

**Election: NO amendment required to Wave-S spec.** Existing spec § 8 retroactive backfill plan + § 6 sequencing are sufficient.

**Reasoning:** the Wave-S spec § 8 already specifies:
- Chronological backfill ordering (S001 first, S002 second, S003 third)
- W-S7 Jaccard distinctness gate operates retroactively in chronological substrate order
- Cache-key by `season_id` enables idempotent re-fire safety + retroactive backfill without per-timestamp drift
- "Same season_id → same cache key → same Wave-S call (or cache-hit on second invocation)"

The remediation re-fires Wave-S against the SAME season_ids but with CORRECTED substrate inputs (corrected Wave A faction names + corrected element_distribution). The cache-key invariance means the re-fire overwrites the existing Wave-S output cleanly (rocket's per-season cache-key for Wave-S enables retroactive overwrite per spec § 8). No spec amendment required.

**One operational note (NOT a spec amendment; an execution flag):** rocket execution should ensure cache invalidation on Wave-S re-fire so the new outputs are NOT cache-hits against the old (biased) outputs. Cache-key by season_id + a Wave-S-input-hash sub-key (faction_name_set + element_distribution) enables this: if the Wave A substrate inputs differ post-aggregator-fix, the input-hash differs, and re-fire produces new output without cache collision. Rocket's cache implementation decision (per Wave-S spec § 9 implementation detail OUT of spec scope) — recommend input-hash-aware cache keying.

---

## § 9 Canonical-write capture

**Sub-discipline candidate (jack-ryan framing-audit § 6 P1 wave-close write):**

**Name:** Vocabulary-staleness-vs-substrate-expansion gap

**Description:** When the substrate canonical catalog expands (e.g., Amendment 7 adding physical as behavioral element), ALL downstream consumers of the categorical vocabulary must be audited for vocabulary completeness. Consumers include: encoding maps (`_ELEMENT_MAP`, `_LINEAGE_MAP`, `_TONE_MAP`, etc.), aggregation functions, prompt-construction formatters, decode-then-report paths. A vocabulary-missing element defaults to a float sentinel value that nearest-neighbor decodes to an incorrect element. The downstream LLM-naming surface produces substrate-dishonest player-facing names while the LLM operates correctly given its (biased) inputs.

**This gap is distinct from:**
- Structural-vs-behavioral variation gap (Instance 6 #3/#4) — consumer exists and fires correctly; this gap = consumer reads the right data but with stale vocabulary
- Layer-isolation-vs-integration gap (Instance 6 #5) — consumer reads wrong source; this gap = consumer reads right source with stale vocabulary
- Phantom-component gap (Instance 6 #1) — consumer is missing; this gap = consumer exists but vocabulary is stale

**Acceptance criterion (for inclusion in engineering-disciplines.md):**

> At any Amendment that expands a canonical categorical catalog (element / attribute / lineage / period / register / weapon-family / geometry / tone), the Amendment dispatch MUST include a verification step: grep all encoding maps in downstream consumers and verify all canonical catalog values are present in the encoding map. If any value is absent, add it before the Amendment dispatch fires its first acceptance test.

**Composition with Designer-writes-substrate principle § 4.1 extension (proposed):**

Per § 5 above, Designer-writes-substrate principle § 4.1 should be EXTENDED to name the aggregator layer as a third locus where substrate-led discipline drift can occur. The aggregator-vocabulary-staleness gap is the FIRST CONFIRMED CASE of this third-locus drift; this remediation establishes the canonical pattern for future Amendments.

**Disc #42a Q7 candidate (proposed for jack-ryan canonical-write):**

> Q7 — Vocabulary completeness audit. For any Amendment that expands a categorical catalog: are all downstream consumer encoding maps updated to include the new catalog value? Specifically: grep all `_<NAME>_MAP` patterns in Phase 5 (and other LLM-prompt-feeding modules); verify every canonical catalog value is a key in the relevant map. If any value is absent, add it before fire.

**Wave-close registration:** P1 priority for jack-ryan wave-close canonical-write per framing-audit § 6.

**Cross-discipline composition:**
- Discipline #41 (substrate-led discipline) — Q7 extends Disc #41 to the aggregator-vocabulary-staleness gap; substrate truth flows through aggregator with vocabulary-completeness
- Discipline #42 (framing-audit at dispatch consumption) — Q7 is a framing-audit checklist item for Amendment dispatches specifically
- Discipline #42a (Q1-Q6 framing-audit) — Q7 extends this to vocabulary completeness
- Discipline #45 (vocabulary lock for class names) — Q7 is the ADDITIVE side (vocabulary-expansion-with-consumer-audit); Disc #45 is the EXCLUSIONARY side (vocabulary-lock-no-leak)

---

## § 10 Cost projection (3-season aggregate per option; vs $50 cap)

| Option | Rocket effort | Re-clustering | Wave A re-fire | Wave-S re-fire | F-C re-fire | Wave B re-fire | 3-season aggregate | % of $50 cap | KR escalation? |
|---|---|---|---|---|---|---|---|---|---|
| A (full re-cluster) | High (re-run Phase 5 PM-1 from scratch) | YES (k may shift; Phase 7 re-fire too) | YES (11+ calls; cluster count may change) | YES (3 calls) | YES (15+ calls; pair count may change) | YES (100+ calls) | ~$1.50 + Phase 7 re-fire cost (uncertain; possibly +$0.50-$2.00) | 3-7% | NO at central estimate; potentially YES if Phase 7 re-fire surfaces |
| **B (existing clusters + all LLM waves)** | Low (vocab fix + targeted re-run) | NO | YES (11 calls) | YES (3 calls) | YES (15 calls) | YES (100 calls) | **~$1.45** ($0.22 Wave A + $0.045 Wave-S + $0.30 F-C + $1.00 Wave B + buffer) | **~2.9%** | **NO** |
| C (existing clusters + Wave A + Wave-S only) | Low (vocab fix + Wave A + Wave-S re-run) | NO | YES (11 calls) | YES (3 calls) | NO | NO (existing Wave B retained with drift-mismatch) | ~$0.27 | 0.5% | NO |

**Per-call cost estimates (informed by hive-mind-state cascade-r4 prior Wave B re-fire actuals):**
- Wave A: ~$0.02 per cluster
- Wave-S: ~$0.015 per season (Wave-S spec § 8)
- F-C: ~$0.02 per pair (analogous to Wave A; substrate-aggregate prompt similar token cost)
- Wave B: ~$0.01 per kit (per recent hive-mind-state observation; 34 kits × $0.01 = $0.34 actuals)

**Recommended option (B) total: ~$1.45 (2.9% of $50 cap) — NO KR escalation required per dispatch acceptance criterion ($5 threshold).**

---

## § 11 Rocket execution spec

**Dispatch: rocket aggregator-fix-and-refire (Option B; ~$1.45)**

**Scope:**

1. **Apply 1-line fix at `reincarnated-engine/src/reincarnated/generation/phase5_pm1_multimodal_clustering.py` lines 310-313:**
   - Add `"physical": 1.0,` as 8th entry in `_ELEMENT_MAP`
   - Update `PM1KitVector.element_encoded` docstring at line ~150 to include "physical" in the supported elements list

2. **Implement retroactive re-fire path** (rocket selects implementation pattern — recommend a new function `retroactive_phase5_rep_recompute_and_llm_refire(season_id, preserve_clusters=True)`):
   - Read existing `phase5_faction_clusters.json` per season; extract `member_kit_ids` per `cluster_id` (preserves membership per Option B)
   - Re-run `_compute_cluster_reps()` per cluster against fixed `_ELEMENT_MAP` (corrected element_distribution + dominant_element + element_token + faction_label_placeholder per cluster)
   - Re-fire Wave A LLM call per cluster (corrected element_distribution + dominant_element in USER prompt; cache-bust by input-hash)
   - Re-fire `{Wave-S, F-C}` parallel post-Wave-A per Wave-S spec § 6 (chronological season order S001→S002→S003 for W-S7 Jaccard distinctness)
   - Re-fire Wave B LLM call per kit (corrected faction_label_canonical + season_name in SUBSTRATE_CONTEXT; cache-bust by input-hash)
   - Overwrite `phase5_faction_clusters.json` + `season_summary.json` + `wave_b_identities.json` artifacts per season

3. **MIGRATION.md §v1.66 entry** (additive):
   - Element_distribution aggregator vocabulary correction
   - Cluster membership preserved (Option B); LLM-naming surface refreshed
   - Backward-compatible at schema level; semantic correction at content level
   - Pre-fix Wave A/Wave-S/Wave B outputs marked HISTORICAL via deprecated timestamp

4. **Tests** (rocket scope):
   - Unit test: `_ELEMENT_MAP` contains all 8 canonical elements (fire, water, earth, wind, lightning, holy, shadow, physical)
   - Unit test: `encode_categorical("physical", _ELEMENT_MAP)` returns 1.0 (or whichever ordinal rocket elects); decode round-trip returns "physical"
   - Integration test: `_compute_cluster_reps()` with mixed-element member kits including physical produces `element_distribution` with `physical` key
   - Acceptance test: season_001 C1 post-fix `element_distribution` matches substrate truth (earth=38.5%, physical=23.1%, fire=15.4%, wind=7.7%, lightning=7.7%, holy=7.7%)

5. **Acceptance criteria (rocket dispatch close):**
   - All 3 seasons re-fire successfully (zero error; zero nameless kits per Matt nameless-kit directive)
   - Cluster membership stable per Option B (member_kit_ids arrays match pre-fix)
   - element_distribution per cluster includes physical key when STR-physical kits are members
   - Wave A faction names + Wave-S season names + Wave B kit names refreshed across 3 seasons
   - Total cost ≤$5 (well below KR escalation threshold)
   - tag `rocket/v1.0-cascade-r4-element-distribution-aggregator-remediation-1`

**Handoff sequencing:**
1. Rocket fires dispatch → fix + retroactive re-fire executes → artifacts overwritten
2. Drax data-refresh auto-fires (drax consumes JSON artifacts; no drax code change)
3. KR surfaces Cycle 14 v1 tag ratification per § 7 sequencing

**Out of scope for rocket (gandalf coordination):**
- Wanderer surface investigation (Cycle 15+)
- Disc #42a Q7 canonical-write (jack-ryan wave-close)
- Designer-writes-substrate principle § 4.1 extension (gandalf canonical update post-remediation)

---

## § 12 Sign-off

**Authored:** gandalf (story-and-design steward) per Matt 2026-05-29 two-message verbatim directive (lightning-themed faction retroactive fix + season-name retroactive refresh) under hive-mind decision-routing.

**For:** the durable canonical coordination of the Phase 5 element_distribution aggregator vocabulary-staleness remediation — resolving cluster-membership-stability + Wave B re-fire necessity + Wave-S retroactive sequencing + Designer-writes-substrate principle composition + Wanderer surface scoping + Cycle 14 v1 close pathway. Recommended Option B (preserve clusters; refresh all LLM waves) honors substrate-led discipline at the aggregator-vocabulary-staleness scope jack-ryan named; produces forward-coherent player-facing surface across 3 seasons; trivially in $5 cost envelope.

**Q1-Q6 verdicts summary:**
- Q1: Option B (existing clusters + all-LLM-waves refresh)
- Q2: Wave B MUST re-fire (faction-name quotes in narratives)
- Q3: Chronological S001→S002→S003 (W-S7 Jaccard distinctness forward-coherent)
- Q4: Option B honors Designer-writes-substrate § 4.1 + aggregator-layer extension
- Q5: Wanderer surface OUT OF SCOPE (Cycle 15+ separate investigation)
- Q6: refresh-then-ship (v1 tag post-rocket-aggregator-fix-and-refire; per Matt directive intent)

**Cost projection (Option B, 3-season aggregate):** ~$1.45 (2.9% of $50 cap; NO KR escalation required per $5 threshold)

**Rocket execution spec (handoff summary):** § 11 — 1-line `_ELEMENT_MAP` fix + retroactive re-fire (preserve cluster membership; re-fire all 4 LLM waves per Wave-S spec sequencing) + MIGRATION.md §v1.66 + tests + tag

**Canonical-write capture (wave-close P1 candidate):** vocabulary-staleness-vs-substrate-expansion gap sub-discipline; Disc #42a Q7 candidate; Designer-writes-substrate principle § 4.1 aggregator-layer extension; criterion "grep all _<NAME>_MAP encoding maps when adding canonical catalog value"

**Cycle 14 v1 close sequencing recommendation:** rocket aggregator-fix-and-refire dispatch → drax data-refresh auto-propagation → jack-ryan Gate-2 verification (optional Pattern E) → KR Matt-surface for v1 tag ratification

**Composition target:** rocket combined dispatch (next sequencing step per § 11); jack-ryan wave-close canonical-write of Disc #42a Q7 + Designer-writes-substrate § 4.1 extension; gandalf canonical update of Designer-writes-substrate principle post-remediation

**Tag target:** `gandalf/v1.0-element-distribution-aggregator-remediation-coordination-1`

Engine first. Game second. Phase third.
