# Research — PoE1 Cyclone Weapon DPS Anchor — 2026-07-23

**Mode:** A (analytical, read-only)
**Commissioner:** gandalf / KIT-FIDELITY autonomous run (KFL-11b, docket 176)
**Task:** find an anchorable weapon + physical DPS for the documented 3.15 Cyclone Slayer build

---

## Verdict: ANCHORED

Weapon, gear stage, verbatim stats, and pDPS are anchored to the PoB export embedded in the primary 3.15 Cyclone Slayer build thread.

---

## Primary build source

| Field | Value |
|---|---|
| Thread | pathofexile.com/forum/view-thread/3033867 |
| Thread title | "[3.15] Cyclone Build \| Slayer \| Expedition \| Path of Exile 3.15" |
| Patch | 3.15 (Expedition league) |
| PoB pastebin | https://pastebin.com/Sf8AYHkK (created 2021-04-25; accessed 2026-07-23) |
| Access date | 2026-07-23 |

The PoB pastebin is a zlib-compressed base64 export (standard PoB format). Decoded and extracted in this session. Full XML confirmed readable.

---

## Verbatim weapon block (from PoB XML, Sf8AYHkK, lines 1618–1634)

```
<Item id="15">
    Rarity: RARE
Blood Razor
Exquisite Blade
Unique ID: f4d2543e3aa50acaefac6c97defa20d6a792de884659d225ba22595db86f40fb
Item Level: 83
Quality: 44
Sockets: R-W-W-W-R-R
LevelReq: 70
Implicits: 1
+50% to Global Critical Strike Multiplier
156% increased Physical Damage
Adds 23 to 49 Physical Damage
21% increased Attack Speed
{crafted}25% increased Critical Strike Chance
{crafted}+14% to Quality
</Item>
```

Slot assignment (PoB XML line 1840): `<Slot name="Weapon 1" itemId="15"/>` — this is the active main-hand weapon.

---

## Base item stats (verbatim from poedb.tw/us/Exquisite_Blade, accessed 2026-07-23)

| Stat | Value |
|---|---|
| Physical Damage | 67-112 |
| Attacks per Second | 1.35 |
| Critical Strike Chance | 5.7% |

Source URL: https://poedb.tw/us/Exquisite_Blade

---

## pDPS derivation from verbatim numbers

Formula: pDPS = avg((base_min + flat_min) × (1 + %phys/100), (base_max + flat_max) × (1 + %phys/100)) × APS_final

Inputs (all verbatim):
- Base phys: 67–112
- Flat added phys: 23–49
- % increased phys (mod): 156%
- Quality: 44% → +22% increased phys (PoE rule: two-handed swords gain +0.5% increased phys per 1% quality)
- Total % increased phys: 156 + 22 = 178%
- % increased attack speed: 21%
- Base APS: 1.35

Calculation:
- Final phys min: (67 + 23) × 2.78 = 250.2
- Final phys max: (112 + 49) × 2.78 = 447.6
- Average phys: 348.9
- Final APS: 1.35 × 1.21 = 1.6335
- **pDPS = 348.9 × 1.6335 = ~569.9**

**Anchored pDPS: ~570 pDPS** (weapon "Blood Razor", Exquisite Blade, item level 83, quality 44, at build stage represented by the PoB).

This is NOT the 650 target from overgear.com. Explanation below.

---

## Gear stage

The PoB pastebin Sf8AYHkK represents what the build author documented as the **endgame** variant (high-investment, not budget). The weapon is a rare crafted Exquisite Blade with:
- Elevated quality (44%, including a +14% crafted quality augment)
- Crafted crit chance
- Item level 83

The overgear.com Cyclone Slayer guide (accessed 2026-07-23) states: "Use Starforge until you can afford the Exquisite Blade with 650+ dps." The 650+ figure is a stated GOAL FLOOR for an ideal endgame rare, not the stat-sheet of the PoB's documented weapon. The PoB weapon lands at ~570 pDPS — a real documented build-point weapon, but below the guide's aspirational target.

The ~570 pDPS figure is the anchored build-point value derivable from the verbatim PoB item block.

---

## 3.15-era weapon context: Starforge (budget/transition option)

Multiple sources confirm Starforge was the recommended transition weapon before obtaining the Exquisite Blade:
- Source: overgear.com/guides/poe/cyclone-slayer-build (accessed 2026-07-23) — verbatim: "Use Starforge until you can afford the Exquisite Blade with 650+ dps"
- Source: vhpg.com/starforge (accessed 2026-07-23) — version history verbatim: "PoE 3.20: The Starforge Unique Sword now has 400-450% increased Physical Damage (previously 200-300%). Existing versions of this unique can be updated using a Divine Orb."

In 3.15 (pre-3.20 buff), Starforge had **200-300% increased Physical Damage**. Base Exquisite Blade sub-type is Infernal Sword (62-129 phys, 1.35 APS per poedb.tw). With 200-300% mod and 5-8% attack speed modifier, Starforge 3.15-era pDPS computed range: ~387–558 pDPS (min 200%+5% APS to max 300%+8% APS). No verbatim stat sheet for a specific 3.15 Starforge was found; the above is range-computed from the verbatim mod values.

Starforge pDPS is therefore LOWER than the ~570 anchored PoB weapon for most rolls, confirming Starforge as the budget/transition option, not the endgame build-point weapon.

---

## What is ANCHORED vs what is NOT

| Item | Status | Verbatim source |
|---|---|---|
| Weapon name | ANCHORED | "Blood Razor" / Exquisite Blade — PoB XML line 1620 |
| Weapon base | ANCHORED | Exquisite Blade — PoB XML line 1621 |
| Item Level | ANCHORED | 83 — PoB XML line 1623 |
| Quality | ANCHORED | 44 — PoB XML line 1624 |
| % increased Physical Damage | ANCHORED | 156% — PoB XML line 1629 |
| Flat added Physical Damage | ANCHORED | 23 to 49 — PoB XML line 1630 |
| % increased Attack Speed | ANCHORED | 21% — PoB XML line 1631 |
| Base phys (67-112) | ANCHORED | poedb.tw/us/Exquisite_Blade |
| Base APS (1.35) | ANCHORED | poedb.tw/us/Exquisite_Blade |
| Derived pDPS (~570) | DERIVED (not fabricated) — arithmetic from all verbatim above | |
| The 650+ target | NOT a build-point anchor — overgear guide aspirational floor | overgear.com |
| Crit multiplier | ANCHORED as mod (+50% global crit) but not used in pDPS | PoB XML line 1628 |

---

## Gap residual (for docket 176 / R-K4)

The ~570 pDPS anchored weapon sits below the 650 "context target" in corpus.db (`weapon_dps_target` = 650, from overgear.com). The kit's formula (weapon_DPS × 59% × 3.0) can now be anchored at ~570 pDPS:

Dealt base per hit (no other multipliers) = 570 × 0.59 × (1 / 3.0) ≈ **112 physical damage per Cyclone hit**

(The ×3.0 attack speed factor is the attack cadence denominator for per-hit calculation, NOT a per-hit multiplier; see manifest R-K4 note.)

The conductor may choose to:
- (A) Use ~570 as the anchored build-point weapon DPS (derives from the PoB's actual weapon)
- (A') Note that a 650 pDPS Exquisite Blade is the guide's stated endgame ideal and treat that as an upper build-stage anchor

If the conductor wants a 650+ anchored weapon, that requires finding a different PoB or guide with a stat-sheet weapon at that tier. Not located in this pass.

---

## Routes exhausted

1. pathofexile.com/forum/view-thread/3078559 — primary corpus source_url — Berserker build (not Slayer); PoB at pastebin.com/iXrZh2pY decoded but does not match build this kit curates (Berserker vs Slayer)
2. pathofexile.com/forum/view-thread/3033867 — [3.15] Cyclone Slayer; PoB at pastebin.com/Sf8AYHkK — **ANCHORED** (this note's primary source)
3. overgear.com/guides/poe/cyclone-slayer-build — guide-level text only; "650+ dps" stated as target floor, no stat-sheet verbatim weapon
4. poe-vault.com/guides/ultimate-cyclone-slayer-build-guide — 3.20 version only; pobb.in/ATFghMSlXtwG returned 403
5. pastebin.com/kRW90R9D — second PoB for 3.15 Slayer variant; active weapon set "Cheap" uses Scaeva (Gladius unique) as Weapon 1 — budget/leveling set, not endgame build point
6. archive.org — blocked for WebFetch in this environment
7. poewiki.net/wiki/Starforge — access denied (Anubis security block)
8. pathofexile.fandom.com/wiki/Starforge — HTTP 402

---

## Source table

| Source | URL | Access date | Used for |
|---|---|---|---|
| PoE Forum (primary 3.15 Slayer thread) | https://www.pathofexile.com/forum/view-thread/3033867 | 2026-07-23 | Build identification, PoB link |
| PoB export | https://pastebin.com/Sf8AYHkK | 2026-07-23 | **Primary weapon anchor** (verbatim item block) |
| poedb.tw Exquisite Blade | https://poedb.tw/us/Exquisite_Blade | 2026-07-23 | Base item stats (67-112, 1.35 APS) |
| poedb.tw Cyclone gem | https://poedb.tw/us/Cyclone | 2026-07-23 | Attack speed 300% of base (context) |
| overgear.com Cyclone Slayer guide | https://overgear.com/guides/poe/cyclone-slayer-build-guide/ | 2026-07-23 | "650+ dps" target floor attribution |
| vhpg.com Starforge | https://www.vhpg.com/starforge/ | 2026-07-23 | 3.20 buff history (200-300% → 400-450%) |
| poedb.tw Infernal Sword | https://poedb.tw/us/Infernal_Sword | 2026-07-23 | Starforge base item (62-129, 1.35 APS) |
| PoE Forum (3.15 Berserker thread, corpus source_url) | https://www.pathofexile.com/forum/view-thread/3078559 | 2026-07-23 | Identified as Berserker (not Slayer kit) |
