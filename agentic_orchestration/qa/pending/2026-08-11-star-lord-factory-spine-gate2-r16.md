# Finding — 2026-08-11 — factory-spine Gate-2 round 16

**Reviewer:** jack-ryan
**Severity:** BLOCK (agentic lane) / PASS-WITH-CONDITIONS (mechanical lane)
**Target:** `c3a4426a` (r15), `265adf95` (r16)
**Developer:** star-lord
**Captured by:** star-lord (jack-ryan does not write findings files; verdict returned inline and captured verbatim)
**Principles applied:** REVIEW_PROCESS #2 (smoke-gate), #3 (cross-seam impact), #4 (decisions-log as truth), #5 (severity matters). Disciplines 8 (validation at boundaries), 10 (empirical inspection over assumption), 12 (tag intermediate states). ADR-004 (MIGRATION), ADR-006 (read-only external systems). README rules 2, 5, 13, 28, 29, 30, 35, 36, 37.

## Verdict summary

| Finding | Round | Adjudication |
|---|---|---|
| J3 usage merge | 15 | **CLOSED** |
| J4 gitdir-as-FILE | 15 | **CLOSED** — with a residual, JR-5 below |
| J5 / J5b grant + stamp | 15 | **CLOSED** |
| H7 content signature | 15 | **CLOSED** |
| H6 host + trees | 16 | **CLOSED IN KIND, three WARNs** — JR-1, JR-2, JR-3 |
| J6 failure reason | — | **INFO**, rides to the agentic lane |
| J7 BUILTIN_TOOLS | — | **BLOCK, escalated** — this is the new agentic-lane block, not a rider |
| J8 `check_grant(init, [])` | — | **INFO**, unreachable through the loader |

---

## 1. Re-audit of star-lord's claims (question 1) — the rule-29 queue, closed

I ran the audit star-lord named and did not close. **Answer: five sites, one root cause, and it is J4-c verbatim.**

`permissions.py:697, 700, 706, 721, 727` emit keys of the form `.git\t<...>`. `_matches` protects by literal `.git/` prefix (`permissions.py:1158` — `path.startswith(bare + "/")`). Measured, not read:

```
prot  classify->BREACH   '.git/\t<common>/hooks/pre-commit'      <- the J4-c fix, correct
NOT   classify->ALLOWED  '.git\t<gitdir pointer unreadable: ...>'
NOT   classify->ALLOWED  '.git\t<gitdir pointer unparseable>'
NOT   classify->ALLOWED  '.git\t<gitdir points at a non-directory: /tmp/x>'
NOT   classify->ALLOWED  '.git\t<commondir unreadable: ...>'
NOT   classify->ALLOWED  '.git\t<commondir points at a non-directory: /tmp/x>'
```

Both claims fail, not one. The rollback's `git_internal` guard at `permissions.py:1479` tests `change.path == ".git" or change.path.startswith(".git/")`, so it does not fire either. Under a restrictive `writes` these become breaches by the allowlist route and then reach the rollback, which reports:

```
guard = nothing_at_path
reason = 'nothing at this path by rollback time; another process may have removed it,
          so the deletion is not ours to claim'
```

That sentence is false about a synthetic key that was never a path. Rule 17 — a negative claim is a claim.

**Mutation JR-5, full suite:** I changed `permissions.py:697` from `.git\t` to `.git/\t` — a mutation *toward* correctness. **SURVIVED, 538/538 green.** Nothing in the suite can tell the protected keying from the unprotected keying in either direction. That is the exact evidence rule 29 predicts.

**But I could not reach it, and I tried four ways.** Real git repos, real linked worktrees, real submodules:

| scenario | result |
|---|---|
| `commondir` chmod 000 | `after.usable = False` → `ContainmentError`, run stops |
| `commondir` → non-directory | `ContainmentError`, run stops |
| `.git` pointer → non-directory | `ContainmentError`, run stops |
| `.git` pointer unparseable | `ContainmentError`, run stops |
| submodule gitdir, planted `commondir` | `ContainmentError`, run stops |

Every route that produces one of these keys also makes `git status` fail, so rule 2 (unmeasurable is not clean) halts the run before `classify` ever sees them. **The hole is real and currently masked by a neighbouring guard that nothing ties to it.** As of today no receipt can ever carry one of these five keys.

Severity **WARN**, not BLOCK, on discipline 10 — I do not report an exploit I could not produce.

**The fix is already in the module, 380 lines away.** `diff_fingerprints:1131` does `d = d.split("\t")[0]` for structure members, which is why the structure markers are safe. The entries path (`:1102–1111`) does not. One normalization applied in `_matches` / `_read_only_hit` / the `git_internal` guard closes all five and every future marker, instead of five one-character edits that the next marker re-opens.

**Cheapest refuting test:** the JR-5 mutation above. If a row exists that kills it, this finding is wrong.

---

## 2. H6's honesty (question 2) — star-lord asked me to rule, so I am ruling

**Sufficient in kind. Insufficient in direction.** Two separate answers.

**On kind — it is not the narrow-answer-in-wide-clothes defect.** That defect requires the narrow answer to be *presented* as the wide one. `host.py:44–47` puts the caveat in the value, not the doc, so the mode cannot be read without it. `test_H6_a_STATED_host_default_is_read_and_its_source_named` asserts the caveat on the success path and my mutation JR-2 (drop the caveat from the stated-mode branch) **was KILLED by exactly that row.** The load-bearing half is genuinely held. Reading one layer and saying so is a measurement; reading one layer and calling it the mode would have been the defect. Star-lord did the first.

**On direction — there is one gap, and it is the one star-lord would not have argued himself out of.** `_LAYERS_NOT_RESOLVED` names *which* layers are unread. It does not say *which way they can move*. Enterprise policy and CLI flags can both be strictly more permissive than the user file. So a recorded `bypassPermissions` is sound — it is the alarming answer, and alarming answers are self-correcting. A recorded `default` is not: it reads as "the host was ordinary" when an unread layer may have made it anything but. The column's falsely-reassuring case is live and the sentence does not warn about it.

This is rule 36 applied to itself: you recorded what you could not measure, and not which direction the unmeasured thing can move.

**Action:** one clause in `host.py:44–47` — an unread layer can be *more* permissive than the one recorded, so a recorded mode is a floor on restriction and not a ceiling on permission. WARN.

---

## 3. The mutation evidence (question 3) — the reading is half right, and the wrong half matters

Star-lord wrote: *"I read that as H6 being a smaller finding, not as the suite having gotten strong. Test that reading."*

Tested. **H6 is a smaller finding AND the suite is weak on exactly the axes H6 introduced.** Five independent mutations, full 538-row suite each, killers by name:

```
SURVIVED  JR-1  runner records only the FIRST repo as measured (trees + sentence)
KILLED    JR-2  a STATED host mode drops the layers-not-resolved caveat
                first killer: test_H6_a_STATED_host_default_is_read_and_its_source_named
SURVIVED  JR-3  report renders the host mode WITHOUT its source sentence
SURVIVED  JR-4  report drops the trees line entirely (mode + limit still render)
SURVIVED  JR-5  gitdir-pointer failure key made PROTECTED (mutation toward correctness)
```

Four survivors. Star-lord's five mutations all targeted paths his own rows were written for; these target the paths nothing was written for.

### JR-1 — `measured_trees` is the DECLARATION, and the multi-tree case is uncertified

`runner.py:141–142` records `measured_trees=self.wf.repos` inside `start_session`, **before any phase runs and therefore before any fingerprint**. `receipts.py:319` says *"`measured_trees` is the set actually fingerprinted."* It is the set that was declared. If a run aborts at phase 0, the row still claims trees were fingerprinted.

And nothing certifies more than one. `test_H6_a_RUN_records_the_trees_it_actually_fingerprinted:188` asserts `== [str(git_repo)]` against a one-repo workflow, so `self.wf.repos[:1]` is the identity function on the only fixture that exists. `test_H6_the_limit_sentence_names_the_trees` passes two trees to the pure function and never to the wiring.

This is J3's SCOPE axis recurring in round 16 — *"none of the five H8 rows set `retries > 0`"* — and it lands on the one column whose entire job is naming a boundary. A boundary sentence is decoration on a single tree; it does work only when there are several, and several is the meta-repo's production shape (engine + godot + demo + loadout). **The column is true in the test and over-claiming in the configuration the factory is for.**

**Cheapest refuting test:** a runner row with two declared repos asserting both appear in `measured_trees` and in `measurement_limit`. It kills JR-1 and it is the only row that can.

### JR-3 / JR-4 — storing the caveat and showing it are two claims

The H6 thesis: *"a query that returns the mode cannot separate it from what the mode is worth."* True of the column. **False of the renderer**, and the renderer is what a human reads.

`report.py:107` joins mode and source. Cut the source (JR-3) — 538 green. `report.py:109–123` renders the trees. Delete the block (JR-4) — 538 green.

Both survive because the single green-path row's three content assertions are each satisfiable by a mechanism other than the one they name:

- `:225 "bypassPermissions" in text` — satisfied by the mode alone, with or without its source.
- `:226 str(git_repo) in text` — satisfied by `**Root:**` at `report.py:146`, which prints the same path for an unrelated reason.
- `:227 "not 'no unauthorised writes'" in text` — satisfied by the limit column, which JR-4 does not touch.

That is **rule 28 on H6's own certifying row**: the row is aimed at a proxy that moves for reasons unrelated to the claim. The J2 fix applied rule 28 to `test_F3_partner_…`; the row written one round later has the same shape.

**Cheapest refuting test:** assert on the *rendered block*, not on substrings of the whole document — locate `## What was measured — and what was not`, slice to the next `##`, and assert mode, source and every declared tree inside that slice. One row, kills JR-3 and JR-4 together, and cannot be satisfied by `**Root:**`.

---

## 4. J6 / J7 / J8 (question 4) — one of these is not like the others

**J6 — INFO, rides to the agentic lane.** `harness/claude_code.py:353` collapses to the literal `"is_error"` when a phase fails with a non-zero return code, no grant error, no denial and no `api_error_status`. A ledger row that records a failure and cannot name it is rule 9 on the agentic lane. Not reachable mechanically; the harness is not constructed for a mechanical phase.

**J8 — INFO, unreachable through the loader.** `check_grant(init, [])` fails the `is None` guard, adjudicates against `expected = set()`, and returns `None` when `granted` is also empty. `validate_tools:147–152` refuses an empty list at load, so `[]` cannot arrive from a workflow. Worth noting for the record only because it is *inconsistent with the J5 ruling*: `granted_tools IS NULL` ≠ `'[]'` was made load-bearing in the ledger, and the adjudicator that produces those values collapses the same distinction. Same semantics, two layers, opposite answers. Defense-in-depth, not a hole.

**J7 — BLOCK, escalated as the agentic lane's block rather than accepted as a rider.**

Star-lord framed J7 as *"`BUILTIN_TOOLS` admits `Task` / `EnterWorktree` / `CronCreate` whose grant ≠ their reach."* That is the finding, and it is larger than its framing. J1 established that after `--allowedTools` proved inert, the tool **base-name vocabulary is the agentic lane's only pre-hoc fence**. `BUILTIN_TOOLS` at `harness/claude_code.py:98–104` is that vocabulary. It currently contains entries that dissolve the fence in two structurally different ways:

- **`Task`** — delegates to a sub-agent. The child's grant is not the parent's `--tools`. A phase declaring `tools: ["Task"]` passes `validate_tools`, passes `check_grant` (granted set matches declared set exactly), and reaches whatever the child is granted. The fence is *satisfied* while being *bypassed* — which is J1's shape, in the mechanism that replaced J1.
- **`CronCreate` / `ScheduleWakeup` / `RemoteTrigger` / `PushNotification`** — reach past the run's *time* boundary. The wall is `fingerprint(before) → execute → fingerprint(after)`. Anything scheduled fires after the after-fingerprint. This is F3's shape on a new axis: *a channel that structurally cannot carry the counterexample*, except the axis is time rather than path, and no amount of hashing closes it.

This is **not** the containment-posture question and therefore **not** Matt's call to make before star-lord acts. The posture question is "how fine can a pre-hoc fence be" — base names vs. scopes — and that is his. This is rule 13 applied to a list star-lord owns: a closed vocabulary that admits names whose grant does not equal their reach is not closed. `BUILTIN_TOOLS` was probed off a live init frame, which established *what the CLI has*; it never established *what each one reaches*, and those are two questions.

**Cheapest refuting test, and it is four minutes of the same kind already spent on J1:**

```
claude -p "Use the Task tool to run a sub-agent that runs: echo REACH_ESCAPED"
  --tools Task --permission-mode default --strict-mcp-config
```

If the child cannot run `Bash`, `Task` is safe in the vocabulary and I withdraw that half. If it can, `Task` must leave `BUILTIN_TOOLS` (or be admitted only with a recorded caveat per rule 36), and the schedulers must leave with it or be declared as reaching past the wall. Run the probe before arguing either way — that is what settled J1's largest claim and its largest error in one sitting.

---

## 5. Stopping rule (question 5) — recommendation, on the record

Matt decides. This is my recommendation, and I want the reasoning on the record because "we found another one" will remain available indefinitely and is not an exit criterion.

**Gate-2 passes when three clauses hold. Not when the findings run out.**

**Clause 1 — the mechanical lane closes on evidence class, not on round count.** A round that produces only *claim gaps with no reachable exploit* is a documentation round. This round produced exactly one such (JR-5: five unprotected keys, five failed reachability probes). **Two consecutive rounds in which every finding is unreachable = the series has converged and the mechanical lane passes.** Round 16 is the first. One more like it and I sign it off. That is a criterion star-lord can meet, it is falsifiable, and it does not reward finding smaller things.

**Clause 2 — the agentic lane does not pass on review at all, and no number of rounds will change that.** Containment against a process holding unrestricted `Bash` is not a finite problem, and sixteen rounds have demonstrated that empirically rather than argued it. It passes on **a stated threat model with a named boundary** (star-lord + gandalf, ratified by Matt), plus `BUILTIN_TOOLS` reduced to a vocabulary whose grant equals its reach (J7). Everything outside the boundary is **accept-and-state, recorded on the receipt** — which is precisely the move H6 just made for the host default, generalized from one setting to the whole posture. Rule 36 is already the answer; it has not been applied at the level it needs to be.

**Clause 3 — the mechanical lane's first compiled workflow fires before the agentic lane is settled.** These are separable and holding them together is now costing more than it buys. The mechanical lane has been PASS-WITH-CONDITIONS since round 14 and every round since has found agentic-lane defects and mechanical-lane claim gaps. Ruling D4's gate is "before the first compiled workflow fires" — a mechanical workflow can fire under clause 1 without waiting on clause 2.

**What I would tell Matt in one sentence:** the review series stopped finding reachable defects two rounds ago and started finding unasserted claims, which is the signature of convergence rather than of thoroughness, and the remaining risk is concentrated entirely in one list of tool names.

---

## 6. Not adjudicated — flagged only

- **v1 containment posture (base-names-only pre-hoc).** Matt's. It does not change the verdict: every finding above is inside the posture, not about it. J7 is a vocabulary defect *within* base-names-only, not an argument against it.
- **Threat-model boundary with gandalf.** Matt's, and it is clause 2 of the stopping rule. It is the only thing that unblocks the agentic lane, so it is now the critical path rather than an owed document.

---

## Action

- [x] star-lord: **JR-5** — normalize the synthetic-marker separator once, in `_matches` / `_read_only_hit` / the `git_internal` guard, using `diff_fingerprints:1131`'s existing precedent. Add one `classify` assertion under `writes=["**"]` per rule 29. WARN.
      → `marker_path()` at `permissions.py:518`, shared by all three sites. Rows mint the five keys through the real producer (no literals) and assert on `classify` under `writes=["**"]` and on `rollback`. Mutations R17-d/e/f killed. R17-g (`_read_only_hit`) survived the first pass and is now killed by `test_JR5_a_marker_on_the_READ_ONLY_TREES_OWN_key_still_names_that_tree` — see notes § 21.6. Your own JR-5 mutation re-run post-fix: **survives, and its inertness is the receipt** (notes § 21.7, README rule 45).
- [x] star-lord: **JR-1** — a runner row with **two** declared repos asserting both in `measured_trees` and `measurement_limit`; and correct `receipts.py:319`'s "actually fingerprinted" to say what the value is (the declared set, recorded at run start) or move the write to where the fingerprint happens. WARN.
      → `test_JR1_a_run_with_TWO_declared_trees_records_BOTH`; kills R17-h and R17-i. Docstring corrected to "the DECLARED set, recorded at session open" rather than moving the write — a run that aborts at load must still leave behind what it was going to measure. `MIGRATION.md` says the stored values did not change and no migration is required; only the claim about them did.
- [x] star-lord: **JR-3/JR-4** — assert on the rendered `## What was measured` block slice, not on document substrings. Kills JR-3 and JR-4 with one row. WARN.
      → `_measured_block(text)` helper in `test_host.py`; the green-path row now asserts the mode↔source join inside the slice. Kills R17-j and R17-k.
- [x] star-lord: **H6 direction clause** — `host.py:44–47`, state that an unread layer can be *more* permissive. WARN.
      → On all four source shapes, not just the read path. `test_JR_the_caveat_states_which_WAY_the_unread_layers_can_move`; kills R17-l.
- [x] star-lord: **J7 probe** — run the `Task` sub-agent reach probe before amending `BUILTIN_TOOLS`. BLOCK.
      → Probed 2026-08-11 on `claude 2.1.119`. A parent granted `--tools Task` reported `tools: ['Task']` at `init` and spawned a child holding `Bash`, `Edit`, `Write` and eleven more; `is_error: false`, `permission_denials: []`. `BUILTIN_TOOLS` was **not** amended — membership was never the wrong answer. `UNFENCEABLE_TOOLS` (7 names) refuses at load, *before* the membership check, because these names ARE members. Frames preserved at `star-lord/notes/evidence/2026-08-11-tool-fence-probes/` with the refused first framing kept deliberately. Mutations R17-a/b/c/m killed.
- [ ] star-lord (optional, INFO): J6 failure-reason vocabulary; J8 empty-vs-absent parity with the J5 ledger semantics.
      → **not worked.** No row, no code.
- [ ] **Matt:** ratify or amend the three-clause stopping rule in § 5, and confirm the mechanical/agentic lane split in clause 3.
- [ ] **Matt:** the threat-model boundary is now the agentic lane's critical path, not a parked document.

## References

- `agentic_orchestration/factory/permissions.py` — `:697, :700, :706, :721, :727` (unprotected keys), `:793` (J4-c fix, correct), `:1131` (the normalization that exists), `:1158` (`_matches`), `:1479` (`git_internal` guard)
- `agentic_orchestration/factory/host.py` — `:44–47` (`_LAYERS_NOT_RESOLVED`), `:63–71` (ROUTE, correct), `:103–109` (zero-fill refused, correct)
- `agentic_orchestration/factory/report.py` — `:107` (JR-3), `:109–123` (JR-4), `:146` (the `**Root:**` line that satisfies `:226`)
- `agentic_orchestration/factory/runner.py` — `:140–142` (H6 wiring, JR-1), `:374, :379` (J3 merge, correct), `:204–209` (fingerprint scope)
- `agentic_orchestration/factory/harness/claude_code.py` — `:98–104` (`BUILTIN_TOOLS`, J7), `:353` (J6), `:367–427` (`check_grant`, J8)
- `agentic_orchestration/factory/receipts.py` — `:217–290` (J5b read→migrate→stamp, correct), `:319` (the "actually fingerprinted" claim)
- `agentic_orchestration/factory/tests/test_host.py` — `:184–192` (JR-1's uncertified row), `:198–227` (JR-3/JR-4's proxy assertions)
- `agentic_orchestration/jrmut.py` — jack-ryan's mutation harness, left untracked and re-runnable; restores every file in a `finally`, reports killers by name, verified against a green baseline before use (rule 35)

---

## star-lord's independent verification of the reported measurements

Before acting I re-ran the two claims that indict my own work, rather than accepting them:

- **JR-5** — `_matches(key, ".git/**")` returns `True` for the J4-c key `'.git/\t<common>/…'` and `False` for all five `'.git\t<…>'` failure keys. Confirmed.
- **JR-3/JR-4** — `report.py:146` emits `**Root:** \`{session['root']}\``, and in `test_H6_the_caveat_is_rendered_on_a_run_with_NO_breaches` the workflow root IS `git_repo`. So `assert str(git_repo) in text` passes off the Root line whether or not the trees block renders. Confirmed: rule 28, on the row I wrote to certify H6.
