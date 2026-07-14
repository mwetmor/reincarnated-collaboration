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

**The vocabulary IS the register (reframe, Matt 2026-07-13).** Operators are *moves along the 13 Class-A coordinates* of the kit-identity key (`coordinate-register-2026-07-13.md` §2). This is load-bearing: **gear paths the genre's *own* canonical axes and invents none.** A kit is a point on the 13 axes; an operator nudges it along one. That is simultaneously the anti-inflation guarantee (no operator may reference a mechanic absent from the register) and the meaningfulness guarantee (gear is what unlocks the genre's canonical texture, so gear matters) — Matt's "path existing ARPG-canonical mechanics into gear at just the right density, and tack on nothing above the kits."

**Legal operator vocabulary, mapped to the register axis each moves:** resource **cost / regen** (#7 economy) · cooldown · cast time (#10 tempo, #11 commit) · range + structural slots farthest/nearest (#9 range) · area / radius / shape (#4 geometry) · target count / chain / pierce / split (#4 geometry, #8 proxy) · magnitude (value-tier, axis-agnostic) · projectile behavior — speed, count, arc, return (#2 delivery, #4 geometry) · cast-while-moving (#1 movement) · activation trigger hooks — on-hit, on-kill, on-cast, on-cooldown-end, on-resource-spend (#12 activation) · defensive axes (#6 defense — see the C1-extension ruling below) · structural slots (primary attack, secondaries, movement ability, highest-cost ability).

**RESERVED — empty-by-ruling:** operators over **resource *type*** (e.g., "convert cost to HP" = blood magic by gear; charge-stack grant by gear). These join the three structural cost-TYPE bins (batch-2 spec §8 R1, Matt 2026-07-06) — different sim plumbing, three binding guards; the bins open only at the **F5 re-derivation event**, and the gear vocabulary opens with them, not before. Until then: mana-substrate + live martial economies only. (Upstream authority for the economy axis is the register's coord-#7 carve — `coordinate-register-2026-07-13.md` §3B: economy *model* is Class-A keyed; resource *name* is 1:1-preserved verbatim from source, out of the key; the 174 econ-`gap` kits are exactly what these F5 bins will natively cost.)

**Trigger-hook caveat (empirical, 2026-07-06 finding):** **on-crit is not currently universal** — crit is DEX-keyed; INT kits are crit-poor by formula. An on-crit operator would fail §7's coverage test *today*. It enters the legal vocabulary only when a spell-crit channel (F-c family) or equivalent lands. This is the convergence bonus working as designed: the agnostic search and the fairness campaign measure the same substrate truth from two sides.

**Defensive axes — RULED C1 EXTENSION (registered + ruled 2026-07-07):** the ruled vocabulary above is **entirely offense/utility-side** — no max-HP, mitigation (armor), per-element resist, recovery, or avoidance axis. Matt affirmed same-day that gear affixes — defensive included — build out through THIS spec (kit-agnostic; no dual system). Defensive axes pass §1 universality **by construction**: every kit takes damage through the same resolver intake (HP pool, armor factor, `elemental_resistances`, the 7×7 substrate matrix) — defender-side axes are MORE agnostic than element-gated offense (§4). **Empirical warrant (chassis-evidence #1, defense half — tracker fourth entry 2026-07-07):** the F2 calibration cliff (pop WR 0.976 → 0.881 → 0.310 → 0.0 across mob_damage_scale 0.025 → 0.040) shows near-zero effective-HP spread across the certified population — without defensive spread the difficulty dial is binary and no kit carries survivability identity (the tank/glass-cannon archetype axis is absent). **Measurability (load-bearing):** on the dead mob-damage channel every defensive operator had ZERO power-delta — the §7 fairness campaign would have auto-rejected the entire class as sub-noise; the 2026-07-07 lived-channel fix is what makes defensive operators bandable at all, and near the calibrated knife-edge their deltas will band LARGE (genre-true: D2 Hell resist caps are the genre's canonical example of defense as the biggest single power spike). **✓ RULED (Matt, 2026-07-07 — as recommended, five lines):** **(1)** defensive VALUE operators enter the universal list: **max-HP% · per-element resist · armor/mitigation% · recovery**; **(2)** block/barrier/shield-grant class is NOT value-tier — stages as **structural/transform** per §8 cost tiers; **(3)** **avoidance/dodge-chance is OUT at v1** — dodge is the piloted Godot layer (the one legitimate layer-handoff); a sim-side dodge stat double-counts with player-piloted dodge and muddies pilot-attribution (bands are `pilot_policy`-stamped); re-enters when the Godot combat layer scopes and a pilot re-derivation event fires; **(4)** recovery hook shapes: **on-kill + on-hit IN** (existing trigger hooks; on-kill is KPM-coupled and self-balances in swarm families), **flat passive regen OUT** — H3 measurement showed regen already races mob chip near the calibrated knife-edge; a flat-regen operator stacks on that race and bands unstable; **(5)** defensive operators band in the **same §7 fairness campaign** as offense — no second instrument; the cert bars already encode survival (WR floors, F4 exit-rate).

### 2.1. TEXTURE vs CORE-COMPETENCY — the dilution guard (ruled 2026-07-13)

Matt's worry: *"if all kits can gain proxy or control/ailments, what is the point of playing a kit that specializes? That dilutes the value of cells if those cells' kits must unlock their core competencies while any kit can do the same."* The answer classifies every register coordinate as **CORE-COMPETENCY** or **TEXTURE** and gates gear by the class.

- **CORE-COMPETENCY (cell-defining):** #5 control-specialization · #8 proxy/summon density · #2 delivery-type. These *are* the cell's identity — what a player picks the cell *for*.
  - **Owner:** gear may **amplify your own** core along a scaling axis (control-effectiveness; minion count/quality). The specialist's reward for specializing.
  - **Non-owner:** the core may appear ONLY as **capped-garnish** — hard-capped, low-potency (a 5% freeze-on-hit; 1–2 static, non-scaling pets), never at the specialist's scaling tier. **Import no one's core.**
- **TEXTURE (not cell-defining):** #1 movement · #3 amplitude · #4 geometry · #6 defense · #7 cost-reduction · #9 range · #10 tempo · #11 commit · #12 activation-trigger · #13 dependency. Any kit may path-unlock texture as a build choice; pathing it dilutes nothing, because it was never what the cell was *for*. **Path texture to anyone.**

This is the register's full gear law (`coordinate-register-2026-07-13.md` §3A.1): **amplify your own · path texture to anyone · import no one's core · invent nothing.**

### 2.2. Coverage-fills authorized against the classification (2026-07-13)

Three vocabulary additions, each classified:
- **#1 cast-while-moving — free texture.** Universal; any kit may equip. (Genre receipt: PoE movement/Inspiration build layer; D4 cast-while-moving affixes.)
- **#5 control-on-hit — capped-garnish only.** A non-controller may equip a *hard-capped* control garnish (e.g. 5% freeze-on-hit); it never reaches a control-specialist's effectiveness scaling. Owners amplify their own.
- **#8 minions — amplify-for-owners + capped-garnish for others.** A heavy/light-proxy owner gets scaling minion operators (count/quality); a non-owner may equip only 1–2 static, non-scaling pets as garnish.

### 2.3. The 3-layer compounding guard (ruled 2026-07-13 — answers "capped-garnish may compound over the cap")

Matt's final contingency: capped-garnish control + capped-garnish proxy across gear AND skills may **compound past the cap.** Guarded in three layers, **capping the EFFECT (aggregate), never the SOURCE (per-piece)** — per-source caps compound by definition; the genre caps the aggregate (D2's 75% resist cap, PoE's action-speed floor, D4's CC diminishing returns):

1. **Qualitative moat (design-time — compounding-PROOF, the load-bearer).** The specialist owns a *scaling axis structurally unreachable by garnish.* Control-effectiveness operators are **amplify-your-own-core** — a damage kit literally cannot equip them (no core control to amplify). Minion-*scaling* is **heavy-proxy-exclusive.** Random→reliable and static→scaling are **phase changes, not magnitude** — no quantity of garnish crosses a phase boundary. Because the moat is qualitative, garnish cannot compound *into* the specialist tier no matter how much stacks.
2. **Tiered aggregate cap (band-time).** ONE cap on **intrinsic + ALL gear summed** (never per-piece), tiered by the kit's own #5 treatment / #8 density: a non-owner's garnish ceiling sits **below** the specialist floor, and the tiers never cross. Cap VALUES = band-time ruling (like the §7a resist caps) → Q10 band-sheet.
3. **Adversarial search + blacklist (validation-time).** §7a "the optimizer is the auditor" red-teams compounding stacks pre-ship: any garnish+skill combo climbing toward specialist-grade is an *optimum* the search finds, landing on the degenerate-combo blacklist / clamp / re-tier ladder.

**Population warrant (why safe):** control is rare in the corpus (31/470, 6.4%); double-intrinsic-core (control **and** heavy-proxy) is **exactly 1 kit.** Specialist tiers are sparse and well-separated; garnish crowding into them is a narrow, searchable risk, not a population-wide leak.

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
- **Transform operators:** slot-exclusive AND **equip-capped at 2 at v1 (✓ RULED Matt 2026-07-07); raises to 3 ONLY when the §7a adversarial audit is live.** Rationale: at cap 2, transform interactions are *exactly* covered by the pairwise composition table — zero uncovered higher-order risk; cap 3 introduces triples only the optimizer stratum can audit. The third slot is earned by the audit instrument, not granted on faith. Receipt: D3 wears 13 gear slots but Kanai's Cube caps legendary *powers* at 3 — the cap is on the build-warping class, not on loot (and D3's power pool was hand-authored; ours is generated). PoE governs support-gem interaction by design rule, not brute force — same move.
- **Bundle validation (G2):** band-pass is per-operator but bundle power-delta ≠ sum of parts. Split: **marquee legendaries are finite authored points → gauntlet them as BUNDLES directly**; the generated mass = few-op items → validate via the **pairwise composition table** (plus a sampled-ensemble sanity ring at loadout level).

## 6. Realized-description contract (C5, ruled — hardened from draft §5.2)

- **Mechanical descriptions are COMPUTED:** a deterministic template render of (item's awake operators × current body × current soul level). Rules text on a player-facing surface is never LLM-paraphrased — an LLM paraphrase of rules risks WRONG rules (D7 AI-tell line).
- **The LLM touches the NAME only** (functional-compression constraint — story spec §7 holds the naming rules) + an optional clearly-subordinate flavor sentence.
- **Persist per-body realized strings only if cheap;** the render is deterministic, so recompute-on-equip is the default contract.

## 7. Search + fairness = ONE gauntlet campaign (merged draft §6+§7)

Draft §6 (agnostic-point search) and §7 (fairness-band validation) are **the same sim runs emitting two statistics** — run one campaign, halve the compute:

- **Relevance** = |power-delta| above the noise floor, per (operator × kit). **Coverage** = fraction of kits above it (agnostic ⇒ high coverage).
- **Fairness** = the same power-delta distribution judged against the band. In-band across (almost) all kits ⇒ ships. Outliers: clamp/condition, exclude regions, or re-tier; broadly out-of-band ⇒ reject. **Band-width STRUCTURE ✓ RULED (Matt 2026-07-07): monotone widening by rarity** — common tightest → legendary widest (build-defining spikes belong at the top); exact widths are derived from the campaign's **measured noise floor** and returned as a **band-sheet for one-shot Matt ratification** (numbers before distributions = calibrating in the dark; the same discipline that vindicated the casters).
- **Sample = the batch-2 population.** Do NOT invent a second sampling scheme — Leg C emits exactly the representative kit spectrum (INT cells + summoners included) the band needs.
- **Staged-pilot discipline applies in full:** representative operator sample first, pre-registered GO/HALT criteria, then the sweep. Operators × kits × gauntlet is batch-scale compute.
- **Instrument inheritance (load-bearing; instrument LANDED 2026-07-07):** the campaign runs on the **four-family lived-channel instrument** (`gauntlet-run-beat-families-spec.md` — built, mob-damage channel lived, calibration completing: F3 `boss_damage_scale` third knob + full-pop re-lock pending) — never on the saturated 8-mob wall (a capped metric cannot band anything; 7/8 martial cells pinned at the ceiling means no headroom to measure an operator's delta). **Whatever instrument certifies kits certifies gear.** One instrument, two customers. The lived channel is also what makes the §2 queued DEFENSIVE operators measurable — on the dead channel their power-delta was structurally zero.
- **Provenance law:** **kits vote BARE in the faction derivation** — loot never contaminates the derivation population. Gear validation is downstream instrumentation, full stop.
- **Persisted outputs (draft §7.4, adopted):** per-operator coverage + band pass/fail + clamped/excluded regions + tier; per-rarity validated pools; the **degenerate-combo blacklist** (operator × kit-region), consulted at drop time so the generator never hands a known-broken pairing to the current body.

### 7a. Combinatorial boundability (registered 2026-07-07 — answers the Matt worry: "un-boundable as we compare all kits × all gear combinations vs all others")

The naive cross-product — kits × loadout-combinations *vs* kits × loadout-combinations — **never runs; it is forbidden and bounded by construction**, in four layers:

1. **Forbidden by provenance law (§7 above):** kits vote BARE — the kit-vs-kit matchup matrix (counter-breadth gate, ~24×24 grouping level) NEVER sees gear. Gear is only ever measured against the gauntlet CONTENT bars, never against other geared kits. The geared-vs-geared cross-product is not expensive — it is *illegal*.
2. **Bounded by marginal banding:** operators certify by per-(operator × kit) power-delta on the batch population — linear in operators, never exponential in loadouts.
3. **Bounded by composition law (§5):** transform equip-cap 2–3 caps interaction depth in the one build-warping class; structural operators are slot-scoped with an explicit compatibility table; the generated mass validates via the pairwise table — O(ops²), not O(2^ops).
4. **The residual interaction space is SEARCHED, not enumerated** — this is the piece §5's "sampled-ensemble sanity ring" gestured at, now specified as **three strata:**
   - **(a) Marginal baseline** — the §7 campaign itself (per-operator, all kits).
   - **(b) ADVERSARIAL SEARCH — "the optimizer is the auditor."** Per kit-chassis (the ~24 grouping representatives), a budget-bounded loadout optimizer (hill-climb/genetic over legal loadouts) climbs toward maximum power-delta. Degenerate combos are *optima*; optimizers find optima — this is precisely the answer to "not just the perceived best choices": we do not trust designer perception, we run the search players' theorycrafters would run, BEFORE emission. Genre receipt: GGG outsources this search to the PoE player-base and nerfs after discovery; D3 shipped its LoN/WW discoveries the same way. We own the sim — we red-team pre-ship. Findings land on the **degenerate-combo blacklist / clamp / re-tier** ladder (remediation-first — adjust the operator band, never reject the kit).
   - **(c) Stratified random ensembles** — coverage statistics over the mid-space (the sanity ring, kept).
   - **Budget receipt (measured):** re-pilot rate ≈ 36 fights/s single-process (42 kits × 98 fights in 114 s). Marginal banding ~60 ops × 24 chassis × 98 ≈ 141k fights ≈ ~1 h; adversarial search at 2k fights/kit × 400 kits ≈ 800k fights ≈ ~6 h, embarrassingly parallel. **Boundable.**
5. **One topology leak, guarded:** gear that bends the counter matrix (per-element resist operators — the licensed matchup-bender) could stack a bare-certified kit into effective immunity and manufacture an A-failure (counters-everything) at runtime. Guard = **resist/mitigation CAPS** (D2's 75% resist cap is the genre's canonical answer). Cap VALUES = band-time Matt ruling (→ Q10).

## 8. Engine build contracts

- **Flattened carried_gear contract (bug-lesson, fixed 2026-07-07):** `carried_gear = {"main_weapon": <binding>}` with **top-level keys** read by `combatant.py:900` (`spell_damage_modifier` etc.). The emission-side declaration that nested `substrate_binding` one level deeper silently zeroed caster pools in persisted rows — found in the HALT investigation, fixed by star-lord (`64289f0`, Gate-2 PASS). The loot build extends THIS flattened contract; schema validation at the boundary is mandatory (Discipline #8).
- **Legacy-channel ABSORPTION rule (inversion-finding consequence, 2026-07-07):** today's near-parity rests on **two opposing legacy asymmetries** — post-Path-α the substrate weapon contributes ~nothing to martials (`base_physical_damage` inert; physical pool reads gear_set only) and ~+88% avg to INT casters (SC-6b `spell_damage_modifier` live). The operator model must **ABSORB both channels into operator vocabulary** (weapon = operator carrier), never stack on top of them — otherwise every band measurement double-counts a ghost. `_DEFAULT_SPELL_MOD_BY_ATTR` + SC-6b live values become value-operator seeds under C4/Track D joint design (rocket + gandalf), not a parallel channel.
- **Soul weapon re-scopes Track D (C4, ruled):** the weapon slot is an **operator carrier with catalogue-substrate identity** (museum/mythic bases via `weapon_knowledge_entries`), re-expressed per body — NOT a base-damage source. ω-penalty (`OMEGA_CROSS_ATTRIBUTE_PENALTY` 0.80): **✓ RULED (Matt 2026-07-07) — RETIRE-by-construction.** C4 removes its trigger entirely (weapon = operator carrier re-expressed per body; cross-attribute wielding impossible). Re-keying to "soul-weapon affinity" was rejected — inventing a mechanic to preserve a penalty nobody would feel is a solution seeking a problem. **Tripwire:** if Track D ever re-opens cross-attribute wielding, this disposition re-opens with it.
- **Cost tiers (staging by rarity is natural de-risking):** **value** = live today (ability_modifiers percent pools + set bonuses) · **structural** = existing resolver geometry params (chain/fork/multi_projectile) exposed as overrides — moderate · **transform** = new rotation-constraint plumbing in ai_strategies — the expensive tier, built last.

## 9. Sequencing

1. **NOW (done with this doc):** spec canonized; vocabulary + algebra + contracts fixed; open rulings queued (Q9 story / Q10 engine).
2. **Pending, not loot-gated:** batch-2 close (Leg C population + caster chassis fix) · gauntlet instrument redesign (design session — the loot campaign inherits its output).
3. **THEN the build, staged by cost tier:** value → structural → transform; marquee-bundle gauntlets + pairwise composition table per §5; staged-pilot GO/HALT per §7.
4. **Runtime integration (draft §8, adopted):** drop-time color by soul-level glean (story spec §3) · equip/reincarnation-time re-expression + computed realized description (§6) · blacklist consulted per current body.

## 10. What waits on Matt (→ Q10)

~~Transform-cap~~ **✓ RULED** (2 at v1; 3 gated on §7a audit live — §5) · ~~fairness-band widths~~ **✓ RULED as structure** (monotone widening by rarity; exact widths = band-sheet ratification from measured noise floor — §7) · ~~ω-penalty~~ **✓ RULED RETIRE-by-construction with tripwire** (§8) · ~~defensive-axes C1 extension~~ **✓ RULED as recommended** (§2 five-line ruling) — *all four swept 2026-07-07.* **Two band-time cap-value items remain, both riding the band-sheet:** (1) **resist/mitigation cap VALUES** (§7a topology guard — D2-75% precedent); (2) **control/proxy capped-garnish aggregate-cap VALUES** (§2.3 layer 2 — the garnish ceiling below the specialist floor, tiered by #5/#8; added 2026-07-13). Neither gates current work.

---

**Signed:** gandalf, 2026-07-07. *One instrument, two customers; kits vote bare; the ghost channels get absorbed, not inherited.*
