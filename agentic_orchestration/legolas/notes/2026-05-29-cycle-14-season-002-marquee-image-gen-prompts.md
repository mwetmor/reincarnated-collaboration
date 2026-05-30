# Image-Gen Prompt Templates — Cycle 14 Season 002
## Season of the Ironsoil Wide-Front — Per-Faction GROUP Portraits + Per-Kit INDIVIDUAL Portraits

**Author:** legolas (research scout; Mode A analytical)
**Date:** 2026-05-29
**Commissioner:** knight-rider (cascade-r4; Season 002 marquee work per Matt 2026-05-29 directive)
**Consumed by:** drax + galadriel (ChatGPT API image-gen; faction group portraits + per-kit individual portraits)
**Authority:** Matt 2026-05-29 verbatim directive — "let's get Season 002 looking like the best we have ever delivered"
**Substrate source:** `agentic_orchestration/cycle-14-wave-5-season-002/phase5_faction_clusters.json` + `wave_b_identities.json`
**Galadriel coordination:** galadriel Season 002 visual-coherence design NOT yet landed at authoring time. These are baseline prompts built from substrate metadata only. Post-galadriel iteration plan: see § Coordination Note at file end.

---

## Style Register Adherence — Locked Language

Applied to every template in this file. All prompts include the following locked language per `canonical/story/style-register.md`:

> hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy / Eastward / CrossCode art direction; isekai-genre-readable; NOT retro pixel-art; pixel-resolution sprites with hand-drawn-illustration sensibility; detailed shading and palette work

---

## D7 AI-Tell Line Compliance Statement

All templates comply with `canonical/38-downstream-delivery-strategy-2026-05-23.md` § D7:

- Prompts use structured, substrate-grounded visual direction — no free-form LLM dialogue generation requests
- All prompts are <= 200 words
- Style register language is fixed (not a variable blank)
- Prompts are STRUCTURED INPUTS to the image-gen API, not open-ended narrative prompts
- No raw LLM output shipped player-facing without human curation layer

---

## Substrate Metadata Reference — Season 002

| Cluster | Faction Name | Members | Cultural Lineage | Engagement | Geometry | Elements (top) |
|---|---|---|---|---|---|---|
| 1 | Stormcallers of the Pale Reach | 3 | european | ranged | large-AOE | lightning 33% / shadow 33% / fire 33% |
| 2 | Ironsoil Vanguard | 9 | european | close | large-AOE | physical 56% / earth 44% |
| 3 | Gale-Blessed Wardens | 13 | fantasy_generic | close | large-AOE | wind 31% / holy 23% / water 23% |
| 4 | Duskchain Ranging Compact | 8 | fantasy_generic | ranged | chain | shadow 38% / physical 25% / lightning 12% |

---

---

# SECTION 1 — PER-FACTION GROUP PORTRAIT PROMPTS (4 prompts)

---

## Group Portrait 1 — Stormcallers of the Pale Reach

**Substrate metadata:** cluster_id=1 | 3 members | european medieval | ranged large-AOE | lightning 33% + shadow 33% + fire 33% (perfectly balanced tri-element) | tags: tri-element ranged, medieval european, wide-arc devastation

**Faction identity narrative (canonical):** "Rooted in European medieval combat tradition, these ranged fighters channel lightning, shadow, and fire in equal measure — practitioners of wide-arc elemental devastation rather than precision. Their craft is less doctrine than pattern, a recurring convergence of destructive range found among those who learned to strike from distance before they learned to ask why."

**Word count:** 178 | Style-adherence: PASS | D7 compliance: PASS

```
GROUP PORTRAIT — Stormcallers of the Pale Reach (Cluster 1)
Season: cycle-14-wave-5-season-002 — Season of the Ironsoil Wide-Front
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy / Eastward / CrossCode art direction; isekai-genre-readable; NOT retro pixel-art; pixel-resolution sprites with hand-drawn-illustration sensibility; detailed shading and palette work

SCENE: A pale, storm-swept highland bluff at dusk. Three European medieval ranged fighters stand in loose triangular formation, each channeling a different destructive force at full draw. Left figure: crackling lightning coils around their raised arms, arcs branching wide across the grey sky. Center figure: shadow threads spill outward from a half-raised staff, pooling darkness at their feet. Right figure: fire blooms in both hands, a wide fan of flame not aimed but released — spreading rather than targeting. All three strike simultaneously, their combined AOE devastating the emptiness before them. The scene reads devastation-first, doctrine-never. Wide-arc composition: the three elemental releases fan out across the full width of the frame, overlapping at the center in a tri-colored convergence of lightning-gold, shadow-violet, and fire-ember.

Lighting: storm-grey sky backlit by simultaneous tri-elemental discharge. Atmosphere: cold highland wind; the smell of ozone and char. Color palette: lightning-gold / shadow-deep-violet / fire-amber-orange against pale grey stone and bleached grass. Ultra-thematic. Dramatic. Pixel-art HD-2D; hand-drawn illustration sensibility; isekai-game-coded; NO retro pixel style.
```

---

## Group Portrait 2 — Ironsoil Vanguard

**Substrate metadata:** cluster_id=2 | 9 members | european medieval | close large-AOE | physical 56% + earth 44% | tags: ironsoil, close-crush, earthen-mass

**Faction identity narrative (canonical):** "Forged from European medieval martial tradition, these close-quarters fighters channel raw physical force and earthen weight into sweeping ground-level devastation. Their combat identity is defined by mass and proximity — bodies and terrain weaponized together in crushing wide-arc engagements."

**Word count:** 183 | Style-adherence: PASS | D7 compliance: PASS

```
GROUP PORTRAIT — Ironsoil Vanguard (Cluster 2)
Season: cycle-14-wave-5-season-002 — Season of the Ironsoil Wide-Front
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy / Eastward / CrossCode art direction; isekai-genre-readable; NOT retro pixel-art; pixel-resolution sprites with hand-drawn-illustration sensibility; detailed shading and palette work

SCENE: An earthen battleground, soil churned and cracked, mist low across broken ground. Nine European medieval close-quarters fighters press forward as a single crushing mass. Front rank: massive warriors with earth-stained armor delivering wide horizontal arc swings, ground fracturing beneath each blow. Mid rank: heavy-set fighters whose strikes raise plumes of soil and gravel, earthen force amplifying raw physical weight. Rear edge barely visible — a depth of bodies suggesting this is the front of an army, not a squad. The wide-arc AOE reads through overlapping impact zones: cracked earth radiates outward in concentric rings from multiple simultaneous strike points. No ranged reach, no elemental flash — only mass and proximity weaponized together.

The mood: relentless. Grim. European medieval martial tradition at its most earthbound. Color palette: ironsoil-brown / aged-steel-grey / earthen-amber dust clouds against muted overcast sky. Ground-level composition — the scene is fought at the soil, not above it. Ultra-thematic. Dramatic. Pixel-art HD-2D; hand-drawn illustration sensibility; isekai-game-coded; NO retro pixel style.
```

---

## Group Portrait 3 — Gale-Blessed Wardens

**Substrate metadata:** cluster_id=3 | 13 members | fantasy_generic medieval | close large-AOE | wind 31% + holy 23% + water 23% + lightning 8% + physical 8% + shadow 8% | tags: wind-dominant, broad-front-combat, elemental-convergence

**Faction identity narrative (canonical):** "A loose medieval fellowship of close-quarters fighters who channel broad sweeps of wind, water, and holy force across wide fronts, their combat style shaped less by doctrine than by the practical overlap of elemental affinities common to the region's wandering defenders. Their identity coheres around the shared geometry of their fighting — wide, sweeping, and sanctified by ambient elemental pressure rather than any formal creed."

**Word count:** 192 | Style-adherence: PASS | D7 compliance: PASS

```
GROUP PORTRAIT — Gale-Blessed Wardens (Cluster 3)
Season: cycle-14-wave-5-season-002 — Season of the Ironsoil Wide-Front
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy / Eastward / CrossCode art direction; isekai-genre-readable; NOT retro pixel-art; pixel-resolution sprites with hand-drawn-illustration sensibility; detailed shading and palette work

SCENE: An open hilltop meadow in the moment before a storm breaks — a loose fellowship of thirteen medieval defenders in mid-sweep, each pulling from a different ambient elemental current. Wind-swept cloaks and banners. The central group of fighters executes wide horizontal arcs, gale-force pressure visible as translucent wind-sweeps crossing the full width of the frame. Holy light bleeds upward from one defender's blade, not blazing but present — sanctified without ceremony. Water-force ripples laterally from another fighter's extended arm, flat and sweeping. The thirteen figures are NOT a tight formation — they are spread across the front, connected not by rank but by the shared geometry of their wide reach.

The mood: elemental convergence without doctrine. The fellowship coheres through common width of arc, not shared creed. Color palette: wind-translucent-teal / holy-soft-gold / water-pale-blue against open grey-green meadow. Sky: overcast but not dark — ambient elemental pressure rather than storm. Ultra-thematic. Dramatic. Pixel-art HD-2D; hand-drawn illustration sensibility; isekai-game-coded; NO retro pixel style.
```

---

## Group Portrait 4 — Duskchain Ranging Compact

**Substrate metadata:** cluster_id=4 | 8 members | fantasy_generic medieval | ranged chain | shadow 38% + physical 25% + lightning 12% + earth 12% + wind 12% | tags: shadow-threading, chain-engagement, frontier-ranging

**Faction identity narrative (canonical):** "A loosely bound collective of ranged fighters who thread shadow and physical force across chained strike patterns, operating in the grey margins of medieval frontier territories. Their combat doctrine favors cascading pressure over direct confrontation, letting darkness and momentum do the work that steel begins."

**Word count:** 187 | Style-adherence: PASS | D7 compliance: PASS

```
GROUP PORTRAIT — Duskchain Ranging Compact (Cluster 4)
Season: cycle-14-wave-5-season-002 — Season of the Ironsoil Wide-Front
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy / Eastward / CrossCode art direction; isekai-genre-readable; NOT retro pixel-art; pixel-resolution sprites with hand-drawn-illustration sensibility; detailed shading and palette work

SCENE: The grey margin of a frontier forest at dusk — sparse trees, uneven ground, the light failing. Eight loosely scattered ranged fighters at various depths of shadow and visibility, each mid-chain-strike. Shadow threads visible as dark filament connecting targets across the mid-ground — not arrows but cascading force jumping from point to point. The chain pattern is the visual subject: dark energy traces a non-linear path through the scene, physically connecting the eight fighters to each other and to their targets in a web of accumulated pressure. Physical force-bolts anchor the chain at key strike nodes; occasional lightning sparks mark where momentum detonates. Some fighters are barely visible — only their shadow-threads and their ranged releases mark their positions.

The mood: patient accumulation, then cascade. Not confrontation — dissolution. Color palette: shadow-deep-violet / physical-steel-grey / dusk-amber-edge lighting against dark frontier forest. The scene reads darker than the other three factions, marginally lit. Ultra-thematic. Dramatic. Pixel-art HD-2D; hand-drawn illustration sensibility; isekai-game-coded; NO retro pixel style.
```

---

---

# SECTION 2 — PER-KIT INDIVIDUAL PORTRAIT PROMPTS (33 prompts)

Each prompt <= 150 words. Kit ID, canonical name, faction, and key substrate axes documented per template.

---

## FACTION 1 — STORMCALLERS OF THE PALE REACH (3 kits)

---

### Kit S2-01 — Stormcaller of the Pale Reach (Lightning/Variable/INT)

**Kit ID:** S1_endgame_bc_ranged_medium_variable_int_light_s0
**Canonical name:** Stormcaller of the Pale Reach
**Faction:** Stormcallers of the Pale Reach (Cluster 1)
**Substrate axes:** ranged | medium tempo | variable amplitude | INT | lightning primary
**Kit narrative:** "A lightning-attuned ranged fighter whose variable tempo reflects the unpredictable discharge of a storm front — striking at medium range with surging INT-driven arcs that widen before they resolve."

**Word count:** 118 | Style-adherence: PASS | D7 compliance: PASS

```
INDIVIDUAL PORTRAIT — Stormcaller of the Pale Reach
Season: cycle-14-wave-5-season-002
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy art direction; isekai-genre-readable; NOT retro pixel-art

A European medieval ranged fighter, staff raised mid-release, lightning arcing wide from outstretched arms across a pale storm sky. Medium range — they have not closed but are not distant. The lightning does not target a single point; it widens as it travels, an arc not aimed but swept. Variable tempo visible in the charged stillness: the strike has not yet landed but the field is already reshaped. European medieval robes, storm-grey and pale-gold palette. Background: highland stone wall, sky the color of an hour before lightning.

Mood: intellectual precision weaponized as elemental chaos. Pixel-art HD-2D; hand-drawn illustration sensibility; isekai-game-coded.
```

---

### Kit S2-02 — Dusk Caller of the Pale Reach (Shadow/Variable/INT)

**Kit ID:** S1_endgame_bc_ranged_medium_variable_int_light_s1
**Canonical name:** Dusk Caller of the Pale Reach
**Faction:** Stormcallers of the Pale Reach (Cluster 1)
**Substrate axes:** ranged | medium tempo | variable amplitude | INT | shadow primary
**Kit narrative:** "A shadow-element ranged practitioner whose variable tempo strikes spread across wide arcs rather than single targets, reading the field through INT-weighted intuition carried from a south asian martial lineage into the Stormcallers' broader pattern."

**Word count:** 125 | Style-adherence: PASS | D7 compliance: PASS

```
INDIVIDUAL PORTRAIT — Dusk Caller of the Pale Reach
Season: cycle-14-wave-5-season-002
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy art direction; isekai-genre-readable; NOT retro pixel-art

A medium-range ranged fighter amid the Pale Reach's storm-grey highlands, arms spread in a wide releasing gesture, shadow billowing outward in broad arcs rather than focused beams. She does not aim — she saturates. Shadow pulses move like waves across the frame, variable in density, reading INT-driven intuition rather than formula. South Asian martial lineage visible in stance: fluid, distributed, no fixed guard. European medieval environment: stone walls, pale sky. Shadow-violet and dusk-indigo palette against bleached stone.

Mood: field-saturation over precision. Every pulse calibrated by feel. Pixel-art HD-2D; hand-drawn illustration sensibility; isekai-game-coded.
```

---

### Kit S2-03 — Ember Caller of the Pale Reach (Fire/Variable/INT)

**Kit ID:** S1_endgame_bc_ranged_medium_variable_int_light_s2
**Canonical name:** Ember Caller of the Pale Reach
**Faction:** Stormcallers of the Pale Reach (Cluster 1)
**Substrate axes:** ranged | medium tempo | variable amplitude | INT | fire primary
**Kit narrative:** "A variable-tempo ranged practitioner whose fire arcs wide across contested ground, trading pinpoint control for sweeping ignition that reshapes the field before the enemy closes."

**Word count:** 121 | Style-adherence: PASS | D7 compliance: PASS

```
INDIVIDUAL PORTRAIT — Ember Caller of the Pale Reach
Season: cycle-14-wave-5-season-002
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy art direction; isekai-genre-readable; NOT retro pixel-art

A ranged European medieval fighter on a pale highland rise, fire fanning outward from raised hands in a wide sweep — not a beam, not a bolt, but an arc of ignition spreading across contested ground. She reads the burn as pattern: the field is reshaped before the enemy has closed. Variable tempo: the fire builds then releases in surging intervals. Fire-amber and ember-orange against pale grey sky. Char-black scorch lines trace the ground below the arc.

Mood: fire as field architecture — not targeted but distributed. The fighter is architect of the burn, not wielder of a weapon. Pixel-art HD-2D; hand-drawn illustration sensibility; isekai-game-coded.
```

---

## FACTION 2 — IRONSOIL VANGUARD (9 kits)

---

### Kit S2-04 — Ironsoil Breaker of the Flattened Ground (Physical/Flat/STR)

**Kit ID:** S1_endgame_bc_melee_high_flat_str_none_s0
**Canonical name:** Ironsoil Breaker of the Flattened Ground
**Faction:** Ironsoil Vanguard (Cluster 2)
**Substrate axes:** close/melee | high tempo | flat amplitude | STR
**Kit narrative:** "A relentless STR-driven striker who sustains flat, unbroken pressure at melee range, grinding opponents down through sheer mass and repeated wide-arc blows. Every engagement is a contest of earthen weight — the Breaker plants and pushes."

**Word count:** 127 | Style-adherence: PASS | D7 compliance: PASS

```
INDIVIDUAL PORTRAIT — Ironsoil Breaker of the Flattened Ground
Season: cycle-14-wave-5-season-002
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy art direction; isekai-genre-readable; NOT retro pixel-art

A massive European medieval STR fighter planted in churned earth, mid-wide-arc swing, the weight of the strike visible in ground fractures spreading from their feet. High tempo: this is not a single blow — it is the middle of many. Flat amplitude: no explosive burst, no surge, just unrelenting pressure. The figure is broad, low-centered, armored in iron-dark plate caked with soil. Every blow grinds. European medieval battlefield: broken ground, grey overcast sky, soil raised in arcs by the force of impact. Ironsoil-brown and steel-grey palette.

Mood: mass as doctrine. The Breaker does not aim — they flatten. Pixel-art HD-2D; hand-drawn illustration sensibility; isekai-game-coded.
```

---

### Kit S2-05 — Rampart, the Ironsoil Crusher (Physical/Flat/STR)

**Kit ID:** S1_endgame_bc_melee_high_flat_str_none_s1
**Canonical name:** Rampart, the Ironsoil Crusher
**Faction:** Ironsoil Vanguard (Cluster 2)
**Substrate axes:** close/melee | high tempo | flat amplitude | STR
**Kit narrative:** "A relentless STR-driven brawler who closes ground at high tempo and delivers flat, sustained devastation through wide-arc melee — no burst, no range, just compounding earthen pressure. Rampart is the body that becomes terrain."

**Word count:** 129 | Style-adherence: PASS | D7 compliance: PASS

```
INDIVIDUAL PORTRAIT — Rampart, the Ironsoil Crusher
Season: cycle-14-wave-5-season-002
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy art direction; isekai-genre-readable; NOT retro pixel-art

European medieval heavy fighter — Rampart — mid-charge, shoulders lowered, a battering force in motion. The body itself IS the weapon: mass accumulated into forward momentum, wide-arc arms delivering flat, compounding devastation at melee reach. The soil beneath their feet is churned by movement; earth-force amplifies each blow's wide sweep. No burst, no flash — only the relentless geometry of mass meeting ground. Iron-dark armor, earthen-brown crust on every surface. Cracked-ground impact markers radiate outward from each foot-plant.

Mood: the body as terrain. Rampart does not break through defenses — they become the landscape those defenses were built around. Pixel-art HD-2D; hand-drawn illustration sensibility; isekai-game-coded.
```

---

### Kit S2-06 — Ironsoil Breaker, Spikewarden of Gravel (Physical/Spiky/STR)

**Kit ID:** S1_endgame_bc_melee_low_spiky_str_none_s0
**Canonical name:** Ironsoil Breaker, Spikewarden of Gravel
**Faction:** Ironsoil Vanguard (Cluster 2)
**Substrate axes:** close/melee | low tempo | spiky amplitude | STR
**Kit narrative:** "A slow-building STR combatant who plants wide and erupts in sudden crushing arcs, turning low-tempo ground pressure into punishing spikes of close-range force. Every engagement is a contest of mass — the Breaker absorbs the earth beneath and returns it as ruin."

**Word count:** 131 | Style-adherence: PASS | D7 compliance: PASS

```
INDIVIDUAL PORTRAIT — Ironsoil Breaker, Spikewarden of Gravel
Season: cycle-14-wave-5-season-002
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy art direction; isekai-genre-readable; NOT retro pixel-art

A European medieval STR fighter at the precise moment of spike-release: the long accumulation has ended, the eruption is NOW. Gravel and earth burst upward from the impact zone. The figure is braced wide, low stance, arms at full extension in a wide crushing arc — the energy of many slow moments detonating in a single spiky blow. The ground itself appears to participate: gravel sprays, soil rises, the earth returns the force it absorbed. Iron-grey and earthen-amber palette; impact burst at the center of the frame. Low-tempo stillness visible in the fighter's braced posture: they held; they held; and now they release.

Mood: patient mass made sudden. Pixel-art HD-2D; hand-drawn illustration sensibility; isekai-game-coded.
```

---

### Kit S2-07 — Rampart Breaker of Ashfeld (Physical/Variable/STR)

**Kit ID:** S1_endgame_bc_melee_medium_variable_str_none_s0
**Canonical name:** Rampart Breaker of Ashfeld
**Faction:** Ironsoil Vanguard (Cluster 2)
**Substrate axes:** close/melee | medium tempo | variable amplitude | STR
**Kit narrative:** "A STR-driven melee combatant whose variable tempo mirrors the unpredictable surge of a battering charge — weight committed fully, arc wide, ground claimed by sheer bodily force."

**Word count:** 123 | Style-adherence: PASS | D7 compliance: PASS

```
INDIVIDUAL PORTRAIT — Rampart Breaker of Ashfeld
Season: cycle-14-wave-5-season-002
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy art direction; isekai-genre-readable; NOT retro pixel-art

A medium-tempo European medieval STR fighter mid-charge across ashen ground, weight fully committed, variable arc unpredictable — a battering approach that adjusts angle mid-strike based on whatever ground remains. Ashfeld battlefield behind them: dark soil, sparse burnt grass, overcast sky. The charge is wide, low, body-first. Impact zone ahead reads as crushed geometry — the Breaker has already passed through this ground before. Iron-plate armor, ash-grey palette, variable arc visible in the asymmetry of the swing.

Mood: ground claimed by bodily force. No finesse, no range. Weight as the only argument. Pixel-art HD-2D; hand-drawn illustration sensibility; isekai-game-coded.
```

---

### Kit S2-08 — Ironsoil Warden of Broken Ground (Physical/Variable/STR)

**Kit ID:** S1_endgame_bc_melee_medium_variable_str_none_s1
**Canonical name:** Ironsoil Warden of Broken Ground
**Faction:** Ironsoil Vanguard (Cluster 2)
**Substrate axes:** close/melee | medium tempo | variable amplitude | STR
**Kit narrative:** "A STR-driven melee fighter who reads the terrain beneath every engagement, shifting weight and arc mid-stride to crush opponents across variable distances. Footing is both weapon and fortress."

**Word count:** 127 | Style-adherence: PASS | D7 compliance: PASS

```
INDIVIDUAL PORTRAIT — Ironsoil Warden of Broken Ground
Season: cycle-14-wave-5-season-002
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy art direction; isekai-genre-readable; NOT retro pixel-art

A European medieval STR fighter reading the broken ground beneath every footfall, mid-stride, arc shifting as terrain shifts. The broken ground itself is the weapon: uneven footing is exploited, not avoided — the Warden's stance adjusts mid-swing to redirect mass through whatever crack or slope presents. Variable amplitude visible in the offset weight: this strike will not land the same way as the last. Crumbled earth, broken stone slabs, iron-dark armor caked with soil. Earthen-amber and steel-grey palette.

Mood: terrain-intelligence in a melee fighter. The ground is both obstacle and fortress. Pixel-art HD-2D; hand-drawn illustration sensibility; isekai-game-coded.
```

---

### Kit S2-09 — Earthen Warden of the Broken Furrow (Earth/Variable/WIS)

**Kit ID:** S1_endgame_bc_melee_high_variable_wis_none_s0
**Canonical name:** Earthen Warden of the Broken Furrow
**Faction:** Ironsoil Vanguard (Cluster 2)
**Substrate axes:** close/melee | high tempo | variable amplitude | WIS
**Kit narrative:** "A WIS-driven melee striker whose tempo surges in unpredictable bursts, the Earthen Warden reads the ground beneath every exchange — shifting weight and footing to redirect force rather than simply absorb it. Weaponizes terrain itself."

**Word count:** 128 | Style-adherence: PASS | D7 compliance: PASS

```
INDIVIDUAL PORTRAIT — Earthen Warden of the Broken Furrow
Season: cycle-14-wave-5-season-002
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy art direction; isekai-genre-readable; NOT retro pixel-art

A WIS-driven European medieval melee fighter in a broken furrow, terrain reading visible in the deliberateness of their footing: they have chosen THIS ground. Mid-variable-burst, a sudden high-tempo strike launches from stillness — the burst caught at peak. Earth rises in chunks from the furrow beneath the strike, redirected force visible as earth-pressure erupting sideways. Variable amplitude: last blow was light; this one is full earthen weight. WIS over STR: the face shows calculation, not brute effort. Earthen-amber and muted-sage-green palette; cracked furrow close-up.

Mood: intelligence as earthen force. The furrow chose the Warden as much as the Warden chose it. Pixel-art HD-2D; hand-drawn illustration sensibility; isekai-game-coded.
```

---

### Kit S2-10 — Earthen Sage of the Broken Ridge (Earth/Variable/WIS)

**Kit ID:** S1_endgame_bc_melee_medium_variable_wis_none_s1
**Canonical name:** Earthen Sage of the Broken Ridge
**Faction:** Ironsoil Vanguard (Cluster 2)
**Substrate axes:** close/melee | medium tempo | variable amplitude | WIS
**Kit narrative:** "A WIS-driven melee fighter whose variable tempo reads the ground beneath each clash, shifting weight and stance to redirect mass rather than simply absorb it. A continental lineage folded into the faction's close-quarters devastation."

**Word count:** 132 | Style-adherence: PASS | D7 compliance: PASS

```
INDIVIDUAL PORTRAIT — Earthen Sage of the Broken Ridge
Season: cycle-14-wave-5-season-002
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy art direction; isekai-genre-readable; NOT retro pixel-art

A measured European medieval melee fighter at the edge of a broken ridge, stance wide, weight balanced between two different elevations. WIS visible in posture: they have read this ridge before the first blow. Mid variable-amplitude strike — the arc redirects earthen force DOWN the ridge rather than straight out, using elevation as multiplier. Medium tempo: not hurried, not slow. The rock face behind them is fractured from prior engagements; the ground has been read and used. Stone-grey and earthen-brown palette; broken ridge framing.

Mood: patience as doctrine. The ridge is a collaborator, not a backdrop. Pixel-art HD-2D; hand-drawn illustration sensibility; isekai-game-coded.
```

---

### Kit S2-11 — Loam Sage of the Broken Ridge (Earth/Variable/WIS — mid)

**Kit ID:** S1_endgame_bc_mid_medium_variable_wis_none_s2
**Canonical name:** Loam Sage of the Broken Ridge
**Faction:** Ironsoil Vanguard (Cluster 2)
**Substrate axes:** mid-range | medium tempo | variable amplitude | WIS
**Kit narrative:** "Where the Ironsoil Vanguard's weight meets measured ground-reading, this fighter reads shifting terrain through patient mid-range presence, redirecting earthen mass with deliberate variable timing rather than brute initiation."

**Word count:** 130 | Style-adherence: PASS | D7 compliance: PASS

```
INDIVIDUAL PORTRAIT — Loam Sage of the Broken Ridge
Season: cycle-14-wave-5-season-002
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy art direction; isekai-genre-readable; NOT retro pixel-art

A European medieval mid-range ground-reader, positioned mid-field on cracked loam, redirecting earthen mass from a tactical remove. Not a brawler — a director of mass. Variable timing: mid-release caught between accumulation and delivery, the timing deliberate not reactive. Loam rises in slow plumes around their feet; mid-range earthen force does not explode but travels as rolling ground-pressure outward. Staff-assisted posture; WIS over brute STR. Loam-tan and muted-olive palette; broken ridge and cracked lowland soil behind them.

Mood: wisdom over impulse. The ridge underfoot is obstacle and weapon both, turned by one who calculates before the crush lands. Pixel-art HD-2D; hand-drawn illustration sensibility; isekai-game-coded.
```

---

### Kit S2-12 — Dustwarden of the Broken Furrow (Earth/Variable/WIS — ranged)

**Kit ID:** S1_endgame_bc_ranged_medium_variable_wis_none_s0
**Canonical name:** Dustwarden of the Broken Furrow
**Faction:** Ironsoil Vanguard (Cluster 2)
**Substrate axes:** ranged | medium tempo | variable amplitude | WIS
**Kit narrative:** "The Dustwarden reads the ground at distance — gauging slope, choke, and crumbling earth to call strikes that arrive variable and late, denying the enemy solid footing before the crush lands. Wisdom over brute tempo."

**Word count:** 128 | Style-adherence: PASS | D7 compliance: PASS

```
INDIVIDUAL PORTRAIT — Dustwarden of the Broken Furrow
Season: cycle-14-wave-5-season-002
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy art direction; isekai-genre-readable; NOT retro pixel-art

A European medieval ranged fighter standing at distance from a broken furrow, arm raised in a ranged earth-call gesture. They do not rush forward — they read the ground ahead, gauging slope and choke before the earthen strike arrives. Mid-release: dust rises in the far ground before the striker has visibly acted, the strike arriving late and off-angle to deny solid footing. Variable amplitude: the delay was tactical. WIS-driven posture — steady, calculating, never urgent. Dust-tan and stone-grey palette; broken furrow terrain stretching toward horizon.

Mood: terrain disruption at distance. Footing is denied before the Vanguard's close work begins. Pixel-art HD-2D; hand-drawn illustration sensibility; isekai-game-coded.
```

---

## FACTION 3 — GALE-BLESSED WARDENS (13 kits)

---

### Kit S2-13 — Windreave of Veldmoor (Wind/Flat/DEX — melee)

**Kit ID:** S1_endgame_bc_melee_high_flat_dex_none_s0
**Canonical name:** Windreave of Veldmoor
**Faction:** Gale-Blessed Wardens (Cluster 3)
**Substrate axes:** close/melee | high tempo | flat amplitude | DEX
**Kit narrative:** "The Windreave fights at a relentless, even tempo — sweeping wide arcs of wind-pressure through close quarters with the unhurried consistency of a moorland gale that never fully breaks."

**Word count:** 127 | Style-adherence: PASS | D7 compliance: PASS

```
INDIVIDUAL PORTRAIT — Windreave of Veldmoor
Season: cycle-14-wave-5-season-002
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy art direction; isekai-genre-readable; NOT retro pixel-art

A DEX-driven close-quarters fighter on a windswept moorland, blades or wind-channeling tools in both hands, mid-wide-arc sweep. High tempo visible in the blur of motion: this is frame N of many equal frames, each carrying the same weight. No surge, no lull. Wind-pressure trails extend from both arms, sweeping laterally across the close-quarters space — not targeted but covering. Flat amplitude: consistent, even, unhurried. Fantasy-generic medieval armor: light, travel-worn, wind-streaked. Wind-teal and moorland-grey palette; veldmoor fog in the background.

Mood: the gale that never fully breaks. Relentless lateral coverage rather than decisive single blow. Pixel-art HD-2D; hand-drawn illustration sensibility; isekai-game-coded.
```

---

### Kit S2-14 — Dextrous Warden of the Gale Front (Holy/Flat/DEX — melee)

**Kit ID:** S1_endgame_bc_melee_high_flat_dex_none_s1
**Canonical name:** Dextrous Warden of the Gale Front
**Faction:** Gale-Blessed Wardens (Cluster 3)
**Substrate axes:** close/melee | high tempo | flat amplitude | DEX
**Kit narrative:** "A swift, close-quarters fighter whose flat, relentless tempo carries holy force across wide fronts in broad, sweeping arcs — elemental pressure of wind and sanctified motion doing the work. Flows laterally, filling gaps with high-frequency DEX-driven cuts."

**Word count:** 132 | Style-adherence: PASS | D7 compliance: PASS

```
INDIVIDUAL PORTRAIT — Dextrous Warden of the Gale Front
Season: cycle-14-wave-5-season-002
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy art direction; isekai-genre-readable; NOT retro pixel-art

A swift fantasy-generic medieval close-quarters fighter mid-lateral-flow across a wide defensive front, holy light bleeding from the arc of their sweeping motion. DEX governs every movement: they do not anchor, they drift the engagement line, high-frequency cuts filling every gap the wind opens. Flat amplitude: each cut carries the same sanctified weight. Holy-pale-gold light traces the arc behind them; wind-teal ambient force moves with the body. Light medieval armor, mobile build. Open front behind them shows the width of their coverage.

Mood: presence as defense. The front holds through motion, not mass. Pixel-art HD-2D; hand-drawn illustration sensibility; isekai-game-coded.
```

---

### Kit S2-15 — Duskward, the Gale-Blind Warden (Shadow/Flat/INT — melee)

**Kit ID:** S1_endgame_bc_melee_high_flat_int_none_s0
**Canonical name:** Duskward, the Gale-Blind Warden
**Faction:** Gale-Blessed Wardens (Cluster 3)
**Substrate axes:** close/melee | high tempo | flat amplitude | INT
**Kit narrative:** "A melee fighter whose intellect-driven read of wind and shadow lets him close gaps with flat, relentless pressure, smothering the front line before opponents can widen their stance. Folds the sweep inward, using ambient elemental weight to compress rather than scatter."

**Word count:** 131 | Style-adherence: PASS | D7 compliance: PASS

```
INDIVIDUAL PORTRAIT — Duskward, the Gale-Blind Warden
Season: cycle-14-wave-5-season-002
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy art direction; isekai-genre-readable; NOT retro pixel-art

An INT-driven melee fighter advancing into close quarters with measured, flat pressure — shadow trailing in folds rather than exploding outward. Where other Wardens sweep wide, Duskward compresses inward: the arc pulls toward the center, smothering rather than scattering. High tempo but controlled — relentless forward compression. The gale-blind element: they close their eyes to wind and read shadow instead, folding ambient elemental weight into tight melee force. Shadow-violet and muted-grey palette; hints of wind-teal absorbed into the shadow folds.

Mood: compression over scatter. Intellect turning gale into a smothering grip. Pixel-art HD-2D; hand-drawn illustration sensibility; isekai-game-coded.
```

---

### Kit S2-16 — Tidewarden of the Broad Current (Water/Flat/INT — melee)

**Kit ID:** S1_endgame_bc_melee_high_flat_int_none_s1
**Canonical name:** Tidewarden of the Broad Current
**Faction:** Gale-Blessed Wardens (Cluster 3)
**Substrate axes:** close/melee | high tempo | flat amplitude | INT
**Kit narrative:** "A melee combatant whose water-attuned intellect drives sweeping close-quarters strikes across wide fronts, reading the pressure and flow of each engagement. Flat, sustained tempo marks them as a dependable line-holder."

**Word count:** 127 | Style-adherence: PASS | D7 compliance: PASS

```
INDIVIDUAL PORTRAIT — Tidewarden of the Broad Current
Season: cycle-14-wave-5-season-002
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy art direction; isekai-genre-readable; NOT retro pixel-art

A melee Warden whose water-attuned INT drives broad sweeping strikes along a wide front. Mid-flat-tempo strike: water-force flows laterally from the arc, not exploding but spreading, steady as a tidal current pressing against open ground. The fighter reads the pressure of the engagement — body posture suggests flow-reading, not force-assertion. Dependable line-holder: their position in the scene reads as structural, a current that cannot be interrupted. Water-blue and grey-green palette; wide front visible behind them as an open field.

Mood: sustained pressure over force. The current does not stop. Pixel-art HD-2D; hand-drawn illustration sensibility; isekai-game-coded.
```

---

### Kit S2-17 — Gale Warden of the Rushing Peak (Wind/Variable/WIS — melee)

**Kit ID:** S1_endgame_bc_melee_high_variable_wis_none_s2
**Canonical name:** Gale Warden of the Rushing Peak
**Faction:** Gale-Blessed Wardens (Cluster 3)
**Substrate axes:** close/melee | high tempo | variable amplitude | WIS
**Kit narrative:** "A high-tempo melee fighter whose variable sweeping strikes ride wind currents with disciplined intuition, reading the battlefield's shifting pressure rather than any fixed sequence. Unpredictable in arc, wide in reach, grounded in elemental geometry."

**Word count:** 133 | Style-adherence: PASS | D7 compliance: PASS

```
INDIVIDUAL PORTRAIT — Gale Warden of the Rushing Peak
Season: cycle-14-wave-5-season-002
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy art direction; isekai-genre-readable; NOT retro pixel-art

A high-tempo melee fighter at a mountain pass summit, mid-variable-arc sweep — the wind behind them is not mere backdrop, it is collaborator. This blow is wider than the last; the next will be different again. WIS-intuition readable in the gaze: already tracking the next pressure shift. Wind-force visible as rushing air-currents sweeping with the arc. Fantasy-generic medieval, light mountain-travel armor, wind-blown cloak. Mountain-peak framing: altitude, cold air, sudden gusts. Wind-teal and mountain-grey palette.

Mood: the gust through a mountain pass — unpredictable in arc, wide in reach, sudden and grounded both. Pixel-art HD-2D; hand-drawn illustration sensibility; isekai-game-coded.
```

---

### Kit S2-18 — Windreader of the Open March (Wind/Variable/WIS — melee medium)

**Kit ID:** S1_endgame_bc_melee_medium_variable_wis_none_s0
**Canonical name:** Windreader of the Open March
**Faction:** Gale-Blessed Wardens (Cluster 3)
**Substrate axes:** close/melee | medium tempo | variable amplitude | WIS
**Kit narrative:** "A wandering Warden whose wide-arc melee technique reads shifting air pressure mid-swing, adjusting strike amplitude on the fly to match whatever front the wind opens. Each blow lands when the gale says so, not before."

**Word count:** 128 | Style-adherence: PASS | D7 compliance: PASS

```
INDIVIDUAL PORTRAIT — Windreader of the Open March
Season: cycle-14-wave-5-season-002
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy art direction; isekai-genre-readable; NOT retro pixel-art

A wandering fantasy-generic medieval Warden on open march ground, mid-wide-arc melee strike — paused in the moment of amplitude-read, feeling for the wind before committing full force. Variable amplitude: this blow's size is not predetermined. Wind-currents visible as ambient pressure patterns shifting across the open field, the fighter's arc adjusting mid-swing to match them. Medium tempo: neither hurried nor slow; each blow waits for the right gust. Open march landscape: rolling grey-green meadow, distant storm bank. Wind-teal palette.

Mood: the wind governs timing. The fighter does not swing — they listen, then swing. Pixel-art HD-2D; hand-drawn illustration sensibility; isekai-game-coded.
```

---

### Kit S2-19 — Tidewarden of the Pale Crossing (Holy/Variable/WIS — mid)

**Kit ID:** S1_endgame_bc_mid_medium_variable_wis_none_s0
**Canonical name:** Tidewarden of the Pale Crossing
**Faction:** Gale-Blessed Wardens (Cluster 3)
**Substrate axes:** mid-range | medium tempo | variable amplitude | WIS
**Kit narrative:** "A mid-range holy fighter whose variable tempo reflects the unpredictable surge of sanctified wind across open ground. Her WIS-rooted timing is shaped by the same ambient convergence that binds the fellowship's wide-front geometry."

**Word count:** 131 | Style-adherence: PASS | D7 compliance: PASS

```
INDIVIDUAL PORTRAIT — Tidewarden of the Pale Crossing
Season: cycle-14-wave-5-season-002
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy art direction; isekai-genre-readable; NOT retro pixel-art

A mid-range holy fighter at a pale crossing point — stone ford, open ground, pale sky — arms spread in a wide variable-amplitude release of sanctified force. Holy light sweeps outward in broad arcs, not targeted but covering the full front geometry. Variable tempo: the release is unscheduled, caught between accumulation and dispersal. WIS-rooted posture: she waits for the ambient wind-surge to tell her the moment. Pale-gold and wind-teal palette; crossing stone below catches the light of the holy arc.

Mood: sanctified pressure without ceremony. The discipline is absorbed from the ambient, not imposed by doctrine. Pixel-art HD-2D; hand-drawn illustration sensibility; isekai-game-coded.
```

---

### Kit S2-20 — Tidewarden of the Flat Shore (Water/Flat/DEX — mid)

**Kit ID:** S1_endgame_bc_mid_high_flat_dex_none_s0
**Canonical name:** Tidewarden of the Flat Shore
**Faction:** Gale-Blessed Wardens (Cluster 3)
**Substrate axes:** mid-range | high tempo | flat amplitude | DEX
**Kit narrative:** "A dexterous mid-range fighter whose water-attuned sweeps sustain relentless tempo across wide fronts, each movement flowing without peak or break like a tide pressing steadily against open ground."

**Word count:** 127 | Style-adherence: PASS | D7 compliance: PASS

```
INDIVIDUAL PORTRAIT — Tidewarden of the Flat Shore
Season: cycle-14-wave-5-season-002
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy art direction; isekai-genre-readable; NOT retro pixel-art

A DEX-driven mid-range fighter on a flat shoreline, water-attuned sweeps spreading laterally across the open front in low, unbroken waves. High flat tempo: frame N of many identical frames, each carrying the same tidal weight. The wide front is held not through force but through relentless coverage — the tide presses and does not recede. Fantasy-generic medieval armor; water-blue and flat-grey palette; flat shore extending wide behind the fighter. Constant lateral motion visible in the water-wake patterns.

Mood: the tide that holds. No peak, no break. Wide coverage through tireless DEX-driven presence. Pixel-art HD-2D; hand-drawn illustration sensibility; isekai-game-coded.
```

---

### Kit S2-21 — Driftcaller of the Open Reach (Wind/Flat/DEX — mid)

**Kit ID:** S1_endgame_bc_mid_high_flat_dex_none_s2
**Canonical name:** Driftcaller of the Open Reach
**Faction:** Gale-Blessed Wardens (Cluster 3)
**Substrate axes:** mid-range | high tempo | flat amplitude | DEX
**Kit narrative:** "A swift-footed Warden who fights at a measured distance, reading wind shifts to time wide, flat arcs of force that press across the full breadth of a contested front. Never anchoring long enough for the gale to leave them."

**Word count:** 130 | Style-adherence: PASS | D7 compliance: PASS

```
INDIVIDUAL PORTRAIT — Driftcaller of the Open Reach
Season: cycle-14-wave-5-season-002
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy art direction; isekai-genre-readable; NOT retro pixel-art

A swift fantasy-generic medieval mid-range fighter in constant lateral drift across an open contested front, mid-flat-arc wind release. They have not anchored: footwork shows they were at a different position a moment ago and will be somewhere else shortly. Wind force sweeps wide from the arc — the full breadth of the front covered by a single drifting pass. DEX governs distance-keeping: never too close, never too far. High flat tempo: each drift-and-release carries equal weight. Open reach behind them; wind-teal and pale-sky palette.

Mood: the wind as corridor. The Driftcaller occupies the full width through lateral presence, never fixed. Pixel-art HD-2D; hand-drawn illustration sensibility; isekai-game-coded.
```

---

### Kit S2-22 — Stormcaller of the Open Reach (Lightning/Flat/DEX — ranged)

**Kit ID:** S1_endgame_bc_ranged_high_flat_dex_none_s0
**Canonical name:** Stormcaller of the Open Reach
**Faction:** Gale-Blessed Wardens (Cluster 3)
**Substrate axes:** ranged | high tempo | flat amplitude | DEX
**Kit narrative:** "A ranged Warden who releases sustained volleys of lightning across wide fronts, her DEX-driven cadence matching the faction's sweeping geometry without pause or surge — flat pressure delivered at range."

**Word count:** 128 | Style-adherence: PASS | D7 compliance: PASS

```
INDIVIDUAL PORTRAIT — Stormcaller of the Open Reach
Season: cycle-14-wave-5-season-002
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy art direction; isekai-genre-readable; NOT retro pixel-art

A ranged Warden at the defensive edge of an open front, sustained lightning volleys spreading wide from raised hands. Flat tempo: no surge, no pause. The volley is mid-stream in a continuous delivery, DEX-driven cadence keeping the arc steady and wide. Lightning does not converge on a single point — it spreads, matching the wide-front geometry of the fellowship. Fantasy-generic medieval; light armor, mobile build. Lightning-gold and wind-teal palette; open front visible across the scene's full width.

Mood: relentless ranged coverage. The arc does not stop. Pixel-art HD-2D; hand-drawn illustration sensibility; isekai-game-coded.
```

---

### Kit S2-23 — Windcaller of the Open Reach (Wind/Variable/WIS — ranged)

**Kit ID:** S1_endgame_bc_ranged_medium_variable_wis_none_s1
**Canonical name:** Windcaller of the Open Reach
**Faction:** Gale-Blessed Wardens (Cluster 3)
**Substrate axes:** ranged | medium tempo | variable amplitude | WIS
**Kit narrative:** "A ranging Warden who reads the shifting pressure of wind and holy resonance to deliver sweeping force across variable distances, adjusting the arc and weight of each release to match the breadth of the front."

**Word count:** 131 | Style-adherence: PASS | D7 compliance: PASS

```
INDIVIDUAL PORTRAIT — Windcaller of the Open Reach
Season: cycle-14-wave-5-season-002
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy art direction; isekai-genre-readable; NOT retro pixel-art

A ranging fantasy-generic medieval Warden mid-release, wind-arc sweeping outward at a variable distance — wider than expected, or narrower, depending on what the ambient pressure demanded at the moment of release. WIS-intuition visible: the gaze tracks the arc's path, reading whether the front's thinnest point was found. Holy resonance bleeds pale-gold through the wind-teal arc, sanctifying the sweep without ceremony. Open reach extending behind them, the front's breadth visible. Medium variable tempo: unscheduled release.

Mood: the arc adjusted to the front, not the other way. Elemental convergence in service of coverage. Pixel-art HD-2D; hand-drawn illustration sensibility; isekai-game-coded.
```

---

### Kit S2-24 — Tidecaller of the Open Reach (Water/Variable/INT — ranged)

**Kit ID:** S1_endgame_bc_ranged_medium_variable_int_none_s0
**Canonical name:** Tidecaller of the Open Reach
**Faction:** Gale-Blessed Wardens (Cluster 3)
**Substrate axes:** ranged | medium tempo | variable amplitude | INT
**Kit narrative:** "A ranged Warden who reads the variable pressure of water and wind across wide fronts, loosing arcing torrents that shift in weight and angle with each breath of ambient current."

**Word count:** 126 | Style-adherence: PASS | D7 compliance: PASS

```
INDIVIDUAL PORTRAIT — Tidecaller of the Open Reach
Season: cycle-14-wave-5-season-002
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy art direction; isekai-genre-readable; NOT retro pixel-art

An INT-driven ranged Warden mid-release of a water-arc torrent that bends and shifts in angle as ambient wind currents redirect it. The torrent is not a straight beam — it curves, adjusting weight and spread with each breath of elemental current. Variable amplitude readable in the shifting width of the water-arc. The fighter reads the current rather than forcing it. Water-blue and wind-teal palette; open front below; the arc's path visibly curved, not linear.

Mood: the torrent that reads the current and rides it. INT governs where the water goes, not force. Pixel-art HD-2D; hand-drawn illustration sensibility; isekai-game-coded.
```

---

### Kit S2-25 — Gale-Blessed Physical Fighter Bearer (Physical/Flat/DEX — ranged fallback)

**Kit ID:** S1_endgame_bc_ranged_high_flat_dex_none_s2
**Canonical name:** Gale-Blessed Physical Fighter Bearer
**Faction:** Gale-Blessed Wardens (Cluster 3)
**Substrate axes:** ranged | high tempo | flat amplitude | DEX | physical
**Kit narrative:** "A physical-aligned fighter bearer from the fantasy-generic lineage of the Gale-Blessed Wardens faction, whose identity was substrate-derived after LLM naming failed." (FALLBACK_SUBSTRATE_DERIVED status noted; prompt authored from raw substrate)

**Word count:** 128 | Style-adherence: PASS | D7 compliance: PASS

```
INDIVIDUAL PORTRAIT — Gale-Blessed Physical Fighter Bearer
Season: cycle-14-wave-5-season-002
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy art direction; isekai-genre-readable; NOT retro pixel-art

A DEX-driven ranged Warden delivering sustained flat physical-force volleys across a wide front — not elemental, not sanctified, but raw kinetic pressure at high consistent tempo. Fantasy-generic medieval build, light mobile armor, bow or hurled-force release. Flat amplitude: every volley equal. The physical force reads as the faction's pragmatic undercurrent — not every Warden channels wind or water; some simply hit. Wide front behind them; high flat cadence visible in the rapid-fire posture. Muted-grey and earthy-tan palette against open green field.

Mood: physical pragmatism inside an elemental fellowship. The covering arc holds regardless of element. Pixel-art HD-2D; hand-drawn illustration sensibility; isekai-game-coded.
```

---

## FACTION 4 — DUSKCHAIN RANGING COMPACT (8 kits)

---

### Kit S2-26 — Duskchain Hexer of the Pale Margin (Shadow/Spiky/INT — mid)

**Kit ID:** S1_endgame_bc_mid_low_spiky_int_none_s0
**Canonical name:** Duskchain Hexer of the Pale Margin
**Faction:** Duskchain Ranging Compact (Cluster 4)
**Substrate axes:** mid-range | low tempo | spiky amplitude | INT
**Kit narrative:** "A slow-burning intelligence operative who coils shadow-threaded pressure across mid-range engagements, releasing it in sudden, spiky bursts that collapse enemy footing before steel is ever drawn."

**Word count:** 131 | Style-adherence: PASS | D7 compliance: PASS

```
INDIVIDUAL PORTRAIT — Duskchain Hexer of the Pale Margin
Season: cycle-14-wave-5-season-002
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy art direction; isekai-genre-readable; NOT retro pixel-art

An INT-driven mid-range operative at the grey margin of a frontier zone, shadow threads coiled around their hands in slow spiraling accumulation. Low tempo: they have been holding this charge. The spike is imminent: shadow pressure is at maximum coil, about to release. The burst-point visible ahead: a compact spot in the mid-ground where the chain will detonate. Fantasy-generic medieval caster robes; pale margin framing — sparse trees, failing light. Shadow-violet and pale-grey palette; the coil's purple density contrasts the washed-out background.

Mood: patience as instrument. The hex is the ledger; the burst is the collection. Pixel-art HD-2D; hand-drawn illustration sensibility; isekai-game-coded.
```

---

### Kit S2-27 — Stormbreak Ranger of the Pale Verge (Lightning/Spiky/DEX)

**Kit ID:** S1_endgame_bc_ranged_low_spiky_dex_none_s0
**Canonical name:** Stormbreak Ranger of the Pale Verge
**Faction:** Duskchain Ranging Compact (Cluster 4)
**Substrate axes:** ranged | low tempo | spiky amplitude | DEX
**Kit narrative:** "A patient frontier striker who holds position until a single dexterous release cracks the chain open with a lightning-threaded spike — low tempo, then sudden overwhelming discharge."

**Word count:** 128 | Style-adherence: PASS | D7 compliance: PASS

```
INDIVIDUAL PORTRAIT — Stormbreak Ranger of the Pale Verge
Season: cycle-14-wave-5-season-002
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy art direction; isekai-genre-readable; NOT retro pixel-art

A DEX-driven frontier ranger at the pale verge of a dark forest, mid-lightning-spike release — the stillness that preceded it visible in their stance: they waited until this exact moment. Single decisive dexterous release, lightning threading through the chain in a single overwhelming discharge. The chain pattern visible: darkness threaded between prior targets, the lightning spike detonating along the chain's path. Fantasy-generic medieval ranger; muted frontier gear. Lightning-gold detonation point against shadow-dark forest verge; pale grey sky above.

Mood: patience, then detonation. The storm does what shadow started. Pixel-art HD-2D; hand-drawn illustration sensibility; isekai-game-coded.
```

---

### Kit S2-28 — Duskchain Striker of Hollow Margins (Shadow/Spiky/DEX)

**Kit ID:** S1_endgame_bc_ranged_low_spiky_dex_none_s1
**Canonical name:** Duskchain Striker of Hollow Margins
**Faction:** Duskchain Ranging Compact (Cluster 4)
**Substrate axes:** ranged | low tempo | spiky amplitude | DEX
**Kit narrative:** "A patient frontier ranger who holds position in shadow until a single opportune strike detonates across the chain — low tempo, devastating amplitude, no wasted pressure. She threads darkness between engagements."

**Word count:** 129 | Style-adherence: PASS | D7 compliance: PASS

```
INDIVIDUAL PORTRAIT — Duskchain Striker of Hollow Margins
Season: cycle-14-wave-5-season-002
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy art direction; isekai-genre-readable; NOT retro pixel-art

A patient DEX-driven frontier ranger barely visible in the shadow margin of hollow terrain — only their silhouette and the shadow-thread extending from their hand marks their position. The thread connects to a detonation point ahead: the chain is primed. Spiky amplitude burst caught at peak — the one strike after long silence. No wasted pressure: shadow consumed in accumulation, now released in full. Dark hollow framing: deep shadows, sparse light. Shadow-violet and hollow-dark palette; the single detonation point is the only lit element in the scene.

Mood: darkness as patience made devastating. Pixel-art HD-2D; hand-drawn illustration sensibility; isekai-game-coded.
```

---

### Kit S2-29 — Duskchain Hexer of the Pale Verge (Shadow/Spiky/INT)

**Kit ID:** S1_endgame_bc_ranged_low_spiky_int_none_s0
**Canonical name:** Duskchain Hexer of the Pale Verge
**Faction:** Duskchain Ranging Compact (Cluster 4)
**Substrate axes:** ranged | low tempo | spiky amplitude | INT
**Kit narrative:** "A shadow-threaded intelligence operative who holds fire until the chain is primed, then releases a single devastating burst that unravels multiple targets across the frontier's grey margins."

**Word count:** 133 | Style-adherence: PASS | D7 compliance: PASS

```
INDIVIDUAL PORTRAIT — Duskchain Hexer of the Pale Verge
Season: cycle-14-wave-5-season-002
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy art direction; isekai-genre-readable; NOT retro pixel-art

An INT-operative standing at a pale frontier verge, shadow-threads seeded across the mid-ground in a web of accumulated pressure. They hold: not yet. The chain is primed but not released. The burst is visible as imminent: shadow-violet energy coiled at the release point, structure already loaded. Low tempo: the operative has been here longer than anyone watching has noticed. Fantasy-generic medieval operative robes; grey verge terrain. Shadow-violet and pale frontier-grey palette; the web of threads is the visual subject.

Mood: structural work before steel ever moves. The hex is the architecture; the burst is demolition. Pixel-art HD-2D; hand-drawn illustration sensibility; isekai-game-coded.
```

---

### Kit S2-30 — Duskchain Striker of the Gaunt Reach (Physical/Spiky/STR)

**Kit ID:** S1_endgame_bc_ranged_low_spiky_str_none_s0
**Canonical name:** Duskchain Striker of the Gaunt Reach
**Faction:** Duskchain Ranging Compact (Cluster 4)
**Substrate axes:** ranged | low tempo | spiky amplitude | STR
**Kit narrative:** "A patient frontier ranger who holds position at the edge of shadow, releasing devastating bursts of physical force only when the chain of pressure has fully loaded — each strike lands like a deferred debt."

**Word count:** 129 | Style-adherence: PASS | D7 compliance: PASS

```
INDIVIDUAL PORTRAIT — Duskchain Striker of the Gaunt Reach
Season: cycle-14-wave-5-season-002
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy art direction; isekai-genre-readable; NOT retro pixel-art

A STR-driven frontier ranger at the gaunt edge of a shadow-dark reach, physical-force release at spiky peak — the deferred debt paid in full. The striker is larger than others in the Compact: physical force demands STR. The single blow is massive in amplitude, physical-kinetic impact crater ahead. Shadow accumulated along the chain's length; physical force detonates at the chain's end-node. Gaunt reach terrain: bare trees, dark soil, grey stone. Shadow-dark and steel-grey palette; the physical-burst point is the scene's kinetic center.

Mood: the long interval ending in one overwhelming answer. Pixel-art HD-2D; hand-drawn illustration sensibility; isekai-game-coded.
```

---

### Kit S2-31 — Duskchain Striker of the Pale Margin (Physical/Spiky/STR — s2)

**Kit ID:** S1_endgame_bc_ranged_low_spiky_str_none_s2
**Canonical name:** Duskchain Striker of the Pale Margin
**Faction:** Duskchain Ranging Compact (Cluster 4)
**Substrate axes:** ranged | low tempo | spiky amplitude | STR
**Kit narrative:** "A frontier-ranging brawler who holds position in the grey edges of engagement, coiling strength into infrequent but punishing strikes that detonate through the chain when the moment finally breaks. Shadow and patience load the blow that steel delivers."

**Word count:** 127 | Style-adherence: PASS | D7 compliance: PASS

```
INDIVIDUAL PORTRAIT — Duskchain Striker of the Pale Margin
Season: cycle-14-wave-5-season-002
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy art direction; isekai-genre-readable; NOT retro pixel-art

A STR-driven ranged brawler at the pale margin — grey-lit frontier edge, sparse cover, the moment of break. Shadow-coiled strength visible as dark energy compressed into the strike arm, releasing in a single spiky physical detonation. The blow is the steel delivery of shadow's patient loading: the grey margin has hidden the preparation; the pale edge is where it lands. Fantasy-generic heavy-frontier build; pale margin terrain. Shadow-violet and pale-grey palette; physical-force impact burst at the strike point.

Mood: shadow loads; steel delivers. The margin hides patience until the moment breaks. Pixel-art HD-2D; hand-drawn illustration sensibility; isekai-game-coded.
```

---

### Kit S2-32 — Dune Watcher of the Cracked Margin (Earth/Spiky/WIS)

**Kit ID:** S1_endgame_bc_ranged_low_spiky_wis_none_s0
**Canonical name:** Dune Watcher of the Cracked Margin
**Faction:** Duskchain Ranging Compact (Cluster 4)
**Substrate axes:** ranged | low tempo | spiky amplitude | WIS
**Kit narrative:** "A patient earth-bound ranger who holds position at the fractured edge of frontier ground, releasing strikes in sudden bursts after long stillness — each hit lands like a shifted stone, part of a chain the enemy only recognizes too late."

**Word count:** 130 | Style-adherence: PASS | D7 compliance: PASS

```
INDIVIDUAL PORTRAIT — Dune Watcher of the Cracked Margin
Season: cycle-14-wave-5-season-002
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy art direction; isekai-genre-readable; NOT retro pixel-art

A WIS-driven frontier ranger positioned on cracked margin ground, mid-earth-spike release after long stillness. The cracked margin is the visual anchor: fractured earth at the foreground, the chain's prior detonation points marked by shifted stones in the mid-ground. The current burst rises from cracked earth like a stone suddenly shifted — small and inevitable. WIS governs the interval: the watcher held until the chain's geometry was complete. Fantasy-generic medieval; earthy frontier gear. Earthen-tan and shadow-dark palette; cracked margin ground detail.

Mood: the stone that shifts when the chain completes. Patient observation as doctrine. Pixel-art HD-2D; hand-drawn illustration sensibility; isekai-game-coded.
```

---

### Kit S2-33 — Galewatch Striker of the Dim Verge (Wind/Spiky/WIS)

**Kit ID:** S1_endgame_bc_ranged_low_spiky_wis_none_s1
**Canonical name:** Galewatch Striker of the Dim Verge
**Faction:** Duskchain Ranging Compact (Cluster 4)
**Substrate axes:** ranged | low tempo | spiky amplitude | WIS
**Kit narrative:** "A patient ranging fighter who reads wind currents along the frontier's shadowed margins, timing her strikes to land in sudden, devastating bursts after long silences of stillness. She chains pressure through breath and drift rather than brute cadence."

**Word count:** 132 | Style-adherence: PASS | D7 compliance: PASS

```
INDIVIDUAL PORTRAIT — Galewatch Striker of the Dim Verge
Season: cycle-14-wave-5-season-002
Style: hand-drawn pixel-art game illustration, HD-2D style — reference Octopath Traveler / Triangle Strategy art direction; isekai-genre-readable; NOT retro pixel-art

A WIS-driven frontier ranger at the dim verge of a shadowed frontier tree-line, reading wind currents with raised fingers before releasing a devastating spiky burst. The burst-moment caught: wind-force erupts along the chain path in a sudden concentrated strike after a long interval of breath-and-drift accumulation. She is the only thing moving in a still scene — the verge, the shadows, the dim light all read as held breath that she has now released. Wind-teal and dim-shadow palette; frontier tree-line at dusk.

Mood: breath as rhythm. The chain carries the weight of every patient interval. Pixel-art HD-2D; hand-drawn illustration sensibility; isekai-game-coded.
```

---

---

# SECTION 3 — COMPLIANCE VERIFICATION

## Style Register Adherence — Per-Template Checklist

| Template | Style register language present | "NOT retro pixel-art" explicit | HD-2D reference present | Octopath/Triangle Strategy cited | PASS/FAIL |
|---|---|---|---|---|---|
| Group 1 — Stormcallers | YES | YES | YES | YES | PASS |
| Group 2 — Ironsoil Vanguard | YES | YES | YES | YES | PASS |
| Group 3 — Gale-Blessed Wardens | YES | YES | YES | YES | PASS |
| Group 4 — Duskchain Compact | YES | YES | YES | YES | PASS |
| All 33 individual kit prompts | YES (all) | YES (all — "NOT retro pixel style" / "isekai-game-coded") | YES (all) | Octopath / Triangle Strategy cited in all | PASS (all 33) |

## D7 AI-Tell Line Compliance — Per-Template Verification

All 37 prompts (4 group + 33 individual):
- [ ] Structured visual direction — NOT open-ended narrative generation requests: CONFIRMED
- [ ] No free-form LLM dialogue requests: CONFIRMED
- [ ] All prompts <= 200 words (group prompts 178-192 words; individual prompts 118-133 words): CONFIRMED
- [ ] Style register language fixed, not a variable blank: CONFIRMED
- [ ] Substrate metadata documented per template (kit_id, faction, BC axes, canonical name): CONFIRMED
- [ ] No raw-LLM-output-to-player-surface: CONFIRMED (all prompts are STRUCTURED INPUTS to image-gen API requiring human curation before player delivery)

## Substrate Metadata Completeness

All 37 prompts filled directly from:
- `phase5_faction_clusters.json` (faction name, member count, cultural lineage, tech level, element distribution, BC axes, faction narrative, thematic tags)
- `wave_b_identities.json` (per-kit canonical name, parent_cluster_id, kit_identity_narrative, per-kit kit_id encoding for substrate axes)

NO substrate gaps surfaced. All group prompts fully filled. All 33 individual prompts filled from confirmed ACCEPT or FALLBACK_SUBSTRATE_DERIVED kit records.

---

---

# SECTION 4 — GALADRIEL COORDINATION NOTE

## Status at authoring time

Galadriel's Season 002 visual-coherence design file (`agentic_orchestration/galadriel/notes/2026-05-29-cycle-14-season-002-marquee-visual-coherence-design.md`) has NOT landed at legolas authoring time. The only galadriel design artifacts available are Season 001 files (cv-pipeline scoring + hero selection).

## Baseline-only stance

These 37 prompts are BASELINE prompts built from substrate metadata only. They are fully usable by drax for image-gen immediately. They are substrate-honest, style-register-compliant, and D7-clean as delivered.

## Post-Galadriel Iteration Plan

When galadriel's Season 002 visual-coherence design lands, the following composition pass is recommended (KR to route):

1. **Group portraits (4):** galadriel's scene-framing recommendations (member composition, dominant visual element, lighting/atmosphere, cultural lineage signaling) should be LAYERED into the existing group portrait prompts. Legolas baseline prompts provide faction-identity substrate and dramatic framing; galadriel's visual-coherence read adds inter-cluster contrast recommendations and HD-2D renderability optimization.

2. **Individual kit prompts (33):** per-kit prompts already substrate-honest and individually authored. Galadriel composition pass would verify register-coherence across kits within each faction (ensuring the 13 Gale-Blessed Wardens read as a visual family; the 9 Ironsoil Vanguard kits form a coherent visual roster). Any cross-kit coherence gaps surfaced by galadriel's A5/A10 read are refinement targets, not blocking gaps.

3. **KR routing trigger:** when galadriel files the Season 002 design, KR routes to legolas for an amendment pass adding galadriel's composition recommendations into the relevant group prompts. Individual kit prompts may not need amendment unless galadriel surfaces specific register-coherence concerns.

## What baseline prompts already capture from galadriel's prior Season 001 design

The Season 001 galadriel visual-coherence rubric (A1-A6 substrate axes, A7-A10 CV-pipeline extension) informed the construction of these baseline prompts implicitly:
- A1 Lineage-period coherence: all prompts ground visual direction in modal cultural lineage (european / fantasy_generic medieval)
- A2 Element-distribution coherence: element palette anchors all prompts to substrate top elements
- A3 BC-axis-geometry coherence: engagement-profile and damage-geometry shape every scene composition
- A4 Faction-narrative coherence: faction_identity_narrative quoted and reflected in scene mood per prompt
- A5 HD-2D pixel-art renderability: style register language locked per `style-register.md` canonical

---

## Kit count summary

| Faction | Cluster | Kit prompts authored |
|---|---|---|
| Stormcallers of the Pale Reach | 1 | 3 (all cluster members) |
| Ironsoil Vanguard | 2 | 9 (all cluster members) |
| Gale-Blessed Wardens | 3 | 13 (all cluster members) |
| Duskchain Ranging Compact | 4 | 8 (all cluster members) |
| **TOTAL** | | **33** |

Group portrait prompts: **4**
Individual kit prompts: **33**
Total prompts delivered: **37**

---

*Filed: legolas — research scout — Mode A analytical — 2026-05-29*
*Season: cycle-14-wave-5-season-002 — Season of the Ironsoil Wide-Front*
