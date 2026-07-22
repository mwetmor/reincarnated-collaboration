# Research — Game Combat AI Landscape 2024–2026 — 2026-07-22

**Mode:** A (analytical)
**Commissioner:** Gandalf (design steward) — feeding live architecture decision
**Context:** Evaluating a "Reader stack" combatant-AI candidate (utility-scored decision layer + influence/exposure map + steering execution; BTs reserved for boss phases; GOAP/HTN/MCTS/RL/LLM-runtime parked). Feeding a preregistered formation-AWARE vs formation-BLIND fighter experiment and the long-term sim + Godot 4.x presentation layer.
**Sources consulted:** GDC Vault 2024/2025/2026, NVIDIA developer blog, Ubisoft La Forge publications, EA SEED, Sony AI / Gran Turismo Sophy, poe-vault.com, icy-veins.com, game-specific news coverage, arxiv.org, Godot Asset Library, GitHub repos.

---

## Summary (3–5 sentences)

Modern ARPGs ship mob AI that is almost entirely authored, scripted, or utility-scored at a per-monster-type level — not learned — and the design sophistication that ships is lower than community perception. The most significant 2024–2026 development in shipped game combat AI is the System 1 / System 2 split (tick-rate behavior tree for reactive combat actions; slower LLM or SLM layer for strategic intent-setting from player commands), pioneered in shipped form by PUBG Ally (GDC 2026, Krafton + NVIDIA) and NARAKA: BLADEPOINT (GDC 2025, NetEase + NVIDIA ACE) — but critically, the LLM/SLM layer in both cases handles communication and goal-setting, never real-time combat targeting or movement decisions. GDC AI Summit material 2024–2026 continues to treat utility AI + director systems as the production-viable backbone of NPC combat, with LLMs positioned exclusively at authoring time (BT generation) or high-latency strategic layers. The Godot 4.x AI ecosystem has a capable, actively-maintained BT+HSM stack (LimboAI, 2.9k stars, v1.8.0 June 2026) and a utility AI GDExtension, but the GDQuest steering framework targeting Godot 3.x is unmaintained. No post-training-cutoff development contradicts Gandalf's Reader-stack verdict; the two-system shipped examples reinforce it.

---

## Findings by Question

### Q1 — ARPG combat/mob AI state of practice 2024–2026

**Path of Exile 2 (Grinding Gear Games, Early Access Dec 2024; Dawn of the Hunt Apr 2025)**

The standard PoE 2 monster roster uses conventional mob archetypes: melee aggressor, ranged caster, proximity trigger, swarm-type. No GGG developer postmortem or talk on the underlying AI architecture has been published or surfaced. The notable design innovation is the **Rogue Exiles** system, introduced in the Dawn of the Hunt league (April 2025). Rogue Exiles are mini-boss-tier elite enemies that carry player-class skill gems, use dodge-roll, and reposition with what the promotional copy calls "smart pathfinding." GGG's stated design goal is to feel like fighting another Exile (PvP-adjacent). The underlying implementation is not publicly documented as ML or learned — all evidence points to authored scripted behavior mimicking player skill sequences with rule-based dodge-roll triggers. No tech talk, postmortem, or developer interview on the AI system architecture was found.

Sources: [Rogue Exiles Are Coming to PoE2: And They Fight Like Real Players — poe-vault.com](https://www.poe-vault.com/poe2/news/rogue-exiles-are-coming-to-poe2-and-they-fight-like-real-players); [Path Of Exile 2: Rogue Exiles, Explained — The Gamer](https://www.thegamer.com/path-of-exile-poe-2-rogue-exiles-explained/); [Rogue Exiles wiki — Fextralife](https://pathofexile2.wiki.fextralife.com/Rogue+Exiles)

**Diablo 4 Season 11 (Blizzard, released ~late 2025)**

Blizzard shipped a significant monster behavior rework in Season 11. The key structural change: monsters moved from a **cooldown-driven action pattern** to a **behavior pool with difficulty-scaling selection**. Concretely, each monster type draws actions from a set of behaviors whose availability adjusts by difficulty tier. Elite and Champion monsters receive more complex behavior sets and HP scaling. Specific role differentiation was added: ranged enemies maintain distance, large units prioritize disruption, swarmers actively surround. Pack spatial spread was increased to reduce AoE triviality. Telegraph clarity was improved on high-disruption attacks. Developer commentary (Colin and Zaven, paraphrased via Raxxanterax interview, Icy Veins coverage) describes the philosophy as "less passive power creep, more meaningful challenge." No AI architecture terminology (behavior trees, utility scores) was disclosed publicly.

Key design note: the "behavior pool" language strongly resembles utility-scored action selection, but this is inferred from design description, not confirmed by developer technical statement.

Sources: [Why Diablo 4 Is Redesigning Monsters and Defenses in Season 11 — Icy Veins](https://www.icy-veins.com/d4/news/why-diablo-4-is-redesigning-monsters-and-defenses-in-season-11/); [Diablo 4 Season 11 Brings Major Monster Reworks — Icy Veins](https://www.icy-veins.com/d4/news/diablo-4-season-11-brings-major-monster-reworks/)

**Last Epoch (Eleventh Hour Games, acquired by Krafton 2025)**

Season 3 (timing unspecified in sources) includes overhauls to monster behavior and skills, and smarter minion AI. No developer technical talk on mob AI architecture found. The studio is publicly navigating a "no AI tools" positioning (manual, verified design) following Krafton's "AI-first company" announcement, but this refers to generative AI content tools, not game AI behavior systems.

Sources: [Last Epoch Developers Comment on Krafton's AI Adoption Course — ixbt.games](https://ixbt.games/en/news/2025/11/29/avtory-last-epoch-prokommentirovali-kurs-krafton-po-vnedreniiu-ii.html)

**No Rest for the Wicked (Moon Studios, Early Access Apr 2024)**

Animation-driven precision combat; enemy AI is described as reactive to being cornered or outnumbered in the co-op update. No technical AI talk found. The game's design priority is animation-over-AI — enemies punish mistimed actions rather than executing complex decision trees.

Sources: [No Rest for the Wicked — Wikipedia](https://en.wikipedia.org/wiki/No_Rest_for_the_Wicked_(video_game)); [Moon Studios co-op update announcement — rpgsite.net](https://www.rpgsite.net/news/19351-no-rest-for-wicked-together-co-op-update-new-gameplay-trailer)

**Hades II (Supergiant Games, Early Access May 2024; v1.0 Sep 2025)**

No developer talk on enemy AI architecture found. Supergiant has publicly stated no generative AI use. The combat design follows Hades I's pattern: carefully authored encounter rooms with per-room enemy type combinations, not emergent or learned behavior. Enemy behaviors are presumably authored state machines or simple BTs, consistent with a studio of ~20 people shipping a roguelike.

Sources: [Hades II v1.0 Coming September 25, 2025 — Supergiant Games](https://www.supergiantgames.com/blog/hades2-coming-sep25/); [Hades II Wikipedia](https://en.wikipedia.org/wiki/Hades_II)

**Titan Quest 2 (Grimlore Games, Early Access 2025)**

Enemy AI described as hand-authored; enemies form factions and combine skills. Reviewer notes mobs retreat, regroup, or flank — but inconsistent hit detection undermines the effect. No AI architecture talk found. "Hand-authored encounter" language is explicit in developer statements.

Sources: [Titan Quest II Wikipedia](https://en.wikipedia.org/wiki/Titan_Quest_II); [Titan Quest II Review — NGOHQ.com](https://www.ngohq.com/2025/08/05/titan-quest-ii-review/)

**Cross-title synthesis**

The per-agent AI sophistication that modern ARPGs actually ship is: authored mob-type behavioral patterns (melee/ranged/caster roles), rule-based engagement triggers, scripted skill rotations, and at most a behavior-pool / weighted-action-selection layer that resembles utility scoring without being publicly confirmed as such. Pack-level formation coordination in ARPGs is designed, not emergent — it manifests as spawn group composition and role mix, not runtime formation maintenance. The "smarter AI" framing in seasonal updates (Diablo 4) refers to richer action sets and better role differentiation, not architectural changes. No ARPG in this survey has shipped learned or LLM-runtime mob AI.

---

### Q2 — GDC 2024–2026 AI Summit material

**GDC 2024 AI Summit (March 2024, Moscone Center, San Francisco)**

Notable sessions surfaced:

- **"From Text to Gameplay: Generative AI's Influence on Behavior Trees"** — Pierre-Arjun Dalaya, Trevor Santarra (Unity Technologies). Explores LLM-assisted behavior tree *authoring* (generation-time, not runtime). Key claim: LLMs can generate BT code from natural-language specs, increasing designer iteration speed. Not a runtime combat AI talk. [GDC Vault](https://gdcvault.com/play/1034764/AI-Summit-From-Text-to)

- **"Game AI Fireside Chat with Damian Isla and Jeff Orkin: Celebrating 20+ Years of Behavior Trees and Automated Planning Systems"** — Isla (Halo BT lineage) and Orkin (F.E.A.R. GOAP lineage) in retrospective. The fact that GDC invited both architects of the canonical BT and GOAP canons for a joint retrospective in 2024 signals that both approaches are viewed as mature/settled rather than live design debates. [GDC schedule](https://schedule.gdconf.com/session/game-ai-fireside-chat-with-damian-isla-and-jeff-orkin-celebrating-20-years-of-behavior-trees-and-automated-planning-systems/917672)

Dave Mark (IAUS, Intrinsic Algorithm) remains the canonical reference for utility AI in games. His 2018 GDC Vault talk "Spatial Knowledge Representation through Modular Scalable Influence Maps" remains the industry reference for influence-map architecture, presented as a complete data-driven architecture for spatial processing across FPS/RPG/sports/strategy genres. No new 2024–2025 IAUS/Mark talk was found surfaced in public search. [GDC Vault 2018](https://www.gdcvault.com/play/1025243/Spatial-Knowledge-Representation-through-Modular)

**GDC 2025 AI Summit (March 2025)**

- **"Growing an AI Director into a Full Adventure Director"** — Marie Mejerwall (Mejerwall Consulting), studio/game not publicly disclosed. Documents the evolution of a Spawn Director (tactical pacing: when/what to spawn) into an Adventure Director (full procedural NPC experience for a co-op action game). Architecture: procedural generation layer + authored override layer. Key insight: the director decides *what* NPCs spawn and at what density; individual NPC behavior is separate. [GDC Vault](https://gdcvault.com/play/1035589/Game-AI-Summit-Growing-an)

- **"Achieving AI Teammates in NARAKA: BLADEPOINT MOBILE PC VERSION"** — NetEase + NVIDIA (GDC 2025). NVIDIA ACE-powered AI teammates shipped in March 2025. Combat behavior handled by scripted/authored systems; ACE adds voice-based tactical coordination (scouting, item gathering, armor swapping on player request). Presented at GDC 2025. [NVIDIA On-Demand](https://www.nvidia.com/en-us/on-demand/session/gdc25-gdc1009/)

- **"Beyond the Hype: Real-World Applications of Google AI in Gaming"** — Jetha Chan, Ju-yeong Ji, Ishan Sharma (Google/DeepMind). Focuses on Gemini/Gemma for developer *workflows*, not runtime combat AI. No combat AI content surfaced in public abstract. [GDC Vault](https://gdcvault.com/play/1035350/Game-AI-Summit-Beyond-the)

- **GDC 2025 AI Summit Experimental Workshop** — Tommy Thompson's newsletter ("Reflections on GDC 2025") covers this session but is behind a paywall. Thompson confirmed a generative AI talk by Ada Eden (1001 Nights game) was well-attended; practical shipped implementations were the focus.

**GDC 2026 AI Summit (March 2026)**

- **"Building a Co-Playable Character: PUBG Ally, an AI Teammate Powered by NVIDIA ACE"** — Kim Hyunseung (KRAFTON AI), Evgeny Makarov (NVIDIA). See Q4 for full architecture details. This is the landmark shipped-AI talk of the 2024–2026 window. [GDC schedule](https://schedule.gdconf.com/session/building-a-co-playable-character-pubg-ally-an-ai-teammate-powered-by-nvidia-ace-presented-by-nvidia/917523)

- Other GDC 2026 AI content was dominated by generative AI workflow tooling (UA creative production, 3D prototyping with LLMs, MCP-based rapid prototyping). The Tencent session covered multi-agent scene layout reasoning and intent-driven scene editors — not combat AI behavior.

**Synthesis for the Reader-stack question**

The GDC 2024–2026 record shows: (a) utility AI + director systems are the uncontested production backbone for NPC combat pacing; (b) BTs and GOAP are retrospective legacy topics, not live architectural competition; (c) LLMs appear exclusively at authoring time or as high-latency goal-setting layers; (d) influence/spatial maps remain the canonical substrate for spatial reasoning (Dave Mark's 2018 work is still the reference, unreplaced). No GDC talk challenged or superseded the utility + influence map + steering stack as the production-viable approach for per-agent combat AI.

---

### Q3 — Learned agents in shipped games or production pipelines 2024–2026

**Gran Turismo Sophy (Sony AI / Polyphony Digital)**

Sophy reached full global release for Gran Turismo 7 players in late 2023 / early 2024. Subsequent development: Sophy 2.1 (March 2025) added Custom Race support with tuned cars. Sophy 3.0 (December 2025, Power Pack DLC, $29.99 paywall) is the most capable version. An independent 2025 research paper trained a vision-only Sophy variant (in-car camera + IMU only, no track geometry oracle) that reached champion level and out-performed the original Sophy on Tokyo Expressway — the finding being that vision-based spatial perception of opponent orientation outperformed positional tracking alone in at least one circuit. This is the most significant learned-agent research delta in the window: oracle geometry access is not always the strongest policy. However, Sophy operates in a fully continuous-state, single-agent racing domain and does not transfer architecture to multi-agent melee combat.

Sources: [Gran Turismo 7's Sophy AI Project Turns Five Years Old — GTPlanet](https://www.gtplanet.net/gran-turismo-7s-sophy-ai-project-turns-five-years-old-20260718/); [Sony AI press release](https://www.prnewswire.com/news-releases/sony-ai-announces-full-global-release-of-ai-driver-gran-turismo-sophy-for-gran-turismo-7-players-in-latest-update-301973930.html)

**Ubisoft La Forge (Smart Bots Group)**

Active RL research program, 2024–2025 publications:

- "Efficient Active Imitation Learning with Random Network Distillation" (ICLR 2025) — data-efficient imitation for bot behavior.
- "Offline Learning of Controllable Diverse Behaviors" (ICLR Workshop Generative Models 2025) — offline RL for diverse NPC behavior generation.
- "Minimax Exploiter: A Data Efficient Approach for Competitive Self-Play" (AAMAS 2024) — data-efficient adversarial agent training.
- "Efficient Visibility Approximation for Game AI using Neural Omnidirectional Distance Fields" (I3D-PACMCGIT 2024) — neural methods for agent perception/awareness.
- Navigation-focused RL (RLC-RLVG Workshop 2025, IEEE CoG 2025, IJCNN 2025) — hierarchical and continual RL for navigation.

Ubisoft's public framing: Smart Bots are for *game testing* (increasing test coverage in AAA games including Battlefield 2042 and Dead Space). The scaling path to AI enemies for players is acknowledged as potential but not shipped in a player-facing product. Key constraint Ubisoft has stated: bots are incentivized toward specific behaviors (e.g., defending) rather than maximum win-rate, to add variability.

Sources: [Ubisoft La Forge publications](https://www.ubisoft.com/en-us/studio/laforge/publications); [La Forge — Next Gen NPCs blog](https://www.ubisoft.com/en-us/studio/laforge/news/4PRxOnlOgGwEPcXYxZRQsq/ubisoft-la-forge-pushing-stateoftheart-ai-in-games-to-create-the-next-generation-of-npcs)

**EA SEED**

A 2023 paper ("Technical Challenges of Deploying Reinforcement Learning Agents for Game Testing in AAA Games," CoG 2023) documents RL agent deployment for QA in Battlefield 2042 and Dead Space (2023). Scope is explicitly *test coverage* (QA), not balance-testing. No 2024–2025 EA SEED publication on balance-testing bots was found. The paper acknowledges the largest unsolved problems are domain transfer and behavioral diversity, not sample efficiency.

Sources: [EA SEED CoG 2023 — ea.com](https://www.ea.com/seed/news/cog23-challenges-deploying-rl-agents-game-testing); [arxiv:2307.11105](https://arxiv.org/pdf/2307.11105)

**CombatVLA (academic prototype, March 2025)**

"CombatVLA: An Efficient Vision-Language-Action Model for Combat Tasks in 3D Action Role-Playing Games" (Chen et al., revised Jan 2026; accepted ICCV 2025). A 3B-parameter VLA model trained on video-action pairs formatted as "action-of-thought (AoT) sequences" for ARPG combat, claiming 50x acceleration and higher success rates than human players on benchmark tasks. This is pure research prototype — not shipped in any game. Resources are to be open-sourced.

Sources: [arxiv:2503.09527](https://arxiv.org/html/2503.09527)

**Artificial Agency (startup, launched alpha July 2025)**

Founded by ex-Google DeepMind researchers. Their behavior engine (alpha, July 2025) supports autonomous Characters (memory, learning, dynamic reaction) and Game Directors (story progression). Runtime decision-making is claimed. Underlying technical architecture (RL, utility, LLM) and partner studio names are not publicly disclosed as of the launch announcement. Pilot program access only.

Sources: [Artificial Agency launch announcement — globenewswire.com](https://www.globenewswire.com/news-release/2025/07/10/3113377/0/en/Artificial-Agency-Launches-Behavior-Engine-to-Create-Video-Games-That-Feel-Truly-Alive.html)

**Synthesis for balance-testing-bot state of practice**

Balance testing bots in the industry are: scripted rule-based bots with behavioral parameterization (dominant), RL bots used for QA/test coverage (Ubisoft, EA SEED — not for balance specifically), and self-play bots in competitive/multiplayer games (Gran Turismo Sophy is the clearest example). No team has published a shipped, player-visible learned combat policy in an ARPG-style game. The gap between research capability and production deployment remains substantial in 2026.

---

### Q4 — LLM-driven game agents 2025–2026: real-time combat control?

**The field consensus, confirmed**

The field does not ship LLMs for real-time combat targeting, movement, or per-tick tactical decisions. This is confirmed by both the shipped examples and the research community's framing.

**PUBG Ally (KRAFTON + NVIDIA ACE, shipped public beta summer 2026)**

This is the most technically documented shipped LLM-in-a-game-combat-context system in the window.

Architecture (System 1 / System 2):
- **System 1 — Behavior tree at game tick rate.** Handles movement, positioning, targeting, immediate threat responses. Operates continuously and independently. "Reflex-level actions never have to wait for the model."
- **System 2 — Quantized 2B-parameter Mistral-NeMo-Minitron SLM on-device.** Interprets player voice commands; generates "steerable commands" that modify System 1's goal state. Runs event-driven, triggered by player speech or significant game events. Latency: full pipeline (ASR + SLM + TTS) under 2.5 seconds on RTX 3060 8GB VRAM minimum spec.
- The SLM never makes real-time combat decisions independently. All combat execution routes through the behavior tree.

Training: 500,000 input/output pairs, LoRA fine-tuning on 8x H100, 10–13 hours. "Gap mining" for domain coverage. Supports English, Korean, Chinese. Cross-session long-term memory via compressed dialogue observation.

GDC 2026 session: "Building a Co-Playable Character: PUBG Ally, an AI Teammate Powered by NVIDIA ACE" (Kim Hyunseung, KRAFTON; Evgeny Makarov, NVIDIA).

Sources: [NVIDIA developer blog — How KRAFTON Built PUBG Ally](https://developer.nvidia.com/blog/how-krafton-built-pubg-ally-a-co-playable-character-powered-by-nvidia-ace/); [KRAFTON AI blog — From Workflow-Based SLM to Autonomous Agent](https://www.krafton.ai/blog/posts/2026-04-15-pubg_ally_nemotron/pubg-ally-nemotron-en.html); [GDC schedule](https://schedule.gdconf.com/session/building-a-co-playable-character-pubg-ally-an-ai-teammate-powered-by-nvidia-ace-presented-by-nvidia/917523)

**NARAKA: BLADEPOINT Mobile PC (NetEase + NVIDIA ACE, shipped March 2025)**

NVIDIA ACE-powered AI companions handling scouting, item gathering, armor swapping, suggestions on skills. Combat behavior (targeting, shooting, movement in a battle royale) handled by separate authored systems. ACE provides the voice interaction and coordination layer. GDC 2025 session confirms this architecture.

Sources: [NVIDIA GeForce News — ACE Autonomous Game Characters](https://www.nvidia.com/en-us/geforce/news/nvidia-ace-autonomous-ai-companions-pubg-naraka-bladepoint/); [NVIDIA On-Demand GDC 2025 session](https://www.nvidia.com/en-us/on-demand/session/gdc25-gdc1009/)

**GDC 2024 — LLM + BT authoring (Unity)**

LLMs generating behavior tree code at authoring time (not runtime). Confirms the field uses LLMs as BT authoring tools, not as runtime combat decision-makers.

**CombatVLA (research prototype only, not shipped)**

A 3B VLA model can execute ARPG combat actions in a research benchmark faster than human baseline. This is 2025 academic work; no shipping path or game partnership announced.

**Field consensus verdict**

LLM/SLM use in shipped games is confined to: (1) authoring-time BT generation (Unity, GDC 2024); (2) high-latency goal-setting and voice command interpretation with combat execution delegated to authored behavior trees (PUBG Ally, NARAKA). Real-time per-tick combat control by LLMs is not shipped anywhere in the industry as of mid-2026. The Reincarnated project's position (LLMs at generation time; not runtime) is exactly consistent with current industry practice.

---

### Q5 — Godot 4.x AI ecosystem current state

**LimboAI (BT + HSM)**

- GitHub: [limbonaut/limboai](https://github.com/limbonaut/limboai)
- Stars: 2,900+
- Latest release: v1.8.0 (June 19, 2026)
- Godot version support: 4.4–4.6 (v1.6.x+); 4.3 supported up to v1.3.x; current series requires 4.6+
- Implementation: C++ GDExtension (no custom engine build required); full GDScript support for authoring tasks and states
- Features: behavior tree editor, visual debugger, blackboard system for inter-task data sharing, subtree reuse, BTState node combining BT execution within HSM, extensive demo project
- Open issues: 57; actively maintained (v1.8.0 shipped June 2026)
- Assessment: **production-grade, actively maintained, the strongest BT option in the Godot 4 ecosystem**

Sources: [limbonaut/limboai — GitHub](https://github.com/limbonaut/limboai); [Godot Asset Library LimboAI 4.4–4.5](https://godotengine.org/asset-library/asset/3787)

**Beehave (BT for Godot)**

- GitHub: [bitbrain/beehave](https://github.com/bitbrain/beehave)
- GDScript implementation; MIT license
- Last updated: February 9, 2026 (confirmed active)
- Godot 4.x branch available
- Lighter-weight than LimboAI; lacks HSM integration and some visual tooling
- Assessment: **active but lighter — suitable for simpler BT needs; LimboAI is the more capable option**

Sources: [bitbrain/beehave — GitHub](https://github.com/bitbrain/beehave); [Godot Asset Library](https://godotengine.org/asset-library/asset/1349)

**Utility AI GDExtension (JarkkoPar)**

- GitHub: [JarkkoPar/Utility_AI](https://github.com/JarkkoPar/Utility_AI)
- C++ GDExtension; MIT license
- Submitted to Godot Asset Library: January 24, 2024
- Godot 4.1 listed on asset library page (last updated date: January 2024)
- Features: utility-based AI Agent Behaviour nodes, utility-enabled Behaviour Tree nodes, utility-enabled State Tree nodes, Node Query System (find top-N nodes, with time budgeting)
- Platform: Windows + Linux binaries; experimental macOS and Web/Wasm
- Assessment: **promising but the asset library page shows Godot 4.1 support and Jan 2024 update date — unclear whether it tracks current Godot 4.6. Requires verification of current maintenance before drax seam adoption.**

Sources: [Utility AI GDExtension — Godot Asset Library](https://godotengine.org/asset-library/asset/2260); [JarkkoPar/Utility_AI — GitHub](https://github.com/JarkkoPar/Utility_AI)

**Godot Steering AI Framework (GDQuest)**

- GitHub: [GDQuest/godot-steering-ai-framework](https://github.com/GDQuest/godot-steering-ai-framework)
- Stars: 1,500
- Last release: v3.0 (May 2020)
- **Built for Godot 3.x. Not ported to Godot 4. Unmaintained.**
- Assessment: **do not use for Godot 4 presentation layer. Seek a Godot 4-native steering implementation.**

Sources: [GDQuest/godot-steering-ai-framework — GitHub](https://github.com/GDQuest/godot-steering-ai-framework)

**Godot 4 built-in NavigationServer + CharacterBody**

Godot 4.0+ ships a rewritten NavigationServer with proper 3D navmesh support, navigation agents, and avoidance. For 2D, NavigationAgent2D with tilemap-baked navigation regions is the standard pattern. Built-in, no addon required. Supports NavigationLink equivalents for jump connections between navmesh islands.

Sources: [Navigation Server for Godot 4.0 — Godot Engine blog](https://godotengine.org/article/navigation-server-godot-4-0/); [Godot 3D Navigation Jump Links — GitHub](https://github.com/smix8/Godot_3D_Navigation_Jump_Links)

**Godot 4.x AI ecosystem summary for drax seam**

| Tool | Type | Status | Godot 4.6 | Notes |
|---|---|---|---|---|
| LimboAI | BT + HSM | Actively maintained | Yes (v1.8.0) | Best-in-class; C++ + GDScript |
| Beehave | BT | Actively maintained | Yes (Feb 2026) | Lighter weight |
| Utility AI GDExtension | Utility + BT + Query | Unclear currency | Needs verification | Jan 2024 last asset-page update |
| GDQuest Steering Framework | Steering | Unmaintained | **No (Godot 3 only)** | Do not use |
| Built-in NavigationServer | Pathfinding | Shipped | Yes | Use for navmesh / pathfinding |

---

### Q6 — Evaluation methodology: information value of game-state reading

No industry or academic paper was found that specifically operationalizes "formation-aware vs formation-blind" as a controlled ablation experiment in a game combat simulator. The terminology and framing are novel to this project. What exists in adjacent literature:

**Closest academic work — Localized Observation Abstraction (Black and Darken, 2024)**

"Localized Observation Abstraction Using Piecewise Linear Spatial Decay for Reinforcement Learning in Combat Simulations" (Scotty Black, Christian Darken; arXiv:2408.13328, August 2024; MODSIM WORLD 2024 Conference). In a military (not game) combat simulation, they compare a *global observation* approach (agent sees all entities regardless of distance) vs. a *localized observation* approach (agent's state representation weights nearby entities more heavily via piecewise linear distance decay). The localized approach consistently outperforms the global approach across increasing scenario complexity. This is the closest available analog to "what is the information value of spatial reading" — it shows that *how* spatial information is structured in the observation matters for agent performance, not merely whether it is present. Note: this is an RL paper, not a utility-AI or scripted-agent paper.

Sources: [arxiv:2408.13328](https://arxiv.org/abs/2408.13328); [MODSIM WORLD 2024 coverage on ResearchGate](https://www.researchgate.net/publication/383428455)

**Adjacent work — Kiting in RTS Games Using Influence Maps (Uriarte and Ontañón, AAAI AIIDE 2012)**

Classic paper: influence maps applied to kiting behavior (attack and retreat) in StarCraft. The paper demonstrates that spatial influence propagation enables tactical reasoning (when to engage vs flee) that is not achievable with simple proximity checks. This is the canonical published case where reading spatial geometry produces a measurable behavioral advantage. Not a controlled ablation study, but demonstrates the existence of a spatial-reading advantage.

Sources: [AAAI AIIDE 2012 — Kiting in RTS Games Using Influence Maps](https://ojs.aaai.org/index.php/AIIDE/article/view/12544)

**Adjacent work — Hierarchical RL in StarCraft with Influence Maps (arxiv:2606.30092, 2026)**

More recent work combining hierarchical RL with influence maps and cluster-based scripts for StarCraft micromanagement. Influence map hashing encodes unit distribution as a matrix to compress the state space. Not a direct ablation of the information value, but confirms influence maps as an active research substrate for combat spatial reasoning.

Sources: [arxiv:2606.30092](https://arxiv.org/html/2606.30092v1)

**Adjacent work — GT Sophy vision-only variant (Sony AI, 2025)**

A vision-only racing agent (camera + IMU, no track geometry oracle) outperformed the original Sophy on one circuit because *seeing opponent orientation* directly provided richer tactical information than positional tracking alone. This is an empirical case where a richer observation modality (vision vs. oracle position) changed policy quality — an analogue to the "does reading formation geometry help?" question in a continuous-state domain.

**Methodology gap — what doesn't exist**

No paper was found that performs the specific experiment the Reincarnated project is designing: same-architecture agents with fight-state features ablated (e.g., enemy formation centroid, enemy cluster density, flanking angle) versus full features, measuring win-rate or fight-quality delta in a tick-based ARPG simulation. This experiment appears to be genuinely novel in its exact specification. The adjacent literature provides methodological precedents (observation ablation, localized vs global observation, oracle vs policy gap), but none in the exact ARPG-combat-sim framing.

**Methodological precedents the project can cite**

1. Localized Observation Abstraction (Black and Darken 2024): ablate observation structure, measure performance across scenario complexity.
2. Kiting with Influence Maps (Uriarte and Ontañón 2012): demonstrate that spatial map reading produces measurable tactical advantage over reactive proximity.
3. GT Sophy vision-only variant (Sony AI 2025): richer spatial observation changes policy quality empirically.
4. "Evolving Game Skill-Depth using General Video Game AI Agents" (Jialin Liu et al., arXiv:1703.06275, 2017): methodological framework for estimating skill-depth of a game using AI agents as evaluation instruments — citable as a framing precedent for using agent performance to measure game design information value.

---

## Knowledge gaps not resolved

1. **GGG (PoE 2) AI architecture** — No developer talk, postmortem, or technical blog post on how Rogue Exile dodge-roll triggers or the base mob AI behavior system is implemented. The gap is real; GGG does not publish technical AI talks.

2. **Diablo 4 AI internals** — Developer statements use "behavior pool" language but no architecture confirmation (BT, utility, FSM). Community-facing communication only.

3. **GDC 2025 AI Summit full session roster** — Tommy Thompson's authoritative newsletter recap is paywalled. Session metadata from GDC schedule/vault suggests utility AI and director systems were covered but detailed content was inaccessible without membership.

4. **Dave Mark 2024–2026 publications** — No new IAUS or influence-map talk found in the 2024–2026 window. His 2018 GDC vault talk remains the primary public reference. Whether he has presented at private industry events is unknown.

5. **Utility AI GDExtension (JarkkoPar) current Godot 4.6 compatibility** — Asset library page shows Godot 4.1 and January 2024. Actual current-branch compatibility with Godot 4.6 requires direct GitHub inspection; not resolved here.

6. **Formation-aware vs formation-blind controlled experiment** — No prior work found in this exact framing. The experiment Reincarnated is designing appears novel; no citation for direct methodological precedent in ARPG combat simulation exists.

---

## Deltas that should change Gandalf's verdict

**Verdict under review:** Reader stack = utility-scored decision layer (target choice + movement intent) fed by an influence/exposure map, steering-style execution; behavior trees reserved for boss phases; GOAP/HTN/MCTS/RL/LLM-runtime rejected or parked.

**Delta 1 — The System 1 / System 2 split is now an industry-documented shipped pattern. No change to verdict, but clarifies future BT role.**

PUBG Ally (GDC 2026) and NARAKA (GDC 2025) both demonstrate the same split: tick-rate authored system (BT in both documented cases) handles all combat execution; slow language model handles goal-setting from player commands. This does not argue for BTs over utility in the Reader stack — the Reader stack's decision layer can equally serve as System 1. What it confirms: the "BT reserved for boss phases" position is fully consistent with industry practice, where BTs are used precisely for the authored, reactive, tick-rate execution layer. If the project ever adds an LLM-driven companion or tactical advisor, the PUBG Ally architecture is the applicable template. **No change to core verdict; architecture precedent now has a primary-source citation.**

**Delta 2 — ARPG mob AI sophistication is lower than canonical game-AI literature might suggest. Reader stack is overqualified, not underqualified.**

Modern ARPGs — including market leaders PoE 2 and Diablo 4 — ship mobs with authored behavior sets, not utility scoring. Diablo 4 Season 11's "behavior pool" is the most sophisticated publicly described ARPG mob AI, and it is essentially weighted-random action selection from a designer-defined pool. The Reader stack (utility scoring with influence map) is more architecturally sophisticated than what the genre leads currently ship. This is an argument for the stack's adequacy, not against it. **No change to verdict.**

**Delta 3 — No evidence of learned / RL combat policies shipping in ARPGs or batch-sim analogues. GOAP/MCTS/RL parked status is confirmed.**

Ubisoft La Forge and EA SEED are the most advanced teams working toward learned agents in AAA games. Both remain in research / QA-testing application (not player-visible). CombatVLA is prototype-only. **Confirms parked status of RL/MCTS for the Reincarnated combat sim.**

**Delta 4 — LLM runtime rejection confirmed, but "authoring-time" LLM use is now standard industry practice.**

GDC 2024 (Unity), GDC 2025 (multiple talks), and GDC 2026 (Roblox MCP session) all document LLMs used to generate game content, BT code, or design assets at authoring time. This is now unremarkable. The Reincarnated project's generation-time LLM use is squarely in the industry mainstream. **No change to runtime rejection; confirms generation-time use is well-precedented.**

**Delta 5 — Formation-aware vs formation-blind experiment has no prior art in the exact framing. This is genuinely novel.**

The closest analogues are the Black and Darken localized observation ablation (military sim, 2024), the Uriarte/Ontañón kiting paper (RTS, 2012), and the GT Sophy vision variant (racing, 2025). None operationalize "formation reading" in a tick-based ARPG batch sim. The experiment design is sound by analogy to the observation-structure ablation literature, but the project will be establishing its own methodological precedent. This is informational — it means the preregistered experiment is original work, not a replication. **No change to verdict; the experiment has methodological support but no prior exact template to cite.**

**Net assessment: Gandalf's verdict stands. No finding in this survey warrants overturning or materially amending the Reader-stack recommendation.**

The one addition worth noting: the PUBG Ally System 1 / System 2 architecture should be on record as the applicable template for any future player-companion or tactical-voice-command feature, if that scope ever enters the Reincarnated roadmap.

---

## Source list

### Primary sources (developer / studio first-party)

1. GDC Vault — "Spatial Knowledge Representation through Modular Scalable Influence Maps" (Dave Mark, 2018): https://www.gdcvault.com/play/1025243/Spatial-Knowledge-Representation-through-Modular
2. GDC Vault — "AI Summit: From Text to Gameplay: Generative AI's Influence on Behavior Trees" (Dalaya, Santarra; Unity; 2024): https://gdcvault.com/play/1034764/AI-Summit-From-Text-to
3. GDC Vault — "Game AI Summit: Growing an AI Director into a Full Adventure Director" (Mejerwall; 2025): https://gdcvault.com/play/1035589/Game-AI-Summit-Growing-an
4. GDC Vault — "Game AI Summit: Beyond the Hype: Real-World Applications of Google AI in Gaming" (Chan, Ji, Sharma; Google/DeepMind; 2025): https://gdcvault.com/play/1035350/Game-AI-Summit-Beyond-the
5. GDC Schedule — "Building a Co-Playable Character: PUBG Ally, an AI Teammate Powered by NVIDIA ACE" (Kim Hyunseung, Makarov; KRAFTON/NVIDIA; 2026): https://schedule.gdconf.com/session/building-a-co-playable-character-pubg-ally-an-ai-teammate-powered-by-nvidia-ace-presented-by-nvidia/917523
6. NVIDIA Developer Blog — "How KRAFTON Built PUBG Ally, a Co-Playable Character Powered by NVIDIA ACE": https://developer.nvidia.com/blog/how-krafton-built-pubg-ally-a-co-playable-character-powered-by-nvidia-ace/
7. KRAFTON AI Blog — "From Workflow-Based SLM to Autonomous Agent: Evolving PUBG Ally's Architecture" (Apr 2026): https://www.krafton.ai/blog/posts/2026-04-15-pubg_ally_nemotron/pubg-ally-nemotron-en.html
8. NVIDIA On-Demand — GDC 2025 session "Achieving AI Teammates in NARAKA: BLADEPOINT Mobile PC Version": https://www.nvidia.com/en-us/on-demand/session/gdc25-gdc1009/
9. NVIDIA GeForce News — "NVIDIA Redefines Game AI With ACE Autonomous Game Characters": https://www.nvidia.com/en-us/geforce/news/nvidia-ace-autonomous-ai-companions-pubg-naraka-bladepoint/
10. GDC Fireside Chat schedule — Damian Isla + Jeff Orkin (2024): https://schedule.gdconf.com/session/game-ai-fireside-chat-with-damian-isla-and-jeff-orkin-celebrating-20-years-of-behavior-trees-and-automated-planning-systems/917672
11. EA SEED / CoG 2023 — "Technical Challenges of Deploying RL Agents for Game Testing": https://www.ea.com/seed/news/cog23-challenges-deploying-rl-agents-game-testing
12. Ubisoft La Forge publications: https://www.ubisoft.com/en-us/studio/laforge/publications
13. Sony AI / PR Newswire — Gran Turismo Sophy global release: https://www.prnewswire.com/news-releases/sony-ai-announces-full-global-release-of-ai-driver-gran-turismo-sophy-for-gran-turismo-7-players-in-latest-update-301973930.html
14. Supergiant Games — Hades II v1.0 announcement: https://www.supergiantgames.com/blog/hades2-coming-sep25/
15. Artificial Agency launch — GlobeNewswire (Jul 2025): https://www.globenewswire.com/news-release/2025/07/10/3113377/0/en/Artificial-Agency-Launches-Behavior-Engine-to-Create-Video-Games-That-Feel-Truly-Alive.html

### Secondary sources (coverage, analysis)

16. poe-vault.com — "Rogue Exiles Are Coming to PoE2: And They Fight Like Real Players": https://www.poe-vault.com/poe2/news/rogue-exiles-are-coming-to-poe2-and-they-fight-like-real-players
17. Icy Veins — "Why Diablo 4 Is Redesigning Monsters and Defenses in Season 11": https://www.icy-veins.com/d4/news/why-diablo-4-is-redesigning-monsters-and-defenses-in-season-11/
18. Icy Veins — "Diablo 4 Season 11 Brings Major Monster Reworks": https://www.icy-veins.com/d4/news/diablo-4-season-11-brings-major-monster-reworks/
19. GTPlanet — "Gran Turismo 7's Sophy AI Project Turns Five Years Old": https://www.gtplanet.net/gran-turismo-7s-sophy-ai-project-turns-five-years-old-20260718/
20. Invisible Friends — "GDC 2026: A Personal Account": https://www.invisiblefriends.net/gdc-2026-a-personal-account/
21. InvenGlobal — "KRAFTON To Detail PUBG Ally AI Teammate at GDC": https://www.invenglobal.com/articles/20123/krafton-to-detail-pubg-ally-ai-teammate-at-gdc
22. NGOHQ — "Titan Quest II Review" (Aug 2025): https://www.ngohq.com/2025/08/05/titan-quest-ii-review/
23. ixbt.games — "Last Epoch Developers Comment on Krafton's AI Adoption Course": https://ixbt.games/en/news/2025/11/29/avtory-last-epoch-prokommentirovali-kurs-krafton-po-vnedreniiu-ii.html

### Academic / research

24. arXiv:2408.13328 — "Localized Observation Abstraction Using Piecewise Linear Spatial Decay for Reinforcement Learning in Combat Simulations" (Black, Darken; MODSIM WORLD 2024): https://arxiv.org/abs/2408.13328
25. AAAI AIIDE 2012 — "Kiting in RTS Games Using Influence Maps" (Uriarte, Ontañón): https://ojs.aaai.org/index.php/AIIDE/article/view/12544
26. arXiv:2503.09527 — "CombatVLA: An Efficient Vision-Language-Action Model for Combat Tasks in 3D Action Role-Playing Games" (Chen et al.; ICCV 2025): https://arxiv.org/html/2503.09527
27. arXiv:2606.30092 — "Hierarchical Reinforcement Learning in StarCraft Micromanagement with Influence Maps and Cluster-based Scripts" (2026): https://arxiv.org/html/2606.30092v1
28. arXiv:1703.06275 — "Evolving Game Skill-Depth using General Video Game AI Agents" (Liu et al., 2017): https://arxiv.org/abs/1703.06275
29. arXiv:2307.11105 — "Technical Challenges of Deploying RL Agents for Game Testing in AAA Games" (EA SEED, CoG 2023): https://arxiv.org/pdf/2307.11105

### Tools / ecosystem

30. LimboAI GitHub (limbonaut): https://github.com/limbonaut/limboai
31. LimboAI Godot Asset Library (4.4–4.5): https://godotengine.org/asset-library/asset/3787
32. Beehave GitHub (bitbrain): https://github.com/bitbrain/beehave
33. Utility AI GDExtension — Godot Asset Library: https://godotengine.org/asset-library/asset/2260
34. JarkkoPar/Utility_AI GitHub: https://github.com/JarkkoPar/Utility_AI
35. GDQuest Steering AI Framework GitHub: https://github.com/GDQuest/godot-steering-ai-framework
36. Godot NavigationServer 4.0 blog: https://godotengine.org/article/navigation-server-godot-4-0/
