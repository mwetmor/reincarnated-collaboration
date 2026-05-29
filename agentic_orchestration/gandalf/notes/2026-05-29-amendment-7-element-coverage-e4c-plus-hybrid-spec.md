# Amendment 7 Spec — Element Coverage E4c + Hybrid Layer

> **STATUS:** CURRENT — Cycle 14 cascade-resumption-3 Amendment 7 spec. Authored by gandalf 2026-05-29 evening late per Matt election. Fires in parallel with Amendment 6 (path α) — KR coordinates bundled rocket dispatch.
>
> **Composes with:** Amendment 6 (S7 deepcopy + Pareto-2 + S8 Bound 4 paired-joint-sampling). Amendment 7 layers on top of Amendment 6's multi-sample structure; the two amendments are mechanically independent and can fire as one rocket dispatch or two — KR's call.

**Date:** 2026-05-29 evening late
**Author:** gandalf (story-and-design steward)
**Authorized:** Matt 2026-05-29 evening late ("confirmed, fire amendment 7" verbatim)
**Composition:** Amendment 6 path α parallel; Cycle 14 wave-5 cascade-resumption-3

---

## 0. TL;DR

Reincarnated foundation declares 7 rotating substrates (fire, water, earth, wind, lightning, holy, shadow) + 1 non-rotating (physical) per D5 LC-012 fix (2026-05-21). Current generation pipeline `_BC_ATTRIBUTE_TO_ELEMENT` maps STR→earth / DEX→wind / INT→fire / WIS→water (1:1 hardcoded), reaching only 4 of 8 elements at gauntlet output. **Amendment 7 replaces this with the canonical scales_with mapping per `elements.yaml` + hybrid promotion at 17.5% per kit**, reaching all 8 elements at population-level coverage.

**Headline change:** Cycle 14 v1 gauntlet output spans 8 elements at population level + chain-level element diversity at hybrid layer.

---

## 1. Problem statement (empirical surface)

### 1.1 Pre-Amendment-7 element coverage

`season_generation_pipeline.py:434-470` infers kit element via `_BC_ATTRIBUTE_TO_ELEMENT` 1:1 mapping. Catalog distribution (per `endgame_encounter_catalog.py`):

| bc_attribute | Cells | _BC_ATTRIBUTE_TO_ELEMENT mapping | Kits per Amendment 6 (3 samples) |
|---|---|---|---|
| STR | 4 | earth | 12 |
| DEX | 4 | wind | 12 |
| INT | 5 | fire | 15 |
| WIS | 5 | water | 15 |

**Pre-Amendment-7 population element distribution (54 kits):**
| Element | Kits | % |
|---|---|---|
| fire | 15 | 28% |
| water | 15 | 28% |
| earth | 12 | 22% |
| wind | 12 | 22% |
| **lightning** | **0** | **0%** ❌ |
| **holy** | **0** | **0%** ❌ |
| **shadow** | **0** | **0%** ❌ |
| **physical** | **0** | **0%** ❌ |

**4 of 8 elements unreachable** under current generation. The foundation's 7-rotating-substrate expansion is declared but not exercised.

### 1.2 Also: legacy mapping is OUT OF SYNC with canonical scales_with

`config/elements.yaml` declares the canonical stat-element coupling via the `scales_with` field:

| Element | scales_with | Inverted (stat → eligible elements) |
|---|---|---|
| fire | intelligence | INT → {fire, water, lightning, shadow} |
| water | intelligence | (same) |
| lightning | intelligence | (same) |
| shadow | intelligence | (same) |
| earth | wisdom | WIS → {earth, wind, holy} |
| wind | wisdom | (same) |
| holy | wisdom | (same) |
| physical | strength | STR → {physical} |
| — | — | DEX → (no element scales_with DEX; canonical disposition Option C decouple) |

**Legacy `_BC_ATTRIBUTE_TO_ELEMENT` does NOT match canonical scales_with:**
- STR mapped to earth (canonical: physical)
- DEX mapped to wind (canonical: nothing per Option C decouple)
- INT mapped to fire only (canonical: 4 elements eligible)
- WIS mapped to water only (canonical: nothing — water scales with INT)

Amendment 7 corrects the canonical-engine drift AND expands element coverage in the same operation.

### 1.3 Canonical doc disposition for DEX

`canonical/story/attribute-system-2026-05-24.md` § 2.1 deliberated DEX-element coupling and **gandalf-lean recommendation Option C: DEX as weapon-property attribute, decoupled from element-system.** Amendment 7 operationalizes Option C for Cycle 14 v1 — DEX cells sample from the full 8-element foundation pool (since DEX is element-agnostic at the canonical scaling layer).

---

## 2. Amendment 7 mechanism (3 layers)

### Layer 1 — Cell-level element selection (per canonical scales_with)

**Per BC cell**, determine the eligible element pool from the inverted canonical scales_with mapping:

```python
STAT_ELEMENT_POOLS = {
    "INT": ["fire", "water", "lightning", "shadow"],   # 4 elements
    "WIS": ["earth", "wind", "holy"],                    # 3 elements
    "STR": ["physical"],                                 # 1 element
    "DEX": ["fire", "water", "earth", "wind",            # 8 elements (Option C decouple)
            "lightning", "holy", "shadow", "physical"],
}
```

**Per BC cell, draw `N_SUBSTRATE_SAMPLES_PER_CELL` (=3 per Amendment 6) elements WITHOUT REPLACEMENT** from the eligible pool:
- INT cell (pool size 4): 3 distinct elements drawn from 4 — variance guaranteed
- WIS cell (pool size 3): 3 distinct elements drawn from 3 — covers entire WIS pool exactly
- STR cell (pool size 1): with replacement (or all 3 same — `[physical, physical, physical]`)
- DEX cell (pool size 8): 3 distinct elements drawn from 8 — high variance

**STR cells degenerate case:** pool size 1 forces all 3 mirror copies to physical. Documented limitation; alleviated partially by Layer 2 hybrid (some STR kits become hybrid with non-physical secondary).

**Seeding:** `enc_seed + sample_idx * 17` (composes with existing Amendment 6 seed pattern).

### Layer 2 — Hybrid promotion (17.5% per kit)

For each of the 3 mirror samples per cell, roll a hybrid promotion gate **independently**:

```python
HYBRID_RATE = 0.175  # 17.5% midpoint of 15-20% range per Matt election
for sample_idx in range(N_SUBSTRATE_SAMPLES_PER_CELL):
    primary_element = layer_1_draw[sample_idx]
    is_hybrid = rng.random() < HYBRID_RATE
    if is_hybrid:
        # Secondary draws from FULL 8-element foundation pool, excluding primary
        secondary_pool = ALL_8_ELEMENTS - {primary_element}
        secondary_element = rng.choice(secondary_pool)
    else:
        secondary_element = None
```

**Hybrid rate independent per kit** — a single BC cell might produce 0, 1, 2, or all 3 hybrid mirrors. Expected hybrid rate at population level: ~9-10 of 54 kits (~17.5%).

### Layer 3 — Chain assignment (where hybrid lives mechanically)

Using the existing `ChainSpec.element` field (already declared at `season_generation_pipeline.py:490/506/522` but currently hardcoded to share `kit.element`):

```python
if is_hybrid:
    chain_1.element       = primary_element     # PRIMARY (preserves identity)
    chain_2.element       = secondary_element   # HYBRID chain
    supporting.element    = primary_element     # SUPPORTS primary identity
else:  # MONO
    chain_1.element       = primary_element
    chain_2.element       = primary_element
    supporting.element    = primary_element
```

**Rationale for chain assignment pattern:**
- chain_1 anchors primary element identity (kit.element for archetype_tag + cohesion judge + ailment signature)
- chain_2 = hybrid chain — natural surface for ELEMENT_CONVERSION Layer 2 T4 strategy (canonical doc 47 § 4.6) to operate on
- supporting_chain preserves primary identity (class-identity passive layer)

---

## 3. Schema extensions

### 3.1 PlayerClass (kit) schema additions

Add to `PlayerClass` dataclass / kit construction:

```python
@dataclass
class PlayerClass:
    # ... existing fields ...
    element: str                              # PRIMARY element (existing; semantics unchanged)
    is_hybrid: bool = False                   # NEW: hybrid promotion flag
    secondary_element: str | None = None      # NEW: hybrid kit's chain_2 element; None for mono kits
```

**Downstream consumption:**
- `kit.element` continues to drive `archetype_tag` (line 1173) + cohesion judge + ailment signature for mono kits
- For hybrid kits: `archetype_tag` still uses `kit.element` (primary); downstream consumers can opt-in to hybrid-aware logic via `kit.is_hybrid` flag
- LLM Phase 5 prompts can include hybrid metadata (Wave A `element_distribution` + Wave B `kit.secondary_element` if hybrid)

### 3.2 ChainSpec field semantics (no schema change; existing field reused)

`ChainSpec.element` field already exists but currently hardcoded to share `kit.element`. Amendment 7 USES the existing field to carry per-chain element variance for hybrid kits. **No ChainSpec schema change required.**

### 3.3 Telemetry capture

Telemetry should capture `kit.is_hybrid` and `kit.secondary_element` per emitted kit for downstream Pareto-2 analysis + Phase 5 cohesion judge feedback + Cycle 14 wave-close empirical validation of hybrid rate calibration.

---

## 4. Implementation file references

| File | Change |
|---|---|
| `reincarnated-engine/src/reincarnated/generation/season_generation_pipeline.py` | Layer 1 + Layer 2 + Layer 3 logic in `w5r1_generate_kit_candidates` (line 566+) + `_build_chain_specs` (line 463+) refactor |
| `reincarnated-engine/src/reincarnated/generation/season_generation_pipeline.py:434-446` | RETIRE `_BC_ATTRIBUTE_TO_ELEMENT` legacy table; REPLACE with `STAT_ELEMENT_POOLS` per canonical scales_with |
| `reincarnated-engine/src/reincarnated/generation/season_generation_pipeline.py` (or appropriate kit model file) | Add `is_hybrid: bool` + `secondary_element: str \| None` to PlayerClass / KitCandidate |
| `reincarnated-engine/config/elements.yaml` | No change (canonical scales_with mapping is the source of truth) |
| `reincarnated-engine/src/reincarnated/foundation/foundation.py:98` | `get_rotating_elements()` already exists; use to derive STAT_ELEMENT_POOLS via inversion at module load |
| Telemetry export schema | Add hybrid fields per § 3.3 |

---

## 5. Population effect prediction

**Per-stat element coverage** (54 kits at 17.5% hybrid):

| Stat | Cells | Mirrors | Pool size | Mono kits | Hybrid kits | Element variance per cell |
|---|---|---|---|---|---|---|
| INT | 5 | 15 | 4 | ~12-13 | ~2-3 | 3 of 4 distinct per cell |
| WIS | 5 | 15 | 3 | ~12-13 | ~2-3 | 3 of 3 distinct per cell (covers pool) |
| STR | 4 | 12 | 1 | ~10 | ~2 | None (pool size 1; degenerate) |
| DEX (Option C) | 4 | 12 | 8 | ~10 | ~2 | 3 of 8 distinct per cell |

**Population-level element appearance count (primary + secondary chain-level):**

| Element | Mono kits as primary | Hybrid kits as secondary | **Total chain-level appearances** |
|---|---|---|---|
| fire | ~4 | ~1-2 | ~5-6 |
| water | ~4 | ~1-2 | ~5-6 |
| lightning | ~4 | ~1-2 | ~5-6 |
| shadow | ~4 | ~1-2 | ~5-6 |
| earth | ~5 | ~1-2 | ~6-7 |
| wind | ~5 | ~1-2 | ~6-7 |
| holy | ~5 | ~1-2 | ~6-7 |
| physical | ~10-11 | ~1-2 | ~11-13 |

**All 8 elements have presence at both primary-mono layer AND hybrid-secondary layer.** Distribution non-uniform (physical over-represented due to STR pool size 1 + DEX Option C contribution + STR hybrid secondary contributions) but no element is at zero.

---

## 6. Composition with existing canon + Amendment 6

### 6.1 Composition with Amendment 6 (path α parallel)

Amendment 6 introduces:
- S7 deepcopy fix (multi-sample independent kits per cell)
- Pareto-2 partition on (BC_cell, cultural_lineage_canonical)
- S8 Bound 4 paired-joint-sampling for skill tree (54 compositions)

Amendment 7 introduces:
- Element selection per canonical scales_with
- 17.5% hybrid promotion
- chain_2.element variance for hybrid kits

**Composition is clean:** Amendment 6's multi-sample structure is the substrate Amendment 7's per-sample element variance operates on. The two amendments are mechanically independent and can fire as one rocket dispatch or two — KR's call. Recommended: single combined rocket dispatch for atomicity.

### 6.2 Composition with canonical doc 47 § 4.6 (two-layer T4 architecture)

Layer 2 T4 cycles through 6 mechanical strategies including 3 ELEMENT_CONVERSION variants. Hybrid kits at Amendment 7 layer (kit-side element-pair surface) are the natural input to ELEMENT_CONVERSION Layer 2 T4 strategy (engine-side mechanical surface).

**Predicted post-Amendment-7 ELEMENT_CONVERSION fire pattern:**
- Mono kits (~82.5%): ELEMENT_CONVERSION fires rarely; Layer 2 T4 selects DIRECT_DAMAGE_AMPLIFICATION / GEOMETRY_COLLAPSE / RESOURCE_CONVERSION
- Hybrid kits (~17.5%): ELEMENT_CONVERSION fires more frequently at Layer 2 T4 (variants A/B/C per primary→secondary conversion)

**Empirical observation post-A2-1 RE-FIRE-3** will validate this prediction.

### 6.3 Composition with `canonical/story/attribute-system-2026-05-24.md`

Amendment 7 § 2.1 Layer 1 STAT_ELEMENT_POOLS operationalizes the canonical scales_with table at § 2 of that doc. DEX disposition Option C is operationalized at the implementation layer (decouple DEX from element-pool restriction; sample from full 8-element foundation).

**Canonical doc 47 § 4.5 v1.2 ELEMENT_CONVERSION variants:** Variant A (1.50×) / Variant B (1.25×) / Variant C (0.25 additive + ailment) are the engine-side mechanical realization of hybrid kits. Amendment 7 generates the kit-side surface; Layer 2 T4 selection at Phase 5+ realizes the mechanic.

### 6.4 No impact on canonical scope these amendments do NOT touch

- Pre-A2-1 cascade architecture mechanics (Phase 2-7 structurally unchanged beyond Layer 3 chain.element variance)
- Cohesion judge architecture (operates on kit.element + kit.is_hybrid; hybrid-aware logic optional)
- Pareto-2 partition (unchanged — partitions on (BC_cell, cultural_lineage_canonical); element variance within partition is captured by Pareto archive ranking)
- LLM prompt templates (additive metadata only — Wave A `element_distribution` includes 8 elements rather than 4; Wave B optional `kit.secondary_element` field)
- Class taxonomy eradication (Amendment 6 base; Amendment 7 orthogonal)

---

## 7. Test acceptance criteria

### 7.1 Layer 1 verification (cell-level element selection)

| Test | Expected output |
|---|---|
| All 18 BC cells × 3 mirrors = 54 kits generate | 54 kit candidates emitted |
| INT cell element distribution | Each INT cell has 3 distinct elements from {fire, water, lightning, shadow} |
| WIS cell element distribution | Each WIS cell has 3 distinct elements = full {earth, wind, holy} pool |
| STR cell element distribution | Each STR cell has 3 × physical (mono pool) |
| DEX cell element distribution | Each DEX cell has 3 distinct elements from 8-element foundation pool |
| Population element coverage | All 8 elements have ≥1 kit at primary-mono layer |

### 7.2 Layer 2 verification (hybrid rate)

| Test | Expected output |
|---|---|
| Hybrid rate at 54-kit population | 6-13 hybrid kits (95% CI for binomial(54, 0.175)) |
| Hybrid roll independence | Cell-by-cell variance in hybrid kit count (some cells 0 hybrid, some 1-2-3) |
| Hybrid secondary element distribution | All 8 elements appear as secondary at chain-level across population |

### 7.3 Layer 3 verification (chain assignment)

| Test | Expected output |
|---|---|
| Mono kit chain elements | chain_1 = chain_2 = supporting = kit.element |
| Hybrid kit chain elements | chain_1 = supporting = primary; chain_2 = secondary; primary ≠ secondary |
| Schema field population | `kit.is_hybrid` matches Layer 2 roll; `kit.secondary_element` non-None only for hybrid kits |

### 7.4 Composition with Amendment 6 verification

| Test | Expected output |
|---|---|
| Pareto-2 partition still works | (BC_cell, cultural_lineage_canonical) partition emits archives; Amendment 7's element variance does not break partition logic |
| S7 deepcopy preserved | Hybrid kit's chain_2 element does not mutate adjacent kits via shared reference (re-test Amendment 6's S7 fix scope) |
| S8 Bound 4 paired-joint-sampling preserved | 54 skill-tree compositions still generated per Amendment 6 spec |

---

## 8. Discipline composition

| Discipline | Application |
|---|---|
| **Disc #41 substrate-led discipline** | Element pools derived from canonical `elements.yaml` scales_with field — substrate-declared coupling, not pre-imposed mapping. Legacy `_BC_ATTRIBUTE_TO_ELEMENT` retired (engine-side drift from canonical). |
| **Disc #42a framing-audit (Q1-Q6)** | Framing-audit caught the 4-of-8 element coverage gap that the cascade-resumption-3 work scope did not initially surface. Cycle 14 v1 ships with 8-element coverage rather than 4-element. |
| **Disc #18 math hotspot consultation** | Amendment 7 mechanism finalized through gandalf-Matt design call (single-session); no separate methodology consultation needed (canonical scales_with mapping is the source of truth; Option C disposition documented in attribute-system-2026-05-24.md). |
| **Disc #19 background processes** | Amendment 7 fires as parallel rocket dispatch alongside Amendment 6 per path α; no resource conflict (rocket-only operation). |
| **Disc #45 vocabulary lock** | Element vocabulary locked at canonical `elements.yaml` names (fire/water/earth/wind/lightning/holy/shadow/physical); hybrid vocabulary "primary"/"secondary" element locked at PlayerClass schema layer. |
| **Recognition → empirical validation → commit** | Amendment 7 hybrid rate (17.5% midpoint) is the empirical-validation instrument. Cycle 14 wave-close + Cycle 15+ empirical observation feeds rate calibration; canonical-write candidates queued (STR pool expansion; DEX disposition Cycle 15+ revisit). |

---

## 9. Cycle 14 wave-close canonical-write candidates surfaced

Amendment 7 implementation closes element-coverage for Cycle 14 v1 but surfaces several Cycle 15+ canonical-write candidates:

1. **STR pool expansion candidate** — STR mono-physical (pool size 1) means 12 STR kits all share physical element. Genre canon supports STR-fire-warrior, STR-shadow-knight, STR-holy-paladin patterns. Cycle 15+ canonical write may expand STR pool beyond physical via canonical scales_with secondary mapping (e.g., physical + ??? elements where STR is secondary scaling).
2. **DEX disposition Cycle 15+ revisit** — Option C decouple operationalized for Cycle 14. Empirical observation of DEX cell element coverage feeds Option A (DEX↔physical co-eligible) vs Option B (DEX↔wind co-eligible) vs Option C (full decouple) re-deliberation post-Cycle 14.
3. **Hybrid rate calibration** — 17.5% midpoint is the Cycle 14 v1 anchor. Empirical observation of hybrid kit performance + Pareto archive composition + cohesion judge naming + player-facing surface feeds Cycle 15+ rate adjustment.
4. **Multi-element kit architecture (E3 full decouple)** — Amendment 7 maintains kit.element as single primary; chain_2 hybrid is the only multi-element surface. Cycle 15+ canonical write may explore full element decouple (E3 from authorization spec) where each chain independently samples element.
5. **`_BC_ATTRIBUTE_TO_ELEMENT` legacy retirement record** — drift between engine generation pipeline (legacy table) and canonical `elements.yaml` scales_with (canonical truth) surfaced. Amendment 7 retires the legacy table. Discipline candidate: canonical-engine drift detection at jack-ryan canonical write.

---

## 10. KR routing instructions

**Recommended bundling:**
- Single rocket dispatch combining Amendment 6 + Amendment 7 scope (atomic close + single Gate-2 check; recommended)
- OR two parallel rocket dispatches (Amendment 6 + Amendment 7 independent) per KR's dependency-graph judgment

**Dependency graph:**
- Amendment 7 depends on Amendment 6's S7 multi-sample structure being implemented (`N_SUBSTRATE_SAMPLES_PER_CELL = 3` cycle structure)
- Amendment 6 does NOT depend on Amendment 7
- Therefore: Amendment 6 must implement first OR concurrently; Amendment 7 layers on top

**Path α (parallel concurrent):** rocket implements both in one dispatch as integrated work. Total estimate: ~6-8h rocket work (Amendment 6 ~5-6h + Amendment 7 ~1-2h additive).

**Path β (sequential):** Amendment 6 ships first; Amendment 7 fires after Amendment 6 lands. Rejected per Matt election in favor of path α.

**Pre-fire empirical-verification gate (Amendment 5):** at Phase 5 entry of re-fired cascade, Matt-gate fires with form counts + per-cohort + per-lineage + per-ELEMENT distribution (NEW: 8-element coverage verification per Amendment 7 acceptance) + cost projection. Matt elects RATIFY-FIRE / REDUCE-SCOPE / ABORT per Amendment 5 § 5.

---

## 11. Sign-off

**Authored:** gandalf (story-and-design steward) per gandalf-Matt design call 2026-05-29 evening late
**Election authority:** Matt 2026-05-29 evening late ("confirmed, fire amendment 7" verbatim)
**Composition:** Amendment 6 path α parallel; cascade-resumption-3 work program

**For KR:** route Amendment 7 to rocket as parallel-path-α dispatch (bundled with Amendment 6 recommended). Reference this spec at dispatch prompt. Amendment 7 acceptance criteria § 7 must pass at jack-ryan Gate-2 before A2-1 RE-FIRE-3 commitment.

**For rocket:** retire legacy `_BC_ATTRIBUTE_TO_ELEMENT` table; implement STAT_ELEMENT_POOLS per § 2 Layer 1; implement hybrid promotion per § 2 Layer 2; implement chain assignment per § 2 Layer 3; add schema fields per § 3; pass acceptance criteria § 7.

**For jack-ryan Gate-2:** verify acceptance criteria § 7.1-7.4 all pass; verify canonical scales_with mapping operationalized (not new designer-imposed pool); verify Amendment 6 composition does not break (S7 deepcopy + Pareto-2 + S8 Bound 4 paired-joint-sampling preserved).

**For Matt (Phase 5 entry gate per Amendment 5):** empirical-verification gate surface includes per-element distribution at primary-mono + chain-level (8-element coverage acceptance). RATIFY-FIRE if 8 elements present; REDUCE-SCOPE if any element at zero; ABORT if architectural concern surfaces.
