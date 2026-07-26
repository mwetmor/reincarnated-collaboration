# QA PENDING — 2026-07-26 — gamora — G-5 WAVE 0: universal liveness gate (Gate 2, DEV-MODE)

**Submitted by:** gamora (simulation seam)
**Reviewer requested:** jack-ryan, **DEV-MODE Gate 2, BLOCK authority — NON-WAIVABLE**
**Closure confirmed by:** knight-rider (NOT self-cleared; Wave-1 G-3 calibration and both §3
conversion loops fire on that confirmation, not on my tag)
**Tag:** ~~`gamora/v-g4-liveness-gate-1` @ `b9781f1`~~ → **`gamora/v-g4-liveness-gate-2`** (remediated)
**Repo:** `reincarnated-engine`, branch `main`. **COMMIT-NEVER-PUSH** — no push performed.

> **STATUS: BLOCKED → REMEDIATED, AWAITING RE-VERIFICATION.**
> Gate-2 verdict `qa/findings/2026-07-26-gate2-g5-wave0-liveness-gate.md` — **BLOCK** on one named
> defect (**R1-CARRIER**), everything else PASS. Remediated at tag `gamora/v-g4-liveness-gate-2`.
> **I have NOT self-cleared the BLOCK.** jack-ryan re-verifies; per his own scoping,
> **re-verification is the round-trip only** — Clauses 1–5 and the ablation stand verified and
> were NOT re-run.
> **Jump to the [REMEDIATION](#remediation--gamorav-g4-liveness-gate-2) section at the bottom.**
> Everything above it is the ORIGINAL submission, preserved unedited except for one factual
> correction marked in place ("13 hosts" → 11), so the finding still reads against what it reviewed.

---

## What was built

The G-4(2) UNIVERSAL liveness gate: *dead defenders receive nothing; no counter ever counts a
corpse.* Matt-ruled 2026-07-25. This wave **fronts the entire G-5 key program** — L0-CLOSE, KEY-NUM
and the G-3 control-payload calibration all sit behind it.

**Dispatch:** `dispatches/2026-07-26-gamora-liveness-gate-wave0.md`
**Charter:** `gandalf/notes/2026-07-25-g5-key-program-charter-draft.md` §1 row 0, §2 Wave 0, §4 R-1
**Gate-1 (binding):** `qa/findings/2026-07-26-gate1-wave0-q1.md` — CONCUR-WITH-NOTES
**Math note (Discipline #1, landed BEFORE code):**
`reincarnated-engine/src/reincarnated/simulation/math/g5-wave0-universal-liveness-gate-2026-07-26.md`

---

## Commits in review (7, in order)

| Commit | Milestone |
|---|---|
| `ba7be49` | corpus enumeration harness — Gate-1 item (a), the HALT test |
| `ee0aa95` | math note (predicate, per-class draw map, semantic-shift register, verified line map) |
| `49881d9` | implementation — five gates + R-1 marker |
| `beedc47` | test suite (42) + ablation driver; **contains a fix to `49881d9` found by the suite** |
| `04cb903` | Clause-4 coverage enumeration |
| `567a2682`* | smoke gate (collaboration repo) |
| `c18066a` | MIGRATION.md cross-seam entry + executed round-trip check |
| `b9781f1` | full frame + AGENT_STATE SESSION 74 |

\* collaboration repo; the rest are engine repo.

---

## Clause-by-clause status (all self-reported — please verify first-hand per Discipline #11)

| Clause | Status | Evidence |
|---|---|---|
| **1** outcomes byte-identical | **PASS** | smoke 16/16; **full frame 64/64**; every metric delta exactly `0.0` |
| **2** `landed:` strictly decrease | **PASS** | full frame burn 5,043→**400**; chill 5,187→**426** |
| **3** corpse share → **0.0% EXACT** | **PASS** | full frame burn **92.07%→0.0%**, chill **91.79%→0.0%**; total corpse landings **9,404 → 0** |
| **4** coverage, no bypass | **PASS** | 31 application call sites / 4 seam files / **11** hosts *(I wrote 13; the script prints 11 — transcription error, corrected)*, **all classified**; mechanical re-running check, not a pasted grep |
| **5** exemptions unit-tested | **PASS** | 42 tests; negative test per exemption path; Q-4 self-target explicit |
| **5b** forward-only marker | **PASS** | `FightResult.liveness_gate_version` == 1 on post-gate results |
| ablation discrimination | **PASS** | baseline 42/42, ablated 18/42, **24 flipped**, 0 register violations |
| round-trip | **PASS** | 4/4 rows **executed**, published in `MIGRATION.md` §5 |
| Q-1 roll-then-discard | **PASS** | attempt counts IDENTICAL across arms (burn 14,949/14,949; chill 14,840/14,840) |

---

## The five Gate-1 binding items — where each one landed

| Item | Landed |
|---|---|
| (a) corpus enumeration; non-zero ⇒ HALT | math note §1. **0 of 5,021 skills** carry ≥2 damage effects; **0** carry `execute_threshold_fraction`. **NO HALT.** |
| (b) discard point per class, per generator | math note §3.2 — four draws across two generators, conditional crit included |
| (c) zero-draw classes named moot | math note §3.4 — marks, buff/shield/HoT appends, DoT ticks, both aura paths |
| (d) predicate re-read per effect application | math note §2.3 — the Clause-3 no-op trap, stated so it cannot be re-introduced |
| (e) semantic-shift register | math note §6 — 4 shifts + 2 NAMED-NOT-GATED (reflect N-1; the pre-roll stun convention N-2) |

---

## Things I want looked at hardest (self-flagged; do not take my word for these)

1. **A defect the suite caught in my own gate — verify the fix, not the story.** T-6b failed on
   first run: the pre-existing `continue` lives INSIDE the not-shatter branch, so ANDing my gate
   into that condition made a *gated* execute fall through and consume a dodge draw the ungated arm
   never consumed. That is the Clause-1 stream shift Q-1 exists to prevent, introduced by me while
   implementing the ruling. Fixed by nesting the gate with the `continue` outside it. **Worth
   checking whether any of the other four gates has the same class of ordering error** — I found
   this one because a test existed; I cannot prove I wrote a test for every such case.

2. **The damage-class gate (D2/D3) is provably dead code today.** It rests entirely on the corpus
   count being 0. It is present for universality and Clause 4. If you judge that shipping a gate
   which cannot fire is the wrong call — or that the forward guard T-G is insufficient protection
   when generation starts emitting `execute_threshold_fraction` — that is a legitimate finding.

3. **Exemption (a) is mechanism-only.** The engine has no live on-death payload family; the
   exemption is unit-tested against synthetics. Q-4's self-target ruling is honoured by
   construction (the predicate never inspects who the attacker is). Whether an untestable-in-
   production exemption should count as Clause-5 satisfied is your call, not mine.

4. **`_apply_wavec_th_reflect` still feeds the attacker from a corpse hit.** NAMED, not gated,
   per Q-2. If you read G-4's "no procs" as reaching this, it is a finding — I read Q-2's
   defender-side-only ruling as governing, and routed the trigger-semantics question to W1/B1.

5. **Two opposite ordering conventions now coexist in `_try_apply_ailment`** — the stun immunity
   drop is PRE-roll, my gate is POST-roll. Deliberate, reasoned in math note §6 (N-2). If you
   think the codebase should not carry both, that is a design finding worth raising.

6. **Clause 2's verdict deliberately excludes unexercised counters.** A counter at zero in both
   arms votes for nothing. Verify I have not quietly counted one.

---

## What was NOT done (dispatch non-goals, all respected)

No telemetry backfill (pre-gate counters stay poisoned by ruling). No registry edit — `targets_corpse`
READ side only; write side owed to rocket, routed to Wave 1. No attacker-side gating. No Wave-1
resolver primitives (B1/B4/B7/B9). No G-3 control-payload work. No kill-resolution reordering. No
`M_min=0.06` scope. No re-litigation of `is_control != hard`. **No push.**

---

## Owed to others (recorded in `MIGRATION.md`)

- **rocket:** `targets_corpse` registry schema + emission path (write side).
- **star-lord:** decide whether to persist `liveness_gate_version` as a telemetry column
  (recommended `INTEGER DEFAULT 0` so existing rows read pre-gate with no data migration).
  **Consumer trap flagged in MIGRATION §5:** post-gate, `landed_on_corpse:*` keys do not appear at
  all — absent because the event never happens, not because instrumentation was dropped. Read with
  `.get(key, 0)` or the wave's headline result inverts.
- **W1/B1:** does a hit on a corpse count as a qualifying trigger event for attacker procs?

---

## Artifacts

- Math note: `reincarnated-engine/src/reincarnated/simulation/math/g5-wave0-universal-liveness-gate-2026-07-26.md`
- Gate module: `reincarnated-engine/src/reincarnated/simulation/liveness_gate.py`
- Tests: `reincarnated-engine/tests/test_g5_wave0_liveness_gate.py`
- Harnesses: `reincarnated-engine/src/reincarnated/simulation/scripts/g4_{corpus_multidamage_enum,liveness_gate_coverage,liveness_gate_ablation}_2026_07_26.py`
- A/B driver: `agentic_orchestration/gamora/notes/2026-07-26-g5-wave0-liveness-ab.py`
- Archived JSON: `agentic_orchestration/gamora/notes/2026-07-26-g5-wave0-liveness-ab-{smoke,full}.json`, `…-ablation.json`
- MIGRATION: `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` (2026-07-26 entry)
- AGENT_STATE: `reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md` SESSION 74

---

# REMEDIATION — `gamora/v-g4-liveness-gate-2`

**Appended 2026-07-26 by gamora** in response to
`qa/findings/2026-07-26-gate2-g5-wave0-liveness-gate.md` (jack-ryan, DEV-MODE Gate 2, **BLOCK**).
**Re-verification ask: the ROUND-TRIP ONLY**, per §6 of the finding — *"Clauses 1, 2, 3, 4, 5 and
the ablation stand verified and do not require re-running after remediation."* I took that scoping
literally and did not re-run them. **BLOCK not self-cleared.**

## The defect, stated as I now understand it

I put the R-1 marker on `FightResult`. Nothing in `export/`, `telemetry/` or `output/` references
`FightResult`; the cross-seam row is `SpatialFightResult`, an **independent dataclass, not a
subclass**, so the field did not inherit. MIGRATION therefore told star-lord to persist a column
with **no producer on the row he writes**.

**The part worth more than the fix:** my own round-trip evidence hid it. I reported §5 PASS off a
`FightResult` constructed *inside a unit test*. That is a struct-shape assertion — and a shape
assertion on the wrong object **passes forever** while the contract is unimplementable. The failure
mode is a green test, not a missing one, and the tell is that the test never touches the code that
emits the row. When a clause says *production-path fixture*, a hand-built dataclass does not
discharge it. That lesson is recorded in `AGENT_STATE.md` SESSION 75, not just here.

## Per finding item

| Finding item | Severity | What changed | Where |
|---|---|---|---|
| **DEFECT R1-CARRIER** (a) — marker on the wrong carrier | **BLOCK** | `liveness_gate_version: int = LIVENESS_GATE_VERSION` added to `SpatialFightResult`. Additive, `validate()`-exempt — the brownfield pattern you named (`total_displacement` / `mean_active_proxy_count`). **Producer is the dataclass default, not a construction-site stamp**, at the identical discipline used for `FightResult`; `spatial_engine.py`'s construction site deliberately does NOT name the field. Both carriers default to the ONE constant in `liveness_gate.py`, so agreement is structural. `FightResult` keeps its copy (your call to me; I took "no harm in both"). | `spatial_telemetry.py:477`; `fight_result.py:134` comment corrected to say plainly it is NOT the cross-seam carrier |
| **DEFECT R1-CARRIER** (b) — round-trip not satisfied as written | **BLOCK** | Production-path fixture: `_production_spatial_fight()` drives a REAL `SpatialFightEngine.run()` and reads the emitted row. Rig **pinned first** (Discipline #11) — 40/40 kills, `killing_element="fire"`, resolver-backed path — because a fight in which nothing dies is a fight in which the gate could not fire and the assertion would be vacuous. Executed rows re-published in MIGRATION §5. | `tests/…::TestForwardOnlyMarkerProductionPath` (T-M/b); driver `gamora/notes/2026-07-26-g5-wave0-r1-carrier-roundtrip.py` |
| **DEFECT R1-CARRIER** (c) — MIGRATION names the wrong field | **BLOCK** | §1 retitled to `SpatialFightResult`, both carriers tabulated, which-one-crosses stated, MUST-AGREE stated, producer stated precisely. The correction is **called out**, not silently swapped — anyone who read v1 needs to know it changed. §5 re-executed. | `simulation/MIGRATION.md` §1, §5 |
| **T-G half-guard** (finding §3 #2) | WARN | §1 makes TWO claims; I guarded one. **T-G/b** added — zero `execute_threshold_fraction` over the same corpus walk, its own named-cause message. This is the half the D1 premise **and semantic shift #4** rest on, so that premise had no forward alarm at all. Walk factored into `_walk_corpus_skills()` so the halves cannot drift to different corpora. | `tests/…::TestCorpusForwardGuard`; math note §1 |
| **DOC-1** — math note §7 says default 0 / "boolean-valued" | WARN | §7 rewritten with the error called out at the top: a consumer implementing "default 0, stamped on the post-gate path" builds **per-site stamping**, which is the design that was rejected. New **§7.1** (the default IS the constant; no site may stamp it — a *testable* invariant) and **§7.2** (two carriers, which crosses, why both, must-agree). | math note §7 / §7.1 / §7.2 |
| **Frame width** (finding §3, flip side of #6) | WARN | **NOT re-run** — out of re-verification scope. **RECORDED** as a limitation in three places so it cannot be mistaken for coverage: the frame exercised `burn` + `chill` ONLY; freeze/stun/slow/root/silence/sunder/marks/damage/procs are not exercised at all; "0.0% EXACT" is a measurement for the measured class and an **argument** (shared predicate + Clause-4 enumeration + registry-wide unit test) for the rest. Whoever cites the headline inherits the paragraph. | math note **§8.1** (new); MIGRATION §6; `AGENT_STATE.md` SESSION 74 results table + SESSION 75 |
| **AUDIT-1** — suppressed second `on_kill` | INFO | **Semantic shift #5** added to the register, and to the D2/D3 gate comments. Written from the consumer's side because `last_kill_element` is what `SpatialFightResult.killing_element` reads — ungated, a corpse hit could overwrite the element that actually landed the kill. | math note §6; MIGRATION §4; `damage_resolver.py` D2 + D3 |
| **AUDIT-3** — M1's recorded argument is the wrong one | INFO | New **§2.2.1**. Your argument recorded as the real one: scratch HP is re-seeded **only on a hit**, hits skip dead targets, so a corpse's scratch HP retains its last ≤ 0 value. Also named the fragility that creates — **any future change to scratch-HP re-seed lifetime breaks M1 silently**; T-5 is the catcher. | math note §2.2.1 |
| **AUDIT-2** — M1's gate precedes the assert | INFO | **N-3** added: a corpse-mark with a mis-wired identity now returns silently. Accepted and stated, **not** fixed, with the trade written down so it is re-decidable (M1 is zero-draw; entry is the cheapest correct placement; the assert still fires on every reachable path). | math note §6 |
| **#5 / AUDIT-2** — N-2 cross-reference at the stun site | INFO | Cross-reference added **at the stun pre-roll site itself**: DO NOT GENERALISE THIS PLACEMENT, byte-neutrality here comes from rarity, there from consuming the draw anyway, full argument at N-2. | `damage_resolver.py` `_try_apply_ailment` |
| **DOC-2** — duplicate Q-1 row | INFO | Dropped, **with its reason left in place**: those were the SMOKE counts, sitting below a table that already reports Q-1, so they read as a third measurement contradicting 14,949 / 14,840. | MIGRATION §6 |
| **"13 hosts"** | INFO | Corrected to **11** everywhere it appeared: this stub (marked in place), `AGENT_STATE.md` SESSION 74 (marked in place), MIGRATION §6. The script is authoritative; re-ran it to confirm. | 3 files |

**Also added, not asked for — `T-M/d`.** §7.1 says no construction site may stamp the field
explicitly. That is an invariant, so it is tested, not asked for: `T-M/d` greps
`src/reincarnated/` and fails naming file:line. **Proven non-vacuous** — injecting
`liveness_gate_version=1` at `spatial_engine.py`'s construction site trips it
(`spatial_engine.py:5377`). Injection reverted.

## Round-trip re-run — EXECUTED ROWS

Driver: `agentic_orchestration/gamora/notes/2026-07-26-g5-wave0-r1-carrier-roundtrip.py`
(deterministic — re-run it to reproduce). Mirrored as tests in
`TestForwardOnlyMarkerProductionPath`. Also published in `MIGRATION.md` §5.

**Rig, pinned FIRST:** carrier returned by `SpatialFightEngine.run()` = `SpatialFightResult`;
`winner=player`, `kills=40/40`, `elapsed=98.60s`, `killing_element="fire"` (resolver-backed
damage path taken); seed `91126`, `SCENARIO_OPEN_ARENA`.

| # | Check | Result |
|---|---|---|
| 1 | Marker present on the `SpatialFightResult` **emitted by `run()`** | **PASS** — `value=1`, `type=int` (and not `bool`) |
| 2 | Survives `validate()` (P7 writer gate does not reject the additive field) | **PASS** |
| 3 | Survives `dataclasses.asdict()` serialization | **PASS** — `liveness_gate_version=1` |
| 4 | Accepted by star-lord's **concrete** `SqliteSpatialTelemetryWriter` | **PASS** — `writes_ok=1`, `writes_failed=0`, `rows_persisted=1`; column not yet in schema (expected — that is his owed item), and the additive field does not break the existing positional writer |
| 5 | Archived pre-gate dict without the key reads `0` via `.get(key, 0)` | **PASS** |
| 6 | The two carriers **agree** | **PASS** — `{FightResult: 1, SpatialFightResult: 1}`; `issubclass=False` |

**ROUND-TRIP VERDICT: PASS — 6/6 executed rows against a production-path row.**

## Test counts

| Suite | Result |
|---|---|
| `tests/test_g5_wave0_liveness_gate.py` | **49 passed** (42 → 49: T-G split a/b, T-M split a/b/c/d) |
| + sibling ailment suites (`test_ailment_layer_gamora_slice`, `…_rocket_slice`, `test_ailment_registry`) | **239 passed** total |
| Spatial/telemetry regression (`round_trip_spatial_telemetry`, `test_w095_telemetry`, `test_f8_hard_cc_consumer`, `test_spatial_gauntlet_scenarios`, `test_wd_spatial_bc_measurement`) | **201 passed** |
| Round-trip driver | **6/6 PASS** |

`ABLATION_REGISTER` updated 6/7 → 8/9 rows. **The ablation ARM was NOT re-run** — out of scope per
your §6 — and the register docstring now says so, rather than letting the pre-split 42/18/24
numbers read as describing the new suite.

## Commits (5, in order — engine repo, `main`, COMMIT-NEVER-PUSH)

| Commit | Milestone |
|---|---|
| `da47c12` | **math note FIRST** (Discipline #1) — §7/§7.1/§7.2 carrier rewrite, §1 T-G both halves, §2.2.1 M1's real argument, §6 shift #5 + N-3, §8.1 frame coverage |
| `92e6f51` | code — `SpatialFightResult.liveness_gate_version`; `fight_result.py` comment corrected; shift #5 at the D2/D3 gates; N-2 cross-reference at the stun site |
| `9247bd5` | tests — production-path round-trip (T-M/b), carrier agreement (T-M/c), stamping guard (T-M/d), corpus guard T-G/b |
| `ed297ac` | `MIGRATION.md` — §1 carrier corrected, §4 shift #5, §5 re-executed, §6 frame coverage + host count + DOC-2 |
| `1a6e25f` | `AGENT_STATE.md` SESSION 75 + math note §9.1 carrier line map |

**Tag:** `gamora/v-g4-liveness-gate-2` @ `1a6e25f`.

## Re-verification ask

**Round-trip only**, per your §6. Concretely, the four things I would check if I were you:

1. The marker is on **`SpatialFightResult`** and the emitting construction site does **not** stamp
   it — and `T-M/d` actually trips if it does (I injected one; you may prefer to inject your own).
2. The round-trip rows above came from `SpatialFightEngine.run()` and **not** from a hand-built
   dataclass. The rig-pinning test is the one that decides whether the evidence is vacuous.
3. `MIGRATION.md` §1 now names a field star-lord can actually implement against, and §5's PASS is
   backed by the driver rather than by a struct assertion.
4. Whether my framing of the **frame-coverage limitation** is strong enough. I recorded it in three
   places and did not widen the frame. If you judge that "0.0% EXACT" still travels too easily
   without its qualifier, say so — that is a finding I would rather take now than after KEY-NUM
   cites it.

**Not self-cleared.** knight-rider confirms closure; L0-CLOSE, KEY-NUM and the G-3 calibration
fire on that confirmation, not on my tag.
