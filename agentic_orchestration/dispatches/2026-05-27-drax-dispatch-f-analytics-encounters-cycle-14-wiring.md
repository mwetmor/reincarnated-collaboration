# Dispatch — 2026-05-27 — drax — Dispatch F: Analytics + Encounters Cycle 14 wiring (~1 week; Phase 7 IMPL gated; ✅ NOW UNBLOCKED)

**From:** knight-rider
**To:** drax (loadout/demo seam owner)
**Approved by:** Matt 2026-05-27 verbatim "Dispatch F (Analytics + Encounters Cycle 14 wiring): fires NOW (Phase 7 IMPL ✅ landed eca0aa5)"
**Estimated effort:** ~1 week (Analytics.tsx + Encounters.tsx wiring; engine data consumption; KPM + Phase 7 verdict + G-B distance + F-C analytics)
**Acceptance:** Analytics tab consumes Cycle 14 schemas (KPM bands + Phase 7 verdict tracking + G-B pairwise distance + F-C analytics); Encounters tab consumes Cycle 14 encounter_analytics post Phase 7 IMPL output (when available); no #45 vocabulary lock violations introduced

## Quality criterion (Move 1)

**Game-quality goal this dispatch serves:** wire player-facing Analytics + Encounters tabs to Cycle 14 production data (kit_archive + ExportFactionCluster + ExportFactionRelationship + phase7_kit_verdict_log + phase7_cluster_aggregate_log). Without Dispatch F, Cycle 14 production seasons emit data that NO player-surface consumes — Analytics shows Cycle 13 aggregates only; Encounters shows Cycle 13 reference. Composes "Engine first. Game second. Phase third." — engine-side close at Wave 5 flows into game-side surface at Analytics + Encounters.

**Refutation conditions:**
- ExportFactionCluster + ExportFactionRelationship schemas don't expose enough fields for Analytics consumption (schema gap)
- Phase 7 verdict log schemas not stable (gamora may refine post first production run)
- F-C analytics UI conflicts with existing Analytics tab visual language

## Context

**Matt verbatim:** "Dispatch F (Analytics + Encounters Cycle 14 wiring): fires NOW (Phase 7 IMPL ✅ landed eca0aa5)"

**Per drax Cycle 14 Pattern-A response (`a0a449e`):**

**Analytics gaps:**
- Functional aggregate display consuming all discovered seasons
- Zero Cycle 14 schema wiring: no KPM bands, no Phase 7 verdict tracking, no G-B pairwise distance, no F-C analytics

**Encounters gaps:**
- Shows Cycle 13 reference encounters
- No Cycle 14 encounter_analytics.json (Phase 7 IMPL output landed; Wave 5 production season output landing post Matt's Wave 5 firing)

**Upstream Cycle 14 data sources:**
- kit_archive (gamora `749d5aa` + Phase 7 IMPL `eca0aa5`) — gauntlet_pass_rate column added
- ExportFactionCluster (star-lord `bf7f659` + `94f8c88`) — primary_pair_flag + gb_selection_rationale + pairwise_distance_distribution fields
- ExportFactionRelationship (star-lord `6f94ce5`) — 6-enum relationship_type + tension_narrative + shared_history_hook + diversity metrics
- Phase7KitVerdictLog + Phase7ClusterAggregateLog (gamora `eca0aa5`) — Phase 7 2-layer verdict logs

## Required reading

- `canonical/49-loadout-sample-player-surface-design-2026-05-27.md` (player-surface design canonical)
- `canonical/story/ab-comparison-protocol-cycle-14-close-2026-05-27.md` (6 measurement dimensions; Analytics may surface subset for player consumption)
- `agentic_orchestration/drax/notes/2026-05-27-cycle-14-tab-integration-pattern-a-response.md` § Analytics + Encounters gap inventory
- `~/Games/reincarnated-loadout/src/components/Analytics.tsx` (primary target 1)
- `~/Games/reincarnated-loadout/src/components/Encounters.tsx` (primary target 2)
- `~/Games/reincarnated-engine/src/reincarnated/export/schemas.py` ExportFactionCluster + ExportFactionRelationship
- `~/Games/reincarnated-engine/src/reincarnated/simulation/phase7_db.py` Phase7KitVerdictLog + Phase7ClusterAggregateLog DDL
- `~/Games/reincarnated-engine/design/math/phase-7-2-layer-joint-gate-thresholds-2026-05-27.md` (Phase 7 thresholds canonical)
- `.claude/skills/reincarnated-drax-operating-procedure`

## Discipline #46 compliance

- N/A — loadout consumes engine output JSON; no DB queries

## Discipline #42 framing-audit

- **Q1:** (1) Cycle 14 schemas (ExportFactionCluster/Relationship + Phase 7 verdict logs) are stable enough for Analytics consumption; (2) Encounters consumption gated on Wave 5 production season output landing (POST Matt Wave 5 firing); (3) F-C analytics UI fits existing Analytics visual language
- **Q2:** verify schema field stability at impl entry (consult star-lord MIGRATION.md § v1.10 + § v1.11 + § v1.12); verify Wave 5 production season output JSON shape
- **Q3:** if schemas unstable OR Wave 5 output not yet available, partial-fire scope (Analytics now; Encounters when Wave 5 output lands) OR invoke #44 framing-refusal

## Scope

### Part 1 — Analytics tab Cycle 14 wiring (~3-4 days)

- [ ] KPM bands display per-cohort (5 cohorts: Damage / Defensive / Control / Support / Hybrid per Phase 7 spec § 1.3)
- [ ] Phase 7 verdict tracking (PASS / HELD-cohesion-fail / HELD-mechanical-fail / FAIL distribution)
- [ ] G-B pairwise distance histogram (from ExportFactionCluster.pairwise_distance_distribution)
- [ ] F-C analytics (relationship_type distribution; D7 AI-tell compliance score distribution; diversity smoke results)
- [ ] Composition with existing aggregate display patterns (do not break Cycle 13 backward compatibility)

### Part 2 — Encounters tab Cycle 14 wiring (~2-3 days; gates on Wave 5 production season output)

- [ ] Cycle 14 encounter_analytics consumption (engine emission post Wave 5 production season landing)
- [ ] Per-kit gauntlet_pass_rate display
- [ ] Per-cohort encounter sweep results
- [ ] Composition with existing Cycle 13 reference encounter display (Cycle 14 supersedes when available; backward compat for prior cycles)

### Closure

- [ ] Update `~/Games/reincarnated-loadout/AGENT_STATE.md`
- [ ] Build verification (tsc -b + vite build clean)
- [ ] Visual verification (manual test or screenshot)
- [ ] #45 vocabulary lock grep audit post-edit (zero new violations)
- [ ] Append completion record to this dispatch
- [ ] Commit + push per Matt's per-cycle push pattern

## Acceptance criteria

- [ ] Analytics tab consumes Cycle 14 schemas (KPM + Phase 7 + G-B + F-C)
- [ ] Encounters tab consumes Cycle 14 encounter_analytics (when Wave 5 production season output lands)
- [ ] No #45 vocabulary lock violations introduced
- [ ] Build clean
- [ ] Completion record + commit + push

## Out of scope

- Do NOT touch Loadout.tsx (Dispatch B scope)
- Do NOT touch Summary tab (Dispatch C; gated)
- Do NOT touch Sample tab (Dispatch D; gated)
- Do NOT touch stat calculator (Dispatch E; gated)
- Do NOT execute Wave 5 production season (gamora seam at Wave 5 dispatch; firing NOW per Matt authorization)

## Open questions for drax

- **Q-DF-1:** Wave 5 production season output JSON path — your judgment on convention (`output/cycle-14-production-season-001/encounter_analytics.json`?); coordinate with gamora Wave 5 output staging
- **Q-DF-2:** F-C relationship_type visualization — color-coding? force-directed graph? grid? Your UX judgment
- **Q-DF-3:** Phase 7 verdict display granularity — per-kit detail vs per-cohort aggregate vs per-season summary? Your UX judgment

## References

- Matt 2026-05-27 Dispatch F ratification
- Drax Pattern-A response `a0a449e`
- Phase 7 IMPL `eca0aa5` (gamora); Phase 7 thresholds canonical `3d4eda5` (jack-ryan); Phase 7 spec `0cf4e3d` (gandalf)
- ExportFactionCluster + ExportFactionRelationship + Phase 7 verdict log schemas

---

## Completion record

(append on completion)
