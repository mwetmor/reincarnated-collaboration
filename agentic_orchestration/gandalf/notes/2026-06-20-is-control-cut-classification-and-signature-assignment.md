# DoT/ailment emission — `is_control != hard` cut classification + per-ailment signature assignment

**Type:** design-fit ruling + per-ailment classification (gandalf design-track → input to rocket regen dispatch; Matt has DISPOSED the breadth fork; this scopes the implementation).
**Date:** 2026-06-20
**Author:** gandalf (story-and-design steward)
**Authority:** knight-rider-relayed Matt disposition of the emission-breadth fork. Matt resolved the fork (`a9cd243` full-signature breadth recommendation vs. DoT-trio-first) as the **middle path: `is_control != hard`** — damage signatures emit on the DoT trio AND soft-control ailments; hard-control ailments are EXCLUDED.
**Grounded first-hand on:** `config/ailments.yaml` (registry, authoritative `is_control` field), `element_biases.py:65-104` (ELEMENT_AILMENT 8-element map + `_ailment_is_control` derivation), `foundation/ailment_loader.py:334-353` (the `hard`/`soft`/`none` partition helpers the engine already exposes).
**Composes with:** `a9cd243` (breadth note — superseded on breadth by Matt's cut; its §4 CC-soup analysis and §6 STR-lever conservation are LIVE and load-bearing here), `df1023b` (Arm C pre-reg — STR bleed-as-focus-fire lever continuity), rocket's STR-bleed regression diagnosis (the wiring bug this regen fixes).

---

## 0. One line

The `is_control != hard` cut maps **exactly** onto the registry's own `is_control` field — no new classification work, the engine already partitions this way (`ailment_loader.get_hard_control_ailments()`). The cut emits signatures on **5 of 8** ailments (burn, bleed, drain, chill, consecrate) and excludes **3 of 8** (root, knockback, shock). **The one judgment call the cut surfaces that Matt's framing did not name: `consecrate` is `is_control: none` (amplification, not DoT), so the literal `!= hard` cut INCLUDES it. I rule it IN, but flag it explicitly below — it is the only ailment whose inclusion is a ruling rather than a mechanical read.** And the cut RETIRES the diminishing-returns guardrail as a gate on this regen: the guardrail I flagged in `a9cd243` was scoped to the hard-control trio specifically, and the cut removes exactly that trio from emission. Soft-control (chill, the only soft ailment) does NOT create an equivalent DR need. Guardrail = RETIRED-as-a-dependency for gamora's refit.

---

## 1. The cut maps onto an EXISTING engine field — verified, not asserted

Matt's cut is `is_control != hard`. The registry `is_control` field is a three-value enum (`config/ailments.yaml` header, verbatim):

> `is_control: "hard" | "soft" | "none"`
> `hard = immobilization/displacement (root, knockback, shock)`
> `soft = partial restriction (chill — slows but does not immobilize)`
> `none = no movement/action restriction (burn, bleed, drain, consecrate)`

The engine ALREADY exposes the exact partition the cut needs (`ailment_loader.py:342-345`):

```python
def get_hard_control_ailments(...) -> frozenset[str]:
    """Return frozenset of ailment names with is_control == 'hard'."""
```

So the cut is not a new design taxonomy I'm inventing — it is **the registry's own `is_control` field, read at face value.** The emitting set is the registry complement of `get_hard_control_ailments()`. This is recompose-first at the classification layer: the substrate already declares which ailments are hard-control, and the cut consumes that declaration directly. **rocket can implement the cut as `ELEMENT_AILMENT[element]` emitted UNLESS `AILMENT_IS_HARD_CONTROL[ailment]` — no hand-maintained exclusion list.**

---

## 2. ANSWER 1 — per-ailment `is_control` cut classification table

The full 8-ailment / 8-element registry, partitioned by the cut. (Your prompt's list — bleed, burn, drain, chill, root, knockback, shock, consecrate — is the COMPLETE set; there are exactly 8 ailments, one per element. No ailment is missing.)

| element | ailment | `is_control` | category | side of cut | EMITS signature? |
|---|---|---|---|---|---|
| physical | **bleed** | `none` | dot | non-control (DoT) | **YES** |
| fire | **burn** | `none` | dot | non-control (DoT) | **YES** |
| shadow | **drain** | `none` | dot | non-control (DoT) | **YES** |
| water | **chill** | `soft` | soft_control | soft-control | **YES** |
| holy | **consecrate** | `none` | amplification | non-control (special — see §4) | **YES** (ruled in) |
| earth | **root** | `hard` | hard_control | hard-control | **NO — excluded** |
| wind | **knockback** | `hard` | hard_control | hard-control | **NO — excluded** |
| lightning | **shock** | `hard` | hard_control | hard-control | **NO — excluded** |

**Emitting set (5):** bleed, burn, drain, chill, consecrate.
**Excluded set (3):** root, knockback, shock — the `is_control: hard` trio.

This matches the cut's intent precisely. The three excluded ailments are exactly the lock-stacking immobilize/displace trio (`root` positional lock, `knockback` forced displacement, `shock` paralysis-on-arc) — the ones whose per-hit re-application is the CC-soup/stagger-soup hazard I flagged in `a9cd243` §4. The cut surgically removes the hazard set from emission, which is what lets the breadth widen past the DoT trio WITHOUT the DR guardrail (§5 below).

**One classification note for rocket:** `chill` is the ONLY `soft` ailment in the registry. So "soft-control ailments" in the cut's phrasing resolves to a set of exactly one (chill / water). The cut's practical shape is "DoT trio + chill + consecrate." Worth knowing so the dispatch doesn't imply a broader soft-control population than exists.

---

## 3. ANSWER 2 — per-ailment damage-signature + scaling-attribute assignment (emitting set)

**Recompose-first holds completely — every signature in the emitting set is an ailment the substrate ALREADY declares with its OWN param shape. There is no new mechanic to invent. The "signature" is just the ailment the element already owns, emitted on chain_A.** The deferred control-ailment-damage-signature proposal (wind cut+bleed, earth thorny-root, water cold-burn) is NOT needed for this regen — it was a proposal to give *hard-control* ailments a damage tick, and those are exactly the ailments the cut now EXCLUDES. The cut makes that proposal moot for this pass.

| ailment | damage signature (what it does) | scales on (attribute) | param shape (registry, already exists) | recompose source |
|---|---|---|---|---|
| **bleed** | physical DoT — per-tick `hp -= tick_dmg` | **str/dex** (originating skill's scaling attr) | `tick_damage` (set from `base_mag`) + `duration_seconds` | registry `dot` category; F2 source-attr routing |
| **burn** | fire DoT — escalating per-tick damage | **int/wis** (originating skill's scaling attr) | `tick_damage` (from `base_mag`) + `duration_seconds` | registry `dot`; already int/wis-correct |
| **drain** | shadow DoT — sustained life-drain per-tick | **int/wis** (originating skill's scaling attr) | `tick_damage` (from `base_mag`) + `duration_seconds` | registry `dot`; already int/wis-correct |
| **chill** | soft-control: slow (no damage tick) | n/a (no damage signature) — see ruling | `slow_percent` + `duration_seconds` | registry `soft_control` |
| **consecrate** | zone DoT to shadow targets + heal-amp to self | **int/wis** (holy caster scaling attr) | `dot_tick_damage` (from `base_mag`, shadow-only) + `heal_amplification_percent` + `zone_duration_seconds` | registry `amplification` |

**The scaling-attribute routing is the SAME rule I ruled design-correct in `df1023b` §DESIGN-FIT(1): the tick reads the ORIGINATING SKILL's scaling attribute, mirroring the direct-damage path at `damage_resolver.py:312` (`scaling_stat = attacker.attribute_values.get(_sa_norm, 0)`).** Not a martial/caster hardcode, not the kit's highest attribute. This is what makes a STR kit's bleed scale on str/dex (the F2 fix gamora has committed) and a fire caster's burn scale on int/wis. Each DoT funds its own archetype. This composes directly with gamora's tick-scaling fix — no new sim work; the regen just needs to EMIT the effect so gamora's already-committed resolver has something to scale.

### The two signature-assignment rulings inside this table (these are design calls, not mechanical reads):

**(a) `chill` — emit the ailment, NOT a damage signature on it.** Chill's registry shape is `slow_percent` — it has no `tick_damage` param. The cut emits "damage signatures" on the non-hard set, but chill's *signature* is a slow, not a tick. **Ruling: emit chill as the water element's signature on chain_A (so water reads as itself — the chill lands), but it carries NO damage tick — its signature IS the slow.** This is correct design: chill is the soft-control identity marker (it makes water feel like water — KonoSuba's Aqua-tier "everything slows in my presence"), and forcing a damage tick onto it would invent a mechanic the substrate never declared (recompose-first violation). Chill emits as a slow-only effect; it contributes ZERO to the DPS band (which is why it adds no DR need — §5). **The phrase "damage signature" in the cut, applied to chill, resolves to "the chill slow," not "a new chill DoT."**

**(b) `consecrate` — IN, but it is the one ruling the cut's literal phrasing forces.** Consecrate is `is_control: none`, so `is_control != hard` literally includes it. But consecrate is NOT a clean DoT and NOT a soft-control — it is the `amplification` category (valenced zone: shadow-target DoT + ally heal-amp). Its damage signature (`dot_tick_damage`) applies ONLY to shadow targets. **Ruling: emit consecrate IN the set (the cut is `!= hard`, and consecrate is `none`; excluding it would require a special-case carve-out that contradicts the clean registry-field implementation in §1).** Holy substrate needs its signature to read as holy, same parity argument as every other element. The shadow-only DoT condition is a sim-side resolver concern (the resolver already knows consecrate's valenced shape); generation just emits the effect. **The one caution: consecrate's DoT only fires vs. shadow targets, so against the synthetic non-shadow endgame mob it contributes ~zero damage — meaning holy's DPS-band injection from this regen is near-nil. That is correct (holy's identity is amplification, not raw DoT), but rocket+gamora should not expect a holy band-shift from this regen the way they will see one for the DoT trio.**

**Net emitting-set DPS-band impact:** real injection on bleed/burn/drain (the three true DoTs, scaling on their archetype attrs); ZERO injection from chill (slow-only); near-zero injection from consecrate vs. non-shadow mobs. So the band refit gamora sizes is driven by the DoT TRIO, exactly as the `a9cd243` §5 economy predicted — the cut's addition of chill+consecrate widens the *thematic* emission to 5/8 without widening the *DPS-band* injection beyond the trio. This is the cleanest possible middle path: full-feeling substrate identity, DoT-trio-sized band move.

---

## 4. The consecrate flag, surfaced plainly for Matt (the one place the cut's wording underdetermines the answer)

Your read of the cut's intent: "hard-control ailments are the lock-stacking ones whose re-application risks CC-soup, so keeping signatures off them widens emission without the DR guardrail." **That intent is fully served by excluding the `hard` trio — and consecrate is not in that trio, so the intent does not speak to it.** I've ruled consecrate IN on parity + clean-implementation grounds. If Matt's mental model of the cut was "DoT trio + chill only" (i.e., he was thinking of consecrate as a control-adjacent or special ailment to leave out), that is a one-line amendment: exclude consecrate too, and the emitting set becomes 4 (bleed/burn/drain/chill). I do not think he should — holy deserves its signature and the shadow-only DoT is self-limiting — but it is the ONE place where `is_control != hard` as literally stated and "the DoT trio + soft-control" as conceptually described could diverge. Flagging so the dispatch encodes the intended set, not an accidental one.

---

## 5. ANSWER 3 — guardrail disposition: **RETIRED as a dependency on this regen + gamora's refit. Not kept, not must-size.**

This is the load-bearing question and the answer is clean.

**The DR guardrail I flagged in `a9cd243` §4 was scoped EXPLICITLY and ONLY to the hard-control trio (root/knockback/shock).** Verbatim from that note: *"The one risk to watch — CC-soup on the hard-control trio (root/knockback/shock)... This is the reason a substrate might NOT want its signature on every primary hit — and it is the only such reason. It does not apply to the DoT trio... or to consecrate."* The guardrail existed because, under the `a9cd243` full-signature breadth, root/knockback/shock would have ridden every chain_A hit and produced the stunlock treadmill.

**The `is_control != hard` cut removes exactly that trio from emission.** No hard-control ailment now carries a signature → the CC-soup-from-damage-stacking path is structurally closed by the cut itself. The guardrail's entire reason-for-being is gone. **This is precisely the trade Matt's middle path makes: accept a narrower emission (no hard-control signatures) in exchange for not needing the DR guardrail.** The cut and the guardrail-retirement are two faces of the same decision.

**Does soft-control (chill) create its OWN DR need? NO.** Three reasons:
1. **Chill carries no damage signature** (§3a ruling) — its signature is a slow, not a tick. There is no "damage-stacking" path on chill to diminish, because chill does no damage. The DR guardrail was a *damage*-stacking guardrail; chill has no damage to stack.
2. **Chill is `soft` control by registry definition** — "slows but does not immobilize." Stacking slow does not produce the lock-loop/stagger-soup failure that stacking root/knockback/shock does. A perma-slowed enemy is still a *fighting* enemy (it moves, attacks, just slower); a perma-rooted/knocked/shocked enemy is a non-participant. The CC-soup failure mode is specific to *hard* control removing the enemy from the fight; soft control degrades but does not remove. (Genre precedent: D2 chilling/freeze had a soft cap and felt fine perma-applied; D2 stun-lock and PoE perma-freeze were the degenerate cases — both *hard*. The cut excludes exactly the hard cases.)
3. **Even un-capped, max chill is `slow_percent: 0.50`** (registry max) — a 50% slow is a meaningful debuff, not an action-denial. There is no "soup" at 50% slow; the enemy still acts.

**So: the guardrail is RETIRED. gamora's refit pass does NOT inherit a DR-sizing dependency from this regen.** The refit sizes the DoT-trio DPS-band injection (bleed/burn/drain scaling on their archetype attrs) against the current bands — the exact refit `df1023b` Arm C already pre-registers and `a9cd243` §5 already scoped. No extra dependency. The chill+consecrate additions carry zero/near-zero DPS-band weight (§3 net-impact), so they do not even widen the refit's magnitude.

**The one honest caveat (does NOT reopen the guardrail):** if a LATER decision re-adds hard-control signatures (e.g., Matt revisits and wants root/knockback/shock to carry the deferred thorny-root/cut-bleed damage signatures from `project_ailment_damage_thematic.md`), the DR guardrail comes BACK as a dependency at that point. The guardrail is retired *for this cut*, not deleted from the design space. The deferred control-ailment-damage proposal and the DR guardrail are a matched pair: they ship together or not at all, and the `is_control != hard` cut ships NEITHER this regen. I record this so the retirement is understood as cut-scoped, not absolute — exactly the discipline `df1023b` §"What this run does NOT settle" holds for the profiled-resistance flag.

---

## 6. The three answers, tight (for the rocket regen dispatch)

1. **Cut classification — EMIT on 5, EXCLUDE 3, off the registry's own `is_control` field:**
   - EMIT (non-hard): **bleed** (none/dot), **burn** (none/dot), **drain** (none/dot), **chill** (soft), **consecrate** (none/amplification).
   - EXCLUDE (`is_control == hard`): **root**, **knockback**, **shock**.
   - Implement as `ELEMENT_AILMENT[element]` emitted UNLESS `is_control == "hard"` — read the registry field, no hand-maintained list. (`get_hard_control_ailments()` is the existing helper.)
   - ONE flag for Matt: `consecrate` is `is_control: none` so the literal cut INCLUDES it; I rule it IN, but confirm the intended set wasn't "DoT trio + chill only."

2. **Signature + scaling assignment (emitting set), recompose-first:**
   - **bleed → str/dex** (originating skill's scaling attr; F2 routing). DoT tick from `base_mag`.
   - **burn → int/wis**. DoT tick from `base_mag`.
   - **drain → int/wis**. DoT tick from `base_mag`.
   - **chill → slow-only, NO damage tick** (its signature is the `slow_percent`, not a DoT — emit the ailment, contributes 0 to DPS band).
   - **consecrate → int/wis**, shadow-target-only DoT (`dot_tick_damage` from `base_mag`) + self heal-amp; near-zero DPS vs. non-shadow mobs.
   - All ticks read the ORIGINATING SKILL's scaling attr, mirroring `damage_resolver.py:312` — composes directly with gamora's committed tick-scaling fix.
   - Breadth (which CHAINS carry it) is `a9cd243`'s separate ruling — chain_A primary-attack, all 4 tiers. The cut is orthogonal: it decides WHICH AILMENTS emit; `a9cd243` decides WHICH SKILLS. Both apply.

3. **Guardrail — RETIRED as a dependency on this regen + gamora's refit.** The DR guardrail was scoped to the hard-control trio; the cut excludes exactly that trio; the CC-soup path is structurally closed by the cut. Soft-control (chill) creates NO equivalent need (carries no damage signature, soft-slow doesn't lock, 50% max is not action-denial). gamora's refit inherits NO extra dependency — it sizes the DoT-trio DPS-band injection against current bands exactly as already pre-registered. Caveat: retirement is CUT-SCOPED — if hard-control signatures are ever re-added (deferred thorny-root/cut-bleed proposal), the guardrail returns as a paired dependency. Not this regen.

---

**Signed:** gandalf, 2026-06-20 — the cut maps onto the engine's own `is_control` field; emit 5, exclude the hard trio, recompose-first on every signature, guardrail retired-as-scoped. The one ruling beyond the mechanical read is consecrate-IN (flagged for Matt's confirmation). This is the gating classification for rocket's regen dispatch; design-fit only, no generation code touched.
