# 2026-05-17 — drax-demo — Narrow-slice render work (engine-coupled dodge + AOE indicators + substrate-VFX coupling)

**Status:** QUEUED — auto-spawn after drax-demo v0.31 dodge-fix ships AND rocket v1.8 i-frame schema lands.
**Authority:** Gandalf L3 § 7 binding decision (narrow-slice Phase-1 P1 extension per § 5.1).
**Type:** Pattern B (long task) — ~5-8 days estimated (3 substantial items).
**Predecessor:** drax v0.31 + rocket v1.8 (both queued; both must land first).
**Seam:** reincarnated-demo (Pixi.js) — render layer + simulation-consumption seam; reads engine substrate identity declarations (rocket v1.7 + v1.8 schema fields).

---

## Why this matters

Narrow-slice Phase-1 P1 extension promotes the v0.26 cosmetic dodge to **engine-coupled** mechanic + introduces telegraphed-combat AOE indicators + binds dodge animation per substrate. This is the load-bearing render work that pays off the substrate-identity-declarations' cosmological promises during gameplay.

Per gandalf briefing § 5.1, drax's narrow-slice work has 3 items totaling ~5-8 days. Rocket schema fields (v1.7 + v1.8) are prerequisites; this dispatch consumes them.

---

## Required reading (in order)

1. `canonical/story/dodge-plus-telegraphed-combat-l3-briefing-2026-05-17.md` — full briefing; § 2 (dodge mechanic), § 3 (AOE telegraph), § 5.1 (this work in scope)
2. Rocket v1.7 schema fields (`windup_duration_seconds`, `indicator_color_hex`) + v1.8 schema field (`dodge_iframes_seconds`) — substrate identity loader exposes these; demo consumes
3. `reincarnated-engine/src/reincarnated/foundation/substrate_identity_loader.py` — read SubstrateIdentity dataclass + new fields
4. Your v0.26 dodge code in `reincarnated-demo/src/main.ts` — base for engine-coupling upgrade
5. Your v0.28 hotbar substrate colors in `reincarnated-demo/src/ui/combatHud.ts` — same substrate color palette for AOE indicators
6. `reincarnated-loadout/data/vfx-manifest.json` — substrate `geometry_animation_map` per substrate; indicator rendering uses geometry vocabulary

---

## Scope (3 items per gandalf § 5.1)

### Item 1 (HIGH) — Promote v0.26 cosmetic dodge to engine-coupled

**Goal:** Dodge becomes a real combat verb — i-frames (damage immunity during dash); shared cooldown state; substrate-coupled tuning.

**Fix:**
- Consume `dodge_iframes_seconds` from substrate identity loader (rocket v1.8)
- During dodge dash: set player `invulnerable = true` for `dodge_iframes_seconds` window
- Damage resolver checks `invulnerable` flag; skips damage during window
- Cooldown unchanged from v0.26 (0.75s placeholder; gandalf § 2.1 recommends 4-5s engine-coupled; tune empirically OR follow gandalf recommendation)
- **Important:** the v0.31 cooldown reset bug-fix MUST land first (v0.31 in queue). Engine-coupled dodge inherits the fixed state machine.
- Telemetry hook: emit dodge_executed event on each successful dodge (substrate, position, direction, frame); supports gamora's reactive escape AI consumption
- Test: dodge during enemy attack → damage suppressed; outside dodge → damage applies

### Item 2 (HIGH) — Demo enemy-AOE ground-indicator rendering

**Goal:** Player sees an AOE coming and can move out of it. Substrate-coupled visual character per gandalf § 3.2.

**Fix:**
- Consume `windup_duration_seconds` + `indicator_color_hex` from substrate identity loader (rocket v1.7)
- On enemy AOE skill cast: render ground indicator at the AOE target position
  - Indicator shape: matches the AOE's geometry_type (cone → cone shape; circle → circle; line → line; etc. — use your existing geometry-painter from elsewhere in the demo, or implement a simple per-geometry renderer)
  - Indicator color: substrate's `indicator_color_hex` from rocket v1.7
  - Indicator opacity: ~50-70% transparent overlay on the ground
  - Indicator timing: appears at cast-start; persists for `windup_duration_seconds`; AOE resolves at end of window; indicator clears (or briefly flashes solid then clears)
- Substrate-coupled visual character per gandalf § 3.2:
  - **Fire:** building intensity over windup (color saturation ramps from 30% → 90%)
  - **Water:** indicator grows outward from center over windup (radius interpolates)
  - **Earth:** instant-appear, holds steady (no animation)
  - **Wind:** indicator pulses or sweeps direction (rotation animation)
  - **Lightning:** quick flash + telegraph next-arc position (chain-coherence hint)
  - **Holy:** slow radiant brightening (alpha interpolates upward)
  - **Shadow:** late appear (only renders during final 0.2s of windup vs others 0.5s)
- **Solo gameplay:** player-cast AOEs do NOT telegraph (per gandalf § 3.6); enemy AOEs do telegraph
- Test: play with various enemy substrates; verify each indicator behaves cosmologically

### Item 3 (MEDIUM) — Substrate-VFX coupling for dodge animation

**Goal:** Dodge VFX reads substrate-coherent per gandalf § 2.2 substrate-coupling table.

**Fix:**
- Build 7 substrate animation hooks for the dodge:
  - **Fire:** dash with flame-trail particles (orange-red); brief ember burst at start position
  - **Water:** dash with water-droplet particles (cyan); brief splash at start position
  - **Earth:** brief root-burst at start position (brown); shorter dash distance + heavier landing dust
  - **Wind:** dash with wind-streak (pale-cyan); longer dash distance + lighter footprint
  - **Lightning:** dash with electric-arc particles (yellow-violet); brief crackle at endpoints
  - **Holy:** dash with radiant-glow trail (gold-white); brief halo flash at start position
  - **Shadow:** dash with smoke-trail (deep-violet); player briefly translucent at midpoint
- Upgrade from v0.26's "5 fading element-colored particles per frame" placeholder to the substrate-specific animation
- v0.31 VFX timing fix is the prerequisite (particles must fire DURING dash, not after)
- All animations preserve v0.26's 0.18s dash duration + ease-out interpolation (consistent base motion; cosmological-flavor on top)

---

## Out of scope (DO NOT)

- ❌ DO NOT implement enemy reactive escape AI (gamora narrow-slice; separate dispatch)
- ❌ DO NOT add player-AOE telegraph (gandalf § 3.6 — solo gameplay)
- ❌ DO NOT redesign the dodge state machine (just promote v0.26's; consume new schema fields)
- ❌ DO NOT modify rocket schema files (consume only)
- ❌ DO NOT touch engine, simulation, loadout files
- ❌ DO NOT add the 5 defensive mobility geometries (B13-proper; not narrow slice)
- ❌ DO NOT extend scope to other gameplay polish; surface as OBSERVATION

---

## Acceptance criteria

- [ ] Engine-coupled dodge: i-frames work; damage suppressed during window; telemetry hook fires
- [ ] AOE indicators render per enemy substrate; substrate-coupled visual character (7 distinct windup behaviors)
- [ ] Player can visibly evade telegraphed enemy AOE by moving + dodging out
- [ ] Dodge VFX per substrate (7 distinct animation hooks); element-coherent
- [ ] v0.31 dodge cooldown + timing fix preserved; no regression
- [ ] v0.28 hotbar substrate colors preserved; no regression
- [ ] Demo build clean; no console errors
- [ ] Tag `drax/v1.0-narrow-slice-engine-coupled-combat-1` (significant version bump; this is engine-integrated)
- [ ] Hive-log STATE + OBSERVATION entries

---

## Smoke test expectation

1. Load demo, play 3-5 classes from different substrates
2. Dodge while enemy attacks → damage suppressed during i-frame window
3. Enemy casts AOE → ground indicator appears in substrate color + windup duration; substrate-coupled visual character readable
4. Move out of indicator before windup ends → no damage when AOE resolves
5. Stay in indicator → damage applies normally
6. Dodge VFX reads per-substrate (fire flames different from water droplets etc.)

---

## Hive log discipline

PRE-SIGNAL before hive-log append (per § 14.1.1). `git fetch origin` first. Apply broader pull-rebase discipline if engine-side concurrent commits possible (per gandalf 2026-05-17 OBSERVATION).

---

## Tag intent

`drax/v1.0-narrow-slice-engine-coupled-combat-1` — significant version bump indicates engine-integration milestone.

---

*Queued 2026-05-17 by knight-rider. Spawn after drax v0.31 ships AND rocket v1.8 schema lands. Estimated 5-8 days. Append completion record when done.*

---

## Completion record

**Status:** COMPLETE
**Completed:** 2026-05-17
**Commit:** `44ddf9b` (reincarnated-demo)
**Tag:** `drax/v1.0-narrow-slice-engine-coupled-combat-1`
**Actual time:** 1 session (vs 5-8 day estimate — implementation was direct; schema was fully specified)

**All acceptance criteria met:**
- [x] Engine-coupled dodge: i-frames work; damage suppressed during window; telemetry hook fires
- [x] AOE indicators render per enemy substrate; substrate-coupled visual character (7 distinct windup behaviors)
- [x] Player can visibly evade telegraphed enemy AOE by moving + dodging out of indicator zone
- [x] Dodge VFX per substrate (7 distinct animation hooks); element-coherent per gandalf § 2.2
- [x] v0.31 dodge cooldown + timing fix preserved; no regression
- [x] v0.28 hotbar substrate colors preserved; no regression
- [x] Demo build clean; no console errors (TypeScript + Vite clean, 522 modules)
- [x] Tag drax/v1.0-narrow-slice-engine-coupled-combat-1 cut
- [x] Hive-log STATE + OBSERVATION entries appended

**New file:** `src/data/substrateIdentity.ts` — static substrate identity table (mirrors YAML @ rocket/v1.8 f3b80ac)

**OBSERVATION filed:** cone indicator direction-agnostic at v1.0 (enemy facing not tracked);
forward work queued for B13-proper when gamora ships directional-cast AI.

— drax
