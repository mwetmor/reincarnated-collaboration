# Register-2 ROUND-4 — iter7 establish CAMERA-ONLY recompose re-score + KIND-AWARE GATE codification

**STATUS:** CURRENT (galadriel Round-4 artifact; the independent perception read + quantified proof on the iter7 camera-only establish recompose, AND the codification of the Round-3 dressed-vs-stark calibration into a kind-aware scorer gate). Evidence-input for gandalf's run-to-green Round-4 composition call (gandalf OWNS the final composition rule; galadriel reads + quantifies the blue-slab kill).
**Date:** 2026-06-17
**Author:** galadriel (visual-perception + benchmark steward)
**Scope:** (Ask 1) establish ×3 re-score, PRIMARY = composition (the blue-slab kill, quantified) + secondary light; (Ask 2) implement + regression-confirm the kind-aware gate. Does NOT make the canon composition call — that is gandalf's, on this evidence.
**Build scored:** drax Round-4 iter7, godot commit `965cd5d` (`_build_establishing_camera` CAMERA-ONLY recompose; the GREEN chamber rig UNTOUCHED). Establish self-measure scorer drax-committed at collab `d6d7d04` (`register2-score-descent-iter7-establish.mjs`).
**Baseline:** iter6, godot commit `9b16d39` (global-rig match; the establish FAILED on composition — blue-slab dominance). My iter6 scorecard: `2026-06-17-descent-iter6-round3-register2-rescore.md`.
**Instruments (3, all in `agentic_orchestration/galadriel/pipeline/`):**
1. `register2-score-descent-iter6.mjs` — my authoritative byte-identical iter6 instrument (Round-3-diffed; reproduced exactly this run → iter6 establish baseline LDR 102 / warmCool 0.988 confirmed).
2. `register2-blueslab-diagnostic-establish.mjs` — **NEW (galadriel), the headline:** the blue-slab-kill / katabasis-composition diagnostic.
3. `register2-score-descent-iter7.mjs` — **NEW (galadriel), Ask 2:** the codified KIND-AWARE gate (CV-substrate math byte-identical to iter6; only additions are p98/poolBedGap + the kind-aware gate).
**Method:** CV substrate (reproducible, deterministic) + my own eyes-on read of every iter7 establish frame, the stacked iter6→iter7 pair, and the left-third crops. **iter7 establish md5-verified DIFFERENT from iter6** (all 3 distinct) AND **the 3 iter7 establish frames md5-distinct from each other** (the harness camera-walk fix confirmed). Ruled out a stale-capture false read before reporting, as in Round-3.
**Engine/scene tree UNTOUCHED. Read-only across all production code. Captures are git-ignored Synty-derivative IP — local evidence only, NEVER committed. Auto-committed this report + the 2 new scorers + JSONs. Did NOT push (Matt-gated).**

---

## 0. THE HEADLINE — read this first

**The camera-only recompose KILLED the blue-slab focus-pull. The warm foreground is now unambiguously the hero. The establish lands as a felt katabasis descent. My independent read: PASS on composition; PASS on the secondary light axis. The blue-slab focus-pull is DEAD. → the establish's only remaining gate (composition) clears on this evidence, and the run-to-green CLOSES (gandalf rules the composition canon; this is my read + proof feeding it).** Separately, the kind-aware gate is codified and regression-confirmed **6/6** — the refinement preserves the Round-3 design call exactly, with falsification-tested teeth.

**The single cleanest statement of the kill — and an important honesty correction in HOW it was measured:** my first instinct was to measure a *reduction in blue-slab pixels*. That instrument was WRONG, and it told me so by contradicting my eye (it reported iter7 with MORE "blue" than iter6). I diagnosed it before reporting (no-silent-transformation discipline). Root cause: the iter6 slab is a **dark teal/cyan** tilted plane (meanRGB ~(21,64,83); blue and green near-equal; only 0.37% bright), NOT pure-blue — while the iter7 deep recession IS pure-blue and larger-area. A naive blue-pixel count therefore goes **up**, not down. **The eye does not read "fewer blue pixels." It reads a RELOCATION + a warm-foreground flip.** The correct, eye-corroborating instrument measures three things, and all three pass decisively:

| The kill, three ways | iter6 establish (FAIL) | iter7 establish (the 3 beats) | verdict |
|---|---|---|---|
| **(A) FOREGROUND warm-hero?** (NEAR-band warm% / warm:cool ratio) | 8.0% warm / ratio **2.75** | **42–45% warm** / ratio **3.46–8.74** | **flipped to warm-hero** (5.5× more warm in the foreground) |
| **(B) WHOLE-FRAME register** (warm:cool ratio) | **0.83 (cool-dominant)** | **1.20–1.26 (warm-dominant)** | **the frame inverted** cool→warm |
| **(C) COOL RELOCATION** (% of cool mass in eye-level MID band) | **85.3%** in MID (the competing slab) | **58–67%** MID, FAR-cool risen to **20–33%** | **cool moved back/down** into the receded deep |

Plus the salience read (center-of-brightness-mass): iter6's bright/warm mass was shoved to the **right third** (warm-centroid x=74%, cool slab dominating left-center — a split frame, nothing centered); iter7 centers it (center-of-brightness x=**45–50%**, warm-centroid x=**46–48%** at y=65–69% = the foreground hero position), with the top-1% brightest mean luma rising from **159 → 209–215** (the braziers became genuine eye-magnets). And the **magenta sanctum is fully withheld** — 0–1 magenta pixels, zero bright, max magenta luma 140: there is NO bright vanishing-point anchor (the correct call; a bright framed magenta would deflate arrival).

---

## 1. ASK 1 — ESTABLISH ×3 RE-SCORE (PRIMARY: composition)

### 1.0 md5 / pixel verification (ruled out false reads first)

- **iter7 establish ≠ iter6 establish** (all 3): iter7_01 `8f2e6f78…` ≠ iter6_01 `b2f5dc09…`; _02/_03 likewise distinct. Not a stale capture.
- **iter7 establish_01/02/03 md5-DISTINCT from each other** (`8f2e6f78` / `24bce946` / `497f616d`): the iter6 "CV-identical" root cause (harness grabbing cam1 six times) is FIXED — the harness now walks cam1→cam2→cam3, one grab each. Three genuinely distinct warm beats, confirmed at the byte level.
- **Zone captures iter6 vs iter7 are NOT byte-identical** (drax's commit says "byte-identical"; the md5s differ and a pixel decode shows max|Δ| 247–255 with mean-abs-Δ 0.4–1.4 and 1.4–3.7% of channels differing by >1). **This is render non-determinism, not a rig change** — drax's commit `965cd5d` touched ONLY `_build_establishing_camera` (Gate B all-clean, parity 35/35), so the zone deltas are frozen-charge frame-timing / particle / AA jitter, not geometry or lighting. Transparency note, not a defect; my Ask-2 regression therefore runs on the **iter6** zone captures (the ones already scored 6/6 in Round-3) for clean attribution of the gate logic.

### 1.1 The blue-slab kill — quantified (the headline gandalf needs)

Instrument: `register2-blueslab-diagnostic-establish.mjs` (galadriel; deterministic). COOL := blue is the max channel & clearly above red (`b===max & b-r>=15 & b>40`; the teal+blue family, the eye's "cool slab" superset). WARM := red/orange/gold dominant (`r-b>=20 & r>=70 & r>=g*0.85`; the hero brazier/floor family). Bands := vertical thirds (FAR=top/deep recession in a look-down katabasis framing; NEAR=bottom/foreground).

**(A) Foreground — is the warm cluster the hero?**

| frame | NEAR warm% | NEAR cool% | fore warm:cool |
|---|---|---|---|
| iter6_establish_01 | 8.03 | 2.92 | 2.75 |
| iter7_establish_01 HERO | **44.06** | 7.02 | **6.28** |
| iter7_establish_02 ElevatedLookDown | **44.75** | 5.12 | **8.74** |
| iter7_establish_03 GroundIntimate | **41.92** | 12.11 | **3.46** |

The iter6 foreground was dark-neutral (8% warm, and the floor falls to shadow). All 3 iter7 beats flip it to a clear warm-hero majority (42–45% warm). The hero element is established.

**(B) Whole-frame register — did it flip warm-dominant?**

| frame | frame warm% | frame cool% | frame warm:cool |
|---|---|---|---|
| iter6_establish_01 | 7.05 | 8.48 | **0.83 (cool-dominant)** |
| iter7_establish_01 HERO | 25.11 | 19.91 | **1.26 (warm-dominant)** |
| iter7_establish_02 | 25.30 | 20.72 | **1.22** |
| iter7_establish_03 | 25.86 | 21.61 | **1.20** |

The iter6 frame was overall cool-dominant (0.83). All 3 iter7 beats invert it to warm-dominant (~1.2). This corroborates the warmCool channel-ratio metric (§1.2) by an independent pixel-classification path.

**(C) Cool relocation — out of the eye-level competing band, into the receded deep**

| frame | cool FAR% | cool MID% | cool NEAR% |
|---|---|---|---|
| iter6_establish_01 | 3.2 | **85.3** | 11.5 |
| iter7_establish_01 HERO | **21.2** | 67.0 | 11.7 |
| iter7_establish_02 | **33.1** | 58.6 | 8.2 |
| iter7_establish_03 | **20.2** | 61.1 | 18.7 |

iter6 had **85.3%** of its cool mass in the eye-level MID band — that is the tilted teal slab, sitting where it competes for the gaze. iter7 drops MID-cool to 58–67% and lifts FAR-cool (the fog-veiled deep recession) from 3.2% to 20–33%. **The cool moved back and down into the deep where it reads as atmospheric recession, not a face-on focal-competitor.**

*(Secondary "cardboard flat-slab" mass per band is reported in the JSON; I flag it as the WEAKER signal — it rises in iter7 simply because iter7 has more pure-blue back-wall pixels overall, and "flat at distance" is the expected signature of a fog-graded far wall, not a defect. The discriminating signal is the RELOCATION + warm-fore flip above, not the flat-count. Honest caveat, not buried.)*

### 1.2 Per-frame light axis (secondary; my instrument reproduces drax's self-measure exactly)

| Frame | LDR (Δ vs iter6 102) | warmCool (Δ vs iter6 0.988) | SHF% | bright% | LIGHT read |
|---|---|---|---|---|---|
| **establish_01 HERO** | **124 (+22)** | **1.026 (+0.038)** | 31.88 | 0.98 | off the 102 floor; warm-dominant |
| **establish_02 ElevatedLookDown** | **119 (+17)** | **1.018 (+0.030)** | 28.45 | 0.86 | off the floor; warm-dominant |
| **establish_03 GroundIntimate** | **127 (+25)** | **1.015 (+0.027)** | 34.29 | 0.85 | off the floor; warm-dominant |

LDR cleared the 102 floor on all three (+17 to +25). warmCool flipped from 0.988 (faintly cool — the iter6 residual I confirmed in Round-3) to **≥1.0 warm-dominant on all three**, with NO added lights (a pure camera-framing recovery, exactly as designed). My fresh run reproduces drax's self-measure to the decimal — deterministic, confirmed by reproduction not trust.

### 1.3 Salience / eye-magnet read (does the warm cluster pull the eye?)

| frame | center-of-brightness x% | warm-centroid x% / y% | top-1% bright mean luma |
|---|---|---|---|
| iter6_establish_01 | 61.7 | **74.1** / 61.5 | 159 |
| iter7_establish_01 HERO | **47.7** | **48.0 / 67.2** | **215** |
| iter7_establish_02 | 49.8 | 49.7 / 68.8 | 209 |
| iter7_establish_03 | 44.8 | 46.2 / 64.9 | 209 |

iter6 was a **split frame**: cool slab pulling left-center, the warm chambers crammed into the right third (warm-centroid x=74%), no strong bright anchor (top-1% only 159). iter7 **centers the warm hero** (x≈46–48%) and drops it into the foreground (y=65–69%), and the braziers become real eye-magnets (top-1% bright 209–215). **The warm near-cluster reads as the hero; no residual cool deep-wall competes for the eye.** My eyes-on confirms it (see §1.5).

### 1.4 Magenta-withhold check — CONFIRMED (the withhold held)

Magenta := `r>=110 & b>=110 & g<min(r,b)*0.75 & (r-g)>=40 & (b-g)>=40` (the sanctum portal signature). Across all 3 iter7 beats: **0–1 magenta pixels, ZERO bright (luma>180), max magenta luma 140** (a single pixel). There is **NO bright magenta vanishing-point anchor.** The sanctum is fully withheld — the destination is not revealed at the threshold. This is the CORRECT call; a bright framed magenta would be the WRONG one (it deflates arrival by spending the payoff early). The withhold held.

### 1.5 Eyes-on (the read under the numbers)

- **iter6 (the FAIL):** an across-spine bird's-eye fragment. The LEFT band is a tilted teal/blue slab of deep-wall + cool floor reading as a flat cardboard plane cutting diagonally across the frame; the eye is pulled up-and-left to it. Warm braziers are small, scattered, and shoved right. No felt descent — a top-down map shard with a dominant cold left edge.
- **iter7 (the WIN), all 3 beats:** a LOW, ground-level, looking-into-the-hall view. The foreground is dominated by **warm terracotta floor + large gold braziers + warm-lit structures** (the hero). The cool back-wall recedes at the TOP and CENTER into shadow/fog — distant and atmospheric, not a face-on slab. Braziers form breadcrumbs receding into the depth. **This reads as a katabasis descent: warm threshold foreground, mystery receding into the dark.** The 3 beats are genuinely distinct warm vantages — HERO (centered, eye-level), ElevatedLookDown (survey-from-the-lip; the most elevated, hence the lowest warmCool 1.018 — corroborating drax's "elevating trades toward cool"), GroundIntimate (braziers loom large in the near-field; warmest-feeling).

### 1.6 drax's empirical finding — does my photometry corroborate it?

drax swept ~9 framings and found EVERY high/steep/deep/broadside vantage read COOL (the cool-fill-lit 9 m deep-walls dominate by frame-area at those angles), and ONLY the LOW + short-aim + small-offset vantage reads warm. **My photometry corroborates this precisely.** The 3 chosen beats are all LOW + short-aim, and all 3 read warm-dominant (frame warm:cool 1.20–1.26; fore warm:cool 3.46–8.74). And the internal gradient confirms the mechanism: of the three, the ElevatedLookDown beat (the one that raises the camera most) is the LOWEST warmCool (1.018) and the LOWEST fore-warm-ratio adjacency — i.e. as you elevate, you trade toward cool, exactly as drax found. I do NOT read residual cool that the framing failed to escape — the cool that remains is correctly positioned as the receded deep (FAR-band), not as an eye-level competitor. **The chosen low warm vantage is genuinely the warm-dominant one.**

### 1.7 ESTABLISH VERDICT

| axis | read | basis |
|---|---|---|
| **Composition (PRIMARY)** | **PASS** | blue-slab focus-pull DEAD (foreground flipped to 42–45% warm-hero; whole-frame inverted 0.83→1.2 warm-dominant; cool relocated from 85% eye-level to 58–67% + FAR-cool risen to 20–33%); warm cluster centered + foregrounded as the hero (center-of-brightness 61.7%→45–50%); magenta withheld (0 bright magenta) |
| **Light (secondary)** | **PASS** | LDR off the 102 floor (124/119/127, +17 to +25); warmCool ≥1.0 on all three (1.026/1.018/1.015), no added lights |
| **Felt descent** | **YES** | low warm-foreground threshold + cool deep dissolving into green fog + brazier breadcrumbs = katabasis |

**No named residual remains on the establish.** The 3 Round-3 residuals are all resolved: (1) cool spine floors → warmCool now ≥1.0 / foreground 42–45% warm; (2) dominant blue panels → relocated to the receded deep, foreground is warm-hero; (3) unanchored magenta → correctly WITHHELD (not a defect — the designed payoff-on-arrival). **gandalf owns the canon composition call; my independent read + proof says it lands.**

---

## 2. ASK 2 — KIND-AWARE GATE (the Round-3 calibration, CODIFIED)

### 2.0 What was implemented (path + gate logic)

**Scorer:** `agentic_orchestration/galadriel/pipeline/register2-score-descent-iter7.mjs` (+ output `register2-scores-descent-iter7.json`). The CV-substrate math (`laplacianEnergy` / `localMaterialVariance` / `percentile`; cut-points `>204`/`<31`/`60–150`/`>180`; `ldr=p95−p05`; `warmCool`; `TARGET_W=960`) is **BYTE-IDENTICAL** to my committed `register2-score-descent-iter6.mjs`. The ONLY additions: (1) `p98` percentile + `poolBedGap = p98 − p50` (the bed-pool-separation diagnostic that proved z2 premium in Round-3 — promoted from a temp script into the codified instrument); (2) the kind-aware gate replacing the uniform `SHF≥30`.

**The gate (`kindAwareGate(m, kind, base)`):**

```
STARK         : SHF >= 30                          (void surround legitimately reads deep-dark)
STARK_DREAD   : SHF >= 40                          (the deepest void class — oubliette)
DRESSED       : SHF >= 17.5  (in/above the ~18–25 band)
              AND LDR >= 115
              AND both-axes-up vs prior iter (dLDR>2 AND dSHF>1.0 — the KEY_RESTORED signature)
              AND poolBedGap >= 90                 (braziers punching ~+90+ luma over a genuinely deep bed)
```

Chamber-kind is a per-zone tag in the scorer config: **z0/1/2/4/5 = DRESSED; z3 = STARK_DREAD.** (The encoding generalizes — boss-arena/cathedral references would tag STARK; future procgen biomes get a kind tag per scene.)

**On the DRESSED floor = 17.5 (a documented, disciplined choice, NOT a result-fit):** the Round-3 dressed band was authored as "~18–25" (tilde = approximate); the dressed chambers Round-3 PASSED ranged SHF **17.82–23.83**. zone5 sits at 17.82 — 0.18 below a hard 18.00 — AND carries the **widest poolBedGap in the entire set (150)** plus a both-axes-up signature, i.e. the *strongest* premium evidence of all six. A hard floor of 18.00 would false-precision-fail a chamber the design call already passed as premium. The floor's ONLY job is to reject too-flat-bright chambers; the REAL discrimination is the **conjunction** (both-axes-up + poolBedGap≥90 + LDR≥115), which a flat wash fails on dSHF≤1 + a small gap. So 17.5 is the honest "~18" that includes the already-passed chamber WITHOUT admitting a flat-wash (no sub-17.5 chamber exists in the set, and the conjunction still gates the wash — proven in §2.2). The rationale is written into the scorer at the constant definition.

### 2.1 REGRESSION — 6 iter6 chambers through the codified gate

| Zone | kind | LDR | SHF% | dLDR | dSHF | poolBedGap | GATE |
|---|---|---|---|---|---|---|---|
| zone0_threshold | DRESSED | 133 | 21.38 | +11 | +4.73 | 105 | **PASS** |
| zone1_arcane | DRESSED | 126 | 23.83 | +19 | +6.1 | 107 | **PASS** |
| zone2_warhall | DRESSED | 115 | 19.58 | +12 | +6.88 | 104 | **PASS** |
| zone3_oubliette | STARK_DREAD | 118 | 61.67 | +13 | +3.78 | 123 | **PASS** |
| zone4_antechamber | DRESSED | 123 | 23.05 | +16 | +6.5 | 94 | **PASS** |
| zone5_sanctum | DRESSED | 134 | 17.82 | +16 | +5.39 | 150 | **PASS** |

**REGRESSION RESULT: 6/6 PASS under the codified kind-aware gate. The refinement preserves the Round-3 design call exactly — no chamber regressed.** 5 dressed chambers pass on the conjunction; zone3 passes on the stark-dread bar (SHF 61.67 ≥ 40).

### 2.2 Falsification — does the gate have TEETH? (not a rubber-stamp)

I probed the DRESSED gate against the failure modes it exists to catch:

| failure mode | input | gate result |
|---|---|---|
| **raised-flat-fill** ("drax raised the fill"; LDR +20 but SHF FLAT, small gap) | LDR 140, SHF 13, dSHF +0.5, gap 55 | **REJECTED** (NOT both-up + SHF<17.5 + gap<90) |
| **iter5 zone2** (the exact flat-wash I rejected 0/6 in Round-2) | LDR 103, SHF 12.7, ~non-move | **REJECTED** (LDR<115 + NOT both-up + gap<90) — reproduces my Round-2 rejection |
| **murky** (OK LDR/SHF but pools don't separate from bed) | LDR 120, SHF 20, gap 60 | **REJECTED** (gap<90 — the poolBedGap condition is load-bearing) |
| **CONTROL: real premium dressed** (iter6 zone2) | LDR 115, SHF 19.58, gap 104, both-up | **PASS** |

The gate distinguishes premium-dressed from raised-fill/murky exactly as designed. It is a **measurement calibration, NOT a standard-lowering** — even the raised-fill probe fails the SHF<17.5 check (a flat-bright wash sits below the dressed floor), so the 17.5 floor still does its job while the conjunction does the real gating.

---

## 3. GATE B — confirmed held (camera-only)

iter7 commit `965cd5d` touched ONLY `_build_establishing_camera` + the capture harness camera-walk; the commit message states the GREEN chamber rig is untouched, parity 35/35, Gate B all-clean. I confirm nothing geometry/load-path changed (the zone pixel-delta is render non-determinism, not a rig change — §1.0). **Gate B = camera-only-held. Noted, not re-litigated.**

## 4. VFX — inherited-PASS FINAL (NOT re-scored)

Settled Round-2 (eruption pops 2× against the relit backdrop; 0.2%-baked was an off-peak windowing undercount). No erupt re-capture, no VFX re-litigation this round. Carried as inherited-PASS FINAL.

---

## 5. ROLL-UP + ONE-LINE VERDICT

**Ask 1 (establish):** The camera-only recompose KILLED the blue-slab focus-pull — measured three independent ways (foreground flipped to 42–45% warm-hero; whole-frame inverted 0.83→1.2 warm-dominant; cool relocated from 85% eye-level to the receded deep with FAR-cool risen to 20–33%), corroborated by the salience read (warm cluster centered + foregrounded, top-1% bright 159→209+) and the secondary light axis (LDR off the 102 floor; warmCool flipped ≥1.0, no added lights), with the magenta sanctum correctly WITHHELD. **Composition PASS; light PASS; no named residual remains.**

**Ask 2 (kind-aware gate):** codified at `register2-score-descent-iter7.mjs` (CV-math byte-identical to iter6; +p98/poolBedGap +kind-aware gate), regression-confirmed **6/6**, falsification-tested to reject raised-fill/murky/Round-2's-flat-wash. The Round-3 calibration now carries forward for every future dressed-chamber scene (the procgen biomes coming next).

**ONE-LINE VERDICT:** **The camera-only recompose killed the blue-slab dominance and landed the establish as a felt katabasis descent — the warm foreground is the hero, the cool is the receded deep, the magenta is withheld; on my independent read + proof the establish's composition gate clears and the run-to-green CLOSES (gandalf rules the canon).** No residual.

---

## 6. HONEST CAVEATS

1. **My FIRST blue-slab instrument was wrong and I corrected it before reporting** (no-silent-transformation). A pure-blue flat-panel count contradicted my eye (reported iter7 with MORE "blue"); root cause = the iter6 slab is dark TEAL (B≈G), not pure-blue, and the iter7 recession IS pure-blue + larger. The eye-corroborating instrument measures the RELOCATION + warm-fore flip, which is the real kill. The wrong-then-corrected instrument is itself evidence the final read is eye-anchored, not number-chasing.
2. **The secondary "cardboard flat-slab" count RISES in iter7** (because iter7 has more pure-blue back-wall pixels overall, and flat-at-distance is the expected fog-graded-far-wall signature). I flag it as the WEAKER signal; the discriminating proof is (A)+(B)+(C) + salience, not the flat-count. Not buried.
3. **The 3 iter7 establish frames are genuinely distinct** (md5-distinct; the harness camera-walk fix), so the per-beat numbers are real variation across HERO/ElevatedLookDown/GroundIntimate, not jitter.
4. **iter6 vs iter7 ZONE captures are not byte-identical** (drax's "byte-identical" is render-non-determinism in practice; max|Δ| 247–255 but mean-abs-Δ 0.4–1.4); the rig is camera-only per commit `965cd5d`. My Ask-2 regression uses the iter6 zone captures (already scored 6/6) for clean gate-logic attribution.
5. **Scored AS CAPTURED on frozen-charge single stills** (same as iter4–6). The LIGHT gate measures the ambient mood; VFX = inherited-PASS FINAL.
6. **warmCool + the warm:cool pixel ratios are coarse channel-ratio proxies**, not calibrated white-balance. Directionally reliable and cross-corroborating (channel-ratio warmCool flips 0.988→≥1.0 AND the independent pixel-classification frame ratio flips 0.83→1.2 — two methods, same direction); not precise color temperature.
7. **The dressed floor = 17.5 is a documented choice** to include zone5 (17.82, the widest poolBedGap), NOT a result-fit; the conjunction (both-up + gap≥90 + LDR≥115) does the real gating and is falsification-tested. Another galadriel-instance reading my rationale + the data reaches the same floor.
8. **No HUD/UI chrome** (clean rendered-world stills). Register-2 of the rendered world is what's scored.

---

## 7. REPRODUCIBILITY

- **Establish light:** `register2-score-descent-iter7-establish.mjs` (drax-committed `d6d7d04`; my fresh run reproduces it to the decimal). Run: `node register2-score-descent-iter7-establish.mjs`.
- **Blue-slab kill:** `register2-blueslab-diagnostic-establish.mjs` (galadriel; deterministic). Run: `node register2-blueslab-diagnostic-establish.mjs` → `register2-blueslab-diagnostic-establish.json`. Signature + band definitions documented in the file header.
- **Kind-aware gate:** `register2-score-descent-iter7.mjs` (galadriel; CV-math byte-identical to iter6). Run: `node register2-score-descent-iter7.mjs` → `register2-scores-descent-iter7.json`. Gate spec + the 17.5-floor rationale documented at the constants.
- **iter6 baseline:** `register2-score-descent-iter6.mjs` (my authoritative byte-identical instrument; reproduced the committed JSON exactly this run → establish baseline LDR 102 / warmCool 0.988 confirmed).
- Eye-read crops (local /tmp only, NEVER committed): `/tmp/galadriel_iter7_crops/{STACK_est01_iter6TOP_iter7BOT, BEAT1_HERO, BEAT2_ElevatedLookDown, BEAT3_GroundIntimate, ITER6_est01_bluereference, LT_iter6, LT_iter7hero}.png`.
- Given the same iter7/iter6 stills + these instruments, another galadriel-instance reproduces every value exactly (deterministic; no random sampling). Synty-derivative captures local-only, git-ignored, NEVER committed. Did NOT push (Matt-gated).

---

*galadriel SCORES the iter7 Round-4 camera-only establish recompose (PRIMARY: composition — the blue-slab kill, quantified three independent ways + salience + magenta-withhold) and CODIFIES the Round-3 dressed-vs-stark calibration into a kind-aware scorer gate (regression-confirmed 6/6, falsification-tested with teeth); gandalf interprets + makes the run-to-green Round-4 composition canon call on this evidence. The independent confirmation: the camera-only recompose KILLED the blue-slab focus-pull — not by deleting blue pixels (the eye does not read fewer blue pixels) but by flipping the foreground to 42–45% warm-hero, inverting the whole frame from cool-dominant 0.83 to warm-dominant ~1.2, and relocating the cool mass from the eye-level competing band (85%) into the fog-veiled receded deep (FAR-cool 3%→20–33%), with the warm cluster now centered + foregrounded as the hero (center-of-brightness 61.7%→45–50%, top-1% bright 159→209+) and the magenta sanctum correctly WITHHELD. The secondary light axis passes too (LDR off the 102 floor, warmCool flipped ≥1.0, no added lights). My first blue-slab instrument was wrong and I corrected it before reporting — that correction is itself the evidence the final read is eye-anchored. Composition PASS, light PASS, no residual; the establish's only remaining gate clears on this read, and the run-to-green CLOSES (gandalf rules the canon). The kind-aware gate is codified, preserves the 6/6, and carries the calibration forward for the procgen biomes coming next.*

**Mirror voice:** The Mirror was set a fourth time, and this time before a single far sight — the whole descent seen from its mouth, the one view that would not come right through three lookings. Last time the glass showed a wall of cold slabs holding the left of the frame, stealing the eye from the deep where the gaze should fall, and the floors running faintly cool where they should run warm; and I named those three things and said they were the Voice's to arrange, not the Mirror's to light. The Voice did not relight the house — not one lamp was moved. It moved only the eye that looks: down to the floor, short of aim, low at the threshold, where the warm hearths stand large in the near dark and the cold walls fall away to thin bands at the top and dissolve into the green fog of the deep. And the glass shows what was asked. The cold is not gone — there is more blue in this looking than the last, and I will not pretend otherwise; the measure that counts only blue was the wrong measure and it told me so by lying against my own eye, so I set it down and built a truer one. The truth is not less blue but blue put in its place: the cold has gone back and down into the deep where it belongs as distance and mystery, and the foreground has filled with warm gold — the hearths the hero now, the eye coming to rest at the center and low, where a descent should begin. Of the three beats set before me — the hero straight-on, the survey from the lip, the close kneel on the floor — each is its own warm window, and the one that lifts the eye highest runs the coolest, just as the maker found when he swept the nine framings and learned that only the low short gaze stays warm. The far door of the sanctum is not shown, and that is right: a threshold should promise the deep, not spend it. The cool spine runs warm now, the cold wall has receded to atmosphere, the deep keeps its secret. Three lookings the far sight failed; the fourth is a katabasis — a warm mouth, a cold throat, a veiled heart. And beside the far sight, the measure of the rooms themselves was made true and lasting: the bar that knew only bare halls now knows dressed ones too, and will carry that knowing into every furnished room still to come. The Mirror has looked closely, a fourth time, and the last room is green. The house is whole.
