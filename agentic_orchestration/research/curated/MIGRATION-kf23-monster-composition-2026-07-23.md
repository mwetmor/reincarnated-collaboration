# MIGRATION — KF-2/3 monster-side + composition-ledger tables (additive)

**Author:** elrond (data steward) | **Date:** 2026-07-23 | **DB:** `agentic_orchestration/research/curated/corpus.db`
**Run:** KIT-FIDELITY (charter `agentic_orchestration/gandalf/notes/2026-07-23-kit-fidelity-run-charter.md`), gate KF-2 + KF-3, ledger KFL-8(d).
**Class:** ADDITIVE-ONLY. Two new tables. Zero changes to existing columns/tables' shape (charter LAW). No FK to `canon_corpus` on the monster side (monsters are not kits — they have no `canon_corpus` row).
**Backup taken:** `corpus.db.pre-kf23-monster-comp-2026-07-23-backup` (pre-DDL, Discipline #8/#11).

---

## Why these tables

KF-3 harvests MONSTER data from the source-game databases; KF-2's composition audit (KFL-7 fold) needs a
first-class home for the per-kit expected-value factor chain. Neither has a table today. The monster side
mirrors `kit_numeric`'s dual-column anchored-source discipline; the composition ledger is a new relational
shape (kit × direction × factor).

**Dual-column law held on both tables:** `source_value` is IMMUTABLE and carries a verbatim anchor; `rdr_value`
stays NULL until the gamora/star-lord normalization-rule lane derives it. elrond authors neither the rules nor
the rdr_values.

---

## Table 1 — `monster_numeric` (KF-3 monster-side dual-column store)

Mirrors `kit_numeric` (monster analogue). Because monsters have no `canon_corpus` PK to anchor an
FK, `monster_id` + `game` are free-text and form the identity. The charter explicitly asks the monster table
to carry anchor quote / URL / access-date / source_scale / rdr_value NULL / starter-set membership — so those
are first-class columns here (on `kit_numeric` the URL+date are packed into the single `source_anchor` TEXT;
the monster table separates them, which is additive and cleaner for the harvest provenance).

```sql
CREATE TABLE monster_numeric (
    monster_id       TEXT NOT NULL,                 -- e.g. 'd2-fallen', 'poe1-goatman-leapslam-l68'
    game             TEXT NOT NULL,                 -- 'd2' | 'poe1' | 'poe2' | 'gd' (matches canon_corpus.game codes)
    monster_name     TEXT NOT NULL,                 -- display name, e.g. 'Fallen (Normal Act 1)'
    numeric_key      TEXT NOT NULL,                 -- e.g. 'hp_min','defense','ar_attack1','fire_resist_pct'
    source_value     REAL NOT NULL,                 -- IMMUTABLE, anchored (VERIFY territory) — dual-column law
    source_scale     TEXT NOT NULL,                 -- e.g. 'd2_flat_hp','d2_defense_rating','poe1_armour_rating','pct'
    rdr_value        REAL,                          -- DERIVED by rule; NULL until a normalization_rule runs; sim reads THIS only
    rule_id          TEXT REFERENCES normalization_rule(rule_id),
    rule_version_applied INTEGER,                   -- staleness check (which rule version produced current rdr_value)
    source_anchor    TEXT NOT NULL,                 -- verbatim quote for source_value (elrond anchor law)
    source_url       TEXT NOT NULL,                 -- provenance URL
    source_date      TEXT NOT NULL,                 -- access date (ISO)
    starter_set      TEXT NOT NULL,                 -- starter-set membership tag, e.g. 'd2-act1-normal','poe1-zone68','poe2-levelscale'
    gap_flag         TEXT                           -- NULL when hard-anchored; a note when the row is an inference/gap-annotated value
                       CHECK (gap_flag IS NULL OR gap_flag IN ('normal_resist_inferred','formula_level_anchor','one_source','range_estimate')),
    created_date     TEXT NOT NULL DEFAULT (date('now')),
    PRIMARY KEY (monster_id, numeric_key)
);
CREATE INDEX idx_mnum_game    ON monster_numeric(game);
CREATE INDEX idx_mnum_starter ON monster_numeric(starter_set);
CREATE INDEX idx_mnum_rule    ON monster_numeric(rule_id);
```

**Column notes:**
- `gap_flag` is the schema home for the harvest notes' own gap annotations (e.g. d2 "Normal-difficulty resist
  row not explicitly stated — inferred 0% from Hell column + Normal baseline"). Such rows are curated with the
  anchored value the note gives AND `gap_flag='normal_resist_inferred'` so a downstream consumer never mistakes
  an inference for a hard anchor. A value the note marks FULL GAP is NOT inserted at all (anchor law: gaps are
  absences, never estimates) — it appears only in the rules-needed manifest / MIGRATION gap register.
- `formula_level_anchor` flags the poe2 rows sourced from the level-scaling table (a formula-level anchor, not a
  per-named-mob anchor, per the poe2 note's own recommendation).

## Table 2 — `kit_composition` (KF-2 composition-ledger, KFL-7 fold)

Per-kit, per-direction (dealt/received) expected-value factor chain
`base × skill/mastery modifiers × hit-chance × crit-EV × (1 − mitigation)`, every factor labeled
ANCHORED / PINNED / GAP-EXCLUDED with its ref (verbatim anchor citation OR charter PIN id).

```sql
CREATE TABLE kit_composition (
    comp_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    kit_id           TEXT NOT NULL REFERENCES canon_corpus(kit_id),
    direction        TEXT NOT NULL CHECK (direction IN ('dealt','received')),
    factor_key       TEXT NOT NULL,                 -- e.g. 'base_damage','fire_mastery_mult','hit_chance','crit_ev','target_mitigation'
    factor_role      TEXT NOT NULL,                 -- ordered position in the chain: 'base'|'modifier'|'hit_chance'|'crit_ev'|'mitigation'
    status           TEXT NOT NULL CHECK (status IN ('anchored','pinned','gap_excluded')),
    factor_value     TEXT,                          -- the value/expression when anchored or pinned (TEXT: may be a range or formula); NULL when gap_excluded
    ref              TEXT NOT NULL,                 -- anchor citation (URL + verbatim) OR PIN id (e.g. 'PIN-C2','KFL-8(b)') OR GAP id
    notes            TEXT,
    created_date     TEXT NOT NULL DEFAULT (date('now'))
);
CREATE INDEX idx_kcomp_kit ON kit_composition(kit_id);
CREATE INDEX idx_kcomp_dir ON kit_composition(kit_id, direction);
```

**Column notes:**
- `factor_role` gives the chain its order so a consumer can reconstruct `base × modifier × hit_chance × crit_ev
  × (1 − mitigation)` deterministically regardless of insert order.
- `status='gap_excluded'` rows carry `factor_value=NULL` and a `ref` naming the GAP (e.g. `GAP-B1` for the poe2
  armour formula). The gauge computes over the declared (non-excluded) factors only; the exclusion is named —
  charter §9 GAP-display rule. No silent estimation ever fills a gap_excluded factor.
- `status='pinned'` rows cite a charter PIN as `ref` (the pin IS the authority; not an anchor, not an estimate).

---

## schema_meta stamp

A `corpus_schema_meta` row is inserted at apply time:
`version='kf23-monster-comp-2026-07-23'`, note describing the two additive tables + KFL-8(d) provenance.

## Rollback

Additive only — rollback is `DROP TABLE monster_numeric; DROP TABLE kit_composition;` (plus the schema_meta
row). No existing table is touched, so rollback cannot affect prior data. Backup retained regardless.

## Commitment-boundary check

No non-additive need arose. Both tables are new; no existing column is renamed/removed/retyped. Had a note's
data required an existing-column change, the charter LAW is STOP-and-report (commitment-boundary) — that did
not occur.
