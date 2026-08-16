# KC2-PM4 · LAP Z — PREREGISTRATION · THE RING-OPERAND FORK PAIR

**Agent:** legolas (UNKNOWN-RESEARCHER) · **Conductor:** gandalf (`RUN-CONDUCTOR`) · **2026-08-16**
**Commission:** ruling `R-PM4-65 part 3`. Charter row `L-54`/`R-PM4-64`, `L-55`/`R-PM4-65`.
**Provenance of the question:** `UNREACHED-I24D-1`, named-not-decoded by gamora at the I-24-D
census landing (§ 10), root defect `D-I24D-1`.

> **THIS FILE IS COMMITTED ALONE, BEFORE ANY INSTRUMENT RUNS.** Sixth consecutive use; the commit
> graph is the attestation. Nothing below is edited after the instrument fires — grades and results
> are appended in `pm4z_findings.md`, never back-written here.

---

## § 0 — THE FORK PAIR (two questions, one lap)

### FORK (a) — WHICH OPERAND

When Grim Dawn's engine performs its melee contact/range test, what numeric value does it hold for
`gameengine.dbr : meleeTargetDistance`?

- **Limb A1 — STORED-FLOAT32 (promoted).** The value is whatever the compiled database stores,
  which is a 4-byte IEEE-754 single; promoted to a double for a double-precision reproduction that
  is `2.4000000953674316` (exactly `2.400000095367431640625`).
- **Limb A2 — DECIMAL 2.4.** The engine's operand is the decimal value `2.4` as cited by the DB
  reader / display path — i.e. some path re-parses or re-quantises the number such that the
  operative threshold is the double `2.4` (exactly `2.399999999999999911182158029987`).

### FORK (b) — SQUARED OR ROOTED

Does the engine's contact/range test compare **squared** distances (`dx²+dy²  ≤  r²`) or take a
**root** first (`√(dx²+dy²) ≤ r`)?

- **Limb B1 — SQUARED.**
- **Limb B2 — ROOTED.**
- (b) matters only insofar as it moves the *effective boundary radius* in metres. § 4 pre-registers
  the arithmetic that decides whether it moves it at all.

### The third admissible answer on either fork — **UNREACHED**

The corpus does not express it. This is a fully acceptable return and I will file it without
embarrassment on either limb independently.

### 0.1 ⚑ THE STAKES ARE CONTEXT, NOT A TARGET (Law 3)

I record here, before looking, that I know which way the stakes point. gamora's I-24-D § 10 reports
that ~59 % of `PX-LO`'s occupancy ticks fall inside the 9.5e-8 m window between the two (a)-limbs,
and that the measured occupancy metric moves 0.234 → 0.372 across it. **No term in this lap is
adjusted toward any outcome, and neither limb is designated by which grades better** (`R-PM4-27
part 3`). The occupancy number is not mine to produce. I state my own bets in § 4 so that a wrong
bet is visible in the git graph rather than quietly retired.

### 0.2 ⚑ SCOPING DISCLOSURE

This is a **RECORD lap**. It runs **no simulation**, reads **no sim outcome**, touches **no baton**,
and writes **nothing** outside
`agentic_orchestration/legolas/notes/2026-08-16-kc2-pm4-lap-z-ring-operand/` and one instrument
script under `agentic_orchestration/research/scripts/`. It does not re-open Lap Y's verdict, does
not re-grade I-24-D, does not fold anything, and does not repair `D-I24D-1` — the repair is
gamora's at the I-24 fold, on whatever verdict this lap returns.

### 0.3 ⚑ A PREMISE I WILL TEST, NOT ASSUME

The commission states as background that "the DBR files store single-precision floats." I treat
that as a **claim to be verified from the archive bytes**, not as a given. If the compiled record
turns out to carry something other than a 4-byte single for this field, fork (a) is mis-posed and I
report that as a commission-premise finding rather than silently executing around it.

---

## § 1 — PINNED INPUTS (re-verified at instrument start; **HALT** on the first mismatch)

Digests below were computed **before this file was committed**. Hashing a file is not an instrument
run; no content was read to produce them.

### 1.1 Carried pins — stated here verbatim from Lap Y § 1.1, independently re-hashed

| input | sha256 |
|---|---|
| `…/grim-dawn-edition-III-20260808/database/database.arz` | `2ad6d379285cfb745462316949e8d59e9450cb58a13f9ffa2fdeb70193183bfd` |
| `…/grim-dawn-edition-III-20260808/gdx1/database/GDX1.arz` | `431e64e1d372e4ebee5d1048d3aca458923e1df8c97844274636f5373a01e292` |
| `…/grim-dawn-edition-III-20260808/gdx2/database/GDX2.arz` | `13fa0b93be15835958968ad672b9efa5159d7221a279aca791590390dd81a072` |
| `…/grim-dawn-edition-III-20260808/gdx3/database/GDX3.arz` | `e990e1265f14ff2ee241658433d4d666d399a5b0be27543ae9481fc97d6a2ae4` |
| `…/grim-dawn-edition-III-20260808/database/templates.arc` | `679db83f019020ef7d4d27be8e61203006ee94e5c582dd8a59642f3fddd54602` |
| `…/vendor/grim-dawn/Game.dll` (x86) | `4876d6bdb69cca71cfa987652cbd7a42cf6d5578564d02d09aaf9b55c078ab02` |
| `…/vendor/grim-dawn/Engine.dll` (x86) | `7141b51ae61b396fd0743da9e51471043329c51b3bb61d0037b2ce934864c87c` |

### 1.2 ⚑ NEW PINS established by this lap

| input | sha256 | why new |
|---|---|---|
| `…/vendor/grim-dawn/Grim Dawn.exe` (x86) | `1a71e188ea3d7f83bec296e22acecf7cac71686c9c0c117d0eb03c9d7ada1ff4` | third shipped module; Lap V-2 read strings from it |
| `…/vendor/grim-dawn/x64/Game.dll` | `7c62f1aa8b32ce3dbfb5a640b7af280203d28016b8f9e39225e36028136b26eb` | **the x64 build has never been consulted by this run.** SSE-scalar x64 code distinguishes float32 from double *in the instruction mnemonic* (`mulss`/`comiss` vs `mulsd`/`comisd`) — the single most direct evidence class either fork could have |
| `…/vendor/grim-dawn/x64/Engine.dll` | `d6df581038af18184ce7f63d75ecbe56f350d12e49d396064445bda3a6650a2c` | as above |
| `…/vendor/grim-dawn/x64/Grim Dawn.exe` | `82c42980a194e152bd91092461198e0d04d8e47aea14701d3a997d2e238691e3` | as above |
| `…/vendor/grim-dawn/DBREditor.exe` | `4d11ae30b4c0faca7d8e4a2f410e023cd22bcc9cfad20a3a1598a5777794d93a` | **the shipped tool that authors DBR values.** Speaks to fork (a)'s storage limb from the *writing* side |
| `…/vendor/grim-dawn/ArchiveTool.exe` | `fae1c6ec40a6beeb3968ad15a10e7345ef025f47f552d002952b4f3a6c0cce0a` | shipped archive tool |
| `…/vendor/grim-dawn/AssetManager.exe` | `7e84db3f26adf9f18376251baa26c5450d7875ec5a54fd95487116f288a23aa3` | shipped asset pipeline |

### 1.3 Carried readers (byte-identical; NOTE-9)

| reader | sha256 |
|---|---|
| `…/research/scripts/gd_arz_adapter_2026_07_24.py` | `040bd078a73f81ed7b839820fcfc15af1e74beba81a930fc147f1080bb317266` |
| `…/research/scripts/gd_arc_reader_2026_07_26.py` | `a5def5a669270f6362f96dfcb932d0ba8a77b689919086675b97b95fa16f7597` |
| `…/research/scripts/pm4s_pe_2026_08_14.py` | `3c98664ded52dc427b9778cbd457295288de9c37386dbe45add938549f1de5ef` |
| `…/research/scripts/pm4f_lib_2026_08_13.py` | `aed0eda8606ffbd587e906588750429ae8e2845a3dbb1cb3ccedd1db8b6b462e` |

### 1.4 Commission provenance (read as context, not as evidence)

| input | sha256 |
|---|---|
| `…/gamora/notes/2026-08-16-kc2-pm4-i24d-engagement-census-landing.md` | `69fee4ea7072c8018073fc5cc81df6a7714344c8ccbbbfe902863fb2a6327ba1` |

---

## § 2 — EVIDENCE CLASSES (declared closed; nothing added later without a defect row)

⚑ **`R-PM4-64 part 3` obeyed in the commission itself:** the classes below name **which
already-pinned artifacts get re-queried under the new question** — `database.arz`,
`templates.arc`, and the three x86 modules are all prior pins, re-interrogated here.

| id | class | artifact | what it can say | grade ceiling |
|---|---|---|---|---|
| **EC-1** | **compiled-record byte read** — the raw `.arz` field entry for `meleeTargetDistance`: its type tag, its declared value count, and the exact 4 (or 8) payload bytes, reported as hex | `database.arz` (+ the three GDX overlays, checked for an override) | what the shipped database *literally stores* — the only place a "2.4 vs 2.4000000953674316" distinction can physically exist on disk | **DECODE** |
| **EC-2** | **template declaration** — the `Variable` block for `meleeTargetDistance` in `gameengine.tpl`: `name` / `class` / `type` / `description` / `defaultValue` | `templates.arc` | the declared type of the field, and whether the format admits a `double`-width numeric type at all | **DECODE** |
| **EC-3** | **format type-system census** — every distinct type tag present across the whole compiled DB, and every distinct `type` string declared across all templates | `database.arz`, `templates.arc` | whether *any* double-precision numeric type exists anywhere in the shipped data format. A decoded **absence** is a strong structural fact for fork (a) | **DECODE** or **decoded-absent** |
| **EC-4** | **record sweep for a squared-distance concept** — exhaustive field-name scan for `*Sq*` / `*Squared*` / any distance field whose declared units are area-shaped | `templates.arc`, `gameengine.dbr` | whether the *data layer* expresses fork (b) at all | **DECODE** or **decoded-absent** |
| **EC-5** | **string residency** for distance/range primitives (`DistanceSq`, `LengthSquared`, `Length2`, `SqrDist`, `meleeTargetDistance`, `GetDistance`, RTTI class names) across the six shipped modules + the three tools | six modules, three tools | corroboration that a squared-distance primitive exists in the engine's vocabulary. **`NOTE D-V2-1` honoured: no vtable base reads.** String residency alone never names *which* test uses it | **CORROBORATION ONLY** |
| **EC-6** | **targeted instruction-stream read (x64)** — locate the loader/consumer of the `meleeTargetDistance` field by a **citation-solid anchor** (the field-name string → its dword/rip-relative reference → the enclosing function), then read the surrounding SSE scalar instructions. `mulss`/`comiss`/`ucomiss` vs `mulsd`/`comisd`; presence/absence of `sqrtss`/`sqrtsd` | `x64/Game.dll`, `x64/Engine.dll` | **the only class that can DECODE fork (b)**, and independent confirmation on fork (a)'s precision | **DECODE**, *only if* every step of the anchor chain is cited by file + RVA + bytes. Any break in the chain ⇒ the claim is not made |
| **EC-7** | **IEEE-754 boundary arithmetic** — enumerate the candidate effective thresholds under the cross-product {A1,A2} × {B1,B2} × {float32-arithmetic, double-arithmetic} and report each as a distance in metres, with the pairwise deltas | pure arithmetic, no artifact | **bounds the stakes**; can prove a limb *inert* (two limbs that coincide exactly are not a fork). Cannot, alone, select a limb | **IDENTITY** (proves coincidence/non-coincidence only) |
| **EC-8** | **TQ/GD engine-lineage documentation** — community documentation of the ARZ/DBR compiled format and of the engine's range tests. Titan Quest counts as lineage evidence (same Iron Lore-derived engine, same ARZ/ARC container formats) and is cited **as lineage**, never as the shipped corpus | web, read-only | may supply a **LEAN**. **Never load-bearing.** Standing rule since the grimtools-vs-`.arz` contradiction | **LEAN / CORROBORATION ONLY** |

**Explicitly OUT of scope as decode evidence:** forum posts, wikis, community guides, grimtools.
Any such source may appear in the findings **only** as corroboration or as an explicitly-labelled
lean, never load-bearing.

---

## § 3 — ⚑ THE VERDICT VOCABULARY, PRE-COMMITTED

Fixed **now** so that I cannot invent a flattering grade after seeing the evidence. Each fork limb
is graded **independently**; (a) may land DECODED while (b) lands UNREACHED, or vice versa.

- **DECODED** — a shipped artifact **directly determines** the answer: the archive's own bytes, a
  template's own declaration, or an instruction stream read at a cited file + RVA with every anchor
  step cited. Nothing weaker earns it.
- **DECLARED** — no shipped artifact states the answer, **but** a structural property of the
  shipped format or of the shipped data leaves no admissible alternative, *and* that property is
  itself DECODED. A `DECLARED` verdict must publish the surviving alternative(s) it is rejecting
  and the exact structural fact that rejects them. It is **never** selected by which limb grades
  better downstream (`R-PM4-27 part 3`).
- **UNREACHED** — the evidence classes are silent. **Both limbs are published with their
  arithmetic**, and a lineage-based **LEAN** may be stated *if one exists*, explicitly labelled
  `LEAN — NOT A DECODE` and never propagated as a number.

**A grade may not be upgraded by rhetoric**, and no grade may be upgraded because the I-24 fold
needs an answer. If only EC-7 speaks, the verdict says so in the headline.

**⚑ A fourth outcome is admissible and must be reported if it obtains: `INERT`.** If EC-7 proves
that two limbs of a fork yield *bit-identical* effective thresholds, that fork is not a fork — it
is a distinction without a difference, and saying so is the strongest possible return.

---

## § 4 — PRE-REGISTERED PREDICTIONS, WITH MY BETS

Values below are stated **before** any instrument ran. `r32` denotes the exact float32 nearest
`2.4`, asserted here to be `2.400000095367431640625` (bit pattern `0x4019999A`).

| id | claim | my bet |
|---|---|---|
| `P-Z-1` | `database.arz` stores `meleeTargetDistance` as a **single 4-byte IEEE-754 float** with bit pattern `0x4019999A`, i.e. exactly `r32`. The commission's premise holds. | **PASS** |
| `P-Z-2` | `templates.arc` declares `meleeTargetDistance` with a **real/float**-class type, and **no template in the entire shipped corpus declares a double-precision numeric type** | **PASS** |
| `P-Z-3` | The compiled `.arz` type-tag alphabet contains **no 8-byte floating-point tag** — the format has no way to store `2.4` as a double | **PASS** |
| `P-Z-4` | **`r32² is exact in double.`** `r32` has a 24-bit significand, so `r32²` needs ≤ 48 bits and is representable exactly in a 53-bit double. Therefore **under double arithmetic, SQUARED and ROOTED comparisons have the identical threshold `r32`** ⇒ fork (b) is **INERT at double precision** | **PASS** |
| `P-Z-5` | **Under float32 arithmetic, fork (b) is NOT inert:** `fl32(r32²) ≠ r32²`, and the implied boundary radius differs from `r32` by `|Δ|` in the band **[1e-8 m, 1.5e-7 m]** — i.e. the *same order* as the 9.5e-8 m window fork (a) is worth | **PASS** |
| `P-Z-6` | No shipped template or record field anywhere in the corpus expresses a squared-distance quantity (EC-4 returns **decoded-absent**) | **PASS** |
| `P-Z-7` | ≥ 1 shipped module carries a resident string naming a squared-distance or length-squared primitive | **PASS** (corroboration only) |
| `P-Z-8` | **THE FORK-(a) VERDICT.** | I bet **A1 — STORED-FLOAT32**, at grade **DECODED or DECLARED** |
| `P-Z-9` | **THE FORK-(b) VERDICT.** | I bet **UNREACHED** — I bet I will *not* be able to cite the instruction stream that performs the melee range test |
| `P-Z-10` | EC-6's anchor chain (field-name string → reference → enclosing function) completes in ≥ 1 x64 module | **FAIL** — I bet it breaks |

**Wording of a failed prediction is never rewritten** (Lap X `P-X-4b` precedent, Lap Y `P-Y-8`
precedent). `P-Z-9` and `P-Z-10` are deliberately pessimistic bets against my own instrument; if
they fail, the lap returned more than I expected and the git graph will show it.

---

## § 5 — FALSIFIERS, ONE PER LIMB MINIMUM

| id | fires against | condition |
|---|---|---|
| `F-Z-A1` | **Limb A1 (STORED-FLOAT32)** | Any shipped evidence of a re-quantisation, decimal re-parse, or rounding step between the archive byte and the range comparison — e.g. a double-typed field in the format, a text-form DBR consulted at runtime, or an instruction stream that loads the field and rounds it. |
| `F-Z-A2` | **Limb A2 (DECIMAL 2.4)** | The archive byte read (EC-1) returns `0x4019999A` **and** EC-3 proves the format has no double-width numeric type. Under both conditions A2 requires positive evidence of a re-parse path; absent that, A2 has no physical carrier on disk. |
| `F-Z-B1` | **Limb B1 (SQUARED)** | A cited instruction stream showing `sqrtss`/`sqrtsd` on the melee range path, or a shipped field/declaration expressing a rooted distance comparison. |
| `F-Z-B2` | **Limb B2 (ROOTED)** | A cited instruction stream showing the field's square being formed and compared against a summed-squares term with no root. |
| `F-Z-C` | **fork (a) as posed** | EC-1 returns something other than a 4-byte single (e.g. a string, an 8-byte payload, a multi-value array). Then the commission premise is wrong, the fork must be re-posed, and I file it as a **commission-premise finding** with the corrected shape. |
| `F-Z-D` | **fork (b) as posed** | EC-7 proves both (b)-limbs bit-identical under the arithmetic the engine actually uses. Then fork (b) is **INERT** and the correct return is to say so, not to pick a limb. |
| `F-Z-E` | **the DECODED grade on either fork** | The relevant evidence classes are silent, or the EC-6 anchor chain breaks at any step. Best available grade is then `DECLARED` or `UNREACHED`. |

---

## § 6 — WHAT UNREACHED LOOKS LIKE (so I cannot quietly avoid returning it)

**Fork (a) returns UNREACHED** if and only if: EC-1's byte read is ambiguous or the field is absent
from the compiled record; **and** EC-2/EC-3 do not settle the format's type system; **and** EC-6
does not reach a cited load site. In that case both limbs are published with their exact decimal
expansions, `UNREACHED-I24D-1` stays named-not-decoded, and the I-24 fold is told plainly that the
corpus cannot settle it.

**Fork (b) returns UNREACHED** if and only if: EC-4 is decoded-absent; **and** EC-6's anchor chain
does not reach the melee range test's instruction stream; **and** EC-7 does not prove the fork
INERT. In that case both limbs are published with their boundary arithmetic, and any lineage lean
is labelled `LEAN — NOT A DECODE`.

**A weak answer is not upgraded to a strong one because a downstream fold wants one.** In
particular: the I-24 fold is pre-authorised (`R-PM4-65 part 4`) to import the ring constant *by
identity* on this lap's verdict. If this lap returns UNREACHED on fork (a), the honest downstream
consequence is that the constant's provenance stays open — and that is the finding.

---

## § 7 — DISCIPLINE STACK ACKNOWLEDGED

- `R-PM4-55 part 2` — full 64-hex sha256 on every artifact consulted; pinned inputs re-verified
  before use; **HALT** on drift.
- **Law 3** — the referent's numbers are GRADES, never inputs. gamora's 0.234/0.372 occupancy pair
  is context recorded in § 0.1 and is **not** consulted during grading.
- `R-PM4-27 part 3` — **no limb is designated by which one grades better.**
- `R-PM4-56 part 4` — any genuinely NEW mechanism is **NAMED, not decoded**.
- `NOTE D-V2-1` — **no vtable base reads**; every claim cites the exact artifact it came from; no
  claim rests on archetype knowledge or memory of how engines "usually" work. Where I know the
  archetype answer, I must still cite bytes or return UNREACHED.
- `GL-12` — decode, never estimate.
- `NOTE-9` — every emitted quantity carries its own basis.
- **Defects** — self-caught defects go in the findings defect table with disposition;
  commission-premise errors are reported, not silently executed around.
- **Determinism ×2** — the instrument runs twice end to end; artifacts must be byte-identical.
- **Read-only everywhere** outside this lap's notes directory and its one instrument script. No
  engine code, no sim file, no baton, no push.

## § 8 — OUTPUTS DECLARED IN ADVANCE

`pm4z_findings.md` · `pm4z_operand.json` · `pm4z_type_system.csv` · `pm4z_binary_anchors.json` ·
`pm4z_boundary_arithmetic.csv` · `pm4z_digests.json` · `decode.log`.
Instrument: `agentic_orchestration/research/scripts/pm4z_ring_operand_2026_08_16.py`.

**Commit order:** this file **ALONE** → then instrument + all outputs. **No push** (conductor
pushes at banking).

---

*Pre-registered by legolas (UNKNOWN-RESEARCHER), 2026-08-16, before any instrument ran.*
