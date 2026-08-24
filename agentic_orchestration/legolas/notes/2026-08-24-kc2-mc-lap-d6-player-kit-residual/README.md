# KC2 MODEL-COMPLETION RUN · Lap D-6 — PLAYER-KIT RESIDUAL DECODE

**Author:** legolas, 2026-08-24 · **Conductor:** gandalf (RUN-CONDUCTOR) · **Ledger:** L-21 / L-26
**Commission:** the DRIFT-CRITIC verdict `2026-08-24-kc2-mc-b1-drift-critic-verdict.md` **F-3** —
B-1's three UNBUILDABLE rows are D-2-CLASS (extraction coverage), not D-5-CLASS (substrate absence),
"each priced at one unvisited record or one template field." Commission: visit the records.
**Law 3 ABSOLUTE:** per-target verdict is DECODED (fields + provenance) or UNDECODABLE-FROM-SUBSTRATE
(with the search record). Read-only against substrate.

---

## 0 · VERDICT — 3 / 3 DECODED, 0 UNDECODABLE

| # | target | verdict | the finding in one line |
|---|---|---|---|
| **T1** | `fighting_spirit` trigger direction | **DECODED** | **`HitByEnemy`-class — on being hit.** Proven from `Game.dll`'s dispatch chain, not inferred from the prose token. **And a correction B-1 could not have made: the row's `cooldown_s = 5.0` is INERT** — the re-fire gate is the active-duration timer. |
| **T2** | Ulzaad's Decree payload | **DECODED** | **There is no `_buff` companion and there never was.** `Class = Skill_BuffSelfDuration` — the payload is on the skill record itself. 8 magnitude fields at dev 20, incl. **two limbs the lap README's prose omitted.** |
| **T3** | `resilience` beyond-heal | **DECODED** | **Heal is NOT the whole payload.** Three further limbs at rank 3 (+3 % DA, +2 % Max All Res, +4 % Physical Res) — plus `thresholdDuration = False`, an **authored override** of the template's `1`, which says the 5 s window does *not* wait for HP recovery. |

**Machine-readable:** `d6_player_kit_residual.csv` — 27 rows, `target / record / level_kind / level /
index / field / value / unit / status / provenance`. Drop-in for the B-2 / B-1f cluster.

**F-3's pricing was right.** All three were unvisited-record / unlocated-field gaps. Two of the three
also returned something *stronger* than the ask — see § 5.

---

## A · THE INDEX CONVENTION, ESTABLISHED BEFORE ANY VALUE IS QUOTED

Every magnitude in this lap is an array read. If the index convention is wrong, every number is wrong
and plausibly so — the failure mode the run exists to prevent. So it is **proven, not assumed**, against
nine values that four prior artifacts pinned independently:

| record | level | field | index read | value | agrees with |
|---|---:|---|---:|---:|---|
| `devotion/tier2_05f_skill_buff` (Maul) | 20 | `defensiveProtectionModifier` | 19 | **−35.0** | B-1 § 5.2 ✓ |
| `devotion/tier2_05f_skill_buff` (Maul) | 20 | `offensiveLifeLeechMin` | 19 | **45.0** | B-1 § 5.2 ✓ |
| `devotion/tier2_17c_skill` (Arcane Barrier) | 20 | `damageAbsorption` | 19 | **2900.0** | Lap G ✓ |
| `devotion/tier1_29e_skill` (Turtle Shell) | 25 | `damageAbsorption` | 24 | **6100.0** | Lap G ✓ |
| `devotion/tier1_29e_skill` (Turtle Shell) | 25 | `skillCooldownTime` | 24 | **8.0** | Lap G ✓ |
| `playerclass01/fightingspirit1` | 5 | `onHitActivationChance` | 4 | **30.0** | Lap G ✓ |
| `playerclass01/fightingspirit1` | 5 | `characterOffensiveAbility` | 4 | **108.0** | B-1 § 5.1 ✓ |
| `playerclass01/fightingspirit1` | 5 | `offensiveTotalDamageModifier` | 4 | **95.0** | B-1 § 5.1 ✓ |
| `playerclass09/passive02` (Resilience) | 3 | `characterHealIncreasePercent` | 2 | **24.0** | I-17 / B-1 § 5.3 ✓ |

**9 / 9 agree. Convention: `array index = level − 1`,** for both player-skill ranks and devotion
levels, across arrays of length 20 *and* 25. Note the Turtle Shell row does real work: its array is
25 long where the devotion procs' are 20, so a hard-coded "index 19" would have silently returned
4,300 instead of 6,100. The rule is level-relative, not array-relative.

---

## 1 · T1 — `fighting_spirit`: THE DIRECTION IS `HitByEnemy`. **DECODED.**

### 1.1 The weaker of B-1's two gaps closes on the record itself

B-1 § 5.1: *"the 30 % has no named field home — `pm4g_field_evidence.csv` records
`onHitActivationChance` on `skill_passiveonhitbuffself.tpl` as 'field not on this template', so the
value is MEASURED in the artifact but its field is unlocated."*

**The field is `onHitActivationChance`, and it is on the record.** The Lap-G evidence row was right
that it is not declared *directly* on `skill_passiveonhitbuffself.tpl` — and wrong to conclude the
field was unlocated, because that template's **first act is four `Include File` directives**:

```
Skill_Base.tpl · Skill_Buff.tpl · Skill_OnHit.tpl · Skill_Bonus.tpl
```

`templatebase/skill_onhit.tpl` declares exactly one variable:

| name | class | type | description (verbatim, GD's own) |
|---|---|---|---|
| `onHitActivationChance` | array | real | **`0 to 100`** |

`fightingspirit1.dbr` carries a 22-entry array; index 4 (rank 5) = **30.0**. The Lap-G measurement and
the field home now agree. *Method note for the crawler contract: a template-field lookup that does not
follow `Include File` returns false negatives. `skill_passiveonhitbuffself.tpl` declares 9 variables
directly and inherits several hundred.*

### 1.2 The direction — decided in code, because no data field decides it

B-1's diagnosis was exactly right: `OnHit` is **not** a member of the autocast `triggerType` picklist,
`controller_record` is empty, and no field on the record names a direction. So the answer is not in the
data layer at all. It is in `Game.dll`, and it is unambiguous.

**The chain, read instruction by instruction** (`d6_gamedll_dispatch.txt` carries the verbatim listing):

```
CombatManager::TakeAttack(ParametersCombat&, SkillManager&, CharacterBio&)     ← the VICTIM's path
  └─ SkillManager::UnderAttack(const ParametersCombat&)                        ← SOLE caller. Exactly one.
       for each Skill* s in this->skills:
           if  s->vslot62  IsSkillOnHitActive()        → 0x18051e50e
               s->vslot53  OnHitActivation(owner, p)   → 0x18051e525
```

and the disjoint sibling path, for contrast:

```
SkillManager::OnCriticalAttack(const ParametersCombat&)                        ← the ATTACKER's path
       for each Skill* s in this->skills:
           if  s->vslot63  IsSkillOnCritActive()       → 0x18051e69e
               s->vslot53  OnHitActivation(owner, p)   → 0x18051e6b5
```

**The discriminator is the gate, not the activation.** Both paths converge on the same slot-53
activation; they differ in which predicate admits a skill. And:

| class | overrides vslot62 `IsSkillOnHitActive` | overrides vslot63 `IsSkillOnCritActive` | reachable from |
|---|:--:|:--:|---|
| **`Skill_PassiveOnHitBuffSelf`** (Fighting Spirit) | **YES** | no (base ⇒ false) | **`UnderAttack` only** |
| `Skill_PassiveOnCritBuffSelf` (Deadly Aim, Battle Surge) | — | **YES** | `OnCriticalAttack` only |

`Skill_PassiveOnHitBuffSelf::IsSkillOnHitActive` is four instructions: `return GetCurrentLevel() != 0`
— i.e. *the skill is learned*. There is no further condition. **Fighting Spirit is reachable only from
`CombatManager::TakeAttack`. It fires when the player is hit.**

> ⚑ **Honesty note on method, because the shortcut here is tempting and wrong.** A byte-scan for
> `call qword ptr [reg + 0x1a8]` returns 17 sites, and `0x1a8` is slot 53 of *whatever* vtable the
> register points at — it names no receiver type. The script emits that superset in full
> (`slot53_bytescan_superset_receiver_type_UNKNOWN`), with `.pdata` RUNTIME_FUNCTION ranges used to
> reject the 6 matches that land mid-instruction. **The scan is not the evidence.** The evidence is
> that the two `SkillManager` sites pair slot 53 with slot 62 / slot 63, which exist only on the
> `Skill` vtable, over `SkillManager`'s own skill list — read directly, not pattern-matched.

### 1.3 Two independent corroborations, both from shipped vendor data

**(a) GD's own description string** — `resources/Text_EN.arc :: tags_skills.txt`,
`tagClass01SkillDescription07A`, verbatim:

> *"Far from beating you into submission, the sting of enemy blows rouses your anger instead, adding
> extra force to your attacks. **^oActivates when taking damage.**"*

**(b) A corpus census of the whole `OnHit` class family** (14,015 skill records scanned; every
resolvable `skillBaseDescription` read out of `Text_EN.arc`). The engine's naming is consistent and the
split is clean:

| class | n | what the shipped descriptions say |
|---|--:|---|
| `Skill_PassiveOnHitBuffSelf` | 5 | Fighting Spirit ×2 ("Activates when taking damage"), Stone Ward, Scavenger Whirlwind, base template |
| `Skill_PassiveOnHitBuffShield` | 11 | **11/11 on-being-hit**: *"whenever struck by"*, *"when struck by physical blows"*, *"Upon suffering harm"*, *"whenever an enemy manages to find a weak point in your defenses"* |
| `Skill_OnHitAttackRadius` | 13 | retaliation-shaped: Counter Strike (*"counter strikes against your attackers"*), Ice Surge (*"enemies that strike you"*), Vindictive Flame |
| `Skill_PassiveOnCritBuffSelf` | 4 | **outgoing** — Deadly Aim, Battle Surge: *"**As you land** critical blows"* |

Every class in the `OnHit` family reads as on-being-hit. The one outgoing case in the neighbourhood is
named `OnCrit`, not `OnHit`. **`OnHit` is the engine's word for the defensive side.**

### 1.4 ⚑ THE FINDING UNDER THE FINDING — `cooldown_s = 5.0` IS INERT, AND THE ROW ALREADY CARRIES IT

This was not commissioned and is the most consequential thing in the lap, because it corrects a value
already sitting in a decoded row rather than filling a hole that was flagged as empty.

`Skill_PassiveOnHitBuffSelf::OnHitActivation`, decompiled to its predicate skeleton:

```
if (services == null)                       return;
if (!vslot61 IsSkillEnabled())              return;
if ( vslot57 GetCurrentLevel() == 0)        return;
if ( this->[0x5cc] > 0 )                    return;      // ⚑ THE RE-FIRE GATE
chance = SkillProfile::GetActivationChance(vslot175 GetSkillProfile(), level);
roll   = rng_uniform_int(0, 100);
if ((float)roll > chance)                   return;      // fire iff roll <= chance
…activate…
this->[0x5cc] = this->[0x5c8] = (int)(skillActiveDuration_s * 1000.0f);
```

`[0x5cc]` is the **remaining active duration in ms**, decremented by `dt` in `Update` and zeroed on
expiry. `OnHitActivation` **never reads a cooldown timer.** And the class's `EndCooldown` override
(`rva 0x158b0`) is the **COMDAT-folded `ret` stub** — byte `0xC3`, address-shared with
`Singleton<Quest2Repository>::~Singleton`, `SkillState::~SkillState` and four other empty destructors.
`SkillManager::EndCooldown` dispatches the cooldown tick through vslot 79; for this class that lands on
the stub. **The cooldown never advances, and nothing reads it.**

> **Consequence for the model:** Fighting Spirit's re-fire period at rank 5 is
> **6.1999998 s (the active duration), not 5.0 s.** A build using the 5.0 would over-fire the proc by
> ~24 % on a saturated incoming stream. The value is on the record and it is real data; it simply is
> not wired to anything in this class. Row status in the CSV is **`DECODED-BUT-INERT`**, with the gate
> shipped alongside as an explicit `REFIRE_GATE` row so a consumer cannot pick up the number without
> the caveat.

### 1.5 What the decode buys — B-1's pricing stands, and F-3's two-column reading is now substantiated

B-1 measured that both magnitudes are non-folding: `characterOffensiveAbility +108` is **provably
inert** (minimum PTH 149.2 already clears `pthThreshold6 = 135`; `HIT_CHANCE` already 1.0; PTH monotone
in OA), and `offensiveTotalDamageModifier +95 %` is the standing `counterplay.NOT_FOLDED` declaration.
**Nothing here disturbs that.** What D-6 adds is that the *schedule* is now decoded rather than
unknown — the activation stream (`HitByEnemy`, 30 % per incoming hit, gated by a 6.2 s active window)
is exactly the visible-activation series F-3 argued a live player is entitled to. `blocks_playability`
= FALSE on `arithmetic`, TRUE on `presentation`, and the presentation column now has a firing rule
behind it rather than a guess.

---

## 2 · T2 — Ulzaad's Decree: THE PAYLOAD IS ON THE SKILL RECORD. **DECODED.**

### 2.1 The premise of the ask is falsified, and that is the finding

B-1 § 5.2 reasoned by analogy from Maul — which ships as a **pair**, `tier2_05f_skill.dbr` (4 fields,
empty magnitudes) + `tier2_05f_skill_buff.dbr` (659 fields, all the numbers) — and concluded *"Ulzaad's
Decree has no `_buff` companion row in the artifact — the payload record was never visited."*

**`records/skills/devotion/tier2_37d_skill_buff.dbr` does not exist in any of the eight archives.** It
was not missed by the extraction. It is not authored. The reason is structural and visible on the
record itself:

| record | `Class` | shape |
|---|---|---|
| Maul `tier2_05f_skill.dbr` | *(4 fields — a pointer stub)* | thin skill → fat `_buff` payload |
| **Ulzaad `tier2_37d_skill.dbr`** | **`Skill_BuffSelfDuration`** | **735 fields — self-buff, payload in place** |

Maul is a **debuff applied to a target**, so its payload lives in a separate applied-buff record.
Ulzaad's Decree is a **self-buff with a duration**, so the payload is the skill. The `_buff` suffix is
a consequence of the class, not a corpus-wide convention. *This generalises: `…_buff` companion lookups
should be gated on `Class`, not attempted blindly — the D-2 "unvisited owner record" reflex produces a
false ABSENT here.*

### 2.2 The payload at devotion 20 (index 19)

| field | value @ dev 20 | unit — from GD's own UI format tag |
|---|---:|---|
| `defensiveProtection` | **190.0** | flat **Armor** (`DefenseAbsorptionProtectionPlus` = `+{n} {^E}Armor`) |
| `offensivePhysicalModifier` | **200.0** | % Physical damage |
| `offensivePierceModifier` | **200.0** | % Pierce damage |
| **`offensiveSlowPhysicalModifier`** | **200.0** | % Physical **DoT** — ⚑ absent from the README prose |
| **`offensivePhysicalMin` / `Max`** | **42.0 / 45.0** | flat Physical — ⚑ absent from the README prose |
| **`retaliationPhysicalMin` / `Max`** | **205.0 / 450.0** | flat Physical Retaliation (`RetaliationPhysical`) — ⚑ absent from the README prose |
| `skillActiveDuration` | **10.0 s** | — (matches Lap G's independently-read 10.0 ✓) |
| `skillCooldownTime` | **22.0 s** | scalar, not an array (matches Lap G ✓) |
| `instantCast` | `True` | — |
| `templateAutoCast` | `records/controllers/itemskills/cast_@selfonattack_20%.dbr` | Lap G's binding, unchanged |

**Lap G's prose — *"+200 % phys/pierce, 190 flat protection"* — is CONFIRMED against the machine
substrate.** B-1 was right to refuse to fold it (*"prose in a landing note is not the machine
substrate"*) and right on the content. Three further limbs surface that the prose did not carry.

**For facet (d) specifically:** the sustain-relevant limb is **`defensiveProtection = 190` flat Armor**,
which composes with the global-flat-armour operand (Lap Y) rather than with the absorb/heal layers.
The offensive and retaliation limbs are outside facet (d)'s scope and are shipped in the CSV for
whichever facet claims them, not folded here.

---

## 3 · T3 — `resilience`: HEAL IS NOT THE WHOLE PAYLOAD. **DECODED.**

`playerclass09/passive02.dbr` — `Class = Skill_PassiveOnLifeBuffSelf`, archive `gdx2`, rank 3 → index 2.

| field | value @ rank 3 | unit — from GD's own UI format tag | in model before D-6? |
|---|---:|---|---|
| `characterHealIncreasePercent` | 24.0 | `Healing Effects Increased by {n}%` | ✅ folded via I-17 |
| **`characterDefensiveAbilityModifier`** | **3.0** | `{+n}% {^E}Defensive Ability` | ❌ **new** |
| **`defensiveAllMaxResist`** | **2.0** | `{+n}% {^E}Max All Resistances` | ❌ **new** |
| **`defensivePhysical`** | **4.0** | `{n}% {^E}Physical Resistance` | ❌ **new** |
| `lifeMonitorPercent` | 66.0 | scalar — the monitor threshold | ✅ (B-1 `MONITOR_BASIS`) |
| `skillActiveDuration` | 5.0 s | scalar | ❌ new |
| `skillCooldownTime` | 15.0 s | scalar | ❌ new |
| **`thresholdDuration`** | **`False` — an AUTHORED OVERRIDE of the template's `1`** | see § 3.1 | ❌ **new** |

`damageAbsorption` / `damageAbsorptionPercent` / `defensiveProtection` are **ABSENT on the record** —
reported as absent, not defaulted. So B-1's alternative outcome ("a clean finding that heal is the whole
payload") is **falsified**: three further limbs exist, all defensive, all facet-(d) adjacent.

⚑ **One semantic worth carrying to F-4's regen/ADCtH exposure**, straight from GD's own stat tooltip
(`tagCharStatsHealIncreaseInfo`, `tagsgdx2_ui.txt`): *"The percent bonus to all healing effects,
**including Potions and Attack Damage Converted to Health**. **Does not increase Health Regeneration**."*
Resilience's +24 % therefore multiplies the potion **and the ADCtH stream** — the two largest sustain
rows on the cell — and does **not** touch the 129.38 hp/s regen. That is a fold rule, not a magnitude,
and it is decoded here rather than assumed.

### 3.1 `thresholdDuration` — **`False`, and it is AUTHORED, not inherited**

The field is declared on `skill_passiveonlifebuffself.tpl`:

| name | class | type | **default** | description (verbatim, GD's own) |
|---|---|---|---|---|
| `thresholdDuration` | variable | **bool** | **`1`** | *"Wait for life to be above threshold before starting duration timer?"* |

**`passive02.dbr` carries `thresholdDuration = False`** — Crate explicitly wrote the value that
*overrides* the default. The question the field asks is answered **NO** for Resilience:

> **The 5.0 s duration timer starts on trigger and runs regardless of HP.** Resilience does **not**
> hold itself open until the player climbs back above 66 %. It is a fixed 5 s window on a 15 s
> cooldown, and the `lifeMonitorPercent = 66` threshold is a *firing* condition only, not a
> *sustaining* one.

This is the same field B-1 § 1.2 leans on for Menhir's Will, and the two records need not agree — the
value is per-record and this one is authored. **It is a direct input to the `MONITOR_ON_FLOOR` vs
`POLL_AT_SLOT` limb question**, and it points the opposite way from the assumption that a monitor-limb
buff persists through an excursion. *Reported, not folded: designating a limb is gamora's call and
grading it is nobody's this lap.*

**Corpus context, so "authored" is a measurement and not a manner of speaking:** 65 skill records in
the corpus set `thresholdDuration` explicitly, in both directions (`ironmaiden_willtolive1` = True,
`item_dreegcommand` = False, …). Authors write this field when they mean the non-default, and
`passive02.dbr` is one of the 65.

### ⚑ 3.2 `D-D6-1` — MY FIRST PASS READ THIS FIELD AS ABSENT. PUBLISHED, NOT QUIETLY FIXED.

My first dump of `passive02.dbr` suppressed falsy values as noise — a reasonable filter against the
several hundred `…XOR` / `…Global` / `…DamageQualifier` booleans that every skill record carries at
default `False`. **It also swallowed the one `False` that was authored,** and I wrote a § 3.1 that
declared the field absent and derived the *opposite* semantics from the template default. Same class of
defect as `D-B1-1`: a filter that was right about the population and wrong about the one row that
mattered.

**Caught by an instrument, not by re-reading.** The fix is not "look harder" — it is a
**bool-vs-template-default sweep** that resolves the full `Include File` graph (1,144 declared variables
for this template) and reports every bool whose record value differs from its default. It is retained
in `d6_decode.py` (`_bool_sweep`) and emitted to `d6_summary.json`, so the authored-vs-inherited call is
reproducible rather than one-shot. It returns three overrides across the three targets:
`passive02: thresholdDuration=False, roundBitmap=True` · `tier2_37d: instantCast=True` ·
`fightingspirit1: none`.

> **The general form, for the crawler contract:** *in a corpus where records store only deviations
> from a template, `False` is not the same as absent, and a falsy-suppressing dump cannot tell them
> apart. Authored-vs-inherited must be decided against the template graph, never against the
> record alone.*

---

## 4 · PROVENANCE, AND THE ONE VERSION SKEW — DECLARED, NOT BURIED

| artifact | sha256 | what it supplied |
|---|---|---|
| `edition-III/database/database.arz` | `2ad6d379285cfb745462316949e8d59e…` | `fightingspirit1` |
| `edition-III/gdx2/database/GDX2.arz` | `13fa0b93be15835958968ad672b9efa5…` | `passive02` |
| `edition-III/gdx3/database/GDX3.arz` | `e990e1265f14ff2ee241658433d4d666…` | `tier2_37d_skill` |
| `edition-III/database/templates.arc` | `679db83f019020ef7d4d27be8e612030…` | field schema + developer descriptions (matches D-2's pin ✓) |
| `edition-III/resources/Text_EN.arc` | `1105b1eef70c83914a00d0516ea6db3a…` | `tags_skills.txt`, `tags_ui.txt` |
| `edition-III/gdx2/resources/Text_EN.arc` | `8aec9207b5dd0b33cb981455ec867d71…` | `tagsgdx2_skills.txt`, `tagsgdx2_ui.txt` |
| `grim-dawn/x64/Game.dll` | `7c62f1aa8b32ce3dbfb5a640b7af2802…` | **T1 dispatch semantics only** |
| `grim-dawn/Game.dll` (x86) | `4876d6bdb69cca71cfa987652cbd7a42…` | parity check — the build prior KC2 laps pinned |

> ⚑ **VERSION SKEW, stated plainly.** All **magnitudes** come from the edition-III 2026-08-08 depot —
> the corpus every prior KC2 lap read. The **semantics** in T1 come from the 2026-07-23 install's
> `Game.dll`, a **different build**: that install's `database.arz` is `8cdeff12…`, not edition-III's
> `2ad6d379…`. **No magnitude in this lap comes from `Game.dll`.** Two things bridge the gap and both
> are checked in code: (a) the class-name string `Skill_PassiveOnHitBuffSelf` appears verbatim in the
> edition-III `templates.arc` *and* in `Game.dll`'s export table; (b) an **x86/x64 symbol-parity check**
> over the seven load-bearing symbols returns **ALL PRESENT IN BOTH BUILDS** — so the class/method set
> is not build-specific, and the prior laps' pinned x86 binary carries the identical structure.

**Reader used:** `E3.winner()` (whole-record replacement, the L-33/C-9 overlay law) for magnitudes;
`E3.merged()` for the corpus censuses, matching the reading each prior artifact was extracted under.
PE parsing is a ~40-line read-only reader in `d6_decode.py` (export directory + vftables + `.pdata`);
disassembly is `capstone` 5.0.7. No third-party PE library, no writes to any vendor path.

---

## 5 · WHAT THIS LAP RETURNS BEYOND ITS COMMISSION

F-3 priced three targets at "one unvisited record or one template field." That pricing held. Two of
the three also returned something the commission did not ask for, and in both cases it corrects
something already *in* the model rather than filling a hole already marked empty:

1. **`fighting_spirit.cooldown_s = 5.0` is inert** (§ 1.4). The re-fire period is 6.2 s. This value is
   already in the decoded Lap-G row and would have been built.
2. **The Maul-pair analogy does not generalise** (§ 2.1). `…_buff` companion lookups must be gated on
   `Class`; blind lookups return false ABSENTs. Worth a line in the crawler contract.
3. **Healing Increase multiplies ADCtH and the potion but not regen** (§ 3). A fold rule for F-4's
   continuous-sustain exposure, decoded from GD's own stat tooltip.
4. **`resilience.thresholdDuration = False` is authored**, and points the *opposite* way from the
   template default (§ 3.1) — a live input to the `MONITOR_ON_FLOOR` / `POLL_AT_SLOT` limb question.
   Caught only by the bool-vs-template sweep that `D-D6-1` forced (§ 3.2).

**Owed to nobody by this lap; offered to the conductor:** items 1 and 3 both touch rows that are
already built or already on the wire, which is the F-1 class of defect (a pinned text that has stopped
being true) pointing at data rather than prose. Routing is the conductor's call.

**No new absence rows are earned.** The absence registry gains nothing from D-6 — which is the outcome
F-3 predicted, and the reason it refused to let B-1's three refusals be written down as substrate gaps.

---

## FILES

| file | what it is |
|---|---|
| `README.md` | this — per-target verdicts and the argument behind each |
| `d6_player_kit_residual.csv` | **27-row machine-readable parameter table** — the gamora deliverable |
| `d6_summary.json` | full structured record: index-convention checks, dispatch analysis, class-family census, bool-vs-template-default sweep, UI-tag semantics, digests, skew declaration |
| `d6_gamedll_dispatch.txt` | verbatim capstone listing of the five functions T1 rests on — no interpretation |
| `d6_decode.py` | the reproducible decode; read-only; `python3 d6_decode.py` regenerates all four artifacts |
