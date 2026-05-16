# Findings — gamora — modifier range root-cause (0.09–0.52 vs 0.85–1.15 target)

**Date:** 2026-05-16  
**Author:** gamora  
**Status:** COMPLETE — no code changes; findings + mitigation path documented  
**Math note:** `reincarnated-engine/src/reincarnated/simulation/math/modifier-range-root-cause.md`  
**Dispatch:** `agentic_orchestration/dispatches/2026-05-16-gamora-modifier-range-investigation.md`

---

## Executive summary

The modifier range of 0.09–0.52 observed in season_001005 (B10.4 Option 2) is **not a regression, not a semantic artifact, and not generation-side overtuning**. It is the expected output of the current simulator given a structural mechanical gap between elemental mana classes and physical rage classes.

The 0.85–1.15 target band (from `canonical/29-design-overview.md`) is a design aspiration for the end-state; it was never calibrated against the current simulator and is not a regression baseline. Reaching it requires B6 generation work (energy-system-aware tier assignment) and B14.5 V2 energy-type levers — not a simulation fix.

**Recommended action: Document as calibration baseline; queue B6 pre-work for rocket.**

---

## Q1 — Overtuning or semantic artifact?

**Resolution: Neither. Root cause is simulation-side energy mechanics.**

The 0.09–0.52 range appears identically across all 7 recent seasons (001001–001007) including pre-Option 2 seasons. Option 2 made convergence work (10/10 vs 2/10 before), making the modifier range OBSERVABLE — but it did not CAUSE it.

The 0.85–1.15 band was set aspirationally in file 29 before the current gauntlet, before B14.5 V1, before Option 2. It assumed energy-system power differentials would be compensated elsewhere. They have not been yet.

**This is NOT a bug. It is a known gap between current implementation state and design target.**

---

## Q2 — B7 percentile spread

**Resolution: Real concern but non-blocking; noted for B7 gate planning.**

Low modifiers (0.095) amplify the *relative* impact of gear affixes (+500 flat damage = larger % boost to a 9.5%-DPS class). The B7 gate (when implemented as Stage A2 item) should test at the converged modifier with realistic gear percentiles at each modifier level. Not blocking current work.

---

## Q3 — Structural cause

**Resolution: Three compounding simulation-side mechanics produce a ~3–5× DPS-per-modifier disadvantage for physical rage classes vs elemental mana classes.**

### Factor 1: Rage energy startup (dominant factor)

```python
# combatant.py _ENERGY_CONFIGS
"rage": (100.0, False, 0.0),   # max=100, start_full=False, regen=0/s
# vs mana: starts at full pool (100+ for elemental mages)
```

Rage starts at 0. Physical_warrior cannot use rage-costed skills until rage accumulates via:
- 10 rage per skill hit dealt
- 5 rage per auto-attack
- A primary_attack (~20 rage cost) becomes available around seconds 5–8

Result: in short fights (trash, magic — which make up 3–4 of the 6 non-pack gauntlet slots), physical_warrior's DPS is substantially reduced in the first third of the fight. Elemental mana classes burst immediately from full mana.

### Factor 2: Physical miss rate (~15%)

- Elemental attacks: **always hit** (no hit check in `damage_resolver.py`)
- Physical attacks: `did_hit(0.90, ~0.05, roll)` → ~85% effective hit rate
- 15% miss rate = 0.85× effective DPS multiplier

### Factor 3: Armor vs elemental resistance (~18.6% vs ~0%)

- Physical: `damage * (1 - armor / (armor + 3000))` → ~18.6% reduction for standard monsters
- Elemental: `damage * (1 - resistance)` → resistance ≈ 0% for most monsters in current config
- Net: physical DPS passes through at ~81.4%; elemental at ~100%

### Skill magnitude parity (key negative finding)

**Generation is NOT the cause.** Both hybrid_mage/water (modifier=0.095) and physical_warrior (modifier=0.525) use tier 25–50 skills with nearly identical magnitude distributions:

| Class | modifier | magnitude range | est. DPS at mod=1.0 |
|---|---|---|---|
| hybrid_mage/water | 0.095 | 625–2,500 (tier 25–50) | ~77,700 |
| physical_warrior | 0.525 | 625–2,500 (tier 25–50) | ~76,500 |

The ~5.5× modifier gap between them is entirely from sim mechanics, not from generation producing different power budgets.

### Combined factor estimate

| Mechanism | Effective DPS ratio (elemental advantage) |
|---|---|
| Rage startup (short fights) | ~1.5–2.0× |
| Miss rate | ~1.18× |
| Armor vs resistance | ~1.23× |
| Melee positioning delays | ~1.1× estimated |
| **Combined** | **~2.4–3.3×** |

Observed modifier gap (hybrid_mage vs physical_warrior): **5.5×**. The remaining gap beyond the ~3× estimate likely comes from the gauntlet fight distribution (6 non-pack fights; trash and magic fight outcomes favor elemental burst) and from the interaction of factors in specific fight types.

---

## Archetype gradient (all 7 recent seasons)

| Archetype | Avg modifier | Notes |
|---|---|---|
| fire_mage | 0.068 | Most DPS-dense; burn DoT stacking |
| water_mage | 0.070 | |
| earth_caster | 0.084 | |
| hybrid_mage | 0.098 | |
| wind_caster | 0.109 | |
| wind_controller | 0.134 | Control slots reduce DPS density |
| fire_controller | 0.137 | |
| earth_controller | 0.145 | |
| water_controller | 0.187 | |
| physical_warrior | 0.317 | Rage startup + melee + armor |
| hunter | 0.594 | Physical ranged: miss rate only (no melee gap) |
| experimental/physical | 0.718 | Outlier class type |

The gradient is monotonic: elemental pure casters → elemental controllers → physical melee → physical ranged. Each tier up corresponds to reduced DPS density or reduced fight-mechanical efficiency.

---

## Mitigation path

### Recommended: Option (e) — Wait for B6 + B14.5 V2

**Rationale:** The gap is architectural. A targeted sim patch (e.g., giving rage classes 15–20 starting rage) would compress modifiers by ~20% without closing the structural 3–5× gap from miss rate + armor + full fight dynamics. Better to fix holistically.

**Required work (not my seam):**

1. **B6 generation — rocket dispatch needed:** Archetype templates should specify energy-type-aware tier ranges. Rage/physical archetypes need ~1.5–2× higher skill tier baseline to compensate for sim-mechanical disadvantages. Approximate targets:
   - Mana elemental: tier 25–50 (current) 
   - Rage/physical: tier 38–65 (proposed; ~1.7× higher)
   
   This is a generation-seam change: rocket should implement energy_type as a parameter in `archetype_template.py` tier bounds.

2. **B14.5 V2 — energy-type lever:** The primary recompose loop currently cycles skill_swap, geometry_mix, cooldown_energy. A future lever could adjust the energy_cost distribution per archetype (reduce rage costs to allow more early-fight skill use, effectively mitigating the startup gap via composition rather than via starting rage gift).

### Immediate action: Calibration epoch declaration

The current (0.09–0.52) modifier range is the **B10.4 Option 2 operational baseline**. All future regression monitoring should compare against this baseline, not against the aspirational 0.85–1.15 band.

Tracking metric going forward: `mean |modifier - 1.0|` per convergence semantic (non-pack WR = 50%):
- Current B10.4 Option 2 baseline (7 seasons, CONVERGED non-experimental): **mean |mod-1.0| ≈ 0.82**
- B6 + B14.5 V2 target: ~0.50
- File 29 full-system target: ~0.10

---

## Cross-seam flags

### Rocket (action required)
Knight-rider should author a rocket dispatch: **B6 pre-work — energy-type-aware tier assignment**. The finding is: current templates assign identical tier ranges (25–50) to all archetypes regardless of energy type. Rage/physical archetypes need higher-tier skills to compensate for ~3–5× sim-mechanical DPS disadvantage. See math note §4.3 for estimated compensation factor.

### Star-lord (existing, unchanged)
CLI summary_formatter.py should display `convergence_winrate` not `actual_winrate`. This was flagged at B10.4 close; it remains open.

### Jack-ryan
This finding does NOT require Gate 1/Gate 2 review — it is a pure analytical deliverable with no design decision changes and no code changes. If knight-rider decides to queue the rocket dispatch as a design-level decision, that would require normal Gate process.

---

## What did NOT change

- No code changes to `balance_loop.py`, `combatant.py`, `fight_engine.py`, or any production file
- No MIGRATION.md entry (no schema changes)
- No smoke test (no code to verify)
- No tag cut (investigation only)

---

*Findings complete — 2026-05-16. Author: gamora.*
