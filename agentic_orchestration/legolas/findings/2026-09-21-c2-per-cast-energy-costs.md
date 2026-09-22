# Research — C-2: per-cast energy cost, the four bound skills — 2026-09-21

**Mode:** A (analytical / primary-source probe)
**Commission:** **C-2**, issued under *The Commission Rule* (`gandalf/notes/2026-09-21-the-commission-rule.md`), Run KC2-PLAY
**Commissioner / conductor:** gandalf (RUN-CONDUCTOR)
**Agent:** legolas (UNKNOWN-RESEARCHER)
**Access:** read-only. No save, game file, pack or oracle modified. **No network fetch was made** (§ 7) — the question is answerable from primary sources and a guide could not outrank a DBR here.
**Companion:** `2026-09-21-s1-save-bio-block.md` (S-1) — shares the tooling and the rank method; ⚑ **S-1 carries a self-correction filed from this commission's work** (§ 6).

---

## HEADLINE

**All four have a per-activation energy cost. None of it is placeholder, none of it is zero, and the pack charges zero for all four.**

| skill | record | total rank | `skillManaCost` | **× 0.90** | cooldown | **/s at full uptime** |
|---|---|---|---|---|---|---|
| **Blitz** | `playerclass01/blitz1.dbr` | 5 | 42.0 | **37.8** | 3.5 s | 10.80 |
| ↳ *Blindside* (modifier) | `playerclass01/blitz2.dbr` | 7 | +6.0 | +5.4 | — | +1.54 |
| **Vire's Might** | `playerclass09/viremight1.dbr` | 2 | 26.0 | **23.4** | 3.6 s → **3.1 s** | 7.55 |
| ↳ *Volcanic Stride* | `playerclass09/viremight2.dbr` | 2 | ⚑ **none by design** | — | — | — |
| ↳ *Tectonic Shift* (modifier) | `playerclass09/viremight3.dbr` | 5 | +5.0 | +4.5 | −0.5 s | +1.45 |
| **War Cry** | `playerclass01/warcry1.dbr` | 16 | 50.0 | **45.0** | 7.5 s | 6.00 |
| ↳ *Break Morale* (modifier) | `playerclass01/warcry2.dbr` | 22 | **+68.0** | +61.2 | — | +8.16 |
| **Rune of Rush** — *Violent Delights* | `itemskillsgdx2/runes/rush_d203.dbr` | 1 (item skill, fixed) | 66.0 (scalar) | **59.4** | 2.5 s | 23.76 |

**Per activation, modifiers included:** Blitz **43.2** · Vire's Might **27.9** · War Cry **106.2** · Rune of Rush **59.4**.

⚑ **At perfect uptime — every skill cast the instant its cooldown ends — the four together draw ≈ 59.3 energy/s.** Against a measured regeneration of 75.37 /s, that is **79 % of the character's entire income**, spent by four buttons the pack models as free. Against the 176.4 /s channel it is a further **+34 %**. **This is not a rounding error in Matt's complaint; it is the missing half of it.**

⚑ **Break Morale is the shape nobody would have guessed: a modifier that costs MORE than the skill it modifies** — 68.0 against War Cry's own 50.0, because 12 allocated ranks are pushed to 22 by +skill gear and the array runs to 68 at its ceiling. War Cry is the referent's most expensive button by a factor of two, and the pack charges nothing for it while modelling its effect in full.

**Two corroborations and one contradiction, all reported:**

- ✅ **The 0.90 cost factor is confirmed, and it survived a check that could have broken it.** I went looking for a second reduction source and **found one** — the Owl devotion's `skillManaCostReduction = 5.0`. ⚑ **It is NOT allocated.** The Seal of Annihilation's 10 % is the character's only reduction, exactly as C-1 § 7 said. § 3.
- ✅ **It applies to all four, not only to Eye of Reckoning** — established, not assumed. § 3.
- ⚑ **CONTRADICTION, unreconciled:** the pack's `MO_ENERGY_RESERVATION = 982.0` cites *"Σ **7** DB-CITED aura reserves."* An exhaustive depth-6 walk of the save's entire allocation finds **5** reserving records totalling **682** at total ranks. **A 300-energy and 2-source gap.** § 5.

---

## 0 · Surfaces

| Surface | Status |
|---|---|
| **Game on disk — DBRs / ARZ** | ✅ **LIVE**, 8 archives, record counts matching the 2026-07-23 probe. ⚑ **Expansion-override precedence applied** (S-1 § 5) — `viremight*` and the rune skill live in `GDX2.arz`. |
| **Localization** | ✅ 20,394 tags across 7 `Text_EN.arc` |
| **Save** | ✅ `player.gdc` sha256 `b8e6f510…` — allocation and gear read for ranks |
| **Client tooltip figures** | ⚑ **NOT RECOVERABLE.** Only the FORMAT string ships (`ManaCost = "{^E}Energy Cost"`); the number is computed at runtime. C-1's 176.4 came from an **in-video** tooltip, and **the source MP4 is gone** (`/Users/admin/gd-scratch/eor-test-2/`, C-1 § 0). No re-measure possible this session. § 4 |
| **Skill-bar bindings** | ❌ the save's `ui_settings` block parsed EMPTY under the g7 reader. The four are taken from the commission, not confirmed from the save. Named, not glossed. |
| **Build guide / web** | ⚪ **NOT FETCHED.** Per the standing v1.2.0.0 constraint, a 1.1.9.x guide could not outrank a post-1.2 DBR on a cost value. **No robots.txt claim is made because no fetch was attempted.** |

**Tooling:** `legolas/scratch/2026-09-21-s1-bio/` — `arz.py` (precedence-correct), `gdcg7.py`, `arcread.py`, `tags.py`, `c2_ranks.py`, `ledger.py`.

---

## 1 · Total ranks — the method, and its positive control

A skill's `skillManaCost` is a **per-rank array**, so the cost depends on TOTAL rank, not allocated rank. Total rank = allocated (`level` in the save's skill block) + every `+skill` bonus the gear grants.

**Bonus sources enumerated across all 12 equipped items and their affix chains** (`c2_ranks.py`):

| source | bonus |
|---|---|
| `b201e_necklace.dbr` (Kaisan's Burning Eye) | `augmentAllLevel` **+1** — every class skill |
| `d028_head.dbr` (Warborn Visor) | `_classtraining_class01` **+1** — all Soldier skills |
| `d107_blunt2h.dbr` (Gutsmasher) | `_classtraining_class01` **+2** — all Soldier skills |
| `d007_feet.dbr` | `blitz2` **+2** |
| `d026_torso.dbr` | `warcry2` **+3** |
| `b016e_medal.dbr` | `warcry2` **+3**, `viremight3` **+3** |

⚑ **No item on this character grants `_classtraining_class09`** — the Oathkeeper skills receive only the necklace's universal +1.

**Two independent positive controls on the method, both EXACT:**

| control | computed | published |
|---|---|---|
| Eye of Reckoning total rank | 15 allocated + 4 (weapon) + 2 (head) + 2 (torso) + 2 (hands) + 1 (necklace) = **26** | `fixture.py` `EOR_TOTAL_RANK = 26` ✓ |
| `skillManaCost` at that rank | `eyeofreckoning1.dbr[26]` = **16.0** | `fixture.py` `SKILL_MANA_COST_R26 = 16.0` ✓ |
| Presence of Virtue buff total rank | 12 + 3 (hands) + 2 (waist) + 1 (necklace) = **18** | C-1 § 2.1 row 2, rank 18 ✓ |

**Resulting totals for the four:**

| skill | allocated | + all | + Soldier mastery | + specific | **total** |
|---|---|---|---|---|---|
| Blitz | 1 | +1 | +3 | — | **5** |
| Blindside | 1 | +1 | +3 | +2 (feet) | **7** |
| Vire's Might | 1 | +1 | — | — | **2** |
| Volcanic Stride | 1 | +1 | — | — | **2** |
| Tectonic Shift | 1 | +1 | — | +3 (medal) | **5** |
| War Cry | 12 | +1 | +3 | — | **16** |
| Break Morale | 12 | +1 | +3 | +3 (torso) +3 (medal) | **22** |
| Rune of Rush | — | ⚑ item skill, `itemSkillLevelEq = 1`, **not rank-scaled** | | | **1** |

**One boundary, declared:** I have **not** established whether `augmentAllLevel` / `augmentMasteryLevel` also raise the **mastery-bar** records (`_classtraining_class0N`). GD convention says no, and no source on this host states it either way. It does not affect C-2 (the four are not mastery bars) but it **would** raise S-1 § 2.2's attribute totals if it were true. ⚑ **Declared, not decided** — grade `CONVENTION-ASSUMED`, direction known (it can only raise).

---

## 2 · The costs, per record, with provenance

### 2.1 Blitz — *"Charge into battle"* (`tagClass01SkillName03A`)

| field | value | source |
|---|---|---|
| `skillManaCost` | array n=26, `[1] = 30.0` … `[5] = 42.0` … `[26] = 107.0` | `database.arz :: records/skills/playerclass01/blitz1.dbr` |
| `skillCooldownTime` | **3.5 s** (scalar) | same |
| `Class` | `Skill_AttackWeaponCharge` | same |
| `skillActiveManaCost` | ❌ absent — **not a channelled skill** | same |
| modifier **Blindside** `skillManaCost` | array n=22, `[7] = 6.0` | `database.arz :: playerclass01/blitz2.dbr`, `Class = Skill_Modifier` |

**→ 42.0 alone · 48.0 with Blindside · × 0.90 → 37.8 / 43.2 per cast.**

### 2.2 Vire's Might — *"Charge forward"* (`tagGDX2Class09SkillName04A`)

| field | value | source |
|---|---|---|
| `skillManaCost` | array n=26, `[1] = 22.0`, `[2] = 26.0`, `[26] = 122.0` | `GDX2.arz :: playerclass09/viremight1.dbr` |
| `skillCooldownTime` | **3.5999999 s** (scalar) | same |
| `Class` | `Skill_AttackPathCharge` | same |
| **Volcanic Stride** (`viremight2`) | ⚑ **NO `skillManaCost` field at all** | `GDX2.arz`, `Class = SkillSecondary_AttackProjectileAreaEffect` |
| **Tectonic Shift** (`viremight3`) `skillManaCost` | array n=22, `[5] = 5.0` | `GDX2.arz`, `Class = Skill_Modifier` |
| **Tectonic Shift** `skillCooldownTime` | array n=22, `[5] = **−0.5**` — a cooldown **reduction** | same |

**→ 26.0 alone · 31.0 with Tectonic Shift · × 0.90 → 23.4 / 27.9 per cast, on a 3.1 s cooldown.**

⚑ **Volcanic Stride is the commission's "no cost by design" case, and it is a clean one:** a `SkillSecondary_*` record that fires as a consequence of the parent and carries no cost field of any kind. Its absence is **structural**, not a gap — and that is a different thing from an unmodelled cost, which is what the other three are.

### 2.3 War Cry — *"A battle cry"* (`tagClass01SkillName04A`)

| field | value | source |
|---|---|---|
| `skillManaCost` | array n=22, `[1] = 20.0`, `[16] = 50.0`, `[22] = 62.0` | `database.arz :: playerclass01/warcry1.dbr` |
| `skillCooldownTime` | **7.5 s** (scalar) | same |
| `Class` | `Skill_AttackRadius` | same |
| ⚑ modifier **Break Morale** `skillManaCost` | array n=22, `[1] = 4.0`, **`[22] = 68.0`** (the array's ceiling) | `database.arz :: playerclass01/warcry2.dbr`, `Class = Skill_Modifier` |

**→ 50.0 alone · 118.0 with Break Morale · × 0.90 → 45.0 / 106.2 per cast.**

⚑ **The modifier costs more than the skill.** Break Morale is allocated to its cap of 12 and then pushed to 22 by +6 of gear and +1 of the universal bonus, landing on the last entry of its own array. **The +skill gear that makes the build strong is what makes this button expensive**, and a model that reads allocated rank instead of total rank would report 4.0 where the truth is 68.0 — a 17× understatement on the single most expensive activation the character has.

### 2.4 Rune of Rush — the item is **Rune of Violent Delights**

⚑ **Naming, corrected:** the commission calls it *Rune of Rush*. The record path is `rush_d203.dbr`, but the **item** is `tagGDX2RuneD203 = "Rune of Violent Delights"` and its **skill** is `tagGDX2RuneSkillD203 = "Violent Delights"`. A different rune, `B205`, is the one actually named `"Rush"` (item: *Emblem of the Charging Bull*) and **is not equipped**. Recorded so the registry row does not acquire the wrong name.

| field | value | source |
|---|---|---|
| `skillManaCost` | **66.0** — ⚑ **scalar, no array** | `GDX2.arz :: records/skills/itemskillsgdx2/runes/rush_d203.dbr` |
| `skillCooldownTime` | **2.5 s** | same |
| `skillMaxLevel` | 1 | same |
| `Class` | `Skill_AttackPathCharge` | same |
| granted by | `itemSkillName` on `GDX2.arz :: records/items/enchants/runes/d203_rune.dbr`, `itemSkillLevelEq = 1`, socketed in `b016e_medal.dbr` per `player.gdc` | |

**→ 66.0 × 0.90 → 59.4 per cast, on 2.5 s — the highest sustained energy-per-second of the four.**

### 2.5 The composition rule for modifiers — evidence, and its grade

A `Skill_Modifier`'s `skillManaCost` is an **increase to the parent's cost**. The client says so, for a different skill, in a sentence written to clarify the *timing* of an increase whose existence it assumes:

> `tagClass05SkillDescription06B` (**Disintegration**, `database.arz :: playerclass05/aetherray2.dbr`, `Class = Skill_Modifier`, `skillManaCost` array n=22):
> *"Pours all of your energy into the Aether Ray… ^o**Energy Cost increase** is per damage interval."*

⚑ **Grade split, deliberately:** that a modifier's `skillManaCost` is an **increase** is `CLIENT-VERBATIM`. That the total is exactly `parent + modifier` is the natural reading but is **`STRUCTURAL-INFERRED`** — no source states the arithmetic. **Both columns are given in every table above so a consumer can take the parent-only figure if it prefers the weaker claim.** The Eye of Reckoning control cannot settle it: `eyeofreckoning2.dbr` carries **no** `skillManaCost`, so C-1's byte-exact `16.0 × 12.25 × 0.90 = 176.4` is consistent with either rule and discriminates neither. **I checked, and I am reporting that the control I hoped for is silent.**

---

## 3 · The cost-reduction factor — confirmed for all four, and it survived a real challenge

The commission said *"confirm rather than assume."* I did, and the confirmation nearly broke.

**Step 1 — is `skillManaCostReduction` global or per-skill?** It is a **character stat**, not a skill property:

| tag | text |
|---|---|
| `tagCharStatsManaCostReduction` | `"Skill Energy Cost"` — a character-sheet row |
| `tagCharStatsManaCostReductionInfo` | *"The percent by which the energy cost of **your skills** is reduced."* |
| `SkillManaCostReduction` | `"-{%.0f0}% {^E} Skill Energy Cost"` — the item-affix display form |

Unqualified, plural, and displayed on the character sheet rather than on any skill. **There is no per-skill exemption field anywhere in the database.** Each of the four skill records carries its *own* `skillManaCostReduction = 0.0` slot, i.e. they all participate in the same stat system rather than standing outside it. **→ the reduction applies to all four.** Grade `CLIENT-VERBATIM` for class skills.

⚑ **Weaker for the item skill.** *Violent Delights* is granted by a rune augment, not by the skill tree. The client text says "your skills" without qualification and the record carries the same `skillManaCostReduction` slot, so the natural reading includes it — but nothing states it. **Grade `CLIENT-INFERRED` for Rune of Rush specifically.** If a consumer wants the conservative figure, it is **66.0 unreduced**, not 59.4.

**Step 2 — how many reduction sources does the character have?** An exhaustive walk of every allocated skill, every devotion node, every equipped item and every affix chain:

| source | value | allocated? |
|---|---|---|
| **Seal of Annihilation** — `GDX1.arz :: items/materia/compb_sealannihilation.dbr`, socketed in the necklace | `skillManaCostReduction = 10.0` | ✅ **yes** |
| ⚑ **Owl** (devotion) — `database.arz :: skills/devotion/tier1_12b.dbr` | `skillManaCostReduction = 5.0` | ❌ **NO — `level = 0`** |

⚑ **The Owl node is the challenge this section exists for.** Had it been allocated, the character's reduction would be 15 %, the factor would be ~0.85, and `16.0 × 12.25 × 0.85 = 166.6` would **contradict the client's own 176.4** — which would have put C-3 back in play and thrown the whole energy stack open.

**It is not allocated.** ⚑ **And the way I established that is itself the finding:** the save's devotion entries carry `devotionLevel = 1` on **all 285 devotion records in the file** — the entire tree, taken or not. The allocation flag is `level`, which is non-zero on exactly **55**, matching the bio block's `totalDevotionUnlocked = 55`. **`devotionLevel` is not the allocation field, and it returns a clean, plausible, non-zero value for every node in the game.** See § 6 — it cost me a wrong number in S-1 before it bought a right one here.

**→ `cost_factor = 0.90`, from exactly one source, applying to all four. C-1 § 7's C-3 solution stands, checked against a candidate that could have refuted it.**

---

## 4 · The registry absence, quantified

The commission's framing was right and the numbers sharpen it: **42 entries in the absence registry and none names a per-cast energy cost.** These four are not placeholder-inert — War Cry's *effect* is fully modelled — they are **unmodelled on the energy axis specifically**, while `per_tick_cost = 14.4` is the runtime's only energy debit.

**What the referent actually spends, as an upper bound:**

```
Blitz          43.2 / 3.5 s  = 12.34 /s
Vire's Might   27.9 / 3.1 s  =  9.00 /s
War Cry       106.2 / 7.5 s  = 14.16 /s
Rune of Rush   59.4 / 2.5 s  = 23.76 /s
                               --------
                                59.26 /s   at PERFECT uptime
```

⚑ **This is a BOUND, not a rate, and the distinction is the same one that convicted the `(86, 117)` band.** It assumes every skill recast the instant its cooldown ends — which no player achieves and which the footage would have to establish. **Realized cast frequency is the missing input**, and it is exactly the kind of quantity the footage could supply and the DBRs cannot. **I am not estimating it.** What the bound does establish is the **order**: the unmodelled per-cast axis is worth up to ~59 /s against a 75.37 /s income, so it is not a second-order term and cannot be waved off as one.

**No cooldown-reduction source exists on this character** — `skillCooldownReduction` is zero on every allocated record and every equipped item, so the cooldowns above are the real ones (with Tectonic Shift's −0.5 s the only adjustment).

**Client-side figure: NOT AVAILABLE.** Only the format string `ManaCost = "{^E}Energy Cost"` ships; the number is computed at runtime. The one route to a client-verbatim per-cast figure is a tooltip frame in the footage, and **the source MP4 is gone.** Grade for the client cross-check: ⚑ **`searched-SOURCE-UNLOCATED`.**

---

## 5 · ⚑ CONTRADICTION — the reservation count. I am not reconciling it.

`fixture.py`:
```
MO_ENERGY_RESERVATION = Cited(982.0, "spec §12 MO-2 — BINDING-and-derived, not hard-coded", "MEASURED")
micro_oracles.py:158  """MO-1. `energy_max` (MEASURED, 2576) − Σ 7 DB-CITED aura reserves − dead pct term."""
```

An exhaustive depth-6 walk of the save's entire allocation finds **five** records carrying `characterManaLimitReserve`:

| record | allocated rank | total rank | reserve @ total |
|---|---|---|---|
| `playerclass01/fieldcommand1buff.dbr` | 10 | 14 | 205.0 |
| `playerclass01/fieldcommand2.dbr` | 8 | 12 | 50.0 |
| `playerclass09/presenceofvirtue1_buff.dbr` | 12 | **18** | 220.0 ← C-1's V15-12 value, ✓ |
| `playerclass09/presenceofvirtue2.dbr` | 9 | 10 | 100.0 |
| `playerclass09/presenceofvirtue3.dbr` | 10 | 11 | 107.0 |
| | | **total** | **682.0** |

**982 − 682 = 300, and 7 − 5 = 2.** ⚑ **Both sides could be right and I cannot tell which.** My walk is bounded by the save's allocation and by the chain fields I follow; the pack's 982 is described as *derived*, and I have not read the derivation. **Reported with both numbers and both methods named.** Routed to gamora, whose `micro_oracles.py` owns MO-1/MO-2.

*(Note the same PoV rank-18 read appears on both sides, so the two methods do agree where they overlap. The gap is two whole sources, not a rank disagreement.)*

---

## 6 · ⚑ SELF-CORRECTION — S-1's attribute ledger, filed from this commission's work

C-2's cost-reduction check (§ 3 step 2) exposed a defect in S-1's ledger, **committed one hour earlier at `91c5a2a6`**. S-1's sweep used `max(level, devotionLevel) > 0` as the allocation predicate. **`devotionLevel` is non-zero on all 285 devotion records in the file**, so the sweep summed the ENTIRE devotion tree instead of the 55 allocated nodes.

**S-1 has been amended in place** (§ 2.2 table, § 4.2 arithmetic, § 3.2 Physique decomposition). Corrected, with the right predicate:

| | S-1 as filed | **corrected** |
|---|---|---|
| total Spirit (`characterIntelligence`, flat) | 536 | **396** |
| `characterIntelligenceModifier` | +6 % | ⚑ **0 % — no source at all** |
| total Physique (flat) | 1037 | **707** |
| total Cunning (flat) | 1429 | **1219** |
| C-1 § 5.1 residual, recomputed | ~10.5 /s | **≈19.0 /s** (Crate 0.26 %/pt) · **≈19.8 /s** (the 0.25 %/pt variant) |

⚑ **And the correction produced a positive control that S-1 got backwards.** S-1 § 4.2 flagged C-1's regen terms (19.7 flat / 63 %) for re-audit because the over-counted sweep read 30.3 / 118 %. With the right predicate my sweep reads:

- `characterManaRegenModifier` = **63.0 %** — Scales of Ulcama 33 + Jackal 10 + Arcane Spark 20. ⚑ **EXACTLY C-1's three rows and C-1's total.**
- `characterManaRegen` flat = **15.8**, and the entire difference from C-1's 19.7 is Presence of Virtue read at **allocated rank 12 (6.5)** instead of **total rank 18 (10.4)**. `15.8 + 3.9 = 19.7` ✓ **exact.** C-1 read the rank correctly; I did not.

**So C-1 § 2.1's regen ledger is independently corroborated, row for row. S-1's re-audit flag is RETRACTED.** The three S-1 corrections that survive are the ones that never depended on the sweep: the base-50 double count, the omission of the mastery bars (+194 Intelligence, unchanged) and devotions (+15, not +155), and the `manaIncrement`-per-level error.

⚑ **The shape, for the fourth time in this run and the second time in this file: an instrument that returned cleanly after it stopped answering the question.** `devotionLevel` is a real field with a plausible non-zero value on every row, and reading it as allocation produces a ledger that looks entirely reasonable and is wrong by 42 %. **It was caught only because a DIFFERENT question — "does a second cost-reduction source exist?" — happened to land on a node whose allocation status mattered.** Nothing in the ledger itself would ever have flagged it. That is the argument for the cross-check, not for more care.

---

## 7 · What did NOT close

| question | state |
|---|---|
| Client-verbatim per-cast figures for the four | ⚑ **`searched-SOURCE-UNLOCATED`** — only the format string ships; the footage MP4 is gone |
| Realized cast frequency (the input that turns the bound into a rate) | **NOT ATTEMPTED** — footage-only, and the footage is unavailable. Named as the missing input, not estimated |
| Whether `parent + modifier` is exactly the total | **`STRUCTURAL-INFERRED`** — the client asserts the increase exists; the arithmetic is unstated. Both columns given |
| Whether the 10 % reduction reaches item-granted skills | **`CLIENT-INFERRED`** for Rune of Rush; conservative figure 66.0 also given |
| Whether `augmentAllLevel` raises mastery-bar ranks | **`CONVENTION-ASSUMED`** — affects S-1's attribute totals, not C-2 |
| The 982 vs 682 reservation gap | ⚑ **UNRECONCILED, both sides reported** (§ 5) |
| Bar bindings from the save | ❌ `ui_settings` parsed empty under the g7 reader |

---

## 8 · Source list

**Primary — game files on disk** (`/Users/admin/depots/`, read-only, accessed 2026-09-21; expansion-override precedence applied)
- `database.arz` — `playerclass01/blitz1.dbr`, `blitz2.dbr`, `warcry1.dbr`, `warcry2.dbr`, `fieldcommand1buff.dbr`, `fieldcommand2.dbr`, `playerclass05/aetherray2.dbr`, `skills/devotion/tier1_12b.dbr`
- `GDX1.arz` — `items/materia/compb_sealannihilation.dbr`
- `GDX2.arz` — `playerclass09/viremight1.dbr`, `viremight2.dbr`, `viremight3.dbr`, `eyeofreckoning1.dbr`, `eyeofreckoning2.dbr`, `presenceofvirtue1_buff.dbr`, `presenceofvirtue2.dbr`, `presenceofvirtue3.dbr`, `itemskillsgdx2/runes/rush_d203.dbr`, `items/enchants/runes/d203_rune.dbr`, `skills/playerclass09/_classtraining_class09.dbr`
- 12 equipped item records + affix chains (`c2_ranks.py` output)
- `tags_ui.txt`, `tags_skills.txt`, `tagsgdx2_skills.txt` — `ManaCost`, `ActiveManaCost`, `ManaCostPerSecond`, `SkillManaCostReduction`, `tagCharStatsManaCostReduction(Info)`, `tagClass01SkillName03A/03B/04A/04B`, `tagGDX2Class09SkillName04A/04B/04C`, `tagGDX2RuneD203`, `tagGDX2RuneSkillD203`, `tagGDX2RuneSkillB205`, `tagClass05SkillDescription06B`

**Primary — save:** `player.gdc` sha256 `b8e6f510650dad0b12d60115d119b266283eda674c9c1a7186220ec93454bfa5`

**Internal:** `reincarnated-engine/src/reincarnated/simulation/kc2/fixture.py`, `micro_oracles.py` · `legolas/findings/2026-09-21-c1-off-channel-energy-recovery.md` §§ 2.1, 7 · `legolas/findings/2026-09-21-s1-save-bio-block.md` · `gandalf/notes/2026-09-21-the-commission-rule.md`

**Not consulted:** no web source.

---

**Filed by:** legolas (UNKNOWN-RESEARCHER), 2026-09-21. Read-only throughout.
