# KC2 MODEL-COMPLETION RUN · D-4b — the DoT FIGURE-CONVENTION decode (TOTAL vs PER-SECOND)

> **Run:** KC2 Model-Completion (charter `agentic_orchestration/gandalf/notes/2026-08-24-kc2-model-completion-run-charter.md`) · **Conductor:** gandalf (`RUN-CONDUCTOR`) · ledger **L-24 / L-25**
> **Author:** legolas (UNKNOWN-RESEARCHER) · **Date:** 2026-08-24
> **Named target:** close Lap I § 5.1's DECLARED GAP — are the 264 rider rows' `offensiveSlow<X>Min/Max` values TOTAL-over-duration or PER-SECOND?
> **Laws:** READ-ONLY on every source · **Law 3 — decode-before-declare, no fitted constants, no invented rules** · GL-12 decode-never-estimate · NOTE-9 every quantity asserts its basis · GL-6 digests (§ 8).

---

## VERDICT — **PER-SECOND**, decoded from the engine binary

**`offensiveSlow<X>Min/Max` is a PER-SECOND RATE.** `offensiveSlowPoisonMin = 890` with
`offensiveSlowPoisonDurationMin = 5.0` means **890 HP/s for 5 s (4,450 total)**, not 890 total (178 dps).

This is not inferred from tooltips or community sources. It is read off the application math in
`Game.dll`, from two bit-exact float constants and one integer constant on the path that every
`offensiveSlow*` rider takes:

| # | site (Game.dll RVA) | instruction | meaning |
|---|---|---|---|
| **C-1** | `0x0020d6f6` | `mulss xmm0, [0x105f58a4]` → `cvttss2si` | **`nTicks = (int)(duration × 10.0f)`** |
| **C-2** | `0x0020d7b5` | `mulss xmm1, [0x105f57ac]` | **`perTick = damage × 0.1f`** |
| **C-3** | `0x00207f76` | `cmp edi, 0x64` (+ magic-number `/100`) | **tick cadence = 100 ms** |

Constants verified bit-exact, not "approximately": `0x5f58a4` = `00002041` = `10.0f`;
`0x5f57ac` = `cdcccc3d` = `0.1f`.

**The arithmetic that settles it.** A tick fires every 100 ms and delivers `damage × 0.1`.
Ten ticks per second ⇒ **`damage × 0.1 × 10 = damage` HP per second**. The effect runs for
`nTicks = duration × 10` ticks ⇒ exactly `duration` seconds. Total delivered = `damage × duration`.

> The field multiplies the *rate*, and the duration multiplies the *tick count*. The two are
> orthogonal, and that is only true of a per-second convention. Under TOTAL, `perTick` would have
> had to carry a `1/duration` term. **It does not — see the division scan below.**

### The negative that carries the verdict

**Zero float-division instructions exist anywhere in the ten-function application chain** — the
decisive absence, since a divide-by-duration is the TOTAL signature. Scanned for
`divss/divps/divsd/divpd/fdiv/fdivp/fdivr/fdivrp/fidiv/fidivr` (`d4b_step4_verify.py`, § V2):

| function | RVA | float-div sites |
|---|---|---:|
| `DamageAttributeDur::AddDamageToAccumulator` (rolls the `.dbr` value) | `0x1425b0` | **0** |
| `CombatAttributeDurDamage::ctor` | `0x000d7c80` | **0** |
| `CombatAttributeDurDamage::Process` | `0x000d7dd0` | **0** |
| `CombatAttributeDurDamage::Execute` | `0x000d80c0` | **0** |
| `DurationDamageManager::AddDamage` | `0x00208a30` | **0** |
| `DurationDamageManager::ModifyDuration` | `0x00209db0` | **0** |
| entry insert/merge (vtable slot 1) | `0x0020d6b0` | **0** |
| entry per-tick sum (vtable slot 2) | `0x0020da10` | **0** |
| `DurationDamageManager::ExecuteDamage` | `0x00208370` | **0** |
| `DurationDamageManager::Update` | `0x00207f40` | **0** |

---

## 1 — THE FULL CHAIN, `.dbr` field → HP loss

Every step below is a named export at a named RVA; listings banked under `evidence/E*.asm`.

```
records/**/*.dbr :  offensiveSlow<X>Min / Max / DurationMin / DurationMax
        │
        ▼  DamageAttributeDur::AddDamageToAccumulator          @0x1425b0   [E1]
        │    damage   = lerp(min,  max,  rand)  × accumulator-scale   (Park-Miller RNG)
        │    duration = lerp(durMin, durMax, rand)                     ← rolled INDEPENDENTLY
        │    (ctor inlined at 0x142811: writes vtable 0x105b9940)
        ▼  CombatAttributeDurDamage                             @0xd7c80    [E2]
        │    [this+0x1c] = damage        [this+0x20] = [this+0x24] = duration
        │
        ▼  ::Process(Character&, ReductionInfo&, DamageScaleInfo&, float)  @0xd7dd0  [E3]
        │    damage ×= ([this+0x30] × 0.01)      ← percent modifier ONLY; duration untouched
        │
        ▼  ::Execute(Character&)                                @0xd80c0    [E4]
        │    AddDamage(type, [this+0x1c], [this+0x20], &src, id, [this+0x38])   ← both VERBATIM
        │
        ▼  DurationDamageManager::AddDamage                     @0x208a30   [E5]
        │    damage stored verbatim; duration → ModifyDuration(type, dur) → dur'
        │
        ▼  entry insert/merge, vtable slot 1                    @0x20d6b0   [E6]  ◄── DECISIVE
        │    nTicks  = (int)(dur' × 10.0f)     ← C-1   (tick-bucket container resized to nTicks)
        │    perTick =        damage × 0.1f    ← C-2   (written to instance +0x00 and +0x04)
        │
        ▼  DurationDamageManager::Update(int dtMs)              @0x207f40   [E8]
        │    acc += dtMs;  ticks = acc / 100;  acc %= 100       ← C-3, 100 ms clock
        │
        ▼  entry per-tick sum, vtable slot 2                    @0x20da10   [E7]
        │    Σ over live 24-byte instances of [inst+4]  (`addss`)
        │
        ▼  DurationDamageManager::ExecuteDamage                 @0x208370   [E9]
             → CombatManager::ApplyDamage(float, PlayStatsDamageType&, CombatAttributeType, vector<uint>&)
```

**How the symbols were obtained.** `Game.dll` is PE32 and exports **25,091 decorated C++ names**
with exact RVAs. That turned this from blind disassembly into named-function reading. The export
directory was parsed by a hand-rolled reader (`d4b_pe.py`) rather than installing `pefile`, so
nothing was added to the environment and nothing was written to the vendor tree.

> **⚑ DEFECT D-D4b-1, caught and banked.** My first `IMAGE_EXPORT_DIRECTORY` unpack dropped
> `MinorVersion`, shifting every subsequent RVA by one slot and producing a garbage export map that
> failed loudly (`IndexError`) rather than silently. The struct has **eleven** fields. Fixed and
> commented in `d4b_pe.py`; recorded because the next lap to parse a PE here will hit it.

---

## 2 — CORROBORATION (supporting, never primary)

Lap I found the localization strings but could not use them, because it could not tell whether the
character sheet **displays the raw `.dbr` field or a transformed one**. With the binary decoded,
they are now interpretable — and they agree.

| tag | string | reading, post-decode |
|---|---|---|
| `tagCharStatsPoisonAbsDmgInfo` | "The Poison Damage done **per second** over 5 seconds…" | char-sheet stat is a per-second rate — matches C-2 |
| `tagCharStatsBurn/Coldburn/Electrocute/VitalityDecayAbsDmgInfo` | "…**per second** over 3 seconds…" | same, uniform across families |
| `tagCharStatsPoisonDurationInfo` | "The percent bonus to the duration… **The damage per second is not increased.**" | **now explained by the binary**: `ModifyDuration` raises `nTicks`; `perTick` is untouched |

That last row is the one Lap I flagged as undecidable, and it is the sharpest corroboration.
Under PER-SECOND storage the sentence is exactly what the code does. Under TOTAL storage, extending
the window at a fixed total would *lower* dps, and the string would have to say so — it says the
opposite. **Consistent, but reported as corroboration only; the verdict rests on § 0's constants.**

---

## 3 — THE ROUTES THAT RETURNED NOTHING (recorded, not buried)

Two of these were the commission's suggested first stops. They are clean negatives.

| route | result |
|---|---|
| **`database/templates.arc`** — developer-authored authoring schema, 819 `.tpl` files | **NEGATIVE.** All 167 `offensiveSlow*` Variables carry `description = ""` on Min/Max. Only the duration fields are documented, as `"Seconds"`. The schema names the unit of duration and is silent on the magnitude convention. |
| **`records/game/combatformulas.dbr`** — `magicalDurationDamageEquation` / `physicalDurationDamageEquation` (Game.dll loads these by name) | **NEGATIVE for this question.** They are attribute-scaling only: `magicalDamageDV*((intelligenceDV/200)+1)`, `(physicalDamageDV*((dexterityDV/215)+1))`. No duration term appears in either. |
| **`resources/Scripts.arc`** (107 Lua files) | **NEGATIVE.** Quest/dungeon/wave scripting only; no combat math. |
| **Item-tooltip format strings** | Partial — see § 5 residual. `DamageSingleFormatTime = " over {%.1f0} Seconds"`, `DamageDurationPoison = " {^E}Poison Damage"`. The templates are silent on what the substituted value is. |

---

## 4 — CEILING RE-EVALUATION (the commission's conditional)

The commission scoped the re-run **if and only if** the convention decoded to TOTAL. **It decoded to
PER-SECOND**, so the re-run is a no-op — but the evaluation is stated explicitly, because the whole
point of Lap D-4 § 3.3 was that this test was blocked on this bracket.

D-4's instruments were **re-executed this session** (`d4_step13_waveceiling.py`,
`d4_step15_cumulative.py`), reproducing its figures exactly:

| quantity | value | basis |
|---|---:|---|
| max observed instantaneous post-mitigation DoT drain | **690.0 HP/s** | D-4 M-3, `d4_plateaus.csv` (plateaus at t=797.95 and t=853.93) |
| cumulative-POOL refresh-only ceiling, **TOTAL** limb | 619.1 HP/s | D-4 § 3.3 |
| cumulative-POOL refresh-only ceiling, **PER-SECOND** limb | **1,568.7 HP/s** | D-4 § 3.3 |

**Arithmetic under the decoded convention:**

```
observed 690.0 HP/s   vs   refresh-only ceiling 1,568.7 HP/s
690.0  <  1,568.7           →  observation lies INSIDE the ceiling
690.0 / 1,568.7 = 43.99 %   →  the board's single strongest refresh-only rider set
                               accounts for the observation with 56 % headroom to spare
```

### **Refresh-only is NOT falsified. The test is non-discriminating.**

D-4's § 3.3 verdict of INCONCLUSIVE **stands unchanged** — but the reason has changed in kind, and
that is this lap's deliverable. It was inconclusive because of an *open bracket*; it is now
inconclusive because of a *decided fact*. The bracket is closed, in the direction that does not
rescue the test.

> **The honest disappointment, stated plainly.** This lap was commissioned in the hope that the
> convention would decode TOTAL and hand facet (i) a free falsification on existing footage. It
> decoded the other way. The 619.1 figure — the one that would have been exceeded — is the limb the
> engine does **not** use. No amount of re-arithmetic changes that, and I am not going to look for a
> population assumption that would.

---

## 5 — CONSEQUENCE FOR FACET (i)

Closing Lap I § 5.1 removes the last substrate ambiguity from the DoT magnitude layer — every rider
row now has a single defensible dps, and the up-to-12× bracket Lap I carried is discharged in favour
of the **`dps_if_field_is_per_second_*` limb**. Lap I's dual emission did its job: the correct column
was already computed and shipped, so no re-extraction is owed and every downstream ranking that Lap I
scoped to "where the two conventions agree" can now be re-scoped to the per-second limb alone. But
the closure does **not** unblock the stacking question. The ceiling test that Lap D-4 built and
pre-registered against this convention returns *within-bracket* under the decoded value (690.0 vs
1,568.7 HP/s), so facet (i)'s stacking function remains **UNMEASURED-FROM-VIDEO** on existing
footage, exactly as D-4 § 5 anticipated for this branch. Its recommendation (2) is now the live one:
either a controlled capture, or facet (i) ships declared-absent — **unless the conductor takes up the
incidental lead below, which I believe supersedes both.**

### ⚑ FLAGGED INCIDENTAL — facet (i) may be substrate-decodable after all (NOT worked; out of scope)

While decoding the convention I passed directly through the stacking machinery. **I did not
investigate it and I assert nothing about it**, per the commission's explicit boundary. Recording
what was visible, so the conductor can decide whether to commission a lap:

- At `0x0020d80d`–`0x0020d82c` the insert path compares an incoming instance against each existing
  instance on a **`DurationDamageSource` identity pair**; on a match it does
  `maxss xmm0, xmm1` — *keep the stronger*, no addition.
- On no match (`0x0020d844`) it constructs a new 24-byte instance and appends it (`0x20e420`, a plain
  `movups` copy — no transform).
- At tick time (`0x0020da60`) the per-tick total is `addss` — a **sum over instances**.

Read naively that is **candidate (c), per-source stacking** — D-4's table lists (c) as
"INDISTINGUISHABLE from (a)" *optically*, which is a statement about the video, not about the binary.
**This is a lead, not a finding.** Specifically NOT verified: what the `DurationDamageSource` pair
actually keys on; the relationship between the two containers at `[entry+0x0c]` and `[entry+0x14]`
(one is resized to `nTicks`, suggesting a tick-bucket timeline, and I did not establish how instances
enter and leave it); why the writer sets instance `+0x00` and `+0x04` while the reader sums `+0x04`
and the refresh path `maxss`-es `+0x00`; or how `offensiveSlow<X>Global` / `XOR` participate.
Each of those could overturn the naive reading. **Lap I § 5.3 declared stacking
"UNDECODABLE-FROM-SUBSTRATE"; that declaration was made without the export table in hand and should
be revisited on that basis, not on mine.**

### Residual, named — the DISPLAY layer is NOT closed

This lap decodes the **`.dbr` field**, which is what Lap I extracted and what every KC2 rider row
carries. It does **not** decode what the *item tooltip* prints. `DamageDurationPoison` +
`DamageSingleFormatTime` render "`{value} Poison Damage over {dur} Seconds`" and the format templates
do not say whether `{value}` is the raw field or `field × duration`. **Consequence:** numbers quoted
from tooltips, wikis, or grimtools may or may not be on the same footing as ours, and must not be
joined to KC2 rows without closing this. It does not affect any Lap I value.

---

## 6 — BY-PRODUCTS THAT SHIP

| # | quantity | value | basis |
|---|---|---|---|
| **B-1** | **DoT tick period, from the ENGINE BINARY** | **100 ms** | `Update` @`0x207f76` `cmp edi, 0x64` + `nTicks = dur × 10.0f` @`0x20d6f6` |
| **B-2** | DoT duration semantics | `.dbr` duration is in **seconds**; a duration bonus adds ticks at fixed rate (raises total, not dps) | `ModifyDuration` @`0x209db0` feeding C-1; `templates.tpl` `description="Seconds"` |
| **B-3** | pre-tick damage scaling | `Process` applies a **percent modifier only** (`× field × 0.01`); resistance is applied downstream in `CombatManager::ApplyDamage` | [E3] |

**B-1 independently corroborates D-4's M-1 from a second, non-optical instrument.** D-4 measured
100 ms twice from video (modal 6 frames @60 fps across two recording sessions); the binary states it
as a hard-coded constant. Video measurement and binary decode agree exactly. That is as well-attested
as anything in the KC2 model.

> **⚑ Do not confuse with `TickManager::tickPeriod`.** That exported static (`0x5ab614`) reads
> **1000** (ms) and belongs to a different, 1 Hz system. `DurationDamageManager` also keeps a
> separate 1000 ms accumulator at `[this+0x44]` for per-second bookkeeping. **The DoT damage clock is
> 100 ms and only 100 ms.** Recorded because `tickPeriod` is the obvious symbol to grab and it is the
> wrong one.

---

## 7 — VERSION SKEW, CHECKED NOT ASSUMED

The convention is decoded from `Game.dll` in the **`vendor/grim-dawn`** pull (**v1.2.3.4**,
2026-07-23); Lap I's magnitudes come from the **edition-III** pull (2026-08-08). The two pulls'
`templates.arc` **differ** (`d6d381a5…` vs `679db83f…`), so the transfer had to be justified.

**Check performed** (`d4b_step7_skew.py`): all **167** `offensiveSlow*` Variables in
`templatebase/parameters_offensive.tpl` compared across both pulls on name, class, type, description
and defaultValue — **IDENTICAL, 167/167**. The DoT schema did not move between the pulls.

**What is NOT established:** the edition-III pull is database/resources-only and ships **no engine
binary**, so I cannot diff `Game.dll` across the two. The verdict therefore rests on a v1.2.3.4
binary plus a demonstrated-unchanged schema. Stated so the limit is visible rather than implied.

---

## 8 — ARTIFACTS + DIGESTS

| file | contents |
|---|---|
| `d4b_lib.py` | shared READ-ONLY substrate access (reuses the banked `.arz` / `.arc` readers) |
| `d4b_pe.py` | hand-rolled PE32 section + export-directory reader (D-D4b-1 fixed) |
| `d4b_dis.py` | capstone x86-32 harness; annotates calls with export names and memory operands with `.rdata` constants |
| `d4b_xref.py` | `.text` cross-reference scanner (call-rel32 / push-imm32 / absolute-VA) |
| `d4b_step1_templates.py`, `d4b_step2_blocks.py` | the templates.arc negative (§ 3) |
| `d4b_step3_findeq.py` | the combatformulas.dbr negative (§ 3) |
| `d4b_step4_verify.py` | **V1** bit-exact constants · **V2** float-division scan · **V3** tick period |
| `d4b_step5_tags.py` | § 2 localization corroboration |
| `d4b_step6_evidence.py` | banks the listings below |
| `d4b_step7_skew.py` | § 7 cross-pull schema identity check |
| `evidence/E1…E9*.asm` | the nine load-bearing disassembly listings, re-checkable without capstone |
| `evidence/parameters_offensive.tpl` | the extracted authoring schema |
| `evidence/DIGESTS.txt` | source digests |

```
Game.dll (v1.2.3.4)      4876d6bdb69cca71cfa987652cbd7a42cf6d5578564d02d09aaf9b55c078ab02
templates.arc (ed-III)   679db83f019020ef7d4d27be8e61203006ee94e5c582dd8a59642f3fddd54602
database.arz  (ed-III)   2ad6d379285cfb745462316949e8d59e9450cb58a13f9ffa2fdeb70193183bfd
Text_EN.arc   (ed-III)   1105b1eef70c83914a00d0516ea6db3a25ed06fad8ec91757481e66879d58a27
pm4i_dot_riders.csv      2dc3e380a3800b3afd14f1923d1e2a32efe9263f4ee2eaec7c69c753ed7f6ce1   ← matches Lap D-4 § 8
pe6_crucible_wave_pools  bbdc18f12aab8e3788eac229ed1871a88ed7790dc3d1786c509cd26c076e5587   ← matches Lap D-4 § 8
d4_plateaus.csv          52003af03b53f2e5bfa9c52017e6ee6d68653ce094283d960f3c986b1296f0f5
```

---

## 9 — SELF-CRITIQUE

- **The verdict rests on a negative** (no float division in the chain) as much as on the two
  constants. I scanned ten functions with a fixed mnemonic list. A division expressed as a
  *reciprocal multiply* — `damage × (1/duration)` computed elsewhere and passed in — would evade
  that scan. What rules it out is not the scan but § 1: `damage` is traced from the `.dbr` roll to
  `perTick` through named functions with no arithmetic on it except a percent modifier. **Both legs
  are needed; neither alone is sufficient, and I would rather say that than lean on the tidier one.**
- **I read the entry-instance layout partly by inference.** Writer and reader touch `+0x00` and
  `+0x04` asymmetrically (§ 5) and I did not resolve why. The convention verdict does not depend on
  it — *both* fields are written as `damage × 0.1f` — but a reader should know the layout is not
  fully mapped, and I have not pretended otherwise.
- **Nothing here was validated against a running game.** No Wine, no live process. The decode is
  static. It agrees with D-4's independent video measurement on the one quantity where both speak
  (the 100 ms tick), which is the only cross-instrument check available and it passed.
- **The incidental facet-(i) lead is the thing most likely to be mis-cited.** It is three
  instructions and a naive reading, listed with four named unverified questions. If it appears
  downstream as "per-source stacking confirmed", that is a misreading of this note.
- **`CombatAttributeDurFixedDamage` was not traced.** It is a separate path
  (`AddFixedDamage`/`GetFixedDamageDuration`) which I confirmed is *not* how `offensiveSlow*` riders
  reach the manager, and then left alone. Declared as a scoped exclusion, not an oversight.

---

*Lap D-4b closed 2026-08-24 by legolas. Lap I § 5.1 **CLOSED — PER-SECOND**. Lap D-4 § 3.3 ceiling
test re-evaluated under the decoded convention: **refresh-only NOT falsified**, test
non-discriminating; D-4's § 5 recommendation (2) is live. One flagged incidental lead handed up
unworked. READ-ONLY on all substrate; writes confined to this directory.*
