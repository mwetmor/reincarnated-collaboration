# Live Plan — P0.1 Desktop Render Session (IN PROGRESS, resume marker)

**STATUS:** ACTIVE — Matt at PC console; logging off to correct Windows profile (`mhwet`) then resuming
**Date:** 2026-06-12
**Author:** david-h (PC-side orchestrator)
**Trigger doc:** `z:\agent-prompts\2026-06-11-p0-1-shader-ddc-warm-directions.md` (gandalf, revised) + my wave-close `2026-06-11-manifestation-phase1-spike-wave-close.md` § 4 forward register
**Matt decision (this session):** FULL CLOSE — pull mantis in live to do Gate A so S1 closes in one sitting (vs capture-only-then-second-sitting). Honors "one sitting beats three."

## The session sequence (resume here)

1. **Launch + warm (Matt):** double-click `C:\dev\reincarnated-unreal\Reincarnated\Reincarnated.uproject` on the GPU-attached `mhwet` console; drain `Compiling Shaders (N)` to zero; open `LV_ManifestationKnoll`. PC stays awake (sleep mid-compile = restart).
2. **S5 captures FIRST (Matt, manual — no bridge):** pilot `Cam_GroundLookUp`, `HighResShot 2` → Rig A as-is; then hide `RigA_Moonlight` + `RigA_Skylight`, un-hide `RigB_SpiritGlowOnly`, reshoot → Rig B. Check manual exposure lock (0.03 / bias −2.0) reads right; nudge `AutoExposureBias` if needed. Figure-readability A vs B on Quinn placeholder. Bank before mantis touches the editor (no simultaneous human+bridge driving).
3. **HANDOFF TRIGGER → david-h fires mantis (Pattern A subagent) for Gate A.** Fires when Matt confirms **"editor's up, bridge bound"** (UE_MCP_Bridge on `ws://127.0.0.1:9877`, binds at PostEngineInit). Gate A = expose `StarPositions`/`StarColors` array user-params on emitter + author `BP_CelestialSphere` loading `cosmograph_sphere_001000stars_R8000.json` + bind + recompile → sky renders real R=8,000 sphere, not the ±67 spike cloud. **RISK:** bridge-into-windowed-editor for Niagara stack edits is UNVALIDATED; fallback = mantis hands Matt manual BP steps, or defer S1-sphere (still leave with S5 + warm DDC).
4. **S1 captures (Matt, after mantis confirms bound):** twirl by rotating `CelestialSphere_Sky` actor (never camera); TSR config motion-blur-off / History SP 100 / ghost-rejection 2; `stat fps` + `stat gpu` + `stat unit`; horizon-sprite ghosting under rotation; full-stack FPS vs 60; sprite-size/depth read at R=8,000. mantis can regen at higher R (~1s) + rebind if stars read near.
5. **#5 mythic-weight judgment (Matt):** AFTER exposure tuning (radagast fairness criterion).
6. **Close:** screenshots → `Saved/Screenshots/`; david-h routes to radagast (design-fit) + sam (Gate-2); cross-host "P0.1 done + captures delivered" to Mac-KR; unblocks S2→S3→S4.

## Environment note (load-bearing)
- Render evidence requires GPU-attached interactive desktop as `mhwet` (DXGI gate, recurring — supersedes cold-DDC framing). SSH/WSL windowed launch crashes at viewport creation.
- Git SSH key + DDC + repos (junction `C:\Users\mhwet\Games` → `C:\dev`) are `mhwet`-profile-scoped — wrong-profile login was the blocker this session.

**Resume:** a fresh `claude --agent david-h` reads this note + the trigger doc; hold at step-3 trigger until Matt confirms editor up + bridge bound.
