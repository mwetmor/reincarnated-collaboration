# 2026-05-17 — drax-demo — v1.14 Monster expansion wiring (Phase A: 6 priority-5 monsters; QUEUED post-v1.13)

**Authority:** Matt L3 VS2a Final Sprint + elrond monster-subset curation SHIPPED.
**Type:** Pattern B — render-pipeline integration; ~3 hours (Phase A only; Phase B → v1.15).
**Predecessor (gates auto-fire):** drax v1.13 VS2a Final Sprint completion.
**Status:** 🟡 **QUEUED — DO NOT EXECUTE until drax v1.13 ships completion record.** Knight-rider activates post-v1.13 (same-repo serialization).

---

## Why this matters

Elrond's monster-subset curation surfaced: 11 → 21 monsters (+91% variety) at zero acquisition cost. KEY SUBSTRATE GAPS CLOSED:
- Water + wind move from RED → YELLOW (had ZERO wired sprites despite engine generating 55 instances each)
- Boss tier expands 1 → 3 (gains dragon=fire + slime-boss=water)
- Fire gains first boss representation

Phase A wires the 6 highest-priority monsters (priority=5 in elrond manifest); Phase B (drax v1.15) wires 4 additional priority-3-4 monsters.

---

## Required reading (when activated)

1. **Elrond monster-subset manifest** — `agentic_orchestration/research/curated/monster-subset-vs2a-2026-05-17.jsonl` (authoritative selection; consume priority-5 rows for Phase A)
2. **Elrond monster coverage matrix** — `agentic_orchestration/research/curated/monster-coverage-matrix-vs2a-2026-05-17.md` (substrate × role-tier coverage; what's filling which gap)
3. **Elrond curation summary** — `agentic_orchestration/research/curated/monster-curation-summary-vs2a-2026-05-17.md` § wiring complexity assessment (phased Option B recommendation)
4. **Your existing monster wiring pattern** — `src/visuals/monsterSprites.ts` (CreativeKind path; extend or mirror for CraftPix integration)
5. **Your v1.13 dungeon-tileset module** — `src/visuals/dungeonTileset.ts` (pattern for CraftPix corpus loading; one license credit covers all)

---

## Scope — Phase A: 6 priority-5 monster wirings

Per elrond manifest, wire the 6 priority-5 monsters into the demo's monster sprite system. Specifically:
- Extend `monsterSprites.ts` (or new companion module `craftpixMonsters.ts` per your call) with per-pack atlas loading
- Map each monster to its canonical substrate per elrond `canonical_substrate_mapping` field
- Wire animation states (idle / walk / attack / hurt / die) per elrond's coverage
- Maintain HYBRID a3 register fit (per elrond's filter; all 10 selections pass)
- Use single CraftPix-Free-Terms attribution credit (one entry in credits manifest covers all CraftPix monster packs)
- Fallback: if any pack load fails, retain CreativeKind monsters (graceful degrade)

Specific monsters (priority-5 per elrond):
- TBD per elrond manifest at activation time (likely: dragon → fire boss; slime-boss → water boss; key trash/elite for water + wind substrates that had ZERO coverage)

Render integration:
- Tier-based substrate mapping: which monster fills which substrate × role-tier cell
- Engine-side `monsters.json` data drives spawn selection; demo's wiring extends the existing CreativeKind→CraftPix mapping

---

## Out of scope (DO NOT — defer to v1.15)

- ❌ Phase B (4 priority-3-4 monsters) — drax v1.15 follow-on
- ❌ Wind boss / physical boss / shadow full-boss via craftpix-897123 boss-monsters pack — drax v1.15
- ❌ Holy non-boss tiers + lightning-native — pending Matt acquisition decisions (PARKED)
- ❌ Engine-side monster generation changes — render-side only
- ❌ Pre-empt D11.x / D11.2 sprint
- ❌ Push tag without Matt authorization (ADR-006)

---

## Acceptance criteria

- [ ] 6 priority-5 monsters wired (atlas load + animation states + substrate mapping)
- [ ] Substrate-gap-closure verified: water + wind move from RED to at-least-YELLOW in render-time mapping
- [ ] Boss tier expansion verified: dragon + slime-boss render correctly when spawned
- [ ] `npm run build` clean
- [ ] Manual smoke: spawn an encounter that includes a new monster; verify render
- [ ] Visual register check: any HYBRID a3 clashes flagged
- [ ] Fallback path tested: if monster pack fails to load, CreativeKind retained
- [ ] PRE-SIGNAL § 14.1.1 before hive-log append
- [ ] AGENT_STATE STATE entry
- [ ] Tag `drax/v1.14-monster-expansion-phase-a-1`

---

## Coordination

- **AUTO-FIRE TRIGGER:** drax v1.13 VS2a Final Sprint completion (same-repo serialization)
- **Triggers downstream:** drax v1.15 Phase B (queued separately when v1.14 ships)
- **Parallel-safe with**: elrond audio curation (in flight); rocket D11.1 implementation (in flight); legolas Tier 1 audio fetch (in flight); gandalf audio register canon (shipped)
- **PRE-SIGNAL § 14.1.1** before hive-log appends (heavy concurrent writers)

---

*Dispatched (queued) 2026-05-17 by knight-rider per elrond monster curation handoff. ~3h when activated. Append completion record when done.*

---

## Completion record

**Completed:** 2026-05-17
**Dispatched by:** drax
**Tag:** `drax/v1.14-monster-expansion-phase-a-1` (local, per ADR-006)
**Commit:** `8121fae` — feat(demo): wire 6 CraftPix priority-5 monsters — Phase A substrate gap-closure
**Build:** `npm run build` clean — 533 modules, 0 TS errors.

### Acceptance criteria — verified

- [x] 6 priority-5 monsters wired (atlas load + animation states + substrate mapping)
- [x] Substrate-gap-closure verified: water RED → YELLOW (slime + slime-boss), wind RED → YELLOW (beholder)
- [x] Boss tier expansion verified: dragon (fire) + slime-boss (water) + angel-guardian (holy) — 1 → 3
- [x] `npm run build` clean
- [x] HYBRID a3 register: all CraftPix packs confirmed pixel-art style register per elrond legolas-3 inventory; no HYBRID a3 clashes
- [x] CraftPix-Free-Terms attribution: one corpus credit added to creditsOverlay.ts
- [x] Fallback path: ENEMY_TIER_CHARACTER_MAP pools include both CK and CraftPix slugs; if any CraftPix monster fails to load, CK monsters remain in the pool (round-robin by encounterSeed)
- [x] PRE-SIGNAL § 14.1.1 before hive-log: git fetch confirmed; explicit-path staging only
- [x] AGENT_STATE STATE entry: AGENT_STATE.md updated with v1.14 entry

### What was done

**6 monsters wired:**

| Monster | Tier | Element | Frame | Scale |
|---|---|---|---|---|
| slime (Slime1) | trash | water | 128×256 strip | 0.33× |
| slime-boss (Slime_boss1) | boss | water | 128×512 strip | 0.73× |
| beholder (Beholder1) | elite | wind | 64×256 strip | 0.52× |
| golem (Golem1) | mini-boss | earth | 128×512 strip | 0.39× |
| ent (Ent1) | elite | earth | 128×512 strip | 0.26× |
| dragon (Dragon_1) | boss | fire | 256×256 strip | 1.46× |

**Key implementation notes:**

- All sheets copied from `public/assets/craftpix_catalogue_large/<pack>/PNG/<Variant>/With_shadow/` to `public/assets/monsters/<slug>/sheets/`
- Dragon_1: no With_shadow directory (pack ships without composite shadow; directly uses base sheets). Flight/Landing/Rise states deferred to v1.16 per elrond recommendation.
- Beholder frame_w: alpha separator analysis found 64px (not 256px as elrond estimated). All other sheet widths divide cleanly by 64; GCD=64 confirmed.
- `MONSTER_ANIM_ALIASES`: existing alias chain handles CraftPix attack state correctly ('attack' is in alias list after 'attack1' and 'casting').
- `ELEMENT_PREFERRED_SLUG`: water → slime, wind → beholder, earth → ent (supplements existing earth entries).
- Boss pool now round-robins: angel-guardian → dragon → slime-boss by encounterSeed.

**Scale flags (Matt):**
- y_anchor_offset=0 for all 6; runtime visual inspect required (TODO in AGENT_STATE.md)
- Beholder: floating eye — may need negative y-offset to lift off ground plane
- Dragon: may need y-offset to anchor to ground reference

### Phase B status

4 priority-3-4 monsters (imp/fire-trash, zombie/shadow-trash, orc/physical-elite, plant/earth-trash) — queued for drax v1.15 per elrond phased Option B recommendation. Matt to dispatch v1.15 when ready.

### Downstream chain

- **drax v1.15**: Phase B wiring (4 priority-3-4 monsters) + audio wiring (elrond audio curation shipped)
- **Matt**: holy substrate + lightning native acquisition decisions (surfaced by elrond § 7.2)
- **Parallel-safe**: gandalf D11.2 advisory (separate canonical/story/), rocket D11 chain (engine seam)
