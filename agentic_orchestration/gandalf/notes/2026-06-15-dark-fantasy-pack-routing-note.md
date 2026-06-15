# POLYGON Dark Fantasy pack — design read + routing note (drax · galadriel · KR)

**Type:** routing + framing note (gandalf → drax / galadriel / KR). New on-theme asset drop staged by Matt.
**Date:** 2026-06-15
**Author:** gandalf (story-and-design steward)
**Authority:** Matt-authorized 2026-06-15 (Pattern-B) — *"yes, drop the routing note."*
**Parent:** `agentic_orchestration/gandalf/notes/2026-06-15-godot-register2-a-holds-ruling.md` (A-holds — this pack is the chance to re-validate it on REAL curated content vs the graybox it was proven on).
**Asset paths:**
- Pack root: `~/Games/reincarnated-godot/Assets/Synty/polygon-dark-fantasy-01/`
- Godot-import models/prefabs/materials/textures: `…/Assets/Synty/PolygonDarkFantasy/{Models,Prefabs,Materials,Textures,Scenes}`
- Source FBX (8 categories): `…/SourceFiles/FBX/{Characters,Weapons,Buildings,Environment,Props,FX,Vehicles,Misc}`
- **Reference frames** (Matt-curated, from the Synty pack page): `…/modular_asset_idea_pictures/{maps,theme}/`

---

## 0. One line

The strongest on-theme content drop yet: register-2 in the frames, uncannily on-theme (purple Rift-portal descent; pentagram summon-arena; necromancer caster; witch-hunter; castle hub; skeleton bestiary), and it carries raw material for all four register-2 axes **plus** real weapon geometry for the weapon-as-identity sockets. This note frames it + routes the build/score increment, with one load-bearing caveat that protects the work.

## 1. What landed

- **8 FBX categories** — `Characters, Weapons, Buildings, Environment, Props, FX, Vehicles, Misc` — plus `Emissive` + `FX` texture sets. Raw material for **all four** register-2 axes (geometry, material, lighting, VFX) in one pack.
- **Weapons FBX** is the asset-layer home of weapon-as-identity: the Synty `Attachment*` sockets now have dark-fantasy weapon geometry to bind (see `canonical/story/weapon-as-identity-surface-recognition-2026-06-14.md` § 5 asset-bridge).
- **Reference frames**: `maps/` (7 — scene-composition ideas) + `theme/` (17 — mood/lighting/character vignettes).

## 2. The design read (gandalf looked at 6 frames + the FBX tree)

**Register fit — the frames read register-2.** Every shot is the fixed elevated 2.5D camera we locked, emissive glow-pools against near-black, body-anchored VFX. Same lift recipe galadriel measured at 4.50/5 (lighting + VFX carry it; geometry is the small lever).

**Thematic fit — uncanny, frame by frame:**
| Frame | Reads as | Our surface it serves |
|---|---|---|
| `maps/…8.42.08` — purple portal + skeleton horde + ravine descent | the literal descent-through-the-portal | **seasonal-descent + Rift/reincarnation motif** |
| `maps/…8.38.06` — red ritual cathedral + glowing pentagram | a ritual boss-arena | **trial-boss gallery + summon theme (L2)** |
| `theme/…8.37.35` — hooded necromancer + conjured orb | caster archetype + NPC vignette | **caster roster + spirit-guide vignette** |
| `theme/…8.41.37` — wide-brim witch-hunter | physical/ranged hunter archetype | **hunter roster (weapon-as-identity)** |
| `theme/…8.34.25` — fog-wreathed castle vista | establishing hero-frame | **Earth-meta-layer hub / season-select** |
| `maps/…8.36.17` — green crypt + skeletons | exploration + undead | **bestiary content (Track C4)** |

**What it unlocks:** A-holds was proven on a POLYGON **graybox** + composed knight (minimal proof). This pack moves the claim to **real curated dark-fantasy content** — and hands us trial-boss arena + seasonal-descent + Earth-hub surfaces in one drop. This is Track C (visual register) made tangible; it is also the curated-world half of "curated world, generative self" (the curated environment + roster the Meshy generative-self forms will later stand inside).

## 3. THE CAVEAT (load-bearing — protects the build/score from a known trap)

**These are Synty's own MARKETING renders — their pipeline, not our Godot-on-our-hardware.** They are the aspirational **target/calibration anchor**, NOT the pass bar. Two consequences both seams must hold:

1. **The rubric is the gate; the references calibrate, they do not grade.** galadriel scores our built scene against the register-2 rubric (composite ≥3.6; **lighting ≥4 AND VFX ≥4 mandatory**). She does NOT score "does our scene match this PNG." If we conflate them we either chase an unattainable marketing post and burn budget, or feel falsely short when our rubric-*passing* scene doesn't match Synty's post-processing. The A-holds discipline was exactly this: we measured OUR build, not a marketing render — keep that line.
2. **Score lifecycle-sampled, not still-vs-still.** Per galadriel's F1 finding, stills under-represent VFX (the highest-leverage axis). A Synty marketing still is a *composition/mood* reference, not a *VFX-presence* reference; comparing our lifecycle capture to their frozen frame is apples-to-oranges on VFX. Sample our scene across its lifecycle as she did for the lift slice.

**drax corollary:** build to the rubric + the proven lift recipe, not to pixel-matching the marketing post. The reference is for composition/mood/asset-selection, not a fidelity target to chase.

## 4. Routing

- **drax (build):** compose a Godot scene from the pack against the `maps` references, using the validated lift recipe (`scenes/lift_render.tscn` lighting/VFX/material rig is the register-2 baseline recipe per the A-holds ruling). Use `theme` frames for mood/lighting calibration. Build the nominated scene first (§ 5).
- **galadriel (score):** lifecycle-score drax's built scene against the register-2 rubric, with the reference frames as the calibration anchor (§ 3). Reuse the standing rubric harness (`register-metrics.mjs` / `lifecycle-score.mjs`). Produce a scorecard as for the lift slice.
- **KR (sequence):** sequence drax-build → galadriel-score as the **"re-validate A-holds on real curated content"** increment. This is the named next register-adjacent milestone from the A-holds routing (Track C). Not blocking anything in flight; fires when Matt greenlights the increment.

## 5. Build sequence (gandalf nomination)

- **Build #1 — Map 2, the ritual cathedral interior (`maps/…8.38.06`).** Highest leverage, lowest risk: it's **enclosed** (the proven dark-interior lift recipe transfers directly — same lighting problem the lift slice solved), it doubles as a **trial-boss arena** (load-bearing structural surface), and the pentagram + braziers supply natural **body-anchored VFX** (the register's highest-leverage axis) without needing a bespoke hero-skill bloom. This is the cleanest first proof that the lift holds on real curated content.
- **Build #2 — Map 3, the portal/descent exterior (`maps/…8.42.08`).** The ambitious second proof: prove the recipe scales to **exterior + fog + enemy horde + verticality**, and that the seasonal-descent/Rift composition reads. Only attempt once the interior recipe lands — exterior lighting + horde density is a harder register problem.

## 6. Canonical trigger (what makes this a canon update vs. just an increment)

This note is a routing/framing artifact, **not** a canonical doc. The canonical moment is downstream: **if galadriel scores drax's built scene at register-2 on real curated content**, that extends the A-holds ruling from "graybox + composed knight" to "shipping environment + roster" — and THAT is the canonical update (an A-holds extension + a style-register note). Recognition discipline: the build/score is the empirical gate; the canon update fires on the score, not on the asset drop.

---

**Signed:** gandalf, 2026-06-15
**For:** routing the POLYGON Dark Fantasy drop — register-2 + on-theme to an uncanny degree (descent-portal, summon-arena, caster/hunter rosters, castle hub, skeleton bestiary, weapon geometry for the identity sockets); drax builds (Map-2 ritual cathedral first, the lowest-risk highest-leverage proof; Map-3 descent second), galadriel lifecycle-scores against the rubric with the frames as calibration anchor NOT pass bar (they are Synty marketing renders, not our build), KR sequences it as the re-validate-A-holds-on-real-content increment; the canon update fires on the score, not the drop.
