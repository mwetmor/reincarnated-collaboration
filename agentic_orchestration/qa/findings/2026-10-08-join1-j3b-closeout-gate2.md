# Finding — 2026-10-08 — JOIN-1 J3b close-out (rulebook of record `d5384b4b`), Gate-2

**Reviewer:** jack-ryan
**Severity:** WARN (verdict **GO-WITH-AMENDMENTS**: J3b engine side GO and `d5384b4b` is the J3c pin; MIGRATION needs one amendment before drax starts J3c)
**Target:** engine `9047b515` → `d5384b4b` (with `c4a8b6c2` fail-first, `e0f237e0` instruments, `6bf63ef0` declared test corrections, `814a2176` § 5), MIGRATION `032a08b5`; collab `cd7c78e90`, `5c0203328`, `c48f5f3e3`
**Developer:** gamora · conductor gandalf (KP-391/392)
**Principles applied:** 1, 2, 3, 5 · Disciplines #10, #12

## (1) Certification of `d5384b4b`: HOLDS

- P-J2-9 `pass: true`.
- GM provenance rulebook `d5384b4b`, 7/7.
- § 4.7 v4 **ORACLE BYTE-IDENTICAL**, HEAD start = end = `d5384b4b`, kc2 tree unchanged.
- **nc8n:** `bprime_pass: false`, census differs on `run.charge_per_tick`, as predicted.
- `git diff 9047b515 032a08b5 -- src/reincarnated/simulation/kc2` is empty.

## (2) INFO-3 diff: CLEAN

I ran `git diff 9047b515 d5384b4b -- src/join2_rulebook` myself. Three files changed:
- `a2_table.json`: row 36 plus the comma on row 35;
- `crit.py`: `charge_bound`;
- `forms.py`: `charge_per_tick_` and its install mapping.

Nothing else moved. **L04-1, L05-1 and L05-2 at `9047b515` stand.**

## (3) Controls: VALID and AS PREDICTED

Every control has `valid` all true (25 cells, all 25 sim terminal, closure 0, HEAD fixed, pinned, 0 foreign reads, join records) at rulebook `d5384b4b`.

| Control | Result |
|---|---|
| L01-W @ 200 | `all_7_equal` against ORACLE-TWIN@200 (the twin is valid in its own right); period 250/250; both counters empty |
| L01-P | period 250/250; `acc_bound` {0.6533…: 16} per cell = `row31_calls`; `charge_bound` 9.408 on 400 calls. Count definition: per `simulate_wave` call, per the § 5 corrigendum committed before the rulebook. Row 32 per world tick lower in 25/25 |
| L01-1 | `acc_bound` {0.8}; charge 11.520000000000001; ticks up (23/2), leech per tick down (25/0) |
| L04-2 | law check 0; first divergence 25/25; intake up (sign p 0.108, reported) |
| RT | 7/7 |

The X = 300 survival (17/25 vs 20/25), ticks and intake are **reported, not predicted**, which is correct.

**INFO-1 (for J4a):** re-quantisation alone moves the GD baseline at X = 300 by 3 survivals. So G-D4 @ X will differ from @ 196 before any kit effect, and that is why the comparison must use the Warlord re-run at the same X.

## (4) MIGRATION's J3c obligations: INCOMPLETE (WARN-1)

`032a08b5` lists the J3b deltas: the L-01 refusal, row 36, row 35, L-05, and the refusal of `hits_per_tick` < 1 until S-7. Two problems:

**(a) Row 36 has no consented port site.**
- The KP-360 consent covers S-1…S-5, S-7 and S-9, plus M-3 (KP-363). The site list (`J3-SITE-LIST-8a4da5f8.md` § 2) predates KP-388 and names no energy-charge site.
- After J3c lands **S-7, the port will accept `hits_per_tick` < 1**. Without a row-36 mirror the port charges 14.4 per *world* tick, and the Warlord dries out exactly as the engine did at `9047b515`.
- *Action:* drax determines whether the port's per-tick charge has an in-form hook. If it does, it mirrors row 36 in-form. If it does not, that is a **new sealed site**, which needs its own Matt ruling as a ledger row under the sealed-artifact protocol. Until then the port's refusal must read *"`hits_per_tick` < 1 until S-7 **and** the row-36 mirror"*.
- Add the per-tick charge to the S-9 **P0 inventory** of 196-bound values.

**(b) The pin entry does not restate the standing J3c scope.** Cross-reference it in MIGRATION:
- the KP-360/363 sites: S-1…S-5, S-7, S-9 + M-3, with S-6 held;
- ADJ-J1…J4 and ADJ-J6;
- the booking-census row additions;
- the GD order census before NC-J3-L06-4 is quoted cross-mirror;
- the P0 inventory;
- the hunk-audit G-A/G-B fail-first;
- Matt's windowed `.app` self-test.

Also carry the site list's INFO-2 instrument item: the port emitter re-evaluates summon G1 rows with the sealed law (`kc2p_join1_gm_emit.gd:645`), so **L05-2 / L04 summon-lane controls on the port trip its cross-check** unless the JOIN tool supplies the form's re-evaluation, with its own negative control.

## (5) Semantic shifts: DECLARED

- NC-J2-5b is retired; kit > world now refuses.
- The charge is per kit pulse, so the dry-out threshold is 14.4·h.
- L01-W moved from 300 to 200, with the 300 % runs kept as finding evidence only.
- The L01-1 run at `9047b515` is superseded.
- The post-fail-first test corrections are declared (`6bf63ef0`).

## Action
- [ ] gamora / drax: MIGRATION amendment folding WARN-1 (a) and (b) before J3c's prereg. If row 36 needs a new sealed site, the conductor routes a Matt ruling.
- [ ] conductor: INFO-1 into the J4a framing.
- [ ] Matt: only if WARN-1 (a) finds no in-form hook.

## References
- collab `agentic_orchestration/gamora/analyses/2026-10-08-join1-j3b-record/` (`controls/*/control_report.json`, `compare_vs_ORACLE-TWIN@200.json`, `s47v4.stdout.txt`, `s47-nc8n.stdout.json`, `info3_*.patch`)
- engine MIGRATION `032a08b5`; godot `kc2_play/join/J3-SITE-LIST-8a4da5f8.md` (§ 1 INFO-2, § 2, P0); charter ledger KP-360, KP-363 (read-only)
