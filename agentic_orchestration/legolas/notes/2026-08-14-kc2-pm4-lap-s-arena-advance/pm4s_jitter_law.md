# LAP S — `characterRunSpeedJitter` — THE LAW, AND THE REASON NOT TO FOLD IT

**Agent:** legolas · **Run:** KC2-PM4, Lap S (R-PM4-44 part 3, limb d) · **cliff `C-I18-1`** · **2026-08-14**
**Method:** Lap J's (`pathMass`), reused unchanged — templates decoded from `templates.arc` bytes,
PE32 export tables parsed, `objdump` disassembly against the shipped modules with symbol resolution.

---

## 0. The answer, in two lines

> **The transform exists and is fully decoded: a ONE-SHOT, LOAD-TIME, TWO-SIDED, MULTIPLICATIVE
> uniform percentage, `v' = max(0, v · (1 + (J/100)·(2u − 1)))`.**
>
> **But NO SHIPPED BINARY READS THE FIELD `characterRunSpeedJitter` BY NAME.** It is authored in
> the templates, set on 137 of 169 roster records — and consumed by nothing in this build.

**⚑ RECOMMENDATION TO GAMORA: DO NOT FOLD IT. `C-I18-1`'s refusal was right, and it is now right
for a decoded reason instead of an undecoded one.** Folding a two-sided ±10–30 % speed jitter that
the shipped game does not apply would inject variance the referent does not carry.

---

## 1. `d1` — the declaration (MEASURED, from `templates.arc` bytes)

| property | value |
|---|---|
| exact name | **`characterRunSpeedJitter`** |
| class / type | `variable` / `real` |
| defaultValue | **`0`** |
| description | ***empty*** — the corpus documents nothing (same as `pathMass`, Lap J) |
| declaring group | **`"Character Speed"`** |
| declaring templates | `templatebase/parameters_character.tpl`, `templatebase/parameters_characterequation.tpl` (+ two identical `backup/` copies) |

---

## 2. `d2` — per-record values (MEASURED, Lap D's frozen roster baton, 169 distinct records)

| value | records |
|---:|---:|
| **absent from record** | 32 |
| `0.0` | 22 |
| `10.0` | 32 |
| `15.0` | **68** |
| `20.0` | 5 |
| `25.0` | 4 |
| `30.0` | 6 |

Full rows: `pm4s_jitter_records.csv` (169 × 6). The non-jitter sibling `characterRunSpeed` is
present on **169/169** — so the roster records are complete on speed and merely *decorated* with a
jitter value. `15.0` is the modal authored value.

---

## 3. `d3`/`d4`/`d5` — the transform, disassembled

`Game.dll :: ?AddJitter@CharAttributeValSpeed@GAME@@UAEXMPAVRandomUniform@2@@Z` @ RVA `0x00095400`
(`Game.dll` sha256 `4876d6bd…ab02`). It occupies **vtable slot `+0x44` of
`??_7CharAttributeVal_RunSpeed@GAME@@6B@`**, so this is unambiguously the run-speed path. Full
listing banked at `evidence/addjitter_charattributevalspeed.asm`. The load-bearing body:

```asm
movss  xmm4, [ebp+8]            ; J   = the jitter amount from the record
comiss xmm4, xmm5               ; xmm5 = 0
jbe    .ret                     ; ⚑ J <= 0  ->  RETURN, RNG NOT ADVANCED
mov    edi, [ebp+0xc]           ; RandomUniform*
test   edi, edi
je     .ret                     ; ⚑ null RNG -> RETURN
mulss  xmm4, [0x105f5780]       ; 0.01f       ->  J/100          (PERCENT)
mov    dword [ebp+8], 0x1f31d   ; 127773      ->  Schrage q
movss  xmm6, [0x105f5b10]       ; -0.0f       ->  sign mask
movss  xmm7, [0x105f5718]       ; 2^-31
.loop:                          ; over EVERY float in [esi+8, esi+0xc)
  mov    eax, [edi]             ; seed
  div    dword [ebp+8]          ; Schrage: eax = seed/127773, edx = seed%127773
  movss  xmm3, [ecx]            ; v = the stored speed value
  movaps xmm2, xmm4
  imul   edx, edx, 0x41a7       ; 16807   (MINSTD multiplier)
  imul   eax, eax, 0xb14        ; 2836
  mulss  xmm2, xmm3             ; xmm2 = v * J/100        = the AMPLITUDE
  sub    edx, eax
  movaps xmm1, xmm2
  xorps  xmm1, xmm6             ; xmm1 = -(v * J/100)     = the LOWER OFFSET
  subss  xmm2, xmm1             ; xmm2 =  2*(v * J/100)   = the FULL WIDTH
  lea    eax, [edx+0x7fffffff]
  cmovs  edx, eax               ; wrap negative -> + (2^31 - 1)
  mov    [edi], edx             ; store advanced seed
  ...cvt to float...
  mulss  xmm0, xmm7             ; u = seed * 2^-31   in [0, 1)
  mulss  xmm0, xmm2             ; u * 2*(v*J/100)
  addss  xmm0, xmm1             ; + (-(v*J/100))
  addss  xmm0, xmm3             ; + v
  maxss  xmm0, xmm5             ; ⚑ CLAMP AT ZERO
  movss  [ecx], xmm0            ; ⚑ WRITE BACK IN PLACE
  add    ecx, 4
  cmp    ecx, [esi+0xc]
  jne    .loop
```

Constants read from `.rdata` and verified as floats, not guessed:

| address | bytes | float | role |
|---|---|---|---|
| `0x105f5780` | `0ad7233c` | `0.00999999977` | percent → fraction |
| `0x105f5b10` | `00000080` | `-0.0` | sign mask (float negate via `xorps`) |
| `0x105f5718` | `00000030` | `4.656612873e-10` = **2⁻³¹** | uniform scale |
| `0x105f5ae0` | — | `0.0`, `4294967296.0` | signed→unsigned conversion table |

### The law

$$v' \;=\; \max\!\bigl(0,\; v \;+\; v\cdot\tfrac{J}{100}\cdot(2u-1)\bigr) \;=\; \max\!\bigl(0,\; v\cdot\bigl(1 + \tfrac{J}{100}(2u-1)\bigr)\bigr),\qquad u = \text{seed}\cdot 2^{-31}\in[0,1)$$

with the seed advanced by **MINSTD / Lehmer** (`a = 16807`, `m = 2³¹−1`) using **Schrage's method**
(`q = 127773`, `r = 2836`).

| question | answer | grade |
|---|---|---|
| **d3 roll timing** | **ONE SHOT, AT LOAD/CONSTRUCTION — never per tick.** The function takes an explicit `RandomUniform*` and **mutates the attribute's stored value array in place**; a per-tick application would compound into an unbounded random walk. Corroborated: the only direct callers of the sibling scalar helper `?Jitter@CharAttribute@GAME@@IAEMMMAAVRandomUniform@2@@Z` are `LoadPrefixTable`, `LoadSuffixTable` and `LoadModifierTable` — all **`Load…(const LoadTable&, float, RandomUniform*)`**, i.e. record-load paths. | **MEASURED** |
| **d4 application basis** | **MULTIPLICATIVE PERCENTAGE of the base value** (`v · J/100`), then added. Not additive-absolute, not a flat multiplier. | **MEASURED** |
| **d5 sign / range** | **TWO-SIDED and SYMMETRIC**, uniform on `[v·(1−J/100), v·(1+J/100))`, half-open at the top, **clamped at 0 below**. `J = 15` ⇒ ±15 %. **`J = 0` is not a zero-width roll — the function early-outs and does not even advance the RNG.** | **MEASURED** |
| **each array element** | gets an **independent** draw (the seed advances once per element). | **MEASURED** |

---

## 4. `d6` — ⚑ THE FIELD IS NOT CONSUMED. MEASURED-NEGATIVE, with positive controls.

A DBR field can only be read out of a `LoadTable` by its **name string**, so the name must exist as
a literal in whichever module reads it. Census over **every** `*Jitter` field declared anywhere in
`templates.arc`, run against all three shipped modules, with five non-jitter positive controls:

| field | kind | literal present in |
|---|---|---|
| `lootRandomizerJitter` | JITTER | **`Game.dll`** ✓ |
| `TendrilJitter` | JITTER | **`Game.dll`** ✓ |
| **`characterRunSpeedJitter`** | JITTER | **NONE** ✗ |
| `characterRunSpeed` | CONTROL | `Game.dll` ✓ |
| `characterRunSpeedModifier` | CONTROL | `Game.dll` ✓ |
| `characterAttackSpeed` | CONTROL | `Game.dll` ✓ |
| `pathMass` (Lap J) | CONTROL | `Game.dll` ✓ |
| `placementExtents` (Lap S limb a) | CONTROL | `Game.dll` ✓ |

**The field's own non-jitter sibling is present. The other two jitter fields are present. It is
absent.**

**The runtime-name-construction escape is closed too.** If the engine built the name as
`<base> + "Jitter"` it would need a standalone `"Jitter\0"` literal:

| module | standalone `"Jitter\0"` literals |
|---|---:|
| `Game.dll` | **0** |
| `Engine.dll` | **0** |
| `Grim Dawn.exe` | **0** |

*(Self-caught: the naive test `b"Jitter\0" in blob` returns TRUE on all three — it matches the tail
of `lootRandomizerJitter\0`. The corrected test requires the preceding byte to be a non-identifier
character. The instrument carries the corrected test and a comment saying why.)*

And the machinery that DOES drive `CharAttribute`'s jitter is visible and is **item-affix
randomisation, not monster speed**: `LoadPrefixTable` pushes the literal `lootRandomizerJitter`
(`0x105239b0`) straight into the `LoadTable` lookup before calling `Jitter`.

### The one named caveat, stated rather than buried

`Grim Dawn.exe` ships with a **`.bind` section (Steam DRM)** — its `.text` is encrypted at rest.
A literal *could* in principle hide inside that encrypted region. Two reasons the negative still
stands: (1) the exe's **plaintext `.rdata` is readable** — that is where I read the `Proxy` Lua
binding names — and it does not contain the field; (2) every other character-attribute field,
including this field's own sibling, is owned by `Game.dll`, which is **not** protected and was
disassembled freely. **Grade: MEASURED-NEGATIVE with the DRM boundary named.**

---

## 5. What gamora should do

| | |
|---|---|
| **fold the jitter?** | **NO.** The shipped game does not apply it. `C-I18-1` stands — now as a decoded refusal, not an undecoded one. |
| **if it is ever folded anyway** | the law above is complete and MEASURED on d3/d4/d5, and my PREREGISTRATION § 5 pre-commitment ("I will NOT hand gamora a law graded below MEASURED on d3/d4/d5") is met — so the fold would at least be correct: per-spawn, once, `v·(1 + (J/100)(2u−1))`, clamped at 0, `J=0` ⇒ no roll at all. |
| **what to fold INSTEAD** | the two decoded mechanisms that the shipped game *does* apply and the sim does not model: **patrol-point convergence** (`M-1`) and **spawn beacons** (`M-2`) — see `pm4s_wave_advance.md` § 6. Those are real monster-locomotion terms; the jitter is not. |
