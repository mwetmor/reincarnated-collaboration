# Dispatch — 2026-07-06 — gamora — caster single-target per-cast ledger spike (§6)

**From:** knight-rider
**To:** gamora (lead; rocket adjacency ONLY if an emission-side value is unreadable from on-disk artifacts)
**Approved by:** Matt 2026-07-06 ("run spike per §6 … Output: multiplier ledger that reproduces measured 1.0 KPM from constants")
**Estimated effort:** ~2–4h — ANALYSIS ONLY, no code, no fire, no re-emit
**Acceptance:** a per-cast multiplier ledger that reproduces the measured **1.0 KPM** (open_arena, best pilot INT config) from named constants end-to-end, decomposing the ~4× residual beyond the 2.3384 seed ratio.

## Context

Leg-B HALT resolved toward world (1) — caster chassis under-built — with a named mechanism (gandalf finding, below). The weapon-era damage advantage fossilized into `BASE_PHYSICAL_DAMAGE_L50=48,012.6` vs `BASE_SPELL_DAMAGE_L50=20,532.2` (ratio **2.3384×**, `per_skill_emitter.py:125-126,139-147,106-115`). The AOE-pack channel (`damage_resolver.py:466-468`, `dmg *= pack_proxy_size`) compensated the seed deficit at Phase-3d whole-encounter calibration; a lone 300k/500k wall sets `pack_proxy_size=0`, zeroes the compensation, and exposes the naked ratio. Arithmetic sanity: `9.90 ÷ 2.3384 ≈ 4.2 KPM` caster ceiling, but measured best = **1.0** — a **~4× residual** to decompose. This spike turns fix-sizing (gandalf F-b/F-c) into arithmetic.

## Required reading before starting (§6 is the AUTHORITATIVE spec — do not re-derive it)
- `agentic_orchestration/gandalf/notes/2026-07-06-caster-single-target-structural-finding.md` — **§6 is your spec**; §1–§4 are the mechanism + arithmetic you're verifying; §3/§5 name the secondary differentials.
- `reincarnated-engine/src/reincarnated/output/economy_pilot/economy_pilot_measurement_report.json` — the pilot artifacts (best INT config's emitted skills, investment_points, pools, per-cohort results). Run `617409b8…`.
- `simulation/notes/legB-economy-pilot-read-2026-07-06.md` — your own Leg-B read (the 1.0/2.1 landscape, the localizer).
- `per_skill_emitter.py` (seed constants, `_DAMAGE_MULTIPLIER`/`_COOLDOWN`/`_CAST_TIME` tables), `damage_resolver.py` (crit `:461,:491`, AOE-pack `:466-468`, accuracy/dodge `:444`), `math_model.py` (attr scaling `:14,111-113`, crit_chance DEX-keyed `:158`), `combatant.py` (weapon scaffold `:246-256`).
- A batch-1 martial reference kit on the same wall (the comparison leg).

## Scope (§6, verbatim — all ANALYSIS, all READ)
- [ ] **1. Per-cast ledger reconstruction:** best pilot INT config vs a batch-1 martial reference on the SAME wall — `base × investment × pools × tier × attr × defense × crit-EV` must reproduce measured KPM for BOTH. Validate the 2.3384 seed ratio + decompose the ~4× residual into named factors.
- [ ] **2. Pilot-cell composition audit:** the roles/geometries actually drawn for `endgame_bc_ranged_medium_variable_int_none` — attack-role vs control-role rotation share (does the pilot cell rotate mostly non-single-target-optimal skills?).
- [ ] **3. investment_points state** in pilot emission (0 → 0.35× floor? is the pilot caster under-invested vs the martial reference?).
- [ ] **4. Wall defense values:** armor (physical) vs elemental resistance (magical) on the calibrated 300k/500k mobs + `dmod=0.3` semantics — is the caster paying a resistance tax the martial reference isn't?
- [ ] **5. Crit-EV differential:** DEX distributions martial vs INT kits → crit_chance/crit-EV gap (`math_model.py:158`).
- [ ] **Output = a multiplier ledger table** that reproduces 1.0 KPM from constants, with each residual factor sized. This makes F-b (geometry-keyed magical single-target premium) / F-c (INT spell-crit channel) sizing arithmetic rather than guesswork.

## Cross-seam contract change? (Principle 6 gate)
**NO — analysis + report only.** No schema, fixture, emit-shape, or code touched. Reading across seams (per_skill_emitter is rocket's) is fine for analysis; only writes are seam-gated. `Round-trip: not applicable — no contract change; diagnostic ledger reconstruction from on-disk artifacts + engine constants.`

## Out of scope (explicit non-goals)
- **NO constant changes.** Do NOT touch `BASE_SPELL_DAMAGE_L50` or any multiplier — gandalf's guard: recognition→validate→commit, the **ledger comes BEFORE constants move**. Sizing the fix is arithmetic output; APPLYING it is a separate Matt-ruled dispatch.
- **NO re-emit, NO re-fire, NO re-pilot** — this spike reads the existing pilot artifacts.
- **NO fix recommendation beyond sizing** — F-b/F-c selection is Matt's ELICITOR call; you supply the arithmetic, not the verdict.
- **NO Axis-5 back-door** — mana-substrate-only; charge-stack/blood-magic stay reserved-empty (Matt ruling 2026-07-06).

## Open questions for you to resolve (document your answers)
- Does the ledger CLOSE (reproduce 1.0 within tolerance from named constants), or is there an unexplained residual? An unclosed ledger is itself a finding — flag it.
- Is the dominant residual factor the seed ratio (2.34×), the composition (wrong skills rotated), investment state, the resistance tax, or crit-EV? Rank them — this determines whether F-b alone suffices or F-b+F-c is needed.

## References
- gandalf finding `2026-07-06-caster-single-target-structural-finding.md` §6 (authoritative spec)
- Leg-B read `6c5303b`; pilot report `economy-pilot-v1`; run-state `batch2-run-state-2026-07-06.md`
- Discipline #1 (math-before-code), #11 (attribution — every ledger line cites file:line/artifact), #12 (any later constant move = semantic shift + re-pilot)

---

## Completion record

**Completed:** 2026-07-06 by gamora. **Ledger:** `reincarnated-engine/src/reincarnated/simulation/notes/caster-single-target-ledger-spike-2026-07-06.md`

**Ledger CLOSES? NO — flagged as an unclosed-ledger finding.** The idealized per-cast throughput
reconstructed from named engine constants exceeds the measured 1.0 KPM by **~3–6×**. The residual
beyond the seed ratio is **spatial/geometry, not damage-arithmetic**, and is **path-symmetric**
(a martial single_target kit eats the same de-rating) — so it is not a caster-specific damage defect.

**Two named factors flip the naive framing:**
1. **Seed ratio is net-cancelled by pools.** 2.3384× verified exact (`per_skill_emitter.py:125-126`),
   BUT the INT caster's scaffold weapon carries `spell_damage_modifier=90%` (1.90×,
   `substrate_weapon_binding.py:76`) vs the martial's `physical_damage_pct=5%` (1.05×). Pool ratio
   1.81× ≈ cancels the 2.34× seed. **Net per-cast the caster is within ~1.07× of the martial** (even
   ahead post-mitigation once the martial's 15% dodge-gate tax, `damage_resolver.py:444`, is counted).
2. **Dominant throttle = single_target geometry + composition.** All emitted skills are
   `single_target` (`per_skill_emitter.py:585`, `bc_amplitude="variable"`→default) → pack-multiply
   channel (`damage_resolver.py:466-468`) never fires → one cast, one mob against the dispersed
   8×300k wall. Pilot also drew `support_specialist` (least-damage template; 5/9 attack slots).

**Ranked residuals:** (1) spatial single_target de-rating ~3–6× [path-symmetric]; (2) composition
~1.4–1.6×; (3) seed ratio 2.34× raw / **~1.07× net of pools**; crit-EV ≤1.029× (negligible);
resistance tax **0 — armor & resist symmetric** on both walls (`combatant.py:1111`, driver
`:258-268`); investment **not** a residual (max-profile 1.0×, symmetric, `spatial_engine.py:3048`).

**Sized fix:** **F-b alone suffices** for the arithmetic layer (F-c/crit recovers <3% — texture, not
required). BUT F-b must be sized to the **pool-adjusted** seed ratio, NOT the naked 2.34× or nominal
4×: with scaffold pools that = 2.3384/1.81 ≈ **~1.3×**. Sizing to the naked ratio would over-buff.
The rank-1 spatial/geometry residual is a separate structural lever outside F-b/F-c.

**Provenance flag:** the 9.90 bar exceeds the 8-mob cap (`spatial_engine.py:2527`, no respawn), so it
was NOT measured on the same 8×300k wall as the caster's 1.0 — part of the nominal "4× residual" is a
units mismatch. F-b MUST calibrate caster-vs-martial on the IDENTICAL wall, never against 9.90.

**One unread input:** the 90% spell_pool is the scaffold default; the pilot's DB binding may differ.
Reading the exact production pool requires a re-emit (out of spike scope). Ledger brackets both
(spell_pool 0 → 3.13 idealized kills; 90 → 5.95); either way the residual is spatial, not the seed.

**Discipline:** #1 (math-before-code — no constant moved, no code touched), #11 (every ledger line
cites file:line/artifact). Read-only. No re-emit/re-fire/re-pilot/constant-change/Axis-5. Auto-commit,
no push.
