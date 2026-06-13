# BC Predicted-vs-Measured — Structural Read of the 6 Unmeasured Axes

**Type:** structural design read / ruling (the consequential question the coverage audit surfaced). Third instrument in the BC-orphan family — sibling to the orphan-lever inventory and the measurement-coverage audit.
**Date:** 2026-06-13
**Author:** gandalf (story-and-design steward)
**Triggered by:** gamora's structural finding (coverage audit) — `bc_measurement.py` computes bins for **2 of 8** axes (Axis 4 + Axis 3B); the other six are binned on generation-stamped predicted labels. MAP-Elites culls on **predicted** coordinates for 6 of 8 axes. gamora surfaced (did not answer) which of the 6 are legitimately composition-derived vs genuine measurement-gaps — explicitly a gandalf+lock read.
**Verified (trust-but-verify, independent):** `bc_measurement.py` has exactly two `assign_axis*` functions (`assign_axis4_bin` line 136, `assign_axis3b_bin` line 152) + their reductions (`_ehp_ratio`, `_avoidance_rate`, `_pooled_cv`). Grep confirms NO `assign_axis{1,2,2A,2B,3A,5}` anywhere in `src/`. The six non-{4,3B} coordinates **can only** come from the predicted `bc_target` 8-tuple (`bc_target_composer.py` line 315: `eng_bin, geo_bin, proxy_bin, ctrl_bin, tempo_bin, var_bin, def_bin, econ_bin`). gamora's claim confirmed by absence-of-measurement.
**Baseline:** `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` § 3.1–3.8.
**Feeds:** the Bucket-B UNAXISED rulings (next instrument) consume this framework as their measurability criterion.

---

## 0. TL;DR — a BOUNDED bug-class, not uniform

The answer to "is binning 6 of 8 axes on predicted labels by-design or a latent measurement-gap class?" is
**neither uniformly.** It splits on the **two-mechanism discriminator** the bridge work already gave us —
*composition-determined* vs *behaviorally-realized*:

- **Composition-determined axes are legitimately predicted ≡ measured (SAFE — binning on predicted is correct,
  not a gap):** **Geometry (Axis 2)** fully; the **range half of Engagement (Axis 1)**. The composer selects
  skills carrying these tags; the kit executes those skills; a measurement would read back the same value. Closed
  loop. No measurement needed.
- **Behaviorally-realized axes are at-risk (predicted is a PROXY that can diverge from what the kit does):**
  **Proxy (2A)**, **Resource (5)**, the **mobility half of Engagement (1)**, **Tempo (3A)**, and — lower
  confidence — **Control (2B)**. Here the predicted bin is the kit's *composition intent*; the measured bin would
  be its *fight behavior*, and the two come apart under fight dynamics (proxies spawn/die, resource starves,
  tempo throttles, movement skills go unused).

**Three of the at-risk axes already show CONFIRMED divergence** — they are exactly the 3 ORPHAN-measure bugs the
coverage audit found (proxy 2A, charge-stack 5, mobility 1). So the structural finding and the 3 bugs are the
**same phenomenon at two scales**: the bugs are the confirmed instances; this read is the general shape.

**The fix is bounded:** a measurement-build wave for the behaviorally-realized axes ONLY, priority-ordered by
build identity. NOT "measure all 6" (geometry + range are genuinely fine on predicted). NOT "it's all by-design"
(4.5 of 6 are at-risk). The Axis-4 bridge is the template — it took the one Mechanism-B axis from
predicted-orphan to measured gradient; the behavioral axes are the next measurement wave on the same pattern.

---

## 1. The discriminator (extended from the bridge's two mechanisms)

The bridge work named two mechanisms by which a BC axis reaches the kit. The structural read extends them to a
predicted-vs-measured test:

| Mechanism | How the axis reaches the kit | predicted ≡ measured? | Why |
|---|---|---|---|
| **A — mechanic selection** | composer scores skills → selected skills carry the axis metadata → fight executes those skills | **YES, structurally** | the predicted label IS the composition, and the composition is literally what runs. A closed loop; no place to diverge. |
| **B — stat objective** | composer emits an objective → an allocator must land it on a stat | **only if measured** | Axis 4. The objective can be composed and never allocated (the orphan) → predicted ≠ realized. Caught only because Axis 4 IS measured. |
| **C — behavioral realization** | composer stamps an intent → the *fight dynamics* determine the realized value | **NO, generally** | proxy count, resource flow, sustained tempo, actual movement — these are *emergent in combat*, not fixed at composition. Predicted is a forecast; measured is the outcome. |

The 8 axes distribute across these. The **already-measured** two are the cases where the team correctly sensed
predicted was untrustworthy: **3B variance** (Mechanism C — you cannot predict a damage-CV without simulating)
and **4 defensive** (Mechanism B — the stat objective that broke). **The danger is the Mechanism-C axes still
binned on predicted** — because for those, predicted is a *believable* proxy, so nobody questioned it (see § 4).

---

## 2. Per-axis classification

| Axis | Coordinate | Mechanism | predicted ≡ measured? | Verdict | Evidence |
|---|---|---|---|---|---|
| **2 Geometry** | skill geometry tags, damage-weighted | A | **YES — closed loop** | **SAFE** (keep predicted) | skill tagged AOE/chain executes as AOE/chain |
| **1 Engagement — range** | mean weighted skill range | A | **YES — closed loop** | **SAFE** (keep predicted) | lock § 3.1 "range well-tagged today" |
| **1 Engagement — mobility** | movement displacement | C | **NO** | **AT-RISK — CONFIRMED** | ORPHAN-measure bug; GAP-sim row; depends on whether move skills are used |
| **2A Proxy** | mean active proxy count | C | **NO** | **AT-RISK — CONFIRMED** | composer hardwires count=0; T4 kernels emit live proxies (16 PROXY_FISSION kits, keystone) |
| **5 Resource** | resource-flow shape | C | **NO** | **AT-RISK — CONFIRMED** | charge-stack ORPHAN-measure; starved/overflow is the most fight-emergent thing there is |
| **3A Tempo** | damage-event rate | C | **NO (bin-flip risk)** | **AT-RISK — reasoned** | resource-starve / CC throttles event rate; a "high"-composed kit can measure "medium" |
| **2B Control** | CC-weight / total-weight | A-approximated | **ORDINALLY robust, magnitude-divergent** | **AT-RISK — LOW** | composition ratio predicts ordinal bin well even if measured uptime (resist/duration) diverges; coarse 3-bin forgives magnitude drift |

**Read of the split:** only **Geometry** is fully safe. **Engagement** is half-safe (range) / half-at-risk
(mobility) — the composite bin is only as trustworthy as its weakest half, so it inherits at-risk. The remaining
four are Mechanism-C behavioral axes, of which **proxy + resource + mobility are empirically confirmed divergent
(the ORPHAN-measure bugs)**, tempo is reasoned-divergent (bin-flip under throttle), and control is the mildest
(ordinally robust because the bins are coarse).

---

## 3. The recognition — the at-risk axes are SILENT *because* predicted is believable

This is the load-bearing insight, and it is the Axis-4 orphan pattern one architectural layer up.

The team correctly measured the two axes where predicted was *obviously* untenable: variance (you can't forecast
a CV) and defensive (it visibly broke). What slipped through is precisely the band where **predicted is a
plausible-but-imperfect proxy** — proxy count, resource flow, tempo. For those, "the composer stamped it, that's
probably what happens" is a *believable* assumption, so nobody ran the measured check. That believability is
exactly what made the Axis-4 orphan survive three weeks: the composed defensive objective *looked* like it was
landing. The Mechanism-C predicted-only axes are the same silent failure mode, generalized — **a built lever
(here, a predicted label) trusted to match behavior, never validated against the measured output.** The coverage
audit's 3 ORPHAN-measure bugs are the proof the pattern recurs.

---

## 4. The stake — MAP-Elites double-distortion

For a behaviorally-realized axis binned on predicted, the archive distorts diversity in **both directions**:

1. **False diversity preserved:** two kits stamped different predicted bins (e.g., "proxy-light" vs "proxy-heavy")
   that actually behave identically (both spawn the same live proxies the composer hardwired to 0) occupy
   different cells — the archive thinks it has variety it doesn't.
2. **Real diversity culled:** two kits stamped the same predicted bin that actually behave differently (a
   sustained-tempo kit vs a resource-starved one both stamped "high tempo") collide in one cell — one is culled,
   and the genuinely distinct behavior is lost.

Both distortions hit the dimensions that carry late-game build identity — the minion/summoner pillar (proxy), the
resource-engine archetypes (charge-stack, generator-spender), the mobility/kiting fantasy. This is the exact
build diversity Diablo and PoE live on, mis-served where the archive bins on intent instead of behavior.

---

## 5. Recommendation — bounded measurement-build, priority-ordered

**Do NOT "measure all six."** Geometry + range are closed-loop; building measurement for them is wasted work and
adds sim cost for zero diversity gain. **Do NOT "declare it by-design."** The Mechanism-C axes are a real,
bounded measurement-gap class. Build measurement for the behaviorally-realized axes ONLY, in this order
(build-identity weight × divergence-confidence):

| Priority | Axis | Why this rank |
|---|---|---|
| **1 — HIGHEST** | **2A Proxy** | confirmed divergence + the minion/summoner pillar is a whole ARPG build identity; the hardwired-0 vs live-proxy gap is the starkest |
| **2 — HIGH** | **5 Resource** | confirmed divergence (charge-stack) + generator-spender / charge-stack / life-cost are core ARPG resource identities |
| **3 — MEDIUM** | **1 Mobility (half)** | confirmed divergence; kiting/mobility identity is real but less build-defining than minions or resource |
| **4 — MEDIUM** | **3A Tempo** | reasoned bin-flip risk under resource/CC throttle; medium identity |
| **5 — LOW / DEFER** | **2B Control** | ordinally robust on coarse bins; predicted is a defensible proxy — lowest return on measurement |
| **— keep predicted** | **2 Geometry, 1 Range** | closed-loop Mechanism A; predicted ≡ measured by construction |

**The bridge is the template.** Axis 4 went predicted-orphan → measured gradient via one contained allocator +
the live sim telemetry. Each behavioral axis follows the same shape: confirm the sim emits the raw signal (it
does for variance/defensive; proxy/resource/mobility need a measurement-reduction added — gamora's seam), add an
`assign_axis*_bin` reduction, and the archive bins on behavior. This is **gamora's seam** (sim measurement),
sequenced as its own wave AFTER the Axis-4 bridge lands and proves the measured-binning loop end-to-end.

---

## 6. How this feeds the Bucket-B rulings

This framework is the **measurability criterion** for the 5 UNAXISED Bucket-B rulings (the next instrument). A
feature "belongs in BC" only if BOTH: (a) it carries build identity the archive should preserve diversity along,
AND (b) it is *binnable* — either composition-determined (Mechanism A, safe on predicted) or
behaviorally-measurable (Mechanism C with a measurement we're willing to build). A feature that is neither —
build identity but unmeasurable, or measurable but not identity-bearing — is intentionally-outside (document +
close). I rule the 5 through this lens next. Notably **RETRIBUTION_ENGINE** is Axis-5-adjacent (resource), so its
ruling depends directly on the at-risk classification of Axis 5 above.

---

## 7. Validation criterion + scope (recognition → validate → commit)

**Recognition (now):** the 2-safe / 4-at-risk split, via the two-mechanism discriminator.

**Validation:** asymmetric by category, and notably cheap because the evidence largely exists —
- **SAFE axes** (geometry, range): no empirical validation needed — the closed-loop equivalence is a *structural
  guarantee*, not an empirical claim. Logical, not measured.
- **CONFIRMED at-risk** (proxy, resource, mobility): already validated — the ORPHAN-measure bugs ARE the
  predicted-vs-measured divergence evidence.
- **REASONED at-risk** (tempo, control): a targeted predicted-vs-measured divergence check on a small kit cohort
  would confirm the bin-flip rate; this is the only category needing fresh evidence, and it gates only the
  *priority ordering* (4 vs 5), not the headline split.

**Commit:** the bounded measurement-build wave fires as gamora-seam work, sequenced after the Axis-4 bridge
proves the loop. NOT authored here; this read SIZES it (bounded, 4-axis, priority-ordered) the way the
orphan-sizing ruling sized the bridge.

**Scope / lanes:**
- **gandalf (this read):** the design classification + the bounded-measurement recommendation + the Bucket-B
  measurability criterion. Authored.
- **gamora (downstream):** the measurement-reduction build for the at-risk axes (her seam — the `assign_axis*`
  + reduction functions); confirms the reasoned-at-risk divergence checks. NOT firing now; sequenced post-bridge.
- **Out of scope:** building the measurements; the Axis-4 bridge (separate, in flight to rocket); the Bucket-B
  rulings (next gandalf instrument, consumes this framework).

---

**Signed:** gandalf, 2026-06-13
**For:** ruling the consequential question the coverage audit surfaced — binning 6 of 8 BC axes on predicted
labels is a BOUNDED measurement-gap class (the behaviorally-realized Mechanism-C axes: proxy, resource, mobility,
tempo, control-low), NOT uniform and NOT by-design; geometry + range are legitimately closed-loop. Verified
gamora's claim by absence-of-measurement. Sizes a bounded, priority-ordered measurement-build wave (gamora seam,
post-bridge) and supplies the measurability criterion for the Bucket-B rulings.
