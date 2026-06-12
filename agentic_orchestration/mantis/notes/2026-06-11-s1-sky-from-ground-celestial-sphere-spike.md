# SPIKE S1 — Sky-from-Ground Celestial Sphere

**Date:** 2026-06-11 (PC session, WSL-headless via db-lyon bridge)
**Author:** mantis (UE 5.7 seam)
**Dispatch:** Manifestation Moment Phase-1 spike wave, Track A (Matt-authorized 2026-06-11; dispatched by david-h)
**Verdict:** **PARTIAL-PASS (sphere data + sky assets + scene placement proved headless; render measurements + position-array binding WINDOWED/BP-GATED)**
**Consult lineage:** radagast `2026-06-10-manifestation-moment-ue-feasibility-consult.md` § 3.2 (sky architecture) + § 5 row S1
**Built into:** `/Game/Maps/LV_ManifestationKnoll` (the S5 night rig — companion note `2026-06-11-s5-night-lighting-register-spike.md`)
**Landed sphere radius R = 8,000 UU** (order-10⁴ class per dispatch; empirical default, see § 4).

---

## 1. What proved (headless)

### 1.1 Sphere-interior star positions (the real deliverable)
Generated `Content/Data/CosmographSpike/cosmograph_sphere_001000stars_R8000.json` (230 KB):
- **1,000 stars** projected onto the sphere INTERIOR surface at **radius R = 8,000 UU** around scene origin. Verified: every star at radial distance exactly 8,000 UU; bounds a full sphere (±~8,000 on each axis).
- **6 element clusters** preserved as coherent sky regions via per-cluster spherical-Fibonacci caps (~35° half-angle each), cap centers spread over the full sphere. Below-horizon stars are intentional — the ground-POV camera looks UP into one portion.
- Carries `star_positions_flat` ([x,y,z,…]) and `star_colors_flat` ([r,g,b,a,…]) arrays pre-shaped for `SetNiagaraArrayVector`/`SetNiagaraArrayColor`, plus per-star records with `color_hue`, `brightness`, `sprite_size_uu`.
- This is a **logical sphere** (point positions at radius R), NOT a physical inverted mesh — exactly as the dispatch + consult § 3.2 require.

### 1.2 Sky Niagara system + materials (persisted)
- `NS_CelestialSphere` (`Content/VFX/NS_CelestialSphere.uasset`, 176 KB) — duplicated from the proven `NS_CosmographPointCloud` (criterion 3.7 GREEN lineage; 1 "Minimal" CPU-sprite emitter).
- `M_StarSprite_Emissive` — Unlit + Additive, bright base color; Niagara sprite vertex color multiplies in at render so per-star `color_hue` still drives final color.
- `M_ConstellationLine_Emissive` — Unlit + Additive, dim (0.3,0.4,0.6) — the ribbon/edge-test material.
- All three recompile clean and persist on disk.

### 1.3 Scene placement (in LV_ManifestationKnoll)
- `CelestialSphere_Sky` (NiagaraActor, `NS_CelestialSphere`) at scene origin (0,0,0) — this actor's transform IS the "twirl" container: rotating it rotates the whole starfield around the ground-anchored camera (never rotate the camera — preserves the sky-feels-like-sky read).
- `Cam_GroundLookUp` (CineCameraActor) at (0,−300,170) pitched +45° up — ground-POV establishing look-up.
- `NebulaBackdrop` (Shape_Sphere scaled 240× → ~12,000 UU radius, beyond R) with `MI_VDB_Nebula` material (the in-project VDB nebula asset) as the static depth backdrop beyond the sphere (MVP backdrop per dispatch; VDB Heterogeneous Volume is the production path, deferred to S7).

---

## 2. What is GATED (not done; two distinct gates)

### Gate A — position-array binding (BP or windowed; bridge cannot do it headless)
`NS_CosmographPointCloud`/`NS_CelestialSphere` expose **0 user parameters** (the Session-3 spike set positions inside the emitter, not via exposed array user-params as the design doc had projected). And the bridge's `set_niagara_parameter` supports only float/vector/bool/int — **NO array support** (verified in `NiagaraHandlers.cpp`). So pushing the 1,000 sphere positions into the system requires one of:
1. A **Blueprint** (`BP_CelestialSphere`) that loads the JSON and calls `UNiagaraDataInterfaceArrayFunctionLibrary::SetNiagaraArrayVector("StarPositions", …)` + `SetNiagaraArrayColor("StarColors", …)` on the component — the proven `BP_CosmographTest` pattern from the spike. The emitter must first expose `StarPositions`/`StarColors` user-param arrays and sample them in Particle Spawn (Initialize Particle → array-indexed position). This emitter edit + BP authoring is a **windowed-editor task** (Niagara stack editing through the bridge headless is not validated for array-DI sampling).
2. Until then, `NS_CelestialSphere` renders the original spike's freestanding ±67 UU cloud positions, NOT the sphere — placeholder geometry, correct system, wrong positions.

### Gate B — render measurements (windowed; same DXGI gate as S5)
Per S5 § 2: windowed launch from SSH/WSL crashes at viewport creation (`DXGI_ERROR_NOT_CURRENTLY_AVAILABLE`). So the falsifiable measurements MUST run in a real desktop session:
- **TSR stability under sphere rotation** — rotate `CelestialSphere_Sky` and watch small bright additive sprites near the horizon for ghosting/smearing (the twirl is the TSR stress case criterion 3.6's idle-anim test did not cover). Use the ARPG TSR config (motion blur off, History SP 100, ghost rejection 2).
- **FPS at full stack** vs 60 FPS PC target — stars + ribbon edges + emissive star material + nebula backdrop together (criterion 3.7 measured sprite-only).
- **Sprite angular-size read at R = 8,000 UU** — the falsifiable read is "sky full of stars WITH DEPTH, not a particle effect." Tune `sprite_size_uu` until stars read as distant points, not near sprites. R itself may need adjustment (§ 4).

---

## 3. Scaffold register (Discipline #40)

| # | Scaffold | Value landed | Locked by |
|---|---|---|---|
| 1 | **Star positions** | spherical-Fibonacci projection of tier-2 (1,000) spike cluster data — **FLAGGED PLACEHOLDER, never faked-as-substrate** | contract 6.7 (cosmograph spatial-layout emit — does NOT yet exist) + Phase 2 |
| 2 | Sphere radius R | **8,000 UU** (order-10⁴ class; empirical default) | windowed sprite-size read + art direction (§ 4) |
| 3 | Cluster count | **6** (tier-2 element clusters) — NB consult R4 flags 6-group vs 7-anchor unreconciled; tier-2 data is 6-cluster, so this spike is 6 | Pattern B reconciliation; re-project when 7-region canon + contract 6.7 land |
| 4 | Cap half-angle | ~35° (0.62 rad) — clusters read as distinct constellated regions | windowed visual read |
| 5 | Star distribution | spherical Fibonacci | consult § 7 / WS2 perf+visual |
| 6 | Sky system positions | original spike cloud until BP-bound (Gate A) | windowed BP authoring |
| 7 | Nebula backdrop | static Shape_Sphere + MI_VDB_Nebula (MVP) | S7 VDB Heterogeneous Volume (production) |
| 8 | Star material color | per-star vertex color × Unlit base | windowed VertexColor→Emissive explicit wiring |

**NO rune anchor in this spike** — rune-in-MVP awaits Matt's Pattern-B scope-lock (consult § 7 #5). Not pre-empted, per dispatch.

---

## 4. R = 8,000 UU — why, and the falsifiable adjustment

R was chosen at the low end of the order-10⁴ class. Rationale: tier-2 source data is ~±70 UU; the sky must sit far enough for parallax read ("depth, not flat backdrop") yet near enough to feel "reachable" (consult § 2.6). 8,000 UU puts the sphere ~80 m out — beyond the ~12,000 UU nebula backdrop sits further still. **This is the empirical knob the windowed read tunes:** if stars read as near sprites, push R up (10,000–20,000) and shrink `sprite_size_uu`; if the sky feels detached/tiny, pull R down. Report the landed value back to the scaffold register after the render session. The position generator (`gen-sphere-stars.js`) takes R as a one-line constant — regenerating at a new R is ~1 s.

---

## 5. What P1.5 scene assembly still needs from S1

1. **Windowed BP-binding session** (Gate A): expose `StarPositions`/`StarColors` array user-params on the emitter; author `BP_CelestialSphere` to load `cosmograph_sphere_001000stars_R8000.json` and bind the arrays. This makes the sky render the sphere instead of the spike cloud.
2. **Render measurement session** (Gate B): TSR-under-rotation, full-stack FPS, sprite-size + R tuning, screenshots from `Cam_GroundLookUp`.
3. **Ribbon/edge test**: wire `M_ConstellationLine_Emissive` to a ribbon emitter using the 2,000 `constellation_edges` (Emitter B per criterion 3.7) — currently the material exists but no ribbon emitter is authored (windowed Niagara work).
4. **6→7 region reconciliation** (consult R4): when contract 6.7 + the 7-anchor canon land, re-project from substrate-truthful kit→constellation placement (retires scaffold #1+#3).

**Scripts (rerunnable):** `Reincarnated/spike-s5-s1/gen-sphere-stars.js` (data) + `s1-celestial-sphere.js` + `s1-recompile.js` (bridge on 9877; headless `-nullrhi` editor running).
**Result:** 22 PASS / 2 benign WARN (param-name on recompile), then 3/3 PASS. Sphere data + 3 VFX assets + 3 sky actors persisted.
