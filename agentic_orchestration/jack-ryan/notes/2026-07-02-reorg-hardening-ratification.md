# Ratification — 2026-07-02 — reorg-hardening (commit b2485af)

**Reviewer:** jack-ryan (governance-ratifier mode; the proposer→ratifier seam per canonical-doc-format.md § 6.7)
**Proposer/executor:** gandalf
**Target:** `b2485af` (on main, pushed) — the B-hardening half of the bundled A&B pass following the 2026-06-30→07-01 canonical reorg + the One Realm MVP ruling
**Authority:** Matt 2026-07-02 (ratification set authorized as part of the A&B hardening)
**Principles applied:** REVIEW_PROCESS #4 (decisions-log/canon as single source of truth) · #3 (cross-seam impact) · #5 (severity matters) · ADR-002 (tiered approval — documentation/process governance is jack-ryan-approvable)

---

## 0. TL;DR — four verdicts + two graduation rulings

| Item | Verdict |
|---|---|
| 1. OP § 4.8 Queue↔tracker sync rule | **RATIFY-WITH-AMENDMENT** (one enforceability tightening) |
| 2. OP § 4.9 Tracker-accretion pruning | **RATIFY-WITH-AMENDMENT** (two evidentiary-lineage guards) |
| 3. Three hygiene-routine tripwires + never-prune extension | **RATIFY** (as-written; sound) |
| 4. Live OP↔skill drift (flagged-not-repaired) | **RATIFY the flag; two rulings issued** (repair = gandalf as twin owner; twin-sync GRADUATES to a standing rule → routes to gandalf to execute in canonical-doc-format.md § 6) |
| Graduation of § 4.8/§ 4.9 → engineering-disciplines.md | **NO — stay OP-local.** Process-governance, not engine-engineering. Home is canonical-doc-format.md § 6 if they graduate anywhere. |

All four items verified against the live tree — the evidence-cases are real (see § 5). Nothing here is aspirational-only; the two amendments exist specifically to keep the rules enforceable rather than exhortative.

---

## 1. Item 1 — OP § 4.8 Queue↔tracker sync rule → **RATIFY-WITH-AMENDMENT**

**What it says:** the Matt-surfaces (`matt_decision_needed/`, `matt_to_do/`) and the trackers are ONE state projected twice; any unit that edits a feeding tracker row re-syncs the queue row in the same unit, and vice versa; the queue may never ask a question the tracker has killed.

**Sound.** The evidence-case is confirmed live: story-tracker A11 (`current-to-end-state-story.md` line 99) killed the molt→companion premise; B2 closed into B3 (line 110); yet the queue had carried the dead molt→companion question — which the `matt_decision_needed/` RESOLVED appendix now documents as restated. This is exactly the failure a single-state-projected-twice rule prevents. The rule is correctly bidirectional and correctly scoped to "the same unit of work."

**The concern I checked (per the task):** is "same unit of work" *enforceable* or merely *aspirational*? As written it is exhortative — a unit that edits a tracker row and forgets the queue row violates the rule silently, and nothing catches it until the cron tripwire (c) fires on its weekly cadence (and that routine is itself BLOCKED on the CCR environment, `matt_to_do/` T1). Between now and CCR-instantiation the rule has no enforcement surface. That is a real gap, not a fatal one.

**AMENDMENT 1 (required) — bind the mechanical check to session-end, not just cron.** § 4.8's "Mechanical check (cheap)" already points at § 5 step 2b, but § 5 step 2b (both OP and skill) does NOT yet name the pointer-walk. Make the enforcement concrete: § 5 step 2b must gain an explicit sub-step — *"for every open queue row touched this session (or feeding a tracker row touched this session), follow its source pointer and confirm the pointed-at row is still OPEN and asks the same question; re-sync in this commit if not."* This converts "same unit of work" from an intention into a session-end checklist item with a named actor and a named moment. This is a canonical-doc-format-adjacent edit to the gandalf OP § 5 + skill § 5 — **routes to gandalf to execute** (proposer-executes; it is gandalf's own OP). Not a blocker on the § 4.8 rule text itself, which ratifies as-is.

**Verdict:** RATIFY the § 4.8 rule as written; AMENDMENT 1 lands the enforcement hook in § 5 step 2b (gandalf executes). Cite: REVIEW_PROCESS #4 (one source of truth), #3 (the queues are a cross-surface projection).

---

## 2. Item 2 — OP § 4.9 Tracker-accretion pruning → **RATIFY-WITH-AMENDMENT**

**What it says:** collapse-never-delete at any tracker touch — resolved-and-aged rows (resolved ≥2 sessions back, no live cross-ref citing them *as open*) → one-line CLOSED-appendix entries; SESSION-DELTA entries older than the last two *governing* pivots → one-line summaries (full text in git); guard against collapsing a row cited by an open dispatch / unratified BANKED item / open Matt-queue row.

**Sound in architecture.** "Collapse, never delete" is the correct shape — it matches canonical-doc-format.md § 6.5 (trackers are LIVING; resolved ≠ deleted; reopening is common — B3 is the live proof, reopened 2026-06-30). The size pressure is real (engine tracker is 433 lines / ~19.5K tokens by char-count today; the "~31K token" figure is a tokenizer estimate — either way it is monotonic and heading past the § 1 15–25-min read budget). Collapsing to a CLOSED appendix + compressing stale SESSION-DELTA to one-liners with full text in git is the right lever.

**The concern I checked (per the task):** can § 4.9's collapse criteria destroy evidentiary lineage? The rule as written keeps full text in git and keeps a one-line stub in-tree — so on its face nothing is *lost*. But two edges can degrade evidentiary lineage in ways the current guard misses:

**AMENDMENT 2a (required) — the collapse guard must include the § 6.3 cross-repo reference check, not just "cited as open."** § 4.9's guard says "no live cross-ref citing them *as open*." That is too narrow. A resolved tracker row can be cited by `decisions-log.md` **in the engine repo** as *evidence for a ratified decision* (not "as open" — as lineage). Collapsing its detail to a one-liner would leave the decisions-log citation pointing at a stub, degrading the evidentiary chain even though git retains the text. The guard must read: *never collapse a row whose detail is cited as evidence/source by decisions-log, an OP, a skill, or canonical — across BOTH repos* (the same predicate-4 check canonical-doc-format.md § 6.3 already mandates for prunes). This aligns § 4.9's guard with the established prune-safe predicate rather than inventing a weaker one.

**AMENDMENT 2b (required) — "governing pivots" needs a definition anchor to be non-arbitrary.** "SESSION-DELTA entries older than the last two *governing* pivots" is unenforceable without a shared definition of "governing pivot" — one editor's governing pivot is another's routine delta, and an over-eager collapse could bury the reasoning trail behind a decision that later reopens. Anchor it: a *governing pivot* is a SESSION-DELTA entry that (i) locked or reversed a tracker PART-level item, OR (ii) is cited by a still-open row, OR (iii) carries a Matt ruling. Anything not meeting one of those three is compressible; anything meeting one is retained in full. This makes the "last two" boundary auditable instead of judgment-by-vibe.

Neither amendment changes the rule's intent — both harden it so a well-meaning collapse cannot quietly amputate the reasoning a future reopen (or a decisions-log citation) depends on. Both edit the § 4.9 text in the gandalf OP + skill → **route to gandalf to execute.**

**Verdict:** RATIFY the § 4.9 collapse-never-delete shape; require AMENDMENTS 2a (cross-repo reference guard, per § 6.3 predicate 4) + 2b (governing-pivot definition anchor) before the rule is enforcement-grade. Cite: canonical-doc-format.md § 6.5 (tracker hygiene), § 6.3 predicate 4 (cross-repo reference check), § 6.1 evidentiary note-class (never-degrade lineage).

---

## 3. Item 3 — three hygiene-routine tripwires + never-prune extension → **RATIFY (as-written)**

The three tripwires added to `canonical-hygiene-audit-routine.md` step 7 are sound and correctly scoped as **flag-only, no auto-fix** (which is the right authority level — the routine surfaces, humans/twin-owners repair):

- **(a) dead-home regression** — verifies `canonical/story|historical|dead` do NOT re-exist, with `git log --diff-filter=A` to name the creating commit. Correct: these homes were dissolved/retired in the reorg (confirmed against canonical-doc-format.md § 1). A rebuilt dead home is exactly the kind of silent reorg-decay a tripwire should catch, and naming the creating commit makes it actionable.
- **(b) OP↔SKILL twin drift-diff** — diffs each OP/skill twin body (ignoring YAML frontmatter), flags the pair + first divergent section, explicitly leaves repair to the twin's owner. Correct authority split. It even pre-declares the known gandalf-pair drift at §4.7/§5 as an expected first-fire flag — good faith, and it matches what I confirmed live (§ 5 below).
- **(c) Matt-queue staleness** — the cron half of § 4.8's mechanical check; follows each open queue row's source pointer. Correct — this is the enforcement surface § 4.8 needs on a cadence (and AMENDMENT 1 gives it the session-time twin).

**Never-prune extension** — adding the three trackers + both Matt queues to the never-prune class is correct and already consistent with canonical-doc-format.md § 6.3's never-prune class (which names the trackers, the router, and — as of the game-home founding — should name all three trackers + both queues). The routine's step-1 exclusion list in the standalone prompt already reflects this. Ratified.

**One INFO note (non-blocking):** the routine remains BLOCKED on CCR-environment instantiation (`matt_to_do/` T1). Until that clears, tripwires (a)/(b)/(c) do not run on cadence — which is precisely why AMENDMENT 1 (session-end pointer-walk) matters as the interim enforcement surface for (c). No action beyond noting the dependency.

**Verdict:** RATIFY as-written. Cite: canonical-doc-format.md § 6.6 (the Routine), § 6.3 (never-prune class), REVIEW_PROCESS #4.

---

## 4. Item 4 — live OP↔skill drift (flagged-not-repaired) → **RATIFY the flag; TWO RULINGS**

**The drift is real — I confirmed it by reading both files directly (not just trusting the flag):**
- **§ 4.7:** OP has 6 composition bullets and closes with the § 4.6 / Discipline #43 wave-close stack; the skill's § 4.7 has only 4 bullets and is MISSING the § 4.6 wave-close composition bullet entirely.
- **§ 5 step 2:** OP names all THREE trackers (engine/story/game) and has a step 2b (decision-queue update); the skill's § 5 step 2 names only TWO trackers and has NO step 2b.
- **§ 1 step 2 (bonus find, beyond the flag):** the skill's session-start § 1 step 2 also names only two trackers ("gandalf spans both") — the game-tracker is absent there too. So the drift is wider than the flag stated: it is §1 + §4.7 + §5, not only §4.7/§5.

Additionally the skill's § 3.7 corresponds to the OP's § 3.8 (numbering offset) and the skill lacks the Discipline #42/#43 composition depth the OP § 4.7 carries — consistent with the task's framing.

### RULING (i) — who repairs: **gandalf, as twin owner.**
canonical-doc-format.md § 8 already states the twins "are the same content in two locations" and must be kept in sync; the hygiene routine tripwire (b) explicitly assigns twin-drift repair to "the twin's owner, NOT auto-fixed by this routine." gandalf owns both files (authored + self-maintains per OP § 7). So repair is gandalf's, not a jack-ryan write and not a routine auto-fix. **This is a documentation-only within-scope edit → jack-ryan APPROVES it directly under ADR-002; no Matt escalation needed.** Scope of the repair: bring skill §1 step 2 (three trackers), §4.7 (add the §4.6 wave-close composition bullet + the Discipline #42/#43 stack), and §5 (add step 2b + the third tracker in step 2) into parity with the OP. gandalf executes.

### RULING (ii) — does OP↔skill twin-sync graduate to a standing rule in canonical-doc-format.md § 6: **YES.**
Rationale: the drift is not a one-off; it is a *structural* hazard of the twin architecture (two files, one content, no enforcement) — the same class of silent-decay that § 6 was built to eliminate ("nothing depends on someone remembering to clean up or to update the trackers," § 6 preamble). A twin-sync obligation is the exact sibling of the `Tracker-delta:` propagation convention (§ 6.2): both say *"when you touch one projection of a shared state, update the other in the same unit."* It belongs in § 6 as a first-class rule, not buried in § 8's update-protocol prose and the routine's tripwire.

**What to write (routes to gandalf to execute — proposer-executes; § 6 is canonical-doc-format.md, gandalf-owned; jack-ryan ratifies the rule, which this note does):** a new **§ 6.8 — OP↔SKILL twin-sync** stating:
1. Every `operating-procedures/<name>.md` with a `.claude/skills/reincarnated-*<name>*/SKILL.md` twin is ONE content in two locations; any edit to one is applied to the other **in the same commit** (skill YAML frontmatter excepted).
2. Drift is detected by the hygiene routine tripwire (b) and repaired by the **twin's owner** (never auto-fixed by the routine).
3. This is the twin-file sibling of the § 6.2 `Tracker-delta:` propagation rule and the § 4.8 queue↔tracker sync rule — the general principle is: *a shared state projected into N artifacts re-syncs all N in the unit that touches any one.*

I am **ratifying** this rule now (that is this note's authority under § 6.7); gandalf **executes** the § 6.8 write (the text lives in a gandalf-owned canon file, and § 6.7 assigns § 6 rule-*execution* to gandalf while ratification sits with jack-ryan — which is exactly this split).

**Verdict:** RATIFY the flag as accurate (and note it under-stated the scope — §1 is also drifted); RULING (i) gandalf repairs, jack-ryan-approved under ADR-002; RULING (ii) twin-sync GRADUATES → new canonical-doc-format.md § 6.8, ratified here, gandalf executes.

---

## 5. Graduation ruling — do § 4.8 / § 4.9 leave the OP for engineering-disciplines.md? → **NO. Stay OP-local (home = canonical-doc-format.md § 6 if anywhere).**

The task hands me this call (precedent: OP § 4.2 — the OP captures, jack-ryan canonicalizes to engineering-disciplines.md when ready, for *engine-engineering* disciplines like Discipline #18). That precedent does NOT extend here, because § 4.8/§ 4.9 are **process-governance of the canon/queue system**, not engine-engineering disciplines. engineering-disciplines.md is the rules *engineers run under* (math-before-code, smoke-gate, cross-seam MIGRATION, attribution). § 4.8/§ 4.9 are the rules *doc-and-queue producers run under* — which is precisely what canonical-doc-format.md § 6 already is (its own § 6.7 names the symmetry: "§ 6 is the sibling: the rules doc-producers run under"). Putting a queue-sync rule in engineering-disciplines.md would miscategorize it and dilute that doc's engine-engineering focus.

**So:** § 4.8/§ 4.9 stay in the gandalf OP as the *capture* location (correct for a gandalf-practiced discipline). IF they graduate to a cross-cutting standing rule (and § 4.8 is a strong candidate — it is not gandalf-specific; KR co-maintains the queues, and any agent may surface a row), the destination is **canonical-doc-format.md § 6**, NOT engineering-disciplines.md. I am not forcing that graduation now — § 4.8/§ 4.9 are young (one evidence-case each); OP-local with the § 6.6 routine + AMENDMENT-1 session-end hook is sufficient enforcement for now. Revisit graduating § 4.8 → § 6 (as the general "shared-state-projected-N-times" rule that § 6.8 twin-sync will already gesture at) after it has caught a second live case. That empirical criterion — a second independent queue↔tracker desync caught by the rule — is the gate; not time-passage.

**engineering-disciplines.md writes I am making this session:** NONE. Nothing here is an engine-engineering discipline. (Contrast: had this been a Discipline #18/#42/#43 refinement, it would be my direct write.) This is the correct outcome — the reorg-hardening rules are canon/process governance, and their canonical home is the § 6 system, executed by gandalf.

---

## 6. Consolidated action list

| # | Action | Owner | Authority |
|---|---|---|---|
| A1 | § 4.8 ratified as-written (rule text stands) | — | jack-ryan RATIFIED |
| A2 | AMENDMENT 1 — add session-end pointer-walk sub-step to gandalf OP + skill § 5 step 2b | **gandalf** (executes) | jack-ryan required |
| A3 | § 4.9 collapse-never-delete shape ratified | — | jack-ryan RATIFIED |
| A4 | AMENDMENT 2a — widen § 4.9 collapse guard to the § 6.3 cross-repo reference check (both repos, cited-as-evidence not just cited-as-open) | **gandalf** (executes) | jack-ryan required |
| A5 | AMENDMENT 2b — anchor "governing pivot" definition (locked/reversed PART item OR cited-by-open-row OR carries-Matt-ruling) in § 4.9 | **gandalf** (executes) | jack-ryan required |
| A6 | Three tripwires + never-prune extension ratified as-written | — | jack-ryan RATIFIED |
| A7 | Repair the live OP↔skill drift — skill §1 (three trackers), §4.7 (§4.6 composition + #42/#43 stack), §5 (step 2b + third tracker) to OP parity | **gandalf** (twin owner) | jack-ryan APPROVED (ADR-002; doc-only) |
| A8 | Write new canonical-doc-format.md § 6.8 — OP↔SKILL twin-sync standing rule (text specified in § 4 above) | **gandalf** (executes; § 6.7 assigns § 6 execution to gandalf) | jack-ryan RATIFIED (this note) |
| A9 | § 4.8/§ 4.9 stay OP-local; NO engineering-disciplines.md write; revisit § 4.8 → canonical-doc-format.md § 6 after a 2nd live desync case | — | jack-ryan ruled |

**Nothing here escalates to Matt** — all items are documentation/process-governance within jack-ryan's ADR-002 approval authority and gandalf's proposer-executes lane. Matt authorized the ratification set; this note discharges it. No push (per task).

---

## References

- `agentic_orchestration/operating-procedures/gandalf.md` — OP § 4.8/§ 4.9 (ratified w/ amendments), § 4.7 + § 5 (drift + AMENDMENT-1 target)
- `.claude/skills/reincarnated-gandalf-operating-procedure/SKILL.md` — twin; drift at §1 step 2 / §4.7 / §5 confirmed
- `agentic_orchestration/operating-procedures/canonical-hygiene-audit-routine.md` — step 7 tripwires (a)/(b)/(c) + never-prune extension (ratified); § 6.8 twin-sync will reference tripwire (b)
- `agentic_orchestration/operating-procedures/canonical-doc-format.md` — § 6.2/§ 6.3/§ 6.5/§ 6.6/§ 6.7 (the governance system § 4.8/§ 4.9 compose with); § 6.8 (new — twin-sync, gandalf to execute); § 8 (twin-sync-in-prose, superseded by § 6.8)
- `canonical/matt_decision_needed/README.md` — Q3 restatement + RESOLVED appendix (the § 4.8 evidence-case, confirmed)
- `canonical/matt_to_do/README.md` — T1 (CCR run; blocks the hygiene routine that carries the tripwires)
- `canonical/current-to-end-state/current-to-end-state-story.md` — A11 (line 99) / B2→B3 (lines 110–111): the killed-premise the § 4.8 rule prevents; SESSION-DELTA already synced
- `canonical/current-to-end-state/current-to-end-state-engine.md` — 433 lines / ~19.5K tokens (char-est): the § 4.9 accretion subject
- Commit `b2485af` — the hardening set under review

---

**Signed:** jack-ryan (analyst / QA / doc-lifecycle rule ratifier per canonical-doc-format.md § 6.7)
**For:** ratifying the four reorg-hardening items in `b2485af` — three RATIFY (one with 3 amendments across items 1–2), the drift-flag ratified with two rulings; graduation held OP-local, twin-sync graduated to § 6.8. All follow-up execution routes to gandalf (proposer-executes); no engineering-disciplines.md write warranted.
