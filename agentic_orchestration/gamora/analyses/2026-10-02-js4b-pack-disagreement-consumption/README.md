# J-S4b pack-disagreement consumption classification (gamora, 2026-10-02)

**Task:** for each of the 8 J-S4b `gd-eor-warlord-referent` vs KC2 pack v3.11 disagreements, determine
whether the V311-FULL oracle (`reincarnated-engine/src/reincarnated/simulation/scripts/
gamora_kc2_play_v3p11_oracle_2026_10_02.py`, `run_one("V311-FULL")` + `v3p8.graded_arm`) actually
**consumes** the disputed value in its arithmetic, or whether the value is read-and-ignored / never
read at all. Read-only: the oracle, the pack and `corpus.db` were not touched. The only counterfactual
run (item 2) monkeypatches `player_sustain.eor_leech_fraction` **in-process** in a scratch script —
no file on disk was edited.

**Method.** For each item I traced the oracle's import graph from `run_one()` down through
`v3p10_oracle` → `v3p9` → `v3p8` → `kc2.run` to find the literal code path (if any) that reads the
disputed quantity, then grepped the whole `simulation/kc2/` package (and `simulation/scripts/`) for
every other call site of that quantity to rule out a side door. Classifications below are CONSUMED
(changes the oracle's arithmetic), INERT (read-and-ignored, or never read), or UNDETERMINED.

## Headline

**7 of 8 items are INERT. Only item 2 is CONSUMED**, and it is CONSUMED in a narrower and stranger way
than the dispute states: the oracle is internally split-brained on "EoR's weapon-damage %" — one
computation path uses the pack's 64% (but that computation's *result* is itself never read further
downstream), and a separate, live-consumed path uses the disputed 57%. Items 1 and 6 (the ones flagged
for particular attention) are both INERT, and for structurally different reasons: item 1's disputed
quantity (a rank number) is never read as a number anywhere in the package; item 6's entire subsystem
(devotion-proc damage) is explicitly unmodelled by the oracle's own design ruling (AC-9.1).

## Table

| # | Item | Pack row | Oracle site (file:line) | Class | Effect | Evidence |
|---|---|---|---|---|---|---|
| 1 | EoR total rank: record 26, pm4g 16, oracle's 20 | `ABS-EOR-RANK-OF-RECORD` (math_rules.json `V1-WD-1`) | `simulation/kc2/fixture.py:191` `EOR_TOTAL_RANK = Cited(26, ...)` | **INERT** | none | `EOR_TOTAL_RANK` is defined once and never referenced again anywhere in `simulation/kc2/*.py` or `simulation/scripts/*.py` (`grep -rn "EOR_TOTAL_RANK"` returns only its own definition line). No code multiplies, indexes, or branches on any "EoR rank" integer at runtime. The 26/20/16 disagreement surfaces only through which *already-baked, rank-labelled* constant a human curator cited for a different quantity (weapon-damage %, item 2) and a different file (`player_kit.json` `fixture.eor_rank_total`, also a non-consumed descriptive field — `grep` for it outside JSON returns nothing). Reasoned, not measured (no live input to vary). |
| 2 | EoR weapon damage: 64% (pack `channel.weapon_damage_pct`) vs oracle's 57% (`V1-WD-1`) | `V1-WD-1` HONEST-FAIL — `pack_carries.pct=64.0` (rank 26) vs `oracle_reads.pct=57.0` (rank 20) | **Two sites, two answers:** (a) `simulation/kc2/channel.py:120-131` `compose_damage_basis()` composes `weapon_pct = WEAPON_DAMAGE_PCT_BASE(50.0) + GUTSMASHER(14.0) + WARBORN(0.0) = 64.0` into `DamageBasis.weapon_damage_pct` — **but `grep -rn "\.weapon_damage_pct\b" simulation/kc2/*.py` has zero hits outside its own definition: this field is computed and never read again.** The live per-tick damage (`run.py:1271-1280`, `per_tick_damage = (basis.flat_physical_min + basis.flat_physical_max)/2.0`) uses only the flat physical band, not `weapon_damage_pct`. (b) `simulation/kc2/player_sustain.py:314-319` `eor_leech_fraction()` reads **0.57** from `pm4p_attack_kit.csv` by record match (not from any rank field) and `player_sustain.py:630` (`PlayerSustainFold.__post_init__`: `self._leech_fraction = eor_leech_fraction()`) feeds it into `self._weapon_raw = leech_fraction * weapon_limb.d_weapon` (`player_sustain.py:631`), the life-leech sustain term. | **CONSUMED** (via the leech path only; the 64%/"primary damage" path is a dead field) | Measured, 5 salts (`V311-FULL`, OBS-1 guard `complete=True`, no truncation, both arms): monkeypatching `eor_leech_fraction()` to return the pack's 0.64 instead of the oracle's 0.57 (a +12.3% relative change in the leech term) moves `ratio_vs_referent` **1.0923 → 1.0951 (Δ +0.0028, ≈ +0.26% relative)**, same direction as expected (more leech % → more self-heal → marginally better survival margin). `leg_b_deaths_per_salt` (0.2 → 0.2) and `leg_a_terminals` (same salt reaches w160 in both arms) are **unchanged** — no terminal outcome flips at n=5. Small, real, correctly-signed. | `simulation/kc2/player_sustain.py:272-336`; counterfactual script `js4b_item2_counterfactual.py` (scratchpad, not committed) |
| 3 | Vire's Might cooldown: 3.6 s vs pack `X1-2` 3.1 | `per_cast_energy.py` `BOUND_SKILLS["viremight"]` (the X1-2 row) | `simulation/kc2/per_cast_energy.py:179-184` defines `cooldown_s=Cited(3.1, ...)` for this exact skill, but `simulation/kc2/run.py:49` imports only `refuses_activation` from `per_cast_energy`, keyed to the EoR channel's own per-tick cost (`energy.py:59`, `SKILL_MANA_COST_R26`) — never to `BOUND_SKILLS["viremight"].cooldown_s`. More directly: `run.py:5367-5368` states outright **"Vire's Might cadence — NOT modelled; the sim swings one channel"** (the EoR disc is the only channel the sim advances per tick). | **INERT** | none | `run.py:5350-5369` (`piloting_parameters` disclosure block); repo-wide `grep` for `cost_table(\|charge_for(\|BOUND_SKILLS` outside `per_cast_energy.py` finds only two now-separate analysis scripts (`gamora_kc2_play_c2_energy_fold_and_nine_relift_2026_09_28.py`, `gamora_kc2_c7_insufficient_energy_rows_2026_09_29.py`), neither in the `run_one("V311-FULL")` call chain. |
| 4 | War Cry radius at r16: 16.8 m vs `V13-WARCRY-1` 16.0 (r12) | `V13-WARCRY-1` `skill_target_radius_m: 16.0` | `simulation/kc2/counterplay.py:448` `warcry_reduction_pct=_magnitude(wc, "offensiveTotalDamageReductionPercentMin")`; consumed at `counterplay.py:649` (buff event) and `counterplay.py:746` `cut = dmg * self.kit.warcry_reduction_pct / 100.0` | **INERT** | none | War Cry is modelled purely as a **self-targeted flat incoming-damage reduction** (a player buff with a magnitude and a cooldown/duration), not as a radius-gated AoE debuff on enemies. `grep -n "radius" simulation/kc2/counterplay.py` finds zero occurrences of `skill_target_radius_m` or any spatial gate on the War Cry effect — only `warcry_reduction_pct` (the %) and `warcry_cd_s`/`warcry_duration_s` (timing) are fields on `Kit`. |
| 5 | Modifier mana costs: Blindside 5 vs `X1-0` 6; Tectonic Shift 3 vs `X1-2` 5; Break Morale 50 vs `X1-4` 68 | `per_cast_energy.py` `BOUND_SKILLS` rows `blindside` / `tectonic_shift` / `break_morale` | `simulation/kc2/per_cast_energy.py:167-209` defines `modifier_cost=Cited(6.0, ...)` (Blindside, X1-0), `Cited(5.0, ...)` (Tectonic Shift, X1-2), `Cited(68.0, ...)` (Break Morale, X1-4) — i.e. the oracle's own module already carries exactly the pack's X1-* values, not the disputed record values. But as in item 3, `run.py` only consumes `refuses_activation` against the EoR channel's own per-tick cost; the modifier-cost table (`charge_for`, `cost_table`, `BOUND_SKILLS`) has no caller inside `run.py`'s live tick loop. | **INERT** | none | Same evidence as item 3 (`run.py:49,2316`; repo-wide caller grep). Worth flagging separately from item 3: the oracle's *source data* for these three numbers already agrees with the pack row, not with the disputed record value — so even if this table were wired in, there would be no discrepancy to resolve here. |
| 6 | Celestial power levels: record 25/25/20/20/20/20/15 vs every `DP-*` pack row = 0 | `player_kit.json` `devotion_procs[].value.devotion_level` (all "0") | `simulation/kc2/devotion.py` (whole module) | **INERT** | none | `devotion.py`'s own design ruling, stated in its module docstring (lines 1-19): **"No proc mechanism is built this lap" (R-KC2-1(d))** and **AC-9.1: "the sim emits NO proc damage events. A non-zero proc-damage total is a spec violation, not a bonus."** `DevotionPower` (the dataclass backing `SEVEN_POWERS`, `devotion.py:27-83`) has **no level/rank field at all** — magnitude is a fixed descriptive `envelope` string per power ("DB-max rank, save-measured" per the module's own `ENVELOPE_DISCLOSURE`), not level-scaled. Separately, `devotion_level` is read only as a passthrough display field in `mech_lift.py:810-811,908` (JSON-in, JSON-out) and is never consulted by any arithmetic. **Answer to the task's specific question: no celestial power's effect in the oracle depends on the `DP-*` level field, because no celestial power produces a modelled effect in the oracle at all** — the whole category is a disclosed, out-of-model envelope. |
| 7 | Vire's Might engine class: `Skill_AttackPathCharge` (game data) vs `Skill_AttackWeaponCharge` (binding_model) | `player_kit.json` `skills[].dbr_class_pm4g` | n/a — never read | **INERT** | none | `grep -rn "dbr_class_pm4g\|dbr_class\b" simulation/kc2/*.py simulation/scripts/*.py` (excluding `.json` matches) returns **zero hits**: the field is never read as a Python variable/key anywhere in the package. The movement model's dash cycle (`movement.py:94-113`, `DASH_CYCLE`) does include Vire's Might at a measured 12.0 m / 3.6 s displacement (and separately omits Blitz, whose own `Skill_AttackWeaponCharge` record lacks a decodable range field per Lap-G) — but that inclusion is driven by an independently-cited, camera-measured displacement constant for Vire's Might specifically, not by a live read of its `dbr_class` label. Reasoned: even under the disputed relabelling this measured constant would not change unless Vire's Might's own record were re-examined for a range field, which is outside this item's dispute. |
| 8 | Gutsmasher conversion: 50/50 (game data) vs 55/46 (tooltip) | `other_conversions` (Chaos→Physical, Lightning→Physical) | n/a — never read | **INERT** | none | `fixture.py`'s only Gutsmasher-sourced constant actually used downstream is `WEAPON_DAMAGE_PCT_GUTSMASHER = Cited(14.0, ...)` (`fixture.py:202`, a flat weapon-damage-% contribution, itself part of the dead `weapon_damage_pct` field per item 2) and `FIRE_TO_PHYSICAL_CONVERSION_PCT = Cited(100.0, ...)` (`fixture.py:216-217`), which is **Eye of Reckoning's own** Fire→Physical conversion, not Gutsmasher's separate Chaos→Physical / Lightning→Physical split. No constant for a 50%, 55%, or 46% chaos/lightning conversion fraction exists anywhere in `fixture.py` or `channel.py`; `grep -n "CHAOS\|LIGHTNING" fixture.py channel.py` surfaces only `SOULFIRE_LIGHTNING_MIN` (a flat, already-lightning magnitude explicitly noted as **not** converted by Gutsmasher: `"⚑ LIGHTNING, DESPITE THE NAME. Gutsmasher converts Fire→Physical ONLY"`, `fixture.py:250-251`). The disputed 50/50-vs-55/46 split belongs to a quantity the oracle does not model at all. |

## Flags for the conductor

- **Item 2's split-brain is the one finding worth carrying forward**, independent of this item's
  own small measured effect. `compose_damage_basis()` computes a `weapon_damage_pct` field that
  is dead code downstream (never read past its own dataclass) — `run.py`'s actual player-damage
  term is the flat-physical-band average, not weapon-damage-% scaled at all, and the one place
  weapon-damage-% *is* live (the leech fraction) draws from a different source (CSV, rank 20) than
  the one `compose_damage_basis()` computes (constants, rank 26). This is a pre-existing structural
  oddity in the oracle (visible in its own `V1-WD-1` HONEST-FAIL note), not something introduced by
  J-S4b — I am not proposing a fix, per scope (oracle is FROZEN, Matt Q102).
- **Items 3 and 5 both land on the same underlying fact**: Vire's Might is explicitly and
  deliberately not simulated as an active skill in `run_one("V311-FULL")` ("the sim swings one
  channel"). Every dispute item that hangs off Vire's Might's or its modifiers' *energy economy*
  (cooldown, modifier mana costs) is therefore inert by construction, not by coincidence — this is
  one finding reported twice in the table, not two independent inert items.
- **Item 6 generalizes**: since no celestial/devotion proc produces a modelled effect in the oracle
  (AC-9.1, stated as a spec ruling, not a gap), any future REFERENT-v2 dispute item about devotion
  proc magnitudes, levels, or ICDs for this fixture will land INERT for the same structural reason.
  Flagging so it isn't re-litigated item-by-item next time.
- No REFERENT-v2 items filed and the v3.11 freeze is not reopened here, per scope.

## Commit

Committed alone:
`git -C /Users/admin/Games/reincarnated-collaboration commit --only agentic_orchestration/gamora/analyses/2026-10-02-js4b-pack-disagreement-consumption/README.md`
Not pushed.
