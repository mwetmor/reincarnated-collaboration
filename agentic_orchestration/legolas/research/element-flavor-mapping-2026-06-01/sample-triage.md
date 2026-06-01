# WS1A.Q18 Phase 2 — In-Seam Triage Verdict

**Owner:** legolas (Mode A analyzer)
**Wave:** `WS1A.Q18-flavor-pool-research`
**Phase:** Phase 2 (in-seam triage; fires automatically after all 3 samplers return)
**Date:** 2026-06-01
**Input files:**
- `sample-A.jsonl` (48 rows; ARPG track)
- `sample-B.jsonl` (40 rows; JRPG_isekai track)
- `sample-C.jsonl` (37 rows; tabletop_myth track)
- `sample-A.manifest.json`, `sample-B.manifest.json`, `sample-C.manifest.json`
**Total corpus:** 125 rows across 3 tracks × 8 primaries

**Routing:** this triage feeds PG-1 (gandalf ratification of Phase 3 scope). EXPAND/TERMINATE/NARROW proposals are legolas Phase 2 judgments; gandalf ratifies at PG-1.

---

## 1. Track-Viability Matrix (8 × 3)

Per-cell scores anchored on manifest yield judgments + row counts + qualitative evidence.

| Primary     | ARPG (A)   | JRPG_isekai (B) | tabletop_myth (C) |
|-------------|------------|-----------------|-------------------|
| fire        | STRONG     | STRONG          | STRONG            |
| water       | STRONG     | STRONG          | STRONG            |
| earth       | STRONG     | MEDIUM          | MEDIUM            |
| wind        | MEDIUM     | STRONG          | MEDIUM            |
| lightning   | STRONG     | STRONG          | STRONG            |
| holy        | MEDIUM     | MEDIUM          | STRONG            |
| shadow      | STRONG     | STRONG          | STRONG            |
| physical    | MEDIUM     | STRONG          | STRONG            |

**Score definitions:** STRONG = dense, well-cited, multi-source yield; MEDIUM = yield present but shallower, fewer citations, or structurally constrained; WEAK = near-zero useful yield; MISALIGNED = track structurally wrong for this primary (none found across all 24 cells).

**Notable cells:**
- Wind/ARPG (MEDIUM): cyclone is the best ARPG wind term; genre treats wind through storm/lightning conflation. Gap remains.
- Wind/tabletop_myth (MEDIUM): only 3 rows; MTG doesn't have a wind-exclusive vocabulary; D&D Tempest Domain blends wind+lightning.
- Holy/ARPG (MEDIUM): vocabulary is valid but concentrated in Paladin/Crusader class archetypes with religious-coding risk (divine, blessed, sanctum). Dawn and radiant are tone-safe.
- Holy/JRPG_isekai (MEDIUM): structurally dominated by proper-nouns (Hama, Holy) rather than flavor sub-vocabulary. Functional for player recognition but lacks sub-element depth.
- Physical/ARPG (MEDIUM): ARPG canon is DIVIDED — PoE treats bleed as ailment, Grim Dawn as sibling type. The vocabulary exists but lacks cross-source consensus on its structural role.

---

## 2. Per-Track Keep / Drop / Narrow Recommendation

### Track A — ARPG (keep; targeted expansion on 2 cells)

**Verdict: KEEP all 8 primaries. EXPAND on wind and holy.**

Reasoning:
- Fire, water, earth, lightning, shadow all returned STRONG with multi-source citation. These cells are saturated at the sampler level; Phase 3 expansion would yield diminishing returns.
- Wind: MEDIUM because ARPG conflates wind with storm/lightning. However, Diablo 4 Druid wind skills and squall/whirlwind vocabulary was flagged as under-surveyed. Worth one targeted expansion pass focused on D4 Druid + Lost Ark wind skills.
- Holy: MEDIUM due to religious-coding concentration. Sampler-A recommends expansion specifically to survey non-religious light sub-vocabulary (aureate, luminary, corona) and Grim Dawn Order affinity constellation names. This is a real gap.
- Physical: MEDIUM but the vocabulary exists. The structural question (sub-element vs ailment) is a design-side decision (PG-3), not a research gap per se. Sampler-A has good coverage of bleed/pierce/sever/crush/impale. No expansion needed.

### Track B — JRPG_isekai (keep; targeted expansion on 2 cells)

**Verdict: KEEP all 8 primaries. EXPAND on shadow and holy.**

Reasoning:
- Fire, water, wind, lightning, physical all returned STRONG with well-cited sources.
- Shadow: STRONG but Solo Leveling's shadow system has deeper sub-vocabulary not yet surfaced (Shadow Exchange, Shadow Preserve, Shadow Linker as individual shadow ability names). Sampler-B explicitly recommends expansion. This is the most promising expansion cell across all three tracks.
- Holy: MEDIUM due to JRPG structural limitation — genre uses proper-nouns (Hama, Holy) as primary names rather than sub-element flavor words. Targeted expansion on isekai cleric/paladin class vocabulary could yield Mushoku Tensei and Overlord divine magic sub-vocabulary. Worth one pass.
- Earth: MEDIUM. Only 4 rows. Mushoku Tensei earth magic and Persona earth skills were flagged as under-surveyed. However, earth is already STRONG in ARPG and MEDIUM in tabletop — the gap is less urgent than holy/shadow.

### Track C — tabletop_myth (keep; targeted expansion on 1 cell)

**Verdict: KEEP all 8 primaries. EXPAND on wind only.**

Reasoning:
- Fire, water, lightning, holy, shadow, physical all returned STRONG or near-STRONG. Tabletop is the strongest track for formal damage-type vocabulary and mythological sources.
- Wind: 3 rows is the weakest primary yield across the entire 24-cell matrix. MTG Blue conflates wind with water/island; D&D Tempest Domain conflates wind with lightning. Greek/Norse wind deity vocabulary (Aeolus, Boreas, Zephyrus, Kari) was flagged but not surfaced. One targeted expansion focused on mythological wind deity vocabulary would fill this gap.
- Holy: STRONG (radiant as D&D formal damage type is the key tabletop_myth find). No expansion needed.
- Physical: STRONG (D&D Bludgeoning/Piercing/Slashing trinity is the strongest evidence for 8-element treatment). No expansion needed.

---

## 3. Per-Primary Cross-Source Contamination Report

Candidates appearing in multiple primaries (across all 3 JSONL files, counting both explicit multi-primary rows and cross_primary_contamination flags):

**15 flex candidates identified:**

| Candidate    | Primary        | Contaminates   | Notes |
|--------------|----------------|----------------|-------|
| aether       | holy           | lightning      | Victorian electrical-aether conflation; also classical 5th element |
| aqua         | water          | holy           | KonoSuba: water goddess = divine purification |
| aura         | holy           | wind           | Aura-as-emanation overlaps with wind presence |
| blight       | shadow         | earth          | Organic decomposition is earth-adjacent |
| decay        | shadow         | earth          | Same decomposition overlap as blight |
| dust         | earth          | wind           | Dust is airborne earth |
| hellfire     | fire           | shadow         | Infernal fire has shadow underworld semantics |
| mercury      | water          | lightning      | Quicksilver = speed = electrical metaphor |
| mist         | water          | wind           | Airborne water vapor |
| salt         | earth          | holy           | Folk magic: protective salt circle = purification |
| smelt        | fire           | earth          | Smelting fire + metal/earth transformation |
| squall       | wind           | water          | Rain-squall carries water |
| sulphur      | fire           | shadow         | Brimstone/infernal association |
| tempest      | wind           | lightning      | Storm = wind + lightning (D&D Tempest Domain formalizes this) |
| vortex       | wind           | water          | PoE Vortex is cold-damage; whirlpool framing |

**High-contamination primaries:** wind and shadow are each party to 5+ contamination pairs. Earth has 4 contamination relationships. These primaries need tightest design-side curation at PG-3.

**Cross-track confirmed candidates (appearing in 2+ tracks; high confidence):**

| Candidate  | Tracks confirmed                    | Primary        |
|------------|-------------------------------------|----------------|
| void       | ARPG + JRPG_isekai + tabletop_myth  | shadow         |
| stone      | ARPG + JRPG_isekai + tabletop_myth  | earth          |
| shade      | ARPG + JRPG_isekai + tabletop_myth  | shadow         |
| arc        | ARPG + tabletop_myth                | lightning      |
| cinder     | ARPG + tabletop_myth                | fire           |
| ember      | ARPG + tabletop_myth                | fire           |
| radiant    | ARPG + tabletop_myth                | holy           |
| sacred     | ARPG + tabletop_myth                | holy           |
| glacial    | ARPG + tabletop_myth                | water          |
| tremor     | ARPG + tabletop_myth                | earth          |
| static     | ARPG + tabletop_myth                | lightning      |
| volt       | ARPG + tabletop_myth                | lightning      |
| quake      | ARPG + JRPG_isekai                  | earth          |
| pierce     | ARPG + JRPG_isekai                  | physical       |
| surge      | ARPG + JRPG_isekai                  | lightning      |

Triple-confirmed candidates (void, stone, shade) are the highest-confidence Phase 5 allow-list candidates.

---

## 4. Content / Constraint / Alignment Issues

### 4.1 Constraint issues

**Holy vocabulary — religious-coding risk:**
- Flagged by Sampler-A, echoed by Sampler-C. `divine` (D&D formal magic school) and `blessed`/`consecrated`/`sanctum` carry direct religious connotation.
- `radiant` (D&D formal damage type) and `dawn` (D&D Xanathar spell + solar mythology) are the cleanest options — formal game-mechanical vocabulary without denominational religious framing.
- `sacred` sits in between — D&D has a cantrip named Sacred Flame (mechanically grounded) but the word itself carries religious flavor. Manageable with framing context.
- **Constraint: any Holy allow-list entry that is primarily a religious term should be flagged as `track_alignment_concern: religious_coding` for gandalf's PG-3 curation.**

**Shadow vocabulary — decay/earth contamination:**
- `blight` and `decay` both contaminate shadow↔earth. These candidates are in the ARPG corpus with genuine shadow citations (Diablo blight ailment, Last Epoch decay aura) but their substrate meaning is organic decomposition, which maps naturally to earth. Design-side question: does Reincarnated want shadow to have decay sub-vocabulary, or should decay be reserved for earth?
- **Constraint: blight/decay are dual-primary candidates; their assignment to shadow vs earth is a design-side decision at PG-3, not a research question.**

### 4.2 Alignment issues

**Tabletop_myth holy vocabulary — over-formal mechanical vocabulary:**
- Tabletop_myth track's strongest holy yield includes Bludgeoning/Piercing/Slashing (physical) and Radiant/Necrotic/Force (D&D formal damage types). These are rigorously defined but they are *mechanical keywords*, not *flavor substrate words*. For the Reincarnated allow-list (which feeds player-facing LLM flavor generation), a mechanical keyword like `bludgeoning` may be too explicitly game-mechanical.
- **Alignment: mechanical keywords surfaced in tabletop_myth (bludgeoning, piercing, slashing, force, necrotic) should be treated as vocabulary-validation references for recognizability, but Phase 5 curation should prefer flavor-substrate variants (blunt/pierce/sever/crush) over the mechanical keywords themselves.**

**JRPG_isekai holy vocabulary — proper-noun dominance:**
- Track B's holy yield is structurally dominated by proper-nouns (Hama, Holy). These are player-recognizable within JRPG fanbase but are effectively element-primary names rather than sub-element flavor words. Using `hama` or `holy` as a sub-element flavor keyword would be semantically confusing.
- **Alignment: JRPG_isekai proper-noun holy vocabulary (Hama, Holy as primary element names) should NOT be promoted to the sub-element allow-list. Expansion should focus on non-proper-noun holy descriptors.**

**JRPG_isekai alchemical/scientific lightning vocabulary:**
- `plasma` and `surge` both appear in JRPG_isekai with manhwa citations (Solo Leveling, SAO). These are contemporary-scientific lightning vocabulary, not mythological. For Reincarnated's isekai positioning this may be appropriate — isekai genre frequently blends contemporary-scientific with fantasy.
- **Alignment: plasma/surge are JRPG-provisional candidates; recognizability check recommended at PG-3 (are these recognizable as lightning-flavored to the target audience?).**

### 4.3 Content issues (zero-yield cells)

No cell has zero yield. The weakest cells by row count:
- Wind/tabletop_myth: 3 rows (only above-zero; no zero cells)
- Earth/JRPG_isekai: 4 rows
- Earth/tabletop_myth: 4 rows

These are thin but not empty. EXPAND recommendations in § 2 address the thin cells.

---

## 5. Scope-Adjustment Proposal for Phase 3

Per operational sequence soft cap ≤6 expansion sub-agents. This proposal fits within 5 cells (under cap):

| Cell                      | Verdict     | Rationale                                                                                                                 | Projected rows |
|---------------------------|-------------|---------------------------------------------------------------------------------------------------------------------------|----------------|
| ARPG × wind               | EXPAND      | Diablo 4 Druid wind skills + Lost Ark wind skills under-surveyed; squall/whirlwind gap; moderate depth available         | ~6-8           |
| ARPG × holy               | EXPAND      | Non-religious light sub-vocabulary (aureate, luminary, corona); Grim Dawn Order affinity constellations explicitly flagged | ~6-8           |
| JRPG_isekai × shadow      | EXPAND      | Solo Leveling shadow system has documented deeper sub-vocabulary (Exchange/Preserve/Linker); Overlord undead sub-vocabulary | ~8-10          |
| JRPG_isekai × holy        | EXPAND      | Isekai cleric/paladin vocabulary not yet mined (Mushoku Tensei divine magic; Overlord divine-class abilities)             | ~5-7           |
| tabletop_myth × wind      | EXPAND      | 3-row gap; Greek/Norse wind deity vocabulary (Aeolus, Boreas, Zephyrus, Kari) + MTG Blue storm cards under-surveyed      | ~6-8           |

**TERMINATE (none):** no track × primary cell has weak enough signal to terminate. Even the weakest cells (wind/tabletop_myth at 3 rows; earth/JRPG at 4 rows) have valid yield. TERMINATE is not warranted.

**NARROW (none):** no cell is so deep that pre-conditioned scope is needed at this stage. The sampler-level yields are not over-saturated for any cell.

**Cells with explicit STOP from sampler recommendations (no expansion needed):**
- Fire × all 3 tracks (STRONG across the board; sampler-A/B/C all recommended STOP)
- Water × all 3 tracks (STRONG across the board)
- Earth × ARPG (STRONG; 5 rows; Sampler-A STOP)
- Lightning × all 3 tracks (STRONG across the board)
- Shadow × ARPG (STRONG; Sampler-A STOP)
- Shadow × tabletop_myth (STRONG; Sampler-C STOP)
- Physical × all 3 tracks (vocabulary exists; 7-vs-8 question is design-side, not research gap)

**Total expansion sub-agents proposed: 5** — within the ≤6 soft cap. No over-cap re-ratification needed.

**Expansion sub-agents shaped for parallelism:** all 5 cells are independent (no cross-cell data dependency). Can fire as a single 5-way parallel fan-out at Phase 3.

---

## 6. Preliminary 7-vs-8 Signal (Composed Across 3 Samplers)

**Composed signal: Genre canon FAVORS 8-element treatment (physical with sub-element vocabulary) but with an important structural caveat.**

Evidence summary per track:

**Track A (ARPG) — DIVIDED, leaning 7-element:**
- PoE: bleed = ailment, impale = debuff. NOT sub-elements.
- Grim Dawn: pierce and bleed as SIBLING damage types with own resistances. FOR 8-element.
- Diablo, Torchlight, Last Epoch: physical = flat primary. FOR 7-element.
- Net ARPG read: majority of sources treat physical as flat-primary; Grim Dawn is the minority counter-signal.

**Track B (JRPG_isekai) — STRONGLY FOR 8-element:**
- Persona 3: formal Slash/Strike/Pierce taxonomy with enemy weakness tracking — the same mechanical structure as tracking Fire/Ice/Lightning weaknesses. This is the strongest genre evidence found.
- Mushoku Tensei / Slime isekai: distinguish physical impact from elemental damage.
- Net JRPG read: Persona 3's formal sub-type taxonomy is the clearest argument for treating physical as a sub-element-layered primary.

**Track C (tabletop_myth) — STRONGLY FOR 8-element:**
- D&D 5e: formal Bludgeoning/Piercing/Slashing damage types with distinct creature interactions (werewolf immunity to non-magic slashing; vampire immunity to piercing). Force = fourth physical-adjacent type.
- Pathfinder 2e: formalizes further with trait system.
- Net tabletop read: most rigorous formal taxonomy; D&D treats physical with a 3-way sub-type split that has mechanical consequences.

**Composed verdict:**
2 of 3 tracks STRONGLY support 8-element treatment; 1 track is divided but the majority of ARPG sources lean 7-element. The evidence favors 8-element treatment. However, the structural caveat is important: tabletop sub-types are *mechanical keywords* (bludgeoning/piercing/slashing), and JRPG sub-types are *mechanical tags* (Slash/Strike/Pierce) — neither is *flavor substrate vocabulary* in the way fire has ember/cinder. If Reincarnated adopts 8-element treatment, the sub-element allow-list for physical needs to translate mechanical taxonomy into flavor-coherent substrate words (blunt/crush → bludgeoning; pierce/sever → piercing/slashing). That translation is a design-side curation step at PG-3.

**Preliminary recommendation to gandalf for PG-3 framing:** the empirical evidence supports 8-element treatment but the sub-vocabulary needs flavor-translation. Research does not resolve the design question of whether Reincarnated *wants* physical to behave like Grim Dawn or PoE. This is Matt's architectural-commitment call at PG-3.

---

## 7. Source Index

All research in this Phase 2 triage is derived from the 3 sampler JSONL files and their manifests. No external sources consulted in triage authoring; legolas reports what the samplers found. Source traceability is per-row in the JSONL files (`source_citations` fields).

Key sources across all 3 tracks (most frequently cited):
- Path of Exile 1+2 (ARPG; formal damage type taxonomy; ailment vocabulary)
- Diablo 4 (ARPG; class-element vocabulary)
- Lost Ark (ARPG; 6-element formal system)
- Grim Dawn (ARPG; physical sub-type question; load-bearing)
- Last Epoch (ARPG; Void damage type; shadow anchor)
- Persona 3/4/5 / SMT (JRPG; 30-year locked element vocabulary; physical sub-types)
- Final Fantasy series (JRPG; 30-year locked spell families)
- Solo Leveling (isekai manhwa; shadow vocabulary)
- Overlord (isekai LN/anime; multi-element high-tier magic)
- D&D 5e PHB + Xanathar's Guide (tabletop; formal damage types; holy/shadow/physical)
- Pathfinder 2e (tabletop; named spell vocabulary; formal traits)
- MTG color pie (tabletop; card-name player-facing vocabulary)
- Western alchemical tradition (Sulphur/Mercury/Salt; fire/water/earth unique vocabulary)
- Greco-Roman mythology (holy/shadow: umbra/shade/dawn/aether)

---

**Triage authored by:** legolas (Mode A analyzer)
**Phase 2 complete. Routing to KR for PG-1 dispatch to gandalf.**
