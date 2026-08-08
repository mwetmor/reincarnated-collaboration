# KC2-SIM — baton schema v1: export-seam consult (star-lord)

**Date:** 2026-08-08
**Author:** star-lord (export / output / telemetry / llm seam)
**Run:** KC2-SIM autonomous run, Phase B (conductor: gandalf, RUN-CONDUCTOR)
**Consult target:** `gandalf/notes/2026-08-08-kc2-sim-battle-spec.md` § 11 (DRAFT-FOR-CONSULT, §§ 11.1–11.6)
**Status:** CONSULT — advisory. Final schema form is a conductor ruling under R-KC2-7, veto-open.
**Verified against:** `reincarnated-engine` HEAD `ebf13240`
**Scope discipline:** no production code this session; no commit (charter § 4.7).

---

## Verdict summary

| Q | Subject | Verdict |
|---|---|---|
| 1 | § 11.2 conventions table | **CORRECT, INCOMPLETE** — 5/5 line cites hold at HEAD; 5 conventions missed, 1 row is true-but-misleading |
| 2 | § 11.4 field inventory | **AMEND BEFORE BUILD** — 5 naming divergences, 1 acceptance-criterion failure (AC-2.1), size is a real problem |
| 3 | § 11.5 provenance | **NO CONFLICT, 5 STRUCTURAL GAPS** — one of them (dirty tree) makes the artifact's central claim unfalsifiable |
| 4 | MIGRATION entry shape | **CITES THE WRONG GENERATION** — v1.6/v1.7/v1.10/v1.12 are the 2026-05-27 style; HEAD's style changed |
| 5 | Duplication | **1 COLLISION, 2 PARTIALS, 1 lineage claim** — `arena_scenario_emitter.py` is the collision |

**Size headline (measured, not estimated):** § 11.4 as written emits **~31.6 MB** for the mid-case
93-wave run. The largest artifact Godot currently parses is **3.29 MB**. Three export-side
conventions (precision truncation, columnar tracks, row-array events) bring that to **~8.4 MB**
with no loss of information and no presentation-side sample-rate decision. Detail in Q2 (f).

---

## Q1 — § 11.2 conventions table: correct and complete?

### Line cites — all five hold at HEAD `ebf13240`

| Cite | Status | What is actually there |
|---|---|---|
| `EXPORT_FORMAT_VERSION` `schemas.py:149` | **HOLDS** | `EXPORT_FORMAT_VERSION = "1.0"` — a **string** |
| `ExportMetadata.format_version` `schemas.py:373` | **HOLDS** | class at `:372`, field at `:373`, defaults to the constant |
| Pydantic-at-boundary `season_exporter.py:972–974` | **HOLDS** | comment tail at `:971–972`, the write boundary itself at `:973` (`_write_json(output_path, report.model_dump())`) |
| MIGRATION chain, v1.6/v1.7/v1.10/v1.12 | **HOLDS as entries** | v1.6 `:4725`, v1.7 `:4628`, v1.10 `:4200`, v1.12 `:3808` — but **stale as the entry-shape precedent**, see Q4 |
| `record_fight_events()` `recorder.py:952–1025` | **HOLDS** | `def` at `:952`, closing `except` at `:1024–1025`. `SCHEMA_VERSION = "2.17"` at `recorder.py:22` — § 11.1's "schema v2.17" claim is correct |

The `record_fight_events()` spine, precisely: **REQUIRED** `event_type` + `fight_tick`; everything
else is Pattern-P7 defensive-get → NULL. The optional column set is `geometry_type`,
`damage_source_tag`, `damage_dealt`, `mobs_in_range`, `skill_type`, `damage_taken`,
`mitigation_source`, `resource_cost`, `resource_gained`, `recovery_source`, `schema_version`.
§ 11.2 row 6 says "geometry/damage fields" — that undersells it; the full column list matters for
Q5/D2.

### What the table missed — five conventions

**M1 — `export/arena_scenario_emitter.py` is the closer precedent and is not cited at all.**
MIGRATION § v1.77 (2026-06-15). It is the **only existing engine→Godot JSON contract** and it sets
four conventions the season-exporter lane does not:

- **Underscore-prefixed root provenance keys:** `_generated_from`, `_schema_version` (**int `1`**,
  not a string), `_emitted_at` (`"%Y-%m-%dT%H:%M:%SZ"`), `_do_not_hand_edit` (the regen command).
- **Determinism:** `json.dumps(payload, sort_keys=True, indent=2, ensure_ascii=True) + "\n"`.
- **Atomic write:** `.json.tmp` → `os.replace`, with the reason stated in the source —
  *"prevents partial reads by Godot/drax"*.
- **Validation is assert-based** `_validate_payload()` over `frozenset` required-field sets — **not
  Pydantic**.

That last point makes § 11.2 row 2 true-but-misleading. "Pydantic validation at the export
boundary" is the convention of the *season* lane; the *Godot-facing* lane at HEAD does not do it.
The baton should use Pydantic anyway (it is the stronger discipline), but the MIGRATION entry has
to **say it is diverging**, or the next reader finds two Godot-facing emitters validating two ways
with no stated reason.

Related: the two write helpers in `export/` already disagree.
`season_exporter._write_json` (`:1092–1093`) is `json.dumps(data, indent=2, ensure_ascii=False)` —
no `sort_keys`, no atomic replace. **The baton must pick one explicitly.** I recommend the
`arena_scenario_emitter` form, because the baton is a *reproducibility* artifact and two batons
from the same seed should diff to nothing.

**M2 — `export/run_registry.py` already owns `run_id`.** `make_run_id()` (`:135`) is UUID4;
`emission_runs` (`:70`) is `run_id TEXT PRIMARY KEY`; `register_run()` is `INSERT OR REPLACE`,
idempotent on `run_id`. If the baton mints its own `run_id` we have two `run_id` namespaces in one
seam. Either it **is** an `emission_runs.run_id` (which makes the emitter an external-DB writer →
ADR-006, Matt-authorized per statement) or it is a distinct namespace and must be **named** so.

**M3 — `config_hash` precedent, twice.** `run_registry.compute_config_hash()` (`:140`) and
`one_realm_bundle_assembler._compute_config_hash()` — both sha256, truncated to 16 hex chars, over
a deterministic config string. The baton's `config` block is exactly the thing that wants one: it
lets a consumer tell two batons apart without diffing 8 MB.

**M4 — `stage2_run_record` is the embedded-provenance precedent, not `ExportSimCyclingRecord`.**
`_build_stage2_run_record()` (`one_realm_bundle_assembler.py:794–834`) is a self-describing
provenance dict embedded *in* the artifact: `run_id / timestamp / season_id / engine_version /
config_hash / …counts / stage / gauntlet_summary / cert_status / notes`. § 11.2 row 5 cites
"wave/cycle/node on `ExportSimCyclingRecord`", which is a weaker analogy. `stage2_run_record` also
models the thing § 11.5 needs and does not have: **declared-null with a `notes` string saying why
it is null**, rather than a bare `null`.

**M5 — `engine_version` sourcing is already solved, and the solved version is still not enough.**
`telemetry/db.py:52 get_engine_version()` = `git rev-parse --short HEAD`, returning `"unknown"` on
any failure. `kit_space_emitter.py:104–135` extends it: `_get_engine_version_short()` +
`_get_engine_version_full()` (40-char), emitted as `engine_version_sha` + `engine_version_full`,
plus `engine_provenance: f"engine-{sha}-{event_id}"`. **Neither records whether the tree was
dirty.** See Q3/P1 — for this artifact that is not a nicety.

---

## Q2 — § 11.4 field inventory: emitter-side critique

### (a) Naming — five divergences from vocabulary already serialized in this seam

| § 11.4 | Existing serialized name | Where |
|---|---|---|
| `tier` | `threat_tier` (+ its partner `archetype_tag`) | `arena_scenarios.json`; `arena.py` |
| `facing` | `heading_rad` | `arena.py:179`; `_PosProbe` `spatial_engine.py:1989`; every spawn in `arena_scenarios.json` |
| `damage_type` | `damage_source_tag` | `fight_events` column, `recorder.py:1005` |
| `tick_damage` (enum member) | `damage_dealt` | `recorder.py:986` branches on `event_type == "damage_dealt"` |
| `t`, `t_start`, `t_end`, `spawn_time` | `_s` suffix — `elapsed_s`, `max_duration_s`, `soft_timeout_s` | `SpatialFightResult`; `arena_scenarios.json` |

The `_m` suffix is equally established (`width_m`, `height_m`, `leash_distance_override_m`).
`config.kit` gets this **right** (`tick_period_s`, `radius_m`, `weapon_damage_pct`) — it is the one
block in § 11.4 that needs no naming redline. `placement_extents: 8.0` in the sibling `arena` block
is metres and does not say so.

The `tick_damage` → `damage_dealt` item is the one with teeth: `record_fight_events()` runs its
Pattern-P7 geometry guard on `event_type == "damage_dealt"` (`recorder.py:986–991`). A baton stream
labelled `tick_damage` would ingest with that guard **silently inert** — which is precisely the
"schema drift, silent field drop" failure this seam exists to catch.

### (b) Nesting depth — fine, with one exception

§ 11.4 is ≤ 3 levels, and `arena_scenarios.json` already runs 4 (root → `scenarios` →
`<scenario_id>` → `mob_spawns[]` → fields). No structural objection. The exception is
`events[].position{x, y}` — a 4th level wrapping two floats. **There is no `{x, y}` object anywhere
in this project's serialized surface.** Engine entities carry flat `.x`/`.y`
(`spatial_engine.py:1855` returns the tuple; `_PosProbe` at `:1989` carries `(.x, .y,
.heading_rad)`), and `arena_scenarios.json` serializes `player_spawn` and `mob_spawns[]` flat.
Flatten to `x`, `y`. A 2-element array `[x, y]` is worse than either, because GDScript index access
loses the field name from every error message a consumer might produce.

### (c) Types — `baton_trace_format: "v1"` is a third version encoding

`EXPORT_FORMAT_VERSION` is the string `"1.0"`. `arena_scenarios.json` `_schema_version` is the int
`1`. `baton_trace_format: "v1"` is a string with a `v` prefix — a third form, and the one a Godot
loader can least easily compare (`>= 1` works on an int; `"v1" >= "v1.10"` is a lexicographic
trap). **Keep `baton_trace_format: "v1"` as the human label and additionally carry
`_schema_version: 1` as an int**, so the loader idiom that already exists for `arena_scenarios.json`
transfers unchanged.

### (d) Pydantic model family — nested, and I measured the objection to it away

I expected per-event Pydantic to be prohibitive. **It is not, and I am reporting the measurement
rather than the assumption** (Discipline #10). Measured on this machine, pydantic 2.13.3, a 10-field
event model with a nested position model:

```
model_validate  ×80,000 : 0.25 s  (3.1 µs each)
model_dump      ×80,000 : 0.17 s
```

Even the 198 k-event high case is ~0.6 s of validation. So: **build the full nested family** —
`BatonV1` → `SpecPin` / `SimPin` / `Config{Fixture, Encounter, Kit, Arena}` / `Actor` / `Wave` /
`Event` / `Tracks` / `Provenance` — and validate everything. One flat model would be unreadable and
would lose the per-block reuse that makes `Provenance` independently testable against AC-11.4.

**But decouple the validated in-memory model from the wire form.** The size work in (f) wants
columnar tracks and row-array events; those are *serialization* shapes, not *validation* shapes. The
emitter validates rich nested objects, then flattens at the write boundary; the round-trip test
inflates rows back into objects and asserts model equality. Discipline #8 stays strict, the artifact
stays small, and the two concerns stop fighting.

### (e) TIME representation — both, and the tick is the identity

Emit **both**, with a stated rule:

- **`fight_tick` (int) is the identity.** It joins to `fight_events`, it is exact, and § 11.2 row 6
  claims the baton keeps that spine — dropping the required field of the spine it claims to keep
  would be a hollow claim. `record_fight_events()` *rejects* a row missing `fight_tick`
  (`recorder.py:977–984`, logged as a silent-drop).
- **`t_s` (float seconds) is derived**, `= fight_tick × tick_period_s`, and is rounded per (f).
  Presentation interpolates at display rate, not at 12.25 Hz, so it needs real seconds.
- **`tick_period_s` is emitted once** in `config.kit` (§ 11.4 already does this) so a consumer can
  re-derive and assert the two agree.

The rule that matters: **`t_s` is never a key.** Float equality across a JSON round-trip is exactly
how a trace starts disagreeing with itself. Any cross-reference between blocks (`waves[]` →
`events[]`, `tracks` → `events[]`) uses `fight_tick`.

For the tracks specifically, `t_s` should not be emitted per sample at all — see the `_tick_base` +
`_sample_stride` redline. That is arithmetic on an emitted constant, not re-derivation of a
sim-owned quantity, so § 11.3's no-re-derive rule is untouched.

### (f) SIZE — measured, and it is a problem

**Run geometry, taken from the spec's own § 10.9 clear-time distribution** (so the estimate is
grounded in the fixture, not in a guess): 9 waves at mean 28.57 s + 83 waves at mean 14.29 s =
**1,443.2 s ≈ 24.1 min**. At `tick_period_s = 0.0816` that is **17,686 ticks**.

**Per-record bytes, measured** by serializing records built exactly as § 11.4 declares them:

| record | pretty `indent=2` | compact | compact + 3 dp |
|---|---|---|---|
| `events[]` element | **316 B** | 260 B | 224 B |
| `circle_sweep[]` element | 136 B | 104 B | 78 B |
| `player_path[]` element | 107 B | 90 B | 51 B |
| `player_hp` / `player_energy` element | 53 B | 44 B | 28 B |

Full-precision Python float repr is a large share of that: `1443.2160000000001` is 18 characters,
`-1.5707963267948966` is 19. `arena_scenarios.json` emits exactly that today.

**Totals.** Event count = ticks × channel uptime × mean bodies inside the 3.0 m disc:

| scenario | events | § 11.4 as written | compact + 3 dp | columnar tracks + row-array events + 3 dp | + gzip |
|---|---|---|---|---|---|
| LOW — 50 % uptime, 4 in disc | 35 k | 17.4 MB | 11.2 MB | ~4.0 MB | ~0.9 MB |
| **MID — 65 %, 7 in disc** | **80 k** | **31.6 MB** | 21.3 MB | **~8.4 MB** | **~1.9 MB** |
| HIGH — 80 %, 14 in disc | 198 k | 68.8 MB | 47.6 MB | ~20 MB | ~4.4 MB |

**Why 31.6 MB is a problem and 45 MB elsewhere in `output/` is not.** The largest artifact in
`src/reincarnated/output/` is `w3_batch1_bundle.json` at 45.3 MB — but nothing consumes it in a game
loop. The largest artifact **Godot** parses is `one_realm_demo_bundle.json` at **3.29 MB**, and
`reincarnated-godot/scripts/bundle_loader.gd:98` does `JSON.parse_string(txt)` — whole file into a
String, then the whole tree into Variants. The hazard is not the disk figure; it is 80 k
Dictionaries with ten keys each materialised at once. The MID case as written is ~10× the largest
thing that loader has ever been handed.

**Seven export-side conventions. None of them sets a sample rate.**

**S1 — Precision truncation at the write boundary, declared in the artifact.**
Positions and radii → 3 dp (mm: 500× finer than the 0.5 m entity radius). `t_s` → 4 dp (0.1 ms
against an 81.6 ms tick). `damage_dealt` → 2 dp. Emit
`_precision: {position_dp: 3, time_dp: 4, damage_dp: 2}` at root so a consumer never has to guess
whether a difference is real or rounding. Measured lever alone: **1.4×**. *This is a new convention,
not an inherited one* — `arena_scenarios.json` emits full repr today, so I am proposing it, not
citing it.

**S2 — Columnar (struct-of-arrays) `tracks`.**
`player_path: {tick: [...], x: [...], y: [...], heading_rad: [...]}` rather than an array of
objects. Measured on 17,686 samples × 4 channels: **0.51 MB columnar vs 1.89 MB as pretty
objects — 3.7×**; gzips to 0.19 MB. Tracks are dense and uniform-shape, the textbook case.
Boundary invariant to assert: every channel array within one track has equal length.

**S3 — Row-array + declared column header for `events[]`.**
`events: {columns: [...], rows: [[...], ...]}`. Measured at 80 k events: **7.84 MB vs 18.06 MB as
compact objects — 2.3×**. The `columns` header is load-bearing; without it the artifact is
unreadable by inspection and I would not propose the shape.

**S4 — gzip is the single biggest lever (~10×) and is NOT mine to impose.**
Measured 7.84 MB → 1.67 MB. Godot reads standard gzip via
`PackedByteArray.decompress_dynamic(..., FileAccess.COMPRESSION_GZIP)`, but that is a change inside
drax's loader. **Route as a yes/no to drax's consult; do not assume it.** If the answer is no,
S1+S2+S3 land MID at ~8.4 MB — 2.6× the current largest Godot artifact, which is a step, not a leap.

**S5 — A chunking hook, not chunking.** Do not shard v1. Make sharding a later *additive* change by
giving each `waves[]` entry `event_row_range: [lo, hi)` and `track_sample_range: [lo, hi)`. A v1.1
that splits per-wave files then breaks nothing, and a consumer wanting only wave 160 (the § 10.8
showcase) can slice without loading 8 MB. Cost: two fields × 93 waves.

**S6 — A down-sample hook, not a down-sample rate.** Emit
`tracks._sample_stride: {player_path: 1, circle_sweep: 1, player_hp: 1, player_energy: 1}` at v1,
meaning *every tick*. If drax later wants `player_path` at stride 3, the field already exists and
the consumer already reads it — **no schema entry, no MIGRATION break.** This is the export-side
mechanism that lets drax's sample-rate answer land without reopening the schema, which is the
correct division of the question.

**S7 — Write discipline:** adopt `arena_scenario_emitter`'s `.tmp` → `os.replace` and
`sort_keys=True`. Sorting keys costs nothing under a columnar layout (arrays keep their order; only
key order sorts) and makes two batons from the same seed diff to nothing.

### (g) POSITION representation — flat scalars, `heading_rad` for orientation

Grounded, not stylistic: engine entities carry flat `.x`/`.y` (`spatial_engine.py:1855`); the probe
type carries `(.x, .y, .heading_rad)` (`:1989`); `arena_scenarios.json` serializes every
`player_spawn` and `mob_spawns[]` entry as flat `x`, `y`, `heading_rad`, `entity_radius`. There is
no nested position object and no coordinate array anywhere in the serialized surface. Note both
spellings of *centre* exist in Python identifiers (33 `centre`, 129 `center`) — but **neither
reaches a serialized field name**, so the baton is free to pick, and should pick `centre_x` /
`centre_y` only if it matches whatever § 11.4's final ruling says. My redline keeps `centre_*`
since § 11.4 chose it, and flags only the flattening.

---

## Q3 — § 11.5 provenance block

**No conflict with existing export provenance-field precedent.** § 11.5 is structurally compatible
with `_build_stage2_run_record()` (`one_realm_bundle_assembler.py:794–834`), which is the closest
analog: an embedded, self-describing provenance dict carrying pins + counts + status + notes. It is
also compatible with `kit_space_emitter`'s `engine_provenance` / `engine_version_sha` fields and with
`run_registry`'s `emission_runs` columns. Nothing here has to be re-negotiated.

**Five things are structurally missing for a consumer to trust the artifact.**

**P1 — `sim_pin.engine_commit` cannot support the claim the baton makes.**
`get_engine_version()` (`telemetry/db.py:52`) returns a 7-char SHA, or the string `"unknown"` on any
failure — a `try/except` that swallows everything. It does **not** capture working-tree state. This
run's spec and probe notes are, per ledger §§ A.2–A.7 and § B.3, *uncommitted at consult time*; a
Phase-C emitter run from a working tree with local edits would stamp a clean SHA on a run that did
not come from that SHA. For an artifact whose entire purpose is a calibration-grade provenance
claim, that is a false statement, not a rounding error.

Add: `engine_version_full` (40-char, the `kit_space_emitter._get_engine_version_full()` idiom
already exists) and **`engine_tree_state: "clean" | "dirty"`** from `git status --porcelain`. Then
make it enforceable: **a dirty tree cannot emit `calibration_grade: FULL`.** That is one guard at
the write boundary and it is exactly the class of thing Discipline #8 is for. Also: `"unknown"`
must be a *hard stop* for a baton, not a fallback string — the existing helper's tolerance is right
for telemetry rows and wrong here.

**P2 — `spec_pin` names commits for files that are uncommitted right now.**
Ledger § B.3 marks the spec "uncommitted → rides G-B close"; §§ A.2–A.7 say the same of seven probe
notes. By Phase C those commits should exist — but the emitter must not silently write `null` if
they do not. Add **`spec_pin.pin_state: "COMMITTED" | "UNCOMMITTED-WORKING-COPY"`** plus
**`spec_pin.spec_sha256`** of the spec file's bytes. A baton reading
`{spec_note: <path>, charter_commit: null}` is unfalsifiable; one reading
`{pin_state: "UNCOMMITTED-WORKING-COPY", spec_sha256: "abc123…"}` is checkable by anyone holding the
file. This is the `stage2_run_record` "declared-null with a reason" pattern (M4) applied where it
matters.

**P3 — nothing lets a consumer verify it read the whole artifact.**
For an ~8 MB file crossing a repo boundary into a different runtime, add at root:
`_integrity: {event_row_count, actor_count, wave_count, track_sample_counts: {...}}`. AC-11.2's stub
consumer then has something to assert beyond "it parsed". This is the cheapest available defence
against the failure mode this seam actually sees — silent field drops and truncated writes — and it
converts AC-11.2 from a reconstruction exercise into a reconstruction exercise **with a checksum**.

**P4 — AC-11.4 is not testable as written.**
`declarations` is a list of prose strings. Four of the nine carry stable IDs (G-5, G-2, G-4, G-7);
five do not (the arena-positions declaration, the identity-envelope declaration, the mutators
declaration, the two s2-confound declarations). AC-11.4 says "no declaration dropped" — against
prose that is an eyeball check. Make every entry **`{id, text}`** and the criterion becomes a set
comparison against a declared ID register. Same for `out_of_model`: a list of 11 free-form phrases,
several of which duplicate `config.encounter` fields (`mutators: "OUT-OF-MODEL"` appears in both).

**P5 — `u9_closure_state` carries typed facts inside a prose string.**
`CLOSED (1.9% intra-order residual declared; U9-6 bonus-spawn state = <resolved|UNKNOWN, +-8.4%
branch>)` embeds three separate machine-relevant values in one string — and the bonus-spawn fact is
**already typed two blocks up** as `config.encounter.bonus_spawn_p06: <bool|"UNKNOWN">`. Two
encodings of one fact in one artifact is how they drift apart. Split into
`u9_closure_state`, `u9_intra_order_residual_pct`, `u9_bonus_spawn_state`,
`u9_bonus_spawn_branch_pct`, and have the emitter **assert** `u9_bonus_spawn_state` agrees with
`config.encounter.bonus_spawn_p06` at the write boundary.

**Minor:** `seed_pins` needs `rng_algorithm`. A seed without the generator that consumed it does not
reproduce anything across a Python or numpy version bump, and `SpatialFightResult.seed` has the same
gap today.

---

## Q4 — MIGRATION entry shape

**§ 11.2's MIGRATION row is right in substance and cites the wrong generation of precedent.**

`export/MIGRATION.md` is 8,733 lines, **reverse-chronological — newest at the top**. The cited
entries are all from one day, 2026-05-27, and use a heading style the file has since left behind:

```
## § v1.12-wave-3-seam-2-f-c-export-faction-relationship — F-C … (2026-05-27)
**Author:** / **Dispatch:** / **Authority:** / **Discipline compliance:** /
**ADR compliance:** / **Composes with:**
```

HEAD's two most recent entries — `## [2026-07-29] HQ-2 …` (`:8`) and
`## [2026-07-22] W3 emission-demo-critical …` (`:56`) — use:

```
## [YYYY-MM-DD] <title>
**Author:** / **Run:** / **Source:** / **Consumer impact:**
```

**Write the baton entry in the current shape, at the top of the file.** Recommended skeleton:

```
## [2026-08-XX] baton/v1 — first JSON event-trace emitter (KC2-SIM Phase C)

**Author:** star-lord
**Run:** KC2-SIM 2026-08-08 (conductor: gandalf), Phase C
**Source:** spec `agentic_orchestration/gandalf/notes/2026-08-08-kc2-sim-battle-spec.md` § 11
  (§ 11.4 as amended by the 2026-08-08 star-lord consult + conductor ruling)
  · charter R-KC2-7 (truth boundary; final schema form is a conductor ruling, veto-open)
  · ledger `2026-08-07-kc2-sim-run-ledger.md` § A.1 (P-X1 emission-format recon; L-1 namespace guard)
  · G-B fold commit <sha>
**Consumer impact:** NEW artifact for drax (`reincarnated-godot/` presentation). No change to
  `one_realm_demo_bundle.json`, `arena_scenarios.json`, or any existing key. `encounters` UNTOUCHED
  and still reserved (L-1 / AC-11.5).
```

…and then **restore three header lines the newer style dropped**, because this change earns all
three where the last two did not:

- **`**Discipline compliance:**`** — #1 (companion math note), #2 (smoke test), #8 (Pydantic +
  `_integrity` at the write boundary), #10 (the size figures are measured, not assumed).
- **`**ADR compliance:**`** — ADR-004 (cross-seam schema change ⇒ MIGRATION.md). **ADR-006 must be
  answered explicitly, not omitted:** does the emitter write a row to `emission_registry.db`? If
  yes, that is an external-DB write and needs Matt authorization per statement. If no, say so — the
  answer determines M2's `run_id` namespace question.
- **`**Composes with:**`** — § v1.77 (`arena_scenario_emitter`, the sibling Godot-facing emitter);
  § v1.86 (run registry); `[2026-07-22]` (the `encounters` reservation this artifact must not
  occupy).

**Two things this entry must state that no prior entry had to:**

1. **The drax-SIGNED coverage list, by path.** AC-11.3 makes drax's signature — not the spec — the
   acceptance bar. The precedent exists: the `[2026-07-22]` entry's companion is
   `export/drax-SIGNED-encounters-delta-2026-07-22.md` (verdict SIGN-WITH-CONDITIONS, filed in
   `export/`, reviewing named artifacts point by point). The baton entry cites its equivalent the
   same way.
2. **The validation divergence from `arena_scenario_emitter`** — Pydantic here, assert-based
   `_validate_payload()` there — stated with the reason. Otherwise the next reader finds two
   Godot-facing emitters validating two different ways and no note saying which is intentional.

**Companion math note**, per Discipline #1 and the `[2026-07-22]` precedent
(`export/math/2026-07-22-one-realm-bundle-schema-delta.md`, cited from its MIGRATION entry):
`export/math/2026-08-XX-baton-v1-schema.md`, carrying the Q2(f) size measurements so the MIGRATION
entry cites rather than restates them.

---

## Q5 — Duplication check

**Nothing duplicates the baton whole.** P-X1's read holds: event-level data is telemetry-DB-resident
and every batch JSON in `output/` is aggregates-only. The baton is the engine's first JSON
event-trace surface. **But three things do part of it, and one is a genuine collision.**

### D1 — COLLISION: `export/arena_scenario_emitter.py` already owns arena geometry → Godot

MIGRATION § v1.77 (2026-06-15). It serializes
`simulation.spatial_gauntlet.arena.ALL_SCENARIOS` → `reincarnated-godot/data/arena_scenarios.json`
(16 KB, `_schema_version: 1`, `_emitted_at: 2026-06-15T18:28:18Z`, 6 scenarios). Per scenario it
carries `player_spawn` and `mob_spawns[]` as
`{x, y, heading_rad, entity_radius, is_boss, threat_tier, archetype_tag,
leash_distance_override_m, suppress_leash_hp_reset}`, plus
`arena {width_m, height_m, name, choke_zones[]}`, `max_duration_s`, `soft_timeout_s`,
`win_condition`, `boss_index`, `mini_boss_index`.

§ 11.4's `config.arena {emitter_positions[6], player_spawn, placement_extents: 8.0}` declares the
same *kind* of fact, for a different arena, in a different vocabulary, in a different file, **to the
same consumer**. That is the drift this seam exists to prevent, and it is worth catching now rather
than when a Godot session has two arena vocabularies open.

Two honest resolutions. **I recommend (b).**

- **(a) Single-source it.** Add the Crucible arena as a 7th entry in `arena.py`'s `ALL_SCENARIOS`,
  regenerate `arena_scenarios.json`, have the baton reference `scenario_id`. Geometry stays
  single-sourced and the emitter already exists. Costs: a change in `arena.py` (gamora's seam, not
  mine) and a re-handshake on a drax-consumed file.
- **(b) Keep `config.arena` in the baton, adopt the existing vocabulary verbatim.** The Crucible
  arena is run-specific and DECLARED (§ 10.6, footage-estimable free parameters), not a stable
  engine scenario — so embedding it is defensible. But use `width_m` / `height_m` / `x` / `y` /
  `heading_rad` / `entity_radius`, and add **`arena_schema_kinship: "arena_scenarios.json v1"`** so
  the relationship is stated *in the artifact*, not only in a note. If the Crucible arena later
  stabilizes, promotion to `ALL_SCENARIOS` is then mechanical.

**Not acceptable:** shipping `emitter_positions` / `placement_extents` as a third vocabulary for
spawn geometry with no declared relation to the two that exist.

### D2 — PARTIAL: `fight_events` already defines what an event *is*

`telemetry/recorder.py record_fight_events()` (`:952–1025`), schema 2.17. The baton must not become
a second, divergent definition. **Rule I would apply:** the baton's event column set is the
`fight_events` column set **plus** the baton-only additions (`t_s`, `wave`, `source_id`,
`target_id`, `x`, `y`, `geometry_family`), and any `fight_events` column the baton drops is dropped
**by name in the MIGRATION entry**, not by silent omission.

§ 11.4 currently drops eight columns silently: `damage_source_tag`, `mobs_in_range`, `skill_type`,
`damage_taken`, `mitigation_source`, `resource_cost`, `resource_gained`, `recovery_source`. At least
three of those — `damage_taken`, `mitigation_source`, `resource_cost` — are things § 11.3 explicitly
claims as **sim-owned causal truth** (player HP track, energy track). Under a row-array layout a
null column costs one byte per row, so the case for dropping them is weak.

### D3 — PARTIAL: `export/run_registry.py` already owns run identity + provenance

`emission_runs` table, `make_run_id()` UUID4, columns `run_id / timestamp / season_id /
engine_version / config_hash / … / stage / cert_status / notes`, plus `compute_config_hash()` and
`update_cert_status()`. See M2 and M3. Extend rather than parallel: reuse the config-hash idiom, and
either register the baton run (ADR-006 write authorization) or declare `baton_run_id` a distinct
namespace with an optional `emission_run_id` cross-reference. `cert_status` is also the natural
partner of `provenance.calibration_grade` — worth a line saying whether they are the same axis.

### D4 — NOT duplication, but the baton closes a three-month-old open flag

MIGRATION § v1.15 (2026-05-18, lines `:7268–7278`), *"OBSERVATION — positional telemetry gap"*:

> `fights.jsonl` contains no spatial data: no monster spawn positions, no AOE cast positions, no
> player movement trajectories. […] Recommended future instrumentation: 1. `fights.jsonl`: emit
> `monster_spawn_positions` array + `player_spawn_position` per fight […] **Flagged to knight-rider
> for future dispatch.**

That dispatch never came. `aoe_cast_events` (`telemetry/aoe_cast_event.py:71–79`) still carries
`true_radius` / `apparent_radius` and **no position at all**. The baton is the first artifact that
closes that flag, and the MIGRATION entry should say so — it converts a standing open observation
into a closed one, and that lineage belongs in the log.

**Also worth noting as prior art, not duplication:** `fights.jsonl` is a real JSONL precedent in
this project — but only as an *ingest* source (`scripts/ingest_fights_jsonl_to_telemetry.py`), never
as an emitter output. There is no gzip, no NDJSON, and no streaming-write machinery anywhere in
`export/` or `telemetry/` at HEAD. If S4 (gzip) is adopted, it is a new capability, and the
MIGRATION entry should say that too.

---

## REDLINE — § 11.4 field inventory (changed lines only)

Convention: `-` = spec line as drafted, `+` = proposed replacement. Unchanged lines are omitted.
One reason per redline. **R-8, R-16 and R-22 are the three I would not ship without.**

### Root

```diff
  ├── baton_trace_format: "v1"
+ ├── _schema_version: 1
+ ├── _generated_from, _emitted_at, _do_not_hand_edit
+ ├── _precision  { position_dp: 3, time_dp: 4, damage_dp: 2 }
+ ├── _integrity  { event_row_count, actor_count, wave_count, track_sample_counts{} }
```
- **R-1** `+_schema_version: 1` (int) — the Godot loader's existing version idiom is the int form from `arena_scenarios.json`; `"v1"` is a lexicographic-comparison trap. Keep both: `"v1"` is the human label.
- **R-2** `+_generated_from / _emitted_at / _do_not_hand_edit` — the three root provenance keys every engine→Godot artifact already carries; without `_do_not_hand_edit` someone hand-edits an 8 MB trace.
- **R-3** `+_precision` — a consumer must be able to tell rounding from signal; declaring the truncation is what makes S1 safe.
- **R-4** `+_integrity` — gives AC-11.2's stub consumer something to assert beyond "it parsed"; the cheapest guard against a truncated write crossing a repo boundary.

```diff
- ├── run_id, emitted_at
+ ├── baton_run_id, emission_run_id | null, config_hash
```
- **R-5** `run_id` → `baton_run_id` (+ optional `emission_run_id`) — `run_id` is already `emission_runs`' primary key (`run_registry.py:70`); two namespaces under one name is a join waiting to go wrong.
- **R-6** `emitted_at` → `_emitted_at` (moved to R-2) and `+config_hash` — the existing sha256[:16] idiom lets a consumer distinguish two batons without diffing 8 MB.

```diff
- ├── spec_pin  { spec_note, charter_commit, ledger_commit }
+ ├── spec_pin  { spec_note, spec_sha256, charter_commit, ledger_commit, pin_state }
- ├── sim_pin   { engine_commit, sim_module_version, seed }
+ ├── sim_pin   { engine_version_sha, engine_version_full, engine_tree_state,
+ │               sim_module_version, seed, rng_algorithm }
```
- **R-7** `+spec_sha256, +pin_state` — the spec and seven probe notes are uncommitted as of this consult; a null commit field is unfalsifiable, a content hash is checkable by anyone holding the file.
- **R-8** `engine_commit` → `engine_version_sha` + `engine_version_full` + **`engine_tree_state`** — the existing helper returns 7 chars or `"unknown"` and never reports a dirty tree; a baton stamping a clean SHA on an edited tree is a false provenance claim, which is the one thing this artifact cannot afford. Guard: dirty tree ⇒ `calibration_grade` may not be FULL.
- **R-9** `+rng_algorithm` — a seed without its generator reproduces nothing across a runtime bump.

### `config.arena`

```diff
- │   └── arena  { emitter_positions[6], player_spawn, placement_extents: 8.0,
- │                positions_provenance: "DECLARED" }
+ │   └── arena  { arena_schema_kinship: "arena_scenarios.json v1",
+ │                width_m, height_m,
+ │                spawn_points[6]  { point_id, x, y, heading_rad },
+ │                player_spawn     { x, y, heading_rad, entity_radius },
+ │                placement_extents_m: 8.0,
+ │                positions_provenance: "DECLARED" }
```
- **R-10** `emitter_positions` → `spawn_points[]` with `arena_scenarios.json`'s field vocabulary — D1: this is the third name for a thing the same consumer already reads under two others.
- **R-11** `+width_m, height_m` — the arena footprint is absent entirely; a consumer cannot place six spawn points without knowing what they sit inside.
- **R-12** `placement_extents` → `placement_extents_m` — it is metres and the `_m` suffix is established (`width_m`, `leash_distance_override_m`).
- **R-13** `+arena_schema_kinship` — states the relationship to `arena_scenarios.json` inside the artifact, so the kinship survives past this note.

*(`config.kit` needs no redline — `tick_period_s` / `radius_m` / `weapon_damage_pct` already follow the unit-suffix convention correctly.)*

### `actors[]`

```diff
- ├── actors[]  { actor_id, record_path, display_name, tier(trash|hero|boss|nemesis),
- │              spawn_point, spawn_time, level, hp_max, wave }
+ ├── actors[]  { actor_id, record_path, display_name,
+ │              threat_tier(trash|hero|boss|nemesis), archetype_tag,
+ │              spawn_point_id, spawn_x, spawn_y, spawn_heading_rad, entity_radius_m,
+ │              spawn_t_s, spawn_tick, level, hp_max, wave }
```
- **R-14** `tier` → `threat_tier` — § 0.1 already records that "tier" names three different things in this project; `threat_tier` is the existing serialized name and is unambiguous.
- **R-15** `+archetype_tag` — `arena_scenarios.json` always pairs the two; presentation picks a model from the archetype, not from the threat tier.
- **R-16** `spawn_point` → `spawn_point_id` **plus explicit `spawn_x/spawn_y/spawn_heading_rad`** — AC-11.2 requires reconstructing every actor's spawn time **and position** *from the baton alone*; a point label forces a join through `config.arena`, and a join the consumer can get wrong is not "from the baton alone".
- **R-17** `+entity_radius_m` — the disc predicate is `|e.position − c| ≤ 3.0` centre-to-centre; without a body radius presentation cannot draw a body consistent with the hit test it is forbidden to re-derive.
- **R-18** `spawn_time` → `spawn_t_s` + `spawn_tick` — unit suffix, plus the integer tick that is the exact cross-block key.

### `waves[]`

```diff
- ├── waves[]  { wave, content_tier, reward_tier, t_start, t_end, outcome,
- │             life_modifier_pct, spawn_points_active[], actor_ids[] }
+ ├── waves[]  { wave, content_tier, reward_tier,
+ │             t_start_s, t_end_s, tick_start, tick_end,
+ │             outcome, termination_reason,
+ │             life_modifier_pct, spawn_points_active[], actor_ids[],
+ │             event_row_range: [lo, hi), track_sample_range: [lo, hi) }
```
- **R-19** `t_start/t_end` → `t_start_s`/`t_end_s` + `tick_start`/`tick_end` — unit suffix; and wave boundaries are exactly where a float boundary must not be the key.
- **R-20** `+termination_reason` — `outcome` alone reproduces a known standing telemetry gap in this seam (`termination_reason` missing, per the B14.5 sidecar analyses); a brand-new schema should not inherit it.
- **R-21** `+event_row_range / track_sample_range` — S5: makes per-wave sharding a v1.1 *additive* change instead of a break, and lets a consumer slice wave 160 (the § 10.8 showcase) without loading 8 MB.

### `events[]`

```diff
- ├── events[]  { event_type, t, fight_tick, wave, source_id, target_id,
- │              damage_dealt, damage_type, geometry_type, position }
- │              # event_type ∈ {spawn, tick_damage, dot_tick, death,
- │              #               channel_start, channel_end, energy_dryout,
- │              #               wave_start, wave_end, player_death}
+ ├── events
+ │   ├── columns[]      # declared header — the rows are unreadable without it
+ │   └── rows[][]       # row-array; column order == columns[]
+ │   #  columns = [ event_type, fight_tick, t_s, wave, source_id, target_id,
+ │   #              damage_dealt, damage_source_tag, geometry_type, geometry_family,
+ │   #              x, y, damage_taken, mitigation_source,
+ │   #              resource_cost, resource_gained, mobs_in_range ]
+ │   #  event_type ∈ {spawn, damage_dealt, dot_tick, death,
+ │   #                channel_start, channel_end, energy_dryout,
+ │   #                wave_start, wave_end, player_death}
```
- **R-22** array-of-objects → `{columns[], rows[][]}` — measured **18.06 MB → 7.84 MB** at 80 k events (2.3×); the `columns` header is what keeps it self-describing, and without it I would not propose the shape.
- **R-23** `t` → `t_s`, with `fight_tick` ordered first — the tick is the identity that joins to `fight_events`; `t_s` is derived and rounded, and must never be a key.
- **R-24** `damage_type` → `damage_source_tag` — that is the actual `fight_events` column name (`recorder.py:1005`); a synonym here means the ingest join silently misses.
- **R-25** enum `tick_damage` → `damage_dealt` — `record_fight_events()` branches on `event_type == "damage_dealt"` for its Pattern-P7 geometry guard (`recorder.py:986–991`); a stream saying `tick_damage` ingests with that guard **silently inert**.
- **R-26** `+geometry_family` alongside `geometry_type` — L-16 is Phase-C BINDING: the spin declares its own geometry family and must not reuse the nova (disc↔corridor conflation = 3.076× lethal-area error). `TelegraphSpec.family` with its `VALID_FAMILIES` check already exists (`spatial_telemetry.py:505–511`), and matching on shape alone is the documented silent-blinding failure (`wr2_cell_bat_2026_07_29.py:262`). Carry both or the consumer inherits the bug.
- **R-27** `position{x,y}` → flat `x, y` columns — no `{x,y}` object exists anywhere in this project's serialized surface; entities carry flat `.x`/`.y` and every spawn in `arena_scenarios.json` is flat.
- **R-28** `+damage_taken, mitigation_source, resource_cost, resource_gained, mobs_in_range` — these are `fight_events` columns § 11.4 drops silently, and § 11.3 claims three of them as sim-owned truth (HP track, energy track). Under a row-array a null column costs one byte.

### `tracks`

```diff
- ├── tracks
- │   ├── player_path[]    { t, x, y, facing }
- │   ├── circle_sweep[]   { tick_index, t, centre, radius }
- │   ├── player_hp[]      { t, hp }
- │   └── player_energy[]  { t, energy, energy_max, reserved }
+ ├── tracks
+ │   ├── _sample_stride  { player_path: 1, circle_sweep: 1, player_hp: 1, player_energy: 1 }
+ │   ├── _tick_base      { first_tick, tick_period_s }
+ │   ├── player_path     { tick[], x[], y[], heading_rad[] }
+ │   ├── circle_sweep    { tick[], centre_x[], centre_y[], radius_m[], channel_active[] }
+ │   ├── player_hp       { tick[], hp[], hp_max[] }
+ │   └── player_energy   { tick[], energy[], energy_max[], energy_reserved[] }
```
- **R-29** array-of-objects → columnar (struct-of-arrays) — measured **1.89 MB → 0.51 MB** for `player_path` alone (3.7×); tracks are dense and uniform-shape, the textbook case. Boundary invariant: all channel arrays in one track have equal length.
- **R-30** `+_sample_stride` — S6: the export-side hook that lets drax's sample-rate answer land later **with no schema entry and no MIGRATION break**. v1 ships stride 1 throughout.
- **R-31** `+_tick_base`, and `t` dropped from every track — with a base tick and a stride, `t_s` is exactly derivable; emitting it per sample is ~30 % of track bytes for a value that must equal the derivation anyway. This is arithmetic on an emitted constant, not re-derivation of a sim-owned quantity, so § 11.3's rule is untouched.
- **R-32** `facing` → `heading_rad` — the universal engine and serialized name (`arena.py:179`; every spawn in `arena_scenarios.json`); `facing` appears only in prose comments.
- **R-33** `centre` → `centre_x[]`/`centre_y[]`, `radius` → `radius_m[]` — flat scalars per R-27, `_m` per the unit-suffix rule.
- **R-34** **`+channel_active[]`** — AC-2.1 requires recomputing hit/no-hit **from the emitted telegraph alone**, and a sweep sample with no active flag cannot distinguish "disc positioned here, not channelling" from "disc positioned here, dealing damage". § 11.4 as drafted **fails the G-1h bar it cites in § 2.3**. This is the correctness redline in the set.
- **R-35** `+hp_max[]` — § 11.3 claims HP tracks as sim truth; an HP number with no maximum is not a track a consumer can render.
- **R-36** `reserved` → `energy_reserved` — bare `reserved` collides with the `_reserved` marker convention the same loader already meets at `bundle["encounters"]._reserved` (`one_realm_bundle_assembler.py:1535`).

### Gap, not a redline — `actors`' HP tracks

```diff
+ │   └── actor_hp  { … }   # OR: derive from hp_max + the damage event stream — CONDUCTOR RULING NEEDED
```
- **R-37** § 11.3 claims "**HP tracks (player + every actor)**" as sim-owned truth; § 11.4 emits only the player's. Either the inventory is incomplete or § 11.3 over-claims, and the two must be reconciled before build. Sizing note: a dense per-tick per-actor track is the single largest item in the artifact (17.7 k ticks × ~18 concurrent bodies ≈ 318 k samples, roughly doubling the file). Actor HP is naturally sparse — it changes only on a damage event, and every damage event is already in `events[]`. **Recommendation: emit `hp_max` per actor and declare, in the artifact, that actor HP is reconstructed from `hp_max` minus the event stream.** That is exact, not approximate — but it is a *sanctioned re-derivation of a sim-owned quantity*, which § 11.3 forbids by default. **Conductor ruling, not mine.**

### Provenance (§ 11.5)

```diff
-   u9_closure_state:  CLOSED (1.9% intra-order residual declared;
-                              U9-6 bonus-spawn state = <resolved|UNKNOWN, +-8.4% branch>)
+   u9_closure_state:            CLOSED
+   u9_intra_order_residual_pct: 1.9
+   u9_bonus_spawn_state:        resolved | UNKNOWN
+   u9_bonus_spawn_branch_pct:   8.4
-   declarations: [ "G-5: …", "arena emitter positions are DECLARED …", … ]
+   declarations: [ { id: "G-5", text: "…" }, { id: "D-ARENA-DECLARED", text: "…" }, … ]
+   out_of_model: [ { id: …, text: … } ]
```
- **R-38** split `u9_closure_state` into typed fields — the bonus-spawn fact is **already typed** as `config.encounter.bonus_spawn_p06: <bool|"UNKNOWN">`; one fact in two encodings is how the two drift. Add a write-boundary assert that they agree.
- **R-39** `declarations` and `out_of_model` → `{id, text}` — AC-11.4 ("no declaration dropped") is an eyeball check against prose and a set comparison against IDs. Five of the nine declarations currently have no ID.

---

## Named questions for the conductor

1. **R-37 (actor HP)** — dense per-actor track, or sanctioned exact re-derivation from `hp_max` + events? § 11.3 and § 11.4 disagree today; this is also the largest single size lever left.
2. **D1 resolution** — (a) promote the Crucible arena into `ALL_SCENARIOS` and single-source geometry, or (b) embed it in the baton using `arena_scenarios.json` vocabulary + `arena_schema_kinship`. I recommend (b); (a) touches gamora's `arena.py`.
3. **M2 / ADR-006** — does the emitter register the run in `emission_registry.db`? If yes, that is a Matt-authorized external write and the MIGRATION entry must say so.
4. **S4 (gzip)** — a ~10× lever, but it is a loader change on drax's side. **Route to drax's consult as yes/no.** Not assumed here.
5. **Validation-style divergence** — Pydantic (season lane) vs assert-based `_validate_payload` (`arena_scenario_emitter`, the Godot lane). I recommend Pydantic and a MIGRATION line stating the divergence.

## What is already testable with existing machinery

- **AC-11.5** (baton never occupies `encounters`) is testable today as an absence: `validate_bundle()` (`one_realm_bundle_assembler.py:1270–1276`) already requires `encounters` be a dict, and the reserved marker at `:1531–1544` is what belongs there. A test asserting the marker is byte-unchanged after a baton emit is a two-line pin. The namespace guard is live in code, exactly as ledger § A.1 recorded.
- **AC-11.1** is the `_write_json`-equivalent boundary and follows the `save_sim_cycling_quality_report` / `load_sim_cycling_quality_report` round-trip pattern (`season_exporter.py:970–994`) — write via `model_dump()`, reload via `model_validate()`, assert model equality. That pattern is the right skeleton for the baton's round-trip smoke.
