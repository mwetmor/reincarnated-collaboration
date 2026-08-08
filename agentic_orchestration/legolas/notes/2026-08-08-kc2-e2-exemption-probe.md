# KC2-SIM E-2 — `ignoreGameBalance` exemption column + F-8 Soulfire cost re-read

**Agent:** legolas (UNKNOWN-RESEARCHER) · **Date:** 2026-08-08 · **Commissioner:** gandalf RUN-CONDUCTOR,
KC2-SIM autonomous run, Phase C→D boundary · **Mode:** targeted citation micro-probe (E-2 + F-8 rider)
**Corpora (READ-ONLY):** `~/Games/vendor/grim-dawn-edition-II-20260724/` (8 `.arz` archives, 84,663
distinct record paths) · `~/Games/vendor/grim-dawn/database/templates.arc` (819 `.tpl`, template layer
only — Edition-II ships **no** `templates.arc`; that lineage split is declared in § 0.3)
**Scratch:** `agentic_orchestration/legolas/scratch/2026-08-08-kc2-e2-exemption/`
**Commits:** NONE (charter § 4.7 — conductor commits at gate close)

**Provenance vocabulary used throughout:** `DB-CITED` (field present in a `.dbr`, value read) ·
`TPL-CITED` (declared in a `.tpl`, with the template's own words) · `TPL-DEFAULT` (field absent from
the `.dbr`; value is the template's `defaultValue`) · `DEV-DOC` (Crate's published modding guide) ·
`DERIVED` (my arithmetic over cited values) · `NAMED-ABSENT` (I looked; the corpus does not say).

---

## § 0 — Headline

| # | Finding | Grade |
|---|---|---|
| **1** | **Wave 160 p04 is NOT exempt.** Both of its pools omit `ignoreGameBalance` entirely → template default `0`. The modified body count reads **8**, not 7. The spec's ≤7 bound is **missed**, and I am reporting that rather than reconciling it. | **DB-CITED + TPL-DEFAULT** |
| **2** | **Full 632/635 coverage achieved.** Exemption resolved for **every** pool in the P-E6 CSV. 74 exempt. | DB-CITED |
| **3** | **The 74/632-vs-74/635 "divergence" is not a divergence.** Both my prior numbers are right; they count *different populations*. The exempt count is **74 in all three** populations. | DERIVED over DB-CITED |
| **4** | **"ALL exempt pools are boss pools" is FALSE by exactly one.** `poolsbasicgdx3/celestialmonstrosity_t3.dbr` is a genuine 3-of-3 trash pool with `ignoreGameBalance = True`. U-9 § 5.2's *prose* contradicted U-9 § 5.2's own *table*. | DB-CITED |
| **5** | **Zero multi-archive divergence.** 158/635 pools live in >1 archive; all 158 agree on both value and field-presence. Last-writer-wins is not load-bearing for this flag. | DB-CITED |
| **6** | **F-8 DISSOLVES: Soulfire has no cost.** `eyeofreckoning2.dbr` declares **no `skillManaCost`**. The "3–20 rank-scaled" belongs to `playerclass05/aetherray2.dbr` (Disintegration) — the *unique* record in the corpus with that span. The F-8 premise is a cross-record attribution error. | **DB-CITED** |
| **7** | **Family law behind (6):** **474 of 476** `SkillSecondary_*` records corpus-wide omit `skillManaCost`; the only 2 that carry it are Crate's `records/sandbox/jakub/` dev scratch. Zero shipped secondary skill bills separately. | DB-CITED |
| **8** | **Rider hazard (unasked, material):** 117/635 pools have an **empty regular roster**; the non-exempt `+1` to `spawnMin` conjures a body from an empty draw. Worth **27.0 expected bodies** over waves 151–170. Reported, not folded. | DB-CITED value / DERIVED consequence |

---

## § 0.2 — Emission decision, and why

**PRIMARY: a sidecar CSV keyed by pool record path.**
`pe6_pool_ignoregamebalance.csv` — 635 rows, one per distinct `pool_record`.

**CONVENIENCE: a revised pools CSV.**
`pe6_crucible_wave_pools_v2.csv` — the P-E6 emission verbatim (1998 rows, 23 cols) plus three
appended columns, 26 cols total.

I emitted both, and I am naming the sidecar primary for three reasons.

1. **`ignoreGameBalance` is a property of the pool record, not of the (wave, spawn-point, pool)
   triple.** Replicating one value across the 1998 rows that reference 635 records invites exactly
   the drift the sidecar prevents — 193 of the 1998 rows carry `True`, for 74 distinct pools.
2. **gamora's override table is already keyed by pool path.** The sidecar drops in as a replacement
   with no reshaping; the wide CSV would require her to re-derive the key.
3. **It leaves the P-E6 emission immutable.** `pe6_crucible_wave_pools.csv` keeps its SHA and its
   provenance; the v2 is an additive convenience, not a supersession. If the two ever disagree, the
   sidecar wins and the v2 is regenerable from it by join.

```
SHA-256  pe6_pool_ignoregamebalance.csv    40182de26b64cc03e936d9504274e9135f10373979e73eccc224ec732aff77d3
SHA-256  pe6_crucible_wave_pools_v2.csv    bbdc18f12aab8e3788eac229ed1871a88ed7790dc3d1786c509cd26c076e5587
```

Sidecar columns: `pool_record, pool_archive, pool_family, pool_kind, ignore_game_balance,
field_state, raw_value, provenance, spawn_min, spawn_max, champion_chance, champion_min,
champion_max, proxy_pool_equation`.
v2 appended columns: `ignore_game_balance, igb_field_state, igb_provenance`.

**Every row carries its own provenance.** `field_state ∈ {PRESENT, ABSENT}`; `provenance ∈
{DB-CITED, TPL-DEFAULT}`. A consumer that wants only measured values can filter
`provenance == 'DB-CITED'` and see exactly what it is giving up (511 pools / 1714 rows measured;
124 pools / 284 rows template-defaulted).

## § 0.3 — One lineage split, declared

The `.dbr` values come from **Edition-II**. The `.tpl` declarations come from the **live install**
(`~/Games/vendor/grim-dawn/database/templates.arc`), because Edition-II is a data-only depot slice
and ships no `templates.arc` (`find` returns only `Text_EN.arc` files). Every `TPL-CITED` and
`TPL-DEFAULT` claim below therefore rests on a *different artefact* from its `DB-CITED` neighbour.
I did not find this load-bearing — the template layer is versioned with the editor, not the data —
but it is a seam and it should be visible rather than assumed away.

---

# PART I — TASK 1: the exemption column

## § 1 — Coverage

**635 / 635 distinct pool records resolved. Zero `NORECORD`. Zero unresolved.**

| field state | pools | rows (of 1998) | meaning |
|---|---:|---:|---|
| `PRESENT`, value `True` | **74** | 193 | **DB-CITED** — exempt |
| `PRESENT`, value `False` | 437 | 1521 | **DB-CITED** — not exempt |
| `ABSENT` | 124 | 284 | **TPL-DEFAULT** → `0` → not exempt |

**TPL-CITED, `proxypool.tpl`, verbatim:**

```
Variable
{
    name = "ignoreGameBalance"
    class = "variable"
    type = "bool"
    description = ""
    value = ""
    defaultValue = "0"
}
```

Note `description = ""`. The template names the field's **type and default** but not its
**semantics** — that is `NAMED-ABSENT` in the DB layer. The meaning is `DEV-DOC` only, from Crate's
modding guide, already cited at U-9 § 5.2:

> *"**Ignore Game Balance:** True/false check whether to use the difficulty modifiers that increase
> spawn count. This is important for proxies that dispense a single entity, such as Aether Crystals,
> as otherwise several crystals could spawn on top of each other."*

`ignoreGameBalance` appears in **exactly one** template (`proxypool.tpl`). It is absent from
`proxy.tpl`, `proxypoolequation.tpl` and `gameproxies.tpl` — so there is no proxy-level or
equation-level override of it to hunt for. `TPL-CITED`.

### 1.1 The ABSENT reading is not an adapter artefact — four checks

This mattered enough to attack directly, because the whole E-3 answer turns on it. Verification in
`e4_verify.py` / `e4_out.txt`:

- **V1 — does the adapter surface false-valued bools at all?** Over every `records/proxies/pools*`
  record in the resolved namespace: `{'True': 135, 'False': 678}`. It surfaces 678 explicit
  `False`s. `ABSENT` therefore means *the DBR omits the key*, not *the parser dropped a zero*.
- **V2 — verbatim field dump** of both wave-160 p04 records, from every archive that carries them
  (§ 3.2 below). Eleven fields each. No `ignoreGameBalance` among them.
- **V3 — is `ABSENT` correlated with anything suspicious?** It is perfectly correlated with
  *family*, and with nothing else: all 124 `ABSENT` pools are in `poolsboss` (81), `poolsbossgdx1`
  (25), `poolsbossgdx2` (18). Every `poolsbasic*`, `poolshero*`, `poolsdevotion*`, `poolsbounty*`
  and `poolsbossgdx3` pool declares the field. That is an *authoring* signature — Crate's editor
  writes the key once touched — not a parse signature.
- **V4 — index-bound audit.** Highest declared slot index across all 925 Crucible proxies:
  `pool` ≤ 6, `poolEpic` ≤ 6, `poolLegendary` ≤ 6. The P-E6 `s4` loop bound of 1..12 truncates
  nothing; the U-9 `q5` bound of 1..8 truncated nothing either.

### 1.2 The authoring pattern, stated

| family | `PRESENT:False` | `PRESENT:True` | `ABSENT` |
|---|---:|---:|---:|
| `poolsbasic` / gdx1 / gdx2 | 291 | 0 | 0 |
| `poolsbasicgdx3` | 24 | **1** | 0 |
| `poolshero` (all four) | 95 | 0 | 0 |
| `poolsdevotion` + `poolsbounty` (all) | 22 | 0 | 0 |
| `poolsboss` | 0 | 18 | 81 |
| `poolsbossgdx1` | 0 | 13 | 25 |
| `poolsbossgdx2` | **5** | 6 | 18 |
| `poolsbossgdx3` | 0 | **36** | 0 |

Two readable facts. (a) On non-boss families the flag is *always written and always false* — Crate
treats it as boilerplate. (b) On boss families it is written **only when set true**, with one
exception: five `poolsbossgdx2` pools carry an explicit `False`. So "PRESENT ⟺ True" is a *nearly*
exact rule for boss pools and I will not state it as a rule. `DB-CITED`.

## § 2 — Cross-check against the established 74/632 + boss-pool-only facts

### 2.1 74/632 vs 74/635 — RECONCILED, and it was never a contradiction

My own two prior emissions disagreed:
- U-9 § 5.2 (`2026-08-07-u9-spawnmin-operator-order.md`): *"**74 of 632** Crucible pools set it"*
- P-E6 § (`2026-08-07-pe6-crucible-wave-composition.md` L207): *"**74 of 635** Crucible pools"*

Measuring three populations separately (`e1_census.py`) resolves it as a **population difference,
not an arithmetic one**:

| population | definition | n | IGB=1 |
|---|---|---:|---:|
| **POP-A** | pools reachable via base `pool{i}` (the U-9 `q5` sweep) | **632** | **74** |
| **POP-B** | Gladiator view — `poolLegendary{i}` where the point declares any, else `pool{i}` (the P-E6 `s4`/`s8` sweep → the pools CSV) | **635** | **74** |
| **POP-C** | union of `pool` ∪ `poolEpic` ∪ `poolLegendary` | 637 | 74 |

Set relations, verbatim from `e1_out`:

```
|A|=632  |B|=635  |C|=637        A \ C = {}   (A is a subset of C)
B \ A (5): poolsbasic/aetherialhorror_t1, poolsbasic/thornedhorror_t1,
           poolsboss/aetherial_harrath_nozombies, poolsboss/aetherial_reanimator_zanbrandt,
           poolsboss/chthonian_trappedandalone
A \ B (2): poolsbasic/harvestman_t1, poolsbasic/slith_a_t1
```

**Both figures are correct for what they count.** U-9's 632 is the base-difficulty population;
P-E6's 635 is the Gladiator population that actually governs the fixture. **The IGB=1 count is 74
in all three** — the exempt set sits inside A ∩ B ∩ C, so no downstream arithmetic changes on the
choice. `DERIVED over DB-CITED`.

My POP-A family table reproduces U-9 § 5.2's line-for-line once the groupings are unfolded:
`poolsbasic (+gdx1/gdx2)` 291 = 215+45+31 ✓ · `poolshero` all four 95 = 46+18+15+16 ✓ ·
`poolsdevotion`/`poolsbounty` all 22 = 6+3+3+3+3+2+1+1 ✓ · `poolsboss` 96/78/18 ✓ ·
`poolsbossgdx1` 38/25/13 ✓ · `poolsbossgdx2` 29/23/6 ✓ · `poolsbossgdx3` 36/0/36 ✓.

### 2.2 DIVERGENCE REPORTED — "all exempt pools are boss pools" is false by one

The commission's established-fact list, and U-9 § 5.2's own prose, say:

> *"**Every exempt pool is a boss pool.** No trash or hero pool is ever exempt."*
> *"…and they are exclusively boss pools."*

**That claim has a counterexample, and it was visible inside U-9's own table the whole time** — the
`poolsbasicgdx3` row read `25 / 24 / 1`. The prose and the table contradicted each other and the
prose is the one that is wrong.

`DB-CITED`, `records/proxies/poolsbasicgdx3/celestialmonstrosity_t3.dbr` [sm3], verbatim:

```
championChance         = 0.0        championMin = 0        championMax = 0
ignoreGameBalance      = True
levelVarianceEquation1 = 'records/proxies/lv5_elitechampion.dbr'
levelVarianceEquation2 = 'records/proxies/lv5_elitechampion.dbr'
limit2                 = 2
name1                  = 'records/creatures/enemies/chthonianherald_a01.dbr'    weight1 = 100
name2                  = 'records/creatures/enemies/celestialmonstrosity_d01.dbr' weight2 = 50
proxyPoolEquation      = 'records/proxies/proxypoolequation_01.dbr'
spawnMax = 3            spawnMin = 3
templateName           = 'database/templates/proxypool.tpl'
```

`spawnMin = spawnMax = 3` over a two-monster roster. This is not a singleton-dispenser pool and it
is not in a boss folder. It is a **trash pool that is exempt**.

**Consequence for consumers:** any implementation that derives exemption from `pool_kind == 'BOSS'`
is wrong on this pool — a 3-of-3 trash pool would be inflated to `⌊(3+1)×1.2⌋ = 4` min / `4` max
instead of the DB's `3–3`. It does not appear in waves 151–170 (§ 3.4), so it does not touch the
AC-10.4 window, but it is a live defect anywhere else in the 200-wave table. **Use the flag, never
the folder.** Corrected claim, for propagation:

> **73 of the 74 exempt pools are boss pools; the 74th is `poolsbasicgdx3/celestialmonstrosity_t3`,
> a 3-of-3 trash pool. All 36 FoA boss pools are exempt; 18 of 96 base-game boss pools are.**

### 2.3 A second, softer divergence: what "74/632" is a census *of*

U-9's 74 and my 74 count the same records, but U-9's `q5` sweep read only `pool{i}` on records
matching `proxy_w*_p*<suffix>.dbr`. There are **925** such records and **all 925 carry suffix `a`** —
so the "all suffixes" generality in `q5` was never exercised. Not an error; worth knowing that
`PAT_ANY` and `PAT_A` select the same 925 proxies, and the A/B population gap is *entirely* the
difficulty slot.

### 2.4 Multi-archive override audit — clean

158 of the 635 pools exist in more than one archive. Under GD's last-writer-wins resolution
(`base → gdx1 → gdx2 → gdx3 → sm_mod → sm1 → sm2 → sm3`) a survivalmode republication could in
principle drop a flag the base game set.

**It never happens.** `e3_override_audit.py`:

```
pools present in >1 archive: 158/635
EFFECTIVE-VALUE divergence across archives: 0
same effective value but field-presence differs: 0
```

Every multiply-published pool agrees with itself on both value **and** presence, in every archive
that carries it. The p04 answer therefore does not depend on the resolution order. `DB-CITED`.

---

## § 3 — The wave-160 board (E-3)

### 3.1 Spawn-point inventory, straight off the proxies

`records/proxies/tier16waves/proxy_w10_p{NN}a.dbr`, `DB-CITED` (`e4_out.txt` V4):

| pt | proxy | pool(s) | weight | `ignoreGameBalance` |
|---|---|---|---:|---|
| p01 | `…/proxy_w10_p01a.dbr` [sm3] | `poolsboss/nemesis_all` | 100 | **PRESENT = True** |
| p02 | `…/proxy_w10_p02a.dbr` [sm3] | `poolsbossgdx1/nemesis_all_noaetherialvanguard` | 100 | **PRESENT = True** |
| p03 | `…/proxy_w10_p03a.dbr` [sm3] | `poolsbossgdx1/nemesis_wendigooraetherialvanguard` | 100 | **PRESENT = True** |
| **p04** | `…/proxy_w10_p04a.dbr` [sm3] | `poolsbossgdx1/aetherialcolossus_galakros` | 100 | **ABSENT → False** |
| **p04** | (same proxy, 2nd alternative) | `poolsbossgdx2/korvaaktombguardian` | 100 | **ABSENT → False** |
| p05 | — | — | — | **record does not exist** |
| p06 | `…/proxy_w10_p06a.dbr` [sm3] | `poolsherogdx1/wendigocannibal_hero` | 100 | **PRESENT = False** (explicit) |

Note p06's flag is written and false — a deliberate authoring act, not an omission. And p05 simply
has no proxy at wave 160 (nor do p07/p08), which is why the P-E6 CSV shows five points.

### 3.2 The p04 cell, explicitly — **NOT EXEMPT**

Both p04 alternatives are 11-field records that do not contain the key. Verbatim, from every archive
that carries them:

```
--- [sm1] records/proxies/poolsbossgdx1/aetherialcolossus_galakros.dbr   (11 fields) ---
    championChance = 0.0 · championMax = 0 · championMin = 0
    levelVarianceEquation1 = 'records/proxies/lv7_uber hero.dbr' · limit1 = 1
    name1 = 'records/creatures/enemies/boss&quest/aetherialcolossus_galakros.dbr' · weight1 = 100
    proxyPoolEquation = 'records/proxies/proxypoolequation_01.dbr'
    spawnMax = 1 · spawnMin = 1 · templateName = 'database/templates/proxypool.tpl'
    >>> 'ignoreGameBalance' in record: False
--- [sm3] same record, byte-identical field set                         >>> in record: False

--- [sm2] records/proxies/poolsbossgdx2/korvaaktombguardian.dbr          (11 fields) ---
    …identical shape… name1 = '…/boss&quest/statue_korvaaktombguardian.dbr'
    spawnMax = 1 · spawnMin = 1        >>> 'ignoreGameBalance' in record: False
--- [sm3] same record                                                    >>> in record: False
```

**Resolution: `ignoreGameBalance = False`, provenance `TPL-DEFAULT`, for both alternatives.**

Applying U-9 § 6's count model at w = 160 (`spawnMinAdj[160] = spawnMaxAdj[160] = 0`):

| branch | p04 count | wave-160 body board |
|---|---|---|
| **exempt** (counterfactual) | `1–1` | 3 nemeses + **1** + 3 heroes = **7** ✓ ≤ 7 |
| **NOT exempt** (what the DB says) | `⌊(1+1)×1.2⌋ = 2` … `1+1 = 2` → `2–2` | 3 nemeses + **2** + 3 heroes = **8** ✗ |

**The DB selects the second row.** The spec § 10.8 ≤ 7 bound is **missed by 1**, and E-3's
"exempt ⇒ 7, bound holds" branch does not fire. I am reporting this rather than reconciling it —
neither of the candidate reconciliations the ledger already refused becomes admissible on this
evidence, and the deciding datum came back the way it came back.

Two adjacent facts the conductor may want when adjudicating:

- **The raw (unmodified) board still closes at 5** — `1+1+1+1+1 = 5` regular bodies with p06 on,
  which is what the measured census matched exactly. The 8 is entirely a difficulty-additive
  artefact, and 3 of its 5 spawn points are protected by the flag while p04 is not.
- **p04 is the only wave-160 point whose proxy offers two alternatives.** Both are `spawnMin =
  spawnMax = 1` single-boss dispensers — structurally the exact case Crate's Aether-Crystal warning
  describes — and both were left unflagged. If that is a Crate authoring oversight it is *their*
  oversight, and the shipped game doubles those bosses on Gladiator. U-9 § 5.2 already called this
  out as intended behaviour for the 78 unflagged base-game boss pools; wave 160 p04 is that
  behaviour landing on the showcase wave.

### 3.3 Wave-160 totals under each reading

`e2_out.txt` / `e3_out.txt`, expected bodies:

| reading | w160 E (p06 on) | w160 E (p06 off) |
|---|---:|---:|
| all-non-exempt (default False everywhere) | 12.00 | 8.00 |
| **AS-DECLARED (measured)** | **9.00** | **5.00** |
| all-boss-pools exempt | 8.00 | 4.00 |
| `spawnMax < 2` exempt (the P-E6 `s8` guard) | 5.00 | 4.00 |

With the empty-roster guard of § 4 applied, AS-DECLARED gives **8.00 / 5.00** — the 8 of § 3.2.

### 3.4 Waves 151–170: the calibration-band delta

**31 distinct exempt pools appear in the band**, across 265 rows / 174 distinct pools. Per-wave
(`e2_out.txt`), expected-bodies delta of AS-DECLARED against all-non-exempt:

```
 w151  +0.00     w156  −1.00     w161  −1.00     w166  −1.67
 w152  −0.25     w157  +0.00     w162  +0.00     w167  +0.00
 w153  +0.00     w158  +0.00     w163  −0.50     w168  +0.00
 w154  −2.00     w159  −1.25     w164  −1.33     w169  −2.00
 w155  +0.00     w160  −3.00     w165  −2.33     w170  −4.33

BAND TOTAL  p06 ON : declared 398.17  ·  allFalse 418.83  ·  delta −20.67
BAND TOTAL  p06 OFF: declared 355.50  ·  allFalse 374.83  ·  delta −19.33
```

**The measured exemption set is worth ≈ 20.7 bodies over the band, ≈ 5× the 4.0 the commission
reports for gamora's declared-override table.** My absolute totals are not comparable to her
306.83 / 310.83 / 316.5 — my model differs at least in the empty-roster term of § 4 and possibly
elsewhere — so I am deliberately **not** mapping them onto AC-10.4. What transfers is the *set*:
the 31 pools below, with their waves. That is the minimum override table.

| pool | waves in band |
|---|---|
| `poolsboss/ghost_alkamos` | 166 |
| `poolsboss/nemesis_all` | 160, 165 |
| `poolsboss/nemesis_all_nokymon` | 170 |
| `poolsboss/nemesis_all_nooutlaw` | 170 |
| `poolsbossgdx1/fleshweaverkrieg` | 152, 169 |
| `poolsbossgdx1/humanascendant_terrnox` | 164 |
| `poolsbossgdx1/humanascendant_valaxteria` | 164 |
| `poolsbossgdx1/nemesis_aetherialvanguard` | 161 |
| `poolsbossgdx1/nemesis_all_noaetherialvanguard` | 160 |
| `poolsbossgdx1/nemesis_all_nobeast` | 165, 170 |
| `poolsbossgdx1/nemesis_all_novoidborn` | 170 |
| `poolsbossgdx1/nemesis_beast` | 154 |
| `poolsbossgdx1/nemesis_wendigooraetherialvanguard` | 160 |
| `poolsbossgdx2/fatherkymon` | 154, 166 |
| `poolsbossgdx2/gryphonstone` | 159 |
| `poolsbossgdx2/korvaakfinal` | 169 |
| `poolsbossgdx2/korvaakmessenger` | 159 |
| `poolsbossgdx2/nemesis_eldritch` | 154, 170 |
| `poolsbossgdx3/avian_worldtear` | 170 |
| `poolsbossgdx3/chthonianherald_prodromus` | 166 |
| `poolsbossgdx3/chthoniantyrant_grulthunn` | 154 |
| `poolsbossgdx3/direwolf_frozenwastes` | 156 |
| `poolsbossgdx3/giant_totem` | 169 |
| `poolsbossgdx3/kurnchthonic_chieftain` | 163 |
| `poolsbossgdx3/kurnchthonic_shaman` | 156 |
| `poolsbossgdx3/kurnchthonic_strongholdchieftain` | 165 |
| `poolsbossgdx3/nemesis_kurn` | 154, 170 |
| `poolsbossgdx3/rok_wind` | 159 |
| `poolsbossgdx3/wight_iceboundpassage` | 169 |
| `poolsbossgdx3/wight_scarsfell` | 164 |
| `poolsbossgdx3/yeti_rimehorn` | 159 |

Waves 151, 153, 155, 157, 158, 162, 167, 168 contain **no** exempt pool — the flag is a no-op there.

---

## § 4 — Rider hazard I did not go looking for: the phantom regular

**Not commissioned. Reporting because it is larger than the thing I was commissioned for.**

`DB-CITED`: **117 of the 635 pools declare no `name{j}` roster at all** — 95 hero, 15 devotion,
7 bounty. And **all 117 declare `spawnMin = spawnMax = 0`** (`e3_out.txt` Q2: *"of those, 0 declare
spawnMin/Max != 0"*). Agreement with the P-E6 CSV's own `roster_n` column: **117/117**.

The non-exempt branch adds `+1` to `spawnMin` and multiplies by 1.20. On a pool with an empty
regular roster that produces `⌊(0+1)×1.2⌋ = 1` regular — **drawn from a roster with no entries**.
U-9 § 5.1 already noted the structural case (`poolshero/chthoniandevourer_hero.dbr`: champion-only
roster, zero regulars); the new census shows Crate never once pairs a nonzero `spawnMin` with an
empty roster, in 117 opportunities.

**Grade: DERIVED.** The engine's behaviour when a difficulty additive raises `spawnMin` above an
empty roster is not stated anywhere in the DB or the templates — `NAMED-ABSENT`. What *is* cited is
that the authored data never creates the situation. Both readings are enumerable:

| reading | wave 160 | band 151–170 (p06 on) |
|---|---:|---:|
| additive materialises a body from an empty roster | 9.00 | 398.17 |
| **empty roster ⇒ zero regulars (guard)** | **8.00** | **371.17** |

**The guard is worth 27.0 expected bodies over the band** — larger than the 20.7 the exemption flag
itself is worth, and ~7× the 4.0 the commission is trying to account for. It is also what makes the
wave-160 board read `3 + p04 + 3` rather than `3 + p04 + 4`, i.e. it is *already* implicit in the
spec's own "3+1+3 = 7" arithmetic and in E-4's FACT-5 ruling ("`roster_n = 0` ⇒ zero regulars").
So the spec and I agree on the guard; I am flagging that it is a **DERIVED** term doing 27 bodies of
work, and that its DB support is an absence-of-counterexample rather than a statement.

---

# PART II — TASK 2 (rider): FINDING F-8, the Soulfire cost record

## § 5 — Adjudication: the record declares NO cost. F-8's premise is a misattribution.

### 5.1 What the record actually holds

`records/skills/playerclass09/eyeofreckoning2.dbr` [GDX2.arz], `Class =
SkillSecondary_AttackProjectileOrbiting`, `templateName =
database/templates/skillsecondary_attackprojectileorbiting.tpl`, **330 fields**.

**`skillManaCost` is not among them.** `DB-CITED`.

The only cost-shaped fields present are:

```
skillManaCostReduction          = 0.0        (scalar)
skillManaCostReductionModifier  = 0.0        (scalar)
```

— both *reductions*, both zero, both scalars rather than rank arrays. Corpus-wide sweep of every
record whose path contains `eyeofreckoning` (**47** records: 2 `playerclass09` skills, 12 fx,
29 item skill-modifiers, 4 sounds) returns `skillManaCost = ABSENT` on **all of them except
`eyeofreckoning1`**, which holds
the 26-element `[4,4,5,5,5,6,6,7,7,8,8,9,9,10,10,11,11,12,12,13,13,14,14,15,15,16]` — the base EoR
channel cost that P-E1 § 4.1 cited and that L-22's tooltip decomposition consumed as
`skillManaCost[26] = 16.0`.

### 5.2 Where the "3–20" actually lives

`records/skills/playerclass05/aetherray2.dbr` [database.arz], `Class = Skill_Modifier`,
`skillDisplayName = tagClass05SkillName06B`, `skillBaseDescription = tagClass05SkillDescription06B`:

```
skillManaCost = [3.0, 4.0, 4.0, 5.0, 6.0, 7.0, 8.0, 8.0, 9.0, 10.0, 11.0,
                 12.0, 12.0, 13.0, 14.0, 15.0, 16.0, 16.0, 17.0, 18.0, 19.0, 20.0]   (22 ranks)
```

That is **Disintegration**, the Albrecht's-Aether-Ray modifier. And its tag is where the fine print
lives — `tags_skills.txt`, verbatim:

> `tagClass05SkillDescription06B` = *"Pours all of your energy into the Aether Ray, turning it into
> a catastrophic force that disintegrates all it touches. **^oEnergy Cost increase is per damage
> interval.**"*

**Corpus sweep: `aetherray2.dbr` is the ONLY skill record in the entire corpus whose `skillManaCost`
spans exactly `min = 3, max = 20`.** One record, uniquely identified. `DB-CITED`.

### 5.3 Soulfire's own tag says nothing about cost

`tagGDX2Class09SkillDescription07B`, from `gdx2/tagsgdx2_skills.txt`, **verbatim and complete**:

> *"Through the righteous fire burning with the Oathkeeper's soul, the light becomes as if a
> physical force, spiraling outward and piercing through unwary foes during the Eye of Reckoning."*

`tagGDX2Class09SkillName07B` = `'Soulfire'`.

No cost clause. No interval clause. No `^o` fine-print segment at all. And a corpus-wide sweep for
tags containing *"per damage interval"* returns **exactly one hit** — Disintegration's. `DB-CITED`.

For contrast, the parent's tag `tagGDX2Class09SkillDescription07A` **does** carry the fine print
that L-22 built on: *"…^oRequires a melee weapon. At 100% Attack Speed, Eye of Reckoning deals
damage and drains Energy every 0.16s."*

### 5.4 Diagnosis: how the two records got fused

The chain is traceable and P-E1 is clean.

- **P-E1 § 4.2 is correct.** It cited Disintegration's *"Energy Cost increase is per damage
  interval"* and its 3–20 **as a control case** — a skill whose modifier carries a per-interval cost
  clause — and explicitly concluded *"**It does not discriminate.**"* It was reasoning about the
  **EoR base drain** unit fork (M1 vs M2), not about Soulfire.
- **P-E1 § 5.2 is also correct.** Its Soulfire rank table has exactly two columns —
  `offensiveLightningMin` and `offensiveTotalDamageReductionPercentMin` — and **no cost column**,
  because there is no cost field. My extraction reproduces that table value-for-value (§ 5.5).
- **Spec § 3.1's Soulfire bullet fused them:** P-E1 § 4.2's Disintegration sentence was carried into
  a sentence about Soulfire, becoming *"Its own `skillManaCost` is 3–20 rank-scaled (P-E1 § 5, build
  MAXES the node); fine print: 'Energy Cost increase is per damage interval'"*. The cross-reference
  points at § 5 (the Soulfire section) while the content came from § 4 (the Aether Ray control).

**Nothing in P-E1 needs correcting. Spec § 3.1's Soulfire bullet and § 14's F-8 need striking.**

### 5.5 The commission's three questions, answered

**Q1 — is the 3–20 a per-interval INCREMENT or a total cost?**
**Neither, for Soulfire — it is not Soulfire's number.** For its actual owner, Disintegration, it is
a per-interval **increment**: an *increase* added to the parent Aether Ray's own 12–87 cost, which
is precisely why Crate wrote the clarifying line — the modifier's number is denominated differently
from the base's tooltip display. `skill_modifier.tpl` declares its `skillManaCost` with
`description = "Activated Skills Only"` (`TPL-CITED`), i.e. the field is the modifier's contribution
to an activated parent. This is the same shape as Oathkeeper's own `aegis2` (22 ranks, 2–22),
`ascension2` (3–45) and `judgment2` (4–25) — all `Skill_Modifier`. **Soulfire is not a
`Skill_Modifier`; it is a `SkillSecondary_*`, and it carries no such field.**

**Q2 — does the cost gate on projectile launches or on damage intervals?**
**Moot for Soulfire — there is no cost to gate.** The two structural facts that would have decided
it, had there been one:

- **`TPL-CITED`, `skillsecondary_attackprojectileorbiting.tpl`:**
  ```
  Variable { name = "projectilePeriod"  class = "variable"  type = "real"
             description = "Delay between projectile launches (seconds)."  defaultValue = "0.5" }
  ```
  The template's own words say **launches**, and **seconds**. `eyeofreckoning2.projectilePeriod =
  0.2` → one launch every 0.2 s, plain seconds. This independently **confirms L-26 / HALT-8's
  closure of the interval basis at 0.2 s plain seconds**, and adds that the interval is a *launch*
  cadence, not a damage cadence. (Contrast the parent: `skill_attackradiusspin.tpl` declares
  `timeBetweenAttacks` as `type = "int"` with `description = "Time between hits to enemies along
  the path"` — a *hit* cadence, in 0.8 ms quanta, per P-E1 § 1.3.)
- `skillProjectileNumber = 1`, `projectilePiercingChance = 100.0`,
  `projectileDirection = 'Counterclockwise'`, `projectileStart = 'Front'`.

**Q3 — what does the rank table hold at total rank 15?**
`eyeofreckoning2` has **exactly two** rank-scaled arrays, both 22 long (`skillMaxLevel = 12`,
`skillUltimateLevel = 22`). At rank 15:

| field | r13 | r14 | **r15** | r16 | r22 (ultimate) |
|---|---:|---:|---:|---:|---:|
| `offensiveLightningMin` | 212 | 229 | **246** | 263 | 402 |
| `offensiveTotalDamageReductionPercentMin` | 21 | 22 | **23** | 24 | 30 |

Byte-identical to P-E1 § 5.2's table. **There is no `skillManaCost` row to read at rank 15, because
the array does not exist.** `offensiveTotalDamageReductionPercentDurationMin = 2.0` (scalar).

### 5.6 The family law behind it, and the control that proves it is a choice

The field is **reachable** on this record class — I checked, and my first pass got this wrong before
fixing the include resolver. GD templates declare includes as `Variable { name = "Include File";
type = "include"; defaultValue = "database\Templates\TemplateBase\Skill_Activated.tpl" }`, with
Windows separators and mixed case. After correct expansion:

```
skillsecondary_attackprojectileorbiting.tpl        (6 own vars, 2 includes)  -> 610 variables
  skill_attackprojectile.tpl                       (11 own, 5 includes)
    TemplateBase/Skill_Base.tpl                    (71)
    TemplateBase/Skill_Attack.tpl                  (9)  -> Parameters_Offensive (464), RacialBonus (8)
    TemplateBase/Skill_Activated.tpl               (28) -> Parameters_Skill (15), skill_refresh (12)
    TemplateBase/Skill_ProjectileBase.tpl          (9)
    TemplateBase/Skill_ComboCharge.tpl             (6)
  templatebase/skill_secondary.tpl                 (5)

skillManaCost -> DECLARED by TemplateBase/Skill_Activated.tpl
                 class = "array"  type = "real"  defaultValue = ""  description = ""
```

So `skillManaCost` **is** declarable on `SkillSecondary_AttackProjectileOrbiting`. Its template
default is the empty string — there is no numeric fallback; an absent array is *no cost array*, not
*a cost of 1*. `TPL-CITED`. (Only six templates in the whole 819-file set declare `skillManaCost`:
`templatebase/skill_activated.tpl` with an empty description, and five `skill_*modifier`/
`*transmuter` templates all annotated *"Activated Skills Only"*.)

**Control census** — every `SkillSecondary_*` record in the corpus, does it declare `skillManaCost`?

| | records | declare it |
|---|---:|---:|
| all `SkillSecondary_*` classes (20 distinct) | **476** | **2** |
| the two that do | `records/sandbox/jakub/skillsecondary_orbiting.dbr` (26 ranks, 10–60) · `records/sandbox/jakub/skillsecondary_buffattackradiusduration.dbr` (22 ranks, 15–56) | |

**Both are in Crate's `records/sandbox/jakub/` developer scratch directory. Zero shipped
`SkillSecondary_*` record carries its own energy cost.** `DB-CITED`.

That the sandbox record is *the same class as Soulfire* and *does* set the field is the useful part:
it proves the omission is an **authoring policy consistently applied to shipped content**, not a
template limitation. Secondary skills are dispensed by their parent's activation
(`skill_secondary.tpl`: `specialSecondaryActivation`, `description = "True disables default
secondary activation for unique activation on a skill by skill basis"`, `defaultValue = "0"`;
**`eyeofreckoning2` does not declare it** → default → **default secondary activation**) and they
bill through the parent, not beside it. Corroborating within Oathkeeper: `judgment3`
(`SkillSecondary_BuffAttackRadiusDuration`) is likewise `skillManaCost = ABSENT`, while every
`Skill_Modifier` in the mastery (`aegis2`, `ascension2`, `judgment2`) carries one.

Parent linkage, for completeness: `_classtree_class09.dbr` holds `skillName31 = eyeofreckoning1`
and `skillName32 = eyeofreckoning2` in adjacent slots; `records/ui/skills/class09/skill27.dbr`
carries the UI node. 67 records reference `eyeofreckoning2`, 65 of them `augmentSkillName*` on gear.

### 5.7 Verdict, and what it does to F-8

**Not undecidable. Decided, against the premise.**

> **Soulfire (`records/skills/playerclass09/eyeofreckoning2.dbr`) declares no energy cost of any
> kind.** No `skillManaCost` array; a zero-valued `skillManaCostReduction`; no cost clause in its
> description tag; and 474 of 476 `SkillSecondary_*` records agree with it. The "3–20 rank-scaled,
> per damage interval" belongs to `playerclass05/aetherray2.dbr` (Disintegration), the unique record
> in the corpus with that span, and its clause is about the Aether Ray.

Consequences, stated plainly and left for the conductor to rule on:

1. **F-8's over-constraint dissolves.** It asked *"what positive Soulfire cost can the fixture's
   sustain admit?"* and found none. The DB's answer is that the question has no referent: there is
   no Soulfire cost term. A bound that admits no positive value is exactly what you would expect
   when the true value is **0**.
2. **gamora's ratified `effective_per_s = 0.0` is correct, and its grade can move.**
   `UNADJUDICATED` → **DB-CITED (field absent; record + 474-record family control)**. She held the
   right number for the right reason — she refused to fit it — and the citation now backs it.
3. **The exactness of `176.4 = 16.0 × 12.25 × 0.90` gains a second explanation.** Spec § 3.1 reads
   that exactness as evidence that Soulfire's cost is *declared separately and excluded from the
   tooltip*. It is at least equally consistent with — and now better explained by — **there being
   nothing to exclude**. The `×0.90` factor remains `source UNLOCATED`; this probe touched it only
   to confirm that `eyeofreckoning2.skillManaCostReduction = 0.0` — as are both reduction fields on
   all 29 `eyeofreckoning` item skill-modifiers — so **Soulfire is not the missing −10 %, and
   neither is any EoR gear modifier**. That hunt is still open.
4. **The 0.2 s interval basis is re-confirmed and sharpened.** `TPL-CITED` as *"Delay between
   projectile launches (seconds)"* — L-26 / HALT-8 stands, and the interval is a launch cadence.
5. **Recommended edits:** strike the Soulfire cost sentence from spec § 3.1; retire F-8 in § 14 as
   **RESOLVED — premise withdrawn (misattribution), no cost term exists**; leave AC-3.2's FINDING
   clause unfired on this axis.

**What I am not claiming.** I have not shown that Soulfire is free *in the client* — only that the
DB gives it no cost. If a tooltip ever shows a Soulfire energy line, that would be a client-side
composition of the parent's cost and would need its own citation. And I did not re-derive the
fixture's sustain arithmetic; § 5.7 changes one input to it and gamora owns the recomputation.

---

## § 6 — Residuals

| # | Item | Grade | What would close it |
|---|---|---|---|
| **E2-1** | Engine behaviour when a difficulty additive raises `spawnMin` above an **empty** regular roster (§ 4). Worth 27.0 bodies over the band. | DERIVED / `NAMED-ABSENT` in DB+TPL | Observed hero-placement counts on a Gladiator wave with a champion-only pool; or engine disassembly |
| **E2-2** | Whether the exempt branch also bypasses `proxyPoolEquation`. All wave-160 pools carry `proxypoolequation_01.dbr`, established as `poolValue * 1` on all four spawn/champion fields (KC2-EHP fact 15), so it is a no-op **today** and the question is inert for this fixture — but not answered in general. | `NAMED-ABSENT` | An exempt pool with a non-identity `proxyPoolEquation`; none exists in the Crucible set |
| **E2-3** | The `×0.90` cost factor in L-22's decomposition. Ruled out here: `eyeofreckoning2` (both reduction fields 0.0) and every `eyeofreckoning` item skill-modifier (all 0.0). | UNRESOLVED | grimtools `b28gD0KN`, or an item-side `skillManaCostReduction`/`characterManaCostReduction` sweep over the fixture's 16 gear slots |
| **E2-4** | Template lineage: `.tpl` claims rest on the live install, `.dbr` claims on Edition-II (§ 0.3). Not found load-bearing; not proven irrelevant. | declared | Diff the two installs' `templates.arc` if a version skew is ever suspected |

---

## § 7 — Emissions

`agentic_orchestration/legolas/scratch/2026-08-08-kc2-e2-exemption/`

| file | role |
|---|---|
| **`pe6_pool_ignoregamebalance.csv`** | **PRIMARY** — sidecar, 635 rows keyed by `pool_record`. SHA-256 `40182de2…f77d3` |
| **`pe6_crucible_wave_pools_v2.csv`** | convenience — P-E6 CSV + 3 columns, 1998 rows × 26 cols. SHA-256 `bbdc18f1…6e5587` |
| `e1_census.py` / `e1_census.json` / `e1_points_gladiator.json` | three-population census; the 632/635/637 reconciliation |
| `e2_emit.py` / `e2_out.txt` / `e2_resolve.json` | emitter; index-bound audit; wave-160 board; band table |
| `e3_override_audit.py` / `e3_out.txt` | multi-archive audit; empty-roster census; 4 variant band totals |
| `e4_verify.py` / `e4_out.txt` | ABSENT-is-not-an-artefact verification; wave-160 proxy inventory |
| `e5_exempt_list.txt` / `e6_band_exempt.txt` | the 74 exempt pools; the 31 that appear in 151–170 |
| `f8_soulfire.py` / `f8_out.txt` | full field dump of `eyeofreckoning2` + `eyeofreckoning1`; tag sweep |
| `f9_soulfire_tpl.py` / `f9_out.txt` | ownership of the 3–20; every `eyeofreckoning` record's cost fields |
| `f10_tpl_expand.py` / `f10_out.txt` | corrected template include expansion; the 6 templates declaring `skillManaCost` |
| `f11_secondary_census.py` / `f11_out.txt` | 476-record `SkillSecondary_*` control census; pc09 table; parent linkage |

**Sources.** `~/Games/vendor/grim-dawn-edition-II-20260724/{database,gdx1,gdx2,gdx3,mods/survivalmode,survivalmode1,survivalmode2,survivalmode3}` ·
`~/Games/vendor/grim-dawn/database/templates.arc` · Crate, *Grim Dawn Modding Guide*, "Spawn Pool"
(via U-9 § 5.2, DEV-DOC) · prior emissions: `2026-08-07-u9-spawnmin-operator-order.md` §§ 5.1–5.5,
§ 6 · `2026-08-07-pe6-crucible-wave-composition.md` · `2026-08-07-pe1-eor-spin-parameters.md`
§§ 1.3–1.4, 4.1–4.3, 5.1–5.2 · `2026-08-08-kc2-ehp-composition-probe.md` fact 15.

**Filed:** legolas, 2026-08-08. Read-only throughout. Uncommitted per charter § 4.7.
