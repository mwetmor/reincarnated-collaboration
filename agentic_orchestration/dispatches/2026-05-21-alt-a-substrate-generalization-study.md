# Dispatch — Alt A: Substrate-Generalization Study (Recompose-Hive Follow-On)

**Date:** 2026-05-21
**Author:** gandalf
**Recipient:** rocket (primary — recent context from recompose-hive P2 diagnostic regens) OR gamora (alternate — sim engine specialist)
**Status:** ACTIVE
**Priority:** MEDIUM (epistemic insurance before QD-rebuild P1 substrate enrichment scope-finalizes)
**Estimated effort:** 4-8 hours of focused analysis (per knight-rider's "hours" estimate)

---

## 0. TL;DR

The recompose-validation hive (closed 2026-05-20) established that **kit-composition pathology IS the load-bearing problem** on shadow substrate. Pattern-A compression at 100% in P2 diagnostic regen on `season_100005`.

**Open question:** does this pathology *generalize* to the other 6 substrates (fire / water / earth / wind / lightning / holy), or is it shadow-specific?

This dispatch commissions a focused analysis to answer that question before QD-rebuild P1 substrate enrichment scope finalizes. **The answer materially shapes P1 W1.11 (element-specific substrate enrichment) — comprehensive vs targeted.**

---

## 1. Context

### 1.1 Recompose-hive findings

Per `canonical/story/per-tier-recompose-validation-findings-2026-05-19.md`:

- 100% Pattern-A (compression-only failures) on shadow substrate at full-season scope
- 0/10 floor-lock in P2 diagnostic regen (recompose mechanism unblocked successfully via Option A)
- Three failure-mode disaggregation: 5a compression-only (8/9), 5b lever-signal-gap (1/9 — class_0001 paradigm-level), class_0009 controller-mechanic mismatch overlay
- Verdict: CANNOT REJECT NULL at SoW § 1 worst-case; H_RC empirically not supported; H_RC_0 reinforced
- Catalogue kit-composition pathology IS load-bearing

### 1.2 Why the generalization question matters for QD-rebuild

The QD-rebuild's P1 substrate enrichment work (per `canonical/story/hive-mind-protocol-qd-engine-rebuild-2026-05-21.md` § 6.2) targets:
- Schema extensions for missing metadata fields
- 4 structurally-missing substrate types (HP-economy, charge-stack, damage-taken-converts, player-side proxies)
- Per-element substrate variety expansion (D2 = 7 elements)
- 5× substrate-sufficiency rule per axis × bin

**If kit-composition pathology generalizes across all 7 substrates,** P1 W1.11 (per-element substrate enrichment) requires comprehensive coverage — each element gets the full enrichment treatment.

**If pathology is shadow-specific,** P1 W1.11 can be more targeted — primary effort on the 5a compression-shift candidates, secondary effort on other elements based on element-specific gaps.

The difference is **~2-3 weeks of P1 budget** and the specific enrichment shape per element.

### 1.3 Why this is "epistemic insurance"

Per knight-rider's Path B framing: ~hours of work to verify a critical assumption before committing weeks of kit-redesign work + months of QD-rebuild substrate enrichment. Cheapest-possible verification.

---

## 2. Scope

### 2.1 Research question

**Does the kit-composition pathology (Pattern-A compression at full-season scope) generalize across the other 6 substrates (fire / water / earth / wind / lightning / holy), or is it shadow-substrate-specific?**

### 2.2 Approach (analytical, not full regen)

The full-season diagnostic regen from P2 was a substantial commission. This study uses **cheaper analytical methods** to triangulate the question:

**Track A — Generation-time substrate variance analysis** (gamora-suitable or rocket-suitable)

For each of the 7 substrates, generate a sample of N=20-40 kits using the current generation system and measure:
- Per-axis BC coordinate distribution (using locked 8-axis spec as the measurement target — even if measurements are partial pre-rebuild)
- Kit-composition variance (covariance across BC axes)
- Compression signature (do kits cluster in narrow BC regions?)

Compare across substrates. If compression signatures are similar across all 7, pathology generalizes. If shadow's signature is markedly compressed relative to others, pathology may be substrate-specific.

**Track B — Recompose-hive P2 telemetry mining** (gamora-suitable)

The P2 diagnostic regen produced telemetry on shadow substrate. Cross-reference with historical telemetry from R1 sprint runs (which covered other substrates) to identify compression-signature comparisons. May not need fresh regens.

**Track C — Spot-check regen on 1-2 alternate substrates** (rocket-suitable; if Tracks A+B inconclusive)

If Tracks A+B don't conclusively answer the question, run focused diagnostic regens on 1-2 alternate substrates (e.g., fire as canonical primary, lightning as recently-added) using same methodology as P2. ~2-4 hours per substrate.

### 2.3 Out of scope

- Full diagnostic regens on all 6 alternate substrates (would be ~12-24 hours of regen time; defeats "cheap epistemic insurance" premise)
- Kit-redesign work (separate scope-of-work — see `agentic_orchestration/dispatches/2026-05-21-kit-redesign-queue-scope.md`)
- New constraint discovery (jack-ryan's audit is the authoritative source)
- Architectural recommendations (those flow into QD-rebuild protocol revisions)

---

## 3. Deliverables

Produce findings at:

```
agentic_orchestration/<rocket-or-gamora>/research/substrate-generalization-study-2026-05-21/
  ├── summary.md                          — synthesis (2-3 pages)
  ├── per-substrate-analysis.md           — Track A findings per substrate
  ├── telemetry-cross-reference.md        — Track B comparison if applicable
  ├── spot-check-regen-findings.md        — Track C if fired
  └── data/
      ├── per-substrate-bc-distribution.csv
      └── compression-signature-comparison.csv
```

### 3.1 summary.md structure

1. **Research question + methodology** — what was tested, how
2. **Verdict** — generalizes / shadow-specific / inconclusive
3. **Per-substrate compression signature comparison** — quantitative
4. **Implications for QD-rebuild P1 W1.11** — comprehensive vs targeted enrichment scope
5. **Implications for kit-redesign queue** — does kit-redesign apply across all substrates or shadow-prioritized
6. **Open questions surfacing from the analysis**

### 3.2 per-substrate-analysis.md structure (one section per substrate)

For each substrate:
- Sample size + generation methodology
- BC coordinate distribution
- Compression signature (variance metrics)
- Comparison to shadow baseline

---

## 4. Methodology constraints

- **Use cheapest method first** — Tracks A+B before Track C
- **Stay analytical, not architectural** — surface findings; don't redesign substrate or propose enrichment in this dispatch's output
- **Cite specifically** — telemetry file paths; specific kits; specific BC coordinates
- **Discipline #11 awareness** — pipeline-state vs equilibrium-state distinction; ensure measurements are equilibrium-state where possible
- **Discipline #13b applied** — attribution claims require ablation evidence; pre-ablation, characterize as candidates

---

## 5. Cross-references

- `canonical/story/per-tier-recompose-validation-findings-2026-05-19.md` — recompose-hive canonical findings
- `canonical/story/hive-mind-protocol-qd-engine-rebuild-2026-05-21.md` — QD-rebuild protocol; § 6.2 W1.11 is the consumer of this study
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` — 8-axis spec for BC coordinate measurement
- `agentic_orchestration/jack-ryan/research/legacy-constraint-audit-2026-05-21/constraint-inventory.md` — LC-002 (fire element bias) is related but distinct

---

## 6. Timing

- **Start:** on Matt's signal (likely next session-open)
- **Target completion:** 4-8 hours of focused analysis (per knight-rider's "hours" estimate; closer to 4 if Tracks A+B conclusive; closer to 8 if Track C fires)
- **Blocks:** QD-rebuild P1 W1.11 substrate enrichment scope-finalization (~3-4 weeks out from now)
- **Concurrent with:** P0 W0.X dispatches (rocket may be running both; non-blocking)

---

## 7. Escalation

- **Methodology questions:** route to gandalf
- **If analysis surfaces a finding that suggests P1 scope changes are needed:** flag immediately to gandalf for protocol revision
- **If Track A is inconclusive AND Track C cost is high:** escalate to gandalf for scope reduction decision

---

**Signed:** gandalf (story-and-design steward)
**For:** epistemic insurance before QD-rebuild substrate enrichment commits to scope.
