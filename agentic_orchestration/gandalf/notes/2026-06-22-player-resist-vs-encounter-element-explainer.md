# Player gear-resist × encounter-element — how it actually works (explainer)

**Author:** gandalf (design seam). **Mode:** Pattern-B research, verification-first (Matt asked to understand the resist↔element interaction concretely). **Status:** explainer of CURRENT verified mechanism — not a ruling.

> **CORRECTION (2026-06-22, post-Matt).** The original draft's worked example sampled `exports/season_001001` and reported "a season runs ~4 elements (fire/water/earth/wind)." **That was stale May-2026 export data, pre-dating the Cycle-14 canonical-7 expansion — NOT current design.** Matt confirms: **every season runs all 7 rotating elements (fire/water/earth/wind/lightning/holy/shadow); there is no element rotation/subset.** The 4-element "seasons" were a long-dead legacy concept (LLM-flavor-named elements over a 4-element base). Verified the live code matches the 7-element design: `foundation.get_rotating_elements()` → 7; `monster_generator.py:490` ("Pattern P7: no silent fallback — all rotating elements included"); `t4_sim_cycling.ROTATING_ELEMENTS` + `typed_monster_skills.ROTATING_ELEMENTS` = the 7-tuple; the current cycle-14-wave-5 kit roster spans all 7. **No live 4-element bug** — only stale export files on disk. §3/§5/§7 below are corrected; the MECHANISM (§1/§2/§4/§6/§8) was always element-count-independent and stands.

**Read first-hand:** `foundation/math_model.py:116-128` (the formula) + `:34` (ARMOR_MITIGATION_K=3000); `simulation/damage_resolver.py:466-525` (mitigation flow); `simulation/combatant.py:24-61` (armor-symmetry floor), `:566-575/:926` (player-defender path — RAW resist), `:1100-1108` (monster-defender path — floored); `generation/gear_generation.py:942-992` (the `element_resist` mint — typed-resistance wave); `config/elements.yaml` (taxonomy, 7 rotating + physical); `generation/notes/typed_resistance_roundtrip_smoke_2026_06_21.py` (verified real numbers); `foundation.get_rotating_elements()` / `monster_generator.py:490` / `t4_sim_cycling.py:1071` (7-element confirmation).

---

## 1. The one-line mechanism

`damage_taken = incoming × (1 − resist[element])`

- **Elemental attacks ALWAYS hit** in the sim (`dodgeable:false` for all 7 rotating elements). No avoid-roll. The ONLY mitigation is the per-element resist fraction. (`math_model.py:116-128`)
- Resist is **clamped 0–95%** at the formula; gear **stacks toward a 0.80 per-element ceiling** (`gear_generation` mint + `combined_stats` sum).
- Resist can be **negative** (vulnerability) — the unit convention floor is −1.0 (`generation/MIGRATION.md:126`). Nothing rolls negative today, but the channel exists (a future "−25% fire" cursed item is mechanically legal).

## 2. The load-bearing fact: elemental resist and physical armor are SEPARATE axes

- **Physical armor** (`bonus_armor`, STR×8 + gear) mitigates ONLY physical damage, via `armor/(armor+3000)`.
- **Elemental damage** is mitigated ONLY by the per-element `elemental_resistances` dict. **Armor does nothing against fire/water/wind/etc.**
- A 2000-armor STR tank with `wind:0.00` eats a wind hit at **full**. A 300-armor glass mage with `wind:0.55` shrugs it. This is the **D2 / PoE model exactly** (armour ≠ elemental res; you build both, separately).
- **Asymmetry worth knowing (verified):** when the PLAYER is the defender the resist dict is RAW (`combatant.py:926`, no floor). When a MONSTER is the defender its resist is floored to the armor-symmetric curve (`:1104`, Phase-4 2026-06-20) so player casters can't bypass the mitigation martials pay. Net: **the player has no "free" elemental floor from armor — the defensive read is mandatory for every archetype, not just casters.**

## 3. The taxonomy (`config/elements.yaml`)

**7 rotating** (all `resistance_type: percentage`, all `dodgeable: false` — always-hit): fire, water, earth, wind, lightning, holy, shadow.
**1 non-rotating:** physical (`resistance_type: armor`, `dodgeable: true`, bleed ailment).

**No rotation/subset — every season runs ALL 7** (Matt-confirmed; verified `monster_generator.py:490`). A player at endgame faces all 7 elemental damage types in every season, so the resist read is across the full 7 (plus physical). Holy/shadow add the D7 luminance valence (±25%, `damage_resolver.py:499-504`) on top of the resist multiply, but only when both attacker+defender substrates are KNOWN.

## 4. A REAL sample character (verbatim from the production round-trip test)

A fire-weighted loadout — two fire-resist rolls (0.25+0.20) on the chest, +0.10 fire & 0.10 water on an accessory — resolves through `combined_stats()` to:

```
fire 0.55   water 0.10   earth 0.00   wind 0.00
```

**How the jaggedness is built:** each gear piece can roll an `element_resist` effect keyed to one element (mitigation fraction ≤0.80). `combined_stats()` SUMS per element across the loadout. Same-element rolls **stack** toward 0.80; different-element rolls **spread thin** (the anti-tax design — "cap everything" needs 7×0.80=5.6 resist-units; a realistic budget is ~1.5). So a built character is HIGH in one or two elements and near-zero elsewhere.

## 5. The comparison — this character in a season that runs all 7 (trial boss = WIND signature)

Every season runs all 7. To isolate the resist MULTIPLY (the invariant Matt asked about), hold incoming flat at a representative **1000** per element and read what the FIRE-built character takes:

| Encounter element | incoming | FIRE-built resist | takes | through |
|---|---|---|---|---|
| fire | 1000 | 55% | **450** | 45% |
| water | 1000 | 10% | **900** | 90% |
| earth | 1000 | 0% | **1000** | 100% |
| wind | 1000 | 0% | **1000** | 100% |
| lightning | 1000 | 0% | **1000** | 100% |
| holy | 1000 | 0% | **1000** | 100% |
| shadow | 1000 | 0% | **1000** | 100% |
| **WIND trial boss (signature)** | 1000 | **0%** | **1000** | **100%** |

**The punchline, sharpened by all-7.** The fire-built kit is protected on exactly ONE of seven axes. It brought the wrong form to a WIND capstone and eats the boss at full; it also eats 5 of the 6 non-boss elements at full. A WIND-built kit (`wind:0.55`) takes 45% on that boss — **2.2× less** on the capstone, the "bring the right form" reward made concrete. But note what all-7 does to the floor: a 1.0–1.5 resist-budget spread across 7 elements **cannot** cover them all (§7 / the cap-everything fork). The spiky build is the *only* build the current budget can produce — which is exactly the tension Matt's "65–75% on every element" target collides with.

(Incoming is held flat at 1000 here to isolate the multiply. Whether the live roster actually hits for different magnitudes per element — the thing the stale export wrongly suggested — is an open generation question, §7. The RESIST MULTIPLY column is the invariant Matt asked about and is exactly what ships.)

## 6. The honest generation-state finding (this is WHY the 0.926 watch-item exists)

Every player-side gear export I can read (`season_001005/009/010`, May 2026) has **`elemental_resistances: {}` — EMPTY on all 200 pieces.** Pre-typed-wave, `_derive_stats` initialized the dict and never wrote it (`gear_generation.py` had no `element_resist` branch). **Player elemental defense was a globally-inert constant** — exactly the anchor ruling's phrase.

The **typed-resistance wave (just closed, decisions-log `ea39ecc`)** added the `element_resist` mint branch (`gear_generation.py:969-980`) — verified live. So the CURRENT cycle-14 content is the **first** to carry real per-element rolls. The mechanism in §1–5 is **newly live, not yet seasoned into broad content.** That is the mechanical root of the 0.926 soft-median watch-item: the "bring the right form" reward only just started being minted, and it currently bites at the under-resourced tail rather than the median (compounded by offense substituting for the defensive read — calibration §9.3).

## 7. Two design observations to flag (not rulings)

1. **Magnitude-by-element asymmetry — UNVERIFIED (the stale-export trap).** The stale `season_001001` export showed wind/water hitting 2500 and fire/earth 625 (a 4× spread). I will NOT assert that as current — it is pre-canonical-7 May data, the same stale source that produced my 4-element error. The open question stands regardless: in the live 7-element roster, do different elements hit for materially different magnitudes? If yes, "which element you FACE" swings threat alongside "which element you RESIST," and that wants to be a stated design knob, not an emergent artifact. One glance at a freshly-generated 7-element season answers it. Worth doing before broad emission.
2. **No elemental floor for tanks (the §2 asymmetry).** Because player armor doesn't touch elemental, a high-armor build with an unrolled element is just as exposed there as a glass mage. Defensible (it makes the defensive read universal, which serves "bring the right form"), but Matt should know it's the live behavior: there is no "tanky enough to ignore elements" build. This is good for the design intent — name it so it isn't later "fixed" by accident (Discipline #13 drift guard).

## 8. Where this connects

This is the **build-floor's defensive read** from the encounter-model firm-up disposition (`2026-06-21-encounter-model-firm-up-disposition.md`). The resist↔element interaction IS the floor; the dodge-skill ceiling (Godot, deferred) is the texture on top. The cure for the soft floor remains **build the ceiling + season the content with real rolls**, NOT harden the per-hit damage (the rejected dm=6.0 tail-tax).
