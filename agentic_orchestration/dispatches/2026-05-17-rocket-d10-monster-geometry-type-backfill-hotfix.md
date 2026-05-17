# 2026-05-17 — rocket — D10 monster geometry_type backfill hotfix (parity with class skills)

**Authority:** Matt L3 2026-05-17 late evening — D10 salvage populated geometry_type on CLASS skills but NEVER on MONSTER skills. Empirically: season_002015 has 104/104 monster skills with geometry_type=null. Demo crashes on monster cast (`audio.playAbilityCast(null, ...)` → TypeError → render-loop freeze after 2-4s combat). Demo-side defensive hotfix firing in parallel (drax `v1.12.0.1-audio-null-geometry-hotfix-1`); this dispatch restores engine-side data correctness.
**Type:** Pattern A — ~30-60 min; data backfill + script amendment + 5-season re-emit + copy to demo.
**Predecessor:** rocket v1.12 D10 salvage; v1.12.1 carried_gear backfill; v1.13 D11 implementation (just shipped).

---

## Why this matters

The D10 carried_gear bug taught us that salvage scripts must touch BOTH the field they fix AND any dependent fields that need parity. Carried_gear was one such miss; monster geometry_type is another. Symptom: identical to carried_gear — demo crashes, this time mid-combat instead of on class-select, because:

1. D10 `derive_geometry_type()` populated geometry_type on CLASS skills (51/51 classes, 473 skills, all populated post-D10)
2. Same derivation was NEVER applied to MONSTER skills
3. Monster skills retain pre-D10 geometry_type (null) from generation
4. First monster cast → demo's audio.ts:129 does `geometry.startsWith(...)` on null → TypeError → ticker crash → freeze

This dispatch backfills monster geometry_type using the SAME `derive_geometry_type()` 3-layer cascade rocket built for classes. Surgical fix; no rebalance; no LLM cost.

---

## Required reading

1. **Your D10 implementation** — `src/reincarnated/generation/geometry_derivation.py` (derive_geometry_type 24-type vocabulary; 3-layer cascade)
2. **D10 salvage script pattern** — `scripts/d10_post_process_salvage.py` (pattern to mirror)
3. **carried_gear backfill** — `scripts/d10_carried_gear_backfill.py` (5-season iteration pattern; idempotent)
4. **D10-curated outputs** — `reincarnated-engine/output/standard-demo-regen-2026-05-17/season_002011-015/monsters.json` (your post-process input)
5. **Demo public/seasons** — `reincarnated-demo/public/seasons/season_002011-015/monsters.json` (your copy target)
6. **Demo error site** — `reincarnated-demo/src/audio/audio.ts:129` + `main.ts:2667` (illustrates consumer expectation; geometry_type as non-null string)

---

## Scope — three steps

### Step 1 — Author monster geometry_type backfill script

Create `scripts/d10_monster_geometry_type_backfill.py` (or extend salvage script):

For each season (002011-015):
- Load `monsters.json`
- For each monster:
  - For each skill in monster.skills:
    - If `skill.geometry_type` is None/missing:
      - Call `derive_geometry_type(role=monster.role_orientation, element=skill.canonical_element, range_profile=monster.range_profile, effects=skill.get("effects", []), ...)` (reuse existing function; pass monster-level fields per math note convention)
      - Note: monster skills may have different inputs than class skills (no monster-level "class archetype"); use the existing 3-layer cascade with monster proxies (`role_orientation`, `range_profile`, `dominant_element`)
      - Populate geometry_type with derivation result
- Re-emit `monsters.json` with backfilled geometry_type
- Update manifest provenance: `monster_geometry_backfill=True`

Optional fallback (if derivation fails on edge cases): use `single_target` as safe default + log WARN. Demo defensive coalesce uses same default — keeps the two seams consistent.

### Step 2 — Run script on 5 staged seasons

- Run for seasons 002011 through 002015
- Verify per-season: all monsters have non-null geometry_type on all skills
- Document per-season verdict in completion record (monsters_backfilled / skills_backfilled / derivation_distribution)

### Step 3 — Sync to demo + amend salvage script

- Copy backfilled `monsters.json` to `reincarnated-demo/public/seasons/season_002011-015/`
- Update `reincarnated-loadout/data/season_002011-015/` if it consumes monsters (verify; per-class loader pattern doesn't typically consume monsters, but check)
- Verify smoke: `python3 -c "import json; d=json.load(open('public/seasons/season_002015/monsters.json')); m=d if isinstance(d, list) else d.get('monsters',[]); n=sum(1 for x in m for s in x.get('skills',[]) if s.get('geometry_type') is None); print(f'null_count={n}')"` should print `null_count=0`

### Step 4 — Amend salvage script for future-run prevention

Update `scripts/d10_post_process_salvage.py` (the master entry point) so future D-pass salvage runs:
- Apply geometry_type derivation to BOTH class skills AND monster skills (current code only handles classes)
- Validate as post-condition: assert no skill (class OR monster) has null geometry_type; raise if violated

This ensures D11 (just shipped) and future passes don't regress this fix. Note: rocket's D11 salvage just shipped; verify it didn't ALSO drop monster geometry_type for the 17 hybrid_mage instances it touched (likely fine since D11 only touched class-level damage_multiplier + tax provenance, not monster data — but verify).

---

## Out of scope (DO NOT)

- ❌ DO NOT re-run full D10 salvage (surgical monster-only fix; existing class data is correct)
- ❌ DO NOT re-run LLM naming (use existing names; cost discipline)
- ❌ DO NOT touch simulation/ (gamora's seam)
- ❌ DO NOT modify demo render code (drax owns; demo-side hotfix in flight separately)
- ❌ DO NOT pre-empt D11.1 recalibration (separate Matt-decision; this is unblocking only)
- ❌ DO NOT push tag without Matt authorization (ADR-006)

---

## Acceptance criteria

- [ ] `scripts/d10_monster_geometry_type_backfill.py` authored (or salvage script extended)
- [ ] 5 seasons × N monsters per season backfilled (e.g., 002015 has 44 monsters; total ~200 monsters across 5 seasons)
- [ ] All monster skills have non-null geometry_type post-backfill
- [ ] Derivation distribution documented per season (e.g., "ground_slam: 12; melee_strike: 8; single_target: 15; ..." — sanity check)
- [ ] Backfilled monsters.json copied to `reincarnated-demo/public/seasons/season_002011-015/`
- [ ] `scripts/d10_post_process_salvage.py` amended for future-run prevention (monster + class parity + post-condition assertion)
- [ ] D11 hybrid_mage salvage verified non-regressive (monster geometry_type still null OR populated — confirm which)
- [ ] Hive-log STATE
- [ ] Tag `rocket/v1.13.1-monster-geometry-type-backfill-hotfix-1`
- [ ] HANDOFF → drax: monster geometry_type live; defensive hotfix can be removed in future if desired (recommend keeping for hygiene)
- [ ] Append completion record to this dispatch

---

## Coordination

- **Parallel with**: drax demo-side audio hotfix (`drax/v1.12.0.1-audio-null-geometry-hotfix-1`) — together they unblock crash + restore data
- **Parallel-safe with**: elrond CraftPix curation (shipped); D11 recalibration decision (parked)
- **PRE-SIGNAL § 14.1.1** before hive-log append
- **No tag push** without Matt authorization (ADR-006)

---

## Why this matters (engineering lesson)

This is the SECOND time D10 salvage shipped with a missing-field bug that broke playtest. Pattern:
1. carried_gear was dropped on classes → demo crash on class-select (fixed by rocket v1.12.1 + drax v1.12.0)
2. geometry_type was never populated on monsters → demo crash in combat (fixed by THIS dispatch + drax v1.12.0.1)

The root cause is the same: D10 salvage script only thought about CLASS-level data; treated monster data as already-correct. Discipline #11 (attribution clarity) + Discipline #15 (demo as renderer) both implicated.

The salvage-script amendment (Step 4) is the durable fix — future passes will validate ALL skills (class OR monster) have non-null geometry_type as post-condition.

---

*Dispatched 2026-05-17 by knight-rider per Matt-blocking freeze diagnostic. ~30-60 min. Append completion record when done. Matt is waiting on this; demo-side hotfix is parallel.*

---

## Completion record

**Completed:** 2026-05-17
**Agent:** rocket
**Tag:** `rocket/v1.13.1-monster-geometry-type-backfill-hotfix-1`
**Engine commits:** 309b269 (scripts), 001994e (demo monsters.json data)
**Actual runtime:** ~8 minutes (script execution: 0.7 seconds; most time was reading/writing)

### Acceptance criteria verdict

- [x] `scripts/d10_monster_geometry_type_backfill.py` authored
- [x] 5 seasons x 44 monsters backfilled (220 monsters / 509 skills total)
- [x] All monster skills have non-null geometry_type post-backfill (post-condition PASS on all 5 seasons)
- [x] Derivation distribution documented per season (see below)
- [x] Backfilled monsters.json copied to `reincarnated-demo/public/seasons/season_002011-015/`
- [x] `scripts/d10_post_process_salvage.py` amended for future-run prevention (monster + class parity + post-condition assertion)
- [x] D11 hybrid_mage salvage verified non-regressive (d11 script only reads from `monsters/` subdirectory for balance loop, never writes to `monsters.json` aggregate — no regression path)
- [x] Hive-log STATE updated
- [x] Tag committed
- [x] HANDOFF note to drax: monster geometry_type now live; defensive null-coalesce in audio.ts can be retained as hygiene or removed at drax's discretion
- [x] Completion record appended

### Per-season derivation distribution

| Season | Monsters | Skills | melee_strike | single_target | vortex_pull | circle | self_buff | aura | multi_projectile | ground_slam | dash_attack | teleport | fallbacks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 002011 | 44 | 105 | 33 | 25 | 14 | 8 | 8 | 6 | 4 | 2 | 1 | 2 | 0 |
| 002012 | 44 | 98 | 30 | 25 | 16 | 6 | 7 | 4 | 5 | 3 | 1 | 1 | 0 |
| 002013 | 44 | 97 | 29 | 25 | 14 | 10 | 4 | 6 | 4 | 2 | 2 | 1 | 0 |
| 002014 | 44 | 105 | 34 | 24 | 14 | 6 | 9 | 5 | 6 | 4 | 1 | 2 | 0 |
| 002015 | 44 | 104 | 32 | 25 | 16 | 6 | 8 | 6 | 4 | 3 | 2 | 2 | 0 |
| **TOTAL** | **220** | **509** | **158** | **124** | **74** | **36** | **36** | **27** | **23** | **14** | **7** | **8** | **0** |

Distribution sanity: melee_strike dominance expected (monsters are primarily close-range physical/elemental melee fighters). vortex_pull strong (many control monsters). self_buff/aura present (support-role monsters). No fallbacks to `single_target` from error paths. Distribution is varied and plausible.

### What was done

**Step 1 — Backfill script:** `scripts/d10_monster_geometry_type_backfill.py` authored. Iterates all 5 seasons, loads monsters.json, derives geometry_type for each null skill using `derive_geometry_type()` with monster proxies (`range_profile`, `role_orientation` fallback for skill `role`, `dominant_element` fallback for `canonical_element`). Post-condition assert `null_remaining == 0` raises ValueError on failure. Writes backfilled monsters.json + sets `monster_geometry_backfill=True` in manifest. Copies to demo. Smoke checks demo.

**Step 2 — Execution:** Script ran in 0.7 seconds. All 5 seasons: post_condition=PASS, smoke=PASS. 0 fallbacks across 509 skills.

**Step 3 — Demo sync:** monsters.json synced to `reincarnated-demo/public/seasons/season_002011-015/`. Verified null_count=0 in all 5 demo files.

**Step 4 — Future-run prevention:** `scripts/d10_post_process_salvage.py` amended with two functions:
- `_backfill_monster_geometry_json(season_dir)` — derives + writes geometry_type to monsters.json at end of each salvage pass (mirrors the backfill script logic inline)
- `_assert_no_null_geometry_type(export_classes, season_dir)` — post-condition gate covering BOTH class skills AND monster skills; raises ValueError if any null found
Both wired into `process_season()` after classes.json rebuild. Paired with `_hydrate_carried_gear()` as "missing-field hygiene" block.

**D11 regression check:** `d11_post_process_salvage.py` reads individual monster files from `monsters/` subdirectory only for balance loop construction. It never writes to `monsters.json` (the export aggregate) or any monster export path. Confirmed: no regression from D11 pass.

**Loadout check:** Loadout (`reincarnated-loadout/data/`) uses per-class JSON files, not monsters.json — verified in dispatch scope and confirmed by d10_carried_gear_backfill.py pattern (loadout sync only touches classes). No loadout update required.

### Engineering lesson (captured)

This is the SECOND D10 missing-field bug that broke playtest:
1. `carried_gear=null` on classes → demo crash on class-select (fixed: rocket v1.12.1 + drax v1.12.0)
2. `geometry_type=null` on monster skills → demo crash mid-combat (fixed: THIS dispatch + drax v1.12.0.1)

Root cause in both cases: D10 salvage script treated monsters as "already correct." Only class data was given the derive/populate treatment. The durable fix is the `_assert_no_null_geometry_type()` post-condition gate that covers ALL paths in every future salvage pass. Discipline #11 (attribution clarity) + Discipline #15 (demo as renderer, not test harness) both implicated.
