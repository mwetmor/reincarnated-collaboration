# Glance

One URL that shows the true state of the project — trackers, queues, blockers,
your-move items — **derived from canon on every push, authored by no one.**

Founding principle: **the glance layer is DERIVED, never authored.** Canon stays
in git as markdown; a deterministic parser emits a state model on every push; a
thin static app renders it. **No DB, no server, no LLM anywhere in the truth path.**

Owner: drax (web seam). Contract: `agentic_orchestration/operating-procedures/glance-contract-spec-2026-07-03.md`
(§ 3 state.json) + `canonical-doc-format.md` § 7 (the five legislated shapes,
RATIFIED jack-ryan 2026-07-06) + engineering-disciplines Discipline #60 (CI-fail-loud).

## Architecture (boring on purpose)

```
push to canonical/**  →  GitHub Action  →  parser (parser/parse.mjs, deterministic)
                                            ├── app/public/state.json  (§ 3 contract)
                                            ├── MALFORMED shape  → CI FAIL (file+line)  [Discipline #60]
                                            └── dangling gates-on → warning badge (not a failure)
                          →  static deploy (Vercel — the loadout stack)
```

- **`parser/parse.mjs`** — the deterministic canon → `state.json` parser. NO LLM,
  NO network, NO judgment. Reads ONLY the four `canonical/current-to-end-state/`
  trackers + `surface-ledger.md` (the fifth Tier-0 card, v1.3 §7.2) +
  `canonical/matt_decision_needed/README.md` + `canonical/matt_to_do/README.md`.
  **Never touches the engine tree.**
  - `node parser/parse.mjs` — write state.json; exit 1 on any MALFORMED.
  - `node parser/parse.mjs --report` — list ALL malformed findings in one pass
    (the reconciliation surface), then exit non-zero.
- **`app/`** — Vite + React 18 + Tailwind static SPA. Renders Tiers 0–2.

## The parse contract — the five legislated shapes (canonical-doc-format § 7)

1. **STATUS banner** — first `**STATUS:**` blockquote (stamp + date + raw line).
2. **SESSION-DELTA LOG** — `### YYYY-MM-DD — headline`, newest-first, latest governs.
3. **Queue rows** — table (or modeled bullet) whose first cell begins with a row ID,
   carrying a status prefix (`✓ ⛔ ⚖ PARKED IN-FLIGHT OPEN`).
4. **`gates-on:` tokens** — `gates-on: <token> [(qual)] [· <token> …]` (AND-semantics).
5. **Matt queues** — Q/T-style IDs in the two README indexes; struck/appendix = resolved.

### CI severity split (Discipline #60 / § 7.6) — the discipline that makes CI livable

- **MALFORMED** (exactly 3 conditions: broken table structure on an ID-bearing row;
  unparseable delta date; duplicate row ID within one board) → **CI BUILD FAILURE**, file+line.
- **UNRESOLVED** (dangling `gates-on:` token) → **warning badge** + global counter. Visible debt, not a broken build.
- **ABSENCE** is never an error — a doc with no delta log, a table that isn't a queue: fine, rendered as prose.

## v1.4 — the FOUR-PAGE SPLIT (§7.3)

The app is a hash-routed SPA (zero router dependency — the vercel.json SPA rewrite
funnels every path to index.html, so hash routes work identically in preview + prod):

- **Landing `/`** (`Landing`): the slim five-card index — the ORIGINAL one-screen glance,
  preserved. Each card taps through to its domain page (the surface-ledger card opens
  the header drawer). Plus "Since you last looked".
- **Four domain pages** `#/engine · #/story · #/game · #/content-emission` (`DomainPage`):
  one per tracker, its Tier-0 card EXPANDED IN PLACE — flow-bar lead (§2.7) → STATUS →
  latest delta full + older collapsed → counters → queue tables (in-page Tier-1). All under
  the § 4 supersession law. Tier-2 source deep-links unchanged (every claim → file+line).
- **Global header strip on EVERY page** (`HeaderStrip`): the your-move pixel
  (open matt_decision_needed — the most important pixel; never dropped) · matt_to_do ·
  surfaces-agreed ✓N/M · last-commit age · dangling (gates + flow-refs) · four-tab nav ·
  the **surface-ledger drawer** (`SurfaceLedgerDrawer`) — compact, expandable, on every page.
- **Content-emission page lead** (`KitRoster`): the **KIT ROSTER OF RECORD** table (PART F,
  K1–K25 + H1–H6) as the TOP card, ABOVE the flow-bar. Promoted by SECTION-NAME PIN (the
  serial tracker's `F.1…`/`F.2…` sub-tables) — zero new parse grammar. Columns as authored:
  ID · ARPG Genre Canon kit · BC cell/hypothesis · status · blockers/held rules. Roster
  count + status tallies (25 K + 6 H) render in the card header; cross-doc `gates-on:` tokens
  (proxy-P0/P1/P2, totem-probe) dangle as § 2.6 warning badges (E6 resolves — it's a modeled
  ledger row).

## The six legislated shapes (Tiers 0–2 substrate)

Shapes 1–5 (STATUS · SESSION-DELTA · queue rows · gates-on · Matt queues) + shape 6
(§2.7 FLOW — the ordered end-to-end process view; derived stage-state, most-specific-first
ref resolution, dangling-ref warning badges). Every modeled claim deep-links to file+line
on GitHub (Tier 2). Parser enforces ORDER + BANNERS only — never semantic conflict detection.

## Staged — NOT built in v1 (§ 7 of the spec; clean seams left, no implementation)

- **Tier 3 — dependency graph** (`gates-on:` tokens as a live graph). Entry criterion:
  one full board cycle where new/edited open rows carry tokens + dangling rate < ~10%.
  Seam: `state.json.dangling_gates` + every row's `gates_on[]` already carry the graph edges.
- **RUN-STATE pane** (emission runs / registry / cert status). Entry criterion: the W1 #8
  run registry exists with ≥1 registered run. Seam: a second top-level view alongside `glance`.

## Local dev

```bash
cd app
npm install
npm run parse        # regenerate public/state.json from live canon
npm run dev          # vite dev server
npm run build        # parser (fail-loud) + tsc + vite build  → dist/
npm run build:preview  # tolerant build (writes state.json even on MALFORMED) for local preview
```

## Deploy

Standalone Vercel project **`reincarnated-glance`**. Production alias:
**https://reincarnated-glance.vercel.app** . Root Directory = `glance/app`.
`vercel.json` sets the SPA rewrite (all routes → index.html) — smoke-tested
locally before every deploy (the May-12 missing-rewrite 404 lesson). Production
deploys are Matt-authorized (ADR-006).

**Deploy from the meta-repo ROOT, not from `glance/app`.** The parser's only
input is the sibling `canonical/` tree (`../../canonical` from `glance/parser/`).
A CLI deploy from `glance/app` uploads only that subdir, so the parser can't
reach `canonical/` and the build fails (`Cannot find module .../parser/parse.mjs`
/ missing canon). Deploying from root uploads the whole context; Root Directory =
`glance/app` (set on the project) makes the build + install run there while the
parser still reaches `../../canonical`.

`.vercelignore` (at meta-repo root) allowlists the context to `glance/` +
`canonical/` only — Vercel CLI deploys ignore `.gitignore`, so without it a root
deploy would upload ~4GB of untracked heavy dirs. Keep it in lockstep with the
parser's input paths.

Redeploy:

```bash
cd ~/Games/reincarnated-collaboration   # repo ROOT (project is linked here + at glance/app)
npx vercel deploy --prod --yes          # Matt-authorized; preview = drop --prod
```

The parser's git best-effort reads (`repo_sha` / `last_commit`) return null in
the Vercel build context (no `.git` there) — by design, non-fatal.

Deployment SSO-protection is disabled on the project so the URL is publicly
shareable (standalone-app ruling). Re-enabling it would gate the URL behind
Vercel login.
