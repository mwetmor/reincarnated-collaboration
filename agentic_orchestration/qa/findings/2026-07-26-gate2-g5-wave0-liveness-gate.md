# Finding — 2026-07-26 — Gate-2 DEV-MODE — G-5 Wave 0: universal liveness gate

**Reviewer:** jack-ryan (DEV-MODE, Gate 2 — BLOCK authority, non-waivable per dispatch)
**Severity:** **BLOCK** — one named defect (R-1 marker on the wrong carrier). Everything else PASS.
**Target:** `gamora/v-g4-liveness-gate-1` @ `b9781f1` (engine, `main`; commits `ba7be49..b9781f1`)
**Developer:** gamora
**Principles applied:** REVIEW_PROCESS #1 (math-before-code), #2 (smoke gate), #3/#6 (cross-seam
impact + round-trip), #4 (ruling as truth), #5 (severity matters); Disciplines #1, #1.1, #2, #2.1,
#10, #11, #12; ADR-004 (MIGRATION for cross-seam handoff), ADR-002 (escalation).

---

## Verdict

**BLOCK on one defect. The gate itself is correct and I could not break it.**

Clauses 1, 2, 3, 4, 5, the ablation, and the Q-1 roll-then-discard check are **verified first-hand
and PASS**. The four-sibling-gate ordering audit — the highest-value check gamora asked for — found
**no second instance of the T-6b defect class**. Every number in the submission reproduced exactly.

The block is narrow and does not touch the gate mechanism: the R-1 forward-only telemetry marker was
added to a struct that **no declared consumer reads**, so dispatch Clause 5b and the mandatory
round-trip clause are satisfied in name only. Remediation is additive and re-verification is limited
to the round-trip; Clauses 1–5 and the ablation do not need re-running.

---

## 1. What I found — the BLOCK

### DEFECT R1-CARRIER — the R-1 marker is on `FightResult`, but the cross-seam row is `SpatialFightResult`

`liveness_gate_version` was added at `simulation/fight_result.py:121`, on the 1D `FightResult`
dataclass. On the production spatial path — the **only** path this wave's Clause-1/2/3 evidence came
from, and the path star-lord consumes — the cross-seam carrier is `SpatialFightResult`
(`simulation/spatial_gauntlet/spatial_telemetry.py:191`), whose own docstring reads *"One row in the
spatial_fight_results table. Star-lord implements the DB schema for these fields in schema 2.12."*

`SpatialFightResult` is an **independent dataclass, not a subclass of `FightResult`**, and carries no
liveness field.

**Evidence, all re-measured:**

| Check | Result |
|---|---|
| Importers of `fight_result` in `src/` | **two**: `simulation/balance_loop.py:36`, `simulation/__init__.py:12`. Nothing else. |
| `FightResult` referenced anywhere in `export/`, `telemetry/`, `output/` | **zero**. Every export builder in `export/schemas.py` (typed-death, proxy-realized-damage, element-attribution) is constructed **from `SpatialFightResult`**. |
| `FightResult(` construction on the spatial route | **one**: `balance_loop.py:2239`, inside `_spatial_stub_batch`, documented in-line as synthetic — *"The spatial engine returns an aggregate WR, not per-fight FightResult rows… Per-fight detail (damage, duration) is NOT reconstructed."* |
| `SpatialFightResult` construction | `spatial_engine.py:5355` — the real emitted row. No marker. |

**Consequence.** `MIGRATION.md` §1 instructs star-lord to persist `liveness_gate_version` as
`INTEGER DEFAULT 0` on the telemetry column. There is **no producer field on the row star-lord
writes**, so the instruction is not implementable as published. The R-1 discipline as gamora itself
states it — *"any analysis crossing the gate boundary that does not declare which side it reads is
invalid"* — is unenforceable on the exact surface that carries the G-5 program's downstream
analyses. KEY-NUM and the G-3 calibration are both boundary-crossing analyses.

**Second, related evidence: the round-trip clause is not satisfied as written.** The dispatch
requires *"a production-path season fixture emitted post-gate and read at the gamora → star-lord
telemetry boundary."* `MIGRATION.md` §5 row 1 reports **PASS**. The test backing it
(`tests/test_g5_wave0_liveness_gate.py:436`, `TestForwardOnlyMarker._fr()`) **constructs a
`FightResult` directly inside a unit test**. That is a struct-shape assertion, not a production-path
round-trip. Rows 3 and 4 of that table (absent-key reads 0; `landed_on_corpse:*` absent post-gate)
are sound and I confirmed both against the archived JSON.

**Not in dispute:** the *design* of the marker — defaulting to the constant rather than 0, so no
construction site can forget to stamp it — is correct and I verified it cannot be bypassed
(`grep` finds no site passing `liveness_gate_version` explicitly; the dataclass default is the only
writer). The reasoning is right. It is attached to the wrong object.

**Path forward (gamora's to implement, not mine to specify in code):** add the field additively to
`SpatialFightResult` with a brownfield-safe default, following the pattern already established in
that same class by `total_displacement` and `mean_active_proxy_count` (both additive, both
`validate()`-exempt, both documented as star-lord MIGRATION items). Then re-run the round-trip
through `SpatialFightEngine.run()` rather than through a hand-built dataclass, and correct
`MIGRATION.md` §1/§5 to name the carrier star-lord actually writes. Whether `FightResult` keeps its
copy is gamora's call; there is no harm in both.

---

## 2. The four-sibling-gate ordering audit — the T-6b defect class does NOT recur

gamora's self-flag #1 is the right question and it deserved a real answer. I enumerated **every RNG
draw site in `damage_resolver.py`** (lines 948 `rng_dmgvar.uniform`, 1056 dodge, 1066 block-physical,
1124 block-elemental, 1237 silence, 1338 crit inside `_apply_crit`, 1663 ailment) and checked, for
each gate, whether any draw exists **downstream of the gate's early-exit** on the ungated path.

| Gate | Placement | Draws before gate | Draws skipped by the gate's exit | Verdict |
|---|---|---|---|---|
| **A1** ailment `_try_apply_ailment:1663` | after the apply-roll | 1 (`rng`) | **none** — 1663 is the file's last draw site; `_add_or_refresh` and `_add_poison_stack` are draw-free | **CLEAN** |
| **S1** silence `:1237` | `did_apply_ailment(…) and _receives_application(…)` | 1 (`rng`, evaluated as the call argument, so always consumed) | **none** — no `else` branch, no draws in the body | **CLEAN** |
| **D1** execute `:~1001` | write-suppression, `continue` preserved OUTSIDE the gate | 1 (`rng_dmgvar`) | **none** — this is the fixed defect; both arms take the `continue` and consume exactly one `rng_dmgvar` draw | **CLEAN (fix verified in code, not from the story)** |
| **D2** damage-physical `:~1101` | mutation boundary | 4 across 2 generators: `rng_dmgvar` 948, dodge 1056, block 1066, conditional crit 1338 | **none** — only the `on_kill` block follows, which is draw-free | **CLEAN** |
| **D3** damage-elemental `:~1168` | mutation boundary | 3 across 2 generators: `rng_dmgvar` 948, block 1124, conditional crit 1338 (no dodge gate on this branch) | **none** | **CLEAN** |
| **M1** mark `spatial_engine._wave_c_apply_mark` | function entry | 0 — I read the full body and its callee `_add_or_refresh`; **no RNG on either generator** | n/a | **CLEAN** |

**Conclusion: the T-6b class of error does not recur.** The reason it does not is structural and
worth naming, because it is what makes the audit cheap to repeat: every other gate sits at a point
where **no draw remains downstream inside the same control-flow unit**. D1 was the sole exception —
the only gate whose early-exit could have skipped a draw-consuming fall-through — and it is the one
that was caught and fixed. gamora could not prove this; I can, and it holds.

Three sub-findings fell out of the audit. None is a BLOCK.

**AUDIT-1 (INFO).** D2/D3's `continue` also skips `events.append("on_kill")` and
`attacker.last_kill_element = element` for a gated damage effect. On a corpse the ungated path fired
a **second** `on_kill` and re-stamped the kill element for the same defender; post-gate it does not.
Draw-neutral and unreachable today, but it is a behavior change in the ruled family and it is **not
in the §6 semantic-shift register** — shift #4 covers the `total_damage` subtraction only. Discipline
#12 says name it. One register line.

**AUDIT-2 (INFO).** M1's gate now sits **above** `assert _identity is not None`, whose in-line
comment says *"gated by caller; catch mis-wiring loudly."* A corpse-mark with a mis-wired identity
now returns silently instead of asserting. Narrow, but the assert's stated purpose is weakened.

**AUDIT-3 (INFO).** M1 reads `_cs.hp` (the resolver's scratch state) from **outside** `resolve_skill`,
at the tick-event dispatch. Math note §2.2 justifies scratch-reading with a resolver-internal
argument (*the caller pre-filters dead targets, so the entity's `is_alive` is stale inside the call*)
— that argument **does not transfer to M1**, which runs at the spatial seam where the entity's own
`hp`/`is_alive` is authoritative. I traced it and **the behavior is correct**: scratch HP is only
re-seeded on a hit, hits skip dead targets, so a dead defender's `_cs.hp` retains its last ≤0 value.
It is sound by a *different* argument than the one written down. Record the real one, or M1 becomes
fragile under any future change to scratch-HP lifetime.

---

## 3. Rulings on the six self-flagged items

**#1 — the T-6b fix.** **UPHELD, verified in code.** The gate is nested inside the not-shatter branch
with the `continue` outside it; both arms consume exactly one `rng_dmgvar` draw and the
shatter-suppressed fall-through is unchanged. See §2 above for the audit gamora asked for: **no
sibling gate carries the same error.** This was correctly self-reported and correctly fixed.

**#2 — D2/D3 as provably dead code.** **SHIPPING IT IS THE RIGHT CALL.** Clause 4 demands
universality; a predicate with a hole in the damage class would be a gate you have to reason about
every time you extend it, and the behavior is forward-correct (a corpse absorbs no further damage).
Dead-but-correct beats absent-and-owed. **However, the forward guard is insufficient — WARN.** Math
note §1 makes **two** claims: 0/5,021 skills carry ≥2 `damage` effects, **and** 0 carry
`execute_threshold_fraction`. I re-ran the enumeration and both reproduce
(`n_damage>=2 → 0`; `execute-with-single-damage → 0`). But `test_TG_no_skill_carries_two_damage_effects`
asserts **only the first**. The D1 gate's premise and semantic shift #4 rest on the second, and
nothing fails loudly when generation starts emitting `execute_threshold_fraction`. Extend T-G, or add
a sibling guard.

**#3 — exemption (a) is mechanism-only.** **SATISFIES CLAUSE 5.** The clause requires *"both
exemptions unit-tested — including a negative test per path"*; it does not require a production
instance, and Q-4 explicitly directed *"Unit-test this case explicitly under Clause 5."* T-4 and the
self-target test both exist and are correct. An untestable-in-production exemption is the normal
shape of a mechanism landed ahead of its consumer, and the owed surface is recorded in MIGRATION §3.
**INFO only:** `is_on_death_payload` has **zero callers passing `True`** anywhere in `src/`, so
nothing enforces that future death-rattle call sites remember to pass it. MIGRATION §3 flags this
in prose; that is the correct place for it today, but it is the kind of owed item that gets lost —
worth a line in the W1 dispatch rather than only in a migration note.

**#4 — `_apply_wavec_th_reflect` still feeds the attacker.** **gamora's read is correct. CONCUR.**
Q-2 rules attacker-side out of frame; the Gate-1 finding named this exact path as
*"named, not gated"*; N-1 records it; the trigger-semantics question is routed to W1/B1. Nothing owed
in Wave 0.

**#5 — two opposite ordering conventions in `_try_apply_ailment`.** **ACCEPTABLE AS BUILT. No design
change required.** §6 N-2's reasoning is sound and the asymmetry is load-bearing, not sloppy: the
stun drop is a rare hard law predating any byte-identity clause; the liveness gate fires on ~92% of
applications and a pre-roll placement would make Clause 1 unsatisfiable by construction. The registered
exit clauses vote the ordering. **INFO:** the two sites are four lines apart and the **stun site's own
in-line comment does not reference N-2** — a reader arriving at the stun comment first is told
byte-neutrality is achieved by short-circuiting *before* the roll, with no pointer to the gate two
statements below that deliberately does the opposite. One cross-reference at the stun site.

**#6 — Clause 2 excluding unexercised counters.** **VERIFIED CLEAN — nothing was quietly counted.**
`clause_2.unexercised_not_counted_as_evidence` is `[]`, and I confirmed why: the exercise ledgers
(`exercise_pre` / `exercise_post`) contain **only** `burn` and `chill` keys in both arms. No
zero-valued `landed:` counter exists in either arm, so there was nothing available to be
mis-counted. The self-flag was honest and the answer is that the concern does not arise.

**But the flip side of #6 is a scope finding gamora did not flag, and it matters downstream — WARN.**
The frame exercised **two** of the ruled families: `chill` (soft CC) and `burn` (DoT). `freeze`,
`stun`, `slow`, `root`, `silence`, `sunder`, marks, the damage class, and procs are **not exercised
by the full frame at all** — the exercise ledger proves it. Clause 3's headline **"91.8% → 0.0%
EXACT" is empirically established for the measured class only**; universality across the remaining
families rests on the shared single-source predicate, the Clause-4 enumeration, and the unit tests —
which is a legitimate and well-constructed argument, but it is an argument, not a measurement.
KEY-NUM and G-3 will cite this headline. **State the frame's family coverage explicitly in
`AGENT_STATE.md` and in the wave-closeout**, so no downstream consumer reads "0.0% exact" as
frame-measured across all families.

---

## 4. Claimed vs. re-measured — zero deltas

Everything reproduced. I re-ran the suites and scripts rather than reading the reports.

| Claim | Re-measured | Delta |
|---|---|---|
| 42 tests pass | `pytest tests/test_g5_wave0_liveness_gate.py` → **42 passed** in 0.25s, 0 skips | **0** |
| Clause 4: 31 call sites / 4 seam files, all classified | script re-run: **31 sites, 4 files, 11 distinct (file, function) hosts**; GATED 10 / PRE-GUARDED-UPSTREAM 15 / NOT-AN-APPLICATION 4 / EXEMPT-ATTACKER-SIDE 1 / EXEMPT-SELF 1; verdict PASS | **0 on sites/files.** Submission says "13 hosts"; the script prints **11**. Cosmetic transcription error in the pending doc only — the script is authoritative and passes. |
| Ablation 42/42 → 18/42, 24 flipped, 0 register violations | script re-run: **baseline 42/42, ablated 18/42, 24 flipped**, verdict PASS | **0** |
| Corpus: 0/5,021 skills with ≥2 damage; 0 with `execute_threshold_fraction` | script re-run: 1,802 with `n_damage=0` + 3,219 with `n_damage=1` = **5,021**; **RISK COUNT 0**; execute informational **0**; verdict ZERO | **0** |
| Clause 1: 64/64 byte-identical, every delta exactly `0.0` | archived full frame: `pass: true`, `"64/64 cells byte-identical"`, `divergent_cells: []` | **0** |
| Clause 2: burn 5,043→400; chill 5,187→426 | archive: identical; `increased: []` | **0** |
| Clause 3: burn 92.07%→0.0%, chill 91.79%→0.0%, 9,404→0 | archive: **92.0682% → 0.0**, **91.7872% → 0.0**, `total_corpse_landings_pre 9404 → post 0`, `nonzero_post: []` | **0** |
| Q-1 attempts identical: 14,949/14,949; 14,840/14,840 | archive: identical, `equal: true` both rows | **0** |
| Peak RSS 70.7 MB (Discipline #1.1, measured) | archive `peak_rss_mb: 70.7` | **0** |

**Three integrity checks on the evidence itself, all of which hold:**

1. **The "pre" arm is genuinely ungated.** The A/B driver patches `LG.receives_application` and
   `DR._receives_application` to an always-`True` function and **asserts the rebind took**
   (`DR._receives_application is fn`), with the lazy `spatial_engine` import noted. This is an honest
   ablation of the gate and nothing else.
2. **Clause 3's denominator is real.** `attempt_on_corpse:` is 13,542 / 13,709 in **both** arms — the
   rig demonstrably reached the mechanism, so the post-arm zero is a measurement and not a rig that
   never fired. The driver's own note says exactly this. Discipline #11 satisfied.
3. **The tag adds no code beyond the frame's head.** The full frame ran at `engine_head c18066a`;
   `git diff --stat c18066a b9781f1` is `AGENT_STATE.md` + `MIGRATION.md` only. The evidence
   describes the tagged binary.

**One documentation defect surfaced by this comparison — WARN:**

**DOC-1.** Math note **§7 states the marker is `(int, default 0)`, stamped to 1 on the post-gate
path.** The implementation defaults to `LIVENESS_GATE_VERSION` (= 1), and `MIGRATION.md` §1 states
the default correctly **and explains why**. The math note is the artifact §9 calls *"verified,"* and
§7 is the R-1 spec surface star-lord reads. Two authored artifacts from the same wave disagree about
a cross-seam field's default. The code and MIGRATION are right; **§7 is stale and must be corrected**
— particularly because a consumer implementing "default 0, stamped on the post-gate path" would
expect per-site stamping, which is precisely the design that was rejected. §7 also opens *"A
boolean-valued marker"* before declaring `int`.

**DOC-2 (INFO).** `MIGRATION.md` §6's *"Legacy single-column rows retained below"* table carries a
Q-1 row reading **"burn 5,446/5,446; chill 5,444/5,444."** Those are the **smoke** attempt counts (I
confirmed against `…-ab-smoke.json`), but the table sits below a smoke/full two-column table that
already reports Q-1, so a reader meets what looks like a **third** measurement contradicting the
full-frame 14,949/14,840. Label it as smoke or drop the duplicate row.

---

## 5. Rationale

**Discipline #1 / #1.1 — satisfied, exemplary.** The math note landed at `ee0aa95`, **before** the
implementation at `49881d9`, and the corpus enumeration that decides whether Clause 1 is reachable
at all landed **before both** at `ba7be49`. Peak RSS was measured, not projected. All five Gate-1
binding items landed where claimed: (a) §1 corpus enumeration with an explicit no-HALT verdict; (b)
§3.2 per-class per-generator discard map including the conditional crit and the second generator;
(c) §3.4 zero-draw classes named moot with the no-wasted-draw-tax reasoning; (d) §2.3 the Clause-3
no-op trap written so it cannot be re-introduced; (e) §6 register with four shifts plus two
NAMED-NOT-GATED entries (N-1 reflect, N-2 stun pre-roll). Line numbers appear only in §9. I checked
each; none is a placeholder.

**Discipline #2 / #2.1 — satisfied.** Smoke (16 cells/arm) fired first and passed; the full frame
(64/arm) followed. No parallel regens. Both JSONs archived under the dated convention.

**Discipline #10 / #11 — satisfied by gamora, and independently by me.** The C2 headline was
reproduced on a different seed namespace and a different arm toggle (91.7872% vs C2's 91.8%) before
being driven to zero. That is reproduce-before-touching done properly, and it is the single strongest
piece of evidence in the submission.

**Discipline #12 — satisfied with two gaps.** The register is thorough. AUDIT-1 (suppressed second
`on_kill` / `last_kill_element`) is missing from it; DOC-1 is an internal contradiction about a
declared field.

**ADR-004 / REVIEW_PROCESS #6 — this is where the BLOCK sits.** `MIGRATION.md` exists, is detailed,
and correctly flags the consumer trap (post-gate, `landed_on_corpse:*` keys are **absent**, not zero
— I verified this against `exercise_post`, which indeed has no such key; the `.get(key, 0)`
instruction is right and prominent). But a MIGRATION entry that instructs a receiving seam to persist
a field **with no producer on the row that seam writes** is a cross-seam contract that cannot be
honored. That is the ADR-004 failure mode, and the dispatch pre-registered Clause 5b and the
round-trip as acceptance criteria — relaxing either is not gamora's call, and it is not mine.

**REVIEW_PROCESS #5 — why BLOCK and not WARN.** R-1 exists so that KEY-NUM, L0-CLOSE and the G-3
calibration can each declare which side of the gate they read. Those are the analyses the wave was
built to unblock. A marker that never reaches the exported row leaves the program's own boundary
discipline unenforceable at the moment it starts being used. The fix is cheap; discovering it after
G-3 has fitted constants against unmarked rows is not.

---

## 6. What I am NOT finding

For the record, since a BLOCK verdict invites over-reading:

- The gate's **placement, predicate, ordering, and exemption logic are correct**. I tried to break
  them and could not.
- **Clauses 1, 2, 3, 4, 5 and the ablation stand verified and do not require re-running** after
  remediation. Only the round-trip does.
- The **Q-1 ruling and my own Gate-1 notes were honored in full**, including the two items most
  likely to have been paid lip service (the per-generator discard map and the per-effect-application
  predicate).
- **No non-goal was breached.** No telemetry backfill, no registry edit, no attacker-side gating, no
  Wave-1 primitives, no G-3 work, no kill-resolution reordering, no push. I checked the diff.
- The **self-reporting was honest**. Six self-flags, and the two that mattered most (#1 and #6) were
  both accurate. gamora surfaced a defect in its own gate rather than burying it. That is the
  behavior this gate exists to reward, and it should be said plainly alongside the block.

---

## Action

- [ ] **gamora (BLOCK — must clear before wave closure):** carry the R-1 marker on
      `SpatialFightResult`, the row that actually crosses to star-lord. Follow the additive
      brownfield-safe pattern already used in that class by `total_displacement` /
      `mean_active_proxy_count`. Then execute the round-trip through `SpatialFightEngine.run()` —
      not a hand-constructed dataclass — and correct `MIGRATION.md` §1 and §5 to name the carrier
      star-lord writes. Re-submit the round-trip evidence only; the rest stands.
- [ ] **gamora (WARN):** correct math note §7 — the default is `LIVENESS_GATE_VERSION`, not `0`, and
      the marker is `int`, not boolean-valued (DOC-1).
- [ ] **gamora (WARN):** extend the T-G forward guard to assert the second half of the §1 corpus
      claim — zero `execute_threshold_fraction` — or add a sibling guard. Today only the
      `n_damage >= 2` half fails loudly (self-flag #2).
- [ ] **gamora (WARN):** state the full frame's **family coverage** (`burn` + `chill` only) in
      `AGENT_STATE.md` and the wave-closeout, so "0.0% exact" is not read downstream as
      frame-measured across all ruled families (self-flag #6, flip side).
- [ ] **gamora (INFO):** add AUDIT-1 to the §6 register (D2/D3 `continue` suppresses a second
      `on_kill` and the `last_kill_element` re-stamp on a corpse).
- [ ] **gamora (INFO):** record M1's *actual* soundness argument (AUDIT-3) — scratch HP is only
      re-seeded on a hit and hits skip dead targets — rather than the §2.2 resolver-internal argument,
      which does not transfer to the spatial seam.
- [ ] **gamora (INFO):** cross-reference N-2 at the stun pre-roll site (AUDIT-2/#5); note that M1's
      entry gate now precedes the `assert _identity is not None`.
- [ ] **gamora (INFO):** label or drop the duplicate Q-1 row in `MIGRATION.md` §6 (DOC-2); correct
      "13 hosts" → 11 in the pending doc if it is retained.
- [ ] **knight-rider:** **do not confirm wave closure** until the R-1 carrier defect is cleared.
      L0-CLOSE, KEY-NUM and the G-3 calibration stay held. When it clears, re-verification is the
      round-trip only — this is a short loop, not a re-run of the wave.
- [ ] **knight-rider:** carry the `is_on_death_payload` call-site obligation and rocket's
      `targets_corpse` write side into the Wave-1 dispatch, not only into MIGRATION prose.
- [ ] **Matt (ESCALATION per ADR-002):** if you judge the R-1 carrier defect to be a follow-on
      rather than a blocker — i.e. close Wave 0 now and land the marker on `SpatialFightResult` as
      the first item of Wave 1 — **that is your call to make and I will not contest it.** My reason
      for blocking is that Clause 5b and the round-trip were pre-registered acceptance criteria and
      the program's downstream analyses depend on the marker being readable where they read. The
      gate mechanism itself is sound and would not be the reason for the delay.

---

## References

**Reviewed (engine, `~/Games/reincarnated-engine`):**
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/liveness_gate.py`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/math/g5-wave0-universal-liveness-gate-2026-07-26.md` (§1, §2.2, §2.3, §3.2, §3.4, §6, §7, §9)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/damage_resolver.py` (gates A1/S1/D1/D2/D3; draw sites 948, 1056, 1066, 1124, 1237, 1338, 1663)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py` (M1 `_wave_c_apply_mark`; `SpatialFightResult` construction)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/spatial_telemetry.py` (`SpatialFightResult`, line 191 — **the BLOCK's evidence**)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/fight_result.py` (line 121 — marker as landed)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/balance_loop.py` (line 2239, `_spatial_stub_batch`)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/export/schemas.py` (every export builder sourced from `SpatialFightResult`)
- `/Users/admin/Games/reincarnated-engine/tests/test_g5_wave0_liveness_gate.py` (42 tests; `TestForwardOnlyMarker`, `TestCorpusForwardGuard`)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/scripts/g4_corpus_multidamage_enum_2026_07_26.py`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/scripts/g4_liveness_gate_coverage_2026_07_26.py`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/scripts/g4_liveness_gate_ablation_2026_07_26.py`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` (2026-07-26 entry)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md` (SESSION 74)

**Reviewed (collaboration):**
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/qa/pending/2026-07-26-gamora-g5-wave0-liveness-gate.md`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/dispatches/2026-07-26-gamora-liveness-gate-wave0.md`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/qa/findings/2026-07-26-gate1-wave0-q1.md`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-07-25-g5-key-program-charter-draft.md` (§ WAVE-0 PRE-FIRE RULINGS, Q-1…Q-4)
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gamora/notes/2026-07-26-g5-wave0-liveness-ab.py`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gamora/notes/2026-07-26-g5-wave0-liveness-ab-{smoke,full,ablation}.json`

**Executed first-hand (Discipline #10/#11 — nothing in §4 was taken on report):**
`pytest tests/test_g5_wave0_liveness_gate.py`; the Clause-4 coverage script; the ablation driver; the
corpus enumeration script; `git diff --stat c18066a b9781f1`; RNG-draw-site enumeration across
`damage_resolver.py`; import-graph trace of `FightResult` vs `SpatialFightResult` across `src/`.
