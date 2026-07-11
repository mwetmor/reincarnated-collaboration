# Hybridity Mechanical Scaffolding Audit — the full binding-surface spectrum vs the live engine

> **STATUS:** CURRENT — the missing-mechanics register that the doctrine canonization preface points to (REPLACES doctrine Part II.1's BC-kinds list, per Matt 2026-07-11: that list was Mobile-Claude "groping at potential missing mechanical axes" without engine docs; this audit is the engine-verified answer to the same question).
> **Author:** gandalf, 2026-07-11 (Pattern B, ARCHITECT role). Commissioned by Matt verbatim: *"ultra think about how to architect the full spectrum of mechanical scaffolding on top of which elemental hybridity would need to sit upon and compare that to our current mechanics and look for gaps. If we have gaps, then we need to solve for them now."*
> **Companions:** `matt_notes_handoff_docs/reap-die-rise-element-application-addendum.md` (the seven structures) · `2026-07-10-element-application-doctrine-review.md` · elicitation note §2-quinquies (Spellsword resolution) · serial-content tracker eighth entry (T4 scaling-unification ruling).

---

## §0 — Audit lens

The binder law inverted: element application binds to every surface where damage/effects LEAVE the kit. Therefore the scaffolding = the complete set of exit surfaces, each either existing, half-existing, or absent. Every claim below is line-cited from this pass's engine reads (2026-07-10/11).

## §1 — The binding-surface spectrum (7 structures → 7 surfaces + 1 spine)

| # | Surface (structure) | Engine state — VERIFIED | Gap class |
|---|---|---|---|
| 1 | **Chain slots** (`chain_partition`) | ✓ **LIVE**: Amendment 7a `chain_elements` (`per_skill_emitter.py:864/:1136/:1279`); per-chain ailments (`ELEMENT_AILMENT[chain_elem]` :772); element-driven mitigation (`damage_resolver.py:439+` physical→dodge/block/armor, else resist+7×7; `resistance_matrix.py:137-139` physical deliberately non-substrate); Layer-2 roll `_roll_hybrid` at `HYBRID_RATE=0.175` with physical in secondary pool (`season_generation_pipeline.py:654-664`) | **ONE coupling** (E3 build item): per-chain `damage_scaling_type` + `scaling_attribute` derivation from chain element via canonical `scales_with` — replaces kit-level stamping (`per_skill_emitter.py:1115` `_BC_ATTRIBUTE_TO_SCALING_ATTR[config.bc_attribute]` onto all skills; `:1589` validation). Uncoupled, an INT kit's physical chain is a physical-typed bolt on the magical geometry ladder |
| 2 | **Kernel geometry classes** (`geometry_partition`) | ✓ vocabulary rich: 24-type `geometry_type` + 6-type `spatial_geometry_type` + `geometry_params` (`ability_schema.py:20-29`); elements assign per-chain only | Pipeline assignment rule (geometry-class → element) + affinity-mask `hard_constraint` (kit must span ≥2 geometry classes or the partition is degenerate). Runtime-FREE |
| 3 | **Damage-output split** (`flat_split`) | ~ **HALF-BUILT, generation side**: skills are ability composites (`composition_mode: single/layered/fused/triadic`, `skill_schema.py:9`); **each Ability carries its own `canonical_element`** (`ability_schema.py:17`) — but composition FLATTENS at emission; resolver consumes ONE `skill.canonical_element`; no multi-component accounting (`composition_mode`/`abilities` unread in `damage_resolver.py`/`fight_engine.py`) | **Sim-side component-vector resolution**: hit = {(element, fraction)}, each component → own mitigation channel + own attribution. Math-note items: crit per-component vs per-hit; block per-component vs per-hit (block currently applies in BOTH branches :456/:486) |
| 4 | **On-hit hooks** (`rider_on_hit`) | ~ **DECLARED-NOT-RESOLVED**: resolver EMITS events — `on_hit` (:476/:519), `on_kill` (:522), `on_crit` (:668) — into the per-application events list; NOTHING consumes them to fire secondary effects; ailment-on-hit is HARDWIRED (chain_A primary attacks :772), not a hook entry | **THE HOOK LAYER**: event-consumer registry. First registered hook = existing ailment application refactored onto it (built-in non-regression proof). Then rider entries carry element bindings |
| 5 | **Trigger table** (`proc_trigger`) | ~ **DECLARED-NOT-RESOLVED**: `layer2_trigger` enum EXISTS — `{on_use, on_hit, on_kill, on_take_damage, periodic, threshold_stack, threshold_hp, sequence}` (`skill_schema.py:139-141`) + stackability vocabulary (:135-138) — sim consumption PARTIAL: only the charge-stack path is live (`per_stack_passive_bonus` `damage_resolver.py:329-332`, `combatant.py:188`; E4/Q9 lineage) | **SAME hook layer** — the layer2 enum IS the declared spec; sim consumption is the build. One architecture serves structures 4+5 |
| 6 | **Combo phases** (`phase_partition`) | ✗ **ABSENT cross-skill**: `sequence` in the trigger enum + `prerequisite_skill` (Layer 1.5 coupling, `skill_schema.py`) are declared-not-consumed (grep: no simulation/*.py consumer); no mark/consume state exists; E4 commitment phases are WITHIN-cast, not cross-skill | **The one genuinely NEW mechanical axis**: cross-skill state (skill A marks target → skill B consumes mark for effect). Design from scratch; candidate placement-test hearing (is combo-structure a kit-defining kind?). Genre: D2 CoS-detonate lineage, PoE detonators, D3 Monk combo generators/spenders |
| 7 | **Emission slots** (`emission_carrier`) | ~ **SPECCED-NOT-BUILT**: rotational addendum §3 one-emission-primitive `{entity, origin, trigger, depth≤2}`; proxy/summon system LIVE (proxy_density axis, summon-act scope row); pilot two-arm driver in flight | Build per rotational addendum, sequenced with B12 re-cert (same substrate). **Boundary ruling owed at integration**: emitted-entity vs proxy/summon attribution; the §5 inheritance rule should name proxies explicitly |
| S | **Attribution spine (cross-cutting)** | Damage events exist; NO per-element attribution columns (kill-attribution-by-element, realized-elemental-output-share) | **v1-BLOCKING measurement**: without the spine, no rate band certifies (realized-share law has no instrument). star-lord seam. Must cover ALL exit surfaces incl. DoT ticks and (later) components/emissions/proxy attacks |

## §2 — The headline finding

**v1 hybridity (partitions) blocks on NOTHING new.** The addendum's §9 build order survives engine contact fully intact — and the engine is AHEAD of the addendum's assumptions (chain_partition is literally running at 17.5% prevalence since Amendment 7, 2026-05-29). The gaps live exactly where §9 already deferred: blends (hook layer + component accounting), carrier (emission primitive), phase_partition (the one from-scratch axis).

## §3 — The scaffolding build ladder

1. **E3 dispatch (NOW):** per-chain scaling derivation (type+stat, one site) · geometry-partition assignment rule + mask constraint · `element_application` block on kit packet + per-cell `hybrid_affinity` masks + anchor pins + `HYBRID_RATE` promoted to governed dial · Option C tuple DELETION (4 sites) · `naming_flavor_element` split (mechanical→block; flavor field renamed, naming-only Do-Not-Regress) · scaling-unification T4 (catalog capstone, rollable+pinnable; overrides scaling STAT only) · **attribution spine** (star-lord). Ships `chain_partition` + `geometry_partition`, honestly certified.
2. **HOOK LAYER (next mechanical axis, pre-blends):** one event-consumer registry over the resolver's existing event emissions; ailment application refactored on as first hook; `rider_on_hit` + `proc_trigger` become element-bound hook entries. Half the spec exists (layer2 enum).
3. **COMPONENT ACCOUNTING (pre-`flat_split`):** sim-side component vectors; math note settles crit/block semantics; generation side already compositional.
4. **PHASE/STATE AXIS (pre-`phase_partition`):** mark-and-consume design note from scratch; placement-test hearing on combo-structure-as-kind.
5. **EMISSION PRIMITIVE (carrier):** per rotational addendum; paired with B12 re-cert; boundary ruling (emitted vs proxy) at integration.

## §4 — Doctrine II.1 disposition (canonization preface input)

The BC-kinds list in doctrine Part II.1 = Mobile-Claude gap-groping without engine/pipeline docs (Matt 2026-07-11). Disposition: the preface REPLACES it with (a) the live six-coordinate catalog list (attribute · range · tempo · amplitude · proxy_density · commitment — 972 = 4 × 3^5) + (b) THIS AUDIT as the missing-mechanics register. Mapping of the list's orphans: *trigger hooks* → the hook layer (§1 rows 4–5 — a REAL gap, correctly sensed) · *targeting* → existing auto-target machinery (no hybridity dependency at v1) · *persistent rings* → kept BC cell (rotational addendum §4). **The attribute-axis placement-test hearing DISSOLVES** — the list was never normative; attribute is already a live coordinate.

## §5 — Open items this audit creates

| Item | Owner | Gate |
|---|---|---|
| Crit/block per-component math | gamora math note | Component-accounting build (ladder #3) |
| Combo/phase design note + placement hearing | gandalf | Before ladder #4 |
| Emitted-entity vs proxy attribution boundary | gandalf ruling + gamora/rocket | Emission integration (ladder #5) |
| Do proxy/summon attacks carry element today? (inheritance-law input) | verification, rocket/gamora | Before ladder #5 |
| DoT-tick element attribution (spine completeness) | star-lord | With attribution spine (ladder #1) |

---

**Sign-off:** gandalf, 2026-07-11. Anchors: element addendum §1–§10 · rotational addendum §3 · `per_skill_emitter.py:664/:772/:864/:1115/:1279/:1589` · `damage_resolver.py:329-332/:439-522/:668` · `skill_schema.py:9-141` · `ability_schema.py:17` · `combatant.py:188` · `season_generation_pipeline.py:654-664`. *The scaffolding was never missing under the first span — the bridge is buildable now; the far spans are named, sited, and ordered.*
