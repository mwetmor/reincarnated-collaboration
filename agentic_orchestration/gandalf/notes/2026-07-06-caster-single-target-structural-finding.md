# Caster single-target structural finding — the fossilized weapon ratio + the vanishing pack channel

> **Trigger:** Matt Q (2026-07-06, post-Leg-B-HALT): *"Could the issue simply be that physical kits have the added damage of their weapons whereas we are not adding damage to caster's weapons? … What are the highest damage skills for physical kits vs caster kits? What is the damage of those specific skills based on?"*
> **Method:** direct engine read (damage_resolver.py, per_skill_emitter.py, combatant.py, math_model.py) — every claim carries file:line. Survey-mode: what-IS, then the design consequence.
> **Author:** gandalf (ARCHITECT), 2026-07-06. **Resolves the Leg-B HALT fork toward world (1) — chassis under-built — with a named mechanism.**

---

## 1. Matt's hypothesis: RIGHT DIAGNOSIS, FOSSILIZED MECHANISM

**Literal form — "weapons add flat damage to physical hits, not caster hits" — is NO on today's engine.** W-α1 Path α (Matt-ratified 2026-05-28) refactored the physical path off weapon seeding: *"weapon_base_physical_damage is no longer the primary seed; it carries gear affixes (via physical_damage_pct pool)"* (`damage_resolver.py:717-719`). Both paths seed from calibrated constants; both paths' weapon fields are scaffold-0.0 (`combatant.py:246-256`, "until rocket Track D emission wires substrate weapon binding") and neither formula depends on them.

**But the weapon asymmetry was not removed — it was baked into the constants:**

| Constant | Value (all tiers) | Source |
|---|---|---|
| `BASE_PHYSICAL_DAMAGE_L50` | **48,012.6** | `per_skill_emitter.py:139-147` |
| `BASE_SPELL_DAMAGE_L50` | **20,532.2** | `per_skill_emitter.py:106-115` |
| Ratio | **2.3384×** | `:125-126` — *"Physical/magical path ratio preserved from W-α1 calibration: 43703.3 / 18689.4 ≈ 2.3384"* |

The W-α1 physical values ({65800, 98700, 142500, 263100} pre-W-α3, `:119`) were weapon-Path-A-derived. The refactor preserved the ratio through every recalibration since (W-α3 ×0.664063, Phase 3d uniform-across-tiers, Phase 3d RE-RUN T4-aware). **The weapon-era damage advantage lives on inside one flat scalar.**

## 2. Highest-damage skills — SAME skills, both paths; the tables are path-blind

`_DAMAGE_MULTIPLIER`, `_COOLDOWN`, `_CAST_TIME`, `_ENERGY_COST` are keyed **(tier, role) only** (`per_skill_emitter.py:150-194`). A STR primary_attack and an INT primary_attack of equal tier have identical multiplier, cooldown, cast time, cost.

- **Highest per-cast (both paths):** T3 primary_attack — 1.30 mult × 2.17 tier_coeff = 2.82× base, 8s cooldown.
- **Highest sustained contributor (both paths):** T1 primary_attack — 0.80×1.00/2s = 0.40 base/s (vs T2 0.375/s, T3 0.353/s). Control-role skills run 0.40–1.00× on 4/8/14s cooldowns.
- **T4 = passive capstone** (cooldown 0.0), not rotation damage.
- **Damage basis:** `BASE_<path>_L50 × investment_mult × (1 + pct_pool/100) × ECF × tier_coeff` → attribute scaling `1 + attr×0.005` (`math_model.py:14,111-113`) → armor-curve (physical) / resistance-percent (magical). **No weapon term on either path.**
- **No auto-attack channel exists** (grep `auto_attack|basic_attack|filler` across sim = zero) — no hidden martial swing DPS between cooldowns.

**Answer to Matt's second question in one line:** the highest-damage skills are the *same rotation* for both paths; a caster's copy does **43%** of the martial copy's damage per cast, purely from the seed constant.

## 3. Why calibration said "balanced" and the wall says "broken" — the pack channel

- AOE-geometry hits **multiply damage by pack size**: `if defender.pack_proxy_size > 0 and skill.geometry in AOE_GEOMETRIES: dmg *= defender.pack_proxy_size` (`damage_resolver.py:466-468`).
- Phase 3d calibrated per-path medians on **boss_with_adds** — INT 68.18 vs STR 79.44 KPM (`per_skill_emitter.py:93`) — the pack channel compensating the 2.34× seed deficit at whole-encounter level.
- A lone 300k/500k wall sets pack_proxy_size = 0 → **the entire compensation channel zeroes** and the naked seed ratio is exposed. This is the exact mechanism behind the Leg-B localizer: packs 3–4 KPM fine, single-target 1–2 KPM broken, economy-independent.

**Secondary differentials (spike quantifies):** crit applies to both paths (`:461,:491`) but crit_chance is **DEX-keyed** (`math_model.py:158`) → DEX martial crit-rich, INT crit-poor; physical pays an accuracy/dodge tax casters don't (`:444`); elemental pays wall resistance vs martial armor (values on the calibrated mobs TBC).

**Arithmetic sanity:** martial floor 9.90 ÷ 2.3384 ≈ **4.2 KPM caster ceiling** — measured best 1.0. Residual ~4× to be decomposed by the spike: crit EV differential + pilot-cell role/geometry composition + investment_points state (0 → 0.35× floor, symmetric) + wall defense values.

## 4. Design verdict — the constant is too flat

One scalar (2.3384) carries what should be a small **path × geometry-class matrix**. The architecture balanced casters as "AOE trash-clear pays for weak single-target" — the D3-launch Wizard trap (vanilla Inferno: Wizards couldn't kill bosses; fixed via rune-variant single-target skills + crit mass). D2's actual equilibrium — the Sorceress as THE boss-killer — came from per-skill balance, never one global caster discount. PoE treated weak self-cast single-target as a multi-year defect class and fixed it structurally (damage effectiveness, spell-crit channels), never via mana economy — which matches Leg-B's empirical finding that economy cannot govern this layer.

**C2 floor vindicated:** the bar is martial-reachable (batch-1 derived) and caster-unreachable **by construction**. Bar stays; chassis moves. The floor did precisely its job — it caught a construction defect that whole-encounter calibration had been hiding since W-α1.

## 5. Fix directions (ELICITOR forks — Matt rules; sizing gated on the spike ledger)

| # | Shape | Read |
|---|---|---|
| F-a | Global BASE_SPELL raise toward parity | REJECT — over-buffs caster trash-clear (already healthy 3–4 KPM), breaks martial-hits-harder-per-swing flavor |
| F-b | **Geometry-keyed magical single-target premium** — magical path × single_target-class geometry gets a calibrated multiplier (the flat ratio becomes a path×geometry matrix) | **gandalf lean: primary.** Surgical at the exact deficit; preserves D2 equilibrium (Frozen Orb clears, Fireball nukes); leaves pack channel untouched |
| F-c | INT-keyed spell-crit channel (Last Epoch spell-crit model) | Texture candidate beside F-b; closes the crit-EV differential in-fantasy |
| F-d | Move the floor down | REJECT — C2 principle (D2 Sorceress law); the bar is not miscalibrated, the chassis is |

**Guards carried forward:** mana-substrate-only (no Axis-5 back-door — charge-stack/blood-magic stay reserved, empty-by-ruling); recognition→validate→commit (spike ledger BEFORE constants move); any BASE/multiplier change = Discipline #12 semantic shift + re-pilot (~200s class) before Leg C.

## 6. Sharpened spike spec (replaces KR's exploratory framing — now arithmetic verification)

1. **Per-cast ledger reconstruction:** best pilot INT config vs a batch-1 martial reference on the same wall — base × investment × pools × tier × attr × defense × crit-EV must reproduce measured KPM. Validates 2.3384 + residual decomposition.
2. **Pilot-cell composition audit:** roles/geometries actually drawn for `endgame_bc_ranged_medium_variable_int_none` (attack-role vs control-role rotation share).
3. **investment_points state** in pilot emission (0 → 0.35× floor?).
4. **Wall defense values:** armor vs elemental resistance on the calibrated 300k/500k mobs + dmod=0.3 semantics.
5. **Crit-EV differential:** DEX distributions, martial vs INT kits.

Output = multiplier ledger table → F-b/F-c sizing is then arithmetic; re-pilot validates; Leg C fires only after GO on the re-pilot.

## 7. APPENDED same-session — two constraints carried into the fix build (pushed unprompted; Matt invited)

1. **Calibration-target discipline — don't re-fossilize.** The root failure mode was not the 2.3384 value; it was calibrating a flat constant against a **single encounter mix** (boss_with_adds whole-encounter KPM) that let a compensating channel hide a per-cast asymmetry. When F-b sizing fires, the calibration target MUST be the **two-shell floor structure** (open_arena + chokepoint, pack + wall as separate gates — the C2 band shape), never a whole-encounter median. If `unified_calibration_loop.py` still converges on boss_with_adds, the fix build re-targets it before any constant moves. Otherwise we mint a new flat scalar with a new hidden subsidy and meet this HALT again in a different costume.

2. **Size to the martial DISTRIBUTION, not the floor.** 9.90/11.65 is batch-1 martial-derived `bar_lo`. If F-b sizes casters to *just clear* it, the caster band becomes a floor-scraper population while martial kits distribute well above — and Leg C's caster-cell yield collapses far below martial's 38.9% (a yield surprise at 12–15h scale, exactly what the pilot discipline exists to prevent). Sizing target = the martial **median/distribution shape** on the same shells, floor as the gate it already is. The re-pilot's GO criterion should check yield-rate comparability, not bare floor-clearance existence.

---

**Signed:** gandalf, 2026-07-06 (ARCHITECT). The weapon never left — it fossilized into a constant; the wall just removed the crowd it was hiding behind.
