# Finding — 2026-08-10 — factory-spine-v1 (Gate 2)

**Reviewer:** jack-ryan
**Severity:** BLOCK (agentic lane) · APPROVE (mechanical lane)
**Target:** `agentic_orchestration/factory/` @ 339c7216; landing note @ c8ce2e11
**Developer:** star-lord (builder, ruling D4)
**Build contract:** `agentic_orchestration/gandalf/notes/2026-08-10-factory-spine-spec.md` (Spec A)
**Gating:** Spec A § 11 acceptance item 5
**Principles applied:** REVIEW_PROCESS #2 (smoke-gate / evidence), #3 (cross-seam impact), #5 (severity matters)
**Disciplines cited:** 8 (schema validation at boundaries), 9 (assertions from spec sources), 11 (empirical inspection over assumption), 12 (semantic-shifting fixes need explicit framing)

---

## Verdict

**BLOCK on the first compiled agentic workflow.**
**APPROVE the mechanical lane to continue running unchanged.**

The split is deliberate and load-bearing. The mechanical lane is proven and I
reproduced every claim made for it. The agentic lane is the one Gate-2 exists to
authorize, and it is the one where the containment layer has a blind spot large
enough to lose 3.75 GB of unrecoverable artifacts while reporting PASS.

Two defects (F1, F2) share a single shape: **the containment mechanism degrades
to a silent no-op and the phase greens anyway.** That is the exact failure this
gate was asked to hunt — a path from a broken world to a green phase — and both
are currently *pinned as intended behavior by passing tests*, which is why 136
green did not surface them.

---

## What I verified independently (claims reproduced, not accepted)

Every acceptance claim in the landing note holds. I re-ran all of it.

| Claim | Result |
|---|---|
| 136 tests green | **REPRODUCED** — `136 passed in 1.63s` |
| Workflow runs end-to-end PASS, 3 phases / 14 verdicts | **REPRODUCED** — run `…T230754Z-85f4c8` |
| `determinism` reports EXACT across two laps | **REPRODUCED** — 14 verdicts identical |
| Zero stub gates; sole stub is the Codex adapter, declares itself and raises | **CONFIRMED** |
| Planted out-of-allowlist write ⇒ abort + quarantine + rollback + zero retries | **CONFIRMED, and I re-proved it live** (see F1 control) |
| Scope: meta-repo writes only, no engine-tree writes | **CONFIRMED** — zero files modified in `reincarnated-engine` or `reincarnated-godot` in the last 12 h; `.pytest_cache` there dates to 2026-05-06 (pre-existing), so `-p no:cacheprovider` did its job |

Four things I specifically tried to break and could not:

- **Falsification tests are real.** I read all nine registered gates' cases. Every
  one breaks the gate's *subject* — a deleted file, a zero-byte file, `{"a":1,,}`,
  an unclaimed measured path, a red prior report, exit 1, mutated bytes under a
  pin, a 1 s clip against `min_duration_s=60`. **None earns its red via a
  TypeError or a bad argument.** The `NOT_RUNNABLE`-on-bad-args cases exist but are
  filed as *separate* tests and none of them calls `_record()`, so they cannot
  satisfy registry coverage. That is the right construction.
- **Registry coverage fails safe.** `FALSIFIED` is populated by test execution, so
  partial runs under-report and the assertion reds. Wrong direction is impossible.
- **A phase with no gates cannot exist.** `workflow.py:170` rejects it at LOAD:
  *"an unadjudicated phase is a claim nobody checked."* This closes the most
  obvious no-adjudication path.
- **Default-fail holds under every control-flow branch.** I traced each
  `break`/`continue` in `runner.py::_run_phase`. There is no route to `PASS` that
  does not pass through `finish_with_envelope` under all-green gates.
  `run_gate` converts any exception to `NOT_RUNNABLE`; `is_green` is `status ==
  PASS` and nothing else; `test_not_runnable_is_red_everywhere_it_is_constructed`
  greps the tree for `!= FAIL` comparisons. That chain is sound.

**Discipline #9 — satisfied.** `fixtures/claude_stream_probe.jsonl` is a genuine
recorded frame (claude 2.1.119, real `session_id`, real counts 2/4/15628/9486,
`total_cost_usd` 0.0672). `test_usage.py` reads its assertions out of the file
rather than restating them. I found no test in the suite asserting against a value
the implementation itself chose. The O4 dollars handling — record the figure, stamp
`dollars_source="harness_reported_imputed"`, carry it to the DB column and the
report — is the correct resolution and it survives end-to-end.

**Both self-reported fixes hold.** My live control probe (F1 below) shows the
second fingerprint catching a gate-command write with `during="gate execution"`,
rolling it back, quarantining the bytes, and aborting. The gitignore-based
false-breach fix also works as designed. The problem is what "as designed" turned
out to mean.

---

## F1 — BLOCK — a write to any gitignored path escapes containment entirely

**File:** `agentic_orchestration/factory/permissions.py:129-146` (`fingerprint`)
**Pinned by:** `agentic_orchestration/factory/tests/test_permissions.py:220-223`

`fingerprint()` builds its entire world-model from `git status --porcelain`, which
by definition never reports ignored paths. Every gitignored path in every declared
repo — **including declared `read_only_trees`** — is therefore invisible to the
before/after diff, produces no `Change`, no `Breach`, no rollback, and no abort.

I proved this end-to-end with a real factory run, not a unit probe. A mechanical
phase with `writes: []` whose gate command writes into a gitignored directory:

```
-- phase 1/1: plant_ignored_write [mechanical]
   OK   artifacts_exist: PASS
   OK   command_succeeds: PASS -- `python3 -c "open('/tmp/jr_probe1/ignored_dir/escaped.txt','w')…"` exited 0
   OK   diff_matches_claims: PASS -- change-set (0 path(s)) is a subset of the 1 claimed
   OK   verdict_consistent: PASS -- envelope claims PASS and all 3 prior gate(s) are green
   phase plant_ignored_write -> PASS
run jr-breach-probe-ignored-…-9fc806 -> PASS
=== DID THE FILE SURVIVE? ===
OUT OF ALLOWLIST  <-- WRITE SURVIVED, RUN WENT GREEN
```

**Control** (identical workflow, one character of path difference, target visible
to git) — the machinery works exactly as advertised:

```
   PERMISSIONS BREACH during gate execution — aborting the run
     visible_escape.txt (created) — path is outside the phase's writes allowlist
     rollback: visible_escape.txt -> deleted
ABORTED: permissions breach during gate execution: 1 path(s) outside the allowlist
```

So containment is not broken. It is **scoped to git-visible paths and silently
absent everywhere else**, and nothing in the receipts says so.

**Why this blocks the agentic lane specifically.** The shipped workflow declares
`~/Games/reincarnated-engine` a read-only tree and the workflow file claims *"the
read-only claim is proved per phase, not asserted."* Inside that tree, the
gitignored — and therefore unfenced — region contains:

- `seasons/` — **3.3 GB** of generated season output (`.gitignore:17`)
- `src/reincarnated/telemetry/telemetry.db` — **450 MB** production telemetry DB,
  deliberately untracked per Matt ruling 2026-07-07 (`.gitignore:38`)
- `cache/`, `logs/`, `*.log`, `data/telemetry.db`

None of it is recoverable by `git checkout`, because git has never seen it. An
agentic phase holding Bash and Write can delete all of it and the run reports
PASS with a green read-only proof. For the *mechanical* lane the risk is low —
commands are author-chosen and reviewed. For the agentic lane it is the whole
point of the containment layer, and the layer is not there.

**Discipline #12.** The fix for the false-breach trap (§ 5 of the landing note)
was correct in intent — the factory's own gitignored `sessions/` writes must not
read as self-breaches — but it was applied as a *category* exemption when the
symptom was a *named-path* problem. That silently changed what the fingerprint
validates, from "all writes" to "git-visible writes," and the test at line 220
now encodes the reduced scope as the requirement. This is precisely the
semantic-shifting fix Discipline #12 asks to be framed explicitly; it was framed
as a cost/false-positive fix instead.

**Path forward:** exempt by *named path*, not by *category*. Fingerprint ignored
paths too (`git status --porcelain --ignored=matching`, or a stat sweep for
`read_only_trees`), and subtract only an explicit list —
`agentic_orchestration/factory/sessions/`, `agentic_orchestration/factory/receipts.db*`.
Then invert `test_permissions.py:211` into its falsification partner: a gitignored
write *outside* the factory's own session paths must breach.

---

## F2 — BLOCK — a non-git (or git-failing) declared repo fails OPEN

**File:** `agentic_orchestration/factory/permissions.py:131-136`, `:149-152`
**Pinned by:** `tests/test_permissions.py:226-229` (`…_is_inert`)

```
is_git: False | error: fatal: not a git repository (or any of the parent directories): .git
changes detected: []
breaches: []
```

`fingerprint()` records the failure honestly (`is_git=False`, `error=…`), and then
**nothing ever reads either field.** `diff_fingerprints` returns `[]`
unconditionally at line 151, and `runner.py:174,190` calls `perm.fingerprint(r)`
without inspecting the result. The phase proceeds to gates with an empty
change-set and greens. In an architecture whose entire thesis is default-fail,
this one path defaults open.

Realistic triggers, in rough order of likelihood:

1. **A typo or stale path in `repos:`.** `workflow.py` validates that `wf_root`
   exists (`:105`) but never validates the `repos:` entries at all — not that they
   exist, not that they are git trees. A mistyped repo silently disables
   containment for that tree with no diagnostic.
2. `safe.directory` / dubious-ownership refusal on a moved or externally-mounted
   tree.
3. A stale `index.lock` from a concurrent git operation.
4. `git` absent from the subprocess `PATH`.

**Path forward:** this belongs exactly where `workflow.py`'s own docstring already
puts it — *"Fails at LOAD, not mid-run."* Validate at load that every `repos:`
entry exists and is a git worktree. Mid-run, a `TreeFingerprint` with
`is_git=False` or a non-null `error` must abort the run as a containment failure,
not return an empty diff. Then rename the test: a non-git tree being "inert" is
the defect, not the specification.

---

## F3 — WARN — `diff_matches_claims` cannot fail on a mechanical phase

**File:** `runner.py:174-215` (ordering) · `gates/core.py:160`

`run.changed_paths` is computed from the fingerprint pair taken *around execution*.
For a mechanical phase, execution is the synthesis of an envelope in
`_execute` — a no-op that cannot touch disk. All real mechanical work happens
inside a gate command, i.e. *after* the change-set was already measured. So
`measured` is always the empty set and `unclaimed = {} - claimed` is always empty.

Confirmed in every run, including the shipped one:

```
OK   diff_matches_claims: PASS -- change-set (0 path(s)) is a subset of the 1 claimed
```

The post-gate fingerprint (`runner.py:217-235`) *does* see those writes, but it is
consumed only for breach classification and never fed back to the gate. Net: an
allowed-but-unclaimed write made by a gate command is never surfaced.

This is not a false green in the dangerous sense — permissions still fires on a
git-visible breach. But **3 of the shipped workflow's 14 green verdicts are
structurally incapable of red**, and "14 gate verdicts, all green" reads as more
adjudication than occurred. Fix: pass the post-gate change-set into
`diff_matches_claims`, or drop the gate from mechanical phases and say why.

---

## F4 — WARN — harness fields are silently dropped before the receipts (Discipline #8)

**File:** `harness/claude_code.py:140-146` → `receipts.py:340` (`record_agent_session`)

`RawResult.extra` is populated with `elapsed_ms`, `num_turns`, `stop_reason`,
`frame_count`, and **`permission_denials`**. A tree-wide grep confirms `.extra` is
read by exactly nothing outside `gates/base.py`'s unrelated `RunContext.extra`.
There is no column for any of it in `agent_sessions`, and no test asserts the
round-trip.

This is the B14.5 `convergence_report` failure mode reproduced exactly: a producer
computes a field, the writer has no slot for it, and it dies in memory with no
error. `permission_denials` is the containment-relevant one — it is the record of
the agent attempting a tool use it was not permitted — and it is lost on precisely
the lane this gate would open.

Fix: add the columns (or one `extra_json` column) and a round-trip test.
Discipline #8 wants validation *at* the boundary, and this boundary currently has
none.

---

## F5 — WARN — `usage_absent_reason` is overloaded and will mislead a Tier-2 consumer

**File:** `usage.py:83-86` → `receipts.py` `phases.usage_absent_reason`

`from_claude_result_frame` sets
`absent_reason="harness reported no reasoning_tokens field"` on a **fully
populated** usage object. Since the probe confirms the harness never reports
`reasoning_tokens`, *every real agentic phase* will land a non-null
`usage_absent_reason` next to real token counts.

The column name says "usage absent." A consumer filtering
`WHERE usage_absent_reason IS NOT NULL` to find phases with no usage data gets a
false positive on every row. `one_line()` happens to hide it, which is why no test
caught it. Fix: separate `reasoning_absent_reason` from `usage_absent_reason`, or
rename the column. Worth doing before `SCHEMA_VERSION` 1 acquires a consumer.

---

## F6 — INFO — `_normalize` mangles dotted paths

**File:** `gates/core.py:26` — `str(Path(p)).lstrip("./")`

`lstrip` takes a character *set*, not a prefix:

```
_normalize([".github/w.yml", "../outside.txt"]) -> {"github/w.yml", "outside.txt"}
```

Two distinct paths can normalize to the same string and be treated as claimed in
`diff_matches_claims`. Narrow reachability, but it is a comparison gate. Use
`removeprefix("./")`.

## F7 — INFO — `receipts.record_process` is dead code

Defined at `receipts.py:299`, called only from `tests/test_receipts.py:127`. The
`processes` table will be empty in every real run. Wire it from `_exec_verdict` or
mark it reserved — one of the seven advertised tables currently holds nothing.

## F8 — INFO — writes outside all declared `repos` are wholly uncontained

The runner fingerprints only `wf.repos`. Writes to `~/.claude/`, `/tmp`, or a
sibling repo not listed are invisible by construction. This is inherent to v1 with
sandboxes deferred (ruling D5) and is not a defect — but it is not disclosed in
the landing note's § 7 scope-compliance section, and it should be, because § 7
currently reads as a stronger containment claim than v1 makes.

---

## Action

- [ ] **star-lord — F1:** replace the category-wide gitignore exemption with a
      named-path exemption; fingerprint ignored paths in all repos and especially
      in `read_only_trees`. Invert `test_permissions.py:211` into a falsification
      partner. **Discharges when** a planted write to a gitignored path outside
      the factory's own session paths aborts the run, proven by a live run, not a
      unit test.
- [ ] **star-lord — F2:** validate `repos:` entries at LOAD; treat
      `is_git=False`/`error` as a run-aborting containment failure mid-run.
      **Discharges when** a workflow naming a non-git repo refuses to start, and a
      mid-run git failure aborts rather than greening.
- [ ] **star-lord — F3/F4/F5:** feed the post-gate change-set to
      `diff_matches_claims`; persist `permission_denials`; de-overload
      `usage_absent_reason`. F5 before `SCHEMA_VERSION` 1 gains a consumer.
- [ ] **star-lord — F6/F7/F8:** `removeprefix`; wire or reserve `record_process`;
      add the uncontained-space disclosure to the landing note § 7.
- [ ] **star-lord:** re-submit for Gate-2 re-review after F1 + F2. F3–F8 do not
      gate the re-review.
- [ ] **Matt — decision needed:** none required to *unblock* — F1 and F2 are
      developer-fixable defects, not architectural calls, so this stays within my
      authority per ADR-002 rather than escalating. Escalate only if star-lord
      contests that gitignored-path containment is in v1 scope; that would be a
      scope amendment to Spec A § 8 and yours to rule on.
- [x] **jack-ryan:** mechanical lane approved to continue. No halt.

## Note to gandalf (DRIFT-CRITIC)

The O4 dollars delta flagged for your ruling is, in my read, resolved correctly and
does not need to be dropped: the figure never appears without `dollars_source`
beside it, in the dataclass, the DB column, and `report.py`. The § 3 reasoning —
that a plausible-looking number is a worse failure than silence — is sound and I'd
keep it on the record. My concern sits one field over, at F5: the *labeling*
discipline was applied to dollars and not to `absent_reason`, which is the same
class of problem (a field whose name asserts more than its contents).

## References

- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/factory/permissions.py`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/factory/runner.py`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/factory/phase.py`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/factory/gates/base.py`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/factory/gates/core.py`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/factory/workflow.py`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/factory/receipts.py`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/factory/usage.py`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/factory/harness/claude_code.py`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/factory/tests/test_permissions.py`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/factory/tests/test_gates.py`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/factory/tests/test_usage.py`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/factory/workflows/kc2-baton-mechanical.yaml`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/star-lord/notes/2026-08-10-factory-spine-landing.md`
- Probe evidence (gitignored, in-tree):
  `factory/sessions/jr-breach-probe-ignored-20260810T231116Z-9fc806/` (escaped, green)
  `factory/sessions/jr-breach-probe-tracked-20260810T231128Z-d1df65/` (contained, aborted)
  Probe workflows: `/tmp/jr_breach_ignored.yaml`, `/tmp/jr_breach_tracked.yaml`
