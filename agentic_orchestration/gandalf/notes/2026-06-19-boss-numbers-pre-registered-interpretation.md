# Pre-registered interpretation rule — clean boss-numbers run

**Author:** gandalf
**Date:** 2026-06-19 (written BEFORE the gamora run returns — deliberately)
**Why pre-register:** Gate-1 just caught me reading a regime-mixed artifact into my own prior (the "STR survival crater" that was a tier_2-never-ran default). The antidote to motivated reasoning is to fix the read BEFORE the data lands. This note binds how I will interpret the run's headline (the `a_dead` / `timeout` / `b_dead` termination split per archetype), so I cannot post-hoc rationalize whatever comes back.
**Consumes:** output of `agentic_orchestration/dispatches/2026-06-19-gamora-clean-boss-numbers-harness.md`.

---

## The single fact the run produces

For each archetype (caster int/wis, dex, str), on `boss_with_adds` + `mini_boss`, at faithful power, with tier_2 actually running (KPM-reject bypassed): the distribution over fight terminations —

- **`b_dead`** = boss killed, player alive (clean win)
- **`a_dead`** = player died before the boss did (defensive failure)
- **`timeout`** = both alive at the 240s enrage cap (survived, didn't kill in time)

— plus survive+kill rate (= `b_dead` fraction), TTK on wins, and proxy-inclusive KPM (sanity rail).

## Per-archetype read (BOUND IN ADVANCE)

For the STR boss-crater specifically (the question that drove the run):

| Run result for STR bosses | What it MEANS | Boss-bridge disposition |
|---|---|---|
| **`b_dead`-healthy** (high survive+kill) | The "STR boss-crater" was a **pure KPM-reject artifact.** STR kills bosses fine at faithful power; the gate fabricated a crater by rejecting on KPM before survive+kill ran. | **No crater. No bridge member.** The doctrine fix (stop KPM-gating bosses) alone restores STR. Strongest possible vindication of the doctrine. |
| **`timeout`-dominant** (survives, rarely kills in 240s) | STR is **slow-but-survivable** — exactly the legitimate "outlast it" boss kill the KPM ceiling wrongly condemns, OR a genuine damage-shortfall against the enrage timer. | **Borderline.** Doctrine still right (survival ≠ the problem), but a real DPS-against-enrage question. Feeds the Tier-B DPS-measure case directly. Possible encounter-tuning (enrage length) rather than a kit fix. |
| **`a_dead`-dominant** (dies before killing) | The crater is **real and defensive** — STR genuinely cannot survive the boss at faithful power. | **Real bridge member.** Survival IS the binding constraint; the KPM-reject was accidentally shielding players from un-survivable content. Composer/kit work warranted. |

Same three-way read applies to dex and (as a control) caster. Caster is expected `b_dead`-healthy (spine §5 had casters PROVISIONAL_PASS + tier_2 survival 1.00, which WAS real — tier_2 ran for them). If caster comes back anything but `b_dead`-healthy, something deeper is wrong and the whole regime is suspect.

## Doctrine-level reads (independent of which archetype craters)

1. **Does survive+kill DISCRIMINATE on bosses?** If the termination split varies meaningfully across archetypes/cohorts, survive+kill is a real gate signal → the win-condition split is justified. **If EVERY archetype is uniformly `b_dead`-healthy**, bosses don't discriminate at all under survive+kill → the boss gate is near-vacuous and the doctrine's value is mostly the *removal of the wrongful KPM ceiling*, not the survival gate per se. Either is a real finding; I commit to reporting whichever.
2. **Falsification condition (honesty check):** the doctrine is WEAKENED if `a_dead`-dominant is near-universal — that would mean the KPM gate, by rejecting low-KPM boss attempts, was incidentally preventing players from entering fights they'd lose, i.e. acting as a crude survivability proxy. I would then have to argue the survive+kill gate is a *better* expression of the same protection, not a new permission. I commit to making that argument honestly rather than burying the result.
3. **Over-performance ceiling check:** the boss KPM band tops at p90 (`boss_with_adds` 3.78 mobs/min). If the won-fight KPM distribution shows a real mass ABOVE 3.78 (boss-melts), that empirically confirms the ceiling is clipping the power-fantasy payoff — the §2 asymmetry argument made concrete. If almost nothing exceeds 3.78, the ceiling is rarely binding and the asymmetry argument is theoretical, not yet biting.

## What this run does NOT settle (do not overclaim)

- **DPS** (Matt #8) — scoped out; the `timeout`-vs-`b_dead` split only *motivates* the DPS-measure case, it does not deliver the measurement.
- **Clear-room bands** — untouched; this run is boss-only.
- **rogue crater** — the spine flagged the rogue crater was also synthetic-regime; this run covers attribute-parsed cohorts, not the rogue-composer question specifically. If the data permits a rogue read, treat it as secondary.

---

**Signed:** gandalf, 2026-06-19 — the read, fixed before the data, so the data rules me and not the reverse.
