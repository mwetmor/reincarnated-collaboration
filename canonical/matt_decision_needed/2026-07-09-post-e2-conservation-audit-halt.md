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

## APPENDED 2026-07-09 (gamora) — Lane 3 elite_pack KPM=450 cap remedy, PARKED to be ruled WITH this E2 finding (same censoring family)

**Why appended here (not a separate park):** the autonomous-run Lane 3 item (elite_pack saturates the
KPM=450 instrument cap) was scoped as its own math-note-first work, but the post-E2 conservation audit's
diagnosis reframed it: **the KPM=450 cap is itself a censoring mechanism, and encounter-KPM's sensitivity
to per-hit SIZE (overkill censoring + AoE-overlap) is the SAME family as how the cap censors clear-speed.**
The two are ONE ruling. Cap remedy analyzed; recommendation below; **no instrument change ships** — it
ships only WITH your E2 disposition on this page.

**Math note (full derivation):**
`~/Games/reincarnated-engine/src/reincarnated/simulation/math/elite-pack-kpm-cap-2026-07-09.md`.

**The cap is a DERIVED tick-floor artifact, not a magic number.** elite_pack is a 3-mob room; density
model KPM = 3×60/clear_s = 180/clear_s. The 450 pin ⟺ clear_s = 180/450 = 0.4 s (4 ticks @ TICK_SIZE=0.1 s)
= the greedy-caster (int/wis) fast-clear floor. p90 == max == 450.0 on 990 samples both C3 and E2 → the
upper tail is CLIPPED; mean 295.4 is a censored (low-biased) mean.

**Two remedies derived (arithmetic in the math note):**

1. **Cap raise → 1800 KPM.** `mob_count × 60 / TICK_SIZE = 3×60/0.1 = 1800` — the 1-tick tick-grid
   ceiling, the max the instrument can emit for a 3-mob room; fully un-censors. (A 0.3 s greedy clear
   already produces 600 > 450 — direct proof of censoring.) **SIDE-EFFECT / the coupling to THIS finding:**
   the cap is GLOBAL; raising it un-censors every shell's upper tail — including the offensive-cohort
   tails the E2 audit found FANNING OUT (spread 1.26–1.40×) and lurching dense_cell +35.77 UP via
   AoE-overlap. dense_cell's E2 max is 389.2, climbing toward 450. **A cap raise changes what the E2
   audit measures** (un-clips exactly the mass the audit is tracking). You cannot raise the cap without
   perturbing the E2 readout — hence the joint ruling.

2. **Clear-time-floor guard → T_floor = 1.0 s (10 ticks).** `ceil((TICK_SIZE/band_half_width)/TICK_SIZE)
   = ceil(0.9346/0.1) = 10 ticks`; identical derivation to the STANDING 2026-06-21 domain guard
   (`CLEAR_SHELL_DOMAIN_TMIN_S=1.0`). Clears faster than 1.0 s (KPM > 3×60/1.0 = 180) route to the
   COMPLETION gate (did the pack die?) instead of a KPM number. SIDE-EFFECT: discards genuine fast-clear
   signal (learns the pack died, not how over-powered the clear was) rather than uncensoring it.

**gamora recommendation (PARKED): adopt remedy (2), the clear-time-floor guard at 1.0 s, applied to the
CERT instrument's per-fight KPM pool.** Reasoning: (a) it extends a precedent YOU already ratified
(2026-06-21 domain guard, same artifact, same shell) — anti-Goodhart-clean, not a new curve-fit;
(b) unlike the cap raise, it resolves the cap-confound at the ROOT for BOTH instruments — sub-1.0 s
clears leave the pool, so elite_pack's audit mean/p90 stop being cap-censored and the E2 audit can judge
elite_pack on Δmean like every other shell (retiring the Δp25 workaround in §4 / Caveats above);
(c) it does NOT perturb the offensive-cohort upper tails the E2 audit measures, whereas the cap raise
does. **But it ships only WITH your E2 disposition:** if you re-anchor the lurched bands (option 1), the
floor guard changes which cells enter the re-anchor, so the guard must be decided before/jointly — else
the re-anchor fits a still-cap-confounded elite_pack.

**Cross-seam (parked):** if either remedy touches a driver→star-lord exported KPM field, MIGRATION.md is
required (hand to star-lord; do not modify telemetry schema). Likely MIGRATION-free for an AUDIT-pool
guard (audit metrics are in-JSON gamora-side per the readout), but re-verify at implementation. Parked;
not authored.

**No cap change, no band change, no guard install, no tag ships in Lane 3. Awaiting your joint ruling.**

---

**Parked by:** gamora, 2026-07-09. HALT branch executed cleanly; no re-fit ships. Lane 3 cap remedy
appended 2026-07-09 (same censoring family; recommendation = floor guard, parked to your joint ruling).
Awaiting your disposition ruling.
