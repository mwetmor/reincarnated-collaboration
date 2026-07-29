# Research — Eye of Reckoning unlock timing (Warlord) — 2026-07-28

**Mode:** A (analytical / primary-source probe)
**Commissioner:** gandalf — feeds the EoR Warlord play-test process doc (KIT-CAL-2 fixture capture)
**Corpus:** `/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/` (depot pulled 2026-07-24,
i.e. **post-v1.3.0.0 / Fangs of Asterkarn**, which launched 2026-07-23)
**Tooling:** `agentic_orchestration/research/scripts/gd_arz_adapter_2026_07_24.py` (`ArzArchive`)
and `…/gd_arc_reader_2026_07_26.py` (`ArcArchive`). Read-only throughout; nothing written to vendor.
**Probes:** `agentic_orchestration/legolas/scratch/2026-07-28-eor/probe{1..18}*.py`

---

## Summary

Eye of Reckoning is **skillTier 6**, and the game engine gates tier 6 at **Oathkeeper mastery bar
level 25** — a value that is *not* on the skill record and *not* on the mastery record, but in
`records/game/gameengine.dbr` as `skillMasteryTierLevel = [1, 5, 10, 15, 20, 25, 32, 40, 50]`
(found by brute-force scan of all 93,190 records across the four archives; §2). Skill-point income
is 3/level for levels 2–50, so **EoR rank 1 is first affordable at character level 10** — where the
27 available points cover exactly `25 bar + 1 Soldier bar + 1 EoR`, and where the separate gate
`masteryIncrementLevel = [1, 10]` first permits a second mastery at all. **At level 12 EoR rank 1 is
comfortably reachable** (33 points; 7 to spare after the minimum). The realistic
*natural-main-attack* point is **level ~15–21** depending on split (§4).

The energy finding is the sharp one. `skillManaCost` on EoR is charged **per tick, not per second** —
and the developer-authored description states the tick is every **0.16 s** at 100% attack speed.
So EoR rank 1 drains **25 energy/second**, against a level-10 pool of ~575 and base regen 1.0/s:
**≈24 seconds of continuous channel from a full bar.** Rank 16 drains 68.75/s; rank 26 drains
100/s. Energy is not a hard block at rank 1, but it is a real pacing constraint from the first
point spent, and it is the reason the practical EoR era arrives later than the arithmetic one.

---

## 1. EoR's own record — measured fields

`records/skills/playerclass09/eyeofreckoning1.dbr`, resident in **GDX2.arz** (Forgotten Gods).
**No GDX3 override exists** — checked all four archives. The v1.3.0.0 EoR buff therefore ships as an
in-place revision of `GDX2.arz`, and this depot (2026-07-24) carries it.

| Field | Value |
|---|---|
| `Class` / `templateName` | `Skill_AttackRadiusSpin` / `skill_attackradiusspin.tpl` |
| `skillTier` | **6** |
| `skillMasteryLevelRequired` | **0** — *not* the gate (see §2) |
| `skillMaxLevel` / `skillUltimateLevel` | 16 / 26 |
| `skillManaCost` | `[4,4,5,5,5,6,6,7,7,8,8,9,9,10,10,11,11,12,12,13,13,14,14,15,15,16]` |
| `timeBetweenAttacks` | 200 (ms) |
| `skillTargetRadius` | 3.0 |
| `distanceProfile` / `canUseWhileMoving` | `Melee` / `True` |
| `weaponDamagePct` | 15 @r1 → 39 @r16 → 50 @r26 |
| `offensivePhysicalMin/Max` | 10–15 @r1 → 85–94 @r16 → 162–182 @r26 |
| `offensiveFireMin` | 10 @r1 → 70 @r16 → 138 @r26 |
| `defensiveCrowdControl` | 10 @r1 → 25 @r26 (the v1.3 CC-resist-while-channelling scaling) |

**Correction worth banking:** `skillMasteryLevelRequired` reads 0 on *every* Oathkeeper skill,
including the tier-9 exclusives. Anyone reaching for that field name as the mastery gate will get a
uniformly wrong answer. The field that matters is `skillTier`.

Full Oathkeeper tier census (from `_classtree_class09.dbr` membership + per-record `skillTier`):
tier 1 = Aegis / Righteous Fervor / passive01; tier 2 = Presence of Virtue; tier 3 = Vire's Might;
tier 4 = Ascension, Judgment; tier 5 = Aegis 3, Vire's Might 2; **tier 6 = Eye of Reckoning,
Judgment 2, Presence of Virtue 3**; tier 7 = Celestial Guardian, RF 3, Ascension 2;
tier 8 = **EoR 2** (`eyeofreckoning2.dbr`, tier 8 — the orbiting-projectile modifier);
tier 9 = Path of the Three, Divine Mandate.

> Note for the fixture: **EoR's own modifier line sits two tiers above it.** `eyeofreckoning2.dbr`
> is tier 8 → mastery bar **40**, i.e. ~level 28 at pure-pump minimum. A "complete" EoR kit is a
> materially later character than a "castable" one.

## 2. Where the tier gate actually lives — and why it took a brute-force scan

The gate is **not** in the skill record, **not** in `_classtree_class09.dbr` (a `SkillTree` record
whose 32 `skillLevelN` fields are all `'0'` — it is a membership list only), and **not** in the
`Skill_Mastery` record `_classtraining_class09.dbr` (whose only relevant field is `skillMaxLevel = 50`).

The UI record `records/ui/skills/classcommon/skills_classpanelconfiguration.dbr` proves the mechanism
exists — it carries `masteryMilestoneNumber1..9` (nine `TextNumber` widgets) and
`masteryMilestoneValueMax = 56` — but the nine widgets are empty text boxes the engine fills at
runtime. `templates.arc` confirms the template declares them with empty `defaultValue`.

I therefore scanned **every record in all four archives** (34,114 + 18,447 + 16,451 + 24,178 =
93,190) for any strictly-increasing length-9 numeric array bounded by 60. Six hits, one live and
five in a developer sandbox archive folder, all identical:

```
records/game/gameengine.dbr   skillMasteryTierLevel = [1, 5, 10, 15, 20, 25, 32, 40, 50]
```

(the five others are `records/sandbox/arthur/archive/gameengine <date>.dbr` — dev backups, same
values, which is corroboration rather than noise.)

**`gameengine.dbr` is base-game only; GDX1/GDX2/GDX3 do not override it.** The thresholds are global
across all masteries and unchanged by any expansion including FoA.

→ **Eye of Reckoning (tier 6) requires Oathkeeper mastery bar level 25.**

Mechanism corroborated in `resources/Text_EN.arc :: tags_ui.txt`:
`YouMustIncreaseMasteryLevel = 'You must increase your Mastery Level to add more points.'`

## 3. Skill-point income and the second-mastery gate

`records/creatures/pc/playerlevels.dbr` (GDX2 override authoritative; GDX3 absent):

- `skillModifierPoints` — 199-entry array, run-length `idx 0..48 → 3`, `idx 49..88 → 2`,
  `idx 89..198 → 1`. Index *i* grants points on reaching level *i+2*; verified because that
  indexing yields exactly **3/level for L2–L50, 2/level for L51–L90, 1/level for L91–L100**, and a
  level-100 total of **237**, the figure the community quotes.
- `initialSkillPoints = 0`, `characterModifierPoints = 1` (attribute point per level),
  `maxPlayerLevel = 100`, `maxDevotionPoints = 55`.
- **Cumulative skill points at level L (L ≤ 50) = 3 × (L − 1).**

Second, independent gate, from `records/creatures/pc/malepc01.dbr` (present identically in all four
archives): **`masteryIncrementLevel = [1, 10]`** — first mastery at character level 1, **second
mastery at character level 10**. A character is not a *Warlord* at all before level 10.

## 4. The arithmetic

**Minimum spend for EoR rank 1 as a Warlord:** 25 (Oathkeeper bar) + 1 (Soldier bar, to be a
Warlord) + 1 (EoR rank 1) = **27 points**.

| Level | Points | Verdict |
|---|---|---|
| 9 | 24 | short by 2 even ignoring the Soldier point |
| **10** | **27** | **exactly enough — and the first level a 2nd mastery is legal at all** |
| 12 | 33 | 6 spare over the Warlord minimum |
| 15 | 42 | |
| 18 | 51 | |
| 21 | 60 | |

**Earliest castable: character level 10.** The two independent gates — 27 points, and
`masteryIncrementLevel[1] = 10` — land on the *same level*. That is almost certainly deliberate
design, and it makes level 10 a clean, non-arbitrary floor to quote.
(As a *pure Oathkeeper*, dropping the Soldier point, the floor is still 10: 26 needed, 24 available at 9.)

**Realistic — the split assumption is mine and is stated so it can be re-run.** Two budgets:

- *Efficient / respec-assisted* — bar 25, EoR 12, Presence of Virtue 5, Soldier bar 1 = **43 points
  → level 15–16.**
- *Natural, unrespecced* — bar 25, EoR 12, Presence of Virtue 5, Soldier bar 10 (stats + Fighting
  Spirit), plus ~8 already sunk into Righteous Fervor while levelling = **60 points → level 21.**

→ **Call it level ~15 at the efficient end, ~21 at the natural end; ~20 is the honest single number
for "EoR is now the main attack."** I did *not* measure EoR-vs-Righteous-Fervor damage crossover, so
this band is a point-budget-and-sustain argument, not a DPS argument. Flagged accordingly.

## 5. The level-12 verdict (werewolf-fixture band)

**Yes — EoR rank 1 is reachable at level 12, and not marginally.** 33 points versus a 27-point
Warlord minimum. It is reachable at 12 *without* pure bar-pumping being a knife-edge: 6 points are
free for Righteous Fervor or Presence of Virtue.

It is **not** reachable at 11 with a normal build (30 points — technically 27 suffices, so 11 also
works with 3 spare) — the real floor is **10**, below which no split works.

Caveat, one direction only: I did not enumerate quest skill-point rewards (GD quests live in `.qst`
files inside map `.arc` containers, outside this probe's scope). Any such reward can only *lower*
the floor, never raise it, and by at most a level.

## 6. Energy — the bonus fact, which turned out not to be a footnote

**`skillManaCost` on a channelled skill is charged per tick, not per second.** Three independent
supports:

1. **Developer text is explicit.** `tagGDX2Class09SkillDescription07A` (from
   `gdx2/resources/Text_EN.arc :: tagsgdx2_skills.txt`) ends:
   *"At 100% Attack Speed, Eye of Reckoning deals damage and drains Energy every 0.16s."*
2. **The tick interval is a measured relation, not a guess.** `timeBetweenAttacks × 0.8` reproduces
   the stated interval on all three channelled skills I checked:
   EoR 200 → 0.16 s ✓ · Flames of Ignaffar 300 → 0.24 s ✓ · Albrecht's Aether Ray 300 → 0.24 s ✓
   (FoI and AAR descriptions state 0.24 s in the same sentence form).
3. **Magnitude band separates cleanly.** Oathkeeper per-cast skills cost 14–32 energy at rank 1
   (Aegis 14, Vire's Might 22, Judgment 30, Ascension 32). Per-*repetition* skills cost 1–4
   (Righteous Fervor 1, EoR 4). EoR sits in the repetition band, not the cast band.

The UI carries both labels — `tags_ui.txt` has `ManaCost = 'Energy Cost'` **and**
`ManaCostPerSecond = 'Energy Cost per Second'` — so the game displays a derived per-second figure
for channels. The stored value is the per-tick one.

**EoR drain at 100% attack speed:**

| Rank | cost/tick | energy/sec |
|---|---|---|
| 1 | 4 | **25.00** |
| 5 | 5 | 31.25 |
| 8 | 7 | 43.75 |
| 12 | 9 | 56.25 |
| 16 (max non-ultimate) | 11 | 68.75 |
| 26 (ultimate) | 16 | 100.00 |

**Against what pool?** Base player (`malepc01.dbr`, identical across all four archives):
`characterMana = 250`, `characterManaRegen = 1.0`. Oathkeeper mastery bar
(`_classtraining_class09.dbr`, GDX2, 100-entry arrays) grants **13 energy per bar point** and
**zero energy regen** (`characterManaRegen = 0.0`). At bar 25 that is +325.

> Level 10 Warlord, bar 25, no Spirit investment, no gear:
> **pool ≈ 575, regen ≈ 1.0/s, EoR r1 drain 25/s → net −24/s → ≈24 s of continuous channel.**

So: **the channel is sustainable at rank 1 in bursts, not as a hold-the-button clearing style.**
24 seconds is enough for pack-to-pack combat with regen between fights, and it degrades fast with
rank (rank 8 → ~14 s; rank 16 → ~8.5 s at the same pool). The practical "EoR era" therefore starts
later than level 10 for **energy** reasons independently of the point-budget reasons in §4 —
it starts when the character has energy sustain (Spirit attribute points, `manaIncrement = 16`
energy per attribute point spent on Spirit, plus gear and leech), not merely when it has 27 skill
points.

**Fixture consequence:** if the KIT-CAL-2 capture is piloted at a low level, expect the channel to
be *interrupted by an empty energy bar*, and expect that to show up in the telemetry as broken
channel segments rather than as a piloting error. Worth declaring before recording, alongside the
devotion state.

---

## 7. Knowledge gaps not resolved

- **Quest skill-point rewards not enumerated** (`.qst` inside map `.arc`, out of scope). Direction of
  error is known: can only lower the level floor.
- **EoR-vs-Righteous-Fervor damage crossover not measured.** The §4 "main attack" band rests on point
  budget and energy sustain, not on a DPS comparison. If gandalf wants the crossover, it is a
  tractable follow-up (both records carry full 26-rank `weaponDamagePct` and flat-damage arrays).
- **`masteryMilestoneValueMax = 56` is unexplained.** The mastery bar caps at 50 (`skillMaxLevel = 50`)
  and the tier table tops out at 50, so 56 is neither. Recorded as an open oddity rather than
  smoothed over.
- **Attribute-point → energy semantics inferred, not proven.** I read `manaIncrement = 16` /
  `intelligenceIncrement = 8` / `lifeIncrementIntelligence = 12` as "one attribute point into Spirit
  gives +8 Spirit, +16 energy, +12 life." The field set is self-consistent under that reading and
  under no other I could construct, but `experiencelevelcontrol.tpl` carries empty descriptions, so
  it is inference. It does not affect §4 or §5; it affects only the §6 sustain-improvement rate.
- **Spirit → energy-regen conversion not found.** `gameengine.dbr` and `combatformulas.dbr` carry no
  such constant; it appears engine-side. The 1.0/s figure above is base regen only and is therefore
  a **floor**, not a full accounting.

## 8. Source list

**Primary — game data, first-hand, this session:**
- `/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/{database,gdx1,gdx2,gdx3}/database/*.arz`
  — 93,190 records total, all four parsed. Accessed 2026-07-28.
  - `records/skills/playerclass09/eyeofreckoning1.dbr` (GDX2)
  - `records/skills/playerclass09/_classtree_class09.dbr`, `_classtraining_class09.dbr`
  - `records/game/gameengine.dbr` (base only) — `skillMasteryTierLevel`
  - `records/creatures/pc/playerlevels.dbr` (GDX2), `records/creatures/pc/malepc01.dbr`
  - `records/ui/skills/classcommon/skills_classpanelconfiguration.dbr`
  - `records/skills/playerclass07/purifyingflame1.dbr`, `records/skills/playerclass05/aetherray1.dbr`
    (channel-convention triangulation)
- `/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/gdx2/resources/Text_EN.arc` and
  `resources/Text_EN.arc` — `tagsgdx2_skills.txt`, `tags_ui.txt`
- `/Users/admin/Games/vendor/grim-dawn/database/templates.arc` (Edition-I install, 819 templates) —
  `skill_attackradiusspin.tpl`, `SkillChanneled.tpl`, `ingameui/skillpanebase.tpl`,
  `experiencelevelcontrol.tpl`

**Primary — project substrate:**
- `agentic_orchestration/legolas/notes/2026-07-28-gd-iconic-build-shortlist.md` §C2 (the join key)
- `agentic_orchestration/research/scripts/gd_arz_adapter_2026_07_24.py`,
  `agentic_orchestration/research/scripts/gd_arc_reader_2026_07_26.py`

**Nothing secondary was needed.** Every number in §§1–6 is read from the shipped data or from
developer-authored in-game text. No community source was consulted, and none was required.
