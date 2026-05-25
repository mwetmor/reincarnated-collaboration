# Gandalf Curation Review Request — Cycle 10 Sidecar B Off-Hand Crawl

**From:** legolas (Mode B crawl)
**To:** gandalf (via knight-rider routing per dispatch § 3.5)
**Date:** 2026-05-25
**Dispatch authority:** `agentic_orchestration/dispatches/2026-05-25-elrond-cycle-10-sidecar-b-off-hand-substrate.md` § 3.5

---

## Request

30-row cross-category curation review: 5 rows per category spanning all 6 off-hand categories (shields excluded from legolas crawl; elrond handles shields via existing-source mining).

Crawl output path: `agentic_orchestration/legolas/research/cycle-10-sidecar-b-off-hand-crawl-2026-05-25/`

Total crawl yield: **132 rows** across 5 categories (48 tomes + 34 banners + 30 focuses/talismans + 20 horns).

---

## Review scope per dispatch § 3.5

- Pass threshold: **≥ 24/30 sensible per-category classification + cultural-tradition + period**
- Output target: `agentic_orchestration/gandalf/notes/2026-05-25-sidecar-b-curation-review.md`
- Timing: deferred until elrond existing-source mining also completes (knight-rider proposes single-batch review covering both crawl + mining rows)

---

## Suggested 30-row sample (5 per category)

### Tomes (5 rows)
1. `tome-001` — The Art of War (Sun Tzu; Chinese; tactical)
2. `tome-010` — De Re Militari (Vegetius; Roman/Byzantine; foundational medieval military text)
3. `tome-011` — Strategikon of Maurice (Byzantine; comprehensive military manual)
4. `tome-022` — Key of Solomon (European/Jewish; arcane grimoire)
5. `tome-043` — Book of Five Rings (Japanese; Miyamoto Musashi; swordsmanship/strategy)

### Banners (5 rows)
1. `banner-001` — Oriflamme (French royal battle standard)
2. `banner-002` — Raven Banner (Norse/Viking; Odin-associated)
3. `banner-013` — Kapi Dhvaja / Arjuna's Banner (Hindu; Mahabharata; Hanuman emblem)
4. `banner-010` — Tugh (Mongol/Ottoman horsetail standard)
5. `banner-032` — Kartikeya's Peacock Banner (Hindu war-god's divine banner)

### Focuses (5 rows)
1. `focus-004` — Cup of Jamshid (Persian mythological scrying vessel)
2. `focus-007` — Sampo (Finnish magical artifact)
3. `focus-001` — John Dee's Crystal Ball (European Renaissance divination focus)
4. `focus-008` — Yasakani no Magatama (Japanese imperial sacred jewel; living-tradition flag)
5. `focus-020` — Aphrodite's Cestus (Greek mythological magical girdle)

### Talismans (5 rows — distinguished by weapon_kind:"talisman" in focuses file)
1. `focus-009` — Eye of Horus (Egyptian protective amulet)
2. `focus-013` — Hamsa (Jewish/Islamic hand protective amulet)
3. `focus-014` — Seal of Solomon (multi-religious protective emblem)
4. `focus-015` — Talisman of Charlemagne (European Carolingian reliquary)
5. `focus-017` — Fulu (Chinese Taoist protective script)

### Horns (5 rows)
1. `horn-001` — Gjallarhorn (Norse; Heimdallr's Ragnarök herald)
2. `horn-002` — Oliphant (French medieval; Roland's horn)
3. `horn-008` — Carnyx (Celtic Iron Age war trumpet)
4. `horn-010` — Cornu (Roman military signal instrument)
5. `horn-017` — Golden Horns of Gallehus (Germanic; 5th-century sacral gold horns)

---

## Cultural sensitivity items for gandalf attention

The following rows carry cultural-sensitivity flags and require gandalf sign-off before v1_scope inclusion:

| Asset ID | Name | Flag | Recommended action |
|---|---|---|---|
| `tome-045` | Book of Shadows (Wiccan) | Living religious tradition | Substrate only; exclude from player-facing form naming |
| `focus-008` | Yasakani no Magatama | Shinto imperial regalia; living tradition | Substrate only; use generic "imperial jade jewel" for player-facing naming |
| `focus-012` | Dorje (Vajra) | Tibetan Buddhist ritual object; living tradition | Substrate only; generic "diamond scepter" acceptable if de-contextualized |
| `focus-018` | Ofuda | Shinto talisman; living tradition | Substrate only |
| `focus-026` | Prayer Wheel | Tibetan Buddhist; living tradition | Substrate only |
| `horn-003` | Shofar | Jewish ritual; living tradition | Substrate only for religious context; generic "ram's horn" acceptable |
| `horn-006` | Dungchen | Tibetan Buddhist; living tradition | Substrate only |
| `horn-018` | Shanka | Hindu sacred conch; living tradition | Substrate only for sacred context; "war conch" generic acceptable |

All 8 items follow Q-B § 3.2 cultural-sensitivity stratification (living religious tradition = substrate-resident but NOT player-facing form naming).

---

## Dedup note for elrond

Two banner rows flagged as duplicates from different source pages:
- `banner-021` (Roman Aquila, sourced from History of Flags) overlaps with `banner-004` (Roman Aquila, sourced from Aquila_(Roman) article)
- `banner-033` (Labarum, sourced from History of Flags) overlaps with `banner-008` (Labarum, sourced from Labarum article)

Recommendation: retain the more detailed row from dedicated article; drop the flags-context duplicate at DB insert time.

---

## Knight-rider routing note

Per dispatch § 3.5: gandalf curation review fires AFTER both legolas Mode B crawl (this document) AND elrond existing-source mining are complete. Knight-rider routes this request to gandalf once elrond signals mining complete. Do not fire curation review before elrond mining result is available — combined 30-row sample should include rows from both sources.

**Legolas Mode B crawl: COMPLETE.**
