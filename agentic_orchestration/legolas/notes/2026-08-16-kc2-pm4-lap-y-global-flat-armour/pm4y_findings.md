# KC2-PM4 · LAP Y — WHAT `sumProtectionDV` IS FOR A SINGLE HIT

**Agent:** legolas (UNKNOWN-RESEARCHER) · **Conductor:** gandalf (`RUN-CONDUCTOR`) · **2026-08-16**
**Commission:** ruling `R-PM4-63 part 4`. Charter rows `L-52`/`R-PM4-62`, `L-53`/`R-PM4-63`.
**Provenance:** `UNREACHED-I23-3`, named-not-decoded by gamora in I-23 § 7.
**Pre-registration:** committed **ALONE** at `334c5b86`, before any instrument ran.

---

## § 0 — THE HEADLINE

> ### **VERDICT: PIECE **PLUS** GLOBAL FLAT.** Grade **DECODED**.
>
> The game ships the answer in its own words, wired into the Armor Rating rollover:
>
> ```
> tagCharStatsArmorTotalDescription =
>   "The higher your Armor Rating, the less damage you will take from physical attacks.
>    Bonuses on skills and on non-armor pieces are ADDED TO ALL ARMOR SLOTS."
> ```
>
> **"Added to all armor slots"** — not *added to your Armor Rating*. The slots are the six
> region-covering pieces the hit rolls against. The global flat armour is therefore inside the
> per-hit operand, on every region, and `sumProtectionDV` for a hit is
> **`(piece_after_local% + global_flat) × (1 + global%)`** = **piece + 992.16** on this build.
>
> **Lap X § 7's worked arithmetic used piece-alone. That is a defect of mine — `D-Y-1`, filed in
> § 8.** I-23 inherited it by lineage and is not at fault.

Three further returns, all of which the conductor should read before acting on the headline:

1. **The armour census partitions EXACTLY along the shipped sentence's own two categories, with
   zero remainder** (§ 4). 8,950 region-covering piece armour + 430 from skills/sets + 206 from
   non-armour pieces = 636 global flat. **`UNCLASSIFIED = 0.0`.** Falsifier `F-Y-C` did not fire.
2. **`UNREACHED-X-1`'s −92 is RESHAPED, NOT CLOSED** (§ 6). It is now known to be sensitive to a
   composition choice neither lap has decoded, and one candidate reading fits **better** than Lap
   X's winner. **I decline to designate it.**
3. **⚑ A NEW mechanism is NAMED, NOT DECODED — `UNREACHED-Y-1`** (§ 7): the scope of a
   **component's** `defensiveProtectionModifier` and `defensiveAbsorptionModifier`. It does **not**
   touch this lap's verdict, and it **does** have a large downstream consequence Lap X's absorption
   table depends on. Flagged, not folded.

---

## § 1 — THE GRADE, AGAINST THE RULE I PRE-COMMITTED

`PREREGISTRATION.md § 3` fixed the vocabulary before I looked, precisely so I could not invent a
flattering grade afterwards:

| grade | pre-registered condition | met? |
|---|---|:-:|
| **DECODED** | a shipped statement (record field, template `description`, or shipped UI text) that **directly names** what enters the per-hit armour operand | ⚑ **YES** |
| DECODED-BY-IDENTITY | the sheet-model identity condition | yes, but **not needed** — it is corroboration here, § 5 |
| UNREACHED | all classes silent | no |

**The lap lands on the strongest grade available, and it lands there on shipped text, not on
arithmetic.** The arithmetic (§ 5) agrees but is not load-bearing for the verdict. That ordering
matters: had the two disagreed, the shipped statement would still have won.

---

## § 2 — THE DECIDING EVIDENCE, WIRED END TO END

The sentence is not a loose string found by grepping. It is wired into the Armor Rating rollover
through three records and one template, all in the pinned base archive:

```
records/ui/character/characterinfotab1/charinfo_statsarmortotalrolloverstyle.dbr   [archive: base]
    templateName = database/templates/ingameui/combinedarmorrolloverwindow.tpl
    infoText     = records/ui/character/characterinfotab1/charinfo_statsarmorbreakdown_infotext.dbr
                   └─ textTag = tagCharStatsArmorTotalDescription
                                └─ Text_EN.arc  ⇒  the sentence above
```

The **whole** wired chain, from the instrument (`pm4y_ui_text.csv`, 29 rows):

| rollover field | textTag | shipped text |
|---|---|---|
| `titleText` | `tagCharStatsArmorTotal` | **`Armor Rating`** |
| **`infoText`** | **`tagCharStatsArmorTotalDescription`** | **⚑ the deciding sentence** |
| **`hitTitleText`** | **`tagCharStatsHitArmor`** | **`Chance to Hit Area`** |
| `absorptionTitle` | `tagCharStatsAbsorption` | `Armor Absorption` |
| `headText` / `chestText` / `shouldersText` / `handsText` / `legsText` / `feetText` | `tagCharStatsArmor…` | `Head:` `Chest:` `Shoulders:` `Arms:` `Legs:` `Feet:` |

⚑ **Read the second and third rows together.** The shipped rollover displays, per body region, an
armour number **and a `Chance to Hit Area`** — and the same window's info text says the bonuses go
into all the slots. The window is a per-region armour table keyed by hit chance. That is the
`combatRegion*Chance` roll, displayed to the player, with the global flat declared to be in every
row of it.

### 2.1 The template's own field set confirms the six-region grain

`combinedarmorrolloverwindow.tpl` declares, for **each** of head / chest / hands / legs / feet /
shoulders, a triple `<region>Text` · `<region>Number` · `<region>HitNumber` · plus
`<region>AbsorptionNumber`. Six regions, no seventh. It also declares `unprotectedTag`
(= `Unprotected`), matching `combatRegionUnprotectedChance = 0`.

### 2.2 ⚑ SEVEN ORPHANED BREAKDOWN RECORDS — reported factually, not interpreted

29 `charinfo_statsarmorbreakdown_*` records exist. **Seven are referenced by nothing in the entire
84,829-record corpus** (`pm4y_ui_text.csv :: wired_into_rollover = False`):

```
bonustext · bonusnumber · bonushitnumber · waisttext · waistnumber · jewelrytext · jewelrynumber
```

with shipped tags `tagCharStatsArmorBonus` = `Bonus:`, `tagCharStatsArmorWaist` = `Waist:`,
`tagCharStatsArmorJewelry` = `Jewelry:`. So the build **once** displayed Waist, Jewelry and Bonus
as **separate rows** of the armour breakdown, and no longer does.

Corroborating lineage detail: `defensiveBonusProtection` is declared in
`templatebase/parameters_defensive.tpl` **only** — the parallel `backup/parameters_defensive.tpl`
declares the other eight defensive-protection fields but **not** that one. The "Bonus Armor" field
is a **later addition** to the schema.

> **This paragraph is INFERENCE and is labelled as such:** the orphaning is *consistent with* a
> design change from "show Waist/Jewelry/Bonus as their own rows" to "fold them into every slot and
> say so in the info text." **I do not claim that as decoded.** The decoded facts are: the seven
> records exist, carry those tags, and are referenced by nothing.

---

## § 3 — WHAT THE OTHER EVIDENCE CLASSES RETURNED

| class | result |
|---|---|
| **EC-1** template `description` for the armour family | ⚑ **SILENT.** All nine `parameters_defensive.tpl` protection/absorption fields are declared bare — `class=array`, `type=real`, `defaultValue=0`, **no `description`**. The templates do not state composition. |
| **EC-2** carrier-class census | ⚑ **SPEAKS, structurally.** `armorClassification` is declared on **exactly six** templates: `armor_chest` `armor_feet` `armor_hands` `armor_head` `armor_legs` `armor_shoulders`. There are **nine** `armor_*.tpl`; the three without it are `armor_clothing`, `armor_vestment`, **`armor_waist`**. Six region-covering armour templates against six `combatRegion*Chance` fields summing to exactly 100. |
| **EC-3** record sweep | ⚑ **DECODED-ABSENT.** `sumProtectionDV` appears in **exactly one** field of `combatformulas.dbr` (`physicalDamageDefenseEquationDGP`). No second protection variable. No composition field. `gameengine.dbr` carries one armour field (`armorDefensiveAbsorption`). **The record does not express the answer** — `P-Y-3` PASSED. |
| **EC-4** shipped UI text | ⚑ **THE VERDICT.** § 2. |
| **EC-5** binary residency (**CORROBORATION ONLY**, `NOTE D-V2-1`, no vtable base reads) | `Game.dll` resident: `sumProtectionDV` `0x005273a4` (byte-identical to Lap X's RVA), `sumAbsorptionDV` `0x005273cc`, `physicalDamageDV` `0x00527390`, `defensiveProtection` `0x005407ac`, **`defensiveBonusProtection` `0x0054169c`**, `armorClassification` `0x004ef420`, `armorDefensiveAbsorption` `0x0054c31c`, `combatRegionHeadChance` `0x0052634c`. `Engine.dll`: **0 / 19**. The UI *tag* names are resident in **neither** binary — they are resolved through `Text_EN.arc`, so `P-Y-4` **FAILED** as worded. |

⚑ **`defensiveBonusProtection` being resident in `Game.dll` as a distinct symbol from
`defensiveProtection` is the corroboration that matters** — the engine resolves a *separate* named
field for "Bonus Armor". It carries no magnitude, and I do not let it carry one.

---

## § 4 — ⚑ THE PARTITION TEST: THE SHIPPED SENTENCE NAMES **EVERY** TERM OF THE +636

The sentence names two categories. I partitioned Lap X's **pinned** 175-row armour census
(`pm4x_player_defense_terms.csv`, sha `f4be3d…d993`, re-verified EXACT) into those two categories
plus "region-covering piece armour", with an `UNCLASSIFIED` bucket armed as the `F-Y-C` falsifier.

| bucket | value | members |
|---|---:|---|
| region-covering piece armour | **8,950.0** | the six `defensiveProtection` values on `armor_{head,chest,legs,shoulders,feet,hands}.tpl` |
| **"bonuses on skills"** | **430.0** | devotions `tier1_29a/b/c` `tier2_05c/e` `tier3_20b` = 20+20+40+60+80+90 = 310; Warborn 3-piece set `defensiveBonusProtection` = 120 |
| **"…and on non-armor pieces"** | **206.0** | waist base `defensiveProtection` 96 (`armor_waist.tpl` — **no `armorClassification`**); ring-2 component `defensiveProtection` 75 (`itemrelic.tpl`); legs component `defensiveBonusProtection` 35 (`itemrelic.tpl`) |
| **`UNCLASSIFIED`** | **0.0** | ⚑ **`F-Y-C` DID NOT FIRE** |

**430 + 206 = 636.0 — exactly Lap X's global flat, to the last digit.** `P-Y-8` **FAILED as I bet
it would**: no component of the +636 proves item-local. Lap X's classification is vindicated.

> ⚑ **This is the finding that makes the verdict robust rather than merely textual.** The shipped
> sentence's two categories are not a loose gloss — they *exhaustively enumerate* the +636 and
> nothing else, and they exclude every one of the six region-covering pieces. Two independently
> derived quantities (a 2013-era tooltip's taxonomy; a 175-row 2026 census) partition the same
> number the same way with zero remainder.

---

## § 5 — THE ARITHMETIC, AND WHY IT IS CORROBORATION AND NOT THE VERDICT

### 5.1 The identity, and what it retires

Because the six region chances sum to **exactly 1.000**, adding the global flat *outside* the
weighted sum is **algebraically identical** to adding it to *every piece inside*:

```
(Σ_s w_s · A_s + G) · M   ≡   Σ_s w_s · [(A_s + G) · M]        when Σ_s w_s = 1
        3,465.03456        =        3,465.03456        |Δ| = 0.0 exactly
```

**Lap X's winning sheet model was always the piece-plus-global-flat operand's expectation.** It was
never a competing description; it was the same description, written the other way round. Lap X
§ 2.4 selected it, and Lap X § 7 then failed to carry it into the hit. `P-Y-5` **PASSED**.

### 5.2 The `F-Y-E` composition grid — all nine, sorted by fit, none suppressed

Camera sheet **3,557**. *(Law 3: a residual target for model SELECTION only. No decoded value was
adjusted toward it. This is exactly Lap X's own use.)*

| model | limb | value | residual | % |
|---|---|---:|---:|---:|
| `C7` component % read as **GLOBAL**, weighted | **B** | 3,603.3424 | **+46.3424** | **+1.303 %** |
| `C3` global flat added **before** the local %, weighted | **B** | 3,480.9091 | −76.0909 | −2.139 % |
| **`C1`** Lap X's winner (G outside the weighted sum) | **B** | 3,465.0346 | −91.9654 | −2.585 % |
| `C2` G added to **every piece** (≡ `C1`) | **B** | 3,465.0346 | −91.9654 | −2.585 % |
| `C4` G outside, **simple** average | **B** | 3,350.3808 | −206.6192 | −5.809 % |
| `C8` G **unscaled** by the global % | **B** | 3,108.8746 | −448.1254 | −12.598 % |
| `A1` **piece-alone**, weighted | **A** | 2,472.8746 | **−1,084.1254** | **−30.479 %** |
| `A3` piece-alone, weighted, no local % | **A** | 2,435.4096 | −1,121.5904 | −31.532 % |
| `A2` piece-alone, simple average | **A** | 2,358.2208 | −1,198.7792 | −33.702 % |

**Every Limb-B composition sits within 12.6 %; four sit within 2.6 %. The *best* Limb-A composition
misses by 30.5 %.** `F-Y-A` fires with room to spare.

Stated the other way: for **piece-alone** to reach the sheet, the build would need **124.39 %**
global armour. The census reaches **56 %**. **Piece-alone is not off by a rounding error; it is off
by more than double the entire global-percentage stack.**

`F-Y-B` — the falsifier armed against my own bet — **did not fire.** No template, no record field,
no shipped string anywhere describes the global flat as display-only or names a "total armour"
quantity distinct from the struck piece's. The one shipped statement on the subject says the
opposite.

### 5.3 Region-weighting beats simple averaging, on both limbs

`C1` (−2.585 %) beats `C4` (−5.809 %); `A1` (−30.479 %) beats `A2` (−33.702 %). The sheet is
weighted by `combatRegion*Chance`, and those weights serve exactly one other purpose in the corpus:
the hit-location roll. `P-Y-5`'s second clause **PASSED**.

---

## § 6 — ⚑ `UNREACHED-X-1` (the −92): **RESHAPED, NOT CLOSED**

`P-Y-7` **PASSED** — the −92 is not closed. But it does not survive this lap unchanged, and saying
only "still open" would be under-reporting.

**What changed.** The −92 was Lap X's residual under **one** composition. The grid shows the
residual is a **function of two composition choices neither lap has decoded**:

| choice | Lap X's reading | the alternative | residual under the alternative |
|---|---|---|---|
| does the piece's **local %** apply to the global flat too? | no (`C1`) | yes (`C3`) | **−76.09** (−2.139 %) |
| is a **component's** `defensiveProtectionModifier` local or global? | local (`C1`) | global (`C7`) | **+46.34** (+1.303 %) |

**Both alternatives fit better than Lap X's winner. `C7` fits best of all nine.** `F-Y-E`
therefore **PARTIALLY FIRES**: Lap X's `M-AVG-PLUS-GLOBALFLAT` is *not* the best-fitting
composition in the grid.

> ### ⚑ AND I AM NOT DESIGNATING `C7`.
> `C7` fits best. It is also the composition that would "close the residual by adjusting a term" —
> the exact move Lap X's `UNREACHED-X-1` forbids and gamora refused in I-23 § 7 for the same reason.
> A better residual is **not** decode authority. `C7` rests on `UNREACHED-Y-1` (§ 7), which is
> undecoded. **The primary composition stays `C1`, by lineage, never by grade** — the same
> discipline Lap X applied to the armour-vs-resist order fork (`UNREACHED-X-4`).
>
> The gap **expressed** in each currency, for the record and for nobody's use as an input: `C1`
> would need **60.14 %** global armour (census: 56) **or** **694.95** global flat (census: 636).
> **Neither is applied.**

**Net:** `UNREACHED-X-1` stays **OPEN**, with its cause narrowed from "≈4 points of global armour
from an unreached source" to "one of two undecoded composition choices, or a source outside the
census, or both."

---

## § 7 — ⚑ `UNREACHED-Y-1` — NAMED, NOT DECODED (`R-PM4-56 part 4`)

**The mechanism:** *when a **component** (`itemrelic.tpl`) socketed into a region-covering armour
piece carries a **modifier** field — `defensiveProtectionModifier`, `defensiveAbsorptionModifier` —
is that modifier **local to the host piece** or **global to all six slots**?*

**Why it is genuinely open, stated with the tension intact and not resolved:**

- **For LOCAL** (Lap X's reading): the same legs component record carries **both**
  `defensiveProtectionModifier = 8` **and** `defensiveBonusProtection = 35`. Two protection fields
  on one record is only meaningful if they have different scopes — which is why
  `defensiveBonusProtection` exists as a separate symbol at all (and it *is* a separate symbol in
  `Game.dll`, § 3).
- **For GLOBAL:** the shipped sentence says bonuses on **non-armor pieces** go to all armor slots,
  and a component's template is `itemrelic.tpl` — **not** an armour template, and not one of the
  six carrying `armorClassification`. On that reading the component's 8 % is global, which is `C7`,
  which fits the sheet best.

**I do not adjudicate it.** No shipped text, template `description`, record field or resident
string distinguishes modifier scope by carrier.

### 7.1 ⚑ THE DOWNSTREAM CONSEQUENCE THE CONDUCTOR MUST SEE — flagged, **not** folded

The same question governs **`defensiveAbsorptionModifier`**, and there the swing is much larger
than on armour. Lap X § 2.5 treats the legs component's **8** and the shoulders component's **12**
as local:

| reading | head / chest / feet / hands | legs | shoulders |
|---|---:|---:|---:|
| **Lap X (component mods LOCAL)** | 98.0 % | 106 → **clamped 100** | 110 → **clamped 100** |
| **component mods GLOBAL** | `70 + 48` = 118 → **clamped 100** | **100** | **100** |

**Under the global reading, absorption is 100 % on every region**, and the physical line of every
`damage ≤ armour` hit goes to **exactly zero** rather than Lap X § 7's 32.25. On the worked hit
that moves the physical contribution 17.61 HP → 0.00 HP — a **3.75 %** move on a 469.40 HP round,
and **0 %** on this build's lightning-dominated intake.

> **So: `UNREACHED-Y-1` is load-bearing for the sheet residual and NOT load-bearing for intake on
> this build.** I state both halves so nobody reads the flag as bigger or smaller than it is. **It
> does not touch Lap Y's verdict at all** — `C1`, `C3` and `C7` are all Limb B.

---

## § 8 — DEFECT TABLE

| id | defect | severity | who | disposition |
|---|---|---|---|---|
| **`D-Y-1`** | **⚑ MINE, LAP X.** § 7's worked per-hit arithmetic used `sumProtectionDV` = the rolled piece **alone**, while the same note's § 2.4 selected a sheet model that *is* (identically, § 5.1) the piece-**plus**-global-flat expectation. **Lap X contradicted itself between § 2.4 and § 7 and I did not catch it.** The evidence that settles it — `tagCharStatsArmorTotalDescription` — was inside Lap X's own pinned `Text_EN.arc` intake, which Lap X used (for the `damageAbsorption` UI discriminator, § 5.1) and did not query for armour. | **HIGH** | legolas | **OPEN → CORRECTED HERE.** Lap X § 7's operand is superseded: per-region armour becomes piece + **992.16**. Under either operand the § 7 hit stays on the DLEP branch (1,612.3 ≪ every piece), so **the worked 469.40 HP/round does not change**; the correction bites where the DGP branch fires. |
| **`D-Y-2`** | I-23's fold inherited `D-Y-1` **by lineage**, correctly and transparently, and gamora **named the gap rather than papering it** (`UNREACHED-I23-3`). | **INFO** | gamora | **NOT A DEFECT OF I-23.** Recorded so the correction's provenance is unambiguous: the error is Lap X's, the escalation was correct. |
| **`D-Y-3`** | **MINE, THIS LAP.** My first `F-Y-C` scan covered only the `EQUIP` gear list and so reported the `defensiveBonusProtection` carriers as `[legs component 35]` — omitting the Warborn 3-piece 120 and the devotion 310, which are set/skill carriers outside `EQUIP`. Had I stopped there I would have under-counted the global flat by 430 and mis-stated the partition. | **MEDIUM** | legolas | **SELF-CAUGHT AND REPAIRED before any verdict was written**, by extending the test to Lap X's pinned full 175-row census. The repaired partition (§ 4) closes to `UNCLASSIFIED = 0.0`. Both the gear-scan rows and the census rows ship in `pm4y_kit_carriers.csv`. |
| **`D-Y-4`** | `P-Y-4` was worded as a bet that `Game.dll` carries a character-level armour **accessor** string; it carries the **field** names but the UI **tag** names live only in `Text_EN.arc`. The prediction was mis-specified about where UI tags reside. | **LOW** | legolas | **FAILED AS WORDED, wording not rewritten** (`P-X-4b` precedent). No verdict depended on it — EC-5 is CORROBORATION grade by construction. |

**No commission-premise error found.** The commission's framing of `UNREACHED-I23-3` — including
its statement that the question "is expressed by no field either lap reached" — was **accurate**:
no *field* expresses it. It is expressed by a shipped **UI string**, which is a class neither lap
had queried for armour.

---

## § 9 — THE PRE-REGISTERED PREDICTIONS, GRADED

| id | claim | grade | number |
|---|---|---|---|
| `P-Y-1` | templates separate carrier classes | ⚑ **SPLIT** | Carrier separation **PASSED** structurally (`armorClassification` on exactly 6 of 9 `armor_*.tpl`), but the *mechanism* I predicted — separation visible in the **declarations** — **FAILED**: all nine defensive-protection fields are declared in **one** shared `parameters_defensive.tpl` with **no `description`**. |
| `P-Y-2` | ≥1 shipped tag describes armour as per-body-part | **PASSED** | `tagCharStatsHitArmor` = `Chance to Hit Area`, plus six per-region row tags and `tagCharStatsArmorUnprotected` |
| `P-Y-3` | the **record** is silent on the composition | **PASSED** | `sumProtectionDV` occurs in exactly **1** field corpus-wide; 0 second protection variables; 0 composition fields |
| `P-Y-4` | `Game.dll` carries a character-level armour **accessor** string | ⚑ **FAILED — my bet** | field names resident (8/8), UI tag names **0/8** in either binary |
| `P-Y-5` | the identity holds exactly; weighting beats simple averaging | **PASSED** | `\|C1−C2\| = 0.0` exactly; `C1` −2.585 % vs `C4` −5.809 % |
| **`P-Y-6`** | **the verdict: PIECE-PLUS-GLOBAL-FLAT** | ⚑ **PASSED — my bet, and it was called before I looked** | DECODED on shipped text |
| `P-Y-7` | `UNREACHED-X-1` not closed | **PASSED** | open; **reshaped**, § 6 |
| `P-Y-8` | ≥1 component of the +636 proves item-local | **FAILED — as I bet** | partition `UNCLASSIFIED = 0.0` |

**Six of eight bets called correctly; two failed and their wording stands unedited.**

### 9.1 Falsifiers

| id | fires against | outcome |
|---|---|---|
| `F-Y-A` | Limb A | ⚑ **FIRED.** Identity exact; piece-alone misses by −30.479 %; piece-alone would need 124.39 % global armour |
| `F-Y-B` | Limb B | **DID NOT FIRE.** 0 display-only statements; 0 second protection variables |
| `F-Y-C` | the question as posed | **DID NOT FIRE.** `UNCLASSIFIED = 0.0` |
| `F-Y-D` | the DECODED grade | **DID NOT FIRE.** EC-4 spoke; DECODED earned on shipped text |
| `F-Y-E` | Lap X's own winning sheet model | ⚑ **PARTIALLY FIRED.** `C3` and `C7` both fit better than `C1`. Reported in § 6; **`C7` explicitly NOT designated** |

---

## § 10 — UNREACHED CENSUS

| id | what | status |
|---|---|---|
| **`UNREACHED-I23-3`** | piece-alone vs piece + global flat as `sumProtectionDV` | ⚑ **CLOSED — DECODED as piece + global flat**, on shipped text wired to the Armor Rating rollover |
| `UNREACHED-X-1` | the −92 (−2.59 %) armour residual | **OPEN. RESHAPED, NOT CLOSED** (§ 6). Cause narrowed to two undecoded composition choices and/or a source outside the census |
| **`UNREACHED-Y-1`** | **NEW.** scope of a **component's** `defensiveProtectionModifier` / `defensiveAbsorptionModifier` — local to the host piece, or global to all slots | ⚑ **NAMED, NOT DECODED** (`R-PM4-56 part 4`). Load-bearing for the sheet residual; **not** load-bearing for intake on this build; **does not touch Lap Y's verdict** |
| `UNREACHED-X-4` | armour-vs-resist order | untouched by this lap |
| `UNREACHED-X-9` | the absorption clamp at 100 % | untouched, but see § 7.1 — `UNREACHED-Y-1` changes **which regions** reach the clamp |

---

## § 11 — WHAT THIS MEANS FOR THE FOLD (mine to state, not to decide)

Stated factually. The conductor and gamora decide.

1. **The per-hit armour operand for region `s` is `(A_s + 992.16)`**, where `A_s` is the piece's
   armour after its local % and after the global +56 %, and `992.16 = 636 × 1.56`. Per region:
   chest **3,968.7** · legs **3,521.1** · head **3,591.2** · shoulders **3,591.2** · feet
   **2,716.0** · hands **2,714.4**.
2. **The sheet 3,557 stays DEMOTED** (I-23 `N-3`). It is the hit-weighted **average** of those six,
   still not an operand for a hit. Lap X § 2.4 and I-23 § 8 both stand.
3. **The direction of I-23's armour result flips**, exactly as gamora predicted it would: `DGP`
   moves `0.84p − 2,050` → `0.84p − 2,884` against the incumbent's `0.84p − 2,490`. **That is a
   consequence of the decode, not a reason for it** — the decode was called on shipped text before
   the arithmetic ran, and the shipped text does not know what the fold wants.
4. **Nothing else in Lap X moves.** The physical/only type scope, the six-region roll, the caps, the
   absorption limbs, block DECODED-ABSENT, `Ascension = 30 FLAT` — all untouched.
5. **Under either operand, Lap X § 7's worked 469.40 HP/round is unchanged** (the hit is DLEP on
   every region under both). The correction bites on **DGP-branch** hits — bigger physical hits than
   band-A monsters throw on this board.
6. **DO-NOT:** do not fold `C3`, `C7`, or `UNREACHED-Y-1`. Do not close `UNREACHED-X-1` by moving a
   term. Do not read `C7`'s better residual as authority.

---

## § 12 — DIGESTS (full 64 hex throughout, `R-PM4-55 part 2`)

### 12.1 Outputs of this lap

See `pm4y_digests.json` — it is the authority for `pm4y_findings.md`'s own digest (a file cannot
carry its own).

### 12.2 Inputs — pinned in `PREREGISTRATION.md § 1`, re-verified **20/20 EXACT** at instrument start

HALT armed; **none fired**. Full list in `decode.log § 0` and `pm4y_armour_operand.json :: pins`.
The 16 corpus/binary pins are byte-identical to Lap X's; the four Lap X output pins are
byte-identical to `pm4x_digests.json`; the five `Text_EN.arc` pins are **new to this lap** and were
computed **before** `PREREGISTRATION.md` was committed (hashing a file is not an instrument run).

### 12.3 Instrument

| instrument | sha256 | role |
|---|---|---|
| `research/scripts/pm4y_operand_2026_08_16.py` | *(see `pm4y_digests.json`)* | pins · EC-1…EC-6 · partition test · composition grid · verdict |

Carried readers — `pm4g_lib`, `pm4f_lib`, `pm4l_emit`, `s2_lib`, `gd_arz_adapter`, `gd_arc_reader`
— **imported, never re-implemented** (`NOTE-9`).

### 12.4 Determinism ×2 (FG-10 form)

The instrument was run a **second, real execution** end to end. **All 7 emitted artefacts are
byte-identical** to pass 1: `pm4y_armour_operand.json`, `pm4y_binary_anchors.json`,
`pm4y_composition_grid.csv`, `pm4y_kit_carriers.csv`, `pm4y_template_declarations.csv`,
`pm4y_ui_text.csv`, `decode.log`. The lap draws no RNG and reads no wall clock.

### 12.5 The firewall, discharged

This lap read **no** sim outcome, touched **no** baton, ran **no** simulation, and consumed **no**
referent grade. The camera-read sheet `3,557` entered only as a residual target for model
**selection**, which is precisely and only how Lap X used it. **Not one decoded value was adjusted
toward any number.**

---

*Lap Y closed by legolas (UNKNOWN-RESEARCHER), 2026-08-16. Read-only throughout; nothing outside
this notes directory and `agentic_orchestration/research/scripts/` was written. Not pushed — the
conductor pushes at banking.*
