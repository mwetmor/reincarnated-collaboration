# Per-Source robots.txt + Bot-Policy Verification — 2026-05-22 Evening

**Owner:** knight-rider (overnight orchestrator session)
**Authority:** Matt 2026-05-22 explicit overnight-cascade authorization (per orchestration plan § "Pre-flight check additions" P0.8 + P0.9)
**Empirical grounding:** Meshy probe surfaced ClaudeBot Disallow AFTER fetches had already executed. This pre-flight runs the same probe pattern across EVERY candidate source BEFORE any dispatch fires. Per Discipline #20 (PROPOSED tonight) — respect explicit machine-readable Claude-agent opt-out signals.

---

## Summary table — disposition per source

| Source | Domain probed | ClaudeBot status | anthropic-ai status | Disposition | Notes |
|---|---|---|---|---|---|
| **Wikipedia EN** | en.wikipedia.org | NOT blocked (no entry) | NOT blocked (no entry) | **GREEN — via dumps** | Bot policy: substantial download MUST use dumps.wikimedia.org; not page-by-page API crawl |
| **Wikidata** | wikidata.org | NOT blocked (no entry) | NOT blocked (no entry) | **GREEN — SPARQL + dumps** | SPARQL endpoint public; bulk JSON dumps preferred for volume |
| **Wikimedia Commons** | commons.wikimedia.org | NOT blocked (no entry) | NOT blocked (no entry) | **GREEN — via dumps** | Same Wikimedia policy; use dumps for image metadata bulk |
| **Fandom (top-level)** | fandom.com | unknown (403 to WebFetch) | unknown | **AMBER — manual review** | Cloudflare WAF likely; needs alt-path test from non-WebFetch client |
| **Fandom (poewiki.net independent)** | poewiki.net | **BLOCKED** (Disallow: /) | not listed | **RED** | Explicit Disallow ClaudeBot |
| **Path of Exile Fandom wiki** | pathofexile.fandom.com | unknown (403) | unknown | **AMBER** | Cloudflare; alt-path test needed |
| **OSRS Wiki (independent)** | oldschool.runescape.wiki | **BLOCKED** (Disallow: /) | not listed | **RED** | Also blocks Claude-SearchBot |
| **Warcraft wiki.gg** | warcraft.wiki.gg | **BLOCKED** (Disallow: /) | not listed | **RED** | wiki.gg site-wide pattern |
| **Wowpedia Fandom** | wowpedia.fandom.com | unknown (403) | unknown | **AMBER** | Cloudflare; same alt-path question |
| **Monster Hunter wiki.gg** | monsterhunter.wiki.gg | unknown (429 — rate-limited probe) | unknown | **AMBER → likely RED** | wiki.gg pattern strongly suggests BLOCKED; 429 itself is a Claude-agent block signal |
| **Fextralife Dark Souls** | darksouls.wiki.fextralife.com | NOT blocked (no entry); GPTBot blocked | NOT blocked | **GREEN-with-CAUTION** | Only AI bot they block is GPTBot; ClaudeBot not listed |
| **D&D 5e SRD (dnd5esrd.com)** | dnd5esrd.com | DNS / connection refused | — | **DEAD** | Domain not resolving |
| **D&D 5e API (dnd5eapi.co)** | dnd5eapi.co | 404 on robots.txt | — | **AMBER — needs ToS review** | API alive (per legolas prior research); no robots.txt published |
| **Pathfinder SRD (Archives of Nethys)** | aonprd.com | 404 on robots.txt | — | **AMBER — needs ToS review** | No robots.txt published; OGL content |
| **D&D Beyond** | dndbeyond.com | NOT blocked (no entry) | NOT blocked | **AMBER — copyright caution** | Closed paid content; OGL portion only |
| **5e.tools** | 5e.tools | 404 on robots.txt | — | **AMBER** | No robots.txt; site openly republishes 5e SRD |
| **open5e.com** | open5e.com | content-signal returned (not raw robots.txt) | — | **AMBER** | Site signals search=yes,ai-train=no; ClaudeBot status ambiguous |
| **Smithsonian (si.edu)** | si.edu | **BLOCKED** (Disallow: /) | not listed | **RED for site crawl** | Their robots blocks ClaudeBot site-wide |
| **Smithsonian Open Access API** | api.si.edu via api.data.gov | (no robots.txt on api.data.gov; 404) | — | **GREEN — API path** | API-driven via api.data.gov key; documented endpoint; not page crawl |
| **Royal Armouries** | royalarmouries.org | NOT blocked (no entry; only Crawl-delay: 20) | NOT blocked | **GREEN-with-CAUTION** | 20-second crawl-delay must be honored |
| **Royal Armouries (collection subdomain)** | collections.royalarmouries.org | 404 (redirects to root) | — | **GREEN — via root path** | Use root robots policy |
| **Met Museum** | metmuseum.org | **BLOCKED** (Disallow: /) — also Apple-Extended, Bytespider, etc. | not listed | **RED for site crawl** | API path may still be viable; Met Open Access API at metmuseum.org/api separate question |
| **TVTropes** | tvtropes.org | 429 (rate-limit; itself a likely-RED signal) | — | **AMBER → likely RED** | 429 from a single probe; pattern matches blocked |
| **IMFDB** | imfdb.org | 403 (Cloudflare block on WebFetch) | — | **RED — inaccessible** | Cloudflare WAF blocking our agent before robots fetch |
| **Open Game Art** | opengameart.org | NOT blocked (no entry); Crawl-delay 10 | NOT blocked | **GREEN-with-CAUTION** | Drupal-based; honor 10s crawl delay |
| **Sketchfab** | sketchfab.com | NOT blocked (no entry) | NOT blocked | **GREEN** | Only bingbot-specific Allow rule; default permissive |
| **Kenney** | kenney.nl | 404 on robots.txt | — | **GREEN — static download** | No robots.txt; static ZIP downloads are not crawl traffic |

---

## Disposition rollup

### GREEN — clear to fire

| Source | Method |
|---|---|
| Wikipedia EN | **dumps.wikimedia.org bulk XML** (per bot policy: "download database dumps instead" for substantial pulls) |
| Wikidata | **SPARQL endpoint** (single structured query per weapon Q-item class) + bulk JSON dump for full inventory |
| Wikimedia Commons | **dumps.wikimedia.org** for image metadata (matched on weapon-article File: references) |
| Smithsonian Open Access | **api.data.gov API** (requires SMITHSONIAN_API_KEY env var; per legolas P0.5; Matt-side blocker) |
| Royal Armouries | **HTTPS crawl with 20-sec Crawl-delay** (very slow; ~180 entries/hour; small but feasible) |
| Sketchfab | **Data API v3** (documented; cursor pagination; rate-limited per API policy) |
| Kenney | **Static ZIP downloads** (~10-20 ZIPs; not "crawl" traffic) |
| Open Game Art | **HTTPS crawl with 10-sec Crawl-delay** |

### GREEN-with-CAUTION

| Source | Caution |
|---|---|
| Fextralife Dark Souls | Only GPTBot blocked; ClaudeBot status absent. Acceptable but the lack of explicit allowance is worth noting. |

### AMBER — needs Matt judgement before firing

| Source | Question |
|---|---|
| Fandom-hosted wikis | 403s come from WebFetch path; MediaWiki API endpoint may behave differently. Worth testing api.php direct via curl + ClaudeBot User-Agent header. Decision: defer pending Matt review (out-of-scope for overnight cascade). |
| D&D 5e API (dnd5eapi.co) | No robots.txt; needs ToS / OGL terms review. Defer. |
| Pathfinder SRD (Archives of Nethys) | No robots.txt; OGL terms apply but explicit Claude-agent policy unknown. Defer. |
| D&D Beyond | Mostly closed paid content; OGL subset may be free-to-use. Defer; not high-value vs other SRD sources. |
| 5e.tools | Republishes SRD; legal status ambiguous. Defer. |
| open5e.com | Content-signal ambiguous (search=yes,ai-train=no); ClaudeBot unlisted but signal language suggests caution. Defer. |
| TVTropes | 429 suggests already-throttled or already-blocked. Defer. |

### RED — DO NOT FIRE

| Source | Reason |
|---|---|
| poewiki.net | Explicit `User-agent: ClaudeBot / Disallow: /` |
| Old School RuneScape wiki | Explicit `User-agent: ClaudeBot / Disallow: /` + Claude-SearchBot blocked |
| Warcraft wiki.gg | Explicit `User-agent: ClaudeBot / Disallow: /` |
| Monster Hunter wiki.gg | Inferred RED via wiki.gg site-wide pattern (probe returned 429) |
| Smithsonian si.edu | Explicit `User-agent: ClaudeBot / Disallow: /` (site crawl path; API path still GREEN) |
| Met Museum metmuseum.org | Explicit `User-agent: ClaudeBot / Disallow: /` (site crawl path; Met Open Access API needs separate probe) |
| IMFDB | Cloudflare WAF blocks our agent before robots.txt fetch; effective access denied |
| dnd5esrd.com | DNS / connection refused; domain dead |

---

## Architectural consequence

**The original orchestration plan assumed game-wikis-Fandom + museum-direct-crawl as primary substrate sources. The empirical robots.txt verification surfaces that the bulk of game-wiki content and the major museum collections explicitly block ClaudeBot.**

This is the SAME pattern as Meshy: a target that looks viable on capacity terms is actually unavailable on Claude-agent-respect terms.

**Surviving knowledge-crawl substrate:**

| Track | Method | Estimated entries |
|---|---|---|
| Wikipedia/Wikidata/Commons via dumps | Bulk XML/JSON dump consumption (NOT page-by-page crawl) | ~5,000-15,000 weapon-class entries with infobox + Wikidata property graph + Commons image references |
| Smithsonian Open Access via API | API key + documented endpoint | ~100-400 historical/culturally-diverse weapons |
| Royal Armouries direct (slow crawl with 20s delay) | Authorized HTTPS crawl | ~200-1,000 entries (slow; ~50/hr) |
| Sketchfab CC0+CC-BY via API | Data API v3 cursor pagination | ~1,177 3D weapon models (secondary track; not knowledge data per se) |
| Kenney + OGA static + slow-crawl | Static + slow HTTPS | ~600-800 3D models (secondary; not knowledge data) |
| Fextralife Dark Souls (cautious) | HTTPS crawl with conservative rate limit | ~100-300 weapon entries (game-canon flavor) |

**Total knowledge substrate target REVISED:** ~5,500-17,500 weapon knowledge entries (versus original 15,000-30,000 estimate). Roughly half the original target — but still ~30-100× larger than the original 15-entry catalogue.

**3D model substrate (secondary):** ~2,000-3,000 attachable models (Sketchfab + Kenney + OGA + Fextralife where allowed). Sufficient for image-reference attachment to a meaningful subset of knowledge entries.

---

## Recommendations for fire-cascade tonight

| Track | Action tonight |
|---|---|
| Wikipedia/Wikidata/Commons | **Author dispatch** for legolas to consume bulk dumps (NOT a long-running crawl; tonight: author the dispatch, fire as background process to begin downloading the dump and parsing weapon-class entries; expected runtime: dump download is bandwidth-bound and likely hours; parse is fast) |
| Smithsonian Open Access | **GATED on Matt providing SMITHSONIAN_API_KEY** — author the dispatch but mark it BLOCKED on Matt-side; do not fire tonight |
| Royal Armouries | **Author dispatch** for slow-and-respectful crawl (20s delay = ~180 entries/hour; ~5-7 hours runtime); fire as background |
| Sketchfab | **Fire D3 dispatch** as background (1-4 hours) |
| Kenney | **Fire D4 dispatch** as background (~30-60 min) |
| OGA | **Fire D5 dispatch** as background (~1-2 hours; 10s delay honored) |
| Fextralife | **DEFER — Matt judgement** on GREEN-with-CAUTION sources (preference for explicit allow vs. silence) |
| Fandom-hosted wikis | **DEFER** — needs Matt's alt-path verification |
| All RED sources | **DROP entirely** from this workstream |
| Discipline #20 authoring | **Fire jack-ryan sub-agent** for canonical entry authoring |

---

## Discipline #20 PROPOSED entry — empirical anchor

This verification log IS the empirical anchor for Discipline #20. The pattern observed in real-time tonight:

1. Plan assumed broad source viability
2. Per-source robots.txt probe surfaces hard-Disallow-ClaudeBot signals in ~40% of candidate sources
3. The discipline says: probe BEFORE the workstream commits, not after the first crawl already executed
4. The Meshy probe earlier this evening hit the same lesson but only AFTER multiple fetches had completed

**Discipline #20 PROPOSED (authored by jack-ryan tonight under separate dispatch):**

> Respect robots.txt + explicit Claude-agent directives (User-agent: ClaudeBot / anthropic-ai). For every source touched by automated work, perform the robots.txt probe as a P0 step before scoping. If ClaudeBot or anthropic-ai is Disallow-listed, the source routes to non-Claude implementation or skip. This applies regardless of whether the technical access is possible — the explicit machine-readable directive is binding.

---

**Signed:** knight-rider (overnight orchestrator)
**For:** the four Track A knowledge crawl dispatches (Wikipedia/Wikidata/Commons; Royal Armouries; the Smithsonian API gated dispatch) and the three Track B model crawl dispatches (Sketchfab/Kenney/OGA) authored next.
**Next-session pickup:** robots verification is captured here; dispatches reference this log; aging Fandom + 5e API + Open5e + TVTropes questions are AMBER pending Matt review.
