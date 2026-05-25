# Subset C — DEFERRED Tier-S named-mythological items (flagged for gandalf Pattern A-light)

**Authority:** Matt 2026-05-25 Cycle 12 framing brief bulk-ratification (Q5 sidecars SC-1)
**Routing per dispatch:** KR routes to gandalf for Pattern A-light if elrond surfaces ambiguous items
**Dispatch trigger:** "If you surface items where canonical tagging is ambiguous (e.g., culturally-cross-pollinated items, multi-tradition items, ...), DEFER those specific items + flag to KR for gandalf Pattern A-light routing rather than guessing."

---

## Why these are deferred

Per Discipline #11 (empirical inspection), elrond direct-inspected all 150 Tier-S unknown rows and found three subsets:

- **Subset A (33 rows)** — mythological items proper; canonical_name IS the named mythological weapon (Indraastra, vajra, Mjölnir, Excalibur, etc.). Backfilled.
- **Subset B (23 rows)** — real historical-figure weapons attributed to historical figures; canonical_name IS a real named weapon (Tizona, Hyūga Masamune, Tutankhamun's blade, etc.). Backfilled.
- **Subset C (94 rows)** — DEFERRED. The `named_mythological_match` attribution is **NOT** load-bearing for Sketch F anchor-naming because the canonical_name is either generic-typology (RA "Pike"/"Print"/"Sword"/"Painting"), modern military hardware that namedrops mythology in its branding ("Agni-II", "M982 Excalibur", "Bharat-52", "M142 HIMARS"), modern-fictional ("Mjolnir (comics)", "Hammer of Thor" [TMNT 1987]), or spurious museum-name attribution (Musée Saint-Raymond items tagged via museum name "Raymond of Toulouse").

For Subset C, asserting a canonical tradition would **propagate the metadata-spurious-attribution into downstream cohesion-judge / spirit-guide / Sketch F anchor naming**, generating named-mythological-bearer-resonance scores on items where the attribution is name-only or modern-derivative. This is precisely the "named-mythological-bearer-resonance over-fire" risk that Cycle 12 SC-1 cleanup was meant to prevent in the *opposite direction* (avoid generic-cultural-fallback for canonical items) — but mirror-applied: avoid named-mythological-bearer-resonance for spurious-attribution items.

---

## Recommended dispositions (for gandalf to confirm or override via Pattern A-light)

### Disposition 1 — Modern military hardware named-after-mythology (~52 rows)

**Examples:** Agni-II/IV/V/VI/P (modern Indian missiles), M982 Excalibur (guided artillery), M142 HIMARS (Hercules-aircraft-mention), Operation Aphrodite (WWII codename), Bharat-52 (Garuda-tagged), Nike Hercules, Nike Zeus, Trident (missile), Harpoon (missile), THeMIS, Otomat, Katyusha rocket launcher, Mark 7 nuclear bomb (Thor-codename), etc.

**Recommended disposition:** Treat as Class C — drop the named_mythological_match attribution as load-bearing for Sketch F anchor-naming. Set `cultural_lineage_canonical` and `historical_period_canonical` via standard Phase D regex pipeline (most of these already have lineage populated; only period is unknown — could be filled with `contemporary` or `modern` based on description-text era extraction).

**Alternative disposition (if gandalf prefers):** Strip the `named_mythological_match` from these specific rows so downstream consumers never see them as named-mythological-bearer items. This would require an additional MIGRATION.md and explicit elrond execution.

### Disposition 2 — Royal Armouries generic-typology curatorial items (~34 rows)

**Examples:** Pike, Pollaxe, Partizan, Print, Painting, Wooden head, Helm, Sword, Gun, Equestrian mannequin — all attributed to historical figures by depiction (paintings/prints depicting Henry VIII, Black Prince, Edward III, etc.) or by temporal-association (pikes from Henry VIII's reign).

**Recommended disposition:** Treat as Class C — these are generic-typology RA items, not named-mythological-bearer items. The named_mythological_match attribution is curatorial-context, not weapon-identity. For Henry VIII pikes etc., assignable to `cultural_lineage_canonical='european'` and `historical_period_canonical='early_modern'` if SC-1 scope is expanded to include them, BUT the named-bearer-resonance signal for Sketch F should NOT apply (the named bearer isn't the weapon's identity).

**Alternative disposition:** If gandalf judges that RA Henry-VIII-attributed pikes ARE Sketch-F-anchor-naming-worthy (e.g., "Pike of Henry VIII's Yeomen of the Guard" as flavor naming), then backfill them as Class B. This is a design judgment, not an empirical-inspection judgment.

### Disposition 3 — Modern-fictional namedropping mythology (3 rows)

**Examples:**
- 532 "Hammer of Thor" — fictional weapon from 1987 TMNT series
- 603 "Dark Elf Particle Rifle" — Marvel Thor: Dark World fictional
- 606 "Asgardian Cannon" — Marvel Thor: Dark World fictional
- 175456 "Mjolnir (comics)" — Marvel Comics fictional Mjolnir

**Recommended disposition:** Treat as Class C — set `cultural_lineage_canonical='fantasy_generic'` and `historical_period_canonical='fictional'` per Phase D Step 6.5's source-library fallback for fictional-source rows. Strip named_mythological_match to prevent Sketch F over-fire.

### Disposition 4 — Spurious museum-name attribution (3 rows)

**Examples:**
- 77 "Q88199410" — wikidata stub item in Musée Saint-Raymond, "Raymond of Toulouse" matched via museum-name
- 1006 "Musée Saint-Raymond, D 78 6 6"
- 1530 "Musée Saint-Raymond, Niel 2463 n°6"

**Recommended disposition:** Strip named_mythological_match (the bearer-match is on the museum's name, not the item's substantive provenance). These are museum-catalogue stubs — could be tagged as European medieval (Musée Saint-Raymond holdings are predominantly Languedoc medieval) but cultural-lineage assignment is low-confidence.

### Disposition 5 — Depictive-not-substantive (1 row)

**Example:**
- 46 "Shield Depicting Saint George Slaying the Dragon" — 19th-century industrial-era shield depicting the Saint George legend; named-bearer is depiction-content, not weapon-identity.

**Recommended disposition:** Set `cultural_lineage_canonical='european'`, keep `historical_period_canonical='industrial'`. Optionally strip named_mythological_match.

### Disposition 6 — Genuinely-ambiguous tradition items (0 rows from this audit)

None of the 94 deferred rows fit the "culturally-cross-pollinated / multi-tradition" pattern the dispatch open question #1 anticipated (e.g., Sudarshana Chakra Vedic-vs-Hindu-classical ambiguity). The dispatch named Brahmastra, Sudarshana Chakra, and Aegis as examples, but those items are **Tier-B/C, not Tier-S** (out of SC-1 scope per dispatch §6).

**Tier-A/B/C items elrond surfaced that would benefit from cleanup in v1.1+ per scope-doc §6:**
- id=1 aegis (Tier-C, european, unknown) — Greek mythological aegis
- id=173926 Aegis (Tier-B, european, unknown) — Greek mythological
- id=409 Sudarshana Chakra (Tier-C, south_asian, unknown) — Vedic-Hindu mythological
- id=176479 Sudarshana Chakra (Tier-B, south_asian, unknown)
- id=481 Brahmastra (Tier-C, unknown, unknown)
- id=175231 Brahmastra (Tier-B, east_asian, unknown)
- id=182128 Kimber Aegis (Tier-B, european, unknown) — modern firearm namedrop

Per scope-doc §6, Tier-A/B/C deferred to v1.1+ unless gandalf flags critical.

---

## Subset C complete enumeration

For full per-row dispositions, see `sc1_backfill_log.json` field `subset_c_deferred_list` — 94 rows with id, canonical_name, source_library, and dispatch comment.

---

## Sign-off

**Author:** elrond (data steward)
**Routing target:** knight-rider → gandalf (Pattern A-light) for disposition confirmation
**Status:** FLAGGED — Subset C dispositions are recommended but not authoritative. Gandalf judgment requested before any of the Subset C rows are touched in a follow-on dispatch.
