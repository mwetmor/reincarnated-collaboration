# L0 fixture schema — DRAFT v0.1 (gap 5)

**Agent:** elrond (data steward) · **Commissioner:** gandalf (gap 5, `2026-07-25-gd-three-goal-end-state-and-twin-analysis.md` §6)
**Date:** 2026-07-25 · **Type:** SCHEMA DRAFT. No database created. No DDL applied. No writes to `corpus.db`.
**Status:** for gandalf review. Every §9 open question is genuinely open; none is rhetorical.

**Inputs governing:**
- `agentic_orchestration/gandalf/notes/2026-07-25-gd-live-probe-2-synthesis.md` (field-list seed §6.1; trial table §2)
- `agentic_orchestration/gandalf/notes/2026-07-25-gd-live-probe-1-synthesis.md` (rig verdict)
- `agentic_orchestration/research/knowledge/gd/live-probe-2/` — **raw evidence, governs over the synthesis**
- `agentic_orchestration/elrond/notes/2026-07-25-gd-attestation-scope-census.md` (33-IN state roster; J4)
- `agentic_orchestration/skill_handoff_2026-07-25.md` §2.3 (the L0–L5 ladder)

> ### ⚠ READ §7 FIRST IF YOU ARE SHORT ON TIME
> I re-read all six PlayStats panels at full resolution before designing against them. **Nine of the
> numbers in probe-2 synthesis §2 are wrong**, including two that are load-bearing for the J4 anchor:
> the player **levelled 5→6 between trial 1 and trial 2**, and the `defaultweaponattack` counter is
> **427/429/431/433/435**, not 627/629/633/635. There is also an **unattributed off-trial kill between
> trials 2 and 3**. Corrections in §7.1; consequences in §8. This is why the schema stores *readings*,
> not deltas.

---

## 1. What this schema is for

Three consumers, one shape:

| Consumer | Reads | Needs |
|---|---|---|
| **G3-A fixture bank** | oracle trials (Matt's sittings) | durable, source-anchored, re-readable |
| **G3-B differential harness** | oracle trials **and** sim runs, side by side | *identical* row shape across both lanes |
| **Q47 bar ruling** | per-fixture-set variance | N-trial spread queryable, not just point outcomes |

**The single most important design decision follows from consumer 2:** the oracle lane and the sim
lane are **not two schemas**. They are one schema with a `lane` discriminator. The differential
becomes a self-join on `fixture_set_id` across lanes, not a bespoke comparison script. Anything a sim
cannot populate is either (a) marked oracle-only in the measure dictionary, or (b) not in the schema.

---

## 2. The observable surface, stated exactly

The GD live oracle exposes **no per-hit damage anywhere**. What it exposes:

| Channel | Vocabulary | Grain | Sim can emit? |
|---|---|---|---|
| **PlayStats panel** | ~11 named counters, session-cumulative | per screenshot (before/after) | YES — sim keeps the same counters |
| **`character.LogData true` console** | `Idle · Fidget · Moving · Attack · Flying · Dying` | per-entity transition, timestamped by eye | **PARTIALLY — see §6.3** |
| **Anger overlay** (`ShowAngerLevels`) | `AlertBeforePursue · Startup · followtheleader` | per-entity, current state | YES — these are `ControllerMonster` states |
| **Matt's hand notes** | fight-seconds band, HP-cost band | per trial | YES (sim emits exact; oracle emits band) |
| **HP globe / screenshots** | current/max HP | per screenshot | YES |

Three structural facts the schema is built around:

1. **Every panel number is a session-cumulative reading, not a per-trial quantity.** Deltas are
   *derived*. Store readings; derive deltas in a view. (§8.1 shows why this is not pedantry.)
2. **The console trace and the overlay speak different vocabularies** (§6.3). Conflating them would
   corrupt the G1-C state-confirmation ledger.
3. **The DPS field is a recent-window meter** whose validity depends on capture latency (§8.4). It is
   a *conditionally valid* measurement, and the condition must be a column.

---

## 3. Where it lives — recommendation

**Recommend: a new store, `agentic_orchestration/research/curated/fixtures.db`**, not additive tables
in `corpus.db`. Rationale:

| Consideration | Verdict |
|---|---|
| Lifecycle | `corpus.db` is a *curated corpus* on schema v2.0 with a 417 KB migration ledger and a heavy backup-per-write discipline. The fixture bank grows one Matt sitting at a time and will be written by an autonomous run (`L0-CLOSE`). Mixing write cadences is how migration ledgers become unreadable. |
| Blast radius | An autonomous run writing into `corpus.db` puts 574 curated kits inside its blast radius. A separate file makes the run's write scope physically bounded. |
| Joins | Cross-DB joins are one `ATTACH` away. The join keys are strings (`.dbr` record paths, `kit_id`), already the convention in `exact_skill.record_path`. Nothing is lost. |
| Provenance conventions | **Inherit them verbatim** — `source_version` composite edition pin, `adapter`, `schema_version`, `created_date`, `*_prov`. Same discipline, separate file. |

Its own migration ledger: `research/curated/MIGRATION-fixtures.md`, sibling to the existing
`MIGRATION-*.md` family. **Open question O-1** if gandalf prefers one-DB.

---

## 4. Table shape — the seven tables

```
fixture_session        one Matt PC sitting (or one sim batch)
  └── fixture_character   player character state snapshot  (the G2 key INPUT)
  └── capture             screenshots / console dumps / log files   [ORACLE-ONLY]
  └── fixture_set         the N-trial group: one monster, one rig, one ladder rung
        └── fixture_set_constraint   per-rung constraint attestations (held / not-held / unknown)
        └── fixture_trial            ONE FIGHT
              ├── trial_measurement  every number, as a READING, with provenance   ◄ the core
              └── trial_trace        every observed state token, with its channel
measure_dict           controlled vocabulary for trial_measurement.measure_key
```

### 4.1 `fixture_session`

| Field | Type | Notes |
|---|---|---|
| `session_id` | TEXT PK | `gd-live-2026-07-25-s2`, `sim-L0-<runid>` |
| `lane` | TEXT | `gd-live` \| `sim` — **the discriminator** |
| `session_date` | TEXT | ISO date |
| `operator` | TEXT | `matt` / agent id |
| `game_edition_pin` | TEXT | composite pin per `gd-edition-pin-2026-07-24` convention: edition label + depot + manifest id + `arz_sha256`. **NULL for the round-2 rows — not captured.** |
| `game_build_string` | TEXT | in-game version string if screenshotted |
| `difficulty` | TEXT | `normal`/`veteran`/`elite`/`ultimate` — **UNKNOWN for round 2**; materially changes monster stats |
| `container` | TEXT | `main-campaign` \| `custom-game` \| `crucible` |
| `save_identity` | TEXT | character save name/slot; the continuity key across sittings |
| `console_flags` | TEXT | JSON: `{"LogData":true,"PlayStats":true,"ShowAngerLevels":true}` |
| `rig_version` | TEXT | which probe sheet / procedure was executed |
| `raw_notes_path` | TEXT | repo-relative |
| `capture_dir` | TEXT | repo-relative |
| `sim_config_ref` | TEXT | sim lane only: engine tag + key version + seed |
| `notes` | TEXT | |

### 4.2 `fixture_character` — the G2 key input

| Field | Type | Notes |
|---|---|---|
| `character_id` | TEXT PK | |
| `session_id` | TEXT FK | |
| `snapshot_ordinal` | INT | **a session can hold several** — level-ups mid-session mint a new snapshot (§8.2) |
| `valid_from_playtime_s` | INT | in-game Play Time at which this snapshot became true |
| `char_level` | INT | |
| `mastery_1` / `mastery_2` | TEXT | |
| `hp_max` / `energy_max` | REAL | |
| `oa` / `da` | REAL | offensive/defensive ability — **the PTH formula inputs (R-H5)** |
| `armor_avg` | REAL | |
| `weapon_record` | TEXT | `.dbr` path if known |
| `weapon_dmg_min` / `weapon_dmg_max` | REAL | |
| `attack_speed_pct` | REAL | |
| `resist_json` | TEXT | JSON map of the 9 resist channels |
| `devotion_json` | TEXT | |
| `skill_bar_json` | TEXT | |
| `gear_json` | TEXT | |
| `completeness` | TEXT | `full-sheet` \| `partial` \| `level-and-hp-only` \| `unknown` |
| `capture_id` | TEXT FK | the character-sheet screenshot, if one exists |

> **This table is 90% NULL for round 2 and that is the schema's loudest signal.** The key (G2) is a
> function *of* the character sheet. Not one character-sheet screenshot exists. Everything derivable
> from these three trials about per-hit damage is derivable only up to an unmeasured character.
> One `character.ShowStats`-equivalent screenshot per sitting closes it permanently. → **O-4**

### 4.3 `fixture_set` — the N-trial group

| Field | Type | Notes |
|---|---|---|
| `fixture_set_id` | TEXT PK | `L0-zombie-a01-devilscrossing-01` |
| `session_id` | TEXT FK | |
| `character_id` | TEXT FK | the snapshot in force **for the whole set** — a level-up splits the set |
| `ladder_rung` | TEXT | `L0`…`L5` (handoff §2.3) |
| `monster_record` | TEXT | `.dbr` path — **the identity join to `.arz`** |
| `monster_identity_method` | TEXT | `spawn-command-verbatim` \| `screenshot-nameplate` \| `area-roster-inference` \| **`assumed-unverified`** |
| `monster_identity_evidence` | TEXT | verbatim spawn command / nameplate text / reasoning |
| `monster_level` | INT | **the `charLevel` that J4's bio formulas actually take.** NOT the player's level. NULL for round 2. |
| `monster_level_method` | TEXT | `nameplate` \| `area-band-inference` \| `unknown` |
| `monster_source` | TEXT | `spawned` \| `world` |
| `pack_size` | INT | 1 at L0 |
| `engagement_mode` | TEXT | `pre-aggroed` \| `from-idle` \| `unknown` |
| `area_name` | TEXT | `Devil's Crossing` etc. — proxy for monster level band |
| `intended_n` / `actual_n` | INT | N-trial spread bookkeeping |
| `purpose` | TEXT | free text |

### 4.4 `fixture_set_constraint` — the rung's constraints, attested per set

| Field | Type | Notes |
|---|---|---|
| `fixture_set_id` | TEXT FK | |
| `constraint_key` | TEXT | `single-monster` · `melee-only` · `no-pack` · `no-flee` · `fight-to-death` · `pre-aggroed` · `no-potions` · `no-player-death` |
| `held` | TEXT | `held` \| `violated` \| **`unknown`** |
| `evidence` | TEXT | how we know |

PK `(fixture_set_id, constraint_key)`. **`unknown` is a first-class value.** A rung constraint that
was never checked must not read as satisfied. (The retired no-CC test-character constraint —
expired 2026-07-25 — belongs here as a historical `constraint_key` with an `expired` note rather
than being deleted; annex precedent.)

### 4.5 `fixture_trial` — one fight

| Field | Type | Notes |
|---|---|---|
| `trial_id` | TEXT PK | `L0-zombie-a01-dc-01/t1` |
| `fixture_set_id` | TEXT FK | |
| `trial_ordinal` | INT | 1..N |
| `lane` | TEXT | denormalized from session for query convenience; CHECK matches session |
| `outcome` | TEXT | `monster-killed` \| `player-died` \| `monster-fled` \| `aborted` \| `timeout` |
| `t_start_playtime_s` / `t_end_playtime_s` | INT | **in-game Play Time is the trial clock** (§8.5) |
| `before_capture_id` / `after_capture_id` | TEXT FK | oracle-only; NULL on sim lane |
| `contaminated` | INT | 0/1 |
| `contamination_reason` | TEXT | `second-monster-joined` · `warp-pull` · `potion-used` · `off-trial-activity-in-window` · `ledger-discontinuity` |
| `notes` | TEXT | |

Deliberately **thin**. Every number lives in `trial_measurement`. Rationale in §5.

### 4.6 `trial_measurement` — the core table

| Field | Type | Notes |
|---|---|---|
| `trial_id` | TEXT FK | |
| `measure_key` | TEXT FK → `measure_dict` | controlled vocabulary — **no free-text keys** |
| `phase` | TEXT | `before` \| `after` \| `during` \| `derived` |
| `value_num` | REAL | point value, or **band low** |
| `value_num_hi` | REAL | band high; NULL when the reading is a point |
| `value_text` | TEXT | for categorical measures (`hp_cost_band` = `sliver`) |
| `unit` | TEXT | denormalized from `measure_dict` for read convenience |
| `read_method` | TEXT | **the data-quality flag** — see below |
| `uncertainty_abs` | REAL | e.g. ±1 digit at capture resolution |
| `capture_id` | TEXT FK | which screenshot attests it; NULL if hand-noted or sim-emitted |
| `verbatim` | TEXT | **the raw string as it appeared** — `"137 min 48 sec"`, `"HP cost 15-20"` |
| `validity_flag` | TEXT | `valid` \| `window-expired` \| `superseded` \| `suspect` |
| `validity_note` | TEXT | |

PK `(trial_id, measure_key, phase)`.

**`read_method` vocabulary** (this is the dispatch's per-field data-quality requirement, made
queryable rather than prose):

| Value | Meaning |
|---|---|
| `screenshot-fullres` | read from the banked PNG at native resolution — **highest confidence** |
| `screenshot-downscaled` | read at reduced resolution; digits carry ±1 |
| `screenshot-illegible` | present in frame, not readable |
| `hand-noted-point` | Matt wrote a number |
| `hand-noted-band` | Matt wrote a range (`1-2 s`, `15-20`) |
| `inferred-adjacent-trial` | taken from the neighbouring trial's reading — **not an observation** |
| `sim-emitted` | produced by the sim lane |
| `derived` | computed by a view from other rows |
| `absent` | the panel/log does not carry it |

**Rule: `inferred-adjacent-trial` rows may never be used as evidence for a continuity check** — that
is circular. §8.1 is exactly the failure this rule prevents.

### 4.7 `trial_trace` — the FSM observations

| Field | Type | Notes |
|---|---|---|
| `trial_id` | TEXT FK | |
| `seq` | INT | ordering within the trial |
| `channel` | TEXT | **`anger-overlay` \| `logdata-console` \| `sim-controller-emit` \| `sim-anim-emit`** |
| `entity_ref` | TEXT | which entity the line was tagged to; `player` / monster instance id |
| `trace_token` | TEXT | **verbatim from the source** — `Fidget`, `followtheleader`, `Moving` |
| `controller_state` | TEXT | the mapped 33-IN roster name; **NULLABLE** |
| `mapping_status` | TEXT | `identity` \| `case-normalized` \| `inferred-mapping` \| **`unmapped`** |
| `vocab_status` | TEXT | `in-roster-33` \| `out-by-attestation-5` \| `needs-join-2` \| **`not-in-40-state-table`** |
| `t_offset_s` | REAL | seconds from trial start; NULL when not timeable |
| `duration_s` | REAL | e.g. the AlertBeforePursue beat |
| `duration_method` | TEXT | `hand-noted-band` \| `frame-count` \| `sim-tick` |
| `capture_id` | TEXT FK | |
| `verbatim_line` | TEXT | the whole console line |

**`trace_token` and `controller_state` are two columns on purpose.** §6.3 explains why collapsing
them would have already produced one wrong banked claim.

### 4.8 `measure_dict` — the vocabulary

| Field | Type |
|---|---|
| `measure_key` TEXT PK · `label` TEXT · `unit` TEXT · `value_kind` (`counter`/`gauge`/`band`/`categorical`) · `panel_field` TEXT (verbatim PlayStats label, NULL if not from the panel) · `lane_availability` (`both`/`oracle-only`/`sim-only`) · `ladder_rung_introduced` TEXT · `definition` TEXT · `confounds` TEXT |

`lane_availability` **is** the dispatch's "every field should be one a sim run can also populate, or
be explicitly marked oracle-only" — enforced as data, checkable by `SELECT`.

---

## 5. Why the measurements are a long table and not columns

The obvious alternative is a wide `fixture_trial` with `play_time_delta_s`, `kills_delta`,
`life_healed_delta`, … columns. I recommend against it, on four grounds:

1. **Ladder stability.** L1 adds projectile speed and range bands; L2 adds aggro radius and telegraph
   duration; L3 adds attack-token spacing. A wide table needs a schema migration per rung — five
   migrations we can see coming. The long table needs five `measure_dict` INSERTs.
2. **Per-field data quality is the requirement.** `read_method` + `uncertainty_abs` + `capture_id`
   attach to *each number*. In a wide table that is three shadow columns per measure.
3. **Readings, not deltas.** §8.1 demonstrates that storing deltas loses the information needed to
   detect ledger discontinuity. Before/after is naturally two rows, one column.
4. **Bands are native.** `1-2 s` and `15-20 HP` are ranges, not points. `value_num`/`value_num_hi`
   handles both without nullable pairs multiplying across a wide table.

The EAV failure mode (uncontrolled keys) is closed by the `measure_dict` FK. Ergonomics are restored
by views:

```sql
CREATE VIEW v_trial_wide AS ...   -- pivots the common measure_keys into columns
CREATE VIEW v_trial_delta AS      -- after - before, per measure, with worst-case read_method
CREATE VIEW v_set_spread AS       -- n, min, max, mean, stdev per (fixture_set_id, measure_key)  ◄ Q47
CREATE VIEW v_ledger_continuity AS -- before(n+1) vs after(n) per cumulative counter  ◄ §8.1
CREATE VIEW v_differential AS      -- oracle lane ⋈ sim lane on (fixture_set_id, measure_key)  ◄ G3-B
```

`v_set_spread` is the N-trial-spread requirement (twin note §4: *"fixture schema must record N-trial
spreads, not single outcomes"*). It is a view because spread is **derived** — recomputable from
readings, never stored.

---

## 6. Vocabularies

### 6.1 `measure_dict` seed — L0

| `measure_key` | panel field | unit | kind | lane |
|---|---|---|---|---|
| `play_time` | Play Time | s | counter | both |
| `total_score` | Total Score | pts | counter | oracle-only |
| `deaths` | Number of deaths | count | counter | both |
| `kills` | Number of kills | count | counter | both |
| `health_potions_used` | Health potions used | count | counter | both |
| `mana_potions_used` | Mana potions used | count | counter | both |
| `max_level_achieved` | Max. level achieved | level | gauge | both |
| `dps_field` | Damage per second | dmg/s | gauge | both† |
| `skill_use_count` | Skills Used (per record) | count | counter | both‡ |
| `life_healed` | Life healed | HP | counter | both |
| `shield_block_chance` | Shield block chance | % | gauge | both |
| `fight_seconds` | — | s | band | both |
| `hp_cost_band` | — | — | categorical | both |
| `hp_cost_abs` | — | HP | band | both |
| `hp_current` / `hp_max` | HP globe | HP | gauge | both |
| `capture_latency` | — | s | gauge | oracle-only |

† `dps_field` is a **recent-window** meter; see §8.4 — the sim must reproduce the *window*, not just
a DPS number, for this to be comparable. Flagged as a G3-B design input, not resolved here.
‡ `skill_use_count` is the one measure needing a second key dimension. Two options — **O-2**:
(a) qualify the key: `skill_use_count:records/skills/default/defaultweaponattack.dbr`;
(b) add a nullable `measure_subkey` column holding the `.dbr` path.
I lean **(b)** — it keeps `measure_dict` finite and makes the `.dbr` path a joinable string to
`corpus.db.exact_skill.record_path` rather than a substring.

### 6.2 State vocabulary — check against the 33-IN roster

`trial_trace.controller_state` vocabulary-checks against the census roster
(`elrond/notes/2026-07-25-gd-attestation-scope-census.md` §8): 33 IN, 5 OUT-BY-ATTESTATION, 2
NEEDS-JOIN. A live observation of an OUT state is a **re-entry event** for the annex — it must be
recordable, not rejected. Hence `vocab_status` is a column, not a CHECK constraint.

### 6.3 ★ The two channels do not share a vocabulary — a finding

Round 1 observed `AlertBeforePursue`, `Startup`, `followtheleader` — **all three are
`ControllerMonster` states** (census rows 40, 2, 13). Round 2's `LogData` console observed
`Idle · Fidget · Moving · Attack · Flying · Dying`. Checked against the 40-state table:

| Token | In the 40-state table? |
|---|---|
| `Idle` | ✅ row 1 |
| `Attack` | ✅ row 3 |
| `Dying` | ✅ row 11 |
| `Moving` | ❌ — the table has **`Move`** (row 18). Near-miss, not identity. |
| `Fidget` | ❌ **absent from all 40 rows.** Plausibly the animation-layer name behind `Emote` (row 39) — *inference, not banked*. |
| `Flying` | ❌ **absent from all 40 rows.** Unexplained. |

**Consequence:** the probe-2 synthesis §1.2 banks *"`Fidget` is now LIVE-ATTESTED (census row
confirmation #4)"*. **`Fidget` is not a census row.** It cannot confirm one. The claim is
well-intentioned and structurally wrong: rounds 1 and 2 read **two different instrument channels**,
and only the anger-overlay channel speaks `ControllerMonster`. The `LogData` channel appears to emit
from an animation/actor-state layer.

This is decisive for G3, not cosmetic. Our sim emits **controller** states. Only the overlay channel
is directly comparable. The `LogData` channel needs a `trace_token → controller_state` mapping table,
each row of which is an inference requiring its own confirmation. `mapping_status = 'unmapped'` is
the honest state for `Fidget` and `Flying` today. → **O-3**

---

## 7. The three round-2 trials as first rows

### 7.1 Full-resolution re-read — the corrected panel ledger

Method: `sips` crop of the panel region from each banked 1920×1080 PNG, upscaled 3×, read directly.
Reproducible in one line; the crop is `-c 380 500 --cropOffset 40 1420`. All twelve readings below
are `read_method = 'screenshot-fullres'`.

| shot | Play Time | deaths | kills | HP pot | mana pot | max lvl | DPS | kick | **defaultweaponattack** | Life healed |
|---|---|---|---|---|---|---|---|---|---|---|
| (13) T1 before | 137 min 48 s | 0 | **161** | 0 | 0 | **5** | 0.00 | 1 | **427** | 2245.44 |
| (14) T1 after | 137 min 54 s | 0 | **162** | 0 | 0 | **5** | **19.17** | 1 | **429** | 2245.44 |
| (15) T2 before | 140 min 52 s | 0 | 162 | 0 | 0 | **6** | 0.00 | 1 | **429** | **2258.09** |
| (16) T2 after | 141 min 47 s | 0 | 163 | 0 | 0 | 6 | **0.00** | 1 | **431** | **2292.86** |
| (17) T3 before | 142 min 37 s | 0 | **164** | 0 | 0 | 6 | 0.00 | 1 | **433** | 2311.37 |
| (18) T3 after | 142 min 43 s | 0 | **165** | 0 | 0 | 6 | **19.43** | 1 | **435** | 2311.37 |

**Corrections against probe-2 synthesis §2** (raw evidence governs):

| # | Synthesis said | Full-res reading | Severity |
|---|---|---|---|
| C1 | `defaultweaponattack` 627→629→631→633→635 | **427→429→…→435** | digit misread (6 for 4); Δ=+2 per trial **survives** |
| C2 | "Player level 6 (Max-level field)" | **level 5 at trial 1; 6 at trials 2–3** | **HIGH — the player levelled mid-set** |
| C3 | T1 play-time Δ ~14 s | **6 s** (137:48→137:54) | HIGH — Δ was estimated, not read |
| C4 | T3 play-time Δ ~8 s | **6 s** (142:37→142:43) | moderate |
| C5 | T2 Life healed ~+24 (2258.69→2282.66) | **+34.77** (2258.09→**2292.86**) | **HIGH — the damage-taken proxy is 45% larger** |
| C6 | T3 after DPS ~19.45 | **19.43** | trivial |
| C7 | T1 after DPS 19.15 | **19.17** | trivial |
| C8 | "All three trials are clean single-kill deltas" | **kills 163 → 164 between T2-after and T3-before: an off-trial kill** | **HIGH — §8.1** |
| C9 | (not stated) | **T2-after DPS reads 0.00** — the window expired | HIGH — §8.4 |

Kick counter static at 1 throughout — the synthesis's cleanest claim, **confirmed**.

### 7.2 The rows

**`fixture_session`** — one row:

```
session_id            gd-live-2026-07-25-s2
lane                  gd-live
session_date          2026-07-25
operator              matt
game_edition_pin      NULL          -- NOT CAPTURED
game_build_string     NULL
difficulty            NULL          -- NOT CAPTURED; materially affects monster stats
container             main-campaign -- INFERRED from quest tracker; confidence low
save_identity         NULL
console_flags         {"LogData":true,"PlayStats":true}
rig_version           gandalf/pc-handoff/2026-07-25-gd-probe3-SIMPLE-v2.md
raw_notes_path        agentic_orchestration/research/knowledge/gd/live-probe-2/GD-console-notes-v2-raw.md
capture_dir           agentic_orchestration/research/knowledge/gd/live-probe-2/
```

**`fixture_character`** — **two rows, not one** (C2):

| character_id | snapshot_ordinal | valid_from_playtime_s | char_level | hp_max | oa | da | completeness |
|---|---|---|---|---|---|---|---|
| `gd-2026-07-25-s2/c1` | 1 | ≤ 8268 (137:48) | **5** | NULL | NULL | NULL | `level-only` |
| `gd-2026-07-25-s2/c2` | 2 | ≤ 8452 (140:52) | **6** | **282** | NULL | NULL | `level-and-hp-only` |

`hp_max = 282` is read from the HP globe in shot (17) (`282/282`) and applies to `c2` only.

**`fixture_set`** — **two sets, not one** (the level-up splits them):

| fixture_set_id | character_id | rung | monster_record | identity_method | monster_level | area | actual_n |
|---|---|---|---|---|---|---|---|
| `L0-gd-s2-set1` | `…/c1` | L0 | **NULL** | **`assumed-unverified`** | NULL | (wilderness — minimap differs from set 2) | 1 |
| `L0-gd-s2-set2` | `…/c2` | L0 | **NULL** | **`assumed-unverified`** | NULL | Devil's Crossing vicinity | 2 |

`monster_identity_evidence` for both: *"Matt's raw notes record `game.Spawn
"records/creatures/enemies/zombie_a01.dbr"` under a separate heading from the trials. No note, and no
nameplate in any of the six panel screenshots, states which monster each trial fought. The
identification of these trials with `zombie_a01` is an assumption."* → **O-5**

**`fixture_set_constraint`** — the honest picture:

| set | constraint | held | evidence |
|---|---|---|---|
| both | `single-monster` | `unknown` | no world-view screenshot at engagement |
| both | `melee-only` | `unknown` | monster identity unattested |
| both | `no-pack` | `unknown` | — |
| both | `no-flee` | `unknown` | — |
| both | `fight-to-death` | `held` | kills +1 per trial |
| both | `pre-aggroed` | `unknown` | not noted |
| both | `no-potions` | **`held`** | potion counters static at 0 across all six panels |
| both | `no-player-death` | **`held`** | deaths static at 0 |
| set2 | `no-off-trial-activity` | **`violated`** | +1 kill, +2 attacks between T2-after and T3-before |

**Six of nine read `unknown`.** That is not a schema defect; it is the schema doing its job.

**`fixture_trial`** — three rows:

| trial_id | set | ord | outcome | t_start_s | t_end_s | before/after cap | contaminated |
|---|---|---|---|---|---|---|---|
| `L0-gd-s2-set1/t1` | set1 | 1 | `monster-killed` | 8268 | 8274 | (13)/(14) | 0 |
| `L0-gd-s2-set2/t1` | set2 | 1 | `monster-killed` | 8452 | 8507 | (15)/(16) | 0 |
| `L0-gd-s2-set2/t2` | set2 | 2 | `monster-killed` | 8557 | 8563 | (17)/(18) | **1** — `ledger-discontinuity` upstream |

**`trial_measurement`** — trial 1 shown in full (33 rows across the three trials):

| measure_key | subkey | phase | value_num | value_hi | read_method | capture | verbatim |
|---|---|---|---|---|---|---|---|
| `play_time` | | before | 8268 | | screenshot-fullres | (13) | `137 min 48 sec` |
| `play_time` | | after | 8274 | | screenshot-fullres | (14) | `137 min 54 sec` |
| `kills` | | before | 161 | | screenshot-fullres | (13) | `161` |
| `kills` | | after | 162 | | screenshot-fullres | (14) | `162` |
| `deaths` | | before/after | 0 | | screenshot-fullres | (13)/(14) | `0` |
| `health_potions_used` | | before/after | 0 | | screenshot-fullres | (13)/(14) | `0` |
| `max_level_achieved` | | before/after | 5 | | screenshot-fullres | (13)/(14) | `5` |
| `dps_field` | | before | 0.00 | | screenshot-fullres | (13) | `0.00` |
| `dps_field` | | after | 19.17 | | screenshot-fullres | (14) | `19.17` |
| `skill_use_count` | `…/defaultweaponattack.dbr` | before | 427 | | screenshot-fullres | (13) | `: 427` |
| `skill_use_count` | `…/defaultweaponattack.dbr` | after | 429 | | screenshot-fullres | (14) | `: 429` |
| `skill_use_count` | `…/defaultkickattack.dbr` | before/after | 1 | | screenshot-fullres | (13)/(14) | `: 1` |
| `life_healed` | | before/after | 2245.44 | | screenshot-fullres | (13)/(14) | `2245.44` |
| `fight_seconds` | | during | **1** | **2** | **hand-noted-band** | — | `Trial 1: 1-2s` |
| `hp_cost_band` | | during | — | — | hand-noted-point (`none`) | — | `HP cost 0` |
| `hp_cost_abs` | | during | 0 | 0 | hand-noted-point | — | `HP cost 0` |

Trials 2 and 3 follow the same shape. The three distinguishing rows:

| trial | measure | value | read_method | verbatim |
|---|---|---|---|---|
| set2/t1 | `hp_cost_abs` | **15 – 20** | `hand-noted-band` | `HP cost 15-20` |
| set2/t1 | `life_healed` Δ (derived) | **+34.77** | `derived` | 2258.09 → 2292.86 |
| set2/t1 | `dps_field` after | **0.00**, `validity_flag = window-expired` | screenshot-fullres | `0.00` |

**`trial_trace`** — the honest state is **zero rows attributable to these three trials.** The
observed tokens (`Idle · Fidget · Moving · Attack · Flying · Dying`) come from
`colsole-fight-data-test.png`, which is the `killMonsters` sweep test — a *different* event.
Six session-level observations exist and belong to a session-scoped trace with `trial_id = NULL`:

| channel | trace_token | controller_state | mapping_status | vocab_status |
|---|---|---|---|---|
| `logdata-console` | `Idle` | `Idle` | identity | in-roster-33 |
| `logdata-console` | `Attack` | `Attack` | identity | in-roster-33 |
| `logdata-console` | `Dying` | `Dying` | identity | in-roster-33 |
| `logdata-console` | `Moving` | `Move` | **case/near-miss inferred** | in-roster-33 |
| `logdata-console` | `Fidget` | **NULL** | **`unmapped`** | **`not-in-40-state-table`** |
| `logdata-console` | `Flying` | **NULL** | **`unmapped`** | **`not-in-40-state-table`** |
| `anger-overlay` (round 1) | `AlertBeforePursue` | `AlertBeforePursue` | identity | in-roster-33 |
| `anger-overlay` (round 1) | `Startup` | `Startup` | identity | in-roster-33 |
| `anger-overlay` (round 1) | `followtheleader` | `FollowLeader` | case-normalized | in-roster-33 |

Round 1 + round 2's `AlertBeforePursue` beat observations are `duration_s` 2–3 (close) and ~3 (far),
`duration_method = hand-noted-band` — trace rows with `trial_id = NULL`, `entity_ref = 'zombie'`.

---

## 8. Where the three trials strained the design

Six places. Each one changed the schema.

### 8.1 The panel is a session ledger, and the ledger is not continuous

`kills` reads 163 at T2-after and **164** at T3-before. `defaultweaponattack` reads 431 then **433**.
`life_healed` reads 2292.86 then **2311.37**. Between two trials 50 seconds apart, **one kill, two
attacks, and 18.51 HP of healing happened outside any trial.**

Had the schema stored *deltas* (as the synthesis table does), this would be invisible — each trial's
Δ is a clean +1/+2 and the corruption sits entirely in the gap. It is visible only because before(n+1)
and after(n) are **both stored as readings**.

→ **Schema consequences:** (a) readings, never deltas; (b) `v_ledger_continuity` view;
(c) `contamination_reason = 'ledger-discontinuity'`; (d) `read_method = 'inferred-adjacent-trial'`
barred from continuity evidence — the synthesis's "~629" and "~633" were adjacency inferences, and
inferring T3-before from T2-after would have *manufactured* the continuity it was meant to test.

### 8.2 The character changed mid-set — a fixture-set is not a session

Max level reads **5** in shots (13)/(14) and **6** from (15) on. The quest tracker also changes
(*Waking to Misery / Lost Survivor* → *Helping Out*) and the minimap is a visibly different region.

Trial 1 was fought by a **different character** — different level, different HP pool, different OA/DA,
plausibly a different weapon — in a **different area**, therefore against a plausibly
different-levelled monster. Grouping all three as one N=3 spread would compute variance across a
**covariate change**, and Q47's bar would be ruled against a number that is partly a level-up.

→ **Schema consequences:** `fixture_character.snapshot_ordinal` with `valid_from_playtime_s`;
`fixture_set.character_id` pinned per set; **the level-up splits the trials into two sets (N=1 and
N=2)**. Also a proposed integrity check: no `fixture_set` may span two character snapshots.

*(This also softens the synthesis's headline. "One zombie = one kill = exactly two basic attacks"
holds across **level 5 and level 6, in two areas** — arguably a stronger finding than stated, but it
is a finding about **robustness**, not about **consistency of a controlled fixture**.)*

### 8.3 Monster identity is the primary FK and it is not attested

`fixture_set.monster_record` is the join to the `.arz` — the whole point of the fixture bank. For
these three trials it is **NULL**. Matt's raw notes record the spawn command under one heading and
the trials under another, with no statement connecting them; no panel screenshot shows a nameplate.

The synthesis §3 derives *"zombie_a01 effective HP at charLevel≈6 ∈ (1×, 2×] player basic-hit
damage"* — which requires (a) the monster to be `zombie_a01` and (b) its `charLevel` to be 6.
Neither is attested. And **(b) is a category error**: my census J4 shows GD monster HP comes from
`characterAttributeEquations` bio records keyed on **the monster's own `charLevel`**
(`bio_hero_standard_01`: `characterLife = '((charLevel*18)^1.50)-20'`). The player's level 6 — which
is really 5 for trial 1 — is not that variable. A level-4 and a level-8 zombie differ in HP by ~2.6×
under that formula.

→ **Schema consequences:** `monster_identity_method` with `assumed-unverified` as a first-class
value; separate `monster_level` + `monster_level_method` columns, never derived from
`fixture_character.char_level`. → **O-5**

### 8.4 The DPS field is conditionally valid, and the condition is capture latency

T1-after reads **19.17** (6 s window), T3-after reads **19.43** (6 s), T2-after reads **0.00**
(55 s). One self-consistent reading: the meter reports over a recent window that had **expired** by
the time T2's after-shot was taken. Idle readings return 0.00 for the same reason.

A schema that stored `dps_after = 0.00` for T2 with no qualifier would enter a **false zero** into
the fixture bank, and a differential harness would score it as a catastrophic sim/oracle divergence.

→ **Schema consequences:** `trial_measurement.validity_flag = 'window-expired'`; a
`capture_latency` measure key (oracle-only); and a flag for G3-B that the sim must reproduce the
*window semantics*, not merely emit a DPS number. → **O-6**

### 8.5 Wall-clock is not the trial clock

All eight probe-2 files carry mtimes within a 20-second span (15:40:52–15:41:10) — those are
**transfer** times, not capture times. The only monotonic clock available is the in-game
`Play Time` counter.

→ **Schema consequences:** `t_start_playtime_s` / `t_end_playtime_s` in in-game seconds;
`capture.mtime_utc` recorded but explicitly labelled transfer-time; a session-level
`capture_clock_source = 'in-game-playtime'`.

### 8.6 `life_healed` is a proxy with three named confounds

The synthesis calls it *"a usable damage-taken proxy"*. It is — conditionally:

1. It accrues **+12.65 between T1-after and T2-before with zero kills** — and that interval contains
   the level-up. A level-up raises max HP, putting the character below the new max and triggering
   regen. *(Hypothesis, not banked; it fits, and it is falsifiable by a level-up capture.)*
2. It reads **exactly 0.00** across T1's and T3's 6-second windows, so it does **not** accrue at full
   HP. Good — that is what makes it a proxy at all.
3. T2's +34.77 spans 55 seconds, most of it post-fight regen. It measures *damage taken during the
   window*, not *damage taken in the fight*, and it collides with Matt's hand-noted 15–20 (a ~2×
   disagreement, ~12.3% vs ~5–7% of a 282 pool).

→ **Schema consequences:** `measure_dict.confounds` as a real column, populated for `life_healed`
with all three; both the hand-noted band and the panel delta stored, **neither reconciled**. When two
instruments disagree, the schema's job is to preserve the disagreement. → **O-7**

---

## 9. Open questions for gandalf

| # | Question | My lean |
|---|---|---|
| **O-1** | Separate `fixtures.db`, or additive tables in `corpus.db`? | **Separate** (§3) — bounded blast radius for the `L0-CLOSE` autonomous run. Your call; I implement either. |
| **O-2** | `skill_use_count` sub-key: qualified `measure_key`, or a `measure_subkey` column? | **`measure_subkey`** — keeps `measure_dict` finite; makes the `.dbr` path joinable to `exact_skill.record_path`. |
| **O-3** | The `LogData` channel speaks a **non-`ControllerMonster`** vocabulary (§6.3). Does the `Fidget` = census-confirmation-#4 claim get withdrawn, and does a `trace_token → controller_state` mapping table become a G1-C deliverable? | Withdraw the specific claim; keep the finding (the trace is real and valuable). The mapping table is new scope — I'd rather surface it than absorb it. |
| **O-4** | One character-sheet screenshot per sitting — can this be added to the next probe sheet? | **Yes, please.** It is the single highest-value one-shot addition. The key (G2) is a function of the character sheet; we have level and HP and nothing else. |
| **O-5** | Given §8.3, should the J4 anchor in probe-2 synthesis §3 be re-stated with the identity and monster-level assumptions explicit before gamora evaluates the 720 formula strings? | Yes — otherwise gamora evaluates at the wrong `charLevel` **and** possibly the wrong record. This is cheap now and expensive later. |
| **O-6** | Does G3-B commit to reproducing the DPS field's **window semantics**, or do we drop `dps_field` from the comparable set and treat it as oracle-side colour? | Weak lean to **drop from the comparable set** — the window is undocumented and reverse-engineering it costs more than it yields, given `fight_seconds` + `kills` already bracket TTK. |
| **O-7** | When Matt's hand-note and the panel disagree (§8.6: 15–20 vs 34.77), does anything reconcile them, or do both stand with the disagreement recorded? | **Both stand.** Reconciling would be a silent transformation. But it is worth one probe-sheet line: *"note HP globe reading immediately after the killing blow."* |
| **O-8** | Should `fixture_set` require `monster_record NOT NULL` (making these three rows *provisional* until identity is confirmed), or admit NULL with `assumed-unverified`? | **Admit NULL.** Rejecting them would discard our only trials. But `v_fixture_bank_certified` should filter to identity-attested sets, and Q47's bar should be ruled against the certified view. |
| **O-9** | The retired no-CC constraint (expired 2026-07-25) — carry as an `expired` `constraint_key` row, or omit? | **Carry**, per annex precedent. Constraints that expired are part of the fixture's interpretive context. |
| **O-10** | Do we re-read the round-1 `playstats-panel.png` at full resolution the same way, to give the bank a fourth (pre-trial) baseline reading? | Cheap; I'd do it as part of landing the schema. |

---

## 10. DDL sketch

```sql
PRAGMA foreign_keys = ON;

CREATE TABLE fixture_session (
  session_id        TEXT PRIMARY KEY,
  lane              TEXT NOT NULL CHECK (lane IN ('gd-live','sim')),
  session_date      TEXT NOT NULL,
  operator          TEXT,
  game_edition_pin  TEXT,          -- composite pin, gd-edition-pin-2026-07-24 convention
  game_build_string TEXT,
  difficulty        TEXT CHECK (difficulty IN ('normal','veteran','elite','ultimate') OR difficulty IS NULL),
  container         TEXT,
  save_identity     TEXT,
  console_flags     TEXT,          -- JSON
  rig_version       TEXT,
  raw_notes_path    TEXT,
  capture_dir       TEXT,
  capture_clock_source TEXT NOT NULL DEFAULT 'in-game-playtime',
  sim_config_ref    TEXT,
  notes             TEXT,
  adapter           TEXT NOT NULL,
  schema_version    TEXT NOT NULL,
  created_date      TEXT NOT NULL DEFAULT (date('now'))
);

CREATE TABLE fixture_character (
  character_id      TEXT PRIMARY KEY,
  session_id        TEXT NOT NULL REFERENCES fixture_session(session_id),
  snapshot_ordinal  INTEGER NOT NULL,
  valid_from_playtime_s INTEGER,
  char_level        INTEGER,
  mastery_1 TEXT, mastery_2 TEXT,
  hp_max REAL, energy_max REAL, oa REAL, da REAL, armor_avg REAL,
  weapon_record TEXT, weapon_dmg_min REAL, weapon_dmg_max REAL, attack_speed_pct REAL,
  resist_json TEXT, devotion_json TEXT, skill_bar_json TEXT, gear_json TEXT,
  completeness      TEXT NOT NULL CHECK (completeness IN
                      ('full-sheet','partial','level-and-hp-only','level-only','unknown')),
  capture_id        TEXT REFERENCES capture(capture_id),
  UNIQUE (session_id, snapshot_ordinal)
);

CREATE TABLE capture (                      -- ORACLE-ONLY
  capture_id   TEXT PRIMARY KEY,
  session_id   TEXT NOT NULL REFERENCES fixture_session(session_id),
  path         TEXT NOT NULL,               -- repo-relative
  kind         TEXT NOT NULL CHECK (kind IN
                 ('playstats-panel','console-log','world-view','character-sheet','other')),
  label        TEXT,                        -- 'Screenshot (13)'
  sha256       TEXT NOT NULL,
  mtime_utc    TEXT,                        -- TRANSFER time, not capture time (§8.5)
  pixel_w INTEGER, pixel_h INTEGER,
  notes        TEXT
);

CREATE TABLE fixture_set (
  fixture_set_id     TEXT PRIMARY KEY,
  session_id         TEXT NOT NULL REFERENCES fixture_session(session_id),
  character_id       TEXT NOT NULL REFERENCES fixture_character(character_id),
  ladder_rung        TEXT NOT NULL CHECK (ladder_rung IN ('L0','L1','L2','L3','L4','L5')),
  monster_record     TEXT,                  -- .dbr path; NULL admitted, see O-8
  monster_identity_method TEXT NOT NULL CHECK (monster_identity_method IN
                       ('spawn-command-verbatim','screenshot-nameplate',
                        'area-roster-inference','assumed-unverified')),
  monster_identity_evidence TEXT,
  monster_level      INTEGER,               -- the bio-formula charLevel; NEVER the player's level
  monster_level_method TEXT,
  monster_source     TEXT CHECK (monster_source IN ('spawned','world','unknown')),
  pack_size          INTEGER,
  engagement_mode    TEXT CHECK (engagement_mode IN ('pre-aggroed','from-idle','unknown')),
  area_name          TEXT,
  intended_n INTEGER, actual_n INTEGER,
  purpose TEXT
);

CREATE TABLE fixture_set_constraint (
  fixture_set_id TEXT NOT NULL REFERENCES fixture_set(fixture_set_id),
  constraint_key TEXT NOT NULL,
  held           TEXT NOT NULL CHECK (held IN ('held','violated','unknown','expired')),
  evidence       TEXT,
  PRIMARY KEY (fixture_set_id, constraint_key)
);

CREATE TABLE fixture_trial (
  trial_id       TEXT PRIMARY KEY,
  fixture_set_id TEXT NOT NULL REFERENCES fixture_set(fixture_set_id),
  trial_ordinal  INTEGER NOT NULL,
  lane           TEXT NOT NULL CHECK (lane IN ('gd-live','sim')),
  outcome        TEXT CHECK (outcome IN
                   ('monster-killed','player-died','monster-fled','aborted','timeout')),
  t_start_playtime_s INTEGER,
  t_end_playtime_s   INTEGER,
  before_capture_id  TEXT REFERENCES capture(capture_id),
  after_capture_id   TEXT REFERENCES capture(capture_id),
  contaminated       INTEGER NOT NULL DEFAULT 0,
  contamination_reason TEXT,
  notes TEXT,
  UNIQUE (fixture_set_id, trial_ordinal)
);

CREATE TABLE measure_dict (
  measure_key   TEXT PRIMARY KEY,
  label         TEXT NOT NULL,
  unit          TEXT,
  value_kind    TEXT NOT NULL CHECK (value_kind IN ('counter','gauge','band','categorical')),
  panel_field   TEXT,
  lane_availability TEXT NOT NULL CHECK (lane_availability IN ('both','oracle-only','sim-only')),
  ladder_rung_introduced TEXT,
  definition    TEXT,
  confounds     TEXT
);

CREATE TABLE trial_measurement (
  trial_id      TEXT NOT NULL REFERENCES fixture_trial(trial_id),
  measure_key   TEXT NOT NULL REFERENCES measure_dict(measure_key),
  measure_subkey TEXT NOT NULL DEFAULT '',   -- e.g. the skill .dbr path (O-2)
  phase         TEXT NOT NULL CHECK (phase IN ('before','after','during','derived')),
  value_num     REAL,
  value_num_hi  REAL,
  value_text    TEXT,
  unit          TEXT,
  read_method   TEXT NOT NULL CHECK (read_method IN
                  ('screenshot-fullres','screenshot-downscaled','screenshot-illegible',
                   'hand-noted-point','hand-noted-band','inferred-adjacent-trial',
                   'sim-emitted','derived','absent')),
  uncertainty_abs REAL,
  capture_id    TEXT REFERENCES capture(capture_id),
  verbatim      TEXT,
  validity_flag TEXT NOT NULL DEFAULT 'valid'
                  CHECK (validity_flag IN ('valid','window-expired','superseded','suspect')),
  validity_note TEXT,
  PRIMARY KEY (trial_id, measure_key, measure_subkey, phase)
);

CREATE TABLE trial_trace (
  trace_id     INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id   TEXT NOT NULL REFERENCES fixture_session(session_id),
  trial_id     TEXT REFERENCES fixture_trial(trial_id),   -- NULL = session-scoped observation
  seq          INTEGER,
  channel      TEXT NOT NULL CHECK (channel IN
                 ('anger-overlay','logdata-console','sim-controller-emit','sim-anim-emit')),
  entity_ref   TEXT,
  trace_token  TEXT NOT NULL,          -- VERBATIM
  controller_state TEXT,               -- mapped 33-IN roster name; NULLABLE
  mapping_status TEXT NOT NULL CHECK (mapping_status IN
                   ('identity','case-normalized','inferred-mapping','unmapped')),
  vocab_status TEXT NOT NULL CHECK (vocab_status IN
                 ('in-roster-33','out-by-attestation-5','needs-join-2','not-in-40-state-table')),
  t_offset_s   REAL, duration_s REAL, duration_s_hi REAL,
  duration_method TEXT,
  capture_id   TEXT REFERENCES capture(capture_id),
  verbatim_line TEXT
);
```

Views per §5. Schema version `fixtures-v0.1`; `schema_meta` table mirroring `corpus_schema_meta`.

---

## 11. Provenance ledger

**VERIFIED — read directly from the banked PNGs at full resolution:** every number in §7.1. Method:
`sips -c 380 500 --cropOffset 40 1420` on each `Screenshot (NN).png`, `--resampleWidth 1500`, read.
Source images unmodified; crops written to `/tmp`, not to the repo. Nine corrections to probe-2
synthesis §2 recorded in §7.1 rather than silently applied.

**VERIFIED — read directly:** the 40-state roster check in §6.3, against my own census §3 table.
`Fidget`, `Flying`, `Moving` are absent from the 40 `ControllerMonster` state names.

**INFERENCE, labelled, not banked:** (i) `Fidget` ≈ the animation-layer name behind `Emote`;
(ii) the level-up explains the +12.65 off-trial `life_healed` accrual (§8.6); (iii) T2's DPS 0.00 is
window expiry rather than a genuine zero (§8.4). Each is falsifiable by one capture.

**NOT DONE, by scope:** no database created, no DDL applied, no `MIGRATION.md` entry written, no row
written to `corpus.db` or anywhere else. `corpus.db` was opened read-only (`mode=ro`) for schema
convention reference only; mtime unchanged.

---

**Signed:** elrond, 2026-07-25. The oracle keeps a ledger, not a diary — so we store what it reads,
never what we computed from it, and the gaps between the readings turn out to be where the truth was.
