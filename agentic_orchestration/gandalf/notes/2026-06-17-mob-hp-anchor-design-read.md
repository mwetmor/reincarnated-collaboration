# gandalf design read — MOB_HP calibration-anchor reconciliation (autonomous-run parking-lot item #4)

**STATUS:** LOCKED — Matt ruled **anchor MOB_HP at 1.5x** (2026-06-17), accepting this design read. The 0.367 ablation-floor reframe stands as the rationale of record. Decisions-log entry to follow via KR-draft / jack-ryan-review (per gandalf-recommends / Matt-approves / KR-drafts / jack-ryan-reviews routing). No code change required — 1.5x is already the live `MOB_HP_DIFFICULTY_MULTIPLIER`; the lock confirms the status quo and the mobs/min band ruling holds as-fit (no refit).
**Date:** 2026-06-17
**Author:** gandalf (story-and-design steward)
**Resolves the design half of:** `agentic_orchestration/autonomous-run-2026-06-17-RETURN-PACKAGE.md` § parking-lot item #4 ("A4 MOB_HP baseline reconciliation — which MOB_HP is the 'true' balance reference"). A4 was PRODUCE-only per the autonomous charter; the reconciliation parked for a design read. This is that read.
**Method discipline:** ruled against DISK — computed the figure the return package quotes from the produced baseline (`reincarnated-engine/output/keystone-archive-remeasure-full.json`), not from the prose summary. The framing changed once the real distribution was read.
**Companions:**
- `reincarnated-engine/output/keystone-archive-remeasure-full.json` — the produced A4 baseline (`mob_hp_baseline` 6-kit melee ablation + the 34-kit `arms` keystone-ablation).
- `reincarnated-engine/src/reincarnated/simulation/gauntlet_sim.py` (mobs/min band logic, ~L290-330) — my prior gandalf band ruling, tagged "RE-FIT CANDIDATE if MOB_HP_DIFFICULTY_MULTIPLIER changes."
- `reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md` (session-13 caster finding) — the coverage-bound falsification that the anchor decision must NOT absorb.

---

## 0. The read in one line

**Anchor at MOB_HP 1.5x. It is not a defect — it is the difficulty calibration that makes itemization load-bearing.** The alarming "win-rate 0.367" is the keystone-STRIPPED melee ablation floor (the *measure of how much the keystone is worth*), NOT a win-rate any geared player experiences. Geared players sit at **1.000 at both 1.5x and 1.0x.** Dropping to 1.0x would neuter the gear loop to fix a number nobody plays.

## 1. What the 0.367→0.867 figure actually is (the charter framing is a trap)

The return package quotes "MOB_HP 1.5→1.0 lifts win-rate 0.367→0.867." Computed from the produced baseline, that figure is the mean of the **6-kit `mob_hp_baseline` ablation**, and it is specifically the **keystone-STRIPPED, MELEE-ONLY** arm:

| Arm | Mean WR | Mean clear time |
|---|---|---|
| **stripped** @ 1.5x | **0.367** | 116s |
| **stripped** @ 1.0x | **0.867** | 88s |
| **keystone** @ 1.5x | **1.000** | 32s |
| **keystone** @ 1.0x | **1.000** | 20s |

Three things the headline hides:

1. **It's the keystone-STRIPPED arm, not the player.** The geared player sits at **1.000 at *both* 1.5x and 1.0x.** Nobody who has their keystone gear experiences 0.367. That number is the deliberate ablation floor — it exists to quantify the keystone's value, not to describe anyone's win-rate.
2. **It's melee-only.** All 6 kits are `bc_melee`. The full 34-kit `arms` roster (melee/mid/ranged — **no casters in it at all**) shows the same shape, lower: stripped mean 0.163, geared 1.000 across the board. This baseline is *silent* on casters by construction.
3. **The keystone, not MOB_HP, is the dominant lever.** At 1.5x the keystone buys +0.633 WR (0.367→1.000). MOB_HP 1.5→1.0 buys the stripped floor only +0.5. Gear is the bigger knob; MOB_HP is the secondary knob that makes the gear's value *visible*.

## 2. The reframe — 1.5x is the itemization lever, not a defect

Read as a designer, the table is the **Diablo difficulty-vs-itemization tension**, textbook:

- At **1.5x**, the keystone is *load-bearing* — strip it and melee floors to 0.367; equip it and you're at 1.000. **That gap IS the reason gear exists** — the headroom that makes a drop feel like power.
- At **1.0x**, the stripped build already wins **0.867** and clears in 88s. Gear becomes cosmetic — its payoff shrinks to "win ~5s faster" (keystone clear 20s vs stripped 88s, but stripped already *wins*). This is D3-vanilla-Inferno-nerf territory: lower the floor and loot stops mattering.

The autonomous-run charter calls MOB_HP 1.5x "the second defect." That is exactly backwards. **1.5x is the calibration that makes itemization meaningful.** Setting it to 1.0x to make 0.367 "look healthy" would neuter the gear loop to fix a number no player sees. The convenient branch (set 1.0, aggregate looks fine) is the wrong branch.

## 3. Recommendation

**Anchor at MOB_HP 1.5x. Do NOT flip to 1.0x.** The 0.367 is a healthy ablation floor, not a broken win-rate.

**Clean downstream consequence:** my prior mobs/min band ruling (`gauntlet_sim.py` ~L290-330) was tagged "RE-FIT CANDIDATE if MOB_HP_DIFFICULTY_MULTIPLIER changes." **Keeping 1.5x means the bands hold as-fit — no band rework.** Flipping to 1.0x would force a band refit AND neuter the gear loop; the do-nothing-correct answer avoids both.

## 4. Two things this read explicitly does NOT resolve (do not let the anchor decision absorb them)

1. **Keystone ceiling artifact.** 1.000 WR across all 6 geared kits with zero loss variance is a *ceiling*, not a measurement. The genuinely open question is "is the keystone over-tuned," NOT "is MOB_HP wrong." Separate ticket; not a MOB_HP-anchor question.
2. **Caster coverage-bound failure.** The AGENT_STATE session-13 finding (a 3.3× HP reduction moved fire_mage swarm WR by ~0.02 — 0.467→0.483) lives in the swarm/open-arena GROUP-clear scenario, where casters fail on a spatial/coverage/timeout limit *independent of mob HP*. This A4 baseline cannot see it (no casters in the roster). Anyone reading 0.367→0.867 as "the caster lever" is wrong twice over — wrong cohort (stripped-melee, not caster), wrong arm (ablation floor, not player WR). The caster fix is a scenario-design call, not a MOB_HP-anchor call.

## 5. Sign-off

**LOCKED by Matt 2026-06-17: anchor MOB_HP at 1.5x.** The empirical criterion that gated this read was the produced MOB_HP baseline (already on disk) — read directly, which is what flipped the framing from "1.5 is broken" to "1.5 is the itemization lever." Recognition → validate (read the real distribution) → Matt-commit. No code change (1.5x is already live); the band ruling holds as-fit.

**Coherence note (composes with parking-lot flag #3):** locking 1.5x and flipping the keystone-faithful measurement flag (`apply_max_profile_investment` ON, parking item #3) are mutually reinforcing — at 1.5x the keystone is load-bearing (stripped floors to 0.367; faithful loadout hits 1.000), so measuring kit power on faithful loadouts is the *representative* measurement at the locked anchor. The two decisions point the same direction.

**Signed:** gandalf, 2026-06-17. Locked by Matt same date.
