# Session 4 — Kit Identity + Generation Spec

**STATUS:** DRAFT — Matt-authorized 2026-06-12 (Pattern B session, architecture cascade); mostly independent; can start at any time; rocket-primary
**Author:** gandalf
**Date:** 2026-06-12
**Grounding docs:**
- `canonical/story/2026-05-31-hypothesis-flow-pattern-library-architecture.md` — PRIMARY (§ 4.18, 4.19, 4.20, 4.21, 4.22, 4.23, 4.24)
- `agentic_orchestration/gandalf/notes/2026-06-12-session-1-t4-architecture-spec.md` — T4 catalog (ELEMENT strategies require kit architecture awareness)
- `agentic_orchestration/gandalf/notes/2026-06-12-session-2-proxy-companion-architecture-spec.md` — faction taxonomy (§ 7)
- `agentic_orchestration/gandalf/notes/2026-06-12-vestigial-ontology-discipline-candidate.md` — vestigial-ontology discipline (archetype = NAME-ONLY; no kernel branching)

**Produces:**
1. Kit architecture generation spec (single vs hybrid; skill composition rules) — rocket seam
2. Vestigial-class label taxonomy + substrate-derived assignment function — rocket seam
3. Coupling-architecture (Layer 1.5) rules per kit type — rocket seam
4. Cultural lineage + historical period + register as generation directives + faction alignment — rocket seam
5. Investment profile gear scaling rules — gamora + rocket seam

**Blocks:** Kit identity uniqueness guarantee; faction assignment completeness for companion system

> **NORMALIZATION PASS (gandalf, 2026-06-12, Matt-authorized):** axis bin vocabulary re-pointed to the locked definitions in `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` § 3. Conventions: (1) vestigial-label assignment (§ 2) consumes MEASURED BC bins (it fires on the finalized, BC-measured kit — measurement-time vocabulary applies); (2) generation directives (§ 1, § 4, § 5) bind to structural properties or PREDICTED bins; (3) energy types (mana/rage/focus/charge-stack) are declared `energy_type` values, not Axis 5 bins; (4) "sustain"/"evasion"/"glass_cannon" are not Axis 4 bins — the locked bins are tank/mitigator/dodger/glass; (5) "burst/sustained tempo" is not Axis 3A — front-loadedness lives in the proposed `front_load_profile` metric (Session 3 § 5.1) and spikiness in locked Axis 3B (flat/variable/spiky). Q10 (faction coverage gap for mesoamerican / sub-Saharan / south-SE-Asian lineages, § 4.2 vs Session 2 § 7.2) is flagged in Session 2. Delta summary: `gandalf/notes/2026-06-12-normalization-pass-delta-summary.md`.

---

## 0. Design mandate

Kit identity uniqueness is the guarantee that the 400+ in-band survivors are maximally distinct from each other's FELT EXPERIENCE — not just statistically distinct in BC axis space. Session 4 formalizes the generation rules that make each kit feel like a distinct character build: its elemental coherence, its rotation coupling depth, its cultural identity, and its gear trajectory. These are the substrate properties that players use to explain their kit to other players.

**Vestigial-ontology constraint (applies throughout):** archetype labels and class identity labels are NAME-ONLY assignments. They are derived AFTER kit generation from substrate observations — NOT used as pre-generation constraints. We do not generate "a mage." We generate a kit from substrate axes and then observe "this kit exhibits mage-like properties." Archetype fields carry zero behavioral weight in any kernel or generation branching path.

---

## 1. Kit architecture — single vs hybrid 2-element

### 1.1 Architecture types

| Architecture | Definition | T4 strategy alignment |
|---|---|---|
| **Single-element** | All skills in all chains use the same primary element | ELEMENT_CONVERSION_MONO eligible |
| **Hybrid 2-element** | Kit has a primary element and a sub-element; skills distributed across both | ELEMENT_CONVERSION_HYBRID eligible; ELEMENTAL_ECHO eligible |
| **Physical hybrid** | Kit has at least 1 physical-damage skill + at least 1 elemental skill | ELEMENT_CONVERSION_PHYSICAL eligible |

### 1.2 Element ratio rules (hybrid kits)

For hybrid 2-element kits:
- `primary_element_ratio`: 0.60–0.70 of all skills in the kit use the primary element (3-4 of 5 skills at standard chain count; 4-5 of 6 skills at expanded chain count)
- `sub_element_ratio`: remaining skills use the sub-element
- The sub-element is drawn from a compatibility pool per primary element (not all element pairings are equally viable; see § 1.3)
- Sub-element skills cluster in 1 dedicated chain (preferred for cognitive coherence) OR distribute 1-per-chain (for synergy-across-chains builds)

For physical hybrid kits:
- At least 1 skill must have `damage_type = physical` in its Layer 2 properties
- Physical skills can be any geometry type; they gain the ailment-trigger bonus from ELEMENT_CONVERSION_PHYSICAL
- `physical_ratio`: 0.30–0.50 of skills are physical; remainder are elemental

### 1.3 Sub-element compatibility matrix (hybrid 2-element kits)

Not all element pairings are mechanically or thematically coherent. Rocket uses this compatibility table for sub-element assignment:

| Primary element | Compatible sub-elements | Incompatible sub-elements |
|---|---|---|
| fire | earth, lightning, shadow | ice (thematic opposition; allowed as "edge case" pool) |
| water / ice | wind, earth, shadow | fire (thematic opposition; if paired, must be "conflict" framing) |
| earth | fire, water, lightning, physical | — (earth is highly compatible) |
| wind | lightning, water, shadow | earth |
| lightning | fire, wind, physical | water (conductor interaction reserved for terrain_reactive) |
| shadow | holy, wind, earth | — (shadow pairs widely; narratively any pairing works) |
| holy | shadow, fire, earth | — |
| physical | fire, lightning, wind, earth | shadow, holy (physical-shadow / physical-holy reserved for specific lore framing) |

"Incompatible" sub-elements can appear in a kit only via a Matt-explicit thematic override (e.g., ice + fire "conflict" kit framing for a specific faction). Default generation excludes incompatible pairs.

### 1.4 Skill composition rules (rocket generation directive)

Within a chain (2-4 skills per chain depending on chain count):
1. **Opener position** (first skill use in chain): direct-hit delivery skill (any rich geometry; immediate damage on use/hit); no stacking-DoT skill (Layer 2 `stackability ∈ {stacking_capped_N, stacking_refreshing_N}` with DoT mechanics) as opener — DoT openers feel weak
2. **Body positions** (middle skills): any geometry; stacking-DoT skills preferred here if kit has DoT
3. **Closer position** (last skill in chain, if chain has ≥3 skills): highest-magnitude single hit OR CC skill (the payoff of the chain)

Cross-chain rules:
- At most 1 CC skill per chain (concentrated CC; avoids CC-spam per-chain feel)
- If kit's predicted control share ≥ 0.60 (predicted Axis 2B = control-pure, per Session 3 § 4.3), CC skills are distributed 1 per chain
- A kit must have at least 1 AoE skill in the full kit (no single-target-only kits except by explicit proxy-delegation: a proxy is handling all AoE; player is single-target)

---

## 2. Vestigial-class identity — label taxonomy + assignment function

### 2.1 Design principle

Vestigial-class labels are substrate-derived observations, not pre-generated types. The assignment function takes a finalized kit's BC axis values, dominant element, dominant geometry, energy_type, and T4 strategy family and returns a label string.

Labels are used:
- In player-facing UX (loadout, demo surfaces) — as a quick character-class communication tool
- In star-lord telemetry output — as NAME-ONLY freight (never branched on)
- NOT in fight_engine, damage_resolver, or any kernel path

### 2.2 Label taxonomy (18 labels)

Labels are organized in two tiers: primary identity (dominant read) and secondary modifier (optional flavor append).

**Primary identity labels:**

*(Signatures use MEASURED BC bins — locked vocabulary: Axis 1 close/mid/ranged × fast/slow; Axis 2 single-target/small-AOE/large-AOE/chain/multi-spawn; Axis 2B damage-pure/mixed/control-pure; Axis 3B flat/variable/spiky; Axis 4 tank/mitigator/dodger/glass — plus structural properties: declared `energy_type`, element, T4 strategy, Layer 2 fields.)*

| Label | Dominant substrate signature |
|---|---|
| **Striker** | Axis 1 ∈ {close-fast, close-slow} + front-loaded `front_load_profile` + Axis 2 = single-target + Axis 4 ∈ {tank, glass} (defensive extreme either way) |
| **Ravager** | Axis 1 close + front-loaded + `energy_type` = rage + Axis 4 = glass |
| **Ranger** | Axis 1 ∈ {ranged-fast, ranged-slow} + Axis 2 = single-target + Axis 3B = flat + `energy_type` ≠ rage |
| **Arcanist** | Axis 1 mid/ranged + Axis 2 ∈ {small-AOE, large-AOE} + `energy_type` = mana + scaling_pattern=player_level primary |
| **Warden** | Axis 2B ∈ {mixed, control-pure} + Axis 3B = flat + Axis 4 = mitigator |
| **Berserker** | Axis 1 close + Axis 3B = spiky + `energy_type` = rage + front-loaded |
| **Sentinel** | Axis 4 ∈ {mitigator, tank} + Axis 2 = single-target + Axis 2B = damage-pure + any Axis 1 |
| **Phantom** | Axis 4 = dodger + Axis 2 = single-target + Axis 1 mid + shadow element primary |
| **Invoker** | proxy-dominant (≥1 proxy-family T4 strategy) + Axis 1 mid + Axis 3B = flat |
| **Templar** | holy element + `energy_type` = mana + Axis 4 = mitigator + CC ≥ 1 skill |
| **Reaver** | hybrid 2-element + decay/escalating magnitude_pattern + Axis 1 mid |
| **Conduit** | resource_generation focus (Resource Conduit proxy OR focus/mana + resource_gen skills) |
| **Shadowcaller** | shadow element + Axis 2 AOE bins + Axis 2B ∈ {mixed, control-pure} + shadow binding category eligible |
| **Windrunner** | wind element + Axis 1 mid + Axis 4 = dodger + Axis 3B = spiky |
| **Earthshaper** | earth element + ≥1 skill with `terrain_reactive` tag + Axis 2B ∈ {mixed, control-pure} |
| **Stormbringer** | lightning element + Axis 2 ∈ {small-AOE, large-AOE} OR ≥1 `beam_channel` rich-geometry skill + front-loaded |
| **Pact-holder** | COMPANION_CONTRACT or MONSTER_PACT T4 as primary strategy |
| **Threshold** | charge-stack `energy_type` + TEMPORAL_CHARGE or CHARGED_THRESHOLD_PROXY T4 |

**Secondary modifier (appended if applicable):**

| Modifier | Condition |
|---|---|
| `Twin` | Hybrid 2-element kit architecture |
| `Sovereign` | PROXY_SOVEREIGNTY T4 strategy |
| `Undying` | SACRIFICE_ASCENDANCY T4 strategy |
| `Resonant` | RESONANCE_LOOP T4 strategy |
| `Cascading` | MOMENTUM_CASCADE T4 strategy |
| `Fissured` | PROXY_FISSION T4 strategy |

Example composed labels: "Invoker Sovereign" (proxy-dominant + PROXY_SOVEREIGNTY), "Warden Resonant" (CC + RESONANCE_LOOP), "Ravager Undying" (rage + SACRIFICE_ASCENDANCY).

### 2.3 Assignment function (rocket seam)

Assignment priority (apply first match wins):
1. If T4 strategy family = PROXY → `Invoker` (overrides range/other checks; proxy is the defining identity)
2. If T4 strategy = COMPANION_CONTRACT or MONSTER_PACT → `Pact-holder`
3. If `energy_type` = charge-stack AND T4 ∈ {TEMPORAL_CHARGE, RESOURCE_CONVERSION} → `Threshold`
4. If element = shadow AND Axis 2B ∈ {mixed, control-pure} → `Shadowcaller`
5. If element = holy AND Axis 4 = mitigator → `Templar`
6. If element = earth AND `terrain_reactive`-tagged skill present → `Earthshaper`
7. If element = wind AND Axis 4 = dodger → `Windrunner`
8. If element = lightning AND Axis 2 ∈ {small-AOE, large-AOE} → `Stormbringer`
9. If Axis 4 = dodger AND Axis 2 = single-target AND element = shadow → `Phantom`
10. If Axis 1 close AND `energy_type` = rage AND front-loaded → `Ravager` else if Axis 1 close AND front-loaded → `Striker`
11. If Axis 2B ∈ {mixed, control-pure} AND Axis 4 = mitigator → `Warden`
12. If Axis 1 ranged AND Axis 2 = single-target AND Axis 3B = flat → `Ranger`
13. If Axis 2 ∈ {small-AOE, large-AOE} AND `energy_type` = mana → `Arcanist`
14. If Axis 4 ∈ {mitigator, tank} AND Axis 2B = damage-pure → `Sentinel`
15. If hybrid 2-element AND decay/escalating magnitude → `Reaver`
16. Default: `Arcanist` (covers uncategorized caster archetypes)

*(Rule order note: rule 9 (Phantom) is unreachable after rules 4 — shadow + control bins — only for shadow kits that are damage-pure; the ordering stands but rocket should verify reachability per label at implementation, per the vestigial-ontology discipline: labels that never fire are substrate evidence, not bugs.)*

After primary label: check secondary modifier conditions; append if matching.

---

## 3. Coupling-architecture (Layer 1.5) — coupling depth rules

### 3.1 What coupling depth measures

Coupling depth is the maximum number of "prior skill uses" a skill's optimal use depends on, within the same chain. It is Layer 1.5 — the bridge between kit macro-architecture and skill micro-mechanics.

| Coupling depth | Meaning | Player experience |
|---|---|---|
| 1 | Skills are independent; any order is valid | Free rotation; low planning overhead |
| 2 | At least 1 skill gains bonus from the immediately preceding skill | Opener → payoff; natural 2-step rhythm |
| 3 | At least 1 skill gains bonus from a 2-skill sequence (A → B → C) | Meaningful chain feel; 3-step rotations |
| 4+ | Multi-step chains; 4 or more skills in optimal sequence | High complexity; rewarding for skilled players; dangerous in solo context without proxy aid |

### 3.2 Max coupling depth rules per kit type

| Kit type / T4 family | Max coupling depth | Rationale |
|---|---|---|
| Proxy-family T4 (PROXY_*) | 2 | Proxy handles additional complexity; player needs free rotation |
| RESONANCE_LOOP T4 | 4 | Resonance is inherently a 3-step sequence (A, B, 3rd use); this is the design intent |
| MOMENTUM_CASCADE T4 | 3 | Momentum builds on any hit; some coupling to trigger Cascade efficiently |
| ELEMENTAL_ECHO T4 | 2 | Echo auto-fires; player rotation can be relatively free |
| TEMPORAL_CHARGE T4 | 3 | Hold-to-charge creates implicit coupling (charge → release at max → reset) |
| COMPANION_CONTRACT / MONSTER_PACT T4 | 3 | Companion handles some of the complexity |
| ELEMENT_CONVERSION_* T4 | 2 | Element conversion is a passive amplifier; rotation stays free |
| DEFENSIVE_TRADEOFF T4 | 2 | Mana management is the complexity; rotation stays relatively free |
| SACRIFICE_ASCENDANCY T4 | 3 | HP-management creates coupling (watch HP → activate at right moment) |
| NETWORK_AMPLIFIER T4 | 3 | CC-then-damage rhythm is inherent coupling |
| GEOMETRY_INVERSION / GEOMETRY_COLLAPSE T4 | 2 | Geometry switch is a single decision point |
| DUAL_PROXY T4 | 2 | Two proxies already add complexity; player stays at depth 2 |
| Monster season kits | 1 | Monster companions are proxies; monster kit itself should be simple to use |
| NPC/Mercenary season kits | 2 | NPC companions support the player; kit can have mild coupling |

### 3.3 Coupling depth implementation (rocket seam)

Coupling depth is expressed at skill level via the `prerequisite_skill` field on a skill: a reference to the skill_id that should precede this skill for optimal use. Coupling depth = max chain of prerequisite links in the kit.

Rocket enforces max coupling depth per kit type at generation time: if a generated skill tree exceeds the max depth for the kit's T4 family, the deepest prerequisite link is removed (making that skill independent).

`coupling_depth: int` stored in kit record; used in cognitive_load_score calculation (contributes to `sequence_depth` factor).

---

## 4. Cultural lineage, historical period, register — generation directives

### 4.1 The three dimensions

| Dimension | Rocket field | Function |
|---|---|---|
| `cultural_lineage` | `kit.cultural_lineage` | Primary cultural origin of the kit's aesthetic and thematic identity |
| `historical_period` | `kit.historical_period` | Time period this kit evokes |
| `register` | `kit.register` | Narrative tone / genre lens applied to lineage + period |

These three fields together produce the faction tag (Session 2 § 7.3) and inform:
- D1 element name pool selection (register-gated; see D1 element naming)
- Weapon type family selection (lineage-weighted)
- Skill naming conventions (period + register influence naming vocabulary)
- Companion pool gating (faction from these three fields)

### 4.2 Cultural lineage catalog

| lineage_tag | Description |
|---|---|
| `western_european_germanic` | Germanic, Frankish, Arthurian tradition |
| `western_european_gothic` | Gothic, Slavic, dark-fae tradition |
| `norse_germanic_celtic` | Norse, Germanic, Celtic / Gaelic tradition |
| `greek_roman` | Greco-Roman / Mycenaean / Minoan |
| `middle_eastern_persian` | Islamic Golden Age, Persian, Mesopotamian |
| `north_african_egyptian` | Egyptian, Nile Valley traditions |
| `east_asian_chinese` | Chinese imperial tradition |
| `east_asian_japanese` | Japanese shogunate, samurai, yokai tradition |
| `east_asian_korean` | Korean (Joseon, Goryeo), Korean mythological |
| `south_southeast_asian` | Indian / Southeast Asian (Sanskrit, Vedic, Thai, Balinese) |
| `mesoamerican` | Aztec, Maya, Olmec traditions |
| `sub_saharan_african` | West African, Bantu, East African traditions |
| `pan_industrial` | Cross-cultural industrial (steampunk; no primary lineage) |
| `void_liminal` | Cosmically displaced; no clear cultural lineage; void or interstitial |

### 4.3 Historical period catalog

| period_tag | Approximate CE range | Notes |
|---|---|---|
| `ancient` | Pre-500 CE | |
| `medieval` | 500–1400 CE | |
| `early_modern` | 1400–1800 CE | Renaissance, exploration era |
| `industrial` | 1800–1920 CE | Steam, early electrical |
| `contemporary` | 1920–2020 CE | Modern; rare in fantasy ARPG |
| `mythic` | Timeless / before history | Gods, creation myths, primordial events |
| `void_atemporal` | No time period; void-touching | |

### 4.4 Register catalog

| register_tag | Description | Element affinities |
|---|---|---|
| `high_fantasy` | Epic, bright, heroic; Tolkien-inflected | holy, earth, wind |
| `dark_fantasy` | Grim, morally complex; grit and horror elements | shadow, fire, earth |
| `mythological` | Divine, legendary, epic-mythic | holy, fire, lightning |
| `grimdark` | Brutal, hopeless, unforgiving; Warhammer-inflected | shadow, fire, physical |
| `steampunk` | Industrial-magical; gears + arcane energy | lightning, fire, physical |
| `arcane_modern` | Magic in a recognizable modern context | any element |
| `cosmic_horror` | Lovecraftian; incomprehensible scale; void | shadow, void (if added) |
| `primal_shamanic` | Pre-civilizational; nature spirits; totemic | earth, wind, water, lightning |
| `void_arcane` | Void-touched magic; reality-bending | shadow, holy, void |

### 4.5 Generation directive — weighted sampling

At kit generation:
1. **cultural_lineage** sampling: uniform across lineage catalog unless BC axis priors skew it. NPC/Mercenary season uses same lineage weights as the player season pool being served.
2. **historical_period** sampling: weighted by cultural_lineage (affinity table below). Sampled after lineage is determined.
3. **register** sampling: weighted by (element × engagement_profile × Axis 4 defensive_profile). Table below.

**Lineage → historical period affinity weights (excerpt; rocket implements full table):**

| lineage_tag | ancient | medieval | early_modern | industrial | mythic | void_atemporal |
|---|---|---|---|---|---|---|
| `western_european_germanic` | 0.5 | 2.0 | 1.5 | 0.5 | 0.5 | 0.1 |
| `norse_germanic_celtic` | 0.5 | 2.5 | 0.5 | 0.2 | 1.5 | 0.2 |
| `greek_roman` | 2.5 | 0.5 | 0.5 | 0.1 | 2.0 | 0.1 |
| `east_asian_japanese` | 0.5 | 2.5 | 1.5 | 0.5 | 1.0 | 0.1 |
| `pan_industrial` | 0.0 | 0.0 | 0.5 | 3.0 | 0.0 | 0.3 |
| `void_liminal` | 0.1 | 0.1 | 0.1 | 0.1 | 0.5 | 3.0 |

**Element + Axis 4 → register affinity weights (excerpt):**

| element | Axis 4 / property condition (locked vocabulary; PREDICTED bins at generation time) | high_fantasy | dark_fantasy | mythological | grimdark | primal_shamanic | cosmic_horror |
|---|---|---|---|---|---|---|---|
| shadow | any | 0.5 | 2.0 | 0.5 | 2.5 | 0.3 | 1.5 |
| holy | predicted Axis 4 = mitigator | 2.5 | 0.3 | 2.5 | 0.1 | 0.5 | 0.2 |
| earth | any | 1.5 | 0.8 | 1.0 | 0.8 | 2.5 | 0.1 |
| fire | predicted Axis 4 = glass | 1.5 | 1.5 | 1.5 | 2.0 | 1.0 | 0.3 |
| lightning | predicted Axis 3B = spiky | 1.5 | 1.0 | 2.0 | 1.0 | 1.5 | 0.3 |
| any | void_liminal lineage | 0.1 | 0.5 | 0.5 | 0.5 | 0.1 | 2.5 |

### 4.6 Faction derivation (lookup; references Session 2 § 7.2)

After (lineage, period, register) sampling, faction is derived by lookup:

```
faction = FACTION_LOOKUP_TABLE[(lineage, period, register)]
```

If exact (lineage, period, register) tuple is not in the table: apply nearest-match rule (register has highest match weight → lineage → period). `void_liminal` lineage or `cosmic_horror`/`void_arcane` register → faction = "Void Covenant" (override).

**Rocket implementation note:** FACTION_LOOKUP_TABLE is a data file (not hardcoded); rocket loads it at generation time. Elrond maintains the table as a data steward item when faction assignments need addition or revision.

---

## 5. Investment profile — gear scaling rules

### 5.1 Definition

Investment profile describes how much a kit's effective combat power scales with gear tier. It is the "Diablo 2 rune word" dynamic — some kits are made by their best-in-slot gear; others perform well regardless.

| Profile | T4 vs T1 gear power ratio | Player experience |
|---|---|---|
| **High investment** | ≥ 2.5× | Best-in-slot gear is transformative; low-tier gear feels weak; rune word / convergence item is crucial |
| **Scaling investment** | 1.5× – 2.5× | Gear improves the kit steadily; soft-cap curve; most kits land here |
| **Low investment** | < 1.5× | Kit is relatively self-contained; gear is additive, not multiplicative; accessible to under-geared players |

### 5.2 Assignment rules

Investment profile is assigned at kit finalization based on BC axis values and T4 strategy:

| Condition (locked vocabulary; measured bins — investment profile assigns at kit finalization post-BC-measurement) | Investment profile |
|---|---|
| Axis 4 = glass | HIGH — glass cannon lives by gear optimization |
| Axis 3B = spiky AND TEMPORAL_CHARGE T4 | HIGH — burst peak depends on gear amplifying the charge burst |
| Proxy-primary kit (Invoker label, proxy-family T4) | LOW for player gear; HIGH for proxy gear (separate gear slot if companion) |
| COMPANION_CONTRACT or MONSTER_PACT T4 | SCALING — convergence item is the high-investment slot; player gear scales normally |
| RESONANCE_LOOP T4 | HIGH — Resonance requires precise timing; gear reducing cooldowns amplifies the experience |
| DEFENSIVE_TRADEOFF T4 (mana shield) | HIGH — mana pool size is gear-derived; investment = mana gear |
| Axis 4 ∈ {mitigator, tank} | SCALING |
| NPC/Mercenary season kits | SCALING (companion kits are gear-able by the player; the gear slot IS the investment) |
| Monster season kits | LOW (monsters are stat-based; no gear slots; flat stat progression) |
| Default | SCALING |

### 5.3 Rocket generation directive

`investment_profile: str` ("high" | "scaling" | "low") stored in kit record. Rocket assigns per table above; tie-break on first-match precedence.

**Gamora implication:** high-investment kits may exhibit higher fight-outcome variance in low-gear simulation states. If gamora simulates kit performance at multiple gear tiers (Session 5 validation), investment_profile is the discriminating variable. Session 5 spec should include a gear-tier variation test for high-investment kits.

---

## 6. Faction-kit assignment — completeness verification

### 6.1 Guarantee

After Session 4 generation rules are implemented, rocket must verify that:
- All 8 factions have ≥ 10 player kit representatives in the in-band 400-kit corpus
- All 8 factions have ≥ 20 NPC/Mercenary kit representatives per faction in the 800-NPC corpus
- All 6 binding categories have ≥ 40 monster kit representatives per category in the 600-monster corpus
- No faction has > 30% of the in-band 400-kit corpus (avoids faction dominance)

If any faction has < 10 representatives: the lineage+period+register sampling weights for that faction are adjusted until the floor is met. This is a generation balancing pass, not a QD optimization step.

### 6.2 Faction-assignment verification output (rocket seam)

After generation + QD pipeline:
1. Count kit faction distribution
2. Log faction counts in a generation summary artifact (`phase7_season_summary.json` extension or separate faction report)
3. If any faction < 10 in-band kits: flag to gandalf/knight-rider for weight adjustment
4. If any faction > 30% of in-band kits: flag to gandalf/knight-rider for weight reduction

---

## 7. Session 4 open questions

| # | Question | Priority |
|---|---|---|
| 1 | Sub-element compatibility matrix: are the incompatible pairs truly incompatible, or are edge-case builds (fire + ice "conflict" framing) desirable for player expression? | MEDIUM — Matt design call |
| 2 | Investment profile: is the gear simulation multi-tier testing in scope for Session 5 validation? Or is investment profile stored but validation deferred? | HIGH — affects Session 5 scope |
| 3 | Cultural lineage catalog: does the current 14-lineage set cover the content desired for Cycle 15+ seasons? Any planned lineages missing? | MEDIUM — Matt expansion check |
| 4 | Faction-kit completeness floor: is 10 in-band kits per faction the right minimum? Too low may mean some factions feel underpopulated. 15-20 may be a better floor. | LOW — numbers calibration |
| 5 | Coupling depth: do the T4-family-based max coupling depth rules need additional per-element constraints? (e.g., DoT-heavy earth kits might naturally generate deep coupling independent of T4) | MEDIUM — generation testing will reveal |
| 6 | Register sampling: is `cosmic_horror` a common enough register in normal seasons, or should it be restricted to Void Covenant faction kits only? | MEDIUM — thematic gating question |
| 7 | Vestigial-class label: does "Pact-holder" for both COMPANION_CONTRACT and MONSTER_PACT obscure the distinction? Should there be separate labels ("Pact-holder" vs "Beast-binder")? | LOW — label design preference |

---

**Author:** gandalf, 2026-06-12. Matt-authorized Session 4 spec from Pattern B session. Independent of Sessions 1-3; can begin at any time; rocket-primary.
