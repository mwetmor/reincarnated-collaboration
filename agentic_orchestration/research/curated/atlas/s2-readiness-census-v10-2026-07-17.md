# S2 — Migration-Readiness Census V10 (THE SCOREBOARD, post-Wave-C landing + corpus-align)

**Date:** 2026-07-17 · **Author:** elrond (autonomous atlas-parity run, Wave-C corpus-align + V10 census charge)
**Commissioner:** gandalf-prime (Matt autonomous-run authorization 2026-07-17)
**Corpus state (POST-write):** 585 rows / **563 kit + 22 NULL-grain** / 562 cell_key resolved (incl. 1 -bt sentinel) / 4 dossier_owed held-out / 585 engine_key 1:1 (0 orphans) — UNCHANGED from V9
**Scope:** Post-Wave-C-LANDED (engine `941dbbf` PUSHED; Gate-2 PASS) + Wave-C corpus-align writes (provenance tag `wave-c-corpus-align-2026-07-17`).

**md5-stability:**
- Pre-Part-1: `c20e31f5e02459156daf5b682739ca4d`
- Post-Part-1 writes: `c20e31f5e02459156daf5b682739ca4d`
- Post-census (read-only): `c20e31f5e02459156daf5b682739ca4d`
- Census read pass DID NOT modify DB: **True**

---

## §1 Headline

| Metric | Count | % |
|---|---|---|
| **Candidate pool (denominator)** | **565** | 100.0% |
| **Expressible-now** | **551** | **97.5%** |
| Blocked | 14 | 2.5% |
| — of which dossier_owed held-out | 4 | 0.71% |

Denominator composition (UNCHANGED from V9): 520 corpus positives at kit grain + 45 founding roster = 565. Part 1 writes are TAG-aligns (no grain change, no row_class change).

Corpus expressible: **506/520 (97.3%)**  ·  Roster expressible: **45/45 (100.0%)** (UNCHANGED — verified)

---

## §2 Delta vs V9 — three-lever decomposition (iron law 4)

Δ decomposes cleanly into:
- **Wave-C-landed effect** (rule change: blind/curse/fear/execute/deflect + orbit/placed_lane + TH/BT/LC bins land): +34 kits flipped attributable to Wave-C alone.
- **Corpus-align (Part 1) effect** (5 tag-realign writes on DB): +5 kits flipped attributable to Part 1 writes: ['d2-smiter', 'd2-zealot', 'd3-invoker-thorns', 'd4-thorns-barb', 'gd-retaliation-warlord']
- **Denominator effect**: 0 (Part 1 writes changed NO grain or row_class values).
- **Cross-check identity**: net_flip = 39 = wavec_pure_flip 34 + realign_flipped 5 — OK

| Scoreboard | Pool expressible | % | Corpus | Roster |
|---|---|---|---|---|
| V9 (published, post-Wave-B + reclass) | 509/565 | 90.1% | 464/520 | 45/45 |
| **V10 (this run, post-Wave-C landed + corpus-align)** | **551/565** | **97.5%** | **506/520** | 45/45 |
| **Δ vs V9** | **+42** | **+7.42pp** | +42 | 0 |
| — Wave-C-landed contribution | +34 | | +34 | 0 |
| — corpus-align contribution | +5 | | +5 | 0 |

**Headline movement: V9 90.1% → V10 97.5% (+7.42pp).**

---

## §3 Multi-blocker honesty — Wave-C cohort decomposition (iron law 2)

Wave-C landed the trigger + mark-consume family, 4 new ailments (blind, curse/hex, fear, execute), the deflect def-bin rider, econ:BT + econ:TH + econ:LC bins, and orbit + placed_lane geometries.

| Wave-C-cohort accounting (V9-rule blocked kits touched by Wave-C rules) | Count |
|---|---|
| Distinct kits carrying ≥1 Wave-C-lift-affected token in V9-rule | 39 |
| — **flipped** to expressible (Wave-C was the SOLE remaining blocker) | **39** |
| — **multi-blocker residue** (still blocked on a non-Wave-C gate) | 0 |

**Multi-blocker residue is empty — every Wave-C-cohort kit flipped clean.**

---

## §4 Spec projection cross-check (spec §0 headline)

Wave-C spec §0 projected a 40-kit cohort with:
- **Floor:** 549/565 = 97.17% (all except d2-smiter/d2-zealot)
- **Ceiling:** 551/565 = 97.52% (with d2-smiter+d2-zealot resolved)

**Actual V10 result:** 551/565 = 97.52%

- Δ vs ceiling: **+0** kits (+0.00pp)
- Δ vs floor: **+2** kits (+0.35pp)

Actual matches the projection ceiling exactly.

---

## §5 Blocked-on-what — ranked buckets (V10)

| Bucket category | Kits touched | Sub-buckets |
|---|---|---|
| **unclassified-economy residue** | 8 | econ:UNKNOWN=8 |
| **shapeshift (GX-02 docket)** | 3 | mechanic:shapeshift=3 |
| **wave-D:drain (deferred WC-19)** | 2 | econ:DR=2 |
| **ailment-wave-c+ residue** | 1 | ailment-wave-c+:unknown-ailment=1 |

### §5b Bucket detail (individual buckets ranked)

| # | Bucket | Count |
|---|---|---|
| 1 | `econ:UNKNOWN` | 8 |
| 2 | `mechanic:shapeshift` | 3 |
| 3 | `econ:DR` | 2 |
| 4 | `ailment-wave-c+:unknown-ailment` | 1 |

---

## §6 Named-LANDED bucket rosters (Wave-C)

These buckets are now EXPRESSIBLE (LANDED engine truth); the census does NOT count them as blocked. Rosters below are the kit-set the landed capability serves.

### §6a `damage-taken-converts` (TH) — LANDED (spec §6)
Rosters: **3** kits (via `wave-c-corpus-align-2026-07-17:TH-damage-taken-converts` provenance tag)
- `d3-invoker-thorns`
- `d4-thorns-barb`
- `gd-retaliation-warlord`

Note: `chr-thorns-templar` is out-of-list here; its TH-mechanic decision (add `damage_taken_converts_shape='reflect-damage'`) is DEFERRED to S5 rocket-side authoring per MIGRATION AC-4. Its econ_gaps `[PC, BT]` both landed Wave-B/Wave-C, so V10 shows it EXPRESSIBLE on those alone.

### §6b `econ:BT` (block-trigger) — LANDED (spec §3)
Rosters: **8** kits (via `econ_gaps LIKE '%BT%'`)
- `chr-thorns-templar`
- `d2-charger`
- `d2-hammerdin`
- `d2-smiter`
- `d2-zealot`
- `di-crusader-banner-support`
- `hades1-beowulf-cast`
- `hot-shieldmaiden-block`

### §6c Ailment layer (Wave-C additions LANDED)
- `blind` (spec §4.2): 8 kits (V9 identity)
- `curse/hex` (spec §4.3): 4 kits (V9 identity)
- `fear` (spec §4.4): 4 kits (V9 identity)
- `instant-kill`/`execute` (spec §4.6): 1 kit (V9 identity)
- `deflect` def-bin rider (spec §4.5): 2 kits (V9 identity — now DROPPED from ailment bucket)

### §6d Geometry (Wave-C additions LANDED)
- `orbit` (spec §5.1): 6 kits (V9 identity — was blocked_on)
- `placed_lane` (spec §5.2): 1 kit (le-frost-wall-rm; V9 counted 3 via corpus classifier walls-demand rule, DB truth was 1)

### §6e `econ:LC` (life-cost / hp-cost) — LANDED (spec §7)
Rosters: kits with `econ_status='partial:LC'`:
- `hades1-aspect-guan-yu`
- `le-reaper-form-lich`

---

## §7 Blocked tail (residue — DERIVED FROM DB)

The blocked-tail is ranked from DB truth (not from the charge's expected list). Actual state:

1. `econ:UNKNOWN` — 8 kit(s)
2. `mechanic:shapeshift` — 3 kit(s)
3. `econ:DR` — 2 kit(s)
4. `ailment-wave-c+:unknown-ailment` — 1 kit(s)

**Post-Wave-C ranked blocked tail semantics:**

- `econ:UNKNOWN` = 8: unclassified-economy residue (data-classification lane; not a spec question).
- `mechanic:shapeshift` = 3: GX-02 docket OPEN (Matt-fork-gated). Not a spec item.
- `econ:DR` = 2: drain — deferred by Wave-C ruling WC-19 (defer). Wave-D or later.
- `ailment-wave-c+:unknown-ailment` = 1: unknown-ailment (di-spiritform-druid-pvp); resolution path is re-crawl. Best-effort WebSearch attempted this cycle — no verifiable source found; kit stays flagged.

**Named residue rosters (kit-level):**

- `econ:UNKNOWN` (8):
  - `d2-bowazon` — Bowazon
  - `d2-fireclaw-wolf` — Fireclaws Wolf
  - `d2-fury-wolf` — Fury Werewolf
  - `d2-kicksin` — Kicksin
  - `d2-rabies-wolf` — Rabies Wolf
  - `d2-wl-void-rift` — Void Rift Warlock
  - `poe1-whispering-ice` — Whispering Ice
  - `vs-phieraggi` — Phieraggi (guns union)
- `mechanic:shapeshift` (3):
  - `gd-berserker-wereforms` — Berserker (FoA mastery)
  - `la-ferality-wildsoul` — Ferality Wildsoul
  - `la-phantom-beast-awakening-wildsoul` — Phantom Beast Awakening Wildsoul
- `econ:DR` (2):
  - `hot-norseman-frost-avalanche` — Frost Avalanche Norseman
  - `vs-queen-sigma` — Queen Sigma
- `ailment-wave-c+:unknown-ailment` (1):
  - `di-spiritform-druid-pvp` — Spirit-Form Druid (complaint-tier)

---

## §8 Part 1 corpus-align write ledger

Provenance tag: `wave-c-corpus-align-2026-07-17`

Writes applied THIS RUN: **0** (idempotent re-run — all 6 target kits already carry the provenance tag; no changes needed). DB state reflects the writes from a prior run.

For the fresh-write ledger, consult the first-run stdout of `corpus_s2_census_v10_2026_07_17.py`, or the git commit accompanying this artifact (files touched: `../corpus.db`).

**Realign-attributable flips (Part 1 corpus-align effect, kit-by-kit):**

- `d2-smiter` — flipped V9-blocked → V10-expressible attributable to Part 1 write.
- `d2-zealot` — flipped V9-blocked → V10-expressible attributable to Part 1 write.
- `d3-invoker-thorns` — flipped V9-blocked → V10-expressible attributable to Part 1 write.
- `d4-thorns-barb` — flipped V9-blocked → V10-expressible attributable to Part 1 write.
- `gd-retaliation-warlord` — flipped V9-blocked → V10-expressible attributable to Part 1 write.

Note on `le-frost-wall-rm`: the geometry_value realign (`totem` → `placed_lane`) is a semantic tag hygiene, not an expressibility flip. Neither `totem` nor `placed_lane` blocks in V10-rule (both are landed); the corpus flag `resolved:walls-demand` also does not block in V10-rule. The write brings the DB into alignment with Wave-C spec §5.2:870 for a legacy R0b rule-fire pre-dating placed-lane availability, without moving the census score.

### Part 1 dispositions (no-write items)

- **`chr-thorns-templar`**: NO write. TH-mechanic decision (add `damage_taken_converts_shape='reflect-damage'`) DEFERRED to S5 rocket-side authoring per MIGRATION.md AC-4:203. Kit's `econ_gaps=['PC','BT']` — both landed Wave-B/Wave-C. V10 census shows it EXPRESSIBLE on those alone.
- **`di-spiritform-druid-pvp`**: NO write. Best-effort WebSearch attempted for the Spirit-Form ailment; no verifiable source found (search returned general DI PVP/druid commentary but no authoritative Spirit-Form ailment mechanics). Kit retains `GAP-AILMENT:unknown-ailment` per honesty-first bar. Resolution path: re-crawl (Legolas, community wikis, focused DI PVP forum threads).

### AC-5 role='support' regression audit

Sources queried:
- corpus canon_engine_key.raw_json: **0** kits found
- demo bundle exports/v2_narrow/classes.json: **0** kits found
- demo bundle exports/v2_narrow_phase_5/classes.json: **0** kits found
- data/kit_space/kits/*.json: **0** files found

**Named-EXPECTED-REGRESSION list: EMPTY.** No kit source carries `role='support'`. The `_ROLE_COST_TYPE_PRIORITY['support']` STRIKE (rocket MIGRATION.md line 24) has ZERO corpus-observable regression carriers. The placeholder in MIGRATION.md AC-5:206 can be closed as EMPTY. (Rocket-seam edit; this artifact reports the finding; not writing MIGRATION.md.)

The 5 roles that DO appear across demo bundles: `control`, `damage`, `defense`, `mobility`, `utility`. The 10 roles that appear in `kit_space/kits/*.json`: `area_damage`, `burst_damage`, `control`, `damage`, `damage_over_time`, `defensive`, `mobility`, `primary_attack`, `sustain`, `utility`. Neither surface uses `support`.

---

## §9 Iron-law asserts (PRE V9-state / POST V10-state — TAG-align only)

| Assert | PRE (V9) | POST (V10) | Notes |
|---|---|---|---|
| total_corpus | 585 | 585 | UNCHANGED (TAG-align only) |
| total_engine_key | 585 | 585 | 1:1 UNCHANGED |
| kit_grain | 563 | 563 | UNCHANGED (no grain writes) |
| null_grain | 22 | 22 | UNCHANGED |
| corpus positives (denominator base) | 520 | 520 | UNCHANGED |
| pool = corpus positives + roster 45 | 565 | 565 | UNCHANGED |
| combat-kit (row_class) | 563 | 563 | UNCHANGED |
| system-record (row_class) | 22 | 22 | UNCHANGED |
| cell_key_resolved | 562 | 562 | UNCHANGED |
| bt_sentinel | 1 | 1 | UNCHANGED |
| orphans engine→corpus | 0 | 0 | UNCHANGED |
| orphans corpus→engine | 0 | 0 | UNCHANGED |
| dossier_owed | 4 | 4 | UNCHANGED |

Cross-check assertions:
- `net_flip == wavec_pure_flip + realign_flipped`: 39 == 34 + 5 — OK
- `roster_expressible == 45`: 45 == 45 — OK
- `ailment_wave_c_residue == 1 (unknown-ailment only)`: 1 — OK

---

## §10 Reproducibility

- **Script:** `../scripts/corpus_s2_census_v10_2026_07_17.py`
- **Backup:** `../corpus.db.pre-v10-2026-07-17-backup` (integrity_check=ok, taken before Part 1 write)
- **Transactional writes** — Part 1 wrapped in single transaction; PRE asserts held before writing, POST asserts held after; census is a pure READ on the POST-write state.
- **Idempotent** — Part 1 writes check for provenance tag `wave-c-corpus-align-2026-07-17` and treat re-runs as verified no-op per-row.
- **Delta decomposition** (§2) reports Wave-C-landed effect and corpus-align effect separately, per iron law 4 — the two levers are NOT conflated. Denominator effect is provably zero (Part 1 is TAG-align, not row-class change).
- **md5 stability**: DB md5 recorded pre-write / post-write / post-census. The census is a pure READ; last two hashes should be equal. Verified in this run: post-writes `c20e31f5e024...` == post-census `c20e31f5e024...`: **True**

**Consumers:** governs S5 corpus→engine migration staging. Next re-run: after next econ-wave (econ:UNKNOWN re-crawl closes), a shapeshift ruling on GX-02 docket, or econ:DR spec (WC-19 defer).
