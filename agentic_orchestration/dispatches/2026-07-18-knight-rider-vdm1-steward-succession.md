# KR session brief — VDM-1 orchestration succession (fable-5 conservation)

**Drafted:** 2026-07-18 by gandalf (VDM-1 run steward) under Matt's fable-5 conservation ALERT ("draft a Knight-Rider (opus 4-8) session … for orchestration").
**Purpose:** let a knight-rider session on the opus 4-8 budget take over the MECHANICAL orchestration loop of the VDM-1 autonomous run when the gandalf steward session's fable-5 budget exhausts. Until cutover, the gandalf session continues the loop; this brief is the contingency + cutover protocol. Launch: `cd ~/Games/reincarnated-collaboration && claude --agent knight-rider`, then paste: *"Adopt VDM-1 orchestration per `agentic_orchestration/dispatches/2026-07-18-knight-rider-vdm1-steward-succession.md`. Execute the loop from current run-state."*

## 0. SPEND LAW (Matt 2026-07-18 — ABSOLUTE)

Every spawn = **NAMED seam agent** (`subagent_type`) + **explicit `model: "sonnet"`** + `run_in_background: true`. NEVER un-named subagents (claude/general-purpose/Explore/Plan), NEVER model-inherit (omitting `model` inherits the parent = fable-5 burn). Orchestrator work stays in-session on the KR budget. Background agents notify on completion — never poll, never read their transcript output files.

## 1. Ground truth (read in order at adoption)

1. `agentic_orchestration/gandalf/notes/2026-07-18-vdm1-run-state.md` — THE LEDGER (append bullets via the established python-replace pattern before `## Basin checkpoints`; never rewrite history bullets)
2. `agentic_orchestration/research/vdm1/stage2/basin3/WAVE-PLAN.md` — wave map m01–m15, per-batch hot-facts, standing counts
3. `agentic_orchestration/research/vdm1/stage2/basin3/MAPPING-BRIEF-TEMPLATE.md` — the mapper brief (template-as-brief)
4. `agentic_orchestration/research/vdm1/review-book-accumulators.md` — review-book staging index (amend header at each close)
5. Charter: `agentic_orchestration/gandalf/design-inputs/2026-07-18-vdm1-charter.md` (R-8b; red-flag classes; no Matt interaction until THE REVIEW BOOK except red-flags — ledger currently EMPTY)

## 2. Position at drafting

PoE1 94 ✓ · basin-1 48 ✓ · basin-2 76 ✓ · basin-3 crawl+backfill+INGEST-13 CLOSED & D-2c-verified (effective 681 = 573C/89U/18X/1SNF; ERRATA-43..55; promotions 124/179 gate-pass) · **MW1 IN FLIGHT** (m01+m02+m03, gandalf-seam sonnet background ×3). Remaining: MW1 audit → MW2..MW5 → basin-3 checkpoint row → INGEST-14 → LE 53 tail → Stage 5 blind rider → THE REVIEW BOOK. All work committed+pushed through `37e05bda`; nothing lives only in session memory.

## 3. The per-wave loop (repeat MW2..MW5; MW1 already fired)

1. **Roster recount BEFORE fire** — python over `stage1/basin3/batch-NN-verify.jsonl`, distinct kit_ids; must match WAVE-PLAN batch↔roster map (12 kits; m15=11).
2. **Spawn 3 mapping authors** — prompt skeleton = `stage2/basin3/MW1-SPAWN-PROMPTS.md` (clone per batch: swap batch number, roster, and the per-batch hot-facts line from WAVE-PLAN §hot-facts). Spend law §0 applies.
3. **On each return (D-2c — advisory NEVER trusted):**
   - recount grade histogram from the COMMITTED `mapping-batch-NN.jsonl` (not the agent's return text);
   - ≥25% deep-audit: per sampled kit, every ailment/mechanic token must cite fetched `kit_dossier` language or `verify_ledger.anchor_quote` (store-not-style; probe facts/mech_note ILLEGAL grounds);
   - **FULL-BATCH contiguity battery**: every quoted attestation must appear CONTIGUOUS in its store (splice = leak; basin-2 pattern — grep the quoted span against the DB text);
   - roster coverage NN/12, no phantom kits, terminal_state legality (GAPPED⟺MAPPED_DOCKET).
4. **Amend** WAVE-PLAN hot-facts if a return surfaced new adjudication; append run-state bullet per wave close; update accumulators header.
5. **Commit steward artifacts + PUSH at wave close** (mappers commit pathspec-only, never push).

## 4. Law-boundary rule (KR is orchestrator, not law-author)

Mapping law = main crosswalk doc + basin-3 addendum (`gandalf/design-inputs/2026-07-18-vdm1-crosswalks*.md`). Where a mapper files a question BOTH docs are silent on: **park it in run-state as OPEN — do not improvise law, do not answer design questions in KR voice.** Mint/docket candidates from mappers accumulate in side-files; steward consolidation happens at review-book stage. Grade disputes: files+law govern; if genuinely ambiguous, grade stands as-filed with an OPEN note.

## 5. After MW5

1. **Basin-3 checkpoint ROW** in run-state (format: mirror the basin-1/basin-2 rows under `## Basin checkpoints`).
2. **INGEST-14** — commission **elrond** (sonnet, background): ingest `mapping-batch-01..15.jsonl` into `kit_mapping` (218 → 397). Contract pattern: `research/curated/MIGRATION-vdm1-ingest13-2026-07-18.md` (single writer · FILES GOVERN with PRE-LOAD recount asserts · backup+md5 chain from post-md5 `90e29009…` · pathspec commit, no push). Steward battery on return (exemplar: `stage1/basin3/ingest13-d2c-battery.sh`).
3. **LE 53 tail** — Last Epoch no-probe kits: crawl (legolas-seam, sonnet) → verify/dossier → map, per the basin-2 LE pattern in run-state.
4. **Stage 5 blind rider** — per charter.
5. **THE REVIEW BOOK** — gandalf-class deliverable. If a gandalf session is affordable then, it authors from `review-book-accumulators.md`; else KR assembles the mechanical compilation from the accumulators + run-state and FLAGS it "assembly-only, gandalf pass owed."

## 6. Standing rules

- Red-flag pings to Matt only per charter classes (ledger EMPTY at drafting).
- Rolling status summary to Matt at each wave boundary (standing directive).
- BACKFILL-2 re-crawls still queued: le-bomb-lance, gd-berserker-wereforms (ride with LE tail).
- Steward-fallibility register: 2 basin-3 entries so far (citations-header slip; 4-row pre-state assumption) — new steward errors append there via run-state.
- No sleep/time-of-day framing toward Matt; workstream-relative only.

**Signed:** gandalf (run steward) — succession-ready; gandalf session continues until budget wall or Matt cutover.
