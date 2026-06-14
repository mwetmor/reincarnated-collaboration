# MANUAL-BP-STEP LIST for Matt (PC Console / Tier-B Session) — Celestial-Sphere Rework + Figure-Lighting Repair

**STATUS:** CURRENT — Tier-A handoff deliverable for dispatch `2026-06-13-mantis-celestial-sphere-rework-and-figure-lighting-rig-repair.md`.
**Date:** 2026-06-13
**Author:** mantis (UE 5.7 seam)
**For:** Matt, at the PC console (`TheSa` render profile — the only profile with UE installed; DDC warm). Windowed editor REQUIRED for these (Niagara-stack + Lit-render). NEVER from SSH/WSL (DXGI crash).
**Math reference (read alongside):** `2026-06-13-celestial-sphere-math-transform-and-particle-count-rootcause.md` — esp. § 3 (Rx(+90°) transform), § 4 (root-cause), § 6 (`stat gpu` threshold).
**Pristine-scene note:** the prior session left `LV_ManifestationKnoll` UNSAVED (sphere deletion + CVar disarm + visibility toggles all reverted on reload). So at open you have the ORIGINAL 12-actor scene back, including the origin star-cloud. These steps assume that pristine state.

---

## Pre-flight (do first, every time)

1. Launch UE on `TheSa` (windowed, normal — NOT `-nullrhi`). Open `/Game/Maps/LV_ManifestationKnoll`.
2. **Do NOT pilot `Cam_GroundLookUp` yet** (the origin cloud + un-cost-cut nebula will crash the GPU as before). Stay on free-cam, sphere distant = safe.
3. Console (`` ` ``), session-only safety disarm so you can work without the crash while editing:
   ```
   r.HeterogeneousVolumes 0
   r.VolumetricFog 0
   ```
   (You will RE-ENABLE these after the cost-cut, step M6, to measure the real sky.)

---

## M1 — Inspect + understand the inherited spawn (root-cause confirm, A1)

Open `/Game/VFX/NS_CelestialSphere` in the Niagara editor.
1. Select the emitter (`Minimal`/inherited from `NS_CosmographPointCloud`).
2. Read **Emitter Properties → Sim Target** = `CPUSim` (confirms § 4).
3. Read the **Spawn (SpawnBurst_Instantaneous) → Spawn Count** and **Loop Count Limit** + **Emitter State → Loop Duration** (`InfiniteLoopDuration`). **Record the Spawn Count number** — this × loop behaviour is the source of the 1,005,000 (the exact arithmetic mantis could not read from the packed binary; you can read it here). Note it back to david-h/sam for the A1 close.
4. Confirm there is NO `StarPositions` array driving spawn (it was never bound — that's the defect).

## M2 — Migrate to GPU sim + fixed bounds (A2)

1. Emitter Properties → **Sim Target → GPUCompute Sim**.
2. Emitter Properties → **Calculate Bounds Mode → Fixed**, set Fixed Bounds to a box half-extent ≥ R: **±8200 UU** on each axis (so the R=8000 sphere isn't culled). GPU sims need explicit bounds.
3. Compile. Confirm **no 1M CPU-cap warning** in the Niagara log (A2 acceptance).

## M3 — Expose user-params + author `BP_CelestialSphere` to drive them (A3) — the Gate-A wiring

This is the core of repair #1. Two parts: (a) make the emitter spawn one particle per array entry at the array position; (b) a BP that loads the JSON, applies the Rx(+90°) transform, and sets the arrays.

**M3a — emitter consumes a positions array (in the Niagara editor):**
1. Add two **User-exposed parameters** on the system: `User.StarPositions` (type **Array of Vector** / `TArray<FVector>`) and `User.StarColors` (type **Array of LinearColor**).
2. Change the **spawn** so spawn count = array length (1,000), not the inherited burst. Simplest robust pattern: set SpawnBurst **Spawn Count = 1000** (one-shot, Loop Count Limit = 1) — OR drive it from `User.StarPositions.Length()`. (1,000 is fine to hardcode for this scaffold; note it as scaffold.)
3. In **Particle Spawn**, add a module that reads `User.StarPositions[ExecIndex]` → `Particles.Position`, and `User.StarColors[ExecIndex]` → `Particles.Color`. (Use `ExecutionIndex`/`Engine.Emitter.ExecIndex` to index the array per particle. The "Sample Static Mesh"-style index pattern, or a direct `Array Get` by exec index in a scratch module.)
4. Remove/zero any inherited `InitializeParticle` position randomization that fights the array (this is what currently makes the origin cloud).
5. Compile. Save the system.

**M3b — `BP_CelestialSphere` (new Actor Blueprint, or repair the existing if present):**
1. Create `Content/VFX/BP_CelestialSphere` (Actor) with a **NiagaraComponent** using `NS_CelestialSphere`.
2. On `BeginPlay` (or a `ConstructionScript`/Editor-callable for edit-time preview):
   - Load `Content/Data/CosmographSpike/cosmograph_sphere_001000stars_R8000.json` (read the file; or pre-import as a string/curve asset; simplest = a small C++/BP JSON read, or hardcode-via-DataTable if file-read in BP is painful).
   - Parse `star_positions_flat` into `TArray<FVector>` AND **apply the transform per star: `UE = (x, -z, y)`** (Rx(+90°), see math note § 3 — maps source +Y pole to UE +Z up). DO NOT skip this — without it the dense cap lands on the horizon.
   - Parse `star_colors_flat` (RGBA stride 4) into `TArray<FLinearColor>`.
   - `SetNiagaraVariableVectorArray(NiagaraComp, "StarPositions", positions)` and `SetNiagaraVariableLinearColorArray(NiagaraComp, "StarColors", colors)` (the `SetNiagaraArrayVector`/`SetNiagaraArrayColor` BP nodes from the NiagaraDataInterfaceArray plugin — enable **Niagara Data Interface Array** plugin if not already).
3. **Remove the old `CelestialSphere_Sky` NiagaraActor from the level** (the bare-system actor that made the origin cloud) and place **`BP_CelestialSphere` at world origin (0,0,0)** instead.
4. **Acceptance (A3 wiring):** stars now spawn as 1,000 particles on the R=8000 sphere (verify positions in the Niagara debugger or by piloting after cost-cut), NOT a cloud at origin.

> If a runtime JSON file-read in BP is friction: acceptable fallback = bake the 1,000 transformed positions + colors into a `DataTable` or a `CurveVector`/`UCurveLinearColor` asset offline and have `BP_CelestialSphere` read that asset. Either way the Rx(+90°) transform MUST be applied. Flag which path you took to david-h/sam.

## M4 — Figure-lighting repair: DIRECTION (A4) — VALUES are M7 (tune-on-screen)

Per dispatch § 3: establish a **standalone motivated night-key + ambient fill** on `SK_EarthAvatar`, independent of the sky, distinct from the spirit-glow. **DIRECTION now; do NOT lock final intensity/temperature/falloff/rim values here — those are M7 tuned-on-screen with you watching.**

1. Select **`RigA_Moonlight`** (directional). **Re-aim it** so its lit face hits the avatar's **camera-facing** surfaces from `Cam_GroundLookUp` (camera is at ~`(0,-300,170)` looking up/back toward the figure at origin). A directional light lights the side its `-X` (forward) points at. Aim DIRECTION: a **high, slightly-behind-camera key** — e.g. pitch it down toward the figure from the camera's upper-front quadrant (a believable "moon over the shoulder" angle), NOT pointing its lit face away. Target: the figure's front/camera-side is lit, not back-lit into silhouette. (This is THE likely root-cause of the black-in-Lit: a directional whose lit side faces away.)
2. Select **`RigA_Skylight`**. With an empty/black sky it captures ~0 → no ambient fill. Give it a real source independent of the celestial sphere:
   - Set **Lower Hemisphere Is Solid Color** ON with a dim cool night color (ambient floor), OR assign a **specified night-sky cubemap** to its source. This carries fill so the figure's shadow side isn't pure black, WITHOUT depending on `ns.celestialsphere` emissive.
3. **Motivated-not-spotlight discipline (constraint 1):** the key is the directional moonlight (soft, color-matched to night) + the skylight ambient fill — NOT a hard point spotlight clamped on the figure. The figure should read as "the world's night light finding an ordinary person on a hill."
4. **Distinct-from-spirit-glow (constraint 2):** keep `RigA_Moonlight` temperature/quality readably SEPARATE from `RigB_SpiritGlowOnly`. The moonlight = cool, mundane, world-light pole. The spirit-glow = the supernatural pole. Do not let them converge in color/quality.
5. **No celestial-sphere emissive dependency (A4):** the figure must light from `RigA_Moonlight` + `RigA_Skylight` alone. Test by toggling the celestial sphere OFF — the figure stays lit.

## M5 — Confirm Rig A/B toggle + distinct poles (A5)

1. Confirm the toggle still works: **Rig A** = `RigA_Moonlight` + `RigA_Skylight` visible, `RigB_SpiritGlowOnly` hidden; **Rig B** = invert. (Tags `RigA`/`RigB` from the prior spike; eye-icon or a level-BP/sequencer toggle.)
2. Confirm the two are authored as **distinct poles** (avatar-key cool/mundane vs spirit-glow supernatural). A5 closes the LIGHTING-RIG question only — NOT the full aesthetic mundane-vs-supernatural read (that waits on the real ambiguous-spirit visual; FigureStandIn is a placeholder — dispatch § 6).

## M6 — Apply nebula cost-cut, then RE-ENABLE volumetrics (A7 apply)

In console (these are the permanent-intent values; if you want them to stick, also set in the nebula material/Project Settings, not just CVar):
```
r.HeterogeneousVolumes.MaxStepCount 32
r.HeterogeneousVolumes.DownsampleFactor 4
r.HeterogeneousVolumes.Shadows.Resolution 0
```
Then RE-ENABLE the volumetrics you disarmed in pre-flight (the cost-cut should make them affordable):
```
r.HeterogeneousVolumes 1
r.VolumetricFog 1
```

## M7 — Pilot, tune figure-light VALUES on-screen, then MEASURE + capture (Tier-B B1–B5)

1. NOW pilot `Cam_GroundLookUp`. It should be stable (cost-cut applied). If GPU time climbs toward a hang, drop `MaxStepCount` 32→16 / `DownsampleFactor` 4→8 (math note § 6 lever order) BEFORE disabling the nebula.
2. **`stat gpu` / `stat unit` / `stat fps`** — confirm against the threshold (math note § 6): **stable ≥ 30 s, GPU frame ≤ 16.6 ms, flat (not climbing)**. This is the A7/B2/B5 PASS target. Record the numbers.
3. **B1:** confirm stars render on the R=8000 sphere (cluster caps overhead, none on horizon, none at origin). If a dense cap is on the HORIZON → the Rx(+90°) transform (M3b) was missed.
4. **B3/M7-values:** with you watching, tune `RigA_Moonlight` **intensity / temperature / falloff** + `RigA_Skylight` fill so `SK_EarthAvatar` reads clearly in **Lit** from `Cam_GroundLookUp` as **worldlight-on-an-ordinary-person, NOT a product-shot spotlight**. This is the values-now step that DIRECTION (M4) deferred.
5. **B4:** confirm Rig A key reads **distinct in temperature/quality from Rig B spirit-glow**.
6. **Captures:** `HighResShot 2` for **S1** (sky) and **S5 Rig A** + **S5 Rig B** (toggle per M5). Shots land in `Saved/Screenshots/`.
7. **Do NOT save the level** if you only want to bank captures + CVars are session-only. **DO save** if you want the M2/M3 Niagara+BP rework + M4 light-direction to persist (the rework SHOULD persist; the session-only CVars in M6 should be promoted to material/Project-Settings if you want them durable). Decide per intent and note it.

---

## What closing this list achieves

- M1 → finalizes the exact A1 Spawn Count number (mantis documented the structural root-cause; you read the literal value).
- M2/M3 → A2 + A3 (GPU sim, no cap; stars on R=8000 sphere via bound JSON + Rx(+90°); origin cloud gone).
- M4/M5 → A4 + A5 (figure lights standalone under Rig A; rigs are distinct poles).
- M6 → A7 apply (nebula cheap enough to leave ON).
- M7 → all of Tier-B (B1–B5): render-confirmed sky, no-crash nebula at the `stat gpu` threshold, figure reads in Lit (values tuned on-screen), Rig A/B distinct, perf captured.
