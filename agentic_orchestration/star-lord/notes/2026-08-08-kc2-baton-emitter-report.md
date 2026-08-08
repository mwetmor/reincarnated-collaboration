# KC2-SIM Phase C — baton/v1 emitter build report

**Author:** star-lord (export seam)
**Date:** 2026-08-08
**Commission:** gandalf (RUN-CONDUCTOR), KC2-SIM autonomous run, Phase C — baton-emitter build
**Spec:** `gandalf/notes/2026-08-08-kc2-sim-battle-spec.md` § 11 (MERGED, consumer-signed) · § 12 · § 9.5
**Coverage bar (AC-11.3):** `drax/notes/2026-08-08-kc2-baton-coverage-sign.md` — 23 MUST + 5 SHOULD
**Work surface:** `~/Games/reincarnated-engine/` main, from HEAD `ebf13240`
**Engine commit:** `68e2e372` · tag `star-lord/v1.87-kc2-baton-v1-emitter-1`

---

## 0 — Bottom line

**Built, tested, committed.** 35 tests green. 27 validator checks green. The consumer stub
reconstructs **23/23 MUST and 5/5 SHOULD from the baton alone** — including re-running § 2.1's
disc predicate off the emitted telegraph (329 player damage rows re-tested, **0 outside the
disc**).

**One conflict is load-bearing and needs a ruling: CD-1.** § 11.2 [S7] adopts
`arena_scenario_emitter`'s `json.dumps(..., indent=2)` verbatim, but that emitter serialises
nested *dicts* while the baton serialises a *row-array* — under `indent=2` every one of a row's
24 cells gets its own line. **Measured 1.95×**, putting the MID scenario at **33.2 MB against
drax's declared ≈ 22 MB budget**. I shipped `rows-compact` as the default (one event per line
under its declared header, **+2.6 %** over fully-compact) and kept the literal form reachable as
`json_style="indent"`. It is serialisation, never schema — all styles `json.loads` to the
identical object — so I judged it inside my seam, but it contradicts a spec sentence and is
therefore CONDUCTOR-DECISION-NEEDED. **One argument reverses it.**

Nothing here is calibrated. Every number in the fixture is plausible-shaped, not measured;
the emitter is wired to a **synthetic** run-record because gamora's Phase-C mechanisms are not
in the tree yet (§ 4 lists all 13 integration points).

---

## 1 — Implementation map (§ 11 subsection → file)

| § 11 subsection | Where it lives |
|---|---|
| 11.1 what the baton is · L-1 namespace guard | `export/baton_v1_schema.py` docstring · `_ac_11_5` (absence test) · `tests/…::test_ac_11_5_reserved_marker_byte_unchanged_after_emit` |
| 11.2 conventions extended (format version, root provenance keys, deterministic + atomic write, run identity, config hash, engine-version sourcing, event-record shape) | `export/baton_v1_emitter.py` — `engine_version_sha/​_full`, `engine_tree_state`, `resolve_spec_pin`, `compute_config_hash`, `_serialize`, `write_baton` |
| 11.2 three declared divergences | MIGRATION entry § "Three declared divergences" |
| 11.3 truth boundary · 11.3.1 L-27 `hp_after` | `Event.hp_after` (mandatory on 3 members) · `_ac_11_7e` chained reconciliation · stub `M-23` |
| 11.4 field inventory (logical) | `export/baton_v1_schema.py` — full Pydantic family, 24-column `Event`, four columnar tracks |
| 11.4 twelve pins | `EVENT_COLUMNS` / `EVENT_TYPES` (pins 1, 6, 7) · `_ac_11_7b` (pin 2) · `run_tick` identity + `t_s` derivation in `build_baton` (pins 3, 4) · flat scalars (pin 5) · `hit_test_model` (pin 9) · `scatter_model` + `spawn_x/y` (pin 10) · `arena_id` + `ArenaPin` (pin 11) · `fixture_p06_state` / `run_p06_enabled` (pin 12) |
| 11.5 provenance block, typed + ID-registered | `Provenance`, `DECLARATIONS` (12), `OUT_OF_MODEL` (9), `DEVOTION_ENVELOPE_DISCLOSURE`, `HaltRegister`, `ArenaPin`, `SeedPins` |
| 11.5 write-boundary assert [R-38] | `_ac_11_4g` |
| 11.6.1 size | `export/math/2026-08-08-baton-v1-schema.md` §§ 1–3 (re-measured; see CD-1) |
| 11.6.2 wire form + write discipline | `to_wire` / `from_wire` / `_serialize` / `write_baton` (atomic `.tmp` → `os.replace`) |
| 11.6.4 O-1 gzip | `write_baton(gzip_output=False)` — flag present, **default OFF**, routed to drax |
| 11.6.4 O-2 monster attack model | `ConfigModel.monster_attack_model` default `"abstract-schedule"` (L-28) |
| 11.6.4 O-3 ADR-006 | **no external write**; enforced by AST guard in the test suite |
| 11.6.4 O-4 axis convention | resolved from the sim's own contract — see § 4 IP-6 |
| 11.7 acceptance criteria | `export/baton_v1_validator.py` — 18 AC checks, each addressable by id |
| 11.8 MIGRATION entry | `export/MIGRATION.md` `## [2026-08-08] baton/v1 …` (top of file, current style) |
| 11.9 coverage reconciliation | `export/baton_v1_stub_consumer.py` — **proven by stub**, not by this table |

**Files added** (all in seam):

| Path | Lines | Role |
|---|---:|---|
| `src/reincarnated/export/baton_v1_schema.py` | ~600 | model family + frozen registers + § 9.5 constant |
| `src/reincarnated/export/baton_v1_emitter.py` | ~560 | run-record → model → wire → atomic write; CLI |
| `src/reincarnated/export/baton_v1_validator.py` | ~470 | 27 addressable checks |
| `src/reincarnated/export/baton_v1_stub_consumer.py` | ~420 | the G-E consumer stub |
| `src/reincarnated/export/baton_v1_fixture.py` | ~400 | synthetic coherent run-record (also the seam's executable reference) |
| `src/reincarnated/export/math/2026-08-08-baton-v1-schema.md` | — | companion math note (Discipline #1) |
| `tests/test_baton_v1.py` | ~370 | 35 tests |

`export/__init__.py` deliberately **not** touched — the sibling `arena_scenario_emitter` is not
exported there either; the baton is reached by module path, adding no import weight.

---

## 2 — AC pass/fail table

All 27 checks run on every write; **an invalid baton is never written.**

| ID | Criterion | Result | How it is actually tested |
|---|---|---|---|
| AC-11.1 | validates against the Pydantic model at the boundary | **PASS** | `from_wire(json.loads(json.dumps(to_wire(b)))) == b` — model equality, not key spot-checks |
| AC-11.2 | consumer-stub round-trip green | **PASS** | stub rebuilds 13 actor placements, 3 wave clocks, 333 path + 333 sweep samples, 384 damage events |
| AC-11.3 | 100 % vs the drax-SIGNED list | **PASS** | **23/23 MUST · 5/5 SHOULD** green by reconstruction (§ 3) |
| AC-11.4a | provenance complete, no field elided | **PASS** | field-set equality against `Provenance.model_fields` + no-nulls |
| AC-11.4b | `declarations[]` `{id,text}`, ID set **equals** the register | **PASS** | set comparison vs `DECLARATION_IDS` (12); negative test removes `D-HP-AFTER` and fails |
| AC-11.4c | `out_of_model[]` `{id,text}`, ID set equals register, no `config.encounter` duplication | **PASS** | set comparison vs `OUT_OF_MODEL_IDS` (9) + companion-field rule — **reading declared, see CD-4** |
| AC-11.4d | truthful PARTIAL passes; missing declaration does not | **PASS** | both directions tested |
| AC-11.4e | dirty tree ⇒ grade ≠ FULL | **PASS** | enforced by **raising at build**, not silent downgrade; both branches tested |
| AC-11.4f | `engine_version_sha == "unknown"` ⇒ hard stop | **PASS** | monkeypatched; asserts no file was written |
| AC-11.4g | `u9_bonus_spawn_state` agrees with `fixture_p06_state` | **PASS** | negative test flips the fixture flag and fails |
| AC-11.4h | § 9.5 block verbatim + complete | **PASS** | constant is **re-extracted from the spec note by regex and byte-compared** (Discipline #9) |
| AC-11.5 | never under the `encounters` key | **PASS** | recursive key search + reserved-marker deep-equality after a real emit + `validate_bundle()` still clean |
| AC-11.6 | `_integrity` equals the structures, stub asserts every one | **PASS** | validator **and** stub check all 8 counts independently |
| AC-11.7a | `run_tick` monotonic, never resets at a wave boundary | **PASS** | absence-of-reset per § 11.4 pin 3 — see CD-9 |
| AC-11.7b | `damage_dealt` unique on (run_tick, target_id, source_skill_id) | **PASS** | 344 rows, 0 duplicates; **81 ticks carry >1 target** (the crowd predicate is live, not hypothetical); negative test appends a dup and fails |
| AC-11.7c | path at every tick + bit-identical to sweep centres | **PASS** | **structural** (§ 5) + validated; two negative tests (wire mutation, and a run-record whose centres disagree) |
| AC-11.7d | equal channel lengths within a track | **PASS** | all four tracks |
| AC-11.7e | `hp_after` non-null on the three members + per-actor reconciliation | **PASS** | chained against the previous **emitted** value; clamps at 0/hp_max exact; tol = 1 unit of `damage_dp` — see CD-8 |
| AC-11.7f | `player_death` carries non-null `source_id` | **PASS** | 1 player death, killer `a013_nemesis_zantarin` |
| AC-11.7g | every row length == `len(columns)` | **PASS** | negative test truncates a row and fails |
| AC-11.8 | MIGRATION entry, current style, at the top, ADR-006 answer + by-name drop list | **PASS** | `export/MIGRATION.md` |
| AC-9.2 | disclosure verbatim in every baton | **PASS** | via AC-11.4h |

**Emitter guards** (prose obligations of § 11 made mechanical, not spec ACs) — all PASS:
`G-COLUMNS` (header ≡ `Event` field order, checked at import too) · `G-EVENT-TYPES` (closed
enum) · `G-IDS` (referential integrity; no actor may claim the reserved player id) ·
`G-M6-LABELS` (point_ids, never slots) · `G-M8-AXIS` (8 keys non-null) · `G-M17-HEALS` (an empty
`player_hp_increase_sources` is asserted against the stream *and* the HP track) · `G-M24-CRIT`
(`NOT_MODELLED` ⇒ `is_crit` null everywhere) · `G-RANGES` (row/sample ranges address the emitted
arrays and contain only their own wave) · `G-PRECISION` (emitted numbers respect `_precision`).

---

## 3 — Stub round-trip vs the 23-MUST list

`python -m reincarnated.export.baton_v1_stub_consumer <baton>` → **23/23 MUST green ·
31/31 total green**. The stub imports **none** of the emitter's models; it parses raw JSON the
way `bundle_loader.gd` does.

| ID | Reconstructed evidence (from the baton alone) |
|---|---|
| M-1 | `fixture_p06_state=True` + `run_p06_enabled=True` — two facts, two fields |
| M-2 | `rotation_speed_multiplier=0.35` |
| M-3 | 6 channel segments, 5 with a resolved TAIL — `{IDLE, CHANNELLING, TAIL}` reconstructible |
| M-4 | `channel_tail_s=0.25`; `soulfire{period_s, direction, start, explosion_radius_m}` |
| M-5 | `hit_test_model=point`, `body_radius_role=NON-CAUSAL`, radii on 13/13 actors |
| M-6 | labels `p01..p06`; every actor and every wave cites a label, never a slot |
| M-7 | `scatter_model=SIM-ROLLED`; **13/13 spawns verified inside `placement_extents_m=8.0`** of their own point |
| M-8 | `+z` up, right-handed, facing `+x` CCW-positive over `(-pi, pi]` — 8/8 keys non-null |
| M-9 | `arena_bounds{shape: rect, 40×40}` |
| M-10 | `OPEN-PLANE — no blocking geometry modelled` |
| M-13 | run_tick never resets across 3 waves; actor_id unique run-wide; `t_s = run_tick × 0.0816` **verified on every row**; `energy_reserved` absolute; `hp_max` POST-SCALING |
| M-14 | 12/13 engaged with `engage_tick ≥ spawn_tick`; **the 13th carries `engage_null_reason`** — the nullable branch is exercised, not merely declared |
| M-15 | outcomes `{cleared, player_death}` + `termination_reason {all_actors_dead, player_hp_zero}`, both versioned; death wave's `t_end_s` **equals** the death time |
| M-17 | `player_hp_increase_sources=[]` **and** the HP track verified never to rise — the declaration is asserted, not smoothed. A second fixture variant with a declared source + `heal_tick` rows passes too |
| M-18 | `monster_attack_model=abstract-schedule` (L-28) |
| M-19 | 1 player death, killer named |
| M-20 | 384/384 damage rows carry **both** `damage_raw` and `damage_applied`; `damage_semantic` states the pair's meaning |
| M-21 | 384/384 carry `target_x/target_y` |
| M-22 | distinct `source_skill_id`: `eor_spin`, `gutsmasher_bleed`, `monster_melee` |
| M-23 | **14 HP timelines read directly off `hp_after`** (no event-sum re-derivation); monotone-non-increasing verified per actor; **9 kill-blow frames located** as the rows whose `hp_after` is 0, each joined to its `death` row |
| M-24 | `crit_model=PTH-BAND`, 45 crit rows |
| M-26 | 344 `damage_dealt` rows, all unique on (tick, target, skill); **81 ticks carry >1 target** |
| M-27 | 333 samples over ticks 0..332, stride 1, centres **bit-identical** to the path |
| M-11 | archetypes `{bruiser, elite_caster, nemesis_melee, swarmer}` — no substring sniff needed |
| M-12 | 1 champion of 13 |
| M-16 | nemesis wave `[43]` |
| M-25 | 40 DoT ticks carry `dot_expires_tick ≥ run_tick` |
| M-28 | declared 2 cleared / 8 killed **joined against** 2 / 8 from the event stream |
| *(extra)* AC-2.1 recheck | **329 player damage rows re-tested against `circle_sweep`; 0 outside the disc.** The picture cannot disagree with the damage, and that is now a load-time assertion |

---

## 4 — Integration-point flags (Phase D/E wiring with gamora)

Nothing below exists in the live recorder at HEAD. The emitter is built against § 11's declared
shapes and driven by `baton_v1_fixture.py`, which is **also the executable reference for this
seam**: whatever gamora hands `build_baton()` must have that dict shape.

**Re-checked against gamora's laps 1–3, which landed either side of my commit**
(`8b0d6b5c`, `9d44b00b`, `409ce8a6` — `simulation/kc2/{channel,disc,energy,devotion,opposition,wave_engine,fixture}.py`).
Her package is a **mechanism library** — pure functions and dataclasses for pools, counts, wave
scaling, arrival schedule, channel/disc/energy math. It contains **no event-stream producer**: no
`run_tick`, no `hp_after`, no `channel_active`, no tracks. The run-loop that stitches mechanisms
into a trace is still to come, so every row below stands.

**Two things fell out of that re-check, and one of them is a real catch:**

- **Convention agreement, independently arrived at.** Her `Arena.emitter_xy()` computes
  `theta = π/2 − (oclock/12)·2π` — *byte-identical* to my fixture's bearing→angle conversion
  (12 o'clock is +y, the hand runs clockwise). Two seams read the same frame the same way without
  consulting each other, which is the corroboration O-4 wanted.
- **IP-14 (NEW): only 4 of 6 emitter bearings exist per sitting.** `ARENA_S1 = (3.0, 5.2, 6.9,
  9.6)` and `ARENA_S2 = (1.8, 10.5, 4.5, 7.5)` are four-tuples, but § 11.4 declares
  `spawn_points[6]` (`p01`..`p06`) and § 10.6 names p05 (ambush) and p06 (bonus) specifically.
  **Two points per sitting have no footage-estimated bearing.** The emitter already tolerates
  this — `bearing_clock` is nullable — but `bearing_grade` must then not claim
  `ESTIMATED-FOOTAGE ±15°` for a bearing that was never estimated. Needs either a declared
  position for the missing two or a null bearing carrying its own reason. Flagged rather than
  improvised: it is a provenance-grade question, which makes it yours.

| # | Field / channel | State at HEAD | What gamora must emit |
|---|---|---|---|
| IP-1 | `circle_sweep.channel_active[]` | absent | per-tick bool; the sweep sample with no active flag cannot distinguish "disc here, not firing" from "firing" (R-34/L-25) |
| IP-2 | `hp_after` | **`fight_events` has no such column** | mandatory non-null on every `damage_dealt` / `dot_tick` / `heal_tick`, for the row's target — player or actor |
| IP-3 | `tracks.circle_sweep` (centre, radius) | no producer | radius per tick; centres are **derived by the emitter** from `player_path` (do NOT send a second source — the emitter rejects disagreement) |
| IP-4 | `run_tick` | recorder has **per-fight** `fight_tick` only | run-wide monotonic tick from 0, never reset. `fight_tick` rides alongside, nullable |
| IP-5 | `geometry_family` | `TelegraphSpec.family` exists; `VALID_FAMILIES` **already carries `"eor_spin"`** (BR-2 landed it) | populate per damage row alongside `geometry_type`; matching on shape alone is the documented silent-blinding failure |
| IP-6 | `axis_convention` (**O-4 answered**) | **read from the sim's own contract** | `spatial_telemetry.TelegraphSpec` declares `angle_unit: "rad"`, *atan2 convention (+x=0, CCW+)*, `frame_origin: "bottom_left", +x right, +y up`; `arena.py` corroborates (`heading_rad=-π/2` is commented "facing south", `+π/2` "facing north (+y)"). Emitter pins `up_axis "+z"`, `handedness "right"`, `ground_elevation 0.0`, `facing_range "(-pi, pi]"`. **gamora confirms at wiring** |
| IP-7 | `actors[].spawn_x/spawn_y` | scatter roll not persisted anywhere | the roll inside `placement_extents_m = 8.0` is causal (AC-10.7) and must be retained per actor |
| IP-8 | `actors[].engage_tick` | no engagement timestamp recorded | tick at which the body reaches the disc, or a non-null `engage_null_reason` |
| IP-9 | `dot_expires_tick` | absent | bleed window end; without it the last body's dressing stops early |
| IP-10 | `player_energy` | no per-tick energy series | `energy` on the **usable** scale (ceiling 1594 = 2576 − 982), `energy_reserved` **absolute** 982 (MO-2) |
| IP-11 | `mobs_in_range` | column exists in `fight_events` | per damage row on the spin |
| IP-12 | `player_hp` / `player_path` tracks | absent | stride 1 on the 12.25 Hz grid across the whole run **including IDLE stretches** (M-27) |
| IP-13 | `source_x/source_y` on damage rows | absent | the player position at the tick — the number the hit test already computed |
| IP-14 | `spawn_points[6].bearing_clock` | gamora's `ARENA_S1`/`ARENA_S2` carry **4** bearings each | 2 of 6 points per sitting have no estimated bearing — declare a position or null the bearing **with its own reason**; do not let `bearing_grade` claim a grade for a bearing nobody measured |

**One guard I deliberately did NOT implement, and why.** A cross-block check that
`tracks.player_hp.hp[tick]` equals the last player-targeted `hp_after` at that tick would catch a
whole class of bar-vs-number drift. It requires pinning a semantic the spec does not state
(is the sample the HP *at* the tick or *after* it resolved?). Rather than invent that and force
gamora to match an unstated convention, I flag it: **if the conductor pins the semantic, the
check is four lines** and I would add it at Phase D.

---

## 5 — Two obligations discharged structurally, not by assertion

1. **"Quantise once, write twice" (M-27 × S1).** The emitter takes `player_path.(x, y)` as the
   single positional source, quantises once, and writes the *identical float objects* into
   `circle_sweep.(centre_x, centre_y)`. If a run-record also supplies centres, they are compared
   after quantisation and a mismatch is a **hard build error**. AC-11.7c can now only fail if
   someone edits the wire form after the emitter ran. (The quantiser is `round()` at the declared
   dp, not toward-zero truncation, because only `round()` is idempotent under a JSON round-trip —
   math note § 4.)
2. **L-27's anti-re-derivation intent.** The AC-11.7e reconciliation chains against the previous
   **emitted `hp_after`**, never a running event sum. The check therefore cannot be satisfied by
   a consumer that integrates damage — which is the behavioural property the ruling wanted,
   expressed as an assertion. drax's WR3-ACC measured that sum under-reading by up to 47.5 %.

---

## 6 — CONDUCTOR-DECISION-NEEDED

| # | Item | What I did (reversible) | Why it needs you |
|---|---|---|---|
| **CD-1** | **Serialisation style vs § 11.2 [S7].** Measured: `indent=2` costs **1.95×** — LOW 16.6 / **MID 33.2** / HIGH 76.8 MB, against `rows-compact` 8.5 / **17.4** / 40.5 MB. MID under the literal form is **outside drax's declared ≈ 22 MB budget** | default `json_style="rows-compact"`; literal form kept as `"indent"`; both deterministic, both `json.loads` to the identical object | It contradicts a spec sentence, and the alternative breaks a consumer budget drax signed. Ratify the default, or rule the literal form and re-open the budget with drax |
| **CD-2** | **`engine_tree_state` untracked-file policy.** Measured on this tree: **0 tracked modifications, ~50 untracked artifacts** under `output/` and `data/`. Under the conservative default (untracked ⇒ dirty) **no baton from this repo can ever grade FULL** | default `untracked_counts_as_dirty=True`; `--allow-untracked` flips it | Worse: the enum is `{clean, dirty}` with **no field recording which policy produced a `clean`**. That makes the policy a run-level pin, not a per-call flag, or the provenance is unrecorded. Rule the policy (and if Phase E wants FULL, the tree must be cleaned or the policy pinned before G-D) |
| **CD-3** | **The player's actor id is undeclared.** The player is not in `actors[]` and the schema has no player-id field; consumers would otherwise infer "not in actors[]" | pinned the literal `"player"`; validator forbids any actor claiming it; stated in MIGRATION | Ratify the convention, or rule a v1.1 additive field. Silent inference is exactly the failure class this seam exists to catch |
| **CD-4** | **AC-11.4c's literal reading contradicts § 11.5's own register.** The register mandates `OOM-DEFENSES` / `OOM-BLESSINGS` / `OOM-MUTATORS`; `config.encounter` types `defenses` / `blessings` / `mutators`. "No entry duplicates a `config.encounter` field" cannot mean "no id may correspond to an encounter key" without making the register self-violating | read as: where an OOM entry names something `config.encounter` also types, the **typed field must be the value carrier** and the OOM row merely the reason — the check fails if the typed field is missing | Ratify the reading, or restate the AC |
| **CD-5** | **§ 9.5 disclosure value form.** The block's first line *is* the key `devotion_envelope_disclosure:` | emitted value = the block minus that key line; every remaining line byte-identical, indentation preserved; a test re-extracts from the spec and byte-compares | Trivial, but AC-11.4h says "verbatim, un-restructured" and dropping a line is technically a structure change |
| **CD-6** | **`waves[].tick_end` inclusivity.** `[lo, hi)` is stated for row/sample ranges; nothing states it for tick spans | pinned **inclusive**; validator requires `waves[i].tick_start > waves[i-1].tick_end` | gamora must match, or wave boundaries will be off by one tick in both directions |
| **CD-7** | **`provenance.binding_rows` / `informative_rows` shape.** § 11.5 leaves them `[...]` | typed as `list[dict]`, free-form entries; the fixture demonstrates `{id, quantity, target, observed, within_tolerance}` | Phase D produces the real deltas. If you want them ID-register-comparable like `declarations`, that is a shape decision better made **before** G-D writes the first one |
| **CD-8** | **AC-11.7e "reconciles exactly."** Both sides are quantised at 2 dp, so bit-exactness is unavailable | implemented as exact **at emitted precision**: tol = `10^-damage_dp` = 0.01, one unit, not a fitted slack; clamps at 0 and hp_max accepted as exact | Ratify the reading |
| **CD-9** | **AC-11.7a "strictly monotonic."** Event rows *cannot* be strictly monotonic in `run_tick` — M-26 requires per-(tick, target) rows sharing a tick | implemented as § 11.4 pin 3's own gloss, **absence-of-reset**: events non-decreasing, track ticks strictly increasing, wave spans non-overlapping | Consistent with pin 3; noted so the gate reads the same thing I tested |

**Not decided here, by design:** O-1 gzip (routed to drax — flag exists, default OFF, measured
7.0× on the fixture as evidence only). O-3 ADR-006 (default-NO honoured and enforced as an
absence in the AST; reversing it makes this an external-DB writer and needs Matt per statement).

---

## 7 — Engine commits

| Commit | Tag | Contents |
|---|---|---|
| `68e2e372` | `star-lord/v1.87-kc2-baton-v1-emitter-1` | 5 new modules + 35 tests + MIGRATION entry + math note + AGENT_STATE checkpoint |

Not pushed (ADR-006 / charter § 6 — Matt's word at end of run).

**Smoke (Discipline #2):** `tests/test_baton_v1.py` 35 passed. Adjacent export suites re-run:
`test_export.py`, `test_one_realm_bundle_assembler.py`,
`test_cycle13_wave4_export_schema_round_trip.py` — all green.

**Pre-existing failure, NOT mine, NOT picked up:**
`tests/test_kit_space_emitter.py::TestMultiKitEmit` — 4 failures,
`unrecognized dominant_element='water'` (the water→ice substrate rename left this emitter's
element vocabulary behind). It fails identically without my change; my files are new and nothing
imports them. Per my standing rule I am **flagging it for a knight-rider dispatch rather than
fixing it autonomously** — it is in my seam, small, and well-grounded, which is exactly the
profile that tempts a silent pickup.

---

## 8 — What Phase D/E can do with this today

```bash
# emit
python -m reincarnated.export.baton_v1_emitter --run-record run.json --out baton.json
# prove consumability the way G-E requires
python -m reincarnated.export.baton_v1_stub_consumer baton.json
```

The stub's exit code is the G-E signal: **0 only when every MUST reconstructs.** Coverage is
proven by the stub; emission is not the bar.
