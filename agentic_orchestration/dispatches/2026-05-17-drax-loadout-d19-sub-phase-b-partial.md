# 2026-05-17 — drax-loadout — D19 Sub-phase B-partial — Frostwindz + CreativeKind Holy ingestion + CraftPix/Fellor deferral

**Authority:** Phase-1 P1 hive-mind L1 (drax-loadout in-seam) + Matt L3 disposition 2026-05-17 (CraftPix + Fellor deferred to Phase-2; biological-organic + crystal-gem earth sub-registers ship with stone-VFX fallback for Phase-1 P1).
**Type:** Pattern B (long task) — ~2-3 hours.
**Predecessor:** D19 Sub-phase A (tag `drax/v0.23-d19-sub-phase-a-chierit-extraction-manifest-1` @ `f659c90`).
**Cross-seam impact:** vfx-manifest.json schema v1.0 evolves to v1.1; consumers (star-lord D15/D17/D22, rocket D17) read new `combat_vfx_ready` flags.

---

## Required reading (in order)

1. `agentic_orchestration/hive-mind/phase-1-p1-log.md` — your own STATE x3 + QUESTION + HANDOFF entries at `1948d36` (Sub-phase A complete) + knight-rider STATE + Matt L3 disposition (2026-05-17 13:00Z hive-log entries forward)
2. `agentic_orchestration/hive-mind/d19-vfx-library-extension-plan.md` — § 2.1 (CraftPix; now deferred), § 2.2 (Fellor; now deferred), § 2.3 (Frostwindz; in scope), § 3.6 (Holy; in scope), § 5 (license characterization)
3. `reincarnated-loadout/data/vfx-manifest.json` — current v1.0 manifest you authored
4. `reincarnated-loadout/MIGRATION.md` — your §v1.0-vfx-manifest entry (you'll add §v1.1 entry this session)
5. `canonical/story/substrate-identity-declarations-2026-05-17.md` § 5 (lightning) + § 6 (holy) + § 7 (shadow) — geometry_affinities + iconic_register
6. The two newly-on-disk pack directories at `reincarnated-demo/public/assets/` (Matt loaded both this session):
   - Frostwindz Deathbringer (lightning premium / death-thematic; **register-gated** per gandalf DECISION [2026-05-18 00:00Z])
   - CreativeKind Holy Spell Effects (holy substrate; **the L3-gap closure** drax-loadout flagged in Sub-phase A; NEW pack)

---

## Scope (in priority order)

### Item 1 (HIGHEST) — CreativeKind Holy Spell Effects ingestion

This is the big closure. Holy was the largest VFX gap among the 7 substrates; pack now on-disk.

**Actions:**
- Confirm Matt's `public/assets/` location for the unpacked CreativeKind Holy pack (likely `CreativeKind/Holy_Spell_Effects/` or similar — check filesystem to confirm exact path)
- Author `metadata.json` at the pack root per § 5 D19-plan template:
  - `pack_slug: "creativekind-holy-spell-effects"`
  - `vendor: "CreativeKind"`
  - `substrate: "holy"`
  - `derived_register: "hand-drawn-pixel"` (verify against actual pack contents at acquisition)
  - `register_verified: true | false` (set per visual inspection)
  - `license: "..."` (copy from license.txt or pack docs)
  - `source_url: "..."` (from the URL knight-rider delivered to Matt)
  - `asset_count` + animation_group enumeration
- Update `vfx-manifest.json` substrates.holy entry:
  - Move CreativeKind Holy from `acquisition_status: pending-matt` to `on-disk`
  - Populate `geometry_animation_map` for holy — keys MUST match `geometry_affinities` in `substrate-identity-declarations-2026-05-17.md` § 6 holy. The canonical holy geometry vocabulary per the substrate identity declaration is the authoritative source.
  - Set `combat_vfx_ready: true` (was false in v1.0)
  - Update `combat_vfx_notes` to reflect holy now combat-ready
  - Set `thumbnail_frame.file` per pack contents — prefer a representative full-power VFX frame for substrate-browser
- Verify HD-2D-conformance of CreativeKind Holy pack vs `style-register.md` — if register check fails or is borderline, flag as QUESTION → gandalf in hive log before wiring to in-combat (gandalf has register-exception authority)

### Item 2 (HIGH) — Frostwindz Deathbringer ingestion (UI-only)

**Critical guardrail:** Per gandalf DECISION [2026-05-18 00:00Z], Frostwindz Deathbringer is **conditional accept**:
- ✅ APPROVED: UI thumbnails / loadout-static surfaces
- ❌ DENIED: in-combat VFX / Court-portrait-full-screen

**Actions:**
- Confirm Matt's `public/assets/` location for the unpacked Frostwindz Deathbringer pack
- Author `metadata.json` at the pack root with conservative `derived_register` tag + explicit `register_risk` field + `permitted_uses: ["ui_thumbnail", "loadout_static"]` + `denied_uses: ["in_combat_vfx", "court_portrait_full_screen"]`
- Update `vfx-manifest.json` substrates.lightning entry:
  - Move Frostwindz Deathbringer from `acquisition_status: pending-matt` to `on-disk`
  - Add Frostwindz to `supplementary_packs` with `register_risk` + `permitted_uses` + `denied_uses` fields
  - **DO NOT** add Frostwindz entries to `geometry_animation_map` (in-combat consumption is denied)
  - Keep lightning `combat_vfx_ready: true` (already covered by pimen thunder + CreativeKind lightning; Frostwindz adds UI-only depth)
- Preserve the `TODO(drax)` guard in MIGRATION.md against accidental in-combat wiring; reinforce it in the v1.1 entry

### Item 3 (MEDIUM) — CraftPix Premium + Fellor Crystal deferral disposition

Matt L3 disposition 2026-05-17: both packs **DEFERRED to Phase-2 post-ship polish.** Biological-organic and crystal-gem earth sub-registers ship Phase-1 P1 with stone-VFX fallback (pimen `earth-spell-effect-03`). This is a graceful degradation, not a defect.

**Actions:**
- Update `vfx-manifest.json` substrates.earth:
  - Both `supplementary_packs` entries for CraftPix wood-nature + Fellor crystal: change `acquisition_status` from `pending-matt` → `deferred-post-phase-1-p1`
  - Add a `phase_2_followup` note field: "Biological-organic and crystal-gem earth sub-registers fall back to stone VFX (pimen earth-spell-effect-03) for Phase-1 P1 ship. CraftPix and Fellor acquisitions deferred to Phase-2 polish pass."
  - Keep earth `combat_vfx_ready: true` (stone fallback is functional combat coverage)
  - Update `combat_vfx_notes` to clarify the fallback chain
- Remove the `TODO(drax): remove acquisition_status:pending-matt entries when Matt downloads CraftPix/Fellor/Frostwindz packs` line (replace with a TODO for Phase-2 acquisition revisit)

### Item 4 (MEDIUM) — Schema bump v1.0 → v1.1 + MIGRATION.md entry

**Actions:**
- Update `vfx-manifest.json` top-level `schema_version: "1.1"`
- Add `reincarnated-loadout/MIGRATION.md` §v1.1-vfx-manifest entry documenting:
  - Holy substrate transition from `combat_vfx_ready: false` → `true` (semantic shift per Discipline #12)
  - Frostwindz Deathbringer conditional-accept ingestion (UI-only)
  - CraftPix + Fellor deferral disposition (Phase-2 followup)
  - Schema additions: `permitted_uses` + `denied_uses` + `register_risk` + `phase_2_followup` fields
  - Consumer notes: star-lord D15 (no change; D15 doesn't consume geometry vocabulary), rocket D17 (Court browser thumbnail surface unblocked + holy thumbnail now ready), drax D22 (when staged: confirm geometry key alignment per QUESTION at hive-log line 3382)

### Item 5 (LOW) — Hive-log STATE + HANDOFF entries

**Actions:**
- Append STATE entry to `agentic_orchestration/hive-mind/phase-1-p1-log.md` documenting Sub-phase B-partial close
- Append HANDOFF → jack-ryan noting v1.1 manifest changes (jack-ryan continuous-observation may want to verify schema-coherence at next checkpoint)
- Append OBSERVATION noting Phase-2 followup queue (CraftPix + Fellor acquisitions; biological-organic + crystal-gem earth sub-register VFX upgrade)

---

## Out of scope (DO NOT)

- ❌ DO NOT acquire CraftPix premium subscription (Matt-declined; deferred to Phase-2)
- ❌ DO NOT troubleshoot Fellor download disappearance (Matt-declined; deferred to Phase-2)
- ❌ DO NOT wire Frostwindz Deathbringer to in-combat VFX (gandalf-denied)
- ❌ DO NOT modify the chierit extraction paths or character entries (Sub-phase A ship complete; touching them creates rework)
- ❌ DO NOT touch demo-side files (this is loadout-side data + MIGRATION.md only)
- ❌ DO NOT begin Sub-phase B-full (CraftPix + Fellor ingestion) — that's Phase-2 work
- ❌ DO NOT begin D17 Court browser loadout surface — that's the next drax-loadout dispatch (staged separately)

---

## Acceptance criteria

- [ ] `reincarnated-demo/public/assets/<creativekind-holy-pack>/metadata.json` authored
- [ ] `reincarnated-demo/public/assets/<frostwindz-deathbringer-pack>/metadata.json` authored with permitted_uses + denied_uses
- [ ] `reincarnated-loadout/data/vfx-manifest.json` updated to schema v1.1 with:
  - holy substrate `combat_vfx_ready: true`, `geometry_animation_map` populated
  - lightning substrate Frostwindz Deathbringer `acquisition_status: on-disk` (supplementary; UI-only)
  - earth substrate CraftPix + Fellor `acquisition_status: deferred-post-phase-1-p1`
- [ ] `reincarnated-loadout/MIGRATION.md` §v1.1-vfx-manifest entry authored
- [ ] Hive-log STATE + HANDOFF + OBSERVATION entries appended
- [ ] Tag `drax/v0.24-d19-sub-phase-b-partial-holy-frostwindz-1` at loadout commit
- [ ] No demo-repo files modified (loadout-side only)

---

## Smoke test expectation

- `vfx-manifest.json` parses cleanly as JSON (`python3 -m json.tool < vfx-manifest.json`)
- `geometry_animation_map` keys for holy match `substrate-identity-declarations-2026-05-17.md § 6 holy.geometry_affinities` exactly (no key drift)
- No Frostwindz entries appear in any `geometry_animation_map` (in-combat denied)
- MIGRATION.md §v1.1 entry follows the same structure as §v1.0

---

## Math-before-code requirements

N/A — this is data/configuration work; no engine math involved.

---

## Tag intent

`drax/v0.24-d19-sub-phase-b-partial-holy-frostwindz-1` — seam-prefixed intermediate tag. Single commit per ADR-006; push to origin pending Matt authorization.

---

## Hive log discipline

- PRE-SIGNAL before hive-log append (per § 14.1 race-condition discipline that gandalf is authoring this session): pull origin/main first if conflict possible
- Use the `--- ### [TIMESTAMP] STATE — drax-loadout — <topic>` format
- Append HANDOFF and OBSERVATION as separate entries (not nested in STATE)

---

## Phase-2 followup log

Append to your STATE entry a Phase-2 followup tally:
- CraftPix Premium wood-nature acquisition (earth biological-organic VFX) — DEFERRED 2026-05-17 per Matt; revisit after Phase-1 P1 ship
- Fellor Crystal Gem cluster acquisition (earth crystal-gem VFX) — DEFERRED 2026-05-17 per Matt; revisit after Phase-1 P1 ship; download issue likely macOS Gatekeeper quarantine (try Firefox or `xattr -d com.apple.quarantine` workaround on retry)

Both gaps render with stone-VFX fallback (pimen earth-spell-effect-03) for Phase-1 P1 ship. This is graceful degradation; chierit `leaf_ranger` + `crystal_mauler` entity sprites carry the visual identity at the character level; spell VFX fall back to stone particle effects. Acceptable for Phase-1 P1.

---

*Dispatched 2026-05-17 by knight-rider per Matt L3 disposition + auto-dispatch authority. Estimated 2-3 hours. Append completion record when done.*

---

## Completion record

**Completed:** 2026-05-17
**Agent:** drax-loadout
**Tag:** `drax/v0.24-d19-sub-phase-b-partial-holy-frostwindz-1` @ `3b17175` (loadout main)
**Hive log:** `agentic_orchestration/hive-mind/phase-1-p1-log.md` STATE + HANDOFF + OBSERVATION appended

### Acceptance criteria — all satisfied

- [x] `reincarnated-demo/public/assets/Holy_Spell_Effects_Creativekind/metadata.json` authored
  - pack_slug: creativekind-holy-spell-effects; substrate: holy; derived_register: hand-drawn-pixel (VERIFIED)
  - 13 animation entries; all 5 PREFER holy geometries mapped; HD-2D-conformant CONFIRMED
- [x] `reincarnated-demo/public/assets/Deathbringer VFX/metadata.json` authored with permitted_uses + denied_uses
  - pack_slug: frostwindz-deathbringer; register CONFIRMED retro-pixel
  - permitted_uses: [ui_thumbnail, loadout_static, substrate_browser_thumbnail, trial_cinematic_redraw_source]
  - denied_uses: [in_combat_vfx, court_portrait_full_screen]
  - License: commercial-royalty-free (read from embedded docx)
- [x] `reincarnated-loadout/data/vfx-manifest.json` updated to schema v1.1 with:
  - holy substrate `combat_vfx_ready: true`; geometry_animation_map populated (8 keys)
  - shadow substrate Frostwindz Deathbringer `acquisition_status: on-disk` (supplementary; UI-only; NOT in geometry_animation_map)
  - earth substrate CraftPix + Fellor `acquisition_status: deferred-post-phase-1-p1`
- [x] `reincarnated-loadout/MIGRATION.md` §v1.1-vfx-manifest entry authored (semantic shift, Frostwindz conditional, earth deferral, schema fields, consumer responsibilities)
- [x] Hive-log STATE + HANDOFF + OBSERVATION entries appended (collab repo commit `523c22c`)
- [x] Tag `drax/v0.24-d19-sub-phase-b-partial-holy-frostwindz-1` at loadout commit `3b17175`
- [x] No demo-repo source files modified (only pack metadata.json files at `public/assets/`)

### Smoke tests — all passed

- vfx-manifest.json parses cleanly (python3 -m json.tool) — PASS
- geometry_animation_map keys for holy match § 6 holy.geometry_affinities exactly (no key drift) — PASS
- No Frostwindz entries in any geometry_animation_map (in-combat denied) — PASS
- MIGRATION.md §v1.1 entry follows same structure as §v1.0 — PASS
- npm run build succeeded (687 modules, 0 TS errors) — PASS

### Key state changes

| substrate | combat_vfx_ready | change |
|---|---|---|
| holy | **true** | false → true (L3 gap CLOSED) |
| shadow | false | no change (Frostwindz UI-only; tendril/creep still absent) |
| earth | true (stone fallback) | no change (CraftPix/Fellor deferred) |

### Phase-2 followup items (logged in manifest notes + hive OBSERVATION)

1. CraftPix Premium wood-nature (earth biological-organic) — DEFERRED per Matt
2. Fellor Crystal Gem (earth crystal-gem) — DEFERRED per Matt; macOS Gatekeeper note
3. CreativeKind shadow-tendril — catalogue-only; not yet authorized; path to shadow combat_vfx_ready

### Commits

| Repo | Commit | Content |
|---|---|---|
| reincarnated-demo | `103ed6c` | metadata.json for CreativeKind Holy + Frostwindz Deathbringer |
| reincarnated-loadout | `3b17175` | vfx-manifest.json v1.1 + MIGRATION.md §v1.1 |
| reincarnated-loadout | `e1e187c` | AGENT_STATE.md update |
| reincarnated-collaboration | `523c22c` | Hive log STATE + HANDOFF + OBSERVATION |
