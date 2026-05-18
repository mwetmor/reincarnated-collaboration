# 2026-05-17 — elrond — Monster-subset curation for VS2a final (Q7 = YES authorization)

**Authority:** Matt L3 2026-05-17 late evening — "VS2a Final Sprint"; Q7 monster-subset curation authorized YES (was deferred in prior elrond CraftPix dispatch). 17 monster packs + 4 boss packs on disk per legolas-3; need curated subset manifest for drax wiring follow-on.
**Type:** Pattern B — curation + manifest authoring; ~1-2 hours.
**Predecessor:** elrond CraftPix mega-catalogue curation extension (shipped; stubbed monster-subset as DEFERRED — this dispatch un-defers).

---

## Why this matters

Demo currently has 13 monster sprites wired (angel-guardian / crystal-golem / demon-mage / evil-eye / fire-elemental / fire-lord ×2 / goblin-mage / god-of-lightning / hellfire-rhino / lich / mutant-skeleton / sword-warrior). Legolas-3 surfaced 17 CraftPix monster packs + 4 boss packs on disk — DOUBLE the current variety. Wiring them in VS2a final transforms encounter variety.

This dispatch produces the curated subset manifest. Drax v1.14 follow-on dispatch (after this lands) wires the chosen monsters into the demo.

---

## Required reading

1. **Legolas-3 free_characters_and_vfx inventory** — `agentic_orchestration/research/catalogue/craftpix-mega-catalogue-2026-05-17/inventory.jsonl` (search for monster + boss packs)
2. **Legolas-3 summary** — `agentic_orchestration/research/catalogue/craftpix-mega-catalogue-2026-05-17/summary.md` § 6 (monster roster overview: 17 packs covering undead / demonic / nature / construct / beast / reptilian / dragon)
3. **Current monster sprite wiring** — `reincarnated-demo/src/visuals/monsterSprites.ts` (existing CreativeKind path; understand manifest shape drax consumes)
4. **Current monster acquisitions** — `reincarnated-demo/public/assets/monsters/` (13 wired today; manifest target shape)
5. **Canonical-7 substrate map** — for per-substrate mapping (fire / water / earth / wind / lightning / holy / shadow + physical)
6. **D10/D11 monster data** — `reincarnated-engine/output/standard-demo-regen-2026-05-17/season_002011-015/monsters.json` (current monster instances; 44 per season × 5 = 220; understand archetype distribution to map CraftPix variety to canonical archetypes)

---

## Scope — three deliverables

### Deliverable 1 — Monster subset manifest

Author `agentic_orchestration/research/curated/monster-subset-vs2a-2026-05-17.jsonl`.

Per row (mirror your prior Pimen / icon-prop subset schema):
- asset_id (vendor + pack + variant)
- vendor + pack
- monster_archetype (humanoid / undead / demonic / beast / nature / construct / reptilian / dragon)
- canonical_substrate_mapping (which canonical-7 substrate this monster fits: zombie → shadow; dragon → fire; golem → earth; ent → earth/wind; etc.)
- role_orientation (trash / elite / boss)
- animation_states (idle / walk / attack / hurt / die — coverage per pack)
- pixel_dimensions (sprite size at native; rendered size target)
- file_count + format
- license + attribution_class (CraftPix-Free-Terms standard)
- vs2a_slot_priority (1-5; 5 = wire immediately for VS2a variety; 1 = nice-to-have)
- drax_wiring_notes (manifest shape drax consumes; per-monster file mapping)

Target: prioritize the 8-12 highest-impact monsters for VS2a wiring. Don't try to wire all 17 — drax v1.14 dispatch should be bounded.

### Deliverable 2 — Coverage matrix update

Author `agentic_orchestration/research/curated/monster-coverage-matrix-vs2a-2026-05-17.md`:

Matrix axes:
- 8 canonical substrates × 3 role tiers (trash / elite / boss) = 24 cells
- Per cell: which currently-wired CreativeKind monster fills it (if any); which CraftPix candidate could fill it (if any); GREEN/YELLOW/RED

Flag substrate gaps — which canonical-7 substrates don't have boss representation, etc.

### Deliverable 3 — Summary + handoff

Author `agentic_orchestration/research/curated/monster-curation-summary-vs2a-2026-05-17.md`:

1. Executive summary
2. Per-archetype recommendation (trash / elite / boss per substrate)
3. Acquisition status (all on disk; no $ acquisition needed)
4. Drax wiring complexity assessment (how many monsters can drax reasonably wire in v1.14; recommend phased approach if needed)
5. Element-imbalance flags (which substrates under-served)
6. HANDOFFs:
   - → drax: monster-subset manifest ready for v1.14 wiring follow-on (post-v1.13 VS2a final sprint)
   - → matt: any acquisition gaps surfaced (if you find a substrate that genuinely needs new acquisition; otherwise none)
   - → knight-rider: standard chain coordination

---

## Out of scope (DO NOT)

- ❌ DO NOT commission new vendor acquisitions (all monsters are on-disk free CraftPix)
- ❌ DO NOT modify legolas-3 raw inventory (consume only)
- ❌ DO NOT touch drax wiring code (manifests only)
- ❌ DO NOT include monsters that fail HYBRID a3 register (filter at curation time)
- ❌ DO NOT pre-empt D11.x design work (separate seam; just provides drax with menu for wiring)

---

## Acceptance criteria

- [ ] Monster subset manifest authored (8-12 prioritized rows)
- [ ] Coverage matrix authored (substrate × role-tier; GREEN/YELLOW/RED)
- [ ] Summary doc authored
- [ ] Per-substrate mapping explicit (each manifest row has canonical_substrate_mapping)
- [ ] License posture: all CraftPix-Free-Terms (one attribution credit)
- [ ] Drax wiring complexity assessed
- [ ] PRE-SIGNAL § 14.1.1 before hive-log append
- [ ] Hive-log STATE + HANDOFF → drax + HANDOFF → matt + HANDOFF → knight-rider
- [ ] No tag (curation; not code)

---

## Coordination

- **Parallel-safe with**: drax VS2a final sprint (different seam: drax wires v1.13 environment+VFX; your output feeds drax v1.14 monster expansion); gandalf audio register canon (in flight); rocket v1.13.2 demo-sync; D11.1 sprint chain
- **PRE-SIGNAL § 14.1.1** before hive-log append
- **No tag** (curation)

---

*Dispatched 2026-05-17 by knight-rider per Matt L3 VS2a Final Sprint + Q7 monster-subset curation YES authorization. ~1-2 hours. Append completion record when done.*

---

## Completion record — 2026-05-17 late-evening+4 — elrond

**Status:** SHIPPED. All three deliverables authored and present in `agentic_orchestration/research/curated/`.
**Duration:** ~1.5 hours (within dispatch target band).
**Tag:** none (curation; not code per dispatch directive).
**Hive log:** STATE entry appended at `agentic_orchestration/hive-mind/phase-1-p1-log.md` (`[2026-05-17 late-evening+4] STATE — elrond — Monster-subset curation VS2a Final SHIPPED`), preceded by PRE-SIGNAL § 14.1.1.

### Deliverables shipped

1. **`monster-subset-vs2a-2026-05-17.jsonl`** — manifest authored; stub (`_status: DEFERRED`) overwritten with full manifest (`_status: AUTHORED`, `_manifest_version: 1.0`). 10 priority-3+ rows for drax v1.14 wiring + 2 priority-2 deferred-noted rows = 12 total candidates preserved.

2. **`monster-coverage-matrix-vs2a-2026-05-17.md`** — 8 canonical substrates (fire/water/earth/wind/lightning/holy/shadow/physical) × 3 role tiers = 24-cell GREEN/YELLOW/RED matrix with current CK + candidate CP attribution. Pre-curation vs post-curation comparison; RED-cells-remaining table.

3. **`monster-curation-summary-vs2a-2026-05-17.md`** — executive summary + per-archetype recommendation + acquisition status + drax wiring complexity assessment (phased Option A/B recommendation) + element-imbalance flags + handoffs.

### Key outcomes

- **Variety expansion 11 → 21 monsters (+91%)** with zero acquisition cost (all 10 selections on disk per legolas-3).
- **Substrate-gap-closure:** water and wind move from RED → YELLOW (gained multi-tier coverage); earth gains 3-tier ladder (trash/elite/mini-boss); fire gains first boss representation (dragon).
- **Boss tier expansion 1 → 3 monsters** is the single highest-impact change — substrate-flavored act-culminating encounters now possible.
- **Phased wiring recommended** (Phase A 6 priority-5 monsters ~3h at v1.14; Phase B 4 priority-3-4 monsters ~2h at v1.15) to keep drax wiring sprints bounded.
- **License posture:** single CraftPix corpus credit covers all 10 monsters; no per-pack attribution complexity.

### Acquisition gaps surfaced

Two substrate gaps NOT resolvable from on-disk CraftPix corpus, flagged for Matt L3 decision:
1. Holy substrate non-boss tiers (trash + elite + mini-boss all RED).
2. Lightning substrate native (current fire-lord-creativkind-thunder is thunder-shifted re-skin, not native lightning).

Other RED cells (wind boss / physical boss / shadow full-boss) addressable via on-disk `craftpix-897123-boss-monsters-pixel-art` pack at drax v1.15 follow-on — no acquisition needed.

### Handoffs fired

- **→ drax (v1.14 wiring inputs):** manifest + matrix + summary ready; phased Option B recommended per summary § 4.1.
- **→ matt (acquisition gaps):** holy non-boss + lightning native acquisition decisions per summary § 7.2.
- **→ knight-rider (chain coordination):** next chain links: drax v1.14 → Matt acquisition decision → conditional legolas-4 chierit-pack-expansion → drax v1.15 pack-897123 wiring.

### Acceptance criteria

- [x] Monster subset manifest authored (10 priority-3+ + 2 priority-2 deferred-noted = 12 rows; upper edge of 8-12 target)
- [x] Coverage matrix authored (8 substrate × 3 role-tier; GREEN/YELLOW/RED per cell)
- [x] Summary doc authored (executive + per-archetype + acquisition + drax complexity + element-imbalance + handoffs)
- [x] Per-substrate mapping explicit (each manifest row has `canonical_substrate_mapping` field)
- [x] License posture: all CraftPix-Free-Terms (one attribution credit covers all)
- [x] Drax wiring complexity assessed (phased Option A/B recommendation in summary § 4.1)
- [x] PRE-SIGNAL § 14.1.1 before hive-log append (git fetch + log tip + status verified)
- [x] Hive-log STATE + HANDOFF → drax + HANDOFF → matt + HANDOFF → knight-rider
- [x] No tag (curation; not code)

— elrond
