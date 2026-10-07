# Finding — 2026-10-07 — BV2F Phase 1′ (art-first blockout) Gate-2

**Reviewer:** jack-ryan (DEV-MODE)
**Severity:** WARN (verdict **PASS-WITH-FOLDS**; no BLOCK)
**Target:** LV `96b884f49` + `550682c73`; PH `433a52bb1`, `7e131897c`, `51d955677`
**Developer:** drax (lane LV), galadriel (lane PH)
**Principles applied:** REVIEW_PROCESS #1 (math-before-code), #2 (smoke gate), #4 (decisions-log / charter as truth), #5 (severity matters)
**Governs:** charter `agentic_orchestration/gandalf/notes/2026-10-06-barrow-v2-fidelity-run-charter.md` § 15 + § 15.1 (Gate-1 `89e405a26`, R-C9-186); § 13 W-4 and § 14 W4 where not retired.

## Verdict

**PASS-WITH-FOLDS. M1′ may go to Matt once F-2 and F-3 are folded into the cover.** These are two one-line text edits, and no re-render is needed. F-1 must close before Phase 2′ opens. Every other item is INFO.

## What I found (descriptive)

**§ 15.1 W-3 DONE items**

| Item | Evidence | Status |
|---|---|---|
| (a) P6′ presence/placement/scale vs `layout_bv2art.json`, after a constructed RED | calibration.md § 21: 1.5 m-shift RED fails 5/10. The first run was RED on presence (crag #2 and log #3 below sea_z −6.0; slope stone #4 at the frame edge). This was reported, not adjusted, and treated as a HALT for an LV fix. LV fixed it in `550682c73`. § 23: presence/placement/scale PASS, slot cross-check 34/34. I re-hashed § 23's inputs on disk: ids_art `aeaecf49ce26`, layout `c30e0d449dfa`, placed_fit `bba80944e10d`. All match § 23 and `guide_manifest.json`. | PASS |
| (b) hero-coverage table, mechanical, from the ID render of the stills | `lv_hero_coverage.py`: 12 stills, MIN_PX 5000, 7/7 PASS. `ground_ice` is a separate ID from `ground_shore_ice`, so the "mere" counts really are the mere. | PASS (see F-4) |
| (c) measured footprint vs ~55–65 m | The paint window is 66.2 × 51.0 m (6656 × 4096 px at 100.6 / 80.3 px/m; I recomputed it from the `window` u/v ranges). Placed geometry spans 65.9 × 58.2 m; the v figure includes cliff faces below the window. **The window is the binding definition**, because it sets canvas count and spend. On u, 66.2 m sits at the "about" edge of 65; on v, 51.0 m is under 55. That is acceptable as "about". | PASS (see F-2) |
| (d) declared openings + char/ash class | `declared_openings.json` lists 5 openings: wreck_hull, barrow_door, hall_great_door, gable_breach, sea_cave_mouth. The class map carries `char` 1.09 % and `ash` 3.43 %, with 0 unassigned. | PASS (see F-6) |
| (e) this Gate-2 | — | — |

**Also checked**

- **Frame.** `layout_bv2art.json` `frame` is v1's own frame: same u_hat/v_hat and `world_from_uv`. `make_bv2art.py` maps sketch px to (u, v) directly. `bv2f_level.gd` `_S()` is the identity map (sim (x, z, y) → local), with sim = (u, −v). The 47° in the frame is v1's camera yaw only, and no R_y(47°) Level-frame rotation is inherited. **DEV-4 retirement honoured.**
- **Toolchain.** The guide and ID renders go only through `v1tools/godot_run.sh` (`lv_guide_run.sh` lines 13 and 17). `verify.sh` exit 0: *"21 files; Tier A byte-identical to v1 @ 0f8f73697; Tier B = v1 + allowlisted patches."*
- **v1 untouched.** `git diff d4c59061f HEAD -- barrow_full` shows 5 paths, all under `bv2f/`: art/level.json (new), v7c/level.json, bv2f_level.gd, export_fit.gd, m1_stills.gd. barrow_full's untracked set is identical to `pc/bf_status_before.txt`.
- **Kit and scale.** `kit_inventory.json` lists nothing missing. `placed_fit_bv2art.json` max anisotropy is 1.0001, and P6′ scale finds 88 instances, 0 over 1.10, 0 record mismatches.
- **Spend.** `fal_spend_BV2F.json` was last written by `70ed0b922` (Phase 1), at a running total of $1.20. No image files were added in this phase. **Phase 1′ spent 0 images and $0.**
- **Stale `guide_art/tiles/`.** 99 untracked PNGs left over from the first 9×11 stitch. The only code path naming `tiles` is `lv_guide_stitch.py:66`, which writes it for non-art variants. PH's harness reads `guide_art/*.png` by name. The manifest lists only `tiles_5x5/` (25/25 shas verified). **Nothing reads the stale tiles.** The full-size guide/ID/class PNGs and `tiles_5x5/` are untracked and pinned by manifest shas, the same convention as v7b and v7c.
- **M1′ packet.** The cover is one phone screen with 3 asks, each with one recommendation, and includes the hall-sides ask (R-C9-175). There are 12 play-camera stills, each beside its sketch A crop (3 sheets), plus a labelled map, the guide sheet and the `.command`. The `.command` resolves to `C-9/barrow_full/godot` with `BV2F_VARIANT=art`, and `scenes/bv2f_barrow_v2.tscn` exists.
- **DEV-16.** The art ID table has 29 IDs, under 256.

## Rationale and folds

- **F-1 (WARN; owed before Phase 2′ opens, does not gate M1′).** § 13 W-4 requires the positive control to be re-measured at each phase Gate-2, at the pin, and also at HEAD if `barrow_full` HEAD has moved. HEAD has moved since the last measurement (`d4c59061f`, R-C9-180) by five bv2f-only paths, and no Phase-1′ re-measure is on record. The drift risk is low: the paths are additive bv2f files, `verify.sh` is green, and the untracked set is unchanged. Even so, the rule is not "measure if likely to have drifted". **PT: re-measure T1–T3 at `f1aa715ac` and at current HEAD before the first Phase-2′ image. Any difference is a HALT to the conductor.** This does not gate M1′, because nothing at M1′ paints or takes. *(Discipline: control before reliance; § 13 W-4.)*
- **F-2 (WARN; fold before M1′).** The cover line *"About v1's size (66 x 51 m)"* is an unmeasured claim on a Matt-facing surface. v1's window is **53.4 × 41.4 m**: `frame_grid.v1.json` gives 5376 × 3328 px at 100.6 / 80.3 px/m, on a 4×4 grid of 16 canvases. bv2art is **1.24× v1 per axis and has 25 canvases** (5×5). **LV: replace the line with the measured comparison, e.g. "66 × 51 m (v1: 53 × 41 m); 25 canvases vs v1's 16".** Separately, a 5×5 grid means **DEV-1 is OPENED**, not closed: it is only closed if the grid is exactly 4×4 (§ 15.1 W-6). **Conductor: enter DEV-1 (5×5) in the § 7 register, with the P5-seam / P4-drift A/B named, before Phase 3′ relies on the full grid.** The Phase-2′ pilot (3×3) does not rely on it. *(Discipline: empirical inspection over assumption; § 7.)*
- **F-3 (fold before M1′).** § 14 W4 requires the P6′ result to be shown on the M1 cover, and § 15 does not retire that requirement. The cover was built before § 23 and does not carry it. **LV: add one line: "P6′ PASS: presence, placement, scale; after a constructed RED and one presence fix."**
- **F-4 (INFO; README disclosure, not an ask).** Hero coverage meets the letter of W-3(b), because the mere is one of the seven listed heroes. But the **wreck's and the barrow door's only qualifying neighbour is the mere** (a ground region). Only two stills pair built heroes: hall/gable (09–11) and ring/stair (07). The start still 01 shows the hall at 808 px, below the threshold. **LV: add a "neighbour(s)" column to the README hero table** so Matt sees which hero each pass leans on. Whether that reads well enough is Matt's art call.
- **F-5 (INFO; README disclosure).** The uniform kit rescale shrinks the "monumental" barrow door from 5.81 × 6.67 m at kit scale to **2.6 × 3.0 m** (×0.45). The hall's great door becomes about 2.6 × 2.7 m (×0.571). This is allowed: R-C9-154 is retired. Matt's stated Phase-4 direction, though, is spawns in real doorways. **State both door sizes in the README**, so he judges them on the walk knowing the numbers.
- **F-6 (INFO).** `declared_openings.json` assumes cover ask 2 is answered "closed sides". **If Matt picks the open-sided ruin, LV re-emits declared openings and the class map before Phase 2′.** P6a's INVENTED/DECLARED triage depends on that file.
- **F-7 (INFO).** PH § 22's P11 pilot window (3×3, 40 trials) was computed on the **pre-fix** render, and `results/p11_window_bv2art.json` records no input shas. **PH: re-run it on the § 23 inputs with shas recorded when W-4 closes.** Also on record: P6′ placement cannot detect a 1.5 m shift on large heroes (wreck, barrow, hall, gable and cliffs score 0.95–1.00 under the shift). Hero placement is actually guarded by the slot cross-check (0.02 m). No action needed.
- **F-8 (INFO).** **DEV-16:** 29 IDs, under 256. LV records whether the art level groups IDs. If it does not, DEV-16 closes as *not opened*. If it does, DEV-16 is owed before the first take (§ 15.1 W-6). The stale `guide_art/tiles/` is harmless (see above). Matt or KR may delete it; LV's `rm` was denied.

## Action

- [ ] LV (drax): F-2 cover line; F-3 P6′ line on the cover; F-4 neighbour column; F-5 door sizes in the README. Then M1′ goes to Matt.
- [ ] Conductor (gandalf): DEV-1 (5×5) into the § 7 register (F-2), before Phase 3′.
- [ ] PT: control re-measure at pin and HEAD (F-1), before the first Phase-2′ image.
- [ ] PH (galadriel): P11 window re-run with input shas (F-7), at W-4 close.
- [ ] LV: re-emit declared openings if ask 2 = open-sided (F-6); DEV-16 disposition (F-8).
- [ ] Matt: the art read at M1′ (the three cover asks). Nothing from this Gate-2 is escalated.

## References

- `astra_test_01/burst/runs/C-9/barrow_v2/fid/ph/calibration.md` §§ 21–23; `ph/results/p11_window_bv2art.json`
- `.../fid/lv/art/{layout_bv2art.json, kit_inventory.json, frame_grid.bv2art.json}`; `.../fid/lv/tools/{make_bv2art.py, lv_hero_coverage.py, lv_guide_run.sh, lv_guide_stitch.py}`
- `.../fid/lv/guide_art/{guide_manifest.json, declared_openings.json}`; `.../fid/lv/placed_fit_bv2art.json`
- `.../fid/lv/M1p/{M1p_README.md, M1p_cover.jpg, M1p_stills_A.jpg, M1p_map.jpg, hero_coverage.json, Walk barrow_v2 art.command}`
- `.../fid/v1tools/{verify.sh, frame_grid.v1.json, PIN_COMMIT}`; `.../fid/pc/bf_status_before.txt`; `.../barrow_full/godot/scripts/bv2f/bv2f_level.gd`
