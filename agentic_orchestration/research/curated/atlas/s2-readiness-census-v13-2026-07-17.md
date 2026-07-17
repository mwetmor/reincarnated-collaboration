# S2 — Migration-Readiness Census V13 (post-di-spiritform phantom write)

**Date:** 2026-07-17 · **Author:** elrond (autonomous atlas-parity run, post-phantom-write census charge)
**Commissioner:** gandalf-prime (Matt autonomous-run authorization 2026-07-16; ruling 16 Matt veto-open)

**Sources folded (V12 → V13):**
- Legolas widened re-crawl (third attempt): `agentic_orchestration/legolas/research/di-spiritform-recrawl-2026-07-17/` — PHANTOM finding (gandalf-verified, commit `dc0ce6cd`)
- Elrond ruling 16 application: `atlas/di-spiritform-phantom-2026-07-17.md` (this run) — Option A only per gandalf-prime; Option B parked to E-next lane
- Backup: `../corpus.db.pre-di-spiritform-phantom-2026-07-17-backup`

**Corpus state (POST-phantom-write):** 585 rows / **563 kit-grain (518 positives + 45 negatives) + 22 NULL-grain** / 562 cell_key resolved (incl. 1 -bt sentinel) / 4 dossier_owed held-out / 585 engine_key 1:1 (0 orphans)

**Scope:** This charge is READ-ONLY on corpus.db post-phantom-write.

**md5-stability:**
- Post-phantom-write (baseline for this census): `99def837a90aec875d030cfd8279772d`
- Post-census (read-only): `99def837a90aec875d030cfd8279772d`
- Census read pass DID NOT modify DB: **True**

---

## §1 Headline

| Metric | Count | % |
|---|---|---|
| **Candidate pool (denominator)** | **563** | 100.0% |
| **Expressible-now** | **560** | **99.47%** |
| Blocked | 3 | 0.53% |
| — dossier_owed in-pool (total) | 4 | 0.71% |
| — of-which-in-blocked | 2 | 0.36% |
| — of-which-in-expressible | 2 | 0.36% |

Denominator composition: 518 corpus positives at kit grain (V12 519 → V13 518 via di-spiritform phantom flip) + 45 founding roster = **563** (V12 564 → V13 563).

Corpus expressible: **515/518 (99.42%)**  ·  Roster expressible: **45/45 (100.0%)**

**Structural headline: the census tail is now 100% Matt-gated.** All 3 remaining blocked kits are `mechanic:shapeshift` awaiting the Matt GX-02 shapeshift-docket ruling (forks A–E queued). Zero econ residue, zero ailment residue, zero source-truth residue. Legolas Mode B is closed on the census gate — the last legolas-re-crawl-gated residual (`di-spiritform-druid-pvp`) resolved as phantom this pass.

---

## §2 Delta vs V12 — two-lever decomposition (iron law 4)

Δ decomposes cleanly into:
- **Phantom denominator effect** (1 kit reclassified corpus positive → negative): denominator −1 (564 → 563); blocked tail −1 (4 → 3). This is a **denominator lever**, not a flip lever — the kit was blocked in V12 and did not contribute to the 560 expressible count. Removing it from denominator preserves expressible at 560 while shrinking blocked.
- **Flip effect** (0 blocked-→-expressible transitions): 0. No blocked kit flipped clean this pass.

**Expected V13 identity (baseline-anchored):**
- Expected expressible = V12 560 + flip 0 = **560**
- Expected denominator = V12 564 − phantom 1 = **563**
- Expected blocked = V12 4 − phantom 1 − flip 0 = **3**

**DB truth check:**
- Actual expressible = **560** vs expected 560 → OK
- Actual denominator = **563** vs expected 563 → OK
- Actual blocked = **3** vs expected 3 → OK

| Scoreboard | Pool expressible | % | Corpus | Roster |
|---|---|---|---|---|
| V7 (Wave-B baseline) | 258/568 | 45.4% | 213/523 | 45/45 |
| V8 (post-Gate-2 + econ-audit) | 385/568 | 67.8% | 340/523 | 45/45 |
| V9 (post-Wave-B + reclass) | 509/565 | 90.1% | 464/520 | 45/45 |
| V10 (post-Wave-C landed + corpus-align) | 551/565 | 97.50% | 506/520 | 45/45 |
| V11 (post-econ-recrawl application + phantom ruling) | 558/564 | 98.94% | 513/519 | 45/45 |
| V12 (post-Wave-D-landing + DR reclassify) | 560/564 | 99.29% | 515/519 | 45/45 |
| **V13 (this run, post-di-spiritform phantom write)** | **560/563** | **99.47%** | **515/518** | 45/45 |
| **Δ vs V12** | **+0 (denominator −1)** | **+0.18pp** | **+0 (denominator −1)** | 0 |
| — phantom denominator contribution | denominator −1 | | denominator −1 | 0 |
| — flip contribution | 0 | | 0 | 0 |
| **Δ vs V7** | **+302** | **+54.07pp** | **+302** | 0 |

_Trajectory table corrected 2026-07-17 (same-day): V7-V9 rows misstated in the initial commit; corrected against the minting artifacts. See git lineage._

**Headline movement: V12 99.29% → V13 99.47% (+0.18pp; via phantom denominator −1, zero flip).**

**Trajectory annotation:** V13 is the highest census score in the lineage and closes the legolas-re-crawl-gated axis. All remaining blocked residue is Matt-fork-gated at GX-02.

---

## §3 What moved between V12 and V13 (named lever)

**Lever: di-spiritform phantom ruling (elrond ruling 16-application, Matt veto-open).**

`di-spiritform-druid-pvp` re-classified corpus-positive → corpus-negative per legolas widened re-crawl finding (third attempt): the DI Druid class IS real (Blizzard launched 2025-07-03) but the "spirit form" mechanic does NOT exist. Real transformations = Werewolf/Werebear/Stag Charge/Raven Swarm. Complaint-tier CC vocab all landed. Two independent full-skill enumerations agree; both confirm mechanic-absence verbatim.

Gandalf-prime ruling 16 selected **Option A only**: phantom-flag the row (`negative=1`), retain for 585-conservation and audit signal. **Option B REFUSED for this cycle** — creating clean `di-druid-pvp-cc-stack-2026` row is edition-lane work (rides E-next docket with LA 4 at the E4-ratification Matt gate). **Option C REFUSED** — loses audit signal.

Writes applied THIS RUN: **1** (canon_corpus row `di-spiritform-druid-pvp` phantom-flag). Details in ruling record `atlas/di-spiritform-phantom-2026-07-17.md` (SQL forward + reversal + md5 chain + idempotency guard documented).

**Wave-D remains landed** from V12 (chain `5ed240a..8d8bd26`); no engine-side changes this pass.

---

## §4 Sheet projection cross-check

**Charge projection:** denominator 564 → 563 (phantom −1); expressible 560 UNCHANGED; blocked 4 → 3; result = 560/563 = 99.47%.

**Actual V13 result:** 560/563 = **99.47%**.

Δ vs charge projection: **+0** kits (+0.00pp) — EXACT MATCH.

---

## §5 Blocked-on-what — ranked buckets (V13)

| Bucket category | Kits touched | Sub-buckets |
|---|---|---|
| **shapeshift (GX-02 docket)** | 3 | mechanic:shapeshift=3 |

### §5b Bucket detail (individual buckets ranked)

| # | Bucket | Count |
|---|---|---|
| 1 | `mechanic:shapeshift` | 3 |

**ailment-wave-c+:unknown-ailment bucket: EMPTY** (was 1 in V12; kit reclassified phantom §3).
**econ:DR bucket: EMPTY** (was 2 in V11 pre-DR-reclassify; cleared in V12).

**Structural signal: the residual bucket is a singleton — every remaining blocked kit is a `mechanic:shapeshift` waiting on the GX-02 Matt fork.** No mixed-bucket residue. No source-truth residue. No legolas-re-crawl residue.

---

## §6 Blocked-tail rosters (DERIVED FROM DB)

Named kit rosters per residual blocker:

### `mechanic:shapeshift` (3 kits — Matt-fork GX-02 gate, forks A–E queued)
- `gd-berserker-wereforms` — Berserker (FoA mastery)
- `la-ferality-wildsoul` — Ferality Wildsoul (also dossier_owed)
- `la-phantom-beast-awakening-wildsoul` — Phantom Beast Awakening Wildsoul (also dossier_owed)

**Cross-check DB-truth-vs-expected (per charge):**
- shapeshift bucket: **3 kits** (gd-berserker-wereforms, la-ferality-wildsoul, la-phantom-beast-awakening-wildsoul) — OK
- econ:DR bucket: **0 kits** — OK
- unknown-ailment bucket: **0 kits** (was 1 in V12; di-spiritform phantom-flipped) — OK
- di-spiritform-druid-pvp: **negative=1** (out of denominator; row RETAINED for audit signal per Option A) — OK
- void-rift: phantom-negative per V11 §3 ruling (unchanged; row retained; not in blocked tail) — OK

**Expected-residual gates:**
- shapeshift 3: Matt-fork GX-02 (forks A–E queued) — awaits ruling

**The census tail is 100% Matt-gated. There is nothing legolas or elrond can do to advance the score without Matt's GX-02 ruling.**

---

## §7 dossier_owed enumeration (UNCHANGED from V12)

The 4 dossier_owed kits are all in the LA (Lost Ark) family — 2 Wildsoul + 2 Valkyrie variants:

| # | kit_id | folk_name | in-pool status | shapeshift-blocked? |
|---|---|---|---|---|
| 1 | `la-ferality-wildsoul` | Ferality Wildsoul | **BLOCKED** (shapeshift) | YES |
| 2 | `la-phantom-beast-awakening-wildsoul` | Phantom Beast Awakening Wildsoul | **BLOCKED** (shapeshift) | YES |
| 3 | `la-liberator-valkyrie` | Liberator Valkyrie | **EXPRESSIBLE** | NO |
| 4 | `la-shining-knight-valkyrie` | Shining Knight Valkyrie | **EXPRESSIBLE** | NO |

**Sub-row split:**
- dossier_owed in-pool total: **4**
- of-which-in-blocked: **2** (both Wildsouls; released when GX-02 docket rules)
- of-which-in-expressible: **2** (both Valkyries; already contributing to the 560 expressible count)

**Consistency with §1:** dossier_owed_in-pool 4 is a subset-count in a separate axis from denominator 563. It is not additive with expressible 560 or blocked 3.

---

## §8 Iron-law asserts (PRE V12-state / POST V13-state)

| Assert | V12 (published) | V13 (this run) | Notes |
|---|---|---|---|
| total_corpus | 585 | 585 | UNCHANGED (585 conservation preserved) |
| total_engine_key | 585 | 585 | UNCHANGED |
| kit_grain | 563 | 563 | UNCHANGED |
| null_grain | 22 | 22 | UNCHANGED |
| **kit_positives (denominator base)** | **519** | **518** | −1 (phantom flip) |
| **kit_negatives** | **44** | **45** | +1 (phantom flip) |
| **pool = corpus positives + roster 45** | **564** | **563** | −1 (denominator −1) |
| combat-kit (row_class) | 563 | 563 | UNCHANGED |
| system-record (row_class) | 22 | 22 | UNCHANGED |
| cell_key_resolved | 562 | 562 | UNCHANGED |
| bt_sentinel | 1 | 1 | UNCHANGED |
| orphans engine→corpus | 0 | 0 | UNCHANGED |
| orphans corpus→engine | 0 | 0 | UNCHANGED |
| dossier_owed | 4 | 4 | UNCHANGED |

Cross-check assertions:
- `roster_expressible == 45`: 45 == 45 — OK
- `total 585 conservation`: UNCHANGED — OK
- `denominator identity`: 518 corpus positives + 45 roster = 563 == 563 — OK
- `positives + negatives = kit_grain`: 518 + 45 = 563 == 563 — OK

---

## §9 Reproducibility & SQL derivations

**Backup:** `../corpus.db.pre-di-spiritform-phantom-2026-07-17-backup` (pre-phantom-write; V13 census reports POST-write state)
**Ruling record:** `../atlas/di-spiritform-phantom-2026-07-17.md`
**Legolas widened re-crawl:** `agentic_orchestration/legolas/research/di-spiritform-recrawl-2026-07-17/`

**md5 chain:** pre-write `11f73ab3f000b9ada1492fe496e14e09` → post-write / census-baseline `99def837a90aec875d030cfd8279772d` → post-census-read `99def837a90aec875d030cfd8279772d` → **stable across census pass: True**

**SQL derivations (row-count verification discipline):**

Iron-law state derivation (§8):
```sql
SELECT COUNT(*) FROM canon_corpus;                                          -- 585 total
SELECT COUNT(*) FROM canon_corpus WHERE grain='kit';                        -- 563 kit-grain
SELECT COUNT(*) FROM canon_corpus WHERE grain IS NULL;                      -- 22 null-grain
SELECT COUNT(*) FROM canon_corpus WHERE grain='kit' AND negative=0;         -- 518 kit_positives
SELECT COUNT(*) FROM canon_corpus WHERE grain='kit' AND negative=1;         -- 45 kit_negatives
SELECT COUNT(*) FROM canon_engine_key;                                      -- 585 total
SELECT COUNT(*) FROM canon_engine_key WHERE cell_key IS NOT NULL;           -- 562 cell_key_resolved
SELECT COUNT(*) FROM canon_engine_key WHERE kit_id LIKE '%-bt';             -- 1 bt_sentinel
SELECT COUNT(*) FROM canon_engine_key WHERE row_class='combat-kit';         -- 563
SELECT COUNT(*) FROM canon_engine_key WHERE row_class='system-record';      -- 22
SELECT COUNT(*) FROM canon_corpus WHERE dossier_owed=1;                     -- 4
SELECT COUNT(*) FROM roster_atlas;                                          -- 45
```

Phantom write verification (§3):
```sql
SELECT kit_id, negative, flags, mech_note FROM canon_corpus
 WHERE kit_id='di-spiritform-druid-pvp';
-- → negative=1
-- → flags includes 'phantom-kit-mechanic-invention-2026-07-17:gandalf-ruling-16:Matt-veto-open'
-- → mech_note starts with 'PHANTOM (mob-harvest v3 mis-naming)'
```

Blocked-tail derivation (§5–§6): performed via classification logic mirroring V12:
- ECON_LANDED = {SU, HV, PC, RS, AM, RC, BT, TH, LC}
- AILMENT_LANDED = {damage-amp, freeze, stun, poison-dot, taunt, blind, curse/hex, fear, instant-kill, deflect}
- AILMENT_STILL_BLOCKED = {} (unknown-ailment cleared this pass)
- Shapeshift substring match: {wildsoul, wereforms} — di-spiritform-druid-pvp EXCLUDED from denominator per phantom flip

Result: 3 blocked kits — all 3 shapeshift (gd-berserker-wereforms, la-ferality-wildsoul, la-phantom-beast-awakening-wildsoul). Zero econ, zero ailment, zero source-truth, zero legolas-re-crawl residue.

---

## §10 Consumers & next re-run triggers

**Consumers:** governs S5 corpus→engine migration staging. V13 is the census snapshot published post-di-spiritform phantom write; closes the legolas-re-crawl-gated axis.

**Next re-run triggers:**
1. Matt rules on GX-02 shapeshift docket (forks A–E queued) → shapeshift bucket resolves → **V14**
2. Matt vetoes any of ruling 14 (DR reclassify, V12) / ruling 15 / **ruling 16 (di-spiritform phantom, V13)** → V-revert (SQL in relevant ruling record)
3. E-next admission docket ratifies at E4 Matt gate → new rows ADDED (5 candidates parked: LA 4 + `di-druid-pvp-cc-stack-2026`) → denominator UP, expressible UP → **V-next-admission**
4. Matt vetoes prior phantom (`d2-wl-void-rift`, V11 §3) → denominator +1 → V-revert

**V13 closes end-to-end** at 99.47% pool-expressible. Blocked tail = 3 kits, ALL gated on the Matt GX-02 shapeshift-docket ruling. **This is the highest-ever migration-readiness score in the census lineage (V7→V13) and closes the legolas-Mode-B-gated axis.**

---

## §11 Provenance-integrity finding (linked)

The di-spiritform phantom is the **SECOND** mob-harvest v3 phantom kit surfaced by post-hoc re-crawl audit:
1. `d2-wl-void-rift` — V11 phantom write (franchise-name collision, D2/Destiny-2 vocabulary bleed)
2. `di-spiritform-druid-pvp` — V13 phantom write (mechanic-invention from complaint colloquialism)

Two independent phantoms in `provenance_tag='mobile-harvest-v3'` with `source_date='2026-07-12'` = **systematic risk**. A companion triage docket is issued this run at `atlas/mob-harvest-v3-triage-2026-07-17.md`, ranking the 458 residual positive mob-harvest v3 kits on phantom-risk signals visible in-DB. HIGH-tier rankings there recommend legolas re-crawl batching for gandalf-prime to fire as a follow-on.
