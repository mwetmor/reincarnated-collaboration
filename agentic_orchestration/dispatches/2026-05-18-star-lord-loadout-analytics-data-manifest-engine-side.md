# 2026-05-18 — star-lord — Loadout analytics suite data manifest (engine-side; Track B.6 co-author)

**Authority:** Overnight sprint invocation `agentic_orchestration/gandalf/requests/2026-05-18-knight-rider-mobile-playable-analytics-visual-benchmark-sprint.md` Track B § 2.2 deliverable 6; pre-authorization matrix § 6 row 5.
**Type:** Pattern B; ~1-2 hours.
**Status:** 🟢 **AUTHORED — fires AFTER gandalf IA lands (`canonical/story/loadout-analytics-suite-information-architecture-2026-05-18.md`). Star-lord checks for IA presence before starting; if IA not yet landed, surface QUESTION in hive log and pause.**
**Tag intent:** none (data manifest doc; star-lord authorship).

---

## Why

Gandalf's analytics IA names panels and what stories each panel tells. Each panel needs a data source. Some data lives in engine output (`reincarnated-engine/output/`), some in telemetry (`data/telemetry.db`), some in LLM-generated season artifacts. Star-lord owns the engine + telemetry + LLM-emission side; elrond owns the catalogue + research side. Together they produce a single co-authored manifest that drax consumes when implementing iteration-1.

This dispatch is the engine-side half of the co-authored manifest.

---

## Required reading

1. The full invocation (above) — Track B § 2.2 deliverable 6
2. Gandalf IA: `canonical/story/loadout-analytics-suite-information-architecture-2026-05-18.md` (must be present; produced by gandalf-IA dispatch before this fires)
3. Engine output directories: `~/Games/reincarnated-engine/output/` — what season artifacts exist; per-class JSON shape; gauntlet_recipe.json (per star-lord v1.7); cosmological_vocabulary.json
4. Engine telemetry: `~/Games/reincarnated-engine/data/telemetry.db` (read-only) — schema versions, table list, what telemetry exists in shippable shape
5. Star-lord's own MIGRATION.md files in `~/Games/reincarnated-engine/src/reincarnated/export/` and adjacent — the engine-side schema-of-record
6. LLM thematic generation outputs — wherever D1 vocabulary corpus + season-flavor outputs live (`reincarnated-engine/src/reincarnated/generation/` D1 pool files; per-season cosmological_vocabulary.json; etc.)

---

## Deliverable

A new doc at `agentic_orchestration/research/curated/loadout-analytics-data-manifest-2026-05-18.md` — **engine-side half**, co-authored later with elrond (elrond appends catalogue-side section). Or alternative: two docs, one per author, cross-referenced. Knight-rider prefers single doc with two sections (one manifest, one source of truth).

### Required content (engine-side half)

For each panel in gandalf's IA that requires engine-side data, produce one entry:

```
### Panel: <name from gandalf IA>

Story arc: <which arc this serves>
Data needed: <field list / aggregation type / temporal slice>
Source-of-record: <exact file path or DB query>
Shape today: <what the data looks like today — schema, row count, gaps>
Shippable-tonight: <yes / yes-with-transform / no>
Transform required (if any): <derivation steps drax needs to perform>
Gaps: <what's missing; Phase-2 candidate>
```

Plus a top-level **engine-side data inventory** summarizing:
- All season artifact directories with seasons enumerated + per-season file types
- Telemetry tables relevant to the analytics suite (with row counts as of tonight)
- LLM thematic-generation artifacts (D1 vocabulary pool with status counts; per-season cosmological_vocabulary.json schema; flavor-text outputs if shippable)
- Any engine-emitted JSON intended for cross-repo consumption (gauntlet_recipe.json, etc.)

---

## Methodology

1. **Survey-mode discipline** (Discipline #11 attribution + your seam's own rule): report what EXISTS. "What is" + "what's missing" are separate outputs. Do not interleave aspirational data with actual.
2. **Reproducibility-first.** Every data source has an explicit path + access pattern. Drax should be able to run a CLI snippet (jq, python -c, sqlite3) and reproduce the shape you claim.
3. **Honest gap reporting.** If gandalf's IA panel needs data that the engine doesn't currently emit, say so. Tag as Phase-2. The morning state-of-hive surfaces these to Matt as "panels we'd want but the data isn't there yet."

---

## Out of scope

- Catalogue-side data (elrond's parallel dispatch)
- Loadout app implementation (drax)
- New engine-side telemetry instrumentation (out of scope for tonight; Phase-2 commitments)
- Schema changes (Phase-2 if needed)
- Vercel scoping work (separate dispatch with drax + star-lord co-author — that's the OTHER thing on your plate tonight; see `2026-05-18-drax-plus-star-lord-vercel-deployment-options-paper.md` queued)

## HARD NOs (per invocation § 6)

- No vendor acquisitions
- No `git push --force`
- No CLAUDE.md or AGENTS.md modifications
- No load-bearing canonical-doc amendments

## Completion handoff

1. Append completion record to this dispatch
2. Hive-log STATE entry (§ 14.1.1 PRE-SIGNAL discipline)
3. Manifest doc lands at `agentic_orchestration/research/curated/loadout-analytics-data-manifest-2026-05-18.md`
4. Knight-rider then fires drax-loadout-analytics-iteration-1 (after elrond's catalogue-side section also lands)

---

*Dispatched 2026-05-18 evening by knight-rider per overnight sprint invocation Track B § 2.2 deliverable 6 (engine-side). Single-night sprint cadence.*

---

## Completion record

**Completed:** 2026-05-18 (overnight sprint)
**Author:** star-lord
**Manifest landed at:** `agentic_orchestration/research/curated/loadout-analytics-data-manifest-2026-05-18.md`

### What was delivered

Engine-side half of the co-authored data manifest. Survey-mode discipline applied throughout (what exists vs. what's missing — clearly separated). Covers all 6 gandalf IA arcs from the engine-side data angle.

**Key findings:**
1. **Cosmological vocabulary (Arc 2):** 5 vs2a seasons complete and structurally consistent. 8 slot fills + 3 pair rationale blocks per season. This is the highest-value unshipped data asset — ready to bundle and ship tonight.
2. **D1 corpus (Arc 2):** `data/seasonal_elements/pool.json` — 156 entries (60 allow-list / 50 eligible / 46 quarantine, 4 primary substrates). Note: MEMORY.md count discrepancy (81/40/35 vs current 60/50/46) explained — VFX runtime gate auto-demotes entries; static pool.json counts (60/50/46) are correct for analytics display.
3. **Role × substrate matrix (Arc 4):** Pre-extracted from all 51 classes across 5 seasons. Table included in manifest — drax can use directly as TS const.
4. **CRITICAL GAP: vs2a seasons absent from telemetry.db.** Seasons 002011-002015 have zero records in any telemetry table. Analytics suite must consume artifact JSON files directly, not telemetry.
5. **Hive dispatch pulse (Arc 6):** 231 dispatches, cleanly parseable by filename pattern. Extraction script provided. Last 4 active days: 10 / 92 / 96 / 32 dispatches.
6. **Existing useAnalytics.ts data (Arcs 1/4/5):** Already wired — archetype distribution, modifier ranges, season cards, timeline. No new extraction needed.

**Panels shippable tonight (drax):** Cosmological vocabulary (Arc 2), D1 corpus bar (Arc 2), substrate identity grid (Arc 1 — needs 15-min TS transcription), role × substrate matrix (Arc 4), hive dispatch pulse (Arc 6 — script provided). Existing useAnalytics.ts reuse panels: all ready.

**Phase-2 items captured:** 5 engine-side items (vs2a telemetry backfill, dispatch-by-purpose scan, full git commit pulse, D1 per-entry browser, LLM cost for vs2a seasons).

### Handoff state
- Elrond catalogue-side section: pending append to same manifest doc (§ 8 stub reserved)
- Knight-rider: fires drax-loadout-analytics-iteration-1 after elrond appends
