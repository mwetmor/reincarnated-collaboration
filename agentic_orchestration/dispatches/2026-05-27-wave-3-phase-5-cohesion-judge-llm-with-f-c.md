# Dispatch — 2026-05-27 — Wave 3: Phase 5 cohesion-judge LLM architecture + F-C inter-faction relationships (gandalf + star-lord; Path III integrated)

**From:** knight-rider
**To:** gandalf (LLM prompt authoring + cohesion-judge composition + F-C narrative) + star-lord (ExportFactionRelationship schema + per-pair LLM calls infra)
**Approved by:** Matt 2026-05-27 pre-ratification #2 (F-C LLM prompt tonal direction) + Path III ratification (F-C scope addition per `agentic_orchestration/gandalf/notes/2026-05-27-path-iii-kr-amendment-kicker.md` § 5)
**Estimated effort:** ~2 weeks combined (gandalf prompt authoring + cohesion-judge composition ~1 week; star-lord ExportFactionRelationship schema + per-pair LLM infra + diversity smoke ~1 week; parallel with G-B at Dispatch 3B)
**Acceptance:** Phase 5 cohesion-judge LLM architecture impl + F-C per-pair inter-faction relationships impl; THEMATIC_REGISTRY consumption per § 9.1+§ 9.2; D7 AI-tell compliance ≥0.7; cosine-distance diversity <0.7 per season; ExportFactionRelationship schema + MIGRATION

## Quality criterion (Move 1)

**Game-quality goal this dispatch serves:** lock per-season faction-level narrative coherence layer — Wave 3 transforms PM-1 emergent clusters into player-facing factions with thematic identity + inter-faction relationships. Without F-C inter-faction relationships, factions exist as isolated clusters with no narrative tension. Composes "Engine first. Game second. Phase third." orientation.

**Refutation conditions:**
- THEMATIC_REGISTRY consumption pattern doesn't match prompts (registry term-type tags vs prompt slot mapping mismatch)
- D7 AI-tell compliance score saturates (all PASS at first impl; threshold meaningless)
- F-C cosine-distance >0.7 (narrative diversity inadequate; LLM produces homogeneous tension narratives)
- Per-pair LLM call cost exceeds Path III estimate ($0.15-$0.30 added per season)
- relationship_type distribution becomes "all enemies" default (Matt pre-ratification #2 explicitly forbids)

## Context

**Matt pre-ratification #2 (F-C LLM prompt tonal direction):**
- relationship_type distribution: substrate-evidence-driven across 6-enum; LLM NOT defaulting to "all enemies"; substrate-distance + lineage-difference vote
- Cross-cultural neutrality: no cultural-tradition is intrinsically antagonist; LLM does NOT bring training-data cultural priors
- Genre-appropriate tone; D7 AI-tell templated; 1-2 sentence constraints
- Diversity smoke-test: TF-IDF n-gram (2,4) cosine distance per Star-lord Seam 3 current backend; cosine distance average <0.7 across tension_narratives per season; sentence-transformers upgrade path dormant ✅

**Path III F-C scope (per kicker § 5):**
- Per faction-pair per season (k=3 → 3 pairs; k=4 → 6 pairs), LLM Pattern B structured call
- LLM output: relationship_type enum + tension_narrative + shared_history_hook + primary_pair_intensifier + ai_tell_compliance_score
- ExportFactionRelationship JSON schema (rocket Phase 5 implementation)
- Token cost budget: ~$0.15-$0.30 added per season; within SC-3 envelope
- D7 AI-tell discipline compliance: structured output; templated; constrained enums; ai_tell_compliance_score ≥0.7 acceptance
- Diversity-of-narrative smoke-test: cosine distance between tension_narrative sentences must average <0.7

**Composition with current state:**
- THEMATIC_REGISTRY at `canonical/story/thematic-registry-2026-05-27.md` (meta `da56926`; 665 entries; § 9.1 Wave A consumption pattern documented)
- Star-lord Dispatch 3B Seam 3 already provides asyncio + AsyncAnthropic infra + ExportFactionCluster schema (engine `bf7f659`)
- PM-2 D-Sharpened § 2.7 + § 3.7 (engine `7233e0f`) — Wave A consumption invariance
- G-B primary_pair_flag input (Dispatch 3B integration; primary_pair_intensifier in F-C LLM output)

## Required reading

- `canonical/story/thematic-registry-2026-05-27.md` § 9.1 + § 9.2 (consumption pattern)
- `~/Games/reincarnated-engine/src/reincarnated/generation/math/phase-5-pm-2-faction-label-assignment-math-2026-05-27.md` § 2.7 + § 3.7 (D-Sharpened invariance)
- `~/Games/reincarnated-engine/src/reincarnated/export/schemas.py` ExportFactionCluster (existing schema)
- `~/Games/reincarnated-engine/src/reincarnated/llm/phase5_orchestrator.py` (existing infra)
- `agentic_orchestration/gandalf/notes/2026-05-27-path-iii-faction-assembly-extension.md` (Path III full spec; F-C details + LLM prompt sketch § 3.4)
- `agentic_orchestration/gandalf/notes/2026-05-27-path-iii-kr-amendment-kicker.md` § 5 (Wave 3 F-C scope addition)
- SC-3 (legolas) Pattern B Structured Output with Layer Tags
- Engineering-disciplines.md § Discipline #1 / #11 / #18 / #19 / #41 / #42 / #44 / #46 / D7 AI-tell

## Discipline #46 compliance

- ExportFactionRelationship schema design Discipline #46 § 7 per-cell bounding
- All DB queries stream / push-to-SQL / index / bound
- EXPLAIN QUERY PLAN captures
- MIGRATION.md per ADR-004 for ExportFactionRelationship

## Discipline #42 framing-audit

- **Q1:** (1) THEMATIC_REGISTRY § 9.1 consumption pattern is impl-ready; (2) D7 AI-tell threshold ≥0.7 is empirically achievable; (3) cosine-distance <0.7 acceptance band is empirically achievable
- **Q2:** verify registry term-type tag → prompt slot mapping (gandalf authoring); verify ai_tell_compliance_score calibration on first smoke
- **Q3:** if D7 threshold or cosine-distance acceptance unachievable empirically, invoke #44 + route back for threshold re-calibration

## Scope (two seams + cross-cutting)

### Seam 1 — gandalf: LLM prompt authoring + cohesion-judge composition + F-C narrative (~1 week)

- [ ] Wave A faction-level cohesion-judge LLM prompt template (consumes THEMATIC_REGISTRY § 9.1; element × cultural_lineage cell filter + SPARSE/EMPTY fallback)
- [ ] Wave B per-kit identity LLM prompt template (consumes THEMATIC_REGISTRY § 9.2; refined cell filter)
- [ ] **F-C per-pair LLM prompt template** (relationship_type 6-enum constrained; substrate-distance + lineage-difference framing; cross-cultural neutrality directive; 1-2 sentence tension_narrative + shared_history_hook + primary_pair_intensifier; D7 AI-tell templated)
- [ ] relationship_type 6-enum specification (substrate-evidence-driven; e.g., {antagonist, rival, allied, neutral, mysterious, parallel})
- [ ] SC-3 Pattern B Structured Output with Layer Tags integration
- [ ] D7 AI-tell compliance verification logic (≥0.7 threshold)
- [ ] Cross-Character Diversity Audit DETECTION integration
- [ ] D-Sharpened invariance verified at all prompts

### Seam 2 — star-lord: ExportFactionRelationship + per-pair LLM infra + diversity smoke (~1 week)

- [ ] ExportFactionRelationship JSON schema (faction_a_id + faction_b_id + relationship_type + tension_narrative + shared_history_hook + primary_pair_intensifier + ai_tell_compliance_score + diversity_metrics)
- [ ] **MIGRATION.md** per ADR-004 entry
- [ ] Per-pair LLM call orchestration (extends Wave A/B to handle k(k-1)/2 pairs per season)
- [ ] Concurrency: composes with existing AsyncAnthropic + Semaphore(10) (per `bf7f659`)
- [ ] Diversity smoke-test: TF-IDF n-gram (2,4) cosine distance computation across tension_narratives per season; <0.7 acceptance
- [ ] Cost monitoring: $0.15-$0.30 added per season (target); empirical capture
- [ ] Phase 5 orchestrator integration: F-C calls fire AFTER Wave A (cluster faction calls) + BEFORE Wave B (per-kit identity); composes with primary_pair_flag from G-B

### Cross-cutting

- [ ] Cohesion fields integration with ExportFactionCluster (ai_tell_compliance_score + cohesion_judge_confidence fields ALREADY in `bf7f659`)
- [ ] Phase 7 joint-gate input ready (cohesion fields populated; Phase 7 dispatch separate)
- [ ] No-classes vocabulary throughout (Discipline #41 LOAD-BEARING)
- [ ] Wave 3 GATES gandalf THEMATIC_REGISTRY landing → already CLOSED at `da56926` ✅

### Risks + Watch Items (per failure-modes register § 5)

- F-4 Phase 5 LLM volume drift (cost monitoring)
- F-9 LLM relationship narrative homogeneity (cosine-distance smoke)
- D-2 faction pre-authored drift (substrate-led discipline at relationship_type)
- D-4 Phase 5 LLM as oracle drift (registry as input; LLM output bounded by enum)
- D-5 joint-gate theological drift watch (Discipline #11 at faith-holy cell consumption)

### Closure (per seam)

- [ ] Update respective AGENT_STATE.md (gandalf + star-lord)
- [ ] Tag per seam: `<seam>/v1.X-wave-3-phase-5-cohesion-judge-1`
- [ ] MIGRATION.md for ExportFactionRelationship (star-lord)
- [ ] Per-seam completion records appended
- [ ] Commit + push per Matt 2026-05-27 per-cycle push pattern

## Acceptance criteria (cross-seam)

- [ ] All Wave A + Wave B + F-C LLM prompts authored
- [ ] D7 AI-tell compliance verification logic implemented
- [ ] ExportFactionRelationship schema landed + MIGRATION.md
- [ ] Per-pair LLM call orchestration integrated with existing Phase5Orchestrator
- [ ] Diversity smoke-test PASS (cosine-distance average <0.7)
- [ ] Cost within budget ($0.15-$0.30 added)
- [ ] No-classes vocabulary verified (Discipline #41 grep)
- [ ] Per-seam tags + completion records + commit + push

## Out of scope

- Do NOT touch Phase 4 (gamora Dispatch 3A complete)
- Do NOT touch Phase 7 joint-gate impl (separate Phase 7 dispatch)
- Do NOT touch Dispatch 3B Seam 1 (rocket PM-1 impl; queued separately)
- Do NOT touch THEMATIC_REGISTRY (gandalf cross-cutting closed at `da56926`)
- Do NOT touch Wave 5 production-season (separate dispatch)

## Open questions

- **Q-W3-G-1 (gandalf):** relationship_type 6-enum exact values — your judgment per substrate vote + cross-cultural neutrality
- **Q-W3-S-1 (star-lord):** F-C call sequencing relative to G-B primary_pair_flag — gate F-C on G-B completion OR fire in parallel? Your judgment

## References

- Matt pre-ratification #2 verbatim (above)
- Path III F-C spec (`path-iii-faction-assembly-extension.md` § 5)
- THEMATIC_REGISTRY `da56926`
- Star-lord `bf7f659` (Phase5Orchestrator + ExportFactionCluster)
- PM-2 `7233e0f` (D-Sharpened)

---

## Completion record (two seams)

### Seam 1 — gandalf

**Status:** LANDED 2026-05-27 (RE-FIRE after prior API stream timeout at 658s).

**Deliverable:** `canonical/story/phase-5-llm-prompts-cohesion-judge-2026-05-27.md` (931 lines; commit `3532d76`; pushed).

**Three LLM call surfaces specified:**
- § 4 Wave A faction-level cohesion-judge LLM prompt template (SYSTEM § 4.2; USER § 4.3; acceptance § 4.4); registry § 9.1 consumption; D-Separate per PM-2 § 3.3
- § 5 Wave B per-kit identity LLM prompt template (SYSTEM § 5.2; USER § 5.3; acceptance § 5.4); registry § 9.2 consumption; archetype-name + place-name + secondary motif slots
- § 6 F-C per-pair inter-faction relationship LLM prompt template (SYSTEM § 6.3; USER § 6.4; acceptance § 6.5; distribution § 6.6); Path III addition; consumes Wave A + G-B primary_pair_flag + computed substrate_vote

**Q-W3-G-1 resolved (§ 6.1):** `relationship_type` 6-enum = `{antagonist, rival, allied, neutral, mysterious, parallel}`. Rationale anchored on Diablo IV / PoE / Mushoku Tensei / Earth Self meta-layer; substrate-evidence-driven; cross-cultural neutrality binding; rejects `nemesis` / `progenitor` / `descendant` (pre-authored mythological taxonomy violations of Discipline #41).

**Q-W3-S-1 design recommendation (non-binding; star-lord judgment per dispatch):** GATE F-C on G-B completion (G-B is O(k²) at k∈{3,4}; trivial compute; not latency-meaningful; F-C still fires in parallel across pairs). § 12.2 of deliverable.

**D7 AI-tell verification (§ 8):** combined LLM self-assessment + mechanical grep validation; threshold ≥ 0.7 PASS; ≥ 0.5 ACCEPT_WARN; < 0.5 REGENERATE (max 1); mechanical grep takes precedence on conflict.

**Diversity audit (§ 7):** composes with star-lord Seam 3 cosine-distance infrastructure (`bf7f659`); TF-IDF n-gram (2,4) cosine < 0.7 per season per Matt pre-ratification #2; Wave A re-fire with diversity-penalty system prompt on collision; max 1 regeneration per surface.

**D-Sharpened invariance (§ 2 + § 5.5 + § 6.8):** `substrate_anchored_personage` NOT in any Wave A / Wave B / F-C prompt template; Gate-2 grep audit pattern in § 10.2; player-experience load-bearing property protected.

**Discipline #45 vocabulary lock LOAD-BEARING throughout** (§ 3 documents discipline + carve-outs for narrative term-type tag `archetype-name` per registry § 5 + player-facing emitted output per `canonical/story/` exemption).

**Cross-seam composition spec (§ 9):** Phase5Orchestrator integration sequence specified; per-season cost projection ~$0.65 (k=3) / ~$1.20 (k=4) within SC-3 envelope; ExportFactionRelationship schema reference for star-lord Seam 2 (gandalf does not author schema).

**Open questions queued post first 3 seasons:** F-D2 cosine threshold calibration; F-C12 cross-cultural neutrality validation; F-D3 `ai_tell_compliance_score` saturation check (joint gandalf + star-lord review at wave-close).

**Hand-back:** KR routes star-lord Wave 3 Seam 2 (per-pair LLM infra + ExportFactionRelationship schema + diversity smoke; MIGRATION.md per ADR-004) + rocket 1-line `_apply_gb_tiebreak` step 4 lexicographic_tiebreak return-value fix. Both consume this canonical prompt spec.

### Seam 2 — star-lord
(pending; consumes Seam 1 canonical spec at `canonical/story/phase-5-llm-prompts-cohesion-judge-2026-05-27.md`)
