# Methodology Questions for Matt — Phase 1 Output

**Date:** 2026-05-20
**From:** legolas (Mode A reconnaissance)
**To:** Matt (via gandalf review)
**Purpose:** Questions that need resolution before Phase 2 scope can be locked

---

## Q1: Render Pipeline — URP vs Built-in (BLOCKS VFX PROCUREMENT)

**Question:** Is the Reincarnated game target render pipeline URP or Built-in?

**Why it matters:** Several VFX packs are Built-in only (e.g., SineVFX Aura and Ground Effects). Several newer packs are URP only (e.g., Ultimate Movement FX). If URP, the VFX procurement catalog can be larger and better-quality. If Built-in, some packs must be excluded.

**Recommendation:** URP. It is the Unity-recommended pipeline for new mobile-first projects, compatible with the majority of high-quality VFX packs, and the pipeline for the Pixi.js demo eventual Unity migration would logically target URP.

**Urgency:** Blocks Phase 2 VFX procurement planning.

---

## Q2: Canonical Element Count — 4 or 7? (AFFECTS TRACK B SCOPE)

**Question:** For VFX procurement planning, are we targeting 4 rotating elements (fire/water/earth/wind) or all 7 (fire/water/earth/wind/lightning/holy/shadow)?

**Context found:** The engine's `config/elements.yaml` declares only 4 rotating elements (fire/water/earth/wind/physical). But `config/substrate_identities/` contains 7 files: fire/water/earth/wind/lightning/holy/shadow. The Phase-1 P1 substrate expansion added lightning/holy/shadow. The element pool (`pool.json`) contains vocab-freeze entries for some lightning/holy/shadow vocabulary.

**Why it matters:** If we need VFX for all 7 elements, Phase 2 must specifically hunt for lightning/holy/shadow-themed VFX packs. If only 4 for Phase 0, scope is narrower.

**Clarification needed:** At Reincarnated Phase 0 / Profile A launch, are lightning, holy, and shadow classes planned as shippable? Or are they Phase 2 elements?

---

## Q3: Non-Humanoid Monster Pipeline (AFFECTS TRACK C + E SCOPE)

**Question:** Does the Reincarnated monster generation pipeline target humanoid-only monsters, or do we expect non-humanoid enemy forms?

**Context:** Mixamo is humanoid-only. Non-humanoid monsters (quadrupeds, elemental spirits, multi-limb creatures) cannot be rigged via Mixamo and require a custom rigging workflow (Blender). The `monster_generator.py` exists in the engine source but I did not deep-audit it during this pass.

**Why it matters:** If non-humanoid monsters are in scope for Phase 0, Track C (Mixamo) is insufficient as the sole animation source, and Track E (pipeline) needs a custom-rigging branch scoped and documented. If humanoid-only, the pipeline is simpler.

---

## Q4: VFX Style Register Target (AFFECTS TRACK B QUALITY FILTER)

**Question:** Should VFX procurement target stylized/cartoon register or realistic register?

**Context found:** The ChatGPT→Meshy→Mixamo pipeline naturally produces stylized/semi-realistic outputs depending on the prompt. Cripto289's Realistic Effects Pack 4 is the highest-reviewed VFX pack in the catalog but is in a photorealistic style that may not match Meshy-generated character outputs.

**Recommendation:** Stylized register for VFX, to match expected Meshy character output aesthetic. Photorealistic VFX against stylized characters produces visual incoherence.

**Urgency:** Affects quality filter in Phase 2 VFX catalog expansion (can exclude realistic-register packs from procurement shortlist).

---

## Q5: BC Measurement Scope in Phase 2 — Confirm vs Discover (AFFECTS TRACK A DEPTH)

**Question:** For Phase 2 Track A (internal substrate audit), should I also assess whether the sim telemetry currently supports per-event logging? Or is that gamora's territory?

**Context:** Multiple BC measurement axes require per-event damage-application logging (Axis 3A tempo, Axis 3B variance) that may or may not currently exist in `fight_engine.py` and related sim files. The audit mandate is read-only, so I can survey the sim code but not modify it.

**Recommendation:** Allow legolas to do a quick-pass read of `fight_engine.py` and `fight_result.py` in Phase 2 to confirm presence/absence of per-event logging. This would make Track A substrate assessment more precise and provide gamora with a clearer scope-of-work estimate.

---

## Q6: ARPG Canon Scope for Track D Phase 2

**Question:** Should Phase 2 Track D expand to comprehensive PoE 1 skill gem inventory (~700+ gems), or focus on top-50-per-game depth across D2/D3/D4/Last Epoch/Grim Dawn?

**Context:** PoE 1 has the richest skill geometry variety of any ARPG, with explicit geometry tags in the wiki. A PoE-1-focused Phase 2 Track D pass would likely surface 95%+ of novel geometry patterns. A spread-across-games approach covers more games but with less depth per game.

**Recommendation:** PoE 1 deep pass for Phase 2, supplemented by D4 comprehensive skill tree for a modern design perspective. GD full mastery coverage for the mod-pack-host validation angle.

---

## Q7: Trap Geometry — Un-Defer Decision

**Question:** The ARPG canon shows trap-class skills (PoE Saboteur, D2 Assassin) are signature build-defining mechanics. Our palette defers `trap` due to multi-stage state machine complexity. Is this still the right call for the QD-engine rebuild scope?

**Context:** The QD-engine rebuild scope is 18-26 weeks. If the trap pattern produces meaningfully distinct BC signatures (specifically: Axis 5 generator-spender timing and Axis 2 multi-spawn for detonation), it may be worth including trap geometry in the QD-engine geometry palette expansion.

**Recommendation:** Defer this decision to gandalf after Phase 2 Track D completes. The data to make this decision (how many distinct trap-class builds exist in the canon, what BC signatures they'd produce) will be available after Phase 2.

---

## Note on Methodology Surprises

Two findings from Phase 1 were not anticipated in the commission brief and may affect scope:

**Surprise 1 — Canonical element count is 7, not 4-5.** The dispatch prior was "5-primary core (fire/water/earth/wind/one-other)." The engine actually has 7 rotating substrate identities fully declared. This expands VFX procurement scope if all 7 are Phase 0 targets.

**Surprise 2 — The orbital/rotating projectile geometry pattern is more significant than previously documented.** Blessed Hammer is one of D2's most iconic builds. This geometry type is not representable in our current palette or the 5 BC bins. It's not critical for Phase 0 (we can defer it), but it's worth Matt knowing that one of the ARPG canon's most beloved patterns has no analog in our current system.
