# KC2 LIFT RUN — Wave-1 · elrond curation pass on B2–B8 substrate

> **Run:** KC2 LIFT RUN (charter `agentic_orchestration/gandalf/notes/2026-08-25-kc2-lift-run-charter.md`, ledger L-1) · **Conductor:** gandalf (`RUN-CONDUCTOR`)
> **Seat:** elrond (data steward) · **Date:** 2026-08-25
> **Gate:** schema-valid tables — per-file **PASS / THIN-with-named-absences / HALT**
> **Laws carried:** DR-1 provenance-or-fail · DR-2 rows-not-fields · DR-3 (value, scope, provenance) triples · GL-12 absence-is-declared-not-filled · READ-ONLY on all engine substrate (curated, never edited).

---

## § 0 — PIN VERIFICATION (first move; drifted substrate is not curated)

All seven pinned files re-hashed against charter § 1 **before** any curation. **7/7 MATCH. No HALT.**

Digests below are **derived, not retyped** — each row is `hashlib.sha256(open(path,'rb').read()).hexdigest()`, and the MATCH verdict is a **programmatic substring test against the charter file's own text**, not a visual comparison.

| # | file | sha256 (derived, full) | vs charter § 1 |
|---|---|---|---|
| B2 | `data/kc2/d3_roster_controller_params.csv` | `41abf9da90d45138d0292ae03d8223d2af6f623834c3b3795664783d0c6e997b` | **MATCH** |
| B3 | `data/kc2/pm4_band_b_ehp_by_wave.csv` | `3e82e72b5f35f98f9b30ac46c0aa062c42b804a38ac08791e25d74320ded5024` | **MATCH** |
| B4 | `data/kc2/pe6_crucible_wave_pools_v2.csv` | `bbdc18f12aab8e3788eac229ed1871a88ed7790dc3d1786c509cd26c076e5587` | **MATCH** |
| B5 | `data/kc2/d4c_dot_stacking_decode_README.md` | `63b2e2002bf7264a833d057c8cc0d857920d36f8b43780832f0d943092ffdb2b` | **MATCH** |
| B6 | `data/kc2/d7_control_application_parameters.csv` | `3f2c7250142ec2cdb95f22699f2426f9f1b5bd9faca870d1ee4952e0266b3f06` | **MATCH** |
| B7 | `data/kc2/d9_summon_bodies.csv` | `db6c42c445a21a54f5c18b4843bd85c38b744bae303ea3c6623d3a216e0269bc` | **MATCH** |
| B8 | `data/kc2/d6_player_kit_residual.csv` | `71f2d6fc02e4526d02d85d10f3dd667bf6100b4db6dea8d29c3e4929e00b50bb` | **MATCH** |

> ⚑ **Method note, recorded because it bit me.** The first draft of this table carried hand-typed
> 16-char truncations. **Two of the seven were wrong** (B3 typed `…f88a`, actual `…f98f`;
> B7 typed `…a17b58`, actual `…a21a54`) — transcription noise, in a table whose entire purpose is to
> prove nothing drifted. The verification itself was sound; the *record of it* was not. Regenerated
> derived, per the standing `digests derived-never-retyped` law. A digest a human typed is not a
> digest; it is a claim about a digest.

**Anchor used for "what each lift owes":** the baton-v2 pack's own absence registry,
`src/reincarnated/output/kc2-model-pack-v2-E-s09-cp150-mpol2-20260825_163811/model/provenance.json`,
rows `absence_registry[8..13,15]`. Each verdict below is scored against that row's **own `what` field**, not against my reading of the file name. **This is the whole method:** a table is not "thin" in the abstract — it is thin *for its declared lift purpose*.

---

## § 1 — VERDICT BOARD

| # | block | rows | gate verdict | one-line reason |
|---|---|---:|---|---|
| **B2** | ABS-AI-STATE-MACHINE | 4,081 | **THIN** (3 named absences) | Carries controller **parameters**, not the 43-state **key space / transitions / conditions** the registry names; and it is scoped to the *rolled* roster while B3/B4 lift the *full tier-16 pool*. |
| **B3** | ABS-MONSTER-STAT-BLOCKS | 15,801 | **THIN** (2 named absences) | Registry asks for stat blocks "life, offense, defense, skills, specials". The pin carries **life only** — but it carries it *completely* (tier-16 coverage 466/466). |
| **B4** | ABS-WAVE-ROLL-POOLS | 1,998 | **THIN** (2 named absences, one first-order) | Pool **membership** is complete and clean; the **within-pool member roll rule** (per-slot weight / limit / minPlayerLevel) is absent from the pin **and from the entire `data/kc2` surface**. You cannot roll a pool from this table. |
| **B5** | ABS-DOT-STACKING | prose | **PASS** | Fully decoded, implementably stated, residuals self-declared. The only lift work is transcription into rows. |
| **B6** | ABS-CONTROL-APPLICATION | 43 | **THIN** (1 named absence — and it is *the* row) | Every input to the **concurrency law is present**; the **law itself is not a row**. It is derivable by composing four rows. DR-2 requires it be a row. ⚑ See § 7. |
| **B7** | ABS-SUMMON-BODIES | 216 | **PASS-with-caveat** | Complete, well-graded, self-declaring. One curation hazard: the token `PATH` is **overloaded** between this file and R-L53-2. ⚑ See § 8. |
| **B8** | ABS-DEVOTION-PROCS | 27 | **THIN — most thin of the seven** | Registry asks for "the 8 devotion procs with host bindings, triggers, chances and ICDs". The pin carries **payload rows for 1 devotion** and **zero** binding/trigger/chance rows. Also: two corroborating surfaces say **7**, not 8. ⚑ See § 9. |

**No HALT.** Every thin verdict is accompanied by a named absence row and a named recovery surface, so Wave-2/Wave-3 can proceed against a known shape rather than discovering the hole at build time.

---

## § 2 — THE JOIN-KEY MAP (the part that makes the seven a *pack* and not seven files)

There are exactly **four key spaces** across the seven files. Naming them is most of the curation work.

| key space | canonical form | which files speak it |
|---|---|---|
| **K1 · monster record** | `records/creatures/**/<x>.dbr` | B3 `record` · B4 `roster_records` / `champ_records` (pipe-joined multi-value) |
| **K2 · controller record** | `records/controllers/enemy/controller_<x>.dbr` | B2 `controller` |
| **K3 · wave** | integer 1–200 (`global_wave`) | B3 `wave` (151–170) · B4 `global_wave` (1–200) |
| **K4 · player-side skill record** | `records/skills/**/<x>.dbr` | B7 `source_record_or_rva` · B8 `record` |

### 2.1 K1↔K2 — the bridge B2 does not carry, and its measured cost

**B2 has no monster-record column.** It is keyed on K2 only. Every join from a spawned body to its
AI parameters therefore needs an **external** K1→K2 map. Two exist in `data/kc2`, neither pinned:

| bridge | maps | tier-16 records covered | controllers reached | in B2 |
|---|---:|---:|---:|---:|
| `pm2_tg2_monster_timing.csv` (`record` → `controller`) | 169 | 128 / 466 | 60 | **60 / 60** |
| `kc2_s1_banda_record_inputs.csv` (`record` → `controller_record`) | 895 | 236 / 466 | 59 | 31 / 59 |
| **union** | 964 | **308 / 466** | 91 | 63 / 91 |

`pm2_tg2_monster_timing.csv` is the **rolled-roster** bridge — its 169 records are exactly the
`in_rolled_20w` population B2's own decode note (`d3_controller_groups_decode_README.md` § 1) used as
its roster basis, and it lands **60/60 inside B2**. `kc2_s1_banda_record_inputs.csv` is wider (band A)
and reaches controllers B2 never decoded.

**Measured consequence, tier-16 roll pool (466 distinct records):**

```
  controller resolved AND parameter row present in B2 :  244   (52.4 %)
  controller resolved, NO parameter row in B2         :   64   (13.7 %)
  no K1→K2 bridge exists at all                       :  158   (33.9 %)
```

**This is the single most consequential number in the pass.** B3's registry row already worries in
exactly this shape — *"a runtime whose player kites differently will roll a record this pack has no
block for"* — and B3 turns out to be **fine** (§ 4). It is **B2** that has the hole, and no row
anywhere names it. See absence **A-B2-3**.

### 2.2 K1 — B3 ↔ B4

Clean, and stronger than expected. All **466** distinct monster records reachable from tier-16 pools
(`roster_records` ∪ `champ_records`) are present in B3's 791-record `record` column: **466/466, zero
misses.** Path strings are byte-identical in form; no normalisation is required. This is a
first-class join and should be lifted as one.

The one seam: B4 stores its K1 values as a **pipe-joined string** (` | ` separated) inside
`roster_records` / `champ_records`, positionally parallel to `roster_names` / `champ_names`. That is a
**fields-not-rows** encoding and DR-2 forbids carrying it forward — see § 5's proposed shape.

### 2.3 K3 — the wave axis, and a one-wave scope seam

B3 covers waves **151–170** (tier 16 + tier 17), 790 records × 20 waves. B4 covers **1–200**.
The registry scopes B4 to "waves 150–160". **Wave 150 is tier 15**, and B3 does not carry it: of the
154 distinct records reachable from wave-150 pools, **50 have no B3 row**.

This is a scope seam rather than a defect — B3's declared domain is the *tier-16* roll pool, and on
that domain it is complete. But a Wave-3 consumer who reads "150–160" literally and joins on
`(record, wave)` will get 50 empty joins at wave 150 and no error. Named as **A-B3-2**.

### 2.4 K4 — B7 ↔ B8, via the player kit

B7 and B8 are both keyed on player-side skill records, and they **meet**: B7's Guardian of Empyrion
chain begins at `records/skills/playerclass09/summon_celestialguardian1.dbr`, which is precisely one
of the seven autocast **hosts** in `pm4g_played_kit.csv` (bound to devotion
`records/skills/devotion/tier3_20e_skill.dbr` via controller `cast_@enemyonattack_20%.dbr`).

So **a devotion proc summons one of the two B7 bodies.** B7 and B8 are not independent tables; they
share an edge. Any lift shape that treats them as disjoint loses the fact that Guardian uptime is
*proc-gated*, not player-commanded. This edge is currently carried in **neither pin** — it lives only
in the unpinned `pm4g_played_kit.csv`. Named as **A-B8-2**.

### 2.5 K2 — a second consumer worth knowing about

`d12_roster_anger_parameters.csv` (unpinned, 24 cols) is keyed on the **same K2 controller space** as
B2 and carries the anger/threat parameters B2's decode note explicitly excluded from its own scope
(§ 4 "already-decoded groups"). For the state machine to be liftable as a *machine*, these two
K2-keyed tables want to land as **one** controller-parameter row set with a `group` discriminator,
not two. Noted for star-lord's Wave-3 assembly, not asserted as a requirement.

---

## § 3 — B2 · `ABS-AI-STATE-MACHINE` — schema, and why it is THIN

**Registry `what`:** *"the monster controller state machine — the 43-state key space, its transitions
and their conditions."*

### 3.1 Schema

`d3_roster_controller_params.csv` — 4,081 rows, one per **(controller × field)**. Long/tidy, which is
correct and unusual enough to be worth praising: it is already rows-not-fields.

| column | type | unit / domain | semantics |
|---|---|---|---|
| `controller` | K2 record path | 77 distinct | the `ControllerMonster` record. **Grain key, part 1.** |
| `n_monsters` | int | 1–? (Σ over distinct = 169) | how many rostered monster records bind this controller. A **weight**, not a count of anything in this row — it exists so a consumer can monster-weight a controller-grained histogram. Easy to mis-sum. |
| `group` | enum | 13 values | the `.tpl` field group. One value — `Leader (HIDDEN — not in .tpl)` — is **not a template group**; it is a decoded finding (F-D3-2) wearing a group label. |
| `field` | string | 53 distinct | the record field name. **Grain key, part 2.** |
| `crucible_value` | string (poly-typed) | — | the winning value under the SurvivalMode overlay. Holds ints, floats, bools, enum names and the sentinel `__ABSENT__` in one column. |
| `base_game_value` | string (poly-typed) | — | the base-game winner, for the same field. |
| `owner_archive` | enum | `SurvivalMode{,1,2,3}.arz` | which archive supplies the winner. **77/77 controllers are SurvivalMode-owned** (F-D3-1). |
| `slot` | hex string | `0x2d8`–`0x510`, blank ×385 | the `this+disp` memory slot from `ControllerMonster::Load`. Blank where the field is a `std::string` member or a picklist resolved by string-compare. |

Cell counts, verified: `crucible_value == base_game_value` on **3,430** rows; **651** rows differ.
Zero blank values in either value column (`__ABSENT__` is used, correctly, instead of empty).

**Curation note — poly-typed value columns.** `crucible_value` carries five distinct types plus a
sentinel. This is *right* for a decode deliverable and *wrong* for a lift target: the baton-v3 row
must carry the type explicitly, or every consumer re-derives it by sniffing. See § 3.3.

### 3.2 Named absences

**A-B2-1 · The 43 states are not in this table.** The table carries the **parameters that gate**
transitions (`FleeChance`, `DodgeDelay`, `MaxTimeBeforeRoam`, …). It carries **no state list, no
transition edges, and no transition conditions.** The registry names all three. The 43-state key
space is referenced *by number* in the unpinned decode note (`d3_controller_groups_decode_README.md`
:55 — "`FollowLeader` (#13) and `DefendLeader` (#16) of the 43 states") and individual states are
named across §§ 3.1–3.12 and § 6, but **no enumeration of all 43 exists in `data/kc2`**.

> This is not a criticism of the D-3 lap, which was commissioned on the *field groups* and delivered
> them. It is a statement that **the pin does not cover the registry row**, and Wave-2/Wave-3 must
> either commission the enumeration or lift B2 as a *parameter* block under an honestly narrowed
> `what`. Silently lifting parameters under a "state machine" label would be the failure DR-1 exists
> to prevent.

*Recovery surface:* the four states already declared-unreachable-with-reason
(`Flee` #8, `FollowLeader` #13, `DefendLeader` #16, `Return` #12) and `Patrol` #30
reachable-but-empty, in the decode note § 6.3 — five of 43, free. The remaining 38 need a
`ControllerMonsterState*` export enumeration off `Game.dll`.

**A-B2-2 · 53 fields of a 68-field surface.** The decode note § 1 establishes the surface as
**68 fields** (`controllerai.tpl` 12 + `controllermonster.tpl` 56). The pin carries **53**. The other
15 (Senses / AngerManagement / DistressCalls / Pursuit) were decoded in *earlier* laps and are
partly in the unpinned `d12_roster_anger_parameters.csv`. A consumer reading this file as "the
controller surface" is short 22 %.

**A-B2-3 · Roster-scoped, but the lift purpose is pool-scoped.** Quantified in § 2.1:
**64 of 466** tier-16-rollable records resolve to a controller that has **no row here**, and a
further **158** resolve to no controller at all through any available bridge. If B3 ships the full
tier-16 pool (L-49) and B2 ships 77 rolled-roster controllers, **the two lifted blocks disagree about
which world exists.** That disagreement should be a declared row, not an emergent surprise.

### 3.3 Proposed baton-v3 lift shape

Two row sets, because there are two grains, and collapsing them is how the state machine got lost.

```
ROWSET  controller_param            grain: (controller, field)
  controller_record   TEXT   K2
  group               TEXT
  field               TEXT
  value               TEXT   ── the triple ─┐
  value_type          TEXT   int|float|bool|enum|string|ABSENT
  unit                TEXT   ms|s|m|percent|count|enum|none   (⚑ minSwingPause is
                             AUTHORED in seconds and CONSUMED in ms — carry both, see below)
  scope               TEXT   ── the triple ─┤  "crucible" | "base_game"
  provenance          JSON   ── the triple ─┘  {owner_archive, slot, tpl_default,
                                                engine_default, decode_note_section}
  n_monsters_rolled   INT    weight, NOT a fact about this row
```

Every `(controller, field)` therefore lands as **two rows** — `scope=crucible` and
`scope=base_game` — rather than one row with two value columns. That is DR-2 read strictly, and it
buys something real: F-D3-1's finding ("*any baton row sourced from base-game controller values is
wrong for this fight*") becomes **enforceable by a scope filter** instead of by a reader remembering
which column to take.

⚑ **Unit trap to carry:** `minSwingPause` / `maxSwingPause` are authored in **seconds** and stored by
`ControllerMonster::Load` in **milliseconds** after a `×1000` conversion. The pin carries the authored
value. The row must state `unit=s, unit_consumed=ms, conversion=x1000` or a Godot implementer will
build 0.5 ms swing pauses.

```
ROWSET  controller_state            grain: (state_id)          ⚑ ABSENT — see A-B2-1
  state_id, state_name, reachable(bool), unreachable_reason, provenance
ROWSET  controller_transition       grain: (from_state, to_state, condition_id)   ⚑ ABSENT
```

Both absent rowsets should ship as **explicit absence rows** in the pack — `ABS-AI-STATE-KEYSPACE`
and `ABS-AI-STATE-TRANSITIONS` — with the five already-decoded states populated and the other 38
declared. A partially-populated declared table beats an unmentioned hole.

---

## § 4 — B3 · `ABS-MONSTER-STAT-BLOCKS` — schema, and the good news

**Registry `what`:** *"per-record stat blocks (life, offense, defense, skills, specials) for the
tier-16 roll pool."*

### 4.1 Schema

`pm4_band_b_ehp_by_wave.csv` — 15,801 rows = 790 records × 20 waves + **1 absence row**.

| column | type | unit | semantics |
|---|---|---|---|
| `record` | K1 record path | 791 distinct | the monster record. **Grain key, part 1.** |
| `wave` | int | 151–170 | **Grain key, part 2.** |
| `G_pct` | float | percent | the wave life-modifier (`306.0` at w151 → rising). ⚑ **`306.0` means ×3.06, not ×306** — an unlabelled percent is a foot-gun; the lift row must carry `unit=percent_of_base`. |
| `level_lo` / `level_hi` | int | char level | the spawn-level **band** for that record at that wave. Bands-not-tape, correctly. |
| `ehp_lo` / `ehp_hi` | int | HP | effective HP at `level_lo` / `level_hi`. |
| `life_grade` | enum | `MEASURED` (15,800) / `ABSENT:NO-characterAttributeEquations` (1) | provenance grade. |

**The single non-MEASURED row is exemplary and should be preserved verbatim through the lift:**
`records/skills/nonplayerskillsgdx1/bossskills/pets/krieg_aethertrap.dbr` carries **blank wave,
blank G_pct, blank levels, blank EHP** and `life_grade = ABSENT:NO-characterAttributeEquations`.
That is GL-12 done right — a declared absence occupying a row rather than a silently missing record.
It is also the only row in the file where the blank columns are meaningful, so a naive "drop rows
with nulls" cleaning step deletes the one honest thing in the table. **Do not let it be cleaned.**

### 4.2 Coverage — the finding that closes a registry worry

The registry `why` warns: *"a runtime whose player kites differently will roll a record this pack has
no block for."* **Measured: it will not.** All **466** distinct records reachable from tier-16 pools
are present in B3. **466/466. Zero uncovered.** On the life dimension, B3 is complete for its
declared lift purpose, and the registry's worry can be **retired for life** (not for the other four
dimensions — see A-B3-1).

### 4.3 Named absences

**A-B3-1 · Four of five declared stat dimensions are absent from the pin.** The registry names
"life, offense, defense, skills, specials". The pin carries **life** (as EHP bands). Offense,
defense, skills and specials are absent — though all four exist elsewhere in `data/kc2`, unpinned:

| dimension | recovery surface (unpinned) | shape |
|---|---|---|
| offense (OA/DA) | `pm4o_oa_da.csv` (82 cols) · `pm2_tg2_monster_oa_da.csv` (17 cols) | K1-keyed |
| defense / mitigation | `pm3_measured_defence_sheet.csv` · `pm4l_mitigation_by_body.csv` | K1-keyed |
| skills | `pm2_tg2_skill_tree.csv` (28 cols) | K1 × `tree_index` |
| specials / attack slots | `pm2_tg2_attack_slots.csv` (40 cols) | K1 × `slot` |
| DoT riders (feeds B5) | `pm4i_dot_riders.csv` (40 cols) | K1-keyed |
| body radius (geometry) | `pm4_body_radii.csv` (28 cols) | K1-keyed |

All six are K1-keyed and therefore **join to B3 for free**. The lift is a schema-union problem, not
a decode problem. This is the cheapest large win available in Wave-3.

**A-B3-2 · Wave 150 is absent** (§ 2.3): 50 of 154 wave-150-reachable records have no B3 row.
Scope seam between "tier-16 pool" (B3's real domain) and "waves 150–160" (B4's registry phrasing).
Declare it; do not paper it.

**A-B3-3 · Band scope is unstated in the file.** The filename says `band_b`; nothing inside the table
says so. `pm4i_band_c_ehp_by_wave.csv` (401 records) and `t22_band_a_monster_stats.csv` are siblings
with overlapping K1 spaces. A lifted row that does not carry `band` will silently collide on
re-import. **The band must become a column, not a filename.**

### 4.4 Proposed baton-v3 lift shape

```
ROWSET  monster_stat                grain: (record, wave, stat, level_bound)
  record_path   TEXT   K1
  wave          INT    K3
  band          TEXT   "B"                    ⚑ from filename → column  (A-B3-3)
  stat          TEXT   "ehp" | "oa" | "da" | "resist_<x>" | ...
  level_bound   TEXT   "lo" | "hi"            ⚑ bands-not-tape, as two rows
  value         NUM    ── triple ─┐
  unit          TEXT              │  hp | ability | percent
  scope         TEXT   ── triple ─┤  "wave_modified"   (G_pct already folded in)
  provenance    JSON   ── triple ─┘  {life_grade, G_pct, char_level, source_file, source_sha256}
```

`level_lo/hi` and `ehp_lo/hi` become **two rows** (`level_bound=lo|hi`) rather than four columns.
This is DR-2, and it also makes the band survive the union with the offense/defense tables in
A-B3-1, which use different bound conventions.

`G_pct` moves **into provenance**, not into a value column — it is not a fact about the monster, it
is the transform that produced the value. Keeping it addressable preserves reversibility (raw base
life is recoverable) without inviting a consumer to multiply by it twice.

The `krieg_aethertrap` absence row lifts as `value=NULL, unit=NULL, scope="absent",
provenance={life_grade:"ABSENT:NO-characterAttributeEquations"}` — a **declared** null, which under
GL-12 means not-modelled and never "measured zero".

---

## § 5 — B4 · `ABS-WAVE-ROLL-POOLS` — schema, and the first-order hole

**Registry `what`:** *"pool membership + roll rules for waves 150–160."*

### 5.1 Schema

`pe6_crucible_wave_pools_v2.csv` — 1,998 rows, grain **(global_wave, spawn_point, pool_record)**;
26 columns. Waves 1–200 across tiers 1–20, ten waves per tier, exactly. The 150–160 slice is
**156 rows** over spawn points 1–6 and 117 distinct pools.

| column group | columns | semantics |
|---|---|---|
| **wave axis (K3)** | `global_wave`, `tier`, `tier_wave` | 1–200 / 1–20 / 1–10. Derivable from each other; carry `global_wave` as canonical. |
| **spawn site** | `spawn_point`, `proxy_class`, `proxy_record`, `proxy_archive` | `proxy_class ∈ {Proxy (1,783), ProxyAmbush (215)}` — **ambush is a class on the proxy, not a flag on the wave.** |
| **pool identity** | `pool_record`, `pool_archive`, `pool_kind`, `pool_weight` | `pool_kind ∈ {trash 889, BOSS 488, HERO 320, DEVOTION 213, BOUNTY 88}`. `pool_weight` is the **between-pool** weight at this spawn point. |
| **spawn counts** | `spawn_min`, `spawn_max` | float; the count band for this pool. |
| **champion roll** | `champion_chance`, `champion_min`, `champion_max` | the champion up-roll. |
| **membership (K1)** | `roster_n`, `roster_names`, `roster_records`, `champ_roster_n`, `champ_names`, `champ_records` | ⚑ **pipe-joined multi-value strings, positionally parallel.** |
| **balance flag** | `ignore_game_balance`, `igb_field_state`, `igb_provenance` | `igb_field_state ∈ {PRESENT 1,714, ABSENT 284}` with `igb_provenance ∈ {DB-CITED 1,714, TPL-DEFAULT 284}` — **a per-row provenance grade, already DR-1 shaped.** Good. This is the pattern the other six files should be measured against. |

**Blank-cell audit — clean.** `roster_records` blank on 621 rows, `champ_records` blank on 1,377.
Every blank has `roster_n == 0` / `champ_roster_n == 0` respectively: **zero rows claim members they
do not list.** The blanks fall entirely on `HERO` (320), `DEVOTION` (213) and `BOUNTY` (88) pools —
i.e. pool kinds whose membership resolves through a different limb. Internally consistent; not thin
*as membership data*.

### 5.2 Named absences

**A-B4-1 · ⚑ FIRST-ORDER — the within-pool member roll rule is absent, and absent everywhere.**
`pool_weight` is the weight of *the pool at the spawn point*. It is **not** the weight of a *member
within* the pool. Grim Dawn pool DBRs carry per-slot `name<i>` / `weight<i>` / `limit<i>` /
`minPlayerLevel<i>` — this is directly attested in the run's own lineage
(gandalf run-ledger L-53: *"slot 4 (`name4 = skeleton_d01.dbr`, weight4 75, minPlayerLevel4 45,
**limit4 = 2**)"*). B4 **collapses those slots into a flat pipe-joined name list**, discarding
per-member weight, limit and level gate.

I searched every CSV in `data/kc2` for a column matching `weight1|name1|limit1|minPlayerLevel`:
**zero hits.** The sibling `pe6_pool_ignoregamebalance.csv` is pool-grained, not member-grained.

**Consequence, stated plainly: from the pinned substrate you cannot roll a pool.** You can say which
pool fires at which spawn point on which wave, and how many bodies come out. You cannot say *which
bodies*, except uniformly-at-random over the roster list — which is demonstrably wrong (weights of
75 vs others in the same pool) and which would silently produce a differently-composed fight with
the right body count. **A wrong roll that produces the right count is exactly the kind of error that
survives a census gate.**

*Recovery:* re-extract the pool DBRs' indexed slot arrays. This is a legolas Mode-B lap, not a
curation step, and it is the single highest-value un-commissioned piece I found in this pass.

**A-B4-2 · Roll ORDER and RNG are undocumented.** The table gives roll *parameters*
(`pool_weight`, `spawn_min/max`, `champion_chance`) but no statement of (a) whether pool weights
normalise per spawn point or globally, (b) whether the spawn count is a uniform integer draw over
`[min,max]` or a float, (c) which RNG stream. B2's decode note § 6.2 established that **two distinct
RNG idioms** coexist in this engine (`RandomUniformLocked::IGenerate` vs CRT `rand()%100`, *"except
pet-ignore, which is `%101`"*) — so "assume uniform" is not a safe default in this codebase. Name it.

### 5.3 Proposed baton-v3 lift shape

Four rowsets. The pipe-joined columns **must** decompose — this is DR-2's paradigm case.

```
ROWSET  wave_spawn                  grain: (global_wave, spawn_point, pool_record)
  global_wave, tier, tier_wave, spawn_point,
  proxy_record, proxy_class,               ⚑ ProxyAmbush is a value here, not a wave flag
  pool_record, pool_kind,
  value(pool_weight), scope("spawn_point_relative"), provenance{proxy_archive, pool_archive}

ROWSET  wave_spawn_count            grain: (global_wave, spawn_point, pool_record, bound)
  bound ∈ {min, max}                       ⚑ spawn_min/spawn_max as two rows
  value, unit("bodies"), scope, provenance

ROWSET  pool_member                 grain: (pool_record, member_record, member_class)
  member_class ∈ {roster, champion}        ⚑ the pipe-joins, exploded
  member_record (K1), member_display_name,
  value(member_weight) = NULL,             ⚑ A-B4-1 — DECLARED ABSENT, not defaulted to equal
  member_limit = NULL, member_min_player_level = NULL,
  provenance{source_file, source_sha256, note:"pe6 v2 flattens the pool DBR slot array"}

ROWSET  pool_roll_rule              grain: (pool_record, rule_id)     ⚑ A-B4-2 — mostly absence rows
```

The `pool_member` rowset lands **518 rows for the 150–160 slice / 466 for tier-16**, each with a
**declared-NULL weight**. That is the correct shape: it makes the hole *countable* — a Wave-3 census
can assert "466 member rows, 466 NULL weights, 0 fabricated" — instead of letting an implementer
infer uniform weighting from the absence of a weight column.

---

## § 6 — B5 · `ABS-DOT-STACKING` — **PASS**

**Registry `what`:** *"the DoT application and stacking function."*

The only prose pin of the seven, and the only unambiguous **PASS**. `d4c_dot_stacking_decode_README.md`
states the rule implementably (§ 7), cites every claim to an RVA, records its negatives with the
search that produced them (§ 5 cap fields: *"decided NEGATIVE"* with the per-function immediate-compare
table), and self-critiques six residuals (§ 11). There is nothing to curate; there is only
transcription — which is exactly what "DECODED-NOT-YET-LIFTED" should look like.

### 6.1 The rule, as rows

```
ROWSET  dot_rule                    grain: (rule_id)
  R-DOT-1  timeline_grain      value=100        unit=ms       scope=per(damage_type,attacker)
                               provenance={rva:[0x00207f40,0x0020dc80,0x0020dc30], sites:3}
  R-DOT-2  bucket_count        value="trunc(duration_s * 10)"  unit=buckets
                               scope=per_application  provenance={rva:0x0020d6fe, insn:"cvttss2si"}
           ⚑ TRUNCATES. 3.35 s → 33 buckets → 3.3 s. A real sub-tick loss (§ 11).
  R-DOT-3  per_tick_value      value="damage_per_second * 0.1"  unit=hp_per_tick
                               provenance={rva:0x0020d7b5}
  R-DOT-4  same_source_merge   value="MAX per tick-bucket"     scope=same(source_key)
                               provenance={rva:0x0020d828, insn:"maxss"}
           ⚑ NOT refresh, NOT replace, NOT max(remaining,new).
  R-DOT-5  cross_source_merge  value="ADD at weight damageMagnitude[min(i,N-1)]/100"
                               scope=distinct(source_key)   provenance={rva:0x0020d8ab-0x0020d8e6}
  R-DOT-6  damage_magnitude    value=[100.0]   unit=percent_per_ordinal  scope=shipped_v1.2.3.4 + ed-III
                               provenance={record:"records/game/gameengine.dbr",
                                           tpl_description:"Decreasing same type duration damage",
                                           override_scan:{archives:13, records:172255, hits:6, all:[100.0]}}
           ⚑ THE finding: a first-class per-ordinal attenuation hook, shipped NEUTRAL.
  R-DOT-7  cross_attacker      value="NO MERGE — separate timelines, separate ApplyDamage"
                               provenance={rva:0x00208ad6, 0x000d70e0}
           ⚑ Resistance applies per attacker-timeline, never to a merged total.
  R-DOT-8  caps                value=NONE      scope=sources|duration|magnitude
                               provenance={negative_search: six functions, immediate-compare table § 5}
  R-DOT-9  duration_extension  value="remaining := max(old_remaining, new_duration)"  (never truncated)
  R-DOT-10 fixed_damage_lane   value="separate simpler path: flat maxss on +0x04,
                                      no source key, no sort, no multiplier"
                               scope=CombatAttributeDurFixedDamage  provenance={F14}
           ⚑ This is the lane B6 lives in. R-DOT-10 is the B5↔B6 join.
```

### 6.2 Residuals to carry (the README declares them; the lift must not drop them)

- `DurationDamageSource` dword **semantics** are not named. Structure and keying rule are exact; the
  English gloss ("same caster? same skill? same affix?") is **not established**. A lift row that
  glosses this is fabricating.
- **Display-layer channel:** instance `+0x08` is **MAX**-aggregated into a manager-level per-second
  statistic feeding UI. A figure read off any surface fed by that channel **is not the tick damage**.
- `damageMagnitude` neutrality holds *"as shipped, including all first-party expansions"* —
  **not** "always". Third-party mods are out of the decode's reach by construction.
- The sort comparator was read from the insertion-sort path only; the partition path was not proved
  to agree on tie handling. Numerically irrelevant at `N=1` — which is *why* it is flagged.

**Scope tag for every B5 row: `scope="grim_dawn_shipped_v1.2.3.4+edIII"`.** These are engine laws,
not KC2 measurements, and mis-scoping them as KC2-specific would make them look re-derivable when
they are not.

---

## § 7 — B6 · `ABS-CONTROL-APPLICATION` — ⚑ the concurrency law, and the one row that is missing

**Registry `what`:** *"control-family application parameters and the concurrency law."*
Registry `why`, verbatim: *"⚑ The concurrency law is the highest-value unlifted row for a Godot
implementer: overlapping controls BURN EACH OTHER'S wall-clock (S-8). An engine that queues or
refreshes CC by default ships a fight roughly a third more punishing than the real one."*

### 7.1 Schema

`d7_control_application_parameters.csv` — 43 rows, 7 columns. Grain: **one decoded assertion per row.**

| column | domain | semantics |
|---|---|---|
| `id` | `D7-{E,1,2,3,N}-NN` | ⚑ **a compound ID that encodes the row's class** — `E`=enum, `1/2/3`=the three commissions (`MD-B2-1/2/3`), `N`=clean negative. Discipline #14: *mechanical labels stay internal; per-instance vocabulary stays explicit.* The class must become a **column** in the lift, not stay packed in the key. |
| `kind` | `enum` (15) / `rule` (25) / `negative` (3) | already carries most of what the ID packs — use this, and add `commission`. |
| `key` | string | the assertion's name (`control_resistance_semantics`, `same_type_stacking`, …). |
| `value` | free text | ⚑ **holds prose rules, not scalars** — `"DURATION SCALAR"`, `"LONGEST WINS (max), never additive"`. Not machine-readable, and should not pretend to be. |
| `rva` | hex, sometimes multi | provenance. Blank on `D7-E-14` and `D7-N-02` (both honestly — one has no controller path, one is a census result). |
| `fn` | string | the function or census that establishes it. |
| `note` | free text | the qualifying detail. **Frequently load-bearing** — `D7-1-01`'s note carries the actual formula. |

The 15 `enum` rows are a clean `CombatAttributeType` value map (Stun 42 … CrowdControlCap 65) and
lift directly. The 25 `rule` rows are the substance. The 3 `negative` rows are clean negatives with
their search recorded — GL-12 shaped, keep them.

### 7.2 ⚑ A-B6-1 — the concurrency law is DERIVABLE but is NOT A ROW

This is the finding of the pass for B6, and it matters because the registry singles this law out as
the highest-value item for the Godot team.

**What is present** — four rows which, composed, *entail* the burn law:

| row | key | what it establishes |
|---|---|---|
| `D7-2-02` | `exactly_one_involuntary_effect` | **first-match-wins ladder** `0x2f Immobilize > 0x2e Petrify > 0x2d Freeze > 0x2c Trap > 0x2b Sleep > 0x2a Stun > 0x30 Knockdown > 0x31 TakeHit`; on change `Stop(old)` then `Start(new)`. |
| `D7-2-09` | `control_state_exit` | the state has **no self-timer** — `DefaultBeginStunAction` passes a **zeroed** `ControllerAIStateData`, so *"the timer is the `DurationDamageManager` bucket list, not the state."* |
| `D7-2-08` | `control_state_does_not_refresh` | every `Begin<Control>` slot **inside** a control state is a bare-`ret` stub. A second landing of the same family does not restart the state. |
| `D7-1-11` | `same_type_stacking` | **LONGEST WINS (max), never additive** — insert grows the bucket list only if longer; `GetFixedDamageDuration` takes the max. |

**What is absent:** any row that states the *composed* consequence. Compose them:

> Every landed control family gets its **own independent 100 ms bucket timeline** in
> `DurationDamageManager`. **All live timelines retire buckets in real time, simultaneously,
> whether or not their family is the one currently displayed.** Only **one** involuntary effect is
> *active* (the § 3.2 ladder). Therefore a control that lands while another is active **is already
> burning down** — its clock does not start when it becomes the winner, and does not pause when it
> loses the ladder. **Overlapping controls consume each other's wall-clock.**

Worked: Freeze 2.0 s lands at t=0; Stun 2.0 s lands at t=1.0. Freeze wins the ladder (0x2d > 0x2a) and
holds to t=2.0. At t=2.0 the Freeze timeline is exhausted; Stun's timeline — **which has been
retiring buckets since t=1.0** — has 1.0 s left. Total lockout **3.0 s.**
A queue model gives **4.0 s**. A refresh model gives **3.0 s** *for the wrong reason* and diverges
the moment the families differ or the second control is shorter. The registry's *"roughly a third
more punishing"* is precisely this 4.0-vs-3.0 shape.

**⚑ Schema shapes that would INVITE the wrong reading — flagged per commission:**

1. Any column named `queue_position`, `pending_controls`, `next_control`, `stack_depth`.
   There is no queue. There is no stack. There are **N concurrent independent countdowns** and a
   **selector**.
2. Any single `control_state` field carrying a *duration*. The duration does not belong to the
   state; it belongs to the **timeline**. Binding them invites "the stun state has 2 s left", which
   is false the moment a second family is live. `D7-2-09` says this in the binary's own words.
3. `refresh_on_reapply: false` as the *only* stacking row. It is true and it is **insufficient** —
   it describes same-family behaviour (`D7-1-11`) and says nothing cross-family, which is where the
   third goes missing.
4. Modelling the ladder as **priority-with-preemption-and-resume**. There is no resume. Nothing is
   suspended; the loser was never paused.

**The safe shape is two rowsets with two different grains**, which makes the wrong reading
unstateable:

```
ROWSET  control_timeline            grain: (control_family)          ⚑ the CLOCKS — N concurrent
  family, enum_value, bucket_ms=100, quantisation="(int)(s*10)*100",
  same_family_merge="LONGEST_WINS_MAX",  cross_family_merge="NONE — independent timelines",
  concurrency="ALL LIVE TIMELINES RETIRE IN REAL TIME, INDEPENDENT OF LADDER STATE",
  provenance{rva, fn}

ROWSET  control_selector            grain: (ladder_ordinal)          ⚑ the DISPLAY — exactly 1
  ladder_ordinal 1..8, family, enum_value,
  selection_rule="FIRST GetFixedDamage(t)>0 in ladder order",
  on_change="Stop(old); Start(new)",  resume_semantics="NONE — losers are not paused",
  provenance{rva:0x00209fc0}

ROWSET  control_law                 grain: (law_id)                  ⚑ A-B6-1 — MUST BE MINTED
  L-CC-CONCURRENCY  value="Overlapping controls BURN each other's wall-clock. Two 2.0 s controls
                          landing 1.0 s apart lock the player for 3.0 s, not 4.0 s."
                    scope="all involuntary families (42-49)"
                    provenance={derived_from:[D7-2-02, D7-2-08, D7-2-09, D7-1-11],
                                rva:[0x00209fc0, 0x0011f609, 0x0020e0ae, 0x002089f2],
                                anti_pattern:"queue|refresh|preempt-and-resume — ALL WRONG"}
```

`L-CC-CONCURRENCY` carries `derived_from` rather than a single RVA because it is honestly a
**composition**, not a single decoded site. That is DR-1 satisfied without overclaiming: the
provenance names the four rows and the four sites the composition rests on. **A derived law with
declared inputs is provenanced; a derived law presented as a primary decode is not.**

### 7.3 Other B6 rows the lift must not lose

- **`D7-1-01` — control resistance is a DURATION SCALAR:** `attr.value *= (1 - r/100)`, then
  `max(·,0)`. ⚑ **"NOT a chance gate, NOT a threshold."** The two most common wrong models, named in
  the row itself.
- **`D7-1-10` — quantisation TRUNCATES:** a 1.25 s stun becomes 12 buckets = **1.200 s**. Same
  truncation as `R-DOT-2`; the two should be lifted as one shared law with two scopes.
- **`D7-1-13` — application guard:** `AddFixedDamage` early-returns unless `magnitude>0 AND
  duration>0`, so *a 100 %-resisted control never enters the timeline at all.* Not "applies for 0 s"
  — **never applies.** Observable difference for on-control-applied triggers.
- **`D7-2-04/05/06` — Confusion, Fear and Taunt are NO-OPS on the player.** The row's own words:
  *"a decoded zero, not a defaulted one."* This distinction must survive; a NULL here would read as
  not-modelled under GL-12 and lose a real finding.
- **`D7-1-12` — the PvP duration multiplier is a NO-OP in PvE.** A trap not sprung. Carry it as a
  scoped row (`scope="pvp_only"`) so nobody re-derives it.
- **`D7-E-06` / `D7-E-08` + `D7-N-02`** — enum 47 (Immobilize) and 49 (TakeHit) have **no
  `DefenseAttribute` class**, so they are **unresistible by any per-type stat**. An absence in the
  *game*, decoded — the most valuable kind, and one a schema with a mandatory `resist_stat` column
  would quietly fabricate.

---

## § 8 — B7 · `ABS-SUMMON-BODIES` — **PASS-with-caveat**

**Registry `what`:** *"the two player summons as first-class actor templates."*
Registry `why`: *"⚑ Layer-2 note that must not be mistaken for a Layer-1 one: summoned bodies carry
NO PATH in the recording (R-L53-2) — that is an absence in the REFERENCE, not in the model."*

### 8.1 Schema

`d9_summon_bodies.csv` — 216 rows, 7 columns. Grain: **(summon, group, field)** — long/tidy again.

| column | domain | semantics |
|---|---|---|
| `summon` | `Deathstalker` (131) / `Guardian of Empyrion` (85) | the actor. |
| `group` | `attack_slot` 86 · `resist` 34 · `body` 26 · `bio` 26 · `passive` 16 · `chain` 12 · `swing` 12 · `UNDERIVABLE` 4 | the facet. |
| `field` | string | dotted for attack slots (`basic.offensivePhysicalMin`, `special3.rank_used`) — ⚑ **a two-level key packed into one string**; must split to `slot` + `field` on lift. |
| `value` | poly-typed | includes multi-sentence prose (`invincible_SEMANTICS` is a 400-char decode). |
| `grade` | `MEASURED` 190 · `DECODED` 14 · `INFERRED-WITH-EVIDENCE` 8 · `UNDERIVABLE-WITH-PATH-NAMED` 4 | ⚑ **a four-level provenance grade, per row.** Excellent — this is the DR-1 pattern. |
| `source_record_or_rva` | record path or RVA | provenance locus. |
| `extraction_method` | free text | how. Often carries the qualifier that makes the grade honest. |

Row-count asymmetry (131 vs 85) is **not** a defect: it is `attack_slot` 66 vs 20 — Deathstalker has
`basic` + `special1..4` + `buff_self`; Guardian has `basic` + `buff_self`. The asymmetry is a fact
about the bodies. Body/bio/resist/passive/swing/chain groups are **symmetric at 13/13/17/8/6/6**.

Only 2 genuinely blank values: Guardian's `controllerAggressive` / `controllerDefensive`, both
`grade=MEASURED`, `method="field read"` — i.e. **the field was read and it was empty**, which is a
measured absence rather than a missing measurement. Correct, but indistinguishable from a null on
lift unless the grade travels. **Grade must travel with every value.**

### 8.2 ⚑ A-B7-1 — the word `PATH` is overloaded across the two surfaces (curation hazard, not a data defect)

The commission requires the Layer-2 caveat survive. It is at risk from a **collision of vocabulary**,
and this is exactly the kind of thing that gets silently merged in a lift:

| sense | where | means |
|---|---|---|
| **decode-path** | B7 `grade = UNDERIVABLE-WITH-PATH-NAMED` (4 rows) and its `extraction_method` — *"PATH TO CLOSE: decode `JoinMe@Monster` (0x002d5200)…"* | **the route to closing an open decode.** A property of *our investigation*. |
| **locomotion path** | R-L53-2 — *"summons carry no recorded path"*; star-lord's *"344 actors, 344 paths, zero fabricated"* | **the recorded trajectory** in the SIM-KNOTS artifact. A property of *the reference recording*. |

They are unrelated, and the first appears **four times inside the pinned file** while the second
appears **nowhere in it**. A lift that maps `UNDERIVABLE-WITH-PATH-NAMED` onto "no path" would
conflate a Layer-1 decode residual with a Layer-2 reference absence — **the precise error the
registry row exists to prevent.**

**Mitigation, and I would insist on it:** never emit a bare `path` key in the summon rowset. Use
`decode_path_to_close` and `recorded_locomotion_path`. Two names, no collision, no reader judgement
required.

### 8.3 Named absences (all four self-declared by the file — correctly)

- **`pet_charLevel_binding`** ×2 — `SpawnPet@Skill_SpawnPet` (0x0041c850) contains **no `SetLevel`
  call**; the pet is `Load()`ed then `JoinMe@Monster` binds it to the caster. Path to close named.
  ⚑ Consequence: **the summons' level is not established**, so every `*_base_at_charLevel_100` row
  (grade `INFERRED-WITH-EVIDENCE`) rests on an *inferred* binding. Those 8 rows must not be lifted
  as MEASURED.
- **`difficulty_pak_cell_index`** ×2 — the pak is decoded; the 12-cell index for Crucible-Ultimate-solo
  was not re-derived on that lap. Path to close named (Lap E publishes cell 8 = 15.0).

### 8.4 Proposed baton-v3 lift shape

```
ROWSET  summon_actor                grain: (summon_id)
  summon_id, display_name, spawn_skill_record (K4), body_record, faction="player_summon",
  provenance{archives, extraction_method}
          ⚑ faction per the W4 runtime spec: same actor-template schema as monsters.

ROWSET  summon_stat                 grain: (summon_id, group, field)
  group, field, value, unit, scope, grade,
  provenance{source_record_or_rva, extraction_method}
          ⚑ grade is NOT optional. INFERRED-WITH-EVIDENCE ≠ MEASURED, and the 8 bio rows depend on it.

ROWSET  summon_attack_slot          grain: (summon_id, slot, field)     ⚑ splits `basic.foo`
  slot ∈ {basic, special1..4, buff_self}, field, value, unit, scope, grade, provenance

ROWSET  summon_absence              grain: (summon_id, absent_id)
  ABS-SUMMON-CHARLEVEL-BINDING   layer=1  decode_path_to_close="JoinMe@Monster 0x002d5200 | save/GDC read"
  ABS-SUMMON-DIFFICULTY-PAK-CELL layer=1  decode_path_to_close="re-derive index selection in GameEngine"
  ABS-SUMMON-RECORDED-PATH       layer=2  ⚑ recorded_locomotion_path — R-L53-2
                                 note="ABSENT IN THE REFERENCE, NOT IN THE MODEL. The recording
                                       carries 344 actor paths and the summons are not among them.
                                       A runtime MUST move these bodies; it simply has no measured
                                       trajectory to be graded against."
```

The `layer` column is what makes the caveat survive contact with a consumer. Layer-1 absences are
**decode debts we owe**; the Layer-2 absence is **a limit of the instrument**. Same table, different
column value, no ambiguity — and a grader that tries to score summon locomotion against the
reference will hit a row that tells it not to.

---

## § 9 — B8 · `ABS-DEVOTION-PROCS` — the thinnest, and a count that does not reconcile

**Registry `what`:** *"the 8 devotion procs with host bindings, triggers, chances and ICDs."*
Registry `why`: *"v1 carried only a prose disclosure; v2 owes rows."*

### 9.1 Schema

`d6_player_kit_residual.csv` — 27 rows, 10 columns. Grain: **(target, field)**.

| column | domain | semantics |
|---|---|---|
| `target` | `fighting_spirit` (8) / `ulzaads_decree` (11) / `resilience` (8) | the skill. ⚑ **Only ONE of the three is a devotion.** |
| `record` | K4 skill record path | `playerclass01/` (Soldier), `devotion/`, `playerclass09/` (Oathkeeper). |
| `level_kind` / `level` / `index` | `rank`\|`devotion_level` / int / int | the rank basis and its 0-based array index. Two conventions in one column pair — must carry `level_kind` forward. |
| `field` | string | ⚑ **mixes DBR field names** (`skillCooldownTime`) **with minted SEMANTIC keys** (`TRIGGER_DIRECTION`, `REFIRE_GATE`, `ROLL_RULE`, `PAYLOAD_HOME`). Uppercase = minted. The convention is undeclared but consistent; it must become an explicit `field_class` column. |
| `value` | poly-typed | scalars **and predicates** (`"fire iff uniform_int(0,100) <= onHitActivationChance"`). |
| `unit` | `percent`/`seconds`/`flat_OA`/`flat_armor`/`flat_damage`/`enum`/`predicate`/`bool`/`note` | ⚑ **well-populated, non-empty on every row** — best unit discipline of the seven files. |
| `status` | `DECODED` (25) / `DECODED-BUT-INERT` (1) / `DECODED-AUTHORED-OVERRIDE` (1) | per-row grade. |
| `provenance` | free text | arz overlay coordinates or RVA chain. DR-1 satisfied on all 27. |

Two rows deserve to survive verbatim into the lift:

- **`DECODED-BUT-INERT`** — Fighting Spirit's `skillCooldownTime = 5.0` **is on the record and is
  never read**: `EndCooldown` is a COMDAT-folded `ret`-stub at `0x158b0`, and the real re-fire gate
  is `activeDurationRemaining_ms > 0`. ⚑ **An implementer who reads the DBR gets a 5 s cooldown that
  does not exist.** This is the highest-value row in the file.
- **`DECODED-AUTHORED-OVERRIDE`** — Resilience's `thresholdDuration = False` **explicitly overrides**
  the template default of `1`; 65 corpus records set it explicitly. Value and the fact-of-override
  are two different facts and both are load-bearing.

### 9.2 Named absences

**A-B8-1 · ⚑ The pin does not contain the devotion procs.** Against the registry's four required
facets, on the pinned file alone:

| required facet | present in pin? |
|---|---|
| **host bindings** | **0 rows.** No host→devotion binding appears anywhere in the file. |
| **triggers** | **1 row**, and it is for `fighting_spirit` — **not a devotion** (`TRIGGER_DIRECTION = HitByEnemy`). |
| **chances** | **1 row**, again `fighting_spirit` (`onHitActivationChance = 30.0`). |
| **ICDs** | **0 rows.** `skillCooldownTime` appears on all three targets, but that is a *skill* cooldown, not an internal cooldown, and one of the three is decoded INERT. |
| **coverage** | **1 devotion of 7–8** (`ulzaads_decree`, `tier2_37d_skill.dbr`, 11 payload rows). |

The pin is a genuinely good table — of **player-kit residuals**, which is what its filename says. It
is simply **not the devotion-proc table**, and the registry row points at it as though it were.

*Recovery surfaces, both located, neither pinned:*

1. **`data/kc2/pm4g_played_kit.csv`** (324 rows, 25 cols; 285 `mastery=devotion`) carries the
   binding surface in `autocast_devotion_skill` + `autocast_controller`. **Exactly 7 rows populate
   them**, and the trigger + chance are encoded in the controller record's own path:

   | host skill | devotion skill | autocast controller | trigger | chance |
   |---|---|---|---|---|
   | Vire's Might | `devotion/tier2_05f_skill.dbr` | `cast_@selfonattack_20%.dbr` | self on attack | 20 % |
   | War Cry | `devotion/tier2_37d_skill.dbr` ⟵ **the one in the pin** | `cast_@selfonattack_20%.dbr` | self on attack | 20 % |
   | Eye of Reckoning | `devotion/tier1_08e_skill.dbr` | `cast_@enemyonattackcrit_100%.dbr` | enemy on attack **crit** | 100 % |
   | Summon Guardian of Empyrion | `devotion/tier3_20e_skill.dbr` | `cast_@enemyonattack_20%.dbr` | enemy on attack | 20 % |
   | Field Command | `devotion/tier1_29e_skill.dbr` | `cast_@selfat50%health_100%.dbr` | self at 50 % health | 100 % |
   | Divine Mandate | `devotion/tier2_17c_skill.dbr` | `cast_@selfonanyhit_30%.dbr` | self on any hit | 30 % |
   | Presence of Virtue | `devotion/tier2_02f_skill.dbr` | `cast_@enemyonanyhit_33%.dbr` | enemy on any hit | 33 % |

   ⚑ **Trigger and chance are packed into the controller record's FILENAME.** That is a compound
   ID carrying semantics — Discipline #14's exact anti-pattern. The lift must **decompose** it into
   `trigger_direction` (self|enemy) + `trigger_event` (attack|attack_crit|any_hit|at_50pct_health) +
   `trigger_chance_pct`, and keep `autocast_controller` as provenance. It must **not** ship the
   filename as the trigger.

2. **`src/reincarnated/export/goldens/devotion_envelope_disclosure.value.txt`** (the v1 prose
   disclosure the registry says v2 owes rows for) supplies the envelope classes and the **ICD
   policy**, verbatim: *"NO invented internal cooldowns. `skillCooldownTime` absent on Assassin's
   Mark and Maul ⇒ modelled absent (L-3a). The corpus contains no internal-cooldown field on any of
   its 176 autocast controllers."*
   ⚑ **ICDs are a decoded ABSENCE, not missing data.** The lift must ship `icd = NULL` with
   `scope="decoded_absent"` and that provenance string, or a Godot implementer will invent ICDs to
   fill an apparently-empty column — which the disclosure forbids by name.

**A-B8-2 · ⚑ The count does not reconcile: registry says 8, two surfaces say 7.**

| surface | count |
|---|---|
| absence registry `ABS-DEVOTION-PROCS.what` | **8** |
| `devotion_envelope_disclosure.value.txt` line 2 | **7** — *"powers: 7, all at DB-max rank, save-measured, XP byte-exact, bindings DB↔save 7/7"* |
| `pm4g_played_kit.csv` rows with an autocast binding | **7** |
| named powers in the disclosure (assassins_mark, ulzaads_decree, tip_the_scales, arcane_barrier, turtle_shell, maul, shifting_sands) | **7** |

Three independent surfaces say 7; only the registry prose says 8. I am **not** adjudicating this —
it is a conductor call — but it must be adjudicated **before** the Wave-3 cut, because the pack's
own PRE==POST census gate turns on it. **If star-lord emits 8 rows he fabricates one; if he emits 7
the registry row is wrong.** A census that passes against a wrong expected count is worse than one
that fails.

I note without asserting: the disclosure's seven power *names* and the played-kit's seven *host
bindings* have not been proved to be the same seven — the disclosure names powers, the kit names
hosts, and the only pair I verified end-to-end is `ulzaads_decree ↔ tier2_37d_skill ↔ War Cry`
(via the pinned file). Reconciling the two seven-lists is a cheap, necessary step and it may itself
be where the 8th went.

**A-B8-3 · The B7↔B8 edge is in neither pin** (§ 2.4). `Summon Guardian of Empyrion` is
**proc-driven** — `cast_@enemyonattack_20%`. A lift that ships B7 as a player-commanded summon and
B8 as a damage proc loses the causal edge between them, and with it the Guardian's actual uptime
model.

### 9.3 Proposed baton-v3 lift shape

```
ROWSET  devotion_proc               grain: (proc_id)
  proc_id, display_name, devotion_skill_record (K4), devotion_level, rank_effective,
  host_skill_record (K4), host_display_name,          ⚑ the binding
  autocast_controller_record,                          ⚑ provenance ONLY, never the trigger
  trigger_direction   ∈ {self, enemy}                  ⚑ decomposed from the controller filename
  trigger_event       ∈ {attack, attack_crit, any_hit, at_50pct_health}
  value(trigger_chance_pct), unit="percent",
  scope="crucible_s09_cp150_played_kit",
  provenance{source_file:"data/kc2/pm4g_played_kit.csv", sha256:..., grade:"MEASURED"}

ROWSET  devotion_proc_payload       grain: (proc_id, field)
  field, field_class ∈ {dbr_field, minted_semantic},   ⚑ replaces the uppercase-means-minted convention
  value, unit, scope, status,                          ⚑ status carries DECODED-BUT-INERT
  provenance{arz_overlay | rva_chain}
                                                       ⚑ populated for ulzaads_decree (11 rows) from
                                                          the pin; DECLARED-ABSENT for the other six.

ROWSET  devotion_proc_icd           grain: (proc_id)
  value=NULL, unit="seconds", scope="decoded_absent",
  provenance{"NO invented internal cooldowns (L-3a); corpus contains no internal-cooldown field on
              any of its 176 autocast controllers",
              source:"export/goldens/devotion_envelope_disclosure.value.txt"}
                                                       ⚑ NULL-with-reason, never an empty cell.

ROWSET  devotion_proc_envelope      grain: (proc_id, envelope_class)
  envelope_class ∈ {saturating, duty_cycle_bounded, rate_ceilinged, dual_bound},
  value(bound), unit, scope, provenance, open_semantics_ref   ⚑ OS-1, OS-3 travel as rows
```

`autocast_controller_record` sits in the row as **provenance**, with the trigger decomposed into
three explicit columns beside it. That is Discipline #14 applied: the mechanical label
(`cast_@enemyonattackcrit_100%.dbr`) stays internal as a source pointer; the per-instance vocabulary
(`enemy` / `attack_crit` / `100`) is explicit and queryable.

---

## § 10 — CROSS-CUTTING OBSERVATIONS

**10.1 · Grade columns are the pack's real currency, and they are inconsistent.** Five of seven
files carry a per-row provenance grade, under **five different column names and five different
vocabularies**: B3 `life_grade` {MEASURED, ABSENT:…}; B4 `igb_field_state`+`igb_provenance`
{PRESENT/ABSENT}×{DB-CITED/TPL-DEFAULT}; B7 `grade` {MEASURED, DECODED, INFERRED-WITH-EVIDENCE,
UNDERIVABLE-WITH-PATH-NAMED}; B8 `status` {DECODED, DECODED-BUT-INERT, DECODED-AUTHORED-OVERRIDE};
B6 `kind` {enum, rule, negative}. B2 carries none.

Under DR-3 the grade belongs inside the **provenance** leg of every triple, under **one** name and
**one** controlled vocabulary. My recommendation, as the union of what is actually in use:

```
grade ∈ { MEASURED, DECODED, DERIVED, INFERRED-WITH-EVIDENCE,
          DECODED-INERT, DECODED-ABSENT, UNDERIVABLE-WITH-PATH-NAMED }
```

`DECODED-ABSENT` is the one I would fight for: it is the difference between "we found nothing" and
"we established there is nothing", and **three separate findings in this pass depend on it**
(B8's ICDs, B6's missing `defensiveImmobilize`/`defensiveTakeHit`, B5's cap fields). GL-12 says
absence is declared; this vocabulary is how a *declared* absence stays distinguishable from an
undeclared one after the lift flattens everything into rows.

**10.2 · Three compound IDs pack semantics into keys** — B6's `D7-{class}-{n}`, B7's
`{slot}.{field}`, B8's controller filename `cast_@{direction}on{event}_{chance}%`. All three
decompose cleanly and all three are proposed decomposed above. Discipline #14 (doc 37 § 9.2b):
mechanical labels stay internal, per-instance vocabulary stays explicit.

**10.3 · Two truncation laws, one shape.** `R-DOT-2` (`trunc(duration_s × 10)`) and `D7-1-10`
(`(int)(s × 10) × 100 ms`) are **the same engine behaviour in two lanes**. They should lift as one
law with two scopes, not as two laws — and either way the word **TRUNCATES** must be in the row.
A 1.25 s stun is 1.200 s; a 3.35 s DoT is 3.3 s. Rounding is the default assumption and it is wrong.

**10.4 · Six of seven files are already rows-not-fields.** B2, B6, B7, B8 are long/tidy
`(entity, field, value)`; B3 is `(record, wave)` with a small measure block; B5 is prose. Only
**B4** carries a genuine fields-not-rows encoding (the pipe-joined roster columns). DR-2 compliance
across this substrate is therefore mostly **preservation**, not transformation — which is a good
position to lift from, and worth saying because the temptation in a Wave-3 assembly is to pivot the
tidy tables wide for convenience.

**10.5 · Reversibility holds.** Every proposed shape preserves the source value and adds provenance
beside it; no proposed transformation is lossy. The one place I would put a guard rail is B3's
`G_pct` (§ 4.4) — folding it into provenance rather than dropping it is what keeps base life
recoverable.

---

## § 11 — SELF-CRITIQUE

- **I did not verify the K1→K2 bridges against `Game.dll` or the archives.** § 2.1's coverage
  numbers are joins over two unpinned CSVs whose own construction I took on trust. If either bridge
  is roster-scoped in a way I did not detect, the "158 records with no controller" figure is an
  artefact of *my instrument*, not of the substrate. The direction of the finding is robust (B2 is
  77 controllers and the pool needs more); **the exact number is not, and should not be quoted
  as measured without re-derivation.**
- **The 7-vs-8 devotion count I raise but do not close.** I checked three surfaces and all say 7.
  I did not check the save file, the XP-byte evidence, or the v1 baton's own rows — any of which
  might name an eighth. I am reporting a **discrepancy**, not a correction.
- **I did not read all 4,081 B2 rows or all 15,801 B3 rows.** Structure, cardinality, blank-audits
  and joins are computed over the full files; **semantic** review is over the decode notes plus
  sampled rows. A per-row semantic defect in the interior of either table would not have been caught.
- **The § 7.2 worked example (3.0 s vs 4.0 s) is my composition, not a measured quantity.** It
  follows from four decoded rows and I believe it is right — but it has not been observed in footage
  or asserted by any prior lap in that arithmetic form. It is offered as an **illustration of the
  law's shape**, and gamora should treat it as a hypothesis to check against the sim, not a datum.
  The registry's *"roughly a third more punishing"* is consistent with it, which is corroboration and
  not proof.
- **B4's `pool_weight` semantics I inferred from column position and name**, not from the proxy DBR
  template. If it turns out to be a *within*-pool weight after all, A-B4-1 shrinks considerably.
  I looked for per-slot columns across all 46 CSVs and found none, which is what makes me confident
  the *member* weights are genuinely absent — but the reading of what `pool_weight` *is* rests on
  the name.
- **I have proposed shapes, not schemas.** They are recommendations to gamora (Wave-2) and star-lord
  (Wave-3), authoritative within my data domain per my seat, and **reversible** — if a lift finds a
  better grain, the finding beats my proposal. What is **not** negotiable is the set of named
  absences: those are facts about the substrate and they must land as rows either way.

---

## § 12 — WHAT WAVE-2 AND WAVE-3 SHOULD DO WITH THIS

**gamora (Wave-2):** B5 and B6 are buildable **today** — B5 from § 6.1's ten rules, B6 from § 7.2's
two-rowset split plus the § 7.3 rows. ⚑ Build the control model as **N concurrent countdowns + one
selector**, never as a queue and never as priority-with-resume. B7 is buildable with grades carried
(the 8 `INFERRED-WITH-EVIDENCE` bio rows are not measurements). B8's payload is buildable for
`ulzaads_decree` only; the other six procs need the § 9.2 recovery surfaces first.

**star-lord (Wave-3):** ten absence rows are minted by this pass and each should land in
`provenance.absence_registry` rather than being resolved silently —
**A-B2-1** (43-state key space), **A-B2-2** (15 of 68 fields), **A-B2-3** (64+158 of 466 tier-16
records unparameterised), **A-B3-1** (4 of 5 stat dimensions), **A-B3-2** (wave 150),
**A-B3-3** (band unstated), **A-B4-1** (⚑ per-member pool weights — first-order),
**A-B4-2** (roll order + RNG), **A-B6-1** (⚑ the concurrency law as a row), **A-B8-1** (7 of 8 procs).
**A-B8-2** (the 7-vs-8 count) is **not** an absence — it is an adjudication the conductor owes
before the census gate can be trusted.

**conductor:** two items want a ruling before Wave-3 seals — the **7-vs-8 devotion count** (§ 9.2),
and whether **A-B4-1** justifies a legolas re-extraction lap inside this run or ships as a declared
absence. My read: the count must be settled (it gates a census); the pool weights can honestly ship
declared-absent **if** the `pool_member` rows carry explicit NULL weights per § 5.3, so the hole is
countable rather than inferable.

---

*Curation pass closed 2026-08-25 by elrond. Seven pins verified 7/7; no HALT. Two PASS
(B5, B7-with-caveat), five THIN-with-named-absences (B2, B3, B4, B6, B8). Ten absence rows minted,
one count discrepancy escalated. READ-ONLY on all engine substrate — nothing under
`reincarnated-engine/data/` was modified by this pass.*
