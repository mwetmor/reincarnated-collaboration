# Pi-Hosted LLM API Proxy Architecture — Recognition Record

> **STATUS:** CURRENT (recognition record; architectural commitments deferred per § 4 empirical-evidence triggers) — Matt 2026-05-30 design conversation surfaced the design intent of centralizing all LLM API calls on the Pi as a single source of truth for API keys + logs + cost tracking + caching. PRESERVED as design intent for later Pattern-B engagement; full commitment depends on Pi Phase 2 HTTP API maturity.

**Date:** 2026-05-30
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-05-30 verbatim — "we should also preserve the LLM API calls idea to move to the Pi as a topic for later"
**Companion docs:**
- `canonical/story/2026-05-30-pi-middleware-mac-to-pc-architecture.md` — canonical commitment for Pi-middleware infrastructure
- `canonical/story/2026-05-30-pi-engine-control-dashboard-recognition.md` — companion recognition record (dashboard control plane)
- `agentic_orchestration/gandalf/notes/2026-05-30-physical-infrastructure-implementation-plan.html` — exhaustive HTML implementation plan
- Prior Pi recognition record (Matt 2026-05-25 D1 ratified + D9 DEFERRED) per `MEMORY.md` user-role + project-state files
- `canonical/00-ground-state.md` — will register new CURRENT entry on commit

---

## 0. TL;DR

Centralize all LLM API calls (Anthropic + OpenAI + future providers) through a Pi-hosted FastAPI proxy service. Unified API key management, unified cost tracking (canonical accountant for $50 monthly soft cap), unified request/response logging (PostgreSQL), unified caching (revives D9 LLM cache from Matt 2026-05-25 deferral). Cross-machine: Mac fires now, PC fires from Unreal in Phase 2+, future-dashboard fires from anywhere. Mac removes API keys; Pi holds them.

**LLM naming object coverage** (Matt 2026-05-30 list + gandalf additions):
- ✅ Seasons (Wave-S)
- ✅ Factions (Wave A)
- ✅ Characters (Wave B)
- ✅ Faction relationships (Wave F-C)
- 🔮 Skills (Cycle 15+ if pursued; not currently LLM-named)
- 🔮 Legendary weapons + sets (Cycle 15+ Wave 4)
- 🔮 Spirit-guide narration (Cycle 15+ if pursued)
- 🔮 Hidden-Spirit-Discovery dialog (Cycle 16+ if § 23 advances)

This doc preserves the architectural commitment as deferred; implementation gates on Pi Phase 2 HTTP API readiness + Pattern-B design session.

---

## 1. Architectural shape (preliminary)

### 1.1 Pi-side endpoint family

Pi FastAPI service (same service as Phase 2 data API; separate endpoint family):

```
POST /llm/v1/wave-a/faction-naming
POST /llm/v1/wave-s/season-naming
POST /llm/v1/wave-b/character-naming
POST /llm/v1/wave-fc/faction-relationships
POST /llm/v1/wave-4/legendary-naming         (Cycle 15+; gated on Wave 4)
POST /llm/v1/wave-4/set-naming                (Cycle 15+; gated on Wave 4)
POST /llm/v1/skill-naming                     (Cycle 15+; gated on design call)
POST /llm/v1/spirit-guide-narration           (Cycle 15+ if pursued)
GET  /llm/v1/cost/current-period              Current $ usage vs $50 cap
GET  /llm/v1/cost/per-surface                 Breakdown by Wave A/S/B/FC/etc.
GET  /llm/v1/cache/stats                      Cache hit rate per surface
GET  /llm/v1/calls/recent                     Recent call log (last N)
POST /llm/v1/cache/invalidate                 Clear cache for specific surface
```

### 1.2 Pi-side architecture

| Component | Responsibility |
|---|---|
| **API key store** | Anthropic + OpenAI + future provider keys in Pi env vars (NOT git, NOT Mac, NOT PC); secrets management discipline |
| **PostgreSQL `llm_calls` table** | Per-call log: request hash + model + temperature + max_tokens + response + cost_usd + duration_ms + timestamp + source_machine + source_seam (star-lord / drax / etc.) + season_id (if applicable) |
| **PostgreSQL `llm_cache` table** | Request hash → cached response (TTL configurable per surface; cost-amortizing retroactive replay) |
| **Cost-cap enforcement** | Pi refuses calls above configured monthly threshold (default $50 per cascade-r3 Amendment 8 + Amendment 4 surface conditions); banner surfaces to clients at 75% threshold |
| **Rate-limit** | Per-surface RPM limits (don't accidentally fire 1000 Wave B calls in 60 sec) |
| **Structured logging** | journald + access log; queryable for cost forensics + cache hit analysis + per-cycle attribution |
| **Health endpoint** | `GET /llm/v1/health` returns API key validity + provider availability + cache stats |

### 1.3 Mac-side migration

- star-lord's emit pipeline `tracked_client` + `cache.py` refactored to **thin client of Pi proxy** (HTTP calls to Pi instead of direct Anthropic SDK calls)
- Anthropic + OpenAI API keys REMOVED from Mac env vars and project settings
- Local LLM cache layer on Mac REMOVED (moved to Pi PostgreSQL)
- star-lord MIGRATION.md captures the seam refactor under §v1.72 candidate
- Backward compat: optional fallback to direct provider call if Pi unreachable (controlled by env var; off by default to enforce single source of truth)

### 1.4 PC-side integration (Phase 2+)

- PC's Unreal-side HTTP client (VaRest plugin per drax dispatch) consumes Pi LLM endpoints when Unreal needs LLM (runtime narrative generation, character creation dialog, etc.)
- No API keys on PC
- Unified cost tracking includes PC-originated calls
- Schema versioning per endpoint protects PC client from breaking changes

### 1.5 Future-dashboard integration

When Phase β control plane (per companion recognition record) lands, dashboard exposes LLM cost surface as a top-level KPI tile and per-cycle cost breakdown. Dashboard control buttons that fire LLM-bearing operations show the cost preflight estimate before firing.

---

## 2. Composition with existing canon

### 2.1 Composes with augmentation-not-replacement principle

Per `canonical/story/2026-05-30-pi-middleware-mac-to-pc-architecture.md` § 1.2: Pi handles cross-machine concerns. LLM access IS canonically cross-machine (Mac fires now, PC fires in Phase 2+, dashboard fires later). Pi-hosted proxy is the architecturally honest path.

### 2.2 Revives D9 (LLM cache) from Matt 2026-05-25 deferral

Per `MEMORY.md` Pi recognition record: D9 LLM cache was DEFERRED 2026-05-25 ("G12 NOT TRIGGERED"). The deferral was contingent on architectural readiness. Centralizing LLM on Pi creates the natural home for the cache — same service, same DB, queryable for hit-rate analytics, retroactive-replay-capable. **D9 revival composes with this recognition record's commitment.**

### 2.3 Composes with cascade-r3 Amendment 8 $50 soft cap discipline

Per `agentic_orchestration/gandalf/notes/2026-05-29-cascade-resumption-3-class-eradication-authorization.md` Amendment 8: $50 soft cap re-imposed as primary cost gate. Centralization makes Pi the **canonical accountant** enforcing the cap. Currently cost monitoring is per-cycle ad-hoc; Pi proxy makes it continuous + queryable + enforceable.

### 2.4 Composes with Wave-S retroactive backfill problem

Per cascade-r4 follow-on Wave-S work (Matt 2026-05-29 "did I see that these seasons did not produce LLM names for our characters and for the season itself? Can we implement retroactive LLM naming across these gaps?"): the gap recovery required ~$1 of re-fire because original Wave B responses were not cached at request level. **With Pi LLM proxy + cache, the same recovery would have been ~$0 via cache replay.** This is concrete empirical motivation for the proxy.

### 2.5 Composes with cumulative Disc #42a Instance 6 pattern

The "engine-emit-pipeline-scope-bounded-narrower-than-engine-emission" sub-discipline pattern (4 surfaces in 48 hours) has a parallel at the LLM seam: "engine fires LLM but result not cached + not centrally tracked + cost not enforced at fire time." Pi LLM proxy is the architectural fix for this pattern at the LLM seam.

### 2.6 Composes with Pi Phase 2 HTTP API expansion

Original Phase 2 scope: data API for Unreal queries. Phase 2 now expands to include **three endpoint families**:
1. Data API (original)
2. Control plane (per dashboard recognition record)
3. LLM proxy (this doc)

Together, Pi Phase 2 becomes the **architectural pivot point of the whole rollout** — Pi shifts from "file share" to "cross-machine application layer."

### 2.7 Composes with future Hidden-Spirit-Discovery dialog generation

Per HTML engine-analysis § 23: Hidden-Spirit-Discovery character creation surface. If § 23 advances to canonical commitment, the discovery interaction generates real-time LLM dialog (spirit-guide narration during gesture interaction). Pi LLM proxy is the natural fire path — Mac generates substrate, Pi serves LLM dialog to player surface in real-time.

---

## 3. Cost + risk considerations

### 3.1 Cost implications

| Concern | Analysis |
|---|---|
| **Latency overhead** | Mac → Pi → Anthropic vs direct Mac → Anthropic adds ~50-200ms per call. For batch operations (Wave B 30-50 calls), this is ~3-10sec total — not material relative to Anthropic's own response latency (~1-5sec per call). |
| **Pi as critical path** | If Pi down, LLM-bearing operations fail. Mitigation: optional fallback flag (off by default) to enable direct provider call when Pi unreachable. Pi reliability tracked per Phase 1 acceptance. |
| **Single API key bottleneck** | If Pi compromised, all keys at risk. Mitigation: Pi LAN-only (no internet exposure); key rotation discipline; structured logging for forensics. |
| **Cost forensics** | Currently per-cycle ad-hoc tracking. Pi proxy makes it continuous (`SELECT SUM(cost_usd) FROM llm_calls WHERE date_trunc('month', timestamp) = current_period`). Net win. |
| **Cache hit rate gains** | Wave-S retroactive backfill cost was ~$1; with cache replay, ~$0. Across cycles, cache hit rate compounds. Material long-term savings on $50 monthly cap. |

### 3.2 Operational risks

- Pi being single point of failure for LLM access (mitigated by fallback flag + Pi reliability tracking)
- Schema breakage between client and Pi proxy (mitigated by schema versioning per endpoint)
- Cache staleness (mitigated by TTL configuration + manual invalidation endpoint)
- Cost-cap enforcement edge cases (e.g., partial run when cap reached mid-cascade; needs design call)

---

## 4. Empirical-evidence triggers for canonical-promotion

Per recognition-validate-commit discipline (Disc #21):

1. **Pi Phase 1 + Phase 2 baseline operational** — file share working + data API endpoints serving real queries
2. **Pattern-B design session** with Matt on LLM proxy spec — auth model, cache TTL per surface, cost-cap edge cases, fallback semantics
3. **Star-lord readiness assessment** — `tracked_client` + `cache.py` refactor scope estimate (likely ~1-2 day star-lord work; modest)
4. **Empirical evidence of pain point** — current Wave-S retroactive backfill experience already validates the cost-amortization argument; additional triggers could surface (e.g., cost forensics gap discovered during wave-close consolidation)

When triggers 1-4 satisfied, Pi LLM proxy moves from recognition record to canonical-promotion candidate. **Expected canonical doc:** `canonical/story/YYYY-MM-DD-pi-llm-proxy-architecture.md` (full architectural commitment).

---

## 5. Sign-off

**Authored:** gandalf (story-and-design steward) per Matt 2026-05-30 verbatim "we should also preserve the LLM API calls idea to move to the Pi as a topic for later."

**For:** durable preservation of the Pi-hosted LLM API proxy architectural intent at canonical layer so that future Pattern-B engagement has a substrate to consume. Implementation deferred per § 4 empirical-evidence triggers; primary gate is Pi Phase 2 HTTP API readiness + Pattern-B design session.

**Composition with companion recognition record (dashboard):** both this doc + dashboard recognition record expand Pi Phase 2 scope substantively. Together they make Pi Phase 2 the architectural pivot point of the rollout — Pi shifts from "file share + data API" to "cross-machine application layer with control plane, LLM proxy, and dashboard surface." Worth Pattern-B engagement when both surface together as canonical-promotion candidates.

**For Matt + Pi work in parallel:** this recognition record lives in canon while Matt does Phase 1 physical setup. Returns to active design conversation when Pi Phase 1 closes + Pattern-B fires.
