# Research — ARPG screen-space distortion: does genre precedent put it at T1? — 2026-08-25

**Mode:** A (analytical)
**Commissioner:** knight-rider
**Agent:** legolas (UNKNOWN-RESEARCHER)
**Scope:** verify five genre-history claims made by Grok (web search DISABLED, therefore all from model memory) in `knight-rider/returns/2026-08-25-grok-attacked-the-ruling-and-refuted-it-with-our-own-receipts.md` § 6.
**Access date for all sources:** 2026-08-25

> ⚑ **This document does not adjudicate the design question.** Whether *Reincarnated* should reserve screen-space distortion is gandalf's seam and Matt's call. Genre precedent is an input, not a verdict. Several findings below cut against Grok and several cut against gandalf; none of them decide what our game should do.

---

## Summary

**Grok's counterexample list is materially unreliable as stated, but not fabricated.** The skills exist and most are early; the *distortion* attribution is the part that does not survive. Every specific "this early skill uses screen-space refraction" claim is **UNVERIFIABLE from any accessible source** — the one place I could get to primary evidence, it went the other way.

Three hard results:

1. ⚑ **Grok's single strongest-sounding claim — "D4's VFX bible treats refraction as MATERIAL, not a tier gate" — is REFUTED on the closest public artifact to a D4 VFX bible.** Blizzard's own Lead Visual Effects Artist published D4's VFX philosophy in December 2021 and it states the *tier-gate* rule almost in gandalf's words: *"we reserve visually loud FX for powerful skills, like ultimate abilities, while weaker skills meld into the background."*
2. ⚑ **But the same document also states Grok's rule.** D4 ships a documented system that scales *"the size, intensity, and duration of a skill"* continuously with skill points, +Skill affixes, legendaries and glyphs. **The shipped reference title uses BOTH axes.** They are orthogonal there, and the debate has been treating them as alternatives.
3. **The D3-launch causal claim is REFUTED and inverted.** The documented D3 launch failure was server/DRM (Error 37). The visual controversy is a *different, earlier* event (2008), Blizzard publicly **refused** to desaturate, and the reason Jay Wilson gave is the exact inverse of Grok's story — Blizzard says desaturation *destroyed* readability rather than restoring it.

---

## Method note, stated up front because it bounds several verdicts

Screen-space distortion is a **visual** property. Settling it per-skill would require frame inspection of shipped builds. I have no way to verify video frames — I can cite a video URL but I cannot see it, and citing a timestamp I have not observed would be exactly the fabrication class this commission exists to prevent.

So my evidence ladder was: (1) first-party dev statements → (2) in-game graphics-option tooltips that *name* the render feature → (3) dedicated-wiki VFX descriptions → (4) labelled community consensus. Where a claim reached none of those rungs, the verdict is **UNVERIFIABLE**, and I say which rung it fell off.

**One consequence worth stating plainly:** an in-game "Distortion" graphics toggle proves the *engine* ships screen-space distortion. It does **not** prove which skills use it. I found the former for Diablo IV and could not find the latter for any title.

---

## Per-claim verdicts

### CLAIM 1 — Path of Exile: Cyclone, Flame Dash, Lightning Warp — *"warp at gem level 1"*

**Verdict: MIXED — availability half CONFIRMED-with-one-REFUTATION; distortion half UNVERIFIABLE.**

**Availability (checkable, and checked):**

| Gem | Required character level at gem level 1 | Acquisition |
|---|---|---|
| **Cyclone** | **28** | Act 3 quest reward ("Sever the Right Hand"); drop level 28 |
| **Flame Dash** | **10** | Act 1 quest reward ("The Caged Brute") |
| **Lightning Warp** | **10** | Act 1 quest reward ("The Caged Brute") |

Source: PoEDB (`poedb.tw/us/Cyclone`, `/Flame_Dash`, `/Lightning_Warp`). *(poewiki.net is behind an Anubis JS challenge and is not agent-fetchable; PoEDB mirrors the same game data and was used instead.)*

- **Flame Dash / Lightning Warp: CONFIRMED early.** Both are Act 1, level 10.
- **Cyclone: REFUTED as early.** Level 28, Act 3. Grok named it *"their Whirlwind analogue"* — i.e. it is the one item on the list load-bearing for the melee-combo comparison, and it is the one item that is not early.
- ⚑ **"at gem level 1" is a vacuous qualifier.** *Every* PoE gem starts at gem level 1. The binding gate is the character-level requirement, which is what the phrase reads as promising and is not what it says. This is a phrase that will pass a casual reader as a specific verified fact while asserting nothing.

**Distortion (the actual claim): UNVERIFIABLE.** No source at any rung of the ladder describes screen-space refraction on any of the three. I searched GGG patch notes, GGG forums, and PoE wikis; the PoE forum's own "distortion" hits are about an unrelated PoE2 aura (Overwhelming Presence) drawing grey stripes on monsters.

⚑ **Probable name-collision, flagged because it is the most likely origin of the claim.** **Lightning Warp's "warp" is locomotion, not optics.** Sources describe it as a delayed teleport dealing lightning AoE at the departure point and the arrival point. Nothing in the skill's documented behaviour bends the scene. A model recalling "PoE has a level-10 skill called Lightning *Warp*" and outputting "warp at gem level 1" produces a sentence that is true about the *name* and unsupported about the *renderer*.

---

### CLAIM 2 — Diablo 3: Wizard Teleport, Disintegrate; Whirlwind motion blur

**Verdict: availability CONFIRMED (but trivially) · "motion blur" as evidence of screen-space refraction REFUTED as argumentatively empty · underlying distortion claim UNVERIFIABLE.**

**Availability:** Teleport unlocks at **level 22** (Wizard, Defensive); Disintegrate at **level 21** (Wizard, Secondary); Barbarian Whirlwind at **level 20** (Secondary). Sources: diablowiki.net / Diablo Fandom.

⚑ **"NOT ultimates" is trivially true of D3 and should carry no weight.** *Diablo 3 has no ultimate-ability tier.* Skills unlock on a level curve to 30 and runes continue unlocking to 60. There is no categorical top-tier slot in D3 for anything to be reserved *to*, so D3 cannot supply evidence either way about tier-reservation. Grok cited it as though it could.

**Distortion — this is exactly the failure mode knight-rider predicted, and it is realised:**

- diablowiki's description of Whirlwind's graphic: *"the weapon visible tracking around in a circle, **leaving a glowing light as it spins**."* A **glowing additive weapon trail** is not a screen-space post-process; it does not sample the scene behind it and nothing bends. **This is "technically an effect, argumentatively empty" precisely as flagged.**
- JangaFX's technical breakdown of D3's VFX methods lists layered alpha-multiplied scrolling noise (`Tex1.A * Tex2.A * 2`), hand-painted gradient coloring, alpha-composite blending, and per-particle randomisation — and characterises the approach as achieving its motion through procedural texture variation *"rather than traditional flipbook animations or **advanced shader distortion techniques**."* Secondary source (a VFX-tooling vendor's analysis), but a technically literate one and directly on the disputed point.
- The Julian Love GDC 2013 talk *"Technical Artist Bootcamp: The VFX of Diablo"* (Blizzard) is the primary source that would settle it. **Video is free on the Internet Archive (`archive.org/details/GDC2013Love`) and YouTube (`youtube.com/watch?v=UJI7vPiu-g4`); GDC Vault is paywalled.** The Archive item ships **no transcript or subtitle track** (mp4/ogv/mp3/ogg only). **I cannot verify video content and did not.** ⚑ **This is a named, located, un-consumed primary source — the single highest-value follow-up in this document if anyone wants the D3 question closed properly.**

⚑ **A datum Grok did NOT cite that is stronger for his position than the ones he did.** D3's **Slow Time** (Wizard, **Defensive, unlocks level 16**) is described as *"a bubble of warped time and space"* with *"a distortion effect from the slow time field."* If that description is accurate to the shipped renderer, it is a **level-16, non-ultimate, spatially-bounded distortion dome** — early, real, and *local*. **Note what shape that has:** it supports Grok's amplitude/extent distinction and simultaneously supports gandalf's instinct, because it is a bounded local dome and not a viewport bend. Source is a wiki summary, not primary; treat as **suggestive, not established.**

---

### CLAIM 3 — Diablo 4: Incinerate / Teleport / Frost Nova / Hurricane / Whirlwind, and *"D4's VFX bible treats refraction as MATERIAL, not a tier gate"*

This claim has four separable parts and they get four different verdicts.

**(3a) D4 ships screen-space distortion as an engine feature — CONFIRMED.**

Diablo IV exposes a graphics option whose own tooltip names the feature:

> **"Distortion — Controls whether screen space distortion is applied. Decreasing this may improve performance."**

Corroborated by two independent sources: an official Blizzard forums PC Bug Report thread (2023-07, filed *because* the "decreasing this" wording is wrong for what is in fact **a checkbox, not a slider**), and the vhpg settings reference which quotes the tooltip in full. **This is the strongest single piece of evidence in Grok's favour anywhere in the commission** — D4 unambiguously ships a screen-space distortion post-process pass.

**(3b) Availability / tier placement — CONFIRMED with one correction.**

D4 skill-tree clusters gate on points spent, unlocking at roughly: **Basic L1 · Core L3 · 3rd cluster L4 · 4th cluster L8 · 5th cluster L13 · Ultimate L19** (Maxroll).

| Skill | Cluster | Approx. gate |
|---|---|---|
| **Incinerate** (Sorc) | **Core** (2nd) | ~L3 — Grok correct, genuinely early |
| **Teleport** (Sorc) | **Defensive** (3rd) | ~L4 — Grok correct |
| **Frost Nova** (Sorc) | **Defensive** (3rd) | ~L4 — Grok correct |
| **Whirlwind** (Barb) | **Core** | ~L3 — Grok correct |
| ⚑ **Hurricane** (Druid) | ⚑ **Wrath (5th cluster)** | **~L13 — Grok listed this as "core". It is not.** |

Sources: Fextralife D4 wiki (Frost Nova and Teleport pages both state *"is part of the Defensive Cluster"*), Fextralife Druid Skills (Hurricane → Wrath cluster), Maxroll skill-tree overview. Hurricane is not an ultimate either — Grok is closer than gandalf here — but "core" is wrong, and Hurricane is the one item on his D4 list that is a *sustained area* skill rather than a point effect.

**(3c) Per-skill distortion attribution (Incinerate heat-haze, Teleport, Frost Nova shimmer, Barb WW dust/blur) — UNVERIFIABLE.**

I could not find any source at any rung attributing the Distortion pass to any named skill. The only characterisation I found of *what* the setting covers is tertiary (a settings-guide site describing it as "basically a heat distortion effect, around heat-emitting objects such as fires") and I do not consider that adequate to confirm a per-skill claim. **The engine feature is confirmed; its assignment to these five skills is not.**

⚑ **And one first-party datum points away from it.** Briggs's own description of D4 Whirlwind names its VFX components explicitly: *"in bright daylight, the blade reflects light from the sun. In a dark dungeon, it will reflect more subtle light sources, like torches. **The dust kicked up by the skill is also lit by the environment**, so it blends artfully into the world."* **Lit particles and a reflective blade. No distortion, no blur, in the lead artist's own account of that exact skill.** Grok's "Barb WW dust/blur" is half-right — the dust is real and it is described — but the entry is on his list to evidence *refraction*, and the primary source describes the dust as **lighting-integrated particles**, which is the non-distorting category.

**(3d) "D4's VFX bible treats refraction as MATERIAL, not a tier gate" — the artifact is UNVERIFIABLE; the assertion is REFUTED.**

**No public "Diablo IV VFX bible" exists** that I can find. Searches for a published bible/style-guide surface only VFX showcase reels, ArtStation portfolios, and a RealTimeVFX reference thread with no Blizzard-staff technical commentary. **Grok cited a document that, so far as the public record goes, is not a document.**

The nearest thing that *does* exist is first-party and authoritative: **Blizzard's Diablo IV Quarterly Update — December 2021**, whose VFX section is written by **Daniel Briggs, Lead Visual Effects Artist for Diablo IV**. It is a published statement of D4's VFX philosophy. On tier-gating it says the opposite of Grok:

> *"Our goal is to balance the primary, secondary, and tertiary reads to help you understand what is happening.* ⚑ ***To do this, we reserve visually loud FX for powerful skills, like ultimate abilities, while weaker skills meld into the background.*** *Each class has abilities that range from low to high in costs, cooldowns, and power. In tandem, classes have a range of visual intensity that increases with skill power."*

⚑ **Read the verb. "We reserve." A shipped AAA ARPG's lead VFX artist describing categorical reservation of visual loudness to the ultimate tier, in public, in the studio's own words.** Grok asserted the reference title has no such gate; the reference title says it does.

**The honest bound on this refutation, and it matters:** Briggs is talking about *"visually loud FX"* as a category. **He never uses the words distortion, refraction, or heat haze anywhere in the piece.** So Grok's *narrow* claim — that refraction *specifically* is keyed to material rather than tier — is **not directly contradicted; it is simply unevidenced in either direction.** What is refuted is the *principle* Grok invoked it to establish. He used "D4 doesn't tier-gate" to argue that tier-gating a VFX channel is invented; D4 says in writing that it tier-gates its loudest channel.

---

### CLAIM 4 — Grim Dawn: *"hits hard with coarse sprites + debris + hit-stop"*

**Verdict: MIXED — "coarse sprites + debris" partially supported; ⚑ "hit-stop" UNVERIFIABLE and contra-indicated.**

- **Coarse sprites:** partially supported. Grim Dawn is built on the **Titan Quest engine** (Wikipedia), which is the substrate for the claim about sprite/particle coarseness. I found no dev statement framing coarseness as an intentional impact strategy.
- **Debris:** supported in kind. Grim Dawn is documented as building on TQ with *"improved physics, location-specific damage effects, dynamic weather, a rotatable camera, dismemberment"* (Wikipedia).
- ⚑ **Hit-stop: no evidence found, and the available evidence leans against.** I found no source documenting hit-stop, hit-pause, or freeze-frame in Grim Dawn or the TQ engine. Contra-indications:
  - Crate Entertainment forum thread **"Grim Dawn could use better 'hit feedback'"** (2020-08-09). The OP — a 1,300-hour player — complains that *"visuals of most spells doesnt match their AoE"*, that camera shake is *"absurdly high, especially on a fast auto attack build"*, and that *"in big combats, many of the effects' sounds are constantly missing."* **Zantai (Crate) replied the same day**, calling the white-flash-on-hit mechanic *"rather gamey"* and questioning whether a camera-shake slider justified dev time; he later (2020-09-03) confirmed and fixed the sound-channel bug. **Hit-stop, hit-pause and stagger are not raised by anyone in the thread — not by the complainant, not by the developer.**
  - A community **"Combat Overhaul"** mod adds player strikes that **stagger enemies on hit** as a headline feature — i.e., it was absent from the base game.
- ⚑ **Incidental but load-bearing for Grok's own separate argument:** Grim Dawn **does** ship camera shake, and its community complains it is *excessive*. That is a data point for Grok's internal jab that camera shake is "the more exhausted signifier of the two" — and equally a data point that an over-spent signifier becomes something players switch off.

---

### CLAIM 5 — *"D3 launch was luminance/overdraw/self-occlusion — 'can't see the ground' — fixed with density sliders and desaturation, not beat surgery."*

**Verdict: REFUTED.** Every clause is wrong in a different way, and the last one is inverted.

**(a) What the D3 launch is actually documented for.** Diablo III launched 2012-05-15. The documented launch failure was **login-server saturation ("Error 37")** compounded by always-online DRM for single-player, with players locked out for hours to days; Blizzard resolved it with a server queue. Multiple contemporaneous and retrospective sources. **No documented launch-era "can't see the ground" visual crisis appears in the record.**

**(b) The visual controversy is a different event with a different date.** The art controversy dates to **WWI 2008**, when the revealed palette drew a *"too colourful / too WoW / too cartoonish"* backlash and a petition reported at **~52,000 signatures** demanding a return to a darker, gothic look. That is **four years before launch.**

**(c) "Fixed with desaturation" — REFUTED. Blizzard publicly refused.** Lead designer **Jay Wilson**, to MTV: ⚑ ***"There's no going back now"*** and ***"We really like this art style, and we're not changing it."*** The desaturated Diablo 3 images that circulated (e.g. Shacknews' "See Diablo 3 Desaturated in Action") were **fan mockups**, not a Blizzard change.

**(d) ⚑ And the reason Wilson gave is the exact inverse of Grok's causal story.** Wilson said the earlier *"modern, gritty"* art iterations were abandoned **because desaturation destroyed creature/environment separation**:

> *"You need to be able to tell those things apart fast, and you can't do that when your world is gray and your creatures are gray."*

He added that a uniformly desaturated world also flattens the player's sense of progression, *"because the area they're in looks like the area they were in 30 to 45 minutes ago."* **Grok offered desaturation as Blizzard's readability remedy. Blizzard's on-record position is that desaturation was the readability problem and colour was the remedy.** This is the sharpest inversion in the commission.

**(e) "Density sliders" — REFUTED on two independent counts.** D3's **Clutter Density** setting is real (Off/Low/Med/High). But:
  1. ⚑ **It predates launch.** It is documented in **beta** graphics guides, so it cannot be a fix applied in response to a launch problem.
  2. ⚑ **It does not govern effects.** It controls *"small, detailed textures, like you might see on the ground after a battle: corpses, blood, and the like"* — decorative ground props. Turning it off *"only removes some non-critical decorative items from the game world."* It has nothing to do with spell/effect density, which is the layer Grok's argument needs it to control.

**(f) The real phenomenon, correctly located.** Effect-clutter complaints in the Diablo line are genuine, **community-side, and long-running rather than launch-bound** — a DiabloFans thread worrying about four-player spell overload dates to **2009-09-23**, *before* launch and framed as a prediction (*"When you add up all of those spells plus the spells from the other three players… it get distracting"*), and the request for an option to reduce or hide **other players'** effects recurs continuously on official D3 and D4 forums to the present. ⚑ **I found no D3 patch note adding such an option.** *(Community consensus, explicitly labelled as such.)* So the clutter complaint is real and largely **unremedied** — which is neither the launch event Grok described nor the fix he described.

---

## ⚑ The thing nobody asked about — where the line actually sits

knight-rider asked for this specifically and said it was worth more than any individual claim. It is, and the answer came from one document.

**The shipped reference title uses BOTH axes at once, on different levels of the design. They are not alternatives, and the whole argument has been conducted as though they were.**

From Briggs, D4 Lead VFX Artist, same December 2021 post:

**Axis 1 — continuous amplitude escalation WITHIN a skill (Grok's rule, confirmed as shipped practice):**
> *"Once we have a class skill we are happy with, the VFX team adds the ability for developers to **dynamically change the size, intensity, and duration of a skill**. The visual intensity of a skill will increase as you stack upgrades and items that increase the power of that ability."*

Briggs later confirmed publicly (2023-03-29, @3DBriggs) that this shipped, and that intensity is driven by skill-tree points, +Skill affixes, skill-category affixes, plus legendaries, paragon nodes and glyphs. **Grok's "escalation lives in amplitude, duration and extent" is not a rhetorical construct — it names, almost term for term, a system Blizzard built and documented.**

**Axis 2 — categorical reserve ACROSS tiers (gandalf's rule, also confirmed as shipped practice):**
> *"we **reserve** visually loud FX for powerful skills, like ultimate abilities, while weaker skills meld into the background."*

⚑ **And now the part that neither knight-rider nor Grok nor gandalf raised, and which is the single most on-point sentence I found anywhere:**

> *"Several **ultimates** in our game will even allow you to **change the weather and lighting of the environment** for a limited duration."*

**Environmental response — the world itself visibly reacting to the player — is, in Diablo IV, by explicit first-party statement, an ULTIMATE-tier gesture.** That is not the same mechanism gandalf reserved, but it is the same *layer*, reserved at the same *altitude*, by the studio Grok cited as proof the altitude doesn't exist. Grok's entire counterexample list is local material effects on individual skills — which is precisely the category Briggs says *"melds into the background."*

**Two supporting observations in the same vein:**

- ⚑ **The escalation channels Briggs names do not include distortion.** *"We do not uniformly scale every piece of an effect when changing size and intensity; we modify things like **spawn rate, velocity, emissivity, and color ranges** to make certain the art still fits in the world of Diablo."* Four named channels for amplitude escalation. **Refraction is not one of them** — from the only first-party source on the exact question. This is a negative result and should be weighted as one (absence in a summary blog post is not absence in the shader library), but it is a negative result *at the precise point of dispute*.
- ⚑ **D4's Distortion control is a global on/off checkbox, not a quality slider.** Design consequence neither side raised: **any effect built on that channel is a channel some fraction of the playerbase simply does not have** — switched off for frames, or off because the tooltip invites switching it off. A signifier that a player can globally disable is a poor carrier for information you need them to receive. That is an argument about the channel's *reliability* that is independent of both the scarcity argument and the amplitude argument.

**Net characterisation, stated as carefully as the evidence permits:** in the one shipped ARPG where I could reach first-party VFX doctrine, the line sits at **loudness and world-alteration, not at mechanism.** Amplitude/duration/extent scale continuously and early (Grok's axis is real and shipped). *Loud* effects, and *environment-altering* effects specifically, are reserved to the ultimate tier (gandalf's axis is real and shipped). **Whether refraction sits above or below that line in D4 is exactly the question no accessible source answers.**

---

## Knowledge gaps not resolved

1. ⚑ **The Julian Love GDC 2013 talk, "Technical Artist Bootcamp: The VFX of Diablo" (Blizzard).** Free video at `archive.org/details/GDC2013Love` and `youtube.com/watch?v=UJI7vPiu-g4`; GDC Vault copy paywalled. **The Archive item carries no transcript or subtitle file — mp4/ogv/mp3/ogg only.** I cannot verify video and did not. This is the primary source that would close the D3 half of Claim 2 and is the highest-value single follow-up here. A human watching ~50 minutes settles it.
2. **Per-skill distortion attribution in D4.** Nobody appears to have published a before/after of the Distortion checkbox. A player with the game answers this in five minutes; no amount of searching does.
3. **Any PoE renderer documentation.** GGG has not published a VFX/shader philosophy piece comparable to Briggs's. `poewiki.net` is behind an Anubis JS challenge and is **not agent-fetchable** — PoEDB is the working substitute for game data but carries no VFX commentary. **Lane note for `legolas-crawler`: poewiki.net is DEGRADED-to-DEAD for agent access; route PoE gem data via `poedb.tw/us/<Skill_Name>`, which returns clean level/tag/acquisition rows.**
4. **The ArtStation Magazine "Diablo IV Art Blast" (July 2023)** — likely the richest remaining D4 VFX artifact. `magazine.artstation.com` returns **403** to agent fetch and the `worldstone.io` mirror refuses connections. Not read.
5. **Blizzard's Slow Time distortion description** rests on a wiki summary, not a primary source or observed frames. Suggestive, not established.

---

## Source list

**Primary (first-party developer statements)**
- Blizzard Entertainment — *Diablo IV Quarterly Update—December 2021*, VFX section by **Daniel Briggs, Lead Visual Effects Artist, Diablo IV**. https://news.blizzard.com/en-us/article/23746639/diablo-iv-quarterly-updatedecember-2021 — **the load-bearing source of this document.**
- Daniel Briggs (@3DBriggs), Twitter/X, 2023-03-29, on skill-intensity scaling — relayed by PCGamesN, https://www.pcgamesn.com/diablo-4/skill-intensity-explained
- Jay Wilson (Lead Designer, Diablo III), MTV News interview on the art controversy — *"There's no going back now" / "We really like this art style, and we're not changing it."* https://www.mtv.com/news/r2p5ub/diablo-iii-designer-talks-colors
- Zantai (Crate Entertainment), Crate forums, 2020-08-09 and 2020-09-03. https://forums.crateentertainment.com/t/grim-dawn-could-use-better-hit-feedback/102793
- Julian Love (Blizzard), *Technical Artist Bootcamp: The VFX of Diablo*, GDC 2013. https://gdcvault.com/play/1017660/Technical-Artist-Bootcamp-The-VFX (paywalled) · https://archive.org/details/GDC2013Love (free, no transcript) · https://www.youtube.com/watch?v=UJI7vPiu-g4 — **cited as located, NOT as consumed.**

**In-game data / tooltips**
- Diablo IV Distortion tooltip: *"Controls whether screen space distortion is applied. Decreasing this may improve performance."* — official Blizzard forums PC Bug Report, https://us.forums.blizzard.com/en/d4/t/distortion-setting-has-a-misleading-description/39269 · corroborated https://www.vhpg.com/diablo-4-distortion-setting/
- PoEDB gem data: https://poedb.tw/us/Cyclone · https://poedb.tw/us/Flame_Dash · https://poedb.tw/us/Lightning_Warp

**Secondary (wikis, technical analysis, press)**
- diablowiki.net — Whirlwind, Teleport, Disintegrate, Slow Time, Art controversy *(site is behind Cloudflare; content reached via search-engine extraction only, not direct fetch — treat quotes as second-hand)*
- Diablo Fandom — Whirlwind (Diablo III), Teleport (Diablo III), Incinerate/Hurricane (Diablo IV)
- Fextralife D4 wiki — Frost Nova, Teleport, Druid Skills, Hurricane. https://diablo4.wiki.fextralife.com/
- Maxroll — D4 Skill Tree Overview (cluster level gates). https://maxroll.gg/d4/getting-started/skill-trees
- JangaFX — *Exploring and Modernizing The VFX Methods of Diablo 3*. https://jangafx.com/insights/diablo-3-vfx-experiments
- Tom's Hardware — *Diablo III Performance, Benchmarked* (May 2012), Clutter Density. https://www.tomshardware.com/reviews/diablo-iii-performance-benchmark,3195-2.html
- GameFront — *Diablo 3 Beta Graphics Guide* (Clutter Density present pre-launch). https://www.gamefront.com/news/diablo-3-beta-graphics-guide
- Wikipedia — Grim Dawn (Titan Quest engine, dismemberment/physics). https://en.wikipedia.org/wiki/Grim_Dawn
- GameSpot / NBC News / GameWatcher — Diablo III Error 37 launch coverage, May 2012
- Shacknews — *Diablo 3 Color Controversy Revisited, See Diablo 3 Desaturated in Action* (fan mockups). https://www.shacknews.com/article/54697/diablo-3-color-controversy-revisited

**Tertiary — community, labelled as such**
- DiabloFans, *"Is Diablo 3 to visually busy?"*, opened by ScyberDragon 2009-09-23
- Official Blizzard D3/D4 forum threads requesting an option to reduce or hide other players' spell effects (recurring, 2011→present; no D3 patch note found implementing it)
- Crate forums *Mod — Combat Overhaul* (community-added enemy stagger on hit)
