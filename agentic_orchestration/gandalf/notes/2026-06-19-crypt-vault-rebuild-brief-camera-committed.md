# Crypt-Vault Clear-Room — Rebuild Brief (camera COMMITTED)

**Status:** ACTIVE — the single coherent rebuild gated on Matt's camera commit, which is now GIVEN.
**Author:** gandalf (design steward), 2026-06-19, Pattern B dialogue with Matt.
**Parents:** `2026-06-19-crypt-vault-gate3-verdict-1-calibration.md` (the A–K triples + stair Gate-1 escape) · `2026-06-19-crypt-vault-node-poc-brief.md` (PoC method) · `act_graph_node_schema_draft.json` (footprints/sockets/kit).
**Executes:** drax (presentation seam). **Re-judges:** Gate 1 (engine-truth) → Gate 2 (galadriel register, player-camera) → Gate 3 (Matt, player-camera ONLY).
**Discipline:** nothing scales/canonicalizes until this rebuild passes Matt's Gate 3. recognition → validate → commit.

---

## 0. THE CAMERA COMMIT (the frame everything below serves)

Matt committed, 2026-06-19. **This is very likely THE project ARPG camera — lock it project-wide once this node passes.**

- **Bearing:** camera on the **south / entrance side, looking diagonally toward the NW** (SE-looking-NW isometric — the Diablo II standard; matches the entrance-S / exit-N socket geometry). The E-vs-W skew is a free choice but is hereby LOCKED to this; do not re-litigate per-node.
- **Pitch:** **shallow oblique, ~35° default** (D2 / PoE end of the dial). NOT top-down. Chosen because Matt's towering detailed W/NW backdrop only reads at a shallow pitch (steep foreshortens + flattens detail + brings the tower-top back into frame). Tunable: one number, set in the generator, judged from the first player-camera shot.
- **Scripted, not hand-placed:** drax bakes the camera transform into `render_crypt_vault_node.gd` so it is reproducible and survives regenerate. Matt does NOT set it in the live editor (would be clobbered by the next bake).
- **Far hemisphere (ALWAYS in frame — gets the detail budget):** N wall + W wall + NW corner.
- **Near hemisphere (low / cull / fade — get out of the way):** S wall + E wall.

### Acceptance-unit change (carried from the verdict)
The **orbit is RETIRED as the acceptance unit.** Gate 1 (engine-truth, camera-independent) owns breakage; Gate 2/Gate 3 collapse to the **player's committed 2.5D camera**. Audit/orbit angles survive ONLY as internal debug, never the judged unit. Evidence: the orbit + Gate 1 both passed the broken stairs — only Matt's eye caught them.

---

## 1. Far-wall backdrop (N + W + NW) — the grandeur + the economy

### N wall — functional second level
- **Gallery (G):** extends across the MAJORITY of the N wall; stops a fair bit before the NW corner; ends in a **railing**.
- **Arcade (H) on real columns (L):** arches column-to-column BENEATH the gallery — self-justifying architecture (answers the old "walls with no reason" failure F4). Use **actual columns, NOT square bricks.**
- **Support reaches the deck (C):** columns/piers reach the FULL 6 m gallery deck (prior failure: reached halfway).
- **Carries:** exit door (ground course, punches through the N wall), gargoyle, stair-destination.

### W wall + NW corner — towering pure-architecture backdrop (NEW, Matt 2026-06-19)
- Climbs **above the top of the camera frame** — purposeful, quality architecture with **depth/breadth of detail across the assets.** This is the detail-budget SINK.
- **Never capped:** out-of-frame ⟹ no wall-top, no ceiling authored (false-front economy — D2/D4/PoE).
- **Height gradient (composition):** near walls LOW → N gallery MID → W/NW corner TOWERING. The diagonal rise that sells the 2.5D depth.

## 2. Stairs (fixes A / B / C) — serve the N-wall gallery
- **Ground the foot (A):** stair foot sits ON the annulus floor (prior: floating mid-air).
- **Orient correctly (A):** climb NORTHWARD (away from camera, into the backdrop) ⟹ the climbable face turns TOWARD the player/camera. (prior: facing wrong direction)
- **Open the landing (B):** open the balustrade where the stair tops out (prior: landed at a railing).
- **Backdrop honesty:** the mezzanine is grandeur (combatants never go up) — but it must read as truly climbable, not a cheat.

## 3. Mezzanine clip + dead-space (D)
- **Clip the second level cleanly at the wall** (prior: passed through, reappeared on the far side).
- **Remove the 3 tiles of dead space beyond that wall** (behind the backdrop, never seen — pure waste).

## 4. Near walls (S + E) + wall fade (M)
- **Low / open-front** so they never occlude the play space. Entrance door on the S wall (player enters bottom of screen).
- **Fade (M):** ONLY the near walls (S + E) fade, and ONLY when they would actually occlude the character. Far walls (N + W + NW) NEVER fade. Tighten the trigger distance + width (prior: triggered too soon + too wide ⟹ "the entire room feels transparent" — because there was no committed camera to define near-vs-far; the commit resolves it).

## 5. Annulus soft-boundary (F + K) — keep combatants in the 28×28
- **Numbers:** playable battle area **28×28 m (sacrosanct)**; outer walls at **43×43 m**; **7.5 m annulus band** on every side. Walls are NOT the battle extent.
- **F (generic):** scatter scene-appropriate LARGER objects across the annulus bands to keep player + enemies in the playable footprint (Matt re-derived the locked decoupling soft-boundary rule by eye).
- **K (premium, ONE side — the side without stairs/gallery, e.g. E or S band):** slightly raised + railing + a small step you "might try to climb" BUT a **fallen column blocks it**; raised coffins behind it. **No false affordance.** If on a NEAR band (S/E), keep it LOW so the camera looks OVER it.

## 6. Floor + life
- **Carpet (J):** runs roughly entrance(S) → exit(N), up the screen — wayfinding + telegraphs the clear-room's pass-through job (D4/PoE floor-run convention).
- **Moss / vines / dungeon plants (I):** across the walls, ESPECIALLY around the arches/arcade of the second level — the age pass (a crypt reads OLD, not new-built).

## 7. VFX (E)
- **Tighten brazier flame range** tightly atop each brazier (prior: flame shape changed with camera, spread too wide, read as detached).

## 8. Gates after rebuild
1. **Gate 1 (engine-truth)** — re-run all criteria. **Strengthen crit 4** beyond endpoint-proxies to catch the stair escape: (a) stair ORIENTATION (climbable-face direction via orthogonal index), (b) visual GROUNDING (mesh-on-floor vs float — Synty pivot), (c) clear LANDING (no railing blocking), (d) SUPPORT reaches the supported deck (columns → 6 m). [crit-4 code-strengthening canonical write is jack-ryan's; for THIS rebuild drax makes the stairs pass the stronger checks.]
2. **Gate 2 (register, galadriel)** — cathedral register held; judged from the PLAYER CAMERA, not orbit.
3. **Gate 3 (Matt)** — from the player's 2.5D camera ONLY. Orbit retired as acceptance unit.

## 9. Operational prerequisite (single-occupancy — bit us once)
drax needs **sole occupancy** of the `reincarnated-godot` Godot project for the headless rebuild. Matt closes the editor WITHOUT saving first (the prior drax headless run collided with the open editor and dropped the `[addons] sidekick_creator` block from project.godot). After the rebuild, verify project.godot integrity.

## 10. Deferred (gated on this rebuild passing Matt)
Project-wide camera-convention canonicalization; method/schema/katabasis canonicalization; Gate-1 crit-4 strengthening canonical write (jack-ryan); render-harness → player-camera-only canonical; Godot single-occupant operating discipline (knight-rider sequencing); collider-strip optimization (drax follow-on).
