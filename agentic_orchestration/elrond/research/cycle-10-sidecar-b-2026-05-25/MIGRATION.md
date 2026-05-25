# MIGRATION — 2026-05-25 — Cycle 10 Sidecar B — weapon_kind enum extension (off-hand items) + legolas Mode B ingest

**Author:** elrond (data steward)
**Authority:** knight-rider Cycle 10 Sidecar B dispatch (`agentic_orchestration/dispatches/2026-05-25-elrond-cycle-10-sidecar-b-off-hand-substrate.md` § 3.1 + § 3.2) + composition policy v1 § 8 + off-hand-items canonical doc § 1 + ADR-004
**Status:** v1 — cross-seam impact declaration per ADR-004 + REVIEW_PROCESS Principle 6
**Target DB:** `/Users/admin/Games/reincarnated-loadout/data/telemetry.db` (gitignored; loadout-repo-owned data dir; elrond-owned schema per AGENTS.md)
**Pattern precedent:** Phase D + Stage 1 + Stage 1.5 + Stage 2.5 + Stage 3 Phase 0a + Phase 2 — additive enum extension + additive INSERT pattern

---

## §1 What changed (two lines)

1. `weapon_knowledge_entries.weapon_kind` CHECK constraint extended from 5 enum values to 11 (adds `shield`, `tome`, `banner`, `focus`, `horn`, `talisman`). Implementation via SQLite `PRAGMA writable_schema=1` schema-text edit (the standard SQLite pattern for column-level CHECK modification); integrity-checked + smoke-tested live (positive + negative).
2. ~287 existing-substrate rows reclassified to off-hand `weapon_kind` values (193 shield + 16 tome + 70 banner + 7 horn + 11 talisman + 0 focus) via heuristic source-anchored rules; 130 legolas Mode B rows INSERT-ed (48 tome + 32 banner + 30 focus/talisman + 20 horn — original 132 minus 2 Roman-Aquila/Labarum dedup pairs).

## §2 Why (one line)

Cycle 10 Sidecar B extends substrate scope to include off-hand items per off-hand-items canonical doc § 1 (the 6 categories: shield, tome, banner, focus, horn, talisman) so v1 pipeline supports shield-and-sword tanks + caster-with-focus + banner-bearing strategists + signature off-hand-item forms.

## §3 Who's affected

### §3.1 Cross-seam consumer search results

Verification method (grep at Sidecar B launch 2026-05-25 ~02:18 PT):

```bash
grep -rn "weapon_kind" --include="*.py" --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" --include="*.sql" \
  /Users/admin/Games/reincarnated-engine /Users/admin/Games/reincarnated-loadout /Users/admin/Games/reincarnated-demo \
  2>/dev/null | grep -v node_modules
```

| Repo | Production-code consumers of `weapon_kind` enum | Notes |
|---|---|---|
| `reincarnated-engine` (rocket/gamora/star-lord) | **0** | Engine's own telemetry.db is `reincarnated-engine/data/telemetry.db` (separate file); engine does NOT cross-read loadout-repo telemetry.db |
| `reincarnated-loadout` (drax) | **0** | Vite/React loadout app reads engine season JSON exports; does NOT query weapon_knowledge_entries |
| `reincarnated-demo` (drax demo1) | **0** | Pixi.js demo consumes engine season JSON + local assets only |
| `reincarnated-collaboration` (orchestration/research) | **elrond + legolas research scripts only** — all historical Phase-D / Cycle-10 stage scripts in `agentic_orchestration/elrond/research/*/scripts/` + legolas crawl scripts (write-only INSERTs with explicit column lists). All references are to PRIOR enum values (`category`/`unique`/`named_template`/`ammo_or_consumable`/`unknown`); none would fail under the EXPANDED enum (additive change preserves backward-compat) |

**Cross-seam consumer count: ZERO.** Same finding as Phase D MIGRATION.md § 3.1 (2026-05-23), Stage 1.5 MIGRATION.md § 3.1 (2026-05-24), Stage 3 Phase 2 MIGRATION.md § 8 (2026-05-25). Substrate environment unchanged in 2 days.

### §3.2 Within-domain (elrond's seam) impact

- 1 CHECK constraint modified (additive enum expansion; 5 → 11 values)
- ~287 existing rows reclassified across 5 of 6 off-hand categories (focus had 0 existing-substrate matches because the legolas Mode B crawl supplied the focuses)
- 130 new rows INSERT-ed (legolas Mode B crawl ingest)
- Stage 1 proxy fingerprint columns (`proxy_range_class`, `proxy_geometry_class`, `proxy_tempo_class`, `proxy_attribute_class`, `proxy_fingerprint_confidence`) populated on reclassified + inserted rows using off-hand-aligned heuristics (see § 5.2 below) — `COALESCE(existing, off_hand_default)` pattern; pre-existing proxy values preserved
- Stage 1.5 `extracted_named_bearer` populated on legolas Mode B inserts where `author` field is present (e.g., Sun Tzu, Chanakya, Machiavelli)

## §4 What downstream consumers need to do

**Nothing** — schema delta is purely additive, all change is backward-compatible:

- Existing INSERTs continue to work — old enum values still accepted
- Existing SELECTs continue to work — no columns dropped/renamed/retyped
- Existing reclassification scripts continue to work — they filter on prior enum values which remain valid
- Reclassified rows STILL appear in existing queries that filter on `weapon_kind IN ('category','named_template','unique')` UNLESS the query intent specifically excludes off-hand items, in which case the query must be updated. This is the only theoretical breakage surface; verified zero downstream consumers query weapon_kind by enum-value list per § 3.1.

### §4.1 Future consumers (informational)

- **Wave 5 Phase 2 re-sample** (elrond, post-Sidecar-B): re-runs Phase 2 v1_scope materialization to include off-hand items per composition policy v1 § 8. Schema-ready; sampler logic update required (separate dispatch).
- **Wave 7 Stage 4 mechanical-tagging** (elrond + legolas Mode A consult): off-hand mechanical-axis profile (buff-geometry / aura-tempo) differs from main weapons. Current proxy values (§ 5.2) are weapon-aligned heuristics; Stage 4 will refine via Mode A consultation. Substrate-ready.
- **Phase 5 cohesion-coalescence two-item alignment** (gandalf authors spec post-Cycle-10): two-item alignment scoring extends current 3-tier named-bearer pattern. Schema-ready; no further migration needed.

## §5 Schema diff

### §5.1 CHECK constraint modification

Before:
```sql
weapon_kind TEXT DEFAULT 'unknown' CHECK (weapon_kind IN
  ('category','unique','named_template','ammo_or_consumable','unknown'))
```

After:
```sql
weapon_kind TEXT DEFAULT 'unknown' CHECK (weapon_kind IN
  ('category','unique','named_template','ammo_or_consumable',
   'shield','tome','banner','focus','horn','talisman',
   'unknown'))
```

Implementation pattern (SQLite-specific):

```python
# scripts/01_schema_extension.py
PRAGMA writable_schema = 1;
UPDATE sqlite_master
   SET sql = REPLACE(sql, OLD_CHECK, NEW_CHECK)
 WHERE type='table' AND name='weapon_knowledge_entries';
PRAGMA writable_schema = 0;
PRAGMA integrity_check;  -- must return 'ok' or ROLLBACK
-- Verification: positive INSERT smoke (shield accepted) + negative INSERT smoke (invalid rejected); both passed.
```

| Item | Status |
|---|---|
| Columns dropped | 0 |
| Columns renamed | 0 |
| Columns retyped | 0 |
| Enum values **added** | 6 (`shield`, `tome`, `banner`, `focus`, `horn`, `talisman`) |
| Enum values **removed** | 0 (additive only) |
| Tables dropped | 0 |
| Tables renamed | 0 |
| Indexes dropped | 0 |
| Rows DELETEd | 0 |

### §5.2 Stage 1 proxy fingerprint defaults applied to off-hand rows

| weapon_kind | proxy_range_class | proxy_geometry_class | proxy_tempo_class | proxy_attribute_class |
|---|---|---|---|---|
| shield | melee_close_or_grapple | shield_blocker | reactive_block_tempo | STR_or_DEX |
| tome | off_hand_passive | tome_buff_aura | passive_or_cast_tempo | INT_or_WIS |
| banner | off_hand_aura | banner_rally_aura | aura_pulse_tempo | STR_or_WIS |
| focus | off_hand_passive | focus_channel_amp | cast_amp_tempo | INT_or_WIS |
| horn | off_hand_aura | horn_signal_pulse | aura_pulse_tempo | STR_or_WIS |
| talisman | off_hand_passive | talisman_ward_amp | passive_or_cast_tempo | WIS_or_INT |

`proxy_fingerprint_confidence` = **0.55** (heuristic substrate-class assignment; Stage 4 dispatch will refine via legolas Mode A consult per dispatch § 4 last paragraph).

Defaults applied via `COALESCE(existing_value, default)` — pre-existing proxy values on Stage 1 rows are preserved.

## §6 Row-level mutations

| Mutation | Rows | Reversible? |
|---|---:|---|
| UPDATE `weapon_kind` 'category'/'named_template'/'unknown' → 'shield' | 193 | Yes — reverse via `backups/telemetry.db.pre-sidecar-b` |
| UPDATE `weapon_kind` → 'tome' | 16 | Yes |
| UPDATE `weapon_kind` → 'banner' | 70 | Yes |
| UPDATE `weapon_kind` → 'focus' | 0 | Yes |
| UPDATE `weapon_kind` → 'horn' | 7 | Yes |
| UPDATE `weapon_kind` → 'talisman' | 11 | Yes |
| INSERT legolas Mode B rows | 130 | Yes — DELETE WHERE source_id LIKE 'tome-%' OR 'banner-%' OR 'focus-%' OR 'horn-%' |
| Proxy fingerprint defaults applied to off-hand rows | 417 (287 reclassified + 130 inserted) | Yes |
| Dedup pairs SKIPPED at INSERT | 2 (banner-021, banner-033) | N/A — not inserted |

## §7 Backward-compatibility checklist

| Check | Status |
|---|---|
| Existing INSERT statements with `weapon_kind IN (existing values)` continue to work | ✓ — additive enum |
| Existing SELECT statements continue to work | ✓ — no schema removal |
| Existing PRAGMA introspection | ✓ — CHECK clause expanded; column count unchanged at 46 |
| Existing UNIQUE constraint preserved | ✓ |
| Existing indexes preserved | ✓ |
| Per-row legolas Mode B uniqueness | ✓ — `source_url + #<asset_id>` fragment ensures distinct entries when multiple legolas assets share a Wikipedia page (e.g., Military_treatise hosts 20 tactical treatises) |
| Cross-seam consumer breakage | ✓ — zero per § 3.1 |
| Phase D / Stage 1 / Stage 1.5 / Stage 2.5 / Stage 3 column compatibility | ✓ — all prior schema additions preserved; this MIGRATION is additive on top |

## §8 Migration execution order (actual)

1. Pre-mining DB backup: `cp telemetry.db backups/telemetry.db.pre-sidecar-b` ✓ (203 MB; gitignored)
2. `scripts/01_schema_extension.py` — PRAGMA writable_schema edit + integrity_check + positive/negative smoke ✓
3. `scripts/02_offhand_mining_and_legolas_insert.py` — single-transaction mining + insert ✓
   - Reclassify shields (royal_armouries category_value, met-museum classification, wikidata weapon_type, wikipedia name-token) → 193 rows
   - Reclassify tomes (met-museum Books & Manuscripts, wikipedia/wikidata name-token) → 16 rows
   - Reclassify banners (met-museum Banners, osrsbox-db name-token, wikipedia/wikidata name-token) → 70 rows
   - Reclassify horns (met-museum Horn-Implements, royal_armouries hunting horn / ivory horn, wikipedia/wikidata named historical horns) → 7 rows
   - Reclassify talismans (fextralife-ds1/ds2/ds3 name-token) → 11 rows
   - Reclassify focuses (wikipedia/wikidata crystal_ball / scrying / philosopher's_stone) → 0 rows (legolas Mode B supplies the canonical focuses)
   - INSERT 130 legolas Mode B rows (132 – 2 dedup) with Stage 1 + Stage 1.5 populated
4. Post-execution verification ✓
   - PRAGMA integrity_check = ok
   - PRAGMA foreign_key_check = (empty)
   - Total active rows: 69,137 → 69,267 (+130; matches legolas insert count)
   - Off-hand total: 0 → **427 active rows** (193 shield + 64 tome + 102 banner + 14 focus + 27 horn + 27 talisman)
   - All weapon_kind values within extended enum (0 violations)
   - 8 living-religious-tradition asset IDs flagged in JSON output for gandalf curation
   - 2 dedup pairs verified skipped (only banner-004 + banner-008 present; banner-021 + banner-033 not present)
5. Tag intent: `elrond/cycle-10-sidecar-b-off-hand-mining-2026-05-25` pending gandalf 30-row spot-check pass

## §9 Discipline #25 — semantic-layer rep-audit (substrate-vote-binding boundary check)

Per dispatch § 4.5 + Sidecar B § 5.5 last bullet: off-hand items have less mode-collapse risk than main weapons (off-hand categories are tighter cultural categories). Rep-audit at substrate-classification boundary (substrate vote: does the new weapon_kind cell actually contain off-hand items?):

| Category | Random-10 spot sample (this MIGRATION; same SELECT used in output JSON) | Verdict |
|---|---|---|
| shield | Scutum/Yale, Kanta, Replica shield, Rondache (16C Milanese), Mantlet, Hayato's Shield, multiple "Shield" rows (Met) | PASS — all are shields or shield-fragments; zero false-positives in sample of 10 |
| tome | Galdrabók, Marozzo Arte dell'Armi, Art of War (Jomini), Book of Shadows, Commentarius Poliorceticus, Book of Abramelin, Toshiyoshi copy-book, Sefer Raziel, Dell'arte della guerra (Machiavelli) | PASS — all are tactical/magical/historical treatises |
| banner | Indra Dhvaja, Imperial French Eagle, Karna's Elephant Banner, Saradomin banner, Black Tugh, Landøyðan, Met Banner Showing Saint Sebastian | PASS — all are battle-standards/military-banners; osrsbox-db "Banner" rows are generic game-loot but fit category nominally |
| horn | Hunting horn, Roman Tuba, Salpinx, Shanka (Hindu conch), Montes Bocineros, Oliphant, Lituus, Gallehus, Shofar, Lur (Scandinavian) | PASS — all are signaling/ceremonial horns; zero powder-horn false-positives (correctly excluded in filter) |
| talisman | Carnelian Amulet (Islamic), Ofuda (Shinto), Sunlight Talisman (DS3), Islamic Talismanic Bowl, Agimat / Anting-anting, Takrut Scroll, Eye of Horus, Ankh | PASS — all are amulet/talisman/protective-ward items |
| focus | John Dee's Crystal Ball, Childeric I's Crystal Ball, Urim and Thummim, Aphrodite's Cestus (girdle of magic), Dorje, Skofnung Stone, Prayer Wheel, Yasakani no Magatama, Cup of Jamshid, Sampo | PASS — all are ritual/divinatory/channeling foci |

Per-category sample passes Discipline #25 rep-audit at this seam. Gandalf 30-row cross-category curation review (next session) is the binding gate; this rep-audit is the elrond pre-flight.

## §10 Cultural-sensitivity / living-tradition flags (per dispatch § 4.5 + § 4 Sidecar B § 4.5)

8 legolas Mode B rows flagged as living-religious-tradition (substrate-only per Q-B § 3.2; do NOT auto-promote to Tier-S/A; standard tier-assignment per composite scoring at re-Stage-2.5 if applicable, otherwise leave at default). Preserved in DB at imported rows; flagged in output JSON; surfaced to gandalf for curation:

| asset_id | name | tradition |
|---|---|---|
| tome-045 | Book of Shadows (Wiccan) | Wiccan |
| focus-008 | Yasakani no Magatama | Shinto imperial regalia |
| focus-012 | Dorje (Vajra) | Tibetan Buddhist ritual |
| focus-018 | Ofuda (Shinto talisman) | Shinto |
| focus-026 | Prayer Wheel (Tibetan Buddhist) | Tibetan Buddhist |
| horn-003 | Shofar | Jewish ritual |
| horn-006 | Dungchen | Tibetan Buddhist |
| horn-018 | Shanka (Hindu Conch Horn) | Hindu |

Per dispatch § 4.5: surface to knight-rider any contamination of clusters. NONE detected in this rep-audit — each living-tradition item correctly classified into its off-hand category (tome / focus / horn) with `register_canonical = 'historical'` retained per legolas Mode B normalization.

## §11 Verification statement

Per ADR-004: grep verified `weapon_kind` enum has zero production-code consumers across all four repos (same finding as Phase D MIGRATION.md § 3.1; substrate environment unchanged in 2 days).

Per REVIEW_PROCESS Principle 6 (cross-seam round-trip discipline): substrate-only schema change; no fight_log dict / loadout dict / export packet structure / inter-seam fixture touched; no engine code touched. **Round-trip: not applicable.**

Per Discipline #11 (empirical inspection over assumption): pre-state + post-state per-category counts captured in output JSON; spot-checks executed against live DB; integrity_check + foreign_key_check + invalid_weapon_kind count all = 0.

Per Discipline #25 (semantic-layer rep-audit): per-category random-10 sample inspected and reported in § 9 above; substrate-vote-binding at the categorical-classification cell PASSED for all 6 cells.

## §12 Cross-references

- **Dispatch:** `agentic_orchestration/dispatches/2026-05-25-elrond-cycle-10-sidecar-b-off-hand-substrate.md` § 3.1 + § 3.2 + § 4.3 + § 5.5
- **Composition policy v1:** `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` § 8 (Sidecar B execution scope)
- **Off-hand items canonical:** `canonical/story/off-hand-items-2026-05-24.md` § 1 (6 categories) + Approach B (single-table schema extension)
- **Legolas Mode B crawl:** `agentic_orchestration/legolas/research/cycle-10-sidecar-b-off-hand-crawl-2026-05-25/manifest.json` (132 rows; 2 dedup pairs; 8 living-tradition flags — all consumed as documented)
- **Mining output:** `output/existing-source-mining.json` (per-category counts + per-category 10-row samples + tier/v1 intersection + proxy profiles)
- **Mining markdown:** `existing-source-mining.md` (companion doc; per-category coverage + heuristic rules narrative)
- **Backup:** `backups/telemetry.db.pre-sidecar-b` (~203 MB; gitignored)
- **ADR-004 reference:** `agentic_orchestration/GOVERNANCE.md`
- **Previous additive migrations:** Phase D (9 cols), Stage 1 (5 cols), Stage 1.5 (8 cols), Stage 2.5 (3 cols), Stage 3 Phase 0a (1 col), Stage 3 Phase 2 (3 cols), Sidecar B (this migration: 1 CHECK extension + 130 INSERTs + 287 row reclassifications)

## §13 Authority + sign-off

**Approved by:** Matt 2026-05-24 Stage 0 design dialogue (Custer-with-Art-of-War scenario surfacing) + Cycle 10 scope-doc § 1-3 (autonomous decisions on additive schema choice) + Sidecar B parent dispatch FIRE authorization
**Executed by:** elrond (Sidecar B mining + schema extension)
**Co-fire with:** legolas (Mode B crawl complete 2026-05-25 commit `6b0bb4d`)
**Cross-seam coordination:** none required (zero consumers per § 3.1)
**Next:** knight-rider routes gandalf 30-row cross-category curation review combining legolas Mode B + elrond mining outputs → gandalf PASS ≥ 24/30 → tag `elrond/cycle-10-sidecar-b-off-hand-mining-2026-05-25` fires.

---

**Signed:** elrond (data steward; Cycle 10 Sidecar B executor)
