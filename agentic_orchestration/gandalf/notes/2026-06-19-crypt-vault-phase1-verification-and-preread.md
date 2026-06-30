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

## Matt's verdict (captured — calibration pairing)
**Verdict: STRUCTURE-PASS-WITH-LAYOUT-REVISION.** Camera correct as committed; revise wall ROLES + door placement before any Phase-2 dressing.

- **Camera — confirmed correct (no bug).** Matt's "camera SW / East wall tall" read was the LEFT-HANDED-COMPASS MIRROR: this scene labels +Z=North while keeping +X=East / +Y=up, so (East,North,Up) is left-handed — a mirror of a normal north-up map, which flips map-intuition's L/R. The wall on screen-right is genuinely WEST; the camera is genuinely SE (CAM_AZ_DEG=-45, eye SE looking NW). Verified against the generator math, not the picture. SE is also the ONLY diagonal that keeps BOTH far walls in front of the camera (the other three throw the tower or the gallery behind). Camera unchanged.
- **Layout revision (Matt verbatim):** *"What I would like to see is the grand wall moved to the left (same side as the second level). Then swap the two doors one wall to the right, so that the character crosses from bottom-left to upper right."*
- **Interpretation (locked by his explicit end-state — the crossing direction is the spec):**
  - GRAND towering treatment moves WEST → NORTH, merging with the second-level gallery already on North → unified grand hero wall on the screen-LEFT (upper-left). [grand "to the left, same side as the 2nd level"]
  - WEST demotes to a MID-height far wall (upper-right), carries the EXIT. (height = soft/tunable lever)
  - Doors shift one wall CLOCKWISE in screen-space: exit NORTH→WEST (upper-left→upper-right); entrance SOUTH→EAST (lower-right→lower-left). [="one wall to the right"]
  - Net flow: entrance EAST (bottom-left, near) → exit WEST (upper-right, far) = bottom-left→upper-right. ✓ exactly Matt's stated crossing. The end-state disambiguates "one wall to the right" = clockwise (the CCW reading would put entrance on a far wall / flow upper-right→lower-left — rejected).
- **Calibration triple:** `(composition / eye-flow, the grand backdrop + door diagonal, "consolidate grand + gallery on ONE side (left); route the player's crossing along the screen diagonal bottom-left→upper-right so the eye-path and the traverse-path agree")`. Player consequence: arrival reveals the grand vaulted hero wall on the left, then the traverse pulls the eye diagonally toward the far exit — eye and feet move together (D2/PoE "enter into a reveal, then traverse toward the next gate").
- **Why this GATES Phase 2:** the layered far-wall marquee (archway niches + skulls + foreground colonnade + banner + moss/gargoyles) dresses the FAR walls. Dressing them before the grand-wall role moved W→N would put the single most expensive pass in the node on the WRONG wall. Discipline: re-jig structure → quick eye-check on the bare re-jigged skeleton → THEN dress. (recognition → validate → commit.)
- **Dispatched:** drax structural re-jig (wall roles W↔N grand; doors S→E entrance / N→W exit; stair relocate clear of E entrance, still climb +Z; carpet E→W; warm the North hero wall; Gate-1 re-run w/ entrance=E/exit=W sockets + crit-4 stair + spawn-parity; player-cam re-render). Phase-2 dressing explicitly withheld.
