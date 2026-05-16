# Dispatch — drax viability-gate wiring review (Pimen sample)

**Status:** COMPLETE
**Target:** drax (wiring-track reviewer per AGENTS.md § Viability-gate workflow)
**Branch:** main (collaboration repo — verdict lands here)
**Tag intent:** No tags — verdict file is the deliverable.

## Context

Legolas completed his Pimen Mode-B sample crawl (`research/catalogue/pimen/sample-2026-05-16.json` — 20 rows). Per AGENTS.md § Viability-gate workflow, you (drax) own the **wiring-track review** — assessing whether the sample assets can be consumed by your pixi.js demo + React/Vite loadout pipelines in their current state.

This is **distinct from your earlier schema-wiring review** (where you assessed Elrond's schema design abstractly). This dispatch is **data-wiring review** — does the actual Pimen sample data, with its specific file formats / decomposition states / structure, actually flow through your demo's renderer and loadout app?

## Authorization

Bash access authorized under user-level `bypassPermissions`. Standard git / sqlite3 / file inspection works without prompting.

## Your review focuses on

Per AGENTS.md § Viability-gate workflow wiring-track criteria:

1. **Pixi.js consumption viability per asset.** Inspect the file_format field across the 20 sample rows. Sample row 1 shows `"file_format": "PNG, RAR archive (11 kB)"` — **PNG is fine; RAR archive is a problem.** Pixi.js doesn't load RAR. Is RAR-packaging consistent across Pimen's catalogue (would require a download → unpack → load step) or is it specific to certain packs? What's the operational cost of the unpack step in a full-crawl + ingest pipeline?
2. **Sprite-sheet shape consistency.** When Pimen ships sprite sheets vs individual frame PNGs, does your renderer's animation loader handle both? Are there cases where the sheet's frame layout isn't standard (variable frame size, non-grid layouts, etc.)?
3. **Decomposition sufficiency.** For character/enemy assets (Pimen ships some — your sample shows `category: "vfx"` for the first row but mixed across the 20), is decomposition info sufficient for animation rigging? `monolithic` means baked-atlas (less flexible); `decomposed` means body/head/weapon-separable (more flexible). What % of the sample is each, and does that ratio scale to full-crawl projection?
4. **Format compatibility — Aseprite source files.** Per Legolas Mode-B spec, Aseprite source files may appear. Your loader doesn't directly consume Aseprite — would require export-to-PNG step. Is this in the sample?
5. **Loadout app consumption.** For VFX assets that might reach the loadout app's preview tooltips or gear-card visualization, can the React/Vite consumer fetch + display these formats? Field-by-field compatibility.

## What you do NOT review

- Metadata completeness or schema-fit (elrond's structural track)
- Thematic / style-register design fit (gandalf's design track)
- Whether Pimen packs match the locked aesthetic (gandalf)

## Verdict format

Write your verdict to: `agentic_orchestration/qa/findings/2026-05-16-drax-pimen-sample-wiring-review.md`

Structure:

```markdown
# Finding — 2026-05-16 — drax wiring-track Pimen sample review

**Reviewer:** drax
**Severity:** PASS | PASS WITH FLAGS | NEEDS REWORK
**Target:** Legolas Pimen sample (20 rows)
**Track:** wiring (viability-gate of three)

## Verdict (one line)

## Per-criterion assessment
### 1. Pixi.js consumption viability (PNG vs RAR-archive vs sprite-sheet vs Aseprite)
### 2. Sprite-sheet shape consistency
### 3. Decomposition sufficiency
### 4. Format compatibility — Aseprite + other non-standard formats
### 5. Loadout app consumption

## Adaptation patches required (if any)
List with priority: must-have (blocks full-crawl) vs nice-to-have.

## Operational cost projections
E.g., "If 90% of Pimen ships RAR-archived, full-crawl ingest needs an unpack step costing X hours of pipeline work."

## What this unblocks (if PASS)
Full Pimen crawl release; demo can consume Pimen-sourced assets without modification.

## What this blocks (if NEEDS REWORK)
Specifically what demo-side or pipeline adaptations are needed.
```

## Authority boundary

You don't have schema-design veto on Elrond's work (that's his domain). Your verdict is **wiring-viability assessment** — can the demo consume this data, with what adaptation cost. Genuine cross-track conflicts go to knight-rider; if architectural, to Matt.

## Required reading

- Legolas Pimen sample: `research/catalogue/pimen/sample-2026-05-16.json`
- Your existing demo loader: `reincarnated-demo/src/data/loader.ts`
- Your existing loadout consumer: `reincarnated-loadout/src/hooks/useSeasonData.ts`
- Elrond's curation pipeline (informs the unpack-step question): `research/curated/curation-pipeline.md`
- AGENTS.md § Viability-gate workflow wiring-track criteria
- `~/.claude/agents/drax.md` § wiring-track scope

---

## Completion record

**Completed by:** drax
**Date:** 2026-05-16
**Verdict:** PASS WITH FLAGS
**Verdict file:** `agentic_orchestration/qa/findings/2026-05-16-drax-pimen-sample-wiring-review.md`

Summary: 15/20 rows (75%) ship RAR-archived PNG — mandatory unpack step required in elrond's ingest pipeline before assets reach Pixi.js. 2/20 rows include Aseprite source files (plus PNG, so no blocker). 1/20 row ships individual frames only (no spritesheet — frame-assembly step needed). Character/enemy assets (2 confirmed monolithic + 1 unknown) are wirable with the demo's current baked-animation renderer. Loadout app: static PNG thumbnails compatible now; animated VFX previews deferred. Full crawl greenlit on wiring track conditional on M1 (RAR-unpack) and M2 (frame-assembly) landing in elrond's pipeline before asset ingest.
