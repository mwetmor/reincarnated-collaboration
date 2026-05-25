# Mythological-NULL Rescue — Cycle 10 Stage 4
# Per-row rationale + rep-audit Mode B/C contamination check

**Date:** 2026-05-25
**Author:** rocket
**Authority:** Dispatch § 3.3 + composition policy v1 § 1.4
**Scope:** ~30 mythological-register NULL-typed rows (pre-Stage 4: proxy_range_class IS NULL + register_canonical = 'mythological')
**Actual rescued:** 14 rows (wikipedia source mythological NULL-typed)
**Note:** An additional ~23 rows are mythological-register engine_authored_gap_fill_v1 entries (Stage 3.5 Gap-fill, already typed pre-Stage 4) and appear in weapon_sim_props but are not "rescues" — they had proxy columns pre-populated.

---

## Rep-audit summary (Discipline #25)

**Mode B/C contamination check result:** CLEAN

- No mythological-register NULL-typed rows have `historical_period_canonical = 'fictional'`
- All 14 rescued rows are historically-mythological (not fictionally-mythological Marvel/modern variants)
- The concern flagged by the consult (Mjolnir 1962 = Marvel Comics wikidata row) does NOT apply here: the wikidata Mjölnir entry (id=379) had proxy columns already populated pre-Stage 4 (typed by Stage 1); it was NOT in the NULL-typed rescue set
- The 14 rescued rows are all wikipedia-source, and are classical mythological weapons (Celtic, Norse, Indian Vedic, Welsh Arthurian traditions)

**Mode B contamination check (fantasy-register items misclassified as mythological):**
- None found. All 14 items are documented mythological weapons from pre-classical/classical traditions.

---

## Per-row classification rationale

### 1. Aegis (id: 173926) — wikipedia
- **Classification:** melee / AoE / low / WIS
- **Rationale:** The Aegis is the divine shield of Athena/Zeus — a defensive/protective artifact. LLM correctly identified its divine WIS alignment and AoE protective effect. Shield-class items are melee-range by default. low-tempo reflects the weight/ceremony of a divine shield.
- **Confidence:** 0.60 (borderline — divine artifact; shield framing vs weapon framing)
- **sim_viable:** 1
- **Rep-audit:** CLEAN — classical Greek mythological artifact; no Mode B/C contamination

### 2. Excalibur (id: 173935) — wikipedia
- **Classification:** melee / single / medium / STR
- **Rationale:** Arthurian sword. STR/melee/single/medium is canonical. High confidence.
- **Confidence:** 0.90
- **sim_viable:** 1
- **Rep-audit:** CLEAN — Arthurian medieval mythology; distinct from fictional Excalibur variants

### 3. Gungnir (id: 173990) — wikipedia
- **Classification:** mid / single / high / STR
- **Rationale:** Odin's divine spear. Spear → mid range. High-tempo reflects Odin's precision throwing (infinite-returning divine throw). STR for thrown-spear classification.
- **Confidence:** 0.90
- **sim_viable:** 1
- **Rep-audit:** CLEAN — Norse mythology (pre-classical tradition)

### 4. Gáe Bulg (id: 173997) — wikipedia
- **Classification:** mid / multi-hit / low / STR
- **Rationale:** Celtic spear of Cú Chulainn. Dispatch explicitly flags this for canon-respecting treatment (curse-causality). The multi-hit classification captures the lore property that Gáe Bulg's barbs spread upon impact, causing multiple wounds. Low tempo reflects the deliberate, cursed throw. Mid range is correct for thrown spear.
- **Confidence:** 0.70 (multi-hit interpretation of lore property is an LLM inference)
- **sim_viable:** 1
- **Notes for gandalf Tier-S pass:** Gáe Bulg multi-hit/low-tempo profile is correct per lore; confirm the curse-causality is handled at Phase 5 cohesion level, not mechanical tag level
- **Rep-audit:** CLEAN — Celtic mythology (Iron Age Ireland tradition)

### 5. Tyrfing (id: 173998) — wikipedia
- **Classification:** melee / single / medium / STR
- **Rationale:** Norse cursed sword. Standard sword classification.
- **Confidence:** 0.90
- **sim_viable:** 1
- **Rep-audit:** CLEAN — Norse mythology

### 6. Gram (mythology) (id: 174013) — wikipedia
- **Classification:** melee / single / medium / STR
- **Rationale:** Sigurd's dragon-slaying sword from Norse/Germanic mythology. Standard sword.
- **Confidence:** 0.90
- **sim_viable:** 1
- **Rep-audit:** CLEAN — Norse/Germanic mythology

### 7. Mjölnir (id: 174103) — wikipedia
- **Classification:** melee / AoE / high / STR
- **Rationale:** Thor's hammer. melee/AoE/STR consensus. LLM selected high-tempo (fast return lightning-throw interpretation). Consult suggested low-tempo (heavy hammer throw). Both interpretations valid; high-tempo matches ARPG-genre Thor representation (rapid lightning smashes). Flagged for gandalf Tier-S curation pass to finalize tempo classification.
- **Confidence:** 0.90
- **sim_viable:** 1
- **Notes for gandalf Tier-S pass:** Confirm tempo=high or low based on game-design intent for Mjölnir archetype
- **Rep-audit:** CLEAN — Norse mythology. The wikidata entry (id=379) is a SEPARATE v1_scope entry with proxy columns already populated (not a NULL rescue). This wikipedia entry is the correctly-classified mythological Mjölnir.

### 8. Ruyi Jingu Bang (id: 174314) — wikipedia
- **Classification:** mid / single / medium / STR
- **Rationale:** Sun Wukong's transforming staff. LLM correctly identified as staff/melee-polearm type → mid range, STR for warrior. The wikidata entry (id=388) is mis-classified as DEX/ranged due to incorrect weapon_type='gun' in wikidata structured properties. The wikipedia entry (this one) is the correct classification.
- **Confidence:** 0.85
- **sim_viable:** 1
- **Notes for anomaly:** Both Ruyi Jingu Bang entries (wikidata + wikipedia) are v1_scope. The wikidata entry (388) should have its sim_props corrected at gamora pass or gandalf Tier-S review. See anomaly 1 in mechanical-tagging-report.md.
- **Rep-audit:** CLEAN — Chinese mythology (Journey to the West; classical mythology tradition)

### 9. Fragarach (id: 174315) — wikipedia
- **Classification:** melee / single / medium / STR
- **Rationale:** Irish/Celtic sword of Manannan mac Lir. Standard sword classification.
- **Confidence:** 0.70
- **sim_viable:** 1
- **Rep-audit:** CLEAN — Celtic mythology (Iron Age Ireland)

### 10. Caladbolg (id: 174553) — wikipedia
- **Classification:** melee / cleave / high / STR
- **Rationale:** Ulster Cycle mythological two-handed sword known for sweeping blows. Cleave geometry matches the sword's lore description of clearing a wide swath. High-tempo is LLM interpretation; cleave+high matches ARPG berserker archetype.
- **Confidence:** 0.85
- **sim_viable:** 1
- **Rep-audit:** CLEAN — Irish mythology (Ulster Cycle)

### 11. Gandiva (id: 175065) — wikipedia
- **Classification:** ranged / multi-hit / high / DEX
- **Rationale:** Arjuna's divine bow from Mahabharata. ranged/DEX consensus. Multi-hit captures Arjuna's rapid-fire divine archery lore (multiple arrows simultaneously per Mahabharata). High-tempo consistent with divine archer archetype.
- **Confidence:** 0.90
- **sim_viable:** 1
- **Rep-audit:** CLEAN — Vedic/Hindu mythology (Epic Period; Mahabharata)

### 12. Sudarshana Chakra (id: 176479) — wikipedia
- **Classification:** ranged / AoE / high / WIS
- **Rationale:** Vishnu's divine spinning disc weapon. LLM chose WIS (divine attribute of Vishnu as cosmic preserver) + AoE (returning-disc attack radius). Consult suggested DEX/scatter (chakram). Both defensible. WIS framing gives the item a distinct ARPG identity vs standard DEX/scatter chakram. AoE (not scatter) reflects the returning-disc beam interpretation. High-tempo = fast divine rotation.
- **Confidence:** 0.85
- **sim_viable:** 1
- **Notes for gandalf Tier-S pass:** Review WIS vs DEX framing for design intent. WIS aligns with Vishnu's cosmic-preserver role; DEX aligns with the physical chakram-throw archetype. Recommend WIS unless design wants Sudarshana to fill a specific DEX/scatter cell.
- **Rep-audit:** CLEAN — Hindu mythology (Vedic/Puranic tradition)

### 13. Skofnung (id: 176701) — wikipedia
- **Classification:** melee / single / medium / STR
- **Rationale:** Norse legendary sword. Standard sword classification.
- **Confidence:** 0.90
- **sim_viable:** 1
- **Rep-audit:** CLEAN — Norse mythology

### 14. Shield of Achilles (id: 176861) — wikipedia
- **Classification:** melee / AoE / low / STR
- **Rationale:** The Shield of Achilles from the Iliad is a legendary artifact described in elaborate detail. As a shield, melee range is correct. AoE reflects the shield's described radiating divine protection. STR because Achilles is the quintessential STR warrior archetype. Low-tempo for a heavy shield.
- **Confidence:** 0.60 (shield framing; defensive item)
- **sim_viable:** 1
- **Notes:** This shield is an iconic narrative artifact, not primarily a weapon. Its weapon_sim_props population reflects the "secondary item with combat utility" framing per composition policy § 1.4 legendary-tier secondary items.
- **Rep-audit:** CLEAN — Greek mythology (Bronze Age / Trojan War tradition)

---

## Composition trace update

All 14 rescued rows had `v1_scope_composition_trace` updated to include:
```json
{
  "stage_4_mythological_rescue": "complete",
  "stage_4_rescue_pass": "pass3_llm"
}
```

All 14 rows enter v1_scope at legendary-tier per Architecture B substrate-as-base-type-templates + tiered-instance-loot (as per composition policy § 1.4).

---

## Items flagged for gandalf Tier-S curation pass

From the mythological-NULL rescue set:
1. **Gáe Bulg** — multi-hit/low-tempo lore-accurate; confirm curse-causality at Phase 5 level (not mechanical tag level)
2. **Mjölnir** (wikipedia, id=174103) — tempo=high (LLM) vs tempo=low (consult); design choice for ARPG Mjölnir archetype
3. **Sudarshana Chakra** — WIS/AoE (LLM) vs DEX/scatter (consult); design choice for weapon identity
4. **Ruyi Jingu Bang** (wikidata, id=388) — anomalous DEX/ranged from wikidata 'gun' weapon_type error; override to STR/mid recommended

Additional mythological items (already typed pre-Stage 4; from Stage 1 typed set) that warrant Tier-S gandalf spot-check per dispatch § 4.2:
- Excalibur (wikidata, id=5108) — melee/single/medium/STR (standard; confirmed)
- Gungnir (wikidata, id=387) — mid/single/medium/STR (confirmed)
- Gandiva (wikidata, id=482) — ranged/single/high/DEX (confirmed)
- Mjölnir (wikidata, id=379) — pre-Stage 4 typed; classification to verify

---

## Summary statistics

- Total mythological-register v1_scope entries: 37 (including Stage 3.5 engine-authored)
- Previously NULL-typed (rescued this Stage): 14 (wikipedia source)
- Previously typed (Stage 1): 7 (wikidata source with proxy columns populated)
- Engine-authored gap-fill mythological (Stage 3.5): 16 (Gilgamesh 7, Karna 5, Moctezuma 3 staves, Roland 1 horn)
- All 37 now have weapon_sim_props rows; ZERO mythological-register entries without sim props
