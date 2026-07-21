# Session hand-off — /corpus page LIVE + the VDM-2 mechanical-axis recognition track

> **STATUS:** SESSION WIND-DOWN · author: gandalf, 2026-07-20 · **cold-start read this first next session.** Companion durable docs: the recognition record `2026-07-20-mechanical-axis-sparseness-and-t4-ontology-recognition.md` (the design substance) + the build spec `2026-07-20-glance-per-kit-join-spec.md` (the frozen contract) — both in this folder. Session-close discipline discharged: serial-content-emission tracker fifteenth SESSION-DELTA prepended; no NEW `matt_decision_needed` row warranted (see §7).

---

## ONE-SCREEN TL;DR

**What shipped:** the Glance **`/corpus` page is LIVE in production** — `https://reincarnated-glance.vercel.app/#/corpus` — rendering the **full 574-kit VDM-1 corpus** as a browsable index + per-kit detail drill-down (all 10 joined sections per kit). This is the human-readable face of the D-11 `kit_master` one-representation consolidation.

**What was ruled:** (1) route name = **`corpus`** (Matt); (2) **push authorized** for the whole stack (Matt); (3) the deploy **root-cause fix** (`.vercelignore` allowlist gap) — executed + verified + live.

**What was recognized (deferred, NOT committed):** Matt's two observations — **mechanical-axis sparseness** + the **T4/capstone extraction "folly"** — resolve to ONE future move: a **VDM-2 structured mechanical-axis schema** where a kit's defining T4 mechanic becomes axis-VALUES, not a separate "alteration" record. Held per recognition→validate→commit; the empirical gate is a VDM-2 axis-taxonomy pass. The `/corpus` page is *also the diagnostic that makes the sparseness visible per kit* — render first, schema-complete second.

**Nothing is owed on Matt's gate from this session** — the corpus page is done and live. The next-session work is design-track (VDM-2), and it is not yet ripe for a ruling (needs the validation pass first).

---

## §1 — WHAT SHIPPED (verified live, with proof)

The **per-kit "single source of truth" page** on Glance. Architecture mirrors the existing `/atlas` route exactly — **derived, never authored; no DB / server / LLM in the live truth path.** A build-time generator reads `corpus.db` → emits static JSON → served statically. The DB is read at generate-time only.

**Live-deploy proof captured this session:**
- Live bundle hash flipped to `index-Iv_cRUd4.js` (matches the local deterministic build; the stale pre-fix bundle was `index-DlSZDEWJ.js` with zero Corpus code).
- "Corpus" occurrences in the LIVE bundle: **1** (the tab is shipped).
- `/kits/index.json` → HTTP 200, **167,521 bytes / 574 rows** — the REAL full corpus, not the 5-kit sample fallback.
- `/kits/poe2-twister.json` → HTTP 200, 13,406 bytes — per-kit drill-down reachable.

**The route surface (drax, `5e10f8ef`):**
- `/#/corpus` — browsable/filterable index off `index.json` (filter by game/tier/grade; `_row_counts` density badges).
- `/#/corpus/<kit_id>` — full per-kit detail (`CorpusKit.tsx`, 817 lines) rendering all 10 sections: `spine`, `mapping`, `mints_anchored[]`, `dockets[]`, `atlas_group`, `lineage_enrichment`, `citations[]`, `verify_ledger[]`, `dossier{}`, `_row_counts`.
- Empty/null sections render **gracefully** (the unlinked/unplaced states are common + meaningful, not errors); quarantined citations + abstained dossier rows render **visually flagged** (recorded-but-not-authoritative).

**The data seam (elrond, `3f48145c`):** productionized the 5-kit sample generator to emit all **574 kits** → `research/curated/kits-export/` (`index.json` + 574 per-kit `.json` + `kits-provenance.json` git-stamp). Build-time, deterministic, read-only — pure projection, no LLM/network/judgment.

**The staging seam (drax, `stage-kits.mjs`):** auto-detects elrond's full-corpus path (`FULL_INDEX_SRC` exists → byte-copy branch) else falls back to the frozen 5-kit sample. Correct-by-construction; the sample branch is now dead-but-harmless code. WIPE-first so exactly one served truth remains. FAIL-LOUD if a per-kit file is missing.

---

## §2 — DECISIONS RULED THIS SESSION (Matt)

| # | Decision | Ruling | Status |
|---|---|---|---|
| R1 | Glance route name for the per-kit page | **`corpus`** ("agreed on corpus name") | ✓ shipped as `/#/corpus` |
| R2 | Push the glance per-kit work + flush all committed-unpushed | **push authorized** ("2 - push" + "push anything else which hasn't been pushed yet") | ✓ all 7 session commits on `origin/main`; `origin/main..main` empty |
| R3 | The stale-deploy root cause | (diagnosis accepted; fix executed) | ✓ `1c5c27aa` live-verified |

No ruling was deferred or contested this session. All three were clean approvals.

---

## §3 — THE DESIGN SUBSTANCE: the VDM-2 mechanical-axis recognition track

**This is the load-bearing forward content.** Durable home: `2026-07-20-mechanical-axis-sparseness-and-t4-ontology-recognition.md` (this folder). Summarized here so the handoff is self-contained.

### 3.1 Matt's two observations (2026-07-20, reviewing the /corpus sample)

1. **Mechanical sparseness.** "We only have skill mechanics for certain skills, and we seem to be missing a lot of other mechanical axes to describe the builds/kits." (Better than pre-VDM-1, but incomplete.)
2. **T4/capstone extraction "folly."** "Each Kit is exactly the portion of ONE class from the source game that has ALREADY been mechanically altered by a potential capstone/T4 mechanic. So to then look for another alteration beyond the kit's existence itself is folly."

### 3.2 On (2) — the ontology error (the sharp one)

Matt is correct and the sample proves it. **A kit IS the already-T4-altered artifact** — base skill + its defining capstone/keystone/ascendancy mechanic, captured as one unit *because that fusion is what makes it a distinct build.* The `kit_dossier.capstone_alterations` family asks "what capstone alteration modifies this kit?" — which **presupposes a pre-T4 base to alter *from*. There is none.** The kit's existence already encodes the alteration.

**Evidence:** `poe2-twister.capstone_alterations` = `{"ascendancy":"Spirit Walker (Huntress)","notables":["not individually named…"]}`, **conf 0.45** — the agent hunted for a separate alteration, found the kit's own identity staring back, returned a low-confidence near-empty. Structural confusion, not an extraction miss.

**Distinction to preserve:** the kit's ONE *defining* alteration is redundant to re-record (it IS the kit). A kit may *also* stack *supporting* build-defining choices (extra keystones/notables) — legitimate detail, but mis-framed as "the alteration." The fix is not "capture more alterations"; it's "stop modeling the defining alteration as an external modifier."

### 3.3 On (1) — sparseness is the same problem's other face

We capture kits richly on *some* axes (the 12 `mint_ledger` primitives = *novel* mechanics; `kit_dossier` prose for *documented* skills) but lack a **complete, structured, per-kit mechanical-axis schema.** The atlas coords are the *start* of one but are sparsely populated + not comprehensive.

**Proof:** to find the autonomous-emitter family I had to **keyword-sweep dossier prose** ("wander/erratic/moves-toward") because "self-locomotion/autonomy" **is not a captured axis.** Had it been a column, it's a `SELECT`, not a text-sweep.

### 3.4 Empirical census — from the frozen 574-kit export (what the /corpus page shows)

| finding | count | bucket |
|---|---|---|
| every kit has a coordinate mapping | 574 (100%) | **floor** — the one universal axis |
| no attested element | 302 (53%) | **mixed — see element note** |
| ≥1 abstained ("source silent") dossier fact | 339 (59%) | **real mechanical sparseness** → the thesis |
| lineage_enrichment null | 574 (100%) | **structural, NOT sparseness** |
| atlas-grouped (has a plane group) | 85 (15%) | **structural** (labeling coverage) |
| forces ≥1 mint | 21 (4%) | expected — mints rare by design |

- **59%-abstained = the quantified proof of (1).** Abstention is *honest* ("source didn't say") → a clean diagnostic, not corruption.
- **100%-lineage-null + 15%-atlas-grouped are STRUCTURAL, not thinness.** `roster_lineage_enrichment` FKs `roster_atlas` (the 45 engine-generated B*/H* kits) — a **universe disjoint from the 574 corpus kits.** Lineage is null for all corpus kits by construction. The per-kit page rendering null lineage on every kit is the diagnostic *surfacing the atlas-refresh-on-corpus-universe gate* (same gate blocking the pinnacle decision), not a bug.

### 3.5 The element sub-finding (course-corrects any "historical element per kit" plan)

The 53%-no-element is **mostly not a capture gap.** Name-heuristic split of the 302 blanks: only **~27 (9%)** are elementally-named-but-blank (candidate true misses: "Lightning Spear Sorcerer", "Snowstorm Frost Caster"). The other **~275 (91%)** are *correctly* non-elemental (Whirlwind Barb, Golemancer, Split-Arrow-Bleed, Blessed Hammer, Corpse-Explosion Necro). **A blind element backfill would falsely paint a whirlwind barb "fire."**

Deeper: under the Archive-Frame **element-as-reader-signature** ruling (`matt_notes_handoff_docs/rdr-archive-frame-narrative-spine.md` §3.2), a kit's *source-game* element is **lineage flavor, not a mechanical property** — in RDR the element comes from the player/reader. So "historical element per kit" is a **small (~27-kit) lineage-color pass, not a corpus-wide fill**, and it must classify **three ways (attested / correctly-non-elemental / true-miss), never two.**

### 3.6 Cross-seam corroboration (drax render seam, `c1a01478`)

The thesis got **independent confirmation from a second seam.** Building the per-kit render, drax flagged that `mapping.mapping_json`'s mechanical payloads (`resource_economy`, `trigger_grammar`) are **free-form + vary per kit** (twister has `persistent_condition_shape`; VBV has `charge_stack_sub_shape`) — renderable only as pretty-printed JSON, not first-class fields. Same for `dossier` payloads (`variants` = `{known_variants}`/`{list}`/`{variants}`). **Same wall from the opposite side:** I hit "mechanical detail isn't a structured axis" by *keyword-sweeping prose* (query seam); drax hit it by *falling back to JSON blocks* (render seam). Two seams, one finding → the axis schema is the right move. **Ruling: batch the frozen-contract re-sync into the VDM-2 pass (re-sync once), NOT piecemeal per flag** — the page renders faithfully today via pretty-JSON, so no urgency to churn the contract now.

### 3.7 The unifying fix (VDM-2 CANDIDATE — NOT committed)

(1) and (2) resolve to **one** move: **replace the confused "alterations" extraction with a structured mechanical-axis schema, where the kit's T4/defining identity becomes axis-VALUES, not a separate "alteration" record.**
- Retire/reframe `kit_dossier.capstone_alterations` (folly as posed).
- Define missing axes as first-class columns. Candidates surfaced this session: **locomotion_mode** (static/player-orbital/drift/self-seeking/roaming/host-attached) · **trigger_condition** (on-cast/proximity-armed/timed/channel) · **persistence** (instant/duration-entity/permanent) · **targeting** (aimed/homing/undirected) · **resource-coupling** (stat→damage, the HoWA axis). **Let the kits VOTE which axes earn a column** (substrate-led — do NOT pre-impose a giant schema).

### 3.8 Prediction registered (the validation gate)

When VDM-2 defines `locomotion_mode` and backfills it: (a) the roaming-emitter family becomes a clean `SELECT` (no keyword sweep), (b) mints #8/#10 promote as their four unlinked members anchor, (c) `capstone_alterations` confusion disappears (defining mechanic now lives in axis-values). **If those three hold, the fix is validated.**

---

## §4 — THE DEPLOY-INFRASTRUCTURE LESSON (the "D7 lesson," reinforced)

**Symptom:** Matt reported no Corpus page live even after the code shipped + pushed. **Root cause:** the repo-root `.vercelignore` is an **allowlist** (`*` ignores everything, then `!path` negations un-ignore only the trees the build reads). It never un-ignored `research/curated/kits-export/`, so the Vercel deploy context **dropped stage-kits' 574-file input** → stage-kits found neither the corpus tree NOR the gandalf/notes sample fallback → **failed loud** → the last pre-corpus deploy kept serving.

**The trap (the "D7 lesson," now hit a THIRD time — atlas E3, atlas E4, now corpus):** `.vercelignore` is **INERT locally.** The local `npm run build` staged full-corpus green, so the allowlist gap is INVISIBLE until the deploy build. Any build INPUT that lives OUTSIDE `glance/` MUST be explicitly un-ignored or the deploy build breaks while local stays green.

**Fix (`1c5c27aa`):** added two un-ignore lines + a header comment recording the lesson:
```
!agentic_orchestration/research/curated/kits-export
!agentic_orchestration/research/curated/kits-export/**
```
Verified in an isolated temp git repo: `index.json` + a sample per-kit file + `kits-provenance.json` INCLUDED; `corpus.db` + the gandalf/notes sample DROPPED (correct — the DB never ships).

**Redeploy nuance flagged to Matt (and confirmed resolved):** the fix is a NEW commit, so "Redeploy" of the OLD failed deployment (`c1a0147`) would rebuild the old commit and fail again — must build **latest main.** Matt redeployed correctly; page went live.

**Forward guard for next session:** any new Glance surface whose build input lives outside `glance/` → add the `.vercelignore` un-ignore in the SAME change, and verify in an isolated context (local green is not evidence). This is now the third instance; it is a standing deploy-lane checklist item.

---

## §5 — FOLLOW-UP PUNCH LIST (by owner / seam / gate)

Nothing here is authorized to fire without Matt's go. Ordered by readiness.

| # | Item | Owner | Gate / trigger | Notes |
|---|---|---|---|---|
| F1 | **VDM-2 mechanical-axis schema** — the unifying fix (§3.7) | **gandalf** (axis-taxonomy *design* + genre precedent per axis) + **elrond** (corpus schema); optional **legolas Mode A** (how ARPG theory decomposes build-mechanics) | **NOT YET RIPE** — recognition→validate→commit. Empirical gate = a VDM-2 axis-taxonomy pass (which axes do the 574 kits actually distribute on?). Ratify: jack-ryan / Matt. | The `/corpus` page is the diagnostic that motivates this. Do NOT bundle schema work into the render build. Let the kits vote the columns; do not pre-impose. |
| F2 | **Retire/reframe `kit_dossier.capstone_alterations`** | elrond (schema) + gandalf (design intent) | Rides F1 (part of the same schema pass) | Folly as posed. If supporting-stack detail is wanted, ask it as a distinct question. |
| F3 | **`locomotion_mode` axis** (first column to add; unblocks the roaming-emitter family + mints #8/#10) | gandalf design → elrond backfill | Rides F1; the registered prediction (§3.8) validates it | Highest-value single axis — turns a prose keyword-sweep into a `SELECT`. |
| F4 | **frozen-contract re-sync** — promote the free-form `mapping_json`/`dossier` payloads to first-class fields | elrond (emit) + drax (render) | Rides F1 (batch once, per the §3.6 ruling) | Page renders faithfully via pretty-JSON today → NO urgency; churning the contract now = drift-bait. |
| F5 | **~27-kit historical-element lineage pass** (three-way classification) | elrond + gandalf | Independent of F1; small | Explicitly NOT a corpus-wide fill. Element = reader-signature (lineage flavor). Must classify attested / correctly-non-elemental / true-miss. |
| F6 | **atlas-refresh-on-corpus-universe** — the 574 corpus kits are a universe disjoint from the 45 `roster_atlas` kits (why every corpus kit shows null lineage) | elrond + gandalf | Already tracked under **Q32** (atlas-parity run gate roster) | The per-kit page SURFACED this gate; it is the same gate blocking the pinnacle-mint decision. No new action — it's an existing gate now with a visible symptom. |

**Not follow-ups — HANDLED (see §6):** stage-kits source path, terminal_state index asymmetry, drax's three shape-flags.

---

## §6 — HANDLED / NON-ISSUES (so nobody re-opens them)

- **stage-kits source-path coordination** — drax independently guessed elrond's vendored path (`research/curated/kits-export/`); the seam is clean (574-row index, 0 missing per-kit files). The `TODO(drax)` in the script header is now satisfied by the full-corpus branch firing; the sample branch is dead-but-harmless. No relay was needed.
- **`terminal_state` index asymmetry** — elrond's index rows omit `terminal_state`; drax's `indexRow` includes it in sample-mode; drax renders it conditionally so absence is harmless. Downgraded from "owed" to "handled."
- **drax's three shape-flags** (`resource_economy`/`trigger_grammar` free-form; `variants` key-name variance) — these ARE the §3.6 corroboration, already folded into F4. Not separate debt.

---

## §7 — SESSION-CLOSE DISCIPLINE (discharged)

- **Serial-content-emission tracker** — fifteenth SESSION-DELTA prepended (the /corpus page LIVE + the VDM-2 recognition + the deploy lesson). Latest delta governs.
- **`matt_decision_needed` queue** — **no NEW row warranted.** Rationale: the three decisions this session (route name, push, deploy fix) were all ruled/executed same-session. The VDM-2 fire-decision is a FUTURE Matt-gate but **not yet ripe** (recognition→validate→commit — the axis-taxonomy validation pass gates it, not Matt's ruling yet). The atlas-refresh gate is already tracked under Q32. Surfacing a premature row would violate the "only decisions that genuinely need Matt *now*" contract.
- **`matt_to_do` queue** — untouched (no new host/credential-level action).

---

## §8 — STANDING ITEMS CARRIED (pointers, not re-assertions — the durable homes govern)

These predate this session; listed so cold-start sees the whole board. **Do not treat this list as authority — the linked homes govern** (duplicating detail here is exactly the drift this project fights).
- **VDM-1** — RUN CLOSED + Matt-ratified (`b6713768`); corpus stamped `v1.1-verified`. The `/corpus` page is its human-readable face. Home: serial-content-emission tracker fourteenth delta.
- **Q32** — atlas-parity run gate roster (consolidated; includes the atlas-refresh-on-corpus-universe gate that F6 surfaces + the pinnacle/shapeshift tail). Home: `matt_decision_needed/2026-07-17-atlas-parity-run-gate-roster.md`.
- **Story-session cluster (Q2 / Q3 / Q4)** — run-persistence contract, companion-ship question, keystone [OPEN] cluster. Home: `current-to-end-state-story.md` + the queue README.
- **Q10** — one band-time loot item (resist/mitigation caps, arrives WITH the band-sheet). Home: `reap-die-rise-engine/agnostic-loot-engine-spec.md`.
- **Q12** — rolling surface-ledger demo gate. Home: `current-to-end-state/surface-ledger.md`.

---

## §9 — COMMIT MANIFEST (this session — all on `origin/main`)

| commit | author | what |
|---|---|---|
| `e9ea12e0` | gandalf | glance per-kit SSOT — approved 5-kit sample + build spec + T4-ontology recognition |
| `3f48145c` | elrond | glance per-kit SSOT generator — corpus→JSON at 574 |
| `655f4b1c` | gandalf | recognition record — empirical census backing (574-kit export) |
| `5e10f8ef` | drax | glance per-kit corpus SSOT — /corpus index + /corpus/:id detail render |
| `94d7b914` | drax | AGENT_STATE v1.15 — per-kit render checkpoint + elrond source-path resolution |
| `c1a01478` | gandalf | recognition record — drax cross-seam corroboration of the VDM-2 thesis |
| `1c5c27aa` | gandalf | fix deploy — un-ignore kits-export in `.vercelignore` (/corpus was failing) |

---

## §10 — COLD-START READ ORDER FOR NEXT SESSION

1. **This doc** (§1–§5 for state; §3 + §7 for what's live vs deferred).
2. **The recognition record** — `2026-07-20-mechanical-axis-sparseness-and-t4-ontology-recognition.md` (the VDM-2 design substance + the registered prediction).
3. **The build spec** — `2026-07-20-glance-per-kit-join-spec.md` (the frozen interface contract, if touching the page).
4. **Serial-content-emission tracker** — fifteenth SESSION-DELTA (this session) + fourteenth (VDM-1 close).
5. **`matt_decision_needed/` README** — for the standing Matt gates (Q32, Q2–Q4).

**If next session is the VDM-2 kickoff:** start with the axis-taxonomy validation pass (which axes do the 574 kits distribute on?) BEFORE any schema commit — the substrate votes the columns. gandalf owns the axis *design* + genre precedent; elrond owns the corpus schema; jack-ryan/Matt ratify. Optional legolas Mode A on ARPG build-mechanic decomposition.

**Signed:** gandalf, 2026-07-20. The corpus page is live; the sparseness it renders is honest and by design; the schema that closes it is recognized, predicted, and gated — not yet built.
