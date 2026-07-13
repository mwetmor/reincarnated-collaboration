# Research — Q28 IP-Clearance Probe: Player-Facing Dev-Log Atlas + Primary Hook — 2026-07-13

**Mode:** A (analytical)
**Commissioner:** gandalf (Q28 gate, `canonical/matt_decision_needed/2026-07-13-ip-clearance-devlog-and-hook-surface.md`)
**Date:** 2026-07-13
**Purpose:** Evidence base for Matt's risk-acceptance decision on player-facing publication of Atlas/dev-log with retained game titles and the revised primary hook.

---

> **⚠ MANDATORY BOUNDARY:** This dossier is a research probe — an evidence base. It informs but does NOT substitute for qualified legal review. Every finding below is secondary (legal commentary, practitioner articles, published case law) or tertiary (industry practice, community norms). No finding here constitutes legal advice, and no finding here constitutes a clearance. Matt's decision is a risk-acceptance call on whether to proceed under the informed posture this research documents, or to commission counsel.

---

## Summary (5 sentences)

Copyright exposure on the Atlas/dev-log content is low and well-grounded in established law: game mechanics, rules, and short names are not copyrightable, and the project's derived build names + mechanical descriptions sit cleanly inside this protection. Trademark exposure is the real residual: game titles (d2, poe1, chronicon, le) retained in the public register are others' marks, and commercial-adjacent use triggers nominative fair use analysis, which is defensible under the three-prong test but not guaranteed. Industry norms for build-database/theorycraft sites are favorable as analogues — Maxroll, Icy Veins, and poe.ninja use game titles and skill/class names freely with non-affiliation disclaimers and no documented C&Ds from GGG, Blizzard, or other ARPG publishers. However, those sites operate in an explicitly editorial/commentary role; our public dev-log Atlas must establish and sustain that same editorial posture to benefit from the same norms. The hook change from "ARPG meets Shadows of Mordor" to "Every build the genre ever made. One arena. Reap. Die. Rise." removes the most exposed use (named-franchise headline promotional claim) and the residual "every build the genre ever made" language reads as non-actionable puffery under standard FTC and common-law doctrine.

---

## Findings by Research Question

---

### Q1 — Nominative fair use for trademarks in games/software: stated boundaries for using competitor game titles as factual provenance

**Status: CONFIRMED (established case law; application to this use = PARTIAL)**

**Established framework:**
Nominative fair use is a recognized affirmative defense to trademark infringement under the Ninth Circuit's test from *New Kids on the Block v. News America Publishing*, 971 F.2d 302 (9th Cir. 1992). The three-prong test:

1. **Necessity prong:** The product or service in question is not readily identifiable without use of the trademark (i.e., there is no practical alternative to naming it).
2. **Minimal use prong:** Only so much of the mark is used as is reasonably necessary to identify the product or service.
3. **No false endorsement prong:** The user does nothing that would, in conjunction with the mark, suggest sponsorship or endorsement by the trademark holder.

The defense has been applied in the Ninth Circuit in *Toyota Motor Sales, USA, Inc. v. Tabari* (9th Cir. 2010) — domain name use of "Prius" held to qualify under prong 1 (no substitute for naming the car) and prong 2 (not prominently displayed). The court emphasized that prong 3 is the operative risk point: any framing that creates an impression of commercial affiliation defeats the defense.

**Application to our use (game titles as provenance attribution):**

| Prong | Assessment | Risk |
|---|---|---|
| 1 — Necessity | Using d2/poe1/chronicon/le to identify which game a build came from is the only unambiguous way to provide factual provenance. Alternative (genre-era bucket only) loses specific attribution. Prong 1 satisfied. | LOW |
| 2 — Minimal use | Retaining game titles as provenance labels (not logos, not prominent display, not tagline use) satisfies minimal-use if the identifiers are used inline as attribution and not as headline branding. | LOW-MED (depends on visual hierarchy on the page) |
| 3 — No false endorsement | The risk. Editorial-homage framing + explicit non-affiliation disclaimer is the standard posture to satisfy prong 3. Failure mode: any layout or language that reads as "endorsed by," "official," "partnered with," or "featuring" the named franchise. | MED (manageable with explicit disclaimer) |

**Practitioner consensus (GameDeveloper.com, LegalMovesLawFirm.com, 2026):** Industry legal commentary confirms nominative fair use applies to game-title references in marketing descriptions with careful handling. Recommended practice: use only necessary text (no logos), include non-affiliation disclaimer, use the mark in narrative/descriptive context rather than as a headline claim.

**Key risk point for our specific use:** The dev-log Atlas is player-facing and commercial-adjacent (linked to a Steam product). This is a higher-scrutiny context than a purely editorial fan site. The difference between "safe editorial" and "risky promotional" often turns on whether the named franchise's goodwill is being *used to sell* (risk) versus *used to attribute* (defensible). A dev-log documenting build provenance is closer to attribution; a store-page tag line is closer to selling.

---

### Q2 — Copyright on game mechanics/rules/short names: established position

**Status: CONFIRMED (clear law; negligible residual risk for our content)**

**Primary authority:**
*Tetris Holding, LLC v. Xio Interactive, Inc.*, 863 F. Supp. 2d 394 (D.N.J. 2012): "The rules and play mechanics of a game are not copyrightable... [copyright] extends only to the particular expression of those ideas." The court distinguished protectable expression (the specific visual tiles, their appearance, their particular animation) from unprotectable ideas (falling blocks, clearing rows, board geometry).

**Statutory foundation:**
17 U.S.C. § 102(b): "In no case does copyright protection for an original work of authorship extend to any idea, procedure, process, system, method of operation, concept, principle, or discovery..."

37 C.F.R. § 202.1(a): Words, short phrases, slogans, titles, and names are not copyrightable.

**Downstream case law:** *Spry Fox LLC v. LOLApps Inc.* (W.D. Wash. 2012) — Triple Town cloning case: held that game mechanics and rules are not copyrightable; visual expression and specific narrative elements are.

**Application to our content:**
- **Build names** (derived labels like "Enigma Teleporter," "Ancestral Warchief Totem") — short phrases, not copyrightable.
- **Mechanical descriptions** (tempo, range, proxy mechanics, econ patterns) — descriptions of rules/systems, not copyrightable.
- **Engine-prefix claims** (attr/range/tempo/amp/proxy/commit) — abstract taxonomic labels, not copyrightable.
- **Our specific expression** (the particular writing in dossiers, the Atlas layout, the dev-log prose) — IS copyrightable, but that's our IP, not risk.

**Residual risk:** Near-zero on the copyright axis. The content describes mechanics and attributes builds to their games of origin using short phrases. None of this is the kind of specific creative expression that copyright protects in the plaintiff's favor.

---

### Q3 — Industry norm: how build-database/theorycraft sites use game + skill/class names; documented C&Ds or takedowns

**Status: CONFIRMED (favorable norms; no documented C&Ds found in ARPG space)**

**Observed industry practice:**

| Site | Game titles used | Skill/class names used | Affiliation | Documented C&D |
|---|---|---|---|---|
| Maxroll.gg (IGN Entertainment) | PoE1, PoE2, D3, D4, Last Epoch, Lost Ark | Full skill names, gem names, class names | Non-affiliated; "not endorsed by" disclaimers | None found |
| Icy Veins | D3, D4, WoW, PoE, FFXIV | Full skill/class names | Non-affiliated | None found |
| poe.ninja | Path of Exile (explicitly) | Full skill gem names, league names, item names | Uses official GGG public API; "Path of Exile is a trademark of Grinding Gear Games" footer attribution | None found |
| PoE Vault | Path of Exile (explicitly) | Full skill/class/item names | Non-affiliated disclaimer | None found |

**GGG (Grinding Gear Games) community policy:** GGG provides public APIs for build data and poe.ninja integration. GGG has publicly acknowledged and praised community sites including poe.ninja. No documented C&D or takedown action against any ARPG theorycraft site found in this probe.

**Blizzard/Diablo:** Maxroll and Icy Veins operate prominent D3/D4 coverage with full class/skill name usage. No documented C&Ds found. Blizzard maintains fan content policies that explicitly permit fan sites, guides, and commentary.

**Standard disclaimer text observed (poe.ninja):** "Path of Exile is a trademark of Grinding Gear Games. Path of Exile ninja is not affiliated with or endorsed by Grinding Gear Games."

**Distinction relevant to our case:** These sites operate in a clearly editorial/commentary role — their commercial model is advertising revenue, not a competing game product. Our Atlas is part of the promotional surface for a competing game product. This distinction is meaningful for nominative fair use prong 3 analysis (potential impression of commercial affiliation). It does not invalidate our use; it means our non-affiliation disclaimer and editorial-homage framing carry more weight than they would on a purely editorial fan site.

---

### Q4 — Comparator games homaging genre without naming franchises: store page framing

**Status: PARTIAL (consistent pattern found; no formal study; genre-generic framing is the dominant norm)**

**Hades (Supergiant Games) — gold-standard example:**
Steam short description: *"Defy the god of the dead as you hack and slash out of the Underworld in this rogue-like dungeon crawler from the creators of Bastion, Transistor, and Pyre."*

Key observation: **Hades does not reference any external franchise by name.** The references are to Supergiant's own prior games only. Genre framing = "rogue-like dungeon crawler" (generic). This is the highest-profile recent example of a genre-defining indie game using pure genre-generic + self-referential framing on its store page.

**Vampire Survivors (Poncle) — another relevant example:**
Steam description: *"Mow down thousands of night creatures and survive until dawn! Collect coins, grab upgrades, and evolve your weapons."*
No external franchise references. Genre tags (roguelike, bullet heaven, survival) are the framing mechanism.

**Dead Cells (Motion Twin):**
Steam description: references "roguevania" (portmanteau of genre descriptors). No external franchise references.

**Pattern across successful genre-homage indie games:** The norm is pure genre-generic framing on official store pages. No major indie game found in this probe uses a competing franchise's name in its Steam short description or headline positioning.

**Notable exception searched (not found):** Could not confirm a commercially successful Steam-listed game that uses named competing franchise titles in its primary store description. The "ARPG meets Shadows of Mordor" framing that the hook change retires would have been unusual by industry norms, not just legally risky.

**Implication for our framing:** "Every build the genre ever made. One arena. Reap. Die. Rise." aligns with industry norm (genre-generic, no franchise names). The Atlas/dev-log that retains game titles (d2, poe1, etc.) in its body content is a separate surface from the store-page headline — which matters for the two-register split analysis.

---

### Q5 — Steam/storefront policy on referencing other games' trademarks in store pages/trailers/marketing

**Status: PARTIAL (policy framework found; explicit rule on competitor-name usage in descriptions not located)**

**Steam's own trademark policy (Steamworks branding guidelines):** Valve's published branding guidelines address USE OF STEAM'S OWN MARKS (not third-party game title use in descriptions). The guidelines govern how partners use the Steam logo and "Steam" brand — they do not directly address whether Store descriptions may reference competing game titles.

**Steam community guidelines (content prohibition):** "Character or game names may not violate any third party's trademark right, copyright, or other proprietary right, or which may mislead other members." This applies to user-generated content; it implies a general prohibition on misleading trademark use in Store content, but does not specifically define "mislead" in the context of comparative references.

**Steam enforcement model (confirmed via community discussions):** Valve enforces trademark complaints reactively — trademark holders must file their own complaint; Valve does not proactively screen store descriptions for third-party trademark references. This means: (a) the risk is from a trademark holder complaint, not Valve proactive enforcement; (b) no published case of Valve removing a game from Steam for comparative references in its description found.

**Practical implication:** Steam policy does not create a bright-line prohibition on referencing competitor game titles in store descriptions. The risk is the trademark holder filing a complaint, which then triggers Valve review. This is consistent with the legal analysis in Q1: nominative fair use + editorial framing + non-affiliation disclaimer is the operative posture.

**Gap:** Steamworks developer documentation for store page content policies was not fully fetched in this probe (partner.steamgames.com — potential login wall). This is a "what still needs a lawyer" item if Steam store-page compliance is a specific gate.

---

### Q6 — Puffery vs. false-advertising line for "every build the genre ever made" style superlative claims

**Status: CONFIRMED (puffery doctrine clearly applies to this claim type)**

**Puffery doctrine:**
Under common law and FTC doctrine, "puffery" = vague, subjective, or hyperbolic promotional language that no reasonable consumer would take as a literal factual claim. Puffery is not actionable as false advertising. The FTC does not pursue subjective superlatives.

**FTC standard (15 U.S.C. § 45):** Unfair or deceptive trade practices — applies to OBJECTIVE claims that are measurable and likely to deceive. Subjective claims ("greatest," "every," "best") are puffery.

**"Every build the genre ever made" analysis:**
- "Every build" is a categorical superlative. It is:
  - Non-measurable (no consumer can verify what "every build the genre ever made" means precisely)
  - Genre-aspirational in framing, not a specific factual inventory claim
  - Consistent with community-canon language ("the genre's greatest hits")
- **Verdict: Puffery.** This language does not trigger false-advertising liability under standard doctrine.

**Risk vector (not current, but worth noting):** If the claim shifted to an objective form — e.g., "contains all 2,847 historically documented ARPG builds" — it would become a measurable factual claim requiring substantiation. The current "every build the genre ever made" framing avoids this because it is non-enumerable and genre-aspirational.

**Adjacent risk (defamation/disparagement):** Not applicable. The claim does not assert anything negative about a named competitor.

**"One arena" and "Reap. Die. Rise.":** Both are non-measurable and subjective. No actionability found.

---

### Q7 — Defensive value: does stripping skill/class marks while retaining game titles + genre-generic + community-canon framing measurably reduce trademark exposure?

**Status: PARTIAL (plausible meaningful reduction; no ARPG-specific litigation data; reasoning well-grounded)**

**What naming law §7.1 strips:**
Distinctive skill/class marks (e.g., "Wraithblow," "Ancestral Warchief," "Hammer of the Ancients," "Whirlwind," "Bladestorm") — these are GGG's, Blizzard's, and other publishers' specific creative labels. Stripping these removes the most granular layer of mark exposure.

**What the public register retains:**
Game titles as factual provenance labels (d2, poe1, chronicon, last epoch). These are the top-level marks.

**Defensive value of the strip:**
- Skill/class names are often the most distinctive and creative marks (designed by the publisher as product identifiers). Removing them is a meaningful reduction in the density of mark use.
- Game titles are more generic labels (company names or abbreviations rather than distinctive product identifiers). Nominative fair use is more naturally available for these — they are the most-minimal label for identifying which game a build comes from.
- Net result: the §7.1 strip puts the remaining mark use at the least-distinctive, most-necessary layer — the layer where nominative fair use prong 1 (necessity) and prong 2 (minimal use) are both most easily satisfied.

**Community-canon framing defensive value:**
The editorial-homage / community-canon framing serves nominative fair use prong 3 most directly: it frames the use as tribute/attribution (non-commercial impression) rather than endorsement. Published practitioner analysis confirms that framing the use as "narrative context" rather than "brand claim" is the operative defense for prong 3.

**Explicit non-affiliation disclaimer:**
Standard practice across theorycraft sites (poe.ninja, Maxroll, Icy Veins). Provides a clean prong-3 anchor. Should be in the footer of any player-facing Atlas page.

**Quantification (unavailable):** No ARPG-specific trademark litigation data exists to quantify how much these postures reduce risk. This is a structural judgment — the posture is clearly better than not having it, but "measurably reduces" to a number is not achievable from public sources.

---

## What Still Needs a Lawyer

Ordered by materiality:

1. **The one open question that only counsel can answer:** Is the retained-game-title usage in our public dev-log Atlas, combined with the commercial context (it's linked to a Steam game for sale), sufficient to satisfy nominative fair use prong 3 in practice? The law is clear in principle; the application to a specific player-facing commercial-adjacent dev-log is a judgment call that requires a qualified IP practitioner to assess the actual Atlas content, layout, and framing.

2. **Jurisdiction selection:** Nominative fair use law varies by circuit. Ninth Circuit (where Valve is based, where most US gaming IP actions are filed) has the most favorable precedent (New Kids on the Block, Toyota v. Tabari). If the trademark holder sues in a different circuit, the test may differ. Counsel should confirm the operative jurisdiction and whether the three-prong test applies.

3. **Steamworks store-page content policy:** The Steamworks documentation for publisher store page requirements was not fully fetched in this probe. If there is a specific written policy about third-party trademark use in Steam store descriptions, it should be reviewed by counsel before the Atlas is published with Steam store page links.

4. **Individual mark owners' policies and known enforcement postures:** GGG (PoE) has a known community-tolerant posture (public APIs, explicit fan-site support). Blizzard (D2, D3) has historical fan-content policies but is more aggressive on commercial adjacent content. Chronicon's publisher is smaller. Counsel should check whether any of the retained game-title holders have unusually aggressive enforcement histories relevant to editorial/tribute uses.

5. **Standing trademark disclaimer text review:** The specific disclaimer language should be reviewed by counsel before publication. "Not affiliated with or endorsed by [publisher]" is standard but counsel should confirm this is the recommended minimum for the jurisdiction.

---

## Plain Read: Defensible-Editorial or Exposed-Promotional?

**Honest assessment based on research findings:**

The current posture — retained game titles in Atlas body content, genre-generic hook, community-canon framing, explicit §7.1 skill/class mark strip — reads as **defensible-editorial** rather than exposed-promotional, provided two conditions hold:

1. **Non-affiliation disclaimer is present and visible** on the Atlas/dev-log pages (standard practitioner recommendation; consistent with poe.ninja, Maxroll, Icy Veins norms).

2. **Game titles appear as inline provenance labels** (body text attribution), not as headline branding or prominent visual features (logo use, above-the-fold placement, "featuring Diablo II" style call-outs).

If either condition is violated — no disclaimer, or game titles appearing in positions that create an impression of commercial partnership — the posture shifts toward the exposed end.

**The hook change is a genuine improvement.** "ARPG meets Shadows of Mordor" = named franchise as the PRIMARY marketing hook = trademark used to sell, not to attribute. This is the most exposed pattern in the literature. The new hook ("Every build the genre ever made. One arena. Reap. Die. Rise.") removes that exposure entirely and is genre-generic + puffery-class superlative.

**The industry analog (theorycraft sites) is imperfect but favorable.** Build-database sites use the same game titles and skill/class names freely. They have operated without documented C&Ds for years. Our distinguishing factor (competing game product vs. pure editorial site) is real but is addressed by the editorial-homage framing and explicit disclaimer. The §7.1 strip further narrows the gap.

**The Hades precedent is instructive.** Supergiant's store page uses genre-generic ("rogue-like dungeon crawler") + self-referential framing (own prior titles), with no external franchise names. This is the industry gold standard for how to position a genre-defining indie game without trademark exposure. Our store page should follow this pattern; the Atlas/dev-log, if structured as an editorial archive separate from the store page, is a different surface with more tolerance for named provenance attribution.

---

## Knowledge Gaps Not Resolved

| Gap | Assessed impact | Suggested next source |
|---|---|---|
| Steamworks publisher store-page content policy — not fully fetched (potential login wall) | MED — could contain relevant written rules | Partner Steamworks documentation (requires Valve partner account access); counsel review |
| Individual publisher enforcement posture (esp. Blizzard for D2/D3) | MED — Blizzard historically more aggressive than GGG | Counsel due diligence on Blizzard's known fan-content/commercial-adjacent enforcement pattern |
| Whether Ninth Circuit three-prong applies vs. other circuits | MED — jurisdiction-dependent | Counsel analysis at filing/publishing stage |
| ARPG-specific trademark litigation data | LOW (no litigation found = null evidence; does not prove safety) | Legal database (Westlaw/Lexis) search by counsel |
| Specific disclaimer language approved for our context | LOW (standard text is clear; jurisdiction nuance is counsel's call) | Counsel review of specific disclaimer before player-facing publish |

---

## Source List

**Primary sources (published case law and statutory):**
- *New Kids on the Block v. News America Publishing*, 971 F.2d 302 (9th Cir. 1992) — nominative fair use three-prong test
- *Toyota Motor Sales, USA, Inc. v. Tabari*, 610 F.3d 1171 (9th Cir. 2010) — prong-by-prong application; "only so much of the mark as necessary"
- *Tetris Holding, LLC v. Xio Interactive, Inc.*, 863 F. Supp. 2d 394 (D.N.J. 2012) — game mechanics not copyrightable; idea-expression dichotomy applied to games
- *Spry Fox LLC v. LOLApps Inc.*, No. 2:12-CV-00147-RAJ (W.D. Wash. 2012) — game rules not copyrightable; cloning case
- 17 U.S.C. § 102(b) — idea-expression dichotomy statutory text
- 37 C.F.R. § 202.1(a) — short phrases, titles, names not copyrightable
- 15 U.S.C. § 45 — FTC "unfair or deceptive trade practices" standard (puffery boundary)

**Secondary sources (practitioner articles, legal commentary):**
- "Can you use another game's trademarked name to describe your own?" — Game Developer (gamedeveloper.com), accessed 2026-07-13: https://www.gamedeveloper.com/business/can-you-use-another-game-s-trademarked-name-to-describe-your-own-
- Strebeck Law: "Can you use another game's trademarked name to describe your own?" — https://strebecklaw.com/can-you-use-another-games-trademarked-name-to-describe-your-own/ — accessed 2026-07-13
- LegalMovesLawFirm.com: "Can you use other companies' trademarks in your video game?" — https://legalmoveslawfirm.com/other-companies-trademarks-video-game/ — accessed 2026-07-13
- Steam Branding Guidelines (Steamworks Documentation): https://partner.steamgames.com/doc/marketing/branding — accessed 2026-07-13

**Tertiary sources (industry practice, store pages, site practice):**
- Hades Steam store page (Supergiant Games) — https://store.steampowered.com/app/1145360/Hades/ — fetched 2026-07-13; confirmed no external franchise name references; "rogue-like dungeon crawler" genre framing only
- Maxroll.gg home/PoE2 hub — https://maxroll.gg/poe2 — accessed 2026-07-13; confirmed game title + skill/class name usage without documented publisher objection
- Icy Veins home — https://www.icy-veins.com/ — accessed 2026-07-13; confirmed game title + skill/class name usage without documented publisher objection
- poe.ninja (via earlier session research — "Path of Exile is a trademark of Grinding Gear Games" disclaimer present)
- Steam community discussions on trademark reporting — https://steamcommunity.com/discussions/forum/0/5413843407447267537/ — accessed 2026-07-13; confirmed reactive (not proactive) enforcement model

---

*Filed: legolas, 2026-07-13. Addressed to: gandalf (Q28 gate synthesis) and Matt (risk-acceptance decision). Does not constitute legal advice.*
