# U1-BUILD / G-3 seal item S7 — screenshot verification of the two Tier-2 fleet surfaces

**Date:** 2026-08-24 (captures rendered `2026-08-25T00:27–00:34Z`)
**Verifier:** galadriel (visual-perception steward)
**Run:** RUN U1-BUILD, conductor gandalf · ledger `agentic_orchestration/gandalf/notes/2026-08-24-u1-build-run-ledger.md`
**Method:** Playwright/Chromium headless, deviceScaleFactor 2, viewports 1600/1500/1280/430. Every rendered value compared against a value derived independently from the tape by this agent, not against the surfaces' own prose.

---

## 1. Reference set — disk truth, derived independently

Ground truth is `agentic_orchestration/flight/records-2026-08.jsonl`. Fold performed by an
independent stdlib-`json` script written for this verification (`/tmp/gal_fold.py`,
`/tmp/gal_fold2.py`) — **not** by `flight/schema.py`, so the derivation does not share code
with either surface under test. Reference fold `flight/bin/flight_report --stdout` was
captured as a second opinion only.

| quantity | value derived from tape by galadriel |
|---|---|
| rows on disk | **73** |
| rows carrying a `corrects` key (superseded) | 6 |
| rows after corrections | **67** (73 − 6) |
| distinct `unit_id` | **34** |
| partition | **32 SEALED + 1 IN-FLIGHT + 0 QUEUED + 1 UNBOUND = 34** |
| IN-FLIGHT unit | `run:U1-BUILD` (START, no CLOSE) |
| UNBOUND unit | `run:VFX-AB` (CURATION only) |
| VFX-AB closed units | 30, all `rc=0` |
| VFX-AB `tokens_input` | **72,375,471** (→ 72.4M) |
| VFX-AB `tokens_cached_input` | 67,431,424 → **93.1689 %** (→ 93.2 %) |
| VFX-AB `tokens_output` | **259,471** (→ 259K) |
| VFX-AB `tokens_reasoning` | 154,000 |
| tok-in / artifact (VFX) | 72,375,471 / 30 = 2.41M |
| scorecard `openai/gpt-5.6-sol@xhigh` | **30 units, 30/30 rc=0 (100 %)** |
| codex-serial pins on tape | `{gpt-5.6-sol@xhigh}` — single value |
| grok-serial rows | **exactly 1** (`grok-probe/2026-08-24-capability`) |
| grok row: `cost_usd` | **0.00286** |
| grok row: token keys | **absent — NULL, not 0** |
| grok row: `rc` | absent — NULL |
| grok row: `pin` | absent; carries `model_echo: grok-4.6-build` |
| rows carrying `model_echo` | 1 |
| rows carrying **both** `model_echo` and `pin` | **0 — zero pin-drift comparisons are possible** |
| rows carrying `harness_version` | 1 (grok-cli 1.0.5) |
| claude-agent live rows | 4 (2 START, 1 ENQUEUE, 1 CLOSE) across 2 units |
| claude-subagent rows | 0 |

All three of the conductor's cross-check figures reproduce exactly.

---

## 2. Capture set

| file | surface | viewport |
|---|---|---|
| `board-live-1600-full.png` | fleet board, live server `127.0.0.1:8787` | 1600×1200 full-page |
| `board-live-1280-full.png` | fleet board | 1280×1000 full-page |
| `board-live-430-full.png`, `board-430-crop.png` | fleet board | 430×932 full-page |
| `board-view-top.png` / `-mid1` / `-mid2` | fleet board, scroll positions | 1500×1050 |
| `board-sec-01..05.png` | fleet board, per-`<section>` element shots | 1500 |
| `board-live-text.txt` | fleet board `document.body.innerText` | — |
| `glance-fleet-1500-full.png` | Glance `#/fleet`, vite `localhost:5199` | 1500×1000 full-page |
| `glance-fleet-430-full.png`, `glance-430-crop.png` | Glance `#/fleet` | 430×932 full-page |
| `glance-sec-00..09.png` | Glance fleet card, per-heading card shots | 1500 |
| `glance-fleet-text.txt` | Glance `document.body.innerText` | — |

Capture scripts (galadriel working tree): `agentic_orchestration/galadriel/pipeline/u1-s7-capture-board.mjs`,
`u1-s7-board-sections.mjs`, `u1-s7-board-top.mjs`, `u1-s7-capture-glance.mjs`,
`u1-s7-glance-sections.mjs`. Read-only against `flight/`, `factory/ui/`, `glance/`; nothing in
those trees was modified.

**Probe note.** `board.py --render-to` completed in 3.08 s with all 15 probes running — no hang.
The `--no-lane-probes` variant was rendered as instructed and differs by exactly one element:
the LANES section body is replaced by `— lane probes skipped (--no-lane-probes) — no lane state
is claimed`. Every other byte is identical modulo render timestamp. No divergence to reconcile;
the probed render is the one verified below.

---

## 3. Surface 1 — local fleet board (`factory/ui/board.py`, Tier-2)

### 3.1 Value-by-value comparison

| # | value as rendered on the board | disk truth | result |
|---|---|---|---|
| 1 | `73 rows on disk` | 73 | MATCH |
| 2 | `67 after corrections` | 67 | MATCH |
| 3 | `IN-FLIGHT (1 of 34 units on tape)` | 34 units, 1 in-flight | MATCH |
| 4 | in-flight unit `run:U1-BUILD` · `claude-agent` · owner gandalf · last actor jack-ryan · last event GATE | ditto | MATCH |
| 5 | `queued (ENQUEUE seen, no START yet): 0` | 0 | MATCH |
| 6 | `AT GATE (1 · overlay)` — `G-1-schema-law-ratification` · jack-ryan · PASS-WITH-FINDINGS | ditto | MATCH |
| 7 | `SEALED (32)` | 32 | MATCH |
| 8 | UNBOUND `run:VFX-AB` · OPEN · CURATION · 10h | ditto | MATCH |
| 9 | VFX-AB `30 unit(s) · 30/30 rc=0` | 30 / 30 | MATCH |
| 10 | VFX-AB `72.4M (30/30 units)` | 72,375,471 | MATCH |
| 11 | VFX-AB `93.2%` cache | 93.1689 % | MATCH |
| 12 | VFX-AB `259K` out | 259,471 | MATCH |
| 13 | VFX-AB `6 WARN across 1 curation row(s)` | 1 CURATION row, 6 warns | MATCH |
| 14 | U-4 `— no rc on 1/1 units` / `— null on 1/1 units` / `$0.00286 (1/1 CLOSE rows carry cost_usd)` / grok-sub / 0m | ditto | MATCH |
| 15 | U1-BUILD `1/1 rc=0` / tokens null / no cost_usd / anthropic-max / 23m | ditto | MATCH |
| 16 | scorecard `openai / gpt-5.6-sol@xhigh` — 30 units, `100% (30/30 rc=0)`, 72.4M, 93.2 %, 259K, `2.4M` tok-in/artifact, 4m | ditto | MATCH |
| 17 | scorecard `xai / (no pin recorded)` — 1 unit, `— no rc recorded`, `— null, declared`, `$0.00286 (1/1)`, `— no START→CLOSE pair` | ditto | MATCH |
| 18 | scorecard `anthropic / (no pin recorded)` — 1 unit, `100% (1/1 rc=0)` | ditto | MATCH |
| 19 | codex card pin `gpt-5.6-sol@xhigh` *(derived from this lane's own rows, never asserted here)* | single pin on lane | MATCH |
| 20 | codex last tape activity `vfx-p2/30-ma_video_companion · rc 0 · 1.6M in / 7K out · cost_usd absent on this row · 2026-08-24T14:03:40Z` | ditto | MATCH |
| 21 | grok card `1 CLOSE row(s) across 1 unit(s) on this lane` | exactly 1 row | MATCH |
| 22 | grok card `rc null · tokens null · $0.00286` | NULL / NULL / 0.00286 | **MATCH — declared-null, never 0** |
| 23 | grok card pin `— no row on this lane carries a pin` | no pin on lane | MATCH |
| 24 | grok legs 1 & 3 rendered `not applicable` / `none exists` in `.null` italic, not green | D-6 / D-8 ungated | MATCH |
| 25 | LANES header `probe: degraded — D-2 CLI pending` | required | **MATCH** |
| 26 | Q62 caveat verbatim: *"liveness-NOW is the § 3 CLI check's answer; the board is a VIEW (THE LAW) and may lag its refresh."* | required | **MATCH** |
| 27 | claude card `4 lifecycle row(s) · 1 CLOSE`, tokens null w/ F-7 rationale | 4 live rows, 1 CLOSE | MATCH |
| 28 | `window meters — no SNAPSHOT row on the tape` in `.null` | 0 SNAPSHOT rows | MATCH |
| 29 | `DECISIONS — 21 open / 38 struck` | agrees w/ Tier-1 | MATCH |
| 30 | `ACTIONS — 11 open / 8 struck` | agrees w/ Tier-1 **on re-run** — see note | MATCH |
| 31 | **`pin drift` → green `none` — "no row carries a `model_echo` that disagrees with its `pin`"** | **0 rows carry both `model_echo` and `pin`; zero comparisons possible** | **MISMATCH** |

**Score: 30 MATCH / 1 MISMATCH.**

**Note on row 30.** My first Tier-1 render (`00:26:20Z`) read `actions 10 open`; the board
(`00:27:45Z`) read `11 open`. This is **temporal, not a parser disagreement**: `canonical/matt_to_do/README.md`
has mtime 20:27 local — **T20 (disk headroom) was appended to the queue mid-session**, between the
two renders. Re-running `flight_report` afterwards returns `actions 11 open / 8 struck` and lists T20.
Both surfaces agree. Not a defect; recorded so the delta is not mistaken for one later.

### 3.2 Defects

**D1 — `pin drift` renders a zero-coverage vacuum as a green negative. (MISMATCH; nominated for BLOCK consideration.)**
Markup: `<tr><td>pin drift</td><td><span class='ok'>none</span> — no row carries a `model_echo`
that disagrees with its `pin`</td></tr>`, and `.ok{color:var(--green)}`. Evidence: `board-sec-03.png`.
Disk truth: **exactly one** live row carries a `model_echo` (the grok probe), and that row carries
**no `pin`**. Zero rows carry both keys, so **no comparison is possible at all** — the board's
statement is true only vacuously, and it is rendered green with no denominator.
Tier-1, on the identical tape, refuses this: *"pin drift: **NO COMPARISON POSSIBLE** — 1/34 unit(s)
carry a `model_echo` but none of them carries a `pin`, so nothing can be compared. **Determinate,
not green.**"* The board's own health strip gets this right two rows above — `window meters` uses
`class="null"` for exactly this situation. So the surface holds the null-is-a-fact law everywhere
it was written by hand and drops it in this one cell. Same tape, opposite epistemic rendering,
and Tier-2 picked the flattering one. **Recommendation:** render `pin drift` with `class="null"`
and carry the coverage denominator (`1/34 model_echo · 0/34 comparable`).

**D2 — grok lane wears the same green chip as codex despite 1-of-3-leg coverage. (Affordance.)**
Markup: both lanes render `<span class='state s-open'>open</span>`; `.s-open` is green (#79d79b).
The chip vocabulary is only `s-open` / `s-busy` / `s-unknown` — there is no reduced-coverage chip.
The card body *does* declare the coverage honestly ("this answer rests on 1 of 3 legs"), but Tier-1
renders the state marker itself as **🟡** for grok against **🟢** for codex. The board's stated
use case is *"glance HERE before opening a vendor TUI"* — the distinction Tier-1 draws is exactly
the one lost at a glance. Evidence: `board-sec-02.png`. **Recommendation:** an `s-open-partial`
amber chip keyed on legs-reached < legs-defined.

**D3 — HEALTH strip drops severity colour that Tier-1 carries. (Affordance.)**
`<tr><td>disk</td><td>23 GB free of 494 GB (5%)</td></tr>` — no severity class, renders plain white.
Tier-1 renders the same reading **🔴**. The five `git · …` rows likewise render plain where Tier-1
renders 🟡. Sharpest form of the inconsistency: the board surfaces **T20 — "Reclaim disk headroom …
96% used, RED"** in its own AWAITING MATT column while rendering the underlying disk reading
unalarmed in its own health strip. Evidence: `board-sec-03.png`, `board-view-top.png`.

**D4 — HEALTH strip omits the `harness version` row Tier-1 carries. (Absence.)**
Tier-1: *"harness version: 🟡 stable WHERE RECORDED (U-4: grok-cli 1.0.5) — but only 1/34 unit(s)
record one at all."* Disk confirms exactly 1 row carries `harness_version`. The Tier-2 board has
no such row. Given that the run's own law is about pinning and reproducibility, a 1/34 capture
rate on harness version is a fact the shop board should carry.

**D5 — SEALED rollup omits the `reasoning` column Tier-1 carries. (Absence.)**
Disk: VFX-AB `tokens_reasoning` = **154,000**. Tier-1 renders a `reasoning` column (154K); the
board's rollup has no such column, so 154K reasoning tokens are invisible on Tier-2. Evidence:
`board-sec-04.png`.

**D6 — the partition identity is never stated. (Absence, low.)**
Tier-1 prints `PARTITION ✓ — 34 unit(s) on tape = 32 SEALED + 1 IN-FLIGHT + 0 QUEUED + 1 UNBOUND`.
All four terms are readable on the board, but scattered across four widely-separated regions;
the operator must do the arithmetic. FINDING-2's whole point is that the partition be legible.

**D7 — page-level horizontal overflow at 430 px. (Rendering, low.)**
At 430 px, `document.documentElement.scrollWidth = 810` vs `innerWidth = 430` — the SEALED rollup
table is not inside a scroll container, so the entire page pans sideways. Desktop shop tool, so
low severity; noted only because Glance handles the identical case correctly (below).

### 3.3 Verdict — Surface 1

**PASS-WITH-FINDINGS.** Every figure the board renders is correct: 30 of 31 checked cells MATCH
disk truth, including all the ones the conductor named (73/67, 34 = 32+1+0+1, 72.4M / 93.2 % /
259,471, the 30-unit 100 %-rc=0 scorecard at `gpt-5.6-sol@xhigh`, the single grok row at $0.00286
with tokens rendered as declared-null, the codex pin, the degraded-probe banner, the verbatim Q62
caveat). **D1 is the one cell that disagrees with the Tier-1 reference on the same tape**, and it
disagrees in the direction of unearned reassurance. I flag it for the conductor's severity ruling
rather than ruling on it myself: it is a truth-rendering defect, not a cosmetic one. D2–D3 are the
same failure mode in weaker form (severity affordances dropped in the Tier-1→Tier-2 translation).

---

## 4. Surface 2 — Glance fleet card (`glance/app`, `#/fleet`)

`node parser/parse.mjs` → `✓ parse GREEN — no malformed legislated shapes` (16 dangling-`gates-on`
WARNING badges, all pre-existing and unrelated to `flight/`). Page loaded with **0 console errors
and 0 page errors** at both viewports.

### 4.1 REAR-VIEW-ONLY constraint

**HELD — verified structurally and visually.**
Structurally: `glance/app/public/state.json` → `fleet` carries keys
`source · tape_files · rows_on_disk · rows_after_corrections · unparseable_lines · schema_versions ·
coverage · units_total · units_sealed · workstreams · scorecards · lanes · claude · months ·
verdicts · snapshots`. **No auth key, no health key, no in-flight key, no probe key, no staleness
key.** The live half is absent from the data layer, not merely hidden in the view.
Visually (`glance-sec-00.png`): *"**This is the rear-view mirror, not the windshield.** Everything
here is HISTORY … Live lanes, auth health, unpushed commits and staleness are structurally invisible
to a static build and live on the local fleet board instead."* And on the denominator line:
*"32 sealed of 34 units on tape (denominators for the rollups — **not** lanes; this page renders no
live state)."* The lane section is titled *"Vendor lanes — **historical rollup** per lane"* and says
*"This is what the lane HAS DONE. What the lane is doing RIGHT NOW is a local-only fact."*
No IN-FLIGHT lane, no AT-GATE overlay, no AWAITING-MATT section, no health strip on the card.

### 4.2 Value-by-value comparison

| # | value as rendered on the Glance card | disk truth | result |
|---|---|---|---|
| 1 | `records-2026-08.jsonl · 73 rows on disk, 67 after corrections · rows stamped v1` | 73 / 67 / v1 | MATCH |
| 2 | COVERAGE `tape begins 2026-08-24T03:29:39Z and ends 2026-08-24T23:38:14Z` | ditto | MATCH |
| 3 | `32 sealed of 34 units on tape` | 32 / 34 | MATCH |
| 4 | codex-serial `30 sealed unit(s)` · `30/30 rc=0` | 30 / 30 | MATCH |
| 5 | codex-serial `72.4M in (30/30 units) · 93.2% cache · 259K out` | 72,375,471 / 93.1689 % / 259,471 | MATCH |
| 6 | codex-serial `— no vendor-reported cost on these rows` | 0 of 30 carry `cost_usd` | MATCH |
| 7 | codex-serial `median wall 4m` · `pin gpt-5.6-sol@xhigh` · `chatgpt-sub` | median 239 s; single pin | MATCH |
| 8 | codex-serial last close `vfx-p2/30-ma_video_companion · 2026-08-24T14:03:40Z` | ditto | MATCH |
| 9 | grok-serial `1 sealed unit(s)` | exactly 1 row | MATCH |
| 10 | grok-serial rc `— no exit code recorded` | `rc` absent | **MATCH — declared-null** |
| 11 | grok-serial tokens `— tokens null on 1/1 units` | token keys absent | **MATCH — never 0** |
| 12 | grok-serial `$0.00286 (1/1 rows report one)` | 0.00286 | MATCH |
| 13 | grok-serial median wall `— no START→CLOSE pair on this lane` | CLOSE only, no START | MATCH |
| 14 | grok-serial pin `— no row on this lane carries a pin` | no pin | MATCH |
| 15 | claude lanes `1 (1 CLOSE)`, tokens null w/ F-7 rationale | 1 CLOSE; `run:U1-BUILD` correctly excluded (unsealed) | MATCH |
| 16 | run-cost U-4 row — no rc / no curation / tokens null / $0.00286 / grok-sub / 0m | ditto | MATCH |
| 17 | run-cost U1-BUILD row — `1/1 rc=0` / tokens null / no cost / anthropic-max / 23m | ditto | MATCH |
| 18 | run-cost VFX-AB row — 30 / `30/30 rc=0` / `6 WARN / 1 row(s)` / 72.4M · 93.2 % · 259K / chatgpt-sub / 10.6h | ditto | MATCH |
| 19 | scorecard `openai / gpt-5.6-sol@xhigh` — 30, `100% (30/30 rc=0)`, 72.4M · 93.2 % · 259K, `2.4M` tok-in/artifact, 4m | ditto | **MATCH** |
| 20 | scorecard `xai / — no pin recorded` — 1, no exit code, tokens null, no artifact rows, `$0.00286 (1/1)`, no START→CLOSE | ditto | MATCH |
| 21 | scorecard `anthropic / — no pin recorded` — 1, `100% (1/1 rc=0)`, 23m | ditto | MATCH |
| 22 | cost trend `2026-08 · 32 units · 72.4M in (30/32 units) · 93.2% cache · 259K out · $0.00286 (1/32 rows report one)` | ditto — honest denominators on both | MATCH |
| 23 | verdict history `PASS-WITH-FINDINGS 1` / `PASS 1`; GATE `run:U1-BUILD` 23:20:54Z `G-1-schema-law-ratification · jack-ryan`; CURATION `run:VFX-AB` 14:03:40Z `— no gate id · elrond` | ditto | MATCH |
| 24 | window-meter history `— no SNAPSHOT row on the tape … a gap in capture, **not a reading of zero**` | 0 SNAPSHOT rows | MATCH |

**Score: 24 MATCH / 0 MISMATCH.**

**Honest-emptiness requirement — MET.** Every rollup cell the grok lane cannot fill renders as an
italic declared-null carrying its own reason (`glance-sec-01.png`). The card renders the lane
*because AM-1 §13.1 requires lane parity*, and then says plainly what it does not know. Notably
the underlying `state.json` stores these as `0` with an `n_tokens: 0` / `n_cost: 0` companion
denominator — the view correctly reads the denominator and refuses to print the zero. That is the
right shape: the JSON is a transport, the view is where the null is spoken.

### 4.3 Defects

**G1 — the two wide tables clip their rightmost column at rest, with no visible affordance. (Rendering, moderate.)**
Run cost card: inner table 1060 px inside a 990 px container. Per-model scorecard: 1171 px inside
990 px. Both are correctly wrapped in `-mx-3 overflow-x-auto px-3` — page-level overflow is zero at
both 1500 px and 430 px, which is the right implementation — but macOS overlay scrollbars are
invisible until a scroll gesture, so at rest the operator sees a table that simply *ends*.
Consequence (`glance-sec-05.png`, `glance-sec-06.png`): the `span` column is entirely off-screen on
the Run cost card and `currency` is clipped mid-glyph (`anthropic-ma✂`); `median wall` is entirely
off-screen on the scorecard. The Run cost card's caption spends two lines explaining what `span`
means — *it explains a column the reader cannot see*. **Recommendation:** right-edge fade mask on
the scroll container, or narrow the tokens column (it carries three facts in one cell).

**G2 — Glance and the board disagree on the AWAITING-MATT counts. (Out-of-S7-seam observation; route onward.)**
Glance header tiles read **17 Your move / 9 Matt to-do**; the board, at the same moment against the
same two files, reads **21 open / 11 open**. The six disputed items are **Q39, Q33, Q32, Q10** and
**T9, T10**. The board's rule is mechanical and published on the surface itself — *"a row counts
CLOSED only when its `#` cell is struck"* — and Tier-1 explicitly anticipates this exact class:
*"Rows whose body says RULED/DONE but whose `#` cell is not struck render as open — that is a
defect in the queue file, not in this view."* Glance's parser sets its `resolved` boolean from a
softer signal. **This is not a fleet-card defect** — the fleet card correctly renders no Matt queue
at all, which is right for a rear-view surface. But it is a same-run cross-surface divergence with
a direction: an operator reading Glance sees **six fewer things owed by Matt** than the board says.
Owner is whoever holds `glance/parser`; surfaced here rather than fixed, per read-only seam.

**G3 — the 2 non-sealed units are named only by subtraction. (Note, not a defect.)**
The card renders `32 sealed of 34` and never enumerates the other two. For the IN-FLIGHT unit that
is correct rear-view discipline. The UNBOUND unit (`run:VFX-AB`) is history rather than live state,
and it *does* appear — as the CURATION/PASS row in Verdict history — so nothing is lost. Recorded
for completeness only.

### 4.4 Verdict — Surface 2

**PASS.** 24 of 24 checked values MATCH disk truth. The REAR-VIEW-ONLY constraint holds at the data
layer, not merely in the view. The grok lane renders with honest, reasoned emptiness in every cell
it cannot fill, and never as zero. G1 is a legibility defect worth fixing before this surface is
shown to anyone who has not read the code, but no rendered value is wrong.

---

## 5. Summary

| surface | checked | MATCH | MISMATCH | verdict |
|---|---|---|---|---|
| Fleet board (`factory/ui/board.py`, Tier-2) | 31 | 30 | 1 (`pin drift` green vacuum) | **PASS-WITH-FINDINGS** |
| Glance fleet card (`glance` `#/fleet`) | 24 | 24 | 0 | **PASS** |

Neither surface fabricates a number. Neither surface prints a zero where the tape holds a null —
with the single exception of D1, where the board prints not a zero but something subtler: a green
*"none"* derived from no comparisons at all.

### The Mirror

Both surfaces were built to the same law and both mostly keep it. Where they part is instructive.
The Tier-1 report, asked whether the pins had drifted, answered *"no comparison possible —
determinate, not green."* The Tier-2 board, asked the same question of the same tape, answered
*"none"* — in green. Nothing was fabricated. One cell simply forgot that the absence of a
disagreement is not the same fact as the presence of agreement, and coloured a vacuum with the
colour of a verified all-clear. It is the smallest possible lie and it is the only one on either
board, which is why it is worth naming: a fleet board is read at a glance, and green is read
faster than the sentence beside it.

---

*Filed by galadriel 2026-08-24 for U1-BUILD gate G-3, seal item S7. Read-only against `flight/`,
`factory/ui/`, and `glance/` throughout; all writes confined to
`agentic_orchestration/galadriel/`. Servers started for capture were terminated at close (ports
8787 and 5199 verified free).*
