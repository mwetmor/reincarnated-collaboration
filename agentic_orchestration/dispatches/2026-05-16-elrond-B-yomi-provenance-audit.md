# Dispatch — elrond B: Yomi (season_002328) provenance audit

**Status:** COMPLETE — 2026-05-16 (Completion section below)
**Target:** elrond
**Branch:** main (all repos for read-only investigation; output in collaboration repo)
**Tag intent:** No tags — investigative deliverable is a markdown audit report.

## Context

Per your own data-architecture audit (2026-05-16):

> *"`season_002328` (Yomi) is in loadout but NOT in `engine/seasons/`, NOT in `engine/exports/`, NOT in telemetry. Star-lord's gear_pool re-export ran against telemetry, so the data must be there — let me check… actually it's not in the seasons list above. Yomi must be in a separate telemetry pass or has been generated against a different telemetry instance. **This is a real provenance gap** — the canonical Yomi data lives only in the loadout repo. If the loadout repo is lost, Yomi is lost."*

This is a **single point of failure on data we've been actively building against**:
- Drax v0.5 / v0.5.1 / v0.5.2 used Yomi as the working season
- Star-lord's 2026-05-15 gear-pool-stats work re-exported Yomi-specific gear_pool.json (the seed + 999 deterministic-replay approach implies the source data exists somewhere)
- Gandalf's design work has referenced Yomi as illustrative (the Pomegranate / Izanami Passage example)
- The loadout repo has no `origin` remote (per `skill_handoff_2026-05-15.md` § drax) — so it's truly single-machine

Matt assigned this 2026-05-16 as Elrond task B, sequenced after task A.

## Work

Investigate Yomi's data provenance across all four repos. Specifically:

1. **Engine repo investigation:**
   - `git log --all --grep="002328\|yomi\|Yomi"` across `reincarnated-engine/` — find any commits referencing Yomi
   - Search engine code for any references to `002328` or `yomi`
   - Check `engine/seasons/`, `engine/exports/`, telemetry.db classes table — confirm absence per the audit
   - Check `engine/data/` for any orphan Yomi-related files (e.g., a separate telemetry instance, a backup file)
   - Look for star-lord's gear-pool-stats work — his commit `c1f02ca` should have a `_regen_gear_stats` path; trace what input data it consumed and where THAT lives

2. **Loadout repo investigation:**
   - `git log --all` looking for the original Yomi import commit — when did Yomi first appear in loadout/data/?
   - Inspect `loadout/data/season_002328/` content — what shape is it (engine internal vs export shape)? What's the timestamp on the files?
   - Any provenance metadata in the files themselves (generation timestamps, seed values)?

3. **Other repos:**
   - Check `reincarnated-demo/` for any Yomi references (demo uses 001001-001005 per audit; Yomi shouldn't be there but verify)
   - Check `reincarnated-collaboration/canonical/` and `agentic_orchestration/` for any references that might point at Yomi's origin

4. **Reconstruct the most plausible provenance chain:**
   - Where was Yomi generated (which machine / which engine instance / which seed value)?
   - When was it generated?
   - What's the canonical seed if known (the gear re-export uses `seed + 999 = 3327` — so seed = 2328 likely)?
   - If gear is deterministically reproducible from `seed=2328` against the engine, is the rest of Yomi (classes, monsters, manifests) also reproducible?

5. **File findings at** `agentic_orchestration/research/curated/yomi-provenance-audit-2026-05-16.md`:
   - Full provenance reconstruction
   - Confirmation of the single-point-of-failure status
   - **Remediation recommendations** ranked by effort/value:
     - **(option 1)** Regenerate Yomi from canonical seed against engine → if data shape matches loadout's current files, we have a reproducible canonical
     - **(option 2)** Establish loadout repo origin remote + push (Matt-action, not your work)
     - **(option 3)** Archive loadout/data/season_002328/ to a backup location (in-repo or external)
     - **(option 4)** Accept the gap; document and move on (least preferred)
   - Sequencing recommendation

## Constraints

- **Read-only across all four repos.** Do NOT modify any files; this is investigative.
- **Time-bound target:** 1-2 hours. Investigation + report.
- **No regeneration attempted in this dispatch.** Your job is to FIND the provenance, not to regenerate. Regeneration (if recommended) becomes a separate star-lord/rocket dispatch.

## Out of scope

- Actually regenerating Yomi (separate dispatch if recommended)
- Setting up loadout repo origin remote (Matt-action)
- Modifying any season data

## Acceptance

- Audit report filed at the path above
- Provenance chain documented (where Yomi was generated; when; by what process; reproducibility status)
- Single-point-of-failure status confirmed or refuted
- Remediation options ranked with effort/value
- Knight-rider notified at completion with: report path; recommended next action (option 1 / 2 / 3 / 4 + sequencing)

## Required reading

- Your own audit's Yomi gap section in `data-architecture-audit-2026-05-16.md`
- Star-lord's gear-pool-stats dispatch + completion record at `dispatches/2026-05-14-star-lord-gear-pool-stats.md`
- Star-lord's `MIGRATION.md` at `reincarnated-engine/src/reincarnated/export/MIGRATION.md` (mentions the deterministic-replay approach)

## Completion — elrond, 2026-05-16

### Deliverable

`agentic_orchestration/research/curated/yomi-provenance-audit-2026-05-16.md` — 8 sections including executive verdict, full timeline, comprehensive cross-repo inventory, SPOF assessment, reproducibility-from-seed analysis, four ranked remediation options, sequencing recommendation, documentation follow-ons.

### Headline findings

1. **SPOF CONFIRMED, severity high.** Yomi (season_002328) exists only in `reincarnated-loadout/data/season_002328/` (556 KB total: 10 class JSONs + manifest + gear_pool.json). Loadout has no origin remote — 25 local commits, never pushed. Three-deep redundancy (working tree + local git + remote) reduces here to two-deep.

2. **Audit § 3.6 hypothesis refined.** The audit guessed "Yomi must be in a separate telemetry pass." Reality: Yomi was generated against the canonical engine on 2026-05-13 (seed=2328, anchor=myth-014-yomi), populated full `seasons/season_002328/` + telemetry rows at that time, and both were subsequently deleted from the engine repo after the v1.1 gear_pool re-export of 2026-05-14 23:58. The commit message phrase "from engine side-seed" framed it as a deliberate side-experiment outside the canonical 001xxx numbering — and the engine-side artifacts were treated as disposable scaffolding.

3. **Reproducibility-from-seed is misleading.** Engine code changed substantively between Yomi generation (2026-05-13) and now — notably B10.4 swarm calibration (eff_attr 0→7) which alters pack-combat math and would shift convergence outcomes. Re-running seed=2328 today produces **A Yomi** (same anchor, similar themes) but not **THIS Yomi** (the data drax, gandalf, and design docs all reference). File-level archive is the only path to preserve THIS Yomi.

4. **Cross-repo inventory comprehensive.** Engine: absent (confirmed via filesystem + SQL). Demo: absent. Collaboration: referential-only in 13+ design docs, all skill handoffs, CHANGELOG (loss does not break prose but breaks live iteration against the design vocabulary).

### Recommended next action

**Option 3 (archive into elrond's archive/) — IMMEDIATE, no ADR-006 friction** (read from loadout permitted, write to elrond seam permitted). Output: 556 KB archived + companion markdown + MIGRATION.md v1.2 entry. Closes SPOF immediately.

**Option 2 (loadout origin remote)** — Matt-action when convenient. Complement to option 3, not alternative. Together they restore 4-deep redundancy.

**Option 1 (regenerate from seed)** — separate dispatch if Matt wants Yomi back in canonical engine state for analytics consistency. Should NOT be coupled to SPOF remediation; do option 3 first regardless.

**Option 4 (accept gap)** — rejected.

### Sequencing

Sequenced for knight-rider:

1. **Now (if Matt approves):** Elrond executes option 3. ~15 min.
2. **Matt's convenience:** Matt executes option 2. ~15 min.
3. **Deferred:** Option 1 as separate scoped dispatch.

### Knight-rider follow-ons

- Audit § 3.6 update — replace the Yomi hypothesis paragraph with a pointer to this audit. Can be folded into elrond's option-3 execution pass.
- MIGRATION.md v1.2 entry — elrond authors as part of option 3.
- Optional decisions-log entry codifying the side-seed-archive-on-import discipline.
- Star-lord-side note re: deterministic-replay's silent assumption (`seasons/<id>/gear/catalog.json` must exist for re-export).

Knight-rider: audit ready. If you and Matt sign off on option 3, elrond can execute in this same session. Otherwise, dispatch B is COMPLETE and elrond returns to await-instruction state.

— elrond, 2026-05-16
