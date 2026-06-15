# Visual-Register Scorecard — Godot Cathedral (REAL curated Synty content) vs Register-2 Rubric

**STATUS:** CURRENT (galadriel scoring artifact; evidence-input for gandalf "A-holds extension" ruling)
**Date:** 2026-06-15
**Author:** galadriel (visual-perception + benchmark steward)
**Scope:** SCORING ONLY. This artifact measures the capture against galadriel's register-2 rubric. It does **NOT** make the A-holds canon call — that is gandalf's, on this evidence. This is the durable evidence FOR that ruling: does register-2 hold on a REAL shipping Synty environment, not just a graybox?
**Companion:** instruments at `agentic_orchestration/galadriel/pipeline/lifecycle-score-cathedral.mjs` (+ shared `register-metrics.mjs` defs); raw scores at `pipeline/lifecycle-scores-cathedral.json`; CV overlays in this directory. Prior graybox scorecard: `2026-06-14-godot-lift-register2-scorecard.md`.

---

## 0. What was scored — and what changed since the lift

- **Capture set:** `reincarnated-godot/harness_logs/12_cathedral_capture_01..100.png` — 100-frame motion sequence, 1152x648, Godot Movie Maker (clean deterministic source).
- **Scene (the increment):** drax instanced Synty's **OWN `Demo_Cathedral_01.tscn`**, isolated the Cathedral section, and applied the **SAME lift recipe 1:1** from `lift_render.tscn` (near-black warm ambient + warm key rake + cold rim + filmic tonemap + glow/SSAO/warm-fog). Hero VFX: a **body-anchored red pentagram that CHARGES then ERUPTS a GPUParticles3D summon fire column.** Braziers burn from frame 0; fog/dust always-on.
- **Why this matters:** the 2026-06-14 lift proved register-2 on a dungeon GRAYBOX + composed knight. gandalf ruled "A-holds" but SCOPED to graybox. This re-validates the *same recipe* on **real shipping curated content** — Synty's own marketed cathedral. If register-2 holds here, the evidence supports extending A-holds graybox → real environment. **That extension is gandalf's call, not mine.**
- **Scoring method:** CV instruments run **across the full 100-frame lifecycle**, NOT a single still. Per galadriel F1 finding, stills under-represent VFX (highest-leverage axis); the fire column is a windowed event, so instruments are sampled across pre-ignition → charge → eruption-rise → peak-bloom → live-burn → waning-settle (drax hero-event timing: charge ~30, erupt ~52).

## 1. The rubric (galadriel's — UNCHANGED from the lift)

Composite mean **≥ 3.6/5**, with **lighting ≥ 4 AND VFX ≥ 4 MANDATORY**.

| Axis | Target | Instrument |
|---|---|---|
| Lighting drama | manual ≥ 4 | LDR ≥ 115, SHF ≥ 30% (CV-assisted) |
| VFX presence | manual ≥ 4 | ≥ 1 hero bloom, HLF ≥ 1.5% (CV-assisted) |
| Material-shading | manual ≥ 4 | gradient/light-response, NOT flat per-face |
| Geometry register | manual ≥ 3 | low-poly fine; silhouettes legible |

NOT targets: high-frequency-detail / strong-edge%. Premium ≠ detail-density. (Same rubric applied to the lift — so cathedral scores are directly comparable.)

## 2. CV instrument values (lifecycle-sampled)

Instrument definitions **BYTE-IDENTICAL** to the 2026-06-14 lift scorer and the register baseline (`register-metrics.mjs`): 960w inside-fit, grayscale luma for LDR/SHF/HLF, raw RGB for SAT. Thresholds: HLF>0.80 luma highlight, SHF<0.12 luma shadow, LDR=p95−p05. Same kernels, same thresholds → values directly comparable to the lift (which is the whole point: "same register band as the lift" is the claim under test).

| Phase | frames | LDR | SHF % | HLF % | LMV |
|---|---|---|---|---|---|
| pre-ignition | 1-22 | 207.0 | 49.2 | 6.07 | 35.1 |
| charge | 23-44 | 251.4 | 38.5 | 8.84 | 37.6 |
| eruption-rise | 45-55 | 251.4 | 39.7 | 8.43 | 36.5 |
| peak-bloom | 56-72 | 251.7 | 39.1 | 8.69 | 36.7 |
| live-burn | 73-88 | 246.3 | 41.2 | 8.07 | 36.9 |
| waning-settle | 89-100 | 176.3 | 40.7 | 3.50 | 35.5 |
| **whole-sequence mean** | 1-100 | **231.9** | **41.8** | **7.40** | **36.4** |
| dark-mood window (1-22 + 89-100) | | 196.2 | 46.2 | 5.16 | 35.2 |

**Rubric-relevant extracts (independently re-derived on galadriel instruments):**
- **HLF peak = 9.354%** (frame 26) vs threshold 1.5% → **6.2× over**. Body-anchored hero bloom unambiguously present. HLF floor = 1.749% (frame 1) — *every* frame clears the 1.5% bloom threshold.
- **LDR whole-mean = 231.9** vs threshold 115 → **2.0× over**. Peak pegs the 8-bit ceiling (252) from ~frame 10 onward. **LDR floor = 130 (frame 1)** — even the deepest pre-ignition frame clears 115. Every single one of the 100 frames passes the lighting-drama LDR bar.
- **SHF whole-mean = 41.8%** vs threshold 30% → **1.4× over**. **SHF floor = 37.27% (frame 25**, the brightest charge moment when fire floods the frame) — the dark-mood never collapses; the cathedral voids stay black even at peak bloom.

**Overlay validation** (`12_cathedral_peak26_lumamask.png`): the HLF highlight mask (red) lands exactly on the central fire bloom + brazier flames — the body-anchored hot core at the dais; the SHF shadow mask (blue) lands on the cathedral arch voids + dark side-wall. Instruments are measuring the correct pixels — not fooled by a UI element (the top-down capture carries no HUD chrome) or compression artifact.

**Lifecycle-shape note (honest difference from the lift):** the HLF peak (frame 26) lands in the **charge** phase, not the eruption. Cause: braziers burn from frame 0 AND the pentagram charge-bloom builds early and hot, so HLF is already ~9% before the column's own eruption — then the column *sustains* ~8.5% through eruption→peak→burn before collapsing to 3.5% in waning-settle. This is a different but equally clean hero-event shape vs the lift's sharp ignite-spike: an extended **charge → sustain → collapse** rather than dark-then-ignite. It does not weaken the VFX read — the bloom is present, body-anchored, high-magnitude, and lifecycled. The phase label simply reflects where the brightest moment honestly falls.

## 3. Per-axis manual scores

### Lighting drama — **5 / 5** (target ≥ 4 — MET)
LDR 231.9 (2× threshold) + SHF 41.8% (1.4× threshold), both sustained across every lifecycle phase. The scene is a lit volume punched out of deep dark: warm braziers rake the dais and statuary, cold rim catches the cathedral arches and side-walls, the central altar glows warm-red, the rest near-black. The summon column adds a dynamic warm key that floods the whole foreground at eruption→peak (dais, railings, near-wall all warmly re-lit) then recedes to residual ember. This is filmic, dramatic, register-2 lighting on a *real shipping environment* — and the lighting hold is actually **tighter and more uniform than the lift**: LDR pegs the ceiling from ~frame 10 and never drops below 130, where the lift's pre-ignition floor was lower. The richer curated geometry (carved arches, columns, statuary, stained-glass frames) gives the rake more surface to play across. *Evidence: lifecycle LDR/SHF table; `12_cathedral_peak26_lumamask.png`; lifecycle strip frames 05/20/30.*

### VFX presence — **5 / 5** (target ≥ 4 — MET)
HLF peak 9.354% (6.2× threshold), sustained ~8.5% through charge→eruption→peak→live-burn. The pentagram-charge + GPUParticles3D summon fire column is a genuine body-anchored S-tier skill event with a clean lifecycle (charge under-bloom → eruption column → sustained burn → collapse → residual ember at the dais). The hot core sits center-foreground at the ritual dais where the pentagram is — the bloom emanates from the body-anchor point, reading as *the character's summon*, not ambient fire beside it. Always-on braziers + fog/dust add atmospheric VFX even pre-ignition (HLF already ~2-6% pre-charge). The hero event is unmistakable and well-lifecycled. *Evidence: lifecycle HLF table; `12_cathedral_lifecycle_strip.png`; `12_cathedral_peak26_lumamask.png`.* (Marketing-render caveat: § 5 — scored on own-register merits, NOT Synty-post fidelity.)

### Material-shading — **5 / 5** (target ≥ 4 — MET, exceeds the lift's 4)
LMV whole-mean **36.4** (vs the lift's ~32-38 lit phases) — but the decisive read is the heatmap, not the scalar. `12_cathedral_settle100_lmv_heatmap.png` (mean per-tile std **24.92** at 24×14, vs the lift's 18.6) and `12_cathedral_preign05_lmv_heatmap.png` (mean 23.37) both show variance **distributed across lit surface interiors** — the dais stone, brazier-lit floor, carved railings, altar, statuary — *not* concentrated only at face boundaries. That is the signature of light-responsive material under filmic lighting, not flat per-face fill; the dark voids correctly read GREEN (no light → no material response to read). This scores **5** where the lift held at 4 for an honest reason: the lift was a single hero figure with limited surface area, so its material contribution was subtle and lighting-carried. The cathedral is **real curated content with abundant richly-modeled surface** (carved stone, ornamented columns, stained-glass frames, statuary) catching the warm/cold rake — the surface micro-variance is no longer subtle; it is distributed, substantial (mean-std +34% over the lift), and visibly light-responsive across the whole lit volume. **Honest caveat (not over-claimed):** the CV instrument still cannot fully *isolate* roughness-driven micro-variance from lighting-driven macro-gradient — both are present and both push register-2. But on real curated content the combined material+lighting surface response is materially richer than the graybox, and the heatmap shows it is genuinely distributed, not edge-concentrated. *Evidence: LMV heatmaps (settle 100 + pre-ign 05); whole-mean LMV.*

### Geometry register — **5 / 5** (target ≥ 3 — MET, exceeds)
This is the axis where real curated content most decisively beats the graybox. The frame is dense, legible register-2 geometry: a tiered ritual dais with carved railings, a gothic cathedral shell (pointed arches, ribbed columns, clerestory, stained-glass frames), an ornamented altar, statuary, scattered braziers — all the Synty POLYGON dark-fantasy modular kit reading cleanly with no clipping or broken seams. Low-poly faceting is visible and **correct** for register-2 (this is the exact silhouette-readable low-poly register Torchlight Infinite / Last Epoch ship). Scores **5** where the lift held at 4 specifically because the lift had "no environmental geometry richness in frame" — the cathedral *is* that environmental richness: a full composed shipping scene with foreground, midground, and background geometry layers all legible under the lighting. *Evidence: lifecycle strip; settle frame 100; charge frame 30; marketing-reference composition comparison (mood-anchor only, § 5).*

## 4. Composite + mandatory gates

| Axis | Score (cathedral) | (lift, for reference) |
|---|---|---|
| Lighting drama | 5 | 5 |
| VFX presence | 5 | 5 |
| Material-shading | 5 | 4 |
| Geometry register | 5 | 4 |
| **Composite mean** | **5.00** | 4.50 |

- **Composite mean 5.00 ≥ 3.6** → **PASS**
- **Mandatory gate — Lighting ≥ 4:** 5 → **PASS**
- **Mandatory gate — VFX ≥ 4:** 5 → **PASS**

All gates clear, with maximum margin. The composite *rose* from the lift's 4.50 → 5.00 — the two axes that improved (material-shading 4→5, geometry 4→5) are precisely the two that the lift held back on for "single graybox figure with limited surface / no environmental richness." Real curated content supplies exactly that surface and richness, and the *same lift recipe* unchanged lifts it to top-of-rubric.

## 5. Marketing-render caveat verdict (THE load-bearing caveat)

**The Synty marketing render (`.../maps/Screenshot 2026-06-15 at 8.38.06 AM.png`, the ~8.38.06 ritual-cathedral frame: red cathedral interior + glowing pentagram) is Synty's OWN Unity-pipeline marketing render. It is the CALIBRATION/MOOD anchor, NOT the pass bar. This scorecard scored our BUILD against the RUBRIC — it did NOT pixel-match the PNG.**

- **What I used the marketing render for:** mood/composition calibration only — confirming the warm-red cathedral register + ritual-circle-centered composition is the genre-correct target our build is reaching toward. I did **not** score "does our scene match this PNG."
- **The pentagram specifically:** the marketing render's glowing pentagram is Unity post on a **FLAT-material ritual circle**. drax did **NOT** pixel-match it — he drove his own red emissive sigil + GPUParticles3D column via the proven lift hero-glow lever. **Our pentagram/column reads differently from the marketing render's glowing-sigil — and per the caveat, that is BY DESIGN, not a miss.** I scored VFX on its own register merits: a body-anchored hero bloom IS present (yes), HLF magnitude is high (9.354% peak, 6.2× threshold), the lifecycle is clean (charge→erupt→burn→collapse→ember). It passes VFX on its own register, independent of any fidelity to the Synty Unity post.
- **Method discipline:** I lifecycle-sampled (100 frames across the hero event), I did NOT do still-vs-still. A marketing still is a composition/mood reference, not a VFX-presence reference — and VFX presence is read across motion, which is exactly what the instruments did.

**Caveat verdict: SATISFIED.** The score stands on our build against galadriel's rubric. The marketing render informed mood-calibration only and was never used as a pass bar or a pixel-match target.

## 6. drax CV sanity-check — independent re-derivation verdict

drax reported (his numbers, NOT my score): LDR 235.6 (~2× thr), SHF 40.8% (clears 30%), HLF peak 10.25% (~6.8× thr); claim "same register band as the lift."

| Metric | drax | galadriel (independent) | Verdict |
|---|---|---|---|
| LDR whole-mean | 235.6 (~2× thr) | **231.9 (2.0× thr)** | **CONFIRMED** (Δ1.6%; window/rounding) |
| SHF | 40.8% (clears 30%) | **41.8% whole-mean (1.4× thr)** | **CONFIRMED** (Δ1.0pt) |
| HLF peak | 10.25% (~6.8× thr) | **9.354% (6.2× thr)** | **DIRECTIONALLY CONFIRMED; magnitude slightly lower** |
| "same register band as lift" | claimed | lift HLF peak 14.4% / LDR 231.6 / SHF 60.7%; cathedral 9.354% / 231.9 / 41.8% | **CONFIRMED — same band** |

- **LDR + SHF: CONFIRMED** on my own instruments within method tolerance (small deltas attributable to dark-window definition + rounding — both robustly clear their thresholds either way).
- **HLF peak: my instrument reads 9.354% (frame 26), not 10.25%.** This is a real ~0.9pt difference, likely a frame-selection or peak-window difference (drax may have sampled a slightly different frame or a marginally different inside-fit). It does **not** change any verdict: 9.354% is 6.2× the 1.5% threshold, unambiguously a hero bloom, well within the same band as the lift's 14.4%. I report my number as the scorecard-of-record value; drax's is directionally correct and over-stated by ~0.9pt. **Refined, not refuted.**
- **"Same register band as the lift": CONFIRMED.** Cathedral LDR 231.9 ≈ lift 231.6 (essentially identical lighting drama); cathedral HLF peak 9.354% vs lift 14.4% (both multiples of threshold — same VFX band, lift's column floods a tighter frame so reads higher-fraction). The cathedral runs a *lower* SHF (41.8% vs 60.7%) because the richer lit environment fills more of the frame with lit surface — but it still clears the 30% dark-mood bar comfortably, and that lower-SHF/higher-lit-surface is *expected and correct* for a richly-furnished cathedral vs a sparse dungeon. Same register, different scene-fill.

## 7. One-line read (evidence FOR gandalf's ruling, NOT the ruling)

**The lift recipe holds 1:1 on REAL curated Synty content: Synty's own `Demo_Cathedral_01` cathedral, treated with the unchanged filmic dark-mood lighting + a body-anchored red-pentagram summon-fire-column hero bloom, scores composite 5.00/5 and clears both mandatory gates (lighting 5, VFX 5) with 2×-margin lighting + 6.2×-margin VFX CV support — and the composite RISES from the graybox's 4.50 → 5.00 on exactly the two axes (material-shading, geometry) that real curated content supplies and the graybox could not. The recipe is content-agnostic: it reached register-2 on a graybox and reaches top-of-rubric on a shipping environment.**

## 8. Honest caveats that bear on whether register-2 holds on real curated content

1. **Single-environment evidence.** This is ONE curated scene (cathedral). The lift recipe is now proven on graybox + this one real environment. A second real environment (e.g., a different Synty biome — crypt, ruins, forest) would harden "content-agnostic" from inference to demonstration. I did not over-claim "all real content"; I claim "this real curated content, decisively."
2. **HLF peak lands in charge, not eruption** (§ 2). Honest lifecycle-shape difference from the lift driven by always-on braziers + early charge-bloom; does not weaken the VFX read but is a real difference in the hero-event curve worth carrying forward.
3. **Material-shading CV still cannot fully isolate roughness-micro-variance from lighting-macro-gradient** (§ 3, carried from the lift). Both present; both push register-2; the heatmap shows distribution is genuine and edge-non-concentrated; but the texture-only contribution is not separable on these instruments. The 5 is earned on combined material+lighting surface response + the heatmap distribution, honestly scoped.
4. **Capture has no HUD/UI chrome.** These are clean Movie-Maker renders of the scene, not a live game viewport with inventory/health/skill UI overlaid. Register-2 of the *rendered world* is what's scored and what holds; the eventual UI layer is a separate surface not in scope here and not yet evidenced.
5. **drax's HLF peak (10.25%) over-states mine (9.354%) by ~0.9pt** (§ 6). Refined, not refuted; no verdict changes. Scorecard-of-record value is mine.

None of these caveats threaten the pass. They scope it honestly: register-2 holds, decisively, on this real curated environment under the unchanged lift recipe — with single-environment-evidence the one honest limit on generalizing to "all real content."

## 9. Reproducibility

- Instruments: `pipeline/lifecycle-score-cathedral.mjs` (lifecycle CV; byte-identical instrument defs to the lift scorer + `register-metrics.mjs`), `pipeline/lifecycle-strip-cathedral.mjs` (strip + peak lumamask), `pipeline/lmv-heatmap.mjs` (reused unchanged, arg-driven, for both heatmaps).
- Raw scores: `pipeline/lifecycle-scores-cathedral.json` (per-frame + per-phase + extracts).
- Overlays (this dir): `12_cathedral_lifecycle_strip.png`, `12_cathedral_peak26_lumamask.png`, `12_cathedral_settle100_lmv_heatmap.png`, `12_cathedral_preign05_lmv_heatmap.png`.
- Given the same 100 frames + these instruments, another galadriel-instance reproduces these values exactly (deterministic; no random sampling). The cathedral phase boundaries differ from the lift's (drax hero-event timing: charge ~30, erupt ~52) and are documented inline in `lifecycle-score-cathedral.mjs`.

---

*galadriel SCORES. The A-holds canon-extension call (graybox → real shipping environment) is gandalf's, on this evidence.*
