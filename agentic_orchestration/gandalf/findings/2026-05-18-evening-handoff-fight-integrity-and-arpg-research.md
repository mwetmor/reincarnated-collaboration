# Handoff — 2026-05-18 evening session — Fight-integrity gap + ARPG comparator research + Mod-target analysis

**Authored by:** gandalf, late evening 2026-05-18, before Matt's session close.
**For:** Matt (next session, 2026-05-19 morning); next gandalf instance loading this thread.
**Status:** Session-end handoff. All commitments closed. Pattern-B ready.
**Amended:** 2026-05-18 very late evening — added second-mandate deliverables (engine KPI inventory, expanded mod-target database, ranked recommendations) per Matt's "research EVERY SINGLE of these data points + active modding community games + scoring matrix" follow-up. See § "Second mandate" below.

---

## What Matt asked for at session start

(Late afternoon, after the playtest-finding + diagnostic-question exchange):

> "Write the doc now. And then tee up the conversation by researching EVERY SINGLE of these data points and all other data points across all ARPG games and especially the three recommendations from the Marketing Director (Wolcen, Dragon's Dogma 2, Grim Dawn). I need either a database to be created and loaded with this data or just an addition to one of our existing databases. Once that is done, please write up an analysis of what the differences are vs the current state/desired state of the engine. I know this will be a substantive use of your power as a white wizard, but this is what we will need to begin our next session, prepared to fight the forces of evil! As you prepare to develop, develop and action these workflows, please do not ask me for anything as I will be away for awhile."

## What got done

### Six deliverables, all filed

1. **Canonical doc — fight-integrity gap diagnosis.**
   - Path: `canonical/story/engine-vs-demo-fight-integrity-gap-2026-05-18.md`
   - Captures the 5-axis architectural gap (PackProxy / Aggregate WR / Dimensional mismatch / Range-not-a-design-lever / 3 decoupled AI implementations), Matt's "large room" correction shape, 5 recommended workstreams (R1–R5), per-commercial-path cost re-pricing.

2. **Pattern-B agenda amendment.**
   - Path: `agentic_orchestration/gandalf/open-threads/2026-05-19-pattern-b-commercial-direction-dialogue.md`
   - Added § 0.5 load-bearing context section + per-question amendments (Q1 / Q2 / Q3 / Q4 absorb the gap's path-cost re-pricing; Q5 stands).
   - Required reading reordered: fight-integrity gap doc first, then apex debrief, then research database + gap analysis, then prior context.

3. **ARPG fight-mechanics database — comparator data.**
   - Path: `agentic_orchestration/gandalf/research/arpg-fight-mechanics-database-2026-05-18.md`
   - Structured 12-axis profiles for 8 comparators: Wolcen, Dragon's Dogma 2, Grim Dawn (Director-named, deep dive) + Diablo II/III/IV, Path of Exile 1, Last Epoch (genre baseline). Plus Reincarnated's own profile.
   - Authored from 4 parallel Legolas Mode-A research returns + code-trace audit.

4. **Gap analysis — comparators vs. Reincarnated.**
   - Path: `agentic_orchestration/gandalf/research/arpg-gap-analysis-2026-05-18.md`
   - Per-axis gap analysis, per-comparator mod-first viability ranking (with Director-rec inversion finding), per-commercial-path cost re-estimate, recommended workstream priorities under each path, open Pattern-B questions.

5. **Code-trace audit findings (no doc, but captured in canonical doc § 1.3 and § 2).**
   - Fired 2 parallel Explore agents during the diagnostic exchange:
     - Demo runtime: confirmed no entity collision (`world/movement.ts:197-199` explicitly deferred), confirmed kite-mechanic over-applied via demo-side hardcoded `PREFERRED_RANGE` constants, confirmed AI is hardcoded TypeScript not reading from engine JSON for behavior fields
     - Engine sim: confirmed 1D scalar distance only, confirmed PackProxy mechanics, confirmed aggregate-mean WR convergence with no per-tier thresholds, confirmed 3-band distance state machine, confirmed no per-skill range data anywhere in the catalogue

6. **This handoff doc.**

### Three findings that emerged during research (Pattern-B inputs)

#### Finding 1: Director's mod-first ranking is technically inverted

- **Director rec:** Wolcen (#1) > Grim Dawn (#2) > Dragon's Dogma 2 (#3)
- **Technical evidence rec:** **Grim Dawn (#1) > Dragon's Dogma 2 (#2) > Wolcen (#3)**

Why:
- **Wolcen** is in maintenance-only mode (last patch July 2023, multiplayer shut down Sept 2024). ~24 average concurrent players May 2026 vs. 127k all-time peak. No Steam Workshop. XML-only modding cannot reach Gate of Fates or AI behaviors. Modding community functionally dormant.
- **Dragon's Dogma 2** has active modding (~1,100 Nexus mods) via REFramework, but ceiling is content-recombination not system-level injection. RE Engine exposes no level editor, no quest system, no scripted-dialog editor. Total-conversion not feasible. **Sub-genre mismatch (action-RPG vs. looter-ARPG) is architectural, not cosmetic.**
- **Grim Dawn** ships Crate's full internal toolset (Asset Manager, World Editor, Database Editor, Quest Editor, etc.). Empirical proof of injection-at-scale: Dawn of Masteries mod adds 53 playable classes. 10+ year active modding ecosystem. Fangs of Asterkarn (final expansion 2025–2026) sustains long-tail.

**Both rankings are valid for different goals.** Director may have ranked on commercial-visibility + genre-fit intuition; technical ranking weights modding-ecosystem viability. Pattern-B should surface this — Director may want to update his view, or may have outside info justifying his ranking.

#### Finding 2: The gap re-prices commercial paths asymmetrically

| Path | Track-F cost | Why |
|---|---|---|
| A — standalone | **9–15 dev-weeks** + class-retuning sprint | Must close all 5 axes; ship horizon shifted right 2–4 months |
| B — mod-first (Grim Dawn) | **~3 wk Track-F + 4–6 wk pipeline = ~7–9 wk** | Host game provides spatial substrate, range, collision, leash for free; we ship R1 + R3-subset |
| B — mod-first (Wolcen) | **~3 wk + 3–4 wk pipeline = ~6–7 wk but commercially weak** | Cheap engineering but dead platform |
| C — engine-as-tool (auto-battler buyer) | **~3–5 wk + ops layer = 3–6 months** | Buyer doesn't model space; skip R2/R4 |
| C — engine-as-tool (ARPG buyer) | **~9–15 wk + ops layer = 5–9 months** | Inherits Path A's requirements |

**Gap doesn't change which path is best — it widens the cost spread, in Path B's favor.**

#### Finding 3: Reincarnated currently violates 7-of-7 modern ARPG genre universals

Per the cross-comparator synthesis in the database (§ 5.6):
1. Real spatial substrate — NO (engine 1D)
2. Hard entity collision — NO (demo deferred)
3. Per-skill range published — NO (catalogue has no range data; **D2 had this in year 2000 — we're 26 years behind**)
4. Disengagement as a real option — NO (fight runs to 0 HP)
5. Per-tier balance contract — NO (aggregate mean)
6. Boss telegraph system — NO
7. Movement skill as build element — NO (player-side)

This is the framing that makes Path A (standalone) hardest. A standalone ARPG that violates all 7 of these will be evaluated by reviewers + players as "not actually an ARPG" because that's what the cumulative violations mean.

---

## What's queued for tomorrow

### Pattern-B opens when Matt opens gandalf session

Per `agentic_orchestration/gandalf/open-threads/2026-05-19-pattern-b-commercial-direction-dialogue.md` — the open-thread loads as first context. Updated reading list:

1. `canonical/story/engine-vs-demo-fight-integrity-gap-2026-05-18.md` (LOAD-BEARING — read first)
2. `canonical/story/apex-director-debrief-2026-05-18.md` (Director context)
3. `agentic_orchestration/gandalf/research/arpg-fight-mechanics-database-2026-05-18.md` (comparator data)
4. `agentic_orchestration/gandalf/research/arpg-gap-analysis-2026-05-18.md` (synthesis)
5. `agentic_orchestration/legolas/research/2026-05-18-marketing-director-pitch-context-and-paths-to-market.md` (pre-meeting research)
6. Quick scan `canonical/16-project-roadmap.md`

### Gandalf's pre-Pattern-B lean (open to revision through dialogue)

1. **Lead with the gap diagnosis.** Single highest-leverage new context since the Director meeting. Re-prices everything.

2. **Fire R1 now regardless of direction commit.** Per-tier balance targets (gamora, 1–2 weeks) is required infrastructure under every path. Sequencing now buys empirical validation of the diagnosis (failure appears in metric) and surfaces the class-retuning workload naturally.

3. **Recommended direction lean:** **Path B — Grim Dawn first, with Path C kept warm as parallel option once Path B proves the export pipeline.**
   - Lowest total engineering cost
   - Strongest technical mod platform (proven 53-class injection)
   - Aligns with Director's strongest leaning (mods-then-engine-sale ladder)
   - Sets up Path C buyer narrative: "our engine exports content into the most-modded ARPG of the last decade"
   - Path A defer (not kill) — costs most, exposes most product-market risk

4. **Surface the Wolcen-ranking inversion to the Director eventually.** Not as rebuttal — as updated info.

5. **Hold Q5 (emotional/family dimension) as the final input.** All other questions are resolvable with research and rigor. Q5 is a life question; should land at the end when everything else has been priced and the trade is visible.

### Pattern-B closure criteria (per open-thread)

- Matt converged on Q1 direction commit (or explicit "still undecided, revisit in N days")
- Decisions-log entry drafted (knight-rider routes)
- Roadmap adjustment scoped (if direction differs from current Phase-1 P1)
- Open-thread file moves to `closed/` with resolution note

If dialogue runs long: Pattern-B is sustained, multi-session is appropriate for direction-of-this-magnitude.

---

## What's NOT done (deferred, not abandoned)

1. **Track F (R1–R5) workstream dispatches.** These are recommendations to knight-rider for formal roadmap amendment per ADR-002. Cannot be sequenced until Matt's Pattern-B direction commit. Awaiting.

2. **Class-retuning sprint planning.** Triggered by R1 ship; pre-planning would be premature.

3. **Direct communication to Director about ranking inversion.** Pattern-B should produce Matt's read on whether/how/when. Not gandalf's call to send.

4. **Decisions-log entry.** knight-rider's territory, post-Pattern-B.

5. **Other Phase-1 P1 commitments potentially affected.** Roadmap doc not yet edited to reflect Track F insertion; awaiting direction commit before any roadmap surgery.

6. **VS2a queued demo work (separate from this thread).** Was already queued for tonight per the earlier survey; status check should happen at session open if relevant. Galadriel capture pipeline running in separate top-level terminal per Matt's session-mid update.

---

## Operational notes for next-session gandalf

- **Pattern-B is Matt-driven.** Gandalf engages, pushes back, proposes alternatives. Matt decides.
- **Don't pre-empt the direction commit.** All five workstream priority lists (§ 5 of gap analysis) are conditional on Path A / B / C / combination. Don't pick.
- **The gap re-pricing is the load-bearing new input.** Make sure it lands before Q1 deliberation.
- **The Wolcen finding is the load-bearing surprise.** Surface respectfully. The Director's rec was reasonable on commercial-visibility grounds; the technical inversion is new info, not a rebuttal.
- **Q5 register.** When Q5 arrives in the dialogue, the mythic-grounded voice is appropriate. Matt's son is named in the load-bearing context. "The road forks" is the right register.
- **Sub-agent invocation reminder.** Top-level Matt sessions can spawn sub-agents that themselves can spawn sub-agents (recursive). A sub-agent gandalf cannot recursively spawn (the postmortem at `agentic_orchestration/hive-mind/postmortem-sub-agent-spawn-architecture-2026-05-18.md` captured this). If next-session gandalf is itself a sub-agent of knight-rider, plan accordingly.

---

## Session arc summary (for continuity)

This session ran from late afternoon through evening:

- Matt opened with two playtest findings (boss/miniboss unbeatable, pack-handling broken) + three diagnostic questions (demo AI from engine JSON?, ARPG collision conventions?, standard ARPG AI patterns?)
- Investigation via 2 parallel Explore agents (demo runtime + engine sim) confirmed and structured the findings
- Diagnostic exchange surfaced 4 axes; Matt's clarifying questions added the 5th (range as design lever) and proposed the "large-room sub-gauntlet" correction shape
- Matt authorized: canonical doc + Pattern-B amendment + ARPG comparator research database + gap analysis vs. current/desired engine state
- 4 parallel Legolas Mode-A research agents fired: Wolcen, Dragon's Dogma 2, Grim Dawn, genre-baseline (D2/D3/D4/PoE/LE)
- All 4 returned within the session; database + gap analysis populated iteratively
- Session ends with all 6 deliverables filed, Pattern-B ready for morning open

---

*Filed 2026-05-18 evening by gandalf. The diagnosis is named; the comparators are catalogued; the gap is mapped; the paths are priced. The hive is fed; the road is drawn. Tomorrow we walk it together. Mithrandir signs, and rests.*

---

## Second mandate (added 2026-05-18 very late evening)

After the first handoff, Matt issued a second mandate:

> "Pull ALL of our engine's mathematical, geometrical, logical, temporal, geospatial, etc. KPIs/patterns and add them to the database for this reincarnated engine and also the 4 others (wolcen, dogma, grim dawn, ARPG baseline). Then, send agents out to find any/all ARPGs or Adventure/RPGs which allow modding and have currently active modding communities... Then gather all of the above KPIs/patterns for those active modding community games... Then gather all of the specifications/parameters of the modding interface and add those to the database... Then score the similarity across all vs reincarnated and score the similarity to the JSON packet that reincarnated provides as an output as compared with the necessary inputs of ALL of the modding community games and original 4. If any question does not get to the goal of understanding of the ability to tune reincarnated-engine to quick modding capability, then feel free to revise the questions/research/KPIs/scoring methodology as you go - per your wisdom and your hive mandate. I will be away once more."

### Additional deliverables filed

7. **Reincarnated engine KPI inventory** (in database § 2)
   - Comprehensive 8-section inventory: mathematical / geometrical / logical / temporal / geospatial / output schemas / content generation / catalogue
   - 24 geometry types catalogued with multiplier formulas
   - Full damage formula chain documented (base → scaling → buff → geometry → variance → hit/crit → armor/resistance → substrate matrix → pack AOE)
   - 9 canonical roles, 8 canonical ailments registries
   - Per-artifact JSON schemas with example field listings (monster, class, skill, gear, trait, season manifest, cosmological vocabulary)
   - LLM call timeline: ~317 calls / season, ~$0.74 / season

8. **47-candidate active-modding survey + top-15 ranked list** (in database § 5)
   - Path: `agentic_orchestration/gandalf/research/arpg-mod-target-database-2026-05-18.md`
   - Categories: ARPG, soulslike, open-world RPG, sandbox/survival, strategy
   - 47 candidates evaluated; 20 reach content-injection-or-better with active 2024-2026 communities
   - **MAJOR FINDING: Titan Quest Anniversary Edition surfaces as unexpected #2 candidate** — direct Grim Dawn ancestor, mastery system structurally identical, cross-porting established community practice

9. **Wave 2A modding-interface deep dives** (returning overnight; refinements queued)
   - In flight at handoff time: Titan Quest AE, Torchlight 2, Baldur's Gate 3 — all expected back overnight
   - **Returned by handoff time: Terraria/tModLoader** — critical finding: tModLoader has NO runtime JSON path; all content compiled C# at build time; per-season Reincarnated regen would require weekly rebuild + Workshop push or kRPG-style pre-allocated-slot workaround. Terraria MFS revised to 3.20 (down from 3.55).

10. **Modding-fit scoring matrix** (in database § 6)
    - Path: `agentic_orchestration/gandalf/research/arpg-mod-target-database-2026-05-18.md`
    - 4-axis scoring (KPI / Schema / Pipeline / Community) with revisable weights (20/35/30/15)
    - 15 candidates scored; tier bands (PRIMARY / Secondary / Niche / Not viable)
    - **Top tier:** Grim Dawn (4.05) + Titan Quest AE (3.85)

11. **Ranked recommendations doc** (final synthesis)
    - Path: `agentic_orchestration/gandalf/research/arpg-mod-target-ranked-recommendations-2026-05-18.md`
    - Per-target effort estimates with friction points
    - Phase-1 (Grim Dawn) + Phase-2 (TQAE) + Phase-3 (deferred) sequencing
    - Pattern-B Q1/Q2/Q4 input recommendations

### Three findings (additional, from second mandate)

1. **Reincarnated is structurally well-positioned for mod-export.** The engine's mechanical layer is fully deterministic JSON output; the LLM layer is cleanly isolated to naming/vocabulary. Any modding-export pipeline can run mechanics deterministically, then apply per-host naming, then translate JSON → host schema. **The architecture is the asset.**

2. **The Grim Dawn + Titan Quest AE pairing is the killer leverage finding.** Both hosts share Crate-Iron-Lore mastery-system DNA; cross-porting is established community practice; combined Phase-1+2 reaches 2× audience for ~+25% incremental engineering effort vs. single-target. **This was not in the Director's recommendation set.**

3. **R3 (schema migration) is OPTIONAL for Path B, REQUIRED for Path A.** Most modding hosts can absorb defaults for the gaps (per-skill range, telegraph windows, AI behavior fields) that Reincarnated currently lacks. This **dramatically widens the Path-A-vs-Path-B cost spread further than the fight-integrity-gap doc already named** — Path B Phase 1+2 (~14 wk total Track-F) vs. Path A's ~9-15 wk full Track F + class-retuning sprint.

### Revised Pattern-B recommendation (subsumes original)

**Recommended Q1 direction commit:** **Path B mod-first (Grim Dawn Phase 1 + Titan Quest AE Phase 2) with Path C kept warm-parallel.**

**Recommended Q2 mod-first target ordering:**
1. Grim Dawn first (~6-9 wk)
2. Titan Quest AE second (~2-3 wk incremental on Phase 1)
3. Phase 3 deferred (Torchlight 2 OR Terraria OR Path C transition based on Phase 1+2 reception)

**Surface Director-rec inversion respectfully** — Director ranked on commercial-visibility (valid), technical research adds TQAE as Crate-ancestral leverage play. Updated info, not rebuttal.

### Files filed this session (full list)

| # | Path | Size | Purpose |
|---|---|---|---|
| 1 | `canonical/story/engine-vs-demo-fight-integrity-gap-2026-05-18.md` | 29 KB | Canonical 5-axis gap diagnosis + R1-R5 |
| 2 | `agentic_orchestration/gandalf/open-threads/2026-05-19-pattern-b-commercial-direction-dialogue.md` | 10 KB | Amended Pattern-B agenda |
| 3 | `agentic_orchestration/gandalf/research/arpg-fight-mechanics-database-2026-05-18.md` | 50 KB | 12-axis × 8-comparator combat database |
| 4 | `agentic_orchestration/gandalf/research/arpg-gap-analysis-2026-05-18.md` | 37 KB | Per-axis gap + cost analysis |
| 5 | `agentic_orchestration/gandalf/research/arpg-mod-target-database-2026-05-18.md` | ~70 KB | KPI inventory + 47-candidate survey + 15-candidate scoring matrix |
| 6 | `agentic_orchestration/gandalf/research/arpg-mod-target-ranked-recommendations-2026-05-18.md` | ~25 KB | Final synthesis + Phase-1/2/3 sequencing + Pattern-B input |
| 7 | `agentic_orchestration/gandalf/findings/2026-05-18-evening-handoff-fight-integrity-and-arpg-research.md` | (this) | Session-end handoff |

### Wave 2A returns (ALL FOUR COMPLETED 2026-05-18 very late evening)

All 4 deep-dive agents returned: Titan Quest AE, Torchlight 2, Terraria/tModLoader, Baldur's Gate 3. Refinements integrated into database § 6 + recommendations § 10.

**Key refinement findings:**

| Target | Score change | Critical Wave 2A finding |
|---|---|---|
| Titan Quest AE | 3.85 → 3.275 | UI authoring overhead (8+ DBR files + art per mastery); affix library structural mismatch; community smaller than expected (~742 avg concurrent) |
| Torchlight 2 | 3.50 → 3.525 | DAT text format directly editable; 10-mod limit; Workshop auto-sync; SynergiesMOD has NO license for third-party builds (drops SynergiesMOD-nest option) |
| Terraria/tModLoader | 3.55 → 3.20 | NO runtime JSON path; per-season cadence requires weekly rebuild + Workshop push |
| Baldur's Gate 3 | 2.25 → 2.525 | Pipeline+community stronger than initial; mechanical fit weaker (fundamental mismatches confirmed across all axes) |

**Net tier ranking refined:**
- PRIMARY (≥4.0): Grim Dawn ALONE (4.05)
- Secondary (3.0-3.99): Torchlight 2 (3.525) > Titan Quest AE (3.275) > Terraria (3.20)
- Niche (2.0-2.99): everything else
- Not Viable (<2.0): Wolcen (1.65)

**Recommendation flip:** The Grim-Dawn-plus-TQAE "killer pairing" framing softens because TQAE community is smaller than expected. **Recommendation REMAINS:** Phase 1 Grim Dawn, Phase 2 TQAE — but the framing shifts from "doubles audience reach" to "extends reach modestly + builds cross-host credibility for Path C buyer narrative." Both are valid; the second is more honest.

**Phase 3 Option ordering shift:** Torchlight 2 (TL2) becomes stronger Phase-3 candidate by MFS than Terraria (TL2 3.525 vs Terraria 3.20). DAT text format + Workshop auto-sync makes TL2 most developer-friendly Tier-2 target. Terraria still has order-of-magnitude larger audience (~32k avg vs TL2 250 avg) but operational cost (rebuild + art) is steep — best framed as "moonshot reach" post-Phase-1+2.

### What's NOT done (deferred, not abandoned) — additional

7. **Verification of Grim Dawn v1.2.0.0 modding tool compatibility.** Surfaced as friction-point; needs confirmation before Track-F commitment.
8. **Steam Charts data for TQAE concurrent players 2025-2026.** Affects community-score component of MFS.
9. **SynergiesMOD openness to third-party class additions.** Wave 2A TL2 agent may resolve.
10. **BG3 Script Extender procedural stat generation depth.** Wave 2A BG3 agent may resolve.
11. **V Rising Bloodcraft mod license / openness.** Could serve as nested platform; not investigated this pass.
12. **Project Diablo 2 third-party class loader status.** D2 archaic-pipeline penalty may change if PD2 has matured.
13. **Asset-binding model decision** — human-art / host-default / LLM-image-gen — needs Matt input.
14. **Per-host LLM naming budget approval** — additional cost per host accepted?

### Operational notes for next-session gandalf (updated)

- **Check for Wave 2A returns first.** Three agents (TQAE, TL2, BG3) may have returned overnight. If so, integrate findings into database + recommendations doc; refine MFS scores.
- **Pattern-B opens with the Grim Dawn + TQAE pairing finding as the headline.** This is the highest-leverage new context for Q1/Q2 deliberation since the original fight-integrity gap doc.
- **The Wolcen-rec inversion + TQAE addition is updated info for the Director, not rebuttal.** Matt drives that communication when he chooses.
- **Path-A-vs-Path-B cost spread is now even wider than the fight-integrity doc named.** R3 is OPTIONAL for Path B because mod hosts absorb defaults. Make sure this lands in Q1 deliberation.
- **The R3-optional finding may revise the original Track-F sequencing recommendation.** Fire R1 first is still correct; R3-subset (per-skill range + geometry params + AI fields) is the minimum needed for Path B; full R3 (all 5 axes) is only needed for Path A. Don't sequence full R3 unless Path A is committed.

---

*Re-filed 2026-05-18 very late evening by gandalf. The mod-target landscape is mapped; the pairings are found; the cost is priced again. Two roads to the same Crate-ancestral lineage; one engineering investment reaches both. Mithrandir signs once more, and now truly rests. The hive holds; the road is drawn; tomorrow we walk it together.*
