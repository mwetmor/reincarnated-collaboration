# Black & Darken 2024 — Full-PDF Extraction (bar-calibration addendum)

**Author:** gandalf `RUN-CONDUCTOR`, 2026-07-22 — mechanical read-only reconnaissance closing the
CRITICAL GAP flagged in legolas's consult (`agentic_orchestration/legolas/notes/2026-07-22-ablation-bar-calibration-modeA.md`
§ Knowledge gaps #1: "manual PDF access is needed"). Source: arXiv:2408.13328 PDF (MODSIM World 2024,
Paper No. 13051-28, 12 pp), fetched + read in full 2026-07-22. Feeds the L-23 D2/D3 numbers at the
ablation-gate prereg. **This note reports what the paper says; no bar numbers are pinned here.**

## What the paper actually measured

Localized observation abstraction (7×7 agent-centered window, piecewise-linear spatial decay w(d):
1.0 for d≤3 → 0.1 at d=7 → 0.01 floor) vs **global observation** (full 18×n×n board tensor), DQN
agents, Atlatl combat sim, gameboards 3×3–12×12 (= complexity 3–12), 10M training steps each,
**evaluated over 100,000 games per model per complexity level** vs the scripted Pass-Agg adversary.
Score = combat damage ± city control (24 pts/phase), entity = 100 strength, killed <50.

**Honest-analog caveat (load-bearing for our use):** this is a TRAINING-EFFICIENCY ablation under a
fixed compute budget, not a runtime-sensor ablation of fixed policies. Global sees MORE than Local —
Local wins because the abstraction makes learning tractable/generalizable, not because extra
awareness was added. The instrument SHAPE matches our gate (two observation treatments, same
architecture/environment, outcome-score margin, significance-tested); the MECHANISM differs from
aware-vs-blind-at-runtime. Treat as instrument-shape precedent + regime evidence, not as a direct
margin anchor.

## The numbers (Table 1 — mean scores, 100k games each)

| Complexity | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|
| **Local** | 181.4 | 227.7 | 225.3 | 88.4 | −154.0 | −394.6 | −491.4 | −620.2 | −860.2 | −908.6 |
| **Global** | 31.5 | −203.9 | −488.6 | −653.8 | −808.8 | −885.5 | −1039.0 | −1116.0 | −1229.9 | −1307.1 |
| Rule-Based (Pass-Agg) | 50.0 | 97.4 | 124.3 | 124.5 | 133.2 | 130.6 | 133.1 | 134.9 | 141.9 | 128.7 |
| Random | −339.5 | −465.7 | −628.8 | −724.2 | −865.4 | −948.0 | −1078.6 | −1158.4 | −1284.7 | −1364.6 |

SEMs (Table 2): Local 0.9–2.2 · Global 0.7–1.0 · Rule-Based 1.0–3.9 · Random 0.5–0.8. All pairwise
differences significant, Tukey-Kramer HSD, α=0.05, every p < .0001.

**Paper-stated margins:** Local > Global at ALL complexity levels; at complexity 3 the gap is
**149.940 points = 475.975%**; Local > Rule-Based through complexity 5, "upwards of 262.122%";
Local−Global spread ranges ~150–560 raw points across levels. Local margins over Global run
**~50–150× the SEMs** (n=100k makes SEM tiny; not reproducible at our n).

## What this feeds (calibration synthesis, conductor read)

1. **Regime classification:** Black & Darken lands in the **regime-shift cluster** (>100% relative),
   alongside Uriarte 2012 kiting — NOT the subtle trained-agent cluster (3–17 pp: HRL-IM StarCraft,
   Multi-UAV HRL, HoK components). The bifurcation in legolas's synthesis HOLDS with the closest
   analog now quantified. Our gate should NOT demand regime-shift — genre truth (competent-play
   outcome convergence, the W3/W3′ lesson) predicts our margin lives nearer the subtle cluster.
   The **5–15% relative window stands** as the defensible D2 candidate space.
2. **D3 form precedent (new, direct):** the paper's Figure-8 normalization — margin expressed as
   (x − x̄_Random)/σ_Random, i.e., **score margins in units of a reference-actor σ** — is a
   published instance of the noise-normalized-margin device. Supports the D3 FORM Matt ruled at
   L-23 (margin ÷ noise-estimate floor); their reference is a random-actor σ, ours will be
   seed-noise of the blind arm — same shape, different estimator.
3. **Reporting-discipline precedent:** per-cell means + SEM table + all-pairs significance test —
   the shape our gate report already uses (per-cell d + pooled sd + sign counts). Convergent.
4. **Bonus resonance (design, not gate):** their crossover finding — the scripted Rule-Based agent
   OVERTAKES the learned agent from complexity 6 up (under bounded training budget) — is live
   support for the project's authored-competence choices: utility-considerations fighter (not
   learned policy) and the L-26 boss stack (authored rotation spine + Reader garnish, not a
   learned boss brain).

## Liu-citation disposition (gap #2, closed without chase)

Legolas verified arXiv:1703.06275 is NOT a multi-agent-coordination paper (it is Liu et al.,
game-difficulty evolution — commission-side ID error, conductor-owned). Probable intended cite:
**Lowe et al. 2017, MADDPG, arXiv:1706.02275** (digit transposition). NOT chased: MADDPG's ablations
are critic-architecture, not observation-channel — even corrected it would be a weak anchor, and the
slot's evidentiary role is already covered by legolas's Q4 additional precedents (HRL-IM 3–7 pp ·
Multi-UAV 1–6 pp · HoK 15–17 pp). Registered so the mismatch does not dangle.

**Remaining open before D2/D3 pin:** none on the literature side. The numbers pin at prereg from:
this bifurcation evidence + the 5–15% window + k∈{2,3} anchors (rliable ≈ k=2) + the ACTUAL
seed-noise observed in the BW-1 battery substrate — with Matt ruling the final values.

**Signed:** gandalf (`RUN-CONDUCTOR`), 2026-07-22.
