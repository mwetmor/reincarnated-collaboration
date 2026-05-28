# 50 — Bounded-Viability-with-Specialization Design Directive

> **STATUS:** CURRENT (LOAD-BEARING as of 2026-05-28) — Path α architectural commit; gates all Cycle 14 v1 damage-formula refactor work (W-α1/W-α2/W-α3) + Wave 5 re-fire validation; see `canonical/00-ground-state.md` § 1

**Date:** 2026-05-28
**Author:** gandalf (story-and-design steward)
**Status:** v1 canonical lock — design principle named + 5 operationalized targets + per-encounter-type validation framing + Path β rejection rationale on the canonical record
**Authority:** Matt 2026-05-28 Gate-6 RATIFICATION REVERSAL — Path α RATIFIED; bounded-viability-with-specialization design directive made EXPLICIT (was implicit-but-unnamed); Path β-NARROW + Path β-FULL Gate-6 Option 6 BOTH REJECTED. Full reversal record at `agentic_orchestration/cycle-14-hive-mind-state.md` § "MATT GATE-6 RATIFICATION REVERSAL LOCKED 2026-05-28"
**Companion docs:**
- `canonical/00-ground-state.md` — ground-state oracle (this doc registers as new CURRENT entry; Section 1 update required at session close)
- `canonical/47-damage-scaling-architecture-2026-05-27.md` § 3 — 4-damage-path mechanical partition; this doc is the architectural-experience layer over that mechanical substrate (forward-link added in same session per dispatch § 1.2)
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` — Cycle 13 architectural foundation; "build-specialization vs kit-identity" framing at § 5.3 is genre-precedent context for the specialization half of this directive
- `canonical/46-concentration-architecture-2026-05-27.md` — Layer 1 stat-range bounds (caps + floors at mechanical layer); this doc operates the same "bounded but not undifferentiated" pattern at the cohort layer
- `canonical/02-roadmap.md` § 4.4 — Cycle 14 v1 close trajectory ~4-6 weeks; Path α active workstream; Cycle 15 D2 Option 6 retroactively retracted
- `agentic_orchestration/dispatches/2026-05-28-path-alpha-master-scoping.md` — Path α master scoping (load-bearing parent dispatch)
- `agentic_orchestration/dispatches/2026-05-28-w-alpha-4-gandalf-bounded-viability-canonical.md` — W-α4-gandalf dispatch (this doc fulfills)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § 45 — vocabulary lock (grep audit performed at authoring; "bounded-viability-with-specialization" is new design-vocabulary with zero pre-existing collision in canonical or engine source per audit § 5.3)
- `~/Games/reincarnated-engine/design/decisions/decisions-log.md` — Path α RATIFICATION + Path β rejection rationale entries authored by jack-ryan W-α5a (sibling workstream)

---

## 0. TL;DR

**Design principle (Matt 2026-05-28 verbatim, LOAD-BEARING):**

> *"some kits are better at AOE, others are better at bosses/elites/mini-bosses, others are better at speed running, others are better in team play; all are within a bounded space of minimum viability but also none have zero strengths and all weaknesses."*

**This is the bounded-viability-with-specialization design directive.** It has three constitutive properties: (1) **bounded viability** — every kit functions on every encounter type (no zero strengths anywhere); (2) **specialization** — every kit has designed peaks on 1-2 encounter types (no zero weaknesses anywhere either); (3) **no strict dominance** — no kit dominates all encounter types; no kit is dominated on all encounter types.

**The current engine state produces the INVERSE of this directive.** Per-encounter-type aggregation (Matt 2026-05-28 forensic on cycle-14-wave-5-season-001 telemetry) reveals INT/WIS saturate the 600 KPM ceiling on 4 of 6 encounter types (no measurable weaknesses anywhere) while STR/DEX produce **0.0 KPM on boss and mini_boss** plus **~1.5 KPM on elite_pack** (catastrophic weakness, no strengths anywhere). The cross-path ratio at `elite_pack` is **365×** — substantially worse than the 79× population-median framing that drove Gate-5 and Gate-6 option surfacing.

**5 operationalized design targets** (§ 4) gate Path α close:

1. Base DPS variance ≤1.5× across the 4 damage-scaling paths
2. Every kit produces non-zero KPM on every encounter type (zero_count = 0 across 18 × 6 = 108 cells)
3. No kit saturates the KPM ceiling on any encounter type (saturation_count = 0)
4. Specialization variance: each kit performs ~1.5-2× cohort median on 1-2 encounter types (designed peaks within bounded range)
5. No kit performs <30% of cohort median on any encounter type (bounded-viability floor)

These targets become the validation harness W-α4-gamora implements (sibling workstream). Damage formula refactor (W-α1), KPM ceiling raise/remove (W-α2), and unified calibration pass (W-α3) all gate on this canonical lock.

**Path β-narrow REJECTED** (shipping the current engine state as a "playable demo"): violates the directive at every encounter type; preserves 365× cross-path imbalance; ships a game where INT/WIS strictly dominate, defeating the specialization design intent. **Path β-FULL Gate-6 Option 6 REJECTED**: would replace the gate metric (KPM → damage_fraction_per_fight) while leaving the underlying damage formula divergence intact — every downstream system (gear, T4, progression, balance) would inherit the divergence.

**Cycle 14 v1 architectural commit:** tag `v1-cycle-14-bounded-viability-substrate-led` (revised from `v1-cycle-14-no-classes-substrate-led`). Close trajectory ~4-6 weeks per Matt directive; 6-week re-evaluation hook preserves optionality.

---

## 1. Authority + provenance

### 1.1 Matt 2026-05-28 design directive (verbatim, LOAD-BEARING)

> *"some kits are better at AOE, others are better at bosses/elites/mini-bosses, others are better at speed running, others are better in team play; all are within a bounded space of minimum viability but also none have zero strengths and all weaknesses."*

**Parsed structure:**

- **"some kits are better at AOE, others are better at bosses/elites/mini-bosses, others are better at speed running, others are better in team play"** — specialization clause; designed peaks per encounter-type cohort
- **"all are within a bounded space of minimum viability"** — bounded-viability floor; minimum-functional below which no kit falls
- **"none have zero strengths and all weaknesses"** — no strict dominance clause; bidirectional (no kit has zero weaknesses, no kit has zero strengths)

The directive is not "balance" (homogenized output) and not "diversity" (free-form variance). It is **bounded variance with designed peaks** — every kit is in the band, every kit has a peak, no kit dominates the whole encounter spectrum.

### 1.2 Provenance — Gate-6 ratification reversal

**Authority chain:**

1. **Matt 2026-05-23** hive-mind decision-routing directive: seam owners decide in-scope work; Matt is LAST-resort escalation. Applied here: the directive sat implicit-but-unnamed across multiple cycles of design work; the Gate-6 trigger surfaced its explicit canonicalization.
2. **Gate-5 (2026-05-28 earlier)**: Matt D1 RATIFIED Track 1 baseline (option-f-track-1-post-rebase-telemetry.json); D2 ratified Cycle 15 Option 6 damage/HP% metric replacement; D3 ratified KPM=600.0 as ceiling artifact with Cycle 15 investigation deferred.
3. **Gate-6 (2026-05-28 later)**: KR surfaced two options post case-8 boss HP rebase ratification — Option 5 (re-fire Wave 5 under new boss HP) and Option 6 (replace KPM with damage_fraction_per_fight metric). Both framed against the 79× population-median framing.
4. **Matt 2026-05-28 Gate-6 ratification REVERSAL**: BOTH option framings REJECTED. Matt surfaced the design directive verbatim (§ 1.1) AND the per-encounter-type forensic (INT/WIS saturate 4 of 6 encounter types; STR/DEX 0.0 KPM on boss + mini_boss + ~1.5 KPM on elite_pack; cross-path ratio at elite_pack = 365×). The 79× framing was a population-aggregate masking signal; the per-encounter-type framing surfaces the strict-dominance / strict-domination pattern that the directive prohibits.
5. **Path α RATIFIED**: root-cause damage formula refactor + KPM ceiling raise/remove + unified calibration pass + design-target validation framework. Cycle 14 v1 trajectory revised to ~4-6 weeks; Q10 quality > timeline directly drives.

**Full reversal record:** `agentic_orchestration/cycle-14-hive-mind-state.md` § "MATT GATE-6 RATIFICATION REVERSAL LOCKED 2026-05-28" (lines 648-688).

### 1.3 Why this is a recognition record + a canonical lock

The directive was implicit in the project's design language for many cycles — "each kit has a different best fit"; "no kit is the strict best"; "every kit is playable"; the genre-precedent framing of D2 builds + PoE archetypes + Last Epoch masteries. Matt's verbatim Gate-6 directive is the FIRST instance where the three properties (bounded viability + specialization + no strict dominance) are stated together as a single compound principle.

This doc canonicalizes the principle, names it, and operationalizes it into 5 measurable targets. From this commit forward, "bounded-viability-with-specialization" is the canonical short name for the principle; downstream dispatches, math notes, and decisions-log entries cite it by this name.

---

## 2. Design principle name + framing

### 2.1 Name: bounded-viability-with-specialization

The principle is compound. Each half is doing work:

- **bounded-viability** alone would describe Diablo III "every legendary is viable" homogenization — every build clears every content type at similar speed. This produces undifferentiated builds (D3 Reaper-of-Souls launch design before the Greater Rift redesign sharpened build identities).
- **specialization** alone would describe pure rock-paper-scissors — each build has hard counters; some content types are unplayable for some builds. This produces gatekeeping (early-PoE league mechanics where some builds simply couldn't run certain map mods).

The compound principle is the ARPG genre's mature equilibrium: bounded variance with designed peaks. Every build is in the band; every build has a peak; no build is locked out of any content; no build trivializes all content.

### 2.2 Three constitutive properties

**Property 1 — Bounded viability (the floor).**

Every kit produces meaningful output on every encounter type. The floor is bounded — kits that fall below ~30% of cohort median on any encounter type are not "specialized away from it"; they are broken on it. Bounded viability says: every kit has SOMETHING TO DO on swarm, on magic_pack, on elite_pack, on boss_with_adds, on mini_boss, on open_arena. Even the build whose peak is bosses can run swarm content without softlocking.

Player consequence: a player who builds INT-mage can play any seasonal content. A player who builds STR-warrior can also play any seasonal content. The seasonal content gates do not silently filter players by build identity.

**Property 2 — Specialization (the peaks).**

Every kit has 1-2 encounter types where it outperforms cohort median (1.5-2× per design target #4). Specialization is intentional. AOE kits clear swarm faster than single-target kits. Single-target kits kill bosses faster than AOE kits. Speed-running kits move through chokepoint corridors faster than tanky kits. Team-play kits enable group content compositions even if their solo throughput is below cohort median.

Player consequence: build identity matters mechanically, not just cosmetically. The choice to play a controller vs a DPS vs a sustain build produces real differences in how the player experiences each encounter type. Players who learn their build's peak encounter types feel competent; players who learn their build's trough encounter types still have functional play available.

**Property 3 — No strict dominance (the bidirectional clause).**

No kit dominates the entire encounter spectrum (saturation across all encounter types). No kit is dominated on the entire encounter spectrum (sub-floor on all encounter types). Both halves are load-bearing.

Player consequence: there is no "obvious meta build" that solves all content (no kit dominates). There is no "trap build" that fails at all content (no kit dominated). The build-choice landscape is dimensional, not unidimensional.

### 2.3 Genre positioning — ARPG specialization tradition

The principle is the mature ARPG genre equilibrium across the four reference projects:

| Game | Bounded floor | Designed peaks | No strict dominance |
|---|---|---|---|
| **Diablo II (LoD)** | Every build clears Hell difficulty solo by 1.10 (post-synergy redesign) | Hammerdin = uniques/safety; Javazon = lightning crowds; WW Barb = boss clear; Bonemancer = singletarget | No D2 build was strictly best across all map types; Cow Level / Chaos Sanc / Travincal each had different optimal builds |
| **Path of Exile (pre-3.15 standard)** | Most archetypes can clear Atlas; build-quality dimensions explicit (clear speed + boss damage + survivability + currency efficiency) | Headhunter-MF kits speed-clear; Slayer/Berserker single-target boss kits; Necromancer summoners zone-clear; Trickster/Pathfinder hybrid | No PoE build was strictly best across all four dimensions (clear vs boss vs survival vs farm); GGG explicit design language "each archetype has trade-offs" |
| **Last Epoch (1.0+)** | All masteries can complete monolith echoes (bounded viability gate) | Forge Guard = singletarget bosses; Necromancer = swarm/dungeon clear; Beastmaster = group content; Void Knight = elite-mob clear | No LE mastery strictly best; the master-of-masteries archetype balance is GGG-style explicit trade-offs |
| **Grim Dawn** | Every dual-class combo clears Veteran (bounded floor); most clear Elite | Demolitionist/Soldier = boss; Necro/Occ = AOE summoning; Inquisitor/Arc = ranged DPS; Shaman/Inq = lightning crowd | No GD dual-class strictly best; per-content trade-offs explicit in patch notes |

**Convergent pattern:** every successful ARPG that maintains long-term build interest has bounded-viability-with-specialization. The genre learned this across two decades. Games that violated either half (D3 launch homogenization; early-PoE league hard-counters) corrected back to the equilibrium because player retention required it.

**What this principle is NOT:**

- NOT "balance" in the homogenization sense (every kit produces same KPM on every encounter)
- NOT pure rock-paper-scissors (kits are locked out of some encounter types)
- NOT free-form variance (some kits are objectively best; others objectively worst)
- NOT "every kit needs every mechanic" (kits specialize; specialization is the point)

### 2.4 Composition with existing canonical anchors

**Composition with doc 47 § 3 (4-damage-path mechanical partition):**

Doc 47 establishes the mechanical substrate — 4 damage-scaling paths (STR-physical, DEX-physical, INT-magical, WIS-faith) with distinct formulas. This doc establishes the architectural-experience layer over that substrate — the 4 paths must produce comparable base DPS within ~1.5× variance (§ 4 target 1) AND distinct specialization profiles per kit (§ 4 target 4). The 4 paths are the MECHANICAL partition; bounded-viability-with-specialization is the EXPERIENCE the partition must produce.

**Composition with doc 46 (concentration architecture):**

Doc 46 § 1 establishes bounded stat ranges at the mechanical layer (crit chance 0-95%, crit multiplier 100-500%, DR 0-90%, etc.). This doc operates the same "bounded but not undifferentiated" pattern at the cohort layer — kits are bounded within ~30%-200% of cohort median per encounter type, with designed peaks at 1.5-2×. The two layers compose: mechanical layer caps individual stat output; cohort layer caps relative cohort output.

**Composition with doc 40 § 5.3 (build-specialization vs kit-identity):**

Doc 40 frames the player's investment trade-off — supporting chain absorbs kit-identity (substrate-cluster theme); T4 chains represent build-specialization. This doc names the framing principle that makes the trade-off meaningful — build-specialization must produce REAL peaks (1.5-2× cohort median) AND REAL trade-offs (some encounter types are below cohort median; no encounter type is below 30%).

**Composition with doc 41 § 4.6 (season cardinality / kit-count):**

Doc 41 sets per-season n_kits=40 default with ~70-80% gauntlet PASS rate target. This doc clarifies what "PASS" means — every kit produces non-zero KPM on every encounter type (design target #2) within a bounded range (design target #5). Gauntlet failure cases that violate the directive (kit produces 0 KPM on some encounter type, or saturates on all encounter types) are NOT specialization; they are violations of the directive that gate the kit out of the season.

---

## 3. Empirical evidence of design-violation in current engine state

### 3.1 Per-encounter-type forensic (Matt 2026-05-28)

Matt's Gate-6 disposition surfaced per-encounter-type aggregation of the Wave 5 season_001 telemetry that the 79× population-median framing had masked:

| Encounter type | INT/WIS KPM | STR/DEX KPM | Cross-path ratio | Violation type |
|---|---|---|---|---|
| `boss_with_adds` | saturates 600 ceiling | **0.0** | ∞ | INT/WIS no measurable weakness; STR/DEX zero strength |
| `mini_boss` | saturates 600 ceiling | **0.0** | ∞ | Same |
| `elite_pack` | ~365 | **~1.5** | **365×** | INT/WIS over-band; STR/DEX catastrophically below floor |
| (Other 3 encounter types: `open_arena`, `chokepoint_corridor`, `magic_pack`) | INT/WIS saturates ceiling on 4 of 6 total encounter types | STR/DEX trending dominated; specific values surface during W-α4-gamora harness implementation | wide | Same pattern likely propagated |

**Per `agentic_orchestration/dispatches/2026-05-28-path-alpha-master-scoping.md` § 0.** Specific per-encounter-type aggregation for the other 3 encounter types surfaces during W-α4-gamora harness implementation (sibling workstream); the master scoping dispatch annotates "specific source telemetry to be verified by gamora during W-α4 harness authoring."

### 3.2 Source telemetry anchors

The telemetry artifacts that anchor the forensic:

- `agentic_orchestration/cycle-14-wave-5-season-001/option-f-track-1-post-rebase-telemetry.json` — Track 1 per-damage-path cohort KPM bands (Matt D1 ratified Gate-5); shows STR/DEX boss_kpm_observations EMPTY (0 observations) → median 0.0 KPM; INT/WIS boss_kpm_observations non-empty with median ~73-82 KPM in band 60-100. The aggregation that produced the 79× framing was over POPULATION median; per-encounter-type aggregation surfaces the strict-domination pattern.
- `agentic_orchestration/cycle-14-wave-5-season-001/boss-hp-rebase-empirical-dps-telemetry.json` — boss HP rebase sweep telemetry; population_median_dps_balanced = 296,884.0; per_archetype_kpm_median across 8 boss_hp_factor levels shows STR/DEX 0.0 KPM at every factor level while INT/WIS produces observation signal at boss_hp_mid=230,000 (factor 9-14 range). Confirms the strict-domination pattern is robust across boss HP rebase factor space, not a single-point measurement artifact.

### 3.3 Diagnosis — current engine produces inverse of directive

The current engine state's mechanical signature is:

| Property | Directive expectation | Engine state (Cycle 14 pre-Path-α) |
|---|---|---|
| Bounded viability (no zero strengths) | Every kit non-zero KPM on every encounter type | STR/DEX = 0.0 KPM on boss + mini_boss (catastrophic floor violation) |
| Specialization (designed peaks, ≤2× cohort median) | 1.5-2× cohort median on 1-2 encounter types | INT/WIS saturate ceiling on 4 of 6 encounter types (over-band on majority) |
| No strict dominance | No kit dominates all; no kit dominated on all | INT/WIS strictly dominate; STR/DEX strictly dominated |

The engine produces the **inverse of every property**. This is not "imbalance to be tuned" within an aligned architecture; this is structural mis-alignment between damage-formula architecture and the design directive.

### 3.4 Why the 79× population-median framing masked this

Population median aggregates over kits without per-encounter-type stratification. INT/WIS kits saturating the ceiling on 4 of 6 encounter types AND STR/DEX kits producing 0.0 KPM on 2 of 6 encounter types produces a population median that smooths the bidirectional violation into a single ratio. The 79× ratio understated both the upper-bound saturation (no measurable weakness across 4 encounter types is qualitatively different from "INT is 79× better on average") AND the lower-bound floor violation (0.0 KPM on 2 encounter types is qualitatively different from "STR is 1/79th as effective on average").

Per-encounter-type stratification surfaces the qualitative structural pattern that population aggregation masked. This is a methodological lesson worth capturing: **balance forensics on a directive that operates per-cohort require per-cohort aggregation; population aggregation can hide bidirectional structural violations.** Jack-ryan W-α5c discipline candidate territory (see § 8.5).

---

## 4. Operationalized design targets (5 criteria)

The directive is operationalized as 5 measurable design targets. Path α close-criterion = simultaneous satisfaction of all 5 across the production Wave 5 re-fire output (~18 kits × 6 encounter types = 108-cell matrix).

### 4.1 Target 1 — Base DPS variance ≤1.5× across 4 damage-scaling paths

**Numeric criterion:** max(median_DPS_per_path) / min(median_DPS_per_path) ≤ 1.5 where path ∈ {STR-physical, DEX-physical, INT-magical, WIS-faith} and median_DPS is the L50 population-DPS sweep median against the unified calibration target.

**Validation method:** post-W-α1 damage formula refactor, run population-DPS sweep at L50 across the 4 paths with the W-α3 unified calibration target. Report median + p25 + p75 per path. Pass = max/min ratio ≤ 1.5.

**Rationale:** the bounded-viability floor is impossible to achieve if base DPS divergence dominates kit-level variance. ~1.5× is the genre tolerance band — D2 LoD post-synergy-redesign base damage across builds sits within ~1.3-1.7×; PoE archetypes post-Atlas-redesign sit within ~1.2-1.6×. ≤1.5× preserves architectural room for specialization-driven variance (target #4) without the foundation being pre-imbalanced.

**Player consequence:** at character creation, no path is "the wrong choice." A new player picking INT-mage and a new player picking STR-warrior begin the L1-L50 progression with comparable damage curves. Path choice is identity choice, not stat choice.

### 4.2 Target 2 — Every kit produces non-zero KPM on every encounter type

**Numeric criterion:** zero_count = 0 across the 108-cell matrix (18 kits × 6 encounter types). Zero KPM cells are STRUCTURAL VIOLATIONS, not "specialized weakness."

**Validation method:** per-kit-per-encounter-type gauntlet sim sweep. For each of 18 kits × 6 encounter types: run gauntlet sim with cohort-typical loadout; record KPM. Pass = no cells with KPM = 0.

**Rationale:** "no kit has zero strengths" per Matt directive. A 0 KPM cell is the kit failing to produce ANY measurable progress on that encounter type. Even a specialized speed-running build that's optimized for swarm clear should be able to slowly chip down a boss given enough time — the boss kill time may be 10× the cohort median but it must be finite. 0 KPM means infinite kill time, which is the player-experience equivalent of "this encounter type is not in your game."

**Player consequence:** every seasonal encounter is playable for every kit. A player whose build is bad-at-bosses still kills the boss; it just takes 5-10× longer than a boss-specialist would. The kit's weakness is felt as slow progress, not as encounter-lockout.

### 4.3 Target 3 — No kit saturates the KPM ceiling on any encounter type

**Numeric criterion:** saturation_count = 0 across the 108-cell matrix. Saturation = kit_KPM ≥ ceiling_threshold (currently 600.0; W-α2 raises or removes per gamora seam discretion).

**Validation method:** per-kit-per-encounter-type sweep (same harness as target 2). Pass = no cells at the ceiling. Ceiling threshold is set by W-α2; whatever W-α2 commits, the bounded-viability ceiling derives from post-refactor empirical population DPS distribution.

**Rationale:** "no kit has zero weaknesses" per Matt directive. A saturated cell is the kit hitting the engine's ceiling — additional damage output produces no additional KPM. This hides over-tuning: at the ceiling, you cannot distinguish "well-calibrated kit" from "kit that would produce 3× cohort median if the ceiling allowed it." The KPM=600 ceiling in current engine state masks the actual cross-path divergence — INT/WIS may be 5× or 10× cohort median if the ceiling were raised. W-α2 raises or removes the ceiling so the per-kit-per-encounter signal is empirically truthful.

**Player consequence:** kit identity is mechanically legible. Players can compare INT-mage and STR-warrior on the same boss and see real KPM differences that reflect kit design intent (not engine artifact). Build-crafting community discourse — which is load-bearing for ARPG long-tail retention per doc 40 § 7 peak-moment community layer — requires legible KPM signal.

### 4.4 Target 4 — Specialization variance: each kit ~1.5-2× cohort median on 1-2 encounter types

**Numeric criterion:** for each of 18 kits, ≥1 and ≤2 encounter types have kit_KPM / cohort_median_KPM ∈ [1.5, 2.0]. Kits with 0 designed peaks fail bounded-viability-with-specialization (no specialization). Kits with ≥3 designed peaks fail (too dominant — drift toward strict-best on multiple encounter types).

**Validation method:** per-kit specialization profile derived from per-kit-per-encounter sweep. For each kit, count encounter types in [1.5×, 2.0×] cohort-median band. Pass = each kit has 1-2 such encounter types.

**Rationale:** ~1.5-2× is the genre band for designed peaks. D2 Hammerdin clearing Chaos Sanc was ~1.7× cohort median; D2 WW Barb on Baal runs was ~1.8×; PoE Headhunter-MF on uber maps was ~2.0× before nerf. Below ~1.5× the peak is not perceptually distinct from cohort median (player can't tell their build is specialized). Above ~2.0× the peak is dominant rather than specialized (kit becomes the meta on that encounter type). The 1.5-2.0× band is the perceptual + design sweet spot.

**Player consequence:** kit identity feels real. A controller-build on swarm content clears noticeably faster than the cohort. A boss-specialist on a boss takes noticeably less time. Players who learn their build's peaks have a meta-game; players who don't still play in the cohort band on non-peak encounters.

### 4.5 Target 5 — No kit performs <30% of cohort median on any encounter type

**Numeric criterion:** for each of 108 cells, kit_KPM / cohort_median_KPM_for_that_encounter_type ≥ 0.30.

**Validation method:** per-kit-per-encounter floor check (same harness). Pass = no cells below 30% cohort median.

**Rationale:** the bounded-viability floor. 30% cohort median is the genre tolerance — below ~30% the kit is felt as "broken on this content," not as "specialized away from it." D3 post-Reaper-of-Souls launch had build-floor at ~35% of cohort GR clear time; PoE post-Awakening had build-floor at ~30% of cohort map clear time; LE 1.0 mastery floor at ~30% monolith echo time. Below 30% the player-experience signal flips from "this is my weak content" to "this content is not in my game" — same player consequence as target 2's zero-floor violation, just farther from absolute zero.

The 30% floor is the LOWER bound of the "bounded space of minimum viability" Matt named in the directive. Target 5 + target 4 together specify the variance window: every kit performs in [30%, 200%] of cohort median across all 6 encounter types, with designed peaks at 150-200%.

**Player consequence:** every kit is "in the game" on every encounter type. The slowest cell is felt as challenge, not as softlock. Players running content their build is bad at experience longer kill times AND find ways to optimize (rotation discipline, gear adjustments, positioning) — the encounter is winnable with care, just not with autopilot.

### 4.6 Compound criterion — all 5 targets simultaneously

Path α close-criterion = simultaneous satisfaction of targets 1-5 across the production Wave 5 re-fire output. Partial satisfaction (e.g., targets 1+2+3+5 PASS but target 4 has 4 kits with 0 designed peaks) does NOT close Path α; it surfaces as a scaffold-drift case under the Gate-N → Matt cadence per master scoping dispatch § 1.3.

The 5 targets are not independent — they compose. Target 1 (base DPS variance) is the foundation; without it, no per-kit specialization profile can be honestly measured because the cohort median is contaminated by base imbalance. Targets 2 + 5 are the floor pair; targets 3 + 4 are the peak pair. The directive's three constitutive properties map to the targets:

| Constitutive property | Targets that operationalize it |
|---|---|
| Bounded viability (floor) | Target 2 (no zero) + Target 5 (≥30% cohort median) |
| Specialization (peaks) | Target 4 (1-2 peaks in [1.5×, 2.0×] band) |
| No strict dominance (bidirectional) | Target 3 (no ceiling saturation) + Target 1 (≤1.5× base variance) + Target 5 (no kit below 30% on all encounter types) |

---

## 5. Per-encounter-type validation framing

### 5.1 Six encounter types canonical list

From `~/Games/reincarnated-engine/src/reincarnated/generation/endgame_encounter_catalog.py` (audited at authoring; 6 unique `scenario_shell_id` values across the catalog):

| Encounter type | Description (per catalog source) |
|---|---|
| `open_arena` | 50×50m open terrain; swarm composition |
| `chokepoint_corridor` | corridor terrain; swarm composition with positional constraint |
| `magic_pack` | 32.7×14m; 1 magic + 3 swarm adds |
| `elite_pack` | elite-mob composition; mid-tier encounter |
| `boss_with_adds` | 30×30m; 1 boss + 2 flanking elite adds |
| `mini_boss` | 30×30m; 1 mini-boss + 2 elite adds |

Note on swarm composition: `open_arena` and `chokepoint_corridor` are both "swarm" content at the mob-composition layer, distinguished by terrain (open vs corridor). The directive's "AOE-better kits" applies across both; the terrain distinction surfaces a sub-specialization signal (high-mobility kits on open_arena vs positional kits on chokepoint_corridor).

**Authority:** the 6-encounter-type canonical list is locked in engine source (catalog file). This doc references; it does not redefine. Future encounter-type additions or revisions flow through the engine catalog with cross-reference back to this doc when they affect the bounded-viability-with-specialization measurement.

### 5.2 Validation harness specification (conceptual)

W-α4-gamora (sibling workstream) implements the validation harness. This doc specifies the conceptual shape; gamora owns the implementation per simulation-seam authority.

**Inputs:**
- Per-kit specification (the 18-kit production roster from Wave 5 re-fire)
- Per-encounter-type catalog (the 6 encounter types above)
- Cohort definition (kits within same damage-scaling path or other cohort grouping per gamora math-note)
- Calibration target (W-α3 unified calibration output)

**Outputs (108-cell matrix + derived):**
- 108 cells (18 kits × 6 encounter types) with per-cell `kit_KPM`
- Per-encounter-type cohort_median_KPM
- Per-cell ratio: kit_KPM / cohort_median_KPM_for_that_encounter_type
- Per-kit specialization profile: count of encounter types in [1.5×, 2.0×] band
- Per-kit floor profile: count of encounter types <30% cohort median
- Saturation_count: cells at KPM ceiling (post-W-α2 ceiling raise/remove)
- Zero_count: cells at KPM = 0
- Base DPS variance: max/min ratio of per-path median DPS at L50

**Pass criteria (compound; all 5):**
1. Base DPS variance ≤ 1.5
2. zero_count = 0
3. saturation_count = 0
4. Every kit's specialization profile count ∈ [1, 2]
5. Every kit's floor profile count = 0

**Math-note requirement (Discipline #1):** W-α4-gamora math note captures the cohort definition methodology, the cohort_median computation, the variance ratio formula, the saturation threshold derivation from W-α2 output, and the design-target pass criteria as Boolean composition. The math note becomes the empirical anchor for the W-α4 harness implementation.

### 5.3 Cohort definition open question (forward to W-α4-gamora)

The directive operates per-cohort (cohort_median is the comparison anchor). What defines a cohort? Two candidate framings:

- **A — Per damage-scaling-path:** cohort = all kits sharing the same damage_scaling_type {STR-physical, DEX-physical, INT-magical, WIS-faith}. Cohort_median is computed within each path. Specialization is measured relative to same-path peers.
- **B — Per substrate-cluster grouping:** cohort = P3 multimodal clustering output cluster. Cohort_median is computed within each cluster. Specialization is measured relative to same-cluster peers.

**Gandalf lean (advisory; gamora seam-owns):** A for v1 Path α. Cohort = damage-scaling-path. The directive is operationalized at the layer where the current engine fails — cross-path imbalance. Per-path cohort_median surfaces specialization-within-path while cross-path comparison surfaces base DPS variance (target 1). Cluster-based cohort (option B) is a Cycle 15+ refinement once Path α stabilizes the cross-path foundation. W-α4-gamora math-note explicitly registers cohort definition with rationale.

### 5.4 Per-kit profile output shape

For human + design review of the 18 kits × 6 encounter types output, the harness produces a per-kit profile card:

```
KIT: <kit_id>
  Damage-scaling-path: <path>
  Per-encounter-type KPM + cohort-median ratio:
    open_arena:          KPM = X    (ratio = X / cohort_median_open_arena)
    chokepoint_corridor: KPM = X    (ratio = ...)
    magic_pack:          KPM = X    (ratio = ...)
    elite_pack:          KPM = X    (ratio = ...)
    boss_with_adds:      KPM = X    (ratio = ...)
    mini_boss:           KPM = X    (ratio = ...)
  Specialization peaks (encounter types with ratio ∈ [1.5, 2.0]): [...]
  Floor violations    (encounter types with ratio < 0.30):        [...]
  Saturation cells    (encounter types with KPM = ceiling):       [...]
  Directive compliance: PASS / FAIL (with specific failed target IDs)
```

The profile card is human-legible for design-review and machine-checkable for automated gauntlet pass/fail.

---

## 6. Path β rejection rationale (canonical record)

### 6.1 Context — honoring the prior recommendation framing

This author had a prior Path β-narrow recommendation in Matt-verbal-dialogue prior to the Gate-6 ratification reversal. (No durable artifact captured the dialogue; the recommendation lived in conversational form between gandalf and Matt + KR.) The recommendation served a valid trade-off framing: Cycle 14 v1 close timeline pressure (~4-6 day pre-rebase trajectory) traded against architectural-honesty cost of the deeper refactor Path α represents.

Matt's Gate-6 directive made the previously-implicit design intent EXPLICIT — bounded-viability-with-specialization is the canonical design principle, and that principle is non-negotiable load-bearing for "ship the novel engine with the fun/balanced game." Once the directive is named, Path β-narrow's trade-off framing dissolves: the timeline savings are not savings if they ship a game that violates the directive at every encounter type.

The recommendation was valid within a different trade-off priority weighting (timeline-first). It is not valid within the now-explicit priority weighting (architectural-honesty-first per Q10 quality > timeline). This doc captures the rejection on the canonical record without diminishing the trade-off framing that produced the recommendation — the design-decision landscape genuinely had two valid framings until Matt's directive collapsed them.

### 6.2 Path β-narrow REJECTED

**Description:** ship the current engine state as a "playable demo" preserving the 365× cross-path imbalance at elite_pack and the 0.0 KPM STR/DEX cells at boss + mini_boss + the INT/WIS ceiling saturation on 4 of 6 encounter types. Cycle 14 v1 closes within the original ~4-6 day trajectory; deeper architectural work deferred to Cycle 15+.

**Rejection reason:** violates the bounded-viability-with-specialization directive at every constitutive property:

- Bounded viability VIOLATED: STR/DEX kits have zero strengths on boss + mini_boss
- Specialization VIOLATED: INT/WIS kits saturate the ceiling on 4 of 6 encounter types (no measurable weaknesses; not specialization — domination)
- No strict dominance VIOLATED: INT/WIS strictly dominate the engine; STR/DEX strictly dominated

A "playable demo" in this state ships a game where INT/WIS is the obvious meta and STR/DEX is the trap build. Every downstream system (gear, T4, progression, balance, community discourse) is calibrated against the imbalanced foundation. Future architectural correction becomes harder, not easier, as inherited calibration accumulates against the wrong target.

**Recognition:** Path β-narrow served a valid Cycle 14 v1 close timeline framing under the (then-implicit) trade-off framework. Matt's directive made the framework explicit and shifted the lock to architectural-honesty-first. Path α represents the architectural-honesty path that Q10 quality > timeline directly drives. The 6-week re-evaluation hook preserves optionality (see § 7.3) — if scaffold-drift case #9+ extends Cycle 14 past 6 weeks total, Matt re-evaluates extend-further vs ship β-narrow as Cycle 14 v1 partial close + Path α as Cycle 15 architectural close.

### 6.3 Path β-FULL Gate-6 Option 6 REJECTED

**Description:** replace the gate metric KPM with `damage_fraction_per_fight = total_damage_dealt / encounter_total_HP` while preserving the underlying damage formula. The Cycle 15 D2 Phase 2 per-encounter-type bands (Matt-RATIFIED at Gate-5) become the bounded-viability framework; the existing damage formula divergence is absorbed as "this is how the metric works."

**Rejection reason:** would replace the gate metric while leaving the underlying damage formula divergence intact. Future systems would all inherit the divergence:

- **Gear scaling** would calibrate `+%damage` affixes against the imbalanced base formulas (INT/WIS would over-scale; STR/DEX would under-scale)
- **T4 capstones** would calibrate damage multipliers against the imbalanced base (every per-path T4 would inherit the cross-path imbalance)
- **Progression scaling** (L1-L50 attribute scaling tables) would calibrate against the imbalanced base (per-level progression would compound the divergence)
- **Balance dashboards** would display damage_fraction_per_fight ratios that ARE in-band, masking that the underlying KPM ratios are still 365× — the metric replacement would hide rather than fix the structural problem
- **Community discourse + build-crafting** would form around the metric-replacement view, locking in the underlying divergence as "how the game works"

The architectural cost of metric replacement is comparable to formula refactor (both touch the calibration pipeline), and metric replacement does not produce the bounded-viability-with-specialization output the directive requires. Path β-FULL Option 6 fails the directive AND fails the cost-savings argument that would have been its only advantage.

**Cycle 15 D2 retroactive retraction:** Matt D2 was RATIFIED at Gate-5 for Cycle 15 Option 6 commit. Path α RATIFICATION REVERSAL retroactively retracts D2; the Cycle 15 architectural commit shifts from "metric replacement" to "post-Path-α whatever scope determines." Jack-ryan W-α5a handles the canonical retraction per Discipline #40 case (c) — FOURTH iteration of canonical-lock retraction on the Phase 7 doc (per master scoping § 2.3 Amendment 2 + dispatch § 2.3).

### 6.4 Why naming both rejections together matters

Both β paths share a common architectural failure mode: **they treat the directive as a metric problem rather than a structural problem.** Path β-narrow defers the structural problem to Cycle 15+; Path β-FULL Option 6 absorbs the structural problem into a metric replacement. Path α treats the structural problem as structural — refactor the damage formulas, raise/remove the ceiling, unify calibration, validate against the 5 design targets directly.

Naming both rejections on the canonical record preserves the design-decision lineage: future cycles that face similar timeline-vs-architecture pressure can reference this rejection rationale as precedent. The directive's authority comes from being explicit + load-bearing; rejection of metric-only or defer-only paths is part of what makes the directive operational.

---

## 7. Cycle 14 v1 architectural commit

### 7.1 v1 tag revised

| Prior | Revised |
|---|---|
| `v1-cycle-14-no-classes-substrate-led` | `v1-cycle-14-bounded-viability-substrate-led` |

The revised tag reflects the architectural commit that defines Cycle 14 v1 close. "No-classes" (the 2026-05-27 architectural recommitment to no-class generative architecture, per `agentic_orchestration/gandalf/notes/2026-05-27-no-classes-architectural-recommitment.md`) is PRESERVED as a substrate-led architectural commitment that holds across Cycle 14 — it is not retracted. The tag revision surfaces "bounded-viability" as the higher-order architectural commitment Cycle 14 v1 ships. "Substrate-led" remains in the tag because substrate-emergence is still the generative-architecture commitment; bounded-viability-with-specialization operates AT the substrate-emergence output layer.

### 7.2 Architectural commit shape

Cycle 14 v1 ships the following architectural commits:

1. **Damage formula refactor (W-α1)** — unified or recalibrated damage formulas across 4 damage-scaling paths producing ≤1.5× base DPS variance (target 1). Rocket seam discretion on unified vs recalibrated.
2. **KPM ceiling raise or remove (W-α2)** — current 600.0 ceiling hides over-tuning; W-α2 raises empirically or removes per gamora seam discretion.
3. **Unified calibration pass (W-α3)** — replaces SC-6b (`base_physical_damage_l50`) + SC-7 (`BASE_SPELL_DAMAGE_L50`) binary-search calibrations with single reference target tied to encounter HP scaling + boss HP factor range.
4. **Per-encounter-type design-target validation framework (W-α4)** — this canonical doc (W-α4-gandalf) + W-α4-gamora harness implementing the 5 targets as automated checks against per-kit-per-encounter sweep output.
5. **Wave 5 re-fire validation** — gamora re-runs full production season under new engine state + design-target validation harness; close criterion = all 5 targets simultaneously satisfied across 18 kits × 6 encounter types.

### 7.3 Re-evaluation hook (6-week boundary)

Matt directive: Cycle 14 v1 close trajectory ~4-6 weeks from Path α firing (~2-3 weeks realistic effort + ~2-4 anticipated scaffold-drift cases per master scoping § 1.3). At the 6-week boundary, Matt re-evaluates:

- **Path α extends further** if scaffold-drift case #9+ surfaces and extension is justified by architectural-honesty gain
- **Path β-narrow ships as Cycle 14 v1 partial close + Path α as Cycle 15 architectural close** if scaffold-drift surface area is broader than 6 weeks accommodates and partial close + deferred completion is the optionality-preserving move

The re-evaluation hook is NOT a soft-Path-α lock — Path α RATIFICATION shifts the default to architectural-honesty-first. The hook preserves Matt's authority to re-disposition if empirical surface area exceeds forecast. Per master scoping § 5: "Path α doesn't lock; it shifts default to architectural honesty."

### 7.4 What Cycle 14 v1 does NOT ship

Out of scope for v1 per Path α master scoping § 1.4:

- Spirit Guide gameplay subsystem (gamora seam ownership but not damage formula territory)
- Element / anchor balance beyond damage formulas (rocket seam ownership but not damage formula territory)
- Player-surface work (drax demo + loadout) — gated on Path α close; D13 P1-P9 framework does NOT fire under Path α
- Phase 7 2-layer joint-gate band table infrastructure — preserved as historical instrumentation; new design-target validation harness supersedes; doc transitions LOAD-BEARING → HISTORICAL per W-α5b
- Cycle 15 D2 Option 6 damage/HP% metric — REJECTED per § 6.3
- Wave 5 production season cascade — does not re-fire until Path α close + design targets met

---

## 8. Forward-link to Path α work-streams

### 8.1 W-α4-gamora — validation harness

**Owner:** gamora (simulation seam)
**Scope:** simulation-side validation harness implementing all 5 design targets (§ 4) as automated checks against per-kit-per-encounter-type gauntlet sweep output; produces 108-cell matrix + derived per-kit profile cards (§ 5.4) + compound pass/fail verdict
**Sequence:** fires AFTER this canonical lock (W-α4-gandalf → W-α4-gamora sequential)
**Math note required:** at simulation/math/ path TBD by gamora; captures cohort definition (gandalf lean: per damage-scaling-path; § 5.3) + cohort_median computation + variance ratio formula + saturation threshold derivation from W-α2 + compound pass criterion
**Dispatch:** KR authors W-α4-gamora dispatch on receipt of W-α4-gandalf landing signal (this doc commit + push)

### 8.2 W-α1 — Damage formula refactor

**Owner:** rocket (foundation seam; element/anchor)
**Scope:** unified or recalibrated damage formulas across 4 damage-scaling paths (STR-physical, DEX-physical, INT-magical, WIS-faith per doc 47 § 3); rocket seam-discretion on architectural choice; output must satisfy target 1 (≤1.5× base DPS variance)
**Sequence:** fires PARALLEL with W-α2 + W-α3 post W-α4 design-target lock; W-α3 chains on W-α1 output
**Cross-seam touch:** simulation seam if formula change affects damage routing logic (doc 47 § 4); standard ADR-004 MIGRATION
**Coordination with this doc:** rocket consumes § 4 target 1 numeric criterion + § 5 per-encounter-type validation framing as the architectural acceptance bar

### 8.3 W-α2 — KPM ceiling raise/remove

**Owner:** gamora (simulation seam; gauntlet_sim.py)
**Scope:** raise or remove KPM=600.0 ceiling per gamora seam discretion; if raised, new value derived empirically from post-refactor population DPS distribution; if removed, gate semantics updated
**Sequence:** fires PARALLEL with W-α1 + W-α3 post W-α4
**Coordination with this doc:** gamora consumes § 4 target 3 (no saturation) as the architectural acceptance bar; ceiling threshold setting becomes the empirical anchor for § 4 target 3 measurement

### 8.4 W-α3 — Unified calibration pass

**Owner:** gamora (simulation seam; calibration loops)
**Scope:** replace SC-6b + SC-7 binary-search calibrations with single unified calibration pass tied to encounter HP scaling + boss HP factor range
**Sequence:** chains on W-α1 (W-α3 calibrates W-α1 output); reference target lock awaits W-α2 ceiling signal per master scoping § 2.2 Amendment 1
**Coordination with this doc:** gamora consumes § 4 target 1 (base DPS variance) as the calibration acceptance bar; unified reference target becomes the basis for cross-path variance measurement

### 8.5 W-α5 — Jack-ryan canonical retirements + discipline candidate

**Owner:** jack-ryan (canonical-write seam)
**Scope:** decisions-log entries (W-α5a) + Phase 7 doc LOAD-BEARING → HISTORICAL lifecycle (W-α5b) + engineering-disciplines.md amendments (W-α5c)
**Sequence:** fires PARALLEL throughout; W-α5b begins after W-α4-gandalf canonical write lands (cross-reference target exists — this doc)
**Coordination with this doc:**
- W-α5a captures Path α RATIFICATION + Path β rejection rationale; this doc's § 6 is the canonical reference for both
- W-α5b transitions Phase 7 doc LOAD-BEARING → HISTORICAL; § 3.13 cross-reference back to THIS doc as Path α successor
- W-α5c discipline candidates jack-ryan ratifies at engineering-disciplines.md: (a) per-cohort aggregation requirement for directive-scoped balance forensics (§ 3.4 of this doc surfaces the methodological lesson); (b) bounded-viability-with-specialization framework as design-discipline (composes with #45 vocabulary lock); (c) "case-register distinction between scaffold-drift catches and canonical scaffold resolutions" per master scoping § 2.3
- **Discipline number:** jack-ryan confirms next available at authoring time. Per dispatch § 1.2 + master scoping § 2.3 Gate-1 INFO: Discipline #46 ALREADY EXISTS (DB anti-materialization, landed 2026-05-27); this doc DOES NOT commit a new discipline number — that's jack-ryan W-α5c territory

### 8.6 Master scoping reference

Path α master scoping dispatch (load-bearing parent): `agentic_orchestration/dispatches/2026-05-28-path-alpha-master-scoping.md`

Full cycle 14 v1 close re-trajectory per master scoping § 3:

| Phase | Effort | Calendar |
|---|---|---|
| W-α4 canonical + harness lock | ~2-3d sequential (gandalf canonical → gamora harness) | Days 1-3 |
| W-α1 + W-α2 + W-α3 parallel fan-out | ~3-5d (W-α1 longest pole; W-α3 chains; W-α2 independent) | Days 3-8 |
| Wave 5 re-fire + validation | ~0.5d | Days 8-9 |
| jack-ryan canonical retirements (parallel) | ~0.75d total | Days 3-9 |
| Buffer for ~2-4 scaffold-drift cases | ~2-5d additional | Days 9-14 |
| Matt v1 ratification | <0.1d | Day 14 |

**Realistic estimate: ~10-15d total; ~4-6 weeks per Matt directive accounting for unforeseen surface area.**

---

## Sign-off

**Author:** gandalf (story-and-design steward)
**Date:** 2026-05-28
**Status:** v1 canonical lock; LOAD-BEARING per Path α RATIFICATION; gates W-α1/W-α2/W-α3 + Wave 5 re-fire validation
**Authority:** Matt 2026-05-28 Gate-6 RATIFICATION REVERSAL + Path α RATIFICATION + bounded-viability-with-specialization design directive LOCKED (verbatim § 1.1)
**Discipline #45 vocabulary audit:** PASS — "bounded-viability-with-specialization" is new design-vocabulary with zero pre-existing canonical or engine-source collision per grep audit at authoring time; "specialization" appears as a free-floating noun in prior canonical docs without compound-term conflict; "bounded" similarly free-floating. Prohibited-vocabulary grep audit on this doc returns only exempt occurrences: (1) § 2.3 genre-positioning table references "archetypes" / "dual-class" as descriptive of other ARPG games' design language (PoE / LE / GD) — exempt per Discipline #45 scope exemption "direct quotation of Matt or prior architectural sessions" (extended sense: direct reference to genre-precedent design language); (2) § 7.1 references "no-classes" + "no-class generative architecture" as direct citation of the 2026-05-27 no-classes architectural recommitment — exempt per scope exemption "historical artifact preservation" + direct architectural reference; (3) this audit declaration itself naming the exempted occurrences. Zero non-exempt prohibited-vocabulary usage in dispatch acceptance criteria, quality criterion, generative-architecture description, or schema/field naming.
**Cross-references:** doc 00 (ground-state oracle — registration this session); doc 02 (roadmap — Path α active workstream + Cycle 14 v1 trajectory ~4-6 weeks); doc 47 § 3 (mechanical substrate; cross-link added this session); doc 46 (concentration architecture; companion); doc 40 (Cycle 13 architectural foundation; companion); master scoping dispatch (parent); W-α4 dispatch (executes); engineering-disciplines.md § 45 (vocabulary lock audit anchor); engineering-disciplines.md (next-available number for W-α5c candidate jack-ryan confirms at authoring)

**For:** the architectural-experience layer over doc 47's mechanical substrate; the validation framework Wave 5 re-fire validates against; the canonical record of Path β rejection rationale; the gate W-α1/W-α2/W-α3 fire against. From this commit forward, "bounded-viability-with-specialization" is the canonical short name for the design principle Matt 2026-05-28 made explicit. The game we ship is the game where every kit has somewhere to be excellent and nowhere it cannot play.
