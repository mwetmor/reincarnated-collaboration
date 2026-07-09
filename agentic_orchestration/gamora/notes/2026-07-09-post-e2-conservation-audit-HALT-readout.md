# Post-E2 band re-fit CONSERVATION-LAW AUDIT — HALT readout

**From:** gamora (simulation seam) → **routing:** Matt **via gandalf** (dispatch §7 crit. 6).
**Date:** 2026-07-09 (run completed 2026-07-09 02:27:25 UTC; elapsed 2635.4 s / 43.9 min wall).
**Dispatch:** `agentic_orchestration/dispatches/2026-07-09-gamora-post-E2-band-refit-conservation-audit.md`
  — §1 HALT rule (Matt, verbatim, BINDING): *"If the post-E2 re-fit LURCHES, the conservation law
  leaked — the re-fit HALTS, findings park for Matt, no curve-fit."*
**Math note (Disc #1, landed FIRST):**
  `reincarnated-engine/src/reincarnated/simulation/math/post-e2-band-refit-conservation-audit-2026-07-09.md`.
**Driver + report:** `simulation/post_e2_band_refit_audit_driver.py`;
  `output/post_e2_band_refit_audit/post_e2_band_refit_audit_report.json`;
  log `simulation/output/post_e2_band_refit_audit/full_run.log`.
**Precondition state:** E2 emitter `d99635a` (`economy_k` k-layer) + Gate-2 PASS; C3 arm-G baseline
  (readout `0e2ccff`) + STANDING bands. Four-cohort arm-G path, `cohort_count=4`, `smoke=false`,
  10 fights/tier, 54 kits / 66 configs — instrument IDENTICAL to C3.

---

## 0. VERDICT — HALT (5 of 7 bands LURCHED)

`verdict.reading` (report JSON): **"HALT — a band LURCHED (conservation law leaked; park for Matt,
NO re-fit)."** `lurched_shells = [open_arena, chokepoint_corridor, magic_pack, elite_pack, dense_cell]`.

Per §1 HALT rule + rider-4 / anti-Goodhart: **the seven bands STAND at their C3 values.** No endpoint
moved. No curve-fit. No re-fit tag. The finding parks for Matt.

---

## 1. THE PER-BAND AUDIT TABLE (verified column-by-column against the report JSON)

| shell | class | Δmean | ε | Δin-band-frac | spread_ratio | verdict | lurch trigger |
|---|---|---|---|---|---|---|---|
| open_arena | density-anchor | −0.668 | 8.30 | −0.0303 | **1.2826** | **LURCH** | spread_ratio outside (0.85,1.15) |
| chokepoint_corridor | density-anchor | −1.376 | 10.578 | **+0.1629** | **1.3979** | **LURCH** | Δin-band-frac >0.1 (mass crossed endpoint); spread_ratio |
| magic_pack | density-anchor | −2.123 | 7.944 | **−0.1047** | **1.3989** | **LURCH** | Δin-band-frac >0.1; spread_ratio |
| elite_pack | cap-censored (Lane 3) | (Δp25 **+12.828** vs ε_p25 4.355) | — | — | — | **LURCH** | Δp25 > ε_p25 — **cap-entangled, least clean** |
| dense_cell | density-anchor | **+35.766** | 14.826 | −0.0249 | **1.2620** | **LURCH** | Δmean > ε (UP); spread_ratio — **largest lurch** |
| boss_with_adds | F3 sanity-rail | −0.829 | 2.647 | — | — | STAND | — |
| mini_boss | F3 sanity-rail | −0.095 | 8.948 | — | — | STAND | — |

Numbers verified against `audit.<shell>` in `post_e2_band_refit_audit_report.json`. The paste in the
harvest brief reconciles exactly with the JSON.

**Note — no lurch is a Δmean-DOWN lurch except via companion checks.** The FOUR clear shells that lurch
on `spread_ratio` (open_arena, chokepoint, magic_pack, dense_cell) all have Δmean well within ε
(|Δmean| ≤ 2.2 on the first three; dense_cell alone lurches on Δmean itself). The lurch is a
DISTRIBUTION RESHAPE, not a mean translation. That is the crux (§3).

---

## 2. PER-BAND DIAGNOSIS — candidate leaked-law / second-order channel

The report attaches the full §4 channel list to every lurched shell (it does not pre-select). Below I
ASSIGN the most likely channel(s) per shell, grounded in the report's distributional evidence
(min/mean/max shift + per-cohort deltas). The report carries no spiky-vs-flat per-shell split, so the
attribution rests on the shell's density character + the shape of the shift.

Decisive shape evidence (report `c3_baseline` → `e2_arm_g`, MIN / MEAN / MAX):

| shell | MIN | MEAN | MAX | reading |
|---|---|---|---|---|
| open_arena | 20.77 → 14.44 | 55.34 → 54.67 | 186.0 → 226.4 | fan-out about conserved mean (both tails extend) |
| chokepoint_corridor | 19.68 → 14.34 | 70.52 → 69.15 | 119.0 → 153.2 | fan-out about conserved mean |
| magic_pack | 24.46 → **2.60** | 52.96 → 50.83 | 149.7 → 177.8 | fan-out; low tail collapses hard (overkill starvation) |
| dense_cell | 22.88 → 14.22 | 98.84 → **134.61** | 320.0 → 389.2 | **asymmetric fan-out UP** (high tail rewarded > low tail penalized) |

- **open_arena — overkill waste (§4 ch.1) + burst-vs-truncation (ch.2).** Mean CONSERVED (−0.668,
  ~1% of mean). The lurch is purely `spread_ratio` 1.2826: the k-scaled per-hit makes spiky kits
  spike higher (max 186→226) and dawdle lower (min 20.8→14.4) than the flat cadence, about an
  unchanged mean. Classic granularity-dependent reshape — throughput conserved, per-kill granularity
  not. Open-density room → moderate overkill exposure.
- **chokepoint_corridor — B11 geometry×economy interaction (§4 ch.5) + overkill (ch.1).** Mean
  CONSERVED (−1.376). Two triggers: (i) `spread_ratio` 1.3979 and (ii) Δin-band-frac **+0.1629** —
  mass moved INTO the band (19.4%→35.7%) as the low tail fell toward the 12.52 floor and the funnel's
  AOE-concentration term (my §4 ch.5) interacts non-linearly with the k-scaled per-hit. The funnel is
  the room designed to exploit AoE overlap; a bigger per-hit over/under-shoots the concentration bonus
  per-kill even though period-averaged throughput holds.
- **magic_pack — overkill waste on spiky big-hits (§4 ch.1), strongest signal.** Mean CONSERVED
  (−2.123). The low tail COLLAPSES (min 24.46 → **2.60**) and mass leaves the band
  (Δin-band-frac −0.1047, 86.9%→76.4%). High-mob-count / low-per-mob-HP is exactly the shell my §4
  named as most overkill-exposed: k=1.6 big-hits overkill low-HP mobs, wasting damage above remaining
  HP → the spiky tail clears slower → a long low-KPM tail appears that was not there stripped. This is
  the cleanest overkill signature in the run.
- **dense_cell — B11 AoE-overlap (§4 ch.5) dominating, asymmetric UP — THE crux band.** Mean
  **+35.77 UP** (>ε 14.83) AND `spread_ratio` 1.2620. This is the ONLY mean-lurch and the ONLY UP
  move. My §4 warned: "no listed channel produces a throughput INCREASE." Resolution: this is not a
  throughput increase — it is an encounter-KPM increase from AoE-OVERLAP in the packed cell. dense_cell
  is the tightest-packed geometry; a k-scaled per-hit landing on overlapping mobs kills MORE mobs per
  cast than the throughput model (single-target) predicts. Per-cohort deltas confirm it is
  gear-portfolio-driven: DPS +16.80, Balanced +17.25, Hybrid +17.61, Defensive +0.00 — the offensive
  cohorts carry the overlap gain; Defensive (no offensive throughput tilt) shows zero, exactly as a
  geometry×offense interaction (not a global bug) would.
- **elite_pack — LEAST CLEAN; cap-entangled (see §4 below).** Lurch via Δp25 +12.828 (>ε_p25 4.355).
  The p25 rose 29.03→41.86 in the un-censored lower tail. Candidate channel is overkill/AoE in the
  3-mob room, but the signal is entangled with the KPM=450 cap-censoring (mean/p90 pinned at cap). See
  §4 — its lurch is the least trustworthy of the five.

---

## 3. THE LOAD-BEARING INTERPRETIVE QUESTION — (a) BUG vs (b) SUBSTRATE TRUTH

**The pattern:** means barely moved (open_arena/chokepoint/magic_pack/boss/mini_boss all within a
point or two of conservation), while distributions RESHAPED (spread 1.26–1.40) and dense_cell's mean
jumped +35.77 UP. Is the conservation law implemented WRONG (a), or does single-target throughput
conservation genuinely NOT imply encounter-KPM conservation (b)?

**DIAGNOSIS: (b) SUBSTRATE TRUTH.** The evidence supports (b) and FALSIFIES (a).

**Single strongest piece of evidence:** the shift is a mean-preserving FAN-OUT (min DROPS, max RISES,
spread widens 1.26–1.40x) on SIX shells with conserved means — NOT a uniform proportional translation.
A k-cancellation BUG (k applied to throughput but not period, or vice-versa) would translate the ENTIRE
distribution by the same factor on EVERY shell: min, mean, and max would all scale by k, and
spread_ratio would equal that factor identically across shells. What the report shows instead is
means CONSERVED to ~1–4% on five of seven shells while the spread fans out — the per-skill
throughput invariance HELD (that is what conserves the means), but the throughput→encounter-KPM
MAPPING is not invariant because per-fight granularity (overkill censoring on the low tail,
AoE-overlap on the high tail) depends on per-hit SIZE, which `k` changes even as it preserves
per-hit RATE.

Corroborating (b), falsifying (a):
- **Six conserved means falsify a global k-mis-application.** If the emitter mis-applied `k` globally,
  ALL shells would move UP proportionally. Five clear/rail shells' means barely moved. A global bug
  cannot conserve five means and blow out one.
- **dense_cell's UP move is geometry-specific, not global.** It is the tightest-packed cell; its gain
  is carried by the OFFENSIVE cohorts only (Defensive +0.00). A bug is cohort-blind and shell-blind;
  this move is cohort-selective AND shell-selective — the fingerprint of an AoE-overlap × offense
  interaction, i.e. substrate truth.
- **The reshape channels are exactly the ones my §4 pre-named** (overkill, AoE-overlap, truncation) —
  the granularity-dependent second-order play the scalar was KNOWN not to preserve. The audit did not
  discover a new bug; it measured that these named channels are LARGER than the ε I set — big enough to
  reshape the distribution, though not to translate the mean.
- **The per-skill invariance is proven upstream.** rocket's E2 round-trip smoke (Gate-2 PASS `d99635a`)
  proved throughput = per_hit/period and cost_rate = cost/period cancel `k` exactly at the emitter.
  That per-skill proof + the conserved encounter MEANS here means the law holds where it is DEFINED
  (per-skill throughput); it simply does not extend to encounter-KPM, which is what the audit revealed.

**What (b) means precisely:** the conservation law is a PER-SKILL SINGLE-TARGET throughput claim. It
is TRUE at that scope. The seven bands are ENCOUNTER-KPM bands. Encounter KPM = throughput ×
(mobs-killed-per-hit efficiency), and that efficiency factor is NOT `k`-invariant — it moves with
per-hit SIZE through overkill censoring (low tail) and AoE-overlap (high tail). The audit did not
falsify E2's law; it revealed that the law's scope (per-skill throughput) is NARROWER than the bands'
scope (encounter KPM). The elegant `k`-cancels core is intact where it was proven; it just does not
buy band-invariance.

I do NOT decide the remedy. That is Matt's. My rule is on (a) vs (b) only: the evidence supports (b).

---

## 4. elite_pack CAVEAT — the least-clean lurch (Lane 3 cap-entanglement)

Per math note §2 caveat + dispatch HARD constraint: elite_pack's LURCH is judged on Δp25 (+12.828 >
ε_p25 4.355) BECAUSE its mean/p90 SATURATE the KPM=450 instrument cap (`c3_baseline.mean` 295.4,
`e2_arm_g.mean` 296.9, both p90 = 450.0 — cap-pinned). The Δp25 signal in the un-censored lower tail
IS a real lurch, but it is **entangled with the cap**: the cap censors the upper tail, so any real E2
upward reshape is partly invisible (already at cap) and the p25 rise is read against a distribution
whose top is clipped. **elite_pack's lurch is the LEAST clean of the five** — its Δp25 lurch should be
weighted lightest in any disposition, and it is confounded with the C3-flagged KPM=450 cap artifact
routed separately as Lane 3 (out of scope here; do NOT fold the cap raise/guard into this finding).

---

## 5. MATT'S DECISION SPACE (named, NOT chosen — rider-4)

The diagnosis is (b) substrate truth: single-target throughput conservation does not imply
encounter-KPM conservation. Given that, the option space (I rule on NONE):

1. **Re-anchor the lurched bands at the E2 arm-G baseline** (math-note-first density-model review) — if
   the E2 population is the durable cert population, re-derive the density anchors' endpoints at the E2
   arm-G clear-time distribution. This is a work-unit, not a curve-fit, and would require its own
   dispatch. NOT done here.
2. **Treat the geared spread as difficulty-ladder signal (the C3 disposition-1 analogue).** C3 §4
   (Matt-ratified disposition 1) already reads geared-over-ceiling mass as FLAG_PASS_OVERPOWERED →
   difficulty-ladder input, NOT a band error. The reshape here could be absorbed the same way: the
   spread is intended texture, the bands STAND, the over/under-band mass flags for review. (CAUTION —
   the harvest brief flags this: do NOT conflate the STANDING C3 geared-over-ceiling mass with the E2
   lurch. The C3 disposition was about the C3 baseline sitting over a stripped ceiling; THIS finding is
   about E2 MOVING the distribution relative to that C3 baseline. They are different questions. Reusing
   disposition 1 is an OPTION, but it must be an explicit new ruling, not an automatic carry-over.)
3. **Accept the spread as intended texture and WIDEN the lurch tolerance** — if the fan-out is judged
   acceptable game texture (per-hit-size granularity is a real design surface), the ε / spread_ratio
   band could be re-set to admit it. This is a threshold change, math-note-first, and risks
   anti-Goodhart if done to green cells — Matt must judge it as a genuine scope correction, not a
   curve-fit.
4. **Kick back to rocket (ONLY if (a)).** The evidence is (b), so this is NOT indicated. Listed for
   completeness: if Matt reads the evidence as (a) despite the six conserved means, the remedy is a
   rocket emitter re-inspection of the k-application. My diagnosis is that the six conserved means
   falsify (a); I do not recommend this branch.

**My rule stops at (a) vs (b). The remedy is Matt's.**

---

## 6. WHAT THIS HARVEST DOES / DOES NOT DO

- **DOES:** apply the HALT branch; author this readout; verify all numbers against the report JSON;
  diagnose per lurched band; make the (a)-vs-(b) call (→ b, substrate truth); frame Matt's option space;
  park the finding at `matt_decision_needed/`.
- **DOES NOT:** re-run the driver (compute finished cleanly, 2635.4 s — harvest only); move any band
  (rider-4 — all seven STAND at C3 values); curve-fit any endpoint; tag a re-fit (HALT branch, no
  `post-e2-audit` tag); choose a remedy (Matt's); touch the emitter (E2 landed); fold in the
  elite_pack KPM-450 cap (Lane 3, separate); change any telemetry/star-lord schema (all in-JSON
  gamora-side; no MIGRATION).

---

**Signed:** gamora, 2026-07-09. HALT harvested. Conservation law leaked at the encounter-KPM scope
(diagnosis (b): per-skill throughput invariance is TRUE but does not extend to encounter KPM). Five of
seven bands lurched on distribution reshape (spread 1.26–1.40) with means conserved on six shells and
dense_cell alone moving UP (+35.77, AoE-overlap × offense). Bands STAND. No re-fit. Routed to Matt via
gandalf; parked at `matt_decision_needed/`.
