# Dispatch — Rocket — Cycle 14 Cascade-Resumption-3 Amendment 7: Element Coverage E4C + Hybrid 17.5% Layer

**Date:** 2026-05-29
**From:** knight-rider (orchestrator)
**To:** rocket (content generation seam)
**Authority:**
- Matt 2026-05-29 evening late: "confirmed, fire amendment 7" + Amendment 8 (Matt-gate retired; $50 cap re-imposed)
- gandalf Amendment 7 spec at `agentic_orchestration/gandalf/notes/2026-05-29-amendment-7-element-coverage-e4c-plus-hybrid-spec.md`
- gandalf Amendment 8 commit `be6fdb2` (Matt-gate RETIRED; KR auto-routes per hive-mind decision-routing; $50 cap as primary cost gate)
- Amendment 6 CLOSED in code at engine `6f9843c` + tag `rocket/v1.0-cascade-r3-amendment-6-combined-fix-1`; jack-ryan Gate-2 PASS-with-INFO (collab `beefd64`)

**Pattern:** B sustained-execution (~1-2h Amendment 7 layer + composition verification with Amendment 6)
**R48.4 / R48.5 RETIRED per Amendment 3**
**Standalone dispatch this batch**

---

## 0. TL;DR

**Replace `_BC_ATTRIBUTE_TO_ELEMENT` legacy table with STAT_ELEMENT_POOLS per canonical `elements.yaml` scales_with + add 17.5% hybrid promotion per kit + chain_2.element = secondary for hybrid kits + schema additions.**

Goal: Cycle 14 v1 gauntlet output spans **8 elements** at population level + chain-level element diversity at hybrid layer (pre-Amendment-7 reached only 4 of 8 elements; lightning + holy + shadow + physical at 0%).

**Three-layer mechanism per Amendment 7 spec § 2:**

| Layer | Description |
|---|---|
| **Layer 1 — Cell-level element selection** | STAT_ELEMENT_POOLS: INT→{fire,water,lightning,shadow} / WIS→{earth,wind,holy} / STR→{physical} / DEX→{all 8} (Option C decouple). Draw N=3 elements WITHOUT REPLACEMENT per cell. Seeding: `enc_seed + sample_idx * 17` |
| **Layer 2 — Hybrid promotion 17.5%** | Independent roll per sample; secondary draws from FULL 8-element pool excluding primary |
| **Layer 3 — Chain assignment** | Mono: chain_1 = chain_2 = supporting = kit.element; Hybrid: chain_1 = supporting = primary, chain_2 = secondary |

**Composition with Amendment 6 (already in code):** Amendment 7 layers element variance ON TOP of Amendment 6's N=3 multi-sample structure. § 7.4 acceptance verifies Pareto-2 + S7 deepcopy + S8 Bound 4 paired-joint-sampling all preserved.

**No Matt-gate per Amendment 8.** KR routes jack-ryan Gate-2 post-rocket close; cascade fires through Phase 5 LLM entry WITHOUT Matt-surface; KR monitors $50 cost cap.

**Effort:** ~1-2h.

---

## 1. Required first reads (in order)

1. `agentic_orchestration/gandalf/notes/2026-05-29-amendment-7-element-coverage-e4c-plus-hybrid-spec.md` — AUTHORITATIVE Amendment 7 spec (3 layers + schema + § 7 acceptance)
2. gandalf Amendment 8 at `agentic_orchestration/gandalf/notes/2026-05-29-cascade-resumption-3-class-eradication-authorization.md` Amendment 8 header (Matt-gate retired; $50 cap re-imposed)
3. `reincarnated-engine/config/elements.yaml` — canonical scales_with mapping (Layer 1 source of truth)
4. `canonical/story/attribute-system-2026-05-24.md` § 2.1 — DEX disposition Option C decouple (DEX→full 8-element pool)
5. `canonical/47-damage-scaling-architecture-2026-05-27.md` § 4.6 — ELEMENT_CONVERSION Layer 2 T4 architecture (hybrid kits feed this)
6. `reincarnated-engine/src/reincarnated/generation/season_generation_pipeline.py`:
   - Lines 434-446 `_BC_ATTRIBUTE_TO_ELEMENT` (RETIRE target)
   - Lines 463+ `_build_chain_specs` (Layer 3 chain assignment)
   - Lines 490/506/522 `ChainSpec.element` field (existing; reuse for Layer 3)
   - Lines 566+ `w5r1_generate_kit_candidates` (Layer 1 + Layer 2 logic)
   - Sub-fix 1 deepcopy at line 294 (Amendment 6 PRESERVE)
7. `reincarnated-engine/src/reincarnated/foundation/foundation.py:98` `get_rotating_elements()` — use to derive STAT_ELEMENT_POOLS at module load
8. Your `AGENT_STATE.md` at `reincarnated-engine/src/reincarnated/generation/AGENT_STATE.md` — Amendment 6 CLOSED checkpoint
9. `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Disc #1 + #2 + #11 + #41 + #42a + #45 LOAD-BEARING

---

## 2. Scope (Amendment 7 spec § 2)

### 2.1 Layer 1 — Retire `_BC_ATTRIBUTE_TO_ELEMENT` + implement STAT_ELEMENT_POOLS

At `season_generation_pipeline.py:434-446`:

**RETIRE:** Legacy `_BC_ATTRIBUTE_TO_ELEMENT` 1:1 table.

**IMPLEMENT:**

```python
STAT_ELEMENT_POOLS = {
    "INT": ["fire", "water", "lightning", "shadow"],
    "WIS": ["earth", "wind", "holy"],
    "STR": ["physical"],
    "DEX": ["fire", "water", "earth", "wind",
            "lightning", "holy", "shadow", "physical"],
}
```

**Cell-level draw:** for each BC cell, draw `N_SUBSTRATE_SAMPLES_PER_CELL = 3` elements WITHOUT REPLACEMENT from cell's eligible pool per `bc_attribute`. STR cells (pool size 1) yield 3× physical (degenerate; documented in spec § 2.1).

**Seeding:** `enc_seed + sample_idx * 17` (composes with Amendment 6 seed pattern).

### 2.2 Layer 2 — Hybrid promotion (17.5% per kit)

```python
HYBRID_RATE = 0.175  # 17.5% midpoint of 15-20% per Matt election
for sample_idx in range(N_SUBSTRATE_SAMPLES_PER_CELL):
    primary_element = layer_1_draw[sample_idx]
    is_hybrid = rng.random() < HYBRID_RATE
    if is_hybrid:
        secondary_pool = ALL_8_ELEMENTS - {primary_element}
        secondary_element = rng.choice(secondary_pool)
    else:
        secondary_element = None
```

Independent roll per kit. Expected hybrid count at 54 kits: 6-13 (95% CI for binomial(54, 0.175)).

### 2.3 Layer 3 — Chain element assignment

At `_build_chain_specs` (line 463+):

```python
if is_hybrid:
    chain_1.element       = primary_element     # PRIMARY identity
    chain_2.element       = secondary_element   # HYBRID chain
    supporting.element    = primary_element     # SUPPORT primary identity
else:  # MONO
    chain_1.element       = primary_element
    chain_2.element       = primary_element
    supporting.element    = primary_element
```

Uses existing `ChainSpec.element` field (no schema change at ChainSpec).

### 2.4 Schema additions

Add to `PlayerClass` (or KitCandidate per implementation knowledge):

```python
is_hybrid: bool = False
secondary_element: str | None = None
```

### 2.5 Telemetry capture (§ 3.3)

Telemetry exports `kit.is_hybrid` + `kit.secondary_element` per emitted kit for downstream Pareto-2 analysis + Phase 5 cohesion judge feedback + Cycle 14 wave-close empirical validation.

### 2.6 Composition verification with Amendment 6 (§ 7.4 acceptance criteria)

- Pareto-2 partition still works on `(BC_cell, cultural_lineage_canonical)`; Amendment 7's element variance does not break partition logic
- S7 deepcopy preserved (line 294); hybrid chain_2 element does not mutate adjacent kits via shared reference
- S8 Bound 4 paired-joint-sampling preserved; 54 skill-tree compositions per Amendment 6 spec

---

## 3. Pre-ratified contingent decisions (per Amendment 7 + Amendment 8)

| Decision point | Pre-ratified action |
|---|---|
| STAT_ELEMENT_POOLS derivation | Per canonical `elements.yaml` scales_with (substrate-led; foundation.py `get_rotating_elements()` invertible) |
| DEX pool composition | All 8 elements (Option C decouple per canonical `attribute-system-2026-05-24.md` § 2.1) |
| STR pool degenerate case | All 3 mirror copies physical; documented limitation (Cycle 15+ canonical-write candidate per § 9 spec) |
| Hybrid rate value | 0.175 (17.5% midpoint of 15-20% per Matt election) |
| Hybrid roll independence | Per sample (cell-by-cell variance OK) |
| Schema field placement | Rocket elects per simpler-implementation (PlayerClass OR KitCandidate per dataclass conventions) |
| Element vocabulary lock (Disc #45) | Canonical `elements.yaml` names verbatim |

---

## 4. Acceptance criteria (Amendment 7 § 7)

### 4.1 Layer 1 verification

- All 18 BC cells × 3 mirrors = 54 kits emitted
- INT cell: 3 distinct elements from {fire, water, lightning, shadow}
- WIS cell: 3 distinct elements = full {earth, wind, holy} pool
- STR cell: 3× physical (mono pool)
- DEX cell: 3 distinct elements from 8-element foundation pool
- Population element coverage: all 8 elements ≥1 kit at primary-mono layer

### 4.2 Layer 2 verification

- Hybrid rate at 54-kit population: 6-13 hybrid kits (95% CI binomial(54, 0.175))
- Hybrid roll independence: cell-by-cell variance
- Hybrid secondary element distribution: all 8 elements appear as secondary at chain-level across population

### 4.3 Layer 3 verification

- Mono kit: chain_1 = chain_2 = supporting = kit.element
- Hybrid kit: chain_1 = supporting = primary; chain_2 = secondary; primary ≠ secondary
- Schema: `kit.is_hybrid` matches Layer 2 roll; `kit.secondary_element` non-None only for hybrid kits

### 4.4 Amendment 6 composition preserved

- Pareto-2 partition still emits archives (per Sub-fix 2)
- S7 deepcopy preserved (per Sub-fix 1)
- S8 Bound 4 paired-joint-sampling preserved (per Sub-fix 3); 54 skill-tree compositions

### 4.5 Smoke + tests + tag

- Smoke test: Phase 2-4 fire (smoke=False; small sample 3-5 BC cells) end-to-end PASS; HALT at Phase 5 entry NOT applicable per Amendment 8 (no Matt-gate); rocket can use Amendment 6's `halt_at_phase=5` mechanism for smoke if convenient
- All existing tests PASS (no regression beyond pre-existing failures)
- New tests for Layer 1 + Layer 2 + Layer 3 + composition
- Engine commit + tag (rocket prefix per CLAUDE.md: e.g., `rocket/v1.0-cascade-r3-amendment-7-element-coverage-e4c-1`)

---

## 5. Out-of-scope

- jack-ryan Gate-2 Pattern E review (KR fires post-rocket close)
- Full-scale production S6c re-fire (KR scope post-Gate-2)
- Matt-gate at Phase 5 entry (RETIRED per Amendment 8)
- Phase 5+ continuation (cascade auto-fires post-Gate-2 per Amendment 8)
- Amendment 6 mechanical changes (preserved; PASS-with-INFO per Gate-2 review)
- LLM prompt template modifications (gandalf seam)
- Phase 7 mechanical gate modifications (gamora seam; CLOSED)
- A/B comparison protocol
- Cycle 15+ flags (STR pool expansion / DEX Cycle 15+ revisit / hybrid rate calibration / multi-element E3 full decouple / `_BC_ATTRIBUTE_TO_ELEMENT` retirement record)

---

## 6. Surface to knight-rider conditions

| Condition | Trigger | Action |
|---|---|---|
| **STAT_ELEMENT_POOLS canonical drift** | `elements.yaml` scales_with mapping inconsistent with canonical doc 47 OR foundation.py `get_rotating_elements()` returns unexpected list | Halt + surface to KR — gandalf canonical reconciliation |
| **Amendment 6 composition broken** | § 4.4 verification fails (Pareto-2 / S7 / S8 Bound 4 regressed) | Halt + surface to KR — Amendment 6 regression |
| **Element coverage < 8 at population** | Any element at 0% post-fix | Halt + surface to KR — STAT_ELEMENT_POOLS misconfigured OR sampling logic bug |
| **Hybrid rate outside 6-13 95% CI** | Sample produces <6 OR >13 hybrid kits | Document; surface to KR for analysis (RNG variance OR sampling logic bug) |
| **Disc #42a framing-audit catch** | Q1-Q6 surfaces pre-imposed assumption | Halt + surface to KR |
| **Schema field consumer breakage** | Adding `is_hybrid` + `secondary_element` breaks downstream consumers (LLM prompts / archive / etc.) | Surface to KR — coordinate with star-lord / gandalf |
| **Effort exceeds ~3h** | Implementation significantly beyond ~1-2h estimate | Surface to KR — scope reconsideration |

---

## 7. Engineering disciplines composition

| Discipline | Application |
|---|---|
| **Disc #1 math-before-code** | Layer 1 sampling math (N=3 without replacement from variable pool sizes); Layer 2 hybrid binomial(54, 0.175) expected count — math note recommended at `generation/notes/cascade-r3-amendment-7-element-coverage-math-2026-05-29.md` |
| **Disc #2 smoke-test before tag** | § 4.5 smoke gate |
| **Disc #11 empirical inspection** | § 4.1-4.4 acceptance gates |
| **Disc #41 substrate-led vocabulary lock** | LOAD-BEARING — STAT_ELEMENT_POOLS derived from canonical `elements.yaml` scales_with (substrate-declared coupling, NOT pre-imposed mapping); legacy `_BC_ATTRIBUTE_TO_ELEMENT` retirement closes canonical-engine drift |
| **Disc #42a framing-audit Q1-Q6** | LOAD-BEARING — Amendment 7 IS the framing-audit catch (4-of-8 element coverage gap caught pre-fire per Amendment 8 discipline composition) |
| **Disc #45 vocabulary lock** | Element vocabulary locked at canonical names; hybrid vocabulary "primary"/"secondary" locked at PlayerClass schema |
| **Disc #48 RETIRED per Amendment 3** | No pre-flight vm_stat gate |
| **Pattern E autonomous-pair pre-authorization** | Applies at jack-ryan Gate-2 post-rocket; PASS/WARN/INFO fire-and-continue per Phase A1 closure + Amendment 5/8 |
| **Recognition → empirical validation → commit** | Recognition: 4-of-8 coverage gap; Validation: § 4 acceptance gates + S6c re-fire population verification; Commit: rocket auto-commits per CLAUDE.md addendum |

---

## 8. Deliverables

1. **Engine commit(s)** — season_generation_pipeline.py (STAT_ELEMENT_POOLS + Layer 1/2/3) + schema (is_hybrid + secondary_element) + tests + tag (rocket prefix per CLAUDE.md)
2. **Math note** (if applicable) at `reincarnated-engine/src/reincarnated/generation/notes/cascade-r3-amendment-7-element-coverage-math-2026-05-29.md` (Disc #1)
3. **MIGRATION.md entry** — schema additions (is_hybrid + secondary_element) may have downstream consumer impact (LLM prompts can opt-in to hybrid metadata); cross-seam awareness for star-lord (Phase 5 prompts) + gamora (Phase 7 verdict) + gandalf (canonical doc reconciliation if any)
4. **Completion record appended to this dispatch file** — captures: (a) Layer 1 retirement + STAT_ELEMENT_POOLS + element coverage evidence; (b) Layer 2 hybrid rate evidence; (c) Layer 3 chain assignment evidence; (d) Amendment 6 composition verification per § 4.4; (e) smoke test results; (f) any surface-to-KR findings
5. **AGENT_STATE.md checkpoint** at `reincarnated-engine/src/reincarnated/generation/AGENT_STATE.md` — Amendment 7 CLOSED + jack-ryan Gate-2 queued + cascade re-fire queued
6. **Auto-commit per CLAUDE.md team commit + push discipline addendum 2026-05-25** — work-products of authorized cascade-resumption-3 work; push REQUIRES Matt-explicit-auth (do NOT push)

---

## 9. Sign-off

**Authored:** knight-rider per Matt 2026-05-29 evening late "confirmed, fire amendment 7" + Amendment 8 (Matt-gate retired; KR auto-routes per hive-mind decision-routing under $50 cap monitoring) + gandalf Amendment 7 spec

**Rocket session-start protocol:**
1. Onboard via § 1 required first reads (especially Amendment 7 spec + Amendment 8 header + canonical `elements.yaml`)
2. Apply Disc #42a framing-audit Q1-Q6 at dispatch consumption — Instance 6 awareness LOAD-BEARING (verify implementation claims match empirical behavior post-each-layer)
3. Author § 2.1 math note BEFORE code if applicable (Disc #1)
4. Execute § 2 scope SEQUENTIALLY: Layer 1 → Layer 2 → Layer 3 → schema → telemetry → composition verification
5. Apply § 4 acceptance gates per layer
6. Surface per § 6 if triggered — auto-route in-scope per hive-mind decision-routing
7. Author § 8 deliverables
8. Auto-commit per CLAUDE.md addendum

**KR next-step on rocket close:**
1. Fire jack-ryan Gate-2 Pattern E review of Amendment 7 (composition verification + § 7 acceptance criteria)
2. Per Gate-2 PASS/WARN/INFO → re-fire S6c production cascade Phase 2-4 → Phase 5 → Phase 7 (NO Matt-gate per Amendment 8)
3. KR monitors $50 cost cap during Phase 5; surface at ~75-80% approach OR breach (mandatory)
4. Continue cascade A2-2 → A2-7 + D13 parallel-fire per existing Phase A2 sequence

**Cascade trajectory:** Amendment 7 → jack-ryan Gate-2 → S6c production cascade (no Matt-gate; $50 cap monitoring) → A2-2 → A2-3 → A2-4 → A2-5 → A2-6 → A2-7 + D13 parallel → Cycle 14 v1 MVP D9 close.

**Signed:** knight-rider (orchestrator)

---

## Completion record

**Completed by:** rocket
**Date:** 2026-05-29
**Engine commit:** 8d5be1b, tag `rocket/v1.0-cascade-r3-amendment-7-element-coverage-1`
**Math note:** `src/reincarnated/generation/notes/cascade-r3-amendment-7-element-coverage-math-2026-05-29.md`
**MIGRATION.md entry:** `src/reincarnated/generation/MIGRATION.md` § [2026-05-29] Amendment 7
**AGENT_STATE.md:** updated — Amendment 7 CLOSED checkpoint appended
**Tests:** 49 new Amendment 7 tests + 554 total PASS

### (a) Layer 1 retirement + STAT_ELEMENT_POOLS + element coverage

`_BC_ATTRIBUTE_TO_ELEMENT` 1:1 table RETIRED. `STAT_ELEMENT_POOLS` active per canonical `elements.yaml` `scales_with` inversion:
- INT → {fire, water, lightning, shadow} (4-pool)
- WIS → {earth, wind, holy} (3-pool; full pool coverage per cell)
- STR → {physical} (1-pool; degenerate; 3× physical)
- DEX → all 8 elements (Option C decouple; attribute-system-2026-05-24.md § 2.1)

`_draw_cell_elements(bc_attribute, enc_seed, n_samples)`: N=3 draws WITHOUT REPLACEMENT via `random.Random(enc_seed + 17).sample(pool, k=3)`. STR degenerate: `[pool[0]] * 3`.

Smoke evidence (seed_base=14001, 54 kits): all 8 elements present at primary layer. Element distribution:
`earth:9, fire:6, holy:6, lightning:6, physical:13, shadow:4, water:4, wind:6`. Missing: [] (empty).

INT kits cover all 4-pool elements; WIS kits cover full 3-pool per cell; STR=physical; DEX covers all 8 across cells.

### (b) Layer 2 hybrid rate evidence

HYBRID_RATE = 0.175. `_roll_hybrid(primary, enc_seed, sample_idx)` seeded `enc_seed + sample_idx * 17 + 1`.

Smoke result: **12 hybrid of 54 kits** (within 95% CI [6-13] PASS). Hybrid roll independence verified (cell-by-cell variance present). All is_hybrid + secondary_element field consistency checks PASS.

### (c) Layer 3 chain assignment evidence

`_build_chain_specs` updated with `primary_element`, `is_hybrid`, `secondary_element` args:
- Mono: chain_1 = chain_2 = supporting = primary_element (VERIFIED at smoke)
- Hybrid: chain_1 = supporting = primary; chain_2 = secondary; primary ≠ secondary (VERIFIED at smoke)

Sample hybrid chain: primary=physical → chain_1=physical, chain_2=wind, supporting=physical.
No ChainSpec schema change; existing `ChainSpec.element` field reused.

### (d) Schema additions

KitCandidate.is_hybrid + secondary_element: present, default False/None, correctly populated at w5r1_generate_kit_candidates.
PlayerClass.is_hybrid + secondary_element: present, default False/None, propagated via _build_real_player_class.
to_character_dict(): serializes both fields. Confirmed via `d["is_hybrid"]` + `d["secondary_element"]` present.

### (e) Amendment 6 composition verification (§ 4.4)

| Fix | Status |
|---|---|
| Pareto-2 partition key (bc_cell_id, cultural_lineage_canonical) unchanged | PASS — element not added to partition key |
| S7 deepcopy in to_character_dict() | PASS — deepcopy still present; hybrid secondary_element on KitCandidate (not gear_set mutation) |
| S8 Bound 4 paired-joint-sampling 54 kits | PASS — 54 kits generated at smoke |

### (f) Smoke test results

Phase 2 (w5r1_generate_kit_candidates): 54 kits, all acceptance gates PASS.
Phase 2-4 end-to-end (wave5_season_orchestrator, halt_at_phase=5): PASS.
Tests: 554 PASS (49 new Amendment 7 + 505 pre-existing; 0 regressions).

### (g) Surface-to-KR findings

None. No § 6 triggers fired:
- STAT_ELEMENT_POOLS correctly derived from elements.yaml (no canonical drift)
- Amendment 6 composition preserved (no regression)
- All 8 elements present at population (none at 0%)
- Hybrid count 12/54 within [6-13] CI
- No Disc #42a framing-audit catch (implementation matches empirical behavior)
- No schema consumer breakage (defaults backward-compatible)
- Effort: ~1.5h wall-clock (within 1-2h estimate)

**KR next step:** fire jack-ryan Gate-2 Pattern E review of Amendment 7. Per PASS/WARN/INFO → re-fire S6c production cascade Phase 5+ per Amendment 8 (no Matt-gate; KR monitors $50 cap).
