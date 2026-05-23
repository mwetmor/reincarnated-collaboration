# reincarnated-decision-log-format — Cross-cutting Reference Skill

> **STATUS:** CURRENT (load-bearing as of 2026-05-23) — Stream 3 cross-cutting reference skill per `canonical/02-roadmap.md` § 2.2
>
> **Skill packaging:** Markdown source for the eventual installable skill `reincarnated-decision-log-format` (per doc 38 § 4 step 2 + Skill Creator pass). Until packaging lands, install by reading this doc + the authoritative source.

**Authored:** 2026-05-23
**Author:** gandalf (cross-cutting Stream 3 authoring)
**Authoritative source:** `~/Games/reincarnated-engine/design/decisions/decisions-log.md`
**Pattern:** universal reference wrapper; load when proposing, drafting, or citing decisions-log entries
**Companion skills:** `reincarnated-engineering-disciplines`; `reincarnated-canonical-doc-format`; `reincarnated-critique-pair-gate-protocol`

---

## 0. What this skill IS and IS NOT

**IS:** the universal format-spec for decisions-log entries. Names: file location, entry format, when to file, who writes, who proposes. Loaded by any agent whose work surfaces a decision that needs durable capture.

**IS NOT:** the authoritative decisions-log itself (that's `decisions-log.md` in engine repo; ALWAYS the canonical source of decision state). NOT a substitute for jack-ryan's authoring authority (jack-ryan is the only agent who writes entries directly). NOT the ADR format spec (founding ADRs live in `agentic_orchestration/GOVERNANCE.md`; decisions-log uses lighter temporal format).

---

## 1. File location + ownership

- **File:** `~/Games/reincarnated-engine/design/decisions/decisions-log.md`
- **Writer:** **jack-ryan** (sole authoring authority per AGENTS.md seam map)
- **Proposers:** any agent surfacing a decision worth capture (gandalf, knight-rider, rocket, gamora, star-lord, elrond, galadriel, drax, legolas)
- **Approver:** Matt (per ADR-002 final-approval authority)
- **Routing:** proposer → knight-rider routes to jack-ryan → jack-ryan drafts entry → Matt approves → jack-ryan commits

---

## 2. Entry format

Every entry follows this structure:

```markdown
### YYYY-MM-DD: Brief decision title

**Decision**: What was decided.

**Reasoning**: Why this was chosen.

**Alternatives considered**: What else was on the table.

**Status**: Active / Superseded by [date] / Reversed by [date]

**Related**: Links to related decisions or documents.
```

**Field discipline:**
- **Date** — actual decision date (not draft date)
- **Title** — brief; ≤80 chars; subject-verb form preferred ("Math engine as project spine"; not "We decided on the math engine")
- **Decision** — one or two sentences stating WHAT (not why)
- **Reasoning** — why this option; reference empirical evidence or design anchors; cite canonical docs by path
- **Alternatives considered** — at least 2 alternatives if any existed; "no other option considered" is acceptable when accurate
- **Status** — `Active` (current); `Superseded by YYYY-MM-DD` (later entry replaces); `Reversed by YYYY-MM-DD` (later entry undoes)
- **Related** — cross-references to canonical docs, prior decisions, dispatches that fired or were blocked

---

## 3. When to file an entry

| Trigger | File? |
|---|---|
| Architectural commitment locked (ADR-shaped) | YES |
| Methodology choice at math hotspot | YES |
| Engine seam interface change | YES |
| Discipline ratification or amendment | YES |
| Pattern retirement (Patterns 4-5-6 type) | YES |
| Recognition record (design hypothesis pending validation) | NO — recognition records live in `canonical/story/` per recognition discipline |
| Routine implementation choice within established pattern | NO — capture in commit message + canonical doc if substantive |
| Wave dispatch FIRE-READY | NO — dispatch artifact is durable; no decisions-log entry needed unless dispatch locked a new architectural commitment |
| Recognition that may become architectural commitment | Author recognition record first; file decisions-log entry only when empirical-evidence criterion validates the commitment |

**Discipline:** recognition → validate → commit. Decisions-log captures the commit step. Recognition records capture the recognition step. Don't conflate.

---

## 4. Proposing an entry (non-jack-ryan agents)

Proposer surfaces decision via:

1. **In-session capture** — name the decision in the current artifact (canonical doc, dispatch, verdict); flag for jack-ryan routing
2. **Knight-rider relay** — knight-rider's Mode D per `operating-procedures/knight-rider.md` § 2; routes to jack-ryan with proposal text
3. **Direct gandalf request** — for design-side decisions; gandalf authors recommendation; routes via knight-rider to jack-ryan

**Proposer responsibilities:**
- Draft the decision text (Decision + Reasoning + Alternatives) in your artifact
- Cite the source (commit, dispatch, canonical doc, empirical evidence)
- Surface to knight-rider for routing OR Matt for direct approval if architectural-commitment-shaped

**Anti-pattern:** drafting entries directly in `decisions-log.md` without jack-ryan. Cross-seam discipline applies — jack-ryan owns the file.

---

## 5. Superseding + reversing

When a later decision supersedes or reverses an earlier one:

1. **New entry** with full Decision + Reasoning + Alternatives + Status:Active
2. **Edit prior entry's Status** to `Superseded by YYYY-MM-DD: <title>` OR `Reversed by YYYY-MM-DD: <title>`
3. **Cross-reference both ways** in Related fields
4. **Do NOT delete prior entries.** Temporal log is append-only with status edits to prior entries.

---

## 6. Cross-reference discipline

Entries cite:
- Canonical docs by path (`canonical/story/<doc>.md`)
- Dispatches by path (`agentic_orchestration/dispatches/<dispatch>.md`)
- Tags by name (`gamora/v1.3-b14-2`)
- Commit hashes for substantive code commits
- Prior decisions-log entries by date-title

External docs (GitHub, research papers, etc.) cited by URL with archive note if ephemeral.

---

## 7. Update protocol for this skill

This skill evolves when:
- The decisions-log format changes in the source (`decisions-log.md` header § Format)
- A new field becomes load-bearing (rare)
- A new proposing pattern emerges (e.g., critique-pair Pattern E ratification authoring)

Authored / maintained by **gandalf** (cross-cutting Stream 3 owner); format amendments routed via jack-ryan as decisions-log owner. The authoritative source remains `decisions-log.md`'s § Format section.

---

**Signed:** gandalf (cross-cutting Stream 3 reference-skill author)
**For:** the universal format-spec for proposing, drafting, and citing decisions-log entries. Single source of truth remains `~/Games/reincarnated-engine/design/decisions/decisions-log.md` § Format. Jack-ryan owns authoring authority; other agents propose via knight-rider routing or direct gandalf request.
