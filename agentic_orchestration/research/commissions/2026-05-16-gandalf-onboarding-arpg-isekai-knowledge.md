# Legolas commission — Gandalf onboarding: ARPG + isekai current-day knowledge

**Date:** 2026-05-16
**Commissioner:** knight-rider (authoring initial commission on Gandalf's behalf; Gandalf will follow up with refined commissions after his Phase-1 self-assessment)
**Mode:** A — analytical research
**Priority:** Active — Gandalf's Phase-2 deliverable depends on this
**Output location:** `agentic_orchestration/research/knowledge/<subdirectory-per-topic>/<YYYY-MM-DD>-<slug>.md`

## Why this commission exists

Gandalf's persona is a long-lived being whose layered experience includes founding-Diablo-team work, anime/isekai media houses, and cross-development veteran knowledge. But his training-data knowledge cutoff means he likely lacks:

- Recent isekai genre evolution (2023-2026)
- Community-side ARPG design discourse from blogs, forums, postmortems
- PoE design philosophy depth from GGG dev manifestos and Chris Wilson talks
- Diablo 4 + Immortal post-launch community design analysis
- Adjacent ARPG design (Last Epoch, Grim Dawn, Lost Ark — community discussions)

This commission fills the gaps so Gandalf's Phase-2 deliverable and ongoing critique work is grounded in current-day genre discourse, not just training-cutoff defaults.

## Scope — five focused passes

Produce **one findings file per topic**, in priority order. Don't try to combine them — separate files for separate topics are easier for Gandalf to consume and reference.

### Pass 1 — Isekai genre evolution (2023-2026)

**Output:** `research/knowledge/isekai/2026-05-16-isekai-evolution.md`

Questions:
- What major isekai series have shipped or evolved since 2023? (Mushoku Tensei seasons, Solo Leveling adaptation, recent light-novel adaptations)
- What new isekai sub-tropes have emerged? (Slime/spider/dragon protagonist patterns, LLM-themed isekai, game-world-as-real isekai variants)
- How are "reincarnated as X" tropes structured narratively? What beats land?
- What does the genre's audience currently expect from a "reincarnated as a slime / spider / non-humanoid" premise?
- Where is the genre moving — toward more meta/self-aware, toward darker themes, toward power-fantasy doubling-down?

Sources: anime news sites, MyAnimeList community discussion, light-novel reader forums, isekai-specific subreddits, recent genre essays.

### Pass 2 — Diablo design retrospectives (all four PC titles + Immortal)

**Output:** `research/knowledge/diablo/2026-05-16-diablo-design-retrospectives.md`

Questions per title:
- **Diablo I (1996)** — atmosphere/tone choices that defined the genre. What design decisions still echo.
- **Diablo II (2000)** — class design rhythm, skill tree structure, itemization philosophy. Why it became the genre's reference point.
- **Diablo III (2012-2014)** — audience-broadening decisions, the auction house controversy, post-launch Reaper of Souls rebuild. What was lost vs gained.
- **Diablo IV (2023)** — modern-loot reconciliation, season structure, Vessel of Hatred expansion. Current state of community design discourse.
- **Diablo Immortal (2022)** — mobile-platform compromises, monetization design, what the team prioritized vs sacrificed.

Sources: Blizzard postmortems, GDC talks, dev interviews, community design analysis blogs (icy-veins, maxroll, mobalytics), Reddit r/Diablo discussions of specific design choices.

### Pass 3 — Path of Exile design philosophy

**Output:** `research/knowledge/poe/2026-05-16-poe-design-philosophy.md`

Questions:
- GGG / Chris Wilson dev manifestos and design philosophy statements (the "Path of Exile manifesto," GDC talks, ExileCon presentations)
- Passive skill tree design rationale and trade-offs
- Gem socket / support gem system design choices
- Currency-as-crafting design philosophy
- Endgame design (atlas, mapping, leagues) — what the team optimized for
- PoE 2 design changes and what they signal about the team's current philosophy
- Where the community sees PoE excelling vs struggling

Sources: GGG official news, Chris Wilson's GDC talks, path-of-exile subreddit design discussions, poe-vault and pathofexile.fandom community analysis.

### Pass 4 — ARPG community design discourse

**Output:** `research/knowledge/arpg-community/2026-05-16-arpg-design-discourse.md`

Questions:
- What design patterns does the modern ARPG community consider "best practices"? (Build diversity, loot generosity, season structure, endgame depth)
- What anti-patterns does the community call out repeatedly? (Bloat, mandatory grind, gear-as-gate, monetization-as-mechanic)
- How has loot design evolved across genre? (Generic-stick-of-stats vs uniques vs crafted vs set bonuses)
- What's the current discourse on AOE-vs-single-target balance specifically?
- How do communities discuss "class fantasy" — what makes a class feel like itself vs feel generic?

Sources: ARPG-focused YouTube design analysis channels, community blogs, broader gaming-design discourse sites.

### Pass 5 — Adjacent ARPGs (comparison knowledge)

**Output:** `research/knowledge/arpg-adjacent/2026-05-16-adjacent-arpgs.md`

Brief design summaries — what each game prioritizes, where it diverges from Diablo/PoE:
- Last Epoch (skill specialization tree, item factions, recent 1.0)
- Grim Dawn (dual-class system, faction system)
- Lost Ark (MMO-ARPG hybrid; Western vs Korean version differences)
- Torchlight 1/2/3 (varied design generations)
- Wolcen, Chronicon, Undecember — briefer notes

## Constraints

- **Read-only.** Public web sources only. No paywalled content unless freely available.
- **Cite specifically.** URLs in source list at end of each file. Inline citations to specific developer talks or posts.
- **Don't synthesize for Gandalf.** Bring back well-organized facts. Gandalf will synthesize.
- **Time-bound per pass.** Aim for ~45-60 minutes per pass; 5 passes total ~4-5 hours of Legolas work spread across the commission.
- **Order matters.** Pass 1 (isekai) and Pass 2 (Diablo) first — they're most directly relevant to Reincarnated's design lineage. Passes 3-5 can come after.

## Completion record

**Completed:** 2026-05-16
**Agent:** legolas

### Output paths

| Pass | Output file |
|---|---|
| Pass 1 — Isekai evolution | `research/knowledge/isekai/2026-05-16-isekai-evolution.md` |
| Pass 2 — Diablo retrospectives | `research/knowledge/diablo/2026-05-16-diablo-design-retrospectives.md` |
| Pass 3 — PoE design philosophy | `research/knowledge/poe/2026-05-16-poe-design-philosophy.md` |
| Pass 4 — ARPG community discourse | `research/knowledge/arpg-community/2026-05-16-arpg-design-discourse.md` |
| Pass 5 — Adjacent ARPGs | `research/knowledge/arpg-adjacent/2026-05-16-adjacent-arpgs.md` |

### Per-pass summary

**Pass 1 (isekai):** 34 series in 2024, 15% of all TV anime — genre at plateau. Major series: Mushoku Tensei S2 (2023–2024), Solo Leveling adaptation (Winter 2024), Slime S3 (Spring 2024). Sub-tropes documented: villainess/otome, non-humanoid (slime/spider/dragon), game-world-as-real, slow-life. Key direction finding: Frieren and Dungeon Meshi (neither is isekai) are absorbing the prestige audience — the isekai mechanic was a delivery vehicle, and the genre is fragmenting between those who want the vehicle and those who want quality fantasy.

**Pass 2 (Diablo):** Full retrospective across five titles. D1: horror-inflected, turn-based→real-time origin story, "mom test" UI philosophy. D2: seven-class archetypes, named-unique itemization, synergy system — the genre's reference standard because items had identity and the farming loop was unsubstitutable. D3: AH disaster (regretted within 2 months), Reaper of Souls course-corrected with Loot 2.0 and season structure. D4: Season 1 backlash (mass nerfs, "fixed an issue where players were having fun") recovered by Season 2; Vessel of Hatred (Oct 2024) praised. Immortal: pay-to-win via legendary gems, $10K–$100K to max estimate, brand damage.

**Pass 3 (PoE):** GDC 2019 "Play Forever" talk captured in detail — seasonal cadence, burnout management, multiple randomness axes. Passive skill tree: 1300+ nodes, internal GGG debate (simplify vs. keep iconic complexity). Currency-as-crafting: functional + trade value, no gold. Support gem system documented (PoE1: sockets on gear; PoE2: sockets on skills). PoE2 design intent: slower/methodical combat, dodge-roll centric, accessibility improvement, same microtransaction pool. Community view: excels at depth/build diversity; struggles at new-player onboarding, trade friction.

**Pass 4 (ARPG discourse):** Best practices: build diversity, smart loot, seasonal structure with resets, meaningful endgame depth. Anti-patterns: mandatory grind, gear-as-gate, bloat (complexity without decisions), monetization-as-mechanic (Immortal as canonical example). Loot evolution table documented (D1 → D2 → D3/AH failure → RoS → PoE era → Last Epoch factions → D4 tempered affixes). AOE/ST balance: no consensus formula — encounter design is the real lever, not damage ratios. Class fantasy: distinct player behavior pattern required, not just different skins.

**Pass 5 (adjacent ARPGs):** Last Epoch 1.0 (Feb 2024): per-skill trees + item factions are the genre's best recent innovations. Grim Dawn: dual-class + devotion = best build diversity, but new player hostile. Lost Ark: MMO-ARPG hybrid; Western version differences documented (censorship, class count, P2W reduction, update lag); honing system as gear-gate conflict with Western expectations. Torchlight: T1/T2 beloved (accessible D2 with pet system); T3 failed (identity loss, mobile feel); Infinite = mobile live-service. Wolcen: broken skills, abandoned — cautionary tale. Chronicon: competent indie, D2 formula. Undecember: classless Korean ARPG, PoE-flexible-but-accessible positioning.

### Sources that were thin or unavailable

- **LLM/AI-themed isekai:** Only anecdotal web-novel community evidence; no anime adaptation data
- **PoE ExileCon talks:** Referenced but not directly sourced from the vault
- **D4 Season 4+ Loot Reborn reception:** Major design overhaul not fully captured
- **Grim Dawn DLC design specifics:** Not sourced beyond base game
- **Lost Ark 2024–2025 player retention data:** Not available in public sources consulted
- **ARPG YouTube design analysis channels** (Asmongold, Rhykker, Raxx discourse): Commission specified these; time constraints prevented deep-dive into video content
- **PoE2 post-EA full launch plans:** Still ongoing; timeline not confirmed
