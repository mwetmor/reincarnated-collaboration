# CraftPix ZIP expansion — DEFERRED stub (Matt Q6 pending)

**Author:** elrond
**Dispatch:** `agentic_orchestration/dispatches/2026-05-17-elrond-craftpix-mega-catalogue-curation-extension.md` § Deliverable 3
**Status:** **DEFERRED** pending Matt Q6 resolution.

---

## Deferral rationale

Per dispatch § Deliverable 3: "If Matt-Q6 = DEFER: stub with 'DEFERRED' and note in completion record."

Matt Q6 (authorize ZIP expansion + DireDungeon overlap analysis vs defer) is unresolved as of dispatch authoring. Stubbing per dispatch instructions. Curation work auto-fires when Matt resolves Q6 = YES.

---

## The two ZIPs on disk (unexpanded)

| ZIP | Path | Size | Provisional category | DireDungeon overlap risk |
|---|---|---|---|---|
| `craftpix-net-382264-armor-and-weapons-pixel-rpg-icons.zip` | `reincarnated-demo/public/assets/craftpix_catalogue_large/craftpix-net-382264-armor-and-weapons-pixel-rpg-icons.zip` | 578K | ui-icons / equipment-icons | **HIGH** — direct subject overlap with DireDungeon's weapon+armor icon set; expansion needed to determine whether this adds breadth/variants or duplicates exactly |
| `craftpix-net-596440-fishing-and-gathering-pixel-art-rpg-icons.zip` | `reincarnated-demo/public/assets/craftpix_catalogue_large/craftpix-net-596440-fishing-and-gathering-pixel-art-rpg-icons.zip` | 116K | ui-icons / gathering-skill-icons | **LOW** — fishing/gathering skill icons; orthogonal scope to DireDungeon items+loot; out-of-scope for VS2a-VS2b (no fishing/crafting mechanic) |

---

## Carry-forward work plan (when Q6 = YES)

1. **Expand both ZIPs** to `reincarnated-demo/public/assets/craftpix_catalogue_large/` siblings (preserving on-disk-only discipline).
2. **net-382264 (armor+weapons) — DireDungeon overlap analysis:**
   - Count distinct icons per equipment class (weapon types, armor pieces).
   - Compare against `DireDungeon_Items_Loot/` 259-item coverage matrix.
   - Identify: (a) exact duplicates → DEFER as redundant; (b) net additions → add to ui-icons/floor-loot manifest as supplementary backup; (c) different art style → flag as visual-register option for future palette work.
   - Update `floor-loot-subset-vs2a-2026-05-17.jsonl` + `ui-icons-subset-vs2a-2026-05-17.jsonl` with new rows where additions are net.
3. **net-596440 (fishing+gathering) — scope check:**
   - Verify VS2a-VS2b scope still excludes fishing/crafting mechanic.
   - If excluded: register as DEFER row in ui-icons manifest with "scope-deferred" rationale.
   - If pet-system gathering or future crafting scope opens: revisit as feature-enabler.

---

## Estimated curation time

~30-60 min post-Q6-resolution. Small footprint — neither ZIP is large; the work is overlap-classification, not new manifest authoring.

---

## Decision dependencies

- **Matt Q6:** authorize expansion + DireDungeon overlap analysis vs defer
- **Pet/gathering scope (out-of-band):** if pet-system commission lands, net-596440 becomes relevant; otherwise stays DEFER

---

*Filed 2026-05-17 by elrond per dispatch authorization. DEFERRED stub; full curation auto-fires on Matt Q6 = YES.*
