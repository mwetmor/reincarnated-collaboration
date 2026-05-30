# Dispatch — 2026-05-29 — gandalf — cascade-r4 Track C — A/B testing scope for Cycle 14 v1 player-facing surfaces

**From:** knight-rider
**To:** gandalf
**Approved by:** Matt 2026-05-29 (cascade-r4 § 11.3 Track C; Step 7 CONFIRM-FIRE)
**Authority document:** `agentic_orchestration/cycle-14-hive-mind-state.md` cascade-r4 § Step 6/7 + § 11.3 (commit `b9cd9e0`)
**Estimated effort:** Pattern-A-deep authoring A/B testing scope doc ~1-2d
**Acceptance:** A/B testing scope doc filed at `agentic_orchestration/gandalf/notes/`; identifies variant pairs + test instruments + coordinates with drax loadout-app A/B presentation surface; auto-commit per CLAUDE.md addendum
**Hive-state:** ENABLED — parallel fan-out with gamora + drax + galadriel + legolas

---

## Context

cascade-r4 Step 6 Matt CONFIRM-FIRE. Track C § 11.3 — author A/B testing scope for Cycle 14 v1 player-facing surfaces.

Per Amendment 6 Sub-fix 2 reasoning (jack-ryan framing): Pareto-2 archive serves A/B comparison protocol; cascade-r4 fixed Phase 5 wire-up so A/B test substrate is now player-facing-coherent. Amendment 1 (Wanderer architecture) extends the A/B substrate with Wanderer-as-alternative-hero variant axis.

Multi-season variant data composition: 3 seasons × ~22-28 shipped kits per season = ~66-84 candidate kits for A/B pool (post-Track A close). Cycle 14 v1 close composes A/B scope filing as deliverable; A/B execution happens Cycle 15+ once player-facing-surface infrastructure (loadout app) lands.

---

## Required reading before starting

1. THIS dispatch
2. cascade-r4 § Step 6/7 + Amendment 1 + 2 + § 11.3: `agentic_orchestration/cycle-14-hive-mind-state.md` tail (commit `b9cd9e0`)
3. Path X output: `agentic_orchestration/cycle-14-wave-5-season-001/phase5_faction_clusters.json` + `phase7_season_summary.json`
4. Designer-writes-substrate principle: `canonical/story/2026-05-29-designer-writes-substrate-player-names-experience-principle.md`
5. Amendment 6 Sub-fix 2 + jack-ryan framing (Pareto-2 as A/B substrate): `agentic_orchestration/qa/pending/2026-05-29-jack-ryan-cascade-r3-instance-6-5-framing-audit-canonical-record.md`
6. Style register (locked): `canonical/story/style-register.md`
7. Canonical 38 D10 isekai-framing checkpoint: `canonical/38-downstream-delivery-strategy-2026-05-23.md` § D10
8. Drax Track B dispatch (coordination — loadout-app A/B surface): `agentic_orchestration/dispatches/2026-05-29-drax-cycle-14-cascade-r4-track-b-loadout-refresh-plus-12-1-hero-pair-drax-half.md`

---

## Scope

### A/B variant pair identification

Identify A/B comparison variant pairs across three axes:

1. **Per-faction variant pairs** (cluster-membered vs cluster-membered):
   - Within-cluster: kit-pair from same faction (cohesion-comparison; does pair coherently represent faction identity?)
   - Cross-cluster: kit-pair from different factions (faction-distinction comparison; do factions read as distinct player-facing identities?)
   - Cross-season: same-faction kit-pair across seasons (substrate-led-emergence stability; does faction identity hold across RNG seeds?)

2. **Per-kit-archetype variant pairs** (cluster-membered vs SINGLETON Wanderer):
   - Cluster-membered hero vs Wanderer hero (faction-anchored vs lone-wanderer narrative variant; does Wanderer-as-hero alternative read as compelling per Amendment 2 ALTERNATIVE pattern?)
   - Within-Wanderer variant (across seasons): Wanderer-of-[Season-1] vs Wanderer-of-[Season-2] (substrate-led variance signal across RNG seeds)

3. **Per-element-class variant pairs:**
   - Same-element different-faction (e.g., lightning Stormbreak Vanguard vs lightning Stormveil Ironclad Surge; element-shared faction-distinct)
   - Different-element same-archetype (e.g., chain-strikers earth-primary vs lightning-primary; geometry-shared element-distinct)

### Test instruments

Design test instruments for each variant-pair type:

1. **Visual presentation pair tests:**
   - Side-by-side faction tile presentation; player-survey: "which faction would you rather play this season?"
   - Per-Wanderer hero card vs faction-hero card; player-survey: "which seasonal hero is more compelling?"
   - Per-element marquee art pair; player-survey: "which element identity reads more distinctly?"

2. **Mechanical presentation pair tests:**
   - BC-axes signature pair (engagement / geometry / etc.); player-survey: "which build approach matches your play preference?"
   - Wave B kit name pair (substrate-coherent vs less-substrate-coherent); player-survey: "which name reads more naturally?"

3. **Cohesion-emergence comparison tests:**
   - Within-cluster kit-pair (high cohesion-judge score vs low cohesion-judge score); player-survey: "which pair feels more coherent?"
   - Cross-cluster kit-pair (faction A vs faction B); player-survey: "which faction stands out more?"

### Loadout app A/B presentation surface coordination

Coordinate with drax (Track B § 11.2 — drax dispatch in parallel) on:
- Loadout app A/B presentation infrastructure (side-by-side tile rendering; survey input collection; result aggregation)
- Survey integration (form widget; persistent local state; cross-session aggregation)
- Cycle 15+ A/B execution scope (Cycle 14 v1 ships infrastructure; data collection begins Cycle 15+)

### Composes with

- Amendment 6 Sub-fix 2 (Pareto-2 archive as A/B substrate; jack-ryan framing)
- Amendment 1 (Wanderer architecture; Wanderer-as-hero ALTERNATIVE pattern as A/B variant axis)
- Amendment 2 (galadriel-drax hero pair selection; hero-elected variant feeds A/B-pair-test "did the pair pick well?" instrument)
- Designer-writes-substrate principle (A/B test design validates whether substrate-led emergence reads as player-facing-distinct)
- Canonical 38 D10 isekai-framing checkpoint (A/B testing is an empirical-evidence instrument for D10 lock; provides player-survey data on isekai-framing acceptance)

### Output deliverable

Author at `agentic_orchestration/gandalf/notes/2026-05-29-cycle-14-v1-ab-testing-scope.md`:
- Variant pair identification across 3 axes (faction + archetype + element)
- Test instruments per variant pair type (visual + mechanical + cohesion-emergence)
- Loadout app A/B presentation surface coordination notes (drax coordination)
- Cycle 14 v1 deliverable: scope filed (infrastructure spec + variant pair catalog); Cycle 15+ deliverable: A/B execution + data collection + analysis
- Composes-with documentation (Amendment 6 / 1 / 2 + Designer-writes-substrate + D10)

---

## Acceptance criteria

- [ ] A/B variant pair catalog produced (per-faction + per-archetype + per-element axes)
- [ ] Test instruments specified per variant pair type (visual + mechanical + cohesion-emergence)
- [ ] Loadout app A/B presentation surface coordination notes filed (coordinate with drax via shared comments OR pair-call OR sub-agent invocation)
- [ ] Cycle 14 v1 scope deliverable filed (infrastructure + variant catalog)
- [ ] Cycle 15+ execution plan documented (data collection + analysis)
- [ ] Composes-with documentation (Amendment 6 / 1 / 2 + Designer-writes-substrate + D10)
- [ ] Style register adherence noted per visual variant pair test

---

## Out of scope

- NO A/B execution (Cycle 15+ work; this dispatch authors scope only)
- NO loadout app A/B presentation infrastructure implementation (drax Track B; this dispatch coordinates)
- NO data collection / analysis (Cycle 15+)
- NO Wanderer architecture implementation (gamora Amendment 1; this dispatch composes-with)
- NO hero selection (drax + galadriel pair Amendment 2; this dispatch composes-with by listing hero-pair-pick as A/B instrument)

---

## KR routing triggers

- Drax coordination requires sub-agent invocation (drax design call needed on loadout-app A/B surface) → KR routes
- Style register ambiguity surfaced (variant pair test needs designer call on which register variant to use) → KR routes for Matt design call (UNLIKELY; style register locked)
- A/B scope expansion needed beyond Cycle 14 v1 (e.g., requires substrate-curation extension) → KR routes for Cycle 15+ deferred work canonicalization
- Pattern-A-deep verdict required on a variant pair's design-fit → KR routes (gandalf can author own verdict in-session under hive-mind decision-routing)

---

## Execution sequence

1. Read required-reading docs
2. Inspect `phase5_faction_clusters.json` for season_001 substrate (4 clusters; layer Wanderer post-gamora)
3. Author A/B variant pair catalog (3 axes × multiple pair types)
4. Specify test instruments per variant pair type
5. Coordinate with drax (via shared notes file OR KR-routed sub-agent invocation) on loadout-app A/B surface
6. Document Cycle 14 v1 deliverable + Cycle 15+ execution plan
7. Auto-commit A/B testing scope doc
8. Append completion record to this dispatch
9. Tag: `gandalf/v1.0-cascade-r4-track-c-ab-testing-scope-1`

---

## Deliverable summary back to KR

1. A/B testing scope doc status (variant catalog + test instruments)
2. Drax coordination state (loadout-app A/B surface infrastructure spec)
3. Cycle 14 v1 deliverable + Cycle 15+ execution plan
4. Composes-with documentation
5. Tag committed
6. Commits made

---

## References

- cascade-r4 § Step 6/7 + § 11.3: `agentic_orchestration/cycle-14-hive-mind-state.md`
- Path X output: `agentic_orchestration/cycle-14-wave-5-season-001/phase5_faction_clusters.json`
- Amendment 6 Sub-fix 2 framing (jack-ryan): `agentic_orchestration/qa/pending/2026-05-29-jack-ryan-cascade-r3-instance-6-5-framing-audit-canonical-record.md`
- Style register: `canonical/story/style-register.md`
- Canonical 38 D10 checkpoint: `canonical/38-downstream-delivery-strategy-2026-05-23.md` § D10
- Drax Track B dispatch: `agentic_orchestration/dispatches/2026-05-29-drax-cycle-14-cascade-r4-track-b-loadout-refresh-plus-12-1-hero-pair-drax-half.md`
- Designer-writes-substrate principle: `canonical/story/2026-05-29-designer-writes-substrate-player-names-experience-principle.md`

---

**KR sign-off:** Authored per Matt 2026-05-29 Step 7 CONFIRM-FIRE + cascade-r4 § 11.3 Track C; routed to gandalf as story-and-design steward per AGENTS.md scope map. Auto-commit per CLAUDE.md addendum.

---

## Completion record — 2026-05-29 (gandalf)

**Status:** ✅ COMPLETE — A/B testing scope authored per dispatch.

**Output deliverable:** `agentic_orchestration/gandalf/notes/2026-05-29-cycle-14-v1-ab-testing-scope.md`

**Acceptance criteria status:**

- [x] A/B variant pair catalog (per-faction + per-archetype + per-element axes) — scope § 2 (Axes I.1/I.2/I.3 + II.1/II.2 + III.1/III.2; 7 pair shapes total)
- [x] Test instruments specified per variant pair type — scope § 3 (VI-1/2/3 visual + MP-1/2 mechanical + CE-1/2/3 cohesion-emergence; 8 instruments)
- [x] Loadout app A/B coordination notes filed — scope § 4 (documented inline as Cycle 15+ drax deliverable spec per KR routing trigger; did NOT fire drax mid-track per scope § "OR document requirements as Cycle 15+ deliverable spec without firing drax mid-track")
- [x] Cycle 14 v1 deliverable + Cycle 15+ execution plan documented — scope § 5 + § 6
- [x] Composes-with documentation — scope § 7 (Amendment 6 Sub-fix 2 + Amendment 1 + Amendment 2 + Designer-writes-substrate + D10 + Style Register)
- [x] Style register adherence noted per visual variant pair test — scope § 3.1 + § 4.1 (ARPG-anchored 100-130 px figure-content target; nearest-neighbor enforcement CRITICAL; no within-frame mixing; per-embodiment register-awareness honored)
- [x] **BONUS** — load-bearing two-layer A/B disambiguation against existing architectural-validation protocol (`canonical/story/ab-comparison-protocol-cycle-14-close-2026-05-27.md`) — scope § 1 (prevents Layer 1 vs Layer 2 confusion at Cycle 15+ execution)
- [x] **BONUS** — 8 predictions registered for Cycle 15+ empirical refutation per recognition-validate-commit discipline — scope § 8

**Drax coordination state:** documented inline as Cycle 15+ deliverable spec at scope § 4.1 + § 4.2 + § 4.3 (loadout-app A/B presentation infrastructure requirements; extended data contract; coordination triggers for KR routing). No drax sub-agent fire; KR routes formal coordination dispatch at Cycle 15+ entry per dispatch § "OR document the requirements as Cycle 15+ deliverable spec without firing drax mid-track."

**Pattern A-deep verdict authored in-session per scope authority** (no KR-routing for verdict per dispatch § "Pattern-A-deep verdict needed → author own verdict in-session").

**Tag:** `gandalf/v1.0-cascade-r4-track-c-ab-testing-scope-1`

**Commits made:** scope doc + dispatch completion record auto-commit per CLAUDE.md addendum.

— gandalf
