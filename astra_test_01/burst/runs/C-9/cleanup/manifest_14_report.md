# Cleanup manifest 14: report

**Author:** drax, lane CL, Run C-9 Phase 2 (conductor gandalf, session aab928). **Written:** 2026-10-06, about 18:15 EDT. The checks were re-run at 18:11.
**Status:** PREPARED. Nothing was deleted. Matt runs the deletion himself.
**Manifest:** `runs/C-9/cleanup/manifest_scratch_prune_14.txt`. Each line reads `<size> KiB  <tier>:<tag>  <absolute path>`, and lines starting with `#` are tier headers. No path contains two spaces in a row. 0 paths contain a single space, but the command below handles spaces anyway.
**Disk at writing:** 23 GiB free (`df -h /System/Volumes/Data`).

## Totals

| Tier | Entries | Frees |
|---|---:|---:|
| A, lane-listed superseded scratch | 135 | **2.07 GiB** (2,165,308 KiB) |
| B, untracked godot `harness_logs/*` and `tmp/*` older than 3 days | 2,441 | **1.67 GiB** (1,749,676 KiB) |
| **Manifest total** | **2,576** | **3.73 GiB** |
| C, superseded JOIN-1 pack roots (NOT in the manifest; conductor decides) | 11 roots | 0.46 GiB if all were approved |
| D, old runs C-1/3/5/6/8 (audit only) | none | none |

Expected result: about 23 GiB free now, about 26.7 GiB after the run (sizes from `du -sk`).

Tier A by tag:

| Tag | Entries | MiB | Source of the "superseded/scratch" call |
|---|---:|---:|---|
| scratch-moviemaker-avi | 16 | 922.4 | Movie Maker `.avi` intermediates in the conductor scratchpad: `film/ film2/ f3..f9/` (EoR whirlwind red/original tests, Oct 2) and `bv2_walk.avi`. **Each folder keeps its x264 `.mp4`**, and `bv2_walk.avi` is encoded as `barrow_v2/greybox/barrow_v2_greybox_walk.mp4`. |
| scratch-c3d_ref | 1 | 589.8 | Named in the brief. |
| en_e3-intermediate-rig | 36 | 213.3 | `en_e3/RESUME.md`, "Cleanup candidates". "Older maw/crab/gazer/raptor/rimethorn rig versions" were resolved as every version below the latest: maw v8, crab v5, gazer v5, raptor v7 and rimethorn v7 are kept. The kept versions are the only ones the lane's `.sh/.py/.json` name (checked by grep). Tripo GLBs and preps of record are kept. |
| en_e2-superseded | 12 | 89.7 | `en_e2/RESUME.md` plus `cleanup/manifest_en_e2_p2_superseded_scratch.txt`. That list was never run, and all 12 entries still exist. |
| so_mx-r138r152-stills | 8 | 68.8 | Brief (r138/r152 probe and before/after still folders): `so_mx/look/r138_{probe,before,after}` and `r152_{live,live_cb,fix,fix_cb,fixb_cb}`. The composited `R-C9-138_*` and `R-C9-152_*` sheets stay. |
| bv2-2d-shelved | 3 | 55.7 | Brief (2D route shelved): `barrow_v2/paint/barrow_v2_guide.png` and `paint/test/T2a_hall_stitched.png`, `T2b_barrow_stitched.png`. The JSONs and compare/seam JPGs stay. |
| so_mx-rejected-optA | 1 | 53.0 | `so_mx/RESUME.md`: option A `export/ss152a` was rejected. **ss152b (option B) is untouched** and still waits for Matt. |
| bv2-2d-staged-canvas | 35 | 44.1 | Brief: `artifacts/CS9-guides/BVP-*` and `BVR-*` staged chunk canvases and sketch-A crops. |
| bvsw-old-guide-tiles | 2 | 35.3 | `barrow_v2/section_sw/guide_tiles` and `guide_tiles_v2` (superseded; `guide_tiles_v3` is current and stays). |
| en_e4-intermediate-rig | 6 | 32.1 | `en_e4/RESUME.md`: `coilseer_rig_v1..v3` and `gloamwing_rig_v1..v3`. The `.rig.json` files and Tripo GLBs stay. |
| barrow-r138r152-stills | 1 | 6.6 | `barrow_full/take/build/r152_barrow`. `r138_barrow` is EXCLUDED because the ledger cites it. |
| scratch-EN3_TMP | 3 | 3.1 | `en_e4/RESUME.md` (EN3_TMP render temp): conductor scratchpad `en3r_*`. |
| bv2-superseded-preview | 10 | 0.6 | Ledger `M-C9-BX-GREYBOX-V1`: `barrow_v2/greybox/preview_*.png` were superseded by the Godot renders. |
| empty-v5-root | 1 | 0.0 | The EMPTY `join1_pack_v5/d2-fire-sorc-bm/`. `so_mx/scripts/r152_05_join_v5.sh` refuses to run while it exists. |

## The command Matt runs

The manifest is parsed with Python, which takes the full path after the second double-space. It does **not** use `awk '{print $NF}'`, which mis-targeted 10 entries of manifest 13. Header lines (`#`) are skipped.

Dry run first. It lists what is there and changes nothing:

```
python3 -c "import sys;[sys.stdout.write(l.rstrip('\n').split('  ',2)[2]+'\0') for l in open(sys.argv[1]) if l.strip() and not l.startswith('#')]" ~/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/cleanup/manifest_scratch_prune_14.txt | xargs -0 ls -d | wc -l
```

That should print **2576**. Then delete:

```
python3 -c "import sys;[sys.stdout.write(l.rstrip('\n').split('  ',2)[2]+'\0') for l in open(sys.argv[1]) if l.strip() and not l.startswith('#')]" ~/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/cleanup/manifest_scratch_prune_14.txt | xargs -0 rm -rf --
```

To run only one tier, add a tier filter. For example, Tier A only: `... if l.strip() and not l.startswith('#') and l.split('  ',2)[1].startswith('A:')]`.

**Re-check at run time.** Two things can go stale between writing and running:
- the 2-hour and 3-day windows are as of 18:11 on 2026-10-06;
- every Tier A entry under `/private/tmp/claude-501/.../60f6998b…/scratchpad/` is in the **live conductor session's** scratchpad. If that session's temp folder is purged first, those paths simply no longer exist, and `rm -rf` on a missing path is a no-op.

## Checks applied to every entry

For each entry the check script confirmed:
- **Exists**, and is sized with `du -sk`.
- **Not git-tracked**: `git -C <repo> ls-files -- <path>` returns empty. A folder holding tracked files would have been split into its untracked files; no Tier A folder held any.
- **Not cited as evidence**: the script grepped for the absolute path, the `C-9`-relative path, `runs/C-9/<rel>`, `scratchpad/<name>`, and (for files with names of 12 or more characters) the bare filename. The texts searched were:
  - the C-9 `ledger.json`;
  - `2026-09-20-kc2-play-run-charter.md`;
  - `2026-09-29-join-1-run-charter.md`;
  - `runs/KC2-PLAY/ledger.json`, where present.
  Parent-dir hits were recorded as information only. They are not grounds for exclusion, because nearly every lane folder (`en_e3/builds`, etc.) is named in the ledger.
- **No open handles**: one `lsof -Fn -w` snapshot, with every entry prefix-matched against it.
- **Not modified in the last 2 hours**: the newest mtime anywhere inside the entry.
- **Tier B also**:
  - newest mtime older than 3 days;
  - not `tmp/kc2/`;
  - not `harness_logs/s2c_rows12_2026-08-25b`;
  - no tracked file inside;
  - **an extra check: the entry's name does not appear in any tracked file of reincarnated-godot or reincarnated-collaboration.** For example, `12_cathedral_capture.avi` is named by `scripts/run_cathedral.sh` and `AGENT_STATE.md`. 76 entries (433 MiB) were held back by this. The same name scan over reincarnated-engine was stopped after 90 CPU-minutes without finishing, so it was not applied. The engine had 0 hits for every C-run path in the Tier D scan.

## EXCLUDED

### Tier A candidates that failed a check (63)


In summary:
- **The BVSW set is held whole**: 56 files, 84 MiB. Lane BS staged it from 15:49 to 17:15 and finished at 17:22, so most of it is under 2 hours old. The rest is held with it so that the set is not split. Put it in manifest 15.
- `barrow_full/take/build/r138_barrow`: the ledger cites it.
- `barrow_v2/paint/barrow_v2_zonemap.png` and `_preview.jpg`: **git-tracked** (force-added despite `*.png` being ignored), and the zone map is ledger-cited.
- `paint/test/T1_hall_stitched.png` and `greybox/barrow_v2_walk_preview.mp4`: the ledger cites both by name.
- The two `section_sw_film_R-C9-158_*.avi` files (264 MiB): modified at 17:20–17:21, so lane BS's film may still be in use. Manifest 15 can take them.

| KiB | Path | Reason |
|---:|---|---|
| 154720 | `60f6998b/scratchpad/section_sw_film_R-C9-158_section_sw_coast_pan_v2.avi` | modified < 2 h ago (newest 2026-10-06 17:21) |
| 116308 | `60f6998b/scratchpad/section_sw_film_R-C9-158_section_sw_coast_pan.avi` | modified < 2 h ago (newest 2026-10-06 17:20) |
| 13892 | `C-9/barrow_v2/paint/test/T1_hall_stitched.png` | cited: C-9 ledger: "T1_hall_stitched.png" |
| 9600 | `C-9/barrow_full/take/build/r138_barrow` | cited: C-9 ledger: "barrow_full/take/build/r138_barrow" |
| 7396 | `C-9/barrow_v2/paint/barrow_v2_zonemap.png` | git-tracked; cited: C-9 ledger: "barrow_v2_zonemap.png" |
| 2704 | `C-9/artifacts/CS9-guides/BVSW-1_3_canvas.png` | modified < 2 h ago (newest 2026-10-06 16:32) |
| 2356 | `C-9/artifacts/CS9-guides/BVSW-2_4_canvas.png` | modified < 2 h ago (newest 2026-10-06 16:43) |
| 2280 | `C-9/artifacts/CS9-guides/BVSW-3_4_canvas.png` | modified < 2 h ago (newest 2026-10-06 16:46) |
| 2208 | `C-9/artifacts/CS9-guides/BVSW-2_3_canvas.png` | modified < 2 h ago (newest 2026-10-06 16:36) |
| 2156 | `C-9/artifacts/CS9-guides/BVSW-1_1_skA.png` | modified < 2 h ago (newest 2026-10-06 16:19) |
| 2104 | `C-9/artifacts/CS9-guides/BVSW-1_0_skA.png` | held with its set: other BVSW canvases were modified < 2 h ago (lane BS finished 17:22); list whole set in a later manifest |
| 2064 | `C-9/artifacts/CS9-guides/BVSW-1_2_skA.png` | modified < 2 h ago (newest 2026-10-06 16:26) |
| 2036 | `C-9/artifacts/CS9-guides/BVSW-0_3_canvas.png` | modified < 2 h ago (newest 2026-10-06 16:29) |
| 2004 | `C-9/artifacts/CS9-guides/BVSW-0_1_skA.png` | modified < 2 h ago (newest 2026-10-06 16:16) |
| 2000 | `C-9/artifacts/CS9-guides/BVSW-5_5_canvas.png` | modified < 2 h ago (newest 2026-10-06 17:15) |
| 1956 | `C-9/artifacts/CS9-guides/BVSW-2_1_skA.png` | modified < 2 h ago (newest 2026-10-06 16:22) |
| 1936 | `C-9/artifacts/CS9-guides/BVSW-0_0_skA.png` | held with its set: other BVSW canvases were modified < 2 h ago (lane BS finished 17:22); list whole set in a later manifest |
| 1904 | `C-9/artifacts/CS9-guides/BVSW-0_2_skA.png` | modified < 2 h ago (newest 2026-10-06 16:22) |
| 1880 | `C-9/artifacts/CS9-guides/BVSW-5_2_skA.png` | modified < 2 h ago (newest 2026-10-06 16:39) |
| 1840 | `C-9/artifacts/CS9-guides/BVSW-4_4_canvas.png` | modified < 2 h ago (newest 2026-10-06 16:52) |
| 1840 | `C-9/artifacts/CS9-guides/BVSW-4_5_canvas.png` | modified < 2 h ago (newest 2026-10-06 17:06) |
| 1756 | `C-9/artifacts/CS9-guides/BVSW-2_0_skA.png` | modified < 2 h ago (newest 2026-10-06 16:16) |
| 1752 | `C-9/artifacts/CS9-guides/BVSW-0_1_canvas.png` | modified < 2 h ago (newest 2026-10-06 16:16) |
| 1740 | `C-9/artifacts/CS9-guides/BVSW-1_2_canvas.png` | modified < 2 h ago (newest 2026-10-06 16:26) |
| 1732 | `C-9/artifacts/CS9-guides/BVSW-2_2_skA.png` | modified < 2 h ago (newest 2026-10-06 16:29) |
| 1708 | `C-9/artifacts/CS9-guides/BVSW-1_3_skA.png` | modified < 2 h ago (newest 2026-10-06 16:32) |
| 1700 | `C-9/artifacts/CS9-guides/BVSW-0_3_skA.png` | modified < 2 h ago (newest 2026-10-06 16:29) |
| 1672 | `C-9/artifacts/CS9-guides/BVSW-5_4_canvas.png` | modified < 2 h ago (newest 2026-10-06 17:04) |
| 1632 | `C-9/artifacts/CS9-guides/BVSW-3_2_skA.png` | modified < 2 h ago (newest 2026-10-06 16:32) |
| 1632 | `C-9/artifacts/CS9-guides/BVSW-4_3_skA.png` | modified < 2 h ago (newest 2026-10-06 16:43) |
| 1628 | `C-9/artifacts/CS9-guides/BVSW-2_5_skA.png` | modified < 2 h ago (newest 2026-10-06 16:52) |
| 1628 | `C-9/artifacts/CS9-guides/BVSW-3_1_skA.png` | modified < 2 h ago (newest 2026-10-06 16:26) |
| 1620 | `C-9/artifacts/CS9-guides/BVSW-2_4_skA.png` | modified < 2 h ago (newest 2026-10-06 16:43) |
| 1612 | `C-9/artifacts/CS9-guides/BVSW-1_4_skA.png` | modified < 2 h ago (newest 2026-10-06 16:39) |
| 1612 | `C-9/artifacts/CS9-guides/BVSW-2_3_skA.png` | modified < 2 h ago (newest 2026-10-06 16:36) |
| 1608 | `C-9/artifacts/CS9-guides/BVSW-4_4_skA.png` | modified < 2 h ago (newest 2026-10-06 16:52) |
| 1604 | `C-9/artifacts/CS9-guides/BVSW-3_3_skA.png` | modified < 2 h ago (newest 2026-10-06 16:39) |
| 1596 | `C-9/artifacts/CS9-guides/BVSW-3_4_skA.png` | modified < 2 h ago (newest 2026-10-06 16:46) |
| 1584 | `C-9/artifacts/CS9-guides/BVSW-3_5_skA.png` | modified < 2 h ago (newest 2026-10-06 17:04) |
| 1584 | `C-9/artifacts/CS9-guides/BVSW-5_3_skA.png` | modified < 2 h ago (newest 2026-10-06 16:46) |
| 1580 | `C-9/artifacts/CS9-guides/BVSW-5_4_skA.png` | modified < 2 h ago (newest 2026-10-06 17:04) |
| 1548 | `C-9/artifacts/CS9-guides/BVSW-0_2_canvas.png` | modified < 2 h ago (newest 2026-10-06 16:22) |
| 1548 | `C-9/artifacts/CS9-guides/BVSW-4_5_skA.png` | modified < 2 h ago (newest 2026-10-06 17:06) |
| 1532 | `C-9/artifacts/CS9-guides/BVSW-4_2_skA.png` | modified < 2 h ago (newest 2026-10-06 16:35) |
| 1496 | `C-9/artifacts/CS9-guides/BVSW-5_5_skA.png` | modified < 2 h ago (newest 2026-10-06 17:15) |
| 1324 | `C-9/artifacts/CS9-guides/BVSW-1_4_canvas.png` | modified < 2 h ago (newest 2026-10-06 16:39) |
| 1292 | `C-9/artifacts/CS9-guides/BVSW-3_5_canvas.png` | modified < 2 h ago (newest 2026-10-06 17:04) |
| 1164 | `C-9/artifacts/CS9-guides/BVSW-0_0_canvas.png` | held with its set: other BVSW canvases were modified < 2 h ago (lane BS finished 17:22); list whole set in a later manifest |
| 1052 | `C-9/artifacts/CS9-guides/BVSW-3_3_canvas.png` | modified < 2 h ago (newest 2026-10-06 16:39) |
| 964 | `C-9/artifacts/CS9-guides/BVSW-2_5_canvas.png` | modified < 2 h ago (newest 2026-10-06 16:52) |
| 912 | `C-9/artifacts/CS9-guides/BVSW-1_0_canvas.png` | held with its set: other BVSW canvases were modified < 2 h ago (lane BS finished 17:22); list whole set in a later manifest |
| 912 | `C-9/artifacts/CS9-guides/BVSW-1_1_canvas.png` | modified < 2 h ago (newest 2026-10-06 16:19) |
| 876 | `C-9/artifacts/CS9-guides/BVSW-2_1_canvas.png` | modified < 2 h ago (newest 2026-10-06 16:22) |
| 864 | `C-9/artifacts/CS9-guides/BVSW-2_2_canvas.png` | modified < 2 h ago (newest 2026-10-06 16:29) |
| 848 | `C-9/artifacts/CS9-guides/BVSW-5_3_canvas.png` | modified < 2 h ago (newest 2026-10-06 16:45) |
| 816 | `C-9/artifacts/CS9-guides/BVSW-3_2_canvas.png` | modified < 2 h ago (newest 2026-10-06 16:32) |
| 804 | `C-9/artifacts/CS9-guides/BVSW-4_3_canvas.png` | modified < 2 h ago (newest 2026-10-06 16:43) |
| 716 | `C-9/barrow_v2/greybox/barrow_v2_walk_preview.mp4` | cited: C-9 ledger: "barrow_v2_walk_preview.mp4" |
| 656 | `C-9/barrow_v2/paint/barrow_v2_zonemap_preview.jpg` | git-tracked |
| 620 | `C-9/artifacts/CS9-guides/BVSW-2_0_canvas.png` | modified < 2 h ago (newest 2026-10-06 16:16) |
| 476 | `C-9/artifacts/CS9-guides/BVSW-4_2_canvas.png` | modified < 2 h ago (newest 2026-10-06 16:35) |
| 464 | `C-9/artifacts/CS9-guides/BVSW-3_1_canvas.png` | modified < 2 h ago (newest 2026-10-06 16:26) |
| 440 | `C-9/artifacts/CS9-guides/BVSW-5_2_canvas.png` | modified < 2 h ago (newest 2026-10-06 16:39) |

### Tier B entries excluded at the entry level (58)

This covers dirs holding tracked files, `tmp/kc2`, the locked `s2c_rows12_2026-08-25b`, and anything touched within 3 days.

| KiB | Entry | Newest | Reason |
|---:|---|---|---|
| 1834852 | `harness_logs/s2c_rows12_2026-08-25` | 2026-08-25 19:52 | contains tracked files |
| 1832268 | `harness_logs/s2c_rows12_2026-08-25b` | 2026-08-25 12:52 | read-only, deliberately locked |
| 1274572 | `harness_logs/s2b_rows37_2026-08-24` | 2026-08-25 12:12 | contains tracked files |
| 1274400 | `harness_logs/s2b_rows37_2026-08-24b` | 2026-08-25 12:12 | contains tracked files |
| 597360 | `harness_logs/s2b_rows12_2026-08-24` | 2026-08-25 01:19 | contains tracked files |
| 523720 | `tmp/restage` | 2026-09-29 00:07 | contains tracked files |
| 479524 | `tmp/br2watch` | 2026-09-29 00:07 | contains tracked files |
| 317604 | `harness_logs/s2b_e1_2026-08-24` | 2026-08-25 03:50 | contains tracked files |
| 93364 | `tmp/hudfix` | 2026-09-29 00:07 | contains tracked files |
| 86444 | `tmp/vfxtruth1` | 2026-08-24 18:41 | contains tracked files |
| 77612 | `tmp/beamv3` | 2026-09-29 00:07 | contains tracked files |
| 75572 | `tmp/hudbuild` | 2026-08-01 23:31 | contains tracked files |
| 72704 | `harness_logs/quiltfix_2026-07-25` | 2026-07-28 20:28 | contains tracked files |
| 65232 | `tmp/beamslits` | 2026-09-29 00:07 | contains tracked files |
| 61080 | `tmp/kc2` | 2026-10-06 16:24 | contains tracked files; tmp/kc2 (KP-86 graded-run evidence); modified within 3 days (newest 10-06 16:24) |
| 57964 | `tmp/hudport` | 2026-09-29 00:07 | contains tracked files |
| 37716 | `harness_logs/wwcr_2026-08-25-lap2` | 2026-08-26 01:28 | contains tracked files |
| 36000 | `harness_logs/wwcr_2026-08-25-cp1supp-ab` | 2026-09-29 00:07 | contains tracked files |
| 30432 | `harness_logs/s2c_rows38_2026-08-25-v3v3` | 2026-08-25 19:23 | contains tracked files |
| 30204 | `tmp/arcclear3` | 2026-09-29 00:07 | contains tracked files |
| 30136 | `harness_logs/s2c_rows38_2026-08-25` | 2026-08-25 16:26 | contains tracked files |
| 14152 | `harness_logs/s2c_rows12_2026-08-25-v3v3` | 2026-08-25 19:16 | contains tracked files |
| 10352 | `harness_logs/s2a_2026-08-24-final` | 2026-08-25 00:36 | contains tracked files |
| 9916 | `tmp/bodyprobe` | 2026-08-01 09:42 | contains tracked files |
| 7356 | `tmp/wr1` | 2026-09-29 00:07 | contains tracked files |
| 6328 | `harness_logs/tcp_l2_2026-07-24` | 2026-07-28 20:28 | contains tracked files |
| 5152 | `harness_logs/s2b_receipts_2026-08-24b` | 2026-08-25 00:35 | contains tracked files |
| 4928 | `harness_logs/wwcr_2026-08-24` | 2026-08-24 19:18 | contains tracked files |
| 4856 | `harness_logs/wwcr_2026-08-25` | 2026-08-25 12:10 | contains tracked files |
| 4844 | `harness_logs/wwcr_2026-08-25-p2` | 2026-08-25 12:10 | contains tracked files |
| 3408 | `harness_logs/s2_review_2026-08-25` | 2026-08-25 17:22 | contains tracked files |
| 3108 | `tmp/l7race` | 2026-09-29 00:07 | contains tracked files |
| 1744 | `harness_logs/wwcr_2026-08-25-wwab-motion` | 2026-09-29 00:07 | contains tracked files |
| 1528 | `harness_logs/s2b_receipts_2026-08-24` | 2026-08-25 00:35 | contains tracked files |
| 1200 | `tmp/vmur` | 2026-07-30 16:06 | contains tracked files |
| 920 | `harness_logs/wwcr_2026-08-25-PROBE-noneutralise` | 2026-08-25 12:10 | contains tracked files |
| 204 | `tmp/arsenal2` | 2026-08-01 16:57 | contains tracked files |
| 32 | `harness_logs/s2b_c1_sweep_2026-08-25` | 2026-08-25 10:32 | contains tracked files |
| 20 | `harness_logs/s2b_rt2_ciede.json` | 2026-08-24 22:53 | tracked file |
| 12 | `harness_logs/14_arena_room_parametric.log` | 2026-06-15 13:31 | tracked file |
| 12 | `harness_logs/15_arena_bake_and_open_arena_fix.log` | 2026-06-15 15:31 | tracked file |
| 12 | `tmp/vmur_cast_i5.tscn` | 2026-07-29 02:26 | tracked file |
| 8 | `harness_logs/11_lift_capture.log` | 2026-06-14 23:33 | tracked file |
| 8 | `harness_logs/12_cathedral_capture.log` | 2026-06-15 09:29 | tracked file |
| 8 | `harness_logs/13_boss_arena_capture.log` | 2026-06-15 12:13 | tracked file |
| 8 | `harness_logs/14_spellfx_compare_AB.log` | 2026-06-17 23:00 | tracked file |
| 8 | `harness_logs/perf_density_render_spike.log` | 2026-07-07 10:03 | tracked file |
| 8 | `tmp/vmur_amb_i5.tscn` | 2026-07-29 02:43 | tracked file |
| 4 | `harness_logs/01_import_boot.log` | 2026-06-14 20:08 | tracked file |
| 4 | `harness_logs/02_compose_test.log` | 2026-06-14 20:10 | tracked file |
| 4 | `harness_logs/03_harness_checkonly.log` | 2026-06-14 20:08 | tracked file |
| 4 | `harness_logs/04_scene_load.log` | 2026-06-14 20:08 | tracked file |
| 4 | `harness_logs/05_retarget_proof.log` | 2026-06-14 21:12 | tracked file |
| 4 | `harness_logs/07_runtime_compose_db_installed.log` | 2026-06-14 21:36 | tracked file |
| 4 | `harness_logs/08_baketime_compose_db_installed.log` | 2026-06-14 21:36 | tracked file |
| 4 | `harness_logs/minspec_escape_density.log` | 2026-07-02 20:31 | tracked file |
| 4 | `harness_logs/wwcr_2026-08-25-region-audit` | 2026-08-25 03:17 | contains tracked files |
| 4 | `tmp/vmur_aura_i3.tscn` | 2026-07-29 02:36 | tracked file |

The 37 dirs that hold tracked files contain **6.49 GiB of untracked files**. The largest are:
- `harness_logs/s2c_rows12_2026-08-25`, 1.75 GiB (3 tracked);
- `s2b_rows37_2026-08-24` and `…24b`, 1.20 GiB each;
- `s2b_rows12_2026-08-24`, 0.56 GiB;
- `tmp/restage`, 0.46 GiB (51 tracked);
- `tmp/br2watch`, 0.46 GiB;
- `s2b_e1_2026-08-24`, 0.30 GiB.

These are Step-2 receipt folders, whose tracked receipts may name their own frames. They need a per-file audit with the Sim Session before any of it is listed, which makes them a **manifest 15 candidate**.

### Tier B entries excluded because tracked files name them (76, 433 MiB)

| KiB | Entry | Reason |
|---:|---|---|
| 65852 | `godot/harness_logs/12_cathedral_capture.avi` | named in tracked files (reincarnated-godot:3) |
| 47320 | `godot/harness_logs/13_boss_arena_capture.avi` | named in tracked files (reincarnated-godot:2) |
| 41020 | `godot/harness_logs/boss_v1summon_capture.avi` | named in tracked files (reincarnated-godot:6) |
| 34756 | `godot/harness_logs/spellfx_compare_B_flipbook2d.avi` | named in tracked files (reincarnated-godot:1) |
| 34636 | `godot/harness_logs/spellfx_compare_A_synty_particle.avi` | named in tracked files (reincarnated-godot:1) |
| 34584 | `godot/harness_logs/spellfx_v1_warhall.avi` | named in tracked files (reincarnated-godot:1) |
| 30864 | `godot/harness_logs/12_cathedral_capture.gif` | named in tracked files (reincarnated-godot:4) |
| 30832 | `godot/harness_logs/13_boss_arena_capture.gif` | named in tracked files (reincarnated-godot:3) |
| 26652 | `godot/harness_logs/11_lift_capture.avi` | named in tracked files (reincarnated-godot:3) |
| 22252 | `godot/harness_logs/descent_sanctum_audit_orbit.avi` | named in tracked files (reincarnated-godot:2) |
| 15960 | `godot/harness_logs/11_lift_capture.gif` | named in tracked files (reincarnated-godot:4) |
| 7864 | `godot/harness_logs/descent_sanctum_audit_stairsubject.png` | named in tracked files (reincarnated-godot:2) |
| 6528 | `godot/harness_logs/11_lift_capture_half.gif` | named in tracked files (reincarnated-godot:2) |
| 2352 | `godot/harness_logs/spellfx_combo_warhall.mp4` | named in tracked files (reincarnated-godot:4) |
| 2276 | `godot/harness_logs/spellfx_compare_A_synty_particle.mp4` | named in tracked files (reincarnated-godot:3) |
| 2232 | `godot/harness_logs/spellfx_compare_B_flipbook2d.mp4` | named in tracked files (reincarnated-godot:3) |
| 2220 | `godot/harness_logs/spellfx_v1_warhall.mp4` | named in tracked files (reincarnated-godot:4, reincarnated-collaboration:3) |
| 2116 | `godot/harness_logs/boss_v1summon_capture.mp4` | named in tracked files (reincarnated-godot:6) |
| 1208 | `godot/harness_logs/descent_iter5_zone1_05.png` | named in tracked files (reincarnated-collaboration:2) |
| 1204 | `godot/harness_logs/descent_iter5_zone2_06.png` | named in tracked files (reincarnated-collaboration:2) |
| 1204 | `godot/harness_logs/descent_iter6_zone2_06.png` | named in tracked files (reincarnated-collaboration:4) |
| 1196 | `godot/harness_logs/descent_iter6_zone1_05.png` | named in tracked files (reincarnated-collaboration:4) |
| 1184 | `godot/harness_logs/descent_iter5_zone2_erupt_78.png` | named in tracked files (reincarnated-collaboration:2) |
| 1184 | `godot/harness_logs/descent_iter5_zone2_erupt_82.png` | named in tracked files (reincarnated-collaboration:2) |
| 1184 | `godot/harness_logs/descent_iter5_zone2_erupt_84.png` | named in tracked files (reincarnated-collaboration:2) |
| 1164 | `godot/harness_logs/descent_iter5_zone4_08.png` | named in tracked files (reincarnated-collaboration:2) |
| 1160 | `godot/harness_logs/descent_iter6_zone4_08.png` | named in tracked files (reincarnated-collaboration:4) |
| 1140 | `godot/harness_logs/descent_iter4_zone5_09.png` | named in tracked files (reincarnated-collaboration:5) |
| 1140 | `godot/harness_logs/descent_iter5_zone5_09.png` | named in tracked files (reincarnated-collaboration:2) |
| 1124 | `godot/harness_logs/descent_iter5_zone0_04.png` | named in tracked files (reincarnated-collaboration:2) |
| 1124 | `godot/harness_logs/descent_iter6_zone5_09.png` | named in tracked files (reincarnated-collaboration:4) |
| 1120 | `godot/harness_logs/descent_iter6_zone0_04.png` | named in tracked files (reincarnated-collaboration:4) |
| 1000 | `godot/harness_logs/descent_iter2_zone0.png` | named in tracked files (reincarnated-godot:3) |
| 976 | `godot/harness_logs/descent_iter2fix_zone0.png` | named in tracked files (reincarnated-collaboration:3) |
| 968 | `godot/harness_logs/descent_iter2fix_zone2.png` | named in tracked files (reincarnated-collaboration:3) |
| 968 | `godot/harness_logs/descent_spellfx_warhall_seq_01.png` | named in tracked files (reincarnated-collaboration:2) |
| 916 | `godot/harness_logs/descent_iter7_establish_02.png` | named in tracked files (reincarnated-collaboration:5) |
| 884 | `godot/harness_logs/descent_iter7_establish_01.png` | named in tracked files (reincarnated-collaboration:5) |
| 880 | `godot/harness_logs/gal_descent_zone2_warhall_04.png` | named in tracked files (reincarnated-collaboration:9) |
| 876 | `godot/harness_logs/gal_descent_zone0_threshold_04.png` | named in tracked files (reincarnated-collaboration:9) |
| 860 | `godot/harness_logs/descent_iter7_establish_03.png` | named in tracked files (reincarnated-collaboration:5) |
| 836 | `godot/harness_logs/gal_descent_zone4_antechamber_04.png` | named in tracked files (reincarnated-collaboration:6) |
| 828 | `godot/harness_logs/gal_descent_zone5_sanctum_04.png` | named in tracked files (reincarnated-collaboration:6) |
| 760 | `godot/harness_logs/descent_iter5_establish_02.png` | named in tracked files (reincarnated-collaboration:2) |
| 760 | `godot/harness_logs/descent_iter5_establish_03.png` | named in tracked files (reincarnated-collaboration:2) |
| 748 | `godot/harness_logs/descent_iter6_establish_01.png` | named in tracked files (reincarnated-collaboration:4) |
| 748 | `godot/harness_logs/descent_iter6_establish_02.png` | named in tracked files (reincarnated-collaboration:4) |
| 748 | `godot/harness_logs/descent_iter6_establish_03.png` | named in tracked files (reincarnated-collaboration:4) |
| 700 | `godot/harness_logs/descent_iter5_zone3_07.png` | named in tracked files (reincarnated-collaboration:2) |
| 672 | `godot/harness_logs/descent_iter6_zone3_07.png` | named in tracked files (reincarnated-collaboration:4) |
| 608 | `godot/harness_logs/gal_descent_zone1_arcane_04.png` | named in tracked files (reincarnated-collaboration:6) |
| 520 | `godot/harness_logs/descent_iter2fix_establish_primary.png` | named in tracked files (reincarnated-collaboration:3) |
| 416 | `godot/harness_logs/gal_descent_establish_primary_04.png` | named in tracked files (reincarnated-collaboration:9) |
| 288 | `godot/harness_logs/gal_descent_zone3_oubliette_04.png` | named in tracked files (reincarnated-collaboration:6) |
| 52 | `godot/harness_logs/10_composed_knight_render.png` | named in tracked files (reincarnated-godot:2) |
| 48 | `godot/harness_logs/06_retarget_render.png` | named in tracked files (reincarnated-godot:2) |
| 48 | `godot/harness_logs/09_composed_base_render.png` | named in tracked files (reincarnated-godot:2) |
| 12 | `godot/tmp/vmur_cast_i1.tscn` | named in tracked files (reincarnated-godot:6) |
| 12 | `godot/tmp/vmur_cast_i2.tscn` | named in tracked files (reincarnated-godot:4) |
| 12 | `godot/tmp/vmur_cast_i3.tscn` | named in tracked files (reincarnated-godot:4) |
| 12 | `godot/tmp/vmur_cast_i4.tscn` | named in tracked files (reincarnated-godot:4) |
| 8 | `godot/tmp/kp227` | named in tracked files (reincarnated-godot:7, reincarnated-collaboration:3) |
| 8 | `godot/tmp/tcp_stride_dump.csv` | named in tracked files (reincarnated-godot:1) |
| 8 | `godot/tmp/vmur_amb_i3.tscn` | named in tracked files (reincarnated-godot:4) |
| 8 | `godot/tmp/vmur_amb_i4.tscn` | named in tracked files (reincarnated-godot:4) |
| 8 | `godot/tmp/vmur_amb_leakctl.tscn` | named in tracked files (reincarnated-godot:4) |
| 8 | `godot/tmp/vmur_amb_leakctl2.tscn` | named in tracked files (reincarnated-godot:4) |
| 8 | `godot/tmp/vmur_amb_leakctl3.tscn` | named in tracked files (reincarnated-godot:4) |
| 8 | `godot/tmp/vmur_amb_leakctl4.tscn` | named in tracked files (reincarnated-godot:4) |
| 4 | `godot/tmp/tcp_stride_measure.json` | named in tracked files (reincarnated-godot:1) |
| 4 | `godot/tmp/vmur_aura_i1.tscn` | named in tracked files (reincarnated-godot:5) |
| 4 | `godot/tmp/vmur_aura_i2.tscn` | named in tracked files (reincarnated-godot:4) |
| 4 | `godot/tmp/vmur_aura_i2_nopart.tscn` | named in tracked files (reincarnated-godot:4) |
| 4 | `godot/tmp/vmur_aura_i3_nopart.tscn` | named in tracked files (reincarnated-godot:4) |
| 4 | `godot/tmp/wallnum_boxuv.gd` | named in tracked files (reincarnated-collaboration:4) |
| 4 | `godot/tmp/wallnum_uvprobe.gd` | named in tracked files (reincarnated-godot:1, reincarnated-collaboration:6) |

## Session temp folders that are not in the manifest

**Not ours. Size only, for the Sim Session to judge:**

| Folder | Size | Note |
|---|---:|---|
| `/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/ac232ef8-034a-45e4-8e9f-65834cd599f9/` | 12.29 GiB (12,886,308 KiB) | Live (`scratchpad/kp298/` written 17:34). |
| `/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/7727ace9-b3f6-45c8-8739-f83328feeaa7/` | 4.22 GiB (4,430,064 KiB), of which `scratchpad/eng311/` is 3.72 GiB | **Also not ours.** It is a `--drax` session started 2026-10-06 11:15, doing KC2 runtime work (`g3_kp290`, `b5_s47_*`, written up to 17:16 today). It belongs to the Sim Session's side, so it is listed here and not in the manifest. |
| `…/b9b98544-c15b-4c51-a4ea-7815fdecad06/` | 0 | Empty. |
| `…/c9-shared/scratchpad/` | 0.3 MiB | BVSW drive logs; lane BS. |

**The live conductor scratchpad (`60f6998b…/scratchpad/`, 4.21 GiB) beyond the lane-listed Tier A items: 2.72 GiB that NO lane listed.** These are the conductor's own; gandalf decides. Largest:
- `web_eor2/` 1,378 MiB (EoR2 web build, Oct 3);
- `ov_raw3/` 148, `ov_raw2/` 135, `ov_raw/` 125 MiB (overlay raw frames, Oct 2);
- `frames1/`..`frames4/` about 43 MiB each;
- `take_dry/` 38 MiB;
- the frames left in `f3/`..`f9/`, `film/`, `film2/` after their `.avi` files are removed (for example `f4/` 28 MiB);
- nine about-26 MiB GLBs (`h1.glb`, `r138_idles.glb`, `t1.glb`, `t2.glb`, `b.glb`, `pA*.glb`);
- `fake_painted.png` 25, `cap0_plate.png` 22 and `cap0/` 22 MiB;
- `guide_v1.png` 18 MiB (today).

## Tier C: superseded JOIN-1 pack roots (NOT in the manifest)

Pack roots are declared immutable. **None of these roots has any git-tracked file**: their `matrix_index.json` and cells are all ignored PNG/JSON. So the pin in a newer kit, a sha256 of the old root's `matrix_index.json`, can only be re-verified while the old root exists. Deleting a pinned root makes that pin unverifiable; it does not break the runtime. KC2's `kc2_play/tools/stage_join1.py` (godot, lines 61–64) already maps every old id to its replacement. These are for the conductor to decide; I propose nothing either way.

| Root | Size | Superseded by | What pins it |
|---|---:|---|---|
| `join1_pack/gd-eor-warlord` | 63.6 MiB (857 files) | `gd-eor-warlord-eor3` (R-C9-141) | **Kit `join1_render/kits/gd-eor-warlord-eor3.json` `supersedes`**: `index_sha256 d44c3626c00a…`, plus body `wl_e1/export/final_k_eor2/wl_body.glb` (sha `492b9e99…`). The KC2 charter (KP-214, and "packs of record per C-9") names it, saying "the old root is a drop-in until P1(e)". `stage_join1.py` maps `gd-eor-warlord` to HERO. `wl_e1/scripts/e61_notch_stills.py` reads it. |
| `join1_pack/en-burrowworm` | 35.2 MiB (417) | `en-burrowworm_p` | **Kit `en-burrowworm_p.json` `supersedes`**: `index_sha256 08bdc4fc4d13…`. `en_e3/RESUME.md`; `en_e3/work/runtime_resample_en-burrowworm.json`. |
| `join1_pack/en-crawlerlarva` | 6.6 MiB (417) | `en-crawlerlarva_p` | **Kit `en-crawlerlarva_p.json` `supersedes`**: `index_sha256 567115366c21…`. `en_e3/RESUME.md`; `en_e3/work/runtime_resample_en-crawlerlarva.json`. |
| `join1_pack/en-magister` | 66.2 MiB (705) | `en-magister_p` | Kit `en-magister_p.json` `painted_texture.supersedes` (prose, no sha). Its source body `en_e2/export/final_k_v1` is kept by lane rule. `en_e2/work/runtime_resample_en-magister.json`; manifest `en-magister_p_clips.json`. |
| `join1_pack/en-warden` | 63.6 MiB (705) | `en-warden_p` | As above: `en-warden_p.json` (prose), source `final_h_v1`. |
| `join1_pack/en-witch` | 38.0 MiB (705) | `en-witch_p` | As above: `en-witch_p.json` (prose), source `final_j_v1`. |
| `join1_pack/en-mindtaker` | 25.1 MiB (705) | `en-mindtaker_p` | As above: `en-mindtaker_p.json` (prose), source `final_q_v1`. |
| `join1_pack_v3/d2-fire-sorc-bm` (and its contact sheet) | 34.7 MiB (745) | `join1_pack_v4/d2-fire-sorc-bm` (R-C9-138) | No sha pin. Kit `d2-fire-sorc-bm.json` targets it, and `d2-fire-sorc-bm_v4.json` names it. The KC2 charter names it twice: once as the pack of record, then as "SUPERSEDED, don't wire it" (corrects KP-250). |
| `join1_pack/d2-fire-sorc` | 37.8 MiB | `join1_pack_v3/d2-fire-sorc-bm` (and `_v2`) | **Kit `d2-fire-sorc_v2.json` `supersedes`**: `index_sha256 be8bb335b161…`. The KC2 charter says "superseding `join1_pack/d2-fire-sorc`". |
| `join1_pack_v2/d2-fire-sorc` | 37.9 MiB | `join1_pack_v3/d2-fire-sorc-bm` | No kit in `join1_render/kits/` names it, and no sha pin was found. |
| `join1_pack_draft/d2-ww-barb` | 40.4 MiB (whole `join1_pack_draft/` 49.0 MiB) | `join1_pack/d2-ww-barb-mx` | No kit names this path, and no sha pin was found. `join1_pack_draft/` also holds `d2-fire-sorc*` contact sheets, and kit `d2-fire-sorc_v2.json` names `join1_pack_draft/d2-fire-sorc`. |

**Not superseded, so not listed:** `join1_pack_v4/d2-fire-sorc-bm` (34.9 MiB) is the **current** sorceress pack of record until v5 renders. The only Tier C exception, the EMPTY `join1_pack_v5/d2-fire-sorc-bm/`, is in Tier A as instructed.

## Tier D: old run folders C-1, C-3, C-5, C-6, C-8 (audit only; no manifest entries)

How the counts were made:
- **Refs** = occurrences of `runs/C-N/<subfolder>` across the tracked files of all three repos. This is `git grep -o`, which counts occurrences; `git grep -c` would count matching lines.
- **Outside run** = refs from files outside that run's own folder.
- A second pass counted bare names (`C-3/xvideo`, `CS-pack-v9`, `stage-keeper`, …), because ledgers often cite artifact ids without a path.

| Run | Size | Tracked files | Path refs (collab / godot / engine) | Of which from inside the run itself |
|---|---:|---:|---:|---:|
| C-1 | 0.69 GiB | 522 | 3,095 / 0 / 0 (325 files) | 2,256 |
| C-3 | 6.89 GiB | 15,986 | 7,366 / 5 / 1 (1,010 files) | 5,363 |
| C-5 | 7.85 GiB | 342 | 30,751 / 0 / 2 (286 files) | 26,836 |
| C-6 | 2.39 GiB | 165 | 1,120 / 0 / 0 (235 files) | 757 |
| C-8 | 2.48 GiB | 231 | 1,297 / 10 / 0 (171 files) | 1,268 |

Largest subfolders, with tracked-file count and path refs (outside-run refs in brackets):

- **C-1:**
  - `xvideo` 398 MiB, 1 tracked, 0 path refs, but 59 bare `C-1/xvideo` refs;
  - `artifacts` 303 MiB, 435 tracked, 2,448 refs [549].
- **C-3:**
  - `artifacts` 3,842 MiB, 1,465 tracked, 1,686 refs [1,102];
  - `xvideo` 238 MiB, 0 tracked, 0 path refs, but 371 bare refs;
  - about 40 `cliffside*` Godot projects at about 145–165 MiB each. Many hold about 1,900 tracked files (v11–v18). v7, v9, v8b and v10 hold about 50, and v6 holds 18.
- **C-5:**
  - `t3` 3,540 MiB, 144 tracked, 14,115 refs;
  - `artifacts` 3,441 MiB, 129 tracked, 250 refs [222];
  - `cliffside_v39`..`v44`, 174 MiB each, 0 tracked, 0–5 path refs. The C-5 ledger names v39 and v42.
- **C-6:**
  - `cliffside_v40-necro` 893 MiB, 1 tracked, 4 refs;
  - `cliffside_v40-warlord-probe` 872 MiB, 1 tracked, 1 ref;
  - `artifacts` 161 MiB, 25 tracked, 390 refs;
  - `cliffside_v40-warlord8` and `8b`, 151 MiB each;
  - `xvideo` 107 MiB, 114 bare refs.
- **C-8:**
  - `web` 1,081 MiB, 9 tracked, 3 refs;
  - `cliffside_v40-warlord`..`warlord5`, 203–221 MiB each, 2–7 tracked, 0–8 refs (warlord5 has 3 from godot);
  - `xvideo` 208 MiB, 214 bare refs;
  - `cells` 101 MiB, 97 tracked.

**Is any big subfolder referenced by nothing tracked?** Strictly, **no**. Every subfolder over 100 MiB has at least one tracked reference (path or bare name) or holds tracked files. The weakest-referenced, which would be **candidates for a manifest 15 after the conductor's and Matt's review**:

| Candidate | Size | Tracked inside | References found |
|---|---:|---:|---|
| `C-8/web/stage-keeper`, `stage-warlord`, `stage-necro` | 250 + 241 + 203 MiB | 0 path refs at depth 3 | 1 bare-name ref each |
| `C-8/web/build-keeper`, `build-necro`, `build-necro2` | 95 + 93 + 93 MiB | – | 0 path refs; bare names ambiguous |
| `C-3/cliffside_v8` | 159 MiB | 0 | 0 path refs; 2 bare (`C-3/artifacts/T3q/receipt.json`, `C-3/t3/T3q/acceptance.json`) |
| `C-3/cliffside` and `C-3/cliffside_v4` | 146 + 142 MiB | 0 | 0 path refs; bare-name counts are not separable from `cliffside_v4x`/`cliffside_vN` |
| `C-5/cliffside_v39`, `C-5/cliffside_v42` | 174 MiB each | 0 | 0 path refs; named in the C-5 ledger rulings (pack v39, v42) |
| `C-5/artifacts/CS-pack-v20-r1` | 389 MiB | – | 0 path refs; 5 bare |
| `C-3/artifacts/CS-pack-v8 … v13`, `CS-pack-web` | about 86 MiB each, about 600 MiB together | – | 0 path refs; 4–8 bare (51 for `CS-pack-web`) |
| `C-6/cliffside_v40-warlord-probe` | 872 MiB | 1 | 1 path ref, 1 bare |

Depth-3 totals with zero path refs:
- `C-3/artifacts`: 244 of 489 subfolders, 2.58 GiB;
- `C-5/artifacts`: 83 of 121, 2.18 GiB;
- `C-8/web`: 12 of 12, 1.06 GiB;
- `C-1/artifacts`: 44 of 153, 107 MiB;
- `C-6/artifacts`: 9 of 92, 24 MiB.

Most of those artifact ids are cited by id in their run's ledger, so path-ref zero is **not** proof of no use.

## Disclosure: one stray file I wrote

During the scratchpad inventory, a mistyped relative redirect wrote a 6.9 KB listing to **`/private/tmp/tmp_unused`**, outside my scratchpad. It holds nothing but a `du` listing. I did not delete it (no-rm rule). It is not in the manifest because it fails the 2-hour check; Matt can `rm /private/tmp/tmp_unused`.

## Reproduce

The working files are in the conductor scratchpad, `60f6998b…/scratchpad/m14/`:
- `cands_a.py` (the Tier A candidate list);
- `tierb.py` (the Tier B scan);
- `check.py` (all checks);
- `gen.py` (manifest writer);
- `tierd_*`, `d3_*` and `named_*` (Tier D grep outputs).

## Addendum: manifest 14b, the conductor scratchpad extras (conductor request, 2026-10-06 about 18:15)

**File:** `runs/C-9/cleanup/manifest_scratch_prune_14b.txt`. It uses the same format, and its lines are tagged `14b:`. It has **10 entries, 1.94 GiB (2,030,600 KiB)**. Every entry passed the same checks as manifest 14 (run at 18:16).

| Entry | KiB | Basis |
|---|---:|---|
| `scratchpad/web_eor2/` | 1,410,796 | EOR2's private build mirror. EOR2 is parked, and its final code is committed at `b4de84e65` (verified present: "R-C9-152 -- sparks that read…"). The folder contains no symlinks. |
| `scratchpad/ov_raw/`, `ov_raw2/`, `ov_raw3/` | 417,796 | Raw overlay renders. The **final atlas `join1_vfx/eor_overlay/` is complete.** Every frame its `manifest.json` lists is present, and each file's sha256 matches: **1,678 of 1,678** (red 839 + original 839), 0 missing, 0 mismatched. |
| `scratchpad/frames1/`..`frames4/` | 174,852 | JPG frame dumps from Oct 2. |
| `scratchpad/r138_idles.glb` | 27,148 | **Byte-identical (sha256) to `C-9/so_mx/work/r138_idles.glb`.** |
| `/private/tmp/tmp_unused` | 8 | My own stray `du` listing (disclosed above). The 2-hour rule is waived for this file only: the conductor named it, and no lane owns it. |

**Lane BS check:**
- `lsof` showed no open handle on any entry.
- `SECTION_RESUME.md` names `tools/`, `godot/data/section_sw/`, `paint/section_sw/` and `section_sw/look/`, plus `SCRATCH=<scratch>` for its film tool.
- BS's film scratch in this scratchpad is `section_sw_film_*.avi` (`section_sw/film.log`), and that stays excluded.
- No BS tool or log names `web_eor2`, `ov_raw*`, `frames*` or the GLBs.

**Excluded from 14b: the other eight about-26 MB GLBs (211,400 KiB).** These are `b`, `h1`, `pA`, `pA6`, `pA8`, `pA10`, `t1` and `t2`. A sha256 compare over every same-size `.glb` in `runs/C-9/` and `reincarnated-godot/` found **no byte-identical copy** of any of them. They date from Oct 2 19:42–19:49, alongside lane SO's R-C9-138/140 work, so they look like probe variants rather than copies. Listing them needs lane SO or the conductor to confirm they are dead.

**Manifest 14 + 14b together:** 2,586 entries, **5.67 GiB**.

Run 14b exactly as manifest 14, with the path swapped to `manifest_scratch_prune_14b.txt` (dry run prints 10).
