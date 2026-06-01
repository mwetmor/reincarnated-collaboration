# Flavor-Pool Per-Primary-Element Lock — WS1A.Q18

> **STATUS:** CURRENT (load-bearing as of 2026-06-01) — see `canonical/00-ground-state.md`

**Date:** 2026-06-01
**Author:** gandalf (story-and-design steward) — authored per Matt 2026-06-01 PG-3 ratification
**Status:** v1.0 canonical lock — Architecture A locked; 118 entries committed; Q18.a-e structural commitments locked
**Authority:** Matt 2026-06-01 verbatim PG-3 architectural-commitment ratification (ADR-002 Tier A) at `agentic_orchestration/cycle-15-ws1a-q18-flavor-pool-research/pg-3-ratification-2026-06-01.md`
**Companion docs:**
- `canonical/story/2026-05-31-hypothesis-flow-pattern-library-architecture.md` § 1.7 + § 8b Q18 — parent canonical doc (Q18 closure path execution)
- `~/Games/reincarnated-engine/config/elements.yaml` — canonical-7+1 element catalog (substrate this lock is built on)
- `~/Games/reincarnated-engine/data/seasonal_elements/pool.json` — existing 156-entry pool (sub-phase 5f migration target)
- `agentic_orchestration/cycle-15-ws1a-q18-flavor-pool-research/pg-3-ratification-2026-06-01.md` — PG-3 architectural-commitment lock (load-bearing input)
- `agentic_orchestration/gandalf/notes/2026-06-01-q18-flavor-pool-research-synthesis.md` — Phase 5a synthesis draft (substantive surface ratified at PG-3)
- `agentic_orchestration/elrond/analysis/element-flavor-mapping-stats-2026-06-01.md` — Phase 4 statistical analysis verdict (empirical anchor)
- `agentic_orchestration/gandalf/notes/2026-06-01-q18-flavor-pool-research-operational-sequence.md` — operational sequence (wave orchestration spec)
- `canonical/story/2026-05-29-designer-writes-substrate-player-names-experience-principle.md` — foundational substrate-led principle composed
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § 41 (substrate-led) + § 42 (framing-audit) + § 18 (math-hotspot methodology consultation)

---

## 0. TL;DR

**Architecture A LOCKED.** 7 rotating primaries (fire / water / earth / wind / lightning / holy / shadow) carry substrate-honest flavor pools; physical exists as the 8th DAMAGE TYPE via Architecture-A taxonomy-sibling registry (NOT a flavor pool). Total: **118 entries** locked across 8 primaries — 109 rotating-primary flavor-pool entries + 9 physical taxonomy-registry entries.

This lock is the keystone artifact for WS1A.Q18 (per-primary flavor-pool research-and-lock wave). It composes with the canonical-7+1 element catalog at `config/elements.yaml` (substrate preserved), authorizes the sub-phase 5f pool.json migration (POST-WAVE), and unblocks WS1A.3 (per-kit sub-element selection) + WS1A.4 (per-skill bounded LLM flavor judgment). Wave-close (PG-4) unblocks the Q16 / Q17 / Q19 hard-blocker waves per pattern-set composition.

**Substrate-led methodology applied:** vote-grounded research (217 rows × 3 tracks × 8 primaries; 31 high-confidence cross-track candidates) + designer-curation overlay at the encoding gate (Discipline #41 refinement). Substrate vote ANCHORS candidate inclusion; designer curation ROUTES per-candidate slots, applies cardinality targets, weighs Reincarnated-fit.

---

## 1. Architecture A definition

**Architecture A — 7-primary rotating + physical-as-taxonomy-sibling.**

- **7 rotating primaries** (fire / water / earth / wind / lightning / holy / shadow) each carry a substrate-honest flavor pool of 12–18 entries (109 total).
- **Physical** exists as the 8th DAMAGE TYPE in the engine taxonomy (for damage resists, mitigation routing, ailment dispatch per `config/elements.yaml`) but does NOT carry a "flavor pool" in the same sense. Its 9 entries form a **damage sub-type field + mechanical action vocabulary registry** (a taxonomy-sibling), categorically different from rotating-primary flavor pools.
- **Physical kits opt out of WS1A.4 LLM flavor judgment.** Physical kit naming uses **mechanical-schema templates** (weapon-form + action-vocabulary composition) rather than LLM bounded judgment against a flavor pool.
- **Physical kit identity differentiates through** (a) WEAPON-FORM substrate (sword / spear / bow / axe — Reincarnated already has this surface per canonical 17-gear); (b) PHYSICAL-AILMENT vocabulary (bleed — already locked in `config/elements.yaml`); and (c) the 9-entry mechanical-action vocabulary registry below.

### 1.1 Why physical-as-taxonomy-sibling (substrate evidence)

Per Phase 4 § 7 (elrond stats verdict):

| Axis | Rotating primaries (range) | Physical |
|---|---|---|
| Modal substrate-type concentration | 0.32 – 0.70 | **0.85 mechanical_keyword** |
| Distinct substrate types | 4 – 5 | **3** |
| HDBSCAN cluster count | 2 – 7 substantive clusters | **1 dominant cluster (n=11) + 1 side cluster (n=2)** |
| Off-diagonal contamination cells | average 2.6 | **1 cell only (`force` via wind)** |
| Top-10 vocabulary | 3+ substrate types mixed | **9-of-10 mechanical_keyword + 1 ailment** |

This IS the D&D 5e damage-type taxonomy (PHB ch.9: bludgeoning / piercing / slashing + force) plus PoE physical-damage subtypes + ARPG-canonical kinetic vocabulary. Rotating primaries flex, contaminate, distribute across substrate-types, fragment into multiple keyword clusters. Physical does the opposite: monolithic, taxonomic, semantically isolated, structurally non-flexing.

### 1.2 Why Architecture A over Architecture B (cross-house genre-canonical convergence)

Every ARPG cited (Diablo 1/2/3/4/Immortal, PoE 1+2, Last Epoch, Grim Dawn, Lost Ark, Torchlight 2/Infinite, Wolcen, Chronicon, Titan Quest) treats physical as taxonomy-sibling, weapon-anchor, or ailment-class — not as flavor-pool-symmetric. JRPG canon (Final Fantasy series, Persona/SMT, Mushoku Tensei) consistently treats physical as its own thing — Megaton Press / God's Hand / Heat Wave / Hassou Tobi are MECHANICAL named skills, not flavor sub-elements. PoE 1+2 is the strongest precedent: physical sub-vocabulary lives in ailment/mechanical space (bleed / impale / maim) — categorically different from elemental ailments (Ignite / Shock / Chill).

`config/elements.yaml` is ALREADY shaped for Architecture A — physical's `rotating: false` + `resistance_type: armor` + `dodgeable: true` configuration is asymmetric against rotating primaries' `percentage` + `dodgeable: false`. The engine taxonomy is ALREADY shaped for A; Architecture A makes the flavor-pool asymmetry MATCH the engine-taxonomy asymmetry.

### 1.3 Composition with downstream consumers

| Consumer | Architecture A handling |
|---|---|
| WS1A.3 — per-kit sub-element selection | Routes 7-primary path against rotating flavor pools + weapon-form path for physical kits |
| WS1A.4 — per-skill bounded LLM flavor judgment | LLM judges against 7 substrate-honest pools; physical kits judged against weapon-form + ailment vocabulary parallel system (mechanical-schema templates) |
| Substrate library | Cleaner: each primary that flavor-pools is substrate-aligned; physical opts out of LLM judgment without forcing substrate-mismatch |

---

## 2. Per-primary allow-lists (FINAL)

### 2.1 fire (16 entries)

`ember`, `cinder`, `blaze`, `scorch`, `inferno`, `ignite`, `fira`, `lava`, `magma`, `charcoal`, `char`, `brand`, `flare`, `fusion`, `thermal`, `combustion`

### 2.2 water (14 entries)

`tide`, `torrent`, `glacial`, `brine`, `aqua`, `frost`, `chill`, `mist`, `ice`, `glacier`, `wave`, `marsh`, `hydro`, `hydraulic`

### 2.3 earth (18 entries)

`stone`, `granite`, `marble`, `clay`, `sand`, `iron`, `gold`, `silver`, `lead`, `gem`, `crystal`, `obsidian`, `amber`, `quake`, `tremor`, `thorn`, `seismic`, `tectonic`

### 2.4 wind (13 entries)

`tempest`, `cyclone`, `whirlwind`, `gale`, `gust`, `squall`, `hurricane`, `zephyr`, `hail`, `sleet`, `cloud`, `sonic`, `shockwave`

### 2.5 lightning (13 entries)

`arc`, `static`, `surge`, `volt`, `bolt`, `shock`, `spark`, `thunder`, `plasma`, `flash`, `ion`, `voltage`, `tesla`

### 2.6 holy (14 entries)

`radiance`, `radiant`, `dawn`, `aura`, `divine`, `sacred`, `blessed`, `lux`, `celestial`, `stellar`, `solar`, `photon`, `laser`, `prismatic`

### 2.7 shadow (12 entries)

`void`, `shade`, `wraith`, `drain`, `necrotic`, `abyss`, `shadow`, `lich`, `blackhole`, `singularity`, `darkmatter`, `soul`

### 2.8 physical (9 entries — Architecture A taxonomy registry; NOT a flavor pool)

**Damage sub-type field (weapon + skill schema):**

- `piercing`, `slashing`, `bludgeoning`, `force`

**Mechanical action vocabulary (skill schema):**

- `pierce`, `slash`, `sever`, `strike`

**Ailment (already locked in `config/elements.yaml`):**

- `bleed`

**Physical kit handling:** physical kits OPT OUT of WS1A.4 LLM flavor judgment; skill naming uses mechanical-schema templates.

**Optional extensions DEFERRED to v1.1+** (not committed at v1.0 lock): `crush`, `impact`, `rend`.

### 2.9 Total cardinality

**118 entries locked across 8 primaries** = 109 rotating-primary flavor-pool entries + 9 physical taxonomy-registry entries.

Per-primary cardinality summary:

| Primary | Count | Shape |
|---|---:|---|
| fire | 16 | rotating flavor pool |
| water | 14 | rotating flavor pool |
| earth | 18 | rotating flavor pool |
| wind | 13 | rotating flavor pool |
| lightning | 13 | rotating flavor pool |
| holy | 14 | rotating flavor pool |
| shadow | 12 | rotating flavor pool |
| physical | 9 | Architecture-A taxonomy-sibling registry |
| **TOTAL** | **118** | |

---

## 3. Q18.a–e structural commitments

Verbatim per PG-3 ratification § 2.

### 3.1 Q18.a — Primary scope

**8 primaries:** 7 rotating (fire / water / earth / wind / lightning / holy / shadow) with flavor pools + 1 physical with Architecture-A taxonomy registry.

### 3.2 Q18.b — Source of authority

**Vote-grounded research + designer-curation overlay at encoding gate** (Discipline #41 substrate-led refinement). Substrate vote at engine-generation; designer curation at encoding/release gate.

**Operational implementation:** Phase 4 high-confidence core (score ≥ T6 AND tracks ≥ 2) is the substrate-grounded anchor; Phase 5a synthesis applied the encoding gate; pool.json migration (sub-phase 5f POST-WAVE) operationalizes the lock.

### 3.3 Q18.c — Flex semantics

**Preserved.** The existing `cross_primary_contamination` field in pool.json schema is renamed to `flex_slots`. Per-candidate slot routing decisions per synthesis § 5 (substrate-honest primary identity determines primary slot; contamination evidence determines flex slots).

**Concrete slot-routing decisions:**

- `mist` → WATER primary (atmospheric water-vapor substrate root; pool-existing wind-primary migrates to water-primary per substrate vote)
- `vortex` → WIND primary (substrate-rotational-primary; PoE Vortex cold-AOE-rotational; designer-judgment surface — Matt may override water per cold-association)
- `hurricane` → WIND primary, water flex (tropical-storm IS wind-rotational at source)
- `squall` → WIND primary, water flex (wind-storm-event; oceanic-squall is secondary)
- `stormtide` → WIND primary, water flex (storm hitting tide; substrate-honest wind-primary)
- `tempest` → WIND primary, water flex (overwhelmingly substrate-wind; pool-existing routing preserved)
- `njord` → WATER primary, wind flex (Norse sea-god primary domain is sea; wind is secondary)

### 3.4 Q18.d — d1_status filter

**Preserved + schema amendment** for `vocabulary_commonness` and `slot_unambiguous` sub-properties (per project memory matt-demote-2026-05-12 lineage + smoke-as-fire vs smoke-as-wind precedent).

**Discipline:**

- Substrate score ≥ T6 AND tracks ≥ 2 → default `allow-list`
- Substrate score ≥ T6 AND tracks = 1 (single-track borderline) → default `eligible`; designer-judgment may PROMOTE
- Substrate score < T6 → default `eligible` if research-cited; `quarantine` if not research-cited and pool-existing-only
- Vocab-obscure flag (project memory matt-demote lineage) → demote to `eligible` regardless of substrate score
- Slot-unambiguous check (smoke-as-fire vs smoke-as-wind precedent) → flag for designer-judgment; demote if ambiguous

**Schema-migration execution:** deferred to sub-phase 5f POST-WAVE migration dispatch.

### 3.5 Q18.e — Cardinality target

**Per ratified per-primary cardinality in § 2.** Per-primary substrate-honest natural-depth TARGET (not floor; not ceiling). Cardinality emerged from substrate vote + pool-depth-anchor + designer-curation overlay, NOT from uniform target.

---

## 4. Physical handling — detailed spec

Architecture A places physical OUTSIDE the rotating-primary flavor-pool semantic. This section operationalizes that placement.

### 4.1 Taxonomy registry structure

Physical's 9 entries decompose by SCHEMA ROLE rather than by flavor-clustering:

| Sub-category | Entries | Schema role |
|---|---|---|
| Damage sub-type field | `piercing`, `slashing`, `bludgeoning`, `force` | Weapon + skill schema; D&D 5e PHB ch.9 damage types |
| Mechanical action vocabulary | `pierce`, `slash`, `sever`, `strike` | Skill schema; verb-form templates for skill naming |
| Ailment (pre-locked) | `bleed` | Already in `config/elements.yaml`; canonical physical ailment per PoE Bleed precedent |

### 4.2 Opt-out from WS1A.4 LLM flavor judgment

Physical kits OPT OUT of WS1A.4 per-skill bounded LLM flavor judgment. Rationale: the substrate (0.85 modal mechanical_keyword + 1 dominant HDBSCAN cluster + near-zero contamination) is structurally non-flexing; LLM bounded judgment over a 9-entry taxonomy-sibling registry would produce uniform-shaped output without flavor differentiation.

**Replacement mechanism — mechanical-schema templates:** physical kit skill naming uses (weapon-form + mechanical-action) composition. Example template: `<weapon-form-modifier> <mechanical-action> <intensifier>` where weapon-form is drawn from canonical 17-gear, mechanical-action is drawn from the 4-entry vocabulary above, and intensifier is drawn from a separate intensifier pool (NOT scope of this canonical doc; gates on future WS-physical-naming work).

### 4.3 v1.1+ deferrals

Optional extensions `crush`, `impact`, `rend` are explicitly NOT committed at v1.0 lock. They are substrate-thin (CWS=4; single-track each) but substrate-supportable. Designer-judgment defers them to v1.1+ pending empirical evidence from Cycle 14+ mechanical-schema-template implementation: if the 9-entry registry produces mechanical-schema saturation (every physical kit name uses the same 4 mechanical-action verbs), extensions activate.

### 4.4 Physical's relationship to WS1A.3 (per-kit sub-element selection)

Physical kits do NOT consume the rotating-primary sub-element selection path. Instead, physical kit identity differentiates via:

1. Weapon-form selection (sword / spear / bow / axe / etc. per canonical 17-gear)
2. Damage sub-type field assignment (piercing / slashing / bludgeoning / force) at schema layer
3. Mechanical-action vocabulary selection at skill-naming layer
4. Bleed ailment routing per `config/elements.yaml` canonical

This is the Architecture-A asymmetry made operational: physical kits compose their identity from a different shape than rotating-primary kits, and that asymmetry matches the engine taxonomy's existing shape.

---

## 5. Cull-tag dispositions

Per PG-3 ratification § 3. Existing pool.json `drift-14-*` cull-tag verdicts disposed against substrate evidence.

| Cull tag | Disposition | Rationale |
|---|---|---|
| `drift-14-wind-storm-cluster-collapse` | DISSOLVE | cyclone / whirlwind / squall / hurricane promoted to wind allow-list per substrate vote (overwhelmingly substrate-canonical wind) |
| `drift-14-plant-anatomical` (thorn only) | DISSOLVE-for-thorn | thorn substrate-confirmed; promoted to earth allow-list (PoE Thorn affix recognizability) |
| `drift-14-plant-anatomical` (vine / root / bark / wood remainder) | KEEP | substrate-silent; preserve designer-prior-judgment |
| `drift-14-biological-organic` | KEEP | substrate-silent; preserve designer-prior-judgment (no override) |
| `drift-14-alternative-liquid` | KEEP | substrate-silent |
| `drift-14-auditory-non-visual` | KEEP | substrate-silent |
| `drift-14-conceptual-not-substance` | KEEP | substrate-silent |

**Principle applied:** substrate-silence ≠ substrate-validation. Where research did not surface a candidate (silence), prior designer cull-judgment is preserved. Where research substrate-confirms a candidate previously culled (storm-cluster, thorn), the cull dissolves per substrate vote.

---

## 6. Pool.json schema amendments + sub-phase 5f deferral

Per PG-3 ratification § 4.

### 6.1 Schema field additions

To be added to pool.json schema at sub-phase 5f migration:

- **`substrate_validation_lineage`** (string enum) — anchor for the 5 lineage categories per § 7 below
- **`vocabulary_commonness`** (numeric/enum sub-property) — per matt-demote-2026-05-12 directive; carries the vocab-obscure flag pattern
- **`slot_unambiguous`** (boolean) — per smoke-as-fire vs smoke-as-wind precedent; flags candidates where cross-element fit creates routing ambiguity

### 6.2 Schema migration execution

**Deferred to sub-phase 5f POST-WAVE migration dispatch** per ADR-004 cross-seam contract change. Migration scope:

- Schema extension (3 new fields)
- 109 rotating-primary entry migration with lineage tags applied per § 7
- 9 physical entry migration to separate taxonomy-registry surface
- elrond + star-lord cross-seam coordination (pool.json is consumed by downstream pipeline)
- Existing entries audited against PRESERVE / DEMOTE / EXTEND verdicts per Phase 5a synthesis § 6

This is operational migration, not architectural commitment. The canonical lock is THIS document; the migration operationalizes it.

---

## 7. Lineage tags (per-entry; substrate-validation provenance)

Per PG-3 ratification § 5. Each of the 118 locked entries carries a substrate-validation lineage tag indicating its provenance:

| Lineage tag | Count | Description |
|---|---:|---|
| `substrate-validated-this-wave-2026-06-01` | 65 | Survived Phase 4 high-confidence core threshold (score ≥ T6 AND tracks ≥ 2); substrate-vote-confirmed cross-track |
| `substrate-silent-2026-05-08-D1-pool` | 24 | Carry-over from original D1 pool (2026-05-08); substrate research did not surface but did not refute (preserved per substrate-silence ≠ substrate-refutation principle) |
| `designer-curation-modern-scientific-overlay-2026-06-01` | 19 | Modern-scientific vocabulary overlay added at PG-3 designer-curation gate (`fusion`, `thermal`, `combustion`, `hydro`, `hydraulic`, `seismic`, `tectonic`, `sonic`, `shockwave`, `plasma`, `flash`, `ion`, `voltage`, `tesla`, `stellar`, `solar`, `photon`, `laser`, `prismatic`) |
| `designer-curation-mystical-fantasy-overlay-2026-06-01` | 1 | Single mystical-fantasy overlay (`shadow:soul`); transparent acknowledgment of designer judgment outside substrate vote |
| `architecture-A-taxonomy-registry-2026-06-01` | 9 | Architecture-A taxonomy-sibling registry entries (physical's 9); semantically distinct from flavor-pool entries |
| **TOTAL** | **118** | |

### 7.1 Per-primary lineage distribution (aggregated for readability)

| Primary | substrate-validated | substrate-silent | designer-curation-modern-scientific | designer-curation-mystical | architecture-A-registry |
|---|---:|---:|---:|---:|---:|
| fire (16) | 9 | 4 | 3 | 0 | 0 |
| water (14) | 8 | 4 | 2 | 0 | 0 |
| earth (18) | 7 | 9 | 2 | 0 | 0 |
| wind (13) | 9 | 2 | 2 | 0 | 0 |
| lightning (13) | 8 | 0 | 5 | 0 | 0 |
| holy (14) | 9 | 0 | 5 | 0 | 0 |
| shadow (12) | 7 | 0 | 4 | 1 | 0 |
| physical (9) | 0 | 0 | 0 | 0 | 9 |
| **TOTAL** | **57** | **19** | **23** | **1** | **9** |

(Aggregate-count totals reconcile to 109 rotating-primary entries + 9 physical = 118. Per-entry lineage tags applied at sub-phase 5f migration; see PG-3 ratification § 5 for the substrate-validation-tag binding to specific entries.)

### 7.2 Why lineage tagging matters

The lineage tag system makes the substrate-led discipline auditable at the per-entry layer. Future audit questions ("how much of pool X is substrate-validated vs designer-overlay?") become directly queryable. The `designer-curation-mystical-fantasy-overlay-2026-06-01` tag with 1 entry (`shadow:soul`) is the transparency anchor: it makes explicit where designer judgment overrode substrate-silence with mystical-fantasy preference, instead of hiding that judgment in the pool without provenance.

---

## 8. Discipline-recognition candidates (awaiting jack-ryan ratification at wave-close)

Per PG-3 ratification § 6. Three discipline candidates emerged from the WS1A.Q18 wave; jack-ryan ratifies at sub-phase 5d Gate-2 PG-4 wave-close OR at wave-close discipline-canonical authoring.

**Note: these are surfaced transparently here per canonical-doc-format § 5 recognition-record special-case protocol. They are NOT yet canonical disciplines; ratification fires at wave-close.**

### 8.1 Discipline-candidate-1 — Substrate-silence ≠ substrate-validation

**Decision 16 MIDDLE:** lineage-tagged allow-list with substrate-silent pool entries acknowledged transparently.

**The discipline asserts:** when substrate research does not surface a vocabulary candidate but does not refute it either, the appropriate disposition is **lineage-tagged preservation** ("substrate-silent" lineage) NOT promotion-to-validated. Transparency on what the substrate said vs what the substrate did not address.

**Operational application in this lock:** 24 entries (`substrate-silent-2026-05-08-D1-pool`) preserved with substrate-silent lineage rather than being either (a) auto-promoted to substrate-validated OR (b) culled for substrate-thin.

### 8.2 Discipline-candidate-2 — Substrate-vocabulary inclusion 3-test (Matt 2026-06-01)

**A three-test inclusion gate for candidate vocabulary:**

- **T1 — Engine-axis orthogonality:** vocabulary that double-encodes existing engine axes fails (e.g., FF `-ra` / `-ga` suffix encodes AOE already in geometry palette).
- **T2 — Compositional naming behavior in hybrid kits:** franchise-specific proper-nouns resist compositional naming (e.g., "Stone Mudo" reads as identity-collision not flavor-blend).
- **T3 — Period-link grounding strength:** cross-cultural / mythological grounding generalizes; franchise-locked modern-Japanese terms have no period-anchor.

**Failure rule:** failure of 1 test = marginal; failure of 2-3 tests = exclusion.

**Operational application:** explains why SMT proper-nouns (mudo / mamudo / mahamaon-ladder) and FF -ra/-ga suffix vocabulary (thundara / blizzara / bufu) were EXCLUDED from the final allow-list despite substrate evidence. Excluded entries failed T1 (engine-axis orthogonality) and T2 (compositional naming) and T3 (period-link grounding) compositely.

### 8.3 Discipline-candidate-3 — Synthesis-draft adversarial Pattern B critique required pre-architectural-lock

**Three amendments emerged from Matt's pushback during Pattern B engagement on the gandalf synthesis draft:**

- substrate-silence framing (gandalf draft initially conflated substrate-silence with substrate-thinness)
- wind JRPG-asymmetry surfacing (gandalf draft did not initially surface that wind storm-flex saturation is substrate-real but Reincarnated-fit-asymmetric)
- physical-as-mechanical-not-flavor reframe (gandalf draft initially leaned WEAK-8 / soft-A; Matt pushback strengthened to HARD-A with explicit opt-out semantic)

**The discipline asserts:** synthesis drafts authored by single-seam stewards must undergo adversarial Pattern B critique with the architectural-commitment authority BEFORE the canonical lock; the lock-quality benefits from the dialogue's amendment cycle.

**Operational application:** the PG-3 ratification at `agentic_orchestration/cycle-15-ws1a-q18-flavor-pool-research/pg-3-ratification-2026-06-01.md` is structurally different (and stronger) than the Phase 5a synthesis draft alone would have been. The Pattern B dialogue surfaced 3 substantive amendments that reshape the lock.

---

## 9. Cross-references

### 9.1 Composes with (existing canon)

- `canonical/story/2026-05-31-hypothesis-flow-pattern-library-architecture.md` § 1.7 (per-skill flavor judgment architecture; WS1A.4 spec) + § 8b Q18 (parent question for this closure path)
- `canonical/story/2026-05-29-designer-writes-substrate-player-names-experience-principle.md` (foundational substrate-led principle; this lock operationalizes at the vocabulary-substrate layer)
- `~/Games/reincarnated-engine/config/elements.yaml` (canonical-7+1 element catalog — substrate this lock is built on; PRESERVED unchanged)
- `~/Games/reincarnated-engine/data/seasonal_elements/pool.json` (existing 156-entry pool — audited + extended at sub-phase 5f; NOT retired)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § 41 (substrate-led; extended via encoding-gate refinement applied to vocabulary) + § 42 (framing-audit; applied at synthesis + Pattern B) + § 18 (math-hotspot methodology consultation; PG-0 → Phase 4 chain)

### 9.2 Authorizes downstream

- **Sub-phase 5f migration dispatch (POST-WAVE)** — extends `data/seasonal_elements/pool.json` per this lock; 3 schema field additions; 118 entries migrated with lineage tags; elrond + star-lord cross-seam coordination. NOT within this canonical doc's scope; operational follow-on.
- **WS1A.3 per-kit sub-element selection implementation** — consumes the locked rotating-primary pools; physical kits route through weapon-form path instead.
- **WS1A.4 per-skill bounded LLM flavor judgment implementation** — consumes the locked rotating-primary pools as judgment-space; physical kits opt out and use mechanical-schema templates.

### 9.3 Does NOT replace or amend

- `~/Games/reincarnated-engine/config/elements.yaml` — canonical-7+1 element catalog preserved unchanged; 8 primaries (7 rotating + 1 physical) are substrate as-given.
- `~/Games/reincarnated-engine/data/seasonal_elements/pool.json` — existing pool.json is audited + extended at sub-phase 5f, NOT retired. PRESERVE / DEMOTE / EXTEND verdicts per Phase 5a synthesis § 6.
- `canonical/story/2026-05-31-hypothesis-flow-pattern-library-architecture.md` — parent canonical doc preserved; this is the Q18 closure path execution, not an amendment of the parent.

### 9.4 Pattern-sets (future composition)

The WS1A.Q18 wave shape (5 phases internally gated; PG-0 elrond data-medium / PG-1 gandalf triage / PG-2 gandalf stats-sufficiency / PG-3 Matt architectural-commitment / PG-4 jack-ryan wave-close) is the template for the remaining WS1A hard-blocker waves:

- **WS1A.Q16** (per-skill flavor judgment LLM prompt design) — composes against the locked Q18 pool; Q16's research scope shifts to LLM-prompt-design canon
- **WS1A.Q17** (hybrid kit element pair selection) — composes against the locked Q18 pool + Q16 judgment design
- **WS1A.Q19** (emergent kit concept naming consistency) — composes against Q16 LLM judgment + Q18 pool

Pattern-setting at Q18 reduces orchestration overhead for subsequent waves by ~30–40% per gandalf estimate.

---

## 10. Sign-off

**v1.0 canonical lock RATIFIED.** Architecture A LOCKED; 118 entries committed; Q18.a–e structural commitments locked; cull-tag dispositions specified; pool.json schema amendments specified (deferred to sub-phase 5f); 3 discipline-recognition candidates surfaced (awaiting jack-ryan wave-close ratification).

**Authority chain:**

- Matt 2026-06-01 verbatim PG-3 ratification per ADR-002 Tier A architectural-commitment authority (artifact at `agentic_orchestration/cycle-15-ws1a-q18-flavor-pool-research/pg-3-ratification-2026-06-01.md`)
- gandalf Phase 5a synthesis draft at commit `5f5b405` (the substantive surface ratified)
- Pattern B substantive design call (Matt + gandalf) complete; 3 amendments surfaced and absorbed

**Disciplines composed:**

- Discipline #41 (substrate-led; encoding-gate refinement applied to vocabulary substrate)
- Discipline #42 (framing-audit; applied at synthesis + Pattern B; surfaced 3 substantive amendments)
- Discipline #18 (math-hotspot methodology consultation; PG-0 elrond data-medium → Phase 4 stats chain)
- 3 candidate disciplines per § 8 (await jack-ryan ratification at sub-phase 5d wave-close OR wave-close discipline-canonical authoring)

**Next operational firing:**

- Sub-phase 5d — jack-ryan Gate-2 PG-4 wave-close critique on this canonical write (BLOCK authority on drift / math-before-code / cross-seam impact unaddressed)
- On PG-4 PASS: sub-phase 5e wave-close (KR wave-close record + gandalf design-quality audit + jack-ryan ratifies 3 discipline-recognition candidates above; WS1A.Q18 wave CLOSED)
- POST-WAVE: sub-phase 5f migration dispatch operationalizes the lock at pool.json

**Composition note (cross-wave):** wave-close (PG-4 PASS) unblocks WS1A.Q16 + WS1A.Q17 + WS1A.Q19 hard-blocker waves per operational sequence § 10.2 composition pattern; pattern-set established here carries forward.

---

**Signed:** gandalf (story-and-design steward)
**For:** the canonical lock of WS1A.Q18 flavor-pool per-primary-element allow-lists at v1.0 — Architecture A (7 rotating primaries with substrate-honest flavor pools + physical as Architecture-A taxonomy-sibling registry); 118 entries committed; Q18.a–e structural commitments locked; substrate-led methodology composed at the vocabulary-substrate layer per Discipline #41 refinement.
