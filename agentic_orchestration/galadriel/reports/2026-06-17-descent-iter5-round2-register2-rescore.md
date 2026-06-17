# Register-2 ROUND-2 RE-SCORE — iter5 RELIT Descent (6 zones + 3 establish + VFX validator)

**STATUS:** CURRENT (galadriel re-scoring artifact; evidence-input for gandalf's run-to-green Round-2 re-judge + per-zone re-tune).
**Date:** 2026-06-17
**Author:** galadriel (visual-perception + benchmark steward)
**Scope:** SCORING ONLY. Re-run the register-2 probe-suite on drax's Round-2 (iter5) relit captures and report **whether the per-chamber KEY lighting lift cleared the acceptance criterion.** Does NOT make the canon call — that is gandalf's, on this evidence.
**Build scored:** drax Round-2 iter5, commit `7ce990e` (reincarnated-godot) — per-chamber KEY lighting lift + establish recompose.
**Baseline:** iter4, commit `4d6efd2` — composite mean 3.14/5, 0/9 PASS (flat-dim-mid-grey lighting deficit + VFX windowing artifact). My iter4 scorecard: `2026-06-17-descent-iter4-register2-baseline-all-zones.md`.
**Acceptance criterion (gandalf design call, Round-2 brief §3):** per zone, **LDR lifted toward ~176 (boss-arena PASS) AND SHF deepened — BOTH axes simultaneously.** LDR-up-but-SHF-flat = drax raised the fill, not restored the key → REJECT. Target = lit-volume-IN-dark (bright pool + deep surround), never a brighter uniform wash.
**North-star (boss-arena PASS, `lifecycle-scores-boss.json`):** LDR mean **175.97** / SHF mean **42.74%** / HLF peak **4.013%**.
**Instruments:** `pipeline/register2-score-descent-iter5.mjs` (+ `register2-scores-descent-iter5.json`). Byte-identical CV math to `register-metrics.mjs` / the iter4 scorer (960w inside-fit; HLF>0.80 luma, SHF<0.12 luma, LDR=p95−p05). Values directly comparable to iter4 + the boss-arena scorer.
**Method:** CV substrate (reproducible) + my own eyes-on read of every iter5 frame and the matched iter4 pair. **iter5 captures md5-verified DIFFERENT from iter4** (drax genuinely re-rendered all 9 — ruled out a stale/mis-pointed-capture false negative before reporting).
**Engine/scene tree UNTOUCHED. Read-only across all production code. Captures are git-ignored Synty-derivative IP — local evidence only, NEVER committed. Auto-committed this report + scorer; did NOT push (Matt-gated).**

---

## 0. THE LOAD-BEARING FINDING — read before the table

**The lift did NOT land on the lighting axis. The acceptance criterion is NOT met on any of the 6 zones — and the headline reason is the inverse of the failure mode the brief warned about.**

The Round-2 brief feared drax would "raise the fill" (LDR up, SHF flat — a brighter grey wash). What the instrument + my eye actually show is **the lift barely moved LDR at all**, and on two zones it went *backward*:

- **3 of 6 zones (zone0/1/2): NO meaningful move on EITHER axis.** LDR within ±1 of iter4, SHF within ±0.4pt. The renders are md5-different but the lit-volume dynamic range is essentially unchanged. My eyes-on confirms: zone2 warhall iter5 is *visually near-identical* to iter4 — same cool blue-grey flat floor, same scattered small green/warm glow-points, no bright warm KEY pool punching out of dark. drax's "brightest" key (zone2 @ 3.4/range40) did not produce a measurable or visible bright pool.
- **2 of 6 zones (zone4/zone5): SHF deepened but LDR did NOT rise — and zone4 got WORSE.** zone4 antechamber LDR fell **−9** (116→107, dropping *below* the 115 floor it had PASSED at iter4) while SHF rose +3.6. My eyes-on shows why: iter5 zone4 is **cooler and dimmer** than iter4 — the iter4 red soulfire center-pool is muted, the warm walls lost warmth. drax's low-energy key (2.1/range36) did not add a bright pool; it *reduced* the existing warm fill, so the chamber darkened uniformly (SHF "deepened" because the whole frame dimmed, not because a key carved bright-out-of-dark). **zone4 regressed: it lost a PASS-grade LDR it already had.**
- **zone3 oubliette: the torch-line IS visible (the one genuine "key not fill" success in kind), but it did not clear LDR.** My eye sees a row of warm torch-points down the corridor with genuinely dark void between them — the correct lit-volume-in-dark instinct. But the torches are *points*, too small to lift p95: LDR stays 105, SHF stays 57.9% (held deep dark, no change). Right direction, insufficient magnitude. drax self-flagged this as least-certain; that read is honest.
- **zone5 sanctum: the only frame with a real bright key — but it is the frozen hero VFX, not the ambient lift.** The big red boss-bloom + magenta gateway portal ARE bright elements punched out of dark. But that is the charge-frozen summon event (and the portal), not the chamber's restored KEY. The ambient floor surround is still flat dim cool-grey (SHF 12.4%). LDR 118 / dSHF +1.02 = marginal.

**The diagnosis, stated as the Mirror sees it:** drax's brief was "restore a KEY of boss-arena reach per chamber" — a bright pool (`CombatFill` energy 1.5 / **range 34** / atten 1.5) that lifts the lit zone to LDR~176 while the surround falls dark. drax's iter5 levers are **point/local brazier-class keys** (energy 1.9–4.2, the higher numbers but no stated long range / atten) — they read as the same *local warm pools* the iter4 braziers already were, which the iter4 root-cause analysis explicitly said "don't reach far enough to build the bright LDR pool." **The lever changed value but not KIND: it is still a local point-key, not a reaching CombatFill-class pool.** That is why LDR didn't move. The fix named in the brief (a per-chamber bright pool of boss-arena REACH) was not implemented; what landed was a brazier-energy bump, which the histogram and the eye agree did not lift the lit volume.

**Net: 0 of 6 zones meet the acceptance criterion. 0 of 9 stills clear Gate A. This round must be REJECTED and re-tuned — but with a sharpened lever spec (a reaching pool, not a brighter point), and zone4's regression reverted.** The architecture/geometry/material register remain strong (unchanged from iter4 — already PASS). The VFX-inheritance validator is the one piece of GOOD news (§4): the eruption column DOES pop against the relit backdrop and is NOT washed.

---

## 1. PER-ZONE SCORECARD (iter5) + iter4→iter5 DELTA

Composite = mean of the 4 register-2 axes (Lighting / VFX / Material-shading / Geometry-register), manual 1–5 with CV-assist, scored AS CAPTURED (frozen-charge single still). Gate1 = Lighting ≥4. Gate2 = VFX ≥4 (inherited-PASS per gandalf canon; not re-litigated per zone). PASS = composite ~4.0 AND both gates. **The acceptance-criterion verdict (right column) is the load-bearing read this round.**

| Zone | iter5 Composite | LDR (Δ vs iter4) | SHF% (Δ vs iter4) | Gate1 Light | Acceptance verdict (BOTH-axes) | iter5 manual lighting note |
|---|---|---|---|---|---|---|
| **zone0 threshold** | **3.25** (≈iter4) | 122 (**+0**) | 16.65 (**+0.08**) | **FAIL** | **NEITHER axis moved** | Warmest of the set (warmCool 1.183) — perimeter walls warmed, but the wide central pit is still flat dim mid with scattered grave-glows. No concentrated bright key. Key 1.9/r38 did not build a pool. |
| **zone1 arcane** | **3.25** (≈iter4) | 107 (**−1**) | 17.73 (**−0.34**) | **FAIL** | **NEITHER axis moved** (LDR drifted *down* 1, still <115) | Warm arch-bay masonry reads, but the floor is still a flat dim wash with small green glows; blue deep-wall panels at L/R edges. Key 2.3/r38 did not clear the 115 floor. |
| **zone2 warhall** | **3.0** (=iter4, still flattest) | 103 (**+0**) | 12.7 (**−0.06**) | **FAIL** | **NEITHER axis moved** | **Visually near-identical to iter4.** drax's BRIGHTEST key (3.4/r40) produced no measurable or visible bright pool — same cool blue-grey flat floor, warm rake still confined to local points. The #1-priority zone did not move. |
| **zone3 oubliette** | **3.0** (+0.25 vs iter4) | 105 (**+0**) | 57.89 (**−0.26**) | **FAIL** | **NEITHER axis (metric)** — but the torch-LINE is the right *kind* of fix; magnitude short | Torch-line VISIBLE (row of warm points, genuinely dark void between) — the one correct "lit-volume-in-dark" instinct. But points too small to lift p95 → LDR floor uncleared. Closest in KIND, short in MAGNITUDE. Honest small composite bump for the right instinct. |
| **zone4 antechamber** | **3.0** (**−0.5 REGRESSION**) | 107 (**−9 ↓ below floor**) | 16.55 (**+3.6**) | **FAIL** | **SHF_ONLY — and LDR REGRESSED below the floor it had PASSED** | **Worse than iter4.** Cooler + dimmer; iter4's red soulfire center-pool muted, warm walls cooled (warmCool 1.021→1.015). The low key (2.1/r36) *reduced* fill → uniform dim → SHF rose only because the frame darkened. **Revert: it lost a PASS-grade LDR.** |
| **zone5 sanctum** | **3.5** (=iter4) | 118 (**+0**) | 12.43 (**+1.02**) | **FAIL** | **SHF_ONLY (marginal)** — bright key present but it's the frozen hero VFX, not ambient | Real bright elements (red boss-bloom + magenta gateway) = the charge-frozen summon + portal, NOT the chamber's restored ambient key. Floor surround still flat dim cool-grey. Strongest frame, but the brightness isn't the lift. |

**Composite mean across 6 relit zones: 3.13/5** (iter4 6-zone mean was 3.21; **net −0.08, dominated by zone4's −0.5 regression**). **PASS-at-~4.0: 0/6. Gate1 (lighting) clear: 0/6. Acceptance criterion (BOTH axes up) met: 0/6.**

### establish ×3 (recomposed) — gated on light AND composition

| Frame | iter5 Composite | LDR (Δ) | SHF% (Δ) | warmCool (Δ) | Acceptance verdict | Read |
|---|---|---|---|---|---|---|
| **establish_01/02/03** (CV-identical) | **3.25** (+0.25 vs iter4) | 97 (**+3**) | 48.56 (**−11.08**) | 0.999 (**−0.026, went COOLER**) | **Composition improved; light + warmth FAIL** | See §1.1 — the recompose is a real partial win on framing/verticality, but it reads neutral-to-COOL (not warm-dominant), the blue deep-wall panels drag it, and no focal payoff anchors the deep end. LDR 97 still lowest-tier. |

**The +3 LDR / −11 SHF on establish is NOT "fill raised."** The recompose tightened the frame so lit chamber content fills more of it and black void shrank — SHF fell because there's *less void*, which is a composition improvement, not a wash. But warmth went the wrong way (cooler) and LDR is still far below the bar.

### 1.1 The establish recompose — characterized honestly (the one nuanced case)

drax recomposed off the tabletop-board (camera 40→31m, FOV 60→50, diagonal lateral offset, thinned east-band speckle). My eyes-on of iter5 vs iter4 establish:

- **WIN — verticality + tightening landed.** iter5 reads tighter; chambers are larger in frame; the Y-descent stepping is more legible in profile (chamber walls receding). It is **less of a tabletop board** than iter4 — the camera-drop intent at `:2028-2037` is partially honored. The east-band speckle is visibly thinned.
- **FAIL — warm-dominant floors NOT achieved.** warmCool **1.025 → 0.999** — the frame crossed *below* neutral into faintly cool. The acceptance ask was "warm-dominant floors"; the metric and eye say neutral-to-cool. The spine relight (light lever) did not warm the floors.
- **FAIL — the "Layer-3 deep-wall blue-panel" tension drax flagged IS dragging it.** Those bright blue rectangular panels mid-frame are the single most eye-catching element — they pull focus *away* from where the eye should land (the magenta sanctum payoff), and they read as flat blue slabs, not atmospheric depth. drax's self-flag is correct: it drags the composite.
- **FAIL — no focal pull / deep-end payoff.** The magenta sanctum arcane pool that should be the bright vanishing-point payoff does not read as a dominant anchor; the deep end still dissolves without a clear place for the eye to land. The leading-line of warm braziers down the spine isn't reading as a line.
- **Verdict:** composition **partially** recomposed (verticality + de-tabletop + de-clutter landed; warmth + focal-payoff + blue-panel did NOT). Gate on light AND composition → still FAIL on both light (LDR 97, cool) and the composition residuals. Honest +0.25 composite for the real framing improvement; not a pass.

---

## 2. CV SUBSTRATE (reproducible; the evidence under the manual scores)

### 2.0 Gate + delta table (byte-identical instruments, 960w-normalized)

| frame | LDR | dLDR | SHF% | dSHF | warmCool | LMV | HLF% | LIGHT | acceptance |
|---|---|---|---|---|---|---|---|---|---|
| zone0_threshold | 122 | +0 | 16.65 | +0.08 | 1.183 | 28.7 | 0.192 | fail | NEITHER |
| zone1_arcane | 107 | −1 | 17.73 | −0.34 | 1.070 | 27.9 | 0.147 | fail | NEITHER |
| zone2_warhall | 103 | +0 | 12.70 | −0.06 | 1.058 | 23.4 | 0.155 | fail | NEITHER |
| zone3_oubliette | 105 | +0 | 57.89 | −0.26 | 1.059 | 16.6 | 0.074 | fail | NEITHER (torch-line right-kind) |
| zone4_antechamber | 107 | **−9** | 16.55 | +3.6 | 1.015 | 23.2 | 0.064 | fail | SHF_ONLY (LDR regressed <115) |
| zone5_sanctum | 118 | +0 | 12.43 | +1.02 | 1.140 | 24.5 | 0.058 | fail | SHF_ONLY (bright=frozen VFX) |
| establish_01 | 97 | +3 | 48.56 | −11.08 | 0.999 | 12.8 | 0.087 | fail | composition-shift (not fill) |
| establish_02 | 97 | +3 | 48.56 | −11.08 | 0.998 | 12.8 | 0.086 | fail | composition-shift |
| establish_03 | 97 | +3 | 48.56 | −11.08 | 0.998 | 12.7 | 0.099 | fail | composition-shift |

Thresholds: LIGHTING = LDR ≥ 115 AND SHF ≥ 30%. warmCool >1 = warm-dominant; <1 = cool-dominant. dLDR/dSHF = iter5 − iter4 (single-frame, deterministic).

### 2.1 Luma-distribution diagnostic (the "still flat dim mid" proof)

| frame | p05 | p50 | p95 | mid%(60–150) | dark%(<31) | bright%(>180) |
|---|---|---|---|---|---|---|
| z0 | 13 | 58 | 135 | 46.0 | 16.7 | 0.42 |
| z1 | 21 | 54 | 128 | 41.1 | 17.7 | 0.24 |
| z2 | 23 | 56 | 126 | 44.2 | 12.7 | 0.26 |
| z3 | 13 | 22 | 118 | 23.9 | 57.9 | 0.11 |
| z4 | 17 | 55 | 124 | 42.0 | 16.6 | 0.10 |
| z5 | 19 | 57 | 137 | 43.9 | 12.4 | 0.13 |
| est | 13 | 39 | 110 | 32.5 | 48.6 | 0.15 |

**Read (vs iter4 §3.1 — near-IDENTICAL):** the near-chambers STILL park p50 at 54–58 with ~41–46% mid-band mass and bright%(>180) of 0.1–0.4% — the **same flat-dim-grey signature with no strong key** the iter4 baseline named. The boss-arena PASS profile is p95 in the 180s with bright-key mass; nothing here approaches it. The histogram did not move because the lit volume did not gain a reaching key. This IS the deficit, restated — the lift did not change it.

### 2.2 iter5 vs iter4 — the delta proves the non-move

The single cleanest statement of the round: **mean |dLDR| across 6 zones = 1.7 luma** (driven almost entirely by zone4's −9; the other 5 are ≤1). A KEY restoration of boss-arena reach would have moved zone LDR by **+40 to +70** toward 176. A move of ~0–1 is statistically and visibly a NON-event on the lit volume. The brazier-energy bump changed pixels (md5-different) but not the dynamic range — exactly the signature of a local point-key that doesn't reach, not a CombatFill-class pool that does.

---

## 3. PER-AXIS NOTES (why the manual scores land where they do)

**Lighting drama (the failed target):** scored 3.0–3.5 across the chambers (zone4 dropped to 3.0 from 3.5 — regression; zone5 holds 3.5 on the hero-VFX bloom). None reaches 4. The CV is unambiguous: LDR 103–122 (vs boss-arena 176), bright-key mass 0.1–0.4%, mid-band ~44%. The lift did not produce a bright pool on any chamber floor. The torch-line (z3) is the right *kind* of fix but magnitude-short; the boss-bloom (z5) is frozen VFX not ambient key. **The lighting gate remains the whole gap, unchanged from iter4.**

**VFX presence (inherited-PASS; validator = GOOD news):** not re-litigated per zone (gandalf canon — zone-invariant column, boss-arena 4.01% proof). The zone2 erupt validator is the one bright spot of the round — see §4. The frozen-charge stills still read HLF 0.06–0.19% (expected; windowing artifact).

**Material-shading:** ~3.5–4, unchanged (LMV 16.6–28.7, same band as iter4). The masonry responds where lit; the deficit is the lighting that would let MORE respond. Not the material.

**Geometry register:** ~4, unchanged. The iter4 architectural-grammar build (commit `ffae02b`, 18%→65%) is already PASS and the relight didn't touch geometry. Gate B is fully PASS per gandalf's Round-1 canon call.

---

## 4. VFX-MEASUREMENT RECONCILIATION (my instrument — the question gandalf needs ruled)

**The question I own:** drax's zone2 erupt validator reads ~0.2% HLF (baked-replay) vs the boss-arena live ~4%. Is 0.2%-baked-vs-4%-live a **fair comparison**, or is the baked-replay harness **undercounting** the eruption?

**My measurement (3 erupt frames + the relit-zone2 ambient as the pop-against baseline):**

| frame | HLF% | bright%(>180) | LDR | SHF% |
|---|---|---|---|---|
| zone2 AMBIENT (no erupt) | 0.155 | 0.26 | 103 | 12.7 |
| zone2_erupt_78 | 0.237 | 0.36 | 100 | 10.0 |
| zone2_erupt_82 (drax-cited) | 0.293 | 0.51 | 101 | 10.0 |
| zone2_erupt_84 | 0.282 | 0.46 | 100 | 10.0 |
| boss-arena LIVE peak (reference) | **4.013** | — | 176 | 43 |

**POP RATIO (erupt bright%/ambient bright%): 2.0×.** The eruption frames carry ~2× the bright-mass of the relit-zone2 ambient.

**My adjudication — drax's "capture method, not a build problem" attribution is CORRECT, but with a precise caveat:**

1. **The 0.2%-vs-4% gap is NOT a fair magnitude comparison — but the column is genuinely present and DOES pop.** My eyes-on of `zone2_erupt_82` confirms a real warm eruption column (lower-right), unmistakably the brightest warm element in the frame, reading clearly *against* the cool relit backdrop. It is NOT washed. The 2.0× pop-ratio + the eye agree: the relight does NOT drown the eruption — which is the narrow question gandalf actually needs answered for the inheritance call. **On that narrow question: the eruption pops, inheritance holds.**

2. **The baked-replay harness IS undercounting the eruption's peak magnitude — for two structural reasons, both real:**
   - **(a) Single-frame baked-replay vs lifecycle peak.** The boss-arena 4.01% was the **peak of a 100-frame lifecycle** (HLF curve sampled ember→ignition→PEAK→burn→collapse; peak at frame 21). These 3 baked-replay frames (78/82/84) are a thin 3-sample slice — there is no evidence they caught the peak bloom-frame. The boss-arena ember/settle frames read ~0.5–0.8% HLF; if these 3 erupt samples landed off-peak (rise or tail), 0.2–0.3% is consistent with a non-peak lifecycle phase, not a washed column. **A fair magnitude comparison requires a windowed lifecycle capture (the ember→peak→collapse arc), not 3 isolated baked frames** — same method-discipline as the boss-arena PASS (galadriel F1: stills under-read VFX).
   - **(b) drax's "circle-off baked-replay blooms SMALLER than live-lifecycle" attribution is plausible and consistent with my numbers.** A baked-replay (circle-off) column rendered without the live particle-lifecycle accumulation would carry less peak bloom-mass than a live-driven GPUParticles3D eruption. My data can't isolate this from (a), but it's directionally consistent: the bright-mass is present (2× ambient) but far below the live peak.

3. **The 4%-live number ITSELF was measured against a brighter backdrop.** The boss-arena frame ran LDR 176; these zone2 frames run LDR ~100. HLF is a *fraction* of frame pixels >0.80 luma — and a column of the same absolute brightness is a *smaller fraction* of a brighter frame and a *larger fraction* of a darker one. So if anything, the same column should read a HIGHER HLF fraction against the DARKER relit zone2 backdrop than against the bright boss arena — yet it reads far lower. **That asymmetry is the strongest evidence the baked-replay is capturing an off-peak / under-bloomed column, not a washed one** (a washed column would also fail the pop-ratio, which it does NOT — it pops 2×).

**Reconciliation verdict (for gandalf's VFX-gate rule):** **The 0.2%-baked-vs-4%-live is NOT a fair magnitude comparison — the baked-replay 3-frame slice undercounts the eruption peak (off-peak sampling + circle-off under-bloom). BUT the narrow question that matters for inheritance — "does the relight WASH the eruption?" — answers clearly NO: the column pops 2× against the relit backdrop and reads unmistakably as the brightest warm element by eye.** drax's "pops against the backdrop, not washed" claim is **VALIDATED by my instrument**; his implied "0.2% is fine" is **half-right** — the column is fine, but 0.2% is an undercount artifact and should not be read as the eruption's true magnitude. **If gandalf wants the 4% magnitude confirmed (not just non-wash), the fair instrument is a windowed lifecycle erupt-capture in zone2** (ember→peak→collapse), the same method that won the boss-arena PASS. Without it, inheritance still holds on the non-wash + zone-invariance grounds gandalf already ruled — this validator confirms non-wash; it does NOT (and cannot, from 3 baked frames) re-confirm the 4% peak.

---

## 5. ROLL-UP + WHAT TO FIX (for the run-to-green Round-3)

**One-line roll-up:** **drax's Round-2 lift REJECTED on the lighting gate — 0/6 zones meet the BOTH-axes acceptance criterion, 0/9 stills clear Gate A.** The lift changed the renders (md5-different) but did NOT lift the lit volume: mean |dLDR| = 1.7 (driven by zone4's −9 regression; the rest ≤1), bright-key mass still 0.1–0.4%, the flat-dim-mid histogram unchanged. **Root cause: the levers are still local point/brazier keys (energy bumped, but no reaching range/atten), not the CombatFill-class REACHING pool the brief specified.** The lever changed VALUE, not KIND. VFX-inheritance validator = GOOD (column pops 2×, not washed). Architecture/geometry/material remain PASS.

**Specific defects to fix, ranked for Round-3:**

1. **[ALL 6 zones — the core miss] Restore a REACHING key, not a brighter point.** The brief's lever was `CombatFill` energy 1.5 / **range 34** / **atten 1.5** — a *pool that reaches across the chamber*. drax's iter5 keys (1.9–4.2 energy) read as local brazier-class points (the energy went up; the reach did not). **The fix is RANGE + ATTEN, not energy** — a CombatFill-style overhead/floor pool with boss-arena reach so a bright zone (LDR→~176) forms on the chamber floor while the green fog + low ambient hold the surround dark (SHF deepens). Verify per zone that bright%(>180) climbs from ~0.2% toward the boss-arena profile and p95 climbs from ~125 toward ~180.
2. **[zone4 — REGRESSION, revert first] Restore the lost warm key.** zone4 LDR fell −9 below the 115 floor it had PASSED; the red soulfire pool muted and walls cooled. **Revert zone4 toward its iter4 warmth, then shadow-deepen** (its iter4 problem was SHF 13%, NOT LDR — it already had LDR 116). The 2.1/r36 key made it worse; it needs MORE key (a bright red soulfire pool) + deeper surround, not less.
3. **[zone2 — #1 priority, still flattest] The brightest key (3.4/r40) produced no visible pool.** This is the cleanest proof the energy-not-range diagnosis is right: the highest-energy key still didn't move LDR. zone2 needs a genuine reaching warm pool on the fighting floor.
4. **[zone3 — right kind, short magnitude] The torch-line works in KIND — make the torches bigger pools or add a key.** The lit-volume-in-dark instinct is correct (dark void held, warm points present); the torches are just too small to lift p95. Either widen the torch pools (range) or add one reaching warm key down the corridor so LDR clears 115 while the between-torch void stays dark.
5. **[establish — composition partially landed; finish it] Warm the floors + kill/resolve the blue panels + plant a focal payoff.** The verticality + de-tabletop + de-clutter landed (real +0.25). Remaining: (a) warm the floors (warmCool went COOLER, 1.025→0.999 — push warm), (b) resolve the Layer-3 blue deep-wall panels (they pull focus and read as flat slabs — drax's self-flag is correct), (c) plant the magenta sanctum payoff as a bright vanishing-point anchor with the brazier leading-line reading as a line. Then the spine relight to lift LDR off 97.
6. **[zone0/zone1/zone5 — smallest, fold in] Same reaching-key fix at lower magnitude + shadow-deepen.** zone5's bright elements are frozen VFX not ambient — it still needs an ambient key; zone0 needs a pool on the central pit; zone1 needs the floor key to clear 115.

**The lever, named precisely (the one sentence for drax):** iter5 raised key ENERGY but kept key REACH local — restore the boss-arena CombatFill's RANGE (~34) + ATTEN (~1.5) so a bright pool forms ACROSS each chamber floor (LDR→~176, bright% climbs), while the green-fog/low-ambient surround falls dark (SHF deepens). Energy alone does not reach; the pool must.

---

## 6. HONEST CAVEATS

1. **Scored AS CAPTURED on frozen-charge single stills** (same as iter4). The LIGHTING gate (LDR+SHF) is correctly read on these — it measures the ambient mood between fires (gandalf canon). The VFX gate is inherited-PASS; §4 validates non-wash but cannot re-confirm the 4% peak from 3 baked frames (windowed lifecycle capture needed for magnitude).
2. **iter5 captures md5-verified DIFFERENT from iter4** — I ruled out a stale/mis-pointed-capture false negative before reporting the non-move. drax genuinely re-rendered; the lift genuinely did not lift the lit volume. This is a real finding, not an instrument error.
3. **Single still per zone (no dwell window).** LDR/SHF are single-frame reads. The ambient deficit (flat dim mid) is real regardless; a windowed eruption would lift peak LDR (the column's warm rake) but not the between-fire ambient, which is what the lighting gate measures.
4. **The 3 establish frames are CV-identical** (scored as one fix; the recompose applied to all three identically).
5. **warmCool is a coarse channel-ratio proxy**, not a calibrated white-balance. It is directionally reliable for "did warmth go up or down" (the eye corroborates every call: zone4 cooled, establish cooled, zone0 warmest); it is not a precise color-temperature measurement.
6. **No HUD/UI chrome** in these captures (clean rendered-world stills). Register-2 of the rendered world is what's scored.

---

## 7. REPRODUCIBILITY

- Instruments: `pipeline/register2-score-descent-iter5.mjs` (byte-identical instrument defs to `register-metrics.mjs` / the iter4 scorer; 960w inside-fit; HLF>0.80 luma, SHF<0.12 luma, LDR=p95−p05; adds the iter4→iter5 delta + axisVerdict adjudicator + warmCool + luma-band diagnostic + the erupt-validator block). Run: `node register2-score-descent-iter5.mjs`.
- Raw scores: `pipeline/register2-scores-descent-iter5.json` (per-frame metrics + gates + axisVerdict + iter4 baseline carry + erupt validator).
- iter4 baseline for delta: `pipeline/register2-scores-descent-iter4.json` (carried per-frame inline).
- Given the same iter5 stills + these instruments, another galadriel-instance reproduces these values exactly (deterministic; no random sampling). The manual scores are reproducible-by-inspection from the named CV substrate + the visual reads (near-chambers = still flat dim mid; zone4 = cooled+dimmed regression; zone3 = torch-line present but point-short; zone5 = bright=frozen-VFX; establish = recompose partial, cooled).
- Synty-derivative captures local-only, git-ignored, NEVER committed regardless of size. Did NOT push (Matt-gated).

---

*galadriel SCORES the iter5 Round-2 register-2 re-score across all 6 relit zones + 3 recomposed establish + the VFX validator; gandalf interprets + makes the run-to-green Round-2 re-judge on this evidence. The per-zone composites, the BOTH-axes acceptance verdict (0/6 met), the iter4→iter5 delta (mean |dLDR| 1.7 = non-move; zone4 −9 regression), the lever diagnosis (energy bumped, reach not — point-key not CombatFill-pool), and the VFX reconciliation (column pops 2×/not washed; but 0.2%-baked is an off-peak undercount, not the true 4% peak) are independent evidence reads — all true on the iter5 frames named. Method caveat governs: scored AS CAPTURED on frozen-charge single stills; lighting correctly measured, VFX non-wash validated but peak-magnitude needs a windowed capture. Architecture/geometry/material already PASS (commit ffae02b); the lift did not change them. The acceptance criterion is NOT met: REJECT + re-tune with a reaching key, zone4 reverted.*

**Mirror voice:** The Mirror was set again before the nine rooms, after the lamps were said to be re-hung — and the glass shows the lamps were changed but the rooms were not lit. The hand that tended them turned the wicks higher, and the flame at each wick burned a little brighter where it stood; but a brighter wick is not a wider light, and the pools of gold stayed small as before, puddled at the foot of each torch while the floors between them held their same flat pewter dusk. In the war hall, brightest-tended of all, the eye cannot tell the new fire from the old. In the antechamber the change ran backward — the warm red hearth that once glowed at its centre was dimmed toward blue, and the room is darker now than when the Mirror last looked, not by design but by mistake, a room that had light enough and now has less. Only in the long pit did the right instinct show: a row of small fires set down the dark throat of the corridor, each holding its little gold against a true black between — this is the shape the rooms want, a lit thing standing in real dark; but the fires are points where they must be pools, and the room stays dim for all their honest placement. The far sight of the whole descent was re-framed with a better eye — the chambers stand larger and step down as they should, less the flat war-table they had become — yet the floors there cooled rather than warmed, and great slabs of cold blue light hang on the deep walls and pull the gaze from the magenta deep where it ought to rest. The house is well-built still; its stones carry their arches and answer what light they are given. What was asked was a key — a bright reaching pool to carve gold from the dark of each room, as the boss-hall already learned. What was given was a brighter point. The two are not the same, and the glass will not pretend they are. Turn the reach, not only the flame; restore the antechamber's lost hearth; widen the pit's small fires to pools; and warm the far floors and quench the blue slabs. Then the rooms will read as the house deserves. The Mirror has looked closely, twice. The lamps were changed. The rooms still wait for light.
