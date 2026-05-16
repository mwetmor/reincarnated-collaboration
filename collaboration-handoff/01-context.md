# Context — What Was Built and Discovered

## Yesterday's accomplishments (May 7-8, 2026, sessions 1-5)

Five engine sessions completed, all merged to `mwetmor/reincarnated-engine` main branch (except session 5 which is on `work/priority-01-physical-warrior` branch awaiting decision):

**Session 1 — Telemetry foundation.** Schema applied with migration 1.0 (9 foundation tables: schema_meta, generation_runs, generation_steps, seasons, classes, abilities, monsters, trials, gear). TelemetryRecorder class with NullRecorder pattern for telemetry-disabled paths. CLI gains `--telemetry-db PATH` flag. SeasonOrchestrator wraps its 8 pipeline steps with `recorder.step()` context manager. Commit `3a9e41b`.

**Session 2 — LLM call tracking.** Migration 1.1 adds `llm_calls` table. TrackedLLMClient wrapper around the engine's LLM client. Naming pipeline routes through tracked client. Cost and token capture working per call with purpose enumeration (skill_naming, class_naming, monster_naming, trial_naming, etc.). Commit `aaec860`.

**Session 3 — Anchor system.** 130-entry place anchor library converted from markdown to library.json. Deterministic-by-seed selection with category balance and library exhaustion handling. History stored in seasons table (anchor_id, anchor_name, anchor_category columns) — no parallel JSON history file. Anchor flows into naming prompts. Two-season smoke test confirmed different anchors selected (The Smoke-Spire and Hyperborea) with no cross-season repetition. Commit `fc6f857`.

**Session 4 — Seasonal element system.** Migration 1.2 adds seasonal_elements and element_proposals tables. 147-entry element pool (after compound cleanup — see below). LLM-driven selection with 5-rule validation, 2 retries, deterministic seed fallback. Auto-accept proposals mutate pool.json. Manifest version bumped to 1.2. Class/skill/monster naming receives seasonal element context. Commit `7bca49f`.

**Element pool cleanup (separate commit).** Initial pool.json had 156 entries including 13 hyphenated compound entries that violated the agreed single-word rule (compounds reserved for ability names, not element names). User edited element-pool.md to remove compounds; pool.json regenerated to 147 entries.

**Session 5 — Physical warrior bug fix (in progress).** Diagnosed two root causes of physical warrior structural underperformance: flat armor formula creates threshold effects (52-84% absorption of primary attacks at standard modifier), and physical warriors had zero elemental resistance against the all-elemental gauntlet. Implemented fix: percentage armor formula with K=3000, plus stub elemental resistance gear for physical archetypes (9% per element). Fix verified working on seed 42 — all 11 classes converged, both warriors hit targets. Commit on work branch but **not merged** — see "Major finding" below.

## Major finding from session 5: monster mana economy bug

Investigation of warrior over-performance at seeds 200 and 300 (88% and 86% respectively, vs 50% target) revealed a pre-existing systemic bug:

**Mechanism:** Monster generation samples cooldowns and mana costs independently from the mana pool. Some combinations produce monsters that exhaust their mana within 1.7 seconds, then can only fire one ability every 2+ seconds for the rest of the fight (effectively self-disarmed).

**Concrete example:** Seed 200's brute had cooldown 0.2s and mana cost 13%. Mana pool ~125, regen ~7.5/s. Burn rate 83/s. Sustainable for 1.7 seconds. After that, fires roughly once every 2.2 seconds.

**Failure rate:** 5 of 8 test seeds (62%) showed convergence failures. Affected both physical warriors (newly exposed by armor formula fix) and fire mages (previously plateauing at ~57% — likely the same bug, hidden behind the scaling plateau).

**Why it was hidden before:** Pre-fix, physical warriors couldn't deal damage at low modifiers (armor floor reduced primary attacks to zero). Fights timed out and monsters "won" — the mana-starved monsters appeared functional because the warriors were equally hobbled. The armor formula fix unmasked the issue by giving warriors actual damage output at low modifiers.

**Implication:** This is a balance verification problem, not a class-specific bug. Any class converging "correctly" against gauntlets that include self-disarming monsters has unreliable balance modifiers. Class quality measurement (Cluster 2 work) would be measuring against intermittently-broken opposition.

## Architectural discussion that emerged

Late-night conversation surfaced design questions that go beyond fixing the immediate bug:

**Resource systems for physical archetypes.** The engine likely has physical archetypes (warriors, rogues, archers) with no resource constraint — only cooldowns. This is mechanically thinner than mana-using elemental classes and may contribute to balance asymmetries. Three options surfaced: unified mana model (D2-style), differentiated resources per archetype (rage/combo/focus/mana), or cooldown-only physical (current state — limited).

**Dimensional class generation.** Insight that energy type, range profile, armor weight, and damage type could be primary generation dimensions, with archetype labels emerging from combinations rather than being predefined. This proposal extends naturally to monsters and might address the mana economy bug architecturally — monsters that don't need mana wouldn't be assigned mana at all.

**Body-swap implications.** The body-swap mechanic benefits significantly from differentiated mechanical identity. Players experiencing many classes briefly need each to feel distinct. Resource system differentiation is one of the most immediate ways to communicate "you're a different combatant now."

## What this means

Yesterday's work landed substantial value (variety system, telemetry, anchor/element rotation) but also surfaced findings that affect what comes next:

1. The monster mana economy bug must be addressed before further class balance verification produces meaningful data
2. Resource systems for physical archetypes deserve deliberate design rather than autopilot defaults
3. The dimensional generation insight, if pursued, affects multiple priorities and is bigger than a bug fix

These insights came at the end of a long working day. They deserve fresh consideration rather than rushed action. This folder's purpose is to support that deliberate consideration.

## Outstanding state

**Branches:**
- `main`: clean, sessions 1-4 merged
- `work/priority-01-physical-warrior`: session 5 work committed, not merged, awaiting decision

**Open priorities:**
- Priority 11 (suggested): Monster mana economy fix — could be tactical or architectural
- Priority 12 (suggested): Class resource systems — design decision required
- Priority 02 (gear): blocked on resource architecture decision
- Fire mage Issue B (Priority 01): likely subsumed by monster mana fix

**Outstanding documentation:**
- Substantial drift accumulated across sessions 1-5 (see 02-doc-maintenance-required.md)
- Yesterday's findings not yet captured in design repo
- Decisions log empty for yesterday's architectural decisions

**Outstanding decisions:**
- Whether to merge `work/priority-01-physical-warrior` as-is or hold pending broader fix
- Three options for resource architecture (see 04-decision-options.md)
- Whether to pursue dimensional generation refactor or defer to Phase 1
