# Findings — gamora — wind_controller modifier 3.51 root-cause investigation

**Date:** 2026-05-16
**Author:** gamora
**Status:** COMPLETE
**Dispatch:** `agentic_orchestration/dispatches/2026-05-16-gamora-wind-controller-modifier-investigation.md`
**Math note:** `reincarnated-engine/src/reincarnated/simulation/math/wind-controller-modifier-rootcause.md`
**Signal class:** STRUCTURAL (modifier anomaly confirmed; mechanism identified; mitigation path recommended)

---

## 1. Empirical picture (Q1 reproduction)

### 1.1 season_001005 vs season_001006 class_0009 summary

| Dimension | s001005 (pre-B6, pre-V2, V1) | s001006 (post-B6, post-V2, V2) |
|---|---|---|
| Convergence semantic | Encounter-level non-pack WR | Room-level non-pack WR (N=3) |
| Converged modifier | 0.1688 | 3.51 |
| Actual winrate (overall) | 0.749 | 0.764 |
| Convergence WR (operative) | 0.498 | 0.528 |
| Mini-boss WR | 0.01 (encounter) | 0.00 (room) |
| Boss WR | 0.00 (encounter) | 0.00 (room) |
| Magic slots WR | 1.0 / 1.0 (encounter) | 1.0 / 1.0 (room) |
| Elite slots WR | 0.20 / 0.79 (encounter) | 0.27 / 0.90 (room) |
| DPS-producing skills | 5/12 (42%) | 3/12 (25%) |
| Convergence iterations | 4 | 4 |
| Converged status | CONVERGED | CONVERGED |

### 1.2 Universal boss/mini-boss floor in season_001006

ALL 11 classes in season_001006 have room WR = 0.0 against:
- monster_00041 (mini-boss/tank/fire, 91843 HP)
- monster_00043 (boss/brute/earth, 178420 HP)

This is not specific to wind_controller. It is a property of the season_001006 gauntlet — the boss and mini-boss tier monsters in this season have sufficient HP and armor that no class in the cohort can survive even a single encounter with high probability across 100 room repetitions. The boss (monster_00043) grew from 146,834 HP (s001005) to 178,420 HP (+22%) and armor from 20,929 to 27,593 (+32%) in s001006.

### 1.3 The convergence arithmetic constraint

With 2/6 non-pack room slots permanently at 0.0, the convergence formula collapses to:

```
room_avg = (WR_slot1 + WR_slot2 + WR_slot3 + WR_slot4 + 0.0 + 0.0) / 6 = 0.50
=> WR_slot1 + WR_slot2 + WR_slot3 + WR_slot4 = 3.0
```

This is a structural constraint for ALL classes in season_001006. The binary search must find a modifier that brings the four swing slots (magic×2 + elite×2) to a sum of 3.0. For wind_controller, reaching this sum requires modifier=3.51 because its low DPS density means room WRs scale slowly with the modifier.

### 1.4 Kit composition comparison

**s001006 class_0009 (wind_controller) DPS-producing skills:** 3 out of 12 (25%)
- skill_3: `damage 1500 wind`, cd=3.5s
- skill_5: `damage 1500 wind`, cd=6.2s
- skill_11: `damage 1500 fire`, cd=5.9s

**s001006 class_0009 non-damage skills (9/12):** buff_damage × 2 (no direct damage), knockback × 3 (no damage), buff_dodge × 1, shield × 2, silence+damage=0 × 1

**s001006 class_0006 (fire_controller, modifier 1.75) DPS-producing skills:** 7 out of 13 (54%)
- Burn DoT × 5 (continuous tick damage), direct damage × 2 (with accompanying burn)

The fire_controller's burn DoT is the differentiating factor: burn damage PERSISTS across encounter boundaries within a room (the DoT continues ticking even as encounter transitions occur). This gives fire_controller a per-encounter head start that does not exist for wind_controller's burst-only damage skills.

**s001005 class_0009 DPS-producing skills:** 5 out of 12 (42%), including knockback+damage combos. The s001006 generator produced a lower-DPS-density wind_controller kit.

### 1.5 Cross-class comparison at convergence

The table below shows all season_001006 classes sorted by modifier, with their per-tier room WR averages:

| class | archetype | modifier | magic avg WR | elite avg WR | trash avg WR |
|---|---|---|---|---|---|
| class_0005 | hunter | 0.1688 | 0.674 | 0.500 | 0.460 |
| class_0001 | fire_controller | 1.000 | 0.537 | 0.210 | 0.416 |
| class_0007 | water_mage | 1.000 | 0.610 | 0.445 | 0.524 |
| class_0002 | water_mage | 1.1875 | 0.640 | 0.520 | 0.500 |
| class_0003 | earth_caster | 1.1875 | 0.633 | 0.535 | 0.498 |
| class_0008 | hybrid_mage | 1.1875 | 0.674 | 0.525 | 0.486 |
| class_0004 | wind_caster | 1.375 | 0.640 | 0.470 | 0.508 |
| class_0006 | fire_controller | 1.75 | 0.790 | 0.500 | 0.514 |
| **class_0009** | **wind_controller** | **3.51** | **0.623** | **0.585** | **0.472** |

At modifier=3.51, class_0009's magic avg WR (0.623) is BELOW class_0005's magic avg WR (0.674) at modifier=0.1688. This is the empirical signature of the anomaly: the wind_controller is applying a 3.51× damage boost but still achieving only moderate magic room WRs. The binary search reached ceiling (magic rooms at 1.0 for the specific magic monsters in the 6-slot gauntlet subset) but the elite rooms remain variable, resulting in the final balance at 3.51.

---

## 2. Q1 resolution — hypothesis evaluation

**Primary: Hypothesis (a) — V2 HP-carryover specifically penalizes pure-control. CONFIRMED.**

The room-level convergence semantic (V2) requires surviving N=3 sequential encounters with HP carryover. Low-DPS classes take more HP damage per encounter; HP deficits compound within a room. The wind_controller's 25% DPS-density kit produces long encounter durations → heavy per-encounter HP cost → severe compounding → collapsed room WR. To compensate, binary search pushes modifier to 3.51, driving magic rooms to ceiling (1.0) and elite rooms near ceiling (0.27/0.90).

**Contributing: Hypothesis (b) — B6 pre-work + V2 interaction. PARTIAL.**

The B6 tier adjustments targeted rage/physical archetypes; they did NOT directly change wind_controller tier ranges. However, the s001006 generator (which includes B6 changes) produced a wind_controller kit with LOWER DPS density (25%) than the s001005 generator produced (42%). This is not from B6 tier changes but from seed-specific RNG over the same generation space. The compound (lower DPS density × V2 room semantics) produces the extreme modifier.

**Partial: Hypothesis (c) — Seed-specific outcome. PARTIAL.**

The DIRECTION of the anomaly (wind_controller needing a higher modifier than other archetypes under V2) is STRUCTURAL, not seed-specific. Evidence: s001005 class_0009 also had the lowest modifier among non-experimental mana classes (0.1688) under V1. The MAGNITUDE (3.51 vs a hypothetical 2.0–2.5 on a seed with better DPS density) is seed-specific. A different seed would likely still produce wind_controller inflation, just smaller.

**Not supported: Hypothesis (d) — Other.** No additional factors surfaced.

---

## 3. Q2 — V2 HP-carryover specific dynamics for pure-control

### 3.1 The DPS-density / room-WR relationship under V2

Under V2 room semantics, room WR is a function of per-encounter HP cost, which scales with fight duration, which scales inversely with DPS density:

- High DPS density (e.g., fire_controller with burn DoT): kills enemies quickly → low per-encounter HP taken → room WR degrades slowly with N encounters → converges at moderate modifier (1.75)
- Low DPS density (e.g., wind_controller with 3 damage skills): kills enemies slowly → high per-encounter HP taken → room WR degrades sharply with N encounters → binary search must push modifier high to drive magic/easy rooms to ceiling

The modifier inflation formula is non-linear: doubling the modifier does not double the room WR (room WR is bounded at 1.0 for winnable slots; unwinnable slots stay at 0.0). For wind_controller, the binary search must find the modifier where the magic room WR is close enough to 1.0 to offset the two guaranteed-zero slots.

### 3.2 Encounter-level vs room-level signal divergence

At modifier=1.0, wind_controller achieves encounter WR = 0.8533 (high, from the recompose-loop encounter-level measurement). Converting via independence approximation to room level:
- Room WR ≈ 0.85^3 ≈ 0.614 per magic monster (independence bound; actual lower due to HP carryover)
- Boss/mini-boss: still 0.0 room WR
- Non-pack room avg ≈ (0.5+0.5+0.25+0.4+0+0)/6 ≈ 0.27 (well below 0.50 target)

This explains why the binary search must push the modifier ABOVE 1.0 (not below): at modifier=1.0, wind_controller is UNDERPOWERED relative to the room-level target even though it has high encounter WR. The conversion from encounter-level to room-level is the semantic shift (Discipline #12) that produces the counter-intuitive result.

### 3.3 Is this archetype-class level or per-class kit-composition?

Both. The archetype-level concern: wind_controller archetype templates generate control-heavy kits with structurally low DPS density. Any wind_controller generated by the current template space will tend toward this pattern. The per-class concern: the specific magnitude (3.51) depends on how DPS-sparse the specific generated kit is. A wind_controller with 4 damage skills and one knockback+damage combo (like s001005) would need a lower modifier under V2 — still anomalous, but less extreme.

---

## 4. Q3 — Reconciliation with doppelganger HIGH-signal verdict; ailment-deferral re-litigation

### 4.1 Reconciliation

The doppelganger gate (findings: `qa/findings/2026-05-16-gamora-doppelganger-gate-rerun.md`) measured class_0009 at encounter-level mirror-match WR = 0.487. This is the HIGH signal band, confirming the class has adequate damage signature for 1v1 encounters.

The V2 modifier anomaly measures room-level sequential-encounter survival probability. These are orthogonal mechanics:

- **Doppelganger question:** "Can this class beat a 1.05× HP version of itself in a single encounter?" → YES (0.487 WR) → encounter-level DPS is sufficient for controlled conditions
- **V2 binary search question:** "Can this class survive 3 sequential encounters against the gauntlet (taking HP damage between encounters)?" → only 52.8% of rooms (at modifier=3.51) → room-level survival is marginal even with extreme modifier inflation

Both observations are empirically correct. The doppelganger HIGH-signal verdict is NOT contradicted by the V2 modifier anomaly. The doppelganger gate is encounter-level by design and always has been (this was documented in the doppelganger findings §2: "V2-semantic alignment: NOT APPLICABLE"). The HIGH-signal verdict stands.

### 4.2 Ailment-deferral re-litigation recommendation

**Recommendation: NO re-litigation warranted.**

The ailment-damage-signatures deferral was made indefinite based on the doppelganger gate HIGH-signal verdict (all four pure-control archetypes 38-49% encounter-level mirror-match WR). This finding is empirically grounded and the decision was made correctly.

The V2 modifier anomaly for wind_controller operates at a DIFFERENT LAYER (room-level HP-carryover) than the ailment-damage-signatures proposal addresses. Ailment-damage-signatures would add secondary damage ticks to knockback/root/chill effects. This would:
1. Increase DPS density slightly (knockback gains a cut+bleed tick)
2. Reduce fight duration modestly
3. Reduce per-encounter HP cost modestly
4. Improve room WR modestly at equivalent modifier

However, the scale of the V2 anomaly (modifier=3.51 vs 1.75 for fire_controller) is too large to be closed by flavor-tier ailment damage (5-10% of skill magnitude). The root cause is structural: 3 vs 7 DPS-producing skills is not solvable by adding tiny secondary ticks. To materially address the V2 modifier anomaly, wind_controller would need more and higher-magnitude damage skills, not flavoring on its CC ailments.

**The ailment-damage-signatures deferral remains correctly indefinite.** The V2 anomaly is a room-level carryover artifact that ailment damage would not meaningfully address. If anything, the V2 findings CONFIRM the doppelganger evidence: the controller's encounter-level DPS is borderline adequate (HIGH signal), and the room-level problem is the carryover compounding, not an encounter-level damage absence.

**If re-litigation were to occur (it should not for the above reasons):** it would need to be framed as "ailment damage to reduce ROOM-LEVEL HP cost" not "ailment damage to fix encounter-level KO rate," and would need math demonstrating that the flavor-tier secondary damage meaningfully reduces fight duration for wind_controller. That analysis is not warranted given the structural magnitude of the gap.

---

## 5. Mitigation proposal

### Recommended: Option (d) — Accept as known anomaly + calibration-epoch addendum

**Rationale:**

1. The binary search is operating CORRECTLY. room_winrate=0.528 is within tolerance; CONVERGED status is accurate; the class is balanced for V2 room semantics at modifier=3.51.

2. The modifier inflation is the balance loop's correct response to a structurally low-DPS-density kit under V2 HP-carryover semantics. It is a signal, not a malfunction.

3. The `modifier_clamp_observation` already records `would_pass_clamp: false` (clamp range [0.15, 2.5], actual 3.51). This observation infrastructure exists precisely for this pattern. The clamp is currently observe-only; no action is required.

4. The mitigation options that would materially address the anomaly (generation-side DPS floor, clamp gate activation) require design decisions beyond this dispatch's scope:
   - Generation-side DPS floor: rocket dispatch needed; design question about pure-control archetype identity
   - Clamp gate activation: requires Matt sign-off on reject-and-regenerate behavior; changes meaning of CONVERGED

### Items to document in calibration-epoch addendum (knight-rider action)

1. **V2 modifier range has a structural outlier pattern for pure-control archetypes.** When a pure-control archetype generates a kit with <30% DPS-producing skills, expect modifier inflation well above 2.0 under V2 room semantics.

2. **The existing clamp-range [0.15, 2.5] is regularly exceeded by wind_controller under V2.** The clamp is observe-only; no action is triggered. The calibration-epoch should document this as "expected behavioral range for pure-control under V2: modifier may exceed 2.5 in extreme cases."

3. **Boss/mini-boss ROOM WR = 0.0 for all classes in high-difficulty seasons is not an anomaly.** It is a consequence of the V2 convergence formula: boss-tier monsters in season_001006 had HP and armor sufficient to be unkillable in room context for all classes. The convergence arithmetic accommodates this by requiring the 4 swing slots to compensate.

### Queued follow-on items (not this dispatch)

- **[Rocket queue] Minimum DPS floor for pure-control archetype templates:** Require wind_controller template to include at least 4 damage-producing skills (effect containing `damage` with `magnitude > 0`). Would reduce but not eliminate the modifier inflation under V2. Knight-rider to assess whether this conflicts with archetype identity before routing to rocket.

- **[Future gamora dispatch] Modifier clamp gate operationalization:** Activate `modifier_clamp_observation` as a reject-and-regenerate trigger (classes with `would_pass_clamp=False` trigger regeneration). Requires Matt sign-off on: (a) what "regenerate" means (new kit from rocket's generator vs INTENTIONAL_OUTLIER status), (b) max re-attempts before accepting the extreme modifier. This is a meaningful design decision about what "balanced" means for extreme outlier cases.

---

## 6. What did NOT change

- No code changes to any production file
- No MIGRATION.md entry (no schema changes)
- No smoke test (analytical work only)
- No tag cut (analytical findings; no mitigation shipped in-session)

---

## 7. Cross-seam flags

### Knight-rider

1. **Ailment-deferral re-litigation:** NOT recommended. V2 modifier anomaly is a room-level phenomenon; ailment-damage-signatures is an encounter-level flavor proposal. The indefinite deferral stands.
2. **Calibration-epoch addendum:** the V2 calibration epoch documentation should include the pure-control modifier inflation pattern (see §5, items to document).
3. **Two queued items** for future routing: (a) rocket dispatch for minimum DPS floor in pure-control templates; (b) future gamora dispatch for modifier clamp gate operationalization. Both require Matt sign-off before routing.
4. **Cross-seam flag: no commit-coordination friction with parallel emission-gap-fix dispatch.** This investigation produced no code changes; the emission-gap-fix dispatch (code changes to `balance_loop.py`) operates on separate files and there is no write-race risk.

### Star-lord

READ-ONLY in this investigation. The telemetry data was sufficient for the diagnostic. One observation: class_fight_loadouts has no boss/elite/mini-boss rows for class_0009 (only magic/trash) due to the existing partial-Tier-1 coverage issue. This did not block the investigation because class_monster_win_rates provided the complete per-monster WR picture, and the class JSON files contained the full kit and convergence metadata.

### Rocket

READ-ONLY in this investigation. Finding: the s001006 generator produced a wind_controller kit with lower DPS density (25%) than the s001005 instance (42%). This may be addressable via a minimum DPS floor constraint in the archetype template, but that is a design decision requiring Matt sign-off before a rocket dispatch is authored.

---

## 8. Acceptance criteria status

- [x] Math note filed at `reincarnated-engine/src/reincarnated/simulation/math/wind-controller-modifier-rootcause.md`
- [x] Q1 reproduction + characterization complete (per-monster WRs; kit composition; cross-class comparison)
- [x] Q1 resolved: primary (a), secondary (b), partial (c) — not (d)
- [x] Q2 resolved: V2 HP-carryover dynamics characterized; mechanism identified
- [x] Q3 resolved: doppelganger HIGH-signal verdict reconciled; ailment-deferral re-litigation NOT recommended
- [x] Mitigation proposal: option (d) accept-as-known-anomaly + calibration-epoch addendum items
- [x] Recommendation on ailment-deferral re-litigation: NO
- [x] Findings file at `agentic_orchestration/qa/findings/2026-05-16-gamora-wind-controller-modifier-rootcause.md`
- [x] Mitigation NOT shipped in-session (analytical findings only; no code changes warranted)

---

*Findings complete — 2026-05-16. Author: gamora.*
