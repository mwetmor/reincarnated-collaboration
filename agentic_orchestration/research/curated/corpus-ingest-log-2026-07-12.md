# Corpus Ingest Log — 2026-07-12

**Author:** elrond
**Date:** 2026-07-12
**Authorization:** Matt Q24(a)/(b)/(c) + ADR-006
**Script:** `agentic_orchestration/research/scripts/corpus_ingest_2026_07_12.py`
**DB:** `agentic_orchestration/research/curated/corpus.db` (gitignored)
**DDL:** `agentic_orchestration/research/scripts/catalogue_migrations/corpus_v2_0_three_layer.sql`

---

## Row Counts

| Table | Rows | Notes |
|---|---|---|
| `canon_corpus` | 524 | 515 CSV canon + 9 mint (source='mint') |
| `canon_probe_facts` | 4780 | 478 positive kits × 10 families each |
| `canon_engine_key` | 478 | combat-kit=463 / system-record=15 |
| `roster_atlas` | 45 | rebuilt roster (Q24(b)) |
| `roster_lineage_enrichment` | 45 | bc6 + lineage + neighbor analysis |

### canon_corpus breakdown

| Segment | Count |
|---|---|
| source=canon (CSV) | 515 |
| source=mint (harvest holes) | 9 |
| negative=1 | 37 |
| is_system=1 | 18 |
| mint=1, dossier_owed=1 | 9 |
| game=hot, tier=T3, tier_confirm_pending=0 | 19 |

---

## Post-Ingest Asserts (all passed)

- canon_corpus = 524 (515 + 9 mint)
- source=canon = 515
- is_system = 18
- negative = 37
- HoT = 19 (tier=T3, tier_confirm_pending=0 per Q24(c))
- mint = 9
- probe_facts distinct kits = 478
- engine_key combat-kit = 463
- engine_key system-record = 15
- roster_atlas = 45
- roster_lineage_enrichment = 45 (0 dangling FK refs)

---

## Acceptance Harness (D6 — boards-v1.md)

### Matched counts

| Board | Metric | Expected | Got | Status |
|---|---|---|---|---|
| Board 2 | combat denominator | 463 | 463 | MATCH |
| Board 2 | system-record | 15 | 15 | MATCH |
| Board 2 | ground_targeted_circle | 102 | 102 | MATCH |
| Board 2 | circle | 69 | 69 | MATCH |
| Board 2 | totem | 48 | 48 | MATCH |
| Board 2 | multi_projectile | 41 | 41 | MATCH |
| Board 2 | single_target | 38 | 38 | MATCH |
| Board 2 | melee_strike | 37 | 37 | MATCH |
| Board 2 | chain | 28 | 28 | MATCH |
| Board 2 | whirlwind | 15 | 15 | MATCH |
| Board 2 | dash_attack | 14 | 14 | MATCH |
| Board 2 | vortex_pull | 12 | 12 | MATCH |
| Board 2 | cone | 11 | 11 | MATCH |
| Board 2 | ring | 9 | 9 | MATCH |
| Board 2 | aura | 8 | 8 | MATCH |
| Board 2 | line | 8 | 8 | MATCH |
| Board 2 | orbit (gx-candidate:orbit) | 4 | 4 | MATCH |
| Board 1 | SU demand (totem + ratified) | 48 | 48 | MATCH |
| Board 3 | damage-amp unique kits | 97 | 97 | MATCH |
| Board 3 | stun | 36 | 36 | MATCH |
| Board 3 | poison-dot | 36 | 36 | MATCH |
| Board 4 | tank | 215 | 215 | MATCH |
| Board 4 | mitigate | 84 | 84 | MATCH |
| Board 4 | glass | 67 | 67 | MATCH |
| Board 4 | evade | 66 | 66 | MATCH |
| Board 4 | absorb | 28 | 28 | MATCH |
| Board 4 | FLAGGED (NULL def_bin) | 14 | 14 | MATCH |
| Board 4 | post-cutoff-deferred | 4 | 4 | MATCH |

### Source-data mismatches (2) — faithfully reported; data NOT adjusted

**Mismatch 1 — Board2: walls**
- Board says 3 (d2-firewall-sorc, le-frost-wall-rm, di-bone-wall-necro-pvp)
- Engine-key has J-GEO:placed-lane flag on only 2 kits (d2-firewall-sorc, di-bone-wall-necro-pvp)
- le-frost-wall-rm: flags=[] in engine-key; geometry=totem; board may use Q15-workstream classification not reflected in flags
- DB stores what the engine-key provides. Count from DB: 2. Forward work: gandalf to add J-GEO:placed-lane (or equivalent) flag to le-frost-wall-rm in engine-key v1.1.

**Mismatch 2 — Board3: freeze**
- Board says 43 distinct kits with GAP-AILMENT:freeze
- Engine-key (corpus-engine-key-v1.jsonl, 478 rows) contains exactly 42 distinct kits with that gap
- The 1-kit discrepancy is between the board generator's source and the delivered engine-key JSONL. No kit has a partial freeze signal that accounts for the difference.
- DB stores what the engine-key provides. Count from DB: 42. Forward work: gandalf to identify which kit the board counted as freeze-gap that the engine-key does not.

---

## D4 Reconciliation — CSV is_system vs EK system-record

| Classification | Count |
|---|---|
| CSV is_system=1 (SYS key_group/flags) | 18 |
| EK row_class=system-record | 15 |
| Overlap (both) | 12 |

**CSV-sys-only (engine-key classifies as combat-kit):**
chr-crown-proc-engine, d3-lod-archetype, le-low-life-ward, poe2-grim-feast, poe2-temporalis-blink, vs-golden-egg-scaling (6 kits)

Note: vs-golden-egg-scaling is absent from the engine-key entirely (478 rows; not keyed).

**EK-sys-only (not SYS-flagged in CSV):**
tli-sage-elixir (route: consumable-economy), ud-multishot-link (route: modifier-grammar), vs-big-trouser (route: meta-currency) (3 kits)

**Interpretation:** Expected divergence per DELTA v2 §D4. Different evidence sources: CSV used probe-pass SYS key_group classification; EK used judgment-resolution-based row_class assignment. Layer-3 row_class governs all combat denominators. CSV is_system column retained as alternative signal (both columns survive in DB).

---

## Curation Findings

1. **Mint kits not in CSV (9):** All 9 mint kits (d2-sacrifice, d2-teleport-sorc, d3-call-of-the-ancients, d3-dashing-strike-monk, le-shift-bladedancer, poe1-blood-magic-kit, poe1-ring-of-shields, poe1-totem-hierophant, poe1-vaal-blade-vortex) are harvest holes — present in mint-dossiers-reexpressed.jsonl but absent from rdr-kit-atlas-v3.csv and corpus-engine-key-v1.jsonl. Ingested as source='mint', mint=1, dossier_owed=1. Not keyed (no Layer-2/3 rows for these kits).

2. **vs-golden-egg-scaling absent from engine-key:** CSV is_system=1 (SYS key_group = "SYS|eternal-stat-inflation") but not in the 478-row engine-key JSONL. No Layer-3 row. Layer-1 row ingested with is_system=1.

3. **le-frost-wall-rm wall-flag gap:** geometry=totem in engine-key (R0b rule); flags=[] (no J-GEO:placed-lane). Board lists it in walls group (3 kits). The wall classification may rely on Q15-workstream designation not captured as a flag in the engine-key. Candidate for a flag addition in a future engine-key update.

4. **Board3 freeze count discrepancy (42 vs 43):** Engine-key has 42 distinct kits with GAP-AILMENT:freeze in ctrl.ailment_gaps. Board says 43. The missing kit is not identifiable from the data at hand (all known freeze-variant labels checked; vs-infinite-corridor-crimson-shroud appears once as distinct; no system-record carries freeze gap). Candidate for gandalf review of the board generator output.

5. **def_bin FLAGGED stored as NULL:** The engine-key stores None (not the string 'FLAGGED') for 14 kits with flagged defensive classification (all system-records with resolved:system-record flag). Acceptance query uses IS NULL; future consumers should be aware that NULL def_bin = FLAGGED in this layer, per the flag column evidence.

---

## Reversibility

corpus.db is gitignored. Clean rebuild: run `corpus_ingest_2026_07_12.py` from the collaboration repo root. Inputs are deterministic (v3 CSV + engine-key JSONL + probe JSONL + roster CSV + lineage JSONL — all committed to git). Output is byte-identical SQLite state.
