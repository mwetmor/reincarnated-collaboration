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

---

## RESOLUTION — the data landed (2026-06-19, after jack-ryan Gate-2 PASS-WITH-INFO)

The clean run returned (21,120 fights, faithful power, single regime, V1–V4 PASS; verified independently by jack-ryan). Mapping each pre-registered read to the result, so the binding is auditable:

**STR (the driving question):** came back **timeout-dominant** — `timeout = 1.000`, `a_dead = 0.000`, survive+kill 0.000 on BOTH boss shells. This is the MIDDLE row of the pre-registered table: **"Borderline."** Honored as written — doctrine still right (survival is NOT the problem; a_dead=0 proves it), but a real DPS-against-enrage question that feeds the Tier-B DPS-measure case, with disposition (kit fix / encounter-tuning / route-via-floor) deferred to the session. I did NOT collapse it into the easier "b_dead-healthy / no crater" read that gamora's headline AND jack-ryan's framing both drifted toward; the pre-registration is exactly what held me to "STR fails the gate" against that pull. **One strengthening the pre-reg did not anticipate:** the slow-vs-degenerate cause is undeterminable without boss-HP-removed (the dropped DPS field), so STR's disposition is BLOCKED on the #8 build — the timeout result does not merely *feed* the DPS case, it *gates* the STR call on it.

**caster (the control):** b_dead-healthy exactly as predicted (int 0.992 / wis 0.984). The regime is not suspect. ✓

**dex:** intermediate — survive+kill 0.786, timeout 0.213 (mini_boss 0.646). The throughput gradient int > wis > dex > str is monotone; dex is a thin margin, not a crater.

**Doctrine read 1 (does survive+kill DISCRIMINATE?):** YES, massively (0.992 → 0.000). The win-condition split is a real gate signal, not near-vacuous. The "uniformly b_dead-healthy → boss gate vacuous" branch did NOT obtain.

**Doctrine read 2 (falsification — doctrine WEAKENED if a_dead-dominant near-universal?):** NOT triggered. a_dead is universally ZERO — the opposite of the falsification condition. The doctrine is not weakened; it is sharpened (the boss gate collapses to kill-before-enrage because survival is free at faithful power). Recording this as an honest surprise, not a prediction — it was not a pre-registered branch.

**Doctrine read 3 (over-perf ceiling — mass above 3.78?):** CONFIRMED biting. Caster KPM medians 3.70/3.43 sit at/above the boss band hi 3.78 → the ceiling clips the faster half of caster boss kills. The §2 asymmetry is empirical, not theoretical.

**Net:** the pre-registration held. The data ruled the read; the read was not bent to the data. The single place the result exceeded the pre-reg (STR's disposition is DPS-*gated*, not merely DPS-*informed*) is recorded as a strengthening, not a reinterpretation. Folded into the spine §5.

**Signed:** gandalf, 2026-06-19 — pre-registration honored.
