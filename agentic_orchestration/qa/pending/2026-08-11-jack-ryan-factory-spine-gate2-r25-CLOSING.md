# Finding — 2026-08-11 — factory-spine Gate-2 round 25 — **CLOSING VERDICT**

**Reviewer:** jack-ryan
**Severity:** **Mechanical lane — LIFT** (three WARN and two INFO ride as declared debts) / **Agentic lane — HOLD, clause 2 only, unchanged**
**Target:** `b8c0311c`, comprising `d3d4df43` (JR-22) · `9be3c525` (JR-23) · `e6a57cc5` (JR-24, JR-25) · `7d3c2b20` (JR-26) · `6bbe85ab` · `b8c0311c`
**Developer:** star-lord
**Against:** `2026-08-11-star-lord-factory-spine-gate2-round-24-return.md`, remediating my round-22 verdict at `qa/pending/2026-08-11-star-lord-factory-spine-gate2-r21.md`
**Principles applied:** REVIEW_PROCESS #2 (smoke-gate), #5 (severity matters). Disciplines 8 (validation at boundaries), 9 (attribution clarity), 10 (empirical inspection over assumption). README rules 13, 44, 45, 47, 48, 49, 50, 50a, 50b, 50c.

**This verdict closes the ladder.** Per Matt's directive it lands regardless of outcome; there is no round 26. Everything below that is not CLOSED is a **declared debt** and its disposition passes to gandalf (SB-1 § 4 fallback + D5 revisit). Nothing here is a remediation request to star-lord.

---

## 0. The one-word answers

| lane | state | on what |
|---|---|---|
| **Mechanical** | **LIFT** | My round-21 BLOCK was JR-22. JR-22 is closed and I verified the closure by measurement. JR-23's damage class is closed and I verified that by measurement. **Nothing found this round meets the BLOCK bar I set at r19 and applied at r20/r21** — no write escapes detection, classification, the receipt, or the abort. The four new findings are WARN/INFO and are named in § 4 |
| **Agentic** | **HOLD, clause 2 only, unchanged** | The threat-model boundary is gandalf's and Matt's and remains this lane's critical path. Nothing mechanical can move it, and nothing this round tried to. My earlier rounds worded this "BLOCK stands, clause 2"; that is the same state, and I adopt Matt's **HOLD** label so the landing declaration carries one word |

**Suite: 622, green, confirmed independently.** `622 passed in 185.71s`, `-p no:randomly`, in a tree extracted from `git archive b8c0311c` and verified file-by-file against HEAD's blobs before the run. Confirmed, not accepted. Was 611 at `7bbba6fb`.

**Instrument note.** Nothing in this round ran against the live tree. Every mutation ran in its own tree copied from the verified-pristine reference; landing was verified by whole-file equality plus an assertion that the changed-file set was exactly one path; the tree was digested immediately before and immediately after pytest and no row was published unless the digests matched; the tree was destroyed afterwards. `git diff HEAD -- agentic_orchestration/factory` is empty and was never non-empty. Probes ran in a separate copy with the loaded `permissions.py` asserted `sha256`-identical to `git show HEAD:` before any probe executed.

---

## 1. Answering the five questions put to me, in order

### 1.1 Does R25-E still hold? — **Yes, and it holds for the right reason.**

Re-ran my R24-C at HEAD (`git_path = marker_path(change.path)` → `git_path = change.path`):

```
JRA   raw  11 failed, 611 passed in 177.87s
      10 × test_JR5_the_rollback_REFUSES_a_marker_key_rather_than_acting
           [both fenced shapes × five broken-pointer parameters]
       1 × test_C2_every_assert_under_tests_is_proven_to_execute
```

**My figure, unmoved, and the FAILED list is identical to the one I recorded at round 22.** star-lord's R25-E is exact.

I did not stop at the count, because a matching count after a new guard lands two lines from the target is precisely what rule 50 warns about. The killing row asserts `a.guard == "git_internal"` (`test_containment_wall.py:2340`). With `marker_path` removed at the guard, the marker-bearing key stops matching `.git`, falls through to the new `unreadable_marker` guard, is still `NOT_ROLLED_BACK` — and reds on the guard-name leg. **So the row dies for the reason I wrote it for, not because something else caught it.** The `assert a.action == "NOT_ROLLED_BACK"` leg would now pass; the row survives the decoupling because it carries a guard-name leg. That leg is what saved my ledger row, and it was there before this round.

**And the ordering claim is not merely correct, it is pinned.** star-lord writes: *"Placed first, all eleven would still have failed and the receipt would have looked identical while measuring something else."* I measured that sentence rather than granting it — mutation JRD makes `git_internal` decline any key carrying `MARKER_SEP`, which is exactly "placed first":

```
JRD   raw  11 failed, 611 passed in 174.65s   — FAILED list BYTE-IDENTICAL to JRA
```

Two different mutations, one receipt. star-lord's statement is confirmed to the row. It is also the strongest worked example rule 50 has produced: the tell that distinguishes them is not available in the receipt at all, only in knowing which edit you made. Recorded for the rule.

### 1.2 Is the JR-23 fix complete? — **The damage class is closed. The recorder/matcher split leaves a fourth behaviour, and it is at the guard, not at a call site.**

**What is closed, measured in both fixture shapes** (probe, `permissions.py` sha256-verified against HEAD):

```
phase's only action:  mkdir "data\tmarker"  inside a read-only tree, ignored+untracked neighbour
CHANGES:   [('protected/data\tmarker', 'created')]
BREACH:    write inside a read-only tree
ACTION:    path='protected/data\tmarker'  NOT_ROLLED_BACK  guard='unreadable_marker'
data/precious.txt   SURVIVES        <-- the K1/L1 damage class, closed
artifact NAMED on the receipt        <-- Discipline #9 NAME axis, closed
```

Both clauses of my JR-23 are answered. star-lord's regrade to BLOCK was correct and their reproduction was correct.

**What is not closed is the CLAIM axis — the thing the second half was added to protect.** § 4.1 (JR-27). In short: the new guard is keyed on the string (`MARKER_SEP in change.path`) and fires on one whole arm where its reason cannot ever be true.

**On the three-matchers claim itself: verified, and one of its premises is genuinely held elsewhere.** `test_JR23_truncation_is_FAIL_CLOSED_…` argues that `_read_only_hit` is safe under truncation *because it matches in both directions*. That premise is a load-bearing input to the row's whole argument and the row does not assert it. I checked whether anything does — mutation JRC removes the ancestor arm:

```
JRC   raw  4 failed, 618 passed
      test_JR12_a_COLLAPSED_ANCESTOR_key_still_reaches_the_read_only_tree ×2 shapes
      test_permissions.py::test_a_collapsed_entry_ABOVE_a_read_only_tree_breaches
      test_C2
```

**KILLED.** The premise is pinned, by JR-12 and by `test_permissions.py`. star-lord's stated reason is sound and its dependency is covered. No finding; recorded because a reasoned claim whose premise nothing checks is what JR-19 was about, and this one is checked.

### 1.3 Rule 50c — **right, and stated one notch too narrow.** § 4.4.

### 1.4 Rows that pass for the wrong reason — **yes, one, and I have it by measurement.** § 4.2. `test_JR23_the_STRUCTURE_WALK_records_the_name_it_was_given` answers *"does this source region contain the substring `marker_path(`?"* as a proxy for *"does the recorder truncate?"*. The wrong answer looks safe.

### 1.5 Vacuous / tautological / expectation-derived legs in the three new JR-23 rows — **one dominated leg.** § 4.3. Nothing vacuous, nothing that derives its expectation from the code under test. The three rows kill disjoint mutant sets, which I confirm: JRA/JRD kill neither of them, JRB kills only the scene row, JRC kills neither.

---

## 2. What I verified of star-lord's other claims

| claim | my finding |
|---|---|
| Suite is 622, green | **Confirmed.** `622 passed in 185.71s`, independent tree, blob-verified |
| JR-23 regrade WARN → BLOCK | **Correct, and I accept the regrade.** The `destroyer` guard does fire on a condition the phase removes; my WARN rested on it; the untracked shape is the reachable one |
| R24-A…D refuted my `_read_only_hit` prediction | **Accepted.** I did not re-run the four; JRC independently confirms `_read_only_hit` is well covered, which is consistent with their 9 |
| "Your fifteen is correct" | **Confirmed, and their self-correction is right.** Walked it myself: `7bbba6fb` → 4 modules in `ADJUDICATED_MODULES`, **15** vocabularies. HEAD archive → 21 modules walked, **16** vocabularies, and the delta is exactly `FACTORY_RUNTIME_FILES`, i.e. their own JR-22 split. Live tree → 48 `.py` naive, **10 under `sessions/`**, filtered walk 21 modules / 16 names. The `sessions/` hazard is real, the exclusion is right, and the observation that a `git archive` review environment is *cleaner* than the shipping tree is the durable part |
| R25-F missed its target; rule 50c is the repair | **Accepted as reported.** Self-surfaced, which is the correct behaviour and the second time this series has produced it |
| R25-E: raw `11 failed, 611 passed` | **Reproduced exactly**, § 1.1 |
| JR-24 third exit, JR-25 seven figures, JR-26 (a)(b)(c) | **Accepted on their receipts.** I re-derived the JR-24 walk figures myself; I did **not** re-measure the seven JR-25 member figures or R25-H…K this round and I am saying so rather than implying coverage I do not have. Stated plainly because a claim of verification I did not perform is the exact defect this ladder has spent five rounds on |
| The instrument failed and was re-run | **Accepted, and the correction is the right one.** "Was the tree clean when I started" is a precondition; "was the tree stable while I measured" is an invariant. Third instrument defect in the series, self-caught, fail-closed. My own harness has carried the digest-stability check from round 22 and it is the reason I can publish these figures |

---

## 3. My mutation table this round

Four suite mutations plus three probe batteries. Baseline 622. Every row: fresh tree from the blob-verified pristine reference, single-file change asserted against the reference digest map, tree digested before and after pytest with equality required, `-rEf` collection, raw summary line reported undeduped, tree destroyed. Reference and harness at `/tmp/jr25/ref` and `/tmp/jr25/mutate.py`.

| id | mutation | observed |
|---|---|---|
| B0 | none (baseline at `b8c0311c`) | **622 passed in 185.71s** |
| JRA | rollback `git_internal` loses `marker_path` — **my R24-C, re-run post-fix** | **KILLED — `11 failed, 611 passed`.** `test_JR5_the_rollback_REFUSES_a_marker_key_rather_than_acting` ×10, `test_C2`. **R25-E reproduced exactly** |
| JRB | truncation reinstated in the recorder **by a different spelling** — `d = d.split(MARKER_SEP, 1)[0]` | **KILLED — `3 failed, 619 passed`.** `test_JR23_a_PHASE_CHOSEN_tab_name…` ×2 shapes, `test_C2`. **`test_JR23_the_STRUCTURE_WALK_records_the_name_it_was_given` did NOT fire.** Compare star-lord's R25-A (same defect, spelled `marker_path`): 4 net, both rows. **JR-28** |
| JRC | `_read_only_hit` loses its ancestor arm (the fail-closed premise) | **KILLED — `4 failed, 618 passed`.** `test_JR12_…` ×2, `test_a_collapsed_entry_ABOVE_a_read_only_tree_breaches`, `test_C2`. Premise pinned; no finding |
| JRD | `unreadable_marker` effectively placed **before** `git_internal` | **KILLED — `11 failed, 611 passed`, FAILED list byte-identical to JRA.** Ordering pinned by the same row. star-lord's counterfactual confirmed |

**Probes** (separate copy, `permissions.py` sha256-verified against `git show HEAD:` before each; both fenced shapes throughout):

- **P1** — phase-chosen tab-named **directory** in a read-only tree, at HEAD. Receipt, disk state, guard, reason.
- **P2** — phase-chosen tab-named **file** (created) and tab-named **tracked file** (modified), at HEAD **and at `e6a57cc5`** (one commit before the JR-23 fix). The differential is JR-27.
- **P3** — a **genuine** `structure_dirs.onerror` mint (`chmod 000` on a committed directory in a read-only tree), at HEAD. Confirms the legitimate half of the new guard fires and its reason is true there.

---

## 4. Open findings — the declared debts

### 4.1 JR-27 — the `unreadable_marker` guard is keyed on the STRING, and is over-broad by one whole arm. **WARN.**

**What I found.** The guard added by `9be3c525` fires on `MARKER_SEP in change.path` (`permissions.py:1693`) for *every* change kind. Its reason asserts three things:

> "this key carries a measurement marker — **the path could not be read when the tree was fingerprinted**, so **what stands at it now is unknown**, and **the text after the `'\t'` is the measurement's own note rather than part of the name**"

For a phase-chosen name all three clauses are false: the path was read normally, what stands there is a directory or file the phase created, and the text after the tab *is* part of the name.

**In the entries arm the reason is false one hundred per cent of the time, and that is provable rather than probable.** I read all six marker mint sites. Every key that can enter `TreeFingerprint.entries` bearing a marker is minted by `_resolve_gitdir_pointer` (`:794`, `:797`, `:803`), `_resolve_commondir` (`:818`, `:824`) or `_gitdir_control_entries` (`:728`, `:748`, `:761`, `:775`), and every one of those is `.git`-prefixed — the only prefixes ever passed in are `".git"` (`:879`, `:892`) and `".git/\t<common>"` (`:890`). All of them are therefore taken by the `git_internal` guard, which truncates, one guard earlier. JRA and JRD both confirm that ordering is real and pinned. **So an entries-arm change reaching `unreadable_marker` can only ever be a phase-chosen name, and the guard's stated reason can never be true there.**

The structure arm is different and the guard is right there: P3 shows a genuine `structure_dirs.onerror` mint (`'protected/locked\t<unreadable: Permission denied>'`, `after_status='structure'`) reaching `unreadable_marker` with a reason that is entirely true.

**The measured behaviour change.** Same probe, at HEAD and at `e6a57cc5` (the commit immediately before the fix), both fixture shapes:

```
                                              e6a57cc5              b8c0311c
phase CREATES  protected/evil\tx.txt          action='deleted'      NOT_ROLLED_BACK
                                              on disk: False        on disk: True   guard='unreadable_marker'

phase MODIFIES protected/tracked\tname.md     action='restored'     NOT_ROLLED_BACK
  (tracked, committed, in a read-only tree)   content: BASELINE     content: PHASE OVERWROTE THIS
```

One commit ago the rollback removed the created file and restored the overwritten committed content, correctly, in a read-only tree. It no longer does either, and a phase selects that outcome by putting a tab in a filename. The first half of the JR-23 fix (the recorder) touches only structure entries — star-lord notes correctly that "the **entries** arm never truncated" — so this is entirely the second half's doing.

**Why this is WARN and not BLOCK, stated so a later reader can regrade rather than guess.** The wall's contract for the undo is explicit and is not "the artifact is always removed":

> `test_the_wall_reports_the_undo_honestly_for_every_artifact_kind` (`test_containment_wall.py:757`): *"NOT 'the artifact is always removed' — that is not the contract and should not be … What must never happen is the third state: the artifact survives and the receipt says `deleted`."*

Under that contract the new behaviour is compliant. The change is detected, classified as a breach, named on the receipt under its true name, copied to quarantine, and the run aborts. Nothing escapes the receipt, which is the property my r19 BLOCK criterion is about, and which JR-18 and JR-22 both violated. Furthermore I graded the structurally identical `.git\tevil` residual at r21 § 5 as WARN and endorsed star-lord's lesser grading of it; grading this BLOCK would be inconsistent with my own precedent one round earlier.

**What would make it BLOCK, for whoever holds this next.** If the founding run's abort path is ever treated as *restorative* rather than *evidentiary* — i.e. if any operator, script or later phase relies on "the rollback returned the read-only trees to their pre-phase state" — then a phase-selectable, silently-false exemption from that guarantee is a fail-open and this is a BLOCK. In the shipped `kc2-baton-mechanical.yaml` every phase carries `writes: []`, so **every** phase write is a breach and the rollback is the only thing that cleans up; that raises the stakes without changing the contract as written.

**Both discriminators the guard needs already exist in the data, unused.**
- `change.after_status == "structure"` — set by the recorder at `permissions.py:1271` (`Change(after.root, path, kind, None, "structure")`) and confirmed live in P3. It separates the entries arm from the structure arm exactly, and the entries arm is the one where the guard can never be right.
- Within the structure arm, where star-lord's "cannot distinguish a mint from a phase-chosen name" argument does hold *for the string*, it does not hold *for the path*: a mint's literal key never exists on disk and a phase-chosen directory always does. `lexists` answers it, and the rollback is about to stat the path anyway.

This is the JR-18 lesson one step further than star-lord took it. JR-18: *the direction of a match is a property of the caller, not of the key.* JR-27: *the provenance of a key is a property of the site that minted it, and it must travel as data rather than be re-derived from the string.* The recorder already knows; nothing carries it.

**Why 622 rows cannot see it.** `ARTIFACT_KINDS` (`test_containment_wall.py:289`) is an enumeration of 21 adversarial artefact kinds, added to over seven rounds, and it explicitly includes `path_with_a_newline`, `quoted_path_with_rename_delimiter` and `pathspec_magic_name` — names chosen because a phase can choose them. **There is no tab-named kind**, and the tab is the single character this whole JR-5 → JR-18 → JR-23 thread is about. Five rows parametrise over `sorted(ARTIFACT_KINDS)` (`:708`, `:738`, `:757`, `:817`, `:862`) across two shapes, so a `path_with_a_tab` entry would have put ten rows through detect/classify/rollback/receipt and the `deleted`→`NOT_ROLLED_BACK` transition would have surfaced as a red at the moment it was introduced. It went in unmeasured instead.

**Action for whoever takes this.** Two separable pieces: (a) narrow the guard so it cannot fire where its reason cannot be true, or reword the reason so it states the undecidable thing rather than one branch of it; (b) add a tab-named kind to `ARTIFACT_KINDS`. (b) is cheap, is where the coverage gap actually is, and would have caught (a). Whoever does (a) should measure it with the P2 differential above, not with a synthetic key.

**References:** `permissions.py:1693–1707` (the guard), `:1661–1676` (`git_internal`, before it), `:728/:748/:761/:775/:794/:797/:803/:818/:824` (the entry mints, all `.git`-prefixed), `:879/:890/:892` (the only prefixes passed), `:644` (the structure mint, the guard's legitimate subject), `:1271` (`"structure"`, the unused discriminator), `:380–385` (`Change`), `test_containment_wall.py:289` (`ARTIFACT_KINDS`), `:757` (the undo contract).

### 4.2 JR-28 — a row that pins a spelling and reports itself as pinning a behaviour. **WARN.**

`test_JR23_the_STRUCTURE_WALK_records_the_name_it_was_given` (`test_containment_wall.py:2605`) locates the structure-walk section by its own comment and asserts no line in it contains `marker_path(`. Its docstring states its purpose as: *"holds the direction at the unit, so a future edit that reinstates the truncation reds here with the reason rather than reds in a scene three layers away."*

Measured, mutation JRB — the JR-23 defect reinstated with `marker_path`'s own body inlined, `d = d.split(MARKER_SEP, 1)[0]`:

```
JRB   raw  3 failed, 619 passed
      test_JR23_a_PHASE_CHOSEN_tab_name_cannot_make_the_rollback_act_on_a_NEIGHBOUR ×2 shapes
      test_C2
```

**The structure-walk row did not fire.** Compare star-lord's R25-A, the identical defect spelled `marker_path(d)`: 4 net, both rows. So the row's discriminating power is over the *spelling*, and its docstring's promise — that a reinstatement reds here with the reason rather than in a scene — is false for the most natural reinstatement.

**This is not a coverage hole.** The scene row catches the behaviour in both shapes and in both spellings, so the JR-23 fix is genuinely pinned. It is a claim defect: a row that says what it does not do, in the file whose subject is claims naming what they are about.

It is also worth naming the class, because it is JR-24's own finding reproduced inside the row written to close JR-23. JR-24 was: *`_module_vocabularies`' container filter is keyed on a spelling, so a vocabulary written in an unrecognised shape leaves the denominator silently.* JR-28 is the same predicate error one file over. The generalisable form: **a source-text assertion is a claim about a spelling; if the docstring states it as a claim about a behaviour, the row is a claim that names the wrong subject.** The repair is either to reword the docstring to what the row does, or to give the source assertion the same third-exit treatment `_classify_module` just received — anything in the walk it cannot classify reds by existing.

**References:** `test_containment_wall.py:2605–2653`; `permissions.py:1229–1271`.

### 4.3 JR-29 — a dominated assertion, and what the reach tracer cannot see. **INFO.**

`test_JR23_truncation_is_FAIL_CLOSED_at_the_two_sites_that_keep_it` (`:2656`) builds each key as `f"{base}{MARKER_SEP}{m}"` and asserts, in order:

```python
assert key.startswith(got)   # the PREFIX property — the row's stated subject
assert got == base           # first-separator splitting
```

Over every sample in the row, the second implies the first: if `got == base` and `key == base + SEP + m`, then `key.startswith(got)` is true by construction. **There is no input in the row on which the prefix leg fails and the equality leg passes**, so the prefix leg cannot discriminate any mutant the equality leg does not already kill. star-lord's own R25-C and R25-D are both equality-leg kills, consistent with this.

Three consequences, in increasing order of interest.

1. The row's title and docstring rest the entire fail-closed argument on prefix-ness, and prefix-ness is the leg with no independent discriminating power. What actually holds the row is `got == base` and, as star-lord correctly says, the single adversarial sample `"a\tb"` — a marker whose own text contains the separator. Their own warning that "a later editor tidying the sample list would silently disarm it" is the accurate description of this row's strength, and it is more accurate than the docstring's.
2. The row's name claims a property of *two call sites* and its body asserts a property of *one function*. The call-site premise (bidirectional matching at `_read_only_hit`) is real and is pinned — JRC, KILLED at 4 — but by JR-12 and `test_permissions.py`, not here. Worth a pointer in the row so the next reader does not have to run JRC to find out.
3. **The general observation, and the reason this is worth writing down at all.** `test_C2_every_assert_under_tests_is_proven_to_execute` proves the prefix leg *runs*. It does. Rule 44's subject is an assert that never executes; this is an assert that always executes and can never fail. **The reach tracer answers "did this assertion run?" — an adjacent question to "could this assertion have failed?" — and its wrong answer looks safe.** That is this ladder's own recurring defect shape, arriving in the instrument built to catch it. I am not asking for a tool; I am naming the gap so that "test_C2 is green" is never read as "no leg is inert."

**References:** `test_containment_wall.py:2656–2709`; `test_reach_audit.py::test_C2`.

### 4.4 JR-30 — rule 50c is right, and one notch narrow. **INFO.**

> **50c.** A fix that ships with its own row must be killed **by that row**. A kill by some other row is not credit — it is a mutation that missed and landed somewhere already defended. Name the expected killer before running, and reconcile.

Correct, well-evidenced, and R25-F is a genuine instance honestly self-surfaced. Three refinements, none of them a rejection.

1. **The scope is narrower than the diagnosis.** The rule is written for "a fix that ships with its own row." The finding it generalises — *the receipt's verdict column was right and its attribution was not* — is true of **every** mutation, including ones aimed at long-standing code with no new row in play. R25-F happened to be a fix-row case; nothing in the mechanism requires that. Stated as *every mutation names its expected killer* the rule covers the same case and the one it currently misses.
2. **"A kill by some other row is not credit" is one notch strong.** It is credit to the *suite* and none to the *row*. The distinction matters, because "the behaviour is defended" and "my new row defends it" are two different facts and a reader dropping the first loses real information — which is precisely rule 50a's point, run the other way.
3. **The genuinely new content is pre-registration, and 50c buries it in the last sentence.** *Name the expected killer before the mutation runs* is a discipline about ordering, and it is the part that cannot be recovered after the fact. The reconciliation half is largely derivable from 50a: had the neutralised run been taken first for R25-F, as 50a already prescribes and as star-lord did do for R24-A, the mutation would have killed with the new row absent and the miss would have been visible immediately. So R25-F is at least as much a 50a application failure as a 50c-shaped gap. Leading 50c with pre-registration would put the irreducible part first.

Rules 50a and 50b I have nothing against; 50b in particular is correct and its correction of my own JR-26(c) is right — I called that missing row rule 44's signature and it is a deleted parametrised case, which is a different failure with an opposite mechanism.

### 4.5 JR-7 INFO rider — still open, still correctly deferred. **INFO, carried.**

The benign `ToolSearch` control. Gated on the agentic lane opening; the agentic lane is HOLD; nothing has changed and nothing should have. Carried into the landing declaration unresolved and undamaged.

---

## 5. Prior-finding disposition — CLOSED / NOT CLOSED

| finding | round raised | state at close | basis |
|---|---|---|---|
| **JR-7** (INFO rider — benign `ToolSearch` control) | 7 | **NOT CLOSED.** Correctly deferred, gated on the agentic lane. Carries as a declared debt | Unchanged since round 17 |
| **JR-18** (writes-allowlist escape) | 21 | **CLOSED** | Verified round 22 live (P1) and by mutation (R22-K/L/M). Both alternatives correctly rejected |
| **JR-18b** (falsification partner) | 21 | **CLOSED** | The leg is present and it is the leg that refutes the fix I offered |
| **JR-19** (admission reasons) | 21 | **CLOSED** | R22-G/H/I. I was wrong on the substance and said so at round 22 |
| **JR-20** (rule 47's second axis) | 21 | **CLOSED** | Denominator re-derived by walking every module; classifier holes carried into JR-24 and closed there |
| **JR-21** (misattributed figure) | 21 | **CLOSED** | `GIT_NESTED_GITDIRS` at round 21; `GIT_CONTROL_PATHS` carried into JR-25 and closed there |
| **JR-22** (`FACTORY_RUNTIME_PATHS` spent as a PREFIX) — *my round-21 BLOCK* | 22 | **CLOSED.** This is the finding the mechanical BLOCK stood on | Repaired stronger than I proposed: split into `FACTORY_RUNTIME_FILES` (exact) + `FACTORY_RUNTIME_DIRS` (prefix), `exempted` reaches the receipt as a refutable sentence. **Verified this round by walking the vocabulary denominator: both names are present and the 15→16 delta is exactly this split** |
| **JR-23** (the un-audited `marker_path` call sites) | 22 | **CLOSED as to the NAME axis and the K1/L1 damage class. NOT CLOSED as to the CLAIM axis** — carried forward as **JR-27** | Damage class closed, measured in both shapes: the untracked neighbour survives and the artifact is named. Regrade WARN → BLOCK accepted; my WARN rested on a guard the phase can switch off |
| **JR-24** (the classifier's two exemptions) | 22 | **CLOSED** | Third exit present, adjudication list live with three entries, denominator walked from the package. Walk figures re-derived by me: 4/15 at `7bbba6fb`, 21/16 at HEAD, `sessions/` hazard real (10 quarantined `.py` in the live tree). Both arms measured by star-lord (R25-H/I); I did not re-run those |
| **JR-25** (rule 47's misattributed figure) | 22 | **CLOSED** | Seven figures, one per member, each naming its member. I verified the corrections landed at both sites; **I did not re-measure the seven figures this round** and say so rather than imply coverage I do not have. Their ledger-id collision point is well made and the `jr/R21-H` prefix proposal is adopted |
| **JR-26** (three precision items) | 22 | **CLOSED, all three** | (a) is rule 50a; (b) R22-H/I recorded and credited; (c) **correctly refuted** — the missing row is a deleted parametrised case, not rule 44's signature. My diagnosis was wrong and theirs is right |
| **JR-27** (`unreadable_marker` keyed on the string) | 25 | **OPEN — WARN.** Declared debt | § 4.1 |
| **JR-28** (the structure-walk row pins a spelling) | 25 | **OPEN — WARN.** Declared debt | § 4.2 |
| **JR-29** (a dominated assertion; the reach tracer's adjacent question) | 25 | **OPEN — INFO.** Declared debt | § 4.3 |
| **JR-30** (rule 50c's scope) | 25 | **OPEN — INFO.** Declared debt | § 4.4 |

Every finding I raised across rounds 18–24 that was actionable by star-lord is **CLOSED**, and closed with measurements I could reproduce. That is the sentence I want on the record for the landing.

---

## 6. Clause 1's counter, since it is Matt's to rule on and this is the last chance to inform it

star-lord records this round as "one fail-open (JR-23), so it stays at 0 — five consecutive rounds of exactly one." I would state it differently now, and the difference matters for how the counter is read after the ladder closes.

- Rounds 18–24 each found exactly one *reachable fail-open in a containment predicate*: JR-5, JR-13/15, JR-18, JR-22, JR-23. Five, and the rate did not fall.
- **Round 25 found none.** JR-27 is a false refusal reason plus an unmeasured reduction in undo coverage; JR-28 is a claim defect in a row; JR-29 and JR-30 are precision. Nothing this round lets a phase write escape the receipt.
- That is the first round in six with no fail-open, and it is one data point, not a trend. I record it as a data point.

What five rounds of one-each actually established, and I said this at round 21 and still hold it: **the lane was not converging on "no defects", it was converging on "one predicate per round answering an adjacent question whose wrong answer looks safe."** JR-27, JR-28 and JR-29 are all that same shape at lower severity — a guard keyed on a string instead of a provenance, a row keyed on a spelling instead of a behaviour, a tracer keyed on execution instead of falsifiability. **Clause 1 is better written about class coverage than about clean rounds**, because the class is what recurs and a clean round is what a narrow instrument produces. That is a recommendation to Matt, not a ruling, and it is the last one I will make on this ladder.

---

## 7. My own instrument, and what I got wrong across the ladder

Recorded per rule 48, because a reviewer's errors belong on the receipt with everyone else's.

- **Round 20: I published an unmeasured claim as a measurement** (*"and the suite stays at 604"*), in a verdict whose central complaint was a row stating a claim without entering its predicate. Measured at round 22: `3 failed, 600 passed`. star-lord built a mechanism partly on that sentence. The mechanism is worth keeping; my justification for it was not evidence.
- **Round 21: a scope claim one notch strong** ("named nowhere by literal or by derivation"). Two rows, not one. star-lord caught it.
- **Round 22: JR-23 graded WARN on a guard the phase can remove.** star-lord's regrade to BLOCK is correct. My reproduction planted the *tracked* neighbour — the half `destroyer` already protects — which is exactly the error I charged the wall's canary with in the same verdict. I made the wall's mistake in the finding about the wall's mistake.
- **Round 22: I predicted `_read_only_hit` was the unasserted call site.** Refuted by R24-B at 9 failed, and independently by my own JR-C this round at 4. Right about the class, wrong about the member.
- **Round 22: JR-26(c) misdiagnosed.** I called the missing row rule 44's signature; it is a deleted parametrised case. star-lord's correction is right and produced rule 50b.
- **What went right by design, all five rounds:** the live tree was never mutated. Every mutation in a disposable copy from a blob-verified reference, digest-stable across the run, no restore step to get wrong. The r20 § 5 hazard is not guarded against in my harness — it is absent from it.

---

## 8. Not adjudicated — carried to the landing declaration for Matt / gandalf

- **The three-clause stopping rule and the lane split.** Matt's. § 6 is my last input.
- **v1 containment posture** (base-names-only, pre-hoc). Matt's.
- **The threat-model boundary**, including rule 39's tension with unscoped `Bash`. gandalf's and Matt's, and the agentic lane's critical path. Unchanged rounds 17–25.
- **JR-7's INFO rider.** Gated on the above.

---

## Action

- [x] **star-lord:** JR-18, JR-18b, JR-19, JR-20, JR-21, JR-22, JR-23 (name axis), JR-24, JR-25, JR-26 — all CLOSED. No further action; the ladder is closed and nothing here routes back.
- [ ] **gandalf (SB-1 § 4 fallback + D5 revisit):** disposition of **JR-27 (WARN)**, **JR-28 (WARN)**, **JR-29 (INFO)**, **JR-30 (INFO)**, and the carried **JR-7 INFO rider**. Each is stated in § 4 with its measurement, its references, and what would change its grade, so it can be actioned without me.
- [ ] **Matt:** ratify or amend the three-clause stopping rule. § 6 recommends clause 1 be written about class coverage rather than clean rounds, and records that round 25 is the first round in six with no fail-open — one data point, not a trend.
- [ ] **Matt / gandalf:** the threat-model boundary. Unchanged from rounds 17–25; the agentic lane cannot leave HOLD without it.

## References

- `agentic_orchestration/factory/permissions.py` — `:1178–1280` (`diff_fingerprints`, the JR-23 recorder fix), `:1271` (the `"structure"` discriminator, unused by the guard), `:1283–1332` (`_matches`, JR-18), `:1335–1369` (`_read_only_hit`; ancestor arm at `:1367`, JRC), `:1661–1676` (`git_internal`), **`:1693–1707` (`unreadable_marker` — JR-27)**, `:580–605` (`marker_path`), `:644` (the structure mint), `:728/:748/:761/:775/:794/:797/:803/:818/:824` (the entry mints, all `.git`-prefixed — JR-27), `:879/:890/:892` (the only prefixes passed), `:428–437` (`REFUSAL_GUARDS`), `:380–385` (`Change`)
- `agentic_orchestration/factory/tests/test_containment_wall.py` — `:289–321` (`ARTIFACT_KINDS`, **no tab-named kind** — JR-27), `:708/:738/:757/:817/:862` (the five parametrised rows), `:757` (the undo contract), `:2317–2341` (`test_JR5_the_rollback_REFUSES_a_marker_key…`, the row that preserves R25-E — `:2340` is the guard-name leg), `:2501–2602` (the JR-23 scene row), **`:2605–2653` (the structure-walk row — JR-28)**, **`:2656–2709` (the property row — JR-29)**
- `agentic_orchestration/factory/tests/test_vocabularies.py` — `:71–95` (`_RUNTIME_SUBTREES`, the `sessions/` exclusion), `:98–115` (`_adjudicated_modules`, the walk), `:172–186` (`REFUSAL_GUARDS` pin, the `unreadable_marker` adjudication), `:318–350` / `:353+` (the two JR-24 rows)
- `agentic_orchestration/factory/README.md` — rules 47, 48, 49, 50, **50a `:849`**, **50b `:861`**, **50c `:874` (JR-30)**
- `agentic_orchestration/factory/workflows/kc2-baton-mechanical.yaml` — `:22` (`root:`), `writes: []` on every phase (§ 4.1, the stakes clause)
- `agentic_orchestration/star-lord/notes/2026-08-11-factory-spine-gate2-round-24-return.md` — the return under review
- `agentic_orchestration/star-lord/notes/2026-08-10-factory-spine-gate2-fixes.md` — §§ 27.1–27.11, the working record; §§ 27.9 and 27.11 are the ledgers
- `agentic_orchestration/qa/pending/2026-08-11-star-lord-factory-spine-gate2-r21.md` — my round-22 verdict, which this closes
- Measurement harness and pristine reference: `/tmp/jr25/mutate.py`, `/tmp/jr25/ref` (extracted from `git archive b8c0311c`, blob-verified). Mutation trees were destroyed after each run.
