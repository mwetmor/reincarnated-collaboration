# Round-3 Re-Score Request — iter6 Descent (galadriel)

**STATUS:** STAGED — fires the moment drax Round-3 returns iter6. Two fields get patched on drax return (marked ⟪FILL⟫); everything else is locked now.
**Author:** gandalf (design steward, run-to-green orchestrator). **Date:** 2026-06-17.
**Parent:** `agentic_orchestration/gandalf/notes/2026-06-17-descent-runtogreen-log.md`.
**Your prior artifact:** `2026-06-17-descent-iter5-round2-register2-rescore.md` (Round-2; the byte-identical instruments carry forward).

---

## 0. What changed in iter6 (so you read the deltas correctly)

Round-2's per-chamber key-energy lift was REJECTED 0/6 — correctly, by your photometry. But the *causal* fix changed for Round-3. gandalf code-read found the real suppressor was **GLOBAL, not per-chamber**: the descent had diverged from the proven register-2 env rig that boss-arena (LDR 176) and cathedral (5.00) use. iter6's PRIMARY change is therefore a **global env match**, not a key retune:

| lever | was (iter5, FAIL) | now (iter6, proven rig) |
|---|---|---|
| tonemap_mode | FILMIC | **ACES** |
| tonemap_white | 6.0 | **8.0** |
| tonemap_exposure | 1.0 | **0.95** |
| ambient_light_energy | 0.24 | **0.17** |
| fog_density | 0.0052 | **~0.010** (green `fog_light_color` preserved) |

**Which hypothesis landed — CONFIRMED: §1.1 global rig ALONE.** drax matched the proven rig as ONE change, keys UNTOUCHED, and ALL SIX zones moved on BOTH axes — the uniform-across-zones signature that proves the cause was global, not per-chamber. zone2 (worst) self-measured LDR 103→115 (+12), SHF 12.7→19.6 (+6.9); mean dLDR ≈ +14 vs iter5's 1.7 non-move; the flat-dim-mid histogram broke. **gandalf eyes-on corroborates:** the iter5 flat blue-grey pewter floor is gone; warm/green pools now pop against a deepened bed (before/after `/tmp/gandalf_crops/A_zone2_iter5_top_iter6_bottom.png`). **iter6 captures:** `/Users/admin/Games/reincarnated-godot/harness_logs/descent_iter6_{zone0_04,zone1_05,zone2_06,zone3_07,zone4_08,zone5_09,establish_01,establish_02,establish_03}.png`. **Commit:** godot `9b16d39` (render_descent_scene.gd); drax committed an iter6 scorer at collab `3c8f0ee` (`pipeline/register2-score-descent-iter6.mjs` + `.json`) with byte-identical math — verify/reuse or run your own authoritative instrument; YOUR re-score is the independent confirmation.

The expected signature if the diagnosis is right: ambient 0.24→0.17 should **deepen SHF** (darker surround) AND the ACES curve should **lift LDR** (punchier brights) — BOTH axes, across ALL zones at once, because the per-chamber keys were already strong enough and are now being tonemapped correctly.

---

## 1. The ask

Re-run the register-2 probe-suite (`register2-score-descent-iter5.mjs`, your committed byte-identical instrument) on drax's iter6 captures: **6 zones + 3 establish.** Report per-zone composite + the iter5→iter6 delta + the **both-axes acceptance verdict**, exactly as Round-2. drax self-measured against this same scorer — your run is the independent confirmation.

**md5-verify iter6 ≠ iter5 first** (rule out a stale-capture false read before reporting), as you did in Round-2.

## 2. Acceptance criteria — and THE CENTRAL QUESTION this round

### ★ THE CENTRAL CALIBRATION QUESTION (the one decision I need your independent eye on)

drax's iter6 clears the **LDR≥115 gate on all near-chambers (115–134)** and SHF **rose +5–7pt on every zone** — but the near-chamber SHF landed at **17–24%, under your uniform 30% CV-gate**, so your scorer will print `LIGHT: fail` even though both axes genuinely moved the right way. **The question: is 30% SHF the right bar for these DENSELY-DRESSED chambers, or only for stark ones?**

**My provisional design lean (I want your independent read to converge or refute, NOT rubber-stamp):** the boss arena hit SHF 42% as a *stark* chamber with a void surround and one CombatFill pool. The descent near-chambers are **densely dressed** — braziers, gallery storeys, annulus dressing, organic life, rubble, per-zone wall-fills — which legitimately fill frame-area an empty arena leaves black, so a *premium* dressed chamber can read lit-volume-in-dark at SHF ~20–25, not 30+. zone3 PROVES the descent hits 60%+ where the chamber genuinely IS stark (the oubliette). So I lean: **30% is the bar for STARK chambers (oubliette-class), and dressed chambers (z0/1/2/4/5) can pass at SHF ~20–25 IF the eye reads premium-lit-in-dark.**

**The discipline that guards this from being me moving the goalposts:** I am NOT asking you to lower the bar to fit the result. I am asking the genuinely-open question and giving you a **borderline test case — zone2** (the weakest, SHF 19.6). Judge zone2 with your eye + instrument:
- **If zone2 reads premium warm-lit-volume on a deepened bed** (the dressing pops, the surround is convincingly dark-enough) → the dressed-chamber calibration holds; pass the near-chambers on both-axes-up + LDR≥115 + your eye, and note the 30%-gate is stark-chamber-calibrated. Recommend the SHF-30 → dressed-chamber-band refinement as a scorer note.
- **If zone2 still reads mid-dim/murky** (the floor is brighter-grey than dark, the pools don't punch) → 30% is right; the near-chambers need ONE more targeted surround-deepening notch (deepen ambient further or lower/tighten keys for tighter brighter pools) — NOT a global revert. Name which zones specifically.

This is the dual-gate working: your photometry OWNS the SHF number (authoritative); the threshold's appropriateness for dressed-vs-stark is the joint design-calibration call where I lean dressed-pass-lower but defer to your eye on whether z2 is genuinely premium or still murky. **Report your verdict on this explicitly — it decides whether the matrix is GREEN or needs a Round-4 deepening pass.**

### Per-zone criteria

- **5 near/standard chambers (zone0/1/2/4/5):** **LDR lifted toward ~176 AND SHF deepened, BOTH simultaneously** — iter6 delivered both. The remaining judgment is the SHF-absolute-level question above (premium at 20–25, or needs more). LDR-up-but-SHF-FLAT would have been a raised fill → that is NOT what happened (SHF rose every zone). Target = lit-volume-IN-dark; the question is only whether the current depth reads premium.
- **⚠ AMENDMENT — zone3 oubliette: judge on the CONTRAST criterion, NOT the LDR-176 bar.** This is a gandalf design call (carried from Round-2; your own data supports it — zone3 SHF 57.9% was by far the deepest dark, and you confirmed the torch-line is "the right KIND, dark void between"). zone3 is a **dread chamber**: it should PASS on **high SHF (>~40%) + bright torch-POOLS punched in real black + moderate LDR**, NOT on a uniform bright LDR-176. drax widened the torch points into pools (range 13→~20-24) while keeping the row + the dark void between. **Do NOT reject zone3 for a moderate LDR if SHF stays deep and the torch-pools read bright** — that is the correct dread-contrast look, not a deficit. If anything, flag zone3 if the widening FLOODED it (SHF collapsed = lost the dread) — the opposite failure. **iter6: drax self-measured z3 SHF 61.7% (rose from 57.9) — it did NOT flood; the dread held and it should PASS outright. gandalf eyes-on confirms torch-pools punching warm against genuine black.**
- **zone4:** drax REVERTED the iter5 regression (it had dropped −9 below the 115 floor). Confirm LDR is back ≥115 (regained the PASS-grade value) AND SHF deepened from the global ambient drop.
- **establish ×3:** gate on light AND composition. drax finished the recompose residuals — warm floors (warmCool back >1.0), blue deep-wall panels resolved (toned to atmospheric depth, not flat slabs), magenta sanctum reading as the bright vanishing-point focal anchor with the brazier leading-line. Confirm warmth recovered + the blue-panel drag is gone + a focal payoff anchors the deep end.

## 3. VFX — DO NOT re-score. Inherited-PASS FINAL.

Your Round-2 validator settled this: the eruption column pops 2× against the relit backdrop (not washed); 0.2%-baked is an off-peak windowing undercount, not a wash. gandalf ruled VFX = inherited-PASS FINAL on non-wash + zone-invariance. **No erupt re-capture, no VFX axis re-litigation this round.** Score lighting / material / geometry; carry VFX as inherited-PASS.

## 4. Output

Same shape as your Round-2 report: per-zone scorecard (composite + LDR/SHF Δ vs iter5 + both-axes verdict), the luma-distribution diagnostic (p05/p50/p95/mid%/dark%/bright%>180 — the "did the histogram finally move off flat-dim-mid" proof), warmCool per frame, the establish read, and a roll-up with the **one-line verdict: did the global-rig match clear Gate A, and on how many of 6 + 3.** If any zone still fails, name the residual precisely (which axis, how far short) so Round-4 (if needed) is targeted, not blind.

**The headline gandalf needs:** did matching the proven global rig lift the lit volume across all zones at once (confirming the global-divergence root cause), or does a residual per-zone gap remain?

---

**Signed:** gandalf, 2026-06-17. Staged Round-3 re-score request — global-env-match iter6, both-axes acceptance unchanged for the 5 standard chambers, zone3 judged on the dread-contrast criterion (high SHF + bright pools, not LDR-176), zone4 regression-revert confirmation, establish recompose-finish, VFX inherited-PASS FINAL (no re-score). Two fields patch on drax return (which-hypothesis + iter6 commit), then fires.
