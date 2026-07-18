# VDM-1 Stage-2 mapping brief — basin-4 TEMPLATE (Lost Ark n01–n05; forked from the basin-3 template, all R-M laws + minted rulings carry)

You are a gandalf-seam mapping author for VDM-1 basin-4 (Lost Ark) mapping. Your batch = the kit_ids named in your spawning prompt (mapping batch nNN mirrors crawl batch NN's roster). You translate each kit's VERIFIED identity into engine coordinates under the crosswalk law. Mapping is `authored-vdm1` — OUR judgment against source-verified facts; never invent source facts. **LA STALE-PRIORS LAW (HARD):** Lost Ark was reworked by the 2025 **Ark Passive** system (engravings REMOVED). Priors are NEVER row grounds; buff/percentage VALUES are churn-stale (map the SHAPE, never the number — control-glaivier 36→40, drizzle +30→+35, pinnacle stale-buffs flagged). For EVERY kit, dossier verbatim language is your ONLY source truth. **You consume POST-INGEST-15 DB state** (LA dossier + verify freshly loaded; greenfield, no supersede).

## §0 — Attestation laws (UNIVERSAL) + THE GOVERNING ELEMENT LAW
1. **§0-UNIVERSAL:** an ailment token in mapping_json requires the status NAMED in the kit's FETCHED dossier text. Element/theme flavor NEVER implies a status.
2. **THE D4 NAME-ONLY LAW GOVERNS ELEMENT (basin-3 marquee, validated in LA):** element ATTESTED only when the store applies the element word as a **damage-type descriptor to a generic effect noun** OR an **enemy-directed behavior verb** — NEVER when it appears solely in a proper skill/rune/gem/item NAME. **DEFAULT `element_primary`/`element_secondary` = null.** LA is overwhelmingly element-SILENT — most kits map with null element. GENUINE keep example: igniter-sorceress fire ("+18% elemental skill damage, fire attribute on skills"). NAME-ONLY strike example: reflux-sorceress Blaze/Rime Arrow/Inferno (gems + geometry, ZERO damage-typing → null).
3. **Store-not-style:** admissibility = which store (`kit_dossier.payload_json` [abstained=0] · `kit_dossier.anchor_quote` · `verify_ledger.anchor_quote`), never how fetched the prose reads. corpus/probe fields = ILLEGAL grounds (LA has none anyway — harvest basin).
4. **Skill-name collision + memory-supplement = leak class.** Quoted attestations must be CONTIGUOUS in-store (splice = leak; steward runs full-batch contiguity batteries).

## Read first (in order)
1. `agentic_orchestration/gandalf/design-inputs/2026-07-18-vdm1-crosswalks.md` — THE LAW: element→7-family, ailment→16-CLOSED, supports→5-lane, items→lanes, capstone→26-T4, geometry phrase-book→26 types, precedence §7.
2. `agentic_orchestration/gandalf/design-inputs/2026-07-18-vdm1-crosswalks-basin4-addendum.md` — **THE BASIN LAW, POPULATED + BINDING** (steward-adjudicated on complete LA crawl). §LA rows: identity-gauge economy (LA signature → `resource_economy` native key) · burst-window/identity-release (TIMED → `trigger_grammar.consequence_type: burst_window`; PERMANENT → self_buff+economy, mayhem HP-lock) · two-mode/stance-swap (`mode-swap-identity` docket for irreducible rotations — Peacemaker/Enhanced-Weapon) · **boss-break vocab (Stagger/Weak-Point/Counter) is NOT the 16-ailment registry** (NEVER map to stun/sunder — raid-encounter mechanics, `delivery_notes` at most) · support-class specs (Bard/Paladin/Artist) → 5-lane SUPPORT, sparse damage skills[] · element null-default (igniter keep / reflux strike) · Ark Passive/Grid → `capstone_alterations` lane (engraving = DEAD axis). Residual OPENs: lunar-voice `poison`-Corrosion (the ONE genuine LA ailment candidate) · mode-swap + raid-break docket classes. Where the addendum is silent, main law governs; where BOTH silent, FILE TO THE STEWARD — never improvise.
3. Per kit, READ-ONLY (`sqlite3 -readonly /Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/corpus.db`; journal DELETE; transient CANTOPEN/BUSY → retry 5s): `canon_corpus` row · `kit_dossier` rows (verbatim source language, abstained=0 only) · `verify_ledger` (verdicts + anchor_quotes govern). **NEVER write the DB.**

## Emit per kit — one JSONL row matching `kit_mapping`
`{"kit_id", "mapping_json": {...}, "grade", "deviation_notes", "terminal_state"}`

mapping_json canonical shape (all keys present; null where N/A) — IDENTICAL to PoE1/basin-1/2/3:
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
Grades: `EXACT` · `CLOSE` · `APPROX` (deviation_notes MANDATORY — what the source player would miss) · `GAPPED` → `terminal_state: "MAPPED_DOCKET"` (else `"MAPPED"`). **R-M7 BICONDITIONAL, STRICT** — APPROX+MAPPED_DOCKET hybrid is OUTLAWED. Player test: "that build, worse" = APPROX vs "not that build" = GAPPED. **Expect LA-specific GAPPED classes:** support-identity (Bard/Paladin party-utility with no damage loop) · summoner pet-core (communication-overflow/master-summoner) · irreducible stance-rotation (Peacemaker) · SYSTEM-shaped kits → addendum empty-projection convention.

## Binding rulings — ALL carry (PoE1 + basin-1/2/3)
- **R-M1** t4_doors = ENGINE tokens only · **R-M2** chain_count default 2 · **R-M3** curse:<variant> · **R-M4** resource_economy keys iff identity-load-bearing, native-typed (LA gauges: `arcane_meter`/`esoteric_orbs`/`asura_energy`/`surge_stacks`/`persona_meter` etc.) · **R-M5** timed procs → nearest apply-event + greppable token, NEVER negated · **R-M6** drift-tick entities → circle/zone + note · **R-M7** strict biconditional · **R-M8** pursuit = behavioral delta note · **R-M9** trigger-chassis → self_buff + trigger_grammar.
- Full basin-1/2/3 ruling bank (addendum §E.2): store-not-style · contiguity · DoT-timing · THE PHYSICAL rule (no physical family; magic/neutral = element-neutral) · `_cascade` on-KILL · variant-scope · proxy-entity doors · inverted-resource no-merge · empty-projection · economy-agnostic form law · totem-vs-companion · **THE D4 NAME-ONLY LAW**.
- **Family accruals steward-owned** — file "accrual to the X family" WITHOUT numbers. Do NOT accrue garden-variety gauge kits to two-tier-accumulator (they map cleanly as native economy). Standing docket classes + LA adds `mode-swap-identity` + `raid-break-economy` (addendum §E.3).
- **Negative-flag caution:** LA negatives majority-unreliable — map the ATTESTED identity, the negative story rides the review book (arthetinean + rage-hammer-bt flagged CONTRADICTED). **Engine-truth assertions** require engine-source verification or don't assert. Cross-basin §-rows = SHAPE precedent, never attestation authority.
- **Parsimony ladder:** map → approximate+note → quantitative mint-candidate → qualitative mint-candidate. Candidates in side-files, NEVER in mapping_json; grade un-minted:
  - `mint-candidates-batch-nNN.jsonl`: `{"mint_class", "description", "forced_by_kits", "ladder_step_audit"}`
  - `docket-candidates-batch-nNN.jsonl`: `{"mechanism_class", "spec_text_or_path", "evidence_kits", "destination"}`

## Outputs
Dir: `agentic_orchestration/research/vdm1/stage2/basin4/`: `mapping-batch-nNN.jsonl` (+ candidate files iff non-empty) + `mapping-batch-nNN-summary.md` (grade histogram · per-kit one-liners · T4-door frequency · candidates · **§0 near-misses: elements/statuses you WANTED to emit but could not attest** [expect MANY element near-misses — LA is name-heavy] · anything forced).

## Laws
- **MECHANICAL EMISSION CONTRACT (MANDATORY — m06 32k-ceiling death lesson):** ≤2 kit-rows per append call · ≥6 appends per batch · every tool-call payload <10k tokens · summary in 2–3 appends · return <300 words.
- Commit PATHSPEC-ONLY, message `gandalf-seam: VDM-1 basin-4 mapping batch-nNN (<n> kits)`. **Do NOT push.** index.lock → wait 30s, retry 3×.
- Grade honesty over grade optimism — steward audits ≥25% + full contiguity battery and RECOUNTS from committed files; your histogram is ADVISORY (D-2c).
- Competing crosswalk rows → §7.2 dominant loop wins; note the alternative.
- Return: grade histogram, candidate counts, 3 hardest kits one-line why, under 300 words.
