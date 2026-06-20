# Pre-registered interpretation rule — DoT/ailment + mitigation-symmetry 3-arm run

**Author:** gandalf
**Date:** 2026-06-20 (written BEFORE the gamora run returns — deliberately; the fourth holding of this discipline across the STR-disposition arc)
**Why pre-register:** the boss-numbers run drifted toward "degenerate," the STR 9-pass run tempted toward "swarm-specialist" — both times only the read fixed *before* the data held the disposition honest. This run is the most confound-laden of the three (an armor/resist asymmetry sits underneath STR's failure, so the result is contaminated by a measurement artifact I surfaced myself). The antidote to retrofitting falsifiers is to bind them ahead of the result. This note commits how I will read each of Q1–Q4 — and which Q1 outcome leans (A) "the tools existed" vs (B) "we need more skills" — so the data rules me, not the reverse.
**Consumes:** output of the dispatch `agentic_orchestration/dispatches/2026-06-20-gamora-dot-ailment-mitigation-symmetry-run.md` (amends my brief `gandalf/requests/2026-06-20-dot-ailment-activation-and-physical-scaling-fix-run-brief.md`, commit `f42915f`). 3 arms: A = existing baseline (DoT inert, mitigation asymmetric — pulled from `612c1a8`, not re-run); B = mitigation SYMMETRIC only (F4); C = DoT active + symmetric (F1+F2+F4). Subjects STR + dex/int/wis. Bands UNTOUCHED.
**Composes with:** the STR 9-pass-floor disposition (`gandalf/notes/2026-06-19-str-9pass-floor-pre-registered-interpretation.md`, RESOLVED — route-via-floor CONFIRMED, anchor-gap as texture *with a working lever*); the doctrine spine §5/§5a (STR ships-via-floor only WITH a focus-fire LEVER; bleed is the candidate lever); the ailment design-debt findings (`gandalf/findings/2026-06-19-ailment-system-design-debt-and-dps-mechanism-correction.md`, Findings 1 & 2 are exactly F1/F2).

---

## The confound this run exists to decompose

STR's disposition (RESOLVED 2026-06-19) was ruled on a measurement I later found to be CONFOUNDED. The synthetic endgame mob carries nonzero armor but `elemental_resistances={}` — physical eats **8/36/66/90/93%** mitigation across swarm→boss tiers; elemental eats **0%**. STR's elite/boss failure maps *exactly* onto that physical-only gradient (boss control: str 0.00 / dex 0.79 / int 0.99 / wis 0.99). So I cannot yet tell how much of STR's gap is a real allocation problem versus an artifact of casters fighting an unarmored-against-magic mob. **The run tests the PREMISE (fair mitigation) before crediting the SOLUTION (bleed lever).**

The decomposition is two single-lever transitions (Discipline #24):
- **A→B** isolates the **mitigation confound** (F4 only — casters now eat what physical eats).
- **B→C** isolates the **bleed lever** (F1+F2 — DoT activates + physical-DoT scales on str/dex, on top of symmetric mitigation).

Every cell is band-fit-classified against the **CURRENT untouched bands** so every shift is visible against the bands I know.

---

## Q1 — decompose STR's elite/boss gap (A→B→C). PRE-COMMITTED PRIOR.

STR fails elite_pack by −2.25 KPM (max cell 3.40 vs 5.65 floor) and times out 100% on boss. I am decomposing that gap into three buckets. **My pre-committed prior on the split:**

| Bucket | Transition | My prior magnitude | Reasoning |
|---|---|---|---|
| **armor-confound** | A→B (relative shift) | **SMALL on STR's own cells; LARGE on the *relative* gap** | F4 does not touch STR's physical damage — STR still eats the same 90/93% physical mitigation in B as in A. STR's *absolute* elite/boss numbers should barely move A→B. What A→B changes is the **reference frame**: casters fall toward STR (Q2), so the *relative* "STR is uniquely broken" framing shrinks even though STR's own cells are ~static. |
| **residual allocation** | what STR still fails at B | **STILL below-floor on elite_pack; STILL timeout on boss** | with DoT inert (B), STR has no single-target lever. The 9-pass allocation thesis predicts STR remains below-floor on the anchor+adds shells in B. I expect B ≈ A for STR's own cells. |
| **bleed-lever-closed** | B→C | **the decisive transition — this is where STR's gap moves or doesn't** | F1+F2 give STR a working bleed that scales on str/dex. IF the lever works, elite_pack rises toward/into band and boss timeout drops. This is the (A)-vs-(B) skill-question's first empirical answer. |

**What CONFIRMS "STR ships-via-floor with a WORKING lever":** B→C closes a *material* fraction of STR's elite_pack gap (KPM rises meaningfully toward the 5.65 floor — I pre-commit a **≥1.0 KPM rise** on the elite_pack max cell as the threshold for "the lever bites") AND boss timeout drops below 1.000 (any non-zero boss survive+kill in C = the lever converts an unwinnable fight into a winnable-with-intent one). The gap becomes a *choice* (bleed the anchor, cleave the adds), which is the texture-not-wall disposition the spine §5a reserved.

**What says "the lever is INSUFFICIENT (B-leaning — needs more skills / weapon-effects)":** B→C moves STR's elite_pack cell by **<1.0 KPM** AND boss stays at timeout=1.000. That means the substrate's single bleed tool, even working and correctly scaled, does not fund enough single-target throughput to close the gap — the focus-fire fantasy needs MORE than one activated ailment (additional single-target skills, weapon-effect single-target levers, or a kit-construction change). That is the (B) answer: the tools that existed are not enough.

**FALSIFIER (the result that would surprise me):** STR's elite_pack cell moves *substantially* A→B (>0.5 KPM) with F4 alone. That should not happen — F4 only adds elemental resist to the mob; STR attacks physically and already ate full physical mitigation in A. If STR's physical KPM shifts on a pure-elemental-resist change, the arm isolation is BROKEN (F4 is leaking into the physical path, or the harness is not gating cleanly) → quarantine, do not read Q1 until reconciled. A second surprise: B→C *over*-closes — STR's elite_pack vaults **above-ceiling** — which would mean the `0.003` coefficient is too hot at this tier and the lever needs magnitude *reduction*, not "insufficient." (That is a magnitude-tune signal, downstream, NOT a disposition reversal.)

---

## Q2 — caster A→B drop. PRE-COMMITTED PRIOR.

Today casters eat **0%** elemental mitigation. Under F4 they eat the physical curve: 8/36/66/90/93% by tier. **My pre-committed prior on the magnitude:**

- On **swarm/clear tiers** (8–36% mitigation): int/wis KPM drops **modestly** — a 36%-mitigation tier removes roughly a third of caster elemental throughput, so I expect clear-room caster KPMs to fall toward (not below) their band floors. Casters currently straddle/clip clear ceilings (the 9-pass run flagged int/wis above-ceiling clipping); A→B should pull them DOWN off those ceilings — which is a *correction*, not a crater.
- On **boss/mini_boss tiers** (90–93% mitigation): caster boss KPM/throughput drops **hard** — at 90% mitigation a caster keeps ~10% of its elemental damage. int boss survive+kill (0.992) and wis (0.984) should fall materially. I pre-commit that **caster boss survive+kill drops below 1.000 and plausibly into the 0.5–0.9 band** once they eat 90%+ mitigation.

**What REFRAMES "casters dominate" as a free-mitigation artifact:** if the A→B caster boss-tier drop is **large** (survive+kill falls by ≥0.15 absolute, or boss KPM falls by ≥40%), then a meaningful share of the prior "casters clear bosses, STR doesn't" read was casters fighting a mob that was transparent to magic. That sizes the downstream band re-fit and reframes the roster-balance picture: casters are not intrinsically boss-dominant; they were eating free mitigation STR never got.

**FALSIFIER (the result that would surprise me):** caster KPM does NOT drop A→B, on either int OR wis, on the boss tiers. That is the Fold-A integrity failure the dispatch elevated to critical: it means `rotating_elements` under-covers the elements the caster cohorts actually cast, so uncovered elements silently resolve to 0.0 resist and the symmetric-mitigation isolation is PARTIAL. **If either int OR wis fails to drop A→B, the run is QUARANTINED — the resist dict is under-covered; Q2 is confounded and A→B is dirty. Do not read Q1 or Q2 until both caster cohorts demonstrably drop.** (The §7 smoke assertion is the enforcement; this pre-reg binds me to honor a quarantine if it fires rather than reading a partial drop as a real result.)

---

## Q3 — boss absolute difficulty under symmetric ~90–93% mitigation (Arm B). PRE-COMMITTED THRESHOLD.

Once casters eat 90–93% boss-tier mitigation (B), the boss may become unkillable for *everyone* — STR already times out, and casters lose ~90% of their throughput. **The threshold I pre-commit, before data:**

> **If NO attribute — str, dex, int, OR wis — achieves boss survive+kill ≥ 0.50 under symmetric mitigation in Arm B, the boss is absolutely too hard, and Matt's armor-nerf for the boss is WARRANTED (downstream, data-driven — NOT this run).**

Rationale for 0.50: survive+kill is defense-free at faithful power (`a_dead=0.000` everywhere, spine §5) — the boss gate is purely kill-before-the-240s-enrage. If even the genre's designated boss-killers (casters) cannot beat the enrage clock more than half the time once mitigation is fair, the encounter's HP/enrage-timer is miscalibrated for the population, not the builds. Below 0.50 for ALL attributes = the encounter is the problem.

**The nuance I bind now so I do not over-call the nerf:** if casters land **0.50–0.85** survive+kill in B (degraded but viable) and only STR times out, that is NOT an armor-nerf signal — that is the boss being correctly hard for everyone, with STR's *specific* gap (no single-target lever in B) still the live question for C. The armor-nerf is warranted ONLY when the boss defeats EVERY attribute, not when it merely defeats STR.

**FALSIFIER (the result that would surprise me):** casters retain **≥0.95** boss survive+kill under symmetric 90%+ mitigation. That would mean 90% mitigation barely dented caster boss throughput — which would imply caster boss kills are NOT primarily elemental-damage-driven (proxy/DoT/non-elemental sources dominate), OR the mitigation is not actually reaching the boss-tier damage. Either way it would falsify my "casters were eating free mitigation" premise and demand I re-trace where caster boss damage actually comes from before crediting any A→B reframe.

---

## Q4 — physical-bleed vs caster-burn symmetry (Arm C). PRE-COMMITTED FAIRNESS DEFINITION.

In C, DoT is live and physical-bleed scales on str/dex (F2) while caster-burn scales on int/wis (unchanged). Both bypass mitigation (ticks apply `hp -= tick_dmg` after only `absorb_with_shield`, no armor/resist lookup — effect_resolver ~:62-71). **What "comparable contribution, each on its own attribute" looks like, bound in advance:**

> A STR kit's bleed-tick contribution (as a fraction of that kit's total damage) is within roughly **0.5×–2.0×** of an int/wis kit's burn-tick contribution (as a fraction of *its* total damage), at matched investment. Each DoT primitive funds its *own* archetype's kit at a comparable proportional level. The bleed is **non-trivial** on a STR kit (the F2 fix verified: a STR kit's bleed scales on its real str/dex, not its near-zero int/wis — so the tick is materially > the pre-fix near-zero).

**What FALSIFIES the fairness claim:** STR-bleed contribution remains **near-zero** in C (the F2 source-attr routing did not take — bleed is still scaling on int/wis, or on nothing) → the fix is broken, not the design. OR the asymmetry is **>3× in either direction** at matched investment — caster-burn dwarfs physical-bleed (or vice versa) by more than 3× as a fraction of kit damage — which means the two DoT primitives are NOT funding their archetypes symmetrically and the substrate's bleed→physical / burn→fire assignment is hollow on one side. Either is a fairness falsification requiring a fix before DoT ships, not a magnitude tune.

**The tick-bypass confirmation is a hard gate, not a soft read:** Q4's symmetry interpretation ASSUMES ticks bypass mitigation. If gamora finds ticks DO get mitigated anywhere (routed through `damage_resolver.py:470` or armor), the whole Q4 frame changes — physical bleed would eat the same 90%+ boss mitigation as direct physical, collapsing the lever exactly where STR needs it. **I pre-commit: if ticks are mitigated, Q4 is re-opened and the Q1 lever read is contingent on that — a mitigated bleed is a far weaker lever than a bypass bleed, and "STR ships with a working lever" weakens accordingly.**

---

## The (A)-vs-(B) skill-investigation bearing — bound in advance

This run is the first empirical probe of Matt's (A) "the tools existed" vs (B) "we need more skills" question. I bind which Q1 outcome leans which way, BEFORE data:

- **Leans (A) "the tools existed":** B→C closes STR's elite_pack gap by ≥1.0 KPM AND drops boss timeout below 1.000. The substrate's single bleed tool, once activated and correctly scaled, suffices to convert the anchor-gap from wall to choice. The tools were there; they just weren't wired. → STR ships-via-floor with a *working* lever; the (A)-vs-(B) investigation can close on the (A) side for STR specifically.
- **Leans (B) "we need more skills":** B→C moves STR's elite_pack cell <1.0 KPM AND boss stays at timeout=1.000. One activated ailment is not enough single-target throughput. The focus-fire fantasy needs additional single-target skills / weapon-effect levers / kit-construction work. → the (A)-vs-(B) investigation opens toward (B) for STR; this run scopes the *next* investigation rather than closing this one.
- **The honest middle I will NOT collapse:** B→C closes elite_pack but NOT boss (timeout stays 1.000 even with a working bleed). That is a *partial* lever — it makes the elite_pack gap a choice but leaves the solo-boss as the one irreducible gap. I pre-commit to reading that as "lever works for the recurring case (elite_pack), insufficient for the extreme case (solo boss)" — which leans (A) for clear-room texture and (B) for the boss specifically. I will not round that to either pole.

---

## Consistency rails (quarantine the run if these break)

1. **Arm isolation holds.** A→B differs ONLY by F4 (mitigation); B→C differs ONLY by F1+F2 (DoT). Same seeds-by-construction, same population, same shells, same bands. If any other variable moved, quarantine.
2. **Both caster cohorts drop A→B (Fold-A).** int AND wis KPM must both fall A→B. If either does not, `rotating_elements` under-covers → quarantine (Q2 binding above).
3. **STR physical cells ~static A→B.** STR eats no new mitigation from F4 (it's already full physical mitigation); STR's own elite/boss cells should barely move A→B. A large STR A→B shift = arm-isolation leak → quarantine.
4. **Arm A provenance matches.** The `612c1a8` baseline cells must be same-population, same-faithful-power, same-bands as B/C so A→B is apples-to-apples. Any drift noted before reading deltas.
5. **DoT demonstrably ticks in C; bleed scales on str/dex.** Smoke shows non-zero `dot_damage` AND a STR kit's bleed is non-trivial (F2 verified). If DoT is still inert or still int/wis-scaled in C, the fix didn't land → do not read Q1/Q4.
6. **V1 (tier_2 ran on all 18 in EACH run arm).** No defaulted-0.0 KPM masquerading as a measured miss — the generalized trap. Read the math note; do not assert.
7. **Boss survival stays defense-free.** `a_dead=0.000` should hold (faithful power) — the boss gate remains kill-before-enrage. If attributes start DYING in B/C, the regime drifted → reconcile before reading Q3.

---

## DESIGN-FIT CHECK (the part this seat owns — surfaced for gamora BEFORE the math note locks)

The brief asks me to rule design-fit on two things before implementation locks:

### (1) Source-attribute routing: martial→str/dex, caster→int/wis — IS this the right mapping?

**RULED: YES, this is the correct design mapping — it is the genre-correct fix, not a convenience.** PoE is the precedent and gets this exactly right: physical-DoT (bleed) scales on physical/attack stats; fire-DoT (ignite) scales on spell/elemental stats — **each damage-over-time primitive draws from the stat its source build invests in.** Reincarnated's substrate already assigns bleed→physical and burn→fire (`ailments.yaml`); the *only* error is that the tick path routed through int/wis regardless of source (Finding 2). Routing the tick through the originating skill's scaling attribute — mirroring the direct-damage path at `damage_resolver.py:312` — is not new design; it is extending the engine's OWN existing fairness rule (already live on direct damage) to the DoT path. A bleed that scales on the stat a bruiser doesn't have is a dead affix on its own archetype; the fix makes bleed fund the class fantasy it was assigned to. **No design concern — this is recompose-first done right.**

**One precision flag for gamora (not a blocker):** the routing must read the **originating SKILL's** scaling attribute, not the attacker's *highest* attribute or a hardcoded martial/caster flag. A skill's scaling attribute is its design-intended funding stat; routing through "whatever attribute the kit has most of" would let an off-archetype kit accidentally fund a bleed it shouldn't. Mirror `:312`'s `scaling_stat = attacker.attribute_values.get(_sa_norm, 0)` precisely — the skill's normalized scaling-attr, not a kit-level max. (The dispatch already specifies this; I'm binding it as the design-correctness condition, not just an implementation note.)

### (2) Symmetric-mitigation: the boss SHOULD be hard for everyone, not just physical — is F4 thematically coherent?

**RULED: YES, symmetric mitigation is the thematically coherent state, and the current asymmetry is the incoherence.** A boss that is transparent to magic but armored against steel is not a *designed* difficulty — it is an accident of `elemental_resistances={}`. Thematically, an endgame anchor SHOULD demand respect from every damage type; a caster melting a boss that walls a fighter is a free-mitigation artifact, not a class-fantasy expression. F4 makes the boss hard *for everyone*, which is the spine §2 over-performance asymmetry's whole point: bosses are payoff moments that every archetype earns by beating the enrage clock, not by exploiting an un-resisted damage channel.

**The design concern I DO flag — and it is a real one, surfaced now before lock:** F4 sets `elemental_resistance = armor/(armor+3000)` so casters eat *exactly* what physical eats. That makes mitigation **perfectly symmetric across all elements**. But the genre's richest boss design is NOT uniform resistance — it is **resistance PROFILES** (D2's immunities, PoE's resistance-by-element, Grim Dawn's per-monster resist spreads) that reward damage-type *diversity* and build-crafting around a boss's specific weaknesses. Uniform symmetric resistance is the correct *measurement-baseline* for THIS run (it isolates the confound cleanly — no element is advantaged), but it should NOT silently become the *shipping* boss design. **Flag for the downstream armor/resist tuning pass (NOT this run): once the confound is decomposed, the design question is whether bosses get per-element resistance PROFILES (richer, build-crafting-rewarding) rather than flat uniform resistance (clean but flavorless).** Uniform-for-measurement now; profiled-for-shipping later is the design arc I'd defend. This run should explicitly NOT lock uniform resistance as the production boss design — it's a measurement instrument.

**Net:** both fixes are design-correct for this run. F2 is genre-correct and ships as-is. F4 is the correct measurement baseline AND the correct *direction* for shipping (bosses hard for everyone), but its *uniform* form is a measurement choice that should not harden into the shipping resistance design — profiled resistance is the richer downstream target. No blocker; one downstream design-arc flag.

---

## What this run does NOT settle (do not overclaim)

- **Magnitude tuning** (the `0.003` coefficient) — measure-only this pass; if the lever over/under-shoots, that's a downstream tune, not a disposition reversal.
- **Armor-level tuning** (`ARMOR_MITIGATION_K=3000` and the `mob_armor` values) — Q3 produces the INPUT to Matt's armor-nerf call; it does not make the call.
- **The band re-fit** — two band-shift events (DoT-live, resist-live); this run measures the shift against current bands; the re-fit is a separate downstream gamora+jack-ryan step.
- **Profiled vs uniform boss resistance** — the design-fit flag above; a downstream design question, explicitly NOT locked by this run's uniform-resistance instrument.
- **The full (A)-vs-(B) skill investigation** — this run is its FIRST probe (STR specifically); dex/int/wis are controls + caster-impact measure, not subjects.
- **rogue** — still un-re-read at faithful power; out of scope.

---

**Signed:** gandalf, 2026-06-20 — the read, fixed before the data, so the data rules me and not the reverse. The fourth holding of this discipline across the STR arc. Q1 decomposes STR's gap into armor-confound vs residual-allocation vs lever-closed, with ≥1.0 KPM elite_pack closure + boss-timeout-drop as the (A)-leaning threshold and <1.0 + timeout-1.000 as the (B)-leaning threshold; Q2 quarantines on either caster failing to drop A→B; Q3 warrants the armor-nerf only if NO attribute reaches 0.50 boss survive+kill in B; Q4 falsifies fairness on near-zero STR-bleed or >3× asymmetry, contingent on tick-bypass holding. Both fixes are design-correct; the one downstream flag is that uniform symmetric resistance is a measurement instrument, not the shipping boss design — profiled resistance is the richer target.
