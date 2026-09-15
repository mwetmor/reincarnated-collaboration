# Research — ARPG skill-VFX motion grammars + how painted-2D games author effects — 2026-09-15

> **STATUS:** CURRENT — legolas Mode A (UNKNOWN-RESEARCHER). Commissioned by gandalf (SPEC-AUTHOR / ARCHITECT, VFX workflow architecture session). Brief: `agentic_orchestration/gandalf/requests/2026-09-15-legolas-mode-a-vfx-grammar-and-authoring-split.md`. Filed by gandalf verbatim from the agent's returned text (the harness blocks sub-agent repo writes — same precedent as `2026-09-14-vfx-oracles/findings.md`).

**Mode:** A (analytical; read-only)
**Commissioner:** gandalf
**Host rule observed:** no video decoding, no frame extraction, one fetch at a time, largest download 1.88 MB (Hades `Fx.sjson`), peak RSS < 120 MB. No installs, purchases or accounts.

**Evidence classes:** VERIFIED (primary source read this session) · MEASURED (first-hand computation, method stated) · DERIVED · INTERNAL (our repos/DBs, path given) · PRACTITIONER-REPORT · INFERRED (my reasoning, marked).

**Prior work cited, not redone:** `agentic_orchestration/legolas/research/2026-09-14-vfx-oracles/findings.md` · `…/2026-09-15-chronicon-com-slormancer-vfx/findings.md` · `…/2026-09-14-vfx-style-atlas/findings.md` · `~/Games/vendor/vfx-atlas/`.

---

## Summary

The grammar taxonomy the brief asks for **already exists inside our own substrate and nobody has been reading it as a VFX artefact.** `agentic_orchestration/research/curated/corpus.db` carries a `motion_signature_registry` of **18 named motion paths** and a `vfx_archetype` vote (run `vfx-archetype-vote-2026-08-23`) of **27 archetypes over 1,135 banded reference skills** drawn from 590 source-game kits across 21 games — with per-archetype modal motion signature at **purity 1.00 for every archetype that has one**, exemplar skill names, and delivery class. That is a finished grammar table, sourced, with exemplars, that the six-kit bake-off did not consult.

**Coverage is better than feared and the corpus is fat-tailed, not flat.** Six grammar templates cover **53–65 %** of the reference corpus by archetype, **88 %** once near-identical archetypes are folded into grammar families; ten templates reach **90 % / 99 %**; fifteen reach **~92 % / 100 %**. The long tail (fork n=5, knockback n=1, defensive_dash n=4) is genuinely rare and can be aliased onto neighbours.

**The engine's palette and the corpus's grammars disagree in both directions, and the brief's own palette list is a third, non-matching vocabulary.** Six names in the brief (`projectile`, `nova`, `summon`, `trap_mine`, `totem_turret`, `channel`) are **not** in `VALID_GEOMETRY_TYPES`; five names in the engine (`ground_targeted_circle`, `circle`, `vortex_pull`, `teleport`, `placed_lane`) are **not** in the brief. The emitted 411-kit corpus contains 87 skills carrying `roll` / `persistent_zone` — values the engine's own frozenset rejects.

**On authoring: no well-documented painted-2D action game hand-draws a flipbook per effect.** Every case with primary evidence is a *composition* system — a small set of painted or rendered sheets, re-instanced with runtime tint, rotation, scale and layer stacking. Hades is the extreme, quantified case: **5,141 named FX entries resolve to 1,152 unique texture sheets**, and **3,396 of the 5,141 (66 %) declare no asset at all** — they inherit one and change parameters (MEASURED this session from `Fx.sjson`).

**H-A is supported without a counterexample found. H-B is supported and now bounded numerically:** per-god unique painted FX sheets in Hades run **4–26, median 12.5** (Zeus 8, Poseidon 12, Aphrodite 6, Demeter 26) over a **shared, element-agnostic particle alphabet of 105 sheets / 46 noun-roots** (MEASURED).

---

# Q1 — The grammar taxonomy

## 1.0 Where the taxonomy already lives (INTERNAL, VERIFIED)

| Artefact | Path | What it is | n |
|---|---|---|---|
| `motion_signature_registry` | `agentic_orchestration/research/curated/corpus.db` | Named spatial/temporal *paths*, each with a one-line definition and an `engine_impl_ref` slot | **18** |
| `vfx_archetype` (run `vfx-archetype-vote-2026-08-23`) | same DB | Archetype ↔ modal motion signature ↔ modal delivery class ↔ exemplar skills ↔ engine-key flag ↔ support tier | **27** |
| `vfx_archetype_member` | same DB | Per-skill assignment with RAW geometry/motion/delivery preserved (curation reversible) | **1,158 rows** |
| `skill_geometry_band` | same DB | Per-skill bands: delivery, origin, width/range/speed, pierce/chain/fork, count-per-cast, cadence, motion signature, confidence, verbatim source anchor | **490 rows** |
| `canon_corpus` | same DB | The source-game reference corpus the archetypes are voted over | **590 kits, 21 games** |

The 18 registered motion signatures, verbatim: `straight_line` · `spiral_out` · `orbit_fixed` · `sine` · `mortar_arc` · `wall_sweep` · `fan_spread` · `chain_hop` · `burst_around_self` · `ground_place` · `point_strike` · `arc_sweep` · `blink_translate` · `lane_place` · `leap_arc` · `inward_pull` · `fork_split` · `ricochet_return`.

`delivery_class` is a 7-value enum — `projectile · beam · zone · motion · aura · summon_delegate · melee_arc` — and it is, in effect, **the grammar taxonomy already collapsed to seven** (VERIFIED, table CHECK constraint). Distribution over 490 banded skills: zone 115 · projectile 97 · melee_arc 77 · aura 71 · summon_delegate 53 · motion 47 · beam 16 · null 14.

## 1.1 Taxonomy table — grammar → phases → exemplars → engine geometry

Exemplars are **verbatim `source_skill` strings from `vfx_archetype_member`** (VERIFIED, INTERNAL) unless marked. "Engine geometry" is the member of `VALID_GEOMETRY_TYPES` (`generation/geometry_derivation.py:42`).

| # | Grammar | Motion signature | Phases (what moves) | D2 | GD | PoE1 | LE | Hades | Engine geometry | Members |
|---|---|---|---|---|---|---|---|---|---|---|
| G1 | **Ground-placed field** | `ground_place` | cast → *reticle/decal at target* → field spawn → **loop tick** → expiry fade | Blizzard · Blaze · Corpse Explosion · Apocalypse | Blackwater Cocktail · Devastation · Dreeg's Evil Eye | Caustic Arrow · Creeping Frost · Armageddon Brand · Contagion | Chthonic Fissure · Ghostflame ¹ | Hail Storm (Zeus+Demeter duo) | `ground_targeted_circle` | **115** |
| G2 | **Point strike** | `point_strike` | anticipation → *weapon/impact at one point* → impact burst → residual | Berserk · Concentrate · Charged Strike | Cadence · Primal Strike · Righteous Fervor | Heavy Strike · Glacial Hammer · Infernal Blow | Smite · Shield Bash ¹ | (see G14) | `melee_strike` | **115** |
| G3 | **Self buff / stance** | *(none — no path)* | cast flare → **persistent body-attached loop** → drop-off | Bone Armor · Enchant · Fade · Cyclone Armor | Blood of Dreeg · Word of Renewal · Mirror of Ereoctes | Blood and Sand · CWDT chassis | Reaper Form · Low-Life Ward ¹ | Cast load (bloodstone into shield) | `self_buff` | **112** |
| G4 | **Placed delegate (totem/turret/pet/summon)** | *(none — delegate carries its own)* | cast → **spawn at point** → delegate acts on its own clock → despawn | Hydra · Death Sentry · Clay Golem · Dire Wolves | Mortar Trap · Reap Spirit · Wendigo Totem · Raise Skeletons | Ancestral Warchief · Ballista Totem · Orb of Storms · Herald of Agony | Storm Totem · Skeleton Necro · Wraithlord ¹ | — | `totem` | **97** |
| G5 | **Single projectile** | `straight_line` | cast flare → **travel (translate + trail)** → impact burst → residual | Bone Spirit · Cold Arrow | Doom Bolt · Blade Trap | Puncture · Power Siphon · Unearth | Frost Claw · Lightning Blast ¹ | Coronacht Attack · Crackling Skewer | `single_target` | **90** |
| G6 | **Melee arc / sweep** | `arc_sweep` | wind-up → **sector sweep in front (rotating wedge)** → per-target impacts → trail fade | *(none banded)* | Blade Arc · Bone Harvest | Cleave · Lacerate · Blade Flurry | Flame Reave · Swarmblade ¹ | — | `melee_arc` | **76** |
| G7 | **Aura** | *(none — no path)* | activation pulse → **anchored ring/dome loop, follows owner** → per-tick pulse → deactivation | Conviction · Battle Orders · Amplify Damage | Night's Chill · Celestial Presence | Righteous Fire · Plague Bearer · aura suite | Fire Aura · Healing Hands ¹ | — | `aura` | **73** |
| G8 | **Multi-projectile / spread** | `fan_spread` | cast flare → **N simultaneous travels diverging** → N impacts | Multiple Shot · Double Throw · Frozen Orb | Phantasmal Blades · Stun Jacks · Canister Bomb | Barrage · Bladefall · Elemental Hit | Umbral Blades · Hammer Throw ¹ | Coronacht Special (homing volley) · Revaal cast | `multi_projectile` | **68** |
| G9 | **Line / pierce** | `straight_line` | cast flare → **single travel that does not stop at first target** → pierce ticks → terminal fade | Bone Spear · Blade Fury · Ice Blast · Lightning | Fire Strike · Forcewave | Freezing Pulse · Spectral Throw · Spectral Helix | Erasing Strike ¹ | — | `line` | **51** |
| G10 | **Nova / ring (burst from self)** | `burst_around_self` | cast flare → **radius expands from origin** → ring peak → collapse | Nova · Poison Nova · Ring of Fire | Callidor's Tempest | Ice Nova · Discharge · Blade Blast | Runic Invocation ¹ | Dragon Rush (bloodstone AoE release) | `ring` *(folded)* / `circle` | **50 + 43** |
| G11 | **Orbit / revolve** | `orbit_fixed` | cast → **N payloads revolve about an anchor, tick on contact** → stack/decay | Blessed Hammer · Frozen Orb | Blade Spirit | Blade Vortex · Winter Orb | Ring of Shields ¹ | — | `orbit` | **18** |
| G12 | **Whirlwind / spin** | `orbit_fixed` | enter → **owner rotates, hitbox sweeps continuously while moving** → exit | Whirlwind | Eye of Reckoning | Cyclone | Warpath · Bladestorm ¹ | Life-stealing Spin Attack | `whirlwind` | **33** |
| G13 | **Dash / charge** | `straight_line` (owner) | telegraph → **owner translates fast along a line, trail streak** → contact impacts → skid | Charge | Blitz · Vire's Might | Whirling Blades · Flicker Strike · Shield Charge | Shift · Dive Bomb ¹ | Divine Dash (Athena) | `dash_attack` / `defensive_dash` | **32 + 4** |
| G14 | **Ground slam / shockwave** | `point_strike` | wind-up → **impact at ground point** → expanding shock ring → debris residual | *(none banded)* | *(none banded)* | Earthquake · Earthshatter · Boneshatter · Seismic Trap | *(none banded)* | Volcanic Strike (Hephaestus) | `ground_slam` | **27** |
| G15 | **Beam / channel** | `straight_line` (sustained) | wind-up → **continuous held beam, origin tracks owner** → per-tick impacts → snap-off | Inferno | Albrecht's Aether Ray · Drain Essence | Incinerate · Divine Ire · Crackling Lance | Soul Feast ¹ | — | `beam_channel` | **23** |
| G16 | **Blink / teleport** | `blink_translate` | vanish flare at origin → *(no travel)* → arrival flare at destination | Teleport · Enigma Teleport | Shadow Strike | Brand Recall | Shift ¹ | — | `blink` / `teleport` | **18 + 8** |
| G17 | **Cone / breath** | `fan_spread` (sustained) | wind-up → **sector opens outward from owner, widening** → falloff | Flame Wave · Howl · Shockwave | Flames of Ignaffar | Ice Shot · Wave of Conviction | Flame Reave ¹ | — | `cone` | **18** |
| G18 | **Chain hop** | `chain_hop` | cast → first travel → **N hops target-to-target, each hop drawn as a link** → terminal | Chain Lightning · Claws of Thunder | Storm Box of Elgoloth | Arc · Lightning Arrow · Storm Brand | Tempest Strike ¹ | Lightning Strike (Zeus) · Thunder Flourish | `chain` | **17** |
| G19 | **Vortex / inward pull** | `inward_pull` | cast → **radial inward suction, targets translate toward focus** → collapse burst | Abyss | *(none banded)* | *(none banded)* | *(none banded)* | — | `vortex_pull` | **15** |
| G20 | **Placed lane / wall** | `lane_place` | cast → **static line segment laid on ground** → loop tick → expiry | Fire Wall · Blade Sentinel | *(none banded)* | *(none banded)* | Frost Wall ¹ | — | `placed_lane` | **9** |
| G21 | **Ricochet / return** | `ricochet_return` | cast → out-travel → **bounce target-to-target, or return to owner** → catch | *(none banded)* | Aegis of Menhir | *(none banded)* | Shield Throw ¹ | — | `ricochet_bounce` | **9** |
| G22 | **Leap arc** | `leap_arc` | crouch → **airborne ballistic arc, owner leaves ground** → landing AoE | Leap · Leap Attack | *(none banded)* | *(none banded)* | Dive Bomb ¹ | — | `leap_strike` | **8** |
| G23 | **Fork / split** | `fork_split` | cast → travel → **split point: N diverging children** → N impacts | Lightning Fury | Panetti's Replicating Missile | *(none banded)* | Detonating Arrow ¹ | — | `fork` | **5** |
| G24 | **Knockback** *(leak)* | *(none)* | — | — | — | — | — | Ancient Spear (Rage Flip) | *(none)* | **1** |
| — | **Mortar arc / thrown-arc → field** | `mortar_arc` | cast → **ballistic lob to a target point** → land → field (→ G1) | — | Blackwater Cocktail ² | Poisonous Concoction ² | Detonating Arrow ¹ | Revaal lob | **no engine geometry** | *(registry-only; 0 rows)* |
| — | **Spiral out** | `spiral_out` | cast → **outward spiral path** | — | — | — | — | — | **no engine geometry** | *(registry-only)* |
| — | **Sine** | `sine` | cast → **sinusoidal travel** | — | — | — | — | — | **no engine geometry** | *(registry-only)* |
| — | **Wall sweep** | `wall_sweep` | **a wall/line sweeps across an area** | — | — | — | — | — | **no engine geometry** | *(registry-only)* |

¹ **INFERRED, name-evident only.** Last Epoch has **37 kits in `canon_corpus` and ZERO banded rows** in `vfx_archetype_member` (VERIFIED by query — see G-1). Every LE cell above is my grammar reading of an attested corpus `folk_name`, not an attested band. Do not cite LE cells as corpus evidence.
² The brief's own exemplars, not corpus rows.

Archetype member counts are VERIFIED. `ring` and `defensive_dash` carry `fold_status='folded'`; `knockback` is `held` with an explicit `vocab_flag` reading *"probable vocabulary leak: an effect noun occupying a geometry slot (n=1)"*.

## 1.2 Where the palettes disagree — three non-matching vocabularies

There are **three** geometry vocabularies in play and no two of them agree.

**(a) Engine truth** — `VALID_GEOMETRY_TYPES`, `generation/geometry_derivation.py:42`, **26 members** (VERIFIED). **(b) The brief's palette list** — 27 names. **(c) What the emitted 411-kit corpus actually carries** — 20 distinct values over 3,009 geometry-bearing skills (MEASURED).

| Direction | Names | Consequence |
|---|---|---|
| **In the brief, NOT in the engine** (6) | `projectile` · `nova` · `summon` · `trap_mine` · `totem_turret` · `channel` | A VFX spec written against the brief's list would name six grammars the generator cannot emit. `nova` ≈ engine `ring`; `summon`/`totem_turret`/`trap_mine` all collapse to engine `totem`; `channel` ≈ `beam_channel`; `projectile` ≈ `single_target`. |
| **In the engine, NOT in the brief** (5) | `ground_targeted_circle` · `circle` · `vortex_pull` · `teleport` · `placed_lane` | **`ground_targeted_circle` is the single largest archetype in the reference corpus (115 skills) and third largest in the emitted corpus (340 skills, 11.3 %).** A VFX architecture built from the brief's list would omit the biggest grammar we have. |
| **In the emitted corpus, NOT in the engine's frozenset** (3) | `roll` (23 skills) · `persistent_zone` (10) · `projectile` (54) | 87 skills carry a value the engine's own validator rejects (`projectile` may be a pre-rename survivor; `roll` and `persistent_zone` are unregistered). No read-compat alias exists for any of the three — `_GEOMETRY_ALIASES` holds only `chain_lightning → chain`. **Cross-seam finding for rocket/elrond; not fixed here.** |

**Engine geometries with NO corpus grammar** (in `VALID_GEOMETRY_TYPES`, zero rows in the emitted 411-kit corpus): `melee_strike`, `melee_arc`, `ground_slam`, `dash_attack`, `whirlwind`, `leap_strike`, `aura`, `orbit`, `placed_lane` — **nine of twenty-six, and they are exactly the ones the reference corpus leans on hardest** (melee_strike 115 + melee_arc 76 + aura 73 + whirlwind 33 + dash_attack 32 + ground_slam 27 = 356 reference skills, **31 % of the banded corpus**). The generator has never emitted one. This is the structural reason the bake-off produced six projectiles: **the emitted corpus is projectile-and-field shaped, and the melee/motion half of the palette is dead code.**

**Corpus grammars with NO engine geometry**: **`mortar_arc`** (thrown-arc → ground field — the brief's own Blackwater Cocktail / Poisonous Concoction case), **`spiral_out`**, **`sine`**, **`wall_sweep`**. Of these only `mortar_arc` is attested in the source material at scale; the other three are registry entries with zero banded members and should be treated as speculative.

**One cross-seam item already closed, recorded so it is not re-raised:** `vfx_archetype` flags `orbit` with *"value is NOT a key of kit_compiler._RICH_TO_SPATIAL — the engine would fall through to the 'point' default"*. That flag is dated 2026-08-23 and was **fixed the next day** — `simulation/kit_compiler/kit_compiler.py:72` now carries `"orbit": "circle"` under change note X-1 (2026-08-24, `simulation/math/x1-orbit-spatial-map-2026-08-24.md`). VERIFIED by read. The `knockback` vocab flag stands.

## 1.3 Coverage — how many grammar templates buy how much corpus

**Method.** Two independent corpora, both counted this session:

- **Reference corpus (source material).** `vfx_archetype.member_skills` summed over 27 archetypes of run `vfx-archetype-vote-2026-08-23` = **1,135 banded skills** from 590 kits over 21 games. MEASURED over VERIFIED rows.
- **Emitted corpus (what we must ship VFX for).** All 411 files in `~/Games/reincarnated-engine/data/kit_space/kits/*.json`, `skills[].geometry_type`: **3,612 skills, 603 null, 3,009 with a value**; `chain_lightning` folded to `chain` per the read-compat alias. MEASURED.

**Two ways to count a "template", both reported:** *per-archetype* (one template per geometry name; pessimistic) and *per-grammar-family* (templates differing only in parameters share one build — all projectile variants = one trajectory template parameterised by count/pierce/fork/bounce). The family number is the one that matters for build cost, and it is the shape H-A predicts.

| N templates | Reference, per-archetype | Reference, per-family | Emitted 411-kit, per-archetype | Emitted, per-family |
|---|---|---|---|---|
| **6** | **53.3 %** | **88.0 %** | **68.0 %** | **88.0 %** |
| **10** | **74.6 %** | **99.5 %** | **87.5 %** | **99.5 %** |
| **15** | **91.7 %** | **100 %** | **96.4 %** | **100 %** |
| 20 | 96.1 % | — | 100 % | — |
| all | 100 % (n=27) | 100 % (n=11) | 100 % (n=20) | 100 % (n=11) |

**The eleven grammar families and the emitted-corpus share each buys** (MEASURED):

| Family | Folds in | Emitted share | Cumulative |
|---|---|---|---|
| **F1 Projectile** (trajectory template, parameterised) | `single_target` · `projectile` · `multi_projectile` · `fork` · `ricochet_bounce` | 37.0 % | 37.0 % |
| **F2 Self/body-attached** | `self_buff` | 15.7 % | 52.7 % |
| **F3 Ground field** | `ground_targeted_circle` · `persistent_zone` | 11.6 % | 64.3 % |
| **F4 Displacement** (owner translate) | `teleport` · `blink` · `defensive_dash` · `roll` | 9.5 % | 73.8 % |
| **F5 Placed delegate** | `totem` | 7.3 % | 81.1 % |
| **F6 Chain hop** | `chain` | 6.9 % | **88.0 %** |
| **F7 Radial expand** | `circle` · `ring` | 6.8 % | 94.8 % |
| **F8 Cone** | `cone` | 2.7 % | 97.5 % |
| **F9 Beam/channel** | `beam_channel` | 1.0 % | 98.5 % |
| **F10 Vortex** | `vortex_pull` | 1.0 % | **99.5 %** |
| **F11 Lane** | `line` | 0.4 % | 99.9 % |

**Read this result carefully — it has a trap in it.** The emitted corpus reaches 88 % on six families *because it is already grammar-poor*. Its distribution is an output of our own derivation cascade, not of the source material: nine engine geometries never appear, and the entire melee/motion half of the reference corpus (356 skills, 31 %) has no emitted counterpart. **The reference corpus is the honest denominator for "what does the genre look like", and there six archetypes buy only 53 %.** If the emitted corpus is later corrected to carry melee/motion geometry — which § 1.2 says it should be — the emitted curve moves toward the reference curve and the six-template plan stops covering.

**Operational reading:** build **F1–F6 first (88 % of what we currently emit, 6 templates)**, then **F7–F10 (99.5 %, 10 templates)**. Fifteen is past the knee — nothing between 10 and 15 buys more than a percent, and the remaining tail is `fork` (5 reference skills), `knockback` (1), `defensive_dash` (4). **Alias the tail onto its family parent rather than building it**: `fork` is F1 with a split point, `ricochet` is F1 with a bounce list, `leap_strike` is F4 with a ballistic Y.

## 1.4 Phases — shared vs grammar-specific (the primitive-alphabet question)

Phase vocabulary taken from the Hades layer stack, the only case where the layers are readable in shipped data (VERIFIED, `Fx.sjson`, plus prior findings § 3).

**Shared across every grammar — build once, reuse everywhere:**

| Phase | What it is | Hades evidence | Grammar-independent? |
|---|---|---|---|
| **P-cast flare** | short bright flash at the origin | `particle_quickflash`, 147 variants, commonest **0.1 s at α 0.5, scale 1.2 → 1.0**; sheet referenced by **30** entries | Yes |
| **P-impact burst** | flash + light disc at contact | `AuraBasicFillCircle` light disc **0.2 s** on `FX_Add_Top`; `particle_glow` referenced by **57** entries | Yes |
| **P-residual decal** | ground scorch/crack that outlives the effect | scorch **3.0 s α .85**; ground crack **1 s** | Yes |
| **P-victim response** | target tint + hit-stop + shake | `DoUnitHitFlash` Color.Red **0.03 s**; hit-stop 0.01×–0.25× for a median **0.12 s**; shake Distance median 3, Duration median 0.12 s | Yes |
| **P-dark underlay** | black-tinted duplicate of the *same* sheet on a Mix layer beneath the additive one | **56 of 78 dark sheets are the same sheet also drawn additive** | Yes — and it is the mechanism that lets an additive effect have a contour at all |

**Grammar-specific — the part that must be built per family:**

| Family | The one thing that is genuinely its own | Painted primitive it needs |
|---|---|---|
| F1 Projectile | a **head** that translates, plus a **trail** that lags it | head sprite · trail streak (Hades `Fx\BowTrailB`, `Fx\GunTrailB`, `ProjectileFire` — 11–13 entries each) |
| F3 Ground field | a **reticle/decal** and a **loop** that tiles or breathes in place | field body · ground decal |
| F4 Displacement | **owner silhouette streak** + arrival flare; no external body at all | streak (`AphroditeStreakA/B`, `SpearDashSwipe` ×10) |
| F5 Delegate | nothing of its own — the **delegate carries its own grammar** | (none) |
| F6 Chain | a **link** primitive drawn N times between N pairs of points | arc/link sprite (`ZeusStaticArcA/B/C`, 11 entries each) |
| F7 Radial | a **ring** whose radius is animated, not drawn | radial nova sheet (`Fx\RadialNova`, **16** entries off one sheet) |
| F8 Cone | a **wedge** whose aperture opens | wedge/fan sheet |
| F9 Beam | a **tileable mid-section** between a cap at each end | beam body · cap |
| F10 Vortex | an **inward** swirl, i.e. F7 with reversed radius | swirl sheet (`DemeterCycloneIn/Loop`) |
| F11 Lane | a **segment** laid flat, tiled to length | lane body |
| G11 Orbit | an **anchor + revolve transform**; the payload is an F1 head | (reuses F1 head) |
| G12 Whirlwind | **owner rotation** + a swept trail; the body is F8's wedge rotating | (reuses F8 wedge) |

**Count of genuinely new painted primitives across all eleven families: 11** — head, trail/streak, field body, decal, link/arc, ring, wedge, beam-mid, beam-cap, swirl, lane-segment — on top of five shared constants (flash, glow disc, decal, dark duplicate = the same sheet, victim tint = no sheet). That is the **primitive alphabet**, and it is the direct input to H-B.

---

# Q2 — The authoring split

| Game | Authoring method | Motion source | Where the painted register is applied | Coherence mechanism | Class · source |
|---|---|---|---|---|---|
| **Hades** | **Shared primitive sheets composed at runtime.** 5,141 named FX entries → 2,440 declare a `FilePath` → **1,152 unique sheets**; **3,396 (66 %) declare no asset at all**, inheriting one via `InheritFrom` and changing parameters. Types: Book 779 (flipbook) · Constant 705 · Random 249 · Slide 65. 992 entries carry a colour field. Prior: **112 of 126 god-variant families share one texture**, recoloured at runtime | Engine: per-frame durations, `PlaySpeed` (median 60, 30–120), runtime rotation (`AngleFromOwner=Take`, `UseOwnAngle`, `RandomFlipHorizontal`, `IsometricSkew`, `PostRotateScaleY ≈ 0.5–0.62` ground squash), velocity-driven particles. **Directionality is runtime rotation, not baked facings** | **Drawn frames.** Every footage frame is a new drawing at 60 fps; the painted read comes from flat hard-edged planes + white core + one dominant hue + dark planes, not from a low frame rate | **One greyscale sheet + runtime tint + a fixed layer stack.** The stack is invariant: additive body · black Mix duplicate · 0.1 s flash · ground nova · 1–3 s decal · light disc. The dark duplicate is what gives additive effects a contour | **MEASURED this session** (`Fx.sjson` @7e06338, parsed) + VERIFIED prior |
| **Hades II** | Same engine family; animation sjson **not public** | not sourced | Footage only: flat hard-edged planes, white core, dark interior holes, particulate residue | not sourced | MEASURED (footage, prior) · scripts VERIFIED (community copy) |
| **Children of Morta** | **Hand-drawn pixel frames** — "every frame… drawn by hand" — plus a **customised Unity render pipeline** integrating "unique lighting techniques with a standard 2D pixel art pipeline" | Hand-drawn shape layers; **HD dynamic lights** and glow are engine | **Split**: pixel-drawn shape layers on the art grid (glyph lattice, mandala at a ~3-px period); glows, beams, bolt halos smooth screen-resolution | **A bright soft glow halo + floor light, no white, no outline.** Ring around the effect **+.16 to +.41** above ground; near-white share at densest moment **0.1 %**; ground *brightens* during casts. Hue contrast is opportunistic (6°–165°), not a rule | VERIFIED (Fassihi, Game Developer postmortem) + MEASURED (prior § 2c) |
| **The Slormancer** | **Mixed by measurement.** Signature shapes and summons are pixel art on a ×4 grid with flat banded value steps (wave: 3 flat bands, flat-run share .93; summons hard-edge share .68); fire bursts, novas, rims, lightning are soft screen-resolution additive particles (hard-edge .01–.08) | GameMaker particles for the soft half; drawn frames for the pixel half | **Both, separated by layer** — the shape carries the pixel register, the glow does not | **No white anywhere + room lit in the element's colour + black "void" shapes.** 0.1 % near-white at 19–24 % effect coverage; median S .52–.81; ground takes the effect's hue (2–11° apart) so separation is by brightness | MEASURED (prior § 2d); engine VERIFIED (Steam FAQ) |
| **Chronicon** | **Particles + shaders over a pixel base**, drawn *off* the art grid at screen resolution with bloom. Patch notes name heat distortion, water ripple, glow/bloom sliders, a "reverse nova" particle type, a Particle Intensity setting "to reduce particle clutter", and a 2025 blend retune "to produce better, less over-saturated, light blending" | GameMaker particle system + post-process | **Not applied to effects** — effects are off-grid and soft while the game is a strict ×3 pixel-perfect scale (640×360 → 1920×1080) | **Weakest of the set — and it breaks.** At its densest, **22 % of the frame is near-white**: the bloom stack erases the scene | VERIFIED (Steam patch notes, app 375480) + MEASURED (prior) |
| **Dead Cells** | **3D sim/model rendered down into 2D sheets.** In-house tool renders 3DS Max models to sprites, small, no AA, cel-shaded, normal map per frame. Stated motive: "great looking pixel art, without having to hand draw each and every retake" | 3D animation + engine particles, 3D lighting, shaders | **Paint-over is replaced by render settings** — the register comes from the render (small, no AA, cel shading), not from drawing | **A single render pipeline every asset passes through** + a normal-mapped 3D lighting pass that ties everything to the scene | VERIFIED (Vasseur, Game Developer / gameanim) |
| **Diablo II** | **Pre-rendered in 3ds Max → 8-bit sprites.** 649 of 684 missiles at AnimSpeed 16 fps; `Trans=1` "darker = more transparent" on 411 of 595 | Baked. **Directions baked**: 16 dirs on 113 missiles, 32 on 98, 8 on 53, 1 on 366 | At render + palette quantisation | **A shared palette + a per-missile light (radius, RGB in data)** — the light pool is what ties a missile to the floor | VERIFIED (`fabd/diablo2` 1.13) |
| **Cuphead** | **Hand-drawn flipbook per effect** — pencil/ink on paper, coloured in Photoshop; Unity particles also used. **24 fps "on the ones"** | Drawn frame by frame | Drawn frames, entirely | **A single house style enforced by a tiny team + a period reference corpus.** The outlier: it *is* per-effect hand drawing, and it cost the studio years | VERIFIED (Moldenhauer, Game Developer) |
| **Hyper Light Drifter** | **Hand-animated**, GameMaker Studio; toolchain Photoshop + Pro Motion + After Effects + Premiere. "Everything in the game… is lovingly hand-animated" | Drawn; After Effects in the chain implies some transform-driven motion | Drawn frames | **One artist (Alx Preston) for essentially the whole surface** — the mechanism is a single hand, not a system | PRACTITIONER-REPORT (GameMaker showcase; Game Developer profile) |
| **CrossCode** | Devblog describes **engine-side particle systems** ("Environment Particles", layered at multiple depths, customisable per map, spawnable by events) and purpose-built transition effects for enemy appearance/destruction; sheet structure not published | Engine particles + sprite transforms | not sourced | not sourced | PRACTITIONER-REPORT (Radical Fish devblog) |
| **Hollow Knight** | Photoshop PNGs; Unity + 2D Toolkit; lighting "with soft transparent shapes"; Unity particles | Engine particles + drawn frames | Drawn frames | not sourced | PRACTITIONER-REPORT (Unity case study) |
| **Sea of Stars / Eastward / Moonlighter** | **Not sourced.** Searched this session; found director interviews and press kits, **no VFX-authoring statement for any of the three** | — | — | — | GAP (G-4) |
| **Anime-style 3D-posterised** (technique, not a game) | **3D sim posterised into a sheet** — EmberGen fluid sim rendered and posterised to flat stepped tones | Simulation | **Paint-over / posterise of sim frames** | Fixed tone-step count | PRACTITIONER-REPORT (80.lv) |

## 2.2 The pattern across the table

**Hand-drawn-per-effect is the minority and it is the expensive minority.** Only Cuphead (VERIFIED) and Hyper Light Drifter (PRACTITIONER-REPORT) draw every effect; both are small-team, single-hand, multi-year projects, and in both the coherence mechanism is *a person*, not a system. Every other case with primary evidence composes.

**The coherence mechanisms cluster into four, and three of them are runtime:**

1. **Shared asset + runtime tint** (Hades — 66 % of entries own no asset; D2's shared palette).
2. **A fixed layer stack applied identically to every effect** (Hades: body / dark duplicate / flash / nova / decal / light — **the strongest single mechanism in the corpus**, because it makes every effect resolve to the same silhouette-plus-glow-plus-ground reading *regardless of grammar*).
3. **A single render or light pass every asset passes through** (Dead Cells' normal-mapped 3D lighting; CoM's custom pipeline; Slormancer's element-coloured room light; D2's per-missile light pool).
4. **A single artist** — which does not scale and is not available to us.

**The register is applied in exactly one of three places** and the choice is independent of the grammar: drawn frames (Cuphead, HLD, CoM's shape layer), render settings on sim/3D output (Dead Cells, D2, EmberGen posterise), or runtime shader/blend stylisation (Hades' tint + dark duplicate; Slormancer's banded flats). Hades and Slormancer apply it in **two** places at once — drawn planes *and* a runtime layer discipline — and they are the two that read most strongly as one language.

---

# Q3 — The two live hypotheses

## H-A — *"Grammar belongs in the runtime (templates that move painted primitives), not in the sheet."*

**SUPPORTED, and no counterexample was found in any game with primary evidence.** The strongest datum is Hades' own file: of **5,141 named FX entries, 3,396 (66 %) declare no texture at all** — they inherit a parent and change parameters, and the 2,440 that do declare one resolve to just **1,152 unique sheets** (MEASURED). Grammar in Hades is unambiguously runtime: direction comes from `AngleFromOwner = Take` / `UseOwnAngle` / `RandomFlipHorizontal` and a `PostRotateScaleY ≈ 0.5–0.62` ground squash, *not* from baked facings — the exact opposite of Diablo II, which bakes 8/16/32 directions per missile and therefore pays for every grammar in asset count. D2 is the control case that shows the cost of the other choice: 684 missiles, **366 of them single-direction**, because per-direction baking is unaffordable past a point. **The corpus structure argues the same way independently**: `vfx_archetype` reports **motion purity 1.00 for every archetype that has a motion signature at all** — grammar is functionally determined by the geometry value, i.e. it is a *parameter*, not a property of the art. And § 1.4 shows the families differ by **one moving element each** (a head that translates, a radius that animates, an aperture that opens, an anchor that revolves) over a shared invariant phase stack — which is a runtime-template description by construction. **Bound:** the evidence establishes that grammar *can* live in the runtime and that the shipped exemplar does it that way; it does **not** establish that a painted register survives arbitrary runtime transform. Hades' sheets are *painted to be rotated* — radially symmetric novas, axis-aligned bolts, squashable discs. A primitive painted with a baked light direction or a hand-placed highlight will break under runtime rotation, and nothing in the corpus tests that.

## H-B — *"A painted-2D ARPG can keep one register across 15+ grammars with a primitive alphabet of ≤ ~12 painted shapes per element, tinted at runtime."*

**SUPPORTED, and now bounded numerically — the hypothesis lands almost exactly on the measured median.** Counting unique `Fx\` texture sheets per god family in `Fx.sjson` (MEASURED this session): **Zeus 8 · Poseidon 12 · Dionysus 13 · Ares 13 · Athena 15 · Artemis 10 · Hermes 10 · Aphrodite 6 · Chaos 4 · Demeter 26** — **range 4–26, median 12.5**. Eight of ten gods sit at or below 15; six at or below 13. Beneath them sits a **shared, element-agnostic particle alphabet of 105 unique sheets reducing to 46 noun-roots**, whose generic core is small and obviously reusable: `glow`, `quickflash`, `ember`, `spark`, `sparkle`, `flare`, `streak`, `trail`, `circle`, `square`, `cone`, `roundedRect`, `AuraBasicFillCircle`. Reuse within that shared layer is heavy — `particle_glow` referenced by **57** entries, `particle_quickflash` by **30**, `Fx\RadialNova` by **16**, `Fx\BasicGlow` by **14**. And § 1.4's independent derivation *from the grammar side* lands on the same order: **11 genuinely new painted primitives** plus five shared constants covers all eleven families. **Bounds and the one honest caveat:** Demeter at 26 is a real outlier and shows the number is not a hard ceiling — a god with many *distinct verbs* (beam, cyclone-in, cyclone-loop, three bow smokes) accumulates sheets faster than an element budget predicts, so **the alphabet scales with grammar count per element, not with element count**. Second, Hades ships **≈ 25 grammars over 10 gods, not 15 over one** — the per-element figure is real but the cross-grammar claim is carried by the *shared* layer (flash, glow, nova, decal, dark duplicate), not by the per-element sheets, so the honest form of H-B is **"≤ ~12 painted shapes per element *plus* a shared ~10-sheet cross-element constant layer."** Third, the two games measured as most coherent under density do it with a **layer discipline, not an alphabet size** — Slormancer holds 19–24 % effect coverage at 0.1 % near-white by banning white and tinting the room; CoM holds legibility with a +.16–.41 halo and a floor light and *no* outline. **An alphabet of 12 will not by itself produce one register; the invariant layer stack is what does that**, and it is the cheaper half to specify.

---

# Knowledge gaps not resolved

- **G-1 — Last Epoch is unbanded.** 37 LE kits in `canon_corpus` with **zero** rows in `vfx_archetype_member` (VERIFIED by query). LE is one of the brief's five source games and contributes nothing to the taxonomy; every LE cell in § 1.1 is name-evident INFERRED. **Next source:** the LE dossiers already crawled at `agentic_orchestration/legolas/research/la-postcutoff-dossiers-2026-07-16/` — an elrond banding pass over 37 kits would close this cheaply.
- **G-2 — `mortar_arc` has zero archetype members.** The thrown-arc → ground-field grammar the brief names first (GD Blackwater Cocktail, PoE Poisonous Concoction) is in the registry but no banded skill carries it, and it has **no engine geometry**. GD's Blackwater Cocktail is banded as `ground_targeted_circle`, which loses the arc. Whether the arc matters to a player is a design call, not a research finding.
- **G-3 — `spiral_out`, `sine`, `wall_sweep`** are registry entries with zero members and no engine geometry. Provenance unknown; possibly authored speculatively. Do not build against them without a source.
- **G-4 — No VFX-authoring source found for Sea of Stars, Eastward, Moonlighter.** Searched; found director interviews and press kits only. CrossCode yielded engine-particle devblog notes but no sheet structure. **Next source:** Sabotage dev streams; the `Architecture of CrossCode` series (not read, host budget).
- **G-5 — Hades II FX data is not public.** Only `Scripts/ProjectileData_*.lua` in a community copy; H2 layer structure is footage-only.
- **G-6 — Blend semantics in Hades are inferred from group names** (`_Add`, `FX_Dark`) and black tints; no renderer definition found. The per-god sheet counts in H-B count `Fx\` sheets whose *path contains the god's name*; a god whose sheets are named for the effect rather than the god would be undercounted. Treat 4–26 as a range with a **soft lower bound**.
- **G-7 — Emitted-corpus vocabulary leak not adjudicated.** 87 skills carry `roll`/`persistent_zone`, 54 carry `projectile`; none in `VALID_GEOMETRY_TYPES`, none aliased. Reported as cross-seam; fixing it is rocket's/elrond's call.
- **G-8 — The two coverage curves disagree and I did not reconcile them.** Which denominator the VFX plan sizes against is a design decision. Both are reported.
- **Blocked / not attempted (host rule):** no video decode, so no new footage measurement; Gilland *Elemental Magic* remains blocked from prior sessions; TechRaptor CoM art piece still 403.

---

# Source list (accessed 2026-09-15 unless noted)

**Primary data (VERIFIED / MEASURED this session)**
- Hades `Game/Animations/Fx.sjson` — https://raw.githubusercontent.com/xuqifzz/hades-mod-tutorial/7e06338/Game/Animations/Fx.sjson (1.88 MB; parsed, retained only in the session scratchpad)
- INTERNAL `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/corpus.db` — `motion_signature_registry`, `vfx_archetype`, `vfx_archetype_member`, `skill_geometry_band`, `canon_corpus`
- INTERNAL `/Users/admin/Games/reincarnated-engine/data/kit_space/kits/*.json` (411 files, 3,612 skills)
- INTERNAL `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/geometry_derivation.py`
- INTERNAL `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/kit_compiler/kit_compiler.py`

**Prior findings cited, not redone (INTERNAL)**
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/research/2026-09-14-vfx-oracles/findings.md`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/research/2026-09-15-chronicon-com-slormancer-vfx/findings.md`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/research/2026-09-14-vfx-style-atlas/findings.md`

**Web (this session)**
- Dead Cells — https://www.gamedeveloper.com/production/art-design-deep-dive-using-a-3d-pipeline-for-2d-animation-in-i-dead-cells-i- · https://www.gameanim.com/2018/01/31/dead-cells-3d-pipeline-2d-animation/ · https://80.lv/articles/case-study-dead-cells-character-art-pipeline
- Hyper Light Drifter — https://gamemaker.io/en/showcase/hyper-light-drifter · https://www.gamedeveloper.com/business/the-ultra-modern-stylings-of-hyper-light-drifter
- CrossCode — https://www.radicalfishgames.com/?p=2475 · https://www.radicalfishgames.com/?p=277
- Sea of Stars (no VFX source found) — https://sabotagestudio.com/presskits/sea-of-stars/ · https://lootlevelchill.com/features/sea-of-stars-sabotage-studios-interview-2025/

**Web (prior sessions, carried)**
- https://github.com/fabd/diablo2 · Cuphead (Moldenhauer, Game Developer) · https://www.gamedeveloper.com/design/postmortem-children-of-morta · Steam news API app 375480 · Steam FAQ app 1104280 · https://80.lv/articles/making-anime-inspired-stylized-3d-explosions-with-jangafx-s-embergen

— legolas (UNKNOWN-RESEARCHER), 2026-09-15
