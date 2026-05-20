# Dispatch — Legolas Mode A: Substrate-Sufficiency Audit for QD-Engine BC Axes

**Date:** 2026-05-20
**Author:** gandalf
**Recipient:** legolas (Mode A — analytical research)
**Status:** ACTIVE (amended 2026-05-20 evening — 8-axis final lock + Unity VFX directive elevation)
**Priority:** HIGH (gates QD-engine rebuild commitment)
**Estimated effort:** 14-22 hours of structured research + synthesis (raised from initial 8-14 estimate after 8-axis lock + external-asset-acquisition elevation)

---

## 0. TL;DR

The QD-engine architectural vision (`canonical/story/engine-architecture-vision-qd-profile-2026-05-19.md`) and the locked operational spec (`canonical/story/qd-engine-bc-axes-lock-2026-05-20.md`) commit to MAP-Elites over **8 mechanical Behavior Characteristic (BC) axes** with 68,040 cells total. For QD to function, the generative substrate must produce **at minimum ~5× as many distinguishable outputs as the bin count of each axis.** If the substrate is undersupplied on any axis, that axis becomes dead — its bins fill unevenly or not at all, and the QD gate produces no signal.

**Your task — two-track audit:**

1. **Internal substrate inventory** — what does the current engine already produce per axis × bin?
2. **External-asset-acquisition research** — what Unity Asset Store VFX packs, Mixamo animations, and open-source asset libraries can be acquired to fill substrate gaps? **This is a primary deliverable, not a secondary suggestion.** Matt's directive (2026-05-20): "legolas needs to bring these in from Unity VFX." The expectation is concrete shortlists with pack names, asset counts, prices, license terms, and per-axis-bin mapping.

---

## 1. The 8 locked BC axes (FINAL — companion spec at `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md`)

| # | Axis | Bins | Bin labels |
|---|---|---|---|
| 1 | **Engagement profile** (range × mobility) | 6 | close-fast / close-slow / mid-fast / mid-slow / ranged-fast / ranged-slow |
| 2 | **Damage geometry** | 5 | single-target / small-AOE / large-AOE / chain / multi-spawn |
| 2A | **Proxy density** | 3 | solo / proxy-light / proxy-heavy |
| 2B | **Control density** | 3 | damage-pure / mixed / control-pure |
| 3A | **Damage tempo** | 3 | low / medium / high |
| 3B | **Damage amplitude variance** | 3 | flat / variable / spiky |
| 4 | **Defensive profile** | 4 | tank / mitigator / dodger / glass |
| 5 | **Resource economy** | 7 | HP-economy / charge-stack / damage-taken-converts / starved / overflow / generator-spender / steady |

**Sufficiency rule:** substrate must produce ≥ 5× the bin count of distinguishably-different outputs per axis.

| Axis | Bins | Substrate target | Current state (pre-audit prior) |
|---|---|---|---|
| 1 | 6 | ~30 engagement profiles | Likely partial — range tagged; mobility undertagged |
| 2 | 5 | ~25 damage geometries | Likely strong — 16-type palette adopted; verify distribution |
| 2A | 3 | ~15 proxy configurations | **Likely severely undersupplied** — player-side proxies absent |
| 2B | 3 | ~15 control compositions | Likely moderate — confirm CC variety |
| 3A | 3 | ~15 damage tempos | Likely moderate — depends on skill cadence variety |
| 3B | 3 | ~15 variance profiles | Likely moderate |
| 4 | 4 | ~20 defensive profiles | Mixed — tank/mitigator/glass likely OK; dodger likely partial |
| 5 | 7 | ~35 economy mechanisms | **Likely severely undersupplied** — charge mechanics + damage-conversion absent |

**The two-track sufficiency check:** for every axis × bin, is it sufficient via (a) current internal generation alone, OR (b) current + cost-effective external asset acquisition? Audit must answer per bin.

---

## 2. Research scope — two tracks

### 2.1 Track A — Internal substrate inventory (codebase survey)

For each axis × bin, document what currently exists in the engine that could feed that bin:

- **Generation systems** — which `reincarnated-engine/src/reincarnated/generation/`, `element/`, `anchor/`, `foundation/` modules contribute?
- **Canonical palette / library** — what's in `reincarnated-engine/src/reincarnated/canonical/`?
- **Skill / gear / kit templates** — current variety; tagging discipline (are skills tagged for their BC contribution today, or would tagging need to be added?)
- **Simulation outcomes** — what does the simulator currently *measure* that could become the BC coordinate calculator?

**Key existing references:**
- `canonical/09-geometry-palette-discussion.md` — 16-type damage geometry palette (feeds Axis 2)
- `canonical/17-gear-and-spirit-guide-design.md` — gear architecture (feeds Axes 3, 4, 5)
- `canonical/32-progression-design.md` + `canonical/33-progression-skeleton.md` — class progression structure
- `reincarnated-engine/src/reincarnated/canonical/` — engine's internal canonical library

### 2.2 Track B — External-asset-acquisition research (PRIMARY DELIVERABLE)

**Matt's directive 2026-05-20:** "legolas needs to bring these in from Unity VFX." This means external asset research is not a sidebar — it's a core deliverable. The QD-engine substrate enrichment plan WILL involve external asset acquisition; the audit must produce the concrete shortlist that enables that acquisition decision.

#### 2.2.1 Unity Asset Store (PRIORITY)

Survey Unity Asset Store comprehensively for VFX assets relevant to each axis × bin. For each candidate pack:

**Required documentation per pack:**
- Pack name + Unity Asset Store URL
- Publisher + reputation indicators (rating, sales volume, review count)
- Total asset count + **asset-count-of-the-type-we-need** (most important — the former is often inflated)
- Price tier (USD)
- License terms (single-seat / commercial / royalty-free / attribution requirements)
- Per-axis-bin mapping (which assets serve which BC dimensions)
- Quality assessment (preview review)

**Search priorities by axis:**

| Axis | Unity Asset Store search targets |
|---|---|
| Axis 1 (Engagement) | Movement-skill VFX packs (dash, blink, teleport, charge animations); cyclone/channel-move VFX; ranged-cast traversal effects |
| Axis 2 (Geometry) | AOE VFX packs (radial blasts, ground-effect persistent), chain-lightning packs, multi-spawn / meteor / area-explosion packs, single-target projectile packs |
| Axis 2A (Proxy) | Summon/minion/totem VFX; spawn-effect VFX; convert/charm effect packs |
| Axis 2B (Control) | CC-effect VFX (stun, freeze, root, fear, blind, knockback); slow-aura VFX; debuff visualizations |
| Axis 3 (Rhythm) | Channel-skill VFX; charge-up-effect packs; burst-skill telegraph VFX |
| Axis 4 (Defense) | Shield/aura VFX; dodge/iframe visual cues; stealth/invisibility shaders; reflection effects; thorns/spike-aura packs |
| Axis 5 (Economy) | Resource-conversion VFX (life-leech, mana-conversion); charge-stack visualizers; HP-cost visual feedback |

**Don't pre-restrict** to listed search targets if you find adjacent relevant packs. Surface anything that serves substrate enrichment.

#### 2.2.2 Mixamo (PRIORITY)

Animation arc library for character + monster movement, attack, dodge, casting profiles. Document:

- Available animation categories relevant to each axis
- Per-category animation count (e.g., "27 melee-arc animations," "14 cast-arc animations," "8 dodge-roll animations")
- License terms (Mixamo is free with Adobe account but commercial-use terms vary)
- Per-axis-bin mapping (which animations serve which BC dimensions, especially Axis 1 mobility + Axis 2 geometry)

#### 2.2.3 OpenGameArt / Kenney / itch.io (SECONDARY)

Open-source / royalty-free alternatives to Unity Asset Store. Lower priority but worth surveying for:
- Cost-free substrate fills (where free assets meet quality threshold)
- License-cleaner alternatives where commercial Unity assets have problematic licensing
- Stylistic alternatives (pixel-art, hand-drawn — relevant to galadriel's locked style register)

#### 2.2.4 ARPG canonical reference counts (BENCHMARK)

This is **benchmark research, not procurement research.** Document how many distinguishable values exist in shipped ARPGs per axis as a market-comparable target:

- Diablo 3/4 skill database (Diablofans, Maxroll, official wiki)
- Path of Exile skill gem inventory (PoE Wiki, official tree)
- Last Epoch skill counts (LE wiki)
- Grim Dawn class data (Grim Dawn wiki)
- Diablo Immortal skill catalog

Per axis, what does each shipped ARPG ship? This sets a "minimum competitive substrate" baseline.

### 2.3 Special audit items — deferred-bin substrate

Several BC bins route to **deferred-evaluation pool** in current sim state (see `qd-engine-bc-axes-lock-2026-05-20.md` § 5 Sim Deferral Matrix). The substrate audit must still cover these — we need to know what generation enrichment will be required when sim catches up:

| Deferred bin | Substrate audit priority |
|---|---|
| Axis 2A proxy-light + proxy-heavy | **High** — substantial known gap; player-side proxy generation absent |
| Axis 4 dodger stealth/iframe/reflection sub-cases | **High** — sim extension parallel work; substrate variety needs early audit |
| Axis 5 charge-stack mechanic | **High** — generation infrastructure for charge-pool absent |
| Axis 5 damage-taken-converts | **High** — generation infrastructure for damage-to-resource absent |
| Axis 3B channeled-tag | Moderate — channel-tagged skill mechanic |

For each deferred bin, the audit reports:
1. What generation infrastructure would be needed to produce kits in this bin?
2. What sim extension would be needed to evaluate kits in this bin?
3. What external assets (Unity VFX, Mixamo) would support visual realization of this bin?
4. Cost estimate for end-to-end enablement?

### 2.4 Cross-axis observations

After per-axis work, surface cross-axis patterns:

- Which axes are most undersupplied? (Where does enrichment have highest leverage?)
- Which axes are over-supplied? (Where can we widen bins for finer discrimination?)
- Are any axes structurally impossible given current architecture?
- **Which Unity packs / Mixamo categories serve MULTIPLE axes?** (Cross-cutting acquisitions = best $/bin ratio)
- **What's the cheapest path to QD-rebuild readiness?** (Combined external + internal cost estimate)

---

## 3. Deliverables

Produce a Mode A research readout at:

```
agentic_orchestration/legolas/research/substrate-sufficiency-audit-2026-05-2X/
  ├── summary.md                       — synthesis (4-6 pages)
  ├── per-axis-detail.md               — axis-by-axis findings (longer; per-bin breakdown)
  ├── unity-asset-store-shortlist.md   — PRIMARY deliverable: pack-by-pack acquisition shortlist
  ├── mixamo-animation-inventory.md    — animation-category catalog with per-axis mapping
  ├── opengameart-survey.md            — open-source alternatives
  ├── arpg-canonical-benchmarks.md     — shipped-game substrate reference
  ├── data/
  │   ├── axis-1-engagement.csv
  │   ├── axis-2-geometry.csv
  │   ├── axis-2A-proxy.csv
  │   ├── axis-2B-control.csv
  │   ├── axis-3A-tempo.csv
  │   ├── axis-3B-variance.csv
  │   ├── axis-4-defensive.csv
  │   ├── axis-5-economy.csv
  │   ├── unity-pack-candidates.csv
  │   ├── mixamo-animation-categories.csv
  │   └── arpg-canonical-substrate-counts.csv
  └── prerequisite-cost-estimate.md    — engineering hours + asset acquisition $ per gap-closure path
```

### 3.1 summary.md structure

1. **Executive summary** — one paragraph per axis: sufficient / marginal / undersupplied via internal + external paths
2. **The blocking-gap table** — axes where (internal + reasonable external acquisition) < 2× bin count (these block QD rebuild)
3. **Prioritized enrichment recommendations** — what to do first; rough sequencing; combined internal + external
4. **Unity Asset Store shortlist** — top 5-10 packs worth procurement evaluation, with rough $ totals
5. **Mixamo shortlist** — top animation categories for acquisition
6. **Engine-extension shortlist** — top 5-10 internal palette/system extensions needed
7. **Total estimated procurement cost** — combined Unity + Mixamo + engineering hours
8. **Open questions** — places where the audit surfaced ambiguity that needs gandalf or Matt input

### 3.2 per-axis-detail.md structure (repeat 8 times — one per axis)

For each axis:

- **Bin definitions (canonical from lock doc)** — reference, not re-stated
- **Current internal substrate inventory** — what exists per bin
- **Substrate count vs 5× rule** — concrete numbers
- **Gap analysis per bin** — which bins underfilled
- **Internal enrichment options** (engine extension, palette expansion, generation-system additions)
- **External enrichment options** (Unity packs, Mixamo categories, OpenGameArt) — **per bin**
- **Combined sufficiency verdict** — sufficient / marginal (1-3× rule via combined) / undersupplied (<1× rule even with reasonable external) / structurally-blocked
- **Estimated cost to reach sufficient** — engineering hours + asset $ + acquisition complexity

### 3.3 unity-asset-store-shortlist.md structure (PRIMARY DELIVERABLE)

Pack-by-pack acquisition shortlist. For each pack:

- Pack name + Unity Asset Store URL
- Publisher
- Price (USD) + license tier
- Total asset count + usable-for-our-purposes count
- **Per-axis-bin coverage matrix** — which BC bins does this pack feed?
- Quality assessment (review-based)
- Acquisition priority (P1/P2/P3)
- Notes (substitutes, related packs, licensing concerns)

Aim for 15-30 pack candidates. Final shortlist of 5-10 with strongest cost/coverage ratio.

### 3.4 data CSVs

Per-axis CSVs:

| bin_label | current_internal_substrate_count | distinguishable_outputs_estimate | gap_to_5x_rule | internal_enrichment_path | internal_enrichment_cost_hours | external_enrichment_recommendation | external_cost_usd | combined_sufficiency_verdict |

Unity pack candidates CSV:

| pack_name | url | publisher | price_usd | license_tier | total_assets | usable_assets | axis_1 | axis_2 | axis_2A | axis_2B | axis_3A | axis_3B | axis_4 | axis_5 | priority | notes |

---

## 4. Methodology constraints

- **Read-only across all sources.** No code changes, no asset acquisitions, no schema modifications. Pure research.
- **Cite specifically.** Internal: file paths + line numbers. External: pack name + URL + asset count + license terms verbatim.
- **Estimate honestly.** When "distinguishable output count" is fuzzy, say so. Better to flag as `~15-25, hard to count` than commit to a false-precision `19`.
- **Stay in Mode A.** Do not invoke sub-agents (per `.claude/agents/legolas.md` § sub-agent constraint).
- **No commitment authority.** Recommendations are recommendations; gandalf reviews + Matt approves before procurement or engineering work begins.
- **External-acquisition research is mandatory, not optional.** Matt's explicit directive: legolas brings in Unity VFX (and analogous external assets). The Unity Asset Store shortlist is a required deliverable; the audit is incomplete without it.

---

## 5. Cross-references

- `canonical/story/engine-architecture-vision-qd-profile-2026-05-19.md` — the architectural target
- **`canonical/story/qd-engine-bc-axes-lock-2026-05-20.md`** — **AUTHORITATIVE 8-axis operational spec; this dispatch operationalizes the audit of that spec**
- `canonical/story/hive-mind-protocol-per-tier-recompose-validation-2026-05-19.md` — concurrent hive (recompose validation); ships before QD rebuild begins
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — disciplines #13a / #13b drift attribution; substrate-sufficiency audit is in part a #13b ablation precondition
- `canonical/09-geometry-palette-discussion.md` — 16-type geometry palette decision; reference for Axis 2 baseline
- `canonical/17-gear-and-spirit-guide-design.md` — gear + spirit guide architecture; touches Axes 3, 4, 5

---

## 6. Timing

- **Start:** immediately on receipt
- **Target completion:** 5-7 days (14-22 hours of focused research time)
- **Blocks:** QD-engine rebuild start (cannot commit until audit + recompose-hive both ship)
- **Concurrent with:** recompose-validation hive (firing now); no interaction needed
- **Output review:** gandalf reviews on completion; Matt approves any procurement decisions

The estimate raised from 8-14 hours (original dispatch) to 14-22 hours reflects:
- Axis count expansion from 6 to 8
- Bin count expansion (notably Axis 5 from 4 → 7 bins)
- Unity Asset Store shortlist elevation to primary deliverable
- Mixamo + OpenGameArt formalization

---

## 7. Escalation

- **Methodology questions:** route to gandalf
- **Scope/priority disputes:** gandalf decides; escalate to Matt only if gandalf+legolas cannot converge
- **External-asset license ambiguities:** flag in summary.md § 8 open questions; do not attempt to resolve
- **If audit surfaces axes that look structurally impossible given current architecture:** flag immediately to gandalf; may trigger axis-lock revision

---

**Signed:** gandalf (story-and-design steward)
**For:** the QD-engine architectural commitment, fully operationalized.
