# Wave-1 Close — mantis Tier-A banked; Tier-B fire-ready for Matt's console

**STATUS:** WAVE-1 CLOSE (split wave per Matt 2026-06-13 "split the wave into two"). Read by next-david-h + Matt + mantis.
**Date:** 2026-06-13
**Author:** david-h (PC-side orchestrator, mhwet/WSL SSH session)
**Predecessor:** `2026-06-13-wave-close-memo-dispatch-ratified.md` (ratification close) → this is the execution split that followed.
**Dispatch:** `agentic_orchestration/dispatches/2026-06-13-mantis-celestial-sphere-rework-and-figure-lighting-rig-repair.md` (ACTIVE).

---

## The split (Matt's call)

Matt split the wave into two so the headless Tier-A work banks now and the console-gated Tier-B happens on his time:
- **Wave 1 (this session, headless):** mantis Tier-A → sam Gate-2 → commit + push. DONE.
- **Wave 2 (Matt's time, console):** Tier-B render-evidence + manual-BP-step list + final key-light values, at the PC console / RDP behind the DXGI gate.

## Wave-1 outcome

**mantis Tier-A — commit `1828499`, tag `mantis/v1.0-celestial-sphere-rework-tierA-1`.**
- **A1 CLOSED** — math/transform note + 1,005,000 root-cause (genuine structural diagnosis; Discipline #1 honored).
- **A6 CLOSED** — D7 PASS by construction.
- **A7 CLOSED (documentable half)** — `stat gpu` budget threshold documented as the Tier-B pass target (stable ≥30 s, GPU frame ≤16.6 ms/≥60 fps, flat trend, volumetric line-items bounded); nebula cost-cut values specified.
- **A2/A3/A4/A5 → manual-BP-step list** (no headless bridge for Niagara array params/sim-target; A4/A5 success is DXGI-render-gated). Mantis STOPPED rather than open a windowed editor over SSH — correct WARN-1 fallback. No UE session opened; pristine level preserved.

**sam Gate-2 — PASS-WITH-WARN (1 WARN, 2 INFO, 0 BLOCK), Tier-A.** Finding `agentic_orchestration/qa/findings/2026-06-13-mantis-celestial-sphere-rework-tierA-gate-2.md` (commit `9af4360`). Cross-seam flag STANDS DOWN (UE-side wiring gap, not an engine-JSON defect; star-lord export verified clean). Pristine-level discipline HELD (commit is exactly the two `.md` notes). The one WARN: M4 figure-light DIRECTION is qualitative vs A1–A3 quantitative — non-blocking (§ 3 constraint 3 already defers VALUES to Tier-B); mantis folds a concrete M4 starting rotation on a future pass.

## Two key findings worth surfacing

1. **The 1,005,000 root-cause:** `NS_CelestialSphere` is a `duplicate_asset` of `NS_CosmographPointCloud` whose `StarPositions` was NEVER bound — it runs inherited CPUSim point-cloud spawn logic (SpawnBurst × InfiniteLoop accumulation) fully decoupled from the 1,000-star JSON, clustered at the actor origin. Fix = bind the JSON + GPU sim; count→1,000 is a *consequence of binding real data*, not a knob-turn.
2. **NEW coordinate finding (was NOT in the prior Gate-A TODO):** the generator builds **+Y-up**, UE is **Z-up**. Verbatim consumption would land the constellations on the **horizon, not overhead**. Required transform: **Rx(+90°) → `UE=(x,-z,y)`** before `SetNiagaraArrayVector` (|r|=8000 preserved; RGBA pass-through). Captured in the math note + manual step M3b with a "DO NOT skip" guard.

## What Matt does in Wave 2 (console)

Execute the ordered manual-BP-step list:
`agentic_orchestration/mantis/notes/2026-06-13-celestial-sphere-MANUAL-BP-STEPS-for-matt-console.md` (M1–M7).
- M1 read literal Spawn Count (finalizes A1 arithmetic) · M2 CPU→GPU sim + fixed bounds · M3 expose `StarPositions`/`StarColors` + author `BP_CelestialSphere` (load JSON, apply Rx(+90°), set arrays) · M4 figure-light DIRECTION re-aim · M5 Rig A/B toggle + distinct-poles confirm · M6 apply nebula cost-cut + re-enable volumetrics · M7 pilot, tune light VALUES on-screen, measure `stat gpu`, capture S1/S5 (Tier-B B1–B5).

Sam Gate-2 confirms the list is precise/ordered/complete enough to execute without re-deriving anything.

## Git state

Wave-1 commits pushed from this mhwet/WSL session: mantis `1828499` (+ tag), sam `9af4360`, this memo. The `reincarnated-unreal` UE tree is NOT git-tracked on this host — the tracked deliverables are the two `.md` notes (math/transform + manual-BP-steps); the actual `.uasset`/`.umap` edits land in Wave 2 at the console and persist on disk only.

## Forward register (unchanged)

- Wave 2: Matt console session executes M1–M7 (Tier-B). Re-shoots S1 + S5.
- Q5 ambiguous-spirit visual: radagast↔Mac-gandalf cross-cutting consult when WS2 art-direction triggers (gates the *aesthetic* B4 contrast read only; A5/B4 close the LIGHTING-RIG question).

**End Wave-1 close.**
