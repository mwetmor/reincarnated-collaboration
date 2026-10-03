# Lane SO: resume note (R-C9-152 sorceress hood fix), paused 2026-10-03 for barrow_v2

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

- **A Barrow build pinned to EOR2 `e98bda6bf`** was mid-run. I let it finish (log `barrow_full/work/r152_build.log`). It staged into `reincarnated-loadout/public/playtest/barrow-painted/`, so the loadout working tree is dirty, but **nothing is committed in loadout**. That staged state is NOT the one to ship: the conductor then asked for `b4de84e65`.
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
