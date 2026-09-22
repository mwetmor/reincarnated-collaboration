# Substrate-integrity census — ARZ archive-precedence exposure — 2026-09-21

**Agent:** elrond (data steward) · **Run:** KC2-PLAY · **Conductor:** gandalf
**Mode:** read-only enumeration. No tool in any seam was modified. No repair was attempted.
**Commissioned from:** legolas S-1 § 5 (`findings/2026-09-21-s1-save-bio-block.md`) + C-2 § 6 (`…-c2-per-cast-energy-costs.md`), routed to elrond as a curation question.

---

## VERDICT

**The exposure is REAL, BROAD, and — on every committed value I could test — it did not land.**

| | |
|---|---|
| **The hazard** | ⚑ **7,385 record paths** exist in more than one main archive *and differ in content*. A first-hit reader returns a stale record on every one of them. |
| **Defective tools** | ⚑ **23**, all in one lineage (`gdc-parse-g7`, July 28, and the `wr1`/`wr3` analyses grown from it). One — `lib_corpus.get()` — has **17 importers**. |
| **Committed data** | ⚑ **CLEAN on every discriminating test run.** 407/407, 95/95, 925/925, 635/635, 62/62, 3/3, 0 stale. Details in § 4. |
| **The monster roster** | ⚑ **CLEAN, and the check was load-bearing** — 460 of the 466 tier-16 records resolve differently under correct precedence, and the committed values took the correct side. |
| **Class closure** | ⚑ **NOT a one-tool defect** — 23 tools, not one. But **not a data defect either**: the defective tools' three git-tracked artifacts contain only single-archive records, so first-hit and correct coincide in them. **The bug is live in the instruments and absent from the outputs.** |

**For the v3.4 cut: no input changes. I found nothing that moves a pack value.**

---

## 1 · THE PRECEDENCE RULE (Q3)

**Stated once: within a game mode, the LAST archive in load order that holds the path wins outright — whole-record replacement, not field merge.**

```
CAMPAIGN   database.arz < GDX1.arz < GDX2.arz < GDX3.arz
CRUCIBLE   database.arz < GDX1.arz < GDX2.arz < GDX3.arz
                        < SurvivalMode.arz < SurvivalMode1.arz
                        < SurvivalMode2.arz < SurvivalMode3.arz
```

### It is uniform across record TYPES and conditional on MODE

⚑ **This is the part neither commission states, and it is the sharper half of the rule.** The SurvivalMode archives are a *mod* database (`mods/survivalmode/`). They layer above the main stack **only when the Crucible is in play**, and they are substantial:

| archive | records held | of which OVERRIDE a main-archive path |
|---|---|---|
| `SurvivalMode.arz` | 3,147 | **1,486** |
| `SurvivalMode1.arz` | 1,004 | **518** |
| `SurvivalMode2.arz` | 811 | **530** |
| `SurvivalMode3.arz` | 1,431 | **712** |

**Consequence, and it cuts both ways:**

- ⚑ **legolas's `arz.find()` defaults to `include_mods=False`.** That is *correct* for S-1/C-2 (campaign player-character questions) and **wrong for any KC2 roster question** — where the winner is a SurvivalMode archive on essentially every monster. The precedence-corrected helper is only corrected for half the problem.
- ⚑ Conversely, the engine's 8-archive readers would be **wrong for a campaign question**, because they would apply Crucible rebalancing to a campaign record.

**There is no single right order. There is a right order per mode, and the mode must be named.**

### Evidence for the direction (not assumed — measured)

| test | result |
|---|---|
| array-length change, first-hit vs correct, across all 7,385 differing records | **1,082 EXTEND** · **3 SHORTEN** · 1,834 same-length-different-values |
| field-count change | **5,813 gain fields** · 98 lose · 1,474 unchanged |
| the decisive structural proof | `playerlevels.dbr`: `maxPlayerLevel` **85 → 100**, `maxDevotionPoints` **50 → 55**. ⚑ **The referent is level 100 with 55 devotion points — both out of range under the first-hit record.** The base record describes a game that cannot contain the character we decoded. |

### What is NOT sourced — declared per Law 3

⚑ **The ordering *among* the four SurvivalMode archives is `CONSISTENT-NOT-SOURCED`.** It is exercised — **602 paths sit in more than one SurvivalMode archive and 469 of them differ** — so it is not a free parameter. My computed order reproduces the engine pipeline's independently recorded `winner_archive` on 407/407 rows, **but 49 of those rows are the only ones that actually test the SM ordering**, and agreement between two tools that may share a naming convention is not independent evidence. Same shape as S-1 § 1.2's two parsers inheriting one ancestor. **No load-order manifest exists on this host.** The order is corroborated, not sourced.

---

## 2 · THE EXPOSURE, ENUMERATED (Q1)

### 2.1 The corpus

`/Users/admin/depots/`, 8 archives. Record counts **34,114 / 18,447 / 16,451 / 24,178 / 3,147 / 1,004 / 811 / 1,431** — identical to the 2026-07-23 probe S-1 cites, so the corpus is the same vintage the extractions ran against.

⚑ **Caveat declared:** the engine-side scripts point at `~/Games/vendor/grim-dawn-edition-{II,III}`, which **does not exist on this host**. Those scripts cannot be re-run here. Record-count identity with the probe corroborates that the two trees were the same vintage; it does not prove byte-identity. `UNDETERMINED-BY-EXECUTION`.

| measure | count |
|---|---|
| distinct record paths, 4 main archives | 82,131 |
| paths in **>1** main archive | **8,148** (9.9 %) |
| ...content **IDENTICAL** (first-hit harmless) | 763 |
| ⚑ ...content **DIFFERS** (first-hit wrong) | **7,385** |

### 2.2 The truncation sub-class — the one that returns a wrong value *cleanly*

**1,082 truncation instances across 441 records** where the first-hit array is *shorter* than the correct one. This is the class that, under a `min()`/clamp index, returns a plausible number with no error.

⚑ **legolas found one stub mastery. There are three.**

| record | base | live | delta at rank 50 |
|---|---|---|---|
| `_classtraining_class07.dbr` (Inquisitor) | **32-rank stub** | **GDX1**, 100 ranks | — |
| `_classtraining_class08.dbr` (Necromancer) | **32-rank stub** | **GDX1**, 100 ranks | — |
| `_classtraining_class09.dbr` (Oathkeeper) | **32-rank stub** | **GDX2**, 100 ranks | `+64/+56/+256` → `+250/+125/+650` |

All three carry the same four truncated fields (`characterStrength`, `characterIntelligence`, `characterLife`, `characterMana`), all 32 → 100. **Any ledger touching an Inquisitor or Necromancer character has the identical trap waiting.**

⚑ **And the 3 reverse-direction cases are the nastier shape.** `item_bleedout_buff_01.dbr` holds a **60-entry** `offensiveSlowBleedingMin` in base and a **3-entry** one in GDX1 — *with entirely different values* (`20/25/30…` vs `45/55/62`). A first-hit reader indexing rank 10 gets a real float out of a dead array. **No IndexError ever fires, in either direction.**

### 2.3 Tooling verdict — 11 distinct resolver implementations

| class | count | verdict |
|---|---|---|
| 🔴 **FIRST-HIT over ascending base→GDX3** | **23 tools** | **EXPOSED** |
| 🟢 LAST-HIT / explicit precedence | ~40 implementations + importers | CORRECT (several say so in a comment) |
| 🔵 REPORTS-ALL (prints every hit) | ~60 probes | SAFE — surfaces duplicates rather than hiding them |
| ⚪ SINGLE-ARCHIVE (one named archive) | ~45 | NOT EXPOSED, but **stale-by-design if the record is overridden** |
| ⚫ NO-RESOLUTION (`.arz` in a comment or sha-pin only) | many | n/a |

**The 23 cluster in one lineage** — `legolas/scratch/2026-07-28-gdc-parse-g7/` and the `wr1`/`wr3` analyses grown from it. **Everything from `2026-08-07-pe5-devotion` onward, and every `research/scripts/pm4*` tool, is precedence-correct.** The defect has a date boundary: it was fixed in practice around 2026-08-07 without ever being named until now.

**The one that propagates:**
`legolas/scratch/2026-07-28-gdc-parse-g7/lib_corpus.py` — `def get(rec): for p,a in _arz: if rec in a.recs: return …` over ascending order. **17 importers.** Two siblings (`resolve_gear.py`, `name_resolve.py`) share the defect and emit three git-tracked JSONs.

**Two latent oddities, recorded not fixed:**
- `scratch/2026-08-01-density/p11_sr.py` — `setdefault` over a **non-monotonic** order (`gdx2, gdx3, base, gdx1`). Its `get()` is defined and never called. Latent only.
- `notes/…-d12-diversion-decode/*.py` load their resolver from `/tmp/d12/`, which no longer exists. Classified against the repo copy. ⚑ **`UNDETERMINED` — if `/tmp/d12/` ever held a modified copy, that is unverifiable now.** Declared rather than assumed equivalent.

### 2.4 Engine and Godot — not exposed

- **`simulation/kc2/` (the model package): NO-RESOLUTION.** Zero archive opens. It reads SHA-pinned CSVs. The ~40 `records/…dbr` literals in it are identity keys, never lookups.
- **The two engine archive readers** (`gamora_kc2_c1_closure_ed3_…`, `gamora_kc2_arr_repass_ed3_…`) both take `ent[-1]` over the **full 8-archive** order, with docstrings naming whole-record replacement. **CORRECT for Crucible work, which is what they do.**
- **`reincarnated-godot`: NO-RESOLUTION, confirmed.** No `.arz`/`.arc` open anywhere. `record_path` is an opaque string key or directory prefix.

---

## 3 · THE NEAR-MISSES IN ALREADY-COMMITTED WORK

Three places where the correct precedence was **load-bearing** and the record survives only because the tool had it right.

### 3.1 ⚑ The pack's most-cited constant sits directly on this exposure

`records/items/gearweapons/melee2h/d107_blunt2h.dbr` — the referent's weapon — **exists in GDX1 and GDX2, and they differ**:

| | GDX1 (first hit) | **GDX2 (correct)** |
|---|---|---|
| `augmentSkillName2` | **absent** | `…/eyeofreckoning1.dbr` |
| `augmentSkillLevel2` | **absent** | **4** |

⚑ **The `+4 Eye of Reckoning` grant exists ONLY in the GDX2 record.** A first-hit reader computes `EOR_TOTAL_RANK = 22`, not 26 — and `fixture.py` carries `EOR_TOTAL_RANK = 26` and `SKILL_MANA_COST_R26 = 16.0` as `DB-CITED`. **C-2's control matched the pack exactly because it used precedence.** S-1 § 7's source list cites this record as *"GDX1"*, which is the first hit, not the winner — **a mislabel in the record, not an error in the value.**

*(Relatedly: `fixture.py`'s `TIME_BETWEEN_ATTACKS_RAW = 200` is the only `Cited` constant in the file naming an archive, and it names **`GDX2.arz`** — the correct direction.)*

### 3.2 The item-cost equation is a different formula, not a different number

`records/game/itemcostformulas_legend.dbr`, `melee2hStrengthEquation`:

```
base   0.92*(0.3*((itemLevel*23)+6*((damageAvgBase*0.381)*(1+(damageAvgPierceRatio/100)))-10*(0.05*(itemLevel^1.61)-1))+10)
GDX1   0.965*(2.79*(itemLevel*6.55)^1.205-1.8*(itemLevel*5.84)^1.2785+((itemLevel^1.5)*0.0125-1)*-5+18)
```

**Not a retune — a different functional form, taking different inputs.** S-1 used the GDX1 record (the winner) and got ≈474 Physique required. The base equation takes a `damageAvgBase` term the GDX1 one does not, so a first-hit read would not merely shift the number, it would demand inputs the caller never supplied. Correct by use, not by luck.

### 3.3 The half that was immune

⚑ **S-1's closed-form control does not depend on precedence at all.** Every constant it rests on is **identical across all holders**: `strengthIncrement`/`dexterityIncrement`/`intelligenceIncrement` = 8, `lifeIncrement` = 20, `lifeIncrementDexterity` = 8, `lifeIncrementIntelligence` = 12, `manaIncrement` = 16, `characterModifierPoints` = 1, and `malepc01.dbr`'s base 50/50/50/250/250 across all four archives. **The mapping proof in S-1 §§ 1–3 is untouched by this class.** That is worth stating as plainly as the exposure: the finding that mattered most was built on ground this hazard cannot reach.

---

## 4 · THE BLAST RADIUS ON COMMITTED VALUES (Q2)

**Method.** Rather than infer from each tool's code shape, I tested the **output**: for every committed row whose record collides, decode both the first-hit and the precedence-correct archive and ask **which one the committed value reproduces.** That discriminator does not care what the tool looked like.

**Surface:** 15,551 distinct DBR paths cited across the engine, collaboration, and godot trees. **2,266 collide; 2,170 collide *and* differ.**

| test | discriminating rows | **stale** | verdict |
|---|---|---|---|
| `pm4i_band_c_roster.csv` · recorded `winner_archive` vs computed | 407 (**387** where first-hit differs) | **0** | ⚑ CLEAN |
| `pm4o_oa_da.csv` · `record_archive` | 95 | **0** | CLEAN |
| `pe6_crucible_wave_pools_v2.csv` · `proxy_archive` | 925 | **0** | CLEAN |
| `pe6_crucible_wave_pools_v2.csv` · `pool_archive` | 635 | **0** | CLEAN |
| `d1_alert_anim.csv` · `alertAnimChance` **value** (30 base → **0** Crucible) | 62 | **0** | ⚑ CLEAN — value-level |
| ⚑ `monsterClassification` **flips** across the whole roster union | **3** | **0** | ⚑ see below |
| `t22_band_a_monster_stats.csv` · `bio_record` | 4 | **0** | CLEAN |
| `pm4m_body_chain.csv` · `bio_record` | 1 | **0** | CLEAN |
| `pm2_tg2_monster_oa_da.csv` · `bio_record` | 0 | — | non-discriminating |
| the three git-tracked first-hit JSONs | 0 of 68 | **0** | ⚑ every record is single-archive |

### ⚑ The sharpest single check

`monsterClassification` is the only field in the corpus that can change a monster's **tiering and roster band**. Across the union of all our roster populations (1,581 records) it flips on exactly **three** — and all three committed values are the Crucible value:

| record | base | **SurvivalMode** | **committed** |
|---|---|---|---|
| `boss&quest/zombiemutant_devilscrossing_01.dbr` | Quest | **Hero** | **Hero** ✓ |
| `boss&quest/zombiemutant_devilscrossing_01b.dbr` | Quest | **Hero** | **Hero** ✓ |
| `bounties/bl_bounty17.dbr` | Hero | **Quest** | **Quest** ✓ |

### The residual uncertainty, declared

⚑ **15 committed files carry DBR paths and NO archive-provenance column** — including the two 937-row tables (`pm4l_applied_damage_by_body.csv`, `pm4l_mitigation_by_body.csv`), `pm4_band_b_ehp_by_wave.csv` (791) and `t22_band_a_monster_stats.csv`. For these, provenance is not recorded and I tested them on the strongest value-level discriminator available (`bio_record`), which is weak — only 4 and 1 rows respectively discriminate. **Their precedence is `CORROBORATED-NOT-PROVEN`:** they are derived tables whose upstream instruments are the `pm4*` family, and every `pm4*` tool I enumerated is precedence-correct — but that is an inference from the producer, not a measurement of the product. **I did not find a stale value in them; I also could not decisively test most of their rows.**

---

## 5 · DOES IT REACH THE MONSTER ROSTER? (Q4) — YES, AND IT HELD

**Short answer: the exposure covers almost the entire roster, the correct precedence changes real combat values, and our committed data is on the correct side everywhere I could test.**

### 5.1 Population membership does not move

A record path either exists in an archive or it does not. **Precedence selects which copy, never whether the path exists.** Verified:

| population | n | in >1 archive | ⚑ first-hit **differs** | absent from all 8 |
|---|---|---|---|---|
| **466** — tier-16 rollable pool (`pe6_crucible_wave_pools_v2.csv`) | 466 | 460 | **460** | 0 |
| **790** — band-B defense limb (`pm4p_leech_resistance.csv`) | 790 | 767 | **764** | 0 |
| **791** — band-B eHP (`pm4_band_b_ehp_by_wave.csv`) | 791 | 768 | **765** | 0 |
| **937** — per-body applied damage / mitigation (`pm4l_*.csv`) | 937 | 908 | **905** | 0 |
| 968 — band-A monster stats (`t22_…`) | 968 | 961 | **961** | 1 |

⚑ **This is not the baton-versus-pool shape.** That defect changed *which population was enumerated*. This one cannot — it changes *which copy of each member is read*. The populations are stable; only the values could have moved.

### 5.2 But the values genuinely move — Crucible rebalances the monsters

On **1,350 of 1,401** roster records, at least one combat/stat field changes under precedence. The overwhelming majority of all changed fields are loot/XP/faction/cosmetic (28,280 instances vs 5,832 combat) — but the combat ones are not trivial:

| field | records affected | example delta |
|---|---|---|
| `distressCallRange` | 1,057 | **18.0 → 50.0** (aggro propagation radius, ~2.8×) |
| `distressCallGroup` / `distressCallTime` | 1,143 / 647 | `2000 → 5000` ms |
| `alertAnimChance` / `rallyAnimChance` | 1,082 / 1,093 | **30 → 0** |
| `skillLevel5` | 432 | `'(charLevel/25)+3'` → `'(charLevel/25)+1'` |
| `skillName2/3/6/…` | ~90 | `damagebase_physical04` → **`physical03`** (a different passive) |
| `characterRunSpeed` / `characterAttackSpeed` | 37 / 20 | `1.5 → 1.25` · `1.3 → 1.15` |
| `defensiveLife` / `defensiveFire` / `defensivePoison` | ~11 | resist deltas |
| ⚑ `monsterClassification` | 3 | Quest ↔ Hero |

On the **466** specifically: all 460 colliding records carry a combat/stat delta, led by `distressCallRange` (370), `alertAnimChance` (353) and `skillLevel5` (167).

**And the committed data took the Crucible side** — §4's `alertAnimChance` test (62/62), the `winner_archive` tests (407/407, 95/95), the pool provenance (1,560/1,560) and the three `monsterClassification` flips all point the same way.

### 5.3 ⚑ **Recommendation for the v3.4 cut: proceed. This is not an input.**

I found nothing that moves a pack value. The one qualification is § 4's residual: the two 937-row tables and the 791 table have no recorded provenance, and their correctness rests on their producers being precedence-correct rather than on a measurement of their rows. **If gandalf wants that closed rather than corroborated before the cut, the cheapest instrument is a provenance column, not a re-derivation** — see § 6.

---

## 6 · WHAT I RECOMMEND (steward's call, data domain)

Read-only constraint honored — these are recommendations, not changes.

1. ⚑ **Name the mode, not just the order.** Every precedence helper should take the mode as a required argument rather than defaulting. `arz.find()`'s `include_mods=False` default is a correct answer to a campaign question silently applied to Crucible questions. **A default is the wrong shape for a parameter whose right value depends on what is being asked.**
2. ⚑ **Make `winner_archive` a schema requirement, not a habit.** The files that carry it are the files I could test decisively; the 15 that do not are the residual uncertainty in this entire audit. Provenance columns are what made a clean verdict *provable* rather than *plausible* — that is a schema property worth mandating on every curated extraction.
3. **The 23 first-hit tools need no repair** — they are scratch instruments in a closed lineage whose three committed artifacts are clean. **But `lib_corpus.get()` should carry a header comment naming the defect**, because 17 importers is an inviting surface for reuse.
4. **The stub class is three masteries, not one.** Any future Inquisitor or Necromancer ledger has the identical trap.

---

## 7 · WHAT DID NOT CLOSE — Law 3 declarations

| question | state |
|---|---|
| The load order *among* the four SurvivalMode archives | ⚑ **`CONSISTENT-NOT-SOURCED`.** Exercised by 469 differing records; reproduces the engine pipeline's recorded winners on 407/407, but only 49 rows actually test it, and agreement between two tools sharing a convention is not independent evidence. No manifest on this host. |
| Whether the vendor tree the extractions ran against is byte-identical to the depot I censused | ⚑ **`UNDETERMINED-BY-EXECUTION`.** `~/Games/vendor/grim-dawn-*` does not exist on this host. Record counts match the 2026-07-23 probe exactly; that is corroboration of vintage, not proof of identity. |
| Precedence of the 15 no-provenance committed files (incl. both 937-row tables and the 791) | ⚑ **`CORROBORATED-NOT-PROVEN`.** Every enumerated `pm4*` producer is precedence-correct; the products themselves are only weakly testable (4 and 1 discriminating rows). No stale value found; most rows untestable. |
| Whether `/tmp/d12/pm4t_arz_2026_08_14.py` matched the repo copy | ⚑ **`UNVERIFIABLE`.** The path no longer exists. The 5 consumers were classified against the repo copy. |
| Whether the `basis` free-text column in the no-provenance files names the winning archive per row | **NOT INSPECTED** — not every row was read. |

---

## 8 · REPRODUCTION

All census scripts are read-only and were run from the session scratchpad, not committed — they import legolas's `scratch/2026-09-21-s1-bio/arz.py` unmodified and add only set arithmetic over the record-name tables. The findings above are all counts and field diffs derivable from `/Users/admin/depots/` plus the committed CSVs named inline; nothing requires re-running a seam tool.

**Primary:** `/Users/admin/depots/` — 8 `.arz`, read-only, 2026-09-21.
**Committed data tested:** `reincarnated-engine/data/kc2/{pm4i_band_c_roster,pm4o_oa_da,pe6_crucible_wave_pools_v2,d1_alert_anim,t22_band_a_monster_stats,pm2_tg2_monster_oa_da,pm4m_body_chain,pm4l_*,pm4_band_b_ehp_by_wave,pm4p_leech_resistance,kc2_s1_banda_record_inputs}.csv`
**Internal:** legolas `findings/2026-09-21-{s1-save-bio-block,c2-per-cast-energy-costs}.md`; `simulation/kc2/fixture.py`.

**Filed by:** elrond, 2026-09-21. Read-only throughout. No tool in another seam was modified.
