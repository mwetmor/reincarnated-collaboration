# Research — Meshy Discover Page Crawl Feasibility Probe — 2026-05-22

**Mode:** A (analytical)
**Commissioner:** gandalf (authorized by Matt 2026-05-22 evening)
**Probe scope:** Bounded technical feasibility assessment — NOT an authorization to crawl
**Sources consulted:**
- https://www.meshy.ai/discover?kind=model&sort=public_popularity&view=recommended (fetched 2026-05-22)
- https://www.meshy.ai/robots.txt (fetched 2026-05-22)
- https://www.meshy.ai/privacy-policy (fetched 2026-05-22)
- https://www.meshy.ai/terms-of-use (fetched 2026-05-22)
- https://www.meshy.ai/acceptable-use-policy (fetched 2026-05-22)
- https://www.meshy.ai/3d-models/01939d54-48a0-7c65-b7ec-3bf29ebf7255 (sample model page, fetched 2026-05-22)
- https://www.meshy.ai/sitemap-models.xml (fetched 2026-05-22)
- https://www.meshy.ai/sitemap-models-en-1.xml.gz through -9 (sampled, fetched 2026-05-22)
- https://docs.meshy.ai/en/api/rate-limits (fetched 2026-05-22)

---

## Summary

The `/discover` page itself is technically unreachable for structured data extraction without JavaScript rendering — it delivers a client-side shell with no inline model data. However, a structurally superior alternative exists: Meshy publishes a public sitemap index at `sitemap-models.xml` containing approximately 365,000 model URLs across 9 English-language shards, and each individual model page at `/3d-models/<uuid>` delivers rich JSON-LD structured data (name, author, tags, license, formats, image URL, date) in fully static HTML without requiring JS execution. The discover-page route is the wrong entry point; the sitemap-plus-per-page-fetch route is technically viable.

The critical blocking finding is in `robots.txt`: `User-agent: ClaudeBot` and `User-agent: anthropic-ai` both have `Disallow: /` applied, constituting an explicit machine-readable directive that Claude agents must not crawl this domain. Any production crawl using Claude tooling would violate this directive. This is a hard constraint regardless of the technical viability findings.

---

## Findings

### 1. Discover Page: HTTP Status and Rendering Architecture

**HTTP status:** 200 OK
**Content-Type:** text/html; charset=utf-8
**Cache-Control:** `private, no-cache, no-store, max-age=0, must-revalidate`
**Powered-by:** Next.js (confirmed in response headers)
**Approximate page weight:** ~1.3 MB per individual model page (confirmed by fetching a sample model page)

The discover page response is a Next.js application shell. The HTML body contains:

```html
<template data-dgst="BAILOUT_TO_CLIENT_SIDE_RENDERING"></template>
```

Two instances of `BAILOUT_TO_CLIENT_SIDE_RENDERING` appear in the discover-page response. This is Next.js's explicit marker that the component bailed out of server-side rendering and will render entirely client-side via JavaScript. There is no `__NEXT_DATA__` JSON blob present. No per-model data (title, author, thumbnail, counts, tags) is embedded in the static HTML.

The discover page is a JS-rendered shell. It cannot be parsed for model metadata without browser automation (Playwright or equivalent) that executes JavaScript after page load.

**Notable infrastructure signal:** The `connect-src` CSP header contains numerous localhost entries (`http://localhost:5324` through `5330`, `8080`, `9000`, `3700`, `3702`, `3800`, `54321`), indicating this is a development-mode build or the production build was compiled with dev CSP. This does not affect crawl feasibility but is notable.

Cookie injection on first load: Meshy sets `statsig-stable-id`, `client_ip`, and `geo_country` cookies immediately. The `statsig-stable-id` is a session identity cookie that persists for one year. This indicates Meshy tracks unique requestors from first contact.

### 2. Individual Model Pages: Static JSON-LD — The Viable Data Source

Individual model pages at `https://www.meshy.ai/3d-models/<uuid>` deliver rich structured data in static HTML without JavaScript execution.

**Confirmed JSON-LD schema (`@type: 3DModel, Product`) present in static HTML:**

```json
{
  "@context": "https://schema.org",
  "@type": ["3DModel", "Product"],
  "@id": "https://www.meshy.ai/3d-models/01939d54-48a0-7c65-b7ec-3bf29ebf7255",
  "name": "Game Assets, Medieval, Polished, ..., Stone Sculpture of a Christmas Present",
  "description": "Download free 3D models as fbx, obj, glb, usdz, stl, blend formats...",
  "image": "https://api.meshy.ai/misc/cdn-images/.../output/preview.png?sign=...",
  "url": "https://www.meshy.ai/3d-models/...",
  "author": {"@type": "Person", "name": "CoolPuzzler"},
  "keywords": "medieval, sculpture, christmas, stone, detailed, realistic, game, assets...",
  "additionalProperty": [{"name": "Rigged", "value": "No"}],
  "encoding": [
    {"name": "GLB Format", "encodingFormat": "model/gltf-binary"},
    {"name": "FBX Format"},
    {"name": "OBJ Format"},
    {"name": "STL Format"}
  ],
  "offers": {"price": "0", "priceCurrency": "USD", "availability": "InStock"},
  "aggregateRating": {"ratingValue": "4.8", "ratingCount": "2117"},
  "license": "https://creativecommons.org/publicdomain/zero/1.0/",
  "category": "ArtAbstract",
  "dateCreated": "2024-12-06T18:59:40.754Z"
}
```

**Also confirmed in static HTML:** Open Graph tags including `og:title`, `og:description`, `og:url`, `og:image`. The `og:image` URL points to a server-side rendered OG image at `https://www.meshy.ai/api/3d-models-og-image/<uuid>`.

**Fields present per model via JSON-LD:**
- `@id` / URL (UUID-based)
- `name` (full prompt-style name with tags embedded)
- `author.name` (creator username)
- `image` (CDN preview PNG, signed URL)
- `keywords` (comma-separated, includes model-type and categorical tags)
- `encoding` (available download formats: GLB, FBX, OBJ, STL)
- `license` (CC0 URL confirmed for this sample)
- `category` (broad category)
- `dateCreated` (ISO timestamp)
- `aggregateRating.ratingValue` and `ratingCount`
- `additionalProperty` (rigged: yes/no)
- `offers.price` (0 = free)

**Fields NOT present in static HTML:**
- Individual like/view counts as discrete numbers
- Download counts
- Tags as a structured array (tags are embedded in the `name` field and `keywords` string only)
- Model dimensions / polygon count
- File size
- Any weapon-specific categorical metadata

The signed `image` URL (with `sign=` parameter and Unix timestamp expiry) means preview images expire and would need re-fetching periodically if used for asset display.

### 3. Sitemap: Scale and Structure

`https://www.meshy.ai/sitemap-models.xml` is a sitemap index containing 234 child sitemaps across 26 languages. English alone has 10 shards (unnumbered + 1 through 9).

**Verified shard sizes (English):**
- Shard 1: 45,000 model URLs
- Shard 9: ~36,387 model URLs (final shard, partially full)

**Estimated total English model count:** ~365,000 models (9 shards, averaging ~40,000 each). This is public models only — the total Meshy catalog across all languages/private models is likely larger.

**Model URL format:** `https://www.meshy.ai/3d-models/<uuid-v7>` (UUID v7 = timestamp-sortable). The UUIDs are lexicographically ordered by creation time, which means shard files are effectively sorted by creation date — useful for incremental crawl strategies.

**Sitemap metadata per entry:** URL, `lastmod` date, `changefreq: weekly`, `priority: 0.6`. No title or other metadata in the sitemap itself.

**robots.txt disallows `/*?kind=` and `/*?page=`** — the query parameters used by the discover page URL are explicitly blocked by robots.txt. This reinforces that the discover page route is both technically hollow (JS shell) and robots-disallowed.

### 4. robots.txt — Full Findings

Fetched verbatim. Key findings:

**General access (`User-agent: *`):**
- `Allow: /` (base rule — the site is not globally blocked)
- `Disallow` list covers: `/workspace/`, `/settings/`, `/shared-workspace`, `/g2-review`, `/s/*` (short URLs), and 21 language-prefixed variants of the same
- Query parameter blocks (relevant to discover page use case):
  - `Disallow: /*?kind=` — blocks `?kind=model` parameter
  - `Disallow: /*?page=` — blocks `?page=N` pagination parameter
  - `Disallow: /*?tab=`, `/*?sort=` not listed but `/*?kind=` and `/*?page=` are blocked
  - `Disallow: /*?showcaseId=`, `/*?utm_source=`, `/*?noRedirect=`, `/*?via=`, `/*?showcase=`, `/*?_rsc=`, `/*?collection_name=`, `/*?download=`

**No Crawl-delay specified.** No crawl delay directive appears anywhere in the robots.txt.

**Bot-specific full blocks:**
```
User-agent: GPTBot
Disallow: /

User-agent: ClaudeBot
Disallow: /

User-agent: anthropic-ai
Disallow: /
```

These three entries constitute an explicit machine-readable block against OpenAI's GPTBot, Anthropic's ClaudeBot, and the `anthropic-ai` user-agent string. The `/discover` path is doubly blocked: by the `?kind=` query parameter disallow (for the parameterized discover URL) and by the `ClaudeBot` / `anthropic-ai` full-site disallow.

The base `User-agent: *` rule does NOT block `/discover` or `/3d-models/*` paths directly — those paths are allowed for general crawlers. Only the specific AI agent user-agents receive full-site blocks.

**Sitemaps listed:**
```
Sitemap: https://www.meshy.ai/sitemap-blog.xml
Sitemap: https://www.meshy.ai/sitemap-features.xml
Sitemap: https://www.meshy.ai/sitemap-3d-tools.xml
Sitemap: https://www.meshy.ai/sitemap-static.xml
Sitemap: https://www.meshy.ai/sitemap-tags.xml
Sitemap: https://www.meshy.ai/sitemap-models.xml
Sitemap: https://help.meshy.ai/sitemap.xml
```

### 5. Terms of Service and Acceptable Use Policy — Relevant Clauses

**TOS URL:** https://www.meshy.ai/terms-of-use (the URLs `/terms`, `/terms-of-service`, `/legal` all 404; the correct URL is `/terms-of-use`)

**Section 2.6 — Prohibited Conduct** (directly relevant):
Prohibits: "reverse engineer, decompile, disassemble, modify, create derivative works of" the Service, and "attempt to gain unauthorized access to or interfere with any parts of the Service."
The TOS does not contain an explicit anti-scraping clause by name. Bulk crawling against the explicit `ClaudeBot: Disallow: /` robots.txt directive could be construed as "interfering with" the Service, but this is a legal interpretation question, not a clear-text prohibition against crawling public pages.

**Community content licensing (directly relevant):**
The TOS explicitly states: "Content shared on Meshy's community page is licensed under Creative Commons Zero (CC0) 1.0 Universal Public Domain Dedication license."
This is the most favorable possible license. CC0 imposes no restrictions on reuse, redistribution, or commercial use.

**Free Plan IP ownership clause (significant):**
"Customers using Meshy's Services under the free plan acknowledge and agree that Provider owns all right, title, and interest, including all intellectual property rights, in and to the AI Customer Output."
This creates a distinction: models generated on free accounts have IP vested in Meshy, while paid-account models have IP retained by the creator. The CC0 community license clause presumably supersedes or overlays this for publicly shared models, but this tension is worth flagging.

**Acceptable Use Policy — automated scripting clause:**
Explicitly prohibits: "Using unauthorized automated or scripting processes (such as bulk or automated uploading of content through a script)."
The word "unauthorized" is load-bearing. This language targets unauthorized bulk *uploading*, not necessarily bulk *reading* of public pages. However, combined with the robots.txt `ClaudeBot: Disallow: /`, unauthorized automated reading would also fall under AUP scope.

**No rate-limit specifications in TOS or AUP** for reading public pages. Rate limits documented in API docs apply to authenticated generation API only (Pro: 20 req/sec; Studio: 20 req/sec; Enterprise: 100 req/sec).

### 6. Scale and Time Estimation for 60K Weapon Crawl

**Sitemap-driven approach (viable technical route, subject to authorization):**

| Parameter | Value |
|---|---|
| Total public English model URLs | ~365,000 |
| Target subset (weapons, if filterable) | Unknown — no category metadata in sitemap |
| Individual model page size | ~1.3 MB |
| JSON-LD extraction time | <1 sec per page (static HTML) |
| Rate-limited throughput (1 req/2 sec) | 1,800 pages/hour |
| 60,000 pages at 1 req/2 sec | ~33 hours |
| 365,000 pages at 1 req/2 sec | ~203 hours (~8.5 days) |
| Total bandwidth for 60K pages | ~78 GB |
| Total bandwidth for full English corpus | ~463 GB |

**Discover-page (parameterized) approach:** Not viable. JS-rendered shell returns no data. Also robots-disallowed via `?kind=` parameter block.

**Filtering challenge:** The sitemap provides no category metadata — only UUID and lastmod date. To isolate weapon models, every page in the corpus would need to be fetched and the JSON-LD `keywords` field text-searched for weapon-relevant terms, OR the authenticated API must be used to filter by category. There is no public URL-based filter for weapon type.

**Failure modes if a crawl were authorized:**
1. Statsig session tracking cookie (`statsig-stable-id`) would allow Meshy to identify and throttle or block a crawl by session, even without user authentication.
2. The signed preview image URLs expire, so thumbnails would need re-fetch on a schedule.
3. `cache-control: private, no-cache` on the discover page means CDN caching does not help; each request hits origin.
4. IP-based throttling is plausible but no evidence of Cloudflare bot protection was detected in headers (no `cf-ray` header observed, no CAPTCHA challenge).

---

## Disposition Recommendation

**RED — with a specific exception path noted.**

**Primary reason for RED:** `robots.txt` contains `User-agent: ClaudeBot / Disallow: /` and `User-agent: anthropic-ai / Disallow: /`. This is an explicit machine-readable opt-out. Any Claude-agent-driven crawl of meshy.ai violates this directive, regardless of whether the target paths are otherwise accessible to general crawlers. This is a hard stop for automated crawl using Claude tooling.

**Secondary reason:** The discover page itself (the commission's named target) is not crawlable — it is a JS-rendered shell with no inline model data, and its query parameters (`?kind=`, `?page=`) are explicitly robot-disallowed.

**The exception path — if Matt authorizes and Meshy partnership/API clarifies:**
The individual model pages (`/3d-models/<uuid>`) deliver rich JSON-LD structured data in static HTML, and the sitemap provides a complete UUID enumeration (~365K models). A non-Claude-agent implementation using a standard crawler user-agent string (not `ClaudeBot` or `anthropic-ai`) could, in principle, extract structured metadata at scale from individual model pages. This would require:
1. Explicit authorization from Matt to proceed despite the robots.txt ClaudeBot disallow
2. A crawl implementation that does NOT use a Claude-agent user-agent string
3. TOS review by Matt for the "unauthorized automated scripting" AUP clause
4. A plan to address the category-filtering problem (no weapon filter in sitemap; full corpus fetch = 463 GB and ~200 hours at conservative rate)

**Alternative path that avoids all these issues:** Meshy's authenticated API. The generation API is documented and authenticated. An enterprise partnership inquiry could open a library-browse endpoint or bulk metadata export that is explicitly authorized and rate-limit documented. This is the vendor-relationship route gandalf flagged.

**Phase D (generation-only) routing:** If the library-browse question remains unresolved, Meshy is cleanly viable as a generation-on-demand backend. The robots.txt and AUP concerns do not apply to authenticated API generation calls.

---

## Knowledge Gaps Not Resolved

1. **TOS interpretation of robots.txt ClaudeBot block vs. non-Claude automated access:** The TOS does not explicitly say "no scraping of public pages." The robots.txt block is specifically for `ClaudeBot`/`anthropic-ai`. Whether a non-Claude automated crawler is permitted under TOS is unresolved — AUP says "unauthorized automated scripting" is prohibited, but does not define what authorization would look like for public-page reading.

2. **Weapon-specific model count:** No category breakdown is available from public metadata. "Weapon" models in Meshy's corpus could range from hundreds to tens of thousands. Without authenticated API access to filter by category, there is no way to estimate the weapon-specific subset size without fetching a large sample.

3. **CC0 scope confirmation:** The TOS states community content is CC0, but the free-plan IP clause creates a potential tension. Whether CC0 applies uniformly to all publicly visible models regardless of plan tier is not entirely clear from the TOS text.

4. **Meshy enterprise/partnership inquiry outcome:** Not researched in this probe. If Matt wants to explore an authorized partnership path, Meshy's `/contact` and `/creators` pages are the entry points.

---

## Source List

| Source | URL | Access Date |
|---|---|---|
| Meshy Discover Page | https://www.meshy.ai/discover?kind=model&sort=public_popularity&view=recommended | 2026-05-22 |
| Meshy robots.txt | https://www.meshy.ai/robots.txt | 2026-05-22 |
| Meshy Privacy Policy | https://www.meshy.ai/privacy-policy | 2026-05-22 |
| Meshy Terms of Use | https://www.meshy.ai/terms-of-use | 2026-05-22 |
| Meshy Acceptable Use Policy | https://www.meshy.ai/acceptable-use-policy | 2026-05-22 |
| Sample Model Page | https://www.meshy.ai/3d-models/01939d54-48a0-7c65-b7ec-3bf29ebf7255 | 2026-05-22 |
| Meshy Sitemap Index | https://www.meshy.ai/sitemap-models.xml | 2026-05-22 |
| Meshy Sitemap Shard en-1 | https://www.meshy.ai/sitemap-models-en-1.xml.gz | 2026-05-22 |
| Meshy Sitemap Shard en-9 | https://www.meshy.ai/sitemap-models-en-9.xml.gz | 2026-05-22 |
| Meshy API Rate Limits | https://docs.meshy.ai/en/api/rate-limits | 2026-05-22 |
| Meshy Static Sitemap | https://www.meshy.ai/sitemap-static-en.xml.gz | 2026-05-22 |
