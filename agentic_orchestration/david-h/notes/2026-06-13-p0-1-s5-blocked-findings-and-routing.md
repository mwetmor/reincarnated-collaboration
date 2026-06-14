# P0.1 Render Session (resumed 2026-06-13) — S5 BLOCKED on rig rework; findings + routing

**STATUS:** Matt's console portion CLOSED. S5 captures NOT banked — figure-lighting rig non-functional once the celestial sphere is removed. S1 already deferred (prior note). Three findings below route to mantis (repair) + radagast (design-fit) + sam (Gate-2). Scene left UNSAVED (deletion/toggles/CVars revert on reload — mantis inherits pristine scene).
**Date:** 2026-06-13
**Author:** david-h (PC-side orchestrator)
**Profile:** `TheSa` (render profile). Predecessors: `2026-06-13-p0-1-resume-after-gpu-crash.md` + `2026-06-12-p0-1-render-session-live-plan.md` + wave-close `2026-06-11-manifestation-phase1-spike-wave-close.md`.

---

## What we set out to do
Bank **S5** (figure-lighting Rig A vs Rig B readability on the avatar) safely off the GPU-killing sky path, per the resume note. S5 was supposed to be the safe, human-manual capture; S1 (the sky) was already deferred to a mantis cost-cut.

## What actually happened (chronological, all empirical)
1. **Sky disarm held.** `r.HeterogeneousVolumes 0` + `r.VolumetricFog 0` + `sg.EffectsQuality 2` verified via CVar-echo (`= "0"`, LastSetBy Console). No GPU crash on piloting `Cam_GroundLookUp` — the prior crash cause (volumetric nebula raymarch) is confirmed and CVar-suppressible.
2. **`Cam_GroundLookUp` rendered empty/black.** Auto-Exposure Histogram on the camera's Post Process did NOT brighten it → ruled out exposure. Unlit showed geometry → ruled out content/material/framing as the *primary* issue.
3. **FINDING 1 — celestial sphere is a GPU landmine at origin.** Niagara warning surfaced live: `ns.celestialsphere:minimal` attempted **1,005,000 CPU particles** vs the 1,000,000 cap. The particles are NOT on the R=8,000 sphere overhead — they are a **dense cloud clustered at the origin, directly under the avatar's feet** (the "±67 spike cloud" the live plan flagged). Looking *down* at it nearly crashed the GPU (overdraw); navigating *past* it froze the editor. This is one root cause behind BOTH the S1 sky failure and the S5 obstruction.
4. **Matt deleted the celestial sphere** (session-only; NOT saved) → editor navigable again.
5. **FINDING 2 — the spirit form is a small particle ball.** When framed, the "figure"/spirit reads as a small particle blob. May be on-design (canon: *intentionally ambiguous* spirit form) — flagged to radagast to confirm intended-read vs missing-mesh. A blob is uninformative for a lighting-readability test regardless.
6. **`SK_EarthAvatar` is the readable humanoid figure** and frames well in `Cam_GroundLookUp`. It looked good in **Unlit**.
7. **FINDING 3 — figure-lighting rig is non-functional without the celestial sphere.** In **Lit**, `SK_EarthAvatar` renders as a **black shadow/silhouette**. Diagnostics that did NOT fix it:
   - Exposure ruled out (Unlit-visible, Lit-black).
   - `RigA_Moonlight` eye-icon confirmed ON (not hidden).
   - `RigA_Moonlight` intensity bumped ~10× — still black.
   - `SK_EarthAvatar` Lighting Channels confirmed **Channel 0** (matches lights).
   - Hypothesis (for mantis): the deleted 1M-star emissive cloud at the avatar's feet was the avatar's de-facto fill light; `RigA_Skylight` now captures an empty black sky (~0 contribution); `RigA_Moonlight` rotation/aim likely points its lit side away from `Cam_GroundLookUp`, OR baked lighting needs a rebuild. **Past quick live-tuning → mantis headless repair.**

## Net
- **S1 (sky):** deferred (unchanged) — mantis cost-cut + reposition.
- **S5 (figure lighting):** NOW BLOCKED on the same celestial-sphere rework + a figure-lighting-rig repair. Re-shoots cleanly after mantis's pass. Zero captures banked this session — by design, not forced through the hazard.

## Actor name register (for routing)
- Earth avatar (S5 subject): **`SK_EarthAvatar`**
- Celestial sphere Niagara: `ns.celestialsphere:minimal` (system); Outliner actor name TBD (deleted live; recover from level on reload) — likely `NS_/BP_CelestialSphere`.
- Spirit particle ball: **TBD** (asked Matt; fill on confirm).
- Lights: `RigA_Moonlight`, `RigA_Skylight`, `RigB_SpiritGlowOnly`.

## Routing (david-h, next)
1. **mantis dispatch (Pattern B, dedicated session):**
   - (a) **S1 cost-cut + reposition:** move `ns.celestialsphere` to **GPU sim** (1M CPU cap N/A on GPU) and/or cut star count; reposition from origin ±67 cloud to the **R=8,000 sphere** via Gate-A (expose `StarPositions`/`StarColors` user-params + `BP_CelestialSphere` loading `cosmograph_sphere_001000stars_R8000.json`).
   - (b) **figure-lighting-rig repair:** make `SK_EarthAvatar` light correctly under Rig A WITHOUT depending on the star-cloud (check `RigA_Moonlight` rotation/aim; `RigA_Skylight` source with empty sky; lighting rebuild) so S5 re-shoots.
   - Route DRAFT through **sam Gate-1** + **radagast** design-fit before publish (Pattern E PC trio).
2. **radagast (design-fit):** is the particle-ball spirit the intended ambiguous-spirit read? Is figure-lighting-by-celestial-sphere acceptable, or should the figure carry its own key light independent of the sky?
3. **sam (Gate-2):** on mantis's eventual commit.
4. **Cross-host note to Mac-KR:** P0.1 produced findings not captures; S5+S1 both gated on celestial-sphere rework; manifestation Phase-1 spike forward register updated.

## Git / push
Authored on `TheSa` (local commits OK, no SSH). **Wave-close `git push` defers to an `mhwet` SSH/WSL session** — GitHub SSH key is `mhwet`-scoped; `C:\dev\` shared on disk so `TheSa` commits are visible to the `mhwet` push session. Do NOT mutate `TheSa` `core.sshCommand` (WSL depends on it).

## Positive signal (not a finding, worth keeping)
`SK_EarthAvatar` looks great in Unlit — the asset itself is solid. The problem is the *rig*, not the avatar.
