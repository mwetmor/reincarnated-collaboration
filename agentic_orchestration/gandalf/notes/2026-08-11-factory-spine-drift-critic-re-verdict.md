# Factory spine — DRIFT-CRITIC **RE-VERDICT** on the final state

**Date:** 2026-08-11 · **Author:** gandalf (DRIFT-CRITIC, sub-agent)
**▶ ROLE: DRIFT-CRITIC** — judging a build against a spec, and the spec is mine.
**⚠ SWITCH: SPEC-AUTHOR → DRIFT-CRITIC.** I wrote Spec A; I am judging its build.
**Second seam, declared because nobody else will:** I am also SB-1's RUN-CONDUCTOR, and this
verdict is SB-1's launch gate. A conductor grading the tooling his own run depends on has an
interest in passing it. The conditions below are written so that interest is visible and
falsifiable rather than quiet.

**Under review:** `agentic_orchestration/factory/` — code head `b8c0311c` (2026-08-11T20:11:15
-04:00); tree head `e386f529`, which I verified touches **only** `LANDING.md`
(`git diff --name-only b8c0311c e386f529 -- agentic_orchestration/factory/` → one path). Working
tree clean for `factory/`.
**Against:** `gandalf/notes/2026-08-10-factory-spine-spec.md` (Spec A), folding
`gandalf/notes/2026-08-10-factory-spine-drift-critic.md` (v1, `4ba09ff0`, FAITHFUL WITH DRIFT at
136 green) and rounds 1–25.
**Suite, my own run:** `622 passed in 172.68s` — `python3 -m pytest factory/tests -q --no-header
-p no:randomly` from `agentic_orchestration/`. jack-ryan's independent figure in a blob-verified
`git archive` tree: `622 passed in 185.71s`. Two instruments, one count.

---

## 0 · Top line

**Verdict vs Spec A, mechanical lane: FAITHFUL-WITH-DRIFT.**
Every law in §§ 2, 3, 4, 6, 8, 9 is compiled, and § 8 is now compiled materially harder than I
specified — but three v1 drift items (D-2, D-5, D-9) are open unchanged, a fourth (D-13) is new
below, and the O4 ruling was never executed. None of it touches the containment guarantee the
lane's LIFT is about, which is why this is drift and not DRIFTED.

**SERVICEABILITY for SB-1 § 4: PASS — with one pre-flight condition.**
The lane SB-1 uses is mechanical, it is LIFT, the suite reproduces at 622 on two instruments, and
the four open findings have exposure I measured at zero for SB-1's cell shapes — but **the
founding-run receipts of record were written 12 hours and four containment commits before the
tree that closed the ladder**, so § 11's end-to-end evidence stands against an ancestor. One
read-only re-measurement converts it. Condition C-1, § 5.

---

## 1 · v1 drift register — discharge

| # | v1 finding | State | Evidence |
|---|---|---|---|
| **O4** | Drop `dollars`/`dollars_source`; bump SCHEMA_VERSION 1→2 | **OPEN — CONTESTED, escalated to Matt. NOT executed.** | `usage.py:44-45` and `receipts.py:119-120` still carry both columns. `SCHEMA_VERSION = 3` (`receipts.py:40`) and **the 3 has nothing to do with O4** — v1→v2 is J5b's `agent_sessions` grant columns, v2→v3 is H6's measurement columns (`receipts.py:49-64`). star-lord implemented neither ruling and said why: jack-ryan ruled KEEP, I ruled DROP, two seam stewards opposite (fixes ledger § 6). **Correct handling.** See § 5, D-4 branch |
| **D-1** | Fingerprint blind to gitignored writes in every tree | **CLOSED — stronger than I asked.** I recommended scoping the exemption to `factory/` and using `--ignored=matching` on read-only trees. star-lord went global: `--ignored=traditional` + a recursive stat sweep inside the collapsed dirs (`permissions.py:920-936`), plus a channel I did not name — unreadable dirs arrive on **stderr** with returncode 0 and are folded in as entries (`:941-955`) | |
| **D-2** | No phase-level exec; the only executable primitive is a gate | **OPEN.** `PhaseSpec` still has no `command`/`exec` field (`workflow.py:44-56`). Queued by star-lord as "a shape change, not a fix" (ledger § 6) — I accept that framing. **Mitigation is live and load-bearing:** gate-execution writes are separately fingerprinted and classified (`runner.py:488-500`), so a mutating gate cannot slip its writes past containment | |
| **D-3** | `verdict_consistent` greens vacuously if not last | **CLOSED.** `LAST_GATE` + load error (`workflow.py:35, 174`) | |
| **D-4** | The dollars label asserted, not read | **CLOSED.** `report.py:60-80` reads `dollars_sources` from the DB, glosses each, prints an unregistered source raw, and renders "**provenance unrecorded**; this figure cannot be read as money spent" when none was recorded | |
| **D-5** | `changed_paths` discards repo identity — `diff_matches_claims` is repo-blind | **OPEN, unchanged.** `runner.py:626` is still `changed_paths=[c.path for c in changes]`. `Change.key` (`permissions.py:387-389`) has **zero production callers** — `grep -rn '\.key\b'` across the tree excluding tests and `sessions/` returns nothing. The gate still subtracts bare repo-relative strings (`gates/core.py:163-167`) | |
| **D-6** | Harness names unvalidated at load; `available()` dead | **CLOSED.** `workflow.py:195-201` calls `available()` at load and refuses the phase naming a closed lane | |
| **D-7** | Red phase's notes travel unlabeled | **CLOSED.** Notes now carry phase name + status + "treat them as a lead, not as an established result" (ledger § 5) | |
| **D-8** | `PROTECTED_ALWAYS` root-repo-scoped though spec said "regardless of config" | **CLOSED.** Split: `PROTECTED_EVERY_REPO` breaches in ANY declared repo, root-only entries say which rule they are (`permissions.py:1405-1420`). Found independently as C4 | |
| **D-9** | Determinism is verdict-level, not evidence-level; the banner over-reads | **OPEN, unchanged.** `cli.py:82` still prints `DETERMINISM: EXACT — N gate verdicts identical`, compared on `(phase, gate, status)` (`receipts.py:619-627`). No evidence hash. The banner is what gets quoted three sessions from now; it still reads stronger than what was compared | |
| **D-10** | No HALT status | **OPEN** — declared in LANDING § 5, agentic-gated. Not SB-1-mechanical-relevant: SB-1's owner-eye halts are conductor-held (charter § 6), not spine-expressed | |
| **D-11** | No agentic phase has run end-to-end; envelope round-trip unproven | **OPEN**, agentic-gated. Folds into the D5 revisit | |
| **D-12** | The containment surface the founding run leans on is the weakest | **SUPERSEDED by D-1's closure**, with a new operational cost — see D-14 | |
| **A-1…A-5** | Quiet additions to ride into Spec A's next revision | **OPEN, and it is MY debt, not star-lord's.** Spec A on disk is unamended since 2026-08-10. `on_fail: continue` (A-2) still has no explicit ruling; I rule it here — see § 3 § 9 row | |

### New this pass — continuing the register

**D-13 · The `writes` allowlist is repo-blind, and this is D-5's containment twin. WARN.**
`classify()` matches every change against the flat allowlist with `_matches(change.path, w,
normalise_marker=False)` (`permissions.py:1421-1427`), and `_matches` (`:1283-1332`) has no repo
dimension at all — it fnmatches a repo-relative string. So `writes: ["scenes/**"]`, authored for
the godot tree, authorises `scenes/**` in **every declared repo**, including the meta-repo root.
JR-18 sharpened the *direction* of that match; nobody asked about its *scope*. The founding run
never exercised it (every phase `writes: []`, every measured change-set 0 paths — read the run
report's `diff_matches_claims` lines).
**The mitigation is code-free and available today, and I verified the ordering that makes it
work:** `_read_only_hit` is checked **first**, before the protected lists and before the
allowlist (`permissions.py:1392-1396`). So declaring every non-target repo in `read_only_trees`
converts the cross-repo widening into a breach that fires before the allowlist is ever consulted.
That is a workflow-authoring rule, not a repair. Ruled into SB-1 as condition C-2, § 5.

**D-14 · D-1's fix has a bill, and it comes due the first time a spine phase runs Godot. INFO.**
`.godot/` is gitignored (`reincarnated-godot/.gitignore:52`) and the tree reports **3,288**
porcelain lines under `--ignored=traditional` today. Static ignored files are harmless — a
fingerprint is a before/after diff and they appear identically at both ends. But a phase that
*imports or renders* churns them, and post-D-1 that churn is now **visible, therefore a breach,
therefore an abort**, unless `writes` covers it. This is the fix working as designed; it must be
planned rather than discovered at minute 30. SB-1's charter already routes all Godot cells to
drax outside the spine (§ 7), which keeps godot read-only on the spine's side. Keep it that way.

---

## 2 · Spec-section conformance

| Spec A § | Verdict | Basis |
|---|---|---|
| **§ 2 default-fail runner** | **CONFORMANT — stronger than specified.** No override parameter exists; a second `finish()` is a protocol error; unhandled exception is FAILED-with-traceback; gates can only downgrade. Unweakened across 25 rounds | |
| **§ 3 synced triad** | **CONFORMANT.** Generated from one `_FIELDS` table; `tests/test_envelope_triad.py` holds it. Still the strongest single piece of the build | |
| **§ 4 claim gates, no-stub law** | **CONFORMANT on the law, with the D-2 residual named.** The only `NotImplementedError` in production is `harness/codex.py:27`, declared `HONEST_STUB`; `tests/test_no_stub_gates.py` proves it three ways and the tree-wide `status == FAIL` scan keeps NOT_RUNNABLE from silently greening. **Residual:** `command_succeeds` still executes, so "gates run post-hoc against artifacts on disk" is violated by design for exactly one gate (D-2) — contained by the double-fingerprint, not removed |
| **§ 5 harness adapters** | **CONFORMANT + one SPEC-SIDE ADDENDUM owed by me.** Claude lane live; Codex interface pinned, body raises, and D-6 now makes the refusal fire at **load**. **Addendum (Spec A § 5, next revision):** T16 landed 2026-08-11 with Codex CLI 0.147.0 resident, and a smoke found `codex exec` **dials configured MCP servers by default**. The un-stub must therefore launch with an **EMPTY MCP config** — an unscoped tool surface entering a lane whose containment posture assumes the process only touches declared trees is the `--tools`/`--allowedTools` failure again, one harness over. This is a spec obligation, **not a build defect**: nothing in the tree is wrong today. Note also that T16 landing does **not** open F2 — an agentic Codex cell is an agentic cell, gated on the same threat-model boundary |
| **§ 6 receipts + UsageBreakdown** | **CONFORMANT on the token law; O4 open-and-escalated.** Reasoning-as-share-of-output enforced twice and asserted. **The absence law holds and the declaration handles it correctly:** every founding-run phase records `NULL (mechanical phase — no model invoked)` (`runner.py:343-344, 555`), never zero-filled, and LANDING § 3 goes further than conformance requires — it names the misreading in advance ("O4 is unanswered *because* the agentic lane never opened… reading an empty column as a low number"). That sentence is the best thing in the declaration. **SCHEMA_VERSION is 3, not 2**, and not for the reason the O4 ruling gave |
| **§ 8 permissions fingerprinting** | **CONFORMANT at the closed state, and harder than § 8 specified.** Judging the state, not the journey: ignored-path blindness closed globally, unreadable-directory stderr channel folded in, protected paths split root-scoped vs every-repo, exemptions named by the *member* that forgave them so an operator can refute the sentence, quarantine-before-delete, measurement-limit caveat rendered on **every** receipt including green ones. **Open at this surface:** JR-27 (§ 4 below) and D-13 |
| **§ 9 YAML config, no `model` field** | **CONFORMANT.** No-model enforced at load and at argv build. **Ruling owed since v1, made here:** `on_fail: continue` (A-2) remains **unruled and unused** — SB-1 spine phases run `on_fail: stop`, as the founding workflow does. A continue-past-red switch on a run whose whole point is that verdicts bind does not get its first outing on SB-1 |
| **§ 11 acceptance** | **DISCHARGED ON REAL WORK — against an ancestor build.** The founding run `kc2-baton-mechanical-20260811T115024Z-361afd` is genuine: 3/3 phases, **15** gate verdicts (6+5+4) all PASS, baton verified at `d7ecd866ac45…` / 1,065,632 B, `BR2W_C9.mp4` at 40.37 s with `['video','audio']`, 78 kc2 session dirs on disk (I counted; matches the declaration). Workflow digest `090247019ba6…` on the live file **equals** the run's `workflow.snapshot` — the workflow did not move. **But the spine under it did.** That run started `2026-08-11T11:50:24+00:00` and its artifacts and `receipts.db` carry mtime `07:52:09 -0400`. Landing after it: `265adf95` report.py H6 (09:32), `46e298f7` permissions.py round-17 (11:03), `9f4a5302` JR-18 (15:47), `d3d4df43` JR-22 (18:09), `9be3c525` JR-23 (19:19). **Four containment commits and the report renderer changed under an unrepeated acceptance run.** Two visible consequences: items 1 and 2 (end-to-end + determinism) hold for `~46e298f7`-era code, not for `b8c0311c`; and the receipt of record's `run_report.md` **lacks the H6 "What was measured — and what was not" block** that `report.py:196-197` now renders on every run — so the run the declaration points at shows "3/3 green" with no measurement-limit caveat, which is the exact over-claim H6 exists to prevent. Items 3 and 4 (zero stub gates, synced triad, breach⇒rollback+abort) I re-verified at HEAD and they hold. Item 5 (jack-ryan Gate-2) closed LIFT-mechanical |

---

## 3 · Findings dispositions

All five are **veto-open** to the conductor and to Matt. The ladder is closed; a dispositioned
repair is a micro-dispatch through knight-rider, not a round 26.

**JR-27 (WARN) — the `unreadable_marker` guard keyed on the string, not on provenance.**
**Disposition: DECLARED DEBT for the guard (a). Coverage row (b) queued as a micro-dispatch,
NOT gating SB-1. VETO-OPEN.**
I measured SB-1's actual exposure rather than reasoning about it: **zero tracked paths bearing a
tab exist in any of the three repos** — meta, engine, godot — checked in both the raw-tab and the
git C-quoted `\t` forms. So the *modified* arm has no reachable subject in SB-1's substrate at
all. The *created* arm needs a phase to author an adversarial filename, and SB-1's spine cells
author no filenames: they are factory-authored YAML running a digest verify, an ffprobe verify,
and a test wall, every one `writes: []`. That exposure justifies debt.
The lean holds for a second reason worth stating plainly: **repair (a) is product code in the
containment wall on a closed ladder with no reviewer in the loop**, and this ladder's most
reliable event is a fix breeding the next finding — JR-22's fix bred JR-24, JR-23's fix bred
JR-27 itself. Touching the guard unreviewed before SB-1 is the highest-probability way to reopen
the lane we just closed. Half (b) — jack-ryan's `path_with_a_tab` entry in `ARTIFACT_KINDS`
(`test_containment_wall.py:289`) — is test-only, puts ten rows through detect/classify/rollback/
receipt across five parametrised rows and two shapes, and **pins the current behaviour** under
the honest-undo contract rather than changing it. That is where the coverage gap actually is, it
is where the durable value is, and it can fire before or after SB-1 without touching the run.
**Regrade trigger, carried verbatim from jack-ryan and I endorse it:** the moment any operator,
script or later phase treats the abort path as *restorative* rather than *evidentiary*, this is
a BLOCK. SB-1 must not acquire that habit.

**JR-28 (WARN) — a row that pins a spelling while its docstring claims a behaviour.**
**Disposition: DECLARED DEBT. VETO-OPEN.** Zero runtime exposure — this is a claim defect in a
test, and the behaviour it claims to pin *is* pinned, by the scene row, in both shapes and both
spellings. The cost is real but deferred: a future editor reads the docstring, believes the
reinstatement reds at the unit, and doesn't check. Cheapest honest repair is a one-sentence
docstring reword to what the row actually does; the better repair is jack-ryan's — give the
source-text assertion the third-exit treatment `_classify_module` just received, so anything in
the walk it cannot classify reds by existing. Fold into the JR-27(b) micro-dispatch if one fires.

**JR-29 (INFO) — a dominated assertion leg, and what the reach tracer cannot see.**
**Disposition: DECLARED DEBT, with one part promoted. VETO-OPEN.** The dominated leg is
housekeeping. The general observation is not, and it should not sit in a closed verdict file:
*`test_C2` answers "did this assertion run?", which is adjacent to "could this assertion have
failed?", and its wrong answer looks safe.* That is this ladder's own recurring shape arriving in
the instrument built to catch it, and it belongs in `README.md`'s rule set beside 44 so that
"test_C2 is green" is never read as "no leg is inert." Rule-text authorship is star-lord's; the
promotion recommendation is mine.

**JR-30 (INFO) — rule 50c scoped one notch narrow.**
**Disposition: DECLARED DEBT. VETO-OPEN.** Adopt all three of jack-ryan's refinements next time
the rule set is touched, and lead with their third: **pre-registration is the irreducible part**
— name the expected killer *before* the mutation runs — and it is currently buried in 50c's last
sentence. The reconciliation half is largely derivable from 50a. Also correct that the rule should
be written about *every* mutation, not only fix-rows.

**JR-7's INFO rider (agentic-gated) — the benign `ToolSearch` control.**
**Disposition: FOLDS INTO THE D5 REVISIT, carried undamaged. Not graded debt-vs-repair here**,
because it cannot be actioned until the threat-model boundary is drawn, and drawing it is not
this verdict's business. Carried is the correct state; carried is what LANDING § 1 does.

---

## 4 · Conditions on the serviceability PASS

Both are read-only or config-only. Neither is a code repair. Both are veto-open.

**C-1 · Re-measure the founding run at HEAD before the first SB-1 spine cell fires.**
`factory run workflows/kc2-baton-mechanical.yaml` and `factory determinism …` on `b8c0311c`.
Both phases are `writes: []` against read-only engine and godot trees; the whole thing took 1 m 45 s
at 07:50. This converts § 11 items 1–2 from "proven on an ancestor" to "proven on the shipped
tree", and produces a receipt of record that carries the H6 measurement block. **If the re-run
reds, no new machinery is needed — SB-1's charter § 4 honorable fallback already covers it**:
SB-1 decouples, proceeds conductor-run, G-FACT closes as a FINDING. The condition is a
measurement, and the failure branch is pre-registered.

**C-2 · Any SB-1 spine phase with a non-empty `writes` declares every non-target repo in
`read_only_trees`** — or is authored as a single-repo workflow. This is D-13's code-free
mitigation and it also collapses D-5 to nothing (one repo, no ambiguity to have).
**And the sentence the conductor most needs:** the founding run never exercised a **writing**
phase — every measured change-set was 0 paths. SB-1's G-WATCH promotion cell would be the first,
and it lands on **D-2** (execution inside a gate), **D-5** (repo-blind claims) and **D-13**
(repo-blind allowlist) simultaneously. Lean: run promotion as a **single-repo** spine workflow,
or keep it conductor-run under § 4. Do not make the first writing phase in this spine's life a
multi-repo one.

---

## 5 · What this verdict does NOT cover

Rubric-diff discipline — said out loud so silence is never read as clearance:

- **The agentic lane.** HOLD, clause 2, unchanged since round 17. Not judged here, not judgeable
  here. Its gate is the threat-model boundary, which is a design decision for me and Matt in the
  D5 revisit, **not a defect and not a drift item**. Nothing in this verdict advances or retards it.
- **Sandboxing / OS-level isolation.** Spec A § 12 non-goal; the D5 revisit's subject. Named, not ruled.
- **The F2 Codex lane.** Interface only. T16's landing does not open it; the § 5 addendum above is
  a spec obligation for whoever fills the body, not a claim the lane is closer.
- **Rule 39's tension with unscoped `Bash`.** Same boundary, same revisit.
- **The three-clause stopping rule and the mechanical/agentic split.** Matt's. jack-ryan's closing
  § 6 recommendation — *write clause 1 about class coverage rather than clean rounds, because the
  class is what recurs and a clean round is what a narrow instrument produces* — is well-founded
  and I have nothing to add to it that would be evidence rather than opinion.
- **O4 itself.** I ruled DROP; jack-ryan ruled KEEP; star-lord correctly implemented neither and
  escalated. I do not re-rule it here, and I withdraw one clause of the v1 verdict: I wrote that
  partial adoption of the four-item fallback is *worse than either endpoint*. That was written
  before D-4 landed. D-4 landed in a form that is safe **in both branches** — the figure is now
  labelled from the receipt, mixed sources render as `A + B`, and an unrecorded provenance renders
  as "this figure cannot be read as money spent." The misread channel is closed. If Matt rules
  KEEP, two items remain: rename the column off the word `dollars`, and make `dollars_source` NOT
  NULL at the schema whenever the figure is present. If Matt rules DROP, the removal is still
  cheap — `report.py` needs no change either way, which is precisely what star-lord engineered.
- **Anything SB-1-run-specific.** Cell design, presentation grammar, the G-EYE checkpoints, the
  fork table. Charter territory, not spine territory.
- **D-10 / D-11.** Open, agentic-gated, correctly declared in LANDING § 5.

---

## 6 · Sign-off

**FAITHFUL-WITH-DRIFT.** The five laws are compiled; § 8 is compiled harder than I wrote it. The
drift that remains is three v1 items nobody claimed to have fixed, one I found this pass, and one
doctrine call sitting where it belongs — on Matt's desk with two reasoned seam opinions attached.

**SERVICEABILITY: PASS**, conditional on C-1 and C-2, with the § 4 fallback standing behind both.

The thing I want on the record for whoever reads this in six months: across 25 rounds this tree's
recurring defect was *a predicate answering a slightly different question than the one asked,
whose wrong answer is the safe-looking one.* It arrived in the product, in the tests, in the
instrument, and in the prose. **It arrived once more in this review** — the founding run's receipt
answers "did the spine pass?" when the question SB-1 needs answered is "did **this** spine pass?"
The shape does not stop arriving. It gets caught by asking what the artifact is actually a
measurement *of*, every time, including when the artifact is green.

**Signed:** gandalf — DRIFT-CRITIC (sub-agent), 2026-08-11.

**Inputs read:** Spec A (`gandalf/notes/2026-08-10-factory-spine-spec.md`) · `factory/LANDING.md`
· `qa/pending/2026-08-11-jack-ryan-factory-spine-gate2-r25-CLOSING.md` · v1 verdict
(`gandalf/notes/2026-08-10-factory-spine-drift-critic.md` @ `4ba09ff0`) · SB-1 charter § 4 + § 11
(`gandalf/notes/2026-08-10-sb1-kc2-scene-run-charter.md`) · star-lord fixes ledger §§ 5, 6, 26,
27 (`star-lord/notes/2026-08-10-factory-spine-gate2-fixes.md`) · the tree at `b8c0311c`:
`permissions.py`, `runner.py`, `workflow.py`, `receipts.py`, `report.py`, `usage.py`, `cli.py`,
`gates/core.py`, `harness/codex.py`, `workflows/kc2-baton-mechanical.yaml`, `tests/`
· founding-run artifacts under `factory/sessions/`.
**Executed (read-only):** the suite (622 green, 172.68 s) · `git show`/`git log`/`git diff
--name-only` on the factory path · `shasum -a 256` on the workflow and its snapshot ·
`git ls-files` tab-exposure counts across three repos · `git status --porcelain
--ignored=traditional | wc -l` on the godot tree · `stat` on the receipts DB and session dir.
**Wrote:** this file. **Modified:** nothing.

---

## Conductor's fold — C-1 executed, verdict accepted (RUN-CONDUCTOR, 2026-08-11)

▶ ROLE: RUN-CONDUCTOR — folding the sub-agent verdict into SB-1's launch gate.

**Verdict ACCEPTED as written**: FAITHFUL-WITH-DRIFT; SERVICEABILITY PASS conditional on C-1 + C-2;
all five findings dispositions accepted **veto-open** (JR-27 declared debt + `path_with_a_tab`
coverage row as non-gating micro-dispatch; JR-28 folds into that dispatch; JR-29 debt + README-rule
promotion authored by star-lord; JR-30 debt; JR-7 folds into Q55). O4 KEEP-vs-DROP stays on Matt's
desk untouched.

**C-1 — CLOSED GREEN.** Executed by the conductor immediately on accepting the verdict, against
tree HEAD `e386f529` (code head `b8c0311c` + LANDING.md):

- `factory run kc2-baton-mechanical.yaml` → **PASS**, 3/3 phases, all gates green.
  Receipt: `kc2-baton-mechanical-20260812T011509Z-f0cf28`.
- `factory determinism` → two further full laps, **DETERMINISM: EXACT — 14 gate verdicts
  identical across two laps**. Receipts: `…20260812T011712Z-b9cdeb`, `…20260812T011857Z-cb3f8d`.
- The drift C-1 named is healed on the record: the HEAD receipts carry the H6 measurement-limit
  honesty block (`containment: coarse — reincarnated-godot measured COARSELY … in region(s):
  ['.godot/', 'Assets/Synty/']`) that the pre-close receipts of record lacked. The founding
  receipt answered "did the spine pass?"; these receipts answer "did **this** spine pass?" — yes.
- Footnote, recorded not alarmed-over: LANDING.md § 3 counts 15 gate verdicts on the founding
  receipts; the HEAD workflow evaluates **14**. The delta sits somewhere in the four containment
  commits between the receipt of record and close; the determinism instrument declares its own
  denominator (14) and matches itself exactly. Left for the JR-27(b) micro-dispatch to name in
  passing if it proves more than a gate consolidation.

**C-2 — ADOPTED as SB-1 authoring law.** Every SB-1 spine phase with non-empty `writes` declares
every non-target repo in `read_only_trees`, or the workflow is single-repo. Conductor lean
unchanged: single-repo or conductor-run for the G-WATCH promotion cell.

**Consequence for SB-1 § 11:** launch condition **(1) CLOSES** — spine ladder closed (LANDING.md,
mechanical LIFT) **+** conductor DRIFT-CRITIC re-verdict PASS with its conditions discharged
(C-1 measured green at HEAD; C-2 adopted into authoring law). Remaining launch residue: (2) Matt's
veto word or silence-past-next-engagement on charter + K-1..K-5; (3) drax Cell 0 countersigns
dispositioned.

**Signed:** gandalf — RUN-CONDUCTOR (conductor of record, SB-1), 2026-08-11.
