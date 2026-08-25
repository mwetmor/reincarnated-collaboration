# reincarnated-canonical-doc-format — Canonical Doc Format + Lifecycle (Cross-cutting Reference)

> **STATUS:** CURRENT (load-bearing). First authored 2026-05-23 (Stream 3 cross-cutting reference skill). **Amended 2026-06-30 — doc-lifecycle governance added (§ 6): propagation + pruning system, ratified by Matt 2026-06-30 after a 14-scenario stress-test.** The pre-amendment "demote to `canonical/historical/` subfolder" model is RETIRED (the reorg went git-is-archive); reconciled in § 1 + § 3. **Amended 2026-07-06 — the parse contract (§ 7) ratified by jack-ryan from gandalf's Glance contract-spec § 2 proposal (proposer→ratifier per § 6.7); old §§ 7–8 shifted to §§ 8–9. Mirrored as Discipline #60 (CI-fail-loud). Amended 2026-07-10 — shape #6 FLOW declaration (§ 7.8) folded via delta-ratification (§ 7.9); shape count 5 → 6; MALFORMED enumeration re-closed at six conditions; Discipline #60 amended in the same commit (twin-sync).** **Amended 2026-08-24 — § 6.3 prune-safe predicate widened: predicate 4 re-derived over the whole tracked corpus (code + data + binaries count as prune BLOCKERS), plus new clauses 4a (a code citation is never auto-prunable) and 5 (liveness is per-clause; a demotion must adjudicate the gap). gandalf proposed `bdec6e1e`; jack-ryan RATIFIED-WITH-AMENDMENT M per § 6.7 proposer→ratifier. Predicate count 4 → 5. The § 6.6 auto-prune HOLD is discharged. Skill twin synced in the same commit (§ 6.8).**

**Authored:** 2026-05-23 · **Amended:** 2026-06-30 (lifecycle governance)
**Author:** gandalf (cross-cutting reference owner + primary canonical-doc author)
**Authority:** Matt 2026-06-30 — doc-lifecycle governance (the four rulings: total-vs-partial supersession, auto-prune ceiling, three note-classes, markdown-only scope)
**Authoritative source for canon status:** `canonical/00-ground-state.md` (the thin router — the three canon homes)
**Companion skills:** `reincarnated-engineering-disciplines`; `reincarnated-decision-log-format`; `reincarnated-critique-pair-gate-protocol`; `reincarnated-hive-mind-protocol`

---

## 0. What this skill IS and IS NOT

**IS:** the universal **format + lifecycle** spec for canonical docs under `canonical/` — the spec folders (`reap-die-rise-{story,engine,game}/`, which carry the numbered spine + story/lore/design artifacts + recognition records since the 2026-07-01 fold-completion, plus the playable-product scope since 2026-07-02), the trackers, and the router. Names: header structure, STATUS protocol, cross-reference rules, **and (§ 6) the authoring → propagation → pruning lifecycle** — how a canonical write feeds the current-to-end-state trackers, and when a doc/note is pruned. Loaded by any agent authoring or amending canonical artifacts.

**IS NOT:** the substantive content guide (each doc's substance is per-topic). NOT the router itself (`canonical/00-ground-state.md` is always the source of canon-home truth). NOT the decisions-log format (`reincarnated-decision-log-format`). NOT a lifecycle for **data / code / binary** artifacts — those (`.json`, `.csv`, `.py`, `.png`, `.mp4`, `.html`) live under their seam owner's lifecycle, explicitly **out of § 6 scope** (§ 6.3).

---

## 1. Where canon lives (reconciled 2026-06-30 — git is the archive)

Canon lives in **three homes** (per the router, `canonical/00-ground-state.md`):

| Home | Contents |
|---|---|
| `canonical/reap-die-rise-story/` + `canonical/reap-die-rise-engine/` + `canonical/reap-die-rise-game/` | the END-STATE **spec** folders (story frame; engine spec; playable-product/game spec — born 2026-07-02, One Realm MVP). Each has a `00-index.md`. |
| `canonical/current-to-end-state/` | the **delta** trackers — `…-engine.md` (build-vs-spec gaps) + `…-story.md` (open story decisions) + `…-game.md` (playable-build gaps). LIVING. |
| `canonical/00-ground-state.md` + `canonical/matt_decision_needed/` + `canonical/matt_to_do/` | the router (sole file at `canonical/` root since the 2026-07-01 fold-completion) + the Matt queues (decisions; actions) |

**Anything older — superseded designs, epoch history, the old historical/dead registry — lives in git, recoverable, not pre-load.**

**Retired 2026-06-30:** the `canonical/historical/` and `canonical/dead/` **subfolders** (they no longer exist). The old model relocated demoted docs into those subfolders to keep them in-tree as lineage. The reorg replaced that with **git-is-archive**: a fully-superseded doc is **removed from the live tree** (git keeps it), not relocated to a subfolder. The STATUS *stamps* CURRENT / HISTORICAL / DEAD survive as **in-doc labels** (§ 3); only the subfolder *relocation* is gone.

**Authoring rule:** new docs land in a spec folder (end-state — design/lore/recognition records included), `canonical/current-to-end-state/` (a tracker), or `canonical/matt_decision_needed/` (decision queue). The numbered-keystone root and `canonical/story/` homes retired 2026-07-01 (fold-completion — everything folded into the spec folders). Docs leave the live tree only via the lifecycle in § 6 (supersession or workstream-close → git-lineage).

---

## 2. Header structure (every canonical doc)

```markdown
# <Doc Title>

> **STATUS:** <CURRENT | HISTORICAL | DEAD> (load-bearing as of YYYY-MM-DD) — see `canonical/00-ground-state.md`

**Date:** YYYY-MM-DD (authoring session)
**Author:** <agent name> (role)
**Status:** v<N> <version + lock status>
**Authority:** Matt YYYY-MM-DD — <authorization note>
**Companion docs:**
- <path> — <one-line relationship>

---

## 0. TL;DR
<3-5 bullets or 1-3 paragraphs>
<If recognition record: "Recognition Record — architectural commitments deferred per § X" framing required>

---

## 1-N. Substantive sections

---

## (Final). Cross-references
<canonical / operational / decisions-log / prior-art links>

Tracker-delta: <none | see § 6.2 — one line: new gap / closed gap / new open decision → which tracker, which PART>

---

**Signed:** <author> (role)
**For:** <one-sentence purpose>
```

**Header field discipline:**
- **STATUS stamp** — CURRENT only when load-bearing; HISTORICAL when informative-only; DEAD when structurally retired (anti-pattern reference)
- **Date** — initial authoring date; never edit (use inline amendment notes for revisions)
- **Author** — primary author; co-authors named in v<N> amendments
- **Status** — version + lock state ("canonical lock" / "draft" / "recognition record")
- **Authority** — who authorized the artifact + when
- **Companion docs** — direct dependencies; not exhaustive
- **Tracker-delta footer** — **new 2026-06-30 (§ 6.2).** One line at the end of the Cross-references section naming what tracker state this write moved (or `none`). Greppable; the hygiene audit checks for it.

---

## 3. STATUS protocol (reconciled 2026-06-30)

| Status | Means | Do |
|---|---|---|
| **CURRENT** | Load-bearing top-of-stack | Treat as authoritative |
| **HISTORICAL** | Shaped current canon; not current truth | Consult for lineage only |
| **DEAD** | Superseded structurally; do NOT consult | Anti-pattern reference only |

**STATUS lifecycle (post-reorg):**
1. **New doc** — authored CURRENT (if load-bearing) or recognition record (commitments deferred).
2. **Partial supersession** — a successor absorbs *part* of this doc's load-bearing content. The doc stays CURRENT-with-a-banner and **folds** in place (transition-lineage, § 6.4). It does NOT leave the tree yet.
3. **Total supersession** — a successor fully absorbs all load-bearing content. The doc → **git-lineage** (removed from the live tree, § 6.3/§ 6.4). No subfolder hop.
4. **Workstream-close** — a working-memory note whose workstream closed → git-lineage (§ 6.3).
5. **Re-surface (rare)** — a doc needed again is recovered from git and re-stamped CURRENT. (Pre-reorg this was a subfolder move-back; now it's a git restore.)

**Registration:** new CURRENT spec/decision content registers its *delta* in the relevant current-to-end-state tracker (§ 6.2), NOT in a router registry (the old per-doc oracle registry was dissolved in the reorg). The router (`00-ground-state.md`) changes **only** when a canon *home* changes.

---

## 4. Cross-reference protocol

- **Path-based** — `canonical/reap-die-rise-story/<doc>.md`, not URL-style
- **Section-anchored when load-bearing** — `…/<doc>.md § 6.4`
- **Bidirectional when substantive** — if A cites B as Companion, B references A back (especially recognition records that later get superseded)
- **Decisions-log entries by date-title** — `2026-05-12: Recompose-first adoption`, not line number
- **Tags by name** — `v1.3-b14-2`, not commit hash
- **Commit hashes only when load-bearing** — `commit f72690f` for architectural locks

---

## 5. Recognition record special case

When authoring a recognition record (substantive recognition + architectural commitments deferred per substrate-led discipline):
- **STATUS:** CURRENT — the recognition IS load-bearing; the deferred commitments are not
- **TL;DR framing:** explicit "Recognition Record — architectural commitments deferred per § X"
- **Empirical-evidence criteria named** — what gates re-engagement (substrate threshold, playtest result, methodology output) — NOT time-passage
- **Predictions registered** — what would land if the recognition fired as commitment
- **Lifecycle:** a recognition record is treated as a **verdict-class** artifact (§ 6.1) — pruned only on TOTAL supersession AND zero live references. If decisions-log later cites it as the source of a ratified commitment, it becomes **evidentiary** and is never auto-pruned.

---

## 6. Doc lifecycle — authoring → propagation → pruning (NEW 2026-06-30)

Ratified by Matt 2026-06-30 after a 14-scenario stress-test (lineage: `agentic_orchestration/gandalf/notes/2026-06-30-doc-lifecycle-governance-stress-test.md`). The system has one job: **nothing depends on someone remembering to clean up or to update the trackers.** Propagation and pruning are triggered by *events*, verified before they fire.

### 6.1 Three artifact classes (and three note sub-classes)

| Class | What | Lifecycle |
|---|---|---|
| **Canonical doc** | spec / decision / recognition / design-spec-as-math | durable; pruned only on TOTAL supersession (§ 6.4) |
| **Tracker** | the two current-to-end-state docs | LIVING; never pruned — resolved rows collapse to a CLOSED appendix (§ 6.5) |
| **Note** | an agent's working artifact in `…/<agent>/notes/` | depends on sub-class ↓ |

**Note sub-classes (a note is classified at prune-time by the cross-repo reference check, § 6.3):**
- **Evidentiary** — cited by `decisions-log` / canonical / an OP / a skill as *source* or *evidence*. **Never auto-pruned** — it is lineage of the permanent record. (Example: `2026-05-25-phase-2-50-row-spot-check.md`, cited in decisions-log as "load-bearing empirical evidence." Pruning it would dangle a ratified decision.)
- **Verdict / recognition** — a Pattern-A-deep verdict or design recognition captured as decision lineage. Pruned only on TOTAL supersession AND zero citations.
- **Working-memory** — scratch analysis, tee-ups, diagnoses, session pointers; never cited; workstream closed. **Auto-prunable** (the only auto-prunable note class).

### 6.2 System A — canonical → tracker propagation (the `Tracker-delta:` convention)

**Problem it solves:** when a canonical doc lands or changes, its spec-delta must reach the trackers. Relying on memory fails silently (today, only gandalf's mandatory update catches it, only for docs gandalf writes).

**The convention:**
1. Every canonical write/update that moves spec or state carries a **`Tracker-delta:` footer** (§ 2) — one line: *new gap / closed gap / new open decision → which tracker, which PART.* `none` if nothing moved.
2. The author **emits** the delta; the author does **not** write the tracker (write-authority is narrow — gandalf + KR only; Matt 2026-06-30).
3. **Consolidation owner:** **gandalf** for design-session writes (immediately); **KR** at wave-close for orchestrated / sub-agent writes — KR extracts the footer from the sub-agent's returned text (sub-agents fire `run_in_background` and cannot reliably write shared docs; they return, KR captures).
4. **Enforcement:** the hygiene audit (§ 6.6) greps commits that touched `canonical/` for a missing `Tracker-delta:` footer and flags them, so propagation cannot silently decay.

### 6.3 System B — pruning (the prune-safe predicate)

Honest ceiling first: **fully-blind auto-delete is unsafe** — a superseded-*looking* doc can carry un-promoted load-bearing content or be cited by a live doc. So "auto" = **event-triggered + reference-verified**, never a timer that deletes on sight.

**A doc/note AUTO-prunes (git-rm; git is the archive) only if ALL four hold** *(predicate 4 REPLACED and 4a + 5 ADDED 2026-08-24 — gandalf proposed `bdec6e1e`, jack-ryan RATIFIED-WITH-AMENDMENT M; see the ratification block below)***:**
1. **Markdown design artifact** — not data / code / binary (those are seam-owner lifecycle, out of scope)
2. **Not a never-prune class** (below)
3. **Either TOTALLY superseded (§ 6.4) OR a working-memory note whose workstream closed**
4. **Zero live references across BOTH repos.** The reference check greps for the candidate's basename across **every tracked file in both repos** (`git grep` over `git ls-files`), **excluding only the candidate itself and other files in the same prune batch — and that exclusion set is enumerated in the sweep record** (Amendment M(c)). It is a **derivation over the tracked corpus**, not a walk of a named list of surfaces (Discipline #76 clause 1). In particular it **must** cover source, config, data and test files (`.py` `.json` `.yaml` `.jsonl` `.sh` `.gd` `.ts` `.tscn`, and binaries — `git grep` reports these as *"Binary file … matches"* and that **counts as a citation**) — **predicate 1 excludes code as a prune TARGET and that exclusion does not transfer to code as a prune BLOCKER.** A citation from running code is the strongest possible evidence a doc is live, because something executes against it.

   > **Declared coverage boundary of this predicate (Amendment M(a); Discipline #70).** Basename grep sees a citation **only if the citing file writes the basename.** It is structurally blind to: a doc cited by *title* rather than filename; a doc cited by a stale path whose basename was later changed by a `git mv`; and a cross-document *section* reference that names no file. **A clean predicate-4 result is therefore "no basename citation found," never "no citation exists."** It is a safety predicate, not a completeness proof, and the sweep record states it in those words.

4a. **A code or data citation is never auto-prunable — it is always judgment-tier.** Where predicate 4 finds a citation from a non-markdown tracked file, the candidate does **not** auto-prune under any circumstances; it surfaces for ratification with the citing `file:line` listed. Rationale: a markdown citation can be lineage; **a code citation is a runtime dependency on a claim.**

5. **Liveness is a per-clause property; STATUS is a per-document stamp. A demotion must adjudicate the gap.** Before stamping a doc `HISTORICAL` / `DEAD` — and therefore before it can ever enter a bulk sweep — the demoting agent asserts, **in the stamp**, that no clause in the doc carries an unmet exit condition. The check is mechanical enough to be cheap: grep the doc for `until … ships/lands` · `exit condition` · `standing` · `in effect from` · `MUST NOT` · `remains operative`, and for each hit either (a) show the condition is met, (b) show the clause is restated in a never-prune surface, or (c) **do not demote.**

   A doc that is 90 % historical and 10 % live is **not** a historical doc. It is a **partial supersession (§ 6.4)** and the existing rule already governs it: *never `git rm` a partially-superseded doc — that amputates load-bearing structure.* **§ 7 of `substrate-expansion-decision-2026-05-17.md` was an amputation, and § 6.4 already forbade it; what was missing was any obligation to look before stamping.** Clause 5 supplies the look.

   > **Amendment M(b) — the keyword list is illustrative, not the population (Discipline #76 clause 1, applied to clause 5's own text).** The six patterns above are a **starting net**, explicitly labelled as such. A live clause phrased without them passes through, and gandalf's own Tranche-1b adjudication declared exactly this residual (9 of 23 read; 14 uncovered). **Where the demoting agent cannot establish per-clause liveness mechanically, the correct output is (c) do not demote** — not a clean grep reported as an assertion. This clause obliges a *look*, and a look that found nothing says so in those terms.

If 1–2 hold but 3–5 are ambiguous → **surface for ratification**, never auto-fire. **"Became irrelevant" has no detectable event — it is ALWAYS surface-for-ratification, never auto-pruned.**

---

> #### ⚖ RATIFICATION — § 6.3 clauses 4 / 4a / 5 (2026-08-24)
>
> **Proposer:** gandalf (`CANON-STEWARD`), commit `bdec6e1e`, from the stranded-live-clause audit (`gandalf/notes/2026-08-24-stranded-live-clause-audit-and-section-7-relocation.md`).
> **Ratifier:** jack-ryan, per § 6.7 proposer→ratifier and the `⚠ SWITCH: CANON-STEWARD → jack-ryan` conflict seam (*proposer ≠ sole-ratifier-on-self*).
> **Verdict: RATIFIED-WITH-AMENDMENT M** (three parts, folded above: M(a) coverage boundary on predicate 4; M(b) keyword list declared illustrative in clause 5; M(c) prune-batch exclusion set enumerated in the sweep record).
> **Authority:** ADR-002 tiered approval — documentation-class governance amendment. **Not escalated to Matt.** See the non-conflict finding below.
>
> **Why this does NOT re-open Matt's 2026-06-30 markdown-only-scope ruling.** This document's authority line names *"markdown-only scope"* as one of four Matt rulings, and clause 4 makes the predicate read non-markdown files. Those are different objects and gandalf drew the distinction correctly: **predicate 1 governs what may be prune-TARGETED (markdown only — unchanged); predicate 4 governs what counts as EVIDENCE that a target is live.** The ruling's scope is untouched.
>
> **The decisive argument is monotonicity, and it is why this needed no Matt gate.** All three clauses are **strictly retention-increasing**. Clause 4 widens the evidence that *blocks* a prune. Clause 4a converts a class of auto-prunes into judgment-tier. Clause 5 adds a precondition on *demotion*. **None of them can cause a file to be deleted that would otherwise have survived.** A change that can only make a destructive automation fire *less* often cannot breach a ceiling ruling whose purpose is to bound that automation. Matt's auto-prune-ceiling ruling is honoured a fortiori, not eroded.
>
> **Predicate 4 was verified, not accepted (Discipline #19.1(b)).** The proposal's claim that `movement-speed-baseline.md` is cited by ~10 engine files was re-derived at ratification: **18 tracked citers, 11 of them non-markdown** — `export/schemas.py`, `generation/class_schema.py`, `generation/monster_generator.py`, `generation/monster_schema.py`, `generation/season_generation_pipeline.py`, `simulation/combatant.py`, `telemetry/migrations.py`, `telemetry/telemetry_seed.db`, and three test modules. The claim reproduces and the binary hit is what motivated M(a)'s binary clause.
>
> **Clause 5 is correctly identified by its proposer as the load-bearing half, and I concur.** Clause 4 would have retained § 7 *by accident* — for a reason unrelated to why it was live. Clause 5 catches the case clause 4 structurally cannot see: **a live-claused doc cited by nothing at all.**
>
> **Declined, with reasons.** gandalf offered a general discipline form — *"a document's STATUS is an assertion about every clause it contains"* — and explicitly left the number to me. **No new discipline number.** It is a doc-lifecycle rule with exactly one corpus (`canonical/` + `agentic_orchestration/` markdown) and one enforcement point (the demotion stamp), and clause 5 is where a reader meets it. Minting a number would create the #58-DECLINED hazard in reverse: a general rule nobody triggers, cited from the specific rule that already works. **Revisit only if a second corpus acquires per-clause liveness semantics.**
>
> **HOLD DISCHARGED.** `agentic_orchestration/HOLD-2026-08-24-hygiene-routine-auto-prune.md` lifts on this ratification per its own step 1, and is deleted in the same commit per its step 2. § 6.6 step 3 (auto-prune tier) resumes **under the amended predicate**, and the step-4 `CODE SURFACES NOT GREPPED` declaration requirement — knight-rider's amendment, correct while it stood — **lapses with it**, because clause 4 now greps them. The 14 unopened Tranche-1b cases remain owed to gandalf and are unaffected by this ratification.

**Never-prune class:** `decisions-log.md`, `CHANGELOG.md` (append-only ledgers); the two trackers (LIVING — § 6.5); `00-ground-state.md` (router); `AGENTS.md` / `GOVERNANCE.md` / `REVIEW_PROCESS.md`; all OPs + skills; the spec-folder `00-index.md` fold-worklists.

**Three triggers fire the predicate:**
- **Supersession-at-authoring** — when you write B that *totally* supersedes A, you `git rm` A **in the same commit** (after the reference check). Supersession IS the prune. (Partial supersession does NOT trigger — § 6.4.)
- **Workstream-close** — when a cycle/investigation closes, each agent self-prunes its own *working-memory* notes for that workstream (one OP line). Distributed routine.
- **Scheduled hygiene audit** (§ 6.6) — the centralized sweep that catches residue the first two missed, runs the reference check, auto-prunes the safe tier, and surfaces the judgment tier.

**Move ≠ prune:** a relocation (`git mv`, content survives at a new path) is not a supersession. Only content *replacement* triggers the prune.

### 6.4 Total vs partial supersession (reconcile, do not amputate)

The dominant real pattern is **partial** supersession: a doc is `STATUS: CURRENT` *and* carries a `⚠ FRAME PARTIALLY SUPERSEDED` banner — its load-bearing structure survives, only retired *labels* die. (Example: `reap-die-rise-engine/2026-06-02-season-archive-realm-expansion-pivot.md` — the frame-neutral engine-architecture spine §3.2–3.4 survives; the isekai content-model dies under v2.)

- **Partial supersession → reconcile in place.** Banner it; fold its surviving structure into the successor (the spec folder); the doc is **transition-lineage** and stays in the live tree until the fold-worklist (`spec-index.md §4` / the tracker PART C) marks it **fully absorbed**. Only then does it become git-lineage. **Never `git rm` a partially-superseded doc** — that amputates load-bearing structure.
- **Total supersession → prune.** Only when the successor absorbs *all* load-bearing content.

A doc is "transition-lineage" (audit-exempt) iff it is an explicit fold-source in an active worklist. Self-documenting via the worklist — no per-doc flag needed.

### 6.5 Tracker hygiene (resolved → CLOSED appendix, not git)

Tracker rows are **resolved**, not deleted — because reopening is common (e.g., B3 season-two-companion, reopened by Matt 2026-06-30). A resolved row is marked ✓ DONE / struck-with-date and, when the live body grows noisy, swept into an in-tree **CLOSED appendix** (collapsed) so the tracker stays focused on what's still owed. Only a truly-dead row (a decision superseded and never reopened) eventually goes to git via the surfaced-ratification path. The trackers themselves are never pruned.

### 6.6 The hygiene-audit Routine

A standing scheduled Routine fires into a gandalf session on a fixed cadence and:
1. finds total-superseded / workstream-closed / orphaned markdown design-artifacts the first two triggers missed;
2. runs the cross-repo reference check (§ 6.3 predicate 4 — **a derivation over `git ls-files` in both repos, code and data included**, as amended 2026-08-24);
3. **auto-prunes the predicate-safe tier** (git-rm; in-scope auto-commit) — **predicates 1, 2, 3, 4 AND 5, with clause 4a excluding any candidate carrying a code or data citation from this tier entirely**;
4. **surfaces the judgment tier** (ambiguous / "became irrelevant" / **any 4a code-citation candidate**) as a prune-list for Matt's ratification;
5. flags canonical commits missing a `Tracker-delta:` footer (§ 6.2 enforcement);
6. collapses resolved-and-aged tracker rows into the CLOSED appendix (§ 6.5);
7. runs the reorg-integrity **tripwires** (dead-home regression · OP↔skill twin drift, § 6.8 · Matt-queue sync) — flag-only, never auto-fix (ratified jack-ryan 2026-07-02).

**Distribute routine, centralize judgment:** each agent self-prunes its own working-memory notes at workstream-close; the gandalf sweep handles cross-cutting residue + the judgment tier + tracker collapse. Scales as agents are added.

### 6.7 Rule-ownership — who RATIFIES doc-lifecycle governance (Matt 2026-06-30)

The § 6 *rules* are a discipline, and a discipline has a conflict-of-interest hazard when the author is also its largest subject. gandalf is the meta-repo's largest note-producer; a gandalf-authored prune-rule that softens treatment of steward notes (the S15 finding, stress-test § 4) is **rule-maker = rule-subject** — the developer↔judge conflict transposed to governance. Matt 2026-06-30 ruled the fix by **symmetry with engineering-disciplines**:

- **jack-ryan RATIFIES doc-lifecycle rules** (the same way jack-ryan owns engineering-disciplines — the rules engineers run under; § 6 is the sibling: the rules doc-producers run under).
- **gandalf PROPOSES + EXECUTES** (proposes mechanisms as the practitioner who feels the pain; executes the prune/propagation on the established rules).
- The **switch-moment is named in the open:** when gandalf proposes a governance rule — *especially one affecting gandalf's own output* — gandalf emits `⚠ SWITCH: CANON-STEWARD (proposer) → jack-ryan (ratifier)` (gandalf OP § 2 role-tags) and routes the rule to jack-ryan before it is canon.
- **Execution is not the conflict.** gandalf (or any seam-owner on their own notes) *running* an established rule is fine — the conflict is only at rule-*authoring*. So proposal → gandalf; ratification → jack-ryan; execution → gandalf + seam-owners.

**Pending ratification:** the **S15 substance-homing refinement** (stress-test § 4) is Matt-agreed *content* but its ratification-ownership now sits with jack-ryan — jack-ryan reviews S15 on next governance touch and either ratifies it into § 6.1/§ 6.3 or returns it. Until then S15 is Matt-agreed-but-not-jack-ryan-ratified, flagged as such in the stress-test record.

### 6.8 OP↔SKILL twin-sync (RATIFIED jack-ryan 2026-07-02)

Several operating-procedure docs (`agentic_orchestration/operating-procedures/<name>.md`) have an installed skill twin (`.claude/skills/reincarnated-*<name>*/SKILL.md`). **They are ONE document in two locations:**

- **Amend together, same commit.** Any edit to an OP section with a twin lands in both bodies in the same unit of work (skill YAML frontmatter excepted — packaging, not content).
- **The OP is source-of-truth** where the twins disagree; the skill is the installed copy.
- **Drift is repaired by the twin's OWNER** (the agent whose OP it is) — the hygiene Routine's tripwire (b) FLAGS divergence (pair + first divergent section), never auto-fixes.
- **Repair is ADR-002 tier** — jack-ryan-approved, no Matt gate (restoring ratified content to parity is not new rule-making).

Sibling of § 6.2: the Tracker-delta rule keeps canon↔tracker in sync; this rule keeps OP↔skill in sync. Evidence case: the gandalf OP/skill drift (§ 1 step 2 / § 4.7 / § 5), flagged + repaired 2026-07-02 — and this doc's own skill twin, found missing § 6.7 during the same pass.

---

## 7. The parse contract — the six legislated shapes (RATIFIED jack-ryan 2026-07-06 · shape #6 FLOW folded 2026-07-10)

**Ratification lineage:** gandalf PROPOSED this as Glance contract-spec § 2 (`agentic_orchestration/operating-procedures/glance-contract-spec-2026-07-03.md`, 2026-07-03); routed to jack-ryan via the § 6.7 `⚠ SWITCH: CANON-STEWARD (proposer) → jack-ryan (ratifier)` beat. RATIFIED here 2026-07-06 (shapes 1–5) with the amendments named in § 7.7. **Shape #6 (FLOW declaration, § 7.8) was added to the Glance contract as v1.1 on 2026-07-07 — AFTER the 2026-07-06 five-shape ratification — and folded into canon here 2026-07-10 (delta ratification, § 7.9).** This section is the **canonical, authoritative** statement of the parse contract; the Glance parser (drax) builds against THIS, not the proposal text. Matt rulings embedded: Glance GO / STANDALONE / fork-4 `gates-on:` tokens LIVE on all queue-row writes NOW (Matt 2026-07-03); FLOW as the Tier-0 end-to-end abstraction (Matt 2026-07-07, fork (b)).

**What this legislates:** canonical docs are already semi-structured data wearing markdown clothes. This section codifies the **MINIMUM parseable set — exactly six shapes** (five at v1.0; shape #6 FLOW added v1.1, Matt-ruled 2026-07-07). Everything else stays free markdown, rendered as prose, never modeled. The team's only new obligation: **keep writing what you already write, parseably.** This is minimum-legislation by design — do not expand the shape count without a fresh proposer→ratifier round.

### 7.1 Shape 1 — STATUS banner
The first blockquote in the doc containing the literal `**STATUS:**` marker. Parser captures: the stamp word(s) (`CURRENT`, `SPEC-CURRENT`, `LIVING`, `ROUTER`, ` HISTORICAL`, `DEAD`, `SUPERSEDED`, `PARTIALLY SUPERSEDED`), the first date found, and the raw line. This is the § 2 header structure surfaced as data — no new authoring obligation.

### 7.2 Shape 2 — SESSION-DELTA LOG
A `## SESSION-DELTA LOG` section whose entries are `### YYYY-MM-DD — <headline>` (multiple same-date entries permitted; suffixes like `(2)` tolerated). **Newest-first in the file; latest governs** (the § 4 supersession law delivered structurally). Entry body = everything until the next `###`/`##`.

### 7.3 Shape 3 — Queue rows
A markdown table under a queue heading where each data row's **first cell begins with a row ID** (`D.1#8`, `B1`, `W0.3`, `III.8`, `Q2`, or a plain ordinal) and some cell carries a **status prefix** from the enum:

| Prefix | Meaning |
|---|---|
| `✓` | closed |
| `⛔` | blocked |
| `⚖` | awaiting Matt ruling |
| `PARKED` | parked (named re-entry) |
| `IN-FLIGHT` | executing |
| `OPEN` *(or no prefix)* | open |

The prefix is the contract; **the remainder of the cell is free prose** (`⛔ BLOCKED — REBASE` parses as blocked + prose). Bullet-list queues (non-table) are modeled **iff** the bullet begins with a row ID followed by `—` or `:`.

### 7.4 Shape 4 — `gates-on:` tokens — fork-4 dependency law (LIVE NOW, Matt 2026-07-03)
Grammar, anywhere within a modeled row's cells (or trailing on a modeled bullet):

```
gates-on: <token>[ (<qualifier>) ] [· <token>[ (<qualifier>) ]]*
token     := row ID (W3, D.1#8, B1, W0.classifier) | named-gate slug (singleton-smoke-green)
qualifier := free prose, captured not interpreted   — e.g. W2 (soft — §7 degrade)
```

**Semantics (verbatim law, Gate-1 #3): `gates-on: X` = *this row fires only after X closes.* Dependents declare their dependencies; the inverse ("unblocks") is NEVER encoded.** Multiple tokens = AND. A token *closes* when the row it resolves to reaches `✓`. A named-gate slug that resolves to no row stays **dangling** — rendered as a warning badge, never a build failure (§ 7.6), because named gates are events that may close in delta prose before any row exists.

### 7.5 Shape 5 — Matt queues
`canonical/matt_decision_needed/` + `canonical/matt_to_do/`: the `README.md` index is the modeled surface — an item = a heading or table row carrying a `Q`-style ID; **resolved** = `~~strikethrough~~` or residence in a resolved/appendix section. Counts feed the Glance header strip.

### 7.6 Severity split — the discipline that makes CI livable
This is the load-bearing enforcement contract. It is mirrored as **Discipline #60** in `engineering-disciplines.md` (CI-fail-loud); the two are ONE rule in two homes (the format-governance statement here; the engineering-enforcement statement there).

- **MALFORMED instance of a legislated shape → CI BUILD FAILURE, reported with file + line** — the same discipline as a broken test. The failure set is a **closed, enumerated, structurally-decidable set of exactly six conditions** (three for shapes 1–5; three for shape #6 FLOW, folded 2026-07-10 — § 7.9 amendment):
  - a queue row (§ 7.3) whose first cell begins with a row ID but whose table structure is broken (unparseable row);
  - a SESSION-DELTA heading (§ 7.2, `### YYYY-MM-DD — …`) whose date is unparseable;
  - a duplicate row ID within one board;
  - a FLOW list item (§ 7.8) missing its `←` separator;
  - a FLOW list item (§ 7.8) missing its bold `**<stage name>**`;
  - a FLOW list item (§ 7.8) with an unparseable ordinal.
- **UNRESOLVED reference** (a dangling `gates-on:` token, § 7.4; OR a FLOW section-ref resolving to no `##` heading, § 7.8) → **Glance warning badge** on the row/stage + a global "dangling dependencies" / `dangling_flow_refs` counter. Visible debt, **not** a broken build.
- **ABSENCE is never an error.** A doc with no delta log, a table that isn't a queue, a tracker with no `## FLOW` block — all fine. The parser models what matches the six shapes and renders the rest as prose.

### 7.7 Ratification amendments to gandalf's § 2 proposal (jack-ryan 2026-07-06)
Three tightening amendments; **zero scope expansion** (shape count held at five, per the minimum-legislation discipline):

1. **Shape-numbering imposed (7.1–7.5).** The proposal named the five shapes as prose sub-sections (2.1–2.6) without a stable shape ordinal. Ratified form numbers them Shape 1–5 so the CI failure message and the § 7.6 severity split can cite a shape by number ("malformed Shape 3 row at file:line"). Reduces ambiguity in CI output — Review Principle #5 (severity matters: findings cite a stable referent).
2. **MALFORMED is defined by an enumerated closed set, not an open "broken structure" phrase.** Ratified § 7.6 fixes the failure set to exactly three detectable conditions (broken table structure on an ID-bearing row · unparseable date on a delta heading · duplicate row ID within one board). A parser cannot fail loud on an open-ended predicate without producing false CI failures on legal free-prose docs (violating the "ABSENCE is never an error" floor). This bounds CI failure to structurally-decidable conditions — protecting the § 7.6 third bullet from erosion.
3. **The severity split is bound to Discipline #60 by name.** The proposal described CI behavior; ratification makes the format-doc statement and the engineering-discipline statement an explicit ONE-rule-two-homes pair (like § 6.2 canon↔tracker and § 6.8 OP↔skill), so neither can drift from the other. Twin-sync obligation applies.

**Held from the proposal unchanged:** the five shapes themselves, the status enum, the `gates-on:` grammar + AND-semantics + dangling-is-a-badge rule, the Matt-queue modeled surface, and the "keep writing parseably" minimum-obligation framing. The § 3 `state.json` output contract (Glance-internal) is NOT folded into canon — it is drax's build artifact, out of this doc's format-governance scope; it consumes § 7 but does not define it.

### 7.8 Shape 6 — FLOW declaration (added Glance-contract v1.1 2026-07-07, Matt-ruled fork (b); folded to canon 2026-07-10)

A `## FLOW` section near the top of a tracker declaring the doc's ordered end-to-end process view — the Tier-0 abstraction Matt asked for ("see the entire process for each system end to end, then drill in"). Grammar — an ordered list where each item is:

```
N. **<stage name>** ← <section-ref> [· <section-ref>]*
```

- **section-ref** = a substring of a `##` heading in the same doc (e.g. `PART III`). Resolution is **most-specific-first**: longer refs claim their headings before shorter refs bind (live case: the game tracker's `PART A′` must bind before `PART A`). **One heading maps to at most one stage.**
- **Stage state is DERIVED, never hand-stamped** — the founding derived-never-authored principle applied to stages. The parser aggregates the modeled queue rows (§ 7.3) under each stage's mapped sections into the standard counter object, plus a **dominant token** for rendering, precedence: `⛔ blocked > ⚖ awaiting_ruling > IN-FLIGHT > OPEN > PARKED > ✓`. A stage whose sections carry **no modeled rows** is `quiet` (rendered neutral — frame/lineage PARTs are legitimately row-less).
- **Severity (extends § 7.6):** section-ref resolving to no heading → **warning badge** + global `dangling_flow_refs` counter (visible debt, like a dangling `gates-on:` token) — never a build failure, because PARTs restructure and the FLOW map may lag a commit. Tracker with no `## FLOW` at all → fine (absence); its Tier-0 card renders without a flow-bar. **Malformed list item** inside a declared FLOW (missing `←`, missing bold stage name, unparseable ordinal) → **CI failure** — malformed instance of a legislated shape, per § 7.6 (the enumeration is closed at six conditions).
- **Maintenance obligation:** the FLOW map is **authored** (it is a declaration, not a derivation) — whoever restructures a tracker's PARTs updates its FLOW refs in the **same commit**. The dangling-ref badge is the drift alarm. Sibling obligation to the § 6.2 `Tracker-delta:` rule and the § 6.8 OP↔skill twin rule: a same-commit sync that keeps two coupled surfaces from drifting.

### 7.9 Delta-ratification amendments — folding shape #6 FLOW into the five-shape contract (jack-ryan 2026-07-10)

Shape #6 was added to the Glance contract (v1.1, § 2.7) on 2026-07-07, *after* the 2026-07-06 five-shape ratification. Per § 9 ("a parse-shape is added or amended → proposer→ratifier round required"), the sixth shape required its own ratification touch. Reviewed at Gate-1 for internal consistency, ambiguity, and enforceability. **PASS-WITH-NOTES.** Two tightening amendments; the shape itself is held as proposed:

1. **The MALFORMED enumeration is re-closed at exactly SIX conditions** (§ 7.6). The § 7.7 amendment #2 pinned MALFORMED to a *closed enumerated set* precisely so a parser cannot fail loud on an open-ended predicate (which would false-positive on legal free-prose docs and erode the "ABSENCE is never an error" floor). Shape #6 adds a fourth condition-*class* (malformed FLOW list item), which itself decomposes to three structurally-decidable conditions (missing `←` · missing bold stage name · unparseable ordinal). The fold widens the closed set from three to six conditions — **still closed, still structurally-decidable, floor preserved.** An open-ended "malformed FLOW" predicate would have been a BLOCK; the enumerated form is not.
2. **FLOW's two dangling classes are bound to the § 7.6 warning tier explicitly.** A section-ref resolving to no heading is a warning badge + `dangling_flow_refs` counter — parallel to the dangling `gates-on:` token, and for the same reason (PARTs restructure; the map may lag one commit; forward-declared structure is legal-in-flight, not malformed). This keeps FLOW on the right side of the truthful-vs-livable line the three-tier split defends.

**Held from the § 2.7 proposal unchanged:** the FLOW grammar, most-specific-first section-ref resolution, one-heading-↔-at-most-one-stage, the derived-never-authored stage-state rule + dominant-token precedence, the `quiet` neutral state, and the same-commit authored-map maintenance obligation. Discipline #60 is amended in the same commit to carry the six-condition enumeration (twin-sync, § 6.8). **Enforceability confirmed empirically:** all five live product-pipeline docs (`pipeline-battle-sim` S0–S8 · `pipeline-serial-content-emission` E0–E8 · `pipeline-story` N0–N5 · `pipeline-game` G0–G8 · `pipeline-arcade` A0–A7) carry grammar-conformant `## FLOW` blocks as of 2026-07-10 — the shape is real, rendering live, and the ratification governs actual authored surface.

---

## 8. Ownership lineage (fixed 2026-06-30 — trackers replace the retired roadmap)

- **`canonical/00-ground-state.md`** (router) — gandalf authors + maintains
- **`canonical/current-to-end-state/…-engine.md` + `…-story.md`** (trackers) — **gandalf + knight-rider write; all other agents read + surface deltas** (write-authority ruling, Matt 2026-06-30). *(Replaces the retired `canonical/02-roadmap.md`, killed in the 2026-06-30 reorg.)*
- **`canonical/reap-die-rise-{story,engine,game}/`** (spec folders) — gandalf primary (story); gandalf + the engine seam owners (engine); gandalf spec-side + drax build-side (game), per `00-index.md`
- **Numbered-spine docs** (`canonical/reap-die-rise-engine/<NN>-<topic>.md`, moved into the engine spec 2026-07-01) — gandalf primary; knight-rider orchestration-side; jack-ryan process-side
- **Design/lore/recognition docs in the spec folders** (`<topic>-YYYY-MM-DD.md`) — primarily gandalf; occasionally jack-ryan (process), gamora (sim-architecture), star-lord (pipeline-architecture)
- **Supersession / prune execution** — gandalf approves design-side; the hygiene Routine auto-fires the safe tier; knight-rider executes any restructure dispatch
- **Doc-lifecycle RULE-ownership (§ 6.7, Matt 2026-06-30)** — **jack-ryan ratifies** the governance rules (symmetry with engineering-disciplines); **gandalf proposes + executes.** Rule-authoring that affects gandalf's own output routes to jack-ryan via the named `⚠ SWITCH: CANON-STEWARD (proposer) → jack-ryan (ratifier)` beat

---

## 9. Update protocol for this skill

This skill evolves when: a new STATUS state lands (rare); a new header field becomes load-bearing; a new recognition-record or lifecycle pattern is established; a canon-home partitioning changes; **a parse-shape is added or amended (§ 7 — proposer→ratifier round required).** **Keep the OP source (`agentic_orchestration/operating-procedures/canonical-doc-format.md`) and the installed SKILL (`.claude/skills/reincarnated-canonical-doc-format/SKILL.md`) in sync** — they are the same content in two locations.

Authored / maintained by **gandalf** (cross-cutting reference owner + primary canonical-doc author).

---

**Signed:** gandalf (§ 1–6, 8–9); jack-ryan (§ 7 parse-contract ratification, 2026-07-06; § 7.8/§ 7.9 shape #6 FLOW delta-ratification, 2026-07-10)
**For:** the universal **format + lifecycle** spec for canonical docs. Header + STATUS + cross-reference rules (§ 1–5); the authoring → propagation → pruning system (§ 6): the `Tracker-delta:` convention, the five-predicate prune-safe rule (amended 2026-08-24), three note-classes, total-vs-partial supersession, and the hygiene Routine; and (§ 7) the parse contract — the six legislated shapes (STATUS · SESSION-DELTA · queue rows · `gates-on:` · Matt queues · FLOW) + the CI severity split (mirrored as Discipline #60). Canon-home truth remains `canonical/00-ground-state.md`.
