# Addendum — Enemies: animation routes for the 19 tier-1 rigs — 2026-10-02

**Mode:** A (analytical), read-only. This continues `README.md` in this folder; its confidence key and download settings still apply.
**Commissioner:** gandalf (Run C-9). Matt wants the crucible enemies built tonight with their animations and VFX.
**Input:** the crucible enemy roster packet, collab `d51b3c47a`, `agentic_orchestration/legolas/research/2026-10-02-crucible-enemy-roster-packet/` (`roster.json`, `README.md`). Tier 1 is 19 rigs carrying 139.8 of 172.0 expected bodies (81.3 %).
**Naming rule:** rows are keyed by the roster's `type_id` only. Every body description is generic. Don't paste a roster display name into any image, mesh or animation prompt.

**Evidence tags used here (in addition to M / L / T / 1 / I from `README.md`):**

| Tag | Meaning |
|---|---|
| **[R]** | Read from `roster.json`: core clip names, ability kinds, emergence windows, bone counts, and the bind-pose mesh bounding box. The roster grades the box DATAMINED, in mesh units, with its Lap F caveat. |
| **[S]** | Read from an official SDK or API schema: the Tripo Python SDK on GitHub, fal's OpenAPI schema, and Meshy's docs. |
| **[K]** | My knowledge of the creature *archetype*. I couldn't inspect the meshes or bones because the Edition III creature archives aren't on disk any more; only Edition II and IV are present, and neither has `Creatures.arc`. |

---

## 0. Short answer

| Route | Rigs | Expected bodies (share of all 172) | Tonight [I] |
|---|---|---|---|
| **Mixamo clips on a humanoid auto-rig** (Meshy rig through fal, or the existing C-9 retarget lane) | 12 | **87.0 (50.6 %)** | **6–10 rigs** |
| **Blender** (local Blender 5.2 + Rigify animal metarigs, simple keyed cycles) | 7 | **52.8 (30.7 %)** | **2–4 rigs** |
| Tripo non-biped auto-rig | 0 as primary | — | Needs a new key. It only gives a walk cycle (§ 3a). |
| Painted 8-heading sprites (C-3..C-8 pipeline) | 0 as primary | — | Fallback only. A style clash in a 3D arena (§ 3c). |

**What Matt should download for enemies:**
1. Creature Pack
2. Not So Scary Zombie Pack
3. Scary Zombie Pack
4. 7 singles

Pro Magic Pack is already on the hero list. The detailed list is in § 4.

---

## 1. Body plan per rig

**How to read the bounding-box ratio.** The roster stores each lead mesh's bind-pose box. Height ÷ depth ≥ about 1.3 together with width ≥ depth (arms out in a T- or A-pose) reads as a **biped**. Height ÷ depth below 1 with depth ≥ width reads as a **long or low body** [I on the rule].

| # | `type_id` | bodies | Body plan (generic) | Evidence | Box W × D × H (mesh units), H/D | Conf. |
|---|---|---|---|---|---|---|
| 1 | `aetherialcorruption` | 17.78 | **Biped brute.** Hulking mutated humanoid with oversized arms. | R walk/run/idle; K | 2.54 × 1.18 × 2.98, **2.5** | high |
| 2 | `wraith` | 15.52 | **Floating.** Hooded spectral humanoid upper body that glides. The roster has **no walk clip**, only a "run" glide. | R; K | 3.28 × 2.08 × 4.41, 2.1 | high |
| 3 | `devourer` | 13.02 | **Quadruped, low crawler.** Toothed maw that spits. | R `attackspit`, low box; K | 2.68 × 2.93 × 2.10, **0.71** | medium |
| 4 | `crabmonstrosity` | 11.51 | **Hexapod-crab.** Many legs plus two claws, breathes frost. | R `breathice`; box; K | 2.98 × 3.02 × 2.16, **0.72** | high |
| 5 | `golemswamp_phase01` | 9.03 | **Biped brute, huge.** Mud-and-vine golem. Its "run" is a slow walk (91 frames). It rises from the ground. | R `appearance` clip, run=walk; K | 5.0 × 3.61 × 6.30, 1.7 | high |
| 6 | `hero01_unarmed` | 7.91 | **Biped humanoid (male), caster.** Ghostly spawn. | R (player-class skeleton, 56 bones) | humanoid | high |
| 7 | `sandlizard` | 7.46 | **Long-bodied reptile.** It has a leap attack. Whether it is a raptor-like biped or a low quadruped is **undetermined**. The box is narrow and very long; its take-hit clip is borrowed from the 45-bone `wendigo` rig, which hints at a biped. | R `attackspecial_c01_leap`, shared hit clip; box | 1.43 × 5.47 × 2.70, **0.49** | low |
| 8 | `wendigo` | 6.04 | **Biped brute, gaunt and hunched.** Long limbs and a beast head. Howl, double slash, ram. | R; K | 4.23 × 3.15 × 4.70, 1.5 | high |
| 9 | `aetherialimp` | 5.98 | **Small biped.** Hunched, quick, melee. | R; box | 3.55 × 1.30 × 3.72, **2.9** | medium |
| 10 | `carnivorousplant01a_p1` | 5.87 | **Stationary plant.** Snapping bulb, spit projectile, 1.5 s sprout. Never rotates. | R `ControllerStationaryMonster`, run = combat idle | 20.3 × 21.3 × 14.5, 0.68 | high |
| 11 | `basilisk` | 5.78 | **Quadruped reptile.** Breath attack and "petrifying glare". | R `breath`, `petrifyingglare`; box; K | 3.0 × 5.23 × 3.78, **0.72** | medium |
| 12 | `cannibal` | 5.65 | **Biped humanoid, hunched.** Melee, plus a throw-like cast for its projectile. | R; box | 3.09 × 0.93 × 3.94, **4.2** | high |
| 13 | `thornedhorrora01` | 5.07 | **Quadruped brute, spiked.** Cross-swipe and a triple ground impale. | R; box; K | 4.33 × 5.12 × 4.80, **0.94** | low–medium |
| 14 | `skeleton_01a` | 5.03 | **Biped humanoid skeleton, caster.** Rises from the ground (61-frame spawn). | R; box | 1.68 × 0.51 × 2.54, **5.0** | high |
| 15 | `heroine01_unarmed` | 4.29 | **Biped humanoid (female), caster.** Ghostly spawn. | R (player-class skeleton, 49 bones) | humanoid | high |
| 16 | `voidfiend` | 4.04 | **Unknown compact non-biped.** It vomits acid. It could be a squat crawler or a floating mass. | R `cast_barfacid`; box | 3.0 × 2.74 × 2.62, **0.96** | low |
| 17 | `chthonianrylok` | 3.48 | **Biped brute, large.** Some variants are winged: their box is 10 units wide. Roar spawn. | R `roar` spawn; box; K | 3.85 (10.1 winged) × 3.06 × 5.30, 1.7 | medium–high |
| 18 | `aetherialbloater` | 3.28 | **Obese biped (uncertain).** Bite and vomit. The box is nearly a cube. | R `bite`, `vomittriple`; box | 3.94 × 4.07 × 4.16, **1.02** | low–medium |
| 19 | `yeti` | 3.04 | **Biped brute, large and furry.** Roar, frost breath, slam. | R; box; K | 4.86 × 2.98 × 5.53, 1.9 | high |

**Emergence for the p05 ambush [R]:**

| Rig | Clip | Window |
|---|---|---|
| `aetherialcorruption` | spawn | **2.45–4.9 s** |
| `golemswamp_phase01` | appearance | **3.57 s** |
| `aetherialimp` | spawn | **1.53 s** |
| `wraith` | spawn | **0.87 s** |
| `carnivorousplant01a_p1` | sprout | **1.5 s** |
| `chthonianrylok` | roar | **1.4–1.87 s** |
| `chthonianrylok` | fire spawn | **3.5 s** |

---

## 2. Bipeds: the Mixamo route (12 rigs)

**Pipeline [I].** Generate the mesh, then auto-rig it as a humanoid, then retarget Mixamo FBX clips. This is the lane C-9 has already proven on the dark knight.

**Humanoid only [S].** Both humanoid auto-riggers we can reach today are humanoid-only:
- **fal `fal-ai/meshy/rigging`** and **`fal-ai/meshy/rigging/multi-animation`**. fal's schema says *"The model must be a humanoid character with clearly defined limbs."* fal is already paid for.
- **Meshy direct**, using `MESHY_API_KEY`, which is set in this environment. Meshy's docs say *"Non-humanoid assets"* are unsuitable for auto-rigging.

**In-Place.** The **IP** column is Mixamo's *supports In-Place* flag [M]. Leave In Place off when downloading (see README § 1.1). Every id below is the first 8 hex digits of the Mixamo product id.

### 2.1 The shared enemy clip set (sources for the per-rig picks) [M]

| Pack / single | Clip (file in zip) | Mixamo description | id | IP | Len |
|---|---|---|---|---|---|
| **Creature Pack** | `mutant breathing idle` | Mutant Breathing Idle | `c9c93f13` | no | 4.0 |
| | `mutant idle` / `(2)` | Stretching Idle With Breathing / Stretching Idle | `c9c93e57` / `c9c940be` | no | 14.2 / 5.3 |
| | `mutant walking` | Mutant Brutal Walk | `c9c93a8c` | **yes** | 1.4 |
| | `mutant run` | Mutant Running | `c9c93cdc` | **yes** | 0.87 |
| | `mutant swiping` | Mutant Attacking With **Left** Hand | `c9c93c1d` | no | 2.67 |
| | `mutant punch` | Quick **Left** Handed Punch | `c9ccb404` | no | 1.1 |
| | `jump attack` / `mutant jump attack` | Mutant Jump Attack To Ready Pose / To Idle | `c9c95cf0` / `c9c95db7` | no | 1.4 |
| | `mutant roaring` | Mutant Roaring | `c9ccb4c2` | no | 5.4 |
| | `mutant flexing muscles` | Flexing From Standing Idle | `c9c94c6f` | no | 4.67 |
| | `mutant dying` | Dying Falling Onto Back | `c9c93d98` | no | 4.6 |
| | turns (5) | 45° and 90° turns | `c9c93242`… | no | 1.3–2.4 |
| **Not So Scary Zombie Pack** | `walking` / `walking (2)` | Zombie Walking / Creeping Zombie Walk | `c9c60315` / `c9c61776` | **yes** | 4.4 / 4.03 |
| | `zombie running` | Zombie Run | `c9c6b0ab` | **yes** | 0.8 |
| | `zombie idle` … `(4)` | Alert · Looking Around · Twitching · Upright Twitching | `c9c6726b` `c9c67dc0` `c9c6b3ad` `c9c6b467` | no | 3.2–6.1 |
| | `zombie punching` / `(2)` | Jab Punch Right Arm / Attack With Right Hand | `c9c67f8b` / `c9c68115` | no | 1.0 / 2.6 |
| | `zombie headbutt` | Headbutt With Hand Grab | `c9c68200` | no | 2.93 |
| | `zombie attack` | **Overhead Two-Hand Attack** | `c9c713dd` | no | 4.5 |
| | `zombie reaction hit` / `(2)` | Flinches / Stumble Back | `c9c68a0f` / `c9c68ad5` | no | 2.0 / 2.17 |
| | **`zombie stand up`** / `(2)` / `(3)` | **Laying On Back / Side / Stomach To Standing Up** | `c9c6b165` / `c9c6b22d` / `c9c6b2ed` | no | **3.07** / 5.77 / 6.0 |
| | `zombie turn` | Turning Right Standing In Place | `c9c6b520` | yes | 1.93 |
| **Scary Zombie Pack** | `zombie walk` / `zombie run` / `zombie idle` | Walking / Running / Standing Idle | `c9cbd4d9` / `c9cbd905` / `c9cbd649` | yes / yes / no | 4.17 / 0.8 / 4.33 |
| | `zombie attack` | Zombie **Swipe** Attack | `c9cbd7ad` | no | 2.6 |
| | `zombie neck bite` | Repeatedly Biting A Neck | `c9cbdbba` | no | 4.17 |
| | `zombie scream` | Zombie Screaming | `c9ccbc37` | no | 1.3 |
| | `zombie death` / `zombie dying` | Hit, Falling Onto Back / Falling Forward | `c9cbda5a` / `c9cc240a` | no | 2.97 / 3.33 |
| | `zombie crawl` / `running crawl` | Crawling Forward / Running On All Fours | `c9cbee0c` / `c9cca748` | yes | 5.13 / 0.57 |
| **Singles** | Treading Water | *"Floating"*: upright hover, legs tucked [T] | `c9c858e6` | no | 2.17 |
| | Floating | *"Floating In Air Flailing Arms"* | `c9c6d01a` | no | 3.57 |
| | Throw | *"Throwing An Object From A Standard Pose"* | `c9cb09fa` | no | 2.17 |
| | Throw Object | *"Picking Up Object And Throwing"* | `c9c9da9b` | no | 4.87 |
| | Big Stomach Hit | *"Receiving A Big Hit In The Stomach"* | `c9cafc81` | no | 1.4 |
| | Flying Back Death | *"Dying Flying Backward"* | `c9cdb4c8` | no | 3.0 |
| | Roar | *"Belting Out A Load Roar"* | `c9c79f59` | no | 6.23 |
| **Pro Magic Pack** (on the hero list) | idle · walk · run · 1H Magic Attack 01 · 2H Area Attack 01/02 · 2H Cast Spell 01 · React Small/Large · Death ×4 | see README Appendix A | | walk/run yes | |

**Pack containment [M]:** Creature NPC Pack (12) is a strict subset of Creature Pack (19), so skip it.

**Hover clips [T]:** "Flying" (`c9c78916`) is a horizontal superhero flight, not an upright hover; **use Treading Water for the wraith's hover.**

### 2.2 Per-rig picks

`L` means the clip uses the left hand. Use Mixamo **Mirror** for a right-hand version (README § 1.1).

| `type_id` | idle | walk / run | melee | projectile | aoe / aura / buff | hit | death | emergence (p05) | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `aetherialcorruption` | mutant breathing idle | mutant walking / mutant run | mutant swiping (L, mirror for R) · zombie attack (overhead slam) for the charge-pincer | **mutant roaring** (the roster's projectile is a roar-nova) | mutant flexing (aura) | zombie reaction hit (2) | mutant dying | **zombie stand up** (from back, 3.07 s) fits the 2.45–4.9 s window natively | The largest rig: 17.8 bodies. Do it first. |
| `wraith` | **Treading Water** (hover) | the same hover plus glide translation; no walk is needed (R) | scary-zombie attack (swipe) | Pro Magic 1H Magic Attack 01 | Pro Magic 2H Area Attack 02 (aura/aoe) · 2H Cast Spell 01 (buff) | Pro Magic React Small Front | Flying Back Death | 0.87 s: a fade-in/scale VFX, no clip | Legs are hidden under the robe or wisps [I]. A procedural bob suits it. |
| `golemswamp_phase01` | mutant idle (2) | mutant walking, slowed; the "run" is a walk (R) | zombie attack (overhead two-hand) | **Throw Object** (pick up and throw) | mutant jump attack (ground slam) · mutant roaring (plant summon) | zombie reaction hit (2) | mutant dying | **zombie stand up** (from back, 3.07 s) at ×0.86 = **3.57 s** | Big and slow. Root-motion scale matters. |
| `hero01_unarmed` | Pro Magic idle | Pro Magic walk / run | — (projectile 40 %, aoe 39 %) | 1H Magic Attack 01 | 2H Area Attack 01 / 02 · 2H Cast Spell 01 | React Small/Large | React Death ×4 | 14-frame ghost spawn: VFX fade | The Pro Magic posture is fine for an enemy caster. |
| `wendigo` | mutant breathing idle | mutant walking / mutant run | mutant swiping (L/R) for the double slash · zombie headbutt for the ram | Throw | **mutant roaring** (howl aura) | Big Stomach Hit | mutant dying | — | |
| `aetherialimp` | zombie idle (3) (twitching) | walking (2) (creeping) / **running crawl** (all fours, 0.57 s) | zombie punching (jab) · mutant punch | — | zombie scream (aoe tell) | zombie reaction hit | zombie dying | **zombie stand up** (back) at ×2 = **1.53 s** | Scale the rig small. |
| `cannibal` | zombie idle (alert) | walking / zombie running | zombie punching (2) · zombie attack | **Throw** (2.17 s) | zombie scream (buff) | zombie reaction hit | zombie death | — | |
| `skeleton_01a` | Pro Magic idle | scary-zombie walk / zombie run (or Pro Magic) | — | 1H Magic Attack 01 | 2H Area Attack 01 · 2H Cast Spell 01 | React Small | React Death Backward | 61-frame spawn: **zombie stand up** (back) at ×1.5 ≈ 2.0 s | |
| `heroine01_unarmed` | Pro Magic idle | Pro Magic walk / run | — | 1H Magic Attack 01 · 1H Cast Spell 01 | 2H Area Attack 02 | React Small | React Death ×4 | ghost spawn: VFX fade | |
| `chthonianrylok` | mutant breathing idle | mutant walking / mutant run | mutant swiping · mutant punch | mutant roaring | **mutant jump attack** (aoe slam) | Big Stomach Hit | mutant dying | **mutant roaring** = the 1.4–1.87 s roar spawn | Wings on some variants need a procedural flap [I]. |
| `aetherialbloater` | mutant breathing idle | scary-zombie walk / mutant walking | **zombie neck bite** (bite) · zombie attack | **zombie scream** (vomit lean-forward) | mutant roaring (worm summon) | zombie reaction hit | mutant dying | — | ⚠ The body plan is uncertain. If the generated mesh lacks clear limbs, the humanoid rigger fails and this rig moves to Blender. |
| `yeti` | mutant idle (2) | mutant walking / mutant run | mutant swiping | **Throw Object** | mutant roaring (roar aura/buff) · mutant jump attack (slam) | Big Stomach Hit | mutant dying | — | |

**Clips Mixamo can't supply for these rigs [M]:**
- Breath attacks: the frost and blood breaths on `yeti`. Use a roar pose held under a cone VFX [I].
- A ground-impale stomp. The closest is `Stomp` (*"Hard Floor Stomp"*, `c9cca5cc`, 1.83 s).
- Wing motion.

---

## 3. Non-bipeds: routes and evidence (7 rigs)

### (a) Auto-rigging services

**Tripo [S]**, from the official Python SDK (`VAST-AI-Research/tripo-python-sdk`, `tripo3d/models.py` and `client.py`, last commit 2026-06-30):
- **Rig types:** `biped`, `quadruped`, `hexapod`, `octopod`, `avian`, `serpentine`, `aquatic`, `others`.
- **Rig spec:** `mixamo` or `tripo`.
- **Preset animations:** `preset:idle`, `walk`, `run`, `dive`, `climb`, `jump`, `slash`, `shoot`, `hurt`, `fall`, `turn`, plus **one** locomotion preset for each non-biped type: `preset:quadruped:walk`, `hexapod:walk`, `octopod:walk`, `serpentine:march`, `aquatic:march`.
- **Tasks:** `animate_prerigcheck`, `animate_rig`, `animate_retarget` (with an `animate_in_place` flag). `import_model` takes an external GLB, OBJ, FBX or STL, so **meshes made through fal can be imported and rigged.**

**What the SDK does not say [unknown]:** whether `idle`, `run`, `slash`, `hurt` and the other generic presets apply to non-biped rigs. If they don't, a quadruped or hexapod gets **only a walk** from Tripo. Attacks, idle, hit and death must then be keyed anyway.

**Access [S + local check]:**
- **fal has no Tripo rigging endpoint.** fal's model catalogue for "tripo" lists generation, segment and remesh only. A search for "rig" returns only `fal-ai/meshy/rigging` and `fal-ai/meshy/rigging/multi-animation`.
- **Tripo rigging needs Tripo's own API key.** The SDK reads `TRIPO_API_KEY` (prefix `tsk_`) and calls `api.tripo3d.ai`. **No such key is set here.** Getting one is a Matt to-do (account and credential).
- **Tripo pricing:** unknown. The platform docs page renders client-side and returned nothing to fetch.

**Meshy (fal or direct):** humanoid only [S]. Not a non-biped route.

### (b) Blender procedural rigs with simple keyed cycles

**Available locally [L]:**
- **Blender 5.2.0 LTS** is installed (`/opt/homebrew/bin/blender`, `/Applications/Blender.app`).
- The bundled **Rigify** add-on ships these metarigs: `Basic/basic_quadruped`, `Animals/wolf`, `cat`, `horse`, `bird`, `shark`, plus `human`.
- There is **no hexapod or serpent metarig**. A crab means a custom bone chain per leg [I].

**Method [I]:**
1. Fit the metarig to the generated mesh and generate the rig.
2. Script the cycles headless in Python:
   - phase-offset leg lifts for walk and run (alternating tripod for six legs);
   - a breathing bob for idle;
   - a lunge and jaw/claw snap for melee;
   - a rear-back for breath or spit;
   - a flinch for hit;
   - a roll-over or collapse for death;
   - a scale-and-translate up from below ground for emergence.
3. Export GLB to Godot.

Six to eight short clips per rig is about the same clip count as the bipeds' Mixamo set.

### (c) Painted per-frame sprites (the C-3..C-8 pipeline)

**What a full character costs [L, C-3/C-6 ledgers]:**
- 5 animations × 8 directions = **40 cells**.
- Grok image-to-video per clip, cut and matted per cell.
- C-6 shipped **25 cells**: 15 unique plus 10 mirrored. The remaining 15 were blocked on seeds.

**Why it's a fallback here [I]:**
- **Style clash:** the C-9 crucible characters are **3D in Godot**. 2D billboard enemies among 3D heroes would clash, and they lock the camera to the painted angle (53°).
- **Throughput:** past runs took days per character, so it is not a "tonight" route for 7 rigs.
- **Where it still fits:** a stationary or nearly rotation-free body, where one heading suffices. The plant qualifies, but Blender is simpler there too.

### Route per non-biped rig

| `type_id` | bodies | Route | Why | Clips to key |
|---|---|---|---|---|
| `crabmonstrosity` | 11.51 | **Blender, custom 8-leg + 2-claw chain.** Tripo `hexapod`/`octopod` + `walk` preset if a key exists. | Highest-body non-biped. Tripo would give the walk only. | idle, walk, run, claw strike ×2, frost breath (rear-back), hit, death |
| `devourer` | 13.02 | **Blender Rigify `basic_quadruped`** | Low crawler | idle, run, bite ×2, spit (aoe), hit, death |
| `basilisk` | 5.78 | **Blender Rigify `wolf` or `cat`** (long body + tail) | | idle, walk, run, breath, glare (head-raise hold), bite, hit, death |
| `thornedhorrora01` | 5.07 | **Blender Rigify `basic_quadruped`** | Body plan low–medium confidence: check the mesh | idle, walk, run, cross-swipe, ground impale ×3, cast, hit, death |
| `sandlizard` | 7.46 | **Blender** (quadruped metarig; switch to a digitigrade biped chain if the mesh stands upright) | Body plan undetermined (§ 1) | idle, walk, run, leap attack, bite/claw, hit, death |
| `voidfiend` | 4.04 | **Blender**, after a 5-minute look at the generated mesh | Body plan unknown | idle, move, acid spit, aoe slam, buff, hit, death, 3.2 s spawn |
| `carnivorousplant01a_p1` | 5.87 | **Blender, keyed bone chain** (stem + jaw) | Stationary, never rotates (R) | sway idle, snap bite, spit, hit, wilt death, **1.5 s sprout** (scale-up from the ground) |

---

## 4. Download list for Matt (enemies), in order

Use the same settings as `README.md` § 1.1: FBX Binary, 30 fps, no keyframe reduction, Without Skin, In Place **off**.

| # | Download | Count | Covers |
|---|---|---|---|
| 1 | **Creature Pack** | 19 [M] | Brute bipeds: idle, walk, run, swipe, punch, jump slam, roar, flex, death. Used by 7 rigs. **Skip Creature NPC Pack (subset).** |
| 2 | **Not So Scary Zombie Pack** | 24 [M] | **Zombie Stand Up ×3** (all p05 emergences), creeping walk, run, punches, overhead slam, hit reacts, idles |
| 3 | **Scary Zombie Pack** | 12 [M] | Swipe, neck bite, scream, running crawl, two deaths |
| — | Pro Magic Pack | (hero list #1) | Casters: `hero01_unarmed`, `heroine01_unarmed`, `skeleton_01a`, `wraith` casts |
| 4 | **Treading Water** | single, `c9c858e6` | `wraith` hover |
| 5 | **Throw** | single, `c9cb09fa` | `cannibal`, `wendigo` |
| 6 | **Throw Object** | single, `c9c9da9b` | `golemswamp_phase01`, `yeti` |
| 7 | **Big Stomach Hit** | single, `c9cafc81` | Heavy hit react |
| 8 | **Flying Back Death** | single, `c9cdb4c8` | `wraith` death |
| 9 | Roar | single, `c9c79f59` | Already on the hero list |
| 10 | Stomp | single, `c9cca5cc` | Optional ground-impale tell |

That is **3 packs (55 clips) plus 6 new singles.**

**What can be covered tonight [I].** These are estimates; the basis is stated with each.

| Route | Rigs | Basis |
|---|---|---|
| **Mixamo** | **6–10 of the 12** | Mesh generation, then Meshy humanoid rig on fal (1–3 min per rig, per fal's endpoint note [S]), then a batch retarget of about 8 clips on the existing C-9 lane. In body order, the first six (`aetherialcorruption`, `wraith`, `golemswamp_phase01`, `hero01_unarmed`, `wendigo`, `aetherialimp`) are **62.3 bodies, 36 % of all**. |
| **Blender** | **2–4 of the 7** | About 1–2 h per rig for metarig fit plus 6–8 scripted cycles. Do them in body order: `devourer` 13.0, `crabmonstrosity` 11.5, `sandlizard` 7.5, `carnivorousplant01a_p1` 5.9. |
| **Tripo** | 0 | No key. A key only buys a walk cycle. |
| **Painted** | 0 | Not recommended tonight. |

## 5. Gaps and risks

1. **Body plans for `sandlizard`, `voidfiend`, `thornedhorrora01` and `aetherialbloater` are inferred.** They rest on bounding-box ratios and archetype knowledge, because the creature archives are no longer on disk. Check each generated mesh before choosing the rig template.
2. **Humanoid auto-riggers reject unclear limbs [S].** Bloated or hunched brutes (`aetherialbloater`, `wendigo`) may fail Meshy's rigger. The fallbacks are Tripo `biped`/`others` (needs a key) or Blender `human` Rigify.
3. **Mixamo has no breath attacks, no wing motion and no non-biped motion at all [M].** Those need VFX over a held pose, or keyed bones.
4. **Mixing capture families on one rig** (Creature/mutant with zombie clips) changes stance width between states [T]. The C-9 retarget lane's stance checks apply.
5. **Licence:** as in README § 2. Enemy FBX files stay out of git, and retargeted clips stay out of the **public** collaboration repo.

## 6. Sources

- **Roster packet** `d51b3c47a`: `roster.json` (types, abilities, clips, `members_detail[].mesh_aabb_*`, spawn notes) [R].
- **Mixamo public catalogue API.** Pack lists for Creature, Creature NPC, Scary Zombie and Not So Scary Zombie packs; details for about 90 additional clips; thumbnails viewed for hover, float, stand-up, crawl and scream [M][T].
- **Tripo Python SDK:** <https://github.com/VAST-AI-Research/tripo-python-sdk> (`tripo3d/models.py`, `tripo3d/client.py`), read via `gh api` [S].
- **fal model catalogue** (`https://fal.ai/api/models?keywords=tripo|rig|rigging|animate`) and the OpenAPI schemas for `fal-ai/meshy/rigging` and `fal-ai/meshy/rigging/multi-animation` [S].
- **Meshy rigging docs:** <https://docs.meshy.ai/en/api/rigging-and-animation> [S].
- **Local:**
  - Blender 5.2.0 and its Rigify metarig list.
  - C-3 and C-6 ledgers (cell counts).
  - C-9 scripts (`tripo3d/h3.1/multiview-to-3d` on fal, used for gear builds).
  - Environment variable names (no values read).
- **Not reachable:**
  - Tripo platform docs and pricing (client-rendered).
  - Edition III creature archives (removed from disk).
  - General web search (session budget spent).
