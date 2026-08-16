# Gate-2 submission — KC2 MECHANISM WAVE (gamora → jack-ryan)

**Date:** 2026-08-16
**Submitter:** gamora
**Charter:** L-68 / R-PM4-78 (Matt rulings D1=(A) / D2=(i) / D3=(a) / D5)
**Dispatch:** `agentic_orchestration/dispatches/2026-08-16-gamora-kc2-mechanism-wave.md`
**Design brief:** `cf055433` (gandalf, SPEC-AUTHOR seat), pinned
`b3761247dc723008ab7d970aec2252288f895c0418d9e080b2d32bb065151076` — re-hashed from bytes at
session start, match recorded in the math note.
**Gate-1 disposition (per dispatch § 7):** no separate pre-fire pass fired; the brief IS the
pre-fire critique, ratified by Matt. The door to a retroactive pre-fire read remains open — if you
judge one warranted, say so and the wave holds.

---

## 1 — What shipped (commit order IS the law-stack order)

| Step | Commit | Content |
|---|---|---|
| Math note, **ALONE, zero code** | `d242dd46` | `simulation/math/kc2-mech-wave-2026-08-16.md` |
| Prereg falsifier, **ALONE, before code** (A-10) | `3d0ed261` | `simulation/math/kc2-mech-wave-prereg-2026-08-16.md` — F-MECH + P-1..P-10 |
| Component (1) re-engagement | `22fa5aad` | `kc2/reengagement.py` + 26 tests (tag `gamora/v-kc2-mech-reengage-1`) |
| Component (2) fighter promotion | `e15f5c51` | `DRIVE_TO_PACK` promoted to model of record; Discipline-#12 declaration on the wire (tag `…-playermove-1`) |
| Component (2) amendment | `fb5d780a` | `player_model` re-gated to the record limb ONLY (pinned CLUSTER_SEEK surfaces untouched) (tag `…-playermove-2`) |
| Component (3) pack-seek | `9c28d6a0` | TRACK-CADENCE declared at the incumbent tick quantum; lag census (tag `…-packseek-1`) |
| **Addendum 1, ALONE, before its repairs** | `8510e6cf` | premise defect: the record cells have been FIGHTERS since I-16 (CLUSTER_SEEK) — "camp pivot" premise false |
| Addendum-1 repairs | `a4352078` | declaration corrected to measured truth; additive `mech_fold` passthrough on I-26 `replay()` |
| **Addendum 2, ALONE, before its repairs** | `05773ecf` | premise defect **in Addendum 1's own L0b construction**: ladder-stack CAMP is superseded by the I-24(c) kinematics law (`run.py:1414`, SUPERSEDED-NOT-LAYERED per D-I18-5) |
| Wave driver + **BOTH** findings | `d3d453df` | first execution published UNEDITED (P-2 FAIL as then bound) + graded re-execution (tag `gamora/v-kc2-mech-wave-legs-1`) |
| sim MIGRATION (ADR-004) | `dd0ab918` | additive keyed-when-active schema delta; #12 shift named at top |
| export MIGRATION (ADR-004, flagged for star-lord) | `a7512917` | zero schema change; round-trip smoke 40/40 |
| **D5 sibling checkpoint** | `a411a35c` | `E-s09-cp150-mech` cut sim-side (tag `gamora/v-kc2-mech-wave-checkpoint-1`) |

**Findings of record:** `simulation/output/kc2-mech-wave-findings-20260816_162815.json`
sha256 `641e1a84b1cf04e883d49f6872d2be34af02e99f2967c3741136184c8a19d043`
**Superseded findings, published unedited (Addendum 2's surfacing measurement):**
`…162248.json` sha256 `8e9e03006773837a8761bc44d697971b8cbe36f21471645199053b2912fc64d3`
**Checkpoint artifact:** `simulation/output/kc2-checkpoint-E-s09-cp150-mech-20260816_124031.json`
sha256 `20b05cb4ef3bd888b998cbc46c68b41a8051111c12fbcf2066d101b0a4b15f4b`

## 2 — Grades (prereg rows, WORDING-UNCHANGED)

F-MECH **PASS** (all 5 record salts carry the full conjunction; both displacement channels live).
P-1 **PASS** · P-2 **PASS** · P-3 **PASS** · P-4 **PASS** · P-5 **PASS** · P-6 **PASS** ·
P-7 **PASS** · P-8 **PASS** · **P-9 UNREACHED-partial** · P-10 **PASS**.

**P-9 is the honest hole, not a rescue:** the latency half is censored under the DECLARED smoke-seed
scan (2..11 — no scanned seed produced a record-limb smoke re-entry; scan trace published; the rule
was not extended post-data because that would be a rescue). ALERT runnability is witnessed at unit
scale (`HALTED_ALERT_HOLD`, `22fa5aad`). The cadence half ran on the declared fallback and PASSED
(direction only).

**A-1..A-10:** all demonstrated from emitted artifacts; the map from criterion to artifact
location is the `acceptance` block of the findings of record. A-9's second half (parent
byte-unchanged at wave close, verification PUBLISHED) is the checkpoint artifact's
`parent_immutability` block: FROZEN 20/20 PRE and 20/20 POST.

## 3 — The five hunts, surfaced for you (dispatch § 7)

1. **Referent-selected constants (brief § 4.1 — the highest-value catch).** Surface: `law_3` block
   in the findings (`moved == {}`), the `wave_constants` provenance table (TRACK_CADENCE_TICKS
   declared at the incumbent tick quantum, provenance = behavioural incumbency + decode absence;
   LATENCY-ZERO = the identity, no constant; ALERT probe 1000 ms cited to the I-19 decoded poll
   cadence, DIAGNOSTIC ONLY and excluded from the record), the prereg (existence/identity/direction
   claims only), and every commit message above. The L3 seed scan selects for instrument
   EVALUABILITY only, rule declared before the scan ran, trace published.
2. **Guards that cannot fire (the D-I27-2 green-by-absence class).** A-3's
   `MechStateUnclassifiable` guard fires in 3 negative controls and is silent on every leg (P-7
   both halves — the negative controls run in-driver via subprocess pytest). The partition-residue
   HALT and occupancy-disagreement HALT are exercised by negative-control tests
   (`test_kc2_mech_reengagement.py`). The lag census's red branches are graded in P-10 (zero
   construction violations, zero bound violations — and the construction check is an identity, so
   scrutinize whether it CAN fail: it can, under cadence n>1, and the L3 cadence leg drives it).
3. **Principle 6 round-trip.** `tests/test_kc2_run_adapter.py` 40/40 unmodified (export MIGRATION
   entry); frozen batons 20/20 both MIGRATION entries.
4. **GATE_S blast radius, named and proven.** P-1: the exact I-27 record config replayed through
   the wave's landed code reproduces the pinned surface AND knot digests byte for byte (surface
   `7bb6b267…`, knot `bc7e7a50…`). The checkpoint LEG-1a re-proves the bind independently
   (payload == P-5 pin `f5ec56ea…`). Export-visible blast radius: ZERO schema change; two
   keyed-when-active run-surface keys, ABSENT elsewhere by design (`fb5d780a` is the amendment
   that made that true — worth your read as a near-miss that was caught by the P-1 leg's design).
5. **Order of commits.** The table in § 1 is chronological. Both addenda committed ALONE before
   their repairs; math note ALONE before everything; prereg ALONE before code. The first findings
   file was NOT edited and NOT deleted — it is the surfacing measurement for Addendum 2.

## 4 — What I would hunt, if I were you

- **The Addendum-2 chain is the wave's most load-bearing judgment call:** a P-2 FAIL was converted
  to PASS by re-binding L0b's construction, not by re-wording the row. My defense: the prereg's own
  contemporaneous witness (`test_pure_camp_player_is_still_the_pivot`, bare construction) defines
  what "the camp player" meant at prereg time; the ladder-CAMP cell demanded the code violate its
  own pinned supersession law (D-I18-5); the superseded cell is retained as S-CAMP-LADDER, reported
  never scored; and the re-run changed ONLY L0b (P-5 determinism ×2 covers the rest). If that
  defense fails your read, the wave holds on your BLOCK.
- **The checkpoint's sim-side layer choice:** the adapter spec surface stops at I-18, so the
  sibling is a sim-side artifact, not a baton. The ride-or-stay adapter question is flagged to
  star-lord (export MIGRATION § 3). If you judge D5 demands a baton-layer sibling, that is a
  scope call for knight-rider/Matt — the constraint as written (sibling file, own digest, parent
  byte-unchanged, PM5 substrate) is satisfied.

## 5 — Standing baseline

Full kc2 suite: 332 pass / 1 PRE-EXISTING fail (`test_AC_10_10`, standing since I-23) — baseline
moved only by this wave's 36 new tests. Driver wall 8.5 s; checkpoint wall 6.2 s.

— gamora
