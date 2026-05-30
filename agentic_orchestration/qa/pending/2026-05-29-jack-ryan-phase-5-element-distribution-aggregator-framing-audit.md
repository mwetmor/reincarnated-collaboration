# Framing-Audit Finding — 2026-05-29 — Phase 5 Element Distribution Aggregator Drift

**Reviewer:** jack-ryan
**Severity:** INFO (NOT Cycle 14 v1 BLOCKING — per Matt explicit; see § 7)
**Scope:** Disc #42a Q1-Q6 framing-audit on Phase 5 element_distribution aggregator drift + Instance 6 cumulative numbering reconciliation
**Authority:** Matt 2026-05-29 cascade-r4 § Element Distribution Aggregator Drift; parallel fan-out directive
**Disciplines applied:** #41, #42, #42a, #43, #45
**Principles applied:** 1, 2, 3

---

## § 0 — Numbering Reconciliation (REQUIRED FIRST)

The prompt notes ambiguity: "is this #7 or #8?" This must be resolved before Q-audit proceeds.

**Cumulative Instance 6 surface record from prior findings:**

| # | Surface | Status | Closure |
|---|---|---|---|
| #1 | Phase 7 C-2 compactness gap — root cause | CLOSED | Amendment 1 Wanderer architecture |
| #2 | Path X wire-up scope | CLOSED | cascade-r4 Path X |
| #3 | GMM BIC k selection | CLOSED | Phase 5 PM-1 gate |
| #4 | chain_2 element — Amendment 7a | CLOSED | commit `5b76790` |
| #5 | config_to_kit collision — DEFERRED | DEFERRED | Cycle 15+ |
| #6 | Gauntlet encounter coverage — Amendment 8 / W-α6 | CLOSED | Amendment 8 |
| #7 | Phase 7 C-2 compactness at n=34 scale | CLOSED | Amendment 1 Wanderer architecture (Gate-2 review `0bee7b2`) |

**The prior Gate-2 review (`0bee7b2`) explicitly closed Instance 6 #7 as "RESOLVED at architectural layer by Amendment 1."** That review stated: "Cumulative: 7 surfaces documented."

**The Phase 4→Phase 5 archive bypass (layer-isolation-vs-integration gap)** documented at cascade-r3 Instance 6 #5 framing-audit (`eb14ec3`) was surface **#5 in the ordering at that time** — but the numbering at that session was 1-5, representing the five surfaces known then. After the Gate-2 review series closed #6, #7 via Amendment 8 / Amendment 1, the sequence rebuilt to 7.

**This Matt-surfaced aggregator drift is therefore Instance 6 #8.**

Note: the prompt instruction states "Cumulative Disc #42a Instance 6 pattern: now 8 surfaces" (hive-mind-state line 5410). This confirms #8.

**DISPOSITION: Instance 6 #8.**

---

## § 1 — Empirical State (Survey-mode: what IS)

Before applying the Q-audit, the empirical state as found:

**Observed pattern** (Matt-surfaced; consistent across all 4 clusters season_001 + spot-check 002/003):

Cluster 1 "Stormfield Chain Wardens" (n=13):
- ACTUAL kit primary elements: earth=5 (38%), physical=3 (23%), fire=2 (15%), wind=1 (8%), lightning=1 (8%), holy=1 (8%)
- WAVE A REPORTED: earth=38%, lightning=31%, fire=15%, wind=8%, holy=8%, physical=0%
- Lightning over-report: 1 actual kit → 31% reported (4× over-representation)
- Physical drop: 3 actual kits → 0% reported (complete drop)

Cluster 2: lightning 9%→27%; physical 18%→0%
Cluster 3: lightning 11%→44%; physical 33%→0%

Pattern is consistent: physical disappears entirely; lightning inflates by approximately the magnitude of physical's actual share.

**Code-level root cause confirmed by jack-ryan read of `phase5_pm1_multimodal_clustering.py`:**

`_ELEMENT_MAP` (lines 310-313) contains 7 entries: fire, water, earth, wind, lightning, holy, shadow. **Physical is absent.**

When `encode_categorical(kit_data.get("element", "fire"), _ELEMENT_MAP)` is called for a STR/physical kit, "physical" is not in `_ELEMENT_MAP`. The function falls back to `default=0.5`.

On decode at element_distribution reconstruction (lines 678-685):
```python
best = min(_ELEMENT_MAP, key=lambda k: abs(_ELEMENT_MAP[k] - kv.element_encoded))
```
A kit with `element_encoded=0.5` (physical→default) finds nearest key = **lightning** (0.571, nearest to 0.5 over {wind=0.429, lightning=0.571}).

**Verified by jack-ryan Python calculation:**
- physical → encode → 0.5 (default) → decode → lightning

**The mechanism is confirmed:** every STR-physical kit votes "lightning" in the aggregator because physical is missing from `_ELEMENT_MAP` and the default 0.5 maps nearest to lightning. This is not a normalization failure or re-attribution via routing logic — it is an encode-decode round-trip loss for a missing element value.

**Physical is absent from `_ELEMENT_MAP` because the map was authored at 7 elements**, predating Amendment 7's addition of physical as a behavioral 8th element (STAT_ELEMENT_POOLS: STR→{physical}(1; degenerate) per Amendment 7 § Layer 1 E4c element coverage).

---

## § 2 — Disc #42a Q1-Q6 Framing Audit

### Q1 — Component existence

**Q1 asks:** Does the Phase 5 element_distribution aggregator exist as a real, in-scope architectural component?

**Finding:** YES — the aggregator IS a real component at lines 678-686 of `phase5_pm1_multimodal_clustering.py`. It exists, fires, and produces output consumed by Wave A LLM faction-naming prompts. It is NOT a phantom component (cf. Instance 6 #1 phantom-component surface).

**Q1 verdict: COMPONENT EXISTS AND IS WIRED.** This distinguishes Instance 6 #8 from Instance 6 #1 (phantom Wave B). The aggregator is real; its defect is a missing vocabulary entry, not a missing component.

---

### Q2 — Cheapest empirical refutation

**Q2 asks:** What is the cheapest empirical test that would refute the hypothesis OR confirm the disjoint?

**Finding:** The cheapest refutation was a Python one-liner (executed above):
```python
min(_ELEMENT_MAP, key=lambda k: abs(_ELEMENT_MAP[k] - 0.5))  # → "lightning"
```
This takes ~10 seconds. It directly confirms the encode-decode round-trip for physical→lightning.

Secondary confirmation (available in ~5 min): grep `_ELEMENT_MAP` in `phase5_pm1_multimodal_clustering.py` and count entries — 7 entries, no "physical" key.

**Q2 verdict: CHEAPEST REFUTATION IS TRIVIAL AND HAS BEEN EXECUTED.** Root cause confirmed at code-read level. Rocket Pattern-A parallel query will confirm implementation detail but is not required to establish the mechanism. The 10-second Python calculation is authoritative.

**Disc #42a Q2 discipline note:** this refutation was available BEFORE any Wave A LLM fires and before any faction-name generation. The discipline would have caught this at Phase 5 PM-1 entry gate if an element-map completeness check had been in the acceptance criteria.

---

### Q3 — Structural vs behavioral disjoint

**Q3 asks:** Is the bug structural (aggregator wired wrong) OR behavioral (aggregator wired per-spec but spec under-specifies physical)?

**Finding:** This is a **behavioral disjoint at the vocabulary/spec layer, not a wiring bug.**

- The aggregator IS wired correctly for the 7 elements that exist in `_ELEMENT_MAP`
- The aggregator is NOT wired for physical because physical was never added to `_ELEMENT_MAP`
- The underlying spec (`_ELEMENT_MAP` as authored) predates Amendment 7's elevation of physical to a behavioral element
- The aggregator behavior is deterministic and correct per its own vocab; the vocab was not updated when Amendment 7 expanded the element catalog

**Pattern classification:** This is the **Amendment 7a structural-vs-behavioral gap pattern** (Instance 6 #4) at the AGGREGATOR layer. Amendment 7 added physical as a behavioral element at the substrate-generation layer. The aggregator's vocabulary was not updated to match. Physical exists at the substrate-truth layer (13 STR kits); it does not exist at the aggregator's element vocabulary layer. The aggregator therefore cannot represent physical faithfully.

**Q3 verdict: BEHAVIORAL DISJOINT — spec gap (missing vocabulary entry) rather than wiring error.** The aggregator is wired correctly for what it knows. What it knows is incomplete post-Amendment 7.

---

### Q4 — Pipeline cardinality-mismatch / data flow source verification

**Q4 (amended per Disc #42a Q4 amendment from cascade-r3 Instance 6 #5):** Is downstream stage input_cardinality orders-of-magnitude different from upstream stage output count? AND — what is the aggregator reading?

**Finding:** This is NOT a cardinality-mismatch in the magnitude sense (unlike Instance 6 #5 where Phase 4=34 vs Phase 5=598). The element_distribution aggregator reads the correct scope: it reads all member kits in the cluster (n=13 for C1). Input cardinality matches the cluster population.

However, the Q4 "verify what the aggregator is reading" principle DOES apply:

- **What the aggregator reads:** per-kit `element_encoded` float, decoded to nearest key in `_ELEMENT_MAP`
- **What the substrate truth is:** per-kit `element` string (direct field on the kit data)
- **The disjoint:** aggregator routes through lossy encode-decode round-trip (float → nearest key) INSTEAD of reading the `element` string field directly

The aggregator could have been implemented as:
```python
elements = [kv.kit_id... kit_data.get("element") for kit in cluster]
```
Instead it reads `element_encoded` (float) and decodes. The encode-decode path is inherently lossy for values not in `_ELEMENT_MAP`.

**Q4 verdict: NOT a cardinality mismatch. IS a data-flow source precision loss.** The aggregator reads the right population but reads it through a lossy encoding. The Q4 "stop and verify data flow source explicitly" principle surfaces: the aggregator should read `element` (string) directly, not reconstruct it from `element_encoded` (float with incomplete vocabulary).

---

### Q5 — Cumulative pattern recognition

**Q5 asks:** Is this Instance 6 #8 in the existing cumulative pattern (calibration-aggregator-semantics-vs-architectural-intent family) OR a new pattern class?

**Finding:** This FITS the existing **structural-vs-behavioral variation gap** family (Instances #3, #4) extended to the aggregator layer. Specifically:

- Instance #3 (emit_skills_for_kit namespace-only): component exists and emits, but content was structurally identical where behavioral variance was assumed
- Instance #4 (chain_2 element metadata-only at skill emitter): element field set in metadata; emitter did not read it
- Instance #8 (element_distribution aggregator physical-as-lightning): element field correct at substrate layer; aggregator reads through lossy vocabulary that doesn't include physical

The shared structure: **a downstream consumer (emitter / aggregator) was not updated when an upstream substrate change (Amendment 7 adding physical as behavioral element) expanded the element catalog.** The substrate knows physical exists; the consumer does not.

This is the **same family** as Instances #3 and #4 — structural-vs-behavioral variation gap — manifesting at the AGGREGATOR-OVER-CLUSTER layer rather than the per-kit skill-emitter layer.

It is NOT the layer-isolation-vs-integration gap (Instance 6 #5 family) — the aggregator IS reading the right population and IS wired to its input. The gap is vocabulary incompleteness, not pipeline wire-up absence.

It is NOT a new pattern class. It IS a natural extension of the structural-vs-behavioral sub-case to the Phase 5 aggregator context.

**Q5 verdict: EXISTING FAMILY — structural-vs-behavioral variation gap, aggregator-layer instantiation. Instance 6 #8 is the same family as #3 and #4.**

---

### Q6 — Layer-isolation-vs-integration gap recognition

**Q6 asks:** Is this another instance of the "Layer-isolation-vs-integration gap" sub-case proposed at cascade-r3 Instance 6 #5? (Pipeline stages individually correct; inter-stage data flow source different than architecturally assumed.)

**Finding:** PARTIALLY. There is a layer-isolation element — the substrate layer (Amendment 7, physical correct at per-kit element field) and the aggregator layer (`_ELEMENT_MAP`, physical absent) are each correct in their own context. The "gap" is at the vocabulary alignment layer between them.

However, this is NOT the Q6 layer-isolation gap in its canonical form. The canonical Instance 6 #5 layer-isolation gap was: Phase 4 archive produces 34 kits; Phase 5 PM-1 reads 598 kits (Phase 3 output). The two stages were wired to different data sources. Here, the aggregator IS reading from the correct data source (cluster member kit vectors); it is reading a field (`element_encoded`) that carries incorrect content for physical kits because the vocabulary was never updated.

**The distinction:** Instance 6 #5 = wrong SOURCE. Instance 6 #8 = correct source, wrong VOCABULARY in the encoding layer.

**Q6 verdict: NOT the canonical layer-isolation-vs-integration gap. IS a vocabulary-staleness gap — the encoding vocabulary (`_ELEMENT_MAP`) was not updated when the substrate element catalog expanded (Amendment 7 physical addition). Distinct sub-case: "vocabulary-staleness-vs-substrate-expansion gap."**

---

### Q1-Q6 Summary Table

| Q | Finding | Severity |
|---|---|---|
| Q1 | Aggregator is a real, wired component (not phantom). | INFO |
| Q2 | Cheapest refutation trivially confirmed: physical → 0.5 → nearest → lightning (10-second Python). | INFO |
| Q3 | Behavioral disjoint: spec gap (missing vocabulary entry). Aggregator correct for what it knows. | WARN |
| Q4 | Not cardinality mismatch; IS data-flow source precision loss (encode-decode via lossy float). | WARN |
| Q5 | Existing family: structural-vs-behavioral variation gap, aggregator-layer instantiation. | WARN |
| Q6 | NOT canonical layer-isolation gap. IS a new sub-case: vocabulary-staleness-vs-substrate-expansion. | INFO |

**Overall Q1-Q6 verdict:** GENUINE SPEC GAP at vocabulary layer. Root cause is confirmed: `_ELEMENT_MAP` missing "physical" → default 0.5 → decode nearest → "lightning." Amendment 7 expanded the element catalog at the substrate-generation layer but did not propagate to the Phase 5 aggregator vocabulary. The fix is a one-line addition to `_ELEMENT_MAP`: `"physical": <ordinal_value>` + a re-fire of Wave A and Wave-S across 3 seasons.

---

## § 3 — Disposition

**Instance 6 #8 — same family (structural-vs-behavioral variation gap, aggregator-layer instantiation) — NOT a new pattern class.**

The family is established. The aggregator-layer manifestation is new (prior instances were at the skill-emitter layer); the structural pattern is identical: substrate change (Amendment 7 physical elevation) did not propagate to downstream consumer vocabulary.

---

## § 4 — Severity Classification for Cycle 14 v1 Close

**Severity: INFO**

Matt has explicitly designated this NOT v1 blocking (hive-mind-state line 5408: "NOT v1 blocking per Matt"). This finding records jack-ryan's concurrence:

**Arguments for INFO (not WARN or BLOCK):**

1. The fix is trivially scoped: add "physical" to `_ELEMENT_MAP` with an appropriate ordinal value (0.5 slot is logically defensible as the midpoint between wind=0.429 and lightning=0.571; alternately, the 8-element uniform-spacing ordinal = 7/7 = 1.0 at the end, or physically-motivated placement). The fix requires ~15 minutes of rocket implementation + Wave A / Wave-S re-fire across 3 seasons (~$0.20).

2. The player-facing output (faction names, Wave-S names) is CORRECTABLE via retroactive re-fire — no schema migration, no archived state invalidation.

3. The substrate at the kit level IS correct. Amendment 7a fixed per-kit element behavioral content at the skill emitter. The substrate-truth layer carries the correct physical distribution. The aggregator failure is isolated to the reporting / LLM-prompt input layer.

4. The Cycle 14 v1 close criterion does not specify "element_distribution accurately represents physical at aggregator layer" — it specifies shipped_worthy count and Gate-2 PASS. The shipped_worthy count (21/34 per Amendment 1 Gate-2) is not affected by the aggregator vocabulary bug.

5. Retroactive correction is sequenced correctly (hive-mind-state § routing: rocket fix + re-fire is Step 4-5, after this framing-audit; drax loadout refresh is Step 6 post-re-fire). Drax can proceed on current faction names and refresh post-re-fire per Matt directive.

**Verdict: INFO. Retroactive fix authorized, non-blocking.**

---

## § 5 — Composition with Designer-Writes-Substrate Principle

The Designer-Writes-Substrate principle (`canonical/story/2026-05-29-designer-writes-substrate-player-names-experience-principle.md`) states: "the engine's generative architecture must separate [designer-writes-substrate] and [player-names-experience] layers cleanly." Specifically:

> "The substrate is designer-curated BUT is itself substrate-led — informed by 89,839-row weapon library + thematic registry + community-validated mechanical architecture."

**Drift analysis:**

The substrate layer IS carrying correct physical distribution (Amendment 7 E4c element coverage operational; STR→{physical}(1) per STAT_ELEMENT_POOLS; 13 STR-physical kits in C1 verified). Designer-writes-substrate discipline is intact at the substrate-generation layer.

The aggregator (Phase 5 element_distribution computation) is at the **designer-writes-substrate → LLM-input handoff layer**. It is the first boundary where substrate-truth is summarized for LLM consumption. The drift at this boundary violates the substrate-led principle at the aggregator layer: physical kits ARE in the substrate; their substrate vote IS being cast; but the aggregator misreads physical votes as lightning votes before the LLM receives the substrate summary.

This is exactly the pattern the Designer-Writes-Substrate principle predicts as a failure mode: the substrate is authored correctly; the consumer (aggregator → LLM) misreads it. The LLM is doing its job correctly given biased input — as Matt's hive-mind-state note states: "LLM is doing its job correctly given biased input data; substrate-led intact at substrate layer; broken at Phase 5 aggregator."

**Composition framing:** Instance 6 #8 is the first confirmed case where Disc #41 (substrate-led discipline) drift occurs NOT at the substrate-generation layer but at the substrate-aggregation-to-LLM-input layer. The Designer-Writes-Substrate principle extends Disc #41 to this handoff boundary — the aggregator must faithfully represent what the substrate contains.

**This framing is load-bearing for the wave-close canonical-write candidate (§ 6 below).**

---

## § 6 — Wave-Close Canonical-Write Candidate Registration

### New sub-discipline candidate: "Substrate-honest aggregation at LLM-input boundaries"

**Sub-discipline name:** Vocabulary-staleness-vs-substrate-expansion gap (Disc #42a Q-extension candidate)

**Description:**

> When the substrate element catalog expands (e.g., Amendment 7 adding physical as behavioral element), ALL downstream consumers of element vocabulary must be audited for vocabulary completeness. Consumers include: encoding maps (`_ELEMENT_MAP`), aggregation functions, prompt-construction formatters, and any decode-then-report paths. A vocabulary-missing element defaults to a float value that nearest-neighbor decodes to an incorrect element. This is a class of spec-propagation failure distinct from structural-vs-behavioral (the consumer exists and fires correctly) and from layer-isolation (the consumer reads the right data source). The gap is: the consumer's vocabulary was not synchronized with the substrate expansion.

**Prevention prescription:**

At any Amendment that adds a new element to the canonical element catalog, add an acceptance criterion: "grep all `_ELEMENT_MAP` / `ELEMENT_MAP` / element-encoding tables in Phase 5 and verify all 8 canonical elements are present. If any element is absent, add it before Phase 5 fires."

**Disc #42a Q-extension candidate:** Q7 (or Q4 elaboration): "For any Amendment that expands a categorical vocabulary (element / attribute / lineage / geometry), verify all encoding maps in downstream consumers are updated to include the new value."

**Priority for wave-close write: P1** — this is load-bearing for future Amendment iterations that might add new elements (e.g., Cycle 15+ additions).

---

## § 7 — Remediation Scope Recommendation for KR → Gandalf Coordination

**Fix scope (minimal, correct):**

1. **Rocket:** Add "physical" to `_ELEMENT_MAP` in `phase5_pm1_multimodal_clustering.py`. Ordinal placement recommendation: uniform 8-element spacing = 0.125 intervals → physical = 1.0 (or at the end), alternatively 0.5 slot freed by ensuring physical does not collide with the default. The exact ordinal value matters less than: (a) physical is in the map, (b) its ordinal value does not collide with another element's ordinal. Suggested: retain 7-element map for existing elements (spacing preserved), add "physical": 0.875 as the 8th slot (equidistant between shadow=0.857 and 1.0). OR: renumber all 8 uniformly at 0.0, 0.143, 0.286, 0.429, 0.571, 0.714, 0.857, 1.0 with physical at 1.0. Rocket selects and smoke-tests; either approach is architecturally defensible.

2. **Rocket:** Retroactive re-fire of Phase 5 Wave A + Wave-S across seasons 001/002/003 (~$0.20 per Matt estimate).

3. **Gandalf:** Post-re-fire, verify new faction names are free of phantom-lightning theming. Drax data refresh follows.

4. **Jack-ryan wave-close:** Vocabulary-staleness sub-discipline candidate (§ 6) added to wave-close canonical-write queue. Priority P1.

**NOT required for this fix:**
- Phase 2-4 re-fire (substrate is correct; only aggregator vocabulary is wrong)
- Phase 7 re-fire (shipped_worthy decisions were on mechanically correct kits; Wave B per-kit names are unaffected by faction-level element distribution)
- Gate-2 formal review of the one-line fix (trivial fix; Matt may elect INFO-level verification; not a Pattern E review)

---

## § 8 — References

**Code reviewed:**
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/phase5_pm1_multimodal_clustering.py` lines 310-313 (`_ELEMENT_MAP` — physical absent), lines 678-686 (element_distribution aggregation), lines 380-383 (encoding call with fallback default=0.5)

**Design docs reviewed:**
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/cycle-14-hive-mind-state.md` lines 5377-5410 (Matt surface + routing + cumulative count)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/qa/pending/2026-05-29-jack-ryan-cascade-r3-instance-6-5-framing-audit-canonical-record.md` (cumulative Instance 6 record; layer-isolation sub-case origin)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/qa/pending/2026-05-29-jack-ryan-cascade-r4-amendment-1-wanderer-architecture-gate-2-pattern-e-review.md` (Instance 6 #7 CLOSED; cumulative count at 7)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-05-29-amendment-7a-per-chain-element-wiring-fix-spec.md` (same family of bug at skill-emitter layer)
- `/Users/admin/Games/reincarnated-collaboration/canonical/story/2026-05-29-designer-writes-substrate-player-names-experience-principle.md` (substrate-led composition)
- `/Users/admin/Games/reincarnated-collaboration/canonical/47-damage-scaling-architecture-2026-05-27.md` (STR→physical scaling path; Variant C physical kits)
- `/Users/admin/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` Disc #42a (Q4/Q5/Q6 subaudit) + Disc #41 (substrate-led)

**Empirical verification:**
- jack-ryan Python calculation: `_ELEMENT_MAP` missing "physical" → default 0.5 → nearest decode → "lightning" (0.571). Confirmed in ~10 seconds.
