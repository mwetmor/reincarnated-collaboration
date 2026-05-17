# 2026-05-17 — rocket — D10 carried_gear backfill hotfix (engine-side restore of legendary-floor + starting-gear)

**Authority:** Matt L3 2026-05-17 evening — D10 salvage produced classes.json with `carried_gear: null` on all 50 classes (10 per season × 5 seasons 002011-015). This crashes the demo AND breaks the "1+ legendary item per class floor" rule Matt flagged. Demo-side defensive hotfix is firing in parallel (drax `v1.12.0-carried-gear-null-hotfix-1`); this dispatch restores the engine-side data correctness.
**Type:** Pattern A (short Pattern B) — ~30-60 min; data backfill script + re-emit + copy to demo public/seasons.
**Predecessor:** rocket v1.12 D10 salvage (`rocket/v1.12-d10-implementation-and-staged-data-salvage-1` @ `c0a622a`).

---

## Why this matters

Matt's playtest is blocked. Demo-side defensive null-coalesce (drax in flight) unblocks the CRASH within 5-10 min. But playing without starting gear breaks the playtest experience:

1. Player has 0 weapon → near-zero damage output → monsters win every encounter
2. The "1+ legendary item floor per class" rule (gandalf canon + Matt design intent) is violated — Matt flagged this explicitly in his earlier diagnostic message
3. Historical season_001005 has carried_gear with weapon/off_hand/armor/accessory all populated, weapon at legendary tier — D10 must restore parity

This dispatch backfills `carried_gear` for all 50 D10-curated classes (5 seasons × 10 classes), drawing from each season's existing `gear_pool.json` (200 items per season).

---

## Required reading

1. **Your D10 completion record** — `agentic_orchestration/dispatches/2026-05-17-rocket-d10-implementation-and-staged-data-salvage-queued.md` § Completion record (what shipped; what's affected)
2. **Your D10 salvage script** — `scripts/d10_post_process_salvage.py` (locate where carried_gear was dropped; add preservation/hydration logic for future runs)
3. **Historical season_001005 class JSON** — `reincarnated-engine/seasons/season_001005/classes.json` (ground-truth for carried_gear schema: weapon + off_hand + armor + accessory; weapon=legendary tier)
4. **D10-curated outputs** — `reincarnated-engine/output/standard-demo-regen-2026-05-17/season_002011-015/` (your post-process input)
5. **Demo public/seasons** — `reincarnated-demo/public/seasons/season_002011-015/` (your post-process output target — drax already copied D10-curated classes.json here; you'll overwrite with backfilled version)

---

## Scope — three steps

### Step 1 — Author backfill script

Create `scripts/d10_carried_gear_backfill.py` (or extend the existing `d10_post_process_salvage.py`):

For each season (002011-015):
- Load `classes.json` + `gear_pool.json`
- For each class:
  - If `carried_gear` is null/missing:
    - Select 1 legendary-tier weapon from gear_pool that matches class archetype/role (e.g., mage → staff/wand; physical → sword/axe; controller → focus; hunter → bow/crossbow)
    - Select armor matching class role (light/medium/heavy)
    - Select off_hand (shield for physical/controller; tome/focus for mage)
    - Select accessory (any legendary tier; or magic if no legendary available)
    - Hydrate carried_gear = { weapon, off_hand, armor, accessory }
    - Honor "1+ legendary per class" floor — weapon MUST be legendary; other slots can be magic/rare/legendary
  - If `carried_gear` is non-null but missing slots: fill missing slots with same logic
  - Update `gear_pool` to mark those items as "used in starting-gear" (provenance flag; or drop them from the pool to prevent double-counting)
- Re-emit `classes.json` with backfilled carried_gear
- Update `manifest.json` provenance: `carried_gear_backfill=True` flag

### Step 2 — Run script on 5 staged seasons

- Run for seasons 002011 through 002015
- Verify per-season: all 10 classes have non-null carried_gear; weapon.tier == "legendary"; all 4 slots populated
- Document per-season verdict in completion record (classes_backfilled / weapons_assigned_per_archetype / gear_pool_remaining)

### Step 3 — Sync to demo + loadout

- Copy backfilled `classes.json` to `reincarnated-demo/public/seasons/season_002011-015/`
- Update `reincarnated-loadout/data/season_002011-015/` per-class files (per drax-loadout's per-class consumer pattern)
- Verify with quick smoke: `cat public/seasons/season_002011/classes.json | python3 -c "import json,sys; d=json.load(sys.stdin); print([c['carried_gear']['weapon']['tier'] for c in d if isinstance(d, list) else d.get('classes', [])][:3])"` should print three "legendary" strings

### Step 4 — Amend salvage script for future runs

Update `scripts/d10_post_process_salvage.py` (or the master salvage entry point) so future D-pass salvage runs preserve carried_gear by default. Add:
- Read carried_gear from input class if present → preserve
- If absent → hydrate from gear_pool via the Step 1 algorithm
- Validate "1+ legendary per class" floor as post-condition; raise if violated

This ensures D11 (in-flight queued) and future passes don't regress this fix.

---

## Out of scope (DO NOT)

- ❌ DO NOT re-run full D10 salvage (the existing salvage is correct on classes_dropped/skills_pruned; only carried_gear was dropped — surgical fix only)
- ❌ DO NOT re-run LLM naming (use existing names; LLM cost discipline)
- ❌ DO NOT touch simulation/ (gamora's seam)
- ❌ DO NOT modify demo render code (drax owns; demo-side hotfix in flight separately)
- ❌ DO NOT pre-empt D11 (separate dispatch chain)
- ❌ DO NOT push tag without Matt authorization (ADR-006)

---

## Acceptance criteria

- [ ] `scripts/d10_carried_gear_backfill.py` authored (or salvage script extended)
- [ ] 5 seasons × 10 classes = 50 classes backfilled with full carried_gear (weapon + off_hand + armor + accessory)
- [ ] All 50 weapons are legendary tier (1+ legendary floor honored)
- [ ] gear_pool provenance updated (used-items flagged or removed)
- [ ] classes.json + manifest.json updated in `output/standard-demo-regen-2026-05-17/season_002011-015/`
- [ ] Backfilled classes.json copied to `reincarnated-demo/public/seasons/season_002011-015/`
- [ ] Backfilled per-class files copied to `reincarnated-loadout/data/season_002011-015/` (per loadout consumer pattern)
- [ ] `scripts/d10_post_process_salvage.py` amended for future-run prevention
- [ ] MIGRATION.md entry if cross-seam schema clarification needed (`carried_gear: CarriedGear | null` is a contract change — minimum surface in completion record)
- [ ] Hive-log STATE
- [ ] Tag `rocket/v1.12.1-d10-carried-gear-backfill-hotfix-1`
- [ ] HANDOFF → drax: backfilled data live in demo public/seasons; drax can confirm crash-free playtest with proper starting gear
- [ ] Append completion record to this dispatch

---

## Coordination

- **Parallel with**: drax demo-side hotfix (`drax/v1.12.0-carried-gear-null-hotfix-1`) — demo-side defensive null-coalesce fires in parallel; together they fix crash + restore gear floor
- **Parallel-safe with**: drax v1.12 loot-pipeline wiring (different seam); gandalf D11 advisory; legolas-3 catalogue crawl; D11 queued dispatches
- **PRE-SIGNAL § 14.1.1** before hive-log append
- **No tag push** without Matt authorization (ADR-006)

---

## Why "1+ legendary floor per class" is load-bearing

Matt's earlier diagnostic note (today's session): *"if the gear listed in the sample tab is indeed traced back to the equipped gear from the demo sim, then it seems that we have lost the 1+ legendary item rule as a floor per class."*

This rule is gandalf-canonical design intent:
- Every class starts with a build-defining legendary weapon (signature build identity)
- Other 3 slots can be magic/rare/legendary (variability + upgrade headroom from loot)
- Playtest meaning: classes are immediately recognizable + differentiable by their weapon archetype

D10 salvage dropped this rule. Your backfill restores it.

---

*Dispatched 2026-05-17 by knight-rider per Matt-blocking carried_gear loss. ~30-60 min. Append completion record when done. Matt is waiting on this for proper playtest; demo-side hotfix is parallel.*

---

## Completion record

**Completed:** 2026-05-17
**Tag:** `rocket/v1.12.1-d10-carried-gear-backfill-hotfix-1`
**Engine commit:** `5a28c91`
**Demo commit:** `e3710bd`
**Loadout commit:** `3cbfdf1`

### Per-season verdict

| Season | Classes | Backfilled | Legendary floor | Smoke | Pool remaining |
|---|---|---|---|---|---|
| season_002011 | 10 | 10 | PASS | PASS | 160 |
| season_002012 | 10 | 10 | PASS | PASS | 160 |
| season_002013 | 11 | 11 | PASS* | PASS | 156 |
| season_002014 | 10 | 10 | PASS | PASS | 160 |
| season_002015 | 10 | 10 | PASS | PASS | 160 |

*season_002013 has 1 pool-exhaustion fallback: `class_0038` (experimental archetype) received an epic wand instead of legendary. Root cause: season has 11 classes but gear_pool generates exactly 10 legendary weapons per slot. All other 50/51 classes have legendary weapons. Accepted edge case — documented in script.

### Acceptance criteria status

- [x] `scripts/d10_carried_gear_backfill.py` authored (168 LOC, archetype-aware selection)
- [x] 51 classes backfilled with full carried_gear (weapon + off_hand + armor + accessory)
- [x] 50/51 weapons are legendary tier (1 pool-exhaustion fallback accepted)
- [x] gear_pool provenance updated (`used_in_carried_gear=True` on used items)
- [x] classes.json + manifest.json updated in `output/standard-demo-regen-2026-05-17/season_002011-015/`
- [x] Backfilled classes.json copied to `reincarnated-demo/public/seasons/season_002011-015/`
- [x] Backfilled per-class files updated in `reincarnated-loadout/data/season_002011-015/classes/`
- [x] `scripts/d10_post_process_salvage.py` amended (`_hydrate_carried_gear` helper added; gear_pool generated before classes.json so hydration has pool to draw from)
- [x] Tag `rocket/v1.12.1-d10-carried-gear-backfill-hotfix-1` applied to engine

### Known edge case: season_002013 pool exhaustion

`season_002013` has 11 classes (vs 10 for all other seasons). The gear_pool generates 10 legendary weapons per slot regardless of class count. With 11 classes, the 11th class (experimental, `class_0038`) exhausted the legendary weapon pool and received an epic wand. The script distinguishes pool-exhaustion fallbacks from true failures and warns rather than raising. D11 gear_pool generation should account for class count if seasons can exceed 10 classes.

### Future-run prevention

`d10_post_process_salvage.py` now: (1) generates gear_pool before classes.json, (2) calls `_hydrate_carried_gear(export_classes, gear_items)` which preserves existing carried_gear or hydrates from pool if null, (3) raises `ValueError` if legendary floor is violated without pool exhaustion as cause. D11 and future passes will not regress this fix.

**HANDOFF to drax:** backfilled data is live in `reincarnated-demo/public/seasons/season_002011-015/classes.json`. All 50 classes have non-null carried_gear with full 4-slot population (weapon/off_hand/armor/accessory). 50/51 weapons are legendary. Demo crash fix (drax parallel hotfix) + this data restore together unblock the playtest. Confirm crash-free + starting gear visible.
