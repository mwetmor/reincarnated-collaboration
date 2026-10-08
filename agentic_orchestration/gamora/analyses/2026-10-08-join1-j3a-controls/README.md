# JOIN-1 · J3a deferred controls + RT, at rulebook `06b9bdb3` (PACK_PIN v3; KP-384)

**gamora, 2026-10-08.**
- **Prereg:** `6e412839` § 5, AMENDMENT-1 A-3, and AMENDMENT-4 (`06d6db42`; restated count anchors; its § 5 HOLD is lifted by v3).
- **Instrument:** engine `gamora_join3a_controls_2026_10_08.py`.
- **Runs:** each as one courtesy-gated hold, in sequence. Engine HEAD was `06b9bdb3` throughout.
- **Bulk:** `/Users/admin/Games/join3a-bulk-evidence/controls-06b9bdb3-<RUN>`.

**INFO-V2-3:** the sealed referent's `fixture.CRIT_DAMAGE_PCT` is **12** (the Visor alone), not 57 or 69.

**INFO-Δ4 #12:** under `independent-proc`, G1 `crit_tier` records 0/1.

**Every run is valid:** HEAD fixed, instrument pinned, 25 cells, 0 foreign reads, join records pass, the profile as specified. Every run also has **0 `raised:*` cells** and **closure `n_outside` = 0** in 26/26 records.

| Run | Limb | Result |
|---|---|---|
| C-INTAKE-NC | **LANE-1** | **0 violations / 56,765 G1 rows.** Summon rows == the sealed `resolve_hit` law; monster rows == the no-crit law |
| | **NC-J3-L06-1** | **25/25**: the first divergence is a monster row with J-S8 ×1.1 → ×1.0; G3 `intake_hp` ≤ J-S8 at that wave; 0 JOIN draws |
| C-SUMMON-NC | **LANE-2** | **0 violations / 56,511 rows** |
| | **NC-J3-L06-2** | **25/25**: the first divergence is a summon row with ×1.1 → ×1.0; G7 `n_ticks` ≥ J-S8 at that wave; 0 JOIN draws |
| C-L06-3 | **NC-J3-L06-3** | **PASS, both lanes.** (a) draws == `lane_landed` (intake 29,467; summon 22,348) and G1 landed ≤ draws (26,695 / 20,000). (b/c) K within the A-3 bound in 25/25 per lane, max \|z\| 2.42. (d) 0 multiplier violations. The direction of `intake_hp` was not predicted |
| C-L06-4 | **NC-J3-L06-4 (a)–(d)** | **25/25 cells.** Draws == row-32 calls; Soulfire draws == `sf_rows_total`; K within bound per stream (max \|z\| 2.37); `stash_hist` ⊆ {1.0, 1.57} with ['1.57'] == procs; read-back mismatch 0 |
| | **NC-J3-L06-4 (e)** | **PREDICTION FALSE:** G7 Σ `n_ticks` < J-S8 in **15/25** cells (≥ 20 predicted). Reported, not re-scored. This is the same direction failure as G-D3 D-4 (see the G-D3 v3 README) |
| RT (`RT/`) | **NC-J3-L06-RT** | **7/7 FILE-equal** to the J-S8 fixture (sha256 per grain), after the controls, at `06b9bdb3` |
