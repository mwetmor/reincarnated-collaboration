# 2026-05-17 — drax-demo — v1.1 AOE indicator opacity refinement + skill VFX overlay

**Authority:** Matt L3 disposition 2026-05-17 (playtest CONTINGENT PASS on v1.0 ground-targeting; refinement request before step-away).
**Type:** Pattern A (short task) — ~15-45 minutes estimated (visual refinement; bounded).
**Predecessor:** drax v1.0 narrow-slice (`drax/v1.0-narrow-slice-engine-coupled-combat-1` @ `44ddf9b`).
**Seam:** reincarnated-demo (Pixi.js) — AOE indicator rendering + skill VFX layering.

---

## Why this matters

Matt's v1.0 ground-targeting test result: **CONTINGENT PASS**.
Quote: *"The color opacity should be lighter, with elements of the skills ability VFX overlayed and also translucent. I want to see a fireball VFX, transparently move across the floor if this is possible. If not, then PASS!"*

**Critical framing:** Matt explicitly said "If not, then PASS!" — meaning if the VFX-overlay-across-floor part is hard or risky, **ship the opacity reduction only** and treat v1.0 as PASS.

The intent: make the ground indicator **subtle** (where will the AOE land) so the actual skill VFX (fireball, ice, wind streaks, etc.) reads as the **primary** visual. Currently the indicator may be visually dominant; should be supportive.

---

## Required reading (in order)

1. Your v1.0 work — `reincarnated-demo/src/main.ts` `_spawnAoeIndicator()` (around line 893) + the indicator update loop (around line 1101) + the per-substrate visual character logic
2. `reincarnated-demo/src/visuals/` — existing skill VFX rendering (`dispatchAbilityVfx()`, projectile animation, particle systems)
3. Your prior v1.0 STATE entry in `agentic_orchestration/hive-mind/phase-1-p1-log.md`

---

## Scope (2 items; Item 1 required, Item 2 conditional)

### Item 1 (REQUIRED) — Reduce AOE indicator opacity

**Symptom:** v1.0 indicator opacity (~50-70% transparent overlay per dispatch spec) reads as too prominent; competes with skill VFX visual focus.

**Fix:**
- Reduce indicator base alpha from current value to **~25-35%** transparent
- Substrate-coupled visual character per gandalf § 3.2 still applies (fire brightens over windup, water radial-grows, earth instant-persist, etc.) — just scaled to the lower alpha range
- Specifically: peak alpha during indicator should not exceed ~35-40% even when "brightening"
- Color saturation unchanged (still substrate `indicator_color_hex`); only alpha lowered

**Smoke:** indicator visible but reads as background/secondary; skill VFX (when traveling toward target) reads as primary visual.

### Item 2 (CONDITIONAL) — Skill VFX renders ACROSS the indicator floor

**Symptom:** Matt wants the actual skill projectile/animation VFX to be visible passing across the ground indicator translucently — e.g., a fireball trailing across the floor where it will land.

**Investigation needed:**
- Audit the current skill VFX rendering for ground-targeted AOEs
- Where does the projectile/animation render? (above the indicator? alongside? not at all for AOE-cast types?)
- Is there a z-order issue where the indicator overlays/obscures the projectile?
- Is there a render-layer issue where ground-targeting VFX renders in a separate layer from the indicator?

**Fix (if low-risk):**
- Ensure skill VFX renders ABOVE the ground indicator (z-order)
- Both rendered translucent (~50-70% alpha for VFX, ~25-35% for indicator beneath)
- The VFX's particle trail should be visible passing across the indicator's floor footprint
- Verify per geometry type: circle (fireball arc-to-target visible across the indicator); cone (sweeping motion visible); line (path visible); etc.

**Decision authority:** Drax — your call whether this is achievable in 30-45 minutes additional.
- **If clean implementation path identified:** ship Item 2 alongside Item 1
- **If complex / risky / requires VFX system refactor:** ship Item 1 only, document Item 2 finding as OBSERVATION + Phase-2 followup, and tag as "v1.1 (Item 1 only)" — fully acceptable per Matt's "If not, then PASS!"

---

## Out of scope (DO NOT)

- ❌ DO NOT redesign the AOE indicator system (substrate-coupled visual character per v1.0 stays)
- ❌ DO NOT modify the dodge / i-frame / telemetry logic from v1.0
- ❌ DO NOT modify engine, simulation, or loadout files
- ❌ DO NOT change substrate `indicator_color_hex` values (those come from engine; demo only consumes)
- ❌ DO NOT change AOE windup timing
- ❌ DO NOT extend scope to other VFX polish noticed; surface as OBSERVATION
- ❌ DO NOT pursue Item 2 if implementation requires more than ~45 min additional or touches the VFX system in non-trivial ways — Matt explicitly authorized Item 1-only fallback

---

## Acceptance criteria

- [ ] AOE indicator alpha reduced (peak ~25-35% instead of v1.0's higher values)
- [ ] Substrate-coupled visual character preserved (fire brightening, water growing, etc.)
- [ ] If Item 2 attempted: skill VFX renders translucently above/across indicator; z-order clean; no visual fighting
- [ ] If Item 2 deferred: documented as OBSERVATION in hive log + Phase-2 followup task
- [ ] Demo build clean (`npm run build`); no console errors
- [ ] Tag `drax/v1.1-aoe-indicator-opacity-refinement-1` (Item 1) or `drax/v1.1-aoe-indicator-opacity-and-vfx-overlay-1` (Items 1+2)
- [ ] Hive-log STATE entry documenting which path chosen + reasoning

---

## Smoke test expectation

1. Load demo; play a class with AOE skills
2. Enemy casts AOE → indicator appears with lighter opacity; substrate-coupled animation still readable
3. If Item 2 shipped: skill VFX (fireball/ice/etc) visible passing through/over the indicator translucently
4. Build clean

---

## Math-before-code requirements

N/A — visual polish.

---

## Hive log discipline

PRE-SIGNAL before hive-log append (per § 14.1.1). `git fetch origin` first.

---

## Tag intent

`drax/v1.1-aoe-indicator-opacity-refinement-1` (Item 1 only) or `drax/v1.1-aoe-indicator-opacity-and-vfx-overlay-1` (Items 1+2).

---

*Dispatched 2026-05-17 by knight-rider per Matt L3 disposition before step-away. Estimated 15-45 min. Append completion record when done.*

---

## Completion record

**Completed:** 2026-05-17 by drax
**Path taken:** Item 1 only (Matt's "If not, then PASS!" fallback applied for Item 2)
**Tag:** `drax/v1.1-aoe-indicator-opacity-refinement-1` @ `dd770fd`
**Build:** TypeScript clean, Vite 14.10s, 522 modules.

**Item 1 — shipped:**
- `baseAlpha` building ramp: `0.07 → 0.25` (was `0.18 → 0.63`). Peak under 0.25.
- Impact flash: `0.35` peak (was `0.85`).
- Earth persist: starts `0.20` (was `0.45`), fades to 0 over 1.5s.
- All 7 substrate visual characters preserved. Indicator reads as background; VFX reads as primary.

**Item 2 — deferred (architectural blocker found, not complexity aversion):**
AOE indicator geometries (`circle`, `ground_targeted_circle`, `ground_slam`, `cone`, etc.) don't
produce traveling projectiles — VFX fires at impact position instantaneously. Traveling projectile
geometries (`projectile`, `ranged_physical`, etc.) are in `noIndicatorGeoms` (no AOE indicator).
No configuration exists where a projectile "travels across" an AOE indicator. Achieving Matt's
fireball-across-floor vision requires spawning a decorative windup-arc VFX for AOE geometry skills
— a new feature (~2-4h), not a z-order fix. Z-order is already correct (VFX added after indicator
in same `particles` container, so VFX naturally renders on top). Deferred cleanly.

**Acceptance criteria status:**
- [x] AOE indicator alpha reduced (peak ~25% during windup)
- [x] Substrate-coupled visual character preserved
- [x] Item 2 deferred: documented as OBSERVATION in hive log + Phase-2 followup task in AGENT_STATE
- [x] Demo build clean
- [x] Tag applied: `drax/v1.1-aoe-indicator-opacity-refinement-1`
- [x] Hive-log STATE entry with path chosen and reasoning
