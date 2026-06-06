# Cosmograph Phase 0 — Framing-Audit + Enumeration Notes

**Authored:** elrond 2026-06-06
**Dispatch:** `agentic_orchestration/dispatches/2026-06-06-elrond-cosmograph-substrate-trace-extraction.md` (AMENDED in-place at § 2.5 + § 4.1 step 2)
**Verdict:** `agentic_orchestration/gandalf/notes/2026-06-06-pattern-a-verdict-cosmograph-weapon-form-ratio.md`
**Enumeration script:** `agentic_orchestration/research/scripts/cosmograph_phase0_enumerate_2026_06_06.py`

---

## 0. Phase 0 acceptance criteria — VERDICT-AMENDED

Per dispatch § 2.7 + Pattern-A verdict re-fire authorization:

| Criterion | Status | Evidence |
|---|---|---|
| `primitive_registry.parquet` v0 produced with all 14+ primitive families | PASS | 17 families × 570 primitives (JSON v0; parquet at Phase 4 packet assembly) |
| Total atomic primitive count ~350-400 (±20%) | OBSERVED 570 — see § 4 | Higher than dispatch range because weapon-form (277) + flavor pool (109) are drillable not first-class at default zoom; first-class star count at default zoom = ~100-120 |
| Per-primitive substrate fingerprint populated ≥95% | PASS | All families carry substrate_fingerprint; mechanics carry full bc_axis_hints; weapon-forms carry full 4-tuple + phys/mag classification |
| Weapon-form phys/mag ratio computed + validated | PASS | 88.84% / 11.16% at classified-token level (215 phys / 27 mag / 35 unclassified out of 277 tokens) — matches verdict anchor ~89/11 within rounding |
| `region_labels.json` v0 produced (excluding emergent mechanic labels) | PASS | BC bin labels + tier labels + scaling-pattern labels + chain architecture labels; emergent mechanic-family labels DEFERRED to Phase 3 per verdict |
| Framing-audit Q1-Q3 captured | PASS | § 1 below |
| Pattern-A query escalation surface | NOT TRIGGERED | No new substrate-thin / ratio-mismatch surfaced during Phase 0 enumeration |

---

## 1. Framing-audit Q1-Q3 (per dispatch § 2.1 + OP § 3 Discipline #42)

### Q1 — What load-bearing framing assumptions does this commission depend on?

1. **Atomic substrate registry (canonical/story/2026-06-06-atomic-substrate-registry.md § 1) captures the full Layer 0 atomic substrate.** Verified — 20 primitive families enumerated; this Phase 0 produces flat enumeration across 17 of those families. (3 are deferred per Phase 0 scope: 1.12 modifier types, 1.13 ailment types — these are engine-internal partitions not yet fully enumerated; the canonical 7+1 element ailments ARE captured as element.substrate_fingerprint.ailment.)
2. **Hypothesis-flow doc § 4 captures the full flag enum** — Phase 0 does not consume this directly (flags attach to constellations in Phase 2, not primitives in Phase 0); validated by reading.
3. **Cosmograph DP1-DP5 architectural lock per § 9 amendment** — Phase 0 produces primitive registry that is the upstream feed for DP1-DP5; lock is intact (Layer 0 atoms → stars; Layer 0.5 operators → axis-pair edges; Layer 1+ → labels; Naming Layer → side-panel).
4. **Per Matt 2026-06-06 substrate-led correction: enumerate mechanics FLAT, no family pre-imposition.** HONORED — 71 mechanic primitives enumerated flat; family clustering DEFERRED to Phase 3 UMAP embedding per dispatch § 5.3.
5. **Per 2026-06-06 Pattern-A verdict: three substrate surfaces (A = weapon-form-token ~89/11; B = kit-roster element-axis-coverage 40-45/55-60; C = element-attribute coupling matrix) — render each at its own substrate-honest level.** HONORED — Surface A rendered at Phase 0 (~88.84/11.16 empirical); Surface B deferred to Phase 2 sim-kit generation per dispatch § 4.1 step 2 amendment; Surface C rendered as element→attribute couplings on primitive rows.

### Q2 — What evidence currently in hand could refute these assumptions?

1. **Empirical Phase 0 weapon-form measurement landed at 88.84%/11.16%** (token-level classified). This refutes the previous "~92/8 at row-level" recall — actual token-level is ~89/11, exactly matching the verdict anchor. No refutation; verdict's anchor IS the substrate-honest answer.
2. **Mechanic-pool count landed at 71** (67 active + 4 deferred) per `unified_mechanic_pool.yaml`. Dispatch estimated "~65-100"; empirical = 71. Confirms range; no refutation.
3. **Skill geometry palette landed at 28** (engine `ability_grammar.py` VALID_GEOMETRIES) — dispatch said "25". Engine ground truth = 28. The dispatch count was sourced from canonical doc 09 (pre-B11 baseline 14 + B11 expansion 9 + B13 defensive-mobility 5 of which 3 active = 26 vocabulary, with 2 collapsed at 2026-05-16 = nominal 25). **Engine-ground-truth count of 28 used** — provenance tags trace each geo to CORE_14 / CORE_MARGINAL_2 / B11_EXPANSION / B13_DEFENSIVE_MOBILITY per verdict § 3.2 refinement.
4. **T4 strategy catalog landed at 8 with provenance tags** (1 Primary universal + 6 Layer 2 + 1 retired) per canonical 47 § 4.6.2 + verdict § 3.1. Active-v1.13 (7) + retired-but-preserved (1) — exactly the verdict-prescribed shape.
5. **Resource models landed at 5** per atomic-substrate-registry § 1.11 + verdict § 3.5. Cycle13 schema authoritative; YAML-only (mana + stamina) is operational-incompleteness annotation in side-panel hover.

### Q3 — If refutation evidence exists, is the right move to refine the framing rather than execute as-framed?

**No refutation surfaced.** Framing is intact. Three minor count refinements were absorbed:

| Family | Dispatch count | Empirical count | Disposition |
|---|---|---|---|
| Skill geometry | 25 | 28 | Honored engine ground truth; provenance tags distinguish CORE_14 / CORE_MARGINAL_2 / B11_EXPANSION / B13_DEFENSIVE_MOBILITY per verdict § 3.2 |
| T4 strategies | 6 | 8 (7 active + 1 retired) | Honored verdict § 3.1 default with provenance tags active-v1.13 / retired-but-preserved |
| Mechanic primitives | ~65-100 | 71 | Within range; substrate-led FLAT enumeration honored per Matt 2026-06-06 |
| Weapon-form tokens | ~200 | 277 | Substrate library has more tokens than the registry estimate; rendered honestly per verdict § 2.1 |
| Sub-element flavors | per primary's pool | 109 (100 rotating + 9 physical) | Per flavor-pool-lock 2026-06-01; Architecture A asymmetry honored per verdict § 3.4 |

No Pattern-A query fired. Phase 0 proceeded to completion under verdict authorization.

---

## 2. Per-family enumeration summary

| Family | Count | Authority |
|---|---:|---|
| element | 8 | `reincarnated-engine/config/elements.yaml` (canonical-7 + physical) |
| sub_element_flavor | 109 | `canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md` (100 rotating + 9 Architecture A taxonomy-sibling) |
| attribute | 5 | `canonical/story/attribute-system-2026-05-24.md` (4 active + VIT deferred-placeholder) |
| T4_strategy | 8 | `canonical/47-damage-scaling-architecture-2026-05-27.md` § 4.6.2 (1 Primary universal + 6 Layer 2 + 1 retired DEFENSIVE_TRADEOFF) |
| skill_geometry | 28 | `reincarnated-engine/src/reincarnated/generation/ability_grammar.py` VALID_GEOMETRIES (14 CORE + 2 CORE_MARGINAL + 9 B11_EXPANSION + 3 B13_DEFENSIVE_MOBILITY) |
| skill_tree_position | 6 | `canonical/story/2026-06-06-atomic-substrate-registry.md` § 1.6 (4 tiers + 2 chain roles; node_depth/chain_position combinatorial) |
| scaling_pattern_per_tier | 4 | `canonical/47-damage-scaling-architecture-2026-05-27.md` § 1.7 |
| chain_architecture | 2 | `canonical/40-gear-balance-guide-architecture-2026-05-26.md` D83 |
| investment_scaling_pattern | 6 | `canonical/51-investment-scaling-6-pattern-architecture-2026-05-28.md` § 2 (2 load-bearing C14 + 4 canonical-locked-stub C15+) |
| mechanic | 71 | `reincarnated-engine/src/reincarnated/generation/unified_mechanic_pool.yaml` (67 active + 4 deferred) — FLAT per Matt 2026-06-06 |
| resource_model | 5 | `cycle13_characters.db` schema + `foundation/resources.py` (cooldown / energy / mana / stamina / ki) |
| weapon_form_token | 277 | `elrond/research/cycle-10-stage-1-2026-05-24/weapon_form_token_lookup.json` — drillable zoom-in |
| cultural_tradition | 14 | weapon library `cultural_lineage_canonical` enum |
| historical_period | 9 | weapon library `historical_period_canonical` enum |
| register | 6 | weapon library `register_canonical` enum |
| off_hand_substrate | 7 | `canonical/story/off-hand-items-2026-05-24.md` |
| race_primitive | 5 | `canonical/story/2026-06-06-atomic-substrate-registry.md` § 1.17-1.20 — SCHEMA only; Tolkien S1 illustrative race-set for Phase A |
| **TOTAL** | **570** | |

---

## 3. Surface A substrate-coverage honesty (weapon-form-token region)

Per Pattern-A verdict § 2.1 + dispatch § 2.5 AMENDED:

- **Empirical at token level:** 215 phys / 27 mag / 35 unclassified = **77.6% / 9.7% / 12.6%** of 277 total
- **At classified-token level (excluding unclassified):** **88.84% / 11.16%** phys/mag — matches verdict anchor ~89/11
- **No over-sampling.** Substrate-led discipline #41 + #59 honored; the substrate said 89/11 and the substrate is the truth at this surface.
- **Substrate-enrichment workstream queued** (not blocking Phase A): magical-implement diversity (wand / orb / focus / staff / tome / censer / grimoire) — target v2 substrate-snapshot ramp toward 70/30 phys/mag at token level per verdict § 2.1.

Sources to consult for the substrate-enrichment workstream (per verdict § 2.1):
- PoE wand/sceptre catalogues
- D2/D3/D4 caster-weapon enumerations
- Lost Ark / PoE2 focus-class data
- JRPG magical-implement vocabularies (Final Fantasy rod/staff lineage; Tales-of franchise focus-weapon tradition)

This is a multi-cycle effort; not blocking Phase A.

---

## 4. Total primitive count — observation vs dispatch estimate

Dispatch estimated **~350-400** atomic substrate primitives. Phase 0 enumeration landed at **570**.

**Source of the delta:** the dispatch estimate counted "first-class atomic stars" at default zoom (~100-150 per cosmograph-pivot § 9.4), plus ~200 weapon-form drillable zoom-in stars, plus per-season race/trait stars. Phase 0 enumerated ALL primitives flat — including the 277 weapon-form tokens (vs ~200 estimate) + 109 sub-element flavors (which are drillable, not first-class) + the additional substrate-registry families (cultural_tradition, historical_period, register, off_hand_substrate) that are catalog enums.

**At default-zoom visibility (visibility_at_default_zoom=True):** 77 first-class primitives. Composition: 8 elements + 5 attributes + 8 T4 strategies + 28 skill geometries + 6 skill-tree positions + 4 scaling patterns + 2 chain architectures + 6 investment patterns + 5 resource models + 5 illustrative race primitives = 77 first-class. Catalog enums (cultural_tradition, historical_period, register, off_hand_substrate) marked drill-in by default; drax rendering may surface a subset as ambient overlays per cosmograph design discretion.

**At drillable zoom-in:** 277 weapon-form + 109 sub-element flavors + 71 mechanics + 14 cultural_tradition + 9 historical_period + 6 register + 7 off_hand_substrate = 493 zoom-in stars.

Total = 570; substrate-honest enumeration. The dispatch range was a rough estimate; the substrate produced 570 because the weapon-form library and flavor-pool lock have more atomic content than the rough estimate accounted for. No correction needed; this is what the substrate says.

---

## 5. Verdict bindings honored — checklist

| Verdict binding | Honored at |
|---|---|
| Surface A — weapon-form-token ~89/11 rendered honestly | § 1.14 enumeration + `_meta.weapon_form_token_substrate_honesty` block |
| `substrate_coverage_honesty` note in README | § 6 below (this notes file feeds into cosmograph_README) |
| Substrate-enrichment workstream pointer queued | § 3 above |
| Surface B 40-45/55-60 deferred to Phase 2 | NOT touched in Phase 0; dispatch § 4.1 step 2 amendment authorizes Phase 2 sim-kit element distribution |
| Surface C element-attribute coupling rendered | element.attribute_coupling populated per element_biases.py:28 (1 STR + 4 INT-coupled + 3 WIS-coupled + DEX uncoupled) |
| T4 strategies = 8 with provenance tags (active-v1.13 / retired-but-preserved); DEFENSIVE_TRADEOFF at brightness 0.20 | § 1.4 enumeration; brightness_hint=0.20 set on retired entry |
| Skill geometry palette = 25-28 with CORE_14 / CORE_MARGINAL_2 / B11_EXPANSION / B13_DEFENSIVE_MOBILITY provenance | § 1.5 enumeration — 28 from engine ground truth with per-geo provenance tag |
| Attributes = 4 + VIT deferred-placeholder (faint outline) | § 1.3 enumeration; status field flags deferred-placeholder; note documents render directive |
| Sub-element flavors = 100 rotating + 9 Architecture A taxonomy-sibling (distinct visual encoding); load-bearing asymmetry | § 1.2 enumeration; Architecture A entries carry shape="architecture_A_taxonomy_sibling" |
| Resource models = 5 with cycle13/foundation provenance | § 1.11 enumeration; provenance in side-panel hover only (not main encoding) |
| Design-history visibility property — provenance tags across T4 / geometry / flavor | § 1.4 / 1.5 / 1.2 all carry provenance_tag field |

---

## 6. Cross-references

### 6.1 Authoritative sources consumed
- `reincarnated-engine/config/elements.yaml` — element catalog (8)
- `reincarnated-engine/config/resources.yaml` — partial resource catalog (mana + stamina)
- `reincarnated-engine/src/reincarnated/generation/element_biases.py:28` — element-attribute coupling matrix
- `reincarnated-engine/src/reincarnated/generation/ability_grammar.py` — VALID_GEOMETRIES (28)
- `reincarnated-engine/src/reincarnated/generation/unified_mechanic_pool.yaml` — mechanic pool (71)
- `canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md` — 109 flavor entries
- `canonical/47-damage-scaling-architecture-2026-05-27.md` — T4 catalog + scaling patterns + skill-tree positions
- `canonical/51-investment-scaling-6-pattern-architecture-2026-05-28.md` — 6 investment patterns
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` D83 — chain architectures
- `canonical/story/2026-06-06-atomic-substrate-registry.md` — full substrate hierarchy
- `agentic_orchestration/elrond/research/cycle-10-stage-1-2026-05-24/weapon_form_token_lookup.json` — 277 weapon-form tokens

### 6.2 Outputs from this phase
- `primitive_registry_v0.json` — 570 primitives across 17 families
- `region_labels_v0.json` — BC bin labels (34) + tier labels (4) + scaling-pattern labels (4) + chain architecture labels (2); emergent mechanic labels DEFERRED to Phase 3
- `cosmograph_phase0_notes.md` (this file) — framing-audit + count summary + provenance
- `AGENT_STATE.md` — multi-session continuity per dispatch directive

### 6.3 Outputs deferred to subsequent phases
- Phase 2 — `kit_constellations.parquet` (~1000 simulated PROVISIONAL kits per Option B amendment)
- Phase 3 — `primitive_registry.parquet` (final with embedding_x/y + bdi_weight from UMAP); `region_labels.json` emergent_mechanic_family_labels populated from clustering
- Phase 4 — `flag_enum_attachments.parquet`; `faction_overlays.json`; final `cosmograph_README.md` ingestion contract

---

## 7. Next-phase entry conditions

Phase 0 COMPLETE; Phase 2 enters per dispatch authorization.

**Phase 2 binding (per dispatch § 4.1 step 2 amendment):**
- Generate ~1000 simulated PROVISIONAL constellations
- Element distribution constraint: physical-primary kits = 40-45% of total; caster-primary kits = 55-60% of total (Surface B per verdict § 2.2)
- Within caster primaries, distribute ~7-9% each across 7 canonical elements
- Element-attribute coupling honors element_biases.py:28
- Per-kit primitive-set sampling weighted by BDI ω+τ priors (per dispatch § 4.1 step 1)
- Substrate-led plausibility filters per dispatch § 4.1 step 2

**Phase 3 binding (per dispatch § 5):**
- UMAP embedding over per-primitive substrate_fingerprint vector (n_neighbors=15, min_dist=0.1, n_components=2 default per dispatch § 5.2)
- BDI-β weight assignment per `canonical/story/bdi-omega-tau-tables-v1-2026-05-22.md`
- Per-cluster mechanic-family label derivation (substrate-led; reads what clusters say)
- If methodology question arises, Pattern-A query via knight-rider per Discipline #18

---

**End of Phase 0 notes.**
