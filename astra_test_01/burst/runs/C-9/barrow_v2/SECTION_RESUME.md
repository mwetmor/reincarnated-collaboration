# barrow_v2 SECTION SW: resume notes (R-C9-158, lane BS, drax)

The south-west proof section: the wreck (p01), the coast and cliff, the sea cave and stair (p03), built in true 3D and painted by the v1 method.

## Pipeline (all re-runnable, in order)

1. **Build data:** `python3 tools/section_sw_build.py` writes `godot/data/section_sw/{section.json, terrain.f32, ground.png}`.
   - Its random placement is deterministic (seed 158).
   - The POST-FIXES block runs after every random draw, so local fixes there leave every floe, pebble and tuft unchanged.
2. **Guide render:** `godot --path godot --resolution 1280x720 --script tools/section_run.gd -- guide <tiles_dir>`, under the heavy lock.
   - This gives 4 x 4 tiles of 1984 x 1216.
   - Stitch them with `python3 tools/section_sw_stitch.py guide <tiles_dir>` to get `paint/section_sw/section_sw_guide.png` (7936 x 4864, plate density 100.6 px/m).
3. **Paint config:** `python3 tools/section_sw_paintcfg.py` writes `paint/section_sw/cfg_section_sw.json` (prefix BVSW; 36 chunks, 8 skipped).
4. **Paint:** `zsh tools/section_sw_drive.sh`. It is resumable: re-run it until `bvp_paint.py <cfg> status` shows todo 0.
   - Lane cap: 60 Astra images, counting BVSW bursts only.
   - A usage-limit message HALTs it with exit 7.
5. **Stitch the painting:** `python3 tools/section_sw_stitch.py paint` writes `section_sw_painted.png` and `seams.json`.
   - Skipped or missing chunks fall back to guide pixels.
6. **Stills:** `godot ... --resolution 1920x1080 --script tools/section_run.gd -- stills <dir> [paint=<painted.png>]`.
   - Without `paint=` you get the unpainted guide look.
7. **Film:** `SCRATCH=<scratch> tools/section_sw_film.sh <painted.png> section_sw/look/<name>.mp4`.
8. **Comparison sheets for Matt:** `python3 tools/section_sw_sheets.py` writes `section_sw/look/R-C9-158_*`.

## Frame

`guide px = ((x + 57.5) * ppm, (sin(a) y - cos(a) z + 4.0) * ppm)`, in the sim frame, with ppm 100.617553710938 and a 52.9535 deg pitch.

## State

The live state is in the ledger milestone `M-C9-BS-SECTION-SW` and in the hand-back.
