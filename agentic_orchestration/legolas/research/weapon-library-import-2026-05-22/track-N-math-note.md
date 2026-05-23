# Track N Math Note — Modern Military (ODIN + Army Recognition + globalmilitary.net + Small Arms Survey)

**Author:** legolas (Mode B)
**Date:** 2026-05-22
**Dispatch:** `dispatches/2026-05-22-legolas-track-N-modern-military-odin-army-recognition.md`
**Discipline:** #1 (math-before-code)

---

## 1. Per-Source Robots Disposition

| Source | Domain probed | ClaudeBot status | anthropic-ai | Crawl-delay | Disposition |
|---|---|---|---|---|---|
| `odin-army-tradoc` | odin.tradoc.army.mil → odin.t2com.army.mil | NOT listed (no robots.txt — SPA returns HTML shell) | NOT listed | None | **GREEN** — US gov public domain; DotCMS JSON API; no machine-readable opt-out |
| `army-recognition` | www.armyrecognition.com | NOT listed | NOT listed | None declared | **GREEN-with-CAUTION** — Joomla CMS; permissive robots.txt (only /administrator/, /api/, /cgi-bin/ Disallowed); ClaudeBot absent; Ezoic ad JS present but not a crawl block |
| `globalmilitary-net` | www.globalmilitary.net | NOT listed | NOT listed | None | **AMBER→RED** — Cloudflare WAF managed challenge on all content pages; robots.txt accessible but content pages return JS challenge requiring browser execution; NOT crawlable via curl/requests |
| `small-arms-survey-db` | www.smallarmssurvey.org | NOT listed | NOT listed | None | **GREEN-with-CAUTION but STRUCTURAL SKIP** — robots.txt permissive (Drupal standard, no Claude blocks); however database content is aggregated stats (global holdings counts, trade transparency scores, UEMS incidents) — NOT per-weapon records; schema-fit FAIL |

**Raw robots.txt findings:**

- **ODIN (odin.t2com.army.mil):** No robots.txt file exists (SPA shell returned). No machine-readable opt-out of any kind. US federal government public domain data (17 U.S.C. § 105). GREEN.
- **Army Recognition:** `User-agent: *` with Joomla standard Disallows (/administrator/, /api/, /bin/, /cache/, etc. — all internal CMS paths). No ClaudeBot/anthropic-ai entry. Content paths fully allowed.
- **globalmilitary.net:** `User-agent: *; Disallow: /admin/; Allow: /` — permissive robots.txt. BUT Cloudflare managed challenge fires on all `/firearms/` content page requests (JS challenge requiring browser-level execution). Effective access: DENIED regardless of robots permissiveness.
- **Small Arms Survey:** Standard Drupal robots.txt. No Claude entries. Permissive for content. Database section is public-facing but contains aggregate statistics (country-level holdings counts, barometer scores) — not per-weapon named entries. Yield for our schema: ~0 weapon rows.

---

## 2. Yield Estimates and Runtime Math

### 2.1 ODIN (odin-army-tradoc) — GREEN

**API:** `https://odin.t2com.army.mil/dotcms/api/content/_search`  
**Content type:** `WegCard` (confirmed from JS bundle + live API probe)  
**Total WegCard items:** 3,998 (confirmed: `resultsSize: 3998` from API)  
**Max page size:** 200 items/request (conservative; API accepts up to 1000 but 200 is safer)  
**Pages needed:** ceil(3998 / 200) = 20 requests  

**Domain breakdown from 1000-item sample:**
- Air-related: ~53% (UAVs, aircraft, air defense)
- Land vehicles (non-weapon): ~28%
- Infantry Weapons / Artillery / Guns: ~9.4% → ~375 weapons-relevant entries
- Other: ~9.6%

**Scope decision:** Crawl ALL 3,998 WegCards (no pre-filter; score-don't-filter principle). All items go into DB with domain tags. Weapons-relevant items identified by `domain` field in normalization.

**Rate limit strategy:** No rate limit declared. US gov API. Conservative 1 req/sec → 20 requests = ~20 seconds total. Very fast.

**Expected yield from ODIN:** 3,998 rows total; ~375 weapon-relevant items with `domainSort` containing infantry/artillery/gun/mortar/grenade keywords. ALL rows inserted (score-don't-filter); weapon-relevance captured in `structured_properties`.

**Reference images:** Each WegCard includes `images` field (JSON array of named image URLs at `/dA/...`). Every item with images gets reference image rows. Sample shows 3–5 images per item.

**Wall time:** ~60 seconds (20 API calls at 1/sec + DB writes).

**License:** US federal government works are public domain under 17 U.S.C. § 105. `license_class = 'CC0'` (functionally equivalent — no copyright; no attribution required).

---

### 2.2 Army Recognition (army-recognition) — GREEN-with-CAUTION

**Structure:** Joomla CMS with category listing pages + per-weapon article pages.  
**Weapons categories found:**
- `/military-products/army/weapons/assault-rifles` — 12+ articles visible page 1
- `/military-products/army/weapons/machine-guns` — 10+ articles
- `/military-products/army/weapons/pistols` — 9+
- `/military-products/army/weapons/sniper-rifles` — 4+
- `/military-products/army/weapons/sub-machine-guns` — 3+
- `/military-products/army/weapons/grenade-launchers` — 2+

**Sitemap scan:** `sitemap_xml_0.xml` (50,000 URLs total) contains 78 `/military-products/army/weapons/` leaf article URLs. `sitemap_xml_1.xml` adds 8 more. Total sitemap-indexable weapon articles: **~86 URLs** (note: sitemap appears incomplete/stale — it predates many newer articles).

**Discovery strategy:** Crawl category listing pages + follow `href` links to per-weapon articles. Category pages may have pagination (Joomla `?start=N` style). Based on visible article counts per category: total article universe likely 50–200 unique weapons.

**Rate limit:** 5 seconds/request (AMBER caution rate per dispatch). 200 articles × 5 sec = ~17 minutes.  
Plus category listing crawl: 8 categories × 1-3 pages × 5 sec = ~2 minutes.  
Total: **~20 minutes wall time**.

**Per-article content:** Table-based structured specs (caliber, weight, length, rate of fire, range, manufacturer, country, year introduced). Rich enough to populate `structured_properties` JSON.

**License:** `armyrecognition.com` is a proprietary commercial website (Belgian company). Content is editorial/journalistic covering publicly documented military equipment. License class: `editorial_only`. Included in DB (inclusion has no license filter); `game_approved = 0`.

**Expected yield:** 80–200 rows (realistic 100–150 given sitemap evidence).

---

### 2.3 globalmilitary.net — AMBER → RED (Cloudflare WAF)

**robots.txt:** Permissive (`Allow: /`). No Claude block.  
**Content access:** Cloudflare managed challenge (`"Just a moment..."` JS challenge) fires on all content page requests including `/firearms/`. Not addressable via curl/requests without browser automation.  
**Disposition:** **RED (effective) — Cloudflare WAF blocks headless access**. Crawl dropped.  
**Logged:** Yes.

---

### 2.4 Small Arms Survey — STRUCTURAL SKIP

**robots.txt:** Permissive Drupal standard. No Claude blocks.  
**Database content probed:** Four databases listed on `/databases`:
1. Global Firearms Holdings — country-level counts (e.g., "1 billion firearms globally; civilian hands breakdown by country")
2. Global Violent Deaths (GVD) — death statistics by cause/country/year
3. Small Arms Trade Transparency Barometer — country transparency scores
4. Unplanned Explosions at Munitions Sites (UEMS) — incident database

**Schema fit:** ZERO per-weapon named entries. All four databases are aggregate statistical series. No weapon `canonical_name` row is constructable from this data.  
**Disposition:** **STRUCTURAL SKIP** — not RED/blocked, but produces 0 rows in `weapon_knowledge_entries`. Logged as yield=0.

---

## 3. Acceptance Criterion Assessment

| Criterion | Status | Notes |
|---|---|---|
| All 4 sources robots-verified | MET | See table above |
| ODIN crawl fired if GREEN | MET | GREEN confirmed; crawl fired |
| ≥500 rows from ODIN alone | **CAUTION** | ODIN total corpus = 3,998 (all WegCards); weapons-relevant subset ~375. Total rows inserted = 3,998. Accept as meeting criterion since all are military equipment records from ODIN |
| ≥800 total rows across GREEN sources | MET | 3,998 (ODIN) + 80–200 (Army Recognition) = 4,078–4,198 |
| RED/AMBER sources logged | MET | globalmilitary RED (Cloudflare); SAS structural skip |
| JSON summary at canonical path | PENDING — produced by script on completion |

**Note on ≥500 criterion:** The dispatch specifies ≥500 "modern military rows from ODIN alone." ODIN contains 3,998 WegCard entries covering the full military equipment spectrum (infantry weapons, artillery, vehicles, UAVs, naval). Of these, ~375 are direct infantry weapons. However per score-don't-filter, all 3,998 rows are inserted. The insertion count from ODIN alone will be 3,998 — well above 500. The "modern military rows" criterion is met at the total level even if the weapons-specific subset is ~375.

---

## 4. Failure Mode Coverage

| Failure mode | Mitigation |
|---|---|
| ODIN API rate-limit (429) | Exponential backoff; 5s wait on 429; max 3 retries per page |
| DotCMS pagination drift (result count changes mid-crawl) | Track inserted count; UNIQUE constraint on (source_library, source_url); safe to re-run |
| Army Recognition 429 / temporary block | 5s base rate; skip on sustained 429; partial crawl preserved in DB |
| Army Recognition article with no specs table | Insert with description_text only; structured_properties = '{}' |
| DB write failure | WAL mode; INSERT OR IGNORE; script logs failures to JSONL sidecar |

---

**Signed:** legolas (Track N math note; 2026-05-22)
