# Field spec — `recompose_energy_calibration_applied` (A4 / v2.15 ALTER TABLE)

**STATUS:** CURRENT (spec deliverable; consumed by star-lord v2.15 migration)
**Date:** 2026-06-14
**Author:** gamora (simulation + balance-loop seam)
**Authority:** A4 dispatch `agentic_orchestration/dispatches/2026-06-14-star-lord-gamora-a4-v2-15-alter-table.md`; W0.1 math note §8 (originating spec); W0.2 math note §8.4 (co-migration mandate); gandalf §7.6 BC-cutover ruling
**Companion:** `~/Games/reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` v1.24 (already filed); `~/Games/reincarnated-engine/src/reincarnated/simulation/math/w0-1-b14-5-v2-energy-type-lever.md` §8
**Scope:** SPEC ONLY. star-lord authors the ALTER TABLE. No balance-loop / AI logic touched (Stage 2 is a separate dispatch).

---

## 0. Disposition — this is execution of a deferred obligation, not new design

The `recompose_energy_calibration_applied` field is ALREADY implemented in `balance_loop.py` (W0.1, 2026-05-20, MIGRATION.md v1.24). The producer side has been live since W0.1; only the schema column was deferred. This dispatch finally lands the column. So this spec is a **confirmation + table-placement note**, not a fresh design. The field semantics below are read off the existing code, not invented here.

The one decision genuinely open at A4 (per dispatch §"Open questions"): **default value (false vs null) and backfill disposition for historical rows.** That is resolved in §3 and §4 below.

---

## 1. Field spec (the four bullets)

| Property | Value |
|---|---|
| **Column name** | `recompose_energy_calibration_applied` |
| **SQL type** | `INTEGER` (boolean stored as 0/1 per SQLite convention; the field is tri-state — see §2) |
| **Nullable** | `YES` (nullable required — the producer emits `None` legitimately, not just as an absence-of-data sentinel) |
| **Default** | `NULL` (NOT `0`/false — justified §3) |
| **Set true at** | `balance_loop.py:2482` (`accepted = delta > RECOMPOSE_DELTA_FLOOR`) → surfaced into the attempt dict at `:2492`, then aggregated to the class-level result at `:1383-1388` and written to `balance_metadata` at `:1415` / the `ClassBalanceResult` dataclass field at `:718` |
| **Historical rows** | Stay `NULL`. No backfill. (justified §4) |

---

## 2. Tri-state semantics — load-bearing; the column is NOT a plain boolean

The field is typed `bool | None` (`balance_loop.py:718`, `:1381`). The three states each carry distinct meaning. star-lord's column MUST preserve all three; collapsing `None` into `0` would be a silent semantic shift (Discipline #12).

| Value | Stored | Meaning |
|---|---|---|
| `True` | `1` | Sub-lever B (`energy_type_calibration`) fired AND was accepted for this class — i.e. an energy-type class (rage / combo / stamina-as-resource) was confirmed miss-suppressed and the probe-WR rose by > `RECOMPOSE_DELTA_FLOOR`. Set at `:2482`/`:2492`; aggregated at `:1383`. |
| `False` | `0` | Recompose ran but energy calibration was NOT accepted — either the energy type is not in `ENERGY_TYPE_LEVER_PHYSICAL_TYPES` (mana classes always land here, `:2455-2460`), or the lever evaluated but the probe delta did not clear the floor. |
| `None` | `NULL` | Recompose was SKIPPED entirely — `recompose_attempts` is empty (`:1382`). This is the experimental-class case (recompose loop does not run). It is a genuine "not applicable," distinct from "ran and was false." |

Aggregation rule at the class level (`:1383-1388`): `True` iff ANY recompose attempt has `recompose_energy_calibration_applied=True` AND `accepted=True` AND `lever=="energy_type_calibration"`. The `lever==` predicate matters — the flat `"recompose_energy_calibration_applied": False` key is stamped on ALL standard lever attempt dicts (`:1803`) for always-present telemetry, so the aggregation must filter to the calibration lever specifically.

**Consumer implication:** any star-lord recorder or jack-ryan query that treats this as a 2-valued boolean will mis-bucket experimental classes (`NULL`) as `False`. The correct read is 3-valued: `1` = calibration confirmed; `0` = recompose ran, not applied; `NULL` = recompose did not run / pre-W0.1 row.

---

## 3. Default value — `NULL`, not `0`/false (justified)

**Decision: column default `NULL`.**

Reasoning:
1. **`None` is a real producer output, not an absence sentinel.** The balance loop legitimately emits `None` for experimental classes (recompose skipped). If the column defaulted to `0`/false, an experimental-class row that for any reason failed to write the field explicitly would be indistinguishable from a "recompose ran, not applied" row. `NULL` default keeps the "no value written" case aligned with the "not applicable" semantic, which is the closest-correct fallback.
2. **Consistency with sibling tri-state columns.** `modifier_extreme_low` (v2.12), `floor_lock_recompose` (v2.13) are all `bool | None` nullable columns where `None` = "pre-feature / not-applicable" and the schema column is nullable with no false-default. `recompose_energy_calibration_applied` is the same shape (`:704`, `:712`, `:718` are three adjacent fields with identical tri-state handling). Defaulting this one to `0` while its siblings default `NULL` would create an inconsistent read surface across the three lever-provenance columns.
3. **Post-W0.1 engine rows always write the field explicitly** (`True`/`False`/`None`), so the default is only ever exercised by (a) pre-W0.1 historical rows and (b) any malformed write — and for both, `NULL` ("unknown / not applicable") is the honest value. A `0` default would assert "calibration definitely did not apply" about rows where we simply do not know.

The W0.1 MIGRATION.md v1.24 already specified `-- NULL for pre-W0.1 rows` (`MIGRATION.md:6651`). This spec confirms that disposition.

---

## 4. Historical rows — stay `NULL`, no backfill (justified)

**Decision: NO backfill. Pre-v2.15 / pre-W0.1 rows stay `NULL`.**

Reasoning:
1. **The flag cannot be reconstructed from stored data.** `recompose_energy_calibration_applied=True` is the outcome of a probe-WR re-evaluation against `RECOMPOSE_DELTA_FLOOR` at balance time (`:2473-2482`). That probe WR was never persisted as a standalone column; it only ever existed inside the recompose-attempt evaluation. There is no source column to derive a backfill value from — any backfill would be a fabricated value.
2. **`NULL` is already the correct semantic for these rows.** Pre-W0.1 rows were produced by an engine that did not run sub-lever B at all. That is exactly the "recompose calibration not applicable to this row" case `NULL` denotes. Backfilling to `0` would falsely assert the lever ran and declined; `NULL` correctly says "this engine version had no such lever."
3. **No consumer requires backfill.** The only consumers of this field (the recompose-loop diagnostics, jack-ryan provenance queries) are forward-looking — they analyze W0.1+ energy-type-class behavior. Historical comparisons across the W0.1 boundary already partition on engine_version; pre-W0.1 rows are not pooled with post-W0.1 rows for this field.

---

## 5. Consumer-read implications for the recompose loops

1. **No new read on the recompose loop itself.** The balance loop is the PRODUCER of this field; it does not read the persisted column back during convergence. The v2.15 column adds a persistence sink, not a new input to the loop. Confirming the out-of-scope boundary: this dispatch does not change any balance-loop read path.
2. **Recorder boundary (star-lord seam) — P7 WARN on absent key.** Per W0.1 §8 / MIGRATION.md v1.24 (`:6657`): post-W0.1 engine attempt dicts ALWAYS carry the key (`True`/`False`, never absent — see `:1803`, `:1845`, `:2459`, `:2492`). The recorder should P7-WARN if the key is absent in a post-W0.1 row (signals a producer regression), but accept `None`→`NULL` as valid. star-lord owns this recorder logic; flagged here so the migration's round-trip smoke exercises the `None` path, not just `True`/`False`.
3. **Table placement note (raise to star-lord, do not overturn).** The W0.1 originating spec (math note §8, MIGRATION.md v1.24) named the column on `recompose_attempts` / surfaced via `class_balance_results`. The A4 dispatch places it on `class_fight_loadouts` alongside `archetype_label`. These are not the same table. star-lord owns table placement and the single-script v2.15 mandate (W0.2 §8.4) — so I am NOT overturning the dispatch's `class_fight_loadouts` target. But the producer writes this field into `player_class.balance_metadata` (`:1415`) and the `ClassBalanceResult` dataclass (`:718`), both of which are class-level, not loadout-level. **star-lord should confirm the recorder path that lands a per-class field onto `class_fight_loadouts` is correct (1 loadout : 1 class assumption holds), OR confirm intent to put it on `class_balance_results` per the original W0.1 spec.** This is the one item where the A4 dispatch and the originating W0.1 spec name different tables; resolving it is a star-lord recorder decision. Round-trip smoke must read the field back from whichever table receives it.

---

## 6. Round-trip smoke fixture (already exists; cite for star-lord)

The write-side round-trip fixture already passes:
`tests/test_balance_loop.py::TestW01EnergyTypeLever::test_w01_recompose_energy_calibration_round_trip` (PASS per AGENT_STATE.md `:3668`).

It asserts: rage class → `recompose_energy_calibration_applied` present in `ClassBalanceResult`; mana class → `False` (not None, not True). star-lord's v2.15 acceptance round-trip should extend this through the export/telemetry boundary to confirm the `None`/`NULL` (experimental-class) path persists and reads back as `NULL`, since the existing fixture only exercises `True`/`False`.

---

## 7. Summary for star-lord

```
column:   recompose_energy_calibration_applied
type:     INTEGER         -- tri-state 0/1/NULL, NOT plain boolean
nullable: YES
default:  NULL            -- not 0; None is a real producer output (experimental classes)
backfill: NONE            -- pre-W0.1 rows stay NULL (no source to derive from)
set true: balance_loop.py:2482 -> :2492 -> aggregated :1383 -> metadata :1415 / dataclass :718
caveat:   table placement (class_fight_loadouts vs class_balance_results) needs star-lord
          recorder confirmation — field is class-level, dispatch names loadout table.
```
