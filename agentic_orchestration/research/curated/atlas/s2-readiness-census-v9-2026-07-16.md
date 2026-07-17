# S2 — Migration-Readiness Census V9 (THE SCOREBOARD, post-Wave-B rerun)

**Date:** 2026-07-16 · **Author:** elrond (autonomous atlas-parity run, cycle 3, CENSUS V9 charge)
**Commissioner:** gandalf-prime (Matt authorization 2026-07-16)
**Corpus state (POST-reclass):** 585 rows / **563 kit + 22 NULL-grain** / 562 cell_key resolved (incl. 1 -bt sentinel) / 4 dossier_owed held-out / 585 engine_key 1:1 (0 orphans)
**Scope:** Post-Wave-B-LANDED (jack-ryan Gate-2 PASS-WITH-AMENDMENTS, engine `b850800` PUSHED; rocket `4f2548e`/`33ffc86`/`176f353` + gamora `1a0e5e4`/`e81f3f9`/`c037c5b`/`41e45f6`) + ruling-11 IT/UT reclass EXECUTED (3 rows). corpus.db written for reclass; classifier is a pure READ.

---

## §1 Headline

| Metric | Count | % |
|---|---|---|
| **Candidate pool (denominator)** | **565** | 100.0% |
| **Expressible-now** | **509** | **90.1%** |
| Blocked | 56 | 9.9% |
| — of which dossier_owed held-out | 4 | 0.71% |

Denominator composition: 520 corpus positives at kit grain + 45 founding roster = 565. Denominator dropped 568→565 per ruling-11 (3 IT/UT rows reclassified out to `system-record`). Negatives (43 kit-grain), NULL-grain system-records (22 post-reclass), and grain=NULL mints EXCLUDED per spec.

Corpus expressible: **464/520 (89.2%)**  ·  Roster expressible: **45/45 (100.0%)** (UNCHANGED — verified)

Roster (45 K/H/B) is SPEC ANCHOR — the engine's first-class targets; Wave-A close covers the proxy-hosted H-cells, ailment overlays land per emission, Wave-B economy family (PC/RS/AM/RC) now live. Expressible-now at the geometry+economy+ailment layers.

---

## §2 Multi-blocker honesty — the Wave-B flip decomposed (iron law 2)

Wave-B economy LANDED, so the 4 in-flight econ tokens that V8 scored blocked (econ:PC persistent-condition · econ:RS reservation · econ:AM attunement-meter · econ:RC recharge) are now expressible engine truth. But **a kit blocked on Wave-B AND econ:UNKNOWN does NOT flip just because Wave-B landed.** The census unions ALL blockers per kit; a kit is expressible only when its ENTIRE blockset is empty.

| Wave-B-cohort accounting | Count |
|---|---|
| Distinct kits carrying ≥1 now-landed Wave-B econ token (the **cohort**) | 125 |
| — **flipped** to expressible (Wave-B was the SOLE remaining blocker) | **113** |
| — **multi-blocker residue** (still blocked on a non-Wave-B gate) | 12 |

The kit-grain flip is **113**, matching the V8→V9 corpus-expressible net delta (cross-check: V8-rule corpus expressible on the V9 denominator = 351; V9-rule = 464; Δ = 113; assert `net_flip == wb_flipped`). The V8-published `econ:PC` 44 · `econ:RS` 42 · `econ:AM` 16 · `econ:RC` 16 counts were token-touches with duplication (a kit can carry >1 Wave-B token); the 125 cohort kits collectively hold those tokens, and 12 of them remain gated by a non-Wave-B blocker.

**Multi-blocker residue — what the 12 Wave-B-cohort kits are still blocked on** (token-touches; a kit can carry >1):

| Residual blocker | Cohort kits still gated |
|---|---|
| `econ:BT` | 3 |
| `ailment-wave-c+:blind` | 3 |
| `ailment-wave-c+:fear` | 2 |
| `ailment-wave-c+:curse/hex` | 2 |
| `mechanic:shapeshift` | 1 |
| `econ:LC` | 1 |

Reading: of the 12 residue kits, the dominant re-block is now **ailment-wave-c+** (blind + fear + curse/hex accumulate to ~7 of the 12) and **econ:BT** (3 kits) — i.e. the Wave-B flip hands off directly to the ailment-wave-c+ closure batch and the block-trigger small-add as the next levers. A handful are re-blocked on shapeshift or LC/DR (Wave-C).

---

## §3 Blocked-on-what — ranked buckets (V9, all corpus-side)

| Bucket category | Kits touched | Sub-buckets |
|---|---|---|
| **ailment-wave-c+** | 20 | ailment-wave-c+:blind=8; ailment-wave-c+:curse/hex=4; ailment-wave-c+:fear=4; ailment-wave-c+:deflect=2; ailment-wave-c+:instant-kill=1; ailment-wave-c+:unknown-ailment=1 |
| **unclassified-economy** | 13 | econ:UNKNOWN=13 |
| **small-add:block-trigger-BT** | 8 | econ:BT=8 |
| **small-add:orbit-25th-geo** | 6 | geometry:orbit=6 |
| **wave-C:life-cost-drain** | 5 | econ:LC=3; econ:DR=2 |
| **shapeshift (GX-02 docket bg)** | 3 | mechanic:shapeshift=3 |
| **small-add:walls-placed-lane** | 3 | geometry:walls-placed-lane=3 |

**Reading the buckets (post-Wave-B-landed):**

- The 4 in-flight Wave-B econ buckets (PC/RS/AM/RC) are GONE from the blocked ledger — they landed (`b850800`).
- `ailment-wave-c+` = 20 token-touches (blind 8 / curse-hex 4 / fear 4 / deflect 2 / unknown-ailment 1 / instant-kill 1) — NOT in the landed spec; stays blocked (iron law 3). NOTE: V8 headline said 21; actual DB state was 20 (verified via V8-rule re-execution). See §5 corpus-hygiene note.
- `unclassified-economy` (`econ:UNKNOWN`) dropped 16 → 13 (−3 via ruling-11 reclass: the 3 IT/UT rows that were carrying UNKNOWN left the denominator, they weren't reclassified within it). 18 residual kits carry `econ-audit-ambiguous-2026-07-16` for a future re-crawl (unchanged from V8).
- `small-add:*` = orbit-25th-geo (6), walls-placed-lane (3), block-trigger-BT (8) — post-Wave-C small adds. UNCHANGED from V8.
- `wave-C:life-cost-drain` (`econ:LC` 3 + `econ:DR` 2) — Wave-C per Gate-1 ruling. UNCHANGED.
- `shapeshift` = GX-02 keystone (gd-berserker-wereforms + 2 in-pool Wildsoul); +2 held-out Wildsoul in §6.

---

## §3b Bucket detail (top individual buckets)

| # | Bucket | Count |
|---|---|---|
| 1 | `econ:UNKNOWN` | 13 |
| 2 | `ailment-wave-c+:blind` | 8 |
| 3 | `econ:BT` | 8 |
| 4 | `geometry:orbit` | 6 |
| 5 | `ailment-wave-c+:curse/hex` | 4 |
| 6 | `ailment-wave-c+:fear` | 4 |
| 7 | `econ:LC` | 3 |
| 8 | `geometry:walls-placed-lane` | 3 |
| 9 | `mechanic:shapeshift` | 3 |
| 10 | `ailment-wave-c+:deflect` | 2 |
| 11 | `econ:DR` | 2 |
| 12 | `ailment-wave-c+:instant-kill` | 1 |
| 13 | `ailment-wave-c+:unknown-ailment` | 1 |

---

## §4 Delta vs V8 (published baseline: 385/568 = 67.8%)

The V8→V9 delta has **two levers** that must be reported separately (per iron law 4 — do not conflate):
- **Denominator change** (ruling-11 reclass): 568 → 565. The 3 reclassified rows were BLOCKED in V8 (all carried `econ:UNKNOWN`), so V8's expressible tally (385) is preserved on the new denominator. Effect: 385/568 (67.8%) → 385/565 (68.14%) = +0.34pp mechanical.
- **Wave-B flip** (real gain): 385 → 509 = +124 kits expressibility gained on the 565-row denominator = +21.95pp.

| Scoreboard | Pool expressible | % | Corpus | Roster |
|---|---|---|---|---|
| V8 (published, post-ailment + econ-audit) | 385/568 | 67.8% | 340/523 | 45/45 |
| V8-adjusted (on V9 denominator, no Wave-B flip yet) | 385/565 | 68.14% | 340/520 | 45/45 |
| **V9 (this run, post-Wave-B + reclass)** | **509/565** | **90.1%** | **464/520** | 45/45 |
| **Δ vs V8 published** | **+124** | **+22.29pp** | +124 | 0 |
| — denominator-change contribution | 0 | +0.34pp | 0 | 0 |
| — Wave-B flip contribution | +124 | +21.95pp | +124 | 0 |

**Headline movement: 67.8% → 90.1% (+22.29pp).** The +124 pool-expressible decomposes cleanly:
- **+0.34pp denominator effect** (ruling-11 reclass — 3 UNKNOWN-blocked rows left the frame; no expressibility gained, just a smaller denominator).
- **+124 kits flipped** (Wave-B economy landed) = **+21.95pp Wave-B contribution**. 12 Wave-B-cohort kits did NOT flip (multi-blocked — §2).

**Per-bucket flips (V8 blocked → V9):**

| Bucket | V8 | V9 | Δ |
|---|---|---|---|
| `econ:PC` | 44 | 0 (LANDED) | −44 |
| `econ:RS` | 42 | 0 (LANDED) | −42 |
| `econ:AM` | 16 | 0 (LANDED) | −16 |
| `econ:RC` | 16 | 0 (LANDED) | −16 |
| `econ:UNKNOWN` | 33 | 13 | −20 (audit closed 17 + reclass removed 3) |
| `econ:BT` | 8 | 8 | 0 (frozen — Wave-C small-add) |
| `econ:LC` / `DR` | 3+2=5 | 3+2=5 | 0 (frozen — Wave-C) |
| `ailment-wave-c+:*` | 20 | 20 | 0 (frozen — not in landed spec; V8 header said 21 but actual DB was already 20 — corpus-hygiene note in §5) |
| `geometry:orbit` / `walls-placed-lane` / `mechanic:shapeshift` | 6+3+3 | 6+3+3 | 0 (frozen — post-Wave-C) |

**New blocked-bucket ranking (top 5 — feeds post-Wave-B sequencing):**

| Rank | Bucket | Kits |
|---|---|---|
| 1 | `econ:UNKNOWN` | 13 |
| 2 | `ailment-wave-c+:blind` | 8 |
| 3 | `econ:BT` | 8 |
| 4 | `geometry:orbit` | 6 |
| 5 | `ailment-wave-c+:curse/hex` | 4 |

With the Wave-B cohort cleared, **the residue tail is now `ailment-wave-c+` + `econ:UNKNOWN` + small-adds** — no single lever comparable in size to the Wave-B family. Next-wave sequencing should target the UNKNOWN-audit-residue re-crawl (18 kits carry `econ-audit-ambiguous-2026-07-16`) and the ailment-wave-c+ closure batch.

---

## §5 Ruling-11 reclassification record

Delegated ruling 11 (decisions-log ~5910, ratified into engine at Gate-2 `b850800`) executes at V9 per its own timing clause. 3 kits reclassify from `combat-kit` (grain='kit') to `system-record` (grain=NULL) because their 'economy' is build-construction / account-progression, not per-fight resource operation — no combat bin exists for them.

| kit_id | folk_name | game | route | reclass flag |
|---|---|---|---|---|
| `d3-lod-archetype` | Legacy of Dreams (setless archetype) | d3 | `itemization-meta` | `ruling-11-reclass-2026-07-16` |
| `vs-red-death` | Red Death / Mask of the Red Death | vs | `unlock-meta` | `ruling-11-reclass-2026-07-16` |
| `vs-vlad-dracula` | Vlad Tepes Dracula | vs | `unlock-meta` | `ruling-11-reclass-2026-07-16` |

**Denominator arithmetic:** pool 568→565 · corpus positives 523→520 · kit_grain 566→563 · null-grain 19→22 · row_class combat-kit 566→563 · row_class system-record 19→22. Total 585 UNCHANGED · engine_key 1:1 585 UNCHANGED · dossier_owed 4 UNTOUCHED.

**Reversibility:** the `ruling-11-reclass-2026-07-16` flag on each of the 3 rows makes reversal trivial (one SQL UPDATE per row: restore grain='kit', row_class='combat-kit', clear route, drop the flag). Matt-veto window remains open per ruling-11's ratification clause. Backup at `corpus.db.pre-v9-2026-07-16-backup` (integrity_check=ok).

**Convention followed:** identical to the existing 19 system-records — `grain=NULL`, `grain_note` stamped with 'system-record: not kit/gear/class emittable; excluded from fits by row_class', populated `route`, `flags` array carries `resolved:system-record` + reclass audit flag.

**Corpus-hygiene note (ailment-wave-c+ count):** V8's published headline for `ailment-wave-c+` was 21 token-touches; actual DB state at V8-time was 20 (verified by V8-rule re-execution on current DB: 20). The delta appears to reflect either an editorial rounding-up on V8's write, or a stale count that pre-dated an intervening resolution. This V9 census reports the DB-truth count (20). The ledger detail: blind 8 / curse-hex 4 / fear 4 / deflect 2 / unknown-ailment 1 / instant-kill 1 = 20. No V9 action reclassified an ailment row — all three reclass targets had empty `ctrl_ailment_gaps`.

---

## §6 Ailment-wave-c+ residue (stays blocked — iron law 3, UNCHANGED from V8 semantically)

NOT in the landed spec (20 token-touches across distinct kits):

| Sub-bucket | Kits |
|---|---|
| `blind` | 8 |
| `curse/hex` | 4 |
| `fear` | 4 |
| `deflect` | 2 |
| `instant-kill` | 1 |
| `unknown-ailment` | 1 |

`unknown-ailment` (1 in current DB — the two originally-scoped kits di-warlock-launch and di-spiritform-druid-pvp had one resolved by the recent legolas re-crawl; the other retains the `GAP-AILMENT:unknown-ailment` token). Resolution path is re-crawl, not rule.

---

## §7 Held-out list (4 dossier_owed — pool members, flagged NOT-YET-EMISSIBLE; UNCHANGED)

- `la-ferality-wildsoul` — Ferality Wildsoul — blocked_on=['mechanic:shapeshift']
- `la-liberator-valkyrie` — Liberator Valkyrie — (mechanically expressible; held by dossier gate)
- `la-phantom-beast-awakening-wildsoul` — Phantom Beast Awakening Wildsoul — blocked_on=['mechanic:shapeshift']
- `la-shining-knight-valkyrie` — Shining Knight Valkyrie — (mechanically expressible; held by dossier gate)

IN the denominator (§F.5(1) pool) but held-out per E4 T4/P-1 — E-next admission behind Matt E4 ratification. The 2 Wildsoul are additionally shapeshift-gated (GX-02); the 2 Valkyrie are mechanically expressible but held by the dossier gate. UNCHANGED from V8.

---

## §8 Iron-law asserts (PRE V8-state / POST V9-state — write is bounded to ruling-11)

| Assert | PRE (V8) | POST (V9) | Notes |
|---|---|---|---|
| total_corpus | 585 | 585 | UNCHANGED |
| total_engine_key | 585 | 585 | 1:1 UNCHANGED |
| kit_grain | 566 | 563 | −3 ruling-11 reclass |
| null_grain | 19 | 22 | +3 ruling-11 reclass |
| corpus positives (denominator base) | 523 | 520 | −3 ruling-11 reclass |
| pool = corpus positives + roster 45 | 568 | 565 | −3 ruling-11 reclass |
| combat-kit (row_class) | 566 | 563 | −3 ruling-11 reclass |
| system-record (row_class) | 19 | 22 | +3 ruling-11 reclass |
| cell_key_resolved | 562 | 562 | UNCHANGED (incl. 1 -bt sentinel) |
| bt_sentinel | 1 | 1 | UNCHANGED |
| orphans engine→corpus | 0 | 0 | UNCHANGED |
| orphans corpus→engine | 0 | 0 | UNCHANGED |
| dossier_owed | 4 | 4 | UNTOUCHED |

Cross-check assertions:
- `net_flip == wb_flipped`: 113 == 113 — OK
- `ailment_wave_c_touches == 20`: 20 == 20 — OK (corrected from V8-published 21 — see §5 corpus-hygiene note)
- `roster_expressible == 45`: 45 == 45 — OK

---

## §9 Reproducibility

- **Script:** `../scripts/corpus_s2_census_v9_2026_07_16.py`
- **Backup:** `../corpus.db.pre-v9-2026-07-16-backup` (integrity_check=ok, taken before ruling-11 write)
- **Transactional write** — ruling-11 reclassification wrapped in single transaction; PRE asserts held before writing, POST asserts held after; classifier is a pure READ on the POST-reclass state.
- **Idempotent** — re-run detects the `ruling-11-reclass-2026-07-16` flag on the 3 target rows and treats as verified no-op.
- **Wave-B flip is computed at kit grain** (V8-rule vs V9-rule blockset per kit); the multi-blocker residue is named, not elided (§2).
- **Delta decomposition** (§4) reports denominator-change effect and Wave-B flip contribution separately, per iron law 4 — the two levers are NOT conflated.

**Consumers:** governs S5 corpus→engine migration staging (`current-to-end-state-serial-content-emission.md` §F.5). Next re-run: after the next econ-wave lands (V10 delta — the UNKNOWN-audit-residue re-crawl closes, ailment-wave-c+ closure batch, or post-Wave-C small-adds).
