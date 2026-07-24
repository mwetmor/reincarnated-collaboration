# MCP-BAKEOFF — P2 judge-note (galadriel, judge channel)

**Date:** 2026-07-24 · **Charter:** run-charter §3/P2 · **Matrix:** `drax/captures/2026-07-23-mcp-bakeoff/MATRIX.md` (row P2, finding #2) · **Input for:** conductor (gandalf) verdict rec → Matt pick.

## Files inspected (all under `drax/captures/2026-07-23-mcp-bakeoff/`, plus my pipeline)

- **Pro** `pro/P2_compare_moved.json` wire payload: `{changed_pixels: 244419, total_pixels: 2135040, diff_percentage: 11.45, threshold: 10, size: "1920x1112"}` + 2nd content `type:image` (743 656-B base64). `pro/P2_compare_identity.json` = 0.09 % (1966 px), same `threshold: 10`. `pro/P2_diff_AC.png` (native diff) + `P2_editor_a.png`/`_c.png` (inputs).
- **Incumbent** `incumbent/p2_similarity_report.json` (MSE 0.0049 / RMSE 0.070 / 92.98 %) + `p2_diff_a0_vs_a180.png` / `_a0.png`.
- **My instrument** `galadriel/pipeline/descent-similarity-vs-reference.mjs` — HSV-hue histogram cosine (36-bin, S·V-weighted) + Laplacian/Canny edge-density + register-ratio axes vs reference centroid.

## Q1 — Artifact-class sufficiency: NO, not for register/perceptual verdicts

Look at `P2_diff_AC.png`: the **entire** grid, gizmo axes, and sky band flood red. Yet inputs A/C (`P2_editor_a/c.png`) are the same empty KT3 grid from a marginally rotated camera — content-identical. Pro's `threshold: 10` is a fixed **raw per-channel** cutoff; every anti-aliased grid line shifted sub-pixel by camera motion trips it. The 11.45 % / 244 419 px is almost all AA-line re-rasterization, **not** semantic change — the exact failure mode my HSV+edge-density register scoring rejects (SSIM/perceptual reads these near-identical). Two further limits: (a) it diffs the **whole editor chrome** (docks, toolbar), so UI churn contaminates the score — not subject-isolated; (b) raw counts carry no AA tolerance, no lighting normalization, no per-region weighting. **My pipeline outclasses it where it matters.** The incumbent's `p2_similarity_report.json` (MSE/RMSE) is the same raw class — and its "diff" PNG is not a delta at all, it's the a180 frame.

## Q2 — Operational value of in-wire diff: YES, real and new

An agent-callable diff **mid-run**, no external-CV hop, is genuinely new to my pattern. It buys a **fast in-wire regression tripwire** — "did this frame change vs last known-good?" — cheap per conductor-eye step. Identity 0.09 % proves the floor works (stable frames read ~0). For gross detection (moved / broke / went blank) it is a legitimate conductor-eye instrument without invoking my pipeline. A **coarse tripwire, not a judgment.**

## Q3 — Verdict for the conductor: **PARTIAL**

Pro's P2 justifies a second stack **for my channel in one narrow slot only.**

- **Use Pro `compare_screenshots` for:** in-wire mid-run **change-detection tripwires** — blank/regression alarms, "did anything move" gates on conductor-eye steps, quick same-camera A/B. Its diff PNG usefully localizes *where* pixels moved.
- **Stays external (the deciding instrument):** every **register/perceptual/similarity verdict** — DoE-reference scoring, AA- and lighting-tolerant comparison, HSV+edge register scoring, anything folding into `style-register.md`. Raw threshold-10 counts are not defensible there.

Not a displacement — a **cheap in-wire pre-filter feeding my instrument.** Per matrix finding #4, P2 alone does not carry the pick (native P4 freeze/step is incumbent-only; my channel does not weigh on P4).

---

**The Mirror voice:** the paid tool paints the whole grid red and calls a still camera a change. It counts pixels; it does not see. That is a fine bell to ring mid-run — but the eye that judges the picture stays mine.

**Signed:** galadriel (judge channel), 2026-07-24.
