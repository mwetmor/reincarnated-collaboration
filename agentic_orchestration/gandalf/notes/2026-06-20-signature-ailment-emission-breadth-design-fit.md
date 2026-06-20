# Signature-ailment emission breadth — design-fit recommendation

**Type:** design-fit recommendation (gandalf design-track → rocket implements; Matt disposes at scope gate; informs, does not bind).
**Date:** 2026-06-20
**Author:** gandalf (story-and-design steward)
**Authority:** knight-rider-dispatched design micro-call following rocket's regression diagnosis (`reincarnated-engine/src/reincarnated/generation/notes/2026-06-20-str-bleed-emission-regression-diagnosis.md`) and gamora's DoT/ailment measurement finding (0 of 66 season-001 configs carry any ailment; STR has zero `tick_damage`). Matt confirmed STR was DESIGNED to carry bleed → wiring bug, not design gap.
**Composes with:** pre-reg df1023b (STR bleed-as-single-target-focus-fire-lever; deferred Arm C re-fires once this lands); `agentic_orchestration/gandalf/notes/2026-06-19-encounter-measurement-doctrine-spine.md` (clear-room = throughput-banded, boss-room = survive-and-kill, DPS measured not ceiling-gated).

---

## 0. One line

**Emit the element's signature ailment on the PRIMARY-ATTACK chain only (chain_A, all four tiers), full per-element signature (DoT trio AND control types), deterministically. Breadth = primary-attack-only. This restores STR's bleed as the single-target focus-fire lever exactly as df1023b specified, restores burn/drain to fire/shadow casters, and brings the control-signature substrates (water/earth/wind/lightning/holy) into thematic parity — while keeping the power injection (and downstream band refit) to ONE chain of twelve, not all twelve.**

---

## 1. The structural facts the call rests on (verified first-hand, not on report)

The emitter (`per_skill_emitter.py:389-497`) builds 3 chains × 4 tiers = 12 skills per kit. The role assignment (`_CHAIN_ROLE`, :354-358) is NOT uniform — it is the lever this whole call turns on:

| chain | T1 | T2 | T3 | T4 | what it IS |
|---|---|---|---|---|---|
| chain_A | primary_attack | primary_attack | primary_attack | primary_attack | the spammed single-target/main-damage chain |
| chain_B | secondary_attack | secondary_attack | secondary_attack | secondary_attack | the AoE chain |
| chain_C | control | control | support | support | utility/CC + sustain |

The element→ailment map (`element_biases.py` `_element_ailment`, validated against `config/ailments.yaml`) is intact and splits cleanly by registry `category`:

| element | ailment | category | ticks damage? |
|---|---|---|---|
| fire | burn | dot | **YES** |
| physical | bleed | dot | **YES** |
| shadow | drain | dot | **YES** |
| water | chill | soft_control | no |
| earth | root | hard_control | no |
| wind | knockback | hard_control | no |
| lightning | shock | hard_control | no |
| holy | consecrate | amplification | no |

STR's element pool is `["physical"]` → `ELEMENT_AILMENT["physical"] = "bleed"` resolves correctly the instant the emitter consults it. The sim already consumes these (`effect_resolver.py` `_DOT_AILMENT_NAMES`, registry-driven) with no schema change.

---

## 2. Micro-call 1 — WHICH skills carry the signature ailment: **PRIMARY-ATTACK ONLY (chain_A, all 4 tiers)**

**Recommendation: emit on chain_A only — the four primary_attack skills. NOT chain_B (AoE), NOT chain_C (control/support).**

Reasoning, design-first:

- **The signature ailment IS the primary-attack identity.** In every ARPG that does signature ailments well, the ailment is the *consequence of your main hit*, not a separate button. Diablo II's Open Wounds and PoE's "hits apply Bleed" both ride the attack you spam. STR's bleed is the focus-fire lever precisely because it accrues on the single-target chain you sit on. Putting it on chain_A and only chain_A is the cleanest possible expression of "your basic attack carries your element's mark."

- **chain_A is single-target; chain_B is AoE.** df1023b framed bleed as the SINGLE-TARGET focus-fire tool. chain_A (single_target_damage geometry) is its native home. Emitting on chain_B (aoe_damage) would convert a single-target lever into an AoE-DoT spray — exactly the "ailment-on-everything" power creep that broke late-D3 (every monster perma-ignited; trash melted before the ailment mattered). Keeping it off chain_B PRESERVES the single-target/AoE distinction the geometry already encodes.

- **chain_C is control/support — emitting a control-type ailment there would double-stack control.** chain_C T1-2 are ALREADY `control` role. If earth's `root` or wind's `knockback` also rode chain_C, you'd get control-on-control: a CC chain that also CCs as a side effect. That is the CC-soup hazard (micro-call 3). Keeping signature ailments off chain_C means the control chain controls *by design* and the primary chain marks *by signature* — two distinct identities, not a blur.

- **Band-refit economy.** One chain of twelve carries the injection. This is the smallest breadth that still restores the designed lever. See §5.

**Tiering within chain_A: all four tiers, NOT tier-gated.** The ailment is a flat signature, not a power escalator — its magnitude scales off the skill's own `base_mag` (registry note: "set dynamically from base_mag at generation time"), so T1 bleed is small and T4 bleed is large *automatically*. Gating it to T4 would make low-level STR feel signature-less (no bleed until capstone) and would break the "every primary hit marks" read. Emit on all four; let `base_mag` do the scaling.

---

## 3. Micro-call 2 — DoT trio only, or full signature: **FULL PER-ELEMENT SIGNATURE (DoT + control)**

**Recommendation: emit the FULL `ELEMENT_AILMENT[element]` signature — the DoT trio (burn/bleed/drain) AND the control types (chill/root/knockback/shock/consecrate). Not DoT-only.**

Reasoning:

- **Thematic parity is the whole point of substrate identity.** `substrate-identity-declarations-2026-05-17.md` assigned each element ITS ailment as a load-bearing identity marker. If only the DoT-3 emit, then fire/physical/shadem casters have a signature and water/earth/wind/lightning/holy casters silently don't. That is a two-tier substrate world where half the elements feel mechanically mute. KonoSuba's Megumin is *all* signature (one explosion, fully herself); a water mage whose chill never lands is a Megumin who can only point. Emit the full signature so every element reads as itself.

- **The DoT-trio-only framing is a measurement artifact, not a design boundary.** gamora's run measures `tick_damage` because that is the lever the encounter-doctrine throughput band reads. But "what the run measures" must not become "what generation emits." Restricting emission to the measurable subset would let the instrument define the design — the exact inversion the doctrine spine warns against (§GATE-1: "what the run measures must not become what generation emits"). The control ailments are no less designed for being un-ticked.

- **The sim already consumes both cleanly.** `_DOT_AILMENT_NAMES` routes the tickers to DoT handling; the control types route to their own (root/knockback/shock = `is_control: hard`, chill = `soft`, consecrate = `amplification`). No new mechanic; registry-driven on both sides. Emitting the full signature costs no sim work the DoT-3 wouldn't also cost.

- **STR's lever is untouched and SHARPENED.** Full-signature emission still gives STR exactly `bleed` on chain_A — the df1023b focus-fire lever — because STR's pool is mono-physical. Full-signature is a SUPERSET of DoT-only that happens to also serve the control substrates; it takes nothing from STR.

---

## 4. Micro-call 3 — thematic coherence + the CC-soup risk

**"Every primary attack applies the element's signature ailment" MATCHES the design vision and genre expectation — WITH ONE GUARDRAIL on the hard-control trio.**

What's right:
- Signature-ailment-on-main-hit is the ARPG/isekai genre default (D2 Open Wounds, PoE hit-applied ailments, Slime-class "every strike carries my nature"). It is what makes an element feel like an element rather than a damage-type recolor.
- DoT signatures (burn/bleed/drain on primary) are pure upside: they reward focus-fire, give DoT-archetypes a mirror-match identity, and create the "they're already dying, switch targets" texture that makes single-target play feel tactical.

**The one risk to watch — CC-soup on the hard-control trio (root/knockback/shock):**
- `root`, `knockback`, `shock` are `is_control: hard` (immobilize/displace). If EVERY primary hit of an earth/wind/lightning kit hard-CCs, the enemy is permanently locked/launched and the fight stops being a fight — it becomes a stunlock treadmill. This is the late-D3 / early-Lost-Ark stagger-soup failure: when control is free and constant, control stops meaning anything and the encounter loses its threat curve. knockback is the worst offender — perma-launch can punt a boss out of its own arena geometry.
- **THIS is the reason a substrate might NOT want its signature on every primary hit** — and it is the only such reason. It does not apply to the DoT trio (a DoT ticking constantly is fine — that's the point) or to consecrate (zone amplification, not a lock).

**The guardrail (recommend, route to rocket; does NOT block the core fix):** the hard-control trio needs a *per-application gate* so it doesn't fire every tick — either (a) a cooldown/diminishing-returns window on re-application (the genre-standard fix: D4 and Lost Ark both DR-stack hard CC), or (b) emit the hard-control signature on chain_A T-capstone-only while the DoT/soft trio emit on all four. I lean (a) — DR is the cleaner, more genre-faithful answer and keeps the "every hit marks" read intact for the visual/feel layer while neutering the lock-loop. But (a) is a SIM-side concern (the emitter just emits; the resolver applies DR), so it can land as a fast-follow and need not gate the generation fix. **Flag it now so it isn't discovered as a "why is the boss stunlocked" bug after the band refit.**

Net: emit the full signature on chain_A; the DoT-3 and chill and consecrate are clean immediately; the hard-control-3 want a DR window before they ship to players, but the generation fix is correct as specified and the DR gate is a sim-side fast-follow.

---

## 5. Micro-call 4 — band-shift / breadth tradeoff (for rocket + Matt to weigh)

**The breadth/refit tradeoff, stated plainly so the scope gate can price it:**

- **Primary-attack-only (recommended) injects power into 1 chain of 12 (4 of 12 skills).** Every kit gains a second effect on its four chain_A skills. For STR this is +bleed-DoT on the spam chain — a real but bounded DPS lift. The band refit is the SAME refit gamora's DoT-activation run already records as a dependency; it does not widen with this choice because chain_A was always the measured-throughput chain.
- **Had we chosen primary+secondary (chain_A+B = 8 of 12), the injection roughly doubles** and the AoE band (chain_B drives clear-room KPM) moves too — a second, larger refit on the throughput band that the encounter-doctrine spine just stabilized. Not worth it; chain_B AoE doesn't need a signature to do its job.
- **Had we chosen all-skills (12 of 12),** chain_C control/support skills would also carry ailments — maximal injection, maximal refit, AND the CC-soup hazard at its worst (control chain double-controlling). Reject.

**The caution for rocket:** size the band shift off chain_A only. The DoT trio's injection is a clean DPS-band move (recompose-first per B14.5 V1 pattern; the encounter-doctrine clear-room band already has the floor+ceiling machinery to absorb it). The hard-control trio's injection is NOT a DPS move — it's a fight-duration move (locked enemies die slower OR get punted), so its band effect is indirect and the §4 DR guardrail must be sized BEFORE the control-substrate bands are read, or the band data will encode the stunlock artifact. Generation-side and sim-side refits sequence together (rocket's diagnosis §Blast-radius already flags this).

---

## 6. STR-lever conservation check (df1023b)

Confirmed: the recommendation keeps STR's bleed as the single-target focus-fire lever exactly as pre-registered.
- STR pool = mono-physical → `ELEMENT_AILMENT["physical"] = bleed`.
- Emitted on chain_A (single_target geometry) all 4 tiers → bleed accrues on the spammed single-target chain.
- NOT on chain_B → bleed stays single-target, not AoE-sprayed.
- `base_mag`-scaled → small at T1, large at T4, no tier-gate dead zone.
This IS the df1023b lever. The deferred Arm C re-fires against a generation that now actually emits the thing it measures.

---

## 7. Decisions-log feed

This note feeds the entry "season-001 generation emits signature ailments per element" (route via knight-rider → jack-ryan writes; architectural YES per rocket diagnosis §Decisions-log). The design ruling to record:
- **Breadth:** primary-attack chain only (chain_A, all 4 tiers).
- **Signature scope:** full per-element signature (DoT trio + control types), not DoT-only.
- **Guardrail:** hard-control trio (root/knockback/shock) requires a sim-side diminishing-returns re-application window before player-ship (fast-follow; does not gate the generation fix).
- **Rationale anchor:** signature-ailment-on-main-hit is the genre-faithful expression of substrate identity; restricting to DoT-3 would let the measurement instrument define the design and would mute half the elements.

---

## 8. What I am NOT ruling (reserved for Matt at the scope gate)

- The DR-window numbers (cooldown length / stacks) on the hard-control trio — sim-side calibration, gamora's lane.
- Whether the hard-control guardrail lands same-wave or fast-follow — sequencing, knight-rider's lane.
- The band-refit magnitude itself — rocket sizes; Matt disposes.
This note sets emission BREADTH and SCOPE and names the one risk; it does not bind the fix.
