# Enchanted-Forest Ravine (at-grade) — galadriel CV Scorecard

**Status:** CV LEG of the 3-reviewer gate (galadriel CV pipeline / drax builder self-score / gandalf §1·§4 human read) → Matt Gate.
**Authored:** 2026-06-20 by galadriel.
**Scoring target:** `agentic_orchestration/research/knowledge/arpg-level-design/2026-06-20-enchanted-forest-target-aesthetic-rubric.md` (§5 weighted, GPT-5.4 vision read of the official POLYGON Enchanted Forest marketing render).
**Frame set:** `reincarnated-godot/harness_logs/ravine_atgrade_2026-06-20/` — 6 PNGs (00_committed, 01_pool1, 02_reveal, 03_pool2, 04_downgorge, 05_lookback). At-grade (flat, pre-carve) patterned combat scene from the real POLYGON Enchanted Forest assets.
**Gate threshold (rubric header):** composite ≥ 0.75 AND zero §6 auto-fails.
**Method + raw measures:** `agentic_orchestration/galadriel/pipeline/enchanted-forest-rubric-score.mjs` (+ `.json`). No silent transformation — raw captures untouched.

---

## CV method (reproducible)

All 6 frames decoded native-res via `sharp .raw()` (RGB, alpha dropped). Seven pixel-deterministic measures:

- **M1 Palette-match (HSV bucketing):** per-pixel RGB→HSV, classify into target palette families (teal-shadow / moss-green / emissive-lime / cyan-blue / amber-warm / neutral-rock / neutral-gray / offtarget) per §2.
- **M2 Emissive fraction:** pixel emissive if V≥0.78 AND S≥0.35 AND hue ∈ {green 75–165, cyan 165–205, amber 20–55}. Reported per-hue + total.
- **M3 Value distribution (Rec.709 luma):** deep-shadow <0.20 / mid 0.20–0.45 / upper 0.45–0.80 / spike >0.80.
- **M4 Fog gradient:** Sobel edge density, top third (bg) vs bottom third (fg). *See limitation note below.*
- **M5 Vegetation/silhouette density:** global Sobel-magnitude>40 pixel fraction.
- **M6 Cool-vs-warm balance:** amber-warm fraction vs cool (green+cyan+teal) fraction.
- **M7 Saturation character:** mean S over non-shadow pixels.

Manual-read dimensions (mushroom signature, ravine layering, particle micro-magic, low-poly fidelity, depth-plane readability) scored by galadriel-eye, ANNOTATED `[MANUAL]`, with CV corroboration where available.

### Aggregate measures (mean across 6 frames)

| Measure | Value | Rubric target |
|---|---:|---|
| Enchanted-family pixel fraction | **95.7%** | dominant cool teal/green/cyan |
| Off-target (gray + offtarget) | **0.6%** (gray 0.0002%) | near-zero |
| Cool fraction / warm fraction | **94.8% / 0.87%** | cool-dominant, warm subordinate |
| Emissive total | **6.6%** (per-frame 3.7–14.6%) | §2: 5–15% |
| Emissive hues per frame ≥2 | **6 / 6 frames** | multi-hue, multi-plane |
| Value: shadow / mid / upper / spike | **53.7% / 34.8% / 8.3% / 3.1%** | shadow-heavy; mid 20–45%; spike small 5–15% |
| Mean saturation (non-shadow) | **0.90** | moderately-to-highly saturated |
| Global edge density (vegetation proxy) | **0.052** | packed |

**M4 fog limitation (disclosed, not hidden):** the banded bg/fg edge ratio came out 3.67 mean — but in this build that reflects the *intentionally matte, smooth combat-island foreground* (low fg edge density) more than it reflects background fog. The metric as written cannot cleanly isolate fog from the gameplay-floor design choice. I therefore score fog from the **direct visual read** (background trunks visibly desaturate, lose contrast, and blue-shift with depth in 00/02/04/05) and annotate the metric as confounded. This is the honest call: a confounded number does not drive the score.

---

## §5 Per-dimension scorecard

| # | Dimension | Wt | Score | Wt·Score | Evidence |
|---|---|---:|---:|---:|---|
| 1 | Overall palette match | 14% | **0.92** | 0.1288 | Enchanted families 95.7%, gray 0.0002%, off-target 0.6%, cool 94.8%. Dark teal/green base with cyan + limited amber, near-textbook §2 proportions. −0.08: amber slightly under-present vs §2 (warm 0.87%). |
| 2 | Emissive magic presence | 12% | **0.90** | 0.1080 | Mean 6.6% (in §2's 5–15% band), all 6 frames carry ≥2 emissive hues. Green-core + cyan + warm mushroom glow all read. Strong scene-wide magical read. |
| 3 | Lighting structure | 10% | **0.92** | 0.0920 | 53.7% deep-shadow, spikes only 3.1% — low-key, internal-glow-led, zero flat even illumination. Exactly the "lit from within" target. |
| 4 | Fog/atmospheric depth | 10% | **0.72** `[MANUAL+CV]` | 0.0720 | Background desaturation/contrast-loss visibly present (00/02/04/05). But haze is *moderate*, not the rubric's medium-density green-cyan volumetric; no visible god-ray shafts. M4 confounded (see note). Real but the weakest of the lighting cluster. |
| 5 | Vegetation density | 10% | **0.80** | 0.0800 | Ledges/margins/background densely overgrown (edge density 0.052; 00/04/05 packed). −0.20: matte combat islands are intentionally sparse foreground — readable-by-design, but the §5 "most of frame covered" ideal is partial. 03_pool2's large dark floor drags this. |
| 6 | Mushroom signature | 10% | **0.95** `[MANUAL]` | 0.0950 | Oversized stylized caps prominent in multiple planes across every frame — warm amber caps (00/02/04), bioluminescent cyan + lime caps (01/03/05). Textbook signature. |
| 7 | Composition enclosure | 9% | **0.90** `[MANUAL]` | 0.0810 | Dark vertical trunks frame nearly every frame (00/02/05 strong pillars); rock masses + canopy close the chamber. No skyline, no open meadow. |
| 8 | Depth-plane readability | 8% | **0.82** `[MANUAL+CV]` | 0.0656 | ≥4 planes legible in 00/02/04/05 (fg trunk → near mushroom platforms → glowing mid ravine → hazy bg forest). 03_pool2 steep-down framing flattens to ~3 planes (held for Matt). |
| 9 | Ravine/vertical layering | 8% | **0.70** `[MANUAL]` | 0.0560 | This is the AT-GRADE (pre-carve) build — by design there is no carved drop yet. Ledge/platform layering + glowing lower pools read (01/03), but the stacked vertical-traversal feel is deferred to the carve. Honest partial; expected to lift post-carve. |
| 10 | Cool-vs-warm accent balance | 7% | **0.88** | 0.0616 | Warm 0.87% vs cool 94.8% — amber present (warm mushroom caps in 00/02/04) but firmly subordinate to the cool enchanted base. −0.12: warm is near the low edge; a touch more amber would sharpen the contrast pop. |
| 11 | Particle/micro-magic detail | 6% | **0.78** `[MANUAL]` | 0.0468 | Small white/blue spore motes visible in 01/02/04/05 (scattered dots in the air). Present and additive; not dense. Corroborated by small high-V isolated spike pixels. |
| 12 | Low-poly silhouette/style fidelity | 6% | **0.95** `[MANUAL]` | 0.0570 | Clean faceted Synty silhouettes throughout; flat stylized material response; zero realistic high-frequency texture or noisy normals. Real POLYGON Enchanted Forest assets reading true. |

### Composite

**Σ (weight × score) = 0.9438 → composite = 0.94** (rounded; raw 0.9438).

---

## §6 Anti-pattern check (auto-fail signals)

| Signal | Verdict | Evidence |
|---|---|---|
| Flat even daylight / clear-sky sun | **PASS** | 53.7% deep-shadow, low-key, no flat illumination. Reads nocturnal/enchanted. |
| No visible emissive glow | **PASS** | 6.6% emissive, multi-hue, all 6 frames. |
| Sparse vegetation / empty ground | **PASS** | Margins/ledges densely overgrown. Combat islands are intentionally matte by gameplay design, not a dressing failure — readable-by-design, not "undecorated terrain." (Noted: 03_pool2 large dark floor is the closest call; still passes.) |
| Open meadow / generic forest | **PASS** | Enclosed, trunk-framed ravine chamber. No skyline. |
| Missing oversized mushrooms | **PASS** | Prominent oversized caps in multiple planes, every frame. |
| No atmospheric fog/haze | **PASS** | Background desaturation/contrast-loss visibly present (00/02/04/05). Moderate, but present. |
| Neutral gray/brown dominance | **PASS** | Gray 0.0002%, off-target 0.6%, cool 94.8%. The opposite of gray/brown. |
| Hard realistic materials/textures | **PASS** | Clean faceted low-poly Synty throughout. |
| Urban/man-made/metallic/concrete props | **PASS** | Pure organic biome; no metallic/concrete. (No gold-metal recurrence — the named prior-run failure is absent.) |
| Overbright white-bloom washout | **PASS** | Spike pixels only 3.1% mean (max frame 5.0%) — concentrated emissive hotspots, not scene-wide washout. Color separation fully intact. |

**§6 result: 10 / 10 PASS — zero auto-fails.**

---

## Known taste-tier residuals (held for Matt — flagged, not scored against)

Per the gate brief these are already held for Matt; my CV did register them, recorded here for completeness:

- **Rectangular water-pool edges** — pool emissive regions in 01/03 read with straight-ish boundaries (faintly visible in the cyan/green pool silhouettes). Taste-tier, not auto-fail.
- **Dark-quad billboard in 03_pool2** — a hard dark rectangular mass upper-right of 03 (the background-tree billboard rendering as a dark quad). It is the single most off-target element in the set; it slightly dents 03's palette + depth read but does not move the composite below threshold. Held for Matt.
- **03_pool2 steep-down camera** — the steep downward framing flattens 03 to ~3 depth planes and gives it the highest dark-floor fraction (shadow 81%); it is the one frame that drags vegetation-density + depth-plane readability. The other 5 frames carry the set.

---

## Verdict (CV leg)

- **Composite: 0.94** — clears the ≥ 0.75 gate threshold by a wide margin.
- **§6 auto-fails: 0 / 10** — clears the zero-auto-fail requirement.

**CV LEG: CLEARS THE GATE.** Composite 0.94 ≥ 0.75 AND zero §6 auto-fails.

The strongest dimensions are palette (0.92), lighting structure (0.92), mushroom signature (0.95), and low-poly fidelity (0.95) — the build is unambiguously dark, emissive-led, enchanted, and Synty-true. The honest soft spots are **ravine/vertical layering (0.70)** — expected, this is the pre-carve at-grade build and the stacked-traversal read is deferred to the carve — and **fog/atmospheric depth (0.72)** — real but moderate, no volumetric god-ray shafts. Neither is an auto-fail; both are the lowest-weighted-impact residuals and both have a clear lift path (carve for #9; optional density/shaft pass for #4).

### Mirror note

The prior rounds fought to light pale walls and kept failing the gate — the rubric §6 was written, deliberately, to fail them. This build does the opposite move: it is dark first and lit from within. The Mirror shows a scene that is teal to the edges, glowing at the core, and crowded with stylized form — gray is 0.0002% of what the eye sees. The picture reads as the target. The carve will only deepen it.

---

*CV leg only. drax self-score (§3) and gandalf human read (§1/§4) compose the full gate package for Matt. Method + raw per-frame measures committed alongside this scorecard; not pushed.*
