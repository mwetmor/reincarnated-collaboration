# Synty Pre-Recon — Auth Mechanism + Download Variants
**Date:** 2026-06-16
**Mode:** B (catalogue recon — pre-auth pass)
**Commissioner:** Matt (via dispatch `agentic_orchestration/dispatches/2026-06-16-legolas-synty-recon.md`)
**Sources:** syntystore.com public pages + subscription URL (read-only, Matt's account)

---

## 1. Auth-Mechanism Characterization

### Subscription page behavior (most important finding)

The URL `https://syntystore.com/apps/downloads/subscriptions/mhwetmore@gmail.com/530884` returns **HTTP 200 with no login redirect**. The page renders Matt's full entitled pack catalogue with download links visible in the HTML. No session cookie is required to reach this page — the email address + subscription ID in the URL path ARE the auth token for the catalogue enumeration endpoint.

**Download URL pattern** (extracted verbatim from page source):
```
/apps/downloads/downloads/<DOWNLOAD_ID>?email=mhwetmore%40gmail.com&order_id=178619150&order_item_id=311325427
```

### Download endpoint behavior (definitive)

Hitting `/apps/downloads/downloads/2302008?email=mhwetmore%40gmail.com&order_id=178619150&order_item_id=311325427` returns **HTTP 302** redirecting to a **signed AWS CloudFront URL**:

```
https://djox3levv7u3o.cloudfront.net/8170/<UUID>/POLYGON_Generic_SourceFiles_v2.zip
  ?response-content-disposition=attachment
  &response-content-type=application%2Fx-zip-compressed
  &Expires=1781667745
  &Signature=<AWS_CLOUDFRONT_SIGNED_SIG>
  &Key-Pair-Id=APKAJO6D4YCMUHCYEOSQ
```

Key structural facts:
- **No session cookie required** anywhere in the chain
- **Auth parameters are URL-embedded**: `email` + `order_id` + `order_item_id`
- **Signed URLs have expiry**: `Expires=1781667745` is a Unix timestamp (~30 minutes from generation based on observed window). A fresh redirect must be fetched per download; URLs cannot be pre-generated and queued.
- **CDN host**: `djox3levv7u3o.cloudfront.net` (AWS CloudFront)

### What Matt must provide for automation

**Nothing additional.** The subscription catalogue is already accessible at:
```
https://syntystore.com/apps/downloads/subscriptions/mhwetmore@gmail.com/530884
```

The full auth credential set is:
- `email`: `mhwetmore@gmail.com` (known)
- `order_id`: `178619150` (extracted from subscription page)
- `order_item_id`: per-pack value (extracted from subscription page per pack)
- `DOWNLOAD_ID`: per-file integer (extracted from subscription page per download entry)

**No browser session export needed. No cookie jar needed. No OAuth flow.** The Synty custom download app authenticates entirely via URL parameters. A script that crawls the subscription page (possibly paginated), extracts `(DOWNLOAD_ID, order_item_id)` tuples per pack, then hits the download endpoint to get a fresh signed CloudFront URL, then fetches that URL — can automate the entire corpus with only the four values above.

### Shopify account login (separate, not required for downloads)

`https://syntystore.com/account/login` redirects to `https://account.syntystore.com/` — Shopify's "new customer accounts" headless system. This flow is **not required** for the download automation described above. It would only be needed if future enumeration required browsing the Shopify account portal itself (e.g., to enumerate order items not already surfaced by the subscription URL).

The account login at `account.syntystore.com` returned HTTP 429 on second fetch (rate-limited), confirming Cloudflare is rate-limiting that endpoint. The download endpoint itself did not rate-limit.

---

## 2. Download-Variant Vocabulary

Confirmed across three packs (Adventure Pack, Dungeon Pack, City Pack — all verified on product pages):

| Variant name (verbatim) | Format | Notes |
|---|---|---|
| `FBX Source Files` | `.zip` containing FBX + textures | Preferred for engine-agnostic mesh work |
| `Unity 2022.3 package` | `.unitypackage` (gzipped tar) | Characters set up with Mecanim, no animations |
| `Unreal 5.3 project` | `.zip` Unreal project | Engine-baked |
| `Godot 4.5.1 project` | Godot project | Engine-baked |
| `Godot 4.5.1 generic particle fx project` | Godot particles | Separate particle FX file |

**FBX availability:** FBX Source Files appear to be a **standard variant across all POLYGON packs** — confirmed present on all three sampled product pages. The subscription page shows `POLYGON_Generic SourceFiles | v2` as a downloadable file, confirming FBX source files are included in the SyntyPass entitlement.

**Note on "Contents may vary between engines"** (verbatim from Dungeon Pack page): some geometry or material setup may differ per engine build; FBX source is the canonical/portable form.

**File naming convention observed**: `POLYGON_Generic_SourceFiles_v2.zip` (75.2 MB for generic shared assets). Per-pack FBX zips are expected to follow a similar pattern.

---

## 3. Throttle Signals

**No documented rate limits found** on any Synty public-facing page (FAQ 404'd, support 404'd, blog 404'd). No mention of per-account download throttling, bandwidth caps, or concurrent download limits in any accessible page.

**Observed signals:**
- `account.syntystore.com` returned HTTP 429 on second fetch in rapid succession — Cloudflare is protecting the Shopify account portal from crawling. This endpoint is not needed for download automation.
- The download app itself (`/apps/downloads/`) did not rate-limit during this pass.
- CloudFront signed URLs have **short expiry** (~30 min window observed). This is a design constraint, not a throttle: each file download must be initiated with a fresh redirect fetch. Sequential download with immediate follow-through is the correct pattern.
- Matt's prior observation of "slowness" is most likely **per-file CDN throughput** (75 MB files over residential), not a server-side per-account throttle. No evidence of token-bucket or per-account rate enforcement.

**Operational recommendation (factual):** Sequential + resumable architecture is appropriate. Fetch the signed URL immediately before each download (not pre-queued). If a download fails, re-fetch the redirect to get a fresh signed URL, then retry.

---

## 4. Pagination Finding

The subscription page is paginated. Pages 1, 2, and 3 all show the same 40-item list header — the WebFetch tool is likely rendering the first page repeatedly due to JavaScript-driven pagination. The actual pagination mechanism (`?page=N`) may be JavaScript-rendered. The authenticated full crawl will need to handle this (either headless browser or direct API enumeration). The two currently visible download entries (`POLYGON_Generic SourceFiles v2` and `GENERIC_Particle_FX Godot_4_5_1`) are SyntyPass-level generic assets shared across the subscription, not per-pack files — per-pack files likely surface when a specific pack's expandable row is opened (JavaScript interaction). This is the primary unknown for the full automated recon: whether per-pack download links are accessible without JavaScript execution.

---

## Knowledge gaps

- **Per-pack file enumeration without JS**: the subscription page may require JavaScript to expand individual pack rows and expose their `order_item_id` + `DOWNLOAD_ID` values. Static fetch may only surface the two generic files. Full enumeration may require a headless browser (Playwright/Puppeteer) or an authenticated API call to the Synty downloads app backend. To be determined in the authenticated recon pass.
- **Total pack count**: pagination appeared to repeat the same 40 packs across pages 1–3, suggesting JS-rendered pagination. Actual corpus size unknown until authenticated JS-capable pass.
- **FBX zip internal structure**: whether FBX zips contain body/head/weapon decomposed files or baked scenes — requires a sample pull in the authenticated pass.
