# Research — Grim Dawn iconic-build shortlist (KIT-1 candidate set) — 2026-07-28

**Mode:** A (analytical)
**Commissioner:** gandalf (RUN-CONDUCTOR), per ruling R-KC1-5 / grill item 5 in
`agentic_orchestration/gandalf/notes/2026-07-27-kit-cal-1-run-charter.md` §4.5
**Lane:** parallel, **non-gating** to the KIT-CAL-1 run (charter §3)
**Status:** DELIVERED — decision-shaped. **The pick is Matt's.** Nothing below pre-commits it.

---

## Summary

Eight candidates are scored below on canon-fame × RDR-archetype-need × v2-recordability. Four
findings shape the whole set. **(1) Fangs of Asterkarn is five days old** — it launched
2026-07-23 with patch v1.3.0.0, so *no* FoA-native build has canon yet; the community's own
theorycraft thread says its listings "can be either top20 material or not work at all." Every
canon-fame score here is therefore **1.2-era canon re-graded against the v1.3.0.0 patch notes**,
and I say per candidate which way 1.3 pushed it. **(2) The corpus agrees but is also pre-FoA** —
all 41 `canon_corpus` GD rows carry `eras` terminating at `patch-1.1-1.2`; none has an FoA era tag.
**(3) One unknown gates three candidates:** whether the OCR rig's `skill_use_count` increments
per *activation* or per *tick* for a channelled skill is unresolved, and it decides the
instrumentation quality of Eye of Reckoning, Flames of Ignaffar, and Albrecht's Aether Ray alike.
A ~60-second in-game probe closes it (§6). **(4) Retaliation is off the table on sim grounds, not
canon grounds** — the string `retaliation` appears nowhere in `src/reincarnated/simulation/*.py`;
calibrating a retaliation build would have nothing to be accountable to (§5).

On the corpus-privileged kit: `gd-flames-of-ignaffar-purifier` **deserves candidacy but not
automatic top billing**, for a reason that is about its *canonical form* rather than its channel
mechanics — the top-20-grade FoI build is the **RtA (retaliation-to-attack)** variant, which is
doubly un-instrumented (§C3).

**Top-2 recommendation: C2 Eye of Reckoning Warlord + C6 Cadence Witchblade / Krieg Death Knight**,
with named swaps for two different strategic preferences (§7).

---

## 1. What the calibration kit already exercises (the baseline the shortlist must extend)

Confirmed first-hand against the Edition-II `.arz` (`gdx3/database/GDX3.arz`, 24,178 records,
1,858 `playerclass` skill records — Berserker is `playerclass10`):

| Werewolf-kit component | Record | Template | Ranks |
|---|---|---|---|
| Werewolf (the transform) | `playerclass10/werewolf1.dbr` | `Skill_Shapeshift` | 16 / 26 |
| Claws | `playerclass10/werewolf1_skill01_claws.dbr` | **`Skill_AttackWeapon`** | 16 / 26 |
| Charge | `playerclass10/werewolf1_skill02_charge.dbr` | (gap-close) | 16 / 26 |
| Onslaught | `playerclass10/onslaught1.dbr` | `Skill_WeaponPool_BasicAttack` | 16 / 26 |
| Default attack | `records/skills/default/defaultweaponattack.dbr` | — | — |

**The load-bearing consequence:** claws is `Skill_AttackWeapon`, which is *the same template as
Blade Arc*. So the calibration kit already covers instant, weapon-damage, melee, self-transform-buff,
gap-close, and basic-attack-pool. **Blade Arc adds no template the fixture does not already hold** —
which is why the widely-canonical Blade Arc builds (`gd-blade-arc-warder`, Physical 2H Blade Arc
Death Knight, #14 in the Top-20) are *not* in the shortlist below despite strong canon.

Families **not** exercised, ranked by how much the sim can actually be held to them:

| Family | RDR sim support (evidence) | Gap size |
|---|---|---|
| **sustained channel** | modelled + has calibration history — `gauntlet_lived_channel_repilot_driver.py`, `math/step3-lived-channel-calibration-repilot-2026-07-07.md`, `commit_val='channel'` BC axis | **large** |
| **DoT-stacking** | modelled — `effect_resolver.py`, `dot_activation_phase3_harness_2026_06_20.py`, `dot_mitigation_symmetry_arm{b,c}_harness_2026_06_20.py` | **large** |
| **pure-spell (non-weapon) damage + energy economy** | modelled — resource-economy is a BC axis | **large** |
| **charged-finale / every-Nth-hit amplitude spike** | modelled — "damage amplitude variance" BC axis (flat/spiky/var); werewolf kit is flat | medium |
| **projectile / drop / wave geometry** | modelled — `AOE_GEOMETRIES` in `damage_resolver.py` | medium |
| **pet / summon (player-side proxy)** | **being built** — Matt ruled Option 1 on 2026-07-06 (`canonical/matt_decision_needed/2026-07-03-w3-summoner-emission-structural-gap.md`); `damage_resolver.py`'s only proxy term is `defender.pack_proxy_size`, i.e. *enemy* packs | **large, rising** |
| **retaliation** | **absent** — zero hits for `retaliation` in `src/reincarnated/simulation/*.py`; nearest analogue is defender-side `damage_taken_converts_shape == "reflect-damage"` (`_apply_wavec_th_reflect`, `WAVEC_REFLECT_MAX_FRACTION = 1.00`, chain-depth 0) | n/a — see §5 |

## 2. What the OCR telemetry rig can and cannot see

From the KIT-CAL-1 substrate: the rig reads GD's **`game.PlayStats`** panel, and its per-skill
series are keyed by `.dbr` record path — `measure_key='skill_use_count'`,
`measure_subkey='records/skills/…'` (`research/scripts/fixtures_m6_gp_run01_ingest_2026_07_26.py`,
`fixtures_m5_v0_3_schema_2026_07_26.py`). Instrument validation on the werewolf run was clean:
`kills` 0 non-monotonic rejections, per-skill counters 0 rejections, `life_healed` 3.1%
(the efficacy verdict §1).

Three legibility classes follow, and they drive the recordability axis:

- **Legible (best case).** A skill the player presses, one activation at a time. One press → one
  counter increment. Attack-*replacers* (Cadence, Fire Strike, Savagery, Righteous Fervor,
  Onslaught) are the densest of all, because the counter accrues per auto-attack swing.
- **Unresolved.** Channelled skills. The counter's tick-vs-activation semantics are **not
  established by any artifact I could find**, and the answer differs by an order of magnitude in
  sample density. Note the corpus already banks `foi_tick_interval_sec` as a `kit_numeric` row, so
  the tick exists on the source side — what is unknown is whether the panel counts it.
- **Illegible.** Damage that originates without a player skill activation. This is
  **pet damage** (attributed to the pet, not the player) and **retaliation damage** (reactive, no
  activation at all). `kills`, `deaths`, `play_time`, and `life_healed` still accrue, so a
  TTK/intake fixture remains *possible* — but the rig would measure such a build's **outcome and
  none of its cause**.

## 3. GD Stash constructability — viable, and current

The accepted endgame-construction path works and is up to date for the current build:

- Method: create the character, close GD, use GD Stash to grant XP, restart, kill one mob to
  resolve to level 100; the **Char Editor** tab clears/reassigns skill points; items are granted
  from the stash ([Crate forum: "How to create authentic level 100 character using GD stash?"](https://forums.crateentertainment.com/t/how-to-create-authentic-level-100-character-using-gd-stash/125121)).
- **Version currency confirmed:** GD Stash 1.8.2a added support for the 1.3.0.0 save-file formats
  and for Fangs of Asterkarn ([GD Stash, Nexus mod 2](https://www.nexusmods.com/grimdawn/mods/2)).
  This was a real risk worth checking — the expansion is five days old.
- Alternative: pre-built endgame saves exist ([Nexus mod 213](https://www.nexusmods.com/grimdawn/mods/213)).
- **Standing caveat for every candidate:** devotion state is a separate axis from level and gear.
  The play-test-v1 fixture already carries an UNVERIFIED devotion-points claim (verdict §9), and
  the charter's grill item 4 `.gdc` save probe is the instrument that would settle it. Whatever
  KIT-1 is, its devotion tree should be **declared before recording**, not reconstructed after.

---

## 4. Candidate scorecards

Scores are 1–5. Axis definitions: **CF** = canon-fame (community canonisation, longevity across
patches, name recognition — evidence-weighted). **AN** = RDR archetype need (coverage of a family
the werewolf kit misses, discounted where the sim cannot be held accountable to it).
**REC** = v2-recordability (Stash constructability + pilot difficulty + OCR legibility).

---

### C1 — Forcewave Warlord (physical, two-hander)
*A two-hander smashes the ground and a cone shockwave rolls out through the pack. One button, one press, one wave.*

- **CF 5.** #7 in the Top-20 Softcore list — *"very strong and consistent farmer with very few
  vulnerabilities."* `canon_tier=deep` in corpus (`gd-forcewave-warlord`, eras `fg-2019;patch-1.1-1.2`).
  **v1.3.0.0 buffed it directly**: Forcewave *"increased % Weapon damage scaling with rank to 315%
  by rank 16, 465% by max ultimate rank."* This candidate is favoured, not merely survived, by FoA.
- **AN 3.** New geometry (projected wave/cone) — but still instant, weapon-damage, physical. It
  extends the geometry axis, not the damage-resolution family.
- **REC 5.** One press = one counter increment. Common Soldier/Oathkeeper physical gear, trivial to
  Stash. Pilot difficulty low.
- **.arz confirmed:** `records/skills/playerclass01/shieldhammer1.dbr` → `Skill_AttackWave`, 16/26.
  (Note the internal record name is a legacy artifact — `shieldhammer` is Forcewave, identified by
  template and by the `records/fx/skillclass01/forcewave*` FX family. Worth banking, because a
  naive name-keyed lookup for `forcewave` returns nothing.)

### C2 — Eye of Reckoning Warlord ("Gutsmasher")
*Hold the button and the character becomes a walking blender; everything inside melee radius dissolves while you keep moving.*

- **CF 5.** #2 in the Top-20 Softcore list — *"the best channelling skill boosted by all the perks
  of the best dmg type."* `canon_tier=deep` (`gd-eor-warlord`). **v1.3.0.0 buffed it**: weapon
  damage and CC-resist scaling increased, *plus defensive benefits added while channelling*.
- **AN 5.** Two named gap families in one kit: **sustained channel** and **aura-melee proximity
  AoE**. And a methodological gift the others lack — EoR is **weapon-based**, so it isolates
  channel mechanics from a whole new damage model. When the run misses, the §0 honorable-fail
  decomposition (source-mapping vs sim-mechanics vs fixture-measurement) stays clean, because the
  weapon-damage path is already validated by the werewolf fixture.
- **REC 4.** Stash-constructable; pilot is "hold button and walk," the easiest on the list. Carries
  the §6 channel-counter unknown — **but degrades gracefully**: even if `skill_use_count` proves
  useless for channels, EoR's kills-per-engagement and TTK series remain fully legible, because
  a melee-radius channel kills what it touches when it touches it.
- **.arz confirmed:** `records/skills/playerclass09/eyeofreckoning1.dbr` → `Skill_AttackRadiusSpin`, 16/26.

### C3 — Flames of Ignaffar Purifier
*Hold the button and pour a short cone of fire; packs melt at four metres.*

- **CF 4.** In Nery's maintained list at 1.2.1.6 (#11, *"FoI RtA Purifier"*); a community build
  video is titled *"SC 'TOP 20' — Patch 1.2.1.6."* Forum guides span **1.1.7.2 (2020) → 1.2.0.2
  (2024)** — genuine cross-patch longevity. GrimTools carries **49 builds** under the skill.
  `canon_tier=deep`. Scored 4 not 5 because its top-20-grade form is a hybrid (below).
- **AN 4.** Channel + cone + fire. Real coverage, but it **competes for the same channel slot as
  C2 and C4** — picking two channels buys one family twice.
- **REC 2.** The problem is the *canonical* variant. **RtA = retaliation-to-attack**: a large share
  of its damage originates from a retaliation stat, which the rig cannot see (§2) and the sim does
  not model (§5). Nery's own note on it: *"Retal unsuitable for leveling."* A non-RtA conversion
  Purifier (e.g. the 1.1.7.2 "fire ConeMan") is recordable — but it is the *less* canonical build,
  so choosing it trades away part of the reason for picking FoI at all.
- **Corpus privilege — real, and worth stating precisely.** FoI is the **only** GD kit with numeric
  depth: **26 `kit_numeric` rows** and the **only `exact_skill` GD row** —
  `purifyingflame1.dbr`, `Skill_AttackSpellCone`, `rank_count=26`, `fidelity_grade=MEASURED`,
  `fidelity_basis=primary-source-datamine`, display name confirmed against the authoritative
  `Text_EN.arc` tag `tagGDX1Class07SkillName04A`. It is by a wide margin the cheapest kit to **spec**.
- **Does it deserve top billing? My read: no — but the counter-argument is real and Matt should see
  both.**
  - *For:* the byte-match certificate drives **source-mapping error toward zero**, and source-mapping
    error is one of the three terms the §0 honorable-fail decomposition must separate. Nulling one
    term makes the other two easier to read. That is a genuinely strong argument.
  - *Against:* its canonical form is retaliation-hybrid — doubly un-instrumented on a rig that
    cannot see retaliation and a sim that does not model it. And C2 gets you the *same* channel
    family with a *cleaner* isolation property (weapon-based, so the damage model is already
    validated) at higher canon rank (#2 vs #11) and with 1.3 tailwind rather than silence.
  - *Disposition:* **strong fallback, not headliner** — specifically, the pick to make if the §6
    channel probe comes back favourable **and** Matt wants source-mapping error minimised above
    all else.

### C4 — Albrecht's Aether Ray Spellbinder
*A continuous aether beam that pierces everything in a line. You stand still and things stop existing.*

- **CF 5.** The signature Grim Dawn caster. `canon_tier=deep`, and the **longest era string among
  the caster rows** (`aom-2017;fg-2019;patch-1.1-1.2`). "Clairvoyant Spellbinder" is #21 in Nery's
  1.2.1.6 list. **Spellbinder is S-tier in the only FoA-aware tier list I found (dated 2026-07-27).**
  The corpus already holds five `kit_dossier` rows for it with anchor quotes from Nery's 1.1.9.3
  beginner guide.
- **AN 5.** The widest extension on the list: **channel** + **pure spell damage, no weapon
  component at all** + **piercing-line geometry** + **energy-economy pressure** (the corpus's own
  anchor quote: *"AAR is also pretty energy hungry skill, that's the main challenge"*) — and
  resource economy is a live BC axis the werewolf kit does not touch.
- **REC 3.** Stash-constructable, but caster gear is more set-dependent than physical melee. Pilot
  is easy to execute and fragile to survive — it is a **rooted** channel, so deaths happen and the
  fixture inherits death-clock breaks (the werewolf run already showed dying costs wallclock the
  game does not count). Carries the §6 channel unknown, **without** FoI's retaliation confound —
  100% of its damage is spell-side and reads straight off the `.arz`.
- **.arz confirmed:** `records/skills/playerclass05/aetherray1.dbr` → `Skill_AttackSpellBeam`, 16/26.

### C5 — Primal Strike Warder / Vindicator
*A lightning-charged overhead smash that cracks in a radius. The loudest, flashiest button in the game.*

- **CF 5.** Highest raw name recognition of anything here. Beginner compendium entry
  *"Lightning | Ranged Primal Strike | Vindicator | 1.2.1.5 | HonorabruS."* Nery's #1 leveling
  entry (Dawnbreaker Warder) instructs *"swap to Primal Strike early."* **Warder is #1 in the
  FoA-aware 2026 tier list** — *"the best class in 2026 because you can do pretty much any type of
  endgame content even with average items."* `canon_tier=deep`. v1.3.0.0 touched only an item
  modifier (Mythical Ultos' Stormseeker), not the skill.
- **AN 2 — and this is the honest score.** Instant, weapon-based, melee-radius: it is the closest
  thing on this list to a *replicate* of the werewolf kit. Its one genuine extension is the
  **ranged Vindicator variant** (`range_val` melee → ranged). Its real value is as a **control** —
  the near-replication check that asks whether the harness reproduces a build *adjacent* to the
  calibration kit before being asked to reproduce a distant one.
- **REC 5.** The best on the list. One press, one counter. Both variants Stash cleanly. Lowest
  pilot difficulty (*"easier in every way," "beginner friendly, flashy and fun"*).
- **.arz confirmed:** `records/skills/playerclass06/savagestrike1.dbr` → `Skill_AttackWeaponRadius`,
  16/26. (Second legacy-name trap banked: Primal Strike's record is `savagestrike`, and `savagery`
  is a *different* skill at `savagery1.dbr`.)

### C6 — Cadence Witchblade / Krieg Death Knight
*Two ordinary swings, then the third one detonates. Grim Dawn's oldest signature rhythm.*

- **CF 5.** Cadence is the Soldier's tier-1 skill and the most recognisable mechanic in the game —
  the thing a new player's first character does. Beginner compendium carries *"Fire | 2H Cadence |
  Commando | HC 1.2.1.6."* Corpus holds **two** deep-tier Cadence kits (`gd-cadence-witchblade`,
  `gd-krieg-death-knight` — the latter also runs Bone Harvest, which v1.3.0.0 buffed hard).
  v1.3.0.0 improved Cadence item support (Valdun's Betrayal / Valdun's Bounty).
- **AN 3.** The **charged-finale** family: an every-Nth-hit amplitude spike. This maps directly onto
  RDR's "damage amplitude variance" BC axis (flat / spiky / var), where the werewolf kit sits at
  *flat*. Genuinely new on the tempo and amplitude axes; overlapping on the damage model.
- **REC 5 — the highest sample density available.** Because Cadence rides the default attack, its
  `skill_use_count` accrues **per swing**, not per deliberate press. That is a direct answer to the
  R2 fixture's stated weakness: 106 engagements sits *at the floor* of the 100–250 target band, and
  per-kill attack cost was declared **not recoverable** (verdict §5, the named field covered 4.9% of
  kills). An attack-replacer build restores exactly that series. Trivial to Stash; very low pilot
  difficulty.
- **.arz confirmed:** `records/skills/playerclass01/cadence1.dbr` → `Skill_WeaponPool_ChargedFinale`, 16/26.

### C7 — Vitality Conjurer (Sigil of Consumption + Bloody Pox + Wendigo Totem)
*You paint the ground with a sigil, spread a plague, plant a totem, and walk away while everything rots.*

- **CF 4.** `canon_tier=deep`, and it carries the **longest era string of any GD row in the corpus** —
  `base-2016;aom-2017;fg-2019;patch-1.1-1.2`, i.e. all four eras. **Conjurer is S-tier in the
  FoA-aware 2026 tier list.** Scored 4 rather than 5 because it is a durable *lineage* rather than a
  ranked top-20 *build*; v1.3.0.0's Wendigo Totem cooldown cut (to 4s) is a tailwind.
- **AN 5.** Three families off the werewolf kit at once — **DoT-stacking**, **ground-placement /
  drop geometry**, and **light proxy** (totem). RDR models DoT explicitly and has dedicated
  mitigation-symmetry harnesses for it, so there is real machinery to be accountable to.
- **REC 4.** Instant presses, clean per-cast counters. The catch is interesting rather than
  disqualifying: **TTK becomes DoT-lagged**, and kills arrive after the player has stopped acting.
  That is harder for engagement segmentation — and it is *precisely* the stress test that would
  expose a bad grain choice at HALT H-1. If Matt wants the segmentation rule pressure-tested rather
  than merely applied, this is the candidate that does it.
- **.arz confirmed:** `playerclass03/sigilofdestruction1.dbr` → `Skill_AttackProjectileAreaEffect`
  (12/22); `playerclass03/pox1.dbr` → `Skill_AttackBuff`. Note Bloody Pox has **no
  `skillMaxLevel`/`skillUltimateLevel` fields** — a rank-axis shape the FoI adapter's
  `rank_axis_source` convention has not yet had to handle.

### C8 — Pet Cabalist / Skeleton Ritualist
*You summon a warband and become its manager. The pets do the killing.*

- **CF 4.** Pets are a canonical GD pillar — *"Conjurer and Cabalist are the best pet classes."*
  Corpus holds `gd-pet-conjurer` and `gd-skeleton-ritualist`, both `canon_tier=deep`. v1.3.0.0
  buffed pets broadly (summoned pets no longer consume energy; life-leech resist to 60%). Scored 4,
  not 5, on a specific documented limit: the Top-20 authors state plainly that **no pure pet build
  made their list**, and attribute this to their own lack of pet expertise. The canon is broad but
  deliberately unranked.
- **AN 5, and rising.** Player-side proxy is the largest single hole. Matt ruled **Option 1** on
  2026-07-06 — build the summon gen-path and re-fire summoner emission as registered batch 2 — so
  RDR is actively acquiring this family. An external ground-truth fixture for proxy-heavy kits will
  be wanted; the question is timing.
- **REC 1.** The rig would see the outcome and none of the cause. Pet damage carries no player-side
  activation, so `skill_use_count` collapses to "how many times you re-summoned." Kills, deaths and
  `life_healed` still accrue, so a TTK/intake fixture is technically obtainable — but the run's
  §0 promise is a *decomposed* miss, and a pet build offers nothing to decompose with. Pet leveling
  is also the hardest to Stash-shortcut cleanly (Nery flags pet leveling as a difficulty on two
  separate entries).
- **Disposition:** the right candidate for a **later** lap — after the summon gen-path lands, and
  after the rig has a pet-side counter story. Recording it now buys an outcome series the sim
  cannot yet be held to.

---

## 5. Named non-candidate — Retaliation (Acid RtA Aegis Sentinel / Retaliation Warlord)

Stated out loud so the omission is deliberate rather than an oversight, per the commission's
explicit request that retaliation be considered as a family.

- **Canon-fame would score 5.** #4 in the Top-20 Softcore list — *"the strongest retaliation build
  with good clearspeed."* `gd-retaliation-warlord` is `canon_tier=deep`. **v1.3.0.0 buffed
  Counter Strike** (activation chance, weapon damage, and retaliation scaling all increased), and
  buffed Oathkeeper's Heart of Wrath retaliation scaling. By canon alone it belongs on any iconic list.
- **It is excluded on sim grounds.** `retaliation` does not appear in
  `src/reincarnated/simulation/*.py`. The nearest RDR analogue is a **defender-side** mechanic —
  `damage_taken_converts_shape == "reflect-damage"` in `damage_resolver.py::_apply_wavec_th_reflect`
  (`WAVEC_REFLECT_MAX_FRACTION = 1.00`, §I12 LOCKED, §I13 chain-depth 0). That is a monster/TH-kit
  reflect, not a player build archetype. **A calibration kit needs something on the sim side to be
  accountable to; this one has none.**
- **And it is the worst-instrumented build in the game for this rig.** Retaliation damage is
  reactive — there is no activation to count. `.arz` confirms Counter Strike is
  `Skill_OnHitAttackRadius` (`playerclass01/counterstrike1.dbr`, 16/26): a proc, not a press.
  Nery: *"Retal unsuitable for leveling."* Gear-gated hard on specific retaliation sets.
- **Ruling: do not shortlist.** If retaliation ever becomes an RDR family, revisit — the canon will
  still be there.

Also considered and set aside, with reasons, so the search is auditable:

| Set aside | Reason |
|---|---|
| Blade Arc Warder / Physical 2H Blade Arc Death Knight (#14 Top-20) | `Skill_AttackWeapon` — **identical template to werewolf claws** (§1). Strong canon, **zero** archetype extension. |
| Savagery Avenger Archon / Warder (#1 and #12 Top-20) | `Skill_WeaponPool_ChargedScaling` — an attack-replacer like C6, but C6 (Cadence) has strictly higher name recognition and the same instrumentation profile. C6 dominates it. |
| Trozan's Sky Shard Druid | `canon_tier=deep`, three-era longevity, and a clean drop-geometry extension — but **v1.3.0.0 nerfed it** (target radius reduced to 3.6), so its canon status is actively in motion. Revisit after the meta settles. |
| Drain Essence Spellbinder / Blightlord Oppressor | Excellent channel candidates, but **v1.3.0.0 reduced Drain Essence's aether scaling**; C2/C4 give the same family with tailwind instead of headwind. |
| Berserker wereform builds (Primalist / Reaver / Thane / Veilwalker / Zealot etc.) | These are the FoA-native combos, five days old, explicitly *"theorycraft… can be either top20 material or not work at all."* Also the *closest* archetype to the calibration kit — near-zero extension. `gd-berserker-wereforms` sits in corpus with `core_skills = ["wereform suite(TBD)"]`, i.e. the corpus itself has not resolved it. |

---

## 6. The one unknown that should be closed before the pick is executed

**Question:** does the `game.PlayStats` panel's per-`.dbr` `skill_use_count` increment **once per
channel activation** or **once per channel tick**?

**Why it matters:** it is the single input that separates REC 4 from REC 2 for C2, C3 and C4
simultaneously — three of the eight candidates, and the entire channel family.

**Probe (cheap, non-gating, ~60 seconds of play):** load *any* character with any channelled skill,
enable the PlayStats panel, note the counter, channel continuously for ~10 s against nothing, note
it again. Activation-counting → the counter reads +1. Tick-counting → it reads +N, and N/10 should
land near the source-side tick interval (the corpus already banks `foi_tick_interval_sec` for FoI,
giving an immediate cross-check). This does not require the KIT-1 character to exist yet, does not
touch the KIT-CAL-1 run, and can be done on the existing werewolf save with any borrowed channel.

**Second, smaller unknown, worth one line in the same session:** whether an *attack-replacer's*
counter increments per swing (as the werewolf run's `onslaught` / `defaultweaponattack` series
suggest) or per held-mouse press. C6's REC 5 rests on the per-swing reading. The werewolf evidence
is strongly consistent with per-swing — `defaultweaponattack` climbed **one at a time**, 61→74
across `play_time` 1019–1134 (verdict §C-2) — but that is inference from a default attack, not a
direct confirmation on a replacer.

---

## 7. Ranked table and recommendation

Equal weights across the three axes. **The weighting is mine, not ratified — reweight it and the
order moves.** A recordability-first ordering (the ordering implied by KIT-1's job of producing a
*measured* v2 fixture) is given in the last column.

| # | Candidate | CF | AN | REC | Σ | Family added | REC-first rank |
|---|---|:--:|:--:|:--:|:--:|---|:--:|
| **C2** | **Eye of Reckoning Warlord** | 5 | 5 | 4 | **14** | channel + aura-melee | 3 |
| **C1** | Forcewave Warlord | 5 | 3 | 5 | **13** | wave/cone geometry | 1= |
| **C4** | Albrecht's Aether Ray Spellbinder | 5 | 5 | 3 | **13** | channel + pure-spell + energy economy | 6 |
| **C6** | **Cadence Witchblade / Krieg DK** | 5 | 3 | 5 | **13** | charged-finale amplitude spike | 1= |
| **C7** | Vitality Conjurer (Sigil/Pox/Totem) | 4 | 5 | 4 | **13** | DoT-stacking + ground-place + light proxy | 4 |
| **C5** | Primal Strike Warder / Vindicator | 5 | 2 | 5 | **12** | (control — near-replicate; ranged variant) | 1= |
| **C3** | Flames of Ignaffar Purifier | 4 | 4 | 2 | **10** | channel + cone (corpus-privileged) | 7 |
| **C8** | Pet Cabalist / Skeleton Ritualist | 4 | 5 | 1 | **10** | pet / player-side proxy | 8 |
| — | *Retaliation Sentinel / Warlord* | *5* | *—* | *1* | *—* | **excluded, §5** | — |

### Top-2 recommendation — **C2 Eye of Reckoning Warlord + C6 Cadence Witchblade / Krieg Death Knight**

The reasoning is a hedge, and the hedge is the point.

**C2 is the strongest single candidate on the merits.** It is #2 on the community's own top-20
list, it was *buffed* by the five-day-old patch rather than merely spared, and it buys the largest
modelled gap (sustained channel) plus a second family (aura-melee proximity AoE) in one kit. Most
importantly it buys them **weapon-based**, which means when the harness comparison misses, the miss
decomposes cleanly — the weapon-damage path is already validated by the werewolf fixture, so
residual error localises to the channel mechanics rather than smearing across an unfamiliar damage
model. That property is worth more to a *calibration* kit than raw archetype distance.

**C6 exists in the pair to cover C2's one exposure.** Both C2's and C6's value depend on
`skill_use_count`, but they fail differently: if the §6 probe returns badly for channels, C2
degrades (TTK and kills survive; per-skill attribution weakens) while **C6 is unaffected and in
fact improves the fixture** — an attack-replacer restores the per-swing series the R2 fixture
explicitly could not recover (verdict §5: per-kill attack cost not recoverable, named field covered
4.9% of kills). C6 also lands the highest-recognition skill in the game and a genuinely new
amplitude shape, at the lowest pilot difficulty and Stash cost on the list. Pairing a
*new-family-with-instrument-risk* against a *known-good-instrument-with-high-sample-density* means
the lap produces a usable measured fixture under either probe outcome.

**Named swaps, so the pick stays Matt's:**

- **Want maximum coverage extension over hedging → swap C6 for C4 (Aether Ray Spellbinder).**
  C2+C4 is the highest-ceiling pair on this list: channel, pure spell, energy economy, piercing
  line, and an S-tier FoA-aware class. The cost is that both halves ride the *same* unresolved
  channel-counter unknown — you would be betting twice on one coin. Only take this pair *after*
  the §6 probe returns favourably.
- **Want source-mapping error driven toward zero → swap C2 for C3 (Flames of Ignaffar Purifier).**
  Its 26 `kit_numeric` rows and byte-match `exact_skill` certificate null one of the three error
  terms in the §0 honorable-fail decomposition outright. Accept in exchange that its canonical
  form is retaliation-hybrid and its non-RtA form is the less canonical build.
- **Want the segmentation grain stress-tested rather than assumed → add or swap in C7
  (Vitality Conjurer).** Its DoT-lagged kills are the sharpest available probe of whatever
  engagement grain gets ruled at HALT H-1.
- **Want a near-replication control before attempting distance → C5 (Primal Strike Warder).**
  Cheapest possible lap, lowest information yield, highest probability of a clean PASS. Legitimate
  if the goal is to de-risk the *harness* before de-risking the *coverage*.

**Not recommended for this lap:** C8 (pet) until the summon gen-path from the 2026-07-06 Option-1
ruling lands and the rig has a pet-side counter story; retaliation at all, per §5.

---

## 8. Knowledge gaps not resolved

- **Per-skill build counts across GrimTools could not be systematically harvested.** GrimTools'
  `/builds/skill/<id>` pages do expose a total (Flames of Ignaffar = 49), which would have made an
  excellent quantitative canon-fame metric — but `grimtools.com/robots.txt` carries
  `User-agent: ClaudeBot → Disallow: /` and `User-agent: Claude-User → Disallow: /`. I stopped and
  deleted the one page I had already pulled to disk. **Canon-fame here therefore rests on the
  curated forum lists (Top-20 Softcore 2022; Nery's Top-20/21 leveling list at 1.2.1.6, Feb 2026;
  the Beginner Compendium at 1.1.9.0–1.2.1.6) plus the corpus's own `canon_tier`** — a
  qualitative-but-authoritative basis rather than a counted one. If Matt wants counted popularity,
  it needs a human-driven pull or a licensing conversation, not an agent crawl.
- **No FoA-native canon exists yet.** Five days post-launch. Every canon-fame score above is
  1.2-era canon re-graded against v1.3.0.0 patch notes. If KIT-1 is meant to be iconic *in the
  current meta*, that meta does not exist yet and will not for months. My read is that this argues
  *for* the durable pre-FoA canon rather than against it — a build canonised across four eras is a
  better join key than one canonised for five days — but that is a judgement, and it is Matt's.
- **The channel `skill_use_count` semantics** (§6) — the one gap I would close before executing.
- **WebFetch summarisation is unreliable on class-combo attribution.** Fetched summaries of the
  Crate forum threads mis-assigned masteries on several rows (e.g. rendering Oppressor as
  Shaman/Occultist rather than Necromancer/Oathkeeper). **I have relied on build *names*, *core
  skills*, and *rank positions* from those threads — never on their fetched class-combo columns.**
  Build-name and rank data agreed across two independent threads plus corpus rows.
- **Not investigated:** exact gear/set requirements per candidate, devotion trees, or GD Stash
  step-by-step construction per build. Those belong to whichever kit is picked, not to the shortlist.

---

## 9. Source list

**Primary — game data (local, first-hand):**
- Edition-II `.arz` extraction, `/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/`
  (`database.arz` 34,114 rec · `GDX1.arz` 18,447 · `GDX2.arz` 16,451 · `GDX3.arz` 24,178), read via
  `agentic_orchestration/research/scripts/gd_arz_adapter_2026_07_24.py`. Accessed 2026-07-28.
- `agentic_orchestration/research/curated/corpus.db` — `canon_corpus` (41 gd rows), `kit_numeric`
  (26 gd rows, all `gd-flames-of-ignaffar-purifier`), `exact_skill` (1 gd row), `kit_dossier`.

**Primary — project substrate:**
- `agentic_orchestration/gandalf/notes/2026-07-27-kit-cal-1-run-charter.md` (the commission)
- `agentic_orchestration/gandalf/notes/2026-07-26-gd-playtest-v1-efficacy-verdict.md` (§1, §5, §C-2)
- `agentic_orchestration/research/scripts/fixtures_m{2,3,5,6}_*_2026_07_26.py` (rig field semantics)
- `reincarnated-engine/src/reincarnated/simulation/damage_resolver.py`, `effect_resolver.py`,
  `gauntlet_sim.py`
- `canonical/matt_decision_needed/2026-07-03-w3-summoner-emission-structural-gap.md` (Option-1 ruling)

**Primary — developer / official:**
- [Grim Dawn v1.3.0.0 + Hotfixes patch notes, Crate Entertainment Forum](https://forums.crateentertainment.com/t/grim-dawn-version-v1-3-0-0/155979) — accessed 2026-07-28
- [Fangs of Asterkarn official guide page](https://www.grimdawn.com/guide/about/fangs-of-asterkarn/)

**Secondary — community canon (curated, authored, maintained):**
- [Top 20 Softcore builds in Grim Dawn (An Opinion)](https://forums.crateentertainment.com/t/top-20-softcore-builds-in-grim-dawn-an-opinion/122229) — banana_peel et al., 2022-10-12, patch 1.1.9.6/.7
- [How to level top 20 (21) builds in Grim Dawn [1.2.1.6]](https://forums.crateentertainment.com/t/how-to-level-top-20-21-builds-in-grim-dawn-1-2-1-6/151255) — Nery, 2026-02-02
- [Beginner Build Compendia for Fangs of Asterkarn & Forgotten Gods](https://forums.crateentertainment.com/t/beginner-build-compendia-for-fangs-of-asterkarn-forgotten-gods/106137) — Ulvar1 / tqFan, ~180+ builds, versions 1.1.9.0–1.2.1.6
- [Fangs of Asterkarn builds theorycraft calcs list](https://forums.crateentertainment.com/t/fangs-of-asterkarn-builds-theorycraft-calcs-list-for-endgame-and-leveling/155952) — 2026-07-21/22, **self-described as unvalidated theorycraft**
- [[1.1.9.8–1.2.0.2] Build Overview — Fire Flames of Ignaffar Purifier (SR75-80+)](https://forums.crateentertainment.com/t/1-1-9-8-1-2-0-2-build-overview-fire-flames-of-ignaffar-purifier-sr75-80/129320)
- [[1.1.7.2] The fire ConeMan! Fire Flames of Ignaffar Purifier focused on conversion](https://forums.crateentertainment.com/t/1-1-7-2-the-fire-coneman-fire-flames-of-ignaffar-purifier-focused-on-conversion/102294)
- [How to create authentic level 100 character using GD Stash?](https://forums.crateentertainment.com/t/how-to-create-authentic-level-100-character-using-gd-stash/125121)
- [GD Stash — Nexus mod 2](https://www.nexusmods.com/grimdawn/mods/2) (1.8.2a: 1.3.0.0 + FoA support)
- [Save files for multiple endgame characters — Nexus mod 213](https://www.nexusmods.com/grimdawn/mods/213)

**Tertiary — aggregator tier list (FoA-aware, used only for corroboration):**
- [Grim Dawn Best Class Tier List 2026](https://skycoach.gg/blog/grim-dawn/articles/best-classes-grim-dawn) — dated 2026-07-27; **explicitly declines to rank Berserker**, which is the right call and is why I trusted its other rows

**Consulted, blocked:**
- `grimtools.com/builds/skill/<id>` — per-skill build counts exist; site `robots.txt` disallows
  `ClaudeBot` / `Claude-User`. Not crawled. One count (FoI = 49) obtained before the check and
  retained with this disclosure; nothing further pulled and the cached page deleted.
