# WR2-ENCGEO Cell A — aim-line supplementary emission + the R-WR2-2 non-perturbation falsifier

**Run:** WR2-ENCGEO-2026-07-29 · **Cell:** A · **Seam:** gamora · **Date:** 2026-07-29
**Conductor:** gandalf (`RUN-CONDUCTOR`) · **Charter:** `agentic_orchestration/gandalf/notes/2026-07-29-wr2-encgeo-run-charter.md` §1 mechanism A
**Commits (engine, NOT PUSHED):** `c8ef0ba` (harness arm + driver + MIGRATION), `6b13b25` (driver instrument repairs)
**Status:** all five task items COMPLETE. **No HALT.** Nothing graded — the cell computes, the conductor grades.

---

## Verdict table

| # | item | verdict |
|---|---|---|
| 1 | flag located; arming is caller-side, ZERO kernel change | **CONFIRMED — no halt** |
| 2 | supplementary battery re-run into a new sibling directory | **DONE** — 450 fights, 3 legs, `wr1_battery_2_aim/` |
| 3 | **R-WR2-2 falsifier — 450 pairs** | **PASS 450/450** |
| 4 | S-5 shape check | **HOLDS on all three legs**, 450/450 player-attack fights carry ≥1 decision |
| 5 | determinism | **150/150 byte-identical, twice** |

---

## 1 — Flag location, and why arming it is not a kernel change

The instrument **already existed**. R-WR1-22's "zero `decision` events in 450 traces" was never a
missing feature; it was an **unthreaded parameter**.

| what | where |
|---|---|
| engine attribute | `spatial_engine.py:2854` — `self._trace_decisions: bool = False` |
| the emission site the render needs | `spatial_engine.py:~5068` — inside `if self._trace_decisions:`, calls `self._frame_sink.decision(tick, target_id, intent, t_s)` |
| the caller-side parameter | `spatial_engine.py:6943` — `run_spatial_fight(..., trace_decisions: bool = False)` |
| the gate | `spatial_engine.py:7169` — `if trace_decisions: engine._trace_decisions = True` |
| record emitter | `replica_frame_emitter.py:425` — `def decision(self, *, tick, target_id, intent, t_s)` |

All of the above shipped with BW-1 / REPLICA-1 G2 on **2026-07-22**. `spatial_engine.py` is
**untouched by this cell** — verify with `git show --stat c8ef0ba`.

### What DID change (config-level plumbing only)

`kitcal_g5_harness.py` — the battery-emission entry point that produced `wr1_battery_2` — did not
pass the parameter. Threaded, default `False` everywhere:

```
main(--trace-decisions)  →  drive(trace_decisions=)  →  _drive_armed(trace_decisions=)
                         →  run_one_fight(trace_decisions=)  →  run_spatial_fight(trace_decisions=)
```

Plus three declarations, each matching an existing harness convention rather than inventing one:

* `--trace-decisions` CLI flag (shape copied from `--emit-telegraphs`, the other emission-only arm);
* `_dec` label suffix on the artifact directory + report filename (sixth generation of the harness's
  "a report copied out of its directory must still declare its arm" rule);
* `report["wave_regime"]["trace_decisions_wr2_a"]` — additive bool, sits beside
  `emit_telegraphs_r_wr1_12`. It exists because WR1's traces carried zero decisions and **no field
  said why**: a reader could not distinguish "the player never decided" from "the instrument was
  never armed" — the measured-zero / unmeasured-zero confusion P-2 exists to prevent.

**One deliberate non-threading:** the INS-1 insensitivity probe is NOT armed. It emits no trace, so
there is no sink for a decision record to reach; arming it would allocate a discarded list and change
nothing observable — an arm with no consumer.

**MIGRATION.md filed BEFORE the run**, not after (ADR-004 trigger is "a consumer's parse surface
gained a key"): `~/Games/reincarnated-engine/src/reincarnated/simulation/MIGRATION.md`, entry
`[2026-07-29] WR2-ENCGEO Cell A`.

---

## 2 — Emission path

**Driver:** `~/Games/reincarnated-engine/src/reincarnated/simulation/wr2_cell_a_aim_2026_07_29.py`
Run with `python3 -m reincarnated.simulation.wr2_cell_a_aim_2026_07_29`.

It reuses `wr1_battery2_2026_07_29.LEGS` **by import, not by transcription** — R-WR2-5 (same seeds
74000800×30, same legs pre/post/pre_endpoint, same arms, same 36×36 arena) is therefore a property of
the code path rather than a promise in a comment. The argv per leg is WR1's argv with exactly two
edits: `--trace-decisions` appended, `--out-dir` re-pointed. Legs fire SEQUENTIALLY (Discipline #3).

**Output:** `~/Games/reincarnated-engine/src/reincarnated/simulation/output/kitcal_g5/wr1_battery_2_aim/`

| leg | regime | directory | wall |
|---|---|---|---|
| pre | `R2_proxy` | `g5_m4cadence_nova_mitR2proxy_tg_dec/` | 2.8 s |
| post | `R3` | `g5_r3arm_m4cadence_nova_mitR3_tg_dec/` | 3.9 s |
| pre_endpoint | `R2_proxy_resists_low` | `g5_m4cadence_nova_mitR2proxyresistslow_tg_dec/` | 2.4 s |

Statistics artifact: `wr1_battery_2_aim/wr2_cell_a_aim_statistics.json`.

### SS-1 is asserted, not promised

`wr1_battery_2/` was opened **read-only** and never written. The driver asserts at entry that the
output root is neither the banked root nor a descendant of it, for both the aim root and the
determinism scratch roots. `git status` on `output/kitcal_g5/wr1_battery_2/` is clean.

---

## 3 — R-WR2-2 falsifier: **PASS, 450 / 450**

**Method.** Per trace, records are normalized to canonical JSON (sorted keys, no whitespace) and
SHA-256'd in order. `decision` records are dropped from **both** sides — applied to the banked side
too, deliberately: it is a no-op there that proves itself, and dropping on one side only would
manufacture a mismatch out of a schema difference. Two digests per pair:

| digest | exclusions | **matched** |
|---|---|---|
| `raw` | decisions only | **0 / 450** |
| `declared` | decisions + `header.engine_git_hash` | **450 / 450** |

**VERDICT: PASS.** The fights are the same fights.

### The 0/450 row is the evidence, not an embarrassment

A falsifier that quietly excludes fields until it passes proves nothing. The `raw` row states what
the single exclusion is worth: without it, **every** pair differs. The exclusion is therefore live,
named, and worth reporting.

**The one excluded field, declared:** `header.engine_git_hash`. It is **run identity, not fight
content** — the banked battery ran at `7f77ea0`, the supplementary set at `6b13b25`. A digest
including it could only ever say "different", which is a comparison that cannot fail informatively.

**The exclusion's blast radius is INSPECTED, not trusted.** The driver computes the field list that
separates `raw` from `declared` and refuses if it carries anything beyond the declared set. Observed:
`['engine_git_hash']` — exactly the declared set, nothing more. This is what stops an exclusion list
from quietly growing to absorb a real perturbation.

**Non-perturbation is now measured, not argued.** The pre-existing argument — the instrument reads an
already-chosen target and an already-evaluated advance/hold predicate, draws no RNG, writes no
HP/position — is a claim about code someone read. This is a claim about 450 fights that ran.

---

## 4 — Gate S-5 shape check (computed, NOT graded)

"Player-attack fight" is operationalized as `breadth.presses > 0`, read from each leg's own report —
so the population is defined by the battery's own record, not by this driver's opinion.

| leg | regime | fights | player-attack fights | zero-press | **decision events** | per-fight min…max | `advance` | `hold` | S-5 shape |
|---|---|---|---|---|---|---|---|---|---|
| pre | `R2_proxy` | 150 | **150** | 0 | **40,046** | 50 … 671 | 1,680 | 38,366 | **holds** |
| post | `R3` | 150 | **150** | 0 | **45,362** | 50 … 590 | 1,680 | 43,682 | **holds** |
| pre_endpoint | `R2_proxy_resists_low` | 150 | **150** | 0 | **32,499** | 50 … 635 | 1,680 | 30,819 | **holds** |
| **total** | | **450** | **450** | **0** | **117,907** | | **5,040** | **112,867** | |

**Zero-press fights = 0 in every leg**, so the S-5 denominator is the whole battery — the predicate
is not satisfied vacuously by an empty population.

**`decision` count == `tick` count, EXACTLY, in all 450 traces.** One aim-line per tick, no gaps: a
renderer can index decisions by tick with no fallback branch.

`intent` takes only `advance` / `hold`. `evade` remains structurally unreachable on the production
path (`piloted_competence` is not passed by this harness) — MIGRATION's M-6 §2 statement is unchanged.

### ⚠ The S-5 census is also a Cell-C datum, and it is reported as one

**`advance` totals 1,680 per leg — IDENTICAL across all three mitigation regimes.** Per tier that is
**6 (trash) / 7 (mixed_pack) / 11 (champion) / 16 (boss) ticks per fight**, after which the player
**HOLDS for the entire remainder**. The approach phase is regime-invariant because it is over before
mitigation matters.

This corroborates the Cell-SPEC §0 finding from an **independent instrument**: the player has no
contact-range movement policy at all. Two consequences worth having before Cell C fires:

* **Cell C fills a near-empty policy, it does not replace a busy one.** ~99 % of the player's
  decision ticks are `hold`.
* **A renderer should expect a mostly-static aim-line.** Matt watching the BEFORE render will see the
  line snap to a target and stop moving; that is faithful to the sim, and it is the thing Cell C
  changes.

---

## 5 — Determinism: **150 / 150 byte-identical, twice**

Leg `pre` fired **twice** at the same seeds into two scratch roots, traces compared **byte-for-byte**
(no normalization — a determinism check that normalizes is weaker than the one S-4 asks for).
Reports are excluded from the comparison because they embed absolute trace paths, which differ by
scratch root by construction.

Cross-check against the banked aim set: identical **including** the header line (both stamped
`6b13b25`).

### The first determinism run FAILED, and the reason is worth keeping

The first attempt compared one replicate against the banked aim set and reported **150/150 differing
at exactly 6 bytes each**. The 6 bytes were **`-dirty`**: the aim set was emitted from a clean tree at
`c8ef0ba`, and the replicate ran while a one-line repair to the driver sat uncommitted, so
`_git_hash()` correctly stamped the header differently. That is SESSION 90's own provenance detector
doing precisely its job.

**A determinism check that straddles a tree change measures the tree, not the RNG.** The replicate is
now self-contained: two fires, one tree state, one process. The whole cell was then re-fired from a
clean tree so the aim set and its verifier share one stamp.

*(Second instrument bug, same class, also mine: the gap-inspector parsed display-truncated 600-char
strings and could only ever return `<unparseable>` — it tripped the driver's own refusal on a run
whose 450 digests had all matched. Both repairs are in `6b13b25` with their reasons in the docstrings.)*

---

## 6 — Artifact size and the git decision

**Precedent checked as instructed:** `wr1_battery_2/` **is tracked** — 454 files (450 traces + 3 leg
reports + 1 statistics), 129 MB. This cell **matches that precedent**.

| directory | size | committed |
|---|---|---|
| `wr1_battery_2/` | 129 MB | tracked (pre-existing, FROZEN) |
| `wr1_battery_2_aim/` | **145 MB** | **yes** — matches precedent; drax's Godot playback consumes these |
| `wr1_battery_2_aim_determinism{,_b}/` | 42 MB each | **no** — regenerable scratch; the result lives in the statistics artifact |

Per-trace growth measured at **+5 %** (trash) to **+16 %** (boss). **Flagged to the conductor:** this
adds 145 MB to the repo. If that is unwanted, the aim set is fully regenerable in ~9 s of wall time
from `c8ef0ba`+ by one command, and the note + driver + harness arm are sufficient to reproduce it.

---

## 7 — Test evidence

| suite | result |
|---|---|
| `test_kitcal_g5_harness.py` + `test_bq3_calibration_override_door.py` | **70 passed** |
| `test_aware_fighter_policy_seam.py` + `test_spatial_gauntlet_scenarios.py` | **72 passed** |
| `--smoke` armed vs unarmed, seed 74000700, 5 fights | tick / damage / death / telegraph counts and every fight verdict **identical**; `decision` 0 → {59, 68, 248, 373, 635} = the tick count exactly |

**Full regression NOT run**, and that is stated rather than omitted (the WR1 §8.19 lesson): this
landing is caller-side threading behind a default-off flag, with `spatial_engine.py` untouched.
Gate-2 may reasonably require the full name-diff; it is not self-cleared here.

---

## 8 — For the conductor

* **S-5 is GREEN on shape** and **R-WR2-2 is PASS** — the two halves of the charter's S-5 predicate.
* **Nothing is graded here.** Every number above is a measurement with its predicate quoted.
* **Handoff to drax:** the render source is `wr1_battery_2_aim/`, schema-identical to
  `wr1_battery_2/` plus the decision record class. The MIGRATION entry carries the loader notes.
* **Handoff to Cell C:** the `advance`/`hold` census in §4 is prior evidence about the policy Cell C
  is about to write.
* **Not pushed.** Both engine commits are local.

---

*gamora, 2026-07-29. The cell computes; the conductor grades.*
