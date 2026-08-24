# KC2 MODEL-COMPLETION RUN · D-4c — the DoT STACKING FUNCTION, decoded

> **Run:** KC2 Model-Completion (charter `agentic_orchestration/gandalf/notes/2026-08-24-kc2-model-completion-run-charter.md`) · **Conductor:** gandalf (`RUN-CONDUCTOR`) · ledger **L-24 / L-25 / L-29**
> **Author:** legolas (UNKNOWN-RESEARCHER) · **Date:** 2026-08-24
> **Named target:** resolve the four unverified questions filed in D-4b § 5, at the RVAs it named.
> **Laws:** READ-ONLY on every source · **Law 3 — decode-before-declare, no guesses, no fitted constants** · GL-12 decode-never-estimate · NOTE-9 every quantity asserts its basis · GL-6 digests (§ 9).

---

## VERDICT — **DECODED.** All four questions resolved; the stacking rule is stated implementably below.

Lap I § 5.3 declared facet (i) **UNDECODABLE-FROM-SUBSTRATE**. That declaration was made without the
25,091-symbol export table in hand. **It is wrong, and it is now retired.** The stacking function is
fully readable from `Game.dll`, and the decisive control parameter turns out to be a
**developer-named, developer-described field in `records/game/gameengine.dbr`**.

**The one-line rule.** Per *(damage type, attacker)* timeline, at each 100 ms tick the engine sums a
set of per-source instances. **Re-application by the same source takes a MAX per tick-bucket; distinct
sources ADD.** The additive weight of the *i*-th strongest source is `damageMagnitude[min(i, N−1)]%`
— a first-class diminishing-returns table that Crate ships as **`[100.0]`**, i.e. **1.00 for every
ordinal, no diminishing at all**.

> **The finding under the finding.** D-4 listed candidate **(d) partial / capped** as *UNTESTED*.
> It is neither absent nor present: **the engine implements it as a first-class hook and Crate ships
> it neutral.** The authoring schema names it in the developers' own words —
> `description = "Decreasing same type duration damage"` — and the shipped array has exactly one
> element, `100.0`. A model pack that recorded only "GD stacks DoTs additively per source" would
> lose the more useful fact: *GD's engine has a per-ordinal attenuation dial, and it is turned off.*

---

## 1 — THE FOUR QUESTIONS, ANSWERED

D-4b § 5 filed four named unverified questions. Verdicts, each with its binary citation.

| # | D-4b § 5 question | verdict |
|---|---|---|
| **Q1** | *"what the `DurationDamageSource` pair actually keys on"* | **RESOLVED (structure + rule), PARTIAL (provenance).** See § 2. |
| **Q2** | *"the relationship between the two containers at `[entry+0x0c]` and `[entry+0x14]`"* | **RESOLVED.** `+0x0c` is a **per-attack scratch** timeline; `+0x14` is the **live** timeline. `DurationDamageManager::EndAttack` commits scratch→live and clears scratch. See § 3. |
| **Q3** | *"why the writer sets instance `+0x00` and `+0x04` while the reader sums `+0x04` and the refresh path `maxss`-es `+0x00`"* | **RESOLVED.** `+0x00` is the **base** per-tick value (the max-merged authoritative per-source figure); `+0x04` is the **effective** value after the stack-ordinal multiplier. The tick sums `+0x04`. See § 4. |
| **Q4** | *"how `offensiveSlow<X>Global` / `XOR` participate"* | **RESOLVED, and the answer is: not at all in the stacking function.** Both are *application gates* two layers upstream, in `DamageAttributeStore`. See § 6. |

D-4b also asked, implicitly, for **any cap/limit fields**. **Decided NEGATIVE** — see § 5.

---

## 2 — Q1 · THE SOURCE KEY

Two named exports settle the structure without inference:

| export | RVA | body | meaning |
|---|---|---|---|
| `?GetDamageSourceId@CombatAttribute@GAME@@QBEABUDurationDamageSource@2@XZ` | `0x000da0b0` | `lea eax,[ecx+0x10]; ret` | **`DurationDamageSource` is the 8-byte pair at `CombatAttribute+0x10`** |
| `?SetSkillSource@CombatAttribute@GAME@@UAEXI@Z` | `0x000d70e0` | `mov [ecx+0x18], eax; ret` | the **fallback** key is a `unsigned int` skill source |

`?AddDamage@DurationDamageManager@GAME@@UAEXW4CombatAttributeType@2@MMABUDurationDamageSource@2@IM@Z`
carries both in its own mangled signature: `(type, damage, duration, const DurationDamageSource&, unsigned int, float)`.

**The keying rule**, read off the insert path at `0x0020d6ed`–`0x0020d822` **[F-E6]**:

```
incoming key :  (S.first, S.second)          if S.first != 0        S = the DurationDamageSource
                (S.skillSource, 0)           otherwise

instance key :  (inst+0x0c, inst+0x10)       if inst+0x0c != 0
                (inst+0x14, 0)               otherwise
```

The two are computed by the **same** two-alternative branch, and the instance layout mirrors the
incoming struct field-for-field (`S+0x10→inst+0x0c`, `S+0x14→inst+0x10`, `S+0x18→inst+0x14`, written
at `0x0020d844`–`0x0020d85a`). Match ⇒ `maxss`. No match ⇒ append.

**Named residual (honest).** I decoded the *structure* and the *rule* exactly. I did **not** name
what the two dwords semantically are. Traced upward they are
`{ arg1 of DamageAttributeDur::AddDamageToAccumulator , thisDamageAttribute->field_0x54 }`
(`0x00142821`–`0x00142824`, **[E1]**), and `AddDamageToAccumulator`'s first parameter is an
un-named `unsigned int` in the mangled signature. Naming it needs a caller walk I did not do.
**This does not affect the stacking rule** — the rule is "same key ⇒ max, different key ⇒ add",
and the key is decoded. But a reader should not attribute to me a claim that the pair is
"(caster entity, skill)" or similar. **I have not established that.**

---

## 3 — Q2 · THE TWO CONTAINERS (the piece D-4b could not see)

This is the question whose answer reorganises everything else, so it is worth stating plainly:
**D-4b's naive reading of the `maxss` was directionally right but structurally mis-sited.** The
`maxss` does not operate on the live timeline; it operates on a **per-attack copy** of it.

### 3.1 The entry object

The destructor `0x0020c050` **[F1]** is the proof. It sets `vptr = 0x105cf034`, destroys a
`std::list` at `+0x14`, then one at `+0x0c` (MSVC destroys members in reverse declaration order),
then `operator delete(this, 0x24)`. So:

```
entry (0x24 = 36 bytes), one per (CombatAttributeType, attacker):
  +0x00  vptr
  +0x04  attacker id           (set from manager+0x18 — see § 3.4)
  +0x08  CombatAttributeType
  +0x0c  list<vector<Instance>>  SCRATCH   (_Myhead @0x0c, _Mysize @0x10)
  +0x14  list<vector<Instance>>  LIVE      (_Myhead @0x14, _Mysize @0x18)
  +0x1c  int  ms accumulator
  +0x20  int  ticks due this frame
```

Each list node is a **tick bucket** holding a `vector` of 24-byte instances. `sizeof(node)=0x14`
(next + prev + 3-pointer vector); `sizeof(instance)=0x18`, confirmed by the `imul 0x2aaaaaab; sar 2`
divide-by-24 idiom used at every stride site.

That the live list is the timeline is settled by three query methods on the same vtable, all reading
`+0x14`:

| slot | RVA | body | reading |
|---|---|---|---|
| 3 | `0x0020dc30` **[F7]** | `imul eax, [ecx+0x18], 0x64` | **remaining duration (ms) = liveList.size() × 100** |
| 5 | `0x0020dbd0` **[F8]** | Σ `inst+0x04` over the **first 10** buckets | **damage in the next 1.00 s** |
| 4 | `0x0020dc40` **[F9]** | Σ `inst+0x04` over **all** buckets | total remaining DoT |

> Slot 5 is an independent structural corroboration of D-4b's PER-SECOND verdict: the engine's own
> "rate" query is *ten buckets*, and ten buckets is one second only if a bucket is 100 ms and the
> stored figure is a per-tick tenth. It is the same fact from a different function.

### 3.2 Copy-on-write, decoded

```
AddDamage (any number of times within one attack)
   ├─ if SCRATCH.empty():  SCRATCH = LIVE                 0x0020d73c–0x0020d74a  → list::assign @0x20c6c0
   ├─ if SCRATCH.size() < nTicks:  SCRATCH.resize(nTicks) 0x0020d757–0x0020d777  → list::resize @0x20e4b0
   └─ merge the rider into SCRATCH buckets [0, nTicks)     § 4

EndAttack()                                                ?EndAttack@DurationDamageManager@GAME@@QAEXXZ @0x208c30
   └─ per entry, 0x0020d940 [F2]:
        if LIVE.empty():        LIVE = SCRATCH
        else:                   if LIVE.size() < SCRATCH.size(): LIVE.resize(SCRATCH.size())
                                lockstep j:  LIVE[j] = SCRATCH[j]        ← vector::operator= @0x20e2e0 [F3]
        SCRATCH.clear()                                                   ← list::clear @0x20c470
```

`0x0020e2e0` **[F3]** is MSVC `vector::operator=` — self-assign guard, then *overwrite* semantics
(empty source ⇒ `_Mylast = _Myfirst`, i.e. the destination is **cleared**, not left alone). So the
commit is an **assignment**, not an append. Because the scratch was seeded as a **copy of the live
timeline**, the merge decisions in § 4 are nonetheless made against the *live* instances. That is
why D-4b's naive reading survives: it reaches the right rule through the wrong object.

`?BeginNewAttack@...@QAEXW4ParametersCombatStyle@2@@Z` @`0x208cd0` is the counterpart; `EndAttack` is
called from `CombatManager::TakeAttack`, `Character::DebufTarget`, and the buff/trap/freeze appliers
(6 call sites).

### 3.3 The tick loop, closed

```
Update(dtMs)         0x00207f40 [E8]   per entry:  acc += dtMs
                                                   ticksDue = acc / 100 ;  acc %= 100      (cmp edi,0x64)
ExecuteDamage        0x00208370 [E9]   per entry:  vtable[2] @0x20da10 [E7]
                                                     sum = Σ over the first `ticksDue` LIVE buckets
                                                           of Σ inst+0x04            (addss @0x0020da60)
                                                     out  = max over those of inst+0x08
                                                     ids  = collected, then sorted + deduped
                                                   → CombatManager::ApplyDamage(sum, …, ids)
Update tail          0x0020829d      per entry:  0x0020dc80 [F6]
                                                   pop_front × ticksDue  (unlink, --_Mysize, free vec)
                                                 if LIVE.size()==0 → erase the entry
```

`0x0020dc80` **[F6]** is a second, independent binary attestation of the **100 ms** period: exactly
one bucket retires per 100 ms of elapsed game time. (D-4b's B-1 got it from `duration × 10.0f` and
`cmp edi,0x64`; this is a third site.) Note the loop is hitch-safe: if a frame exceeds 100 ms,
`ticksDue > 1`, the sum spans that many buckets, and that many are retired — no damage is lost.

### 3.4 Entries are keyed by **(damage type, attacker)**

`AddDamage` selects its entry by `E+0x08 == type && E+0x04 == manager+0x18` (`0x00208ad6`,
`0x00208ae0`, **[E5]**). And `?SetAttacker@DurationDamageManager@GAME@@QAEXI@Z` is at RVA
**`0x000d70e0`** — byte-identical to, and COMDAT-folded with, `CombatAttribute::SetSkillSource`
(`mov [ecx+0x18], eax; ret`). So `manager+0x18` is the **attacker id**, and each attacker gets its
own timeline per damage type. Corroborated downstream: `ExecuteDamage` compares `entry+0x04` against
a game-object field to decide whether the tick counts toward the local player's stats
(`0x002084e7`–`0x002084fd`).

**Consequence for the rule: two distinct attackers never share a bucket, and their damage is applied
through two separate `ApplyDamage` calls** — so resistance is applied per attacker-timeline, not to a
merged total.

---

## 4 — Q3 · THE MERGE, AND THE STACK-ORDINAL MULTIPLIER

Per bucket `j ∈ [0, nTicks)`, where `nTicks = (int)(duration′ × 10.0f)` (**truncating**, `cvttss2si`
@`0x0020d6fe`) and `perTick = damage × 0.1f` (@`0x0020d7b5`):

```
1.  scan the bucket for an instance whose key == incoming key        0x0020d80d–0x0020d820
      MATCH    :  inst[+0x00] = max(inst[+0x00], perTick)            0x0020d828  maxss
      NO MATCH :  append {  +0x00 = perTick, +0x04 = perTick,
                            +0x08 = arg6,  +0x0c/+0x10/+0x14 = key } 0x0020d870  push_back @0x20e420

2.  sort the bucket DESCENDING by +0x00                              0x0020d899  std::sort @0x20ea70 [F4]
      comparator is INLINED: comiss on offset +0x00, strict-greater  0x0020ef9c / 0x0020effa [F5]

3.  for each instance at ordinal i in the sorted bucket:             0x0020d8ab–0x0020d8e6
      inst[+0x04] = inst[+0x00] × damageMagnitude[min(i, N−1)] × 0.01f
```

Step 3 is the piece nobody had. `[ebp-0x48]` is a local copy of a `vector<float>` taken from
`gGameEngine + 0x292d4` at function entry (`0x0020d6cb`–`0x0020d6de`) — the very member exported as
**`?GetDurationDamageV@GameEngine@GAME@@QBEABV?$vector@M@mem@@XZ`**.

**Where that vector comes from** — `GameEngine::LoadFromDatabase`, `0x002579f2`:

```
0x002579f2  lea  eax, [edi + 0x292d4]
0x002579f8  push eax                     ; out
0x002579f9  push 0x105529ec              ; "damageMagnitude"
0x00257a03  call [reader_vtbl + 0x44]    ; read float-array field
```

**The authoring schema, `database/templates.arc :: gameengine.tpl`:**

```
Variable
{
    name         = "damageMagnitude"
    class        = "array"
    type         = "real"
    description  = "Decreasing same type duration damage"
    value        = ""
    defaultValue = ""
}
```

**The shipped value, decoded from the raw `.arz` field block (type, COUNT, values — not read through
any adapter's singleton collapse):**

| pull | type | COUNT | values | multiplier at every ordinal |
|---|---|---:|---|---:|
| `vendor/grim-dawn` **v1.2.3.4** | real | **1** | `[100.0]` | **1.00** |
| `vendor/grim-dawn-edition-III-20260808` | real | **1** | `[100.0]` | **1.00** |

**No archive overrides it.** Because the whole rule turns on this one array, every `.arz` in both
pulls was scanned field-by-field (`d4c_step10_override.py`): **13 archives, 172,255 records, and
`damageMagnitude` appears in exactly 6 records — all of them `gameengine`, all `COUNT=1`, all
`[100.0]`.** The three expansions (`GDX1`, `GDX2`, `GDX3`), all four survival-mode archives and the
bundled mod contain **zero** occurrences, so none of them can shift the stacking regime.

| archive | records | `damageMagnitude` |
|---|---:|---:|
| `database.arz` (base) | 34,114 / 34,171 | 3 — `records/game/gameengine.dbr` + 2 dev archives, all `[100.0]` |
| `GDX1` / `GDX2` / `GDX3` | 18,447 / 16,451 / 24,307 | **0 / 0 / 0** |
| `SurvivalMode` ×4 | 3,147 / 1,004 / 811 / 1,433 | **0** |

Because `N = 1`, the index `min(i, N−1)` is `0` for every ordinal, so **`inst[+0x04] = inst[+0x00]`
for every instance** and the tick sum is a plain unweighted sum. The sort in step 2 is therefore
a no-op *numerically* in shipped data — but it is not decorative: it is what makes the ordinal
meaningful, and the descending order means the **strongest** source occupies ordinal 0 and would
keep full weight under any decreasing table. That is exactly what the developers' description says.

**Q3 answered:** `+0x00` = base per-source per-tick value, the field the same-source `maxss` merges;
`+0x04` = effective value after the ordinal multiplier, the field the tick sums. Two fields because
the base must survive re-normalisation each time the bucket's population changes.

---

## 5 — CAP / LIMIT FIELDS · **DECIDED NEGATIVE** (with the search record)

The commission asked for "any cap/limit fields". There are none, and the search is recorded rather
than asserted. Every `cmp`/`test` against a non-trivial immediate in the six functions that touch the
instance vector (`d4c_step8_verify.py`, V5):

| function | RVA | non-trivial immediate compares |
|---|---|---:|
| insert / merge | `0x0020d6b0` | **0** |
| `std::sort` | `0x0020ea70` | 3 × `cmp ecx, 0x20` |
| insertion sort | `0x0020ef70` | **0** |
| per-tick sum | `0x0020da10` | **0** |
| `EndAttack` per-entry commit | `0x0020d940` | **0** |
| bucket retire | `0x0020dc80` | **0** |

The three `0x20` are the MSVC introsort insertion-sort threshold, not a game cap. Excluded as
allocator/overflow guards, and named so the exclusion is auditable: `0x3fffffff` and `0xaaaaaaa`
(`vector::max_size` for 4- and 24-byte elements), `0x1000`/`0x23`/`0x1f` (small-block heap checks),
`0x2aaaaaab` (the divide-by-24 magic).

**So:** no cap on simultaneous sources per bucket; no cap on bucket count (i.e. on DoT duration); no
truncation of the live timeline on commit. The **only** attenuation mechanism in the whole path is
`damageMagnitude`, and it is neutral.

---

## 6 — Q4 · `Global` AND `XOR` — decoded, and out of the stacking function

Both are `class = "variable"`, `type = "bool"`, `description = ""` in
`templatebase/parameters_offensive.tpl` — 17 of each among the 167 `offensiveSlow*` Variables. The
schema is silent, so this is decoded from the binary.

They are read by named per-class virtuals — `?GetLoadGlobalTag@DamageAttributeDur_Poison@GAME@@MBEPBDXZ`
(→ `"offensiveSlowPoisonGlobal"`) and `?GetLoadXorTag@...` (→ `"offensiveSlowPoisonXOR"`) — and the
flags sort each rider into one of **three lists** on `DamageAttributeStore`. The driver is
`?AddDamageToAccumulator@DamageAttributeStore@GAME@@UBEXIAAVCombatAttributeAccumulator@2@IMM@Z`
@`0x00156bf0` **[F11]**:

| list | store range | behaviour |
|---|---|---|
| plain | `+0x1c … +0x20` | each rider called with `global = 0` → **rolls its own chance** (`0x00156c31 push 0`) |
| **Global** | `+0x10 … +0x14` | **one** Park–Miller roll (`16807 / 127773 / 2836`, `0x00156ce5`–`0x00156d05`) against the store's `globalChance[rank]` gates the **whole list**; members are then called with `global = 1` (`0x00156d84 push 1`) → per-rider chance roll **skipped** |
| **XOR** | `+0x04 … +0x08` | pass 1 sums `GetChance(rank)` over the list; roll `uniform(0, total)`; pass 2 walks accumulating until cumulative ≥ roll and calls **exactly that one** with `global = 1` (`0x00156e40`–`0x00156e94`) → **chance-weighted roulette, exactly one member applies per attack** |

The `global` bool is arg5 of `DamageAttributeDur::AddDamageToAccumulator`, and its only use is the
early gate at `0x001425dd`–`0x001425fd` **[E1]**: `if (!global && !accumulator->RollChance(chance)) return;`.

**Verdict:** `Global` and `XOR` determine **whether and which** riders apply. Neither flag reaches
`DurationDamageManager`; neither appears anywhere on the merge, sort, multiplier, tick or retire
paths. **They do not participate in the stacking function.** They matter to a model pack only as
*population* effects — an item with 6 XOR-flagged riders contributes exactly one instance per attack,
not six.

---

## 7 — THE COMPOSED RULE (implementable)

Everything above, stated once, at the level a designer or an engine author can act on.

**State.** For each **(damage type, attacker)** pair on a target, a timeline of 100 ms buckets. Each
bucket holds a set of instances keyed by source; each instance carries a base per-tick value.

**Application** of a rider with rolled `damage` (a **per-second rate**, D-4b) and rolled `duration′`
(seconds, post-`ModifyDuration`):

```
nTicks  = trunc(duration′ × 10)          # truncating, not rounding
perTick = damage × 0.1                   # 1/10 s worth of the per-second rate

for j in 0 .. nTicks-1:                  # extend the timeline if it is shorter
    if bucket[j] contains an instance with this source key:
        that.base = max(that.base, perTick)          # SAME SOURCE  → MAX
    else:
        bucket[j].append(instance(base = perTick, key))   # NEW SOURCE → ADD
    bucket[j].sort(by base, DESCENDING)
    for i, inst in enumerate(bucket[j]):
        inst.effective = inst.base × damageMagnitude[min(i, N-1)] / 100
```

**Tick** (every 100 ms per timeline):

```
applied = Σ over instances in bucket[0] of inst.effective
CombatManager::ApplyDamage(applied, type, dedup(source ids))    # resistance applied here
retire bucket[0]
```

**Consequences worth stating explicitly, because they are the ones a summary would blur:**

1. **Same-source re-application is neither "strict refresh" nor "replace" nor "max(remaining,new)".**
   It is a **per-tick-bucket max over the union of the two windows**. If the new application is
   weaker but longer, the overlap keeps the *old* (stronger) value and the tail gets the *new*
   (weaker) one. If stronger but shorter, the overlap is raised and the old tail survives unchanged.
   Equivalently: **for one source, the rate at time *t* is the max over all that source's live
   applications still covering *t*.**
2. **Remaining duration becomes `max(old_remaining, new_duration)`** — never truncated, because the
   walk covers only `[0, nTicks)` and the commit never shortens the live list.
3. **Across sources the rates add**, at weight `damageMagnitude[ordinal]`. In shipped GD that weight
   is **1.00 at every ordinal**, so it is a plain sum. The strongest source holds ordinal 0.
4. **Across attackers nothing merges at all** — separate timelines, separate `ApplyDamage` calls.
5. **No cap** on sources, duration, or magnitude anywhere on the path (§ 5).
6. `CombatAttributeDurFixedDamage` is a **separate, simpler** path **[F14]**: same bucket timeline,
   but a flat `maxss` on `+0x04` with **no source key, no sort, no multiplier** — i.e. a pure
   strongest-wins channel. Declared as a scoped distinction; the `offensiveSlow*` riders do not use it.

### Against D-4's candidate table

| D-4 candidate | D-4 status (video) | **D-4c status (binary)** |
|---|---|---|
| (a) full stacking (sum) | NOT CONFIRMED | **numerically CORRECT in shipped data**, as the `N=1, [100.0]` special case of (c) |
| (b) no stacking / refresh-only | DISFAVOURED, NOT FALSIFIED | **FALSIFIED as a global rule** — and **EXACTLY CORRECT as the same-source sub-rule** |
| (c) per-source stacking | INDISTINGUISHABLE from (a) | **CONFIRMED — and the indistinguishability is now explained**: with `damageMagnitude = [100]`, (c) *is* (a). They were never separable because they coincide. |
| (d) partial / capped | UNTESTED | **mechanism PRESENT and first-class (`damageMagnitude`, "Decreasing same type duration damage"); DISABLED in shipped data** |

---

## 8 — VIDEO-CONSISTENCY CHECK (stated explicitly, as commissioned)

Cross-checked against the D-4 video lap (`…/2026-08-24-kc2-dot-stacking-video-lap/README.md`).
**Corroboration only — the verdict rests on § 4's binary evidence.**

| D-4 measurement | decoded rule's prediction | consistent? |
|---|---|---|
| **M-1/M-2: 100 ms tick**, modal 6 frames @60 fps, twice | hard-coded: `nTicks = dur × 10`, `cmp edi,0x64`, **and** `pop_front` retiring exactly one bucket per 100 ms | **YES — exact**, and now from three independent binary sites |
| **M-3: 120 – 690 HP/s** envelope, max **690.0 HP/s** | mechanism is uncapped and unattenuated (§ 5), so any observed rate is admissible; the figure constrains the *roster population*, not the *rule* | **YES — vacuously.** Stated as such rather than dressed up as a passed test |
| **§ 3.3 ceiling: 690.0 vs 1,568.7 HP/s** refresh-only ceiling (per-second limb) | that ceiling was the ceiling **of the hypothesis the binary falsifies**. Under additive-across-sources there is no such bound | **YES**, and D-4b § 4's "non-discriminating" verdict is now explained rather than merely restated |
| **§ 3.4, n=16 re-application asymmetry**: rises large (up to **3.4×** off a single hit), falls small and gradual | a single hit can introduce **several new instances** (distinct families and/or distinct sources), each entering at full weight ⇒ large rises. Decay is bucket-by-bucket `pop_front` at 100 ms with longer instances persisting ⇒ small, gradual falls | **YES — and this is the sharpest of the four.** D-4 recorded the direction and refused to ship it (n=16, unattributable). The binary supplies the mechanism the direction was pointing at |

**No contradiction on any measured quantity.** The one place D-4 and D-4c would have collided —
if the binary had decoded to strict refresh-only — did not occur.

**Honesty note on the ceiling arithmetic.** D-4b § 4 re-ran D-4's ceiling test and found it
non-discriminating. That conclusion stands and is *unchanged* by this lap; what changes is that we no
longer need it. The test was an attempt to infer the rule from an aggregate; the rule is now read
directly. I did not re-run it and I did not look for a population assumption that would rescue it.

**Display-layer guard honoured.** No tooltip, wiki or grimtools figure is joined to any KC2 row
anywhere in this lap. D-4b's § 5 residual (item tooltips may print `field × duration`) is **not**
closed here and remains open. Indeed this lap *adds* to it: instance `+0x08` (= `AddDamage` arg6)
is **max**-aggregated at tick time into an out-parameter that `Update` folds into a manager-level
per-second statistic at `[manager+0x4c]` (`0x00208067`) which feeds a UI/stats call. **That is a
display channel carrying a MAX, not a sum** — a figure quoted from any surface fed by it would not be
the tick damage. Named, not resolved.

---

## 9 — VERSION SKEW, ARTIFACTS, DIGESTS

**Skew, checked not assumed.** The binary is v1.2.3.4 (no engine binary ships in the ed-III pull, so
no `Game.dll` diff is possible — same limit D-4b recorded). The one **data** value the rule depends
on was therefore read from **both** pulls independently and is identical: `damageMagnitude`,
`type=real`, `COUNT=1`, `[100.0]`; the `gameengine.tpl` schema block is byte-identical across pulls;
and the override scan (§ 4) covers all 13 archives in both pulls, 172,255 records, finding no other
writer of the field. **The decisive parameter does not move between the pulls and is not overridden
by any expansion, survival mode or bundled mod.**

| file | contents |
|---|---|
| `d4b_lib.py`, `d4b_pe.py`, `d4b_dis.py`, `d4b_xref.py` | D-4b's READ-ONLY harness, reused unmodified (incl. the D-D4b-1 PE-export fix) |
| `d4c_step1_magnitude.py` | locates `damageMagnitude` on the GameEngine record |
| `d4c_step2_tpl.py` | extracts the authoring schema block (the developer description) |
| `d4c_step3_rawfield.py` | hand-decodes the raw `.arz` field block — type / **COUNT** / values |
| `d4c_step4_vtable.py` | attributes the insert and sum slots to their vtables |
| `d4c_step5_globalxor.py` | classifies all 167 `offensiveSlow*` Variables |
| `d4c_step6_xorbin.py` | locates the `Global`/`XOR` tag strings and their `GetLoad*Tag` owners |
| `d4c_step7_caller.py` | resolves the `AddDamageToAccumulator` vtable slot and its driver |
| `d4c_step8_verify.py` | **V1** bit-exact constants · **V2** merge/sum sites · **V3** comparator key+direction · **V4** the multiplier table, both pulls · **V5** the cap scan |
| `d4c_step9_evidence.py` | banks the listings below |
| `d4c_step10_override.py` | override scan — all 13 `.arz` archives, both pulls, 172,255 records |
| `evidence/F1…F14*.asm` | the fourteen listings this lap adds, re-checkable without capstone |
| `evidence/DIGESTS.txt` | source digests |

`d4c_step8_verify.py` prints **PASS on every check.**

```
Game.dll (v1.2.3.4)        4876d6bdb69cca71cfa987652cbd7a42cf6d5578564d02d09aaf9b55c078ab02   ← matches D-4b
database.arz (v1.2.3.4)    8cdeff128422c765278087b7e4f95a41b59be8ee51184370d139c451afb5ae3f
templates.arc (v1.2.3.4)   d6d381a544172abbae1cc2846810e53dc6bdd396b3845af470cb9c859dd13e72   ← matches D-4b
database.arz (ed-III)      2ad6d379285cfb745462316949e8d59e9450cb58a13f9ffa2fdeb70193183bfd   ← matches D-4b
templates.arc (ed-III)     679db83f019020ef7d4d27be8e61203006ee94e5c582dd8a59642f3fddd54602   ← matches D-4b
```

`E1`–`E9` citations refer to D-4b's banked listings; `F1`–`F14` to this lap's.

---

## 10 — CONSEQUENCE FOR FACET (i)

**The model-pack row ships DECODED. The Matt fork (a)/(b) does NOT fire.** Facet (i) was carried as
UNMEASURED-FROM-VIDEO with two live options — commission a controlled capture, or ship
declared-absent. Neither is now needed: the stacking function is read from the engine binary with
per-claim citations, the four D-4b questions are closed, the cap question is a decided negative with
its search record, and the rule is consistent with every quantity D-4 measured from video (§ 8),
exactly agreeing on the only one both instruments speak to (the 100 ms tick). What ships is § 7's
composed rule plus the correction to D-4's candidate table — including the finding that candidate (d)
is a *disabled first-class hook* rather than an absent mechanism, which is the most transferable
result in the lap. Two residuals travel with the row and must not be dropped: the semantic
**provenance** of the `DurationDamageSource` dwords (§ 2 — structure and keying rule decoded, naming
not established) and the still-open **display-layer** question, which § 8 widens with the `+0x08`
max-aggregated stat channel. Neither touches the rule; both bound how it may be cited.

---

## 11 — SELF-CRITIQUE

- **The strongest claim in this lap rests on a one-element array**, so a single override anywhere
  would silently turn "additive stacking" into "diminishing per ordinal" with no code change. I
  raised this against myself and then closed it: all 13 archives in both pulls were scanned
  (§ 4) — **zero overrides**. What I have *not* established is behaviour under third-party mods
  outside the vendor tree, which by construction I cannot see. The statement is therefore
  "**as shipped, including all first-party expansions**", not "always".
- **D-4b's incidental lead was right for a reason it did not know.** It read the `maxss` as the
  cross-application refresh rule. It is not — it operates on a per-attack scratch copy (§ 3). The
  conclusion survives only because the scratch is seeded from the live timeline. Had the seeding gone
  the other way, D-4b's naive reading would have been wrong, and nothing in its evidence would have
  revealed that. **The lesson is the one D-4b itself flagged: three instructions are a lead, not a
  finding.** This lap exists because that flag was honoured.
- **I did not name the `DurationDamageSource` dwords** (§ 2) and I have declined to guess. A reader
  wanting "same source" in human terms — same caster? same skill? same item affix? — does not get it
  from me. The rule is exact; the English gloss is not established.
- **`nTicks` truncates.** `cvttss2si` rounds toward zero, so a 3.35 s duration yields 33 buckets =
  3.3 s. Small, but it is a real sub-tick loss the model should carry rather than assume rounding.
- **Nothing was validated against a running game.** Static decode only; no Wine, no live process.
  The only cross-instrument check available is § 8's, and the only quantity both instruments measure
  independently — the 100 ms tick — agrees exactly.
- **The sort's comparator is inlined and I read it from the insertion-sort path only.** I did not
  separately confirm the partition path at `0x20eb90` uses the same predicate; it visibly compares
  the same `+0x00` offset (`0x0020ebe0`–`0x0020ec40`) but I did not prove the two agree on tie
  handling. With `N=1` this is numerically irrelevant, which is precisely why I am flagging it: it
  would matter the moment `damageMagnitude` had more than one entry.

---

*Lap D-4c closed 2026-08-24 by legolas. **Lap I § 5.3's "UNDECODABLE-FROM-SUBSTRATE" declaration is
RETIRED** — the stacking function is decoded. D-4b § 5 Q1 (partial, structure+rule decoded, provenance
named-open) · Q2 **CLOSED** · Q3 **CLOSED** · Q4 **CLOSED**. Cap/limit fields: **decided NEGATIVE**
with search record. D-4 candidate table corrected: (c) confirmed, (b) falsified-as-global but correct
as the same-source sub-rule, (a) coincides with (c) in shipped data, (d) present-but-disabled.
READ-ONLY on all substrate; writes confined to this directory.*
