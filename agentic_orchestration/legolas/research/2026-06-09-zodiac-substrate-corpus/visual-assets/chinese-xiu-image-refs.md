# Chinese 28 Xiu — Image References
**Crawl date:** 2026-06-09
**Used in:** corpus-chinese-xiu.yaml (all 28 entries)

---

## Primary diagram — all 28 entries

| Field | Value |
|---|---|
| URL | `https://upload.wikimedia.org/wikipedia/commons/7/75/28_xiu.svg` |
| Description | Diagram of the twenty-eight mansions of Chinese astronomy; north at top; shows all mansion positions in a circular ecliptic map |
| Creator | Mysid (Wikimedia Commons contributor) |
| Created | 2008-05-04 |
| Tool | Inkscape (based on celestial photograph) |
| Dimensions | 629 × 629 px (SVG, scalable) |
| File size | 144 KB |
| License | CC-BY-SA 3.0 Unported / GFDL 1.2+ |
| Verified loads | true (confirmed via Wikipedia article fetch 2026-06-09) |
| Commons page | https://commons.wikimedia.org/wiki/File:28_xiu.svg |

This image is used as the primary `image_url` for all 28 entries in the corpus. It provides the full-system context for each mansion's position.

---

## Four Guardians — quadrant SVG files

These files exist on Wikimedia Commons and provide per-quadrant guardian imagery. Useful for entries where quadrant context is primary.

| Guardian | File | URL |
|---|---|---|
| Azure Dragon (East) | `Azure_Dragon_of_the_East.svg` | https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Azure_Dragon_of_the_East.svg |
| Black Tortoise (North) | `Black_Tortoise_of_the_North.svg` | https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/Black_Tortoise_of_the_North.svg |
| White Tiger (West) | `White_Tiger_of_the_West.svg` | https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/White_Tiger_of_the_West.svg |
| Vermilion Bird (South) | `Vermilion_Bird_of_the_South.svg` | https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Vermilion_Bird_of_the_South.svg |

**Note:** The above thumb URLs are partial — full direct URLs require appending resolution parameters (e.g., `/800px-White_Tiger_of_the_West.svg.png`). Phase 2 should verify these load correctly and add as `image_url_secondary` entries to the 7 mansions per quadrant.

---

## Historical Chinese astronomical art

The Wikipedia article on Twenty-Eight Mansions references the following historical works depicting the 28 Xiu:

| Work | Period | Notes |
|---|---|---|
| Five Stars and Twenty-Eight Mansions (五星二十八宿神形图) | Late Sui to early Tang dynasty | Attributed to Liang Lingzan; depicts each mansion as a deity figure |
| Shilin Guangji illustration | Yuan dynasty (Chen Yuanjing) | Woodblock depiction of the 28 mansion layout |
| Shuilu ritual paintings, Baoning Temple | Ming Dynasty | Four separate paintings for the Four Guardians + mansions; full color |

These are high-value Phase 2 research targets for per-mansion deity iconography (the Five Stars work has individual deity portraits for each of the 28 mansions).

**Five Stars and Twenty-Eight Mansions — Wikimedia search:** https://commons.wikimedia.org/wiki/Special:Search?search=five+stars+twenty-eight+mansions

---

## Per-mansion star chart sources (Phase 2)

For Phase 2 star coordinate verification and individual mansion star charts:

| Source | URL | Notes |
|---|---|---|
| Wikipedia: Twenty-Eight Mansions | https://en.wikipedia.org/wiki/Twenty-Eight_Mansions | Full table + determinative stars |
| SIMBAD Astronomical Database | http://simbad.u-strasbg.fr/simbad/ | Authoritative J2000 coordinates for all stars |
| Stellarium (open source planetarium) | https://stellarium.org | Can render each mansion's asterism visually |
| Sun & Kistemaker (1997) | Book: ISBN 978-9004107373 | Primary academic source for all 28 mansions |

---

## Notes for YAML `image_url_secondary` population

Current state: all 28 entries have empty `image_url_secondary: []`.

Recommended Phase 2 additions per quadrant:
- **Azure Dragon entries (001–007):** Add Azure Dragon SVG URL
- **Black Tortoise entries (008–014):** Add Black Tortoise SVG URL
- **White Tiger entries (015–021):** Add White Tiger SVG URL
- **Vermilion Bird entries (022–028):** Add Vermilion Bird SVG URL
- **All entries:** Consider adding the Five Stars deity portrait URL for each mansion once those individual files are located on Commons
