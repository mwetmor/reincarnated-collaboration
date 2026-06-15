# drax brief — merge the 6 rooms into ONE connected dark-fantasy DESCENT scene (lit, dressed, on-theme)

**Type:** direct gandalf→drax brief, AUTONOMOUS execution (Matt is away; Matt-authorized 2026-06-15 — *"make the next piece for drax to migrate all scenes into one large scene connected by doors/portals or hallways … add ambient lighting and help him design the lighting source to fit the mood … work with him to add the scenery objects … do all of this autonomously so I see a great single scene when I get back all connected, lit better and looking like the …/modular_asset_idea_pictures theme."*).
**Date:** 2026-06-15
**Author:** gandalf (story-and-design steward — owns the mood/lighting/connection/dressing DESIGN; drax owns the scene-graph implementation + coordinates + asset resolution)
**Parent:**
- `agentic_orchestration/gandalf/notes/2026-06-15-register2-6of6-across-footprints-ruling.md` — the 6/6 ruling. Carries: circle OUT, hero bloom STAYS, ambient density REPLACES the circle (this brief delivers the density).
- `agentic_orchestration/gandalf/notes/2026-06-15-drax-brief-bake-to-scene-and-open-arena-camera.md` — the bake-to-editable-.tscn pattern (reuse it; the output here is also an editable scene).
- `reincarnated-godot/scripts/render_arena_room.gd` — the parametric room builder. The 6 baked `scenes/arena_*.tscn` are its output.
- **Reference art (the literal target):** `reincarnated-godot/Assets/Synty/polygon-dark-fantasy-01/modular_asset_idea_pictures/{theme,maps}/*.png`.

---

## 0. One line

Compose the six spec-driven battle rooms into **one connected, descending dark-fantasy crypt-to-cathedral scene** — rooms placed as rigid parity-preserved units, joined by crypt-doors / hallways / archways (the `chokepoint_corridor` *is* a connector), lit with a global cool-fog + dense warm-motivated rig that progresses in color as you descend, and dressed densely from the pack's crypt/graveyard vocabulary — so Matt opens **one editable scene** that reads like the reference art: a real place, atmospheric, lit, and alive.

## 1. The thesis — mood, dressing, and the VFX-density fix are ONE move

The 6/6 ruling owed an **ambient VFX-density** layer so the nonsensical hero summon-circle could come out. The dark-fantasy reference art shows that this is the *same* move as "look like the theme": every warm point in the maps reference is a **motivated fire source** (brazier / pyre / lantern / candelabra) distributed densely through the space. Dense motivated fire = the mood **and** the lighting **and** the distributed-highlight VFX density that carries the VFX register without the ritual disc. You are not doing three jobs; you are doing one — dress the space with light-emitting dark-fantasy props.

**What the references establish (design-binding):**
- **theme/** — global atmosphere: cool **green-teal fog** depth, warm **pinpoint** lights, gothic silhouettes receding into haze. The space is DARK; light is motivated and local.
- **maps/** — the per-zone target: a bounded combat space **densely** dressed (tombstones, banners, sarcophagi, pyres, rubble, ruins) lit by **mixed warm + cold-arcane** sources; a **portal/cathedral** doorway (magenta arcane glow) connecting levels; multi-level stone verticality (steps, arches, balustrades). This is exactly "rooms connected by portals, densely dressed" — Matt's ask, pictured.

## 2. Connection architecture — the DESCENT (this is the spine; I own the intent, you own the coordinates)

Reincarnated's own myth is a **seasonal descent**. Order the six footprints by **escalating threat = descending deeper**, so the connected scene reads as a journey from the graveyard threshold down into the cathedral sanctum:

| Order | Room | Identity in the descent |
|---|---|---|
| 1 (entry, highest) | `open_arena` (the 50×50 swarm court) | the **graveyard threshold** — wide, moonlit, first contact |
| 2 | `magic_pack` | an arcane **chamber** (candlelit, books, ritual-adjacent PROPS) |
| 3 | `elite_pack` | a deeper **hall** (pyres, banners, body-piles) |
| 4 (connector) | `chokepoint_corridor` | **literally the connecting corridor** — the tightening before the deep — darkest, gibbets along the walls |
| 5 | `mini_boss` | the **antechamber** — green soul-fire, statues, pyre-stakes |
| 6 (deepest) | `boss_with_adds` (30×30) | the **cathedral sanctum** — the magenta arcane portal focal (ref maps/8.42), flanking pyres, the climax |

**Topology:** a descending **spine**. The `chokepoint_corridor` footprint is the natural mid-spine connector (it's already a corridor — use it as one, not as an isolated room). Short **hallways / archways / crypt-doors** bridge the gaps between the other footprints. A gentle step-down in floor height per zone (even ~0.5–1.5m) sells "descent" and gives the multi-level read the references have. You choose exact world-offsets and bridge geometry.

**PARITY IS SACROSANCT (load-bearing — do not violate):** each room's **internal spawn positions + footprint come from `data/arena_scenarios.json` and must not change.** Offset each whole room as a **rigid unit** in world space; connect the *gaps between* footprints. Never move a spawn *within* a room to make a connection fit — move the *room*, or route the connector around. The engine `SpatialFightEngine` runs these exact geometries; the visual scene stays a faithful consumer (the parametric-room contract). If a connection wants space a footprint occupies, the connector yields, not the footprint.

## 3. Lighting / mood design (I own this — implement to intent)

**Global rig (one `WorldEnvironment` for the whole scene):**
- **Cool depth fog** — green-teal base (`theme/` signature), density tuned for *depth without wash*: distant zones haze out, the active fighting band stays legible. Fog is load-bearing for the reference mood — both reference sets are heavy with it.
- **Low cool ambient** — the space is dark; ambient is a faint cool fill, not a key. Keep the existing filmic tonemap + the warm-key/cold-rim/low-fill per-room rig as the *local* lighting; the WorldEnvironment is the *global* atmosphere over it.
- **Bloom/glow ON** (it's how the motivated fire reads premium — the register-2 VFX carrier).

**Motivated sources = the dressing (dense, distributed):** every warm prop that *should* emit gets a small warm `OmniLight3D` (orange ~`Color(1.0,0.55,0.20)`) + a fire `GPUParticles3D` (reuse the brazier `FX_Fire_Medium_01` / `FX_Fire_Large_01` path already wired). Braziers, **pyres** (`SM_Prop_Pyre_Stake_*_Burnt`), candelabras (`SM_Prop_Candelabra_01`), chandeliers (`SM_Prop_Chandelier_01`), candles. Density per the references — many, not a few.

**Per-zone color progression (the descent told in light):**
- **Threshold (open_arena):** cool **moonlit blue-green**, sparse warm braziers at the perimeter — exterior, liminal.
- **Chambers (magic / elite):** warmer interior amber, denser candelabra/brazier — you're inside now.
- **Corridor (chokepoint):** **darkest**, a few flickering wall-torches — dread compression.
- **Antechamber (mini_boss):** **green soul-fire** accents (necrotic green-flame braziers — tint a subset of fire emitters green; the maps reference shows green soul-flame, a dark-fantasy signature) among warm.
- **Sanctum (boss):** the **focal** — an **arcane magenta/purple** portal glow at the cathedral end (ref maps/8.42: a cool magenta `OmniLight`/emissive behind the boss marquee), flanked by the brightest warm pyres. The destination is the most-lit, most-dramatic point — the eye is pulled down the descent toward it.

The hero's **body-anchored bloom stays** (the ruling) — the player's own power. Do **not** reintroduce the `HeroSummonSigil` ritual decal as hero VFX (`USE_RITUAL_CIRCLE_PLACEHOLDER` stays false). Pack ritual/arcane *environmental* props for the magic room's identity are fine — they're dressing, not the hero's nonsensical summon disc.

## 4. Dressing design (I own the per-zone INTENT + density; you own placement + exact prefab picks)

**Density target: match the references — DENSE.** Matt explicitly wants "much more ambient objects." Err toward more. **But protect readability:** dressing goes to the **perimeter, walls, negative space, and vertical accents** — NOT into the spawn band / fighting space. Spawn positions and the engagement lane stay clear.

**The extracted vocabulary (all confirmed `.tscn`-loadable in `…/PolygonDarkFantasy/Prefabs/Props/`; you pick + place):**
- **Connectors / architecture:** `SM_Prop_Crypt_Door_01` (the door between zones), Base `Floor/Wall/Pillar` (already wired), archways from wall+pillar kits.
- **Vertical accents (the references lean on these):** banners — `SM_Prop_Flag_Dark_02`, `SM_Prop_Flag_Witch_Damaged_04`, `SM_Prop_Flag_Hero_01`, `SM_Prop_Flag_Light_02/03` (hang along walls / flank the sanctum).
- **Graveyard / crypt:** `SM_Prop_Tomb_Stone_02/03/Basic_02`, `SM_Prop_Skull_Pile_01` (wired), `SM_Prop_Skull_04`, `SM_Prop_Bones_Rotten_01`, `SM_Prop_Body_Skeleton_02/03`, `SM_Prop_Body_Pile_Burnt_01`.
- **Dread set-dressing:** `SM_Prop_Gibbet_01_Damaged_01` / `_Body_01` (hanging cages — line the corridor), `SM_Prop_Noose_Knot_01`, `SM_Prop_Pyre_Stake_01/02_Burnt_*` (burning stakes — emit fire), `SM_Prop_Statue_People_02`, `SM_Prop_Demon_01`.
- **Interior clutter (chambers/sanctum):** `SM_Prop_Candelabra_01`, `SM_Prop_Chandelier_01`, `SM_Prop_Candle_04/08/09`, `SM_Prop_Pew_01_Damaged_01`, `SM_Prop_Bookshelf_*`, `SM_Prop_Table_*`, `SM_Prop_Well_01`.
- **Assembly reference:** `…/PolygonDarkFantasy/Scenes/Demo_Graveyard_01.tscn` (Synty's own dressed demo — mine it for placement density + grouping), and your prior `scenes/dark_fantasy_cathedral.tscn` experiment.

**Per-zone dressing identity:** threshold = graveyard (tombstones, skull-piles, dead bones, damaged banners, perimeter braziers). magic = arcane study (candelabra, bookshelves, candles, papers). elite = war-hall (pyres, banners, barricades, body-piles). corridor = oubliette (wall-gibbets, noose, bones underfoot, sparse torches). antechamber = execution-ground (pyre-stakes, statues, green soul-braziers). sanctum = cathedral (pews flanking an aisle to the boss, chandelier, big banners, statues, the arcane portal). Connective hallways: crypt-doors, wall-sconces, bones lining the floor.

## 5. The summon-circle carry (from the 6/6 ruling — do not re-litigate)

- `USE_RITUAL_CIRCLE_PLACEHOLDER` **stays false.** The hero ritual disc is out for good.
- The hero's **body-anchored fire bloom + glow + lifecycle stay** (the A-holds-validated own-power VFX).
- The **distributed environmental fire** this brief adds is the density layer that lets the circle stay out *and still pass VFX*. That's the whole point of the dressing being light-emitting.

## 6. Constraints (acceptance-binding)

1. **Parity sacrosanct** (§2) — spawn positions + footprints unchanged; rooms offset as rigid units.
2. **Register-2 must HOLD** — the connected scene must still read register-2 (lighting ≥4, VFX ≥4) per room/zone. Denser motivated fire *helps* VFX; do not let fog wash the lighting drama or the readability.
3. **Readability** — combat bands stay legible; dressing to perimeter/verticality.
4. **One editable scene** — output is a **single openable `.tscn`** (reuse the bake-to-scene pattern: build procedurally if you like, but Matt must be able to open ONE scene and explore it; set `.owner` recursively so nothing drops on pack/save — the gotcha from the bake brief).
5. **Camera** — give Matt an impressive **establishing/overview** view of the whole descent on open (the "wow"), AND preserve the per-room capture cameras so Galadriel can still lifecycle-score each zone. A slow overview orbit or a fixed dramatic establishing angle down the descent spine is ideal.
6. **No engine repo writes** — this is all `reincarnated-godot/`. `arena_scenarios.json` is read-only authority here.

## 7. Build stages (self-staged; commit between)

- **Stage 1 — Connect + light.** Place the 6 footprints along the descent spine (parity-rigid), bridge with crypt-doors/hallways/archways, step the floor heights, stand up the global `WorldEnvironment` (cool fog + bloom) and the per-zone color progression. Commit. *Acceptance: one scene you can walk/fly through end-to-end; the descent reads; rooms are connected; nothing dropped on save.*
- **Stage 2 — Dress dense + motivated fire.** Per-zone dressing identities (§4) at reference density; every warm source emits (light + fire). Commit. *Acceptance: each zone reads as its dark-fantasy identity; the space is densely dressed but the fighting bands stay clear; the arcane sanctum portal is the focal pull.*
- **Stage 3 — Establishing camera + final pass.** The overview camera; a readability/parity sanity check; commit.
- Then **handoff to galadriel** (via gandalf) to capture + score register-2 across the connected zones AND visual-similarity vs the `modular_asset_idea_pictures` references. gandalf interprets + iterates with you.

**Commit locally** (auto-commit in-scope per the team addendum). **Do not push** (Matt-gated; local commits are enough for Matt to open the scene). Leave an `AGENT_STATE.md` note + a one-paragraph report back to gandalf with: the scene path, the descent layout you chose, any asset that failed to load (so I can adjust), and anything where the design intent fought the footprint geometry.

## 8. Roles / acceptance

- **drax:** the build (connect + light + dress + camera + bake to one editable `.tscn`); asset resolution + coordinates + scene-graph are yours; surface anything where intent fought geometry.
- **gandalf:** owns mood/lighting/connection/dressing **intent**; reviews the result; iterates with you; interprets galadriel; the canon record.
- **galadriel:** captures the connected scene; scores register-2 (gates hold) + similarity vs the dark-fantasy references; her frames are how gandalf judges theme fidelity.
- **Acceptance:** Matt opens ONE editable scene and sees a connected, descending, densely-dressed dark-fantasy crypt-to-cathedral that reads like the reference art — lit better, alive, on-theme — with parity preserved and register-2 holding.

---

**Signed:** gandalf, 2026-06-15
**For:** the autonomous connected-scene build — merge the six parity-preserved battle footprints into one descending crypt-to-cathedral dark-fantasy scene (rigid-unit offsets + crypt-door/hallway connectors, the chokepoint corridor as a literal connector, stepped floor heights for the descent read), lit with a global cool-fog + dense warm-motivated rig that progresses threshold-blue → chamber-amber → corridor-dark → antechamber-green-soulfire → sanctum-arcane-magenta, dressed densely per-zone from the extracted crypt/graveyard vocabulary (the motivated-fire dressing IS the ambient VFX-density that retires the summon circle), output as one editable .tscn with an establishing overview camera, register-2 and parity both held, verified by galadriel against the reference art.
