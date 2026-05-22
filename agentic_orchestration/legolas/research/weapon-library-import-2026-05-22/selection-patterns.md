# Selection Patterns — Substrate-Vector → Candidate Weapon Set
# Priority 4

**Date:** 2026-05-22
**Mode:** A (analytical design)
**Commissioner:** gandalf, authorized by Matt 2026-05-22 evening
**Commission:** `agentic_orchestration/dispatches/2026-05-22-legolas-weapon-library-import-discovery.md`
**Depends on:** `schema.sql` (this directory), `canonical/story/bdi-omega-tau-tables-v1-2026-05-22.md`,
`canonical/story/gear-substrate-rule-table-v1-2026-05-22.md`
**Consumer:** rocket (W1.15 engine implementation), drax (loadout app queries)

---

## Summary

Seven parameterized SQL query templates cover the canonical selection path from substrate-vector
to candidate weapon set. The selection flow is: (1) determine the gear_catalogue_id for the
substrate-vector via the rule table; (2) query the weapons table for matching candidates using
the three-tier score (mechanical fit → aesthetic fit → license preference); (3) check density
and route to Meshy gap-fill if N=0 or N<3. The BDI ω/τ formalism integrates at two points:
ω scores inform the `dominant_element_affinities` column populated at import time (shaping
which gear × element pairings are available), and τ scores can optionally be used to penalize
near-zero or negative-τ pairs in the scoring function. All queries target the `weapons` table
using the compound indexes in schema.sql.

---

## 1. Selection Flow Overview

```
INPUT: substrate_vector = {
    dominant_element: "fire",
    range_profile: "ranged",
    stat_distribution_signature: "INT-dominant"
}
PLUS aesthetic_preference = {
    tech_level: "medieval",
    cultural_lineage: "european"
}
PLUS license_preference = "CC0"  (or "CC_OK" for CC0+CC-BY)

STEP 1: Lookup gear_catalogue_id
    → G1 rule table: (fire, ranged, INT-dom) → gear_catalogue_id = 11 (Caster Staff)

STEP 2: Query weapons (patterns P1–P5 below)
    → ordered candidate set with match_score

STEP 3: Check density (pattern P6)
    → N=0 → Meshy gap-fill (pattern P7)
    → N<3 → serve available + queue Meshy gap-fill
    → N≥3 → serve from ranked candidates

OUTPUT: ranked weapon list [{weapon_id, display_name, match_score, source_url, ...}, ...]
```

---

## 2. Gear Catalogue Lookup (Pre-Query Step)

The rule table (`canonical/story/gear-substrate-rule-table-v1-2026-05-22.md`) maps
(dominant_element, range_profile, stat_distribution_signature) → gear_catalogue_id.
This is a deterministic lookup implemented in engine code (not SQL), returning an integer 1–15.

**Stat distribution signature → range_class mapping:**
```
range_profile "melee"  → range_class = 'melee'
range_profile "medium" → range_class = 'medium'
range_profile "ranged" → range_class = 'ranged'
```

**Element → stat_affinity default (per element_biases.py:28):**
```
fire/water/lightning/shadow → INT
earth/wind/holy            → WIS
(physical/cross-attribute) → STR
```

---

## 3. Query Templates

### P1 — Canonical Selection Query (primary path; full aesthetic match)

Returns weapons matching all three layers: gear catalogue + aesthetic tuple + license.
Scored and ranked. This is the standard query called at generation time.

```sql
-- P1: Canonical selection query
-- Parameters: :gear_id, :range, :tech, :culture, :license_ok_min
-- :license_ok_min = 1 to accept game_approved licenses; set :cc0_only = 1 for CC0-only mode

SELECT
    w.weapon_id,
    w.display_name,
    w.weapon_subclass,
    w.gear_catalogue_id,
    w.range_class,
    w.tech_level,
    w.cultural_lineage,
    w.tone,
    w.style_register,
    w.dominant_element_affinities,
    w.best_omega_score,
    ws.source_url,
    ws.preview_image_url,
    ws.license_id,
    l.slug AS license_slug,
    l.attribution_required,
    ws.attribution_text,
    -- SCORING FUNCTION (higher = better match)
    (
        -- Layer 1: Mechanical fit (40% weight)
        -- gear_catalogue_id exact match is the primary mechanical predicate
        CASE WHEN w.gear_catalogue_id = :gear_id THEN 40 ELSE 0 END
        -- range_class bonus for exact match (within gear family, range confirms)
        + CASE WHEN w.range_class = :range THEN 10 ELSE 0 END

        -- Layer 2: Aesthetic fit (40% weight)
        -- tech_level: exact match = 20pts; adjacent = 10pts
        + CASE
            WHEN w.tech_level = :tech THEN 20
            WHEN :tech = 'medieval' AND w.tech_level = 'fantasy' THEN 10
            WHEN :tech = 'medieval' AND w.tech_level = 'ancient' THEN 8
            WHEN :tech = 'fantasy' AND w.tech_level = 'medieval' THEN 10
            ELSE 0
          END
        -- cultural_lineage: exact match = 20pts; fictional always accepted = 5pts
        + CASE
            WHEN w.cultural_lineage = :culture THEN 20
            WHEN w.cultural_lineage = 'fictional' THEN 5
            WHEN w.cultural_lineage = 'cross_cultural' THEN 8
            ELSE 0
          END

        -- Layer 3: License preference (20% weight)
        + CASE l.slug
            WHEN 'CC0'                      THEN 20
            WHEN 'CC_BY'                    THEN 15
            WHEN 'OGA_BY'                   THEN 14
            WHEN 'CC_BY_SA'                 THEN 8
            WHEN 'royalty_free_commercial'  THEN 5
            ELSE 0
          END

        -- BDI ω-score bonus: high-ω pairs get a small boost (0–10 pts)
        + COALESCE(ROUND(w.best_omega_score * 10), 0)
    ) AS match_score

FROM weapons w
JOIN weapon_sources ws ON ws.weapon_id = w.weapon_id AND ws.is_primary = 1
JOIN licenses l        ON l.license_id = ws.license_id AND l.game_approved >= :license_ok_min

WHERE
    w.gear_catalogue_id = :gear_id
    AND w.range_class    = :range
    AND w.readiness_state = 'ready_to_import'

ORDER BY match_score DESC
LIMIT 20;
```

**Performance notes:**
- Uses `idx_weapons_selection_core` (gear_catalogue_id, range_class, tech_level, cultural_lineage, readiness_state)
- The WHERE clause hits the two leftmost index columns (gear_catalogue_id, range_class) + rightmost (readiness_state)
- Typical result set: 5–50 rows at 100K weapon scale; LIMIT 20 caps output

---

### P2 — Strict Mode (CC0 only + sim_verified)

For when only CC0-licensed, sim-verified weapons are acceptable. Adds `ws.license_id = 1`
(CC0 license_id from seed data) and `sim_viable = 1` predicates.

```sql
-- P2: Strict mode — CC0 + sim verified only
-- Parameters: :gear_id, :range, :tech, :culture

SELECT
    w.weapon_id,
    w.display_name,
    w.weapon_subclass,
    ws.source_url,
    ws.preview_image_url,
    ws.attribution_text,
    (
        CASE WHEN w.tech_level = :tech THEN 20 ELSE
             CASE WHEN w.cultural_lineage = 'fictional' THEN 5 ELSE 0 END
        END
        + CASE WHEN w.cultural_lineage = :culture THEN 20
               WHEN w.cultural_lineage = 'fictional' THEN 5
               ELSE 0 END
        + COALESCE(ROUND(w.best_omega_score * 10), 0)
    ) AS match_score

FROM weapons w
JOIN weapon_sources ws  ON ws.weapon_id = w.weapon_id AND ws.is_primary = 1
JOIN licenses l         ON l.license_id = ws.license_id AND l.slug = 'CC0'
LEFT JOIN weapon_sim_props sp ON sp.weapon_id = w.weapon_id

WHERE
    w.gear_catalogue_id   = :gear_id
    AND w.range_class     = :range
    AND w.readiness_state = 'ready_to_import'
    AND (sp.sim_viable = 1 OR sp.weapon_id IS NULL)  -- allow unverified if no sim record exists

ORDER BY match_score DESC
LIMIT 10;
```

---

### P3 — Aesthetic Expansion (fallback: cross-aesthetic allowed)

When P1 returns fewer than 3 results for a specific (tech, culture) pair, expand the
aesthetic search to accept adjacent tech_levels and cross-cultural weapons.

```sql
-- P3: Aesthetic expansion — relaxed cultural + tech matching
-- Used when P1 returns N < 3 results
-- Parameters: :gear_id, :range

SELECT
    w.weapon_id,
    w.display_name,
    w.weapon_subclass,
    w.tech_level,
    w.cultural_lineage,
    ws.source_url,
    ws.preview_image_url,
    l.slug AS license_slug,
    (
        -- License preference preserved
        CASE l.slug WHEN 'CC0' THEN 20 WHEN 'CC_BY' THEN 15
                    WHEN 'OGA_BY' THEN 14 ELSE 5 END
        + COALESCE(ROUND(w.best_omega_score * 10), 0)
        -- Penalize non-fictional cultural mismatches slightly
        + CASE w.cultural_lineage WHEN 'fictional' THEN 5
                                  WHEN 'cross_cultural' THEN 3
                                  ELSE 2 END
    ) AS match_score

FROM weapons w
JOIN weapon_sources ws ON ws.weapon_id = w.weapon_id AND ws.is_primary = 1
JOIN licenses l        ON l.license_id = ws.license_id AND l.game_approved = 1

WHERE
    w.gear_catalogue_id   = :gear_id
    AND w.range_class     = :range
    AND w.readiness_state = 'ready_to_import'
    -- Exclude weapons already in the P1 result set by passing their weapon_ids
    AND w.weapon_id NOT IN (SELECT value FROM json_each(:p1_ids))

ORDER BY match_score DESC
LIMIT 10;
```

---

### P4 — Gear Family Fallback (relax to gear family on empty)

If both P1 and P3 return 0 results, relax the gear_catalogue_id constraint to the gear family
(melee / caster / ritual / ranged) rather than specific gear ID.

```sql
-- P4: Gear family fallback
-- gear_family_ids = comma-separated list of IDs in the same family
-- e.g., melee family = (1,2,3,4); caster family = (9,10,11,12,13,14,15); ranged = (5,6,7,8)
-- Parameters: :gear_family_ids (JSON array), :range, :tech, :culture

SELECT
    w.weapon_id,
    w.display_name,
    w.gear_catalogue_id,
    w.weapon_subclass,
    w.tech_level,
    w.cultural_lineage,
    ws.source_url,
    l.slug AS license_slug,
    (
        CASE l.slug WHEN 'CC0' THEN 20 WHEN 'CC_BY' THEN 15 ELSE 5 END
        + CASE WHEN w.tech_level = :tech THEN 15 ELSE 0 END
        + CASE WHEN w.cultural_lineage = :culture THEN 15
               WHEN w.cultural_lineage = 'fictional' THEN 8
               ELSE 0 END
        + COALESCE(ROUND(w.best_omega_score * 10), 0)
    ) AS match_score

FROM weapons w
JOIN weapon_sources ws ON ws.weapon_id = w.weapon_id AND ws.is_primary = 1
JOIN licenses l        ON l.license_id = ws.license_id AND l.game_approved = 1

WHERE
    w.gear_catalogue_id IN (SELECT value FROM json_each(:gear_family_ids))
    AND w.range_class     = :range
    AND w.readiness_state = 'ready_to_import'

ORDER BY match_score DESC
LIMIT 10;
```

**Gear family groupings:**
```
melee_family:   [1, 2, 3, 4]  (Greatsword, Twin Daggers, Battle Spear, Mace/Warhammer)
ranged_family:  [5, 6, 7, 8]  (Longbow, Crossbow, Blunderbuss, Throwing Knives)
caster_family:  [9, 10, 11, 12] (Wand, Orb, Caster Staff, Tome)
ritual_family:  [13, 14, 15]   (Censer, Holy Symbol, War-Trumpet)
```

---

### P5 — BDI ω-Filtered Query (high-ω pairs only)

For engines running in "canonical-pairing" mode — only serving weapons whose element
affinity has a BDI ω-score above a threshold. Requires the `dominant_element_affinities`
column to be populated at import time.

```sql
-- P5: BDI ω-filtered selection
-- :gear_id, :range, :element (the dominant_element from substrate-vector), :omega_min_threshold
-- Requires dominant_element_affinities to be populated (import phase B+)

SELECT
    w.weapon_id,
    w.display_name,
    w.weapon_subclass,
    w.best_omega_score,
    w.dominant_element_affinities,
    ws.source_url,
    l.slug AS license_slug,
    (
        CASE l.slug WHEN 'CC0' THEN 20 WHEN 'CC_BY' THEN 15 ELSE 5 END
        -- ω-score contributes directly to ranking (0–30 pts based on 0.0–1.0 range)
        + COALESCE(ROUND(w.best_omega_score * 30), 0)
    ) AS match_score

FROM weapons w
JOIN weapon_sources ws ON ws.weapon_id = w.weapon_id AND ws.is_primary = 1
JOIN licenses l        ON l.license_id = ws.license_id AND l.game_approved = 1

WHERE
    w.gear_catalogue_id   = :gear_id
    AND w.range_class     = :range
    AND w.readiness_state = 'ready_to_import'
    AND w.best_omega_score >= :omega_min_threshold  -- e.g., 0.70 for canonical pairs only
    -- Element affinity check: does this weapon pair with the dominant element?
    AND (
        w.dominant_element_affinities LIKE '%' || :element || '%'
        OR w.dominant_element_affinities IS NULL  -- NULL = not yet analyzed; include permissively
    )

ORDER BY match_score DESC
LIMIT 10;
```

**ω threshold guidance (per BDI ω-table v1):**
- `>= 0.85`: canonical pairs only (holy+censer, shadow+twin-daggers, lightning+wand, fire+orb)
- `>= 0.70`: canonical + cross-attribute coherent pairs (most BDI table entries)
- `>= 0.50`: any mechanically-coherent pair (wide selection)
- No threshold: any weapon in the gear family

---

### P6 — Density Check Query

Called before P1 to determine whether to attempt DB selection or route immediately to Meshy.
Returns a single density_tier value.

```sql
-- P6: Density check — before attempting P1
-- Parameters: :gear_id, :range, :element
-- Uses precomputed substrate_density table for fast lookup

SELECT
    weapon_count_ready,
    weapon_count_cc0,
    weapon_count_cc_ok,
    density_tier,
    meshy_gapfill_queued
FROM substrate_density
WHERE
    dominant_element  = :element
    AND range_class   = :range
    AND gear_catalogue_id = :gear_id;
```

**Density-routing decision logic (engine-side; not SQL):**
```python
density = db.execute(P6, element=element, range=range_class, gear_id=gear_id)

if density is None or density.weapon_count_ready == 0:
    # N=0: empty substrate region
    route = "meshy_gapfill"
    if not density.meshy_gapfill_queued:
        queue_meshy_gapfill(element, range_class, gear_id)

elif density.weapon_count_ready < 3:
    # N<3: sparse
    route = "db_selection_with_meshy_queue"
    if not density.meshy_gapfill_queued:
        queue_meshy_gapfill(element, range_class, gear_id)  # background; don't block

else:
    # N>=3: adequate/dense
    route = "db_selection"
    candidates = db.execute(P1, gear_id=gear_id, range=range_class, ...)
```

---

### P7 — Density Maintenance Aggregate (run after each import batch)

Populates the `substrate_density` table. Not a selection query — a maintenance query run
by the import pipeline after each batch completes.

```sql
-- P7: Density map refresh
-- Run after each import batch; refreshes all (element, range, gear) combinations

-- Step 1: Clear and repopulate from aggregate
DELETE FROM substrate_density;

-- Step 2: Repopulate for each element × range × gear combination
-- Note: element is derived from dominant_element_affinities JSON string
-- This INSERT uses JSON_EACH for affinities; adapter note: SQLite JSON functions require 3.38+

INSERT OR REPLACE INTO substrate_density
    (dominant_element, range_class, gear_catalogue_id,
     weapon_count_total, weapon_count_ready, weapon_count_cc0, weapon_count_cc_ok,
     density_tier, last_computed)
SELECT
    je.value AS dominant_element,
    w.range_class,
    w.gear_catalogue_id,
    COUNT(*)                                           AS weapon_count_total,
    SUM(CASE WHEN w.readiness_state = 'ready_to_import' THEN 1 ELSE 0 END) AS weapon_count_ready,
    SUM(CASE WHEN w.readiness_state = 'ready_to_import'
              AND l.slug = 'CC0' THEN 1 ELSE 0 END)   AS weapon_count_cc0,
    SUM(CASE WHEN w.readiness_state = 'ready_to_import'
              AND l.game_approved = 1 THEN 1 ELSE 0 END) AS weapon_count_cc_ok,
    CASE
        WHEN SUM(CASE WHEN w.readiness_state = 'ready_to_import' THEN 1 ELSE 0 END) = 0 THEN 'empty'
        WHEN SUM(CASE WHEN w.readiness_state = 'ready_to_import' THEN 1 ELSE 0 END) < 3 THEN 'sparse'
        WHEN SUM(CASE WHEN w.readiness_state = 'ready_to_import' THEN 1 ELSE 0 END) <= 10 THEN 'adequate'
        ELSE 'dense'
    END AS density_tier,
    datetime('now') AS last_computed

FROM weapons w
JOIN weapon_sources ws ON ws.weapon_id = w.weapon_id AND ws.is_primary = 1
JOIN licenses l        ON l.license_id = ws.license_id
JOIN json_each(COALESCE(w.dominant_element_affinities, '"all"')) je
     ON je.value IN ('fire','water','earth','wind','lightning','holy','shadow')
     -- NOTE: for weapons without element affinities, treat as available for all elements
     -- by using a CROSS JOIN to elements table instead — see implementation note below

WHERE w.gear_catalogue_id IS NOT NULL
GROUP BY je.value, w.range_class, w.gear_catalogue_id;
```

**Implementation note on element affinity:** Until the ω-analysis pass populates
`dominant_element_affinities`, weapons with NULL affinities should be treated as candidates
for ALL element combinations. The import pipeline should seed this column using the
gear_catalogue_id → natural_element_family mapping from the BDI ω-table and rule-table
during Phase A import.

---

## 4. Density-Routing Rules (Complete)

```
P6 result → routing decision:

N=0 (density_tier='empty'):
    → Route to Meshy gap-fill
    → Queue Meshy generation request with params:
        {gear_catalogue_id, dominant_element, range_class, tech_level, cultural_lineage}
    → Return placeholder (null gear) or pre-generated Meshy fallback if available
    → Mark substrate_density.meshy_gapfill_queued = 1

N=1–2 (density_tier='sparse'):
    → Serve available weapons from P1 (use them; don't block on generation)
    → Queue Meshy gap-fill in background (no blocking)
    → Log sparse region for priority gap-fill schedule

N=3–10 (density_tier='adequate'):
    → Run P1; serve top result
    → No Meshy gap-fill needed

N>10 (density_tier='dense'):
    → Run P1 with full scoring; select top-ranked result
    → Consider P5 (ω-filtered) for canonical-pairing mode
    → No Meshy gap-fill needed
```

---

## 5. Scoring Framework

The scoring function in P1 operates in three layers:

**Layer 1: Mechanical fit (0–50 points)**
- Gear catalogue ID exact match: 40 pts
- Range class confirmation: 10 pts
- Rationale: gear_catalogue_id is derived deterministically from the rule table; a weapon in
  the correct gear slot always scores these points. Range class is a redundant confirmation.

**Layer 2: Aesthetic fit (0–40 points)**
- Tech level exact match: 20 pts; adjacent: 8–10 pts
- Cultural lineage exact match: 20 pts; fictional: 5 pts; cross-cultural: 8 pts
- Rationale: aesthetic fit drives cohesion-judge identity recognition. A medieval European fire
  mage should get a medieval European caster staff, not a sci-fi wand. The 20-pt cap ensures
  a perfect aesthetic match cannot outweigh a wrong gear slot.

**Layer 3: License preference (0–20 points)**
- CC0: 20 pts (maximum preference — no attribution overhead)
- CC-BY: 15 pts (attribution required but commercially viable)
- OGA-BY: 14 pts (equivalent to CC-BY for game purposes)
- CC-BY-SA: 8 pts (share-alike complication; caution)
- Royalty-free commercial: 5 pts (viable but adds cost/procurement tracking)
- Rationale: license preference is a tiebreaker, not a primary filter. game_approved=1
  is already enforced in the JOIN condition; the scoring layer differentiates WITHIN the
  approved set.

**BDI ω bonus (0–10 points):**
- best_omega_score × 10 (adds 0–10 pts based on ω ∈ [0.0, 1.0])
- Rationale: high-ω pairs are canonically resonant per BDI formalism; they should be
  preferred over low-ω alternatives when both are otherwise equal. The 10-pt cap ensures
  ω is a tiebreaker at equal aesthetic scores, not a primary discriminator.

**Total score range:** 0–100 points (perfect match: 40+10+20+20+20 mechanical+range+tech+culture+license = 110; capped in practice by exclusive branches)

---

## 6. BDI ω/τ Integration

### ω integration (mechanical overlap → element affinity population)

The BDI ω-table (`canonical/story/bdi-omega-tau-tables-v1-2026-05-22.md`) provides predicted
ω values for each gear-archetype × element pair. These inform the `dominant_element_affinities`
and `best_omega_score` columns at import time:

**Import-time ω assignment (Phase A):**
For each weapon imported with a known `gear_catalogue_id`, assign element affinities by
applying the BDI ω-table threshold:
- ω ≥ 0.70 for this gear × element pair → add element to `dominant_element_affinities`
- Store the maximum ω across all qualifying elements as `best_omega_score`

Example: Weapon with gear_catalogue_id=9 (Wand/Focus Rod):
- BDI ω-table: Wand+lightning=0.90, Wand+water=0.87, Wand+shadow=0.88, Wand+fire=0.83
- All ≥ 0.70 → dominant_element_affinities = "lightning,water,shadow,fire"
- best_omega_score = 0.90

**Post-H3 ω recalibration (Phase C+):**
After rocket runs the H3 hypothesis test (W1.21), empirical β-archive data will recalibrate
the ω-table scaling constants κ_1/κ_2. At that point, `dominant_element_affinities` and
`best_omega_score` for all weapons should be recomputed against the calibrated table. This
is a full-table UPDATE pass — add it to the import-batch maintenance script.

### τ integration (thematic resonance → tone/cultural selection)

The BDI τ-table documents positive-τ pairs (canonical resonance) and negative-τ pairs
(polar opposition requiring bridge substrate). For weapon selection:

**Positive-τ use:** When `tone` column matches the τ-pairing (e.g., tone='sacred' for a
holy+censer weapon), add a τ-bonus to the P1 scoring. This is NOT currently in the P1 query
— it requires the `tone` column to be reliably populated at import time (which it often isn't
for non-Smithsonian sources). Flag for Phase B implementation after import quality improves.

**Negative-τ use:** Negative-τ pairs (holy+shadow, sustain+glass-cannon) should NOT be served
together in the same kit. This is a kit-composition constraint enforced at the engine level
(post-selection), not at the weapon-selection query level. The weapon selection queries do NOT
enforce τ constraints — they select the best individual weapon; the engine enforces τ compatibility
across the full substrate-vector.

---

## 7. Query Performance Considerations

**Index utilization for P1:**
```
QUERY PLAN (expected at 100K weapons):
SEARCH weapons USING INDEX idx_weapons_selection_core
    (gear_catalogue_id=? AND range_class=? AND readiness_state=?)
→ expected rows: ~500–2,000 (gear_catalogue_id alone narrows to ~6,667; range+readiness ~400)
→ sequential scan of these ~400 rows for scoring + ORDER BY
→ LIMIT 20 stops early

Total cost: acceptable; sub-millisecond at 100K scale
```

**P6 density check (hot path):**
```
SEARCH substrate_density USING INDEX idx_density_vector
    (dominant_element=? AND range_class=? AND gear_catalogue_id=?)
→ 315-row table; single row return; near-instant
```

**P7 density refresh (batch; not hot path):**
The P7 aggregate query is expensive (full table scan + JSON_EACH) but runs as a batch job
after import, not during generation. At 100K weapons, expected runtime: 2–10 seconds.
Acceptable for a once-per-import-batch maintenance job.

---

**Signed (research):** legolas (research scout; Mode A analytical design)
**For:** rocket (W1.15 engine-side query implementation); drax (loadout-app queries);
BDI ω/τ integration sketch for gandalf canonical doc authoring.
