# DoT semantics audit — KC2-PM3 Lap C, deliverable 3

**Agent:** legolas (UNKNOWN-RESEARCHER) · **Conductor:** gandalf (`RUN-CONDUCTOR`) · **2026-08-12**
**Charter:** `gandalf/notes/2026-08-12-kc2-pm3-run-charter.md`, Lap C item (3)
**Discipline:** GL-12 — every claim below cites a named record, template file or localization tag
in the Edition-III corpus. **Nothing here comes from a wiki, a forum, or model prior.** Where the
corpus is silent the silence is named as a CLIFF and the question is left open.

**Corpus (imported basis, not re-declared):** `/Users/admin/Games/vendor/grim-dawn-edition-III-20260808`,
8-archive last-wins overlay via `s2_lib.E3` (84,829 record paths). Localization: 5 `Text_EN.arc`
archives, 20,471 tags. Templates: `database/templates.arc`.

---

## §0 — Headline (five findings, in order of consequence to the fold)

| # | finding | consequence |
|---|---|---|
| **F-1** | **SEM-1 is RATIFIED by measurement, not merely defaulted-to.** The game's own tooltip composition proves `offensiveSlow<X>Min` is the **TOTAL delivered over `offensiveSlow<X>DurationMin` seconds**. | Conductor ruling **R-PM2-1 stands and is now MEASURED**, not "unresolvable → take the lower reading". The PM-2 fold's DoT arithmetic is correct. No change to gamora's v2. |
| **F-2** | **`playerDefenseCap = [80, 80, 80]` is decoded.** `records/game/gameengine.dbr`, template description "Index by difficulty 0 to 2". | Lap A gap **G-2 (`resist_max_overcap_all = GAP`) is CLOSED**. The PM-2 fold used the sheet's **85 %** bleed resistance uncapped; the cap is 80 %. **Correction: bleed mitigation 0.15 → 0.20 ⇒ +33 % bleed damage taken.** Every other resistance on the sheet is exactly 80 and is unaffected. |
| **F-3** | **`aetherialcorruption_rotskin` is a toggled damaging AURA, not a discrete attack.** `Class = Skill_BuffAttackRadiusToggled` (a `static` template field), `skillTargetRadius = 3.5 m`, template includes `Skill_Activated.tpl` with `skillActiveManaCost` / `skillActiveLifeCost` — the signature of a sustained toggle, not a swing. | The PM-2 fold consumed it through the `initial` slot on the D.3 one-slot-per-opportunity clock. **Named mis-fold.** Direction of error is NOT decidable (aura tick rate is engine-side, CLIFF C-4) but the *geometry* is: this threat is **positional and continuous inside 3.5 m**, which is exactly what the PM-3 CLUSTER policy walks into. |
| **F-4** | **The Acid/Poison and Vitality/Vitality-Decay resistance joins in PM-2 §A.1 are CORRECT.** `DefensePoison` = "Poison & Acid Resistance" — one stat covers both `offensivePoison` (Acid, instant) and `offensiveSlowPoison` (Poison, DoT). `DefenseLife` = "Vitality Resistance", covering `offensiveLife` and `offensiveSlowLife`. | Ratified. No change. |
| **F-5** | **A same-type-DoT diminishing constant EXISTS and is named:** `records/game/gameengine.dbr` `damageMagnitude = 100.0`, template description **"Decreasing same type duration damage"**. | The stacking question now has a *substrate address* it did not have. The mapping from `100.0` to a stacking rule is **NOT decoded — CLIFF C-4.** Do not model a stacking rule off this; model the address. |

---

## §1 — Q: total-over-duration, or per-second? (SEM-1 / R-PM2-1)

### 1.1 What settles it

Grim Dawn composes a DoT line in a skill tooltip from **two** localization tags, both in
`resources/Text_EN.arc :: tags_ui.txt`:

| tag | value |
|---|---|
| `DamageDurationPoison` | `' {^E}Poison Damage'` |
| `DamageDurationLife` | `' {^E}Vitality Decay Damage'` |
| `DamageDurationBleeding` | `' {^E}Bleeding Damage'` |
| `DamageSingleFormatTime` | `' {^E}over {^H}{%.1f0} {^E}Seconds'` |
| `DamageRangeFormatTime` | `' {^E}over {^H}{%.1f0}-{%.1f1} {^E}Seconds'` |

The rendered line is therefore `<value> Poison Damage **over** N Seconds`, where `N` is the
record's `offensiveSlowPoisonDurationMin`. **A number printed "over N seconds" is a total, not a
rate.** That is the direct evidence Lap B looked for and could not find.

### 1.2 The corroborating half

`tags_ui.txt` also carries the *other* display, and it is explicitly per-second, which is why the
question was confusable:

* `tagDurationDamageOverTime` = `'{%d0} {^E}Damage Every Second'` — the **HUD debuff-icon** rollover.
* `tagDotTimeRemaining` = `'{^H}{%.0f0} {^E}Seconds Remaining'` — the same rollover's clock.

So GD renders a live DoT as *rate + remaining time*, and a skill's contract as *total + duration*.
Both exist; they describe different surfaces. `DamageSingleFormatTime` is the one bound to the
skill record's `offensiveSlow*Min` field, and it says **total**.

### 1.3 Verdict

> **The PM-2 fold's `dot_dps_if_field_is_total` (= raw ÷ duration, applied per second for
> `dot_duration_s` seconds) is the CORRECT reading, and is now MEASURED rather than defaulted.**
> R-PM2-1 needs no revision. 718 of 4,722 Lap-B rows (15.2 %) ride on this and they ride correctly.

### 1.4 The one thing it changes anyway — duration is a damage axis

`tags_ui.txt` is unambiguous that duration modifiers move **total** damage and not DPS:

* `tagCharStatsPoisonDurationInfo` = *"The percent bonus to the duration of your Poison Damage
  attacks. **The damage per second is not increased.**"* (identical wording for Bleed, Burn,
  Frostburn, Electrocute, Internal Trauma, Vitality Decay.)

⇒ `total = (stored_value / base_duration) × actual_duration`, and
`actual_duration = base_duration × (1 + attacker duration bonus %) × (1 − defender duration reduction %)`.

**The defender duration-reduction axis is entirely absent from the PM-2 fold** (§A.1 maps
resistances only). For this run that is harmless — **the measured player sheet carries no
defensive duration-reduction row at all** (`measured-player-sheet.csv`: the `*_duration` rows,
lines 60/63/85/88/91/94/97, are the player's *offensive* DoT durations). It is NOT harmless for the
BLESSINGS-ON arm: `blessingulo_buff.dbr` grants `defensivePoisonDuration = 50` — a flat halving of
incoming poison **total**, on top of the 80 % resistance. Whichever arm folds blessings must fold
the duration axis or it will understate Ulo by a factor of two on exactly the threat family that
killed the reference player.

Default base durations, decoded from the char-sheet tooltips (`tagCharStats*AbsDmgInfo`):
Poison **5 s** · Internal Trauma **5 s** · Bleed / Burn / Frostburn / Electrocute / Vitality Decay **3 s**.
*(These are the character-sheet display defaults. A skill record that ships its own
`offensiveSlow<X>DurationMin` — both audited skills do — uses its own value, not these.)*

---

## §2 — Q: where does resistance apply?

### 2.1 The family → resistance map, decoded from the game's own stat names

| offensive field | rendered as (`tags_ui.txt`) | resisted by | rendered as |
|---|---|---|---|
| `offensivePoisonMin` | `DamagePoison` = "**Acid** Damage" | `defensivePoison` | `DefensePoison` = "**Poison & Acid** Resistance" |
| `offensiveSlowPoisonMin` | `DamageDurationPoison` = "**Poison** Damage" | `defensivePoison` | *same stat* |
| `offensiveLifeMin` | — | `defensiveLife` | `DefenseLife` = "Vitality Resistance" |
| `offensiveSlowLifeMin` | `DamageDurationLife` = "Vitality **Decay** Damage" | `defensiveLife` | *same stat* |
| `offensiveSlowBleedingMin` | `DamageDurationBleeding` = "Bleeding Damage" | `defensiveBleeding` | `DefenseBleeding` = "Bleeding Resistance" |

**One resistance covers the instant and the DoT half of a family.** PM-2 §A.1's DoT→base-family
map is therefore exactly right, and the "80 acid / 80 vitality / 85 bleed" sheet values DO apply to
`livingplant_venomousseed` and `aetherialcorruption_rotskin`. The charter's framing — *"DoTs are
#1–2 incoming DESPITE 80/80/85"* — is not a contradiction to resolve; it is what a 20 % leak on a
very large number looks like.

### 2.2 The cap — Lap A gap G-2, CLOSED

```
records/game/gameengine.dbr        playerDefenseCap  = [80.0, 80.0, 80.0]
                                   monsterDefenseCap = [100.0, 100.0, 100.0]
database/templates.arc :: gameengine.tpl
                                   playerDefenseCap  class="array" type="real"
                                                     description="Index by difficulty 0 to 2"
```

Corroboration that 80 is a **cap** and not a coincidence: the corpus carries a whole family of
*max-resist* stats whose only purpose is to raise it — `DefensePoisonMaxResist` = "% **Max**
Poison & Acid Resistance", `DefenseBleedingMaxResist`, `DefenseAllMaxResist`, `DefenseCrowdControlMaxResist`.
A cap-raising stat implies a cap.

**Correction owed to the fold:** the sheet's `resist_bleeding = 85` must be clamped to **80**
unless a max-resist source is measured (none is on the sheet). Mitigation `0.85 → 0.80`, i.e.
**bleed damage taken ×1.333**. All other sheet resistances are exactly 80 and are unaffected.
`resist_physical = 16` is far below cap and unaffected.

⚑ **Residual, declared:** whether the GD character sheet prints the raw total or the already-capped
value is **not decodable from the corpus** — it is a UI behaviour. If the sheet prints post-cap, 85
would imply a +5 max-resist source and no correction is owed. The 80-cap constant is measured; the
sheet's pre/post-cap convention is **CLIFF C-3**. Flagged, not silently applied.

### 2.3 Per-tick or on-application?

**NOT DECODABLE. CLIFF C-1.** The corpus contains no record, template field or tag that binds the
moment of resistance evaluation. Two structural facts bound the question without answering it:

* Magnitude (`defensivePoison`) and duration (`defensivePoisonDuration`) are **independent fields
  in independent template groups**, so at minimum the engine evaluates two distinct defender terms.
* `damageMagnitude`'s description ("Decreasing same type duration damage") sits on the *engine*
  record, not on the skill, which means at least one DoT-composition rule is global and applied at
  the receiving end.

For a sim in which the player's resistances are **constant for the whole fight**, per-tick and
on-application are numerically identical. **The distinction is inert for PM-3 and should not be
modelled.** It becomes live only if the fold ever gives the player time-varying resistances
(e.g. an Ulo blessing that expires at `skillActiveDuration = 1500 s`).

---

## §3 — Q: stacking

### 3.1 What the corpus gives

```
records/game/gameengine.dbr    damageMagnitude = 100.0
gameengine.tpl                 damageMagnitude  class="array" type="real"
                                                description="Decreasing same type duration damage"
```

This is the first substrate address for GD's DoT-stacking behaviour that this project has found.
It says, in Crate's own words, that **same-type duration damage is subject to a decreasing rule**,
and that the rule is parameterised by a single global engine constant currently set to `100.0`.

Per-skill application gates also exist and are decoded, but are **not** set on either audited skill:

* `offensiveSlowPoisonXOR` (bool) — false on both.
* `offensiveSlowPoisonGlobal` (bool) — false on both.
* `offensiveSlowPoisonChance` — absent (⇒ no chance gate) on both.

### 3.2 What the corpus does NOT give — CLIFF C-4

The **function** mapping `damageMagnitude = 100.0` to an outcome is engine-side. Nothing in the
`.arz`, the templates, the localization or the Crucible's Lua states whether same-type DoTs from
**different sources** stack additively, take-the-max, or decay; nor whether a re-application from
the **same source** refreshes, extends, or is ignored.

> **Ruling for gamora: do not model a stacking rule.** Continue PM-2's behaviour (each landed DoT
> application contributes its own total over its own duration, summed). Carry `damageMagnitude` and
> this cliff on the wire as a declared over-read of the same-type case. If PM-3's findings hinge on
> it, the resolution requires either a live in-game A/B measurement or engine disassembly — both
> outside a read-only lap.

### 3.3 The multiplicity that is decodable, and matters more

Same-type stacking is a second-order question here because the **first-order** driver is the number
of distinct DoT *sources* on the board, and that IS measured. In `tg2_attack_damage.csv`
(4,724 rows, the E-s09-cp150 roster) the two audited skills occupy **50 rows across 8 distinct
carrier records** — `aetherialcorruption_intro / _h01 / _h03 / _c01` (rotskin, ranks 26–28) and
`livingplant_a01 / livingplant_a01_summon` (venomousseed, ranks 27–28), the latter a **summon**,
so its count scales with pet population. Different carriers are different sources under any
stacking rule. **A CLUSTER movement policy that maximises bodies-in-disc maximises exactly this
count.** That is the load-bearing interaction for PM-3, and it needs no stacking ruling at all.

---

## §4 — Per-skill decode of the two ranked threats

### 4.1 `livingplant_venomousseed` — sim rank #1 incoming, 12,877 dmg

`records/skills/nonplayerskillsgdx1/attackprojectile/livingplant_venomousseed.dbr` (gdx1)
`Class = Skill_AttackProjectileDrop` · `skillMaxLevel = 60` · `projectileExplosionRadius = 2.5` ·
`skillTargetRadius = 1.5` · `distanceProfile = Boss` · fired from `special2`.

| field | @rank 28 | family | rendered as | resisted by |
|---|---:|---|---|---|
| `offensivePoisonMin` | **952** | direct | **Acid** Damage | acid/poison 80 |
| `offensiveSlowPoisonMin` | **252** | dot, `DurationMin = 5.0 s` | **Poison** Damage over 5 s | acid/poison 80 |
| `offensivePercentCurrentLifeMin` | **16 %** | percent-current-life | — | **no resistance family exists** |
| `offensiveSlowPoisonMin` (debuff half) | 252 | — | — | — |

**Audit result: the PM-2 fold read this skill correctly.** Every value in `tg2_attack_damage.csv`
reproduces from the record at the stated rank, the direct/dot split is right, and both halves map
to the same 80 % resistance. **The DoT is not the dangerous half of this skill** — 252 over 5 s
against 80 % resistance is ~50 hp/s reduced to ~10 hp/s, while `offensivePercentCurrentLife = 16 %`
is unresisted and unbounded. The skill's rank in the incoming table is dominated by the 952 Acid
hit and the 16 % term, not by its poison. *(PM-2 §C.3 already flagged `percent_current_life` as the
single largest term and asked for it to be attacked; this decode agrees with that instinct.)*

⚑ A **second** `livingplant_venomousseed.dbr` exists at
`records/skills/nonplayerskillsgdx1/bossskills/special/` with **larger** numbers
(`offensivePoisonMin@28 = 1,407`, `offensivePercentCurrentLifeMin = 18` scalar, plus an
`autoCastSkill` gas-cloud secondary). It is **not** the record the roster uses — Lap B resolved the
`attackprojectile` path, and the values in `tg2_attack_damage.csv` match that path exactly. **The
fold picked the right one of two same-named records.** Noted so nobody "fixes" it later.

### 4.2 `aetherialcorruption_rotskin` — sim rank #2 incoming, 12,992 dmg

`records/skills/nonplayerskillsgdx1/buffattackradius/aetherialcorruption_rotskin.dbr` (gdx1)
`Class = Skill_BuffAttackRadiusToggled` · `skillTargetRadius = 3.5` · `distanceProfile = Short` ·
`charFxPakSelfNames = .../zombie_poisonaura_self_chfxpak01.dbr` ·
`autoCastController = cast_@enemyonanyhit_25%` → `autoCastSkill = aetherialcorruption_aetherorbitalretaliation`.

| field | @rank 28 | family | resisted by |
|---|---:|---|---|
| `offensiveAetherMin` | **205** | direct | aether 80 |
| `offensiveSlowPoisonMin` | **205** | dot, `DurationMin = 2.0 s` | acid/poison 80 |

**The mis-fold (F-3).** `skill_buffattackradiustoggled.tpl` includes `TemplateBase/Skill_Base.tpl`,
`Skill_Activated.tpl` and `Skill_Buff.tpl`, and declares `skillTargetRadius`, `skillActiveManaCost`,
`skillActiveLifeCost`, `instantCast`. **Per-second upkeep costs are the signature of a sustained
toggle.** The self-FX record name (`zombie_poisonaura_self`) is a second, independent witness. This
is a persistent contact aura the carrier switches on once (via `initialSkillName`) and then holds.

PM-2 consumed it as a **slot** skill in the D.3 fixed order, meaning: at most one firing per
`basic_swing_period_s` opportunity, *and* — because only the FIRST eligible slot fires — a rotskin
carrier standing inside 3.5 m spends its opportunity on the aura instead of on its weapon swing.
Both halves of that are wrong for a toggle:

1. a toggle does not consume an attack opportunity, so the carrier's **weapon damage was displaced**
   (under-read of that carrier's melee);
2. the aura's real delivery is continuous inside 3.5 m, so its own contribution is a function of
   **dwell time in the ring**, not of swing count.

⚑ **What I am NOT ruling.** The aura's tick period is engine-side and undecodable (**CLIFF C-4b**).
I cannot say whether the fold over- or under-counted rotskin in net. What I can hand gamora is the
correct *shape*: `direct 205 Aether + 205 Poison over 2 s`, applied to anything within **3.5 m** of
a live carrier, for as long as it is within 3.5 m. If v2 keeps the PM-2 treatment, it should carry
this as a named declared-wrong row rather than as a measurement.

**Carrier census (basis: `tg2_attack_damage.csv`, 4,724 rows, E-s09-cp150 roster):** 4 distinct
carrier records — `aetherialcorruption_intro` (rank 28), `_h01` (28, twice), `_h03` (28),
`_c01` (26). `dralgar_rotskin.dbr` is a fifth, byte-identical-in-effect variant on
`aetherialcorruption_intro`.

---

## §5 — Cliffs (named, not improvised past)

| id | cliff | why it cannot be closed read-only | what to do instead |
|---|---|---|---|
| **C-1** | resistance applied per-tick vs on-application | no record, template or tag binds the evaluation moment | inert while player resistances are fight-constant; do not model |
| **C-3** | does the GD character sheet print pre- or post-cap resistance? | UI behaviour, not corpus | flag the 85 bleed; do not silently clamp without conductor sign-off |
| **C-4** | `damageMagnitude = 100.0` → same-type DoT stacking function | engine-side | keep PM-2's per-application summation; carry the address + the over-read on the wire |
| **C-4b** | toggled-aura tick period (`Skill_BuffAttackRadiusToggled`) | engine-side | fold the 3.5 m geometry; declare the rate |

---

## §6 — Source list (every claim above traces here)

**Records** (Edition-III overlay, `s2_lib.E3`)
`records/game/gameengine.dbr` ·
`records/skills/nonplayerskillsgdx1/attackprojectile/livingplant_venomousseed.dbr` ·
`records/skills/nonplayerskillsgdx1/bossskills/special/livingplant_venomousseed.dbr` ·
`records/skills/nonplayerskillsgdx1/buffattackradius/aetherialcorruption_rotskin.dbr` ·
`records/skills/nonplayerskillsgdx1/bossskills/dralgar_rotskin.dbr` ·
`records/skills/powerups/blessingulo_buff.dbr`

**Templates** (`database/templates.arc`)
`gameengine.tpl` · `templatebase/parameters_offensive.tpl` · `skill_buffattackradiustoggled.tpl` ·
`skill_attackprojectiledrop.tpl`

**Localization** (`resources/Text_EN.arc :: tags_ui.txt`)
`DamagePoison` · `DamageDurationPoison` · `DamageDurationLife` · `DamageDurationBleeding` ·
`DamageSingleFormatTime` · `DamageRangeFormatTime` · `tagDurationDamageOverTime` ·
`tagDotTimeRemaining` · `DefensePoison` · `DefenseLife` · `DefenseBleeding` ·
`DefensePoisonDuration` · `DefensePoisonMaxResist` · `DefenseBleedingMaxResist` ·
`DefenseAllMaxResist` · `tagCharStatsPoisonAbsDmgInfo` · `tagCharStatsPoisonDurationInfo` ·
`tagCharStatsBleedAbsDmgInfo` · `tagCharStatsVitalityDecayAbsDmgInfo`

**Pinned lap inputs**
`legolas/notes/2026-08-12-kc2-pm2-lap-a-player-sheet/measured-player-sheet.csv` ·
`legolas/notes/2026-08-12-kc2-pm2-lap-b-threat-decode/tg2_attack_damage.csv` ·
`reincarnated-engine/src/reincarnated/simulation/math/kc2-pm2-incoming-damage-2026-08-12.md` (§A.1, §C.2, §C.3, §D.1–D.3)
