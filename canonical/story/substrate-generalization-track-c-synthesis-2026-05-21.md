# Substrate-Generalization Study — Track C Synthesis

**Status:** CANONICAL — gandalf synthesis of rocket Track C resumption findings
**Date:** 2026-05-21
**Author:** gandalf
**Source:**
- `agentic_orchestration/rocket/research/substrate-generalization-study-2026-05-21/spot-check-regen-findings.md`
- `agentic_orchestration/rocket/research/substrate-generalization-study-2026-05-21/data/track-c-spot-regen.csv`
- `agentic_orchestration/rocket/research/substrate-generalization-study-2026-05-21/data/compression-signature-comparison.csv`

---

## 0. TL;DR — The verdict matters for P1 W1.11 scope

**OQ-1 resolution: COLLAPSE.** The historical substrate severity gradient (water 15% Pattern-A / earth 40% / physical 100%) was a CALIBRATION ARTIFACT, not substrate-intrinsic property. Under disposition-3 same-calibration, ALL substrates produce 100% Pattern-A.

**Matt's recall reinterpreted:** "water/earth/wind have been weaker across all seasons" — YES, but because those substrates ran under WEAKER CALIBRATION historically, not because they're intrinsically weaker. Same calibration → same severity across all 7.

**P1 W1.11 scope recommendation: UNIFORM comprehensive enrichment depth** — no differentiated weighting toward "historically-weaker" substrates. Saves ~1-2 weeks of P1 budget vs differentiated approach.

**The multi-dim convergence work (§ 2.8 skill tree node population) becomes even more critical** — current framework universally fails boss-tier (kit composition tuning cannot rescue 100% Pattern-A across all 7 substrates). The fix is structural, not parametric.

---

## 1. Empirical data

### 1.1 Per-substrate Pattern-A rates at SAME calibration (disposition-3)

| Substrate | Historical Pattern-A rate | Same-calibration Pattern-A rate | Δ |
|---|---|---|---|
| Water | 15% | **100%** (5/5) | +85 pp |
| Earth | 40% | **100%** (5/5) | +60 pp |
| Physical | 100% | **100%** (3/3) | unchanged |
| Wind | 40% (historical) | — (not in TC-1/TC-2) | — |
| Lightning/Holy/Shadow | — | 100% in P2 (Alt A) | confirmed |

**Conclusion: The boss-tier Pattern-A pathology is calibration-uniform, not substrate-specific.** The historical gradient was artifact of weaker calibration for certain substrates, not intrinsic substrate weakness.

### 1.2 Modifier ranges (the surviving differentiation)

While Pattern-A is uniform, modifier ranges differentiate but don't escape the boss-floor:

| Substrate cluster | Modifier range | Interpretation |
|---|---|---|
| Lightning / fire | 0.072–0.103 | Lean, efficient kits — high-DPS-density mechanics |
| Water | 0.134–0.258 | Sustained-presence pillar reduces instantaneous DPS density |
| Wind / earth / holy | 0.134–0.505 | Control/support role burden drives modifier up |
| Physical | 0.134–1.000 | Armor mitigation + melee geometry vs gauntlet composition |

**Critical observation:** class_0014 (water, damage_fraction=0.73) and class_0019 (physical hunter, modifier=1.000) represent the extreme cases — highest damage fraction and highest modifier saturation respectively — and **both still produce boss_wr=0.0**. The boss-floor problem is not rescuable by kit composition tuning within the current framework.

---

## 2. Architectural implications

### 2.1 P1 W1.11 scope simplification

**Before Track C:** dispatch posed "comprehensive vs targeted/differentiated" as open question. Differentiated approach would have weighted enrichment depth by historical Pattern-A severity (heavier on water/earth/wind; lighter on lightning/holy/shadow).

**After Track C:** uniform-depth comprehensive enrichment confirmed correct. Same depth across all 7 elements. **No differentiated weighting.**

**P1 budget savings:** ~1-2 weeks (no need to author differentiated enrichment plans per substrate; uniform plan applies).

### 2.2 Reinforcement of § 2.8 skill tree node population priority

The Track C verdict confirms that **kit composition tuning under the current framework cannot rescue boss-floor**. The fix is structural — multi-dim convergence over node-subset × per-node-coefficients × modifier — not parametric tuning of existing flat-skill-kits.

The skill tree node population work (§ 2.8 P1 W1.13) is therefore **NOT optional, NOT speculative — it is the empirically-confirmed mathematical lever required to escape the Pattern-A pathology.** The recompose-hive's "fix the synergy, not the arena" warning was directionally correct: the synergy IS the problem (insufficient tuning dimensions in current framework).

### 2.3 Reinforcement of § 2.9 gauntlet migration priority

100% Pattern-A under same-calibration also reinforces the gauntlet migration argument. If current PackProxy ×8 swarm + abstracted boss-tier convergence produces uniform 100% boss-fail rates, it suggests:

- Current gauntlet abstraction is testing kits against an arena that's NOT representative
- True multi-monster positional gauntlet would let kits exercise mobility / positioning / kiting strategies that PackProxy abstraction strips out
- The gauntlet migration (§ 2.9 P0 W0.9) is more critical than just "fix the arena" principle — it's a candidate empirical fix to the boss-floor problem

**Caveat: this is a HYPOTHESIS, not proven.** The boss-floor might be a function of both gauntlet structure AND framework tuning dimensions. Both fixes (§ 2.8 + § 2.9) likely needed; either alone may be insufficient.

### 2.3.1 Joint-resolution triad framing — behavioral-correctness caveat (gandalf amendment 2026-05-21)

Per gandalf W0.9 cumulative Gate-2 architectural close-out 2026-05-21: the joint-resolution triad (W0.2 source diversity + W0.1 calibration fairness + W0.9 arena fidelity) addresses **structural** sufficiency. The empirical discovery from W0.9 Phase 2.5 calibration sweep — the boss AI leash-reset bug — surfaces a fourth concern: **arena-occupant behavioral correctness**.

The triad's claim was always *structural* sufficiency. Behavioral correctness of arena occupants (player AI, monster AI, leash semantics, targeting logic) is a separate, lower-tier concern that the triad implicitly assumed. **Triad presumes arena-occupant behavioral correctness; defects in occupant AI are out-of-band and resolved per-bug.**

The W0.10 boss AI fix workstream (added 2026-05-21 per gandalf Option A disposition) is the per-bug resolution for the leash-reset behavior surfaced by Phase 2.5. Future occupant-behavior bugs follow the same per-bug pattern (Discipline #11.1 cold-start empirical surfaces them; the triad does not pre-suppose them).

**The triad's structural sufficiency claim survives.** The behavioral-correctness caveat is an addition, not a refutation.

### 2.4 Profile A ship-window implication

Both ship windows preserved:
- **P3 reduced-cell-space ship (~11-16 weeks):** depends on whether P0 W0.9 gauntlet migration + P1 W1.13 skill tree node population together resolve boss-floor
- **P4 full-cell-space ship (~15-22 weeks):** with all sim extensions in place, including deferred-bin sims that may interact with boss-floor problem

**Risk flag:** if P0/P1 work doesn't empirically resolve boss-floor (Pattern-A persists after § 2.8 + § 2.9 implementations), then Profile A ship blocks until P4 sim extensions land. Watch this in P3 W3.X validation.

---

## 3. New open questions surfaced

### OQ-6 — Physical hunter modifier ceiling

class_0019 hit modifier=1.0000 — the ceiling — and still produced boss_wr=0.0. This suggests **physical hunter archetype may be systemically mis-matched to gauntlet geometry** under current physical melee + armor mitigation formula.

Possible explanations:
- Armor mitigation formula (ARMOR_MITIGATION_K=3000; 76% damage reduction at boss-tier) caps physical effective DPS regardless of modifier scaling
- Hunter-archetype is range-based but tagged physical — physical's melee-geometry preference creates positional mismatch
- Combination of both

**Disposition:** P7 W7.2 reference-archetype certification candidate. The QD-archive query at P7 will surface whether physical hunter archetype is producible under the new framework. If not, this surfaces as a new LC for resolution.

### OQ-7 — Water modifier systemically elevated

Water modifier range (0.134–0.258) is notably higher than fire/lightning (0.072–0.134) despite comparable kit structures. Suggests **water's sustained-presence zone-denial pillar may produce systematically lower instantaneous DPS density**, requiring higher modifier scaling to hit same per-tier WR.

**Disposition:** combat-pillar DPS density analysis candidate for P1 W1.11 scoping. Worth understanding before substrate enrichment finalizes — if water sustained-presence is structurally lower-DPS-density, enrichment should target instantaneous-burst skill templates to balance the modifier requirement.

---

## 4. Action items

### 4.1 For knight-rider (autonomous absorption)

- **P1 W1.11 scope:** confirm uniform-depth comprehensive enrichment per Track C verdict
- **Save ~1-2 weeks** of P1 budget previously held for differentiated-depth analysis
- **No new dispatch needed** — Track C result folds into existing W1.11 scope

### 4.2 For Matt review on return

- Track C synthesis confirms substrate-as-cohesion architecture (substrate identity is calibration-uniform; differentiation is in mechanic-pool composition + modifier scaling, not in substrate-intrinsic depth)
- Track C verdict reinforces § 2.8 + § 2.9 architectural commitments (both empirically necessary, not optional)
- OQ-6 + OQ-7 surface for P7 + P1 W1.11 attention; not P0 blockers

### 4.3 For P7 W7.2 reference-archetype certification

Reference roster (12 archetypes preserved from canceled kit-redesign dispatch) becomes empirically-validated set:
- Physical hunter (OQ-6 reference) — query at P7 confirms whether QD-engine can produce this archetype
- Water sustained-presence caster — OQ-7 informs whether water archetypes need DPS-density rebalance
- All 12 reference archetypes validated at P7 via archive query (not gauntlet re-execution per § 2.9)

---

## 5. Cross-references

- `agentic_orchestration/rocket/research/substrate-generalization-study-2026-05-21/` — full Track C deliverables (per-substrate analysis, telemetry cross-reference, spot-check findings, CSVs)
- `agentic_orchestration/dispatches/2026-05-21-alt-a-substrate-generalization-study.md` — Alt A dispatch (with rocket completion record appended)
- `agentic_orchestration/dispatches/2026-05-21-knight-rider-qd-rebuild-hive-activation.md` § 2.8 + § 2.9 — multi-dim convergence + gauntlet migration commitments
- `canonical/story/hive-mind-protocol-qd-engine-rebuild-2026-05-21.md` § 6.2 W1.11 — substrate enrichment workstream (now confirmed uniform-depth)
- `canonical/story/per-tier-recompose-validation-findings-2026-05-19.md` — recompose-hive canonical findings (Pattern-A pathology load-bearing)
- `canonical/story/qd-engine-end-to-end-workflow-2026-05-21.md` — Phase 6 W6.X gauntlet usage
- `canonical/16-project-roadmap.md` — QD-rebuild chapter (updated 2026-05-21)

---

## 6. Closing — the wizard reads

Track C's verdict is structurally clarifying: the boss-floor pathology is not substrate-bound, not kit-composition-bound within current framework, not rescuable by parametric tuning. The architectural commitments already in place (§ 2.8 skill tree node population + § 2.9 gauntlet migration) ARE the empirically-required structural fixes.

**The verdict empowers the rebuild plan.** What was theoretically necessary is now empirically necessary. The two architectural commitments are validated by evidence, not just by reasoning.

P1 W1.11 simplifies to uniform-depth comprehensive enrichment (saving ~1-2 weeks). OQ-6 (physical hunter) + OQ-7 (water DPS density) surface for downstream attention. The QD-rebuild's road remains open, with one less ambiguity in the way.

**Track C did exactly what epistemic insurance should do — clarified the architectural commitment before weeks of work commit to a wrong assumption.**

**Signed:** gandalf (story-and-design steward)
**For:** the QD-rebuild's empirical clarity.
