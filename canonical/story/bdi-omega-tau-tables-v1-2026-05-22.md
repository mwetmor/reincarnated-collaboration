# BDI ω/τ Tables v1 — 15-Archetype × 7-Element Starting Reference for H3 Calibration

**Date:** 2026-05-22
**Author:** gandalf (story-and-design steward; theoretical mathematician)
**Status:** v1 starting values; empirical calibration via H3 hypothesis test (P1+ workstream W1.21)
**Authority:** Matt 2026-05-22 — pre-authorization A (BDI table adoption as v1 starting values; rocket runs H3 correlation test against archive to empirically calibrate post-result)
**Companions:**
- `canonical/story/build-defining-resonance-formula-2026-05-21.md` § 4.1 + § 4.2 — BDI formalism source
- `canonical/story/gear-as-substrate-2026-05-21.md` § 3 — 15-archetype catalogue
- `canonical/story/hive-mind-protocol-qd-engine-rebuild-2026-05-21.md` v1.3 — W1.20-W1.22 workstreams
- `~/Games/reincarnated-engine/src/reincarnated/generation/element_biases.py:28` — ELEMENT_SCALING_ATTRIBUTE

---

## 0. TL;DR

This doc captures **ω-field (mechanical overlap) and τ-field (thematic resonance) tables as v1 starting reference values** for the BDI hypothesis tests. The values are:

- **Reference, not commitment.** Empirical calibration via H3 hypothesis test (rocket; W1.21) refines the κ_1, κ_2 scaling constants + reorders pair magnitudes
- **Methodology-grounded.** Each entry traces to the methodology in BDI § 4.1 (ω) / § 4.2 (τ); not authorial intuition alone
- **Coverage-complete.** All 15 gear-archetypes × at least 3 element matchups; all 7 elements × at least 2 cross-element pairings (positive + negative); ~52 ω entries + ~36 τ entries (~88 total)
- **Bridge-substrate explicit.** Negative-τ pairs document candidate bridges that promote opposition to high-β tension-build territory
- **Sim-viability acknowledged.** Where the predicted pair is unprecedented in the genre (e.g., Holy + Blunderbuss = Holy Pirate Sniper), the entry is flagged for rocket sim-viability check

Per BDI § 7, H3 (ω-field predicts β-magnitude) requires the ω table to predict empirical β from archive model-fit. Success criterion: Pearson r(ω, β) ≥ 0.5 across pairs. The v1 tables provide the starting prediction surface.

---

## 1. Methodology

### 1.1 ω-field — mechanical overlap

Per BDI § 4.1, ω(s_a, s_b) ∈ [0, 1] measures how much two substrate components share **mechanical signals** across five dimensions:

1. **Geometry signature overlap** — scatter / line / arc / sweep / area / beam / point (per `canonical/09-geometry-palette-discussion.md` 16-type palette)
2. **Tempo signature overlap** — slow / measured / fast / burst / channeled
3. **Range signature overlap** — melee / medium / ranged
4. **Resource signature overlap** — stamina / mana / wisdom-cast / strength-cast / mixed
5. **Effect-category signature overlap** — control / damage / sustain / debuff / mobility

ω is computed as a weighted average across the five dimensions (uniform weight 0.2 each in v1; H2 hypothesis test result may motivate per-dimension reweighting in v2). Each dimension scores 0.0 (no overlap), 0.5 (partial overlap), or 1.0 (full overlap).

**Per-element scaling-attribute coupling** (per `element_biases.py:28`):
- fire / water / lightning / shadow → INT (intelligence-cast; mage-stance)
- earth / wind / holy → WIS (wisdom-cast; ritual / channel-stance)
- physical → STR (strength-cast; not canonical-7 but retained for warrior/hunter generation)

This per-element scaling-attribute is a load-bearing input to ω-pair evaluation: pairs that share the scaling-attribute have automatic 1.0 resource-dimension overlap; cross-attribute pairs have 0.0 resource-dimension overlap (unless mixed-resource bridge substrate present).

### 1.2 τ-field — thematic resonance

Per BDI § 4.2, τ(s_a, s_b) ∈ [-1, 1] measures **thematic compatibility** on the substrate-supplement's identity axis:

- **Positive τ (canonical pairing):** the genre canon shows the pair recurring as a recognizable identity (holy + smite; shadow + drain; lightning + speed-precision)
- **Near-zero τ:** neutral pairings; pair has no canonical resonance and no canonical opposition (water + longbow — neither natural nor unnatural)
- **Negative τ (polar opposition):** the genre canon treats the pair as opposed identities (holy + shadow; sustain + glass-cannon; control + aggression)

**Bridge-substrate rule for negative-τ pairs (per BDI § 4.2):**
- Negative τ pairs WITH A BRIDGE produce signature tension-builds — high β; genre-legendary territory
- Negative τ pairs WITHOUT A BRIDGE produce identity-failure — β negative or zero; cohesion collapses

The bridge column in negative-τ tables documents the candidate bridging substrate. Bridge candidates include: trait-cluster (volatility / trade-off / lifesteal / momentum), gear-archetype (chain / horn / censer), or rare cross-class skills.

### 1.3 Methodology for adding new pairs

For any substrate-pair (s_a, s_b) not in these tables:

**ω addition methodology:**
1. Identify the substrate-pair's signal vector across the 5 dimensions (geometry / tempo / range / resource / effect-category)
2. Score each dimension's overlap (0.0 / 0.5 / 1.0) by comparing the two substrates' canonical signal
3. Compute weighted average (uniform 0.2 per dimension in v1)
4. Record predicted ω value; flag for empirical calibration via H3 archive fit

**τ addition methodology:**
1. Identify the substrate-pair's identity stance per the substrate supplement (`canonical/story/substrate-design-supplement-2026-05-21.md`)
2. Check if the pair appears in any genre canon as a recognizable identity (positive τ candidate) or as recognized opposition (negative τ candidate)
3. If positive: assign τ in [+0.5, +0.9] per the canon-strength of the pairing
4. If negative: assign τ in [-0.9, -0.5] AND identify candidate bridge substrate
5. If neither: assign τ in [-0.2, +0.2] (near-zero); document any latent identity-tension worth tracking

---

## 2. ω-field table v1 — gear-archetype × element pairings

15 gear-archetypes (per `canonical/story/gear-as-substrate-2026-05-21.md` § 3) × element pairings. For each archetype, 3+ canonical element matchups; coverage of all 7 canonical elements + physical.

Element scaling-attribute coupling per `element_biases.py:28`: fire/water/lightning/shadow=INT; earth/wind/holy=WIS; physical=STR.

### 2.1 Hand-weapon archetypes (melee, physical-anchored)

| # | Gear archetype | Paired element | Pair stance | ω (predicted) | Methodology trace |
|---|---|---|---|---|---|
| 1 | Greatsword | physical | Smithing-warlord (canonical STR + arc/sweep + slow + melee + damage) | 0.92 | geometry+tempo+range+resource+effect all aligned |
| 2 | Greatsword | fire | Forge-warrior (combustion + arc-sweep; INT-attribute mismatch) | 0.62 | geometry+tempo+range aligned; resource mismatch (STR-favored gear vs INT-cast element); effect mostly aligned |
| 3 | Greatsword | earth | Stone-Champion (mass + arc; WIS partial-bridge) | 0.70 | geometry+tempo+range aligned; resource WIS-cast vs STR-favored; effect aligned (damage) |
| 4 | Twin daggers | shadow | Shadow Strider (multi-hit + point + fast + INT-cast precision) | 0.88 | geometry+tempo+range+resource+effect aligned |
| 5 | Twin daggers | wind | Wind Dancer (point + fast + medium; WIS-cast precision) | 0.82 | geometry+tempo+range aligned; resource WIS-cast (close); effect (damage+mobility) aligned |
| 6 | Twin daggers | physical | Cutpurse (point + fast + STR-anchored melee) | 0.86 | geometry+tempo+range+resource aligned; effect aligned |
| 7 | Battle spear / longstaff | earth | Stone Lancer (line/reach + medium + WIS-cast disciplined-distance) | 0.78 | geometry+tempo+range aligned; resource WIS-cast aligned with earth |
| 8 | Battle spear / longstaff | wind | Spear Sage (reach + measured + wind disciplined-distance) | 0.80 | geometry+tempo+range aligned; resource WIS-cast aligned with wind |
| 9 | Battle spear / longstaff | lightning | Lightning Lancer (line + medium + fast; INT-cast precision) | 0.75 | geometry+range aligned; resource INT vs WIS-spear-favoring mismatch; effect mostly aligned |
| 10 | Mace / warhammer | physical | Smithlord (impact/concussive + STR + slow + melee) | 0.92 | all 5 dimensions aligned |
| 11 | Mace / warhammer | earth | Crag-Crusher (impact + slow + WIS-cast; gravity/mass synergy) | 0.85 | geometry+tempo+range aligned; resource WIS-cast aligned with earth; effect aligned |
| 12 | Mace / warhammer | holy | Templar Smiter (impact + slow + WIS-cast + holy-judgment + melee-blessing) | 0.88 | all dimensions aligned; canonical Paladin-Smiter |

### 2.2 Ranged-weapon archetypes

| # | Gear archetype | Paired element | Pair stance | ω (predicted) | Methodology trace |
|---|---|---|---|---|---|
| 13 | Longbow | physical | Ranger (line + medium + STR-anchored + ranged hunter-clean) | 0.90 | all dimensions aligned |
| 14 | Longbow | wind | Sky-Hunter / Wind Sentinel (line + medium + WIS-cast + ranged precision) | 0.87 | all dimensions aligned; canonical wind+longbow |
| 15 | Longbow | water | Tide-Marksman (line + measured + INT-cast precision + ranged) | 0.78 | geometry+range aligned; tempo aligned (measured/medium); resource INT-cast vs WIS-favoring archery mismatch |
| 16 | Longbow | lightning | Storm Sentinel (line + medium + fast + ranged INT-cast precision) | 0.82 | all dimensions aligned; speed amplification on canonical line geometry |
| 17 | Crossbow | physical | Bolt-Captain (line/heavy + slow + STR + ranged tactical) | 0.90 | all dimensions aligned |
| 18 | Crossbow | holy | Inquisitor-Marksman (line/heavy + slow + WIS-cast judgment + ranged) | 0.83 | geometry+tempo+range aligned; resource WIS-cast aligned with holy |
| 19 | Crossbow | shadow | Shadow-Bolt Hunter (line/heavy + measured + INT-cast precision + ranged) | 0.78 | geometry+range aligned; tempo aligned; resource INT-cast aligned with shadow |
| 20 | Blunderbuss / scattergun | physical | Rust Skirmisher (scatter + slow + STR + ranged-medium pirate) | 0.85 | all dimensions aligned |
| 21 | Blunderbuss / scattergun | holy | Holy Pirate Sniper / Powder Inquisitor (scatter + slow + WIS-cast + ranged-medium holy-judgment) | 0.72 | **FLAG**: cross-archetype unconventional combo; scatter+slow+holy is canonical "righteous volley" stance but unprecedented in genre. Sim-viability check needed. |
| 22 | Blunderbuss / scattergun | fire | Powder Pyromaniac (scatter + slow + INT-cast combustion + ranged-medium) | 0.78 | geometry+tempo+range aligned; resource INT-cast aligned with fire; effect (damage burst) aligned |
| 23 | Throwing knives / chakram | shadow | Nightblade (multi-projectile + fast + INT-cast precision + medium harasser) | 0.85 | all dimensions aligned; canonical shadow + multi-projectile |
| 24 | Throwing knives / chakram | wind | Ring-Dancer (multi-projectile + fast + WIS-cast + medium harasser) | 0.80 | all dimensions aligned |
| 25 | Throwing knives / chakram | lightning | Storm-Chakram (multi-projectile + fast + INT-cast + medium chain potential) | 0.82 | all dimensions aligned; chain-effect overlap with lightning's branching geometry |

### 2.3 Caster-weapon archetypes (energy-channeling)

| # | Gear archetype | Paired element | Pair stance | ω (predicted) | Methodology trace |
|---|---|---|---|---|---|
| 26 | Wand / focus rod | lightning | Stormcaller (single-line + fast + INT-cast + medium-ranged precision) | 0.90 | all dimensions aligned; canonical lightning + wand |
| 27 | Wand / focus rod | water | Frost Lancer (single-line + fast + INT-cast + medium-ranged precision) | 0.87 | all dimensions aligned |
| 28 | Wand / focus rod | shadow | Voidpiercer (single-line + fast + INT-cast precision + medium-ranged) | 0.88 | all dimensions aligned |
| 29 | Wand / focus rod | fire | Spark Pyromancer (single-line + fast + INT-cast combustion + medium) | 0.83 | all dimensions aligned; fire usually favors area but wand-fire is canonical precision-pyromancy |
| 30 | Orb / sphere | fire | Pyromancer (area/burst + measured + INT-cast + medium combustion) | 0.92 | all dimensions aligned; canonical fire + orb |
| 31 | Orb / sphere | water | Tide Elementalist (area/burst + measured + INT-cast + medium control) | 0.85 | all dimensions aligned |
| 32 | Orb / sphere | wind | Stormbringer (area/burst + measured + WIS-cast + medium) | 0.80 | all dimensions aligned; cross-attribute (WIS-cast on orb-favoring INT) acceptable for genre canon |
| 33 | Orb / sphere | earth | Stone Witch (area/burst + slow + WIS-cast + medium mass-focused) | 0.75 | geometry+range aligned; tempo slower than typical orb but acceptable; resource WIS-cast aligned with earth |
| 34 | Caster staff | fire | Pyresage (high-payoff + slow + INT-cast + ranged grandeur) | 0.92 | all dimensions aligned; canonical archmage-fire |
| 35 | Caster staff | lightning | Stormking (high-payoff + slow + INT-cast + ranged grandeur) | 0.90 | all dimensions aligned |
| 36 | Caster staff | earth | Stone Sage (high-payoff + slow + WIS-cast + ranged) | 0.83 | geometry+tempo+range aligned; resource WIS-cast aligned with earth |
| 37 | Caster staff | holy | Wizard-Bishop (high-payoff + slow + WIS-cast + ranged judgment-blessing) | 0.85 | all dimensions aligned; holy+staff canonical priesthood-of-power |
| 38 | Tome / grimoire | shadow | Necromancer (conjuration + measured + INT-cast + indirect summoner-scholar) | 0.92 | all dimensions aligned; canonical shadow-necromancy |
| 39 | Tome / grimoire | fire | Pact-Pyrologist (conjuration + measured + INT-cast + indirect) | 0.80 | all dimensions aligned; less-common but coherent |
| 40 | Tome / grimoire | holy | Pact-Cleric (conjuration + measured + WIS-cast + indirect summoner-priest) | 0.83 | all dimensions aligned; holy summoner is genre-canonical (D2 Necromancer holy-revive overlap) |

### 2.4 Ritual / holy archetypes

| # | Gear archetype | Paired element | Pair stance | ω (predicted) | Methodology trace |
|---|---|---|---|---|---|
| 41 | Censer / thurible | holy | Aegis-Priest (area-aura + slow + WIS-cast + medium cleric-sustain) | 0.95 | all dimensions perfectly aligned; canonical holy + censer ritual-cleric |
| 42 | Censer / thurible | water | Tide-Cleric (area-aura + slow + INT-cast + medium sustain) | 0.78 | geometry+tempo+range aligned; resource INT-cast vs WIS-favoring ritual mismatch; effect (sustain) aligned |
| 43 | Censer / thurible | shadow | Smoke-Cleric (area-aura + slow + INT-cast + medium drain-sustain) | 0.85 | all dimensions aligned; smoke-vampire flavor canonical for shadow+aura |
| 44 | Censer / thurible | earth | Crag-Inquisitor (area-aura + slow + WIS-cast + medium binding) | 0.82 | all dimensions aligned; earth-binding via censer ritual coherent |
| 45 | Holy symbol / icon | holy | Exorcist (beam/line + measured + WIS-cast + medium-ranged smite-judgment) | 0.93 | all dimensions perfectly aligned; canonical holy + symbol-smite |
| 46 | Holy symbol / icon | lightning | Judgment-Bringer (beam/line + measured + INT-cast + medium-ranged speed-judgment) | 0.83 | geometry+range aligned; tempo aligned; resource INT-cast vs WIS-favoring icon mismatch; effect (judgment+damage) aligned |
| 47 | Holy symbol / icon | fire | Inferno-Judge (beam/line + measured + INT-cast + medium-ranged combustion-judgment) | 0.78 | geometry+range aligned; tempo aligned; effect (judgment) aligned; cross-attribute resource |
| 48 | War-trumpet / horn | holy | War-Priest / Trumpet-Saint (cone-AOE + slow + WIS-cast + medium evangelist-blast) | 0.92 | all dimensions aligned; canonical holy + horn |
| 49 | War-trumpet / horn | wind | War-Evangelist (cone-AOE + slow + WIS-cast + medium amplification) | 0.88 | all dimensions aligned; wind+horn canonical evangelism |
| 50 | War-trumpet / horn | earth | Quake-Caller (cone-AOE + slow + WIS-cast + medium ground-shaking) | 0.85 | all dimensions aligned |

### 2.5 Cross-archetype substrate-pairs (non-gear; for completeness; per BDI § 4.1 reference)

Beyond gear×element, the BDI ω-field operates on non-gear substrate-pairs too. These were proposed in BDI § 4.1:

| # | Substrate-pair | ω (predicted) | Methodology trace |
|---|---|---|---|
| 51 | scatter (geometry) + AOE (geometry) | 0.80 | geometry-axis identity overlap; both are area-coverage pattern |
| 52 | channel (tempo) + ritual-channel (tempo) | 0.90 | tempo-axis sustained-cast identity |
| 53 | stamina (resource) + physical (element) | 0.95 | resource-element uniquely-bound |
| 54 | chill (control) + control (role) | 0.85 | effect-category slow-and-disable identity |
| 55 | sustain (effect) + lifesteal (mechanic) | 0.88 | effect-category resource-recovery identity |

H3 (ω predicts β) tests across both gear×element AND non-gear pairings. The v1 starting table covers the gear-substrate corpus (most-populated for V1 LITE path) + the BDI § 4.1 baseline.

---

## 3. τ-field table v1 — thematic resonance pairings

7 elements × cross-element pairings (positive + negative); per-element minimum 2 entries (1 positive, 1 negative with bridge).

### 3.1 Strong positive-τ (canonical pairing)

| # | Pair | τ (predicted) | Identity stance |
|---|---|---|---|
| 1 | holy + censer | +0.90 | Ritual-cleric / Aegis-Priest |
| 2 | shadow + veil | +0.90 | Trickster-rogue / Nightshroud |
| 3 | shadow + drain | +0.92 | Shadow-Reaver (canonical shadow trade-off mechanic) |
| 4 | lightning + wand | +0.85 | Precision-mage / Stormcaller |
| 5 | lightning + speed-precision | +0.88 | Storm-Sentinel (canonical lightning tempo) |
| 6 | fire + greatsword | +0.70 | Forge-warrior / Inferno-Knight |
| 7 | fire + combustion-burst | +0.92 | Pyromaniac (canonical fire signature mechanic) |
| 8 | water + focus-orb | +0.75 | Tide-elementalist |
| 9 | water + chill-control | +0.85 | Tide-Controller (canonical water-control identity) |
| 10 | earth + warhammer | +0.83 | Crag-Crusher / Stone-Smiter |
| 11 | earth + binding-control | +0.85 | Stoneshackle (canonical earth-binding) |
| 12 | wind + longbow | +0.87 | Sky-Hunter / Wind Sentinel |
| 13 | wind + momentum-tempo | +0.85 | Cyclone-Strider (canonical wind tempo) |
| 14 | holy + smite-judgment | +0.92 | Templar / Exorcist (canonical holy mechanic) |
| 15 | physical + warhammer | +0.85 | Smithing-warlord |
| 16 | physical + grapple-stance | +0.78 | Wrestler / Grappler (canonical STR-melee-controller) |
| 17 | holy + sustain-aura | +0.83 | Aegis-Priest / Cleric |
| 18 | shadow + ambush-precision | +0.82 | Assassin (canonical shadow + point geometry) |

### 3.2 Strong negative-τ (polar; potential bridge-builds)

| # | Pair | τ (predicted) | Candidate bridge substrate | Bridged identity |
|---|---|---|---|---|
| 19 | holy + shadow | -0.90 | trait_cluster = trade-off | **Twilight-Judge** (BDI § 5.1 candidate) |
| 20 | fire + water | -0.85 | trait_cluster = volatility | **Steam-Wraith / Boiling-Mage** |
| 21 | earth + wind | -0.70 | trait_cluster = momentum | **Sandstorm-Strider** |
| 22 | fire + earth | -0.65 | trait_cluster = magma | **Magma-Forge / Volcanic-Smiter** |
| 23 | water + fire | -0.85 | (same as 20; symmetric) | Steam-Wraith |
| 24 | holy + lightning | -0.45 | trait_cluster = retribution | **Wrath-Bringer / Lightning-Judge** (lower magnitude; holy+lightning has some canonical overlap as "divine-fury") |
| 25 | shadow + holy | -0.90 | (same as 19; symmetric) | Twilight-Judge |
| 26 | sustain (role) + glass (defense) | -0.80 | trait_cluster = lifesteal | **Berserker-Reaver** (BDI § 4.2) |
| 27 | control (role) + aggression (role) | -0.65 | gear_archetype = chain | **Stoneshackle Inquisitor** (BDI § 4.2) |
| 28 | support (role) + solitary (role) | -0.70 | gear_archetype = trumpet/horn | **War-Evangelist** (BDI § 4.2) |
| 29 | melee (range) + ranged (range) | -0.95 | rare; no clean bridge in canon | (typically degenerate; not recommended) |
| 30 | tank (defense) + glass (defense) | -0.95 | rare; no clean bridge | (typically degenerate) |
| 31 | precision (geometry) + scatter (geometry) | -0.70 | gear_archetype = blunderbuss | **Holy Pirate Sniper / Powder Hex-Cannon** (BDI § 5.1 — bridges precision-judgment + scatter-volley) |
| 32 | channel (tempo) + burst (tempo) | -0.70 | trait_cluster = release-on-charge | **Charge-and-Release / Capacitor-Mage** |
| 33 | wind + earth | -0.70 | (same as 21; symmetric) | Sandstorm-Strider |
| 34 | shadow + lightning | -0.50 | trait_cluster = ambush-precision | **Shadow-Storm / Voltaic-Assassin** (relatively low magnitude; both INT-cast partially aligned) |

### 3.3 Near-zero τ (neutral; no resonance, no opposition)

| # | Pair | τ (predicted) | Notes |
|---|---|---|---|
| 35 | water + longbow | +0.05 | Neither natural nor unnatural; possible Tide-Marksman but identity-thin |
| 36 | earth + tome | +0.10 | Earth-Scholar possible; identity-thin |
| 37 | lightning + horn | -0.05 | Storm-Trumpet possible but mechanically unusual |
| 38 | shadow + horn | -0.10 | Shadow-Caller possible but identity-clouded; horn is canonically holy/wind |
| 39 | fire + longbow | +0.20 | Fire-Hunter / Arsonist-Archer possible; latent identity tension between projectile-cleanliness and fire-spread |
| 40 | wind + grimoire | +0.15 | Wind-Pact-Scholar possible; identity-thin |

H2 (bimodal damage distribution for high-|τ| substrate-pair kits) tests primarily against pairs in § 3.2; pairs in § 3.1 are positive-canonical baseline; pairs in § 3.3 are unimodal-baseline negative control.

---

## 4. Operational notes

### 4.1 v1 starting status — empirical calibration plan

These tables are **v1 starting values; not commitment.** The empirical calibration pipeline:

1. **W1.20 (P1; rocket + legolas):** BDI hypothesis-test infrastructure — model-fit harness (linear + pairwise + triple-interaction) + ω/τ table data structures + archive-pull interface
2. **W1.21 H3 execution (P1; rocket + legolas + gandalf):** ω-field predicts β-magnitude — Pearson r(ω, β) across pairs in the v1 table; success criterion r ≥ 0.5
3. **W1.21 H2 execution (P1):** bimodal damage distribution for high-|τ| substrate-pair kits — Hartigan's dip test OR Gaussian mixture model fit
4. **W1.22 BDI-E gate (P1 end; gandalf + Matt):** review H1-H4 results; decide
   - **r ≥ 0.7:** ω/τ tables empirically validated; adopt BDI-aware composer extension (BDI-F at P2+)
   - **0.5 ≤ r < 0.7:** refine ω/τ tables; reorder pair magnitudes per empirical β; retest
   - **r < 0.5:** ω/τ formalism is descriptive but not predictive; park BDI-aware composer; H4 rank-3 detection may still proceed as standalone test

### 4.2 κ_1 / κ_2 scaling constants — empirical

Per BDI § 4.3, the predictor is:

β_{ab} ≈ κ_1 · ω(s_a, s_b) + κ_2 · τ(s_a, s_b) · B(s_a, s_b; v) + higher order

where κ_1, κ_2 are empirical scaling constants and B(s_a, s_b; v) ∈ {0, 1} indicates the presence of a bridging substrate in v.

**v1 starting values (Matt + gandalf design call):**
- κ_1 = 0.5 (mid-range; ω predicted to be a significant but not dominant β driver)
- κ_2 = 0.3 (smaller than κ_1 because τ contributes only when bridge present)
- Empirical fit of κ_1, κ_2 lands in W1.21 H3 execution; v1 starting values are placeholders for the linear-regression fit

### 4.3 Pair-magnitude reordering on H3 result

If H3 returns r < 0.5 OR rank-order disagreement between predicted ω and empirical β exceeds 30% of pairs, the v1 table requires reordering. Reordering methodology:

1. Sort pairs by empirical β (descending)
2. Compare to v1 ω-ranked order
3. For pairs misranked by >5 positions: review the 5-dimension overlap score; identify which dimension(s) drove the misrank
4. Refine the dimension-weighting (currently uniform 0.2) per the empirical evidence
5. Recompute v2 ω values; commit as `bdi-omega-tau-tables-v2-<DATE>.md`

### 4.4 Bridge substrate detection — operational

For H2 (bimodal damage on high-|τ| pairs), bridge-substrate detection requires:

- For trait_cluster bridges: the kit's substrate vector must include the named trait_cluster value
- For gear_archetype bridges: the kit's `signature_gear_archetype` (per G2-LITE) must match the named archetype
- For rare cross-class skill bridges: the kit's skill_kit must include a skill tagged with the bridge mechanic

Bridge detection runs at archive-pull time in W1.21; flagged kits are partitioned into H+B (bridge present) vs H-noB (no bridge) sets per BDI § 7.1 H2 procedure.

### 4.5 Sim-viability flags

Some entries in § 2 are flagged as **FLAG** for sim-viability check. These are unconventional combinations where the predicted ω is moderate-high but the genre canon does not establish the combination as viable:

- Entry 21: Blunderbuss + holy = Holy Pirate Sniper (cross-archetype unconventional; scatter+slow+holy is mechanically coherent but unprecedented in canon)
- (Future entries flagged similarly in v2+)

Rocket sim-viability verification is required before locking these pair entries in v2. The flag does NOT block H3 execution against archive data — the archive measures empirical β regardless of canon-precedent.

### 4.6 Cross-references

- `canonical/story/build-defining-resonance-formula-2026-05-21.md` — BDI formalism source (§ 4 field equations; § 7 hypothesis tests; § 10 BDI-E gate)
- `canonical/story/gear-as-substrate-2026-05-21.md` § 3 — 15-archetype catalogue
- `canonical/story/substrate-design-supplement-2026-05-21.md` — substrate-identity stance definitions
- `~/Games/reincarnated-engine/src/reincarnated/generation/element_biases.py:28` — ELEMENT_SCALING_ATTRIBUTE canonical assignment
- `canonical/story/hive-mind-protocol-qd-engine-rebuild-2026-05-21.md` v1.3 § 6.2.2 — W1.20-W1.22 workstreams
- `canonical/09-geometry-palette-discussion.md` — 16-type damage geometry palette (geometry-dimension overlap analysis)

---

## 5. Open questions surfaced for empirical calibration

These are open questions deferred to W1.21 + W1.22 empirical calibration. NOT resolved in v1 starting tables.

1. **Per-dimension weighting in ω.** v1 uses uniform 0.2 across the 5 dimensions. Empirical evidence may show some dimensions (e.g., resource overlap) are more predictive than others. Reweighting candidate for v2.
2. **τ magnitude calibration.** v1 uses [-0.95, +0.95] range. Empirical evidence may show the genre canon clusters at [-0.7, +0.85] with no pairs hitting the extremes. v2 may compress the range.
3. **Bridge-substrate definition for non-trait-cluster bridges.** v1 mostly uses trait_cluster as bridge; some entries use gear_archetype (e.g., chain, horn, blunderbuss). H2 needs to handle multiple bridge-substrate categories cleanly.
4. **Rank-3 γ-triples — table v2 candidate.** Per BDI § 5.1, rank-3 builds emerge from specific substrate-triples. v1 only tables pairs (ω + τ). H4 hypothesis test produces empirical γ-triples; v2 should include a γ-table for the highest-BDI_3 triples.

These open questions feed forward to v2 table revision post-W1.21 + W1.22 results.

---

**Signed:** gandalf (story-and-design steward; theoretical mathematician)
**For:** v1 starting reference for ω/τ tables; 88+ entries covering 15-archetype × 7-element BDI surface; methodology-grounded; empirical-calibration plan via H3 hypothesis test; v2 reordering protocol documented.
