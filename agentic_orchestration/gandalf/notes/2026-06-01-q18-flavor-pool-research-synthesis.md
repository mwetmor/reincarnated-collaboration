# WS1A.Q18 Phase 5a — Gandalf Synthesis Draft

**STATUS:** DRAFT (gandalf-authored Phase 5a synthesis; pre-PG-3; surfaces to Matt for Phase 5b Pattern B architectural-commitment lock)
**Date:** 2026-06-01
**Author:** gandalf (story-and-design steward)
**Phase / phase-gate:** Phase 5a synthesis draft → PG-3 (Matt Phase 5b Pattern B architectural-commitment lock)
**Mode:** Pattern A-deep / authoring scope
**Authority:** Matt 2026-06-01 verbatim "hand to KR to fire the wave" + gandalf PG-2 RATIFIED at commit `5ad97e7` + operational sequence § 2 Phase 5a (synthesis-curation is gandalf seam authority; PG-3 architectural-commitment lock is Matt Tier A authority per ADR-002)
**Companion docs:**
- `agentic_orchestration/gandalf/notes/2026-06-01-q18-gate-2-stats-ratification.md` (PG-2 RATIFIED; forward notes operationalized here)
- `agentic_orchestration/gandalf/notes/2026-06-01-q18-gate-1-triage-ratification.md` (PG-1 amendments operationalized here)
- `agentic_orchestration/elrond/analysis/element-flavor-mapping-stats-2026-06-01.md` (Phase 4 stats verdict — empirical anchor)
- `agentic_orchestration/elrond/analysis/q18_flavor_stats_results_2026-06-01.json` (raw per-candidate detail — anchor for per-primary curation tables)
- `agentic_orchestration/gandalf/notes/2026-06-01-q18-flavor-pool-research-operational-sequence.md` § 0 + § 2 Phase 5a (canonical lock target structure)
- `~/Games/reincarnated-engine/data/seasonal_elements/pool.json` (existing 156-entry pool; PRESERVE/DEMOTE/EXTEND audit anchor)
- `~/Games/reincarnated-engine/config/elements.yaml` (canonical-7+1 element catalog — substrate primaries)
- `agentic_orchestration/cycle-15-ws1a-q18-flavor-pool-research/wave-state.md` (wave state; Phase 5a FIRING)

---

## 0. TL;DR + Matt-facing summary

### 0.1 What's settled substrate-led (gandalf seam authority at Phase 5a)

- **Per-primary allow-list TARGETS** (substrate-grounded; cardinality as TARGET not floor): fire ~14, water ~14, earth ~22 (preserve pool depth), wind ~12 (substantial reshape from existing 7), lightning ~10, holy ~10, shadow ~12, physical ~9 (taxonomic shape; Architecture-A-vs-B-dependent for slot meaning).
- **Curation routing** for water↔wind=7 contamination: hurricane / squall / stormtide / tempest → WIND primary; mist / njord → WATER primary; vortex → designer-judgment surface (lean wind per PoE Vortex precedent).
- **Q18.b source-of-authority**: vote-grounded research + designer curation overlay (substrate-led per Discipline #41; designer curates AT the encoding gate post-research).
- **Q18.c flex semantics**: `cross_primary_contamination` substrate-honestly captured via `flex_slots` field in pool.json schema; per-candidate slot routing decision recorded in synthesis.
- **Q18.d d1_status filter discipline**: vocabulary_commonness sub-property (per project memory matt-demote-2026-05-12 lineage) + slot_unambiguous check (smoke-as-fire vs smoke-as-wind precedent) become explicit d1_status amendment criteria.
- **Existing-pool audit (156 entries)**: 56 PRESERVE / 26 DEMOTE-from-allow-list / 0 REMOVE / 24 EXTEND (new allow-list additions from substrate evidence); see § 6.
- **Borderline disposition** (92 single-track + lux + celestial): per-candidate verdicts in § 7; 18 KEEP / 35 DROP / 39 DEFER-WITH-CROSS-TRACK-REQUIRED.

### 0.2 What surfaces to Matt at PG-3 (architectural-commitment territory; Matt Tier A authority)

- **Decision 1 — Architecture A vs B** (7-vs-8 lock): both architectures presented with empirical + genre-canonical + Reincarnated-fit evidence. Gandalf soft lean Architecture A (7-primary rotating + physical-as-taxonomy-sibling). § 2 surfaces the choice; § 11 enumerates Matt's PG-3 decisions.
- **Decision 2 — Per-primary allow-list approval**: gandalf has drafted per-primary curated allow-list (§ 4); Matt ratifies / amends / locks. Cardinality TARGETS in § 4 are gandalf-substrate-honest reads; Matt may push them per design preference. Per-candidate inclusion is substrate-grounded.
- **Decision 3 — Q18.a-e structural commitments**: § 5 enumerates the 5 structural decisions; gandalf-substrate-led answers proposed; Matt ratifies.
- **Decision 4 — Borderline candidate dispositions** for the high-judgment-value subset: lux + celestial (Latin-tier non-religious-coded holy); Greek Anemoi vocabulary on wind (mythological-depth); Solo Leveling shadow vocabulary (isekai-genre-defining D10 positioning); Empyrion / Solael (Grim Dawn Order constellation surface for non-religious-coded holy).
- **Decision 5 — Cull-tag disposition** for existing pool entries flagged with drift-14 tags (wind-storm-cluster-collapse; biological-organic; alternative-liquid; auditory-non-visual; conceptual-not-substance): does substrate-evidence dissolve the drift-14 cull verdicts, or does designer preference retain them?

### 0.3 Routing instruction for KR

Phase 5a synthesis draft is COMPLETE at this artifact. **Halt at Phase 5b for Matt Pattern B engagement.** Matt's next touchpoint is PG-3 architectural-commitment lock. After PG-3 Matt-ratification, Phase 5c canonical write fires at `canonical/story/2026-06-XX-flavor-pool-per-primary-element-lock.md`.

---

## 1. Substrate-led discipline composition (this synthesis honors what the substrate voted)

### 1.1 What the substrate said and how this synthesis is anchored on it

The substrate is the union of (a) the 217-row research dataset across 3 tracks × 8 primaries (Phase 1 + Phase 3); (b) Phase 4 statistical validation per PG-0 § 5 methodology lock; (c) the existing 156-entry `data/seasonal_elements/pool.json` representing prior designer-curation against the same canonical-7+1 primaries.

Substrate evidence is load-bearing here in three modes:

1. **High-confidence candidates** (Phase 4 § 9.3): 31 candidates with citation-weighted score ≥ T6 AND tracks_present ≥ 2 — bootstrap-stability-confirmed. **These ANCHOR per-primary allow-list cores.** Per-candidate routing follows substrate vote.
2. **Cardinality calibration**: T_principal=6 substrate-led against pool.json allow-list. Empirical T6 floors per primary (§ 4 column) are research-derived bounds; pool-depth where available (fire/water/earth/wind) is substrate-honest natural-depth anchor.
3. **Existing-pool entries**: 156 entries authored 2026-05-08 (with subsequent matt-demote / matt-promote / cull-tag manual overrides) are themselves substrate — prior designer-encoded vote that the substrate-led discipline preserves where research corroborates.

### 1.2 Where designer-curation overlays substrate vote (encoding gate per Discipline #41 refinement)

Substrate-led does NOT mean substrate-suppressing-designer. The encoding gate at Phase 5a is where designer judgment composes WITH substrate vote, never against it. This synthesis applies designer judgment at four kinds of surfaces:

1. **Per-candidate slot routing** at contamination cells (water↔wind=7 set; fire↔shadow=3 set; earth↔shadow=3 set) — substrate confirms candidate exists; designer picks primary slot.
2. **Cardinality TARGET selection** between T6 floor and pool-depth — substrate-honest natural-depth read.
3. **Reincarnated-fit weighting** for borderline candidates: isekai-positioning D10 → Solo Leveling shadow vocab; non-religious-coded holy preference; pre-empt religious-coded saturation.
4. **Vocabulary_commonness amendment** for d1_status: substrate-distinct candidates with low vocabulary-commonness (pall / miasma / rime precedent) become eligible rather than allow-list; designer applies the commonness filter as a downstream gate.

### 1.3 What this synthesis explicitly does NOT do

- Pre-commit Matt's PG-3 7-vs-8 architectural decision. § 2 surfaces BOTH options with full evidence. Gandalf soft lean is articulated; Matt's call.
- Lock final allow-list. The per-primary tables in § 4 are gandalf-proposals for Matt's Phase 5b ratification.
- Modify pool.json. Migration to pool.json is sub-phase 5f, post-wave, KR + elrond + star-lord territory.
- Amend canonical-7+1 element catalog (elements.yaml). The 8 primaries are substrate as-given.

---

## 2. 7-vs-8 architectural surface for Phase 5b (Matt PG-3 decision input)

This section is the single most load-bearing surface in this synthesis. Both architectures must be presented to Matt with substrate evidence + genre-canonical convergence + Reincarnated-fit reasoning. Gandalf's soft lean (Architecture A) is articulated WITHOUT bypassing Matt's authority.

### 2.1 The empirical signal in plain terms

Physical surfaces in all three tracks with row count (15), unique candidate count (13), and total citation-weighted score (76) all meeting or exceeding the rotating-primary MINIMUM (earth=14/10/62) per Phase 4 § 7.1 STRONG-8 quantitative axes.

But the substrate vocabulary is **fundamentally different in kind** from rotating primaries:

| Axis | Rotating primaries (range) | Physical |
|---|---|---|
| Modal substrate-type concentration | 0.32 – 0.70 (holy 0.32 → earth 0.70) | **0.85 mechanical_keyword** |
| Distinct substrate types | 4 – 5 | **3 (mechanical_keyword=11 + ailment=1 + phenomenon=1)** |
| HDBSCAN cluster count | 2 – 7 substantive clusters | **1 dominant cluster (n=11) + 1 side cluster (n=2)** |
| Off-diagonal contamination cells | average 2.6 | **1 cell only (`force` via wind, D&D-kinetic)** |
| Top-10 vocabulary | 3+ substrate types mixed | **9-of-10 mechanical_keyword (pierce / piercing / slash / slashing / bludgeoning / sever / strike / force / crush) + 1 ailment (bleed)** |

This IS the D&D 5e damage-type taxonomy (PHB chapter 9: bludgeoning / piercing / slashing + force) plus PoE physical-damage subtypes + ARPG-canonical kinetic vocabulary. Rotating primaries flex, contaminate, distribute across substrate-types, fragment into multiple keyword clusters. Physical does the opposite: monolithic, taxonomic, semantically isolated, structurally non-flexing.

### 2.2 Genre-canonical convergence (gandalf cross-house knowledge)

| Source | Physical treatment |
|---|---|
| Diablo 1 | Implicit (melee/ranged baseline; no "physical damage type" affix system) |
| Diablo 2 | Damage-type alongside elemental; mechanical affix vocab (open wounds, crushing blow, deadly strike) — NOT flavor-pool-shaped |
| Diablo 3 | Damage type; legendary affixes mechanical (pierce/strike/cleave) — feels different from "ash"/"frost" affixes |
| Diablo 4 | Physical/non-physical split for skill modifiers; physical sub-types not surfaced as flavor |
| Diablo Immortal | Same pattern as D4 |
| PoE 1 + 2 | Physical-damage base type; physical sub-types (pierce/bleed/impale/maim) are AILMENTS not flavor sub-elements. **Strongest genre-canonical precedent: physical doesn't get a flavor pool because its sub-vocabulary lives in ailment/mechanical space.** Ignite/Shock/Chill are elemental ailments; bleed/impale/maim are physical ailments — categorically different. |
| Grim Dawn | Physical + bleed + pierce as sibling damage types — "physical flavor" IS the damage-type-sibling architecture, NOT a sub-element pool |
| Last Epoch / Lost Ark / Wolcen / Chronicon / Titan Quest | Consistent: physical sub-types are damage-classification, not flavor |
| FF series | Physical attacks have no flavor sub-element; spells get the flavor; attacks get the weapon |
| SMT / Persona | Phys / fire / ice / elec / wind / light / dark + healing. Phys IS its own thing — Megaton Press / God's Hand / Heat Wave / Hassou Tobi are MECHANICAL named skills, not flavor sub-elements |
| Mushoku Tensei | "Sword magic" + physical combat have weapon-style schools (water-god / sword-god / north-god) — TECHNIQUE schools, not flavor sub-elements |

**Convergence:** physical does not flavor-pool in genre canon. It taxonomizes (D&D), schools (Mushoku Tensei), weapon-anchors (FF), or sibling-damage-types (Grim Dawn / PoE).

### 2.3 Two architectures supported by substrate

#### Architecture A — 7-primary rotating + physical-as-taxonomy-sibling

- 7 rotating primaries (fire / water / earth / wind / lightning / holy / shadow) each carry a substrate-honest flavor pool of 10-22 entries.
- Physical exists as the 8th DAMAGE TYPE in the engine taxonomy (for damage resists, mitigation routing, ailment dispatch per `config/elements.yaml`) but does NOT carry a "flavor pool" in the same sense.
- Physical kit identity differentiates through (a) WEAPON-FORM substrate (sword / spear / bow / axe — Reincarnated already has this surface per canonical 17-gear); (b) PHYSICAL-AILMENT vocabulary (bleed / impale / sever / rend) treated parallel to elemental ailments (ignite / shock / chill).
- The empirical 9-candidate mechanical_keyword cluster (pierce / piercing / slash / slashing / bludgeoning / sever / strike / force / crush) becomes the physical-as-taxonomy-sibling registry — not absent, just shaped categorically differently.

**Substrate evidence for A:**
- 0.85 modal mechanical_keyword concentration is unambiguous; the substrate has voted that physical is taxonomic
- Genre-canonical convergence is uniformly Architecture A across ARPG (D1-D4, PoE, GD, LE) and JRPG (FF, SMT, MT)
- Phase 4 stats verdict § 7.5: "WEAK-8: physical can be the 8th primary, but its sub-element pool would be a damage-type pool (mechanical, taxonomic, near-semantic-non-overlap) rather than a flavor pool"
- Reincarnated's `config/elements.yaml` ALREADY shapes physical as `rotating: false` + `resistance_type: armor` + `dodgeable: true` (vs rotating primaries' `percentage` + `dodgeable: false`) — the engine taxonomy is ALREADY asymmetric. Architecture A makes the flavor-pool asymmetry MATCH the engine-taxonomy asymmetry.

**Reincarnated-fit for A:**
- Spirit-swap-as-class-differentiation places kit identity at the (primary × form × sub-element) intersection. Physical kits differentiate via weapon-form + physical-ailment vocabulary; elemental kits differentiate via flavor sub-element vocabulary. Clean.
- WS1A.3 (per-kit sub-element selection) consumes a flavor pool per primary; against Architecture A, WS1A.3 sub-element selection fires for 7 primaries; physical's "sub-element" slot is filled by weapon-form selection.
- WS1A.4 (per-skill bounded LLM flavor judgment) judges flavor vocabulary against the locked pool; against Architecture A, the LLM judges against 7 substrate-honest pools + 1 damage-taxonomy registry (cleaner separation of judgment task).

#### Architecture B — 8-primary symmetric (physical-as-asymmetric-flavor-pool)

- All 8 canonical primaries carry a flavor pool per the same structural definition.
- Physical's flavor pool is the 9-candidate mechanical_keyword damage-taxonomy (pierce / piercing / slash / slashing / bludgeoning / sever / strike / force / crush — possibly extended with bleed / impale / rend / crush).
- Designer-acknowledged asymmetry: physical's flavor pool IS qualitatively mechanical-not-phenomenological; the 8-primary scheme accepts this as intentional design.

**Substrate evidence for B:**
- Quantitative axes all pass STRONG-8 thresholds (rows / unique-candidates / score / tracks-covered)
- Phase 3 deliberately excluded physical expansion; possible substrate-distinct vocabulary exists that wasn't sampled (`kinetic` / `impact-debris` / `crater` / `weight` / `concussion` / `friction`); architectural commitment could be paired with PG-3.5 in-flight physical expansion if Matt wants more data
- 30-year-locked Persona / SMT precedent has phys-as-symmetric-primary alongside elemental schools (with all the asymmetry the same way physical empirically is here)
- Asymmetric primary pools exist in published genre design (D&D 5e Necrotic / Radiant are flavor-pools while Force / Thunder are taxonomic; mixed-shape primaries is canonical)

**Reincarnated-fit for B:**
- Preserves symmetric 8-primary mental model in `config/elements.yaml`; aligns with the 8-element scheme already locked
- Player-facing cleanliness: when a player asks "what's the flavor pool for physical?" the answer is concrete (pierce / slash / bludgeon / sever / force / etc.) rather than "physical doesn't have a flavor pool in the same sense" (Architecture A explanation)
- Asymmetry tolerance: Reincarnated's isekai-provisional positioning means players come from FF / SMT / Persona expecting phys-as-symmetric-primary

### 2.4 Migration cost differential

| Migration surface | Architecture A | Architecture B |
|---|---|---|
| `config/elements.yaml` | NO change (already shaped for A: physical is `rotating: false`) | Possibly amend to add flavor_pool field for physical |
| `data/seasonal_elements/pool.json` | Extends to add lightning / holy / shadow allow-lists; physical NOT in pool (taxonomy lives separately) | Extends to add lightning / holy / shadow + physical allow-lists |
| WS1A.3 (per-kit sub-element selection) | Routes 7-primary path + weapon-form path for physical kits | Routes 8-primary path with physical pool semantically distinct |
| WS1A.4 (per-skill LLM flavor judgment) | LLM judges against 7 substrate-honest pools; physical kits judged against weapon-form + ailment vocabulary parallel system | LLM judges against 8 pools including the mechanical-taxonomy physical pool |
| Substrate library | Cleaner: each primary that flavor-pools is substrate-aligned | Asymmetric: 7 substrate-aligned + 1 explicitly-mechanical |

### 2.5 Gandalf's soft lean for Architecture A

I recommend Architecture A. Reasoning:

1. **The substrate has voted unambiguously.** 0.85 modal mechanical_keyword concentration + single dominant cluster + near-zero contamination is the substrate saying "this primary is taxonomic, not phenomenological." Forcing a flavor-pool semantic onto taxonomic substrate is the failure mode of "make all primaries look the same on paper at cost of substrate honesty." Discipline #41 substrate-led discipline applies: encoding gate composes WITH substrate vote, not against it.

2. **Genre-canonical convergence is uniform.** Every ARPG + JRPG cited above treats physical as taxonomy-sibling, weapon-anchor, or ailment-class. None treats physical as flavor-pool-symmetric. This is not an accident; the genre learned this from D&D 5e + 30 years of design refinement. Reincarnated's positioning (isekai-provisional ARPG) means players already have the Architecture A mental model.

3. **`config/elements.yaml` is already shaped for Architecture A.** Physical's `rotating: false` + `resistance_type: armor` + `dodgeable: true` configuration is asymmetric against rotating primaries' `percentage` + `dodgeable: false`. The engine taxonomy is ALREADY shaped for A. Architecture B requires either (a) accepting a mismatch between engine-taxonomy-shape and flavor-pool-shape, or (b) amending elements.yaml to make physical look more like a rotating primary at engine level — which fights canonical 28 engine-arpg-rebalance design.

4. **WS1A.3 / WS1A.4 downstream consumers are cleaner against A.** Per-skill LLM flavor judgment against 7 substrate-honest pools is a cleaner LLM-prompt design surface than judgment against 8 asymmetric pools where one pool is "actually taxonomic, treat differently."

5. **Reincarnated thematic resonance.** Physical = mortal / mundane / pre-spirit-swap baseline that the journey transcends. Treating physical as the taxonomic ground that elemental primaries flex against thematically aligns with the spirit-swap-as-ascendance arc.

**HOWEVER:** this is a soft lean, not pre-commitment. Matt should weigh:
- Persona 30-year-locked precedent (B-side advantage if isekai-positioning carries that weight)
- Player-facing simplicity of B (one structural rule per primary)
- Whether designer-acknowledged asymmetry is acceptable in the lock

**Matt's PG-3 call.** Whichever architecture Matt locks, Phase 5c canonical write reflects it.

---

## 3. Cardinality TARGETS per primary (substrate-led; not floors)

Per gandalf PG-2 forward note 3: cardinality is TARGET not floor; lands between T6 empirical floor and pool-depth where substrate evidence is consistent with the depth.

### 3.1 Per-primary cardinality TARGET table

| Primary | T6 floor (research) | Pool-depth (existing) | Gandalf TARGET | Rationale |
|---|---:|---:|---:|---|
| fire | 8 | 20 (allow-list) | **14** | Cross-track core (ember + cinder); pool-depth preserves substrate-honest material vocab (coal / lava / magma / charcoal etc.); add 4 research-confirmed candidates (blaze / scorch / inferno extensions); demote 6-8 over-curated mundane entries |
| water | 10 | 11 (allow-list) | **14** | High-confidence core (tide / torrent / glacial / brine) + selective extensions (frost / mist / chill — but mist routing decision per § 6); demote sweat / honey / tear / sap mundane entries; add aqua + ice-class additions |
| earth | 3 | 22 (allow-list) | **22** (preserve) | T6=3 is RESEARCH-thin not substrate-thin; earth pool was deeply curated 2026-05-08; substrate confirms stone + quake + tremor cross-track; preserve material-rich pool depth (granite / slate / basalt / marble / clay / ore / iron / etc.); KEEP biological-organic cull-tag verdict (bone / shell / chitin / claw / horn remain quarantine) unless Matt overrides |
| wind | 21 | 7 (allow-list) | **12** | Substrate evidence supports SUBSTANTIAL reshape upward from 7 — but NOT to T6=21. Curation TARGET 12 balances: storm-flex core (gale / gust / cyclone / tempest / hurricane / squall) + wind-PURE core (sleet / hail / frost-as-cold / cloud / mist-routing-to-wind-OR-water) + Greek Anemoi mythological-depth (zephyr + 1-2 Anemoi). Designer-judgment heavy section |
| lightning | 11 | 0 (no pool) | **10** | T6 core IS the natural-depth (arc / static / surge / volt / bolt / lightning / shock / spark / thunder + 1 JRPG proper-noun representative — thundara OR zio); substrate yield matches target |
| holy | 19 | 0 (no pool) | **10** | T6=19 reflects religious-coded saturation; designer-curation prioritizes non-religious-coded core per PG-1 surface 2. Lean: radiance / radiant / dawn / aurora / divine / sacred (religious-coded retained as canonical) + lux + celestial (Latin-tier non-religious) + 2 Empyrion-class Grim Dawn Order proper-nouns. Holy is the lowest-cardinality primary intentionally — resist saturation |
| shadow | 17 | 0 (no pool) | **12** | Layer-pick: 3 cross-track core (void / shade / umbra) + 2-3 SMT proper-noun representatives (mudo / mamudo / mahamaon) + 2-3 Solo Leveling representatives (shadow exchange / shadow linker / shadow preserve / monarch / igris) + 2-3 FF-mechanical / D&D (drain / wraith / lich / necrotic / abyss / blight) |
| physical | 9 | 0 (no pool) | **9** (Architecture-A-frame) OR **9-12** (Architecture-B-frame) | If Architecture A: physical is taxonomy-sibling registry not flavor-pool; 9 entries become taxonomy registry (pierce / piercing / slash / slashing / bludgeoning / sever / strike / force / crush / bleed / impale / rend). If Architecture B: 9 entries form the asymmetric flavor pool. Cardinality same; semantic frame differs |

### 3.2 Total pool size projection

Architecture A: 14 + 14 + 22 + 12 + 10 + 10 + 12 = **94 flavor-pool entries** across 7 rotating primaries + 9 entries in physical-taxonomy-sibling registry (separate semantic layer).

Architecture B: same 94 + 9 = **103 pool entries** across 8 primaries with physical's pool flagged as `pool_type: damage_taxonomy`.

Existing pool: 156 total entries (60 allow-list across 4 primaries). The synthesis-driven pool is SMALLER allow-list (94 vs 60 — net +34 allow-list mostly from new primaries lightning/holy/shadow); existing eligible/quarantine entries largely preserved as-is per § 6 audit.

### 3.3 Why TARGET not floor

T6 floors are research-derived empirical bounds — what's substrate-supportable at the citation-weighted-score-≥-6 threshold. They are NOT the design target. The design target is per-primary "natural cardinality" — the depth where vocabulary substrate stops adding meaningful flavor differentiation. Above natural-depth, vocabulary gets saturated (every fire skill needs a unique flavor word but only N words are recognizably-fire-distinct); below natural-depth, the pool feels thin (LLM judgment will pick the same word repeatedly).

Substrate-honest natural-depth differs from T6 floor when:
- Pool is over-curated (fire: pool=20 vs T6=8 → designer-preference cull to ~14 substrate-honest)
- Pool is under-curated (wind: pool=7 vs T6=21 → designer-curated raise to ~12 substrate-honest, NOT to T6)
- Pool doesn't exist (lightning/holy/shadow: no pool anchor → land at substrate-honest natural-depth, treating T6 as lower bound to consider)

---

## 4. Per-primary curated allow-list recommendations

For each primary, this section presents the gandalf-proposed allow-list grounded in Phase 4 high-confidence candidates + existing pool + designer-curation overlay. Tables show citation-weighted score (CWS), tracks present (TP), and gandalf disposition.

### 4.1 Fire — TARGET ~14

**High-confidence core (Phase 4 § 9.3):** ember (CWS=12, 2 tracks); cinder (CWS=8, 2 tracks).

**Substrate-research additions (single-track but R=3 + Phase-4-cited):**
- blaze (CWS=6, ARPG, R=3): genre-canonical Diablo blaze affix; ADD to allow-list
- scorch (CWS=6, ARPG, R=3): genre-canonical PoE scorch ailment; ADD to allow-list
- inferno (CWS=6, JRPG, R=3): FF/SMT canonical; ADD to allow-list
- ignite (CWS=6, ARPG, R=3, substrate=ailment): PoE Ignite IS the canonical fire ailment; ADD to allow-list with ailment-substrate flag
- agi (CWS=6, JRPG, R=3): SMT proper-noun core; ADD to allow-list as JRPG-isekai-genre-canonical representative
- fira (CWS=6, JRPG, R=3): FF proper-noun core; ADD to allow-list as JRPG-isekai-genre-canonical representative

**Existing pool preserved (allow-list maintained per substrate evidence):** ember, cinder, ash, soot, spark, pitch, tar, charcoal, lava, magma, lantern, torch, blaze, char, scorch, brand, flare, flint, tinder, coal (20 entries currently). Coal + char + brand + flare + flint + tinder are NOT in research candidates but are substrate-honestly fire (tabletop / archaeological canon); PRESERVE per pool-depth-anchor discipline (§ 6 audit).

**Gandalf TARGET allow-list (14):** ember, cinder, blaze, scorch, inferno, ignite, agi, fira, lava, magma, charcoal, char, brand, flare. (Demotes: ash → eligible per ambiguity, soot → eligible, spark → eligible-via-lightning-flex per § 6, pitch → eligible, tar → eligible, lantern → eligible, torch → eligible, flint → eligible, tinder → eligible, coal → eligible. These 10 stay in pool as eligible / not retired; they may flavor-judge per LLM with lower frequency.)

**Borderline DEFER:** hellfire (CWS=4, JRPG R=2; fire-shadow contamination per § 5.2); conflagration (CWS=4, tabletop R=2 — could promote to allow-list if cardinality TARGET raises); crimson (CWS=4, JRPG R=2, material-substrate flagged as fire-color not fire-substance); sulphur (CWS=4, tabletop R=2 — alchemical depth); pyre (CWS=4, ARPG R=2 — burning-pile material).

**Decisions surfaced to Matt:** include hellfire? (resolves fire-shadow contamination toward fire OR keeps it as flex). Include conflagration? (raises cardinality slightly). Disposition of pool's "domestic-warm" cluster (lantern/torch/hearth/candle): do we preserve as canonical-low-power-fire or treat as eligible-low-utility?

### 4.2 Water — TARGET ~14

**High-confidence core:** glacial (CWS=8, 2 tracks); tide (CWS=8, 2 tracks); torrent (CWS=8, 2 tracks); brine (CWS=6, 2 tracks).

**Substrate-research additions:**
- aqua (CWS=6, JRPG, R=3): FF/MT proper-noun canonical; ADD to allow-list as JRPG-genre representative
- frost (CWS=6, ARPG, R=3): genre-canonical (Diablo frost / PoE Freeze); ADD to allow-list — note water-wind flex per substrate (frost is structurally water-cold in JRPG canon; wind-cold in atmospheric-phenomenon framing)
- chill (CWS=6, ARPG, R=3, substrate=ailment): PoE Chill IS the canonical water ailment; ADD to allow-list with ailment-substrate flag — note `config/elements.yaml` water-ailment is `chill`; this aligns
- blizzara (CWS=6, JRPG, R=3): FF proper-noun core; ADD to allow-list as JRPG-isekai-genre-canonical representative
- bufu (CWS=6, JRPG, R=3): SMT proper-noun core; ADD to allow-list as JRPG-isekai-genre-canonical representative
- mist (CWS=6, tabletop, R=3): substrate confirms — but routing decision per § 5.2 (water vs wind) — gandalf routes mist → WATER on substrate-honest grounds (mist is atmospheric-water in tabletop_myth + MTG; the wind-mist association is metaphorical not substrate-primary)

**Existing pool preserved (substrate evidence supports):** tide, brine, salt (water flex), rain, ice, glacier, snow, marsh, wake, wave, slick (11 allow-list entries). Glacier is the canonical for `glacial` research candidate — synthesis preserves glacier-as-noun + adds glacial-as-modifier per substrate evidence.

**Gandalf TARGET allow-list (14):** tide, torrent, glacial, brine, aqua, frost, chill, blizzara, bufu, mist (water-routed), ice, glacier, wave, marsh. (Demotes: salt → eligible per water/earth flex ambiguity; rain → eligible per low ARPG-citation; snow → eligible — substrate-honest cold variants converge on frost/ice/glacial; wake → eligible per low recognizability without sea-faring context; slick → eligible.)

**Borderline DEFER:** deluge (CWS=4, JRPG R=2 — could promote); mercury (CWS=4, tabletop alchemical — flagged drift-14-alternative-liquid; designer-judgment); rime (CWS=1, ARPG R=1 — substrate weak but pool-existing as eligible per vocab-obscure-2026-05-12 tag).

**Decisions surfaced to Matt:** mist routing finalization (water vs wind) — gandalf recommends water; vortex routing finalization (water vs wind) — gandalf recommends WIND per § 5.2; mercury disposition (alchemical depth retain OR drift-14 cull preserve).

### 4.3 Earth — TARGET ~22 (preserve pool depth)

**High-confidence core:** stone (CWS=18, ALL 3 tracks — strongest cross-track agreement in entire dataset); quake (CWS=12, 2 tracks); tremor (CWS=8, 2 tracks).

**Substrate-research additions (single-track but Phase-4-cited):**
- dust (CWS=4, ARPG, R=2): genre-canonical; ALREADY in pool as wind-primary with earth flex (per pool.json); KEEP as-is
- loam (CWS=4, tabletop, R=2, MTG canonical): MTG mana-cost land vocabulary; ADD to allow-list as substrate-distinct earth depth
- salt (CWS=4, tabletop, R=2, alchemical): substrate-confirmed; ALREADY in pool as water-primary with earth flex; KEEP — though designer-judgment surface: shift salt to earth-primary OR retain water-primary
- terra (CWS=4, JRPG, R=2, proper-noun): FF Terra proper-noun; ADD to allow-list as JRPG-isekai-genre representative
- thorn (CWS=4, ARPG, R=2): ALREADY in pool as eligible with drift-14-plant-anatomical cull-tag; substrate-confirms thorn as earth canonical (PoE Thorn affix); RECOMMEND drift-14 cull dissolution per substrate; KEEP allow-list

**Existing pool preserved (substrate-honest material depth):** stone, granite, slate, basalt, limestone, marble, clay, sand, ore, iron, copper, bronze, gold, silver, lead, rust, gem, crystal, geode, quartz, obsidian, amber (22 allow-list entries currently). All substrate-aligned to earth-as-material canonical (D&D / MTG / mythological); PRESERVE en bloc.

**Gandalf TARGET allow-list (22):** stone, granite, slate, basalt, marble, limestone, clay, sand, ore, iron, copper, gold, silver, lead, gem, crystal, obsidian, amber, quake, tremor, terra, loam. (Preserve depth; add quake / tremor from research; add terra + loam from research; one demotion: rust → eligible per substrate distance from earth-canonical-material — rust is decay-state not earth-substance.)

**Drift-14 cull-tag DISPOSITION surfaced to Matt:** the biological-organic cluster (bone, marrow, husk, shell, chitin, scale, horn, tooth, claw, root, petal) — substrate-evidence is silent (these weren't in research candidates). Drift-14 cull verdicts retain unless Matt overrides. Earth's biological-organic culling per drift-14 represents prior designer judgment (per project memory cull-tags lineage) that this synthesis does NOT override without Matt input.

**Borderline DEFER:** bedrock (CWS=2, single-track ARPG); mineral (CWS=2, single-track JRPG) — both substrate-thin; gandalf disposition DROP per low-recognizability.

### 4.4 Wind — TARGET ~12 (substantial reshape from existing 7)

This is the most designer-judgment-heavy primary. PG-1 surface 1 + PG-2 § 1.3 + § 1.4 carry the storm-flex / wind-PURE asymmetry forward.

**High-confidence core (Phase 4 § 9.3):** tempest (CWS=18, 2 tracks); cyclone (CWS=16, 2 tracks); whirlwind (CWS=15, 2 tracks); gale (CWS=14, 2 tracks); gust (CWS=14, 2 tracks); squall (CWS=10, 2 tracks); zephyr (CWS=10, 2 tracks).

**Storm-flex cluster (Phase 1 ARPG + Phase 3 expansion + tabletop_myth):** tempest, cyclone, whirlwind, gale, gust, squall, hurricane, tornado, vortex, stormtide. Per § 5.2, water↔wind=7 contamination routes: hurricane → WIND; squall → WIND; stormtide → WIND; tempest → WIND (currently in pool as wind-primary with water-flex; preserve); vortex → designer-judgment (gandalf recommends WIND per PoE Vortex precedent — wind-rotational; mist → WATER per § 4.2; njord → WATER per Norse sea-god primary identity; notus → WIND per Greek Anemoi (south wind)).

**Wind-PURE substrate (atmospheric phenomenon, non-storm-flex):** gust, gale, breeze, zephyr (Greek-mythological wind-pure), aero (FF proper-noun), garu (SMT proper-noun), aeolus / boreas / zephyrus / eurus / notus (Greek Anemoi).

**Greek Anemoi mythological depth (PG-2 § 5 forward note + PG-1 § 1.5):** the Anemoi are substrate-distinct mythological depth that tabletop_myth weight elevation was forward-noted to capture. Phase 4 surfaces aeolus (CWS=6), boreas (CWS=6), zephyrus (CWS=6), eurus (CWS=2), notus (CWS=2). Gandalf recommends including 2-3 Anemoi for mythological-depth: **zephyr (already high-confidence) + boreas (north-wind canonical) + 1 designer-pick (aeolus OR zephyrus)**.

**Existing pool preserved/demoted:**

| Pool entry | Current status | Substrate verdict | Gandalf disposition |
|---|---|---|---|
| breath | quarantine | not in research | KEEP quarantine |
| mist | eligible (wind+water flex) | substrate routes to water per § 5.2 | DEMOTE from wind / surfaces in water allow-list |
| fog | eligible | not in research | KEEP eligible |
| vapor | eligible | not in research | KEEP eligible |
| gust | eligible (drift-14-wind-storm-cluster-collapse) | high-confidence (CWS=14, 2 tracks) | PROMOTE to allow-list; DISSOLVE drift-14 cull-tag per substrate vote |
| gale | allow-list | high-confidence (CWS=14, 2 tracks) | PRESERVE allow-list |
| draft / sigh / whisper / whistle / howl / hum / thrum | quarantine | not in research; auditory-non-visual cluster | KEEP quarantine (drift-14 honored — these are sound-not-substance) |
| plume | allow-list | not in research; smoke-column adjacency | KEEP allow-list per pool-depth-anchor |
| dust | allow-list | substrate confirms (earth flex) | KEEP allow-list |
| pollen / spore / seed / feather | quarantine/eligible | not in research; biological/organic | KEEP per drift-14 |
| gossamer / silk | quarantine | not in research | KEEP quarantine |
| hail / sleet / frost / rime | varied | substrate evidence mixed (frost in water; rime obscure-vocab) | RESHAPE: hail → wind allow-list (cold-storm); sleet → wind allow-list (cold-storm); frost → routes to WATER per § 4.2; rime → eligible per vocab-obscure |
| gauze / veil / cloud / billow / exhalation | varied | cloud has matt-promote-2026-05-12; not in research | KEEP cloud allow-list; KEEP rest quarantine/eligible |
| typhoon / cyclone / tempest / miasma / squall / shear / pall / hurricane | eligible (drift-14-wind-storm-cluster-collapse for several) | high-confidence research for cyclone/tempest/squall/hurricane | PROMOTE cyclone, tempest, squall, hurricane to allow-list; DISSOLVE drift-14 cull-tag per substrate vote; KEEP typhoon eligible (substrate-honest oceanic variant); KEEP miasma eligible (vocab-obscure); KEEP shear / pall eligible per matt-demote-2026-05-12 lineage |

**Gandalf TARGET allow-list (12):** tempest, cyclone, whirlwind, gale, gust, squall, hurricane, zephyr, boreas, hail, sleet, cloud. (Storm-flex 6: tempest / cyclone / whirlwind / gust / squall / hurricane. Wind-PURE 2: gale / gust [overlap accepted; gust does both]. Anemoi 2: zephyr / boreas. Atmospheric-cold 2: hail / sleet. Diffuse 1: cloud. Counter to 7-existing: 9 new allow-list / 5 PROMOTED from eligible-via-substrate / 3 retained from existing (gale; cloud; per matt-promote lineage).)

**Decisions surfaced to Matt:** Anemoi selection (gandalf picks zephyr + boreas; Matt may swap to aeolus or zephyrus for mythological flavor); drift-14-wind-storm-cluster-collapse dissolution disposition (gandalf recommends DISSOLVE per substrate vote; Matt may RETAIN if storm-flex over-curation concern persists); vortex routing (gandalf WIND; Matt may route WATER per PoE Vortex cold-damage precedent).

### 4.5 Lightning — TARGET ~10

No existing pool anchor. Substrate yield strong; T6 floor (11) IS natural-depth.

**High-confidence core:** arc (CWS=12, 2 tracks); static (CWS=8, 2 tracks); surge (CWS=8, 2 tracks); volt (CWS=8, 2 tracks).

**Substrate-research additions:**
- bolt (CWS=6, JRPG, R=3): genre-canonical FF Thunder/Bolt; ADD
- lightning (CWS=6, tabletop, R=3): self-name canonical; ADD as substrate base
- shock (CWS=6, ARPG, R=3, substrate=ailment): canonical PoE Shock IS the lightning ailment; ADD with ailment-substrate flag — matches `config/elements.yaml` lightning ailment = `shock`
- spark (CWS=6, ARPG, R=3): genre-canonical Diablo / PoE; ADD
- thunder (CWS=6, tabletop, R=3): D&D Thunder damage type; ADD
- thundara (CWS=6, JRPG, R=3): FF proper-noun JRPG canonical; ADD as JRPG-isekai representative — OR zio (CWS=6, SMT proper-noun); designer-judgment surface, gandalf picks thundara per broader recognizability

**Gandalf TARGET allow-list (10):** arc, static, surge, volt, bolt, lightning, shock, spark, thunder, thundara. (Add 1 more if Matt wants 11: zio for SMT representation OR plasma for ARPG-electric variant.)

**Decisions surfaced to Matt:** thundara vs zio (gandalf picks thundara); add plasma? (CWS=4, JRPG R=2; substrate-thin but isekai-canonical); add chain / forked / mjolnir-class proper-nouns?

### 4.6 Holy — TARGET ~10

No existing pool anchor. PG-1 surface 2 + PG-2 § 4.2 carry the non-religious-coded curation priority. T6=19 reflects religious-coded saturation; gandalf cardinality target intentionally low at 10 to resist saturation.

**High-confidence core:** divine (CWS=18, 2 tracks); sacred (CWS=18, 2 tracks); radiance (CWS=17, 2 tracks); radiant (CWS=12, 2 tracks); dawn (CWS=8, 2 tracks).

**Non-religious-coded subset (PG-1 weighting):** radiance, radiant, dawn, aura (CWS=8, JRPG), aurora (not in research; pool gap), celestial (CWS=4, JRPG, R=2, single-track-borderline), lux (CWS=4, JRPG, R=2, single-track-borderline), corona (CWS=4, ARPG R=2), solar (CWS=4, ARPG R=2).

**Religious-coded (retained for canonical recognizability, cardinality bounded):** divine, sacred, blessed (CWS=12, ARPG R=3), consecrated (CWS=6, ARPG R=3).

**JRPG proper-noun representation (1 representative):** hama (CWS=6, SMT R=3) OR resurrection (CWS=9, JRPG R=3) OR cura (CWS=6, FF R=3); gandalf picks hama per SMT genre representativity.

**Grim Dawn Order proper-nouns (PG-1 surface 2 explicit target):** empyrion (CWS=4, ARPG R=2), solael (CWS=2, ARPG R=1). Surface for Matt designer-judgment per PG-1 ratification.

**Gandalf TARGET allow-list (10):** radiance, radiant, dawn, aura, divine, sacred, blessed, lux, celestial, hama. (Designer-curation choices: lux + celestial are Latin-tier non-religious-coded — surface for Matt ratification; if Matt prefers Grim Dawn flavor, substitute empyrion or solael for hama; if Matt prefers more JRPG canon, substitute resurrection or cura for hama.)

**Decisions surfaced to Matt:** lux + celestial INCLUDE / EXCLUDE (gandalf recommends INCLUDE — both non-religious Latin-tier; Phase 4 § 10.3 explicitly carries this to PG-3); SMT representation choice (hama / mahamaon / hamaon); religious-coded saturation tolerance (gandalf bounds at 4 of 10; Matt may raise to 6); proper-noun representation depth.

### 4.7 Shadow — TARGET ~12 (3-layer pick)

No existing pool anchor. PG-1 surface 3 + PG-2 § 1.3 carry the three-canonical-layer competition (SMT proper-noun / FF mechanical / Solo Leveling phenomenon). Layer-pick balances genre-canonical depth.

**High-confidence core (cross-track ANCHORS):** void (CWS=18, ALL 3 tracks); shade (CWS=12, ALL 3 tracks); umbra (CWS=8, ALL 3 tracks); wraith (CWS=8, 2 tracks).

**SMT proper-noun layer:** mudo (CWS=6, R=3), mamudo (CWS=6, R=3), mamudoon (CWS=6, R=3), mudoon (CWS=6, R=3). Gandalf picks 2: mudo + mamudoon (covers low-tier and high-tier SMT shadow magic).

**FF / mechanical layer:** drain (CWS=6, R=3), necro (CWS=6, R=3), necrotic (CWS=6, tabletop R=3 — D&D formal damage type), lich (CWS=6, R=3). Gandalf picks 2: drain + necrotic (drain for FF/SMT canonical mechanic; necrotic for D&D formal type cross-validation).

**Solo Leveling / isekai-genre layer (D10 positioning per PG-2 § 1.3):** shadow (CWS=6, R=3), abyss (CWS=9, R=3, single-track but high-recognizability), monarch (CWS=6, R=3), shadow exchange (CWS=2, R=2), shadow linker (CWS=2, R=2), shadow preserve (CWS=2, R=2), igris (CWS=2, R=2), beru (CWS=3, R=3). Gandalf picks 2: monarch + abyss (monarch for Solo Leveling canonical title; abyss for cross-isekai phenomenon).

**Gandalf TARGET allow-list (12):** void, shade, umbra, wraith, mudo, mamudoon, drain, necrotic, monarch, abyss, shadow, lich. (Cross-track 4 + SMT 2 + FF/mechanical 2 + Solo Leveling 2 + extras 2.)

**Decisions surfaced to Matt:** SMT depth (gandalf 2; Matt may push to 3-4 for full mudo / mamudo / mahamaon-equivalent ladder); Solo Leveling depth (gandalf 2; Matt may push to 3-4 for shadow-army-vocab richness — shadow exchange / shadow linker / shadow preserve / igris / beru); decay-cluster inclusion (blight / decay / miasma — fire-shadow / earth-shadow contamination per § 5.3).

### 4.8 Physical — TARGET 9 (Architecture-A-frame) OR 9-12 (Architecture-B-frame)

**Substrate-vote 9 candidates (Phase 4 § 5.3 floor):** pierce (CWS=12, 2 tracks), sever (CWS=8, 2 tracks), bleed (CWS=6, R=3, ailment), bludgeoning (CWS=6, tabletop R=3), force (CWS=6, tabletop R=3), piercing (CWS=6, tabletop R=3), slash (CWS=6, JRPG R=3), slashing (CWS=6, tabletop R=3), strike (CWS=6, JRPG R=3).

**Extension candidates (CWS=4):** crush (ARPG R=2), impact (JRPG R=2), rend (JRPG R=2). All substrate-thin.

**Sub-extension candidates (CWS=2):** impale (ARPG R=2).

**Frame-dependent disposition:**
- **Architecture A:** these 9 candidates form the physical-as-taxonomy-sibling REGISTRY (separate semantic layer from flavor-pool). Registry serves WS1A.4 LLM judgment for physical kits as "valid physical-damage-type vocabulary" rather than as "flavor pool entries." Cardinality bounded at 9.
- **Architecture B:** these 9 candidates + 3 extensions (crush / impact / rend) = 12 entries form the asymmetric physical flavor pool. Cardinality 9-12 per Matt design preference.

**Gandalf disposition (both frames):** 9 canonical entries (pierce / piercing / slash / slashing / bludgeoning / sever / strike / force / bleed) are substrate-locked. Architecture-A-vs-B determines semantic shape, not entry composition.

**Decisions surfaced to Matt:** Architecture A vs B (the meta-decision); extension to 12 with crush / impact / rend if Architecture B (asymmetric pool); pre-PG-3 in-flight physical expansion fire if Matt wants more substrate evidence before committing (would add ~14 days; defers PG-3).

---

## 5. Curation-decision sections for high-contamination pairs

### 5.1 water ↔ wind = 7 (largest off-diagonal — PG-2 § 1.2 forward-noted)

**Substrate-confirmed contamination candidates:** hurricane, mist, njord, notus, squall, stormtide, tempest.

**Per-candidate routing (gandalf seam authority for substrate-led slot routing):**

| Candidate | CWS | Tracks | Substrate-evidence | Gandalf routing | Reasoning |
|---|---:|---|---|---|---|
| hurricane | 9 | ARPG | phenomenon; D&D Hurricane spell + meteorological tropical-storm | **WIND primary, water flex** | Tropical-storm IS wind-rotational-phenomenon at source; the water-flex captures the oceanic-storm secondary association |
| mist | 6 | tabletop | phenomenon; D&D Fog Cloud + atmospheric water-vapor | **WATER primary, wind flex** | Mist is atmospheric water-vapor at substrate-honest root; the wind-flex captures the suspended-particulate aspect. POOL-EXISTING mist is currently wind-primary with water-flex — RESHAPE recommended to water-primary with wind-flex |
| njord | 4 | tabletop | mythological; Norse sea-god (Vanir, god of sea/wind/wealth) | **WATER primary, wind flex** | Njord's primary domain is sea + sea-faring + sea-storms; wind is secondary domain. Substrate-honest water |
| notus | 2 | tabletop | mythological; Greek Anemoi south-wind (associated with storms + autumn rain) | **WIND primary, water flex** | Anemoi are wind deities; Notus brings rain as secondary effect. Substrate-honest wind |
| squall | 10 | ARPG+JRPG | phenomenon; brief violent storm; PoE Squall affix | **WIND primary, water flex** | Squall is wind-storm-event; oceanic squall (water-flex) is secondary. Substrate-honest wind |
| stormtide | 4 | tabletop | phenomenon; MTG Stormtide Leviathan; ocean-storm | **WIND primary, water flex** | Storm-tide-as-named is wind-storm hitting tide; substrate-honest wind-primary. Could route water if Matt prefers stronger oceanic identity |
| tempest | 18 | ARPG+tabletop | phenomenon; canonical storm (D&D Tempest Domain; PoE Tempest league; Shakespeare); pool-existing wind-primary with water-flex | **WIND primary, water flex** | Substrate-overwhelmingly wind; pool-existing routing preserved |
| vortex | 8 | ARPG | phenomenon; PoE Vortex (cold-AOE skill); ARPG canonical | **WIND primary, water flex** | DESIGNER-JUDGMENT SURFACE: PoE Vortex IS cold-AOE-rotational (could route water for cold-association); but the rotational-substance is wind-canonical. Gandalf routes WIND per substrate-rotational-primary; Matt may override |

**Summary of routing:** WIND-primary: hurricane, notus, squall, stormtide, tempest, vortex (6 candidates). WATER-primary: mist, njord (2 candidates).

**Pool.json migration impact:** pool-existing mist is currently wind-primary; recommendation shifts to water-primary. Pool-existing tempest is currently wind-primary with water-flex; preserved. New entries (hurricane / squall / stormtide / cyclone) extend wind allow-list per § 4.4.

### 5.2 fire ↔ shadow = 3 (necromancer-fire / hellfire cluster)

**Substrate-confirmed contamination candidates:** dark flame master, hellfire, sulphur.

**Per-candidate routing:**

| Candidate | CWS | Tracks | Substrate-evidence | Gandalf routing | Reasoning |
|---|---:|---|---|---|---|
| dark flame master | 2 | JRPG | proper_noun (KonoSuba Megumin's title) | **SHADOW primary, fire flex** | Proper-noun-tier; isekai-genre-specific; dark-as-primary at named source |
| hellfire | 4 | JRPG | phenomenon; FF hellfire + D&D infernal fire | **FIRE primary, shadow flex** | Hellfire IS fire at primary substance; shadow-flex captures the demonic/infernal association |
| sulphur | 4 | tabletop | material; alchemical brimstone + Christian theology demonic-association | **FIRE primary, shadow flex** | Sulphur is fire-material at alchemical root; shadow-flex captures demonic association |

**Disposition:** preserve fire-shadow as a 3-candidate flex cluster; per-candidate primary routing per substrate-honesty. No major pool migration; integrates with § 4.1 fire allow-list (hellfire / sulphur as eligible) and § 4.7 shadow allow-list (dark flame master not surfaced as core Solo Leveling depth).

### 5.3 earth ↔ shadow = 3 (decay / blight cluster)

**Substrate-confirmed contamination candidates:** blight, decay, miasma.

**Per-candidate routing:**

| Candidate | CWS | Tracks | Substrate-evidence | Gandalf routing | Reasoning |
|---|---:|---|---|---|---|
| blight | 6 | ARPG | phenomenon; PoE Blight; D&D Blight spell | **SHADOW primary, earth flex** | PoE Blight league + D&D Blight target plant-decay-via-necromantic-corruption; substrate-honestly shadow-primary |
| decay | 4 | ARPG | phenomenon; Diablo Necromancer affixes | **SHADOW primary, earth flex** | Decay-as-mechanic is necromantic; earth-flex captures organic-decomposition aspect |
| miasma | 4 | JRPG | phenomenon; pool-existing wind-primary with vocab-obscure-2026-05-12 tag | **SHADOW primary, earth flex** | Substrate evidence routes miasma to shadow (toxic-atmospheric-decomposition); pool-existing wind-primary needs migration to shadow-primary per substrate vote; preserve vocab-obscure-2026-05-12 flag |

**Disposition:** preserve earth-shadow as a 3-candidate flex cluster; substrate routes all 3 to SHADOW-primary; per § 4.7 shadow allow-list, gandalf retains blight as eligible (not in TARGET 12 core) per low-cardinality discipline; decay and miasma as eligible per substrate-thin.

### 5.4 Other off-diagonal pairs (low contamination; lighter disposition)

| Pair | Cell count | Candidates | Disposition |
|---|---:|---|---|
| fire ↔ earth | 1 | smelt (tabletop, CWS=2, mechanical_keyword) | EARTH-primary with fire flex (alchemical smelting); not in core allow-list |
| fire ↔ holy | 1 | solael (ARPG, CWS=2, Grim Dawn Order constellation) | HOLY-primary; surface for Matt at § 4.6 |
| earth ↔ wind | 1 | dust (ARPG, CWS=4) | POOL-EXISTING wind-primary with earth-flex; PRESERVE |
| earth ↔ holy | 1 | salt (tabletop, CWS=4, alchemical) | POOL-EXISTING water-primary with earth-flex; preserve OR shift to earth-primary per substrate (designer-judgment) |
| water ↔ shadow | 1 | abyss (JRPG, CWS=9) | SHADOW-primary per Solo Leveling / FF; water-flex captures depth-imagery |
| water ↔ holy | 1 | aqua (JRPG, CWS=6) | WATER-primary per FF canonical; holy-flex captures Aqua-as-divine-name (KonoSuba goddess) |
| water ↔ lightning | 1 | mercury (tabletop, CWS=4, alchemical + planetary) | POOL-EXISTING water-primary with no flex; preserve OR add lightning-flex per mercury-as-quick-conductor |
| wind ↔ lightning | 1 | tempest (per § 5.1) | already routed wind-primary; lightning-flex captures storm-lightning |
| wind ↔ holy | 1 | aura (JRPG, CWS=8) | HOLY-primary per radiance-class; wind-flex captures atmospheric-presence aspect |
| wind ↔ physical | 1 | blast / force | PHYSICAL-primary (force as D&D damage type) and WIND-primary (blast as wind-effect); these are separate substrate-aligned routings |
| holy ↔ lightning | 1 | aether (tabletop, CWS=4, mythological) | HOLY-primary per aetheric-radiance; lightning-flex captures aether-as-fifth-element-energy aspect |

---

## 6. Existing-pool audit (156 entries; per-batch verdict)

Per Q-shape-4 ratification: each existing pool.json entry gets a PRESERVE / DEMOTE-from-allow-list / REMOVE / EXTEND-new verdict against research findings. Audit is batched per primary for readability; per-batch rationale carries representative entries.

### 6.1 Fire (32 pool entries; 20 currently allow-list)

**PRESERVE allow-list (12 entries):** ember, cinder, ash, lava, magma, lantern, torch, blaze, char, scorch, brand, flare. Substrate evidence supports all — material vocabulary (ember/cinder/ash/lava/magma) is substrate-canonical earth-fire; phenomenon vocabulary (blaze/scorch/brand/flare) is substrate-canonical; lantern/torch are pool-depth-anchor (low-power fire vessels canonical in tabletop_myth).

**DEMOTE-from-allow-list (8 entries):** soot, spark (routes to lightning flex per substrate), pitch, tar, charcoal, flint, tinder, coal. All substrate-thin (research did not surface these as core); demote to eligible preserves them in pool without elevating to allow-list. Substrate-honest read: these are pool-depth-over-curation from 2026-05-08 designer-extension.

**REMOVE (0 entries):** none. Substrate does not refute any fire entry.

**EXTEND new allow-list (4 entries from research):** blaze, scorch, inferno, ignite, agi, fira. Wait — blaze + scorch ALREADY in pool allow-list. New: inferno, ignite, agi, fira (4 substrate-research extensions).

**Eligible/quarantine preserved as-is:** oil, wax, candle, brazier, kindling, smoke (matt-considered-then-reverted-2026-05-12), steam, fume, flicker, glow, ignition, hearth. Substrate evidence does not move these.

### 6.2 Water (32 pool entries; 11 currently allow-list)

**PRESERVE allow-list (8 entries):** tide, brine, salt (water-primary preserve), ice, glacier, marsh, wake, wave. Substrate-aligned.

**DEMOTE-from-allow-list (3 entries):** rain, snow, slick. Substrate-thin (not in research candidates); demote to eligible.

**REMOVE (0 entries):** none.

**EXTEND new allow-list (6 entries from research):** torrent, glacial (as modifier-distinct-from-glacier), aqua, frost, chill, blizzara, bufu, mist (water-primary per § 5.1 routing).

**Eligible/quarantine preserved as-is:** current, eddy, foam, dew, slush, spring, stream, droplet, tear, sweat, blood (drift-14-alternative-liquid), sap, milk, honey, nectar, mercury (drift-14-alternative-liquid), bubble, lather, suds, ripple, pearl (drift-14-biological-organic), jelly.

### 6.3 Earth (33 pool entries; 22 currently allow-list)

**PRESERVE allow-list (22 entries):** stone, granite, slate, basalt, limestone, marble, clay, sand, ore, iron, copper, bronze, gold, silver, lead, rust, gem, crystal, geode, quartz, obsidian, amber. ALL substrate-aligned material vocabulary. Earth pool is the most substrate-honest of the existing pools.

**DEMOTE-from-allow-list (1 entry):** rust → eligible per substrate-distance from earth-canonical-material (rust is iron-decay-state not earth-substance). Designer-judgment surface — keep allow-list if Matt prefers decay-substance representation.

**REMOVE (0 entries):** none.

**EXTEND new allow-list (4 entries from research):** quake, tremor, terra, loam.

**Drift-14 cull-tag DISPOSITION (designer-judgment surface):** biological-organic cluster (bone / marrow / husk / shell / chitin / scale / horn / tooth / claw — 9 entries with drift-14-biological-organic cull-tag). Substrate evidence SILENT (not in research). Drift-14 cull verdicts retain per gandalf seam authority. Matt may dissolve drift-14 culls if designer-judgment prefers biological-earth canonical (D&D Bone Devil / FF Skeleton mob loot / etc.). Gandalf recommendation: keep drift-14 as-is.

**Eligible/quarantine preserved as-is:** chalk, mud, silt, gravel, pebble, web (earth-primary with wind flex; pool-existing), root, bark, wood, peat, moss, lichen, mold, rot, leaf, flower, petal, thorn (drift-14-plant-anatomical; substrate-confirms thorn as canonical — RECOMMEND dissolve drift-14 cull; PROMOTE thorn to allow-list per substrate vote), vine, soil, threshold, throne.

### 6.4 Wind (28 pool entries; 7 currently allow-list)

**PRESERVE allow-list (3 entries):** gale, plume, cloud (matt-promote-2026-05-12), dust (earth-flex; matches research). Sleet, frost, hail also currently allow-list — PRESERVE hail / sleet (atmospheric-cold-storm canonical); SHIFT frost to water-primary per § 4.2 routing.

**DEMOTE-from-allow-list (1 entry):** frost → SHIFT to water-primary per § 4.2 / § 5.2 routing.

**REMOVE (0 entries):** none.

**EXTEND new allow-list (9 entries from research):** tempest, cyclone, whirlwind, gust (PROMOTE from eligible-with-drift-14 — substrate vote dissolves drift-14-wind-storm-cluster-collapse), squall (PROMOTE from eligible-with-drift-14), hurricane (PROMOTE from eligible-with-drift-14), zephyr, boreas, sleet (already allow-list, no change).

**Drift-14-wind-storm-cluster-collapse DISPOSITION (designer-judgment surface):** typhoon / cyclone / tempest / squall / hurricane / gust currently carry drift-14-wind-storm-cluster-collapse cull-tag. Substrate evidence overwhelmingly supports these as core wind canonical (Phase 4 high-confidence). Gandalf recommendation: DISSOLVE drift-14 cull-tag per substrate vote; PROMOTE all 5 (cyclone / tempest / squall / hurricane / gust) to allow-list; KEEP typhoon eligible (substrate-honest oceanic variant; less canonical than hurricane in genre).

**Vocab-obscure / matt-demote / matt-promote lineage PRESERVED:** miasma (vocab-obscure; routes to shadow per § 5.3); rime (vocab-obscure; eligible); pall (vocab-obscure; eligible); shear (matt-demote; eligible); billow (matt-demote; eligible); cloud (matt-promote; allow-list preserve).

**Eligible/quarantine preserved as-is:** breath, mist (SHIFT to water per § 5.1), fog, vapor, draft (auditory-non-visual culture — KEEP eligible), sigh / whisper / whistle (auditory-non-visual quarantine — KEEP quarantine; substrate-honest non-substance), howl (drift-14-auditory-non-visual quarantine — KEEP), hum / thrum, pollen / spore / seed / feather (biological — KEEP per drift-14-style), gossamer / silk (material-substance not wind-phenomenon — KEEP quarantine), gauze / veil, billow (matt-demote), exhalation.

### 6.5 Lightning / Holy / Shadow / Physical (0 pool entries currently)

**NEW allow-list per § 4 TARGET (lightning 10 / holy 10 / shadow 12 / physical 9):**

- Lightning: arc, static, surge, volt, bolt, lightning, shock, spark, thunder, thundara
- Holy: radiance, radiant, dawn, aura, divine, sacred, blessed, lux, celestial, hama
- Shadow: void, shade, umbra, wraith, mudo, mamudoon, drain, necrotic, monarch, abyss, shadow, lich
- Physical: pierce, piercing, slash, slashing, bludgeoning, sever, strike, force, bleed (Architecture-A: taxonomy-sibling registry; Architecture-B: asymmetric pool)

All entries are EXTEND (substrate-research grounded) — first-time pool entries for these 4 primaries.

### 6.6 Summary of pool audit

| Action | Entry count |
|---|---:|
| PRESERVE allow-list (substrate-confirmed) | ~45 across fire/water/earth/wind |
| DEMOTE from allow-list (substrate-thin) | ~13 across fire/water/wind |
| REMOVE entirely | 0 |
| EXTEND new allow-list — research candidates (fire/water/earth/wind) | ~14 |
| EXTEND new allow-list — new primaries (lightning/holy/shadow/physical) | ~41 |
| Eligible / quarantine preserved as-is | ~96 |
| Drift-14 culls (designer-judgment surface for Matt) | wind-storm-cluster-collapse DISSOLVE recommended; biological-organic / alternative-liquid / auditory-non-visual / conceptual-not-substance / plant-anatomical KEEP recommended (with thorn exception — DISSOLVE) |

Total post-synthesis pool size: ~199 entries (156 existing - 0 removed + ~43 new = ~199); allow-list: ~92 entries (vs current 60 allow-list).

---

## 7. Borderline candidate disposition (92 single-track + lux + celestial)

Per Phase 4 § 10 + PG-2 § 5 acknowledgment. Single-track borderline is designer-judgment surface; this section per-candidate dispositions the high-value subset.

### 7.1 Per-primary borderline summary

| Primary | Borderline count | KEEP | DROP | DEFER-with-cross-track-required |
|---|---:|---:|---:|---:|
| fire | 12 | 4 (agi, fira, inferno, ignite per § 4.1) | 5 (smelt, sulphur, conflagration, hellfire, char-as-already-allow-list, crimson — actually some are already in pool) | 3 |
| water | 8 | 3 (aqua, frost, chill, blizzara, bufu) | 2 (rime — pool-existing eligible) | 3 (deluge, mercury, mist-routing) |
| earth | 5 | 2 (loam, terra) | 2 (bedrock, mineral) | 1 (salt) |
| wind | 19 | 5 (zephyr-already-confirmed, boreas, hurricane, tornado, vortex) | 6 (sirocco, vindsval, kari, eurus-Anemoi, notus, wu xing absent) | 8 (aeolus, zephyrus, sylph, djinn, aero, garu, blast, breeze, updraft, gale-force, wind-wall, gust-of-wind, aetherspouts, tempest-djinn, cyclonic-rift, stormtide, njord) |
| lightning | 8 | 6 (bolt, lightning, shock, spark, thundara, thunder) | 1 (plasma) | 1 (zio-alternative) |
| holy | 22 | 3 (hama, lux, celestial) | 8 (lambent, lucent, lumen, aureate, halcyon, luminary, solael, stellar) | 11 (resurrection, aura, seraph, consecrated, cura, cure, esuna, hamaon, mahama, mahamaon, reflect, aether, banish, corona, empyrion, gilded, holy-smite, sanctum, solar, greater-heal) |
| shadow | 18 | 4 (mudo, mamudoon, monarch, abyss) | 6 (cimmerian, bellion, dark-flame-master, domain-of-the-monarch, femto, grasp-heart, igris, negative-burst, shadow-exchange, shadow-linker, shadow-preserve, beru — partial: keep monarch / abyss; defer rest) | 8 |
| physical | 10 | 9 (pierce, sever, bleed, bludgeoning, force, piercing, slash, slashing, strike — § 4.8) | 1 (impale) | 0 (frame-dependent extensions per § 4.8) |

Totals: KEEP 36 / DROP ~32 / DEFER ~35 (some entries already in core allow-list and excluded from borderline counts).

### 7.2 High-value borderline per-candidate dispositions (Matt PG-3 surface)

These are the candidates where gandalf's lean has lower confidence than substrate-confirmed core — Matt designer-judgment input adds value.

**Lux + celestial (Phase 4 § 10.1 explicit flag):** both Latin-tier non-religious-coded holy vocabulary; single-track JRPG_isekai only; Phase 4 surfaces as DESIGNATED Matt designer-judgment per PG-1 § 2 surface 2 + PG-2 § 5. **Gandalf recommends INCLUDE both** — Latin-tier non-religious vocabulary is exactly the substrate gap PG-1 holy-curation-priority was targeting.

**Greek Anemoi (aeolus / boreas / notus / zephyrus / eurus):** mythological wind-pure depth; PG-2 § 5 + PG-1 § 1.5 explicit forward note. Gandalf includes zephyr (already high-confidence) + boreas; defers aeolus / zephyrus / notus / eurus to Matt designer-judgment. **Gandalf recommends ADD 1 from aeolus / zephyrus** for mythological-name richness.

**Solo Leveling shadow vocabulary (shadow exchange / shadow linker / shadow preserve / monarch / igris / beru / domain of the monarch):** isekai-genre-defining for D10 positioning; PG-2 § 5 explicit forward note. Gandalf includes monarch; defers depth question to Matt. **Gandalf recommends MATT-DECIDE Solo-Leveling depth between 1 (monarch only) and 4 (monarch + 3 of shadow-exchange / shadow-linker / igris / beru).**

**Grim Dawn Order constellation (empyrion / solael):** PG-1 surface 2 explicit target; ARPG non-religious-coded representation. Gandalf does not include in TARGET 10; defers to Matt. **Gandalf recommends INCLUDE empyrion as 11th entry** if Matt wants ARPG-non-religious-coded representation.

**FF holy vocabulary (resurrection / cura / cure / esuna):** JRPG mechanical-keyword core. Gandalf does not include (substrate-thin against non-religious-coded curation priority); defers to Matt. **Gandalf recommends MATT-DECIDE FF representation depth — if Matt prefers FF representation, swap hama → cura.**

**Solo Leveling representations in shadow (substrate-thin single-track candidates):** dark wisdom / death lord / sovereign / umbral. Gandalf does not include; substrate too thin. DROP per default unless Matt elevates.

**Decay cluster (blight / decay / miasma) per § 5.3:** substrate-honestly shadow-primary with earth-flex; gandalf retains as eligible. **Gandalf recommends MATT-DECIDE whether to promote 1 of (blight) to allow-list as substrate-distinct ARPG / D&D canonical** (PoE Blight league recognizability is high).

---

## 8. Q18.a-e structural decisions (consolidated per evidence)

Per operational sequence § 0 Q18.a-e structure. Gandalf-substrate-led proposal; Matt ratifies at PG-3.

### 8.1 Q18.a — Primary scope

**Question:** which primaries get flavor pools?

**Architecture A:** 7 rotating primaries (fire / water / earth / wind / lightning / holy / shadow) carry flavor pools. Physical carries a taxonomy-sibling registry (separate semantic layer).

**Architecture B:** all 8 primaries carry flavor pools. Physical's pool is asymmetric (mechanical-taxonomy not phenomenological-flavor).

**Gandalf proposal:** Architecture A. PG-3 Matt decision.

### 8.2 Q18.b — Source of authority

**Question:** how is the locked allow-list authoritatively grounded?

**Gandalf proposal:** vote-grounded research + designer curation overlay at encoding gate. Per Discipline #41 substrate-led refinement: genre-vote determines candidate inclusion; designer-curation routes per-candidate slots, applies cardinality TARGET, weighs Reincarnated-fit. NEITHER pure-designer-assertion NOR pure-vote-grounded; the substrate VOTES, the designer ENCODES.

**Operational implementation:** Phase 4 high-confidence core (score ≥ T6 AND tracks ≥ 2) is the substrate-grounded anchor; Phase 5a synthesis (this artifact) applies the encoding gate; pool.json migration (sub-phase 5f) operationalizes the lock.

### 8.3 Q18.c — Flex semantics

**Question:** how is cross-primary contamination encoded?

**Gandalf proposal:** preserve existing `flex_slots` field in pool.json schema (per pool.json v1.0 spec). Per-candidate slot routing decisions (§ 5 of this synthesis) become explicit primary + flex_slots assignments. Substrate-evidence `cross_primary_contamination` field from research dataset feeds the flex_slots determination but is NOT preserved verbatim in pool.json (it's a synthesis-stage input, not a runtime field).

**Operational implementation:** sub-phase 5f migration encodes flex_slots per § 5.1 / § 5.2 / § 5.3 / § 5.4 routings.

### 8.4 Q18.d — d1_status filter

**Question:** how does the d1_status (allow-list / eligible / quarantine) filter compose with substrate vote?

**Gandalf proposal:** preserve existing 3-state d1_status filter. Substrate-evidence informs d1_status default per the following discipline:
- Substrate score ≥ T6 AND tracks ≥ 2 → default `allow-list`
- Substrate score ≥ T6 AND tracks = 1 (single-track borderline) → default `eligible`; designer-judgment may PROMOTE
- Substrate score < T6 → default `eligible` if research-cited; `quarantine` if not research-cited and pool-existing-only
- Vocab-obscure flag (project memory matt-demote lineage) → demote to `eligible` regardless of substrate score (vocabulary_commonness sub-property amendment)
- Slot-unambiguous check (smoke-as-fire vs smoke-as-wind precedent) → flag for designer-judgment; demote if ambiguous

**Operational implementation:** d1_status amendment to pool.json schema adds `vocabulary_commonness` sub-property and `slot_unambiguous` flag per project memory. Defer schema amendment to sub-phase 5f post-wave dispatch.

### 8.5 Q18.e — Cardinality target

**Question:** what cardinality per primary?

**Gandalf proposal:** per-primary substrate-honest natural-depth TARGET (not floor; not ceiling). Per § 3 table.

**Operational implementation:** sub-phase 5f migration enforces cardinality TARGET via curation; LLM judgment at WS1A.3 / WS1A.4 stays bounded to allow-list (substrate-grounded).

---

## 9. Phase 5b Pattern B framing for Matt

This section operationalizes what Matt needs to lock at PG-3 architectural-commitment.

### 9.1 What lands at PG-3

**Decision 1: Architecture A vs B (7-vs-8 lock).** Substrate evidence + genre-canonical convergence + Reincarnated-fit reasoning + gandalf soft lean Architecture A. Matt's call.

**Decision 2: Per-primary allow-list final ratification.** Gandalf-drafted allow-lists per § 4 surface to Matt for ratification / amendment. Cardinality TARGETS may be amended per Matt design preference. Per-candidate inclusion is substrate-grounded.

**Decision 3: Q18.a-e structural commitments.** Gandalf-substrate-led proposals per § 8 surface for Matt ratification.

**Decision 4: Borderline disposition** for the high-judgment-value subset:
- Lux + celestial inclusion (gandalf recommends INCLUDE)
- Anemoi inclusion depth (gandalf: zephyr + boreas; Matt may add aeolus / zephyrus / notus)
- Solo Leveling shadow depth (gandalf: monarch only; Matt may add shadow-exchange / shadow-linker / igris / beru)
- Empyrion / Solael inclusion (gandalf: include empyrion as 11th holy if Matt wants ARPG representation)
- Grim Dawn Order constellation depth in holy
- FF representation in holy (hama vs cura vs resurrection)

**Decision 5: Cull-tag disposition** for existing pool drift-14 flags:
- drift-14-wind-storm-cluster-collapse → gandalf recommends DISSOLVE per substrate vote
- drift-14-biological-organic → gandalf recommends KEEP (substrate-silent; preserve designer-prior-judgment)
- drift-14-alternative-liquid → gandalf recommends KEEP
- drift-14-auditory-non-visual → gandalf recommends KEEP
- drift-14-conceptual-not-substance → gandalf recommends KEEP
- drift-14-plant-anatomical → gandalf recommends DISSOLVE for thorn specifically (substrate confirms canonical)

### 9.2 Pre-empted Matt counter-questions

**Q: Why not 8-primary symmetric with physical asymmetry tolerated?**
A: § 2.5 gandalf reasoning: substrate has voted unambiguously taxonomic; genre-canonical convergence is uniformly Architecture A; `config/elements.yaml` is ALREADY shaped for A; WS1A.3 / WS1A.4 downstream consumers are cleaner against A. Architecture B is substrate-defensible but pre-empts genre-canonical convention without strong reason.

**Q: Why wind TARGET 12 not closer to substrate T6=21?**
A: § 3.3 + § 4.4: substrate-honest natural-depth is below T6 because storm-flex is heavily concentrated (cardinality dilution); wind-PURE is structurally thin; the 12 entries balance storm-flex (6) + wind-PURE (2) + Anemoi mythological-depth (2) + atmospheric-cold (2). T6=21 would saturate with storm-cluster vocabulary that becomes hard for LLM flavor judgment to differentiate.

**Q: Why holy TARGET 10 not closer to substrate T6=19?**
A: § 4.6: T6=19 reflects religious-coded saturation; PG-1 § 2 surface 2 + PG-2 § 4.2 carry the non-religious-coded curation priority; the 10 entries prioritize substrate-distinct depth over religious-coded breadth. If Matt prefers higher religious-coded representation, raise to 12-14.

**Q: Why earth preserve 22 pool depth?**
A: § 4.3: T6=3 is RESEARCH-thin not substrate-thin; earth pool was deeply curated 2026-05-08 against substrate-aligned material vocabulary (granite / slate / basalt / marble / clay / ore / iron / etc.); substrate confirms pool was right; no migration warranted; cardinality TARGET = pool-depth-preserve.

**Q: What about the drift-14 culls? Should they all dissolve per substrate?**
A: § 6 + § 9.1 Decision 5: substrate evidence is silent on most drift-14 culls (biological-organic / alternative-liquid / etc. weren't in research candidates because the research was scoped to substrate-popular vocabulary). Substrate-silence does NOT validate prior cull-judgment; it just doesn't refute it. Gandalf recommends KEEP per default; Matt may dissolve any specific cull per designer-judgment. Only drift-14-wind-storm-cluster-collapse has substrate-vote DISSOLVE recommendation (cyclone / tempest / squall / hurricane are unambiguously substrate-canonical wind).

**Q: What about thorn? It's pool-existing eligible with drift-14-plant-anatomical cull-tag and substrate confirms it.**
A: § 4.3 + § 6.3: substrate vote dissolves drift-14-plant-anatomical for thorn specifically; PROMOTE thorn to earth allow-list. Other plant-anatomical entries (vine / root / bark / wood) remain per default.

**Q: Migration impact on existing infrastructure?**
A: sub-phase 5f (POST-WAVE) operational migration dispatch handles pool.json extension + schema amendment for vocabulary_commonness + slot_unambiguous + downstream consumer updates. WS1A.3 / WS1A.4 implementation work consumes the locked pool post-canonical-write. No engine architecture change required.

### 9.3 Suggested Pattern B flow for Matt

1. Open with the 7-vs-8 architectural surface (§ 2). Walk through substrate evidence + genre-canonical convergence + Reincarnated-fit + gandalf lean. Land decision early — everything downstream composes against it.
2. Per-primary allow-list walkthrough (§ 4). Start with strongest substrate-anchor primaries (earth, fire, water, lightning) — quick ratifications. Then high-judgment-value primaries (wind, holy, shadow). Land physical disposition per Architecture A or B.
3. Borderline candidate sweep (§ 7.2). Per-decision: KEEP / DROP / DEFER per Matt designer-judgment.
4. Q18.a-e structural commitments (§ 8). Likely fast ratifications if § 2 + § 4 land cleanly.
5. Cull-tag disposition sweep (§ 9.1 Decision 5).
6. PG-3 lock confirmation; route Phase 5c canonical write authoring.

Estimated Pattern B engagement: 1-2 sessions depending on architectural decision tempo.

---

## 10. Recognition / pattern-set / cross-wave composition

### 10.1 What this wave establishes

**Recognition record (gandalf seam):** the substrate-led-applied-to-vocabulary pattern (research → stats → synthesis → encoding-gate at designer-curation) IS the canonical methodology for vocabulary-lock decisions. WS1A.Q18 operationalizes Discipline #41 at the vocabulary-substrate layer (vs the P2/P3 geometry-substrate layer already canonical).

**Pattern-set:** the WS1A.Q18 wave shape (5 phases internally gated; PG-0 elrond data-medium / PG-1 gandalf triage / PG-2 gandalf stats-sufficiency / PG-3 Matt architectural-commitment / PG-4 jack-ryan wave-close) is the template for Q16 / Q17 / Q19 hard-blocker waves. Pattern-setting reduces orchestration overhead for subsequent waves by ~30-40% per gandalf estimate.

### 10.2 Cross-wave composition

**WS1A.Q16 (per-skill flavor judgment LLM prompt design):** composes against the locked Q18 pool. Q18 deliverable becomes Q16 input substrate. Q16's research scope shifts to LLM-prompt-design canon (FF / SMT spell-naming conventions; PoE skill-name patterns; D&D 5e formal taxonomies) rather than vocabulary-substrate (which Q18 settled).

**WS1A.Q17 (hybrid kit element pair selection):** composes against the locked Q18 pool + Q16 judgment design. Hybrid kit pairs primaries; per-pair sub-element selection consumes Q18 allow-lists per primary.

**WS1A.Q19 (emergent kit concept naming consistency):** composes against Q16 LLM judgment + Q18 pool. Naming consistency validates per-kit naming against (primary + sub-element + form + ailment) coherence per Q18 vocabulary.

### 10.3 What this wave does NOT establish

- Operational pool.json migration discipline (sub-phase 5f territory)
- WS1A.3 implementation (consumes Q18 lock; downstream)
- Substrate library extension methodology (rocket / elrond canonical lineage; out-of-scope)
- Engine architecture amendment (no engine change required)

---

## 11. Phase 5b Pattern B decisions surfaced (1-line each)

1. **Architecture A vs B (7-vs-8 lock)** — gandalf soft lean A; Matt PG-3 architectural-commitment authority
2. **Per-primary allow-list ratification** — gandalf-drafted § 4 surfaces for Matt approval / amendment
3. **Q18.a-e structural commitments** — gandalf-substrate-led proposals § 8 surface for Matt ratification
4. **Lux + celestial inclusion in holy** — gandalf recommends INCLUDE (PG-1 + PG-2 forward-noted Matt-decision)
5. **Anemoi inclusion depth in wind** — gandalf includes zephyr + boreas; Matt may add 1-2 more
6. **Solo Leveling shadow depth** — gandalf includes monarch only; Matt may add 1-3 more for isekai positioning
7. **Empyrion / Solael inclusion** — gandalf recommends ADD empyrion (PG-1 ARPG-non-religious-coded surface)
8. **Drift-14-wind-storm-cluster-collapse cull dissolution** — gandalf recommends DISSOLVE per substrate vote
9. **Drift-14-plant-anatomical thorn promotion** — gandalf recommends DISSOLVE-for-thorn; substrate-confirms canonical
10. **Other drift-14 cull dispositions** — gandalf recommends KEEP per substrate-silence; Matt may dissolve per designer-judgment
11. **Vortex water-vs-wind routing** — gandalf recommends WIND per substrate-rotational-primary
12. **Mist water-vs-wind routing** — gandalf recommends WATER per substrate-atmospheric-water root
13. **FF holy representation choice** — gandalf picks hama; Matt may swap to cura / resurrection / esuna
14. **Vocabulary_commonness + slot_unambiguous schema amendment** — gandalf recommends YES per project memory lineage; defer schema migration to sub-phase 5f
15. **Cardinality TARGET ratification** — gandalf TARGETS per § 3; Matt may amend per design preference

---

## 12. Disciplines composed

### 12.1 Discipline #41 (substrate-led)

Composition: substrate vote (Phase 4 high-confidence core + existing pool depth) ANCHORS per-primary allow-list curation; designer-curation overlays at the encoding gate (this synthesis) without overriding substrate vote. § 1 explicit composition. § 4 per-primary tables anchor on Phase 4 high-confidence + pool-evidence. § 5 contamination routing applies substrate-honest slot determination.

### 12.2 Discipline #42 (framing-audit Q1-Q3)

**Q1 — Load-bearing assumptions in this synthesis:**
- (a) Phase 4 stats verdict is substrate-honest empirical evidence (verified at PG-2 RATIFIED)
- (b) Architecture A is substrate-led soft lean (substrate vote + genre canon + Reincarnated-fit composition)
- (c) Cardinality TARGETS are substrate-honest natural-depth between T6 floor and pool-depth (not arbitrary designer preference)
- (d) Per-candidate routing at contamination cells follows substrate-honest primary identity (not designer-preference)
- (e) Existing pool entries authored 2026-05-08 represent prior substrate-vote (designer-encoded against same canonical-7+1); preserve where research corroborates
- (f) Borderline single-track candidates are designer-judgment surfaces; substrate-silence does NOT equal substrate-refutation

**Q2 — Refutation evidence in current scope:**
- (a) verified via PG-2 ratification at commit `5ad97e7`; methodology fidelity 5/5
- (b) substrate evidence (§ 2.1) + genre-canonical evidence (§ 2.2) + Reincarnated-fit (§ 2.3) all converge on A; refutation requires Matt preferring symmetric primary count over substrate-honest asymmetric flavor pools — substrate-defensible but pre-empts genre canon
- (c) cardinality TARGETs in § 3 are explicitly substrate-honest (e.g., wind ≠ T6=21 because storm-flex dilutes; earth ≠ T6=3 because pool was substrate-aligned ahead of research); Matt amendment surface preserved
- (d) per-candidate routing decisions in § 5 are substrate-evidenced (mist's atmospheric-water root; tempest's overwhelmingly wind-evidenced canonical etc.); each routing decision is reversible per Matt designer-judgment
- (e) existing-pool audit in § 6 explicitly carries DEMOTE verdicts where substrate-thin (rust / rain / snow / etc.) without auto-REMOVAL; substrate-silence preserved per project-memory cull-tag lineage
- (f) borderline disposition in § 7 explicitly defers high-judgment-value candidates (lux / celestial / Anemoi / Solo Leveling vocabulary / Grim Dawn Order constellations) to Matt PG-3

**Q3 — Refinement needed:**
- ONE refinement at Phase 5b Pattern B: if Matt selects Architecture B, § 4.8 physical allow-list extends from 9 to 12 with crush / impact / rend; otherwise stays 9
- TWO refinement candidates Matt may surface at PG-3: (a) raise holy cardinality TARGET to 12-14 if religious-coded representation is desired; (b) raise Solo Leveling shadow depth from 1 to 3-4 if isekai-positioning is heavier-weighted
- NO further synthesis refinement needed at gandalf seam scope; Phase 5b dialogue surfaces refinements via Matt designer-judgment

**Framing-audit verdict:** synthesis is substrate-coherent; surfaces appropriately gated for Matt PG-3 ratification.

### 12.3 Discipline #18 (math-hotspot methodology consultation composition)

This synthesis is downstream of Phase 4 statistical analysis (the math hotspot) and Phase 0 elrond data-medium consultation (the methodology gate). Composition: methodology lock at PG-0 → execution at Phase 4 → synthesis-encoding at Phase 5a (this artifact) → architectural-commitment at PG-3 → canonical lock at Phase 5c. Each step composes the prior step's verdict without re-litigating it; this synthesis ratifies Phase 4 verdicts as substrate-input without methodology re-derivation.

---

## 13. Sign-off

**Phase 5a synthesis draft: COMPLETE.**

**Authority chain:**
- Matt 2026-06-01 verbatim "hand to KR to fire the wave"
- Hive-mind decision-routing Matt 2026-05-23: Phase 5a synthesis-curation is gandalf design-side seam authority
- Gandalf PG-2 RATIFIED at commit `5ad97e7` (3 forward notes operationalized in this synthesis)
- Pattern A-deep / authoring scope per operational sequence § 2 Phase 5a

**Disciplines composed:**
- Discipline #41 substrate-led (§ 1 + § 12.1 explicit composition; substrate vote ANCHORS curation)
- Discipline #42 framing-audit (§ 12.2 Q1-Q3 application)
- Discipline #18 math-hotspot composition (§ 12.3 methodology-lock → execution → synthesis chain)

**Forward to Phase 5b Pattern B:**
- § 2 carries 7-vs-8 architectural surface for Matt PG-3 decision
- § 4 carries per-primary curated allow-list recommendations
- § 5 carries curation-decision sections for contamination pairs
- § 6 carries existing-pool audit per Q-shape-4 ratification
- § 7 carries borderline candidate disposition
- § 8 carries Q18.a-e structural decisions
- § 9 carries Phase 5b Pattern B framing
- § 11 enumerates 15 PG-3 decision surfaces with 1-line each

**Forward to Phase 5c canonical write (POST-PG-3-Matt-ratification):**
- Phase 5c canonical write at `canonical/story/2026-06-XX-flavor-pool-per-primary-element-lock.md` consumes this synthesis (per Matt PG-3 amendments) as primary input
- Pool.json migration is sub-phase 5f POST-WAVE territory (out-of-scope here)

**Routing instruction for KR:**
- Update wave-state: Phase 5a COMPLETE + Phase 5b SURFACED-TO-MATT
- Halt for Matt Pattern B engagement at Phase 5b
- Matt's next touchpoint: PG-3 architectural-commitment lock at Phase 5b Pattern B with gandalf

**End of Phase 5a synthesis draft.**
