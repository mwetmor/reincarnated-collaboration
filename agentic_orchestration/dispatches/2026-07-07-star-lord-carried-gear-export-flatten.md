# Dispatch — 2026-07-07 — star-lord — carried_gear export-path flatten (step 2, re-scoped from rocket)

**From:** knight-rider
**To:** star-lord (export seam — the correct owner; re-scoped from the rocket+gamora nesting dispatch after rocket's STOP-and-flag)
**Approved by:** Matt 2026-07-06/07 (step 2 of the relayed 5-step sequencing — SAME defect, correctly-located seam)
**Estimated effort:** small — single-function flatten + round-trip smoke + MIGRATION; ~1–2h
**Acceptance:** the PERSISTED `carried_gear` (export path) carries the substrate binding in the canonical FLAT shape so an export/DB-read-back → combatant reads a NON-ZERO `spell_damage_modifier` for an INT kit (currently 0.0), with the in-memory pilot/gauntlet path unchanged and no other `carried_gear` consumer regressed.

## Context — verified premise (rocket STOP-flag `b3e5658`/`802cf5e` + knight-rider confirmation)

The original step-2 dispatch (`2026-07-07-rocket-gamora-carried-gear-nesting-unification.md`) named `season_generation_pipeline.py:472` as the fix site and assumed `gear_representative` and `carried_gear` are the same dict at different nesting depths. **rocket proved that FALSE by inspecting the actual phase2 JSON**, and knight-rider verified every link:

- `gear_representative.main_weapon` is a **full 10-field gear-slot entry** (`gear_instance_id, slot, rarity, partition_modifiers, capability_modifiers, t4_annotation, set_bonus, set_bonus_rank, is_unique, triggered_passive`) with the binding attached as a sub-key `substrate_binding` **BY DESIGN** (to avoid colliding with those 10 slot fields). `:472` is CORRECT — do not touch it.
- `carried_gear.main_weapon` is the binding **DIRECTLY** (canonical flat shape): the pilot builder produces `carried_gear = {"main_weapon": kit.substrate_weapon_binding}` (`season_generation_pipeline.py:1604`); `combatant.py:893-901` reads `_carried.get("weapon") or _carried.get("main_weapon")` then `.get("spell_damage_modifier", 0.0)` at TOP level. **The two shapes are correctly different.**
- **THE BUG (your seam):** `export/cycle13_normal_season_export.py:367-378` `_derive_carried_gear` returns `gear_representative` **verbatim** as `carried_gear` (`return gear_rep`). So a combatant built from the exported/persisted class reads the 10-field slot dict, finds no top-level `spell_damage_modifier`, and gets **0.0**. Persist path: `recorder.py:1211-1222` → read-back `season_exporter.py:725` → combatant → 0.0.

**Why it matters (gandalf inversion finding, §8.2):** casters depend ENTIRELY on the weapon spell pool (INT ~88%) for martial parity; martials get nothing from the weapon (physical pool is `gear_set`, empty in pilot). A 0.0-spell-pool caster from the persisted path is a silent nerf-to-zero. This must be fixed before loot work multiplies persisted-path consumers.

## Required reading before starting
- `agentic_orchestration/rocket/notes/2026-07-07-carried-gear-nesting-STOP-flag.md` — rocket's full empirical trace (the two shapes, all consumers).
- `agentic_orchestration/gandalf/notes/2026-07-06-caster-single-target-structural-finding.md` §8.1–8.3 (verified chain + inversion finding).
- `export/cycle13_normal_season_export.py:367-378` (`_derive_carried_gear` — THE fix site) + `:381-394` (`_derive_main_weapon` — the SEPARATE loadout WeaponDescriptor field, so you can confirm carried_gear vs main_weapon roles).
- `season_generation_pipeline.py:1604` (canonical flat shape) + `combatant.py:893-901` (the reader — do NOT change it).
- `recorder.py:1211-1222` (persist) + `season_exporter.py:725` (read-back) — the persisted round-trip you must exercise.
- `generation/MIGRATION.md:325` + `simulation/MIGRATION.md:4126-4130` — the two-shape carried_gear contract (already documented; keep honest).

## Math-before-code (Discipline #1) — document BEFORE editing
- The canonical flat shape you will produce: `carried_gear["main_weapon"] = <substrate_binding dict>` (matching `:1604`), NOT the 10-field slot entry.
- **The seam-owner decision (see open question 1):** whether the persisted `carried_gear` has ANY consumer besides the sim combatant that depends on `main_weapon`'s shape (the loadout via `types.ts`, any telemetry read-back). This determines whether a plain flatten is safe or whether the contract needs more care. RESOLVE and document this before editing — if a loadout/telemetry consumer needs the slot fields, STOP-and-flag like rocket did rather than break it.

## Cross-seam contract change? (Principle 6 gate — knight-rider completes this at authoring time)
**YES.** `carried_gear` is a persisted loadout-boundary dict (export → DB → sim combatant, and potentially → loadout UI). Changing its persisted shape is a cross-seam contract change.

**Acceptance MUST include:** `Round-trip smoke: an EXPORTED/persisted INT class → carried_gear → combatant_from_player_class (via the read-back path) reads a NON-ZERO spell_damage_modifier (was 0.0), AND the in-memory pilot/gauntlet path STILL reads the same non-zero value (no regression), AND no other carried_gear consumer (loadout/telemetry) regresses.` **MIGRATION.md REQUIRED** — update the EXISTING `substrate_binding`/`carried_gear` entries (`generation/MIGRATION.md:325`, `simulation/MIGRATION.md:4126-4130`) in lockstep to state the export path now produces the canonical flat shape.

## Scope
- [ ] **Fix `_derive_carried_gear` (`cycle13_normal_season_export.py:367-378`)** to produce the canonical FLAT `carried_gear` shape — extract `gear_representative["main_weapon"]["substrate_binding"]` up to `carried_gear["main_weapon"]` (matching the pilot builder at `:1604`). Handle the None/missing-binding case null-safely.
- [ ] Resolve open question 1 (other carried_gear consumers) and document the decision.
- [ ] **`cycle14_unified_bundle_emitters.py:538-576` is UNAFFECTED** (knight-rider verified: it reads `gear_representative`, not `carried_gear`) — confirm this holds and note it; do NOT change it.
- [ ] MIGRATION.md lockstep update (both files).
- [ ] Round-trip smoke (persisted path + pilot path) per Principle 6.
- [ ] Regression clean; pilot/gauntlet path behavior UNCHANGED.
- [ ] AGENT_STATE.md updated.
- [ ] Tag: `star-lord/v-batch2-carried-gear-export-flatten-1`.
- [ ] **Submit the tagged commit to `agentic_orchestration/qa/pending/` for jack-ryan Gate-2** (this is a persisted-path code change).

## Acceptance criteria
- [ ] Exported/persisted INT class → read-back → combatant reads NON-ZERO `spell_damage_modifier` (was 0.0). Concrete proof.
- [ ] In-memory pilot/gauntlet path STILL reads the same non-zero value — no regression.
- [ ] No other `carried_gear` consumer (loadout/telemetry) regresses (open question 1 resolved).
- [ ] `cycle14` emitter confirmed unaffected.
- [ ] Round-trip smoke (persisted + pilot paths) GREEN.
- [ ] MIGRATION.md existing entries updated in lockstep.

## Out of scope (explicit non-goals)
- **NO constant changes** (BASE_SPELL, multipliers, SC-6b values) — pure persisted-shape fix.
- **NO change to `gear_representative`** (`:472`) — it is correct-by-design; cycle14 + the reconstruction bridge + the validator all depend on its nested shape.
- **NO change to `combatant.py:893-901`** (the reader is already correct — fix the producer).
- **NO change to pilot/gauntlet path behavior** — it is already correct; if your fix would change it, STOP and flag.
- **NO loot-operator work** — this is the prerequisite that makes loot-path persistence safe.
- **NO caster bar re-derivation or re-pilot** (steps 1/3, gamora — step 1 is running now).
- **NO physical gear_set/pool change** (inversion finding is a later design fork; note in MIGRATION, don't act).

## Open questions for you to resolve (seam-owner decisions — document your answers)
1. **Does the persisted `carried_gear` have any consumer besides the sim combatant that depends on `main_weapon`'s shape** — the loadout (`types.ts`), any telemetry read-back? `_derive_main_weapon` (`:381`) produces a SEPARATE `main_weapon` WeaponDescriptor for the loadout, which suggests `carried_gear` is sim-facing and the flatten is safe — CONFIRM this. If a loadout/telemetry consumer needs the 10 slot fields under `carried_gear.main_weapon`, the plain flatten is NOT safe → STOP-and-flag with the contract conflict rather than break it.
2. Whether the flat `carried_gear` should carry ONLY `main_weapon` (matching the pilot builder exactly) or also other gear slots — decide per what combatant + any confirmed consumer actually reads.
3. Detached vs in-session (this is small; likely in-session with a checkpoint).

## References
- rocket STOP-flag `b3e5658`/`802cf5e`; gandalf finding §8 `9fb3467`; gamora ledger `79796e2`
- ADR-004 (MIGRATION), Principle 6 (round-trip), Discipline #1 (design-before-code), #11 (attribution)
- Run-state `batch2-run-state-2026-07-06.md` (5-step sequencing, step 2)

---

## Completion record

**Completed:** 2026-07-07
**Engine commit:** `64289f0`
**Tag:** `star-lord/v-batch2-carried-gear-export-flatten-1`
**Gate-2 submitted:** `agentic_orchestration/qa/pending/2026-07-07-star-lord-carried-gear-export-flatten-gate2.md`

### Open question 1 resolution

**FLATTEN IS SAFE.** The persisted `carried_gear` has no consumer besides the sim combatant that reads `main_weapon`'s internal substrate fields:

- Demo `CarriedGear` interface (`weapon/off_hand/armor/accessory` keys, `GearInstance` values) is a completely separate contract; applies to old-format seasons (season_002011 etc.), not the cycle-13 persist path.
- Loadout (`reincarnated-loadout`) has `carried_gear: null` for all classes in `v2_narrow_phase_5` and cycle-13 data.
- Loadout WeaponDescriptor (`main_weapon` field) is produced by `_derive_main_weapon()` (line 381), which reads `gear_representative` directly. This is a SEPARATE exported field from `carried_gear`.
- Telemetry DB stores `carried_gear` as opaque TEXT — no internal shape validation.
- Sim combatant (`combatant.py:893-901`) is the SOLE consumer of `carried_gear["main_weapon"]["spell_damage_modifier"]`.

### Fix applied

`cycle13_normal_season_export.py:_derive_carried_gear` now extracts `gear_representative["main_weapon"]["substrate_binding"]` and returns `{"main_weapon": substrate_binding}` (flat). Null-safe when binding is None or absent (static cycle-13 classes return `None`, correct scaffold behavior).

### cycle14 emitter confirmed unaffected

Zero references to `carried_gear` in `cycle14_unified_bundle_emitters.py`. It reads `phase2_kit.get("gear_representative")` exclusively — uses `gear_representative["main_weapon"]["substrate_binding"]` and `gear_representative["main_weapon"]["gear_instance_id"]` at the two-level nested structure, which is unchanged.

### Round-trip smoke — ALL PASS

```
SMOKE TEST 1: _derive_carried_gear flat output
  spell_damage_modifier = 0.72 at top level of main_weapon (no nesting)
  PASS

SMOKE TEST 2: combatant from_player_class read path
  combatant reads spell_damage_modifier = 0.72 (was 0.0 before fix)
  PASS

SMOKE TEST 3: null-safety (4 cases)
  All null-path cases return None correctly
  PASS

SMOKE TEST 4: in-memory pilot path unchanged
  fixed exporter output byte-equivalent to pilot builder carried_gear shape
  PASS

SMOKE TEST 5: real cycle-13 static char (S1_endgame_int_01_standard_wizard)
  substrate_binding = None → None (correct scaffold sentinel for non-substrate classes)
  PASS
```

### MIGRATION.md updates (lockstep, 3 files)

- `export/MIGRATION.md` — new batch-2 step 2 entry with full shape contract, consumer analysis, round-trip results, and inversion-finding out-of-scope note
- `generation/MIGRATION.md:325` — shape contract clarification appended (substrate path: binding is flat under main_weapon, not the slot entry)
- `simulation/MIGRATION.md:4126-4130` — key-alias note (main_hand/weapon/main_weapon or-chain) + persisted-path fix note appended
