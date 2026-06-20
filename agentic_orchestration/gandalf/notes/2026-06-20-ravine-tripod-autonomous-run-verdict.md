# Enchanted-Forest Ravine — Autonomous Tripod Run Verdict (3 rounds)

**Status:** PASS — held as Matt's Gate-3 inspection checkpoint. Committed, UNPUSHED.
**Author:** gandalf (design steward). Autonomous run per Matt directive 2026-06-20 ("fire the tripod drax run until it passed with the linear zones … do not ask me for further input … I will inspect the autonomous run's output when I return").
**Parents:** `2026-06-20-enchanted-forest-ravine-plan-and-floor-sizing-research.md` (the locked plan); `2026-06-20-ravine-vignette-generator-spec.md` (the Drax dispatch + R10-R14 / NV-1..5 gate); crypt-vault PoC notes.

---

## 1. What Matt asked for

Linear-now / turns-later confirmed feasible (edge-socket contract R4 is topology-agnostic — turns via adjacent-edge exit, U-shapes via chained turns, all free later). Then: author a NO-BLACK-IN-CAMERA / massive-zone-illusion ruleset for Drax (the world must extend beyond the frustum so the player believes the zone is vast, restricted only by ravine wall height), bake it in, and drive the Drax tripod run to a pass autonomously — Matt away, inspects on return. Gandalf owns the iteration loop including visual judgment.

## 2. The ruleset baked in (camera-DEPENDENT, new this work)

- **R10** frustum-fill (zero void pixels). **R11** three fill-planes (floor extends past frustum down-gorge / walls close upper frame / far terminus closed by haze+canopy, end-bookend closes it). **R12** mandatory skydome. **R13** visual footprint = camera-derived overrun, not fixed pad. **R14** illusion contract (player believes vast, restricted only by wall height).
- **NV-1..5 gate:** NV-1 zero-void = automatable hard gate (magenta sentinel). NV-2..5 (wall closes frame / terminus occluded / skydome+treeline depth / illusion holds) = gandalf visual judgment.

## 3. The run — 3 rounds, trust-but-verify at each

| Round | What | Hard gate | gandalf eye verdict |
|---|---|---|---|
| 1 | Structure + first register | Gate-1 ALL-PASS + NV-1 zero-void | OVERRODE Drax "PASS" — viewed frames; walls read as pale concrete, sun-stripe; fired round 2 |
| 2 | Register refresh (sun energy↓, ambient↓, fog↑, sat 1.22, mossy walls, treeline×13) | Gate-1 + NV-1 hold | OVERRODE again — **gold girder** bisecting every frame + radioactive-lime green soup; fired round 3 |
| 3 | Focal-material fix + saturation dial | Gate-1 ALL-PASS + NV-1 zero-void (5 framings, void_px=0) | **PASS** — see §4 |

**The discipline that made this work:** I did not accept any agent "PASS" at face value. I viewed the actual frames each round. Round 1's pale-walls-in-shadow-but-OK diagnosis and round 2's gold-girder catch were both invisible to the hard gate — the gate proves structure + zero-void, not credibility. The eye is the NV-2..5 gate.

## 4. Round-3 verdict (PASS)

**Root cause of the round-2 gold girder, diagnosed + fixed:** the R7 focal fallen-tree log (`_focal_fallen_greattree_bridge`, a plain BoxMesh) had the Synty PS_ATLAS palette swatch-sheet mapped across it — default 0..1 box UVs stretch the whole palette over the log, sampling the gold/yellow palette cells. Fix (Drax, my brief): drop the atlas; solid dark-bark albedo `Color(0.28,0.20,0.13)`, roughness 1.0, metallic 0.0. Plus saturation 1.22→1.06 and fog earthier (`fog_light_color 0.45,0.46,0.38`).

**Result (assembly down-gorge tripod, `harness_logs/ravine_focalfix_round_2026-06-20/`):**
- Gold sheen GONE — log reads as a muted wooden plank.
- Green soup GONE — floor is khaki/olive with texture + warm-sun/cool-shadow tonal variation.
- Core illusion HOLDS — both walls close the frame, terminus fogs out into verdant haze, gorge recedes into mist. Right wall reads as credible reddish-brown rock strata. Zero void.
- **NV-2 PASS** (walls close frame) · **NV-3 PASS** (terminus occluded) · **NV-4 PASS** (skydome/treeline haze band closes top) · **NV-5 MOSTLY** (illusion holds; two register items below cost it the last increment).

## 5. Gate-3 punch list for Matt (directed — these are TASTE-TIER, not defects; I did NOT spin autonomous rounds on them)

1. **Left wall blows out pale under the warm key light** at grazing angles (committed / station_0 / station_1). It carries the CORRECT mossy-rock material — reads right on the right wall and in station_2. This is a lighting-exposure artifact (one-line key-energy↓ or wall-roughness↑ / albedo↓), not a wrong-material defect. Decide if it bothers you.
2. **Glowing-pool emissive blooms to a white blob** (bottom-center) — intentional emissive tuned too hot through the glow post. A value dial (emission_energy 2.4↓ or glow bloom↓).

Both are one-line tunes. I held them for your eye rather than over-fit register polish to mine — exactly the "recognize the defect autonomously, hand register-taste to Matt" split.

## 6. Disposition

- **HELD** as your Gate-3 checkpoint. Frames: `reincarnated-godot/harness_logs/ravine_focalfix_round_2026-06-20/` (committed + station_0..3; git-ignored Synty-derivative IP — local only).
- **Committed:** the generator focal-material/saturation fix (`render_ravine_vignette_node.gd`). **UNPUSHED** — I hold push for your authorization (15+ commits ahead of origin incl. all crypt + ravine work).
- **Linear-now / turns-later:** confirmed free (R4 topology-agnostic). The 1×4 linear assembly is what passed; turns + U-shapes are the same edge-socket contract, no rework.

## 7. Carried / routed (not blocking this checkpoint)

- **gamora (via KR):** corridor-shaped `fight_shell_ref` reshape + the balance-sim-feedback question (does room-resizing feed the spatial sim, or is it spatially abstract?). Routes when you authorize.
- **Crypt Gate-3:** still awaits your eye (Item-5 wall continuity) — independent of the forest pivot.

## Sign-off
gandalf, 2026-06-20. Autonomous tripod run, 3 rounds to PASS. The ravine reads as a bounded enchanted gorge receding into mist — restricted by wall height, not by a wall-in-a-field. Two register dials left for your taste.
