# S2 — Migration-Readiness Census V8 (THE SCOREBOARD, post-Gate-2 rerun)

**Date:** 2026-07-16 · **Author:** elrond (autonomous atlas-parity run, cycle 2, CENSUS V8 charge)
**Commissioner:** gandalf-prime (Matt authorization 2026-07-16)
**Corpus state:** 585 rows / 566 kit + 19 NULL-grain / 562 cell_key resolved (incl. 1 -bt sentinel) / 4 dossier_owed held-out / 585 engine_key 1:1 (0 orphans) — **byte-stable (pure read this run)**
**Scope:** Post-ailment-LANDED (Gate-2 PASS-WITH-AMENDMENTS, engine `cec8f12` PUSHED, decisions-log 5796–5844) + post-econ:UNKNOWN-audit (5 fills applied, `93233d18`). corpus.db READ-ONLY — no backfill rider.

---

## §1 Headline

| Metric | Count | % |
|---|---|---|
| **Candidate pool (denominator)** | **568** | 100.0% |
| **Expressible-now** | **385** | **67.8%** |
| Blocked | 183 | 32.2% |
| — of which dossier_owed held-out | 4 | 0.70% |

Denominator composition: 523 corpus positives at kit grain + 45 founding roster = 568 (SAME denominator law as V7). Negatives (43 kit-grain), NULL-grain system-records (19), and grain=NULL mints EXCLUDED per spec.

Corpus expressible: **340/523 (65.0%)**  ·  Roster expressible: **45/45 (100.0%)**

Roster (45 K/H/B) is SPEC ANCHOR — the engine's first-class targets; Wave-A close covers the proxy-hosted H-cells (H1/H2/H3/H4). Expressible-now at the geometry+economy layer; ailment overlays now LAND per emission (the ailment layer is live).

---

## §2 Multi-blocker honesty — the ailment flip decomposed (iron law 2)

The ailment layer LANDED, so the 5 in-flight ailment buckets that V7 scored blocked (damage-amp/sunder · freeze · stun · poison-dot · taunt) are now expressible engine truth. But **a kit blocked on ailment AND econ:PC does NOT flip just because ailment landed.** The census unions ALL blockers per kit; a kit is expressible only when its ENTIRE blockset is empty.

| Ailment-cohort accounting | Count |
|---|---|
| Distinct kits carrying ≥1 now-landed ailment token (the **cohort**) | 191 |
| — **flipped** to expressible (ailment was the SOLE remaining blocker) | **122** |
| — **multi-blocker residue** (still blocked on a non-ailment gate) | 69 |

**The real flip is 122, not 227.** The charter's ≤227 ceiling (222 in-flight-ailment token-touches + 5 econ) is a TOKEN-TOUCH upper bound. The kit-grain flip is 122 because (a) the 191 cohort kits collectively hold 222 ailment token-touches (many kits carry >1 ailment), and (b) 69 of those kits remain gated by a non-ailment blocker. The 5 econ-audit fills are NOT part of this flip — they already landed in the DB (pre-V8) and lifted corpus from V7-published 213 to the 218 that this V8 read starts from.

**Multi-blocker residue — what the 69 ailment-cohort kits are still blocked on** (token-touches; a kit can carry >1):

| Residual blocker | Cohort kits still gated |
|---|---|
| `econ:PC` | 22 |
| `econ:RS` | 21 |
| `econ:UNKNOWN` | 7 |
| `econ:AM` | 6 |
| `econ:BT` | 4 |
| `econ:RC` | 4 |
| `ailment-wave-c+:curse/hex` | 2 |
| `geometry:orbit` | 2 |
| `ailment-wave-c+:deflect` | 2 |
| `ailment-wave-c+:blind` | 2 |
| `ailment-wave-c+:fear` | 1 |
| `mechanic:shapeshift` | 1 |
| `econ:DR` | 1 |
| `geometry:walls-placed-lane` | 1 |
| `econ:LC` | 1 |

Reading: of the 69 residue kits, the dominant re-block is the **econ reservation/persistent-cost family** (`econ:PC` + `econ:RS` lead) — i.e. the ailment flip HANDS OFF directly to Wave-B as the next lever. A handful are re-blocked on wave-c+ ailments, small-add geometry, or shapeshift.

---

## §3 Blocked-on-what — ranked buckets (V8, all corpus-side)

| Bucket category | Kits touched | Sub-buckets |
|---|---|---|
| **wave-B:persistent-cost** | 44 | econ:PC=44 |
| **wave-B:reserved-slot** | 42 | econ:RS=42 |
| **unclassified-economy** | 33 | econ:UNKNOWN=33 |
| **ailment-wave-c+** | 21 | ailment-wave-c+:blind=8; ailment-wave-c+:curse/hex=4; ailment-wave-c+:fear=4; ailment-wave-c+:deflect=2; ailment-wave-c+:unknown-ailment=2; ailment-wave-c+:instant-kill=1 |
| **wave-B:attunement-meter** | 16 | econ:AM=16 |
| **wave-B:recharge** | 16 | econ:RC=16 |
| **small-add:block-trigger-BT** | 8 | econ:BT=8 |
| **small-add:orbit-25th-geo** | 6 | geometry:orbit=6 |
| **wave-B/C:life-cost-drain** | 5 | econ:LC=3; econ:DR=2 |
| **shapeshift (GX-02 docket bg)** | 3 | mechanic:shapeshift=3 |
| **small-add:walls-placed-lane** | 3 | geometry:walls-placed-lane=3 |

**Reading the buckets (post-ailment-landed):**

- The 5 in-flight ailment buckets (damage-amp/sunder · freeze · stun · poison-dot · taunt) are GONE from the blocked ledger — they landed (`cec8f12`).
- `ailment-wave-c+` = 21 token-touches (blind 8 / curse-hex 4 / fear 4 / deflect 2 / unknown-ailment 2 / instant-kill 1) — NOT in the landed spec; stays blocked (iron law 3). legolas re-crawl (in flight, read-only) is probing the 2 `unknown-ailment` kits (di-warlock-launch, di-spiritform-druid-pvp).
- `wave-B:*` (persistent-cost + reserved-slot + attunement-meter + recharge) is now the TOP blocked family — **Wave-B spec is at Gate-1 now; this ranking is live input to Wave-B sequencing.**
- `unclassified-economy` (`econ:UNKNOWN`) dropped 38 → 33 (elrond econ-audit `93233d18`; 18 residual kits carry `econ-audit-ambiguous-2026-07-16` for a future re-crawl; 15 more queued as spec-amendment rule sketches).
- `small-add:*` = orbit-25th-geo (6), walls-placed-lane (3), block-trigger-BT (8) — post-Wave-C small adds.
- `shapeshift` = GX-02 keystone (gd-berserker-wereforms + 2 in-pool Wildsoul); +2 held-out Wildsoul in §6.

---

## §3b Bucket detail (top individual buckets)

| # | Bucket | Count |
|---|---|---|
| 1 | `econ:PC` | 44 |
| 2 | `econ:RS` | 42 |
| 3 | `econ:UNKNOWN` | 33 |
| 4 | `econ:AM` | 16 |
| 5 | `econ:RC` | 16 |
| 6 | `ailment-wave-c+:blind` | 8 |
| 7 | `econ:BT` | 8 |
| 8 | `geometry:orbit` | 6 |
| 9 | `ailment-wave-c+:curse/hex` | 4 |
| 10 | `ailment-wave-c+:fear` | 4 |
| 11 | `econ:LC` | 3 |
| 12 | `geometry:walls-placed-lane` | 3 |
| 13 | `mechanic:shapeshift` | 3 |
| 14 | `ailment-wave-c+:deflect` | 2 |
| 15 | `ailment-wave-c+:unknown-ailment` | 2 |
| 16 | `econ:DR` | 2 |
| 17 | `ailment-wave-c+:instant-kill` | 1 |

---

## §4 Delta vs V7 (published baseline: 258/568 = 45.4%)

| Scoreboard | Pool expressible | % | Corpus | Roster |
|---|---|---|---|---|
| V7 (published, pre-econ-audit) | 258/568 | 45.4% | 213/523 | 45/45 |
| **V8 (this run, post-Gate-2 + econ-audit)** | **385/568** | **67.8%** | **340/523** | 45/45 |
| **Δ** | **+127** | **+22.4pp** | +127 | 0 |

**Headline movement: 45.4% → 67.8% (+22.4pp).** The +127 pool-expressible decomposes cleanly:
- **+5 econ-audit fills** (V7-published 258 → 263): 2 native/spend (chr-bleed-berserker, chr-high-ranger-warden) + 3 SU/Wave-A-landed (poe1-baron-zombies, poe1-siege-ballista, gd-pet-conjurer). Already in DB pre-V8.
- **+122 ailment flip** (263 → 385): distinct kits whose sole remaining blocker was an in-flight ailment, now landed. 69 ailment-cohort kits did NOT flip (multi-blocked — §2).

**Per-bucket flips (V7 blocked → V8):**

| Bucket | V7 | V8 | Δ |
|---|---|---|---|
| `ailment-in-flight:damage-amp` | 97 | 0 (LANDED) | −97 |
| `ailment-in-flight:freeze` | 42 | 0 (LANDED) | −42 |
| `ailment-in-flight:poison-dot` | 36 | 0 (LANDED) | −36 |
| `ailment-in-flight:stun` | 36 | 0 (LANDED) | −36 |
| `ailment-in-flight:taunt` | 11 | 0 (LANDED) | −11 |
| `econ:UNKNOWN` | 38 | 33 | −5 (econ-audit) |
| `econ:SU` (Wave-A, expressible) | 6 | 9 | +3 (econ-audit reclass) |
| `econ:PC` / `RS` / `AM` / `RC` / `LC` / `DR` / `BT` | frozen | frozen | 0 |

**New blocked-bucket ranking (top 5 — feeds Wave-B sequencing, live at Gate-1):**

| Rank | Bucket | Kits |
|---|---|---|
| 1 | `econ:PC` | 44 |
| 2 | `econ:RS` | 42 |
| 3 | `econ:UNKNOWN` | 33 |
| 4 | `econ:AM` | 16 |
| 5 | `econ:RC` | 16 |

With the ailment cohort cleared, **the reservation/persistent-cost economy family (`econ:PC` 44 + `econ:RS` 42) is now the single biggest expressible-now lever**, followed by the audit residue (`econ:UNKNOWN` 33), then `econ:RC` 16 / `econ:AM` 16. Wave-B's exhibits map directly onto this ranking.

---

## §5 Ailment-wave-c+ residue (stays blocked — iron law 3)

NOT in the landed spec (21 token-touches across distinct kits):

| Sub-bucket | Kits |
|---|---|
| `blind` | 8 |
| `curse/hex` | 4 |
| `fear` | 4 |
| `deflect` | 2 |
| `unknown-ailment` | 2 |
| `instant-kill` | 1 |

`unknown-ailment` (2: di-warlock-launch, di-spiritform-druid-pvp) is under active legolas re-crawl (in flight, read-only — no contention with this census). Resolution path is a re-crawl, not a rule.

---

## §6 Held-out list (4 dossier_owed — pool members, flagged NOT-YET-EMISSIBLE; UNCHANGED)

- `la-ferality-wildsoul` — Ferality Wildsoul — blocked_on=['mechanic:shapeshift']
- `la-liberator-valkyrie` — Liberator Valkyrie — (mechanically expressible; held by dossier gate)
- `la-phantom-beast-awakening-wildsoul` — Phantom Beast Awakening Wildsoul — blocked_on=['mechanic:shapeshift']
- `la-shining-knight-valkyrie` — Shining Knight Valkyrie — (mechanically expressible; held by dossier gate)

IN the denominator (§F.5(1) pool) but held-out per E4 T4/P-1 — E-next admission behind Matt E4 ratification. The 2 Wildsoul are additionally shapeshift-gated (GX-02); the 2 Valkyrie are mechanically expressible but held by the dossier gate. UNCHANGED from V7.

---

## §7 Iron-law asserts (held PRE + POST — DB byte-stable)

| Assert | Expected | Notes |
|---|---|---|
| total_corpus | 585 | pure READ; no writes |
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

- **Script:** `../scripts/corpus_s2_census_v8_2026_07_16.py`
- **Backup:** `../corpus.db.pre-s2-census-v8-2026-07-16-backup` (integrity_check=ok)
- **Pure census** — corpus.db READ-ONLY (no backfill, no schema-meta INSERT, no column writes). Only output is this artifact + the MIGRATION.md entry. DB byte-stable PRE→POST.
- **Idempotent** — re-run yields identical artifact + identical asserts.
- **Ailment flip is computed at kit grain** (V7-rule vs V8-rule blockset per kit); the multi-blocker residue is named, not elided.

**Consumers:** governs S5 corpus→engine migration staging (`current-to-end-state-serial-content-emission.md` §F.5). **Wave-B spec (at Gate-1 now) takes its exhibit sequencing from the §4 top-5 ranking.** Next re-run: after Wave-B lands (V9 delta — the PC/RS/AM/RC family flips).
