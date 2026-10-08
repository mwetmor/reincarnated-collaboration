# JOIN-1 · J3a · G-D3 RE-EMISSION, the row of record: `JOIN[warlord, gd-decoded @ 196]` at rulebook `06b9bdb3` (PACK_PIN v3)

**gamora, 2026-10-08.**
- **Prereg:** engine `3627ab62` §§ 1–5, plus § 6, appended and committed before this run.
- **Instrument:** `gamora_join3a_gd3_2026_10_08.py`.
- **Run:** one courtesy-gated hold.
- **Analysis:** `gd3/gd3_report.json`. Bulk at `/Users/admin/Games/join3a-bulk-evidence/gd3-v3-emission-06b9bdb3`.

**Labels carried:**
- **INFO-V2-3:** the sealed referent's `fixture.CRIT_DAMAGE_PCT` is **12** (the Warborn Visor alone). It never fires (CritLimb LO). The referent carries 12, not 57 or 69.
- **WARN-A2-2:** `gd-decoded` reads board-fed PTH, so this is a **LOWER-SIDE** reading against the referent footage.
- **JUDGED:** crit damage is EoR 69 % (sheet 57 + Visor 12) and Soulfire 57 %. The roll rule itself is DECODED (D-L5, legolas).

## Gate results

| Limb | Prediction | Result |
|---|---|---|
| Run validity | HEAD fixed, pinned, 25 cells, 0 foreign reads, join records pass | **VALID**; profile `gd-decoded` / `pth-coupled` / span 100 / CD 69·57 |
| **PERIOD tripwire (INFO-4)** | G7 `tick_period_s` JOIN == J-S8, bit-for-bit | **250/250 equal → no HALT** (code reading: the period is frozen from AS at `run.py` :1215/:1233) |
| **CLOSURE (INFO-3)** | `n_outside` == 0 per cell; 0 refusals | **0 in 25/25; 0 `raised:*`; 25/25 cells reach a sim terminal** |
| Coverage | reported | lookups: damage_against 158,047 · soulfire_applied 206,501 · bleed 282,078. Decoded pairs 196 distinct, all in the 248-pair pack |
| **D-1 (FRESH)** | draws == row-32 calls; Soulfire draws == row-34 == `sf_rows_total`; Σ body n == draws | **25/25** |
| D-2 / D-3 | 350 tests at 4σ / exact | **350/350**, max \|z\| 3.85 |
| D-4 cost direction | G7 Σ `n_ticks` < J-S8 in ≥ 20/25 | **FALSE: 15/25.** Reported, not re-scored (C-L06-4 (e) fails the same way) |
| 7/7 vs J-S8 | predicted FALSE | FALSE |

**Determinism check.** The 21 cells that were never refused in the first emission reproduce it **identically** (terminal, ticks, intake). The re-emission differs only in the 4 formerly refused cells, which now run to completion: **all 4 survive the window**.

## The Warlord's JOIN baseline vs the referent, in plain terms (all 25 cells; for Matt's J3→J4 checkpoint)

| | Referent J-S8 (crit LO; CD constant 12, never fires) | JOIN `gd-decoded @ 196` |
|---|---|---|
| Damage multiplier per player hit | ×1.000 | **×1.178 EoR** (expected 1.176) · **×1.152 Soulfire** (expected 1.151); measured over 158,047 / 65,462 hits |
| Survived the 151–160 window | **20/25** | **17/25** (4 survive→die, 1 die→survive; **exact sign test p = 0.375**) |
| Σ world ticks | 117,695 | 113,051 (**−3.9 %**; fewer in 15/25 cells) |
| Σ intake HP | 22.28 M | 21.13 M (**−5.2 %**) |

**Reading:**
- **Damage:** the Warlord deals **about 15–18 % more damage per hit**, exactly as the decoded rule predicts.
- **Waves:** they end a little sooner (−3.9 % ticks), and he takes a little less damage in total (−5.2 % intake).
- **Survival: no detectable effect.** The observed direction is **adverse** (17 vs 20 survive), but p = 0.375 at n = 25. Survival per cell is chaotic: the crit streams re-route each cell's trajectory.
- **The earlier 21-cell reading is superseded.** It was biased: its 4 excluded cells were exactly the ones that reached the pet, and all 4 survive here. This 25-cell row is the baseline of record.

**G-D4 (prereg § 5 reading, flagged at Gate):** with no joined kit, X = 196, and this emission **is** the G-D4 baseline row.
