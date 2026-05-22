# Findings Summary — Weapon Library Import Discovery + SQL Schema Proposal

**Date:** 2026-05-22 (evening)
**Steward:** legolas (research scout; Mixed Mode A + Mode B; bounded sub-agent run)
**Commissioned by:** Matt, via gandalf-routed dispatch
**Commission:** `agentic_orchestration/dispatches/2026-05-22-legolas-weapon-library-import-discovery.md`
**Note:** This summary was returned as agent output text (sub-agent output constraints prevented direct write); materialized to disk by gandalf for canonical reference.

---

## Headline Finding 1 — The CC0 Library Landscape is Larger Than Expected

Three libraries provide a credible import baseline at **$0**:

- **Meshy.ai user library:** 60,073+ weapon models, CC0 uniform, FBX/GLB/OBJ, 8 structured subcategories (Swords & Blades: 12,287; Firearms: 7,151; Polearms: 1,064; Bows & Ranged: 1,005; Fantasy Weapons: 2,021). **Largest CC0 weapon source found by a wide margin.**
- **Sketchfab CC0+CC-BY:** 2,570 CC-licensed models in weapons-military category per the peer-reviewed S3D3C dataset (arXiv 2407.17205). License breakdown: 9.5% CC0 (~244), 36.3% CC-BY (~933). Full Data API v3 with category/license/downloadable filters and cursor-based pagination. Platform total: ~5M models.
- **Kenney.nl:** ~200–400 CC0 weapons, game-ready GLB/FBX/OBJ, ZIP archive per pack, ideal Phase A seed.

**Tier 1 combined target: 4,000–12,000 weapons at $0 before any paid procurement.**

Additional inventoried libraries: TurboSquid (42K+ weapons, royalty-free commercial), CGTrader (126,920 weapons, royalty-free commercial), Open Game Art (389 3D weapon entries, CC0/CC-BY/OGA-BY/GPL mixed), Smithsonian Open Access (172 Sketchfab-published models + 3,583 3D digitization catalogue items, CC0, museum-grade metadata), itch.io (986 packs tagged 3D+Weapons, CC0 subset filterable), Free3D (1,605 weapons, personal-use default — reject), Clara.io (defunct 2022 — skip), BlendSwap (.blend-only format overhead — defer), Poly Haven (no weapons category).

---

## Headline Finding 2 — Three Gear Catalogue Entries Have No Natural Library Presence

Confirming the prior Unity Asset Store survey: **Censer/Thurible (#13), Holy Symbol/Icon (#14), and War-Trumpet/Horn (#15) are absent from every surveyed web library.** This is a *structural gap*, not a coverage gap. These are game-design-specific ritual weapon abstractions.

**They are Meshy gap-fill targets by construction, not by density shortfall.** The vast-library framing is accurate for 12 of 15 gear catalogue entries; the ritual family (3 entries) requires Meshy as a first-class primary source.

---

## Headline Finding 3 — Cultural Register Coverage is Asymmetric

Medieval-European is saturated across all sources. **The Smithsonian is the ONLY source with structured cultural metadata** (`culture` field) covering underrepresented registers: Japanese/Korean swords, Native American weapons, African arms, Indian weapons — all CC0, museum provenance. It is small (~100–400 weapon models total) but uniquely authoritative for non-European `cultural_lineage` population.

All other sources rely on free-text tag inference for `cultural_lineage` — lossy but workable for European/East-Asian; largely absent for South Asian, African, Mesoamerican.

**Operational consequence:** non-European cultural register population is a hybrid of Smithsonian (authoritative; small scale) + Meshy gap-fill (scalable; aesthetic-prompted) + free-text tag inference (lossy fallback for fringes).

---

## Headline Finding 4 — Schema Design (9 Tables; Ready to Run)

The proposed 9-table SQLite schema (`schema.sql`, ready to run against the empty greenfield DB at `/Users/admin/Games/reincarnated-loadout/data/telemetry.db`) makes three non-obvious choices:

1. **Selection hotpath fields as direct columns on `weapons`** with a compound index on `(gear_catalogue_id, range_class, tech_level, cultural_lineage, readiness_state)` — avoids JOIN overhead on the most frequent generation-time query.

2. **`substrate_density` precomputed table** — the P6 density check is a single-row lookup on a 315-row table rather than a `COUNT` aggregate at generation time. Density-routing decisions are O(1).

3. **BDI ω-scores denormalized** as `best_omega_score` + `dominant_element_affinities` columns on `weapons`, seeded from the BDI ω-table at import time. Full per-element normalization deferred to post-H3 calibration.

Detail in `sql-ddl-proposal.md`; DDL in `schema.sql`.

---

## Headline Finding 5 — $0 Path Through Phase D Validated

Four-phase import plan, all $0:

| Phase | Duration | Cost | Scope |
|---|---|---|---|
| **A** | 1–2 wk | $0 | Schema lock + Kenney seed (150–250 weapons; pipeline validation) |
| **B** | 2–4 wk | $0 | Sketchfab API crawl + Meshy top-1,000 per subcategory (3,500–5,000 weapons) |
| **C** | 2–3 wk | $0 | OGA full crawl + Smithsonian API + itch.io CC0 packs (420–980 weapons; cultural diversity) |
| **D** | ongoing | $0 (Meshy Pro) | Gap-fill against density map; priority targets: gear IDs 13/14/15 + non-European substrate regions |

**Total target: 4,000–6,500 indexed weapons. Total cost: $0** (Tier 3 commercial deferred to post-Phase-D targeted dispatches if Meshy cannot fill specific substrate regions).

---

## Open Carries — Knowledge Gaps Needing Matt's Call

1. ~~**Meshy.ai bulk API** — no public API documented; web scrape required for Phase B.~~ **RESOLVED 2026-05-22 evening (Matt update):** Matt provides an authenticated Meshy API key via `MESHY_API_KEY` env var. Meshy API documentation lives at **https://docs.meshy.ai/en**. Phase B path becomes API-driven structured crawl, NOT web scrape. This materially improves: TOS compliance (unambiguous authenticated user), speed (likely hours not days for 60K), structured-metadata fidelity (typed responses; no HTML inference), rate-limit handling (documented), Discipline #19 compliance (bounded background process; structured progress; resume-on-failure feasible).
2. **Smithsonian weapon count** — `api.data.gov` key required for precise enumeration; estimate 100–400 weapons. Resolve at Phase C dispatch.
3. **CC-BY-SA legal status** — share-alike clause may be compatible with commercial games if assets kept separate from code; currently set `game_approved=0`. Matt/legal review recommended.
4. **ω-analysis pass timing** — `dominant_element_affinities` column must be seeded from BDI ω-table at Phase B import time (before Phase C) for density-routing by element to function correctly.

---

## API Access Addendum — Operational Pattern for Phase B Import Dispatch

**Authentication:**
- Env var: `MESHY_API_KEY` (set by Matt locally; `.env` file gitignored; never hardcoded; never logged)
- API docs: https://docs.meshy.ai/en (reference for endpoint inventory, request schemas, rate limits)
- Pattern inheritance: same as galadriel's `OPENAI_API_KEY` handling per `~/Games/reincarnated-engine/scripts/pitch/canary_meshy_regen.py`

**Pre-dispatch verification step (recommended before import script runs):**
- Confirm key scope covers **library browse endpoints** (model enumeration), not only text-to-3D generation. If browse access not available with this tier, request scope expansion OR fall back to authenticated-scrape (key as auth header + higher rate limits).
- Quick probe: `curl -H "Authorization: Bearer $MESHY_API_KEY" https://api.meshy.ai/...` against library-list endpoint.

**Import script discipline (per Discipline #19 RATIFIED 2026-05-22):**
- Bounded background process (`Bash(run_in_background=true)` or `nohup ... > log 2>&1 &`)
- Rate-limit-aware batching with exponential backoff
- Resume-on-failure via DB row checkpointing (60K is long; can't lose progress)
- Structured progress logging at known path
- JSON summary artifact as final-act cross-session continuity
- Status checks via `SELECT COUNT(*) FROM weapons WHERE source_library='meshy'` direct one-shot Bash queries

**Cost ledger:**
- Track Meshy Pro credits consumed per call OR per-batch fixed costs
- Append to existing cost-ledger pattern at `/Users/admin/Games/reincarnated-loadout/public/pitch/cost-ledger.json` (or a dedicated weapon-library-import ledger if separation cleaner)

This addendum was added by gandalf 2026-05-22 evening after Matt provided the API direction. The forthcoming import dispatch (authored tomorrow morning) will operationalize these specifics into a runnable bounded commission.

---

## Files in this directory

| File | Purpose |
|---|---|
| `library-enumeration.md` (761 lines) | Priority 1 — 14-library inventory with structured profiles |
| `metadata-normalization.md` (295 lines) | Priority 2 — canonical tag schema + per-library normalization mapping |
| `sql-ddl-proposal.md` (317 lines) | Priority 3 — schema rationale, ERD, table justifications, open questions for Matt |
| `schema.sql` (562 lines) | Priority 3 — ready-to-run DDL against the greenfield DB |
| `selection-patterns.md` (607 lines) | Priority 4 — 7 query templates (P1–P7) + density-routing + BDI ω/τ integration |
| `import-strategy.md` (354 lines) | Priority 5 — phased plan + license-tier policy + scale targets |

---

## Cross-Reference Map

| Consumer | Relevant finding |
|---|---|
| **gandalf** (Profile A pipeline doc finalization; gear-heavy-promotion doc) | Vast-library framing validated for 12/15 gear; 3/15 require Meshy gap-fill by construction; cultural-register coverage hybrid (Smithsonian authoritative; Meshy scalable; free-text fringes) |
| **Matt** (procurement + legal review) | $0 path validated through Phase D; CC-BY-SA legal review needed; Meshy partner-API outreach recommended |
| **rocket** (W1.15 implementation) | `schema.sql` is ready to run; selection-patterns specify query interfaces; substrate_density precomputed table is the engine's density-routing data structure |
| **drax** (loadout integration) | Schema lives in `/Users/admin/Games/reincarnated-loadout/data/telemetry.db`; any loadout-app queries against `weapons` table should respect the compound index on `(gear_catalogue_id, range_class, tech_level, cultural_lineage, readiness_state)` |
| **knight-rider** (import execution sequencing) | Four-phase plan (A→B→C→D); Phase A is schema lock + Kenney seed; Phase B is Sketchfab + Meshy scrape; Phase C is cultural-diversity crawl; Phase D is Meshy gap-fill ongoing |

---

**Signed (research):** legolas (research scout; Mode A + Mode B mixed; commission complete; ~20 min execution against 3-3.5-day budget)
**Materialized to disk by:** gandalf, 2026-05-22 evening
**For:** Profile A asset pipeline finalization tomorrow morning; gear-heavy promotion canonical doc; rocket W1.15 implementation; Matt procurement decisions + legal review carries.
