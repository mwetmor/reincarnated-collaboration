# Gate-3 bridge balance check — fission bridge army power is IN-BAND (gamora)

**Author:** gamora, 2026-06-13
**For:** gandalf Gate 3 (bridge math) — the conditional gate that fires when a bridge-bearing
summoner is present in the corpus. Season 001010 corpus: PROXY_FISSION ×16 present (gamora_kernel-owned).
**Anchor:** `agentic_orchestration/gandalf/notes/2026-06-12-q6-q7-convergence-matrix-dual-proxy-pools.md`
§ 4.3 (Golem aggregative bridge cap) + § 4.3-bis (Baby Good Mimic replicative bridge, scaler-exclusion).
**Kernel evidence:** `src/reincarnated/simulation/proxy_combatant.py` (FissionLineage, spawn_fission_subproxy),
`fight_engine.py:1215-1222` (cap-enforced fission spawn).

## Question

Does the fission bridge army power stay in-band (no PoE-3.8→3.15 multiplicative spiral; scaler-exclusion
holds), given a fission-bearing summoner (PROXY_FISSION ×16) in the existing corpus?

## Verdict: IN-BAND. No multiplicative spiral is structurally possible in the current kernel.

Four independent structural guards, each empirically verified against the live kernel:

1. **Cap-bounded.** `FissionLineage.recursion_cap = 4` bounds TOTAL fission entities ever spawned in a
   lineage (not depth). Empirically: simulating repeated death-split cascades (root dies → 2 subs; each
   sub dies → tries 2 more; …) the total spawned saturates at exactly 4 and never exceeds the cap.
   `fight_engine.py:1218` gates every spawn on `lineage.can_spawn(n)`.

2. **Stat-decayed (geometric DECAY, not growth).** Each fission generation is `fission_stat_fraction=0.60`
   of its parent's HP and damage_multiplier. Army damage = root(1.0) + subs(0.60, 0.60, 0.36, 0.36) =
   **2.92× owner base** — finite and small.
   **LOAD-BEARING FINDING:** `n × frac = 2 × 0.60 = 1.2 > 1`. The fission geometric series would DIVERGE
   if uncapped (each generation adds MORE total than it removes). **The recursion_cap=4 is therefore
   load-bearing, not cosmetic** — it is the structural guard that converts a divergent series into a
   bounded 2.92× army. This is the gamora-seam analogue of the § 4.3 Golem cap discipline.

3. **Additive, not multiplicative (scaler-exclusion holds by absence).** Fission subs are stat-fractioned
   COPIES that contribute to army DPS ADDITIVELY (sum of decayed copies). They carry NO aggregative
   per-proxy count-bonus — the Golem bridge-bonus (§ 4.3) and the Mimic replicative bridge (§ 4.3-bis)
   are both DRAFT and NOT yet in the kernel. The PoE-3.8 spiral requires a count-scaling multiplier that
   feeds itself (Mimic-copies-Golem → +1 army count → Golem per-proxy bonus rises → spiral). **The current
   kernel has no such self-feeding count-scaler, so the spiral is not merely tuned-out — it is structurally
   impossible.** Scaler-exclusion is satisfied trivially because no scaler exists yet.

4. **Transient.** Fission subs expire at `fission_expiry_s = 30.0s`, so even the bounded 2.92× army is
   temporary, not a permanent power floor.

## Implication for the Golem/Mimic bridge-bonus when it LANDS (forward guard, not a current block)

When gandalf's § 4.3 Golem aggregative bridge-bonus + § 4.3-bis Mimic replicative bridge move from DRAFT
into the kernel (the NEXT gamora proxy-bridge dispatch), the in-band guarantee MUST be re-verified — that
is the point at which a count-scaler enters and the scaler-exclusion guardrail becomes load-bearing rather
than trivially-satisfied. Two checks gamora must enforce at that landing:
- The Golem per-proxy bonus is a SINGLE bounded layer (capped, per § 4.3), not stacked atop fission's
  geometric multiplication. With fission's `n×frac=1.2` divergence-without-cap, the Golem bonus must NOT
  multiply the fission army (it bounds count, fission bounds total) — keep them as separate bounded layers.
- Mimic scaler-exclusion (cannot copy the Golem or another Mimic) is enforced in copy-TARGET selection at
  spawn — the structural guard that prevents Mimic→Golem→count→spiral. This is a generation gate (rocket)
  AND a kernel copy-target filter (gamora).

For the CURRENT corpus (fission only, no bridge-bonus in kernel), army power is unambiguously in-band.

## Evidence script

`/tmp/gate3_bridge_check.py` (ephemeral) — reproduces all four guards against the live
`proxy_combatant` kernel. Re-runnable; deterministic; no DB write, no full sim, no corpus regen.
