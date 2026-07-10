# Glance — Contract Spec (parse contract · state model · render rules)

> **STATUS:** SPEC-CURRENT v1.8 (2026-07-10) — **Matt rulings embedded (2026-07-03): GO on the staged build · STANDALONE app · named "Glance" · fork-4 `gates-on:` tokens live on all queue-row writes NOW. v1.1 (2026-07-07, Matt-ruled fork (b)): shape #6 FLOW declaration added (§2.7) — Tier-0 renders each tracker as an abstracted end-to-end process view with drill-in; all four trackers carry `## FLOW` blocks as of this date. v1.2 (2026-07-08): §7.1 RUN-STATE pane data path spec'd — run-state docs enter parse scope + registry-snapshot export; entry criterion for the pane is MET (emission_runs registry live with 14 rows as of this date). v1.3 (2026-07-08, Matt full-run-pivot directive): §7.2 SURFACE-LEDGER card — `canonical/current-to-end-state/surface-ledger.md` enters the modeled set as a fifth Tier-0 card (same six shapes, zero new parse logic); header strip gains the surfaces-agreed counter (the demo-gate number). v1.4 (2026-07-09, Matt ruling): §7.3 FOUR-PAGE SPLIT — the app becomes four domain pages (engine / story / game / content-emission); the content-emission page leads with the KIT ROSTER OF RECORD first-glance table (serial tracker PART F, K1–K25 + H1–H6); zero new parse logic. v1.5 (2026-07-09, Matt ruling, same session — supersedes v1.4's lead-element law): §7.4 FIFTH PAGE "KITS" — the roster moves to its own `/kits` page; the content-emission page reverts to flow-bar-first (the end-to-end PIPELINE view); FLOW blocks on the serial + engine trackers get re-authored pipeline-shaped by gandalf (§2.7 grammar unchanged — zero parser impact); the Kits page is the named future consumer of the §7.1 feed-2 registry snapshot (per-kit cert truth auto-updating from emission runs). v1.6 (2026-07-10, Matt Glance-build feedback): §7.5 PRODUCT-PIPELINE FLOW SOURCES — `/engine` + `/content-emission` FLOW bars REPOINT to the dedicated MATT-FACING pipeline docs (`canonical/current-to-end-state/pipeline-battle-sim.md` S0–S8 / `pipeline-serial-content-emission.md` E0–E8); tracker FLOW blocks demoted to doc-nav; `/kits` gains the PART F.3 bench table (blocked/held B-series below F.2); §7.4-rule-4 reshape obligation discharged-by-supersession; zero new parse shapes. v1.7 (2026-07-10, executed — build version, no contract delta): §7.5 rule 4 discharged — `/story` + `/game` FLOW bars repointed to `pipeline-story.md` (N0–N5) / `pipeline-game.md` (G0–G8); built + tagged `glance/v1.7-story-game-pipeline-repoint`. v1.8 (2026-07-10, Matt ruling): §7.6 SIXTH PAGE `/minigames` — `pipeline-arcade.md` (A0–A7, POST-LAUNCH mode factory) gets its own tab; zero new parse shapes.**
> **§2 (the format law) is PROPOSED, not canon** — per `canonical-doc-format.md` §6.7, gandalf proposes + executes, **jack-ryan RATIFIES** doc-lifecycle/format governance. ⚠ SWITCH: CANON-STEWARD (proposer) → jack-ryan (ratifier) — §2 routes to jack-ryan's next governance touch; on ratification he folds it into `canonical-doc-format.md` (+ skill twin, same commit, §6.8).
> **Author:** gandalf (SPEC-AUTHOR) · run-window authoring per demo-readiness-run-spec §9 — not a wave dependency of the live run.
> **Builder:** drax (parser + app + CI — his web seam; never touches the engine tree; interleaves after the current KR run closes).

---

## 0. What Glance is

One URL that shows the true state of the project — trackers, queues, blockers, your-move items — **derived from canon on every push, authored by no one.** The founding principle decides everything downstream: *the glance layer is DERIVED, never authored.* A hand-maintained dashboard is a fifth living document that drifts (the failure class the doc-reorg killed); a Notion/Linear mirror is an authored copy with a sync job that lies within two weeks. So: canon stays in git, in markdown; a deterministic parser emits a state model on every push; a thin static app renders it. No DB, no server, **no LLM anywhere in the truth path.**

(Lineage note: proposed as "Palantír"; Matt renamed it — correctly — to what it does. The seeing-stone's classic failure was true images without provenance; Glance's answer is §6's deep-link-to-file+line on every claim.)

## 1. Architecture — boring on purpose

```
push to canonical/**  →  GitHub Action  →  parser (~300 lines, deterministic)
                                             ├── state.json  (§3 — the model)
                                             ├── parse errors → CI FAIL (file+line)   [§2.6]
                                             └── warnings (dangling tokens) → badge   [§2.6]
                          →  static deploy (Vercel — the loadout stack, drax's proven seam)
```

- **The repo is the database.** Latency push→live: a minute or two.
- **Staged build (Matt ruling):** v1 = Tiers 0–2 (§5–§6). Tier 3 (dependency graph) + the RUN-STATE pane are staged behind named criteria (§7).
- **Standalone (Matt ruling):** its own app + URL, not a loadout page. Repo choice is drax's; lean = a `glance/` app in this collab repo with its own Vercel project (source and derived surface share one push).

## 2. THE FORMAT LAW — the parse contract *(PROPOSED → jack-ryan per §6.7)*

The trackers are already semi-structured data wearing markdown clothes — ~80% of a parse contract nobody designed on purpose. This section codifies that surface. **Scope discipline: legislate the MINIMUM parseable set — six shapes** *(five at v1.0; shape #6 FLOW added v1.1, Matt-ruled)*. Everything else stays free markdown, rendered as prose, never modeled. The team's only new obligation: keep writing what they already write, *parseably*.

### 2.1 STATUS banner
First blockquote in the doc, containing the literal `**STATUS:**` marker. Parser captures: the stamp word(s) (e.g., `SPEC-CURRENT`, `CURRENT`, `LIVING`, `SUPERSEDED`, `PARTIALLY SUPERSEDED`), the first date found, the raw line.

### 2.2 SESSION-DELTA LOG
A `## SESSION-DELTA LOG` section whose entries are `### YYYY-MM-DD — <headline>` (multiple same-date entries permitted; suffixes like `(2)` tolerated). **Newest-first in the file; latest governs.** Entry body = everything until the next `###`/`##`.

### 2.3 Queue rows
A markdown table under a queue heading where each data row's **first cell begins with a row ID** (`D.1#8`, `B1`, `W0.3`, `III.8`, `Q2`, or a plain ordinal) and some cell carries a **status prefix** from the enum:

| Prefix | Meaning |
|---|---|
| `✓` | closed |
| `⛔` | blocked |
| `⚖` | awaiting Matt ruling |
| `PARKED` | parked (named re-entry) |
| `IN-FLIGHT` | executing |
| `OPEN` *(or no prefix)* | open |

The prefix is the contract; **the remainder of the cell is free prose** (`⛔ BLOCKED — REBASE` parses as blocked + prose). Bullet-list queues (non-table) are modeled iff the bullet begins with a row ID followed by `—` or `:`.

### 2.4 `gates-on:` tokens — fork-4 law (LIVE NOW, Matt 2026-07-03)
Grammar, anywhere within a modeled row's cells (or trailing on a modeled bullet):

```
gates-on: <token>[ (<qualifier>) ] [· <token>[ (<qualifier>) ]]*
token     := row ID (W3, D.1#8, B1, W0.classifier) | named-gate slug (singleton-smoke-green)
qualifier := free prose, captured not interpreted   — e.g. W2 (soft — §7 degrade)
```

**Semantics (Gate-1 #3, verbatim law): `gates-on: X` = *this row fires only after X closes.* Dependents declare their dependencies; the inverse ("unblocks") is NEVER encoded.** Multiple tokens = AND. A token *closes* when the row it resolves to reaches `✓`; a named-gate slug that resolves to no row stays **dangling** — rendered as a warning badge, never a build failure (§2.6), because named gates are events that may close in delta prose before any row exists.

### 2.5 Matt queues
`canonical/matt_decision_needed/` + `canonical/matt_to_do/`: the `README.md` index is the modeled surface — item = a heading or table row carrying a `Q`-style ID; resolved = `~~strikethrough~~` or residence in a resolved/appendix section. Counts feed the §5 header strip.

### 2.6 Severity split — the discipline that makes CI livable
- **MALFORMED instance of a legislated shape** (row with an ID cell but broken table structure; delta heading with unparseable date; duplicate row ID in one board) → **CI build failure, file+line** — same discipline as a broken test.
- **UNRESOLVED reference** (dangling `gates-on:` token) → **Glance warning badge** on the row + a global "dangling dependencies" counter. Visible debt, not a broken build.
- **ABSENCE is never an error.** A doc with no delta log, a table that isn't a queue — fine; parser models what matches, renders the rest as prose.

### 2.7 FLOW declaration — shape #6 *(v1.1, Matt-ruled fork (b) 2026-07-07)*

A `## FLOW` section near the top of a tracker declaring the doc's ordered end-to-end process view — the Tier-0 abstraction Matt asked for ("see the entire process for each system end to end, then drill in"). Grammar — an ordered list where each item is:

```
N. **<stage name>** ← <section-ref> [· <section-ref>]*
```

- **section-ref** = a substring of a `##` heading in the same doc (e.g. `PART III`). Resolution is **most-specific-first**: longer refs claim their headings before shorter refs bind (live case: the game tracker's `PART A′` must bind before `PART A`). One heading maps to at most one stage.
- **Stage state is DERIVED, never hand-stamped** — the founding principle applied to stages. Parser aggregates the modeled queue rows (§2.3) under each stage's mapped sections into the standard counter object, plus a **dominant token** for rendering, precedence: `⛔ blocked > ⚖ awaiting_ruling > IN-FLIGHT > OPEN > PARKED > ✓`. A stage whose sections carry **no modeled rows** is `quiet` (rendered neutral — frame/lineage PARTs are legitimately row-less).
- **Severity (extends §2.6):** section-ref resolving to no heading → **warning badge** + global `dangling_flow_refs` counter (visible debt, like a dangling `gates-on:` token) — never a build failure, because PARTs restructure and the FLOW map may lag a commit. Tracker with no `## FLOW` at all → fine; its Tier-0 card renders without a flow-bar. **Malformed list item** inside a declared FLOW (missing `←`, missing bold stage name, unparseable ordinal) → CI failure — malformed instance of a legislated shape, same as §2.6 rule 1.
- **Maintenance obligation:** the FLOW map is authored (it's a declaration, not derivation) — whoever restructures a tracker's PARTs updates its FLOW refs in the same commit. The dangling-ref badge is the drift alarm.

## 3. `state.json` — the parser's output contract

```jsonc
{
  "generated_at": "ISO-8601", "repo_sha": "…",
  "last_commit": { "sha": "…", "author": "…", "date": "…", "subject": "…" },
  "trackers": [{
    "id": "engine",                       // engine | story | game | serial-content-emission | surface-ledger (v1.3)
    "path": "canonical/current-to-end-state/…md",
    "status_banner": { "stamp": "LIVING", "date": "…", "raw": "…", "line": 3 },
    "deltas": [{ "date": "2026-07-03", "headline": "…", "body_md": "…", "line": 12 }],   // newest first
    "queues": [{
      "title": "…", "line": 200,
      "rows": [{
        "id": "D.1#8", "cells_md": ["…"], "owner": "star-lord",
        "status": { "token": "blocked", "prose": "REBASE" },
        "gates_on": [{ "token": "W0.classifier", "qualifier": null, "resolved": true }],
        "line": 214
      }]
    }],
    "counters": { "open": 0, "in_flight": 0, "blocked": 0, "awaiting_ruling": 0, "parked": 0, "closed": 0 },
    "flow": {                              // §2.7 — node ABSENT when the doc declares no FLOW
      "line": 24,
      "stages": [{
        "n": 1, "name": "Battle-sim deltas", "refs": ["PART I"], "resolved": true,
        "counters": { "open": 2, "in_flight": 1, "blocked": 0, "awaiting_ruling": 0, "parked": 0, "closed": 5 },
        "dominant": "in_flight",           // §2.7 precedence; "quiet" when no modeled rows
        "line": 26
      }]
    }
  }],
  "matt_decision_needed": [{ "id": "Q2", "title": "…", "resolved": false, "path": "…", "line": 9 }],
  "matt_to_do":          [{ "…": "…" }],
  "dangling_gates": [{ "token": "singleton-smoke-green", "row": "D.1#8", "path": "…", "line": 214 }],
  "dangling_flow_refs": [{ "ref": "PART X", "tracker": "engine", "stage": 3, "path": "…", "line": 27 }]
}
```

**Every node carries `path` + `line`** — provenance is schema-level, not a rendering nicety. Owner extraction: from an owner-named column when present, else the first known agent name in the row (best-effort; absent is fine).

## 4. Supersession rendering — the one subtle piece

A naive per-section render shows stale body text as current and *misleads*. The law: **the delta log is the truth spine.**

1. Render order per tracker: STATUS banner → **latest delta** (full) → older deltas (collapsed) → body PARTs. Body text never appears above its governing delta.
2. Any body section carrying a `SUPERSEDED` / `PARTIALLY SUPERSEDED` banner renders banner-first, visually de-emphasized.
3. The parser enforces **ORDER and BANNERS only** — it never attempts semantic conflict detection between delta and body (that would need judgment, i.e., an LLM in the truth path — forbidden). Latest-governs is delivered structurally.

Done right, Glance is *more* truthful at a glance than reading the raw file top-to-bottom — that's the bar.

## 5. Tier 0 — the glance (one screen, phone-first)

- **Header strip:** `matt_decision_needed` open count — **the your-move number, the most important pixel on the screen** · `matt_to_do` count · **surfaces agreed `✓N / M` (v1.3 — derived from the surface-ledger card's counters; the demo-gate number: GATE1 closes at N = M)** · last commit (agent + age) · global dangling-gates count.
- **Four tracker cards:** **flow-bar first** *(v1.1 — when the tracker declares FLOW, §2.7)*: the ordered stages as a compact segmented bar, each segment colored by its dominant token, counters on tap — the abstracted end-to-end process view is the card's LEAD element (Matt 2026-07-07: "see the entire process for each system end to end, then drill into each sub-section"). Tapping a segment deep-links to that stage's sections in Tier 1. Beneath it: condensed STATUS · latest delta (date + headline + one line) · counters (open / in-flight / ⛔ / ⚖ / parked / ✓) · top-3 open items (first three non-✓ rows by board order).
- **"Since you last looked":** the four delta logs merged, newest first; entries newer than the client's last-seen watermark highlighted. v1 watermark = **max delta-date seen** (localStorage, no server); v1.1 upgrades to SHA-precise via parser-side git-blame on delta entries. *This affordance is ~60% of the system's value — it ends re-reading-to-find-what-changed.*

## 6. Tier 1 — the drill · Tier 2 — the source

- **Tier 1 (tap a card):** the tracker's queues as live sortable/filterable tables (by status, owner, gates-on) · the delta timeline · PART list — rendered under the §4 supersession law.
- **Tier 2 (tap a row/claim):** full doc render with anchors; **every modeled claim deep-links to file+line on GitHub** (glance → drill → canon in two clicks; git history is one more) · client-side search over the canonical tree.

## 7. Staged (Matt ruling: go on the staged build — these do NOT gate v1)

| Stage | What | Entry criterion (empirical, not time) |
|---|---|---|
| **Tier 3 — dependency graph** | `gates-on:` tokens rendered as a live graph: what's blocked on what; what unblocks when the in-flight thing lands. The living mini-roadmap nobody maintains. | Token adoption density: one full board cycle where new/edited open rows carry tokens (they're law now, §2.4) + dangling rate < ~10% |
| **RUN-STATE pane** | Second pane of the same cockpit: emission runs, registry entries, cert status — the ruled "database → website tracker" direction converges here | ~~The W1 #8 run registry exists with ≥1 registered run~~ **✓ MET 2026-07-08** — `data/emission_registry.db :: emission_runs` live with 14 registered runs (schema: run_id/season_id/config_hash/kit_count/gauntlet_summary/cert_status/stage/notes; carries supersession + defect-audit records). Pane now gates only on drax's build reaching it (post-v1). |

### 7.1 v1.2 — RUN-STATE pane data path + run-state parse scope (2026-07-08)

The pane's two feeds, both preserving the founding principle (derived-never-authored, no LLM, no server):

1. **Run-state chain docs** (`agentic_orchestration/*run-state*.md` — e.g. `batch2-run-state-2026-07-06.md`) **enter the parse scope** as a named-pattern EXCEPTION to §8's `canonical/**`-only charter. They already write §2-shaped surfaces (status-prefixed queue rows, dated deltas); a chain doc that adds a `## FLOW` block (§2.7 grammar — e.g. `1. **R1 design read** ← R1` …) gets the same Tier-0 segmented flow-bar the trackers get: **the autonomous chain rendered as an end-to-end process view, each leg colored by dominant status, drill-in to the leg's rows.** Maintenance obligation identical to §2.7: whoever appends a chain delta keeps the FLOW refs true.
2. **Registry snapshot export:** the parser NEVER reads the engine tree (§8 holds). Instead, the emission driver's registry-write step (star-lord seam) also exports a snapshot JSON to `agentic_orchestration/run-registry/emission-runs-snapshot.json` in this repo (append-on-register, committed by the run — the same cross-repo pattern star-lord's completion records already use). The pane renders registry rows from the snapshot with the same path+line provenance discipline; staleness is self-declaring (snapshot carries its own `exported_at` + source mtime).

Sequencing: feed 1 is pure parser scope (drax, v1 if trivial — it's the same six shapes on two more globs); feed 2 needs star-lord's export hook (small; fires with the next registered run). Neither requires new Matt rulings — the pane itself was ruled staged 2026-07-03; this section only specs its data.

### 7.2 v1.3 — SURFACE-LEDGER card (2026-07-08, Matt full-run-pivot directive — IN v1, not staged)

Matt directive (verbatim, 2026-07-08): *"build a surface chart/table out EXACTLY like this in the Glance report as we go along. Once I agree on all surfaces for the engine, story, demo/game and content emission pipeline, then we can proceed with the demo in full view."* Operationalized without violating the founding principle — the ledger is a **canon doc written in the already-legislated shapes**, not a Glance feature:

- **`canonical/current-to-end-state/surface-ledger.md`** joins the modeled set as a **fifth Tier-0 card** (id `surface-ledger`). It is already inside the §8 parse charter (`canonical/**`) and carries STATUS (§2.1) + SESSION-DELTA (§2.2) + queue rows (§2.3, status-prefixed) + `gates-on:` (§2.4) + FLOW (§2.7). **Zero new parse logic** — one more entry in the tracker glob.
- **Row semantics (rendering note, not parser logic):** a ledger row's status prefix encodes the **Matt-agreement state** of a surface (⚖ awaiting ruling · IN-FLIGHT = ruled-FLIP being executed · ✓ = Matt-agreed · ⛔ = gate-bound). The card's counters therefore read as *surfaces agreed vs. outstanding* — surfaced in the header strip as `✓N / M` (§5).
- **The demo-gate render:** the ledger's `GATE1` row carries `gates-on: all-surfaces-agreed` (a named gate, §2.4 — dangling by design until closed in a delta). Tier-3, when it lands, renders GATE1 as the sink node of the dependency graph: the demo, visibly gated on every un-agreed surface.
- **Not a fifth tracker** (ledger header states this): trackers = build-vs-spec queues; ledger = trivialization-audit surfaces + per-surface Matt agreement. The parser doesn't care; the distinction is editorial discipline.
- **Ratification rider:** this section rides the same jack-ryan §2 ratification as the rest of the format law — no new shapes were legislated, so it adds no ratification surface beyond the glob addition.

### 7.3 v1.4 — FOUR-PAGE SPLIT + the content-emission first-glance roster (2026-07-09, Matt ruling — IN v1)

Matt directive (verbatim, 2026-07-09): *"I think we need to split the glance HTML doc into 4 pages, and this survey should roughly be the serial content emission pipeline page… Everything we currently have for content emission but also each of the numbered kits above in a table as the 'first glance', numbered with ARPG Genre Canon kit name, BC cell/hypothesis, status, blockers/held rules (if any)."*

**Page architecture (amends §5's single-screen Tier-0):**

1. **Four domain pages:** `/engine` · `/story` · `/game` · `/content-emission` — one per tracker. Each page = that tracker's full Tier-0 card **expanded in place** (flow-bar lead → condensed STATUS → latest delta full + older collapsed → counters → queue tables, all under the §4 supersession law). Tier-1 drill becomes in-page; Tier-2 (source deep-links) unchanged.
2. **Global strip on every page** (the glance survives the split): the §5 header strip — your-move number · `matt_to_do` count · **surfaces agreed `✓N / M`** · last commit · dangling-gates count — plus a four-tab nav. The **surface-ledger card** (§7.2) renders compact in the strip's drawer on every page (it's the demo gate; it belongs everywhere), full on whichever page the user expands it.
3. **Landing behavior:** `/` = a slim index of the four cards in current Tier-0 form (one screen, phone-first — the original glance), each card tapping through to its page. The split adds depth; it must not delete the one-screen glance.

**The content-emission page — lead element law:**

- **Top card = the KIT ROSTER OF RECORD table**: serial tracker **PART F** (`current-to-end-state-serial-content-emission.md`), rows K1–K25 + H1–H6. This is Matt's demo-curation denominator (fourth ruling set, one-realm §3) rendered as the page's *first glance* — before the flow-bar. Columns exactly as authored: ID · ARPG Genre Canon kit · BC cell/hypothesis · status · blockers/held rules.
- **Zero new parse logic:** PART F rows are §2.3-shaped (first-cell row IDs `K1…`/`H1…`, status-prefix enum in the Status cell, §2.4 `gates-on:` tokens inline in the blockers cell). The renderer promotes the PART-F table to the page lead by **section-name pin** (`PART F`), not by new grammar. Roster `gates-on:` tokens reference surface-ledger rows (`E6`) and named gates (`totem-probe`, `proxy-P0/P1/P2`) — cross-doc tokens resolve if the target row is modeled, else dangle as §2.6 warning badges (visible debt, by design).
- **Below the roster:** everything the serial tracker already models — FLOW bar (§2.7), STATUS, deltas, PART C/D/E queues — i.e., *"everything we currently have for content emission."*
- **Roster row count + status tallies** (25 K + 6 H; OPEN/IN-FLIGHT/✓ counts) join the page header; when batch-2 flips statuses, the page shows the roster filling in — the demo-curation pool becoming real, at a glance.

**Ratification rider:** same as §7.2 — no new shapes; a section-name pin and a routing layer are render rules (§5 territory), not parse law. Rides the standing jack-ryan §2 ratification untouched.

### 7.4 v1.5 — FIFTH PAGE "KITS" + pipeline-shaped FLOW (2026-07-09, Matt ruling, same session — amends §7.3)

Matt directive (verbatim): *"maybe we should make a 5th tab called 'Kits' as the home for the new built kits/hypotheses draft… I want to see the end-to-end desired pipeline flow on the serial content emission pipeline (and we need to build this in a way that github pushes auto update it. And the same goes for the Battle Sim page…)."* Matt's instinct fixes a conflation in v1.4: the roster is a NOUN-list (what exists), the pipeline is a PROCESS-flow (how it gets made) — they deserve separate leads.

1. **Five pages:** `/engine` (the battle-sim page) · `/story` · `/game` · `/content-emission` · **`/kits`**. Nav + global strip per §7.3 rule 2; `/` index gains a sixth card slot for Kits (roster tallies as the card face: 25 K + 6 H, per-status counts).
2. **`/kits` — the roster home:** PART F (K1–K25 + H1–H6) renders as the page lead, promoted by section-name pin exactly as §7.3 spec'd it (the pin just points at a different page now). Row drill → Tier 2 file+line. **Named future consumer of §7.1 feed 2:** when star-lord's registry-snapshot export lands, per-kit cert status (emission runs, gauntlet results) joins the roster rows as machine truth — the roster fills in automatically as batch-2 emits, no hand edit in the loop for run-derived facts.
3. **`/content-emission` reverts to flow-bar-first** — the §2.7 FLOW segmented bar IS the page lead (the end-to-end pipeline view Matt asked for), followed by STATUS → deltas → queues. Same for `/engine`: its FLOW bar leads (the battle-sim process view).
4. **Pipeline-shaped FLOW (gandalf doc obligation, NOT parser work):** the current FLOW blocks on the serial + engine trackers map doc-PARTs (navigation view). Matt wants PROCESS stages (e.g. serial: emission driver → flavor passes → bundle assembly → registry → curation → Godot consumption; engine: catalog → sampler → composer → emitters → gauntlet → bands → certification). gandalf re-authors both FLOW blocks with pipeline-named stages backed by per-station sub-headings so §2.7's one-heading-one-stage law holds and stage state stays DERIVED from real queue rows. **§2.7 grammar unchanged — the parser needs nothing.** Auto-update is the founding architecture (push → parse → deploy): stage states re-derive on every push because they aggregate live queue rows, never hand-stamps.
5. **Ratification rider:** same as §7.2/§7.3 — routing + a page, no new shapes.

### 7.5 v1.6 — PRODUCT-PIPELINE FLOW SOURCES + `/kits` bench (2026-07-10, Matt Glance-build feedback — supersedes §7.4 rule 4)

Matt feedback on the built v1.5 app (verbatim core): *"The pipelines on the Engine/Story/Game/Content Emission are pipelines made to represent state progression. What I need are the 'desired state end to end pipelines of the actual products.' I want to see what the battle sim consumes and what it does every step of the way. I want to see where/how the content emission pipeline starts, where it hands off to the battle sim, where it picks up, where it calls the LLM via API… Maybe this needs to be a part of the current-to-end-state documents so that the glance HTML doc can simply pull from there."* Plus: *"Didn't you list 10 or so more (maybe more) that are currently blocked/gated?"*

The diagnosis: tracker FLOW blocks map doc-PARTs (state-progression/navigation view) — the §7.4-rule-4 plan to reshape them in place was the WRONG fix. Product data-flow gets its own doc class.

1. **New doc class — MATT-FACING · LIVING · PURGE-EXEMPT product-pipeline docs,** homed in `canonical/current-to-end-state/`: **`pipeline-battle-sim.md`** (stages S0–S8: inputs → spawn → decision loop → cast/motion → hit/damage → termination/telemetry → gauntlet → band fit/cert → outputs) + **`pipeline-serial-content-emission.md`** (stages E0–E8: design substrate → emission driver [START] → kit gen → LLM flavor [API CALL] → sim handoff → sim → verdict pickup → bundle/registry → Matt curation gate → Godot consumption). Each carries a `## FLOW` block in the exact §2.7 grammar + doc-39-style ASCII visual + per-stage Consumes/Does/Emits/State with drill-through source links. **Purge-exempt:** these docs serve Matt, not the team — they are NEVER folded/retired/hidden without an explicit Matt ruling (the structural fix for "they keep getting hidden"). Owning agents (gamora/rocket/star-lord/drax) update stage stamps as builds land; gandalf stewards shape.
2. **FLOW-source repointing:** `/engine` page lead FLOW bar parses **`pipeline-battle-sim.md`**'s FLOW block; `/content-emission` page lead parses **`pipeline-serial-content-emission.md`**'s. Tracker FLOW blocks stay valid §2.7 grammar but are DEMOTED to doc-nav (render below the fold or in Tier-1, drax's layout call — they answer "which PART to read," not "how the product flows").
3. **`/kits` gains the bench:** serial tracker **PART F.3** (B1–B13 blocked/held table — same §2.3 table grammar) renders below F.2. The page now answers both "what's in the 31" AND "what's named-but-held" — held genre-canon is never invisible-by-omission.
4. **Story/game pipeline docs — named next, not yet authored:** game = assets → catalogue → retarget → scene assembly → capture → demo build; story = canon → run-beats → surface templates → LLM narrow-blank fill → player text. Author on Matt format-confirmation; on landing, `/story` + `/game` FLOW bars repoint identically.
5. **Ratification rider:** same as §7.2–§7.4 — source repointing + one table render, **zero new parse shapes** (FLOW grammar §2.7 unchanged; bench table is shape #3).

### 7.6 v1.8 — SIXTH PAGE "MINIGAMES" (2026-07-10, Matt ruling: *"regarding the pipeline-arcade, let's make it a 6th tab called minigames"*)

1. **Six pages:** `/engine` · `/story` · `/game` · `/content-emission` · `/kits` · **`/minigames`**. Nav + global strip per §7.3 rule 2; `/` index gains a seventh card slot (card face: A0–A7 stage states — expect PARTIAL·GAP·GATED until arcade build fires; that honest read is the point).
2. **`/minigames` — the arcade-pipeline home:** lead FLOW bar parses **`canonical/current-to-end-state/pipeline-arcade.md`** (stages A0–A7: template lattice → packet authoring → schema validation → range certification → runtime+bots → registry/rotation curation → player surface → creator exposure gates). Same MATT-FACING doc class as §7.5 rule 1: purge-exempt, same-commit stamp law, ASCII visual rendered verbatim (fenced block — do NOT parse), per-stage drill-through to spec homes (`reap-die-rise-game/arcade-minigame-taxonomy-spec.md` · `business-platform-strategy.md` · `wc3-sc-custom-game-compendium.md`).
3. **POST-LAUNCH rider renders visibly:** the doc's scope rider (nothing on this page gates the demo or launch; only the four free NOW-obligation laws are present-tense) renders near the FLOW bar so the page never reads as current build obligation.
4. **Ratification rider:** same as §7.2–§7.5 — one page + one FLOW source, **zero new parse shapes**. Stage-heading conformance (##, the v1.7 Defect-2 class) pre-verified by gandalf before relay.

## 8. Out of scope — permanently or by charter

- **No LLM in the truth path** (a narrative-digest tier may ride ON TOP later; the glance layer stays deterministic).
- **No mirrors** (Notion / Linear / GitHub Projects) — rejected: two sources of truth + sync-back.
- **Not player-facing** — team tooling; the style register / G2 gate does not apply.
- **No engine-tree involvement** — parser reads `canonical/**` + the two Matt queues only.

## 9. Seams + sequencing

| Who | What | When |
|---|---|---|
| gandalf | this contract ✓ · §2 proposal routed · **v1.1 §2.7 FLOW amendment ✓ + all four trackers' `## FLOW` blocks authored (2026-07-07)** | done (this doc) |
| jack-ryan | **ratify §2 (now six shapes — #6 FLOW rides the same ratification)** → fold into `canonical-doc-format.md` §7 (+ skill twin, same commit per §6.8) · add the CI-fail-loud entry to disciplines | his next governance touch |
| drax | parser + app + CI + Vercel project, built against §2/§3/§4/§5 **as ratified** — v1.1 adds: FLOW parse (§2.7) + `flow` node (§3) + Tier-0 flow-bar (§5) | after the current KR run closes (KR sequences; zero collision — web seam only) |
| all agents | emit `gates-on:` on queue-row writes · whoever restructures a tracker's PARTs updates its FLOW refs same-commit (§2.7) | **NOW (Matt ruling, fork 4; FLOW maintenance from v1.1)** |

---

**Sign-off:** gandalf, 2026-07-03 (SPEC-AUTHOR; §2 as CANON-STEWARD-proposer → jack-ryan-ratifier per §6.7). Anchors: Matt Glance rulings 2026-07-03 · Gate-1 #3 token semantics (demo-readiness-run-spec §3) · canonical-doc-format §6.7/§6.8 · the derived-never-authored principle (ELICITOR Q#2 analysis, this session).
