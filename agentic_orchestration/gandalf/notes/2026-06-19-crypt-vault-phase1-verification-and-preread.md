# Phase 1 verification + gandalf pre-read — crypt-vault rebuild (camera-committed)

**Status:** drax Phase 1 (structure + architecture) complete + gandalf-verified. Surfaced to Matt for the structural-composition checkpoint. Matt's verdict pending → pairs with this pre-read as calibration data.
**Author:** gandalf, Pattern B dialogue with Matt.
**Parents:** `2026-06-19-crypt-vault-rebuild-brief-camera-committed.md` (the brief) · drax Phase-1 task report.

---

## What I verified DIRECTLY (trust-but-verify)
- **Render ×2 frames** (00_committed, 03_follow_forward) — looked myself; composition holds across framings (NOT cherry-picked).
- **Strengthened crit-4 gate code** (`check_crypt_vault_gate1.gd`) — real ORIENT/GROUND/LAND/SUPPORT logic + a distinct `columns` bucket; not a rubber stamp.
- **project.godot** — `sidekick_creator` 1 ref + `godot_mcp` 3 refs INTACT (not clobbered; single-occupancy held).
- **No owner-recursion regression** — baked scene 620 `[node]`, **0 MeshCollider, 0 CollisionShape3D** (the bug yields 601).
- **Trusting (with evidence):** drax's Gate-1 numbers + the negative-control proof (break stair → crit-4 fails 3 ways, exit 1 → revert → passes, exit 0).

## Verdict: PHASE 1 STRUCTURAL PASS (my read; Matt's eye is the checkpoint)
The composition reads as a coherent, contained 2.5D ARPG cathedral-crypt. The prior failures (floating stairs, overlapping crypts, square-brick supports, reasonless walls) are GONE.

## Confirmed good — load-bearing decisions realized
- **Camera commit realized** — proper SE-looking-NW diagonal; height gradient (near LOW → gallery MID → tower TALL) reads.
- **N gallery + arcade on real 6 m columns** — fixes square-bricks (L) + reasonless-wall (F4/H).
- **W/NW tower climbs past frame; rosette clerestory** = the towering backdrop (Matt's requirement).
- **Stairs grounded + attached + climb-north + open-landing** — fixes A/B/C, the escape Matt's eye caught.
- **Gate-1 all-pass with crit-4 that now CATCHES the escape** (negative-control proven).
- **Annulus depth preserved** — floor inboard of both far walls ⟹ Phase-2 layering (foreground colonnade + niches) has room. (The thing I committed to check: PASS.)

## For Matt's eye — judgment-calls cheap to nudge on the BARE skeleton (before dressing)
- **(a) Cold/warm split:** N gallery + near-E read cold-blue; W tower warm. Intentional drama, or warm the N gallery for a unified cathedral? (Gate 2 quantifies warm-dominance post-dressing; flagged now because it reads stark.)
- **(b) NW corner junction:** the low blue gallery wall meets the tall warm tower a bit abruptly. Phase-2 layering + banner may soften; eye it.
- **(c) Stair placement:** grounded + correct but tucked in the E/left corner — integrated enough, or more central to the gallery?
- **(d) Camera fine-tune:** drax CAM_DIST=47 / pitch=35; tower climbs past the top edge; clip-more-aggressively is the one-number lever, cheapest now.

## Phase-2 WILL fix (not concerns)
Empty floor → annulus soft-boundary objects (F) + carpet (J). Bare uniform walls → layered niches + skulls + moss/vines + small gargoyles + banner. The emptiness is EXPECTED at a structural checkpoint — it shows why F+J matter (right now the floor reads as an empty plaza).

## Gate to Phase 2
Matt's eye on the composition. Reads → fire Phase 2 (layered far-wall + dressing + any camera/lighting nudge Matt calls). Wants a structural/camera nudge → do it cheap on the skeleton first.

## Matt's verdict (pending — calibration pairing)
[capture verbatim when it lands]
