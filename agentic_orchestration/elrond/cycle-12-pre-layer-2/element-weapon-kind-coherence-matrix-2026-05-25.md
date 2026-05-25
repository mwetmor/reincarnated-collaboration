# element × weapon_kind Coherence Matrix — v1_scope substrate

**Authored:** 2026-05-25
**Author:** elrond (data steward)
**Dispatch:** `agentic_orchestration/dispatches/2026-05-25-elrond-cycle-12-pre-layer-2-prep.md`
**Source DB:** `/Users/admin/Games/reincarnated-loadout/data/telemetry.db` table `weapon_knowledge_entries`
**Per MC-2 spec** (`agentic_orchestration/legolas/research/cycle-12-mc-2-substrate-binding-heuristics-2026-05-25/methodology-recommendation.md` § 6.1 + flag 3): "Tier S/A substrate distribution" used as coherence proxy; matrix consumed by Layer 2 substrate-binding heuristic at scoring-function `w_coherence × element_weapon_kind_coherence_score` (w_coherence = 0.15 per MC-2 § 6.4).
**Consumer:** rocket Layer 2 dispatch authoring → mechanical_substrate_triple selection at runtime.
**Per Discipline #11:** direct-inspected ≥3 raw rows before aggregating (see § 4).
**Per Discipline #25 L9 semantic-layer rep-audit:** uses mechanical fields only (element + weapon_kind); no cultural_tradition / lineage / period included per MC-2 § 1 + composition policy § 3.

---

## 1. Headline finding — substrate has weak direct element-typing signal

**The substrate carries the element dimension only IMPLICITLY in canonical_name text.** No `element` column exists on `weapon_knowledge_entries`; no `element` namespace exists in `tag_taxonomy` (only `weapon_class`, `cultural_lineage`, `tech_level`, `tone`, `style_register`, `range_class`, `geometry_class`, `tempo_class`, `gear_catalogue`); the engine-side `weapons.dominant_element_affinities` column is fully NULL (0 of 5,162 rows populated). The MC-2 coherence-matrix derivation therefore necessarily falls back to keyword-inference over `canonical_name`.

Under refined word-boundary keyword inference (see § 3 for keyword sets used), the **element signal across Tier S+A is sparse**:

| Element | Tier S+A rows with name-match | % of 1,214 S+A v1_scope rows |
|---|---:|---:|
| water | 15 | 1.2% |
| holy | 13 | 1.1% |
| fire | 6 | 0.5% |
| earth | 6 | 0.5% |
| shadow | 5 | 0.4% |
| lightning | 1 | 0.1% |
| wind | 0 | 0.0% |
| **physical** (no element keyword) | **~1,168** | **~96.2%** |

This is **substrate gap #1** for Layer 2 substrate-binding: the MC-2 hybrid scoring function's element_weapon_kind_coherence_score (w_coherence = 0.15) will have near-zero discriminative signal on Tier S/A alone because >96% of S+A rows resolve to `physical` (the universal base element per MC-2 § 6.1). Per dispatch open question (§ "include Tier B for completeness if it informs the question"), elrond exercises judgment to **also include Tier B**, yielding ~10× signal density (see § 2.B below).

Per MC-2 § 6.1: "No element × weapon_kind pairing is fully impossible in the genre; some are less conventional. The coherence score should WEIGHT toward conventional pairings, not hard-filter unconventional ones." This matrix is therefore a **soft signal**, not a hard filter.

---

## 2. The matrices

### 2.A Tier S+A only — strict MC-2 spec interpretation

**Population:** 1,214 v1_scope=1 rows with quality_tier IN ('S','A')
**Matrix cells = COUNT(DISTINCT id) per (element, weapon_kind) pair; rows may match multiple elements (composite element-themed names)**

| element ↓ \\ weapon_kind → | category | named_template | ammo_or_consumable | unique | shield | talisman | banner | horn | TOTAL |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| fire        | 6  | 0  | 0  | 0 | 0 | 0 | 0 | 0 | 6 |
| water       | 14 | 0  | 1  | 0 | 0 | 0 | 0 | 0 | 15 |
| earth       | 6  | 0  | 0  | 0 | 0 | 0 | 0 | 0 | 6 |
| wind        | 0  | 0  | 0  | 0 | 0 | 0 | 0 | 0 | 0 |
| lightning   | 1  | 0  | 0  | 0 | 0 | 0 | 0 | 0 | 1 |
| holy        | 8  | 4  | 0  | 0 | 1 | 0 | 0 | 0 | 13 |
| shadow      | 3  | 2  | 0  | 0 | 0 | 0 | 0 | 0 | 5 |
| **physical** | (residual; ~1,142) | (residual; ~519) | (residual; ~19) | (residual; ~16) | (residual; ~7) | (residual; ~4) | (residual; ~4) | (residual; ~1) | ~1,168 |

**Normalized frequency (count / total typed elemental + physical row × 1.0 for self-cell)**: matrix is dominated by `physical` × `category` and `physical` × `named_template` cells, exactly as MC-2 § 6.1 predicted ("physical is the universal base element — ALL weapon kinds").

### 2.B Tier S+A+B (elrond judgment per dispatch open question) — richer signal

**Population:** 2,224 v1_scope=1 rows with quality_tier IN ('S','A','B')
**Tier B contains the bulk of `pyromantic_*`, `*-thorned`, `vampir-*` Stage 3.5 fantasy + named-template entries which carry the element signal.**

| element ↓ \\ weapon_kind → | category | named_template | ammo_or_consumable | unique | shield | talisman | banner | horn | unknown | TOTAL |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| fire        | 8  | 5  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 13 |
| water       | 14 | 7  | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 22 |
| earth       | 9  | 57 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 67 |
| wind        | 0  | 8  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 8 |
| lightning   | 1  | 4  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 5 |
| holy        | 8  | 16 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 25 |
| shadow      | 3  | 78 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 82 |
| **physical** | **1,098** | **737** | **147** | **42** | **16** | **10** | **7** | **1** | 0 | **~2,058** |

**Normalized frequency (cell-count / 2,224 total S+A+B rows):**

| element ↓ \\ weapon_kind → | category | named_template | ammo_or_consumable | unique | shield | talisman | banner | horn |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| fire        | 0.36% | 0.22% | — | — | — | — | — | — |
| water       | 0.63% | 0.31% | 0.04% | — | — | — | — | — |
| earth       | 0.40% | 2.56% | — | — | — | — | — | — |
| wind        | — | 0.36% | — | — | — | — | — | — |
| lightning   | 0.04% | 0.18% | — | — | — | — | — | — |
| holy        | 0.36% | 0.72% | — | — | 0.04% | — | — | — |
| shadow      | 0.13% | 3.51% | — | — | — | 0.04% | — | — |
| **physical** | **49.4%** | **33.1%** | **6.6%** | **1.9%** | **0.72%** | **0.45%** | **0.31%** | **0.04%** |

### 2.C Normalized per-element coherence (recommended Layer 2 lookup form)

For MC-2's soft coherence weight `w_coherence × element_weapon_kind_coherence_score(element, weapon_kind)` (w_coherence = 0.15 per § 5.2), the recommended lookup table is **row-normalized within each element** (i.e., for a given element, what fraction of name-matched rows are of each weapon_kind). This gives the "given this element, how typical is this weapon_kind?" answer the scoring function needs.

| element ↓ \\ weapon_kind → | category | named_template | ammo_or_consumable | unique | shield | talisman |
|---|---:|---:|---:|---:|---:|---:|
| fire        | 0.62 | 0.38 | 0.00 | 0.00 | 0.00 | 0.00 |
| water       | 0.64 | 0.32 | 0.05 | 0.00 | 0.00 | 0.00 |
| earth       | 0.13 | 0.85 | 0.00 | 0.00 | 0.00 | 0.01 |
| wind        | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lightning   | 0.20 | 0.80 | 0.00 | 0.00 | 0.00 | 0.00 |
| holy        | 0.32 | 0.64 | 0.00 | 0.00 | 0.04 | 0.00 |
| shadow      | 0.04 | 0.95 | 0.00 | 0.00 | 0.00 | 0.01 |
| physical    | 0.53 | 0.36 | 0.07 | 0.02 | 0.01 | 0.00 |

**Reading the table:** the value at (`fire`, `category`) = 0.62 means "given that an entry's name keys to `fire`, there is a 62% chance its weapon_kind is `category` in the S+A+B substrate." This is the coherence probability MC-2's scoring function multiplies by w_coherence = 0.15.

For zero-cells, MC-2 § 6.1 recommends NOT hard-zeroing; replace with epsilon (~0.01) to preserve soft-weighting per MC-2's "weight toward conventional pairings, not hard-filter unconventional ones" directive.

---

## 3. SQL query used

**Element inference is keyword-based over `canonical_name`** with word-boundary protection (padded LIKE patterns) to avoid false positives like `Centrefire revolver` matching `fire` or `Pair of Sword-Grip Ornaments (Menuki)` matching `air`. Keyword sets per element (rendered as SQL `LIKE` patterns with space-padded haystack):

```sql
WITH base AS (
  SELECT
    id,
    ' ' || LOWER(COALESCE(canonical_name, '')) || ' ' AS nm_padded,
    COALESCE(weapon_kind, 'unknown') AS wk
  FROM weapon_knowledge_entries
  WHERE v1_scope=1 AND quality_tier IN ('S','A','B')  -- ('S','A') for strict MC-2 variant
),
elem_match AS (
  -- FIRE keywords (boundary-protected; excludes -fire firearm suffix)
  SELECT id, wk, 'fire' AS element FROM base WHERE
    nm_padded LIKE '% fire %' OR nm_padded LIKE '% fire-%' OR nm_padded LIKE '%-fire %'
    OR nm_padded LIKE '% flame%' OR nm_padded LIKE '% pyro%' OR nm_padded LIKE '%pyromantic%'
    OR nm_padded LIKE '% blaze%' OR nm_padded LIKE '% burn%' OR nm_padded LIKE '% ember%'
    OR nm_padded LIKE '% cinder%' OR nm_padded LIKE '% inferno%' OR nm_padded LIKE '% scorch%'
    OR nm_padded LIKE '% flare%' OR nm_padded LIKE '% magma%' OR nm_padded LIKE '% phoenix%'
    OR nm_padded LIKE '% volcan%' OR nm_padded LIKE '%hellfire%' OR nm_padded LIKE '%firebrand%'
    OR nm_padded LIKE '%dragonfire%' OR nm_padded LIKE '%sunfire%' OR nm_padded LIKE '%wildfire%'
    OR nm_padded LIKE '%conflagration%' OR nm_padded LIKE '% ashen%' OR nm_padded LIKE '%ashbound%'
  UNION
  -- WATER keywords (includes ice/frost/snow/cold per element-canonical-pair flavor)
  SELECT id, wk, 'water' FROM base WHERE
    nm_padded LIKE '% water%' OR nm_padded LIKE '% ice %' OR nm_padded LIKE '% iced%' OR nm_padded LIKE '% icy%'
    OR nm_padded LIKE '% frost%' OR nm_padded LIKE '% frozen%' OR nm_padded LIKE '% glacial%' OR nm_padded LIKE '% glacier%'
    OR nm_padded LIKE '% tide%' OR nm_padded LIKE '% ocean%' OR nm_padded LIKE '% sea %' OR nm_padded LIKE '%-sea %'
    OR nm_padded LIKE '% snow%' OR nm_padded LIKE '% cold%' OR nm_padded LIKE '% blizzard%'
    OR nm_padded LIKE '% coral%' OR nm_padded LIKE '% mermaid%' OR nm_padded LIKE '% kraken%'
    OR nm_padded LIKE '% aqua%' OR nm_padded LIKE '% hydro%' OR nm_padded LIKE '% rime%'
    OR nm_padded LIKE '% poseidon%' OR nm_padded LIKE '% trident%' OR nm_padded LIKE '%tsunami%'
    OR nm_padded LIKE '% wave %' OR nm_padded LIKE '%cleanrot%'
  UNION
  -- EARTH keywords (includes stone/bone/crystal/thorn sub-element flavors per composition policy § 6.5)
  SELECT id, wk, 'earth' FROM base WHERE
    nm_padded LIKE '% earth%' OR nm_padded LIKE '% stone%' OR nm_padded LIKE '%stone %'
    OR nm_padded LIKE '% rock%' OR nm_padded LIKE '% bone %' OR nm_padded LIKE '% obsidian%'
    OR nm_padded LIKE '% crystal%' OR nm_padded LIKE '% iron %' OR nm_padded LIKE '%-iron %'
    OR nm_padded LIKE '% granite%' OR nm_padded LIKE '% boulder%' OR nm_padded LIKE '% root%'
    OR nm_padded LIKE '% mountain%' OR nm_padded LIKE '% mud%' OR nm_padded LIKE '% clay%'
    OR nm_padded LIKE '% quake%' OR nm_padded LIKE '% sand%' OR nm_padded LIKE '% thorn%'
    OR nm_padded LIKE '% moss%' OR nm_padded LIKE '% marble%' OR nm_padded LIKE '% petrify%'
    OR nm_padded LIKE '% golem%'
  UNION
  -- WIND keywords (tight bounds to exclude pair/air/falcon/feather false-positive overlap)
  SELECT id, wk, 'wind' FROM base WHERE
    nm_padded LIKE '% wind %' OR nm_padded LIKE '% wind-%' OR nm_padded LIKE '%-wind %'
    OR nm_padded LIKE '% gale%' OR nm_padded LIKE '% tempest%' OR nm_padded LIKE '% hurricane%'
    OR nm_padded LIKE '% cyclone%' OR nm_padded LIKE '% zephyr%' OR nm_padded LIKE '% breeze%'
    OR nm_padded LIKE '% squall%' OR nm_padded LIKE '% tornado%' OR nm_padded LIKE '% airblade%'
    OR nm_padded LIKE '%windborne%' OR nm_padded LIKE '%stormcaller%'
  UNION
  -- LIGHTNING keywords ("storm" deliberately removed — too ambiguous between wind/lightning;
  -- belongs to wind here for consistency with Vincere element split; lightning gets explicit thunder/electric/bolt-mythological)
  SELECT id, wk, 'lightning' FROM base WHERE
    nm_padded LIKE '% lightning%' OR nm_padded LIKE '% thunder%' OR nm_padded LIKE '%-thunder %'
    OR nm_padded LIKE '% shock %' OR nm_padded LIKE '% spark%' OR nm_padded LIKE '% electric%'
    OR nm_padded LIKE '% levin%' OR nm_padded LIKE '% mjolnir%' OR nm_padded LIKE '% volt%'
    OR nm_padded LIKE '% zeus%' OR nm_padded LIKE '% plasma%'
  UNION
  -- HOLY keywords
  SELECT id, wk, 'holy' FROM base WHERE
    nm_padded LIKE '% holy%' OR nm_padded LIKE '% sacred%' OR nm_padded LIKE '% divine%'
    OR nm_padded LIKE '% blessed%' OR nm_padded LIKE '% saint%' OR nm_padded LIKE '% angel%'
    OR nm_padded LIKE '% paladin%' OR nm_padded LIKE '% cleric%' OR nm_padded LIKE '% seraph%'
    OR nm_padded LIKE '% cherub%' OR nm_padded LIKE '% radiant%' OR nm_padded LIKE '% dawn%'
    OR nm_padded LIKE '% halo %' OR nm_padded LIKE '% grace%' OR nm_padded LIKE '% redemption%'
    OR nm_padded LIKE '% celestial%' OR nm_padded LIKE '% balder%' OR nm_padded LIKE '% hallow%'
    OR nm_padded LIKE '% smite%' OR nm_padded LIKE '%hammerdin%' OR nm_padded LIKE '%herculean%'
  UNION
  -- SHADOW keywords (includes necro/vampir/wraith fantasy sub-flavors per composition policy § 6.5)
  SELECT id, wk, 'shadow' FROM base WHERE
    nm_padded LIKE '% shadow%' OR nm_padded LIKE '% dark%' OR nm_padded LIKE '% void%'
    OR nm_padded LIKE '% night%' OR nm_padded LIKE '% black%' OR nm_padded LIKE '% vampir%'
    OR nm_padded LIKE '% abyss%' OR nm_padded LIKE '% death%' OR nm_padded LIKE '% necro%'
    OR nm_padded LIKE '% curse%' OR nm_padded LIKE '% hex %' OR nm_padded LIKE '% plague%'
    OR nm_padded LIKE '% blight%' OR nm_padded LIKE '% doom%' OR nm_padded LIKE '% dread%'
    OR nm_padded LIKE '% spectre%' OR nm_padded LIKE '% wraith%' OR nm_padded LIKE '% demon%'
    OR nm_padded LIKE '%hellfire%' OR nm_padded LIKE '% umbral%' OR nm_padded LIKE '% dusk%'
    OR nm_padded LIKE '% gloom%' OR nm_padded LIKE '% wither%' OR nm_padded LIKE '%suneater%'
    OR nm_padded LIKE '% reaper%' OR nm_padded LIKE '% ghoul%'
)
SELECT element, wk AS weapon_kind, COUNT(DISTINCT id) AS row_count
FROM elem_match
GROUP BY element, wk
ORDER BY element, row_count DESC;

-- Physical = base - elem_match (default element per MC-2 § 6.1)
SELECT 'physical' AS element, wk, COUNT(*) AS cnt
FROM base
WHERE id NOT IN (SELECT id FROM elem_match)
GROUP BY wk
ORDER BY cnt DESC;
```

**Note on multi-element rows:** the UNION (not UNION ALL) deduplicates within element. Across elements, a single row CAN match multiple elements (e.g., "Hellfire Wraith" matches both `shadow` and `fire`). In that case, COUNT(DISTINCT id) per (element, weapon_kind) increments both `(fire, X)` and `(shadow, X)` cells. This is intentional — for soft coherence scoring, the substrate truly supports both element associations for such rows, and the scorer should reflect that.

---

## 4. Empirical inspection sample (Discipline #11)

Sample raw rows BEFORE aggregating; spot-checks across the seven non-physical elements:

| canonical_name | weapon_kind | tier | inferred element |
|---|---|---|---|
| `Flame Tongue Glaive` | named_template | B | fire |
| `Type 93/Type 100 flamethrower` | category | B | fire |
| `Flamethrower, Portable, No 2` | category | B | fire |
| `pyromantic_ember_staff` | category | A | fire |
| `pyromantic_cinder_focus` | category | A | fire |
| `Frost Spear` | named_template | B | water |
| `Cleanrot Spear` | named_template | B | water |
| `Cairn Wraith's Soulreap Grasp (Missile)` | named_template | B | shadow |
| `Dread Catapult - Necrotic Skulls` | named_template | B | shadow |
| `Thorned Whip` | named_template | B | earth |
| `Obsidian Blade` | named_template | B | earth |
| `Colossal Boulder Club` | named_template | B | earth |
| `Thorned Greatsword` | named_template | B | earth |

Spot-check confirms:
- Fire pyromantic Stage 3.5 gap-fills are correctly captured (the only fire-themed entries in the substrate).
- Flamethrower entries are correctly captured as fire (judgment call — flamethrowers ARE fire-elemental for game-design purposes despite being historical/military_modern register).
- Earth `Thorned *` named_template rows form the largest single element-keyword cluster (57 rows) — confirming the substrate-led skew toward earth via thorn/bone/obsidian/stone vocabulary.
- Shadow vampir/necro/wraith named_templates form the largest non-physical cluster overall (78 rows).

**No obvious false-positive contamination remains under refined word-boundary patterns.** The earlier-tested unrefined patterns (which produced 170 fire hits) included false-positives like `centrefire` and `rimfire` (firearm cartridge terminology); these are correctly excluded under the refined `% fire %` / `% fire-%` / `%-fire %` patterns. Similarly, "Pair" no longer matches `% air%`.

---

## 5. Vocabulary notes for rocket Layer 2 consumer

### 5.1 Canonical element enum (8 elements per ground-state § 1)

Per `canonical/00-ground-state.md` § 1 and MC-2 § "Mechanical Substrate Dimensions":
1. `fire`
2. `water` (includes ice/frost/cold sub-element flavors per composition policy § 6.5)
3. `earth` (includes stone/bone/crystal/thorn sub-element flavors per § 6.5)
4. `wind`
5. `lightning`
6. `holy`
7. `shadow` (includes vampir/necro/abyss sub-element flavors per § 6.5)
8. `physical` (universal base element; no element keyword on substrate row)

**Substrate enum compliance:** all element-typed rows in this matrix conform to the 8-element enum. No `unknown` or out-of-enum element values needed.

### 5.2 weapon_kind enum (per substrate schema)

Per `weapon_knowledge_entries.weapon_kind` CHECK constraint:
- `category` (1,139 in v1_scope; 1,098 in S+A+B) — primary type-class; "Sword", "Spear", "Bow", etc.
- `named_template` (927; 737 in S+A+B) — specific named instances; "Excalibur", "Mjolnir", `pyromantic_ember_staff`, etc.
- `ammo_or_consumable` (148; 147 in S+A+B) — arrows, bolts, throwing items
- `unique` (42; 42 in S+A+B) — one-off historical/mythological pieces
- `shield` (17; 16 in S+A+B) — off-hand defensive
- `talisman` (11; 10 in S+A+B) — off-hand magical
- `banner` (7; 7 in S+A+B) — off-hand support
- `horn` (1; 1 in S+A+B) — off-hand instrument
- `unknown` (1) — orphan

**No `tome` or `focus` populated** — though both are in the CHECK constraint enum. Layer 2 should expect these weapon_kinds to be ZERO-coverage in v1_scope; INT/WIS caster cells will sample primarily from `category` rows (which includes generic "Staff", "Wand", "Rod", "Tome" categorial entries) and from `named_template` (which includes the Stage 3.5 `pyromantic_*_focus` / `pyromantic_*_tome` entries — these are the ONLY tome/focus-themed rows in v1_scope, mapped to `category` weapon_kind not the unused `tome`/`focus` weapon_kinds).

---

## 6. Substrate gaps surfaced (for rocket Layer 2 + KR awareness)

### 6.1 Element field is implicit, not explicit

**Gap:** Neither `weapon_knowledge_entries` nor `weapons` carries an explicit element column for v1_scope rows. The engine-side `weapons.dominant_element_affinities` exists but is fully NULL.

**Impact on Layer 2:** Rocket cannot do `SELECT * WHERE element = ?` against the substrate; element-matching at substrate-bind must use the keyword-inference matrix in this artifact, or escalate to a future elrond enrichment pass that populates an element column directly. Recommend the keyword-inference matrix as the v1 substrate-binding signal; a proper element column is a v1.1+ schema evolution.

### 6.2 Sparse element signal in Tier S+A

**Gap:** Only 46 of 1,214 Tier S+A v1_scope rows (3.8%) have ANY element-keyword in the name. The remaining 96.2% default to physical.

**Impact on Layer 2:** The MC-2 hybrid scoring function's w_coherence × element_weapon_kind_coherence_score (w_coherence = 0.15) will deliver near-zero discriminative pressure for INT/WIS caster cells expecting fire/water/earth/wind/lightning/holy/shadow kits — substrate provides at most 5-15 rows per non-physical element. Recommend Layer 2 use Tier S+A+B (matrix 2.B) for coherence scoring, not strict S+A (matrix 2.A).

### 6.3 Zero-coverage cells in matrix

**Gap:** Several (element, weapon_kind) cells are zero in BOTH S+A and S+A+B matrices:
- `wind × *` — only 8 total wind-themed entries (all named_template); zero `category` / `ammo_or_consumable` / `shield`. Wind kits requesting a category-level weapon will fall back to physical category.
- `lightning × *` — only 5 total; same situation as wind.
- `fire × ammo_or_consumable` — zero. Fire-themed throwing items / ammo are missing from substrate. Cell `dex_trap_assassin` (proxy=heavy fire-bomb archetype) cannot bind a fire-themed ammo at substrate.
- `fire × shield` — zero. Fire-themed shields are missing.
- `*-element × shield/talisman/banner/horn` — almost all zero. Off-hand items have minimal element-themed coverage in substrate.

**Per MC-2 § 6.1:** "no element × weapon_kind pairing is fully impossible — soft signal." Layer 2 should NOT hard-zero these cells. Apply epsilon (~0.01) or fall back to physical-category for thin-cell triples.

### 6.4 The Vincere `physical` element-handling clarification

Per MC-2 § 6.1 row `physical | ALL weapon kinds — physical is the universal base element | N/A`. This matrix treats physical as the residual element: any row whose canonical_name does NOT key to fire/water/earth/wind/lightning/holy/shadow is classed `physical`. This matches MC-2 spec.

For substrate-binding, `physical` is the highest-coherence pairing with any weapon_kind. Rocket Layer 2 should treat physical-element queries as "wide-open weapon_kind selection" without coherence penalty.

### 6.5 Composite (multi-element) rows are common in the shadow/earth fantasy named-template clusters

Some Tier-B rows match multiple elements (e.g., earth+shadow for "Boneblight Maul"). The matrix counts these in BOTH cells (per § 3 SQL note). Layer 2 substrate-bind should be aware: when sampling a row, the row may have implicit sub-element flavor across multiple Vincere elements; cohesion-judge at Phase 5 will pick the dominant element from the kit context.

---

## 7. Consumer note — what Layer 2 should expect

- **Use Matrix 2.C as the primary lookup form** for MC-2's `element_weapon_kind_coherence_score(element, weapon_kind)` scoring function. The values are row-normalized within element (sum to ~1.0 across weapon_kinds per element).
- **Apply Matrix 2.B as the secondary "raw count" form** if Layer 2 needs absolute support counts (e.g., "is there enough substrate for this element × weapon_kind cell to fire at all?").
- **Reserve Matrix 2.A (S+A only)** for QA / Phase 5 quality-only scoring contexts; it is too sparse for Phase 2 substrate-binding.
- **Substitute epsilon (~0.01) for zero cells per MC-2 § 6.1** to preserve soft-weighting.
- **`physical` is universal-coherence**; weight all (physical, *) pairings at the highest tier in the scoring function (suggest 1.0).
- **Element inference is keyword-based**, not a proper element-column lookup. Substrate gap #1 (§ 6.1) flagged for v1.1+ schema evolution; v1 Layer 2 can proceed with keyword-inference.
- **Wind and lightning are critically thin** (5-8 rows each total across all weapon_kinds in S+A+B); any kit requiring wind or lightning at substrate-bind will exercise thin-cell-fallback cascade per MC-2 § 5.2 routinely.
- **`tome`/`focus` weapon_kinds are zero-populated despite enum** — caster kits requesting tome/focus weapon_kinds will substrate-bind from `category` "Staff/Rod/Wand" entries, not from the `tome`/`focus` enum values.
