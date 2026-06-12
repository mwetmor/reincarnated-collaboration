# Gap-Register Architecture-Fit Audit — Generation Seam (Fable-5 WRAP Refutation Test)

**STATUS:** CURRENT — read-only architecture-fit audit; no production code modified
**Date:** 2026-06-11
**Author:** rocket (engine content-generation seam owner)
**Commission:** gandalf, Matt-authorized this session. The 2026-06-10 WRAP verdict (`canonical/story/2026-06-10-engine-greenfield-verdict-wrap-and-extend.md`) measured throughput/cost only; it did NOT measure design-architecture divergence against the cemented future-state (atomic-substrate-registry + hypothesis-flow). This audit is the cheapest refutation test on that unmeasured axis.
**Instrument:** EXTENDS-CLEANLY (new code against existing interfaces; no structural change) / EXTENDS-WITH-FRICTION (workable but awkward adapters or local refactors) / FIGHTS-THE-ARCHITECTURE (against the grain; module rebuild cheaper).
**Sources read in full:** atomic-substrate-registry (2026-06-06); hypothesis-flow Phase A-E (2026-05-31, § 5.2); canonical-synthesis § 9 gap register (2026-06-10); my 2026-06-10 throughput consult.
**Method:** empirical code inspection of `generation/`, `element/`, `anchor/`, `foundation/`, `canonical/` (Discipline #11). File/function citations on every classification.

---

## 0. Verdict headline (read this first)

**WRAP-WITH-TARGETED-REBUILDS — but the rebuilds are SMALL and LOCAL, not whole-module.**

The cemented future-state architecture **EXTENDS** the current generation seam far more than it FIGHTS it. The crown jewels (Option-C dimensional generation, substrate-vector machinery, canonical library, BC-target cell composition, the data-driven element/substrate-identity YAML layer) are the *exact* shape the future architecture assumes upstream. Where the future-state diverges, the divergence is concentrated in **two structural patterns**, both bounded:

1. **Process-stateful `global` ID counters** pervade generation (FIGHTS — item F is a symptom, not a local bug).
2. **The kit-composition cell input is a hard-coded literal table** (`CELL_DEFS`), not a queryable lifecycle-versioned cell library — Phase C pattern-library consumption needs a loader swap (FRICTION, not fight).

Everything else extends cleanly or with workable adapters. **A greenfield rebuild is NOT justified by architecture-divergence** any more than it was by throughput. The WRAP verdict survives on the axis it did not originally measure — with two named local rebuild targets.

### Count summary

| Classification | Count | Items |
|---|---|---|
| EXTENDS-CLEANLY | 5 | A (data primitives), C (naming deferral), E#2 (DDA), E#19 (doc-45 fields), E#21 (max-8) |
| EXTENDS-WITH-FRICTION | 4 | B (combinatory operators), D (Phase C pattern-library), A-race (schema-only families), and the off-hand-culture sub-operator within B |
| FIGHTS-THE-ARCHITECTURE | 1 | F (process-stateful counters — structural, not local) |

(11 sub-items audited across A–F; A splits cleanly because data-primitives EXTEND-CLEANLY while race/racial-trait families are FRICTION — both reported.)

---

## 1. Classification table + evidence

### A. Atomic-substrate-registry Layer 0 (20 primitive families)

**Headline split: data-backed primitives EXTEND-CLEANLY; the schema-only NEW families (race / racial-trait / race-affinity) are EXTENDS-WITH-FRICTION.**

| Family class | Classification | Evidence |
|---|---|---|
| Elements, sub-element flavors, attributes, ailments, resource models, geometry palette | **EXTENDS-CLEANLY** | These are already **data, not code paths**. `config/elements.yaml` (8 elements with `scales_with`/`ailment`/`rotating` fields), `config/substrate_identities/*.yaml` (7 typed `SubstrateIdentity` declarations loaded by `foundation/substrate_identity_loader.py`), `config/ailments.yaml` (registry-driven via `foundation/ailment_loader.py`). `element/pool.py:load_element_pool` loads `data/seasonal_elements/pool.json` with per-entry `d1_status` allow-list/eligible/quarantine. Adding a primitive = adding a YAML/JSON row. |
| T4 strategies, scaling-pattern-per-tier, chain-architecture, investment-scaling, skill-tree-position, weapon-form tokens, weapon-substrate properties, modifier types | **EXTENDS-CLEANLY (data present) with a behavioral caveat** | `t4_category_schema.py:47-58` defines the 7 strategies as module string constants in `ALL_T4_STRATEGIES`; weapon substrate carries `cultural_lineage_canonical` (14-enum) + `historical_period_canonical` (9-enum) + `register_canonical` per `substrate_weapon_binding.py:229,536`; investment patterns + per-tier scaling are enumerated in `per_skill_emitter.py`. The future-state's primitive set is *already represented* in code as the engine's generative inputs. **Caveat:** per-strategy weight LOGIC is coded (e.g., `t4_algorithm_wave2.py:400 a_weights[STRATEGY_RESOURCE_CONVERSION]=1.2`), so a NEW T4 strategy needs both the constant AND its behavior — but that is adding a case to a registry-shaped dispatch, the registry already exists. |
| **Race / racial-trait / race-element-affinity / race-attribute-affinity (NEW per Matt 2026-06-06)** | **EXTENDS-WITH-FRICTION** | These families **do not exist anywhere in production generation code** — `grep -rln "race_id\|racial_trait\|race_set\|race_element_affinity" src/reincarnated/` returns ONLY the canonical sidecar (`canonical/sidecars/atomic_substrate_registry_v1.json`, schema-only, `primitive_count_status: schema_only`, `primitives: []`) and AGENT_STATE.md. The registry itself marks them `schema_only` (registry § 1.17-1.20), so this is *anticipated* future authoring, not divergence. Friction is real but bounded: races compose via `race × element-attribute` (the element-attribute coupling already exists in `element_biases.py:ELEMENT_SCALING_ATTRIBUTE` + substrate-identity YAMLs) and racial traits compose with the existing mechanic-altering passive pool (`unified_mechanic_pool.yaml`, `mechanic_alteration.py`). New family loaders + a season-design authoring surface are NEW code, but they bolt onto the existing YAML-loader pattern (`substrate_identity_loader.py` is the template). No existing structure fights this. |

**Verdict A:** the substrate representation **accommodates primitives as data** for every family that exists today — this is the single strongest WRAP-supporting finding. The four NEW families are greenfield authoring within an established data-loader pattern, not a structural conflict.

### B. Layer 0.5 combinatory operators — **EXTENDS-WITH-FRICTION**

| Operator | Classification | Evidence |
|---|---|---|
| element-count → kit_architecture | EXTENDS-CLEANLY (latent) | single/hybrid distinction already threads `class_schema.py`, `class_generator.py`, `kit_space_schema.py` (grep hits for `hybrid_2_element`/`secondary_element`). The derivation operator is a thin formalization of state the schema already carries. |
| race × element-attribute interaction | EXTENDS-WITH-FRICTION | the *inputs* exist (element-attribute coupling in `element_biases.py`), but the race side does not (see A). New operator, existing coupling substrate. |
| seasonal-substrate-rotation | EXTENDS-WITH-FRICTION | partially seeded: `anchor/selector.py:select_seasonal_anchor` already does history-aware rotation (exclude used anchors, prefer non-recent categories, `RECENT_CATEGORY_LOOKBACK=3`); `cross_season_persistence.py:compute_archetype_signature` persists an 8-dim substrate-grounded signature across seasons; `element/pool.py` per-entry `d1_status` supports per-season element subsetting. The *primitives* for "hold ≥1 axis / rotate the rest" exist axis-by-axis, but there is **no unified per-axis hold/rotate operator** spanning all 10 rotatable axes (registry § 2.5). Assembling it extends these seams; it does not fight them. |
| **main + off-hand culture/period combinatorics** | **EXTENDS-WITH-FRICTION** | main-weapon carries `cultural_lineage_canonical` + `historical_period_canonical` (`substrate_weapon_binding.py`), but `off_hand_contract.py` defines off-hand as a **fixed mechanical-contract type** (banner/focus/talisman/tome/horn), NOT a parallel substrate with its own lineage/period. The culture-bridge operator (registry § 2.3: "Norse main + Aztec off-hand") is new construction, but it extends the existing lineage-binding query rather than fighting it. |

**Verdict B:** all four operators are *new code over existing substrate inputs*. None requires working against the grain. The friction is "assemble a unifying operator over seams that were built axis-at-a-time."

### C. Naming Layer N1-N4 + naming-as-survivor-reward deferral — **EXTENDS-CLEANLY**

Naming is already **architecturally downstream and confined**. Import audit (my 2026-06-10 consult § 2.1): exactly 4 files in `generation/` touch `llm/`; all naming flows through `kit_space_skill_naming.py` / `phase5_skill_naming.py` / `phase5_t4_narration.py`. Kit *mechanics* are 100% LLM-free (~9 ms/kit). Deferring naming to post-sim survivors needs **no structural change** — the naming pass is already a separate phase invoked after generation, and the sim consumes mechanical kits (`KitCandidate.to_character_dict()` / `VariantKitRow`) that carry no names. The future-state's N1-N4 stack placement (downstream of engine substrate, registry § 5) is *exactly* where the code already puts it. Deferral is a call-ordering change, not a rewrite.

### D. Pattern-library Phase C (Generation Logic Integration) — **EXTENDS-WITH-FRICTION**

The generation pipeline **already consumes a cell-addressed target**: `bc_target_subspace_generator.py:BcTargetSubspaceGenerator.generate()` iterates `CellDef` (`bc_target_cell_sampler.py:42 @dataclass(frozen=True) class CellDef` with `cell_id`/`label`/`bc_target: BcTargetCell`/`matching_policy`/`policy_weight`). This is the **correct seam** for Phase C — the generator is cell-driven by design.

The friction: the cells are a **hard-coded literal table** (`CELL_DEFS` list, ~25+ entries hand-authored at `bc_target_cell_sampler.py:84+`), not a queryable lifecycle-versioned library. Hypothesis-flow Phase C requires feeding **LIBRARY-LOCKED cells** (§ 5.2: "only LIBRARY-LOCKED cells enter generation logic") from a `pattern_library.db` with PROVISIONAL→LOCKED status. Two adapters needed: (1) replace the `CELL_DEFS` literal with a loader querying locked cells; (2) map the richer hypothesis-flow cell schema (experiential axes + flag enum + cell-shape) onto the existing `BcTargetCell` 5-tuple, which today carries only `(range, tempo, amplitude, attribute, proxy_density)`. Workable adapter against a correctly-shaped input seam — **not a rebuild**. The generator does not fight pattern-library cells; it just currently reads them from a Python literal.

### E. Per-entry gap-register items

| # | Item | Classification | Evidence |
|---|---|---|---|
| **#2** | DIRECT_DAMAGE_AMPLIFICATION scaffold retirement | **EXTENDS-CLEANLY** | The scaffold is **module-isolated**: `mechanic_alteration.py:82 STRATEGY_DIRECT_DAMAGE_AMPLIFICATION`, applied via a single function (`mechanic_alteration.py:666-716`, "Primary T4 universal slot scaffold") and one universal-application site (line 1180). Retiring it = replacing one function's body with natural mechanics; the call site and the universal-slot contract stay. No structural entanglement. Already flagged for Cycle 15 (Discipline #39 Mode B, explicit retirement commit). |
| **#19** | doc-45 fields `scope_preference`/`is_unique` + placeholder unique pools | **EXTENDS-CLEANLY (already landed)** | These are **already implemented**: `partition_schema.py:561,586 scope_preference: str | None`, `partition_schema.py:651 is_unique: bool`, `gear_instance_generator.py:520 is_unique`, `:517 t4_scope_preference`, `:444 "5 placeholder uniques per legendary tier for sim validation"`. The gap-register entry ("current code state is rocket-seam verification territory") resolves: the proposed fields exist now. Path-B post-generation form clustering (the other half of #19) is a NEW additive consumer, also clean. |
| **#21** | max-8-active skill constraint | **EXTENDS-CLEANLY** | The constraint is **not yet implemented** — `NODE_MAX_ACTIVE=15` in `per_skill_emitter.py:219` is per-node investment points, NOT a kit-level active-skill cap; no `n_active`/`active_count<=8` check exists in `b6_kit_builder.py`/`skill_tree.py`/`converge.py`. Adding a kit-level cap is a new validation predicate at kit assembly — additive, against the existing builder interface. Roadmap § 3 marks it Phase-2a ❌ (unbuilt), confirming it is forward work, not a refactor of something in the way. |

### F. Cache-hygiene bug (process-stateful skill-id counters) — **FIGHTS-THE-ARCHITECTURE**

**This is the one genuine architecture-fight, and it is structural, not local.** My 2026-06-10 consult measured the symptom (50% cache miss; volatile `skill_000283`→`skill_000327` ids leak into LLM prompts). Inspection shows the root cause is **pervasive process-stateful `global` counters**:

```
class_generator.py:395    global _class_counter
class_generator.py:493    global _experimental_counter
skill_composition.py:23   global _skill_counter
gear_roller.py:70         global _instance_counter
gear_generation.py:1163   global _gear_instance_counter
monster_generator.py:447  global _monster_counter
trial_generator.py:91     global _trial_counter
```

Seven module-global mutable counters across the seam mean generated IDs are **a function of process invocation order, not of content**. This fights the future-state on three cemented axes:

1. **Naming-as-survivor-reward + delta-adaptation (forward-architecture contract):** delta-naming and cross-run cache reuse REQUIRE content-deterministic ids. Volatile ids defeat the disk cache by construction (measured 50% miss).
2. **Cosmograph runtime LOOKUP (synthesis § 6.2 / canonical-synthesis § 8.1):** "engine pre-generates offline → JSON packet → runtime lookup by stable kit-id." Process-order-dependent ids undermine the stable-kit-id contract the realm-expansion content model depends on (kits emit into a continuously-growing space with **stable kit-ids**, season-archival pivot § ).
3. **Variant-as-delta overlay lineage:** `VariantKitRow` overlays inherit base-kit lineage; if base-kit ids shift per process, overlay provenance is fragile across regen.

**Why FIGHTS and not FRICTION:** the fix is not a one-line id-hygiene patch (though that mitigates the *prompt-leak* symptom). The architecture wants **content-addressed / seed-deterministic ids** as an invariant across the whole seam — that is a cross-cutting refactor touching 7+ modules and every downstream consumer that keys on id (cache, lineage, telemetry, kit_archive.db). It is the cheapest place where "module rebuild would be cheaper than adapter" is true at the seam level. **Scoped, not whole-seam** — but genuinely against the current grain.

**Refutation honesty:** I am NOT defending the WRAP verdict here. F is a real fight. But it is ONE fight, it is scoped to the id-generation substrate (not the kit-composition or substrate-vector machinery), and fixing it makes the future-state cleaner without rebuilding the validated generators. It downgrades "WRAP-CONFIRMED" to "WRAP-WITH-TARGETED-REBUILDS," not to "WRAP-REFUTED."

---

## 2. Named rebuild targets (the "targeted" in the verdict)

| Target | Scope | Why a rebuild not an adapter |
|---|---|---|
| **ID-generation substrate** (the 7 `global` counters) | content-addressed / seed-deterministic id scheme across `class_generator`, `skill_composition`, `gear_*`, `monster_generator`, `trial_generator` | process-statefulness is an invariant violation; an adapter cannot make a stateful counter deterministic — the generation policy itself must change. MIGRATION.md-gated (downstream id consumers). |
| **CELL_DEFS literal → pattern_library loader** (Phase C) | replace the hard-coded `bc_target_cell_sampler.py` literal table with a `pattern_library.db` query of LIBRARY-LOCKED cells + a cell-schema → `BcTargetCell` mapping adapter | this is FRICTION-grade (a loader swap + field mapper), listed here as the second targeted change because it is the other place the future-state needs structural (not additive) work. NOT urgent — gated behind hypothesis-flow Phase B reaching ~10 locked cells (4-8 months out per § 5.3). |

Everything else in the gap register is additive against existing interfaces.

---

## 3. Why this does NOT refute WRAP

Matt's challenge (greenfield-from-clean-specs was historically fast; modify-in-place costly): the audit's honest finding is that the generation seam's **validated core is the same shape the future-state assumes**, so "clean re-implementation" would re-derive the substrate-identity YAML layer, the BC-target cell composition, the Option-C dimensional generators, the data-driven element pool, and the confined downstream naming stack — i.e., re-build the crown jewels to land in the same place, at the cost of re-validating ~5 weeks of balance/distribution work (Path-α closure, B14.5 V1 loop, the 5× substrate-variety calibration). The two genuine structural divergences (F's stateful ids; D's literal cell table) are **cheaper to refactor in place than to re-validate from scratch** — which is the precise definition of WRAP over greenfield.

The one place I would *not* over-claim: if a future requirement makes the stateful-id refactor (F) collide with a simultaneous large substrate-schema expansion (e.g., the race/racial-trait families landing AND pattern-library Phase C AND cosmograph stable-id contract all at once), the combined blast radius could approach "rebuild the id+cell+composition spine together." That is a *conjunction* re-open criterion, not a current state. Today, each is a bounded local change.

---

## 4. Sign-off

**rocket**, 2026-06-11. Read-only audit; zero production code modified. Verdict: **WRAP-WITH-TARGETED-REBUILDS** (id-generation substrate; CELL_DEFS→pattern-library loader). Counts: **5 cleanly / 4 friction / 1 fights**. The single FIGHTS item (F, process-stateful counters) is structural and pervasive but scoped to id-generation, and refactoring it strengthens the future-state rather than justifying a greenfield rebuild. The WRAP verdict survives on the design-architecture-divergence axis it did not originally measure.
