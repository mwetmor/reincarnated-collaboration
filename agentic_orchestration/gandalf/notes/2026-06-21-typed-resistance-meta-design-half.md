# Design-half — 2026-06-21 — typed-resistance meta for the defensive-axis recal wave

**Type:** gandalf design-half (Stage-0b deliverable of the defensive-axis recal wave)
**Author:** gandalf
**Status:** authored; routes to jack-ryan Gate-1 (DESIGN-MODE) before the MASTER re-draft
**Authority:** rules the DESIGN — typed-offense direction, the resistance-meta (how resistance becomes a choice, not a tax), the gear-resist generation prerequisite's INTENT + definition-of-done, the resolver-route spine, the salvaged-guard re-expression. Does NOT set constants (gamora), does NOT size the rocket generation delta in LOC (rocket sizes against the DoD here).
**Supersedes:** the threat-design-spec's "monster offense is TYPELESS" ruling and my earlier "type-it-later / future-fork" call. Matt LOCKED typed resistances 2026-06-21. This doc is the reversal-of-record (threat-spec §5b amendment in §10 below).

---

## §0 — One line

Monster offense becomes TYPED; the death channel routes through the existing kernel resolver so the kit's real armor/per-element resistances go live on defense; resistance is made a **reward-for-matching against signature-element bosses** (not a mandatory cap) — and the spirit-swap pillar gains a defensive dimension as a result. One bounded generation prerequisite (gear must mint *differentiated* per-element resist) gates the payoff.

---

## §1 — The locked direction (what reverses)

Matt ruled (2026-06-21): **typed resistances are the headline of this wave**, premise "we already have them in kits/gear." This reverses two prior positions of mine, both now amended:

1. The threat-design spec (`2026-06-21-monster-offense-threat-design-spec.md` §2/§4) ruled monster offense **typeless** (heavy-slow magnitude through the flat death channel). **Amended:** monster offense is typed.
2. My Pattern-B answer initially ruled typing a **future fork** (to avoid the homogenization-guard collision). That collision argument was **measured on a false mitigation scenario** (Matt's correction — see §6) and is dropped. The guard's *principle* survives, re-founded on real per-kit defense.

The MASTER dispatch KR is holding (`dispatches/2026-06-21-recal-wave-defensive-axis-MASTER.md`) is built on the superseded flat/typeless spine and **cannot publish as the typed wave.** This doc is the corrected design it re-drafts against.

---

## §2 — The verified substrate (first-hand, this session)

**A. The two combat directions are radically asymmetric.**

| | Player → Monster (offense) | Monster → Player (death channel) |
|---|---|---|
| Path | `damage_resolver.resolve_skill` (kernel truth), routed when `combatant_state` populated (`spatial_engine.py:533-534`) | bespoke flat branch (`spatial_engine.py:1951`) |
| Typed? | **Fully** — physical → `compute_physical_damage(mag, scaling, defender.armor)` (`damage_resolver.py:456/460`); element → `res = defender.elemental_resistances.get(element, 0.0)` → `compute_elemental_damage` (`:478/485`); **plus a 7×7 attacker-sub × defender-sub matrix** (`:502`) | **No** — `dmg = raw × (1.0 - self.player.armor_factor)`, a single scalar |
| Player defensive stat | the kit's real armor/resist (carried on `combatant_state`) | a **flat global constant** — `PLAYER_ARMOR_FACTOR_VS_BOSS` / `_VS_STANDARD`, set per-scenario at `spatial_engine.py:1575-1578` / `:2390`, **overriding the kit's roll** |

So the kit's defensive build is **inert on defense** in the spatial sim today. Player *death* is a function of (HP, global knob, kill-speed) — two kits with identical HP and opposite defensive builds die identically. That is not a defensive axis; it is HP-and-kill-speed wearing a defense costume. The substrate **already fully supports typed damage** — it is live, right now, on the player's *offense* (the monster is a typed resolver DEFENDER: `spatial_engine.py:2454-2460`, `spatial_resolver_adapter.py:232-233`; Phase-4 armor-symmetric floored at `combatant.py:1142`). It simply was never wired on the monster→player direction (mobs carry `resolver_skills=[]` — not attackers — `spatial_engine.py:2508`).

**B. The kit resistance surface is THIN and UNDIFFERENTIATED — the load-bearing gap.**

- The production aggregation **preserves** per-element differentiation: `combined_stats()` sums `s.elemental_resistances.items()` keeping element keys (`gear_schema.py:252-253`), and that flows to the sim combatant (`combatant.py:566/575/926`) and into the resolver (`damage_resolver.py:478`). **The plumbing on both ends is ready.**
- But the **main gear roll path emits empty** resistances (`gear_generation.py:943-972` — no effect branch populates the dict).
- Every path that *does* populate resist spreads an aggregate **evenly across all four elements** (`keystone_loadout_materializer.py:275-279` `resist_total/4`; `gear_catalog.py:188-190`) — and the keystone projection is explicitly "NOT wired into the sim / diagnostic" (`:256-259`).
- The `element_resistance` modifier category EXISTS with a real range — `(-1.0, 0.80)`, negative = vulnerability, 80% max (`gear_instance_generator.py:66`), fed by `respen_per_element_resist` (`:487`) — but it is **not minted into differentiated, element-keyed per-instance GearStats**.
- The endgame boss the wave targets carries `elemental_resistances={}` and `"skills": []` (`t4_sim_cycling.py:1016`, `:1082`).

**Conclusion:** today's kits have *"more all-resist vs less all-resist"* — D3 Resist-All blended toughness — **not** *"fire-resistant vs water-resistant"* per-element identities. **Typing monster offense into an even-spread/empty resist surface buys nothing** a single armor number wouldn't: the resolver would run the same `res` for every element. Typed resistance is worth the complexity ONLY if kits can build toward *specific* elements. That differentiation is the prerequisite (§4).

---

## §3 — THE DESIGN RULING: signature-element bosses + reward-for-matching (not a tax)

The genre's typed-resistance failure mode is the **mandatory cap**: D2 Hell starts you at −100% all-res and 75%-cap-or-die makes resistance a checkbox, not a choice; PoE's "resistance tax" is the community name for *you must hit 75/75/75 before the build functions.* D4's launch resistances were reworked wholesale for the same disease. The blended escape (D3 Resist-All) is what we have now, and it has no identity. **We want the D2/PoE resistance *identity* without the D2/PoE *tax*.** The ruling:

1. **Signature element per trial-boss.** Each boss carries a KNOWN elemental identity (the fire boss does fire) — telegraphed, part of its gallery identity. This is the structural gift the trial-boss gallery gives us that PoE lacks: in PoE you blind-cap because content is randomized; in a **known-boss gallery you build against a named threat.** That alone converts "cap everything" into "prepare for this fight."

2. **Resistance is a strong REWARD for matching, never a GATE.** A kit that matches (high fire-res vs the fire boss) gets a meaningfully easier fight — more margin, more forgiveness. A kit that does NOT match still has a path: **survive by playing well** (kite the heavy-slow telegraphed slam, kill fast — offense/position substitutes, per §6). Harder, not impossible. **No hard cap that becomes the floor.** Resistance is a continuous margin lever, not a binary safe/dead switch.

3. **The magnitude band (gamora's typed re-derivation target):** tuned so the resist lever moves the boss from *"hard but doable"* (unmatched) to *"comfortable"* (matched) — NEVER from *"impossible"* (unmatched one-shot) to *"trivial"* (matched faceroll). Even at max matching resist (80% single-element ceiling) the boss is a real fight; even at zero matching resist the boss is survivable-by-skill. This is the typed analog of the glass-0.6–0.8 / bruiser-0.95 spread.

4. **THE THEMATIC PAYOFF — spirit-swap gains a defensive dimension.** The form library lets the player bring a *different form* to each boss. Typed resistance makes form-selection a **defensive read against the boss's signature element** — bring the water-attuned form to the fire boss. The "resistance build" stops being gear-grinding for 75/75/75 and becomes **"bring the right form to the known fight"** — which IS the game's core loop (form accumulation → form selection per trial). This converts the genre's most-resented chore (the resistance tax) into an expression of our most load-bearing pillar (spirit-swap, confirmed-load-bearing per design intent). Typed offense doesn't just add a defensive axis; it gives the form-swap a reason to exist on defense. **This is why Matt's call is right** — but it is entirely contingent on differentiation (§4); even all-resist forms make the defensive read meaningless (every form resists everything equally).

   **§3.4-VERIFIED (2026-06-21, gandalf first-hand at publish-go) — the payoff splits into two halves; record the split honestly.** `grep -rln elemental_resistance` across `foundation/`, the class-definition path, and `spirit_guide/` returns NOTHING — **no form/class carries an intrinsic `elemental_resistances` field.** Resist lives only on gear, monsters, trials. Player resist is 100% gear-sourced (`combatant.py:566` `combined_stats()` → `:575` → `:926`). Consequence:
   - **Offense half — form-intrinsic, lands this wave.** Typed skills travel WITH the form; swapping form swaps the offensive elemental identity. "Bring the right form" is literally true on offense via the 7×7 matrix. The dominant half, and real.
   - **Defense half — GEAR-mediated today, NOT form-intrinsic.** "Bring the form that *resists* fire" is mechanically "equip fire-resist gear" (equippable on any form). Typed DEFENSE still goes fully live this wave (the resolver-route makes the kit's gear-resist load-bearing for the first time) — it just reads off the gear, not the form.
   - **WATCH-ITEM, not a blocker.** The wave delivers the full payoff in gear terms. DEFERRED follow-on lever: should forms carry an intrinsic defensive elemental identity? (D2 immunities were monster-side; PoE resistance gear-side; *form-side* defensive identity would be genuinely ours.) Additive, earns its way in on typed telemetry — NOT part of soldering this seam. Do not bolt a second net-new generation surface onto a wave that already has one (§4).

---

## §4 — The gear-resist GENERATION PREREQUISITE (scoped; rocket sizes against this DoD)

**Why it is a prerequisite:** §3.4's payoff and the entire typed direction require kits/forms to carry *differentiated* per-element resist. §2.B shows they do not today. Schema + aggregation + sim consumption are READY; only the minting is missing. This is a bounded "solder the middle" gap (the same texture as the gen→sim proxy seam), not a resistance-system rebuild.

**Definition of done (DESIGN intent — rocket owns implementation + sizing):**

- [ ] A piece of gear can roll resist toward a **specific element** (e.g. `{"fire": 0.30}`), not an even spread across all four. The `element_resistance` modifier category (`gear_instance_generator.py:66`, range −1.0..0.80) is the existing magnitude source; mint it onto per-instance `GearStats.elemental_resistances` with the **element key preserved.**
- [ ] Differentiation survives to the sim combatant unchanged — verifiable end-to-end: a kit built with a fire-weighted loadout shows higher `elemental_resistances["fire"]` than other elements at `combatant.elemental_resistances` (the path is already non-lossy per `gear_schema.py:252-253` → `combatant.py:575/926`).
- [ ] A kit can **build a defensive elemental identity** — i.e., reach a meaningful resist in one element by choice, not be stuck at uniform all-resist. *Source is GEAR* (per §3.4-VERIFIED: no form-intrinsic resist exists today; this DoD is gear-expressed). The 80% single-element ceiling is the existing cap; the design wants the *spread* (matched element well above unmatched), not necessarily the ceiling.
- [ ] **Anti-tax constraint on generation:** do NOT make broad all-element resist trivially stackable to the point that "cap everything" dominates "match the fight." The signature-boss design (§3.1) only works if specializing into the boss's element is a *better* defensive return than spreading thin. (This is a generation+calibration joint constraint; gandalf+gamora converge on the exact shape.)

**Confirm rocket runs at build (sizes the delta):** trace whether `element_resistance` partition modifiers already carry a target element that the per-instance GearStats build simply drops, vs. whether the element assignment itself must be added. The former is a "preserve through the per-instance build" fix (small); the latter adds element selection to the roll (medium). Either way the schema/aggregation/sim are unchanged.

**Out of scope:** changing the 80% ceiling, the resolver mitigation curve, or the substrate matrix. The prerequisite is *minting differentiated per-element resist*, nothing downstream of it.

---

## §5 — The resolver-route spine (recompose-first) + flat-anchor invalidation

**The spine (engine):** route the monster→player death channel through `damage_resolver.resolve_skill` with the **player as a real DEFENDER**, reusing the same resolver the offense side already uses (`spatial_engine.py:533-534`). The resolver reads everything off a generic `defender` (`armor`, `elemental_resistances`, `block_value`, `substrate`, `status_resist`) — defender-agnostic by construction — and the production player entity already carries its real mitigation on `combatant_state` (currently ignored on defense). The mob becomes a resolver ATTACKER (it currently carries `resolver_skills=[]`), which composes with the rocket typed-skill emission. This:

- makes the kit's defense live (a bruiser's armor saves it; a glass cannon's thin armor gets it killed);
- collapses the asymmetry onto ONE damage path (no flat-branch / resolver dual-maintenance);
- makes typed-vs-untyped a **content property** (the `element` field on the monster skill), not an engine fork.

**Flat anchor is INVALID under this spine.** The MASTER's constraint-1 anchor (`MOB_DAMAGE_SCALE=4.0`, `PLAYER_ARMOR_FACTOR_VS_BOSS≈0.76`) was fit to the flat equation `raw × (1 − 0.76)`. The resolver uses entirely different mitigation curves (`compute_physical_damage` armor curve; `compute_elemental_damage` resist curve; substrate matrix). **Magnitude must be re-derived from scratch** under the resolver. The flat anchor is, at most, a starting intuition — not a knob-set. The `PLAYER_ARMOR_FACTOR_*` constants are likely **retired or repurposed** (the kit now provides mitigation; any boss-harder-than-trash scaling moves to the monster attack-magnitude side).

---

## §6 — The salvaged homogenization guard, re-expressed for typed defense

The guard as previously measured (the fast-cadence sweep) held the **flat global armor constant fixed** — so it tested HP-vs-kill-speed, never kit-defense-vs-kill-speed (Matt's correction). That measurement cannot adjudicate the typed-defense decision, and the "typing collides with the guard" argument is **dropped.** What survives is the guard's **principle** — *no mandatory defensive checkbox* — re-founded on real per-kit typed defense:

**Re-founded acceptance criterion:** at the chosen production knob-set, an **under-resisted kit must survive the signature-element boss by playing well** (kiting the heavy-slow telegraphed threat / killing fast — offense and position substitute for matched resistance), while a **matched kit survives more comfortably.** If the only way to survive is to match-cap the element, the knob-set FAILS (that is the PoE tax). Two viable paths — *match the element* OR *out-play the unmatched fight* — or reject the knob-set. Re-run on real typed per-kit defense, not inherited from any flat sweep.

---

## §7 — Swarm / clear-shell elemental treatment (keeps trash < boss)

The boss is the **peak elemental-decision point** (signature element, matching matters most). Swarm/clear-shell mobs carry **minor / mixed** elemental damage (broad resist helps a little) — NOT a per-element resist-check, which would re-import the D4 "every white mob is a threat" tax and risk inverting trash<boss. So: **boss = signature element (matching is the decision); trash = minor/mixed (broad resist mildly helps).** The threat-design-spec's trash<boss ordering and per-hit-variance swarm lever (§3) are preserved; typing the swarm is intentionally *shallow.* Clear-shell death stays rare-by-design and boss-only-fallback remains the logged escape if no guard-respecting clear-shell mechanism lands.

---

## §8 — Per-seam buildable handoff

**rocket** — (a) the §4 gear per-element-resist minting (the prerequisite — confirm the delta size first); (b) typed *resolver-attacker* monster skills: `element` + magnitude + `scaling_stat` + `substrate` (so `resolve_skill` processes them), each boss carrying its **signature element**, on the heavy-slow boss shape (threat-spec §2); swarm minor/mixed (§7). Geometry still constrained to wired `{point, circle, line, cone}` (threat-spec §1). MIGRATION.md (gen→sim).

**gamora** — (a) the §5 resolver-route spine (player as defender; mob as attacker); (b) **re-derive magnitude from scratch** under the resolver (flat anchor invalid, §5); (c) the §3.3 typed band (unmatched hard-but-doable / matched comfortable; no unmatched one-shot, no matched faceroll); (d) re-found the §6 guard on typed per-kit defense; (e) two-axis joint re-rate (unchanged from MASTER constraint 7/8). Seed hygiene: disjoint base (MASTER assigns 47M+). Math-before-code on the resolver mitigation curves before the sweep.

**star-lord** — additive telemetry: **death-cause WITH element / damage-by-type** (richer than the typeless version — needed to tune the typed band and verify matching matters). Additive only; MIGRATION.md; round-trip smoke.

**jack-ryan** — Gate-1 this design-half (DESIGN-MODE); then Gate-1 the re-drafted MASTER; Gate-2 each build.

---

## §9 — Stage-0 de-risks (gate the MASTER re-draft)

Two parallel, both BEFORE the full build commits (empirical-criterion-before-commit):

- **0a — gamora resolver spike:** does `resolve_skill` cleanly accept **player-as-defender + mob-as-attacker** (substrate both sides, no mob-shaped assumptions)? Throwaway typed mob; same pattern as the proxy de-risk spike. If it does not route cleanly, the §5 spine changes and the re-draft would be wasted — so this gates it.
- **0b — this design-half (gandalf) + the §4 confirm-trace:** authored; routes to jack-ryan Gate-1. The §4 confirm (preserve-vs-add element selection) sizes the gear prerequisite.

On 0a PASS + 0b Gate-1 PASS, KR re-drafts the MASTER around §5/§4/§3/§6/§7. **Hold publish on the current MASTER until then.**

---

## §10 — Threat-design-spec amendment (§5b — reversal of record)

The threat-design spec (`2026-06-21-monster-offense-threat-design-spec.md`) §2/§4 ruled monster offense typeless and §5 named typed-offense a *future fork*. **Amended this date:** typed offense is the CHOSEN direction (Matt-locked). The §5 positional-avoidance ruling (recompose-first, no dodge model) is UNCHANGED — typing is orthogonal to avoidance. The heavy-slow boss shape and light-variance swarm shape are UNCHANGED — typing is a property layered on the same shape. Only the typeless ruling reverses.

---

## §11 — Player consequence

A player walks into the fire-boss trial. They KNOW it is fire (gallery identity, telegraphed). They have a choice with teeth: bring the water-attuned form (comfortable margin), bring a glass form and out-play the telegraphed slams (tense but doable), or bring a mismatched tank and grind it (slow but safe). No form is locked out; the *right* form is rewarded. Death is real, per-kit, and legible — "I died because I brought the wrong form / didn't dodge the slam," never "I died because I hadn't farmed 75% fire-res." That is the D2 resistance *identity* (build for the fight) routed through the spirit-swap pillar (the form IS the build) and stripped of the PoE *tax* (no mandatory cap). The defensive axis the recal restores is, finally, the *kit's* axis — not a global constant's.

---

## References

- Encounter-model ruling (nine constraints, SHAPE): `2026-06-21-defensive-axis-recal-encounter-model-ruling.md`
- Threat-design spec (heavy-slow boss / variance swarm; amended §5b here): `2026-06-21-monster-offense-threat-design-spec.md`
- Superseded MASTER (flat/typeless spine): `dispatches/2026-06-21-recal-wave-defensive-axis-MASTER.md`
- Calibration diagnostic + Gate-2 (flat-model anchor, now invalid for the resolver): `defensive-axis-calibration-diagnose-2026-06-21.md`; `qa/findings/2026-06-21-defensive-axis-calibration-diagnose-gate2.md`
- Proxy de-risk spike (the spike pattern + the allegiance-flip precedent): `2026-06-21-proxy-combat-decision-packet.md`
- Engine — death channel (typeless): `spatial_engine.py:1951`; player flat constant `:1575-1578/:2390`; offense resolver route `:533-534`; mob-as-defender `:2454-2460`; mob `resolver_skills=[]` `:2508`
- Engine — resolver typed paths: `damage_resolver.py:456/460/478/485/502`
- Gen — resist surface: empty main path `gear_generation.py:943-972`; even-spread projections `keystone_loadout_materializer.py:275-279` / `gear_catalog.py:188-190`; non-lossy aggregation `gear_schema.py:252-253`; modifier category+range `gear_instance_generator.py:66/487`; player combatant resist source `combatant.py:566/575/926`
- Gen — endgame boss empty + skill-less: `t4_sim_cycling.py:1016/1082`
