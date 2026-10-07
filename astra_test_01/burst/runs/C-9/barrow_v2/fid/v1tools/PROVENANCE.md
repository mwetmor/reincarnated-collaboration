# BV2F frozen v1 toolchain: provenance (lane PT, Phase 0.3)

**Rulings:** R-C9-163 (Gate-1 B-1 two-tier freeze), R-C9-166 (bases = HEAD files; as-run shas recorded here; the hazard where a copy resolves BF from its own location is fixed by arg/env or a pinned root, with Tier A kept byte-identical).
**Pin:** `0f8f73697` (`PIN_COMMIT`). Every "v1 sha" below and in `SHA256SUMS` comes from `git show 0f8f73697:astra_test_01/burst/runs/C-9/<path> | shasum -a 256`, never from the copies. `verify.sh` re-derives them on every run.
**All paths** are relative to `astra_test_01/burst/runs/C-9/`. Commit times are local (-04:00); ledger times are UTC.

## Files

| Tier | Shipped path | v1 source | v1 sha12 @ pin | Shipped sha12 | As-run by v1 (sha12, commit) and evidence |
|---|---|---|---|---|---|
| A | `tierA/conductor_scripts/guided_paint.py` | `conductor_scripts/guided_paint.py` | f2b2026eafed | = | Same file. Committed at 816fd84b8 (09-29 22:33 = 02:33Z), the start of T10BF-0_0. No later change. |
| A | `tierA/conductor_scripts/guided_stitch.py` | `conductor_scripts/guided_stitch.py` | ec26846c8c99 | = | Same file. 640fa39c6 is the only commit, and it is the stitch commit. Ledger M-C9-T10BF-PAINTED: a re-run reproduces the stitch byte for byte. |
| A | `tierA/conductor_scripts/wave.sh` | `conductor_scripts/wave.sh` | bf1c8a5ecd1d | = | Same file. 1eb213d2d (09-26) is the only commit. |
| A | `tierA/conductor_scripts/refs_guard.py` | `conductor_scripts/refs_guard.py` | 708a67dd0a16 | = | **Two versions ran.** `2f2f539f949f` (e829fdb80) for the chunks briefed before 57c04ef86 (09-29 23:22:52 = 03:22:52Z): 0_0 through 2_2, 12 chunks (ledger bursts 286–298). `708a67dd0a16` (57c04ef86 = HEAD) for 3_2, 1_3, 2_3 and 3_3 (from the 06:00:49Z restart). The diff only adds names to `FORBID`. The edit time is bounded by the commit time. |
| A | `tierA/conductor_scripts/cfg_t10bf.json` | `conductor_scripts/cfg_t10bf.json` | 08027d0ea791 | = | Same file. Committed at 816fd84b8, the only commit. It carries v1's `geo`, `rules` and `refs` brief (plan W3) and the 4×4 grid. Guide sha `e866051c` is recorded in `_guide_sha256`. |
| A | `tierA/barrow_full/tools/heather_instances.py` | `barrow_full/tools/heather_instances.py` | 51eb1ae519d8 | = | Same file. 3b8a4fbfd is the only commit; `take/build/heather_instances.json` was made by it in the same commit. |
| A | `tierA/barrow_full/tools/hero_surface.py` | `barrow_full/tools/hero_surface.py` | 44fc5bf92288 | = | Same file. 3b8a4fbfd is the only commit. |
| A | `tierA/barrow_full/tools/t5_06b_bake.py` | `barrow_full/tools/t5_06b_bake.py` | 28b2dc11dcd1 | = | **Two copies exist and are byte-identical**: `nb_t8/scripts/t5_06b_bake.py` is also `28b2dc11dcd1`. v1 ran the `barrow_full/tools` copy: `bake_heroes.py:27` (`BAKE = HERE/t5_06b_bake.py`) asserts it equals nb_t8's (`:36`), and `take/build/bake_report.json:3` records the sha `28b2dc11dcd18b6b…`. |
| A | `tierA/barrow_full/tools/make_layout.py` | `barrow_full/tools/make_layout.py` | 3629eaaf5fc8 | = | Reference only. b65f1dfae (kerb text) is the layout's last commit. It imports the sibling `geom2d.py`, which is not frozen. |
| A | `tierA/nb_t8/scripts/t5_06a_surface.py` | `nb_t8/scripts/t5_06a_surface.py` | b954e825bc24 | = | Frozen per R-C9-163. **v1's level did not run it**: `hero_surface.py:13-24` ("WHY NOT t5_06a ITSELF") replaced it for the placed heroes. It is a Blender script. |
| B | `tierB/barrow_full/godot/tools/capture_blockout.gd` | `barrow_full/godot/tools/capture_blockout.gd` | f630f564c1fd | see SHA256SUMS | The guide was rendered by **`feaa1c94f1ff` (e0462ab03)**. HEAD (111c85f5d) adds `--painted` with default false, so the blockout path is unchanged. **There is a second copy, `barrow_full/app/tools/`, byte-identical (`f630f564c1fd`).** It is the export mirror (`build_app_painted.sh:65` rsyncs `godot/` → `app/`; `app/` is gitignored at `barrow_full/.gitignore:7`). v1 ran the `godot/` copy. |
| B | `tierB/barrow_full/godot/tools/capture_ids.gd` | `barrow_full/godot/tools/capture_ids.gd` | 7e6e16369489 | see SHA256SUMS | Same as HEAD. 46181364c is the only commit. **The `app/tools/` copy is byte-identical** (the mirror, as above). `take/take_report.json` `regenerate` records `Godot --path godot … tools/capture_ids.gd`. Re-run at HEAD in 0.1 T1: ids.png and ids.json are byte-identical to v1's. |
| B | `tierB/barrow_full/tools/paint_world_prep.py` | `barrow_full/tools/paint_world_prep.py` | b77325d07621 | see SHA256SUMS | The level was built by **`21ca10b2c89a` (111c85f5d)**. HEAD (5f96ba0fe) only adds `web()` / `--web`; `main()` is unchanged. |
| B | `tierB/barrow_full/tools/take_from_paint.py` | `barrow_full/tools/take_from_paint.py` | 17998c5a986a | see SHA256SUMS | The first take used **`8c745b812ad6` (46181364c)**. HEAD (3b8a4fbfd) changed the tuft density base line, and `tufts.json` was re-made with it in that commit, so HEAD is v1's final take tool. Re-run at HEAD in 0.1: all take outputs are byte-identical to the tracked ones. |
| B | `tierB/conductor_scripts/t10bf_drive.sh` | `conductor_scripts/t10bf_drive.sh` | 8c2c32ec21a5 | see SHA256SUMS | **HEAD never ran.** It was committed at 174512232 (06:28 = 10:28Z), after the last chunk ended at 06:12:15Z. As run: **`e2f5f37d68a0` (816fd84b8, 41 GiB guard)** from 02:33Z to 06:00Z, then **`4ba9b86c6544` (32d068af9, 25 GiB)** from the 06:00:49Z restart (ledger N-C9-DRIVE-STALL). The three versions differ only in the disk-guard constant and its comment. |
| own | `v1run.py`, `godot_run.sh`, `cfg_check.py`, `frame_grid.v1.json`, `DEV12_substitutions.json`, `DEV11_refs.json` | — | — | see `SHA256SUMS` | BV2F-own files (runners, cfg check, config, DEV tables). |

## Hard-coded frame/grid constants (audit list; Tier-B patches touch only the ALLOWLIST lines)

- `guided_paint.py`: `:25` stride 1280×768 · `:26` canvas 1536×1024 · `:31-32` the same · `:35`, `:44`, `:46` 256 / 1536×1024 in the brief text · `:5` artifact paths (absolute; `S` = `artifacts/CS9-guides`). Cols and rows come from the cfg (`:6`). **Tier A.** BV2F keeps v1's canvas and stride; the grid size goes in the cfg.
- `guided_stitch.py`: `:12` W, H, SX, SY = 1536, 1024, 1280, 768 · `:10` artifacts path. **Tier A** (same reason).
- `wave.sh`: `:3`, `:4` paths (the burst root, the log dir, the c9-shared scratch). **Tier A.**
- `refs_guard.py`: `:6-8` repo paths · `:9-13` ALLOW sha pins. **Tier A.**
- `t10bf_drive.sh`: `:6` CFG path · `:7` log name · `:9` / `:20` / `:22` / `:27` prefix T10BF · `:12` disk 20. → **Tier B**: cfg from argv, prefix and log from the cfg, `$A` frozen calls, verify first, exit 7 (DEV-15). Disk 20 is kept.
- `capture_blockout.gd`: `:26` GUIDE 5376×3328 · `:27` PLAY 1920×1080 · `:28` CRUCIBLE_SHOT · `:29-30` TOP / TOP_PX_PER_M · `:33-35` GRID_STEP / U / V · `:71` scene · `:111` comment. → **Tier B**: GUIDE, TOP*, GRID* and the scene.
- `capture_ids.gd`: `:23` GUIDE · `:47` scene · `:131-132` 100.617553710938 / 80.3076 · `:145`, `:149`, `:151` labels. → **Tier B**: GUIDE, the scene, and the `:145` / `:151` labels (now formatted from GUIDE, with identical bytes for v1). The `:131-132` and `:149` px/m and pitch stay: M0(c) keeps v1's zoom.
- `paint_world_prep.py`: `:34-39` paths and sha prefix · `:43` PPM · `:44` PITCH · `:46` yaw 47 · `:387` snow field/trail 768/1024 px · `:400-403` web. → **Tier B**: painting, sha prefix, PPM, PITCH and yaw.
- `take_from_paint.py`: `:40` painting default · `:42` sha prefix · `:44` layout path · `:276` RES 10 · `:404` GRES 20 · `:345` / `:395` px filter sizes. → **Tier B**: painting and sha prefix. The frame is already read from the layout (`:46-58`).
- `heather_instances.py`: `:39` STEP 0.15. The frame comes from tufts.json and the layout. **Tier A.**
- `hero_surface.py`: `:32` SIZE 1024 · `:37` SS 4. The camera comes from plates.json. **Tier A.**
- `t5_06b_bake.py`: none (the cell comes from the sheet). **Tier A.**
- **Data, not tools:** two v1 layout copies differ. Root `barrow_full_layout.json` (`3c9a47c9ac23`) is read by take_from_paint and heather_instances. `godot/data/barrow_full_layout.json` (`abe8256fad68`) is read by paint_world_prep and the scene.

## The BF-from-own-location hazard and its fix

v1's python tools locate their inputs from their own path: `HERE = dirname(__file__)`, and `BF` / `ROOT = dirname(HERE)`. This is true of take_from_paint, paint_world_prep, heather_instances, hero_surface, t5_06b_bake (ROOT) and t5_06a_surface (ROOT). A frozen copy run in place would read `fid/v1tools/<tier>/barrow_full/`.

**Fix: `v1run.py --root <WORKROOT> <tier>/<path/tool.py> [args]`.** It checks the frozen bytes against `SHA256SUMS`, sets the tool's `__file__` to `<WORKROOT>/<tool's dir name>/<name>`, and execs those bytes, so BF = WORKROOT. Tier A files are not copied or edited. Under Blender, use `blender -b --python v1run.py -- --root R tierA/nb_t8/scripts/t5_06a_surface.py -- <args>`.

The GD tools run inside a Godot project. Use `--script <abs path to tierB/…gd>` against the level's project; the path is proven by the 0.3 freeze-proof run (see `RESUME_PT.md`).

## Proofs

- `verify.sh` is green at the pin. It goes RED, exit 1, on each of: a tampered Tier-A copy, a driver line naming the original `conductor_scripts/wave.sh`, and a driver line calling `$C/refs_guard.py`. The tests were run in place and restored from backups; the log is `fid/pc/run/verify_red_tests.txt`.
- DEV-15: the driver's exit-7 clause, run on a simulated limit message, gives exit 7 plus a HALT log line; on a clean run it gives no exit. The log is `fid/pc/run/dev15_dryrun.txt`.
- Freeze proof: 0.1's ID self-test re-run through the patched `capture_ids.gd` with `frame_grid.v1.json` must reproduce the unpatched result. See `RESUME_PT.md`.

## Gate-2 folds (R-C9-173; jack-ryan W-1, W-2)

- **W-1:** `verify.sh` now fails any non-blank added patch line that neither carries `BV2F` nor sits inside a `BV2F-BEGIN` … `BV2F-END` block. The Tier-B files gained comment-only markers for this (same pin; only the shipped shas changed).
  - RED test: an unmarked `var PX_OVERRIDE := 101.0`, with its diff and SUMS row regenerated so that only W-1 can catch it, gives exit 1 (`fid/pc/run/verify_red_tests.txt`).
  - Re-proofs after the markers: `take_from_paint.py` via `v1run.py` gives 6/6 outputs byte-identical; `capture_ids.gd` via `godot_run.sh` gives ids.png `ed9cfcd207c1` and ids.json `f9e63ebe605c`, equal to v1.
- **W-2(a):** `cfg_check.py <cfg>` is called by the driver before staging (exit 9). It requires `rules` == v1 `rules` with `DEV12_substitutions.json` applied, and `refs` == v1 `refs` + `DEV11_refs.json`. Both tables are empty until LV's Phase-1 class list and the Phase-2 A/B fill them; empty means verbatim v1. Tested: the v1 cfg gives OK; one changed word in `rules` gives HALT.
- **W-2(b):** `lane/run_burst.py` is shared lane infrastructure, not a v1 tool, so it is recorded rather than frozen. `verify.sh` WARNs (it does not fail) if it drifts from:

run_burst_pin_sha256 2d6607679807ea4f9e076bb78d0bd6e777634fd62ddb2809b5e91e528e75e966

- **W-2(c):** `godot_run.sh <project> <tier/path.gd> [-- args]` runs `verify.sh`. It checks that the `.gd` is a SHA256SUMS row under `tierA/` or `tierB/` with a matching sha (else exit 10), applies the disk gate of 21, and runs Godot by absolute path behind the heavy lock. Tested: an outside path gives exit 10; an unlisted file gives exit 10.

### Control-file shas at this fold (record for the ledger milestone)

```
b7e68c0f3f267c1ab2b257b0a2f645182b3d07e14751f993ac0271747119e65a  verify.sh
2098d92f850e475544888ba1965eeef9ba99953b4ddeadb812657cb2d71217db  ALLOWLIST.md
197abbac7212e2595807dd1cdac2005aee3203701312abf7071a0dad915fdb9a  patches/capture_blockout.gd.diff
41ce20ec30f15104376f0ab011760cb4aba15314aa3a823c1ed5cb4e7fb5b45f  patches/capture_ids.gd.diff
6fb95f2d7c13ebbfa1fd93e93b99631ba0ab1f033574234f8490f41e55dff260  patches/paint_world_prep.py.diff
bdc2532e2fe78ed2c9ad72ee96884ce5c7db6bc919574b29e2841e666a1837f7  patches/t10bf_drive.sh.diff
8e4fe6821f6b45c9f0c89331967b6cd912cefbf1206959ea74822541acbad625  patches/take_from_paint.py.diff
49c2633b7646b4017b1c6da37f69b77bc792a93ae8dd53d20ea07bbf07374d8c  SHA256SUMS
```
