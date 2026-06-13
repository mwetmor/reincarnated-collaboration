# P0.1 Render Session — RESUME HERE (after GPU crash)

**STATUS:** PAUSED mid-session — Matt signed off after a GPU crash on the sky render. NOTHING LOST (no captures fired, level never edited/saved). Recovery is known and below.
**Date:** 2026-06-13
**Author:** david-h (PC-side orchestrator)
**Full context:** this session's live plan `2026-06-12-p0-1-render-session-live-plan.md` (+ its CORRECTION block) and wave-close `2026-06-11-manifestation-phase1-spike-wave-close.md`.

---

## Where we actually are

- On the **`TheSa`** profile (the ONLY profile with UE installed — this is the render profile; do NOT switch to `mhwet`). DDC is warm here (no shader-compile counter on launch).
- `LV_ManifestationKnoll` opens fine; 12 actors present in the Outliner; scene intact.
- **GPU crashed** (`D3D Device Removed`, NVIDIA Aftermath, fault in `fragment_02` pixel shader) the moment the ground-look-up camera filled the screen with the volumetric sky.

## Root cause (confirmed from the log)

The nebula uses UE 5.7 **Heterogeneous Volumes** with brutal settings — `r.HeterogeneousVolumes.MaxStepCount:256`, `Shadows.Resolution:512`, plus `VolumetricFog` and Lumen translucency volumes on. Full-screen volumetric raymarch hung the GPU (an RTX **4060 Ti** — capable; the scene is the problem, not the hardware). The stutter before the crash was the warning.

## Recovery + S5 captures (do this next session)

1. Relaunch UE; open `LV_ManifestationKnoll`. **Do NOT pilot the look-up camera yet** — stay on free-cam (sky distant = safe).
2. Open the console (`` ` `` or `~`) and run, one at a time (session-only, non-destructive):
   ```
   r.HeterogeneousVolumes 0
   r.VolumetricFog 0
   ```
   Belt-and-suspenders: Settings toolbar → Engine Scalability Settings → **Medium**.
3. Now pilot `Cam_GroundLookUp` (Outliner → select → right-click → Pilot). Should be stable now.
4. Confirm exposure (manual `0.03`, `AutoExposureBias` −2.0; nudge if mud).
5. `HighResShot 2` → **Rig A**.
6. Hide `RigA_Moonlight` + `RigA_Skylight`; un-hide `RigB_SpiritGlowOnly`.
7. `HighResShot 2` → **Rig B**. Shots land in `Saved/Screenshots/`.
8. **Do NOT save the level** — visibility toggles are session-only; keep the scene pristine.

→ This banks S5 (figure-lighting Rig A/B readability) safely, off the GPU-killing path.

## S1 (the sky) — DEFERRED off Matt's GPU

The celestial-sphere/nebula render is now a confirmed **feasibility finding**, not a quick capture. Plan: **mantis reduces cost headlessly** (`MaxStepCount` 256→~32, raise `DownsampleFactor`, kill volume shadows, cap Niagara star overdraw), commits, THEN one controlled S1 render — rather than repeated GPU crashes. Original S1 Gate-A (expose `StarPositions`/`StarColors` user-params + author `BP_CelestialSphere` loading `cosmograph_sphere_001000stars_R8000.json`) still applies AFTER the cost cut.

## david-h actions at next session start

1. Route the GPU-crash finding to **radagast** (design-fit), **sam** (Gate-2), **mantis** (cost-reduction dispatch). Crash dump: `Saved/Logs/D3D12.0.2026.06.12-23.59.59.nv-gpudmp`; log: `Saved/Logs/Reincarnated.log`.
2. Hold at the S5 capture step until Matt confirms he's piloting `Cam_GroundLookUp` post-CVar.
3. Wave-close push must run from an **`mhwet`** SSH/WSL context (github SSH key is `mhwet`-scoped; `TheSa` git push fails). `C:\dev\` is shared on disk, so `TheSa` commits are visible to the `mhwet` push session.

## Git note (load-bearing)

`TheSa` repo `core.sshCommand` is set to a WSL path (`/mnt/c/...`) — valid in WSL, broken in native/Git-Bash on `TheSa`; that's why pull/push hang here. Do NOT mutate it (WSL sessions depend on it). Override per-command or push from `mhwet`.
