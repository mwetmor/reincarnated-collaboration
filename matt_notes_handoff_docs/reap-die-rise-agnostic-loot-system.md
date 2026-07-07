# Reap. Die. Rise. — Archetype-Agnostic Loot System (Technical Spec)

> **⚠ SUPERSEDED BY CANON (2026-07-07) — lineage only.** Canonized into the spec pair **`canonical/reap-die-rise-story/agnostic-loot-story-spec.md`** (soul-as-lens, gleaning, cementing, soul weapons, naming surfaces) + **`canonical/reap-die-rise-engine/agnostic-loot-engine-spec.md`** (operator algebra, merged §6+§7 validation campaign, build contracts), absorbing the 2026-07-06 review reconciliations (C1–C5) + the 2026-07-07 rulings (G1/G2/G3, body-persistence). **The canon pair governs.** Corrections baked into canon that this draft still carries: "~64K" (→ 68,040/12,960 of record) · resource-*type* operators (→ RESERVED, empty-by-ruling) · §5.2's "LLM (or a templating layer)" hedge (→ rules text COMPUTED, LLM names only) · §6/§7 as two builds (→ ONE merged gauntlet campaign) · gear persistence unstated (→ cementing; body crosses cleansed).

**Audience:** the build team (Claude agent team on the Mac).
**Status:** design spec. Some pieces already exist (the coordinate space, legendary operators, the LLM naming call); this doc unifies them and adds the two missing pieces — **agnostic-point search** and **cross-kit fairness-band validation**.

---

## 0. The problem this solves

The game changes the player's class/kit by **reincarnating into a defeated boss** (potentially twice per descent, possibly by choice). Traditional gear breaks under this loop:

- **Body-bound gear** doesn't work on the new class → dead on reincarnation.
- **Soul-bound gear** (follows you regardless of body) isn't really loot — it's *stats wearing a costume*, because it never has to *fit* anything.
- **Partial body/partial soul** is the worst of both.

**The resolution:** gear is not a bundle of class-coupled stats. Gear is a set of **archetype-agnostic operators** — transformations defined over the *universal structural axes* that every kit possesses. The same operator produces **genuinely different behavior on different kits**, so it (a) transfers across reincarnations without frustration, and (b) is *real loot* — build-defining and body-reactive — not a stat-skin.

This is only possible because kits are already decomposed into a shared coordinate space. Gear lives in the **same space** as kits, so gear can modify *any* kit without knowing which kit it is.

---

## 1. Core model: gear as operators over the coordinate space

### 1.1 Kits are points; gear is operators
- A **kit** is a point (or region) in the mechanic coordinate space (the existing ~64K-point decomposition).
- A **gear affix** is an **operator**: a function that transforms a kit's coordinates, defined only in terms of axes that exist at *every* point in the space.

### 1.2 Universal axes (the only vocabulary gear may use)
Gear operators may ONLY reference **structural axes present in every kit**, never specific abilities. Examples of universal axes:
- Resource (cost, pool size, regen, resource *type*)
- Cooldown / cast time / channel
- Range (per-ability, and structural slots like "farthest-range ability," "nearest-range ability")
- Area / radius / shape
- Target count / chaining / pierce / split
- Magnitude (damage/effect strength)
- Projectile behavior (speed, count, arc, return)
- Trigger hooks: on-hit, on-kill, on-crit, on-cast, on-cooldown-end, on-resource-spend
- Structural slots: "primary attack," "secondary abilities," "movement ability," "ultimate/highest-cost ability"

**Rule:** if an axis exists for *all* kits, an operator on that axis is archetype-agnostic by construction. If an operator references a *specific* mechanic that only some kits have (e.g., "fireball," "summon count"), it is **not** agnostic and is disallowed for transferable gear.

### 1.3 Operator classes (by legibility/power tier)
- **Value operators** (readable, low identity): scale a universal axis. "+X% magnitude," "-X% cost." Use for **low rarities**.
- **Structural operators** (readable, mid identity): act on a structural slot. "Your primary attack chains to +1 target." "Your farthest-range ability gains +30% area." Use for **mid rarities**.
- **Transform operators** (abstract, high identity): impose a dramatic trade/transformation. "You cannot use your primary attack, but secondary abilities cost nothing." "Your area effects trigger twice at half magnitude." "Convert all single-target into area." Use for **legendaries / sets**.

The design intent: **lean abstract on high rarities** (transform operators are the chase and the build-definers), and rely on the naming/description layer (§5) for legibility.

### 1.4 Why this is real loot, not a stat-skin
A transform operator like "primary attack chains to +1 target" does something **different** on a sword-kit vs. a fireball-kit vs. a summoner-kit — same operator, different emergent result per body. So the *same legendary* **plays differently depending on which body wears it**. That is the property that makes it transfer across reincarnations *while remaining genuine loot*.

---

## 2. Rarity via the coordinate space

Rarity is **not** a separate stat budget. Rarity = **how rich a point is** (how many latent operators it carries) and **which operator class** it draws from:

- **Common / low:** sparse points — one or few *value operators*.
- **Rare / mid:** *structural operators*, possibly 2–3.
- **Legendary / set:** rich multi-operator points combining *transform* + supporting operators. Marquee legendaries are **fixed, authored points** (stable identity); the mass of gear is **generated** (sampled points).

Lower rarities being sparser points means soul level (§3) matters less for them and more for legendaries.

---

## 3. Soul level: progressive gleaning (the fiction + the mechanic)

### 3.1 Fiction
Every piece of gear's qualities were **always in the item**. Your **soul level** (a function of experience level × number of reincarnations) determines **how much you can draw out of it** — how many of its latent operators are "awake." The item is fixed light; the soul is the lens.

### 3.2 Mechanic
- Each gear point carries an ordered set of latent operators, each gated by a **soul-level threshold**.
- As soul level rises, more of a held item's operators activate — progression is **deepening the gear you have**, not only replacing it.
- **Color** on pickup reflects how much the *current* soul can glean from that point (its effective revealed rarity for you now).

### 3.3 Design guardrail (important)
Re-gleaning is a **bonus** progression layer, NOT the primary one. Keep the **drop-acquisition dopamine** as the main loop ("more loot than Diablo"). Do not replace drops with re-gleaning or the core loot thrill is starved. Both run in parallel: frequent drops (acquisition) + soul-level re-gleaning of held gear (deepening).

---

## 4. Soul weapons (archetype-agnostic by fiction)

Physical weapons imply an archetype (a sword *wants* to be swung), which fights the agnostic-operator model and creates the "why am I carrying a sword as an archer" problem.

**Solution:** the player's weapon is a **soul weapon** — a manifestation of the soul's armament that **takes the form appropriate to the body wearing it** (blade for a warrior body, bow for an archer body, focus for a caster) while carrying the same operators. "Your weapon" is agnostic *diegetically*, not just mechanically. It re-expresses per body without being a stat-skin, because it carries *operators* that play differently per form.

This is the flagship example of the whole system: agnostic operators + per-body manifestation = gear that belongs to the soul and reshapes to the body while staying real loot.

---

## 5. Legibility layer: LLM naming + per-body realized descriptions

Because high-rarity operators are abstract, the naming/description layer carries legibility. The serial content engine already calls an LLM to name entities; extend it to gear with **strict constraints**.

### 5.1 Item naming — MUST encode the mechanic, not just sound epic
- **Input to the naming call:** the item's actual operator set.
- **Constraint:** the generated name must be a **readable compression of the item's function** — a handle that *signals the mechanic*. E.g., a chain-to-second-target operator → "Twinfang"; a resource-conversion operator → "Hollowcost"; a delayed-but-amplified trigger → "Slowburn."
- **Anti-goal:** arbitrary evocative flavor that tells the player nothing ("Shadowmourne of the Endless Void"). A flavorful-but-opaque name *worsens* legibility (flavor name + opaque operator + no signal). The name is functional compression first, flavor second.

### 5.2 Per-body, per-soul-level realized description
- The LLM (or a templating layer) generates a **plain-language description of the currently-awake operators as realized on the current body**. E.g., on an archer form: "Your arrows split to a second target."
- This is the UX that makes abstract operators legible — computed **per body** and **per soul level**, so the player always sees the concrete effect of what they're actually wearing right now.
- Names give **memorability**; realized descriptions give **clarity**. Together they let operators be as abstract as we want.

### 5.3 Fixed vs. generated naming
- **Marquee legendaries/sets:** fixed, authored names + fixed points → stable identity players learn and trade knowledge about ("everyone knows Twinfang").
- **Generated mass (lower gear):** procedural LLM names → variety and flavor, no shared-identity requirement.
- (Same authored-spine / generated-body split used elsewhere in the game.)

---

## 6. THE AGNOSTIC-POINT SEARCH (missing piece #1 — build this)

**Goal:** find points/operators in the coordinate space that are **agnostic** (meaningful across the kit spectrum) at every rarity — not just for legendaries, and not gear "worn by the player during the sim" as before.

### 6.1 Definition of an agnostic operator (search target)
An operator qualifies as agnostic if:
1. It references **only universal structural axes** (§1.2) — automatic disqualification if it touches a mechanic not present in all kits.
2. When applied across a representative sample of kits, it produces a **non-trivial, non-degenerate effect on (almost) all of them** — i.e., it's *relevant* everywhere, not dead weight on large regions of the space.

### 6.2 Search procedure
1. **Restrict the operator vocabulary** to the universal axes (§1.2). This is the search space of *candidate* operators.
2. **Sample the kit space** — a representative spread of kits across the coordinate space (cover archetype regions: melee, ranged, caster, summoner, hybrid, etc.). This sample is the **test band**.
3. For each candidate operator, **apply it to every kit in the sample** and measure:
   - **Relevance:** does it change the kit's behavior meaningfully? (Non-zero, non-negligible effect.)
   - **Coverage:** on what fraction of the sample is it relevant? Agnostic ⇒ high coverage.
4. **Keep** operators with high coverage (relevant across the spectrum). **Discard** operators that are only relevant to a narrow region (those are archetype-*specific*, even if phrased in universal terms).
5. **Tier** the surviving operators into value / structural / transform classes (§1.3) for rarity assignment.

### 6.3 Lower rarities from "lesser" agnostic points
Previously only legendaries used agnostic operators. **Change:** lower rarities draw from **lesser agnostic points** — sparser, lower-magnitude *value/structural* operators that still pass the agnostic test (universal axis + broad coverage), just with smaller impact. Every rarity is agnostic; they differ in operator count, class, and magnitude — not in whether they're class-locked.

---

## 7. CROSS-KIT FAIRNESS-BAND VALIDATION (missing piece #2 — build this)

**This is the key correction from prior work:** gear must be tested for fairness **across the spectrum of kits**, and only **in-band** gear ships. Previously gear was applied to the player in the sim but **not** validated across kits for fairness — so out-of-band (broken-on-some-kits) gear could slip through. Fix it by running gear through the same gauntlet fitness machinery already used to balance kits.

### 7.1 The core risk
An operator that is fair on most kits can be **degenerate on a specific coordinate region**. Example: "abilities trigger twice" is catastrophic on an already-high-magnitude kit but fine elsewhere. Agnostic ≠ balanced. Balance must be *measured*, not assumed.

### 7.2 Validation procedure (reuse the gauntlet fitness function)
For each gear operator (and each rarity/magnitude variant):
1. **Apply the operator across the sampled kit spectrum** (the same representative sample from §6.2, ideally larger).
2. For each (operator × kit) pairing, run the **existing simulated fight gauntlet** and record the existing fitness metrics: **win rate, kills-per-minute, AOE %, the spatial "fun" signal**, plus a **power-delta** (kit-with-gear vs. kit-baseline).
3. Compute the **distribution** of the power-delta across the kit spectrum.
4. Define a **fairness band** — an acceptable range of power-delta. An operator is **in-band** only if its effect stays inside the band **across (almost) all kits**.
5. **Flag out-of-band outliers:** any kit region where the operator spikes above the band (degenerate combo) or falls below (dead weight). 
   - If a few outliers: **clamp/condition** the operator (e.g., diminishing returns past a magnitude threshold) or **exclude** those kit regions from the operator's applicability.
   - If broadly out-of-band: **reject** the operator, or **re-tier** it (lower magnitude / lower rarity) and re-test.
6. **Only in-band operators ship.** Everything served to players has been validated to stay within the fairness band across the kit spectrum.

### 7.3 Why the engine is uniquely suited to this
The same brute-force gauntlet that balances kits can brute-test **gear × kit** pairings across the whole space — something hand-balancing cannot do. Gear validation is *the same machinery* as kit validation, pointed at operators instead of kits. This is the architectural payoff: **the decomposition that lets us generate kits also lets us generate and fairness-validate gear.**

### 7.4 Outputs of validation (persist these)
- Per-operator: coverage (§6), fairness-band pass/fail, list of clamped/excluded kit regions, tier assignment.
- Per-rarity: the validated operator pool available to drop.
- A **degenerate-combo blacklist** (operator × kit-region pairs to avoid), reusable at drop time so the loot generator never hands a player a known-broken pairing for their current body.

---

## 8. Pipeline integration (how it runs in serial generation)

1. **Search** (§6): enumerate/sample candidate operators over universal axes → filter by coverage → tier.
2. **Validate** (§7): run gear × kit gauntlets → compute fairness band → keep in-band, clamp/exclude/reject the rest → persist pools + blacklist.
3. **Author the spine:** hand-fix marquee legendary points + names.
4. **Generate the body:** sample validated operators into gear points across rarities; LLM-name them (functional-compression constraint, §5.1).
5. **Runtime:** on drop, color by soul-level gleaning (§3); on equip/reincarnation, re-express operators on the current body and generate the per-body realized description (§5.2); respect the degenerate-combo blacklist for the current body.

---

## 9. What was being done wrong before (so we don't regress)

- Gear was **worn by the player during the sim** but **not tested for fairness across the kit spectrum** → out-of-band gear could pass. **Fix:** §7 cross-kit fairness-band validation; only in-band gear ships.
- **Only legendaries** used agnostic points. **Fix:** §6.3 — all rarities use (lesser) agnostic points.
- Gear was framed as **equipment you wear** (archetype-coupled) rather than **agnostic operators over universal axes**. **Fix:** §1 operator model + §4 soul weapons.

---

## 10. Open design decisions (flag for discussion)

- **Abstraction ceiling:** we're leaning abstract on high rarities and relying on §5 for legibility. Confirm the naming-prompt constraint (name must signal mechanic) is enforced, since it's the linchpin of the legibility bet.
- **Reincarnation choice:** leaning toward letting the player *choose* whether to reincarnate. If so, non-reincarnation needs its own gear/power path (interacts with §3 soul-level scaling) — out of scope for this doc but affects gear pacing.
- **Fairness-band width:** the band's tolerance is a tuning knob — tighter = flatter/safer/less exciting gear; wider = spicier/riskier. Decide the target band per rarity (legendaries likely get a wider band — build-defining spikes are *desirable* there, within reason).
