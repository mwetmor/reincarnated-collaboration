# Immediate-Arc Workstream Queue (Strategic Reset 2026-06-01)

**STATUS:** ACTIVE (immediate-arc workstream tracker; strategic reset from post-Q18 long-arc queue)
**Date:** 2026-06-01
**Author:** knight-rider (orchestrator)
**Authority:** Matt 2026-06-01 strategic reset directive (transmitted via gandalf Pattern B reframe; "agree with the above") — narrower IMMEDIATE-ARC focus supersedes long-arc post-Q18 queue
**Composes with:**
- `agentic_orchestration/post-q18-workstream-queue-2026-06-01.md` (long-arc queue; explicitly DEFERRED per strategic reset; not cancelled — preserved as deferred-commitments)
- `gandalf/notes/2026-06-01-q18-deferred-commitments.md` (deferred-commitments record; preserved)
- `canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md` (architectural LOCK; preserved unchanged)

---

## 0. Strategic goal

Generate a season + ensure magic weapons across periods + drax loads generated season into Vercel apps.

**Total horizon:** ~6-10 sessions to "season generated + magic weapons across periods + visible in Vercel apps".

---

## 1. Architectural state PRESERVED (unchanged)

- WS1A.Q18 Architecture A LOCK (109 entries; canonical lock)
- pool.json v1.1 migrated state (100 rotating + 114 legacy preserved-quarantined; physical_taxonomy.json 9 entries; schema extended with 4 additive fields)
- WS1.AP / WS1.AP-FU amendment-pass cleanups (cardinality + lineage aggregate + stormtide annotation + § 7.1 shadow-row fix all closed)
- Disciplines #49 / #50 / #51 ratified
- WS2.P1 modern-caster substrate-coverage audit (data preserved; informs MODERN portion of IA-2 broader audit)
- Hypothesis-flow pattern-library architecture canonical
- Deferred-commitments record (preserved; theme-coherence gating + modern-caster-coverage gap remain RECOGNIZED; activation deferred)

---

## 2. Workstreams DEFERRED (not in immediate-arc scope; preserved as deferred-commitments)

| WS | Disposition | Notes |
|---|---|---|
| **WS2.P2** modern-caster-only manual authoring | ABSORBED INTO IA-2 broader scope | WS2.P1 audit data preserved as MODERN-period input |
| **WS3** sub-element mapping | DEFERRED | Long-arc; not load-bearing for immediate goal |
| **WS4** full engine gen refresh / Manifestation Milestone Phase 1 | DEFERRED | Long-arc; not load-bearing for immediate goal |
| **Q16 / Q17 / Q19** WS1A hard-blocker waves | DEFERRED | Architecture for full identity finalization; not load-bearing for "season with LLM-named skills" |
| **WS1A.3 / WS1A.4** implementation | DEFERRED | |
| **vfx_coverage_manifest.json** extension | DEFERRED | Engine-rendering concern; not load-bearing for data generation or Vercel display |

**Post-immediate-arc re-engagement:** After IA-1 V2 + IA-2 + IA-3 land (V2 season visible in Vercel apps), Matt + gandalf re-engage to decide long-arc reactivation vs continue iterating immediate-arc vs pivot direction.

---

## 3. IMMEDIATE-ARC priorities (3 workstreams)

### IA-1 — Engine season generation V1 (baseline fire)

| Property | Value |
|---|---|
| **Owner** | rocket + star-lord (engine seam; coordination) |
| **Authorization** | ✅ AUTHORIZED to fire pending engine-readiness confirmation |
| **Estimated horizon** | 1-3 sessions |
| **Pre-fire** | Engine-readiness assessment to rocket + star-lord; on confirmation, fire V1 baseline generation |
| **Scope** | Run engine's existing Phase 5+ pipeline against current substrate (post-Q18-lock pool.json v1.1 + existing weapon substrate). Produce new season output with LLM-named skills using current Phase 5 cohesion-judge + skill-naming + faction-naming pipeline. NO Q16/Q17/Q19 or WS1A.3/4 architecture required — engine uses existing prompt design. Q18 vocabulary available as substrate; engine consumes for naming context without bounded-judgment infrastructure. |
| **Output** | New season JSON artifact (becomes input substrate for IA-2 gap analysis + IA-3 drax loading) |

### IA-2 — Magic weapons across periods audit + gap-fill

| Property | Value |
|---|---|
| **Owner** | elrond Mode A audit + gandalf authoring + legolas Mode B crawl supplementary (Y3 hybrid path) |
| **Authorization** | ✅ AUTHORIZED to fire (BROADER scope than WS2.P2) |
| **Estimated horizon** | ~3-5 sessions across 4 phases |

**Phase 1 — Magic-weapons-across-periods substrate audit** (~1-2 sessions)
- Query 89,839-row substrate for MAGIC weapon coverage per period:
  - **ANCIENT period:** Bronze Age myth weapons, Antiquity legendary, mythological/divine artifacts (Mjolnir / Excalibur / Gae Bolg / Vajra / Trishula / etc.)
  - **MEDIEVAL period:** enchanted swords, witch staves, alchemist rods, runed weapons, grimoire-bound focuses, named legendary (Joyeuse / Durendal / Hauteclere / etc.)
  - **MODERN period:** incorporate WS2.P1 modern-caster audit data (uniformly thin coverage across 7 primaries; ~45-67 weapons scope confirmed)
- Report per-period × per-primary coverage state + gap quantified

**Phase 2 — Gap-fill (Y3 hybrid)** (~2-3 sessions)
- Gandalf manually authors anchor weapons per period × primary (~5-7 per cell where coverage thin = ~20-30 anchors)
- Legolas commissions catalog crawl for supplementary coverage across ANCIENT + MEDIEVAL + MODERN magic weapon canon (~30-50 supplementary entries)
- Total scope: ~45-80 weapons across 3 periods × 7 primaries

**Phase 3 — Elrond ingest + lineage tag application** (~0.5 session)
- Schema: `substrate_validation_lineage` tag values:
  - `gandalf-authored-magic-anchor-ancient-2026-06-XX`
  - `gandalf-authored-magic-anchor-medieval-2026-06-XX`
  - `gandalf-authored-magic-anchor-modern-2026-06-XX`
  - `legolas-crawl-magic-supplementary-{period}-2026-06-XX`

**Phase 4 — Substrate-coverage validation pass** (~0.5 session)
- Re-run audit query post-ingest; confirm gap closure

**Output:** substrate populated with magic weapons across 3 periods

### IA-3 — Drax integration (load generated season into Vercel)

| Property | Value |
|---|---|
| **Owner** | drax (reincarnated-loadout React/Vite/Tailwind + reincarnated-demo Pixi.js engine page) + star-lord output pipeline coordination |
| **Authorization** | ✅ AUTHORIZED to open (new drax workstream) |
| **Estimated horizon** | 2-4 sessions across 4 phases |

**Phase 1 — Drax workstream open:** consume IA-1 V1 season output as test substrate; build/refine loadout page data-loading layer + engine page data-loading layer

**Phase 2 — Integration:** drax loads season output into:
- reincarnated-loadout loadout pages (React components consume season JSON; render kits + skills + weapons + factions)
- reincarnated-demo engine page (Pixi.js components consume season JSON; render gameplay-adjacent data)

**Phase 3 — Vercel deployment:** deploy updated loadout + demo apps to Vercel preview environments

**Phase 4 — Iterate with IA-1 V2 season output:** post-IA-2 gap-fill; drax re-loads with improved substrate

**Output:** new season visible in Vercel-deployed loadout + engine pages

---

## 4. Sequencing (parallel-where-possible)

**Phase 1 (parallel fire):**
- IA-1 V1 baseline season generation (rocket + star-lord)
- IA-2 Phase 1 magic-weapons-across-periods audit (elrond)

**Phase 2 (parallel; uses Phase 1 outputs):**
- IA-2 Phase 2-3 magic-weapons gap-fill (gandalf + legolas + elrond)
- IA-3 Phase 1-2 drax workstream open + V1 integration scaffolding

**Phase 3 (sequential):**
- IA-2 Phase 4 substrate-coverage validation
- IA-1 V2 re-fire with improved substrate
- IA-3 Phase 3-4 deploy + iterate with V2

---

## 5. Workstream status table

| WS | Phase | Status | Notes |
|---|---|---|---|
| **IA-1** V1 baseline season generation | V1 FIRE | ✅ **SUCCESS** — season_000042 generated (engine sha `cda99a5`; 1728.7s; validation PASSED; 5 classes all converged 4/5 in target band; 44 monsters; 200 gear; 49.33% trial defeat target 50%; LLM-named cosmological_vocab with 8 slot fills + 3 pair rationales coalesced theme="forge"; star-lord close-summary deferred — KR orchestration close record at `ia-1-v1-close-record-2026-06-01.md` substitutes) | Engine artifacts at `~/Games/reincarnated-engine/seasons/season_000042/` |
| **IA-2.P1** Magic-weapons-across-periods audit | Phase 1 audit | ✅ COMPLETE (commit `1160333`) — 21-cell grid: ANCIENT mostly WEAK-MEDIUM with earth STRONG(38)/holy STRONG(30); MEDIEVAL mostly WEAK with shadow ABSENT(1) worst cell; MODERN ABSENT/WEAK per WS2.P1; coverage asymmetry ANCIENT>>MEDIEVAL~MODERN; fire/water uniformly thin cross-period; Phase 2 scope **~80-100 weapons mid-range** (gandalf 67-88 manual + legolas 22 crawl); within LOCK C ~140 cap; **Retroactive-primary-tagging surfaced** as Phase 3 methodology consideration; no escalation. |
| **IA-2.P2** Gap-fill (Y3 hybrid; gandalf anchor authoring + legolas crawl) | Phase 2 | ✅ AUTHORING COMPLETE (work-in-batches discipline validated): ANCIENT 24 (`7565b0a`) + MEDIEVAL 29 incl CRITICAL × shadow 6 (`b2d42b6`) + MODERN 49 incl × lightning 9 (`de1e2bd`) = **102 gandalf anchors VERIFIED** + legolas crawl 23 entries (`6bb68b2`) = **125 total within ~140 LOCK C cap**. Awaiting JSON consolidation gandalf (background) before IA-2.P3 routes. |
| **IA-2.P2** Gap-fill (Y3 hybrid) | Phase 2 | ⏸ pending IA-2.P1 close | gandalf authoring + legolas crawl |
| **IA-2.P3** Elrond ingest + lineage tags | Phase 3 | 🔥 FIRING (Gate-1 PASS-with-INFO; elrond executes ingest + schema + MIGRATION.md; background ~0.5-1 session; 2 INFO items for elrond awareness: document per-period breakdown; retroactive-primary-tagging caster-class consistency with Option α/β/C) | 125 weapons + additive period_tag schema + retroactive-primary-tagging per audit § 7.4 |
| **IA-2.P4** Substrate-coverage validation | Phase 4 | ⏸ pending IA-2.P3 close | |
| **IA-3.P1** Drax workstream open + V1 integration scaffolding | Phase 1 | ✅ **SUCCESS** — reincarnated-loadout commit `75417f8` + Vercel preview `reincarnated-loadout-dkmj99vb8-matthew-wetmore-s-projects.vercel.app` (data-loading via existing `useSeasonData.ts` glob; 0 TS errors; existing components used); reincarnated-demo commit `0e511c4cb` (no Vercel — R2 in prod; data at public/; 0 TS errors). Existing-component inventory documented per INFO-3. 1 additive type extension per LOCK J § 1 (`blink` GeometryType in demo). 3 existing-component bugs surfaced for post-immediate-arc: (1) classes 0006-0011 `is_act_boss: null` not true; (2) resolveElementDisplay null-guard scope; (3) SeasonManifest elements non-optional vs engine emits null. V2 observation: 8 cosmological slots, 5 surfaced — radiance/penumbra/resonance no dedicated display. | drax close summary at `drax/notes/2026-06-01-ia-3-phase-1-mvp-integration-close.md` |
| **IA-3.P2** Integration | Phase 2 | ✅ ABSORBED-INTO-P1 (drax MVP integrated data + components in single session per LOCK F MVP-discipline) | — |
| **IA-3.P3** Vercel deployment | Phase 3 | ✅ COMPLETE (loadout Vercel preview live; demo R2-served in prod no Vercel deploy per drax-side decision) | reincarnated-loadout-dkmj99vb8-matthew-wetmore-s-projects.vercel.app |
| **IA-3.P4** Iterate with V2 | Phase 4 | ⏸ pending IA-2 close + IA-1 V2 close | |

---

## 6. Active dispatches

| Dispatch | Path | Status |
|---|---|---|
| IA-1 pre-fire question dispatch | `dispatches/2026-06-01-star-lord-rocket-ia-1-engine-readiness-pre-fire-question.md` | ✅ COMPLETE (star-lord; commit `4a2abf2`) |
| IA-1 Gate-1 dispatch | `dispatches/2026-06-01-jack-ryan-gate-1-ia-1-engine-readiness-pre-fire-question.md` | ✅ COMPLETE (PASS clean) |
| IA-1 Gate-1 finding | `qa/findings/2026-06-01-ia-1-pre-fire-question-gate-1.md` | ✅ COMMITTED (`0eff666`) |
| IA-1 star-lord readiness response | `star-lord/notes/2026-06-01-ia-1-engine-readiness-pre-fire-response.md` | ✅ COMMITTED (`4a2abf2`) |
| Immediate-arc pre-commitment ratification | `immediate-arc-pre-commitment-ratification-2026-06-01.md` | 📝 AUTHORED |
| IA-1 rocket entry-point confirmation dispatch | `dispatches/2026-06-01-rocket-ia-1-entry-point-confirmation.md` | ✅ COMPLETE (CLI-PATH-CONFIRMED; commit `155b6ba`) |
| IA-1 rocket response | `rocket/notes/2026-06-01-ia-1-entry-point-confirmation-response.md` | ✅ COMMITTED (`155b6ba`) |
| IA-1 V1 fire dispatch | `dispatches/2026-06-01-star-lord-ia-1-v1-baseline-season-generation-fire.md` | 📝 AUTHORING |
| IA-2.P1 audit dispatch | `dispatches/2026-06-01-elrond-ia-2-phase-1-magic-weapons-across-periods-audit.md` | ✅ COMPLETE (elrond; commit `1160333`) |
| IA-2.P1 Gate-1 dispatch | `dispatches/2026-06-01-jack-ryan-gate-1-ia-2-phase-1-pre-fire-review.md` | ✅ COMPLETE (PASS-with-INFO) |
| IA-2.P1 Gate-1 finding | `qa/findings/2026-06-01-ia-2-phase-1-gate-1.md` | ✅ COMMITTED |
| IA-2.P1 audit artifact | `elrond/audits/2026-06-01-magic-weapons-across-periods-audit.md` | ✅ COMMITTED (`1160333`) |
| IA-2.P1 reproducible script | `research/scripts/ia2_phase1_magic_weapons_across_periods_audit.py` | ✅ COMMITTED (`1160333`) |
| IA-1 V1 fire dispatch | `dispatches/2026-06-01-star-lord-ia-1-v1-baseline-season-generation-fire.md` | 🔥 FIRING (star-lord) |
| IA-1 V1 Gate-1 dispatch | `dispatches/2026-06-01-jack-ryan-gate-1-ia-1-v1-fire-pre-fire-review.md` | ✅ COMPLETE (PASS-with-INFO; `df63366`) |
| IA-1 V1 Gate-1 finding | `qa/findings/2026-06-01-ia-1-v1-fire-gate-1.md` | ✅ COMMITTED |
| IA-2.P2 dispatch | `dispatches/2026-06-01-gandalf-ia-2-phase-2-anchor-authoring-and-crawl-commission.md` | 🔥 FIRING (gandalf) |
| IA-2.P2 Gate-1 dispatch | `dispatches/2026-06-01-jack-ryan-gate-1-ia-2-phase-2-pre-fire-review.md` | ✅ COMPLETE (PASS-with-INFO; `4dde6a5`) |
| IA-2.P2 Gate-1 finding | `qa/findings/2026-06-01-ia-2-phase-2-gate-1.md` | ✅ COMMITTED |

---

## 7. Push discipline

Matt 2026-06-01 strategic reset: PUSH AUTHORIZED per workstream-pattern for immediate-arc cycle. Initial bulk push of ~30 commits + IA-1/2/3 fire commits pushed on standard auto-push pattern per Matt 2026-06-01 explicit authorization.

---

## 8. Post-immediate-arc decision gate

After IA-3 close (V2 season visible in Vercel apps):
- Long-arc reactivation? (Q16/Q17/Q19/WS1A.3/4/WS4)
- Or continue iterating immediate-arc (V3 season; more substrate; more drax features)?
- Or pivot direction based on what V2 reveals?

**Decision-gate at IA-3 close: post-immediate-arc Pattern B with Matt.**

---

## 9. Cross-references

- **Long-arc queue (DEFERRED):** `agentic_orchestration/post-q18-workstream-queue-2026-06-01.md`
- **Deferred-commitments source:** `agentic_orchestration/gandalf/notes/2026-06-01-q18-deferred-commitments.md`
- **Architecture A canonical lock:** `canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md`
- **Hypothesis-flow architecture:** `canonical/story/2026-05-31-hypothesis-flow-pattern-library-architecture.md`
- **WS1A.Q18 wave-close record:** `canonical/story/2026-06-01-ws1a-q18-flavor-pool-wave-close-record.md`

---

**End of immediate-arc workstream queue.**
