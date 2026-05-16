# CP2b Notes and CP3 CLI Prompt

**Captured:** 2026-05-09 (end of day)
**Branch:** `work/priority-02-gear` (engine repo)
**Tests:** 669 passing
**Status:** CP2b done; ready for CP3.

## What CP2b landed

- **Weapon roster expansion:** wand (1H) and greatsword (2H) added.
- **Off-hand base types:** shield, off_hand_dagger, off_hand_sword, grimoire, orb, focus.
- **Handedness:** `handedness: str` on both `BaseItemType` and `GearInstance`. Greatsword is the only `"2h"` entry; wand is `"1h"`.
- **Block fields on GearStats:** `block_chance` and `block_value`. Defaults to 0.0 everywhere; shields populate real values at item creation. Resolver wiring deferred to CP3.
- **Loadout → 4 slots:** weapon, off_hand, armor, accessory. The off_hand slot is auto-excluded by `combined_stats()` and `total_power_score()` whenever `weapon.handedness == "2h"` (or no weapon equipped).
- **Sampling:** `sample_scenario_loadout()` samples off_hand only when the drawn weapon is 1H. `generate_season_gear_pool()` covers all 4 slots.
- **Fit profile overrides** in `_BASE_TYPE_FIT_OVERRIDE` for all 8 new base types:
  - wand → mana / control
  - greatsword → rage / close / damage
  - shield → stamina / control
  - grimoire → mana / support
  - orb → mana / damage
  - focus → focus / long
  - off_hand_dagger and off_hand_sword → physical
- **Placeholder field:** `stat_requirements: dict` on `GearInstance`, empty until CP5b populates it.
- **Migration 1.6** extended with `handedness` column. Recorder updated.
- **Plan revised** to 13-CP structure (CP5b and CP5c inserted; CP3 expanded with block; CP6/CP7 carry signature/API changes).

## Notes / observations

- CP2b was a clean checkpoint with no architectural surprises beyond the four already surfaced and resolved (4-slot Loadout, convergence-loop validator, AffixSpec schema question, block ordering).
- The `_BASE_TYPE_FIT_OVERRIDE` table is now the natural extension point for further base-type additions (maul, spear, etc.) without disrupting the dimensional vocabulary. Worth keeping in mind for the deferred-list items in `../canonical/17-gear-and-spirit-guide-design.md`.
- The 4-slot Loadout's auto-exclusion logic for 2H weapons is what makes the marginal-value math correct — the Spirit Guide's eventual `evaluate_gear_swap()` (CP7) doesn't need to special-case off-hand presence; the loadout primitives already handle it. This is good pre-investment.
- The fit override for `shield → stamina / control` is a defensible call but worth confirming against the convergence data later — physical_warrior is the canonical shield user and warriors run on rage, not stamina. If shields underperform on warrior loadouts in CP6 convergence, this override is the first place to look.

## Carried over to later checkpoints

- **CP3 — block resolver wiring.** Locked design call: block fires *before* crit. Resolver flow:
  ```
  hit-check → block-check
             ├─ blocked → damage = base × (1 − block_value); skip crit; armor still applies
             └─ not blocked → crit-check → armor → apply
  ```
- **CP5b — equip eligibility.** Populate `stat_requirements`, build `can_equip()` validator, change `sample_scenario_loadout(catalog, rng)` → `sample_scenario_loadout(catalog, class_stats, rng)`. The convergence-loop usage is load-bearing — without validator coverage in the sim, the balance loop can produce fire-mages-in-plate.
- **CP5c — affix coherence.** Open architectural question: extend existing `EffectPoolEntry` with `dimensional_tags` + `stat_affinity` fields, or create parallel `AffixSpec` schema. Investigate before duplicating; ~10 minutes reading the existing pool code should clarify.
- **CP6 — convergence integration.** Signature change to `sample_scenario_loadout()` lands here. Also where the epic/legendary power-score max overhang (~0.67 vs. plan ~0.55) gets validated; if convergence variance is stable, the overhang is acceptable.
- **CP7 — Spirit Guide engine API.** `evaluate_gear_swap()` handles 1H↔2H swaps as multi-slot comparison. For 2H candidate vs. current 1H+off_hand: marginal includes off_hand contribution loss. For 1H candidate vs. current 2H: recommend the 1H first if it beats the 2H solo, let off-hand recommendations follow on the next pass.
- **AGI stat:** confirmed dead/reserved per CLI's `migrations.py:110` inspection. One-line note in `notes/plans/priority-02-gear.md`. No code change.

## CP3 instruction (paste into CLI when resuming)

```
Proceed with CP3. Three workstreams per the plan:

1. Dead-field audit — identify and remove any gear-related fields that have been declared but are not yet read or written in the live pipeline. Do NOT remove placeholders for upcoming CPs (`stat_requirements` for CP5b; affix tag fields for CP5c). Surface anything ambiguous before deleting.

2. Gear stat wiring into combat sim — `GearStats` from equipped gear flow into `CombatantState` at fight initialization. Touch points include damage resolver inputs, ability-modifier application, and on-hit effect resolution. Tests should verify equipped gear's stats actually take effect during fights, not just sit on the actor.

3. Block mechanic in damage resolver — design call locked: block fires BEFORE crit. Resolver flow:

       hit-check → block-check
                  ├─ blocked → damage = base × (1 − block_value); skip crit; armor still applies
                  └─ not blocked → crit-check → armor → apply

   Two new derived fields on `CombatantState`: `block_chance`, `block_value`, populated from equipped shield's `GearStats` (0.0 if no shield equipped). One new resolver branch.

CP3 acceptance tests:
- Sample equipped loadout: gear stats observable in combat resolution
- Shield equipped: block fires at expected probability across N fights (statistical, not exact)
- No shield: block_chance = 0; never blocks
- Block + crit: blocked hits do not crit
- Block + armor: armor still applies after block reduction

Stop after CP3, report in the standard format (built / learned / surprised / next), wait for go-ahead before CP4.

Lookahead note (not for CP3 work): when CP5c approaches, you'll need to investigate whether `EffectPoolEntry` can be extended with `dimensional_tags` + `stat_affinity` vs. creating a parallel `AffixSpec` schema. If you happen to have the relevant file open during CP3, a 5-minute skim of the existing pool's shape is welcome — saves time at CP5c. Not a CP3 deliverable.
```

## Cross-references

- `../canonical/17-gear-and-spirit-guide-design.md` — gear architecture (substantially updated 2026-05-08/09 with option C, off-hand mechanics, affix coherence)
- `18-cli-priority-02-gear-prompt.md` — original CLI session prompt
- `../canonical/19-llm-call-map.md` — LLM call inventory (gear delta: ~25 calls/season)
- `21-morning-orientation-2026-05-10.md` — orientation prompt for tomorrow
