# KC2-PM4 · LAP V-2 — THE `ProxyAmbush` DECODE · PRE-REGISTRATION

**Agent:** legolas (UNKNOWN-RESEARCHER) · **Conductor:** gandalf (RUN-CONDUCTOR)
**Authority:** `R-PM4-58 part 2`, ledger row `R-PM4-58` in
`agentic_orchestration/gandalf/notes/2026-08-13-kc2-pm4-replication-run-charter.md`.
Matt's word (2026-08-15, Q-b, verbatim): ***"decode it."*** **Date:** 2026-08-15.

**What this lap is.** Lap V surfaced `F-3M-1` — a THIRD roster mechanism, `ProxyAmbush` at spawn
point 5 — and, under the then-standing `R-PM4-56 part 4` HALT rule, named it and refused to touch
it. Matt has now authorised the decode. This file pins what I expect to find **before I look**, so
that the answers cannot be authored by the answer I want.

**Discipline in force:** GL-6 (full 64-hex on every input and output; no truncated handles —
`R-PM4-55 part 2`) · GL-12 (DECODE-NEVER-ESTIMATE; UNREACHED honest per limb) · NOTE-9 (no repair
outside my own seam; carried constants named with their emitting lap) · **Law-3 (the referent's
19–36 living / median 25 is a GRADE, NEVER an input — if I catch myself choosing between two
readings of a byte because one lands nearer 25, I stop and report the fork verdict-divergent)** ·
**L-46 (THIS FILE COMMITS BY ITSELF, IN ITS OWN COMMIT, BEFORE ANY INSTRUMENT OF THIS LAP RUNS —
priority is git-attested, not self-attested; held on first use at Lap V, held again here)** ·
`R-PM4-56 part 4` (a FOURTH roster-relevant mechanism = name it, quantify exposure, DO NOT decode).

---

## § 0 — RECONNAISSANCE PRECEDING THE HASH (declared in full, per CL-10)

Everything below was read or run **before** this file was written. **None of it is a result of this
lap.** It is orientation and it is named so the reader can discount it. If any statement here later
appears in `pm4v2_findings.md` as a finding of mine, that is a defect and I will label it one.

**Documents read:**

1. The commission text (gandalf, `R-PM4-58 part 2`), including the six decode targets (a)–(f) and
   the seven-item discipline block.
2. Run charter rows `L-47`…`R-PM4-58`.
3. My own Lap V `pm4v_findings.md` — § 0 headline table, § 6 UNREACHED census, **§ 6.1 `F-3M-1`
   verbatim**, § 7.1 fold list, § 7.2 DO-NOTs, § 8 digests.
4. My own Lap U `pm4u_findings.md` file inventory (not re-read in full this lap; the pursue decode
   `ShouldFindEnemy` / `ViewDistance` is carried by reference from `pm4u_pursue_decode.json`).
5. `research/scripts/pm4s_pe_2026_08_14.py` — the durable PE32 reader/objdump bridge (Lap S), which
   is the instrument this lap will use unchanged (NOTE-9).

**Shell reconnaissance run before the hash — declared because it shapes the hypotheses below:**

- **R-0.1** The three anchors the commission handed me are correct and the module is `Game.dll`
  (image base `0x10000000`, PE32 `coff-i386`, 25,091 exports). Confirmed by export-table lookup.
- **R-0.2 — ⚑ THE ONE MATERIAL PIECE OF RECON, AND IT SHAPES EVERY HYPOTHESIS BELOW.** The full
  `ProxyAmbush` export set is visible by NAME (no disassembly read, no byte of any body inspected):

  | RVA | decorated symbol | plain |
  |---|---|---|
  | `0x003541b0` | `??0ProxyAmbush@GAME@@QAE@XZ` | ctor |
  | `0x00354260` | `??1ProxyAmbush@GAME@@UAE@XZ` | dtor |
  | `0x00354400` | `?Load@ProxyAmbush@GAME@@UAEXABVLoadTable@2@@Z` | `Load(const LoadTable&)` |
  | `0x00354520` | `?UpdateSelf@ProxyAmbush@GAME@@UAEXH@Z` | `UpdateSelf(int)` |
  | `0x003546e0` | `?SaveState@ProxyAmbush@GAME@@UBEXAAVBinaryWriter@2@@Z` | `SaveState` |
  | `0x00354ab0` | `?RestoreState@ProxyAmbush@GAME@@UAEXAAVBinaryReader@2@W4Restoration@Entity@2@@Z` | `RestoreState` |
  | `0x00354dd0` | `?GetPlacedObjects@ProxyAmbush@GAME@@UBEXAAV?$vector@I@mem@@@Z` | `GetPlacedObjects(vector<unsigned>&)` |
  | `0x00354fb0` | `?PoolComplete@ProxyAmbush@GAME@@MAEXPAVProxyPool@2@ABV?$vector@VWorldCoords@GAME@@@mem@@@Z` | `PoolComplete(ProxyPool*, const vector<WorldCoords>&)` |
  | `0x00355000` | `?IsAlert@ProxyAmbush@GAME@@ABE_NXZ` | `bool IsAlert() const` (private) |
  | `0x003550c0` | `?PlaceNextObject@ProxyAmbush@GAME@@IAEXXZ` | `PlaceNextObject()` (protected) |
  | `0x005e7774` | `??_7ProxyAmbush@GAME@@6B@` | primary vftable |

  `IsAlert` and `PlaceNextObject` are **not** in the commission's anchor set; I found them by name
  and they are the reason hypotheses `H-2` and `H-3` below have the shape they do. Declared, so
  that "the names told me" is on the record and I cannot later present name-reading as decoding.
- **R-0.3** The corpus of record is `vendor/grim-dawn-edition-III-20260808`; the binaries of record
  are `vendor/grim-dawn/{Game.dll,Engine.dll}`, digests re-verified below and byte-identical to
  Laps U and V.
- **R-0.4** The seven p05 records and their eight identical field values are as the commission
  states; they are Lap V's finding, carried, **not re-derived and not re-claimed** here.

**I have NOT looked at, at the instant of this hash:** any byte of any `ProxyAmbush` function body;
any `Proxy` / `ProxyPool` function body; `proxyambush.tpl`'s field descriptions or defaults; the
Crucible Lua ambush branch beyond the one line the commission quoted; the p05 pool rosters for any
wave; any count, envelope or condition function for any wave. **Every number and every semantic
claim this lap will report is unobserved at this instant.**

---

## § 1 — INPUTS, PINNED (full 64 hex; re-hashed at instrument start, HALT on mismatch)

### 1.1 Corpus + binaries

| input | expected sha256 |
|---|---|
| `edition-III/database/database.arz` | `2ad6d379285cfb745462316949e8d59e9450cb58a13f9ffa2fdeb70193183bfd` |
| `edition-III/gdx1/database/GDX1.arz` | `431e64e1d372e4ebee5d1048d3aca458923e1df8c97844274636f5373a01e292` |
| `edition-III/gdx2/database/GDX2.arz` | `13fa0b93be15835958968ad672b9efa5159d7221a279aca791590390dd81a072` |
| `edition-III/gdx3/database/GDX3.arz` | `e990e1265f14ff2ee241658433d4d666d399a5b0be27543ae9481fc97d6a2ae4` |
| `edition-III/mods/survivalmode/database/SurvivalMode.arz` | `e9f6e2213eada8f5ffcc4fc430395b43c95384b745b629def096dbb2e7da29b6` |
| `edition-III/survivalmode1/database/SurvivalMode1.arz` | `6ac10d6180bfa8491edfc89946d1cfbf166c5ca6442c5862ecf6947290021252` |
| `edition-III/survivalmode2/database/SurvivalMode2.arz` | `940e40344e9dde53bfac8ff6576940d52ebfece600adeabe3774f9f0c3071e95` |
| `edition-III/survivalmode3/database/SurvivalMode3.arz` | `e848791e4b15496670e4c78832075d9868e7b502e6eed93715c24e894902e12a` |
| `edition-III/mods/survivalmode/resources/Scripts.arc` | `47e6426d9534e0ddd5f867ca4d2640e5aa42cc8ffd68baa1db7e8870a61fb009` |
| `edition-III/database/templates.arc` | `679db83f019020ef7d4d27be8e61203006ee94e5c582dd8a59642f3fddd54602` |
| `vendor/grim-dawn/Game.dll` | `4876d6bdb69cca71cfa987652cbd7a42cf6d5578564d02d09aaf9b55c078ab02` |
| `vendor/grim-dawn/Engine.dll` | `7141b51ae61b396fd0743da9e51471043329c51b3bb61d0037b2ce934864c87c` |

### 1.2 Prior-lap artefacts consumed as input (pinned NOW, verified at instrument start)

| input | expected sha256 |
|---|---|
| `lap-v/pm4v_findings.md` | `5450e1567fe58337827c20719ec477ee56a40351cbd7c49ab823d0896ca1b895` |
| `lap-v/pm4v_roster_arithmetic.csv` | `991f75cfdb43ddff06fb01fbd16c81693af020a56f7dfe315e87e11e4db4a93c` |
| `lap-v/pm4v_prediction.json` | `450d52c9c5c430b528d1e2435760ff2ed45dec60c53a3b1981c20cc9701e275b` |
| `lap-u/pm4u_geometry_v3.csv` | `5ab636ebccaef4b613b663db1dbf083e8a166d5e0db4dd4a5cf9e8e3423dfac2` |
| `lap-u/pm4u_pursue_decode.json` | `6efd193aaa88158154beda71a723dbc70feda5f963ad470437137af92f98d733` |

**HALT on any mismatch.** No instrument proceeds past a failed pin.

---

## § 2 — THE PRE-REGISTERED HYPOTHESES

Each is falsifiable at a named address or field, and each is graded in `pm4v2_findings.md` § 3 as
**HELD / REFUTED / UNREACHED**, honestly, including the ones I would rather have held.

### 2.1 `H-1` — **THE PRIMARY STRUCTURAL PREDICTION** (commission item 7 + target (a))

> **`spawnThreshold = 15` is compared against a count of the `ProxyAmbush`'s OWN currently-live
> placed objects — a REFILL / MAINTENANCE threshold — and NOT against (i) a count of players, (ii)
> a cumulative count of monsters killed, (iii) a distance, or (iv) a global living-monster count
> across the whole wave.**

Grounds for the guess, stated so the reader can weigh it: `GetPlacedObjects(vector<unsigned>&)`
exists as a public const accessor, which is the shape of a class that tracks *its own* placed
entity IDs and needs to count the live ones; and `PlaceNextObject` is singular.

**Falsifier:** the compare at or downstream of `UpdateSelf` `0x00354520` reads any operand other
than a live-count over the object's own placed set. If the operand is a *player* count I record
`H-1 REFUTED`, loudly, in § 0 of the findings.

**Sub-predictions, graded separately:**
- `H-1a` — the threshold is evaluated **per tick** inside `UpdateSelf(int)`, not on an event.
- `H-1b` — the comparison is **"live < threshold ⇒ place more"** (strict or non-strict; I do not
  pre-commit to which, and I will read the exact `jl`/`jle` and say so).

### 2.2 `H-2` — target (c), the release shape

> **`PlaceNextObject` places EXACTLY ONE object per invocation, so the 30-body group is a TRICKLE
> gated by `min/maxSpawnTime = 3.0`, not a single instantaneous release of 30.**

**Falsifier:** a loop inside `PlaceNextObject` (or its caller) that places `n > 1` per timer fire.

### 2.3 `H-3` — target (a)/(d), the arming gate

> **`alertArea = 100.0` is a RADIUS tested against player proximity, read by `IsAlert`
> (`0x00355000`), and it ARMS the ambush: before the ambush is alert, zero objects are placed.**
> `min/maxDelayTime = 4.0` is the delay from arming to the FIRST placement (`H-3a`).

**Falsifier:** `IsAlert` reads something other than a proximity/area test, or `alertArea` is
consumed as an area (m²) rather than a radius, or the delay governs something else.

### 2.4 `H-4` — target (b), composition

> **The ambush's bodies are drawn through the SAME `ProxyPool` machinery as an ordinary proxy —
> therefore the Lap V count-resolver `Game.dll sub_10357590` and the Lap V `F-8` `limitN` capacity
> cap BOTH apply — and `minGroupSize`/`maxGroupSize` bounds the number of PLACED BODIES (here
> degenerate at exactly 30).**

**Falsifier / the pre-registered leading alternative `H-4alt`:** `min/maxGroupSize` is **not** a
body count but a count of *placement positions*, *pool invocations*, or *`WorldCoords` slots*, with
the actual body count still governed by the pool's own `spawnMin`/`spawnMax`. `PoolComplete`'s
signature `(ProxyPool*, const vector<WorldCoords>&)` is consistent with **both**, which is exactly
why I am pinning the alternative rather than only the favourite. **If `H-4alt` is what the bytes
say, the p05 contribution is far smaller than `H-4` implies, and I report that outcome with the
same emphasis I would have given the large one.**

### 2.5 `H-5` — target (d), geometry

> **Placement coordinates are PROXY-LOCAL — derived from the p05 point's own position and its
> pool's placement geometry — NOT player-relative.** "Ambush" names *when* it fires, not *where*.

**Falsifier:** a player-entity read feeding the coordinate computation in `PoolComplete` /
`PlaceNextObject`.

### 2.6 `H-6` — target (e), post-spawn behaviour

> **Ambush-spawned bodies pursue exactly as Lap U's `ShouldFindEnemy` / `ViewDistance` decode
> describes.** The Crucible Lua's `IsAmbush() == false` gate suppresses only
> `LinkPatrolPointGroup`, i.e. it removes a **patrol** assignment, not the pursuit AI; a monster
> with no patrol group still acquires and chases.

**Falsifier:** ambush bodies carry a distinct AI/behaviour assignment, or `LinkPatrolPointGroup` is
load-bearing for acquisition rather than for idle patrol routing.

### 2.7 `H-7` — target (f), the SHAPE of the answer (pre-committed before the arithmetic)

> **If `H-1` holds, the per-wave p05 contribution is NOT a scalar. It is a CONDITION FUNCTION of
> runtime living-count, and I will emit the function plus its envelope, not an expected value.**

I pre-commit to this now precisely so that I cannot, after seeing the numbers, quietly collapse a
runtime-dependent term into a convenient scalar. Envelope bounds I *will* emit either way:
a decoded **floor** (bodies placed unconditionally, e.g. the initial fill) and a decoded **ceiling**
(the maximum the mechanism can ever deliver in one wave).

### 2.8 `H-8` — the directional claim, pinned before observation

> **The decoded p05 CEILING exceeds Lap V § 6.1's floor number on ALL SEVEN declaring waves**
> (floors: 151→4.5, 152→3.0, 153→4.5, 156→7.0, 157→3.0, 158→3.0, 159→1.0).

This is a directional bet made blind. It is graded 7/7 or it is graded honestly lower.

### 2.9 Expected-UNREACHED, declared in advance

- `X-1` — whether the ambush **re-arms** across a wave boundary or is one-shot per wave (may live
  in the Lua wave teardown rather than in `ProxyAmbush`).
- `X-2` — the **runtime kill rate** that the `H-1` condition function is evaluated against. That is
  gamora's seam (I-22), not measurable from records or binary. I will not estimate it.
- `X-3` — whether `SaveState`/`RestoreState` semantics change the count on a reload. Out of scope;
  the referent sitting is a single continuous run.
- `X-4` — the concrete `WorldCoords` values of the placement sites, if the pool computes them at
  runtime from navmesh rather than reading them from records.

---

## § 3 — HALT TRIGGERS (binding)

1. **Input digest mismatch** on any § 1 row ⇒ HALT, report, no findings emitted.
2. **A FOURTH roster-relevant mechanism** surfacing (`R-PM4-56 part 4`, standing) ⇒ **name it,
   quantify the exposure it puts on this lap's numbers, DO NOT decode it.** Same shape as Lap V's
   `F-3M-1` treatment of this very mechanism.
3. **Law-3 fork.** If two readings of the same bytes are both defensible and they differ in how
   near the result lands to the referent's 19–36 / median 25, I do **not** pick. I report the fork
   as **verdict-divergent** and hand both to the conductor.

---

## § 4 — DO-NOT, BINDING ON MYSELF THIS LAP

- **DO NOT** let `minGroupSize = 30` become a headline number before `H-4` vs `H-4alt` is settled
  by bytes. Thirty is a field value, not a finding.
- **DO NOT** convert a runtime-conditional term into a scalar because the hand-off would be tidier
  (`H-7` is pinned above precisely to make this a violation rather than a judgement call).
- **DO NOT** re-derive or re-claim Lap V's `F-3` … `F-8`. They are carried by citation.
- **DO NOT** write anywhere outside this lap directory and `research/scripts/`. Read-only on the
  vendor tree, the engine repo, and every other agent's notes.
- **DO NOT** silently repair Lap V's § 3 numbers. Lap V's floors stay as published; this lap emits
  a **replacement table** that says which floor it replaces and by how much.

---

## § 5 — DELIVERABLES

| file | contents |
|---|---|
| `PREREGISTRATION.md` | **this file — committed ALONE, before any instrument** |
| `pm4v2_findings.md` | `F-*` findings at named addresses/fields; § 3 hypothesis grades; per-wave contribution table or condition functions; UNREACHED census; `D-V2-*` defects; § hand-off with DO-NOTs |
| `pm4v2_ambush.json` | machine-readable decode: trigger operands, timers, geometry, composition |
| `pm4v2_contribution.json` | per-wave condition functions / envelopes for the seven declaring waves |
| `pm4v2_disasm.txt` | the disassembly evidence, verbatim, at the named RVAs |
| `pm4v2_digests.json` | full-64 digests of every input and output |

*Pre-registered by legolas (UNKNOWN-RESEARCHER), 2026-08-15, before any instrument of Lap V-2 ran.*
