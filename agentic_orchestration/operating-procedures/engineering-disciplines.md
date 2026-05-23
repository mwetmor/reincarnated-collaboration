# reincarnated-engineering-disciplines — Cross-cutting Reference Skill

> **STATUS:** CURRENT (load-bearing as of 2026-05-23) — Stream 3 cross-cutting reference skill per `canonical/02-roadmap.md` § 2.2
>
> **Skill packaging:** Markdown source for the eventual installable skill `reincarnated-engineering-disciplines` (per doc 38 § 4 step 2 + Skill Creator pass). Until packaging lands, install by reading this doc + the authoritative source.

**Authored:** 2026-05-23
**Author:** gandalf (cross-cutting Stream 3 authoring)
**Authoritative source:** `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`
**Pattern:** universal reference wrapper; load on every session where discipline citation is required
**Companion skills:** `reincarnated-decision-log-format`; `reincarnated-canonical-doc-format`; `reincarnated-critique-pair-gate-protocol`; `reincarnated-hive-mind-protocol`

---

## 0. What this skill IS and IS NOT

**IS:** the universal reference wrapper for the 20 engineering disciplines. Names each discipline with a one-line summary; provides when-to-cite triggers; cross-references to the authoritative source. Loaded on every session that touches code, dispatches, gates, methodology selection, or discipline citation.

**IS NOT:** the authoritative source (that's `engineering-disciplines.md` in engine repo; ALWAYS the single source of truth when discipline text disagrees). NOT a substitute for jack-ryan's Gate-1 / Gate-2 review (jack-ryan applies disciplines; this skill helps agents cite them correctly upfront). NOT the full named-pattern reference (B14.5 V1 primary loop pattern + R-prescriptions live in the engineering-disciplines source).

---

## 1. The 20 disciplines (one-line each)

| # | Discipline | When it bites |
|---|---|---|
| 1 | **Math-before-code on non-trivial changes** | Any change introducing new variance, constraint behavior, or convergence dynamics |
| 2 | **Smoke-test vs full-regen discipline** | Iteration cycles (smoke); milestones (full) |
| 3 | **No parallel regens of same seed** | Multiple agents touching same DB / seed simultaneously |
| 4 | **Right tool for the validation question** | Picking smoke/full/unit-test/sweep/sidecar per question shape |
| 5 | **Triage discipline — blocking vs downstream** | Multi-issue sessions; sort what blocks ship vs what's follow-on |
| 6 | **Tag intermediate states; small checkpoints** | Every Wave / phase boundary; pre-risky operations |
| 7 | **Capture decision telemetry for archaeology** | Every decision; especially novel methodology choices |
| 8 | **Schema validation at export boundaries** | Cross-seam emissions (telemetry, export, output DTOs) |
| 9 | **Test assertions derive from spec sources** | No magic numbers in tests; assertions trace to spec |
| 10 | **Attribution clarity — change one thing, measure one thing** | Lever changes; sweep design; sidecar analyses |
| 11 | **Empirical inspection over assumption** | Every methodology gate; before committing post-execution conclusions |
| 12 | **Semantic-shifting fixes need explicit framing** | When a debugging move silently changes what a test validates |
| 13a | **Drift detection** | Cross-session continuity; implicit-pillar drift watchfulness |
| 13b | **Per-variable attribution** | Sidecar analyses; multi-source-feature provenance tracking |
| 14 | **Internal-vs-generative schema separation** | Engine internal vs LLM-facing schema boundaries |
| 15 | **UI scope decomposition** | Every player-facing engine feature; demo/loadout integration |
| 16 | **Tuning-drift discipline (perception asymmetry)** | Cross-session constant changes; perception/measurement gaps |
| 17 | **Empirical-calibration smoke gate** | Before full-regen / full-salvage with a new lever |
| 18 | **Methodology-before-execution (math-hotspot discipline)** | P2/P3/P5 statistical methodology selection; legolas Mode A consult required |
| 19 | **Agent tool is not for waiting** | All long-running phases as background processes; no Agent-tool polling |
| 20 | **robots.txt + Claude-agent directive respect** | Any crawl-based source; per-source verification pre-fire |

---

## 2. When to load this skill

| Trigger | Load |
|---|---|
| Authoring a dispatch | Always (Principle 1-6 of REVIEW_PROCESS.md derive from disciplines) |
| Math hotspot work (P2/P3/P5) | Always (#18 governs) |
| Cross-seam emission work | Always (#8, #14, Principle 6 round-trip) |
| Long-running execution (crawl/ML/sweep) | Always (#19) |
| External-data acquisition (any crawl) | Always (#20) |
| Sidecar / attribution analysis | Always (#10, #13b) |
| Pre-tag validation | Always (#2, #17) |
| Methodology choice at a hotspot | Always (#1, #18) |
| Routine seam work with no novel patterns | Optional (most disciplines apply universally as background) |

---

## 3. Discipline-citation discipline (meta)

When citing a discipline in a dispatch / commit / verdict / handoff:

- **Cite the number AND the source.** Example: "per Discipline #18 — Methodology-before-execution" not just "#18"
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

## 6. Update protocol

This skill evolves when:
- A new discipline is ratified (add row to § 1 table; cite trigger)
- A discipline is amended (update one-line summary; full text always in source)
- A new named pattern lands (extend § 4)
- A new R-prescription lands (extend § 4)

Authored / maintained by **gandalf** (cross-cutting Stream 3 owner); ratifications routed via jack-ryan. The authoritative source remains `engineering-disciplines.md` — this skill is the cross-session lookup wrapper.

---

**Signed:** gandalf (cross-cutting Stream 3 reference-skill author)
**For:** the universal load-on-every-session reference wrapper for the 20 engineering disciplines. Single source of truth remains `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`; this skill provides one-line discipline summaries + when-to-cite triggers + named-pattern cross-references. Loaded by every per-agent OP skill via § 5 universal companion.
