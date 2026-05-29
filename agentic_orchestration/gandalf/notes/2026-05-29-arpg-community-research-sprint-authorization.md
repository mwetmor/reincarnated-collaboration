# ARPG Community Research Sprint — Authorization + Execution Dispatch

> **STATUS:** OPERATIONAL (firing 2026-05-29 evening late) — Matt 2026-05-29 evening late: "let's hold off on the canonical write up for now, but please draft and immediately fire the full research and DB creation insertion!" Sprint fires in parallel with cascade-resumption-3 (KR-coordinated) per Amendment 2/3 RAM-awareness retirement.

**Date:** 2026-05-29 evening late
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-05-29 evening late ("draft and immediately fire") + multi-turn empirical scouting + principle doc 2026-05-29 evening + Layer 2 cross-site vocabulary verification (6 sites confirmed)

**Companion docs:**
- `canonical/story/2026-05-29-designer-writes-substrate-player-names-experience-principle.md` — foundational principle Layer 1/2/3 architecture; this sprint = empirical-validation instrument for Layer 2
- `canonical/story/2026-05-29-experiential-cascade-architecture-recognition.md` § 3 gate (ii) — this sprint executes gate (ii) at expanded scope
- `agentic_orchestration/gandalf/notes/2026-05-29-legolas-mode-a-arpg-archetype-vocabulary-research-brief.md` — predecessor brief; superseded by this expanded-scope dispatch

---

## 0. TL;DR — Goal + Scope

**Sprint mission:** acquire research-grade ARPG community vocabulary + structured-data corpus across 8-12 sites; build SQLite database; analyze cross-site convergence + composite-archetype patterns + multi-layer loot substrate vocabulary; produce axis-discovery verdict + engine integration design memo.

**Scope expansions over prior brief (per multi-turn 2026-05-29 evening scouting):**
- **Multi-layer vocabulary discovery** (per Matt loot substrate corrections): character-substrate + content-instance-substrate + atlas/meta + augmentation + season-mechanic layers
- **Composite-vs-single-axis archetype critique** (per Matt designer-restriction observation): empirically validate whether community-emergent archetypes are restrictive composites or open single-axis selections
- **Maxroll feature vector schema** (per empirical deep-dive on Whirlwind Barb + Bone Spear Necro): Layer A-E feature vector schema for structured extraction
- **Magic Find morph documentation** (per Matt sub-axis correction): Magic Find preserved as gear-stat/sub-axis; NOT primary archetype in modern ARPGs

**Total estimated effort:** ~3-5d wall-clock; fires in parallel with cascade-resumption-3 close per Amendment 2/3 retired R48.4

---

## 1. Database design — separate SQLite per prior architecture decision

**Path:** `agentic_orchestration/research/arpg-community-axes-2026-05-29/research.db`

**Why separate SQLite (not engine-substrate DB):** different schema + lifecycle + ownership; clean separation; future Pi-Postgres migration easier when that infrastructure lands.

**Schema (empirically-derived from Maxroll deep extractions + cross-site scouting):**

```sql
-- Build identity (per-build root record)
CREATE TABLE builds (
  build_id INTEGER PRIMARY KEY AUTOINCREMENT,
  source_site TEXT NOT NULL,      -- maxroll_d4 / maxroll_poe / maxroll_le / maxroll_poe2 / icy_veins_d4 / poe_vault / poe_ninja / etc.
  source_url TEXT NOT NULL,
  game TEXT NOT NULL,             -- d4 / poe / poe2 / le
  class_or_ascendancy TEXT,       -- Barbarian / Necromancer / Hierophant / Stormweaver / Druid / etc.
  primary_skill TEXT,             -- Whirlwind / Bone Spear / Cyclone / etc.
  season_or_league TEXT,          -- Season 13 / 3.25 Settlers / etc.
  build_name TEXT,                -- full build name as published
  tagline TEXT,                   -- "Spin to Win" / etc.
  author TEXT,
  last_updated TEXT,
  archived_status BOOLEAN DEFAULT 0,
  acquired_at TEXT DEFAULT (datetime('now')),
  UNIQUE (source_site, source_url)
);

-- Layer 2 — STRUCTURED player-experience rating (Maxroll 5-axis or equivalent)
CREATE TABLE build_ratings_structured (
  build_id INTEGER REFERENCES builds(build_id),
  axis_name TEXT NOT NULL,        -- push / speed / bossing / survivability / playability / OR site-specific axis name
  rating_value TEXT,              -- Strong / Excellent / Moderate / Weak / Difficult OR numerical
  rating_normalized REAL,         -- 0.0-1.0 normalized (Strong=0.8, Excellent=1.0, Moderate=0.5, Weak=0.2, Difficult=0.3 for playability inverse)
  PRIMARY KEY (build_id, axis_name)
);

-- Layer 2 — FREE-TEXT pros/cons tags
CREATE TABLE build_pros_cons (
  pc_id INTEGER PRIMARY KEY AUTOINCREMENT,
  build_id INTEGER REFERENCES builds(build_id),
  polarity TEXT NOT NULL,         -- pro / con
  text_tag TEXT NOT NULL,         -- "Incredible AoE Clear" / "Resource Intensive" / etc.
  normalized_concept TEXT         -- aoe_clear / resource_intensive / etc. (gandalf+elrond normalizes for analysis)
);

-- Layer 2 — Activity / content-tier tags
CREATE TABLE build_activities (
  act_id INTEGER PRIMARY KEY AUTOINCREMENT,
  build_id INTEGER REFERENCES builds(build_id),
  activity_name TEXT NOT NULL,    -- bossing / speedfarming / pit / helltide / mapping / heist / sanctum / monolith / etc.
  content_tier_claim TEXT,        -- "Pit 125" / "Tower 140+" / "Mephisto 2-3s" / etc.
  activity_layer TEXT             -- primary_archetype / content_instance / game_specific
);

-- Layer 2 — Variants (progression × activity × mechanic)
CREATE TABLE build_variants (
  var_id INTEGER PRIMARY KEY AUTOINCREMENT,
  build_id INTEGER REFERENCES builds(build_id),
  variant_name TEXT,              -- "Speedfarm Overpower" / "Push Overpower" / etc.
  progression_stage TEXT,         -- starter / midgame / endgame
  activity_focus TEXT,            -- speedfarm / push / bossing
  mechanic_focus TEXT             -- overpower / crit / dot / etc.
);

-- Layer 1 — Skills (substrate-mechanical)
CREATE TABLE build_skills (
  skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
  build_id INTEGER REFERENCES builds(build_id),
  skill_name TEXT NOT NULL,       -- Whirlwind / Bone Spear / War Cry / etc.
  skill_role TEXT,                -- core / amp / defense / resource / mobility / cc / grouping
  order_position INTEGER,         -- skill order in the build
  notes TEXT
);

-- Layer 1 — Gear (substrate-mechanical)
CREATE TABLE build_gear (
  gear_id INTEGER PRIMARY KEY AUTOINCREMENT,
  build_id INTEGER REFERENCES builds(build_id),
  gear_slot TEXT,                 -- helm / chest / gloves / weapon / amulet / ring / etc.
  item_name TEXT NOT NULL,        -- Gohr's Devastating Grips / Mageblood / etc.
  item_type TEXT,                 -- unique / aspect / charm / set / rare / etc.
  is_required BOOLEAN,            -- core vs nice-to-have
  notes TEXT
);

-- Layer 1.5 — Stat targets (player-validated substrate thresholds)
CREATE TABLE build_stat_targets (
  stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
  build_id INTEGER REFERENCES builds(build_id),
  stat_name TEXT NOT NULL,        -- crit_chance / attack_speed / life / armor / resistance / movement_speed / etc.
  target_value REAL,              -- 100 / 7000 / 80000 / etc.
  target_unit TEXT,               -- pct / hp / armor_value / etc.
  priority_tier INTEGER,          -- 1 (essential) / 2 (important) / 3 (nice-to-have)
  notes TEXT
);

-- Layer 2 — Performance claims (empirical content-tier achievement)
CREATE TABLE build_performance_claims (
  claim_id INTEGER PRIMARY KEY AUTOINCREMENT,
  build_id INTEGER REFERENCES builds(build_id),
  claim_type TEXT,                -- content_depth / clear_time / kill_time / dps_estimate
  claim_value TEXT,               -- "Pit 125" / "2-3 seconds" / "10 million DPS" / etc.
  content_context TEXT
);

-- Layer 2 — Summary / flavor text
CREATE TABLE build_summary (
  build_id INTEGER PRIMARY KEY REFERENCES builds(build_id),
  summary_text TEXT,
  descriptors_extracted TEXT      -- JSON array: ["relaxed", "fast-paced", "machine-gun", "tactical-genius", etc.]
);

-- Multi-layer loot substrate vocabulary (per Matt sub-axis correction)
CREATE TABLE loot_substrate_vocabulary (
  vocab_id INTEGER PRIMARY KEY AUTOINCREMENT,
  source_site TEXT,
  game TEXT,
  layer TEXT,                     -- character_substrate / content_instance / atlas_meta / augmentation / season_mechanic
  term TEXT NOT NULL,             -- "Magic Find" / "IIQ" / "Item Rarity" / "Currency Find" / "Scarab" / etc.
  layer_role TEXT,                -- gear_stat / map_mod / atlas_node / scarab_strat / season_mechanic / etc.
  notes TEXT
);

-- Cross-site vocabulary convergence (analytical output)
CREATE TABLE vocabulary_convergence (
  conv_id INTEGER PRIMARY KEY AUTOINCREMENT,
  concept TEXT NOT NULL,          -- "Bossing" / "Speedfarming" / "Magic Find sub-axis" / etc.
  layer TEXT,                     -- primary_archetype / sub_axis / stat_affix
  sites_observed_count INTEGER,
  sites_list TEXT,                -- JSON array of source_sites
  convergence_strength TEXT,      -- STRONG / MODERATE / WEAK / NO
  vocabulary_variants TEXT,       -- JSON array of equivalent terms across sites
  notes TEXT
);

-- Index for cross-site pattern queries
CREATE INDEX idx_builds_site ON builds(source_site, game);
CREATE INDEX idx_builds_class ON builds(class_or_ascendancy);
CREATE INDEX idx_activities_name ON build_activities(activity_name);
CREATE INDEX idx_ratings_axis ON build_ratings_structured(axis_name);
CREATE INDEX idx_stat_targets_name ON build_stat_targets(stat_name);
CREATE INDEX idx_vocab_concept ON vocabulary_convergence(concept);
```

---

## 2. Source prioritization

**Tier 1 — High-density, WebFetch-accessible (legolas Mode B; HTML crawl):**
- Maxroll D4 build guides (sample 30-50 builds)
- Maxroll PoE build guides (sample 20-30)
- Maxroll Last Epoch build guides (sample 20-30)
- Maxroll PoE2 build guides (sample 15-25)
- PoE-Vault build guides (sample 20-30)

**Tier 2 — Requires proper HTTP tooling (legolas Mode B; possibly via WebFetch on specific URLs):**
- Icy-Veins D4 builds (URL pattern requires discovery)
- Icy-Veins PoE builds (same)
- Wowhead D4 builds (URL pattern requires discovery)
- Mobalytics D4 builds (403 on root; try specific URLs)
- D4Builds.gg (404 on /builds; try specific class URLs)

**Tier 3 — Structured data / API (legolas Mode B; specialized endpoints):**
- PoE Ninja `/poe1/data` data dumps endpoint
- PoE Ninja per-build profile pages (top builds per league)
- PoE Wiki via MediaWiki API
- Reddit ARPG subreddits via Reddit JSON API (where accessible)

**Tier 4 — Selective sampling (post-Tier-1/2/3):**
- YouTube ARPG content creator video titles + descriptions
- Twitch ARPG creator stream titles
- Steam Community Guides top-rated ARPG guides
- D2 legacy sites (Diabloii.net) for Magic Find historical baseline

**Sample size target: ~150-250 build records across Tier 1-3; sufficient for cross-site convergence test + pattern recognition.**

---

## 3. Sub-agent role assignment

| Agent | Role | Mode | Dispatch authority |
|---|---|---|---|
| **gandalf** (in conversation thread) | Authorization authoring + synthesis + axis-discovery verdict + engine integration design memo | n/a (in-thread) | Matt 2026-05-29 evening late |
| **legolas Mode B** (catalogue crawl) | Mass acquisition: Tier 1 + Tier 2 + Tier 3 source crawling; structured data extraction per schema | Mode B | gandalf-authored dispatch this batch |
| **legolas Mode A** (analytical research) | Cross-site vocabulary convergence test; categorical-flag taxonomy synthesis; composite-vs-single-axis empirical assessment; multi-layer loot substrate vocabulary analysis | Mode A | gandalf-authored dispatch this batch |
| **elrond** (catalogue DB + abstraction analysis) | Schema validation + stat-target clustering + pattern recognition on combined feature vector + per-archetype distinguishing-signature emergence | n/a (called post-Mode-B) | gandalf-authored dispatch deferred to post-acquisition |

---

## 4. Phased plan

**R1 — Authorization + DB init (gandalf in-thread; ~30min):**
- ✅ This artifact (authorization)
- ✅ DB initialized at `agentic_orchestration/research/arpg-community-axes-2026-05-29/research.db`
- ✅ Schema applied from § 1 spec
- ✅ Sub-agent dispatches authored + fired

**R2 — Mass acquisition (legolas Mode B; ~1-2d wall-clock):**
- Tier 1 + Tier 2 + Tier 3 crawling
- Insert into SQLite per schema
- Acquisition log at `agentic_orchestration/research/arpg-community-axes-2026-05-29/acquisition-log.md`

**R3 — Analysis (legolas Mode A + elrond; ~1-2d wall-clock):**
- Cross-site vocabulary convergence test (legolas Mode A primary)
- Composite-vs-single-axis empirical assessment (legolas Mode A)
- Multi-layer loot substrate vocabulary extraction (legolas Mode A)
- Stat-target clustering + pattern recognition (elrond)
- Output: analysis-findings.md

**R4 — Synthesis + verdict (gandalf in-thread; ~0.5-1d):**
- Axis-discovery verdict (input axes + output axes + cross-site convergence per axis)
- Engine integration design memo (Layer 1/2 mapping; cohort_archetype Disc #41 revisit candidate)
- Composite-archetype-emergence pattern (verify Matt's restriction-critique empirically)
- Output: verdict.md + engine-integration-design-memo.md

**Total: ~3-5d wall-clock; fires in parallel with cascade-resumption-3 close**

---

## 5. Output deliverables

1. **Populated SQLite DB** at `agentic_orchestration/research/arpg-community-axes-2026-05-29/research.db`
2. **Acquisition log** (legolas Mode B)
3. **Analysis findings** (legolas Mode A + elrond)
4. **Axis-discovery verdict** (gandalf synthesis): input axes + output axes + convergence per axis
5. **Engine integration design memo** (gandalf): Layer 1/2 mapping + cohort_archetype revisit + Cycle 15+ candidate recommendations
6. **Composite-archetype empirical assessment**: whether community-emergent archetypes are open single-axis or designer-restricted composites (per Matt critique)

---

## 6. Composition with cascade-resumption-3

**Parallel fire enabled per Amendment 2/3 retired R48.4.** Sprint sub-agents (legolas Mode A + Mode B + elrond) fire alongside KR-coordinated cascade-resumption-3 work (rocket S6a-FIX + gamora Phase 7 bridge fix + jack-ryan Gate-2 + Phase 5 Matt-gate + cascade A2-2 → A2-7).

**No resource conflict:** sprint sub-agents and cascade sub-agents are different seams. KR coordinates cascade; gandalf coordinates sprint.

**Sprint findings feed Cycle 15+ post-A2-7:**
- Doc 52 promotion (experiential archetype dimension as load-bearing architecture)
- Doc 38 amendment (engine commercial framing refinement)
- Wave A + Wave B Cycle 15+ prompt extension (player-experience layer integration)
- cohort_archetype Disc #41 revisit (community-vocabulary-validated cohort mapping)
- Spirit-guide content layer (player-facing narrative with player-experience axes)

---

## 7. Cost projection

LLM token cost across sub-agent dispatches:
- legolas Mode B mass acquisition: ~10-30K tokens per source × ~10 sources = ~100-300K tokens; ~$3-10
- legolas Mode A vocabulary convergence: ~50-100K tokens; ~$2-5
- elrond pattern recognition: ~30-50K tokens; ~$1-3
- gandalf synthesis: minimal (in-thread)

**Total estimated sprint LLM cost: ~$6-18.** Separate from cascade-resumption-3 $50 soft cap (different LLM budget; not within Phase A2 Matt 3-gate Gate (b) scope).

---

## 8. Risk register

| Risk | Mitigation |
|---|---|
| Tier 2 sites (Mobalytics / D4Builds / Wowhead / Icy-Veins-deep) need URL discovery | legolas Mode B with site-mapping + URL pattern inference |
| Reddit JSON API may be rate-limited | sample strategically; defer to Tier 3 if blocked |
| Cross-site schema variance | unified schema absorbs variance; per-site extraction adapters |
| Composite-vs-single-axis empirical signal ambiguous | multi-layer vocabulary capture surfaces the dimensions even if labels overlap |
| Magic Find morph vocabulary scattered across stat-affix vs sub-axis vs strategy layer | dedicated loot_substrate_vocabulary table with layer field |

---

## 9. Sign-off

**Authored:** gandalf (story-and-design steward) per Matt 2026-05-29 evening late directive "draft and immediately fire"

**For:** the operational sprint authorization + DB schema + sub-agent dispatch coordination for the ARPG community research sprint; empirical-validation instrument for the experiential cascade architecture recognition record gate (ii) at expanded multi-layer scope + composite-archetype-emergence critique (Matt 2026-05-29 evening late)

**Immediate fire actions (this batch):**
1. Authorization artifact (this doc)
2. SQLite DB init at `agentic_orchestration/research/arpg-community-axes-2026-05-29/research.db`
3. legolas Mode B dispatch fired (mass acquisition)
4. legolas Mode A dispatch fired (vocabulary convergence + composite-vs-single-axis assessment + multi-layer loot substrate)
5. KR notified (sprint fires in parallel; no cascade-resumption-3 interference)
