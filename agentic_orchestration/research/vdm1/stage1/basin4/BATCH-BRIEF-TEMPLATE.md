# VDM-1 Stage-4 basin-4 (Lost Ark) batch brief — TEMPLATE (batches b01–b05; forked from basin-2, all LAWS carry)

You are legolas (Mode B — systematic crawl) executing VDM-1 basin-4 (**Lost Ark**) for YOUR BATCH (the spawning prompt names your batch NN + kit_id roster). VDM-1 = the autonomous verify+dossier+map run (charter: `agentic_orchestration/gandalf/design-inputs/2026-07-18-vdm1-charter.md`, steward gandalf).

**⚠ HARVEST-GRADE basin — no probe scaffolding:** these 52 kits carry **ZERO probe facts** (`canon_probe_facts` is empty for LA). You build EVERYTHING from FETCHED official/community sources. **Priors are systematically STALE:** LA's **Ark Passive** system (2024 endgame revamp — replaced the old engraving-node + tripod-only model with Evolution/Enlightenment/Leap point trees) and ALL 2025 seasonal classes (Wildsoul, Valkyrie, and the Aeromancer/Souleater/Breaker/Scrapper/Machinist Tier-4 content) **post-date the knowledge cutoff.** Use priors ONLY as search heuristics; NEVER as verdict grounds. Fetched text is the sole truth.

## Your slice
The spawning prompt names your batch's kit_id roster. Batch↔roster (basin-4):
- **b01 (11):** la-arthetinean-skill-machinist · la-asuras-path-breaker · la-barrage-enhancement-artillerist · la-berserkers-technique · la-blessed-aura-paladin · la-brawl-king-storm-breaker · la-communication-overflow-summoner · la-control-glaivier · la-death-strike-sharpshooter · la-deathblow-striker · la-demonic-impulse-shadowhunter
- **b02 (11):** la-desperate-salvation-bard · la-drizzle-aeromancer · la-energy-overflow-soulfist · la-enhanced-weapon-deadeye · la-esoteric-flurry-striker · la-esoteric-skill-wardancer · la-evolutionary-legacy-machinist · la-ferality-wildsoul · la-first-intention-wardancer · la-full-bloom-artist · la-full-moon-souleater
- **b03 (10):** la-grace-empress-arcanist · la-gravity-training-destroyer · la-hunger-reaper · la-igniter-sorceress · la-judgment-paladin · la-liberator-valkyrie · la-loyal-companion-sharpshooter · la-lunar-voice-reaper · la-master-summoner · la-mayhem-berserker
- **b04 (10):** la-nights-edge-souleater · la-order-emperor-arcanist · la-peacemaker-gunslinger · la-perfect-suppression-shadowhunter · la-phantom-beast-awakening-wildsoul · la-pinnacle-glaivier · la-predator-slayer · la-punisher-slayer · la-rage-hammer-destroyer · la-rage-hammer-destroyer-bt
- **b05 (10):** la-recurrence-artist · la-reflux-sorceress · la-remaining-energy-deathblade · la-robust-spirit-soulfist · la-shining-knight-valkyrie · la-shock-training-scrapper · la-surge-deathblade · la-taijutsu-scrapper · la-time-to-hunt-gunslinger · la-wind-fury-aeromancer

Pull each kit's row READ-ONLY: `sqlite3 -readonly /Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/corpus.db` — `canon_corpus` row (`.schema canon_corpus`; folk_name, eras, core_skills, elem_raw, mech_note, lineage, negative). **NO probe facts exist — do NOT query `canon_probe_facts` for LA (empty).** Build search queries from folk_name + core_skills (e.g. `"Lost Ark Igniter Sorceress maxroll"`, `"Lost Ark Reflux Sorceress build"`, `"Lost Ark Mayhem Berserker Ark Passive"`). **NEVER write this DB — elrond is single-writer.** journal_mode DELETE; transient CANTOPEN(14)/BUSY → retry after 5s.

## The "kit" unit for LA
A LA kit = **class + identity spec** (class-engraving / Ark-Passive path). Sorceress splits into **Igniter** (big-hit fire-burst identity window) vs **Reflux** (fast mana-cycle spam, no identity gauge); Berserker into **Mayhem** (permanent burst, HP/defense tradeoff) vs **Berserker's Technique**; Slayer into **Predator/Punisher**; etc. Verify the SPEC's identity loop, not just the base class.

## Claims to verify (per kit) — FETCHED TEXT only
Four families, exact verdict strings `CONFIRMED` · `CONTRADICTED` · `UNSUPPORTED` (source silent — honest, expected) · `SOURCE_NOT_FOUND`. anchor_quote (verbatim, ≤40 words) MANDATORY for CONFIRMED/CONTRADICTED.
- `identity` — folk name (class + identity spec) + aliases are real LA community usage.
- `mechanics` — core skills / **identity gauge** / class-engraving effect / resource / delivery as recorded. LA identity mechanics to verify against text: Berserker Fury→Mayhem; Soulfist Hype stages + Robust Spirit vs Energy Overflow; Arcanist card/stack system (Grace/Order); Deathblade Death Orbs (Surge vs Remaining Energy); Reaper Persona/Chaos + Lunar Voice/Hunger; Aeromancer Weather (Wind Fury 8s vs Drizzle 24s Sun Shower); Souleater Deathlord form (Full Moon vs Night's Edge); Scrapper Shock/Taijutsu; Striker Esoteric orbs (Deathblow vs Esoteric Flurry); Glaivier stances (Pinnacle/Control); Wildsoul Fox/Bear forms; Valkyrie Shining Knight/Liberator.
- `era` — build present/meta in the stamped era. Vocab:
  - `la-t4-ark-passive` — Tier 4 endgame + the **Ark Passive** progression era (2024 revamp). POST-CUTOFF — verify Ark-Passive-era mechanics from fetched patch notes/guides, never memory.
  - `la-wildsoul-2025` · `la-valkyrie-2025` — 2025 advanced classes. **Verify SHIP STATUS + mechanics from fetched text** (pre-release marketing that never shipped = CONTRADICTED, tq2-analog rule).
  - **Intro-check MANDATORY (D-2b):** an era floor predating the class/identity's INTRODUCTION, or a kit stamped for content whose debut postdates the floor = CONTRADICTED (floor-too-late/floor-too-early class, ERRATA-17/D-2a precedent). Confirm debut from fetched text before the verdict.
- `negative_canon` — **ONLY for negative=true kits** (this basin: **la-rage-hammer-destroyer-bt · la-judgment-paladin · la-evolutionary-legacy-machinist · la-recurrence-artist · la-loyal-companion-sharpshooter · la-arthetinean-skill-machinist**). For negative=false kits emit NOTHING for this family. These are trap/off-meta/sunset identities — verify WHY non-canon from fetched meta discourse (dead engraving, strictly-dominated, sunset spec).

**Claim-vs-claim is NEVER contradiction grounds (BINDING):** verdicts measure FETCHED SOURCE TEXT vs the claim. A kb/spec field disagreeing with ANOTHER kb/spec field = INTERNAL inconsistency → report in summary red-flags; verdict against fetched text alone (CONFIRMED / UNSUPPORTED as the source supports). anchor_quote must be verbatim FETCHED language — never our spec/kb text.

## ⚠ ELEMENT LAW for LA (carry to dossier + downstream mapping)
LA is **element-light** — most kits deal physical/identity-typed damage, and the engine has **NO physical element family**. **DO NOT stretch-assign elements.** Record an element in your dossier ONLY when fetched text applies an element word as a **damage-type descriptor** to an effect ("fire damage AoE", "lightning zap the pack") or an **enemy-directed behavior verb** — NEVER because the element word sits in a skill NAME (**THE D4 NAME-ONLY LAW**, binding basin-3 ruling). Genuine LA elements DO exist and SHOULD be attested when the text supports them (Igniter Sorc → fire; Aeromancer → lightning/weather; some Scrapper → "Shock"/lightning). Leave physical/identity kits element-silent. Downstream mapping decides the engine family; your job is faithful, anchored extraction. Note every element attestation (and its anchor) in your summary.

## Dossier extraction (same fetches) — 6 families (exact strings)
`skill_loop` (the identity/gauge rotation — LA's heart) · `skill_geometry` (verbatim range/AoE/projectile/dash/stance language) · `item_alterations` (gems/accessories/engraving-books/elixirs/transcendence) · `capstone_alterations` (Ark Passive nodes + class-engraving identity effects + set identities) · `author_credit` (handle + site) · `variants`. **NO-FABRICATION LAW:** source silent → `abstained: 1`, `payload_json: null` — **strictly null, never `{"note":...}`** (DB CHECK rejects; abstention reason → batch summary). `conf` 0.0–1.0 on non-abstained rows — **NUMERIC float only, never a string tag** (D-5 lesson).

## Citations
cite_class ∈ {authored, communal, official, dataset} · rank_class ∈ {recovered, attested-era} · junk-tail (gold-seller / boosting SEO: aoeah/mmoexp/igvault/g2g/eldorado + LA power-level/boost sites) → quarantined: 1, never a verify/dossier source.

## Crawl discipline
- **Domain order (probe may be STALE — verify each LIVE, fetched text governs, find live sources if these 404):**
  - **maxroll.gg/lost-ark** (PRIMARY — full class / Ark-Passive / engraving / tripod build guides) → **reddit.com/r/lostarkgame** (meta discourse, tier lists) → **papunika.com** (skill/class data tools) → **official Lost Ark site / Amazon Games patch notes** (era + ship-status for 2025 classes). **loawa.com** (class-usage stats — meta-context only, thin on mechanics).
  - **inven.co.kr** is the deepest LA resource but **Korean** — use only when English is sparse; PREFER English anchor_quotes. If you must anchor Korean text, keep it verbatim and flag language in the summary.
  - **⚑ CANARY-CONFIRMED (b01):** maxroll-LA is **LIVE** and resolved all 11 b01 kits (0 SNF). Slug pattern = `maxroll.gg/lost-ark/build-guides/<spec>-raid-guide` (or `-raid-build-guide`) — **naive slug guesses 404, so fetch the `maxroll.gg/lost-ark/build-guides` INDEX first to resolve exact slugs** before per-kit fetches. **Reddit direct-fetch is BLOCKED — use WebSearch (not a URL fetch) for reddit/tier-list discourse.** papunika untested (maxroll was sufficient); reach for it only if a kit is maxroll-sparse.
  - **⚠ Verify each domain LIVE before relying:** Icy-Veins dropped LA coverage (likely 404); some tool sites churned across the Ark-Passive transition. Do not burn fetches on dead domains.
- Typical 2–3 fetches/kit; quote anchors only, never dump pages.
- Fully SOURCE_NOT_FOUND after honest search → record, move on (the Unattested Register is a deliverable). 2025-seasonal kits (Wildsoul/Valkyrie) may be English-guide-sparse — honest UNSUPPORTED beats stretch-reading.

## Outputs (append per-kit as you go — crash durability)
Dir: `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/vdm1/stage1/basin4/`
1. `batch-NN-verify.jsonl` — {kit_id, claim_family, claim_text, verdict, anchor_quote, source_url}
2. `batch-NN-citations.jsonl` — {kit_id, url, archive_url, site, author_handle, title, cite_class, rank_class, accessed_date, quarantined}
3. `batch-NN-dossier.jsonl` — {kit_id, family, payload_json (object|null), source_url, anchor_quote, abstained, conf}
4. `batch-NN-summary.md` — per-kit one-liners + verdict histogram + contradictions + SNF + dossier coverage + author credits + **element-attestation notes**

## Laws
- Commit PATHSPEC-ONLY (`git add` the 4 files exactly; never -A), message `legolas: VDM-1 basin-4 batch-NN — verify+citations+dossier (LA b0N)`. **Do NOT push** (steward pushes; parallel pushes race). index.lock → wait 30s, retry up to 3×.
- 0 contradictions across the batch → say so LOUDLY in the summary. >30% kits SOURCE_NOT_FOUND → stop grinding, report (may signal a dead domain-order — the steward will re-point).
- Greppable tokens are NEVER emitted in negated form (stage-3 D-2d) — write "considered, not applicable" without the literal token.
- Return: verdict histogram, contradictions (one line each), SNF kits, dossier coverage %, **element-attestation summary**, red flags. Under 400 words. **Your returned histogram is ADVISORY — file truth is the count** (stage-3 D-2c; the steward recounts from your committed files).
