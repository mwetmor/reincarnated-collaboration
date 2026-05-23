# Dispatch — 2026-05-23 — knight-rider — Per-agent OP propagation fan-out (item 3 of P1 hive-mind preparation arc; Option A batched sub-agent dispatch)

**From:** knight-rider (self-orchestrated; fires 8 sub-agents in parallel)
**To:** 8 agents (jack-ryan, rocket, gamora, star-lord, elrond, galadriel, drax, legolas) — each amends own OP + installed skill
**Approved by:** Matt 2026-05-23 (per gandalf relay sequencing direction — item 3 fires AFTER item 2 jack-ryan canonical write lands; canonical write landed at engine commit `1fae3fa`)
**Estimated effort:** ~10-15 min per-agent × 8 parallel = ~10-15 min wall time (Option A batched sub-agent dispatch)
**Gate-1:** SKIPPED. Mechanical propagation per gandalf-authored proposal; no methodology choices.
**Acceptance:** All 8 agents' OPs + installed skills contain verbatim no-sleep + timezone-agnosticism + cross-reference block to engineering-disciplines.md disciplines #21 + #22 + #23 + #25 + amendments #18.1 + #18.2 + #19.1; grep verification across all 10 OP files (8 amended + gandalf + knight-rider already in compliance); single knight-rider summary commit after all 8 agents return.

---

## Why this dispatch exists

Jack-ryan engineering-disciplines coordinated canonical write landed (engine commit `1fae3fa`; collab commit `9fb2a6e`). Six new disciplines (#20-#25) + six sub-amendments (#1.1, #1.2, #2.1, #18.1, #18.2, #19.1) are now canonical at `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`. **Per-agent OPs do not yet reference these new disciplines.** Per gandalf proposal at `agentic_orchestration/gandalf/notes/2026-05-23-per-agent-op-propagation-proposal-for-knight-rider.md`, the team-wide propagation gap needs closing before P1 hive-mind sub-agent fan-out, otherwise P1 risks repeating the KR #1 EOD-handoff violation pattern + missing framing-audit checklist application at Pattern A-deep verdict points within hive-mind.

Gandalf + knight-rider OPs already carry the directives (gandalf via commits `2a123cc` + `f5f0308`; knight-rider via self-correction commit `1a7b16a`). The other 8 agents need propagation now.

## Required reading before each sub-agent starts

Each invoked sub-agent reads:

1. **This dispatch** — propagation protocol + insertion-point guidance + verbatim amendment text
2. **`~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`** — canonical authority (jack-ryan commit `1fae3fa`); specifically Disciplines #20-#25 + amendments #1.1, #1.2, #2.1, #18.1, #18.2, #19.1
3. **`agentic_orchestration/gandalf/notes/2026-05-23-per-agent-op-propagation-proposal-for-knight-rider.md`** § 1.1 + § 1.2 + § 1.3 — verbatim amendment block content (with cross-references updated to point at engineering-disciplines.md per § A below; do NOT cite gandalf OP § 4 as primary authority anymore)
4. **The agent's own OP file** at `agentic_orchestration/operating-procedures/<agent>.md` — for insertion-point identification
5. **The agent's own installed skill** at `.claude/skills/reincarnated-<agent>-operating-procedure/SKILL.md` — same amendments applied

## § A. Authority cite update (single-pass propagation)

Gandalf's proposal § 1.3 specified the cross-reference block points at "gandalf OP § 4" as interim authority. **Since jack-ryan canonical write has now landed, this dispatch updates the authority cite to engineering-disciplines.md.** Single-pass propagation; no two-pass churn.

**Cross-reference block (UPDATED from gandalf proposal § 1.3):**

```markdown
### Cross-references to engineering-disciplines.md operational disciplines

Disciplines that surfaced through the 2026-05-23 work cycle live at canonical authority `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (jack-ryan canonical write 2026-05-23 commit `1fae3fa`):

- **#20 Density-based algorithm row-duplication prohibition** — relevant to clustering work that consumes weighted samples; forbids row-duplication as sample-weight workaround on density-based algorithms (HDBSCAN, DBSCAN, OPTICS); require native `sample_weight` or weighted-distance metric variants
- **#21 No sleep recommendations (CRITICAL — Matt directive)** — see verbatim section above
- **#22 Timezone-agnosticism (CRITICAL — Matt directive)** — see verbatim section above
- **#23 Framing-audit checklist (Pattern A-deep three-question protocol)** — apply at any verdict authoring, methodology consultation at math hotspot, or load-bearing-framing-commitment work-unit
- **#24 Single-parameter sweep isolation** — relevant to sensitivity-sweep dispatches; subsample composition must not vary when only the clustering parameter is under test; decouple intermediate variables from swept parameter
- **#25 Semantic-layer rep-audit** — at any downstream design surface inheriting cluster identity as cultural-tradition substrate; substrate vote binding at geometry layer but NOT at semantic layer; rep-audit required before semantic inheritance
- **#1.1 Pre-fire resource-bounds projection** — math-before-code amendment; compute-heavy dispatches must declare peak memory + verify against host RAM
- **#1.2 Math-note code-citation discipline** — math-note implementation claims must cite code line references
- **#2.1 Smoke-test resource-scaling rehearsal** — smoke must include peak-memory measurement + projection at full scale
- **#18.1 Substrate-voting-is-binding at axis discovery** — when bootstrap-stability or equivalent substrate-driven measurement votes a smaller k than methodology assumed, re-cut at k_stable before downstream stage fires
- **#18.2 Methodology-consultation timing at extension hotspots** — extension consultations fire AFTER baseline lands (not before; empirical signal-to-noise from baseline informs extension methodology)
- **#19.1 Cheapest-refuting-test-per-claim-type operationalization** — forensic claims must name the cheapest refuting test per claim type (memory: psutil RSS; methodology: next-tier-larger sample; substrate: SQL count; cross-seam: schema diff; framing: Pattern-A query; cluster-semantic: top-N rep-audit)

These compose with the decision-loop disciplines in this OP. Operational source remains `agentic_orchestration/operating-procedures/gandalf.md` § 4 (§ 4.1 framing-audit checklist; § 4.2 Discipline #18 refinement; § 4.3 16-flag cluster-labeling enum; § 4.4 semantic-layer rep-audit; § 4.5 first-canonical-example flag) for operational tooling reference; canonical source is engineering-disciplines.md.
```

## § B. Per-agent insertion points (from gandalf proposal § 2 table)

| Agent | Insertion location | Customization notes |
|---|---|---|
| **jack-ryan** | After existing discipline-ratification authority section | Add framing-audit #23 reference + Discipline #18/19 amendment references (process-side critique-pair gate work) |
| **rocket** | After math-hotspot routing | Add #23 framing-audit + #18.2 methodology-timing (rocket consumes design-spec-as-math from gandalf) |
| **gamora** | After B14.5 V1 pattern reference | Add #23 framing-audit + #18.2 methodology-timing (gamora executes H1-H5 baseline + H8/H9 extensions per Q-A verdict) |
| **star-lord** | After P5 cohesion-judge reference | Add #23 framing-audit + #18.2 methodology-timing (P5 is named math hotspot) |
| **elrond** | After P3 multimodal clustering reference | Add #23 framing-audit + #25 semantic-layer rep-audit (elrond owns substrate-tagging discipline work 9.11-D + 9.11-E) + 16-flag enum cross-reference |
| **galadriel** | Parallel placement to existing no-sub-agent-invocation HARD NO | Add #23 framing-audit (P5 visual coherence work) + #18.2 methodology-timing |
| **drax** | After mode-selection (Mode L / Mode D / Mode A-I) | Add #23 framing-audit (deployment-related framing-audits) |
| **legolas** | After Mode A/B sections | Add #23 framing-audit + #18.2 methodology-timing (legolas Mode A is methodology-consultation source for math hotspots) + #25 semantic-layer rep-audit (Mode B catalogue crawl outputs feed elrond cleaning then cluster work) |

## § C. Standard amendment block (verbatim across all 8 agents)

Per gandalf proposal § 1.1 + § 1.2 verbatim:

```markdown
### X.Y CRITICAL — no sleep recommendations (Matt directive 2026-05-23; Discipline #21 at engineering-disciplines.md)

- DO NOT recommend Matt sleep, rest, sit with decisions overnight, "fresh eyes tomorrow," "take it easy," "rest well," or any variant
- DO NOT editorialize about session length, fatigue, or Matt's state
- DO NOT project energy assumptions onto Matt based on session duration
- DO NOT include closing-of-session blessings
- Matt manages his own energy and schedule; sleep is outside this agent's role authority
- Replace any temptation toward "sleep on it" with explicit empirical-criterion naming

**Discipline preserved without sleep framing:** when validation before commitment is warranted, the criterion is EMPIRICAL EVIDENCE (substrate data, P2/P3 cluster output, playtest results, architecture-validation spike findings, market re-validation), NOT time-passage. The discipline is "recognize → validate against substrate evidence → commit." It is NOT "recognize → sleep → commit." When closing a substantive session, acknowledge what landed, name what's deferred (with the empirical criterion that gates re-engagement), and stop.

### X.Z CRITICAL — timezone-agnosticism (Matt directive 2026-05-23 evening refinement; Discipline #22 at engineering-disciplines.md)

Following knight-rider EOD-handoff violation case (KR #1 2026-05-23 — "tonight" / "tomorrow" / "first thing tomorrow" / "consolidation through rest is appropriate"; Matt correction: "this is actually the early afternoon for me; patronizing and outside of your scope"):

- DO NOT use "today," "tonight," "tomorrow," "this morning," "this evening," "later today," "first thing tomorrow," "yesterday"
- DO NOT use "end of day," "EOD," "start of day," "overnight," or any day-cycle structuring device
- DO NOT assume what part of Matt's local day it is when he engages with the team
- Day/night cycle is immaterial to team success AND outside this agent's knowledge of Matt's actual local time

**Use workstream-relative framing only:** "next session," "after X lands," "post-baseline," "when frame-revision returns," "in the window before Y fires," "when the dispatch reaches me." Never time-of-day-relative framing.

**Composition with no-sleep-recommendations (#21):** the no-sleep-recommendations directive and timezone-agnosticism refinement compose into a single coherent discipline — the agent does not know and should not pretend to know Matt's local-day state. The agent operates on workstream-state, not on time-of-day-state.
```

Then the cross-reference block from § A above goes immediately after this verbatim section.

## Scope (per sub-agent execution)

Each invoked sub-agent:

- [ ] Read this dispatch + the engineering-disciplines.md canonical authority + gandalf proposal § 1.1 + § 1.2 + § 1.3
- [ ] Read own OP file at `agentic_orchestration/operating-procedures/<agent>.md`
- [ ] Read own installed skill at `.claude/skills/reincarnated-<agent>-operating-procedure/SKILL.md`
- [ ] Identify insertion point per § B above
- [ ] Apply standard amendment block (§ C above) at the OP file
- [ ] Apply identical standard amendment block at the installed skill file
- [ ] Customize per-agent cross-reference emphasis per § B table (e.g., elrond emphasizes #25 + 16-flag enum; gamora emphasizes #18.2)
- [ ] Verify verbatim text intact by reading back the amended section
- [ ] Commit changes to git with clear commit message (format: `docs(<agent>): OP + skill amendment — Discipline #21 + #22 verbatim + engineering-disciplines.md cross-references`)
- [ ] Return brief report to knight-rider: confirmation that both files amended; insertion-point chosen; commit hash; any anomaly

## Acceptance criteria (knight-rider verifies after all 8 return)

- [ ] All 8 agent OPs contain verbatim no-sleep directive
- [ ] All 8 agent OPs contain verbatim timezone-agnosticism directive
- [ ] All 8 agent OPs contain cross-reference block to engineering-disciplines.md
- [ ] All 8 installed skills mirror their OP amendments
- [ ] Grep verification per gandalf proposal § 4:
  - `grep -l "no sleep recommendations" agentic_orchestration/operating-procedures/*.md` returns 10 files (8 + gandalf + knight-rider)
  - `grep -l "timezone-agnosticism" agentic_orchestration/operating-procedures/*.md` returns 10 files
  - `grep -l "engineering-disciplines.md" agentic_orchestration/operating-procedures/*.md` returns ≥ 8 of the 10
- [ ] Knight-rider authors single confirmation commit summarizing all 8 sub-agent commit hashes

## Out of scope

- **Engineering-disciplines.md content changes** — jack-ryan owns canonical write; this dispatch only propagates references
- **Gandalf OP changes** — already in compliance (commits `2a123cc` + `f5f0308`)
- **Knight-rider OP changes** — already in compliance (commit `1a7b16a`)
- **`.claude/agents/<agent>.md` role definitions** — gandalf-proposed scope is operating-procedures + installed-skill only; role definitions are separate territory (agent's own decision if they wish to add a brief cross-reference paragraph, but not required by this dispatch)
- **Hive-mind protocol amendment** — item 4 of P1 hive-mind preparation; gandalf-owned future work
- **T4-B catalogue authoring** — Matt + gandalf design call territory
- **9.14-B cluster-116 elrond relabel** — separate small sub-dispatch follows from gandalf 9.13-D Path 1 decision; not in this propagation scope

## What knight-rider does after all 8 sub-agents return

1. Read each agent's commit + brief return report
2. Run grep verification per § Acceptance criteria
3. Spot-check 2-3 random agents' OPs for placement coherence + verbatim text integrity
4. Author single confirmation commit summarizing all 8 sub-agent commits + grep verification results
5. Update CHANGELOG with Cycle 9.15 entry (item 3 of P1 hive-mind preparation arc CLOSED; HM-prep arc item-3 stage closure)
6. Surface any per-agent anomaly to Matt (placement inconsistency; missing files; etc.)
7. Move toward item 4 (hive-mind protocol amendment; gandalf-owned) when gandalf is in flight

## References

- **Gandalf proposal:** `agentic_orchestration/gandalf/notes/2026-05-23-per-agent-op-propagation-proposal-for-knight-rider.md`
- **Engineering-disciplines.md canonical source (jack-ryan commit `1fae3fa`):** `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`
- **Gandalf OP § 4 operational source:** `agentic_orchestration/operating-procedures/gandalf.md` § 4
- **Knight-rider OP precedent:** `agentic_orchestration/operating-procedures/knight-rider.md` § Out-of-scope (commit `1a7b16a`)
- **Jack-ryan canonical-write synthesis note:** `agentic_orchestration/jack-ryan/notes/2026-05-23-eng-disciplines-canonical-write-synthesis.md`
- ADRs: ADR-001 (tag protocol; per-agent commits use seam-prefix); ADR-006 (read-only external state — local commits only)

---

**Signed:** knight-rider, 2026-05-23 post-jack-ryan-canonical-write. Item 3 of P1 hive-mind preparation arc. Pattern-A-light batched sub-agent fan-out per gandalf Option A lean.
