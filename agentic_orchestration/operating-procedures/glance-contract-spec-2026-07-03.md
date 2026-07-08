# Glance — Contract Spec (parse contract · state model · render rules)

> **STATUS:** SPEC-CURRENT v1.2 (2026-07-08) — **Matt rulings embedded (2026-07-03): GO on the staged build · STANDALONE app · named "Glance" · fork-4 `gates-on:` tokens live on all queue-row writes NOW. v1.1 (2026-07-07, Matt-ruled fork (b)): shape #6 FLOW declaration added (§2.7) — Tier-0 renders each tracker as an abstracted end-to-end process view with drill-in; all four trackers carry `## FLOW` blocks as of this date. v1.2 (2026-07-08): §7.1 RUN-STATE pane data path spec'd — run-state docs enter parse scope + registry-snapshot export; entry criterion for the pane is MET (emission_runs registry live with 14 rows as of this date).**
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
    "id": "engine",                       // engine | story | game | serial-content-emission
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

- **Header strip:** `matt_decision_needed` open count — **the your-move number, the most important pixel on the screen** · `matt_to_do` count · last commit (agent + age) · global dangling-gates count.
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
