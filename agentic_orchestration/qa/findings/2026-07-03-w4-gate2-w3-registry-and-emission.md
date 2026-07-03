# Finding — 2026-07-03 — W4 Gate-2 — W3 registry writer + batch-1 emission (star-lord)

**Reviewer:** jack-ryan (DEV-MODE)
**Severity:** PASS-WITH-FINDINGS (1 WARN → Matt; INFO items)
**Target:** `star-lord/v-demo-run-w3-step0-registry-1` @ `dc00b2a`; `star-lord/v-demo-run-w3-emission-batch1-1` @ `1112cf0` + hygiene `2839caf`
**Developer:** star-lord (export/telemetry seam)
**Principles applied:** #2 (smoke-vs-full), #3 (cross-seam round-trip / bundle-as-contract), #4 (decisions-log/ledger as truth), #5 (severity); Disciplines #2, #3, #8, #11, #29

## What I found
The W3 emission recovered cleanly from a genuine two-defect episode and the fixes are verified in-tree. DEFECT 1 (`config_to_kit` cell-level-key overwrite → 7 reported vs 700 true survivors) is root-caused correctly and fixed: `season_generation_pipeline.py:1647` is now `config_to_kits: dict[str, list]` and the marking loop (`:1708`) iterates every kit per cell — the `_s99`-only artifact is resolved. DEFECT 2 (`parents[4]` DB path escape) is fixed at `run_registry.py:62` (`parents[3]`, verified: DB lands inside the engine repo). The canonical-JSON recovery mode (`--recover-from-canonical`) is honest: its own completion record openly retracts the prior "no re-fight required" claim as WRONG AS SHIPPED and documents the 1.5h burn that gap caused — that is Discipline #11/#29 attribution honesty of a high order. The recovered bundle is real: 700 kits across 7 cells, monsters 40, gear 150, factions present, `proxy_scaling` key present, `proxies:[]` on all (honest batch-1 state, criterion C PARKED not faked), `flavor_text:None` on all 700 (dry-run; LLM pass PARKED-resumable per §7), `bc_target_cell` populated on 700/700 (0 None) after the hygiene fix. I ran the suites: `test_run_registry.py` + `test_w3_emission_driver.py` = 81 passed. Registry ledger queried live: 12 rows — defective `86fa640c` retained DEFECT-DISCOVERED, two interim 700-rows SUPERSEDED (`f0bd67e5`,`3fcd85a1`), canonical `cbeb9471` live (cert=NULL, pre-W4), 8 smoke rows marked SMOKE-ARTIFACT. Ledger matches the records exactly.

## Rationale
The recovery, defect fixes, registry writer, and ledger all pass. Two items do not clear silently:

**WARN — tag `1112cf0` does not cover hygiene `2839caf` (→ Matt).** The batch-1 tag points at `1112cf0`, but the hygiene commit `2839caf` (the only commit after the tag) is NOT tagged and contains material W4-consumed state: (a) the `bc_target_cell` fix that rewrote 5,604 lines of the shipped bundle — at `1112cf0` every kit had `bc_target_cell=None`; the live/canonical bundle W4 audits is the `2839caf` state; (b) the smoke guard + `SmokeProductionPathError`; (c) the smoke-row re-marking. The registry's live canonical run `cbeb9471` was produced by `2839caf`, not by the tagged commit. **A named artifact (the tag) and the artifact W4 actually reviews diverge by one commit.** This is a Discipline #4 ledger-integrity gap: the roster W4/§8 curates comes from an untagged bundle. Recommend a follow-up tag `star-lord/v-demo-run-w3-emission-batch1-2` @ `2839caf` (or move the batch-1 milestone) so provenance is byte-anchored before Matt picks a roster. Not a BLOCK on the content — the bundle is correct — but the provenance seam must close before curation.

**Assessment of "does TestSmokeGuard close the tmp-path blind spot that masked DEFECT 2?" — NO, and the record does not claim it does.** These are two distinct blind spots. (1) The tmp-path blind spot (all 48 tests used `:memory:`, so `_DEFAULT_REGISTRY_PATH` was never exercised → `parents[4]` slipped) is closed by a DIFFERENT test: `test_default_registry_path_inside_engine_root` (test 49, `test_run_registry.py:146`), which asserts `_ENGINE_ROOT.name == "reincarnated-engine"` and `_DEFAULT_REGISTRY_PATH.is_relative_to(_ENGINE_ROOT)`. That test genuinely closes DEFECT 2's blind spot. (2) TestSmokeGuard (Group H, 8 tests) closes a SEPARATE defect — the 8 production-registry smoke rows — by rejecting production stages when `smoke=True`. The guard is sound for future writes but does NOT re-mark or re-stage the 8 historical polluted rows (they remain `stage=stage-2-registered`, cleaned only via `cert_status=SMOKE-ARTIFACT`). So the audit trail is disambiguated by cert_status, not by stage. Adequate for W4 (queries can filter SMOKE-ARTIFACT), noted for the record.

## INFO (non-blocking)
- `--dry-run-flavor` means criterion B (zero hollow spots) is **NOT yet satisfiable on flavor**: `flavor_text=None` on all 700 kits, all 40 monsters, all 150 gear. This is correctly PARKED-resumable per §7, but W4/criterion-B closure cannot certify "no NULL flavor_text" until the LLM pass fires. The pass is per-item/resumable (W1 verified) — no double-billing risk. This is expected state, flagged so W4 DRIFT-CRITIC does not read the current bundle as criterion-B-complete.
- The 8 SMOKE-ARTIFACT rows retain a production `stage` value; only cert_status distinguishes them. Cosmetic, but a future hygiene pass could null their stage for a cleaner ledger.
- `bc_target_cell` is emitted as a nested dict (not the flat cell-id string). Consistent across 700 kits; drax/W4 consumers should key on the dict shape. Not a defect; noting the shape for the six-type/round-trip auditor.

## Action
- [ ] star-lord: fire a follow-up tag at `2839caf` (bundle+guard+bc_target_cell state) so the W4-curated bundle is provenance-anchored — OR document in the registry/state board that `cbeb9471`/`2839caf` is the authoritative batch-1 artifact superseding the `1112cf0` tag.
- [ ] star-lord: fire the PARKED LLM flavor pass (or confirm it as an explicit named W4-follow, so criterion B is not read as met on the current NULL-flavor bundle).
- [ ] Matt (WARN escalation): confirm the follow-up-tag disposition before the §8 roster pick — the curated roster should come from a tagged, not floating, commit.

## References
- `reincarnated-engine/src/reincarnated/export/run_registry.py` (`:62` path fix, smoke guard)
- `reincarnated-engine/src/reincarnated/export/w3_emission_driver.py` (recovery mode)
- `reincarnated-engine/src/reincarnated/generation/season_generation_pipeline.py:1647,1708` (config_to_kits fix)
- `reincarnated-engine/tests/test_run_registry.py:146` (path blind-spot test), Group H (smoke guard)
- `reincarnated-engine/src/reincarnated/output/w3_batch1_bundle.json` (700 kits, live state @ `2839caf`)
- `data/emission_registry.db` (12 rows; canonical `cbeb9471`)
- Tags `dc00b2a`, `1112cf0`; untagged hygiene `2839caf`
