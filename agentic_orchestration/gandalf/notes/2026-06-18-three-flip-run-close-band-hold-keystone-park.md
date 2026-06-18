# gandalf run-close ruling — THREE-FLIP RATIFICATION (Tier-2a band-refit + Tier-2b keystone-ceiling)

**STATUS:** RULED — both reserved Tier-2 calls resolved at run-close. (a) Bands HOLD as-fit (no refit). (b) Keystone-ceiling stays a SEPARATE PARKED ticket; #3's ratification does NOT absorb it.
**Date:** 2026-06-18
**Author:** gandalf (story-and-design steward)
**Closes:** the two Tier-2 items reserved in `agentic_orchestration/gandalf/requests/2026-06-17-kr-flag-flip-run-prompt.md` §40-42, routed back by KR at run-close with gamora's #3 re-measure data.
**Run state on return:** all three flags flipped LIVE (separate commits, smoke-clean); jack-ryan wrote three decisions-log semantic-shift declarations (`f32e48a`) + gate-confirmed each smoke-clean (no BLOCK). Push is Tier-3, held (Matt-gated).

**Companions:**
- `agentic_orchestration/gandalf/notes/2026-06-17-mob-hp-anchor-design-read.md` — the locked MOB_HP 1.5x anchor; §4.1 is the keystone-ceiling parking origin.
- `reincarnated-engine/output/kpm-band-spatial-recal-full-20260616_232152.json` — n=3078 band-fit basis.
- `reincarnated-engine/output/kpm-band-spatial-recal-full-20260618_002503.json` — #3 faithful-loadout re-measure (n=3078).
- `reincarnated-engine/src/reincarnated/simulation/gauntlet_sim.py` ~L308-322 — the mobs/min bands (held as-fit) + L1994-1997 (`_patch_kits_profile` harness seam).
- `reincarnated-engine/src/reincarnated/simulation/unified_calibration_loop.py` L2396-2400 — `_patch_kits_profile(profile="max")` ≡ `_patch_kits_option_a()` by construction property.

---

## 1. Tier-2a — BAND-REFIT CALL: **HOLD as-fit. No refit.**

**One-line rationale:** #3's faithful re-measure is byte-identical to the n=3078 band-fit basis (|Δ|=0.00 all six shells + pooled 8.523), because the bands were ALREADY fit on a max-profile / faithful-loadout regime — #3 only aligns the production *runtime* default to the regime the fit already assumed, so the measurement regime did not change. No regime drift → no refit trigger fires.

**The reserved trigger and why it does not fire.** My run-prompt §41 reserved the band-refit call for a *different* trigger than the MOB_HP one: not "MOB_HP changed" (that trigger is dead — MOB_HP locked at 1.5x, §3 of the anchor note), but "#3 changes the measurement regime (faithful vs stripped → faster clears → higher mobs/min)." That hypothesis was sound on its face — IF the bands had been fit on stripped loadouts, flipping the runtime to faithful would lift mobs/min and drift the bands. The data falsifies the antecedent: the bands were never fit on stripped loadouts.

**Mechanism — verified against disk, not taken on report (Discipline: empirical inspection over assumption).**
1. The band-fit harness applies investment profiles via `_patch_kits_profile(kits, profile=invest_profile)` (`gauntlet_sim.py:1994-1997`), iterating `INVEST_PROFILES` including `"max"`.
2. `_patch_kits_profile(..., profile="max")` is documented as "equivalent to `_patch_kits_option_a()` (construction property)" (`unified_calibration_loop.py:2396-2400`) — i.e. the calibration-seam equivalent of `apply_max_profile_investment=True`. gamora's characterization holds.
3. The #3 re-measure JSON self-describes its slice as `"54-kit representative-loadout base population @ max-profile (determined identity loadout)"` (`...002503.json` L7) — the SAME max-profile determined-identity slice the n=3078 fit ran on.
4. Empirical confirmation, not inference: per-shell + pooled |Δ| = 0.000 (open 13.023, choke 13.826, magic 8.984, elite 6.451, boss 2.501, mini 1.651, pooled 8.523 — identical both runs). Byte-identical is the fingerprint of the regimes being the same regime, not merely close.

**This is the clean-close branch my run-prompt pre-stated.** §41 verbatim: "If it doesn't [materially drift], bands hold and the run closes clean." The data votes NO-drift. Bands hold. No `gauntlet_sim.py` L308-322 edit. gamora correctly left the bands UNCHANGED (did not self-refit — that was my call to make, and the call is HOLD).

**Provenance-tag note (housekeeping, not a refit).** The bands at L308-311 carry a "RE-FIT CANDIDATE if MOB_HP_DIFFICULTY_MULTIPLIER changes" tag. MOB_HP did NOT change (locked 1.5x), so that tag's condition never fired either. Both refit triggers — the MOB_HP one and the #3-regime one — are now resolved NEGATIVE. The tag can stay as-is (still a true conditional for any *future* MOB_HP move); no edit required by this ruling.

## 2. Tier-2b — KEYSTONE-CEILING WATCH: **stays a SEPARATE PARKED ticket. #3's ratification does NOT absorb it.**

**One-line rationale:** the escalation condition I reserved (the 1.000 zero-variance ceiling CHANGING the kit-power read vs merely CONFIRMING the 8.19× multiplier) is technically NOT met — gamora + jack-ryan both independently found the 8.19× multiplier CONFIRMED on the kpm *throughput* metric (which is not ceilinged), so the open_arena 1.000 WR ceiling confirms, not changes, the read. But the ceiling DOES exist, and I explicitly did not want #3 to silently absorb it — so I am recording it parked, intact, not dissolved.

**Why it doesn't change #3's ratification.** The kit-power multiplier (8.19× mean-of-ratios; 6.749× ratio-of-means) is measured on kpm throughput, NOT on win-rate. Win-rate is what saturates at the 1.000 zero-loss-variance ceiling (`spearman_degenerate=true`, `max_rank_shift=23` on the saturated open_arena faithful reference). Throughput is not ceilinged — a kit that wins 1.000 can still clear faster or slower, and that spread is what the multiplier reads. So the ceiling and the multiplier live on different metrics; the ceiling cannot corrupt a multiplier it does not touch. #3 ratifies cleanly.

**Why it nonetheless stays a live ticket.** A 1.000 WR with zero loss-variance is a *ceiling artifact*, not a measurement — it tells you the keystone is at-or-past the saturation point for open_arena, which is exactly the substrate of the genuinely-open "is the keystone over-tuned" question. That question is NOT a MOB_HP-anchor question and NOT a band question; it is its own balance ticket. The MOB_HP anchor note already separated it out (§4.1: "1.000 WR across all 6 geared kits with zero loss variance is a ceiling, not a measurement. The genuinely open question is 'is the keystone over-tuned.' Separate ticket"). This run-close confirms that separation rather than collapsing it.

**PARKING POINTER (so it is not lost):** the keystone-over-tuned question lives at `agentic_orchestration/gandalf/notes/2026-06-17-mob-hp-anchor-design-read.md` §4.1, now cross-confirmed by this run-close (§2 here). It is parked, not closed. Re-engagement criterion (EMPIRICAL, not time-passage): a non-saturated open_arena reference — i.e. when open_arena WR is pulled off the 1.000 ceiling (harder scenario, stripped reference, or a keystone-strength sweep) such that loss-variance becomes non-zero and `spearman_degenerate` goes false. Until a non-degenerate reference exists, the over-tuned question cannot be measured (you cannot rank what does not vary), so there is nothing to act on — the park is correct, not deferral-avoidance.

## 3. Push-gate / Matt-flag content

Nothing in either Tier-2 ruling changes a LOCKED reference (the MOB_HP 1.5x anchor and the band fit both HOLD), so nothing here re-opens a Matt-gated locked decision. The run closes clean on the design side. Two items ride the run-close PUSH GATE for Matt (push is Tier-3, held — KR is NOT pushing without Matt go):
- **(carry, not new decision)** Bands HELD as-fit; no `gauntlet_sim.py` change attributable to this ruling. The push gate's stack is unchanged by Tier-2a.
- **(visibility, not a gate)** The keystone-over-tuned ticket stays parked with an empirical re-engagement criterion (non-degenerate open_arena reference). Flag to Matt as a standing balance ticket, not an action item — there is no measurement to act on until the reference de-saturates. No push consequence.

## 4. Sign-off

Both reserved Tier-2 calls resolved. (a) HOLD — bands as-fit, verified byte-identical regime, run closes clean exactly as the run-prompt pre-stated. (b) PARKED — keystone-ceiling confirmed separate, pointer preserved at MOB_HP note §4.1 + here, empirical re-engagement criterion named. Discipline held: recognition → validate against substrate data (read the #3 JSON slice descriptor + the `_patch_kits_profile` harness seam on disk, not the prose) → rule. No sleep framing, no time-of-day framing — re-engagement gated on the non-degenerate-reference EMPIRICAL criterion, not on time passage.

**Signed:** gandalf, 2026-06-18.
