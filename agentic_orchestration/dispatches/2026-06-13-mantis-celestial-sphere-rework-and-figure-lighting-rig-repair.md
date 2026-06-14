# Mantis Dispatch — Celestial-Sphere Rework + Figure-Lighting-Rig Repair (unblocks S1 + S5)

**STATUS:** DRAFT — pending PC-trio ratification (sam Gate-1 + radagast design-fit per Pattern E) before it fires.
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

## 3. Repair #2 — figure-lighting-rig repair

Diagnostics already EXCLUDED live (do not re-chase): exposure (Unlit-visible/Lit-black), light hidden (`RigA_Moonlight` eye-icon ON), lighting channel mismatch (`SK_EarthAvatar` on Channel 0), low intensity (10× still black).

| Sub-step | Action |
|---|---|
| 2.1 | Inspect `RigA_Moonlight` **rotation/aim** — a directional light's lit side follows rotation; if it points its lit face away from `Cam_GroundLookUp`, the avatar's camera-facing side stays in shadow regardless of intensity. Re-aim so the figure's camera-facing surfaces are lit. |
| 2.2 | Inspect `RigA_Skylight` source/intensity — with an empty sky it captures ~0; set a real source (specified cubemap or `Lower Hemisphere Is Solid Color`) so it carries ambient fill independent of the celestial sphere. |
| 2.3 | If still black: force a **lighting rebuild** (Build Lighting Only) in case stationary/static lighting is stale; confirm `SK_EarthAvatar` mobility + the lights' mobility are compatible. |
| 2.4 | Confirm the figure lights WITHOUT any dependency on `ns.celestialsphere` emissive (the rig must stand alone). |

**Acceptance #2:** `SK_EarthAvatar` reads clearly in **Lit** under Rig A from `Cam_GroundLookUp`, with the celestial sphere present-and-repositioned (not the old origin cloud).

## 4. Acceptance criteria

| # | Criterion |
|---|---|
| 1 | 1,005,000-particle count root-caused + documented (§ 1) |
| 2 | Celestial-sphere emitter on GPU sim; no CPU-cap warning |
| 3 | Stars render on the **R=8,000 sphere** via JSON-driven user-params (Gate-A); origin ±67 cloud gone |
| 4 | Volumetric nebula renders the look-up view WITHOUT GPU crash at default (no CVar band-aid needed) |
| 5 | `SK_EarthAvatar` reads in Lit under Rig A from `Cam_GroundLookUp` (figure-lighting repair) |
| 6 | Rig A/B toggle (`RigA_Moonlight`+`RigA_Skylight` vs `RigB_SpiritGlowOnly`) produces a visible, judgeable lighting difference on the figure (S5 re-shoot enabled) |
| 7 | `stat gpu` / `stat fps` / `stat unit` captured; performance documented for the repositioned sphere + tamed nebula |
| 8 | Sam Gate-2 review PASS or PASS-WITH-WARN |
| 9 | David-H wave-close memo authored + committed; push from `mhwet` context |
| 10 | No raw LLM player-facing content (D7) |

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

## 7. Gates (PC-trio Pattern E)

1. **sam Gate-1 (pre-fire):** review this dispatch DRAFT — scope, acceptance testability, math-before-code sufficiency, R48.4 framing. BLOCK authority.
2. **radagast design-fit:** (a) does repair #1 honor § 2.6 + § 12 sky-surface canon; (b) the standalone design question — should the figure carry its own key light independent of the sky (the rig's sky-dependency is the root of finding #3); (c) is `FigureStandIn`-as-placeholder acceptable for the manifestation spike or does the spirit visual need scoping now.
3. **Both PASS → dispatch fires** (STATUS → ACTIVE); mantis executes in a dedicated session.
4. **sam Gate-2 (post-output):** on mantis's tagged commit.

## 8. Sign-off

**Authored:** david-h 2026-06-13 from empirical findings of the resumed P0.1 render session.
**Authority:** david-h PC-seam dispatch authority; Matt-at-console session producing the findings.
**Routing:** david-h orchestrates; sam Gate-1 + radagast design-fit ratify; mantis executes; sam Gate-2.
**Cross-host:** P0.1 produced findings not captures; cross-host note to Mac-KR queued (S5 + S1 both gated on this rework).
**Composition:** preserves all prior canonical commitments; coupled to the WS2 Niagara commission (same celestial-sphere geometry) but distinct scope.
**End of dispatch (DRAFT).**
