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
# M4 (fixtures-v0.2) — CROSS-STORE: requires corpus.db to carry the GD bridge first.
python3 agentic_orchestration/research/scripts/gd_bridge_m1_display_tags_2026_07_26.py
python3 agentic_orchestration/research/scripts/gd_bridge_m2_monster_records_2026_07_26.py
python3 agentic_orchestration/research/scripts/gd_bridge_m3_bridge_and_fixtures_2026_07_26.py
# M5 (fixtures-v0.3) — schema. M6 — GP run 01 ingest.
python3 agentic_orchestration/research/scripts/fixtures_m5_v0_3_schema_2026_07_26.py
# M7 (fixtures-v0.4) — MUST run before M6: it rebuilds fixture_trial.
python3 agentic_orchestration/research/scripts/fixtures_m7_trial_participant_2026_07_26.py
bash    agentic_orchestration/research/scripts/gp_run01_precompute_2026_07_26.sh   # sha256/mtime/dims
python3 agentic_orchestration/research/scripts/fixtures_m6_gp_run01_ingest_2026_07_26.py
# M8 (fixtures-v0.5) -- the measured-fixture layer. Needs NO /Volumes mount: both
# galadriel capture dirs are committed.
python3 agentic_orchestration/research/scripts/fixtures_m8_gd_playtest_v1_fixture_2026_07_28.py
python3 agentic_orchestration/research/scripts/fixtures_m8b_engagement_grain_2026_07_28.py
python3 agentic_orchestration/research/scripts/fixtures_m8c_rollup_and_fixture_2026_07_28.py
python3 agentic_orchestration/research/scripts/fixtures_m8d_fixture_conditions_claims_2026_07_28.py
# M9 (fixtures-v0.6) -- KC1 ruling amendments. Semantics only; no new measurement.
python3 agentic_orchestration/research/scripts/fixtures_m9_kc1_ruling_amendments_2026_07_28.py
```

**M6 requires the `/Volumes/reincarnated` share to be mounted.** Its precompute step reads
13.2 GB over SMB at ~3.5 MB/s (~70 min); the results are committed under
`research/curated/gp-run01-manifest/` so a rebuild does not have to repeat it.

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

## M4 — 2026-07-26 · schema `fixtures-v0.2` · the tag bridge lands, `monster_record` populated

**Script:** `research/scripts/gd_bridge_m3_bridge_and_fixtures_2026_07_26.py` (the fixtures half of it)
**Companion ledger:** `MIGRATION-gd-displayname-bridge-2026-07-26.md` — the corpus side, where the
bridge itself lives. **This is the first cross-store migration in the fixtures ledger.**
**Backup:** `fixtures.db.pre-v0.2-20260726T144128Z-backup` (md5 `c062bf4a0ecc6747ac6ded847c784fda`)
**Class:** ADDITIVE. Seven `ALTER TABLE … ADD COLUMN`; one `UPDATE` on one row; zero drops.

M3's summary note closed with `monster_record` still NULL on the certified rows and named that the
last link between a certified fixture and the `.arz` statline it is meant to predict. That link now
exists.

### Schema delta

| Table | New column | Why |
|---|---|---|
| `fixture_set` | `monster_record_candidates` | JSON array of ALL bridge candidates. `monster_record` is a heuristic pick; this is the evidence it was picked from. Never discarded. |
| `fixture_set` | `monster_bio_record` | **The column a statline prediction should actually join on.** Far less ambiguous than the record path. |
| `fixture_set` | `monster_rank` | GD `monsterClassification` (`Common` here). The nameplate's implicit second axis. |
| `fixture_set` | `monster_race` | `characterRacialProfile` resolved — the nameplate's third line. |
| `fixture_set` | `monster_record_method` | Provenance of the RECORD, kept separate from `monster_identity_method`. |
| `fixture_set` | `monster_record_evidence` | The full two-hop derivation with its caveats. |
| `measure_dict` | `off_trial_semantics` | v0.1 §7 item 1. Seeded on all 17 keys. |

### The one design call that matters: `monster_identity_method` is NOT overwritten

Legolas §4 recommended `monster_identity_method` gain a value like `tag-bridge-inferred` "so a
bridged row is never mistaken for `spawn-command-verbatim`." The goal is right; the mechanism would
have cost something. `L0-gd-s3-set1` is certified **because** of `screenshot-nameplate`, and
`v_fixture_bank_certified` predicates on that column. Writing a bridge inference into it would have
**decertified the only certified set in the bank** — or, worse, kept it certified on the strength of
an inference.

So the identity column is untouched and a **separate `monster_record_method`** carries the record's
provenance: `tag-bridge-inferred+spawn-command-convergent`. Two different questions, two columns.
`v_fixture_bank_certified` still returns 3 rows, post-write, unchanged.

### What is now on the certified row

```
monster_display_name    Walking Dead                                        [nameplate, certified]
monster_record          records/creatures/enemies/zombie_a01.dbr            [HEURISTIC — tiebreak]
monster_record_candidates  25 entries, JSON, with per-candidate bio + penalty + rank
monster_bio_record      records/creatures/enemies/bios/bio_zombie_01.dbr    [23 of 25 support]
monster_rank            Common
monster_race            Aether Corruption
monster_identity_method screenshot-nameplate                                [UNCHANGED]
monster_record_method   tag-bridge-inferred+spawn-command-convergent
```

`monster_record_evidence` records, in full: that hop 1 is *unique* in the string direction (exactly
one of 2,060 creature tag keys yields "Walking Dead"); that hop 2 fans out 25 ways and the stored
path is a heuristic; that Matt's round-2 console note `game.Spawn "records/creatures/enemies/
zombie_a01.dbr"` succeeding is **convergent, not attesting**, because that spawn happened in session
`gd-live-2026-07-25-s2` under a heading separate from any trial while this set is the round-3 *world*
spawn in Vicinity of The Coffinmakers; and that which specific record a world spawn instantiates
lives in `Levels.arc` spawn tables that are not parsed.

### Round-2 sets stay NULL — deliberately

`L0-gd-s2-set1` / `set2` remain `monster_record IS NULL`. The round-2 spawn command attests **the
record**, not that those trials fought it — which is exactly why M2 banked them `assumed-unverified`.
O-8 admits NULL identity and the certified view already excludes them. Populating them from the
bridge would launder an assumption into a fact.

### ANOMALY A1 — RESOLVED, and it retires one of my own recommendations

v0.1 §4 anomaly A1 was the unexplained third nameplate line "Aether Corruption", flagged as
possibly meaning the fixture was an **affixed variant** and therefore not a vanilla zombie statline.
v0.1 §7 item 3 recommended `fixture_set.monster_affix` / `monster_variant` on that basis.

Legolas §3 resolved it: it is `characterRacialProfile = 'Race005'`, a creature-type noun, confirmed
by the singular/plural pair `tagRace005` / `tagRace005P` and by an exhaustive scan of every EN tag
file finding exactly three occurrences of the literal string — two of them that pair, the third a
player-side item-component skill in gdx1 that cannot appear on a hostile nameplate. The banked
`gd_monster_record` row for `zombie_a01.dbr` carries `race_display = 'Aether Corruption'` directly.

**There is no affix. `monster_affix` / `monster_variant` are therefore NOT added** — building them
anyway would bank a superseded hypothesis as schema. `monster_race` is what the line actually is, so
that is what landed. **The fixture is a vanilla zombie; A1 no longer qualifies the set.**

### `off_trial_semantics` seed (v0.1 §7 item 1)

`v_ledger_continuity` flagged `life_healed` as DISCONTINUOUS between every trial pair — correctly,
and uselessly, because regeneration legitimately accrues off-trial. That judgment was the analyst's;
it now lives in the dictionary. All 17 keys seeded across four values:

| value | keys |
|---|---|
| `must-not-advance` | `kills`, `skill_use_count`, `deaths`, `health_potions_used`, `mana_potions_used`, `max_level_achieved` |
| `may-advance` | `life_healed`, `play_time`, `hp_current`, `total_score` |
| `invariant-within-character` | `hp_max`, `shield_block_chance` |
| `trial-scoped` | `fight_seconds`, `hp_cost_band`, `hp_cost_abs`, `dps_field`, `capture_latency` |

### Still open after v0.2

- **Applied-modifier chain.** `bio_zombie_01` gives the BASE statline. `damage_totaladjuster` /
  `armorbase01` passives and difficulty globals stack on top and are not traced. A fixture HP
  prediction is not scoreable until they are.
- **World-spawn → specific record.** `Levels.arc` lane, unopened.
- Q47 remains PARTIAL FIRE per the v0.1 note §3. Nothing in v0.2 moves it.

### Verification

`PRAGMA integrity_check` ok · `foreign_key_check` clean · `v_fixture_bank_certified` = 3 rows
(unchanged) · `measure_dict.off_trial_semantics` 17/17 populated · 1 `fixture_set` row updated.

---

## M5 — 2026-07-26 · schema `fixtures-v0.3` · the ledger layer splits from the trial layer

**Script:** `research/scripts/fixtures_m5_v0_3_schema_2026_07_26.py`
**Backup:** `fixtures.db.pre-v0.3-20260726T232202Z-backup`
**Commission:** gandalf, `2026-07-26-gd-general-play-run-protocol.md` §5 (data contract), against
`2026-07-26-gd-playtest-v1-artifact-verification.md`.
**Class:** ADDITIVE + THREE TABLE REBUILDS (`capture`, `fixture_trial`, `fixture_set`). Zero rows
lost: 28 / 7 / 4 preserved, `v_fixture_bank_certified` still 3.

### The change that matters: the unit of observation moved

v0.1/v0.2 assume the unit of observation is a **trial**. Every number lands in
`trial_measurement` under a `(trial_id, phase)` key. That is exactly right for L0, where Matt
hand-brackets each fight with a before/after screenshot pair.

It is **wrong for a general-play run.** There the unit of observation is a **session-continuous
ledger**, sampled ~2 fps off a panel that is on in every frame. That series exists *prior to* and
*independent of* any segmentation into engagements — and protocol §4.5 asks for **three competing
segmentations at once** (S1 kill-to-kill / S2 combat-window / S3 per-entity). Routing the ledger
through `trial_measurement` would have stored the same readings three times, once per
segmentation, and let the three copies drift.

So v0.3 splits the layers:

| Layer | Table | Keyed on |
|---|---|---|
| **observed** | `session_ledger` (new) | `(session_id, measure_key, measure_subkey, capture_id, play_time_ms)` |
| **windowed** | `fixture_trial` (rebuilt) | `(fixture_set_id, segmentation, trial_ordinal)` |
| **attributed** | `trial_measurement` (unchanged) | as before |

A trial is now a **window over the ledger**, carrying which rule cut it. `trial_measurement`
survives untouched for the hand-bracketed L0 rows and for values attributed to a specific fight.

### New tables

| Table | Purpose |
|---|---|
| `session_ledger` | the observed panel series. `play_time_ms` is the join key; `pts_ms` rides along for frame retrieval. Carries `read_confidence` + `cross_check_status` — gandalf D-1 made structural. |
| `session_break` | deaths / zone transitions / epoch boundaries, first-class. Location is a **band** (`play_time_ms_lo/hi`), because a death known only to lie between two panel samples is located to that bracket. |
| `session_control` | run properties that change what a measure **means** — the no-potion control, linked to `life_healed` with `effect_on_measure='confound-retired'`. |
| `clock_anchor` / `clock_map` | the piecewise slope-1 `play_time ↔ pts` map, **fitted per session, never assumed** (gandalf §3 ruling, made into a table). |
| `character_gear_slot` | per-slot equipment provenance. `slot_state='occupied-unread'` is what "drop the slot, never infer it" looks like — and it is not a validation error. |
| `read_method_dict` | the read-method vocabulary of record. Adds `video-frame-human` and `video-frame-ocr` as **separate** methods. |

### Three break flags, not one

`session_break` carries `breaks_combat_continuity`, `breaks_clock_affine` and
`breaks_character_state` as independent booleans, because the three break kinds are genuinely
different events:

| | combat | clock | character |
|---|---|---|---|
| death | ✔ | — | — |
| zone transition | ✔ | ✔ | — |
| epoch boundary | — | — | ✔ |

Collapsing them into one "is a break" flag would have made every death a clock knot and every
zone transition a character epoch.

### The §6b block is enforced, not remembered

`measure_dict` gains `layer ∈ (observed, derived)`, `derivation`, `depends_on`, `ingest_block`,
`block_ref`, `semantics_status ∈ (settled, contested, unknown)`. Two `BEFORE INSERT` triggers
(`trg_block_derived_trial_measurement`, `trg_block_derived_session_ledger`) `RAISE(ABORT)` on any
measure carrying a non-NULL `ingest_block`.

`attacks_per_kill` is registered and **BLOCKED**, citing the verification §6b swings-vs-activations
question. `skill_use_count` is `semantics_status='contested'` but **not** blocked — raw counts are
observed values and ingest fine. `total_score` and `dps_field` are `unknown` per D-3.
Unblocking is one `UPDATE measure_dict SET ingest_block=NULL`.

### `fixture_trial.segmentation` joins the unique key

§5 asked for `fixture_trial.segmentation ∈ S1/S2/S3`. Adding it as a plain column would have
collided with `UNIQUE (fixture_set_id, trial_ordinal)` the moment two segmentations covered one
set. It is now `UNIQUE (fixture_set_id, segmentation, trial_ordinal)`, and `v_set_spread` /
`v_ledger_continuity` / `v_differential` group and self-join on it — without that, the first S1+S2
ingest would have silently averaged three windowings of the same kills into one "spread".

A fourth value, **`S0-explicit`**, was added and is the default. The seven banked L0 trials are
hand-bracketed by Matt's screenshot pairs; no kill-to-kill rule produced them, and labelling them
`S1` would have been a lie.

### `monster_rank` collision — averted

§5.1 requested `fixture_set.monster_rank`. **That column already exists** (M4) carrying the
corpus-derived GD `monsterClassification` (`Common`). §4.3's rank is a *different quantity* from a
*different instrument* — nameplate colour, `∈ {normal, champion, hero, boss, unknown}`. Writing OCR
into the existing column would have destroyed the M4 bridge evidence. v0.3 adds
`monster_rank_observed` + `_method` + `_evidence` alongside. Disagreement between the two is
**evidence** (an affixed spawn), not an error to reconcile — O-7.

### Other rebuild-forced corrections

- `capture.kind` gains `video-session`, `equipment-doll`, `skill-tree`, `nameplate-tooltip`
  (and `unclassified`, added in M6). `kind` was carrying two axes at once, so **`media_kind`**
  (`still|video|video-frame|text-log`) is now the media axis and `kind` stays the content-role axis.
- `capture.storage_root` — `path` was documented repo-relative; a 13 GB session MP4 will never be
  in the repo.
- `capture.mtime_semantics` — v0.1 documented `mtime_utc` as **transfer** time. For the GP run it
  is demonstrably **capture** time (it aligns to the video timeline at four independent points).
  Same column, two meanings, previously silent. Existing 28 rows backfilled `transfer-time`.
- `capture.pts_ms` / `play_time_ms` / `burst_id` / `parent_capture_id` / `duration_s`.
- `fixture_set.ladder_rung` gains `'GP'`, **plus** `evidence_class ∈ (ladder-calibration,
  distribution-sample)`. §5.1 proposed `rung='GP'`; a general-play set is not a rung on the L0–L5
  constraint ladder — it holds none of L0's constraints by construction. Both columns exist so the
  ladder stays honest and the grade is still expressible.
- `fixture_trial.spans_break_id` → a trial straddling a death or zone transition is excluded from
  `v_fixture_bank_certified` by a JOIN rather than by an analyst remembering.
- `fixture_character.completeness_detail` / `provenance_gap` / `epoch_trigger`.
- `fixture_session.video_start_epoch` (+ method + uncertainty), `playtime_banked_prefix_s`.

### New views

`v_session_ledger_wide` (the observed series, keyed on the game-state clock, exposing the weakest
cross-check and weakest confidence per sample) · `v_measure_interpretability` (what a measure means
in a given session, given that session's controls) · `v_character_provenance` (honest inventory of
what an epoch actually has behind it, including `n_slots_unread`).

### Verification

`integrity_check` ok · `foreign_key_check` CLEAN · 28/7/4 rows preserved across the three rebuilds ·
`v_fixture_bank_certified` = 3 (unchanged) · both ingest-block triggers confirmed to ABORT.

---

## M6 — 2026-07-26 · GP run 01 ingest — the spine, and nothing invented

**Script:** `research/scripts/fixtures_m6_gp_run01_ingest_2026_07_26.py`
**Session:** `GP-gd-2026-07-26-s1` · **Artifacts:**
`/Volumes/reincarnated/visual-artifacts/GD-matt-test/play-test-v1/` (313 PNG + 2 MP4, 13.2 GB)

Ingests the **spine**: 315 `capture` rows with sha256 + mtime + video-timeline placement; 10
`clock_anchor` rows and the 9-segment `clock_map`; the `session_break` set; 12 `session_control`
rows; and every panel digit that has actually been **read by a human at full resolution**.

**No `fixture_character`, `fixture_set` or `fixture_trial` rows are created.** Those need monster
identity and character sheets, which need the OCR pass galadriel owns. A `fixture_set` with a
hypothesised monster would poison exactly the oracle this bank exists to be.

`attacks_per_kill` was not ingested — the M5 trigger would have refused it.

### Timeline placement

`video_start_epoch = 1785096216.5`; `pts_ms = round((mtime − video_start_epoch) × 1000)`. All 313
stills place by mtime arithmetic alone. Banked with `pts_uncertainty_ms = 500`: the *fractional*
video mtime gives `1785103033.4488 − 6816.516667 = 1785096216.932`, 0.43 s later than the banked
constant. gandalf's value is banked as directed and the discrepancy sits inside the uncertainty.

**`play_time_ms` is populated on 4 of 313 stills** and left NULL on the other 309, with
`play_time_method='absent'`. The clock map cannot substitute: up to 19 s of frozen loading time
sits unallocated inside a single segment (see `clock_map.residual_max_ms`) and an engagement lasts
~5 s. Interpolating would be a silent transformation of the join key itself.

### Three qualifications on `play_time_ms`-as-join-key

The ruling is right — video offset is the camera clock and 73.5 s of loading must not be
attributed to gameplay. Three things about it need saying anyway, none of which retires it:

1. **Granularity.** The panel renders `play_time` to **whole seconds**. `play_time_ms` is
   quantised at 1000 ms, an engagement is ~5 s, and an AoE multi-kill puts several kills in one
   tick. `play_time` **cannot order events within a second** — and S1 kill-to-kill segmentation is
   exactly about ordering kill increments. The operative key is the **composite
   `(play_time_ms, pts_ms)`**: `play_time_ms` is the correctness axis (the only one that survives
   the loading discontinuity), `pts_ms` at 16.7 ms is the ordering axis *within* a clock segment.
   Every `session_ledger` and `capture` row carries both.
2. **Not injective.** `play_time` freezes during loading, so many frames map to one
   `play_time_ms` across a zone transition. Lookup by `play_time` alone is one-to-many precisely
   at the breaks — where it matters most.
3. **Save-scoped, not session-scoped.** `play_time` is SAVE-cumulative, so the true key is
   `(save_identity, play_time_ms)`. A second run on this save continues from ~7088 s and orders
   correctly; a run on a **new character restarts at 0 and collides**.
   `fixture_session.save_identity` is NULL here because it was never attested — §2.1 item 9 asks
   for difficulty, starting area and character level, but not for save identity.

### Capture bursts and epoch-boundary candidates

Screenshot mtimes cluster: 59 bursts at a ≤ 8 s gap threshold, banked as `capture.burst_id` /
`burst_ordinal` (a structural fact, independent of what the shots contain). Bursts with **n ≥ 10
and duration ≥ 25 s** are banked as `session_break` rows of kind `epoch-boundary`, `confidence =
'hypothesis'`, `detection_method = 'mtime-burst-inference'` — protocol §2.3 says a boundary costs
~60–90 s of overlapping sheet crops, which is exactly this signature. **Eleven candidates.**
Protocol §7 F-1 predicted 2–4 epoch boundaries; `max_level_achieved` went 1 → 12, so ~11 is the
consistent number and F-1's cost estimate is low by roughly 3×.

Not one pixel was read to produce these. They are hypotheses for galadriel to confirm or drop.
Two known sensitivities, stated rather than tuned away: the last candidate is the §2.5 **END
BLOCK** sheet, which is a character snapshot but not a §2.3 boundary; and two adjacent candidate
pairs sit ~40 s apart and may each be one boundary that the 8 s gap threshold split in two. So the
honest reading is *8–11 boundaries*, and the coincidence with 11 level-ups should not be leaned on.

### The run's counters do not start at zero

Two frames were extracted and read during this ingest — the run video at `pts=14.5` and the smoke
clip at `t=25` — because A6 declares `skill_use_count` and `life_healed` session-scoped and §2.0
permits the smoke to be its own session, which makes that boundary semantically load-bearing.

| counter | smoke @ t=25 | run @ pts=14.5 | run end (shot 352) | **run delta** | used in the verification |
|---|---|---|---|---|---|
| `kills` | 2 | 2 | 882 | **880** | 882 |
| `skill_use_count` total | 8 | 8 | 692 | **684** | 692 |
| …`defaultweaponattack` | 8 | 8 | 74 | **66** | 74 |
| `life_healed` | 16.33 | 16.33 | 12468.06 | **12451.73** | 12468.06 |
| `deaths` | 0 | 0 | 2 | 2 | 2 |
| `max_level_achieved` | 1 | 1 | 12 | — | 1 → 12 ✓ |
| `shield_block_chance` | 15.00 | 15.00 | 18.00 | — | 18.00 |

Two consequences.

**(1) Every bookend delta needs the baseline subtracted.** §6b's ratio is 684 / 880 = 0.777, not
692 / 882 = 0.784 — conclusion unchanged, number corrected. §8's endogenous healing is 12451.73.

**(2) A6's session-scoping split is in question.** `kills` reading 2 at both points is exactly
A6's SAVE-cumulative behaviour. But `skill_use_count` and `life_healed` also survived that
boundary, and A6 classifies them SESSION-scoped and resettable by a menu return. Either Matt did
not return to the menu between the smoke and the run, or the split is wrong. 550.9 s of wallclock
separates the two clips while `play_time` advanced 13 s (358 → 371) — a lot of frozen time for an
unbroken session. Banked as an open question on `fixture_session GP-gd-2026-07-26-smoke`.

**And a live D-1 reproduction, mine.** My first read of the run's head frame used a 460×290 crop
at 2.5× and returned `Number of kills: 0`. The same pixels at 430×90 / 1.6× read `2`. Legible and
wrong, exactly as D-1 warns — and the wrong value was the *more plausible* one, which is what makes
the failure mode dangerous. Only tight reads are banked; `session_ledger.validity_note` records the
crop geometry on every one.

**A second occlusion source.** D-2 named the quest tracker. In the smoke clip the green
`ShowAngerLevels` `[entityId] Action State: X` text renders **over** the PlayStats potion counters
and makes them unreadable. §3.4's priority order (`PlayStats > LogData > ShowAngerLevels`) is
correct and this is the evidence that the conflict is real rather than hypothetical.

### Absent, not inferred

**No `notes.md` was delivered** (protocol §3.5). Therefore: `difficulty` is NULL; starting area is
absent; per-boundary `play_time` jots (§2.3 item 1) and per-transition area names (§2.4) are
absent; and `no-state-modifying-console` is banked `held='unknown'` rather than `'held'`. Three
`session_control` rows carry the gap explicitly so it does not read as an oversight later.

### Verification

`foreign_key_check` CLEAN · **315 captures** (313 stills + 2 videos, all 1920×1080, 313 distinct
sha256 → no duplicate stills) · 59 capture bursts · **10 clock anchors** · **9 clock-map segments**
· **23 session breaks** (2 death + 2 zone-transition + 8 unallocated-clock-loss + 11
epoch-boundary candidates) · **17 session controls** · **49 session-ledger readings** (41 run + 8
smoke) · **0** `fixture_character` / `fixture_set` / `fixture_trial` rows · captures carrying
`play_time_ms` = **5 / 315**, by design. Re-run is idempotent (row counts identical).

Two sessions are written: `GP-gd-2026-07-26-s1` (the run) and `GP-gd-2026-07-26-smoke` (the §2.0
gate clip), because A6 makes that boundary semantically load-bearing.

---

## M7 — 2026-07-26 · schema `fixtures-v0.4` · a trial is a MANY-monster event

**Script:** `research/scripts/fixtures_m7_trial_participant_2026_07_26.py`
**Backup:** `fixtures.db.pre-v0.4-*-backup` · **Class:** additive + one `fixture_trial` rebuild
(7 rows preserved, `v_fixture_bank_certified` still 3).

### The defect

v0.1 defines `fixture_set` as "the N-trial group: **one monster**, one rig, one ladder rung", and
`fixture_trial.fixture_set_id` is `NOT NULL`. Protocol §5.1 carries that hierarchy into the
general-play run — `fixture_set` "partitioned by `(epoch, monster_display_name, monster_level,
monster_rank, area, difficulty)`", `fixture_trial` "one per engagement". **Those two sentences
cannot both hold,** and §5.3 of the same document declares `single-monster` **violated (packs)**.

A pack engagement has several monsters, of several display names, at several levels, of several
ranks. It belongs to several of those partitions *at once*. There are exactly two ways to force it
into one:

- pick a "representative" monster per engagement → **a fabricated identity**
- duplicate the trial into every set it touches → **double-counted engagements**

Both are worse than the problem. Monster participation in an engagement is **many-to-many**, and a
one-to-many parent cannot carry it.

### The fix

- `fixture_trial.fixture_set_id` → **NULLABLE**. A trial can be a window over the session ledger
  with no set. A partial unique index (`WHERE fixture_set_id IS NULL`) keys ledger-derived trials
  on `(session_id, segmentation, trial_ordinal)` instead.
- `fixture_trial.session_id` added, `NOT NULL`. The session is the real parent.
- **`trial_participant`** — one row per monster in the engagement, each with its own
  `monster_display_name` / `monster_level` / `monster_rank_observed` / `identity_method` /
  `role` / `kill_attributed_to`. `identity_method='unidentified'` is first-class: **O-8 pushed
  down from the set to the individual**, which is where §5.4 says most failures will land.
  `kill_attributed_to ∈ (player, pet, dot, retaliation, environment, unknown)` is the attribution
  term §6b explanation 2 needs, and `entity_id` (F4) is the only channel that can *count* pack
  members without identifying them — the target-count term explanation 1 needs.
- **`fixture_set` is unchanged** and still means one monster. L0 is untouched.

New views: `v_trial_participants_rollup`, `v_trial_homogeneous`. The second one matters
philosophically: a general-play engagement that turns out to be single-monster, single-level,
single-rank and fully identified is structurally an L0 fixture — and it is now **discovered by
query** rather than **asserted in order to be storable**.

---

## Cross-seam notes

No engine-side schema change is requested by any migration in this ledger. `fixtures.db` reads
nothing from `reincarnated-engine/data/telemetry.db`.

**The cross-store dependency is now exercised (M4).** `fixture_set.monster_record` /
`monster_bio_record` / `monster_rank` / `monster_race` are all derived from `corpus.db`
(`monster_display_tag` → `gd_monster_record` → `v_gd_monster_bridge`). The join keys are strings
(`.dbr` record paths) as anticipated at landing, so the coupling is by value, not by FK — the two
stores remain physically independent and either can be rebuilt alone. The rebuild ORDER, however,
is now constrained: `corpus.db`'s bridge must exist before `fixtures.db` M4 runs. That order is
written into the rebuild block at the top of this ledger.

The remaining unexercised join is `trial_measurement.measure_subkey` → `exact_skill.record_path`.

---

## M8 — 2026-07-28 · schema `fixtures-v0.5` · the MEASURED-FIXTURE layer

**Commission:** G-3, phase P-1 of run `KC1-2026-07-27` (KIT-CAL-1). Conductor gandalf.
**Charter:** `gandalf/notes/2026-07-27-kit-cal-1-run-charter.md` §1, §2 T-3, §8.
**Scripts** (run in order; each transactional, each idempotent on re-run):

```bash
python3 agentic_orchestration/research/scripts/fixtures_m8_gd_playtest_v1_fixture_2026_07_28.py   # DDL + the two series
python3 agentic_orchestration/research/scripts/fixtures_m8b_engagement_grain_2026_07_28.py        # 106 engagements + quality
python3 agentic_orchestration/research/scripts/fixtures_m8c_rollup_and_fixture_2026_07_28.py      # regime rollup + TTK recompute
python3 agentic_orchestration/research/scripts/fixtures_m8d_fixture_conditions_claims_2026_07_28.py # fixture, targets, conditions, grades
```

**DDL:** `research/scripts/fixtures_v0_5_ddl.sql` · **Backup:** `fixtures.db.pre-v0.5-*-backup`
**Class:** additive (11 new tables, 7 new views, 24 new `measure_dict` keys) + one table rebuild.

### Why `fixtures.db` and not `corpus.db`

Ruling O-1 already separates them, and this ingest is the case the ruling anticipated.
`corpus.db` holds curated **kit knowledge** — what a skill *is*, per the `.arz`. This is a
**measurement of one afternoon**: two OCR readers walking one recording. The join between
them is `measured_fixture.kit_id` → `corpus.db` kit rows, by value, one `ATTACH` away. The
stores stay physically independent, so the calibration run cannot damage the corpus and a
corpus rebuild cannot silently move a fixture.

### What landed

| Grain | Table | Rows |
|---|---|---|
| Build-stable span | `session_regime` | **3** (R1 report-only · R2 fixture · R3 secondary) |
| A named cut into engagements | `segmentation_run` | **1** (`…/S1-gap5s-v1`, status `current`) |
| T-A panel series, 0.5 s | `panel_series_sample` / `panel_series_reading` | **13,633** / **175,985** |
| T-B globe series, 15 fps | `globe_series_frame` | **19,348** (17,183 OK + **2,165 refusals kept**) |
| Engagement | `fixture_trial` (+`trial_measurement`) | **106** (+1,368) |
| Reader quality, three grains | `series_field_quality` | **1,761** |
| Regime rollup | `regime_stat` | **329** |
| Fixture identity / contract | `measured_fixture` / `fixture_target` | **3** / **11** |
| Declared holes | `fixture_condition` | **19** (9 high · 7 moderate · 3 low) |
| Evidence grades | `evidence_claim` | **14** (5 MEASURED · 2 DERIVED · 3 ATTESTED · 1 INFERRED · 3 UNVERIFIED) |

Per regime, on the segmentation of record: **R1 13 engagements / 43 kills · R2 77 / 647 ·
R3 16 / 190** — the verdict §3 table reproduced cell-for-cell from the banked rows.

### The four constraints, made structural rather than documentary

1. **Regime-partitioned, never pooled.** `regime_stat.regime_id` is an FK to `session_regime`,
   which holds only real build-stable spans. There is no `ALL` row to point at, so a pooled
   table is not a thing you have to remember not to build — it is a thing you cannot insert.
   Verified: the insert fails `FOREIGN KEY constraint failed`.
2. **`life_healed`'s rejection rate rides as a column.** `series_field_quality` carries
   `n_present / n_accepted / n_rejected_nonmonotonic / n_missing` at **session, regime and
   engagement** grain, and the rejected reads themselves are banked with their raw value in
   `panel_series_reading.value_raw`. Nothing was smoothed; nothing was interpolated.
3. **Coverage travels with every intake figure.** `measure_dict.requires_coverage` plus two
   `RAISE(ABORT)` triggers make a NULL coverage on a coverage-bearing figure unrepresentable.
   Verified: the insert fails with the named message.
4. **Evidence grades are first-class.** `evidence_claim` carries WHO said it, WHEN, and the
   **empirical criterion** that would move it. Devotion-zero is ATTESTED (Matt 2026-07-28)
   with `upgrade_criterion` naming the R-KC1-4 `.gdc` probe. Grades also ride on
   `regime_stat`, `trial_measurement`, `session_regime.boundary_grade` and `session_control`.

And the fifth: **kills/engagement is not the headline.** `fixture_target.tier` = `provisional`
with `gate_ref` = the G-2b decomposition. `measure_dict.semantics_status` = `contested`.
`v_fixture_accountability` shows the tier beside every target, so no consumer can read the
number without reading its standing.

### Re-ingestion tolerance (the G-2b question, answered in the schema)

A re-segmentation is **a new `segmentation_run` row, never an UPDATE.** `fixture_trial` gained
`segmentation_id`, and the ledger-scoped unique index was re-keyed onto it, so two cuts of the
same session can each hold an `e007`. `regime_stat` and `measured_fixture` are both keyed on
`segmentation_id`. A consumer that pinned one keeps reading exactly what it read before.

Concretely, when HALT H-1 rules a different grain: insert the new `segmentation_run`, re-run
M8b/M8c against it, flip the old row to `status='superseded'` with `superseded_by`, and
re-point `measured_fixture.segmentation_id`. **The two series underneath are untouched** —
they are the measurement; everything above them is a partition of it. That is the whole reason
the 13,633 panel samples and 19,348 globe frames were banked rather than just the rollup.

### Four things found while ingesting that the sources did not say

**(1) The totals gate is FRAME coverage, not DELTA coverage — and the two disagree.** My first
pass stored delta coverage on the intake figures. An independent recompute of the coverage-gated
totals then **disagreed with galadriel's rollup**: R2 n=63 instead of 62, R3 n=10 instead of 9,
and the R3 mean moved **163.3 → 188.4**. The gate is on frame coverage. Both quantities are
real and neither is "the" coverage, so the store now holds both:
`trial_measurement.coverage` = frame coverage (the gate coverage — filtering `>= 0.80`
reproduces the inclusion sets exactly), and `series_field_quality.covered_s / wallclock_s` =
the delta family. After the correction all three regimes **AGREE** on n / mean / median / max.
Discipline #11 earned its keep here: the disagreement only existed because the rollup was
recomputed rather than trusted.

**(2) `life_healed`'s 3.1% is a run-wide average that hides a 5× regime skew.**
Banked at regime grain: **R1 0.20% · R2 1.26% · R3 15.15%** of present reads. The noise is
concentrated almost entirely in R3 — the same regime that carries the coverage hole, and the
regime whose figures rest on nine engagements. The headline rate is not wrong; it is flat
where the substrate is not.

**(3) The verdict's "3.1%" sits between two defensible denominators.** 413 rejections is
**3.198%** of the 12,913 present reads and **3.029%** of the 13,633 samples. This store
records the counts and lets `v_series_rejection` show both rates. It does not choose.

**(4) The R2/R3 boundary is DERIVED, not MEASURED.** The verdict grades everything MEASURED.
But the poison-DoT boundary comes from a gear-equip event that **brackets** to `play_time`
6052–6282 — a 230 s band — and 6052 is the band's lower edge. The bracket is measured; its
collapse to a point is a derivation, and it can move up to 230 s of engagements between R2
and R3. `session_regime.boundary_grade` reads **DERIVED** for R3 and MEASURED for R2, and
`EC-DOT-BOUNDARY-6052` names the criterion that would settle it.

### One defect closed in passing

`trial_measurement`'s inline `read_method` CHECK had frozen the v0.1 nine-value list while
`read_method_dict` grew to fifteen. Any honest `video-frame-ocr` provenance would have been
forced into a wrong bucket. The table was rebuilt (179 rows preserved) with the CHECK replaced
by an **FK to the dictionary**, so the two cannot drift again. **`character_stat` carries the
same latent drift and was left alone** — out of scope here, logged for a later pass.

### Verification

`foreign_key_check` **CLEAN** · `integrity_check` **ok** · DB 51 MB · re-run of all four
scripts is idempotent (row counts identical).

Closure checks that passed: panel `kills` endpoint **882** vs segmentation total **880** —
they agree exactly once the 2 pre-run kills are subtracted (control `counters-start-at-zero`
VIOLATED, banked as `C-COUNTERS-NONZERO`). Regime table reproduced cell-for-cell. Per-field
accepted/rejected counts match `ta-full-2fps-summary.json` **exactly on all twelve fields**.
Coverage-gated intake totals **AGREE** with `tb-rollup.json` on all three regimes after the
coverage-semantics correction above.

### ADR-004 + reversibility

No engine-telemetry change; star-lord's ledger is unaffected. `fixtures.db` still reads nothing
from `reincarnated-engine/data/telemetry.db`. Reversible: `fixtures.db.pre-v0.5-*-backup`
restores the exact PRE state. The `.db` remains gitignored — **the four scripts plus the DDL
are the durable record**, and both source capture directories are committed, so a byte-
equivalent rebuild needs no `/Volumes` mount (unlike M6).

### Known limits of the guards

The pooled-regime guard is an **FK**, and SQLite enforces foreign keys **per connection**
(`PRAGMA foreign_keys=ON`, off by default in the CLI). A consumer that opens the file with FKs
off can insert a pooled row. The `requires_coverage` guard is a **trigger** and holds
unconditionally. Named here rather than left to be discovered.

---

## M9 — 2026-07-28 · schema `fixtures-v0.6` · the KC1 rulings land as structure

**Commission:** elrond amendment pass, fired non-gating from charter §12.2 item (d),
run `KC1-2026-07-27`. **Charter:** `gandalf/notes/2026-07-27-kit-cal-1-run-charter.md`
§11 (my G-3 landing as recorded), §12 (rulings R-KC1-7…12, Matt-ratified verbatim:
*"Ratified on all six rows, cascade"*).

**Script:** `research/scripts/fixtures_m9_kc1_ruling_amendments_2026_07_28.py`
**Backup:** `fixtures.db.pre-v0.6-*-backup` (+ `.md5.txt`)
**Class:** semantics + vocabulary. **No new measurement was ingested.** Four table
rebuilds (CHECK widening only — column lists byte-identical to v0.5), one new table,
four new columns, three new `measure_dict` keys, four new `fixture_target` rows, three
new `fixture_condition` rows, two superseded/successor `evidence_claim` pairs, four
views. Idempotent; re-run verified as a no-op.

### The design question M9 actually turned on

Three rulings arrived. Two of them (retirement, boundary upgrade) look like value
edits. They are not — each one needed a **new axis** before it could be recorded
honestly, and the temptation each time was to overload an existing column instead.

**(1) Retirement is not a semantics status.** The obvious move was
`measure_dict.semantics_status = 'retired-as-target'`. That column answers *"do we
know what this number means?"* — and for `kills_per_engagement` the answer is still
**contested**, exactly as M8 banked it: it is a composite of two kit quantities and one
player quantity. Retirement answers a different question: *"is the sim held to it?"*
Two questions, two columns. M9 adds **`measure_dict.target_standing`**
(`structural-accountability-target` / `secondary-corroboration` / `retired-as-target` /
`declared-non-target` / `not-a-target`) with `target_standing_ref` for provenance, and
leaves `semantics_status` alone. A measure can be perfectly understood and not a target;
it can be a target and contested. Collapsing them would have hidden one behind the other.

**(2) `DERIVED-NONIDENTIFYING` is stronger than `DERIVED`, not weaker.** M8 graded the
R2/R3 boundary DERIVED because the gear bracket 6052–6282 collapses to its lower edge.
Charter §11.3 says more: there is **no combat between `play_time` 5808 and 6475** — a
667 game-second gap (last kill 5808 / engagement 89; next kill 6475 / engagement 90;
`dps` falls to 0 at 5814 and does not resume until 6282). Every candidate boundary in
that interval **partitions the engagement data identically**. So the placement is
uncertain *and provably immaterial*. "DERIVED" alone invites a precision worry that does
not exist. The grade vocabulary now carries the distinction on `session_regime`,
`evidence_claim` and `fixture_condition.cause_grade`. R2 keeps `MEASURED` — its
*identity-determining* edge is the lower one, the C-2 build break at 1134 — with the
non-identifying note appended so nobody has to rediscover why the grades differ.

**(3) The grain is a property of the instrument, so it needs its own table.**
R-KC1-8 makes the engagement grain **instrument-canonical**: not a fact about this
fixture and not RDR design ontology, but a versioned property of the shared harness,
applied identically to GD-OCR, sim-adapter and Godot-OCR ledgers. A bare
`harness_version` string column would have recorded the *label* and lost the *content*.
M9 adds a **`harness_version` table** whose row is what `harness-v1` **means** —
encounter rule, burst rule, `params_json`, where the code of record lives, which ledgers
it applies to, and its **declared limits as part of its identity rather than a footnote**
(19.2% of combat-state time outside the padded windows: 240 s of 1,250 s across 27
stretches; the death-counter increment at `play_time` 2837 invisible to every instrument,
the one at 5152 inside both; the dps-span/E family deferred to v2). `segmentation_run`
gains `harness_version` (FK) + `grain_role`, so the grain travels with every partition
below it. `source_agnostic` is banked **0** — that flag is the acceptance test for
galadriel's routed refactor (§12.2 item a), not a claim already true.

### What changed, table by table

| Table | Change |
|---|---|
| `harness_version` | **NEW.** 1 row: `harness-v1`, status `current`, `source_agnostic=0` |
| `segmentation_run` | `+harness_version` (FK), `+grain_role`; existing cut → `harness-v1`/`encounter`; **+1 row** for the burst unit (below) |
| `measure_dict` | `+target_standing`, `+target_standing_ref`; **+3 keys** (A/B/C); 1 retired, 3 marked structural, 4 marked secondary |
| `fixture_target` | tier CHECK widened to 7; 4 rows `primary`→`secondary-corroboration`, 1 `provisional`→`retired`, **+4 rows** (3 structural-primary, 1 non-target) |
| `session_regime` | `boundary_grade` CHECK `+DERIVED-NONIDENTIFYING`; R3 upgraded |
| `evidence_claim` | `grade` CHECK `+DERIVED-NONIDENTIFYING`; 2 superseded, **+2 successors** |
| `fixture_condition` | `condition_kind` `+data-gap`, `cause_grade` `+DERIVED-NONIDENTIFYING`; 2 amended, **+3 rows** |
| views | `v_fixture_accountability` + `v_regime_stat_conditioned` recreated; `v_measurement_join_key` + `v_harness_ledger` new |

**Target slate on `GD-R2-werewolf` after M9** (`v_fixture_accountability`, ordered by tier):

| target_key | tier | measure_key | rows behind it |
|---|---|---|---|
| `a_step_multikill_emergence` | structural-primary | `kills_per_kill_event` | **0** |
| `b_dot_tail` | structural-primary | `kill_events_per_burst` | **0** |
| `gear_step_survivability` | structural-primary | `hp_max_observed` | 101 (trial grain) |
| `ttk_shape` · `damage_intake_total` · `damage_intake_rate` · `hazard_tail` | secondary-corroboration | — | 8 / 8 / 8 / 1 regime rows |
| `damage_per_kill` · `per_kill_attack_cost` | report-only | — | 1 / 0 |
| `c_bursts_per_encounter` | **non-target** | `bursts_per_engagement` | 0 |
| `kills_per_engagement` | **retired** | `kills_per_engagement` | 8 regime · 106 trial |

### The gap, declared rather than filled — and why that was the right call

**A and B are named as the accountability targets and are NOT in this store.** The
21 measure keys at regime grain do not include A, B or C. They exist and are computed —
in G-2b's committed capture, `galadriel/captures/2026-07-28-gd-playtest-v1-g2b/`:
`g2b-abc-factors.csv` carries A/B/C per regime with confidence intervals at **three**
burst thresholds (b = 1.0, 1.5, 2.0), and `g2b-per-engagement.csv` carries
`n_bursts_b*` / `active_s_b*` / `travel_s_b*` per engagement.

Copying those numbers in would have been cheap and wrong for this pass. M9 is a
**semantics amendment**; ingesting a new measurement family is a measurement pass with
its own Gate-0 reproduction obligation (M8's Discipline #11 lesson earned exactly here:
recomputing rather than trusting the rollup is what surfaced the frame-vs-delta coverage
disagreement). So the gap is banked three ways, none of them a sentence in a document:

1. `segmentation_run` row **`…/S1-burst1.5s-v1`**, status `candidate`, `n_engagements`
   NULL, `grain_role='pack-proxy-burst'` — the burst unit exists as a **declared-empty
   partition**, so A and B have an address before they have values.
2. Condition **`C-AB-NOT-INGESTED`** (new kind `data-gap` — distinct from
   `coverage-hole`, which is footage the instrument missed; this is a quantity the store
   is *accountable to* but does not hold), naming the exact source files and the M10
   remedy, including *bank all three burst thresholds so the b-sensitivity is visible
   rather than chosen*.
3. `v_fixture_accountability` carries `n_regime_rows` / `n_trial_rows` / `condition_ids`
   per target, so **the emptiness is visible in the same row as the target**. A consumer
   reading the slate sees `structural-primary … 0 … C-AB-NOT-INGESTED`, not a target that
   looks satisfied.

Nothing is blocked today: R-KC1-12 makes G-5's first act a **PRESENT/ABSENT signature
grading**, not a numeric comparison.

### Discharges, with lineage kept

- **`C-SEG-GRAIN-UNRULED` → `accepted`** (not `resolved`). The original hazard text —
  gap>5 s is simultaneously the most permissive defensible threshold *and* the only one
  reaching §1's 100–250 band (>8 s → 75, >10 s → 67) — is retained **verbatim**, with the
  discharge appended as a marked block. What discharges it: the accountability targets no
  longer depend on the encounter boundary (A grain-invariant, B burst-defined, C a
  declared non-target). The residual pressure applies to the **reporting unit only** and
  is now a documented property of a versioned instrument. `accepted` rather than
  `resolved` deliberately — `affects_measure_keys` is still accurate for the
  reporting-unit figures and should keep riding on those rows in the conditioned view.
- **`C-KPE-PROVISIONAL` → `superseded`**, by new **`C-KPE-RETIRED`** (`open`). The T-1
  gate cleared, and the confound turned out to be *structural rather than removable*. The
  caution does not lapse; it changes character. Keeping it `open` on a successor row is
  what preserves the do-not-headline warning on the 106 banked rows — marking the old one
  `resolved` would have silently dropped it out of `v_regime_stat_conditioned`.
- **`EC-DOT-BOUNDARY-6052` → `EC-DOT-BOUNDARY-NONIDENTIFYING`** (`supersedes` FK set).
- **`EC-SEGMENTATION-GRAIN` → `EC-HARNESS-V1-GRAIN`**. Note this is a **dissolution, not
  an upgrade**: the old claim asked whether gap>5 s is the *correct* definition of an
  engagement, and R-KC1-8 rules that is not a question with a truth value. Graded
  `ATTESTED` — it is a ruling, so its authority is its source; `upgrade_criterion` names
  harness-v2 via the Godot calibration leg.
- **`C-HARNESS-V1-LIMITS`** banked `accepted` — R-KC1-8's declared limits surface
  alongside every other condition instead of living only in the harness row.

### The cross-ledger join surface (R-KC1-7 / R-KC1-8)

`v_measurement_join_key` is the structural like-for-like surface: `(harness_version,
grain_role, ledger_lane, ledger_adapter, regime_key, measure_key, target_standing,
statistic, value_num, coverage, evidence_grade)`. A sim-adapter or Godot-OCR ledger
banked here (or `ATTACH`ed) exposes the same columns; the comparison is an equi-join on
`(harness_version, grain_role, measure_key)`. Ledgers on different harness versions do
not join — which is the point, and is now checkable rather than remembered.
`v_harness_ledger` shows every segmentation grouped under its harness version.

**Design note on placement.** `harness_version` lives on `segmentation_run` **only** —
one source of truth — and reaches `regime_stat` / `fixture_trial` / `measured_fixture`
through their existing `segmentation_id` FK, surfaced by the views. Denormalising it onto
each partition table would have made the join a one-hop convenience at the cost of a
drift surface; the grain is a property of the *cut*, and that is where it belongs.

### Verification

`foreign_key_check` **CLEAN** · `integrity_check` **ok** · all four rebuilds preserved
their row counts exactly (3 / 14 / 11 / 19) · re-run of the script is a **no-op**
(state-guarded rebuilds skip; row writes are `ON CONFLICT DO UPDATE` and marked-block
appends fire once).

Closure check: `v_measurement_join_key` reproduces `kills_per_engagement` mean
**3.3077 / 8.4026 / 11.875** for R1/R2/R3 — cell-identical to G-2b's `abc_decomposition`
column, now travelling with `target_standing='retired-as-target'` attached.

### ADR-004 + reversibility

No engine-telemetry change; star-lord's ledger untouched; `fixtures.db` still reads
nothing from `reincarnated-engine/data/telemetry.db`. Two cross-seam dependencies are
**recorded, not assumed**: (a) galadriel's source-agnostic harness refactor is the
acceptance test for `harness_version.source_agnostic=1`; (b) the star-lord/gamora
sim-adapter ledger must emit `harness_version` to join here at all — that is a schema
expectation on their side and should reach them via knight-rider with the G-4 adapter-spec
addendum. Reversible: `fixtures.db.pre-v0.6-*-backup` restores the exact PRE state. The
`.db` remains gitignored — **the script plus this entry are the durable record**, and a
rebuild reproduces the amended state with no `/Volumes` mount.

### Carried forward

- **M10:** ingest A/B/C onto `…/S1-burst1.5s-v1` (all three burst thresholds; Gate-0
  recompute from `g2b-per-engagement.csv`, do not trust the rollup). Closes
  `C-AB-NOT-INGESTED`.
- **Still open from M8:** `character_stat` carries the same latent `read_method` CHECK
  drift that `trial_measurement` had; untouched here, still logged.
- **Guard limit, restated:** the pooled-regime guard is an **FK**, enforced per
  connection. A consumer opening the file with `PRAGMA foreign_keys=OFF` can still insert
  a pooled row. The `requires_coverage` trigger holds unconditionally.
