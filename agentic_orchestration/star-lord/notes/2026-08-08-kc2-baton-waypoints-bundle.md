# KC2-SIM — the BATON WAYPOINTS BUNDLE

**Author:** star-lord (export / output / telemetry / llm seam)
**Date:** 2026-08-08 · KC2-SIM autonomous run, conductor gandalf, Phase D
**Authority:** **R-L48-4** (Option-1 waypoints, veto-open) · **R-LOCO-1** / **R-LOCO-2**
(`gandalf/notes/2026-08-08-kc2-locomotion-spec-amendment.md` § 6) · jack-ryan
`2026-08-08-kc2-gate2-d2-1-reverdict.md` findings **R-1** (WARN, ADR-002 test tier — approved),
**R-2** (WARN), **R-4** (INFO) · spec § 2.3, § 10.6, § 10.9a A/B, § 11.3, § 11.4
**Engine state:** working tree, **NOT committed** — see § 5. **NOT pushed** under any condition.
**Status of this note:** UNCOMMITTED meta-repo note; the conductor folds it.

---

## 0 — Headline

Six items, one seam touch, all six discharged. **86 baton tests** (was 51), **32 addressable
validator checks** (was 28), **33 consumer-stub items** (was 31), all green.

Three things the conductor should read even if nothing else:

1. **⚑ A MEASURED FINDING THAT IS NOT MINE TO RESOLVE.** The spec's "10-member cited enumeration"
   (§ 10.9a B) is a **map-name** enumeration and it **UNDER-DETERMINES the geometry**. The cited
   table holds **16 (archive, map) pairs over 10 map names**; six names appear in both `sm1` and
   `sm_mod` with different placements. On `survivalworld_f` — the arena gamora's in-flight
   `locomotion.ARENA_SELECTION` DECLARES for s1 — p06 reads **29.73 m (sm1) vs 40.35 m (sm_mod),
   36 % apart**. The schema now REQUIRES `arena_archive`; the enumeration itself is § 6 item 1.
2. **⚑ THE RULING'S COST PREMISE MISSES ~10×, MEASURED.** R-L48-4 chose Option 1 over per-tick
   tracks partly on *"~tens of bytes per actor"*. Under the shipping `rows-compact` default it
   measures **357 B/actor**. Still only 3.2 % of a 17.4 MB artifact and inside drax's ≈ 22 MB
   budget, so the ruling holds — but the premise is corrected, not absorbed (§ 3, the S-I2
   precedent).
3. **⚑ CENSUS CONFOUND, MEASURED AND SEPARATED.** gamora's locomotion lap landed **uncommitted in
   the shared tree during my session**. It fails 10 tests in two files outside the L-39 census.
   Attribution measured by stash-probe, not asserted (§ 4). Not mine.

---

## 1 — Per-item disposition

| # | Item | Disposition |
|---|---|---|
| **1** | R-LOCO-1 / R-L48-4 — Option-1 waypoints + `path_model`; G-1h law re-worded for motion | **LANDED** — with one named strengthening (§ 2.1) |
| **2** | `arena_ref` sibling + six radii + two-layer `positions_provenance` | **LANDED** — one breaking retype; `arena_archive` added on a measurement |
| **3** | R-LOCO-2 — AC-11.4b re-sync `D-ARENA-DECLARED` → `D-ARENA-CITED` | **LANDED** — id renamed, text rewritten with inline strike lineage |
| **4** | R-4 TYPE rider — str-side MAPPING widening **and** bool-side TYPE gap | **LANDED, both** — mapping is now DATA; bool side is an additive GRADE sibling |
| **5** | R-1 — pin the EMITTED p06 defaults against L-37(b) | **LANDED, twice over** — value pin **plus** a boundary guard (§ 2.4) |
| **6** | R-2 — `baton_v1_fixture.py:362` hardcoded `run_p06_enabled = True` | **LANDED** — fixed by **wiring**, not by re-typing the literal |

### The reconstruction law, re-worded for motion (item 1's prose obligation)

> **The baton records the ONE REALIZED trajectory per actor. The Godot session REPLAYS it and never
> re-simulates.**

§ 2.3's *"hit/no-hit is a function of two trajectories"* describes the **SIM's branch point** — it
is not a licence for the consumer to explore both. The baton emits the branch that happened. This
sentence is now carried in three places that a reader actually reaches: the schema module header,
`config.arena.path_interpolation` (**inside the artifact**), and the MIGRATION entry.

---

## 2 — SCHEMA-DELTA (for drax counter-sign)

**Two rows change a loader. Everything else is additive.** Byte costs are measured on the fixture
under the shipping `rows-compact` default, then projected at ≈ 1,580 actors (≈ 17 bodies/wave ×
93 waves) against § 11.6.1's measured 17.4 MB artifact.

### 2.1 `actors[]`

| field | change | type | byte cost | breaks a loader? |
|---|---|---|---|---|
| `path[]` | **ADDED** | `list[{run_tick:int, t_s:float, x:float, y:float}]`, default `[]` | **357 B/actor** (3 knots) → ≈ 560 KB / **3.2 %** | **no** (additive) |

**⚑ ONE DELIBERATE DEVIATION from the routed `{t_s, x, y}` shape — the waypoint also carries
`run_tick`.** § 11.4 **pin 4** rules that `t_s` is derived and **NEVER a key**, and the waypoint's
entire job is to join against `circle_sweep`, which is keyed on `tick`. A list keyed only on `t_s`
would route the G-1h reconstruction through a float equality across a JSON round-trip — the exact
failure pin 4 exists to forbid. Every event row already carries the same pair for the same reason.
Cost ≈ 8 B/waypoint. **Named as a judgment call; strike it if the conductor disagrees.**

### 2.2 `config.arena`

| field | change | type | breaks a loader? |
|---|---|---|---|
| `arena_id` | **RE-WORDED ONLY** — names the **SITTING**, not the arena | `"s1" \| "s2"` — unchanged | no |
| `arena_ref` | **ADDED — REQUIRED** by `G-ARENA-REF` (may be honestly `UNDISCRIMINATED`) | object, ≈ 500 B **once per baton** | **YES — must be emitted** |
| `positions_provenance` | **RETYPED** | `str` → `{emitter_geometry, arena_selection, ruling}` | **YES — the one breaking change** |
| `path_model` | **ADDED** | `Literal["PIECEWISE-LINEAR"]`, defaulted | no |
| `path_interpolation` | **ADDED** | `str`, defaulted — the rule ships IN the artifact | no |
| `path_coverage` | **ADDED** | `str`, defaulted — what the span covers, and where position is UNDEFINED | no |
| `path_target_policy` | **ADDED** | `"L-A-ZONE-FIRST" \| "L-B-GATE-FIRST" \| null` (§ 10.9a A) | no |
| `path_node_assignment_rule` | **ADDED** | `"nearest-node" \| "group-centroid" \| "per-emitter" \| null` **[R-LOCO-6]** | no |
| `v_ref` | **ADDED** | `float \| null` — the SOLE free locomotion scalar (§ 10.9a B/D; charter § 4.2) | no |
| `d_engage_m` | **ADDED** | `float \| null` — `meleeTargetDistance` 2.4 … `meleeAutoTargetDistance` 4.0 | no |

`arena_ref` = `{arena_key, arena_archive, arena_tag, selection_grade, selection_note, enumeration,
enumeration_source, emitter_radii, geometry_source, geometry_sha256, reference_frame}`;
`emitter_radii` = `{p01_m … p06_m, p01_tier_key, grade: "CITED-PER-ARENA" | "SYNTHETIC"}`.

**Why `positions_provenance` was retyped rather than re-valued.** § 11.4 already marks the flat
scalar **⚠ OPERATIVE-FALSE post-L-46**: it is wrong at layer 1 (positions are **CITED**; only the
SELECTION is DECLARED). A false provenance claim inside a provenance block is the one defect this
artifact exists to prevent. A longer *string* would have kept two machine-relevant values in prose,
which § 11.5 **[R-38]** forbids by the schema's own law. **Back-compat cost is zero: `find . -name
"*baton*.json*"` → 0 artifacts, and there is no `baton/v1` loader in any drax repo** (the "baton"
hits in `reincarnated-godot/scripts/*.gd` are the WR1/WR2 grading-synthesis batons — a different
artifact entirely).

**Why `arena_archive` is required and not cosmetic — MEASURED:**

| (archive, map) | p05 | p06 |
|---|---:|---:|
| `sm1/survivalworld_f` | 13.82 | **29.73** |
| `sm_mod/survivalworld_f` | 10.96 | **40.35** |

Six of ten map names appear in two archives. A baton naming only the map pins an emitter ring a
third wrong — **F-12a wearing a citation**. `split_arena_ref()` is the one named adapter for the sim
seam's composite `"sm_mod/survivalworld_f.map"`, so neither side grows its own parser.

### 2.3 `config.encounter`

| field | change | type | breaks a loader? |
|---|---|---|---|
| `fixture_p06_state` | **unchanged** (`False`) | `bool` | no — drax's M-1 `isinstance(..., bool)` stays green |
| `fixture_p06_state_grade` | **ADDED** [R-4 bool side] | `"RULED-OFF" \| "MEASURED-OFF" \| "MEASURED-ON" \| "DEMOTED-OPEN" \| "UNKNOWN"`, default `"RULED-OFF"` | no |
| `run_p06_enabled` | **unchanged in schema**; the fixture SUPPLIER fixed [R-2] | `bool` | no |

**Why the bool side landed as a grade sibling rather than a retype.** What `bool` cannot express is
not a third **value** — p06 was either on or off — it is the **grade of the claim**: *"ruled off, by
adoption of an s2-measured limb over an s1 sitting that was never separately measured"*
(`calibration.S1_P06_PROVENANCE` says exactly that). `False` is the correct value; `RULED-OFF` is
the correct grade. This is CD-2's own pattern (`engine_tree_state` + `tree_state_policy`) and it
keeps AC-11.4g's pairing rule computable.

*One asymmetry, stated because it looks inconsistent otherwise:* `tree_state_policy` defaults to
`None`, this one defaults to the ruled member. `tree_state_policy` describes **what the emitter
did**, so back-filling it would invent a measurement; `fixture_p06_state_grade` describes **a fact
about the fixture**, whose state of record IS the ruling — so the do-nothing state *should* be the
ruled state. That is precisely the property R-1 found unpinned, and it is now pinned by a test.

### 2.4 `provenance`

| field | change | breaks a loader? |
|---|---|---|
| `u9_bonus_spawn_state` | **DEFAULT MOVED** `"UNKNOWN"` → `"RULED-OFF"`; type unchanged; `"UNKNOWN"` still admitted | no |
| `declarations[]` | **ID RENAMED** `D-ARENA-DECLARED` → **`D-ARENA-CITED`**, text rewritten with inline strike lineage | **yes if you match on the id** |

The retired id is kept NAMED in `DECLARATION_IDS_RETIRED`, so an old wire is told *what happened*
rather than getting a bare `unexpected ['D-ARENA-DECLARED']`. It is **struck, not aliased** — an
alias would let the false claim keep validating.

### 2.5 New addressable checks (28 → 32) and stub items (31 → 33)

| id | what it enforces |
|---|---|
| `G-P06-GRADE` | grade ↔ value ↔ state cross-consistency. **This is the guard R-1 found missing.** |
| `G-ARENA-REF` | two-layer provenance · `arena_ref` present · archive required · enumeration intact · F-12a radii invariant · citation backed by sha256 |
| `G-LOCO-PATH` | `path_model` named · spawn-anchored · strictly ordered · `t_s` derived · span reaches `engage_tick` · **empty path FAILS** |
| `G-LOCO-ONE-TRAJECTORY` | the path and the event rows are ONE trajectory; **refuses to pass vacuously** if it inspected nothing |
| `R-LOCO-1` (stub) | every actor's trajectory is replayable from the baton alone |
| `R-LOCO-1-HITTEST` (stub) | **hit AND no-hit** re-decided from the two emitted trajectories — the G-1h bar under motion |

---

## 3 — MEASURED: the waypoint cost, against the ruling's own premise

R-L48-4 chose Option 1 over per-tick tracks partly on cost; the routed lean read *"~tens of bytes
per actor"*. Measured on the fixture (13 actors, 39 waypoints):

| style | Δ B/waypoint | Δ B/actor | full doc |
|---|---:|---:|---:|
| **`rows-compact` (shipping default)** | **119** | **357** | 147,463 |
| `compact` | 51 | 152 | 135,744 |
| `indent` | 119 | 357 | 291,807 |

**Cause:** `rows-compact` collapses leaf arrays of **scalars** onto one line (that is what makes an
event row readable under its header); a waypoint list is an array of **objects**, so it does not
collapse. Projected: **≈ 560 KB, 3.2 % of the measured 17.4 MB artifact**, consuming ~12 % of the
headroom under drax's ≈ 22 MB budget. **The ruling holds on cost. Its stated premise does not, by
~10×, and is corrected here rather than absorbed** (Discipline #10; the S-I2 precedent where the
derived 9–12 MB was superseded by a measured 17.4 MB).

**A mitigation exists and is DELIBERATELY NOT TAKEN.** Extending the leaf collapse to arrays of
**flat objects** measures **186 B/actor (−48 %) and 2.3 % document-wide**, and round-trips to the
identical object (verified). I did not take it because `rows-compact` is a **signed** write-discipline
corrigendum (L-31/CD-1) and this bundle already carries one breaking retype — *one bundle, one signed
surface*. **Routed with its number attached; one line reverses it.**

---

## 4 — Test evidence, by path

All paths absolute.

| evidence | where |
|---|---|
| schema | `/Users/admin/Games/reincarnated-engine/src/reincarnated/export/baton_v1_schema.py` |
| validator (+4 checks) | `/Users/admin/Games/reincarnated-engine/src/reincarnated/export/baton_v1_validator.py` |
| emitter (structural spawn anchor + derived waypoint clock) | `/Users/admin/Games/reincarnated-engine/src/reincarnated/export/baton_v1_emitter.py` |
| fixture (**the board now moves**) | `/Users/admin/Games/reincarnated-engine/src/reincarnated/export/baton_v1_fixture.py` |
| consumer stub (+2 items, `Scene.actor_position`) | `/Users/admin/Games/reincarnated-engine/src/reincarnated/export/baton_v1_stub_consumer.py` |
| tests **51 → 86** | `/Users/admin/Games/reincarnated-engine/tests/test_baton_v1.py` |
| MIGRATION entry (ADR-004, drax counter-sign block at the top) | `/Users/admin/Games/reincarnated-engine/src/reincarnated/export/MIGRATION.md` |
| checkpoint | `/Users/admin/Games/reincarnated-engine/src/reincarnated/export/AGENT_STATE.md` |

### 4.1 The fixture's board moves — and that is what makes the evidence real

`make_synthetic_run_record()` now walks each actor **spawn → patrol node → engage**, computes its
position at any tick by interpolating **its own emitted path**, and runs the § 2.1 predicate against
that position instead of the proxy *"is it engaged?"*. Measured on the emitted wire:

- **13/13 actors change position** (a static board reads 0)
- **39 waypoints**, 2–3 knots/actor — the interior knot exercises multi-segment interpolation
- **11 `damage_dealt` rows on 6 distinct actors land BEFORE their engage tick** — AC-10.8's shape
- `G-LOCO-ONE-TRAJECTORY` inspects **46 rows**; `R-LOCO-1-HITTEST` re-decides **156 (actor, tick)
  pairs**, 0 missed hits, 0 phantom hits, 0 on the rim
- event rows 409 → **428**; every pre-existing spawn coordinate **byte-identical** (the locomotion
  draws use a separate RNG stream, deliberately, so this bundle's diff stays readable)

Three independent implementations of the interpolation now exist — fixture (producer), validator
(checker), stub (consumer) — and that is on purpose: one shared function would make the guards agree
with themselves by construction, the same reason the stub re-implements the hit test.

### 4.2 Negative controls — 14 run, every guard has teeth

| perturbation | fires |
|---|---|
| interior waypoint bent 0.5 m | `G-LOCO-ONE-TRAJECTORY` |
| empty `path` | `G-LOCO-PATH` |
| out-of-order waypoints | `G-LOCO-PATH` |
| `path[0]` ≠ spawn (position or tick) | **refused at `build_baton`**, not merely flagged |
| retired flat `"DECLARED"` scalar | `G-ARENA-REF` (+ `AC-11.1`), named as retired |
| prose two-layer string (**what the sim seam emits today**) | `G-ARENA-REF`, names the object to emit |
| `arena_ref` absent | `G-ARENA-REF` |
| `arena_key` set, `arena_archive` null | `G-ARENA-REF`, with the 36 % measurement in the message |
| unsplit composite `"sm_mod/survivalworld_f.map"` | `G-ARENA-REF`, points at `split_arena_ref` |
| one radius for six emitters / ambush outside ring | `G-ARENA-REF` |
| SYNTHETIC radii claiming `CITED-PER-ARENA` | `G-ARENA-REF` (sha256-backed) |
| `D-ARENA-DECLARED` on the wire | `AC-11.4b` + `AC-11.4d`, **with lineage** |
| **two-sided p06 revert `(True, "RESOLVED")`** | **`G-P06-GRADE`** — R-1's exact case |
| grade absent | `G-P06-GRADE` |
| `(False, "RULED-OFF")` | **accepted** — R-4's str-side ask, now round-trips |
| **every path frozen at spawn = the F-12 defect verbatim** | **`R-LOCO-1` + `R-LOCO-1-HITTEST` go RED** (20 phantom hits) |

### 4.3 ⚑ The best thing in this bundle is a test that failed

The F-12 static-board negative control went **GREEN** on first run. The `R-LOCO-1` stub item
computed the moved-count, printed *"0 actually change position"* **in its evidence string** — and
graded on structure alone. **A number a reader has to notice is not a check.** Moved into the
predicate (as a `still` count, so a legitimate spawn-and-die body with a degenerate span is not
punished); the control now goes RED. I would not have found this by inspection — it took writing the
control that was supposed to fail.

---

## 5 — Census vs the L-39 baseline

**Bar:** 63F / 10,277P / 21E, 12 named failure files + 1 error file; **zero NOVEL failure files**
(jack-ryan re-reproduced this at `cbb29e68`).

> **⚑ CONFOUND, NAMED FIRST.** The tracked tree was **clean at my session start**. During the
> session **gamora's locomotion lap landed uncommitted in the shared working tree** — 4 modified
> tracked modules (`calibration.py`, `micro_oracles.py`, `run.py`, `wave_engine.py`) plus untracked
> `locomotion.py`, which `wave_engine.py:41` now imports. The census below therefore measures **two
> agents' work at once**, and I separated them by measurement rather than by assertion.

### 5.1 Attribution probe (measured, Discipline #10)

`git stash push -- src/reincarnated/export/ tests/test_baton_v1.py` (my files ONLY; gamora's
untouched), then re-run:

```
WITHOUT my change: 10 failed, 60 passed
  tests/test_kc2_s1_ramp.py                 9
  tests/test_kc2_opposition_wave_engine.py  1
```

**All 10 reproduce with my change removed.** Corroborated structurally: neither file imports
anything under `export/` or any `baton` module, so no import path exists by which my diff could
reach them. Stash popped; 86/86 baton tests green after restore.

### 5.2 Per-file census — `python3 -m pytest tests/ -q`, 11:38 → 12:00 (21:55)

```
76 failed, 10299 passed, 3 warnings, 21 errors in 1315.41s (0:21:55)   EXIT=1
```

| file | mine | L-39 | class |
|---|---:|---:|---|
| `test_cycle12_layer4_convergence.py` | 33 | 33 | ✅ tree |
| `test_cycle12_layer6_t4_wireup.py` | 12 | 12 | ✅ tree |
| `test_foundation.py` | 4 | 4 | ✅ tree |
| `test_substrate_identity_loader.py` | 2 | 2 | ✅ tree |
| `test_wave5_swift_closure_path_x…` | 1 | 1 | ✅ tree |
| `test_no_canonical_four_in_llm_prompts.py` | 1 | 1 | ✅ tree |
| `test_kit_space_skill_naming.py` | 1 | 1 | ✅ tree |
| `test_dispatch_3b_phase5_seam1_pm1_gb.py` | 1 | 1 | ✅ tree |
| `test_cycle13_normal_season_export.py` | 1 | 1 | ✅ tree |
| `test_kit_space_emitter.py` | 4 | 4 | ✅ baseline |
| `test_wr2_d_nova_telegraph.py` | 2 | 2 | ✅ baseline |
| `test_wr1_m12_gd_mitigation_nova.py` | 1 | 1 | ✅ baseline |
| **subtotal — L-39's 12 named files** | **63** | **63** | **EXACT, file by file** |
| `test_kc2_s1_ramp.py` | 9 | 0 | ⚠ NOVEL — gamora |
| `test_kc2_micro_oracles.py` | 2 | 0 | ⚠ NOVEL — gamora |
| `test_kitcal_g5_harness.py` | 1 | 0 | ⚠ NOVEL — tree-state |
| `test_kc2_opposition_wave_engine.py` | 1 | 0 | ⚠ NOVEL — gamora |
| **total failed** | **76** | 63 | 63 accounted + 13 novel |
| `test_cycle13_wave5_season_generation.py` (errors) | 21 | 21 | ✅ env |

**Every one of L-39's twelve named failure files is at its identical count. The error file is
identical. All 13 novel failures sit in four files in gamora's seam, and none of them imports
anything under `export/` or any `baton` module.**

**Collection arithmetic closes exactly:** 76 + 10,299 + 21 = **10,396** = jack-ryan's 10,361 at
`cbb29e68` **+ 35**, and +35 is precisely my baton test additions (51 → 86). gamora added **zero**
tests; her novel failures are pre-existing tests failing against her in-flight modules.

**Second, independent confirmation — the tree moved under the census.** A repeat of the same
stash-probe at 12:03 returned a *different* failure set (1 instead of 10). `stat` shows
`calibration.py` 12:02:42, `run.py` 12:01:30, `wave_engine.py` 12:01:18 — **gamora edited three
modules during and after my census run**. Failures that track her mtimes and not my diff are hers.

### 5.3 Verdict, and why I did NOT commit

**Zero novel failure files attributable to this bundle**, proven twice (stash-probe + import-graph)
and corroborated by the collection arithmetic. My seam is green: 86/86 baton, 32/32 validator
checks, 33/33 stub items, disk round-trip green.

**I still did not commit, and the reason is my own discipline pointed at me.** A commit made now
would be measured against a working tree that carries **another agent's uncommitted work-in-flight**,
and its message would have to claim a census that no longer describes the tree it lands on. That is
a **clean grade stamped on an edited tree** — the exact false-provenance failure `AC-11.4e` /
CD-2 / `engine_tree_state` exist in this very schema to prevent. Committing would have been me doing
the thing my own boundary refuses to let anyone else do.

The dispatch also gives the branch explicitly: *"otherwise working tree + report."* Taking it costs
one message from the conductor; the alternative costs a false claim in the permanent log.

**State handed over:** 8 files modified, all in-seam (`src/reincarnated/export/` ×7 +
`tests/test_baton_v1.py`), **+1,720 / −36**. Nothing of gamora's touched. Safety copies at
`/tmp/starlord-kc2-baton/mine-final.patch` (2,087 lines) and the full census transcript at
`/tmp/starlord-kc2-baton/census-11-38-to-12-00.txt`.

**To land it:** one word from the conductor. The commit is one `git add` over those 8 paths — the
message is drafted in § 7.

---

## 6 — Handed back to the conductor

| # | Item | Why it is not mine |
|---|---|---|
| **1** | **The cited arena enumeration is a MAP-NAME enumeration and under-determines the geometry** (16 archive×map pairs over 10 names; 36 % divergence on the very arena declared for s1). The schema now requires `arena_archive`; whether § 10.9a B's enumeration should be re-stated as 16 pairs is a **spec** call. | spec text is the conductor's |
| **2** | **`path_model`'s home.** Landed at `config.arena` because the routed Option-1 text puts it there verbatim and `collision_model` — the adjacent motion declaration — already lives there. `config.model` is the arguable alternative. Named, not taken. | § 11 is signed |
| **3** | **The `rows-compact` mitigation** (357 → 186 B/actor, 2.3 % doc-wide, round-trip identical). Not taken: `rows-compact` is a signed corrigendum (L-31/CD-1). | signed write discipline |
| **4** | **The sim seam emits shapes this schema now rejects** — `locomotion.locomotion_provenance()` returns `arena_ref` as a flat composite string and `positions_provenance` as prose. Both are caught with actionable messages and `split_arena_ref()` is the named adapter, **but gamora's lap is uncommitted and I did not touch her seam.** Needs a cross-seam note. | gamora's seam |
| **5** | **`G-` ids vs `AC-11.4x` ids.** Four new checks carry `G-` per the CD-2 precedent — the conductor lands the § 11 rows. Renaming is one line each. | § 11 row-landing |
| **6** | **Proposed spec-text deltas** for § 11.4 (I did NOT edit the spec): strike the `positions_provenance: "DECLARED"` ⚠ line → the typed object; annotate `arena_id` as the SITTING; add the `arena_ref` / `actors[].path[]` / `path_*` rows; strike pin 12's TYPE-GAP clause as LANDED; re-word § 11.4's `D-ARENA-DECLARED` → `D-ARENA-CITED`. | spec is the conductor's |

**Still open from Gate-2 Phase-D2, NOT self-assigned** (per the flagged-but-not-dispatched rule —
these want a knight-rider dispatch, not my initiative): **D2-6** (widen the CD-2 count check),
**D2-12** (retag `baton_v1_fixture.py:61`'s POOLED bearing list — I tagged my *own* new synthetic
data with a `SYNTHETIC` grade so as not to repeat it, but did not touch line 61), **D2-13**
(section-scoped digest in the golden sidecar).

---

## 7 — Commit / push posture, and the drafted commit

- **Push: NOT DONE, not requested, not attempted.** Engine sits at 15 unpushed through `cbb29e68`
  by design; Matt's word gates push.
- **Commit: NOT MADE** — reason in § 5.3. Working tree, 8 in-seam files, +1,720 / −36.
- This note is **uncommitted** in the meta-repo; the conductor folds it.

**Drafted, ready to fire on one word** (paths are exactly the 8 in-seam files; nothing of gamora's):

```
git add src/reincarnated/export/baton_v1_schema.py \
        src/reincarnated/export/baton_v1_validator.py \
        src/reincarnated/export/baton_v1_emitter.py \
        src/reincarnated/export/baton_v1_fixture.py \
        src/reincarnated/export/baton_v1_stub_consumer.py \
        src/reincarnated/export/MIGRATION.md \
        src/reincarnated/export/AGENT_STATE.md \
        tests/test_baton_v1.py
```

> **star-lord: baton/v1 waypoints — the board MOVES, and the arena stops claiming its geometry is a
> free parameter**
>
> R-L48-4 / R-LOCO-1 Option-1 waypoints (`actors[].path[]` + `path_model`), `arena_ref` over the
> cited enumeration + six radii, `positions_provenance` retyped to the two-layer object,
> R-LOCO-2's `D-ARENA-DECLARED` → `D-ARENA-CITED`, and R-4's rider landed on BOTH sides (str-side
> mapping widening + bool-side grade sibling). R-1's unpinned default is now pinned at the wire AND
> guarded at the boundary, so the two-sided revert fires. R-2's supplier is WIRED to the sim of
> record, not re-typed.
>
> Measured, not assumed: the map name under-determines the geometry by 36 % on the very arena
> declared for s1, so `arena_archive` is required; the waypoint cost is 357 B/actor against a
> routed premise of "tens", reported rather than absorbed.
>
> 86 baton tests (was 51) · 32 validator checks (was 28) · 33 stub items (was 31). The fixture's
> board moves and 11 damage rows land before engage, so the guards bite on motion rather than on
> endpoints.
