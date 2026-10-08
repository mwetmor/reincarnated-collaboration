# JOIN-1 · J3d CLOSE-OUT: engine forms + grids for the port-emitted levers L-02 / L-03 / L-07 / L-08

**gamora, 2026-10-08.**
- **Prereg:** engine `dfdb6a9f`; AMENDMENT-1 (jack-ryan WARN-1: each packet is the sealed `damage_against` expression); AMENDMENT-2 (legolas's D2 Crushing Blow decode, collab `fb0585972`: ADJ-J4 SOURCED, plus a third L-08 mode).
- **Fail-first:** `tests/test_join3d_forms.py` (7 tests).
- **Rulebook:** **`a8e11af60422745c9512d89f2ec32d833de11911`**.
- **Grid generator:** `scripts/gamora_join3d_grids_2026_10_08.py` (`43954d1a`).

**Label for every J4 fidelity row of these levers: `PORT-EMITTED · ENGINE-GRID (arithmetic only)`** (jack-ryan INFO-2). The engine proves arithmetic parity, not integration. A row-level replay of the port's per-packet records through these forms is drax's option at J3c.

## Certification of `a8e11af6` (defaults; the forms are installed on NO A-2 row)

| | Result |
|---|---|
| `pj29.json` | P-J2-9 30/30 |
| GM (bulk `j3d-golden-master-a8e11af6`) | 7/7 FILE-equal (sha256 per grain); 0 JOIN draws; `n_outside`, `acc_bound` and `charge_bound` empty in 26/26 |
| `s47v4/` | § 4.7 v4 ORACLE BYTE-IDENTICAL |
| `info3_rulebook_diff_d5384b4b_a8e11af6.patch` | **purely additive** (0 deleted lines): the new pure forms in `forms.py`, plus `PortOnlyLever` / `L08Unset` and the profile refusal in `levers.py` |

## Grids (`grids.json`; inputs and outputs with f64 bit-hex, for the port to equal bit for bit)

| Prediction | Result |
|---|---|
| **G-L02-1** n = 1 ≡ `min(PlayerOffense.damage_against(record, mult, res_bonus), hp)` on real board rows, k ∈ {None, 1, 0.93, 1.07}, banner ∈ {1, 1.15}, aura ∈ {0, 12} | **3,168 / 3,168 bit-exact** |
| G-L02-2: no-death total == left-to-right sum of per-packet values | PASS |
| G-L02-3: res + bonus ≥ 100 applies 0.0 (k included) | PASS |
| G-L02-4: death on packet k < n gives Σ applied == hp_start exactly; after-death packets 0.0 | PASS (every death row) |
| G-L02-5: the piecewise armour law (2 × raw/2 vs 1 × raw, straddling armour) | 40 / 40 rows apply less with 2 packets, as predicted |
| G-L02-6: per-packet sustain proration frac == applied / a | PASS |
| G-L03: hp_after_max_change (both policies, clamp, h = 0, 5 named domain refusals) | PASS |
| G-L07/08: proportional_raw (+ floor); L-08 yes / no / pct-resist-only; killability; L08Unset | PASS |
| G-ADJ-J4 (SOURCED) | CB first on pre-hit HP: prop 100, hp 700; leech no 200 / yes 300; **the cap case gives leech 125 (CB lowers the cap)**; the `after` alternate gives 80 / 720. PASS |

**Declared fixes, made before the generator's commit:**
- the first grid domain lacked a straddle row (G-L02-5 read 0 rows), so raw 160 was added;
- the G-L02-4 check was tightened to the preregistered exact-sum form.

## Status of the open items
- **L-08 `pct-resist-only`** (the third mode) needs **jack-ryan's decisions-log entry**. The ratification `77d45b23` covers yes/no.
- **legolas's per-kit CB facts** (tier fractions, ranged ×2, player count, no crit doubling) are carried to J4 (notes N-5).
- **The design's port controls** are restated as paired totals + sign test (prereg § 4). NC-J3-L07-1 states `l08 = yes`.

## The new J3c pin
**`a8e11af60422745c9512d89f2ec32d833de11911`** supersedes `d5384b4b`. It is `d5384b4b` + the J3d pure forms (additive; defaults unchanged).
- MIGRATION amendment engine **`247b879a`** carries the row-36 port site (no consented site yet: an in-form hook or a Matt ruling) and the KP-360 / J3c scope cross-reference. **It discharges jack-ryan's J3b close-out WARN-1 (`bb6a86230`), for his confirmation.**
