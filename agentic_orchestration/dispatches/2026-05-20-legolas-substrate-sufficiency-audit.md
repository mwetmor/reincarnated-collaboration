# Dispatch — Legolas Mode A: Substrate-Sufficiency Audit for QD-Engine BC Axes

**Date:** 2026-05-20
**Author:** gandalf
**Recipient:** legolas (Mode A — analytical research)
**Status:** ACTIVE
**Priority:** HIGH (gates QD-engine rebuild commitment)
**Estimated effort:** 8-14 hours of structured research + synthesis

---

## 0. TL;DR

The QD-engine architectural vision (`canonical/story/engine-architecture-vision-qd-profile-2026-05-19.md`) commits to MAP-Elites over 6 mechanical Behavior Characteristic (BC) axes. For QD to function, the generative substrate must produce **at minimum ~5× as many distinguishable outputs as the bin count of each axis.** If the substrate is undersupplied on any axis, that axis becomes dead — its bins fill unevenly or not at all, and the QD gate produces no signal.

**Your task:** audit the current substrate per axis × bin, identify gaps relative to the 5× sufficiency rule, recommend enrichment paths (internal palette extension / engine-system extension / external asset acquisition), and estimate prerequisite cost.

---

## 1. The 6 locked BC axes

(Subject to refinement during concurrent axis-lock theory-craft between gandalf and Matt. Treat as load-bearing but possibly revised by ~2026-05-21. If axes shift, gandalf will issue an amendment.)

| # | Axis | Bins | Bin labels (provisional) |
|---|---|---|---|
| 1 | **Engagement profile** (range × mobility composite) | 6 | close-fast / close-slow / mid-fast / mid-slow / ranged-fast / ranged-slow |
| 2 | **Damage geometry** | 5 | single-target / small-AOE / large-AOE / chain / multi-spawn |
| 3 | **Damage rhythm** | 4 | spike / mixed / sustained / channeled |
| 4 | **Defensive profile** | 4 | tank / mitigator / dodger / glass |
| 5 | **Resource economy** | 4 | starved / generator-spender / steady / overflow |
| 6 | **Proxy + control composite** | 5 | solo-damage / solo-control / hybrid / proxy-damage / proxy-control |

**Sufficiency rule:** substrate must produce ≥ 5× the bin count of distinguishably-different outputs per axis. For axis 1 (6 bins) that's ~30 outputs; axis 2 (5 bins) ~25; axis 3 (4 bins) ~20; etc.

---

## 2. Research scope

### 2.1 Internal substrate inventory (Mode A internal codebase survey)

For each axis × bin, document what currently exists in the engine that could feed that bin:

- **Generation systems** — which `reincarnated-engine/src/reincarnated/generation/`, `element/`, `anchor/`, `foundation/` modules contribute?
- **Canonical palette / library** — what's in `reincarnated-engine/src/reincarnated/canonical/`?
- **Skill / gear / kit templates** — current variety; tagging discipline (are skills tagged for their BC contribution today, or would tagging need to be added?)
- **Simulation outcomes** — what does the simulator currently *measure* that could become the BC coordinate calculator? (E.g., AOE-share can be computed from per-skill `is_aoe` flags + damage attribution.)

### 2.2 External enrichment landscape (Mode A external research)

For axes where internal substrate is undersupplied, survey external sources. **Survey only — do not commit to acquisition; this is research, not procurement.**

- **Unity Asset Store** — VFX packs relevant to damage-geometry axis (AOE shapes, chain-lightning effects, multi-spawn visualizations). Document: pack name, asset count, price tier, license terms, asset count *of the type we need* (not total pack count).
- **Mixamo** — animation arc library. Document: relevant animation categories (movement/dodge/melee-arc/cast-arc), animation count per category.
- **OpenGameArt / Kenney / itch.io game-asset packs** — open-source / royalty-free alternatives.
- **ARPG canonical reference counts** — Diablo 3/4 skill databases, PoE skill gem inventory, Last Epoch skill tree counts, Grim Dawn class data. How many distinguishable values exist in shipped ARPGs per axis? This sets a market-comparable target.

### 2.3 Cross-axis observations

After per-axis work, surface cross-axis patterns:

- Which axes are most undersupplied? (Where does enrichment have highest leverage?)
- Which axes are over-supplied? (Where can we widen bins for finer discrimination?)
- Are any axes structurally impossible given current architecture? (E.g., if the simulator has no concept of "channeled skill," the damage-rhythm "channeled" bin can never be populated until simulation gets channeled-skill support.)

---

## 3. Deliverables

Produce a Mode A research readout at:

```
agentic_orchestration/legolas/research/substrate-sufficiency-audit-2026-05-2X/
  ├── summary.md              — synthesis (3-5 pages)
  ├── per-axis-detail.md      — axis-by-axis findings (longer; per-bin breakdown)
  ├── data/
  │   ├── axis-1-engagement.csv
  │   ├── axis-2-geometry.csv
  │   ├── axis-3-rhythm.csv
  │   ├── axis-4-defensive.csv
  │   ├── axis-5-economy.csv
  │   ├── axis-6-proxy-control.csv
  │   └── external-asset-landscape.csv
  └── prerequisite-cost-estimate.md — engineering hours per gap-closure path
```

### 3.1 summary.md structure

1. **Executive summary** — one paragraph per axis: sufficient / marginal / undersupplied
2. **The blocking-gap table** — axes where current substrate < 2× bin count (these block QD rebuild)
3. **Prioritized enrichment recommendations** — what to do first; rough sequencing
4. **External-acquisition shortlist** — top 3-5 asset sources worth procurement evaluation
5. **Engine-extension shortlist** — top 3-5 internal palette/system extensions needed
6. **Open questions** — places where the audit surfaced ambiguity that needs gandalf or Matt input

### 3.2 per-axis-detail.md structure (repeat 6 times)

For each axis:

- **Bin definitions (operational, not vague)** — what *exactly* makes a skill/kit/season land in each bin
- **Current substrate inventory** — what exists per bin
- **Substrate count vs 5× rule** — concrete numbers
- **Gap analysis** — which bins underfilled
- **Enrichment options** (ranked by cost-effectiveness)
- **Sufficiency verdict** — sufficient / marginal (1-3× rule) / undersupplied (<1× rule) / structurally-blocked

### 3.3 data CSVs

Per axis, a CSV with columns:

| bin_label | current_substrate_count | distinguishable_outputs_estimate | gap_to_5x_rule | enrichment_source | enrichment_cost_estimate |

---

## 4. Methodology constraints

- **Read-only across all sources.** No code changes, no asset acquisitions, no schema modifications. Pure research.
- **Cite specifically.** Internal: file paths + line numbers. External: pack name + URL + asset count + license.
- **Estimate honestly.** When "distinguishable output count" is fuzzy, say so. Better to flag as `~15-25, hard to count` than commit to a false-precision `19`.
- **Stay in Mode A.** Do not invoke sub-agents (per `.claude/agents/legolas.md` § sub-agent constraint).
- **No commitment authority.** Recommendations are recommendations; gandalf reviews + Matt approves before procurement or engineering work begins.

---

## 5. Cross-references

- `canonical/story/engine-architecture-vision-qd-profile-2026-05-19.md` — the architectural target; § 2 BC axes; § 6 dependency chain
- `canonical/story/hive-mind-protocol-per-tier-recompose-validation-2026-05-19.md` — concurrent hive (recompose validation); ships before QD rebuild begins
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — disciplines #13a / #13b drift attribution; substrate-sufficiency audit is in part a #13b ablation precondition
- `canonical/09-geometry-palette-discussion.md` — 16-type geometry palette decision; reference for axis 2 baseline
- `canonical/17-gear-and-spirit-guide-design.md` — gear + spirit guide architecture; touches axes 3, 4, 5

---

## 6. Timing

- **Start:** immediately on receipt
- **Target completion:** 3-5 days (8-14 hours of focused research time)
- **Blocks:** QD-engine rebuild start (cannot commit until audit + axis-lock both ship)
- **Concurrent with:** axis-lock theory-craft (gandalf + Matt; may produce minor axis revisions; gandalf will amend dispatch if axes shift)
- **Hive context:** recompose-validation hive is firing in parallel; do not interrupt or coordinate with it; this audit is independent

---

## 7. Escalation

- **Methodology questions:** route to gandalf
- **Scope/priority disputes:** gandalf decides; escalate to Matt only if gandalf+legolas cannot converge
- **External-asset license ambiguities:** flag in summary.md § 6 open questions; do not attempt to resolve

---

**Signed:** gandalf (story-and-design steward)
**For:** the QD-engine architectural commitment
