# Finding — 2026-05-15 — B10.4: Option 2 verdict + AOE philosophy investigation

**Reviewer:** jack-ryan
**Severity:** BLOCK (Q3 finding) + WARN (Q2 flag) + INFO (Q1 flags)
**Target:** `v1.3-b10-4-swarm-calibration` (pending tag — held per gamora AGENT_STATE)
**Developer:** gamora (balance loop); rocket (skill generation)
**Principles applied:** Principle 1 (math-before-code), Principle 4 (decisions-log as source of truth), Discipline #1, #12

---

## Q1 — Is Option 2 the right call?

**Verdict: PASS WITH FLAGS**

Option 2 (converge on non-pack WR only; pack fights as diagnostic surface) is semantically sound and is the correct architectural path. The floor-math in the briefing is validated by gamora's empirical finding: 8/10 classes fail convergence because the aggregate WR floor sits at 55-70% when pack fights win ~100%. The binary search cannot reach a 50% target from inside that floor — this is not a calibration artifact, it is a structural consequence of the gauntlet composition.

**Why Option 2 is better than Option 1:**

Option 1 (shift target to 75%) degrades the semantic value of `damage_modifier`. The modifier currently has a clean definition: "value at which the class wins 50% of canonical encounters." Under Option 1, the modifier becomes a composite of "win 50% of real encounters PLUS enjoy pack dominance for free," calibrated against a moving target that depends on AOE kit shape. Modifier semantics drift as pack composition changes; the number becomes harder to reason about across season regen cycles. Discipline #12 (semantic-shifting must be named and framed explicitly) applies: Option 1 would shift modifier semantics without a corresponding decisions-log update, violating the naming contract.

**Flags on Option 2 (not blockers for the option itself):**

- **Pack fight telemetry must remain in the fight log.** The current B10.2 implementation runs pack fights and emits telemetry. Option 2 must preserve this behavior — pack fights serve as the AOE-differential diagnostic surface. If the implementation excludes pack fights from simulation entirely, the diagnostic value is lost. Gamora's description ("pack fights still simulate and emit telemetry but don't contribute to binary-search target") is correct. Verify the implementation matches this description before tagging.

- **Convergence target semantics need a decisions-log entry.** "Non-pack WR = 50%" is a new calibration definition. This must be committed to the decisions-log as an active entry — not just left as a code comment. It is load-bearing for anyone running balance analysis against future seasons.

- **A third path worth noting (not blocking):** Dynamic-target convergence (adjust target WR as a function of pack-slot count in the gauntlet) is architecturally feasible and would allow both pack and non-pack fights to contribute to convergence without semantic dilution. However, this requires more math work (how does target WR scale with pack fraction?) and is not needed for B10.4 resolution. File as a B10 V3 candidate, not a requirement here.

---

## Q2 — Does the B10.2 Two-Gauntlet Pattern revision read coherently?

**Verdict: WARN — real architectural revision to a locked decision; needs explicit supersession**

The B10.2 decisions-log entry (2026-05-14) reads:

> "Recompose = proxy-free 1v1. Convergence = full fidelity."

Under Option 2, convergence also becomes proxy-free (or rather, proxy-excluded from the binary search target). The distinction the B10.2 entry was encoding — recompose uses a clean 1v1 signal, convergence uses full fidelity including packs — collapses. Both loops now operate against the non-pack signal for their respective purposes.

The B10.2 entry's "general principle" language is also affected:

> "Any future proxy entity that modifies encounter shape requires the same treatment."

Under Option 2, the "treatment" changes: future proxy entities would be excluded from convergence targeting, not just from recompose evaluation. The principle remains directionally correct but the specific framing ("Convergence = full fidelity") is directly contradicted.

**Required action:** Before Option 2 goes in, the B10.2 Two-Gauntlet Pattern entry should be superseded with an updated entry that:
1. States the revised pattern: "Recompose = proxy-free 1v1. Convergence = non-proxy fights only (proxy fights are diagnostic surface, not convergence target)."
2. Notes what changed from B10.2 and why.
3. Updates the general-principle clause for future proxy entity treatment.

This is a WARN not a BLOCK because the B10.2 entry is less than 24 hours old and was locked on empirical grounds that the full-regen immediately falsified. The spirit of the entry (keep proxy inflation out of calibration loops) is preserved by Option 2 — the letter just needs updating.

---

## Q3 — Which AOE balance philosophy is operative in rocket's skill generation?

**Verdict: View A is operative. This is the BLOCK finding.**

### What the code does

**Step 1 — Role-level damage multiplier (math_model.py:47)**

```
"area_damage": 0.6
"burst_damage": 1.0
"primary_attack": 0.25
```

AOE-role (`area_damage`) skills emit 0.6× base magnitude versus burst_damage's 1.0×. On this axis alone, AOE skills deal less single-cast damage than single-target burst skills. This looks like View B.

**Step 2 — Energy cost range (role_constraints.py)**

```
area_damage:  energy_cost_range=(15.0, 30.0)
burst_damage: energy_cost_range=(20.0, 40.0)
```

AOE skills actually cost LESS than burst damage skills on average. Burst_damage costs 20-40% of max mana; area_damage costs 15-30%. This is not View B or C behavior — AOE skills are cheaper than single-target burst.

**Step 3 — Cooldown range (role_constraints.py)**

```
area_damage:  cooldown_range=(3.0, 8.0)
burst_damage: cooldown_range=(4.0, 10.0)
```

AOE cooldowns are shorter or equal to burst cooldowns. Again, no cost penalty for AOE coverage.

**Step 4 — Empirical telemetry (telemetry.db, all class abilities, latest seasons)**

Aggregate by AOE_GEOMETRIES (as defined in b6_archetype_templates.py) vs non-AOE:
- AOE geometries: avg energy_cost_pct = 22.43, avg cooldown = 7.67s
- Non-AOE (single_target): avg energy_cost_pct = 18.53, avg cooldown = 8.20s

AOE skills cost 21% MORE energy than single_target but have SHORTER cooldowns (7.67s vs 8.20s). The cost differential is real but small; the cooldown differential favors AOE. The net throughput effect: AOE classes cast slightly less frequently per energy pool but recover faster per cooldown.

Breaking down area_damage role specifically: energy_cost avg = 21.5, cooldown avg = 5.52s. Burst_damage (single-target dominant): energy_cost avg = 28.56, cooldown avg = 7.04s. So within the damage role family, area_damage is cheaper AND faster to recast than burst_damage while carrying the 0.6× per-hit magnitude.

**Step 5 — The AOE_GEOMETRIES N× multiplier (damage_resolver.py:93-115)**

When a skill's geometry is in AOE_GEOMETRIES and the defender is a PackProxy, damage is multiplied by `pack_proxy_size` (N=8). Single-target skills deal 1× against the same PackProxy. This is the pack-fight amplification.

**The actual balance model:**

- AOE skills hit single targets for 0.6× magnitude (reduced burst)
- AOE skills cost 15-30% energy (cheaper than burst)
- AOE skills have 3-8s cooldowns (shorter than burst)
- AOE skills deal N× (=8×) damage against PackProxy opponents

The per-hit damage reduction (0.6×) is a partial View B signal, but it is not compensatory — it reduces raw burst, not total throughput. The energy cost and cooldown reductions partially offset the magnitude penalty in single-target 1v1 fights. And in pack fights, the N× multiplier makes AOE skills outclass single-target by a factor of ~8 on the same energy cost. There is no mechanism in the generator or resolver that imposes a "total throughput equalizes at pack fights" constraint.

**Conclusion: View A is the operative philosophy.** AOE skills have lower per-hit damage (partial View B signal) but faster recast, lower cost, and an 8× pack amplifier with no compensating cost. The result is that AOE-capable classes are strictly better in pack fights and roughly comparable in 1v1 (lower burst offset by faster cycling). This is genre-correct View A — "AOE advantage is the class fantasy" — but it was not an explicit design decision. It is the emergent result of three independently set parameters (0.6× magnitude in math_model, 15-30% cost in role_constraints, N× in damage_resolver) that have never been examined together as a coherent budget.

### The file 29 conflict

File 29 (canonical/29-design-overview.md) states:

> "Reincarnated's classes differ by COMPOSITION first, by NUMBERS last."
> "damage_modifier is the last-resort fine-tune in a tight range (target 0.85-1.15)"

View A (AOE free upside, no compensation) is not inherently in conflict with composition-first design — kit shape still varies by archetype. But file 29 also identifies "AOE budget rebalancing for ARPG genre feel" as a known Category B gap. This confirms the AOE budget has always been acknowledged as incomplete.

The critical implication for Option 2: if View A is operative (AOE = free upside in pack fights), then Option 2's convergence semantics ("modifier = value at which class wins 50% of non-pack encounters") is internally consistent. But it means the post-Option-2 engine will produce modifiers calibrated on 1v1 performance while AOE classes enjoy uncompensated free upside in all pack content. Whether this is the intended metagame shape is a design call for Matt, not an implementation decision for gamora.

**What this is NOT:** View A being operative does not mean the implementation is wrong. Diablo 3, Diablo 4, and Path of Exile all implement something close to View A — AOE advantage is the class fantasy. The finding is that View A is implicit and unexamined, not that it is incorrect.

---

## Discipline-relevant observations

**Discipline #1 (math-before-code):** The AOE budget interaction — 0.6× magnitude + lower cost + N× pack multiplier — has never been analyzed as a joint system. Three separate parameters in three separate files (math_model.py, role_constraints.py, damage_resolver.py) combine to produce the operative balance philosophy. No math note in any seam captures this as an intentional joint design. This is an implicit-pillar situation: the philosophy exists, is internally consistent, and produces the right genre feel, but its derivation is accidental, not deliberate. Discipline #1 would require a math note before any future changes to any of these three parameters.

**Discipline #12 (semantic-shifting):** The B10.2 Two-Gauntlet Pattern decisions-log entry requires explicit supersession before Option 2 code ships, per the analysis in Q2. The entry's "Convergence = full fidelity" clause directly conflicts with Option 2's implementation.

**Candidate Discipline #13 (implicit-pillar drift):** The AOE budget case is a candidate for what could be named as a new discipline: "When three or more independent parameters produce a joint behavioral outcome, the joint behavior must be named in a math note before any parameter is changed." This prevents future modifications to 0.6× magnitude, energy_cost_range, or N× pack size from unknowingly destabilizing the emergent balance. Recommend adding to engineering-disciplines.md at next review — not blocking B10.4 but worth capturing.

---

## Overall verdict on the B10.4 tag

**BLOCK — pending resolution of the following before tagging `v1.3-b10-4-swarm-calibration`:**

1. **Option 2 implementation must ship.** The current B10.4 code (eff_attr=7 only) does not resolve the 8/10 convergence failure. The tag must not be applied until Option 2 code is implemented and a full regen confirms convergence.

2. **B10.2 Two-Gauntlet Pattern decisions-log entry must be superseded** with an updated entry reflecting the revised convergence semantics. This is required before the Option 2 code commits (Principle 4 — decisions-log is source of truth; Discipline #12 — semantic shift must be framed).

3. **New decisions-log entry for "non-pack convergence target"** — states explicitly that `damage_modifier` is calibrated against non-pack WR=50%, and pack fights are a diagnostic-only surface.

**Matt decision needed on one question:**

Is View A (AOE = free upside in pack fights; no compensating cost/damage mechanism) the intended permanent design philosophy, or is AOE budget rebalancing (file 29 Category B gap) still an active intent to move toward View B or C? Option 2 is correct under either answer, but the answer determines whether the B3 AOE budget item in file 28 is a future sprint priority or a conscious permanent deferral to B10 V2.

**After the above three items are resolved:** gamora re-runs full regen, confirms convergence, updates AGENT_STATE, then tags. The tag then passes to Matt for milestone approval per ADR-002 (milestone tagging is Matt-only authority).

---

## References

- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/balance_loop.py` — GAUNTLET_TIER_COMPOSITION, `_make_recompose_gauntlet()`, `balance_class()` primary/secondary loops
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/damage_resolver.py` — AOE N× multiplier (lines 93-115)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/b6_archetype_templates.py` — AOE_GEOMETRIES definition (line 415), archetype aoe_share_min/max
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/role_constraints.py` — energy_cost_range, cooldown_range per role
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/foundation/math_model.py` — apply_role_multiplier (area_damage=0.6×)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md` — gamora blocking state, 8/10 convergence failure confirmation
- `/Users/admin/Games/reincarnated-engine/design/decisions/decisions-log.md` — Two-Gauntlet Pattern (line 954), B10.4 entries (line 970+)
- `/Users/admin/Games/reincarnated-collaboration/canonical/29-design-overview.md` — "AOE budget rebalancing" Category B gap, shaped-balance philosophy
- `/Users/admin/Games/reincarnated-engine/data/telemetry.db` — abilities table query results (energy_cost_pct, cooldown_seconds by geometry_type, all class abilities)
