# RUN KC2-PM4 — HALT BRIEF TO MATT

**Author:** gandalf (`RUN-CONDUCTOR`) · **Date:** 2026-08-14
**Fires per:** R-PM4-39 part 5 / R-PM4-53 part 4 / R-PM4-54 (the pre-registered exit ramp, executed BEFORE this HALT)
**Ledger:** `agentic_orchestration/gandalf/notes/2026-08-13-kc2-pm4-replication-run-charter.md` (L-1..L-45, R-PM4-1..R-PM4-54)

---

## 0 — The HALT in one paragraph

You asked the run to replicate your Grim Dawn Crucible fight (EoR Warlord, waves 150–160, death
at 160, last-4-lap 182.7167 s) faithfully, autonomously, with no tuning. Seven engine iterations
(I-15..I-21) and eight decode laps (N/O/P/Q/R/S/T/U) later, the run has its first **T2 hit on a
record cell** — I-21's pursuit fold lands l4l **161.0612 s, ratio 0.8815, inside the band** — with
**zero constants ever moved toward an outcome** (Law-3 tripwire clean across every iteration, with
witnesses). The residual that remains has been renamed seven times as each carrier was decoded and
folded — sustain → locomotion → geometry-size → structure → arrival-speed → distance → concurrency
— and its final carrier is **not a mechanic: it is a COUNT.** Wave 160 in the sim fields **5
bodies**; your referent held **19–36 living bodies (median 25) inside an 11.6 m circle.** With the
movement model now fully decode-true, 100 % of the board reaches you — *the movement model has
nothing left to give; what is missing is bodies.* And the wave rosters are the frozen substrate
E-s09-cp150's own rolls — amending them is a substrate amendment, which is yours to rule on, not
mine. The run HALTs here: at a named commitment boundary, with the residual measured on both
sides, not at exhaustion and not at a claimed convergence.

---

## 1 — T1–T4 scorecard (exit-ramp component c)

Best-ever per target across the whole run, verified from emitted artifacts (not agent prose):

| target | referent | best EVER on a record cell | iteration | status |
|---|---|---|---|---|
| **T1** death wave | 160, band {159–161} | **155** (I-21; prior best 156 at I-17/I-18) | I-21 | **MISS by 4 waves** — bounded by roster (§ 2) |
| **T2** last-4-lap | 182.7167 s, band [155.31, 210.12] | **161.0612 s, ratio 0.8815** | **I-21** | **MET** — first record-cell hit of the run |
| **T3** span MAE | per-wave pacing | 3.287 s (I-20, on **1** evaluable wave) vs 16.672 s (I-21, on 5) | — | **NOT COMPARABLE across iterations** (evaluable-wave counts differ); reported, not claimed |
| **T4a** mean HP frac | 0.932 ± 0.02 | **0.9309 — in band** (I-19 `COU·PX-LO·NEAR`); I-21 reads 0.8848 | I-19 | **MET at I-19, regressed under later decode-true folds** — honest note: the in-band cell predates the arrival/pursuit decodes |
| **T4b(b)** full-health dwell | 1.6166 s | 0.0 s (all iterations) | — | **NEVER MET** |
| **T4b(c)** w160 instant kill from full | fires only at wave 160 | never armed — **no ladder has reached wave 160** | — | **NEVER ARMED** (blocked behind T1) |

Graded distances (R-PM4-42 part 2) on the closing record cell `COU·PX-LO`: T1 Δ −5 · T2 ratio
0.8815 · T4a Δ −0.0472. Determinism three-leg ×2 arms EXACT; fold-off byte-identity 6/6 EXACT;
frozen 20/20; `export/` untouched; smoke 296 pass / 1 pre-existing.

**What the run proved beyond the scorecard:** the entire Crucible movement model is now decoded
from the game's own binary and records, not modelled — spawn→PLAYER march (`ShouldFindEnemy`
override, `ViewDistance` 80.0 m on 169/169 rolled monsters, string-dispatched `Pursue`), patrol
semantics (2.0 m tolerance, shouldRun), spawn geometry (120 tier-16 points, span 0.3253–26.08 m),
and your own motion (you MILL — net median 3.61 m/wave over 40–83 m paths, straightness 0.060).
Three folds in a row were adopted on decode authority alone; two graded WORSE and were kept, and
both are load-bearing for the one that grades better (U-S-2's cyclic traversal, exactly inert at
I-20, is worth +29.6 s under pursue-all). That is R-PM4-27 part 3 working as written.

---

## 2 — The commitment boundary: what is yours to rule (the residual)

**The residual is ROSTER SIZE.** Sim wave rosters across 151–160: 28, 18, 24, 13, 18, 19, 21, 33,
9, **5** (median 18.5; five of ten below the referent's floor). Referent: 19–36 living (median
25, a LOWER bound) inside 11.6 m. The rosters are **E-s09-cp150's rolls — the frozen substrate.**

Decodable next addresses exist and are priced (gamora, I-21 landing § 11.2):

1. **`bonusSpawnStatus` (C-12 / UNREACHED-S7)** — sim runs `P06_BONUS_SPAWNS = False` on an open
   UNREACHED; priced at **+25 bodies** over the band. A records/binary decode of exactly the shape
   Lap U executed.
2. **The count model itself (C-13)** — `EMPTY_ROSTER_DISPOSITION` declared over two never-fitted
   alternatives; priced at **+11**.
3. **`AlertBeforePursue` (UNREACHED-U3)** + **LOS/walls (UNREACHED-U2/U4, D-PDEF-2)** — unmeasured
   ramp terms; one decode closes the LOS+walls pair AND bounds D-I21-1's drift.

**But the honest arithmetic travels with the offer:** even if (1) and (2) both land in full, wave
160 reaches ~**8** bodies against a floor of **19**. The roster limb is worth a lap, it is
decodable, **and it will not close T1 by itself.** Full T1 closure requires the frozen substrate's
waves to field referent-scale rosters — a substrate amendment, outside the run's own laws.

**Your options (conductor's lean stated, ruling yours):**

- **(A) Close the run here.** T2 replicated on a record cell; movement fully decoded; residual
  named, priced, addressed. The run's laws held to the end. *Conductor's lean: this is a legitimate
  close — the run converged on everything the frozen substrate could express.*
- **(B) Authorize the roster lap (decode-only).** Legolas decodes C-12/C-13/U3/LOS from records +
  binary; no fold, no substrate touch; the decode prices the gap exactly. Compatible with (A) —
  closes the knowledge debt without amending anything.
- **(C) Rule the substrate amendment.** Authorize folding decoded roster counts into the sim's
  waves (E-s09-cp150 rolls superseded for wave population). This is the only path to T1 — and it
  changes what "frozen substrate" means for this run's claims. If taken, the run re-opens under an
  amended charter with the amendment on the record.

---

## 3 — Carried-debt disposition, complete (exit-ramp component b)

**CLOSED during the run** (for the record): UNREACHED-T2 · T3 · T5 · S8-partial (`.lvl` tiling) ·
U-U-6 (I-21's census answered it) · U-T-1 (the run's central question — the march targets YOU) ·
D-I20-1 (repaired in legolas's own seam, v3 CSVs) · D-T-2 (itself a D-I20-1 casualty; corrected by
D-U-2, Lap S's F-12 substantially right) · I-20 look-alike hygiene (digests before bytes) · the
reach-tripwire question (evaluated in-run, did NOT fire, pre-registered with mechanism).

**ROUTED OUT of the run, owner named:**

| debt | route |
|---|---|
| decisions-log package ×5 (D-I15-2 · D-I16-1 · D-I17-1 · D-I18-5 · D-I18-6) | KR → jack-ryan (decisions-log entries) |
| KC2RunSpec S-* limbs · `export/` MIGRATION I-12..I-17 gap · D-PDEF-1 removal proposal (24 `defenses_enabled` uses in `export/` — NOTE-9 refusal held, never repaired by the run) | star-lord |
| Q57 | Matt, non-blocking |
| D-I21-1 player-motion policy fold (model choice with a measured target — Lap U § 1.2 numbers; NOT a decode; must be labelled a policy if ever taken) | future iteration, only under an explicit charter line |

**OPEN — roster-lap-contingent** (fire only under option B/C): C-12/UNREACHED-S7 · C-13 ·
UNREACHED-U3 · UNREACHED-U2+U4/D-PDEF-2 (one decode, three closures).

**OPEN — banked unknowns, non-blocking, honest** (each carries an UNREACHED or U-flag in its
artifact of record): U-P-N-2..5 · U-S-1/3/4/5 · UNREACHED-S1/S3..S6 · UNREACHED-T1/T4 ·
UNREACHED-U1 · U-U-1..5 · U-T-3 (revived at 83.3 % aura coverage; fold experiment only if a
residual points at monster DPS — none does) · U-T-4 · U-R-2/3/4/6 · U-O-1 · D-P1/D-P2 · D-Q1 ·
U-PDEF-1 · U-I19-1/D-I19-2 · D-U-4 · D-I21-2..5 (all self-caught, addendum-before-repair on the
record) · v3 archive-key vacuum (repaired in-run, named) · explosion-centre.

---

## 4 — jack-ryan full wall audit (exit-ramp component a)

> **PENDING — fired 2026-08-14 as named jack-ryan sub-agent; verdict appended on return.**
> Report path: `agentic_orchestration/jack-ryan/notes/2026-08-14-kc2-pm4-full-wall-audit.md`

---

## 5 — The run record, one screen

| unit | what it decided |
|---|---|
| I-15..I-17 | baseline + sustain falsified as the residual's carrier |
| Lap N/O/P/Q | referent instrumentation (OCR counters, FCT, heal discriminator, leech/resist) |
| I-18 · Lap R | locomotion folded; record cells established |
| Lap S | arena decode; geometry-size refuted |
| I-19 | structure folded (graded worse; kept on decode authority) |
| Lap T | arrival-speed decode; beacon measured-negative for movement |
| I-20 | arrival folded (graded worse; kept); U-S-2 measured inert |
| Lap U | **the march targets the PLAYER** — decided by two instructions; residual named CONCURRENCY with the referent's number on the table |
| I-21 | pursuit folded; **first record-cell T2 hit**; census removes exactly ONE term (C-1, model-assumption vs decode); residual re-carriered to **ROSTER SIZE** |

Law-3: `moved == {}` at every iteration, with witnesses. Five FIT-law conductor corrections banked
lifetime. Every defect in the run's artifacts is self-caught and committed before its repair.

---

*Awaiting your ruling on § 2 (A / B / C). The run holds at the boundary.*
