# KIT-CAL-1 R-KC1-20 / R-KC1-21 — the scratch `max_hp` wake: census, battery, findings

**Author:** gamora (simulation seam) · **Date:** 2026-07-28
**Run:** KIT-CAL-1 (`KC1-2026-07-27`), gandalf RUN-CONDUCTOR · **Rulings:** R-KC1-20 + R-KC1-21, Matt
**Tag:** `gamora/v-scratch-maxhp-wake-1` @ `9218238` (engine, `main`, **not pushed**)
**Math note:** `reincarnated-engine/src/reincarnated/simulation/math/scratch-maxhp-wake-2026-07-28.md`
**Gate 2:** REQUIRED, NOT self-cleared — item 3 of
`agentic_orchestration/qa/pending/2026-07-28-gamora-bq3-calibration-override-door.md`

---

## 1. The one-line result

The projection player's kernel scratch `max_hp = 1.0` is repaired to the real pool. Four kernel
operators that were computing defined answers to the wrong question now compute the right one.
**No emitted field, digest, or fight outcome changed** — all three digests byte-identical.

---

## 2. The correction the measurement forced

Both O-d and the commission assumed the repair "wakes production kits' lifesteal in every season".
Measured, it does neither of those things:

- **The defect is confined to the PROJECTION path.** `balance_loop.py` and `gauntlet_sim.py` thread a
  real `PlayerClass` → `from_player_class` → real `max_hp`. Season generation therefore never calls
  the repaired factory. Reachability, not a digest argument.
- **Production-path kernel lifesteal was never dormant.** It fires **55×** in a 6-fight battery, plus
  75 HoT scratch heals (max 888 HP) and 170 nonzero scratch heals — **all discarded**, because the
  spatial loop carries back exactly two scalars (damage float `:2554`, DoT float `:5241`) and
  `SpatialFightResult` has no heal field among its 47.

One symptom, two mechanisms: **scratch-clamp** on the projection path, **sync-omission** on the
production path. Only the first is what R-KC1-20 repairs.

---

## 3. Census (R-KC1-21) — class rulings

Bounded to the adapter's scratch construction, `resolve_spatial_hit`'s discard list, and the two sync
sites. **[O]** = operand / sync-list correction, fixed now. **[B]** = build class, reported not built.
**[D]** = declared projection default, not a death.

### 3a — Scratch-clamp deaths

| # | member | site | class | fixed-or-finding |
|---|---|---|---|---|
| S1 | kernel lifesteal clamp `min(dmg·pct, max_hp−hp)` | `damage_resolver.py:1259` | **[O]** | **FIXED** — 0 → 42 fires (PROJ battery) |
| S2 | heal cap `min(mag·bonus, max_hp−hp)` | `damage_resolver.py:1203` | **[O]** | **FIXED** — same operand (181 corpus `heal` effects) |
| S3 | HoT tick cap `min(tick_heal, max_hp−hp)` | `effect_resolver.py:124` | **[O]** | **FIXED** — 0 → 51 scratch heals (93 corpus HoT effects) |
| S4 | freeze-shatter `hp/max_hp < frac`, `dmg = max_hp·pct` | `effect_resolver.py:140-142` | **[O]** | **FIXED, still 0 fires** — `freeze` emitted by NOTHING (0/4,772 class skills, 0/2,332 mob effects) |
| S5 | execute threshold `hp/max_hp < frac` | `damage_resolver.py:977`, `:552` | **[O]** | **FIXED, still 0 fires** — `_ResolverSkill` has no such field AND 0/5,021 corpus skills carry it |
| S6 | scratch `mana=1e9` / stamina / regen | adapter `:234-241` | **[D]** | deliberate double-gate avoidance (spatial selector owns energy) |
| S7 | scratch defence literals (armor/resists/crit/dodge/accuracy/status/block) | adapter `:246-257` | **[D]** | this IS the ratified BQ-3 door surface |
| S8 | scratch `skill_states=[]` | adapter `:253` | **[D]** | resolver skills carried separately; `resolve_skill` reads none |
| S9 | `SpatialEntity.max_hp` vs kernel `max_hp` may DIVERGE (production path, gear `bonus_hp`) | `:5678` vs `combatant.py:1066` | **[B]** | **FINDING F-1** — two HP pools for one actor; not created or repaired here |

### 3b — Sync-omission deaths

| # | member | site | class | fixed-or-finding |
|---|---|---|---|---|
| Y1 | **HoT healing** (the commission's named candidate) | `effect_resolver.py:125` | **[B]** | **FINDING F-2 — I ruled it BUILD, not sync-list.** See §4. |
| Y2 | direct `heal` effect heal | `damage_resolver.py:1204` | **[B]** | **FINDING F-3** — same carrier problem, same double-count hazard |
| Y3 | kernel lifesteal heal | `damage_resolver.py:1260` | **[B]** | **FINDING F-4** — carrying it back would STACK with the ratified O-d door |
| Y4 | reflect / thorns `attacker.hp -= _reflect` | `damage_resolver.py:532` | **[B]** | **FINDING F-5** — player-side thorns structurally inert on the spatial path |
| Y5 | `on_lifesteal` / `on_crit` events at the OFFENSE site (`return_events=False`) | `spatial_engine.py:2554` | **[B]** | **FINDING F-6** — Wave-C trigger plumbing; death channel already opts in |
| Y6 | `shield` ActiveEffect on attacker scratch | `damage_resolver.py:1210` | **[D]** | **NOT dropped** — read by `absorb_with_shield`. Docstring was over-broad; corrected. |
| Y7 | `buff_damage` / `buff_*` | `damage_resolver.py:1231` | **[D]** | **NOT dropped** — read by `get_buff_percent`. Same correction. |
| Y8 | `silence` on defender scratch | `damage_resolver.py:1244` | **[D]** | **NOT dropped** — F8 gate reads it (`spatial_engine.py:2219-2238`) |
| Y9 | `last_kill_element` / `output_by_element` | `:929`, E3 spine | **[D]** | **NOT dropped** — persistent scratch |
| Y10 | attacker scratch `hp` NOT re-synced at the OFFENSE site | `spatial_engine.py:2546-2604` | **[B]** | **FINDING F-7 — HALTED.** See §5. |

**Held out by ruling regardless of temptation:** BQ-4 on-crit Battle Surge · BQ-1 target-cap
rank-scaling · BQ-2 per-skill cone · passive HP regen tick (1.10 HP/s, undetectable by G-5).

---

## 4. Why the HoT bridge is BUILD class and not a copy-list omission

`tick_effects` **returns one scalar** (DoT damage). Healing is not in its return contract, and the
kernel is READ-ONLY at this seam (Phase 0 boundary, MIGRATION v1.64). The only zero-signature-change
carrier is a delta-read of `heals_received` — and that counter is **conflated**: lifesteal (`:1262`),
`heal` (`:1205`) and HoT (`:126`) all increment it. A delta-read would therefore carry lifesteal heals
back too — i.e. **build O-d's mechanism through the back door and double-count against the ratified
O-d door**. A clean HoT-only carrier does exist (`bc_signals.hot_recovered`, split out for BC §2.4),
which is exactly why electing it is a design call: it needs a ruling on the clamp (spatial pool vs
kernel pool — see F-1) and on ordering against the DoT subtract. Q-KC1-1.

---

## 5. What I HALTed on

**F-7 — the attacker scratch `hp` is not re-synced at the offense site.** It is re-synced only
defensively (`adapter:373` when the player is a defender, `spatial_engine:5204` on the DoT bridge). It
looks like a one-line sync-list addition. It is not: adding the in-sync **without** F-2/F-3/F-4's
out-carry makes every clamp compute a *more* truthful heal that is **still discarded** — zero benefit
— while changing WHEN each operator sees a damaged pool, which is a semantic change to five operators
with no consequence to justify it. The in-sync and the out-carry are one decision.

**No awakened mechanic was found behaving wrongly.** Nothing else was HALTed.

---

## 6. Battery verdict

Harness: `simulation/scripts/gamora_kc1_scratch_maxhp_wake_battery_2026_07_28.py`.
Artifacts: `2026-07-28-kc1-scratch-maxhp-wake-battery-{before,after}.json` (this directory).
6 fights, seed `74_000_500`, open_arena, a kit carrying lifesteal + heal + HoT + shield + buff_damage,
mobs carrying lifesteal.

| digest | before | after |
|---|---|---|
| BQ-3 pre-registered (`730_010_001`) | `25c212eb…` | **UNCHANGED** |
| ARM PROD (`74_000_500`) | `9c4da4f7…` | **UNCHANGED** |
| ARM PROJ (`74_000_500`) | `94236eb0…` | **UNCHANGED** |

**The pre-registered digest did NOT need re-registering.** The commission expected it to move; it did
not, and I declined to perform a cosmetic re-registration that would leave a record claiming a golden
master was reset when it was not.

### Deltas per awakened mechanic (ARM PROJ)

| mechanic | before | after | reaches spatial HP? | reaches an emitted field? |
|---|---|---|---|---|
| kernel lifesteal (`on_lifesteal`) | 0 | **42** / 48 branch entries | **no** (F-4) | no |
| heal cap + lifesteal (nonzero scratch heals) | 0 | **84**, max 243.76 HP | **no** (F-3/F-4) | no |
| HoT tick cap | 0 | **51**, max 432.0 HP | **no** (F-2) | no |
| freeze-shatter | 0 | **0** | — | — |
| execute | 0 | **0** | — | — |
| `mean_mobs_killed` / `win_rate` | 3.5 / 0.0 | **3.5 / 0.0** | — | — |

ARM PROD: **every counter identical** — the repaired factory is not on that path.

**Anomalies: NONE.** No awakened mechanic behaved wrongly; each behaved exactly as its (now truthful)
operands imply, and each heal is discarded by the same unbuilt carry-back that discarded it before.

### Other instruments

- **KF-4 kit-compiler smoke:** 36 GREEN / 0 RED / 1 known GAP; four pilot fights **numerically
  identical** (`win_rate` 1.00/0.00/0.00/0.00, `mobs_killed` 40/5/26/23, `elapsed`
  56.1/120.1/120.1/120.1 s), diffed against a same-tree `git stash` baseline.
- **Door suites:** 76/76 (BQ-3 39 + O-d 37). 4 new tests; 2 rewritten with inverted semantics.
- **Regression:** 1,587 vs 1,585 (same-tree stash baseline); 34 failed / 21 errors both sides;
  **55 failure NAMES diff-empty**.

---

## 7. No-stack result

- **NS-1** — compiled pilot kits (`compile_kit` over `PILOT_KITS`) carry **no** skill-borne
  `lifesteal`. SKIPs rather than passing vacuously if the corpus DB is absent.
- **NS-2** — with the door open AND a kernel-lifesteal skill firing, `calibration_lifesteal_healed`
  equals `min(Σ delivered·pct, headroom)` **exactly** — no kernel admixture.
- **NS-3** — spatial HP gain over the cast equals the door's `healed` **exactly**; the kernel's
  contribution is 0.0. `OD-10b` pins the mechanism (the kernel heals the scratch, `SpatialEntity.hp`
  does not move), so NS-3 survives the day F-4 is built.

---

## 8. For the G-5 harness (queuing directly behind this)

Three things the harness may now assume that it could not before, and nothing it assumed is retracted:

1. The fixture's `_calibration_overrides["max_hp"]` reaches the **kernel** state as well as the
   spatial entity — **one body, not two**. Previously the kernel saw a 1-HP player while the entity
   saw 1,600.
2. Any `hp/max_hp` fraction the kernel computes for the player is real, so a future threshold mechanic
   will behave rather than silently never firing.
3. The O-d door remains the **only** leech reaching spatial HP (NS-3) — the A/B comparison measures
   what it says it measures.

**One thing the harness must NOT assume:** that freeze-shatter and execute are structurally dormant.
They are **corpus**-dormant. `freeze` is emitted by nothing today and `execute_threshold_fraction` by
nothing today; both facts have an expiry date, and the day generation emits `freeze`, player-side
shatter goes live at 20% of max HP per proc.

---

## 9. Housekeeping

- `src/reincarnated/output/leg3_pilot_section8a1_band_measurement.json` (star-lord's seam) was
  **not** rewritten this session — `tests/test_w3_emission_driver.py` was explicitly deselected and
  the file's mtime predates every run here. It remains uncommitted and is **not** in `9218238`.
- Battery output is written to a caller-supplied path; the harness never writes into
  `src/reincarnated/output/`.
- **Seed hygiene:** battery band `74_000_500–599`. **Next-free `74_000_700+`.**
- **Not pushed.** The conductor pushes.
