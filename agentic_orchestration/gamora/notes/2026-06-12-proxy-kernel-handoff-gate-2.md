# Proxy-kernel handoff — Gate-2 handoff (Session 2, Items 1–5)

**Author:** gamora
**Date:** 2026-06-12
**Gate:** Gate-2 (DEV-MODE) — routed to jack-ryan
**Dispatch:** `agentic_orchestration/dispatches/2026-06-12-gamora-proxy-kernel-handoff.md`
**Spec:** `gandalf/notes/2026-06-12-session-2-proxy-companion-architecture-spec.md` § 3 (ratified, three riders)
**Math note:** `reincarnated-engine/src/reincarnated/simulation/math/proxy-kernel-extension-2026-06-12.md` (§0–§8, §10–§11)
**MIGRATION:** `simulation/MIGRATION.md` v1.66
**Engine commits:** `3102363` (Items 1+2), `dae0349` (Item 4), `e00cb6d` (Item 3)

---

## Top-line

All five dispatch items complete and empirically validated. **Brownfield guarantee held at every gate:
golden-master self-verify 0/60 cells moved** after Items 1+2, after Item 4, and after Item 3. Three smoke
harnesses green (16/16 + 8/8 + 15/15). No kernel file edited for Item 3 (caller-side). No star-lord schema
change required (proxy FightResult fields are internal-to-seam; export surfacing is a separate dispatch).

| Item | Status | Gate evidence |
|---|---|---|
| 1. ProxyCombatant entity model | ✓ complete | proxy smoke 16/16; 14/14 type instantiation; fail-loud on unknown type |
| 2. simulate_fight extension | ✓ complete | golden-master 0/60 on `proxies_a=None, proxies_b=None`; FightResult additions default-neutral |
| 3. Companion modifier vector (caller-side) | ✓ complete | companion smoke 15/15; no kernel edit; golden-master 0/60 |
| 4. Charge-stack energy type (kernel-change-protocol) | ✓ complete | charge-stack smoke 8/8; golden-master 0/60 (§6.6 confirmed) |
| 5. Terrain-reactive assessment | ✓ delivered | 1-page note; Session-3 recommendation (caller-side `terrain_type`) |

---

## Item 1 — ProxyCombatant entity model

**New files:** `simulation/proxy_combatant.py` — `PROXY_TYPE_TIER` (14-type→tier), `FissionLineage`
(lineage cap = 4 TOTAL entities), `ProxyCombatant`, `entity_from_proxy_dict` (fail-loud),
`spawn_fission_subproxy` (0.60 fraction, 30 s expiry), + supporting types.

**fight_engine.py modification sites (Disc #1.2):** `_ProxyTelemetry`:1088; `_proxy_owner_dps`:1117;
`_handle_proxy_death`:1144; `_proxy_bodyguard_intercept`:1169; `_dispatch_proxies`:1192; proxy setup
guard `_has_proxies`:209; tick-loop intercept-capture + dispatch calls ~:295-320.

**Three behavioral tiers:** minimal (no HP/position; support-only), mid (position+targeting; no rotation),
full (skill rotation + cooldowns). PROXY_FISSION is the sole sanctioned proxies-of-proxies exception
(lineage cap 4 TOTAL, not depth; 30 s expiry).

## Item 2 — simulate_fight extension + golden-master self-verify

**Signature (symmetric, keyword-only, both default None):**
```python
def simulate_fight(combatant_a, combatant_b, *,
                   proxies_a: list[ProxyCombatant] | None = None,
                   proxies_b: list[ProxyCombatant] | None = None, ...) -> FightResult
```
**Golden-master self-verify output:** `[VERIFY] 0/60 cells MOVED vs oracle` — the
`proxies_a=None, proxies_b=None` path is bit-identical to the pre-extension baseline. ✓ (brownfield contract met).

**FightResult additions (additive, default-neutral):** `proxy_damage_contributed=0.0`,
`proxy_damage_by_type={}`, `proxy_death_events=[]`, `proxy_resource_generated=0.0`,
`proxy_damage_a/proxy_damage_b=0.0`, property `a_proxy_contribution_pct`.

**Proxy damage basis (math note §1.1; Discipline #11 correction):** first impl used a per-action D_ref on
a 1 s cadence → smoke measured contribution 0.185 vs predicted ~0.55. Re-anchored to **owner DPS basis**
(`owner.damage_dealt / max(TICK_SIZE, elapsed)`; per-attack `= dm × owner_DPS × attack_interval_s`; cadence
cancels) → re-measured 0.556. Math note updated BEFORE re-run (math-before-code preserved).

## Item 2/Item 1 — Proxy smoke results (16/16; `scripts/gamora_proxy_kernel_smoke_2026_06_12.py`)
- Brownfield None/None == default; all proxy fields default ✓
- 14/14 proxy types instantiate; unknown type fails loud (ValueError) ✓
- Tier behavior: minimal survive full fight; mid deal nonzero tracked dmg (24,919); full exercise 2 distinct skills ✓
- **proxy_contribution_pct reachability: 0.556 ≥ 0.45 gate** ✓ (rider 3 + proxy-primary §5 ~0.5 reachability metric surfaced in smoke telemetry). *Synthetic stacked composition proving the seat is mechanically reachable; whether realistic generatable PROXY magnitudes reach it is rocket's measurement, not asserted here.*
- PROXY_FISSION: 2 sub-proxies at 0.60±0.02, expiry set, lineage cap 4 ✓
- Bodyguard intercept: >20%-max-HP hit intercepted, owner HP preserved; sub-threshold NOT intercepted ✓

## Item 3 — Companion modifier vector (cap-check + WR-delta)
**Caller-side, balance_loop.py ONLY — no kernel edit.** Smoke 15/15 (`scripts/gamora_companion_modifier_smoke_2026_06_12.py`):
- **Cap-check output:** NPC over-cap clamped+flagged (damage_amp 1.20→1.15, survivability 0.20→0.10,
  resource 0.20→0.10); monster cap column differs (survivability→**0.0**, resource→0.05, damage_amp→1.10). ✓
- Field application: damage_amp→`damage_modifier ×1.15`; survivability→`hp/max_hp ×1.10`; resource→`mana_regen ×1.10`. ✓
- Real CC duration scaling (water/seed=3 root effect): cc_duration_mult=1.25 → 2.3→2.875; deepcopy isolation
  (rebuilt kit reads unscaled 2.3). ✓
- aoe_radius_mod 1D no-op (recorded, zero state change). ✓
- **WR-delta measurement guard:** Δ>0.10 → `warn=True` (logged WARN, never silent); Δ=exactly 0.10 → False (strict `>`). ✓
- Golden-master 0/60 (no kernel edit confirmed). ✓

## Item 4 — Charge-stack energy type (kernel-change-protocol)
**Golden-master delta: 0/60** (§6.6 prediction confirmed — every branch dead code for mana-only corpus).
Charge-stack smoke 8/8 (`scripts/gamora_charge_stack_smoke_2026_06_12.py`): on-hit accumulation +1/clamp10/no-zero-gain;
passive held bonus ratio **exactly 1.5 = 1+10×0.05**; spend-all burst ratio **exactly 6.0 = 1+10×0.5**;
§6.5 DEFENSIVE_TRADEOFF positive mana-test gate. **Semantic note (Disc #12):** §6.1+§6.2 ordering —
spend-all zeroes the pool before resolve, the landing hit re-accrues +1 (post-cast pool = 1.0, not 0).

## Item 5 — Terrain-reactive geometry assessment
Note at `gamora/notes/2026-06-12-terrain-reactive-geometry-assessment.md`. Greenfield confirmed (only
`ChokeZone` arena.py:104, movement-only). Recommendation: position-independent `terrain_type` kwarg
(caller-side, brownfield-safe, reuses Item 3/Item 4 caller-supplied-magnitude idiom) as Session-3 v1;
defer steppable terrain to a 2D `TerrainZone` built on a generalized AABB membership primitive.

---

## Vestigial-ontology charge compliance
- New surface names — `proxy_type`, `behavioral_tier`, `damage_multiplier`, `accumulation_state`,
  `per_stack_passive_bonus`, `charge_burst_per_stack`, `terrain_type`, companion-modifier keys — are
  **substrate-truthful / behavioral-descriptor** vocabulary. No legacy ontology-named field introduced.
- **One new `energy_type` value** ("charge-stack") added to the kernel vocabulary — a Q2=PHYSICAL
  behavioral descriptor per the register; no register update required, no new ontology vocabulary.
- No new **required** kernel-schema field: proxy FightResult fields default; charge-stack kit-data fields
  default 0.0; companion vector is caller-side. Brownfield-safe by construction.

## MIGRATION.md version bump
`simulation/MIGRATION.md` **v1.66** authored (newest-at-top). star-lord telemetry NOT affected by a schema
change (proxy fields internal-to-seam; export surfacing deferred to a separate dispatch).

---

## Design-latitude calls recorded (Matt-granted latitude on HOW, not WHAT)

1. **Proxy dispatch as side-effect** to the a↔b tick loop (not structural modification) — per dispatch
   "minimal coupling preferred." Proxies act after the acting side, before enemy response.
2. **Proxy damage basis = owner DPS** (not per-action D_ref) — forced by the §1.1 empirical correction;
   the identity `proxy_total/owner_total = dm` only holds on the DPS basis. Math-note-anchored.
3. **Charge-stack §6.1+§6.2 ordering** (spend-all → resolve → re-accrue +1) — post-cast pool = 1.0 not 0;
   surfaced by smoke, judged intended (the next charge begins on the spending hit). Flagged as a semantic
   detail for the decisions-log (Disc #12).
4. **Item 3 CC composition:** the two multiplicative CC levers (cc_duration_mult, enemy_cc_mult) compose
   **multiplicatively** onto the single realized CC-duration scale (same kernel quantity); all six modifier
   TYPES otherwise independent (no cross-type compounding per §7).
5. **Item 3 CC application via control-effect `duration_seconds` scaling** on deepcopied player skills — the
   kernel's only multiplicative CC surface (the existing `control_duration_bonus` hook is additive-seconds).
   DoT ailments excluded so cc_duration_mult never doubles as a damage lever.
6. **Item 3 not yet wired to a live COMPANION_CONTRACT/MONSTER_PACT pairing** — companion-record source is
   rocket-pending (no companion data in Season 001010). Mechanism + acceptance shipped; live wiring is a
   follow-on once rocket emits companion records.
7. **Item 5 v1 recommendation = caller-side `terrain_type`** (position-independent) over a steppable 2D zone —
   cheapest brownfield-safe surface; steppable terrain deferred unless a design requirement demands it.

## Routes requested of jack-ryan
- **Decisions-log entry** for the Item 4 charge-stack semantic ordering (Disc #12) and the new `energy_type`
  value addition.
- **Gate-2 review** of the three smoke harnesses + golden-master evidence against the ratified §3 interface
  and the three riders (proxy-stacked smoke population; proxy_contribution_pct surfaced; locked BC vocabulary).
- Confirm the latitude calls above sit within Matt-granted HOW-latitude (not WHAT-latitude).
