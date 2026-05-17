# REVIEW_PROCESS.md — How work moves through the team

**Status:** Active 2026-05-13
**Authority:** ADR-002 (Tiered approval), ADR-004 (Cross-seam handoff), ADR-006 (External writes), ADR-007 (Survey-mode)

This document is the **operational playbook** for how changes flow from idea to shipped artifact. Read with `AGENTS.md` (who) and `GOVERNANCE.md` (founding rules).

---

## 1. Review principles

These shape every Gate 1 and Gate 2 review. jack-ryan applies them; Matt invokes them when escalating. Principles 1-5 are founding (2026-05-13). Principle 6 / 6b added 2026-05-16 (R11(b) + P8 operationalization).

### Principle 1 — Math-before-code on non-trivial changes

Per Discipline #1. Before any non-trivial implementation, the math must be on paper (or in a markdown file in the seam). Includes: scaling factors, distribution targets, threshold values, optimization criteria. If the developer can't write the math, they don't write the code yet.

**Gate 1 question:** "What math did you do before coding this?"
**BLOCK trigger:** Implementation without math justification on non-trivial work.

### Principle 2 — Smoke-gate before commit

Per Discipline #2. Every commit includes smoke-test output or an explicit skip-reason. Full validation runs at milestone tags only.

**Gate 2 question:** "Where's the smoke-test output for this commit?"
**BLOCK trigger:** Code commit without smoke-test evidence and no skip-reason.

### Principle 3 — Cross-seam impact called out explicitly

Per ADR-004 + Discipline #12. If a change affects another seam's consumers, the developer writes `MIGRATION.md` AND notes the affected seams in the commit message.

**Gate 1 question:** "Does this change touch any consumer's interface?"
**BLOCK trigger:** Cross-seam change without MIGRATION.md before tagging.

### Principle 4 — Decisions-log is single source of truth for design state

When in doubt, the decisions-log wins. New decisions land there before they land in code. Conflicting changes get flagged.

**Gate 1 question:** "Which decisions-log entry justifies this approach?"
**BLOCK trigger:** Implementation that conflicts with a locked decision and doesn't propose superseding it.

### Principle 5 — Severity matters; escalation is normal

INFO < WARN < BLOCK. jack-ryan has BLOCK authority. BLOCK doesn't mean "permanently stop" — it means "this needs Matt's eyes before it ships." Escalation is the system working, not a failure.

### Principle 6 — Cross-seam contract changes require round-trip discipline

Per Drift-audit Drift-12 / R11(b). Operationalized 2026-05-16 after two Pattern P7 instances at different seams (gamora V2.1 emission gap + star-lord season_writer.py form-bias silent drop) confirmed the pattern is structural, not incidental.

**What triggers this principle:** a dispatch ships a change to any cross-seam contract. A cross-seam contract change is any of the following:

| Trigger type | Examples |
|---|---|
| Telemetry schema field added/modified | new column on `class_fight_loadouts`; new `class_balance_results` field |
| Fight_log dict key added/modified | new key emitted by gamora's fight_engine or balance_loop |
| Loadout dict key added/modified | new key in the loadout packet gamora/rocket passes to star-lord or drax |
| Export packet structure changed | new top-level key in season JSON; changed season_writer.py output shape |
| Any inter-seam fixture format changed | new field in any dict crossing a seam boundary |

Note: a field renamed, removed, or made optional is also a cross-seam contract change even if no new field is added.

**Gate 1 question:** "Does this dispatch include a cross-seam round-trip smoke test — generate, export, validate at the consumer boundary using PRODUCTION-PATH fixtures, not test-isolated fixtures — OR an explicit justification for why round-trip is not applicable?"

The two permissible outcomes are:
- **(i) Round-trip smoke included.** Acceptance criteria must specify: what production-path fixture is used, which consumer boundary is exercised, and what field-presence check confirms the field flows end-to-end.
- **(ii) Round-trip-not-applicable justification.** Acceptance criteria must include an explicit line: `Round-trip: not applicable because <reason>`. Valid reasons include: "change is additive-nullable; existing consumer code paths tolerate absent keys; isolation verified by <test name>." Invalid reason: silence.

**BLOCK trigger:** a dispatch ships a cross-seam contract change (by the trigger-type table above) with neither clause present in the acceptance criteria.

**Gate 2 check:** when the completion record lands, verify the round-trip smoke output is present (or the justification is present). Missing either is a WARN → BLOCK if the pattern has already been flagged once for this agent.

**What this does NOT cover:**
- Within-seam refactors with no change to the inter-seam dict/schema surface (Principle 3 already handles the MIGRATION.md angle)
- Catalogue data layer changes (elrond/legolas seam — see Principle 6b below)
- Documentation-only dispatches

### Principle 6b — Catalogue dispatches require per-product-line register validation (secondary hook, legolas/elrond seam)

Per Drift-audit Pattern P8 (Drift-13; CraftPix VFX vs character line register confusion). Operationalized 2026-05-16 after 4 P8 instances confirmed the pattern is structural.

**Judgment on scope:** P8 does not warrant a full Gate-1 BLOCK hook equivalent to Principle 6. The per-record `style_register` field already provides the correct granularity; existing per-record curation is correct. The gap is at the *vocabulary layer* — dispatch authoring and findings-summary docs aggregating by vendor where per-product-line granularity is required. The three existing enforcement layers (legolas persona-rule extension per P8(a); elrond schema flag per P8(d); quarterly re-pass per R10/P8(b)) are sufficient. Principle 6b is therefore a *soft gate* — a Gate-1 question, not a BLOCK trigger.

**What triggers this principle:** a dispatch covers catalogue work for a vendor that spans multiple product lines (e.g., VFX + characters; sprites + tilesets; portraits + environments).

**Gate 1 question:** "Does this catalogue dispatch instruct the crawling agent to record `deliverable_register` (or equivalent) per product line — based on per-product-page inspection, NOT inferred from the vendor's site-wide marketing label? And does the findings-summary format include a `vendor-register-mixed: yes/no` flag?"

**WARN trigger (not BLOCK):** catalogue dispatch for a multi-product-line vendor that does not include per-product-line register-validation instruction. WARN because the per-record data is the primary source-of-truth and missing the dispatch instruction does not corrupt existing records; it only risks accumulating new records with wrong register inferences.

**No decisions-log entry required for 6b:** this is a persona-rule and dispatch-authoring convention, not an architectural decision. The P8 pattern is already canonically documented in drift-audit.md; 6b operationalizes it at Gate-1 without requiring a new ADR or decisions-log entry.

---

## 2. Change lifecycle

```
┌─────────────────────────────────────────────────────────────────────┐
│                       Change lifecycle (typical)                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1. Developer reads startup manifest (AGENTS.md Section 3)          │
│         ↓                                                           │
│  2. Developer reads AGENT_STATE.md from their seam                  │
│         ↓                                                           │
│  3. Developer drafts MATH note (Principle 1) for non-trivial work   │
│         ↓                                                           │
│  4. Developer implements                                            │
│         ↓                                                           │
│  5. Developer runs smoke-test (~2-3 min)                            │
│         ↓                                                           │
│  6. If smoke fails: iterate (back to step 3 or 4)                   │
│         ↓                                                           │
│  7. Smoke passes → write MIGRATION.md if cross-seam impact          │
│         ↓                                                           │
│  8. Commit with smoke-line and cross-seam note                      │
│         ↓                                                           │
│  9. Tag intermediate (per-seam prefix): <seam>/v1.3-<feature>-<n>   │
│         ↓                                                           │
│  10. Add work item to qa/pending/                                   │
│         ↓                                                           │
│  11. Update AGENT_STATE.md (where I left off)                       │
│         ↓                                                           │
│  12. jack-ryan reviews (Gate 2, batched)                            │
│         ↓                                                           │
│  13a. INFO/WARN → developer notes; merges proceed                   │
│  13b. BLOCK → developer fixes OR escalates to Matt                  │
│  13c. APPROVE → if jack-ryan has authority (ADR-002 table)          │
│  13d. ESCALATE → if Matt-only authority (ADR-002 table)             │
│         ↓                                                           │
│  14. At milestone: Matt approves → drop seam prefix → tag v1.3-…    │
│         ↓                                                           │
│  15. Update decisions-log + canonical/ + CHANGELOG.md as applicable │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Gate 1 (pre-prompt review)

When knight-rider dispatches a task to a developer, jack-ryan reviews the prompt BEFORE the developer runs. Catches:
- Missing math justification (Principle 1)
- Conflict with decisions-log (Principle 4)
- Ambiguous cross-seam scope (Principle 3)
- Cross-seam contract change without round-trip discipline (Principle 6)
- LLM prompt-construction site exposing internal schema labels (Discipline #14)
- Outcome-attribution claim without ablation evidence (Discipline #13b)

Gate 1 is fast (~2 min). jack-ryan in DESIGN-MODE — peer collaborator with knight-rider, not gatekeeper.

### Gate 2 (post-output review)

When a developer ships a commit to `qa/pending/`, jack-ryan reviews in DEV-MODE — gatekeeper with BLOCK authority. Batched, typically every few hours OR before any milestone tag.

Gate 2 produces a finding file in `qa/findings/<date>-<work-item>.md` with severity + rationale + action.

---

## 3. File-type rules

### Code changes

- **Smoke-test required** before commit (Principle 2)
- **MIGRATION.md required** if cross-seam (Principle 3 + ADR-004)
- **Math note required** for non-trivial (Principle 1)
- **Tests SHOULD accompany** any new function or schema change
- **jack-ryan reviews at Gate 2**, Matt approves at milestone (ADR-002)

### Documentation-only changes

- **Smoke-test skipped** with explicit "docs-only" line in commit message
- **jack-ryan approves directly** (no Matt escalation unless content is architectural)
- **Decisions-log entries**: special case — must reference at least one ADR or discipline

### Test additions / fixtures

- **jack-ryan approves directly** (low risk, quality-ratcheting)
- **Should pass on first run** in the developer's seam
- **Tests that span seams** require MIGRATION.md and Matt approval

### Dependency bumps

- **Patch/minor**: jack-ryan approves
- **Major**: Matt approves (breaking change risk)
- **New dependency**: Matt approves (architectural choice)

### Schema changes (telemetry, JSON output, gear catalog, etc.)

- **MIGRATION.md required** (ADR-004)
- **Affects every downstream consumer** — explicitly enumerate in MIGRATION.md
- **Matt approves** (cross-seam by nature)
- **Backward-compat shim preferred** over forced migration

### ADR additions / canonical doc changes

- **jack-ryan drafts** (owns design-side canonical)
- **Matt approves** new ADRs
- **knight-rider archives** superseded ADRs (don't delete; mark superseded)

---

## 4. External-system execution rules

Per ADR-006: read-only by default; writes require per-statement authorization.

### Databases

- **telemetry.db**, **research.db** — read-only by default
- Writes (INSERT/UPDATE/DELETE/schema): explicit Matt authorization per statement
- SELECT queries: agent runs freely
- Schema introspection (PRAGMA, .schema, .tables): agent runs freely

### LLM API calls

- **Cost tracked** in every session (record token counts, model, dollar estimate)
- **Retries documented** — if a call fails 3+ times, agent stops and reports
- **Rate-limit handling** — back off exponentially; never spin
- **Bulk operations** (full season regen, batch class generation): Matt authorizes the batch up-front; agent runs the batch; reports cost

### File system

- **Within seam**: agent reads/writes freely
- **Outside seam**: read-only; writes require Matt authorization
- **Cross-repo**: read-only across all repos other than the agent's own; writes require Matt authorization

### Process spawning

- **Tests, builds, smoke runs**: agent runs freely
- **External tools** (LLM CLI, npm install, pip install): agent runs freely with reporting
- **Background processes** (long regens): Matt authorizes the spawn; agent reports PID + log location
- **Process termination**: Matt authorizes

### Git operations

- **Read** (status, log, diff, branch list): agent runs freely
- **Local writes** (add, commit, tag, branch): agent runs freely WITHIN tier authority
- **Remote pushes**: Matt authorizes (especially main / stage-a2)
- **Destructive** (reset --hard, force push, branch -D): Matt authorizes always

---

## 5. Finding file format

Each Gate 2 review produces a finding in `agentic_orchestration/qa/findings/<date>-<work-item>.md`:

```markdown
# Finding — <date> — <work-item>

**Reviewer:** jack-ryan
**Severity:** INFO | WARN | BLOCK
**Target:** <tag or commit hash>
**Developer:** <agent name>
**Principles applied:** <numbers from Section 1>

## What I found
<one paragraph>

## Rationale
<cite specific principle, ADR, or discipline number>

## Action
- [ ] Developer: <action>
- [ ] Matt (if BLOCK or ESCALATE): <decision needed>

## References
<paths to specific files reviewed>
```

---

## 6. Escalation paths

| Trigger | First responder | Escalates to |
|---|---|---|
| BLOCK from jack-ryan | Developer fixes OR escalates | Matt |
| Cross-seam ambiguity | knight-rider clarifies | jack-ryan or Matt if architectural |
| Decisions-log conflict | jack-ryan flags | Matt resolves |
| External-system write request | Matt authorizes | (terminal) |
| Major dependency change | jack-ryan flags | Matt resolves |
| Tool failure / API outage | Developer reports, retries | knight-rider if persistent |

---

## 7. What review is NOT

- **Not a permission gate for routine work.** Developers proceed without asking permission for in-seam work that fits the playbook.
- **Not a quality bar everyone must meet at every step.** INFO and WARN exist for a reason — they record observations without blocking.
- **Not synchronous.** jack-ryan reviews batched; developers don't wait.
- **Not infallible.** If jack-ryan misses something, Matt or the developer raises it. The system is meant to catch most issues, not all.

---

## References

- `AGENTS.md` — who does what
- `GOVERNANCE.md` — founding ADRs
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — the 12 disciplines
- `reincarnated-engine/design/decisions/decisions-log.md` — design state
