# JOIN-1 · J4b: the 16a drain recorder on HIS flinch-off arm (prereg § 4 item 12; KP-427 WARN-1; authorised KP-476 (5)) (gamora, 2026-10-15)

- **Recorder:** engine `f4a66673` (`gamora_join4b_drain_recorder_2026_10_15.py`), with failing tests `c332b3c4` first. Run in the dedicated worktree under the courtesy gate.
- **Bulk:** `/Users/admin/Games/join3a-bulk-evidence/j4b-drain-16a-f4a66673`.
- **Gates:**
  - its own G1–G7 equal the instrument's emission (byte-identical to `4c30b0d64`) **row for row on 25 / 25 cells**;
  - the oracle's attributes are present on all 10 waves of every cell.
- **Result over the 25 cells (his arm):**
  - **SlowManaLeach 68 landings**, in every cell (1–6 per cell);
  - **Disruption 6** (M0 s0 ×2, M-POL-2-NULL s0, W1 s0, W1 s2, W1-NULL s0);
  - **PierceRatio 2** (M0 s0, M-POL-2-NULL s0).
- **The registered static pre-count predicted "SlowManaLeach-only exposure". That is FALSE AS PRE-STATED:** Disruption and PierceRatio both landed on his arm.
- **Bounds:**
  - **B_hi = 68 × 1,032 = 70,176 mana** in total, the trivial bound on his arm's exposure translated to her pool;
  - **B_eq: NO VERDICT.** The oracle records landing counts, not drain magnitudes;
  - **the Disruption lost-cast bound: NO VERDICT.** Lockout seconds are not recorded.
- **The bias on HER margin is still 0.** Her port side (16b) recorded **0** landings of any of these families on 25 / 25 cells (`non_health_by_type` empty). Her own runs met no drain.
- **Labels:** completeness POST-HOC; CORR-4 FALSE AS PRE-STATED; probe limbs by reference; Meteor-delay semantics OPEN (KP-476), no pair flips.
