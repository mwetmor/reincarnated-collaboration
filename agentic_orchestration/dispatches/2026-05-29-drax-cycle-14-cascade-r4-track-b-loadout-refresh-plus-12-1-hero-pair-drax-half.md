# Dispatch — 2026-05-29 — drax — cascade-r4 Track B — loadout app refresh + § 12.1 hero pair drax half

**From:** knight-rider
**To:** drax
**Approved by:** Matt 2026-05-29 (cascade-r4 § 11.2 Track B + Amendment 2 hero pair delegation; Step 7 CONFIRM-FIRE)
**Authority document:** `agentic_orchestration/cycle-14-hive-mind-state.md` cascade-r4 § Step 6/7 + § 11.2 + Amendment 2 (commit `b9cd9e0`)
**Estimated effort:** Track B loadout refresh ~1-2d Mode L work; § 12.1 hero pair drax half ~2-4h
**Acceptance:** Loadout app surfaces season_001 4-cluster output + Wanderer post-gamora; § 12.1 hero selected by drax + galadriel pair consensus; auto-commit per CLAUDE.md addendum
**Hive-state:** ENABLED — parallel fan-out with gamora + galadriel + legolas + gandalf

---

## Context

cascade-r4 Step 6 Matt CONFIRM-FIRE + two amendments. Step 7 four-track parallel fan-out fires. Track B is the player-facing surface track: drax (loadout app refresh + summary tab + § 12.1 hero pair drax half) + galadriel (CV scoring against genre peers + § 12.1 hero pair galadriel half) + legolas (image-gen prompts from substrate metadata).

Amendment 2 — Matt 2026-05-29 late verbatim "leave the seasonal hero call up to galadriel and drax." Hero selection moves off Matt's plate; galadriel + drax pair becomes selection authority for § 12.1.

Amendment 1 — Wanderer architecture (gamora dispatch in parallel). Loadout app data contract MUST handle `cluster_id` as integer (1,2,3,...) OR string "SINGLETON" (Wanderer state). Drax baseline work proceeds on existing 4-cluster output; Wanderer-layer integration extends post-gamora.

---

## Required reading before starting

1. THIS dispatch
2. cascade-r4 § Step 6/7 + Amendment 1 + 2: `agentic_orchestration/cycle-14-hive-mind-state.md` tail (commit `b9cd9e0`)
3. Path X completion record + season_001 output: `agentic_orchestration/dispatches/2026-05-29-rocket-cycle-14-cascade-resumption-4-path-x-phase4-feeds-phase5.md` (completion record) + `agentic_orchestration/cycle-14-wave-5-season-001/phase5_faction_clusters.json` + `phase7_season_summary.json`
4. Designer-writes-substrate principle: `canonical/story/2026-05-29-designer-writes-substrate-player-names-experience-principle.md`
5. Style register (locked): `canonical/story/style-register.md`
6. Canonical 38 D7 AI-tell line: `canonical/38-downstream-delivery-strategy-2026-05-23.md` § D7
7. Gamora Amendment 1 dispatch (for coordination): `agentic_orchestration/dispatches/2026-05-29-gamora-cycle-14-cascade-r4-amendment-1-wanderer-architecture.md`
8. Galadriel dispatch (pair coordination): `agentic_orchestration/dispatches/2026-05-29-galadriel-cycle-14-cascade-r4-track-b-cv-scoring-plus-12-1-hero-pair-galadriel-half.md`

---

## Scope

### Track B § 11.2 — drax loadout app refresh + summary tab

1. **Loadout web app refresh** (`reincarnated-loadout/` React/Vite/Tailwind/Vercel) to surface Cycle 14 v1 production output as it lands:
   - season_001 (Path X output: 4 substrate-led factions; Wanderer architecture extends post-gamora)
   - seasons 002 + 003 as Track A produces them
   - Data contract: consume per-season `phase5_faction_clusters.json` + `phase7_season_summary.json` + Wave B kit names

2. **Summary tab UI surface** integrating:
   - Per-faction tiles (cluster_id ∈ {1,2,3,...} + faction name + modal lineage + BC engagement signature + element distribution + member count + Wave B kit names)
   - Per-Wanderer tiles (cluster_id="SINGLETON" + "Wanderer of [Season Identity]" framing + Wave B kit name + substrate metadata)
   - 3-season comparison surface (when Track A lands)
   - Hero image + Meshy animation embed (when § 12 lands)

3. **Cluster_id type union handling:** loadout app data layer MUST accept `cluster_id: int | "SINGLETON"` per gamora Amendment 1 cross-seam contract. Author TypeScript type union; document in drax notes.

4. **Style register adherence:** all UI surfaces honor `canonical/story/style-register.md` lock (hand-drawn pixel-art HD-2D-shaped register).

5. **Iterate as seasons land:** loadout app refresh is incremental; surface season_001 baseline NOW; extend per-Wanderer post-gamora; extend per-season-002+003 post-Track-A.

### § 12.1 hero pair drax half (Amendment 2)

Coordinate with galadriel as § 12.1 selection-authority pair. Drax provides:

1. **UX-fit read per candidate kit:** does the kit slot cleanly into the loadout app summary tab presentation? (cluster-membered: kit fits in faction tile; SINGLETON: kit anchors a Wanderer tile)

2. **Image-extraction feasibility per kit:** does the substrate metadata + 11 gear-slot composition support the § 12 extraction protocol? (cultural lineage + period + register + element + weapon family + faction OR Wanderer identity populated?)

3. **Implementation pragmatism preference:** rank candidates by substrate-metadata richness for ChatGPT API image-gen prompt construction (richest metadata → strongest prompt)

4. **Pair consensus selection:**
   - DEFAULT: hero per cluster faction (4 candidates in season_001; pair elects ONE faction's candidate as season marquee)
   - ALTERNATIVE: Wanderer-as-hero ("Lone Wanderer of [Season Identity]" pattern; substrate-honest + genre-thematic isekai canon); elected if pair judges Wanderer standalone identity stronger than any faction candidate
   - Pair operates by consensus; deadlock → gandalf sub-agent (NOT Matt) for design-fit adjudication

5. **Document selection** at `agentic_orchestration/drax/notes/2026-05-29-cycle-14-v1-seasonal-hero-selection.md`:
   - Per-cluster candidate read (galadriel)
   - Per-Wanderer candidate read (galadriel; if any)
   - UX-fit read (drax)
   - Elected hero + reasoning
   - Composes with cascade-r4 § 12.1 + Matt 2026-05-29 late delegation + substrate-led discipline

### § 12.2-12.4 — DEFERRED until hero selection lands

Per cascade-r4 § 12.2-12.4 (unchanged by Amendment 2):
- Drax generates seasonal hero image via ChatGPT API (substrate-metadata-informed prompt; coordinate with legolas Track B for prompt construction)
- Drax extracts 11 isolated gear-piece images
- Drax sends 12 images (1 hero + 11 gear) to Matt
- Matt loads into Meshy → returns animation URL
- Drax wires URL into loadout app summary tab

These steps fire AFTER § 12.1 hero pair selection lands. Coordinate via KR.

---

## Acceptance criteria

### Track B § 11.2 (loadout app refresh)

- [ ] Loadout app data layer handles `cluster_id: int | "SINGLETON"` type union
- [ ] Summary tab surfaces season_001 4-cluster output (baseline NOW; pre-Wanderer)
- [ ] Style register honored (hand-drawn pixel-art HD-2D-shaped)
- [ ] Iteration plan documented for: post-gamora Wanderer integration; post-Track-A season 002 + 003 surfacing; post-§ 12 hero + Meshy animation embed
- [ ] Vercel preview deployment lands (or local dev server if Vercel deferred)

### § 12.1 hero pair drax half

- [ ] UX-fit read per candidate kit produced
- [ ] Image-extraction feasibility read per candidate kit produced
- [ ] Pair consensus reached with galadriel (or deadlock escalation to gandalf-sub-agent)
- [ ] Selection documented at `agentic_orchestration/drax/notes/2026-05-29-cycle-14-v1-seasonal-hero-selection.md`
- [ ] § 12.2-12.4 DEFERRED notice in completion record (fires post-pair-selection close)

---

## Out of scope

- NO § 12.2-12.4 work this dispatch (defers to post-§ 12.1 selection)
- NO Wanderer architecture implementation (gamora Amendment 1; drax consumes the data contract)
- NO Track A seasons 002+003 work (rocket; blocked on gamora)
- NO image-gen prompt authoring (legolas Track B; drax consumes prompts post-legolas close)

---

## KR routing triggers

- Pair deadlock with galadriel → gandalf-sub-agent design-fit adjudication (NOT Matt)
- Three-way pair + gandalf deadlock → Matt surface (Pattern B design call; expected zero firings)
- Style register drift detected by galadriel CV scoring → coordinate via KR
- Substrate metadata gap surfaced (engine substrate-curation issue) → surface to KR for elrond routing
- Vercel deployment failure → Matt surface (push-to-remote authorization needed)

---

## Execution sequence

1. Read required-reading docs
2. Fire Track B § 11.2 work: loadout app data contract + summary tab UI baseline on season_001 4 clusters (NOW; pre-gamora Wanderer integration)
3. Fire § 12.1 hero pair drax half: UX-fit + image-extraction feasibility reads per candidate kit on existing 4 clusters (anticipate post-gamora Wanderer candidate addition)
4. Coordinate with galadriel (independent dispatch firing in parallel): pair consensus selection via shared notes file at `agentic_orchestration/drax/notes/...`
5. Auto-commit Track B § 11.2 work-products + § 12.1 selection note
6. Append completion record to this dispatch
7. AGENT_STATE.md updated
8. Tag: `drax/v1.0-cascade-r4-track-b-loadout-plus-12-1-pair-1`

---

## Deliverable summary back to KR

1. Loadout app refresh status (data contract + summary tab UI baseline)
2. § 12.1 hero pair selection outcome (DEFAULT faction-hero OR Wanderer-as-hero; selected kit + reasoning)
3. Pair coordination state (consensus reached OR deadlock escalated)
4. Wanderer integration plan (post-gamora-close iteration)
5. § 12.2-12.4 readiness (DEFERRED notice; fires post-pair-selection)
6. Vercel deployment state (preview URL OR local dev)
7. Tag committed
8. Commits made

---

## References

- cascade-r4 § Step 6/7 + Amendment 1+2: `agentic_orchestration/cycle-14-hive-mind-state.md`
- Path X output: `agentic_orchestration/cycle-14-wave-5-season-001/phase5_faction_clusters.json` + `phase7_season_summary.json`
- Style register: `canonical/story/style-register.md`
- D7 AI-tell line: `canonical/38-downstream-delivery-strategy-2026-05-23.md` § D7
- Gamora dispatch: `agentic_orchestration/dispatches/2026-05-29-gamora-cycle-14-cascade-r4-amendment-1-wanderer-architecture.md`
- Galadriel pair dispatch: `agentic_orchestration/dispatches/2026-05-29-galadriel-cycle-14-cascade-r4-track-b-cv-scoring-plus-12-1-hero-pair-galadriel-half.md`
- Legolas Track B dispatch: `agentic_orchestration/dispatches/2026-05-29-legolas-cycle-14-cascade-r4-track-b-image-gen-prompts-substrate-metadata.md`

---

**KR sign-off:** Authored per Matt 2026-05-29 Step 7 CONFIRM-FIRE + Amendment 2 hero pair delegation; routed to drax as seam owner of `reincarnated-loadout/` + § 12 image extraction per AGENTS.md scope map. Auto-commit per CLAUDE.md addendum. KR mediates pair consensus + deadlock escalation if needed.

---

## Completion record

**Completed:** 2026-05-29
**Agent:** drax
**Session commits:**
- `9ceeb40` — loadout: cycle-14 §11.2 Summary tab faction cluster tiles + cluster_id type union
- `c7b4bd0` — loadout: AGENT_STATE.md checkpoint
- `33678d2` — collab: §12.1 hero pair drax-half selection notes

**Tag applied:** `drax/v1.0-cascade-r4-track-b-loadout-plus-12-1-pair-1` (reincarnated-loadout repo)

---

### Acceptance criteria check

**Track B §11.2 (loadout app refresh):**
- [x] Loadout app data layer handles `cluster_id: int | "SINGLETON"` type union — `src/data/cycle14Types.ts` ClusterId type
- [x] Summary tab surfaces season_001 4-cluster output (baseline NOW; pre-Wanderer) — Cycle14SeasonSection + FactionClusterTile components live on /pitch
- [x] Style register honored (hand-drawn pixel-art HD-2D-shaped) — dark palette, pixel-register typography, minimal chrome matching existing Pitch page aesthetic
- [x] Iteration plan documented — in-code TODOs + AGENT_STATE.md + Cycle14SeasonSection.tsx
- [x] Build smoke-test: `npm run build` clean (870 modules, 0 TS errors, 81 tests passing)
- [ ] Vercel preview deployment: PENDING push authorization (Matt required per ADR-006)

**§12.1 hero pair drax half:**
- [x] UX-fit read per candidate kit produced — all 4 clusters assessed; ratings 2–5/5
- [x] Image-extraction feasibility read per candidate kit produced — substrate richness ranked; Cluster 3 highest
- [x] Pair consensus: DRAX-SIDE COMPLETE — Cluster 3 (Stormveil Ironclad Surge) elected; AWAITING GALADRIEL
- [x] Selection documented at `agentic_orchestration/drax/notes/2026-05-29-cycle-14-v1-seasonal-hero-selection.md`
- [x] §12.2–12.4 DEFERRED notice — recorded in selection notes § 6 and AGENT_STATE.md

---

### Deliverables back to KR

1. **Loadout app refresh status:** COMPLETE (baseline). Summary tab now surfaces 4 faction cluster tiles from season_001 Phase 5 output. `cluster_id: number | "SINGLETON"` type union implemented. Wanderer placeholder rendered (post-gamora slot held). Hero image placeholder rendered (post-§12 slot held). Build clean.

2. **§12.1 hero pair selection outcome:** DRAX-SIDE COMPLETE. Drax election: **Cluster 3 — Stormveil Ironclad Surge** (european + lightning-dominant + close-AOE; strongest substrate for image-gen prompt construction). Awaiting galadriel visual-coherence reads + CV scoring to complete pair consensus.

3. **Pair coordination state:** DRAX-HALF COMPLETE — galadriel reads outstanding. When galadriel returns, KR routes to drax for pair consensus confirmation or deadlock assessment.

4. **Wanderer integration plan:** Post-gamora Amendment 1 close. Wanderer placeholder tile is already rendered in Cycle14SeasonSection.tsx (cluster_id="SINGLETON" filter). When gamora ships Wanderer kits with SINGLETON cluster_id, they will surface automatically on refresh. No loadout-side structural work needed beyond data refresh.

5. **§12.2–12.4 readiness:** DEFERRED. Fires after: (a) pair consensus confirmed on hero selection, (b) legolas Track B prompt construction lands, (c) Matt authorizes Meshy handoff. All three prerequisites outstanding.

6. **Vercel deployment state:** Preview deploy NOT yet fired. Requires push authorization (Matt per ADR-006). Local dev server: `npm run dev` renders faction cluster tiles on /pitch route. Preview deploy can fire immediately once push authorization is given.

7. **Tag committed:** `drax/v1.0-cascade-r4-track-b-loadout-plus-12-1-pair-1` ✅

8. **Commits made:** 3 commits across 2 repos (2 in reincarnated-loadout, 1 in reincarnated-collaboration)

---

### Findings and notes for KR

**Wave B kit names not available:** Wave B implementation was missing at cascade-resumption-2. The faction clusters in phase5_faction_clusters.json contain engine-format kit IDs (e.g., `S1_endgame_bc_melee_high_flat_dex_none_s1`) but no LLM-generated per-kit names. The loadout displays member_count per faction rather than individual kit names. This is correct behavior for the current data state — per-kit names will surface when Wave B ships.

**substrate_anchored_personages null on all clusters:** The phase5_faction_clusters.json has `substrate_anchored_personages: null` on all 4 clusters. When substrate-anchored personages are populated by elrond in a future wave, the FactionClusterTile component will need a display extension. The null is currently handled silently.

**Individual kit substrate fields for §12.2:** Per-kit cultural_lineage_canonical, weapon_type_family, historical_period_canonical are in kit_archive.db (not in phase5 JSON). For §12.2 image-gen prompt construction, the elected kit's substrate fields should be retrieved from kit_archive.db. If this requires elrond, route to KR.

**Style register:** The faction tile UI uses the same dark palette (gray-950/900/800 backgrounds, mono-uppercase labels, border-based structure) as the existing Pitch page components. Pixel-art HD-2D register is honored at the UI chrome level; actual sprite/image assets will honor it when hero images land in §12.2+.
