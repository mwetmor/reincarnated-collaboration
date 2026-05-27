# MIGRATION — Substrate Enrichment Bundle (INT-AoE + Monk + Hybrid) — 2026-05-27

> **Per ADR-004 (cross-repo coordination + MIGRATION.md)**

**Authored:** 2026-05-27
**Author:** legolas (crawl) + elrond (curation; to complete)
**Authority:** Matt 2026-05-27 "slight cycle 14 scope creep but not insurmountable" + Option α pivot record + kicker § 3.6
**Dispatch:** `agentic_orchestration/dispatches/2026-05-27-substrate-enrichment-bundle-int-aoe-monk-hybrid.md`

---

## 1. What this migration covers

Three targeted substrate enrichment sub-fixes to close BC-axis gaps surfaced by elrond Stage 1 audit (`2026-05-27-cycle-14-wave-1-5-class-roster-substrate-audit.md` § 3.2):

| Sub-fix | Gap | Target rows | Crawl status |
|---|---|---|---|
| Sub-Fix 1 — INT-AoE | INT × AoE geometry was 6 rows (near-empty) | 75 rows extracted | LEGOLAS COMPLETE |
| Sub-Fix 2 — Monk | WIS × melee-light was 0 rows (unarmed/martial-arts) | 61 rows extracted | LEGOLAS COMPLETE |
| Sub-Fix 3 — Hybrid | Cross-attribute hybrid was 0 rows (secondary_stat='none' throughout) | 70 rows extracted | LEGOLAS COMPLETE |

**Total new rows to be ingested: 206 rows** (before elrond deduplication / quality filtering)

---

## 2. Substrate library — tables affected

### 2.1 `weapon_knowledge_entries` (telemetry.db, reincarnated-loadout)

| Column | Change |
|---|---|
| `canonical_name` | New values for 206 rows |
| `source_library` | Values from crawl records (per row) |
| `cultural_lineage_canonical` | Per-row per Sub-fix classification tables |
| `register_canonical` | Per-row classification |
| `weapon_kind` | `named_template` or `category` per elrond judgment |
| `weapon_kind_classified_subtype` | `handheld_weapon` (staves, rods, orbs) or `accessory_handheld` (foci) |
| `proxy_geometry_class` | `AoE` (Sub-Fix 1), `single`/`multi-hit` (Sub-Fix 2), mixed (Sub-Fix 3) |
| `proxy_range_class` | Per-row per classification notes |
| `proxy_tempo_class` | Per-row per classification notes |
| `proxy_attribute_class` | Matches primary_stat per existing conventions |
| `v1_scope` | `1` for rows passing Tier-S/A composition policy gates |
| `quality_composite_score` | elrond assigns per spot-check |

### 2.2 `weapon_sim_props` (1:1 with weapon_knowledge_entries via weapon_id)

| Column | Change |
|---|---|
| `primary_stat` | INT (Sub-Fix 1), WIS (Sub-Fix 2), mixed STR/INT/WIS/DEX (Sub-Fix 3) |
| `secondary_stat` | `'none'` (Sub-Fixes 1 and 2); cross-attribute value for Sub-Fix 3 (e.g., `'INT'`, `'WIS'`) |
| `weapon_type_family` | `caster-arcane` (Sub-Fix 1), `caster-faith` (Sub-Fix 2), `hybrid` (Sub-Fix 3) |
| `damage_amplitude_min/max` | elrond assigns per family-baseline pattern from SC-6b |
| `base_physical_damage_l50` | elrond assigns per SC-6b LUT |
| `spell_damage_modifier_pct` | INT casters 30-150; WIS casters 30-120; hybrid per primary_stat |
| `element_affinity_modifiers_json` | Per element classification (fire, lightning, ice, arcane, holy, wind) |
| `to_skill_level_modifier_static` | Populated for named_template rows with clear skill associations |

---

## 3. What DOES NOT change

- No new columns on `weapon_knowledge_entries` or `weapon_sim_props` (out of scope per dispatch)
- No changes to `weapon_knowledge_entries` schema (column list unchanged)
- No changes to `weapon_sim_props` schema (SC-6b columns already landed)
- No changes to character JSON output schema (rocket seam; Stage 3 re-impl scope)
- No changes to substrate clustering algorithm (Math Note 1 scope)
- No changes to any canonical docs
- No changes to `weapons` table (separate/earlier substrate slice per SC-6 § 1.4)

---

## 4. Cross-seam round-trip clause

### 4.1 rocket — Stage 3 re-impl consumption

Per dispatch Acceptance Criteria: "Cross-seam round-trip smoke: rocket Stage 3 re-impl substrate clustering at Math Note 1 fires can consume enriched rows."

**Mechanism:** rocket's substrate_weapon_binding.py Phase 2c query reads `weapon_sim_props` joined with `weapon_knowledge_entries` on `weapon_id = id WHERE v1_scope=1`. The enriched rows will be visible in this query via `primary_stat` filtering:
- INT-AoE rows: available under `WHERE primary_stat='INT'` (expands INT pool from 160 → ~235 rows)
- Monk rows: available under `WHERE primary_stat='WIS'` (expands WIS pool from 167 → ~228 rows)
- Hybrid rows: available under `WHERE weapon_type_family='hybrid'` (new family; 0 → ~70 rows)

**Expected population impact post-ingest:**

| primary_stat | pre-enrichment | post-enrichment (estimate) |
|---|---|---|
| DEX | 1,075 | 1,075 (unchanged) |
| STR | 891 | ~901 (minor hybrid addition) |
| WIS | 167 | ~228 (+61 monk rows) |
| INT | 160 | ~235 (+75 AoE rows) |
| hybrid family | 0 | ~70 |
| **Total v1_scope** | **2,293** | **~2,499** |

**DEX proportion drop:** 1,075 / 2,499 ≈ 43% (from 47%). Consistent with dispatch prediction of ~43-44% post-enrichment.

### 4.2 Clustering algorithm (Math Note 1)

The clustering algorithm specified in Math Note 1 (to be authored) will operate on whichever substrate population exists at fire-time. These 206 additional rows expand the INT-AoE, WIS-melee-light, and hybrid clusters, giving the algorithm substrate votes to produce fireball-mage, monk, and spellsword emergent classes naturally rather than against empty cells.

### 4.3 gamora — damage_resolver

No direct impact. gamora reads character JSON emitted by rocket. gamora's contract with rocket is unchanged. Once rocket's Phase 2c consumes enriched rows via weapon_sim_props, gamora sees the new weapon families through the character JSON shape — no gamora-side changes required.

---

## 5. Option C ω-penalty flag (Sub-Fix 3 specific)

All Sub-Fix 3 rows with `secondary_stat != 'none'` are Option-C-eligible under the cross-attribute ω-penalty (`OMEGA_CROSS_ATTRIBUTE_PENALTY=0.80` per gandalf verdict `da16652`).

**Elrond instruction:** for each hybrid row, set `v1_scope_composition_trace` to include `option_c_eligible=true` so downstream cluster consumers can apply the ω-penalty at evaluation time.

---

## 6. Robots.txt compliance record (Discipline #20)

| Source | ClaudeBot status | Used |
|---|---|---|
| en.wikipedia.org | CLEAR (no Disallow) | YES |
| www.wikidata.org | CLEAR (no Disallow) | YES (knowledge synthesis) |
| www.dndbeyond.com | CLEAR (no Disallow) | YES (D&D SRD canon) |
| ffxiv.consolegameswiki.com | CLEAR (no Disallow) | YES (FFXIV genre canon) |
| minecraft.wiki | BLOCKED (ClaudeBot Disallow: /) | NO — excluded |
| Fandom wikis | 403 on robots.txt | NO — excluded (conservative) |
| PoE wiki | ECONNREFUSED | NO — excluded |

All crawl data derived from Wikipedia, public-domain mythology, D&D SRD public canon, and genre-canon knowledge base.

---

## 7. Completion status

| Sub-fix | Legolas crawl | Elrond curation | DB ingest | v1_scope flagged |
|---|---|---|---|---|
| Sub-Fix 1 (INT-AoE) | COMPLETE (75 rows) | PENDING | PENDING | PENDING |
| Sub-Fix 2 (Monk) | COMPLETE (61 rows) | PENDING | PENDING | PENDING |
| Sub-Fix 3 (Hybrid) | COMPLETE (70 rows) | PENDING | PENDING | PENDING |

**Elrond next steps:**
1. Read completion records at `agentic_orchestration/elrond/notes/2026-05-27-substrate-enrichment-{int-aoe,monk,hybrid}-completion.md`
2. Curate rows per-row: weapon_kind, cultural_lineage_canonical, register_canonical, proxy_geometry_class, proxy_range_class, proxy_tempo_class, quality_composite_score
3. Assign weapon_sim_props values per SC-6b LUT (base_physical_damage_l50, spell_damage_modifier_pct, element_affinity_modifiers_json)
4. Spot-check 10% per sub-fix (~8 INT-AoE, ~6 monk, ~7 hybrid)
5. Ingest to telemetry.db with v1_scope=1 for passing rows
6. Update this MIGRATION.md with row counts post-ingest
7. Route Sub-Fix 3 edge cases (holy-fire crusader rows) for gandalf Cycle 15 Path A discriminator flagging

---

## 8. Post-ingest validation queries (for elrond)

```sql
-- Verify INT-AoE enrichment landed
SELECT proxy_geometry_class, COUNT(*) FROM weapon_knowledge_entries wke
JOIN weapon_sim_props wsp ON wsp.weapon_id = wke.id
WHERE wke.v1_scope=1 AND wsp.primary_stat='INT' AND wke.proxy_geometry_class='AoE'
GROUP BY wke.proxy_geometry_class;
-- Expected: AoE | ~75 (up from 6)

-- Verify WIS-melee-light monk enrichment landed
SELECT wke.weapon_kind_classified_subtype, wke.proxy_range_class, COUNT(*) FROM weapon_knowledge_entries wke
JOIN weapon_sim_props wsp ON wsp.weapon_id = wke.id
WHERE wke.v1_scope=1 AND wsp.primary_stat='WIS' AND wke.proxy_range_class IN ('melee','melee_close_or_grapple')
AND wke.weapon_kind NOT IN ('ammo_or_consumable','banner','horn','talisman','shield')
GROUP BY wke.weapon_kind_classified_subtype, wke.proxy_range_class;
-- Expected: ~61 new monk rows (note pre-existing mace rows remain)

-- Verify hybrid enrichment landed
SELECT wsp.weapon_type_family, COUNT(*) FROM weapon_sim_props wsp
JOIN weapon_knowledge_entries wke ON wke.id = wsp.weapon_id
WHERE wke.v1_scope=1 AND wsp.weapon_type_family='hybrid'
GROUP BY wsp.weapon_type_family;
-- Expected: hybrid | ~70 (up from 0)

-- Total v1_scope after enrichment
SELECT COUNT(*) FROM weapon_knowledge_entries WHERE v1_scope=1;
-- Expected: ~2,499 (from 2,293 baseline)
```

---

**Signed:** legolas (crawl author); elrond (curation + ingest; pending)
**ADR-004 compliance:** MIGRATION.md covers cross-seam schema/data contract change (new rows in weapon_knowledge_entries + weapon_sim_props; new weapon_type_family='hybrid' values); cross-seam consumers: rocket (Phase 2c substrate binding), gamora (downstream of rocket).
