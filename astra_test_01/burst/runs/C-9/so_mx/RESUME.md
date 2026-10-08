# Lane SO: resume note (R-C9-152 sorceress hood fix), paused 2026-10-03 for barrow_v2; resumed R-C9-224, PAUSED AGAIN 2026-10-08

## R-C9-233 (2026-10-08): the sorceress's FACE under the hood -- STEPS 0-2 DONE, stills with the conductor for Matt. NO deploy, NO loadout commit until Matt approves

Brief (ledger R-C9-233): diagnose (isolation grid at the play camera), fix, live-vs-fix stills.
- Tools: `scripts/r233_01_class_tex.py` (UV class texture: face / front hair / other hair -> `work/r233/class.png`),
  `scripts/r233_02_head_pitch.py` (head/neck pitch per clip, glTF FK -> `work/r233/head_pitch.json`),
  `barrow_full/godot/tools/probe_face_r233.gd` (the grid IN the painted Barrow, web renderer; one frozen pose per clip x
  heading; variants live / nofronthair / nohood / headzero / fill / noink (= the web pen off) / fixA..G (an IMPORTED body,
  and optionally hood, swapped on); passes beauty z1+z3, pen-off, ID, face footprint), `scripts/r233_03_measure.py`
  (coverage %, pen %, face luma, sheets), `scripts/r233_04_build.py` (the fix body), `scripts/r233_05_lining.py` (hood
  lining), `scripts/r233_06_stills.py` (live vs fix sheets). Every Godot run: heavy lock + `scripts/r152_06_godot_guard.py`
  (timeout, SCRIPT ERROR abort, log cap).
- DIAGNOSIS (look/r233_final, final_measure.json; means over S/SE/SW/E/W): live idle -- face visible 39% of its footprint,
  front hair over it 21%, hood brim 19%, pen 11%, visible-face luma 54/255 (footprint 47). Hiding the front hair -> 55%
  visible; hiding the hood -> 51%; head+neck at rest -> 39% (NO help: the hood rides on the head); fill light -> luma 101
  (but it washes her whole figure); pen off -> footprint luma 54. Head pitch DOWN 8.9 deg idle / 13.2 walk / 4.8 Fire Ball
  at the shot (r233_02). ON THE WEB BUILD HER HULL INKS ARE HIDDEN (barrow_full.gd "one pen"): the lines on her face are
  the depth-only screen pen. Cause: dark painted face (albedo luma ~101, painted fringe streaks on the forehead) in the
  ramp's shadow band + front strands across it + the opening framed by dark hair. Runs are not bit-repeatable (pen lines
  vary run to run, ~3000 px): compare variants only within one run. look/r233_grid (grid0) is CONTAMINATED -- superseded.
- FIX G (proposed): body `export/ss233g/so-body_ss233.glb` (from work/ss138a_pre.glb): hood_braid now takes ALL her hair in
  while the hood is worn (braid as ss152b, exactly); the head's non-hair texels lifted (gamma 0.65 x1.18: luma 107 -> 177)
  and the forehead above 1.60 m repainted as her skin; hood `export/ss233d/hood.glb` = ss152b's + an inward LINING
  (inset 2.5 mm, one light hood-red texel). Idle: face visible 53%, front hair 0%, visible-face luma 100 (live 54),
  footprint 77 (live 47); walk 95/71; Fire Ball 96/74. Orb-tip trace identical to ss152b: releases 0.2667 / 1.80 s.
  NOTE: G takes ALL front hair in -- R-C9-233 asked "hair still frames the face"; E (outer cheek strands kept) measured
  the same but the kept strands crossed her face at our camera angle. A ruling item.
- Stills for Matt: `look/r233_final/R-C9-233_live_vs_fixG_z1.jpg` (play scale) and `_z3.jpg`; isolation sheets
  `look/r233_final/final_sheet_<clip>_z{1,3}.jpg`.
- Candidates imported for the probe only: `barrow_full/godot/models/variants/so_r233/` (r233a..g bodies, hood_r233d) --
  in no slot and no pack (VARIANTS in build_web_painted.sh is explicit). Matt deletes the folder when done (lanes do not).
- AFTER MATT APPROVES: copy ss233g body + ss233d hood into so_bm134 via make_slots (body file name + slot json), re-run
  texture_provenance, web rebuild (EOR2 pin as before), select_check + web_perf, ONE loadout commit; conductor pushes.

## RESUMED (R-C9-231/232) AND STEPS 2-5 DONE, 2026-10-08 -- only Matt's look + the conductor's push remain

- Step 2: the paused build (`barrow_full/work/r224_build.log`, EOR2 pin b4de84e65, EXIT 0) re-staged unchanged into loadout (only barrow_v2_sw files had changed in the source since; staged pcks hash-equal to the build).
- Step 3: `select_check.js` 19/19, 0 page errors (`barrow_full/take/build/r224_select`); `web_perf_eor.sh` +0.000 ms/frame, worst 19.1 / 18.9 ms, 0 over 33 ms, 0 errors (`barrow_full/take/build/r224_eor_perf`).
- Step 4: **loadout commit `68ab873`** (15 barrow-painted files + AGENT_STATE.md), NOT pushed -- the conductor pushes.
- Step 5: `join1_pack_v5/d2-fire-sorc-bm` rendered (guarded, EXIT 0, 0 SCRIPT ERROR): 64/64 cells, 744 frames, releases r=3 at 0.2667 s and r=9 at 1.8000 s; sockets worst 0.0575 m over 3720 samples (= v4); contact sheet `join1_pack_v5/d2-fire-sorc-bm_contact_sheet_1x.png`; lint 0 mismatches + 3 negative controls each exit 1. v5 supersedes v4.
- Hood stills at the play camera (shipped light, 4 headings, guarded): `barrow_full/take/build/r224_hood/r224_hood_barrow_play_camera.jpg` (+ per-heading beauty/mask/full PNGs). Crown and back read as closed red fabric at every heading.
- Step 6: milestone text handed back to the conductor (lanes do not write ledger.json).


## Second pause (conductor relay of Matt, "forget the sorceress for now"), after R-C9-224 resumed with OPTION B

**Option B is confirmed (R-C9-224); step 1 is done.** Done in the resume before the stop:
- **Step 2 built, EXIT 0, 0 FAIL fences.** Barrow web pinned to EOR2 `b4de84e65` (pinned eor_kc2_fx.gd 6fa210e1..., whirlwind_channel.gd 173e78e3...); every Godot run went through the new guard `scripts/r152_06_godot_guard.py` (per-run wall-clock timeout + kill on SCRIPT ERROR / Parse Error). Log `barrow_full/work/r224_build.log`. The build sits in `barrow_full/web_painted/build/web` (sorceress.pck 45,492,508 B; variant_so_bm134.pck 34,575,896 B). It staged into loadout and **I reverted loadout to HEAD** (`git checkout -- public/playtest/barrow-painted`), so loadout is clean apart from the two old untracked n25/n40 packs. Nothing committed in loadout, nothing pushed.
- **Step 5b (the lint) done:** `scripts/r152_07_lint_v5.sh` -> `join1_render/work/manifest_lint_d2-fire-sorc-bm_v5.txt`: the v5 manifest against `so-body_ss152.glb`, 19 clips, 0 mismatches, exit 0; negative controls neg_release / neg_prose / neg_spin each exit 1 (2 / 1 / 1 planted mismatches caught).
- `scripts/r152_05_join_v5.sh` now runs Godot through the guard (GG_TIMEOUT_S=2700) instead of a bare perl alarm.

**Not done (stopped before starting):** step 3 (select_check.js + web_perf_eor.sh), step 4 (the loadout commit), step 5's render (`zsh scripts/r152_05_join_v5.sh`; `join1_pack_v5/d2-fire-sorc-bm/` does not exist, so it is free to run) and its release-frame check (frame 3 = 0.2667 s, frame 9 = 1.80 s), the Barrow play-camera stills of the hood (planned: `barrow_full/godot/tools/probe_charlight.gd -- --as-web --c sorceress --armor bm134 --tag r224 --out barrow_full/take/build/r224_hood`, 4 headings, through the guard + heavy lock), step 6.

**On the next resume:** if EOR2 has not committed past `b4de84e65` and nothing under barrow_full/godot that the painted Barrow exports has changed, re-stage the existing build (`rsync -a --delete --exclude .gdignore barrow_full/web_painted/build/web/ <loadout>/public/playtest/barrow-painted/`) rather than rebuilding; otherwise rebuild with the step-2 command below plus `GODOT=<abs>/so_mx/scripts/r152_06_godot_guard.py`. Then steps 3-6.


Paused on the conductor's word ("100% focus on barrow_v2"). Resume only on Matt's word.

## Where things stand

**Live on Vercel: loadout `d069c4b`.** This is the arena kit `ss138a`. Its R-C9-140 `hood_hair` morph pulls the hair inside her body. R-C9-152 found that this leaves the top and back of the hood see-through.

**Cause, measured.** `scripts/r152_01_hood_holes.py` reads `work/r152_hood_loops.json`:
- The hood piece is an open shell: 67 boundary loops and 3,426 open edges.
- The largest openings are on the crown (1.28 m of open edge at y 1.58–1.69) and around the back of the neck.
- Its material is single-sided, and the Barrow's character shader culls back faces (`paint_stack.gd` CHAR_SHADER `cull_back`).
- The hair surface used to fill those openings. Once it was pulled in, they read as holes.

### Fix built and checked in stills; NOT deployed and NOT in a pack

The fix is in `export/ss152b/`, from `scripts/r152_02_hood_cap.py` and `r140_03_hood_morph.py --name hood_braid`:
- The hair stays exactly as it was. The face and front hair are untouched: every hair vertex with z > 0.035 m, 8,476 vertices.
- **Hood cap.** The hood piece gains a second primitive. It is a copy of the back and top hair surface above 1.30 m (20,159 vertices), pushed 4 mm out along its normal and skinned with the hair's own weights. Its texture comes from the hood's red outer fabric: each cap vertex takes the UV of the nearest red-fabric hood vertex.
- **Braid.** A new morph, `hood_braid`, tucks the braid (the 3,998 hair vertices below 1.30 m) inside her back while the hood is worn. The slot rule is `hood_braid: hood`.
- Taking the hood off with G removes the cap and releases the braid, so the hair comes back unchanged.

The rejected option A is `export/ss152a`: the cap also covered the braid. It read as a red tail down her back.

### Evidence

- **Sheets** (live vs A vs B vs hood off, 8 headings, idle / walk / Fire Ball, 3× and 1×): `look/R-C9-152_{idle,walk,cast_fireball_m}_{3x,1x}.jpg`.
- **Barrow camera:** `barrow_full/take/build/r152_barrow_heads_live_vs_fix.jpg`. That is the first cut, A, before the red-fabric UV pick; B has not been rendered in the Barrow.
- **Stills harness:** `gear_sets/sorceress_battlemage/film_rt/gear_stills.gd` now takes `GS_CULL_BACK=1`, so stills render culled the way the Barrow does.
- **Release times are unchanged.** The orb-tip trace on `ss152b` is identical to `ss138a`'s (`work/r152_release_tip_ss152b.json`): Fire Ball 0.2667 s, Meteor 1.80 s.

### Already pointed at the fix, uncommitted until this pause commit

- `barrow_full/tools/make_slots.py` reads `so_mx/export/ss152b` and `character_sorceress_ss152b.json`. It has been run: `godot/models/variants/so_bm134` holds `so-body_ss152.glb` and the capped `hood.glb`, and `data/slots/so_bm134*.json` carry `hood_braid: hood`.
- I moved the old `so-body_ss138*` files out of the variant folder into `barrow_full/work/superseded_r152/`.
- `texture_provenance.py` has a row for `so-body_ss152` (66/66 pass).
- **Select page:** the dark knight's card has a new "Smoke tint" row: Light / Medium (default) / Strong, mapping to `eorsmoke` = 1 / (empty) / 3. `select_check.js` has a matching case. This has not been run against a build.
- `build_web_painted.sh` has a new PIN mode: `PIN_SHA=<sha> PIN_PATHS="..."` writes another lane's files into the build mirror from that commit, not from its live working copy.

### Interrupted when the pause landed

- **A Barrow build pinned to EOR2 `e98bda6bf`** was mid-run. I let it finish (EXIT 0, every fence ok; log `barrow_full/work/r152_build.log`). It staged into loadout, and I then reverted loadout's `public/playtest/barrow-painted/` to HEAD (`git checkout --`, = the live `d069c4b`). So loadout is clean apart from the two old untracked n25/n40 packs, and **nothing is committed in loadout**. `barrow_full/web_painted/build/web` still holds that e98bda6bf build; it is NOT the one to ship (the conductor then asked for `b4de84e65`).
- **The JOIN-1 v5 render never started.** It was still waiting for the heavy lock when I stopped it. But `join1_pack_v5/d2-fire-sorc-bm/` was already created, empty. `scripts/r152_05_join_v5.sh` refuses to run while that path exists, so Matt needs to delete that empty directory first (lanes don't delete).

## Next, in order, on resume

1. Show Matt the R-C9-152 sheets and confirm option B, or the fallback of bringing the braid over the shoulder. If he wants the shoulder version, build it.
2. Rebuild the Barrow pinned to **EOR2 `b4de84e65`** (the latest relayed: sparks as a generated streak, reddish translucent smoke):

   ```
   PIN_SHA=b4de84e65 PIN_PATHS="scripts/eor_kc2_fx.gd scripts/whirlwind_channel.gd" bash barrow_full/tools/build_web_painted.sh
   ```

   At pause time the working tree already matched `b4de84e65` for those files. If EOR2 has committed something newer, ask the conductor which sha to use.
3. Re-run `select_check.js` (19 cases with the `eorsmoke` row) and `tools/web_perf_eor.sh`.
4. Make one loadout commit (`--only`, the barrow-painted paths and `AGENT_STATE.md`). Don't push; the conductor pushes.
5. Run the JOIN-1 v5 pack, `zsh so_mx/scripts/r152_05_join_v5.sh` (kit `join1_render/kits/d2-fire-sorc-bm_v5.json`, manifest `manifests/d2-fire-sorc-bm_v5_clips.json`). Then run the manifest lint plus its 3 negative controls, and confirm the releases at frame 3 = 0.2667 s and frame 9 = 1.80 s. The new root supersedes v4.
6. Add ledger milestones for R-C9-152 and hand back with the stills.

## Budgets

- Disk was 42 GiB at pause. HALT if it drops below 21 GiB.
- Lane allotment is 1.2 GiB. R-C9-152 has added about 70 MB of stills plus about 60 MB of GLBs in `export/ss152a` and `export/ss152b`.
