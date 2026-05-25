# Migration Log — Cycle 10 Stage 3 Phase 0a

**Date:** 2026-05-25
**Owner:** elrond (data steward)
**Target DB:** `/Users/admin/Games/reincarnated-loadout/data/telemetry.db`
**Table:** `weapon_knowledge_entries`
**Pattern:** Additive (1 new column); same ADR-004 additive pattern as Stages 1 + 1.5 + 2.5
**Dispatch:** `agentic_orchestration/dispatches/2026-05-24-elrond-cycle-10-stage-3-v1-scope-materialization.md` § 3.2 + § 5

---

## §1 Schema changes applied

```sql
ALTER TABLE weapon_knowledge_entries
ADD COLUMN weapon_kind_classified_subtype TEXT;
```

One column added (nullable TEXT, no CHECK constraint). Schema column count: 42 → 43. Of the 89,841 active rows, 1,126 Tier-S rows are populated (449 handheld_weapon + 316 siege_vehicle + 115 armor_body_or_head + 77 accessory_weapon_integrated + 52 art_object + 45 accessory_horse_or_equipment + 31 other + 23 ammo_consumable + 10 armor_shield + 8 accessory_handheld). The remaining 88,715 non-Tier-S rows are NULL (Phase 2 may extend population to non-Tier-S rows in future stages; current Phase 0a touches only Tier-S per scope).

**No CHECK constraint** on this column intentionally — the enum may extend in later stages (e.g., Stage 4 mythological-NULL rescue may surface new categorizations; Sidecar B may introduce subcategories not present in current substrate). String-match queries in Phase 2 sampler are deterministic without a CHECK constraint.

---

## §2 Prerequisite state finding

The dispatch describes this column as "already populated on 1,126 Tier-S rows" — empirically, the column did NOT exist in the DB at Phase 0a session start. The Stage 2.5 classifier wrote ONLY to JSON artifact `tier-s-classification.json`; no `ALTER TABLE` landed at Stage 2.5 (confirmed by reading `cycle-10-stage-2-5-2026-05-24/MIGRATION.md` § 1 — three columns added but none named `weapon_kind_classified_subtype`).

Phase 0a therefore performed a three-step operation:
1. `ALTER TABLE ADD COLUMN weapon_kind_classified_subtype TEXT`
2. Populate parent category for all 1,126 Tier-S rows from Stage 2.5 JSON
3. Subdivide the 255 accessory + armor rows per composition policy § 1.1 sub-enum

Step 1 is the substrate schema change covered by this MIGRATION.md. Steps 2 + 3 are data writes that occurred in the same script (`classify_accessory_armor_subcategory.py`). All three steps are additive (no destructive curation; no existing column values changed).

Recorded in dispatch completion record per Principle 6 transparency.

---

## §3 Cross-seam impact assessment

Empirical grep at Phase 0a launch (verifies the Stage 2.5 + Stage 1.5 finding still holds):

```
grep -RIE "weapon_kind_classified_subtype|weapon_knowledge_entries" /Users/admin/Games/reincarnated-engine /Users/admin/Games/reincarnated-loadout --include="*.py" --include="*.ts" --include="*.tsx" --include="*.js" 2>/dev/null
```

(Re-verify at Phase 2 launch per dispatch § 5 amendment.)

- **engine (rocket / gamora / star-lord):** no consumer touches `weapon_knowledge_entries` directly today (catalogue surface is consumed via `weapons` / `weapon_sources` / `weapon_tags` canonical-merged tables). Additive column DOES NOT affect existing engine queries. **No MIGRATION.md handoff required for engine seam.**
- **loadout (drax):** Vite/React loadout app does NOT query `weapon_knowledge_entries` directly (per Stage 2.5 finding and dispatch § 5.5: "loadout app reads substrate but does NOT yet consume v1_scope columns — drax integration is post-Cycle-10 work"). **No handoff required.**
- **demo (drax demo1):** Pixi.js demo does NOT query catalogue DB. **No handoff required.**
- **galadriel visual-similarity pipeline:** read-only consumer; new column is available if needed in future. No current breakage.

ADR-004 protocol: additive change with NO cross-seam consumer breakage = elrond steward authority; no parallel-handoff required.

---

## §4 Rollback procedure (if needed)

Backup taken at: `backups/telemetry.db.pre-phase-0a` (~162 MB; 2026-05-25; gitignored per per-directory `.gitignore`)

Rollback SQL (if needed):
```sql
-- SQLite 3.35+ supports DROP COLUMN:
ALTER TABLE weapon_knowledge_entries DROP COLUMN weapon_kind_classified_subtype;
-- OR restore from backup at backups/telemetry.db.pre-phase-0a
```

---

## §5 Cross-references

- Dispatch: `agentic_orchestration/dispatches/2026-05-24-elrond-cycle-10-stage-3-v1-scope-materialization.md` § 3.2 + § 5
- Composition policy v1: `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` § 1.1 (D1a / D1b / D1c)
- Phase 0a artifact: `accessory-armor-subcategory-classification.md` + `.json` (this dir)
- Population script: `classify_accessory_armor_subcategory.py` (this dir)
- Execution log: `classify_log.out` (this dir)
- Stage 2.5 source: `cycle-10-stage-2-5-2026-05-24/tier-s-classification.json` (1,126-row Tier-S classifier output JSON; binding upstream for Phase 0a)
- Previous additive migrations: Stage 1 (5 columns), Stage 1.5 (8 columns), Stage 2.5 (3 columns), Phase 0a (1 column)
- ADR-004 reference: `agentic_orchestration/GOVERNANCE.md`

---

## §6 Sign-off

**Owner:** elrond (Phase 0a)
**Authority:** Cycle 10 Stage 3 dispatch FIRE-READY (Gate-1 cleared) + Cycle 10 scope-doc § 1 autonomous decisions on additive schema choice
**Tag intent:** combined with Stage 3 final tag `elrond/v0.0-cycle-10-stage-3-v1-scope-materialization` per dispatch § 7 (single tag at Stage 3 completion; not per-phase)
