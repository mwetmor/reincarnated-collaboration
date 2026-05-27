# 41 — Progression Framework (L50 Hybrid + ~30-Day Seasonal Duration)

> **STATUS:** CURRENT (load-bearing as of 2026-05-27) — foundational architectural commitment locked in Matt + gandalf Pattern-B session 2026-05-27; see `canonical/00-ground-state.md`

**Date:** 2026-05-27
**Author:** gandalf (story-and-design steward)
**Status:** v1 canonical lock — progression framework architecture for Reincarnated v1; substantial latent canon made explicit; per-level scaling math implementation deferred to future design call with empirical-evidence trigger
**Authority:** Matt 2026-05-27 — "the hybrid progression framework (level 50 cap) was exactly my design intent for smaller one month seasons"
**Companion docs:**
- `canonical/00-ground-state.md` — ground-state oracle (this doc registers as new CURRENT entry)
- `canonical/02-roadmap.md` — engine build visual-flow progress tracker
- `canonical/38-downstream-delivery-strategy-2026-05-23.md` — D1-D10 delivery strategy keystone
- `canonical/39-qd-engine-end-to-end-workflow-2026-05-24.md` — engine workflow architecture
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` — Cycle 13 architectural foundation (D1-D86)
- `agentic_orchestration/gandalf/notes/2026-05-27-cycle-13-pre-launch-design-session-closeout.md` — session closeout (source of lock § 6.1)
- `agentic_orchestration/gandalf/notes/2026-05-27-block-c-calibration-scaffolding.md` — Block C calibration scaffolding (uses node identities from this doc)

---

## 0. TL;DR

Reincarnated v1 ships with a **hybrid progression framework**: light leveling (L1-L50 cap) + content-tier-driven endgame progression. Each season runs ~30 days; player progresses L1→L50 over ~3-4 weeks of engagement; endgame phase continues at L50 cap through gear acquisition + chain investment + T4 unlock + set completion. No paragon-style infinite leveling. Cross-season learning loop (D25) refines next-season generation. This framework was latent in skill-point math (Block A3) + seasonal-cycling architecture (D2) + 85th-percentile cumulative engagement target (D18) + 4 progression nodes (D27) + gear tier progression (D50) but had not been explicitly canonicalized until Matt + gandalf Pattern-B session 2026-05-27.

---

## 1. The framework

### 1.1 Core commitment

> **Reincarnated v1 ships with hybrid progression: L1-L50 leveling cap + content-tier-driven endgame progression. Each season ~30 days duration (NOT cadence-term "monthly" — see § 1.4 language discipline). Player levels L1→L50 over ~3-4 weeks engagement; endgame phase continues at L50 cap through gear + chain investment + T4 unlock + set completion. No paragon-style infinite leveling.**

### 1.2 Why hybrid

Two pure architectures considered + the hybrid synthesis adopted:

| Architecture | Description | Why not adopted alone |
|---|---|---|
| **Level-driven (pure)** | Player levels up; per-level stat scaling; monster level-matched (Diablo 1-4, PoE pre-90, classic ARPG) | Pure leveling treadmill in every season creates "every season starts from zero" tedium incompatible with seasonal-cycling cadence (D2); doesn't compose with gear-tier-driven endgame model already implicit in canon (D11 Epic→Legendary discontinuity, D50 drop pool restriction, D27 cumulative engagement target) |
| **Content-tier-driven (pure)** | Player's stats are baseline; power grows through gear + chain investment + T4 unlock; content tiers (T0→T2) provide difficulty progression (PoE post-90 endgame, D3-D4 endgame, LE endgame) | Loses the early-game "leveling up feels like progress" emotional beat that mainstream ARPG audiences expect from the first ~1-2 weeks of a season; harder onboarding for newer players |
| **Hybrid (ADOPTED)** | Light leveling (L1-L50) provides early/mid game progression beats; content-tier-driven dominates endgame post-cap | Captures leveling emotional beat for early/mid game + gear-tier-driven endgame depth + composability with all existing canon |

### 1.3 Why L50 specifically

- **L50 is a small enough cap to be reachable in ~3 weeks of engagement** for the 85th-percentile player (per D18 cumulative target), leaving ~1 week of endgame phase before season close (typical ~30-day season per § 1.4)
- **L50 enables ~50 skill points raw from leveling** (1 per level) which composes with ~20 content-completion bonus points = 70-point endgame budget (locked Block A3) — math anchors cleanly
- **L50 is round enough to be memorable** and matches genre convention for "modest-cap" ARPGs
- **L50 is small enough to NOT create the "leveling treadmill in every season" tedium** that pure-level-driven architectures suffer from in seasonal cadences
- **L50 is large enough to provide ~4 progression nodes worth of leveling content** (per D27 mapping: L1-15 / L15-30 / L30-45 / L45-50+)

### 1.4 ~30-day seasonal duration — NOT cadence-term "monthly"

**Language discipline (per D3 in ground-state DEAD list):** we say "seasonal" as the cadence name + describe duration as "~30-day" or "~1-month." We do NOT use "monthly" as the cadence term itself. D3 (2026-05-23) rejected "monthly" as the cadence term because it implied something specific that "seasonal" doesn't.

**~30-day duration is the typical season length.** Specific duration may vary per season per content-tier engagement requirements; the architectural commitment is to short-cycle seasons (~3-4 weeks engagement + ~1 week endgame phase) compatible with the L50 hybrid framework, NOT to a strict 30-day clock.

### 1.5 Endgame post-cap progression

After player reaches L50 cap, power growth continues through:
- **Gear acquisition** — progression through tier 0 → tier 0.5 → tier 1 → tier 2 legendary/unique/set instances (per D50 drop pool restriction)
- **Chain investment** — completing chains beyond initial investment to maximize per-chain output
- **T4 unlock** — reaching T4-unlock threshold (70% of chain max per Block A3) on multiple chains for build flexibility (T4-respec mechanism per Block A4)
- **Set completion** — assembling 4-piece sets for major build-identity bonuses (per Block B1d)
- **Build refinement** — respec-with-legendary-trigger mechanism (D65) drives gear-acquisition-driven build evolution within the season

**NO PARAGON-style infinite leveling.** Post-cap is gear-and-build-driven, not stat-treadmill-driven.

---

## 2. Composition with existing canon

The framework was latent in MANY existing canonical commitments. Capturing the composition explicitly:

| Canonical element | How L50 hybrid serves it |
|---|---|
| **Skill point earning (Block A3 — 70-point endgame budget)** | L1→L50 = 50 raw points + ~20 content-completion bonuses = 70 endgame anchor ✓ |
| **Per-node graduated investment (Block A3 — 5/15/1 max)** | Math budget calibrated for L50 cap; 70-point budget at ~50% utilization vs ~130-140 max possible per kit |
| **Seasonal cycling (D2 Pattern A)** | ~30-day season = L1→L50 engagement window + endgame phase; cross-season retirement before within-season drift accumulates |
| **85th-percentile cumulative engagement (D18)** | Engagement-time distribution = monthly-bounded; "reaching 85% target by engagement-end" = "reaching endgame phase + meaningful tier 1+2 acquisition within season" |
| **4 progression nodes (D27)** | Maps to level bands: Early (L1-15) / Mid (L15-30) / Endgame-start (L30-45) / Endgame (L45-50+) |
| **Gear tier progression (D50)** | Tier mapping to player level bands: T0 drops early (L1-15); T0.5 mid (L15-30); T1 endgame-start (L30-45); T2 endgame (L45+) |
| **Cross-season learning (D25)** | Each season = one L1→L50+endgame arc; season N telemetry informs season N+1 generation |
| **T4-unlock economics (Block A3 — 70% chain-max threshold)** | Reaching 70-point budget at L50 cap → unlocking 1-2 T4 chains per build identity per season + meaningful partial investment elsewhere |
| **Respec-with-legendary-trigger (D65)** | Drives mid-season build refinement; composes with endgame phase post-L50 |
| **T4-attuned gear (Block B1 content-compositional)** | Tier 1+2 legendary/set carry T4-attunement; only available endgame; composes with endgame phase post-L50 |
| **Spirit-guide projection (D28-D32)** | Projection language bounds to "within ~3-4 weeks engagement" and "endgame phase" — operates on cycle-bounded time, not infinite-progression time |

**This framework was the missing keystone** — explains why so many of these locked architectural choices feel cohesive.

---

## 3. Node identity mapping

The 4 progression nodes (D27) now have explicit level-band identities under L50 hybrid:

| Node | Level band | Content tier (per D50) | Engagement window (~3-4 week season) | Power vector P_node intent (per Block C scaffolding) |
|---|---|---|---|---|
| **Early game** | L1-15 | T0 dominant | First ~1 week | KPM ~20-30 (illustrative); defense uptime ≥70%; resource sustainable; emerging rotation |
| **Mid game** | L15-30 | T0.5 dominant | Week 2 | KPM ~40-55; higher HP scaling; defense uptime ≥75%; sustainable with active management; emerging rotation depth |
| **Endgame start** | L30-45 | T1 dominant (T0+0.5 still drop) | Week 3 | KPM ~60-70; scaling to endgame mobs; defense uptime ≥75%; active resource economy meaningful; full rotation depth emerging |
| **Endgame** (85% target node) | L45-50+ | T1+T2 (all tiers in drop pool) | Week 3-end + endgame phase | KPM ~75+; endgame mob calibrated; defense uptime ≥80%; active resource management critical; full rotation depth |

**P_node target numerical values are ANCHOR INTENTS; gamora calibrates specifics via simulation per Block C scaffolding (`agentic_orchestration/gandalf/notes/2026-05-27-block-c-calibration-scaffolding.md`).**

---

## 4. Deferred commitments

| # | Commitment | Status | Empirical-evidence trigger for re-engagement |
|---|---|---|---|
| 1 | **Per-level scaling formulas** (player HP / mana / base damage / resistances scaling per level; monster stat scaling per level; XP curve from per-content-completion sources to L50; encounter difficulty multipliers per level) | Deferred to future Matt + gandalf Pattern-B design call | Cycle 13 mechanical season gen telemetry OR scaling-implementation cycle scheduled |
| 2 | **Multi-node calibration WORK** (Block C Scaffolds 1+3 per-node numerical calibration across all 4 nodes) | Deferred — gates on #1 | Per-level scaling formulas land (post #1) |
| 3 | **Acquisition curve calibration sharpening** (D21 Option A specifics; calibrated against L50 hybrid engagement window) | Deferred — gates on #1 + per-cohort empirical engagement data | Post-scaling-formulas + telemetry-based per-cohort engagement data |
| 4 | **Pre-L50 mechanical content generation** | Cycle 13 v1 constrained to endgame-reference-encounter only; multi-node mechanical content fires Cycle 14+ | Per-level scaling formulas (#1) + scaling implementation in engine |
| 5 | **Endgame post-cap content scaling** (how content difficulty scales beyond L50 cap via gear-tier interaction) | Implicit in tier mapping (D50) but specific math deferred | Cycle 13 telemetry + Cycle 14+ acquisition curve calibration |

---

## 5. Operational notes

### 5.1 To rocket (generation seam)

L50 hybrid framework affects:
- Phase 2a kit composition — kits generate against the 70-point endgame budget assumption; chain compositions support L50 cap reachability
- Phase 2b T4 algorithm — T4-unlock threshold (70% of chain max per Block A3) calibrated against 70-point endgame budget
- Phase 2d spec-driven gear gen — gear tiers (T0/0.5/1/2 per D50) align to player level bands per § 3
- Phase 2e coherence + faction — supporting chain absorbs class-intrinsic baseline passives per Block A.5 (May 12 trait architecture absorption); supporting chain composition reflects class identity at L1 baseline + grows through investment

### 5.2 To gamora (simulation seam)

L50 hybrid framework affects:
- Cycle 13 v1: calibrate against endgame-reference-encounter (L45-50+ node only); multi-node calibration deferred per #2 above
- Block C scaffolding (Scaffold 1 P_node + Scaffold 3 W function) operates against this framework; per-level scaling math implementation gates on #1 above
- Methodology consultation per D60 + D84 + Discipline #18.2 — node-population sampling considers L50 cap as bounded space (no infinite-progression endgame to sample)

### 5.3 To star-lord (telemetry + LLM seam)

L50 hybrid framework affects:
- Telemetry capture should track per-level engagement data (how long players spend at each level band; what content tiers they engage at each band; KPM/defense-uptime per band)
- This telemetry is INPUT to deferred #1 per-level scaling formulas design call
- Cross-season learning loop (D25) refines next-season generation; star-lord pipeline tracks this

### 5.4 To drax (player surface seam)

L50 hybrid framework affects:
- Loadout app should display player level + level-band context for spirit-guide projections
- Progression UI should show endgame post-cap progression mechanisms (gear acquisition, chain investment, T4 unlock, set completion) as primary post-L50 progression surface, NOT a paragon-style infinite stat treadmill
- Spirit-guide projection language (D31) bounds to season-engagement timeframe (~3-4 weeks)

### 5.5 To jack-ryan (engineering-disciplines seam)

L50 hybrid framework affects:
- Engineering-discipline #21 (no sleep recommendations) + #22 (timezone-agnosticism) compose with this framework's seasonal-cycling cadence (no time-of-day projection onto Matt regarding season timing)
- Discipline candidate: **explicit framework declaration** — when a design surface depends on a framework choice (level-driven vs content-tier-driven vs hybrid), the framework should be canonically declared BEFORE downstream architectural commitments operate against it. This doc is the founding instance of this discipline.

### 5.6 To knight-rider (orchestration seam)

L50 hybrid framework affects:
- Cycle 13 scope constrained to endgame-reference-encounter calibration (per Block C scaffolding § 1.5)
- Cycle 14+ scope expansion candidate: per-level scaling formulas implementation (post deferred-commitment #1 re-engagement)
- Roadmap 02 § 4 active workstreams: this doc lands as foundational architecture; Cycle 13 work proceeds against it
- Cycle 13 scope-doc references this doc + Block C scaffolding for calibration framework

---

## 6. Sign-off

**Author:** gandalf (story-and-design steward)
**Status:** CURRENT — foundational architectural commitment for Reincarnated v1 progression framework
**Composition:** with doc 38 (delivery strategy), doc 39 (engine workflow), doc 40 (gear/balance/guide/multi-T4 architecture), doc 02 (roadmap), and the session closeout doc + Block C scaffolding doc from Matt + gandalf Pattern-B session 2026-05-27

**For:** the L50 hybrid progression framework (~30-day seasonal duration; light leveling L1→L50 + content-tier-driven endgame; node-to-level-band mapping; endgame post-cap progression via gear + chain investment + T4 unlock + set completion; no paragon-style infinite leveling) for Reincarnated v1. Substantial latent canon made explicit per Matt 2026-05-27 design call. Per-level scaling math implementation deferred per § 4 deferred-commitments with empirical-evidence triggers.

**Signed:** gandalf (story-and-design steward)
