# Dossier — Liberator Valkyrie (`la-liberator-valkyrie`)

**Mode:** A (analytical, live-sourced)
**Commissioner:** gandalf-prime, 2026-07-16
**Roster target:** Edition-IV hold-out (T4/P-1 predicate; dossier_owed=1)
**Priority:** HIGH (blocks atlas parity)
**Post-cutoff:** TRUE — class released 2025-08-20 NA/EU (Rise of the Valkyrie patch)
**Status:** PARTIAL — mobility-while-casting posture underspecified in accessible sources; flagged below.
**Crawl date:** 2026-07-16

---

## Identity

**Game:** Lost Ark (Smilegate/Amazon Games)
**Class:** Valkyrie (Warrior subclass — female Holy Knight class)
**Engraving / spec identity:** Liberator (Support specialization)
**Sibling engraving:** Shining Knight (DPS; see dossier 03)
**Patch/era:** Rise of the Valkyrie (Aug 20 2025 NA/EU); ongoing.
**Canon tier:** shallow → medium.
**Shipped / negative-canon:** SHIPPED — positive canon.

## Support-genre observation (C2 sweep context)

The megaprobe C2 sweep verdict was: NO solo-context pure-support kit exists in the 515-row corpus (genre-structural — solo-play ARPG has no ally to support). Lost Ark Valkyrie Liberator is a party-context support kit — it validates C2 by being an MMO party class, NOT a solo-context precedent. For atlas parity purposes, this kit's SUPPORT semantics are recorded but the C2 verdict for RDR (solo game) stands. The Liberator kit is genre-precedent for BUFF-CYCLE mechanics and SHIELD/CLEANSE mechanics — extractable design patterns even without importing the party-context.

## Shapeshift-relevance (GX-02)

**VERDICT: NEGATIVE.** No form-swap. Recorded for completeness.

## Build identity (2–4 sentences)

The Liberator Valkyrie is the SUPPORT arm of the Valkyrie class — a party-buff cycler wielding shield-primary tools to deliver Attack Power buffs, Brand debuffs, shields, heals, and damage reduction to allies. Her Z-identity (Release Light) generates stacks of Liberator (max 3, 60s duration, +10% self damage per stack); her X (Light of the Faithful) consumes all stacks and heals the party for 10/20/30% of Max HP based on stack count. Her signature party buff is Wings of Freedom — a 24m-radius aura granting +2% damage and +8% move speed to party members for 60 seconds. The kit emphasizes reliable buff throughput ("regardless of positioning"), stagger and destruction contribution, and defensive layering — shield application, cleansing, damage reduction zones.

## Core skill loop

**Z-identity (Release Light):**
- Grants "one stack of Liberator for 60 seconds (max 3)"
- Each stack: +10% damage dealt to enemies (self)
- Feeds into X (Light of the Faithful) for the payoff

**X-payoff (Light of the Faithful):**
- Consumes all Liberator stacks at once
- Heals based on stack count consumed (10% / 20% / 30% Max HP per Maxroll — mapping to 1/2/3 stacks)

**Party buff throughput layer:**
- **Wings of Freedom** — 24m radius, 60s duration, +2% damage + +8% move speed to party (base tripod values)
- **Circle of Truth** — applies Brand debuff on target; tripod "allows it to track the enemy and keep refreshing the buff for its entire duration" [Maxroll]
- **Seraphic Leap** and **Seraphic Oath** — both apply the same buff (do not stack; alternating cast pattern for uptime maintenance)

**Defensive layer:**
- **Blessing of Salvation** — shield application + Cleanse
- **Sheltering Shield** (tripod alt) — shield + damage reduction (used "whenever you don't need a Cleanse")
- **Salvation Site** — AoE damage reduction zone
- **Identity healing** via Light of the Faithful

**Additional party buffs (Maxroll):**
- **Divine Confirmation** — party +10% damage for 10s + +20% Hyper Awakening Damage for 30s

**Commitment:** WIND-UP MED. Buff cycles are timed (60s durations) requiring rotational maintenance. Individual buff applications appear near-instant to enable throughput; identity heal (X) is a discrete commitment moment.

## Delivery verbs and geometry

- **Buff auras** — 24m radius from caster (Wings of Freedom).
- **Shield application** — at-target ally or self.
- **Salvation Site** — at-target ground AoE (damage reduction zone).
- **Circle of Truth** — Brand on target (with tracking tripod).
- **Light of the Faithful** — self-centered party heal.

Geometry: predominantly self-origin or at-target-ally utility geometry. Not attack-projectile-oriented.

## Mobility-while-casting posture — PARTIAL (flagged gap)

Maxroll notes Valkyrie has "a lot of mobility and fast animations" [Maxroll Liberator guide]. But the specific rooted-vs-walk-vs-full-move posture for buff-application skills (Seraphic Leap / Seraphic Oath / Circle of Truth) is not explicitly documented in the accessible Maxroll section. Class-overview Maxroll rates Liberator "Poor mobility" as the class-tag verdict (contrast with Shining Knight's "Good mobility"). Reconciliation: Liberator sacrifices per-skill mobility features for buff-application throughput; the class-tag "Poor" applies to combat-mobility while the "fast animations" characterization applies to buff-application speed.

**This is the PARTIAL gap for the dossier.** Downstream design should treat mobility-while-casting posture as "rooted / brief walk" for buff-application skills pending clearer confirmation.

## Defense verbs

Extensive defensive layering (support class):
- **Blessing of Salvation** — shield + Cleanse (removes debuffs)
- **Sheltering Shield** — shield + damage reduction (tripod alternative)
- **Salvation Site** — AoE damage reduction zone (ground-placed)
- **Light of the Faithful (X)** — party heal via stack consumption
- **Divine Confirmation** — party damage buff (indirect defense via burst-window compression)

Contrast with Shining Knight: SK relies on Counter + mobility for defense; Liberator provides layered protection (shield + heal + DR) to the party AND self.

## Economy

**Primary resource:** Liberator stacks (max 3, 60s duration each; refreshed by Z casts).

**Secondary economy:** Buff durations (Wings of Freedom 60s; Divine Confirmation split 10s/30s; Circle of Truth Brand refreshable via tracking tripod). The kit is TIMER-management heavy.

**Identity meter:** Same Light Meter / Piety Meter as Shining Knight (assumed shared class-identity meter; not fully resolved in extracts). Filled by skill casts; unlocks Z (Release Light).

## Element / damage mode

**Element:** Holy/Light thematic. Damage output is not the point of the kit; utility throughput is. Some damage on Circle of Truth, Salvation Site, and stagger tools.

## Distinction from Shining Knight (sibling engraving)

See dossier 03 §Distinction table for the full axis breakdown. Key axes:
- **Role:** Support (this) vs DPS (SK)
- **Z:** Release Light (self-buff stack + payoff setup) vs Shining Knight (party debuff + self-buff on next 3 HB)
- **X:** Light of the Faithful (party heal) vs Final Splendor (single-hit burst)
- **Weapon emphasis:** Shield-primary vs Sword-primary
- **Party contribution:** Layered utility (Attack Power buff + Brand + shield + heal + DR) vs Synergy application only
- **Mobility rating:** Poor vs Good
- **Amp shape:** Flat throughput vs spiky burst-finisher

## Engine-prefix claims

| Slot | Value | Confidence | Evidence |
|---|---|---|---|
| attr | SPEC | HIGH | Specialization scales identity meter and buff magnitudes [Maxroll]. |
| range | melee | MED | Sword-and-shield melee class; buff-application radius is aura-based (24m Wings of Freedom) but the class is played at melee-mid range around the boss/party. |
| tempo | mid | MED | Buff-cycle timers (60s primary, various sub-durations) create a rotational maintenance cadence — steady rather than burst-heavy. |
| amp | flat | MED | Support-role damage is not the primary output; party-throughput is FLAT-SHAPED (steady buff + shield uptime rather than single spike). Note: this is amp of THE CLASS's damage contribution, not the party's damage contribution. |
| proxy | solo | HIGH | Direct-player support-casting. Party members receive buffs but are not proxies in the D3/PoE minion sense — they are independent player-actors in the MMO context. For solo-context translation the class has no proxy actor. |
| commit | wind-up | MED | Buff-application near-instant; identity heal (X) is a commit moment; overall kit is rotational maintenance rather than deep wind-up. |

## Raw descriptors

**geo:** 24m party aura (Wings of Freedom); at-target ally shield; ground AoE (Salvation Site); Brand on target (Circle of Truth).
**ctrl:** Brand debuff (Circle of Truth); Cleanse (Blessing of Salvation removes ally debuffs); Stagger/Destruction contribution ("Reliable Stagger and Destruction" per fdaytalk). Not hard-CC dominant.
**mob:** POOR (class-tag per Maxroll). "Fast animations" for buff-application per Maxroll but combat-mobility low. Flagged PARTIAL — see mobility section.
**def:** Layered — shields (Blessing of Salvation, Sheltering Shield), damage reduction zone (Salvation Site), heal (Light of the Faithful), Cleanse. Highest defensive-layer count in the 4-dossier set.
**econ:** Liberator stack (max 3, 60s) → Z→X consume cycle. Timer-management heavy (multiple 60s buff durations).

## Sources

1. Maxroll Liberator Valkyrie Build Guide — https://maxroll.gg/lost-ark/build-guides/liberator-valkyrie-build-guide (accessed 2026-07-16). Primary source for Release Light stacks, Light of the Faithful heal, Wings of Freedom aura, Blessing of Salvation shield-cleanse.
2. Maxroll Shining Knight Valkyrie Build Guide (sibling cross-reference) — https://maxroll.gg/lost-ark/build-guides/shining-knight-valkyrie-build-guide (accessed 2026-07-16).
3. PlayLostArk — Rise of the Valkyrie Release page — https://www.playlostark.com/en-us/game/releases/rise-of-the-valkyrie (accessed 2026-07-16). Piety Meter, Light Unleashing, Conviction of Liberation official terminology. "Support: heals allies and leads the battlefield with the power of light."
4. Maxroll class overview — https://maxroll.gg/lost-ark/resources/class-overview (accessed 2026-07-16). Liberator "Poor mobility" implied (no mobility pro).
5. fdaytalk Valkyrie build guide — https://www.fdaytalk.com/lost-ark-valkyrie-build/ (accessed 2026-07-16). "Reliable Stagger and Destruction" attribution.

## Knowledge gaps

1. **Mobility-while-casting posture for buff skills** — Seraphic Leap / Seraphic Oath / Circle of Truth rooted-vs-walk-vs-full-move not explicitly resolved. Class-tag "Poor mobility" + "fast animations" tension unresolved at per-skill grain. PARTIAL flag.
2. **Piety Meter (official) vs Light Meter (Maxroll)** naming reconciliation — same issue as Shining Knight dossier.
3. **Exact Wings of Freedom base vs tripod values** — Maxroll gives base +2% damage +8% MS; tripod scaling not extracted.
4. **Divine Confirmation trigger condition** — Maxroll states +10% damage 10s + +20% Hyper Awakening Damage 30s; the activation trigger (which skill grants it) not extracted.
5. **Sword vs shield weapon-slot** — PlayLostArk confirms one-handed sword; the shield's mechanical status (offhand? distinct slot? cosmetic?) not extractively resolved. Liberator "uses her shield to cast protective skills" — shield is a mechanical component of the support kit but weapon-slot semantics unclear.
</content>
</invoke>