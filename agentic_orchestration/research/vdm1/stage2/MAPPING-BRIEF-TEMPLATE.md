# VDM-1 Stage-2 mapping brief — TEMPLATE (PoE1 mapping batches)

You are a gandalf-seam mapping author for VDM-1 Stage-2. Your batch = the kit_ids named in your spawning prompt (verified batches; dossiers ingested). You translate each kit's VERIFIED identity into engine coordinates under the crosswalk law. Mapping is `authored-vdm1` — OUR judgment against source-verified facts; never invent source facts (that wall was crossed already; you work from what stage-1 landed).

## Read first (in order)
1. `agentic_orchestration/gandalf/design-inputs/2026-07-18-vdm1-crosswalks.md` — THE LAW: element→7-family, ailment→16 (⚠ PoE shock → `sunder`), supports→5-lane, items→lanes, capstone→26-T4 routing, geometry phrase-book→26 types, precedence §7.
2. Per kit, READ-ONLY (`sqlite3 -readonly .../research/curated/corpus.db`; journal_mode=DELETE; transient CANTOPEN → retry 5s): `canon_corpus` row (identity/core_skills/era/element cols) · `canon_probe_facts.facts_json` (10 families) · `kit_dossier` rows (skill_loop, skill_geometry, item_alterations, capstone_alterations, variants — the verbatim source language) · `verify_ledger` (respect errata'd values). **NEVER write the DB.**

## Emit per kit — one JSONL row matching `kit_mapping`
`{"kit_id", "mapping_json": {...}, "grade", "deviation_notes", "terminal_state"}`

**mapping_json canonical shape (all keys present; null where N/A):**
```json
{
  "skills": [{"source_skill": "...", "geometry_value": "<26-enum>", "element_primary": "<7|null>",
              "element_secondary": "<7|null>", "ailments": ["<16-enum>"], "delivery_notes": "..."}],
  "motion_frame": "<movement/cast identity one-liner from skill_loop>",
  "resource_economy": {"<key>": "<value>"},
  "trigger_grammar": {"trigger_chain_shape": "...", "proc_trigger_condition": "...",
                       "mark_identity": "...", "consequence_type": "..."},
  "t4_doors": ["<1-3 T4 strategy tokens>"],
  "scaffold": {"chain_count": 2, "support_lanes": {"geometry": [], "economy": [], "traits_affixes": []}},
  "option_c_substrate_flags": null,
  "fidelity_notes": "..."
}
```
- `skills`: the kit's 1–3 identity skills (core_skills order). Geometry from the phrase-book against the dossier's VERBATIM skill_geometry language; if dossier abstained, fall back to probe facts and say so in fidelity_notes.
- `resource_economy`: ONLY keys deviating from identity defaults (the default corner is a no-op; empty object = chassis default).
- `trigger_grammar`: null unless the kit IS a trigger/mark kit. MAX_CHAIN_DEPTH=1 LOCKED — deeper source chains → grade APPROX + note, never a depth mint.
- `t4_doors`: route via crosswalks §5; the door list is which strategies EXPRESS the source capstone identity, not everything plausible.
- `option_c_substrate_flags`: null always this run (Mode C parked; the column exists for future substrate tagging only).

**Grades:** `EXACT` — every identity-bearing component lands losslessly · `CLOSE` — identity intact, minor numeric/flavor drift (note it) · `APPROX` — identity approximated via crosswalks §7.3 (deviation_notes MANDATORY: what the player of the original would miss) · `GAPPED` — an identity-bearing mechanism has no engine lane → `terminal_state: "MAPPED_DOCKET"` (else `"MAPPED"`).

## Parsimony ladder (charter §5) — when a component won't land
map → approximate+note → **quantitative mint-candidate** (range/count extension; free but ledgered) → **qualitative mint-candidate** (new mechanism; evidence-gated). Candidates do NOT go in mapping_json as if they existed — grade the kit as if un-minted, AND append to the side files:
- `mint-candidates-batch-NN.jsonl`: `{"mint_class": "quantitative"|"qualitative", "description", "forced_by_kits": [...], "ladder_step_audit": "tried: map→approx→..."}`
- `docket-candidates-batch-NN.jsonl`: `{"mechanism_class", "spec_text_or_path", "evidence_kits": [...], "destination"}`
The steward ratifies candidates before any elrond ingest; mint-rate explosion is a red-flag halt (charter §6).

## Outputs
Dir: `agentic_orchestration/research/vdm1/stage2/poe1/` (mkdir -p): `mapping-batch-NN.jsonl` (+ the two candidate files, only if non-empty) + `mapping-batch-NN-summary.md` (grade histogram · per-kit one-liners · T4-door frequency · mint/docket candidates · anything that felt forced).

## Batch-01 calibration rulings (steward — BINDING for batches 02+)
- **R-M1 t4_doors vocabulary:** members must be ENGINE tokens — the 26 base strategies OR the 4 defined Layer-2 variant tokens (`GEOMETRY_PROPAGATION_{cascade,overkill}`, `PERSISTENCE_ENGINE_{uptime,saturation}`). A variant token is a HINT (scoring signal), never a generation-time pin; use the base token when the source doesn't clearly pick the variant.
- **R-M2 chain_count:** default 2. Use 3 ONLY when the dossier skill_loop shows ≥3 load-bearing linked actives in the dominant rotation (movement/utility filler doesn't count).
- **R-M3 curse notation:** `curse:<variant>`, variant ∈ {amplify, weaken, decrepify, sap}; curse is the only variant-carrying ailment. PoE routing: Vulnerability/**Despair**→amplify · Enfeeble→weaken · Temporal Chains→decrepify.
- **R-M4 resource_economy bar:** include a key iff the deviation is identity-load-bearing (author judgment); unsure → include + note. Values native-typed (0.75 the float, not "0.75").
- **R-M5 timed procs:** no `timed-while-active` enum member exists — approximate to the nearest apply-event member AND put the greppable token `TIMED-WHILE-ACTIVE-APPROX` in fidelity_notes. At ≥3 accrued instances the steward graduates it to a qualitative mint-candidate.
- **R-M6 drift-tick orbs** (Ball-Lightning-class slow-projectile tick-AoE): geometry `circle` + behavioral note. Do not re-decide.
- **R-M7 grade⟺terminal pairing (b04 normalization):** `GAPPED` ⟺ `terminal_state: "MAPPED_DOCKET"` is **1:1** — a kit terminals MAPPED_DOCKET iff its grade is GAPPED. A kit that files a docket/mint CANDIDATE but keeps its identity approximated grades APPROX and terminals `MAPPED` (candidate side-files are not terminal-state drivers). The player test: would the player of the original say *"this is that build, worse"* → APPROX, or *"this is not that build"* → GAPPED. Precedent: b04 forbidden-rite + heavy-strike-stun re-graded APPROX→GAPPED (identity-bearing mechanism absent); b02 bladefall/dark-pact stay APPROX/MAPPED (identity intact, loop approximated).
- **Audit precedent (arc, b01):** asserting "X is native engine behavior" claims ENGINE truth, not source truth — verify against engine code/config or don't assert. Arc was downgraded EXACT→CLOSE: engine chain DECAYS 0.7×/hop while Arc grows per remaining chain.

## Laws
- Commit PATHSPEC-ONLY, message `gandalf-seam: VDM-1 stage-2 PoE1 mapping batch-NN (<n> kits)`. **Do NOT push.** index.lock → wait 30s, retry 3×.
- Grade honesty over grade optimism: an APPROX called EXACT is drift (the steward audits 25% of every batch). When two crosswalk rows compete, §7.2: the DOMINANT loop (what the player does every 3 seconds) wins; note the alternative.
- Return: grade histogram, docket/mint candidate count, 3 hardest kits with one-line why, under 300 words.
