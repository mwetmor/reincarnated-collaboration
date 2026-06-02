# EAA-3 + EAA-4 — Joint elrond-side spec (ingest-compat + chronicle storage)

**Date:** 2026-06-02
**Author:** elrond (data steward; LOCK K + LOCK E seam authority)
**Pattern:** Pattern A-deep — substantive cross-dispatch schema verdict
**Composes:** EAA-3 (per-kit output schema; rocket primary; elrond co-owner) + EAA-4 (chronicle infrastructure; elrond primary; star-lord co-owner)
**Authority:** Matt 2026-06-02 + Locks A-P (LOCK K active; ADDITIVE-AND-REVERSIBLE per LOCK J)
**Routed by:** knight-rider
**Composes with:** `canonical/story/2026-06-02-season-archive-realm-expansion-pivot.md` § 3.3 + § 3.4 (binding)

---

## 0. TL;DR

This note locks the elrond-side decisions for the two composed dispatches (EAA-3 + EAA-4) BEFORE either schema spec finalizes. Three coupled decisions:

1. **`kit_id` format:** `kit_<primary>_<seq6>` (e.g., `kit_shadow_000001`); stable permanent identifier; primary-element-grouped; text-sortable.
2. **`kit_space_expansion_event_id` format (FK shared with EAA-4):** `kse_<YYYYMMDD>_<seq3>` (e.g., `kse_20260602_001`); SEQ-3 canonical per `reincarnated-engine/data/kit_space/chronicle/CHRONICLE_SCHEMA.md` § 3 + MIGRATION v1.9 (the prior `eaa-3-eaa-4-coordination` UUID-hex draft has been SUPERSEDED and redirects to this joint spec); chronological at day-granularity (lexical sort = chronological sort) with HHMMSS-precise emit-time preserved separately via `event_timestamp` field; future-extensible event_type prefix space (`re_` realm-expansion reserved).
3. **Chronicle storage medium:** Option α (flat JSON at `data/kit_space/kit_space_chronicle.json`) as source of truth + Option β-light (shadow tables `engine_kit_index` + `engine_kit_space_events` in curated catalogue.db) as derived-and-rebuildable analytical index.

elrond ingest-compat: **CONFIRMED.** Per-kit JSON entries are filesystem-addressable; shadow tables are additive (LOCK J ADDITIVE-AND-REVERSIBLE); ingest pipeline is a directory-walk + insert/upsert (substrate DB extension authored additively per LOCK K).

---

## 1. Foreign-key format lock (the cross-dispatch coordination item)

Per Phase 1 batch Gate-1 finding amendment 2 (jack-ryan): **rocket + elrond MUST coordinate `kit_space_expansion_event_id` format JOINTLY before either EAA-3 or EAA-4 finalizes spec.**

**AUTHORITATIVE FORMAT NOTE:** SEQ-3 (`kse_<YYYYMMDD>_<seq3>`) is the canonical FK format, sourced from `reincarnated-engine/data/kit_space/chronicle/CHRONICLE_SCHEMA.md` § 3 + `agentic_orchestration/research/curated/MIGRATION.md` v1.9 (smoke 9/9 PASS). An earlier coordination draft at `agentic_orchestration/cycle-16-eaa-engine-architectural-amendment/eaa-3-eaa-4-coordination/event-id-foreign-key-format-2026-06-02.md` proposed a UUID-hex alternative (`kse_<YYYYMMDD>_<HHMMSS>_<6char-hex>`); that draft has been SUPERSEDED and now redirects to this joint spec. This § 1 restates the SEQ-3 lock for joint-spec reading convenience; jack-ryan Gate-2 BLOCK 2026-06-02 confirmed SEQ-3 as canonical and triggered this amendment to retire the UUID-hex documentation drift.

### 1.1 Format (SEQ-3; canonical per CHRONICLE_SCHEMA.md § 3 + MIGRATION v1.9)

```
kse_<YYYYMMDD>_<seq3>
```

- `kse` — event-type namespace prefix; 3 chars; lowercase (`kse` = kit-space-expansion; future-extensible: `re_` reserved for realm-expansion per canonical record § 3.4)
- `_` — separator
- `YYYYMMDD` — UTC date of event-fire (8 chars; zero-padded; ISO basic format)
- `_` — separator
- `seq3` — within-day zero-padded 3-digit sequence (`001`–`999`; first event of day = `001`)

**Example:** `kse_20260602_001`

**Total length:** 16 chars (fixed). Lexical sort = chronological sort (by day, then by within-day sequence).

**Regex:** `^kse_\d{8}_\d{3}$`

**Construction:** `kse_` + `YYYYMMDD` (UTC date) + `_` + zero-padded 3-digit within-day sequence.

### 1.2 Rationale (SEQ-3; mirrors CHRONICLE_SCHEMA.md § 3)

- **Sequence query at emit-time** — `prior_today_count + 1` queried against the chronicle at event-fire; deterministic, single-source-of-truth, no distributed-minting concern (events fire sequentially from the engine; not a distributed system).
- **999/day bound** — three-digit within-day sequence supports up to 999 kit-space-expansion events per UTC day; sufficient for foreseeable kit-space-expansion event cadence (canonical pivot anticipates expansion events at parameter-scope-amendment cadence, NOT per-kit cadence).
- **Human-inspectable ordering** — reading `kse_20260602_001` immediately tells the inspector when the event fired and its within-day ordinal; lexical sort = chronological sort within a day.
- **Decoupled from engine SHA** — engine sha goes in a separate field (`engine_version_sha`); two-axis provenance preserved.
- **Future-extensible** — `kse_` event-type prefix lets future event types (realm-expansion `re_`, etc.) coexist without renaming.
- **Defense-in-depth FK integrity** — the prefix in the id-itself encodes the event-type fact; a per-kit JSON FK that ever points to a non-`kse_` event is immediately flagged by regex validation.
- **Sub-day chronological precision** — within-day sequence is at day-granularity ordinal precision; emit-time HHMMSS precision is preserved separately via the `event_timestamp` (ISO-8601 UTC) field on the chronicle entry. SEQ-3 is the ordering id; `event_timestamp` is the precise wall-clock.
- **Composes with CHRONICLE_SCHEMA.md § 5 emit-order discipline** — chronicle entry FIRST → per-kit JSON SECOND; atomic `.tmp` → `os.replace` write convention ensures the FK target exists before any per-kit JSON references it.

### 1.3 Generation rule (engine-side; rocket + star-lord implementation; canonical per CHRONICLE_SCHEMA.md § 3)

```python
def mint_kit_space_expansion_event_id(event_date_utc, prior_today_count: int) -> str:
    seq = prior_today_count + 1
    return f"kse_{event_date_utc.strftime('%Y%m%d')}_{seq:03d}"
```

`prior_today_count` is queried from chronicle at emit-time (count of existing events with same `event_date_utc`). First event of day = `001`.

Same construction MUST be used by both:
- EAA-4 chronicle emit path (engine fires expansion event → queries chronicle for `prior_today_count` → mints id → writes chronicle entry)
- EAA-3 per-kit emit path (each kit references the SAME id minted at expansion-event-start; NOT re-minted per kit)

**Emission order:** event_id minted FIRST (at expansion-event start) → chronicle entry appended FIRST → per-kit JSONs emitted SECOND, each carrying the minted `kit_space_expansion_event_id`. Atomic `.tmp` → `os.replace` per CHRONICLE_SCHEMA.md § 5.2.

### 1.4 Cross-seam contract

This is the **single foreign-key value** linking EAA-3 per-kit JSON entries to EAA-4 chronicle entries. Format LOCKED (SEQ-3) per CHRONICLE_SCHEMA.md § 3 + MIGRATION v1.9. Schema spec on both sides MUST use this exact format; jack-ryan Gate-2 will verify against the regex `^kse_\d{8}_\d{3}$`.

### 1.5 Companion field on chronicle entry

SEQ-3 form uses **only** the `event_id` field on chronicle entries; no companion UUID is minted or stored. The prior UUID-hex companion (`event_uuid`) was UUID-hex-form-specific and does not apply under SEQ-3.

Precise wall-clock timing is preserved separately via the `event_timestamp` (ISO-8601 UTC) field on the chronicle entry per CHRONICLE_SCHEMA.md § 4.2 — SEQ-3 carries the within-day ordinal, `event_timestamp` carries the HHMMSS-precise fire time. Two-field decomposition (ordinal id + precise timestamp) is cleaner than packing both into the id.

Shadow table `engine_kit_space_events` accordingly does NOT require an `event_uuid_full` column; `event_id` (PK) + `event_timestamp` cover the provenance surface.

---

## 2. `kit_id` format lock

### 2.1 Format

```
kit_<primary>_<seq6>
```

- `kit` — prefix for kit type; 3 chars; lowercase; reserves namespace for future asset types (e.g., `mob_`, `gear_`, `realm_`)
- `_` — separator
- `<primary>` — canonical-7+1 primary element (lowercase: `fire`, `water`, `earth`, `wind`, `lightning`, `holy`, `shadow`, `physical`)
- `_` — separator
- `<seq6>` — per-primary zero-padded sequence (6 digits; supports up to 999,999 kits per primary; ample for project lifetime)

**Examples:**
- `kit_shadow_000001` — first shadow-primary kit ever generated
- `kit_fire_000042` — 42nd fire-primary kit
- `kit_physical_000007` — 7th physical-primary kit

**Total length:** varies 17-22 chars (depends on primary name length); column-friendly; grep-friendly.

### 2.2 Why per-primary sequence (not global monotonic)

Per canonical record § 3.3, kits are continuously addressable. Primary element is the load-bearing identity dimension (Q18 lock + canonical-7+1 catalog). Per-primary numbering:

- Makes primary distribution legible at-a-glance (count shadow kits by max seq; instant cardinality query)
- Supports natural lexicographic grouping in directory listings
- Decouples primary-kit-counts from each other (adding 50 fire kits doesn't renumber shadow kits)
- Survives parameter-expansion-event interleaving (different events may add kits across multiple primaries; each primary's sequence advances independently)

### 2.3 Why NOT season-numbered, NOT UUID

- **Season-numbered (rejected):** canonical pivot retires seasons; kit_ids must outlive the season concept.
- **UUID (rejected):** opaque; no human-debuggability; loses primary-element signal at first glance.
- **Composite-hash (rejected):** brittle if substrate inputs are renamed; not stable.

### 2.4 Generation rule (engine-side; rocket implementation)

```python
def mint_kit_id(primary: str, prior_primary_count: int) -> str:
    """
    primary: canonical-7+1 primary element name (lowercase)
    prior_primary_count: number of kits with this primary already minted (substrate query)
    """
    assert primary in {"fire", "water", "earth", "wind", "lightning", "holy", "shadow", "physical"}
    seq = prior_primary_count + 1
    return f"kit_{primary}_{seq:06d}"
```

**Per-primary counter source:** engine queries kit space directory (or shadow DB index) for `count(kit_id) where primary_element = <primary>` immediately before minting; first kit of primary = 000001. LOCKED at mint; never re-minted.

---

## 3. Chronicle storage medium decision (LOCK K seam authority)

### 3.1 Decision: Option α (source-of-truth) + Option β-light (analytical shadow)

**Option α — `data/kit_space/kit_space_chronicle.json`** (filesystem source-of-truth):
- Single flat JSON file; append-only entry list; chronological order by event_id
- Parallels pool.json v1.1 pattern (substrate-truth lives in a flat JSON file under `data/`)
- Engine writes on event-fire; drax + EAA-7 reads on engine-page render
- Git-versioned; trivially diffable; recoverable from git history
- No external DB dependency for the source-of-truth surface

**Option β-light — curated catalogue.db shadow tables** (analytical index):
- `engine_kit_index` — per-kit row indexed by kit_id (denormalized projection of per-kit JSON for fast queries)
- `engine_kit_space_events` — per-event row indexed by event_id (denormalized projection of chronicle entries)
- Both REBUILDABLE from filesystem (truncate + reload from JSON files; deterministic)
- Live in elrond's curated DB (NOT in engine's data/ tree); engine remains read-only on this surface
- Powers cross-cutting analytical queries elrond needs: e.g., "join kit_id to substrate_provenance to cultural_tradition" — joins that engine doesn't perform but elrond's analytical workstreams do

### 3.2 Why both (not either-or)

- **Engine ownership separation (ADR-006):** engine owns its emitted artifacts (data/kit_space/); elrond owns analytical curated layer (catalogue.db). Mirroring kit data into elrond's curated DB DOES NOT muddy ownership — the source-of-truth stays in engine; elrond holds a derived rebuildable index.
- **Query patterns differ:** engine + drax fetch by kit_id (single-key lookup); elrond + future analytical workstreams need cross-cutting joins (count by primary x cultural_tradition x period; substrate-provenance audit; chronicle-event correlation against substrate ingest timeline). SQL > JSON-walk for the analytical surface.
- **Reversibility (LOCK J):** shadow tables can be DROPPED at any time without affecting engine; engine can regenerate filesystem any time without affecting elrond shadow. Round-trip clean.
- **Smoke-test friendly:** rebuild from filesystem is a deterministic operation; elrond can verify ingest correctness by truncate-and-reload, then compare row counts to filesystem kit count.

### 3.3 Rejected alternatives

| Option | Rejected because |
|---|---|
| Per-event JSON file in `kit_space_events/` directory (γ from EAA-4 § 3.2) | Adds filesystem hops for chronicle reads; engine page render becomes N-fetches instead of 1 |
| Pure substrate DB extension table (β-only; no filesystem chronicle) | Violates engine self-containment; engine becomes dependent on elrond DB for chronicle truth; cross-repo dependency hazard |
| Filesystem only (α-only; no shadow tables) | Forces elrond analytical work to walk JSON files at every query; cross-cutting joins become impractical |
| In-engine SQLite chronicle DB (`data/kit_space_chronicle.db`) | Engine doesn't currently host its own analytical DB; would establish new pattern with no clear benefit over flat JSON |

### 3.4 Chronicle JSON shape (engine source-of-truth; star-lord implements emit)

```json
{
  "schema_version": "1.0",
  "schema_notes": "kit-space-expansion chronicle. Per canonical/story/2026-06-02-season-archive-realm-expansion-pivot.md § 3.4. Event-type extensible per event_type field; this v1.0 implements kit-space-expansion only.",
  "events": [
    {
      "event_id": "kse_20260602_001",
      "event_type": "kit-space-expansion",
      "event_timestamp": "2026-06-02T14:30:52Z",
      "event_date_utc": "2026-06-02",
      "event_scope": "First kit-space-expansion: Q18 vocabulary lock + WS2.P2 magic weapons substrate; 20-30 kits with WS1A.4-lite per-skill flavor naming",
      "substrate_inputs_changed": [
        "pool.json v1.1 (WS1A.Q18 lock 2026-06-01)",
        "WS2.P2 magic-weapons substrate ingested",
        "WS1A.4-lite per-skill LLM judgment active"
      ],
      "engine_version_sha": "<sha7>",
      "engine_version_full": "<sha40>",
      "kit_ids_generated": ["kit_shadow_000001", "kit_fire_000001", "..."],
      "kit_count": 25,
      "skip_flags_active": ["skip_theme_coalescence", "skip_cosmological_vocabulary"],
      "lineage_tags": {
        "kit_space_lineage": "kit-space-expansion-kse_20260602_001",
        "engine_provenance": "engine-<sha7>-kse_20260602_001",
        "substrate_provenance": "pool-v1.1+ws2.p2-magic-weapons",
        "generation_cohort_date": "2026-06-02"
      }
    }
  ]
}
```

### 3.5 Shadow tables (elrond-side; this MIGRATION authors)

```sql
-- engine_kit_space_events: per-chronicle-event row
CREATE TABLE engine_kit_space_events (
    event_id                TEXT PRIMARY KEY,                      -- kse_<YYYYMMDD>_<seq3> format (LOCKED § 1; SEQ-3 canonical)
                                                                   --   regex: ^kse_\d{8}_\d{3}$ (16 chars)
    event_type              TEXT NOT NULL DEFAULT 'kit-space-expansion'
                            CHECK (event_type IN ('kit-space-expansion', 'realm-expansion', 'reserved-future')),
    event_timestamp         TEXT NOT NULL,                         -- ISO-8601 UTC
    event_date_utc          TEXT NOT NULL,                         -- ISO date (denormalized; supports date-range queries cheaply)
    event_scope             TEXT NOT NULL,                         -- human-readable scope description
    substrate_inputs_changed_json TEXT NOT NULL,                   -- JSON array preserving full string list
    engine_version_sha      TEXT NOT NULL,                         -- 7-char short sha
    engine_version_full     TEXT,                                  -- 40-char full sha (nullable; if engine doesn't emit)
    kit_count               INTEGER NOT NULL CHECK (kit_count >= 0),
    skip_flags_active_json  TEXT,                                  -- JSON array of skip-flag names active at fire (nullable)
    lineage_tags_json       TEXT,                                  -- JSON object of lineage_tags dict (nullable for backward-compat)
    source_chronicle_path   TEXT NOT NULL,                         -- filesystem path to source chronicle.json (provenance anchor)
    ingest_timestamp        TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP -- when elrond shadow ingested this row
);

CREATE INDEX idx_kse_event_date ON engine_kit_space_events(event_date_utc);
CREATE INDEX idx_kse_event_type ON engine_kit_space_events(event_type);

-- engine_kit_index: per-kit row indexed by kit_id
CREATE TABLE engine_kit_index (
    kit_id                          TEXT PRIMARY KEY,                  -- kit_<primary>_<seq6> format (LOCKED § 2)
    primary_element                 TEXT NOT NULL                      -- canonical-7+1
                                    CHECK (primary_element IN ('fire', 'water', 'earth', 'wind', 'lightning', 'holy', 'shadow', 'physical')),
    cultural_tradition              TEXT,                              -- nullable until WS1A.3-style substrate lands
    period                          TEXT                               -- ANCIENT / MEDIEVAL / MODERN per WS2.P2 substrate
                                    CHECK (period IS NULL OR period IN ('ANCIENT', 'MEDIEVAL', 'MODERN')),
    emergent_kit_concept            TEXT,                              -- e.g., "Necromancer" (Wave B identity LLM output)
    chain_composition_json          TEXT,                              -- JSON preserving full chain selection metadata
    t4_selection_json               TEXT,                              -- JSON preserving T4 selection metadata
    supporting_chain_json           TEXT,                              -- JSON preserving supporting chain metadata
    skill_count                     INTEGER NOT NULL CHECK (skill_count >= 0),
    skills_summary_json             TEXT NOT NULL,                     -- JSON array of {skill_id, skill_name, flavor_decision, flavor_word_used} per skill
    substrate_trace_json            TEXT NOT NULL,                     -- JSON preserving substrate inputs (cultural-tradition source, period source, etc.)
    kit_space_expansion_event_id    TEXT NOT NULL REFERENCES engine_kit_space_events(event_id),
                                                                       -- FOREIGN KEY to chronicle (LOCKED § 1 format)
    engine_version_sha              TEXT NOT NULL,                     -- 7-char short sha at this kit's generation
    generation_timestamp            TEXT NOT NULL,                     -- ISO-8601 UTC
    lineage_tags_json               TEXT,                              -- JSON object: kit_space_lineage / engine_provenance / substrate_provenance / generation_cohort_date
    source_kit_json_path            TEXT NOT NULL,                     -- filesystem path to source per-kit JSON (provenance anchor)
    ingest_timestamp                TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_kit_primary ON engine_kit_index(primary_element);
CREATE INDEX idx_kit_event ON engine_kit_index(kit_space_expansion_event_id);
CREATE INDEX idx_kit_period ON engine_kit_index(period);
CREATE INDEX idx_kit_cultural_tradition ON engine_kit_index(cultural_tradition);
```

**Ingest discipline:**
- Rebuildable from filesystem (truncate + reload from `data/kit_space/`)
- Source-anchored: every row carries `source_chronicle_path` / `source_kit_json_path`
- Reversible: drop tables at any time without affecting engine
- Tagged not encoded: `lineage_tags_json` preserves the four lineage-tag fields as discrete JSON (NOT packed into a compound id)
- Versioned: schema-meta entry (next section)

### 3.6 schema_meta entry (per existing catalogue.db convention)

```sql
INSERT INTO schema_meta (version, applied_at, description) VALUES (
    'v1.8-eaa-3-plus-4-engine-kit-shadow-tables',
    CURRENT_TIMESTAMP,
    'EAA-3 + EAA-4: engine_kit_index + engine_kit_space_events shadow tables (additive; rebuildable from kit_space/ filesystem). Source of truth lives at reincarnated-engine/data/kit_space/*.json; these tables are a derived analytical index per LOCK J ADDITIVE-AND-REVERSIBLE. Composes with pool.json v1.1 lineage-tag substrate.'
);
```

---

## 4. Per-kit JSON entry schema (elrond ingest-compat confirmation; rocket primary)

Per EAA-3 dispatch § 3.1, rocket authors the draft schema spec; this section names the elrond-side ingest-compat requirements + the iteration points where DRAFT discipline may require schema adjustment.

### 4.1 Required field shape (engine source-of-truth; rocket implements emit)

```json
{
  "schema_version": "1.0",
  "kit_id": "kit_shadow_000001",
  "primary_element": "shadow",
  "cultural_tradition": "necromantic-folk",
  "period": "MEDIEVAL",
  "chain_composition": { /* engine chain metadata; preserved verbatim */ },
  "t4_selection": { /* engine T4 metadata; preserved verbatim */ },
  "supporting_chain": { /* engine supporting-chain metadata; preserved verbatim */ },
  "skills": [
    {
      "skill_id": "skill_000001",
      "skill_name": "Bone Spear",
      "flavor_decision": true,
      "flavor_word_used": "bone",
      "role": "burst_damage",
      "canonical_element": "shadow",
      "effect_category": "single_target_damage",
      "energy_cost": 28.2,
      "cooldown_seconds": 6.7,
      "damage_multiplier": 1.0,
      "tier": 1,
      "chain_id": "chain_A",
      "chain_position": 1,
      "parent_skill_ids": [],
      "scaling_coefficient": 1.0678,
      "effects": [ /* preserved verbatim from existing class JSON schema */ ],
      "flavor_text": "..."
    }
  ],
  "emergent_kit_concept": "Necromancer",
  "substrate_trace": {
    "cultural_tradition_source": "...",
    "period_source": "...",
    "chain_composition_source": "...",
    "t4_selection_source": "...",
    "supporting_chain_source": "...",
    "substrate_inputs_changed_since_prior_event": "..."
  },
  "kit_space_expansion_event_id": "kse_20260602_001",
  "engine_version": "<sha7>",
  "generation_timestamp": "2026-06-02T14:23:18.117Z",
  "lineage_tags": {
    "kit_space_lineage": "kit-space-expansion-kse_20260602_001",
    "engine_provenance": "engine-<sha7>-kse_20260602_001",
    "substrate_provenance": "pool-v1.1+ws2.p2-magic-weapons",
    "generation_cohort_date": "2026-06-02"
  }
}
```

### 4.2 Required-vs-optional field discipline

**Required (cannot be null) for ingest-compat:**
- `kit_id` (PK; FORMAT LOCKED § 2)
- `primary_element` (FK to canonical-7+1; FORMAT LOCKED upstream)
- `kit_space_expansion_event_id` (FK to chronicle; FORMAT LOCKED § 1)
- `engine_version` (provenance anchor)
- `generation_timestamp` (provenance anchor; ISO-8601 UTC)
- `skills` (at least one entry; engine's existing skill schema preserved)
- `schema_version` (forward-compat marker)

**Required-but-nullable (substrate-substrate fields):**
- `cultural_tradition` (nullable if substrate not yet supplying for this kit)
- `period` (nullable; CHECK constraint on shadow table)
- `emergent_kit_concept` (nullable for kits where Wave B identity LLM hasn't fired; expected non-null in first kit-space-expansion event per LOCK N)
- `chain_composition` / `t4_selection` / `supporting_chain` (preserved verbatim from engine; nullable if substrate doesn't supply)

**Strongly recommended (for analytical queries; not blocking ingest):**
- `substrate_trace` (provenance details; recommended non-null)
- `lineage_tags` (four-field substructure; matches pool.json v1.1 pattern)

### 4.3 Per-skill EAA-1 metadata (compose with EAA-1 dispatch)

Per EAA-1 WS1A.4-lite scope, per-skill judgment fires `flavor_decision: bool` + `flavor_word_used: str | null`. This composes natively:

- `flavor_decision: true` → `flavor_word_used` MUST be non-null (a Q18-pool word from kit's primary element)
- `flavor_decision: false` → `flavor_word_used` MUST be null (canonical skill name)

Constraint at shadow-table level deferred (skill granularity lives inside `skills_summary_json` blob); engine-side schema MUST enforce this at emit-time (rocket's responsibility per EAA-1).

### 4.4 Elrond ingest-compat verdict: **CONFIRMED**

- Per-kit JSON entry is consumable as a filesystem read + JSON parse
- Shadow table column types map 1:1 to JSON field types (TEXT for strings, INTEGER for counts, JSON-as-TEXT for nested structures)
- Required-vs-nullable discipline preserves shadow-table CHECK constraint feasibility
- No engine-side schema field that breaks ingest

**Iteration points where DRAFT discipline may surface adjustments (rocket attention required):**

1. **`primary_element` enum constraint:** must match canonical-7+1 EXACTLY (lowercase). If rocket emits `Shadow` (titlecase) or `dark` (variant), shadow table CHECK fails. Engine-side schema spec must lock to lowercase canonical names.
2. **`period` enum constraint:** must match `ANCIENT` / `MEDIEVAL` / `MODERN` (uppercase per WS2.P2 substrate convention). If engine emits variant casing or value outside the enum, shadow table CHECK fails. Rocket may need to align engine-side period field if it diverges.
3. **`kit_space_expansion_event_id` referential integrity:** every per-kit JSON entry's `kit_space_expansion_event_id` MUST match a chronicle entry's `event_id` EXACTLY. Engine emit order: chronicle event entry FIRST, then per-kit entries (so the FK target exists when shadow ingest runs).
4. **`engine_version` short-sha format:** shadow table uses 7-char short-sha column. If engine emits longer or differs in format, shadow ingest will need string slicing or column widening. Recommend: engine emits both 7-char short + 40-char full; shadow stores short, optional full.
5. **`flavor_decision` + `flavor_word_used` integrity:** EAA-1 cross-coupling per § 4.3 above; engine-side schema must enforce or shadow ingest must detect-and-warn.

If rocket's DRAFT spec diverges on any of these five points, **iteration cycle in-scope per LOCK K** (jack-ryan Gate-1 INFO-B); convene rocket + elrond + star-lord briefly to align before EAA-3 Gate-2 submission.

---

## 5. Filesystem layout (engine source-of-truth; star-lord implements emit)

```
~/Games/reincarnated-engine/data/kit_space/
├── kit_space_chronicle.json          # chronicle source-of-truth (§ 3.4)
├── kits_index.json                   # optional flat list of kit_ids (cheap directory enum; reproducible from glob)
└── kits/
    ├── kit_shadow_000001.json
    ├── kit_shadow_000002.json
    ├── kit_fire_000001.json
    ├── kit_fire_000002.json
    └── ...
```

**NOT** under `seasons/` (canonical pivot: kit space is continuous, NOT season-scoped).

**Parallel to** `seasons/` (historical seasons preserved per Path α; continue to exist; not migrated).

**Emit order discipline (star-lord):**
1. Chronicle entry appended FIRST (event_id minted; event entry written)
2. Per-kit JSON entries written SECOND (each carries kit_space_expansion_event_id = chronicle event_id just minted)
3. Optional kits_index.json regenerated after (cheap glob; can be rebuilt at any time)

**Atomicity:** if rocket + star-lord can emit as a single transaction (write chronicle, write all kit JSONs, fsync), prefer that. If not, document the partial-failure recovery story in MIGRATION.md (elrond shadow ingest tolerates missing per-kit JSONs by skipping; surfaces warning).

---

## 6. Backward-compatibility statement (consumer-impact)

### 6.1 Historical season manifests (UNCHANGED)

Per canonical record § 6 (Path α): existing `seasons/season_000001` through `seasons/season_000200` PRESERVED. Schema unchanged. Consumers reading from `seasons/` continue to function. NO migration.

### 6.2 New kit space (ADDITIVE)

- New directory: `data/kit_space/`
- New schema: per-kit JSON entry (§ 4)
- New chronicle: `kit_space_chronicle.json` (§ 3.4)
- New shadow tables: `engine_kit_index` + `engine_kit_space_events` in catalogue.db (§ 3.5)

NO removal of existing season writer code (per LOCK M Stage 1 — skip-flag pattern only; Stage 2 code removal deferred). Both emit paths coexist.

### 6.3 Drax loadout (LOCK O scope; EAA-6 separate)

Drax MVP reframe (EAA-6) will consume new kit space output. THIS dispatch does NOT touch drax. Drax consumer can read filesystem (`data/kit_space/`) or use a future engine-emitted manifest export; design choice deferred to EAA-6.

### 6.4 Engine page reframe (LOCK O scope; EAA-7 separate)

EAA-7 consumes chronicle JSON for engine page rendering. THIS dispatch produces the chronicle data; EAA-7 consumes it via existing EngineStatePipelineFlow component pattern per LOCK O.

---

## 7. Smoke-test discipline (Disc #2; EAA-3 § 3.4 + EAA-4 § 3.4)

Before EAA-5 first-fire consumes this infrastructure:

1. **Single-event-single-kit smoke:** mint one event_id (`kse_<YYYYMMDD>_<seq3>` per § 1.3 generation rule); write chronicle entry; write one kit JSON entry; verify:
   - Chronicle file parses (JSON valid; schema_version present)
   - Per-kit JSON parses (schema_version present; all required fields present)
   - `kit_space_expansion_event_id` in per-kit JSON matches chronicle entry `event_id`
   - Lineage tag values in per-kit JSON match chronicle event lineage tags
2. **Shadow ingest smoke:** run elrond ingest script against single-event-single-kit emission:
   - Chronicle event row inserted (1 row in `engine_kit_space_events`)
   - Kit row inserted (1 row in `engine_kit_index`)
   - FK integrity holds (kit's `kit_space_expansion_event_id` resolves to chronicle row)
   - schema_meta version bumped to `v1.8-eaa-3-plus-4-engine-kit-shadow-tables`
3. **Rebuild smoke:** truncate shadow tables; rerun ingest; verify same row counts + same row contents (deterministic rebuild)
4. **Backward-compat smoke:** verify existing season manifest emit path still works when skip flags inactive (covered by EAA-2 smoke-test; cross-reference here)

Smoke-test scripts authored when EAA-3 + EAA-4 implementation lands. This note locks the SHAPE of the smoke-tests; implementation follows.

---

## 8. Open coordination items

### 8.1 With rocket (EAA-3 primary)

- **DRAFT discipline:** rocket authors per-kit JSON schema as DRAFT against this spec; iterate against § 4.4 five iteration points if engine-side surfaces divergence
- **`emergent_kit_concept` source:** is this from Wave B identity LLM call (existing engine) or new component? Confirm at rocket implementation; doesn't affect schema field — just where engine sources the value
- **`substrate_trace` field discipline:** rocket determines exact field set within `substrate_trace`; elrond accepts any JSON structure; recommend at minimum: `cultural_tradition_source`, `period_source`, `chain_composition_source`, `t4_selection_source`, `supporting_chain_source`

### 8.2 With star-lord (EAA-3 + EAA-4 emit pipeline)

- **Emit atomicity:** prefer single-transaction emit (chronicle entry + all per-kit JSONs together with fsync); if not feasible, document partial-failure recovery
- **`engine_version_sha` source:** star-lord names how engine determines its sha at fire time (git-rev-parse during generation; commit at emit-time)
- **Shadow ingest trigger:** star-lord pipeline can OPTIONALLY trigger elrond shadow ingest as a post-emit step; OR elrond owns the ingest script and fires on cycle-orchestrator schedule. Decision is operational; doesn't affect schema. Recommend: elrond owns the ingest script; runs after each kit-space-expansion event (cycle orchestrator calls elrond ingest as a post-emit hook).

### 8.3 With EAA-6 / EAA-7 (future drax workstreams)

- **kit space consumption:** drax may either read filesystem directly OR consume via engine-emitted manifest export. Decision deferred to EAA-6.
- **Engine page chronicle consumption:** EAA-7 reads `kit_space_chronicle.json` via existing EngineStatePipelineFlow pattern. Schema is consumable as-is.

---

## 9. ADR-004 cross-seam contract summary

| Contract | Old | New | Backward-compat |
|---|---|---|---|
| Engine output unit | Per-season manifest (`seasons/season_NNNNNN/manifest.json` + class/monster/trial/gear JSONs) | Per-kit JSON entry (`data/kit_space/kits/kit_<primary>_<seq6>.json`) + chronicle event entry | BOTH coexist; historical seasons preserved; new generation emits per-kit |
| Engine chronicle | Per-season manifest record on engine page (legacy) | `kit_space_chronicle.json` event list | BOTH coexist (engine page may surface historical season chronicle as legacy view; new content from new chronicle) |
| Elrond ingest | NO existing ingest of engine class JSONs (analysis read filesystem ad-hoc) | NEW shadow tables (`engine_kit_index` + `engine_kit_space_events`) in catalogue.db; rebuildable from filesystem | Strictly additive; rebuildable; reversible per LOCK J |
| Foreign-key linkage | N/A (no cross-file FK in old per-season schema) | `kit_space_expansion_event_id: kse_<YYYYMMDD>_<seq3>` links per-kit JSON to chronicle event | New contract; FORMAT LOCKED § 1 (SEQ-3; canonical per CHRONICLE_SCHEMA.md § 3 + MIGRATION v1.9) |

**ADDITIVE-AND-REVERSIBLE per LOCK J:** ALL changes are additive (no old field removed; no enum value removed; no required-field added to existing schemas). Shadow tables can be DROPPED without affecting engine; engine kit_space/ can be DELETED without affecting historical seasons.

---

## 10. Sign-off

**Verdict:** elrond ingest-compat **CONFIRMED**. `kit_space_expansion_event_id` format **LOCKED** (§ 1). `kit_id` format **LOCKED** (§ 2). Chronicle storage medium **LOCKED** (§ 3.1; Option α source-of-truth + Option β-light analytical shadow). Per-kit JSON entry shape **LOCKED** for ingest-compat (§ 4); rocket DRAFT spec composes natively.

**Authority:** LOCK K (engine schema design authority; elrond co-owner on EAA-3 ingest schema + EAA-4 chronicle schema as primary). Per CLAUDE.md addendum 2026-05-25 auto-commit; per Matt 2026-06-02 cycle-push authorization.

**Composition with concurrent dispatches:**
- EAA-1 WS1A.4-lite: composes via `flavor_decision` + `flavor_word_used` per-skill fields (§ 4.3)
- EAA-2 skip-flag pattern: composes via skip-flags-active emit chronicle field (§ 3.4); orthogonal otherwise
- EAA-5 first generation fire: blocked-by EAA-3 + EAA-4 PASS; per LOCK N first-fire generates 20-30 kits emitting per § 4 + § 5
- EAA-6 / EAA-7 drax reframes: blocked-by EAA-5 PASS; consume kit space + chronicle as documented

**Next moves:**
1. Author MIGRATION.md v1.8 entry covering EAA-3 + EAA-4 elrond-side shadow tables (this is appended to `agentic_orchestration/research/curated/MIGRATION.md`)
2. Communicate FK format lock (§ 1) + kit_id format lock (§ 2) to rocket + star-lord (this note IS the communication artifact)
3. Author elrond shadow-table CREATE script + ingest script (deferred to EAA-3 + EAA-4 implementation phase post-Gate-2)
4. Smoke-test on EAA-5 first-fire (§ 7)
5. jack-ryan Gate-2 review on schema spec + MIGRATION.md

**Signed:** elrond (data steward; LOCK K + LOCK E seam authority; EAA-3 + EAA-4 co-owner)
