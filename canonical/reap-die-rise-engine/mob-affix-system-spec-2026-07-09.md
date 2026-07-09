# Mob Affix System — Design Spec (surface-ledger E10, Leg 2)

> **STATUS: CURRENT (load-bearing)** — Matt-ratified in the 2026-07-09 Pattern-B design session (frame + all forks ruled in-session). Build (Leg 3) queued; this spec is its authority.

**Author:** gandalf. **Ratified:** Matt, 2026-07-09 — frame ("Ratify the frame. It is elegant… I love the inversion-based perspective."), Fork 1 = A, Fork 2 = (c) after dialogue, Fork 3 agreed, Fork 4 agreed, RIVAL naming grammar adopted with spec greenlight.
**Lineage:** E9-C ruling (population = stat-blocks + affix layer) → affix-layer existence audit **ABSENT** (`agentic_orchestration/research/2026-07-08-mob-affix-layer-existence-audit.md`) → E10 accrued → **path (iii) FULL-SPEC FIRST PASS** ruled (Matt: *"If we have the knowledge and systems built to scaffold, why not bring it to life at first pass?"*) → Leg 1 genre canon (`agentic_orchestration/research/2026-07-08-mob-affix-genre-canon.md`) → **this spec (Leg 2)**.
**Companions:** surface-ledger row E10; S1 identity-layer wiring (shared bestiary wells — see §10); D7 AI-tell line; `canonical/reap-die-rise-story/` identity layers (race/family/order/faction/culture/lineage).

---

## 0. What this is / is not

**IS:** the design authority for Reincarnated's monster-modifier (affix) layer — the generative construction, its constitution (five laws), its three-layer architecture, pack semantics, family scopes, telegraph/loot contracts, and the RIVAL naming grammar.

**IS NOT:** a hand-authored affix list (path (iii) explicitly rejects that — the pool is *generated* from substrate); a certification change (see instrument guard); the RIVAL-class build spec (launch-scope, §9 covers only its naming grammar); the boss-encounter design (multi-phase machines reserved there, §5.2).

**INSTRUMENT GUARD (standing, Matt 2026-07-08):** affixed mobs populate **content encounters only** — never the certification gauntlet rooms. Zero certification-contract change. KPM bands, gauntlet composition, and the per-axis pilot instrument are unaffected by this spec.

## 1. The generative frame (ratified)

**Affix instance = (functional family × element/substrate flavor × magnitude @ threat tier).**

The genre's entire affix design space collapses into **8 functional families** (canon §2A):

| # | Family | Layer class |
|---|---|---|
| 1 | Damage-Add | stat |
| 2 | Defense / Stat-Inflate | stat |
| 3 | Terrain-Denial | spatial |
| 4 | Displacement / Movement-CC | spatial |
| 5 | Summon / Spawn | encounter-composition |
| 6 | Resource-Attack | resource |
| 7 | Player-Debuff | resource |
| 8 | On-Death / Threshold | temporal |

The element vocabulary **generates** the pool the way it already generates kits: fire × terrain-denial = burning ground; water × terrain-denial = freezing pool; wind × displacement = vortex; earth × displacement = stone wall. **Sparse-matrix discipline:** only intersections that express *naturally* are emitted — force-filling every family × element cell is the Archnemesis bloat path. The substrate votes; we do not force cells.

## 2. The Five Laws (the constitution — each inverts a documented genre failure)

1. **One modifier, one effect.** (AN failure axes 1–2: bundled mods gave 3-mod rares 12–18 hidden effects; GGG's own 3.20 fix: "one modifier, one effect, self-descriptive name.")
2. **The name carries the mechanic, wrapped in substrate flavor.** (AN axis 1: thematic-only names failed the nameplate channel; PoE 3.20 returned to mechanical naming; D2's "Extra Strong" is the genre readability floor. Our glyph substrate supplies the wrap, the functional family supplies the readable core; D7 AI-tell line governs the LLM fill.)
3. **≤4 mods per mob; category budgets underneath:** ≤1 defensive, ≤1 displacement/CC, elemental-enchants mutually exclusive. (The 4-cap is near-universal — D2 Hell 3, D3/D4 4, PoE 3.20 4 — because ~4 is the player's working-memory budget; D3's category caps + mutually-exclusive displacement quartet are the proven guards.)
4. **Loot coupling = quantity/quality only, hidden until kill, ZERO loot-conversion in ambient encounters.** (AN axes 3+5: conversion mods created skip-the-encounter friction; the 3.20 hide-rewards fix eliminated the opt-out. Conversion-class effects are permitted ONLY in future opt-in contexts on the loot-campaign surface — never ambient.)
5. **No reflect-class mechanics, ever; resource-attack bounded.** (D3 Reflects Damage punished optimal play and was deleted from the genre — D4 carries no analogue. D2 Mana Burn's lesson: drain must never lock the player out of their primary ability loop — every resource-attack magnitude carries a drain ceiling keeping the fight winnable. D2 Thief's lesson folded in: no modifier ever attacks build-investment assets — gear, inventory, cemented progress — only in-combat state.)

## 3. Three-layer architecture (Fork 2 = (c), ruled after dialogue)

**Coarse combat archetypes (damage/support/control/hybrid) are RETIRED from the affix layer** — the kit-naming lesson generalized: identity keyed off coarse mechanical taxonomy is generic by construction; identity keys off substrate. **BC cells stay player/RIVAL-side** — giving ambient mobs BC coordinates would re-open the kit-built door E9-C closed.

### 3.1 Layer 1 — Eligibility: bestiary-substrate affinity profiles (fantasy coherence)

Each mob **family/order** carries an **affinity profile** over the 8 functional families × element expressions — which affixes express naturally for this kind. Cult orders summon and curse; carrion kinds plague the ground; stone-lineage kinds shrug physical; a skittering swarm never Walls. The profile draws from the **same identity wells the player kits draw from** (race/family/order/faction/culture/lineage) — one identity architecture, two consumers (player side wired by S1; mob side consumed here). Sparse by discipline; profile tightness is a tuning knob (tight profile → recognizable kind, D2-champion-like fixed-bundle feel; looser profile → surprising elite, D2-unique-like random-draw feel — one generative track spans the genre's two-track structure).

**Player consequence:** kind predicts trick — the player learns the bestiary the way D2 players learned Fallen flee and Fetishes swarm. Bestiary literacy is the oldest telegraph channel and it makes Law 2's names land instead of carrying readability alone.

### 3.1a Race-well admission constraints (Matt ruling 2026-07-09 — S2 caution, BINDING on Leg 3)

The S2 ruling (vessel-race = bestiary provenance; player kits and mobs draw race from the SAME well) carries two admission criteria plus a construction rule, per Matt's caution (*"if the LLM derives a race that does not fit the Synty humanoid skeletal structure, we will have massive issues… too many varied races [adds] too much scope to the Godot-Synty combinatorial process and [ruins] our ability to derive factions/orders"*):

1. **The race well is CLOSED and CURATED — the LLM never derives races.** Race entries are substrate rows (pattern: the 8-element canon, the register 4-enum). The LLM's only role is naming/flavor WITHIN an admitted race's culture register (D7 narrow-blank fill). No generation path may mint a race.
2. **Rig-conformance gate (admission criterion 1).** A race is admissible ONLY with a verified Synty-humanoid presentation mapping — GeneralSkeleton retarget per the Q7 Option-A contract, using existing POLYGON humanoid variants (+ proportion/scale/material variation). "Space orc" passes (orc frame, sci-fi material register); a serpent-bodied kind FAILS. **Consequence — the bestiary is two-tier:** **becomable races** (rig-gated; vessels, lieutenants, kit provenance) vs **mob-only kinds** (unrestricted; beasts/horrors that are never worn). The fiction supports it natively: the order shapes vessels from reapable humanoid stock — *not every corpse can hold you.* Mob-only kinds still carry §3.1 affinity profiles; they simply never enter the vessel/race well.
3. **Cardinality budget (admission criterion 2).** Race count is a DERIVED budget, not a free choice: with season population P (~700 kits), minimum viable faction mass M (PM-1 clustering mass + per-floor faction/lieutenant/spawn-table needs), and F factions per race, R ≤ P / (M × F). Indicative: P=700, M≈40, F≈2 → **R ≤ ~8; v1 lean 4–6 races** (also bounded above by actual Synty humanoid-variant coverage and below by demo expressiveness). Exact ceiling = Leg 3 math note (Disc #1), fed by (a) drax's read-only Synty humanoid-asset inventory and (b) PM-1 clustering-mass empirics. Factions emerge race-dominant under clustering (modal race + minority members) — strict race-coherence is NOT imposed; the budget math is robust to either.

**Leg 3 gate — SUBSTANTIALLY CLOSED 2026-07-09:** Matt curated the race list in-session (Pattern-B well-design session; `bestiary-race-well-design-2026-07-09.md` — the §3.1a companion): **Human, Goblin, Orc admitted rig-verified** (orc = reskin-tier per Matt's construction ruling: human frame + green material + bulk modular pieces, skeleton untouched); **Elf, Dwarf admitted pending Lane-4a rig-conformance check** (frames confirmed in fantasy character packs). Remaining gate = that rig check + orc modular-asset enumeration (drax). The two-tier admission cost model (reskin / reframe), race-row schema, W1–W4 rulings (race×register composition; undeath = vessel-state; no kit-side race×element coupling; demo-realm distribution) all live in the companion doc.

### 3.2 Layer 2 — Budget: threat tier (balance; identity-blind)

Threat tier sets roll count (genre canon: count scales with difficulty — D2 1/2/3 by difficulty, D3 level-gated 1→4). The engine's existing tier ladder (`swarm < magic < trash < elite < mini-boss < boss`, `monster_generator.py:22`) maps to affix-count brackets at build time (exact bracket table = build-time math note). Law 3's caps + the **small hard ban-table** sit underneath, identity-blind — the backstop doesn't care what you are, only that nobody gets double-displacement.

### 3.3 Layer 3 — Naming: glyph substrate + D7

Name = f(family/order culture, element, functional-family mechanical core). Mechanics readable through the flavor wrap ("Necromonger Pyre-Herald" — order + element + family). LLM fills narrow blanks only (D7); the mechanical descriptor is never LLM-invented.

## 4. Pack model (Fork 1 = A): pack-as-unit, leader-carrier + selective inheritance

Affixes roll on the **pack leader**; inheritance to minions is **selective by layer class** (D2 canon §1.1C generalized):

| Layer class (families) | Inheritance |
|---|---|
| Stat (1–2) | **Inherits, attenuated** (~half-stat, D2 Extra Strong precedent; exact attenuation = build math note) — "the whole pack is Extra Strong and coming at you" |
| Spatial (3–4) | **Leader-only** — one Waller per pack; pack-wide ground hazard is visual noise + movement-budget exhaustion |
| Encounter-composition (5) | **Leader-only** by definition (the summoner IS the leader) |
| Resource (6–7) | **Leader-only** (pack-wide drain is the Mana-Burn 256× bug reborn as design) |
| Temporal (8) | **Leader-only** (the leader's threshold trigger is the pack's gear-shift moment) |

The arena's existing pack-composition machinery (`arena.py:468-502` — the "rare/champion" labels the existence audit found) is the structural home: we give the existing unit a brain, not build a new organ.

## 5. Family scope rulings

### 5.1 Displacement (family 4) — Fork 3 ruled
**Pull and immobilize enter at v1:** pull mirrors the live player-side `vortex_pull` geometry (plumbing, not invention); immobilize rides the existing control/ailment layer. **Walls: DEFER RATIFIED (Matt + gandalf co-sign, 2026-07-09 — Q15).** The named feasibility spike fired (gamora, `agentic_orchestration/gamora/notes/2026-07-09-walls-feasibility-spike-fork3.md`): verdict **DEEP-ARCHITECTURE-CHANGE** — sim space is concrete-positional but obstacle-free (straight-line nav, occluder-blind hit kernels, scalar-distance targeting); dynamic mid-fight spawn is solved, but blocking geometry is a new spatial subsystem. A wall mobs walk and shoot through is a telegraph without a mechanic (the Law-2 inversion this spec forbids). **Walls are a NAMED future spatial-layer workstream** (obstacle type + obstacle-aware nav + hit-occlusion; multi-dispatch, math-note-first) — deferred with a name, not quietly cut.

### 5.2 Temporal (family 8) — Fork 4 ruled
**Simple one-way HP-threshold triggers in scope** (Berserker-at-50% class; combat-state hooks already instrumented for fight telemetry). **Multi-phase state machines reserved for boss/RIVAL encounters.** A trash mob with one gear-shift is texture; a trash mob with a script is a boss wearing the wrong nameplate.

### 5.3 Resource-attack (family 6) — Law 5 operationalized
Every magnitude carries a **drain ceiling**: post-drain, the player's primary loop must remain executable (never full-bar drain; never drain outpacing recovery at intended threat tier). Build math note derives ceilings per energy type.

## 6. Exemplar intersections (NON-CANON — illustrations of the frame, not a list)

*The pool is generated at build time from affinity profiles; these exist only to show the construction's grain:* fire × terrain-denial → burning ground trail · water × terrain-denial → freezing pool (slow-on-stand) · wind × displacement → vortex pull · earth × displacement → stone wall *(spike-gated)* · earth × defense → stone skin analog · element × damage-add → X-Enchanted (element name IS the label anchor) · cult-order × summon → grave-call · carrion × on-death → burst spores. Any exemplar the substrate does not naturally express at build time is dropped without ceremony.

## 7. Telegraph metadata contract

The emitted affix record carries: `functional_family`, `element`, `mechanical_descriptor` (Law 2 core), `flavor_name` (Layer 3), and **telegraph-channel hints** — model tint/VFX (element-coded), ground-decal flag (spatial families), audio-sting flag (on-activation families), nameplate text (mechanical core). The engine emits *readable mechanics*; drax's presentation layer inherits them instead of inventing them. (Canon: the five-channel grammar, §2B; AN's failure was losing the nameplate channel.)

## 8. Loot coupling (Law 4 operationalized)

More mods → more drop rolls (quantity), never different drop *types*. Rewards hidden until kill (PoE 3.20: "kill everything, don't skip" — engagement motivation without pre-kill evaluation friction). Champion-modifier→specific-drop coupling (LE sealed-affix style) is a **future opt-in loot-campaign question**, not ambient design. This section binds to the agnostic-loot specs when that surface lands.

## 9. RIVAL naming grammar (adopted — story canon; build stays launch-scope per E9-C)

**Two-stage: title-epithet at first encounter → true name yielded on defeat.** Genre convergence: Grim Dawn's "Moosilauke, the Chillwind" (evocative, not mechanic-spoiling) + Solo Leveling's Blood-Red Commander Igris (title carries threat color + class; re-named on claim) + Slime's naming-as-identity-evolution + PoE Rogue Exiles (player-grammar hostiles; the direct E9-C mechanical precedent). **Thematic ground:** in the *Reap. Die. Rise.* frame, rivals are other reaped souls on the same descent — a rival announced by epithet whose true name is yielded only when put down is our reincarnation/identity theme arriving on schedule, not borrowed convention. The epithet is substrate-generated (order + element + family, §3.3); the true name persists in session/meta records once earned. RIVAL selection grammar, session-persistence hooks, and encounter design = launch-scope build spec (separate doc, when E9-C's re-entry fires).

## 10. Build notes (Leg 3 — verified gaps + dependencies)

1. **Bestiary identity wells do not exist engine-side (verified 2026-07-09):** the mob record carries `dominant_element`, behavioral `archetype`, power tier, per-element resistances (`monster_generator.py:393-462`) — **no race/family/order/faction/culture/lineage fields.** These are story-spec layers not yet emission-wired. **Shared dependency with S1** (deliberate — one identity architecture, two consumers). Leg 3 cannot fill affinity profiles until the wells exist; S1's walk + the wiring work precede or co-land.
2. **New artifacts Leg 3 builds:** affinity-profile schema (per family/order); ban-table + category-budget enforcement; pack-leader affix roll in arena composition; inheritance attenuation; telegraph metadata emission; threat-tier bracket table.
3. **Named feasibility spike:** dynamic blocking geometry (walls) in room architecture — fires inside Leg 3, rocket/gamora seam.
4. **Sequencing:** Leg 3 slots into the KR sequence **post-design, not demo-blocking, must not preempt C3/E2** (standing). Math note first (Disc #1); build math note derives: affix-count brackets per tier, stat-inheritance attenuation, resource-drain ceilings, magnitude scales per family @ tier.

## 11. Build acceptance criteria (bind the Leg 3 dispatch)

1. Five Laws enforced structurally: no multi-effect mod possible by schema; ≤4 cap + category budgets + ban-pairs enforced at roll time (test: adversarial roll attempts rejected); zero reflect-class or conversion-class entries representable in ambient pools.
2. Affinity profiles are substrate-read (from bestiary wells), not hand-authored constants; sparse cells verifiably absent, not zero-weighted padding.
3. Pack smoke: leader rolls, selective inheritance by layer class per §4 table; minions never carry spatial/composition/resource/temporal mods.
4. Telegraph record complete per §7 on every emitted affix.
5. Instrument guard audit: certification gauntlet composition byte-identical pre/post; affix machinery unreachable from cert paths (the arm-G lesson — prove reachability claims by call-site, not intent).
6. Provenance: every rolled affix names its (family, element, profile source, tier bracket) — certification-honesty style visibility.

---

**Signed:** gandalf, 2026-07-09. Rulings: Matt, in-session (frame + Forks 1-A / 2-(c) / 3 / 4 + naming-grammar adoption). Canon: legolas E10 Leg 1. Build: Leg 3, KR-sequenced.
