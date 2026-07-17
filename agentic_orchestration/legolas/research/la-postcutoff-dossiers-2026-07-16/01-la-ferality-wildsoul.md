# Dossier — Ferality Wildsoul (`la-ferality-wildsoul`)

**Mode:** A (analytical, live-sourced)
**Commissioner:** gandalf-prime, 2026-07-16
**Roster target:** Edition-IV hold-out (T4/P-1 predicate; dossier_owed=1)
**Priority:** HIGH (blocks atlas parity)
**Post-cutoff:** TRUE — class released 2026-02-26 NA/EU (Call of the Wildsoul patch)
**Crawl date:** 2026-07-16

---

## Identity

**Game:** Lost Ark (Smilegate/Amazon Games)
**Class:** Wildsoul (Specialist Advanced Class; Female Gunlancer/Artist lineage — new class, not gender-lift)
**Engraving / spec identity:** Ferality (also called "Wild Instincts" on Maxroll — the Maxroll build URL is `wild-instincts-wildsoul-build-guide`; the in-game engraving name is Ferality)
**Sibling engraving:** Phantom Beast Awakening (this build's mirror — see dossier 02)
**Patch/era:** Post-launch Season 4-adjacent (Call of the Wildsoul, Feb 26 2025 NA/EU launch); ongoing.
**Canon tier:** shallow → medium (1 year+ live; still meta-relevant per Maxroll continued guide maintenance)
**Shipped / negative-canon:** SHIPPED — positive canon.

## The two-engraving split (why these are two distinct rows)

Every Lost Ark advanced class has TWO class engravings that produce distinct build identities. Wildsoul's are:
- **Ferality** — nimble shapeshift-in-tandem playstyle; Fox and Bear alternation as the loop
- **Phantom Beast Awakening** — timed super-mode playstyle; identity gauge fills → Z activates form → cooldown-reduction economy

The atlas hold-out lists both separately because they are mechanically distinct kits sharing a class chassis. This dossier covers Ferality.

## Build identity (2–4 sentences)

The Ferality Wildsoul IS the shapeshift keystone in mechanical form. The player alternates between Fox form and Bear form on a per-skill cadence, and Fox-only and Bear-only skill sets are gated by form membership — Fox skills cannot be cast in Bear form and vice versa. The rotation is structured in ordered pairs ("3-2-3 setup" per Maxroll): Pair 1 = Fox Flame, Boulder Bear, Fox Illusion; Pair 2 = Fox Orb, Swish Bear, Fox Illusion; with Vulpine Velocity + Tailwind + Claw as the between-pair filler that recovers the central Phantom Beast Energy resource. Form-swap is not free — it draws on Phantom Beast Energy — and casting form-locked skills feeds two secondary meters (Fox Energy and Bear Energy) that gate the ultimate abilities Forbidden Sorcery: Fox Star Rainstorm and Forbidden Sorcery: Ripping Bear.

## Shapeshift-relevance (GX-02 keystone evidence)

**VERDICT: STRONG POSITIVE.** Ferality Wildsoul is the closest genre-precedent I've found to a persistent-form shapeshift-as-loop kit identity. Recording the exact mechanical grammar as commissioned:

- **Form-entry cost.** Transformation skills require Phantom Beast Energy (center gauge). "You passively generate energy for whichever form you are in currently" — but the transformation *skills themselves* are the resource sink. In Human form the character regenerates 2% of max Phantom Beast Energy per second (source: nexus-guide-site / Fandom Wiki cross-corroboration). This means: form is not free; form is spent-into.
- **Form-locked skill sets.** Fox skills (Fox Illusion, Fox Leap, Fox Flame, Fox Orb, Crow Parade, Vulpine Velocity) are castable ONLY in Fox form. Bear skills (Boulder Bear, Swish Bear, Digger Bear, Growling Bear, Ursine Windup, Rolling Wheel) are castable ONLY in Bear form. Neutral: Claw (counter skill, castable any form) [Fandom Wiki / nexus-guide-site].
- **Gauge interplay (dual side meters).** "You must be in Fox form to cast Forbidden Sorcery: Fox Star Rainstorm and in Bear form to cast Forbidden Sorcery: Ripping Bear when each respective gauge is full" [Maxroll]. Two secondary gauges (Fox Energy left, Bear Energy right) fill independently through form-specific skill usage. This means the shapeshift decision is not just "which form do I want to be in" but "which ultimate am I building toward."
- **Ferality stack mechanic.** "Casting transformation skills grants you a stack of Ferality" (max 3 stacks), providing HP recovery, attack speed, and defense debuff on target [Maxroll]. The stack IS the payoff for staying in the shapeshift loop.
- **Form buff differential.** Fox form = +20% Attack Speed and +20% Move Speed. Bear form = +10% Damage Reduction [Maxroll]. Alternating forms = alternating combat profiles.

**Implication for RDR GX-02:** if the RDR shapeshift keystone chooses a "persistent-form" geometry, Ferality is the atlas anchor. If instead it chooses a "temporal-window" geometry, Phantom Beast Awakening is the anchor (dossier 02). The two dossiers together give downstream design both flavors.

## Core skill loop

**Rotation:** "The optimal way to rotate through your skills is in pairs of three at a time. Between each pair, make sure to cast Vulpine Velocity, Tailwind, and Claw" [Maxroll].

**Pair 1:** Fox Flame · Boulder Bear · Fox Illusion (Fox → Bear → Fox transition)
**Pair 2:** Fox Orb · Swish Bear · Fox Illusion (Fox → Bear → Fox transition)
**Between-pair filler:** Vulpine Velocity · Tailwind · Claw (recovers Phantom Beast Energy)

**Delivery verbs and geometry:** Fox skills lean at-target melee/mid (Fox Leap = dash; Fox Flame = area strike; Fox Illusion = repositioning/burst). Bear skills lean self-origin heavy melee (Boulder Bear, Swish Bear, One-Hit Bear function as primary damage dealers). The rotation trades precision (Fox) with brute-force (Bear). Explicit geometry beyond "AoE from Earthquake Pound refills Phantom Beast Energy" is not detailed in Maxroll's public guide.

**Commitment:** WIND-UP predominant. The rotation demands ordered execution (pair sequence matters) and each transformation skill has a visible animation. No skills are flagged as channels. "No casting wind-ups mentioned; skills appear instant or rapid" per Maxroll on the individual skills, but the ORDERED-PAIR CADENCE is itself a wind-up macro pattern.

## Mobility-while-casting posture

**Fox form** provides +20% Move Speed baseline. **Bear form** provides no move-speed increase (trades speed for damage reduction). Individual skill posture is not extractively documented — Maxroll lists "Good mobility" as a pro of the class but does not resolve per-skill rooted/walk/full-move for Ferality specifically. Fox Leap is explicitly a dash (movement-as-skill). Cross-Wildsoul class rating on Maxroll for Ferality: "Low mobility" con listed on the Wild Instincts / Ferality variant [Maxroll class overview], corroborating that Ferality's mobility is form-gated (high in Fox, low in Bear).

## Defense verbs

- **Bear form:** +10% Damage Reduction [Maxroll].
- **Claw:** primary Counter skill [Maxroll — "Claw serves as the 'main Counter skill'"].
- **Ferality synergy debuff:** "Defense of the target hit by Shapeshift skills -12% for 5 seconds (Synergy)" [Maxroll].
- **Class-level immunities:** Ferality Wildsoul carries Paralysis Immunity and Push Immunity as pros [nexus-guide-site].
- **No shield / block / dodge invulnerability** in the kit; defense is form-mediated and via the Counter Claw.

## Economy

**Primary resource:** Phantom Beast Energy (center gauge, 100% cap). Spent by transformation skills; regenerates passively in Human form (2%/sec) and via non-transformation filler skills (Vulpine Velocity, Tailwind, Claw).

**Secondary resources:** Fox Energy (left gauge) and Bear Energy (right gauge) — each fills through form-specific skill usage. Enable Forbidden Sorcery ultimate skills at full.

**Con flagged by Maxroll on Ferality:** "Very high mana drain" — additional mana pressure beyond Phantom Beast Energy management.

## Element / damage mode

Wildsoul does not carry a primary elemental label in the D2/PoE sense. Damage is HIT-based on the transformation skills (Boulder Bear, Ursine Windup, Fox Flame etc.) with the Ferality synergy debuff adding a rider damage-taken increase on target. No confirmed DoT vector as the dominant mode.

## Distinction from Phantom Beast Awakening (sibling engraving)

Verbatim from Maxroll's Ferality guide: "If you want a more dynamic playstyle based on summoning your fox and bear as companions to attack in your stead, check out our Phantom Beast Awakening guide."

**Core distinction:**
- **Ferality** = the player IS the beast; direct player shapeshifting with skill execution in each form; active rotation management.
- **Phantom Beast Awakening** = the player summons Fox and Bear as companions AND enters a timed identity super-form (Phantom Beast Awakening state, 30s, Z-activated). Companion-flavored damage.

Framing from mmorpg.com (developer detail): "summon a beast or becoming one (technically two) themself." Ferality is the "become one" arm.

## Engine-prefix claims

| Slot | Value | Confidence | Evidence |
|---|---|---|---|
| attr | SPEC | HIGH | Lost Ark uses Specialization as the class-identity scaling stat — the Wildsoul's Phantom Beast Energy gauge is SPEC-scaled. [Maxroll character stats section; class-overview.] |
| range | melee-mid | HIGH | Bear skills are melee self-origin; Fox skills reach mid-range (Fox Leap dash + Fox Flame at-target AoE). No ranged-projectile dominant kit. |
| tempo | high | HIGH | 3-2-3 rotation + between-pair triple filler = very high APM cadence; +20% Attack Speed in Fox form compounds. |
| amp | spiky | MED | Forbidden Sorcery ultimates are burst-shaped when the secondary gauges fill; base rotation is more sustained. Spiky at the ultimate cadence. |
| proxy | solo | HIGH | Direct-player damage; no proxy actors (the Phantom Beast summons are the sibling build's identity, not Ferality's). |
| commit | wind-up | MED | Ordered-pair execution is itself a macro wind-up. Individual skills instant. |

## Raw descriptors

**geo:** Fox = at-target medium-radius; Bear = self-origin melee small-radius; Earthquake Pound = large-zone (Awakening skill). Ferality is small-to-medium radius throughout the core loop.
**ctrl:** Defense-debuff on target via Ferality synergy (-12% defense, 5s). No hard CC dominant. Claw counters.
**mob:** Form-gated. Fox = +20% MS + Fox Leap dash. Bear = mobility low. Rated "Low mobility" pro/con class-level for the Ferality variant [Maxroll].
**def:** Bear form +10% DR; Ferality provides stacking HP recovery; Paralysis + Push immunity; Claw counter. No shield/block layer.
**econ:** Phantom Beast Energy center + Fox Energy left + Bear Energy right (triple-meter identity). High mana drain flagged. Spend-and-recover model.

## Sources

1. Maxroll Ferality Wildsoul Build Guide (URL slug: `wild-instincts-wildsoul-build-guide`) — https://maxroll.gg/lost-ark/build-guides/wild-instincts-wildsoul-build-guide (accessed 2026-07-16). Primary source for rotation, engraving mechanics, gauge system.
2. Maxroll Phantom Beast Awakening Wildsoul Build Guide — https://maxroll.gg/lost-ark/build-guides/phantom-beast-awakening-wildsoul-build-guide (accessed 2026-07-16). Cross-reference for the sibling engraving distinction.
3. Lost Ark Fandom Wiki — Wildsoul — https://lostark.fandom.com/wiki/Wildsoul (accessed 2026-07-16). Skill list per form; class chassis.
4. PlayLostArk — Class Spotlight: Wildsoul (en-gb) — https://www.playlostark.com/en-gb/news/articles/wildsoul-class-spotlight (accessed 2026-07-16). Official class framing, three-meter identity confirmation.
5. Nexus guide site — Wildsoul — https://nexus-guide-site.pages.dev/guides/wildsoul (accessed 2026-07-16). Full skill list confirmation; engraving pros/cons; class immunities.
6. Maxroll class overview — https://maxroll.gg/lost-ark/resources/class-overview (accessed 2026-07-16). Class-tag (Specialist), engraving-specific mobility ratings.
7. MMORPG.com — Wildsoul Advanced Class detail — https://www.mmorpg.com/news/lost-ark-details-wildsoul-advanced-class-letting-you-summon-or-become-a-beast-2000134195 (accessed 2026-07-16). Summon-vs-become framing.
8. MMOs.com release corroboration — https://mmos.com/news/lost-arks-february-update-call-of-the-wildsoul-launches-feb-26-with-shapeshifting-class-and-progression-revamp (accessed 2026-07-16). Release date + "shapeshifting class" official framing.

## Knowledge gaps

1. Exact Phantom Beast Energy cost per transformation skill not published in accessible sources.
2. "3-2-3" numeric label arithmetic not obviously mapping to 6-skill loadout — needs supplementary context on Fox Illusion's role.
3. Weapon type not extractively confirmed (transformations imply "form is the weapon").
4. Full engraving-tree effect wording (level 1/2/3 stack values) — Fandom Wiki Ark Passive page returned 402; secondary corroboration only.
</content>
</invoke>