# Drax commissioning prompt — Glance build (v1.4: four-page split + content-emission first-glance roster)

**Authored:** gandalf, 2026-07-09, per Matt ruling (*"Can you please draft a prompt to create this tab?"*).
**Status:** PASTE-READY. KR sequences the fire (contract §9: after the current run closes; web seam only, zero collision).
**Governing spec:** `agentic_orchestration/operating-procedures/glance-contract-spec-2026-07-03.md` (SPEC-CURRENT v1.4).

---

## The prompt (paste below this line into a drax session)

Read your operating procedure skill and execute session-start protocol. Then execute this commission.

**COMMISSION: build Glance v1 — the project's derived-state web app — per the ratified contract, including the v1.4 four-page split.**

**Context you need (read in this order):**
1. `agentic_orchestration/operating-procedures/glance-contract-spec-2026-07-03.md` — the ENTIRE governing contract (v1.4). Every architectural question you'll have is answered there; where it delegates, it says so explicitly.
2. The five modeled docs: `canonical/current-to-end-state/current-to-end-state-engine.md`, `…-story.md`, `…-game.md`, `…-serial-content-emission.md`, `canonical/current-to-end-state/surface-ledger.md` — these are your parser's real fixtures. Note the serial tracker's **PART F** (KIT ROSTER OF RECORD, rows K1–K25 + H1–H6) — it is the content-emission page's lead element.
3. The two Matt queues: `canonical/matt_decision_needed/README.md` + `canonical/matt_to_do/README.md` (header-strip counters, contract §2.5).

**What you build (v1 = Tiers 0–2 + the §7.3 page split):**
- **Parser** (~300 lines, deterministic): the six legislated shapes (§2.1 STATUS banner · §2.2 SESSION-DELTA LOG · §2.3 queue rows · §2.4 `gates-on:` tokens · §2.5 Matt queues · §2.7 FLOW) → `state.json` per §3. Severity split per §2.6: malformed legislated shape = **CI failure with file+line**; dangling token/FLOW ref = **warning badge + counter**; absence is never an error.
- **Static app** (your loadout stack): routing per §7.3 — `/` = slim one-screen index of the five Tier-0 cards (the original glance survives); `/engine` · `/story` · `/game` · `/content-emission` = each tracker's card expanded in place (flow-bar lead → STATUS → deltas → queues, §4 supersession law: delta log is the truth spine, body never renders above its governing delta). Global header strip on every page: your-move count · matt_to_do count · surfaces-agreed `✓N / M` · last commit · dangling-gates count · four-tab nav · surface-ledger compact drawer.
- **Content-emission page lead-element law (§7.3):** the PART F roster table renders as the TOP card, before the flow-bar — Matt's demo-curation denominator at first glance (ID · ARPG Genre Canon kit · BC cell/hypothesis · status · blockers/held rules). Promotion is by **section-name pin** (`PART F`), not new grammar. Roster tallies (25 K + 6 H; per-status counts) join the page header.
- **CI:** `.github/workflows/glance.yml` — parse on every push to `canonical/**` + the two queue READMEs + the contract-named run-state globs (§7.1 feed 1 if trivial; it's the same six shapes on two more globs — your call at build time, contract says v1-if-trivial).
- **Deploy:** standalone Vercel project (Matt ruling: own app + URL, NOT a loadout page). Repo home is your choice; contract lean = a `glance/` app inside this collab repo so source and derived surface share one push.
- **Tier 2:** every modeled claim deep-links to file+line on GitHub. This is the provenance answer — non-negotiable.

**Founding law (violations are build-rejections, not style notes):**
- **Derived, never authored.** No hand-maintained state anywhere in the app. The repo is the database.
- **No LLM in the truth path.** No summarization, no semantic conflict detection (§4 rule 3 — order and banners only), no generated copy.
- **No server, no DB.** Parser output + static render.
- **No engine-tree reads.** Parse scope = `canonical/**` + the two Matt queues (+ the §7.1 named run-state globs). The registry pane's snapshot feed is star-lord's hook, post-v1 — do not reach into `reincarnated-engine/`.
- **Not player-facing** — team tooling; the style register / G2 gate does not apply.

**Sequencing + governance notes:**
- §2 (format law) is PROPOSED → jack-ryan ratification. Build against §2 as written; if you hit a parse ambiguity the contract doesn't answer, flag it to jack-ryan via KR — do NOT improvise new grammar (that's a format-law amendment, gandalf/jack-ryan territory).
- Staged features (Tier 3 dependency graph, RUN-STATE pane render) are NOT v1 — entry criteria live in §7. Don't build ahead of the gates.
- `gates-on:` tokens in PART F reference surface-ledger rows (`E6`) and named gates (`totem-probe`, `proxy-P0/P1/P2`) — cross-doc tokens resolve if the target row is modeled, else render as §2.6 dangling badges. That's by design; visible debt, not an error to "fix."
- MIGRATION.md per ADR-004 if anything you produce crosses seams; commit auto-fires per the team addendum; push per the batch pattern KR runs.

**Definition of done (v1):** a phone-first URL where Matt sees — in one glance — the your-move number, the five cards, the four domain pages, the content-emission roster filling in as batch-2 emits, and can reach any claim's file+line in two taps. Parse errors fail CI loudly with file+line. Nothing on the screen was authored by hand.
