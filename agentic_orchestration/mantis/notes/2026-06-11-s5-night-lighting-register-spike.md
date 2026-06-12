# SPIKE S5 — Night-exterior Lighting Register

**Date:** 2026-06-11 (PC session, WSL-headless via db-lyon bridge)
**Author:** mantis (UE 5.7 seam)
**Dispatch:** Manifestation Moment Phase-1 spike wave, Track A (Matt-authorized 2026-06-11; dispatched by david-h)
**Verdict:** **PASS (authoring-complete; render-evidence WINDOWED-GATED)**
**Consult lineage:** radagast `2026-06-10-manifestation-moment-ue-feasibility-consult.md` § 3.4 (lighting rig) + § 5 row S5
**Companion:** `2026-06-11-s1-sky-from-ground-celestial-sphere-spike.md` (built into the same level)

---

## 1. What proved

A **reusable** night-knoll testbed level was authored headlessly and persists clean across editor restarts.

- **Level:** `/Game/Maps/LV_ManifestationKnoll` — on disk `Content/Maps/LV_ManifestationKnoll.umap` (32 KB). Built as a REUSABLE persistent-realm level per the operator-framing guard (recurring jump-in/jump-out transition; Earth is a returnable hub). NOT baked into `LS_Materialization_Cinematic` or any one-shot sequence.
- **Composition:** `Knoll_Ground` (Shape_Plane scaled 120× → ~12,000 UU wide, low horizon) + `Knoll_Hill` (Shape_Cube scaled 40×40×6, sunk to z=-260, gentle mound) + `ExponentialHeightFog` (subtle night haze). Sky-dominant, low-horizon as canon requires.
- **Figure stand-in:** `FigureStandIn` = `SKM_Quinn_Simple` (clean UE biped from NiagaraExamples Gallery — internal test only, never player-facing; honors the no-Crusader player-facing intent). Placed on the hill crest for the readability check.

### Rig A (hybrid; recommended per consult § 3.4) — all tagged `RigA`
| Actor | Type | Parameters (landed) |
|---|---|---|
| `RigA_Moonlight` | DirectionalLight | intensity 0.6 lux, color (150,175,220) cool, pitch −55° yaw 35° |
| `RigA_Skylight` | SkyLight | intensity 0.4, color (120,140,200) — ambient sky fill (cosmograph cubemap capture is the production source; SLS_CapturedScene default for now) |
| `RigA_SpiritGlow` | PointLight | intensity 2200, color (180,210,255), at (120,0,110) — DIEGETIC fill where the spirit form stands (the becoming lights the scene; motivates ground-figure readability in-fiction) |
| `RigA_PPV` | PostProcessVolume | **bUnbound=true; manual exposure LOCK** |

**Manual exposure lock (the load-bearing trap-fix):** `Settings.AutoExposureMethod = AEM_Manual`, `AutoExposureMinBrightness = AutoExposureMaxBrightness = 0.03`, `AutoExposureBias = -2.0`, all override-flags set. This pins the bright-sky/dark-ground composition so auto-exposure cannot wash out the stars or crush the ground (the exact trap consult § 2.4 flagged).

### Rig B (comparison; pure-emissive night) — tagged `RigB`
- `RigB_SpiritGlowOnly` PointLight (intensity 1600) only — no directional key, no skylight. **Disabled by default** (`bHidden=true`); toggle visibility in a windowed session to A/B against Rig A.

---

## 2. What is WINDOWED-GATED (not done; clean gate)

**Environment reality check (dispatch P0.1) — RESOLVED to a sharper gate than cold-DDC.** The documented cold-DDC stall did NOT occur. The shader DDC is warm enough that the editor reaches PostEngineInit and the bridge binds on `ws://127.0.0.1:9877` in ~22 s. The real blocker for windowed work from the SSH/WSL context is different and cleaner:

> **A windowed launch crashes at viewport creation:** `DXGI_ERROR_NOT_CURRENTLY_AVAILABLE` at `WindowsD3D12Viewport.cpp:149` → `SlateRHIRenderer` → `MainFrame`. The SSH/WSL session has no interactive GPU-attached Windows desktop, so DXGI cannot acquire a swap-chain for the editor window. The bridge starts fine; rendering surface creation is what fails.

**Consequence:** anything needing a render surface (PIE, `capture_screenshot`, `capture_scene_png`, FPS / `stat unit`, TSR observation) cannot run from this SSH/WSL context. All asset/level/actor/material authoring runs cleanly **headless with `-nullrhi -nosound`** (bridge binds in ~20 s, no crash, perf-stats responsive). This is the proven WS3.1 / spike pattern and is what was used here.

**Deferred to a real desktop session (Matt at PC, or RDP/console-attached):**
1. High-res screenshots of Rig A vs Rig B from the `Cam_GroundLookUp` ground POV.
2. Figure-readability A/B judgment (`FigureStandIn` under Rig A vs Rig B; toggle `RigB_SpiritGlowOnly` visibility on + Rig A actors off).
3. Confirm manual-exposure EV reads correctly at night (tune `AutoExposureBias` if the 0.03 brightness lock is too dark/bright once rendered).

---

## 3. Scaffold register (Discipline #40)

| # | Scaffold | Value landed | Locked by |
|---|---|---|---|
| 1 | Moonlight intensity | 0.6 lux (cool) | windowed render judgment + Matt #5 |
| 2 | Skylight intensity | 0.4 | windowed render + cosmograph-cubemap production source |
| 3 | Spirit-glow intensity | 2200 (point) | S2 spirit-form integration + render judgment |
| 4 | Manual exposure EV | min=max brightness 0.03, bias −2.0 | windowed render tuning |
| 5 | Hill geometry | Shape_Cube proxy (sunk cube) | landscape/sculpt pass later; proxy reads the composition only |
| 6 | Ground material | Shape_Plane default | environment-art pass |
| 7 | Fog density | 0.02 (clamped from request) | render judgment |
| 8 | Figure stand-in | SKM_Quinn_Simple (internal test only) | S6 avatar pipeline (the real Earth avatar) |

No value here is faked-as-substrate; all are deliberate placeholders for the static-scene feeling check (MVP falsifiable floor #5).

---

## 4. Bridge / tooling learnings (for the seam)

- Windows `node.exe` at `C:\Program Files\nodejs\node.exe` (v24); WSL `/tmp` maps to Windows `C:\tmp` — keep scripts inside the project tree and call with Windows paths.
- `spawn_light` supports point/spot/directional/rect/sky with location/rotation/intensity/color/label/onConflict.
- `set_actor_property` supports nested dot-paths (`Settings.AutoExposureMethod`) + `force` to bypass EditDefaultsOnly. **Enum values must be the NAME string** (`AEM_Manual`), not the integer.
- `set_fog_properties` requires an `ExponentialHeightFog` actor to already exist (place it first).
- `list_assets` directory filtering is unreliable (returns /Game root regardless of `directoryPath`/`path`); use `search_assets` by name + filter on `className`.

---

## 5. What P1.5 scene assembly still needs from S5

- A real desktop render session for the #5 mythic-weight judgment (screenshots + Rig A/B comparison).
- The S6 Earth avatar to replace `FigureStandIn`.
- The S2 ambiguous spirit form to replace `RigA_SpiritGlow`'s placeholder position (the glow becomes diegetically motivated by the actual becoming).
- Exposure-bias fine-tune once rendered.

**Scripts (rerunnable):** `Reincarnated/spike-s5-s1/s5-night-lighting.js` + `s5-fixups.js` (bridge on 9877; headless `-nullrhi` editor must be running).
**Result:** 23 PASS / 2 benign WARN (initial), then 11/11 PASS (fixups). Level persisted; 18 actors total (incl. S1).
