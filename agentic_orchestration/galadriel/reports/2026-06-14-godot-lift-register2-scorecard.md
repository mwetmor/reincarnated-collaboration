# Visual-Register Scorecard — Godot "Lift" Vertical Slice vs Register-2 Rubric

**STATUS:** CURRENT (galadriel scoring artifact; evidence-input for gandalf A-vs-B ruling)
**Date:** 2026-06-14
**Author:** galadriel (visual-perception + benchmark steward)
**Scope:** SCORING ONLY. This artifact measures the capture against galadriel's register-2 rubric. It does NOT rule the A-vs-B design question — that is gandalf's. This is evidence FOR that ruling.
**Companion:** rubric instruments at `agentic_orchestration/galadriel/pipeline/register-metrics.mjs` + `lifecycle-score.mjs`; raw scores at `pipeline/lifecycle-scores.json`; CV overlays in this directory.

---

## 0. What was scored

- **Capture set:** `reincarnated-godot/harness_logs/11_lift_capture_01..100.png` — 100-frame motion sequence, 1152x648, Godot Movie Maker (clean deterministic source).
- **Scene:** composed Synty knight (modular part-swap, Starter armor) in dark POLYGON dungeon graybox. Near-black ambient; warm key rake + cold blue rim + low fill + warm hand glow-pool; filmic tonemap; glow/SSAO/distance-fog ON. VFX: fog/dust/smoke always-on + FX_Fire_Large_01 as S-tier hero-skill bloom that **ignites mid-sequence**.
- **Scoring method:** CV instruments run **across the full 100-frame lifecycle**, NOT a single still. Per galadriel F1 finding, stills under-represent VFX (highest-leverage axis); the fire is a windowed event, so instruments are sampled across pre-ignition → ignition-rise → peak-bloom → live-burn → waning-drift → settle.

## 1. The rubric (galadriel's)

Composite mean **≥ 3.6/5**, with **lighting ≥ 4 AND VFX ≥ 4 MANDATORY**.

| Axis | Target | Instrument |
|---|---|---|
| Lighting drama | manual ≥ 4 | LDR ≥ 115, SHF ≥ 30% (CV-assisted) |
| VFX presence | manual ≥ 4 | ≥ 1 hero bloom, HLF ≥ 1.5% (CV-assisted) |
| Material-shading | manual ≥ 4 | gradient/light-response, NOT flat per-face |
| Geometry register | manual ≥ 3 | low-poly fine; silhouettes legible |

NOT targets: high-frequency-detail / strong-edge%. Premium ≠ detail-density.

## 2. CV instrument values (lifecycle-sampled)

Instrument definitions identical to the 2026-06-14 register baseline (`register-metrics.mjs`): 960w inside-fit, grayscale luma for LDR/SHF/HLF, raw RGB for SAT. Thresholds: HLF>0.80 luma highlight, SHF<0.12 luma shadow, LDR=p95−p05.

| Phase | frames | LDR | SHF % | HLF % |
|---|---|---|---|---|
| pre-ignition | 1-8 | 165.6 | 78.6 | 3.04 |
| ignition-rise | 9-22 | 225.1 | 68.1 | 8.70 |
| peak-bloom | 23-40 | 251.3 | 51.6 | 12.50 |
| live-burn | 41-70 | 251.1 | 59.6 | 12.79 |
| waning-drift | 71-94 | 227.6 | 59.6 | 8.00 |
| settle | 95-100 | 194.7 | 57.3 | 4.41 |
| **whole-sequence mean** | 1-100 | **231.6** | **60.7** | **9.73** |
| dark-mood window (1-8 + 95-100) | | 178.1 | 69.5 | 3.63 |

**Rubric-relevant extracts:**
- **HLF peak = 14.4%** (frame 28) vs threshold 1.5% → **9.6× over**. Hero-skill bloom unambiguously present.
- **LDR whole-mean = 231.6** vs threshold 115 → **2.0× over**. Peak hits the 8-bit ceiling (253) — fire blows to max white against near-black ambient. Even the lowest phase (pre-ignition, 165.6) clears 115.
- **SHF whole-mean = 60.7%** vs threshold 30% → **2.0× over**. Never drops below 46% even at peak-bloom (when fire floods the frame). Genuine dark-mood.

**Overlay validation** (`11_lift_peak28_lumamask.png`): the HLF highlight mask lands exactly on the fire column + figure hot-core; the SHF shadow mask lands on the dungeon voids. Instruments are measuring the correct pixels — not fooled by a UI element or compression artifact.

## 3. Per-axis manual scores

### Lighting drama — **5 / 5** (target ≥ 4 — MET)
LDR 231.6 (2× threshold) + SHF 60.7% (2× threshold), both sustained across every lifecycle phase. The scene is a lit volume punched out of deep dark: warm key rake on the figure, cold blue rim on the pillars, warm glow-pool at the feet, the rest near-black. The fire adds a dynamic warm key that sweeps the whole scene at peak (crate, floor, back-wall all warmly re-lit) then recedes. This is filmic, dramatic, register-2 lighting — not flat-lit graybox. *Evidence: lifecycle LDR/SHF table; `11_lift_peak28_lumamask.png`.*

### VFX presence — **5 / 5** (target ≥ 4 — MET)
HLF peak 14.4% (9.6× threshold), sustained ~12.5% through peak-bloom + live-burn. The FX_Fire_Large_01 hero bloom is body-anchored and erupts vertically from the figure's torso — a genuine S-tier skill event with a clean lifecycle (rise → peak column → sustained burn → collapse → residual). Always-on fog/dust/smoke add atmospheric VFX even pre-ignition (HLF already 3% from the glow-pool). *Evidence: lifecycle HLF table; `11_lift_lifecycle_strip.png`.* (T-pose caveat: § 5 — does NOT depress this score.)

### Material-shading — **4 / 5** (target ≥ 4 — MET)
LMV 32-38 across lit phases; per-tile heatmap (`11_lift_settle99_lmv_heatmap.png`, mean per-tile std 18.6 at 24×14) shows variance **distributed across lit surface interiors**, not concentrated only at face boundaries — the signature of light-responsive material vs flat per-face fill. Floor shows a continuous warm-glow gradient with specular sheen; armor catches warm light per-surface-orientation; back-wall panels show top-to-bottom falloff. The dark-tinted StandardMaterial3D + procedural FastNoiseLite roughness reads as light-responsive stone. **Honest caveat (not over-claimed):** the CV instrument cannot fully separate roughness-driven micro-variance from lighting-driven macro-gradient; both are present and both push register-2, but the texture contribution alone is not isolable. Held at 4 (not 5) because the per-face roughness response, while present, is subtle — the lift is carried more by lighting than by surface micro-detail. *Evidence: LMV heatmaps; settle frame 99/100.*

### Geometry register — **4 / 5** (target ≥ 3 — MET, exceeds)
Silhouette fully legible: distinct helmet, shoulders, layered chest, faulds, greaves, articulated arms; clean modular part-swap with no clipping or broken seams (compose-proof `10_composed_knight_render.png`). Low-poly faceting is visible and **correct** for register-2 (Torchlight Infinite / Last Epoch run this exact silhouette-readable low-poly register). Scores 4 not 5 only because it's a single hero figure with no environmental geometry richness in frame; the figure itself is clean register-2 geometry. *Evidence: compose-proof render; settle frames.*

## 4. Composite + mandatory gates

| Axis | Score |
|---|---|
| Lighting drama | 5 |
| VFX presence | 5 |
| Material-shading | 4 |
| Geometry register | 4 |
| **Composite mean** | **4.50** |

- **Composite mean 4.50 ≥ 3.6** → **PASS**
- **Mandatory gate — Lighting ≥ 4:** 5 → **PASS**
- **Mandatory gate — VFX ≥ 4:** 5 → **PASS**

All gates clear, with margin.

## 5. T-pose / VFX-as-hero-skill caveat verdict

**The static compose T-pose does NOT break the VFX-as-hero-skill read, and does NOT materially depress the VFX-presence manual score.**

- The fire originates **body-centered**, erupting vertically from the figure's torso (frames 25/28/70) — the hot core sits inside the silhouette. This reads as a power *emanating from the character* (ignite / immolation-aura / fire-channel), not as ambient fire a figure stands beside. Body-anchored fire reads as "the character's skill" regardless of limb pose.
- The CV instruments (HLF/LDR/SHF) are pose-agnostic — bloom pixel-presence/brightness/contrast are identical T-pose vs combat-pose. The bloom is the bloom.
- What the T-pose **costs** is *cast intentionality / directionality* (narrative legibility), NOT VFX presence. A combat cast-pose would convert "character is channeling fire" → "character is *casting* fire," adding agency. The arms-out compose pose neither points at nor shapes the fire.

**Re-capture recommendation: NO (not required for the ruling).** A combat-pose re-capture would raise skill *legibility/presentation*, but is unlikely to change any of the four axis scores — VFX-presence already sits at 5 on bloom merits, and lighting/material/geometry are pose-agnostic. The composite and both mandatory gates pass without a re-pose. Re-pose is a cheap, high-presentation-value *polish* follow-up gandalf MAY want for the A-vs-B presentation, but it is NOT a scoring-gate blocker.

## 6. One-line read (evidence FOR gandalf's ruling, not the ruling)

**The lift reaches register-2: cheap Synty modular geometry, treated with filmic dark-mood lighting + a body-anchored S-tier fire bloom + light-responsive procedural material, scores composite 4.50/5 and clears both mandatory gates (lighting 5, VFX 5) with 2×-margin CV instrument support — the same geometry that reads as register-1 graybox under flat lighting reaches premium-stylized-ARPG register under the lift.**

## 7. Reproducibility

- Instruments: `pipeline/lifecycle-score.mjs` (lifecycle CV), `pipeline/register-metrics.mjs` (baseline-comparable defs), `pipeline/lifecycle-strip.mjs` + `pipeline/lmv-heatmap.mjs` (overlays).
- Raw scores: `pipeline/lifecycle-scores.json` (per-frame + per-phase + extracts).
- Overlays (this dir): `11_lift_lifecycle_strip.png`, `11_lift_peak28_lumamask.png`, `11_lift_settle99_lmv_heatmap.png`, `11_lift_preign01_lmv_heatmap.png`.
- Given the same 100 frames + these instruments, another galadriel-instance reproduces these values exactly (deterministic; no random sampling).
