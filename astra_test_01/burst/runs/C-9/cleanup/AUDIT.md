# Disk-cleanup audit: C-5 working folders and old captures (R-C9-70)

Read-only audit for gandalf, Run C-9, generated 2026-09-29 01:33. Nothing was deleted, moved or changed. The only files written are this note and the two manifests beside it.

**Status:** `manifest_c5_t3.json` has **already been executed** by the conductor: manifest committed in 63737cd5f, executed in 1897bcbae (55,879 deleted, 0 skipped, 5.87 GB freed; `deletions_c5_t3.log.gz`). `manifest_captures.json` has **not** been executed.

## Result

| Manifest | Frees | Files |
|---|---|---|
| `manifest_c5_t3.json` | **5.87 GB** | 55,879 |
| `manifest_captures.json` | **12.47 GB** | 16,528 |
| **Total** | **18.34 GB** | 72,407 |
| Held back, not in any delete list | 2.15 GB | 621 (FL1-fire-8dir-v44 frames, see below) |

Every listed file is untracked and is an image, a Godot import-cache file (`.godot/`, `.import`) or a Movie-Maker `.wav`. These always stay: git-tracked files, videos, all JSON/MD/TXT/logs/scripts/archives, declared burst deliverables, files cited by path or name, `evidence/` folders, and images named chosen/hero/final/compare/contact/sheet/board/consecutive/strip/montage. Recheck that each file exists, is untracked and matches its listed size at delete time, as `03_execute.py` already does.

## A. C-5 `t3/` (9.48 GB, 73 folders)

| Folder | Class | GB freed | Evidence |
|---|---|---|---|
| FL1-fire-8dir-v43 | SUPERSEDED | 2.15 | v43's dance layers were clipped (F-C5-43, R-C5-136); v44 was proven (R-C5-138) and shipped as web12 (M-C5-WEB12). The 621 raw frames go; the sheets, the native-crop board showing the defect, and both MP4s stay. |
| T4c | REGENERABLE | 1.85 | The conductor's Movie-Maker bakes, four-ground renders and replay-project copies, all made by tracked `export/replay.py`. Results kept: R-C5-9, `vo1_compare.json` (tracked), bg/vo1 JSON. VO1 clause closed (R-C5-44). |
| necro_walk_v21 | REGENERABLE | 0.32 | `grey_cast/` is the 91 frames of `cast_grey.mp4`, which stays in the same folder. Boards and stills stay. |
| E0a | REGENERABLE | 0.25 | Staged project and export copies (images byte-identical to artifacts of record) plus import cache. The ledger-cited boards stay. |
| T4b | REGENERABLE | 0.25 | Unpacked copies of the kept deliverable zips (870/870 files match by path, CRC and size) plus import cache. |
| FL-2 | REGENERABLE | 0.19 | Re-export and input-parallax copies, 100% byte-identical to artifacts of record. |
| E1-judge-v28 | REGENERABLE | 0.16 | Staged v28 project (= `artifacts/CS-pack-v28-r1`) plus import cache. Judge sheets and MP4s stay. |
| FL-2b | SUPERSEDED | 0.09 | FAILED-accepted-in-part and replaced by FL-2c's capsule collider (R-C5-96/97). Its copies are byte-identical to artifacts. |
| T4v | REGENERABLE | 0.09 | Export-check copy, 100% byte-identical to artifacts. |
| T4s-r1 | REGENERABLE | 0.09 | Export-check copy, 100% byte-identical to artifacts. |
| T4j | REGENERABLE | 0.07 | Import caches of already-pruned staged projects plus bake `.wav`. Test fixture JSON, byte-lock evidence and `test_tmp/` stay. |
| T4l | REGENERABLE | 0.07 | Import cache plus bake `.wav`. `evidence.tar.gz` and `legacy_hashes.json`, which the suite reads, stay. |
| T4g | REGENERABLE | 0.07 | Import cache of a staged project whose sources were already pruned, plus bake `.wav`. |
| T4q | REGENERABLE | 0.07 | Import cache plus bake `.wav`. The key-state boards stay. |
| T4o | REGENERABLE | 0.07 | Import cache plus bake `.wav`. |
| T4n-r1 | REGENERABLE | 0.07 | Import cache plus bake `.wav`. |
| FL1-fire-8dir-v31 … v42 (12) | SUPERSEDED | 0 | Older fire-lane captures. Their frames were purged at the time; only sheets, MP4s and logs remain. |
| FL1-fire-8dir-v44 | KEEP | 0 (2.15 conditional) | The final build. The web12 dispatch and deploy_truth cite this folder as the proof gate, and there is no MP4 of it (see below). |
| T4f · FL-2c | KEEP | 0 | Live test fixtures: `tests/test_t4d_export.py` reads `T4f/project`; `test_vfx_picker.py` runs Godot inside `FL-2c/reexport`. |
| T4x | KEEP | 0 | The suite rebuilds it on every run, and 164 of its files are the surviving copies that `lane_dupes_manifest.json` relies on. |
| 41 others | KEEP | 0 | Records, deliverable zips and archives, stills, or under 10 MB freeable: BL-1a-killed, BL-1a-r1, BL1-bwc-8dir-v38, E1-judge, E1-judge-v29, E1-keystates, E3-looks-v30, FL-1a, FL-1b, FL-3, FL-3b, FL-4a, FL-4b, FL-4c, FL-4d, FL-5, FL-5b, FL-5c, FL-6, FL-6b, FL-6c, T4a, T4d, T4e, T4e-r1, T4f-r1, T4h, T4h-r1, T4i, T4i-r1, T4k, T4m, T4n, T4p, T4r, T4s, T4s-r2, T4s-r3, T4t, T4u, T4w. |

## B. Old captures (13.28 GB in scope, 9 folders)

| Folder | Class | GB freed | Evidence |
|---|---|---|---|
| 2026-09-20-c8-whirlwind | SUPERSEDED | 2.19 | drax. `A_warlord2/` and `B_warlord3/` are the 190-frame sources of the two kept MP4s; builds warlord2 and warlord3 are superseded (C-8 handoff). `frames/` is a 90-frame trial capture made with the method NYQUIST-1 invalidated. The strips stay. |
| 2026-09-21-c8-whirlwind-w4 | SUPERSEDED | 2.71 | drax. `cap/` is the 390-frame source of the kept MP4. `frames/` is the aliased capture that `cap/` replaced. warlord4 was superseded by warlord5 (R-C8-7). |
| 2026-09-21-c8-whirlwind-w5 | REGENERABLE | 1.82 | drax. `cap/` is the 390-frame source of `whirlwind_warlord5.mp4`, which stays in the folder. |
| 2026-07-30-shadow-cal | REGENERABLE | 2.62 | galadriel. Its own `.gitignore` declares `tmp/` and `frames/` regenerable. The source video is now found on `/Volumes/reincarnated`, and every listed file was re-extracted byte-identical (both keyframe ladders, bursts, grabs). |
| 2026-08-08-eor-followup | REGENERABLE | 1.16 | galadriel. Its own `.gitignore` declares `work/` regenerable, and both sitting videos are present. The timestamped frames re-extract byte-identical. |
| 2026-07-29-wr1-gal3 | REGENERABLE | 0.90 | galadriel. Its own `.gitignore` declares the frames regenerable; all 460 frames re-extracted byte-identical. |
| 2026-08-07-eor-sittings | REGENERABLE | 0.58 | galadriel. Its own `.gitignore` declares the frames regenerable; the whole 1 fps series (3,532 files) re-extracted byte-identical with the note's command. Only the listed frame series go. |
| 2026-08-08-kc2-third-extraction | REGENERABLE | 0.35 | galadriel. There is no author claim here, so only the 137 timestamped raw frames proven byte-identical are listed. |
| 2026-07-28-gd-playtest-v1-g6 | REGENERABLE | 0.14 | galadriel. Only the thumbs, crops and tooltips re-derived byte-identical from the source stills are listed. |

How the 12.47 GB is backed:
- 6.72 GB are frames of a video kept in the same folder, or superseded captures.
- 4.23 GB were regenerated here file by file and matched by sha256.
- The remaining 1.52 GB are author-declared frame series whose source was proven by byte-exact re-extraction.

**Why the galadriel folders are listed now.** galadriel's own 2026-09-10 reclaim (`galadriel/notes/2026-09-10-captures-reclaim-manifest.md`) kept all six for one measured reason: the sources were unreachable. `play_test_2026-07-26.mp4` had vanished from `gd-scratch`, and `/Volumes/reincarnated` was not mounted. So the caches had become "the original". Today the volume is mounted and holds `play-test-v1/recorded_videos/play_test_2026-07-26.mp4` (13.1 GB, 6816.5 s), both EoR sitting videos, and the 313 G-6 source stills. That answers her NEEDS-MATT item 1 with option (a). The regeneration commands recorded in each folder's `.gitignore` and note reproduce the cached frames byte for byte. After deletion, that footage and those stills exist only on that external volume, where the originals always were.

## Left KEEP because unsure

- **FL1-fire-8dir-v44 frames (2.15 GB).** This is the final build, and web12 cites the folder as its proof gate; there is no MP4. It is listed under `conditional` in `manifest_c5_t3.json`. It becomes safe to release if you first encode the nine third-speed clips from these frames, as was done for v31–v42, or if you accept re-rendering from `artifacts/CS-pack-v44/godot` with `conductor_scripts/probe_cast_dir.gd`.
- **T4f, FL-2c (0.44 GB).** These are live suite fixtures. Pruning staged copies under the suite already broke tests once (N-C5-STAGED-FIXTURES, logged as a conductor error), and the fix that re-points the tests (FL-6d) never ran. Release them after the tests read artifacts of record.
- **shadow-cal leftovers.** `tmp/hw3` did not reproduce (0/60), so it stays. Also kept: the `draw*` debug drawings, `tmp/key`, `tmp/scan5`, the tmp-root images, the `.npy` arrays, and the 170 keyframe names cited by `FAILED-sc8-v*.json`.
- **eor-sittings `work/` root (310 images, about 142 MB).** These are mixed derived analysis images; the engine's `data/kc2/pe1_eor_spin_parameters.md` cites `s2-full-*.png` there. **eor-followup** `work/` root zooms and `_xN`/`view_` images stay too.
- **kc2-third-extraction** `evidence/` (untracked but cited) and its work-root composites. **G-6** composites, node-series, grid, counters and `LOC_*` tooltips are derived images I did not re-derive; its `sheets/` also stays.
- **T4h, T4h-r1, BL-1a-killed, T4r.** Regenerable, but under 10 MB each, so not worth a review.
- **Out of scope.** No other July–August galadriel folder is over 100 MB (the largest is `kc2-fourth-extraction` at 85 MB). September galadriel captures and all other drax captures were excluded as instructed.

## Notes for the executor

- `lane_dupes_manifest.json` uses 338 files in `t3/` as the surviving copy behind its DUP deletions. None of them is in `manifest_c5_t3.json`. There is no overlap with `manifest_godot_frames.json`.
- Two tools will fail if run as written after this deletion: the T4c README replay recipe names `t3/T4b/painted_project` (unzip `painted_project.zip` there first), and `T4g/verify_rendered.py` (never run; the question it answers was closed by R-C5-44) names `T4c/conductor/vo1_v21`.
- Charter §4 asks for every deletion to be recorded in the ledger (path, size, reason). Each manifest folder entry carries the reason.
- Correction to the executed t3 manifest: its T4j line says all `project/` PNGs were artifact copies. 57 of 59 were; the other two were synthetic solid-colour test cells (`idle_E_0`, `cast_E_0`, under 1 MB). Nothing else changes.
- Drax w5 holds the capture of the current playable build (warlord5). Its MP4 stays in the folder and the build is on disk, so a full-resolution re-capture is one probe run away.
