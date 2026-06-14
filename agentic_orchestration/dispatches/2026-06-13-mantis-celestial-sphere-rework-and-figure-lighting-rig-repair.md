# Mantis Dispatch — Celestial-Sphere Rework + Figure-Lighting-Rig Repair (unblocks S1 + S5)

**STATUS:** ACTIVE — PC-trio ratified 2026-06-13 (Pattern E). sam Gate-1 = PASS-WITH-WARN (4 WARN, 0 BLOCK; finding `agentic_orchestration/qa/findings/2026-06-13-mantis-celestial-sphere-rework-gate-1.md`); radagast design-fit = PASS-WITH-WARN (1 amendment, 0 BLOCK; verdict `agentic_orchestration/radagast/notes/2026-06-13-celestial-sphere-rework-design-fit.md`). All WARNs folded below (see § 9 fold-record). FIRE-READY: mantis executes in a dedicated session with Matt at the PC console for render-evidence (DXGI gate; see § 4 tier-A/tier-B split).
**Date:** 2026-06-13
**Author:** david-h (PC-side orchestrator)
**Authority:** david-h PC-seam dispatch authority; empirical findings from 2026-06-13 P0.1 resumed render session (Matt at `TheSa` console + david-h orchestrating).
**Audience:** mantis (executor); sam (Gate-1 pre-fire + Gate-2 post-output); radagast (design-fit).
**Companion docs (read first):**
- `agentic_orchestration/david-h/notes/2026-06-13-p0-1-s5-blocked-findings-and-routing.md` (the three empirical findings this dispatch acts on)
- `agentic_orchestration/david-h/notes/2026-06-13-p0-1-resume-after-gpu-crash.md` (GPU crash root cause + CVar disarm)
- `agentic_orchestration/david-h/notes/2026-06-12-p0-1-render-session-live-plan.md` (Gate-A definition; ±67 spike cloud vs R=8,000 sphere)
- `canonical/story/2026-06-07-earth-avatar-cosmograph-creation-moment-architecture.md` § 2.6 (spherical-shell celestial-sphere geometry lock) + § 12 (sky surface)
- `canonical/story/2026-06-11-avatar-projection-and-hall-of-heroes-framing.md` § 4 (manifestation build consequences)

---

## 0. TL;DR

**Mission:** Two coupled repairs on `LV_ManifestationKnoll`, both empirically diagnosed live this session, both headless (no Matt GPU exposure until the controlled final renders):

1. **Celestial-sphere cost-cut + reposition (Gate-A).** The star field is currently a **1,005,000-particle CPU Niagara cloud clustered at the origin** (the "±67 spike cloud") — it exceeds UE's 1M CPU cap, sits as a GPU landmine directly under the figure, and is NOT on the R=8,000 sphere overhead. Move it to GPU sim + reposition to the real sphere + tame the volumetric nebula.
2. **Figure-lighting-rig repair.** `SK_EarthAvatar` renders correctly in Unlit but is a **black silhouette in Lit** — even with `RigA_Moonlight` visible, on Lighting Channel 0, at 10× intensity. The rig was leaning on the now-removed star-cloud for fill. Make the figure light under Rig A independent of the sky.

**Why coupled:** both gate the manifestation Phase-1 spike captures — **S1** (the sky render) and **S5** (figure-lighting Rig A/B readability). Neither can be banked until this lands. S5 was attempted live this session and BLOCKED on repair #2; S1 was already deferred to repair #1.

**Estimated wall-clock:** 1–2 sessions (mantis convention). Repair #1 is the larger piece (Niagara GPU-sim migration + JSON-driven sphere authoring per Gate-A); repair #2 may be small (a light rotation/source fix) or a lighting rebuild.

---

## 1. Math-before-code (Discipline #1) — required before any reposition

The reposition is geometric and must be specified as math before implementation:
- Stars distribute on a sphere of radius **R = 8,000** (UE units), camera/avatar at origin looking up at the **interior** surface (§ 2.6 spherical-shell lock).
- Source data: `cosmograph_sphere_001000stars_R8000.json` (1,000 stars at R=8,000). Confirm the JSON's coordinate convention (cartesian vs spherical; handedness; up-axis) maps to UE's Z-up left-handed space — author the transform note before binding.
- **Particle-count sanity:** the live warning was 1,005,000 — that is ~1,000× the JSON's 1,000 stars. Diagnose the multiplier (per-star sub-emission? a spawn-rate loop? a stale high-count default?). Document the source of the 1,005,000 before cutting — silent count reduction without root-cause is a Discipline #1 violation.

File the math/transform note at `reincarnated-unreal/.../docs/` (or AGENT_STATE companion) before the BP edit.

## 2. Repair #1 — celestial-sphere cost-cut + reposition (Gate-A)

| Sub-step | Action | Acceptance |
|---|---|---|
| 1.1 | Root-cause the 1,005,000-particle count (see § 1) | count source documented |
| 1.2 | Migrate `ns.celestialsphere:minimal` emitter from **CPU sim → GPU sim** (1M cap is CPU-only) | emitter runs GPU; no cap warning |
| 1.3 | Expose `StarPositions` / `StarColors` array user-params on the emitter | params bound + drivable |
| 1.4 | Author/repair `BP_CelestialSphere` to load `cosmograph_sphere_001000stars_R8000.json` → drive the user-params | stars render on R=8,000 sphere, NOT the origin ±67 cloud |
| 1.5 | Tame the volumetric nebula (the GPU-crash source): `r.HeterogeneousVolumes.MaxStepCount` 256→~32, raise `DownsampleFactor`, **kill volume shadows** (`Shadows.Resolution` off/low), trim `VolumetricFog` | look-up view renders without `D3D Device Removed` |
| 1.6 | Cap Niagara star overdraw (sprite size/depth, GPU bounds) | no overdraw spikes; `stat gpu` stable |

**Note:** this session's CVar disarm (`r.HeterogeneousVolumes 0` / `r.VolumetricFog 0`) was a session-only band-aid. Repair #1.5 makes the nebula **cheap enough to leave ON** so S1 renders the intended sky, not a black void.

**Execution-environment fallback (sam Gate-1 WARN-1 — load-bearing).** Sub-steps 1.2 (CPU→GPU sim) and 1.3 (expose user-params) are Niagara-stack edits, and bridge-into-windowed-editor for that edit class is UNVALIDATED over SSH (per `2026-06-12-...-live-plan.md`). **NEVER open a windowed editor over SSH — it crashes at viewport creation (DXGI; no GPU-attached desktop).** If the headless/bridge path cannot perform a given Niagara edit, mantis STOPS that sub-step and hands Matt a precise manual-BP-step list to execute at the PC console; mantis does not force a windowed editor. Headless `-nullrhi` authoring is the default; the console (Matt present) is the fallback execution surface, not SSH-windowed-editor.

## 3. Repair #2 — figure-lighting-rig repair

Diagnostics already EXCLUDED live (do not re-chase): exposure (Unlit-visible/Lit-black), light hidden (`RigA_Moonlight` eye-icon ON), lighting channel mismatch (`SK_EarthAvatar` on Channel 0), low intensity (10× still black).

**Design constraint on the repair (radagast design-fit, folding the Mac-gandalf key-light ruling 2026-06-13):** The Earth avatar carries its OWN motivated key light, independent of the sky — its legibility is invariant to the knoll's lighting flux (genre-settled: Diablo char-select, Destiny Tower, Soulslike hubs). Three constraints on HOW:
1. **Motivated + grounded, not a product-shot spotlight.** Color-matched to the night scene, soft, rim-biased, anchored to the avatar — natural light finding the figure. The fix is not "crank a hard directional"; it is "give the figure a believable night-key + ambient fill that reads as the world lighting an ordinary person on a hill" (§ 4.2 knoll-reads-as-intentional-ordinary-place).
2. **DISTINCT from the diegetic spirit-glow.** The avatar key = the mundane/grounded pole (the human not-yet-become); `RigB_SpiritGlowOnly` = the supernatural pole (the becoming). The contrast IS the mythic content and must NOT blend — keep the avatar key's temperature/quality readably separate from the spirit-glow's. When both are present, a viewer must be able to tell "this is worldlight on a person" from "this is the spirit's own light."
3. **Direction-now, values-later.** This dispatch establishes the rig DIRECTION (standalone, motivated, distinct) headless. The VALUES — intensity / temperature / falloff / rim weight — are TUNED in the render-console session downstream of the exposure lock, with Matt at the console (DXGI gate + acceptance #5 mythic-weight judgment). Do NOT attempt to land final values headless.

| Sub-step | Action |
|---|---|
| 2.1 | Inspect `RigA_Moonlight` **rotation/aim** — a directional light's lit side follows rotation; if it points its lit face away from `Cam_GroundLookUp`, the avatar's camera-facing side stays in shadow regardless of intensity. Re-aim so the figure's camera-facing surfaces are lit. |
| 2.2 | Inspect `RigA_Skylight` source/intensity — with an empty sky it captures ~0; set a real source (specified cubemap or `Lower Hemisphere Is Solid Color`) so it carries ambient fill independent of the celestial sphere. |
| 2.3 | If still black: force a **lighting rebuild** (Build Lighting Only) in case stationary/static lighting is stale; confirm `SK_EarthAvatar` mobility + the lights' mobility are compatible. |
| 2.4 | Confirm the figure lights WITHOUT any dependency on `ns.celestialsphere` emissive (the rig must stand alone). |

**Acceptance #2:** `SK_EarthAvatar` reads clearly in **Lit** under Rig A from `Cam_GroundLookUp`, with the celestial sphere present-and-repositioned (not the old origin cloud).

## 4. Acceptance criteria (two-tier per sam Gate-1 WARN-3/WARN-4)

**Tier A — mantis-headless (self-closeable; gates the commit + Sam Gate-2):**

| # | Criterion |
|---|---|
| A1 | 1,005,000-particle count root-caused + documented (§ 1) |
| A2 | Celestial-sphere emitter on GPU sim; no CPU-cap warning |
| A3 | `BP_CelestialSphere` authored/repaired to load `cosmograph_sphere_001000stars_R8000.json` → drive `StarPositions`/`StarColors` user-params on the R=8,000 sphere (Gate-A wiring complete; origin ±67 cloud removed) |
| A4 | Figure-lighting rig re-aimed/repaired so `SK_EarthAvatar` is mechanically no-longer-black in Lit under Rig A, with NO `ns.celestialsphere` emissive dependency, as a **standalone motivated night-key + ambient fill** (rig DIRECTION per § 3 constraints 1–2; final VALUES deferred to tier B) |
| A5 | Rig A/B toggle (`RigA_Moonlight`+`RigA_Skylight` vs `RigB_SpiritGlowOnly`) is wired and switchable; the two rigs are authored as distinct poles (avatar-key vs spirit-glow per § 3 constraint 2) |
| A6 | No raw LLM player-facing content (D7); stars/runes hand/JSON-authored |
| A7 | Nebula cost-cut applied (§ 2 repair #1.5); a **`stat gpu` budget threshold** documented as the pass target for tier B (stable frame ≥ a stated N seconds, no rising trend toward `D3D Device Removed`) — sam WARN-2 |

**Tier B — render-confirmed (Matt at PC console / RDP; DXGI gate; does NOT block the commit's Gate-2 or wave-close push — sam WARN-4):**

| # | Criterion |
|---|---|
| B1 | Stars visibly render on the R=8,000 sphere in a console render (not headless wiring alone) |
| B2 | Volumetric nebula renders the look-up view WITHOUT GPU crash at default (no CVar band-aid), meeting the A7 `stat gpu` budget threshold |
| B3 | `SK_EarthAvatar` reads in Lit under Rig A from `Cam_GroundLookUp` as a standalone motivated night-key + ambient fill, reading as **worldlight-on-an-ordinary-person — NOT a product-shot spotlight**; final intensity/temperature/falloff values console-tuned (§ 3 constraint 3) — radagast amended #5 |
| B4 | The Rig A avatar-key reads **DISTINCT in temperature/quality from the Rig B spirit-glow** (mundane pole vs supernatural pole; the contrast must not blend), producing a judgeable S5 lighting difference. NOTE: this closes the LIGHTING-RIG question only; the full aesthetic mundane-vs-supernatural contrast read carries forward to when the real ambiguous-spirit visual exists (see § 6 forward item) — radagast amended #6 |
| B5 | `stat gpu` / `stat fps` / `stat unit` captured at console; performance documented for the repositioned sphere + tamed nebula |

## 5. Discipline citations

- **Discipline #1 (math-before-code)** — geometric reposition + particle-count root-cause specified before BP edits (§ 1).
- **R48.4 (host-RAM-aware concurrency)** — GPU-sim migration + Niagara bounds must respect the RTX 4060 Ti budget; no 1M-particle CPU spikes.
- **D7 (AI-tell line)** — star/rune content hand/JSON-authored; no runtime LLM.
- **Substrate-led-at-rendering-layer** — the R=8,000 sphere honors § 2.6 spherical-shell geometry; the sky IS the cosmograph, not a backdrop.
- **Smoke-gate / empirical-evidence** — repairs validated by a single controlled render each (S1 + S5), not repeated GPU crashes.

## 6. Out of scope

- ❌ `FigureStandIn` spirit-form mesh — it is an explicit **placeholder stand-in** (particle ball); the real ambiguous-spirit visual is a radagast design question, NOT this dispatch.
- ❌ Cluster-rune / constellation overlay rendering (WS2 commission `2026-06-10-david-h-ws2-niagara-cluster-rune-rendering-commission.md`).
- ❌ Materialization cinematic (WS3).
- ❌ Any change to `SK_EarthAvatar` the asset itself — it renders great in Unlit; the fault is the rig.
- ❌ Saving session-only CVar/visibility state into the level.

**Forward design item (radagast design-fit (c); NOT this dispatch's scope):** the ambiguous-spirit visual (§ 4.5 Q5 of the creation-moment architecture — `FigureStandIn` is an explicit placeholder particle ball) needs scoping before S5's *aesthetic* mundane-vs-supernatural contrast judgment (B4) can fully close. This is cross-cutting creation-moment refinement (Mac-gandalf primary per radagast drift-discipline). David-H logs it as a forward-register item routed to a **radagast↔Mac-gandalf consult**, triggered by WS2 prototype / art-direction iteration — not now, not here. Mantis must NOT over-read a clean Rig A/B light-toggle on the placeholder as closing the contrast question; A5/B4 close the LIGHTING-RIG question only.

## 7. Gates (PC-trio Pattern E)

1. **sam Gate-1 (pre-fire):** ✅ DONE 2026-06-13 — PASS-WITH-WARN (4 WARN, 0 BLOCK). Finding `agentic_orchestration/qa/findings/2026-06-13-mantis-celestial-sphere-rework-gate-1.md`. All four WARNs folded (§ 9).
2. **radagast design-fit:** ✅ DONE 2026-06-13 — PASS-WITH-WARN (1 amendment, 0 BLOCK). Verdict `agentic_orchestration/radagast/notes/2026-06-13-celestial-sphere-rework-design-fit.md`. § 3 amendment + acceptance #5/#6 reworded; forward Q5 item logged (§ 6).
3. **Both PASS → dispatch FIRED** (STATUS → ACTIVE per Pattern E autonomous-pair ratification); mantis executes in a dedicated session.
4. **sam Gate-2 (post-output):** on mantis's tagged commit — reviews **Tier-A criteria only** (A1–A7). Render-gated **Tier-B criteria (B1–B5) confirm post-render with Matt at console and do NOT block the commit's Gate-2 or the wave-close push** (sam WARN-4). Tier-B confirmation is a separate render-evidence pass.

## 8. Sign-off

**Authored:** david-h 2026-06-13 from empirical findings of the resumed P0.1 render session.
**Authority:** david-h PC-seam dispatch authority; Matt-at-console session producing the findings.
**Routing:** david-h orchestrates; sam Gate-1 + radagast design-fit ratify; mantis executes; sam Gate-2.
**Cross-host:** P0.1 produced findings not captures; cross-host note to Mac-KR queued (S5 + S1 both gated on this rework).
**Composition:** preserves all prior canonical commitments; coupled to the WS2 Niagara commission (same celestial-sphere geometry) but distinct scope.

---

## 9. Fold-record (PC-trio ratification 2026-06-13)

**sam Gate-1 — PASS-WITH-WARN (4 WARN, 2 INFO, 0 BLOCK):**
- **WARN-1** (execution-environment hazard) → folded into § 2 "Execution-environment fallback": Niagara-stack edits (1.2/1.3) get an explicit "never windowed-editor-over-SSH; hand Matt a manual-BP-step list if the headless/bridge path can't perform the edit" clause.
- **WARN-2** (acceptance #4 needs a metric) → folded into A7 + B2: `stat gpu` budget threshold (stable frame ≥ N sec, no rising trend toward device-removed) is the documented pass target.
- **WARN-3** (partition acceptance into tiers) → § 4 split into Tier-A (mantis-headless A1–A7) vs Tier-B (render-confirmed B1–B5).
- **WARN-4** (re-sequence gates) → § 7.4: Sam Gate-2 reviews Tier-A only; Tier-B confirms post-render and does not block the commit's Gate-2 or wave-close push.

**radagast design-fit — PASS-WITH-WARN (1 amendment, 0 BLOCK):**
- **(a) sky-geometry** PASS — R=8,000 interior-sphere reposition corrects TOWARD § 2.6/§ 6.3; nebula-stays-on is canon-required, not optional.
- **(b) figure key-light** amendment → § 3 design-constraint preamble (the three gandalf-ruling constraints: motivated-not-spotlight / distinct-from-spirit-glow / direction-now-values-later) + acceptance B3 (worldlight-on-ordinary-person, not spotlight; values console-tuned) + B4 (Rig-A key distinct from Rig-B spirit-glow).
- **(c) FigureStandIn** PASS — placeholder acceptable for the lighting-readability spike; Q5 spirit-visual scoping logged as a forward radagast↔Mac-gandalf consult item (§ 6), not this dispatch.

**Carried ruling:** the Earth-avatar key-light independence call was already made Mac-side by gandalf (handoff design question 1); radagast folded the DIRECTION (not values). No new cross-cutting consult needed for (b); the Q5 spirit-visual consult is the only forward cross-cutting item.

**End of dispatch (ACTIVE — fire-ready).**
