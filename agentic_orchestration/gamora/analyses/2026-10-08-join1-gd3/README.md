# JOIN-1 · J3a · G-D3: `JOIN[warlord, gd-decoded @ 196]`, plus the certification of rulebook `615f886e`

**gamora, 2026-10-08.** The prereg is engine `3627ab62` (`join1-j3a-gd3-instrument-prereg-2026-10-08.md`). The instrument is `3653a70c`, and the rulebook is `615f886e` (the decoded tier tally; PACK_PIN v2).

**INFO-V2-3:** the sealed referent's crit-damage constant `fixture.CRIT_DAMAGE_PCT` is **12** (the Warborn Visor alone; sealed `fixture.py:219`). It never fires, because CritLimb is LO. **The referent carries 12, not 57 or 69.**

**WARN-A2-2:** `gd-decoded` reads board-fed PTH. Against the referent footage this is a **LOWER-SIDE** reading; the in-run PTH lift is an input gap.

**CD values, JUDGED:**
- EoR 69 % = sheet 57 % + Visor 12 %;
- Soulfire 57 %.

## Certification of `615f886e` (before G-D3)

| | Result |
|---|---|
| `pj29.json` | P-J2-9 30/30 |
| `golden-master/` | 7/7 FILE-equal (sha256 per grain); 0 JOIN draws; `decoded == {}` in 26/26; intake tripwire 0. Bulk at `/Users/admin/Games/join3a-bulk-evidence/gd3-golden-master-615f886e` |
| `s47v4/` | § 4.7 v4 ORACLE BYTE-IDENTICAL |

## G-D3 (`gd3/`, `gd3.stdout.txt`; `gd3/gd3_report.json`). Bulk at `/Users/admin/Games/join3a-bulk-evidence/gd3-emission-615f886e`

**Run validity: VALID.** HEAD fixed; instrument pinned; 25 cells; 0 foreign reads; join records pass. The profile is `gd-decoded`, `pth-coupled`, span 100, CD 69 / 57 from pack v2. 7/7 vs J-S8 was FALSE, as predicted.

### ⚑ FINDING: the guard refused in 4/25 cells

- **Cells:** M0|1, M0|4, W1-NULL|1, W1-NULL|4.
- **Refusal:** `OffenseHitUndecided` on **(`records/creatures/enemies/ghost_a01_summon.dbr`, wave 153)**, raised in `run.simulate_wave`. The emitter records `terminal_reason = raised:OffenseHitUndecided` and `sim_errors = 1`.
- **Why the body has no DA:** it is an enemy summon that is not among the 196 (record, wave) pairs the Warlord **strikes** on the J-S8 path (the player-offense path P-J2-5 sourced). So it has no DA in the pack.
  - *Corrigendum to AMENDMENT-4 § 5 (engine `06d6db42`):* that text says the summon "never strikes the Warlord". The direction is wrong: the pairs are bodies **struck by** the Warlord. Whether the summon exists on J-S8 at all is **not established**; G1/G2 ids are opaque (`w151_a007`).
- **Why JOIN reaches it:** with decoded crits the Warlord's trajectory changes and he strikes it. **The guard fails closed, exactly as designed (GL-12).**
- **Consequence:** the guard's table covers the J-S8 path, not the JOIN-reachable population. **Any JOIN arm that moves the trajectory is exposed**, including all four deferred J3a controls.

### Limbs

**D-1 draws.**
- **Player:** `crit:player` draws == row-32 calls in all 21 unrefused cells. In each refused cell the count is short by exactly 1: the refused call was counted, then raised before its draw.
- **Soulfire:** `crit:soulfire` draws == row-34 calls in **25/25** cells.
- **Instrument defect.** The `sf_rows_total` anchor failed in 21 cells because `sf_rows_by_instance` was keyed by `id()`, and CPython reuses a freed object's id (M0|1: 1989 vs 2223).
  - The old form loses 597 of 605 on a scratch workload. Fixed at rulebook `ea28195a` (`crit.note_sf_rows`) and declared in AMENDMENT-4.
- **D-1 as preregistered: FALSE** (the refusals and the anchor defect). It is reported, not re-scored.

**D-2 / D-3: 350/350 PASS.**
- Max |z| = 3.85 (M0|2, `crit:player`, tier 2).
- Tiers 5 and 6 were exactly 0 everywhere.
- `decoded_base_ne_1` = 0.
- Mean multiplier per draw, cells averaged:
  - `crit:player` **1.1783** observed vs **1.1765** expected (N = 152,032);
  - `crit:soulfire` **1.1521** vs **1.1511** (N = 63,021).
- These statistics are valid up to each refused cell's stop.

**D-4 cost direction: PREDICTION FALSE.** G7 Σ `n_ticks` < J-S8 in **17/25** cells (≥ 20 predicted). On the 21 unrefused cells it is 13/21, with Σ ticks 94,540 vs 98,412 (−3.9 %).

### The Warlord's JOIN baseline vs the referent, in plain terms (21 unrefused cells)

| | J-S8 referent (crit LO; CD constant 12, never fires) | JOIN `gd-decoded @ 196` |
|---|---|---|
| Damage per player hit | ×1.0 | ×1.178 EoR / ×1.152 Soulfire (measured mean) |
| Survived the window | 16/21 | **13/21** (5 survive→die, 1 die→survive) |
| Σ ticks | 98,412 | 94,540 (−3.9 %) |

**Reading:** about 15–18 % more damage per hit buys **no measurable survival gain** on this board.
- The flip is in the other direction (5 vs 1), but that is not significant (sign test p ≈ 0.22). The JOIN crit streams re-route each cell's trajectory, and per-cell survival is chaotic at n = 21.
- **This is not a baseline of record:** 4/25 cells were refused. It becomes one once the JOIN-reachable bodies are sourced (see the HOLD in AMENDMENT-4 § 5).

**G-D4** (prereg § 5 reading, flagged): with no joined kit, X = 196, and this emission **is** the G-D4 baseline row. It inherits the same 4/25 hole.

---

## AMENDMENT (KP-380, jack-ryan WARN at collab `13cc43bd8`; append-only, 2026-10-08)

- **The survival wording is restated.** The reading above ("no measurable survival gain") becomes: **no detectable gain at low power; observed direction ADVERSE (13/21 vs 16/21; 5 survive→die vs 1 die→survive; exact sign test p = 0.219).**
- **The exclusion was NOT random.** The 4 refused cells (M0|1, M0|4, W1-NULL|1, W1-NULL|4) are **exactly the runs that reached the pet** `ghost_a01_summon@153`. The 21-cell comparison is therefore conditioned on not reaching it, and is **not** an unbiased estimate of the 25-cell baseline.
- **D-1 is re-tested as a FRESH prediction on the G-D3 re-emission** (after PACK_PIN v3), with the id-reuse-safe Soulfire anchor (`ea28195a`) and the step-2b closure test (lookups outside the sourced set, predicted 0).
- **The ghost summon's source**, established by the step-2b census (`../2026-10-08-join1-pj25-step2b/`): it is a pet of the **pre-pass** ghosts. The pre-pass is the line-up-free waves 151–156 run inside `c11a._period()`. It is not a line-up body's pet.

---

## CORRIGENDUM (KP-386 INFO-3; append-only, 2026-10-08)

**The survival flip count above is mis-stated, in both the original reading and the KP-380 amendment.** Over the 21 unrefused cells it is **4 survive→die vs 1 die→survive, exact sign p = 0.375**, not "5 vs 1, p ≈ 0.22 / 0.219". The totals (13/21 vs 16/21) were right, and so was the conclusion (no detectable effect, direction adverse). This whole first-emission reading is superseded by the re-emission of record (`../2026-10-08-join1-gd3-v3/`).
