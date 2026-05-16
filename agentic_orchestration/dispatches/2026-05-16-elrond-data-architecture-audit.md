# Dispatch — elrond data-architecture audit (2026-05-16)

**Status:** COMPLETE
**Target:** elrond (data steward; first major task per `~/.claude/agents/elrond.md`)
**Branch:** main (across all four repos for read-only inspection)
**Tag intent:** No code tags — this dispatch produces a baseline audit document, not code changes.

## Context

The Reincarnated project's data surface has accreted organically across four repos. Stores include:
- `reincarnated-engine/data/telemetry.db` (star-lord-owned engine telemetry, ~1.8M `class_fight_loadouts` rows per gamora B10.4 finding)
- `reincarnated-engine/research.db` (mentioned in older permission allowlists; status unclear; needs investigation)
- `reincarnated-engine/exports/season_NNN/*.json` (season export artifacts; star-lord)
- `reincarnated-loadout/data/season_NNN/*.json` (loadout app season data; star-lord-exported, drax-consumed)
- `reincarnated-demo/` data files (drax)
- `agentic_orchestration/research/` (new — Legolas raw output + Elrond curated state)
- Future: catalogue database (Elrond-owned per the catalogue-based form-bias resolution path locked in doc 37)
- Future: map/story/quest generator data (TBD)

Without a coherent architecture map, these fragment. New work (catalogue crawl, form-bias resolution, future generators) needs a baseline to build against. **This audit is your first major task — it grounds all your subsequent data-steward work.**

## Deliverable

A single comprehensive baseline document at:

`agentic_orchestration/research/curated/data-architecture-audit-2026-05-16.md`

### Required sections

1. **Inventory** — every data store across all four repos. Format: name, location, owner (current), schema version (if applicable), table list, approximate row counts, file size, last-modified date. Be complete — don't skip stores that seem minor.

2. **Ownership map** — which agent owns each store today per AGENTS.md and observed practice. Flag any stores with ambiguous or split ownership.

3. **Gaps and overlaps** — where stores duplicate data, where data is missing that should exist (e.g., gear stats not in telemetry per the 2026-05-15 star-lord gear-pool-stats discovery), where consistency is brittle across stores.

4. **Cross-store joins currently performed** — how agents query across stores today. Are joins ad-hoc reads? Manual SQL ATTACH? Cross-repo file reads? Document the existing patterns; flag any that are fragile.

5. **Recommended architecture** — principled separation. Proposed:
   - **Engine telemetry layer** (star-lord) — engine-internal simulation/balance data
   - **Generated season artifacts** (star-lord) — exported JSON consumed by demo/loadout
   - **External research layer** (Elrond) — catalogue DB, research findings, abstraction analysis tables
   - **Demo/loadout app data** (drax-consumed) — derived from generated artifacts, not authoritative

   But this is your professional call. If you see a better separation, propose it.

6. **Schema conventions** — what conventions should hold across stores (naming, versioning, source-anchoring, license/cost capture for external data, audit trails)?

7. **Migration recommendations** — which existing stores should be restructured, which are fine as-is. Cost/benefit per recommendation. Sequencing.

8. **Cross-store query patterns** — recommended standardized patterns for legitimate cross-store queries (SQL ATTACH conventions, view definitions, etc.).

9. **Pending work this enables** — which queued items become unblocked once the audit lands:
   - Catalogue DB schema design (your subsequent work)
   - Catalogue-based form-bias work (rocket integration, eventually)
   - Star-lord telemetry tier-1 extension (dispatched 2026-05-14, may benefit from audit findings)
   - Future map/story/quest generator data layer

## Constraints

- **Read-only across all four repos.** Do not modify any code, schema, or data. The deliverable is documentation only.
- **No backfilling assertions you can't verify.** If a store's status is unclear (e.g., `research.db` mentioned in old allowlists), document what you can verify and flag uncertainty.
- **Cite specifically.** When you describe a schema, reference the actual file or `sqlite3 .schema` output. When you describe a pattern, reference the code that does it.
- **Time-bound target:** 3-5 hours of focused Elrond work. Audit is comprehensive but not exhaustive — sections 1-4 are descriptive (must be complete); sections 5-8 are prescriptive (your professional recommendations); section 9 is forward-looking.

## Cross-seam coordination

- **Star-lord** — engine telemetry is his seam. Your audit reads his code and DB but does not modify. If your recommendations affect telemetry schema, those flow through knight-rider with MIGRATION.md per ADR-004 — not unilateral changes.
- **Drax** — loadout / demo data consumption is his. Your audit reads his code and data; recommendations flow through knight-rider.
- **Knight-rider** — receives the audit deliverable; sequences any follow-on dispatches the audit recommends.
- **Gandalf** — when his Phase-2 deliverable is informed by your audit (e.g., data-architecture implications for embodiment vocabulary), you provide structured findings on request.

## Acceptance

- All nine sections present and substantive
- Inventory is complete (no stores missed)
- Recommendations are specific (not handwavy)
- Document is referenced in your `AGENT_STATE.md` at session close
- Knight-rider notified at completion with audit path + 2-3 sentence verdict

## Required reading before starting

1. `AGENTS.md` — team topology and seam ownership
2. `GOVERNANCE.md` — especially ADR-004 cross-seam coordination
3. `~/.claude/agents/elrond.md` — your own definition; specifically "First major task — Data architecture audit"
4. `canonical/37-form-bias-diagnosis-and-recovery.md` § "Catalogue-based form-bias resolution path" — context on why this audit matters now
5. `agentic_orchestration/skill_handoff_2026-05-15.md` — current team state at start of audit
6. Any recent `MIGRATION.md` files in the engine repo

## Completion record

**Completed:** 2026-05-16 (first-invocation session)
**Audit path:** `agentic_orchestration/research/curated/data-architecture-audit-2026-05-16.md`
**AGENT_STATE seed:** `agentic_orchestration/research/curated/AGENT_STATE.md`

### Summary verdict

The data layer is structurally sound at the seam level but has three concrete fragilities — a 15 GB telemetry hotspot driven by JSON-blob columns, a silent `engine/seasons/` → `loadout/data/` shape mismatch (the largest architectural issue surfaced), and a dormant `research.db` whose deferral has gone stale. The forthcoming catalogue layer fits cleanly as a fourth, independent data store. No emergency restructures recommended; three sequenced cleanups proposed.

### Key findings

1. **`class_fight_loadouts.loadout_json` drives the 15 GB telemetry size** (1.9M rows × ~6.7 KB per blob ≈ 12.7 GB inside one column; season_001005 alone is ~10 GB of that). Normalization is medium-cost; deferred until query/disk pressure forces it.
2. **`engine/seasons/` directory shape is leaking into `loadout/data/`.** Loadout consumes the engine's *internal* working manifest (`manifest_version: 1.3`, per-class JSON tree) for most seasons but consumes the export-shape gear_pool for Yomi. The publish step is a manual `cp` with no script, no provenance, no schema gate. Two consumers (demo, loadout) on incompatible shapes. Recommended Phase-2 cleanup.
3. **`research.db` is dormant since 2026-05-07.** All structural content is in telemetry.db; only `research_notes` (5) and `bugs_log` (5) carry narrative. The 2026-05-07 decisions-log deferral ("Active. Consolidation deferred until research.db contents and schema are audited") is now satisfied. Recommended Phase-1 cleanup: archive narrative content to markdown, retire DB.
4. **Empty `telemetry.db` at engine root** (0 B, 2026-05-14) — almost certainly an accidental wrong-cwd `sqlite3` invocation residue. Cosmetic but misleading. Recommended Phase-1 cleanup.
5. **Telemetry NULL gaps despite migration 1.9**: `seasonal_element_name` 87% NULL, `convergence_wall_time_seconds` 84% NULL, `termination_reason` 79% NULL on `class_fight_loadouts`. Pre-1.9 rows; star-lord's seam to backfill (already noted in star-lord AGENT_STATE).
6. **Inconsistent season coverage across stores**: 23 in telemetry, 23 in `engine/seasons/`, 5 in `engine/exports/`, 5 in `demo/public/seasons/`, 6 in `loadout/data/`. Notably `season_002328` (Yomi) lives ONLY in `loadout/data/` — its source data is not in engine telemetry or `seasons/`. Provenance gap; needs star-lord investigation.
7. **No SQL ATTACH or formal cross-store join pattern exists today.** Fine while there's only one DB; needs convention before catalogue.db ships. Convention proposed in audit § 8.
8. **Schema-versioning is inconsistent.** Telemetry.db has rigorous `schema_meta` + numbered migrations. JSON-file stores (anchor library, element pool, canonical library) are pinned at `1.0` in their `version` field despite content growth. Convention proposed in audit § 6.

### Sequencing recommendations

| Phase | Owner | Cost | Trigger |
|---|---|---|---|
| **Phase 0** — this audit | elrond | done | — |
| **Phase 1** — `research.db` retirement + empty `telemetry.db` deletion | elrond + Matt approval (ADR-006) | 30 min | Ready when Matt authorizes |
| **Phase 2** — codify L2→L4 publish step + retire `engine/seasons/` shape from loadout | star-lord (lead) + drax | 1-2 days | Knight-rider authors dispatch when sequenced |
| **Phase 3** — `class_fight_loadouts.loadout_json` normalization | star-lord + gamora | several days | Disk pressure or analytics-cost trigger; not active |
| **Phase 4** — Catalogue DB schema design | elrond | 1-2 days | Awaits Gandalf style-register lock + first Legolas catalogue sample |

### Deviations from spec

None. All nine required sections present. Section 5 ("Recommended architecture") refines the dispatch's three-layer proposal into a four-layer separation (L1 engine internal / L2 generated artifacts / L3 external research+catalogue / L4 app-derived) — explicitly justified in audit § 5.1 as a refinement, not a rejection.

### Notification

Knight-rider: audit ready for read; recommend reading § 0 verdict, § 3.3 (the publish-step leak), § 7 (sequencing). Phase-1 is low-risk and ready to dispatch as soon as Matt has a window.
