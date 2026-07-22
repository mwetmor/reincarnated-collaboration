# Tier-3 Encounter-Geometry — Charter Elicitation Grill (R5 = BEGIN)

> **STATUS:** ✅ GRILL COMPLETE — ALL FORKS RULED 2026-07-22. **F1 ✓ CONFIRMED** (Matt: *"F1 confirmed"*) · **F2 ✓** gamora (+drax-sequencing rider) · **F3 ✓** all-three/Q38, as amended by R-b2 (era×FAMILY) · **F4** gate v0 → X/Y at prereg · **F5 ✓ TRAVELING-KIN** (Matt: *"traveling kin is right"*) · **R-b1/R-b2/R-b3 ✓** (second batch below). **CHARTER DRAFTED:** `agentic_orchestration/gandalf/notes/2026-07-22-tier3-encounter-geometry-run-charter.md` → jack-ryan Gate-1 → prereg → run. **Queue row Q41.**
> **Authority:** Q40 ruling sheet R5 = *"BEGIN = ELICITOR charter session with me present."* This sheet is the durable grill surface for that session — rule async here or live in-session; either lands the same.
> **Author:** gandalf (ELICITOR) · 2026-07-22
> **Discipline:** desirable-run-pattern § 3 — a Tier-3 run cannot charter without a **decidable target-state**. These three forks ARE the target-state definition. ELICIT, don't impose: leans stated, Matt rules.

**▶ ROLE: ELICITOR — draining the unmade decisions out of "Tier-3 encounter-geometry" before any charter is drafted.**

---

## What Tier-3 is (one paragraph of shared ground)

The kit corpus (574 real kits; 267 record-class with full v2.0 six-block geometry data) describes what builds DO. Nothing yet describes what they do it TO — the encounter side: arena shapes, mob formations, pressure patterns, the geometry a kit's bands collide with. Tier-3 is the run that gives the project an encounter-geometry layer. D2's pit runs vs Baal waves, PoE's breach-circles vs ritual-rings, Last Epoch's monolith arenas — every ARPG that respects its kits builds encounter geometry that STRESSES them differently. We have the kit half; Tier-3 builds the collision half.

---

## T3-F1 — What is the run's PRODUCT? (the decidable target-state)

| Option | What ships | Decidability | Tradeoff |
|---|---|---|---|
| **(a) Encounter-grammar spec** | A design vocabulary: arena archetypes, formation grammars, pressure patterns (named, typed, parameterized) | Weak alone — a vocabulary can't FAIL | Fast; pure design doc; but an undecidable product violates the run pattern |
| **(b) Kit→encounter fit layer** | A computable mapping: given a kit's geometry bands, which encounter geometries stress vs showcase it — emitted as data | Strong — the mapping either discriminates or it doesn't | Needs (a)'s vocabulary as substrate; larger |
| **(c) Walls prereg** | A pre-registered sim experiment: encounter variants vs kit sample, effect sizes asserted | Strongest per-experiment | Narrowest; proves discrimination without shipping the layer |

**Lean: (a) as intermediate → (b) as the decidable product.** The grammar spec is Leg-1 scaffolding, not the deliverable; the run CLOSES on the fit layer discriminating. (c)'s experiment shape becomes the gate (see T3-F4), not the product.

**— Matt's word (2026-07-22): lean ADOPTED, with two riders —** (1) *"Would it make sense to marry this to the roguelite run structure (act of a run = era/age; fit the encounter-grammar to the kits of that era/age)?"* (2) *"Do any grammars lean toward potential areas of a map — e.g., the centralized multi-faction melee area or the de-centralized faction outpost area?"* → Both folded into **§ THE F1 FOLD** below; one confirm pends on the folded shape.

## T3-F2 — Who is the FIRST CONSUMER? (routes the output format)

| Option | Consumes as | Consequence |
|---|---|---|
| **gamora (sim)** | Encounter specs become sim scenarios; fit-layer claims become effect-size asserts | Falsifiable immediately; output = machine-readable scenario data |
| **drax (Godot floors)** | Grammar feeds level-authoring (crypt/ravine grammar) | Player-visible soonest; but claims stay unfalsified until playtest |
| **Q11 gauntlet** | Encounter variants slot into the gauntlet harness | Reuses built harness; narrower coverage |

**Lean: gamora.** Sim-falsifiable first; drax inherits a VALIDATED grammar rather than a speculative one. (Matches engine-first orientation: prove the layer against the sim before it shapes floors.)

**— Matt's word (2026-07-22): RULED — gamora.** Sequencing rider registered: *"Drax cannot engage until something emits from the serial content pipeline via JSON. Then we build out the demo with the emitted modular roster (kits → mapped gear, monsters → mapped factions, biome/tileset → faction morph)."* Consumer chain therefore: **gamora falsifies → serial-content JSON emission → drax modular roster.** Tier-3's fit-layer output format must be emission-compatible with `canonical/current-to-end-state/current-to-end-state-serial-content-emission.md` from day one — the fit layer is a future JSON block, not a design-doc-only artifact.

## T3-F3 — What SUBSTRATE feeds it? (bounded substrate, per the run pattern)

| Option | In | Cost |
|---|---|---|
| **record-267 six-block** | gb_* geometry bands as the kit half | Free — landed in VDM-2 Leg A |
| **+ mob-harvest** | New capture: genre mob-formation/arena data (D2/PoE/GD/LE encounter shapes) | New legolas/elrond harvest lane — the only NEW collection |
| **+ Q38 biome-morph frame** | k=5 element-courts + eras-as-shelves + biome-morph rider as the encounter-side organizing frame | Free — already ruled (Q38); using it keeps encounter vocabulary congruent with kit vocabulary |

**Lean: all three, Q38 as the frame.** The kit half exists; the mob-harvest is the run's genuine collection cost; Q38 keeps the two halves speaking one language. (Sizing note: mob-harvest scope gets its own bound in the charter — it is the substrate risk.)

**— Matt's word (2026-07-22): RULED — all three, Q38 as frame.** F1's era rider stratifies the mob-harvest by era/age shelf (per-era collection bounds go in the charter).

## THE F1 FOLD — Matt's two riders, folded (2026-07-22; confirm pending)

**Folded product shape: the fit layer is ERA-INDEXED and the grammar is TIERED.**

1. **Era-act marriage (rider 1 — ADOPTED into the fold).** The roguelite run structure (act = era/age) becomes the fit layer's indexing spine: `fit(kit, encounter | era)`. Q38 already ruled eras-as-shelves on the kit side — this makes the encounter side speak the same coordinate. Three concrete wins: (i) the mob-harvest gets per-era strata (bounded substrate, tractable collection); (ii) the decidability gate sharpens — showcase/stress claims are tested per-era, not corpus-global; (iii) an act's encounter deck IS its era's grammar subset — the fit layer feeds run-generation directly. Genre precedent: Hades' act-biomes each carry their own encounter grammar and the same build plays differently per act; D2's acts carry distinct pressure signatures (Act-2 swarm+ranged-burst beetles/mummies vs Act-4 curse-pressure oblivion knights). **One named caution:** era-conditioning states what encounters SUIT an era's kits — it must NOT silently become kit-availability gating. Availability is progression design (the §1.6 scaling-curve lane, jack-ryan Gate-1 per R6), not Tier-3's to decide.
2. **Map-area archetypes (rider 2 — ADOPTED as the grammar's MACRO tier).** The grammar is three-tiered: **MACRO-topology** (map-area archetype: hub-brawl / outpost-lattice / corridor-gauntlet / siege-line, …) → **MESO-formation** (mob formations within an area: swarm ring, ranged crescent, elite+retinue) → **MICRO-pressure** (per-pack timing/spacing). Matt's two examples are genuinely distinct macro archetypes with opposite pressure grammars: *centralized multi-faction melee* (converging pressure, faction crossfire, player-as-third-party — D2 Travincal council brawl, GD three-way faction fights) vs *decentralized faction outposts* (sweep-and-clear, approach-vector choice, pull discipline — D2 Pit/seal-pop patterns, GD nemesis outposts, PoE expedition placement). **Faction-composition is a macro-tier PARAMETER** (mono-faction outpost vs multi-faction contested) — which plugs straight into the F2 modular roster (monsters → mapped factions; biome/tileset → faction morph). Falsifiability split: MESO/MICRO claims are gamora-sim-testable now; MACRO claims become fully testable when drax floors consume — so the T3-F4 gate binds on meso/micro, and macro ships as parameterized grammar with sim-proxy checks (spawn-topology effects on pressure metrics).

**Confirm wanted (one word):** F1 = era-indexed fit layer + three-tier grammar (macro/meso/micro) with faction-composition as a macro parameter — the run CLOSES on the fit layer discriminating at meso/micro per-era. On confirm, the charter drafts. **→ ✓ CONFIRMED (Matt 2026-07-22: *"F1 confirmed"*) — charter drafted same-turn.**

## T3-F4 — Decidability gate v0 (DRAFTED, per the folded F1; finalized at prereg)

For **each era shelf**: a stratified record-class kit sample (floor n≥8 per era, courts represented) runs in sim against (i) its fit-layer-matched **SHOWCASE** encounter, (ii) its matched **STRESS** encounter, (iii) a **neutral arena** baseline. Pre-registered claims: showcase beats neutral on the kit's declared showcase metrics (declared per register — e.g., sustain-uptime for channel kits, burst-window kill-time for strikers) by effect size ≥ X; stress trails neutral by ≥ X in the opposite direction; direction-consistency ≥ Y% of the sample. **X and Y are set at prereg from gamora baseline variance data (Discipline #18 — methodology AFTER baseline), not guessed here.** Fallback envelope §8-C-style, pre-committed: if the fit layer discriminates corpus-global but fails per-era (or vice versa), the fit layer is NOT served; the grammar spec still lands as scaffolding and the failure mode is named in the review book. Gate text goes to jack-ryan Gate-1 with the charter.

---

**Next beat (~~confirm~~ → LANDED 2026-07-22):** F1 confirmed + T3-F5 traveling-kin ruled → **charter DRAFTED** (`agentic_orchestration/gandalf/notes/2026-07-22-tier3-encounter-geometry-run-charter.md`; gandalf RUN-CONDUCTOR; fit test 4/4 YES) → jack-ryan Gate-1 → W0 harvest+freeze → prereg (X/Y on gamora baselines) → run; fires on Gate-1 pass, veto-open. Island re-cut + naming stays gated behind Tier-3 completion (R1 resolved PATH A; trigger word still Matt's).

---

## APPENDIX — era-act × court split of the record-267 (Matt-requested decision-input, 2026-07-22)

Source: `canon_corpus`, `corpus_class='record'`, read-only query 2026-07-22. `era_year` is populated 267/267 and takes exactly FOUR values — the age spine is already in the data. (Courted kits = 258, "about 260" as Matt estimated; 9 court-NULLs are the known V-15/V-20 honest-NULL residue, 6 of them in Age I.)

| era-act (age) | source shelf | physical | fire | lightning | cold | chaos-poison | (NULL) | **TOTAL** |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| **Age I — 2000** | D2 | 27 | 12 | 7 | 3 | 5 | 6 | **60** |
| **Age II — 2013** | PoE1 | 27 | 20 | 13 | 14 | 17 | 2 | **93** |
| **Age III — 2016** | GD | 9 | 9 | 8 | 4 | 10 | 1 | **41** |
| **Age IV — 2024** | PoE2 + LE (+1 modern-league PoE1) | 27 | 14 | 14 | 6 | 12 | 0 | **73** |
| **court totals** | | **90** | **55** | **42** | **27** | **44** | **9** | **267** |

Readings (gandalf, senior-designer):

1. **Four ages fall out natively** (60/93/41/73) — uneven but workable act pacing (D2's own acts are uneven; Act-4-style tight acts read as intentional).
2. **Zone-per-court viability differs sharply by age:** Age I is physical-dominant (45%) — cold(3)/chaos-poison(5) cannot carry solo zones; **Age II is the only age where ALL FIVE courts clear zone viability** (13–27 each) — the natural five-zone sprawl act; Age III is flat (8–10 across four courts) — reads as the multi-faction CONTESTED act (the macro-tier hub-brawl archetype), not court-pure zones; Age IV supports 3–4 zones (cold 6 thin).
3. **Cold is structurally thin everywhere** (27 total = 10%; never >15% in any age). Options: cold zones only where viable (Age II); cold as biome-MORPH modifier on other zones (the Q38 rider doing exactly its job); or later cold-kit minting. Do not plan a standing cold zone per act off this substrate.
4. **Within-act time-texture is cheap:** multi-shelf continuity is high (43/60 · 75/93 · 40/41 · 63/73 kits span multiple patch-shelves in their game) — zones inside an act can progress through the game's own patch history with minimal kit-pool discontinuity.
5. **Classification guard:** these are ARCHIVE-side affinity counts — they bound zone theming, era-stratified mob-harvest sizing (F3 strata = these row totals), and showcase-encounter density. They are NOT player kit-availability gates (standing caution).
6. **Archive-frame resonance + one story fork:** under the ruled archive-frame, `era_year` is the in-world age spine — acts = ages of the genre (2000→2013→2016→2024). Whether a run DESCENDS chronologically, reverse-chronologically (descending into older strata — archaeology-of-the-genre, strong death-faith fit), or player-chooses act order is a STORY call — flagged, not decided.

---

## APPENDIX B — era-act × BUILD-FAMILY split (Matt-requested sequel to Appendix A, 2026-07-22)

Matt: *"element looks good, but can you show me by build family (including multi-projectile volley)? … you may see patterns specific to these 5 games and draft potential family columns as you go."*

**Method:** memberships joined read-only against `canon_corpus.era_year` (populated 585/585 — all classes). Three membership tiers kept SEPARATE: **RATIFIED** (gateA table `atlas_gateA_labels_2026_07_14`; τ-propagated shown as `+Np` with the standing ~1/3-precision caveat) · **DOCKETED** (`family-candidates-docket-2026-07-17.md`, self-scored precision shown; awaiting Matt names-review) · **FRESH-DRAFT** (this pass, unscored). No court/element anywhere (family view per Matt's course-correction). Off-spine = annex+system members (the 16 non-spine games: la · d3 · d4 · vs · tq · di · hot · chronicon · undecember · tl2 · tli · hades1/2 · tq2 · mcd · tl1).

### B1 — the six RATIFIED families × ages

| family | Age I · D2 (60) | Age II · PoE1 (93) | Age III · GD (41) | Age IV · PoE2+LE (73) | off-spine | Σ |
|---|---:|---:|---:|---:|---:|---:|
| WHIRLWIND | 3 | 1 | 1 | 2 | 8 | 15 |
| CHANNELED-BEAM | — | 2 | 3 | 1 | 3 | 9 |
| MINION-PET | — | — | — | — | 7 | 7 |
| AURA | 1 | 3 +1p | — | 1 | 3 +1p | 8 +2p |
| TOTEM-SENTRY | 0 +3p | 8 +6p | 1 +2p | 7 +5p | 8 +6p | 24 +22p |
| TRAP-MINE | 2 +4p | 8 +4p | 0 +5p | 2 +1p | 11 +6p | 23 +20p |

### B2 — the five DOCKETED candidates × ages (docket 2026-07-17)

| docket (self-scored precision) | Age I | Age II | Age III | Age IV | off-spine | Σ |
|---|---:|---:|---:|---:|---:|---:|
| MELEE-STRIKE (0.90) | **10** | — | 5 | 3 | 18 | 36 |
| DOT-AILMENT (0.97) | 4 | **15** | 4 | 5 | 8 | 36 |
| MULTI-PROJECTILE-VOLLEY (1.00) | 3 | **8** | — | 3 | 6 | 20 |
| SHAPESHIFT (0.80) | 4 | — | 1 | 3 | 6 | 14 |
| IDENTITY-GAUGE (0.97) | — | — | — | — | **31** | 31 |

### B3 — FRESH-DRAFT flags (this pass; unscored; geometry-axis + roster sanity-read)

| draft | I | II | III | IV | n (record) | note |
|---|---:|---:|---:|---:|---:|---|
| CHAIN-BOUNCE | 3 | 6 | 5 | 5 | 19 raw | the one age-BALANCED candidate (Javazon → Arc → Panetti's/Stormbox → Lightning Blast). Raw axis fuses bounce-lightning with contagion-spread (Rabies / Bloody Pox / ED-C — DOT-AILMENT's territory); bounce-core ≈ 12 |
| DASH-STRIKER | 1 | 2 | 2 | 1 | 6 | coherent (Charger / Flicker / Shadow Strike / Shift) but sub-scale — flag only |
| NOVA-RING | 2 | — | — | 1 | 3 | Nova Sorc + Poison Nova Necro + Bladestorm — too thin to column |
| PULL-VORTEX | — | 2 | — | 2 | 4 | + the LA identity-gauge pull cohort off-spine + R4's LA-4 mint incoming — **re-probe post-mint** |
| SUMMONER-LEGION (obs) | — | ~3 | — | ~2 | ~5–8 | record-class summoners (Spectres, Skeleton Mages, Golementalist, Wormblaster, Poet's Pen VD) are claimed by NOTHING — ratified MINION-PET is the narrow taunt-pet archetype (7/7 off-spine); the spine's summoner mass awaits its own docket |

### Coverage + readings

Family-claimed share of the act spine (ratified + propagated + docketed): Age I 28/60 = **47%** · Age II 53/93 = **57%** · Age III 20/41 = **49%** · Age IV 31/73 = **42%** · **total 132/267 = 49%**. Residual geometry mass: ground_targeted_circle 36 · blank 26 · circle 22 · single_target 10.

Readings (gandalf, senior-designer):

1. **Each age has a SIGNATURE family — the act-personality result.** Age I = MELEE-STRIKE (10, its largest on-spine cell) + SHAPESHIFT (4) + WHIRLWIND (3): the physical-brawl act. Age II = DOT-AILMENT (15) + TOTEM (8+6p) + TRAP (8+4p) + MPV (8): the attrition-and-emplacement act. Age III = CHANNELED-BEAM (3, its home shelf) + MELEE-STRIKE (5) + chain (5): the sustained-fight act. Age IV = TOTEM (7+5p) + the highest residual (58% unclaimed): the hybrid frontier act.
2. **The holes are load-bearing, and they are TRUE genre history:** CHANNELED-BEAM absent from Age I (D2 never made channel viable — Inferno's whole career); MELEE-STRIKE absent from Age II (PoE1's famous melee deficit — 0 of 36 docket members are poe1); SHAPESHIFT absent from Age II; AURA absent from Age III; MPV absent from Age III. Under the F1 fold these holes are FEATURES: per-act showcase decks differ because the families genuinely lived and died by era.
3. **Matt's two map-area archetypes map onto ages:** the centralized multi-faction melee area is Age I/III native (melee-strike + brawl mass — Travincal lineage); the de-centralized faction outpost area is Age II native (totem nests, trap fields, DoT clouds — emplacement warfare). The MACRO tier can deal area-archetypes per act from the act's own family deck.
4. **MPV lesson — docket over axis:** the current corpus carries 29 record kits with `multi_projectile` geometry, but the axis-only extras include summoners whose MINIONS volley (Spectres, Skeleton Mages, Golementalist) and proc-engines (Poet's Pen VD). The docket-20 (islet ∩ axis, precision 1.0) is the servable core. Family = mechanism-IDENTITY, not raw axis value — the same reason the six ratified families are camera-robust.
5. **Guest-family fork (ELICIT, parked for Matt):** IDENTITY-GAUGE (31, all LA) and ratified MINION-PET (7, all off-spine) have ZERO act-spine presence. If acts = the four ages of the five spine games, these families cannot headline any act natively. Options: (a) catalogue-only until an edition admits annex games to the spine; (b) off-spine GUEST encounters (rift-style cameos); (c) MINION-PET docket re-seed with a loosened axis to capture the spine's summoner mass (composes with the SUMMONER-LEGION observation, B3).
6. **~49% claimed / ~51% residual is the right amount of structure:** enough family mass to deal era-signature showcase encounters per act NOW; enough residual to keep future dockets honest (CHAIN-BOUNCE and SUMMONER-LEGION are the two the residual is loudest about).
7. **Standing guard re-stated:** these are archive-affinity counts — encounter-grammar inputs, NOT player kit-availability gates (progression = R6 / jack-ryan lane).

---

## SECOND RULING BATCH — 2026-07-22 (post-Appendix-B): THE FAMILY-FACTION FOLD

> Registered by gandalf (ELICITOR) same-session, directly from Matt's words. **Three rulings** (R-b1 · R-b2 · R-b3), **one new fork** (T3-F5), **one fork-let** (5b), one standing mandate.

### Matt's verbatim anchors

1. *"Ok, I am decided on build families for the grouping of kits/factions per run."*
2. *"…we need to split up the monsters (I call them monsters but they may be humanoid NPC faction members) with the same main skills/ability types as their build family kit leaders."*
3. *"Each time you save an enemy kit by beating it, and you become it, there should be at least one faction in the next act that is the same as the faction that you just chose to be. This is because I want to align the build family factions to their intent towards you. When you become a whirlwind kit, it automatically makes you at odds with all other build family factions except whirlwind. The whirlwind faction does not fight against you, and you can interact with them (maybe they have shops, offer boons, etc)."*
4. Standing refinement mandate: *"Your ultra think was great and we need to continue to refine it as we build the table/pattern into the roguelike run structure."* → the era×family cross-tab is a LIVING instrument of the Tier-3 run, refined as the grammar builds.

### R-b1 ✓ RULED — build-families are THE run faction-grouping

Kits and factions per run group by BUILD-FAMILY. This consumes the T3-F2 modular-roster chain: roster modules key on family (kits→gear stays; monsters→factions now keys on family; biome→faction-morph rider composes). Membership tiers stay provenance-clean — RATIFIED > DOCKETED > FRESH-DRAFT; working labels remain provisional until Matt's names-review (docket §6 guardrail holds).

### R-b2 ✓ RULED — monsters split by family-leader mechanism (AMENDS T3-F3)

The mob-harvest is now **era × FAMILY stratified**, not era-only. "Monsters" may be humanoid NPC faction members — the family IS the faction identity either way. Mob/NPC templates INHERIT the family kit-leader's mechanism verbs: whirlwind mobs spin-and-close · totem mobs emplace-and-hold · trap mobs pre-seed ground · beam mobs channel lanes · volley mobs fan projectiles · DoT mobs stack-and-retreat · melee mobs swarm the brawl. MESO formations + MICRO pressure verbs DERIVE from the family mechanism — the three-tier grammar gets its vocabulary from the family table above.

### R-b3 ✓ RULED — the KIN-FACTION loop (become → kin guaranteed; all others hostile)

Beat an enemy kit → save it → **become** it → **≥1 faction of that family is GUARANTEED in the next act.** Faction disposition keys on PLAYER-FORM: every family ≠ yours = hostile; your family = **kin** — non-hostile, interactive (shops, boons, etc.). Becoming is a diplomatic act: the form you wear IS your allegiance.

### Design heart (gandalf reading)

**Enemies are the menu of future selves.** Kin = consolidation (rest, shop, boon); hostiles = the only path to becoming something else. Fighting IS shopping for your next body — the reap-die-rise loop finding its faction grammar. Genre lineage: this inverts the D2 hostility model (static monster allegiance) into a Mushoku-Tensei-class identity mechanic (the world reads what you ARE, not what you did).

### T3-F5 — NEW FORK: kin-guarantee × era-hole collision

The kin guarantee collides with Appendix-B reading 2 (holes are true genre history). Concrete case: become MELEE-STRIKE at the end of Age I → Age II (PoE1 act) has **ZERO native melee** (0/36 docket members are poe1). Same collision for SHAPESHIFT→II, BEAM-becomes entering I, AURA→III, MPV→III.

| option | mechanism | verdict |
|---|---|---|
| **(a) TRAVELING KIN** | your kin faction TRAVELS with you — a reserved encampment slot per act; the anachronism IS the story (a whirlwind caravan camped in the trap-age). D2 caravan lineage: Warriv/Meshif follow the player through acts | **✓ RULED (Matt 2026-07-22: *"traveling kin is right"*)** |
| (b) ERA-RELAXATION | kin faction simply spawns in-act regardless of era-affinity; no narrative dressing | functional, flavorless fallback |
| (c) BECOME-GATING | only allow becoming families native to the NEXT act | **REJECT** — constrains the core become-fantasy to serve a spawn table |
| (d) KIN-ADJACENCY | nearest-family substitute counts as kin | **REJECT** — dilutes "at odds with ALL other families except yours"; the ruling's edge is its clarity |

Under (a), the era-holes stay load-bearing for HOSTILE composition (per-act showcase decks unchanged) while the kin slot is exempt-by-story — the guarantee never bends the act's native family deck.

### Fork-let 5b — disposition-flip timing

When you become mid-act: do already-spawned same-family packs flip to kin INSTANTLY or at the act boundary? **Lean: INSTANT** — the world reads the form; the mid-fight flip is the reveal that TEACHES the rule (one becoming, witnessed, replaces a tutorial). *(Adopted veto-open — charter ledger T3-V1.)*

### Residual-role observation

~51% of record kits are family-unclaimed → these are the **unaffiliated wilds** — monsters hostile to everyone, belonging to no court of becoming. Standing guard: archive-affinity, not player availability (R6 lane).

### UPDATED F1 FOLD — what Matt's confirm decides (plain language; supersedes the earlier confirm ask)

Confirming the F1 fold = saying YES, the Tier-3 run builds these three things:

1. **An era-indexed fit layer** — `fit(kit, encounter | era)`: how well a player kit meets an encounter, conditioned on which age/act it lives in.
2. **The three-tier encounter grammar** — MACRO map-area archetypes (centralized brawl + decentralized outposts — now with a DISPOSITION dimension per R-b3: hostile-outpost vs kin-outpost) · MESO formations · MICRO per-pack pressure verbs; faction composition family-keyed (R-b1/R-b2) and player-form-coupled (R-b3).
3. **The T3-F4 gate** — MESO/MICRO must BIND in simulation (gamora evidence, X/Y set at prereg); MACRO ships parameterized.

It does NOT decide: kit availability/progression (R6 — jack-ryan lane) · act ORDER (descent-direction story fork, parked) · T3-F5 (~~its own word~~ **✓ RULED TRAVELING-KIN same-day**).
