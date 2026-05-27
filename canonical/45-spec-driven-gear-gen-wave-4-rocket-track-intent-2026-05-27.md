# 45 — Spec-Driven Gear Gen Wave 4 Rocket Track Intent (Cycle 13 — 2026-05-27)

> **STATUS:** CURRENT (load-bearing as of 2026-05-27) — Wave 4 spec-driven gear gen design INTENT canonical (rocket track) for Cycle 13 multi-T4 architecture cycle; see `canonical/00-ground-state.md`

**Date:** 2026-05-27
**Author:** gandalf (story-and-design steward)
**Status:** v1 canonical lock — Wave 4 spec-driven gear gen design intent (rocket track ONLY; gamora SC-7 T4 Phase 4 sim cycling Track B is separate seam firing concurrently); per-rarity gear instance generation algorithm across all 10 rarity tiers per partition design (doc 42) + T4-attunement annotation per content-compositional model (doc 40 D33+D38+D51 amended) + triggered-passive added-skill generation per D55 high-probability rule + modifier-surface expansion at legendary per D56 + capability-toolkit-legendary-exclusive enforcement per Wave 1 SC-4 Gate 5 LOCKED HYBRID + 4-piece set bonus structure (Set T1-T2 endgame-only per closeout § 3.4) + sub-wave structure W4R.0-W4R.7 (8 sub-waves; mirrors Wave 1/2/3 implementation-atomic pattern) + Wave 4 implementation guidance for rocket + composition with gamora SC-7 Track B
**Authority:** Matt 2026-05-27 verbatim — "Resume Wave 0 → Wave 1 dispatch sequencing per ratified framing brief § 4.1 autonomous scope. No further Matt-creative-ratification gates on Cycle 13 progression." + jack-ryan Wave 3 Gate-2 PASS verdict on rocket Wave 3 implementation (commit `99ec777` / engine `2e8bc33`) UNBLOCKS Wave 4 dispatch authoring + Wave 3 CLOSED + WARN-pattern PRESERVED milestone (full closure maintained through Wave 3 — Wave 4 expectation: 100% accurate post-script empirical count assertions preserved)
**Companion docs:**
- `canonical/00-ground-state.md` — ground-state oracle (this doc registers as new CURRENT entry)
- `canonical/38-downstream-delivery-strategy-2026-05-23.md` — D1-D10 delivery strategy keystone
- `canonical/39-qd-engine-end-to-end-workflow-2026-05-24.md` — engine workflow Phase 2d spec-driven gear gen is Wave 4's home
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` — Cycle 13 architectural foundation (D1-D86 + 2026-05-27 amendments); § 3 spec-driven gear gen + § 3.5 tier structure + § 3.6 per-rarity × per-slot grid + D33/D38/D51 (content-compositional attunement) + D48-D57 (legendary 4-tier + unique 4-tier + set 2-tier + capability toolkit) + D55 (high-probability triggered-passive on weapons) + D56 (modifier-surface expansion legendary-exclusive)
- `canonical/41-progression-framework-2026-05-27.md` — L50 hybrid + cell × node × cohort context (drop-pool restriction maps gear tier to player level band)
- `canonical/42-stat-sheet-modifier-partition-intent-2026-05-27.md` — Wave 1 partition substrate (gear gen CONSUMES per-slot affinity matrix + per-rarity grid + tier-restricted modifier surface + 6 principles)
- `canonical/43-t4-algorithm-wave-2-intent-2026-05-27.md` — Wave 2 T4 algorithm substrate (3-category taxonomy + 7-strategy registry + parallel-chain reach + DUAL_ELEMENT_ADDITION); gear's T4-attunement annotation refers into this
- `canonical/44-t4-algorithm-wave-3-phase-3-intent-2026-05-27.md` — Wave 3 T4 algorithm Phase 3 substrate (scope dimension); gear's T4-attunement annotation may carry scope-preference hint
- `canonical/02-roadmap.md` — engine build visual-flow progress tracker
- `agentic_orchestration/gandalf/notes/2026-05-27-cycle-13-pre-launch-design-session-closeout.md` — Matt + gandalf Pattern-B session closeout § 3 (Block B gear architecture substantive content; § 3.2 per-rarity grid; § 3.3 affinity matrix + 6 principles; § 3.4 content-compositional attunement + 4-piece set structure)
- `agentic_orchestration/qa/findings/2026-05-27-cycle-13-wave-3-gate-2-rocket-implementation.md` — Wave 3 Gate-2 PASS + I5 drax cross-seam touch flag (`scope_projection_data` dict on T4CandidateV2 → Wave 4+ drax consumption)
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` — 8-axis BC operational truth (cross-cohesion validation coordinate system; W4R.6 extends Wave 1/2/3 cross-cohesion pattern to gear gen)
- `canonical/story/off-hand-items-2026-05-24.md` — off-hand items operational definition (6 categories; informs per-slot family routing in W4R.1)

---

## 0. TL;DR

Wave 4 spec-driven gear gen design intent (rocket track) for Cycle 13 multi-T4 architecture cycle. Operationalizes the **spec-driven gear gen architectural pattern** per doc 40 § 3 D7 — gear generation uses the same scored-candidate strategy registry pattern as the T4 algorithm; kit+T4 produces a gear specification; strategies produce candidates; simulation validates. Specs the **per-rarity gear instance generation algorithm across all 10 rarity tiers** (Common / Uncommon / Rare / Epic / Legendary T0 / Legendary T0.5 / Legendary T1 / Legendary T2 / Set T1 / Set T2 per `PartitionRarity` enum landed in Wave 1) — per-tier modifier count + categories rollable + added-skill content gate + T4-attunement annotation gate per doc 42 § 3 per-rarity grid. Specs the **T4-attunement annotation per content-compositional model** (per closeout § 3.4 + doc 40 D33+D38+D51 amended) — annotation is METADATA recording generation-time alignment intent (chain + T4 target) at Tier-1+2 legendary + all sets; gear content IS the attunement; magnitude IS content quality; algorithm consumes annotation for drop pool restriction (D50) + spirit-guide projection (D34) + algorithm-side optimization. Annotation may carry **scope-preference hint** per Wave 3 doc 44 (character-wide / chain-wide-OWN / chain-wide-PARALLEL T4 target). Specs the **triggered-passive added-skill generation per D55 high-probability rule** — per-slot-family generation pattern (weapons spawn geometric AOE on hit / thorny on hit / shrapnel burst on physical hit; armor on-being-hit triggers; accessories general passives + rare true-actives on weapons only) with probability calibration STARTING ESTIMATES anchored per Verdict-B.4-pattern (gamora SC-7 iterates post-Wave-4-baseline per Discipline #18.2). Specs the **modifier-surface expansion at legendary per D56** — legendaries unlock NEW stat types Epic cannot roll (per doc 42 § 4.2 Legendary+ exclusive types: capability toolkit categories + added-skill triggered-passive + on-block/on-dodge triggers + T4-attunement metadata). Locks the **capability-toolkit-legendary-exclusive enforcement** per Wave 1 doc 42 § 7 SC-4 Gate 5 LOCKED HYBRID — multiplicative / mechanic-adjusting / spatial-adjusting / axis-adjusting / added-skill categories at legendary T0-T2 only (Epic+ rarity gate; cross-ARPG consensus all 4 reference ARPGs). Specs the **4-piece set bonus structure (Set T1-T2 endgame-only)** per closeout § 3.4 — 2-piece minor always-active bonus + 4-piece full T4-attuned bonus; sets are endgame-exclusive (no Tier 0 / Tier 0.5 sets). Provides **sub-wave structure W4R.0-W4R.7** (8 sub-waves; mirrors Wave 1 W1.0-W1.8 + Wave 2 W2.0-W2.9 + Wave 3 W3.0-W3.5 implementation-atomic pattern; scope between Wave 1 and Wave 2). Provides **Wave 4 implementation guidance for rocket** including substrate consumption from Wave 1 partition (PartitionGearInstance schema + AffinityMatrix + TIER_1_2_RARITIES + CapabilityModifier + T4AttunementAnnotation already operational) + Wave 2+3 T4 algorithm (T4CandidateV2 with `t4_scope` field + `scope_projection_data` dict W3.5 carryover) + drax cross-seam touch flag for `scope_projection_data` consumption + maintain WARN-pattern PRESERVED status. Composes with gamora SC-7 Track B (T4 Phase 4 sim cycling) — gear gen output is sim consumption input; doc 45 flags data-field implications for SC-7 cross-reference. § 12 Discipline #23 framing-audit INCLUDED FROM START per doc 44 § 11 precedent (avoids Wave 1 W1 amendment pattern). Wave 4 close criterion (rocket track) = jack-ryan Gate-2 PASS on rocket Wave 4 implementation against this intent + WARN-pattern PRESERVED status maintained + coordinated with gamora SC-7 Track B close. Disciplines #1 + #1.2 + #11 + #18 + #18.2 + #23 + #26 + #27 + #29 + #30 + #31 + #32 compose throughout.

---

## 1. Architectural foundation cross-references

This doc operationalizes the Wave 4 spec-driven gear gen design intent (rocket track) grounded in the locked architectural foundation + Wave 1+2+3 substrate.

| Foundation doc | What it provides | Where this doc operationalizes |
|---|---|---|
| **Doc 38** (D1-D10 delivery strategy) | Variant C engine-vs-game; isekai provisional; ~30-day seasonal | Composes with § 10 |
| **Doc 39** (QD-engine workflow Architecture B) | Phase 2d spec-driven gear gen substrate-bound | Wave 4 IS the operationalization of Phase 2d for rocket implementation; gear instances consume the partition substrate landed at Phase 2c |
| **Doc 40** (Cycle 13 architectural foundation, post-amendments) | § 3 spec-driven gear gen D7 (scored-candidate strategy registry mirroring T4 algorithm); § 3.3 capability toolkit (multiplicative + mechanic-adjusting + spatial-adjusting + axis-adjusting + added-skill); § 3.4 modifier-surface expansion D56 (legendary-exclusive new stat types); § 3.5 tier structure D48-D57 (legendary 4-tier + unique 4-tier as sub-category + set 2-tier endgame-only); § 3.6 per-rarity × per-slot grid (Wave 1 substrate); D33+D38+D51 amended (content-compositional attunement); D54-D55 (capability toolkit legendary-exclusive + triggered-passive high-probability on weapons + rare true-active weapon-only); D80 (gap-filling discipline) | This doc IS the operationalization of doc 40 § 3 + D-decision content for Wave 4 rocket implementation |
| **Doc 41** (L50 hybrid progression framework) | 4 progression nodes (L1-15 Early / L15-30 Mid / L30-45 Endgame-start / L45-50+ Endgame); endgame post-cap progression via gear + chain investment + T4 unlock + set completion | Drop pool restriction per D50 maps gear tier to player level band; Set T1-T2 endgame-exclusive aligns with L45-50+ endgame node |
| **Doc 42** (Wave 1 partition intent) | 9-category × 11-slot affinity matrix; per-rarity grid; tier-restricted modifier surface enumeration; capability toolkit legendary-exclusive; 6 principles; sample modifier enumerations per category per slot family; `PartitionGearInstance` schema landed | Wave 4 spec-driven gear gen CONSUMES Wave 1 partition substrate: gear gen algorithm samples from partition pool per slot per rarity per affinity weight (principle 1); enforces tier-restriction (principle 2); gates resource modifiers per class resource model (principle 3); applies gap-filling (principle 4); enforces no-skill-modifier (principle 5); cross-cohesion validates (principle 6) |
| **Doc 43** (Wave 2 T4 algorithm intent + Wave 2 implementation) | 3-category taxonomy + 7-strategy registry (6 + DUAL_ELEMENT_ADDITION); parallel-chain reach; compositional synergy scan; Option F retry; one-T4-active gating; variable 3-or-4 chain architecture; T4CandidateV2 schema | Wave 4 gear gen reads T4 algorithm output: `T4CandidateV2` instances carry the T4 identity that gear's T4-attunement annotation aligns to; per-class chain count informs which chain attunement values are valid |
| **Doc 44** (Wave 3 T4 algorithm Phase 3 intent + Wave 3 implementation) | scope dimension (CHARACTER_WIDE / CHAIN_WIDE_OWN / CHAIN_WIDE_PARALLEL); `T4Scope` enum; `t4_scope` field on T4CandidateV2; `scope_projection_data` dict W3.5 carryover for drax cross-seam consumption | Wave 4 gear gen MAY carry scope-preference hint in T4-attunement annotation (e.g., a Tier-2 legendary aligned to a character-wide-favoring T4 hints that scope at annotation time; algorithm uses annotation for spirit-guide projection); drax cross-seam consumer of `scope_projection_data` is informed by Wave 4 attunement choices |
| **Closeout doc 2026-05-27** | § 3.1 9-category char sheet surface; § 3.2 per-rarity × per-slot grid; § 3.3 affinity matrix + 6 principles; § 3.4 content-compositional attunement + 4-piece set structure (2pc minor always-active + 4pc full T4-attuned); § 3.5 spirit-guide projection synergy-score | Source authority for all locks in this doc |
| **Wave 3 Gate-2 finding 2026-05-27** | Wave 3 PASS verdict (engine commit `2e8bc33` + collab `fd2d7f6`); WARN-pattern PRESERVED milestone (full closure maintained through Wave 3); rocket implementation discipline established (146/146 tests PASS; 10/13 count assertions empirically verified); I5 drax cross-seam touch flag (`scope_projection_data` dict on T4CandidateV2) | Wave 4 inherits the discipline: 100% accurate post-script empirical count assertions; module-load `assert len(X) == N` pattern; no count drift; drax cross-seam touch flag carries forward (Wave 4 may surface drax consumption surface) |
| **8-axis BC lock** | 68,040 cells; operational measurement coordinate system | Wave 4 cross-cohesion validation (W4R.6) extends Wave 1/2/3 cross-cohesion pattern: gear gen output across 4 cohort archetypes (DPS-min-maxer / Balanced / Defensive / Hybrid) × per-rarity × per-slot grid validates build-diversity preservation per principle 6 |

**Authority basis:** Matt 2026-05-27 verbatim "Resume Wave 0 → Wave 1 dispatch sequencing per ratified framing brief § 4.1 autonomous scope" + jack-ryan Wave 3 Gate-2 PASS verdict (commit `99ec777` / engine `2e8bc33`) UNBLOCKS Wave 4 dispatch authoring + Wave 3 CLOSED + WARN-pattern PRESERVED milestone (full closure maintained through Wave 3).

---

## 2. Spec-driven gear gen operationalization (per doc 40 § 3 D7)

Per doc 40 § 3.1 + D7. The spec-driven pattern mirrors the T4 algorithm architecture but operates at the gear-instance generation layer.

### 2.1 Architectural pattern

> **Gear generation uses the same scored-candidate strategy registry pattern as the T4 algorithm.** A kit-plus-T4-selection produces a gear specification; the strategy registry produces candidate gear pieces that fit the spec; simulation validates the result against the kit's endgame power target.

The pattern composes:

| Layer | Input | Algorithm | Output |
|---|---|---|---|
| **Kit composition** (Phase 2a) | Class + cell-type + BC-coordinate identity | Kit composition algorithm (per doc 39 Architecture B) | Kit instance with chains + class resource model + element profile |
| **T4 algorithm** (Phase 2b — Wave 2+3) | Kit instance | T4 candidate generation + scoring + synergy scan + Option F retry | `T4CandidateV2` per chain × per class × per scope (Wave 3) |
| **Spec-driven gear gen** (Phase 2d — Wave 4 THIS DOC) | Kit instance + selected T4 candidates + partition substrate (Wave 1) | Per-rarity gear instance generation algorithm (this doc) | `PartitionGearInstance` per slot × per rarity × per T4-attunement target |
| **Sim cycling** (Phase 3 — Wave 5 + SC-7 Track B) | All Phase 2 output | Gauntlet sim validation across cohort archetypes × cells × encounters | Per-cohort balance band validation + Pattern 9+10 detection |

**Composition rule:** Wave 4 gear gen is the **last Phase 2 step before sim cycling fires** — it consumes Wave 1+2+3 substrate and produces the final input surface for SC-7 Track B sim cycling.

### 2.2 Spec-driven means substrate-bound

Per doc 39 Architecture B substrate-bound at Phase 2: gear gen does NOT synthesize modifier types from scratch. It samples from the partition substrate (Wave 1 partition pool) per slot per rarity per affinity tier. The "spec" is the kit+T4 context; the "driven" is the substrate-bound sampling per affinity matrix.

**What this is NOT:** gear gen is NOT LLM-prompted to generate modifier types. The partition pool is the ground-truth modifier surface; gear gen samples from it. LLM is permitted for player-facing NAMING of legendary instances per § 5.5 (D7 AI-tell line preserved).

### 2.3 Scored-candidate at gear-instance layer

For each gear slot to be generated, the algorithm:

1. Determines slot + rarity + (legendary-specific: chain + T4 target + scope hint) per drop context
2. Samples N candidate modifier rolls from partition pool per per-slot affinity matrix
3. Scores each candidate against fit criteria: (a) tier-restriction enforcement; (b) resource-model gating; (c) gap-filling against accumulated kit stat sheet (D80); (d) T4-attunement coherence (legendary T1-T2 + all sets); (e) capability-toolkit-as-chain-effect-composer surface (legendary only)
4. Selects highest-scoring candidate; ties broken by gap-fill preference per D80
5. Emits `PartitionGearInstance` with full modifier roll + (if legendary) capability toolkit + (if Tier-1+2 / all sets) T4-attunement annotation

Scoring is **arithmetic + pattern library** (no LLM raw-reasoning per D7); gap-fill function + tier-restriction enforcement + affinity-weighted sampling are all algorithmic.

---

## 3. Per-rarity gear instance generation (10 rarity tiers)

Per doc 40 § 3.6 + closeout § 3.2 + Wave 1 partition substrate doc 42 § 3 per-rarity grid + `PartitionRarity` enum landed at `partition_schema.py:67-77` (10 values: COMMON / UNCOMMON / RARE / EPIC / LEGENDARY_T0 / LEGENDARY_T0_5 / LEGENDARY_T1 / LEGENDARY_T2 / SET_T1 / SET_T2).

### 3.1 Per-rarity generation specification

| Rarity | Modifier count | Categories rollable | Capability toolkit? | Added-skill content? | T4-attunement annotation? | Set bonus rank? |
|---|---|---|---|---|---|---|
| **COMMON** | 1-2 | 1-3 (Damage / Defense / Resource ONLY) | No | No | No | N/A |
| **UNCOMMON** | 2-3 | 1-6 (+ Crit + Speed + Res-Pen) | No | No | No | N/A |
| **RARE** | 3-4 | 1-6 + 9 (+ Util/Meta) | No | No | No | N/A |
| **EPIC** | 4-5 | 1-9 (full 9-category surface) | No | No | No | N/A |
| **LEGENDARY_T0** (early-game) | 4-5 + Epic-exclusion modifiers (D56) | 1-9 + legendary-exclusive modifier surface | Yes (one capability slot) | Yes — chain-aligned (triggered-passive per D55) | No | N/A |
| **LEGENDARY_T0_5** (mid-game) | 5-6 (higher density) | 1-9 + legendary-exclusive | Yes (one capability slot) | Yes — chain-aligned | No | N/A |
| **LEGENDARY_T1** (endgame-entry) | 5-7 (higher density + T4 annotation) | 1-9 + legendary-exclusive + T4-attunement annotation (metadata) | Yes (one capability slot; possible dual at Tier 2) | Yes — **chain + T4-attuned** | **Yes (1 attunement)** | N/A |
| **LEGENDARY_T2** (endgame) | 6-8 (highest density + T4 annotation) | Same + dual-attunement variants + rare true-active weapon-only | Yes (one + possible dual at ~rare rate per `DUAL_CAPABILITY_PROBABILITY`) | Yes — chain + T4-attuned + **rare true-active** (weapon-only per D55; ~1.5% probability) | **Yes (1-2 attunements)** | N/A |
| **SET_T1** (endgame-exclusive) | Per legendary T1 + set-bonus rank | Same as legendary T1 + set-cohesive | Yes (per legendary T1) | Yes — chain + T4-attuned + set-cohesive | **Yes (set-level attunement per D35)** | **Yes (rank-1 set bonus)** |
| **SET_T2** (endgame-exclusive) | Per legendary T2 + set-bonus rank | Same as legendary T2 + set-cohesive | Yes (per legendary T2) | Yes — chain + T4-attuned + set-cohesive + rare true-active | **Yes (set-level + per-piece attunement)** | **Yes (rank-2 set bonus)** |

**10-tier completeness verification:** the 10 entries above correspond 1:1 to the `PartitionRarity` enum landed at `partition_schema.py:67-77`. Module-load `assert len(PartitionRarity) == 10` per Wave 1 discipline (verified in Wave 1 partition implementation). Per-rarity grid is complete.

### 3.2 Unique gear sub-category routing (per D49 + D53)

Per doc 40 D49 + D53: uniques are 4-tier (T0/T0.5/T1/T2) sub-category of legendary with signature-mod patterns. The 10-tier `PartitionRarity` enum does NOT add separate unique rarities — uniques are a **metadata flag** on legendary rarity instances. Recommended encoding: `PartitionGearInstance.is_unique: bool` field added in Wave 4 (or extension of existing schema; rocket adjusts per implementation experience).

**Unique generation pattern (Wave 4 spec):**

- Unique drop pool is a SUB-POOL of legendary at matching tier (T0 / T0.5 / T1 / T2)
- Each unique entry in the pool has fixed signature-mod patterns (specific stat ranges + specific capability toolkit selection + named-template identity)
- Unique generation picks from pool rather than rolling from partition (constraint: unique instances are pre-defined; the algorithm picks WHICH unique to drop, not WHAT modifiers it has)
- Per-tier T4-attunement annotation rule preserved: T0/T0.5 unique = chain-alignment only; T1/T2 unique = chain + T4-attuned

**Cross-seam touch flag:** unique pool definition is a content authoring surface (gandalf + design); Wave 4 implementation provides the GENERATION-TIME ROUTING; the POOL CONTENT itself is downstream authoring work (Cycle 14+). Wave 4 ships with placeholder unique pool (~5-10 placeholder uniques per tier for sim validation) per closeout § 8 deferred-commitments pattern.

### 3.3 Density gradient discipline (per closeout § 3.2 + Pattern R1)

Per closeout § 3.2: higher tier = higher density of modifiers per gear instance. The modifier count column in § 3.1 enforces this — Common 1-2 → Uncommon 2-3 → Rare 3-4 → Epic 4-5 → Legendary T0 4-5 → Legendary T0.5 5-6 → Legendary T1 5-7 → Legendary T2 6-8 → Set T1-T2 per legendary T1-T2 + set-bonus rank.

**Density IS part of the rarity-power escalation pattern** (per Pattern R1 quantity escalation per SC-4 § S2 — see doc 42 cross-reference). Magnitude escalation per modifier is SEPARATE from density escalation; both compose into "rarity IS power escalation" per D8.

---

## 4. T4-attunement annotation per content-compositional model

Per closeout § 3.4 + doc 40 D33+D38+D51 amended. Content-compositional model SUPERSEDES binary/graduated framing.

### 4.1 Annotation mechanics

> **The annotation is METADATA recording generation-time alignment intent. Gear content IS the attunement; magnitude IS content quality.**

- Annotation field exists on `PartitionGearInstance` per `T4AttunementAnnotation` dataclass landed at `partition_schema.py:479` (Wave 1)
- Annotation populated at generation time per algorithm-side T4 target selection (chain + T4 candidate selected from kit's available T4 candidate pool)
- Annotation does NOT toggle anything ON/OFF at consumption time — gear passives always fire; synergy value varies by build
- Annotation drives downstream consumption surfaces (per § 4.4)

### 4.2 Which gear instances carry annotation

Per doc 42 § 3 + doc 40 D33+D51 amended:

| Rarity | Annotation? | Annotation content |
|---|---|---|
| COMMON / UNCOMMON / RARE / EPIC | No | N/A |
| LEGENDARY_T0 / LEGENDARY_T0_5 | No (chain-alignment annotation only) | Chain identity only; no T4 target |
| LEGENDARY_T1 | Yes — 1 attunement | Chain + T4 candidate target |
| LEGENDARY_T2 | Yes — 1-2 attunements | Chain + T4 candidate target; may carry dual-attunement (composes with two T4 targets across parallel chains per Wave 2 W2.3 parallel-chain reach) |
| SET_T1 / SET_T2 | Yes — set-level attunement per D35 | Chain + T4 candidate target; coherent across 4 pieces of set |

### 4.3 Scope-preference hint per Wave 3 (NEW for Wave 4)

Per Wave 3 doc 44 scope dimension: T4 candidates now carry a `t4_scope` field (CHARACTER_WIDE / CHAIN_WIDE_OWN / CHAIN_WIDE_PARALLEL). The T4-attunement annotation may carry a **scope-preference hint** indicating which scope the gear instance was generated to favor.

**Algorithm-side:** when gear generation produces a Tier-1+2 legendary or set with T4-attunement annotation, it selects the T4 target from the kit's T4 candidate pool. That candidate has a `t4_scope`. The annotation records the scope as part of the alignment metadata (proposed field: `T4AttunementAnnotation.scope_preference: T4Scope | None`).

**Use cases for scope hint:**

| Consumer | How scope hint is used |
|---|---|
| Drop pool restriction (D50) | Gear hinted at character-wide T4 may have slightly different drop weights vs chain-wide-OWN gear (gamora SC-7 calibrates post-baseline per #18.2) |
| Spirit-guide projection (D34 + closeout § 3.5) | Spirit guide surfaces per-scope projection messaging consistent with gear's annotated scope hint |
| Algorithm-side gap-fill (D80) | Gap-fill recognizes scope-aligned gear as completing a scope-aligned build kit |
| drax cross-seam touch (Wave 3 I5) | `scope_projection_data` dict on T4CandidateV2 is consumed by drax for player-facing surfaces; gear's scope-preference annotation aligns with that data surface |

**Discipline:** scope hint is OPTIONAL on the annotation. Gear generation MAY emit annotations without scope hint (fallback when no clear scope alignment; gamora SC-7 iterates post-Wave-4-baseline on default-scope-hint policy per #18.2).

### 4.4 Annotation consumption surfaces

Per doc 40 D34 + D50 + closeout § 3.5:

1. **Drop pool restriction (D50):** algorithm uses annotation to restrict drop pool — player at endgame content sees all 4 tiers + Set; player at early game sees only Tier 0 (no annotation needed at early game)
2. **Spirit-guide projection (D34):** spirit guide surfaces synergy-score projection per closeout § 3.5: "Playing T4-A: projected KPM 75. Switching to T4-B: projected KPM 62. Net synergy score: T4-A composes 23% better with this gear AND amplifies wind chain by +18%." Annotation is the input to the projection arithmetic.
3. **Algorithm-side optimization:** gap-fill (D80) + cross-cohesion validation (principle 6) consume annotation to validate build-diversity preservation across T4 targets
4. **Spirit-guide-pacing discipline (#28 Matt 2026-05-26 candidate; doc 40 § 5):** annotation drives offer-triggering mechanism — gear with strong T4-A alignment surfacing prompts spirit-guide T4-swap offer

### 4.5 Composition with Disciplines #27 + #31 + #32

- **#27 dual-effect capstone:** Wave 4 annotation refers to T4 candidates per Wave 2+3 substrate; #27 is preserved upstream at T4 algorithm layer (every T4 has Category A + Category B/C). Gear's annotation refers to the T4 unit; #27 is not at gear layer
- **#31 dual-effect separability:** preserved upstream at T4 algorithm layer; not at gear layer
- **#32 first-do-no-harm:** Wave 4 gear gen MUST validate that gear instances do NOT compose with their annotated T4 to produce Pattern 9 (passive screen-clear) OR Pattern 10 (DoT-stack degenerate) effective rates. Cross-cohesion validation (W4R.6) extends Wave 2+3 Pattern 9+10 detection at GEAR-EFFECTIVE rate (gear modifier × T4 multiplier vs Pattern 9+10 threshold)

---

## 5. Triggered-passive added skills on legendaries (per D55 high-probability)

Per doc 40 D55 + § 3.3 capability toolkit + closeout § 3.4. The dominant added-skill flavor on legendaries is **triggered-passive** (auto-trigger from gameplay actions; no player budget impact; Diablo 2 "10% chance to cast tornado on hit" lineage).

### 5.1 Per-slot-family triggered-passive generation patterns

Per doc 40 § 3.3 + D55 + closeout § 3.4:

| Slot family | Dominant triggered-passive patterns (5-10 examples per family; rocket extends per implementation) |
|---|---|
| **Weapons (main-hand + dual-wield-secondary)** | (1) spawns geometric AOE on hit (tornado / shrapnel burst / fire nova); (2) thorny on hit (spike retaliation); (3) chain lightning on crit; (4) element-projectile-spawn on element-cast (e.g., fire skill spawns fireball projectile); (5) on-kill explosion; (6) freeze-on-crit AOE; (7) life-steal on hit (% of damage as health); (8) curse-on-hit (debuff target); (9) charge-build on hit (resource gain); (10) summon-temporary-minion on element-cast |
| **Armor (head / chest / hands / feet / legs)** | (1) on-being-hit reflection (small AOE retaliation); (2) on-being-hit stun (brief CC); (3) on-being-hit thorns (% of incoming damage as fire); (4) on-low-HP shield (temporary defensive buff); (5) on-block counter (auto-strike); (6) on-dodge speed-boost (movement buff); (7) on-being-CC'd cleanse (status removal); (8) on-element-resist-hit element-buff (e.g., resisting fire grants fire damage buff); (9) on-near-enemy area-buff (proximity defensive); (10) on-kill near-enemies fear (AOE CC) |
| **Accessories (amulet / ring × 2 / belt)** | (1) general passive: % damage bonus per nearby enemy; (2) general passive: HP regen per second; (3) general passive: resource regen on kill; (4) on-cast trigger (any spell): minor element-mark on target; (5) on-skill-use minor cooldown reduction; (6) **RARE true-active (weapon-only per D55) — does NOT appear on accessories**; (7) on-trigger gold-pickup boost; (8) on-trigger experience boost; (9) on-trigger temporary mini-buff; (10) on-trigger meta-progression token |

**Rocket implementation MUST distinguish weapon-only triggered patterns from accessory-allowed patterns** per slot routing in `PartitionGearInstance` generation.

### 5.2 Probability calibration starting anchors (per Verdict-B.4-pattern)

Per Verdict-B.4-pattern: magnitude bands ANCHORED with starting estimates; gamora SC-7 iterates post-Wave-4-baseline per Discipline #18.2 (consultation at extension hotspots fires AFTER baseline empirical data, not before).

**Per-slot triggered-passive probability anchors (Wave 4 ships with these; gamora SC-7 iterates):**

| Slot family | Triggered-passive presence probability (per legendary instance) | Trigger fire rate per gameplay event |
|---|---|---|
| Weapons | **~90% probability** of triggered-passive on legendary T0 / T0.5; **~100% probability** at T1 / T2 (always present) | Fire rate per event: ~10-25% chance (e.g., "10% chance to spawn tornado on hit") at T0; ~25-40% at T1/T2 |
| Armor | **~70% probability** at T0 / T0.5; **~90% probability** at T1 / T2 | Fire rate per event: ~15-30% chance |
| Accessories | **~50% probability** at T0 / T0.5; **~75% probability** at T1 / T2 | Fire rate per event: variable; many are passive-always (e.g., +% damage per nearby enemy fires whenever near enemy) |

### 5.3 Rare true-active on weapons (per D55)

Per doc 40 D55 + § 3.3: TRUE ACTIVE added skills are EXTREMELY RARE and weapons-only. Probability anchors per `TRUE_ACTIVE_PROBABILITY` (Wave 1 schema partition_schema.py:390):

| Rarity | True-active probability per legendary weapon |
|---|---|
| LEGENDARY_T0 / LEGENDARY_T0_5 | 0% (true-active is Tier-1+2 exclusive per doc 42 § 4.3) |
| LEGENDARY_T1 | ~0.5% per legendary weapon drop |
| LEGENDARY_T2 | ~1.5% per legendary weapon drop |
| SET_T1 / SET_T2 | ~per-tier (set true-active is rarest endgame chase) |

True-actives are **additive to base skill budget per D57** (do NOT consume the flat-8 active skill slot allocation). When they roll, they ADD a slot beyond the 8-skill base budget.

### 5.4 Composition with capability toolkit (D54)

Per doc 40 § 3.3 + D54: capability toolkit is the **broader category** containing added-skill triggered-passive + added-skill true-active + multiplicative + mechanic-adjusting + spatial-adjusting + axis-adjusting. Per § 7 below: capability toolkit is LEGENDARY-EXCLUSIVE (all tiers; T0-T2 + sets).

**Per-legendary instance:** algorithm selects ONE capability toolkit slot per legendary at T0/T0.5/T1 (per `can_roll_capability_toolkit()` Wave 1 partition_schema.py:384). At T2: `DUAL_CAPABILITY_PROBABILITY` (partition_schema.py:400) may select 2 capability slots (rare even at T2).

**Triggered-passive added-skill is ONE TYPE of capability toolkit slot.** Per slot-family: the triggered-passive variant has higher probability vs. multiplicative / mechanic-adjusting / etc. on WEAPONS (per D55 high-probability flavor); on ARMOR and ACCESSORIES other capability types dominate.

### 5.5 LLM raw-reasoning constraint (D7 AI-tell line) preserved

Per Wave 2 doc 43 § 11.5 + Wave 3 doc 44 § 8.7: synergy scan is pattern library + statistical priors + algorithmic composition. **NOT LLM raw-reasoning.** Wave 4 gear gen preserves this constraint:

- Per-slot triggered-passive pattern library is gandalf-curated (per § 5.1)
- Probability anchors are tabular constants per § 5.2
- True-active probability is tabular per § 5.3
- Composition with capability toolkit is algorithmic per § 5.4

**LLM is permitted for player-facing NAMING of legendary instances** (the lore-name of the legendary; e.g., "Stormbreaker's Wrath" for a wind-element thorny-on-hit legendary). LLM is PROHIBITED for SCORING / SELECTION of which triggered-passive pattern rolls on which legendary instance. The line between naming (LLM-allowed) and scoring (LLM-prohibited) is preserved per D7.

---

## 6. Modifier-surface expansion at legendary (per D56)

Per doc 40 § 3.4 + D56 + doc 42 § 4.2 Legendary+ exclusive modifier types.

### 6.1 Per-rarity expansion specification

| Rarity | Modifier surface expansion |
|---|---|
| COMMON / UNCOMMON / RARE / EPIC | Baseline 9-category surface (per doc 42 § 5 sample enumerations); ~32 baseline modifier types |
| LEGENDARY_T0 / LEGENDARY_T0_5 / LEGENDARY_T1 / LEGENDARY_T2 | Baseline 32 + Legendary-exclusive: capability toolkit categories (multiplicative / mechanic-adjusting / spatial-adjusting / axis-adjusting / added-skill triggered-passive) + on-block / on-dodge triggers (defensive triggers tied to specific defensive mechanics); ~50 effective modifier types |
| SET_T1 / SET_T2 | Per legendary T1-T2 + set-bonus rank (per `SetBonusDefinition` partition_schema.py:493) |

### 6.2 Drop fantasy framing per D56

Per doc 40 § 3.4: legendaries differentiate from lesser rarities PRIMARILY through **modifier-surface expansion** (new stat types Epic cannot roll) rather than scalar-numerical-escalation. The drop fantasy is **"did I get NEW capabilities"** rather than "did I get bigger numbers."

**Implementation enforcement:** Wave 4 gear gen MUST ensure legendary drops include at least one modifier from the Legendary+ exclusive surface (capability toolkit OR added-skill OR on-block/on-dodge OR T4-attunement annotation at Tier 1+2). Pure-numerical-escalation legendaries (legendary with only baseline 32 modifiers + slightly higher magnitudes) are ANTI-PATTERN per D56 + closeout § 3.4 drop-fantasy framing.

### 6.3 Composition with tier-restriction (doc 42 principle 2)

Per doc 42 § 4 tier-restricted modifier surface + principle 2: ~35-45% of effective modifier types are tier-restricted (Epic+ / Legendary+ / Tier-1+2 exclusive). Wave 4 gear gen enforces this via `TierRestriction` enum + `modifier_passes_tier_check()` function landed at `partition_schema.py:297-330` (Wave 1).

**Per-rarity enforcement:** when generating a legendary T0 instance, the algorithm CAN include capability-toolkit modifiers (Legendary+) but CANNOT include T4-attunement annotation (Tier-1+2 only). Tier-restriction enforcement is per modifier, not per rarity tier.

---

## 7. Capability toolkit at legendary tier (legendary-exclusive enforcement)

Per Wave 1 doc 42 § 7 SC-4 Gate 5 LOCKED HYBRID + doc 40 § 3.3 + D54.

### 7.1 Capability-toolkit-legendary-exclusive lock

Per SC-4 cross-ARPG consensus (Diablo 4 + Path of Exile + Last Epoch + Grim Dawn — all 4 reference ARPGs): capability-toolkit modifiers are LEGENDARY-EXCLUSIVE. The capability category taxonomy per doc 40 § 3.3 enumerates **6 categories** spanning the toolkit surface. Wave 1 `CapabilityCategory` enum (partition_schema.py:376-381) implemented **5 of the 6 categories**; Wave 4 extends the enum to **6 members** by adding `MULTIPLICATIVE` at W4R.1 (additive, non-breaking schema change per ADR-004) so the implementation enum matches the doc 40 canonical taxonomy 1:1 before capability toolkit generation fires at W4R.4.

**Empirical state (partition_schema.py:376-381 at Wave 3 close — 5 members):**

| # | Enum member | Status |
|---|---|---|
| 1 | `MECHANIC_ADJUSTING` | Present (Wave 1) |
| 2 | `SPATIAL_ADJUSTING` | Present (Wave 1) |
| 3 | `AXIS_ADJUSTING` | Present (Wave 1) |
| 4 | `TRIGGERED_PASSIVE` | Present (Wave 1) |
| 5 | `TRUE_ACTIVE` | Present (Wave 1) |

**Wave 4 W4R.1 extension (add 1 member → 6 total):**

| # | Enum member | Status |
|---|---|---|
| 6 | `MULTIPLICATIVE` | **ADD at W4R.1** (Wave 4 extension; closes the doc 40 § 3.3 taxonomy gap) |

**Post-W4R.1 enum (target — 6 members per doc 40 § 3.3 canonical taxonomy):**

| Enum member | Doc 40 § 3.3 row | Effect | Legendary-exclusive? | Slot constraint |
|---|---|---|---|---|
| `MULTIPLICATIVE` | Multiplicative | Numerical multiplier on matching T4 path (Tier 1+2 only per doc 40 § 3.3) | YES | All legendary/set slots |
| `MECHANIC_ADJUSTING` | Mechanic-adjusting | Changes HOW a mechanic works (e.g., bleeds also slow) | YES | All legendary/set slots |
| `SPATIAL_ADJUSTING` | Spatial-adjusting | Changes geometry / range / area (cone→circle; ranged→melee) | YES | All legendary/set slots |
| `AXIS_ADJUSTING` | Axis-adjusting | Changes damage type or resource axis (fire→ice; mana→HP) | YES | All legendary/set slots |
| `TRIGGERED_PASSIVE` | Added skill — passive (triggered-effect-dominant) | Auto-triggered added-skill passive (per § 5 above) | YES | All slots |
| `TRUE_ACTIVE` | Added skill — true active | Player-activated added-skill on skill-bar (per § 5.3); EXTREMELY RARE | YES | **Weapons only** (per D55 + § 5.3) |

**Semantic distinction (binding):** `MULTIPLICATIVE` and `TRUE_ACTIVE` are categorically distinct mechanisms and MUST NOT be conflated. `MULTIPLICATIVE` is an auto-applied numerical multiplier on a matching T4 path (passive scalar; no player input); `TRUE_ACTIVE` is a player-activated skill on the skill-bar consuming an additive base-skill-budget slot. Conflation would corrupt the doc 40 § 3.3 taxonomy and break the content-compositional attunement model (closeout § 3.4) which depends on multiplicative-on-T4-path as a foundational mechanism.

**W4R.1 implementation requirements for the enum extension:**

- Add `MULTIPLICATIVE = "multiplicative"` as the 6th member of `CapabilityCategory` (partition_schema.py:376-381 extends to 376-382)
- Update module-load assertion: `assert len(CapabilityCategory) == 6` (Wave 1 implicit count of 5 → Wave 4 explicit count of 6)
- MIGRATION.md filing per ADR-004 (additive enum extension; no breaking change to Wave 1/2/3 consumers — existing enum members + values preserved verbatim; new member appended)
- Math note per Discipline #1 BEFORE W4R.1 implementation (covers per-rarity grid + capability toolkit composition; capability category enumeration is consumed by per-slot-family weighting in § 7.3)

**Wave 4 gear gen enforcement (post-W4R.1):** `can_roll_capability_toolkit(rarity)` (partition_schema.py:384) returns True ONLY for legendary rarities (`LEGENDARY_RARITIES` frozenset partition_schema.py:89). Epic and below MAY NOT roll capability toolkit. All 6 enum members are legendary-exclusive uniformly; per-category-per-slot-family weighting per § 7.3 applies only within the legendary-exclusive gate.

### 7.2 Per-legendary capability slot allocation

Per doc 40 § 3.3 + Wave 1 partition substrate:

- LEGENDARY_T0 / LEGENDARY_T0_5 / LEGENDARY_T1: 1 capability toolkit slot per legendary (always)
- LEGENDARY_T2: 1 capability toolkit slot + `DUAL_CAPABILITY_PROBABILITY[LEGENDARY_T2]` chance of 2nd slot (rare even at T2; gamora SC-7 calibrates post-Wave-4-baseline per #18.2)
- SET_T1 / SET_T2: per legendary T1-T2 rate

### 7.3 Capability category selection per slot family

Different slot families favor different capability categories:

| Slot family | Dominant capability categories |
|---|---|
| Weapons | TRIGGERED_PASSIVE (per § 5 dominant) + MULTIPLICATIVE (T1+2 only) + AXIS_ADJUSTING (element-conversion variants) |
| Armor | TRIGGERED_PASSIVE (on-being-hit variants) + MECHANIC_ADJUSTING (defensive mechanic tweaks) + SPATIAL_ADJUSTING (defensive-geometry tweaks) |
| Accessories | TRIGGERED_PASSIVE (general passive variants) + MULTIPLICATIVE (universal damage / defense bonus) + AXIS_ADJUSTING (resource-axis tweaks) |

Wave 4 implementation MUST encode per-slot-family capability category weighting; rocket calibrates starting weights at W4R.4.

---

## 8. Set bonus structure (Set T1-T2 endgame-only)

Per closeout § 3.4 + doc 40 D48.

### 8.1 4-piece set structure

> **4-piece sets standard; 2-piece minor bonus (always-active) + 4-piece full bonus (content composed with chain + T4).**

| Pieces equipped | Effect tier |
|---|---|
| 1 of set | No bonus (per-piece stats apply per legendary rules) |
| 2 of set | **Minor bonus** (always-active; e.g., "+15% damage when set bonus active") |
| 3 of set | No additional bonus (Wave 4 v1 architecture; future v1.1+ may add 3-piece intermediate per substrate evidence) |
| 4 of set | **Full bonus** (T4-attuned + set-cohesive; e.g., "When [T4-A is active]: all wind chain skills gain stormburst trigger + 25% chain damage") |

### 8.2 Endgame-exclusive

Per doc 40 D48: sets are 2-tier (T1 + T2); endgame-only; ALWAYS T4-attuned. No Tier 0 / Tier 0.5 sets exist. Set drops are gated to L45-50+ endgame content per doc 41 progression node mapping.

### 8.3 Set bonus rank per `SetBonusDefinition` (Wave 1 schema)

Per `SetBonusDefinition` dataclass partition_schema.py:493 (Wave 1 schema):

- Set bonus rank value encoded per set instance
- Rank-1 = SET_T1 set bonus magnitude
- Rank-2 = SET_T2 set bonus magnitude

Wave 4 gear gen populates `SetBonusDefinition` per generated set instance with chain + T4-attunement coherence across the 4 pieces.

### 8.4 Set generation atomicity discipline

**Set pieces are generated as a coherent 4-piece bundle, not as independent gear instances.** The algorithm:

1. Selects set identity (which set; from set pool at endgame content tier)
2. Selects T4-attunement target for the set (one T4 candidate per closeout § 3.4 — "content composed with chain + T4")
3. Generates 4 PartitionGearInstance entries with coherent T4-attunement annotation + per-piece slot routing (typically 1 weapon + 2 armor + 1 accessory OR 4 armor; per-set composition is content authoring surface)
4. Encodes `SetBonusDefinition` with rank + 2pc + 4pc bonus specifications

Set generation atomicity prevents partial-set drops (player gets only 2 pieces of a 4-piece set leaves the other 2 in the global drop pool to be obtained later via continued play).

---

## 9. Sub-wave structure W4R.0-W4R.7 for rocket Wave 4 implementation

Mirrors Wave 1 W1.0-W1.8 + Wave 2 W2.0-W2.9 + Wave 3 W3.0-W3.5 implementation-atomic pattern. Wave 4 scope is between Wave 1 and Wave 2 in size; 8 sub-waves.

| Sub-wave | Work-unit | Owner | Gate |
|---|---|---|---|
| **W4R.0 — Substrate prep + repo-scaffold** | Review Wave 1 partition output (`partition_schema.py` + `partition_modifier_pool.py` + `partition_roller.py`); Wave 2+3 T4 algorithm output (`t4_category_schema.py` + `t4_scope_selector.py` + `t4_synergy_scan.py` + `t4_option_f.py` + `t4_algorithm_wave2.py`); identify consumption points (PartitionGearInstance generation entry-point; T4CandidateV2 consumption for annotation; capability toolkit selection); spot-check existing schema coherence to confirm field-addition pattern viable | rocket | Substrate prep audit committed; ready for W4R.1 |
| **W4R.1 — Per-rarity gear instance generation algorithm + `CapabilityCategory` enum extension (`MULTIPLICATIVE` add)** | Implement gear generation algorithm per § 3 per-rarity grid for all 10 rarity tiers (Common through Set T2); algorithm samples from partition pool per per-slot affinity matrix; tier-restriction enforcement per `modifier_passes_tier_check()`; resource-model gating per principle 3; gap-filling per D80; module-load `assert len(PartitionRarity) == 10` enforcement. **PLUS: Extend `CapabilityCategory` enum per § 7.1 — add `MULTIPLICATIVE = "multiplicative"` as 6th member (Wave 1 implemented 5; doc 40 § 3.3 canonical taxonomy specifies 6; W4R.1 closes the gap before capability toolkit generation fires at W4R.4); module-load `assert len(CapabilityCategory) == 6` enforcement; MIGRATION.md filing per ADR-004 (additive non-breaking; existing 5 members + values preserved verbatim).** Math note per Discipline #1 BEFORE algorithm implementation (covers per-rarity grid + capability category enumeration consumed by § 7.3 per-slot-family weighting) | rocket | jack-ryan Gate-1 critique; math note PASS per #1; per-rarity generation produces valid PartitionGearInstance for all 10 rarities; `CapabilityCategory` extended to 6 members with `MULTIPLICATIVE` present + `len()` assertion at module load |
| **W4R.2 — T4-attunement annotation per content-compositional model** | Implement T4-attunement annotation population per § 4: Tier 1+2 legendary + all sets get annotation; T4 target selected from kit's T4 candidate pool (Wave 2+3 substrate); scope-preference hint populated when available per § 4.3 (proposed `T4AttunementAnnotation.scope_preference: T4Scope \| None` field addition); annotation does NOT toggle ON/OFF (preserved per § 4.1) | rocket | jack-ryan Gate-1 critique; annotation correctly absent for COMMON-EPIC + LEGENDARY T0/T0.5; correctly present + populated for LEGENDARY T1/T2 + SET T1/T2; scope hint optional per § 4.3 |
| **W4R.3 — Triggered-passive added-skill generation per D55** | Implement per-slot-family triggered-passive pattern library per § 5.1; probability anchors per § 5.2; rare true-active weapon-only per § 5.3; composition with capability toolkit per § 5.4; per-slot routing distinguishes weapon-only vs accessory-allowed patterns; LLM raw-reasoning constraint per § 5.5 preserved (gandalf-curated patterns + tabular probabilities; LLM permitted only for player-facing naming) | rocket | jack-ryan Gate-1 critique; per-slot-family triggered-passive correctly routed; weapon-only true-active enforcement verified; probability anchors empirically match § 5.2 starting estimates |
| **W4R.4 — Modifier-surface expansion per D56 + capability toolkit at legendary** | Implement modifier-surface expansion per § 6: legendary gear MUST include at least one Legendary+ exclusive modifier (D56 anti-pattern enforcement); capability-toolkit-legendary-exclusive enforcement per § 7 via `can_roll_capability_toolkit()`; per-slot-family capability category weighting per § 7.3; dual-capability roll at LEGENDARY_T2 per `DUAL_CAPABILITY_PROBABILITY` | rocket | jack-ryan Gate-1 critique; modifier-surface expansion verified; capability-toolkit-legendary-exclusive enforced; dual-capability rolls observed at expected rate |
| **W4R.5 — Set bonus structure (Set T1-T2)** | Implement set generation atomicity per § 8.4: 4-piece coherent bundle generation with shared T4-attunement annotation + per-piece slot routing; 2pc minor + 4pc full bonus per § 8.1; rank encoding per `SetBonusDefinition` § 8.3; endgame-exclusive drop gating per § 8.2 (L45-50+ content) | rocket | jack-ryan Gate-1 critique; set atomicity verified (no partial-set drops in single generation event); 2pc + 4pc bonuses correctly composed; rank encoding matches § 8.3 |
| **W4R.6 — Cross-cohesion validation per #26 + Block C** | Extends Wave 1/2/3 cross-cohesion pattern with gear gen output validation: spot-check sim runs against generated gear instances across 4 cohort archetypes (DPS-min-maxer / Balanced / Defensive / Hybrid per Block C scaffolding) × per-rarity × per-slot grid; validation criteria — per-cohort gear distribution preserves build diversity (no cohort × slot cell structurally locked out; gap-filling D80 distributes drops); Pattern 9 + Pattern 10 detection at GEAR-EFFECTIVE rate (gear modifier × T4 multiplier vs Pattern 9+10 threshold) per § 4.5 #32 composition; WARN-pattern starting estimate <15% per cohort × slot × rarity cell (gamora SC-7 iterates post-Wave-4-baseline per #18.2) | gamora + jack-ryan | jack-ryan Gate-2 PASS on cross-cohesion validation; per-cohort gear distribution within expected bounds; Pattern 9+10 gear-effective WARN-rate within bounds |
| **W4R.7 — Round-trip smoke per Principle 6 (CRITICAL: maintain WARN-pattern PRESERVED milestone)** | Full round-trip smoke covering all 10 rarity tiers including `legendary_t0_5` (Wave 1/2/3 carryover discipline); gear gen per slot × per class × per rarity × per T4-attunement target; T4-attunement annotation matching verified across rarity variants; capability-toolkit composition verified across slot-family variants; scope-preference hint emission verified (when annotation populated) per § 4.3; drax cross-seam touch flag — `scope_projection_data` field consumption by drax-ready data structure verified (Wave 3 W3.5 carryover); post-script empirical count assertions per Discipline #11 (CRITICAL: maintain WARN-pattern PRESERVED milestone — Wave 4 Gate-2 = 0 empirical assertion failures; module-load `assert len()` for all extended catalogs); MIGRATION.md filed per ADR-004 (Wave 3 → Wave 4 contract change is additive: optional `scope_preference` field on T4AttunementAnnotation; optional `is_unique` field on PartitionGearInstance if added per § 3.2) | rocket + jack-ryan | jack-ryan Gate-2 PASS on round-trip smoke + maintained WARN-pattern PRESERVED + MIGRATION.md filed |

Sub-wave sequencing is implementation-atomic; rocket + knight-rider may adjust dependencies per Wave 4 implementation dispatch.

**Sub-wave count = 8 (W4R.0 through W4R.7).** Module-load `assert` equivalent at dispatch authoring time: 8 sub-waves enumerated.

---

## 10. Wave 4 implementation guidance for rocket

Concrete next-steps for rocket Wave 4 implementation against this design intent.

### 10.1 Wave 1+2+3 substrate consumption

Wave 4 algorithm CONSUMES Wave 1+2+3 substrate as platform. Specific consumption points:

| Wave 1/2/3 surface | Wave 4 consumption |
|---|---|
| **`PartitionRarity` enum** (10 values; partition_schema.py:67-77) | Per-rarity gear generation iterates all 10 values per § 3.1 |
| **`AffinityMatrix`** (partition_schema.py:241-292) | Per-slot affinity sampling per § 2.3 algorithm |
| **`TIER_1_2_RARITIES`** (partition_schema.py:99) | T4-attunement annotation gate per § 4.2 |
| **`LEGENDARY_RARITIES`** (partition_schema.py:89) | Capability toolkit gate per § 7.1 |
| **`CapabilityCategory`** (partition_schema.py:376) | Capability slot selection per § 7.3 |
| **`CapabilityModifier`** (partition_schema.py:411) | Capability modifier instantiation per § 7 |
| **`T4AttunementAnnotation`** (partition_schema.py:479) | Annotation population per § 4 (PROPOSED extension: add `scope_preference: T4Scope \| None` field) |
| **`SetBonusDefinition`** (partition_schema.py:493) | Set bonus rank + 2pc + 4pc bonus encoding per § 8 |
| **`PartitionGearInstance`** (partition_schema.py:515) | Final emit surface; gear gen produces these (PROPOSED extension: add `is_unique: bool` field if uniques routed per § 3.2) |
| **`TRUE_ACTIVE_PROBABILITY`** (partition_schema.py:390) | True-active rolling per § 5.3 |
| **`DUAL_CAPABILITY_PROBABILITY`** (partition_schema.py:400) | Dual-capability rolling at LEGENDARY_T2 per § 7.2 |
| **`T4CandidateV2`** (t4_category_schema.py:240) | T4 target selection for annotation per § 4 |
| **`T4Scope`** (Wave 3 enum on T4CandidateV2) | Scope-preference hint propagation per § 4.3 |
| **`scope_projection_data`** dict on T4CandidateV2 (Wave 3 W3.5 carryover) | Cross-seam touch flag for drax consumption per § 10.5 |

### 10.2 Math-before-code (Discipline #1) requirement

Per Discipline #1: math note BEFORE algorithm implementation. Wave 4 math note location: `~/Games/reincarnated-engine/src/reincarnated/generation/math/cycle-13-wave-4-spec-driven-gear-gen-math-2026-05-2X.md` (rocket-authored at W4R.1).

**Math note must cover:**
- Per-rarity modifier count formula + categories rollable per § 3.1
- Per-slot affinity matrix sampling + normalization per Wave 1 § 9.2 (consumption)
- Tier-restriction enforcement formula per § 6.3
- Gap-filling scoring formula per D80
- T4-attunement annotation population logic per § 4
- Triggered-passive probability anchors per § 5.2
- True-active probability per § 5.3
- Capability category weighting per § 7.3
- Set bonus rank encoding per § 8.3

### 10.3 Discipline #11 empirical inspection (CRITICAL — maintain WARN-pattern PRESERVED milestone)

Per Wave 1+2+3 Gate-2 WARN-pattern PRESERVED milestone (full closure through Wave 3): Wave 4 Gate-2 MUST maintain the discipline. **Every post-script empirical count assertion in completion record MUST verify against actual code state via `len()` or equivalent at write-time.** Per Wave 2+3 rocket pattern, prefer module-load `assert len(X) == N` enforcement for constant collections.

**Asserted counts to verify empirically at Wave 4 completion-record authoring time:**
- `PartitionRarity` length = 10 (preserved from Wave 1; CRITICAL — gear gen iterates all 10)
- `LEGENDARY_RARITIES` length = 6 (LEGENDARY_T0 + LEGENDARY_T0_5 + LEGENDARY_T1 + LEGENDARY_T2 + SET_T1 + SET_T2)
- `TIER_1_2_RARITIES` length = 4 (LEGENDARY_T1 + LEGENDARY_T2 + SET_T1 + SET_T2)
- `CapabilityCategory` length = **6** post-W4R.1 (extends Wave 1's 5 members by adding `MULTIPLICATIVE` per § 7.1; final ordered members: MECHANIC_ADJUSTING + SPATIAL_ADJUSTING + AXIS_ADJUSTING + TRIGGERED_PASSIVE + TRUE_ACTIVE + MULTIPLICATIVE — Wave 4 extension; closes the doc 40 § 3.3 canonical taxonomy gap; module-load `assert len(CapabilityCategory) == 6` at W4R.4 close; W4R.1 math note covers the extension)
- Per-slot-family triggered-passive pattern library counts (rocket determines per § 5.1 enumeration extension)
- Sub-wave count = 8 (W4R.0-W4R.7)
- Round-trip smoke rarity coverage = 10 (preserved from Wave 1+2+3; including `legendary_t0_5`)

Each assertion MUST be drawn from `len()` against the module-level constant at write-time. No pre-addition draft counts.

### 10.4 Cross-seam contract change (Principle 6 gate)

Wave 4 introduces ADDITIVE cross-seam contract changes (no breaking):

- `T4AttunementAnnotation.scope_preference: T4Scope | None` proposed field addition (default `None` preserves Wave 1 read-back compatibility)
- `PartitionGearInstance.is_unique: bool` proposed field addition if unique routing per § 3.2 (default `False` preserves Wave 1 read-back compatibility)
- Gear generation output telemetry gains per-rarity distribution + per-slot-family triggered-passive distribution + per-T4-attunement distribution (input to D25 cross-season learning + gamora SC-7 calibration)
- drax cross-seam touch flag — Wave 4 gear gen output consumes `scope_projection_data` dict from T4CandidateV2 (Wave 3 W3.5 carryover) for spirit-guide projection messaging per § 4.3

Round-trip smoke per Principle 6 fires at W4R.7 covering all 10 rarity tiers × slot variants × T4-attunement target variants + cross-seam consumer paths (drax spirit-guide consumption + telemetry consumption + gamora SC-7 sim cycling consumption). MIGRATION.md filing per ADR-004 required (additive; no breaking change to Wave 1/2/3 consumers).

### 10.5 drax cross-seam touch flag (per Wave 3 I5 carryover)

Per Wave 3 Gate-2 finding I5 noted: `scope_projection_data` dict on T4CandidateV2 (Wave 3 W3.5 output) is a drax cross-seam touch for Wave 4+ integration. Wave 4 gear gen:

- Reads `scope_projection_data` from T4CandidateV2 selected for annotation
- Populates Wave 4 gear generation telemetry with per-scope-aligned drop attribution
- Provides surface for drax to consume per-scope T4 projection messaging (spirit-guide voice per closeout § 3.5 + doc 41 D31 spirit-guide-projection language framework)

drax cross-seam consumption surface is downstream of Wave 4 (not implemented in Wave 4 itself); doc 45 FLAGS the surface for drax Wave 4+ integration dispatch (separate from rocket Wave 4 implementation dispatch).

### 10.6 Telemetry emission for gamora SC-7 calibration (#18.2)

Per § 5.2 + § 7.2 starting estimates: Wave 4 implementation MUST emit telemetry sufficient for gamora SC-7 post-Wave-4-baseline calibration.

**Required telemetry fields per gear generation event:**
- Rarity selected (10 values)
- Slot routed (11 values)
- Modifier categories rolled (per § 3.1 categories rollable)
- Capability toolkit category selected (if applicable; 5 values + "none")
- Triggered-passive presence + pattern selected (per § 5.1 pattern library)
- True-active roll outcome (binary; weapon-only)
- T4-attunement annotation populated (if applicable; chain + T4 candidate + scope-preference hint)
- Set bonus rank (if set)
- Gap-fill score per D80 (input to gap-filling calibration)
- Cross-cohesion validation outcome (per W4R.6 spot-check)

Telemetry feeds into D25 cross-season learning + gamora SC-7 methodology consultation post-Wave-4-baseline.

### 10.7 Disciplines #27 / #31 / #32 composition preserved

Per Wave 2+3 doc 43/44 § 11.7-11.8 + Gate-2 D3+D4+D5 verification: Disciplines #27 + #31 + #32 compose throughout Wave 2+3; Wave 4 preserves the composition.

- **#27 dual-effect capstone:** preserved upstream at T4 algorithm layer; Wave 4 gear annotation refers to T4 candidates (not at gear layer per § 4.5)
- **#31 dual-effect separability:** preserved upstream at T4 algorithm layer (per § 4.5)
- **#32 first-do-no-harm:** EXTENDED in Wave 4 per § 4.5. Pattern 9 + Pattern 10 detection at GEAR-EFFECTIVE rate (gear modifier × T4 multiplier vs Pattern 9+10 threshold). Wave 4 cross-cohesion validation (W4R.6) implements #32 at gear-gen layer

Each Wave 4 sub-wave dispatch (W4R.0-W4R.7) must cite the relevant disciplines explicitly.

---

## 11. Composition with gamora SC-7 Track B

Wave 4 has TWO TRACKS per dispatch:

- **Track A (rocket; THIS DOC):** spec-driven gear gen
- **Track B (gamora; SEPARATE DISPATCH):** T4 Phase 4 sim cycling per doc 40 D81 Phase 4 + D85; methodology output by gamora SC-7

### 11.1 Cross-track data-flow

Wave 4 Track A (rocket gear gen) produces gear-instance output that Wave 4 Track B (gamora SC-7 sim cycling) consumes:

| Track A output | Track B consumption |
|---|---|
| `PartitionGearInstance` instances per kit × per rarity × per slot | Sim cycling samples gear loadouts from gear gen output; runs gauntlet sim per cohort × per cell × per encounter |
| T4-attunement annotation per Tier-1+2 legendary + sets | Sim cycling validates T4-attunement coherence (gear aligned to T4-A composes well with T4-A active; gear aligned to T4-B composes poorly when T4-A active — per spirit-guide projection delta per § 4.4) |
| Capability toolkit selections | Sim cycling validates capability-toolkit + T4 + chain composition produces playability-AND-in-band per Discipline #26 |
| Scope-preference hints (Wave 3 W3.5 carryover) | Sim cycling validates scope-preference + T4 scope coherence (character-wide-hinted gear with character-wide T4 composes coherently) |
| Set bonus structure (4-piece coherent bundles) | Sim cycling validates set 4-piece bonus composes with T4-attunement coherence per § 8 |
| Pattern 9 + Pattern 10 gear-effective WARN-flags (W4R.6 output) | Sim cycling cross-validates gear-effective Pattern 9+10 flags against sim-observed degenerate states |

### 11.2 Cross-track cohesion validation

Wave 4 close criterion (coordinated):

- Track A (rocket gear gen) close: jack-ryan Gate-2 PASS on rocket Wave 4 implementation per § 13
- Track B (gamora SC-7 sim cycling) close: jack-ryan Gate-2 PASS on gamora SC-7 methodology output (per gamora SC-7 dispatch separate scope)
- **Wave 4 close = BOTH Track A AND Track B closed** (coordinated; one track closing alone does NOT close Wave 4)

### 11.3 Data-field implications flagged for SC-7

Doc 45 flags the following Wave 4 Track A data fields as Track B SC-7 consumption surface:

| Wave 4 Track A field | SC-7 Track B implication |
|---|---|
| `PartitionGearInstance` per-modifier roll values | SC-7 sim cycling consumes gear stat rolls as kit stat sheet input |
| `T4AttunementAnnotation.scope_preference` (proposed) | SC-7 sim cycling consumes scope hint as cohort-archetype validation input |
| `CapabilityModifier` triggered-passive pattern selection | SC-7 sim cycling consumes triggered-passive patterns as proc-rate input |
| `SetBonusDefinition.rank + 2pc + 4pc` | SC-7 sim cycling validates set-bonus contribution to per-piece effective DPS |
| Gear gen telemetry per § 10.6 | SC-7 sim cycling cross-validates telemetry-observed distribution vs sim-observed distribution |

SC-7 dispatch authoring (separate from this doc 45) will encode these consumption surfaces explicitly.

### 11.4 No cross-track contract during Wave 4 authoring

Doc 45 (THIS DOC) does NOT specify SC-7 methodology — that is gamora's SC-7 seam ownership. Doc 45 only flags consumption surfaces. SC-7 methodology + sim cycling design is gamora-authored per separate dispatch firing concurrently with this dispatch.

---

## 12. Discipline #23 framing-audit (three-question protocol)

Per Discipline #23 (framing-audit checklist) + Wave 2 doc 43 § 11.9 + Wave 3 doc 44 § 11 precedent: at any Pattern A-deep verdict authoring, methodology consultation at a math hotspot, or work-unit committing load-bearing framing assumptions, apply the three-question protocol before execution proceeds. Doc 45 is a load-bearing design-intent doc for the Wave 4 spec-driven gear gen (rocket track) and operationalizes the Phase 2d spec-driven gear gen substrate-bound at substrate (Wave 1) plus the T4 algorithm output (Wave 2+3). **§ 12 included FROM START per Wave 2 Gate-1 W1 amendment lesson + doc 44 § 11 precedent — doc 45 does NOT repeat the W1 amendment pattern.**

**Load-bearing framing assumption (Q0 — what's being audited):** the **spec-driven gear gen architectural pattern** as a SCORED-CANDIDATE strategy registry mirroring the T4 algorithm pattern at the GEAR-INSTANCE LAYER IS the correct structural framing for Wave 4 implementation, AND the per-rarity grid (10 tiers per `PartitionRarity` enum) + T4-attunement annotation per content-compositional model (NOT toggle mechanism) + capability-toolkit-legendary-exclusive enforcement + triggered-passive added-skill high-probability on weapons per D55 + 4-piece set bonus structure endgame-only correctly bound the design space for the gear gen layer.

### Q1 — What evidence would refute the spec-driven gear gen scored-candidate framing?

The spec-driven scored-candidate framing means gear gen mirrors T4 algorithm architecture (kit+T4 produces spec; strategies produce candidates; sim validates). Refutation evidence would surface as one of:

1. **Pattern surface fit gap:** if the gear gen problem shape does NOT actually match the T4 algorithm shape — e.g., if gear gen is fundamentally a CONTINUOUS sampling problem (per-slot per-rarity per-modifier roll within continuous magnitude bands) rather than a DISCRETE candidate-strategy problem (where strategies map to algorithmic-distinct cases like the 7 T4 strategies). The T4 algorithm has discrete strategies because T4 design space is structurally discrete (RESOURCE_CONVERSION vs ELEMENT_CONVERSION are categorically different); gear gen modifier rolling is a CONTINUOUS sampling problem with discrete capability-toolkit overlay. If discrete-vs-continuous is a load-bearing distinction, the "mirrors T4 algorithm" framing may be over-fit. **Refutation evidence:** Wave 4 implementation surfaces a CONTINUOUS-sampling abstraction that does not benefit from the discrete-strategy-registry pattern, suggesting alternate framing (e.g., affinity-weighted sampler + tier-restriction filter + gap-fill scorer without a "strategy registry" layer).
2. **Substrate-already-suffices gap:** if Wave 1 partition substrate (affinity matrix + per-rarity grid + tier-restricted modifier surface + 6 principles + `partition_roller.py` sampling) is ALREADY a complete gear gen algorithm without needing the spec-driven scored-candidate layer. **Refutation evidence:** Wave 1 partition implementation already produces valid gear instances at all rarities; Wave 4 may be over-engineering the layer above. Mitigation: § 2.2 spec-driven means substrate-bound (the spec is kit+T4 context; sampling happens from the partition pool). The spec-driven LAYER adds T4-attunement annotation + capability toolkit + triggered-passive added-skill ON TOP of the partition sampling. Wave 1 partition is the modifier-rolling primitive; Wave 4 is the gear-instance-assembly composition over that primitive.
3. **Gear-vs-T4 layer mismatch:** if gear gen layer should NOT generate T4-attunement annotation at all (annotation should live elsewhere — e.g., as a kit-level metadata field rather than per-gear-instance). **Refutation evidence:** content-compositional attunement per closeout § 3.4 means annotation IS the gear's content quality; per-gear-instance annotation is correct per content-compositional model (the annotation IS the gear's identity, not a side metadata). If annotation moves to kit-level, the content-compositional framing breaks.

### Q2 — What evidence is currently in hand?

Current evidence supporting the framing:

- doc 40 D7 explicitly locks "Gear generation uses the same architectural pattern as T4: a scored-candidate strategy registry" — same scored-candidate strategy registry pattern; mirrors T4
- closeout § 3.4 content-compositional attunement explicitly locks per-gear-instance annotation (NOT kit-level)
- Wave 1 partition substrate (doc 42) provides the affinity matrix + per-rarity grid + tier-restricted surface + 6 principles — these are MODIFIER-ROLLING primitives; Wave 4 layers gear-instance ASSEMBLY (capability toolkit + triggered-passive + T4-attunement annotation + set bonus structure) on top
- Wave 2+3 T4 algorithm (doc 43/44) provides the T4CandidateV2 schema that Wave 4 consumes for annotation
- 10-tier `PartitionRarity` enum is a structural fact (10 distinct rarity tiers; each requires distinct generation rule per § 3.1)
- 4-ARPG cross-consensus on capability-toolkit-legendary-exclusive (per SC-4 Gate 5 LOCKED HYBRID)

Current evidence that could refute (per Q1 candidates):

- No empirical Wave 4 implementation yet (this doc is design intent BEFORE implementation); cannot directly refute pattern-surface-fit gap until rocket attempts Wave 4 algorithm
- Wave 1 partition implementation already produces valid PartitionGearInstance; Wave 4 ADDS to that surface but does not REPLACE it; risk of over-engineering is mitigated but not eliminated until rocket implements

### Q3 — Refine framing OR proceed as-framed?

**Verdict: proceed as-framed with two refinement notes for rocket Wave 4 implementation:**

1. **Refinement note A:** Wave 4 implementation MAY surface that the "strategy registry" framing is over-fit for gear gen (per Q1 #1). Rocket has discretion at W4R.1 to adopt the actual implementation shape that fits — whether that's a strategy registry analog (mirrors T4 algorithm) OR an affinity-weighted-sampler + capability-toolkit-overlay decomposition. The DESIGN INTENT is the OUTPUTS (per-rarity gear instances per § 3 grid + T4-attunement annotation per § 4 model + capability toolkit per § 7 + triggered-passive per § 5 + set structure per § 8); the ALGORITHM SHAPE is rocket's implementation discretion within the spec-driven substrate-bound constraint.
2. **Refinement note B:** if rocket implementation experience at W4R.1-W4R.5 reveals that the content-compositional attunement model has a load-bearing failure mode (per Q1 #3), surface to gandalf for Pattern-A consultation before W4R.6 fires. Annotation-as-metadata vs. annotation-as-content-quality may need refinement. Current framing per closeout § 3.4 + § 4.1 is CONTENT-COMPOSITIONAL (gear content IS the attunement; annotation IS metadata recording it; magnitude IS content quality). This framing is load-bearing.

**Net:** proceed with Wave 4 doc 45 as design intent; rocket Wave 4 implementation has algorithm-shape discretion within spec-driven substrate-bound constraint; framing-audit refinement notes A+B logged for rocket reference.

---

## 13. Wave 4 close criterion (rocket track)

Wave 4 (rocket track) closes when:

- [ ] W4R.0-W4R.7 all complete per completion record table
- [ ] Per-rarity gear instance generation operational per § 3 for all 10 rarity tiers; module-load `assert len(PartitionRarity) == 10` enforcement preserved
- [ ] T4-attunement annotation per § 4 content-compositional model implemented; annotation populated for LEGENDARY_T1 / LEGENDARY_T2 / SET_T1 / SET_T2; annotation absent for COMMON-EPIC + LEGENDARY T0/T0.5; scope-preference hint optional per § 4.3 (proposed `scope_preference` field addition on T4AttunementAnnotation)
- [ ] Triggered-passive added-skill generation per § 5 D55 high-probability rule operational; per-slot-family pattern library populated; probability anchors per § 5.2 starting estimates; weapon-only true-active enforced per § 5.3
- [ ] Modifier-surface expansion per § 6 D56 enforced; capability-toolkit-legendary-exclusive per § 7 SC-4 Gate 5 LOCKED HYBRID; dual-capability roll at LEGENDARY_T2 per `DUAL_CAPABILITY_PROBABILITY`
- [ ] Set bonus structure per § 8: 4-piece atomicity; 2pc minor + 4pc full bonus; endgame-exclusive drop gating; rank encoding per `SetBonusDefinition`
- [ ] Cross-cohesion validation per #26 + Block C scaffolding (4 cohort archetypes × per-rarity × per-slot grid; gamora spot-check sim); jack-ryan Gate-2 PASS on cross-cohesion
- [ ] Round-trip smoke per Principle 6 covering all 10 rarity tiers × slot variants × T4-attunement target variants × drax cross-seam touch flag (`scope_projection_data` consumption); jack-ryan Gate-2 PASS
- [ ] **WARN-pattern PRESERVED milestone MAINTAINED** per Discipline #11 (Wave 4 Gate-2 = 0 empirical assertion failures; module-load `assert len()` enforcement for all extended catalogs; full closure milestone maintained from Wave 1+2+3)
- [ ] Disciplines #27 + #31 + #32 explicitly composed throughout Wave 4 dispatches (per Wave 1+2+3 Gate-1 routing precedent); #32 EXTENDED at gear-effective rate per § 4.5
- [ ] MIGRATION.md filed per ADR-004 (additive cross-seam contract changes: `scope_preference` field on T4AttunementAnnotation; `is_unique` field on PartitionGearInstance if uniques routed)
- [ ] Math note authored per Discipline #1 BEFORE algorithm implementation (per § 10.2)
- [ ] Telemetry emission operational per § 10.6 (supports gamora SC-7 post-Wave-4-baseline calibration)
- [ ] drax cross-seam touch flag (`scope_projection_data` consumption surface) operational per § 10.5
- [ ] jack-ryan Gate-2 PASS on aggregate Wave 4 (rocket track) close
- [ ] **Coordinated with gamora SC-7 Track B close** — Wave 4 = BOTH Track A AND Track B closed per § 11.2

**Wave 4 ready to feed Wave 5 implementation when:** rocket's Wave 4 spec-driven gear gen produces generated gear instances per slot × per rarity × per T4-attunement target whose surface is consumed by gamora SC-7 Track B sim cycling per § 11.1 cross-track data-flow AND by Wave 5 gauntlet sim per D67 independent gauntlet sim AND by drax Wave 4+ spirit-guide projection consumption per § 10.5.

---

## 14. Sign-off

**Author:** gandalf (story-and-design steward)
**Date:** 2026-05-27
**Cycle:** 13
**Wave:** 4 design intent (rocket track)
**Authority:** Matt 2026-05-27 verbatim "Resume Wave 0 → Wave 1 dispatch sequencing per ratified framing brief § 4.1 autonomous scope" + jack-ryan Wave 3 Gate-2 PASS verdict (commit `99ec777` / engine `2e8bc33`) UNBLOCKS Wave 4 dispatch authoring + Wave 3 CLOSED + WARN-pattern PRESERVED milestone

**Companion doc cross-references (final):**

- `canonical/00-ground-state.md` — registers doc 45 as new CURRENT entry
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` § 3 + § 3.5 + § 3.6 + D7-D17 + D33+D38+D51 + D48-D57 + D80 — architectural foundation
- `canonical/42-stat-sheet-modifier-partition-intent-2026-05-27.md` — Wave 1 partition substrate (gear gen consumes)
- `canonical/43-t4-algorithm-wave-2-intent-2026-05-27.md` + `canonical/44-t4-algorithm-wave-3-phase-3-intent-2026-05-27.md` — Wave 2+3 T4 algorithm substrate (gear gen reads for annotation)
- `agentic_orchestration/gandalf/notes/2026-05-27-cycle-13-pre-launch-design-session-closeout.md` § 3 — substantive content authority
- `agentic_orchestration/qa/findings/2026-05-27-cycle-13-wave-3-gate-2-rocket-implementation.md` — Wave 3 Gate-2 PASS + I5 drax cross-seam touch flag

**Gates:** jack-ryan Wave 4 Gate-1 critique on doc 45 → rocket Wave 4 implementation dispatch authoring (post-Gate-1 PASS) → rocket Wave 4 implementation (W4R.0-W4R.7) → rocket Wave 4 Gate-2 (post-implementation) → Wave 4 close (coordinated with gamora SC-7 Track B close per § 11.2)

**Priority:** P1 — critical-path Wave 4 start (rocket track; fires in parallel with gamora SC-7)

**Signed:** gandalf (story-and-design steward)
**For:** the Wave 4 spec-driven gear gen design intent (rocket track) canonical lock for Cycle 13 multi-T4 architecture cycle; per-rarity gear instance generation across all 10 rarity tiers + T4-attunement annotation per content-compositional model + triggered-passive added-skill generation per D55 + modifier-surface expansion at legendary per D56 + capability-toolkit-legendary-exclusive enforcement + 4-piece set bonus structure (Set T1-T2 endgame-only) + sub-wave structure W4R.0-W4R.7 + Wave 4 implementation guidance for rocket + composition with gamora SC-7 Track B + § 12 Discipline #23 framing-audit INCLUDED FROM START per doc 44 precedent + WARN-pattern PRESERVED milestone maintained through Wave 4 Gate-2.
