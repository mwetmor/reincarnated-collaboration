# cycle-11-hive-mind-scope

> **STATUS:** RATIFIED 2026-05-25 — Matt verbatim authorization across 7 decision items (P1-P3) captured at `agentic_orchestration/matt-log-back-decisions-2026-05-25.md`
> **Cycle:** 11
> **Cycle subject:** v1 implementation push — Algorithm § 8 (6 strategies) + Loadout M1-M6 + Cycle-10 housekeeping
> **Canonical authority basis:** `agentic_orchestration/matt-log-back-decisions-2026-05-25.md`
> **Effective:** 2026-05-25 through Cycle-11-final-tag (estimated ~3 weeks wall-clock = v1.0-T4-post-mortem-readiness)
> **Pattern context:** Cycle 11 is the SECOND application of hive-mind-scope-discipline (Cycle 10 was founding retroactive instance; Cycle 11 is first prospective instance per amended hive-mind-protocol.md § 2.2 step 1.5)

---

## 0. Cycle state at scope-doc authoring

**Just completed (Cycle 10):**
- Cycle 10 substrate-curation workstream FULLY CLOSED 2026-05-25
- Tag `v1.0-weapon-substrate-cycle-10-shipped` cut + pushed (anchored commit `75a1891`)
- v1_scope = 2,293 items LOCKED as substrate for v1
- Hive-mind-scope-discipline pattern PROVEN EFFECTIVE on first test (zero ask-safety pauses; zero Matt mid-cycle escalations)

**Queued for Cycle 11:**
- Algorithm § 8 v1 implementation (6 sim-extension-free strategies) — critical path for T4 post-mortem
- Loadout app M1-M6 implementation — parallel with Algorithm § 8
- Pre-migration mitigation (PRAGMA busy_timeout) — small star-lord work
- Decisions-log canonical-write batch — jack-ryan
- BC-shift validation sweep (Algorithm § 8 cheapest-refuting-test) — rocket compute

**NOT in Cycle 11 (deferred):**
- Pi infrastructure execution (Matt "right moment" deferral)
- Hosted-Postgres setup for loadout DB (deferred per P2a)
- Tailscale install G11 (Matt 15-min window; can fire any time independent of Cycle 11)
- D9 LLM cache build (G12 NOT TRIGGERED)
- Algorithm § 8 v1.1 strategies (4 sim-extension-required + proxy-spawn)
- Loadout v1.1+ items D1-D13
- W1.13 hypothesis testing (chain blocked; gamora awaits prereq resolution)

---

## 1. In-scope autonomous decisions (knight-rider fires without re-asking)

KR fires the following without per-decision Matt re-asking:

- **Dispatch authoring** for Cycle 11 scope items:
  - Pre-migration mitigation dispatch → star-lord (~10 min star-lord work)
  - Decisions-log canonical-write batch → jack-ryan (2 entries + terminology cleanup per P3)
  - Star-lord schema extensions dispatch (4 fields: `t4_alteration_output`, `main_weapon`, `secondary_item`, `source_library`)
  - Drax M4 dispatch (no dependencies; can fire immediately)
  - Drax M1/M2/M5 dispatch (after star-lord schema lands)
  - Drax M3/M6 dispatch (after rocket § 8 + star-lord schema land)
  - Rocket § 8 implementation dispatch (6 v1 strategies; ~1-2 weeks)
  - Rocket BC-shift validation sweep dispatch (cheapest-refuting-test per Discipline #18 + #19.1)
- **Sub-agent invocation sequencing** — when to fire parallel vs sequential; which seam-owners to consult; how to integrate returns
- **Wave-internal failure handling** — retry, scope-reduce, route-to-seam-owner per hive-mind-protocol.md § 3.2
- **Acceptance criterion application** — Gate-2 PASSes; declaring Wave complete vs requiring rework
- **State-file updates** — per-Wave / per-Phase status capture
- **Intermediate tag-cutting** — per-Wave or per-Phase milestone tags per ADR-001 convention
- **Gate-1 critique-pair coordination** — sending dispatches to jack-ryan / gandalf for critique-pair review per `dispatches/README.md`
- **Decision-routing per hive-mind-protocol.md § 4** — seam-owner-first sub-agent invocation for any cross-seam decision

## 2. In-scope autonomous executions

KR executes the following without re-asking:

- All Cycle 11 dispatches once authored + critique-pair-cleared
- Background-process firing per Discipline #19 (nohup, PID tracking, log capture)
- BC-shift validation sweep computation (~200-300 min compute)
- Sub-agent invocations per § 1 above
- Cross-seam parallel critique invocations (jack-ryan + gandalf simultaneously for Gate-1 if warranted)
- DB queries against catalogue substrate for cycle-state verification

## 3. In-scope autonomous commits

Per CLAUDE.md § "Team commit + push discipline" addendum (2026-05-25), KR AUTO-COMMITS:

- Dispatch artifacts (newly authored Cycle 11 dispatches)
- State-file updates
- Wave-closeout summaries
- Gate-1/Gate-2 critique-pair coordination artifacts
- Per-Wave intermediate tag commits
- Sub-agent return capture artifacts (per hive-mind-protocol.md § 5.5.4 file-write-constraint pattern when applicable)

Commit timing: at natural seams (Wave completion, dispatch authoring close, critique-pair clearance). Do not batch beyond a single workstream-day without strong reason.

## 4. Push posture for this cycle

**RATIFIED:** `push-per-wave` — auto-push after each Wave completion AND after each major artifact authoring (dispatch fire-ready, state-file update).

**Rationale:** Cycle 10 push-per-wave authorization worked cleanly (no incidents); Matt confirmed pattern preference 2026-05-25; Cycle 11 inherits.

**Override:** if a Wave includes uncommitted multi-day work that's mid-experiment (e.g., rocket § 8 implementation mid-BC-shift-validation-sweep), KR can defer push until experiment stabilizes — flag deferral in state-file.

## 5. Out-of-scope — MUST escalate to Matt

KR escalates the following:

- **Architectural amendments** to canonical docs — gandalf authors; Matt ratifies
- **Scope amendments to Cycle 11** — adding workstreams beyond § 0 enumeration; expanding Algorithm § 8 to v1.1 strategies; changing M1-M6 list; firing Pi infrastructure execution before Matt "right moment"
- **Cross-cycle commits** — anything outside Cycle 11 scope (e.g., W1.13 re-fire; Pi infrastructure work; hosted-Postgres setup; Cycle 12 prep)
- **ADR-002 tier-2/3 decisions** — anything per `GOVERNANCE.md` ADR-002 requiring Matt
- **Final Cycle 11 tag** (`v1.0-T4-post-mortem-ready` or KR's judgment) — Matt ratifies before final tag is cut
- **Cycle 11 wind-down summary author + close** — KR drafts; Matt reviews + ratifies (UNLESS skip-confirmation directive ratified for Cycle 11 wind-down at that time)
- **Algorithm § 8 BC-shift validation sweep finding "poor differentiation"** — if validation shows the algorithm produces insufficient keystone differentiation, escalate before broader rocket commitment fires
- **Sim-seam boundary surprise** — if rocket § 8 implementation surfaces that one of the 6 "sim-extension-free" strategies actually requires sim hooks, route to gamora sub-agent for verification first; if genuine boundary issue, escalate to Matt for scope amendment (4 → 5 strategies in v1; or move 1 to v1.1)
- **P2b "Confirm minima" ambiguity surfacing** — if KR interprets Matt's "Confirm minima" as Natural Subset (6) but downstream work suggests Matt may have meant MINIMAL cherry-pick (3-4), KR routes back BEFORE rocket § 8 dispatch fires

## 6. Pre-resolved known-unknowns

| If this happens | Then |
|---|---|
| Algorithm § 8 BC-shift validation sweep returns mid-tier differentiation (acceptable but not strong) | Route to gandalf sub-agent for design-fit critique; if gandalf says "acceptable for v1 ship," fire forward; if gandalf says "needs refinement before v1 ship," escalate to Matt |
| Algorithm § 8 BC-shift validation sweep returns clean strong differentiation | Fire forward; gandalf confirmation light-touch; no Matt re-engagement |
| Star-lord schema extension surfaces a backwards-compat issue with existing loadout app code | Route to drax sub-agent for triage; if recoverable via migration, fire forward; if requires breaking change, escalate to Matt |
| Drax M1-M6 implementation surfaces UI question not pre-resolved by drax memo Q1-Q5 | Route to gandalf Pattern A-light for design-fit critique; integrate return; fire forward |
| Jack-ryan decisions-log batch surfaces additional canonical-write items beyond the 2 enumerated in P3 | Defer additional items to v1.1+ canonical-authoring queue UNLESS gandalf flags critical |
| Rocket § 8 implementation surfaces that one of the 6 strategies has performance issues | Route to rocket+gamora sub-agent collaboration; if recoverable via optimization, fire forward; if not, escalate for v1.1 deferral of that one strategy (5 of 6 in v1 acceptable) |
| Pre-migration mitigation (PRAGMA busy_timeout) causes regression in any star-lord workflow | Star-lord triages + reverts via dispatch; flag to KR; no Matt re-engagement unless regression is severe |
| Specialist failure mid-execution | Apply hive-mind-protocol.md § 3.2 Wave-internal failure handling; route to seam-owning sub-agent for triage |
| KR encounters genuinely-unenumerated decision | Default to in-scope per scope-discipline § 5.3 anti-pattern guard; fire forward via hive-mind decision-routing § 4 (seam-owner-first); flag the gap to gandalf for next-cycle scope-doc refinement |
| Mac mini kernel panic recurs during sustained Cycle 11 workload | Star-lord triages; if PRAGMA busy_timeout mitigation insufficient + Postgres migration is the only path, escalate to Matt for "right moment" trigger (infrastructure execution authorization) |
| W1.13 chain unblocks (e.g., rocket completes P1 enrichment as side-effect of Algorithm § 8 work) | Surface to Matt at next natural seam; do NOT autonomously re-fire W1.13 dispatch — that's a fresh Matt-authorization |
| G11 Tailscale install fires (Matt's 15-min window) | Acknowledge; no Cycle 11 impact (independent task) |

## 7. Cross-cycle escalation triggers

Scope-doc applicability ENDS (triggers re-scoping) when:

- Cycle 11 final tag is cut (then Cycle 12 scope-doc authored)
- Matt issues a directive that materially changes Cycle 11 scope (e.g., "pause Cycle 11 to fire infrastructure now")
- An architectural recognition surfaces mid-cycle that warrants protocol amendment (gandalf authors recognition record; Matt ratifies scope-doc amendment OR cycle-reset)
- Algorithm § 8 BC-shift validation sweep returns "FAIL" (architecture doesn't differentiate keystones meaningfully) — triggers re-scoping; may require return to skill-system § 8 design

---

## 8. Sequencing recommendation (KR's discretion within scope)

Recommended parallel-fire pattern at Cycle 11 open (KR's discretion; not prescriptive):

**Day 1 (immediate fires):**
- Pre-migration mitigation dispatch → star-lord (~10 min; fires first as zero-dependency)
- Decisions-log canonical-write batch → jack-ryan (~1-2 hrs; fires in parallel)
- Drax M4 dispatch → drax (~0.25 day; fires in parallel)
- Star-lord schema extensions dispatch → star-lord (~1.75-3.25 days; fires in parallel)
- Rocket § 8 implementation dispatch → rocket (~1-2 weeks; fires in parallel; BC-shift validation sweep mid-flight)

**Day 4-7 (after star-lord schema lands):**
- Drax M1 / M2 / M5 dispatch → drax (~2.25 days; gated on schema)

**Day 10-21 (after rocket § 8 lands):**
- Drax M3 / M6 dispatch → drax (~3 days; gated on § 8 + schema)
- T4 post-mortem readiness milestone

---

## 9. Sign-off

**Drafted by:** gandalf (story-and-design steward) 2026-05-25 (Pattern-B dialogue with Matt + decision-surface synthesis)
**Ratified by:** Matt 2026-05-25 — session dialogue ("2 = confirm; 3 = confirm; 4 = authorize; 5 = confirm; 6 = confirm minima; 7 = approved" + P1 = "I already had KR commit/push. If the tag isn't cut yet I authorize that also")
**Authority basis:**
- `agentic_orchestration/operating-procedures/hive-mind-scope-discipline.md` (the discipline this doc instantiates per § 2.1 + hive-mind-protocol.md § 2.2 step 1.5)
- `agentic_orchestration/matt-log-back-decisions-2026-05-25.md` (canonical capture of Matt's 7 decisions)
- `agentic_orchestration/cycle-10-wind-down-summary-2026-05-25.md` (Cycle 10 close context)
- Legolas methodology recommendation at `agentic_orchestration/legolas/research/algorithm-section-8-methodology-consult-2026-05-25/methodology-recommendation.md`
- Drax loadout scoping memo at `agentic_orchestration/drax/notes/2026-05-25-loadout-app-readiness-scoping.md`
- Pi recognition record at `canonical/story/infrastructure-raspberry-pi-postgres-and-closed-loop-pipeline-2026-05-25.md`

**Effective immediately on commit.**
