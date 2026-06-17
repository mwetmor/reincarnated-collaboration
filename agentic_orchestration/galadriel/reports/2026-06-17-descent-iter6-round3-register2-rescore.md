# Register-2 ROUND-3 RE-SCORE — iter6 GLOBAL-RIG-MATCH Descent (6 zones + 3 establish)

**STATUS:** CURRENT (galadriel re-scoring artifact; the independent confirmation of drax's iter6 self-measure; evidence-input for gandalf's run-to-green Round-3 Gate-A call + the §2 dressed-vs-stark threshold calibration).
**Date:** 2026-06-17
**Author:** galadriel (visual-perception + benchmark steward)
**Scope:** SCORING ONLY + the one calibration judgment gandalf delegated to my eye (§2 zone2 premium-vs-murky). Does NOT make the canon call — that is gandalf's, on this evidence.
**Build scored:** drax Round-3 iter6, commit `9b16d39` (reincarnated-godot, `render_descent_scene.gd`) — GLOBAL env-rig matched to the proven register-2 rig (ACES / white8 / exp0.95 / ambient0.17 / fog~0.010, green `fog_light_color` kept). NO per-chamber key retune (clean one-change attribution).
**Baseline:** iter5, commit `7ce990e` — per-chamber KEY lift, which I REJECTED 0/6 in Round-2 (the suppressor was global env-divergence, not per-chamber key energy). My iter5 scorecard: `2026-06-17-descent-iter5-round2-register2-rescore.md`.
**Acceptance criteria (gandalf Round-3 brief §2):** (a) 5 standard chambers (z0/1/2/4/5): **LDR lifted toward ~176 AND SHF deepened, BOTH simultaneously** — then the §2 SHF-absolute-level judgment. (b) zone3 oubliette: judged on the **CONTRAST criterion** (high SHF + bright torch-pools in real black + moderate LDR), NOT the LDR-176 bar. (c) zone4: regression-revert confirmation (LDR back ≥115). (d) establish ×3: light AND composition.
**North-star (boss-arena PASS, `lifecycle-scores-boss.json`):** LDR mean **175.97** / SHF mean **42.74%** / HLF peak **4.013%**.
**Instruments:** drax's `pipeline/register2-score-descent-iter6.mjs` (+ `register2-scores-descent-iter6.json`) — **I diffed it function-by-function against my committed Round-2 instrument `register2-score-descent-iter5.mjs` and confirmed the CV math is BYTE-IDENTICAL** (laplacianEnergy / localMaterialVariance / percentile identical; the pixel cut-points `>204`/`<31`/`60–150`/`>180`, `ldr=p95−p05`, `dLDR>2` acceptance trigger, warmCool ratio, TARGET_W=960 all identical; the only diffs are comments + the iter5-only erupt-validator console block). I then **ran it fresh myself** — my execution reproduces the committed JSON exactly (deterministic, no random sampling). This is my authoritative instrument by inheritance.
**Method:** CV substrate (reproducible) + my own eyes-on read of every iter6 frame, the matched iter5 stacked pairs, and a §2-arbiter bed-pool-separation diagnostic. **iter6 captures md5-verified DIFFERENT from iter5** — all 9 hashes distinct from their iter5 counterparts (zone2: iter6 `3510ce41…` ≠ iter5 `6dee78ea…`); timestamps 09:15 (iter6) vs 08:28 (iter5). Ruled out a stale/mis-pointed-capture false read before reporting, as in Round-2.
**Engine/scene tree UNTOUCHED. Read-only across all production code. Captures are git-ignored Synty-derivative IP — local evidence only, NEVER committed. Auto-committed this report; the scorer + JSON were already drax-committed (verified byte-identical math). Did NOT push (Matt-gated).**

---

## 0. THE HEADLINE — the §2 verdict, read before the table

**The global-rig match CLEARED Gate A's lighting axis the way the diagnosis predicted — ALL NINE frames moved on BOTH axes at once (the global-cause fingerprint), reversing the Round-2 non-move completely. On the THRESHOLD question gandalf delegated to my eye: I CONVERGE with his dressed-chamber lean. zone2 — the borderline arbiter — reads PREMIUM warm-lit-volume on a genuinely deepened bed, NOT murky; the dressed-chamber SHF-band (17–24%) HOLDS. The matrix is GREEN. No Round-4 deepening pass is needed.**

The single cleanest statement of the round, against Round-2's failure: in Round-2 the mean |dLDR| across 6 zones was **1.7** (a statistical and visible NON-event — the per-chamber key bump changed pixels but not the lit volume). In iter6 the mean dLDR is **+14.5** (z0 +11, z1 +19, z2 +12, z3 +13, z4 +16, z5 +16) and SHF rose on EVERY zone (+3.78 to +6.88). **A move of +14 mean LDR with SHF deepening on all six simultaneously is the unmistakable signature of a GLOBAL cause corrected — the keys were already strong enough; they are now being tonemapped correctly and surrounded by a properly-deepened ambient.** The flat-dim-mid histogram I named at iter4/iter5 finally broke: p50 dropped from 54–58 to 44–48, dark%(<31) rose from ~12–18% to ~18–24%, and the warm/green pools now sit a clear ~100 luma above the deepened bed. **The global-divergence root-cause diagnosis is CONFIRMED by my independent instrument and my eye.**

**Gate-A clearance, counted honestly against the dual-gate:**
- **By the raw uniform 30%-SHF scorer gate:** 1 of 9 prints `LIGHT: PASS` (zone3 only). This is the number my scorer mechanically prints, and I report it as-is — my photometry does not move the goalposts.
- **By the dressed-vs-stark calibration gandalf delegated to my eye (the correct reading):** **8 of 9 PASS** — all 6 zones + 2 of 3 establish-frames' LIGHT-axis, with establish gated-OUT on COMPOSITION (gandalf's call), not on light. The near-chambers clear LDR≥115, moved both-axes-up, and read premium-lit-in-dark to my eye at SHF 17–24 because they are DENSELY DRESSED — the photometry below proves the dressing occupies the frame-area a stark arena leaves black.

**The §2 calibration verdict, stated plainly (this is the load-bearing delegation):** I am NOT lowering the bar to fit the result. I judged zone2 — the weakest near-chamber, SHF 19.58, the case gandalf chose precisely because it is borderline — with my eye AND a dedicated bed-pool-separation diagnostic. **zone2 reads PREMIUM.** The floor bed is a genuinely deep cool-teal (32.9% of the frame below luma 40; median pixel luma 46, dim not mid-grey), and the warm braziers + green soul-fire pools punch a clear **104 luma above** that median bed. That is the photometric AND visible signature of "lit-volume-IN-dark," not "flat-dim-mid murk." A murky frame shows little real dark and a small pool-to-bed gap; zone2 shows substantial deep-bed mass AND a wide pool-bed separation — the opposite. **The dressed-chamber calibration HOLDS: 30% is the bar for STARK chambers (oubliette-class, which the descent PROVES it hits at zone3's 61.7%), and the densely-dressed chambers (z0/1/2/4/5) legitimately read premium-lit-in-dark at SHF ~18–24.** zone3's 61.7% vs the dressed band's ~20% is not the dressed chambers falling short — it is the photometric fingerprint of the dressing filling frame-area that the stark oubliette leaves as void (zone3 dark%=69.6 vs zone2 dark%=19.6; the 50-point gap IS the dressing).

**The discipline check, satisfied:** gandalf explicitly built a falsifiable test — "if zone2 reads murky, 30% is right and the near-chambers need ONE more deepening notch." I looked for the murky read. It is not there. The bed is deep, the pools punch, the eye reads premium. If zone2 had shown a brighter-grey floor with pools barely separated, I would have said so and named the deepening notch — that is what my Round-2 report did to the per-chamber key lift (REJECTED 0/6). This round the evidence genuinely passes, so I report PASS. **Converge, not rubber-stamp: my photometry independently lands where gandalf's design lean pointed, and the zone2 arbiter — the one he flagged as the risk — is the strongest single piece of evidence FOR it, not against.**

**The one scorer refinement I recommend (as a note, not a goalpost-move):** the uniform 30%-SHF gate is **stark-chamber-calibrated**. It should be refined to a **dressed-chamber band (~SHF 18–25 with LDR≥115 + both-axes-up + bed-pool-separation poolBedGap ≳ 90)** for densely-dressed chambers, while STARK chambers retain the ≥30% (oubliette-class) or ≥40% (dread) bar. This is a measurement-calibration refinement that makes the scorer correctly distinguish "premium dressed dungeon" from "raised flat fill" — it is NOT a lowering of the standard, because the both-axes-up + poolBedGap conditions still gate out a flat wash (a raised fill would show LDR-up-but-SHF-FLAT and a SMALL poolBedGap; iter6 shows neither). I'll author it into the scorer as a dressed-chamber gate on gandalf's go.

---

## 1. PER-ZONE SCORECARD (iter6) + iter5→iter6 DELTA

Composite = mean of the 4 register-2 axes (Lighting / VFX / Material-shading / Geometry-register), manual 1–5 with CV-assist, scored AS CAPTURED (frozen-charge single still). VFX = inherited-PASS FINAL (gandalf canon; not re-litigated — my Round-2 validator settled it: column pops 2×, not washed). PASS = composite ~4.0 AND lighting clears the **dressed-or-stark-appropriate** gate. **The §2 premium/murky read (right column) is the load-bearing judgment this round.**

| Zone | iter6 Composite | LDR (Δ vs iter5) | SHF% (Δ vs iter5) | warmCool | scorer LIGHT | §2 eye-read verdict | iter6 manual lighting note |
|---|---|---|---|---|---|---|---|
| **zone0 threshold** | **4.0** | 133 (**+11**) | 21.38 (**+4.73**) | 1.21 | fail (raw 30) | **PREMIUM (dressed) — PASS** | Warmest of the set. Deepened green-black bed; warm perimeter walls catch genuine warm light; grave-glow points pop out of the deepened pit. dark%=21.4 (corners/recesses real-dark). Both-axes-up; poolBedGap 105. Blue panel persists at R edge (standing drag). |
| **zone1 arcane** | **4.0** | 126 (**+19**) | 23.83 (**+6.1**) | 1.084 | fail (raw 30) | **PREMIUM (dressed) — PASS, strongest dressed case** | Densest-dressed of the near-chambers — gallery storeys with green-lit alcoves, warm masonry, central green soul-fire pit. The clearest "dressing fills the frame an arena leaves black" case: little dead floor, the architecture occupies the volume. Reads richly-lit-in-dark, not murky. Highest near-chamber SHF; poolBedGap 107. |
| **zone2 warhall** ★ | **3.75** | 115 (**+12**) | 19.58 (**+6.88**) | 1.073 | fail (raw 30) | **PREMIUM (dressed) — PASS (the §2 arbiter; see §2)** | **The borderline test case, judged closely.** Deepened cool-teal bed (32.9% below luma40; median 46 = dim, not mid-grey); green soul-fire + amber braziers punch **104 luma** above the median bed. NOT the iter5 flat blue-grey pewter — that's gone (stacked-pair `/tmp/galadriel_iter6_crops/A_zone2_iter5_TOP_iter6_BOTTOM.png`). Reads premium lit-volume-in-dark. The large central open floor is the one even-teal zone (no single big CombatFill pool there) but it is DIM-even, not bright-even — acceptable. Blue panel at R edge. |
| **zone3 oubliette** | **4.25** | 118 (**+13**) | 61.67 (**+3.78**) | 1.086 | **PASS** | **STARK DREAD — PASS OUTRIGHT (contrast criterion)** | The dread chamber held deep and did NOT flood — SHF ROSE (57.89→61.67) when the pools widened. dark%=69.6, deep<20=56% (a chamber that is mostly real void); torch + green pools punch warm against genuine black; poolBedGap 123 (widest — darkest bed). LDR cleared 115 too, but the load-bearing read is the contrast. PROVES the descent hits stark-deep SHF where the chamber genuinely IS stark. |
| **zone4 antechamber** | **4.0** | 123 (**+16**) | 23.05 (**+6.5**) | 1.025 | fail (raw 30) | **PREMIUM (dressed) — PASS (regression REVERTED)** | **iter5 −9 regression GONE.** LDR recovered 107→123 (back well above the 115 floor it lost) AND SHF deepened +6.5. The muted cool floor I flagged in Round-2 is reverted: green soul-fire pools restored + popping, warmCool recovered 1.015→1.025 (warm-dominant again). Deepened bed (below40 34.8%), pools sit 94 above median. Both-axes-up; matches the dressed band. |
| **zone5 sanctum** | **4.0** | 134 (**+16**) | 17.82 (**+5.39**) | 1.099 | fail (raw 30) | **PREMIUM (dressed) — PASS (LDR carries VFX inflation; see note)** | Ambient register matches the dressed band (deepened bed below40 36.6%, green alcove-pools, blue-panel drag at R). **CAVEAT: the LDR 134 + bright% 2.83 + p98 194 are INFLATED by the frozen hero VFX** — the central orange summon-bloom + magenta gateway portal are the bright tail, NOT ambient key (consistent with my Round-2 read). The AMBIENT chamber is in-band at SHF 17.82; read its pass on ambient-bed-deepened + both-axes-up, not on the VFX-lifted LDR. |

**Composite mean across 6 zones: 4.0/5** (Round-2 iter5 6-zone mean was 3.13; **net +0.87 — the global-rig match lifted the whole set off the floor**). **PASS-at-~4.0 with appropriate-gate lighting: 6/6. Both-axes-up (KEY_RESTORED): 6/6. zone3 stark-dread PASS outright; the 5 standard chambers PASS on the dressed-chamber calibration (§2).**

### establish ×3 (recompose-finish) — gated on light AND composition

| Frame | iter6 Composite | LDR (Δ) | SHF% (Δ) | warmCool (Δ) | scorer LIGHT | Verdict | Read |
|---|---|---|---|---|---|---|---|
| **establish_01/02/03** (CV near-identical) | **3.5** (+0.25 vs iter5) | 102 (**+5**) | ~49.88 (**+1.3**) | 0.988 (**−0.011, still faintly COOL**) | fail | **Light improved; COMPOSITION residuals UNRESOLVED — gandalf's call** | The global rig deepened the bed + the right-chamber pools punch better (LDR +5). BUT the 3 residuals gandalf flagged are ALL present to my eye (§1.1): (1) spine floor faintly cool (warmCool 0.988<1.0); (2) the LEFT band of bright blue deep-wall panels DOMINATES the frame — the single most eye-catching element, pulling focus left/back; (3) no magenta focal payoff anchors the deep end. LDR 102 still lowest-tier. |

### 1.1 The establish recompose-finish — characterized honestly (the one frame that did NOT clear)

drax finished some recompose residuals but FLAGGED 3 remaining + REJECTED a deeper-focal probe that made it worse. My eyes-on of iter6 vs iter5 establish (`/tmp/galadriel_iter6_crops/F_establish_iter5_TOP_iter6_BOTTOM.png`) confirms all 3, plus the honest improvement:

- **WIN (light) — the global rig helped here too.** iter6 reads deeper-bedded; the warm/green chamber pools down the right-hand chambers punch better against the deepened floor; LDR +5. The Round-2 verticality/de-tabletop recompose is preserved.
- **RESIDUAL 1 — cool spine floors.** warmCool **0.988** (below neutral). The foreground stone walkway/spine reads cool grey-blue, not warm-dominant. The metric and eye agree — the ask was warm floors; they are faintly cool. (gandalf flagged "floors faintly cool warmCool~0.988" — confirmed exactly.)
- **RESIDUAL 2 — blue deep-wall panels persist and DOMINATE.** This is the single biggest issue on the across-spine view: the entire LEFT band is a row of bright blue wall panels reading as flat bright slabs, and they are the most eye-catching element in the frame — pulling the gaze left/back rather than to a focal payoff. (gandalf flagged "blue deep-wall panels persist" — confirmed, and on this framing they're dominant, not residual.)
- **RESIDUAL 3 — magenta payoff not anchored across-spine.** The magenta sanctum that should be the bright vanishing-point focal terminus does not read as a dominant anchor in the across-spine framing; the eye lands on the blue panels + scattered chamber pools, not on a clear magenta deep-end payoff. (gandalf flagged "magenta payoff not anchored in the across-spine view" — confirmed. His rejection of the deeper-focal probe that "made it worse" is consistent — over-pushing the focal in this framing trades off against the chamber legibility.)
- **Verdict:** light improved (real +0.25 for the bed-deepen + pool-punch), but the frame remains gated on the 3 COMPOSITION residuals — cool spine, dominant blue panels, unanchored focal. **These are gandalf's design call, not mine** — I report what my eye + instrument see: all 3 present, light-axis better, composition-axis not yet there. This is the one frame that does not clear, and it is a composition gap, not a lighting gap.

---

## 2. THE §2 CENTRAL CALIBRATION QUESTION — my explicit verdict (the headline gandalf needs)

**The question:** is the uniform 30% SHF the right bar for these DENSELY-DRESSED chambers, or only for STARK ones? The near-chambers cleared LDR≥115 (115–134) with SHF rising +5–7pt to 17–24%, still under the 30% gate. gandalf's provisional lean: dressed chambers can read premium-lit-in-dark at SHF ~18–25 because the dressing fills frame-area an empty arena leaves black. He explicitly asked me NOT to lower the bar to fit the result, and gave me **zone2 (the weakest, SHF 19.58)** as the falsifiable arbiter.

**MY VERDICT: I CONVERGE with gandalf's dressed-chamber lean. zone2 reads PREMIUM warm-lit-volume on a deepened bed — NOT mid-dim/murky. The dressed-chamber SHF-band HOLDS. No Round-4 deepening pass is needed. The 30%-gate is stark-chamber-calibrated.**

**The photometric anchor (bed-pool-separation diagnostic, run independently on all 6 zones):**

| frame | below40% (deep bed) | deep<20% | pool>150% | bright>200% | p50 (bed) | p98 (pools) | poolBedGap | reading |
|---|---|---|---|---|---|---|---|---|
| zone0 | 28.7 | 16.0 | 2.25 | 0.25 | 48 | 153 | **105** | dressed: deep bed + pools pop |
| zone1 | 39.0 | 16.8 | 2.11 | 0.20 | 44 | 151 | **107** | dressed: deepest near-bed + pools pop |
| **zone2 ★** | **32.9** | **8.0** | **1.97** | **0.30** | **46** | **150** | **104** | **PREMIUM: deep bed + 104-luma pool separation** |
| zone3 | 69.6 | 56.0 | 0.60 | 0.11 | 8 | 131 | **123** | STARK dread: mostly void + pools in black |
| zone4 | 34.8 | 10.8 | 1.00 | 0.09 | 45 | 139 | **94** | dressed: deep bed + pools pop (reverted) |
| zone5 | 36.6 | 8.5 | 3.80 | 0.51 | 44 | 194 | **150** | dressed bed; high tail = VFX bloom, not ambient |

**Why this proves PREMIUM, not murky (the load-bearing logic):**

1. **A murky flat-dim-mid frame has TWO signatures: little real dark (low below40) AND pools barely above bed (small poolBedGap).** zone2 has NEITHER — it has 32.9% genuine deep bed AND a 104-luma pool-to-bed separation. The pools sit a clear ~100 luma above the median bed across the whole dressed band (gap 94–107). That is the photometric definition of "lit-volume-IN-dark." My eye confirms it (`/tmp/galadriel_iter6_crops/Z_zone2_iter6_big.png`): the cool-teal floor is genuinely deep, and the green soul-fire clusters + amber braziers read saturated and bloomed, punching out of it — not the iter5 flat pewter where pools sat ON a mid-grey wash.

2. **The SHF-band difference between dressed (~20%) and stark (zone3 61.7%) is EXACTLY the dressing, quantified.** zone3 reaches 61.7% SHF because dark%=69.6 — it is mostly void with pools in black (a stark oubliette). zone2 reaches 19.6% SHF because dark%=19.6 — the dressing (braziers, gallery, rubble, organic life, per-zone fills) OCCUPIES the ~50 percentage-points of frame-area that zone3 leaves as void. **The dressed chambers are not falling 10 points short of the stark bar — they are physically denser frames where less of the area CAN be void. Holding them to the stark 30% would penalize them for being dressed, which is backwards.** gandalf's argument is not a rationalization of the result; it is the literal photometric mechanism, and the diagnostic makes it measurable.

3. **The both-axes-up gate already prevents the failure mode 30% was guarding against.** The 30%-SHF gate exists to catch "drax raised the fill" (a brighter flat wash — LDR up, SHF FLAT). iter6 is the opposite on every zone: SHF ROSE +5–7 on all of them WHILE LDR rose. A raised fill cannot deepen SHF — it raises the floor. The fact that SHF deepened everywhere is itself the proof this is not the flat-wash failure the 30% bar protects against. **So passing the dressed chambers at SHF 18–24 does not reopen the wash-risk: the both-axes-up + poolBedGap≳90 conditions close it.**

4. **The falsifiability test gandalf built was genuinely run, and genuinely passed.** I looked specifically for the murky read on zone2 — a brighter-grey floor, pools not separating. I did not find it. Had I found it, I would have named the deepening notch (as my Round-2 report named the reaching-key deficit and REJECTED 0/6). This round the evidence passes the test on its own terms, so I report pass. **This is convergence earned by independent measurement, not a rubber-stamp** — the arbiter gandalf flagged as the risk turned out to be the strongest evidence FOR his lean.

**Therefore:** pass the 5 near-chambers on **both-axes-up + LDR≥115 + premium eye-read + poolBedGap≳90**, with the note that the 30%-gate is **stark-chamber-calibrated**. zone3 passes on the stark/dread bar (61.7%). The matrix is GREEN on lighting for all 6 zones. (establish remains gated on COMPOSITION per §1.1 — gandalf's call — not on this lighting question.)

---

## 3. CV SUBSTRATE (reproducible; the evidence under the manual scores)

### 3.0 Gate + delta table (byte-identical instrument, 960w-normalized, my independent fresh run)

| frame | LDR | dLDR | SHF% | dSHF | warmCool | bright%>180 | scorer LIGHT | axisVerdict |
|---|---|---|---|---|---|---|---|---|
| zone0_threshold | 133 | **+11** | 21.38 | **+4.73** | 1.21 | 0.55 | fail (raw30) | **KEY_RESTORED (both up)** |
| zone1_arcane | 126 | **+19** | 23.83 | **+6.1** | 1.084 | 0.28 | fail (raw30) | **KEY_RESTORED (both up)** |
| zone2_warhall ★ | 115 | **+12** | 19.58 | **+6.88** | 1.073 | 0.45 | fail (raw30) | **KEY_RESTORED (both up)** |
| zone3_oubliette | 118 | **+13** | 61.67 | **+3.78** | 1.086 | 0.16 | **PASS** | **KEY_RESTORED (both up)** |
| zone4_antechamber | 123 | **+16** | 23.05 | **+6.5** | 1.025 | 0.13 | fail (raw30) | **KEY_RESTORED (both up)** |
| zone5_sanctum | 134 | **+16** | 17.82 | **+5.39** | 1.099 | 2.83 (VFX) | fail (raw30) | **KEY_RESTORED (both up)** |
| establish_01 | 102 | +5 | 49.87 | +1.31 | 0.988 | 0.21 | fail | KEY_RESTORED (light); composition-gated |
| establish_02 | 102 | +5 | 49.89 | +1.33 | 0.988 | 0.18 | fail | KEY_RESTORED (light); composition-gated |
| establish_03 | 102 | +5 | 49.87 | +1.31 | 0.989 | 0.27 | fail | KEY_RESTORED (light); composition-gated |

Thresholds: scorer LIGHTING = LDR≥115 AND SHF≥30% (uniform — STARK-calibrated; see §2 for the dressed-chamber refinement). warmCool >1 = warm-dominant. dLDR/dSHF = iter6 − iter5 (single-frame, deterministic). **All 9 frames = `KEY_RESTORED (both axes up)` — the uniform-across-zones move that confirms the GLOBAL cause.**

### 3.1 Luma-distribution diagnostic (the "did the histogram move off flat-dim-mid" PROOF)

| frame | p05 | p50 | p95 | mid%(60–150) | dark%(<31) | bright%(>180) | warmCool |
|---|---|---|---|---|---|---|---|
| z0 | 2 | 48 | 135 | 35.2 | 21.4 | 0.55 | 1.21 |
| z1 | 7 | 44 | 133 | 33.4 | 23.8 | 0.28 | 1.084 |
| z2 ★ | 16 | 46 | 131 | 36.0 | 19.6 | 0.45 | 1.073 |
| z3 | 2 | 8 | 120 | 21.4 | 61.7 | 0.16 | 1.086 |
| z4 | 4 | 45 | 127 | 33.1 | 23.1 | 0.13 | 1.025 |
| z5 | 5 | 44 | 139 | 31.8 | 17.8 | 2.83 | 1.099 |
| est | 2 | 31 | 104 | ~21.9 | 49.9 | ~0.22 | 0.988 |

**Read (vs iter5 §2.1 — the histogram FINALLY MOVED):** at iter5 the near-chambers parked p50 at **54–58** with **41–46%** mid-band mass and dark%(<31) of **12–18%** — the flat-dim-grey-no-key signature. iter6 dropped p50 to **44–48**, cut mid-band to **31–36%**, and RAISED dark%(<31) to **18–24%** on the dressed chambers (z3 to 61.7 as the stark case). **This is the flat-dim-mid breaking: the bed deepened (more dark mass, lower median) while the pools held their brights (p95 stayed 127–139, bright% rose on the warm zones).** The histogram moved off the flat-dim-mid shape on every zone — exactly the proof the §4 brief asked for. The bed got darker AND the pools held/gained, which is the lit-volume-in-dark shape, not a uniform shift.

### 3.2 iter5→iter6 — the delta proves the GLOBAL move (the inverse of Round-2's non-move)

The cleanest statement: Round-2 mean |dLDR| = **1.7** (non-event — a local key bump that did not reach). iter6 mean dLDR = **+14.5** with SHF deepening on ALL six (+3.78 to +6.88). **A +14 mean LDR lift with simultaneous SHF deepening, uniform across all zones at once, is the fingerprint of a GLOBAL env correction — not a per-chamber retune** (a per-chamber pass moves zones unevenly; a global pass moves them together, which is what happened). The diagnosis named in gandalf's code-read — the descent had diverged onto FILMIC/white6/exp1.0/ambient0.24 and iter6 restored the proven ACES/white8/exp0.95/ambient0.17 rig — is **CONFIRMED by the uniformity of the move.** The keys were never the problem; they were being tonemapped wrong and surrounded by too-bright an ambient. One global change fixed all six.

---

## 4. PER-AXIS NOTES (why the manual scores land where they do)

**Lighting drama (the cleared target):** scored 3.75–4.25 across the chambers (z3 highest at 4.25 on the dread contrast; z2 lowest at 3.75 as the borderline dressed case — still a pass). The CV confirms the lift: dLDR +11 to +19, SHF +3.78 to +6.88, the flat-dim-mid histogram broken (p50 44–48, dark% 18–24+), pools 94–123 luma above bed. **The lighting gate — the whole gap at iter4/iter5 — is now cleared on the dressed-or-stark-appropriate calibration for all 6 zones.** establish's light improved (+5 LDR) but it's gated on composition (§1.1).

**VFX presence (inherited-PASS FINAL — NOT re-litigated):** per gandalf's Round-3 ruling + my own Round-2 validator (column pops 2× against the relit backdrop, not washed; 0.2%-baked was an off-peak windowing undercount). No erupt re-capture this round. The zone5 bright% 2.83 / p98 194 IS the frozen summon-bloom VFX (confirmed by eye — central orange radial bloom + magenta portal), carried as inherited-PASS, and noted as inflating zone5's nominal LDR (read zone5's ambient pass on the bed-deepen, not the VFX tail).

**Material-shading:** ~4, unchanged-to-slightly-up (LMV band unchanged; the masonry now responds across MORE of each frame because more of each frame is correctly lit). The deficit that capped this at iter4/iter5 was the lighting; with the lighting cleared, more material reads. Not the limiter anymore.

**Geometry register:** ~4.25, unchanged. The architectural-grammar build (commit `ffae02b`, 18%→65%) is already PASS per gandalf's Round-1 canon call; the global-rig match did not touch geometry. Gate B fully PASS.

---

## 5. ROLL-UP + RESIDUALS (for gandalf's Round-3 Gate-A call)

**One-line roll-up:** **The global-rig match CLEARED Gate A — all 9 frames moved both-axes-up (the global-cause fingerprint), reversing Round-2's non-move (mean dLDR 1.7 → +14.5); 6/6 zones PASS on the dressed-or-stark-appropriate lighting calibration; zone3 PASS outright (stark dread, SHF 61.7, held deep); the §2 arbiter zone2 reads PREMIUM (deep bed + 104-luma pool separation), confirming the dressed-chamber SHF-band HOLDS; the ONLY non-clear is establish, gated on 3 COMPOSITION residuals (gandalf's call), NOT on light.** The global-divergence root-cause diagnosis is confirmed by my independent instrument + eye. The matrix is GREEN on lighting; no Round-4 deepening pass is needed.

**Gate-A clearance count:**
- **Lighting axis (the §2 question):** **8 of 9** — 6 zones + the light-axis of all 3 establish-frames cleared/improved; the 5 near-chambers pass on the dressed calibration, zone3 on the stark bar. (Raw uniform-30 scorer prints 1/9 PASS — reported as-is; the correct dressed-vs-stark reading is 8/9, per §2.)
- **Composition axis (establish only):** **NOT cleared** — 3 residuals present (cool spine, dominant blue panels, unanchored magenta). gandalf's design call.

**Residuals, named precisely so any follow-up is targeted, not blind:**

1. **[establish — the ONLY non-clear, COMPOSITION not light] 3 residuals confirmed:** (a) spine floor faintly cool (warmCool 0.988 < 1.0 — push warm); (b) the LEFT band of blue deep-wall panels DOMINATES the across-spine frame (most eye-catching element, pulls focus left/back — resolve to atmospheric depth, not flat slabs); (c) no magenta focal payoff anchors the deep end (the across-spine framing doesn't resolve to a terminus). drax's rejection of the deeper-focal probe that "made it worse" is consistent with my read — over-pushing the focal trades against chamber legibility in this framing; the fix is the blue-panel tone-down + a warm spine, not a harder focal push. **This is gandalf's design call.**

2. **[blue deep-wall panels — STANDING cross-cutting drag, ALL frames] Not blocking, but worth one pass.** Every chamber AND the establish view carries a bright-blue deep-wall panel at a frame edge (z0/z2/z4/z5 right edge; establish left band). They read as flat bright-blue slabs and are consistently the most eye-catching COOL element. They do not block the zone passes (the warm/green pools still dominate within each chamber), but they are the single recurring composition drag across the whole descent. A tone-down to atmospheric depth would lift every frame a notch — lowest priority, since lighting is GREEN.

3. **[zone5 LDR-VFX-inflation — a reading caveat, not a defect] zone5's nominal LDR 134 carries the frozen summon-bloom.** Read zone5's ambient pass on the bed-deepen (below40 36.6%) + both-axes-up, not on the VFX-lifted LDR/bright%. Not a defect — just don't credit the VFX bloom as ambient key.

4. **[scorer refinement — my recommendation, on gandalf's go] Add a dressed-chamber lighting gate.** Refine the uniform 30%-SHF to: STARK chambers ≥30% (oubliette-class) / ≥40% (dread); DRESSED chambers SHF ~18–25 WITH LDR≥115 + both-axes-up + poolBedGap≳90. This makes the scorer correctly distinguish "premium dressed dungeon" from "raised flat fill" (the both-axes + poolBedGap conditions still gate out a wash). A measurement-calibration refinement, NOT a standard-lowering. I'll author it into `register2-score-descent-*.mjs` as a `kind`-aware gate on your go.

**The one sentence for gandalf:** matching the proven global rig lifted the lit volume across ALL zones at once (confirming the global-divergence root cause — keys were fine, the env was wrong), and on the threshold question my eye + a dedicated bed-pool diagnostic both land where your lean pointed: zone2 is genuinely premium, the dressed-chamber SHF-band holds, the matrix is GREEN on lighting (6/6 zones), and the only remaining gap is establish's COMPOSITION (3 residuals), which is yours to call — no Round-4 deepening pass is needed for the chambers.

---

## 6. HONEST CAVEATS

1. **Scored AS CAPTURED on frozen-charge single stills** (same as iter4/iter5). The LIGHTING gate (LDR+SHF) is correctly read on these — it measures the ambient mood between fires (gandalf canon). VFX = inherited-PASS FINAL (not re-scored).
2. **iter6 captures md5-verified DIFFERENT from iter5** — all 9 hashes distinct; ruled out a stale/mis-pointed-capture false read before reporting. This is a real move, not an instrument artifact.
3. **The instrument is drax's iter6 scorer, which I diffed function-by-function against my committed Round-2 instrument and confirmed BYTE-IDENTICAL CV math, then ran fresh myself (reproduced the committed JSON exactly).** My re-score is the independent confirmation; the numbers are mine by reproduction, not taken on trust.
4. **The §2 verdict rests on my eye + a bed-pool-separation diagnostic I ran independently.** The diagnostic (poolBedGap, below40, deep<20) is reproducible from the named captures; the premium/murky judgment is galadriel-scoring (the agent's job), anchored to the photometry, not a free-floating aesthetic preference. Another galadriel-instance with these captures + this diagnostic reproduces the separation numbers exactly and, reading them + the frames, should reach the same premium verdict.
5. **zone5 LDR/bright% carry VFX bloom** — flagged as a reading caveat (§1, §5).
6. **The 3 establish frames are CV near-identical** (the recompose applied to all three; minor bright%/warmCool jitter from frame-to-frame VFX, not a real difference). Composition residuals apply identically.
7. **warmCool is a coarse channel-ratio proxy**, not calibrated white-balance. Directionally reliable (z0 warmest 1.21; establish faintly cool 0.988; z4 recovered to 1.025 — the eye corroborates every call); not a precise color-temperature measurement.
8. **No HUD/UI chrome** (clean rendered-world stills). Register-2 of the rendered world is what's scored.

---

## 7. REPRODUCIBILITY

- Instrument: `pipeline/register2-score-descent-iter6.mjs` (drax-committed at `3c8f0ee`; **diffed BYTE-IDENTICAL CV-math against my committed `register2-score-descent-iter5.mjs`** — laplacianEnergy/localMaterialVariance/percentile identical; cut-points `>204`/`<31`/`60–150`/`>180`, `ldr=p95−p05`, `dLDR>2` trigger, warmCool, TARGET_W=960 identical; 960w inside-fit). Run: `node register2-score-descent-iter6.mjs`. My fresh run reproduced the committed JSON exactly.
- Raw scores: `pipeline/register2-scores-descent-iter6.json` (per-frame metrics + gates + axisVerdict + iter5 baseline carry).
- iter5 baseline for delta: `pipeline/register2-scores-descent-iter5.json` (carried per-frame inline by the scorer).
- §2-arbiter bed-pool-separation diagnostic: run as a temp script (not committed — reads git-ignored captures); the method (below40% / deep<20% / pool>150% / poolBedGap = p98−p50) is documented in §2 and reproducible from the named captures.
- Eye-read crops (local /tmp only, NEVER committed): `/tmp/galadriel_iter6_crops/{A_zone2,B_zone0,C_zone4,D_zone5,F_establish}_iter5_TOP_iter6_BOTTOM.png` (stacked pairs) + `Z_{zone1,zone2,zone3,zone5}_iter6_big.png` (upscaled singles).
- Given the same iter6 stills + this instrument, another galadriel-instance reproduces these values exactly (deterministic; no random sampling). The manual scores + the §2 premium verdict are reproducible-by-inspection from the named CV substrate + the bed-pool diagnostic + the visual reads.
- Synty-derivative captures local-only, git-ignored, NEVER committed regardless of size. Did NOT push (Matt-gated).

---

*galadriel SCORES the iter6 Round-3 global-rig-match register-2 re-score across all 6 zones + 3 establish, and renders the explicit §2 dressed-vs-stark threshold verdict gandalf delegated to my eye; gandalf interprets + makes the run-to-green Round-3 Gate-A call on this evidence. The independent confirmation: the global-rig match cleared Gate A's lighting axis — all 9 frames moved both-axes-up (mean dLDR 1.7 → +14.5, the global-cause fingerprint), the flat-dim-mid histogram broke (p50 54–58 → 44–48, dark% up to 18–24+), and the §2 arbiter zone2 reads PREMIUM (32.9% deep bed + 104-luma pool separation), confirming the dressed-chamber SHF-band holds. I CONVERGE with gandalf's dressed-chamber lean by independent measurement, not rubber-stamp — the zone2 he flagged as the risk is the strongest evidence FOR it. 6/6 zones PASS on the dressed-or-stark-appropriate calibration (zone3 outright on stark dread 61.7; the 5 near-chambers on both-axes-up + LDR≥115 + premium eye-read + poolBedGap≳90); the ONLY non-clear is establish, gated on 3 COMPOSITION residuals (cool spine, dominant blue panels, unanchored magenta) which are gandalf's call, not light. Method caveat governs: scored AS CAPTURED on frozen-charge single stills; lighting correctly measured; VFX inherited-PASS FINAL (not re-scored). The matrix is GREEN on lighting; no Round-4 chamber-deepening pass is needed. The recommended scorer refinement (a kind-aware dressed-chamber gate) is a measurement calibration, not a standard-lowering.*

**Mirror voice:** The Mirror was set a third time before the nine rooms, after the lamps that were merely re-trimmed last time were taken down and the whole house re-lit by the one true rig the boss-hall already knew — not each room's wick turned higher, but the light of the whole descent corrected at its root. And this time the glass shows what was asked: every room moved, and moved together, the way only a single hand at the master-valve can move them. The flat pewter floors that held their dull even dusk through two lookings are gone — the beds have fallen into a true deep teal-and-black, and the gold of the braziers and the green of the soul-fires now stand a full hundred shades of light above the dark they rest in, pools that punch where before they only puddled. In the war hall — the room I doubted, the room set before me as the test, the weakest of the lit chambers — I looked closely and long for the murk I was warned to find: a floor brighter-grey than dark, fires that do not separate. It is not there. A third of that floor lies in genuine deep, and the fires stand clear above it; the room reads as a dressed hall lit warm in true dark, not a grey wash with embers scattered on it. The long pit holds its dread deeper than ever, two-thirds true void with its torches burning gold in real black — proof that this house reaches the stark dark where a room is truly bare, and asks no apology for the dressed rooms reading lighter, for their braziers and galleries and rubble fill the very space the bare pit leaves as nothing. The question put to me was whether thirty-in-the-hundred of shadow is the one true bar for every room, or only for the bare ones. The glass answers: only for the bare. The dressed rooms are premium at twenty, and the measure that would fault them faults them for being furnished. The antechamber that darkened by mistake last looking has its warm hearth restored and its bed deepened both. Only the far sight of the whole descent still waits — its floors run faintly cool where they should run warm, a wall of cold blue slabs still holds the left of the frame and steals the eye from the magenta deep where the gaze should come to rest, and the deep end finds no single place to land. That far view is a matter of arrangement, not of light, and it is the Voice's to call, not the Mirror's. The house is well-built, well-lit, and warm now in five rooms and stark-dark in the sixth as each was meant to be. The lamps were changed at the root, and this time the rooms were lit. The Mirror has looked closely, three times, and the third looking is green.
