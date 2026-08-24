# RT-4 pre-flight — `whirlwind` archival donor playback

**Date:** 2026-08-24
**Agent:** legolas (UNKNOWN-RESEARCHER)
**Commissioner:** knight-rider
**Trigger:** spec § 6.1 **RT-4** — pre-registered, MUST fire before `whirlwind` is minted
**Class:** evidentiary note (probe record)
**Access:** read-only; all fetches public, unauthenticated

---

## Overall verdict: **BOTH-LIVE**

**The row proceeds at stated confidence.** The Dust-Devil confound on the D4 S14 primary (`KaMPoPywM40`) is **subtractable** — both structural subtraction bases survive.

Stronger than that: **Donor A is not merely alive, it is the highest-fidelity whirlwind reference in the corpus** — 1280×720, 374 decodable frames, on Blizzard's own CDN. RT-4 does not fire. See § "Record corrections" — three statements of record are refuted by measurement.

| Donor | Verdict | Headline |
|---|---|---|
| **A** — D3 Blizzard March-2012 rune-free core-skill clip | **`PLAYABLE`** | Original `.flv` live on Akamai; 720p; frame-verified |
| **B** — D3 2008 pre-release build (`swOroVI1UaM`) | **`DEGRADED-BUT-USABLE`** | `playabilityStatus: OK`; hard cap measured at **240p** |

---

## Donor A — D3 March-2012 core-skill clip · `PLAYABLE`

### The reframe that resolved it

The commission asked the right question: *does the embedded 2012 video still play*, not *does the page 403*. Pursuing that literally produced the answer, because **the bluetracker page never contained a video at all.**

`bluetracker.gg` is a **blue-post text mirror**. Its "videos" are hyperlinks out to the Diablo III skill pages. The media lived on Blizzard's own CDN. So the Cloudflare door was guarding a room that never held the thing we wanted.

### Step 1 — the 403 reproduces exactly (page, not media)

```
curl -sS -o /tmp/rt4_botA.html -D /tmp/rt4_hdrA.txt \
  -w "http_code=%{http_code} size=%{size_download}\n" \
  -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ... Chrome/126.0.0.0 Safari/537.36" -L \
  "https://www.bluetracker.gg/diablo3/topic/us-en/4737240-in-development-class-skill-changes"
```

```
http_code=403 size=5979
cf-mitigated: challenge
server: cloudflare
cf-ray: a30598349d3ac594-MIA
```

State of record held 5,988 B; measured today 5,979 B. Same Cloudflare challenge signature. **403 confirmed as bot-block, not absence** — consistent with standing lane law.

### Step 2 — Wayback resolves the page and confirms provenance

```
curl -sS "http://web.archive.org/cdx/search/cdx?url=bluetracker.gg/diablo3/topic/us-en/4737240*\
&output=text&limit=40&collapse=digest&fl=timestamp,original,statuscode,length"
→ 20220123094315  .../4737240-in-development-class-skill-videos-continued/  200  5244
```

Fetched capture (`http_code=200 size=26824`). Archived body text, verbatim:

> "Much like the last two updates, we'll show off videos of core class skills, **unmodified by runes** … **Barbarian → Whirlwind**"

**The rune-free provenance is now MEASURED from an archived primary source, not asserted.** Previously the dossier's `confounds` field conceded this "could not be independently frame-checked from the text-only archive."

### Step 3 — the archived page has zero embeds

Scanning the archived HTML (`/tmp/rt4_scan.py`):

```
count iframe   4   (all Wayback/battle.net UI shims — "support-shim", "explore-shim")
count .mp4     0
count <object  0
count embed    0
count youtube  0
```

The only Whirlwind reference is `<a href=".../d3/en/class/barbarian/active/whirlwind">Whirlwind</a>`. **Confirmed: bluetracker is a text mirror.** This is why a human-browser check of that URL would have returned "no video here" — a false negative that would have read as donor death.

### Step 4 — following the link to the real media host

The original Blizzard blog is archived from 2012 (`us.battle.net/d3/en/blog/4737240`, eleven captures, earliest `20120331081355`, 200/18,506 B). Both it and the linked skill page load a **Flash** player: `us.media.blizzard.com/global-video-player/themes/d3/video-player.swf`.

The skill page carries the asset path:

```html
Lightbox.loadVideo([{ width: 960, height: 540,
  flvBase: 'http://us.media.blizzard.com/d3/flash/skills',
  flvPath: '/barbarian/whirlwind.flv' }]);
```

### Step 5 — **the 2012 master is still live**

```
curl -sSI "http://us.media.blizzard.com/d3/flash/skills/barbarian/whirlwind.flv"
```

```
HTTP/1.1 200 OK
Content-Length: 6872672
Content-Type: video/x-flv
Last-Modified: Mon, 26 Mar 2012 20:27:46 GMT
Server: AkamaiNetStorage
ETag: "5216e47825af02f4a8ee2412ec89c53b:1332793666"
```

`Last-Modified` 2012-03-26 sits **two days before** the 2012-03-28 blog post. The file is the original, untouched for fourteen years, on Blizzard's own Akamai origin under the canonical path `skills/barbarian/whirlwind.flv`. Provenance chain is closed end-to-end: Blizzard blog (archived, rune-free text) → Blizzard skill page (archived, asset path) → Blizzard CDN (live, original mtime).

Full retrieval and integrity:

```
download http_code=200 bytes=6872672
sha256   855bb3d9c7edca8b372869e667682eda6de85ea813628377e567522d9e998637
magic    464c 5601 05…  → "FLV" v1, flags 0x05 (audio+video)
```

### Step 6 — it decodes, at 720p

```
ffprobe -v error -show_entries stream=codec_name,width,height,r_frame_rate,pix_fmt \
  -show_entries format=duration,size,bit_rate /tmp/rt4_ww2012.flv
```

```
codec_name=vp6f   width=1280  height=720   pix_fmt=yuv420p   r_frame_rate=30000/1001
codec_name=mp3    (audio)
duration=12.479   size=6872672   bit_rate=4405912
```

Note the **1280×720** — the `960×540` in the page markup was the player's display box, not the encode. Full decode count:

```
ffprobe -count_frames -select_streams v -show_entries stream=nb_read_frames → 374
ffprobe -show_entries packet=size | awk …  → video packets=374 avg=17265 B/frame
```

**374 frames, zero decode errors.** ~17 KB/frame at 720p is a genuine detail budget, not an upscale.

Five stills extracted at t = 1.0 / 4.0 / 6.5 / 9.0 / 11.5 s, all returning `1280,720`.

### Step 7 — frame-verified content read

- `evidence-contact-sheet.png` — 15 frames spanning the clip. Frame 0 is a black fade-in; **every subsequent frame is gameplay-camera combat** (dark swamp/graveyard, enemy pack, contact impacts). **Not a title card, not concept art, not a presentation backdrop.**
- `evidence-rotation-strip.png` — six *consecutive* frames at t≈10.2 s. The silhouette's weapon-sweep orientation advances frame-to-frame while the body translates across ground littered with contact decals. **This is the continuous spin + translation + adjacent-contact signature of Whirlwind.**

`frame_extraction_adequate = Y`, established from pixels.

---

## Donor B — D3 2008 pre-release build · `DEGRADED-BUT-USABLE`

**Not deleted, not private, and confirmed playable.**

```
curl -sS "https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=swOroVI1UaM&format=json"
→ http_code=200 size=797
{"title":"Diablo 3 Barbarian Whirlwind Skill","author_name":"Diablo3Inc", …}
```

oEmbed returns 404 for removed/private videos; a 200 with real metadata is positive proof of existence. Watch-page playability:

```
"playabilityStatus":{"status":"OK","playableInEmbed":true, …}
embed_page http_code=200 size=129657
watch_page http_code=200 size=1125107
```

**Ceiling measured, not inferred** — this is the number the record was missing:

```
qualityLabels: ['144p', '240p']
```

Thumbnail ladder corroborates, with pixel dimensions read from the JPEG SOF marker rather than trusted from byte count:

| variant | http | bytes | JPEG dims |
|---|---|---|---|
| `maxresdefault` | **404** | 1097 | **120×90** (placeholder) |
| `sddefault` | **404** | 1097 | 120×90 (placeholder) |
| `hqdefault` | **200** | 10453 | **480×360** (real frame) |
| `mqdefault` | 200 | 8463 | real |
| `default` | 200 | 3594 | real |

**Verdict rationale:** a live 240p source. Fully adequate for **silhouette, cadence and radius**; inadequate for fine particles or material response — exactly the constraint already on the row. Its subtraction value is *structural*, not pixel-based: it predates the runestone system, so cyclones are **impossible**, not merely absent. That argument survives at any resolution.

---

## Record corrections (measured; these refute prior statements)

1. **"the bluetracker archive is a locked door"** → the door is real but **irrelevant**. The page is a text mirror with **zero** video embeds. The media is elsewhere and directly fetchable over plain HTTP. A locked door, and the room behind it was empty anyway — the thing we wanted was in a different building, unlocked.
2. **Dossier § Notes: "Not one whirlwind candidate yields a frame-verified read."** → **REFUTED.** Donor A yields 374 frames at 1280×720. This is now the corpus's *best* whirlwind pixel evidence, exceeding the D4 S14 primary (resolution `UNKNOWN`) and Donor B (240p).
3. **Donor B `max_resolution: UNKNOWN`** → **RESOLVED to 240p.** The dossier correctly warned that a missing `maxresdefault` "alone cannot distinguish 720p from lower encodes." It cannot — so I read `qualityLabels` off the player response instead.

Minor: the spec § 3.1.12 slug `4737240-in-development-class-skill-**changes**` does not exist. The real slug is `…-in-development-class-skill-**videos-continued**` (the dossier's candidate-1 URL is correct). Topic ID 4737240 is right in both.

---

## No `matt_to_do` row filed — and why that is the correct call

The commission authorised a ~30-second human-browser check if Donor A "genuinely requires a human browser." It does not, and such a row would have been **actively misleading**:

- Opening the **bluetracker** URL in a browser shows **no video** (zero embeds) → a human would report "dead," a **false negative**.
- Opening the **Blizzard skill page** invokes a **Flash `.swf`** player. Flash reached end-of-life 2020-12-31 and was removed from all major browsers in 2021. It **cannot** play in any current browser → a second false negative.

Both human checks would have condemned a donor that is, in fact, the best evidence in the corpus. Machine fetch of the raw `.flv` was the only route that answers the question truthfully.

---

## Lane-generalizable finding (recorded, **not actioned** — outside RT-4 scope)

The entire Blizzard 2012 skill-video tree is intact and agent-fetchable. All eight probed assets returned 200 with 2012 `Last-Modified` dates:

| asset | bytes | Last-Modified |
|---|---|---|
| `barbarian/whirlwind` | 6,872,672 | 2012-03-26 |
| `barbarian/seismic-slam` | 8,165,864 | 2012-03-12 |
| `barbarian/hammer-of-the-ancients` | 8,308,657 | 2012-04-25 |
| `demon-hunter/fan-of-knives` | 9,354,799 | 2012-03-26 |
| `monk/way-of-the-hundred-fists` | 9,343,512 | 2012-03-26 |
| `monk/tempest-rush` | 9,688,043 | 2012-03-26 |
| `witch-doctor/locust-swarm` | 9,302,063 | 2012-03-26 |
| `wizard/explosive-blast` | 7,013,605 | 2012-03-26 |

Sampled encodes share Donor A's profile — `seismic-slam` and `tempest-rush` both `vp6f, 1280×720, 30000/1001` (14.21 s / 17.58 s).

Two consequences for knight-rider to route, not for me to decide:

- **`seismic-slam` is carried in the spec (§ 3.1, line 522) as a `gamestar.de` `UNVERIFIED-BOT-BLOCKED` canonical donor with `t_start TBD`.** Its Blizzard master is live at 720p. Same likely applies to other rows whose D3 donors are bot-blocked mirrors.
- This is a **rune-free, official-Blizzard, 720p, confound-free reference lane** — structurally the cleanest baseline material available to the run, and it is a plain `curl` away.

**Method is mapped; volume extraction is `legolas-crawler` work, under a fresh commission.** I am not crawling it here.

---

## Measured vs inferred

**Measured:** every status code, byte count, hash, header, codec, dimension and frame count above; the archived blog text; the zero-embed scan; Donor B's 240p ceiling and `playabilityStatus`; the eight sibling assets.

**Inferred:** (a) that `whirlwind.flv` is *the* clip from the 2012-03-28 post — inferred from canonical path + `Last-Modified` two days prior + the archived post naming Barbarian Whirlwind; very high confidence, though no archived page states the filename in the same breath as the post. (b) That the 2008 clip is a genuine 2008 pre-release build — inherited from the dossier, uploader-asserted, **not** independently verified today; it does not affect the verdict, since its subtraction value rests on pre-dating runestones, which the footage's own content supports.

**What would settle the residual:** nothing outstanding for RT-4. Both donors are live; the confound is subtractable; the row proceeds.

---

## Artifacts

- `evidence-contact-sheet.png` — 15 frames across the clip (proof: gameplay, not title card)
- `evidence-rotation-strip.png` — 6 consecutive frames (proof: rotation cadence)
- Working copy (not committed, `/tmp`): `rt4_ww2012.flv`, sha256 `855bb3d9…98637`

## Source list

- `https://www.bluetracker.gg/diablo3/topic/us-en/4737240-in-development-class-skill-changes` — 403 Cloudflare · accessed 2026-08-24
- `http://web.archive.org/cdx/search/cdx?url=bluetracker.gg/diablo3/topic/us-en/4737240*` — CDX · accessed 2026-08-24
- `https://web.archive.org/web/20220123094315/https://www.bluetracker.gg/diablo3/topic/us-en/4737240-in-development-class-skill-videos-continued/` — 200 · **primary (archived)**
- `https://web.archive.org/web/20120331081355/http://us.battle.net:80/d3/en/blog/4737240` — 200 · **primary (archived)**
- `https://web.archive.org/web/20120419050938/http://us.battle.net:80/d3/en/class/barbarian/active/whirlwind` — 200 · **primary (archived)**
- `http://us.media.blizzard.com/d3/flash/skills/barbarian/whirlwind.flv` — 200, 6,872,672 B · **primary (live original)**
- `https://www.youtube.com/oembed?url=…swOroVI1UaM&format=json` — 200 · primary (platform API)
- `https://www.youtube.com/watch?v=swOroVI1UaM` — 200 · primary (platform)
- `https://i.ytimg.com/vi/swOroVI1UaM/{maxres,sd,hq,mq,}default.jpg` — thumbnail ladder
