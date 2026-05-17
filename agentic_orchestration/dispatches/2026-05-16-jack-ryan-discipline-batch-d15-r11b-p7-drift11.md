# Dispatch — 2026-05-16 — jack-ryan — Engineering-disciplines batch: D15 (UI scope decomposition) + R11(b) cluster + P7 cluster + Drift-11 sibling-sweep

**From:** knight-rider (authored per Matt directive Day-4 close: gandalf v2 Path A-prime Matt-decision #3 — AUTHORIZE gandalf + jack-ryan co-authorship of forward disciplines batch; one coordinated pass beats four piecemeal amendments)
**To:** jack-ryan
**Approved by:** Matt at 2026-05-16 Day 4
**Status:** PENDING
**Mode:** Engineering-disciplines authoring (jack-ryan's lane; consumes gandalf's design-side input from canonical docs)
**Estimated effort:** 1 session (~2-3h); coordinated discipline pass

**Gate-1 bypass rationale:** N/A — jack-ryan IS the Gate-1 reviewer; this is direct Matt-routed engineering-disciplines authoring with gandalf design-side input via existing canonical docs.

**Acceptance summary:** `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` amended with D15 (UI scope decomposition for player-facing engine features) + R11(b) cluster codification (cross-seam round-trip discipline; already operationalized via REVIEW_PROCESS.md Principle 6 but needs disciplines.md codification) + Pattern P7 cluster codification (silent-drop disciplinary cluster; already operationalized via recorder fail-loud R11(d) but needs disciplines.md codification) + Drift-11 sibling-cluster-sweep lesson (NEW; per gandalf carry-forward). Discipline-13a-lineage prescription noted (consume PIL-measured empirical baseline over extrapolated reference estimates).

---

## Why this dispatch exists

Three discipline-extension candidates have accumulated through Day-4 work + 1 surfaced today by gandalf:

1. **D15 — UI scope decomposition for player-facing engine features.** Surfaced via gandalf P6 forward audit. Pattern: every player-facing engine feature should have an explicit UI scope decomposition (what's the visible surface? what's queued? what's deferred?) authored before implementation begins. Audio Phase-1 framework + B6 skill-tree UI + embodiment-display loadout all required these decompositions post-hoc; D15 codifies the pre-condition.

2. **R11(b) cluster codification.** R11(b) (cross-seam round-trip discipline) was operationalized today as REVIEW_PROCESS.md Principle 6 + dispatch-template "Cross-seam contract change?" section. Decisions-log entry committed earlier today. **Needs codification in engineering-disciplines.md** so future developers see it in the canonical discipline list alongside other R-prescriptions (R1-R11(a), R11(d)).

3. **Pattern P7 cluster codification.** Pattern P7 (test scaffolding masks production defect; silent-drop pattern) was operationalized via recorder fail-loud R11(d) + the Stage B export-DTO finding pattern. **Needs codification in engineering-disciplines.md** as a named pattern alongside P6 / P8.

4. **Drift-11 sibling-cluster-sweep lesson** (NEW; from gandalf canonical-amendments batch return). Pattern: when a deferred milestone surfaces ONE upstream-of-near-term-ship dependency, sweep for sibling dependencies in the same session; they tend to cluster. Gandalf recommended NOT a separate amendment — feed as input to discipline pass. **This dispatch is that pass.**

5. **Discipline-13a-lineage prescription** (NEW; from Matt's own drift-ownership today on the 1.31× math error). Pattern: consume PIL-measured empirical baseline over extrapolated reference estimates when both exist in working tree. Matt's self-correction names the Discipline #13a pattern; codify as forward-protection.

**Per Matt:** one coordinated discipline pass beats four piecemeal amendments. **This is that pass.**

## Cross-seam contract change?

**Round-trip: not applicable** — engineering-disciplines.md amendment; no schema or runtime contract change; no production code modified. Per R11(b) Principle 6 (which this dispatch codifies).

## What this dispatch produces

### Track 1 — D15 codification (UI scope decomposition)

Author D15 entry in engineering-disciplines.md. Consume gandalf's design-side input from:
- `canonical/story/audio-scoping-framework-2026-05-16.md` (audio Phase-1 framework — 7 sub-axes decomposition)
- `canonical/story/b6-skill-tree-ui-scoping.md` (B6 UI scope decomposition)
- `canonical/story/embodiment-display-loadout.md` (embodiment-display first-surface decomposition)
- `canonical/story/p6-forward-audit-2026-05-16.md` (gandalf P6 forward audit)

D15 prescription: every player-facing engine feature MUST have a UI scope decomposition authored before implementation begins. Includes: visible surface (what player sees); queued surface (what's planned next); deferred surface (what's explicitly out-of-scope); cross-seam dependencies; first-commission triggers.

Forward-protection rationale: prevents recurrence of the audio Phase-1 "atomic deferral" P6 risk pattern.

### Track 2 — R11(b) cluster codification

Codify R11(b) (cross-seam round-trip discipline) in engineering-disciplines.md alongside R1-R11(a). Consume:
- `agentic_orchestration/REVIEW_PROCESS.md` Principle 6 (the Gate-1 hook)
- `agentic_orchestration/dispatches/README.md` "Cross-seam contract change?" section
- Decisions-log entry from earlier today (R11(b) discipline operationalization)
- 2 P7 instances cited as empirical justification (gamora V2.1 emission-gap fix `df717a8`; star-lord Stage 2 cosmological vocabulary `4bbc906`)

Add to disciplines.md R-prescription list. Brief — codification, not re-justification (decisions-log entry has the full reasoning).

### Track 3 — Pattern P7 cluster codification

Codify Pattern P7 (test scaffolding masks production defect; silent-drop pattern) in disciplines.md alongside P6 / P8. Consume:
- `canonical/story/drift-audit.md` § Pattern P7 (the source-of-truth definition)
- R11(d) recorder fail-loud (the operationalized prescription)
- Star-lord Stage B export-DTO silent-drop finding (Matt-named gandalf finding)

Add to disciplines.md Pattern list. Cross-reference R11(b) cluster (R11(b) is the cross-seam-contract-change Gate-1 hook; P7 is the underlying drift pattern P-NN).

### Track 4 — Drift-11 sibling-cluster-sweep lesson codification

Codify Drift-11 sibling-cluster-sweep lesson as a discipline-style prescription. Consume:
- `canonical/story/drift-audit.md` Drift-11 (the source pattern)
- Gandalf canonical-amendments batch return note (surfaced this lesson explicitly)

Prescription: when a deferred milestone surfaces ONE upstream-of-near-term-ship dependency, sweep for sibling dependencies in the SAME session; they tend to cluster.

### Track 5 — Discipline-13a-lineage prescription (Matt's drift self-correction)

Codify Matt's self-correction lesson from the 1.31× math drift. Consume:
- Matt's drift-ownership message (the gandalf math error trace)
- Discipline #13a (implementation-vs-intent drift) — extend with this lineage-specific prescription

Prescription: when both PIL-measured empirical baseline AND extrapolated reference estimate exist in working tree, ALWAYS consume the PIL-measured baseline. Pre-PIL legolas estimates (or any pre-empirical-measurement extrapolation) are obsoleted by post-PIL empirical measurements; do not consume the older figure without checking against the newer.

Worth naming as a sub-prescription under Discipline #13a rather than a new discipline number (extends existing #13a; doesn't establish a new pattern).

### Track 6 — Gandalf co-authoring input loop

Jack-ryan operates analytical-only per persona. Gandalf's design-side input is consumed via the canonical docs cited in Tracks 1-4. If gaps surface during authoring:
- For D15: jack-ryan calls out scope-decomposition methodology gaps; gandalf-authored canonical docs are the input source
- For other tracks: gandalf's role is design-side input only; jack-ryan owns the disciplines.md authorship

If jack-ryan finds the canonical docs insufficient for any track, surface to knight-rider for routing additional gandalf input dispatch BEFORE proceeding.

## Out of scope (explicit)

- **NO code authorship** (jack-ryan analytical-only)
- **NO new ADR drafting** (extends existing disciplines + patterns; does not create new ADRs)
- **NO B14.5 / V2 priority restructuring**
- **NO retrospective audit of existing dispatches** (forward-looking only; per R11(b) decisions-log entry standard)
- **NO Discipline #15 numbered-discipline addition** for R11(b) cluster (R11(b) operationalizes cleanly as a process gate per Gate-1 hook; doesn't generalize to within-seam work)
- **NO codification of D14** (already codified per decisions-log entry today)
- **NO unilateral disciplines re-numbering** (preserve existing numbering; extend in-place)
- **NO gandalf-direct authorship of disciplines.md** (gandalf is design-side input only; jack-ryan owns the file)

## Required reading

- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (the target file; current state)
- `canonical/story/audio-scoping-framework-2026-05-16.md` (D15 input)
- `canonical/story/b6-skill-tree-ui-scoping.md` (D15 input)
- `canonical/story/embodiment-display-loadout.md` (D15 input)
- `canonical/story/p6-forward-audit-2026-05-16.md` (D15 input)
- `agentic_orchestration/REVIEW_PROCESS.md` Principle 6 (R11(b) input)
- `agentic_orchestration/dispatches/README.md` "Cross-seam contract change?" section (R11(b) input)
- Decisions-log entry on R11(b) discipline operationalization (R11(b) input; today's commit)
- `canonical/story/drift-audit.md` § Pattern P7 + Drift-11 (P7 + Drift-11 input)
- Star-lord Stage B export-DTO silent-drop finding (P7 input): `agentic_orchestration/gandalf/findings/2026-05-16-export-dto-stage-b-silent-drop.md`
- Matt's drift-ownership message (forwarded today; #13a-lineage input)
- Gandalf canonical-amendments batch return note (Drift-11 sibling-cluster-sweep surfacing)

## Acceptance criteria

- [ ] D15 entry added to engineering-disciplines.md (UI scope decomposition prescription)
- [ ] R11(b) cluster codified in disciplines.md alongside R-prescriptions
- [ ] Pattern P7 cluster codified in disciplines.md alongside P6/P8
- [ ] Drift-11 sibling-cluster-sweep lesson codified as discipline-style prescription
- [ ] Discipline-#13a-lineage sub-prescription added (PIL-measured-baseline-over-extrapolated)
- [ ] Cross-references between disciplines + canonical sources + decisions-log
- [ ] No new disciplines #15+ (R11(b) cluster stays as R-prescription per earlier jack-ryan judgment)
- [ ] Knight-rider notified with: amendments summary, any gaps in gandalf canonical input that required surfacing back

## Tag policy

- **No git tag** (jack-ryan analytical output; engineering-disciplines.md commit suffices for traceability)

---

## Completion record

**Completed:** 2026-05-16
**Amendments summary:**
- **D15 (Track 1):** Discipline #15 added as a numbered core discipline. Five-element decomposition template (visible / queued / deferred / cross-seam dependencies / first-commission triggers). Gate-1 question codified. Three canonical examples cited (b6-skill-tree-ui-scoping, embodiment-display-loadout, audio-scoping-framework). Positioned between #14 and the R-prescriptions section.
- **R11(b) (Track 2):** New "R-prescriptions" section created in disciplines.md. R11(b) codified with cross-seam contract change trigger table (5 field types), two required acceptance-criteria clauses (round-trip smoke OR not-applicable justification), Gate-1 BLOCK trigger, Gate-2 check. Cross-referenced to REVIEW_PROCESS.md Principle 6, dispatches/README.md, decisions-log entry "2026-05-16: R11(b) cross-seam round-trip discipline operationalized as Gate-1 hook".
- **Pattern P7 (Track 3):** New "Named patterns" section created. P7 (test scaffolding masks production defect; silent-drop) codified with four-step pattern shape, two empirical instances (gamora V2.1 `df717a8`; star-lord Stage B `4bbc906`), prevention prescription (R11(b) primary; R11(d) code-layer). Pattern P6.a also codified in same section (implicit-bundled UI surfaces) as a companion entry. Both cross-reference Drift-12, Drift-11, and the relevant disciplines.
- **Drift-11 sibling-cluster-sweep (Track 4):** "Sibling-cluster-sweep lesson" section added (below Named patterns, above Terminology Lock). Not a numbered discipline. Prescription: one dependency found = sweep for siblings in same session. Operational example (MS baseline + Gate-3b sim-consumption both VS2a-gating, Day-4 same session). Gate-1 question codified.
- **Discipline #13a-lineage (Track 5):** Sub-prescription added between #13a and #13b. PIL-measured empirical baseline supersedes pre-measurement extrapolation. Operational example: JRPG-extrapolated 80-100px → PIL-measured ARPG-empirical 100-130px (~31% gap). Gate-1 question covers pixel scale, damage magnitudes, telemetry counts, and any other numerical baseline. Cross-referenced to legolas Section 3 + embodiment-display-loadout § 1.1.

**Gaps in gandalf canonical input (if any):** none. All five tracks had sufficient canonical-doc input. No escalation to knight-rider was required.

**Notes for knight-rider:**
- File is at `/Users/admin/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — 449 lines (was 286). Net additions: 163 lines.
- Document anatomy section added to "How to extend this document" explaining the three-tier structure (numbered disciplines / R-prescriptions / named patterns).
- Cross-references section expanded to include drift-audit, p6-forward-audit, REVIEW_PROCESS.md Principle 6, and dispatches/README.md.
- No existing discipline content was altered; all additions are net-new sections or sub-prescriptions within existing numbered entries.
- No new ADR authored. No decisions-log entry authored (the decisions-log entries for R11(b) and #13a/#13b/#14 were already committed today per the dispatch).
- No git tag per dispatch policy (jack-ryan analytical output; commit suffices).
