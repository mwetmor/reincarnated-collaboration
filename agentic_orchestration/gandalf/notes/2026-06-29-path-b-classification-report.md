# Path B — Spine-Membership + Inbound-Link Classification Report

**STATUS:** CURRENT (operational audit trail) — the mechanical classification that authorizes the Path B vestigial-bulk delete.
**Author:** gandalf, 2026-06-29 (Path B step 1, per Matt's accepted method).
**Companion:** `canonical/reap-die-rise/00-index.md` (Path A supersession map); `canonical/story/current-to-end-state.md` (LIVING tracker).
**Method authority:** Matt 2026-06-29 verbatim — *"1. Spine-membership + inbound-link classification (mechanical — no reading). 2. Delete the presumptive-vestigial bulk in revertable per-category commits. 3. Reserve all careful reading for the keep-set intra-doc surgery."*

---

## 1. Principle

**git-is-archive.** Hard-delete from the working tree is git-recoverable; no `archive/` folder is created. Precondition (satisfied): every deleted file was committed first (baseline `20a73a2` captured all untracked + in-flight tracked work before any delete).

**Classification is mechanical — no content reading.** A doc is KEPT if it is (a) on the canonical spine, OR (b) one-hop inbound-linked from a protection source, OR (c) recent (in-flight work guard). Everything else in `agentic_orchestration/` is presumptive-vestigial and deleted. Careful reading is reserved for the `canonical/` keep-set surgery (Path B step 3 + Path A patron correction), NOT for this bulk.

**Scope of THIS pass:** `agentic_orchestration/` only. `canonical/` (220 docs: 177 story + 17 root + 15 historical + 10 reap-die-rise + 1 dead) is handled SEPARATELY and carefully in step 3, using `00-ground-state.md` §1 CURRENT-table as keep-authority — NOT bulk-filtered.

---

## 2. Protection sources (the spine + one-hop neighborhood)

Inbound-link protection is computed by extracting every `*.md` path-reference from these sources, then intersecting with the tracked `agentic_orchestration/` corpus:

- **Spine:** `canonical/story/current-to-end-state.md` (LIVING tracker); `canonical/00-ground-state.md` (+ its §1 CURRENT-table doc list).
- **Path A v2 set:** `canonical/reap-die-rise/` (10 docs incl. `00-index.md`).
- **Governance first-reads:** `agentic_orchestration/AGENTS.md`, `GOVERNANCE.md`, `REVIEW_PROCESS.md`.
- **Operating procedures:** `agentic_orchestration/operating-procedures/*.md` (role OPs + protocol docs).
- **Role definitions:** `.claude/agents/*.md` (14 federated agents).

Extraction yielded **739 distinct `*.md` path-refs**. Intersected with the tracked `agentic_orchestration/` corpus → **215 inbound-protected docs**.

**Validation (extraction is sound):** the gandalf OP cites three founding-precedent notes by exact path —
`gandalf/notes/2026-05-23-phase-E-1-bis-design-fit-verdict.md`,
`…/2026-05-23-question-A-w1-13-tier-4-hypothesis-verdict.md`,
`…/2026-05-23-phase-E-1-kernel-panic-diagnosis.md`.
All three are correctly classified PROTECTED (not in the delete list). The inbound-link guard catches real citations.

---

## 3. Recency guard (in-flight work protection)

Beyond inbound-links, any `agentic_orchestration/` doc whose filename carries an embedded ISO date **≥ 2026-06-15** is protected, to shield in-flight cycle work (e.g., the 2026-06-22 drax Path-B dispatch, the 2026-06-19 gandalf crypt-vault note — both seen modified in the working tree). This guard is a conservative safety addition beyond Matt's stated two criteria; it errs toward keeping recent work.

---

## 4. The numbers (reconcile to corpus)

| Bucket | Count |
|---|---|
| **Total tracked `agentic_orchestration/*.md`** | **2002** |
| KEPT — inbound-link protected | 215 |
| KEPT — recency-protected (≥2026-06-15, not inbound) | 252 |
| KEPT subtotal | **467** |
| DELETE-candidate (vestigial) | **1535** |
| — minus infra-reserve (see §6) | −3 |
| **FINAL bulk delete** | **1532** |

**Integrity checks (all passed, under `LC_ALL=C`):**
- delete-candidates NOT git-tracked: **0** (every deletion is a tracked file → recoverable)
- delete-candidates intersecting the protected set (guard breach): **0**
- delete-candidates with date ≥ 2026-06-15 (recency breach): **0**
- `node_modules/**/*.md` (16 vendored READMEs): out of scope — git-untracked, 0 in either list.

---

## 5. Per-category bulk breakdown (1532)

Operational exhaust — consumed orchestration/QA/research/per-agent working artifacts. Each category deleted as its own revertable commit.

| Category | Count | Nature |
|---|---|---|
| `dispatches/` | 649 | consumed orchestration dispatches |
| `gandalf/` | 215 | consumed design notes (recent ones protected by §3) |
| `qa/` | 133 | consumed Gate-1/Gate-2 findings |
| `legolas/` | 123 | consumed research + crawl artifacts |
| `research/` | 72 | consumed research artifacts |
| `elrond/` | 66 | consumed catalogue-curation artifacts |
| `rocket/` | 65 | consumed generation-seam notes |
| `_root` (loose `agentic_orchestration/*.md`) | 49 | skill-handoffs, wave-summaries, briefings, state files |
| `hive-mind/` | 36 | consumed hive-mind state |
| `mantis/` | 19 | consumed UE-spike notes |
| `gamora/` | 17 | consumed simulation-seam notes |
| `david-h/` | 17 | consumed PC-orchestration notes |
| `knight-rider/` | 15 | consumed orchestration notes |
| `galadriel/` | 11 | consumed vision-pipeline notes |
| `jack-ryan/` | 10 | consumed QA-design notes |
| `drax/` | 10 | consumed presentation-seam notes |
| `star-lord/` | 8 | consumed pipeline-seam notes |
| `radagast/` | 4 | consumed PC-design notes |
| `fable-5-eval/` | 3 | consumed eval artifacts |
| `cycles/` | 3 | consumed cycle-scope docs |
| `sam/` | 2 | consumed PC-QA notes |
| misc cycle wave-states | 4 | `cycle-15/16/18` wave-state + `logs/` |

---

## 6. Infra-reserve (excluded from bulk; reserved for careful review)

Three singletons live in **infrastructure** directories, not exhaust directories — held back from the mechanical bulk:

- `operating-procedures/work-cycle-skeleton.md` — work-cycle template (operational infrastructure; the rest of `operating-procedures/` is protected).
- `pc-setup/CLAUDE.md` — active Claude Code configuration file, not a doc.
- `memory-annotations/2026-05-16-suggestion-project-ailment-damage-thematic.md` — design-suggestion record tied to the `project_ailment_damage_thematic` auto-memory entry.

These are reviewed in step 3, not blind-deleted.

---

## 7. Reversibility

Each category is a single `git rm` + commit. To restore any category: `git revert <sha>` (or `git checkout <sha>^ -- <paths>`). The full pre-purge tree is at baseline `20a73a2`.

**Signed:** gandalf, 2026-06-29 — Path B step 1 complete; authorizes step 2 (bulk delete).
