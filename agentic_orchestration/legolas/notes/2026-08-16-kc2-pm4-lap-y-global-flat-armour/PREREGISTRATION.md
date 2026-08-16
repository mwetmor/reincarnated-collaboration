# KC2-PM4 · LAP Y — PREREGISTRATION

**Agent:** legolas (UNKNOWN-RESEARCHER) · **Conductor:** gandalf (`RUN-CONDUCTOR`) · **2026-08-16**
**Commission:** ruling `R-PM4-63 part 4`. Charter rows `L-52`/`R-PM4-62` and `L-53`/`R-PM4-63`.
**Provenance of the question:** `UNREACHED-I23-3`, named-not-decoded by gamora in I-23 § 7.

> **THIS FILE IS COMMITTED ALONE, BEFORE ANY INSTRUMENT RUNS.** Fifth consecutive use; the commit
> graph is the attestation. Nothing below is edited after the instrument fires — grades are
> appended in `pm4y_findings.md`, never back-written here.

---

## § 0 — THE ONE QUESTION

For a single physical hit against the played character (`EoRWarlGuts`), what does the engine bind
to `sumProtectionDV` in `combatformulas.dbr`'s two armour equations?

```
physcialDamageDefenseEquationDLEP = physicalDamageDV * (1 - sumAbsorptionDV)
physicalDamageDefenseEquationDGP  = (sumProtectionDV * (1 - sumAbsorptionDV))
                                    + (physicalDamageDV - sumProtectionDV)
```

**Limb A — PIECE-ALONE.** `sumProtectionDV` = the armour of the equipment piece covering the rolled
`combatRegion*`, after that piece's *local* `defensiveProtectionModifier` and after the character's
global **percentage** armour (+56 %). This is what Lap X § 7's worked arithmetic used, and what
I-23's fold inherited **by lineage**.

**Limb B — PIECE-PLUS-GLOBAL-FLAT.** `sumProtectionDV` = the same, **plus** the character's global
**flat** armour bonus (+636 raw → **+992.16** after the +56 %).

**Third admissible answer — UNREACHED.** The corpus does not express it.

### 0.1 ⚑ THE STAKES ARE CONTEXT, NOT A TARGET (Law 3)

I record here, before looking, that I know which way the stakes point: I-23 reports that Limb B
flips the sign of its armour result (`0.84p − 2,050` → `0.84p − 2,884` against the incumbent's
`0.84p − 2,490`). **No term in this lap is adjusted toward any outcome.** The sign is not mine to
produce. I state my own bet in § 4 so that a wrong bet is visible in the git graph rather than
quietly retired.

### 0.2 ⚑ SCOPING DISCLOSURE

This is a **RECORD lap**. It runs **no simulation**, reads **no sim outcome**, and touches **no
baton**. It answers one decode question and reports collateral findings factually. It does not
re-open Lap X's other verdicts, does not re-grade I-23, and does not fold anything.

---

## § 1 — PINNED INPUTS (re-verified at instrument start; **HALT** on the first mismatch)

### 1.1 Carried from Lap X § 13.2 — values stated here verbatim, from Lap X, before re-hashing

| input | sha256 (expected) |
|---|---|
| `edition-III/database/database.arz` | `2ad6d379285cfb745462316949e8d59e9450cb58a13f9ffa2fdeb70193183bfd` |
| `edition-III/gdx1/database/GDX1.arz` | `431e64e1d372e4ebee5d1048d3aca458923e1df8c97844274636f5373a01e292` |
| `edition-III/gdx2/database/GDX2.arz` | `13fa0b93be15835958968ad672b9efa5159d7221a279aca791590390dd81a072` |
| `edition-III/gdx3/database/GDX3.arz` | `e990e1265f14ff2ee241658433d4d666d399a5b0be27543ae9481fc97d6a2ae4` |
| `edition-III/mods/survivalmode/database/SurvivalMode.arz` | `e9f6e2213eada8f5ffcc4fc430395b43c95384b745b629def096dbb2e7da29b6` |
| `edition-III/survivalmode1/database/SurvivalMode1.arz` | `6ac10d6180bfa8491edfc89946d1cfbf166c5ca6442c5862ecf6947290021252` |
| `edition-III/survivalmode2/database/SurvivalMode2.arz` | `940e40344e9dde53bfac8ff6576940d52ebfece600adeabe3774f9f0c3071e95` |
| `edition-III/survivalmode3/database/SurvivalMode3.arz` | `e848791e4b15496670e4c78832075d9868e7b502e6eed93715c24e894902e12a` |
| `edition-III/database/templates.arc` | `679db83f019020ef7d4d27be8e61203006ee94e5c582dd8a59642f3fddd54602` |
| `vendor/grim-dawn/Game.dll` | `4876d6bdb69cca71cfa987652cbd7a42cf6d5578564d02d09aaf9b55c078ab02` |
| `vendor/grim-dawn/Engine.dll` | `7141b51ae61b396fd0743da9e51471043329c51b3bb61d0037b2ce934864c87c` |
| `…/_EoRWarlGuts/player.gdc` | `b8e6f510650dad0b12d60115d119b266283eda674c9c1a7186220ec93454bfa5` |
| Lap A `measured-player-sheet.csv` | `6852794382b9bf608f13433ea18be7a52d1f2f0942801e5bb7c4e1be8899badd` |
| Lap G `pm4g_played_kit.csv` | `2fd5a34792b96125bd55a40891dfd65cdeb43c385c6ef06607486342d53ce0b3` |

### 1.2 Lap X outputs consumed as inputs — from `pm4x_digests.json`

| input | sha256 (expected) |
|---|---|
| `pm4x_player_defense.json` | `5fa9db84f3ae014cf48f926e1901fd9ea05c57a63162597b8c57e129f54cddf1` |
| `pm4x_formulas.json` | `cabc727d6711dfa3018be9f250811d841a32dbb8abcd1e41d752279bdd3f02a7` |
| `pm4x_player_defense_terms.csv` | `f4be3d8d4026226e6b6bfc758679f6e400ffb01aa4f6d40c73bdf06d49cdc993` |
| `pm4x_findings.md` | `6740e8eaf0dfe17ddce475320c1e27282b6de264804e7d3a334b18ff8d47f5f7` |

### 1.3 ⚑ NEW PINS established by this lap — digests computed **before** this file was committed

These are pure `sha256` of archive bytes. **Hashing a file is not an instrument run**; no content
was read to produce them.

| input | sha256 |
|---|---|
| `resources/Text_EN.arc` | `1105b1eef70c83914a00d0516ea6db3a25ed06fad8ec91757481e66879d58a27` |
| `gdx1/resources/Text_EN.arc` | `85baef4bd2a44eadadbb779c409cfa5238c4b4de2ce5182cb2ed9cf32797093a` |
| `gdx2/resources/Text_EN.arc` | `8aec9207b5dd0b33cb981455ec867d71ebc0d1646fa27e85b59b4556e8d814a1` |
| `gdx3/resources/Text_EN.arc` | `001b87bd0c52ac210ebf5fab42f94aef11ee68130b384776144de6443088dc08` |
| `mods/survivalmode/resources/Text_EN.arc` | `fa0689778ef0badb4472213684733e958edfbeeebb45086830939c9693b3d06e` |

---

## § 2 — EVIDENCE CLASSES I WILL CONSULT (declared closed; nothing added later without a defect row)

| id | class | what it can say | grade ceiling |
|---|---|---|---|
| **EC-1** | `templates.arc` **declarations** for the armour family — `defensiveProtection`, `defensiveProtectionModifier`, `defensiveProtectionChance`, `defensiveBonusProtection`, `defensiveAbsorption*`, and any `character*Armor*` field. Each `Variable` block carries `name` / `class` / `type` / `description` / `defaultValue`. | whether a field is declared as equipment-local or character-global, and whether any `description` states the composition | **DECODE** (shipped declaration) |
| **EC-2** | **carrier-class census** — `declaring_templates(field)` for each armour-family field. Which template families may carry it (armour vs. skill vs. pet vs. character). | separates "which records can hold it" from "how it is summed". Establishes the *carrier* fact only. | **DECODE** for carrier class; **cannot** settle summation alone |
| **EC-3** | **record sweep** of `combatformulas.dbr` + `gameengine.dbr` — every field, exhaustively, hunting a second protection variable, a composition declaration, or a per-region/aggregate switch. | whether the record expresses the answer **at all** | **DECODE** or **decoded-absent** |
| **EC-4** | **shipped UI text** (`Text_EN.arc` ×5) — every tag whose value mentions armour / absorption / body part / protection. Includes the character-sheet armour tooltip. | the game's own statement to the player about what armour does and what the sheet number is | **DECLARED** (shipped text is corpus, but a tooltip is a claim about behaviour, not the behaviour) |
| **EC-5** | **`Game.dll` string residency** for candidate composition symbols. | corroboration that a named accessor exists | **CORROBORATION ONLY** — `NOTE D-V2-1` honoured, **no vtable base reads**, no disassembly |
| **EC-6** | **arithmetic identity test** on Lap X's own pinned per-piece values and region weights vs. the camera-read sheet `3,557`. Tests: (a) is `M-AVG-PLUS-GLOBALFLAT` algebraically *identical* to the region-chance-weighted expectation of a per-piece `(piece + G)·M` operand? (b) does region-chance weighting beat unweighted simple averaging? (c) how far does piece-alone miss? | whether the **sheet** is the expectation of a piece-plus-global-flat operand | **IDENTITY** — see the grading rule in § 3 |

**Explicitly OUT of scope as decode evidence:** forum posts, wikis, community guides, grimtools.
Any such source may appear in the findings **only** as corroboration, labelled, never load-bearing
(standing rule; the grimtools-vs-`.arz` contradiction is why).

---

## § 3 — ⚑ THE GRADING RULE, PRE-COMMITTED

I fix the grade vocabulary **now** so that I cannot invent a flattering grade after seeing the
evidence.

- **DECODED** — requires a shipped statement (record field, template `description`, or shipped UI
  text) that **directly names** what enters the per-hit armour operand. Nothing weaker earns it.
- **DECODED-BY-IDENTITY** — available **only** on this exact condition, stated in advance: the
  camera-read sheet's winning model is *algebraically identical* to the
  `combatRegion*Chance`-weighted expectation of a per-piece operand, **and** those weights serve no
  other purpose in the corpus than the hit-location roll, **and** the competing limb's expectation
  misses the sheet by an order of magnitude more. This grade asserts the **sheet is the operand's
  expectation**; it does **not** assert a shipped statement exists.
- **UNREACHED** — EC-1…EC-5 are silent and the EC-6 condition above does not hold. **This is a
  fully acceptable return** and I will file it without embarrassment.

**A grade may not be upgraded by rhetoric.** If only EC-6 speaks, the verdict says so in the
headline.

---

## § 4 — PRE-REGISTERED PREDICTIONS, WITH MY BETS

| id | claim | my bet |
|---|---|---|
| `P-Y-1` | `templates.arc` separates carrier classes: `defensiveProtection` is declared on equipment/armour templates; the +636's carriers are declared on non-equipment (skill / devotion / component / character) templates | **PASS** |
| `P-Y-2` | ≥ 1 shipped `Text_EN.arc` tag describes armour as applying to a **body part / region / covered area**, i.e. the game tells the player armour is per-location | **PASS** |
| `P-Y-3` | `combatformulas.dbr` + `gameengine.dbr` contain **no** field expressing the composition of `sumProtectionDV` beyond the two equations — the record is **silent on the direct question** | **PASS** |
| `P-Y-4` | `Game.dll` carries ≥ 1 distinct resident string naming a character-level armour accessor separate from `defensiveProtection` | **PASS** (corroboration only) |
| `P-Y-5` | `E_w[(piece_after_local + 636) × 1.56] == 3,465.0346` **exactly** (≤ 1e-6 abs), i.e. Lap X's winner *is* the piece-plus-global-flat operand expectation restated; **and** unweighted simple averaging gives a strictly worse residual than region-chance weighting | **PASS** |
| `P-Y-6` | **THE VERDICT.** Which limb the lap lands on | **I bet PIECE-PLUS-GLOBAL-FLAT** |
| `P-Y-7` | `UNREACHED-X-1`'s −92 (−2.59 %) is **not** closed by this lap | **PASS** — it stays open |
| `P-Y-8` | ≥ 1 component of the +636 turns out on template evidence to be **item-local**, not global (which would be a **Lap X defect of mine**) | **FAIL** — I bet all 636 is genuinely global |

**Wording of a failed prediction is never rewritten** (Lap X `P-X-4b` precedent).

---

## § 5 — FALSIFIERS, ONE PER LIMB MINIMUM

| id | fires against | condition |
|---|---|---|
| `F-Y-A` | **Limb A (PIECE-ALONE)** | The sheet's winning model is exactly the region-chance-weighted expectation of `(piece + G)·M`, the weights being `combatRegion*Chance` — which the corpus uses for nothing but the hit roll — **and** the piece-alone expectation (`2,472.87`) misses the camera sheet by ≥ 25 %. Under these conditions Limb A survives **only** with positive evidence of a display-only path for the global flat. |
| `F-Y-B` | **Limb B (PIECE-PLUS-GLOBAL-FLAT)** | Any shipped declaration — template `description`, record field, or UI text — stating that a global armour bonus is **display-only**, or that it applies to a "total armour" quantity **distinct** from the armour of the struck piece; **or** the discovery of a second protection variable in the equations that separates the two. |
| `F-Y-C` | **the question as posed** | Any component of the +636 proves **item-local** on template evidence. Then "+636 global flat" is a mis-classification, the question must be re-posed per-source, and I file it as a **Lap X defect of my own** with a corrected split. |
| `F-Y-D` | **the DECODED grade** | EC-1…EC-5 all silent ⇒ no `DECODED`. Best available grade is `DECODED-BY-IDENTITY` or `UNREACHED`. |
| `F-Y-E` | **`M-AVG-PLUS-GLOBALFLAT` itself** | If unweighted simple averaging, or any *third* composition, closes the sheet better than `3,465.03` does, then Lap X's winner is not the winner and both limbs rest on a broken base. |

---

## § 6 — WHAT UNREACHED LOOKS LIKE (so I cannot quietly avoid returning it)

I return **UNREACHED** if, and only if:

1. no `templates.arc` `description` in the armour family states the composition; **and**
2. no field of `combatformulas.dbr` / `gameengine.dbr` names a second protection quantity or a
   composition rule; **and**
3. no shipped UI tag distinguishes "the armour of the piece hit" from "your total armour"; **and**
4. the `F-Y-A` identity condition fails — e.g. the sheet turns out **not** to be region-weighted, or
   a competing composition fits as well or better.

In that case the findings headline reads **UNREACHED**, both limbs are published with their
arithmetic, `UNREACHED-I23-3` stays **named, not decoded**, and I state plainly that the corpus
cannot settle it. **A weak answer is not upgraded to a strong one because a downstream fold wants
one.**

---

## § 7 — DISCIPLINE STACK ACKNOWLEDGED

- `R-PM4-55 part 2` — full 64-hex sha256 on every artifact; pinned inputs re-verified before use;
  **HALT** on drift.
- **Law 3** — the referent's numbers are GRADES, never inputs. The camera sheet `3,557` is a
  *measured witness of the game's own UI*, not a referent grade, and it is used as a **residual
  target for model selection only** — exactly as Lap X used it. No decoded value is adjusted to it.
- `R-PM4-56 part 4` — any genuinely NEW mechanism is **NAMED, not decoded**.
- `NOTE D-V2-1` — **no vtable base reads**; string residency is **CORROBORATION grade only**.
- `GL-12` — decode, never estimate.
- `NOTE-9` — every emitted quantity carries its own basis.
- **Defects** — self-caught defects go in the findings defect table with disposition;
  commission-premise errors are reported, not silently executed.
- **Determinism ×2** — every instrument runs twice, end to end; artifacts must be byte-identical.

## § 8 — OUTPUTS DECLARED IN ADVANCE

`pm4y_findings.md` · `pm4y_armour_operand.json` · `pm4y_template_declarations.csv` ·
`pm4y_ui_text.csv` · `pm4y_binary_anchors.json` · `pm4y_digests.json` · `decode.log`.
Instrument: `agentic_orchestration/research/scripts/pm4y_operand_2026_08_16.py`.

**Commit order:** this file **ALONE** → then instrument + all outputs. **No push** (conductor
pushes at banking).

---

*Pre-registered by legolas (UNKNOWN-RESEARCHER), 2026-08-16, before any instrument ran.*
