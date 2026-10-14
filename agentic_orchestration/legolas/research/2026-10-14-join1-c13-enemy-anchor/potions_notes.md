# C-13 census row 21: potions (KP-423), provenance notes

**Scope:** D2 LoD 1.13 potion laws for the Fire Sorceress, and the GD Warlord's health potion as the KC2 oracle carries it. The data is in `potions.json`, which `scripts/potions_extract.py` regenerates, running every assertion listed below. Everything was read-only. The oracle was imported, never edited.

**Grades:**
- **DATAMINED:** read from a 1.13 txt file at the pin.
- **MODEL-VERIFIED:** D2MOO code structure (the 1.10f reconstruction @ `5596f5cb`) confirmed by at least one community source.
- **INFERRED:** the code shows it by absence, or there is one source only.
- **UNKNOWN:** stated where it applies.

## Sources

| Source | Path | sha256 / pin |
|---|---|---|
| Misc.txt (1.13) | `captures/potions/Misc.txt` | `d01a3741…e207`; git blob `0640c199…3c61` = upstream `fabd/diablo2@45112569` (55,668 B) |
| Armor.txt (1.13) | `research/datamine-acquisition/d2/raw/Armor.txt` | same pin (J-S7 local copy) |
| Belts table | `captures/potions/blizzhackers-d2data-belts.json` | `c1f6b1f0…2db8`. ⚑ **This is D2R 3.0 data** (`blizzhackers/d2data@fc469993`); Belts.txt is absent from the 1.13 mirror. Used only for the box count, which Arreat and Basin confirm for 1.13 |
| D2MOO potion handlers | `../2026-10-08-d2-crushing-blow/captures/d2moo-SkillItem.cpp` | `1045184b…8696`: `SKILLITEM_pSpell03_Potion` L140–313, `pSpell05_RejuvPotion` L461–590 |
| D2MOO class multipliers | `captures/potions/d2moo-D2Common-Items.cpp` | `e494cec3…ee57`, L4572–4614 |
| D2MOO belt use and compaction | `captures/potions/d2moo-ItemMode.cpp` | `88c7ff5a…9d69`, L4388–4528 |
| D2MOO auto-belt slot search | `captures/potions/d2moo-D2Inventory.cpp` | `04c9bd2f…34e1`, L1714–1790 |
| D2MOO Blood Golem life-share (`sub_6FD0F8B0`) | `captures/potions/d2moo-Skills.cpp` | `ae7608f7…a7c4`, L358–400 (not relevant to the Sorceress) |
| Arreat Summit, Potions | `captures/potions/arreat-items-potions.{shtml,txt}` | `a46c3c12…a83` |
| Arreat Summit, Character basics (double-heal formulas) | `captures/potions/arreat-basics-characters.shtml` | `84db6f93…fee1` |
| Arreat Summit, belts (#Boxes) | `captures/potions/arreat-items-{normal,exceptional,elite}-belts.shtml` | see `shasum` |
| Basin, Consumable (class table) and Belt (Rows) | `captures/potions/basin-{Consumable,Belt}-raw.txt` | `627a7edc…`, `438cebc0…` |
| PureDiablo, *Diablo 2 Potions* (fill rate, averaging, belt) | `captures/potions/purediablo-diablo-2-potions.{html,txt}` | `fffbf921…`, `57167821…` |
| Oracle | `reincarnated-engine/src/reincarnated/simulation/kc2/{counterplay,sustain_procs,fixture}.py` and `data/kc2/pm4g_consumables.csv` | counterplay `f375323d…`, sustain_procs `dc8bb228…`, consumables `6956bfcb…` (also pinned inside counterplay.py) |

## D2 laws

1. **Amounts by tier.** The Misc.txt `calc1` value is multiplied by the class factor. For the Sorceress:

   | Potion | Health | Mana |
   |---|---|---|
   | Minor | 30 | 40 |
   | Light | 60 | 80 |
   | Regular | 100 | 160 |
   | Greater | 180 | 300 |
   | Super | 320 | 500 |

   Arreat's tables agree for all 7 classes, and the script asserts this. Internal Misc names are shifted one tier from the displayed names: `hp4 "Strong"` is displayed as Greater, `hp5 "Greater"` as Super. **MODEL-VERIFIED.**
2. **Durations.** Misc.txt `len`, in frames at 25 fps:

   | Potion | Frames | Seconds |
   |---|---|---|
   | Minor Healing | 192 | 7.68 |
   | Light Healing | 160 | 6.40 |
   | Healing | 171 | 6.84 |
   | Greater Healing | 192 | 7.68 |
   | Super Healing | 256 | 10.24 |
   | Every mana potion | 128 | 5.12 |

   The code uses `len` as the timed stat list's expiry. PureDiablo's "Fill Rate" column matches exactly. **MODEL-VERIFIED.**
3. **Delivery.** The amount is placed in 1/256-point units on the `healthpot` or `manapot` state as a per-frame regen of total ÷ frames.
   - **A second potion of the same kind extends the window and adds its amount.** The rate becomes (new + remaining) ÷ (remaining + len), so it never rises. Drinking a small potion on top of a large one slows the fill.
   - Code (pSpell03 L250–275), Arreat ("will not cause you to replenish life any faster") and PureDiablo ("averaged over the total time") all agree. **MODEL-VERIFIED.**
4. **Rejuvenation** (pSpell 5):
   - **Rejuvenation Potion:** 35 % of max life and 35 % of max mana. **Full Rejuvenation:** 100 % of each.
   - **Instant,** clamped to the maximum.
   - **No class multiplier and no double roll** (pSpell05 calls neither).
   - Sources: code and Arreat. **MODEL-VERIFIED.**
5. **Double fill.** Each health potion has a chance to deliver double, decided by **Vitality**; each mana potion by **Energy**.
   - The chance is P(rand%100 < ⌊randLimited(stat)/2⌋). The code-exact value equals Arreat's closed forms on both branches (below and above 200), and the script asserts this.
   - Example chances: Vitality 100 → 24.5 %; 200 → 49.5 %; 300 → 66.3 %.
   - **MODEL-VERIFIED.** ⚑ The Sorceress's Vitality is not pinned by the kit record, so the expected heal per Super potion runs from 320 up to 640 (×(1 + chance)). The parent's defensive sheet sets Vitality.
6. **Class modifiers.**
   - Health: Sorceress ×1.0 (Amazon, Paladin, Assassin ×1.5; Barbarian ×2.0).
   - Mana: **Sorceress ×2.0** (Necromancer and Druid ×2.0; Amazon, Paladin, Assassin ×1.5; Barbarian ×1.0).
   - Code (`ITEMS_GetBonus*BasedOnClass`), Arreat tables, Basin Consumable (relative form), PureDiablo tables. **MODEL-VERIFIED.**
7. **Cast interaction.** Drinking from the belt is an item-use request. Its code path has no player-mode gate and no animation, so it neither interrupts nor delays a cast. **INFERRED:** single code source, by absence; no community statement found.
8. **Being hit does not cancel the potion.** The state ends only at its expiry frame, and nothing in `SUnitDmg.cpp` removes `healthpot`. Arreat's "run away long enough for them to heal fully" is consistent with this but not explicit. **INFERRED.**
9. **No cooldown.** There is no use delay in pSpell03 or in the belt-use path; the limit is the stock. **INFERRED.**
10. **Belt.** Arachnid Mesh's base is Spiderweb Sash `ulc`: Armor.txt `belt` = 6 (DATAMINED), which gives **16 boxes = 4 rows × 4 columns**. Arreat elite belts list #Boxes 16, Basin lists Rows 4, and the D2R mirror gives numboxes 16. **MODEL-VERIFIED** for the 16.
    - **Hotkeys:** only the bottom row is hotkeyed (1–4).
    - **Column drop:** drinking pulls the potions above down that column (`sub_6FC49140`; PureDiablo "vending machine").
    - **Pickup:** a picked-up potion goes to a column already holding the same type, otherwise to an empty bottom slot if Misc `autobelt` = 1 (`INVENTORY_GetFreeBeltSlot`; PureDiablo).
    - **No inventory refill:** inventory potions do not refill the belt by themselves; shift-click moves them (Arreat).
    - These rules are MODEL-VERIFIED (code plus PureDiablo/Arreat). ⚑ The decompiled compaction loop indexes `4*i` without a column offset, which is probably a decompiler simplification. The rule rests on PureDiablo plus the code's intent.

## GD (oracle as carried; grade MEASURED per the oracle's own pins)

- **Record:** `records/skills/default/defaulthealthpotion.dbr` ("Tonic of Mending", `Skill_ChargePotion`), plus the allocated modifier `healthpotion_healovertime.dbr` ("Sansochromatis", rank 1).
- **Heal:** **800 flat + 25 % max HP instant**, plus **25 % max HP over time**. **Cooldown 12.0 s, 1 charge.** Unlimited uses in the oracle, which keeps no inventory count.
- **Over-time duration is MEASURED-ABSENT.** The oracle spreads it over the 12.0 s cooldown (C-I4-5, its lower limb).
- **At the oracle's hp_max of 20,005:** instant **5,801.25 HP (29.0 %)**, over time **5,001.25 HP at 416.8 HP/s**, total **10,802.5 HP (54.0 %) per drink**.
- **Healing increase:** Resilience's +24 % multiplies the potion (sustain_procs, row `resilience`, D-6).
- **Control states:** `RequestUseItem` is decoded PERMITTED in every control state, so no stun or trap gates it. `instant_cast` is True.
- **Actuation threshold** (fraction of max HP), by limb:
  - `I4_EXCURSION_MAX` = **0.49**: the default, and MEASURED-FALSIFIED at 5 of 9 by PREDICATE F, per the oracle's own docstring.
  - `TRACE_CONSISTENT` = **0.2297**.
  - `NEVER` = 0.

## Gaps and conflicts
- **Belts.txt 1.13 was not acquired.** The box count rests on Armor.txt type 6 plus three independent statements of 16, one of them D2R data.
- **Cast interruption, hit-cancel and no-cooldown are INFERRED** from code by absence. No second source was found.
- **The Sorceress's Vitality and Energy are unpinned**, so the double-fill expectation is a function of a stat the record does not fix.
- **D2 Belts and potion code are 1.10f (D2MOO), not 1.13.** No 1.13 change to the potion laws was found in Arreat or PureDiablo; that conclusion rests on absence.
- **GD over-time duration is MEASURED-ABSENT** in the oracle's own substrate. This is not a new gap.
