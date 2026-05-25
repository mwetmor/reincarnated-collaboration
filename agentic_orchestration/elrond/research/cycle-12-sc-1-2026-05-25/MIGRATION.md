# MIGRATION — Cycle 12 SC-1 substrate-tagging cleanup (Tier-S named-mythological items)

**Authority:** Matt 2026-05-25 Cycle 12 framing brief bulk-ratification (Q5 sidecars SC-1)
**Dispatch:** `agentic_orchestration/dispatches/2026-05-25-elrond-cycle-12-sc-1-substrate-tagging-cleanup.md`
**Executor:** elrond
**Date:** 2026-05-25
**Cross-seam scope:** data-only change on existing columns; no schema change; no fixture-dict shape change
**ADR reference:** ADR-004 (cross-seam coordination + MIGRATION.md)

---

## Summary

Backfilled `cultural_lineage_canonical` and `historical_period_canonical` on 56 Tier-S named-mythological items in `/Users/admin/Games/reincarnated-loadout/data/telemetry.db` table `weapon_knowledge_entries`. Items where canonical_name IS a named mythological/historical weapon (e.g., Indraastra, vajra, Mjölnir, Excalibur, shield of Achilles, Joyeuse, Tizona, Hyūga Masamune, Narmer Macehead) now carry canonical lineage and period assignments derived from the `named_mythological_match` bearer-tradition.

94 additional Tier-S named-mythological items DEFERRED + flagged for gandalf Pattern A-light routing — these are spurious-attribution cases (modern military hardware named-after-mythology, Royal Armouries generic-typology curatorial items, modern-fictional namedropping, museum-name attribution). See `subset-c-deferred-flagging-for-gandalf.md`.

---

## Schema changes

**None.** Both columns (`cultural_lineage_canonical`, `historical_period_canonical`) and the confidence field (`cultural_lineage_confidence`) already existed on `weapon_knowledge_entries` per Phase D Step 6.5 (2026-05-23). This is a pure data-backfill on existing columns.

---

## Data changes

### Subset A — Mythological items proper (33 rows)

Items where canonical_name is the mythological weapon itself. Tradition → canonical mapping:

| Tradition (named_mythological_match) | cultural_lineage_canonical | historical_period_canonical |
|---|---|---|
| greek (Achilles, Poseidon, etc.)     | european       | classical       |
| vedic_hindu (Indra, Arjuna, Murugan) | south_asian    | pre_classical   |
| norse (Thor, Odin, Freyr, Beowulf, Heimdall, Baldr) | european | medieval |
| european_medieval Arthurian (Arthur, Gawain, Lancelot) | european | medieval |
| european_medieval Carolingian (Charlemagne, Oliver, Tristan, Saint George) | european | medieval |
| east_asian mythological (Sun Wukong, Guan Yu, Tomoe Gozen, Tai'e) | east_asian | pre_classical or classical |

Items backfilled (Subset A, 33 rows): 11, 209, 4391, 175173, 175580, 180679, 190415, 482, 497, 5097, 5105, 5108, 5131, 5135, 5137, 5165, 924, 660, 388, 4996, 191620, 5144, 379, 387, 174017, 174145, 176853, 131, 134, 366, 385, 194198.

### Subset B — Real historical-figure weapons (23 rows)

Items where canonical_name is a real named weapon attributed to a historical figure. Period derives from the figure's era:

| Figure / class | cultural_lineage_canonical | historical_period_canonical |
|---|---|---|
| El Cid (Tizona, Colada)              | european       | medieval        |
| Japanese smith-attributed blades (Masamune, Sadamune, Yoshimitsu, Kotetsu, Norimitsu) | east_asian | early_modern (overrides regex-misfires) |
| Pharaonic Egypt (Tutankhamun, Narmer)| middle_eastern | pre_classical (overrides regex-misfires) |
| Mesopotamian (Tukulti-Ninurta I, Shulgi) | middle_eastern | pre_classical (overrides regex-misfires) |

Items backfilled (Subset B, 23 rows): 2463, 2477, 181836, 1647, 1728, 1734, 1736, 1738, 3149, 4254, 4255, 4256, 4257, 1729, 1730, 1737, 3224, 4288, 3164, 1676, 13367, 107, 634.

**Note on regex-misfire overrides:** Subset B items 1676 (Tutankhamun's blade — was 'medieval'), 107 (Tukulti-Ninurta mace — was 'contemporary'), 634 (Shulgi mace — was 'contemporary') had their `historical_period_canonical` corrected. Phase D Step 6.5's `YEAR_RE` regex matched year-like substrings in descriptions (e.g., "1207 BCE" → 1207 → 1207 CE → modern) producing misfires. Per Discipline #11 empirical inspection, elrond override applied with explicit log entry.

### Confidence promotion

`cultural_lineage_confidence` raised to 0.9 (from 0.7 or lower) for all 56 backfilled rows. Rationale: SC-1 backfill is elrond-asserted from a strong-signal source (named-mythological-bearer match + canonical_name = mythological weapon proper). Higher than the 0.7 description-regex confidence assigned by Phase D Step 6.5; lower than 1.0 to preserve the meta-signal that this is an elrond-applied backfill rather than a vendor-source-structured-tag.

### Idempotency

Backfill only overwrites fields whose current value is `'unknown'` (with the explicit exception of the 3 regex-misfire overrides in Subset B above, where the comment in the source declares `'override'`). Existing non-unknown values were preserved. Re-running the script is a no-op.

---

## Downstream consumer impact

Per `canonical/story/qd-engine-end-to-end-workflow-2026-05-24.md` Phase 5, these fields are designed to be consumed by:

- **cohesion-judge** (Phase 5; not yet implemented in engine code): for named-mythological-bearer-resonance scoring on Sketch F anchor naming. Pre-SC-1, the 56 backfilled items defaulted to generic-cultural-fallback (lineage='unknown'); post-SC-1, they carry their canonical tradition.
- **spirit-guide explainer** (Phase 5; not yet implemented): for naming-context strings on equipped items.
- **loadout app surface** (not yet implemented): may render these fields in item-tooltip / item-detail panels.

Current grep across `reincarnated-engine/src`, `reincarnated-loadout`, `reincarnated-demo` source trees shows **no production code consumers** of these columns as of 2026-05-25. Cross-seam impact is forward-looking (Architecture B Phase 5 will surface the change when Phase 5 lands). No coordinated change required from other seams now.

---

## Reproducibility

- Backfill script: `agentic_orchestration/elrond/research/cycle-12-sc-1-2026-05-25/sc1_backfill.py`
- Backfill log (full per-row before/after): `agentic_orchestration/elrond/research/cycle-12-sc-1-2026-05-25/sc1_backfill_log.json`
- Before-state snapshot (150 rows × full columns): `agentic_orchestration/elrond/research/cycle-12-sc-1-2026-05-25/before-state-150-rows.csv`
- Subset C deferral list with flagging notes: `agentic_orchestration/elrond/research/cycle-12-sc-1-2026-05-25/subset-c-deferred-flagging-for-gandalf.md`

---

## Audit

- Pre-state: 150 Tier-S rows with named_mythological_match IS NOT NULL AND (cultural_lineage_canonical='unknown' OR historical_period_canonical='unknown')
- Backfilled (Subset A + B): 56 rows; 73 field updates (lineage + period + confidence promotions)
- Post-state: 94 Tier-S rows still unknown (= Subset C deferred, exactly matches the deferral list)
- Post-audit on backfilled set: 56/56 clean — every Subset A/B row now has both lineage AND period populated to a non-unknown value.

---

## Sign-off

**Executor:** elrond
**Status:** complete
**Tag (auto-commit):** `elrond/cycle-12-sc-1-substrate-tagging-cleanup-2026-05-25`
