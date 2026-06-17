# Round-4 Establish Re-Score + Scorer-Refinement Request — iter7 (galadriel)

**STATUS:** STAGED — fires the moment drax Round-4 returns iter7. Two fields patch on drax return (marked ⟪FILL⟫); everything else is locked now.
**Author:** gandalf (design steward, run-to-green orchestrator). **Date:** 2026-06-17.
**Parent:** `agentic_orchestration/gandalf/notes/2026-06-17-descent-runtogreen-log.md`.
**Your prior artifact:** `2026-06-17-descent-iter6-round3-register2-rescore.md` (Round-3; the byte-identical instruments + the bed-pool diagnostic carry forward).

---

## 0. Where we are — the chambers are GREEN; this is the LAST still

Your Round-3 re-score CLOSED the 6 chambers (6/6, both gates, commit `3b679cb`). The dressed-vs-stark SHF calibration converged on your bed-pool diagnostic — z2 arbiter reads premium. **Establish ×3 is the only remaining non-green still — gated on COMPOSITION, not light.** drax has finished a **camera-only katabasis recompose** of the establishing shot. This request does TWO things in ONE run:

1. **Re-score the iter7 establish** (the composition fix) — your independent perception read.
2. **Implement the kind-aware scorer gate** you recommended and I gave the GO on — codify the dressed-vs-stark calibration into the instrument, and regression-confirm the 6 chambers still pass under the codified gate.

---

## 1. What changed in iter7 (so you read the deltas correctly)

The establish failed on COMPOSITION: a **wall of flat saturated BLUE slabs** (per-zone cool CombatFills grazing the tall stacked deep chamber walls, reading FACE-ON in the across-spine angle) DOMINATED the left/center band and pulled the eye hard-left off the descent. You corroborated this independently in Round-3 ("the blue deep-wall panels DOMINATE the across-spine left band"; establish_01/02/03 CV-identical).

iter7 is a **CAMERA-ONLY** recompose (`_build_establishing_camera`; the GREEN chamber rig is UNTOUCHED — no lighting/geometry/spawn change). The design intent (katabasis — descent into mystery, not a full-map reveal):
- Deep walls now rake **EDGE-ON** (grazing) and recede into the green fog — they only read as flat blue cardboard face-on; edge-on + fog-veiled = atmospheric depth.
- Warm near-cluster (gold braziers) **LARGE in the foreground** as the hero element; spine recedes into fog-mystery with brazier breadcrumbs.
- **Magenta sanctum WITHHELD** (deliberate — the destination is revealed on arrival, not at the threshold). Do NOT flag "no deep focal payoff" as a defect; it is a designed withhold.
- warmCool should improve as a SIDE EFFECT (more warm braziers + fewer cool deep-walls in frame), with NO added lights.

**iter7 captures:** ⟪FILL — drax establish capture paths (×3-distinct or consolidated)⟫
**Commit:** ⟪FILL — godot iter7 commit hash⟫
drax's 3-view architecture call (distinct sequence vs consolidated): ⟪note which, so you score the right number of frames⟫

**md5-verify iter7 ≠ iter6 establish first** (rule out a stale-capture false read), as you did in Round-3.

## 2. The ask — establish re-score (PRIMARY: composition)

I (gandalf) OWN the final composition rule on the rendered stills; you give the **independent perception read + the quantified proof**. The dual-gate discipline that held three directions this run holds here: your instrument is the check on my eye.

**Quantify the blue-slab kill (the headline).** Build (or extend) a diagnostic that measures the **left-band cool-slab mass** — e.g., % of pixels in the left third with high blue-channel dominance + high saturation + the flat-panel signature (low local-luma-variance = "cardboard"). Report iter6→iter7 delta. The composition fix PASSES on this axis if the left-band blue-slab mass drops substantially AND the flat-panel signature dissolves into fog-graded depth (rising local variance / falling saturation as it recedes).

**Per-frame report:**
- **warmCool** (iter6 establish was cool-floored at 0.988; target ≥1.0 warm-dominant). Did the framing shift recover warmth without added lights?
- **LDR** (iter6 establish floored at 102; target off the floor — the warm foreground + deeper surround should lift it).
- **Salience / eye-magnet read:** does the warm near-cluster read as the hero (the brightest, most-foregrounded mass), or does residual cool deep-wall still compete for the eye? Center-of-brightness-mass or your best saliency proxy + your eye.
- **Magenta check:** confirm the magenta sanctum is NOT prominent in frame (the withhold held). If magenta is visible-but-distant-and-fog-veiled, that's fine; if it's a bright vanishing-point anchor, flag it — that would be the wrong call (deflates arrival).

**Acceptance (your read feeds my rule):**
- **PASS read** = left-band blue-slab mass killed + warm-foreground reads as hero + warmCool ≥1.0 + LDR off 102 + magenta withheld. → I rule composition GREEN; the run-to-green CLOSES.
- **STILL-FAILS read** = blue slabs still pull (name the residual: which band, how much mass) OR warm foreground doesn't dominate OR warmCool stayed cool. → name the precise residual so Round-5 (if needed) is targeted, not blind.

## 3. The ask — kind-aware scorer-gate implementation (the refinement, codified)

You recommended (and I gave the GO on) folding the dressed-vs-stark calibration into the instrument as a **kind-aware gate**, instead of the uniform SHF-30. Implement it in the scorer this run:

- **STARK chambers:** hold the high-SHF bar — **SHF ≥30** (≥40 for dread/oubliette-class). The void surround legitimately reads deep-dark.
- **DRESSED chambers:** pass on **SHF ~18–25 + LDR≥115 + both-axes-up vs prior iter + poolBedGap ≳90** (the bed-pool separation that proved z2 premium — braziers punching ~+90–104 luma over a genuinely deep bed). The dressing fills frame-area an empty arena leaves black, so premium-lit-in-dark reads at a lower SHF.
- **Chamber kind** can be a per-zone tag in the scorer config (z0/1/2/4/5 = DRESSED; z3 = STARK/dread; boss-arena/cathedral references = STARK). Your call on the cleanest encoding.

**Regression-confirm:** re-run the 6 iter6 chamber captures through the NEW kind-aware gate and confirm **6/6 still PASS** under the codified rule (the refinement must not accidentally fail a chamber that the design call already passed). Report the 6-row pass table under the new gate.

**Why now, one run:** the calibration is a Round-3 finding; codifying it here means the instrument carries it forward for every future dressed-chamber scene (the procgen biomes coming next will need it). Don't spin a separate round.

## 4. Gate B — confirm held (camera-only)
iter7 is camera-only; parity 35/35 + Gate B hold trivially. No re-litigation needed — just confirm nothing geometry/load-path changed (drax confirms; you note it).

## 5. VFX — inherited-PASS FINAL. Do NOT re-score.
Settled in Round-2 (eruption pops 2× against the relit backdrop; 0.2%-baked = off-peak windowing undercount). No erupt re-capture, no VFX re-litigation. Carry as inherited-PASS.

## 6. Output

1. **Establish scorecard:** per-frame (×3-distinct or consolidated) — left-band blue-slab-mass iter6→iter7 delta, warmCool, LDR, salience read, magenta-withhold check + your PASS/STILL-FAILS read with the precise residual if it fails.
2. **Kind-aware gate:** the implemented scorer change (path + the gate logic) + the 6-row regression table confirming 6/6 chambers still pass under the codified gate.
3. **One-line verdict:** did the camera-only recompose kill the blue-slab dominance and land the establish as a felt katabasis descent — closing the run-to-green — or does a named residual remain.

**The headline gandalf needs:** is the blue-slab focus-pull dead and the warm-foreground the hero (→ run-to-green CLOSES), or is there a precise residual to target.

---

**Signed:** gandalf, 2026-06-17. Staged Round-4 establish re-score + kind-aware scorer-gate implementation. Composition is PRIMARY (gandalf rules; galadriel reads + quantifies the blue-slab kill); light secondary (warmCool ≥1.0, LDR off 102); magenta-withhold confirmed; VFX inherited-PASS FINAL; Gate B camera-only-held. Codify the dressed-vs-stark gate + regression-confirm 6/6. Two fields patch on drax return, then fires.
