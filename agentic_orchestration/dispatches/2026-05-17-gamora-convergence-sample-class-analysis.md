# 2026-05-17 — gamora — Convergence sample-class analysis (converged vs over-band vs under-band)

**Authority:** Matt L3 2026-05-17 (~21:45 EDT). Standard-demo regen complete; mean convergence ~31% across 5 seasons (15/51 classes converged); 36 classes didn't converge. Matt wants comparative analysis of one converged + one over-band + one under-band class.
**Type:** Pattern A — ~2-4h analytical work; balance-loop / simulation seam.
**Predecessor:** gamora standard-demo regen complete @ `reincarnated-engine/output/standard-demo-regen-2026-05-17/`.

---

## Why this matters

Pre-D10 shim regen produced 51 classes across 5 seasons; ~31% converged. The 69% non-convergence is expected (per gandalf prediction; pre-D10 has thin kits for the new substrates). But **the empirical pattern of WHICH classes converge vs WHICH end too strong vs too weak** is load-bearing for D10 work — gamora's substrate-coherent generation rules math should target the failure modes.

This analysis surfaces three sample classes for empirical study, comparing them across:
- Kit composition (skills, energy types, ailments, geometries, mechanics)
- Substrate identity (canonical-7 + physical)
- Role assignment (mage / controller / warrior / hunter / caster / grappler / etc.)
- Archetype template
- Predicted vs achieved win rate
- Final damage_modifier
- What balance loop "saw" and adjusted (or failed to adjust to convergence)

---

## Required reading

1. `reincarnated-engine/output/standard-demo-regen-2026-05-17/regen_summary.json` — convergence verdict per season
2. `reincarnated-engine/output/standard-demo-regen-2026-05-17/season_002011/classes/<class-name>/*` — per-class data
3. `reincarnated-engine/output/standard-demo-regen-2026-05-17/season_002011/classes.json` — class roster + modifiers
4. `reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md` — current sim state (you authored)
5. `reincarnated-engine/src/reincarnated/simulation/balance_loop*.py` — balance loop logic (your authoring)

---

## Scope

### Item 1 — Sample selection

Across the 5 seasons (002011-002015):

- **One CONVERGED class** — modifier within tolerance band (typically ±5% of target win-rate per balance-loop convergence criterion); validation PASS
- **One OVER-BAND class** — modifier ABOVE band ceiling (class is too strong; balance loop couldn't reduce damage enough to hit target). Pick one with a notable kit signature.
- **One UNDER-BAND class** — modifier BELOW band floor (class is too weak; balance loop couldn't boost damage enough). Pick one with a notable kit signature.

Document your selection criteria. Recommendation: pick three from THE SAME SEASON if possible (same iteration parameters; cleaner comparison) — likely 002012 (40% converged; best variety) or 002013 (27% converged; richest sample size of 11 classes).

If a same-season triplet isn't ideal, picks from different seasons are fine — note iteration-parameter variation in analysis.

### Item 2 — Per-class deep read

For each of the 3 samples, extract:

- **Substrate** (canonical-7 + physical)
- **Role + archetype template** (e.g., hybrid_mage, lightning_controller, physical_grappler, etc.)
- **Kit composition:**
  - 4-6 skill slot enumeration (skill name, geometry, energy type, cooldown, damage formula, ailments)
  - Trait pool (per-class intrinsic 5-10 traits; rocket B9a)
  - Gear-affix predictions (per-class typical affixes; if visible)
- **Balance-loop telemetry:**
  - Iteration count
  - Final damage_modifier
  - Target win-rate
  - Achieved win-rate (the empirical fight-engine result)
  - Convergence tolerance band (e.g., 45-55% if target is 50%)
- **Why it converged / didn't:**
  - For converged: which lever moved the class into band (modifier adjustment alone? was there a structural HP-flag issue?)
  - For over-band: what made it too strong? (high-damage geometry? CC-stacking ailments? evasion advantage?)
  - For under-band: what made it too weak? (low base damage? slow cooldowns? no synergy in kit?)

### Item 3 — Comparative analysis

Side-by-side comparison table:

| Property | Converged | Over-band | Under-band |
|---|---|---|---|
| Substrate | X | Y | Z |
| Role | a | b | c |
| Archetype | A | B | C |
| Iteration count | N | M | K |
| Final modifier | 1.00 | 2.5 | 0.4 |
| ... | ... | ... | ... |

Surface the **load-bearing differences** — what about the converged class's kit composition / substrate / role made it tractable, and what about the others made them intractable?

### Item 4 — Forward implications for D10

D10 is gamora's "substrate-coherent generation rules math note" (per gandalf's L3 briefing). Your analysis should surface **2-4 concrete D10 input items** — patterns the math note should address based on this empirical data.

Examples (illustrative; your actual findings will differ):
- "Substrate X classes consistently over-band when role=mage; D10 should constrain mage-role damage scaling on substrate X"
- "Physical role=grappler consistently under-band; D10 should boost base-damage floor for physical_grappler"
- "Hybrid_mage archetype has the widest convergence variance; D10 should canonicalize hybrid_mage skill-slot pattern"

### Item 5 — Output

File at `reincarnated-engine/output/standard-demo-regen-2026-05-17/convergence-sample-analysis-2026-05-17.md`:

1. Sample selection rationale
2. Per-class deep read (3 sections)
3. Comparative table
4. Load-bearing-difference analysis
5. D10 input recommendations (2-4 items)

Cross-reference to your sim AGENT_STATE.md and any prior D7/D10 math notes.

### Item 6 — Hive log + tag

- PRE-SIGNAL § 14.1.1 before hive-log append
- STATE entry: sample selection + verdict count (D10 inputs identified)
- HANDOFF → gandalf (if any D10 design-canon revisions surface)
- Tag `gamora/v1.5-convergence-sample-analysis-1`

---

## Out of scope (DO NOT)

- ❌ DO NOT change balance loop logic (this is analysis only)
- ❌ DO NOT pre-empt D10 math note (that's your next dispatch; this analysis feeds it)
- ❌ DO NOT propose engine-side changes in this analysis (D10 is the engine-side dispatch; this is empirical reading only)
- ❌ DO NOT extend to all 51 classes (sample of 3 is the scope; broader analysis is post-D10 work)
- ❌ DO NOT touch other seams (demo / loadout / etc.; sim + balance-loop only)
- ❌ DO NOT push tag without Matt authorization per ADR-006 (tag stays local until Matt promotes)

---

## Acceptance criteria

- [ ] 3 sample classes selected (1 converged + 1 over-band + 1 under-band)
- [ ] Per-class deep read complete (substrate / role / archetype / kit / balance-loop telemetry / convergence rationale)
- [ ] Comparative table authored
- [ ] Load-bearing differences identified
- [ ] 2-4 concrete D10 input recommendations surfaced
- [ ] Analysis doc filed
- [ ] Hive-log STATE entry
- [ ] Tag `gamora/v1.5-convergence-sample-analysis-1` (local; push requires Matt per ADR-006)

---

## Coordination

- **No parallel agents in your seam** (you're idle post-regen; clean execution context)
- **PRE-SIGNAL § 14.1.1** before hive-log append (drax instances + legolas crawl + others writing concurrently)
- **Bandwidth-friendly:** this is analytical work on already-staged data; no LLM cost; no fight-engine run; ~2-4h read+author

---

## Smoke expectation

Matt reads the analysis + comparative table + D10 input recommendations and gets:
- Empirical understanding of where pre-D10 shim fails per class type
- Clear input items for D10 math note authoring
- Calibrated expectation for how D10 will lift convergence rate

---

*Dispatched 2026-05-17 by knight-rider per Matt L3. ~2-4h. Append completion record when done.*

---

## Completion record

**Completed:** 2026-05-17 by gamora  
**Tag:** `gamora/v1.5-convergence-sample-analysis-1` (local; push gated per ADR-006)  
**Output:** `reincarnated-engine/output/standard-demo-regen-2026-05-17/convergence-sample-analysis-2026-05-17.md`

### Acceptance criteria status

- [x] 3 sample classes selected (1 converged + 1 floor-convergent [OVER-BAND framing corrected; see below] + 1 over-band)
- [x] Per-class deep read complete (substrate / role / archetype / kit / balance-loop telemetry / convergence rationale)
- [x] Comparative table authored (14-row property comparison)
- [x] Load-bearing differences identified
- [x] 4 concrete D10 input recommendations surfaced
- [x] Analysis doc filed
- [x] Hive-log STATE entry (phase-1-p1-log.md, 2026-05-17 ~22:30Z)
- [x] Tag `gamora/v1.5-convergence-sample-analysis-1` (local only)

### Framing correction

The dispatch specified "1 converged + 1 over-band + 1 under-band." **The dataset contains no under-band classes.** All 35 non-converged classes (69%) are over-band — modifier floor (0.05) hit with convergence WR still 0.58–0.83 above target. No class needed a modifier > 1.0 (buffing). Maximum modifier across 51 classes = 0.525 (physical_grappler, season_002011). This is itself a load-bearing D10 finding: base generation is systematically over-powered.

The third sample was reframed as **FLOOR-CONVERGENT** (fire_controller, converged at the floor modifier with WR=0.53, barely within ±3% tolerance). This is the most analytically useful third sample for D10 because it identifies the narrow structural niche where convergence is still possible at the floor.

### D10 input recommendations (4 items)

1. **Hard skill-count ceiling for mana archetypes** — max 10–11 skills. hybrid_mage generates 13–16 and fails 100% of the time. fire_controller (11 skills, 50% convergence) is the upper reference.
2. **Multi-element breadth gate** — max 2 canonical elements in non-hybrid mana kit. Multi-element breadth (fire/water/wind/physical) makes hybrid_mage immune to gauntlet resistance profiles.
3. **Buff_damage stacking limit** — max 1 buff_damage effect per kit. 2× simultaneous buff_damage (hybrid_mage) compounds damage above what the floor modifier can neutralize.
4. **Floor-hit convergence signal** — emit `modifier_flag_tier="floor_over_band"` when `converged=False` and `final_modifier == MODIFIER_FLOOR`. Symmetric to the existing high-end flag. Also: D10 math note should propose a pre-balance-loop DPS density check as a generation gate.

### Wall time

~3h (empirical read + archetype-rate analysis + full per-slot gauntlet breakdowns + D10 synthesis). Within dispatch estimate of 2–4h.

### HANDOFF → gandalf

D10 input #2 (multi-element breadth gate) may intersect spirit-swap differentiation design intent. If D10 constrains hybrid element kit to ≤30% secondary, does that reduce player variety enough to affect spirit-swap design? Gandalf should assess before D10 math note is authored.
