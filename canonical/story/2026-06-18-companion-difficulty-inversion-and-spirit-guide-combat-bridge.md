# Companion Difficulty-Inversion + the Spirit-Guide Combat-Bridge

**STATUS:** DESIGN RECOGNITION (Matt-originated; gandalf-refined) — a SEASON-2 planning item, NOT a season-1 blocker
**Date:** 2026-06-18
**Author:** gandalf (story-and-design steward), capturing + refining a Matt design insight
**Origin:** Matt, mid-session, immediately after confirming companions = season-2 (the "npc" strike). Verbatim: *"The only thing I am worried about though is that season 2 may be too easy with a companion compared with season 1 when you don't have a companion. We will just have to add a note to scale enemy health in season 2 with the addition of the companion, and maybe offer some type of generic companion for boss fights for solo players.. like maybe the spirit guide itself adds damage on tough encounters until you ascend your first form and gain a companion."*
**Couples to:** `canonical/story/2026-06-18-current-to-end-state-battlesim-and-pipeline.md` (Part V Q6 — the season-2 difficulty-curve open question); `canonical/historical/17-gear-and-spirit-guide-design.md` (the spirit-guide layer); `canonical/story/2026-06-13-companion-as-hall-of-heroes-ally-commitment.md` (the companion = D2/D3 mercenary ruling); engine `simulation/balance_loop.py:128–271` (companion modifier-vector + caps + WR-delta guard — the existing machinery this would reuse).

---

## 0. The recognition in one line

**Adding a companion in season-2 without reconciling the enemy baseline creates a difficulty INVERSION** — season-2-with-ally would be *easier* than the solo season-1 descent, cheapening both the progression curve and the companion reward. Matt named the problem and the two-part fix; this note refines the fix and routes it to the right owners. **It is a season-2 design item, deferred behind season-1; recording it now so it is not lost and not re-invented.**

---

## 1. Why the concern is real (and genre-faithful)

The difficulty-inversion Matt fears is a **known ARPG failure mode**, not a hypothetical:

- **Diablo II mercenaries.** D2 never scaled monster difficulty to merc presence. The Act-2 aura merc (Might/Holy-Freeze, later Insight/Infinity) became so load-bearing that the merc did the "hard part" for most builds — the game's real difficulty quietly assumed you had one. Result: the ally became a *mandatory crutch*, and solo-merc-less play became the "wrong way to play." That is the same root cause as Matt's fear (ally power un-reconciled with enemy baseline), surfacing from the opposite side.
- **The always-on-ally trivialization fork.** Any persistent ally forces the designer to choose: balance enemies *assuming the ally* (→ solo play becomes brutal) or *assuming no ally* (→ the ally trivializes content). Matt is correctly choosing to close the second branch by scaling the season-2 baseline.

And it maps **cleanly onto our genre's own logic.** Isekai power-fantasy is never "you get stronger and the world stands still" — it is "your power grows AND the threat grows in lockstep." Solo Leveling: Jin-Woo's shadow army arrives AND red gates / monarchs escalate. Mushoku Tensei: Rudeus's party makes harder content *accessible* while the world's threats scale (Teleport Incident, demon continent). **The companion's arrival should COINCIDE with a threat escalation, not open a difficulty trough.** Matt's instinct to scale season-2 enemies is genre-faithful, not merely mechanical bookkeeping.

---

## 2. Mitigation (a) — "scale enemy health in season 2" — REFINE, don't take literally

The instinct is right; the *blunt* version ("scale HP") walks into a second well-known anti-pattern:

- **HP-only scaling = the spongey-enemy trap.** Diablo III's pre-loot-2.0 Inferno and several PoE league mechanics earned the same criticism: scaling only the HP pool makes fights *longer*, not more *interesting*. If you scale ONLY HP to absorb the companion's added DPS, every fight takes the same wall-clock time it did solo — now with two actors chipping it down. The player's takeaway is "nothing changed except I have a friend," which undercuts BOTH the difficulty progression AND the companion's felt impact.
- **Better: scale the THREAT, with HP as the coarse balancer underneath.** A second actor lets encounter design assume two targets — which unlocks mechanics that are *fair to a duo but were impossible to ask of a solo player*: split-target pressure, adds that must be handled WHILE the boss is DPS'd, telegraphed AOEs one actor body-blocks while the other repositions. The spatial sim already models multi-actor positioning and proxy-population, so this is expressible in the apparatus, not just on paper.
- **This is a SIM problem before it is a content problem.** The gauntlet today has 4 cohorts, all solo. A companion-present season-2 needs its **own cohort with re-fit KPM bands** (two-actor throughput shifts the whole distribution). That is gamora's work. Matt's mitigation (a) is therefore not "add a number" — it is "the balance apparatus needs a companion-present measurement mode."

**Player consequence:** done as threat-scaling, the season-2 player *feels* the companion mattering (new encounter shapes they couldn't survive solo) AND feels the difficulty rise. Done as HP-only, they feel neither.

---

## 3. Mitigation (b) — the spirit-guide combat-bridge — ENDORSE STRONGLY, and sharpen

This is the more interesting half, and it is genuinely good design. Matt: *"maybe the spirit guide itself adds damage on tough encounters until you ascend your first form and gain a companion."*

### 3.1 What it solves

Scaling season-2 enemies for companion-present creates a *mirror* spike: the **early-season-2 player who hasn't yet earned their companion** (the window before first-form ascension) faces companion-scaled enemies *solo*. The spirit-guide combat-bridge fills exactly that window — the "training-wheels ally" that carries the player from "season-2 enemies are now companion-scaled" to "you have actually earned your companion."

### 3.2 Why it is THEMATICALLY load-bearing (not a bolt-on)

This is the part that makes it more than a balancing hack. **The spirit-guide IS the future-self / guide layer (doc 17).** A future-self stepping in to add power *"until you can stand on your own"* is the literal arc of the guide archetype — the mentor who fights beside you until you are ready, then steps back so you become who you must become. Gandalf at Helm's Deep; the guest party-member who departs once you're strong (the FF-genre pattern); the tutorial-buddy who carries the first dungeon then hands off. **The combat contribution EXPIRING on first-form ascension is the guide-archetype's whole arc compressed into a difficulty curve.** When the system-behavior and the story-behavior are the *same gesture*, the mechanic means something. This one does.

### 3.3 Three sharpenings (the discipline that keeps it from becoming the D2-merc trap)

1. **Visibly temporary, with a baton-pass — never a silent nerf.** Matt already built the off-ramp ("until you ascend your first form and gain a companion"). The discipline: the guide must *visibly hand the baton to the companion* at first-form ascension — the guide steps back AS the earned ally steps forward, same support-slot, narrative continuity. "My guide carried me; now my ally carries forward" is a *triumphant* beat. If the contribution just silently switches off, the player feels nerfed instead of graduated.
2. **Encounter-tier-gated — boss/elite only.** "Tough encounters" already has a definition in the apparatus: the boss/elite tier (`boss_with_adds`, `mini_boss`, `elite_pack`) vs the swarm/open-arena trash tier. Gate the guide's contribution to the boss/elite tier so it does *nothing* in trash clears. This preserves the solo power-fantasy of mowing down packs (you still feel like the hero in the moment-to-moment) and intervenes *only* at the single-hard-target walls where a solo DPS deficit actually hurts.
3. **Reuse the companion modifier-vector machinery — don't build a new system.** The engine already has the companion modifier-vector + caps + WR-delta guard (`balance_loop.py:128–271`). The spirit-guide combat-bridge is mechanically a *capped, encounter-tier-gated partial-companion* — a tighter-capped modifier-vector with a tier gate. gamora parameterizes the existing companion system rather than authoring a new one. Real implementation economy worth naming up front.

---

## 4. The one decision for Matt (sizes whether season-1 stays combat-pure)

Season 1 is *also* solo-and-companion-less. So: **does the spirit-guide combat-bridge exist in season 1 too, or is it season-2-only?**

- **(i) Season-2-only [gandalf lean].** Season 1 is the *pure solo crucible* — no spirit-guide combat aid; the difficulty IS the point (you prove yourself before the guide will fight for you). The guide's combat-aid is itself a season-2+ unlock — part of progression. This keeps season-1 as the clean solo baseline that makes the companion's season-2 arrival *feel* like escalation, and it gives the guide a *narrative reason to start fighting* in season-2 (the threats finally crossed the threshold where the guide intervenes). The resulting support-curve is clean and rising — **S1 solo-pure → S2-early guide-assisted → S2 companion-earned** — matched against a rising threat-curve.
- **(ii) Universal solo-boss-bridge.** The guide combat-aid is available season-1 too, as a standing "solo boss bridge"; the season-2 companion simply replaces and exceeds it. Simpler narratively but flattens the S1→S2 gradient and dilutes season-1's solo identity.

**Recommendation: (i).** It preserves season-1's solo identity (which we just locked with the six-type bundle), makes the companion arrival an escalation rather than a relief, and gives the spirit-guide an *earned* combat debut. Awaiting Matt's call when season-2 planning opens.

---

## 5. Routing + scope discipline

- **NOT a season-1 blocker.** Season-1 stays the six-type solo bundle (kits/monsters/factions/gear/weapons/flavortext). This note disturbs nothing in the season-1 plan.
- **Season-2 planning items it generates:**
  - gamora: a **companion-present gauntlet cohort** with re-fit KPM bands (two-actor throughput) — mitigation (a).
  - gamora: a **spirit-guide combat-bridge** as a capped, encounter-tier-gated reuse of the companion modifier-vector — mitigation (b).
  - gandalf: the **threat-scaling encounter-design spec** (what two-actor mechanics season-2 enemies gain), the **baton-pass beat** (guide→companion hand-off at first-form ascension), and the **season-1-pure-vs-universal decision** packaged for Matt.
- **Genre guardrail to carry forward:** the failure to avoid is the D2-merc "mandatory crutch" — both the companion AND the guide-bridge must be balanced-around without becoming the thing that does the hard part FOR the player. The player is always the protagonist; the ally is an extension of their offense, not a substitute for it. (This is the same principle as the Proxy-Commander Set #6 discipline: *"the army is an EXTENSION of your offense, not a clone-multiplier."*)

---

**Signed:** gandalf, 2026-06-18. Matt saw the inversion before it was built — that is the cheapest time to catch it. The fix is genre-faithful: scale the *threat* (not just HP) for the companion, and let the spirit-guide fight beside the player through the pre-ascension window, then pass the baton. The guide-archetype's arc and the difficulty curve are the same gesture — which is exactly why it will feel right. Deferred to season-2 planning; recorded so it survives.
