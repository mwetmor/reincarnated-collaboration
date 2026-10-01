# Research — JOIN-1 J4b: D2 Fire (Meteor) Sorceress formulas, primary rows, loadout and C-12b — 2026-10-01

**Mode:** A (analytical; primary-source probe)
**Commissioner:** gandalf (Run JOIN-1, wave J4b research leg). Scope follows charter v0.5.1, which added Inferno, the prerequisites and the block exclusion mid-leg.
**Consumers:** gamora (the same D2 adapter, extended) → star-lord (kit rows) → drax
**Version for every number unless flagged:** Diablo II: Lord of Destruction, **expansion game, 1.13 txt data** (`fabd/diablo2 @ 45112569deb9384738ccafe5c24ebbb71f41c7c9`). The JOIN-1 law is LoD 1.13 (KP-160, Q10). Where D2R differs, the entry says so.

**Re-used, not redone:**
- J4a packet `agentic_orchestration/legolas/research/2026-10-01-join1-j4a-d2-ww-barb/`: resist law F07, DR/MDR F06, life/mana op law F12, leech F13, DifficultyLevels.
- Animation packet `agentic_orchestration/legolas/research/2026-10-01-join1-d2-animation-timing/`: FCR, FHR, FBR, Fire Ball travel, Meteor timeline.

## Files

| File | What it holds |
|---|---|
| `formulas.json` | 11 formula entries (H01–H11). Each has a label, a version, at least two sources, an explicit **damage_type** (W1), the cross-check, the D2R difference, conflicts and open items. H01 and H02 also carry sensitivity examples |
| `primary_rows.json` | Skills.txt rows 47, 56, 36, 61, 37 and 41, plus prerequisite rows 51 and 46. Also: Missiles `fireball`, `meteorcenter`, `meteorfire` (and the client visuals), SkillDesc ×5, SkillCalc, CharStats Sorceress. All verbatim and DATAMINED. Also per-level tables for slvl 1–60, a damage-type table, the kit's items resolved in 1.13 tables, file sha256s and the verification log |
| `c12b_home_frontier.md` | Commission C-12b: verdict, D2R-vs-1.13 analysis, candidates, re-entry criterion |

The labels are as in J4a:
- **DATAMINED:** read from the txt files or from D2MOO source.
- **MODEL-VERIFIED:** D2MOO structure confirmed by Arreat and/or Basin, with tables reproduced.
- **(partial):** one sub-clause is single-source or conflicted.
- **INFERRED** and **UNKNOWN:** as stated.

**Verification.** A generator rebuilt every table and asserted each against its second source; it aborts on any mismatch. All checks passed, with one recorded Arreat typo (see `verification_log`).

**Reproduction scripts (`scripts/`, added at the conductor's request after KP-166):**
- `fetch_sources.py`: read-only `curl` GETs of the five Basin pages and the Arreat Fire Spells page. Writes plain text to `scripts/sources/`, which is gitignored (or to `$J4B_SOURCES`).
- `gen_j4b.py <out_dir>`: reads the 1.13 txt tables from `research/datamine-acquisition/d2/raw/`, writes `primary_rows.json` and runs every assertion.
- `gen_formulas_j4b.py <out_dir>`: writes `formulas.json`, including the sensitivity rows.

Run them in that order. Re-run on 2026-10-01 from fresh fetches into a temporary directory, both JSON files came out **byte-identical** to the committed ones. Basin is a live wiki: if a page is edited later, the generator aborts and names the changed cell. That abort is intended.

---

## Summary

1. **Scope confirmed from the data.**
   - The operands are **36 Fire Bolt**, **61 Fire Mastery** and **37 Warmth**, as the charter guessed.
   - This leg found a fourth: **41 Inferno**. Meteor reaches it through `meteorcenter` → `meteorfire` → `skill('Inferno'.blvl)*3`. The charter pinned it at v0.5.1.
   - **Fire Wall 51** and **Blaze 46** are prerequisite rows, each with a level floor of 1.
   - **Teleport 54** is excluded: it is named only in the record's `motion_frame`.
   - **Shield block** is excluded under the pin, as a named fidelity cost.
2. **11 formulas: 8 MODEL-VERIFIED and 3 partial (H03, H06, H07).** The partial sub-clauses are:
   - the pyre lifetime (1 frame, code vs Basin) and the meaning of DamageRate, which rests on D2MOO alone (H03);
   - Arreat's Fire Ball radius of "1 yd", against the data's 2 2/3 yd (H06);
   - the auto-hit and no-block clauses, which have data plus code but no named community source (H07).
3. **The primary rows are DATAMINED, and every table reproduces.**
   - Fire Ball, Meteor, Fire Bolt, Fire Mastery and Warmth match Basin's slvl 1–60 tables exactly. That covers damage, mana, Meteor's displayed fire/s and pyre seconds.
   - They match Arreat's slvl 1–20 tables once the **prerequisite-forced synergies** are applied: Fire Ball +14%, Meteor +10%, pyre +3%.
   - The one exception is Meteor slvl 17 minimum: Arreat prints 696, the code gives 695, and Basin's raw 632 agrees with the code.
4. **The kit emits FIRE only (W1).** No physical, magic, cold, lightning, poison, burn or leech component exists on any castable row or its server missiles (`primary_rows.json` → `damage_types`).
5. **The loadout is mostly pinned by the record; the build is not** (§ 3).
   - Pinned gear yields **FCR 105–115**, which is the 105 breakpoint: **8 ticks per cast (0.32 s), action tick 5**.
   - It also yields **−enemy fire resist = 0** and **+11 to +13 skills**.
   - Unpinned values that move damage include Fire Bolt and Inferno hard points, the Eschuta rolls, and the choice between Eschuta and HotO. Rings, boots and charms are also unpinned.
6. **C-12b: no home margin. The home margin is `DEFERRED`.**
   - No timed LoD 1.13 clear exists for this kit.
   - In 1.13 the kit **cannot damage Uber Diablo**: ResFi(H) 110, items cannot pierce immunity, and the kit has no curse.
   - D2R's skill laws for Fire Ball and Meteor are unchanged, apart from Meteor's delay becoming per-skill, which is inert for this kit. But **Sunder charms (D2R only) change the immunity regime**, so D2R times do not transfer.

---

## 1. Formula list

| Id | Formula | Damage type | Label |
|---|---|---|---|
| H01 | Fire Ball per hit: (EMin + level brackets) << 7 → ×(1 + 14%·(Fire Bolt.blvl + Meteor.blvl)) → ×(1 + M%) | FIRE | MODEL-VERIFIED |
| H02 | Meteor impact: same law, HitShift 8, synergy 5%·(Fire Bolt.blvl + Fire Ball.blvl); radius 6 subtiles = 4 yd at every slvl; impact at action + 60 frames; delay 30 frames from action | FIRE | MODEL-VERIFIED |
| H03 | Pyre: 18 fixed size-2 `meteorfire` missiles. Bit rate per frame = ((15 + brackets 4/5/6/6/6)·(1 + 3%·Inferno.blvl), in whole points) << 3, then + M%. Per overlapping missile per frame; lifetime 30 + 15·(slvl−1) frames (code) or 14 + 15·slvl (Basin); DamageRate 41/1024 scales the defender's flat MDR | FIRE | MODEL-VERIFIED (partial) |
| H04 | Fire Mastery 30 + 7·(slvl−1)%. It is the same stat as item "+% Fire Skill Damage" (they add), and it applies after synergy, to all three components | modifies FIRE | MODEL-VERIFIED |
| H05 | Synergies read hard points only. Prerequisites force Fire Bolt, Fire Ball, Inferno, Blaze and Fire Wall ≥ 1 | modifies FIRE | MODEL-VERIFIED |
| H06 | Fire Ball projectile: Vel 20, Range 50 frames, Size 1, dies on first hit. Explosion of 4 subtiles (2 2/3 yd) centred on the missile, not the target | FIRE | MODEL-VERIFIED (partial) |
| H07 | No to-hit roll (Missiles `ToHit` empty); no block (zero physical) | — | MODEL-VERIFIED (partial) |
| H08 | Monster resist: floor −100, ≥ 100 = immune. Item −res does nothing against immunes; skill −res is cut to 1/5 against them. **The kit has 0 −fire res** | FIRE resist | MODEL-VERIFIED |
| H09 | Mana: 35 + 2/clvl + 2/Energy; regen per frame = floor(max_mana_256/3000)·(100 + Warmth% + item%)/100 (~120 s refill); costs (9 + slvl)/2 and (33 + slvl)/2 | — | MODEL-VERIFIED |
| H10 | Cast cadence (sister packet laws); **shield block EXCLUDED** (fidelity cost) | — | MODEL-VERIFIED |
| H11 | Pointers to the shared J4a laws (F06, F07, F12, F13) | — | MODEL-VERIFIED |

**Corrigendum to the animation packet.** LAW_METEOR reads "damage rate 41/1024 of bit rate per frame". D2MOO copies DamageRate into `STAT_DAMAGE_FRAMERATE` and uses it to **scale the defender's flat DR/MDR** per frame. It does not scale damage. Basin's displayed-DPS formula (bit rate × missiles × 25/256) carries no 41/1024 factor, which agrees. Recorded in H03 as a conflict. The sister packet itself is not edited (corrigenda forward).

## 2. Primary rows: key values

| slvl | FB mana | FB fire (raw) | Meteor mana | Meteor impact fire (raw) | Pyre bit rate /frame/missile (raw, 1/256 pt) | Pyre HP/s per missile | Pyre frames (code) | Fire Mastery % | Warmth % |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 5 | 6–14 | 17 | 80–100 | 120–200 | 11.7–19.5 | 30 | 30 | 30 |
| 20 | 14.5 | 199.5–226.5 | 26.5 | 869–927 | 856–936 | 83.6–91.4 | 315 | 163 | 258 |
| 33 | 21 | 421.5–461.5 | 33 | 1928–2012 | 1480–1560 | 144.5–152.3 | 510 | 254 | 414 |
| 60 | 34.5 | 934.5–1001.5 | 46.5 | 4169–4307 | 2776–2856 | 271.1–278.9 | 915 | 443 | 738 |

"Raw" means no synergy and no mastery. **The kit record uses no levels.** It pins no slvl, clvl or +skills. Its verify-ledger anchor quotes Icy Veins: "20 points to Fire Ball … 20 points to Meteor … 20 points to Fire Mastery". Those are hard points.

⚑ **Rune-name quirk:** 1.13 `Runes.txt` names Chains of Honor "Bound by Duty" in its Rune Name column. It is identified by its runes Dol-Um-Ber-Ist, the same quirk as Grief = "Widowmaker" in J4a.

## 3. Loadout: what the record pins and what it leaves open

**Pinned by the kit record** (`dossier.item_alterations.key_items` and `capstone_alterations`), resolved in the 1.13 tables:

| Slot | Record | 1.13 resolution | FCR | +skills to her fire skills | Other relevant |
|---|---|---|---|---|---|
| Weapon | **Eschuta's Temper** (BIS) **or Heart of the Oak** (alt) | Eschuta: Eldritch Orb `obc`, lvl req 72 · HotO: Runeword51, itypes staf / mace | 40 / 40 | +1–3 Sorceress / +3 all | Eschuta: **+10–20% fire skill dmg**, +20–30 Energy · HotO: +15% mana, no +% fire |
| Shield | **Spirit Monarch** | Runeword130 (swor/shld) | **25–35** | +2 | +89–112 mana, +55 FHR |
| Armour | Chains of Honor | Runeword14 ("Bound by Duty") | 0 | +2 | — |
| Helm | **Flickering Flame** or Harlequin Crest | **Flickering Flame has no 1.13 row** ("D2R only", Basin), so 1.13 takes **Harlequin Crest** (`uap`, req 62) | 0 | +2 | +1.5 mana per clvl |
| Gloves | Magefist | `tgl`, req 23 | 20 | +1 fire skills | **+25% mana regen** |
| Belt | Arachnid Mesh | `ulc`, **req 80** | 20 | +1 | +5% mana |
| Amulet | Mara's Kaleidoscope | req 67 | 0 | +2 | +5 Energy |

**Derived from the pins (INFERRED, from DATAMINED item rows plus the sister FCR law):**
- **FCR = 40 + (25–35) + 20 + 20 = 105–115. That is the 105 breakpoint at every Spirit roll:** 8-tick casts (0.32 s), action tick 5 (0.20 s), for both Fire Ball and Meteor.
  - The next breakpoint (200) needs 85 more FCR. The unpinned slots cannot plausibly reach it.
  - **If Magefist or Arachnid is dropped**, FCR falls to 85–95, which is the 63 breakpoint: 9 ticks.
- **+skills to Fire Ball, Meteor and Fire Mastery:** 11–13 with Eschuta, 13 with HotO.
- **Item "+% to Fire Skill Damage":** 10–20 with Eschuta, 0 with HotO. It adds to Fire Mastery's % (H04).
- **−enemy fire resist: 0.** No named item carries `pierce-fire`, and the kit has no curse or aura.
- **clvl ≥ 80** if Arachnid Mesh is worn (its lvl req 80).
- **HotO base:** the record names none. HotO's itypes are staff or mace. **A staff is two-handed and would forbid the Spirit Monarch shield**, so the record's own pairing implies a one-handed mace-class base. It is still unpinned.

**Unpinned, and whether each value moves her numbers:**

| Unpinned value | Moves damage? | Moves cadence? | Size of effect |
|---|---|---|---|
| **Fire Bolt hard points** (floor 1, max 20) | **YES**: Fire Ball +14%/pt, Meteor +5%/pt | no | Fire Ball synergy 294% → 560% (blvl 1 → 20, with Meteor.blvl 20) |
| Fire Ball, Meteor, Fire Mastery hard points | YES | no | The record quotes 20 each; treated as pinned-by-quote, not by field |
| **Inferno hard points** (floor 1) | **YES**, pyre only, +3%/pt | no | Maxroll maxes Inferno (D2R guide); +3% → +60% pyre |
| **Eschuta +skill roll (1–3)** and **+% fire roll (10–20)** | YES | no | Effective slvl 31–33; mastery + item 250–274% |
| **Eschuta vs HotO** | YES (HotO: no +% fire) | no | e.g. Fire Ball at slvl 33, Fire Bolt 20: 10404–11392 (Eschuta, +20%) vs 9848–10782 (HotO) |
| Rings, boots, charms, jewels (facets), switch (CTA), merc | possibly | possibly (FCR) | **The record names none.** the fire Rainbow Facet exists in 1.13 `UniqueItems.txt` (pierce-fire 3–5, extra-fire 3–5, each), so a facet would add −3 to −5% enemy fire res (non-immunes only) and +3–5% fire skill dmg; none is named |
| clvl, Energy, Warmth hard points (floor 0) | no | no | They move **mana sustain** only (H09) |
| Fire Ball / Meteor rotation policy | — | **YES** | The record says "spam Fire Ball between Meteor cooldowns". At 8-tick casts the delay ends 35 frames after the Meteor cast starts; how many Fire Balls fit is an adapter policy, not data |

Sensitivity rows computed with the verified laws are in `formulas.json` H01/H02 → `sensitivity_examples` (INFERRED).
- Fire Ball per hit ranges from **2067–2347** (no +skills, Fire Bolt 1) to **10404–11392** (Eschuta high roll, Fire Bolt 20).
- Meteor impact ranges from **4685–4998** to **21632–22575**.

## 4. C-12b

See `c12b_home_frontier.md`. **Verdict: SEARCHED-UNLOCATED, so there is no home margin and it is `DEFERRED`.** The re-entry criterion is printed there for the fidelity-cost table.

## 5. Open questions

| # | Question | What would settle it |
|---|---|---|
| Q1 | Is `key_items` a pin (all worn) or a menu? FCR moves from 105 to 63 if Magefist or Arachnid is dropped. Eschuta vs HotO moves damage by about 5% | Matt or the conductor pins the loadout (the J4a Q93 pattern) |
| Q2 | Hard points in Fire Bolt and Inferno; Eschuta's rolls; rings, boots, charms and facets; the HotO base | As Q1 |
| Q3 | Pyre lifetime: 30 + 15·(slvl−1) (code) vs 14 + 15·slvl (Basin); one frame (sister Q5) | Frame-step a 1.13 capture |
| Q4 | DamageRate 41/1024 as an MDR scaler rests on D2MOO alone | 1.13 test against a flat-MDR monster, or read the 1.13 D2Game binary |
| Q5 | Pyre overlap count per target is geometry-dependent (Basin: 3 typical for size 2; up to 6) | gamora: model the 18 offsets, or adopt "3" as a declared simplification |
| Q6 | No named community source for the auto-hit and no-block clauses on these missiles (H07) | Trace D2MOO `sub_6FCF5DE0` (the area-damage callback), or a 1.13 test |
| Q7 | Rotation policy between Fire Ball and Meteor's 30-frame delay | Adapter policy (gamora), declared |
| Q8 | The Patch 3.0 "no Sorceress changes" claim rests on one secondary summary | Official 3.0 notes (Blizzard) |
| Q9 | Shield block is excluded; the kit's Spirit Monarch makes BL reachable at home | Already a named fidelity cost (charter v0.5.1); listed for the table |
| Q10 | 1.13 fire-immune census per J-S7 area (it decides which areas could ever be a home point) | elrond/gamora over MonStats/Levels/MonUMod; not tabulated here |

## Source list (accessed 2026-10-01)

**Primary**
- D2 1.13 txt tables, `fabd/diablo2 @ 45112569`: Skills, Missiles, SkillDesc, SkillCalc, CharStats, ItemStatCost, Properties, UniqueItems, Runes, Levels, MonStats. The local copy is `agentic_orchestration/research/datamine-acquisition/d2/raw/`; sha256s are in `primary_rows.json`.
- D2MOO @ `5596f5cb6c5251a0a07c6637d26458b06099d516`, files read:
  - `D2Common/src/D2Skills.cpp` (elemental damage, level brackets, mastery);
  - `D2Common/src/Units/Missile.cpp` (missile damage, ApplyMastery);
  - `D2Game/src/MISSILES/MissMode.cpp` (SrvHit01 Fire Ball, SrvHit14 Meteor centre, the meteor submissile offsets, SrvDo05, SrvDmg03, the to-hit gate, block call);
  - `D2Game/src/UNIT/SUnitDmg.cpp` (resist and immunity, MDR × DamageRate);
  - `D2Game/src/PLAYER/PlrModes.cpp` (mana regen).

**Secondary**
- The Arreat Summit:
  - Sorceress Fire Spells: https://classic.battle.net/diablo2exp/skills/sorceress-fire.shtml
  - Skills Basics: https://classic.battle.net/diablo2exp/skills/basics.shtml
  - Casting Delays: https://classic.battle.net/diablo2exp/skills/castingdelays.shtml
  - Basics, Characters: https://classic.battle.net/diablo2exp/basics/characters.shtml
- Basin Wiki, https://www.theamazonbasin.com/wiki/index.php?title= with these pages: Fire_Ball, Meteor, Fire_Bolt, Fire_Mastery, Warmth, Inferno, Resistance, Immune, Sunder, Mana, Sorceress class table, Spirit, Heart_of_the_Oak, Chains_of_Honor.
- Blizzard, D2R Patch 2.4 Balance PTR notes: https://news.blizzard.com/en-us/article/23765907/diablo-ii-resurrected-patch-2-4-balance-ptr-has-ended
- Maxroll:
  - Patch 2.4 notes: https://maxroll.gg/d2/news/patch-2-4-notes
  - Fire Ball Meteor Sorceress (S14): https://maxroll.gg/d2/guides/meteor-sorceress
- DiabloBytes, Patch 3.0 notes: https://diablobytes.com/d2-resurrected/news/patch-notes-3-0/

**Tertiary:** the C-12b forum sources, listed in `c12b_home_frontier.md`.

**Project inputs (read-only):**
- `gandalf/notes/2026-09-29-join-1-run-charter.md` (v0.5, plus the v0.5.1 relay from the conductor)
- KC2 ledger KP-160
- `research/curated/kits-export/d2-fire-sorc.json`
- the J4a packet
- the animation packet
