# Player gear-resist × encounter-element — how it actually works (explainer)

**Author:** gandalf (design seam). **Mode:** Pattern-B research, verification-first (Matt asked to understand the resist↔element interaction concretely). **Status:** explainer of CURRENT verified mechanism — not a ruling.

**Read first-hand:** `foundation/math_model.py:116-128` (the formula) + `:34` (ARMOR_MITIGATION_K=3000); `simulation/damage_resolver.py:466-525` (mitigation flow); `simulation/combatant.py:24-61` (armor-symmetry floor), `:566-575/:926` (player-defender path — RAW resist), `:1100-1108` (monster-defender path — floored); `generation/gear_generation.py:942-992` (the `element_resist` mint — typed-resistance wave); `config/elements.yaml` (taxonomy); `generation/notes/typed_resistance_roundtrip_smoke_2026_06_21.py` (verified real numbers); `exports/season_001001/monsters.json` + `seasons/season_001001/trial.json` (the roster).

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

**Seasonal rotation:** a season's encounters draw a SUBSET. `season_001001` uses exactly **4** (fire/water/earth/wind), evenly: 10 monsters each. Holy/shadow add the D7 luminance valence (±25%, `damage_resolver.py:499-504`) on top of the resist multiply, but only when both attacker+defender substrates are KNOWN.

## 4. A REAL sample character (verbatim from the production round-trip test)

A fire-weighted loadout — two fire-resist rolls (0.25+0.20) on the chest, +0.10 fire & 0.10 water on an accessory — resolves through `combined_stats()` to:

```
fire 0.55   water 0.10   earth 0.00   wind 0.00
```

**How the jaggedness is built:** each gear piece can roll an `element_resist` effect keyed to one element (mitigation fraction ≤0.80). `combined_stats()` SUMS per element across the loadout. Same-element rolls **stack** toward 0.80; different-element rolls **spread thin** (the anti-tax design — "cap everything" needs 7×0.80=5.6 resist-units; a realistic budget is ~1.5). So a built character is HIGH in one or two elements and near-zero elsewhere.

## 5. The comparison — this character walking `season_001001` (trial boss = WIND)

Damage TAKEN per representative hit (incoming magnitudes verbatim from the export; resist multiply applied):

| Encounter element | incoming | A: FIRE-built resist | A takes | through |
|---|---|---|---|---|
| fire rooms (×10) | 625 | 55% | **281** | 45% |
| water rooms (×10) | 2500 | 10% | **2250** | 90% |
| earth rooms (×10) | 625 | 0% | **625** | 100% |
| wind rooms (×10) | 2500 | 0% | **2500** | 100% |
| **WIND trial boss** | 2500/1500/750 | **0%** | **2500/1500/750** | **100%** |

**The punchline.** The fire-built character brought the wrong form to a WIND capstone. It eats every wind hit at full. A WIND-built character (`wind:0.55`) takes 45% — and over a boss rotation the fire-built kit eats **2.22× the damage** the wind-built kit does (4750 vs 2138 per rotation). *That 2.22× is "bring the right form," made concrete.*

(Magnitudes are from the pre-typed-wave `season_001001` export and are illustrative — note the 4× fire/earth-vs-water/wind spread is itself a generation artifact worth a look, §7. The RESIST MULTIPLY — the 45%/90%/100% column — is the invariant Matt asked about and is exactly what ships.)

## 6. The honest generation-state finding (this is WHY the 0.926 watch-item exists)

Every player-side gear export I can read (`season_001005/009/010`, May 2026) has **`elemental_resistances: {}` — EMPTY on all 200 pieces.** Pre-typed-wave, `_derive_stats` initialized the dict and never wrote it (`gear_generation.py` had no `element_resist` branch). **Player elemental defense was a globally-inert constant** — exactly the anchor ruling's phrase.

The **typed-resistance wave (just closed, decisions-log `ea39ecc`)** added the `element_resist` mint branch (`gear_generation.py:969-980`) — verified live. So the CURRENT cycle-14 content is the **first** to carry real per-element rolls. The mechanism in §1–5 is **newly live, not yet seasoned into broad content.** That is the mechanical root of the 0.926 soft-median watch-item: the "bring the right form" reward only just started being minted, and it currently bites at the under-resourced tail rather than the median (compounded by offense substituting for the defensive read — calibration §9.3).

## 7. Two design observations to flag (not rulings)

1. **Magnitude-by-element asymmetry in the roster.** In `season_001001`, wind/water monsters hit 2500 and fire/earth hit 625 — a 4× spread — AND the trial boss is wind (the heavy element). So "which element you FACE" currently swings threat as much as "which element you RESIST." If unintended, it muddies the resist read; if intended (heavy vs light elements), it wants to be a stated design knob, not an emergent export artifact. Worth one glance before broad emission.
2. **No elemental floor for tanks (the §2 asymmetry).** Because player armor doesn't touch elemental, a high-armor build with an unrolled element is just as exposed there as a glass mage. Defensible (it makes the defensive read universal, which serves "bring the right form"), but Matt should know it's the live behavior: there is no "tanky enough to ignore elements" build. This is good for the design intent — name it so it isn't later "fixed" by accident (Discipline #13 drift guard).

## 8. Where this connects

This is the **build-floor's defensive read** from the encounter-model firm-up disposition (`2026-06-21-encounter-model-firm-up-disposition.md`). The resist↔element interaction IS the floor; the dodge-skill ceiling (Godot, deferred) is the texture on top. The cure for the soft floor remains **build the ceiling + season the content with real rolls**, NOT harden the per-hit damage (the rejected dm=6.0 tail-tax).
