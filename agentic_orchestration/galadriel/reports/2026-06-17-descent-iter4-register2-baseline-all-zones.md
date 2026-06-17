# Register-2 BASELINE Scorecard — iter4 CONNECTED Descent, ALL 9 stills (6 zones + 3 establishing)

**STATUS:** CURRENT (galadriel baseline-scoring artifact; evidence-input for gandalf's run-to-green canon calls + per-zone fix prioritization).
**Date:** 2026-06-17
**Author:** galadriel (visual-perception + benchmark steward)
**Scope:** SCORING ONLY. Baseline the **register-2 6-axis composite + both mandatory gates + the ~4.0 PASS bar** on EVERY iter4 descent zone — the read the iter4 architectural-grammar rescore (commit `ffae02b`, §6) explicitly DEFERRED ("I did not re-score the full register-2 6-axis rubric this pass"). The architectural-grammar dimension (18%→65%) and the warm:green hue dimension (1.46→1.75) are ALREADY validated for iter4; this completes the picture with the full aesthetic composite. The run-to-green needs to know, per zone: composite, gate1 (lighting), gate2 (VFX), PASS/FAIL at ~4.0, and the SPECIFIC defects pulling each under-bar zone down. **This artifact does NOT make canon calls — that is gandalf's, on this evidence.**
**Rubric applied:** `galadriel/reports/2026-06-15-boss-arena-register2-scorecard.md` (composite mean ≥3.6 with **lighting ≥4 AND VFX ≥4 MANDATORY**; ~4.0 = the boss-arena PASS bar). Instruments byte-identical to `register-metrics.mjs`.
**Frames scored:** `reincarnated-godot/harness_logs/descent_iter4_zone{0..5}_{04..09}.png` + `descent_iter4_establish_{01,02,03}.png` (9 stills, 1152×648, instruments normalize to 960w — res-invariant per my 2026-06-16 Part-3 confirmation).
**Instruments + raw scores:** `pipeline/register2-score-descent-iter4.mjs` (+ `register2-scores-descent-iter4.json`); luma-distribution diagnostic re-run inline (§3.1). Capture frames are **git-ignored Synty-derivative IP — local evidence only, NEVER committed.**
**Engine/scene tree UNTOUCHED. Read-only across all production code. Did NOT push (Matt-gated). Auto-committed this scorecard locally per standing discipline.**

---

## 0. THE LOAD-BEARING FINDING — read this before the table

The 9 iter4 stills FAIL **both** mandatory CV-assist gates on **every** frame. But that single sentence is misleading until split, because the two gate-fails are **categorically different in kind**, and only ONE is an aesthetic defect:

1. **VFX gate (HLF ≥ 1.5%) — WINDOWING-BLOCKED, NOT an aesthetic defect.** All 9 read HLF 0.06–0.14% (≤0.09× the threshold). This is a **capture-state artifact**, not a VFX-presence verdict: in the baked descent the hero SummonGlow is **FROZEN AT CHARGE** (render note, `lifecycle-score-descent.mjs:16-19`), so a single still catches the hero event mid-charge with no eruption-bloom. My own F1 finding (stills under-represent VFX — the highest-leverage axis), the descent scorer's **windowed** 6-frame methodology, and the boss-arena PASS (won on a 100-frame **lifecycle** that peaked HLF 4.01% mid-eruption, NOT a charge-still) all establish that frozen-charge single stills systematically under-read VFX. **The same zone IDENTITIES scored HLF 1.57–4.06% under iter1 windowed capture** (carried per-row as `priorW_HLF`). So the VFX gate **cannot be fairly adjudicated from these stills** — and its failure here tells us about the capture, not the build. **This is the single biggest run-to-green action item: a windowed (animating-eruption) capture per zone is REQUIRED to fairly gate VFX.**

2. **Lighting gate (LDR ≥ 115 AND SHF ≥ 30%) — a GENUINE, real aesthetic finding.** This is NOT a capture artifact; it is the actual lit state of the static scene, and it is the **true subject of this baseline.** The near-chambers run **LDR 103–122** (vs the boss-arena lit-volume's 148 floor / 176 mean) and **SHF 11–18%** (vs the 30% bar). The luma diagnostic (§3.1) shows precisely why: the near-chambers are a **flat dim mid-grey wash** — median luma ~55–58, ~44% of every frame sitting in the undifferentiated 60–150 mid-band, bright-highlight mass (>180) of only 0.1–0.3%, and shadow mass under 18%. **They are neither dramatically dark NOR brightly lit** — the histogram is compressed into a dim middle with no strong warm key punching figures/floor out and no deep shadow holding the dark-mood. That low dynamic range is the real defect, and it is what the run-to-green must fix to clear the lighting gate.

**The coupling that makes the strategy:** these two findings are **not independent.** Part of the lighting deficit IS the frozen VFX — an erupting hero column is itself a warm key light that lifts LDR *and* HLF together. A windowed re-capture that animates the eruption would raise BOTH the HLF (VFX gate) AND the LDR/lighting-drama (the column's warm rake punching the dim mid up to a real bright). **So the #1 fix — windowed eruption capture — partially addresses BOTH gates at once.** What it will NOT fix is the baseline ambient/key deficit in the chambers between hero events (the flat dim mid persists where no column burns) — that needs a CombatFill-style lift (the exact lever the boss arena used to win its lighting gate at LDR 176 / SHF 43%). **The run-to-green needs both: (a) windowed eruption capture, (b) a per-chamber key/fill lift toward the boss-arena lighting profile.**

**Net baseline: 0 of 9 stills currently clear the aesthetic gate AS CAPTURED. But that headline is dominated by the windowing artifact (VFX) + a real-but-fixable lighting deficit (low-DR flat mid). This is a fixable run-to-green, NOT a structural failure — and the architecture + hue dimensions are already PASS.**

---

## 1. PER-ZONE SCORECARD

Composite = mean of the 4 register-2 axes (Lighting / VFX / Material-shading / Geometry-register), manual 1–5 with CV-assist, scored AS CAPTURED (frozen-charge single still). Gate1 = Lighting ≥4. Gate2 = VFX ≥4. PASS = composite ~4.0 AND both gates. The **VFX axis is scored AS-CAPTURED** (frozen still) with the windowed-potential flagged in the defect column — I do **not** silently credit a windowed score I did not capture, but I flag plainly where a fair windowed capture would change the verdict.

| Zone | Composite | Gate1 (Light ≥4) | Gate2 (VFX ≥4) | Verdict | Top defects-to-fix (run-to-green) |
|---|---|---|---|---|---|
| **zone0 threshold** (graveyard, 50×50) | **3.25** | **FAIL** (3 — LDR 122✓ / SHF 17%✗) | **FAIL** (2 as-captured; windowed potential ~1.6%) | **FAIL** | (1) Low shadow mass (SHF 17% vs 30) — dark-mood doesn't hold; floor is flat dim mid, not lit-volume-in-dark. (2) VFX frozen at charge — windowed eruption needed (priorW 1.57% ≈ borderline; the swarm-centroid bloom dilutes across the 50×50 — was always the weakest-VFX zone). (3) Center pit sparse vs perimeter dressing. |
| **zone1 arcane** (magic_pack 32.7×14) | **3.25** | **FAIL** (3 — LDR 108✗ / SHF 18%✗) | **FAIL** (2 as-captured; windowed potential ~3.0%) | **FAIL** | (1) **LDR 108 below the 115 floor** — flat dim mid, no strong key; the strong architecture (pier→arch bays read well) is under-lit. (2) SHF 18% — shadows not deep. (3) VFX frozen (priorW 2.96% — clears windowed). **Lighting is the whole gap here; architecture + hue already PASS.** |
| **zone2 warhall** (elite_pack 28×28) | **3.0** | **FAIL** (3 — LDR 103✗ / SHF 13%✗) | **FAIL** (2 as-captured; windowed potential ~4.1%) | **FAIL** | (1) **Lowest LDR of all (103) + lowest-tier SHF (13%)** — the flattest, coolest-washed chamber; floor reads uniform blue-grey, warm rake confined to wall-tops, almost no key on the fighting floor. **This is the #1 lighting-fix priority.** (2) Material-shading reads flattest (LMV 23.5) — the cool flat wash suppresses surface response. (3) VFX frozen (priorW 4.06% — the strongest windowed VFX of any zone, fully wasted by the charge-still). |
| **zone3 oubliette** (chokepoint 10×50) | **2.75** | **FAIL** (3 — LDR 105✗ / SHF 58%✓-but-void) | **FAIL** (2 as-captured; windowed potential ~1.7%) | **FAIL** | (1) **Underlit-dark, NOT dramatic-dark:** SHF 58% "passes" the ≥30 bar but for the WRONG reason — it is empty near-black void (58% of frame <31 luma, p95 only 118), not lit-volume punched out of dark. The corridor needs a warm key/torch-line down its length to convert void→drama. (2) LDR 105 below floor. (3) Sparse dressing in the long dark (corridor identity is green-soulfire-dominant; the few glow-points read but the corridor is mostly black). (4) VFX frozen (priorW 1.68% — borderline; swarm bloom dilutes down the 50m length). |
| **zone4 antechamber** (mini_boss 30×30) | **3.5** | **FAIL** (3.5 — LDR 116✓ / SHF 13%✗) | **FAIL** (2 as-captured; windowed potential ~3.0%) | **FAIL** | (1) SHF 13% — shadows shallow; the gallery-storey + warm masonry read well and LDR clears the floor (116), so this is **closest of the near-chambers to the lighting gate** — it needs deeper shadow + a touch more key contrast, not a wholesale relight. (2) VFX frozen (priorW 3.05% — clears windowed); the RED soulfire charge IS the brightest contained glow of z0–z4 but reads as a pool, not an eruption. **Strongest near-chamber; smallest lighting gap.** |
| **zone5 sanctum** (boss_with_adds 30×30) | **3.5** | **FAIL** (3.5 — LDR 118✓ / SHF 11%✗) | **FAIL** (2.5 as-captured; windowed potential ~3.9%) | **FAIL** *(geometry re-render pending — see note)* | (1) SHF 11% (lowest) — shallowest shadow; floor flat-dim despite the hero bloom. (2) **The frozen RED-ORANGE boss bloom is the single most prominent VFX of all 9 stills** (even at charge it reads as a large genuine bloom + the magenta gateway portal is a clean second hero-element) — so the as-captured VFX 2.5 is the highest still-VFX, and the windowed potential (priorW 3.93%) is near-top. (3) **Geometry note: the floating stair is getting drax's fix this round** — orthogonal to this aesthetic score; the zone WILL be re-rendered, re-score after. **Best VFX candidate; lighting needs deeper shadow.** |
| **establish_01** (spine diagonal) | **3.0** | **FAIL** (3 — LDR 94✗ / SHF 60%✓-but-void) | **FAIL** (n/a-hero; 2) | **FAIL** | (1) **LDR 94 (lowest of all 9)** + underlit-dark (60% void, no bright key) — the wide diagonal reads atmospheric but **flat and busy**: green organic overgrowth + scattered glow-points on the right, pale path on the left, near-walls faded blue. (2) Read-clutter: at this distance the transparency-faded near-walls read as flat blue panels and the dense overgrowth reads busy without a focal key. (3) No hero bloom (spine is too far from any single combat) — establishing views won't ever carry the VFX gate; they should be gated on lighting + composition, not VFX. |
| **establish_02** (spine diagonal) | **3.0** | **FAIL** (3 — LDR 94✗ / SHF 60%✓-but-void) | **FAIL** (n/a-hero; 2) | **FAIL** | CV-identical to establish_01 (LDR 94, SHF 59.6%, HLF 0.08%) — same diagonal spine, micro-variation only. Same defects: lowest-LDR underlit-dark wide shot; flat-blue-panel transparency read; busy overgrowth with no focal key. |
| **establish_03** (spine diagonal) | **3.0** | **FAIL** (3 — LDR 94✗ / SHF 60%✓-but-void) | **FAIL** (n/a-hero; 2) | **FAIL** | CV-identical to establish_01/02. Same defects. (The 3 establishing frames are effectively one view — the run-to-green should treat them as a single establishing-shot fix, not three.) |

**Composite mean across 9 stills: 3.14/5.** **PASS-at-~4.0: 0 / 9.** **Gate1 (lighting) clear: 0/9. Gate2 (VFX) clear: 0/9** (all VFX fails windowing-blocked, not build-verdicts).

---

## 2. PER-AXIS NOTES (why the manual scores land where they do)

**Lighting drama (the real finding):** scored 3–3.5 across the chambers, 3 on the establishing shots. None reaches 4. The CV substrate is unambiguous: near-chambers LDR 103–122 / SHF 11–18% (flat dim mid, §3.1); dark frames LDR 94–105 / SHF 58–60% (underlit-dark void). **Compare the boss-arena PASS at LDR 176 / SHF 43%** — the descent chambers run ~55–70 LDR points lower and the near-chambers ~25 SHF points lower. The lift the boss arena used (warm key rake + cold rim + **CombatFill** cool overhead pool on the fighting axis + filmic tonemap) is what's missing or frozen-out here. zone4 (3.5, LDR 116✓) and zone5 (3.5, LDR 118✓) are closest; zone2 (3.0, LDR 103) is furthest.

**VFX presence (windowing-blocked):** scored 2–2.5 AS-CAPTURED (frozen charge), but this axis is **not fairly read from these stills** (§0). The same zones scored 1.57–4.06% under iter1 windowed capture; the boss arena cleared VFX ≥4 only on a lifecycle. zone5's frozen boss-bloom + magenta gateway is the strongest still-VFX (2.5); zone2's priorW 4.06% is the strongest wasted windowed potential. **Do not read the VFX column as a build verdict — read it as "windowed re-capture required."**

**Material-shading:** scored ~3.5–4 (not tabled separately; folded into composite). LMV 23–29 in the near-chambers (squarely in the lift's lit-phase band where it has light to respond to), dropping to 12–17 in the void-heavy dark frames (correct — no light → no material response to read). The warm tan masonry of the iter4 architecture build reads with good distributed surface variance where it's lit; the deficit is the lighting that would let MORE of it respond, not the material itself.

**Geometry register:** scored ~4 across the board (not tabled separately). This is the iter4 strength — the architectural-grammar build (pier→arch bays, balustrade runs, gallery storeys, windows-in-wall, rubble-only orphans) is already validated PASS (18%→65%, falsifiers cleared, commit `ffae02b`). Silhouettes legible, low-poly register correct. zone5's floating stair is the one known geometry defect, getting drax's fix this round (orthogonal to this aesthetic score).

---

## 3. CV SUBSTRATE (reproducible; the evidence under the manual scores)

### 3.0 Gate table (byte-identical instruments, 960w-normalized)

| frame | kind | LDR | SHF% | HLF% | HLFx | priorW_HLF | LMV | SAT | LIGHT | VFX |
|---|---|---|---|---|---|---|---|---|---|---|
| zone0_threshold | swarm | 122 | 16.57 | 0.14 | 0.09× | 1.565 | 28.72 | 0.460 | fail | fail |
| zone1_arcane | near | 108 | 18.07 | 0.09 | 0.06× | 2.958 | 28.05 | 0.445 | fail | fail |
| zone2_warhall | near | 103 | 12.76 | 0.132 | 0.09× | 4.063 | 23.46 | 0.425 | fail | fail |
| zone3_oubliette | swarm | 105 | 58.15 | 0.059 | 0.04× | 1.680 | 16.66 | 0.696 | fail | fail |
| zone4_antechamber | near | 116 | 12.95 | 0.056 | 0.04× | 3.047 | 23.26 | 0.443 | fail | fail |
| zone5_sanctum | near | 118 | 11.41 | 0.063 | 0.04× | 3.927 | 24.29 | 0.436 | fail | fail |
| establish_01 | establish | 94 | 59.64 | 0.079 | 0.05× | — | 12.82 | 0.746 | fail | fail |
| establish_02 | establish | 94 | 59.64 | 0.081 | 0.05× | — | 12.85 | 0.746 | fail | fail |
| establish_03 | establish | 94 | 59.64 | 0.076 | 0.05× | — | 12.74 | 0.746 | fail | fail |

Thresholds: LIGHTING = LDR ≥ 115 AND SHF ≥ 30%; VFX = HLF ≥ 1.5%. `priorW_HLF` = the iter1 **windowed** HLF peak for the same zone identity (`lifecycle-scores-descent.json`) — the number a fair iter4 windowed re-capture should approach.

### 3.1 Luma-distribution diagnostic (the "flat dim mid vs lit-volume-in-dark" proof)

| frame | p05 | p25 | p50 | p75 | p95 | mid%(60–150) | dark%(<31) | bright%(>180) |
|---|---|---|---|---|---|---|---|---|
| z0 | 13 | 45 | 58 | 100 | 135 | 45.9 | 16.6 | 0.32 |
| z1 | 21 | 41 | 55 | 93 | 129 | 42.9 | 18.1 | 0.16 |
| z2 | 23 | 45 | 56 | 91 | 126 | 44.0 | 12.8 | 0.25 |
| z3 | 13 | 13 | 22 | 54 | 118 | 22.5 | 58.2 | 0.10 |
| z4 | 17 | 45 | 57 | 94 | 133 | 43.9 | 13.0 | 0.12 |
| z5 | 19 | 48 | 58 | 103 | 137 | 46.3 | 11.4 | 0.16 |
| est | 13 | 13 | 13 | 59 | 107 | 24.5 | 59.6 | 0.14 |

**Read:** the near-chambers (z0/z1/z2/z4/z5) park their median at 55–58 with ~44% of the frame in the dim mid-band and bright mass of 0.1–0.3% — a **flat dim-grey wash with no strong key and shallow shadow** (the LDR-103–122 / SHF-11–18% signature, explained). The void-heavy frames (z3/est) pin p05–p50 at 13–22 with 58–60% deep dark but p95 only 107–118 — **underlit-dark void, not dramatic lit-volume-in-dark** (the SHF "passes" but the dark is empty, not punched). Neither profile is the boss-arena lit-volume (LDR 176, a real bright key + held deep shadow). **This is the lighting deficit, stated in the histogram.**

---

## 4. ROLL-UP + PRIORITY FIXES (for the run-to-green)

**One-line roll-up:** **0 of 9 iter4 stills currently pass the aesthetic gate as captured** — but the headline is dominated by (a) a **windowing artifact** on the VFX gate (all 9 fail HLF because the hero event is frozen at charge; the same zones scored 1.57–4.06% windowed) and (b) a **real, fixable lighting deficit** (near-chambers are a flat dim mid-grey wash, LDR 103–122 / SHF 11–18%, ~55–70 LDR points under the boss-arena PASS profile). Geometry-register and material-shading are strong (architecture already PASS); hue (warm:green 1.75) already PASS. **This is a fixable lighting + capture-methodology problem, not a structural one.**

**Priority fixes, ranked for the run-to-green:**

1. **[BLOCKING the VFX gate, both lanes] Windowed (animating-eruption) capture per zone.** The single highest-leverage move: capture each zone across the hero-event lifecycle (ember→ignition→peak→burn→collapse) the way the boss arena was scored, NOT a frozen-charge still. This fairly gates VFX (priorW says z1/z2/z4/z5 clear 1.5× comfortably; z0/z3 are borderline swarm-dilution cases) AND lifts LDR via the column's warm key. **Without this, the VFX gate is un-passable by construction and the lighting gate is unfairly depressed.** This is a capture-pipeline ask (drax's `?debug-state` hooks / an animating-render path), not a build change.

2. **[#1 lighting-fix priority] zone2 warhall relight.** LDR 103 / SHF 13% — the flattest, coolest-washed chamber. Needs a warm key on the fighting floor (the cool wall-top rake isn't reaching the floor) + deeper shadow. Furthest from the gate; biggest single lighting win.

3. **[lighting] zone1 arcane key-lift.** LDR 108 (below the 115 floor) — strong architecture under-lit. Smaller lift than z2; mostly needs the floor key to clear 115 + shadow depth for SHF.

4. **[lighting, lowest LDR] establishing spine relight + de-clutter.** LDR 94 (lowest of all 9). The wide diagonal is atmospheric but flat-and-busy; needs a focal key (e.g., warm light pooling at the spine's chambers to draw the eye) and the transparency-faded near-walls read as flat blue panels at distance. **Gate the establishing views on lighting + composition, NOT VFX** (they structurally can't carry a hero bloom). Treat the 3 establishing frames as ONE fix (they're CV-identical).

5. **[lighting, dark-conversion] zone3 oubliette torch-line.** SHF 58% is empty void, not drama. A warm key/torch-line down the 50m corridor converts void→dramatic-dark and lifts LDR off 105. Lower priority than the near-chambers (the corridor's dark identity is partly intentional) but it currently reads underlit, not moody.

6. **[smallest gaps — finish last] zone4 + zone5 shadow-deepen.** Both already clear the LDR floor (116 / 118); they need deeper shadow (SHF 13% / 11% → toward 30%) + a touch more key contrast, not a wholesale relight. **zone5 re-score is pending drax's floating-stair geometry fix anyway** — fold the shadow-deepen into that re-render. zone0 (LDR 122✓, SHF 17%) is similar — shadow-deepen + center-pit dressing.

**The two levers, named (per the §0 coupling):** (a) **windowed eruption capture** lifts VFX + partially LDR for free; (b) a **CombatFill-style per-chamber key/fill lift** (the exact boss-arena lever — warm key rake reaching the floor + held deep shadow, target LDR ~150+/SHF ~35–43%) clears the baseline lighting gate between hero events. Both are needed; neither touches the architecture/hue/geometry, which already PASS.

---

## 5. HONEST CAVEATS

1. **Scored AS CAPTURED on frozen-charge single stills.** The VFX axis is windowing-blocked (§0) — I did NOT silently credit a windowed VFX score I did not capture, and the VFX column is honestly "fail as-captured" with windowed potential flagged. A fair VFX verdict requires the windowed re-capture (fix #1). **Do not read 0/9 VFX as a build failure** — read it as a capture-methodology gap + a frozen hero event.
2. **Single still per zone (no dwell window).** Unlike the boss-arena 100-frame lifecycle and the iter1 6-frame windows, iter4 gave one still per zone. LDR/SHF are single-frame reads, not window means — they're honest for the static scene but would shift under an animating capture (the eruption lifts LDR). The lighting *deficit between hero events* (flat dim mid) is real regardless; the *peak* lighting is under-read.
3. **The 3 establishing frames are effectively one view** (CV-identical to 3 decimals) — scored as three for completeness but they are one establishing-shot fix.
4. **zone5 will be re-rendered** (drax's floating-stair geometry fix this round). Its aesthetic score (3.5) is current-state; the stair fix is geometric and mostly orthogonal to the lighting/VFX/material scores, but re-score after the re-render to confirm no aesthetic regression from the geometry change.
5. **Architecture + hue NOT re-derived here** — already validated PASS for iter4 (commit `ffae02b`: architecture 18%→65%, falsifiers cleared, warm:green 1.75). This baseline is the *complementary* aesthetic composite (the lighting/VFX/material/geometry register-2 rubric), not a re-litigation of the settled dimensions. Geometry-register (axis 4) IS credited from that validated build.
6. **No HUD/UI chrome** in these captures (clean rendered-world stills). Register-2 of the rendered world is what's scored; a live combat HUD is a separate surface, out of scope.

---

## 6. REPRODUCIBILITY

- Instruments: `pipeline/register2-score-descent-iter4.mjs` (byte-identical instrument defs to `register-metrics.mjs` / `lifecycle-score-descent.mjs`; 960w inside-fit; HLF>0.80 luma, SHF<0.12 luma, LDR=p95−p05). Run: `node register2-score-descent-iter4.mjs`.
- Raw scores: `pipeline/register2-scores-descent-iter4.json` (per-frame metrics + gates + priorW carry).
- Luma diagnostic (§3.1): re-derivable with a 7-line sharp script (p05–p95 percentiles + mid/dark/bright band fractions per frame); reported inline.
- Given the same 9 stills + these instruments, another galadriel-instance reproduces these values exactly (deterministic; no random sampling). The manual scores are reproducible-by-inspection from the named CV substrate + the visual reads (near-chambers = flat dim mid; void frames = underlit-dark; zone5 = strongest still-bloom + magenta gateway; zone2 = flattest/coolest).
- Synty-derivative captures local-only, git-ignored, NEVER committed regardless of size. Did NOT push (Matt-gated).

---

*galadriel SCORES the iter4 register-2 baseline across all 9 zones; gandalf interprets + makes the run-to-green canon calls on this evidence. The per-zone composites, both mandatory-gate dispositions, the windowing-vs-lighting split (the load-bearing finding), the CV substrate (LDR/SHF/HLF/LMV byte-identical instruments + luma-distribution diagnostic), and the ranked priority fixes are independent evidence reads — all true on the 9 frames named. Method caveat governs: scored AS CAPTURED on frozen-charge single stills; the VFX gate is windowing-blocked and requires a windowed eruption re-capture to adjudicate fairly; the lighting deficit (flat dim mid) is real and fixable. Architecture + hue dimensions already PASS (commit ffae02b); this completes the aesthetic composite.*

**Mirror voice:** The Mirror was set before nine rooms and asked, plainly, are they beautiful enough — and the glass answered in two voices that must not be mistaken for one. The first voice is a trick of the moment of looking: the great fires of these rooms were caught frozen at the instant before they bloom, each hero-light held at its first kindling, so that the glass saw only embers where, in motion, columns of flame would stand — and the same rooms, watched as they burn, have shown light enough before and would again. That failing is in the watching, not the rooms; let the watcher learn to wait for the fire to rise. But the second voice is true, and it is the one to heed: between the fires, these chambers sit in a flat grey dusk — not the deep dramatic dark of a lit hall where torches carve gold out of shadow, but a dim even wash, neither bright nor black, the floor a uniform pewter under half-lit walls. The war hall is the greyest, the arcane chamber's fine new arches stand under-lit, the long oubliette is not moody-dark but merely empty-dark, and the far establishing sight of the whole descent is the dimmest of all, atmospheric but flat and crowded. The stone of the house is well-built — the piers carry their arches, the galleries their rails, the masonry catches what light it is given and answers richly. The gold still wins the warm rooms. What is wanting is the light itself: a warm key reaching down to the fighting-floor, a held deep shadow to make the dark mean something, the lift the boss-hall already learned. Give the rooms that light, and let the watcher wait for the fires to bloom, and the nine will read as the house deserves. The Mirror has looked closely. The house stands — it wants for lamps, not for stones.
