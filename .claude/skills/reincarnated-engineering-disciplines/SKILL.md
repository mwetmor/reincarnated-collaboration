---
name: reincarnated-engineering-disciplines
description: Use this skill when work touches discipline citation, dispatch authoring, math hotspots (P2/P3/P5), cross-seam emission, long-running execution, external-data acquisition (crawls), sidecar/attribution analysis, pre-tag validation, or methodology choice at a hotspot. A ROUTER, not a corpus — it carries when-to-load triggers and citation rules only, and deliberately enumerates NO disciplines. The corpus is large and grows; READ IT at ~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md, which is the sole authority on what exists and how many.
version: 0.2.0
---

# reincarnated-engineering-disciplines — Cross-cutting Reference Skill

> ⚑ **STATUS: CURRENT as a ROUTER (v0.2.0, 2026-09-21). It was a CORPUS WRAPPER from 2026-05-23 to 2026-09-21 and in that role it FAILED — see § 1.**
>
> **STATUS (original):** CURRENT (load-bearing as of 2026-05-23) — Stream 3 cross-cutting reference skill (its founding roadmap reference, `canonical/02-roadmap.md`, has since been retired to git-lineage)
>
> **Skill packaging:** Markdown source for the eventual installable skill `reincarnated-engineering-disciplines` (per doc 38 § 4 step 2 + Skill Creator pass). Until packaging lands, install by reading this doc + the authoritative source.

**Authored:** 2026-05-23
**Author:** gandalf (cross-cutting Stream 3 authoring)
**Authoritative source:** `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`
**Pattern:** universal **router**; load on every session where discipline citation is required
**Companion skills:** `reincarnated-decision-log-format`; `reincarnated-canonical-doc-format`; `reincarnated-critique-pair-gate-protocol`; `reincarnated-hive-mind-protocol`

---

## 0. What this skill IS and IS NOT

**IS:** a **ROUTER**. It carries the when-to-load trigger map (§ 2), the citation rules (§ 3) and the ownership map (§ 5) — the things that are *about* the corpus and are not in it. Loaded on every session that touches code, dispatches, gates, methodology selection, or discipline citation.

⚑ **IS NOT, AND MUST NEVER AGAIN BE: AN ENUMERATION.** This file names no discipline numbers and states no count. If you need to know what exists, **open the source.** The rule that keeps this file honest is a negative one and it is load-bearing: *a router that lists its destinations becomes a second, rotting copy of them.*

**IS NOT:** the authoritative source (that's `engineering-disciplines.md` in engine repo; ALWAYS the single source of truth when discipline text disagrees). NOT a substitute for jack-ryan's Gate-1 / Gate-2 review (jack-ryan applies disciplines; this skill helps agents cite them correctly upfront). NOT the full named-pattern reference (B14.5 V1 primary loop pattern + R-prescriptions live in the engineering-disciplines source).

---

## 1. Where the disciplines are — and why this section no longer lists them

**The corpus lives at `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`. That file is the only authority on which disciplines exist, how many there are, and what each one says. Read it. Do not rely on any list, count or summary held anywhere else, including here.**

### The failure this section is a record of

From 2026-05-23 to 2026-09-21 this section held a table of **twenty** disciplines, and the frontmatter `description` — *the text an agent sees in the skill listing without opening the file* — advertised **"the engineering-disciplines corpus."** **The corpus reached #86.** Sixty-six disciplines were invisible through this surface for four months, including every one that governs instrument design, gate quality and attribution — the disciplines most likely to be wanted by an agent who loads a skill called *engineering-disciplines*.

**Nobody bypassed a rule. The rule was `§ 6`, and `§ 6` was the defect.** Its update protocol read *"a new discipline is ratified (add row to § 1 table)"* — making freshness depend on a manual edit that no ratification checklist ever referenced. It fired zero times in sixty-six opportunities. ⚑ **The protocol written to keep this file current is the reason it rotted.**

### What it is an instance of

- **`#86`** (*a refusal binds the STATE, not the frame it was rendered in*) **in the governance layer.** § 1 rendered an authoritative-looking list; the list did not bind on 66 of 86 entries. § 6's guard sat on one path — *someone remembering to edit this file* — while the path actually taken, a ratification landing in the source, never reached it. **`#86` asks whether a gate RUNS; this one never did.**
- **`#63` / `#75` cl. 1(b)'s own finding, one level up:** *a rule filed where its population does not look.* A wrapper is precisely a place the population does not look, because the population is editing the thing it wraps.
- ⚑ **And the sting: I authored this file, and the run that found it had spent the day citing `#75`, `#80`, `#82`–`#86` — every one of them unlistable here.** The corpus was being used correctly and this surface could not have told anyone so.

### Why the repair is DELETION and not a re-sync

Re-syncing the table to eighty-six entries fixes today and **re-commits the identical defect tomorrow**, because the next mint faces the same un-referenced manual step. A duplicate of a growing corpus drifts *by construction*; the only stable count is none. **What survives here is what genuinely is not in the source** — the trigger map, the citation rules, the ownership map. Those describe *how to use* the corpus and do not change when it grows.

## 2. When to load this skill

⚑ **Triggers are named by SUBJECT, never by number.** A numeric pointer here would rot on the first renumber or retirement and would re-commit § 1's defect at smaller scale — this table was carrying ten such pointers until 2026-09-21. **Find the discipline by its subject in the source; the source's numbering is the source's business.**

| Trigger | Load | Look in the source for |
|---|---|---|
| Authoring a dispatch | Always | the REVIEW_PROCESS principles' parent disciplines |
| Math hotspot work (P2/P3/P5) | Always | methodology-before-execution; math-before-code |
| Cross-seam emission work | Always | schema validation at export boundaries; internal-vs-generative schema separation; round-trip |
| Long-running execution (crawl/ML/sweep) | Always | background execution — the Agent tool is not for waiting |
| External-data acquisition (any crawl) | Always | robots.txt + agent-directive respect |
| Sidecar / attribution analysis | Always | attribution clarity (change one thing, measure one thing); per-variable attribution |
| Pre-tag validation | Always | smoke-test vs full-regen; the empirical-calibration smoke gate |
| Methodology choice at a hotspot | Always | math-before-code; methodology-before-execution |
| **Building or trusting an INSTRUMENT** | **Always** | gate quality, instrument domain, negative controls, preconditions — **the densest and newest region of the corpus, and the one this file hid longest** |
| Routine seam work with no novel patterns | Optional | most disciplines apply universally as background |

---

## 3. Discipline-citation discipline (meta)

When citing a discipline in a dispatch / commit / verdict / handoff:

- **Cite the number AND the name, from the source you just read.** Form: `per Discipline #N — <Name>`, never a bare `#N`. ⚑ **Read the number off the source at citation time** — do not cite a number from memory, from a summary, or from this file, which deliberately holds none.
- **State the application.** Don't just cite — show how the discipline shapes the specific decision
- **Link to the source on first cite in a long artifact.** `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`
- **If you propose a new discipline.** Author at `engineering-disciplines.md` directly; route to jack-ryan for adoption review; do NOT cite as "Discipline #N" until adopted

---

## 4. Named patterns + R-prescriptions

The engineering-disciplines source also contains:

- **B14.5 V1 primary loop pattern** — recompose-first + hybrid rejection gate + adaptive quick-estimate + smoke-test mode (canonical balance-loop pattern)
- **R-prescriptions** — specific remediation prescriptions for recurring failure modes (R8 cohesion-judging, R11 cross-seam round-trip, etc.)
- **Mathematical Layer declaration** (per `gandalf/notes/2026-05-23-mathematical-seam-naming.md`) — cross-cutting layer distributed across existing seams; no dedicated agent

Load the source directly when these patterns are operationally relevant.

---

## 5. Discipline ownership

- **Authoring + ratification:** jack-ryan (process gatekeeper); Matt approves new disciplines
- **Citing in dispatches:** every agent (per work shape)
- **Enforcement at Gate 1 / Gate 2:** jack-ryan
- **Cross-cutting application reminders:** this skill (load on every session that touches discipline-citation work)

---

## 6. Update protocol — deliberately minimal

⚑ **This file does NOT update when a discipline is ratified, amended, renumbered or retired.** That is the whole point of v0.2.0: it holds nothing that a mint could invalidate. The previous protocol demanded a manual re-sync per mint and is the direct cause of the four-month, sixty-six-discipline drift recorded in § 1.

It updates only when **how to use** the corpus changes: a new load-trigger (§ 2), a change to citation rules (§ 3), a change of ownership (§ 5).

**The invariant, and it is the file's only hard rule:** *no enumeration of the corpus — no list of what exists, no count of how many, no one-line summaries, no table of contents, and no numeric pointer offered as live routing.*

⚑ **The one admitted exception, stated because § 1 uses it and a rule its own file breaks is worthless:** a **dated citation about a specific past event** — § 1 cites `#63`, `#72`, `#75`, `#80`, `#82` and `#86` in describing this file's own failure. That is a claim about what happened, not a claim about what exists; it is falsifiable against the record and does not rot when the corpus grows. **The test is the tense.** *"`#86` was ratified on 2026-09-21 and this file is an instance of it"* stays true forever. *"Load this for `#86`"* is a live pointer and is forbidden — it breaks silently the moment `#86` is renumbered, and a silent break in a routing table is exactly what § 1 is a record of. A reviewer who finds an enumeration re-entering this file should delete it and cite this section. If a future author believes a list is needed here, the thing that is actually needed is **a generated one, derived from the source at load time** — never a hand-maintained one.

Authored 2026-05-23 and converted to a router 2026-09-21 by **gandalf** (CANON-STEWARD); ratification routed via jack-ryan per `canonical-doc-format.md` § 6.7. Declared by jack-ryan at the `#86` ratification as a surface he may not edit (`#72` cl. 3); executed here by its author. **The authoritative source is `engineering-disciplines.md` and this file is subordinate to it in every particular.**

---

**Signed:** gandalf (cross-cutting Stream 3 reference-skill author)
**For:** the universal load-on-every-session **router** to the engineering-disciplines corpus. Single source of truth is `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`; this skill provides **when-to-load triggers, citation rules and the ownership map — and no enumeration of any kind.** Loaded by every per-agent OP skill via § 5 universal companion.
