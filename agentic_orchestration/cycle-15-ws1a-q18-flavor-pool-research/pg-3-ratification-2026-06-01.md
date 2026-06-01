# WS1A.Q18 PG-3 Architectural-Commitment Lock — Matt Pattern B Ratification

**STATUS:** RATIFIED (PG-3 architectural-commitment lock per ADR-002 Tier A Matt authority)
**Date:** 2026-06-01
**Phase-gate:** PG-3 (post-Phase-5b Pattern B Matt-Gandalf dialogue; wave-terminus architectural commitment)
**Authority:** Matt 2026-06-01 verbatim ratification (Pattern B session with gandalf complete)
**Companion docs:**
- `gandalf/notes/2026-06-01-q18-flavor-pool-research-synthesis.md` (Phase 5a synthesis draft; commit `5f5b405`)
- `gandalf/notes/2026-06-01-q18-gate-2-stats-ratification.md` (PG-2 ratification; commit `5ad97e7`)
- `elrond/analysis/element-flavor-mapping-stats-2026-06-01.md` (Phase 4 stats verdict; commit `abd4782`)
- `gandalf/notes/2026-06-01-q18-flavor-pool-research-operational-sequence.md` (authoritative operational sequence)
- `cycle-15-ws1a-q18-flavor-pool-research/wave-state.md` (orchestration state)
- `~/Games/reincarnated-engine/config/elements.yaml` (canonical-7+1 element catalog — substrate this lock is built on)
- `~/Games/reincarnated-engine/data/seasonal_elements/pool.json` (existing pool — sub-phase 5f migration target)

---

## 0. KEYSTONE

**Architecture A LOCKED** — 7-primary rotating flavor pools + physical-as-taxonomy-sibling.

7 rotating primaries with flavor pools (fire / water / earth / wind / lightning / holy / shadow); physical is a taxonomy-sibling registry (damage sub-type field + mechanical action vocabulary + already-locked bleed ailment), NOT a flavor pool. Physical kits opt out of WS1A.4 LLM judgment; skill naming via mechanical-schema templates.

---

## 1. Per-primary allow-lists (FINAL)

### 1.1 fire (16 entries)

`ember`, `cinder`, `blaze`, `scorch`, `inferno`, `ignite`, `fira`, `lava`, `magma`, `charcoal`, `char`, `brand`, `flare`, `fusion`, `thermal`, `combustion`

### 1.2 water (14 entries)

`tide`, `torrent`, `glacial`, `brine`, `aqua`, `frost`, `chill`, `mist`, `ice`, `glacier`, `wave`, `marsh`, `hydro`, `hydraulic`

### 1.3 earth (18 entries)

`stone`, `granite`, `marble`, `clay`, `sand`, `iron`, `gold`, `silver`, `lead`, `gem`, `crystal`, `obsidian`, `amber`, `quake`, `tremor`, `thorn`, `seismic`, `tectonic`

### 1.4 wind (13 entries)

`tempest`, `cyclone`, `whirlwind`, `gale`, `gust`, `squall`, `hurricane`, `zephyr`, `hail`, `sleet`, `cloud`, `sonic`, `shockwave`

### 1.5 lightning (13 entries)

`arc`, `static`, `surge`, `volt`, `bolt`, `shock`, `spark`, `thunder`, `plasma`, `flash`, `ion`, `voltage`, `tesla`

### 1.6 holy (14 entries)

`radiance`, `radiant`, `dawn`, `aura`, `divine`, `sacred`, `blessed`, `lux`, `celestial`, `stellar`, `solar`, `photon`, `laser`, `prismatic`

### 1.7 shadow (12 entries)

`void`, `shade`, `wraith`, `drain`, `necrotic`, `abyss`, `shadow`, `lich`, `blackhole`, `singularity`, `darkmatter`, `soul`

### 1.8 physical (9 entries — Architecture A taxonomy registry; NOT a flavor pool)

**Damage sub-type field (weapon + skill schema):**
- `piercing`, `slashing`, `bludgeoning`, `force`

**Mechanical action vocabulary (skill schema):**
- `pierce`, `slash`, `sever`, `strike`

**Ailment (already locked in `config/elements.yaml`):**
- `bleed`

**Physical kit handling:** physical kits OPT OUT of WS1A.4 LLM flavor judgment; skill naming uses mechanical-schema templates.

**Optional extensions DEFERRED to v1.1+:** `crush`, `impact`, `rend` (not committed at v1.0 lock).

### 1.9 Total

118 entries locked across 8 primaries (109 rotating-primary flavor pool + 9 physical taxonomy registry).

---

## 2. Q18.a-e structural commitments

### 2.1 Q18.a — Primary scope

**8 primaries** (7 rotating with flavor pools + physical Architecture-A taxonomy registry).

### 2.2 Q18.b — Source of authority

**Vote-grounded research + designer-curation overlay at encoding gate** (Discipline #41 substrate-led refinement). Substrate vote at engine-generation; designer curation at encoding/release gate.

### 2.3 Q18.c — Flex semantics

**Preserved** (`cross_primary_contamination` field renamed to `flex_slots`; per-candidate slot routing per synthesis § 5).

Concrete slot-routing decisions:
- `mist` → WATER
- `vortex` → WIND
- `hurricane` / `squall` / `stormtide` / `tempest` → WIND (per synthesis § 5)
- `njord` → WATER (per synthesis § 5)

### 2.4 Q18.d — d1_status filter

**Preserved + schema amendment** for `vocabulary_commonness` and `slot_unambiguous` sub-properties (per project memory: matt-demote-2026-05-12 + smoke-as-fire vs smoke-as-wind precedent).

### 2.5 Q18.e — Cardinality target

**Per ratified per-primary cardinality above** (§ 1).

---

## 3. Cull-tag dispositions

| Cull tag | Disposition | Rationale |
|---|---|---|
| `drift-14-wind-storm-cluster-collapse` | DISSOLVE | cyclone / whirlwind / squall / hurricane promoted to wind allow-list |
| `drift-14-plant-anatomical` | DISSOLVE-for-thorn | thorn substrate-confirmed; promoted to earth allow-list |
| `drift-14-biological-organic` | KEEP | substrate-silent; no override |
| `drift-14-alternative-liquid` | KEEP | substrate-silent |
| `drift-14-auditory-non-visual` | KEEP | substrate-silent |
| `drift-14-conceptual-not-substance` | KEEP | substrate-silent |

---

## 4. Pool.json schema amendments (deferred to sub-phase 5f POST-WAVE migration)

Add fields:
- `substrate_validation_lineage` (string enum) — anchor for the 5 lineage categories below
- `vocabulary_commonness` (numeric/enum sub-property) — per matt-demote-2026-05-12 directive
- `slot_unambiguous` (boolean) — per smoke-as-fire vs smoke-as-wind precedent

**Schema-migration execution:** deferred to sub-phase 5f (POST-WAVE; cross-seam contract change per ADR-004; elrond + star-lord coordination).

---

## 5. Lineage tags (canonical write applies per-entry)

The canonical write at Phase 5c applies these tags per-entry:

| Lineage tag | Count | Description |
|---|---|---|
| `substrate-validated-this-wave-2026-06-01` | 65 entries | Survived Phase 4 high-confidence core threshold (score ≥ T6 AND tracks ≥ 2) |
| `substrate-silent-2026-05-08-D1-pool` | 24 entries | Carry-over from original D1 pool; substrate research did not surface but did not refute |
| `designer-curation-modern-scientific-overlay-2026-06-01` | 19 entries | Modern-scientific vocabulary overlay (fusion, hydraulic, photon, voltage, blackhole, etc.) added at PG-3 designer-curation gate |
| `designer-curation-mystical-fantasy-overlay-2026-06-01` | 1 entry (`shadow:soul`) | Single mystical-fantasy overlay; transparent acknowledgment |
| `architecture-A-taxonomy-registry-2026-06-01` | 9 entries (physical) | Architecture-A taxonomy-sibling; not a flavor pool |

**Total: 118 entries locked.**

---

## 6. Discipline-recognition candidates (for jack-ryan ratification at wave-close)

The following emerged from the WS1A.Q18 wave as Discipline #N candidates. jack-ryan ratifies at sub-phase 5d Gate-2 PG-4 wave-close OR at wave-close discipline-canonical authoring.

### 6.1 Substrate-silence ≠ substrate-validation

(Decision 16 MIDDLE: lineage-tagged allow-list with substrate-silent pool entries acknowledged transparently.)

The discipline asserts: when substrate research does not surface a vocabulary candidate but does not refute it either, the appropriate disposition is **lineage-tagged preservation** ("substrate-silent" lineage) NOT promotion-to-validated. Transparency on what the substrate said vs what the substrate did not address.

### 6.2 Substrate-vocabulary inclusion 3-test (Matt 2026-06-01)

A three-test inclusion gate for candidate vocabulary:

- **T1 — Engine-axis orthogonality:** vocabulary that double-encodes existing engine axes fails (e.g., FF `-ra` / `-ga` suffix encodes AOE already in geometry palette).
- **T2 — Compositional naming behavior in hybrid kits:** franchise-specific proper-nouns resist compositional naming (e.g., "Stone Mudo" reads as identity-collision not flavor-blend).
- **T3 — Period-link grounding strength:** cross-cultural / mythological grounding generalizes; franchise-locked modern-Japanese terms have no period-anchor.

**Failure rule:** failure of 1 test = marginal; failure of 2-3 tests = exclusion.

### 6.3 Synthesis-draft adversarial Pattern B critique required pre-architectural-lock

Three amendments emerged from Matt's pushback during Pattern B engagement on the gandalf synthesis draft:
- substrate-silence framing
- wind JRPG-asymmetry surfacing
- physical-as-mechanical-not-flavor reframe

The discipline asserts: synthesis drafts authored by single-seam stewards must undergo adversarial Pattern B critique with the architectural-commitment authority BEFORE the canonical lock; the lock-quality benefits from the dialogue's amendment cycle.

---

## 7. KR next-actions (post-PG-3)

1. **Fire Phase 5c canonical write** at `canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md` (gandalf-as-sub-agent invocation; consumes synthesis at `gandalf/notes/2026-06-01-q18-flavor-pool-research-synthesis.md` PLUS this PG-3 ratification document).

2. **Update `canonical/00-ground-state.md` § 1** — add new CURRENT entry for the flavor-pool lock.

3. **Update `canonical/02-roadmap.md`** — move WS1A.Q18 to closed.

4. **Route Phase 5c output to jack-ryan Gate-2 PG-4** (wave-close criterion; BLOCK authority on drift / math-before-code / cross-seam-impact-unaddressed).

5. **On PG-4 PASS, fire sub-phase 5e wave-close:**
   - KR wave-close record at `canonical/story/2026-06-01-ws1a-q18-flavor-pool-wave-close-record.md`
   - gandalf design-quality audit per OP § 4.6
   - jack-ryan ratification of 3 discipline-recognition candidates above
   - Wave-state CLOSED

6. **Author sub-phase 5f migration dispatch (POST-WAVE):**
   - `pool.json` schema extension (3 new fields per § 4)
   - 109 rotating-primary entry migration with lineage tags applied per § 5
   - 9 physical entry migration to separate taxonomy registry surface
   - elrond + star-lord cross-seam touches
   - Operational; not within WS1A.Q18 wave scope

---

## 8. Wave-close criterion

Wave closes on **PG-4 PASS** (jack-ryan Gate-2 on canonical write).

On wave-close, **Q16 / Q17 / Q19 hard-blocker waves unblock** per operational sequence § 10.2 composition pattern (the pattern-set this wave establishes carries forward for the remaining WS1A hard-blocker Q-waves).

---

## 9. Sign-off

**PG-3 verdict: RATIFIED** — Architecture A LOCKED; 118 entries committed; Q18.a-e structural commitments locked; cull-tag dispositions specified; pool.json schema amendments specified (deferred to sub-phase 5f); 3 discipline-recognition candidates surfaced.

**Authority chain:**
- Matt 2026-06-01 verbatim ratification per ADR-002 Tier A architectural-commitment authority
- gandalf Phase 5a synthesis draft commit `5f5b405` (the substantive surface ratified)
- Pattern B substantive design call with gandalf complete

**Disciplines composed:**
- Discipline #41 (substrate-led; encoding-gate refinement)
- Discipline #42 (framing-audit; applied at synthesis + Pattern B)
- Discipline #18 (math-hotspot methodology consultation; PG-0 → Phase 4 chain)
- 3 candidate disciplines per § 6 above (await jack-ryan ratification at wave-close)

**Next:** KR fires Phase 5c canonical write per § 7.1.

**End of PG-3 ratification.**
