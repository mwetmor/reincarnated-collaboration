# S2 — Migration-Readiness Census V12 (THE SCOREBOARD, post-Wave-D-landing + DR reclassify)

**Date:** 2026-07-17 · **Author:** elrond (autonomous atlas-parity run, post-Wave-D-landing census charge)
**Commissioner:** gandalf-prime (Matt autonomous-run authorization 2026-07-16)
**Sources folded (V11 → V12):**
- Engine Wave-D landed: chain `5ed240a..8d8bd26` pushed (rocket vocab-loader repoint + gamora fidelity ×4 + Gate-1/Gate-2 decisions-log entries)
- Gate-2 verdict: PASS-WITH-AMENDMENTS, zero MAJOR/BLOCK (`agentic_orchestration/jack-ryan/notes/2026-07-17-wave-d-gate2.md`)
- DR reclassify (elrond ruling, commit `29dee75e`): `hot-norseman-frost-avalanche` + `vs-queen-sigma` re-classified NR/auto-fire (VS-genre-native) — `econ_status gap → native`, `econ_gaps ["DR"] → []`, flags stamped `dr-reclassify-2026-07-17:elrond-ruling:NR/auto-fire` — Matt veto-open but LANDED in DB
- Backup at `agentic_orchestration/research/curated/corpus.db.pre-dr-reclassify-2026-07-17-backup`
- Ruling record at `agentic_orchestration/research/curated/atlas/dr-reclassify-2026-07-17.md`

**Corpus state (POST-Wave-D + DR reclassify):** 585 rows / **563 kit-grain (519 positives + 44 negatives) + 22 NULL-grain** / 562 cell_key resolved (incl. 1 -bt sentinel) / 4 dossier_owed held-out / 585 engine_key 1:1 (0 orphans)

**Scope:** Post-Wave-D-landing snapshot (engine seam-parity complete on verify; corpus.db DR reclassify folded). This charge is READ-ONLY on corpus.db.

**md5-stability:**
- Pre-census: `11f73ab3f000b9ada1492fe496e14e09`
- Post-census (read-only): `11f73ab3f000b9ada1492fe496e14e09`
- Census read pass DID NOT modify DB: **True**

---

## §1 Headline

| Metric | Count | % |
|---|---|---|
| **Candidate pool (denominator)** | **564** | 100.0% |
| **Expressible-now** | **560** | **99.29%** |
| Blocked | 4 | 0.71% |
| — dossier_owed in-pool (total) | 4 | 0.71% |
| — of-which-in-blocked | 2 | 0.35% |
| — of-which-in-expressible | 2 | 0.35% |

Denominator composition: 519 corpus positives at kit grain (UNCHANGED from V11: no phantom writes this pass; DR reclassify preserves positive status) + 45 founding roster = **564** (UNCHANGED from V11).

Corpus expressible: **515/519 (99.23%)**  ·  Roster expressible: **45/45 (100.0%)** (UNCHANGED — verified)

**dossier_owed sub-row split fix (corrects V11 §1 misplacement):** V11 published "dossier_owed held-out = 4" as if all 4 were IN the blocked bucket. DB truth: the 4 dossier_owed kits distribute as 2-in-blocked (`la-ferality-wildsoul`, `la-phantom-beast-awakening-wildsoul` — shapeshift-blocked Wildsouls) + 2-in-expressible (`la-liberator-valkyrie`, `la-shining-knight-valkyrie` — plate/paladin Valkyrie variants, no blockers). V11's single-row report obscured this split. V12 §1 restores the correct sub-row structure. Registered defect closed.

---

## §2 Delta vs V11 — two-lever decomposition (iron law 4)

Δ decomposes cleanly into:
- **DR reclassify flip effect** (2 econ:DR sole-blocker kits flip clean via NR/auto-fire re-classification): +2 kits expressible.
- **Denominator effect** (none this pass): 0. No phantom rulings, no grain writes, no negative flips. Wave-D landed engine-side but the corpus.db substrate carried through unmodified except for the DR reclassify.

**Expected V12 identity (baseline-anchored):**
- Expected expressible = V11 558 + dr_flip 2 + denominator_effect 0 = **560**
- Expected denominator = V11 564 + denominator_effect 0 = **564**
- Expected blocked = V11 6 − dr_flip 2 + denominator_effect_blocked 0 = **4**

**DB truth check:**
- Actual expressible = **560** vs expected 560 → OK
- Actual denominator = **564** vs expected 564 → OK
- Actual blocked = **4** vs expected 4 → OK

| Scoreboard | Pool expressible | % | Corpus | Roster |
|---|---|---|---|---|
| V10 (post-Wave-C landed + corpus-align) | 551/565 | 97.50% | 506/520 | 45/45 |
| V11 (post-econ-recrawl application + phantom ruling) | 558/564 | 98.94% | 513/519 | 45/45 |
| **V12 (this run, post-Wave-D-landing + DR reclassify)** | **560/564** | **99.29%** | **515/519** | 45/45 |
| **Δ vs V11** | **+2** | **+0.35pp** | **+2** | 0 |
| — DR-reclassify flip contribution | +2 | | +2 | 0 |
| — denominator effect | 0 | | 0 | 0 |
| **Δ vs V10** | **+9** | **+1.79pp** | **+9** | 0 |

**Headline movement: V11 98.94% → V12 99.29% (+0.35pp; two DR kits flipped native + zero denominator change).**

---

## §3 What moved between V11 and V12 (named lever)

**Lever: DR reclassify (elrond ruling, commit `29dee75e`, Matt veto-open).**

Two kits carried `econ_gaps=["DR"]` in V11, blocking the pool 6-count:
- `hot-norseman-frost-avalanche` (Frost Avalanche Norseman)
- `vs-queen-sigma` (Queen Sigma)

Rationale for reclassification (per ruling record `agentic_orchestration/research/curated/atlas/dr-reclassify-2026-07-17.md`):

Both kits carry per-fight economy = auto-fire-while-moving with no per-cast resource pay; meter-based DR (drain-rate) is n/a at per-fight layer. Structurally identical to `vs-phieraggi` (V11 folded as NR/auto-fire, Wave-C precedent). Draft/offer-pool structure (hot's item pool; vs's pre-converged draft + per-level compound scaling) is META-LAYER — captured via `draft-meta-overlay-2026-07-17:offer-pool-hygiene` and `draft-meta-overlay-2026-07-17:pre-converged-draft` flags respectively, not blocking substrate.

Wave-D spec §4.2 C.1 stronger form authorizes NR-land over meter re-key; ruling exercises that stronger form.

Writes applied THIS RUN: **0** (this is READ-ONLY census). Writes previously landed in commit `29dee75e`.

**Wave-D engine-side changes (engine chain `5ed240a..8d8bd26`) do NOT alter census counts** — they are engine-seam parity work (vocab-loader repoint + simulation-fidelity ×4) that lives orthogonal to corpus.db classification. No engine_key/canon_corpus row writes were part of Wave-D landing.

---

## §4 Sheet projection cross-check

**Charge projection:** expressible 558 → 560; denominator UNCHANGED at 564 → 99.29%.

**Actual V12 result:** 560/564 = **99.29%**.

Δ vs charge projection: **+0** kits (+0.00pp) — EXACT MATCH.

---

## §5 Blocked-on-what — ranked buckets (V12)

| Bucket category | Kits touched | Sub-buckets |
|---|---|---|
| **shapeshift (GX-02 docket)** | 3 | mechanic:shapeshift=3 |
| **ailment-wave-c+ residue** | 1 | ailment-wave-c+:unknown-ailment=1 |

### §5b Bucket detail (individual buckets ranked)

| # | Bucket | Count |
|---|---|---|
| 1 | `mechanic:shapeshift` | 3 |
| 2 | `ailment-wave-c+:unknown-ailment` | 1 |

**econ:DR bucket: EMPTY** (was 2 in V11; both kits flipped via DR reclassify §3).

**No other bucket movement:** no econ, no ailment, no geometry deltas landed this pass. Wave-D engine-seam work is orthogonal to the classification substrate.

---

## §6 Blocked-tail rosters (DERIVED FROM DB)

Named kit rosters per residual blocker:

### `mechanic:shapeshift` (3 kits — Matt-fork GX-02 gate, forks A–E queued)
- `gd-berserker-wereforms` — Berserker (FoA mastery)
- `la-ferality-wildsoul` — Ferality Wildsoul (also dossier_owed)
- `la-phantom-beast-awakening-wildsoul` — Phantom Beast Awakening Wildsoul (also dossier_owed)

### `ailment-wave-c+:unknown-ailment` (1 kit — legolas re-crawl-gated)
- `di-spiritform-druid-pvp` — Spirit-Form Druid (complaint-tier)

**Cross-check DB-truth-vs-expected (per charge):**
- shapeshift bucket: **3 kits** (gd-berserker-wereforms, la-ferality-wildsoul, la-phantom-beast-awakening-wildsoul) — OK
- econ:DR bucket: **0 kits** (was 2 in V11; both flipped native) — OK
- unknown-ailment bucket: **1 kit** (di-spiritform-druid-pvp) — OK
- void-rift: phantom-negative per V11 §3 ruling (unchanged); NOT in blocked tail — OK

**Expected-residual gates:**
- shapeshift 3: Matt-fork GX-02 (forks A–E queued) — awaits ruling
- unknown-ailment 1: legolas re-crawl-gated — awaits Mode B follow-up

---

## §7 dossier_owed enumeration (sub-row split fix, corrects V11 defect)

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

**V11 defect this fixes:** V11 §1 collapsed dossier_owed onto a single "held-out" row alongside blocked as though the sub-row was a subset of blocked (`— of which dossier_owed held-out | 4 | 0.71%`). DB truth is that only 2 of the 4 are in the blocked bucket; the other 2 are already expressible. V12 §1 splits the row explicitly and §7 enumerates.

---

## §8 Iron-law asserts (PRE V11-state / POST V12-state)

| Assert | V11 (published) | V12 (this run) | Notes |
|---|---|---|---|
| total_corpus | 585 | 585 | UNCHANGED (no row writes) |
| total_engine_key | 585 | 585 | UNCHANGED |
| kit_grain | 563 | 563 | UNCHANGED |
| null_grain | 22 | 22 | UNCHANGED |
| **kit_positives (denominator base)** | **519** | **519** | UNCHANGED (DR reclassify preserves positives) |
| **kit_negatives** | **44** | **44** | UNCHANGED (no phantom writes) |
| **pool = corpus positives + roster 45** | **564** | **564** | UNCHANGED |
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
- `denominator identity`: 519 corpus positives + 45 roster = 564 == 564 — OK

---

## §9 Reproducibility & SQL derivations

**Backup:** `../corpus.db.pre-dr-reclassify-2026-07-17-backup` (pre-DR reclassify; V12 census reports POST-reclassify state)
**Ruling record:** `../atlas/dr-reclassify-2026-07-17.md`
**Wave-D engine chain:** `5ed240a..8d8bd26` (pushed)
**Wave-D Gate-2 note:** `agentic_orchestration/jack-ryan/notes/2026-07-17-wave-d-gate2.md`

**md5 stability:** pre-census `11f73ab3f000b9ada1492fe496e14e09` == post-census `11f73ab3f000b9ada1492fe496e14e09` → **True**

**SQL derivations (row-count verification discipline):**

Iron-law state derivation (§8):
```sql
SELECT COUNT(*) FROM canon_corpus;                                          -- 585 total
SELECT COUNT(*) FROM canon_corpus WHERE grain='kit';                        -- 563 kit-grain
SELECT COUNT(*) FROM canon_corpus WHERE grain IS NULL;                      -- 22 null-grain
SELECT COUNT(*) FROM canon_corpus WHERE grain='kit' AND negative=0;         -- 519 kit_positives
SELECT COUNT(*) FROM canon_corpus WHERE grain='kit' AND negative=1;         -- 44 kit_negatives
SELECT COUNT(*) FROM canon_engine_key;                                      -- 585 total
SELECT COUNT(*) FROM canon_engine_key WHERE cell_key IS NOT NULL;           -- 562 cell_key_resolved
SELECT COUNT(*) FROM canon_engine_key WHERE kit_id LIKE '%-bt';             -- 1 bt_sentinel
SELECT COUNT(*) FROM canon_engine_key WHERE row_class='combat-kit';         -- 563
SELECT COUNT(*) FROM canon_engine_key WHERE row_class='system-record';      -- 22
SELECT COUNT(*) FROM canon_corpus WHERE dossier_owed=1;                     -- 4
SELECT COUNT(*) FROM roster_atlas;                                          -- 45
```

DR reclassify verification (§3):
```sql
SELECT c.kit_id, ek.econ_status, ek.econ_gaps
FROM canon_corpus c JOIN canon_engine_key ek ON ek.kit_id=c.kit_id
WHERE c.kit_id IN ('hot-norseman-frost-avalanche', 'vs-queen-sigma');
-- → both rows: econ_status='native', econ_gaps='[]'
```

dossier_owed enumeration (§7):
```sql
SELECT c.kit_id, c.folk_name, ek.econ_status, ek.econ_gaps, ek.ctrl_ailment_gaps
FROM canon_corpus c LEFT JOIN canon_engine_key ek ON ek.kit_id=c.kit_id
WHERE c.dossier_owed=1
ORDER BY c.kit_id;
-- → la-ferality-wildsoul (shapeshift-blocked, dossier_owed)
-- → la-liberator-valkyrie (expressible, dossier_owed)
-- → la-phantom-beast-awakening-wildsoul (shapeshift-blocked, dossier_owed)
-- → la-shining-knight-valkyrie (expressible, dossier_owed)
```

Blocked-tail derivation (§5–§6): performed via classification logic mirroring V11:
- ECON_LANDED = {SU, HV, PC, RS, AM, RC, BT, TH, LC}
- AILMENT_LANDED = {damage-amp, freeze, stun, poison-dot, taunt, blind, curse/hex, fear, instant-kill, deflect}
- AILMENT_STILL_BLOCKED = {unknown-ailment}
- Shapeshift substring match: {wildsoul, wereforms, spirit-form, spiritborn-vortex} — excepting the vortex-spiritborn pair (d4-spiritborn-vortex is not blocked)

Result: 4 blocked kits — 3 shapeshift (gd-berserker-wereforms, la-ferality-wildsoul, la-phantom-beast-awakening-wildsoul) + 1 unknown-ailment (di-spiritform-druid-pvp). Zero econ:DR. Zero other residue.

---

## §10 Consumers & next re-run triggers

**Consumers:** governs S5 corpus→engine migration staging. V12 is the census snapshot published for the Wave-D-post-landing state.

**Next re-run triggers:**
1. Matt rules on GX-02 shapeshift docket (forks A–E queued) → shapeshift bucket resolves → V13
2. Legolas re-crawl on `di-spiritform-druid-pvp` unknown-ailment → V13
3. Matt vetoes DR reclassify → 2 kits return to blocked → V12.1
4. Matt vetoes phantom (`d2-wl-void-rift`) ruling from V11 → denominator returns to 565 → V-revert

**Wave-D closes end-to-end** at 99.29% pool-expressible. Blocked tail = 4 kits, all gated on named Matt-fork or legolas-recrawl decisions. This is the highest-ever migration-readiness score in the census lineage (V7→V12).
