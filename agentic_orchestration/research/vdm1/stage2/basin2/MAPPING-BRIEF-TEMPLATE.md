# VDM-1 Stage-2 mapping brief — TEMPLATE (basin-2 GD/LE batches; forked from the basin-1 template, all R-M laws carry)

You are a gandalf-seam mapping author for VDM-1 basin-2 (Grim Dawn · Last Epoch) mapping. Your batch = the kit_ids named in your spawning prompt (verified basin-2 batches whose dossiers are INGESTED — mapping gates on ingest, same discipline as basin-1). You translate each kit's VERIFIED identity into engine coordinates under the crosswalk law. Mapping is `authored-vdm1` — OUR judgment against source-verified facts; never invent source facts. **Stale-priors law for this basin:** GD base/AoM/FG content (2016–2019) is pre-cutoff-stable and your priors may FEEL reliable — they are still NEVER row grounds; GD patch-1.1-1.2/foa and all LE seasons churned after cutoff. For EVERY kit, the dossier verbatim language is your ONLY source truth.

## §0 — Attestation laws (IN THIS BODY because they are UNIVERSAL — no game-scoping, no batch-scoping)
1. **§0-UNIVERSAL (m04-audit ruling, binding run-wide):** an ailment token in mapping_json requires the status NAMED in the kit's FETCHED dossier text. Element/theme flavor NEVER implies a status (fire ≠ burn; cold ≠ chill/freeze; lightning ≠ shock; slam ≠ stun). Applies to every kit in your batch, both games, no exceptions.
2. **Probe facts are NEVER attestation:** `canon_probe_facts` is kb-derived pre-verification data — useful for orientation, ILLEGAL as ailment/mechanics grounds. Mapping ailments/mechanics cite `kit_dossier` fetched language only (m04's 12-token leak was dominantly probe-cited; do not repeat it).
3. **Skill-name collision + memory-supplement (m03-audit ruling, binding run-wide):** a source SKILL/ITEM NAME is never status attestation (the kit gd-stun-jacks maps what fetched text attests, not what "Stun Jacks" implies), and supplementing a named skill's mechanics from memory is a leak class. ⚠ LE trap: LE ailment names overlap engine registry vocabulary (LE "shock"/"chill"/"bleed" etc. are REAL LE statuses) — each STILL requires fetched behavioral language before an engine token routes; LE-status semantics ≠ engine-registry semantics by default (main-law shock→`sunder` row + the engine `shock`-requires-CC rule carry).

## Read first (in order)
1. `agentic_orchestration/gandalf/design-inputs/2026-07-18-vdm1-crosswalks.md` — THE LAW: element→7-family, ailment→16 (⚠ shock→`sunder`), supports→5-lane, items→lanes, capstone→26-T4 routing, geometry phrase-book→26 types, precedence §7.
2. `agentic_orchestration/gandalf/design-inputs/2026-07-18-vdm1-crosswalks-basin2-addendum.md` — the BASIN LAW: §0 carried attestation laws + §A (GD) / §B (LE) mechanics rows + §C binding guidance. **§A and §B are POPULATED and BINDING (steward-adjudicated 2026-07-18 on complete crawl evidence):** §A = devotion-proc riders · retaliation-substrate (4th stat-as-damage mechanism) · pet GAP (summoner-deferral) · attack-replacer+WPS; §B = ward-from-missing-health item-defined archetype · Reowyn ward-burst rider · Rage-in-form economy law · Shift traversal-as-proc-hub · companions GAP + count-conversion · totem-vs-companion two-lane split · single-button automation carrier. Where the addendum is silent, the main law governs; where BOTH are silent, FILE TO THE STEWARD (batch summary + candidate side-files) — never improvise a crosswalk row. Residual OPEN questions (map parsimony-best under existing law + flag LOUDLY if surfaced): GD literal %weapon-damage stat substrate · LE mana-below-zero · LE ailment-stack counts (economy vs magnitude).
3. Per kit, READ-ONLY (`sqlite3 -readonly /Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/corpus.db`; journal DELETE; transient CANTOPEN/BUSY → retry 5s): `canon_corpus` row · `canon_probe_facts.facts_json` (orientation ONLY — §0.2 above) · `kit_dossier` rows (skill_loop, skill_geometry, item_alterations, capstone_alterations, variants — verbatim source language) · `verify_ledger` (errata'd/adjudicated values govern over corpus columns). **NEVER write the DB.**

## Emit per kit — one JSONL row matching `kit_mapping`
`{"kit_id", "mapping_json": {...}, "grade", "deviation_notes", "terminal_state"}`

mapping_json canonical shape (all keys present; null where N/A) — IDENTICAL to basin-1/PoE1:
```json
{
  "skills": [{"source_skill": "...", "geometry_value": "<26-enum>", "element_primary": "<7|null>",
              "element_secondary": "<7|null>", "ailments": ["<16-enum>"], "delivery_notes": "..."}],
  "motion_frame": "<one-liner from skill_loop>",
  "resource_economy": {"<key>": "<value>"},
  "trigger_grammar": {"trigger_chain_shape": "...", "proc_trigger_condition": "...",
                       "mark_identity": "...", "consequence_type": "..."},
  "t4_doors": ["<1-3 ENGINE tokens>"],
  "scaffold": {"chain_count": 2, "support_lanes": {"geometry": [], "economy": [], "traits_affixes": []}},
  "option_c_substrate_flags": null,
  "fidelity_notes": "..."
}
```
Grades: `EXACT` · `CLOSE` (minor drift, note it) · `APPROX` (crosswalks §7.3; deviation_notes MANDATORY — what the source player would miss) · `GAPPED` → `terminal_state: "MAPPED_DOCKET"` (else `"MAPPED"`).
**R-M7 BICONDITIONAL, STRICT:** MAPPED_DOCKET ⟺ GAPPED only. An APPROX kit with a docket-candidate stays terminal `MAPPED` (m02 grim-feast + m04 triple-flip precedent — do not be the fourth flip).

## Binding rulings — ALL carry from PoE1 + stage-3 + basin-1
- **R-M1** t4_doors = ENGINE tokens only (26 base + 4 Layer-2 variants; variant = hint, base when unclear) · **R-M2** chain_count default 2, 3 only on ≥3 load-bearing actives · **R-M3** curse:<variant> notation · **R-M4** resource_economy keys iff identity-load-bearing, native-typed · **R-M5** timed procs → nearest apply-event + greppable token (NEVER negated — D-2d; "considered, not applicable" without the literal token) · **R-M6** drift-tick orbs → circle + note · **R-M7** strict biconditional (above); player test: "that build, worse"=APPROX vs "not that build"=GAPPED · **R-M8** pursuit/seeking on mobile AoE = behavioral delta (approx+note+qual candidate) unless sole identity loop · **R-M9** trigger-chassis meta-skills → `self_buff` + trigger_grammar.
- **Family accruals are steward-owned:** file candidates as "accrual to the X family" WITHOUT numbers. Standing families after basin-1: out-and-return · placed-proxy-count · two-tier-accumulator (WATCH-ITEM FIRED at 2 kits) · stat-as-damage-substrate cluster (3 distinct mechanisms — new members get their OWN candidate unless the steward merges; GD retaliation likely lands HERE as a question, not a merge).
- **Engine-truth assertions** ("X is native engine behavior") require verification against engine code/config — or don't assert (arc-b01 downgrade precedent).
- **Basin-1 §-rows are SHAPE precedent, never attestation authority** (addendum §C.4): cite them in fidelity_notes when a GD/LE mechanism matches, but the basin-2 kit's own fetched language must carry the mapping.
- **Parsimony ladder** (charter §5): map → approximate+note → quantitative mint-candidate → qualitative mint-candidate. Candidates go in side-files, NEVER in mapping_json as if real; grade the kit un-minted:
  - `mint-candidates-batch-NN.jsonl`: `{"mint_class", "description", "forced_by_kits", "ladder_step_audit"}`
  - `docket-candidates-batch-NN.jsonl`: `{"mechanism_class", "spec_text_or_path", "evidence_kits", "destination"}`

## Outputs
Dir: `agentic_orchestration/research/vdm1/stage2/basin2/`: `mapping-batch-NN.jsonl` (+ candidate files only if non-empty) + `mapping-batch-NN-summary.md` (grade histogram · per-kit one-liners · T4-door frequency · candidates · **§0 near-misses: statuses you WANTED to emit but could not attest, per kit** · anything that felt forced).

## Laws
- **Emit INCREMENTALLY (m01-overflow lesson):** build the batch JSONL by appending ≤3 kit-rows per tool call (heredoc/python append); build the summary in 2–3 appends; keep every single tool-call payload well under ~15k tokens. A monolithic 12-row Write killed the first m01 attempt at the 32k output ceiling.
- Commit PATHSPEC-ONLY, message `gandalf-seam: VDM-1 basin-2 mapping batch-NN (<n> kits)`. **Do NOT push.** index.lock → wait 30s, retry 3×.
- Grade honesty over grade optimism — the steward audits ≥25% of every batch and RECOUNTS from committed files; your returned histogram is ADVISORY (D-2c).
- Competing crosswalk rows → §7.2 dominant loop wins; note the alternative.
- Return: grade histogram, candidate counts, 3 hardest kits one-line why, under 300 words.
