# Loadout Analytics Suite — Data Manifest (Engine-Side)

**Author:** star-lord (engine-side half); elrond appends catalogue-side section
**Authority:** `2026-05-18-star-lord-loadout-analytics-data-manifest-engine-side.md` dispatch
**Date:** 2026-05-18
**Companion:** `canonical/story/loadout-analytics-suite-information-architecture-2026-05-18.md` (gandalf IA)
**Status:** ENGINE-SIDE COMPLETE — awaiting elrond catalogue-side append

---

## § 0 — Survey discipline

This document reports **what exists**. "Gaps" and "Phase-2 items" are labeled explicitly. No aspirational data is interleaved with actual. Every data source has an exact path + access pattern reproducible by drax.

---

## § 1 — Top-level engine-side inventory

### 1.1 — Season artifact directories

**Primary:** `reincarnated-engine/output/standard-demo-regen-2026-05-17/`
5 canonical-7 seasons. Total: 4.1GB on disk.

| Season | Anchor | Primary Theme | Classes | Monsters | Size |
|---|---|---|---|---|---|
| `season_002011` | The Border Wall | earth | 10 | 44 | 834MB |
| `season_002012` | The Cartographer's Tower | wind | 10 | 44 | 787MB |
| `season_002013` | The Dwarves' Empty Halls | water | 11 | 44 | 908MB |
| `season_002014` | The Plague City | water | 10 | 44 | 835MB |
| `season_002015` | The Throne Room of the Mad King | wind | 10 | 44 | 864MB |

Per-season file inventory (each season has all of these):

```
classes/                  # Per-class JSON files (10-11 per season)
classes.json              # Full class list as array
cosmological_vocabulary.json  # 8 slot fills + 3 pair rationale blocks
damage_formula.md         # Generation-time balance formula capture
design_context.md         # Anchor + element context
fights.jsonl              # Raw fight simulation data (~800MB per season)
gear/                     # Per-item gear JSON files
gear_pool.json            # Full gear pool (200 items per season)
gear_pool_staged.json     # Staged gear pool
generation_log.txt        # Generation run log
manifest.json             # Canonical season metadata (schema v1.10)
metadata.json             # Loadout-side metadata (format_version 1.0)
monsters.json             # All 44 monsters
reference_gauntlet.json   # Balance loop gauntlet reference (ID list)
trial.json                # Trial configuration
validation_report.json    # Generation validation results
```

**Demo-side (shipped):** `reincarnated-demo/public/seasons/`
10 seasons: 5 legacy (001001-001005) + 5 vs2a (002011-002015). Total: 6.2MB.
Per season: `classes.json`, `gauntlet_recipe.json`, `gear_pool.json`, `metadata.json`, `monsters.json`

**Loadout-side:** `reincarnated-loadout/data/`
Same 10 seasons + `sample-season` + `season_002328` + `telemetry.db` + `vfx-manifest.json`
Structure: per season = `manifest.json` + `classes/` subdirectory

**2026-05-18 regen directory:** `reincarnated-engine/output/standard-demo-regen-2026-05-18/`
Contains `season_002016` (rocket RE-FIRE sprint; REGEN_COMPLETE.json present). Status: HALT per rocket dispatch. Do NOT include `season_002016` in analytics suite — convergence drift unresolved.

---

### 1.2 — Telemetry database

**Path:** `reincarnated-engine/data/telemetry.db` (SQLite, read-only per ADR-006)
**Access pattern:** `sqlite3 ~/Games/reincarnated-engine/data/telemetry.db "<query>"`
**Loadout copy:** `reincarnated-loadout/data/telemetry.db` (synced copy; query same)

| Table | Rows | Relevance to analytics suite |
|---|---|---|
| `seasons` | 25 | Season timeline, primary themes, anchor names |
| `generation_runs` | 84 | Run durations, engine versions |
| `classes` | 261 | Archetype distribution, modifier ranges, stat distributions |
| `abilities` | 5,390 | Skill inventory (not used in analytics suite directly) |
| `monsters` | 1,100 | Monster pool across seasons |
| `trials` | 27 | Trial configurations |
| `gear` | 343 | Gear instances (lightweight) |
| `gear_instances` | 9,578 | Full gear pool with fit scores, power scores |
| `gear_traits` | 3,763 | Gear trait records |
| `llm_calls` | 3,181 | LLM call ledger: purpose, model, tokens, cost |
| `seasonal_elements` | 100 | Element assignments per season |
| `class_fight_loadouts` | 2,511,417 | Fight simulation data (all encounters across balance loop) |
| `class_monster_win_rates` | 1,530 | Per-class win rates |
| `class_balance_results` | 42 | Balance convergence outcomes |
| `schema_meta` | 17 | Schema version history |

**CRITICAL GAP — vs2a seasons not in telemetry.db:**
The 5 canonical-7 seasons (002011-002015) are NOT present in the telemetry DB. All 25 seasons in the DB are the 000xxx-001xxx range (pre-dimensional generation). The vs2a seasons were generated without telemetry write-through. The analytics suite should consume these seasons from the manifest.json / classes/*.json artifact files directly, NOT from telemetry.

The telemetry DB remains valid for LLM cost data and historical season analytics on pre-vs2a seasons.

---

### 1.3 — LLM thematic generation artifacts

**D1 vocabulary corpus:**
- **Path:** `reincarnated-engine/data/seasonal_elements/pool.json`
- **Access:** `python3 -c "import json; d=json.load(open('data/seasonal_elements/pool.json')); print(len(d['elements']), 'entries')"` (run from engine root)
- **Shape:** `{"version": "1.0", "elements": [...]}`
- **Current counts (as of 2026-05-18):** 156 total — 60 allow-list / 50 eligible / 46 quarantine
- **Note on MEMORY.md discrepancy:** MEMORY.md (2026-05-12) recorded 81/40/35. Current pool.json shows 60/50/46. The difference is due to the VFX manifest validation gate (`pool.py:_validate_pool_invariants`) auto-demoting entries where `vfx_catalogue_mapping_clean=False` at load time. The pool.json is the static corpus; the runtime counts after VFX gate are what `selector.py` actually uses. For the analytics suite display, the pool.json static counts (60/50/46) are the appropriate numbers to show — these are the corpus as-authored, before runtime gating.
- **Per-substrate breakdown (primary_slot):**

  | Substrate | Allow-list | Eligible | Quarantine |
  |---|---|---|---|
  | fire | 20 | 11 | 1 |
  | earth | 22 | 13 | 18 |
  | water | 11 | 9 | 13 |
  | wind | 7 | 17 | 14 |
  | **Total** | **60** | **50** | **46** |

- **Note:** Pool contains only 4 primary substrates (fire/earth/water/wind). Lightning/holy/shadow are engine substrates but have no D1 vocabulary pool entries — they are the "vocab freeze" group (per `pool.py:_VOCAB_FREEZE_IDS` pattern). The 7-substrate class system uses these substrates for class identity; the D1 pool generates seasonal *element names* for the 4 original slots only.

**Cosmological vocabulary (per-season):**
- **Path:** `reincarnated-engine/output/standard-demo-regen-2026-05-17/season_*/cosmological_vocabulary.json`
- **Access:** `jq '.' output/standard-demo-regen-2026-05-17/season_002011/cosmological_vocabulary.json`
- **Shape:** 8 `slot_fills` (ignition/suffusion/bulwark/displacement/impact/radiance/penumbra/resonance) + `pair_rationales` dict (3 keys) + `pair_primary_rationale` string + `pair_secondary_rationale` string + `grouping_layer_version`
- **Count:** 5 files, one per vs2a season, all present and structurally consistent
- **Sample (002011 — The Border Wall):**
  - `ignition`: "Contraband Ignition"
  - `suffusion`: "Tar Immersion"
  - `pair_thermal_rationale`: "Contraband Ignition is what accumulates in hidden pockets and detonates at the moment of inspection — volatile, cascading, exposed; Tar Immersion is what coats every surface at the crossing and never fully dries, binding travelers in slow, ambient arrest rather than sudden rupture."
- **Shippable-tonight:** YES. All 5 seasons complete, consistent structure.

**Gauntlet recipe (per-season, demo-side):**
- **Path:** `reincarnated-demo/public/seasons/season_*/gauntlet_recipe.json`
- **Schema:** v1.0; 12 slots (6 pack proxy + 6 named); emitted by star-lord v1.7 (2026-05-17)
- **Not used by analytics suite** — noted here for inventory completeness

---

## § 2 — Panel-by-panel engine-side data manifest

### Panel: Substrate Identity Grid (Arc 1)

**Story arc:** Arc 1 — The Substrate Journey
**Data needed:** Per-substrate: mechanical_signature, forbidden_mechanics, combat_pillar, ailment_signature, iconic_verbs, iconic_register, paired_with, forbidden_hybrid_with
**Source-of-record:** `canonical/story/substrate-identity-declarations-2026-05-17.md`

**Shape today:** YAML blocks embedded in Markdown. 7 substrate declarations (fire, water, earth, wind, lightning, holy, shadow). Each block has the required fields. Not machine-readable JSON — drax must either:
- (Option A) Parse the YAML from the MD at build time
- (Option B) Transcribe the 7 records into a TS const in `reincarnated-loadout/src/data/constants.ts` — faster and appropriate for a static, slow-changing dataset

**Access pattern (Option B — recommended):**
```bash
cat ~/Games/reincarnated-collaboration/canonical/story/substrate-identity-declarations-2026-05-17.md
# hand-transcribe 7 substrate records into:
# reincarnated-loadout/src/data/substrates.ts
```

**Shippable-tonight:** YES with Option B (transcription). The declarations are authored and stable. Option A (parse from MD) is more brittle and slower; Option B is 15 minutes of typing.
**Transform required:** Hand-transcription into TS const, or write a one-off parse script.
**Gaps:** None. All 7 substrates declared.

---

### Panel: Substrate Heatmap — "The expansion, season by season" (Arc 1)

**Story arc:** Arc 1 — The Substrate Journey
**Data needed:** Per-season `dominant_element` distribution across classes
**Source-of-record:** `reincarnated-loadout/src/hooks/useAnalytics.ts` → `allSubstrates`, `archetypeBySeasonRows`

**Shape today:** Already wired in `useAnalytics.ts`. The `SubstrateHeatmap.tsx` component exists. This panel is a move/reuse operation.
**Access pattern:** `grep -r 'allSubstrates\|SubstrateHeatmap' ~/Games/reincarnated-loadout/src/`

**Shippable-tonight:** YES (reuse existing component).
**Transform required:** None — wrap in new page section, add title-card prose.
**Gaps:** None.

---

### Panel: Canonical-7 Narrative Callout (Arc 1)

**Story arc:** Arc 1 — The Substrate Journey
**Data needed:** Static prose about canonical-4→canonical-7 expansion
**Source-of-record:** Static prose authored in `Analytics.tsx`. Move/reuse.

**Shippable-tonight:** YES (cut + paste into new section).
**Gaps:** None.

---

### Panel: Season-as-Authored-World Cards — Cosmological Vocabulary (Arc 2)

**Story arc:** Arc 2 — The LLM Thematic Universe
**Data needed:** Per-season: `season_id`, `anchor_name`, `season_theme_element`, `slot_fills` (8 keys), `pair_rationales` (3 keys), `pair_primary_rationale`
**Source-of-record:** `reincarnated-engine/output/standard-demo-regen-2026-05-17/season_*/cosmological_vocabulary.json` (canonical) + `manifest.json` (for anchor_name, season_theme_element)

**Shape today:** JSON files, one per season. 5 files, all present. Structure verified:
```json
{
  "season_id": "season_002011",
  "grouping_layer_version": "v1.2",
  "anchor_name": "The Border Wall",
  "season_theme_element": "pitch",
  "slot_fills": {
    "ignition": "Contraband Ignition",
    "suffusion": "Tar Immersion",
    "bulwark": "Checkpoint Hold",
    "displacement": "Crossing Surge",
    "impact": "Toll Strike",
    "radiance": "Declared Passage",
    "penumbra": "Smuggled Transit",
    "resonance": "Gate Signal"
  },
  "pair_rationales": {
    "pair_thermal_rationale": "<prose>",
    "pair_position_rationale": "<prose>",
    "pair_luminance_rationale": "<prose>"
  },
  "pair_primary_rationale": "<prose>",
  "pair_secondary_rationale": "<prose>"
}
```

**Note:** `season_theme_element` in `cosmological_vocabulary.json` contains the *seasonal element name* (e.g. "pitch") not the canonical substrate name (e.g. "earth"). The canonical substrate name is in `manifest.json` → `season_theme_element` (e.g. "earth"). Drax: use `manifest.json` for substrate-coded accents, `cosmological_vocabulary.json` for slot fills + rationales.

**Shippable-tonight:** YES. Recommend bundling as a static JSON file:
```
reincarnated-loadout/src/data/cosmological-vocabulary.json
# Array of 5 records, one per vs2a season
```
**Transform required:**
```bash
# Generate bundle:
python3 -c "
import json, os
seasons = ['season_002011','season_002012','season_002013','season_002014','season_002015']
base = 'output/standard-demo-regen-2026-05-17'
records = []
for s in seasons:
    cv = json.load(open(f'{base}/{s}/cosmological_vocabulary.json'))
    m = json.load(open(f'{base}/{s}/manifest.json'))
    cv['anchor_name'] = m['anchor']['name']
    cv['canonical_theme_substrate'] = m['season_theme_element']
    records.append(cv)
print(json.dumps(records, indent=2))
" > src/data/cosmological-vocabulary.json
```
**Gaps:** None.

---

### Panel: D1 Vocabulary Corpus Bar (Arc 2)

**Story arc:** Arc 2 — The LLM Thematic Universe
**Data needed:** allow-list / eligible / quarantine counts; optional per-substrate breakdown
**Source-of-record:** `reincarnated-engine/data/seasonal_elements/pool.json`

**Shape today:**
- Total: 156 entries
- allow-list: 60, eligible: 50, quarantine: 46
- Per-substrate (fire: 20/11/1, earth: 22/13/18, water: 11/9/13, wind: 7/17/14)

**Access pattern:**
```bash
python3 -c "
import json
from collections import Counter, defaultdict
d = json.load(open('data/seasonal_elements/pool.json'))
els = d['elements']
print('total:', len(els))
c = Counter(e['d1_status'] for e in els)
print(dict(c))
"
```

**Shippable-tonight:** YES as static constant (counts don't change between regen cycles).
**Transform required:** Transcribe counts into a TS const or small JSON file — no parsing required.
**Gaps:** The "81/40/35" figure in MEMORY.md (2026-05-12) reflects runtime counts after VFX gate auto-demotion at that point in time. Current static counts are 60/50/46. The analytics suite should display the static pool.json counts (60/50/46) labeled as "D1 corpus as-authored." If drax wants the runtime-effective counts, they differ per VFX manifest state — out of scope for tonight.

---

### Panel: Iconic-Verb Chip Grid (Arc 2)

**Story arc:** Arc 2 — The LLM Thematic Universe
**Data needed:** `iconic_verbs[]` per substrate (7 substrates)
**Source-of-record:** `canonical/story/substrate-identity-declarations-2026-05-17.md` (same as Panel 1)

**Shippable-tonight:** YES — same TS const transcription as Panel 1 (shared source).
**Transform required:** Included in substrate TS const transcription.
**Gaps:** None.

---

### Panel: Role × Substrate Matrix (Arc 4)

**Story arc:** Arc 4 — The Diversity Architecture in Action
**Data needed:** Per-class `dominant_element` + `role_orientation` → count per (substrate, role) cell across 5 seasons
**Source-of-record:** `reincarnated-engine/output/standard-demo-regen-2026-05-17/season_*/classes/*.json`

**Shape today:** 51 classes across 5 seasons. Role × substrate matrix as extracted:

| Substrate | control | damage | hybrid | support |
|---|---|---|---|---|
| earth | 2 | 2 | 2 | — |
| fire | 2 | 4 | 4 | — |
| holy | 3 | 2 | — | — |
| lightning | 2 | 3 | — | — |
| physical | 1 | 4 | — | — |
| shadow | 1 | 2 | 2 | — |
| water | 1 | 3 | 6 | — |
| wind | 1 | 1 | 3 | — |
| **Total** | **13** | **21** | **17** | **0** |

Notes: No support classes yet (support gated to multi-actor contexts per design intent). `holy` and `lightning` have no hybrid classes in this 5-season sample. `water` dominates hybrid (6 of 17 hybrid classes).

**Access pattern:**
```bash
python3 -c "
import json, os
from collections import defaultdict
base = 'output/standard-demo-regen-2026-05-17'
matrix = defaultdict(int)
for s in ['season_002011','season_002012','season_002013','season_002014','season_002015']:
    for f in os.listdir(f'{base}/{s}/classes'):
        if not f.endswith('.json'): continue
        c = json.load(open(f'{base}/{s}/classes/{f}'))
        matrix[(c.get('dominant_element','?'), c.get('role_orientation','?'))] += 1
for k in sorted(matrix): print(k, matrix[k])
"
```

**Shippable-tonight:** YES. I've pre-extracted the matrix above; drax can use the table directly as a TS const or generate from the classes JSON.
**Transform required:** Either transcribe the above table as static data, or add a build-time extraction script. The classes.json (root-level per season) contains the same data in array form — faster for drax to query.

**Gaps:** `archetype_tag` field is present in some classes but None in others (partially populated). The role_orientation + dominant_element tuple is the reliable extraction path. `role_orientation` is populated for all 51 classes (confirmed in extraction above).

---

### Panel: Archetype Distribution (Arc 4) — Existing

**Story arc:** Arc 4 — The Diversity Architecture in Action
**Source-of-record:** `useAnalytics.ts` → `archetypeBySeasonRows`, `allArchetypes`
**Shippable-tonight:** YES (reuse — already wired).
**Gaps:** None.

---

### Panel: Modifier Range Chart (Arc 4) — Existing

**Story arc:** Arc 4 — The Diversity Architecture in Action
**Source-of-record:** `useAnalytics.ts` → `modifierRanges`
**Shippable-tonight:** YES (reuse — already wired).
**Gaps:** None. The "hunter 1.82× range" finding from B14.5 sidecar analyses is a valid annotation to add to this chart's title card.

---

### Panel: Season Summary Cards (Arc 5) — Existing

**Story arc:** Arc 5 — The Journey Across Seasons
**Source-of-record:** `useAnalytics.ts` → `seasonSummaryCards`
**Shippable-tonight:** YES (reuse — already wired).
**Gaps:** None.

---

### Panel: Season Timeline Chart (Arc 5) — Existing

**Story arc:** Arc 5 — The Journey Across Seasons
**Source-of-record:** `useAnalytics.ts` → `seasonTimeline`
**Shippable-tonight:** YES (reuse — already wired).
**Gaps:** None.

---

### Panel: Hive Pulse — Dispatches by Purpose (Arc 6)

**Story arc:** Arc 6 — The Work Behind The Work
**Data needed:** Dispatch count by seam + date (last 14 days)
**Source-of-record:** `agentic_orchestration/dispatches/` filenames

**Shape today:** 231 dispatch files. Filename pattern: `<YYYY-MM-DD>-<seam>-<purpose>.md`
Active seams: star-lord (24), drax variants (many), jack-ryan (15), rocket (12), gamora (10), elrond (many), gandalf (many), legolas (many), knight-rider (0 visible), galadriel (2).

**Last 14 days pulse (as-extracted):**
- 2026-05-14: star-lord×3, drax×4, gamora×2, other×1 → 10 total
- 2026-05-16: star-lord×16, drax×21, gamora×10, rocket×9, gandalf×12, elrond×12, legolas×8, jack-ryan×4 → 92 total
- 2026-05-17: rocket×16, drax×36, gandalf×12, jack-ryan×8, legolas×7, gamora×7, elrond×6, star-lord×4 → 96 total
- 2026-05-18: drax×13, gandalf×4, elrond×5, rocket×4, jack-ryan×3, galadriel×2, star-lord×1 → 32 total

**Shippable-tonight:** YES as static export. I recommend generating `hive-summary.json` tonight.

**Transform required:**
```bash
# Run from reincarnated-collaboration root:
python3 -c "
import json, os, re
from collections import defaultdict, Counter

dispatch_dir = 'agentic_orchestration/dispatches'
files = [f for f in os.listdir(dispatch_dir) if f.endswith('.md')]

SEAM_MAP = {
    'star-lord': 'star-lord', 'drax': 'drax', 'rocket': 'rocket',
    'gamora': 'gamora', 'gandalf': 'gandalf', 'jack-ryan': 'jack-ryan',
    'elrond': 'elrond', 'legolas': 'legolas', 'knight-rider': 'knight-rider',
    'galadriel': 'galadriel'
}

by_date_seam = defaultdict(Counter)
for f in files:
    parts = f.replace('.md','').split('-')
    if len(parts) < 4: continue
    date = '-'.join(parts[:3])
    rest = '-'.join(parts[3:])
    seam = 'other'
    for k in SEAM_MAP:
        if rest.startswith(k):
            seam = SEAM_MAP[k]
            break
    by_date_seam[date][seam] += 1

result = {
    'generated_at': '2026-05-18',
    'total_dispatches': len(files),
    'dispatch_pulse': {date: dict(counts) for date, counts in sorted(by_date_seam.items())}
}
print(json.dumps(result, indent=2))
" > src/data/hive-summary-dispatches.json
```

**Gaps (Phase-2):** Dispatches-by-*purpose* (impl vs advisory vs sprint vs scout) requires reading file contents, not just filenames. Tonight: by-seam-by-date. Phase-2: by-purpose requires a content scan.

---

### Panel: Hive Pulse — Commits per Seam (Arc 6)

**Story arc:** Arc 6 — The Work Behind The Work
**Data needed:** Per-commit author (seam), date — across 4 repos
**Source-of-record:** `git log` in engine + loadout + collaboration + demo repos

**Shape today:** Git log is readable from all 4 repos. Seam attribution via commit message prefix (`feat(star-lord):`, `docs(jack-ryan):`, etc.) or author + convention.

**Access pattern:**
```bash
# Engine repo:
cd ~/Games/reincarnated-engine && \
  git log --format="%ad|%s" --date=format:'%Y-%m-%d' --since="2026-05-01" | \
  grep -oP '^\d{4}-\d{2}-\d{2}|\(([a-z\-]+)\)' | head -60
```

**Shippable-tonight:** YES with extraction script (30-45 min effort). The commit message prefix pattern (`feat(seam):`, `docs(seam):`, `chore(seam):`) is consistent across the engine repo. Recommend adding commits-per-seam-per-day to `hive-summary.json`.

**Gaps:** 
- The loadout repo is primarily `mhwetmore` with seam attribution by branch/message prefix (less consistent than engine)
- The reincarnated-demo repo has similar loose attribution
- For tonight: engine repo commits + dispatch filename counts are sufficient to produce the pulse chart

---

### Panel: Team Manifest Card (Arc 6)

**Story arc:** Arc 6 — The Work Behind The Work
**Data needed:** 8 (9) agent names + one-line role descriptions
**Source-of-record:** `agentic_orchestration/AGENTS.md`

**Shippable-tonight:** YES — static TS const. Contents from AGENTS.md: star-lord, rocket, gamora, drax, elrond, gandalf, jack-ryan, knight-rider, galadriel (pending Matt L3 activation).
**Transform required:** Hand-transcribe from AGENTS.md → TS const.
**Gaps:** None.

---

### Panel: Featured Sprint Card (Arc 6)

**Story arc:** Arc 6 — The Work Behind The Work
**Data needed:** Static prose about tonight's overnight sprint
**Source-of-record:** `agentic_orchestration/gandalf/requests/2026-05-18-knight-rider-mobile-playable-analytics-visual-benchmark-sprint.md`

**Shippable-tonight:** YES — drax authors static prose card. No data extraction needed.
**Gaps:** None.

---

## § 3 — Recommended output shape for drax

### 3.1 — Bundle structure

I recommend these static data files in `reincarnated-loadout/src/data/`:

```
src/data/
  substrates.ts              # 7 substrate identity records (TS const — hand-transcribed from canonical/story)
  cosmological-vocabulary.json  # 5 vs2a season cosmological vocab records (generated by extraction script)
  d1-corpus-summary.json     # D1 counts (allow-list/eligible/quarantine by substrate) — static
  role-substrate-matrix.json # Role × substrate counts from 5-season extraction — static
  hive-summary.json          # Dispatch pulse by seam/date + commit pulse (generated script)
```

These files are **generated once per batch** from engine artifacts and checked into the loadout repo. They do NOT require the loadout app to query the engine at runtime.

### 3.2 — Recommended hook

```typescript
// reincarnated-loadout/src/hooks/useTheWorkData.ts
// Mirror of useAnalytics.ts pattern
// Imports static JSON bundles + the substrate TS const
// Exposes typed data to TheWork.tsx page
```

### 3.3 — Data that already exists in useAnalytics.ts (DO NOT re-source)

These are wired and should be consumed via the existing hook:
- `archetypeBySeasonRows` — Arc 4 archetype distribution
- `modifierRanges` — Arc 4 modifier ranges
- `seasonSummaryCards` — Arc 5 season cards
- `seasonTimeline` — Arc 5 timeline
- `allSubstrates`, `allArchetypes` — Arc 1/4 substrate counts

---

## § 4 — Telemetry tables relevant to analytics suite

The analytics suite consumes **artifact JSON files** for vs2a seasons (not telemetry, which lacks them). The telemetry DB is relevant for:

1. **Historical LLM cost data** (if Arc 6 exposes "total AI spend to date"): `llm_calls` table. Total: 3,181 calls, $8.28 total across seasons 000093–001010.
   ```sql
   SELECT SUM(estimated_cost_usd), COUNT(*) FROM llm_calls;
   -- $8.28, 3181 calls
   ```
2. **Historical season analytics** (legacy pre-vs2a): 25 seasons in the DB, enriching Arc 5's "journey" if the timeline reaches back before vs2a.
3. **NOT useful for vs2a seasons**: seasons 002011-002015 have zero records in any telemetry table. Confirmed.

---

## § 5 — Known telemetry gaps (for Phase-2 awareness)

These are documented gaps from the B14.5 sidecar analysis — not blocking tonight's suite, but informing the Phase-2 roadmap:

| Gap | Table | % NULL | Impact |
|---|---|---|---|
| `engine_version` | `seasons` | 64% (16 of 25 show "unknown") | Cannot correlate season behavior to engine version |
| `convergence_wall_time_seconds` | `classes` | 75% (197 of 261 NULL) | Cannot report convergence time per archetype |
| `seasonal_element_name` | `classes` | 80% (209 of 261 NULL/empty) | Cannot link class to its seasonal element |
| `termination_reason` | `class_fight_loadouts` | Unknown (not checked tonight) | Cannot distinguish timeout vs death outcomes |

These gaps affect the pre-vs2a telemetry records. The vs2a seasons have no telemetry records at all (a different and larger gap). Phase-2 resolution requires Matt authorization per ADR-006.

---

## § 6 — Phase-2 items (engine-side)

| # | Item | Why deferred | Phase-2 path |
|---|---|---|---|
| P2-E1 | vs2a seasons in telemetry | vs2a regen ran without telemetry write-through; backfill requires ADR-006 authorization + schema migration | Matt approves; star-lord writes backfill script; ~1 session |
| P2-E2 | hive-summary.json — dispatches by purpose | Requires content scan of 231 MD files | Add purpose-tag metadata to dispatch headers; star-lord aggregates in next sprint |
| P2-E3 | Full git commit pulse (all 4 repos) | Demo/loadout commit attribution is inconsistent; engine is clean | Normalize commit message conventions; revisit after B-series |
| P2-E4 | D1 per-entry detailed browser | 156 entries viewable in a table with per-entry metadata | Simple table component; ship when per-entry detail adds value |
| P2-E5 | LLM cost for vs2a seasons | Not tracked in telemetry (vs2a regen ran outside tracked calls) | Resolve P2-E1 first |

---

## § 7 — Hive log pre-signal (§ 14.1.1)

**STATE:** Star-lord engine-side data manifest complete. Manifest doc landed at `agentic_orchestration/research/curated/loadout-analytics-data-manifest-2026-05-18.md`. Unblocks elrond catalogue-side append (their section will be added below) and drax implementation dispatch. No new code written tonight; dispatch was survey + doc authorship.

**Next actions for drax (after elrond appends):**
1. Transcribe substrate identity records → `src/data/substrates.ts`
2. Run cosmological vocabulary extraction script → `src/data/cosmological-vocabulary.json`
3. Transcribe role × substrate matrix (§ 2, Panel 4) → static const or JSON
4. Run hive dispatch pulse extraction → `src/data/hive-summary.json`
5. Transcribe D1 corpus counts → `src/data/d1-corpus-summary.json`
6. Wire `useTheWorkData.ts` hook consuming these files
7. Build `TheWork.tsx` page per gandalf IA § 2/3/6

---

## § 8 — Elrond append section (to be added)

*Elrond's catalogue-side section follows here. Star-lord has completed the engine-side half.*

---

*Authored 2026-05-18 by star-lord per dispatch `2026-05-18-star-lord-loadout-analytics-data-manifest-engine-side.md`. Survey-mode: reported what exists; gaps labeled explicitly; no aspirational data interleaved with actual.*
