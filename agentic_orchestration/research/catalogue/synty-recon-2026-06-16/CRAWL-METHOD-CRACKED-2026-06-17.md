# Synty Crawl Method — CRACKED + full enumeration

**Date:** 2026-06-17
**Author:** knight-rider (autonomous hive-mode session per Matt directive "uncover how to complete the download crawl and then fire the crawl process")
**Supersedes the open knowledge gaps in** `pre-recon-auth-and-variants.md` §4 + "Knowledge gaps"
**Status:** mechanism proven end-to-end; full FBX pull FIRED to Mac staging `~/Games/synty-corpus/fbx/`

---

## 1. The two things that defeated every prior pass

1. **The library is a Shopify *Sky Pilot* folder TREE, not a flat list.** Everything hangs off one order_item (`311325427`). The "tons of pages" is NOT the `folders_page` pagination (that's only ~4 pages of 40) — it's the **per-collection drill-in**. There are **157 top-level collections**, and each collection's files live on its own `/collections/<id>` page. Prior passes only ever read top-level folder *names*, never drilled in, so they saw ~157 names and concluded that was the corpus.

2. **The download endpoint requires a browser `User-Agent`.** Without a UA header, `/apps/downloads/downloads/<id>?...` returns a **200 HTML shell** (the un-hydrated Sky Pilot app page). *With* a desktop-Chrome UA it returns the **302 → signed CloudFront** zip. The Playwright/headless agents kept burning usage caps doing in a heavyweight browser what a single `curl -A` does — and the raw-curl attempts silently got the 200 shell because they lacked the UA.

**Net:** the entire corpus is plain **server-rendered HTML reachable by `curl -A "<chrome-ua>"`**. No browser, no Playwright, no cookies, no OAuth, no usage caps.

## 2. Full crawl recipe (reproducible)

Constants: `email=mhwetmore@gmail.com`, `order_id=178619150`, `order_item_id=311325427`, `logged_in_customer_id=9479474479356`.
UA: `Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36`

1. **Enumerate collections** — for `folders_page=1..N`:
   `…/order_items/311325427?logged_in_customer_id=<CID>&line_item_311325427_folders_page=<P>`
   Parse `collections/(\d+)…sky-pilot-folder-heading'>(name)`. Stops at page 5 (headings drop to 1). → **157 collections**.
2. **Per collection** — fetch `…/order_items/311325427/collections/<cid>?logged_in_customer_id=<CID>` (UA).
   Each file row: a `sky-pilot-file-heading` (name + `sky-pilot-file-size`) followed by a `sky-pilot-actions` anchor `/apps/downloads/downloads/<download_id>?email&order_id&order_item_id`.
   Variant is read from the heading text: `SourceFiles`→FBX, `Unity`, `Unreal`, `Godot`, `.png`→icon.
3. **Per file** — GET `/apps/downloads/downloads/<download_id>?email=…&order_id=…&order_item_id=…` **with UA** → 302 signed CloudFront URL (`djox3levv7u3o.cloudfront.net`, `Expires` ~30 min, must fetch fresh per download) → GET that → bytes. `curl -C -` resumes. Verify with `unzip -t`.

## 3. Full enumeration result (620 file rows across 157 collections)

| Variant | Files | Size |
|---|---|---|
| FBX (SourceFiles) | 136 | **8.41 GB** |
| Unity | 153 | 19.30 GB |
| Unreal | 129 | 20.06 GB |
| Godot | 19 | 0.73 GB |
| icon (.png) | 154 | 0.15 GB |
| other | 29 | 2.28 GB |
| **All variants** | **620** | **~50.9 GB** |

**Storage verdict — settled:** even the *entire* multi-engine corpus (~51 GB) fits the Pi microSD (106 GB free). The partition-onto-Mac contingency is permanently moot. FBX-only gear substrate = **8.41 GB**.

**22 collections ship NO FBX** (Unity/Unreal-only) — several are character-relevant and will need `.unitypackage`/Unreal extraction if wanted: Knights, Vikings, Western, Kids, Battle Royale, Gang Warfare, MINI Fantasy Pack, Nature, plus the INTERFACE HUDs and SIMPLE map packs (non-character). This sizes the extraction-pipeline scope (elrond, later) — full list in the crawl log.

## 4. Sample FBX content confirms substrate value

`POLYGON_Adventure_Pack_SourceFiles_v4.zip` (38.8 MB, integrity-verified) →
`SourceFiles/Character_Files/SK_Character_Human_{Knight,Peasant,Shopkeeper,Viking,Warrior}.fbx` — per-character skeletal-mesh FBX. Multiple distinct character archetypes per pack as separate FBX files: exactly the gear/character substrate the gear-spec generator needs.

## 5. Artifacts

- `full-fbx-variant-manifest.jsonl` — 620 rows: `{collection_id, collection_name, download_id, file_name, variant, size, size_mb, download_url}`.
- `collections-157.json` — collection_id → name.
- Downloader (resumable, bash-3.2-safe): `~/Games/synty-corpus/download_fbx.sh`; log `~/Games/synty-corpus/download.log`.

## 6. Reusable downloader note

The same recipe pulls Unity/Unreal/Godot variants by changing the manifest variant filter. The downloader is destination-agnostic (`$2` = dest dir) — re-point to the Pi share `/Volumes/reincarnated/synty-assets` once it is re-mounted (it was unmounted at session time; FBX staged to Mac-local to avoid blocking on the SMB password).
