# Dispatch — Kit-Redesign Queue: Scope-of-Work (Parallel Track to QD-Rebuild)

**Date:** 2026-05-21
**Author:** gandalf
**Recipient:** rocket (primary; specialist on generation seam)
**Status:** **QUEUED — DO NOT FIRE UNTIL P0 SHIPS** (`v0.0-constraint-removal-shipped` tag)
**Priority:** MEDIUM (Reincarnated near-term content path; runs parallel to QD-rebuild from P1)
**Estimated effort:** 4-6 weeks of focused specialist work
**Earliest fire date:** ~2026-06-04 to 2026-06-11 (post-P0 completion)

---

## 0. TL;DR

The recompose-hive established kit-composition pathology as the load-bearing problem. The QD-rebuild's architectural answer (22-33 weeks) doesn't deliver shippable Reincarnated content in the near term. **Kit-redesign queue ships hand-tuned tactical content in ~4-6 weeks of post-P0 specialist work.**

**Critical sequencing constraint:** kit-redesign does NOT start until P0 (constraint removal) ships. B6 energy-type fix (LC-004) and archetype refactor (LC-001) must land first, or kit-redesign tunes against shifting baseline.

**Forward-compatibility design:** every redesigned kit explicitly targets a BC cell address from the locked 8-axis spec. Kits become forward-compatible reference archetypes for QD-rebuild P7 W7.2 validation. **Interim canonical until QD-archive ships v8.0-qd-engine-final.**

---

## 1. Context

### 1.1 Why this dispatch exists

Per Matt 2026-05-21: "I accept blended path A and kit redesign in parallel if no foreseen adverse effects." This dispatch is the kit-redesign track of that parallel commission.

Per gandalf adverse-effects analysis: parallel kit-redesign + QD-rebuild is viable IF and ONLY IF kit-redesign is sequenced to start after P0 ships. The two HIGH-risk adverse effects (resource contention + architectural drift) are mitigated by sequencing, not by avoidance.

### 1.2 What the recompose-hive's 5a/5b/class_0009 disaggregation tells us

Per `canonical/story/per-tier-recompose-validation-findings-2026-05-19.md`:

- **5a compression-only (8/9 cases):** composition-shift candidates — kits with insufficient range; redesign opens range
- **5b lever-signal-gap (1/9 — class_0001):** paradigm-level mismatch (Diablo II Frozen-Orb vs Lightning analog); redesign targets BC cell discrimination
- **class_0009 controller-mechanic mismatch overlay:** controller archetype mis-fit; redesign targets Axis 2B (control density) + Axis 4 (defensive) accuracy

These three failure modes map directly to specific redesign approaches.

### 1.3 Why target Profile A core archetypes only (not all 38/51 R1 failures)

The kit-redesign queue could target all 38/51 R1 failures (4-6 weeks of dedicated work). But:
- QD-rebuild will eventually replace ALL kits via archive-derived equivalents
- Manual hand-tuning of 38 kits is substantial waste if QD-archive replaces them
- Profile A near-term ship requires only the **core archetypes that need to ship in Reincarnated Phase 0**

**Scope is intentionally smaller: 8-12 core Profile A archetypes.** Other failed kits wait for QD-engine archive treatment.

---

## 2. Scope

### 2.1 Target archetype list (gandalf-authored; subject to Matt revision before fire)

The 8-12 core Profile A archetypes should cover the recognizable ARPG class identities across the 7 elements. Initial proposal (12 candidates; final 8-12 selection at fire time):

| # | Archetype | Element | Locked BC cell address (target) |
|---|---|---|---|
| 1 | Fire DPS wizard (Disintegrate / Meteor caster) | fire | [ranged-slow, large-AOE OR multi-spawn, low-tempo, spiky, mitigator, generator-spender] |
| 2 | Ice control sorceress (Frozen Orb stand) | water | [ranged-slow, multi-spawn, low-tempo, flat, mitigator, steady] |
| 3 | Lightning chain caster (Chain Lightning) | lightning | [ranged-fast, chain, high-tempo, flat, mitigator, steady] |
| 4 | Earth defender (Phalanx-equivalent) | earth | [close-slow OR mid-slow, multi-spawn, low-tempo, flat, tank, generator-spender] |
| 5 | Wind speedster (cyclone-channel barbarian) | wind | [close-fast, small-AOE, high-tempo, flat, mitigator, generator-spender] |
| 6 | Holy paladin (Hammer-rotation) | holy | [mid-slow, multi-spawn, medium-tempo, variable, tank, generator-spender] |
| 7 | Shadow rogue (DoT-stack assassin) | shadow | [mid-fast, single-target, medium-tempo, variable, dodger, generator-spender] |
| 8 | Fire ranger (Multishot-equivalent) | fire | [ranged-fast, multi-spawn, high-tempo, flat, dodger, generator-spender] |
| 9 | Water frost-mage (control-pure variant) | water | [ranged-slow, small-AOE, low-tempo, flat, glass, steady] |
| 10 | Earth tank (turtle-build) | earth | [close-slow, small-AOE, low-tempo, flat, tank, steady] |
| 11 | Wind hunter (kite-archer) | wind | [ranged-fast, single-target, high-tempo, flat, glass, generator-spender] |
| 12 | Holy support (aura-stacker) | holy | [mid-slow, small-AOE, low-tempo, flat, mitigator, charge-stack OR overflow] |

This is a 12-archetype canonical Profile A roster across 7 elements × 4-5 role variants. Matt may revise selection before fire.

### 2.2 Per-kit redesign methodology

For each target kit:

**Step 1 — BC cell target verification.** Confirm the target BC cell address is reachable given current substrate (post-P0 state). Surface any gap to gandalf before redesign begins.

**Step 2 — Reference-archetype analysis.** Identify the ARPG-canonical exemplar this kit channels (e.g., D3 Wizard for #1, D2 Sorc for #2, etc.). Document the reference build's signature properties.

**Step 3 — Composition redesign.** Hand-tune the kit's composition to:
- Hit the target BC cell address
- Match the reference-archetype signature properties
- Resolve any failure-mode classification from recompose-hive (5a compression-shift, 5b paradigm-targeting, controller-mechanic alignment)
- Avoid legacy-constraint regression (Discipline #13a; jack-ryan critique-pair)

**Step 4 — Empirical validation.** Run the kit through convergence + per-tier WR test:
- Convergence at expected modifier range
- Per-tier WR matches design targets (swarm 0.65-0.80; magic 0.55-0.70; elite 0.45-0.60; mini-boss 0.35-0.55; boss 0.30-0.45)
- BC coordinate lands in target cell (using best-available BC measurement; full measurement requires P2 ship)

**Step 5 — Critique-pair review.** jack-ryan critique (legacy-constraint regression check); gandalf critique (archetype-recognition alignment); Matt approval (if structural).

**Step 6 — Tag fire.** Per-kit completion fires `kit-redesign/v1.X-<archetype-name>` tag.

### 2.3 Out of scope

- Substrate enrichment (that's QD-rebuild P1)
- BC measurement infrastructure (QD-rebuild P2)
- Schema extensions (QD-rebuild P1 W1.1)
- New canonical document authoring beyond kit-specific records
- Any kit NOT in the 8-12 core Profile A roster

---

## 3. Deliverables

Per redesigned kit:

```
agentic_orchestration/rocket/kit-redesign/<kit-name>-<date>/
  ├── redesign-record.md         — full redesign rationale + reference + final composition
  ├── convergence-validation.md  — empirical convergence + per-tier WR results
  ├── critique-pair-records.md   — jack-ryan + gandalf critiques
  └── data/
      ├── kit-composition.csv
      └── convergence-telemetry.csv
```

Aggregate deliverables on queue completion:

```
agentic_orchestration/rocket/kit-redesign-queue-summary-2026-XX-XX/
  ├── queue-summary.md                 — synthesis across all 8-12 kits
  ├── archetype-coverage-matrix.md     — BC cell coverage from queue
  ├── reincarnated-phase-0-handoff.md  — ship-readiness brief
  └── data/
      ├── all-kits-bc-coordinates.csv
      └── per-kit-convergence.csv
```

---

## 4. Methodology constraints

- **Forward-compatible design:** every kit targets a specific BC cell address using the locked 8-axis spec. Kits become reference archetypes for QD-rebuild P7 W7.2 validation.
- **Legacy-constraint regression guard:** every kit critique includes Discipline #13a check against jack-ryan's 62-constraint inventory.
- **Discipline #11 awareness:** BC coordinate measurement is equilibrium-state, not pipeline-state.
- **Interim canonical labeling:** all kits explicitly labeled "interim canonical until QD-archive ships v8.0-qd-engine-final." No false-permanence claims.
- **Tag namespace discipline:** `kit-redesign/v<X.Y>-<descriptor>`. Separate from `qd-rebuild/v<X.Y>-<descriptor>`.
- **Telemetry source-tagging:** all sim runs from this queue include track-source attribution (`kit-redesign-queue` vs `qd-rebuild-validation`).

---

## 5. Cross-references

- `canonical/story/per-tier-recompose-validation-findings-2026-05-19.md` — recompose-hive findings; failure-mode disaggregation
- `canonical/story/hive-mind-protocol-qd-engine-rebuild-2026-05-21.md` — QD-rebuild protocol; this queue runs parallel to P1-P7
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` — 8-axis spec for BC cell target addressing
- `agentic_orchestration/jack-ryan/research/legacy-constraint-audit-2026-05-21/constraint-inventory.md` — 62-constraint inventory for regression checks
- `reincarnated-engine/design/decisions/decisions-log.md` — B6 energy-type fix (LC-004; lands in P0 W0.1)

---

## 6. Timing

- **Fire condition:** P0 ships (`v0.0-constraint-removal-shipped` tag fires)
- **Earliest fire date:** 2026-06-04 to 2026-06-11 (estimated P0 completion)
- **Duration:** 4-6 weeks (8-12 kits × ~3-4 days per kit including critique-pair + empirical validation)
- **Reincarnated Phase 0 ship-ready:** ~2026-07-09 to 2026-07-23
- **Concurrent with:** QD-rebuild P1 (substrate enrichment) through P3 (archive) — kit-redesign output feeds P7 W7.2 reference-archetype validation

---

## 7. Sunset / replacement protocol

When QD-engine ships Profile A (v8.0-qd-engine-final), QD-archive-derived kits replace kit-redesign output. Kit-redesign kits transition to "reference archetype" status — they remain in canonical record as validation targets but no longer ship as Profile A content.

This is **intentional planned obsolescence**, not failure. Kit-redesign serves the near-term ship; QD-engine serves the architectural ship; the transition is the design.

---

## 8. Escalation

- **Sequencing question (does P0 actually need to ship first?):** route to gandalf — adverse-effect analysis is documented; deviation requires gandalf approval
- **Kit selection revision (Matt wants different archetype list):** Matt revises at fire-time
- **Convergence failure during validation:** specialist reports; gandalf + jack-ryan diagnose; may surface new constraint not in audit
- **Forward-compatibility conflict (target BC cell unreachable post-P0):** flag to gandalf; may trigger P1 substrate enrichment scope revision

---

**Signed:** gandalf (story-and-design steward)
**For:** the parallel kit-redesign + QD-rebuild commitment.
