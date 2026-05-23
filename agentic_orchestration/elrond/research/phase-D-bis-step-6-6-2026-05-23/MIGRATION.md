# MIGRATION — 2026-05-23 — Phase D-bis Step 6.6 category-promotion sweep + Step 6.6.b unknown-lineage recovery + Step 7 F4 re-run

**Author:** elrond (data steward)
**Authority:** Matt 2026-05-23 (fire authorization for Phase-D-bis Step 6.6 + §5 self-disposition delegation for 6.6.b)
**Status:** v1 — cross-seam impact declaration per ADR-004 + REVIEW_PROCESS Principle 6
**Target DB:** `/Users/admin/Games/reincarnated-loadout/data/telemetry.db` (gitignored; loadout-repo-owned data dir; elrond-owned schema per AGENTS.md)
**Precedent doc:** `phase-D-cleaning-pipeline-2026-05-23/MIGRATION.md` (Phase D's cross-seam analysis remains the baseline; this amendment is additive within elrond's existing seam)

---

## §1 — What changed (one line)

`weapon_knowledge_entries` row-level mutations only: ~7,500 rows shift `cultural_lineage_canonical` from `'unknown'` to a recovered non-unknown lineage; ~34,200 rows promote `weapon_kind` from `'unknown'` to `'category'` plus `wieldable_humanoid` populated from source-driven rules; ~500 rows have south_american_indigenous lineage corrected; Step 7 F4 cross-source merge re-runs on the enlarged candidate pool adding ~60–300 new merge components. **Zero schema changes.** **Zero column adds/drops/renames/retypes.** **Zero enum changes.** **Zero DELETEs.**

## §2 — Why (one line)

E1 audit (`agentic_orchestration/elrond/notes/2026-05-23-phase-E-1-bis-E1-lineage-audit.md`) revealed that the 94.46% fantasy_generic figure in Legolas's Phase E-1 PCA was a v_category_sample membership artifact, NOT a real substrate property: ~35,960 museum/encyclopedia/modern-military canonical rows sit at `weapon_kind='unknown'` and never enter v_category_sample. Matt-approved fix promotes them to category; sampling-disposition triggers parallel unknown-lineage recovery so newly-promoted rows enter v_category_sample with best-available lineage labels.

## §3 — Who's affected

### §3.1 Cross-seam consumer search results

`weapon_knowledge_entries` consumer search re-run identically to Phase D MIGRATION.md §3.1 (same code paths exist; no new consumers since 2026-05-23 02:43):

| Repo | Production-code consumers | Notes |
|---|---|---|
| `reincarnated-loadout` (drax) | **0** | Loadout web app reads engine season JSON exports + per-season `data/season_NNN/` artifacts; does NOT query `data/telemetry.db` for weapon-knowledge entries. |
| `reincarnated-engine` (rocket / gamora / star-lord) | **0** | Engine's own telemetry DB is `reincarnated-engine/data/telemetry.db` (separate file); engine does NOT cross-read the loadout-repo telemetry.db. |
| `reincarnated-demo` (drax) | **0** | Demo consumes engine season JSON + Pixi.js assets; no DB queries. |
| `reincarnated-collaboration` (orchestration/research) | **legolas Phase E-1 pipeline** — `agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/scripts/*.py` (Pattern-6 axis discovery; consumes `v_category_sample` view via `SELECT * FROM v_category_sample`). |

### §3.2 Within-domain (elrond's seam) impact

- **`weapon_knowledge_entries` table:** row-level mutations only (no schema change). See §6 below for mutation counts.
- **`knowledge_entry_canonical_merge` table:** ~60–300 new rows inserted from Step 7 F4 re-run. The existing 1,194 entries (1,168 F1 RA + 26 F4 cross-source) remain intact.
- **`v_category_sample` view:** unchanged DDL; row-membership grows from 16,699 → ~49,400–50,400 (per math note §2.1 projection).

## §4 — What downstream consumers need to do

### §4.1 legolas Phase E-1 pipeline (the load-bearing consumer)

**Phase E-1 deliverables are NOW STALE and MUST be regenerated on the enlarged v_category_sample.**

Stale artifacts:
- `agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/phase-E-1-features.md` — feature matrix dimensions (16,699 × 160) become (~50,000 × 160)
- `agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/phase-E-1-axis-discovery.md` — PCA axes derived from the 16,699-row monocultural slice; will produce different axes on the enlarged pool
- `agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/phase-E-1-axis-loadings.json` — loadings change with pool
- `agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/phase-E-1-clusters.md` — clustering on the smaller pool is not meaningful for the enlarged pool

**Knight-rider authors the legolas re-fire dispatch AFTER this Phase-D-bis tag completes. It is out of scope for this dispatch.**

### §4.2 No DB-side cluster invalidation needed

Per dispatch §"Cross-seam contract change?" call-out:
- The DB tables `clusters` and `cluster_membership` are still empty (Phase E-1 smoke skipped DB writes; full-mode died mid-Deliverable-3 before HDBSCAN write-back)
- `weapon_knowledge_entries.cluster_id` is still NULL across all rows
- No cluster-invalidation mutation required from this dispatch

### §4.3 Canonical-doc impact

Per dispatch: the gandalf canonical-axis discussion in `canonical/story/hive-mind-protocol-weapon-library-import-2026-05-22.md` § 6.4 is **unaffected**. F5 PCA-primary lock is not amended; only the upstream pool the methodology operates on is corrected. Gandalf's design-fit verdict (`agentic_orchestration/gandalf/notes/2026-05-23-phase-E-1-bis-design-fit-verdict.md`) similarly preserved for the loop record; surface to knight-rider for any post-Phase-E-1-re-fire methodology decisions.

### §4.4 If a Phase D-bis-bis re-fire happens

Same backward-compat profile — re-fire is idempotent UPDATE patterns; consumers see the same column set with possibly-different values per row. No schema change in a re-fire.

## §5 — Schema diff

**NONE.** Phase-D-bis is purely row-level mutations within the existing Phase D schema (9 columns + 3 views laid down in Phase D math note §1, still intact).

| Item | Status |
|---|---|
| Columns added | 0 |
| Columns dropped | 0 |
| Columns renamed | 0 |
| Columns retyped | 0 |
| Enum values added | 0 |
| Enum values removed | 0 |
| Tables added | 0 |
| Tables dropped | 0 |
| Views added | 0 |
| View definitions changed | 0 |
| Indexes added/dropped | 0 |

## §6 — Row-level mutation summary

| Mutation type | Approximate row count | Reversible? |
|---|---|---|
| **Step 6.6.b** `cultural_lineage_canonical` recovery (additive only — only rows currently at 'unknown' are touched) | ~7,500 rows shift from 'unknown' → recovered lineage | Yes — idempotent UPDATE; reverse via pre-step6.6 backup |
| **Step 6.6.b** secondary regex fix (`south_american_indigenous` → 'fantasy_generic' or 'unknown' for ~498 FPs in game sources) | ~498 rows | Yes — idempotent; reverse via backup |
| **Step 6.6** `weapon_kind` promotion ('unknown' → 'category') for museum/encyclopedia/modern-military canonical sources | ~34,200 rows (post-FP-exclusion per math note §1.5) | Yes — idempotent WHERE clause; reverse via pre-step6.6 backup |
| **Step 6.6** `wieldable_humanoid` backfill (parallel to Step 6.5's mid-pipeline gap-fill per Phase D completion summary §7.5) | Same ~34,200 rows | Yes — source-driven deterministic extraction; reverse via backup |
| **Step 6.6** `dedup_status` upgrade ('unprocessed' → 'canonical') for newly-promoted rows that were at default unprocessed | ~29,000 of the ~34,200 promoted rows | Yes — idempotent CASE; reverse via backup |
| **Step 7 F4 re-run** new `knowledge_entry_canonical_merge` INSERT rows (cross-source merges from enlarged pool) | ~60–300 new rows | Yes — additive INSERT; reverse via backup |
| **Step 7 F4 re-run** `dedup_status` 'canonical' → 'merged_into' for newly-discovered cross-source duplicates | ~120–600 rows (estimated based on Phase D F4 ratio: 26 components × ~5 members = ~130 rows; could be higher with enlarged pool) | Yes — backup restoration; otherwise non-trivial to selectively reverse |
| **Step 7 F4 re-run** `variant_relationship` 'independent' → 'sub_variant_of:<canonical_id>' for newly-merged rows | Same ~120–600 rows | Yes via backup |

**Net effect on v_category_sample (the engine consumption view):**
- Before: 16,699 rows; 98.6% TRPG/MMO/ARPG/SRD/soulslike monoculture
- After (projected): 49,400–50,400 rows; multi-cultural distribution per math note §2.3

## §7 — Idempotency

All mutations are idempotent per math note §8. Re-running this pipeline on the post-Phase-D-bis state is a no-op (Step 6.6.b's WHERE clause filters on `cultural_lineage_canonical='unknown'`; Step 6.6's WHERE clause filters on `weapon_kind='unknown'`; Step 7's WHERE clause filters on `dedup_status IN ('canonical','unprocessed') AND weapon_kind NOT IN ('ammo_or_consumable','unknown')`).

## §8 — Rollback

**Pre-step6.6 backup:** `agentic_orchestration/elrond/research/phase-D-bis-step-6-6-2026-05-23/backups/telemetry.db.pre-step6.6` (single backup; ~152 MB; gitignored).

Restoration command (Matt-authorization required per ADR-006):
```bash
cp /Users/admin/Games/reincarnated-collaboration/agentic_orchestration/elrond/research/phase-D-bis-step-6-6-2026-05-23/backups/telemetry.db.pre-step6.6 \
   /Users/admin/Games/reincarnated-loadout/data/telemetry.db
```

Pre-existing 9 Phase D pre-step backups remain intact for deeper rollback to pre-Phase-D state if needed.

## §9 — Tag

**`elrond/phase-D-bis-step-6-6-2026-05-23`** (seam-prefix per ADR-001; intermediate; local only; **no remote push without Matt approval**).

Single tag for the amendment per math note §7. Phase D's tag `elrond/phase-D-cleaning-pipeline-2026-05-23` (commit `9e7d14b`) remains the durable Phase D baseline; this tag layers on top.

Milestone-tag candidate `v0.2-weapon-library-substrate-cleaned` is deferred per dispatch §"What knight-rider does after your return" item 6 — milestone-tag promotion awaits the post-Phase-E-1-re-fire empirical results, so the milestone reflects the corrected substrate.

## §10 — Cross-references

- This dispatch's math note: `phase-D-bis-step-6-6-2026-05-23/phase-D-bis-math-note.md`
- Phase D's MIGRATION.md (baseline cross-seam analysis; unchanged by this amendment): `phase-D-cleaning-pipeline-2026-05-23/MIGRATION.md`
- E1 audit (the load-bearing diagnostic that triggered this dispatch): `agentic_orchestration/elrond/notes/2026-05-23-phase-E-1-bis-E1-lineage-audit.md`
- Gandalf design-fit verdict (preserved in loop): `agentic_orchestration/gandalf/notes/2026-05-23-phase-E-1-bis-design-fit-verdict.md`
- Knight-rider option-set (partially obviated by E1 audit): `agentic_orchestration/knight-rider/notes/2026-05-23-phase-E-1-bis-remediation-options.md`
- Cleaning-policy § 5.2 (design intent; preserved): `canonical/story/cleaning-policy-design-2026-05-22.md`
- Hive-mind protocol § 6 Pattern 6 (preserved): `canonical/story/hive-mind-protocol-weapon-library-import-2026-05-22.md`
- Phase E-1 stale deliverables (will be regenerated on enlarged pool via separate knight-rider dispatch): `agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/`
- ADR-001 (tag protocol), ADR-004 (cross-seam coordination), ADR-006 (external-write authorization)

---

**Signed:** elrond (data steward; Phase D-bis Pattern-B executor)
**Authority:** Matt 2026-05-23
**Status:** v1 ratified pre-fire; awaiting pipeline execution
