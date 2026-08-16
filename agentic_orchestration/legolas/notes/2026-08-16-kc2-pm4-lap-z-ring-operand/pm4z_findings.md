# KC2-PM4 · LAP Z — FINDINGS · THE RING-OPERAND FORK PAIR

**Agent:** legolas (UNKNOWN-RESEARCHER) · **Conductor:** gandalf (`RUN-CONDUCTOR`) · **2026-08-16**
**Commission:** `R-PM4-65 part 3` · **Provenance:** `UNREACHED-I24D-1` (gamora, I-24-D § 10);
root defect `D-I24D-1`.
**Preregistration:** `prereg.md`, sha256 `a39aa0c2b3c8185f5d0d377e903644047b80c8a2a2128192156010b3149a6bf2`,
committed **ALONE** as `d54f2c6c` before any instrument ran.

> **RECORD lap.** No simulation run. No sim outcome read. No baton touched. Nothing written outside
> this directory and one instrument script. `D-I24D-1` is **NOT repaired here** — the repair is
> gamora's at the I-24 fold, on this verdict.

---

## 0 — THE HEADLINE, IN ONE PARAGRAPH

**Both fork limbs are DECODED, and the pair turns out to be COUPLED: (b) changes what (a) means.**
Fork (a) is `A1 — STORED-FLOAT32`: the compiled database stores `meleeTargetDistance` as a 4-byte
IEEE-754 single with bit pattern `0x4019999A`, and both shipped builds store the DB accessor's
return into a 4-byte `float` slot (`movss dword ptr [r13+0x13a4]` on x64; `fstp dword ptr
[edi+0xc7c]` on x86). The decimal `2.4` has **no physical carrier anywhere on the path** — the
compiled format has no 8-byte numeric type at all. Fork (b) is `B1 — SQUARED`: the engine's melee
reach flows as the `float` radius of a `Sphere` into `GAME::World::GetEntitiesInCone`, thence to a
box-vs-sphere primitive that computes `mulss xmm0, xmm0` on the radius and `comiss` it against an
accumulated squared distance — **no `sqrt` and no double-precision arithmetic anywhere in that
function**, on either shipped build. And the coupling is the finding that matters downstream:
because the square is taken **in float32**, `fl32(r32²) = 5.7600002288818359375` is *not* `r32²`,
so the engine's effective boundary radius is **`2.4000000476837156`** — which sits at the
**midpoint** of the 9.5367e-8 m window the fork was posed over, `4.7684e-8` m from **each** limb.
The sim's `2.4` and the run's published `2.4000000953674316` are **both wrong by the same amount,
in opposite directions.**

**Two of my ten pre-registered bets FAILED** — `P-Z-9` (I bet fork (b) would land UNREACHED) and
`P-Z-10` (I bet the instruction-stream anchor chain would break). Both were deliberately pessimistic
bets against my own instrument. Their wording is unchanged in `prereg.md § 4`.

---

## 1 — VERDICT PER FORK LIMB

| fork | question | **VERDICT** | one-line basis |
|---|---|---|---|
| **(a)** | float32-promoted `2.4000000953674316` or decimal `2.4`? | **DECODED — `A1` STORED-FLOAT32** | `database.arz` stores a **4-byte** payload `9a991940` (= `0x4019999A`) under type tag **1**, and the compiled format has **no 8-byte numeric type** (99,781 records, 32,264,692 field entries, four type tags, **zero** stream residue under a 4-byte stride); both shipped builds store the accessor's return into a **4-byte float slot**. |
| **(b)** | squared comparison, or root first? | **DECODED — `B1` SQUARED, in float32, no root** | `x64/Engine.dll` `0x27cff0`: `movss xmm0,[rdx+0xc]` (the Sphere's radius) → `mulss xmm0,xmm0` → `comiss xmm0,xmm3` → `setae al`. **Zero** `sqrt*` and **zero** double-precision instructions in the function; the independent node primitive at `0x134b50` and the x86 build's `0x222d8a` are structurally identical. |

### 1.1 ⚑ THE COUPLED CONSEQUENCE — a third number neither limb named

Because (b) squares **in single precision**, the engine's accept predicate is

```
accept  ⟺  fl32( r32 × r32 )  ≥  d²          with  r32 = 0x4019999A = 2.400000095367431640625
           └─────────┬──────┘
            5.7600002288818359375   (exact; float32 bit pattern 0x40b851ec)
```

so the **effective boundary radius** is `√(fl32(r32²)) = 2.4000000476837156`.

| candidate | metres | Δ vs engine (m) |
|---|---|---|
| `A2/B2` decimal `2.4`, rooted, double | `2.4` | `−4.768372E-8` |
| `A1/B2` stored float32, rooted, double | `2.4000000953674316` | `+4.768372E-8` |
| `A2/B1` decimal `2.4`, squared, double | `2.4` | `−4.768372E-8` |
| `A1/B1` stored float32, squared, **double** | `2.4000000953674316` | `+4.768372E-8` |
| **`ENGINE` stored float32, squared, float32** | **`2.4000000476837156`** | **`0`** |

Two structural facts inside that table, both DECODED:

1. **At double precision fork (b) is INERT.** `r32` has a 24-bit significand, so `r32²` needs ≤ 48
   bits and is *exactly* representable in a 53-bit double. `√(fl64(r32²)) == r32` bit-for-bit.
   A double-precision reproduction cannot tell squared from rooted. (`P-Z-4` PASS.)
2. **At single precision fork (b) is NOT inert**, and it is worth `4.7684e-8` m — the same order as
   the `9.5367e-8` m window fork (a) was posed over. (`P-Z-5` PASS.)

---

## 2 — THE ANCHOR CHAIN, LINK BY LINK

Every link cited by module + RVA + bytes. Full listings in `pm4z_binary_anchors.json`; full trace in
`decode.log`. **`NOTE D-V2-1` honoured** — no vtable base is read anywhere in this lap; see § 2.1.

| # | link | citation |
|---|---|---|
| **L1** | the field-name string | `x64/Game.dll` file offset `0x65f928`, rva `0x660528`, section `.rdata`, **1** occurrence in the module |
| **L2** | its references in `.text` | exactly **1** rip-relative reference, `lea rdx,[rip+0x3ac78d]` at rva `0x2b3d94`, bytes `488d158d7c3a00` |
| **L3** | the load site | inside `RUNTIME_FUNCTION 0x2b3bc0..0x2bf074`. `mov rax,[r14]` · `movss xmm2,[r13+0x13a4]` (the prior value, passed as the accessor's default) · `lea rdx,[rip+…]` (the name) · `mov rcx,r14` · `call [rax+0x48]` · **`movss dword ptr [r13+0x13a4], xmm0`** — a **4-byte** store |
| **L4** | independent slot-width witness | the C++ constructor at `0x2ac178` writes the same slot with a **dword** immediate: `mov dword ptr [rdi+0x13a4], 0x40400000` |
| **L5** | every reference to slot `+0x13a4` in the whole module | **7** instructions total; exactly **one reader**: `movss xmm7, dword ptr [rax+0x13a4]` at rva `0x50134a` |
| **L6** | what the reader does with it | `RUNTIME_FUNCTION 0x5012d0` places it at `[rsp+0x30]` and calls `0x2d6930`, whose IAT slot chain resolves through the **import directory** to `Engine.dll :: ?GetEntitiesInCone@World@GAME@@QEAAXAEAV?$vector@PEAVEntity@GAME@@@mem@@AEBVWorldVec3@2@AEBVVec3@2@MM_NW4EntityListType@2@@Z` — i.e. `World::GetEntitiesInCone(vector<Entity*>&, const WorldVec3&, const Vec3&, float, float, bool, EntityListType)`. **The value is the second `float` — the cone RADIUS.** |
| **L7** | export resolution, D-V2-1-guarded | `x64/Engine.dll` rva `0x21dc40`; **no other exported name shares that RVA** (1 of 6,279); section `.text`; `.pdata` bounds `0x21dc40..0x21e396`; **rva == function start** |
| **L8** | the Sphere is built with a 4-byte radius | `0x21dceb movss xmm0,[rbp+0xc8]` → `0x21dcf3 movss dword ptr [rsp+0x3c], xmm0`. `Sphere = {float x,y,z; float radius}`, radius at `+0xc`. Delegates to `World::GetEntitiesInSphere` (`0x21e3a0`) |
| **L9** | per-entity test site | inside the quadtree gather `0x134080`: `lea rcx,[rdi+0x44]` (or `+0x5c`) = the entity's ABBox · `mov rdx,rax` = the Sphere · `call 0x27cff0` |
| **L10** | **THE COMPARISON** | `x64/Engine.dll 0x27cff0`, `.pdata` bounds `0x27cff0..0x27d0df`. Per-axis clamped deltas each `mulss`-squared and `addss`-accumulated into `xmm3`; then `movss xmm0,[rdx+0xc]` · **`mulss xmm0, xmm0`** · **`comiss xmm0, xmm3`** · `setae al`. **`sqrt` instructions: NONE. Double-precision instructions: NONE.** |
| **L11** | second, independent primitive | `0x134b50` (node-vs-sphere): same shape, `movss xmm0,[r9+0xc]` · `mulss xmm0,xmm0` · `comiss xmm0,xmm1` · `seta al`. `sqrt`: NONE. double: NONE. |
| **L12** | the **x86** shipped build, independently | `Game.dll` rva `0x24d141 push 0x1054d7ac` (the name) → `call eax` → **`0x24d14b fstp dword ptr [edi+0xc7c]`** — a **4-byte** store. `Engine.dll 0x222d83`: `movss xmm0,[edx+0xc]` · `mulss xmm0,xmm0` · `comiss xmm0,xmm3` · `setae al`. **Both builds agree on both forks.** |

### 2.1 How `D-V2-1` was discharged, not merely invoked

`D-V2-1` was a *method* defect: `??_7X@…@6B@` **vtable data symbols** collide on RVAs in the export
table, so vtable bases read from exports are unreliable. This lap reads **no vtable base**. It
resolves exactly **one** symbol by name — a *function* export — and guards it three ways, all
asserted in the instrument and recorded in `pm4z_binary_anchors.json`:

1. **no other exported name shares its RVA** (the exact failure mode of `D-V2-1`);
2. the RVA lands in `.text`;
3. the RVA is the **start** of a `.pdata` `RUNTIME_FUNCTION`.

Every other code site in the chain is reached by a **byte-cited reference** (a rip-relative
displacement, an absolute dword, an import-directory entry, or a direct `call` target) — never by a
symbol lookup. The one virtual call adjacent to the path (`call [rax+0x4b8]` at `0x50140a`, which
also receives the melee distance, in `xmm3`) was **deliberately not resolved**, because resolving it
would require exactly the vtable read `D-V2-1` forbids. It is named in § 6 as a carry, not decoded.

---

## 3 — THE DATA-LAYER DECODE

### 3.1 EC-1 — what the shipped database literally stores

`records/game/gameengine.dbr`, from `database.arz`
(`2ad6d379285cfb745462316949e8d59e9450cb58a13f9ffa2fdeb70193183bfd`):

| field | stream offset | type tag | count | payload bytes | as u32 | width | as double |
|---|---|---|---|---|---|---|---|
| `meleeRange` | `0x0a8c` | 1 (float32) | 1 | `0000a03f` | `0x3fa00000` | 4 B | `1.25` |
| `meleeAutoTargetDistance` | `0x0a80` | 1 (float32) | 1 | `00008040` | `0x40800000` | 4 B | `4.0` |
| **`meleeTargetDistance`** | **`0x0a98`** | **1 (float32)** | **1** | **`9a991940`** | **`0x4019999A`** | **4 B** | **`2.4000000953674316`** (exact `2.400000095367431640625`) |

Field-stream residue for this record: **0 bytes**. **No overlay overrides it** — the record is
absent from all seven of `GDX1/2/3` and `SurvivalMode/1/2/3`, checked individually.

### 3.2 ⚑ `D-Z-1` — the decoy set, published rather than merely avoided

A substring match on `gameengine` returns **7** records. Six are decoys and **five carry a different
value**:

| record | `meleeTargetDistance` |
|---|---|
| `records/ingameui/gameengine.dbr` | `0x40500000` = `3.25` |
| `records/sandbox/arthur/archive/gameengine 01-23-15.dbr` | `0x40133333` = `2.299999952316284` |
| `…/gameengine 02-01-16.dbr` · `…/gameengine 09-09-15.dbr` · `…/gameengine 10-31.dbr` · `…/gameengine 7-31.dbr` | `0x40133333` = `2.299999952316284` |

My first exploratory read took `hits[0]` and landed on a dev-sandbox archive carrying **2.3**. Caught
before any claim was formed; the shipped instrument now enumerates the whole decoy set explicitly so
the guard is on the record rather than in my head. See § 7.

### 3.3 EC-2 — the template declaration

`templates.arc → gameengine.tpl`:

```
Variable { name = "meleeTargetDistance"      class="variable"  type="real"
           description = "TQ was 2.5"        value=""          defaultValue = "2.5" }
Variable { name = "meleeAutoTargetDistance"  class="variable"  type="real"
           description = "TQ was 3.0"        value=""          defaultValue = "3.0" }
```

### 3.4 EC-3 — the format has no double. Two independent proofs.

**Declared side.** 818/819 templates parsed (one entry has a zero-length name and
`decomp_size = 0` — an empty sentinel, reported, not skipped silently). **24** distinct `type=`
strings across the corpus. The *only* floating-point one is **`real`** (7,804 declarations).
`double` appears **nowhere**. (`P-Z-2` PASS.)

**Compiled side — the falsifiable width test.** The reader assumes a **4-byte stride per value**. If
any type tag carried an 8-byte payload, the field stream would desync and leave residue. Across all
eight archives:

| | records | field entries | distinct type tags | records with stream residue |
|---|---:|---:|---|---:|
| **GRAND** | **99,781** | **32,264,692** | **{0, 1, 2, 3}** | **0** |

Zero residue in 99,781 records. **There is no 8-byte numeric type in the compiled database
format**, so the decimal `2.4` has no place to live on disk. (`P-Z-3` PASS.) This is what converts
`A2` from "a losing limb" into "a limb with no physical carrier."

### 3.5 EC-4 — the data layer is silent on fork (b)

**0 of 19,005** distinct `Variable` names in the whole template corpus match `squared` / `*sq` /
`sqr`. **Decoded-absent.** Fork (b) was never answerable from the data layer; it required the code.
(`P-Z-6` PASS.)

### 3.6 EC-5 — string residency (CORROBORATION grade only)

`?GetDistanceSquared@World@GAME@@QEBAMAEBVWorldVec3@2@0@Z` — a named, squared-distance primitive
returning `float` — is resident in `Game.dll` and `Engine.dll` on **both** builds. `LengthSquared`
and `SqrDist` are absent everywhere. The three shipped **tools** (`DBREditor.exe`,
`ArchiveTool.exe`, `AssetManager.exe`) carry **none** of the seven needles — they are not on the
runtime path and contribute nothing. (`P-Z-7` PASS.) Residency names a vocabulary; it never names a
caller, and none of it is load-bearing here.

### 3.7 EC-8 — the lineage attestation came from inside the corpus, not from outside

Two bounded external searches (ARZ/DBR float storage; `meleeTargetDistance`) returned **nothing
load-bearing** — as pre-registered, external sources are never load-bearing on this lap. The lineage
evidence that *does* speak is **shipped, first-party, and DECODE-grade**: of **19,005** distinct
`Variable` names in the entire template corpus, **exactly two** carry a description naming Titan
Quest — and they are precisely the two fields at issue:

```
gameengine.tpl  meleeTargetDistance      real   "TQ was 2.5"
gameengine.tpl  meleeAutoTargetDistance  real   "TQ was 3.0"
```

⚑ **This is `R-PM4-64 part 3` landing a second time.** The commission asked for TQ-lineage evidence
from outside; the deciding lineage statement was sitting in an **already-pinned** artifact
(`templates.arc`, pinned since Lap Y), unqueried under this question. The corpus you hold keeps
containing the answer you were about to go outside for.

---

## 4 — ⚑ WHAT THIS MEANS FOR THE I-24 FOLD — DECODE ONLY, NO PRESCRIPTION

Stated as arithmetic, not as an instruction. The fold chooses; `R-PM4-65 part 4` gives it
import-by-identity authority, and these are the identities.

**The engine's predicate, exactly:**

```
accept  ⟺  fl32(r32 × r32)  ≥  Σ_axes fl32( clamp-delta² )
r32              = 0x4019999A          = 2.400000095367431640625
fl32(r32 × r32)  = 0x40b851ec          = 5.7600002288818359375        (EXACT, no rounding left)
√ that           =                       2.4000000476837156           (the effective radius)
```

**Three things the fold must not be allowed to believe:**

1. **`2.4000000953674316` is the right operand but the wrong threshold.** It is the exact value the
   engine *holds*; it is **not** the boundary the engine *tests at*, because the square is taken in
   float32. Publishing the operand as the ring radius reproduces the provenance and misses the
   boundary by `+4.7684e-8` m.
2. **`2.4` is not "the safe reading."** It misses by `−4.7684e-8` m — the same magnitude, the other
   way. Neither incumbent is closer than the other. That symmetry is exact to twelve significant
   figures and is not a coincidence: `2.4` and `r32` are adjacent float32 neighbours and the
   float32 square lands on the midpoint.
3. **No single double reproduces the engine's accept-set bit-for-bit, and the fold must not pretend
   otherwise.** The *threshold* side is exactly representable (`5.7600002288818359375`). The
   *distance* side is not: the engine accumulates `d²` in float32 with per-axis rounding, from a
   **box-vs-sphere clamped distance**, not a point-to-point distance (§ 6, `NAMED-Z-1`). A
   double-precision sim can reproduce the threshold exactly and the distance only approximately.
   Any claim of bit-identity would be false.

**Sensitivity, for scale, from the run's own record.** gamora measured that the `2.4` ↔
`2.4000000953674316` window (`9.5367e-8` m) contains ~59 % of `PX-LO`'s occupancy ticks and moves the
occupancy metric `0.234 → 0.372`. The engine's threshold splits that window in half. Whether a
half-window shift is material is a **measurement the fold makes**, not a claim this lap makes.
**Law 3 note:** those numbers are recorded here as context (`prereg.md § 0.1`) and were not consulted
while grading; the verdict was fixed by bytes, and neither limb was designated by which grades better
(`R-PM4-27 part 3`).

---

## 5 — ⚑ DO-NOT BLOCK (binding on every downstream fold)

1. **DO NOT** cite `2.4000000953674316` as "the engine's ring radius." It is the engine's **stored
   operand**. The **tested boundary** is `2.4000000476837156`. Those are different claims with
   different bases; conflating them is exactly the class of error `D-I24D-1` was.
2. **DO NOT** treat fork (b) as settled *in the abstract*. `SQUARED` is decoded **for the shipped
   engine's float32 arithmetic**. In a double-precision reimplementation the squared and rooted
   forms are provably **identical** (§ 1.1). "Square it because Grim Dawn squares it" is a
   non-reason in a double-precision sim; the only reason to carry the square is to carry the
   **float32 rounding**, and that must be done deliberately or not at all.
3. **DO NOT** claim a double-precision sim reproduces the engine's accept-set exactly. The threshold
   is exactly representable; the distance side is not (§ 4.3).
4. **DO NOT** propagate the **box**-vs-sphere structure as decoded sim behaviour. It is `NAMED-Z-1`
   — a real structural difference from the sim's point/disc model, named because it is real, and
   **not** decoded as to magnitude. It is not a licence to change body geometry.
5. **DO NOT** read § 4's sensitivity paragraph as a finding about occupancy. Lap Z ran no
   simulation, read no sim outcome, and makes **no claim** about whether this repair moves the
   I-24-D residual. It moves a constant. Whether the constant moves the board is gamora's
   measurement.
6. **DO NOT** use the three shipped tools, the six decoy `gameengine` records, or the C++
   constructor defaults (§ 6, `NAMED-Z-2`) as sources for any number. They are published here so
   that they are visibly excluded, not so that they are available.
7. **DO NOT** cite the external EC-8 searches for anything. They returned nothing load-bearing and
   are recorded only so the declared evidence class is visibly discharged rather than silently
   dropped.

---

## 6 — COLLATERAL, NAMED NOT DECODED (`R-PM4-56 part 4`)

| id | finding | status |
|---|---|---|
| **`NAMED-Z-1`** | **The engine's melee gather is a BOX-vs-SPHERE test, not point-vs-point.** `0x27cff0` receives the entity's axis-aligned bounding box (`entity+0x44`, or `entity+0x5c` when the flag at `entity+0x74` is set) and clamps the sphere centre to it per axis before squaring. A body is "in reach" when its **box** intersects the reach sphere — so the effective reach is the ring **plus the body's own half-extent along the approach axis**. The sim models bodies as points/discs. Structurally real; **magnitude not decoded** (it needs the per-body ABBox extents, which this lap did not commission). | **NAMED** |
| **`NAMED-Z-2`** | **The C++ constructor defaults and the template defaults disagree, and appear transposed.** `x64/Game.dll 0x2ac16e-0x2ac178` writes `[+0x13a0] = 0x40200000 = 2.5f` (the `meleeAutoTargetDistance` slot) and `[+0x13a4] = 0x40400000 = 3.0f` (the `meleeTargetDistance` slot), while `gameengine.tpl` declares `defaultValue "2.5"` for `meleeTargetDistance` and `"3.0"` for `meleeAutoTargetDistance`. **Neither default is ever used** — the DB supplies both (`2.4` and `4.0`). Reported factually; **no interpretation offered**, and it moves no number. | **NAMED** |
| **`NAMED-Z-3`** | **The melee query is a 14° cone, not a full circle.** The consumer passes the literal `14.0` (`x64/Game.dll` rva `0x773c34`) as the cone angle in **degrees**; the `0x2d6930` wrapper multiplies by `0.01745329238474369` (π/180) and `GetEntitiesInCone` halves it (`×0.5` at rva `0x21dcbb`) to a 7° half-angle. The sim's disc is a full 360°. Named because it is a real shape difference on the same call path; **not decoded** as to which sim quantity it corresponds to, and explicitly **not** offered as a fold. | **NAMED** |
| **`UNREACHED-Z-1`** | **The second consumer of the melee distance was not resolved.** `x64/Game.dll 0x50140a` passes the same value in `xmm3` to `call qword ptr [rax+0x4b8]` — a **virtual** call. Resolving it requires a vtable base read, which `D-V2-1` forbids. Whether it applies a *second*, differently-rounded range test is **not known**. It does not disturb fork (a) (the value is the same float32 either way) and it does not disturb the decoded `GetEntitiesInCone` path; it means fork (b) is decoded **for the gather**, and open for that one branch. | **UNREACHED — named, not decoded** |

---

## 7 — DEFECT TABLE (all mine; all self-caught; all before any claim)

| id | defect | disposition |
|---|---|---|
| **`D-Z-1`** | My exploratory read of `gameengine.dbr` took the first **substring** match and landed on `records/sandbox/arthur/archive/gameengine 01-23-15.dbr`, which carries `0x40133333 = 2.3` — not the shipped `2.4`. | **CAUGHT BEFORE ANY CLAIM.** Repaired by naming the record exactly *and* by enumerating the full 6-record decoy set in the instrument and in § 3.2, so the guard lives in the artifact rather than in my attention. ⚑ Lesson: **a decoy set is ENUMERATED, not avoided** — the `D-I24D-2` class, in my own seat. |
| **`D-Z-2`** | My PE export-directory parser was **off by one field** — `"<IIHHIIIIII"` omits `NumberOfFunctions` — so every export RVA was read from the wrong table. It reported 4,866 exports instead of 6,279 and raised `KeyError` on a symbol I had already proved exists. | **REPAIRED before any export was cited.** Self-caught by an internal contradiction: the symbol was present in `Game.dll`'s **import** directory and absent from `Engine.dll`'s **export** directory, which cannot both be true. The corrected parser (`"<IIHHIIIIIII"`) is in the committed instrument. ⚑ A silent off-by-one in a header parse does not crash — it lies. |
| **`D-Z-3`** | PE32 has no `.pdata`, so an x86 disassembly start is a **manual byte anchor**. A linear sweep from an arbitrary offset desynced mid-instruction and printed `movups xmmword ptr [edi+0xc7c]` where the true instruction is `movss dword ptr [edi+0xc7c]` — i.e. it would have mis-reported a 4-byte load as a 16-byte one, in the exact function whose operand **width** is the question. | **CAUGHT AND REPAIRED IN-INSTRUMENT.** Self-caught by disagreement with an earlier decode from a different start. Repaired by **strengthening**: the instrument now decodes from **three** independent starts and asserts the store instruction is identical in all three (`d_z_3_three_start_convergence: true`). The `D-I23-4` class — the guard was right, the implementation was the wrong shape. |

---

## 8 — PRE-REGISTERED PREDICTIONS, GRADED

Wording of a failed prediction is never rewritten (`prereg.md § 4`).

| id | bet | result | evidence |
|---|---|---|---|
| `P-Z-1` | `.arz` stores a 4-byte single, pattern `0x4019999A` | **PASS** | § 3.1 |
| `P-Z-2` | declared `real`; **no** double type anywhere in templates | **PASS** | § 3.4 — 24 type strings, `double` absent |
| `P-Z-3` | compiled type-tag alphabet has **no** 8-byte float tag | **PASS** | § 3.4 — 4 tags, 0 residue / 99,781 records |
| `P-Z-4` | `r32²` exact in double ⇒ fork (b) **INERT** at double precision | **PASS** | § 1.1 |
| `P-Z-5` | under float32, `\|Δ\|` ∈ `[1e-8, 1.5e-7]` m | **PASS** | `4.7684e-8` m |
| `P-Z-6` | no shipped field expresses a squared distance | **PASS** | § 3.5 — 0 / 19,005 |
| `P-Z-7` | ≥ 1 resident squared-distance symbol | **PASS** | § 3.6 — `World::GetDistanceSquared` |
| `P-Z-8` | fork (a) = `A1`, at `DECODED` or `DECLARED` | **PASS** (landed **DECODED**) | § 1 |
| `P-Z-9` | fork (b) = **UNREACHED** | ⚑ **FAILED** | landed **DECODED**; § 2 L10–L12 |
| `P-Z-10` | the anchor chain **breaks** | ⚑ **FAILED** | it completed, and continued across a module boundary; § 2 |

**Both failures are mine and both are in the same direction:** I under-estimated what a
citation-solid instruction-stream read could reach without touching a vtable. Registering the
pessimistic bet is what makes that visible instead of retiring it quietly.

---

## 9 — METHOD, DETERMINISM, AND WHAT WAS NOT DONE

- **Instrument:** `agentic_orchestration/research/scripts/pm4z_ring_operand_2026_08_16.py`,
  sha256 `97b40c013ea8f16c448235a13dbabdf9e2c9a34b7f7f69bc97c59841fd2532f0`.
- **Determinism ×2:** the instrument ran twice, end to end. **All six artifacts byte-identical**
  (digests in § 10).
- **Pins:** 21 inputs re-verified before any read; **all EXACT**, HALT-on-drift armed and not
  triggered. The seven pins shared with Lap Y match Lap Y's published values.
- **Read-only** on every source. No engine file, no sim file, no baton was opened for writing or
  read for outcome.
- **Not done, deliberately:** no vtable resolution (`D-V2-1`); no repair of `D-I24D-1`; no
  simulation; no re-grading of I-24-D; no re-opening of Lap Y; no prescription to the fold beyond
  the arithmetic in § 4 and the prohibitions in § 5.

---

## 10 — ARTIFACT DIGESTS (full 64-hex sha256)

### 10.1 Emitted by this lap

| artifact | sha256 |
|---|---|
| `prereg.md` | `a39aa0c2b3c8185f5d0d377e903644047b80c8a2a2128192156010b3149a6bf2` |
| `pm4z_operand.json` | `6e689f8a3930dca5b132ae250810f7035273d75515db61f383a7f11b967d1802` |
| `pm4z_binary_anchors.json` | `11b523fd1c7bc23dced18602e1746a59a110442730fb206f5574bdc480478f3b` |
| `pm4z_type_system.csv` | `055c779a14db4b7ec4142aedc7dea1ca4adb70e7756e7724368ba77c5ce10711` |
| `pm4z_boundary_arithmetic.csv` | `3a9cac943d61ee42d51041fc6ec6ea48443116da2f9042bcfb9acd4e912f3563` |
| `pm4z_digests.json` | `3516b7074675a57df9edc3c5f3858eef1983232c5e1724bb8a935d6ed755cbf1` |
| `decode.log` | `56aaa34a5a5dfaf995eb6273a129dd0be6c77091f5447fe3be8bbc3d385da351` |
| `pm4z_ring_operand_2026_08_16.py` | `97b40c013ea8f16c448235a13dbabdf9e2c9a34b7f7f69bc97c59841fd2532f0` |

### 10.2 Every artifact consulted (pinned, re-verified EXACT at instrument start)

| artifact | sha256 |
|---|---|
| `…/grim-dawn-edition-III-20260808/database/database.arz` | `2ad6d379285cfb745462316949e8d59e9450cb58a13f9ffa2fdeb70193183bfd` |
| `…/grim-dawn-edition-III-20260808/database/templates.arc` | `679db83f019020ef7d4d27be8e61203006ee94e5c582dd8a59642f3fddd54602` |
| `…/grim-dawn-edition-III-20260808/gdx1/database/GDX1.arz` | `431e64e1d372e4ebee5d1048d3aca458923e1df8c97844274636f5373a01e292` |
| `…/grim-dawn-edition-III-20260808/gdx2/database/GDX2.arz` | `13fa0b93be15835958968ad672b9efa5159d7221a279aca791590390dd81a072` |
| `…/grim-dawn-edition-III-20260808/gdx3/database/GDX3.arz` | `e990e1265f14ff2ee241658433d4d666d399a5b0be27543ae9481fc97d6a2ae4` |
| `…/mods/survivalmode/database/SurvivalMode.arz` | `e9f6e2213eada8f5ffcc4fc430395b43c95384b745b629def096dbb2e7da29b6` |
| `…/survivalmode1/database/SurvivalMode1.arz` | `6ac10d6180bfa8491edfc89946d1cfbf166c5ca6442c5862ecf6947290021252` |
| `…/survivalmode2/database/SurvivalMode2.arz` | `940e40344e9dde53bfac8ff6576940d52ebfece600adeabe3774f9f0c3071e95` |
| `…/survivalmode3/database/SurvivalMode3.arz` | `e848791e4b15496670e4c78832075d9868e7b502e6eed93715c24e894902e12a` |
| `…/vendor/grim-dawn/Game.dll` (x86) | `4876d6bdb69cca71cfa987652cbd7a42cf6d5578564d02d09aaf9b55c078ab02` |
| `…/vendor/grim-dawn/Engine.dll` (x86) | `7141b51ae61b396fd0743da9e51471043329c51b3bb61d0037b2ce934864c87c` |
| `…/vendor/grim-dawn/Grim Dawn.exe` (x86) | `1a71e188ea3d7f83bec296e22acecf7cac71686c9c0c117d0eb03c9d7ada1ff4` |
| `…/vendor/grim-dawn/x64/Game.dll` | `7c62f1aa8b32ce3dbfb5a640b7af280203d28016b8f9e39225e36028136b26eb` |
| `…/vendor/grim-dawn/x64/Engine.dll` | `d6df581038af18184ce7f63d75ecbe56f350d12e49d396064445bda3a6650a2c` |
| `…/vendor/grim-dawn/x64/Grim Dawn.exe` | `82c42980a194e152bd91092461198e0d04d8e47aea14701d3a997d2e238691e3` |
| `…/vendor/grim-dawn/DBREditor.exe` | `4d11ae30b4c0faca7d8e4a2f410e023cd22bcc9cfad20a3a1598a5777794d93a` |
| `…/vendor/grim-dawn/ArchiveTool.exe` | `fae1c6ec40a6beeb3968ad15a10e7345ef025f47f552d002952b4f3a6c0cce0a` |
| `…/vendor/grim-dawn/AssetManager.exe` | `7e84db3f26adf9f18376251baa26c5450d7875ec5a54fd95487116f288a23aa3` |
| `…/research/scripts/gd_arz_adapter_2026_07_24.py` (carried, unchanged) | `040bd078a73f81ed7b839820fcfc15af1e74beba81a930fc147f1080bb317266` |
| `…/research/scripts/gd_arc_reader_2026_07_26.py` (carried, unchanged) | `a5def5a669270f6362f96dfcb932d0ba8a77b689919086675b97b95fa16f7597` |
| `…/gamora/notes/2026-08-16-kc2-pm4-i24d-engagement-census-landing.md` (commission context) | `69fee4ea7072c8018073fc5cc81df6a7714344c8ccbbbfe902863fb2a6327ba1` |

---

*Returned by legolas (UNKNOWN-RESEARCHER), 2026-08-16. Prereg committed alone as `d54f2c6c`
before any instrument ran; this file and the instrument follow in a second commit.*
