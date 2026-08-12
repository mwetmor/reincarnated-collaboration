# Factory spine — LANDING DECLARATION

**Author:** star-lord · **Date:** 2026-08-11 · **Tree:** `agentic_orchestration/factory/`
**Authority:** Matt's closing directive — *land the round-24 return plus jack-ryan's verdict on it, then close the ladder regardless of verdict outcome; no round 25. If the verdict re-opens the mechanical lane, do not fix it — record the finding and close anyway; disposition moves to gandalf (SB-1 § 4 fallback + D5 revisit).*
**Build contract:** `agentic_orchestration/gandalf/notes/2026-08-10-factory-spine-spec.md`, ruling D4 (star-lord builds; gandalf DRIFT-CRITIC on landing; jack-ryan Gate-2 before the first compiled workflow)
**Closing verdict:** `agentic_orchestration/qa/pending/2026-08-11-jack-ryan-factory-spine-gate2-r25-CLOSING.md`

This file is the state of record at close. It is written to be read by someone who was
not here, six months from now, with none of us available.

---

## 1. Lane states

### Mechanical lane: **LIFT**

jack-ryan, Gate-2, round 25. The BLOCK the mechanical lane stood on was **JR-22**
(`FACTORY_RUNTIME_PATHS` spent as a prefix, so a phase-chosen filename made a root-repo
write invisible to the fingerprint). It is closed, repaired stronger than proposed —
split into `FACTORY_RUNTIME_FILES` (exact match) and `FACTORY_RUNTIME_DIRS` (prefix),
with `exempted` reaching the receipt as a refutable sentence — and the closure was
verified by the reviewer independently, not accepted on my report.

**What LIFT means here:** no finding at close lets a phase write escape detection,
classification, the receipt, or the abort. That is the criterion the lane's BLOCK
criterion was written about, and it is met.

**What LIFT does not mean:** it is not "no defects". Four findings are open below, two
of them WARN, and one of those (JR-27) is a behaviour regression I introduced in this
final round. LIFT is a statement about the containment guarantee, not about the tree.

### Agentic lane: **HOLD** — clause 2 only, unchanged since round 17

**Declared state.** The agentic lane has never opened and is not opening here. It is
blocked on the **threat-model boundary**, which is gandalf's and Matt's to draw and is
not star-lord's to decide. Rule 39's tension with unscoped `Bash` sits inside that
question. Nothing in rounds 17–25 changed the boundary, and no amount of mechanical-lane
work can lift this — the gate is a design decision, not a defect.

Everything gated on it stays gated, explicitly: **JR-7's INFO rider** (the benign
`ToolSearch` control) is carried unresolved and undamaged, which is the correct state
for it.

---

## 2. Suite, and what was measured

| | |
|---|---|
| **Suite at close** | **622 rows, green** |
| Command | `python3 -m pytest factory/tests -q --no-header -p no:randomly`, run from `agentic_orchestration/` |
| Independently reproduced | Yes — jack-ryan, round 25, in a tree extracted from `git archive` and blob-verified against HEAD |
| Trajectory across the ladder | 604 → 611 → 617 → **622** |
| Head commit at close | `b8c0311c` |

**Mutation record.** The standing method mandate for the whole ladder was *a mutation per
fix; verify each new row kills its own mutation; keep the suite green; commit.* The final
round ran fifteen mutations across two batteries (`R24-A…D`, `R25-A…G`, `R25-H…K`); all
killed except `R24-A`, whose **survival was the finding**. Ledgers with raw pytest lines
are at `../star-lord/notes/2026-08-10-factory-spine-gate2-fixes.md` §§ 27.9 and 27.11.

---

## 3. Founding-run receipts

The factory's founding run is **`kc2-baton-mechanical`** — the KC2 baton scene build,
mechanical lane, three phases.

| | |
|---|---|
| Workflow | `kc2-baton-mechanical.yaml`, digest `090247019ba6…` |
| Phases | 3/3 green — `baton_digest_pin`, `render_ffprobe_verify`, `baton_test_wall` |
| Gate verdicts | 15, all PASS |
| Sessions recorded | 78, of which **73 PASS** |
| Latest receipt of record | `kc2-baton-mechanical-20260811T115024Z-361afd` |
| Earliest | `kc2-baton-mechanical-20260810T225204Z-944554` |
| Baton pinned | `kc2-baton-v1-E-s09-cp150-20260809_052836.json` at `d7ecd866ac45…`, 1,065,632 B |
| Render verified | `BR2W_C9.mp4` — 40.37 s, streams `['video', 'audio']` |
| Usage | **NULL — no model was invoked.** Every phase is mechanical |

Receipts live in `sessions/<run-id>/` (`run_report.md`, `workflow.snapshot`, `prompts/`,
`seal/`, `breach/`, `context_handoff/`) and are views over `receipts.db` — one data path.

**Read the NULL honestly.** The founding run cost nothing in tokens because no lane was
priced, not because pricing was solved. **O4 (dollars) is unanswered, and it is unanswered
*because* the agentic lane never opened.** Any future reading of these receipts as
evidence about cost would be reading an empty column as a low number.

---

## 4. Declared debts

Nothing below routes back to star-lord. Per the closing directive, disposition passes to
**gandalf** (SB-1 § 4 fallback + D5 revisit). Each is stated in the closing verdict with
its measurement, its file references, and what would change its grade.

| id | sev | one line | owner | detail |
|---|---|---|---|---|
| **JR-27** | **WARN** | The `unreadable_marker` guard is keyed on the **string**, not on provenance; in the entries arm its stated reason can never be true, and a phase can exempt itself from rollback by putting a tab in a filename | gandalf | verdict § 4.1 |
| **JR-28** | **WARN** | `test_JR23_the_STRUCTURE_WALK_records_the_name_it_was_given` pins a **spelling** while its docstring claims it pins a **behaviour** | gandalf | verdict § 4.2 |
| **JR-29** | INFO | A dominated assertion leg in the property row — it executes but cannot fail; `test_C2` proves reach, not falsifiability | gandalf | verdict § 4.3 |
| **JR-30** | INFO | README rule 50c is right but scoped one notch narrow (fix-rows only, when the diagnosis covers every mutation) | gandalf | verdict § 4.4 |
| **JR-7** | INFO | The benign `ToolSearch` control rider — correctly deferred, **gated on the agentic lane opening** | gandalf / Matt | verdict § 4.5 |

### JR-27 in full, because it is mine and it is a regression

I introduced it in this final round, in the second half of the JR-23 fix, and jack-ryan
found it. It deserves to be stated plainly rather than compressed into a table row.

The guard fires on `MARKER_SEP in change.path` (`permissions.py:1693`) for **every**
change kind, above the created/modified/committed verbs. Its reason asserts the path
could not be read when the tree was fingerprinted. For a phase-chosen tab name all of
that is false — the path read fine, and the text after the tab *is* part of the name.
Every marker-minting site that can reach `TreeFingerprint.entries` is `.git`-prefixed and
is taken by `git_internal` one guard earlier, so **an entries-arm change reaching this
guard can only ever be a phase-chosen name.**

Measured, against `e6a57cc5` (immediately before the fix):

```
                                          e6a57cc5           b8c0311c (HEAD)
phase CREATES  protected/evil\tx.txt      deleted            NOT_ROLLED_BACK, survives
phase MODIFIES protected/tracked\tname.md restored           NOT_ROLLED_BACK, overwrite stands
```

Graded WARN because the wall's undo contract is explicitly *not* "the artifact is always
removed" — the change is still detected, classified as a breach, named truthfully on the
receipt, quarantined, and the run aborts. **It becomes a BLOCK the moment anyone treats
the abort path as restorative rather than evidentiary.** In the shipped
`kc2-baton-mechanical.yaml` every phase carries `writes: []`, so every phase write is a
breach and the rollback is the only cleanup — that raises the stakes without changing the
contract as written.

Both discriminators the guard needs already exist in the data and are unused:
`change.after_status == "structure"` (set at `permissions.py:1271`) separates the two arms
exactly, and within the structure arm `lexists` separates a mint from a phase-chosen name,
because a mint's literal key never exists on disk.

**The cheap repair is the coverage gap, not the guard.** `ARTIFACT_KINDS`
(`test_containment_wall.py:289`) enumerates 21 adversarial artefact kinds — including
`path_with_a_newline`, `quoted_path_with_rename_delimiter`, `pathspec_magic_name` — and
has **no tab-named kind**, though the tab is the single character the entire JR-5 → JR-18
→ JR-23 thread is about. Five rows parametrise over it across two shapes; a
`path_with_a_tab` entry would have put ten rows through detect/classify/rollback/receipt
and reddened at the moment I introduced this.

---

## 5. Open questions that are not debts — they are Matt's and gandalf's

Carried unresolved, by design, and named so nobody mistakes silence for closure:

- **The three-clause stopping rule, and the mechanical/agentic lane split.** Matt's.
  jack-ryan's last input (verdict § 6): rounds 18–24 each found exactly one reachable
  fail-open; round 25 found none, which is *one data point, not a trend*. Their
  recommendation is that **clause 1 be written about class coverage rather than clean
  rounds**, because the class is what recurs and a clean round is what a narrow
  instrument produces. I hold no position on this; it was never mine.
- **The v1 containment posture** (base-names-only, pre-hoc). Matt's.
- **The threat-model boundary.** gandalf's and Matt's. The agentic lane's critical path.
- **O4 (dollars)** — unanswered, and § 3 explains why the receipts cannot answer it.
- **D-10 (no HALT status)** — open.

---

## 6. What the ladder actually established

Twenty-five rounds. The finding that recurred was never a category of bug — it was a
**shape**:

> *A containment predicate that answers a slightly different question than the one asked,
> whose wrong answer is the safe-looking one.*

It arrived twenty-plus times and it never stopped arriving. It arrived in the product (a
matcher's question asked of a recorder; an exempt file forgiven by its prefix; a guard
keyed on a string instead of a provenance). It arrived in the **tests** (a canary keyed on
the same fact as the guard it audits — so the net was strung across the half that was
already safe). It arrived three times in the **measuring instrument** itself (a receipt
that asked "did anything fail?" instead of "which rows failed?"; an assert that was
present but never executed; a precondition that asked "was the tree clean at the start?"
instead of "was it stable throughout?"). And in the last round it arrived in the
**prose** — I compared two vocabulary counts taken over different denominators and called
the difference the reviewer's error, inside the note explaining the fix.

The durable output is the rule set in `README.md` (rules 13, 28, 29, 39, 44–50, 50a–50c),
each of which is a measurement someone got wrong first. The two from the final round:

- **50a** — re-run the *reviewer's* mutation after your own fix, and take the neutralised
  run first, because a fix can decouple a ledger row from what used to kill it.
- **50c** — a fix that ships with its own row must be killed **by that row**; a kill by
  some other row is not credit. `KILLED :: 2 failed` is exactly what success looks like,
  which is why a missed mutation hides inside a green receipt.

Both reviewers' errors and mine are on the record, in the verdict § 7 and in the working
notes § 27 respectively. That was the point.

---

## 7. Handoff

- **star-lord:** JR-18, JR-18b, JR-19, JR-20, JR-21, JR-22, JR-23 (name axis), JR-24,
  JR-25, JR-26 — **all CLOSED**, each with a measurement the reviewer reproduced. No
  further action. **The ladder is closed.**
- **gandalf:** JR-27, JR-28, JR-29, JR-30, and the carried JR-7 rider. Also the drift
  review that ruling D4 owes on landing.
- **Matt:** the stopping rule; the containment posture; the threat-model boundary with
  gandalf; O4; D-10.

The mechanical lane is **LIFT**. The agentic lane is **HOLD**. The suite is **622 green**.
The founding run is on the record with 73 passes and a NULL cost column that means
"unpriced", not "free".
