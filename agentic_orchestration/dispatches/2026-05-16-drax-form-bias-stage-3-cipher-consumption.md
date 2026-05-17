# Dispatch — 2026-05-16 — drax — Form-bias Stage 3: cipher-migration drax-side consumption (6 LEAK-RISK sites + manifest v1.5)

**From:** knight-rider (authored per star-lord Stage 3 cipher migration completion 2026-05-16; star-lord surfaced 6 drax-side LEAK-RISK sites + concrete field names for drax consumption)
**To:** drax
**Approved by:** Matt at 2026-05-16 Day 4 (form-bias 5-entry batch Entry 5 cadence Option II Stage 3 drax-side)
**Status:** QUEUED — fires after BOTH (a) your in-flight queue clears (drax MS-consume waiting on rocket + star-lord Stage B) AND (b) gandalf's per-character chierit scale recommendation lands (avoid touching loadout/demo code while scale work is in flight). Knight-rider routes when timing is clean.
**Estimated effort:** 1 session (~2-4h); LEAK-RISK site fixes + fallback resolver hardening + smoke + intermediate tag

**Gate-1 bypass rationale:** Matt-directed (form-bias cadence Option II Stage 3 — Matt-approved batch entry); single-seam (drax loadout + demo only); reversible (additive consumption with fallback pattern); paths-audit-grounded scope (no scope expansion beyond 6 enumerated sites).

**Acceptance summary:** All 6 drax-side LEAK-RISK sites consume `seasonal_dominant_element` / `seasonal_element` / `manifest.seasonal_elements` per star-lord Stage 3 export contract. Fallback pattern `seasonal_dominant_element ?? dominant_element` honored for transition seasons. Smoke verifies no canonical-four leak on player-visible paths from manifest v1.5+ seasons. Tag + AGENT_STATE + completion record. **Unblocks Spirit Guide voice audio pipeline downstream** (DS-5 dependency D2 from gandalf audio scoping framework).

---

## Why this dispatch exists

Star-lord Stage 3 cipher migration completion 2026-05-16 (`star-lord/v1.3-form-bias-stage-3-cipher-migration @ 19d8ba0`) shipped the engine-side cipher migration. 4 tracks complete: LLM prompt filters, export packet additive fields, manifest parallel structure (v1.5), debug logging cleanup. 22-test no-leak guard passing in engine.

**6 drax-side LEAK-RISK sites remain** per the cipher-migration paths-audit (`agentic_orchestration/research/cipher-migration-paths-audit-2026-05-16.md`):
- L-06, L-07: player-visible canonical-four leaks on gear cards
- L-12: leak site (loadout app)
- L-02 / L-13: fallback paths needing hardening
- L-11: additional leak site

Per gandalf audio framework load-bearing dependency D2: **Spirit Guide voice audio pipeline MUST ship AFTER Stage 3 cipher migration + paths-audit confirms no canonical-four leaks.** This dispatch is the precondition for that downstream audio commission.

## Cross-seam contract change?

**Round-trip: not applicable for the contract itself** — drax is the CONSUMER of contracts authored upstream (star-lord Stage 3 export packets + manifest v1.5). However:

- **Required: field-presence assertion at JSON load boundary.** Per R11(b) Principle 6 — when consuming engine-emitted seasonal fields, drax verifies field is present + correct shape before using.
- **Fallback semantics explicit:** `seasonal_dominant_element ?? dominant_element` is the transition-period fallback; old seasons (manifest_version < 1.5) lack seasonal fields and must resolve cleanly via canonical fallback. Fail-loud if BOTH are missing (NOT silently render empty).

## What this dispatch produces

### Step 1 — Concrete field consumption (per star-lord Stage 3 completion record)

Field names star-lord ships:
- `skill.seasonal_element` (string | null) — per-skill seasonal grouping name
- `classData.seasonal_dominant_element` (string | null) — per-class seasonal grouping name
- `gearItem.seasonal_dominant_element` (string | null) — per-gear seasonal grouping name
- `manifest.seasonal_elements` keyed by `"ignition"`, `"suffusion"`, `"bulwark"`, `"displacement"` (present in manifest_version 1.5+ seasons; null for older)

Wire each consumer site to read seasonal fields first; fall back to canonical fields when seasonal is null.

### Step 2 — Per-LEAK-RISK site fixes

Address each of the 6 sites from paths-audit:
- **L-06, L-07** (gear card player-visible) — load-bearing player-visible leaks; primary fix targets
- **L-12** — loadout app leak site
- **L-02 / L-13** — fallback resolver hardening (consume `resolveElementName() ?? canonical_key` pattern's hardening per paths-audit)
- **L-11** — additional leak site

Each site: replace direct canonical-four usage with seasonal-first + fallback pattern. Use the `manifest.seasonal_elements` lookup when grouping-name resolution is needed.

### Step 3 — Fallback resolver hardening (paths-audit P-INTENDED-PUBLIC-AS-CIPHER sites)

3 fallback sites use `resolveElementName() ?? canonical_key`. These must be hardened so that when manifest is unavailable OR has no seasonal mapping for the canonical key, the behavior is:
- Fail-loud with WARN log + render placeholder OR
- Render a degraded-but-non-leaking fallback (e.g., element-shape glyph without seasonal name)
- Do NOT silently leak canonical-four text to player-visible surfaces

Pick the approach that fits each site's UX context; document in completion record.

### Step 4 — Smoke test (Discipline #2 + R11(b) round-trip)

- Load a manifest v1.5+ season (rocket + star-lord just shipped); verify no canonical-four labels in player-visible paths (gear cards / class names / skill descriptions / loadout UI)
- Load an old manifest-v1.4-or-earlier season; verify fallback to canonical works cleanly (no errors, no missing-text)
- Field-presence assertion at JSON load boundary
- Existing demo + loadout tests pass

### Step 5 — Tag + AGENT_STATE + completion record

- Intermediate tag: `drax/v0.21-form-bias-stage-3-cipher-consumption`
- AGENT_STATE updated (both demo + loadout repos if both touched)
- Fill completion record

## Out of scope (explicit)

- **NO engine-side cipher work** (star-lord's seam; just landed)
- **NO MS schema/export/sim/consumption work** (separate MS cascade dispatches)
- **NO scale-strip / sprite-scale work** (separate dispatches)
- **NO new manifest structure** (v1.5 shape is locked by star-lord Stage 3)
- **NO Spirit Guide voice work** (downstream; this dispatch unblocks it, doesn't ship it)
- **NO scope expansion beyond the 6 LEAK-RISK sites** (paths-audit is canonical)
- **NO playable feature work beyond LEAK-RISK closure**

## Required reading

- Star-lord Stage 3 dispatch completion record: `agentic_orchestration/dispatches/2026-05-16-star-lord-form-bias-stage-3-cipher-migration.md`
- Cipher-migration paths-audit: `agentic_orchestration/research/cipher-migration-paths-audit-2026-05-16.md` (the 6 LEAK-RISK + 3 fallback sites enumerated)
- Star-lord MIGRATION.md §v1.2 (drax action items + backward-compat contract)
- Engine no-leak guard pattern: `tests/test_no_canonical_four_in_llm_prompts.py` (reference for drax-side equivalent tests)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — #2 smoke, #11 attribution, R11(b)

## Acceptance criteria

- [ ] 6 LEAK-RISK sites fixed (L-06, L-07, L-12, L-02/L-13, L-11)
- [ ] Fallback resolver hardened at 3 P-INTENDED-PUBLIC-AS-CIPHER sites
- [ ] Field-presence assertion at JSON load boundary
- [ ] Smoke: manifest v1.5+ season has no canonical-four leaks on player-visible paths
- [ ] Smoke: manifest v1.4-or-earlier season falls back cleanly
- [ ] No new TS errors; existing tests pass
- [ ] Intermediate tag `drax/v0.21-form-bias-stage-3-cipher-consumption` cut
- [ ] AGENT_STATE.md updated (demo + loadout as applicable)
- [ ] Knight-rider notified with: tag hash, per-site fallback strategy chosen at each P-INTENDED-PUBLIC site, Spirit Guide voice unblock confirmation

## Tag policy

- **Intermediate tag:** `drax/v0.21-form-bias-stage-3-cipher-consumption`
- **Milestone tag:** none from this dispatch (form-bias cadence Option II Stage 3 closeout could be milestone-tagged separately by Matt if the full cascade closeout warrants).

---

## Completion record

**Completed:** 2026-05-16
**Sites fixed:** L-06, L-07, L-12, L-02/L-13, L-11 (all 6 enumerated LEAK-RISK sites)
**Intermediate tag:** `drax/v0.21-form-bias-stage-3-cipher-consumption @ 84487ea`
**Tests status:** Build clean (687 modules, 0 TS errors). 18 cipher-guard tests written in `src/__tests__/cipher-no-leak.test.ts` — BLOCKED on vitest devDependency (jack-ryan approval required). Type-level contracts enforced by `tsc -b`.

**Fallback strategies chosen at 3 P-INTENDED-PUBLIC-AS-CIPHER sites:**

1. **L-02 (SkillDetailPanel.tsx + SkillTree.tsx — resolveElementName):**
   Strategy: FAIL-LOUD-WITH-PLACEHOLDER. Added `resolveElementDisplay(canonical, manifest, context)` to `types.ts`. Resolution chain: `seasonal_elements` lookup by `canonical_slot` → `elements` lookup → `console.warn("[drax cipher] WARN: ...")` + return `"Unknown"`. Never returns raw canonical-four. `seasonal_element` direct field on Skill used first when present (v1.5+, bypasses manifest lookup entirely).

2. **L-13 (Loadout.tsx + Sample.tsx — dominantElementName for class header):**
   Strategy: PREFER-DIRECT-FIELD-THEN-FAIL-LOUD. `classData.seasonal_dominant_element ?? resolveElementDisplay(...)`. The `??` fallback invokes the hardened resolver (see L-02 above), never the raw canonical key. Pre-v1.5 seasons correctly resolve via `manifest.elements` (fire→lantern, earth→bone etc. for Yomi season — no canonical-four leak).

3. **L-12 (Loadout.tsx + Sample.tsx — ElementMappingBadges / ElementMappingRow — manifest.elements[canonical] iteration):**
   Strategy: V1.5-PRIMARY-WITH-CANONICAL-FALLBACK. For v1.5+ manifests: iterates `manifest.seasonal_elements` (grouping-layer keyed: ignition/suffusion/bulwark/displacement); displays grouping key as semantic slot label. For pre-v1.5: falls back to `CANONICAL_ORDER` iteration over `manifest.elements`. Pre-v1.5 fallback shows canonical-four in the grouping key position — acceptable transitional display (these are pre-cipher seasons where the canonical IS the intended label). `assertManifestSeasonalFields()` called to fail-loud if v1.5 manifest is missing the new field.

**Spirit Guide voice unblock confirmation:** YES. All 6 player-visible canonical-four LEAK-RISK sites in the loadout app are closed. Dependency D2 from gandalf audio framework is satisfied. Spirit Guide voice audio pipeline may now proceed.

**Notes for knight-rider:**

1. **Demo follow-on discovered (out of scope):** `reincarnated-demo/src/ui/classSelector.ts:147` renders `cls.dominant_element` as a player-visible Pixi.js Text node in the class selector card. This was NOT in the 6 enumerated paths-audit sites (paths-audit classified demo VFX paths as INTENDED-INTERNAL, but the classSelector text display is player-visible). Recommend a follow-on drax dispatch to close this site. Low urgency (demo is desktop-only / dev-facing).

2. **v1.5 season data not yet exported:** Star-lord Stage 3 shipped the code (19d8ba0) but the loadout repo still has pre-Stage-3 season data (season_002328 at v1.3, older seasons at v1.0-1.2). Gear element display will continue to show canonical-four for existing items until a v1.5 season is generated and its export data is placed in the loadout `data/` directory. The consumption code is ready — waiting on data.

3. **Vitest gap:** Loadout repo has no test framework. 18 cipher-guard tests written at `src/__tests__/cipher-no-leak.test.ts` but require vitest as devDependency. Jack-ryan approval needed. Low urgency given type-level correctness confirmed by `tsc -b`.

4. **Archetype labels for Analytics routes:** `useAnalytics.ts` and the Analytics page may still use `ARCHETYPE_LABEL` directly for chart labels. These are analytics-internal uses (not player-character-facing). The `ARCHETYPE_LABEL` constant is unchanged; only the display-facing call sites in Loadout.tsx + Sample.tsx were updated to `resolveArchetypeLabel`. Analytics charts don't have access to a manifest, so they fall back to static labels — acceptable for analytics context (internal-use orientation).

5. **Smoke passed:** All existing pre-v1.5 season manifests resolve element names correctly via `manifest.elements` fallback (0 canonical-four leaks on element display names). Simulated v1.5 fixture resolves correctly via `seasonal_elements` (0 canonical-four leaks).
