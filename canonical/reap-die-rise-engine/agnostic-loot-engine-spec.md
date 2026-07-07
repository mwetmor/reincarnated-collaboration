# Archetype-Agnostic Loot — ENGINE spec (operator algebra, search + fairness campaign, build contracts)

**STATUS:** CANONICAL SPEC — authored 2026-07-07 (gandalf, SPEC-AUTHOR), absorbing Matt's mobile draft (`matt_notes_handoff_docs/reap-die-rise-agnostic-loot-system.md`, now bannered superseded-by-canon) + the 2026-07-06 review (`agentic_orchestration/gandalf/notes/2026-07-06-agnostic-loot-system-review.md`) + the 2026-07-07 ruling set (C1–C5 · G1 · G2 · G3).
**⚠ BUILD GATE (hard):** the loot **BUILD** fires only after **(i) batch-2 close** (the full kit population — INT cells + summoners — is the fairness sample; operators band-tested against the unfixed caster chassis would mis-band permanently) **and (ii) the redesigned gauntlet instrument** (the 8-mob wall is a **broken instrument** per the 2026-07-07 Step-1 re-derivation — bars 9.90/11.65 exceed the metric's hard cap of 8; 7/8 martial cells saturate at 8.0; design session pending). **This doc is spec, not authorization. Zero compute rides on it.**
**Companion (story half):** `../reap-die-rise-story/agnostic-loot-story-spec.md` — soul-as-lens fiction, gleaning, cementing, soul weapons, naming surfaces. This doc owns the math + the build contracts.
**Open build-gate rulings:** `canonical/matt_decision_needed/README.md` **Q10**.

---

## 1. Operator model (LOCKED — draft §0/§1 adopted)

- **Kits are points; gear is operators.** A kit is a point/region in the mechanic coordinate space; a gear affix is a **function over universal structural axes** — axes present at *every* point — never a reference to a specific ability. Same operator, different emergent behavior per body (**the real-loot criterion**, draft §1.4): that property is what lets gear transfer across reincarnations while remaining genuine loot rather than a stat-skin.
- **Genre receipts:** D3 build-changing legendaries + PoE build-imposing uniques (Mjölner) prove transform-identity is the chase; D3 Legacy-of-Nightmares-era generic "+X% damage" proves value-only gear is a stat-skin. Operators act on **STRUCTURE** (slots, chains, triggers) — the correct answer.
- **Three operator classes, mapped to rarity AND to cost tier (§8):**
  | Class | Rarity | Example | Legibility |
  |---|---|---|---|
  | **Value** | common/low | "+X% magnitude," "−X% cost" | readable, low identity |
  | **Structural** | rare/mid | "primary attack chains +1 target" | readable, mid identity |
  | **Transform** | legendary/set | "cannot use primary; secondaries cost nothing" | abstract, high identity — the chase |
- **Rarity = point richness** (how many latent operators + which class), not a separate stat budget. Marquee legendaries are **fixed authored points**; the mass is **generated** (sampled points). All rarities are agnostic (draft §6.3) — they differ in operator count/class/magnitude, never in class-lock.

## 2. Universal axes + the RESERVED list (C1, ruled 2026-07-06)

**Legal operator vocabulary (universal axes):** resource **cost / pool / regen** · cooldown / cast time / channel · range (per-ability + structural slots: farthest/nearest) · area / radius / shape · target count / chain / pierce / split · magnitude · projectile behavior (speed, count, arc, return) · trigger hooks (on-hit, on-kill, on-cast, on-cooldown-end, on-resource-spend) · structural slots (primary attack, secondaries, movement ability, highest-cost ability).

**RESERVED — empty-by-ruling:** operators over **resource *type*** (e.g., "convert cost to HP" = blood magic by gear; charge-stack grant by gear). These join the three structural cost-TYPE bins (batch-2 spec §8 R1, Matt 2026-07-06) — different sim plumbing, three binding guards; the bins open only at the **F5 re-derivation event**, and the gear vocabulary opens with them, not before. Until then: mana-substrate + live martial economies only.

**Trigger-hook caveat (empirical, 2026-07-06 finding):** **on-crit is not currently universal** — crit is DEX-keyed; INT kits are crit-poor by formula. An on-crit operator would fail §7's coverage test *today*. It enters the legal vocabulary only when a spell-crit channel (F-c family) or equivalent lands. This is the convergence bonus working as designed: the agnostic search and the fairness campaign measure the same substrate truth from two sides.

**Defensive axes — QUEUED C1 EXTENSION (registered 2026-07-07; ruling → Q10):** the ruled vocabulary above is **entirely offense/utility-side** — no max-HP, mitigation (armor), per-element resist, recovery, or avoidance axis. Matt affirmed same-day that gear affixes — defensive included — build out through THIS spec (kit-agnostic; no dual system). Defensive axes pass §1 universality **by construction**: every kit takes damage through the same resolver intake (HP pool, armor factor, `elemental_resistances`, the 7×7 substrate matrix) — defender-side axes are MORE agnostic than element-gated offense (§4). **Empirical warrant (chassis-evidence #1, defense half — tracker fourth entry 2026-07-07):** the F2 calibration cliff (pop WR 0.976 → 0.881 → 0.310 → 0.0 across mob_damage_scale 0.025 → 0.040) shows near-zero effective-HP spread across the certified population — without defensive spread the difficulty dial is binary and no kit carries survivability identity (the tank/glass-cannon archetype axis is absent). **Measurability (load-bearing):** on the dead mob-damage channel every defensive operator had ZERO power-delta — the §7 fairness campaign would have auto-rejected the entire class as sub-noise; the 2026-07-07 lived-channel fix is what makes defensive operators bandable at all, and near the calibrated knife-edge their deltas will band LARGE (genre-true: D2 Hell resist caps are the genre's canonical example of defense as the biggest single power spike). **Proposed shape at ruling:** defensive VALUE operators (max-HP%, per-element resist, armor/mitigation%, recovery on-hit/on-kill via existing trigger hooks) enter the universal list; block/barrier-class grants stage as structural/transform per §8 cost tiers.

## 3. Numbers of record (C2)

The coordinate space of record is **68,040 full lattice / 12,960 live** (BC survey). The draft's "~64K-point decomposition" is a retired myth with no code derivation — do not re-propagate it.

## 4. Trait reconciliation — the kill-test (C3, ruled 2026-07-07: "operator-native or dead")

The 2026-05-12 gear-affix trait architecture is reconciled by reduction, not coexistence:

- **Element-gated trait affixes SURVIVE** as **value operators** — element is a universal gate (every kit has one), so element-conditioned value scaling passes §1's universality rule.
- **Mechanic-gated trait affixes** are re-expressed as **mechanic-GRANTING structural operators** (the gear grants the hook it modifies) **or retired.** A gate on a mechanic only some kits have violates universality; a *grant* of that mechanic is universal by construction.
- **Anything that does not reduce cleanly is RETIRED.** **No dual system** — partial body/partial soul is the worst of both (draft §0; Matt: "I would rather throw the traits away than have them compete with the new system").
- **Intrinsic B9a class traits are UNTOUCHED** — they are body-side (the kit's own progression), not gear. This spec governs the gear channel only.

## 5. Composition algebra (G1 + G2, ruled 2026-07-07)

The **LOADOUT is the unit of play, not the operator** — players wear ~10 slots and the combinatorics forbid brute-forcing ensembles. Rules:

- **Every slot loots.** The game is loot-driven (Matt, ruled); no cap on lootable slots, ever.
- **Value operators:** commute and stack, each within its band. Uncapped.
- **Structural operators:** slot-scoped (each binds to a structural slot; two operators on the same slot compose only per an explicit compatibility table). Uncapped as a class.
- **Transform operators:** slot-exclusive AND **equip-capped at 2–3 simultaneous** (exact number = tuning; Q10). Receipt: D3 wears 13 gear slots but Kanai's Cube caps legendary *powers* at 3 — the cap is on the build-warping class, not on loot. PoE governs support-gem interaction by design rule, not brute force — same move.
- **Bundle validation (G2):** band-pass is per-operator but bundle power-delta ≠ sum of parts. Split: **marquee legendaries are finite authored points → gauntlet them as BUNDLES directly**; the generated mass = few-op items → validate via the **pairwise composition table** (plus a sampled-ensemble sanity ring at loadout level).

## 6. Realized-description contract (C5, ruled — hardened from draft §5.2)

- **Mechanical descriptions are COMPUTED:** a deterministic template render of (item's awake operators × current body × current soul level). Rules text on a player-facing surface is never LLM-paraphrased — an LLM paraphrase of rules risks WRONG rules (D7 AI-tell line).
- **The LLM touches the NAME only** (functional-compression constraint — story spec §7 holds the naming rules) + an optional clearly-subordinate flavor sentence.
- **Persist per-body realized strings only if cheap;** the render is deterministic, so recompute-on-equip is the default contract.

## 7. Search + fairness = ONE gauntlet campaign (merged draft §6+§7)

Draft §6 (agnostic-point search) and §7 (fairness-band validation) are **the same sim runs emitting two statistics** — run one campaign, halve the compute:

- **Relevance** = |power-delta| above the noise floor, per (operator × kit). **Coverage** = fraction of kits above it (agnostic ⇒ high coverage).
- **Fairness** = the same power-delta distribution judged against the band. In-band across (almost) all kits ⇒ ships. Outliers: clamp/condition, exclude regions, or re-tier; broadly out-of-band ⇒ reject.
- **Sample = the batch-2 population.** Do NOT invent a second sampling scheme — Leg C emits exactly the representative kit spectrum (INT cells + summoners included) the band needs.
- **Staged-pilot discipline applies in full:** representative operator sample first, pre-registered GO/HALT criteria, then the sweep. Operators × kits × gauntlet is batch-scale compute.
- **Instrument inheritance (load-bearing; instrument LANDED 2026-07-07):** the campaign runs on the **four-family lived-channel instrument** (`gauntlet-run-beat-families-spec.md` — built, mob-damage channel lived, calibration completing: F3 `boss_damage_scale` third knob + full-pop re-lock pending) — never on the saturated 8-mob wall (a capped metric cannot band anything; 7/8 martial cells pinned at the ceiling means no headroom to measure an operator's delta). **Whatever instrument certifies kits certifies gear.** One instrument, two customers. The lived channel is also what makes the §2 queued DEFENSIVE operators measurable — on the dead channel their power-delta was structurally zero.
- **Provenance law:** **kits vote BARE in the faction derivation** — loot never contaminates the derivation population. Gear validation is downstream instrumentation, full stop.
- **Persisted outputs (draft §7.4, adopted):** per-operator coverage + band pass/fail + clamped/excluded regions + tier; per-rarity validated pools; the **degenerate-combo blacklist** (operator × kit-region), consulted at drop time so the generator never hands a known-broken pairing to the current body.

## 8. Engine build contracts

- **Flattened carried_gear contract (bug-lesson, fixed 2026-07-07):** `carried_gear = {"main_weapon": <binding>}` with **top-level keys** read by `combatant.py:900` (`spell_damage_modifier` etc.). The emission-side declaration that nested `substrate_binding` one level deeper silently zeroed caster pools in persisted rows — found in the HALT investigation, fixed by star-lord (`64289f0`, Gate-2 PASS). The loot build extends THIS flattened contract; schema validation at the boundary is mandatory (Discipline #8).
- **Legacy-channel ABSORPTION rule (inversion-finding consequence, 2026-07-07):** today's near-parity rests on **two opposing legacy asymmetries** — post-Path-α the substrate weapon contributes ~nothing to martials (`base_physical_damage` inert; physical pool reads gear_set only) and ~+88% avg to INT casters (SC-6b `spell_damage_modifier` live). The operator model must **ABSORB both channels into operator vocabulary** (weapon = operator carrier), never stack on top of them — otherwise every band measurement double-counts a ghost. `_DEFAULT_SPELL_MOD_BY_ATTR` + SC-6b live values become value-operator seeds under C4/Track D joint design (rocket + gandalf), not a parallel channel.
- **Soul weapon re-scopes Track D (C4, ruled):** the weapon slot is an **operator carrier with catalogue-substrate identity** (museum/mythic bases via `weapon_knowledge_entries`), re-expressed per body — NOT a base-damage source. ω-penalty (`OMEGA_CROSS_ATTRIBUTE_PENALTY` 0.80) may lose its trigger by construction (cross-attribute wielding becomes impossible); disposition — retire vs re-key to soul-weapon affinity — is a Matt ruling (Q10).
- **Cost tiers (staging by rarity is natural de-risking):** **value** = live today (ability_modifiers percent pools + set bonuses) · **structural** = existing resolver geometry params (chain/fork/multi_projectile) exposed as overrides — moderate · **transform** = new rotation-constraint plumbing in ai_strategies — the expensive tier, built last.

## 9. Sequencing

1. **NOW (done with this doc):** spec canonized; vocabulary + algebra + contracts fixed; open rulings queued (Q9 story / Q10 engine).
2. **Pending, not loot-gated:** batch-2 close (Leg C population + caster chassis fix) · gauntlet instrument redesign (design session — the loot campaign inherits its output).
3. **THEN the build, staged by cost tier:** value → structural → transform; marquee-bundle gauntlets + pairwise composition table per §5; staged-pilot GO/HALT per §7.
4. **Runtime integration (draft §8, adopted):** drop-time color by soul-level glean (story spec §3) · equip/reincarnation-time re-expression + computed realized description (§6) · blacklist consulted per current body.

## 10. What waits on Matt (→ Q10)

Transform-cap exact number (2 vs 3) · fairness-band widths per rarity (legendaries likely wider — build-defining spikes are desirable there) · ω-penalty disposition under soul weapons · **defensive-axes C1 extension** (§2 queued — which defensive value operators enter the vocabulary at v1; gandalf recommends max-HP% / per-element resist / armor% / recovery as the v1 set). None gate current work; all gate the BUILD.

---

**Signed:** gandalf, 2026-07-07. *One instrument, two customers; kits vote bare; the ghost channels get absorbed, not inherited.*
