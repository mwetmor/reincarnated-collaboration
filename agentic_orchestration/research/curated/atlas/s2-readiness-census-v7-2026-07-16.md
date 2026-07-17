# S2 — Migration-Readiness Census V7 (THE SCOREBOARD)

**Date:** 2026-07-16 · **Author:** elrond (autonomous atlas-parity run, cycle 2, S2 charge)
**Commissioner:** gandalf-prime (Matt authorization 2026-07-16)
**Corpus state:** 585 rows / 566 kit + 19 NULL-grain / 562 cell_key resolved (incl. 1 -bt sentinel) / 4 dossier_owed held-out / 585 engine_key 1:1 (0 orphans)
**Scope:** Post-S1 completion (`62721bdd`), post-Wave-A close, ailment layer IN FLIGHT (rocket+gamora cycle 2 bg — NOT LANDED YET).

---

## §1 Headline

| Metric | Count | % |
|---|---|---|
| **Candidate pool (denominator)** | **568** | 100.0% |
| **Expressible-now** | **258** | **45.4%** |
| Blocked | 310 | 54.6% |
| — of which dossier_owed held-out | 4 | 0.70% |

Denominator composition: 523 corpus positives at kit grain + 45 founding roster = 568. Negatives (43 kit-grain), NULL-grain system-records (19), and grain=NULL mints (2, captured under NULL-grain exclusion) EXCLUDED per spec.

Corpus expressible: **213/523 (40.7%)**  ·  Roster expressible: **45/45 (100.0%)**

Roster (45 K/H/B) is SPEC ANCHOR — the engine's first-class targets. Wave-A close (proxy family) enables the 4 proxy-hosted H-cells (H1/H2/H3/H4). Roster block classified as expressible-now at the geometry+economy layer; ailment overlays land per emission at §7 (§F.5(1) mechanics-buildout objective).

---

## §2 Blocked-on-what — ranked buckets (all corpus-side)

| Bucket category | Kits touched | Sub-buckets |
|---|---|---|
| **ailment-in-flight (Gate-2 pending)** | 222 | ailment-in-flight:damage-amp=97; ailment-in-flight:freeze=42; ailment-in-flight:poison-dot=36; ailment-in-flight:stun=36; ailment-in-flight:taunt=11 |
| **wave-B:persistent-cost** | 44 | econ:PC=44 |
| **wave-B:reserved-slot** | 42 | econ:RS=42 |
| **unclassified-economy** | 38 | econ:UNKNOWN=38 |
| **ailment-wave-c+** | 21 | ailment-wave-c+:blind=8; ailment-wave-c+:curse/hex=4; ailment-wave-c+:fear=4; ailment-wave-c+:deflect=2; ailment-wave-c+:unknown-ailment=2; ailment-wave-c+:instant-kill=1 |
| **wave-B:attunement-meter** | 16 | econ:AM=16 |
| **wave-B:recharge** | 16 | econ:RC=16 |
| **small-add:block-trigger-BT** | 8 | econ:BT=8 |
| **small-add:orbit-25th-geo** | 6 | geometry:orbit=6 |
| **wave-B/C:life-cost-drain** | 5 | econ:LC=3; econ:DR=2 |
| **shapeshift (GX-02 docket bg)** | 3 | mechanic:shapeshift=3 |
| **small-add:walls-placed-lane** | 3 | geometry:walls-placed-lane=3 |

**Reading the buckets:**

- `ailment-in-flight` = spec landed (`ailment-layer-engine-spec.md`), Gate-1 PASS (`c8fcf5b2`), implementation cycle 2 bg (rocket+gamora, `PROXY_TAUNT_PRIORITY` first / gamora consumes last). **Post-Gate-2 rerun** will flip these to expressible-now. Damage-amp = `sunder` (ruling 5).
- `ailment-wave-c+` = blind, fear, curse/hex, instant-kill, deflect, unknown-ailment — NOT in current spec; Wave-C or beyond. `unknown-ailment` = legolas probe couldn't resolve (2 kits) — audit re-crawl candidates.
- `wave-B:*` = reservation/aura + persistent-cost + attunement-meter + recharge — Wave B family (not yet spec'd).
- `small-add:*` = orbit-25th-geo (6 kits), walls-placed-lane (~3 kits per Q15), block-trigger-BT — post-Wave-C small adds.
- `shapeshift` = GX-02 keystone (Wildsoul ×2 + PBA + gd-berserker-wereforms). Docket drafter bg cycle 2.

---

## §3 Bucket detail (top individual buckets)

| # | Bucket | Count |
|---|---|---|
| 1 | `ailment-in-flight:damage-amp` | 97 |
| 2 | `econ:PC` | 44 |
| 3 | `ailment-in-flight:freeze` | 42 |
| 4 | `econ:RS` | 42 |
| 5 | `econ:UNKNOWN` | 38 |
| 6 | `ailment-in-flight:poison-dot` | 36 |
| 7 | `ailment-in-flight:stun` | 36 |
| 8 | `econ:AM` | 16 |
| 9 | `econ:RC` | 16 |
| 10 | `ailment-in-flight:taunt` | 11 |
| 11 | `ailment-wave-c+:blind` | 8 |
| 12 | `econ:BT` | 8 |
| 13 | `geometry:orbit` | 6 |
| 14 | `ailment-wave-c+:curse/hex` | 4 |
| 15 | `ailment-wave-c+:fear` | 4 |
| 16 | `econ:LC` | 3 |
| 17 | `geometry:walls-placed-lane` | 3 |
| 18 | `mechanic:shapeshift` | 3 |
| 19 | `ailment-wave-c+:deflect` | 2 |
| 20 | `ailment-wave-c+:unknown-ailment` | 2 |
| 21 | `econ:DR` | 2 |
| 22 | `ailment-wave-c+:instant-kill` | 1 |

---

## §4 Delta vs V6 (baseline: prior thinking-state, no live V6 artifact — this is the first live-executed scoreboard)

V6 was gandalf's mental scoreboard entering the run (charter §1). This V7 makes it executable. Delta framing is therefore against V6-implied targets:

- **Wave A LANDED delta:** proxy/summon economies (SU + HV bins) flipped to expressible-now — ~0 kits no longer blocked on economy-family gates (V6 pre-Wave-A: blocked; V7 post-Wave-A: expressible).
- **Ailment layer NOT LANDED yet:** in-flight ailment buckets remain blocked in V7. Post-Gate-2 rerun (V8) will show the sunder+freeze+stun+poison-dot+taunt cohort flip.
- **Small-add adjacencies exposed:** orbit-25th-geo (6 kits), walls-placed-lane (3 kits), block-trigger-BT (3+8=11 kits) — now empirically loaded for pause-2/V3 sequencing.
- **Shapeshift docket cohort:** 3 kits touched by mechanic:shapeshift → drives GX-02 docket scope (dossier evidence + gd attestation).

---

## §5 kb-URL backfill (rider payload)

Applied to `canon_corpus.source_urls` from legolas sheet (`agentic_orchestration/legolas/research/la-postcutoff-dossiers-2026-07-16/kb-url-backfill-sheet.md`):

| Disposition | Sheet-summary count | Sheet-rows actual | Applied (writes) |
|---|---|---|---|
| confirm | 35 | 34 | 33 |
| correct | 4 | 3 | 4 |
| unverifiable (flagged) | 13 | 15 | 15 |
| TOTAL | 52 | 52 | 52 |

**Sheet-integrity note (doc-authority rule):** the legolas sheet's summary block (§ "Backfill sheet totals" — 35/4/13) does NOT reconcile with its own row-by-row `**disposition**` markers (34/3/15) NOR with its § "Notes for Elrond application pass" list of 4 corrections. Two axes of tension:

- `d4-blazing-abyss-warlock`: row marker = `**confirm**` (with correction note "meta-name evolved to Blazing Scream"); Notes list treats it as correct-class. Applied under **correct** disposition (URL + `backfill-correct-2026-07-16:<rename>` flag) — the correction is real and future audits will need the flag.
- The 15 unverifiable rows (rows 5/6/8/11/13/15/16/23/31/32/34/35/36/37/40 per verbatim marker) all got the `kb-only-backfill-attempted-2026-07-16` flag. Sheet summary count of 13 undercounts by 2.

Doc wins on **row-level markers** — applied numbers therefore honor the actual rows (33 confirm-writes + 4 correct-writes + 15 unverifiable-flags) rather than the sheet summary. All 52 rows touched; no data lost; every action auditable via flag/URL/schema-meta record. Legolas summary-count discrepancy filed as an audit note (not blocking).

Unverifiable rows carry `flags += 'kb-only-backfill-attempted-2026-07-16'`; corrected rows carry `flags += 'backfill-correct-2026-07-16:<note>'`. dossier_owed = 4 UNTOUCHED (E-next admission).

---

## §6 Held-out list (4 dossier_owed — pool members, flagged NOT-YET-EMISSIBLE)

- `la-ferality-wildsoul` — Ferality Wildsoul
- `la-liberator-valkyrie` — Liberator Valkyrie
- `la-phantom-beast-awakening-wildsoul` — Phantom Beast Awakening Wildsoul
- `la-shining-knight-valkyrie` — Shining Knight Valkyrie

These are IN the denominator (§F.5(1) candidate pool) but held-out per E4 T4/P-1 — legolas dossiers landed cycle 1; E-next admission behind Matt E4 ratification. GX-02 SHAPESHIFT keystone bears on Wildsoul ×2.

---

## §7 Iron-law asserts (held PRE + POST)

| Assert | Expected | Notes |
|---|---|---|
| total_corpus | 585 | census is a READ; backfill is column-value-only |
| total_engine_key | 585 | 1:1 |
| kit_grain | 566 | denominator base: 523 positives |
| null_grain | 19 | excluded from pool |
| cell_key_resolved | 562 | incl. 1 -bt sentinel |
| bt_sentinel | 1 | -bt placeholder |
| orphans engine→corpus | 0 | |
| orphans corpus→engine | 0 | |
| dossier_owed | 4 | UNTOUCHED |

---

## §8 Reproducibility

- **Script:** `../scripts/corpus_s2_census_v7_and_kb_backfill_2026_07_16.py`
- **Backup:** `../corpus.db.pre-s2-census-v7-2026-07-16-backup` (integrity_check=ok)
- **Idempotent** — re-run yields identical POST asserts; backfill guarded by `WHERE source_urls IS NULL OR ''` predicate + flag idempotency.
- **Transactional** — rolls back on any assert breach; sys.exit non-zero.

**Consumers:** this scoreboard governs S5 corpus→engine migration staging (`current-to-end-state-serial-content-emission.md` §5). Wave-B/C sequencing takes cues from bucket-count ranking. Next re-run: after ailment Gate-2 (V8 delta).
