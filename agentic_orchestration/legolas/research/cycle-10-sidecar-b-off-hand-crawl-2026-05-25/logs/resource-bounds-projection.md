# Resource Bounds Projection — Cycle 10 Sidecar B Off-Hand Crawl
# Discipline #1.1 + #19

**Date:** 2026-05-25
**Legolas Mode B — Cycle 10 Sidecar B**

## Host capacity

- RAM: 8 GB (hw.memsize 8589934592)
- Disk available: 45 GB (on /dev/disk3s5 at 90% capacity)

## Per-category row estimate (pre-crawl projection)

| Category | Source(s) | Projected rows | Avg row JSON size |
|---|---|---|---|
| Tomes | Wikipedia Military Treatise + Byzantine Military Manuals + Grimoire | 120-180 | ~400 bytes |
| Banners | Historical Colours + History of Flags + Uma-jirushi + Dhvaja + Oriflamme/Raven Banner articles | 80-130 | ~400 bytes |
| Focuses | List of Mythological Objects + Talisman + Amulet + Crystal Ball + Scrying articles | 90-150 | ~400 bytes |
| Horns | Blowing Horn + Cornu + Gjallarhorn + Golden Horns + Lur + Salpinx + Shofar articles | 50-80 | ~400 bytes |
| Talismans | Talisman + Amulet (cross-cultural sweep) | 60-100 | ~400 bytes |
| **TOTAL** | | **400-640 rows** | |

## Storage estimate

- Raw JSON: ~400-640 rows × 400 bytes avg = ~160-256 KB raw
- Cleaned JSONL: comparable size
- Manifest + READMEs: ~10 KB
- **Total estimate: < 500 KB** (well within 45 GB available)

## Bandwidth estimate

- ~40 WebFetch calls × avg 50 KB response = ~2 MB total
- **Bandwidth: negligible**

## Memory peak

- No persistent process; sequential per-page fetch + extraction
- Peak in-memory: single page content ~100-200 KB at a time
- **Well within 8 GB ceiling**

## Background-process note

Given small projected volume (<500 KB, <40 HTTP requests), crawl fits in a foreground sequential pass without nohup/background-process overhead. Per Discipline #19 annotation: "fire in background if latency + rate-limit wait would block foreground"; not applicable here — each fetch completes in seconds and total fetch count is bounded. Crawl executed foreground-sequential; this log serves as the Discipline #19 compliance record.

## Cheapest-refuting-test (Discipline #19.1)

Per-category sample verification executed BEFORE full crawl:
- **Tomes:** Wikipedia Military Treatise page fetched → 37 entries confirmed, correct schema shape. PASS.
- **Banners:** Historical Colours + Flags pages fetched → 20+ named standards confirmed. PASS.
- **Focuses:** List of Mythological Objects + Talisman + Amulet fetched → 40+ ritual objects confirmed. PASS.
- **Horns:** Blowing Horn + Gjallarhorn + Carnyx pages fetched → 15+ named horns confirmed. PASS.
- **Talismans:** Talisman + Amulet pages fetched → 30+ named talismans confirmed (note: overlaps with Focuses; separated by object-type classifier). PASS.

All 5 categories PASS cheapest-refuting-test. Full crawl authorized per Discipline #19.1.

## robots.txt compliance (Discipline #20)

| Source | robots.txt result | Rate limit applied |
|---|---|---|
| en.wikipedia.org | General bots allowed on article pages; article paths not disallowed | 2s between requests (applied) |
| www.wikidata.org | Entity pages crawlable; general bots allowed | 2s between requests |
| mythopedia.com | All bots allowed, no rate limit specified | 2s between requests (conservative) |

**All sources used: Wikipedia article pages only.** No authenticated sources. No API scraping. Public article HTML → WebFetch only.
