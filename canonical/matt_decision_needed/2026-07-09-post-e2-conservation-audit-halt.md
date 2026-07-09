# Matt decision needed — post-E2 conservation-law audit HALTED (5/7 bands lurched)

**STATUS:** OPEN — waiting on Matt (disposition ruling; the bands STAND pending your call).
**Surfaced:** 2026-07-09 by gamora (simulation seam), HALT branch of the post-E2 band-refit
conservation-law audit. Routed to Matt via gandalf.
**Authority for the HALT:** Matt HALT rule (verbatim, BINDING, dispatch §1): *"If the post-E2 re-fit
LURCHES, the conservation law leaked — the re-fit HALTS, findings park for Matt, no curve-fit."*

---

## The verdict

The post-E2 band-refit audit **HALTED**: **5 of 7 KPM bands LURCHED** against the pre-stated ε
(15% of each shell's C3 arm-G mean; elite_pack via Δp25). Lurched: open_arena, chokepoint_corridor,
magic_pack, elite_pack, dense_cell. STAND: boss_with_adds, mini_boss.

Per rider-4 / anti-Goodhart + your HALT rule: **no band was re-fit, no endpoint moved, no tag.** The
seven bands STAND at their C3 values pending your ruling.

## The crux — (a) BUG vs (b) SUBSTRATE TRUTH

The MEANS were conserved on 6 of 7 shells (throughput ~conserved on average), while the
DISTRIBUTIONS reshaped (spread widened 1.26–1.40x) and dense_cell's mean jumped **+35.77 UP**.

- **(a) k-layer BUG** — the conservation law is implemented wrong (k applied to throughput but not
  period, or vice-versa).
- **(b) SUBSTRATE TRUTH** — single-target per-skill throughput conservation does NOT imply
  encounter-KPM conservation, because per-fight granularity (overkill censoring on the low tail,
  AoE-overlap on the high tail in packed cells) depends on per-hit SIZE, which k changes even as it
  preserves per-hit RATE.

**gamora's diagnosis: (b) SUBSTRATE TRUTH.** Strongest evidence: the shift is a mean-preserving
FAN-OUT (min drops, max rises, spread widens) on six shells with conserved means — NOT a uniform
proportional translation. A global k-mis-application bug would translate the ENTIRE distribution by the
same factor on EVERY shell; it cannot conserve five means while blowing out one. dense_cell's UP move
is geometry-specific and carried by offensive cohorts only (Defensive +0.00) — an AoE-overlap × offense
interaction, not a cohort-blind bug. The per-skill invariance is proven upstream (rocket E2 round-trip
smoke, Gate-2 PASS `d99635a`); it simply does not extend to encounter KPM. **E2's elegant k-cancels
core is intact where it was proven; it does not buy encounter-band-invariance.**

## Your decision space (gamora rules on none — rider-4)

1. **Re-anchor the lurched bands at the E2 arm-G baseline** (new math-note-first density-model review
   dispatch).
2. **Treat the geared spread as difficulty-ladder signal** — the C3 §4 disposition-1 analogue. NOTE:
   this must be an EXPLICIT new ruling, not an automatic carry-over — the C3 disposition was about the
   C3 baseline sitting over a stripped ceiling; THIS is about E2 MOVING the distribution relative to the
   C3 baseline. Different question.
3. **Accept the spread as intended texture and widen the lurch tolerance** (threshold change,
   math-note-first; must be a genuine scope correction, not a curve-fit to green cells).
4. **Kick back to rocket** — indicated ONLY if you read the evidence as (a). gamora's diagnosis is (b);
   the six conserved means falsify (a). Not recommended.

## Caveats

- **elite_pack's lurch is the LEAST clean** — judged on Δp25 (+12.828 > ε_p25 4.355) because its
  mean/p90 saturate the KPM=450 instrument cap (C3-flagged, routed as Lane 3). Its Δp25 signal is
  entangled with the cap; weight it lightest. The KPM-450 cap raise/guard is OUT OF SCOPE here (Lane 3).

## Read the full diagnosis

- **HALT readout (full per-band diagnosis + evidence tables):**
  `agentic_orchestration/gamora/notes/2026-07-09-post-e2-conservation-audit-HALT-readout.md`
- **Math note (pre-stated ε + conservation prediction + channels):**
  `~/Games/reincarnated-engine/src/reincarnated/simulation/math/post-e2-band-refit-conservation-audit-2026-07-09.md`
- **Report JSON:**
  `~/Games/reincarnated-engine/src/reincarnated/output/post_e2_band_refit_audit/post_e2_band_refit_audit_report.json`
- **Related (do NOT conflate):** C3 readout `0e2ccff`
  (`agentic_orchestration/gamora/notes/2026-07-08-c3-band-refit-e1-readout.md`) + the pending
  declared-baseline succession entry (`2026-07-09-declared-baseline-succession-entry-approval.md`).

---

**Parked by:** gamora, 2026-07-09. HALT branch executed cleanly; no re-fit ships. Awaiting your
disposition ruling.
