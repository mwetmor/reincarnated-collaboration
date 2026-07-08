# Mob Rare/Champion Affix Layer — Existence Audit — 2026-07-08

**Commissioned by:** knight-rider
**Question (E9, Option C):** Does the mob rare/champion affix layer exist in the engine (real roll logic), or is it stubbed/never built?
**Verdict:** ABSENT

---

## Finding

The mob population is a flat stat-block system with no per-mob affix roll layer. There is no
rare/champion/elite modifier system analogous to Diablo 2 champion mods or PoE rare mods applied
to individual mobs at generation or simulation time.

---

## Evidence — what IS there (threat-tier stat-blocks only)

`monster_generator.py:382-475` — `MonsterGenerator.generate()` builds every monster as:
- HP roll from `TIER_HP_FACTOR_RANGE` (swarm / magic / trash / elite / mini-boss / boss)
- Armor roll from `TIER_ARMOR_FRACTION`
- Resistance rolls from dominant element
- Mana stats from `TIER_SKILL_COUNT`
- Skill set from archetype role pool
- AI behavior fields from archetype + threat_tier

No affix selection step, no rare/champion classification flag, no per-mob modifier roll exists in this path. The function returns a `Monster` with fixed stat-block fields only (`monster_generator.py:450-475`).

`endgame_mob_stat_profile.py:113-253` — the endgame profile table defines HP-factor ranges and armor fractions per threat tier (swarm / magic / elite / mini-boss / boss). No affix or modifier fields exist on `EndgameMobStatProfile` (`endgame_mob_stat_profile.py:154-185`).

`monster_schema.py` — not read directly, but the `Monster` dataclass fields referenced throughout are stat-block fields only; the `MonsterGenerator.generate()` return at `monster_generator.py:450-475` enumerates them all.

---

## Evidence — what "champion" / "rare" mean in the codebase (not an affix layer)

`arena.py:468-502` — "rare packs" is a **pack-composition label**: 3 packs of 1 `threat_tier="elite"` brute + 3 `threat_tier="swarm"` swarmer minions. These are unmodified flat stat-block mobs. The word "rare" labels the group arrangement, not a per-mob quality tier with modifier rolls.

`arena.py:980-1006`, `endgame_encounter_catalog.py:1032-1049` — "champion pack" means a group of magic-tier caster mobs (4× `threat_tier="magic"`) used as a harder sub-group within a room. No champion-affix roll; the mobs are standard `MonsterGenerator.generate()` outputs.

`spatial_engine.py:3470-3478` — "champion elevation" (`escape_elevation_multiplier=2.0`) is a **player-side damage scalar** for the F4 escape_lane scenario only. It multiplies the player's effective spatial offense, not a mob modifier. This is explicitly noted as a per-scenario instrument parameter, not a change to mob stat-blocks (`arena.py:339-343`).

`partition_modifier_pool.py` — all `affix` references are player gear affixes (weapon/armor/accessory slot modifiers). No mob affix pool exists in this file.

`generation/` directory-wide — every `affix` reference traces to player-side systems: `defensive_allocator.py:64-214` (player defensive profile affixes), `bc_target_composer.py:417-837` (player kit affix budget), `gear_generation.py`, `gear_catalog.py`, `gear_schema.py`. Zero mob-affix references.

---

## Disposition

**ABSENT.** No per-mob affix roll layer exists anywhere in the engine. The mob population is
purely a flat stat-block system: threat tier selects HP/armor/skill-count ranges; archetype
selects AI behavior and role pool; dominant element sets resistances. The genre-standard
rare/champion modifier layer (roll 2-6 mods per rare mob at spawn) has no implementation and
no stub — it was never built.

**Accrual lean:** this is its own axis row for Matt. The E9 stat-block reading is confirmed as
correct for what EXISTS, but the affix half of the "stat-blocks PLUS affix layer" design intent
is unbuilt. If the affix layer is desired for the full-run pivot, it requires net-new
construction (no partial implementation to extend).

---

## File:line citation index

| Claim | Citation |
|---|---|
| `MonsterGenerator.generate()` — flat stat-block only, no affix step | `monster_generator.py:389-475` |
| `TIER_HP_FACTOR_RANGE` — threat-tier stat tables, no affix fields | `monster_generator.py:32-51` |
| `EndgameMobStatProfile` — HP/armor/intent only, no affix fields | `endgame_mob_stat_profile.py:154-185` |
| "rare packs" = pack-composition label (elite + swarm mobs, flat) | `arena.py:468-502` |
| "champion pack" = group of magic-tier mobs (flat stat-blocks) | `arena.py:960-1006` |
| "champion elevation" = player damage scalar, not mob modifier | `spatial_engine.py:3470-3478`, `arena.py:339-343` |
| All `affix` hits in `generation/` are player-gear affixes | `defensive_allocator.py:64-214`, `bc_target_composer.py:417-837` |
| No mob-affix module exists anywhere under `src/` | directory-wide grep (zero hits on mob+affix compound patterns) |
