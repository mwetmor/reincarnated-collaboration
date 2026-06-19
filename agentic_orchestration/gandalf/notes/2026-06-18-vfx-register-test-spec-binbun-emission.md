# SPEC — VFX register-test: does Binbun + in-engine juice reach the genre-register floor?

**Author:** gandalf (design steward — criteria + adjudication half of the dual-gate).
**Date:** 2026-06-18. **Type:** controlled register-test spec — the design half. galadriel owns the CV instrument; drax owns the build/render; gandalf adjudicates.
**Trigger:** Matt — fire the tripod (drax dev / galadriel judge / gandalf design) directly from this session to settle whether the purchased Binbun catalogue is register-sufficient before committing to (or skipping) a Hovl-style Unity→Godot harvest pipeline.
**Governs / governed by:** locked register-2 (`canonical/story/style-register.md` — stylized-low-poly-3D Synty, "S-tier GPUParticles3D juice + dramatic GI"); the pixel-VFX pushback (`pushback/2026-06-17-pixel-vfx-into-godot-register-conflict.md`); the rubric-ladder tee-up (`notes/2026-06-18-scene-scoring-rubric-opportunity-memo.md`, T0–T3); the VFX research synthesis (`legolas/research/2026-06-18-godot-vfx-packs/synthesis.md`).

---

## 1. The decisive question (why this test, and why now)

The Legolas run established **Binbun as the parametric backbone** (covers 5/6 substrate axes, CC0, but reads "stylized-clean / *slightly under* register"), with a **Hovl Unity→Godot harvest** as the candidate fix for the on-register-but-low-axis-coverage gap. The synthesis named **Gap #8 — the emission test — as the single experiment that collapses the decision tree.**

**The one question:** When Binbun's CC0 particles are pushed with the locked register's OWN proven lever — high `emission_energy` + additive blend + layered sub-emitters, through a dramatic-GI post chain — **do they reach the T2 genre-register floor (D2-class), or do they structurally cap below it?**

- If they REACH it → the Hovl harvest demotes to optional polish. We saved a whole pipeline build.
- If they cap BELOW it → the harvest is justified, and we now know *by how much* and *on which axis* — which is what makes the harvest worth its cost instead of a guess.

This is the cheapest possible experiment that produces a load-bearing verdict: **no new purchases, no harvest tooling, ~one build session.** It also produces the first real Godot frames to score on the T0–T3 ladder — calibrating the rubric and answering the buy/build question in the same pass.

---

## 2. The variants (drax builds — priority-ordered)

All in `reincarnated-godot` (Godot 4.6.3, Forward+). A single test scene, one variant active at a time, identical stage (§3).

| # | Variant | Source | What it isolates | Priority |
|---|---|---|---|---|
| **V0** | Binbun fire-cast, **DEFAULT** | `Assets/Binbun_VFX/assets-19/BinbunVFX/fire_effects/effects/Fire/fire_ball_*.tscn` (+ `fire_trail.tscn` for travel), tinted to a clear fire-orange hue, **stock tool-script settings** | The out-of-box register read — the backbone "as shipped" | **MANDATORY** |
| **V1** | Binbun fire-cast, **JUICED** | Same scene, **high `emission_energy` + additive blend_mode + one layered sub-emitter** (a 2nd `GPUParticles3D` for ember/spark — the PoE "composable detail" move) | The in-engine juice ceiling — backbone + the locked lever | **MANDATORY** |
| **V2** | Flipbook-into-3D | `Assets/brackeys_vfx_bundle/flipbooks/fire_01_8x8.tga` (8×8 = 64 frames) as a `GPUParticles3D` billboard + additive + flipbook flow (the PoE/D4 technique my pushback validated as sound — Brackeys sheets are smooth/hand-drawn, **register-appropriate**, a free proxy for what a Hovl harvest yields) | Whether a flipbook source structurally beats Binbun particles → the "is the harvest even needed" probe | **STRONGLY ENCOURAGED** |
| **V3** | Non-fire generalization | `assets-14/.../magic_orb_flash/magic_orb_flash_vfx_0X.tscn` re-tinted to a cold/arcane hue, V1 juice settings | That the juice lever generalizes across element hues, not just fire | **OPTIONAL** (only if cheap; skip if V0–V2 eat the session) |

**The headline comparison is V0 vs V1.** V2 is the harvest-need cross-check. V3 is a generalization sanity check.

**Tool-script API:** `assets-14/BinbunVFX/shared/script/vfx_controller.gd` + `vfx_light.gd` expose the parametric knobs — use them; do not hand-rebuild particle materials from scratch.

**Godot 4.6.3 / Vol.2 shader caveat:** the `fire_effects` pack (assets-19) ships its own shader under `src/shader/fire` — Binbun's Vol.2 serialization caveat applies above Godot 4.5. **If assets-19 throws shader-import errors, fall back to the Vol.1-safe magic-orb packs** (`assets-14/.../magic_orb_flash/`, re-tinted fire-orange) as the V0/V1 subject — the experiment is about the emission lever, not specifically the fire pack. Surface the swap; don't burn the session fighting a shader.

---

## 3. The stage contract (controlled-experiment rigor — Discipline #10)

Validity depends on isolating ONE independent variable (emission + blend, V0→V1). Everything else is **fixed identically across all variants:**

- **Camera rig:** locked distance + angles. One **primary** angle (the player-facing 2.5D-ish view); 3 secondary angles for multi-view robustness.
- **Background:** neutral mid-grey, featureless. No environment geometry, no textures — register-metrics must read the VFX, not a dungeon.
- **WorldEnvironment / post:** glow (bloom) threshold, tonemap (Filmic or ACES), exposure, ambient — **set once, frozen across every variant.** This is the fixed "lens." V1's higher emission naturally blooms *more* through the same frozen post — that is the lever we are measuring, not contamination.
- **The ONLY thing that changes V0→V1:** `emission_energy` + `blend_mode` (+ the V1 sub-emitter). Nothing else.

If any stage parameter has to differ for a variant to render at all, **flag it** — an uncontrolled difference invalidates the delta read.

---

## 4. Capture spec (drax RENDERS — native Godot, not galadriel's web capture)

galadriel's `capture.mjs` is Playwright/headless for **web** surfaces. This is a Godot 3D scene → **drax renders the PNGs in-engine** via a capture script:

```gdscript
get_viewport().get_texture().get_image().save_png(path)
```

stepping the particle sim deterministically (fixed `delta`, seed the `GPUParticles3D` if needed for repeatability). Two capture products per variant:

1. **Temporal lifecycle sequence** — PRIMARY angle, **~16–24 frames** across the full cast→travel→impact→residual lifecycle. Feeds `spell-motion-score` (energy-travel, motion-presence, directionality need a time axis).
2. **Multi-angle peak stills** — the visual-peak frame at **3–4 angles**. Feeds `register-metrics` (HFD/LMV/LDR/SAT/HLF/SHF) + multi-view robustness.

**Naming (so galadriel can batch):** `{variant}_{angle}_{frame:03d}.png` — e.g. `v1_primary_007.png`, `v1_peak_angle2.png`. Write to a single flat dir; hand galadriel the path.

**Deliver to galadriel:** the PNG dir + a one-paragraph build note (which source pack used, the exact V0 vs V1 setting deltas, any stage exception, any Vol.2 shader fallback).

---

## 5. Division of labor

- **drax (dev):** build V0/V1 (+V2/V3), the locked stage rig, the capture script; render the PNG sets; write the build note. **Does not score.**
- **galadriel (judge):** Wave 1 — anchor the T0–T3 ladder from the genre reference set (§7). Wave 2 — score drax's PNGs through `register-metrics.mjs` + `spell-motion-score.mjs` onto the anchored ladder; report per-variant tier-positions + the V1−V0 delta. **Does not adjudicate the buy/build call.**
- **gandalf (design):** this spec + the criteria (§6); Wave 3 — adjudicate PASS/MARGINAL/FAIL and write the VFX-library decision memo (buy-vs-build verdict). **Cross-check eye↔number: if the instrument and my eye diverge on a variant, that divergence is a first-class finding, not noise** (the dual-gate working).

---

## 6. Register-pass criteria (gandalf design half — the verdict logic)

**"Reaches register" = V1 meets the T2 floor on the three load-bearing JUICE axes, AND hue-legibility ≥ T2:**

| Juice axis | Instrument metric(s) | Why it's load-bearing |
|---|---|---|
| **Highlight / bloom presence** | `register-metrics` **HLF** (luma>0.80) | The additive-emissive glow that separates "lit FX" from "flat decal" — the lever that scored 5/5 at register-lock |
| **Layering / depth** | `register-metrics` **LMV** + `spell-motion` **layering-variance** | PoE's "composable detail" — multiple depth layers vs. a single flat billboard |
| **Motion** | `spell-motion` **motion-presence + energy-travel** | A spell is a *verb*; static juice is not enough — the cast must read as moving energy |

Plus **hue-legibility ≥ T2** (`spell-motion` hue-legibility): the element reads unambiguously as fire (or V3's arcane) — element-legibility is non-negotiable for a 400+-combinatory catalogue where the player must *read* the element at a glance.

### Verdict tiers

- **PASS** — V1 ≥ **T2 floor** on all three juice axes + hue. → *Binbun CC0 backbone is register-sufficient with the in-engine juice lever.* Hovl harvest demotes to **optional polish** for hero slots. Biggest win: no harvest pipeline to build.
- **MARGINAL** — **T1 ≤ V1 < T2.** → *Binbun = parametric VOLUME backbone* (carries the 400+ breadth via parametric axes), *Hovl harvest JUSTIFIED for the hero/signature slots* that must hit T2.8+. A two-tier asset strategy: Binbun for breadth, harvest for heroes.
- **FAIL** — **V1 < T1** (juice lever doesn't lift it above placeholder-coherence). → *Reopens the backbone source choice.* Binbun structurally can't carry register; the harvest becomes the **primary** path, not the polish path.

### The headline read — the V1−V0 delta

The *absolute* tier matters, but the **delta diagnoses the cause:**

- **LARGE delta (V1 ≫ V0):** the gap to genre-register is an **emission/post gap** → cheap, in-engine, no new assets. *Best outcome — the lever works.*
- **SMALL delta (V1 ≈ V0):** the gap is **structural** (source geometry/texture caps register regardless of juice) → *Hovl harvest justified* even if V1 happens to scrape T2.

### V2 cross-check (the harvest-need probe)

- **V2 ≫ V1** on the juice axes → flipbook source is structurally richer than Binbun particles → **harvest is worth it.**
- **V2 ≈ V1** → Binbun particles are as good as register-appropriate flipbooks → **no harvest needed**, regardless of the V1 absolute tier.

---

## 7. Wave structure + the reference-set state

- **Wave 1 (parallel — two Agent calls, one message):**
  - **drax** → build + render V0/V1 (+V2; V3 if cheap), deliver PNG dir + build note.
  - **galadriel** → anchor the T0–T3 ladder from `galadriel/reference-images/3d-stylized-arpg-2026-06-14/`.
    **Known reference-set state (gandalf inspected 2026-06-18):** `last-epoch/` (LE-01..04) and `torchlight-infinite/` (TLI-01..04) are populated with general-combat frames; **`diablo/` and `path-of-exile/` folders are EMPTY placeholders;** `_strips/` has `dark-mood.png` + `register-spread.png`. The frames are general-combat, **not isolated fire-spell.** Wave-1 task: anchor the ladder with what exists, **flag the empty D2/PoE folders, and best-effort source 3–5 isolated fire-spell exemplars** (PoE fireball/firestorm, D2/D4 fire, LE fire skill) so the T2/T3 *fire* anchor is real. **If sourcing is hard, surface the gap and anchor against the LE/TLI combat frames — the experiment's PRIMARY signal is the V1−V0 delta + V2 cross-check, which are delta-based and do NOT block on a perfect absolute anchor.** Absolute tier = "as good as the anchors allow, refine later" (honest to instrument v0.1 maturity).
- **Wave 2 (dependent):** resume galadriel via SendMessage with drax's PNG dir → score onto the anchored ladder; report per-variant tiers + V1−V0 delta + V2 cross-check + any eye↔number divergence.
- **Wave 3:** gandalf adjudicates → PASS/MARGINAL/FAIL → VFX-library decision memo (buy-vs-build verdict + the harvest-justification, if any, with the specific axis + magnitude of the gap).

---

**Signed:** gandalf, 2026-06-18. This is the design half of the dual-gate — the criteria and the verdict logic. The single decisive question is Gap #8: does Binbun + the locked register's own juice lever reach the T2 floor? V0 vs V1 is the headline (emission/post gap vs. structural gap); V2 is the harvest-need cross-check. PASS saves a pipeline; MARGINAL defines a two-tier strategy; FAIL reopens the backbone. Cheapest experiment that collapses the buy/build tree — and the first real Godot frames on the T0–T3 ladder. Tripod fires now.
