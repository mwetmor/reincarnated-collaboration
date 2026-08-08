# KC2 — Edition-III intake + II→III record-granularity diff

**Agent:** legolas (UNKNOWN-RESEARCHER)
**Date:** 2026-08-08
**Commission:** KC2-SIM run, fold L-59, from gandalf (RUN-CONDUCTOR)
**Status:** IN PROGRESS — appended live
**Attribution grade tags:** R-KC2-7 (MEASURED / INFERRED / MODELED)

> ### ⚠ CORRIGENDA-FORWARD BANNER — added 2026-08-08 under ruling R-L64-3. Nothing below is struck or rewritten.
>
> | # | site | what is wrong | what is right | authority |
> |---|---|---|---|---|
> | C-1 | **§ a.7 HEADER** (`"8 CHANGED / 8 IDENTICAL (of the 16 shared)"`) | the count | **9 DIFFER / 7 IDENTICAL** | a.7's own TABLE (9 = 7 `.arz` + base/gdx3 `Text_EN`; 7 = `sm2.arz` + 6 `Text_EN`); jack-ryan's independent L-60(b) re-hash; his L-62(c) re-verification. Majority of independent measurement, 3 : 1. |
> | C-2 | **§ a.7 closing prose, line 214** (`"It is 8 of 16."`) | the same count, second site | **It is 7 of 16.** | as C-1. Header-only repair would have left this standing — the widened scope is jack-ryan's L-62(e) catch. |
> | C-3 | **instrument `kc2set_verdicts.json`** | 6 rows report `ABSENT-BOTH` from unresolved path-guesses, not from absence | all 6 resolve and are **IDENTICAL**. **The note's `15/15 summon bodies` claim was CORRECT; the ARTEFACT was stale.** | jack-ryan L-62(d) found 2 (`fleshshaper_spirit_01`, `krieg_aethertrap` → `…/bossskills/pets/`); this touch's re-emit found 4 more (`swampcrab_h05`, `aetherialcorruption_h05` → `…/hero/`; `swampcrab_crabgenerator`, `springscrab_crabgenerator` → `…/summoning/`). **Superseded by `kc2set_verdicts_v2.json`** (613 IDENTICAL / 5 CHANGED / 9 genuinely ABSENT; equality predicate declared in-file per Discipline #69 clause (i)). v1 retained for lineage. |
> | C-4 | **§ c.1** (`averagePlayerLevel = 100 CONFIRMED`) | the value, and the inference that produced it | **`averagePlayerLevel` ∈ [103.0, 103.92)** — DERIVED. The `108 = 103 + 5` reading was arithmetically valid but rested on the record `charLevel` additive offset entering the spawn level, which is now MEASURED-FALSE (below). | `2026-08-08-kc2-consolidated-record-touch.md` § 4–5 |
> | C-5 | **§ c.5 / the NAMED BLOCK B-KC2-C1** (`×2.7181 unexplained residual`) | the framing, not the arithmetic | **No residual exists.** The stack is **additive-within-field**: Σ = 580 (difficulty) + 308 (survival w152) + `armorbase0N.characterLifeModifier[charLevel−1]`. At charLevel 108 → Σ = 1009 % → **×11.0900 EXACT**. `×2.7181` was the artefact of dividing by a `×4.08` that never multiplied. **B-KC2-C1 is CLOSED, not merely unblocked.** | same note, § 3 |
> | C-6 | **§ d falsifiable prediction** (`Rotmouth's plate must read 109 or 110`) | the prediction (registered, falsified — as designed) | plate reads **107**, MEASURED 7/7 (galadriel). The identity join (`hero/basilisk_h02.dbr`, w152 sp = 2, `poolsherogdx1/basilisk_hero`) **STANDS**; the failed link is the **offset**. | same note, § 5 |
>
> Everything else in this note stands as filed, including every § b diff verdict (independently reproduced by jack-ryan at L-62(c)).

## Commission parts

- (a) INTAKE — SHA-256 pin + inventory of the 38-file Edition-III tree; reconcile vs `depot.pins.predicted.txt`; independently re-verify Edition-II 16/16
- (b) II→III RECORD-GRANULARITY DIFF on the KC2-dependent set
- (c) PAIR-SEAT CHECK (Edition-II records; fixture explanation) — re-seat the Δ1.752 % pair after galadriel's plate read falsified `p04 = Carraxus`
- (d) `Rotmouth` resolution (orange→hero, w152 t≈704.47)

---

## WORK LOG

(appended live below)

## PART (a) — EDITION-III INTAKE (SHA-256 pin + inventory)

**Status: COMPLETE.** Grade: **MEASURED** (SHA-256 computed by me this session against the
resident tree; no value taken on report).

### a.1 Corpus identity

| field | value |
|---|---|
| tree | `/Users/admin/Games/vendor/grim-dawn-edition-III-20260808/` |
| data files | **38** (confirms Matt's count) |
| total data bytes | **3,646,927,935** = 3.40 GB (confirms Matt's 3.4 GB) |
| non-data files present | `depot.pins.predicted.txt` (1,357 B), `.DepotDownloader/` (14 manifests + 14 `.sha` + `depot.config`) |
| buildid | 24619876 (per predicted-pins header; PICS-sourced, not independently re-read by me — **INHERITED**) |
| patched | 2026-08-07T19:33:54Z (same provenance — **INHERITED**) |

**Improvement over Edition-II:** Edition-III **retains the `.DepotDownloader/*.manifest`
binaries**. Edition-II did not (cut record § 8 flags the fetch transcript as "currently the
only Edition-II version pin"). Edition-III's version pin is now **self-contained in the tree**
— the manifest ID is recoverable from the corpus itself without an external transcript. This
closes the single-point-of-failure noted at the Edition-II cut.

### a.2 Manifest-pin reconciliation vs `depot.pins.predicted.txt` — 8/8 CONFIRMED

Matt's pre-fetch prediction table was registered *before* the fetch (prediction test, not
description). Reconciled against the manifest filenames DepotDownloader wrote on disk:

| depot_id | predicted manifest | on-disk manifest | verdict |
|---|---|---|---|
| 219991 (base) | 8441812226096803528 | 8441812226096803528 | ✅ MATCH |
| 483840 (survivalmode) | 843586781480686150 | 843586781480686150 | ✅ MATCH |
| 642280 (gdx1 / AoM) | 4481705397278971242 | 4481705397278971242 | ✅ MATCH |
| 642281 (survivalmode1) | 789766979280218767 | 789766979280218767 | ✅ MATCH |
| 897670 (gdx2 / FG) | 6512697996754910669 | 6512697996754910669 | ✅ MATCH |
| 897671 (survivalmode2) | 2984427886892515994 | 2984427886892515994 | ✅ MATCH (and unchanged from Ed-II, as predicted) |
| 2699230 (gdx3 / FoA) | 3421000675863911201 | 3421000675863911201 | ✅ MATCH |
| 2699231 (survivalmode3) | 6967883975494022349 | 6967883975494022349 | ✅ MATCH |

**8/8. Matt's 8/8 score is independently CONFIRMED** (MEASURED — read off the on-disk
manifest filenames, which DepotDownloader derives from the CDN response, not from the
prediction file).

Six additional non-data depots also landed manifests (228983/4/5/6, 228990, 229003) — these
are the 0-byte/non-data depots the Edition-II record already classified. Pins recorded in
a.5 for completeness; they contribute no files to the tree.

**Also verified: the manifest-pin premise itself, a second time.** Depot 897671
(survivalmode2) carries manifest `2984427886892515994` in BOTH Edition-II and Edition-III.
Prediction: identical manifest ⇒ identical bytes. **Result: `SurvivalMode2.arz` SHA-256
`940e4034…` in both editions — IDENTICAL.** This is the second independent live test of the
"manifest ID is a content identifier" claim (Edition-II tested it 11/11 across a 24-hour
window; Edition-III tests it across a 15-day window and a full game patch). The pin holds.

### a.3 Full 38-file inventory — path | bytes | SHA-256

```
database/database.arz                          58543495   2ad6d379285cfb745462316949e8d59e9450cb58a13f9ffa2fdeb70193183bfd
database/templates.arc                           793541   679db83f019020ef7d4d27be8e61203006ee94e5c582dd8a59642f3fddd54602
gdx1/database/GDX1.arz                         42427625   431e64e1d372e4ebee5d1048d3aca458923e1df8c97844274636f5373a01e292
gdx1/resources/Creatures.arc                  260602996   c6d03e7f7262ac10b91191a7546a22fe8b3622bd39703937c8c5b00181f2b6be
gdx1/resources/Levels.arc                     307082344   56ebce469604ae68b9f852cca9de653e33ea4e7564e238629c36640ded65441a
gdx1/resources/Scripts.arc                       231213   9c8a858e2c396c3097951e47a1bc27f042b87070a16ad2a3b42e691894d121af
gdx1/resources/Text_EN.arc                       195871   85baef4bd2a44eadadbb779c409cfa5238c4b4de2ce5182cb2ed9cf32797093a
gdx2/database/GDX2.arz                         33117410   13fa0b93be15835958968ad672b9efa5159d7221a279aca791590390dd81a072
gdx2/resources/Creatures.arc                  337186096   61d0145d4f6e090be92d8317242a061ede287956dd4ca9163c7d52d07d8c585b
gdx2/resources/Levels.arc                     497414784   4d7e9dad9906820fd50b558e5b33d1250ba3a035415ac14a13df1b9cc76bfcfb
gdx2/resources/Scripts.arc                       178004   ef92db11fb04f2a5a3b384f96807a42e0a3628699c01c7bc6d5fc4f785fa85dd
gdx2/resources/Text_EN.arc                       237800   8aec9207b5dd0b33cb981455ec867d71ebc0d1646fa27e85b59b4556e8d814a1
gdx3/database/GDX3.arz                         47552036   e990e1265f14ff2ee241658433d4d666d399a5b0be27543ae9481fc97d6a2ae4
gdx3/resources/Creatures.arc                  656307665   c53c7e87af854360d33b0243667391d3dddb94e4b7faa31545a8f251fa140b64
gdx3/resources/Levels.arc                     653107915   a70407dcc2731c0a66ffee778b6bf8ddf7a77e61dc85cb01f79df51407d4297c
gdx3/resources/Scripts.arc                       290351   73231b4f3e11e7da446c06ad033379041e0e4c2c9c140bc14890f10b783dbd7a
gdx3/resources/Text_EN.arc                       191439   001b87bd0c52ac210ebf5fab42f94aef11ee68130b384776144de6443088dc08
mods/survivalmode/database/SurvivalMode.arz     7052806   e9f6e2213eada8f5ffcc4fc430395b43c95384b745b629def096dbb2e7da29b6
mods/survivalmode/resources/Creatures.arc       6129791   087f0d4727c0c3704424f10b6e4159dba908af64af4a8ea8e7dd25417b1eb1da
mods/survivalmode/resources/Maps.arc            9738368   5377259861ad5c17a6009ae045ebc94612faca9a65bc14904b193b9c6d4fa708
mods/survivalmode/resources/Scripts.arc           72984   47e6426d9534e0ddd5f867ca4d2640e5aa42cc8ffd68baa1db7e8870a61fb009
mods/survivalmode/resources/Text_EN.arc            7787   fa0689778ef0badb4472213684733e958edfbeeebb45086830939c9693b3d06e
resources/Creatures.arc                       460978144   bdafb01070fed09d27976813f8520fa04d98d756376701fd068ccfc6bb1de07c
resources/Levels.arc                          221750903   721ef6f350c17f6c626c9a525b8bdded45776a919b8acaeb65ff5345f8d61fd0
resources/Scripts.arc                            287114   323b46deb08abfe41f3b86d3652777fc1f3f6f586b7579fde46d50d8270df672
resources/Text_EN.arc                            471514   1105b1eef70c83914a00d0516ea6db3a25ed06fad8ec91757481e66879d58a27
survivalmode1/database/SurvivalMode1.arz        2464736   6ac10d6180bfa8491edfc89946d1cfbf166c5ca6442c5862ecf6947290021252
survivalmode1/resources/Maps.arc               14976494   2f5b34fe914e26d6fadda88aebd4080d172dc92b8d66ac990c3e108e05821237
survivalmode1/resources/Scripts.arc               33853   27d0c258d1b6dc6017d1b0e68385a67913f73e019196aaeb7f81c28b40f52278
survivalmode1/resources/Text_EN.arc                2261   af9d87ce5cc72629ffb970aa8e6a06e2cdf1b0fd0bf6dd0dcd3e32244430a694
survivalmode2/database/SurvivalMode2.arz        2351568   940e40344e9dde53bfac8ff6576940d52ebfece600adeabe3774f9f0c3071e95
survivalmode2/resources/Maps.arc                3104975   cef96030be9bdc9be64bf187389aeccec6552ba1cfde30d1c63d716d2f6dbaec
survivalmode2/resources/scripts.arc                2048   8269f89cc6eda34847e8839722767f11a3ac66210a198bc5b82e65823a3c824f
survivalmode2/resources/text_en.arc                2048   8269f89cc6eda34847e8839722767f11a3ac66210a198bc5b82e65823a3c824f
survivalmode3/database/SurvivalMode3.arz        3922410   e848791e4b15496670e4c78832075d9868e7b502e6eed93715c24e894902e12a
survivalmode3/resources/Maps.arc               18082354   94e20abadfce0f92d5187ab20bb8a9510fca9163e2b5b67b038cb55953f34911
survivalmode3/resources/Scripts.arc               32973   2c376262c0969eb247af46fb88047a02ac1e24447d291f7d3a3e438934c0ed6b
survivalmode3/resources/Text_EN.arc                2219   6336cde2568712253eb21020732421a4a8d417fd92eab60a2f6f86c606927524
```

**Inventory anomaly worth flagging (not an error, but a trap):**
`survivalmode2/resources/scripts.arc` and `survivalmode2/resources/text_en.arc` are BOTH
2,048 bytes with the **identical SHA-256** `8269f89c…`. These are empty-`.arc` stubs
(same header, no payload) — the depot ships placeholder archives. Anyone diffing by hash
alone will see a spurious "duplicate file" signal here. Both are also the *lowercase*
filenames that caused the Edition-I coverage gap (cut record § 5); Edition-III now carries
both, and this intake used a case-blind `find -type f` with **no name filter at all**, so the
coverage-boundary hazard (discipline D-a) does not recur.

### a.4 Edition-III is NOT a superset-by-count of Edition-II — it is a different SHAPE

Edition-II held 16 data files: 8 `.arz` + 8 `Text_EN.arc`. Edition-III holds 38: the same
8 `.arz` + 8 `Text_EN.arc`, **plus 22 asset/script archives that Edition-II never fetched**:

| new-in-Edition-III class | files | note |
|---|---|---|
| `**database/templates.arc**` | 1 (793,541 B) | **THE TEMPLATE LAYER — now resident.** Blocker on the Part-C/Part-B derivation chain is lifted. See § b.6. |
| `*/resources/Creatures.arc` | 4 (base, gdx1, gdx2, gdx3, +survivalmode) — 5 | 1.72 GB — model/animation assets |
| `*/resources/Levels.arc` | 4 | 1.68 GB — level geometry |
| `*/resources/Maps.arc` | 4 (survivalmode ×4) | Crucible map payloads |
| `*/resources/Scripts.arc` | 7 | Lua/engine scripts |

So the II→III relation is **not** "same files, some changed." It is "same 16 files (8 changed,
8 identical) **plus** 22 files Edition-II never had." Any statement of the form "Edition-III =
Edition-II + patch" is wrong on the file axis. It is *both* a patch *and* a scope widening.

### a.5 Non-data depot pins (recorded for completeness)

`228983 → 8124929965194586177` · `228984 → 2547553897526095397` ·
`228985 → 3966345552745568756` · `228986 → 8782296191957114623` ·
`228990 → 1829726630299308803` · `229003 → 8740933542064151477`

### a.6 EDITION-II RE-VERIFICATION — 16/16 UNTOUCHED, INDEPENDENTLY CONFIRMED

Re-computed SHA-256 over all 16 Edition-II data files this session and compared against the
pinned values in the Edition-II cut record (`2026-07-24-gd-edition-II-cut-record.md` § 4 for
the 5 new-in-II files; the Edition-I freeze table via that record's § 3 for the other 11).

| file | pinned SHA-256 | recomputed | verdict |
|---|---|---|---|
| `gdx3/database/GDX3.arz` | `1661be5e…30dcf0` | `1661be5e…30dcf0` | ✅ |
| `gdx3/resources/Text_EN.arc` | `d6e7f781…0d1f18` | `d6e7f781…0d1f18` | ✅ |
| `survivalmode3/database/SurvivalMode3.arz` | `b4aa2d78…03af7e` | `b4aa2d78…03af7e` | ✅ |
| `survivalmode3/resources/Text_EN.arc` | `6336cde2…927524` | `6336cde2…927524` | ✅ |
| `survivalmode2/resources/text_en.arc` | `8269f89c…3c824f` | `8269f89c…3c824f` | ✅ |
| other 11 (base, gdx1, gdx2, sm, sm1, sm2 `.arz` + `Text_EN.arc`) | Edition-I freeze table | all match | ✅ |

**16/16 UNTOUCHED — CONFIRMED (MEASURED, independent recomputation).** Matt's report holds.
Edition-II remains a valid, unmoved substrate for the two fixture sittings.

Full Edition-II recomputed table (for the record):
```
8cdeff128422c765278087b7e4f95a41b59be8ee51184370d139c451afb5ae3f  database/database.arz
613457c8df72fe5a16de88def05dd00f518cf4e61c14cf375ef2ccab6dbd6e01  resources/Text_EN.arc
b4aa2d78675c4f05f92988e5c524ff9874a13984700484656a10b0578b03af7e  survivalmode3/database/SurvivalMode3.arz
6336cde2568712253eb21020732421a4a8d417fd92eab60a2f6f86c606927524  survivalmode3/resources/Text_EN.arc
e28ab2515477ac80bdc3f955b6aa804eee791d4c51fda64c9ea01306522a4539  gdx1/database/GDX1.arz
85baef4bd2a44eadadbb779c409cfa5238c4b4de2ce5182cb2ed9cf32797093a  gdx1/resources/Text_EN.arc
940e40344e9dde53bfac8ff6576940d52ebfece600adeabe3774f9f0c3071e95  survivalmode2/database/SurvivalMode2.arz
8269f89cc6eda34847e8839722767f11a3ac66210a198bc5b82e65823a3c824f  survivalmode2/resources/text_en.arc
1661be5ef6db1f0805cba4929d7d50bf13cbdc983c1b4413f6016a5ef330dcf0  gdx3/database/GDX3.arz
d6e7f7810ab251e3ad9e0dcf87e22d0af8f7d1611c02e1be4d431c44fd0d1f18  gdx3/resources/Text_EN.arc
6df94d3be33e600c737634bc8fcf1949a4b51d349677c7404b98c44ce2da6e5a  survivalmode1/database/SurvivalMode1.arz
af9d87ce5cc72629ffb970aa8e6a06e2cdf1b0fd0bf6dd0dcd3e32244430a694  survivalmode1/resources/Text_EN.arc
f6d5bd67602ce5af2de394507c36f198a9388be26350517434e7ff5e4ee1e985  gdx2/database/GDX2.arz
8aec9207b5dd0b33cb981455ec867d71ebc0d1646fa27e85b59b4556e8d814a1  gdx2/resources/Text_EN.arc
e55b760f36ab80a6ad16fd34f3f8ca76e1cde55ee6160d72eb574c01221405f2  mods/survivalmode/database/SurvivalMode.arz
fa0689778ef0badb4472213684733e958edfbeeebb45086830939c9693b3d06e  mods/survivalmode/resources/Text_EN.arc
```

### a.7 FILE-LEVEL II→III DELTA — 8 CHANGED / 8 IDENTICAL (of the 16 shared)

> **⚠ CORRIGENDUM C-1 (2026-08-08, R-L64-3) — this header count is WRONG. It is 9 DIFFER / 7 IDENTICAL.**
> The header is left standing per corrigenda-forward; the TABLE BELOW is correct and is the record.
> Second site of the same slip: the closing prose at "It is 8 of 16" (→ corrigendum C-2). See the banner at the top of this note.

| path | Edition-II | Edition-III | verdict |
|---|---|---|---|
| `database/database.arz` | `8cdeff12…` | `2ad6d379…` | **CHANGED** |
| `gdx1/database/GDX1.arz` | `e28ab251…` | `431e64e1…` | **CHANGED** |
| `gdx2/database/GDX2.arz` | `f6d5bd67…` | `13fa0b93…` | **CHANGED** |
| `gdx3/database/GDX3.arz` | `1661be5e…` | `e990e126…` | **CHANGED** |
| `mods/survivalmode/database/SurvivalMode.arz` | `e55b760f…` | `e9f6e221…` | **CHANGED** |
| `survivalmode1/database/SurvivalMode1.arz` | `6df94d3b…` | `6ac10d61…` | **CHANGED** |
| **`survivalmode2/database/SurvivalMode2.arz`** | `940e4034…` | `940e4034…` | **IDENTICAL** |
| `survivalmode3/database/SurvivalMode3.arz` | `b4aa2d78…` | `e848791e…` | **CHANGED** |
| `resources/Text_EN.arc` (base) | `613457c8…` | `1105b1ee…` | **CHANGED** |
| `gdx3/resources/Text_EN.arc` | `d6e7f781…` | `001b87bd…` | **CHANGED** |
| `gdx1/resources/Text_EN.arc` | `85baef4b…` | `85baef4b…` | **IDENTICAL** |
| `gdx2/resources/Text_EN.arc` | `8aec9207…` | `8aec9207…` | **IDENTICAL** |
| `mods/survivalmode/resources/Text_EN.arc` | `fa068977…` | `fa068977…` | **IDENTICAL** |
| `survivalmode1/resources/Text_EN.arc` | `af9d87ce…` | `af9d87ce…` | **IDENTICAL** |
| `survivalmode2/resources/text_en.arc` | `8269f89c…` | `8269f89c…` | **IDENTICAL** |
| `survivalmode3/resources/Text_EN.arc` | `6336cde2…` | `6336cde2…` | **IDENTICAL** |

**Matt's FINDING B is CONFIRMED and SHARPENED.** Restated precisely:
- Among the **8 `.arz` databases: 7 CHANGED, 1 IDENTICAL** (`SurvivalMode2.arz` alone). Matt's
  "only SurvivalMode2.arz identical" is exactly right *as a statement about `.arz` files*.
- Among the **8 `Text_EN.arc` localization archives: 2 CHANGED (base, gdx3), 6 IDENTICAL.**
  Matt named both changed ones correctly.
- **The sharpening:** Matt's phrasing could be read as "only 1 of 16 identical." It is 8 of 16.
  > **⚠ CORRIGENDUM C-2 (2026-08-08, R-L64-3) — WRONG at this second site. It is 7 of 16.** Left standing per corrigenda-forward; see the banner at the top of this note. The sharpening's *point* (many-more-than-one identical) is unaffected.
  The six unchanged localization archives matter for Part (d) — the `Rotmouth` tag-join is
  reproducible on gdx1/gdx2/sm/sm1/sm2/sm3 text across BOTH editions, and only base + gdx3
  text carry edition-skew risk.


---

## PART (b) — II→III RECORD-GRANULARITY DIFF

**Status: COMPLETE, and wider than commissioned.** Rather than diff only the named
KC2-dependent set, I ran a **full record-level diff of all 84,663 shared `.dbr` records**
across the 8-archive overlay in both editions (39 s runtime — the cost of completeness was
negligible, and it converts every "not in my set" from an assumption into a measurement).

Instrument: `agentic_orchestration/legolas/scratch/2026-08-08-kc2-ed3-diff/`
(`lib2.py` dual-edition overlay resolver · `fulldiff.py` · `kc2set.py` ·
`fulldiff_summary.json` · `fulldiff_detail.json` · `kc2set_verdicts.json` · `tpl_changed.json`).
Method: last-wins field merge across the 8-archive stack per edition, then field-by-field
compare with float normalization to 6 dp.

### b.0 HEADLINE — the corpus barely moved, and it did not move where KC2 lives

| measure | value |
|---|---|
| shared records | 84,663 |
| **IDENTICAL** | **83,605 (98.75 %)** |
| **CHANGED** | **1,058 (1.25 %)** |
| **NEW in Edition-III** | **166** |
| **REMOVED in Edition-III** | **0** |

Changed records by top-level namespace:
`skills 656 · items 216 · creatures 54 · sounds 41 · interactive 29 · proxies 25 ·
endlessdungeon 12 · fx 7 · ui 6 · game 5 · level art 4 · controllers 3`

### b.1 PER-RECORD VERDICT TABLE — the commissioned KC2-dependent set

| # | set member | records checked | IDENTICAL | CHANGED | verdict |
|---|---|---:|---:|---:|---|
| **1** | **SurvivalMode3 tier-16 wave/pool/spawn tables (global w151–160)** | 54 (`records/proxies/tier16waves/*`) + 1 tier-16 spawn entity | **55** | **0** | ✅ **ALL IDENTICAL** |
| **2** | **w151–158 pool proxy records** (from `pe6_crucible_wave_pools_v2.csv`) | 90 | **90** | **0** | ✅ **ALL IDENTICAL** |
| **2** | **w151–158 rostered monster records** | 429 | 426 | **3** | ⚠ 3 CHANGED — see b.2 |
| **2b** | **summon bodies** (crabling, springscrab summon, spikeshell, stoneshell, skeletal archer `skeleton_a02_summon`, apparition `ghost_a01_summon`, traps, aetherial corruptions, colossus, fleshshaper spirit, krieg aethertrap) | 15 | **15** | **0** | ✅ **ALL IDENTICAL** |
| **3** | **survival scalar arrays** — `balancingadjustment_survivalmode_enemies01/02/03` (+ their `backup/` and `copy of` twins) and every other `balancingadjustment*` record in the corpus | 21 | 19 | **2** | ✅ the three **survivalmode** arrays are IDENTICAL; the 2 changed are NOT survival — see b.3 |
| **4** | **proto bios** (every `bio_*` / `*/bios/*` record corpus-wide) | **808** | **808** | **0** | ✅ **ALL IDENTICAL — zero bios moved** |
| **4** | **levelVarianceEquations** | — | — | — | Not a record; it is a **field**, governed by `proxylevelvarianceequation.tpl` — see b.6 |
| **5** | **L-58 mechanism chains** — `hero/swampcrab_h01…h05`, `hero/springscrab_h01…h04`, `boss&quest/swampcrab_ugdenbog_01` (Carraxus), `carraxus_summonswampcrabc`, `swampcrab_crabgenerator`, `springscrab_crabgenerator`, `skeletalgolem_b01`, `skeletalgolem_b01_summon`, `skeletalgolem_c01`, `poolsherogdx1/aetherialcorruption_hero`, `hero/aetherialcorruption_h01…h05` | 30+ | **all** | **0** | ✅ **ENTIRE CHAIN IDENTICAL** |
| **6** | **TEMPLATE layer** (`templates.arc`, 819 templates) | 819 | **811** | **8** | ✅ 8 changed are **purely additive**; every KC2-relevant template IDENTICAL — see b.6 |

**Path-resolution note (method honesty).** My first pass at set (5) guessed paths
(`records/creatures/enemies/swampcrab_h01.dbr`) and got `ABSENT-BOTH` on 13 of 17. The records
live at `records/creatures/enemies/**hero/**swampcrab_h01.dbr`,
`records/skills/nonplayerskillsgdx1/**summoning/**swampcrab_crabgenerator.dbr`, etc. I re-resolved
by corpus search rather than reporting the absences. Recorded because an `ABSENT` returned from a
guessed path is **not** evidence of absence — it is evidence of a bad path, and the two are
trivially confusable in a verdict table.

### b.2 CHANGED-RECORD VERDICTS — what re-derivation each forces

Three of the 429 w151–158 rostered monster records changed. **None of them touches w152 or w157.**

**(i) `records/creatures/enemies/bounties/ku_bounty_07.dbr` — appears at w153 and w167.**
> **Re-derivation forced: NONE for the two fixture waves; a NAMED CAVEAT on w153 only.** This is
> a gdx3 Kurn bounty body. The fixture sittings scored w152 and w157; w153 is not a scored wave in
> either sitting. **Any future Edition-III-scoped w153 composition claim must re-read this record**
> — an Edition-II-derived w153 roster row is now version-skewed by exactly one member. Nothing
> already banked depends on it. (Its twin `ku_bounty07.dbr`, no underscore, also changed and is
> not in the w151–158 roster at all.)

**(ii) `records/creatures/enemies/nemesis/nemesis_beast_02.dbr` — w154 + 15 later waves
(160, 170, 171, 175, 180, 185, 187, 188, 190, 192, 195, 196, 198, 199, 200).**
**(iii) `records/creatures/enemies/nemesis/nemesis_eldritch_02a.dbr` — w154 + 8 later waves.**
> **Re-derivation forced: NONE for w152/w157. A REAL and BROAD obligation above w160.** Both are
> nemesis bodies. They are absent from w152 and w157 rosters entirely, so the fixture explanation
> is untouched. But they are members of **sixteen** and **nine** waves respectively across the
> 151–200 band, concentrated in the 170–200 tail. **Any Edition-III-scoped statement about the
> nemesis-bearing waves (170/171/180/190/195/196/198/199/200) must re-derive from Edition-III**,
> not carry an Edition-II row forward. This is the single largest re-derivation obligation the
> diff produces, and it lands entirely *outside* the KC2 fixture band.

**(iv) `records/controllers/factions/faction_aetherial.dbr` — CHANGED, one field.**
> ```
> nemesisSpawn  II : (…/nemesis_aetherial_01.dbr, …/nemesis_aetherialvanguard_01.dbr)
>              III : (…/nemesis_aetherial_01.dbr, …/nemesis_aetherialvanguard_01b.dbr)
> ```
> **Re-derivation forced: NONE — but this is the record that nearly poisoned the L-58 sweep.**
> The `_01b` variant is one of the 166 new-in-III records. My a1 broad sweep was *rejected* in the
> join note precisely because it followed `factions → faction_aetherial.dbr → nemesisSpawn → …`
> and thereby attached the Aetherial Vanguard's crystal summon to every Aetherial-faction monster
> in the band. **The strict sweep — `skillName{i}` edges only — does not traverse this field, so
> the L-58 mechanism table is immune to this change.** Had the broad sweep been the sweep of
> record, this diff would now be forcing a full re-derivation of every Aetherial monster's add
> budget. The methodological correction made in the join note is what buys the immunity; that is
> worth naming, because it is the second time the faction-table edge has tried to contaminate
> this lane.

**(v) `records/game/gamefactions.dbr` — `nemesisRespawnKillModifier` 4.0 → 1.5.**
> **Re-derivation forced: NONE for Crucible.** This governs campaign nemesis respawn cadence
> (kills required between respawns). Crucible nemesis appearances are wave-table-driven, not
> respawn-driven. **Caveat for G-STATS:** if any forward stat reads campaign nemesis encounter
> *rate*, that rate is now 2.67× faster in Edition-III and an Edition-II-derived figure is wrong.

**(vi) `records/game/gameengine.dbr` — one field ADDED: `superBossDisableToken` (string).**
> **Re-derivation forced: NONE.** Purely additive; no existing field moved. Pairs with the new
> `gameengine.tpl` variable (b.6) and the `superBossSpawnModifier` addition in
> `ascendantaltarformula.tpl` — this is the Asterkarn super-boss opt-out plumbing.

**(vii) `records/game/balancingadjustment_ultramode_enemies01.dbr` — one field ADDED:
`characterPercentHealIncreaseModifier`.**
> **Re-derivation forced: NONE for KC2.** Ultra mode is the gdx3 difficulty, not Crucible.
> Additive.

**(viii) `records/endlessdungeon/difficultyscaling/balanceadjustment_04.dbr` —
`characterPercentHealIncreaseModifier` array rebased from `(25,25,25,25,25,24,22,21,20,18,…)`
to `(0,0,0,0,0,−1,−3,−4,−5,−7,…)` — a uniform −25 shift.**
> **Re-derivation forced: NONE for KC2 (Shattered Realm ≠ Crucible).** Flagged because the
> −25 rebase is exactly the size of the field that was newly *added* to `ultramode` in (vii): the
> patch moved a flat +25 % enemy heal-increase out of SR shard-4 scaling. Any SR-scoped sustain
> figure carried from Edition-II is now wrong by 25 points.

### b.3 THE ONE THAT MATTERS MOST — and it is NOT the survival array

**`records/game/balancingadjustment_survivalmode_enemies03.dbr` — IDENTICAL.**
Verified at field granularity, not by hash: **627 fields, 27 of them 200-entry wave-indexed
arrays, every one array-equal, whole-record `II == III` → `True`.** This includes
`characterLifeModifier` (the 200-entry wave-indexed life array named in the commission),
`characterOffensiveAbility`, `characterDefensiveAbility`, `spawnMinAdj`/`spawnMaxAdj`,
`spawnChampionMinAdj`/`spawnChampionMaxAdj`, and the full offensive/retaliation set.
`…_enemies01` and `…_enemies02` likewise IDENTICAL, as are the `records/game/copy of …` and
`records/game/06-10-26 backup/…` twins. Sample of the shared array (index → value):
`[0]=95 · [50]=113 · [150]=306 · [151]=308 · [152]=310 · [157]=320 · [199]=990`.

**Player counterpart: `balancingadjustment_mp+difficulty_players01.dbr` — IDENTICAL.**
**Pet counterpart: `balancingadjustment_mp+difficulty_pets01.dbr` — IDENTICAL.**

**The enemy counterpart CHANGED, in exactly one field:**
```
records/game/balancingadjustment_mp+difficulty_enemies01.dbr
  offensivePhysicalModifier
    II  : (  0,   0,   0,   0, 0, 0, 0, 0, 0, 0, 0, 0)
    III : (-10, -10, -10, -10, 0, 0, 0, 0, 0, 0, 0, 0)
```
> **Re-derivation forced: NONE for any HP/eHP/composition claim. A NAMED OBLIGATION for any
> incoming-physical-damage claim.** Twelve slots, first four moved from 0 to −10. Zero defensive,
> zero life, zero spawn-count fields moved. **Every KC2 result that is about how many bodies
> spawn, what tier they are, or how much HP they have is untouched.** Any KC2 or G-STATS figure
> that is about *enemy physical damage output* in the first four slots of this table is
> version-skewed and must be re-read from Edition-III.
> **NAMED BLOCK — not estimated:** I have **not** established what the 12 slots index
> (difficulty × player-count is the standing hypothesis, not a measurement), so I cannot say
> whether solo-Gladiator Crucible reads slot 0–3 or slots 4–11. Resolving that requires the
> `mp+difficulty` indexing convention, which I did not probe. **Do not assume the −10 applies
> to Matt's solo runs, and do not assume it does not.**

### b.4 VERDICT — Edition-II KC2 results CARRY FORWARD

Per the commission's own logic (records IDENTICAL ⇒ Edition-II results carry forward MEASURED):

> **The entire KC2 fixture-explanation substrate for w152 and w157 is byte-identical between
> Edition-II and Edition-III.** 55/55 tier-16 wave tables, 90/90 pool proxies, 426/429 rostered
> monsters (3 exceptions all outside w152/w157), 15/15 summon bodies, 808/808 proto bios,
> 3/3 survivalmode scalar arrays, and the complete L-58 mechanism chain.
>
> **No blanket re-derivation. No targeted re-derivation either, for w152/w157.**

Named obligations produced, in priority order:
1. **Nemesis-bearing waves 170–200** — `nemesis_beast_02` + `nemesis_eldritch_02a` changed;
   re-derive before any Edition-III claim about those waves. *(largest)*
2. **Enemy physical-damage figures** — `balancingadjustment_mp+difficulty_enemies01`
   `offensivePhysicalModifier` slots 0–3; indexing convention is a NAMED BLOCK.
3. **w153 composition** — `ku_bounty_07` changed. *(narrow; w153 not a scored fixture wave)*
4. **Campaign nemesis respawn rate** — `nemesisRespawnKillModifier` 4.0 → 1.5.
5. **Shattered Realm shard-4 sustain** — `characterPercentHealIncreaseModifier` −25 rebase.

Items 4 and 5 are outside KC2 entirely and are recorded for G-STATS, which reads Edition-III.

### b.5 WHAT THE PATCH ACTUALLY WAS (context for the conductor)

The 166 new records and 1,058 changed records describe the patch plainly: gdx3/Asterkarn content
work (Kurn chieftain/shaman/blackheart variants, Beronath final-fight lightning patterns, Prodromus
/ Yurra / Naddo / Gruldir boss skills, `controller_dreadabyss` + dread-orb entities, 30 new
`totemloot` containers, ~12 new gdx3 items), four **Loyalist Pack 04** cosmetic transmute sets
(base archive), a super-boss opt-out token, and the Ascendant-altar loot plumbing.
**Nothing in the patch is Crucible wave-composition work.** Zero records under
`records/proxies/tier15waves/` … `tier19waves/` changed; the single wave-proxy change in the whole
corpus is `records/proxies/tier20waves/proxy_w10_p03a.dbr` (global wave 200 — the final wave).

### b.6 THE TEMPLATE VERDICT — and how I got a measurement instead of a block

**The problem.** `templates.arc` is resident in Edition-III but was **never fetched into
Edition-II** (Edition-II holds 8 `.arz` + 8 `Text_EN.arc` and nothing else). A direct II→III
template diff is therefore impossible on the two pinned trees. That is the shape of a NAMED BLOCK.

**The move.** A pre-patch `templates.arc` exists at
`/Users/admin/Games/vendor/grim-dawn/database/templates.arc` (780,972 B, mtime 2026-07-23 22:39).
Before using it I established its provenance **by content, not by assumption**: I re-hashed every
`.arz` in that tree and compared to the Edition-II pins.

```
grim-dawn/database/database.arz                    8cdeff12…  == Edition-II  ✅
grim-dawn/gdx1/database/GDX1.arz                   e28ab251…  == Edition-II  ✅
grim-dawn/gdx2/database/GDX2.arz                   f6d5bd67…  == Edition-II  ✅
grim-dawn/survivalmode1/database/SurvivalMode1.arz 6df94d3b…  == Edition-II  ✅
grim-dawn/survivalmode2/database/SurvivalMode2.arz 940e4034…  == Edition-II  ✅
grim-dawn/mods/survivalmode/…/SurvivalMode.arz     e55b760f…  == Edition-II  ✅
```
Six for six. `templates.arc` ships in **depot 219991, the same depot as `database.arz`**; that
depot's payload in this tree is byte-identical to Edition-II's. **The tree is therefore a
content-pinned Edition-II-era snapshot of depot 219991, and its `templates.arc` is a valid
Edition-II-era template layer.** Grade: **MEASURED** on the six hashes; **INFERRED** on the
one step "same depot + identical `database.arz` ⇒ same-manifest fetch ⇒ this is the Edition-II
`templates.arc`." I flag that step explicitly rather than smuggling it: it is the same
*resemblance-vs-join* shape that produced the FoI/gdx2 error in the Edition-II cut record. Here
the join key is real (shared depot ID + byte-identical co-resident payload), but it is an
argument, not a hash of the file in question.

**The result. 811 of 819 templates IDENTICAL; 8 changed.** (Identity established by the ARC
file-entry `crc` + `decomp_size` pair — decode-free, and it sidesteps a decompression failure the
current reader hits on one entry, which I did **not** paper over: see b.7.)

| template | pre-patch → III | what moved |
|---|---|---|
| `ascendantaltarformula.tpl` | 5,978 → 6,190 B | +`superBossSpawnModifier` |
| `character.tpl` | 29,474 → 29,692 B | +`checkForcedUpdateLoadSphere` (bool, default 0) |
| `controllernpc2.tpl` | 1,792 → 1,880 B | +`npcIdleLoop`; −`fileNameHistoryEntry` block |
| `dungeonentrance.tpl` | 2,650 → 2,780 B | +`reloadTargetRegion`; −`fileNameHistoryEntry` block |
| `gameengine.tpl` | 49,936 → 50,163 B | +`superBossDisableToken` |
| `monstershrine.tpl` | 8,138 → 8,397 B | +`Ascendant` group, +`ascendantLootTable` |
| `npc.tpl` | 6,651 → 6,830 B | +`controller` |
| `staticshrine.tpl` | 10,011 → 10,270 B | +`Ascendant` group, +`ascendantLootTable` |

**All eight are semantically ADDITIVE.** Nine new variable declarations; the only "removals" are
two `fileNameHistoryEntry` blocks (editor bookkeeping — the literal strings
`"Templates\ControllerNpc2.tpl"` and `"templates/dungeonentrance.tpl"`). **Zero variables removed.
Zero types changed. Zero `defaultValue`s changed.**

**The two verdicts the commission asked for:**

1. **FORWARD (Edition-III derivation chain): UN-BLOCKED.** The template layer is resident and
   parses. `proxylevelvarianceequation.tpl` is **IDENTICAL** and now readable — it declares the
   five equation variables a proxy's `levelVarianceEquations` may reference:
   **`averagePlayerLevel`, `minPlayerLevel`, `maxPlayerLevel`, `numberOfPlayers`, `gameDifficulty`**
   (all `class = "static"`, `type = "eqnVariable"`). That is the missing piece of the Part-C
   level-solve: the wave-proxy level equation is a function of **player level and party size and
   difficulty only** — it has no wave-index or tier term of its own. `monster.tpl`,
   `characterattributeequations.tpl`, `pet.tpl`, `petnonscaling.tpl`, `petplayerscaling.tpl`,
   `levelparameters.tpl` and `leveltable.tpl` are all **IDENTICAL** as well.
2. **BACKWARD (does the chain apply to Edition-II records?): YES.** Because every KC2-relevant
   template is byte-identical between the Edition-II-era layer and Edition-III, and because the
   eight that moved are additive-only, **the Edition-III template layer is a sound interpreter for
   Edition-II records.** The fixture-side derivation may proceed on Edition-II `.dbr` values read
   through Edition-III templates with no version-skew hazard. This is the single most useful
   by-product of Part (b): it makes the template acquisition retroactive.

### b.7 A reader defect found, and NOT papered over

`gd_arc_reader_2026_07_26.ArcArchive.read_file()` raises
`LZ4BlockError: Decompression failed: corrupt input or insufficient space in destination buffer`
on **one** entry of `templates.arc` — the archive's first name-table entry, which is the empty
string `""` (819 entries, index 0 is blank). Every real `.tpl` decodes cleanly. The CRC+size
identity path I used does not touch the decoder, so the 811/819 verdict is unaffected; and I
confirmed the eight changed templates decode and text-diff correctly. Recorded because the reader
is elrond-facing production tooling and a caller that iterates `names()` naively will crash on
entry 0. **Suggested guard (not applied — not my file): skip zero-length names in `names()`.**


---

## PART (b) ADDENDUM — the b.3 NAMED BLOCK is now CLOSED

While anchoring Part (c) I read the 12-slot layout of `balancingadjustment_mp+difficulty_enemies01`
and it resolves the indexing question I had explicitly refused to guess at in b.3:

```
characterLifeModifier  [ 50, 50, 50, 50 | 320, 320, 320, 320 | 580, 580, 580, 580 ]
                         └─ Normal ──┘   └──── Elite ─────┘   └─── Ultimate ────┘
                          (players 1-4)   (players 1-4)        (players 1-4)
```
Three difficulty blocks × four player-counts. Corroborated by
`characterDefensiveAbilityModifier` = `[−15 ×4 | −8 ×8]`, which breaks at the same 4-boundary,
and by `survivalinfo.dbr` binding `…_enemies01/02/03` to Normal/Elite/Ultimate.

**Therefore:**
```
offensivePhysicalModifier   II  : [  0,  0,  0,  0 | 0 ×4 | 0 ×4 ]
                            III : [-10,-10,-10,-10 | 0 ×4 | 0 ×4 ]
                                    └ NORMAL only ┘
```
> **The −10 lands on NORMAL difficulty only. Elite and Ultimate are untouched (0.0 → 0.0).**
> Crucible Gladiator is **Ultimate**. **No KC2 figure and no Crucible-scoped G-STATS figure is
> affected by this change** — obligation #2 in b.4 is **WITHDRAWN**, downgraded to: *campaign
> Normal-difficulty enemy physical damage is 10 % lower in Edition-III.* Grade: **MEASURED**
> (block layout read off two independent fields, not assumed).

The b.4 obligation list therefore reduces to **four** items, of which only #1 (nemesis waves
170–200) is substantial.

---

## PART (c) — PAIR-SEAT CHECK (Edition-II records; fixture explanation)

**Status: RE-SEAT ATTEMPTED — ALL THREE COMMISSIONED CANDIDATES FALSIFIED. The pair is
NOT re-seated. Two new MEASURED findings, and one NAMED BLOCK that is the real obstacle.**

Substrate: Edition-II (correct per R-KC2-9 — both fixture sittings predate the patch), and per
Part (b) every record used here is byte-identical in Edition-III anyway.
Instruments: `c1_anchor.py`, `c2_seat.py` in the Part-(b) scratch dir.

### c.0 First: my Part-B derivation was falsified TWICE, and the second one is mine

galadriel falsified the *seat* (`p04 = Carraxus` — no Carraxus on the board). Re-deriving, I
falsified my own *level model*, which is the more consequential error:

> **CORRECTION to my join note § 3.2 (MEASURED).** That section reported: *"`charLevel` multiplier
> census over all 2,974 enemy Monster records: ×1 on 2,787, ×1.1 on 187. **No other multiplier
> exists.**"* The sentence is true and useless. I censused the **multiplier** and never looked at
> the **additive term**. Full expression census over all Monster records:
>
> | `charLevel` expression | count |
> |---|---:|
> | `charLevel*1` | 1,785 |
> | **`charLevel*1+5`** | **521** |
> | **`charLevel*1+3`** | **202** |
> | `(charLevel*1.1)+2` | 187 |
> | `(charLevel*1)+2` | 122 |
> | `charLevel*1+1` | 119 |
> | `charLevel*1+2` | 114 |
> | `charLevel*1-1` | 34 |
> | `charLevel*1+6` | 13 |
> | `(charLevel*1)` / `1*1` / `1` | 18 |
>
> **1,132 of ~3,115 records (36 %) carry a non-zero additive level offset, spanning −1 to +6.**
> The § 3.2 level-interval table gives **proxy-draw** levels, not **effective charLevels**;
> effective = draw + per-record offset. Since the life equation is `((charLevel·k)^p)+c`, an
> additive offset does **not** cancel in a ratio — `((L₂+o)/(L₁+o))^p < (L₂/L₁)^p` — so **every
> achievable-ratio band in § 3.3 / § 3.4 is systematically OVERSTATED for offset-carrying
> records.** The § 3.4 verdicts must be re-run before they are relied on. I am not re-running them
> here (out of commission scope, and it does not gate the baton) — **flagged as owed.**

The offset is not a footnote: it is what makes the Haraxis plate legible, below.

### c.1 The Haraxis seat — MEASURED, and it validates the corrected model exactly

| datum | value | grade |
|---|---|---|
| w152 sp=4 BOSS pool alternatives | `swampcrab_carraxus` · `aetherialfleshshaper_hinissius` · **`aetherialfleshshaper_haraxis`** · `fleshweaverkrieg` | MEASURED |
| **Is Haraxis in the p04 pool I read?** | **YES — same spawn point, sp = 4.** He is alternative #3 of 4. The slot did not move; the *roll* went to Haraxis instead of Carraxus. | **MEASURED** |
| pool `levelVarianceEquation1` | `records/proxies/lv7_uber hero.dbr` — **not** `lv8_boss+` | MEASURED |
| `lv7_uber hero` @ apl 100 | min `(apl+3)` = **103.0**; max `(apl+3)+(apl/50)` = 105.0 | MEASURED |
| `aetherialfleshshaper_haraxis` `charLevel` | **`charLevel*1+5`** | MEASURED |
| ⇒ effective charLevel from a minimum draw | 103 + 5 = **108** | derived |
| **galadriel's plate read** | **level 108** | MEASURED (independent) |

> **The plate is reproduced exactly, from a lv7 minimum draw plus the +5 record offset, at
> `averagePlayerLevel = 100`.** Two consequences:
> 1. **`averagePlayerLevel = 100` is CONFIRMED** for this sitting. Inverting the constraint
>    (draw ∈ [103,104) for the plate to floor to 108) gives **apl ∈ [98.04, 100]**; with a
>    level-100 character, apl = 100 and the draw sat on the interval floor.
> 2. **Nameplate levels are directly comparable to effective `charLevel`.** This is a reusable
>    calibration for galadriel↔corpus joins and it was not previously established.
>
> **This is why the commission's "an L108 seat widens your level solve" instinct was right, but
> for the opposite reason:** L108 does not imply a higher-than-modelled level band. It implies
> the band was modelled correctly and the *record offset* was missing.

### c.2 CANDIDATE 1 — Haraxis's own summon chain: **FALSIFIED on tier**

Both of Haraxis's body-producing skills, read at field granularity:

| skill | `Class` | `petLimit` | `petBurstSpawn` | TTL | body | body tier |
|---|---|---:|---:|---:|---|---|
| `fleshshaperharaxis_aethercorruptiongenerator` | `Skill_MonsterGenerator` | **8** | 2 | 40 s | `aetherialcorruption_c01_summon` (`charLevel*1+1`) | **Champion** |
| `fleshshaperharaxis_summonspirits` | `Skill_TargetedSpawnPet` | **6 → 12** (rank 17+) | **3 → 6** | 30 s | `fleshshaper_spirit_01` | **Champion** |

> **Answer to the commission's question, split in two because the record splits it in two:**
> **Does the Fleshweaver chain summon a limit ≥ 7 body? YES — two of them, at limit 8 and limit 12.**
> **Is either a PLAIN body? NO. Both are `monsterClassification = Champion`.** Burst is 2 and 3→6,
> never 4.
> **Verdict: FALSIFIED as a seat for the plain-tier pair, and for the +10 plain-tier surplus.**
>
> **But do not discard this record.** A `petLimit = 12`, `petBurstSpawn = 6` spirit summon is the
> largest single add budget anywhere in the w152 hit table — larger than the crab generator's 8/4 —
> and the composition model has **no** term for it. It cannot explain a *plain-tier* surplus, but
> **any Champion-tier count on w152 that the model under-supports should be seated here first.**
> Recorded as a live lead, not a dead end.

### c.3 CANDIDATE 2 — `chthonianabomination_summondevourers_a01`: **FALSIFIED on roster**

The skill exists (`records/skills/nonplayerskills/bossskills/chthonianabomination_summondevourers_a01.dbr`).
Its summoner does not. **`chthonianabomination` is not a member of any w152 pool.** The only
chthonian records on the w152 roster are 25 `records/creatures/enemies/devotion/chthonian*_h0N.dbr`
bodies reachable through the sp=6 DEVOTION pool — and in those, the devourer *is* the hero body,
not a summoned add; none of them carries the abomination's summon skill.

> **Verdict: FALSIFIED. No summoner ⇒ no seat.**
> **A trap I nearly walked into, recorded.** My first scan injected `chthoniandevourer_a01` into
> the candidate set by corpus search rather than by roster membership, and it returned a beautiful
> false positive: **42,637 HP at L105.0 vs the measured 42,798 — 0.38 % off**, plus 43,415 at
> L106.5 vs 43,548. Two near-hits on both pair members from one record. **It is not reachable on
> wave 152.** A numeric match against a record the wave cannot spawn is not evidence; it is
> discipline **D-b — resemblance mistaken for a join key** — and the HP class of a devourer is
> close to a crabling's precisely *because* the two are the same rough size of trash body. The
> commission asked me to check "devourer HP class vs ≈ 42.8 K": **the HP class matches and the
> match means nothing.**

### c.4 CANDIDATE 3 — the p01 roll's level spread: **FALSIFIED on band — but the mechanism is REAL**

A genuinely new MEASURED datum, from the survival array's spawn-count adjusters at w152:

```
balancingadjustment_survivalmode_enemies03.dbr  @ wave-index 151 (= w152)
    spawnMinAdj = 0    spawnMaxAdj = 0
    spawnChampionMinAdj = +1     spawnChampionMaxAdj = +1
```
> **At w152 every champion-bearing pool spawns championMin+1 … championMax+1 = TWO champion
> bodies, not one.** The `swampcrab_hero` pool's `championMin/Max = 1/1` therefore yields **two
> swampcrab heroes**, each drawing its own `lv6_hero` level, **each carrying its own
> `swampcrab_crabgenerator` (petLimit 8, burst 4)**.
>
> This **repairs** the structural objection I could not answer in Part B — a two-level crabling
> spread is mechanically available after all, and the plain-tier add budget on w152 is **2 × 8 =
> up to 16 crablings**, not 8. *That alone is a candidate explanation for the +10 plain-tier
> surplus, independent of the pair question,* and it should be carried to the composition model.
>
> **But it still cannot produce the measured ratio.** `swampcrab_h01…h05` all carry
> `charLevel*1` (no offset — checked individually), so effective level = draw ∈ `lv6_hero` =
> **[104, 105]**. With the crabling's `p = 1.28`, the maximum achievable spread is
> `(105/104)^1.28 = 1.236 %`. **The measured pair is 1.752 %.**
> **Verdict: FALSIFIED on band — by a wider margin than Part B claimed, because Part B's band was
> itself overstated (c.0).**

### c.5 The absolute-HP solve, and the NAMED BLOCK that stops the re-seat

Every multiplier on a given wave is shared, so a within-wave HP *ratio* is multiplier-free.
Using galadriel's MEASURED Haraxis max HP as the anchor:

```
Haraxis  life = ((charLevel*30)^1.5)+500 ,  charLevel 108  ->  184,924 base
         MEASURED max HP 2,050,807       ->  implied total multiplier x11.0900
crabling life = ((charLevel*6)^1.28)+25  ,  charLevel*1
```
Required crabling levels for the pair, sweeping Haraxis's admissible draw (eff. 108 → 108.99):

| pair member | required crabling level |
|---:|---|
| 42,798 | **105.10 – 106.23** |
| 43,548 | **106.54 – 107.69** |

`lv6_hero` = [104, 105]. **The lower pair member overshoots the interval ceiling by 0.10–1.23
levels; the upper by 1.54–2.69.** The overshoot is small, systematic, and in one direction.

**THE BLOCK — stated, not estimated.** The anchor is only valid if the multiplier stack is
**tier-independent**, and it is not established that it is. Evidence that it is *not*:

```
implied total multiplier          x11.0900
w152 survival characterLifeModifier   +308 %  -> x4.0800
residual                                        x2.7181   <-- unexplained
```
The residual does not decompose against `balancingadjustment_mp+difficulty_enemies01`
(`characterLifeModifier` = 50 / 320 / 580 % → ×6.12, ×17.14, ×27.74 multiplicatively, or ×9.88
additively at Ultimate — **none is ×11.09**). I searched the corpus for a rank/classification
multiplier table (`monsterclass*`, `rankmultiplier*`, `monsterlevel*`): **zero records.**

> **NAMED BLOCK — B-KC2-C1.** A ×2.718 component of the w152 enemy-life multiplier stack is
> **unaccounted for**, and I cannot rule out that it is **tier-dependent** (Haraxis = `Quest`,
> crabling = `Common`). If it is tier-dependent it does **not** cancel in a Quest↔Common ratio,
> and every required-level figure in this section is wrong by an unknown factor. **The pair
> therefore cannot be re-seated on absolute HP until the residual is decomposed.**
> Zero estimation offered. What would decide it: one MEASURED HP reading from **any Common-tier
> w152 body with a known record** (galadriel already has the `Ugdenbog Crabling` plate on the
> board — a max-HP read on *that* plate collapses this block immediately, because it anchors
> Common against Common and the tier question drops out).

### c.6 PART (c) VERDICT

| candidate | verdict | falsified on |
|---|---|---|
| 1 — Haraxis's own summon chain | **FALSIFIED** | tier (both bodies Champion, not plain) |
| 2 — `chthonianabomination_summondevourers_a01` | **FALSIFIED** | roster (summoner absent from w152) |
| 3 — p01 roll's level spread vs `lv6_hero` | **FALSIFIED** | band (1.236 % max vs 1.752 % measured) |

**The Δ1.752 % pair is NOT re-seated.** Standing status: **UNSEATED**, blocked on B-KC2-C1.

**What survives, and what is newly owed:**
- ✅ **Mechanism class stands** (per the commission) — crab-summoner adds are real: `Ugdenbog
  Crabling` is MEASURED on the board and the generator chain is byte-identical in both editions.
- ✅ **NEW — the plain-tier add budget on w152 is 2× what the model assumes**
  (`spawnChampionMinAdj/MaxAdj = +1` ⇒ two crab heroes ⇒ up to 16 crablings). This is an
  independent, MEASURED candidate for the **+10 plain-tier surplus** and does not depend on the
  pair question at all. **Recommend routing this to the composition model regardless of how the
  pair resolves.**
- ✅ **NEW — nameplate level = effective `charLevel`**, calibrated on Haraxis (108 = 103 + 5).
- ⚠ **OWED — re-run join-note § 3.3 / § 3.4** with per-record additive offsets included; the
  published ratio bands are overstated (c.0).
- 🚫 **BLOCKED — B-KC2-C1**, the ×2.718 residual. One Common-tier plate HP read clears it.

**Attribution per R-KC2-7:** c.1 pool membership / variance eq / `charLevel` / spawn adjusters /
skill fields / tag joins / expression census = **MEASURED** (read from Edition-II records this
session). c.5 required-level figures = **MODELED** (conditional on the unproven tier-independence
of the anchor). c.2/c.3/c.4 falsification verdicts = **MEASURED** on their falsifying facts
(tier, roster membership, interval arithmetic), which is why they hold even though c.5 is blocked.

---

## PART (d) — `Rotmouth` — **RESOLVED**

**Method:** localization-tag join. Decoded every `tags*.txt` in every `Text_EN.arc` across the
corpus (7 archives in Edition-III, 4 in Edition-II) and searched case-insensitively for the
display string; then round-tripped the tag back to the record that declares it.

**Forward join (string → tag):** exactly **one** hit, in both editions.
```
gdx1/resources/Text_EN.arc  ::  tagsgdx1_creatures.txt
      tagGDX1HeroBasilisk_H02=Rotmouth
```

**Reverse join (tag → record):**
```
records/creatures/enemies/hero/basilisk_h02.dbr
      description            = tagGDX1HeroBasilisk_H02
      monsterClassification  = Hero              <-- matches the ORANGE plate
      charLevel              = charLevel*1+5
      owners                 = ['gdx1', 'gdx2', 'sm1']   (last-wins: sm1)
```

**Seat on wave 152:**
```
sp = 2   kind = HERO   pool = records/proxies/poolsherogdx1/basilisk_hero.dbr
```
The sp=2 pool has exactly two alternatives — `poolsherogdx1/basilisk_hero` and
`poolsherogdx3/thornedhorrorfrost_hero`. **The wave rolled `basilisk_hero`, and the pool rolled
hero variant `h02` = Rotmouth.**

> ### VERDICT — **RESOLVED, MEASURED. Not a roster gap.**
> `Rotmouth` = **`records/creatures/enemies/hero/basilisk_h02.dbr`**, seated at **w152 spawn
> point 2** via `poolsherogdx1/basilisk_hero`. galadriel's **orange → hero** plate read is
> corroborated by the record's own `monsterClassification = Hero`.
>
> **R-W152-2 (roster gap) should be CLOSED.** The body was never missing from the corpus — it was
> missing from the *plate tables*, which is a name-coverage gap in our extraction, not a
> composition gap in the model. The w152 model already supports a hero body at sp=2; Rotmouth is
> that body, correctly predicted, merely unnamed.
>
> **Two corroborations at no extra cost:**
> 1. The `basilisk_hero` roll at sp=2 **forecloses** `thornedhorrorfrost_hero`, which pins the
>    other half of the w152 hero composition — and galadriel's census independently lists
>    `Stonegaze Basilisk` on the same board, the basilisk trash line from sp=3's
>    `poolsbasicgdx1/basilisk_t3`. **Both basilisk-branch pools rolled together**, exactly as a
>    shared-family wave would.
> 2. **A falsifiable prediction for galadriel, free:** `basilisk_h02` carries `charLevel*1+5` and
>    `lv6_hero` draws [104, 105] at apl = 100. **Rotmouth's plate must read level 109 or 110.**
>    (Under the same rule that reproduced Haraxis's 108 exactly.) If the plate reads anything
>    else, the `charLevel`-offset model of c.1 is wrong and c.1's `averagePlayerLevel = 100`
>    confirmation falls with it.
>
> **Edition scope:** the tag file lives in `gdx1/resources/Text_EN.arc`, which is one of the
> **six IDENTICAL** localization archives (a.7). The record `basilisk_h02.dbr` is IDENTICAL
> across editions (Part b). **This resolution is valid in BOTH Edition-II and Edition-III** —
> tag, record, tier and offset all byte-match.

---

## CLOSING — status per commission part

| part | status | grade |
|---|---|---|
| **(a)** INTAKE — 38-file SHA-256 pin + inventory; 8/8 manifest reconciliation; Edition-II 16/16 re-verify | **COMPLETE** | MEASURED |
| **(b)** II→III record-granularity diff | **COMPLETE — widened to all 84,663 shared records**; KC2 fixture substrate 100 % IDENTICAL; 4 named obligations, all outside w152/w157; template layer measured (811/819 identical, 8 additive) | MEASURED |
| **(c)** PAIR-SEAT CHECK | **RE-SEAT FAILED — all 3 candidates falsified.** Pair UNSEATED. Blocked on **B-KC2-C1** (×2.718 unexplained multiplier residual). Two new MEASURED findings + one owed re-run. | mixed, tagged inline |
| **(d)** `Rotmouth` | **RESOLVED** → `hero/basilisk_h02.dbr`, w152 sp=2. R-W152-2 closable. | MEASURED |

**External fetches: ZERO.** All work corpus-resident and read-only. Nothing committed
(conductor centralizes commits at fold close). Note UNCOMMITTED as instructed.

**Instruments (reproducible):**
`agentic_orchestration/legolas/scratch/2026-08-08-kc2-ed3-diff/` —
`lib2.py` (dual-edition overlay resolver) · `fulldiff.py` · `kc2set.py` · `c1_anchor.py` ·
`c2_seat.py` · `fulldiff_summary.json` · `fulldiff_detail.json` · `kc2set_verdicts.json` ·
`tpl_changed.json` · `fulldiff.log`
