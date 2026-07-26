# MIGRATION-fixtures.md — `fixtures.db` migration ledger

**Store:** `agentic_orchestration/research/curated/fixtures.db`
**Owner:** elrond (data steward) · **Commissioner:** gandalf (GD program, gap 5)
**Sibling ledgers:** `MIGRATION.md` (catalogue), `MIGRATION-vdm1-*.md`, `MIGRATION-gd-*.md` (corpus)
**Authority:** ADR-004 (cross-seam coordination + per-store migration ledger)

This store is **separate from `corpus.db` by ruling O-1** (gandalf, 2026-07-25). Rationale
carried from the draft §3: `corpus.db` holds 574 curated kits on schema v2.0 with a heavy
backup-per-write discipline; the fixture bank grows one Matt sitting at a time and will
eventually be written by an autonomous run (`L0-CLOSE`). A separate file physically bounds
that run's blast radius. Cross-store joins are one `ATTACH` away — the join keys are strings
(`.dbr` record paths) already conventional in `corpus.db.exact_skill.record_path`.

The `.db` file is **gitignored** (`curated/.gitignore` → `*.db`), per the standing convention
that curated SQLite stores are regenerable from committed scripts. **The scripts below are the
durable record.** A byte-equivalent rebuild is:

```bash
python3 agentic_orchestration/research/scripts/fixtures_m1_landing_2026_07_26.py
python3 agentic_orchestration/research/scripts/fixtures_m2_backfill_r12_2026_07_26.py
python3 agentic_orchestration/research/scripts/fixtures_m3_ingest_r3_2026_07_26.py
```

---

## M1 — 2026-07-26 · schema `fixtures-v0.1` landed

**Script:** `research/scripts/fixtures_m1_landing_2026_07_26.py`
**DDL:** `research/scripts/fixtures_v0_1_ddl.sql` (sha256 `c1287b4675…0ba6d166`)
**Applies:** 11 tables + 7 views + `measure_dict` seed (17 keys) + `schema_meta` row.

### Tables

| Table | Purpose |
|---|---|
| `fixture_session` | one Matt PC sitting, or one sim batch. `lane` is the discriminator. |
| `capture` | screenshots / console dumps. ORACLE-ONLY. |
| `fixture_character` | player-state snapshot; several per session (level-ups mint new ones). |
| `character_stat` | **E1** — long-form exhaustive character-sheet readings, per-field provenance. |
| `fixture_set` | the N-trial group: one monster, one rig, one ladder rung. |
| `fixture_set_constraint` | per-rung constraint attestations; `unknown` and `expired` are first-class. |
| `fixture_trial` | one fight. Deliberately thin. |
| `measure_dict` | controlled vocabulary for `trial_measurement.measure_key`. |
| `trial_measurement` | **the core** — every number as a READING, with per-field provenance. |
| `trial_trace` | FSM observations; `trace_token` and `controller_state` stay two columns. |
| `schema_meta` | version ledger, mirroring `corpus_schema_meta`. |

### Views

`v_trial_wide` · `v_trial_delta` · `v_set_spread` (Q47's spread instrument) ·
`v_ledger_continuity` (off-trial-activity detector) · `v_differential` (G3-B oracle⋈sim) ·
`v_fixture_bank_certified` (**O-8: Q47 rules against this view only**) ·
`v_fixture_bank_certified_clean`.

### Ruling conformance verified at landing

| Ruling | Where it lives in the store | Verified |
|---|---|---|
| O-1 separate `fixtures.db` | own file, own ledger (this doc) | ✅ |
| O-2 `measure_subkey` column | `trial_measurement.measure_subkey`, in the PK | ✅ |
| O-6 `dps_field` = oracle colour only | `measure_dict.lane_availability='oracle-only'` | ✅ **corrected at landing** |
| O-7 disagreeing readings both stand | no reconciliation logic anywhere; both `hp_cost_abs` and the `life_healed` delta are banked | ✅ |
| O-8 NULL identity admitted; certified view filters | `fixture_set.monster_record` nullable + `v_fixture_bank_certified` predicate | ✅ |
| O-9 expired no-CC constraint carried | `fixture_set_constraint.held` CHECK includes `'expired'` | ✅ |

### DDL verification — what I changed vs. what I inherited

The DDL file was authored by a prior session that did not survive to apply it. It was
**re-verified line-by-line against draft §10 and the ten rulings before use**, not trusted.
Findings:

1. **Table creation order is correct.** `capture` is created before `fixture_character`,
   which FKs it. The draft §10 sketch had them in the opposite order and would have failed
   under `PRAGMA foreign_keys=ON`. The inherited file had already fixed this — verified, kept.
2. **Six landing extensions (E1–E6) are additive and defensible**, and are documented in the
   DDL header: `character_stat` (E1), `outcome += 'no-fight-baseline'` (E2, carries O-10's
   round-1 baseline), `capture.kind += 'trial-frame'` (E3), `fixture_set.monster_display_name`
   (E4, nameplate text as distinct from the `.dbr` join), `fixture_trial.monster_entity_id`
   (E5, overlay instance id — start==end proves one fight), `fixture_character.notes` (E6).
   All accepted.
3. **`dps_field` lane availability was wrong in the draft** (§6.1 said `both†`) and gandalf's
   O-6 ruling supersedes it. The DDL needed no change (it is data, not schema); the seed in
   `fixtures_m1_landing_2026_07_26.py` sets `oracle-only`. **This correction is the one
   substantive fix this milestone makes to the inherited artifact.**
4. **Applied to an empty DB:** `PRAGMA foreign_key_check` CLEAN; all 7 views selectable.

### `measure_dict` seed — 17 keys

`play_time` · `total_score`* · `deaths` · `kills` · `health_potions_used` ·
`mana_potions_used` · `max_level_achieved` · `dps_field`* · `skill_use_count` ·
`life_healed` · `shield_block_chance` · `fight_seconds` · `hp_cost_band` · `hp_cost_abs` ·
`hp_current` · `hp_max` · `capture_latency`*   (* = `oracle-only`)

`confounds` is populated, not decorative: `life_healed` carries all three named confounds
from draft §8.6; `dps_field` carries the window-expiry confound from §8.4; `fight_seconds`
carries the round-3 screenshot-overhead bias from `matt-addendum-timing-uncertainty.md`.

---

## M2 — 2026-07-26 · rounds 1–2 backfill (uncertified)

**Script:** `research/scripts/fixtures_m2_backfill_r12_2026_07_26.py`

Backfills draft §7.2 exactly. Key structural facts, all preserved rather than smoothed:

- **Two sessions.** `gd-live-2026-07-25-s1` (round 1, rig verdict + the O-10 baseline panel)
  and `gd-live-2026-07-25-s2` (round 2, the three trials).
- **Two character snapshots in s2, not one.** The player levelled 5→6 between trial 1 and
  trial 2 (draft correction C2). `hp_max=282` is read from the shot-(17) globe and applies to
  the level-6 snapshot only.
- **The level-up splits the trials into two sets** — `L0-gd-s2-set1` (N=1) and
  `L0-gd-s2-set2` (N=2). Computing an N=3 spread across a covariate change would have ruled
  Q47's bar against a number that is partly a level-up.
- **Contamination flag on the off-trial discontinuity.** `kills` 163→164, `defaultweaponattack`
  431→433, `life_healed` 2292.86→2311.37 between T2-after and T3-before: one kill, two
  attacks and 18.51 HP of healing outside any trial. `L0-gd-s2-set2/t2` carries
  `contaminated=1`, `contamination_reason='ledger-discontinuity'`.
- **Session-scoped trace rows** (`trial_id IS NULL`). The `Idle/Fidget/Moving/Attack/Flying/
  Dying` tokens come from `colsole-fight-data-test.png` — the `killMonsters` sweep, a
  *different event* from the three trials. They are session observations, not trial
  observations. `Fidget` and `Flying` are `mapping_status='unmapped'`.
- **Identity `assumed-unverified` for both sets.** No nameplate in any of the six panel
  screenshots; Matt's spawn command sits under a separate heading from the trials. These
  rows therefore do **not** appear in `v_fixture_bank_certified` — by design, per O-8.
- **O-10 round-1 baseline.** `live-probe-1/playstats-panel.png` re-read at full resolution
  and banked as a `no-fight-baseline` trial (extension E2), giving the bank a pre-trial
  reading of the same counters.
- **O-9.** The expired no-CC test-character constraint is carried on both sets as
  `held='expired'`.

---

## M3 — 2026-07-26 · round-3 ingestion (first CERTIFIED candidate set)

**Script:** `research/scripts/fixtures_m3_ingest_r3_2026_07_26.py`
**Evidence:** `research/knowledge/gd/live-probe-3/` — 12 character-sheet shots
(`Screenshot (19)`–`(30)`), 6 trial shots, `GD-console-notes-v3-raw.md`,
`matt-addendum-timing-uncertainty.md`.

### METHOD LAW for this ingestion

**Every banked digit comes from a full-resolution crop.** Crops taken with
`sips -c <h> <w> --cropOffset <y> <x>` against the native 1920×1080 PNGs, then upscaled 2×
for legibility. **No digit is ever read off a downscaled full frame.** Downscaled full frames
were used once, for *region location only*, and no value banked from them.
`read_method='screenshot-fullres'` is asserted only where this held; `uncertainty_abs` is
recorded per reading.

### Round-3 specific provenance rulings applied

- `fight_seconds` 5/5/4 s are banked with `uncertainty_abs=2.0`, `read_method='hand-noted-band'`,
  and a `validity_note` citing `matt-addendum-timing-uncertainty.md` — the hand notes include
  ~1 s per screenshot of capture overhead, a systematic **upward** bias.
- O-7 stands: where Matt's hand-noted HP cost and the globe/panel readings disagree, **both
  are banked** and neither is reconciled.
- `difficulty='normal'` — the first sitting for which this is attested (round 2's is NULL).

Row counts, per-trial certification verdicts and the Q47 evaluation are in the summary note
`elrond/notes/2026-07-26-fixtures-db-landing-and-v3-ingestion.md`.

---

## Cross-seam notes

No engine-side schema change is requested by any migration in this ledger. `fixtures.db` reads
nothing from `reincarnated-engine/data/telemetry.db`. The only cross-store dependency is a
prospective read-only `ATTACH` of `corpus.db` to resolve `.dbr` record paths
(`trial_measurement.measure_subkey` → `exact_skill.record_path`;
`fixture_set.monster_record` → the `.arz` monster slice). Neither is exercised yet.
