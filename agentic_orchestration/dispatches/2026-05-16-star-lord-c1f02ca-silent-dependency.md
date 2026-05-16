# Dispatch — star-lord c1f02ca silent-dependency hardening

**Status:** COMPLETE
**Target:** star-lord
**Branch:** main (engine repo)
**Tag intent:** Intermediate `star-lord/c1f02ca-silent-dependency-hardening`; no milestone tag (internal hardening).

## Context

Per Elrond's Yomi provenance audit (`agentic_orchestration/research/curated/yomi-provenance-audit-2026-05-16.md`), the gear-pool-stats re-export from your 2026-05-15 commit `c1f02ca` has a **silent dependency** on `engine/seasons/<id>/gear/catalog.json` persistence:

- The export reads `catalog.json` from disk during re-generation
- The "side-seed" framing of seasonal scaffolding treats these files as disposable
- **Yomi's engine-side artifacts were deleted** after the 2026-05-14 23:58 v1.1 gear_pool re-export — the trigger event for the SPOF that bit the project

If another season's engine-side artifacts are deleted in the future, the gear-pool re-export breaks **silently** on next invocation — no error guards on the catalog.json presence. The fragility is structural.

## Work

Guard the silent dependency. Specifically in `reincarnated-engine/src/reincarnated/export/season_exporter.py` (or wherever `_regen_gear_stats` lives):

1. **Add an explicit pre-check** for `seasons/<id>/gear/catalog.json` existence at the start of the re-generation path. If absent, raise an explicit error with a clear message naming the missing file + a remediation hint (e.g., *"Cannot regenerate gear pool for season X — engine-side artifacts at `seasons/X/gear/catalog.json` are missing. This file is required input. Either restore from archive or re-run season generation."*).
2. **Document the dependency** in `reincarnated-engine/src/reincarnated/export/MIGRATION.md` (or a sibling persistence-contract doc — your call on naming). Section title: "Persistence contract: `seasons/<id>/gear/catalog.json` is load-bearing for gear-pool re-export." Explain: the file must persist for ANY season that may be re-exported in the future; deletion-as-scaffolding-cleanup is incompatible with downstream re-export.
3. **Audit other re-export paths** for similar silent dependencies on `seasons/<id>/` files (e.g., monster re-exports, season-manifest re-exports). Surface any found; fix in this dispatch or queue follow-on.

## Out of scope

- Fixing Yomi specifically — Elrond's archival closure (Yomi Option 3) handles that file-level. Your dispatch is about *future* prevention.
- Modifying the structure of `seasons/<id>/` layout — that's not the issue; the issue is the contract going forward.
- Backfilling other engine-side artifacts that may have been deleted.

## Acceptance

- Pre-check + clear error in the re-export path
- MIGRATION.md (or sibling) section documenting the persistence contract
- Audit report (inline in MIGRATION.md or separate file) of other silent-dependency paths
- Commit with smoke-test confirmation (Discipline #2 — at minimum, simulate the missing-file case and confirm the new error fires correctly)
- Intermediate tag `star-lord/c1f02ca-silent-dependency-hardening` + push
- Knight-rider notified at completion

## Pairing recommendation

This is small (~30-60 min) and pairs naturally with the queued `2026-05-16-star-lord-research-db-script-cleanup.md` dispatch. Both are engine-side hygiene work; both are post-Yomi-incident response. Single session covers both efficiently.

## Time-bound target

30-60 minutes. Small scope.

## Required reading

- Elrond's Yomi provenance audit: `agentic_orchestration/research/curated/yomi-provenance-audit-2026-05-16.md` (especially the c1f02ca silent-dependency finding)
- Your own commit `c1f02ca` (the gear-pool-stats re-export)
- `reincarnated-engine/src/reincarnated/export/MIGRATION.md` (you already authored — append section)

---

## Completion record

**Completed:** 2026-05-16  
**Commit:** `fabbc65`  
**Tag:** `star-lord/c1f02ca-silent-dependency-hardening` (pushed to origin)

### What was done

1. **Pre-check added** — `_regen_gear_stats()` in `season_exporter.py` now raises `FileNotFoundError` with a detailed remediation hint when `seasons/<id>/gear/catalog.json` is absent. Silent degradation (return `[]` → `stats=null`) replaced with a loud failure.

2. **MIGRATION.md updated** — New section "Persistence contract: `seasons/<id>/gear/catalog.json` is load-bearing for gear-pool re-export" documents: contract statement, incompatible pattern (deletion-as-cleanup), compatible pattern (treat as durable artifact), behavior change (v1.1 null-stats fallback is gone), and audit of two other silent-dependency paths (`classes/` + `monsters/` subdirectory deletion).

3. **Audit of other silent dependencies** — Two additional paths exist (`classes_dir.glob()`, `monsters_dir.glob()`), protected at the outer `season_dir.exists()` level but vulnerable to selective subdirectory deletion. Documented in MIGRATION.md as lower-probability; queued as follow-on hardening (not blocking).

4. **Smoke test** — `test_missing_catalog_raises` added to `tests/test_export.py`; confirms `FileNotFoundError` with message matching `"engine-side artifact missing"`. 31/31 export tests pass.

### Acceptance checklist

- [x] Pre-check + clear error in re-export path
- [x] MIGRATION.md persistence contract section
- [x] Audit report (inline in MIGRATION.md)
- [x] Commit `fabbc65` with smoke-test confirmation
- [x] Tag `star-lord/c1f02ca-silent-dependency-hardening` + pushed
- [ ] Knight-rider notified (see research-db-cleanup completion record — single notification covers both)
