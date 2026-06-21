# Enchanted-Forest Ravine (CARVED, Revision 1) — galadriel CV Scorecard

**Status:** CV LEG of the 3-reviewer tripod gate (galadriel CV pipeline / drax builder self-score / gandalf §1·§4 human read) → Matt Gate. The whole carve is HELD for the Matt Gate; this scorecard is committed, not pushed.
**Authored:** 2026-06-21 by galadriel.
**Scoring target:** `agentic_orchestration/research/knowledge/arpg-level-design/2026-06-20-enchanted-forest-target-aesthetic-rubric.md` (§5 weighted, GPT-5.4 vision read of the official POLYGON Enchanted Forest marketing render). Same rubric as the at-grade score.
**Baseline / method reference:** `agentic_orchestration/galadriel/reports/2026-06-20-enchanted-forest-ravine-atgrade-cv-scorecard.md` (at-grade pre-carve: composite **0.94**, **0/10** §6 auto-fails).
**Frame set:** `reincarnated-godot/harness_logs/ravine_carved_2026-06-21/` — the scene CARVED into a gorge then Revision-1-corrected (added a slightly-blue sky sliver + a sun FILL light to lift the gorge floor out of murky-black).
**Gameplay frames scored (drive composite + §6):** `00_committed`, `01_pool1`, `02_reveal`, `03_pool2`, `04_downgorge`, `05_lookback`, `10_carve_floor_downgorge`.
**Diagnostic frames (scored SEPARATELY, NOT in composite):** `06_carve_up_pool1`, `07_carve_up_pool2` — camera aimed UP the shaft to prove the sky-sliver depth-hierarchy read; their higher brightness is excluded from the gameplay composite by design.
**Gate threshold:** composite ≥ 0.75 AND zero §6 auto-fails.
**Method + raw measures:** `agentic_orchestration/galadriel/pipeline/enchanted-forest-rubric-score-carved-r1.mjs` (+ `.json`). No silent transformation — raw captures untouched.

---

## CV method (reproducible; identical M1–M7 to the at-grade score, plus R1 register-survival measures)

All frames decoded native-res via `sharp .raw()` (RGB, alpha dropped). M1 palette HSV-bucketing, M2 emissive fraction (strict V≥0.78 ∧ S≥0.35 ∧ green/cyan/amber hue), M3 value distribution (Rec.709 luma), M4 fog gradient (banded Sobel), M5 vegetation/silhouette edge density, M6 cool/warm balance, M7 saturation character. **Added for the R1 register-survival question:**

- **Per-frame VALUE MEDIAN** (Rec.709 luma, 0–1) — does the base still sit in the rubric's ~5–20% dark-first band after the sun-fill add?
- **Per-frame EMISSIVE p99** (luma of emissive-classified pixels) — do glow elements remain the brightest things in frame?
- **Lit-from-within delta** = emissive p99 − value median — the magnitude of the internal-glow read over the dark base.
- **Relaxed-glow probe** (V≥0.45 ∧ S≥0.30 ∧ green/cyan hue) — a sidecar to catch the carved scene's *diffuse* trough/pool glow, which is softer/cooler than the at-grade lime hotspots (disclosed below, not hidden).

### Gameplay aggregate (mean across the 7 gameplay frames)

| Measure | Carved R1 | At-grade baseline | Rubric target |
|---|---:|---:|---|
| **Value median (luma)** | **0.096** | (n/a — added this run) | §2: base ~5–20% value → 0.05–0.20 |
| **Emissive p99 (luma)** | **0.698** | (n/a — added this run) | hotspots spike 80–100%, small-area |
| **Lit-from-within delta** | **~0.60** (on emissive-bearing frames) | — | glow brightest over dark base |
| Enchanted-family pixel fraction | **99.9%** | 95.7% | dominant cool teal/green/cyan |
| Neutral-gray fraction | **0.007%** | 0.0002% | near-zero |
| Off-target (gray+offtarget) | **0.04%** | 0.6% | near-zero |
| Cool / warm fraction | **99.9% / 0.0004%** | 94.8% / 0.87% | cool-dominant, warm subordinate |
| Value: shadow / mid / upper / spike | **90.6% / 7.7% / 1.7% / 0.0003%** | 53.7% / 34.8% / 8.3% / 3.1% | shadow-heavy; spike small |
| Emissive total (STRICT V≥0.78) | **0.08%** | 6.6% | §2: 5–15% |
| Relaxed-glow fraction (V≥0.45, green/cyan) | **4–12%** on hero frames | — | the diffuse trough/pool glow the eye reads |
| Mean saturation (non-shadow) | **0.86** | 0.90 | moderately-to-highly saturated |
| Global edge density | **0.015** | 0.052 | packed |

### Per-frame register-survival table

| Frame | medV | emisP99 | litΔ | shadow% | spike% | ench% | gray% | relaxed-glow% |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 00_committed | 0.100 | 0.708 | 0.608 | 85.3 | 0.000 | 99.8 | 0.030 | 12.4 |
| 01_pool1 | 0.129 | 0.543 | 0.415 | 88.2 | 0.000 | 100 | 0.011 | 9.4 |
| 02_reveal | 0.079 | — | — | 98.1 | 0.000 | 100 | 0.000 | 1.1 |
| 03_pool2 | 0.068 | 0.745 | 0.677 | 86.1 | 0.000 | 100 | 0.000 | 7.1 |
| 04_downgorge | 0.086 | 0.699 | 0.613 | 94.7 | 0.000 | 100 | 0.000 | 4.9 |
| 05_lookback | 0.090 | — | — | 99.6 | 0.000 | 100 | 0.000 | 0.0 |
| **10_floor_downgorge** | 0.121 | **0.793** | 0.672 | 82.3 | 0.000 | 99.8 | 0.006 | 4.1 |
| *06_up_pool1 (DIAG)* | *0.128* | *—* | *—* | *98.3* | *0.000* | *100* | *0.000* | *—* |
| *07_up_pool2 (DIAG)* | *0.146* | *0.891* | *0.745* | *76.9* | *0.0001* | *100* | *0.000* | *—* |

---

## THE CRITICAL QUESTION — R1 register-survival verdict

Revision 1 added a slightly-blue sky sliver + a sun FILL light. The risk: this breaks the locked EMISSIVE-LED register (dark-first / lit-from-within). The CV says it did **not**.

1. **Base value still dark-first.** Gameplay value median **0.096** — dead-center in the rubric's ~5–20% band. Every gameplay frame sits 0.068–0.129. Shadow fraction is **90.6%** — the carve made the scene *darker* than the at-grade build (53.7%), not flatter. The sun fill lifted the floor *off pure black* (no gameplay frame medians below 0.068) without raising the base out of the dark band. **PASS.**

2. **Emissive hotspots remain the brightest elements.** Emissive p99 **0.698** against a base of 0.096 → a lit-from-within delta of **~0.60** on every emissive-bearing hero frame (00/03/04/10). The brightest single gameplay element is the green trough current in `10_floor_downgorge` at p99 **0.793**. The sun fill did NOT wash out or out-brighten the glow — the glow is still the apex of the value range. **PASS.**

3. **Spike (>0.80 value) ≈ zero (0.0003%).** No daylight washout, no white-bloom flooding. The sun fill is a *fill*, not a key — it never drives any pixel into the daylit-spike band.

4. **Neutral-gray near-zero (0.007%), enchanted-family 99.9%.** The palette is *cleaner* than at-grade (99.9% vs 95.7%). The blue sky-sliver tint reads as cool teal/blue family, not neutral daylight gray. **PASS.**

### REGISTER-SURVIVAL VERDICT: **SURVIVED.**

The numbers behind it: value median 0.096 (in-band), shadow 90.6% (deepened, not flattened), emissive p99 0.698 with lit-Δ ~0.60 (glow is the apex), spike ~0%, gray 0.007%. The dark-first / lit-from-within register is intact. The R1 sun fill did its job — it lifted the floor out of murky-black readability-death **without** breaking the emissive lead.

**One honest character-shift (disclosed, scored, not hidden):** the *emissive* read migrated from the at-grade build's punchy high-V lime mushroom-cap hotspots to the carved build's **diffuse, cooler teal/cyan glow** off the trough current + large pool surfaces. The strict V≥0.78 emissive count collapses (6.6% → 0.08%) because the carved glow is softer and cooler than the lime caps — but the relaxed-glow band (V≥0.45, saturated green/cyan) catches **4–12%** of frame on the hero shots, which is the glow the eye actually reads, and the lit-from-within delta confirms it is still the brightest element. So: the register survived, but the emissive CHARACTER softened from hot-spotted-multi-hue toward diffuse-cool. That is a real, scoreable shift — it dents the emissive-presence dimension (below), it does NOT auto-fail.

---

## §5 Per-dimension scorecard (gameplay frames)

| # | Dimension | Wt | Score | Wt·Score | Evidence |
|---|---|---:|---:|---:|---|
| 1 | Overall palette match | 14% | **0.94** | 0.1316 | Enchanted families 99.9%, gray 0.007%, off-target 0.04%, cool 99.9%. Cleaner than at-grade. −0.06: amber essentially absent now (warm 0.0004%) — the carve put the warm mushroom caps out of frame. |
| 2 | Emissive magic presence | 12% | **0.80** | 0.0960 | Glow present + dominant (litΔ ~0.60; trough+pools brightest, relaxed-glow 4–12% on hero frames). −0.20 vs at-grade 0.90: emissive CHARACTER softened from punchy multi-hue lime caps to diffuse teal/cyan; only 1/7 frames carries ≥2 strict-emissive hues; 02/05 carry no hero glow. Real read, softer than ideal. |
| 3 | Lighting structure | 10% | **0.95** | 0.0950 | 90.6% deep-shadow, spike ≈0%, glow-led low-key. The R1 fill is a true fill (no spike-band intrusion). Textbook lit-from-within; the strongest dimension of the set. |
| 4 | Fog/atmospheric depth | 10% | **0.80** `[MANUAL+CV]` | 0.0800 | Background blue-shift + contrast-loss with depth visibly present (00/02/04/05); gorge depth read aided by the carve. bgFg edge ratio 0.58 (fg now busier than bg — consistent with depth fade). −0.20: still moderate, no hard god-ray shafts. Lifts +0.08 over at-grade — the carve deepened the haze read. |
| 5 | Vegetation density | 10% | **0.72** `[MANUAL+CV]` | 0.0720 | Rim/ledge vegetation + cyan mushroom clusters read at pool bases (01/03/10). −0.28: the carve traded the at-grade's packed margins for large dark gorge-wall masses; edge density dropped 0.052→0.015. Walls are intentionally clean rock, but the §5 "most of frame covered" ideal is now more partial. The gorge floor of 10 carries the best density (combatants + mushroom clusters + trough). |
| 6 | Mushroom signature | 10% | **0.85** `[MANUAL]` | 0.0850 | Cyan/blue bioluminescent mushroom clusters at cliff/pool bases (01/03/10); the Pool-2 green hero mushroom reads in 03. −0.15 vs at-grade 0.95: the warm amber-cap mushrooms are largely out-of-frame in the gorge framings; the signature is now cool-dominant. Present + prominent, less varied. |
| 7 | Composition enclosure | 9% | **0.96** `[MANUAL]` | 0.0864 | The carve is a pure win here. Dark gorge walls frame every gameplay frame; the sky sliver reads as a thin band (02/05), not an open sky. Maximally enclosed ravine-chamber feel. +0.06 over at-grade. |
| 8 | Depth-plane readability | 8% | **0.86** `[MANUAL+CV]` | 0.0688 | ≥4 planes legible in 00/02/04/10 (fg wall → near platforms/pools → glowing trough → hazy gorge-depth + sky sliver). The carve's sky-sliver depth anchor (proved by the DIAG frames) strengthens the read. 05_lookback is the flattest (dark dune fg dominates). +0.04 over at-grade. |
| 9 | Ravine/vertical layering | 8% | **0.92** `[MANUAL]` | 0.0736 | This is the whole point of the carve and it lands. Stacked gorge walls + pool ledges + the down-gorge descent (04/10) create genuine stacked vertical-traversal feel over the luminous trough. +0.22 over at-grade 0.70 — the deferred lift the at-grade score predicted has arrived. |
| 10 | Cool-vs-warm accent balance | 7% | **0.74** | 0.0518 | Cool 99.9%, warm 0.0004%. −0.26: warm has functionally vanished in the gorge framings — the amber spot-contrast the rubric wants is essentially gone. The base is gorgeously cool, but the warm-against-teal contrast pop the §3-SUPPORTING line calls for is the weakest it has been. Flagged for drax: a single warm mushroom cap in-frame would restore it. |
| 11 | Particle/micro-magic detail | 6% | **0.82** `[MANUAL]` | 0.0492 | Spore/firefly motes visible in 01/03/10 (scattered light dots); 10_floor_downgorge shows the clearest air-mote field (white/blue dots across the gorge top). +0.04 over at-grade — the dark gorge backdrop makes the motes read more clearly. |
| 12 | Low-poly silhouette/style fidelity | 6% | **0.95** `[MANUAL]` | 0.0570 | Clean faceted Synty silhouettes throughout; flat stylized material response; the carved gorge walls are clean low-poly facets, no realistic high-freq texture. POLYGON Enchanted Forest reading true. |

### Composite

**Σ (weight × score) = 0.8464 → composite = 0.85.**

(Per-dimension weighted contributions: 0.1316 + 0.0960 + 0.0950 + 0.0800 + 0.0720 + 0.0850 + 0.0864 + 0.0688 + 0.0736 + 0.0518 + 0.0492 + 0.0570 = 0.8464.)

---

## §6 Anti-pattern check (auto-fail signals) — gameplay frames

| Signal | Verdict | Evidence |
|---|---|---|
| Flat even daylight / clear-sky sun | **PASS** | Value median 0.096, shadow 90.6%, spike ≈0%. The R1 sky sliver reads as a thin cool band (02/05), NOT an open daylit sky. The sun fill never drives a daylit spike. Reads nocturnal/enchanted. |
| No visible emissive glow | **PASS** | Emissive p99 0.698, lit-Δ ~0.60; relaxed-glow 4–12% on hero frames. The green trough + cyan pools are unambiguously the brightest elements. Glow present and dominant. |
| Sparse vegetation / empty ground | **PASS** (closest call) | Rim/pool-base vegetation + mushroom clusters present (01/03/10). Edge density dropped to 0.015 and gorge walls are large clean masses — this is the nearest §6 call, but the walls are *intentional carved rock*, not undecorated dressing-failure; the populated gorge floor (10) and pool ledges carry the density read. Passes; flagged in residuals. |
| Open meadow / generic forest | **PASS** | Maximally enclosed gorge chamber; the carve strengthened this. No skyline beyond the thin sliver. |
| Missing oversized mushrooms | **PASS** | Cyan bioluminescent clusters + the Pool-2 green hero mushroom read across 01/03/10. Cool-dominant now, but present and prominent. |
| No atmospheric fog/haze | **PASS** | Background blue-shift + contrast-loss visibly present (00/02/04/05); gorge-depth haze reads. |
| Neutral gray/brown dominance | **PASS** | Gray 0.007%, off-target 0.04%, cool 99.9%. The opposite of gray/brown. |
| Hard realistic materials/textures | **PASS** | Clean faceted low-poly Synty throughout, including carved gorge walls. |
| Urban/man-made/metallic/concrete props | **PASS** | Pure organic biome; no metallic/concrete. (Named prior-run gold-metal failure absent.) |
| Overbright white-bloom washout | **PASS** | Spike pixels 0.0003% — concentrated emissive hotspots, zero scene-wide washout. The R1 fill did NOT introduce bloom. Color separation fully intact. |

**§6 result: 10 / 10 PASS — zero auto-fails.**

---

## Strongest dissonances (top, with recommendations for drax)

1. **Warm-vs-cool contrast has collapsed (dim. #10 → 0.74; warm 0.0004%).** The gorge framings put every warm amber mushroom cap out of frame; the rubric wants warm present-but-subordinate as spot contrast. *Recommendation:* place one warm amber-lit mushroom cap inside at least the hero gorge-floor framing (10) and the reveal (02) — restores the §3-SUPPORTING amber-against-teal pop without threatening the cool dominance.
2. **Emissive character softened diffuse (dim. #2 → 0.80).** The glow survived (it IS the brightest element) but lost the punchy multi-hue lime-cap read; only 1/7 frames carries ≥2 strict-emissive hues, and 02/05 carry no hero glow at all. *Recommendation:* if a punchier read is wanted, raise the trough-current emissive value (toward V≥0.78) at the hero pool moments (03/10) so the strict-emissive band re-populates — but this is taste-tier, not a gate blocker.
3. **Vegetation density dropped on the gorge walls (dim. #5 → 0.72; edge 0.052→0.015).** The clean carved walls trade packed-margins for large dark masses. *Recommendation:* spill vegetation / hanging roots over the upper gorge ledges (the §3-SUPPORTING "hanging vines/roots bridging the ravine" line) to re-pack the wall planes without cluttering the combat floor.

## Gaps / absences (findings, not scores)

- **02_reveal and 05_lookback carry no hero emissive** — they are legitimately transition/look-back framings (gorge wall + sky sliver + dark dune). They hold the dark-first base and the enclosure read but contribute no glow; they pull the emissive-presence mean down. Not a defect — a framing-purpose distinction. The eye-level hero frames (00/03/04/10) carry the emissive load.
- **Diagnostic frames (06/07) behave exactly as intended** — see below.

---

## Diagnostic frames — scored SEPARATELY (NOT in composite)

`06_carve_up_pool1` and `07_carve_up_pool2` are camera-aimed-UP-the-shaft depth-hierarchy proofs, not gameplay framings. Their job is to prove the sky-sliver-over-dark-gorge depth read; they are correctly brighter (value median 0.128 / 0.146 vs gameplay 0.096) because they point at the lit sliver.

- **They prove the depth hierarchy:** 06/07 show the gorge-wall-to-sky-sliver value gradient cleanly (07's bgFg edge ratio 3.25 — sharp background structure up the shaft); 07 also catches the green hero mushroom (emisP99 0.891). The sky sliver reads as a discrete bright band at the top of a dark shaft — exactly the depth anchor R1 was added to create.
- **They are correctly excluded from the gameplay composite.** Including their higher brightness would have lifted the gameplay value median (0.096 → ~0.10) and falsely flattered the dark-first read. The verdict above is computed on gameplay frames ONLY, per the gate brief.
- **They do NOT trip §6 daylight** even on their own terms: shadow still 76.9–98.3%, spike ≈0%. Even looking straight up the shaft, the sliver is a band, not an open sky.

---

## Verdict (CV leg)

- **Composite: 0.85** — clears the ≥ 0.75 gate threshold.
- **§6 auto-fails: 0 / 10** — clears the zero-auto-fail requirement.
- **Register-survival: SURVIVED** — value median 0.096 (dark-first band), shadow 90.6% (deepened), emissive p99 0.698 with lit-Δ ~0.60 (glow is the apex), spike ~0%, gray 0.007%.

**CV LEG: CLEARS THE GATE.** Composite 0.85 ≥ 0.75 AND zero §6 auto-fails AND the locked emissive-led register survived Revision 1.

The composite stepped down from at-grade 0.94 to 0.85 — and that step-down is honest and expected: the carve traded breadth for depth. It WON big on the dimensions the carve exists to deliver — ravine/vertical layering (0.70 → 0.92), composition enclosure (0.90 → 0.96), depth-plane readability (0.82 → 0.86), fog depth (0.72 → 0.80). It paid for those wins on the dimensions the gorge framings deprioritize — emissive multi-hue punch (0.90 → 0.80), mushroom variety (0.95 → 0.85), vegetation density (0.80 → 0.72), and most of all warm-cool contrast (0.88 → 0.74). None of those costs is an auto-fail; all have a clear, cheap lift path (one warm cap, a punchier trough, some wall vegetation).

### Mirror note

The Mirror was set on a deeper scene this time. The team feared the new light would open the dark and break the spell — that the blue sliver and the sun fill would turn the enchanted gorge into a daylit forest. The Mirror shows the opposite: the floor lifted just enough to be walked, and the dark held everywhere else. Ninety-one parts in a hundred of the picture is still shadow; the brightest thing the eye finds is not the sky but the green water running down the trough. The sliver is a thread of cold light at the top of a deep cut, not a sky — it tells the eye how far it has fallen, and then lets the dark take it again. The carve went down, and the register came with it.

---

*CV leg only. drax self-score (§3 signature elements) and gandalf human read (§1/§4 mood/enclosure/depth) compose the full tripod gate package for Matt. Method + raw per-frame measures committed alongside this scorecard at `pipeline/enchanted-forest-rubric-score-carved-r1.{mjs,json}`; not pushed — the whole carve is held for the Matt Gate.*
