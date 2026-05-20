# ARPG Canon — Initial Skill Geometry Enumeration

**Date:** 2026-05-20
**Phase:** 1 — Reconnaissance
**Sources:** diablo2.io/skills (D2 full skill list), poewiki.net (PoE skills), community wikis/guides for D3/D4/PoE2/Last Epoch/Grim Dawn via WebSearch
**Total skills cataloged in CSV:** 74

---

## Summary

Phase 1 enumerated 74 iconic shipped ARPG skills across D2, D3, D4, PoE, PoE2, Last Epoch, and Grim Dawn. This represents the signature skills — the ones every ARPG player knows by name — not comprehensive rosters.

**Key vision-layer findings:**

1. **Four geometry patterns that do NOT fit cleanly into our 5 operational bins** emerged repeatedly. These are candidates for future bin-cut review (flagged in CSV as `geometry_fits_5_bins = PARTIAL`).

2. **The 5 operational bins handle the majority of shipped skills well.** Single-target, small-AOE, large-AOE, chain, and multi-spawn account for 55-60 of the 74 skills cataloged. The bins are not wrong — they're appropriate operational buckets.

3. **Element distribution in the canon** aligns broadly with our 7-element list, with fire/lightning/cold/physical dominating. Holy/dark/void are well-represented in specific games.

4. **Proxy/summon skills** appear in every game as signature builds but are a distinct axis (2A), not geometry bins — the canon validates our separation of proxy density as its own axis.

---

## Vision-Layer Findings: Geometry Patterns Outside the 5 Bins

The following patterns appear repeatedly in the ARPG canon and do not fit cleanly into single-target / small-AOE / large-AOE / chain / multi-spawn:

### Pattern 1: Orbital / Rotating Projectile

**Examples:** D2 Paladin Blessed Hammer, D3 Crusader Blessed Hammer, D2 Druid Tornado (partially)

**Description:** One or more projectiles orbit or spiral around the caster or a fixed point, dealing damage on contact with enemies during rotation. This is distinct from multi-spawn (which fire simultaneously) and from large-AOE (which is a centered blast). The rotational trajectory gives it a unique time-profile: enemies run into it rather than being hit by it.

**Current engine treatment:** Our palette has `whirlwind` (caster rotates) and `ring` (donut AOE) but neither captures "orbiting persistent projectile." The `persistent_zone` geometry is the closest approximation but lacks the orbital movement.

**Verdict:** This pattern is present in two of the most iconic builds in D2/D3 history. It does not cleanly map to any of our 5 bins. **Candidate for a future geometry type or parameter extension.** In the QD-engine context, this would produce a meaningfully distinct kit identity that currently cannot be generated.

---

### Pattern 2: Teleport-Strike / Gap-Closer Attack

**Examples:** PoE Flicker Strike, GD Blitz, D2 Barbarian Leap Attack, PoE2 Monk Tempest Flurry, D2 Paladin Charge, Last Epoch Erasing Strike (partially)

**Description:** The character teleports/dashes to a target and deals melee damage at the destination, all in one action. The damage is technically single-target, but the mandatory mobility component means the skill serves dual purpose (damage + repositioning) simultaneously.

**Current engine treatment:** `dash_attack` geometry covers this. It is in our palette (B11 addition). BC-wise it maps to single-target damage + Axis 1 mobility contribution. The five bins handle the damage geometry correctly; the mobility contribution feeds Axis 1 naturally. **No bin-cut change needed — this is well-handled.**

Verdict: NOT a missing geometry. The dual-purpose nature is captured across axes.

---

### Pattern 3: Attached / Branded Persistent Effect on Enemy

**Examples:** PoE Storm Brand (brand attaches to enemy and auto-attacks), PoE Vaal Flicker Strike (attached haste effect), some PoE curse skills

**Description:** An effect is placed on a specific enemy (not a ground location) and persists, dealing damage or applying effects over time. This is distinct from: ground persistent-zone (fixed location), DOT ailment (no autonomous action), totem (placed on ground), proxy (ally entity). It's specifically an effect that follows an enemy.

**Current engine treatment:** No geometry or effect type covers "attached-to-enemy persistent." Our DOT ailments approach this but they don't have the "autonomous action targeting the marked enemy" quality.

**Verdict:** Niche in the canon (primarily PoE 1's brand mechanic). At Phase 1, this is documented but not flagged as critical. If PoE-style brand identity is important for a future archetype, a parameter extension on DOT ailments might suffice.

---

### Pattern 4: Multi-Stage Trap / Charged Bomb

**Examples:** PoE Detonate Mines, D2 Assassin Wake of Fire, PoE2 Siphoning Trap, D2 Assassin traps generally

**Description:** Two-phase interaction: (1) place trap at ground location; (2) detonation triggered by proximity or explicit activation. The placement phase and detonation phase are distinct interactions with potentially different geometries.

**Current engine treatment:** `trap` geometry is DEFERRED in our palette (canonical/09-geometry-palette-discussion.md) specifically due to this multi-stage state machine complexity. The axis-lock doc doesn't address it.

**Verdict:** The ARPG canon confirms traps are load-bearing skill identity (Saboteur is one of PoE's most popular archetypes). Our deferral is documented and intentional. **This is a future bin-cut candidate for Phase 2+ archetype expansion.**

---

### Pattern 5: Channeled-Move AOE (Whirlwind / Cyclone)

**Examples:** D2 Barbarian Whirlwind, D3 Barbarian Whirlwind, D4 Barbarian Whirlwind, PoE Cyclone

**Description:** The character deals AOE damage continuously while moving, with the movement path defining the damage area. This is in our palette as `whirlwind` geometry. For Axis 2 BC purposes it maps to small-AOE (the local radius around the caster at any moment).

**Verdict:** This is in our palette. Axis 3 (tempo + variance) naturally captures the sustained-high-tempo, low-variance profile. **No bin-cut change needed.**

---

## Element Distribution in the Canon (74 skills)

| Element | Approximate count | Notes |
|---|---|---|
| Fire | ~12 | Fireball, Meteor, Firestorm, Volcano, Detonate Dead variants, Phoenix Strike, Burning variants |
| Physical | ~12 | Whirlwind, most melee attacks, Barrage, Bone Spear, Erasing Strike |
| Lightning / Electric | ~10 | Chain Lightning, Lightning Fury, Arc, Storm Brand, Thunder Storm, Shock Web |
| Cold / Ice / Water | ~9 | Blizzard, Frozen Orb, Frost Nova, Ice Blast, Olexra's Flash Freeze, Glacier |
| Dark / Chaos / Void | ~9 | Corpse Explosion, Bone Spirit, Detonate Dead, Drain Life, Poison Nova, Dreeg's Eye |
| Wind / Air | ~5 | Hurricane, Tornado, Whirlwind (partial), Twister |
| Holy | ~4 | Blessed Hammer, Conversion, Holy Shock Aura, Consecrate |
| Neutral / Arcane | ~8 | Black Hole, Archon, Spectral Blade, Runic Invocation, various |
| Earth | ~5 | Pulverize, Fissure, Forcewave, ground effects |

**Key observation:** Fire and Physical are over-represented in the canon relative to our element palette. This is consistent with the telemetry finding in project memory (fire over-represented at 23.6% vs 20% expected in existing seasons). Earth and wind are under-represented in the canon's most iconic skills — they skew toward less iconic support/defensive roles.

---

## Timing Pattern Distribution

| Pattern | Approximate count | Notes |
|---|---|---|
| Instant | ~40 | Most offensive spells |
| Sustained/Channel | ~8 | Whirlwind, Cyclone, Archon, Aura of Censure, Auras |
| DOT/Persistent | ~10 | Burn, Bleed, Haunt, Poison skills |
| Delayed | ~4 | Meteor, Trozan's Sky Shard, Siphoning Trap |
| Triggered | ~6 | Detonate Mines, CWDT-style, Iron Maiden |
| Charge-up | ~3 | Phoenix Strike, Charged Dash (not in Phase 1 set), some PoE2 skills |
| Summon (persistent entity) | ~8 | Skeleton armies, Hydra, Gargantuan, Summon Sabertooth |

---

## Validation of Axis Structure Against Canon

### Axis 2 (Damage Geometry) — Validated
All 5 bins appear in the canon repeatedly. The bins are well-chosen.

### Axis 2A (Proxy Density) — Validated
Every game has signature summoner archetypes. Proxy-light (hydra, sentry, totem) and proxy-heavy (skeleton army) are both well-represented. The proxy axis cleanly captures a category that cannot be folded into geometry.

### Axis 2B (Control Density) — Validated
Pure control casters (PoE Curser, D3 Wizard freeze-orb, D2 Necromancer with curses) exist as recognized archetypes. The mixed vs control-pure distinction is meaningful.

### Axis 5 (Resource Economy) — Validated
- HP-economy: D2 Bone Spirit, PoE Blood Magic, D4 Necro Sever — each uses HP as resource. Confirmed important archetype category.
- Charge-stack: PoE Frenzy/Power charges, D3 Wizard arcane orbs. Confirmed.
- Damage-taken-converts: PoE CWDT, D4 Barbarian rage-on-damage. Confirmed.
- Generator-spender: D3 Barbarian Fury, D3 Crusader Wrath, D4 Rogue combo. Confirmed as the core modern ARPG economy pattern.

**Assessment:** The 7-bin Axis 5 structure is well-validated by the canon. All bins have multiple canonical representatives.

---

## Phase 2 Recommendations for Track D

1. **Expand D2 skill coverage** — only ~40% of D2 classes fully enumerated in Phase 1. Assassin traps, Amazon javelin skills, Druid shapeshifting have gaps.
2. **Expand PoE 1 coverage** — PoE has the richest skill geometry variety. Full skill gem inventory (~700+ gems) would be highest-value Phase 2 target.
3. **Add Diablo Immortal** — not covered in Phase 1. Has simplified but canonical skill geometry that mirrors D3.
4. **Document orbital/rotating projectile pattern more fully** — at least 3-4 more examples likely exist in Torchlight / Lost Ark / Marvel Heroes.
5. **Confirm trap geometry coverage** — enumerate all trap-class skills to assess whether trap as a geometry type is sufficiently load-bearing to warrant un-deferring.
