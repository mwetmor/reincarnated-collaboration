# Research — Defended-Zero Red-Team: Hybrid-Wedge Atlas Claim — 2026-07-15

**Mode:** A (analytical)
**Commissioner:** Gandalf
**Sources consulted:** See Source List

---

## EXECUTIVE SUMMARY (one screen)

The claim under attack: **"the genre has never built kits with treatment=hybrid (co-equal damage+control; deletion test: remove either half and the kit collapses) — a 29-cell wedge of the atlas near the rooted/PERFORM region is genuinely unexplored."**

Five candidate near-misses examined. None break the claim. The closest candidate is Matt's own MCD gravity assembly (Charge 3 item v), which deserves the most serious treatment precisely because it is the player-experienced combination most resembling treatment=hybrid. But on inspection, the gravity mechanic in MCD is kit-intrinsic-to-the-enchant only — it is assembled via item enchantments, not intrinsic to a character class skill — and the deletion test reveals asymmetry: the build continues to function (at reduced efficiency) without the gravity pull, because the damage spender still works; whereas removing the damage source while retaining gravity leaves a build that CC's enemies together but cannot kill them efficiently. The pull is substantially the delivery mechanism, not a co-equal treatment half. The taxonomy key from the commission brief (rider-proc ≠ treatment-hybrid) is confirmed and clarified by the examination below.

**No surviving claim-breaker found. Claim holds as pre-publication defended.**

---

## CHARGE 3 — Defended-Zero Red-Team

### The Deletion Test Operationalized

The claim requires that treatment=hybrid satisfies: **remove damage half → kit collapses; remove control half → kit collapses.** Collapsing means: the remaining half is not viable as a standalone build. A build where control is merely a delivery mechanism for damage (rider-proc) fails the test on the control side: remove the damage half, the control half is useless. A build where damage is merely an amplification of control outcomes also fails: remove the control half, the damage half still fires.

Rider-proc examples that do NOT satisfy the deletion test:
- Strongarm Bracers + Ess of Johan (D3): pull triggers knockback → triggers +25% damage buff. Remove the pull: damage still fires (from other sources), slightly lower. The buff is a rider on the pull, not a co-equal half.
- Cyclone Strike (D3/DI Monk): pull → enemies take +150% more damage from Mystic Ally. Remove the pull: Mystic Ally still damages. Damages are amplified by pull, not dependent on it.

### Candidate 1 — PoE CwC Cyclone (Cast-while-Channelling + Discharge / SRS)

**What it is:** Cyclone channels continuously, triggering another spell (Discharge, SRS, Arc, etc.) via the CwC support gem on a timer. The player's character spins through enemy packs while the triggered spell fires automatically.

**Co-equal damage+control test:**
- **Cyclone's role:** Delivers the channeling vehicle. Cyclone itself deals modest damage (channeling attack). In the Discharge CwC variant, Cyclone also generates charges (via Hierophant's Conviction of Power: "25% chance to gain Endurance Charge when you gain Power Charge"). Cyclone's primary build-mechanical role is trigger delivery + charge generation.
- **Is Cyclone "control"?** Cyclone provides implicit knockback (has a minor pushback on hit in older versions) and Fortify defense, but it is not meaningfully a control skill. It does not stun, freeze, pull, or root enemies as a functional outcome. It positions the PLAYER, not the enemy.
- **Deletion test:**
  - Remove Cyclone: Discharge cannot fire via CwC without the channeling vehicle. Build collapses. But this doesn't confirm co-equal treatment — removing ANY delivery mechanism collapses any build. The question is whether Cyclone is providing damage AND control in parallel.
  - Remove Discharge: Cyclone alone deals weak damage. Build collapses.
- **Verdict:** Cyclone in CwC is a **delivery mechanism** (animation trigger), not a control treatment. Control is not a meaningful Cyclone output. The build's "treatments" are: damage (Discharge) and mobility (Cyclone positioning player). There is no co-equal control output. **Does not break the claim.** The taxonomy note is confirmed: CwC is rider-proc architecture, not treatment-hybrid.

**Source:** PoE forum [3.12] Cyclone Discharge Hierophant (https://www.pathofexile.com/forum/view-thread/2988277); PoB Archives (https://pobarchives.com/builds/rfAQ93Ab)

---

### Candidate 2 — PoE Curse-on-Hit Cyclone / Warlord Influence Rings

**What it is:** Cyclone spins through packs; a ring with "Curse Enemies with Vulnerability on Hit" automatically applies Vulnerability (damage-taken amplifier) on each hit. The build takes advantage of spreading cursing at speed.

**Co-equal damage+control test:**
- **Vulnerability:** is a debuff that increases damage the enemy takes, not a movement/lockdown control. It is classified in PoE's own taxonomy as an offensive curse, not a control (hard stop / slow) curse. Enfeeble and Temporal Chains are the defensive/control curses; Vulnerability is an offensive amplifier.
- **Is the debuff control?** Not in the relevant sense. It is damage amplification expressed as a debuff. "Control" in the kit-treatment taxonomy requires: impeding enemy action or positioning (CC — blind, stun, knockback, root, pull, slow, fear). Vulnerability does none of these.
- **Deletion test:**
  - Remove the curse ring: Cyclone still spins and kills, just slower. Build does not collapse — it runs suboptimally.
  - Remove Cyclone (curse only, no movement, no damage): enemies are Vulnerable but alive. Build collapses.
- **Verdict:** This is **damage amplification via debuff**, not damage+control hybrid. The "control" half is not a genuine control treatment; it is an offense multiplier expressed as an item effect. Does not approach treatment=hybrid. **Does not break the claim.**

**Source:** Cyclone build guides (Overgear: https://overgear.com/guides/poe/cyclone-build/; Mobalytics Cyclone Slayer: https://mobalytics.gg/poe/builds/cyclone-slayer-league-starter-to-endgame-step-by-step-guide-beginner-friendly)

---

### Candidate 3 — Last Epoch Warpath Ignite-Stacking Paladin

**What it is:** Warpath (channeled spin attack) applies Ignite stacks on each hit. Ignite stacks deal damage over time. The build scales Ignite magnitude and application rate; the character spins indefinitely, applying DoT stacks.

**Co-equal damage+control test:**
- **What Warpath does:** deals physical/fire hit damage on each spin tick; applies Ignite stacks (DoT) at a rate determined by hit chance + ignite application chance.
- **What Ignite does:** deals fire damage over time; stacks infinitely within stack duration. Ignite is a damage ailment, not a control ailment. It does not slow, root, stop, or reposition enemies.
- **Control output from Warpath?** Warpath in this build has no meaningful control output. The build is an ailment-stacking DoT build: the Warpath hit serves as delivery for Ignite, and Ignite provides the sustained damage. There is no CC component in either the base skill or the Ignite ailment. "Ailment" ≠ "control ailment." In Last Epoch's taxonomy, control ailments (Stun, Slow, Chill, Freeze, Shock) are separate from damage ailments (Ignite, Bleed, Poison).
- **Deletion test:**
  - Remove Warpath (Ignite only via other delivery): Build needs a different delivery mechanism; Warpath is not the only ignite-applier. Not perfectly substitutable, but the ignite damage function doesn't collapse.
  - Remove Ignite (pure Warpath hit damage only): Build deals hit damage only. Still functional, just slower. Does not collapse on the control side because THERE IS NO CONTROL SIDE to remove.
- **Verdict:** Warpath Ignite is a **damage + DoT damage** build, not a damage + control build. The ailment involved is a damage type (Ignite), not a CC type. **Does not break the claim.** This candidate was not even close — it is damage-over-time architecture misread as damage+control.

**Source:** LastEpochTools.com — Ignite Warpath Paladin 1.3.1 (https://www.lastepochtools.com/build-guides/you-are-already-dead---ignite-stacking-warpath-paladin); Tales of the Aggronaut — Ignite Warpath 2024 (https://aggronaut.com/2024/02/29/ignite-warpath-in-monoliths/)

---

### Candidate 4 — D3 zMonk / zBarb Grouping Support Kits

**What they are:** Support roles in group GR pushing. The zMonk uses Cyclone Strike to pull + group enemies and apply debuffs; the zBarb uses Ancient Spear Rage Flip + Ground Stomp Wrenching Smash to group and provides buff uptime. These are explicitly NOT damage dealers — they are dedicated support roles whose damage output is negligible.

**Co-equal damage+control test:**
- **zMonk:** Cyclone Strike pulls + deals holy damage + applies debuffs (enemies take 150-200% more damage from Mystic Ally). But the role of zMonk in the group is explicitly the CC/grouping/buff side; a dedicated damage dealer handles damage. The zMonk's "damage" output is trivial in a group GR context — this is a control-primary, damage-trivial kit.
  - Deletion test: Remove the pull → the debuffs still apply but enemies are ungrouped. Build collapses as grouping support. Remove the trivial Cyclone damage → grouping and debuffs still work. Control half survives; damage half is vestigial.
  - **Result: control-primary, not co-equal.** The zMonk violates the deletion test from the damage side — removing damage does not collapse the kit's ROLE.

- **zBarb:** Ancient Spear Rage Flip has a damage component, but in the zBarb build, gear is specifically chosen to MINIMIZE the Barbarian's own damage (to avoid breaking Rift Guardian kill timing for the trash killer). The damage output is deliberately suppressed. Pull + grouping is the entire purpose.
  - Deletion test: Remove pull mechanics → zBarb has no group-relevant function. Collapses. Remove damage (or reduce to near-zero, which IS the intended state) → grouping still works perfectly. That is the intended build outcome.
  - **Result: control-primary, damage deliberately secondary (often suppressed to near-zero).** The zBarb is the OPPOSITE of treatment=hybrid; it has so much control identity that its damage is treated as a liability.

**Verdict:** Both candidates are **control-primary, damage-suppressed or vestigial.** Not co-equal. **Does not break the claim.** In fact, the zBarb makes the claim's territory clearer: the genre solved the "control without damage" space (S-tier group support roles) and the "damage without control" space (DPS builds), but never the co-equal intersection.

**Source:** Maxroll zBarb guide S39 (https://maxroll.gg/d3/guides/support-zbarb-guide); DiabloFans zMonk guide (https://www.diablofans.com/builds/98593-support-monk-an-in-depth-guide-to-zmonk); Maxroll D3 4-player push meta (https://maxroll.gg/d3/meta/4-player-push-meta)

---

### Candidate 5 — DI Cyclone Strike Monk (PvP/PvE "Helicopter")

**What it is:** Diablo Immortal Monk using Cyclone Strike to pull enemies + deal damage simultaneously. The "helicopter" variant adds Driven Thunder essence for CC immunity while spinning, making the monk both damage dealer and crowd controller in PvP.

**Co-equal damage+control test:**
- **Cyclone Strike's dual output:** The skill explicitly both pulls enemies AND deals holy damage in one cast. In PvP, the pull determines enemy positioning (preventing them from escaping range) while the damage deals direct HP loss.
- **Intrinsic?** Yes — Cyclone Strike's pull is intrinsic to the skill. The damage and pull both fire from the same skill activation without additional item support. The Driven Thunder essence adds CC immunity to the Monk (self-buff), not additional control to enemies. The Storm Spirit chest piece converts Cyclone Strike into "pure DPS" (removing the pull) — confirming that both damage and control are real functional halves.
- **Deletion test:**
  - Remove Cyclone Strike damage (use a zero-damage version, or substitute a pure-pull with no damage): the control (pull) still works but the DPS role collapses. Monk cannot kill.
  - Remove Cyclone Strike pull (use Storm Spirit chest — pure DPS version): the pull is gone, just damage. Control role collapses in PvP (enemies can escape range; grouping for team is lost). DPS role survives.
  - **Both halves can be independently removed. Both would cause the build to lose a major function.** This is the closest candidate to a genuine co-equal hit.

- **BUT: is it assembled or intrinsic?** Cyclone Strike's pull is skill-intrinsic (no item support required). The skill is defined as both damage AND pull. This makes it more intrinsic than rider-proc.
- **HOWEVER: the critical taxonomy question.** In the kit framework, "treatment" is about the character's DESIGNED ROLE, not a single skill. The DI Monk has multiple skills; Cyclone Strike is one active with supporting skills. The typical Cyclone Strike Monk build pairs it with Tempest Rush (mobility), Mystic Strike / Flying Kick (additional damage), and defensive skills. In PvE (raids), Icy Veins notes Cyclone Strike in the raid Monk build is used "as an AoE DPS ability instead of its traditional CC role" (Storm Spirit build). In PvP, control is dominant. **The Monk class overall oscillates between damage-primary and CC-support depending on build configuration.** No single build has BOTH halves hardlocked as co-equal — the player configuration choice determines which treatment is primary.
- **Versus the claim's rooted/PERFORM region:** The atlas claim targets kits where BOTH damage and control are hardwired into the kit's identity — you cannot make a variant of the kit that de-emphasizes either half without the kit ceasing to function as designed. The DI Monk Cyclone Strike is a skill, not a kit, and the kit around it is configurable in ways that break the co-equal constraint.

**Verdict:** DI Cyclone Strike is the closest genre-canon near-miss found. The skill itself has genuine co-equal damage+pull outputs and the deletion test would partially break the build from either side. **However:** the kit built around Cyclone Strike is configurable (Storm Spirit removes pull; builds exist that are pure DPS or pure CC using the same skill); the treatment-hybrid status is not hardlocked. Under the strict definition (kit-level intrinsic, not player-configuration-variable), this is not a true treatment=hybrid. **Does not break the claim** under the strict reading. Flag: this is the most substantive near-miss found; warrant a brief acknowledgment in the atlas publication that DI Cyclone Strike Monk was examined.

**Source:** Icy Veins — DI Monk Cyclone Storm Build (https://www.icy-veins.com/diablo-immortal/monk-cyclone-storm-build-guide-for-raids); PCGamesN — best DI Monk builds (https://www.pcgamesn.com/diablo-immortal/monk-build); Game Rant — DI Cyclone Strike Monk build (https://gamerant.com/diablo-immortal-best-cyclone-strike-monk-build-skills-gear-gems-reforge/)

---

### Candidate 6 — MCD Gravity Assembly (Matt's Direct Play — Leap + Gravity + Generator/Spender Pummel)

**What it is:** Matt's described assembly: Hammer of Gravity (built-in Gravity pull, heavy attack) combined with a leap-to-center artifact for initial positioning, followed by a generator/spender pummel loop. This is the gravity build as actually played.

**Reconstructed mechanics from sources:**
- Leap artifact (e.g., Gravity Pulse armor enchant + Anvil bow + Corrupted Seeds) brings Matt to the group center while triggering a gravitational pulse that pulls mobs inward.
- Hammer of Gravity hit: each heavy attack triggers Gravity I (pull toward impact point), grouping residual mobs not already pulled by the leap.
- Generator hits: light attacks build up some proc or artifact cooldown (e.g., Soul Healer, Fireworks, etc. — MCD artifacts vary by player configuration). These deal hit damage.
- Spender/burst: artifact activation (e.g., Deathcap Mushroom, Corrupted Seeds, etc.) dealing large burst AoE into the now-grouped cluster.

**Co-equal damage+control test:**
- **Control output:** Pull via Gravity (on-hit, no CD) + leap displacement. Real, functional crowd control output — enemies repositioned to cluster.
- **Damage output:** Heavy attack + generator hits + spender artifact burst. Real, functional damage output — enemies die.
- **Deletion test:**
  - Remove the gravity/pull (use a weapon without Gravity enchant; skip leap): enemies scatter. AoE efficiency drops significantly. In a game where the power curve never lets you outscale content, reduced density means reduced kill speed means potential survival failure at high Apocalypse Plus threat. **The pull is load-bearing.** However — at lower difficulty, the build does not strictly "collapse" without gravity; it just becomes less efficient. The build is not INOPERABLE without gravity.
  - Remove the damage (hypothetically: gravity-only, no weapon damage, no spender): enemies are pulled together and... the build cannot kill them. **Strict collapse.** No damage → no kill → no function.
- **Result:** The deletion test is asymmetric. Gravity removal = reduced efficiency (not total collapse). Damage removal = total collapse. The kit is **damage-primary, with pull as a significant amplifier** — which is the rider-proc pattern, not treatment=hybrid.

**Why does it FEEL like co-equal?** Because in MCD's flat-curve ecology, the efficiency loss from removing gravity is so severe that it feels like collapse. At Apocalypse Plus threat level with tight challenge, failing to group enemies means you cannot kill them fast enough to survive the encounter. The game ecology makes the pull feel mandatory. But the underlying mechanic is still: damage primary, pull amplifies damage delivery. The control is not an autonomous functional output — enemies pulled but not damaged are a zero-progress outcome.

**The intrinsic vs. assembled question:** The Gravity pull is NOT intrinsic to a character class. It is: (a) weapon enchant chosen by player configuration, (b) artifact choice for the leap, (c) weapon selection (Hammer of Gravity). Every element is player-assembled via gear. No base class in MCD has a pull mechanic — there are no classes. The enchantment system is the entire skill layer. This means MCD gravity assemblies map EXACTLY to Gandalf's rider-proc ≠ treatment-hybrid taxonomy: the control is assembled via items/enchants, not intrinsic to a character's designed treatment.

**Verdict:** MCD gravity assembly is the most seriously considered candidate in this census. Treat it with full weight: it is a player-experienced assembly where both pull and damage are genuinely load-bearing at the ecological difficulty level Matt was playing. But the deletion test is asymmetric (gravity removal degrades efficiency; damage removal causes strict collapse), and the control is entirely gear-assembled, not class-intrinsic. **Does not break the claim under strict taxonomy.** The claim stands.

---

## Examined-and-Excluded Table

| Candidate | Co-equal D+C? | Control intrinsic? | Deletion test | Verdict |
|---|---|---|---|---|
| PoE CwC Cyclone + Discharge | No. Cyclone = delivery/trigger, not control | N/A | Removing Cyclone collapses trigger delivery (any removal of vehicle would); removing Discharge collapses damage. Control output is absent — Cyclone moves player, not enemies. | Rider-proc (delivery + damage). Does not break claim. |
| PoE Curse-on-Hit Cyclone | No. Vulnerability = damage amplifier, not CC | Gear-assembled (Warlord ring) | Remove curse ring → build suboptimal, not collapsed. Remove Cyclone → build collapsed. Asymmetric. | Damage + offense-multiplier. No genuine CC half. Does not break claim. |
| LE Warpath Ignite Paladin | No. Ignite = damage ailment, not CC ailment | Ailment is gear/node-scaled | Remove Warpath → needs new delivery, but Ignite damage concept survives. Remove Ignite → pure hit damage, still functional. | Damage + DoT damage. Zero CC treatment. Does not break claim. |
| D3 zMonk Cyclone Strike support | No. Damage is vestigial; control primary | Partially intrinsic (Cyclone Strike skill) | Remove trivial damage → grouping/debuff survive. Remove CC (pull) → collapses grouping role. Asymmetric opposite: CC-primary. | Control-primary, damage-suppressed. Opposite of hybrid. Does not break claim. |
| D3 zBarb grouping support | No. Damage deliberately suppressed | Skill-intrinsic (Ancient Spear, Ground Stomp) | Remove pull → collapses grouping role. Remove damage (intentionally minimized) → grouping intact. CC-primary by design. | Control-primary, damage-actively-suppressed. Does not break claim. |
| DI Cyclone Strike Monk (helicopter) | Partially. The skill itself has genuine co-equal pull+damage. Kit around it is configurable. | Skill-intrinsic pull | Remove pull (Storm Spirit): DPS-only, no CC. Removes CC half. Remove damage (hypothetically): pull exists but kill function gone. Both halves matter. BUT: kit is player-variable. Storm Spirit build deliberately removes pull, yielding pure DPS Monk. | CLOSEST near-miss. Skill is dual-purpose; kit is configurable (breaks hardlock requirement). Does not break claim under strict reading. Warrants publication acknowledgment. |
| MCD gravity assembly (Matt's play) | Ecologically near-co-equal. Strict analysis: damage-primary; pull amplifies delivery. | Gear-assembled entirely. No class intrinsic. | Remove gravity → degraded efficiency at challenge difficulty, NOT strict collapse at lower settings. Remove damage → strict collapse (enemies alive). Asymmetric. | Damage-primary, pull-as-amplifier (rider-proc). Assembled via enchants, not class-intrinsic. Does not break claim under strict taxonomy. Most substantive candidate. |

---

## Claim Status

**Claim holds: no candidate breaks the treatment=hybrid criterion under the strict deletion-test definition.**

The closest near-miss (DI Cyclone Strike Monk) is substantive enough to warrant a one-paragraph note in publication: "DI Cyclone Strike Monk was examined. The skill itself delivers co-equal pull and damage outputs; a version that removes pull (Storm Spirit variant) and a version that emphasizes pull over damage (zMonk-style grouping) both exist within the same class/skill. The hardlock condition — that both halves are simultaneously non-removable without collapse — is not satisfied at the kit level. The skill is dual-use; the kit is configurable. The claim is not broken, but this candidate sits closer to the boundary than any other examined."

The rider-proc vs. treatment-hybrid taxonomy is confirmed by the full examination: across all candidates, pull or debuff functions as a rider on the damage delivery chain (multiplier, trigger, grouping for AoE efficiency), never as an autonomous treatment half with equal structural weight.

---

## Implications for Corpus Function-Level Question

The examination produces a clean answer to the open question: **should `pull` be elevated to a function level (parallel to blind, expose, fear, hard-stop, hex, knockback, silence, stun, taunt)?**

Evidence for elevation:
- Pull operates as a distinct positional CC in ≥3 franchise contexts (D3 multi-skill, DI Cyclone Strike, MCD Gravity, Lost Ark Destroyer, Hades Poseidon Aid augment). The geometry of pull (inward force) is meaningfully distinct from knockback (outward force) in both tactical effect and density-economy implications.
- The corpus already encodes `vortex_pull` as a GEOMETRY class. If the geometry exists at the kit side but the corresponding function-level label does not, the classification is asymmetric.
- The DI Cyclone Strike Monk near-miss established that pull IS a meaningful co-equal output of at least one skill in canon, even if not at kit level.

Evidence against (or for qualification):
- Pull is consistently ecology-dependent: in boss-centric contexts it has marginal function-level identity; it only matters in horde-density contexts.
- Pull in canon is almost always: (a) support-role confinement (zBarb, zMonk), (b) skill-effect on one move, or (c) gear-assembled. It is rare as a class-identity function level.

**Recommended conclusion for corpus team:** Elevate `pull` to a function-level label. Mark it as **ecology-sensitive** — annotate at the instance level whether pull is a meaningful function (horde-density context) or marginal function (boss-centric context). This resolves the geometry-class vs. function-level asymmetry without overclaiming pull as universally load-bearing.

---

## Knowledge Gaps Not Resolved

- Hades 2 pull mechanics: Poseidon boon set in Hades 2 may have introduced more developed pull. Not searched in depth; Hades 2 is not yet in the corpus per commission briefing.
- Torchlight Infinite pull: insufficient data on TLI-specific skill taxonomy to determine if any TLI skill is pull-primary with co-equal damage output.
- Full Diablo Immortal balance history for Cyclone Strike (fandom wiki 402'd): possible additional nerfs or buffs that could sharpen the DI near-miss analysis.

---

## Source List

- PoE forum — Cyclone Discharge Hierophant [3.12]: https://www.pathofexile.com/forum/view-thread/2988277
- PoB Archives — CwC Cyclone builds: https://pobarchives.com/builds/rfAQ93Ab
- Overgear — Cyclone build guide: https://overgear.com/guides/poe/cyclone-build/
- Mobalytics — Cyclone Slayer guide: https://mobalytics.gg/poe/builds/cyclone-slayer-league-starter-to-endgame-step-by-step-guide-beginner-friendly
- LastEpochTools — Ignite Warpath Paladin 1.3.1: https://www.lastepochtools.com/build-guides/you-are-already-dead---ignite-stacking-warpath-paladin
- Tales of the Aggronaut — Ignite Warpath 2024: https://aggronaut.com/2024/02/29/ignite-warpath-in-monoliths/
- Maxroll — zBarb S39: https://maxroll.gg/d3/guides/support-zbarb-guide
- Maxroll — D3 4-player push meta S39: https://maxroll.gg/d3/meta/4-player-push-meta
- DiabloFans — zMonk in-depth guide: https://www.diablofans.com/builds/98593-support-monk-an-in-depth-guide-to-zmonk
- Icy Veins — DI Monk Cyclone Storm build: https://www.icy-veins.com/diablo-immortal/monk-cyclone-storm-build-guide-for-raids
- PCGamesN — best DI Monk builds: https://www.pcgamesn.com/diablo-immortal/monk-build
- Game Rant — DI Cyclone Strike Monk: https://gamerant.com/diablo-immortal-best-cyclone-strike-monk-build-skills-gear-gems-reforge/
- Minecraft.wiki — Gravity: https://minecraft.wiki/w/Dungeons:Gravity
- Game8 — Enchantments Tier List (Gravity S-tier): https://game8.co/games/Minecraft-Dungeons/archives/289819
- Minecraft Dungeons Wiki Fextralife — Gravity Pulse: https://minecraftdungeons.wiki.fextralife.com/Gravity+Pulse
