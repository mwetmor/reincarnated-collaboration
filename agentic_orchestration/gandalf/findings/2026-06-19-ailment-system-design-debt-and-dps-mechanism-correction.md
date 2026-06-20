# Finding — ailment-system design-debt + DPS math-note mechanism correction

**Author:** gandalf
**Date:** 2026-06-19
**Status:** DESIGN-DEBT — none of the three is a blocker for the current STR disposition. All three surfaced from the ailment-parity investigation Matt prompted ("do STR kits have functioning ailments? do INT/WIS kits?") during the combat-efficacy measurement work. Captured now so they are not lost; routing/fix deferred to their proper windows.
**Composes with:** the win-condition split doctrine (spine), the boss DPS instrumentation run, and the STR 9-pass-floor run (in flight). Code citations verified fresh 2026-06-19 (line numbers can drift — re-confirm before acting).

---

## Why these three are logged together

Matt's hypothesis was that an ailment asymmetry might explain STR's boss failure — "if a fire caster has burn but a physical melee cannot have bleed/cleave, it could cause some of this disparity." The investigation **inverted the premise** (physical HAS bleed, the exact structural mirror of fire's burn; the disparity is melee-vs-ranged allocation, not ailment access) but in doing so surfaced three real things about the ailment/DoT layer. Two are latent asymmetries in the engine; one is a documentation error in a prior math note. All three are design-debt to capture, not defects blocking the STR call.

---

## Finding 1 — all DoT ailments are INERT in the spatial sim (the shipping regime)

**The finding.** Three of the eight canonical ailments are DoT (burn / bleed / drain; `effect_resolver._DOT_AILMENT_NAMES`). In the spatial gauntlet — the only fight regime that ships — **none of them tick.** An ailment IS applied (an `ActiveEffect` is appended to the defender in `damage_resolver._try_apply_ailment`, ~line 992) but it is never advanced: the spatial engine has **zero** `tick_effects` / DoT references (`spatial_gauntlet/spatial_engine.py`, grep-confirmed absent), and the resolver adapter explicitly discards the scratch mutation (`spatial_resolver_adapter.resolve_spatial_hit` docstring: "its internal HP mutation is scratch and discarded. Only the returned damage float is carried back"). So the appended DoT effect is a discarded side-effect. Burn, bleed, and drain are **decorative** in the shipping sim today.

**Why it matters (design consequence).**
- It made the STR-vs-DEX comparison FAIR, which is load-bearing for the current disposition: both are physical, both carry bleed, both inert → bleed did not differentiate them, which is exactly what let the boss runs isolate melee-vs-ranged *allocation* as the sole variable. (This is the good news; the finding strengthens the STR read.)
- But it means three of eight ailments contribute zero combat power in the regime players actually fight in. The KPM/DPS measures (and therefore the cohort bands) currently capture **none** of the DoT contribution. The day DoT is activated in spatial, it is a real power injection that shifts every band — a re-fit event, not a free addition.

**Disposition.** Not a blocker. Park as a known interim state. Flag the band-re-fit dependency: whenever DoT goes live in the spatial sim, the `ENCOUNTER_COHORT_KPM_BAND` values must be re-derived (the same way the comment at `gauntlet_sim.py` flags `MOB_HP_DIFFICULTY_MULTIPLIER` as a re-fit trigger). Owner at activation time: gamora (sim) + jack-ryan (Gate-2 band re-fit).

## Finding 2 — DoT tick-scaling is INT/WIS-only (latent asymmetry; the real fix-before-activation)

**The finding.** When DoT *does* tick (in the non-spatial `effect_resolver` path), the tick magnitude scales **only on caster attributes:**

```
damage_resolver.py:987  eff_attr = attacker.attribute_values.get("intelligence", 0) or attacker.attribute_values.get("wisdom", 0)
damage_resolver.py:988  tick_scale = 1.0 + eff_attr * 0.003
```

`eff_attr` reads intelligence-or-wisdom and **never strength or dexterity.** So a physical bleed applied by an STR kit scales off that kit's (near-zero) int/wis — the bleed is near-worthless for the exact archetype whose canonical ailment it is. Contrast the DIRECT-damage path, which already scales fairly on each kit's own scaling attribute (`damage_resolver.py:312` — `scaling_stat = attacker.attribute_values.get(_sa_norm, 0) ...`). The fairness principle exists in the engine; it simply was never applied to the DoT tick path.

**Why it matters (design consequence).** This is backwards in the precise way that hollows out a class fantasy. **PoE gets this right:** physical-DoT (bleed) scales on physical/attack stats; fire-DoT (ignite) scales on spell/elemental stats — each damage-over-time primitive draws from the stat its source build invests in. Reincarnated's substrate assigns bleed to physical (`ailments.yaml`: bleed → physical, dot) — but the tick scaling routes through int/wis, so a STR bruiser's bleed is funded by a stat the bruiser doesn't have. If activated as-is, bleed would be a dead affix on martial kits and a live one only when an int/wis kit somehow applied it. That inverts the intended ownership.

**Disposition — the fix to land BEFORE DoT activation.** The tick scaling must read the originating skill's scaling attribute (martial source → str/dex; caster source → int/wis), mirroring the direct-damage path at `:312`. This is not new design — it is extending the existing fairness rule to the DoT path. Sequenced with Finding 1: Finding 1 says DoT is inert today (no rush); Finding 2 says **do not flip DoT live until this scaling fix lands**, or martial DoT ships dead-on-arrival. Owner at activation time: gamora (resolver) + gandalf (design-fit on the source-attribute routing) + jack-ryan (Gate-2).

## Finding 3 — gamora DPS math-note §1.1 mechanism claim is incorrect (non-blocking doc fix)

**The finding.** The DPS-instrumentation math note (`simulation/math/dps-measurement-instrumentation-2026-06-19.md`) §1.1 states that DoT "folds into the per-hit resolver float." It does not. Per Finding 1, the DoT `ActiveEffect` is appended to the defender as a discarded scratch side-effect (`spatial_resolver_adapter` docstring) — it is **not** folded into the returned damage float. The accumulated/returned float is direct-and-proxy damage only.

**Why it matters — and why it does NOT.** The **numbers are unaffected:** DoT contributes zero in the spatial regime either way (Finding 1), so whether one describes it as "folded in" or "discarded," the measured DPS / boss_HP_removed is identical, and the STR classification stands. This is a **documentation-mechanism error, not a data-integrity error** — the same class as jack-ryan's earlier cosmetic-citation INFO on that note, not a Gate-2 BLOCK.

**Disposition.** Non-blocking. Route a one-line correction to gamora (math-note author) + jack-ryan (Gate-2 record) **after the in-flight STR 9-pass-floor harness run settles** — do not interrupt the current run to fix a zero-impact doc line. Correct it so the mechanism record is accurate for whoever reads it next (especially relevant once Finding 1/2 make DoT non-zero, at which point this line would become genuinely misleading).

---

## Summary table

| # | Finding | Code anchor (verify before acting) | Bites when | Fix owner |
|---|---|---|---|---|
| 1 | DoT ailments inert in spatial sim | `spatial_engine.py` (no tick_effects); `spatial_resolver_adapter` docstring | DoT activated → band re-fit | gamora + jack-ryan |
| 2 | DoT tick-scaling int/wis-only | `damage_resolver.py:987-988` vs `:312` | DoT activated → martial bleed dead-on-arrival | gamora + gandalf + jack-ryan |
| 3 | math-note §1.1 "folds into float" wrong | `dps-...-2026-06-19.md` §1.1 vs adapter docstring | already (doc only; zero number impact) | gamora + jack-ryan (after current run) |

**Signed:** gandalf, 2026-06-19 — captured while fresh from the ailment-parity investigation. Findings 1+2 are the latent asymmetry to resolve before DoT goes live in the shipping regime; Finding 3 is a zero-impact doc correction. None gates the STR disposition.
