# 2026-05-17 — drax-demo — VS2a first VFX integration (4-step chain step 3)

**Authority:** Matt L3 2026-05-17 (~21:00 EDT) — all 3 elrond-flagged PARKED decisions resolved; step 3 of 4-step attribution-pipeline chain fully unblocked.
**Type:** Pattern B — 1.5-2 day; two-phase structure (Phase A architectural prep + Phase B VFX integration).
**Predecessors (all shipped today 2026-05-17):**
- VFX scene-needs spec @ `canonical/story/vs2a-vfx-scene-needs.md` (commit `43396bb`) — your section 2 + gandalf sections 1/3/4/5 + register-fence rule
- Elrond Pimen subset selection @ `agentic_orchestration/research/curated/pimen-subset-vs2a-2026-05-17.jsonl` (commit `6b9a689`) — 31 rows / 14 packs / 30 substrate-tags
- Drax v1.7 M1 typography foundation (commit `ef614e8`) — typography baseline preserved

**Matt-resolved acquisitions:**
- CodeManu Impact FX Pack acquired at `/Users/admin/Games/reincarnated-demo/public/assets/Impact FX Pack_Codemanu/` (closes Gap G4)
- Pimen elemental bundle acquired at `/Users/admin/Games/reincarnated-demo/public/assets/pimen/` (resolves mega-pack-02 acquisition)

---

## Why this matters

Step 3 is the first concrete render-side execution of the attribution pipeline. Up to now we've shipped the spec, the curated manifest, and the asset acquisitions. This dispatch wires assets to engine-emitted skill events so the gauntlet's first VFX render lands.

Per VFX scene-needs spec § 2 (your own authoring): **`_layers.particles` sub-container split is VS2a integration step 0** — must precede any sprite integration. This dispatch executes that step-0 prep AND the first integration in one coordinated session.

---

## Required reading

1. `canonical/story/vs2a-vfx-scene-needs.md` § 2 (your own section — render constraints + 6 slots) — primary reference
2. `canonical/story/vs2a-vfx-scene-needs.md` § 1 + § 3 + § 4 (gandalf's encounter inventory + substrate-tag inventory + per-encounter scene walkthroughs)
3. `agentic_orchestration/research/curated/pimen-subset-vs2a-2026-05-17.jsonl` — elrond's manifest; your input source for wiring
4. `agentic_orchestration/research/curated/pimen-subset-vs2a-selection-2026-05-17.md` — elrond's summary; 7×6 coverage matrix + gap closure status
5. `reincarnated-demo/scripts/pimen-ingest/` — your existing ingest pipeline (Pimen pack ingestion)
6. `reincarnated-demo/src/main.ts` — locate `_layers` definition site (Phase A target)
7. `reincarnated-demo/public/assets/Impact FX Pack_Codemanu/` — CodeManu assets (Phase B physical-impact target)
8. `reincarnated-demo/public/assets/pimen/` — Pimen elemental assets (Phase B canonical-7 target)

---

## Scope — two phases

### Phase A — `_layers.particles` sub-container split (step 0 prep)

Per your own spec § 2 finding: split `_layers.particles` into two sub-containers `particlesUnder` and `particlesOver` arranged around the `entities` layer in Z-order. This is the architectural foundation that Phase B (and all future VFX integration) needs.

Acceptance:
- `_layers.particlesUnder` exists (below entities Z-order)
- `_layers.particles` retained OR renamed `_layers.particlesOver` (above entities Z-order)
- All existing VFX render sites updated to choose Under vs Over per spec § 2 layering rules:
  - Slot A (cast-charge): `particlesUnder` (behind caster in Z-order — spec § 2.A)
  - Slot B (projectile/movement): `particlesMid` ≈ `particlesOver` for in-air projectiles
  - Slot C (impact): split layer — peak above-entity / fade below-entity (spec § 2.C)
  - Slot D (status-apply): concurrent with Slot C; same layer pattern
  - Slot E (status-ambient): `particlesUnder` for ground; `particlesOver` for overlay (spec § 2.E)
  - Slot F (skill-expired): `particlesOver`
- No visual regression on existing demo VFX (dodge trails, AOE indicators, etc.)
- `npm run build` clean

### Phase B — First VFX integration from manifest

Consume `agentic_orchestration/research/curated/pimen-subset-vs2a-2026-05-17.jsonl`. Wire the manifest rows through to engine skill events.

**Scope decision (your call):** the manifest has 31 rows. You can either:
- **B1 (recommended):** wire all 31 rows in one pass; verify each slot end-to-end with one substrate before expanding
- **B2:** wire a smaller proof-of-concept subset first (e.g., fire-only across all 6 slots) then expand iteratively

Document your choice in the completion record with rationale.

For each wired row:
- Asset loaded from vendor path (Pimen at `public/assets/pimen/<pack-slug>/...`; CodeManu at `public/assets/Impact FX Pack_Codemanu/...`)
- Substrate-tag → engine skill event mapping respects gandalf § 3 substrate-tag inventory
- Slot timing/layering matches your own § 2 render constraints
- Encounter-compatibility honored per manifest `encounter_compatibility` field
- Performance budget respected (spec § 2 numbers; manifest § 3 ingest cost estimates)

**Empirical read on G1 (cast-prep-sustained):** elrond's manifest closes G1 via Pimen spell-effect-3 startup frames + procedural fallback. Verify empirically: do spell-effect-3 startup frames give acceptable cast-prep-sustained look for substrate Slot A? Surface verdict in completion record:
- PASS: G1 confirmed CLOSED; no Mode-B crawl needed
- FAIL: G1 needs Mode-B crawl (knight-rider authorizes follow-on legolas dispatch)

**Empirical read on Slot D tint-composition (elrond's surfaced observation):** does buff/debuff status-apply tint-composition land legibly across all 7 canonical substrates? Surface PASS/FAIL with notes.

### Phase B sub-deliverable — manifest schema verification

Audit your ingest pipeline (`scripts/pimen-ingest/`) consumes elrond's manifest format correctly. Elrond's manifest schema:

```json
{
  "asset_id": "pimen.fire.cast.001",
  "vendor": "pimen",
  "substrate_tag": "fire-cast-charge",
  "slot": "A",
  "encounter_compatibility": [...],
  "attribution_class": "commercial-license" | "cc-by",
  "pack_origin": "...",
  "render_notes": "..."
}
```

If your existing pipeline keys differ (elrond noted: `source_asset_id` = `pack_slug` in your pipeline), document the mapping in completion record. **DO NOT modify elrond's manifest format** — adapt drax-side or surface as OBSERVATION for elrond follow-up.

### Phase B attribution surface

For CC-BY assets (single row in manifest: `pixel-battle-effects` per elrond) AND the newly-acquired CodeManu pack — verify attribution requirements. Both are commercial-licensed or CC-BY:
- **CodeManu** acquisition has been Matt-authorized; commercial license terms apply (check pack docs)
- **CC-BY rows** require attribution credit — author credit text in a place Matt-decides (likely game credits screen, post-VS2a)
- For VS2a ship, attribution-credit-string SHOULD be queued as a small follow-on dispatch; do NOT pre-empt by authoring a credits screen unilaterally

---

## Out of scope (DO NOT)

- ❌ DO NOT modify elrond's manifest format (consume only; surface mismatches as OBSERVATION)
- ❌ DO NOT modify the VFX scene-needs spec (consume only)
- ❌ DO NOT touch engine sim (Discipline #15 — demo as renderer; the spec is a demo-side artifact)
- ❌ DO NOT pre-empt step 4 (star-lord LLM optimization addition)
- ❌ DO NOT pre-empt elrond's eventual VS2b attribution-pipeline schema dispatch
- ❌ DO NOT author a credits screen unilaterally (CC-BY attribution surface is a Matt-decided UX choice)
- ❌ DO NOT extend M1 typography work (M2-M7 mobile phases stay post-VS2a)
- ❌ DO NOT extend to other VFX vendors not in manifest (Frostwindz / Pixogen / Fellor — those are post-VS2a)
- ❌ DO NOT pre-empt MM1-MM6 map overlay work (separate dispatch chain)

---

## Acceptance criteria

### Phase A
- [ ] `_layers.particlesUnder` + `_layers.particlesOver` (or equivalent split) implemented in `main.ts`
- [ ] Existing VFX render sites updated to choose layer per spec § 2 rules
- [ ] No visual regression on dodge trails, AOE indicators, existing VFX
- [ ] `npm run build` clean; 0 TS errors

### Phase B
- [ ] Manifest schema verification (drax pipeline consumes elrond's manifest correctly OR mismatch surfaced)
- [ ] At least the GREEN-cell core of the 7×6 coverage matrix wired (per your B1/B2 scope choice)
- [ ] Asset loading from `public/assets/pimen/` + `public/assets/Impact FX Pack_Codemanu/` works in-build
- [ ] Substrate-tag → engine skill event mapping respects spec § 3 inventory
- [ ] Slot timing/layering matches spec § 2 render constraints
- [ ] Encounter-compatibility honored per manifest field
- [ ] G1 empirical-read verdict in completion record (PASS = CLOSED / FAIL = escalate)
- [ ] Slot D tint-composition verdict in completion record (PASS / FAIL with notes)
- [ ] No regression on existing demo behavior

### Both phases
- [ ] `npm run build` clean; 0 TS errors
- [ ] Existing test suite green (or pre-existing failures confirmed unrelated)
- [ ] Tag `drax/v1.8-vs2a-first-vfx-integration-1`
- [ ] Hive-log STATE entry
- [ ] Cross-references in completion record: spec § 2, manifest path, asset paths

---

## Coordination

- **PRE-SIGNAL § 14.1.1** before hive-log appends; pull-rebase before collab-repo commits
- **Bandwidth context:** gamora regen still running in background (PID 72312; season 5 LLM naming as of last check); your work is in demo repo and shouldn't interfere
- **Engine ↔ demo parity (Matt pillar):** this is demo-side VFX integration; no engine-side changes needed for VS2a first integration

---

## Smoke test

1. Build clean
2. Load demo on desktop; cast skills across all 7 canonical substrates
3. Verify Phase A: dodge trails still render correctly; AOE indicators still render correctly
4. Verify Phase B: skill cast triggers Pimen/CodeManu VFX at expected slots; substrate-tagged assets fire on correct skill events
5. Verify G1 empirical read: spell-effect-3 startup frames look like cast-prep on enemy AOE windups (per gandalf § 4 encounter walkthroughs)
6. Verify Slot D tint-composition: buff/debuff status-apply visually legible across substrates

---

## Output to next chain step

Step 4 (star-lord LLM optimization addition) consumes:
- Your G1 empirical-read verdict (do we need more cast-prep coverage?)
- Your Slot D tint-composition verdict (do we need substrate-specific status-apply tints?)
- Any other empirical findings worth surfacing as elrond VS2b schema input

---

*Dispatched 2026-05-17 by knight-rider per Matt L3 step-3 unlock. ~1.5-2 day. Append completion record when done.*
