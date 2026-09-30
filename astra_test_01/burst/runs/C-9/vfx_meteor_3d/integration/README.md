# Lane B Meteor → barrow_full: integration patch

**What it is.** Her Meteor, built 3D first, on the painted page behind `?meteor=b` (desktop: `-- --c sorceress --meteor b`). The bake-off accepted it. Lane A's painted ring and burning ground are worn as ground plates.

**What it does to the page without `?meteor=b`: nothing.**
- No hook runs.
- No shader changes: the painted surfaces and her ramp draw HEAD's shaders, byte for byte.
- `MeteorFx.wanted()` is one check, run once at load.

**Base:** barrow_full at collab HEAD `1d9686510`. Its barrow_full files are identical to `1a850e54b` (the cast-start hitch fix). `git apply --cached --check` passes against HEAD.

## Apply (about 2 minutes)

```bash
cd ~/Games/reincarnated-collaboration
P=astra_test_01/burst/runs/C-9/vfx_meteor_3d/integration/lane_b_meteor.patch
git apply --check "$P"          # against your working tree
git apply "$P"                  # or: git apply --3way "$P" if your Fire Ball work touched the same lines
```

Then rebuild the page as usual (`tools/build_web_painted.sh`).
- Its import step registers the new `MeteorFx` class.
- Its fence now also launches `--c sorceress --meteor b` and requires the `[meteor_b] armed ... plates_sha_ok=true ... warmed=true ... placeholder_meteor=off ... fire_ball=kept` line, with no script or shader error.

**Undo:** `git apply -R "$P"`

## What the patch touches

8 files; every edit to an existing file is additive.

| File | Change |
|---|---|
| `godot/project.godot` | A `[shader_globals]` section: the 10 `fx_*` globals. Required: the derived shaders read them. |
| `godot/scripts/painted_world.gd` | One block after `static var _shaders`: the FX uniforms and functions, and `with_fx(code, surface)`, a pure function that derives a painted surface's Meteor variant from its **live** code with asserted swaps. **No existing function changes.** |
| `godot/scripts/paint_stack.gd` | One block after `static var _shader_cache`: `with_char_fire(code)`, the fire's light folded **into the sun's pass** (see "Web fire light" below). **No existing function changes.** |
| `godot/scripts/barrow_full.gd` | Two hooks: `var meteor_fx`, and before `ready_done = true`: `if MeteorFx.wanted(self): meteor_fx = MeteorFx.attach(self)`. |
| `godot/scripts/meteor_fx.gd` | New. The effect, pooled (2), with everything built and warmed at attach. |
| `godot/data/meteor/plates.bin` + `manifest.json` | New, 95 KB. Lane A's ring (`VF-met-ring-01`) and burning ground (`C-5 VF-prim-fire-pool-01`) as one RGBA PNG (value index + alpha each). The manifest carries each source's sha256. Tracked (not under an ignored pattern). |
| `tools/build_web_painted.sh` | Ships `data/meteor/*`. Adds the `?meteor=b` launch fence. |

## How it runs

**`MeteorFx.attach(scene)`, once at load, does:**
- switches the placeholder Meteor off (`spell_fx.casts_by_slot` loses `chop`); the Fire Ball stays;
- reads the release time from her package (`casts.*.release_s` for the chop slot: 1.6333 s on v2);
- keeps both suns off the effect's layer (1 << 12);
- relabels `FxLabel`;
- derives the Meteor variant of every painted surface's material (27 painted, the snow, the heather) and every character-ramp material, one shader per distinct shader;
- draws everything once, unseen (`warm = 1`);
- prints `[meteor_b] armed`.

**The shader swap.** The variants are **swapped in only while a Meteor is alive** and swapped back when the last one ends.
- Measured cost: a shader carrying the ground terms costs about 1.5 ms per frame on the desktop even with its branch never taken. So the terms are never compiled into the idle page.
- If you add a character after load, call `meteor_fx.collect_materials()` so the fire lights it too.

**Shake** is the camera's `h_offset` / `v_offset`, never its transform.

**Nothing is created, freed or loaded at cast.** No light node exists: the fire's light on the characters is two globals.

## Web fire light: folded into the sun's pass

Compatibility sRGB-encodes each light's pass before adding them. That is PaintStack's ambient trap, and it is why the first build's separate omni light summed hot on the web. With the fold, the fire is one term added in linear light inside the ramp's own sun pass, on both renderers.

Measured on her with a frozen pose, as a linear fire-on/fire-off ratio, web minus desktop (`vfx_meteor_3d/artifacts/v2/web_fire_light_match.json`):

| Level | Red | Green | Blue |
|---|---|---|---|
| Burn (energy 2.8) | -0.006 | -0.001 | -0.001 |
| Impact hot (energy 6) | -0.017 | -0.001 | 0.000 |

Both are inside the 0.01–0.02 band the other meeting rules hold.

## Measured on lane B's copy (HEAD + this patch)

Evidence: `vfx_meteor_3d/artifacts/v2/`.

### Idle: Meteor never cast

`idle_ab_page_never_cast.json`. The page scene, run with barrow_full's own `--frame-cost`, windowed 1920×1080, alternated a b a b a b.

| Renderer | a: no `?meteor=b` | b: `?meteor=b` | b − a |
|---|---|---|---|
| Forward+ | 13.70 ms | 13.58 ms | −0.12 ms (noise) |
| Compatibility (`--as-web`) | 13.23 ms | 13.20 ms | −0.03 ms |

- **Unchanged.**
- The first build, which compiled the terms into every painted shader, measured +1.55 ms here. That is why the terms are swapped in, never left in.

### Cast budget, as the delta against the matched control

Cold caches; 1 cold cast, then 19 casts with the effect interleaved with 20 without.

**Desktop, Forward+ at 1080** (`perf_desktop_forward_plus_1080_cold.*`):

| Measure | Result |
|---|---|
| Effect cost | **+0.85 ms/frame** (script 0.03 ms) |
| Added draw calls at peak | **+4** |
| Worst frame, cold first cast (cast / release / impact) | 11.9 / 13.5 / 14.5 ms |
| Worst frame, warm casts | 13.9 / 15.0 / 14.6 ms |
| Worst frame, control | 13.7 / 13.9 / 14.5 ms |

**Web, Chrome at 844×390 @3x** (ANGLE Metal on the M2, fresh profile, 60 Hz this session; `perf_web_chrome_phone_size_cold.json`):
- 0 frames over 20 ms in any phase, cold first cast included (worst 19.1 ms, at her cast input, before the effect exists);
- render-CPU delta +0.05 ms/frame;
- script 0.04 ms;
- **+4** draw calls.

**Page idle in Chrome** (`chrome_page_idle_ab.json`, barrow_full's own `web_painted_test.js`, 844×390 @3x, 60 Hz; fps, higher is better):

| Phase | Without `?meteor=b` | With `?meteor=b` |
|---|---|---|
| Walking (never cast) | 55.0 / 55.0 | 55.0 / 54.8 |
| Standing: first 12 s after build, where the warm-up compiles land | 57.8 / 58.0 | 55.8 / 55.3 |

Build time is equal. Errors: 0.

### Fences

The patched `tools/build_web_painted.sh`, run verbatim with `--no-stage` on HEAD + patch: **19 ok, 0 FAIL**. That covers:
- every existing fence: 28/28 painted files, 54 plates, the instance counts, the pen, the blockout;
- `?c=sorceress` with her v2 releases `spells=placeholder:cast_fireball@0.9333,cast_meteor@1.6333`: the Fire Ball armed;
- the new `?meteor=b` fence.

### Web fire light

`web_fire_light_match.json`: see "Web fire light" above.

## Notes for the owner

- **Fire Ball bake.** If your bake replaces `spell_fx.gd`, keep a `casts_by_slot` dictionary with a `chop` key, or change the two lines in `MeteorFx._attach` that erase it. The fence's `placeholder_meteor=off` / `fire_ball=kept` words come from there.
- **Style switch.** `?meteor_style=procedural` swaps lane A's plates for the procedural ring and scorch (B1).
