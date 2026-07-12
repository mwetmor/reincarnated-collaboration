# Dossier — d2 Sacrifice (Paladin)

**Mode:** A (analytical)
**Commissioner:** gandalf (via Matt's usage-offload directive, 2026-07-12)
**Roster target:** K26 (adjacent to blood-family — commission flags as "arguably negative-canon; recommend shipped/negative status, Matt rules")
**Priority:** LOW
**Corpus gap confirmed:** No Sacrifice record in `canon-corpus-d2.jsonl`
**Crawl date:** 2026-07-12

---

## Identity

**Game:** d2 (Diablo 2 / Diablo 2 Resurrected)
**Patch/era span:** D2 original (2000) — D2R (ongoing); Sacrifice has been in the Paladin skill tree since launch. Never meta-viable as a primary build skill.
**Canon tier:** negative (recommended; see §7 — born-bad category per §9.6 v2.2 FOLD: "born-bad (trap skills: Impale, Sweep)")
**Folk names:** "Sacrifice Paladin," "Sacrificin" (extremely niche; forum-level folk naming only, not mainstream)
**Shipped / negative-canon status:** NEGATIVE CANON RECOMMENDED — see recommendation section below.

## Skill mechanics

Sacrifice (Paladin skill, D2):
- Deals 185% weapon damage per hit
- Inflicts 8% of damage dealt as self-damage to the Paladin on each hit
- Synergy with Fanaticism (Conviction / Holy Bolt / Zeal) for damage bonuses
- Requires sufficient Life Steal (≥16% Nightmare / ≥24% Hell) to negate the self-damage
- Holy Shield (a prerequisite in the same tree) is always taken alongside it

Community assessment: "Each hit landed with Sacrifice inflicts 8% of its damage on the Paladin. This effect is potentially very deadly, and subsequently this skill is seldom used." The skill is almost universally used as a SYNERGY INVESTMENT for Zeal (not as a primary attack), because Sacrifice synergizes with Zeal's damage formula. Building Sacrifice as the PRIMARY attack is extremely rare.

## Recommendation: NEGATIVE CANON (Matt's ruling requested)

**Arguments for NEGATIVE CANON status:**
1. The skill meets the "born-bad" criterion: it has a prohibitive self-damage mechanic that makes primary use consistently lethal without very specific itemization
2. No community-named build exists where Sacrifice is the PRIMARY loop (it appears only as a SYNERGY SKILL in Zeal/Hammerdin builds)
3. The "community-named mechanical loop" criterion (§1 grain law) is not satisfied — "Sacrifice Paladin" is a forum curiosity, not a recognized build archetype
4. The self-damage is not a design-interesting trade-off that generates interesting builds (unlike RF which has rich self-damage economy design); it is simply a poorly-calibrated early D2 skill that the community has never found a satisfying way to build around

**Arguments for SHIPPED status (negative-twin value):**
1. Sacrifice IS useful as a SYNERGY SKILL — investing points in it (without casting it) boosts Zeal damage; this "negative primary, positive synergy" pattern is itself design-interesting
2. It provides evidence for the GX-06 (self-damage economies) family as a FAILED implementation — alongside D4 Blood Surge (another self-damage skill with adoption challenges)
3. As a "Zeal synergy" note on an existing record (d2-zeal-paladin if one is minted), it's useful without needing a standalone row

**Legolas recommendation:** Flag as NEGATIVE CANON with `negative: true`. Retain as a negative-canon entry specifically for GX-06 evidential value (self-damage economy that FAILED to produce a build identity). Matt's ruling requested per commission.

If Matt confirms NEGATIVE: mint as `d2-sacrifice` with `negative: true`, `canon_tier: negative`, and neg_twin pointing to the GX-06 positive exemplar (PoE1 Blood Magic RF or D4 Blood Mage).

## Engine-prefix claims (for completeness, regardless of negative status)

| Slot | Value | Confidence | Evidence |
|---|---|---|---|
| attr | STR | HIGH | Paladin = STR archetype in D2; all Paladin physical skills scale with STR/weapon damage |
| range | MELEE | HIGH | Sacrifice is a melee attack skill; direct weapon strike |
| tempo | HIGH | MED | If used as primary attack: rapid weapon strikes (attack speed determines cadence); HIGH when viable |
| amp | FLAT | MED | 185% weapon damage = consistent flat multiplier per hit (no special per-hit variance) |
| proxy | SOLO | HIGH | No proxy; pure solo melee |
| commitment | INSTANT | HIGH | Single melee strike; instant; no wind-up or channel |

## Raw descriptors (not engine keys)

**geo:** Single-target melee hit; no AoE; point-contact damage.

**ctrl:** No CC; pure melee strike.

**mob:** Standard Paladin mobility (walk/run); no special movement skill tied to Sacrifice.

**def:** The skill's self-damage IS the defining design problem: no defensive identity; the build is defined by its fragility (self-damage makes it softer than any other Paladin build).

**econ:** Self-damage as implicit cost: 8% of damage dealt = life drain proportional to damage output. With Crushing Blow (reduces monster HP by fixed %) the interaction becomes especially dangerous (Crushing Blow → 8% of very large damage → extreme self-damage). Unique failure mode: the BETTER you perform, the faster you kill yourself.

**elem:** Physical primary.

## Sources

- Sacrifice (Diablo II) Fandom Wiki: https://diablo.fandom.com/wiki/Sacrifice_(Diablo_II) — mechanic confirmation
- diablo2.diablowiki.net/Sacrifice — community assessment text
- rankedboost.com D2 Sacrifice builds — confirms rarity of primary-use builds
- Knowledge base (kb) — D2 Paladin skill mechanics from training data
- V4-r2 §F4 mint-list (gandalf, 2026-07-12): "LOW | d2 Sacrifice | K26 | arguably negative-canon — recommend shipped/negative status, Matt rules"

## Knowledge gaps

- Whether D2R introduced any balance changes to Sacrifice that made it more viable (patch history post-2021)
- Exact life steal breakpoints for viability on Hell difficulty (16%/24% were cited; exact mechanics in D2R vs classic may differ)
