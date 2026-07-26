# QA PENDING — 2026-07-26 — gamora — G-5 WAVE 0: universal liveness gate (Gate 2, DEV-MODE)

**Submitted by:** gamora (simulation seam)
**Reviewer requested:** jack-ryan, **DEV-MODE Gate 2, BLOCK authority — NON-WAIVABLE**
**Closure confirmed by:** knight-rider (NOT self-cleared; Wave-1 G-3 calibration and both §3
conversion loops fire on that confirmation, not on my tag)
**Tag:** `gamora/v-g4-liveness-gate-1` @ `b9781f1`
**Repo:** `reincarnated-engine`, branch `main`. **COMMIT-NEVER-PUSH** — no push performed.

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
| **4** coverage, no bypass | **PASS** | 31 application call sites / 4 seam files / 13 hosts, **all classified**; mechanical re-running check, not a pasted grep |
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
