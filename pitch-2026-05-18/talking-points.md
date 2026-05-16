# Talking Points — 2026-05-18 Meeting

**For Matt's eyes only.** Anchor doc for the conversation. Keep open on phone or print.

**Audience:** Director of Apex Games (friend, informal). **Goal:** marketability sanity check. **Not** a job/funding pitch.

---

## Opening (30 seconds)

Pick one framing depending on his energy at the start:

**Casual opener:** "I've been building this on the side for a while — a procedural content engine for ARPGs, plus an isekai-themed game on top of it. Took me a year-ish to get to where it's actually generating balanced content. Wanted your read on whether this has industry legs."

**Direct opener:** "Quick frame: this splits into two products. There's an engine — procedural content generation with simulation-balancing — and there's a game that runs on top of it. I want your read on whether either one has marketability, and which I should lead with."

Use direct opener if he's clearly in work-mode. Casual opener if it's coffee-shop tone.

---

## Walkthrough flow (open `https://reincarnated-loadout.vercel.app`)

Roughly 5-7 minutes if uninterrupted. Pause for questions liberally — *his* questions are the point of the meeting.

### Stop 1 — `/loadout` (the player view)

"This is what a player sees. The Yomi season — Japanese underworld theme — has 10 classes, all generated this week from one seed. Here's Lantern-Keeper of Yomi's Winds — hybrid mage, fire-element with the seasonal 'lantern' flavor."

**Point to:**
- Class flavor (tap the (i) icon — the lore reads coherent because it was generated as one piece, not stitched)
- Skill tree (tier × chain layout, two-step interaction)
- Stats panel
- Element badges

**What to say:** "This whole class — name, kit, lore, balance modifier — was generated and validated automatically. No human curation."

### Stop 2 — `/sample` (engine baseline view — the unvarnished version)

"This is what the engine actually produced. Sample mode shows every skill at rank 1, gear synthesized from class affinity, no player choices applied. It's the engine's raw output, not a curated demo."

**Why this matters in the pitch:** transparency. Many procgen demos hide their seams; this one shows them.

### Stop 3 — `/analytics` (what the engine learned about itself)

"These are findings the engine surfaced that I didn't ask for. Hunter archetype has the widest balance range — 1.82× modifier spread, meaning the kit-shape isn't consistent. Fire is over-represented at 23.6% vs the 20% you'd expect for 5 elements. Mana energy dominates at 85%."

**Lean on:** the engine finds problems it wasn't told to look for. That's the simulation layer doing real work.

### Stop 4 — `/encounters` (the AOE mechanic visualized)

"Here's the AOE-vs-single-target differential against swarm packs. AOE skill hits 8 pack members → 8× damage. Single-target hits 1 → 1× damage. This is genre-correct ARPG combat emerging from the math, not from hand-tuning."

**Cite:** Diablo / PoE players intuitively understand "AOE matters in packs." The engine produces this without being told.

### Stop 5 — Demo1 (if asked)

"There's also a playable Pixi.js demo from last week — happy to show that if you're interested. It demonstrates the seasonal arc end-to-end."

Only pivot to demo1 if he asks. Don't volunteer — it's older work.

---

## Trajectory — 60 seconds

Cover three phases:

- **Phase 0 (where I am):** validate the generation works. Mostly done.
- **Phase 1 (next 6-12 months, solo or with team):** demo2 with rooms + AOE-tuned gauntlet, non-humanoid character generation, Earth Self meta-layer prototype.
- **Phase 2-3 (longer):** for the engine, multi-tenant SaaS + first licensing conversation. For the game, closed beta with full Earth Self mechanics, then production launch.

Earth Self is worth explicitly naming: "The game's twist is that the persistent player identity isn't the character — it's the collection of classes you've embodied. Weekly reincarnations are mortal; the collection is permanent. That's the isekai genre executed mechanically."

---

## Honest weaknesses to acknowledge upfront

Volunteer these before he raises them. Saves him the awkwardness, signals seriousness.

- **"It's a Phase 0 prototype, not production-ready."**
- **"I haven't validated player-side appeal. The engine validates generation; nobody's played it for retention metrics."**
- **"It's been a solo project. Scaling beyond solo is the obvious blocker."**
- **"Mobile ARPG market is crowded. I'd be entering against polished competition."**
- **"The math-before-code discipline catches engineering issues — but there's no comparable rigor on the player-experience side yet."**

These all sound like weaknesses, but they're actually *strengths in disguise*: they show you know exactly what's not done and you've named the risks honestly. That's what serious people do.

---

## Likely Q&A — be ready with crisp answers

### "Why isn't this just D2/PoE with extra steps?"

*Differentiation question.* Answer:

"D2 and PoE have static content with seasonal patches. Their content velocity is bounded by manual production. This engine produces a fully balanced season in 41 minutes for under a dollar. The bet isn't on combat innovation — combat is genre-canonical. The bet is on content velocity at a price point no manual studio can match."

### "Are you building an engine or a game?"

*Scope clarity question.* Answer:

"Both, but separable. The engine could ship as middleware to other studios. The game could ship as a standalone product on a different content pipeline. I'd lead with whichever the market values more — that's actually part of why I want your read."

### "What player audience does this resonate with first?"

*Positioning question.* Answer:

"My guess is ex-PoE / ex-Diablo players who churned on content drought. Isekai-genre fans who haven't found a native-game adaptation. Mobile-first players who want depth but can't commit to PC sessions. But I'm guessing — that's the read I want from you."

### "How does this scale beyond solo?"

*Production reality question.* Answer:

"Engine work is well-suited to a small team — I have a 5-agent synthetic engineering team operating across the codebase right now, doing parallel work across content gen, simulation, telemetry, and presentation. Scaling to actual engineers, the obvious early hires are: a senior live-service engineer, a content designer, and a player-experience lead. Pre-scaling, the engine doesn't need more people — it needs more validation cycles."

### "Why LLMs vs hand-authored content?"

*Architectural rationale.* Answer:

"LLMs handle naming, flavor text, thematic coherence at a quality bar I couldn't reach with templates. But the LLM is only ~$1 of the cost — most of the engine work is deterministic Python + simulation. The LLM is doing what it's actually good at: language and theme. The math and balance are done classically. It's not 'LLM generates a game' — it's 'LLM does the language layer, engine does the systems layer.'"

### "What's it cost at 1M users?"

*Unit economics.* Answer:

"At ~$1 per season generated + ~10 seasons per year, the content cost per user is under $10/year — and that's BEFORE caching, sharing across users, or any LLM cost optimization. Compare to a live-service studio spending $30M/year on a 50-person content team supporting 1M users = $30/user-year just for content. This engine is 3× cheaper at scale, before optimization."

### "What's the IP/legal story on isekai?"

*Risk surface.* Answer:

"Isekai is a genre, not an IP — like 'cyberpunk' or 'fantasy.' The conceit is decades old. Specific properties (Slime Tensei, Re:Zero, etc.) are IP, but the genre conventions are public domain. The game uses isekai conventions, not isekai properties. No IP licensing required."

---

## Questions YOU should ask him

These are the marketability-feedback questions that turn the conversation into intel. Bring deliberate questions, not "what do you think?"

1. **"What's the closest thing you've seen in the industry to procedurally-generated balanced game content? Did it work or fail, and why?"**

2. **"Where would a content engine like this fit best — AAA live-service, mobile premium, indie? Which has the strongest pull for procgen + simulation balance?"**

3. **"What's the biggest risk you'd flag from a publisher's perspective?"**

4. **"If you were going to take this seriously as a product, what's the first thing you'd want to see beyond what I showed you today?"**

5. **"For the game specifically: who's the player audience that would resonate with weekly reincarnation + Earth Self collection? Are they real, or am I building for an audience that doesn't exist?"**

6. **"What's the path you'd take if this were you? Engine-first commercialization, game-first commercialization, or something else entirely?"**

7. **"If I wanted to take this seriously over the next 12 months, what would your first hire be?"**

---

## How to close the meeting

Two things to say in the last 5 minutes:

1. **Acknowledge his time and the value of the read.** *"Honestly, the part that matters to me is the candid take. Thanks for the time."*

2. **Ask if you can stay in touch.** *"I'll send a follow-up email with the URL — I'm continuing to build. If anything you've said sparks more thoughts later, I'd love to hear them."*

DO NOT pitch for anything else (job, intro, investment) unless he opens it. The whole frame of this meeting is "feedback only" — pivoting to advancement would feel transactional. If he wants to open that door, he will.

---

## After the meeting

- Capture his answers to your 7 questions in a notes file ASAP (within 2 hours, while memory is fresh)
- File at `pitch-2026-05-18/feedback-captured.md`
- jack-ryan can later help process the feedback into actionable design changes
- Don't email him for at least 48 hours unless he asked for something specific — gives him space to think

---

## Reminders for the day

- Open `https://reincarnated-loadout.vercel.app` on phone BEFORE the meeting; verify it loads cleanly
- Have the one-pager (PDF or shareable link) ready to send him after the meeting, not before
- Don't open with apologies ("sorry to take your time", "this is rough", etc.) — sets the wrong frame
- If he asks "what specifically do you want from this conversation," answer honestly: "candid industry read on marketability"
- Phone on silent. Notebook ready for capturing his answers.

Good luck.
