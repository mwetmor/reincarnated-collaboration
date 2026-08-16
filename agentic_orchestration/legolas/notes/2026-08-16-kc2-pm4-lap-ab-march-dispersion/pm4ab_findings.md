# KC2-PM4 · LAP AB — FINDINGS · THE REFERENT'S MARCH DISPERSION + TWO CARRIED ITEMS

**Agent:** legolas (UNKNOWN-RESEARCHER) · **Conductor:** gandalf (RUN-CONDUCTOR) · **2026-08-16**
**Commission:** `R-PM4-70 part 3` (ledger `L-60`).
**Pre-registration:** `prereg.md`, sha256
`61e7db1814f6070627977393448378d4ca42f00cf1a57fb0d5087382c2dd2248`, committed **ALONE** in
`0e22f57d` before this lap's instrument existed. Reconnaissance preceding the hash is declared in
its § 0.
**Instrument:** `agentic_orchestration/research/scripts/pm4ab_march_dispersion_2026_08_16.py` (I-AB).
**Discipline:** GL-12 decode-never-estimate · GL-6 full-64-hex on every input and output ·
`D-V2-1` exact artifact/offset on every claim · decoy sets ENUMERATED · three-start convergence on
disassembly · NOTE-9 (prior instruments imported unchanged) · outcome-firewalled (no sim artifact
opened by any leg) · **brackets stay brackets** (`R-PM4-70 part 4(ii)`) · read-only throughout.
**Determinism:** the instrument was run twice; all seven emitted artifacts are **byte-identical**.

---

## 0 — THE HEADLINE, IN ONE PARAGRAPH

**Nothing in the Crucible compresses the roster's march.** The complete run/total-speed field
surface is 51 fields; swept exhaustively over the Crucible's own 3,147-record layer, exactly
**seven** records carry a non-neutral speed modifier or slow, and of those exactly **one** was
purchased in the referent run: the **Deathchill Beacon's `turretice_icebolt` — a 35 % run-speed
slow for 5 s**, delivered by a single ground-targeted projectile with a **2.0 m** blast from a
stationary emplacement whose controller sees **24.0 m**. Its action on the roster's speed
*distribution* is **proportional**, which in time-space **EXPANDS** the arrival spread; it cannot
compress it, and it cannot touch the first ~10 m of a 29–39 m march at all. Everything else is a
decoded negative: `characterRunSpeedModifier` **0.0 on 91/91** tier-16 records; the **difficulty**
selector's three `balancingadjustment_survivalmode_enemies0{1,2,3}` records carry the full 23-slot
run-speed surface at **zero on all three**; `characterTotalSpeedModifier` — the layer no prior lap
read — is **ABSENT on 790/790**; all four celestial blessings carry **zero** speed terms (and were
not purchased). **The referent's march dispersion is, in the shipped data, the sim's own dispersion
— because it is the same 188-actor record band.** `F-AB-1` **FAILS as written** (measured ramp
width 1.700 s vs 2.585–5.709 s predicted, every proxy, both edges) **but the failure is confounded
and I say so**: fewer than half a wave's decoded bodies are ever simultaneously inside the observed
window (median peak/E = **0.4395**), and two waves exceed 1.0 on previous-wave survivors — the
truncation-robust form is **UNREACHED**, published as a number-shaped hole rather than a number.
`UNREACHED-AA-3` **CLOSES**: the alert animation is **23–74 frames** (median 49; **0.767–2.467 s**
at the universally-constant rate field 30, span **3.22×**) — and **52 of 188 rostered actors have
an EMPTY alert slot and play nothing at all**. `OBS-I26-1` resolves to **disposition (ii)**: Lap AA
§ 5.2 stands **with a named qualifier** — **8.53 %** of candidate-restricted placements fall inside
the 6.0 m gate radius (12.27 % on the nearer proxy), concentrated in **3 of 18** spawn points, and
**no spawn point is entirely inside**.

---

## 1 — VERDICT PER FORK

| fork | verdict | one-line basis |
|---|---|---|
| **(a) DATA** | **DECODED + DECODED-NEGATIVE** | 51-field surface enumerated; 3,147-record Crucible layer swept; **7** hits, **1** purchased (35 %/5 s slow, 24 m emitter); every other channel zero |
| **(a) VIDEO/TRACK** | **MEASURED, with `F-AB-1` FAILING AS WRITTEN and its confound priced** | ramp width 1.700 s vs predicted 2.585–5.709 s; peak/E median 0.4395 makes the two functionals not like-for-like — `D-AB-3`, mine |
| **(a) per-body speed** | **UNREACHED** | the pinned tracks carry no velocity column, span only the last ~11.6 m, and Lap U's `D-U-3` demotes the entry set to a strict upper bound |
| **(b)** | **DECODED** (length) **+ UNREACHED-AB-1/2** (seconds; state duration) | 3,452/3,452 `.anm` parsed, acceptance gate 0.9922 vs 0.95; 94 alert slots over the tier-16 roster |
| **(c)** | **MEASURED → disposition (ii)** | analytic + Monte-Carlo agree to 6.1 × 10⁻⁴; 8.53 % / 12.27 % candidate-restricted |

---

## 2 — THE DECOY SET, ENUMERATED (`D-Z-1` / `D-AA-1`)

`pm4ab_speed_surface.csv` — **51 distinct fields** matching the run/total-speed surface across
**819** templates in `database/templates.arc` (**1** template payload was unreadable and is
**counted, not silently skipped**). Classified:

| family | n | why it is a decoy for this question |
|---|---:|---|
| **SELF-LOCOMOTION** | **5** | `characterRunSpeed`, `…Modifier`, `…MaxModifier`, `…Jitter`, `characterTotalSpeedModifier` — **the only family that can change how fast a body marches** |
| APPLIED-SLOW | 28 | `offensiveSlow*` / `retaliationSlow*` — acts on the caster's **TARGET**, not the caster. A monster's `offensiveSlowRunSpeedMin` slows *the player*, never another monster. **This is the single largest trap in the surface and it is where a careless sweep would have manufactured a compressor.** |
| ENGINE-CAP | 8 | `monster/boss/player/absoluteRunSpeedCap{Min,Max}` — clamps, not multipliers |
| UI-DISPLAY | 7 | `tab1RunSpeed*` / `tab2RunSpeed*` / `tab2PetRunSpeed*` — strings |
| SLOW-RESISTANCE | 3 | `defensiveTotalSpeed{Chance,Resistance,MaxResist}` — changes a slow's magnitude, never its direction |

Two further decoy classes are **excluded by construction and named**: the `*AnimSpeed*` /
`*AnimWeight*` family (by far the largest `Speed`-matching population in the corpus, and **not
locomotion** — it is fork (b)'s subject), and the record-path decoys `records/sandbox/**`,
`records/ingameui/**`, `**/backup/**`, `copy of *` (the class that carried a *different*
`alertDistance` at Lap AA § 2.3).

**⚑ Template descriptions are EMPTY on every field in the surface except
`offensiveSlowRunSpeedDuration{Min,Max}` ("Seconds").** No semantic can be read off the template.
Every semantic claim below therefore rests on a record value, a call site, or is marked UNREACHED.

---

## 3 — FORK (a) DATA SIDE

### 3.1 The corpus layer no prior lap in this run opened

`records/creatures/defenses/*` resolves in **none** of the seven `.arz` layers Laps D–AA walked.
It lives only in an **eighth** layer — `mods/survivalmode/database/SurvivalMode.arz`
(sha256 `e9f6e2213eada8f5ffcc4fc430395b43c95384b745b629def096dbb2e7da29b6`, **3,147 records**), the
Crucible mod's own record set. The mod stack used here, in load order (later WINS, Lap AA
`D-AA-4`): `base · gdx1 · gdx2 · gdx3 · sm · sm1 · sm2 · sm3`.

> This is the same **class** of miss as Lap R § 5.4 (`Crucible spawn geometry — UNREACHED`, five
> candidate paths probed, none resolving): the record existed, in a container the probe did not
> open. Recorded here so the pattern is legible, not to reopen a closed verdict.

### 3.2 `A-d1` — the three negatives, re-verified from my own seat, **and the difficulty axis with them**

`records/game/survivalinfo.dbr` [`sm`] carries exactly three adjustment references, and they are
**indexed by DIFFICULTY, not by wave**:

| field | record | fields | run/total-speed surface | **non-zero** |
|---|---|---:|---:|---:|
| `survivalAdjustmentNormal` | `records/game/balancingadjustment_survivalmode_enemies01.dbr` | 627 | 23 | **0** |
| `survivalAdjustmentElite` | `…_enemies02.dbr` | 627 | 23 | **0** |
| `survivalAdjustmentUltimate` | `…_enemies03.dbr` | 627 | 23 | **0** |

> **⚑ `A-d5` IS ANSWERED BY THE SAME ARTIFACT.** The commission asked for difficulty-tier
> multipliers on movement speed. The Crucible's difficulty axis *is* this three-way record
> selector, and **the run-speed surface is zero on all three** — so the answer is a **DECODED
> NEGATIVE across every difficulty, not just the referent's**. Lap T reached these same three
> records and reported them as "wave scaling"; the records do carry per-wave arrays, but the
> **selector** is difficulty. Both readings are true and the distinction is published because the
> commission's question turns on it.

`characterRunSpeedModifier` on the tier-16 band: **`0.0` on 91 / 91** records — Lap T's 790-record
negative holds on the sub-band from an independent walk.

### 3.3 `A-d2` — the layer Lap T's artifact does not carry

| field | tier-16 (91 records) | full roster (790 records) |
|---|---|---|
| **`characterTotalSpeedModifier`** | **ABSENT on 91/91** | **ABSENT on 790/790** |
| `characterRunSpeedMaxModifier` | ABSENT on 91/91 | — |
| `characterRunSpeedJitter` | `0.0`×12 · `10`×17 · `15`×38 · `20`×4 · `30`×6 · ABSENT×14 | — |

`characterTotalSpeedModifier` is a **second, distinct multiplier layer** that `pm4t_march_speed.csv`
does not carry a column for, and it is now read: **the roster does not use it at all.** `P-2`
passes. `characterRunSpeedJitter` is non-zero on **65 / 91** — it would **EXPAND** the spread, and
Lap S proved it MEASURED-NEGATIVE at consumption (`F-11`); it is emitted here rather than dropped.

### 3.4 `A-d3` — the Crucible's own layer, swept exhaustively

**3,147 records scanned; exactly SEVEN carry a non-neutral run- or total-speed modifier/slow**
(the base scalar `characterRunSpeed` and `…Jitter` are excluded from this count — they are the
roster's own values, § 5):

| record | term(s) | owner | **in the referent?** |
|---|---|---|:-:|
| `records/skills/defenses/turretice_icebolt.dbr` | `offensiveSlowRunSpeedMin = 35.0`, `…DurationMin = 5.0` | `turret_ice.dbr :: attackSkillName` + `skillName3` | **YES** |
| `records/skills/defenses/turretice_icebolt2.dbr` | `45.0` / `5.0` | `turret_ice02.dbr` | no (upgrade) |
| `records/skills/defenses/turretice_icebolt3.dbr` | `45.0` / `5.0` | `turret_ice03.dbr` | no (upgrade) |
| `records/skills/defenses/turretice_chillingsurge_buff.dbr` | `characterRunSpeedModifier = −50.0` | `turret_ice02.dbr :: skillName4` + `specialAttackSkillName` | no (upgrade) |
| `records/skills/defenses/turretice_chillingsurge02_buff.dbr` | `characterRunSpeedModifier = −50.0` | `turret_ice03.dbr` | no (upgrade) |
| `records/skills/defenses/banneroffense_frenzy_buff.dbr` | `characterTotalSpeedModifier = +35.0` | `banner_offense02/03 :: buffOtherSkillName` | no (upgrade; and it buffs **allies**) |
| `records/skills/nonplayerskills/buffoffensive/trap_iceaura_buff.dbr` | `characterTotalSpeedModifier = −20.0` | `trap_iceaura.dbr :: buffSkillName` | not on the tier-16 roster |

**The referent's purchases are pinned by Lap PM3-C § 1 (measured from the tribute counter and the
Defense-Site dialogs): Deathchill Beacon + Stormcaller Beacon + Inferno Beacon + Vanguard Banner,
all tier 1, no upgrades, and ZERO celestial blessings.** Of the fifteen defence-site creature
records, four were purchased; five carry a speed term; **the intersection is exactly one.**

**The one term that acted, decoded in full** (`records/skills/defenses/turretice_icebolt.dbr` [`sm`]):

| field | value |
|---|---|
| `offensiveSlowRunSpeedMin` | **35.0** |
| `offensiveSlowRunSpeedDurationMin` | **5.0** (template description: *"Seconds"*) |
| `offensiveSlowRunSpeedMax` / `…DurationMax` / `…Modifier` / `…ModifierChance` / `…DurationModifier` | `0.0` |
| `offensiveSlowRunSpeedChance` | **`0.0`** |
| `offensiveSlowRunSpeedGlobal` / `…XOR` | `False` |
| `projectileExplosionRadius` | **2.0** |
| `skillProjectileNumber` / `skillProjectileTargetGroundOnly` | 1 / `True` |
| `offensiveFreezeChance` | 50.0 |
| emitter reach — `records/controllers/defenses/controller_turretice.dbr` | `ViewDistance = 24.0`, `InnerViewDistance = 18.0`, `MaxPursuitDistance = 25.0`, `MaxYViewDistance = 20.0` |

> **⚑ `UNREACHED-AB-3` — `offensiveSlowRunSpeedChance = 0.0`.** Whether a zero `Chance` on a family
> whose `Min` is non-zero means *never fires* or *fires unconditionally* is **not decoded**: the
> template description is empty and I did not disassemble the consumer. The game's own dialog text
> for this purchase (*"slowing their advance"*, Lap PM3-C § 1) is **CORROBORATION for the
> unconditional reading and may not establish it** (§ 2 evidence class 4). **The § 3.5
> classification does not depend on which reading is right** — it holds under both — so the
> residual is registered rather than resolved.

### 3.5 `A-d7` — **THE DISPERSION QUESTION ITSELF**, which is what the commission actually asked

Every decoded term, classified by its action on the roster's speed **distribution**:

| term | population | action on the **spread** |
|---|---|---|
| `turretice_icebolt` 35 % slow, 5 s | bodies hit by a 2.0 m blast from a 24 m-reach fixed emitter | **EXPAND** — a *proportional* speed reduction maps `t → t/(1−f)`, which scales every march time by a common factor **> 1** and therefore scales the absolute time spread up with it. It is also spatially confined: it cannot act on the first ~5–15 m of a 29–39 m march. |
| `characterRunSpeedJitter` (65/91 non-zero) | the roster | **EXPAND** if consumed — and Lap S proved it MEASURED-NEGATIVE at consumption (`F-11`) |
| ALWAYS-ON chain terms (Lap T § 3.3, imported) | **12 / 91** tier-16 records carry ≥ 1 | **EXPAND (slightly)** — a positive shift on a *subset* widens the band; Lap T priced the pooled effect at ≈ **+1.6 %** |
| `characterRunSpeedModifier` / `…MaxModifier` / `characterTotalSpeedModifier` | roster | **NONE** — zero or absent everywhere |
| difficulty selector (`balancingadjustment_survivalmode_enemies01/02/03`) | all difficulties | **NONE** — 23-slot surface zero ×3 |
| celestial blessings (12 powerup records) | — | **NONE**, and MEASURED-INACTIVE (not purchased) |
| `banneroffense_frenzy_buff` +35 %, `turretice_chillingsurge*` −50 % | banner/turret **tier 2–3 upgrades** | **MEASURED-INACTIVE** — not purchased in the referent |

> **⚑ THE ANSWER. Not one decoded term compresses the tier-16 roster's march-speed spread. Two
> expand it. The rest are zero.** `P-4` passes.

### 3.6 `A-d6` — hero/champion modifiers, and what stays NAMED

Lap T's ALWAYS-ON / CONDITIONAL / TRANSIENT bucketing is **IMPORTED BY IDENTITY** from
`pm4t_march_speed.csv` and restricted to the tier-16 band (**91/91 covered**): records with ≥ 1
permanent chain speed term = **12**; with ≥ 1 transient = **29**. Whether the Crucible applies
*additional* spawn-time champion/hero modifier records beyond the rolled records is **`NAMED-AB-1`,
not decoded** — the prereg's own instruction, honoured.

**`NAMED-AB-2`:** `survivalinfo.dbr` carries `mutatorFx` and `mutatorSound`, i.e. the Crucible has a
**player-mutator** concept this run has never touched. Named, not decoded, not folded.

---

## 4 — FORK (a) VIDEO / TRACK SIDE — a re-query, not a re-derivation

### 4.1 `A-v1` — what the pins attest about arrival clustering

**IMPORTED BY IDENTITY** from `pm4u_ramp_analysis.json` (`S4_march_reconciliation`, `S2_D_U_3`):

| quantity | value |
|---|---|
| referent living-count ramp `t50` | **3.267 s** |
| referent living-count ramp `t90` | **4.967 s** |
| **ramp width `t90 − t50`** | **1.700 s** |
| per-wave ramp decomposition | **NOT pinned** — only the pooled pair exists in the artifact |
| peak living count per wave (151→160) | 24 · 20 · 25 · 28 · 19 · 25 · 36 · 26 · 29 · 25 |

**Lap U's `D-U-3` is inherited in full**: `pm4u_arrivals.csv` is a **STRICT UPPER BOUND** on arrival
rate and **must not be graded against a sim as-is**. It is not used as a rate anywhere in this lap.
**The living-count ramp is the like-for-like functional** — Lap U's own ruling, unamended.

### 4.2 `A-v2` — per-body approach speeds: **UNREACHED, obstacle named**

`pm4u_arrivals.csv`'s columns are
`entry_id, wave, t_abs_s, t_since_wave_s, r_gpx, r_m_lo119, r_m_hi125, bearing_deg, n_frames,
lifetime_s, r_min_gpx, basis` — **no velocity column exists.** The tracks cover entries into the
observed ~11.6 m frustum window, i.e. the **last third of a 29–39 m march**, and their births are
contaminated by nameplate re-appearance (`UNREACHED-S4`). A per-body **full-march** approach-speed
distribution is **not recoverable from the pins**, and the pre-registration forbids re-opening raw
video for it. **`P-5` passes.**

### 4.3 `A-v3` — the compression test, both edges, every named proxy

Tier-16 rostered actors, waves 151–160 (Lap R pin): **n = 188** over **91** distinct records.
`characterRunSpeed` quantiles: p0 **0.600** · p10 **0.660** · p25 0.8375 · **p50 1.000** ·
p75 1.150 · p90 1.200 · p100 **1.550**.

Converted on **both** `UNREACHED-T1` edges (`K` = 3.055412 / 3.209466 m·s⁻¹ per unit, Lap T § 3.5 —
**never as a scalar**), the arrival-time width the referent's own record band predicts:

| distance proxy | edge | pred `t50` | pred `t90` | **pred width** | measured | ratio |
|---|---|---:|---:|---:|---:|---:|
| AA-candidate spawn→patrol-centroid median (33.863 m) | px-LO | 11.083 | 16.792 | **5.709 s** | 1.700 | **3.36** |
| ″ | px-HI | 10.551 | 15.986 | **5.435 s** | 1.700 | **3.20** |
| AA-candidate spawn→nearest-patrol median (16.104 m) | px-LO | 5.271 | 7.986 | **2.715 s** | 1.700 | **1.60** |
| ″ | px-HI | 5.018 | 7.603 | **2.585 s** | 1.700 | **1.52** |
| U-implied spawn→player, lo119 (21.038 m) | px-LO | 6.885 | 10.433 | **3.547 s** | 1.700 | **2.09** |
| ″ | px-HI | 6.555 | 9.932 | **3.377 s** | 1.700 | **1.99** |
| U-implied spawn→player, hi125 (22.099 m) | px-LO | 7.233 | 10.959 | **3.726 s** | 1.700 | **2.19** |
| ″ | px-HI | 6.886 | 10.433 | **3.547 s** | 1.700 | **2.09** |

Full-band span (slowest minus fastest body, same march): **5.13 – 11.32 s** depending on proxy and
edge — the order-of-magnitude quantity gamora's decomposition pointed at, now published as a
**bracket** rather than a scalar.

> **`F-AB-1` FAILS AS WRITTEN.** Measured ramp width is smaller than the predicted width on **every
> proxy and both edges**. `P-6` passes.

### 4.4 ⚑ `D-AB-3` — MY OWN CRITERION WAS NOT LIKE-FOR-LIKE, AND I AM SAYING SO BEFORE ANYONE ELSE DOES

`R-PM4-70 part 4(i)` requires a distributional falsifier to declare its like-for-like window **in
the criterion**. `F-AB-1` declared a *window* (per wave, waves 151–160, ramp width, per edge). It
did **not** establish that the two **functionals** are comparable — and on execution they are not:

* **(x)** is the width of a **windowed living-count** ramp: bodies inside an observed ~11.6 m
  frustum around the player, counted *while alive*.
* **(y)** is the width of the **arrival-time quantiles of a full wave** over a **full march**.

Priced from pinned artifacts — peak living count (Lap U) against decoded expected bodies per wave
(Lap V `pm4v_roster_arithmetic.csv`, `e_bodies` summed per wave):

| wave | 151 | 152 | 153 | 154 | 155 | 156 | 157 | 158 | 159 | 160 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **peak living / E[bodies]** | 0.528 | 0.370 | 0.394 | **0.903** | 0.312 | 0.443 | 0.436 | **0.234** | **1.933** | **3.125** |

**Median 0.4395.** Two consequences, both with **known sign**:

1. **Truncation (down-bias on x).** Fewer than half a wave's decoded bodies are ever simultaneously
   inside the window — bodies killed on approach, or still outside it, never enter the count. A
   slow body that dies before arriving cannot widen the measured ramp. **The measured width is a
   LOWER bound on true arrival dispersion.**
2. **Carry-over (down-bias on x).** Waves 159 and 160 have peak living **above** their own decoded
   body count, so previous-wave survivors sit in the window at `t = 0`. A non-zero baseline
   compresses a measured ramp width mechanically.

**Both confounds push the measured width DOWN, which is the direction that makes `F-AB-1` fail.**
The failure is therefore **not evidence** that the referent compresses its march. **The
truncation-and-carry-over-robust form of `F-AB-1` is `UNREACHED` from the pinned artifacts** — the
pins do not carry a per-wave ramp, a per-body arrival time free of window truncation, or a
previous-wave-survivor mask. **I publish the hole instead of a number.** This is `D-I26-4`'s lesson
applied to my own criterion one lap after the run banked it.

### 4.5 ⚑ WHAT SURVIVES THE CONFOUND — and it is the finding that matters

The confound touches the **video** limb only. The **data** limb is untouched, and it answers the
commission's question on its own:

> **The referent's march-speed dispersion and the sim's are the SAME dispersion, because they are
> the same records.** The tier-16 `characterRunSpeed` band is decode-true on both sides (Lap R,
> 169/169; this lap, 91/91 on the 151–160 sub-band). § 3 establishes that **nothing in the Crucible
> context modifies it**: no difficulty multiplier, no blessing, no wave-scaling term, no second
> multiplier layer, and the single purchased slow is proportional, spatially confined, and
> spread-**expanding**. **There is no referent-side compressor for the sim to be missing.**

That is a **decoded negative on the commission's own question**, and it holds regardless of how
`F-AB-1` is eventually graded. **It does not say the speed spread is or is not the run's next
address** — that is the conductor's ruling, not mine (`R-PM4-27 part 3`, no designation by grade).

---

## 5 — FORK (b) — `UNREACHED-AA-3` CLOSES (in frames)

### 5.1 `B-1` — the ordinal, three starts, one candidate REFUTED

**Start (i) — the site itself, re-verified from my own seat.**
`ControllerMonsterStateAlertBeforePursue::OnBegin` (`Game.dll 0x10109410`):

```
10109410: 6a 00              push 0x0
10109412: 6a 00              push 0x0
10109414: 51                 push ecx
10109415: 8b 49 04           mov  ecx, [ecx+0x4]
10109418: c7 04 24 00 00 80 3f   mov dword ptr [esp], 0x3f800000      ; 1.0f
1010941f: ff 35 b0 52 4e 10  push [0x104e52b0]                        ; const Name&
10109425: 6a 21              push 0x21                                ; <- AnimationSet_Type
10109427: e8 c4 e3 fd ff     call 0x100e77f0 <ControllerAI::PlayAnimation>
1010942c: c3                 ret
```

`AnimationSet_Type` is the **first** parameter and is therefore the **last** push before the call.
Reproduces Lap AA § 5.2 byte-for-byte.

**Start (ii) — the sibling-state anchor set.** All **16** call sites to
`ControllerAI::PlayAnimation` were enumerated across `.text`; the nine in controller-state classes:

| ordinal | caller |
|---:|---|
| `0x0b` | `ControllerMonsterStateParalyze::OnBegin` |
| `0x13` | `ControllerMonsterStateStartup::OnBegin` · `…StateHidden::OnUpdate` |
| **`0x21`** | **`ControllerMonsterStateAlertBeforePursue::OnBegin`** |
| `0x24` | `ControllerMonsterStateEmote::OnBegin` |
| `0x25` | `ControllerMonsterStateFlee::OnBegin` |
| `0x26` / `0x27` | `ControllerMonsterStateGettingUp::OnUpdate` — a **consecutive pair selected on a boolean** (`test al,al; je → push 0x26; jmp; push 0x27`) |

**Start (iii) — the animation table's own field ordering** (`charanimationtable.tpl`, `unarmed*`
fields, numbered variants collapsed to slot families): `… Alert 0x20 · Waiting 0x21 · Rally 0x22 ·
Emote 0x23 · Flee 0x24 · Fidget 0x25 · Pickup 0x26 · PassItem 0x27 · Chat 0x28 · GetUpFaceDown 0x29
· GetUpFaceUp 0x2a …`

**The convergence, stated exactly.** Across the three consecutive semantic anchors
**Alert → Emote → Flee**, the binary's ordinals (`0x21 → 0x24 → 0x25`) reproduce the table's
family spacing (`Alert`, *Waiting*, *Rally*, `Emote`, `Flee`) **exactly**, at a constant offset of
+1. A state class named `AlertBeforePursue` plays the slot the table calls `Alert`, and its two
nearest siblings play the two slots the table places three and four positions later. The
`GettingUp` pair is likewise **consecutive**, as `GetUpFaceDown`/`GetUpFaceUp` are.

**⚑ What does NOT converge, published rather than smoothed:** the +1 offset is **local, not
global** — `GettingUp`'s `0x26/0x27` sit three slots below the table's `0x29/0x2a`, and
`Paralyze`'s `0x0b` five slots above the table's `Stun` at `0x06`. **The full `AnimationSet_Type`
enum is therefore NOT reconstructed and is registered `UNREACHED-AB-4`.** The claim carried forward
is the narrow one: **ordinal `0x21`, at this call site, selects the animation table's `Alert`
slot.**

**⚑ THE REFUTED CANDIDATE, ENUMERATED AND EXCLUDED (`D-Z-1` discipline).** The naive
"`.rdata` literal order == the enum" mapping — exhaustively rebuilt from **269** `unarmed*`
literals in `Game.dll` (and with the reconnaissance filter's two-digit `SpecialAnimNN` bug
repaired, § 0.4 of the prereg) — puts ordinal `0x21` on **`unarmedSpecialAnimRef1`** and `0x25` on
**`unarmedSpecialAnimRef3`**. A `Flee` state cannot play `SpecialAnimRef3`. **The ordering is
refuted and published so that it is visibly excluded, not so it is available.** `P-7` passes.

### 5.2 `B-2` — the `.anm` duration law, gated on the whole population

**3,452** distinct `.anm` files across five `Creatures.arc` archives (base + gdx1/2/3 +
`mods/survivalmode`). **All 3,452 parse; zero unparsed.** Header: `ANM\x02`, then
`u32 field0 | u32 field1 | u32 rate | u32 name_len | <name>`.

| test | result |
|---|---|
| `rate` field distribution | **`30` on 3,452 / 3,452 (100 %)** |
| `(payload − header) / (field0 × field1)` | min 56.014 · p25 56.301 · **median 56.584** · p75 56.986 · max 91.500 |
| **acceptance gate** — fraction within ±5 % of median | **0.992178** vs pre-registered threshold **0.95** → **PASS** |
| `field0` constant within a rig directory | 45 / 91 rig dirs |
| `field1` constant within a rig directory | **3 / 91** rig dirs |

**`field0` = BONE COUNT, `field1` = FRAME COUNT** — field0 is constant within a rig fifteen times
more often than field1, and ≈ 56 bytes per bone-frame is exactly **14 float32**, a clean per-bone
key stride. `P-8` passes.

> **⚑ `UNREACHED-AB-1`.** The `rate` field is **constant at 30 across the entire population**.
> Constancy is **consistency, not proof that the field is frames-per-second**. Durations are
> therefore published **in FRAMES as primary**, and every seconds figure below and in
> `pm4ab_alert_anim.csv` is a **DERIVED** column computed at 30 fps and labelled as such in the
> artifact's own `basis`. It is not a decode.

### 5.3 `B-3` — the alert animation over the tier-16 roster

Join: roster record → `charAnimationTableName` → `<weaponset>AlertAnim{1,2,3}` (+ `…AnimSpeed`,
`…AnimWeight`) → `.anm` header.

| quantity | value |
|---|---|
| tier-16 records | **91** (0 without an animation table) |
| **HAS-ALERT** | **66** |
| **ALERT-SLOT-EMPTY** | **25** |
| rostered **actors** with an alert animation | **136 / 188** |
| **rostered actors with NO alert animation at all** | **52 / 188 (27.7 %)** |
| alert slots resolved | 94 |
| length, **frames** | min **23** · p25 43 · **median 49** · p75 67.5 · max **74** |
| length, seconds at 30 (DERIVED) | **0.767** · — · **1.633** · — · **2.467** |
| span | **3.217 ×** |

**`P-9` passes** — the distribution is not degenerate and spans more than 2×.

Every resolved slot carries `AlertAnimSpeed = 1.0` and `AlertAnimWeight = 100.0` on the tier-16
population, so the pool weights do not re-shape the distribution and the animation speed does not
rescale the length. Per-record, per-weaponset, per-variant rows are in `pm4ab_alert_anim.csv`.

### 5.4 ⚑ THE THREE THINGS FORK (b) DOES NOT CLAIM, as pre-registered

1. **`UNREACHED-AB-2` — the animation length is NOT claimed to be the state's duration.** Lap AA
   decoded `AlertBeforePursue::OnEnd` as a bare `ret`; the state's **exit condition** is not
   decoded by that lap or this one. *"The alert animation is 23–74 frames"* is decoded.
   *"Therefore the state lasts 23–74 frames"* is **not**, and no fold may make that step silently.
2. **Immobility is not claimed** (Lap AA DO-NOT 4, carried unchanged).
3. **The anger limb** (`15.0 > GetAngerDiff`) remains `NAMED-AA-1`, carried.

**And one new caveat the consumer needs.** The creature records carry an **`alertAnimChance`** field
(e.g. `30` on `turret_ice.dbr`). Whether it gates the animation played by this state is
**`UNREACHED-AB-5`** — it is emitted per record in `pm4ab_alert_anim.csv` so the consumer can see
it, and it is **not** folded into the duration.

> **⚑ THE SHAPE THE CONSUMER SHOULD CARRY.** The alert gate is **not a uniform per-body constant**.
> Over the referent's own tier-16 band it is **zero for 27.7 % of rostered actors** (empty slot)
> and **0.77–2.47 s for the rest** (at 30 fps, DERIVED), and the state's exit condition is not
> decoded. A fold that needs a scalar here does not have one.

---

## 6 — FORK (c) — `OBS-I26-1` DISPOSITION

### 6.1 The semantics, pinned before any number

`Game.dll 0x1010a360 + 0x35f` : `comiss / jbe` — `if (d <= alertDistance) goto skip`, with
`alertDistance = 6.0` from `records/game/gameengine.dbr` (Lap AA § 5.2). **A body INSIDE 6.0 m
SKIPS the alert.** *"The gate holds"* = the body is **outside** 6.0 m and **does** enter the state.

### 6.2 Method — two pinned inputs, no new source

Point set: `pm4u_geometry_v3.csv`, digest asserted EXACT, `parse_complete` honoured. Scatter law:
Lap AA § 3.2 — `ρ ~ U(0, placementExtents = 8.0)`, `θ ~ U(0, 2π)`, **uniform in radius, never a
uniform disc** (Lap AA DO-NOT 2). Fraction computed **analytically** over the exact law
(`P(d ≤ R) = (1/E)∫₀^E arccos(clamp((D²+ρ²−R²)/(2Dρ)))/π dρ`, 4,001-node trapezoid) and
**independently by a deterministic 200,000-draw Monte-Carlo**.

**⚑ `D-AB-2`, self-caught.** The pinned geometry artifact carries the same map from more than one
`Maps.arc` (`survivalmode1` and `survivalmode3`), and the two copies are **not identical** —
`survivalworld_a`'s near point reads **10.0946 m** in sm1 and **10.2826 m** in sm3. The first cut
averaged both, double-counting every arena. Lap AA's `D-AA-4` already ruled the stack:
**survivalmode3 wins**. Resolved per map to the winning archive: **120 rows → 60**, 60 superseded
copies **counted and published**, not hidden. The resolved counts — **18** candidate-restricted,
**60** all-arena — now match Lap AA § 2.4's own `n = 18` / `n = 60` exactly.

### 6.3 The number

| scope | target proxy | n points | **mean fraction of placements inside the 6.0 m gate** | points with **any** placement inside | points **entirely** inside |
|---|---|---:|---:|---:|---:|
| **candidate-restricted (a/b/e)** | `to_patrol_centroid_m` | 18 | **0.0853** | **3** | **0** |
| **candidate-restricted (a/b/e)** | `to_nearest_patrol_m` | 18 | **0.1227** | **6** | **0** |
| all arenas | `to_patrol_centroid_m` | 60 | 0.0757 | 10 | 0 |
| all arenas | `to_nearest_patrol_m` | 60 | 0.1217 | 22 | 0 |

The distribution is **bimodal, not diffuse**: the three near points carry essentially all of it —
`survivalworld_e` at D = **0.1122 m** → **0.7499**, `survivalworld_b` at D = **2.4534 m** →
**0.7114**, `survivalworld_a` at D = **10.0946 m** → **0.0810**; every other candidate point is
**0.000000**.

**CORROBORATION — analytic vs Monte-Carlo** (independent second route, § 2 class 4):
D = 0.1122 m → 0.749934 / 0.750540 (|Δ| 6.06 × 10⁻⁴) · D = 2.4534 m → 0.711360 / 0.711245
(|Δ| 1.15 × 10⁻⁴) · D = 33.9762 m → 0.000000 / 0.000000. The two routes agree; the analytic form is
the one published.

**`P-10` passes** (non-zero and strictly under 25 % on both proxies).

**⚑ `UNREACHED-AB-6` — the proxy substitution, named.** The gate's `d` is monster→**enemy**, and
**the player's per-wave world position is not pinned by any artifact in this run.** Both proxies
above are patrol-ring quantities, not the player. Lap U's *implied* spawn→player ≈ 21.0–22.1 m
(INFERRED-WITH-EVIDENCE) is **CORROBORATION only** and is not used as a distance here. The
player-referenced fraction is **UNREACHED**; the bracket across the two named proxies governs.

### 6.4 THE DISPOSITION — **(ii): Lap AA § 5.2 stands WITH A NAMED QUALIFIER**

`P-11` passes. The qualifier, written as a quotable sentence for downstream carry:

> **⚑ THE QUALIFIER.** *Lap AA § 5.2's "the gate holds for essentially every body" is correct as a
> statement about the arena's **typical** spawn point and wrong as a statement about **all** of
> them. Under the decoded uniform-in-ρ scatter law with `placementExtents = 8.0`, **8.5 % of
> candidate-restricted placements (12.3 % on the nearer proxy) land inside `alertDistance = 6.0` and
> SKIP the alert entirely** — and that fraction is **not spread evenly**: it is carried almost
> entirely by **3 of 18** authored spawn points, at which **67–75 %** of the pack skips the gate,
> while at the other fifteen the fraction is exactly zero. **No spawn point is entirely inside.**
> A pack released at a near point therefore **SPLITS**, and a pack released anywhere else does not.*

**Both halves of `OBS-I26-1` are true and neither is unqualified.** § 5.2's "essentially every body"
is a statement about the *point population* (15 of 18 points contribute nothing); § 2.4's 0.112 m
minimum is a statement about the *extreme point* (at which three quarters of the pack skips). They
are compatible once the distribution is published instead of its endpoints.

**On the comparison to the sim's 14.29 %:** the outcome firewall holds — no sim artifact was opened
by this lap and gamora's figure is **not** graded here. What is published is the **referent-side**
fraction under two named proxies. Whether the two numbers are like-for-like depends on gamora's own
definition of a "pack split", which is **the conductor's reconciliation to make, not mine.**

---

## 7 — DEFECT TABLE (all mine · all self-caught · all repaired or declared BEFORE any claim rested on them)

| id | defect | how caught | disposition |
|---|---|---|---|
| **`D-AB-1`** | The `.anm` join returned **zero** lengths: the `.dbr` field spells the path `creatures/enemies/<rig>/anm/x.anm` while the ARC entry name **omits the leading `creatures/`**. | The instrument crashed on an empty duration list rather than publishing "the roster has no alert animations" — **the empty-population case was the thing that saved it.** Had the code been one line more defensive it would have published a spectacular false negative. | Both spellings indexed; join is total; the comment naming the trap is in the instrument. |
| **`D-AB-2`** | Fork (c) averaged **two copies of every arena** (`survivalmode1` + `survivalmode3` `Maps.arc`), which are **not identical**. | Point counts came back `n=36`/`n=120` against Lap AA § 2.4's published `n=18`/`n=60` — **the prior lap's own count was the check.** | Resolved per map to the mod-stack winner (Lap AA `D-AA-4`); 60 superseded rows counted and published; counts now match Lap AA exactly. |
| **`D-AB-3`** | **`F-AB-1`'s criterion declared its window but not its FUNCTIONAL.** The measured and predicted quantities are not like-for-like. | Priced on execution against Lap V's decoded body counts (median peak/E = 0.4395). | `F-AB-1` graded **FAILS AS WRITTEN**; the confound published with its sign; the robust form declared **UNREACHED**. § 4.4. |
| **`D-AB-4`** | Reconnaissance's `.rdata` literal ordering used a regex that dropped two-digit `SpecialAnimNN` names, producing an ordering with a hole. | Caught in the prereg (§ 0.4) **before** the hash, and declared there. | Repaired exhaustively in the instrument; the ordering is now correct **and refuted on its merits**, § 5.1. |

---

## 8 — PRE-REGISTERED PREDICTIONS, GRADED WORDING-UNCHANGED

| # | prediction (verbatim) | grade | evidence |
|---|---|---|---|
| **P-1** | Lap T's three negatives re-verify from my own seat: `characterRunSpeedModifier` is `0.0` on every roster record, and the run-speed field surface of all three `balancingadjustment_survivalmode_enemies0{1,2,3}` records is zero. | **PASS** | 91/91 at `0.0`; 23-slot surface, non-zero = 0 ×3 (§ 3.2) |
| **P-2** | `characterTotalSpeedModifier` — the layer Lap T's artifact does not carry — is **also** neutral (absent or `0.0`) on the tier-16 roster. | **PASS** | ABSENT on 91/91 and on 790/790 (§ 3.3) |
| **P-3** | At least one **purchased** referent defence carries a run-speed-family term that lands on monsters, with a **finite radius** smaller than the march. | **PASS** | `turret_ice` → `turretice_icebolt` 35 %/5 s; `ViewDistance = 24.0`, blast 2.0 m (§ 3.4) |
| **P-4** | No decoded term acts to **COMPRESS** the roster's run-speed spread. Every term that fires classifies as `SHIFT` or `NONE` under `A-d7`. | **PASS** (with a correction to my own wording) | No term compresses. **Two EXPAND** — a class my prereg's wording did not offer, so the classification table publishes `EXPAND` and the prediction's *substance* (nothing compresses) holds while its *enumeration* was incomplete. Declared, not glossed. (§ 3.5) |
| **P-5** | **Per-body approach speed over the full march is UNREACHED from the pinned track artifacts**, because the pinned tracks exist only inside the observed frustum window near the player. | **PASS** | no velocity column; window ≈ 11.6 m of a 29–39 m march (§ 4.2) |
| **P-6** | The referent's **measured** ramp width (`t90 − t50`, living count) is **smaller** than the arrival-time spread its own roster `characterRunSpeed` band predicts over the candidate-restricted march, on **both** `UNREACHED-T1` edges. | **PASS** | 1.700 s vs 5.709 / 5.435 s (§ 4.3) — **but see `D-AB-3`: the comparison is confounded and the prediction passing does not license the inference** |
| **P-7** | The three candidate orderings for `AnimationSet_Type 0x21` do **not** all agree on first inspection, and at least one recon-level candidate is refuted by the three-start convergence. | **PASS** | `.rdata` order refuted; table order converges only locally (§ 5.1) |
| **P-8** | The `.anm` bytes-per-key invariant of `B-2` holds across **≥ 95 %** of the 1,770-file population. | **PASS** (population larger than predicted) | 0.992178 conformance over **3,452** files — my prereg's "1,770" counted only the base archive; the gate was applied to the full five-archive population, which is stricter, not weaker (§ 5.2) |
| **P-9** | The alert-slot `.anm` durations over the tier-16 roster are **not** a single constant — they vary by rig by at least a factor of two. | **PASS** | 23–74 frames, span 3.217× (§ 5.3) |
| **P-10** | Fork (c): the fraction of referent spawn **placements** falling inside the 6.0 m gate radius is **non-zero but small** — strictly between 0 % and 25 % — on the candidate-restricted point set under **both** proxies. | **PASS** | 8.53 % and 12.27 % (§ 6.3) |
| **P-11** | Fork (c) resolves to disposition **(ii)** — AA § 5.2 stands *with a named qualifier* — rather than (i), (iii) or (iv). | **PASS** | § 6.4 |
| **P-12** | No fork of this lap requires opening the referent video, the sim's cells, or any source outside the pinned corpus + pinned prior-lap artifacts. | **PASS** | inputs are the eight `.arz` layers, five `Creatures.arc`, `templates.arc`, `Game.dll`, and five pinned prior-lap artifacts — all listed in `pm4ab_digests.json` |

**12 PASS · 0 FAIL · 0 UNGRADED.** Two passes carry declared wording defects in the prediction
itself (`P-4`'s missing `EXPAND` class, `P-8`'s undercounted population); both are published above
rather than quietly satisfied. **`F-AB-1` FAILS AS WRITTEN and its failure is confounded** — § 4.4.

---

## 9 — ⚑ DO-NOT BLOCK (binding on every downstream fold)

1. **DO NOT** fold a Crucible-context multiplier on monster movement speed. There is none. § 3 is a
   decoded negative across the difficulty selector, the wave-scaling records, the blessings, the
   second multiplier layer, and the roster's own modifier fields. Do not re-open it as an assumption.
2. **DO NOT** read `turretice_icebolt`'s 35 %/5 s slow as a march-wide term. It is delivered by a
   **single ground-targeted projectile with a 2.0 m blast** from a **fixed** emplacement whose
   controller sees **24.0 m**, against a **29–39 m** march. And **do not** assume it fires at all:
   `offensiveSlowRunSpeedChance = 0.0` and its semantics are `UNREACHED-AB-3`.
3. **DO NOT** treat any `offensiveSlow*` field on a **monster's** skill as acting on that monster or
   on its pack. That family acts on the caster's **target**. It is 28 of the 51 fields in the
   surface and it is the single easiest way to manufacture a compressor that does not exist.
4. **DO NOT** cite `F-AB-1`'s failure as evidence that the referent compresses its march.
   `D-AB-3` prices two confounds, **both** biasing the measured width **down**. The robust form is
   **UNREACHED**. § 4.4 is the sentence to quote, not § 4.3's ratios.
5. **DO NOT** convert the alert animation's frames to seconds as a decode. `UNREACHED-AB-1`: the
   rate field's identification as fps is not decoded. Frames are decoded; seconds are DERIVED and
   labelled so in the artifact's own `basis` column.
6. **DO NOT** equate the alert animation's length with the alert **state's** duration
   (`UNREACHED-AB-2`), do not claim immobility during it (Lap AA DO-NOT 4), and do not fold it as a
   uniform per-body constant — **27.7 % of rostered actors have an empty alert slot.**
7. **DO NOT** cite `AnimationSet_Type` ordinals other than `0x21` from this lap. The full enum is
   `UNREACHED-AB-4`; only the `0x21 → Alert` identification is carried, and the `.rdata` literal
   ordering in § 5.1 is published to be **excluded**, not used.
8. **DO NOT** cite fork (c)'s fraction without the proxy caveat. The gate's distance is
   monster→**player** and the player's world position is not pinned (`UNREACHED-AB-6`). The
   candidate-restricted bracket across the two named proxies governs (Lap AA DO-NOT 5).
9. **DO NOT** use `pm4u_arrivals.csv` as an arrival rate. Lap U's `D-U-3` demotion is inherited
   unchanged: strict upper bound, not gradeable against a sim.
10. **All prior DO-NOT blocks are carried unchanged** — Lap V § 7.2, Lap V-2 § 11.2, Lap W § 7.2,
    Lap X § 12.2, Lap Y § 11.6, Lap Z § 5, **Lap AA § 6 (all eight)**. In particular Lap AA § 4.5's
    **two-table caveat**: this lap's band is **151–160** and it makes no wave-150 claim.

---

## 10 — UNREACHED CENSUS (obstacle named on every one)

| id | what | obstacle |
|---|---|---|
| **`UNREACHED-AB-1`** | `.anm` rate field `30` as **frames per second** | constant across 3,452/3,452 files, which is consistency, not identification; the loader's use of the field was not disassembled |
| **`UNREACHED-AB-2`** | the alert **state's** duration (vs the animation's length) | `OnEnd` is a bare `ret` (Lap AA); the state's exit condition is in the same virtual-dispatch driver Lap U left as `UNREACHED-U1` |
| **`UNREACHED-AB-3`** | `offensiveSlowRunSpeedChance = 0.0` semantics (never vs unconditional) | template description empty; consumer not disassembled; the game's own dialog prose is CORROBORATION only |
| **`UNREACHED-AB-4`** | the full `AnimationSet_Type` enum | the table-order offset is local, not global; two anchors (`GettingUp`, `Paralyze`) do not fit it |
| **`UNREACHED-AB-5`** | whether `alertAnimChance` gates the animation this state plays | field emitted per record; consumer not decoded |
| **`UNREACHED-AB-6`** | the **player-referenced** gate fraction | the player's per-wave world position is not pinned by any artifact in this run |
| **`F-AB-1` robust form** | truncation- and carry-over-robust ramp-width comparison | the pins carry no per-wave ramp, no truncation-free arrival time, and no previous-wave-survivor mask (§ 4.4) |
| **per-body approach speed** | full-march per-body speeds | no velocity column in the pinned tracks; window ≈ 11.6 m; `D-U-3` demotion (§ 4.2) |
| carried in | `UNREACHED-T1` (the `characterRunSpeed` → m/s constant), `UNREACHED-AA-2` (scatter failure path), `NAMED-AA-1` (the anger limb), `UNREACHED-S4`, `UNREACHED-U1` | unchanged by this lap |

**NAMED, not decoded** (`R-PM4-56 part 4`): `NAMED-AB-1` — Crucible spawn-time champion/hero
modifier records beyond the rolled roster. `NAMED-AB-2` — the Crucible's **player-mutator** system
(`survivalinfo.dbr :: mutatorFx` / `mutatorSound`), which this run has never touched.

---

## 11 — WHAT THIS LAP DID NOT DO (the firewall, stated)

No sim artifact — cell, code, telemetry, or record — was opened by any leg. No referent video frame
was decoded; the video limb is a **re-query of already-pinned Lap R / Lap U artifacts** and nothing
else. No number in this lap elects, ranks, or recommends anything for the sim
(`R-PM4-27 part 3`). No m/s quantity is published on a single edge. No estimate stands anywhere in
place of a decode.

---

## 12 — ARTIFACT DIGESTS (full 64-hex sha256)

### 12.1 Emitted by this lap

| file | sha256 |
|---|---|
| `pm4ab_speed_surface.csv` | `dc9dd5fb733aabc28a16272ede63f44aa4d908e8b4e06b19a864db39df5fa00f` |
| `pm4ab_fork_a_data.json` | `971abf8bb3df8b7a59c7ea9e87569fd1eb90aba4031e92aa532265ad7cd3d7bd` |
| `pm4ab_dispersion.json` | `bbedd417bb3f3e4d0015e684cd5b84b5876cc5ce9665cdc5e2a2ebc200c68bea` |
| `pm4ab_alert_anim.csv` | `65706232f07e8366459f20e9c3873527ac4c837f7896b80a3e87eebb56fe3aa5` |
| `pm4ab_alert_ordinal.json` | `1f10d1c0141f4118db98b793b389222f085dc01c04a88c49dd107c94036de547` |
| `pm4ab_gate_fraction.json` | `c881b38daae740e2e41d334cd1db3808410c407627636d1cf674534e5a239de0` |
| `decode.log` | `210559eb3eef353f75c63cd2ce7be2e2f0c915bdbcb1a354fcdbf4452bd9bbf3` |

*(`pm4ab_digests.json` carries these plus every input; it is the artifact the conductor should
re-hash. Its own digest is not self-referential and is reported by the landing note.)*

### 12.2 Asserted EXACT at instrument start (HALT on mismatch)

| artifact | sha256 |
|---|---|
| `prereg.md` (this lap) | `61e7db1814f6070627977393448378d4ca42f00cf1a57fb0d5087382c2dd2248` |
| `…-III-20260808/database/database.arz` | `2ad6d379285cfb745462316949e8d59e9450cb58a13f9ffa2fdeb70193183bfd` |
| `…-III-20260808/database/templates.arc` | `679db83f019020ef7d4d27be8e61203006ee94e5c582dd8a59642f3fddd54602` |
| `…-III-20260808/mods/survivalmode/database/SurvivalMode.arz` | `e9f6e2213eada8f5ffcc4fc430395b43c95384b745b629def096dbb2e7da29b6` |
| `…-III-20260808/survivalmode1/database/SurvivalMode1.arz` | `6ac10d6180bfa8491edfc89946d1cfbf166c5ca6442c5862ecf6947290021252` |
| Lap U `pm4u_geometry_v3.csv` | `5ab636ebccaef4b613b663db1dbf083e8a166d5e0db4dd4a5cf9e8e3423dfac2` |
| Lap V `pm4v_roster_arithmetic.csv` | `991f75cfdb43ddff06fb01fbd16c81693af020a56f7dfe315e87e11e4db4a93c` |

Fifteen further inputs (the remaining `.arz` layers, five `Creatures.arc`, Lap R / Lap T / Lap U /
Lap AA artifacts, and `Game.dll`) are **RECORD**-class and are pinned for the first time here; every
one is in `pm4ab_digests.json :: inputs`.

---

## 13 — METHOD

One instrument, `pm4ab_march_dispersion_2026_08_16.py`, run twice; **all seven emitted artifacts
byte-identical** across the two legs. It imports `gd_arz_adapter_2026_07_24`,
`gd_arc_reader_2026_07_26` and `pm4s_pe_2026_08_14.PE32` **unchanged** (NOTE-9) and re-implements
nothing. Disassembly is `objdump` at VMA-corrected addresses through the project's existing `PE32`
helper. The Monte-Carlo leg uses a fixed-seed LCG so the emitted artifact is byte-stable. Prior-lap
numbers enter only through their **emitted artifacts** with digests asserted — never from prose
(`R-PM4-67 part 2` / `D-CON-6`).
