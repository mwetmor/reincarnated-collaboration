# Dispatch — gamora: post-E2 band re-fit = the CONSERVATION-LAW AUDIT

**From:** knight-rider → **To:** gamora (simulation seam — band tables + certification driver)
**Date:** 2026-07-09
**Pattern:** B (multi-hour compute; math-before-code). **No fresh Gate-1** — this re-runs the C3 methodology (already Gate-1 `7956484`-lineage + Gate-2 PASS) on the E2-modified population; Gate-2 applies to the output.
**Authority:** Matt autonomous-continuation-run Lane 2 (2026-07-09): "E2's landing then triggers the NEXT band re-fit cycle … expected band impact small by construction, which doubles as the conservation-law audit." E2 landed + pushed (rocket `d99635a`, tag `rocket/v2.0-economy-axis-2`, Gate-2 PASS `2026-07-09-gate2-rocket-e2-economy-axis.md`). E2 design note §1.2 (conservation law) + §4 (sequencing) BIND the interpretation.
**Status:** FIRE-READY.

---

## 0. Why this run exists — and why it is an AUDIT, not a re-fit

E2 gave `bc_amplitude` mechanical meaning via a single per-skill scalar `k` on (per_hit≡`damage_multiplier`, cooldown, energy_cost). The elegant core (design note §1.2, math note `economy-axis-e2-2026-07-09.md`): **throughput = per_hit/period and cost_rate = cost/period are invariant under joint `k` by construction** — `k` cancels. KPM is throughput-driven. **Therefore the seven KPM bands should NOT move.** This run regenerates the population on the E2 emitter, runs the two-arm four-cohort-arm-G certification, and cross-checks the arm-G KPM distributions against the seven STANDING bands (C3 readout `0e2ccff`).

**This is the conservation-law audit.** By construction the bands hold; any real deltas come ONLY from second-order play the scalar does not preserve: overkill waste on spiky big-hits, burst against fight-truncation, energy pooling/lockout pressure, ailment-application cadence, B11 geometry interaction. That texture is expected small. **A LURCH is the alarm.**

## 1. HALT RULE (Matt, verbatim, BINDING)

> **If the post-E2 re-fit LURCHES, the conservation law leaked — the re-fit HALTS, findings park for Matt, no curve-fit.**

Operationalize "lurch": you MUST state a numeric lurch threshold in the math note BEFORE the run (e.g. per-band floor/ceiling drift beyond a stated ε, or a cohort-delta magnitude beyond the C3 baseline envelope). If any band crosses it: **STOP** — do NOT re-fit the band, do NOT curve-fit endpoints (rider-4 / anti-Goodhart). Author a HALT readout naming which band lurched, by how much, and the candidate leaked-law mechanism (overkill / truncation / pooling / cadence). Park at `matt_decision_needed/`. Do NOT tag a re-fit.

If NO band lurches: the audit PASSES — bands STAND (re-validated at the E2 population), you author a clean audit readout, tag, and route to Matt via gandalf.

## 2. MATH-BEFORE-CODE (Discipline #1) — REQUIRED, precedes any run

Author `simulation/math/post-e2-band-refit-conservation-audit-<date>.md` FIRST. It MUST state:
- **The lurch threshold** (§1) — the numeric criterion that separates "expected second-order texture" from "leaked-law lurch." Justify it against the C3 four-cohort delta envelope (max delta 52.68; compression 0.986–1.021).
- **The conservation prediction** — per-band, what "holds" looks like numerically (throughput-invariance ⇒ KPM distribution should overlay the C3 arm-G distribution within the threshold). This is the null hypothesis the audit tests.
- **The second-order channels** you expect to produce sub-threshold texture (name them; they are the diagnostic vocabulary if something moves).
- **Declared baseline** = arm G (geared), same as C3. Stripped arm is the scaling-delta diagnostic (E5-C), NOT the cert measure. No stripped figure quoted as the geared baseline (reframe-validity).

## 3. Run config (inherits C3 riders — BIND)

- **Four-cohort arm-G path** (C3 INFO-2): the driver DEFAULTS to a single `Balanced` cohort — that is the trap. Exercise the four-cohort arm-G path; the readout MUST enumerate four distinct per-cohort deltas. A single-cohort run is a HARD FAIL of this dispatch.
- **Same per-cell seed both arms** (Disc #3 — no parallel regens of same seed; the driver enforces; confirm in the banner).
- **Population regenerated on the E2 emitter** (`d99635a`) — confirm the emitter carries `economy_k` provenance on emitted skills (the E2 round-trip smoke proved this) so you can, if a band moves, attribute by `k` value.

## 4. #2-FF fields (MANDATORY)

- **Verdict-rendering instrument named:** the per-band audit table (STAND vs LURCH against the §2 threshold) + the four-cohort arm-G delta map + the second-order attribution if any band moves.
- **One-command pre-fire verification that exercises the PATH:** a single command proving (a) the regenerated population carries the E2 `k`-layer (e.g. a variable kit shows `economy_k` 1.6 on chain_A / 0.7 on chain_B/C — NOT all 1.0, which would mean E2 didn't take), and (b) the four-cohort arm-G path runs with `cohort-count == 4` in its first-log line. A bare non-zero-delta check does NOT defeat either trap. State the expected first-log line.
- **Precondition state cited:** E2 `d99635a` + Gate-2 PASS; C3 readout `0e2ccff` (the STANDING bands); design note §1.2.

## 5. The STANDING band set (the audit reference — from C3 `0e2ccff`)

| Family room | (floor, ceiling) |
|---|---|
| open_arena | (20.87, 53.33) |
| chokepoint_corridor | (12.52, 60.00) |
| magic_pack | (12.52, 102.86) |
| elite_pack | (8.26, 28.13) |
| dense_cell | (12.52, 102.86) |
| boss_with_adds | (2.49, 3.78) |
| mini_boss | (0.57, 3.30) |

**Note (from C3 §4, Matt-ratified disposition 1):** chokepoint_corridor / dense_cell / elite_pack already run geared distributions above their stripped-derived ceilings — that is `FLAG_PASS_OVERPOWERED` → difficulty-ladder input, NOT a band error. The E2 audit must not conflate that STANDING geared-over-ceiling mass with an E2-induced lurch. The audit question is narrow: **did E2 MOVE the distribution relative to the C3 arm-G baseline** — not whether the C3 baseline itself sits over a stripped ceiling.
**elite_pack KPM=450 cap:** still saturates (instrument artifact, C3-flagged, routed as its own item — Lane 3). Do NOT read cap-saturation as an E2 signal.

## 6. Cross-seam discipline (ADR-004)

No sim contract CHANGE expected — you re-run values you own (band tables) on a population from the already-landed+pushed E2 emitter (no rocket interface change; E2 added no new emitted field the sim must consume — Gate-2 confirmed). If the audit surfaces a driver→star-lord telemetry reporting need, that is cross-seam → MIGRATION.md + Matt before tagging.

## 7. Acceptance criteria

1. Math note lands FIRST (Disc #1), stating the lurch threshold + conservation prediction + second-order channels (§2).
2. Population regenerated on the E2 emitter; two-arm certification with the **four-cohort arm-G path** (four distinct per-cohort deltas enumerated).
3. Per-band audit table: STAND vs LURCH against the stated threshold.
4. **Branch on result:** (PASS) bands STAND, clean audit readout, tag `gamora/v<X.Y>-post-e2-audit-1`, route to Matt via gandalf. (HALT) name the lurched band + magnitude + candidate leaked-law mechanism, park at `matt_decision_needed/`, do NOT re-fit, do NOT tag a re-fit.
5. #2-FF fields present in the run banner.
6. Readout authored and routed to Matt via gandalf either way.

## 8. Explicitly OUT OF SCOPE

- **elite_pack KPM-450 cap raise/guard** — that is Lane 3, its own math-note-first item; do NOT fold it in here.
- **Curve-fitting any band** to green a cell — REJECTED (rider-4 / anti-Goodhart); endpoints move only on diagnosed mis-specification, and a leaked-law lurch is a HALT+park, not a re-fit.
- **E3/E4 axes** — queued; not this run.
- **Emitter changes** — E2 landed; do not touch `per_skill_emitter.py`.
- **The §4 geared-over-ceiling disposition** — Matt-ratified (disposition 1); not re-opened here.

## 9. Instrument guard (STANDING)

Affixed mobs and content encounters never enter the certification gauntlet rooms. The gauntlet certifies kits against the clean four-family instrument.

---

**Required reading (gamora, at session start):**
1. This dispatch.
2. `agentic_orchestration/gandalf/notes/2026-07-09-e2-economy-axis-design-note.md` §1.2 (conservation law — the null hypothesis) + §4.
3. `agentic_orchestration/gamora/notes/2026-07-08-c3-band-refit-e1-readout.md` — the STANDING bands + four-cohort delta envelope + the §4 disposition-1 geared-over-ceiling framing (do not conflate with an E2 lurch).
4. `src/reincarnated/generation/math/economy-axis-e2-2026-07-09.md` — the k-layer math (why throughput/cost-rate are invariant; the cast_time E4-boundary residual).
5. Your own `leg_i_cell_grain_two_arm_driver.py` + the four-cohort arm-G path (C3 completion record).

**Sign-off:** knight-rider, 2026-07-09. Fires directly (methodology already gated via C3). Gate-2 on the output.
