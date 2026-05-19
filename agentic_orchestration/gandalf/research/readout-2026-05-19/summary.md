# Reincarnated Mod-Target Analytical Readout — Executive Summary

**Status:** v4 — 2026-05-19 morning. Six riders returned. **R6 — Host-Calibration Protocol — added** after Matt push-back exposed a flaw in the original "R3 OPTIONAL for Path B" claim (see § 4.5). **Modding-economics rider empirically resolves Matt's class-only-vs-world-content question** (see § 5.5) — with a discipline correction on the $5K–$50K-per-pack number that I authored as a "rough estimate" in the original Apex debrief and then propagated as if it had come from the Director. Empirical numbers are MUCH lower (Calamity ceiling ~$30K/year). Companion artifact: `readout.html` (visualized charts).

---

## § 0.5 — Discipline correction note (drift acknowledged)

The `apex-director-debrief-2026-05-18.md` § 1.3 I authored yesterday contains my own synthesis-time estimate *"~$5K–$50K-ish ceiling per mod-pack"* — clearly labeled "rough" in that doc, but I subsequently propagated it as if it represented the Director's framing. **The Director did not state this number.** His actual debrief said *"money can be made from mod packet sales"* with no dollar range. Empirical data from rider 6 now shows the real numbers are much smaller (top Patreon at maximum-scope Terraria TC = $2,552/month = ~$30K/year; class-only ARPG mods = $0 monetization). This correction matters substantively because the framing of Path B as a revenue play vs. credibility play depends materially on this number. Going forward: numbers I make up at synthesis time must be tagged as my estimate every time I cite them downstream — not lifted into the next layer as if they were sourced.

**Companion data files** (`data/` directory, Excel-importable):
- `scoring-matrix.csv` — 16-candidate MFS ranking, flat
- `axis-detail-long.csv` — per-(host, axis) long-form for charting
- `reincarnated-engine-kpis.csv` — producer profile + schema gaps
- `sequencing-plan.csv` — week-by-week phased plan

---

## § 0 — The headline in one paragraph

The data recommends **Path B mod-first (Phase 1 Grim Dawn → Phase 2 Titan Quest AE OR Torchlight 2, ~14 weeks total) with Path C kept warm-parallel**. Path A is preserved at portfolio-demo scope (not retired). The Director's strongest leaning (mod-first then engine sale) is preserved; his target ordering is corrected — **Wolcen is dead (MFS 1.65, end-of-life)**; Grim Dawn is the only PRIMARY-tier host (MFS 4.05). The Crate-lineage "killer pairing" (GD + TQAE) has a permission-axis crack the original scoring missed — **THQ Nordic's EULA contains an IP-assignment clause that vests ownership of Reincarnated-generated content in THQ Nordic GmbH on publication**. This does not kill Phase 2 TQAE, but it changes what Phase 2 *is*: viable as technical-credibility-only, not viable for monetization or portfolio licensing without written agreement that does not currently exist for any modder we found. **The Q5 family-partnership question is Matt's alone to weigh** and gates whether the recommendation stands or shifts to Path A-prime.

---

## § 1 — The four findings the data is telling us

1. **Grim Dawn is the only PRIMARY-tier mod-target.** MFS 4.05. No other host clears 4.0. The pipeline-accessibility (5/5) and schema-compatibility (4/5) axes carry it. Gap to next-best is 0.525 — meaningful, not noise.

2. **The Director's three named recommendations are technically inverted.** Correct ordering by MFS: Grim Dawn 4.05 > Dragon's Dogma 2 2.50 > Wolcen 1.65 (DROPPED — end-of-life since 2023, MP shut down Sept 2024, ~24 avg concurrent May 2026). His commercial intuition (mod-first) was right; his target ranking was inverted.

3. **The Crate-Iron-Lore lineage produces an engineering-leverage pairing** (Grim Dawn + Titan Quest AE) the Director didn't surface. Shared mastery-system DNA + established TQ→GD cross-port community practice means Phase 2 TQAE adapter costs ~+25% incremental on Phase 1 work. **Caveat: Wave-2A tempered audience reach** (TQAE ~742 avg concurrent May 2026) and **rider returns added a permission-axis poison pill** (THQ Nordic IP-assignment clause) that affects monetization not engineering.

4. **R3 schema migration is OPTIONAL for Path B; R6 host-calibration protocol is NOT.** *Corrected after Matt push-back (see § 4.5 below).* Host games absorb spatial substrate, AI behavior, range, aggro/leash **at runtime** — but the engine's balance loop converges against the 1D PackProxy gauntlet **at generation time**. A class engine-rated "balanced" at WR 50% has been tuned against a combat model that does not exist in Grim Dawn. Path B does not route around the fight-integrity gap; it restates the gap as a host-calibration problem. The per-path cost-spread (corrected):
   - Path A standalone: ~9–15 dev-weeks of Track F
   - Path B mod-first: ~5–8 dev-weeks per host (R1 + R3-subset + R6 host-calibration protocol)
   - Path C engine-as-tool: bimodal ~3–5 or ~9–15 depending on buyer substrate

---

## § 2 — Strategic context — the Apex Director's reframe

From the 2026-05-18 Zoom debrief (`canonical/story/apex-director-debrief-2026-05-18.md`):

> *"Rather than using the engine to create iterative seasonal worlds, he would want to cement a season for a time period (3/6/9/12 months) and generate copious playable assets from it through countless simulations of the same season. He would then plan his entire seasonal strategy upon the pre-generated assets and stories. He would create decision trees and use them to pre-plan for new content launch cycles and for player feedback scenarios with assets and stories ready to be deployed as the timeline of the seasonal journey unfolds."*

The Director's load-bearing insight separates two axes Reincarnated had been collapsing: **player-facing season cadence** (currently weekly) from **studio-facing asset-generation depth** (thousands of variants pre-built within one cemented thematic frame). His strongest leaning: **mod-first into Wolcen / Grim Dawn / Dragon's Dogma → engine sale to host studio as strategic prize**. The MFS analysis preserves the leaning, inverts the target ordering, adds the Crate-lineage pairing, and surfaces an IP-clause complication the Director's commercial-visibility framing did not see.

**Three commercial paths in option space** (Apex debrief § 2):
- **Path A — standalone Reincarnated-the-game:** viable with effort; cadence-uncertain at AAA scale (Director's read); doesn't capitalize on cross-genre engine value
- **Path B — mod-first PoC (Director's strongest leaning):** validates engine in real studios' games; builds case for engine acquisition; the path uniquely advantaged by the fight-integrity gap
- **Path C — engine-as-tool / B2B SaaS:** highest valuation in Director's read; cement-deep-season → asset-bank → decision-tree model; closer to engine's existing capability than initially priced

---

## § 3 — Rider returns (4 of 5)

The scoring matrix knew **can you author** (pipeline accessibility) and **does your schema map** (schema compatibility) — but it did not capture **are you permitted to author**, **who owns what you make**, **can you charge for it**, and **what type of mods does each community make**. Four riders returned with per-host modding-scope briefs:

### 3.1 — Grim Dawn (`2026-05-19-modding-scope-grim-dawn.md`)

- **EULA:** No published mod EULA. Tools page invites mods; no prohibitions stated. Wide modder tolerance documented.
- **Monetization:** **UNKNOWN / UNPUBLISHED.** Zero precedent for paid or Patreon-gated GD mods. **Material Pattern-B gap.**
- **Modifiable:** Mastery slots (slot-additive up to ~30 engine cap), all combat .dbr parameters, full world/quest/dialogue, UI textures, custom 3D models / textures / animations / sound.
- **Locked:** Core AI logic, native shaders, damage formula arithmetic. Lua API undocumented (reverse-engineer only).
- **Risk:** v1.2 Dec 2024 broke mods via `gameengine.dbr`. v1.3.0 + Fangs of Asterkarn (H1 2026) likely repeats. No Steam Workshop. **Reign of Terror TC is tolerated, NOT licensed** by Crate or Blizzard.
- **Action item:** **Pre-Phase-1 outreach to Crate** (Medierra / Zantai are public forum dev presences) on commercial mod stance.

### 3.2 — Titan Quest AE (`2026-05-19-modding-scope-titan-quest-ae.md`)

- **EULA: HARSH.** Sweeping IP-assignment clause that **technically vests ownership of Reincarnated-generated content in THQ Nordic GmbH** if published as a TQAE mod. Commercial distribution requires "prior written consent." No Verified Creators program. No indie-tolerance carve-out documented for any current modder.
- **Modifiable:** Masteries fully replaceable, AI parameters via DBR, full world/quest authoring.
- **Locked:** **Core damage formula compiled-in (NOT DBR-accessible).** 3D mesh toolchain never released. UI partially hardcoded. **Affix system cannot be bypassed** — Reincarnated's inline `rolled_effects` must translate into LootRandomizer library entries.
- **Risk:** **Atlantis update historically broke ALL existing mods** (ARC format + MapCompiler path shift). Legion of Champions hard-requires Eternal Embers. Patch stability unguaranteed.
- **Verdict:** **The IP-assignment clause is the dominant Pattern-B signal from rider returns.** Phase 2 viable as credibility-only (we don't monetize TQAE content separately); not viable for paid mods or portfolio licensing without written agreement.

### 3.3 — Torchlight 2 (`2026-05-19-modding-scope-torchlight-2.md`)

- **IP chain:** Runic → Perfect World → Gearbox Publishing SF → **Arc Games (April 2024, Embracer Group)**. NOT Echtra Games (which only made TL3/Frontiers). Runic ToU §6.4 prohibits commercial mod exploitation; remains operative; no successor entity has modified it.
- **Monetization:** Prohibited by ToU, practically unenforced. Patreon gray zone, no precedent.
- **Modifiable:** Classes, skills, combat balance parameters (DAT plain-text), UI layout, custom 3D models (Ogre mesh / 3DSMax plugins), textures / animations / sound (no official audio pipeline tool).
- **Locked:** Combat formula functions = compiled C++. Procedural dungeon assembly = compiled C++. AI = data-parameterized but primitive.
- **Risk:** **IP-orphan state is real.** SynergiesMOD has dual permission problem (Salan unreachable + ToU layer). Engine frozen since 2017 = stable but stagnant. Risk is IP abandonment, not hostile interference.
- **Verdict:** Promotable from Phase 3 to Phase 2 candidate **if TQAE IP-assignment clause is deemed disqualifying**. Lower active IP risk; broader audience (TL2 community lighter but cleaner permission).

### 3.4 — Terraria / tModLoader (`2026-05-19-modding-scope-terraria-tmodloader.md`)

- **EULA: Strongest posture in the corpus.** Re-Logic hired tModLoader devs onto payroll (jopojelly May 2024). tModLoader free Steam DLC. MIT license. Patreon-supported free mods (Calamity) tolerated. Direct paid mods prohibited.
- **Modifiable:** Full DamageClass injection, ModNPC/ModItem/ModProjectile C# API, full custom world generation, full UI replacement.
- **Locked:** No runtime JSON path — content compile-time C#. **Workaround documented and viable**: kRPG pre-allocated-slot pattern + ModConfig.ServerSide JSON auto-sync. CI pipeline (Reincarnated JSON → C# transpiler → GitHub Actions → Workshop) technically constructible.
- **Risk:** **Patch fragility is the active risk.** Terraria 1.4.5 launched late 2024; tModLoader compat still in progress as of May 2026 (1.4.4 took 9 months historically). Any Reincarnated season mod tied to 1.4.4-stable branch indefinitely.
- **Verdict:** Phase 3 Option B remains viable; **1.4.5 compat lag tempers urgency**; revisit when tModLoader 1.4.5 stabilizes.

---

## § 4 — What the rider returns change about the recommendation

### 4.1 — The "killer pairing" has a permission crack

The Crate-lineage pairing (GD + TQAE) relied on the assumption that ~+25% incremental engineering buys ~2× audience-plus-credibility. **The engineering case still holds.** The commercial case now has a poison-pill axis: THQ Nordic's IP-assignment clause could claim ownership of Reincarnated content published as TQAE mods. This changes Phase 2's role from "validate revenue + credibility" to **credibility-only**, or alternatively, swaps Phase 2 from TQAE to Torchlight 2.

### 4.2 — The pre-Phase-1 outreach action item

Before Phase 1 ships any commercial Grim Dawn content, **Matt should contact Crate directly** on monetization stance. Medierra and Zantai are public dev presences on the Crate forum. A direct ask + recorded response is the action that resolves the UNKNOWN/UNPUBLISHED status. This is not a Pattern-B blocker — the technical work can begin under "free mod" assumption — but it's a real action item the data surfaced.

### 4.5 — R6 Host-Calibration Protocol (correction from Matt push-back)

**Matt's challenge:** *"Although these two host games will manage the spatial substrate, AI behavior, range mechanics, and aggro/leash defaults, how will we provide balanced classes through the engine without converging on those via use of said mechanics at generative/sim time?"*

**Acknowledged: the original "R3 OPTIONAL" claim conflated runtime substrate (host game absorbs) with generation-time balance convergence (engine still has to converge against *something*).** The engine's balance loop currently tunes classes against the 1D PackProxy gauntlet — a combat model that does not exist in Grim Dawn. Classes shipped to GD without calibration would manifest the same fight-integrity gap the demo shows today, just on a different surface. The host game doesn't make our balance true; it exposes the same wrongness in a new place.

**Five viable approaches** to closing the calibration gap, in order of cost:

| Option | Approach | Engineering cost |
|---|---|---|
| **A** | Host-specific balance harness — approximate GD's combat math + 2D dynamics in Python so balance loop converges against GD-shaped fights | **5–8 wk per host** (most accurate, most expensive) |
| **B** | Headless host-game test harness — automated combat scenarios in GD itself, telemetry back to balance loop | 3–5 wk IF GD permits headless automation; indefinite if not |
| **C** | **Reincarnated-class → host-class analog mapping** — declare target GD-class equivalent per Reincarnated class (fire wizard → Demolitionist, shadow controller → Necromancer); tune to known balance parameters via extended `balance_metadata` schema | **2–3 wk for protocol; reusable across seasons + Crate-lineage hosts** |
| **D** | Hybrid — keep 1D gauntlet for damage ballpark + per-host translation table mapping our DPS curves to GD's hit/dodge/crit reality | 2–3 wk per host |
| **E** | Curator-in-the-loop — engine produces directional candidate pool; human curator (Matt + Crate-forum modder partner) plays through and picks winners | ~0 engineering up-front; 1–2 wk curator time per season |

**Recommended: Option C as the load-bearing engineering work; Option E as the deployment safety net during Phase 1.** Option C is what every successful GD content mod (Dawn of Masteries, Reign of Terror) does by hand — we automate it. Our LLM-generation + structured balance metadata makes this automatable in a way hand-modders cannot match. **This is the actual Path-B engineering advantage that Reincarnated uniquely owns.**

**Workstream R6 — Host-Calibration Protocol** is added to the sequencing plan alongside R1–R5 in the Track F list. Sized at 2–3 wk for protocol authoring; reusable across Crate-lineage hosts (GD + TQAE + TL2) with ~+2-3 wk delta per additional host. Total Phase 1 estimate updates from 6–9 wk to **9–12 wk** to include R6.

**The fight-integrity gap diagnosis is now stronger, not weaker.** The gap was named as "engine balances the wrong game vs. demo." The correction restates it as *"engine balances the wrong game vs. ANY runtime that isn't the 1D gauntlet itself"* — including all three Path-B host candidates. This will be reflected in a canonical-doc amendment after Pattern-B closes.

### 4.6 — The revised pairing question

| Pairing | Engineering cost | Audience | Permission risk |
|---|---|---|---|
| **GD + TQAE** (original) | ~+25% incremental | Modest (~2×) | **IP-assignment clause active on Phase 2** |
| **GD + TL2** (revised) | ~+50–60% incremental (different DBR/DAT schemas) | Broader audience surface (TL2 community lighter but cleaner permission) | No active IP-assignment risk |

The revised pairing is meaningful Pattern-B deliberation. The Mount Doom rider may surface a third pairing candidate (post-training-cutoff games with permission postures we don't yet know).

---

## § 5 — Sequencing — the data's recommended Pattern-B answer (v3 with R6)

```
Week 0:    Pattern-B direction commit (Matt) — Path B + Path C warm-parallel
                + pre-Phase-1 Crate outreach on monetization stance
Week 1-2:  Phase 0 — R1 per-tier balance targets (gamora)
                + class-retuning sprint fires in parallel
Week 3-5:  Phase 0b — R3-subset schema migration (rocket + star-lord + elrond)
                per-skill range + geometry params + AI behavior fields
                backfill across 5 shipped seasons
                IN PARALLEL: Phase 0c — R6 host-calibration protocol (rocket + gamora)
                Reincarnated-class → GD-class analog mapping
                balance_metadata schema extension
                balance loop convergence targeting host-class parameters
Week 6-11: Phase 1 — Grim Dawn DBR exporter + first single-class mod ship
                (rocket + star-lord)
                Classes calibrated to GD-class analogs per R6
                Crate-forum modder community feedback loop
                LEGOLAS parallel: scout Path C buyer profiles
                                + Last Epoch Paradox Classes commercial data
Week 12-14: Phase 2 — TQAE ARC adapter OR TL2 GUTS/DAT adapter
                (Matt decision gated on TQAE IP-assignment resolution)
                R6 calibration absorbs second host with ~+2-3 wk delta
                STAR-LORD parallel: spec Path C operational layer
Week 15+:  Phase 3 — Reception evaluation gates trinity-completion
                OR Terraria pivot OR Path C transition
```

**Total Track-F engineering: ~14 weeks to two-mod-host viability** (Phase 1 estimate ~9-12 wk including R6; Phase 2 adds ~+2-3 wk leveraging R6 reuse across Crate-lineage hosts). This is still significantly less than Path A's 9–15 weeks of full Track F + class-retuning sprint. The Path-C operational layer prototype emerges as a side-effect of the export pipeline.

**Cost-spread correction:** the original "~14 weeks total" was right; the per-path-cost framing of "~3-5 wk Path B vs ~9-15 wk Path A" was wrong because it omitted R6. The corrected spread is "~5-8 wk per host for Path B vs ~9-15 wk for Path A" — Path B still cheaper, less than the inflated original claim suggested.

---

## § 5 — Mount Doom rider returns — new releases + modding-purpose taxonomy

### 5.1 — New releases 2024–2026 (Job 1)

**No 2024–2026 new release challenges Grim Dawn for PRIMARY tier.** Three findings reshape the future:

| Candidate | Verdict | Why it matters |
|---|---|---|
| **Titan Quest II** (EA Aug 2025, THQ Nordic / UE5) | Watch / MFS ~2.75. Official modding tools "under internal discussion" — not confirmed. Recheck at 1.0 (~late 2026). | The TQAE adapter (Phase 2) would likely be **partially reusable** for TQ2 (~70-80%) if THQ Nordic ships official tools. Assuming IP-assignment clause carries forward, TQ2 = Phase 4 future option. **This is a real reason to retain Phase 2 = TQAE even with IP-clause caveat — it future-proofs into TQ2 ground.** |
| **Last Epoch** (Eleventh Hour, 1.0 Feb 2024) | Closed pipeline (no official modding tools; MelonLoader offline-only). Developer monetizing class expansion as paid DLC ("Paradox Classes"). | **Critical Path-C market-validation context:** Eleventh Hour is doing exactly what Reincarnated would do — paid class-pack DLC on their own engine. They are the closest commercial analog. Reverse-engineer their pricing, sales cadence, reception. **Recommend Legolas Mode A pass on Paradox Classes data when Pattern-B Q1 commits direction.** |
| **STALKER 2** (Nov 2024, GSC / UE5) | NotViable (FPS survival genre) but capable Zone Kit SDK + Mod.io + Workshop | Demonstrates UE5 modding is real and shippable as official SDKs. Useful precedent for what TQ2's tools might look like. |
| **PoE 2 / D4 / Avowed / Hades II / Wartales / Throne and Liberty / Eternal Strands / Tainted Grail / NRftW / Elden Ring Nightreign** | NotViable for various structural reasons | Most prohibit modding outright (PoE2, D4) or have wrong genre loop. EA limbo (NRftW). Mobile ARPGs uniformly closed. **None of them shifts the recommendation.** |

### 5.2 — Per-host modding-purpose taxonomy (Job 2)

**THE FIRST-MOVER SIGNAL:** Procedural/generative modding is **universally absent** across all 8 surveyed host communities. No host community currently has a normalized pattern of "procedurally-generated content packs flowing in from external tools." **Reincarnated's use case would be genuinely novel everywhere.** This is the first-to-narrative opportunity Legolas's pre-meeting research flagged, now confirmed empirically.

| Receptivity | Hosts | Why |
|---|---|---|
| **Most receptive** | Grim Dawn, Torchlight 2 | Both treat large external class/mastery drops as first-class content (Dawn of Masteries 53-port; Classes Reborn 40+ classes). *"A new mastery this season"* is intelligible vocabulary. **TL2 has native procedural-generation DNA** (dungeon randomizer) priming the conceptual model. |
| **Moderately receptive** | Terraria, Minecraft | High tolerance for novel systems. Terraria blocker = operational (compile-time C#, 1.4.5 compat lag). Minecraft blocker = voxel genre conversion. |
| **Dark-horse** | V Rising | Server-operator community already thinks **"what do I deploy this season?"** — culturally prepared for seasonal content-pack framing. Small audience (MFS 2.40 stands), but the mental model is uniquely aligned. Worth Path-C-adjacent revisit. |
| **Unreceptive** | BG3, Elden Ring | BG3 = cosmetic-first / narrative-immersion. Elden Ring = curated handcrafted content as **core community identity**; procedural generation is antithetical to FromSoftware ethos. *Cultural fit is weak regardless of MFS.* |

### 5.3 — What Mount Doom changes about the pairing recommendation

**The cultural-receptivity finding strengthens the GD+TL2 revised pairing over GD+TQAE.** Both Crate-lineage hosts share schema DNA, but TL2 ranks in the most-receptive cultural tier alongside GD, while TQAE does not.

| Pairing | Engineering | Audience | Permission | Cultural fit | Net signal |
|---|---|---|---|---|---|
| **GD + TQAE** (original) | ~+25% incremental | Modest (~2×) | IP-assignment risk | Mixed (GD strong, TQAE smaller/conservative) | Engineering-optimized |
| **GD + TL2** (revised, recommended) | ~+50–60% incremental | Broader, lighter | IP-orphan but no active risk | **Both in most-receptive tier**; TL2 has native procedural DNA | **Culture- and permission-optimized** |
| **GD + V Rising** (dark horse Path-C adjacent) | ~+80% incremental | Modest | BepInEx tolerated | Server-operator "deploy this season" mental model = unique Path-C buyer narrative | Path-C strategic play |

---

## § 5.5 — Modding-economics rider returns (Matt's class-only-vs-world-content question, empirically resolved)

### Your question, the empirical answer

> *"Is class-only with seasonal cohesion + new loot + skill trees + VFX/SFX enough, or do we need maps/quests/NPCs?"*

**The community accepts class-only as complete. The constraint is not perceived value but mod-culture norms on paid content.** Direct empirical proof:

| Mod | Scope (no new world content) | Community treatment |
|---|---|---|
| **Dawn of Masteries** (GD) | 53 classes, no maps/quests/NPCs | *"Can't play vanilla anymore"* — top-recommended; treated as definitive GD experience |
| **Grimarillion** (GD) | Masteries from TQ + D3 | *"Most stable class-expansion option"* — actively maintained through GD 1.2 |
| **SynergiesMOD** (TL2) | 4 new classes + endgame dungeons | **661,700 Steam Workshop subscribers** — 5-star, 12,795 ratings, 972,070 unique visitors |
| **Soulvizier** (TQAE) | Mastery + loot depth, no new world | *"Ten thousand times better with Soulvizier"* — treated as complete |

**The GD community's definition of "complete":** all skills functional, all items have loot entries, maintained for current game version. **New maps are not in the definition.** Reincarnated's class + skill tree + seasonal cohesion + new loot scope matches this completely.

### Revenue picture — concrete empirical numbers (replacing my $5K-$50K drift)

| Mod | Host | Scope | Patron count | Monthly revenue |
|---|---|---|---|---|
| Calamity Mod Team | Terraria | Class + biomes + bosses + lore (max scope) | 2,669 | **$2,552/month** (~$30K/year) |
| Vault Hunters | Minecraft | Full modpack | 1,868 | $2,455/month |
| Median XL | Diablo 2 | Full overhaul + server costs | 693 | starting $1/month |
| **Dawn of Masteries** | Grim Dawn | 53 classes | **None** | **$0** |
| **Reign of Terror** | Grim Dawn | Full D2 TC | **None — explicitly refused donations** | **$0** |
| **Grimarillion** | Grim Dawn | Mastery compilation | **None** | **$0** |
| **SynergiesMOD** | Torchlight 2 | 4 classes + endgame | **None** | **$0** |
| **Soulvizier** | TQAE | Mastery depth | **None** | **$0** |

**Nexus Donation Points pool:** ~$325K/month distributed across all opted-in mods on the entire platform. A top GD mod earns "a few hundred dollars/month at most" — supplemental, not a business model.

**Patreon ceiling at MAXIMUM scope (Calamity):** $2,552/month with 9.18M Workshop subscribers (0.03% conversion rate). This is the entire category's revenue ceiling.

### The critical reframe — constraint is mod-culture, not scope

> *"Not a single ARPG class mod charges for its content. All are free. Reign of Terror (full D2 reimplementation in GD) explicitly refuses donations on principle. The constraint is not perceived value but host-platform culture. Attempting to charge $5 for a GD mastery pack would be a culture break, not just a pricing decision."*

**This is the finding that genuinely re-prices Path B's commercial framing:**

- Path B mod-revenue is essentially zero. Patreon at $0–$30K/year ceiling. The mod itself does not pay.
- **Path B is a credibility play, not a revenue play.**
- The Director's commercial reasoning is validated more strongly: *engine sale is the strategic prize.* Mod-sales noise compared to engine acquisition (mid-six to low-seven figures plausible).
- **Path B = years of credibility-building that earns the engine-sale conversation.**

### The Enderal alternative — standalone product path (new option in space)

The rider surfaced a path Pattern-B did not explicitly name:

> *"Enderal (Skyrim TC) went on Steam as a free standalone. A Reincarnated class pack as a paid standalone on itch.io or Steam is a different question than 'paid Grim Dawn mod.'"*

**Path B-as-standalone-product:** use host-mod credibility to launch Reincarnated as a paid Steam/itch.io standalone at indie pricing ($5–$20). Bypasses mod-platform cultural-no-paid-mods constraint. **This is Path A in standalone-product clothing**, riding on Path B's credibility ladder:

1. **Phase 1–2 (free mods in GD/TL2):** build community credibility + Dawn-of-Masteries-tier reception
2. **Phase 2.5 (standalone product launch):** ship Reincarnated-as-paid-standalone using credentialed reception
3. **Phase 3 (continue):** engine sale path OR sustain standalone product

**This re-opens Pattern-B Q3** (Reincarnated-the-game disposition). Reincarnated doesn't retire and doesn't become only-a-mod. It becomes **the credentialed-standalone-after-mod-ladder**. The playtest partnership with Matt's son survives intact.

### Project Diablo 2 — seasonal model precedent

PD2 runs 4-month seasonal ladders with themed content drops (Season 13 = "Betrayal," April 2026 launch). Strong engagement; entirely free. **Validates Reincarnated's seasonal-cohesion framing as community-intelligible** — but does not yet monetize. *No precedent for LLM-generated/procedural seasonal content as a subscription service exists.* Reincarnated would be defining the category.

### Open questions surfaced by rider 6 (worth your direct attention)

1. **Crate Entertainment's explicit policy on paid mods for GD** — not in public documentation. **Action item: direct inquiry to Crate forum (Medierra / Zantai) to clarify whether paid standalone distribution on itch.io / Steam is contractually prohibited under the modder's de-facto agreement.** This is the same outreach already in the action-item list (pre-Phase-1); the question can be combined.
2. **GGMods (launched Jan 7, 2026)** — first platform offering salaried contracts for modders. Supports Skyrim, BG3, Fallout 4 currently. *Worth tracking as a structural change in mod monetization.* Does not yet cover GD/TL2/TQAE.
3. **Whether LLM-generated/procedural seasonal content as a subscription service has precedent** — none found. Would be novel.

---

## § 6 — Open gaps after all riders return

### Gap 1 — Crate monetization stance (action item, not research)
Matt must contact Crate directly. Public forum DM to Medierra / Zantai. ~1-2 week response window. **Pre-Phase-1 dependency.**

### Gap 2 — Last Epoch Paradox Classes commercial data (Legolas commission, post-Pattern-B)
Eleventh Hour's paid class-pack DLC on their own engine is the closest commercial analog to Path-C. **Recommend Legolas Mode A pass on Paradox Classes pricing / sales cadence / community reception** when Pattern-B Q1 commits direction. This is the buyer-side market-validation data Pattern-B Q4 has been waiting for.

### Gap 3 — Path C buyer-profile validation (Legolas commission queued)
Pattern-B Q4 needs concrete buyer profiles for the "cement-deep-season → live-ops tool" framing. **Recommended:** commission Legolas Mode A scout on Director of Live Operations / Creative Director / Production Director buyer personas at live-service shops, plus auto-battler/idle/strategic-layer studios as alternate buyer profiles. Fires after Pattern-B direction commit.

### Gap 4 — Titan Quest II watch (recheck late 2026)
THQ Nordic / UE5. Official modding tools "under internal discussion" — not confirmed. Recheck at 1.0 (~late 2026). If tools ship and IP-assignment clause carries forward, treat as Phase 4 (TQAE adapter reusable ~70-80%).

---

## § 7 — Additional context (per Matt directive — beyond what the data says)

### 7.1 — The fight-integrity gap is the structural reason Path B is correct

The Director's reasoning for Path B was commercial — mod sales build the case for engine acquisition. The fight-integrity gap analysis (Gandalf 2026-05-18, `engine-vs-demo-fight-integrity-gap-2026-05-18.md`) adds an architectural reason that compounds: **Path B is the only path where the host game absorbs our hardest unsolved problem (spatial substrate) for free.** Path A pays the ~9–15 dev-week tax. Path C pays bimodally. Path B alone gets spatial substrate as a free dependency. When the engineering case and the commercial case point the same direction, that's rare enough to take seriously.

### 7.2 — The Director's cement-deep-season is closer to Path-C-MVP than originally priced

The engine already generates variants within a thematic frame (every season regen is exactly this — we just don't *bank* them deliberately). Banking is mostly persistence + tagging (weeks not months). The decision-tree authoring tool is genuine new surface (4–8 weeks). **Minimum-viable Path C may be ~6–10 weeks, not 3–6 months** originally priced. Enterprise-grade Path C is still the bigger number, but only relevant after a buyer says yes.

### 7.3 — The Q5 dimension the data cannot resolve

Path B and Path C both take the deliverable away from "the game we're playing together with your son" toward "content that runs in someone else's game" or "tool that powers other studios' seasons." The playtest partnership has been load-bearing for design instinct. **Only Matt can weigh whether this is a load-bearing project constraint or a graceful-degrade benefit.** The recommended Path B + warm-parallel Path C posture assumes graceful-degrade. If load-bearing, the answer becomes **Path A-prime** — Reincarnated-the-game preserved at developer-portfolio-grade playable demo scope with explicitly documented Phase-0 caveats (per-tier WR failures, missing range mechanics named rather than hidden). Eats much less Track F. Preserves the playtest partnership at slower cadence.

### 7.4 — Visual benchmark trajectory (galadriel, separate work in flight)

Today's parallel work: galadriel's visual benchmark report scored the demo's current state at 2.3/5 against the Diablo: Path of Exile / Diablo IV reference. After drax v1.24 portrait HUD remediation + color-register reconciliation (Matt picked option iii per-substrate-keyed in earlier dialogue) + ground-particle pass, trajectory is ~3.5+/5. **Load-bearing for Path A if pursued** — visual baseline 3.5+ closes most of the genre-credibility gap. For Path B mod-first, host-game art absorbs this entirely. Another structural Path-B advantage.

---

## § 8 — The recommendation in one paragraph (v4 — post-economics-rider)

**The data recommends Path B mod-first (Phase 1 Grim Dawn, ~9–12 weeks with R6) as a CREDIBILITY ladder, NOT a revenue play; with Path C engine-sale as the actual monetization target AND Path-B-as-standalone-product (Enderal model) held open as alternative monetization:**

- **Phase 1 Grim Dawn (~9–12 wk including R6):** Ship free class-pack mod with seasonal cohesion; target Dawn-of-Masteries-tier community reception (proven community-acceptance of class-only-as-complete artifact)
- **Phase 2 = TL2 OR TQAE OR both sequenced (~+2–3 wk per host leveraging R6 reuse):**
  - TQAE if IP-assignment clause is acceptable (credibility-only — no monetization, no portfolio licensing); future-proofs into TQ2 (late 2026)
  - TL2 if IP-assignment is disqualifying; cleaner permission + matched cultural-receptivity (most-receptive tier alongside GD)
  - **Both sequenced** is the data's nuanced answer for trinity completion at modest extra cost
- **Path C kept warm-parallel:** Legolas buyer-profile scouting + Last Epoch *Paradox Classes* commercial-data reverse-engineering during Phase 1
- **Path-B-as-standalone-product alternative (Enderal model):** after Phase 1+2 credibility, ship Reincarnated as paid Steam/itch.io standalone at indie pricing — bypasses mod-platform-cultural-no-paid-mods constraint. This is **Path A in standalone-product clothing**, riding on Path B's credibility ladder. *Preserves Reincarnated-the-game AND the playtest partnership with your son.*
- **Path A preserved at portfolio-demo scope** in parallel (not retired); ship Reincarnated-the-game with explicitly documented Phase-0 caveats; preserves credentialing artifact
- **Pre-Phase-1 action items:**
  - Matt contacts Crate (Medierra / Zantai) on monetization stance — combined ask covering both "paid GD mod" AND "paid standalone via itch.io / Steam carrying Reincarnated branding while built on GD"
- **Q5 family-partnership question** is the load-bearing one — the standalone-product path preserves the partnership; pure-mod-shipping-only weakens it; engine-sale ends it
- **Revenue framing corrected:** Path B mod-revenue is essentially zero (Patreon ceiling ~$30K/year at maximum scope, $0 for class-only ARPG mods). **The Director's strategic-prize framing — engine sale — is where the actual revenue lives**, validated more strongly than v1 implied
- **First-mover narrative confirmed:** procedural/generative modding is universally absent across all surveyed communities; Reincarnated would be first everywhere. *This is the press story Legolas's pre-meeting research flagged, now empirically grounded.*

---

## § 9 — Provenance

Authored 2026-05-19 morning by gandalf during Pattern-B dialogue with Matt. Synthesizes:

- `arpg-mod-target-database-2026-05-18.md` (914 lines) — KPI inventory + 16-candidate survey
- `arpg-mod-target-ranked-recommendations-2026-05-18.md` — synthesis with Wave-2A revisions
- `arpg-mod-target-scoring-matrix-2026-05-18.json` — machine-readable scoring
- `arpg-fight-mechanics-database-2026-05-18.md` — comparator combat data
- `arpg-gap-analysis-2026-05-18.md` — per-axis gap synthesis
- `canonical/story/apex-director-debrief-2026-05-18.md` — Director's strategic reframe
- `canonical/story/engine-vs-demo-fight-integrity-gap-2026-05-18.md` — 5-axis architectural gap
- `2026-05-19-modding-scope-grim-dawn.md` — rider 1 return
- `2026-05-19-modding-scope-titan-quest-ae.md` — rider 2 return
- `2026-05-19-modding-scope-torchlight-2.md` — rider 3 return
- `2026-05-19-modding-scope-terraria-tmodloader.md` — rider 4 return
- `2026-05-19-mount-doom-new-releases-and-modding-purpose.md` — rider 5 (pending)

v2 lands when Mount Doom rider returns; will incorporate per-host modding-purpose taxonomy + post-training-cutoff candidate verdicts.

*The road forks; the data speaks; the riders ride. Mithrandir signs.*
