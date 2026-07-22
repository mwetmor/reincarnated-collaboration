# Tier-3 Encounter-Grammar Spec — three-tier (MACRO / MESO / MICRO)

**ARTIFACT A of W1.** The run's law for encounter geometry. Buildable-against; the fit layer (W2) reads it as math, the emission pipeline (KR Lane-1) reads its schema twin (`…-w1-encounter-schema-draft.json`) as the payload of the reserved `encounters` bundle key.

**Author:** named-`gandalf` sub-agent (SPEC-AUTHOR) · 2026-07-22
**Run:** Tier-3 Encounter-Geometry Run · Wave W1 · conductor gandalf `RUN-CONDUCTOR`
**Charter:** `agentic_orchestration/gandalf/notes/2026-07-22-tier3-encounter-geometry-run-charter.md` (§4 W1 row · §5 · §7 T3-V1..V7)
**Run state / ledger:** `…-run-state.md` (rulings L-8 · L-9 — the Gate-2 obligations this spec satisfies)
**Substrate (FROZEN, read-only):** THE CENSUS `agentic_orchestration/elrond/notes/2026-07-22-tier3-w0-census-substrate-freeze.md` + four harvest files md5-stamped (`9b41f22c…` I · `f3ae9f6e…` II · `b255680354…` III · `0dcae6ad…` IV).
**Emission-congruence target:** `canonical/current-to-end-state/current-to-end-state-serial-content-emission.md` + the on-disk `one_realm_demo_bundle.json` (verified bundle shape, this session).

---

> ## ⚠ WORKING-LABEL CAVEAT (charter §5 · T3-V2 · census §h.8) — READ BEFORE ANYTHING ELSE
>
> **Every FAMILY name in this spec and its schema twin is a WORKING LABEL, not canon.** WHIRLWIND, CHANNELED-BEAM, AURA, TOTEM-SENTRY, TRAP-MINE, MELEE-STRIKE, DOT-AILMENT, MULTI-PROJECTILE-VOLLEY, SHAPESHIFT, CHAIN-BOUNCE, DASH-STRIKER, MINION-PET, IDENTITY-GAUGE — all provisional. Matt's names-review is a pending commitment-boundary beat (§5). **Nothing here is served as canon.** The schema carries the same caveat in its `$comment`. When these become canon, a rename pass sweeps both artifacts; the schema treats family as a string token precisely so the rename is a value-swap, never a structure change.

---

## §0 — What this spec is, in one breath

Matt ruled it (grill sheet R-b1/R-b2/R-b3, 2026-07-22): **enemies are the menu of future selves.** Kits and factions per run group by BUILD-FAMILY. Beat an enemy kit → become it → at least one faction of that family is guaranteed kin in the next act; every other family is hostile. The world reads what you ARE. This spec gives that fantasy its **encounter geometry** at three scales:

- **MACRO** — the map-area archetype a run deals per act, per era. What the camera frames when you enter a zone. Carries a DISPOSITION parameter (hostile / kin) and reserves one traveling-kin encampment slot per act.
- **MESO** — the formation a pack stands in. How bodies arrange in space when combat starts.
- **MICRO** — the pressure-verb a family exerts. What the pack DOES to you, inherited from the family kit-leader's mechanism (R-b2).

The three tiers are **not independent**: MESO formations and MICRO verbs DERIVE from the family table (R-b2 — "the three-tier grammar gets its vocabulary from the family table"). MACRO decks are dealt from each act's own family deck, era-honest (Appendix-B presence).

The genre lineage is not decoration. Age I is Diablo II's physical-brawl world (Travincal, Chaos Sanctuary). Age II is Path of Exile 1's attrition-and-emplacement world (totem nests, trap fields, DoT clouds — and its famous melee deficit, a hole we honor). Age III is Grim Dawn's sustained-fight world (Aetherial channel-beams down city streets). Age IV is the hybrid-frontier world (PoE2 + Last Epoch — every family present, none dominant). **The eras have personalities because the families genuinely lived and died by era.** That is the whole design.

---

## §1 — Coordinate system + provenance discipline (the spine everything hangs on)

### §1.1 — The address of any encounter element

Per census §c join-key discipline, every element is uniquely addressable and every derived element joins the census cleanly:

```
(era ∈ {I, II, III, IV},  family ∈ <13 working labels>,  provenance ∈ {GENRE-ATTESTED, RDR-NATIVE-DERIVED},  tier ∈ {MACRO, MESO, MICRO})
```

**Provenance is a TAG column, never encoded into row identity** (census §c; Discipline #14 spirit: tag, don't encode). A GENRE-ATTESTED formation and an RDR-NATIVE-DERIVED formation for the same (era, family) cell sit in the same list, distinguished by their `provenance` value alone. The 80 harvest rows are all GENRE-ATTESTED; the 5 templates §5 authors are all RDR-NATIVE-DERIVED. Nothing else.

### §1.2 — Q38 coordinates (the encounter side speaks the kit side's language)

Per charter §7 (Q38 inherited): **element-courts k=5 · eras = shelves · biome-morph rider.** Where an encounter element carries an element or court hook, it speaks these coordinates — the encounter side and the kit side share one address space so `fit(kit, encounter | era)` can compute in W2. Concretely: a MICRO verb that deals fire (DOT-AILMENT fire-stack) tags `court`/`element` in the same vocabulary the kit substrate uses; era is already the shelf via the `era` field. The **biome-morph rider** means a family's surface presentation (its faction dressing, its ground-hazard flavor) may re-skin by biome without changing its mechanism — spec'd at MESO as `biome_morph_slot` (v1 = reserved; the emission `floor_manifest.dominant_element` is its consumption hook).

### §1.3 — Act-order agnosticism (charter §1 parked fork — DO NOT resolve)

Whether a run descends chronologically (I→IV), reverse-chronologically (IV→I, archaeology-of-the-genre), or player-chooses act order is a STORY call, PARKED. **This spec builds ORDER-AGNOSTIC decks.** Every per-era deck is self-contained: it names its own family roster, its own archetypes, its own kin slot. No deck references "the previous act" or "the next act" by content — only the kin-guarantee loop (R-b3) crosses act boundaries, and it crosses by FAMILY IDENTITY (a data key), not by act ordinal. A whirlwind kin caravan is expressible whether Age II follows Age I or Age IV. The schema carries `act_ordinal` as an OPTIONAL positioning hint, never a structural dependency.

---

## §2 — MACRO tier: per-era map-area decks

### §2.1 — What a MACRO archetype is

A **map-area archetype** is the framed shape of a zone: its terrain personality, its faction-camp structure, its disposition (hostile / kin), and the family roster it deals from. It is what the run instantiates when it enters an act. Per T3-F1 / grill R-b3, MACRO ships PARAMETERIZED (the gate binds MESO/MICRO in sim; MACRO is dealt, not sim-certified) — so the MACRO deck is a **deal-table**, and its archetypes are slots a run fills from the era's present families.

**Every archetype carries a `disposition` parameter** (charter §4): `hostile` (the default — the menu of future selves you must fight through) or `kin` (the reserved traveling-kin slot, §2.3). The disposition dimension is Matt's R-b3 ruling made spatial: a kin-outpost and a hostile-outpost are the same terrain archetype with opposite faction intent toward the player-form.

### §2.2 — Era-personality honesty (the deck differs by act because the families did)

Per census §b + Appendix-B readings, each era's HOSTILE deck deals only from families **present** in that era (Appendix-B holes respected — no fabricated members). The archetype *forms* are era-personality-honest:

- **Ages I + III are melee-native** → BRAWL-form archetypes headline (centralized multi-faction melee — the Travincal / Chaos Sanctuary / Cronley's-Hideout lineage). Census reading 3: "the centralized multi-faction melee area is Age I/III native."
- **Age II is emplacement-native** → OUTPOST / EMPLACEMENT-form archetypes headline (totem nests, trap fields, DoT clouds — decentralized faction-outpost warfare). Census reading 3: "the de-centralized faction outpost area is Age II native."
- **Age IV is full-spectrum** → the hybrid frontier deals brawl AND outpost AND channel-arena forms; highest residual (58% unclaimed — census §b coverage), so its deck is the widest.

### §2.3 — The TRAVELING-KIN ENCAMPMENT SLOT (T3-F5 · T3-V4 · T3-V5 — Matt: "traveling kin is right")

**One reserved kin slot per act.** Mechanism (Matt's ruling, grill sheet R-b3 + T3-F5 option (a)): when you become a family, ≥1 faction of that family is guaranteed kin in the next act. Because the kin faction TRAVELS with the player (D2 Warriv/Meshif caravan lineage), **the kin slot is EXEMPT from era-nativity** (T3-V4). A whirlwind caravan can be camped in the trap-age; the anachronism IS the story.

Rules the slot obeys:

1. **The kin slot is exempt from era-nativity (T3-V4).** It may present ANY family, regardless of whether that family is native to the current era's HOSTILE deck. The whirlwind caravan in Age II (PoE1, where WHIRLWIND is a monster-side hole) is not a contradiction — it is the traveling caravan.
2. **HOSTILE decks stay era-pure (T3-V4).** The kin guarantee NEVER bends the act's native hostile family deck. Appendix-B holes remain load-bearing genre history for hostiles. The kin slot is the ONLY era-nativity exemption in the entire grammar.
3. **Kin = non-hostile + interactive (R-b3).** A kin archetype is `disposition: kin`, `hostile: false`, and carries parameterized interaction hooks: `shop_hooks` and `boon_hooks` (v1 = presence + hook surface only). Its faction relationship to the player-form is `kin` (the emission `factions.relationships[].type` vocabulary, §6.3).
4. **Interaction scope v1 = encampment surface ONLY (T3-V5).** Shop/boon hooks are parameterized slots, not filled NPC dialogue. **The full traveling-kin caravan NPC ensemble is DEFERRED to the story fold** — SCENEWRIGHT/STORYWRIGHT work, out of W0–W4 scope (this is the same deferral L-4 logs for the guest-family edge). The schema exposes the hooks; the caravan's characters are not this run's job.
5. **The kin slot is filled by the RUN, from the become-history (R-b3), not by the deck.** The MACRO deck RESERVES the slot and specifies its interaction surface; WHICH family fills it is a run-time function of what the player became (RD-1's job, §7). The deck's kin-slot entry is therefore a template with `family: <run-supplied>`, disposition `kin`, era-exemption flagged.

### §2.4 — The four per-era MACRO decks (COMPLETE)

Each deck lists **≥4 map-area archetypes** (charter §4). Archetype forms drawn from the harvest Faction-Camp Structure column, era-personality-honest per §2.2. `family roster` = the families the archetype may deal hostiles from (present-in-era only). The kin slot is the exempt 5th entry in every deck.

Legend: `[BRAWL]` centralized-melee-convergence · `[OUTPOST]` decentralized faction-camp · `[NEST]` spawner/environmental-anchor · `[CHANNEL-ARENA]` beam/emplacement kill-zone · `[PATROL]` mobile line/wedge · `[WAVE-ARENA]` scripted sequential faction presentation · `[KIN]` traveling-kin encampment (exempt).

#### Deck I — Age I · Diablo II (the physical-brawl act)

Signature family: MELEE-STRIKE (census reading 1). Present families (census §b): WHIRLWIND, AURA, TOTEM-SENTRY, TRAP-MINE, MELEE-STRIKE, DOT-AILMENT, MULTI-PROJECTILE-VOLLEY, CHAIN-BOUNCE + (RDR-derived) SHAPESHIFT-I, DASH-STRIKER-I. Holes: CHANNELED-BEAM, MINION-PET, IDENTITY-GAUGE.

| # | Archetype | Form | Hostile family roster (present-in-era) | Harvest anchor | Disposition |
|---|---|---|---|---|---|
| I-A | **Open-plains warband** | `[PATROL]` | MELEE-STRIKE · DOT-AILMENT | rows #1 #2 #10 (Fallen/Goatman clan patrols) | hostile |
| I-B | **Enclosed nest-crypt** | `[NEST]` | MELEE-STRIKE · TRAP-MINE · MULTI-PROJECTILE-VOLLEY | rows #3 #4 #9 (Zombie/Skeleton/Maggot nests) | hostile |
| I-C | **Emplaced lane-sanctuary** | `[CHANNEL-ARENA]` | TOTEM-SENTRY · MULTI-PROJECTILE-VOLLEY · AURA | row #11 (Arcane Sanctuary Spires + Specters) | hostile |
| I-D | **Centralized boss-brawl courtyard** | `[BRAWL]` | WHIRLWIND · AURA · TOTEM-SENTRY · DOT-AILMENT | rows #14 #17 (Travincal / Chaos Sanctuary — THE Age-I signature) | hostile |
| I-E | **Scripted wave-throne** | `[WAVE-ARENA]` | CHAIN-BOUNCE · MELEE-STRIKE · DOT-AILMENT · TOTEM-SENTRY | row #19 (Throne of Destruction five-wave) | hostile |
| **I-KIN** | **Traveling-kin encampment** | `[KIN]` | *(run-supplied family; era-exempt)* | D2 Rogue Encampment / caravan lineage | **kin** |

#### Deck II — Age II · Path of Exile 1 (the attrition-and-emplacement act)

Signature family: DOT-AILMENT (15 — census reading 1, "the attrition act"). Present families: CHANNELED-BEAM, AURA, TOTEM-SENTRY, TRAP-MINE, DOT-AILMENT, MULTI-PROJECTILE-VOLLEY, CHAIN-BOUNCE + (RDR-derived) WHIRLWIND-II. **Load-bearing holes (DO NOT deal hostiles from these): MELEE-STRIKE (the famous PoE1 melee deficit, 0/36), SHAPESHIFT, MINION-PET, IDENTITY-GAUGE.**

| # | Archetype | Form | Hostile family roster (present-in-era) | Harvest anchor | Disposition |
|---|---|---|---|---|---|
| II-A | **Fire-camp totem outpost** | `[OUTPOST]` | TOTEM-SENTRY · MULTI-PROJECTILE-VOLLEY | rows #3 #15 (Cannibal fire-camp / Goatman shaman) | hostile |
| II-B | **Necromancer emplacement-hall** | `[CHANNEL-ARENA]` | TOTEM-SENTRY · CHANNELED-BEAM | rows #4 #14 #7 (Necromancer corpse-loop / Arcmage lane) | hostile |
| II-C | **Trap-seeded corridor** | `[NEST]` | TRAP-MINE · DOT-AILMENT | rows #10 #12 #17 (Brittle Corsair / Evangelist / Hellion) | hostile |
| II-D | **Bandit-faction outpost** | `[OUTPOST]` | AURA · MULTI-PROJECTILE-VOLLEY · CHANNELED-BEAM | rows #6 #16 #9 (bandit camp / Exile patrol / Lunar Devotees) | hostile |
| II-E | **Chaos-DoT plaza + arc-tomb** | `[BRAWL]`-attrition | DOT-AILMENT · CHAIN-BOUNCE | rows #18 #11 #19 (Chaos Zealots / Voidbearers / Arc skeletons) | hostile |
| **II-KIN** | **Traveling-kin encampment** | `[KIN]` | *(run-supplied family; era-exempt — e.g. a WHIRLWIND caravan camped in the trap-age)* | Warriv/Meshif caravan lineage | **kin** |

> Note: Age II has NO native BRAWL headline (the melee hole). Its centralized-pressure archetype (II-E) is an ATTRITION-brawl — bodies converge into a DoT field, not a melee sweep. This is the era-personality result made honest: PoE1 never made melee-brawl work, so its "central fight" is a standing-in-poison fight.

#### Deck III — Age III · Grim Dawn (the sustained-fight act)

Signature family: CHANNELED-BEAM (its home shelf, 6 rows — census reading 1). Present families: WHIRLWIND, CHANNELED-BEAM, TOTEM-SENTRY, TRAP-MINE, MELEE-STRIKE, DOT-AILMENT, CHAIN-BOUNCE, DASH-STRIKER + (RDR-derived) SHAPESHIFT-III. **Load-bearing holes: AURA (true genre hole for Age III), MULTI-PROJECTILE-VOLLEY (Gunman fire is single-shot not fan-volley), MINION-PET, IDENTITY-GAUGE.**

| # | Archetype | Form | Hostile family roster (present-in-era) | Harvest anchor | Disposition |
|---|---|---|---|---|---|
| III-A | **Aetherial-warband street** | `[PATROL]` | MELEE-STRIKE · CHANNELED-BEAM | rows #1 #3 (possessed infantry + rear channel) | hostile |
| III-B | **Channel-beam city-node** | `[CHANNEL-ARENA]` | CHANNELED-BEAM · DOT-AILMENT | rows #9 #16 #10 (Dominator / Archmage Aether Ray — Age-III signature) | hostile |
| III-C | **Bandit-gang hideout** | `[BRAWL]` | MELEE-STRIKE · DASH-STRIKER | rows #7 #8 (Cronley's Gang — the Age-III melee-native brawl) | hostile |
| III-D | **Beast-pack waste / nest-grove** | `[PATROL]` / `[NEST]` | MELEE-STRIKE · TRAP-MINE | rows #13 #14 (Manticore patrol / Blood Grove nest) | hostile |
| III-E | **Chthonian cult stronghold** | `[BRAWL]`-ritual | DOT-AILMENT · TOTEM-SENTRY · TRAP-MINE · CHAIN-BOUNCE | rows #11 #12 #15 #18 (Bloodsworn cult / raise-chain / void rifts) | hostile |
| **III-KIN** | **Traveling-kin encampment** | `[KIN]` | *(run-supplied family; era-exempt)* | Devil's Crossing safe-hold lineage | **kin** |

#### Deck IV — Age IV · PoE2 + Last Epoch (the hybrid-frontier act)

No single dominant family; highest residual (census reading 1, "the hybrid frontier act"). ALL ten families present (census §b): WHIRLWIND, CHANNELED-BEAM, AURA, TOTEM-SENTRY, TRAP-MINE, DOT-AILMENT, MULTI-PROJECTILE-VOLLEY, MELEE-STRIKE, SHAPESHIFT (monster-side present here — row #11 Geonor), CHAIN-BOUNCE (thin — RDR-derived). Holes: MINION-PET, IDENTITY-GAUGE (off-spine). **MEDIUM-confidence tag on all 9 LE rows (1.0-era; Season-3 overhauls not reflected — §8).**

| # | Archetype | Form | Hostile family roster (present-in-era) | Harvest anchor | Disposition |
|---|---|---|---|---|---|
| IV-A | **Open hunting-ground pack** | `[PATROL]` | WHIRLWIND · MELEE-STRIKE | rows #1 #4 #10 (Rotten Pack / Hyenic Raiders / Kin beetles) | hostile |
| IV-B | **Ritual-altar mine-field** | `[NEST]` | TRAP-MINE · TOTEM-SENTRY | rows #3 #5 #15 (Ominous Altars / Faridun / Void ritual) | hostile |
| IV-C | **Emplacement-outpost (volcanic/wraith)** | `[OUTPOST]` | TOTEM-SENTRY · MULTI-PROJECTILE-VOLLEY | rows #12 #18 #7 (Volcanic Golems / Wraith Caller / tentacle nest) | hostile |
| IV-D | **Cross-fire channel-arena** | `[CHANNEL-ARENA]` | CHANNELED-BEAM · AURA · DOT-AILMENT | rows #9 #19 #21 (Vaal Overseer / Void Beam / Nagasan tribe) | hostile |
| IV-E | **Shapeshift boss-arena** | `[BRAWL]`-transform | SHAPESHIFT · MULTI-PROJECTILE-VOLLEY · WHIRLWIND | rows #11 #22 #2 (Count Geonor human→wolf / Lagon / Candlemass) | hostile |
| IV-F | **Void-convergence field** | `[PATROL]`-isolation-break | DOT-AILMENT · (UNMAPPED-reserved: U-7 convergence) | rows #14 #16 (Void Horror / Imperial Watcher three-body) | hostile |
| **IV-KIN** | **Traveling-kin encampment** | `[KIN]` | *(run-supplied family; era-exempt)* | PoE2/LE settlement-hub lineage | **kin** |

---

## §3 — MESO tier: formations

### §3.1 — What a MESO formation is

A **formation** is the spatial arrangement a pack stands in when combat starts, and the geometric pressure that arrangement creates. Per R-b2, formations DERIVE from the family mechanism (a whirlwind pack's formation is a converging spin-body; a totem pack's is an emplaced-anchor + mobile-screen). The harvest **Formation** column is the source (charter §4). Formations bind to the emission `monsters[]` fields `aggro_radius_m`, `leash_distance_m`, `preferred_behavior`, `skill_rotation_priority`, and the pack's spatial spread (schema §6.4).

### §3.2 — Requirement + the census density caveats

**≥2 formations per family-present cell** (charter §4). "Family-present cell" = a (family, era) cell the census §b matrix marks covered (`✓N`, `THIN`, or RDR-served). Formations are sourced from the harvest Formation column for GENRE-ATTESTED cells; for the 5 RDR-derived cells (§5) the formations derive from the kit-leader mechanism.

Census §h density caveats the SPEC-AUTHOR must honor:
- **Age-III Manticore #13/#14 are ONE creature, two MESO variants** (patrol-line vs nest-defense — census §h.6). They are NOT two independent family exemplars. Deck III-D deals both as patrol/nest variants of the same beast.
- **Age-I TOTEM-SENTRY rests on a 2-row multi-family base** (#11 #14 — census §h.7). Both rows are multi-family; if either re-scopes, three cells thin. The formations for TOTEM-I are drawn from these two, flagged fragile.
- **DOT-AILMENT-II is present-but-lightly-sampled** (f-6: 3 rows vs 15 kit-mass — Age II's SIGNATURE attrition family). Its MESO derivation MAY lean on kit-side mass to reach formation richness — noted as a density-permitted derivation lean, not a fabrication (the formations still trace to attested rows #11 #13 #18; kit-mass informs *variant count*, not new content).

### §3.3 — The formation catalogue (per family, ≥2 each, era-tagged)

Each entry: `formation_id` · geometry · the pressure it creates · era(s) present · harvest anchor(s) / RDR-derivation. Secondary co-mappings (census §b legend) are legitimate formation-TEXTURE inputs, flagged `secondary`.

**WHIRLWIND** (spin-and-close):
- `ww_converge_spin` — pack forms a rotating encirclement body that pins-and-closes on the player point. Present: IV (rows #1 #10 Rotten Pack / Kin beetles). GENRE-ATTESTED.
- `ww_arc_sweep` — single large body delivers wide melee arc covering surrounding space (boss-tier). Present: I (row #17 Diablo pentagram spin) · III (row #6 Alkamos Blade Arc, confidence MEDIUM per harvest). GENRE-ATTESTED.
- `ww_derived_frenzy_line` — RDR-derived for Age II (see §5.5): an aura-driven frenzy line that behaves as a spin-body without a native PoE1 spin-mob. RDR-NATIVE-DERIVED.

**CHANNELED-BEAM** (channel-lanes):
- `cb_lane_hold` — caster channels a directed beam down a lane; melee screen holds the player in the beam's effective zone. Present: II (rows #7 #20 Arcmage / Gravicius) · III (rows #9 #16 Dominator / Archmage) · IV (row #9 Vaal Overseer channels from height). GENRE-ATTESTED.
- `cb_crossfire` — paired casters at opposite ends channel tracking beams; cross-fire geometry forces constant repositioning. Present: IV (row #19 Void Beam Summoner pair). GENRE-ATTESTED. Secondary: III (row #17 Valdaran teleport-resets beam-angle).
- *(Hole: CHANNELED-BEAM absent Age I — no formation dealt; the D2 Inferno career hole, load-bearing.)*

**AURA** (aura-enable-and-pressure):
- `aura_carrier_pack` — a hidden aura-carrier anchor buffs the whole pack (damage/speed/resist-strip); player must identify-and-kill the carrier first. Present: I (row #18 Aura-Enchanted Champions) · II (rows #6 #16 bandit leader / Exile mod) · IV (rows #13 #16 Tukohama shaman / Imperial Watcher). GENRE-ATTESTED.
- `aura_matron_center` — a central aura-anchor (damage-reduction) makes a triangle of ranged threats survivable; break the anchor to break the field. Present: IV (row #21 Nagasan Diamond Matron). GENRE-ATTESTED. Secondary: I (row #15 Mephisto Holy Freeze radiating slow-field).
- *(Hole: AURA absent Age III — true genre hole per census §b; GD's "Supporter" archetype is unratified, admission A-III.4. No formation dealt.)*

**TOTEM-SENTRY** (emplace-and-hold):
- `ts_anchor_screen` — a stationary emplacement (totem/spire/summoner/caller) holds position and generates a sustained threat while a mobile screen prevents the player reaching it; the anchor must be prioritized. Present: I (row #11 Lightning Spires — fragile 2-row base) · II (rows #3 #4 #14 fire-totem / Necromancer loop) · III (row #11 Bloodsworn summoner) · IV (rows #5 #7 #17 #18 #20 — the Age-IV signature; Faridun/tentacle/Bone Sculptor/Wraith Caller/Wengari). GENRE-ATTESTED.
- `ts_resurrection_loop` — emplace-and-hold VIA resurrection: a stationary raiser continuously raises battlefield dead as a self-replenishing melee screen (the cross-era resurrection-leader — U-2/U-6 candidate MICRO-verb, §5.6). Present: II (rows #4 #14 Necromancer) · IV (row #17 Bone Sculptor). GENRE-ATTESTED. **Candidate cross-era link:** the D2 Fallen/Fetish Shaman (U-2) and GD Aetherial Dominator (U-6) resurrection-leader role — spec'd as ONE candidate verb spanning I+III, flagged CANDIDATE / NOT-A-FAMILY / docket-input (§5.6). Do NOT canonize.
- `ts_environmental_nest` — the emplacement is TERRAIN (egg sac / ceiling anchor / spawner-entity), not a placed unit; triggers a simultaneous spawn burst on approach. Present: II (row #5 spider nest — currently UNMAPPED U-5) · IV (row #7 tentacle nest). GENRE-ATTESTED, flagged secondary/candidate (U-5's environmental-vs-placed distinction is a parked ruling, §4).

**TRAP-MINE** (pre-seed):
- `tm_preseed_corridor` — hazards (death-explosions / corpse-fields / fire-patches) pre-seed a corridor so it becomes a sequential detonation field as the player advances. Present: I (rows #13 #20 Stygian Doll / Nihlathak Corpse Explosion) · II (rows #10 #12 #17 Brittle Corsair / Evangelist / Hellion). GENRE-ATTESTED.
- `tm_ritual_minefield` — altars / rifts / ritual-chests are placed mine-nodes that spawn waves or hazard-clouds on trigger; the field forces serial engagement. Present: II (row #12 Evangelist proximity-shield DoT-zone) · III (rows #12 #18 Karroz crystals / Void Rifts) · IV (rows #3 #15 Ominous Altars / Void ritual-chest). GENRE-ATTESTED.
- `tm_spawner_nest` — an egg/young/nest spawner pre-seeds regenerating waves that pin the player front-and-rear. Present: I (row #9 Maggot nest) · III (row #14 Manticore young — the same egg-mechanic lineage). GENRE-ATTESTED. Secondary.

**MELEE-STRIKE** (swarm-the-brawl):
- `ms_swarm_surround` — massed melee runners close-and-surround from multiple angles; low individual threat, lethal density. Present: I (rows #1 #3 #12 Fallen/Zombie/Flayer swarms) · III (rows #1 #13 possessed infantry / Manticore) · IV (rows #4 #10 Hyenic Raiders / Kin beetle — note #10 is WHIRLWIND-primary, MELEE secondary per harvest). GENRE-ATTESTED.
- `ms_wedge_advance` — organized clan/military wedge advances to hold the player at a chokepoint with no sideways retreat. Present: I (rows #2 #6 #10 Goatman clan patrols) · III (rows #3 #7 Convict brawlers / Cronley gang). GENRE-ATTESTED.
- *(Hole: MELEE-STRIKE absent Age II — THE famous PoE1 melee deficit, 0/36; census §b ⚠-B. Rows #1 #2 #8 (Rhoa / Zombie herd / Blackguard wedge) are UNMAPPED to honor the hole — U-3/U-4. **These MUST NOT map into MELEE-STRIKE-II** (census guidance; the hole is load-bearing genre history). No MELEE formation dealt in Age II.)*

**DOT-AILMENT** (stack-and-retreat):
- `da_field_retreat` — casters stack DoT ground-fields (chaos/poison/cold/fire) from range then retreat; melee chaff drives the player INTO the fields. Present: I (rows #8 #16 Claw Viper cold-slow / Venom Lord acid) · II (rows #11 #18 Voidbearers / Chaos Zealots — signature attrition, density-caveat f-6) · III (rows #4 #11 Revenants / Bloodsworn) · IV (rows #8 #21 Filthy Crones / Nagasan). GENRE-ATTESTED.
- `da_curse_at_distance` — applied-at-distance debuff/curse stacks (Iron Maiden / Decrepify / Mark of Aetherfire) degrade the player without a ground-field. Present: I (row #17 Oblivion Knight curses) · III (row #16 Mark of Aetherfire). GENRE-ATTESTED. Secondary.

**MULTI-PROJECTILE-VOLLEY** (fan):
- `mpv_fan_from_position` — ranged units fan projectile volleys from a fixed/elevated position while a screen holds the player in the fan's cone. Present: I (rows #4 #11 Skeleton Archers / Specters) · II (rows #9 #15 Lunar Devotees / Goatman Shaman) · IV (rows #2 #6 #12 Candlemass / Desiccated Liches / Molten Imps). GENRE-ATTESTED.
- `mpv_boss_sweep` — a colossal entity delivers a fan-volley sweep across the arena (boss-tier). Present: IV (row #22 Lagon Storm Wave). GENRE-ATTESTED. Secondary: I (row #5 Blood Hawk dive-scatter — UNMAPPED U-1, converging-dive-vs-true-ranged ruling parked).
- *(Hole: MULTI-PROJECTILE-VOLLEY absent Age III — GD ranged is single-shot not fan-volley; census §b ⚠-C3. No formation dealt.)*

**CHAIN-BOUNCE** (bounce-and-chain):
- `cbn_corridor_arc` — arc/spark bolts bounce between player, adds, and walls; corridor geometry amplifies bounce hits into multi-hit pressure. Present: I (row #19 Unraveler chain-arc, MEDIUM per harvest) · II (row #19 Arc skeleton pack — the clearest attested) · III (row #15 Skeletal Priest raise-CHAIN, propagating-resurrection-as-chain). GENRE-ATTESTED.
- `cbn_derived_arc_pass` — RDR-derived for Age IV (see §5.4): a Lightning-Blast/arc-chain leader (kit corpus carries ~5 CHAIN-BOUNCE record kits in Age IV per Appendix-B B3). RDR-NATIVE-DERIVED. **Future validation path: a poe2db arc-chain direct pass** (harvest's own recommendation, §8). Secondary attested texture: IV (row #6 Scarab arc-bolt — the sole Age-IV signal, THIN, f-3; row #22 Storm Burst).

**SHAPESHIFT** (form-transition):
- `ss_phase_transform` — the transformation IS the mechanic: a boss/patrol transitions form (human→wolf, three-head-alternating, crystal-morph), and the new form brings new attack verbs; a fog/phase beat may spawn form-themed adds. Present: IV (row #11 Count Geonor human→wolf — the sole monster-side attested SHAPESHIFT on the spine). GENRE-ATTESTED. Secondary: IV admissions (Crystal Lotus / Xyclucian — future-lap specimens).
- `ss_derived_form_swap` — RDR-derived for Ages I + III (see §5.1, §5.2): the family kit-leader's form-swap mechanism (D2 Druid werewolf/werebear; GD player-transmog) rendered monster-side, where genre history holds SHAPESHIFT as player-kit-origin ONLY. RDR-NATIVE-DERIVED (two cells: SHAPESHIFT-I, SHAPESHIFT-III).

**DASH-STRIKER** (dash-and-strike):
- `ds_flank_burst` — dash-and-stab burst from a flank position (Shadow Strike lineage); the striker closes distance in a single burst, hits, repositions. Present: III (rows #7 #8 Cronley Murderer Shadow Strike — the sole GENRE-ATTESTED DASH-STRIKER on the spine). GENRE-ATTESTED.
- `ds_derived_gap_close` — RDR-derived for Age I (see §5.3): the family kit-leader's dash mechanism (Assassin Dragon Talon kick-dash / Flicker-lineage) rendered monster-side, where D2 has no dedicated dash-mob (Fanatic speed-mod is a modifier, not a dash-skill — f-2). RDR-NATIVE-DERIVED (one cell: DASH-STRIKER-I). **Age IV DASH-STRIKER gets NO derived formation (f-5 / §5 non-obligation).**

---

## §4 — UNMAPPED / reserved handling (census §d — nothing lost, nothing force-mapped)

Per census guidance, the 7 UNMAPPED rows are NOT force-mapped. The schema (§6) carries an **expressible `unmapped_reserved` slot** so they ride the artifact as findings for the next lap, never lost, never fabricated into a family.

| Ref | Subject | Disposition in this spec | Parked ruling needed |
|---|---|---|---|
| **U-1** | Blood Hawk aerial dive-scatter (Age I #5) | reserved; texture-secondary on `mpv_boss_sweep` | MPV boundary: converging-dive vs true-ranged-projectile |
| **U-2 + U-6** | Resurrection-leader (D2 Shaman + GD Dominator) | **ONE candidate cross-era MICRO-verb** spanning I+III, flagged CANDIDATE / NOT-A-FAMILY / docket-input (§5.6). NOT canonized. | resurrection-leader verb ruling (TOTEM-variant? MINION-PET re-seed? new verb?) — future docket |
| **U-3** | Rhoa physical-charge swarm (Age II #1) | reserved. **MUST NOT map into MELEE-STRIKE-II** (load-bearing PoE1 melee hole). | charge-swarm → WHIRLWIND (spin-and-close) or stay UNMAPPED-to-honor-hole? |
| **U-4** | Zombie herd slow-melee push (Age II #2) | reserved. **MUST NOT map into MELEE-STRIKE-II** (same hole). | UNMAPPED-to-honor-hole vs derived-mapping |
| **U-5** | Spider-nest environmental spawner (Age II #5) | reserved; candidate-secondary on `ts_environmental_nest` | environmental-spawner-nest: TOTEM sub-type or distinct nest-verb? |
| **U-7** | Void Horror three-body convergence (Age IV #14) | reserved; deck IV-F deals it as `[PATROL]`-isolation-break texture | is engage-one-reveals-all a MESO (formation) property orthogonal to family, or a family verb? |

**Charter §1 parked forks the spec does NOT resolve:** act-ORDER (§1.3) · the guest-family fork (IDENTITY-GAUGE / MINION-PET catalogue-only this run) · U-2..U-7 rulings above. These are commitment-boundaries (§5) or docket-work, not W1's job.

---

## §5 — The 5 RDR-NATIVE-DERIVED template entries (Gate-2 hard obligation L-9)

Per L-9: the corrected serving set = **5 cells / 4 findings**. Each cell gets a DERIVED mob-template spec entry — derived from the family kit-leader's mechanism verbs (R-b2), provenance-flagged **RDR-NATIVE-DERIVED**. Everything harvest-attested is GENRE-ATTESTED. **f-5 (DASH-STRIKER-IV) gets NO derived template** (fresh-draft non-obligation, T3-V2 — explicitly excluded).

### §5.0 — The TWO-LAW COMPOSITION carried on these entries (T3-V2 × L-9 — BOTH explicit)

**This is the load-bearing composition the charter demands I carry, not silently resolve.** Two laws govern these entries simultaneously:

- **T3-V2 (tier law)** governs ROSTER/HEADLINE composition: RATIFIED families may headline · DOCKETED serve as secondary · PROPAGATED are hypothesis-only (never solo-headline) · **FRESH-DRAFT families are excluded from *serving* as headliners.**
- **L-9 (serving set)** governs which CELLS get derived template entries so the 4 findings are answerable: SHAPESHIFT-I, SHAPESHIFT-III, DASH-STRIKER-I, CHAIN-BOUNCE-IV, WHIRLWIND-II.

**Where they interact:** DASH-STRIKER-I and CHAIN-BOUNCE-IV are **fresh-draft-TIER families** (Appendix-B B3) inside the L-9 cell set. The composition resolves as: **the derived template EXISTS** (the finding is answered, provenance-flagged RDR-NATIVE-DERIVED) — L-9 satisfied. **AND** per T3-V2 a fresh-draft family **may not HEADLINE an act encounter** — so these templates appear as `serving_role: secondary` / texture / docket-input ONLY, never as a MACRO deck's headline hostile. The template's `serving_role` field (schema §6.5) carries the restriction as data. SHAPESHIFT-I/III and WHIRLWIND-II sit in DOCKETED/RATIFIED-tier families respectively, so their derived templates may serve at their family's tier (SHAPESHIFT DOCKETED → secondary-capable; WHIRLWIND RATIFIED → headline-capable).

**Concrete tier map for the 5 cells:**

| Cell | Family tier (Appendix-B) | Finding answered? (L-9) | May headline? (T3-V2) | `serving_role` |
|---|---|---|---|---|
| SHAPESHIFT-I | DOCKETED (0.80) | ✓ | secondary only (docketed) | `secondary` |
| SHAPESHIFT-III | DOCKETED (0.80) | ✓ | secondary only (docketed) | `secondary` |
| DASH-STRIKER-I | FRESH-DRAFT | ✓ | **NO (fresh-draft)** | `texture_docket_input` |
| CHAIN-BOUNCE-IV | FRESH-DRAFT | ✓ | **NO (fresh-draft)** | `texture_docket_input` |
| WHIRLWIND-II | RATIFIED | ✓ (f-4 fold, Gate-2 adopted) | yes (ratified) | `headline_capable` |

**Composition-soundness check (charter demand — surface tension, don't silently pick a law):** I found NO unsound case. The two laws compose cleanly here because L-9's "the template EXISTS" and T3-V2's "fresh-draft may not headline" operate on DIFFERENT fields — existence (`provenance`) vs serving-role (`serving_role`). A fresh-draft cell's derived template can simultaneously exist (answering the finding) and be barred from headlining (respecting the tier law). **No tension to escalate.** The one place it *could* have been unsound — if L-9 had required a fresh-draft template to headline — it does not: L-9 requires the finding be *answerable*, which secondary/texture placement satisfies. Recorded for the conductor: the composition is sound; the derived-fresh-draft templates ship as texture/docket-input, not headliners.

### §5.1 — SHAPESHIFT-I (Age I · Diablo II) — RDR-NATIVE-DERIVED · DOCKETED · `serving_role: secondary`

- **Why derived:** f-1 CONFIRMED — SHAPESHIFT has no monster-side template in Age I. Genre history holds it player-kit-origin only (D2 Druid Shapeshifting tree — werewolf/werebear). The optional bosses (Andariel poison-metamorphosis, Possessed champion modifier) are thematically adjacent, mechanically distinct; excluded (census §b, admission A-I.2). Zero fabrication of a "found" mob — this is an explicitly-derived template.
- **Derivation leader (kit-side mechanism):** D2 Druid Shapeshifting — the form-swap verb: enter an alternate body-form that replaces the attack surface (melee-brawl form) and buffs survivability.
- **Derived template:** a faction-member that TRANSITIONS from a humanoid caster/handler form into a beast-brawl form on an HP/aggro trigger; the transition swaps its MICRO verb from a ranged/handler pressure to `ms_swarm_surround`-adjacent melee pressure. MESO: `ss_derived_form_swap`. Element/court: inherits from the become-family's court (Q38 §1.2).
- **Serving:** SECONDARY only (DOCKETED tier). Appears as a form-transition texture WITHIN a hostile brawl archetype (deck I-D), never as its own headline. `provenance: RDR-NATIVE-DERIVED`, `derivation_source: "D2 Druid Shapeshifting (player-kit)"`.

### §5.2 — SHAPESHIFT-III (Age III · Grim Dawn) — RDR-NATIVE-DERIVED · DOCKETED · `serving_role: secondary`

- **Why derived:** f-1 CONFIRMED — same finding, Age III. GD's single SHAPESHIFT record is player-kit; the Bloodsworn Summoner "transform" is a summoner-variant not a body-morph (admission A-III.1); the Ravager three-form boss is post-game optional, excluded (A-III.2). Age IV DOES have monster-side SHAPESHIFT (Geonor) — so this finding is I+III-specific.
- **Derivation leader:** GD player-transmog / form-swap mastery mechanic.
- **Derived template:** structurally identical to §5.1 (form-transition monster), re-skinned to the Age-III Aetherial/Chthonian faction dressing (biome-morph rider, §1.2). Transition trigger = HP/phase; new form brings a sustained-fight verb (`cb_lane_hold`-adjacent or `ms_wedge_advance`-adjacent per the become-family). MESO: `ss_derived_form_swap`.
- **Serving:** SECONDARY only. Texture within deck III-C or III-E. `provenance: RDR-NATIVE-DERIVED`, `derivation_source: "GD player-transmog (player-kit)"`.

### §5.3 — DASH-STRIKER-I (Age I · Diablo II) — RDR-NATIVE-DERIVED · FRESH-DRAFT · `serving_role: texture_docket_input`

- **Why derived:** f-2 CONFIRMED — no dedicated dash-teleport mob in D2. The Fanatic-enchanted +100% move-speed is the closest but is a MODIFIER not a dash-skill (admission A-I.1). The Assassin Dragon Talon kick-dash is the player side. Zero fabrication.
- **Derivation leader:** D2 Assassin Dragon Talon / charge-lineage — the gap-close-and-strike verb: cover distance in a single burst, deliver a strike, disengage.
- **Derived template:** a flanking striker that dashes into the player from a perimeter position, delivers a burst hit, and repositions out (Shadow-Strike behavior rendered in the D2 faction idiom). MESO: `ds_derived_gap_close`.
- **Serving:** TEXTURE / DOCKET-INPUT ONLY — **fresh-draft tier bars headlining (T3-V2, §5.0).** Appears as a flank-pressure texture within a hostile MELEE brawl (deck I-A / I-D), or as an input to a future DASH-STRIKER docket. NEVER a headline hostile. `provenance: RDR-NATIVE-DERIVED`, `derivation_source: "D2 Assassin Dragon Talon (player-kit)"`.

### §5.4 — CHAIN-BOUNCE-IV (Age IV · PoE2 + LE) — RDR-NATIVE-DERIVED · FRESH-DRAFT · `serving_role: texture_docket_input`

- **Why derived:** f-3 CONFIRMED — CHAIN-BOUNCE-IV is THIN: the only signal is the Scarab arc-bolt SECONDARY (row #6), no dedicated primary CHAIN-BOUNCE row in PoE2/LE. Ages I/II/III each have a primary chain row; Age IV is the sole thin cell.
- **Derivation leader:** the Age-IV chain kit corpus — Lightning Blast (LE) / Arc (PoE2), ~5 CHAIN-BOUNCE record kits per Appendix-B B3.
- **Derived template:** an arc-chain caster whose bolts bounce player→adds→walls; the derived MESO is `cbn_derived_arc_pass`, using the Age-IV faction dressing (Maraketh/Vaal/Void). Attested texture available: Scarab arc-bolt (row #6), Storm Burst (row #22).
- **Future validation path (harvest's own recommendation, §8):** a **poe2db arc-chain direct pass** — Arc is a PoE2 skill with act-spine encounter presence that the W0 web sources did not surface; a targeted poe2db lookup would upgrade this cell from RDR-derived to GENRE-ATTESTED in a future lap. Named here as the cell's validation route.
- **Serving:** TEXTURE / DOCKET-INPUT ONLY — **fresh-draft tier bars headlining (T3-V2, §5.0).** `provenance: RDR-NATIVE-DERIVED`, `derivation_source: "LE Lightning Blast / PoE2 Arc (player-kit corpus)"`, `validation_path: "poe2db arc-chain direct pass"`.

### §5.5 — WHIRLWIND-II (Age II · Path of Exile 1) — RDR-NATIVE-DERIVED · RATIFIED · `serving_role: headline_capable`

- **Why derived:** f-4 — the FOURTH kit-present/monster-empty cell, NOT in the original L-8 three, **folded into the serving set at Gate-2 (3→4, L-9(ii), jack-ryan §8 authority).** Appendix-B B1 records WHIRLWIND=1 for Age II; harvest supplies zero (⚠-A). Same class as f-1/f-2/f-3: a PoE1 spin/melee deficit (same root as the MELEE-STRIKE-II hole). Re-crawl was REJECTED at Gate-2 (no integrity payoff for a single fresh-record cell). Zero fabrication.
- **Derivation leader:** the WHIRLWIND kit-leader spin-and-close mechanism.
- **Derived template:** because PoE1 has no native spin-mob, the derivation renders WHIRLWIND-II as an **aura-driven frenzy line** (`ww_derived_frenzy_line`, §3.3) — a pack that behaves as a converging spin-body driven by a leader's frenzy aura, in the PoE1 bandit/cultist idiom. This is the honest derivation: it does NOT fabricate a PoE1 spinning mob; it renders the family's spin-and-close pressure through PoE1-available mechanisms (aura + frenzy), which the era DOES have.
- **Serving:** HEADLINE-CAPABLE (RATIFIED tier — the ONLY one of the 5 derived cells that may headline). May anchor a hostile archetype in deck II. **BUT the traveling-kin exemption note:** WHIRLWIND-II is precisely the family whose kin caravan (a whirlwind caravan in the trap-age) is the T3-F5 archetype case — so WHIRLWIND presence in Age II is TWO things: this RDR-derived HOSTILE template (era-honest derivation), and separately, the era-EXEMPT kin slot when the player became WHIRLWIND. These do not conflict: one is a derived hostile, one is a traveling kin. `provenance: RDR-NATIVE-DERIVED`, `derivation_source: "WHIRLWIND kit-leader spin-and-close, rendered as PoE1 aura-frenzy line"`.

### §5.6 — The cross-era resurrection-leader (U-2 + U-6) — CANDIDATE MICRO-verb, NOT one of the 5 derived templates

Per census §d + guidance: U-2 (D2 Fallen/Fetish Shaman) and U-6 (GD Aetherial Dominator) are the SAME mechanism in two ages — a resurrection-leader that raises battlefield dead as a self-replenishing melee screen. **Spec'd as ONE candidate cross-era MICRO-verb spanning I+III, flagged CANDIDATE / NOT-A-FAMILY / docket-input. DO NOT canonize.** It rides the schema as an `unmapped_reserved` entry with `candidate_verb: resurrection_leader`, `spans_eras: [I, III]`, `docket_input: true`. It is NOT a sixth derived template and NOT a family; it is a parked verb-candidate for a future resurrection-leader ruling (which would resolve U-2 and U-6 together). Its nearest existing home is `ts_resurrection_loop` (§3.3) as a formation texture, but the ruling on whether resurrection-leadership is a TOTEM-variant, a MINION-PET re-seed, or a new verb is future-docket work (§4).

---

## §6 — Schema congruence (how ARTIFACT B binds to this spec + the emission bundle)

The JSON schema twin (`…-w1-encounter-schema-draft.json`) is the payload shape for the reserved top-level **`encounters`** bundle key (T3-V7 — KR Lane-1 reserved it and builds no encounter emission until this schema freezes it). This section states the congruence contract; the schema file is the machine form.

### §6.1 — Verified emission bundle shape (this session, against on-disk `one_realm_demo_bundle.json`)

Confirmed top-level keys: `bundle_version`, `generated_at`, `engine_version`, `season_id`, `schema_status`, `schema_note`, `proxy_scaling`, `stage2_run_record`, `kits`, `monsters`, `gear_pool`, `factions`, `floor_manifest`, `_assembly_notes`. **No `encounters` key exists yet** — this schema freezes its payload. The `encounters` payload is a SIBLING top-level key, congruent with the existing keys' style (versioned, season-scoped).

### §6.2 — The join surfaces (encounter grammar → existing bundle keys)

- **→ `factions.clusters[]`** (family groupings, R-b1): each cluster carries `cluster_id`, `name`, `identity_narrative`, `thematic_tags`, `member_kit_ids`. The encounter roster references `family` (working label) AND may carry `cluster_id_ref` to bind to the emitted faction cluster. Family is the join key (R-b1: "modular roster keys monsters→factions on FAMILY").
- **→ `factions.relationships[]`** (disposition, R-b3): carries `between: [id,id]`, `type` (`rival` etc.), `tension_narrative`. **The kin/hostile disposition speaks this vocabulary** — `disposition: kin` maps to a relationship `type: "kin"` keyed on player-form; `disposition: hostile` maps to the default rival/hostile relationship. The encounter schema's `disposition` enum is the encounter-side authority; the emission `relationships` array is where it lands.
- **→ `floor_manifest.floor_sequence[]`** (MACRO substrate): carries `floor_id`, `dominant_element`, `notes`. The per-era MACRO deck is the era-stratified GENERALIZATION of `floor_sequence` — an act's dealt archetypes populate a floor sequence. `dominant_element` is the biome-morph consumption hook (§1.2).
- **→ `monsters[]`** (MESO/MICRO binding): carry `id`, `archetype_tag`, `dominant_element`, `role_orientation`, `range_profile`, `preferred_behavior`, `skill_rotation_priority`, `aggro_radius_m`, `leash_distance_m`, `skills[]`. MESO formations bind `aggro_radius_m`/`leash_distance_m`/pack-spread; MICRO verbs bind `preferred_behavior`/`skill_rotation_priority`/`skills[]`. An encounter instance's roster is a list of `monster_id` refs + a formation + a verb-set.

### §6.3 — The `encounters` payload top-level shape (frozen here)

```
encounters (object):
  encounters_version : "encounters-v1"        // mirrors bundle_version style
  season_id          : string                 // joins the bundle season
  schema_status      : "DRAFT"                 // working-label caveat lives here + in $comment
  working_label_caveat : string               // the §5-caveat, machine-visible
  provenance_axis    : ["GENRE-ATTESTED","RDR-NATIVE-DERIVED"]   // the two values, declared
  era_decks          : [ EraDeck, ... ]        // 4 entries, one per era (MACRO)
  formation_catalogue: [ Formation, ... ]      // MESO, per (family, era) cell, ≥2/cell
  pressure_verbs     : [ PressureVerbSet, ... ]// MICRO, ≥1/family, inherit per R-b2
  unmapped_reserved  : [ UnmappedEntry, ... ]  // U-1..U-7 + resurrection-leader candidate
  encounter_instances: [ EncounterInstance, ...] // OPTIONAL at W1 (RD-1 populates); schema-ready now
```

### §6.4 — Forward-instantiability as RD-1 (charter §4 + T3-V6)

The schema is **forward-instantiable as RD-1** (the conditional first run-object, fires only on W3 gate PASS). RD-1 populates: per-era act decks (`era_decks` filled with dealt archetypes) · family rosters under T3-V2 (each encounter's roster tier-restricted per §5.0) · the encampment slot (kin slot filled from become-history) · encounter instances with formations + verbs (`encounter_instances[]` populated). **Schema-valid instantiation is RD-1's own done-predicate.** Therefore `encounter_instances` is OPTIONAL in the W1 schema (empty is valid — W1 freezes the shape) but its item schema is COMPLETE now, so RD-1's fill is a validation target, not a schema extension. NO star-lord pipeline code from this run — RD-1 is a spec-authored DATA artifact + gamora smoke (T3-V6).

### §6.5 — The tier-restriction + provenance as DATA (not identity)

Every roster entry and derived template carries:
- `provenance ∈ {GENRE-ATTESTED, RDR-NATIVE-DERIVED}` — the census two-value axis (§1.1). TAG, not identity.
- `family` — working-label string token (rename-safe).
- `serving_role ∈ {headline_capable, secondary, texture_docket_input}` — the T3-V2 × L-9 composition as data (§5.0). A fresh-draft family's derived template carries `texture_docket_input`; the emission/RD-1 consumer reads this to place it as texture, never headline.
- `family_tier ∈ {RATIFIED, DOCKETED, PROPAGATED, FRESH-DRAFT}` — the Appendix-B tier, so the tier law is re-derivable from data.

---

## §7 — What W1 hands W2 (and the parked items)

**To W2 (fit layer + sim scenarios):**
- This spec as spec-as-math: `fit(kit, encounter | era)` reads (a) the family address (§1.1), (b) the MICRO verb-set per family (§3.3 verb column / §5 derived), (c) the MESO formation topology (§3.3), (d) the era shelf (§1.2). W2's job is to make `fit` compute over 267 × per-era decks without error, and to build MESO/MICRO sim scenarios.
- **Harness-expressiveness risk is flagged for W2 by design (charter §4/§8):** if the gamora harness cannot express formation topology (`aggro_radius_m`/`leash_distance_m`/pack-spread geometry, the `cbn_corridor_arc` wall-bounce, the `cb_crossfire` paired-beam geometry), that surfaces at W2 as a red-flag ping + honorable fallback (harness-extension spec routed to KR Lane-2, T3-V7 — never a new lane). The formations most likely to strain the harness: `cbn_corridor_arc` (needs wall geometry), `cb_crossfire` (needs paired-emitter positional tracking), `ts_environmental_nest` (needs terrain-spawner), `ss_phase_transform` (needs mid-fight verb-swap). W2 should probe these first.

**To RD-1 (conditional, on W3 PASS):** the complete schema (§6) + the tier-restriction data (§6.5) + the kin-slot template (§2.3) — RD-1 composes the first act-structured run-object and validates it against this schema.

**PARKED (not W1's job — §4 + charter §5):** act-ORDER story fork · U-2..U-7 rulings (incl. resurrection-leader) · guest-family fork · family NAMES canonization (commitment-boundary) · kin-caravan NPC ensemble (story fold, T3-V5).

---

## §8 — Confidence tags that travel (Gate-2 obligation L-9 · census §h)

Per L-9 hard obligation 4, MEDIUM-confidence tags travel into the spec + schema:
- **Age II rows 17–18** (Maxroll-only citation floor, poewiki 403-blocked — census §h.4): the formations derived from these rows (`tm_preseed_corridor` Hellion #17, `da_field_retreat` Chaos Zealot #18) carry `confidence: MEDIUM`.
- **All 9 LE rows (Age IV #14–22)** (1.0-era data; LE Season-3 enemy-behavior overhauls NOT reflected — census §h.5): every Age-IV element sourced from an LE row carries `confidence: MEDIUM` + `staleness_note: "LE 1.0-era; Season-3 overhauls not reflected"`. A Season-3 delta pass is a future-lap item.
- **Harvest-internal MEDIUM flags** carried through: `ww_arc_sweep`/III (Alkamos Blade Arc is arc-sweep not true 360° spin) · Port Valbury/Valdaran (sealed-dungeon sample access).

All other elements carry `confidence: HIGH` (the harvest's default for well-anchored rows).

---

## §9 — Ingestion normalization (Gate-2 obligation L-9 · census §h.1–h.3)

Per L-9 hard obligation 3, this spec's schema + any consumer normalizes the two-agent-split drift:
- **Header casing:** Files I+III use Title Case (`Area Archetype`, `Faction-Camp`); files II+IV use sentence case (`Area archetype`, `Faction-camp`). Same six-column semantics. Ingestion normalizes to the schema's canonical field names (§6) — never assume byte-identical headers.
- **Source-attribution branch:** Age IV needs the per-row `**PoE2**`/`**LE**` tag for the source dimension (the only two-game era); Ages I–III inherit source from the file header (D2/PoE1/GD). The schema's `source_game` field is per-row for Age IV, file-level for I–III (census §h.3).
- **Preamble format:** read the ROW TABLE + SUMMARY as authoritative, not the family-deck preamble (which diverges in format between the pairs — census §h.2).

---

**Spec complete.** Per-tier counts: **MACRO** = 4 era decks × ≥4 archetypes (I:5+kin · II:5+kin · III:5+kin · IV:6+kin) all with disposition + reserved kin slot. **MESO** = ≥2 formations per family-present cell (catalogue §3.3, 11 families × formations, holes respected). **MICRO** = ≥1 pressure-verb set per family (the §3.3 verb column, R-b2-inherited). **5 RDR-NATIVE-DERIVED templates** authored (§5.1–5.5); f-5 excluded. Two-law composition carried explicitly (§5.0) — sound, no tension to escalate. Working labels stamped throughout. NO production code.

*Filed by named-`gandalf` sub-agent (SPEC-AUTHOR), 2026-07-22.*
