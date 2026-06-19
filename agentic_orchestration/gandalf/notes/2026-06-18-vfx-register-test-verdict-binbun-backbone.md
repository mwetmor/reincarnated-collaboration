# VERDICT — VFX register-test (Gap #8): Binbun backbone + in-engine juice vs the T2 genre floor

**Author:** gandalf (design steward — Wave-3 adjudication; PASS/MARGINAL/FAIL is the design call). **Date:** 2026-06-18. **Type:** verdict + VFX-library decision memo (the buy-vs-build recommendation).
**Inputs:** the spec `notes/2026-06-18-vfx-register-test-spec-binbun-emission.md` (§6 verdict logic); galadriel's Wave-2 scorecard `galadriel/reports/2026-06-18-vfx-register-wave2-scorecard.json` + anchored ladder `galadriel/rubrics/2026-06-18-vfx-register-ladder-anchored-marks.json`; drax's 72-PNG render `reincarnated-godot/harness_logs/vfx_register_2026-06-18/`.
**Authority:** the verdict (MARGINAL) is mine to call. The downstream buy/build (commit or defer the Hovl harvest pipeline) is a RECOMMENDATION Matt ratifies.

---

## VERDICT: **MARGINAL** — Binbun backbone is register-VIABLE; the gap is in-engine-fixable, NOT a harvest mandate.

The in-engine juice lever is **proven on the energy axes** (bloom above T3, motion +26.2 — the "slightly under" Legolas flagged is **reversed** by the emission lever). The two shortfalls are **(1) hue — an in-engine tuning fix**, and **(2) depth — inconclusive** (under-layered build + a mis-windowed metric). Neither justifies committing the expensive harvest. The V2 cross-check independently leans against it. **Recommendation: DEFER the harvest, run a cheap V1.1 in-engine round, re-score.**

---

## 1. The scorecard (condensed — V1 is "the lever," V0 default, V2 flipbook)

| Load-bearing juice axis | T2 floor | V0 | V1 (lever) | V2 (flipbook) | V1−V0 delta |
|---|---|---|---|---|---|
| **HLF bloom** | 0.6 (T3=2.85) | 0.60 (at T2) | **3.47 (▲ above T3)** | 3.22 (above T3) | **+2.87 LARGE** |
| **Motion-presence** (temporal) | (no abs. anchor) | 41.3 | **67.5 (highest)** | 42.6 (least alive) | **+26.2 LARGE** |
| **Depth** (spell-region) | 18 (T1≤11) | ~7 (sub-T1) | ~3–6 (sub-T1, ≈V0) | ~2–4 (flattest) | **~0 / negative** |
| **Hue-legibility** | 0.66 (T3=0.88) | 0.94 (above T3) | 0.58 (T1–T2) | 0.86 WARMHI / 0.39 HI-gate | **−0.36** |

**The headline is the delta's SHAPE: large-positive on bloom+motion, null-on-depth, negative-on-hue.** Per spec §6 "the delta diagnoses the cause" — and it diagnoses cleanly.

## 2. What the delta means (the diagnosis)

**Energy axes (bloom + motion) — the lever WORKS, gap closeable in-engine, no harvest.** V1 doesn't just reach the bloom floor, it **overshoots T3** (3.47 vs 2.85), and it's the most *alive* cast (motion +26.2, growth 3.09×). This is the §6 best-outcome signal: the gap to genre-register on the "juice" axes is an **emission/post gap** — cheap, in-engine, no new assets. **Legolas's "Binbun reads slightly-under-register" is REVERSED by the emission lever on the axes that carry the juice.**

**Deficit 1 — HUE (an in-engine TUNING fix).** V1 drops to 0.58 (below the 0.66 floor) because raw additive blew **~22–26% of the bright region white** (achromatic, out of the fire band). But a **58–66% majority stays warm fire, and the eye reads V1 unmistakably as fire.** This is "premium-bloom-WITH-hue-cost," not illegibility — and it's a **knob, not a wall.** drax raw-additive'd the *whole* particle; the fix is the **PoE/D4 technique: a hue-locked core under an additive bloom halo** (additive only the glow, preserve the core color). In-engine. No harvest.

**Deficit 2 — DEPTH (INCONCLUSIVE, not a fail — two confounds).** All three variants sit below T1 on spell-region depth, and V1 doesn't lift it (additive *smooths* the bright core). But before reading this as a Binbun structural cap:
- **(a) Under-built:** drax added **one** ember sub-emitter; the PoE "composable detail" move wants **3–4 layered systems** (hue-locked core + mid-flame body + embers + smoke-wisp), each at a different depth/scale. The depth axis was barely exercised.
- **(b) Mis-windowed metric (galadriel confirms in her own caveat):** spell-region layering-variance gates on the **bright core (luma≥158)**, where additive bloom is uniform *by nature* — and the ember periphery (real depth, to the eye) lives **below** that gate. The metric measures depth where a fire spell has the *least* of it and **excludes where spell depth actually lives** (mid-luma body + ember field). The number under-credits V1's visible structure.

⇒ Depth is **inconclusive** (under-built + mis-measured), **not** a clean Binbun failure. It does **not** justify a harvest mandate. It justifies (i) a properly-layered V1.1 and (ii) **re-windowing the depth metric to the full spell region** (an O2/O4 rubric-ladder refinement).

## 3. Eye↔number adjudications (the dual-gate working — 3 divergences resolved)

1. **Hue (the crux):** number below-floor, eye reads fire. **I credit the instrument** — the white-hot core IS a real, visible quality cost the "looks juicy" eye would wave through. The dual-gate caught a fixable defect. Resolution: *reads fire, but the white core is a fixable tuning cost.* Fix = hue-locked-core + additive-halo.
2. **Depth:** number ≈V0, eye sees more (ember periphery). **I weight the eye** — the metric is mis-windowed (above). Refine the metric; don't conclude a cap.
3. **V2 hue:** WARMHI 0.86 reads high but the eye sees a pale puff; the **HI-gate (0.39) matches the eye** (⅔ white-blown core). Learning: for additive VFX, the **un-warm-gated HI hue read is more honest** than the warm-gated one — feed this into the rubric.

## 4. V2 cross-check (is the harvest even needed?) — leans AGAINST

V2 (Brackeys flipbook, a harvest proxy) **under-performs V1 on every juice axis** (bloom −0.25, motion −24.9, depth −1.82, growth −1.56×) — a pale, barely-growing, ⅔-white-blown puff. Per §6, V2 ≤ V1 ⇒ **"register-appropriate flipbooks don't beat the in-engine lever ⇒ no harvest needed."** **Caveat (galadriel's, and mine):** a *single* Brackeys sheet at emission 0.8 is a **weak Hovl proxy** — a real harvest yields richer multi-layer sheets. So this is *suggestive, not conclusive*: the cheap flipbook route did NOT out-juice Binbun. It removes the easy assumption that flipbooks are automatically better.

## 5. Test-coverage gap (for V1.1) — in-place, not a directed projectile

drax rendered a **centered in-place lifecycle** (emerge→grow→peak→fade, core fixed ~48% x), **not** the directed **cast→travel→impact** projectile the spec named. So **energy-travel + directionality were not exercised** (correctly flagged non-load-bearing here). For a 400-combo catalogue full of directed projectiles, that arc-juice axis is real and **untested.** V1.1 must include a **directed cast.**

## 6. RECOMMENDATION (buy/build — Matt ratifies)

**Do NOT commit to the Hovl harvest pipeline now.** The evidence says the backbone is register-viable with in-engine fixes; the only "structural" worry (depth) is confounded by an under-built variant and a mis-windowed metric.

**Run a cheap V1.1 in-engine round** (drax build + galadriel re-score on the same ladder), four named changes:
1. **Hue-locked core + additive halo** (fix the white-hot core; recover hue ≥ T2).
2. **3–4 composed depth layers** (core + mid-flame + embers + smoke-wisp — exercise the depth axis properly).
3. **A directed projectile** (cast→travel→impact — cover energy-travel/directionality).
4. **Re-window the depth/layering metric** to the full spell region (mid-luma body + ember field), not the bright-core gate (galadriel; O2/O4 rubric refinement).

**Decision gate after V1.1:**
- **If V1.1 clears T2 on depth + hue** → the harvest is **unnecessary**; Binbun backbone is **confirmed register-sufficient for the full 400-combo catalogue** (the big win — no pipeline to build).
- **If depth stays capped despite proper layering + a re-windowed metric** → *then* scope the Hovl harvest **for hero/signature slots only** (two-tier: Binbun for breadth, harvest for heroes), with **depth** named as the specific axis and its magnitude quantified — exactly the justification a harvest-build needs instead of a guess.

## 7. Process flags
- **Stage discrepancy (minor, non-verdict-affecting):** drax's build-note said a 0.10 dark-neutral background; the pixels rendered mid-grey ~129. The controlled comparison still holds (identical across variants; whole-frame metrics down-weighted), but V1.1 should **lock the background to a known value and verify the pixels match the spec.**
- **Harness self-close (your directive — landed):** the happy-path `get_tree().quit()` was already present; the orphaned windows were hung/killed debug iterations. drax added a **120s watchdog Timer → quit()** so even a hung capture self-closes; headless correctly rejected (viewport capture needs a real GL framebuffer). Committed `e71e989`. Recorded as standing discipline (spec §8).

---

**Signed:** gandalf, 2026-06-18. Verdict: **MARGINAL** — the juice lever is proven (bloom above T3, motion +26), the hue cost is an in-engine tuning fix, the depth shortfall is inconclusive (under-built + mis-windowed), and the flipbook cross-check leans against a harvest. **Recommendation: defer the harvest pipeline, run a four-fix V1.1, and let the depth+hue re-score decide — harvest only if depth stays capped after proper layering.** The cheapest path that protects the 400-combo breadth (Binbun) without committing a pipeline build on confounded evidence. Matt ratifies the buy/build.
