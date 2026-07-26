# Finding — 2026-07-26 — Gate-2 RE-VERIFICATION — G-5 Wave 0: universal liveness gate

**Reviewer:** jack-ryan (DEV-MODE, Gate 2 — BLOCK authority retained)
**Severity:** **PASS-WITH-FINDINGS** — the BLOCK is **CLEARED**. Two WARNs and two INFOs recorded,
none of which holds the wave.
**Target:** `gamora/v-g4-liveness-gate-2` @ `1a6e25f` (annotated tag; verified `^{commit}` ==
`1a6e25f` == `main` HEAD, `git diff tag..HEAD` empty). Remediation commits `da47c12`, `92e6f51`,
`9247bd5`, `ed297ac`, `1a6e25f`.
**Prior finding:** `qa/findings/2026-07-26-gate2-g5-wave0-liveness-gate.md` — **BLOCK**, DEFECT
R1-CARRIER, on `gamora/v-g4-liveness-gate-1` @ `b9781f1`.
**Developer:** gamora
**Principles applied:** REVIEW_PROCESS #3/#6 (cross-seam impact + round-trip), #4 (ruling as truth),
#5 (severity matters); Disciplines #1, #2, #10, #11, #12; ADR-004 (MIGRATION as cross-seam contract),
ADR-002 (escalation).

---

## Verdict

**DEFECT R1-CARRIER is CLEARED. Wave 0 closes.**

The remediation is correct, it is complete against every item I raised, and the round-trip is now
real evidence rather than a struct-shape assertion. I re-ran it and every number reproduced to the
digit. gamora did not self-clear, took my scoping literally, and did not re-run what I said not to
re-run — which is the behavior the gate is supposed to produce.

**Scope note, stated explicitly because I pre-scoped this review to the round-trip only.** I widened
it, deliberately and narrowly, on exactly one axis: gandalf's named concern about
**default-as-producer**. That concern deserved a first-hand answer and it got one (§3). Widening it
surfaced one real, demonstrated defect — but the defect's trigger is in **Wave 1**, not Wave 0, so
it is a WARN carried into star-lord's consumer dispatch, not a second BLOCK. I did not re-run
Clauses 1–5 or the ablation; they stand verified from the first review.

---

## 1. Round-trip re-verification — EXECUTED, all six rows reproduce

I ran gamora's driver first-hand rather than reading the reported table.

```
[RIG] carrier : SpatialFightResult (SpatialFightEngine.run() return)
[RIG] fight   : winner=player  kills=40/40  elapsed=98.60s  killing_element=fire
ROUND-TRIP: PASS — 6/6 rows executed against a production-path row (seed=91126)
```

| # | Check | gamora claimed | I measured | Delta |
|---|---|---|---|---|
| rig | production carrier, kills reached, resolver path taken | `SpatialFightResult`, 40/40, 98.60s, `fire` | identical | **0** |
| 1 | marker on the row `run()` emitted | PASS, `value=1`, `int` not `bool` | PASS, identical | **0** |
| 2 | survives `validate()` (P7 writer gate) | PASS | PASS | **0** |
| 3 | survives `dataclasses.asdict()` | PASS, `=1` | PASS, `=1` | **0** |
| 4 | star-lord's concrete `SqliteSpatialTelemetryWriter` | `writes_ok=1`, `writes_failed=0`, `persisted=1` | identical | **0** |
| 5 | archived dict without the key reads `0` via `.get(k,0)` | PASS | PASS | **0** |
| 6 | two carriers agree; `issubclass=False` | `{FightResult:1, SpatialFightResult:1}` | identical | **0** |

**This is now a production-path round-trip and not a struct assertion.** The rig is pinned before
the marker is read (Discipline #11), and the pin is load-bearing: 40/40 kills with
`killing_element="fire"` proves the resolver-backed damage path was taken and defenders actually
died mid-fight, so the gate could fire. A fight in which nothing dies would have made the marker
assertion vacuous. That is the correct construction and gamora built it unprompted.

**Row 4 is the one that matters for ADR-004** and it now discharges what the earlier version could
not: the field reaches star-lord's *concrete* writer, the additive column does not break his
existing positional INSERT, and the schema column is confirmed **absent** — which is the correct
state, because adding it is his owed item, not gamora's.

### The three checks I made on the remediation itself

1. **The marker is on the right carrier and the emitting site does not stamp it.** Verified in code:
   `spatial_telemetry.py:477` carries `liveness_gate_version: int = LIVENESS_GATE_VERSION`;
   `spatial_engine.py:5355`'s construction site does not name the field. A repo-wide grep finds the
   field at exactly two declaration sites and zero construction sites.
2. **T-M/d is non-vacuous — proven by my own injection, not gamora's.** I built a detached worktree
   at `1a6e25f`, inserted `liveness_gate_version=1` into the `SpatialFightResult(...)` construction
   at `spatial_engine.py:5356`, and ran the guard. It failed, naming the file and line:
   `R-1 STAMPING DISCIPLINE BROKEN: ... Offenders: simulation/spatial_gauntlet/spatial_engine.py:5356`.
   Injection reverted; the engine working tree was never touched.
3. **MIGRATION §1 now names a field star-lord can implement against.** Both carriers tabulated,
   which one crosses stated in bold, the producer stated precisely, and — correctly — the v1 error
   is **called out at the top of the section** rather than silently swapped. Anyone who read v1 is
   told it changed. §5's PASS is now backed by the driver.

---

## 2. Every other finding item — discharged

I checked each one rather than accepting the remediation table.

| Item | Sev | Status |
|---|---|---|
| **T-G half-guard** | WARN | **CLEARED.** T-G split a/b; both pass. The second half now asserts zero `execute_threshold_fraction` — the half the D1 premise and semantic shift #4 rest on. The corpus walk is factored into `_walk_corpus_skills()` so the two halves cannot drift to different corpora. That factoring was not asked for and is the right call. |
| **DOC-1** (math note §7 said default `0` / "boolean-valued") | WARN | **CLEARED.** §7 rewritten with the error called out in a blockquote at the top, plus new §7.1 (the default is the constant; no site may stamp it — stated as a *testable* invariant) and §7.2 (two carriers, which crosses, why both, must-agree). |
| **Frame coverage** (flip side of self-flag #6) | WARN | **CLEARED, and gamora's framing is strong enough** — that was its question 4 and the answer is yes. Math note §8.1, MIGRATION §6 and `AGENT_STATE.md` all carry it; §8.1 separates the three legs of the universality argument and closes with *"an argument, not a measurement… whoever cites it inherits this paragraph."* KEY-NUM and G-3 cannot now cite "0.0% EXACT" without meeting the qualifier. |
| **AUDIT-1** (suppressed second `on_kill`) | INFO | **CLEARED.** Semantic shift #5 in the §6 register and at both the D2 and D3 gate sites. Written from the consumer's side — `last_kill_element` feeds `SpatialFightResult.killing_element` and E3 attribution — which is a better statement of it than mine was. |
| **AUDIT-3** (M1's recorded argument was the wrong one) | INFO | **CLEARED.** New §2.2.1 records the real argument (scratch HP re-seeds only on a hit; hits skip dead targets) *and* names the fragility it creates: any future change to scratch-HP re-seed lifetime breaks M1 silently, with T-5 named as the catcher. |
| **AUDIT-2 / N-3** (M1's gate precedes the assert) | INFO | **CLEARED.** N-3 added. Accepted-and-stated rather than fixed, with the trade written down so it is re-decidable. Correct disposition. |
| **N-2 cross-reference at the stun site** | INFO | **CLEARED.** `damage_resolver.py::_try_apply_ailment` now carries `DO NOT GENERALISE THIS PLACEMENT` with the rarity-vs-consume-the-draw distinction inline. |
| **DOC-2** (duplicate Q-1 row) | INFO | **CLEARED.** Dropped with its reason left in place, so the removal is auditable. |
| **"13 hosts"** | INFO | **CLEARED, verified.** Corrected to **11** in all three files; the only surviving "13" is the correction-in-place note. I re-ran the coverage script: 31 sites / 4 seam files, GATED 10 / PRE-GUARDED-UPSTREAM 15 / NOT-AN-APPLICATION 4 / EXEMPT-ATTACKER-SIDE 1 / EXEMPT-SELF 1, **CLAUSE 4: PASS**. |
| **`T-M/d`, not asked for** | — | Added on gamora's own initiative and proven non-vacuous. Correct instinct — an invariant asserted in a math note that is not tested is a comment. See WARN-2 for its one scope problem. |

---

## 3. RULING — gandalf's default-as-producer concern

**The question, as gandalf put it:** a dataclass default cannot distinguish "the liveness gate ran on
this fight" from "a row of this type was constructed." If any construction path can produce a
`SpatialFightResult` whose fight did not pass through the gate, the default stamps a **false
attestation**, which is worse than the missing field I blocked on. `T-M/d` guards that no site
*overrides* the field — a different property.

**gandalf is right that the two properties are different, and right that false-positive is the worse
failure. He is wrong that this makes default-as-producer unsound for Clause 5b. Ruling: the default
SATISFIES Clause 5b on the emission path. The false-attestation path he predicts is REAL, I
demonstrated it, and it lives on the REHYDRATION path — which does not exist yet.**

### 3.1 Why the two propositions collapse on the emission path

Clause 5b asks for a forward-only marker declaring **which side of the gate a run sits on**. The
gate has no runtime toggle: no config flag, no feature switch, no seed dependence. It is compiled
in. Clause 4's enumeration — which I re-ran today, PASS — establishes that **no ailment-application
path in the seam bypasses the predicate**: 31 sites across 4 seam files, 10 GATED, 15
PRE-GUARDED-UPSTREAM, 4 NOT-AN-APPLICATION, 2 EXEMPT-and-tested. There is exactly one
`SpatialFightResult` construction in `src/` reachable from a real fight (`spatial_engine.py:5355`).

Therefore, for any row **emitted by a fight in this build**, *"the build has the gate"* and *"this
fight's counters were gate-filtered"* are the same proposition. The distinction gandalf draws is
real in general; it collapses here, and it collapses for a reason that was independently established
by Clause 4 rather than assumed.

### 3.2 Why the default is the *stronger* producer for that job

The two designs fail in **opposite** directions, and the asymmetry runs gamora's way, not gandalf's:

- **Explicit stamp + default `0`** fails toward **FALSE NEGATIVE**. A new emission site that forgets
  the stamp emits a genuinely gate-clean row marked pre-gate. Under R-1's own semantics — absence is
  meaningful, pre-gate counters stay POISONED — the analysis then **silently discards good data**,
  with nothing to detect it.
- **Default = constant** fails toward **FALSE POSITIVE**, but only at construction sites that are
  not fights.

gandalf's severity ordering (false attestation > missing field) is correct, and it is precisely why
the default choice has to be *paid for* by closing the false-positive side. It does not by itself
condemn the default.

### 3.3 Where the false-attestation path DOES exist — demonstrated, not hypothesised

I went looking for it and found it. `SpatialFightResult(**row)` is this repo's **established
rehydration idiom**, used at three sites today — including one inside **star-lord's own seam**
(`src/reincarnated/telemetry/e3_attribution_spine_v221_smoke_2026_07_11.py:78`). I splatted an
archived pre-2026-07-26 row, which legitimately has **no marker key**, through it:

```
archived PRE-GATE row rehydrated via SpatialFightResult(**row):
   liveness_gate_version -> 1   (expected pre-gate reading: 0)
   asdict() now serializes  -> 1
```

A correct *"absent = pre-gate"* signal is converted into a **false gate-clean attestation**, and
`asdict()` then re-serializes the lie. Math note §7.1 says *"a result produced by this binary always
went through the gate."* The word carrying the argument is **produced**. The default applies equally
to rows merely **constructed** by this binary from pre-gate data, and §7.1 does not distinguish the
two. That is the gap, stated exactly.

**Why this is not a BLOCK.** No consumer reads the marker: I grepped `export/`, `telemetry/` and
`output/` and found zero references, and the round-trip confirms the column is **not in star-lord's
schema**. No analysis can be corrupted today. The three rehydration sites are two test fixtures and
one standalone temp-DB smoke harness that is never imported. The hazard is **latent, and its trigger
is the read path star-lord builds in Wave 1** — which is where the fix belongs and where it is
cheap. Blocking Wave 0 for a defect that fires in Wave 1, after gamora cleared the named defect
exactly, would be a misuse of the gate.

---

## 4. WARNs

### WARN-1 (R1-REHYDRATE) — §7.1's invariant must be scoped to EMISSION

**Description.** `liveness_gate_version` defaults to the constant on both carriers. The default is
correct for rows the engine *emits* and incorrect for rows the engine *rehydrates* from pre-gate
storage, where it silently overwrites a meaningful absence with a false `1` (§3.3, demonstrated).

**Prescription.** Math note §7.1 and MIGRATION §1 should state the invariant as scoped —
*the default is the producer for **emitted** rows; a row reconstructed from storage must carry the
persisted value, and a persisted value that is absent means `0`* — and MIGRATION §1 should carry a
consumer-facing line telling star-lord not to round-trip archived rows through the dataclass without
supplying the column. This is the paragraph that stops R-1's central premise ("absence is meaningful,
and there is no backfill") from being destroyed by the very field that implements it.

### WARN-2 (T-M/d SCOPE) — a gamora-seam guard is enforced inside star-lord's seam

**Description.** `T-M/d` walks `src/reincarnated/**` and fails on any explicit
`liveness_gate_version=`. That tree includes `telemetry/`, `export/` and `output/` — star-lord's
seam. The correct Wave-1 read-path implementation (carry the persisted column value onto a
rehydrated row) is, syntactically, exactly the explicit stamp T-M/d forbids. star-lord doing the
right thing will fail a test he does not own, with an assertion message authored in another seam.

**Prescription.** Before star-lord's consumer dispatch fires, either scope the walk to gamora's seam
or add a named, documented exemption for read/rehydrate sites. The invariant T-M/d is protecting is
*no construction site may stamp an emitted row*; that is not the same statement as *no line in the
package may name the field*.

---

## 5. INFO

**INFO-1 — the ablation plugin now under-ablates the new carrier.**
`g4_liveness_gate_ablation_2026_07_26.py`'s generated plugin rebinds `LG.LIVENESS_GATE_VERSION = 0`
and re-binds **`FightResult`**'s dataclass field default and `__init__.__defaults__` to `0`. It does
**not** do either for `SpatialFightResult`, whose default was likewise bound at class-creation time.
With the gate ablated, the cross-seam carrier would still stamp `1`. The declared per-test ablation
expectations still hold (the test module binds the constant at import, after the plugin has zeroed
it), so nothing is currently wrong — but gamora correctly did **not** re-run the ablation arm at
`-2`, and the next re-run will be asymmetric with the two-carrier design unless the plugin is
extended. Cheap to fix at the moment the register is next re-measured.

**INFO-2 — `liveness_gate.py:34` is stale on the carrier question.** The constant's own header
comment still reads *"Stamped onto `FightResult.liveness_gate_version` on every post-gate run."*
That is the sentence DOC-1 was about, in the one file a reader is most likely to open first. Same
class as DOC-1; one line.

---

## 6. Claimed vs. re-measured

Nothing below was taken on report. Suites were re-run in the engine working tree at `1a6e25f`.

| Claim | Re-measured | Delta |
|---|---|---|
| liveness suite 42 → **49** | `49 passed in 1.12s`, 0 skips | **0** |
| ailment suites **239 passed** | `239 passed in 2.21s` | **0** |
| spatial/telemetry regression **201 passed** | `201 passed in 29.77s` | **0** |
| round-trip **6/6 PASS**, seed 91126, 40/40 kills, 98.60s | identical to the digit | **0** |
| Clause 4: 31 sites / 4 files / **11** hosts, PASS | script re-run: identical, verdict PASS | **0** |
| T-M/d non-vacuous | **confirmed by my own injection**, not gamora's | **0** |
| tag `gamora/v-g4-liveness-gate-2` @ `1a6e25f` | annotated tag, `^{commit}` matches, `diff tag..HEAD` empty | **0** |
| COMMIT-NEVER-PUSH | 12 commits unpushed; no `g4-liveness` tag on `origin` | **honored** |

---

## 7. The "all pre-existing" whole-repo failure claim

_(filled below)_

---

## Action

- [x] **gamora — DEFECT R1-CARRIER: CLEARED.** Re-verified first-hand.
- [ ] **gamora (WARN-1):** scope §7.1's invariant to emission and add the rehydration clause to
      MIGRATION §1 (§4 above). Documentation-only; **I approve this directly under ADR-002** — it
      does not need to reopen the wave.
- [ ] **gamora (WARN-2):** before star-lord's Wave-1 consumer dispatch fires, scope `T-M/d`'s walk
      to gamora's seam or add a named read/rehydrate exemption.
- [ ] **gamora (INFO-1):** extend the ablation plugin to rebind `SpatialFightResult`'s default when
      the register is next re-measured.
- [ ] **gamora (INFO-2):** correct the stale carrier sentence at `liveness_gate.py:34`.
- [ ] **knight-rider:** **Wave 0 may close.** L0-CLOSE, KEY-NUM and the G-3 calibration are
      released. Carry WARN-1 and WARN-2 into star-lord's Wave-1 consumer dispatch as binding
      pre-conditions — they are cheap now and expensive after he has built the read path.
- [ ] **knight-rider:** the Wave-1 dispatch still owes the `is_on_death_payload` call-site
      obligation and rocket's `targets_corpse` write side, per the first finding.
- [ ] **Matt:** no escalation required. Recorded for visibility only: I widened re-verification
      beyond my own pre-scoping to rule on gandalf's concern, and the widening found one real
      latent defect (§3.3). If you would rather WARN-1 be closed before Wave 0 formally closes
      rather than as a Wave-1 pre-condition, that is your call; I judge it not worth the hold.

---

## References

**Reviewed (engine, `~/Games/reincarnated-engine` @ `1a6e25f`):**
- `src/reincarnated/simulation/spatial_gauntlet/spatial_telemetry.py:477` — the corrected carrier
- `src/reincarnated/simulation/fight_result.py:134` — 1D carrier + corrected comment
- `src/reincarnated/simulation/liveness_gate.py:43` — `LIVENESS_GATE_VERSION` (and `:34`, INFO-2)
- `src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py:5355` — the emitting site
- `src/reincarnated/simulation/damage_resolver.py` — shift #5 at D2/D3; N-2 cross-ref at the stun site
- `src/reincarnated/simulation/MIGRATION.md` §1 / §4 / §5 / §6
- `src/reincarnated/simulation/math/g5-wave0-universal-liveness-gate-2026-07-26.md` §2.2.1, §6, §7,
  §7.1, §7.2, §8.1, §9.1
- `src/reincarnated/simulation/AGENT_STATE.md` SESSION 75
- `src/reincarnated/simulation/scripts/g4_liveness_gate_{coverage,ablation}_2026_07_26.py`
- `src/reincarnated/telemetry/e3_attribution_spine_v221_smoke_2026_07_11.py:78` — a rehydration site
- `tests/test_g5_wave0_liveness_gate.py` — T-G/a,b; T-M/a,b,c,d
- `tests/round_trip_spatial_telemetry.py:93`, `tests/test_aware_fighter_policy_seam.py:281`,
  `tests/test_wd_spatial_bc_measurement.py:170` — the other rehydration / hand-build sites

**Reviewed (collaboration):**
- `agentic_orchestration/qa/findings/2026-07-26-gate2-g5-wave0-liveness-gate.md` (the governing finding)
- `agentic_orchestration/qa/pending/2026-07-26-gamora-g5-wave0-liveness-gate.md` § REMEDIATION
- `agentic_orchestration/gamora/notes/2026-07-26-g5-wave0-r1-carrier-roundtrip.py`

**Executed first-hand:** the round-trip driver; `pytest tests/test_g5_wave0_liveness_gate.py`; the
three ailment suites; the five spatial/telemetry suites; the Clause-4 coverage script; a T-M/d
injection in a detached `/tmp` worktree (reverted; the engine working tree was never modified); a
rehydration probe constructing `SpatialFightResult(**archived_pre_gate_row)`; whole-repo `pytest`
at `1a6e25f` and at baseline `b9781f1`; `git diff b9781f1 1a6e25f` reduced to its executable delta.
