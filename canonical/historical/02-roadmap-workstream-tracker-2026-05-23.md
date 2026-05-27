# 02 — Workstream Tracker Roadmap (HISTORICAL — superseded 2026-05-26)

> **STATUS:** HISTORICAL (superseded 2026-05-26 by new `canonical/02-roadmap.md` — Engine Build Visual-Flow Tracker) — see `canonical/00-ground-state.md`
>
> **Demotion reason:** workstream-tracking layer was duplicating ground-state.md § 5 and per-cycle scope-docs. Replaced by an operational engine-build progress tracker structured around the QD-engine workflow visual flow (per doc 39), updated at every commit during hive-mind cycle execution, maintained by knight-rider through engine build completion.
>
> **What's still valid here for lineage:** active-workstream snapshot through 2026-05-25; deferred architectural commitments + empirical-evidence gates (the latter partially migrated to recognition records and to the new roadmap's deferred-commitments section).
>
> **Original document follows below.**

---

> **Living-doc protocol (HISTORICAL):** updated whenever workstream state shifts (new workstream enters; existing closes; dependency landscape changes). Authored / maintained by gandalf. Supersedes `canonical/historical/16-project-roadmap.md` (A-series roadmap, HISTORICAL — predates QD-rebuild + vast-library pivot + D1-D10 lock).

**Date:** 2026-05-23 (initial authoring)
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-05-23 — confirmed during cleanup-pass session
**Purpose:** name the active + queued + deferred workstreams with explicit dependencies + empirical-criterion gates. The companion to `canonical/00-ground-state.md` — the oracle says *what's true*; this doc says *what's sequenced*.
**Companion docs:**
- `canonical/00-ground-state.md` — current epoch + canon status
- `canonical/38-downstream-delivery-strategy-2026-05-23.md` — D1-D10 delivery strategy keystone
- `canonical/37-engine-and-game-two-products.md` — Variant C lock (engine vs game)
- `canonical/story/fate-genre-recognition-and-mobile-alignment-trajectory-2026-05-23.md` — recognition record (commitments gated)
- `canonical/story/hive-mind-protocol-weapon-library-import-2026-05-22.md` — substrate-acquisition P-series
- `canonical/story/hive-mind-protocol-qd-engine-rebuild-2026-05-21.md` — engine-rebuild P-series

---

## 0. TL;DR

The roadmap has four layers:

1. **Active workstreams** (in flight RIGHT NOW): see § 1.0 status update for current accurate state (2026-05-25 entry is canonical; 2026-05-23 entry preserved as historical).
2. **Queued workstreams** (immediate next, sequenced): T4-B post-mortem evaluation (post-Cycle-12 close); engine P1 hypothesis tests / Layer 7 BDI test framework (DEFERRED v1.1 per Option γ); substrate P2/P3/P4 sequence; per-agent operating-procedure skill packaging.
3. **Deferred architectural commitments** (gated by empirical-evidence criteria, not time): D10 Path C lock as Fate-genre; D1 mobile-platform reconsideration; MVP scope lock; faction architecture; three-tier branding; Track M1 mythological-named-weapons fire; Pi infrastructure execution; Layer 7 BDI test framework; broader weapon-equip flexibility.
4. **Out of scope** (not in current roadmap): items belonging to other canonical authorship or to specialist decisions outside the roadmap's reach.

Every deferred commitment lists the **specific empirical-evidence criterion** that gates re-engagement. Per the discipline: recognition → validate against substrate evidence → commit. No commitments fire on time-passage; all commitments fire on evidence.

**Three different P-series in current use — disambiguation:**

| P-series | Range | Purpose | Source |
|---|---|---|---|
| **Substrate P-series** | P0-P5 | Substrate processing pipeline (acquisition → cleaning → axis discovery → clustering → labeling → cohesion-judge validation) | This roadmap § 2.4-2.8 |
| **Engine P-series** | P0, P1 | Engine itself (P0 = constraint-removal CLOSED 2026-05-22; P1 = BDI hypothesis tests Layer 7 DEFERRED v1.1) | This roadmap § 2.7 |
| **QD-engine workflow Phases** | Phase 1-8 | Engine's runtime generation pipeline | `canonical/story/qd-engine-end-to-end-workflow-2026-05-24.md` |

See § 4.0 (QD-engine 8-phase workflow mapping to Cycle 12 Layers) for the v1-engine-scope clarification.

---

## 1.0 Status update — 2026-05-25 (active workstream state, current accurate)

Living-doc update reflecting workstream evolution post 2026-05-23 evening. Captures Cycle 10 closure + Cycle 11 closure + Cycle 12 open (Option γ full new engine parallel-build) + Tier 2 ratification + L9 substrate split + L11 strict 4-tuple gauntlet matching + Pi recognition record + hive-mind-scope-discipline 3 applications.

### Closed since 2026-05-23 evening status

| Workstream | Closure |
|---|---|
| **Cycle 10 — Substrate Curation Multi-Stage Dispatch** | ✅ FULLY CLOSED 2026-05-25 — tag `v1.0-weapon-substrate-cycle-10-shipped` cut + pushed at commit `75a1891`; v1_scope = 2,293 items LOCKED (Tier S=539 / A=675 / B=1,056 / C=23); all 7 Waves + 2 Sidecars + Wave 5.5 add-on CLOSED; jack-ryan Gate-2 PASS throughout; Recognition 1 (sampling-proportionality) MIGRATED v1.1+ → v1 LOCKED via composition policy v1 + Wave 5.5 + gandalf Path A verdict |
| **Cycle 11 — v1 implementation push (post-Cycle-10)** | ✅ FULLY CLOSED 2026-05-25 — tags `v1.0-t4-intent-metadata-ready` cut + pushed on engine (commit `70061a7`) + loadout (commit `b948d3d`); § 8 BC-shift sweep FAILED → diagnostic triple-fire → unanimous "architecture sound; test misaligned" → Matt Tier 2 ratification → drax Wave 3b M3/M6 shipped intent-metadata-display path + spirit-guide narration + Vercel preview; 5 post-cycle dispatches RETURNED (W1.13 blocked-flag; Algorithm § 8 consult; loadout scoping; G1 SQLite contention TRIGGERED; G12 NOT TRIGGERED); discipline-test outcome: escape-hatch fired correctly; KR escalated via diagnostic triple-fire pattern; Matt re-engagement at Tier 2 ratification |
| **Post-Cycle-10 canonical authoring queue (PARTIAL)** | Pi recognition record landed; matt-log-back-decisions captured; Cycle 12 framing brief RATIFIED with L1-L11 + interface contract § 4; remaining items (Phase 4 simplified archive math spec + Phase 5 cohesion-judge calibration spec + loot architecture + sub-element architecture + naming-space partitioning) DEFERRED to Cycle 12 wind-down or v1.1 |
| **Algorithm § 8 implementation v1** | ⚠️ SHIPS AS INTENT METADATA (Tier 2 path) — § 8 algorithm implemented (commit `3430269`); BC-shift validation sweep FAILED (test design + missing wire-up; architecture SOUND per unanimous diagnostic triple-fire); Tier 2 ratified — ships as intent metadata + spirit-guide narration + loadout display; Layer 6 wire-up (alterations reach combat arithmetic) DEFERRED to Cycle 12 via new engine layers; BDI mathematical validation DEFERRED to v1.1 (Cycle 13+) |
| **Loadout app readiness scoping** | ✅ COMPLETE — drax + star-lord scoping memo at `agentic_orchestration/drax/notes/2026-05-25-loadout-app-readiness-scoping.md`; 6 M-items M1-M6 + 5 Q1-Q5 ratified per Matt P2c "Approved"; drax M4 ✅ (Cycle 11); M3 + M6 ✅ (Cycle 11 Wave 3b); M1 + M2 + M5 pending star-lord schema extensions (likely absorbed into Cycle 12 Layer 2 work) |

### Active workstreams as of 2026-05-25 (post Cycle 12 open + Wave 2 in-flight)

**Matt locked-decisions 2026-05-25** (per gandalf log-back session covering Tier 2 + L9 + Option γ + L11 + Pi recognition + Cycle 12 framing brief bulk ratification):

1. **Tier 2 ratified** for Cycle 11 § 8 BC-shift FAIL response — ships § 8 as intent metadata + spirit-guide narration + loadout display; Layer 6 wire-up + BDI validation DEFERRED.
2. **L9 substrate split locked** (mechanical vs semantic) — cultural_tradition / lineage / period are SEMANTIC OVERLAY, NOT in BDI math model. Q-A verdict 2026-05-23 § 2.2 mathematical model REFINED per L9 (substrate_triple constituents = mechanical only). Q-A verdict addendum 2 added (SECOND canonical example of framing-audit on authored verdict). § 8 algorithm opportunity-scan triggers REFACTOR per L9 in Cycle 12 Layer 6 work.
3. **Option γ confirmed** for Cycle 12 (full new engine parallel-build — Layers 2+3+4+6; skip Layer 7 BDI test framework which DEFERS to v1.1 / Cycle 13+).
4. **L11 strict 4-tuple BC-target matching for gauntlet sim** locked (Cycle 12 scope); broader weapon-equip flexibility = v1.1+ deferred design concept (player-facing experience question separable from gauntlet sim's strict-match requirement).
5. **D1 Pi-Postgres infrastructure path RATIFIED** with Matt "right moment" execution deferral — Pi-Postgres for engine-internal DBs (telemetry + catalogue); D4 hosted-Postgres for loadout AMENDED to DEFERRED CONDITIONAL (only fires IF concrete YES-scenario surfaces; for v1 + foreseeable use cases, loadout stays static-JSON-bundled); D8 Tailscale install authorized for Matt 15-min window; D9 LLM cache DEFERRED (G12 NOT TRIGGERED — 0.13% repeat rate vs 20% threshold; structural cross-session zero collisions).
6. **Cycle 12 framing brief BULK RATIFIED** (8 Q-items Q1-Q8 + interface contract § 4 as-drafted) at `agentic_orchestration/gandalf/notes/2026-05-25-cycle-12-new-engine-parallel-build-framing-brief.md`.
7. **Skip-confirmation fire-forward re-authorized** for Cycle 12 wind-down (per Cycle 10 pattern precedent).

| Workstream | Owner | Status | Empirical-criterion gate |
|---|---|---|---|
| **Cycle 12 — v1 full new engine parallel-build (Option γ)** | knight-rider (hive-mind orchestrator); rocket L2 + L3 + L4 + L6; legolas Mode A MC-1 + MC-2 + MC-3; elrond SC-1 + SC-2 sidecars; jack-ryan Gate-1 + Gate-2 throughout | **WAVE 2 IN-FLIGHT 2026-05-25** — Wave 0/0.5 ✅ COMPLETE (prereq clearance: jack-ryan Gate-1 CLEAR-WITH-AMENDMENTS + legolas MC-1 Hybrid H3 + MC-2 hybrid filter-then-sample + gandalf comp-policy § 4 Option B + elrond pre-Layer-2 prep + SC-1 + SC-2); Wave 1 ✅ COMPLETE (rocket L2 46-min wall-clock + L3 17-min wall-clock; both jack-ryan Gate-2 PASS; CRITICAL VELOCITY ANOMALY — both layers landed in ~1 hour vs ~4-6 weeks estimated); Wave 2 ⏳ IN-FLIGHT (Gate-2 on L2 + MC-3 parallel); Waves 3-5 QUEUED (Layer 4 + Layer 6 + integration smoke + auto-close per skip-confirmation re-auth) | T4 post-mortem readiness milestone (new engine functional + § 8 wire-up reaches combat arithmetic via new engine layers + integration smoke + jack-ryan Gate-2 on full new engine PASS) |
| **T4-B post-mortem evaluation framework** | Matt + gandalf post-mortem session (post-Cycle-12 close) | **POST-CYCLE-12 — gated on T4 post-mortem readiness milestone** — per Matt 2026-05-24 algorithm-as-v1-deliverable lock; Cycle 12 closes engine generation track; T4-B becomes ~1-2 post-mortem sessions evaluating Layer 6 output via loadout app + hand-authoring ~5-10 alternative T4 entries for comparison | Cycle 12 closes + engine generates ~30-40 v1 forms with algorithm-produced T4s via new engine + forms upload into loadout app + Matt + gandalf post-mortem review session 1 |
| **Pi infrastructure execution** | star-lord (Postgres + migration); gandalf design-fit (recognition record reference); Matt schedule for "right moment" | **DEFERRED to Matt "right moment"** — D1 RATIFIED for Pi-Postgres engine-internal (telemetry + catalogue); G1 TRIGGERED with 4 kernel panics empirically confirmed; status-quo continues with PRAGMA busy_timeout mitigation (P2.5 landed Cycle 11); execution NOT in Cycle 12 scope per Matt P2a verbatim | Matt schedules Pi build (NVMe HAT + Ubuntu Server + Postgres install) + Tailscale install (D8; 15-min independent task) |
| **Hive-mind-scope-discipline (3 applications)** | gandalf authors + maintains; knight-rider consumes; jack-ryan reviews process-side | ✅ LANDED 2026-05-25 + 3 prospective applications | Cycle 10 founding retroactive ✅ PROVEN EFFECTIVE; Cycle 11 first prospective ✅ HOLDING UNDER ESCAPE-HATCH FIRE; Cycle 12 second prospective ⏳ IN-FLIGHT (Wave 2; holding through 8 dispatches + zero BLOCKs) |
| **W1.13 H1-H5 baseline + W1.20 BDI infrastructure (Layer 7 deferred)** | rocket + legolas + gamora + critique-pair (upstream chain) | **DEFERRED to v1.1 / Cycle 13+** — Layer 7 (BDI test framework) explicitly DEFERRED per Option γ confirmation 2026-05-25; framework + acceptance gates (H1-H5 + H8/H8.diff/H9 + G1-G4) retained as canonical for Cycle 13+ work via Q-A verdict 2026-05-23 + L9 addendum 2 | Cycle 12 close → engine functional → empirical observation surfaces whether statistical validation is warranted; if surfaces concerns OR by-design follow-on, Cycle 13 opens W1.20 + BDI test framework build |

### Companion artifacts 2026-05-25

- `agentic_orchestration/gandalf/notes/2026-05-25-cycle-12-new-engine-parallel-build-framing-brief.md` — Cycle 12 RATIFIED framing brief with L1-L11 + interface contract § 4
- `agentic_orchestration/cycles/cycle-12-hive-mind-scope.md` — Cycle 12 RATIFIED scope-doc
- `agentic_orchestration/gandalf/requests/2026-05-25-knight-rider-cycle-12-kicker.md` — Cycle 12 KR kicker (bundled with Cycle 11 close)
- `agentic_orchestration/cycle-11-wind-down-summary-2026-05-25.md` — Cycle 11 wind-down summary (RATIFIED)
- `agentic_orchestration/cycle-12-new-engine-parallel-build-state.md` — Cycle 12 live state file
- `canonical/story/infrastructure-raspberry-pi-postgres-and-closed-loop-pipeline-2026-05-25.md` — Pi infrastructure recognition record (D1-D10 enumerated; G1-G13 empirical gates; D1/D4/D8/D9 RATIFIED/AMENDED 2026-05-25)
- `agentic_orchestration/matt-log-back-decisions-2026-05-25.md` — Matt 7-decision log-back capture
- `agentic_orchestration/gandalf/notes/2026-05-25-w1-13-w1-20-framing-brief.md` — SUPERSEDED (preserved as historical for Cycle 13+ BDI work)
- `agentic_orchestration/operating-procedures/hive-mind-scope-discipline.md` — new discipline doc backported into hive-mind-protocol.md § 2.2 + KR OP § 1 / § 3.5

### Next-action sequence (post Cycle 12 Wave 2 in-flight 2026-05-25)

**Cycle 12 critical path** (5 Waves; Wave 2 in-flight; ~days to T4 post-mortem readiness given velocity pattern):

1. **Wave 2 completes** (current): jack-ryan Gate-2 on rocket L2 + legolas MC-3 (multi-dim convergence implementation libraries) — both gate Layer 4
2. **Wave 3 fires**: rocket Layer 4 (W1.13 multi-dim convergence) dispatch integrating Gate-2-on-L2 verdict + MC-3 recommendation + L9 substrate split + WARN-3 dict shape consumption + jack-ryan Gate-2 on L4
3. **Wave 4 fires**: rocket Layer 6 (§ 8 wire-up + L9 opportunity-scan refactor) dispatch + jack-ryan Gate-2 on L6
4. **Wave 5 fires**: integration smoke + jack-ryan Gate-2 on full new engine + KR auto-closes Cycle 12 wind-down per skip-confirmation re-auth → T4 post-mortem readiness milestone
5. **Post-Cycle-12**: T4 post-mortem session(s) (Matt + gandalf; ~1-2 sessions of 1-2 hours each); evaluates Layer 6 output via loadout app; hand-authors ~5-10 alternative T4 entries for comparison
6. **Post-T4-post-mortem**: v1 ship surface decision (narrow engine v1 vs broad game v1 vs wide playable v1) gates next workstream sequencing

**Next Matt-required touchpoint**: T4 post-mortem session 1 (~days to weeks from now; gated on Cycle 12 wind-down). Mid-Cycle-12 escape-hatch touchpoints: 25-cell vs 22-cell discrepancy if Gate-2 on L2 routes to gandalf design-fit; any L4/L6 layer-integration FAIL.

### v1.1+ deferred queue additions 2026-05-25

| Sub-carry | Description | Re-engagement trigger |
|---|---|---|
| **Layer 7 — BDI test framework** | W1.20 + H1-H5 + H8/H8.diff/H9 + G1-G4 acceptance gates per Q-A verdict 2026-05-23 + L9 addendum 2 | Cycle 12 closes + engine functional + empirical observation surfaces statistical-validation need (or by-design follow-on); Cycle 13+ opens |
| **Broader weapon-equip flexibility** (L11 deferred concept) | Player-game design question: should characters be allowed broader weapon equip flexibility (range/melee + period/culture loose-match) beyond their kit's strict 4-tuple BC-target match? | Future Pattern-B design call (gandalf + Matt); v1.1+ player-game design surface; separable from gauntlet sim's strict-match requirement |
| **Pi infrastructure execution** | Pi build (NVMe HAT + Ubuntu Server + Postgres install) + Tailscale install (D8) | Matt schedules "right moment" |
| **Hosted-Postgres for loadout DB (D4 CONDITIONAL)** | Only fires IF concrete YES-scenario surfaces in roadmap (player-saved loadouts / accounts / Earth Self server-side / `/the-work` live aggregation needs DB-backing / real-time refresh) | YES-scenario actually lands in roadmap; until then loadout stays static-JSON-bundled |
| **§ 8 algorithm 4 sim-extension-required strategies + proxy-spawn** | Resource-buffer + leech-replacement + zone-control + conditional-modifier (sim-extension-required); proxy-spawn (v1.1+ per BC-axes-lock) | Sim seam refactor lands; rocket fires v1.1 § 8 implementation against 4 strategies |
| **v1_scope row-count reconciliation** | KR direct-verified v1_scope = 2,293 (Tier-A 675) vs Cycle 10 close Tier-A = 1,431; 756-row drift since Cycle 10 close — cause unknown (possibly Cycle 10 Stage 4 mechanical-tagging or subsequent curation) | v1.1+ elrond reconciliation pass; flagged from Cycle 12 elrond pre-Layer-2 prep |
| **Substrate `element` column schema evolution** | No first-class `element` field on substrate; keyword inference works but fragile (rocket Layer 2 uses `infer_element_from_name`) | v1.1+ elrond schema evolution |
| **pf2ools-quarantined corpus pollution cleanup** | id=177340 surfaced PF2e character BACKGROUND tagged as weapon; suggests broader pf2ools-quarantined corpus may have analogous pollution | v1.1+ elrond Tier-B/Tier-C grep cleanup |
| **Wind / lightning critically thin substrate** (8 / 5 rows) | Substrate enrichment never reached comprehensive depth; thin-cell-fallback fires routinely for wind/lightning kits → kit variety will be repetitive | v1.1+ element-specific substrate enrichment continuation |
| **Cell 20 Holy Knight + Cells 11 Red Mage + 22 Monk + 24 Artillery Mage § 4.1 amendments** | Composition policy v1 § 4.1 one-line amendments per gandalf comp-policy § 4 Pattern A-light verdict | Post-Cycle-12 canonical-amendment pass |
| **SC-1 Subset C 94-row disposition** | Tier-S spurious-attribution items deferred from Cycle 12 SC-1 substrate-tagging cleanup | gandalf Pattern A-light (sequenced post-Cycle-12 close OR mid-cycle natural seam) |
| **SC-1 Tier-A/B/C activation for Brahmastra / Sudarshana Chakra / Aegis** | Framing brief examples were Tier-B/C (out of Cycle 12 SC-1 scope) | gandalf judgment + elrond execution |
| **Greek / Norse mythological period conventions** | Substrate-tagging convention discipline; gandalf judgment needed | gandalf judgment + elrond curation |
| **Discipline #26 candidate — diagnostic triple-fire pattern operationalization** | Discipline candidate surfaced from Cycle 11 BC-shift FAIL response (triple-fire of rocket calibration + gandalf design-fit + legolas methodology re-review converged on unanimous verdict) | jack-ryan engineering-disciplines.md amendment cycle (post-stability) |

---

## 1.0 Status update — 2026-05-23 evening (active workstream state, current accurate AT THAT TIME)

> **Note 2026-05-25:** this status update preserved as historical record. Current state at § 1.0 entry ABOVE (2026-05-25).

Living-doc update reflecting workstream evolution post-initial-authoring. Capture current accurate state; supersede § 1.1-1.3 snapshot for "what's active RIGHT NOW" reads.

### Closed since initial authoring (§ 1.1-1.3 snapshot superseded)

| Workstream | Closure |
|---|---|
| § 1.1 Phase D cleaning pipeline | CLOSED — Phase D concluded; downstream Phase E (clustering) also concluded |
| § 1.2 Canonical folder structural restructure | CLOSED — restructure complete |
| § 1.3 Documentation cleanup pass continuation | CLOSED — cleanup concluded |
| Phase E-1 clustering pipeline | CLOSED — frame-revision stratified subsample k=3; 125 clusters |
| Phase E-1.5 sensitivity sweep | CLOSED — Cycle 9.13; jack-ryan Gate-2 CONDITIONAL PASS |
| Phase E-2 cluster labeling + DB UPDATE | CLOSED — 125 canonical labels in production DB |
| P1 hive-mind preparation arc items 1-4 | CLOSED — T4-B scaffolding + engineering-disciplines.md canonical write (5 new disciplines #20-#25; 6 sub-discipline amendments) + per-agent OP propagation + hive-mind protocol amendment §§ 7.3-7.6 |

### Active workstreams as of 2026-05-24 evening (post Stage 3 design call closure + Architecture B lock)

**Matt locked-decisions 2026-05-24 evening** (per gandalf Stage 3 design call session covering D1-D7 decisions + engine architecture A/B/C discussion):

1. **Architecture B LOCKED as production canonical engine architecture** (substrate-bound at Phase 2 + substrate-genre-flagging unified-architecture). Supersedes Architecture A (substrate-AGNOSTIC; archived as developer-tool / R&D reference). Hypothesis: substrate-context (period/culture/named-personage) at engine level brings weight to clustering + algorithmic outcomes; genre-canonical alignment (D2/D3/D4/PoE/LE/GD all substrate-bind at generation). Empirical-trigger discipline § 4 for potential switch to A or C. See `canonical/story/qd-engine-end-to-end-workflow-2026-05-24.md`.
2. **Stage 3 design call FULLY CLOSED with D1-D7 all locked.** Composition policy v1 canonical doc landed at `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md`. v1_scope target ~1,700-3,100 items. Sidecar B scope expanded (off-hand items + 5 thin-cell-enrichment + 4 thin-tradition boost). Stage 3.5 budget ~25-50 engine-authored entries (4 Sketch F anchors + Cell 14 Pyromantic).
3. **Sub-element terminology disambiguation** (renamed from "element canonical-pair flavor" to disambiguate from retired seasonal-realm-mapping concept AND from legendary canonical-pair set-bonuses). Sub-elements are flavor manifestations of core elements per substrate-tradition at LLM-runtime (Phase 5 cohesion-coalescence).
4. **T4-B v1 catalogue reframed as POST-MORTEM evaluation** (per Matt 2026-05-24 algorithm-as-v1-deliverable lock). Algorithm § 8 mechanic-alteration implementation is v1 deliverable (rocket seam; post-Cycle-10; ~1-2 weeks parallel with W1.13/W1.20 BDI). T4-B post-mortem sessions (~1-2 sessions; ~3-5 weeks from now post-engine-form-generation + loadout-app upload) evaluate algorithm output + author ~5-10 alternative T4 entries for comparison.

| Workstream | Owner | Status | Empirical-criterion gate |
|---|---|---|---|
| **Cycle 10 — Substrate Curation Multi-Stage Dispatch** | knight-rider (hive-mind orchestrator); Sidecar A: star-lord + gandalf + jack-ryan; Stages 1-4: elrond + rocket + gandalf + gamora + legolas + jack-ryan; Stage 0 + 3 design calls: Matt + gandalf | **STAGE 3 DESIGN CALL CLOSED 2026-05-24; WAVE 5 NEXT** — Wave 1 (Sidecar A) CLOSED + committed + tagged + pushed; Wave 2 (Stages 1 + 1.5 + v1.1 fix) CLOSED + committed + tagged + pushed; Wave 3 (Stages 2 + 2.5 + pre-Stage-3 classifier) CLOSED + committed + tagged + pushed; Wave 4 (Stage 3 design call) CLOSED 2026-05-24 with D1-D7 all locked + composition policy v1 landed; Wave 5 (Stage 3 execution + Stage 3.5 gap-fills + Stage 4 mechanical-tagging) GATED on knight-rider authoring Stage 3 execution dispatch (in-scope; pending) | Wave 5: v1_scope subset materialized + Stage 3.5 ~25-50 engine-authored gap-fills + Stage 4 accurate mechanical-tagging on v1_scope including mythological-NULL rescue + Discipline #18 methodology consults (legolas Mode A for constrained-sampling + mechanical-tagging methodology) + jack-ryan Gate-2 PASS per dispatch § 8 |
| **T4-B v1 catalogue (REFRAMED to post-mortem)** | Matt + gandalf post-mortem session (post-engine-form-generation) | **POST-MORTEM evaluation framework; ~3-5 weeks from now** — per Matt 2026-05-24 algorithm-as-v1-deliverable lock; algorithm § 8 implementation is the v1 T4 deliverable; T4-B becomes ~1-2 post-mortem sessions evaluating algorithm output via loadout app + hand-authoring ~5-10 alternative T4 entries for comparison | Algorithm § 8 implementation lands + engine generates ~30-40 v1 forms with algorithm-produced T4s + forms upload into loadout app + Matt + gandalf post-mortem review session 1 |
| **Algorithm § 8 implementation (production T4 deliverable)** | rocket (engine generation/skill composition); Discipline #18 legolas Mode A consult required before; jack-ryan Gate-2 validates | **POST-CYCLE-10 v1 critical path** — per skill-system § 8.5 amendment + Matt 2026-05-24 algorithm-as-v1-deliverable lock; ~1-2 weeks rocket implementation; parallel with W1.13 + W1.20 BDI gamora work | Algorithm produces mechanic-alteration regime-changes per kit's BC-axis space + jack-ryan Gate-2 validates sim-viability; Discipline #18 consult lands first |
| **Loadout app readiness scoping** | drax + star-lord coordination; knight-rider routes | **POST-CYCLE-10 parallel work** — per `agentic_orchestration/gandalf/requests/2026-05-24-knight-rider-t4-reframing-and-loadout-readiness.md`; ~half-day combined sub-agent investigation; loadout must consume engine-generated forms + display skill trees for T4-B post-mortem authoring | drax + star-lord report current loadout form-rendering capability + skill-tree display status + T4-authoring-interface lift estimate |
| **9.12-A through 9.12-D — Question A workstream (W1.13 H1-H5 baseline + W1.20 BDI infrastructure)** | rocket + legolas + gamora + critique-pair (upstream chain) | UPSTREAM CHAIN UNMET → POST-CYCLE-10 UNBLOCKED — H1-H5 baseline not run; P1 substrate enrichment + W1.13 implementation + W1.20 BDI infrastructure prerequisites unmet; ~1-2 weeks gamora work post-Cycle-10 closure; can fire in parallel with algorithm § 8 implementation | Engine-seam in flight post-Cycle-10; gates per Q-A verdict § 12.4 + § 9 empirical-evidence criteria; not Matt's direct territory |
| **Post-Cycle-10 canonical authoring queue** | gandalf | **POST-STAGE-3 CLOSURE QUEUED** — ~6-8 hours canonical authoring during Cycle 10 wind-down: (1) Phase 4 simplified archive math spec ~30-45 min; (2) Phase 5 cohesion-judge calibration spec ~1 hr; (3) loot architecture canonical doc; (4) sub-element architecture canonical doc; (5) naming-space partitioning canonical doc; (6) optional knight-rider OP amendment if hive-mind decision-routing concern recurs | Cycle 10 wind-down phase |
| ~~**Weapon-substrate-conclusion declaration**~~ | knight-rider | ✅ CLOSED Cycle 9.16 | Conclusion-declaration artifact landed at `canonical/story/2026-05-23-weapon-substrate-conclusion-declaration.md` + roadmap § 3.8 added |
| ~~**9.14-A per-agent OP propagation fan-out**~~ | knight-rider sub-agent dispatch | ✅ CLOSED Cycle 9.15 | All 8 agents amended OP + installed SKILL with verbatim #21/#22 + engineering-disciplines.md cross-references |
| ~~**9.14-B cluster-116 elrond relabel**~~ | knight-rider sub-dispatch | ✅ CLOSED Cycle 9.15 | Single-row UPDATE on clusters.id=116 landed |
| ~~**Cycle 10 Stage 3 design call (D1-D7)**~~ | Matt + gandalf | ✅ CLOSED 2026-05-24 | D1 (Tier-S weapon-kind gate) + D2 (thin-cell action queue) + D3 (5-tuple → 3-tuple cell-collapse) + D4 (mythological-NULL rescue) + D5 (4 Sketch F anchors → Stage 3.5) + D6 (composition policy synthesis validated) + D7 (Stage 3.5 budget locked) — composition policy v1 canonical doc landed |
| ~~**Architecture B engine architecture lock**~~ | Matt + gandalf | ✅ CLOSED 2026-05-24 | substrate-bound at Phase 2 + substrate-genre-flagging unified-architecture; Architecture A archived as developer-tool reference; canonical doc landed |

### Companion artifacts

- `agentic_orchestration/gandalf/notes/2026-05-23-session-end-state-capture.md` — gandalf-side session-end state capture (substantive context for next-session pickup)
- KR session-end EOD handoff (forthcoming her territory) — orchestration-side session-end capture
- `agentic_orchestration/gandalf/notes/2026-05-23-question-A-w1-13-tier-4-hypothesis-verdict.md` + § 12 addendum — Q-A workstream design-spec
- `agentic_orchestration/gandalf/notes/2026-05-23-t4-b-v1-catalogue-scaffolding.md` — T4-B scaffolding
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (engine repo commit 1fae3fa) — 25 disciplines + 6 sub-discipline amendments

### Next-action sequence (post Stage 3 design call closure 2026-05-24)

**Stage 3 design call CLOSED 2026-05-24 with D1-D7 all locked + composition policy v1 landed + Architecture B locked. Next-action sequence:**

1. **Knight-rider authors Stage 3 execution dispatch** routing to elrond for constrained-sampling per composition policy v1 (knight-rider's in-scope orchestration; jack-ryan Gate-1 critique-pair before publishing)
2. **Stage 3 execution** (elrond seam): constrained-sampling produces per-row v1_scope flag + composition-trace metadata
3. **Wave 5 fires:** Stage 3.5 engine-authored gap-fills (rocket + gandalf + star-lord; ~25-50 entries; 4 Sketch F anchors + Cell 14 Pyromantic) + Stage 4 accurate mechanical-tagging on v1_scope including mythological-NULL rescue (rocket + gamora + jack-ryan + legolas Mode A consult)
4. **Stage 3.6 research-replacement notes** (gandalf authors per Stage 3.5 gap-fills)
5. **Cycle 10 wind-down:** roadmap + ground-state oracle updates + Cycle 10 closeout handoff + post-Cycle-10 canonical authoring queue (Phase 4/5 amendments + loot architecture + sub-element architecture + naming-space partitioning ~6-8 hours gandalf)
6. **Parallel post-Cycle-10 work:** Algorithm § 8 implementation (rocket; ~1-2 weeks; Discipline #18 consult first); W1.13 + W1.20 BDI implementation (gamora; ~1-2 weeks); loadout app readiness scoping (drax + star-lord ~half-day)
7. **Post-form-generation (~3-5 weeks from now):** engine generates ~30-40 v1 forms with algorithm-produced T4s → forms upload into loadout app → Matt + gandalf T4-B post-mortem session 1

**Next Matt-required touchpoint:** T4-B post-mortem session 1 (~3-5 weeks from now post-engine-form-generation + loadout-app upload). Window of low Matt-involvement between Stage 3 closure and T4-B post-mortem (Wave 5 + wind-down + algorithm § 8 + W1.13 all run without Matt-direct attention).
3. **Cycle 10 Waves 2-5** execute per dispatch § 4.1 dependency graph; ~3-4 calendar days post-Stage-0; produces v1_scope subset + composition policy doc + accurate mechanical-tagging
4. **T4-B v1 catalogue authoring** unblocked at Cycle 10 closeout; design call session 1 schedules (Matt's calendar territory)
5. **Question A upstream chain monitoring** (engine seam; rocket + others; not direct Matt territory; not gated on Cycle 10)

### v1.1+ deferred substrate-refinement queue

Per Matt locked-decisions, the following move to v1.1+ post-ship substrate-refinement queue:

| Sub-carry | Description | Re-engagement trigger |
|---|---|---|
| **9.11-C** | east_asian period_unknown curation gap (Cluster 90 ~10K rows) | Post-v1-ship; elrond Phase-D-bis-style review |
| **9.11-D** | Substrate-tagging-artifact review (~15-25 affected clusters) | Post-v1-ship; elrond systematic review |
| **9.11-E** | Geographic-origin vs cultural-lineage tagging discipline (canonical write candidate) | Post-v1-ship; elrond + jack-ryan discipline-amendment |
| **9.10-E** (subsumes **9.11-B**) | Substrate expansion via legolas Mode B; Mode-A-targeted crawls for all 5 marginal lineages (Smithsonian Latin American + INAH Mexico + Te Papa NZ + Bishop Museum + British Museum Pacific + Sámi cultural archives) | Post-v1-ship + D10 Path C architectural commitment OR explicit Matt-architectural-call |
| **Three design-discipline recognitions** | (1) Sampling-proportionality flagging per design surface (explicit declaration of policy at design-spec-as-math time); (2) Country-title name cleanup at substrate-curation (parse/flag geographic-encoding in canonical_name); (3) Commercial-vs-solo output differentiation per output stream (output_purpose field for engine generation). See `canonical/story/v1-1-plus-design-discipline-recognitions-2026-05-23.md` for full recognition record + empirical-evidence gates | Per recognition record § 4.2 — sampling-proportionality fires when T4-B v1 catalogue design call surfaces first explicit policy declaration; country-title cleanup folds into elrond v1.1+ work; output-purpose flag fires when multi-consumer engine scenario emerges (Profile B B2B SaaS scoping OR Reincarnated v1.1+ player-surface integration) |

These compose into a single post-v1-ship substrate-and-design-discipline-refinement work-unit. Until v1 ships + downstream surfaces consume substrate per Discipline #25 rep-audit, the substrate-as-is is operationally sufficient. The three design-discipline recognitions are forward-looking flags for v1.1+ design surface authoring, not v1-gating constraints.

---

## 1. Active workstreams (in flight)

### 1.1 Phase D cleaning pipeline (substrate normalization)

| Aspect | Spec |
|---|---|
| **Owner** | Elrond (executing under Pattern-B Gate-1 PASS-WITH-AMENDMENTS) |
| **State** | Mid-execution. Steps 1-6 complete per most recent reports; Steps 7+ in progress. |
| **Inputs** | 89,839-row weapon substrate (post-hive-mind-Cycle-8 wind-down). Phase A audit + Phase B policy + Phase C variant-cluster assignments completed earlier. |
| **Outputs** | Normalized substrate with `dedup_status` (canonical / merged / unprocessed); `weapon_kind` tagging; F1 RA TIERED collapse; F3 quarantines (pf2ools, souls-api); F4 cross-source canonical merge; updated v_category_sample view. |
| **Empirical criterion for completion** | All 7 cleaning steps committed; Discipline #11 empirical inspection at each gate passed; substrate ready for P2 axis discovery as feedstock. |
| **Unblocks** | P2 axis discovery (substrate Phase 2). |

### 1.2 Canonical folder structural restructure

| Aspect | Spec |
|---|---|
| **Owner** | Knight-rider (Pattern-B sub-agent dispatch authored 2026-05-23) |
| **State** | In flight (firing concurrently with this doc's authoring). |
| **Scope** | Move HISTORICAL-stamped docs to `canonical/historical/`; DEAD-stamped to `canonical/dead/`; same split for `canonical/story/`. Two outright deletes (CLI prompts 35 + 36). Cross-reference audit across all four sibling repos. Single end-of-pass commit. |
| **Empirical criterion for completion** | Commit lands; ~4 CURRENT docs visible at `canonical/` top-level; gandalf spot-check passes; cross-references resolved or flagged. |
| **Unblocks** | Cleaner browseable structure for next-session agents + Matt. |

### 1.3 Documentation cleanup pass continuation

| Aspect | Spec |
|---|---|
| **Owner** | Gandalf (story-and-design steward) |
| **State** | Near-complete. This roadmap doc closes the major-artifact authoring. Remaining: skill_handoff reframing as Matt-facing daily-state (queued, not yet executed). |
| **Empirical criterion for completion** | All cleanup-pass artifacts landed; agent-slowdown root cause (epoch-collision + per-invocation read budget growth) structurally resolved. |
| **Unblocks** | Team operates under disciplined documentation pattern; per-invocation read budget reduced 60-70%. |

---

## 2. Queued workstreams (sequenced, post-active)

### 2.1 Skill_handoff reframing as Matt-facing daily-state

| Aspect | Spec |
|---|---|
| **Owner** | Jack-ryan (working-agreement review) + knight-rider (integration) |
| **Trigger** | Cleanup pass continuation (1.3) closes |
| **Scope** | The next end-of-session handoff written by knight-rider treats Matt as primary audience (not next-session knight-rider). Sections: pending Matt-decisions queue; active workstreams + status; awaiting-Matt blockers; recent decisions Matt made; "next session pickup" guidance. |
| **Empirical criterion for completion** | Next handoff lands in new format; Matt confirms it's useful for session-start; pattern adopted as working-agreement. |
| **Effort** | Small (working-agreement edit + one handoff in new format). |

### 2.2 Per-agent operating-procedure skills + cross-cutting work-mode skills (Skill Creator packaging)

| Aspect | Spec |
|---|---|
| **Owner** | Multi-agent coordination via knight-rider; each agent authors their own per-agent OP skill; cross-cutting skills authored per ownership lineage |
| **Trigger** | Cleanup pass continuation (1.3) + Skill_handoff reframing (2.1) land |
| **Stream 2 — per-agent OP skills** | Thin operating-procedure skill (~500-800 words): session-start protocol; mode-selection (what kind of work is this session?); session-end protocol. Specialized work-mode skills compose on top |
| **Stream 2 landed (2026-05-23 morning)** | `operating-procedures/gandalf.md` (prototype); `operating-procedures/jack-ryan.md`; `operating-procedures/knight-rider.md` |
| **Stream 2 landed (2026-05-23 fan-out)** | `operating-procedures/rocket.md`; `operating-procedures/gamora.md`; `operating-procedures/star-lord.md`; `operating-procedures/elrond.md`; `operating-procedures/galadriel.md`; `operating-procedures/drax.md`; `operating-procedures/legolas.md` (Pattern C parallel fan-out per `gandalf/requests/2026-05-23-knight-rider-stream-2-per-agent-op-fan-out.md`; gandalf executed on Matt direct authorization 2026-05-23) |
| **Stream 2 status** | **COMPLETE.** All 10 agents now have per-agent OP skills. |
| **Stream 3 — cross-cutting work-mode skills** | Compose on top of per-agent OP skills when in specialized work modes |
| **Stream 3 landed (2026-05-23 keystone)** | `operating-procedures/hive-mind-protocol.md` — hive-mind work-mode skill (gandalf author; cross-cutting; covering state entry/exit + Wave cadence + decision routing per Matt 2026-05-23 directive + critique-pair structure + Discipline #19 + math hotspots + Discipline #18 + state-file + wind-down + sub-agent verdict pattern § 5.5) |
| **Stream 3 landed (2026-05-23 batch)** | `operating-procedures/engineering-disciplines.md`; `operating-procedures/decision-log-format.md`; `operating-procedures/canonical-doc-format.md`; `operating-procedures/substrate-vector-cheatsheet.md`; `operating-procedures/critique-pair-gate-protocol.md` (gandalf foreground authoring; cross-cutting reference skills wrapping canonical sources) |
| **Stream 3 status** | **COMPLETE.** All 6 cross-cutting skills landed (1 keystone + 5 reference wrappers). |
| **Streams 2 + 3 status** | **BOTH COMPLETE.** 10 per-agent OP skills + 6 cross-cutting skills = 16 skills total authored as Markdown sources. |
| **Skill Creator packaging pass (2026-05-23)** | **COMPLETE.** All 16 Markdown sources converted to installable Claude Code skills at `.claude/skills/<name>/SKILL.md` with YAML frontmatter (name + description with auto-load triggers + version). Project-local skill registration; Markdown sources at `operating-procedures/` remain authoritative for revisions. |
| **Stream 2 + 3 + packaging — final status** | **ALL COMPLETE.** Skills auto-load per description triggers; per-invocation read budget empirical verification queued for next session-start under skill-load discipline. |

### 2.3 Architecture-validation spike (Unreal pipeline)

| Aspect | Spec |
|---|---|
| **Owner** | Matt + knight-rider scope; specialists per integration |
| **Trigger** | Skill packaging (2.2) lands (per doc 38 § 4 step 3) |
| **Scope per doc 38 § 4.3** | JSON output → Meshy → Control Rig → Unreal → playable form with one skill. Specific acceptance criteria: clean Meshy import; Control Rig export importable into Unreal; **image-pass-through-to-Meshy validation** on 3-5 museum-tier weapons vs ChatGPT-gen comparison; Niagara consuming JSON ability-spec; PCG room generation; TAA/TSR fast-combat readability validation. |
| **Effort** | ~1-2 weeks |
| **Empirical criterion for completion** | All sub-criteria pass per § 4.3 acceptance; or specific blockers identified for follow-on resolution. |
| **Unblocks** | D1 mobile-platform reconsideration (3.2); MVP scope lock (3.3); Track M1 indirectly. |

### 2.4 Substrate P2 — axis discovery (statistical methodology)

| Aspect | Spec |
|---|---|
| **Owner** | Elrond (execution); gandalf (design intent + acceptance criterion) |
| **Trigger** | Phase D cleaning pipeline (1.1) completes |
| **Scope** | PCA / factor analysis / NMF / UMAP / t-SNE methodology selection on sparse multimodal feature matrix; variance-explained validation; axis-stability bootstrapping; interpretability scoring. **Math hotspot per Discipline #18 — legolas Mode A methodology consultation required before execution.** |
| **Empirical criterion for completion** | Axes discovered with stability metrics + interpretability scores; ready for P3 multimodal clustering as feedstock. |
| **Unblocks** | P3 multimodal clustering (2.5). |

### 2.5 Substrate P3 — multimodal clustering

| Aspect | Spec |
|---|---|
| **Owner** | Elrond (execution); gandalf (design intent + acceptance criterion) |
| **Trigger** | P2 axis discovery (2.4) completes |
| **Scope** | HDBSCAN / k-means / GMM / spectral clustering choice; silhouette + Davies-Bouldin + gap-statistic validation; multimodal-distance-metric design; cluster-count selection. **Math hotspot per Discipline #18 — legolas Mode A methodology consultation required.** |
| **Empirical criterion for completion** | Clusters produced with validation metrics; ready for P4 semantic labeling. |
| **Unblocks** | P4 cluster semantic labeling (2.6); faction architecture canonical authoring (3.4). |

### 2.6 Substrate P4 — cluster semantic labeling

| Aspect | Spec |
|---|---|
| **Owner** | Matt + gandalf (design call) |
| **Trigger** | P3 multimodal clustering (2.5) completes |
| **Scope** | Name the ~50-150 emergent clusters with design-meaningful identity. Acceptance gate: **≥80% of clusters receive a design-meaningful name within one design call**. If <80%, methodology rerun triggered (back to P2 or P3 with refined methodology). |
| **Empirical criterion for completion** | ≥80% cluster naming with confidence; cluster taxonomy ready for cohesion-judge consumption. |
| **Unblocks** | D10 Stage 1 checkpoint (3.1); cohesion-judge validation (P5); faction architecture (3.4). |

### 2.7 Engine P1 hypothesis tests (W1.20-W1.22) — Layer 7 BDI test framework

> **2026-05-25 UPDATE:** explicitly DEFERRED to v1.1 / Cycle 13+ per Option γ confirmation. Cycle 12 builds the engine (Layers 2-3-4-6) WITHOUT the BDI test framework (Layer 7). Validation at v1 ship is via design judgment + playtest; statistical hypothesis testing framework + acceptance gates fire in Cycle 13+ if/when warranted.

| Aspect | Spec |
|---|---|
| **Owner** | Gamora + jack-ryan + legolas Mode A (methodology at math hotspots) |
| **Trigger** | Cycle 12 closes + engine functional + empirical observation surfaces statistical-validation need (or by-design follow-on) |
| **Scope** | BDI H1-H5 hypothesis tests against engine-output kit_power samples + W1.20 model-fit harness + ω/τ table data structures + archive-pull interface + H8/H8.diff/H9 (per Q-A verdict + L9 addendum 2 refinement) + G1-G4 per-entry acceptance gates per T4 catalogue entry. Operates on mechanical_substrate only per L9 (cultural_tradition/lineage/period are semantic overlay; not in BDI math). |
| **Effort** | ~2-3 weeks rocket (W1.20 + W1.1-W1.11 P1 enrichment + W1.13 multi-dim convergence implementation as separate dispatches) + ~1-2 days gamora execution; plus legolas Mode A consultation BEFORE statistical methodology fires |
| **Empirical criterion for completion** | All H1-H5 hypotheses resolved (confirmed / refuted / reframed); H8/H8.diff/H9 + G1-G4 gates measured per T4 catalogue entry; diagnostic findings inform v1.1+ engine refinement work |
| **Companion docs** | `agentic_orchestration/gandalf/notes/2026-05-23-question-A-w1-13-tier-4-hypothesis-verdict.md` (mathematical framework + § 12 addendum sequencing + § 13 addendum 2 L9 substrate split refinement); `agentic_orchestration/gandalf/notes/2026-05-25-w1-13-w1-20-framing-brief.md` (SUPERSEDED but preserved as historical for this work) |

### 2.8 Substrate P5 — cohesion-judge validation

| Aspect | Spec |
|---|---|
| **Owner** | Star-lord (statistics execution); gandalf (design intent); gamora (simulation-side integration) |
| **Trigger** | P4 cluster semantic labeling (2.6) lands |
| **Scope** | LLM-as-judge calibration with statistical rigor; inter-rater reliability; significance testing; probability calibration via isotonic regression. **Math hotspot per Discipline #18 — legolas Mode A methodology consultation required.** |
| **Empirical criterion for completion** | Judge calibrated to acceptance threshold; tail-behavior reported alongside accuracy point estimates. |
| **Unblocks** | Production-grade content generation gated on validated cohesion judge. |

---

## 3. Deferred architectural commitments (gated by empirical-evidence criteria)

### 3.1 D10 Stage 1 checkpoint (Fate-genre alignment evidence)

| Aspect | Spec |
|---|---|
| **Decision deferred** | D10 Path A (tighten to isekai) vs Path B (shift framing copy) vs Path C (Fate-genre positioning) lock |
| **Empirical-evidence criterion** | P4 cluster semantic labeling completes; ≥80% of clusters express cultural-mythological-tradition identity (≥8-10 of the 13 predicted natural factions clearly clustered); spirit-guide narrative output coheres with Fate-genre register |
| **Decision authority** | Matt + gandalf design call |
| **Downstream consequence (if Path C confirms)** | Track M1 fires; faction architecture authoring opens; D10 architectural lock; doc 38 amendment; commercial-pitch material updates |
| **Downstream consequence (if Path A or B confirms instead)** | Different engine-tightening or copy-shift work fires; recognition-record doc gets amendment noting refined recognition |

### 3.2 D1 mobile-platform reconsideration

| Aspect | Spec |
|---|---|
| **Decision deferred** | D1 unchanged (PC-first + mobile port at +6mo) vs amended (simultaneous mobile + PC + console launch) vs mobile-primary (FGO model) |
| **Empirical-evidence criterion** | Architecture-validation spike (2.3) completes; Unreal mobile feasibility for ARPG depth confirmed; schedule analysis quantifies timeline impact of simultaneous-launch path (~3-6 additional calendar months estimated) |
| **Decision authority** | Matt |
| **Downstream consequence (if Path 2 — simultaneous launch)** | D1 amendment; timeline floor revised (~260-320 effective days, ~13-18 calendar months); mobile UI architecture acceleration; cross-platform infrastructure work fires |
| **Downstream consequence (if Path 1 — unchanged)** | Original D1 holds; mobile work remains at +6mo |

### 3.3 MVP scope lock

| Aspect | Spec |
|---|---|
| **Decision deferred** | Specific roster size, season count for launch, feature inclusion list, monetization model |
| **Empirical-evidence criterion** | D10 Stage 1 (3.1) resolves + architecture-validation spike (2.3) completes |
| **Decision authority** | Matt + gandalf + jack-ryan |
| **Downstream consequence** | All scope-creep candidates gated against this lock; jack-ryan enforces lock at milestones; ship-discipline anchor |

### 3.4 Faction architecture canonical doc

| Aspect | Spec |
|---|---|
| **Decision deferred** | Faction model specifics (allegiance fluidity; faction-coherent kit pools; Rift Event PVE/PVP framework; cross-faction summoning rules) |
| **Empirical-evidence criterion** | P3 multimodal clustering (2.5) validates faction-equivalent clusters; P4 cluster semantic labeling (2.6) names them; ≥8-10 of the 13 predicted natural factions clearly expressed |
| **Decision authority** | Matt + gandalf design call |
| **Downstream consequence** | Faction architecture canonical doc authored; integration with seasonal cadence design; Rift Event design scoped |

### 3.5 Three-tier branding lock ("Reincarnation War" franchise banner)

| Aspect | Spec |
|---|---|
| **Decision deferred** | Franchise banner ("Reincarnation War" vs "Spirit War" vs other); season-instance title; event-level naming pattern |
| **Empirical-evidence criterion** | Title-IP search completes (no blocking trademarks/conflicts); marketing director re-validation; D10 Stage 1 (3.1) confirms Fate-genre alignment |
| **Decision authority** | Matt |
| **Downstream consequence** | Branding canonical doc authored; marketing positioning lock; commercial-pitch material updates |

### 3.6 Track M1 — mythological-named-weapons substrate import

| Aspect | Spec |
|---|---|
| **Decision deferred** | Whether to fire Track M1 (estimated 2-3 day hive-mind cycle; 200-500 named-mythological-weapons entries) |
| **Empirical-evidence criterion** | D10 Stage 1 (3.1) confirms Fate-genre alignment; Phase D cleaning (1.1) complete; substrate ready for layered enrichment |
| **Decision authority** | Matt + gandalf + knight-rider dispatch |
| **Downstream consequence (if fires)** | Named-mythological substrate joined to existing weapon_knowledge_entries; faction-anchor objects available to cohesion judge; spirit-guide narrative templates can surface named-mythological echoes per form |
| **Placeholder usage in meantime** | Ad-hoc named-mythological references in in-flight design work (form-library concept notes, season concept docs, spirit-guide narrative drafts) are fine. These get bound to actual substrate rows when M1 lands. Standard refactor pattern. |

### 3.7 Monetization model

| Aspect | Spec |
|---|---|
| **Decision deferred** | Premium vs F2P vs hybrid; expansion pricing; mobile-port monetization model |
| **Empirical-evidence criterion** | First playable vertical-slice demo lands; MVP scope lock (3.3) resolves; market-test feedback if applicable |
| **Decision authority** | Matt |
| **Downstream consequence** | Monetization integration architected into game systems before MVP scope freeze |

### 3.8 Weapon-substrate v1.1+ refinement queue (post-ship substrate-refinement; deferred per Matt 2026-05-23)

| Aspect | Spec |
|---|---|
| **Decision deferred** | Substrate-tagging-discipline refinement work + targeted rare-lineage substrate expansion. Originally surfaced as Cycle 9.10-9.14 sub-carries (**9.11-C** east_asian period_unknown curation; **9.11-D** substrate-tagging-artifact review across ~15-25 affected clusters; **9.11-E** cultural-vs-geographic tagging discipline canonicalization; **9.10-E** substrate expansion via targeted marginal-lineage crawls; **9.11-B SUBSUMED into 9.10-E** per Matt decision 3 — single unified v1.1+ dispatch covers all 5 marginal lineages). All deferred to v1.1+ post-ship queue per Matt 2026-05-23 three-decision relay. |
| **Empirical-evidence criterion** | One of: (1) P4 cluster semantic labeling (§ 2.6) completes + faction-coherence assessment surfaces Mode B/C/D contamination as downstream design-quality blocker → fire 9.11-D + 9.11-E; (2) D10 Path C architectural commitment is made (per § 3.1) AND substrate-coverage gaps surface as faction-architecture blockers → fire 9.10-E (substrate expansion subsumes 9.11-B); (3) Engine consumption work (cohesion judge; spirit-guide narrative) surfaces specific Mode B/C/D contamination cases that Discipline #25 rep-audit cannot handle at consumption → fire targeted relabel sub-dispatches; (4) Post-ship player-facing feedback indicates substrate-quality issues affecting player experience → fire prioritized refinement queue |
| **Decision authority** | Matt (substrate-cleaning scope re-engagement); gandalf (semantic-layer cultural-tradition-vs-geographic-origin discipline canonicalization); jack-ryan (Discipline #25 ratification refinements if needed) |
| **Downstream consequence (if any path fires)** | 9.11-D → 9.11-E → mesoamerican re-tag-then-re-cluster smoke order per gandalf 9.11-G meta-record recommendation. Substrate-tagging cleaning policy refinement may surface as new working-agreement amendments. Post-cleaning re-cluster may emit new Phase E-1.x outputs requiring follow-on P4 labeling pass. |
| **Until trigger fires** | Discipline #25 (semantic-layer rep-audit) handles substrate contamination at consumption per engineering-disciplines.md canonical (jack-ryan canonical write commit `1fae3fa` engine repo). Downstream design surfaces (gandalf at T4-B substrate-anchoring; P4 cluster semantic labeling; cohesion judge; spirit-guide narrative output) apply rep-audit at every semantic-inheritance decision. Substrate contamination from Modes B/C/D (geographic-origin / naming-allusion / cross-tagged-error per marginal-lineage meta-record) does NOT block downstream work. |
| **Authoritative conclusion-declaration** | `canonical/story/2026-05-23-weapon-substrate-conclusion-declaration.md` (knight-rider authored per Matt decision relayed via gandalf 2026-05-23) |

---

## 4.0 QD-engine 8-phase workflow mapping (v1-engine-scope clarification — added 2026-05-25)

Per `canonical/story/qd-engine-end-to-end-workflow-2026-05-24.md`, the QD-engine runtime pipeline has 8 phases. This table maps each phase to its v1-scope status + Cycle 12 Layer coverage + downstream work:

| QD-engine Phase | Description | v1 status | Coverage |
|---|---|---|---|
| **Phase 1 — Archive Inspection** | Substrate query layer (v1_scope flag + composition policy substrate-pool selection) | ✅ EXISTS in legacy + DB infrastructure | Cycle 10 closed substrate; queryable now |
| **Phase 2 — BC-Target Generation** | Kit identity production (BC-target cell sampler + Architecture B substrate-binding + skill content assembly) | ⏳ **Cycle 12 Layer 2 + Layer 3** | Wave 1 COMPLETE 2026-05-25; tests PASS |
| **Phase 3 — Convergence / Measurement** | W1.13 multi-dim convergence (per math note v1.1; 5-6 dimensions) | ⏳ **Cycle 12 Layer 4** | Wave 3 queued; fires after Wave 2 (Gate-2-on-L2 + MC-3) lands |
| **Phase 4 — Insertion** | Post-generation insertion into archive | ✅ EXISTS in legacy; may need minor amendment per new engine layer integration | Phase 4 simplified archive math spec QUEUED for gandalf canonical authoring (~30-45 min) |
| **Phase 5 — Cohesion Coalescence** | LLM-runtime naming + sub-element manifestation per substrate-tradition (cohesion-judge naming discipline) | ⚠️ EXISTS in legacy; calibration spec QUEUED | Phase 5 cohesion-judge calibration spec QUEUED for gandalf canonical authoring (~1 hr); legolas Mode A consult required first per Discipline #18 |
| **Phase 6 — Visual Coalescence** | Image generation (Meshy integration + image-pass-through vs LLM-description path per Cycle 10 Sidecar A finding) | ✅ EXISTS-PARTIAL | Sidecar A verdict landed Cycle 10; Phase 6 production wire-up pending |
| **Phase 7 — Joint-Gate** | Final per-form acceptance gate (Phase 5 + Phase 6 outputs jointly evaluated) | ⚠️ MAY EXIST in legacy; specifics need verification | Status unclear — possibly fires implicitly via existing acceptance criteria; explicit Phase 7 spec authoring may be needed for new engine |
| **Phase 8 — Profile Assembly** | Final kit assembly into shipped form (kit + name + visual + skill tree + T4 keystone alteration via Cycle 12 Layer 6 wire-up) | ⏳ **Cycle 12 Layer 6 adds T4 wire-up** | Wave 4 queued; alterations reach combat arithmetic via new engine layers per L9 opportunity-scan refactor |

**v1-engine-scope summary:**
- **Cycle 12 covers:** Phase 2 (Layers 2+3) + Phase 3 (Layer 4) + Phase 8 partial (Layer 6 T4 wire-up). Approximately 50% of the 8-phase pipeline.
- **Already exists (legacy):** Phase 1 (Archive Inspection), Phase 4 (Insertion), Phase 5 (Cohesion Coalescence — calibration spec pending), Phase 6 (Visual Coalescence partial via Sidecar A).
- **Status unclear (Phase 7 Joint-Gate):** may exist implicitly; explicit spec authoring may be needed.
- **Engine-side post-Cycle-12 to v1 ship:** Phase 4 archive math spec (gandalf ~30-45 min) + Phase 5 cohesion-judge calibration spec (gandalf ~1 hr + legolas Mode A consult) + Phase 7 verification (assess vs author) + T4 post-mortem session(s) (Matt + gandalf ~1-2 sessions of 1-2 hours each) + loadout app M1/M2/M5 finishing (drax + star-lord ~2-3 days; may be absorbed into Cycle 12 work).

**"v1 ship" depends on scope definition** (per gandalf 2026-05-25 dialogue):
- **Narrow (engine v1):** Cycle 12 closes + Phase 4/5/7 spec gaps closed + T4 post-mortem + loadout finishing = **~1-2 weeks post-Cycle-12**
- **Broad (game v1 with playable demo):** Narrow + MVP scope lock + trial-boss-gallery + vertical-slice playable demo = **~2-3 months post-Cycle-12**
- **Wide (Reincarnated game playable for son):** Broad + Earth meta-layer + actual play loops + season-as-life-narrative + balance polish = **~6-12 months post-Cycle-12**

The narrow/broad/wide scope question is itself a deferred decision (MVP scope lock per § 3.3) that fires post-Cycle-12 close.

---

## 4. Roadmap sequence (dependency view)

```
[ACTIVE — RIGHT NOW]
    Phase D cleaning (elrond)  ←  hive-mind state Cycle 9
    Canonical restructure (knight-rider sub-agent, background)
    Documentation cleanup continuation (gandalf, foreground)

         ↓ Phase D cleaning completes

[QUEUED — SUBSTRATE TRACK]
    P2 axis discovery (elrond + gandalf + legolas Mode A)
         ↓ Discipline #18 methodology consult → execute
    P3 multimodal clustering (elrond + gandalf + legolas Mode A)
         ↓ Discipline #18 methodology consult → execute
    P4 cluster semantic labeling (Matt + gandalf design call)
         ↓ ≥80% nameable clusters acceptance
    P5 cohesion-judge validation (star-lord + gandalf + gamora + legolas Mode A)

         ↓ P4 cluster labeling completes

[GATED — D10 STAGE 1 CHECKPOINT]
    Fate-genre alignment evidence reviewed
         ↓ if confirmed: Path C lock + downstream amendments fire

[POST-CHECKPOINT — ARCHITECTURE TRACK]
    Track M1 mythological-named-weapons substrate import (legolas + elrond)
    Faction architecture canonical doc (gandalf + Matt)
    Three-tier branding lock (Matt)
    D10 architectural amendment (gandalf)
    Commercial-pitch material updates

[PARALLEL — OPERATIONAL TRACK]
    Skill_handoff reframing (jack-ryan + knight-rider)
    Per-agent operating-procedure skills (multi-agent coordination)
    Architecture-validation spike (Matt + specialists)
         ↓ schedule + Unreal mobile feasibility
    D1 mobile-platform decision

[PARALLEL — ENGINE TRACK]
    Engine P1 hypothesis tests W1.20-W1.22 (gamora + jack-ryan)
    Engine P1 substrate enrichment (rocket + gandalf design-spec-as-math)

[POST-ALL-ABOVE — SHIP TRACK]
    MVP scope lock (Matt + gandalf + jack-ryan)
    Trial-boss-gallery roster (gandalf + Matt)
    Monetization model (Matt)
    Player-facing copy for continuity architecture (gandalf)
    Vertical-slice playable demo
    ...
```

---

## 5. What this doc does NOT decide

Out of scope for the roadmap; lives in other canonical authorship or specialist decisions:

- **Specific Unreal engine implementation choices** (Blueprint vs C++ boundary, plugin selection, asset-import-automation specifics) — owned by architecture-validation-spike outcomes
- **Specific cluster naming language** at P4 — owned by Matt + gandalf design call when P4 fires
- **Specific weapon-substrate per-row decisions** (which weapons to feature; which forms get which signature weapons) — owned by post-P4 form-library design work
- **Specific mythology selection for M1** (which traditions to import deeply vs lightly) — owned by post-Stage-1 M1 dispatch authoring
- **Specific monetization tier structure** (price points, F2P balancing, mobile-store positioning) — owned by post-MVP-scope-lock monetization design
- **Specific MVP roster size** — owned by post-Stage-1 scope-lock work
- **Provisional patent application timing** — Matt's domain (independent of dev roadmap)
- **Engineering disciplines** — jack-ryan's territory; lives in `engineering-disciplines.md`
- **Per-agent operating-procedure specifics** — owned by each agent authoring their own when 2.2 fires

---

## 6. How this doc gets updated

This is a **living doc**. Update triggers:

- **A workstream enters Active or moves between phases** — update § 1
- **An empirical-evidence criterion resolves and unblocks a deferred decision** — move from § 3 to § 1 or § 2; mark the dependency landscape change
- **A new workstream surfaces (from Matt direction or discovered need)** — add to § 2 or § 3 with explicit empirical-evidence criterion
- **An architectural commitment fires** — update § 3 to reflect lock; cross-reference the downstream canonical doc; mark the dependency change
- **A workstream completes** — strike from § 1; cross-reference completion artifact in § 6

Authored / maintained by **gandalf** (story-and-design steward). Knight-rider can update when workstream state shifts during orchestration.

---

## 7. Cross-references

### Active project canon this roadmap depends on
- `canonical/00-ground-state.md` — ground-state oracle
- `canonical/37-engine-and-game-two-products.md` — Variant C lock
- `canonical/38-downstream-delivery-strategy-2026-05-23.md` — D1-D10 delivery strategy
- `canonical/story/fate-genre-recognition-and-mobile-alignment-trajectory-2026-05-23.md` — recognition record
- `canonical/story/legacy-categorical-cleanup-audit-2026-05-22.md` — Pattern 4-5-6 retirements
- `canonical/story/hive-mind-protocol-weapon-library-import-2026-05-22.md` — substrate P-series
- `canonical/story/hive-mind-protocol-qd-engine-rebuild-2026-05-21.md` — engine P-series
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — 20 disciplines (including #18 methodology-before-execution + #11 empirical inspection)
- `~/Games/reincarnated-engine/design/decisions/decisions-log.md` — temporal decisions log

### Live state references
- `agentic_orchestration/weapon-library-import-hive-mind-state.md` — current hive-mind state
- `agentic_orchestration/weapon-library-import-wind-down-summary-2026-05-22.md` — 89,839-row substrate baseline

### Predecessor (HISTORICAL)
- `canonical/historical/16-project-roadmap.md` (formerly `canonical/16-project-roadmap.md`) — A-series roadmap; predates QD-rebuild + vast-library pivot + D1-D10 lock; consulted for lineage only

### Downstream artifacts this roadmap anchors
- Future workstream-specific dispatches (knight-rider authors per active workstream entries)
- Future architectural amendments (gated by § 3 empirical-evidence criteria)
- Future MVP scope lock canonical doc (post-Stage-1)
- Future faction architecture canonical doc (post-P3 + P4)
- Future monetization model canonical doc (post-MVP-scope-lock)

---

## 8. Sign-off

**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-05-23 — confirmed during cleanup-pass session
**Status:** CURRENT — living doc; updated as workstream state evolves
**Maintenance:** gandalf authors + maintains; knight-rider updates when workstream state shifts during orchestration

**For:** the canonical record of the workstream sequencing, empirical-evidence-gated commitments, and active/queued/deferred status of Reincarnated's downstream work as of 2026-05-23. Supersedes A-series roadmap framing per the QD-rebuild + vast-library + D1-D10 + Fate-genre-recognition trajectory.
