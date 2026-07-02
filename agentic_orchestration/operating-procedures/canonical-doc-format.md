# reincarnated-canonical-doc-format — Canonical Doc Format + Lifecycle (Cross-cutting Reference)

> **STATUS:** CURRENT (load-bearing). First authored 2026-05-23 (Stream 3 cross-cutting reference skill). **Amended 2026-06-30 — doc-lifecycle governance added (§ 6): propagation + pruning system, ratified by Matt 2026-06-30 after a 14-scenario stress-test.** The pre-amendment "demote to `canonical/historical/` subfolder" model is RETIRED (the reorg went git-is-archive); reconciled in § 1 + § 3.

**Authored:** 2026-05-23 · **Amended:** 2026-06-30 (lifecycle governance)
**Author:** gandalf (cross-cutting reference owner + primary canonical-doc author)
**Authority:** Matt 2026-06-30 — doc-lifecycle governance (the four rulings: total-vs-partial supersession, auto-prune ceiling, three note-classes, markdown-only scope)
**Authoritative source for canon status:** `canonical/00-ground-state.md` (the thin router — the three canon homes)
**Companion skills:** `reincarnated-engineering-disciplines`; `reincarnated-decision-log-format`; `reincarnated-critique-pair-gate-protocol`; `reincarnated-hive-mind-protocol`

---

## 0. What this skill IS and IS NOT

**IS:** the universal **format + lifecycle** spec for canonical docs at `canonical/` (numbered keystone docs + the spec folders) and `canonical/story/` (story + lore + design artifacts). Names: header structure, STATUS protocol, cross-reference rules, **and (§ 6) the authoring → propagation → pruning lifecycle** — how a canonical write feeds the current-to-end-state trackers, and when a doc/note is pruned. Loaded by any agent authoring or amending canonical artifacts.

**IS NOT:** the substantive content guide (each doc's substance is per-topic). NOT the router itself (`canonical/00-ground-state.md` is always the source of canon-home truth). NOT the decisions-log format (`reincarnated-decision-log-format`). NOT a lifecycle for **data / code / binary** artifacts — those (`.json`, `.csv`, `.py`, `.png`, `.mp4`, `.html`) live under their seam owner's lifecycle, explicitly **out of § 6 scope** (§ 6.3).

---

## 1. Where canon lives (reconciled 2026-06-30 — git is the archive)

Canon lives in **three homes** (per the router, `canonical/00-ground-state.md`):

| Home | Contents |
|---|---|
| `canonical/reap-die-rise-story/` + `canonical/reap-die-rise-engine/` | the END-STATE **spec** folders (story frame; engine spec). Each has a `00-index.md` fold-worklist. |
| `canonical/current-to-end-state/` | the **delta** trackers — `…-engine.md` (build-vs-spec gaps) + `…-story.md` (open story decisions). LIVING. |
| `canonical/` (numbered) + `canonical/story/` | keystone docs (37–51 still folding into the spec folders) + story/design/lore artifacts + recognition records |

**Anything older — superseded designs, epoch history, the old historical/dead registry — lives in git, recoverable, not pre-load.**

**Retired 2026-06-30:** the `canonical/historical/` and `canonical/dead/` **subfolders** (they no longer exist). The old model relocated demoted docs into those subfolders to keep them in-tree as lineage. The reorg replaced that with **git-is-archive**: a fully-superseded doc is **removed from the live tree** (git keeps it), not relocated to a subfolder. The STATUS *stamps* CURRENT / HISTORICAL / DEAD survive as **in-doc labels** (§ 3); only the subfolder *relocation* is gone.

**Authoring rule:** new docs land in a spec folder (end-state), `canonical/current-to-end-state/` (a tracker), `canonical/` (keystone), or `canonical/story/` (design/lore). They leave the live tree only via the lifecycle in § 6 (supersession or workstream-close → git-lineage).

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

- **Path-based** — `canonical/story/<doc>.md`, not URL-style
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

**A doc/note AUTO-prunes (git-rm; git is the archive) only if ALL four hold:**
1. **Markdown design artifact** — not data / code / binary (those are seam-owner lifecycle, out of scope)
2. **Not a never-prune class** (below)
3. **Either TOTALLY superseded (§ 6.4) OR a working-memory note whose workstream closed**
4. **Zero live references across BOTH repos** — the reference check greps `decisions-log` + `engineering-disciplines` + all OPs + all skills + `canonical/` + the trackers, in **both** the collab meta-repo and `reincarnated-engine/` (decisions-log lives there and cites collab-repo notes)

If 1–2 hold but 3–4 are ambiguous → **surface for ratification**, never auto-fire. **"Became irrelevant" has no detectable event — it is ALWAYS surface-for-ratification, never auto-pruned.**

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
2. runs the cross-repo reference check (§ 6.3 predicate 4);
3. **auto-prunes the four-predicate-safe tier** (git-rm; in-scope auto-commit);
4. **surfaces the judgment tier** (ambiguous / "became irrelevant") as a prune-list for Matt's ratification;
5. flags canonical commits missing a `Tracker-delta:` footer (§ 6.2 enforcement);
6. collapses resolved-and-aged tracker rows into the CLOSED appendix (§ 6.5).

**Distribute routine, centralize judgment:** each agent self-prunes its own working-memory notes at workstream-close; the gandalf sweep handles cross-cutting residue + the judgment tier + tracker collapse. Scales as agents are added.

### 6.7 Rule-ownership — who RATIFIES doc-lifecycle governance (Matt 2026-06-30)

The § 6 *rules* are a discipline, and a discipline has a conflict-of-interest hazard when the author is also its largest subject. gandalf is the meta-repo's largest note-producer; a gandalf-authored prune-rule that softens treatment of steward notes (the S15 finding, stress-test § 4) is **rule-maker = rule-subject** — the developer↔judge conflict transposed to governance. Matt 2026-06-30 ruled the fix by **symmetry with engineering-disciplines**:

- **jack-ryan RATIFIES doc-lifecycle rules** (the same way jack-ryan owns engineering-disciplines — the rules engineers run under; § 6 is the sibling: the rules doc-producers run under).
- **gandalf PROPOSES + EXECUTES** (proposes mechanisms as the practitioner who feels the pain; executes the prune/propagation on the established rules).
- The **switch-moment is named in the open:** when gandalf proposes a governance rule — *especially one affecting gandalf's own output* — gandalf emits `⚠ SWITCH: CANON-STEWARD (proposer) → jack-ryan (ratifier)` (gandalf OP § 2 role-tags) and routes the rule to jack-ryan before it is canon.
- **Execution is not the conflict.** gandalf (or any seam-owner on their own notes) *running* an established rule is fine — the conflict is only at rule-*authoring*. So proposal → gandalf; ratification → jack-ryan; execution → gandalf + seam-owners.

**Pending ratification:** the **S15 substance-homing refinement** (stress-test § 4) is Matt-agreed *content* but its ratification-ownership now sits with jack-ryan — jack-ryan reviews S15 on next governance touch and either ratifies it into § 6.1/§ 6.3 or returns it. Until then S15 is Matt-agreed-but-not-jack-ryan-ratified, flagged as such in the stress-test record.

---

## 7. Ownership lineage (fixed 2026-06-30 — trackers replace the retired roadmap)

- **`canonical/00-ground-state.md`** (router) — gandalf authors + maintains
- **`canonical/current-to-end-state/…-engine.md` + `…-story.md`** (trackers) — **gandalf + knight-rider write; all other agents read + surface deltas** (write-authority ruling, Matt 2026-06-30). *(Replaces the retired `canonical/02-roadmap.md`, killed in the 2026-06-30 reorg.)*
- **`canonical/reap-die-rise-{story,engine}/`** (spec folders) — gandalf primary (story); gandalf + the engine seam owners (engine), per `00-index.md`
- **`canonical/<NN>-<topic>.md`** (keystone) — gandalf primary; knight-rider orchestration-side; jack-ryan process-side
- **`canonical/story/<topic>-YYYY-MM-DD.md`** — primarily gandalf; occasionally jack-ryan (process), gamora (sim-architecture), star-lord (pipeline-architecture)
- **Supersession / prune execution** — gandalf approves design-side; the hygiene Routine auto-fires the safe tier; knight-rider executes any restructure dispatch
- **Doc-lifecycle RULE-ownership (§ 6.7, Matt 2026-06-30)** — **jack-ryan ratifies** the governance rules (symmetry with engineering-disciplines); **gandalf proposes + executes.** Rule-authoring that affects gandalf's own output routes to jack-ryan via the named `⚠ SWITCH: CANON-STEWARD (proposer) → jack-ryan (ratifier)` beat

---

## 8. Update protocol for this skill

This skill evolves when: a new STATUS state lands (rare); a new header field becomes load-bearing; a new recognition-record or lifecycle pattern is established; a canon-home partitioning changes. **Keep the OP source (`agentic_orchestration/operating-procedures/canonical-doc-format.md`) and the installed SKILL (`.claude/skills/reincarnated-canonical-doc-format/SKILL.md`) in sync** — they are the same content in two locations.

Authored / maintained by **gandalf** (cross-cutting reference owner + primary canonical-doc author).

---

**Signed:** gandalf
**For:** the universal **format + lifecycle** spec for canonical docs. Header + STATUS + cross-reference rules (§ 1–5) and the authoring → propagation → pruning system (§ 6): the `Tracker-delta:` convention, the four-predicate prune-safe rule, three note-classes, total-vs-partial supersession, and the hygiene Routine. Canon-home truth remains `canonical/00-ground-state.md`.
