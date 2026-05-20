# Internal Substrate State — Phase 1 Quick Assessment

**Date:** 2026-05-20
**Mode:** A (analytical)
**Commissioner:** gandalf
**Sources:** reincarnated-engine source code, canonical design documents

---

## Summary

The current engine substrate has strong coverage in mid-range elemental mage archetypes and the mid-slow/ranged-slow engagement bins, but shows material gaps in three areas flagged by the axis-lock document: Axis 2A (proxy density), Axis 5 (HP-economy and charge-stack), and Axis 4 (full dodger bin). Two structural metadata gaps block all BC measurement: `movement_displacement_per_cast` (Axis 1) and `cost_type` (Axis 5 HP-economy) do not exist on the Ability schema. The `aoe_radius` field is also absent — Axis 2 geometry bins would be assigned by geometry type name rather than measured radius.

---

## Canonical Element List (Confirmed)

From `config/elements.yaml` + `config/substrate_identities/` directory listing:

**Rotating elements (substrate-bearing):** fire / water / earth / wind / lightning / holy / shadow  
**Non-rotating:** physical

That is **7 rotating + 1 non-rotating = 8 total canonical elements**.

The commission dispatch prior ("5-primary core") is inaccurate against the current engine state. The engine has 7 rotating substrate identities fully declared, with lightning/holy/shadow as the Phase-1 P1 expansion set (vocab-freeze list in `element/pool.py` shows some associated vocabulary entries are still frozen, but the substrate identities themselves exist in `config/substrate_identities/`).

**Implication for Track B (VFX catalog):** element tagging in the Unity asset catalog needs to cover all 7 rotating elements, not just 4-5.

---

## Per-Axis Assessment

### Axis 1 — Engagement Profile (6 bins)

**Current state:** Geometry pool infrastructure exists with close/medium/long range routing (`_filter_geometry_by_range()` in `ability_grammar.py`). Close-range pool covers warrior/grappler/skirmisher. Long-range physical covers hunter. Medium/long non-physical covers elemental mages.

**Substrate count estimate:** 5-8 distinguishable engagement profiles across archetype templates. Physical archetypes (warrior, grappler, skirmisher, hunter) + elemental mages (7 elements × 3-4 role orientations) provide meaningful variety.

**Key gap:** `movement_displacement_per_cast` metadata field does not exist on the `Ability` schema (`ability_schema.py` reviewed — no such field). Without it, the sim cannot measure tiles-per-minute displacement → Axis 1 bin assignment is blocked. The generator can produce mobility-bearing kits, but BC measurement for Axis 1 requires this extension.

**5× rule status:** Likely PARTIAL. Close-fast and ranged-fast bins require mobility metadata to confirm.

---

### Axis 2 — Damage Geometry (5 bins)

**Current state:** 26 active geometry types in `VALID_GEOMETRIES` frozenset (`ability_grammar.py` line 231-247). Geometry pools are well-populated across role types.

**Per-bin status:**
- **single-target:** 4 distinct geometries (melee_strike, single_target, projectile, ranged_physical). LIKELY OK.
- **small-AOE:** 8-10 distinct geometries (cone, circle, melee_arc, ground_slam, ring, vortex_pull, fork, ricochet_bounce, whirlwind). LIKELY OK.
- **large-AOE:** 3-5 (ground_targeted_circle, persistent_zone, multi_projectile, some circle/aura at large radius). PARTIAL — `aoe_radius` not tagged per skill, so bin separation requires radius measurement infrastructure.
- **chain:** 2 geometries (chain_lightning, ricochet_bounce). GAP. `is_chain` metadata not on Ability schema.
- **multi-spawn:** 2-3 (multi_projectile, totem, some approximations). PARTIAL. `is_multi_spawn` metadata not on Ability schema.

**Key gap:** `aoe_radius`, `is_chain`, `is_multi_spawn` not on Ability schema. Bin assignment would require inference from geometry name (which is reliable for chain_lightning and multi_projectile but not for general radius thresholds).

**5× rule status:** Single-target and small-AOE bins appear OK. Chain and multi-spawn are undersupplied (2-3 distinct geometries each vs ~5 required). Large-AOE marginal.

---

### Axis 2A — Proxy Density (3 bins)

**Current state:** Solo bin fully populated (all current archetypes). Proxy-light and proxy-heavy are fully deferred.

- **solo:** All current generation. 5× rule easily met.
- **proxy-light:** 0 shippable substrate. Totem geometry exists in the palette but ally AI / proxy lifecycle tracking absent from sim.
- **proxy-heavy:** 0 shippable substrate. `summon_combatant` staged but excluded.

**This is the most significant substrate gap flagged in the axis-lock document.** The axis-lock document (`qd-engine-bc-axes-lock-2026-05-20.md` §3.3) explicitly notes: "Player-side proxy generation absent today — major substrate gap." Phase 1 confirms this.

---

### Axis 2B — Control Density (3 bins)

**Current state:** 6 distinct ailment types in `config/ailments.yaml`: burn (dot), chill (soft_control), root (hard_control), knockback (hard_control), shock (hard_control), consecrate (amplification), drain (dot), bleed (dot). Of these, chill/root/knockback/shock are true CC ailments for Axis 2B.

Additionally, silence effect is in the grammar (`_make_effect()` handles silence directly).

**Per-bin status:**
- **damage-pure:** Multiple archetype templates produce kits with minimal control roles. LIKELY OK.
- **mixed:** Elemental mages with natural CC ailments (all rotating elements carry an ailment). LIKELY OK.
- **control-pure:** No dedicated control-pure archetype template. Control role exists but is paired with damage. Coverage thin.

**5× rule status:** damage-pure and mixed bins likely OK. control-pure may be undersupplied at the archetype template level.

---

### Axis 3A — Damage Tempo (3 bins)

**Current state:** `AbilityTiming` supports: instant, cast, channel, charge, delayed. Channel and charge timings produce distinctly different tempo signatures.

Energy cost types affect tempo: combo (0 cost primary = rapid spam), rage (builds up, limits spam), mana (standard rotation).

**Key gap:** Per-event damage-application logging in sim telemetry is not confirmed. Axis 3A measurement requires counting distinct damage events per second — this requires event-level telemetry, not just fight totals. The current `fight_result.py` and `fight_engine.py` would need review (not done in this pass).

**5× rule status:** Likely adequate at the generation level (enough timing variety). Measurement confirmation pending.

---

### Axis 3B — Damage Amplitude Variance (3 bins)

**Current state:** Charge timing produces spiky output. Channel timing produces flat output. Standard rotation with burst cooldown produces variable output. The three bins appear naturally emergent from existing timing mechanics.

**Key gap:** Per-event magnitude logging required (same as Axis 3A). Channel-tagged kits may need deferred routing if channel mechanics are incompletely simulated.

**5× rule status:** Likely adequate at generation level. Measurement pending.

---

### Axis 4 — Defensive Profile (4 bins)

**Current state:**
- `shield` effect in grammar (buff with magnitude + duration)
- `buff_defense` effect in grammar
- `buff_dodge` effect in grammar
- `heal_over_time` effect in grammar
- `lifesteal` effect in grammar
- `dodge_stance` geometry in VALID_GEOMETRIES (B13 extension)
- `roll` and `blink` in VALID_GEOMETRIES

**Per-bin status:**
- **glass:** Multiple archetypes have no defensive role — glass is the natural default. LIKELY OK.
- **mitigator:** Lifesteal + shield_buff + heal_over_time effects exist. PARTIAL — sim measurement of mitigation_fraction not confirmed.
- **tank:** High-eHP builds possible through stat allocation, but shield_pool tracking distinct from HP is unconfirmed in sim.
- **dodger:** dodge_stance/roll/buff_dodge exist. But stealth, iframe, and reflection sub-cases all deferred. Evasion-probability case may work.

**Key gap:** `eHP_effective_ratio` computation requires shield_pool tracking, regen tracking, and mitigation_fraction — none confirmed in current sim telemetry. The axis-lock document (§3.7) explicitly lists these as required sim extensions.

**5× rule status:** glass probably OK. Mitigator partial. Tank and dodger at risk.

---

### Axis 5 — Resource Economy (7 bins)

**Current state from ability_grammar.py and ability_schema.py:**

- `energy_cost: float` on Ability — no `cost_type` field (mana/HP/charge/etc.)
- Energy types in archetype templates: mana / rage / combo / focus / stamina-as-resource
- `AbilityTiming.name` can be "charge" for charge-up mechanic
- No `hp_cost_fraction`, no `is_charge_pool`, no `charge_cap`, no `charge_decay` fields

**Per-bin status:**
- **HP-economy:** 0 substrate. `cost_type` does not exist on Ability schema. FULL GAP.
- **damage-taken-converts:** 0 substrate. No mechanic exists. FULL GAP.
- **charge-stack:** Charge timing exists but this is charge-up-and-release (Axis 3 mechanic), not charge-pool accumulation (Axis 5 mechanic). Structural gap.
- **starved:** Emergent from high-cost mana builds. Likely some coverage.
- **overflow:** Rage post-buildup approximates overflow. Likely some coverage.
- **generator-spender:** Combo energy type explicitly implements this. Rage also qualifies. LIKELY OK.
- **steady:** Standard mana with balanced cost/regen. LIKELY OK.

**This is the second most significant substrate gap.** The axis-lock document (§5 substrate flags) notes HP-cost skill variety and charge-stack mechanic variety as both requiring enrichment. Phase 1 confirms both are absent.

**5× rule status:** HP-economy = 0, damage-taken-converts = 0, charge-stack = ~0. Generator-spender and steady likely OK. Starved/overflow partial.

---

## BC Metadata Extension Summary

Fields that must be added to `Ability` schema before full BC measurement is possible:

| Field | Axis | Current state |
|---|---|---|
| `movement_displacement_per_cast` | Axis 1 | absent |
| `aoe_radius` | Axis 2 | absent |
| `is_chain` | Axis 2 | absent |
| `is_multi_spawn` | Axis 2 | absent |
| `cost_type` | Axis 5 | absent — only `energy_cost: float` exists |
| `is_hp_cost` | Axis 5 | absent |
| `is_charge_pool` | Axis 5 | absent |
| `charge_cap` | Axis 5 | absent |
| `charge_decay` | Axis 5 | absent |
| `is_damage_to_resource_conversion` | Axis 5 | absent |
| `grants_evasion` | Axis 4 | absent |
| `grants_stealth` | Axis 4 | absent |
| `grants_iframes` | Axis 4 | absent |
| `grants_reflection` | Axis 4 | absent |

These match the substrate dependency list in `qd-engine-bc-axes-lock-2026-05-20.md` §6.

---

## Highest-Priority Substrate Gaps

1. **Axis 2A proxy-light/proxy-heavy** — 0 substrate; requires sim extension for ally AI + proxy lifecycle. Well-documented deferral.
2. **Axis 5 HP-economy** — 0 substrate; `cost_type` field absent from Ability schema; no Blood Magic equivalent in generation.
3. **Axis 5 charge-stack** — 0 substrate at kit-economy level; only charge-timing exists (which is an Axis 3 mechanic, not Axis 5).
4. **Axis 5 damage-taken-converts** — 0 substrate; no mechanic exists.
5. **Axis 2 chain bin** — 2 geometries (chain_lightning, ricochet_bounce) vs ~5 required for 5× rule.
6. **Axis 4 dodger** — stealth/iframe/reflection sub-cases deferred; evasion-only case thin.
