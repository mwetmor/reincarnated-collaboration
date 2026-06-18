# MEMO — Tee-up: improving the rubric for scoring scene-creation in Godot

**Author:** gandalf (design steward). **Date:** 2026-06-18. **Type:** opportunity memo / dive tee-up — this SETS UP the dive; it is NOT the resolved rubric.
**Trigger:** Matt — *"dive into improving the rubric for scoring scene creation in godot. There is a lot of opportunity there."*
**Collaboration model:** gandalf owns the CRITERIA (what makes a scene good, calibrated to genre); galadriel owns the CV INSTRUMENT that measures it; jack-ryan can gate the methodology. This is the dual-gate discipline already in use — the rubric is its formalization.
**Why now (the empirical trigger):** the spell-VFX head-to-head just exposed the rubric's ceiling on real evidence — a scene can be GREEN-locked AND still sit below the PoE/D2 genre bar, and the rubric had **no axis that could say so**. The quality spike (the next fork Matt named) needs a genre-register measuring stick before it can climb. Build the stick.

---

## 1. What EXISTS (survey — descriptive only, no "should")

A real, working, but **ad-hoc-grown** instrument set under `agentic_orchestration/galadriel/pipeline/`.

**The static spine — `register-metrics.mjs` (6 axes, resolution/compression-robust):**
- **HFD** — High-Frequency Detail (Laplacian edge-energy/px): texture+VFX busyness
- **LMV** — Local Material Variance (per-tile luma std): flat-shaded vs richly-painted surfaces
- **LDR** — Luminance Dynamic Range (p95−p05): lighting drama (lit-volume-in-dark vs flat-lit)
- **SAT** — saturation mean+std: color-register vividness
- **HLF** — Highlight Fraction (luma>0.80): VFX/bloom/glow presence
- **SHF** — Shadow Fraction (luma<0.12): dramatic-dark atmosphere
- *(built explicitly to test the gandalf thesis: premium-feel rides texture+lighting+VFX, not polygon count)*

**Applied scorers over that spine:**
- `register2-score-descent-iter4..7` — the descent-chamber register gate (iter-versioned; drove the descent to GREEN)
- `register2-blueslab-diagnostic` — the flat-panel/cardboard tell (LMV-based: a billboard reads low-variance)
- `descent-similarity-vs-reference` — a single-number similarity vs a genre reference frame
- `descent-colorfair` / `descent-hue-balance` — palette / hue fairness
- `arch-grammar-band-probe` + `edge-regularity` — architectural coherence (piers / arcades / windows)
- `lifecycle-score-{descent,boss,cathedral,corpus}` — the establish→settle LIGHTING lifecycle (temporal-lighting)
- `lmv-heatmap` — spatial visualization of where a scene is flat vs layered
- `spell-motion-score` — the NEW 5-metric TIME-SEQUENCE instrument (energy-travel · motion-presence · hue-legibility · layering-variance · directionality), built THIS session because the static spine "cannot score a verb"

**The capture apparatus:** `capture.mjs` (Playwright / headless) + `states.json` + per-capture provenance sidecars. galadriel's own README flags v0.1 as *"the apparatus, not the analysis"* and lists a Phase-2 maturation backlog (pHash, HSV-cosine, Canny edge-density, CLIP-embedding similarity, reference-set extension). **The maturation is already self-identified — Matt's "a lot of opportunity" names the same gap.**

## 2. The rubric's current CEILING (descriptive — what it does NOT yet do)

Four structural facts about the instrument as it stands:

1. **Its ceiling is "coherent," not "genre-register."** The axes score INTERNAL self-consistency (balanced LDR, fair hue, layered-not-flat, regular edges) and top out at GREEN. The head-to-head proved GREEN ≠ PoE/D2: a GREEN scene with an approved spell still sits below the genre bar, and no axis positions it ON the genre ladder. `similarity-vs-reference` is a single scalar, not a calibrated tier.
2. **It is a PASS/FAIL gate, not a quality LADDER.** Metrics fire against a threshold ("layering 8.55 AT the 9.0 flat-cardboard line"). That answers "is it flat?" — not Matt's actual question, *"where on the placeholder→D2→PoE ladder does this sit?"*
3. **Static and temporal are disjoint instruments.** The static spine scores stills; `spell-motion-score` scores verbs; they share primitives but no common scorecard. A casting hero in a chamber is BOTH and is scored holistically by neither.
4. **It grew per-iter, not per-rubric.** 60+ bespoke files (`iter2fix`, `iter3`, `iter4`…). Each gate spawned a fresh scorer; learnings don't compound into a shared axis taxonomy.

## 3. The OPPORTUNITY (the dive targets — gandalf-criteria; this is where "should" lives)

Five, in priority order:

**O1 — A genre-register CALIBRATION LADDER (the headline).** Replace "above/below a line" with a tiered position anchored to real genre exemplars scored through the SAME instrument:
- **T0** placeholder · **T1** coheres (current GREEN ceiling) · **T2** genre-competent (D2-class: readable, layered, element-legible, juiced) · **T3** genre-reference (PoE / D4-class: alpha-erosion detail, flowmap churn, HDR-bloom multi-layer composite, dramatic GI).
- Score a battery of real PoE / D2 / D4 / Last-Epoch frames through `register-metrics` + `spell-motion-score` → those become the anchored tier-marks. A Godot scene then reads as *"T1.6, where D2-fire = T2.1, PoE-fire = T2.8."* **This is the measuring stick the quality spike needs.**

**O2 — Unify the per-iter scorers into a shared rubric SPINE.** Factor the shared primitives (laplacian, LMV, hue-histogram, centroid, edge-regularity) into named AXES (composition · lighting · palette · layering/depth · motion · genre-register). Any scene-type scores as a PROFILE over the one spine — descent-gate and spell-gate become two profiles, not two codebases.

**O3 — Bridge static + temporal into one scorecard.** A scene gets BOTH its static-register profile AND (where it is a verb) its motion profile, reconciled into a single read — the chamber's composition + the cast's motion, one card.

**O4 — Encode the QUALITY-TIER question, not just presence.** Every axis reports a tier-position (vs the O1 anchors), not just pass/fail. The number answers "are we at the bar?" directly, in Matt's own terms.

**O5 — Structurally encode the dual-gate.** Pair each design CRITERION (gandalf: what makes it good) with its CV MEASUREMENT (galadriel: how we detect it) IN the rubric, so eye↔number DIVERGENCE is a first-class output (the cross-check working), not noise. This bakes the anti-confirmation-bias discipline into the instrument itself.

## 4. How the dive runs + the connection to the live thread

- **The load-bearing connection:** **O1 (the genre-register ladder) IS the measuring stick the quality spike needs.** You cannot climb to "PoE/D2 register" without an instrument that POSITIONS you on that ladder and tells you when you've arrived. The rubric dive and the spike are COMPLEMENTARY — there is a real sequencing argument that O1 lands FIRST (or alongside): build the stick, then climb, and let the climb's own frames be the first things scored on it. This also de-risks the breadth roll-out (you don't scale until the instrument confirms a kit is at-tier).
- **First concrete artifact when the dive fires (cheap, no new code):** score a genre-exemplar battery (PoE / D2 / D4 / LE fire-spell + chamber frames) through the EXISTING `register-metrics` + `spell-motion-score`, UNMODIFIED, to read where the anchors actually fall. That empirically calibrates the tier-marks before any new instrument is built — and quantifies how far the just-approved combo sits below them.
- **Scope of THIS memo:** a tee-up, not the resolved rubric. The dive itself = a Pattern-B design session (gandalf + Matt: fix the tier definitions + which exemplars anchor each tier) + a galadriel commission (build the anchored ladder + the unified spine). Next step, on Matt's steer.
- **Genre grounding for the tier design (gandalf brings):** PoE/D2/D4/Last-Epoch are not interchangeable register anchors — D2's fire is *legible-and-juiced* at a lower fidelity (a good T2 floor), PoE layers *more composable detail* (T2.8–T3), D4 leans *HDR-bloom + GI atmosphere* (T3 lighting). The ladder should anchor to the RIGHT exemplar per axis, not one blanket "AAA" reference.

---

**Signed:** gandalf, 2026-06-18. Tee-up memo for the scene-scoring-rubric dive. The rubric that drove the descent to GREEN is real and load-bearing — but its ceiling is "coherent," and the spell-VFX head-to-head proved coherent ≠ PoE/D2 genre-register. The opportunity (Matt: "a lot of opportunity there") is a genre-register CALIBRATION LADDER anchored to real genre exemplars (O1), a unified rubric spine (O2), a static+temporal scorecard (O3), tier-positioning over pass/fail (O4), and a dual-gate baked into the instrument (O5). O1 is the measuring stick the quality spike needs — build the stick, then climb. Dive fires on Matt's steer; first artifact is a no-new-code exemplar-battery calibration.
