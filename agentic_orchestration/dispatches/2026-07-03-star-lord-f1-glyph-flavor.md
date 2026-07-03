# Dispatch — 2026-07-03 — star-lord — F1 envelope bridge + identity_glyph stamp + shortlist flavor

**From:** knight-rider
**To:** star-lord
**Approved by:** Matt, 2026-07-03 (this session — carve-outs 2 "FLAVOR SHORTLIST-FIRST" + 3 "F1 envelope bridge + identity_glyph stamp", both ruling-independent, fire now)
**Estimated effort:** Beat A ~1-2h (bridge + stamp, ~10s regen); Beat B ~2-4h (LLM flavor of 35 kits, resumable). Detach Beat B if long.
**Acceptance:** Beat A — the 19 F1 envelope fields populate from the char-dict/catalog sources per the findings spec, `identity_glyph` stamped on all 700, round-trip smoke passes, MIGRATION written. Beat B — the 35 shortlist finalists carry name/flavor_text/title_completion; the other 665 stay None.

## Context

Two ruling-independent post-run beats over the W3 batch-1 bundle, both sequenced by KR after W4 close (glyph spec §6 explicitly places these as post-run, pre-demo-bundle beats owned by star-lord). They share the **bundle-assembly join** — do them in one session, Beat A first, because both write at the same join and flavor keys off bundle membership (glyph spec §6).

- **Beat A (glyph spec §6 + findings F1):** the bundle's kit records carry full substance but a hollow envelope — 19 of 31 envelope fields are None on all 700 kits because `to_character_dict()` emits under the W5R vocabulary and `build_kit_record()` reads the cycle13-exporter vocabulary. Same defect class as the v1.90 `bc_target_cell` bridge, times nineteen. Fix = extend the proven v1.90 bridge in the Step-4 assembler loop; `--recover-from-canonical` regen ~10s, **no gauntlet re-run**. Then stamp `identity_glyph` (glyph spec §4 derivation, pure function of `bc_target_cell` + skill loading). **Unblocks curation tooling + the element-tint pip.**
- **Beat B (Matt's shortlist-first flavor ruling):** flavor ONLY the 35 curated finalists KR fanned — not all 700. $0 spent so far; per-item resumable.

## Required reading before starting
- Glyph spec (the law): `canonical/reap-die-rise-engine/scouting-glyph-coordinate-mapping-spec-2026-07-03.md` — §2 (inputs, v1.1 vocabulary), §4 (identity-glyph derivation, 5 rules first-match-wins), §6 (stamp point + F1 prerequisite).
- Findings note (the F1 bridge table): `agentic_orchestration/gandalf/notes/2026-07-03-glyph-s5-pre-run-findings.md` — F1 (19-field bridge map), F2 (role_orientation is PHANTOM — do NOT bridge it; see below).
- Finalist list (Beat B scope): `agentic_orchestration/w3-batch1-flavor-finalists-2026-07-03.md` — the 35 kit ids.
- v1.90 bridge precedent: engine `2839caf` (the `bc_target_cell` bridge you extend).

## Beat A — F1 bridge + identity_glyph stamp

### Math/decisions before code (Discipline #1)
The bridge is a vocabulary remap, not new computation. Document the field→source map before editing. From findings F1:

| Bundle field | Bridge from | Note |
|---|---|---|
| `dominant_element` | char_dict `element` | **glyph-load-bearing** — the element-tint pip; do this one right |
| `energy_type` | char_dict `resource_model` | **adopt doc-48 vocabulary** (mana/rage/combo/stamina/charge-stack); the cycle13 enum is stale — glyph §2 already updated to match |
| `archetype_tag` | catalog `archetype_name` (encounter) | NAME channel only — never a glyph input |
| `range_profile` | `bc_tuple.range` | legacy-compat only; glyph v1.1 reads bc coordinates directly |
| remaining ~15 | **your triage** | which are demo-bundle-load-bearing vs cycle13-legacy is your call; document per field |

**HARD CONSTRAINTS:**
- `role_orientation` is **PHANTOM** (findings F2): `KitCandidate` has no such field; the router hard-codes `"damage"` for all 18 archetypes (`season_generation_pipeline.py:1557`). **Do NOT synthesize or bridge it.** Leave it None or drop it; document which. Bridging a phantom axis is exactly the F2 framing-audit failure (Disc #23). If you populate it, say from what live varying coordinate — you won't find one.
- `name` / `flavor_text` / `title_completion` stay **None** in Beat A **BY RULING** (flavor is parked-resumable; Beat B fills only the 35 finalists).
- `identity_glyph`: stamp per glyph spec §4 (rule 1 SUMMONER→0 by ruling; 2 CONTROLLER→0; 3 WARDEN→0; 4 melee→BRUISER; 5 mid/ranged→GLASS CANNON). Batch-1 result must be 300 BRUISER / 400 GLASS CANNON. Deterministic from `bc_target_cell` — needs no bridge itself; the element-tint pip needs `dominant_element` (above).

### Cross-seam contract change? (Principle 6 gate — YES)
This dispatch **adds** the `identity_glyph` field and **populates** 19 previously-None envelope fields on the bundle consumed by drax (demo UI, loadout app, grimoire) and by curation tooling. This is a consumer-contract change → **MIGRATION.md required** (ADR-004), and the Acceptance MUST include a round-trip smoke:

**Round-trip smoke:** regenerate the bundle via `--recover-from-canonical` on a production-path fixture; assert on the bundle output that (a) `dominant_element` is non-None and ∈ the canonical element set on all 700, (b) `energy_type` uses doc-48 vocabulary, (c) `identity_glyph` ∈ {BRUISER, GLASS CANNON} on all 700 with the 300/400 split, (d) `name`/`flavor_text`/`title_completion` remain None (Beat A must not fabricate flavor), (e) `role_orientation` not fabricated. Field-presence check at the assembler→consumer boundary.

## Beat B — flavor the 35 finalists only

- Scope: exactly the 35 kit ids in `w3-batch1-flavor-finalists-2026-07-03.md`. Write `name`, `flavor_text`, `title_completion` for those; leave all other 665 None.
- Per-item resumable (Matt: "$0 spent so far; per-item resumable per §7"). Detach if long; checkpoint so a kill doesn't lose completed items.
- **Attribution discipline (#11):** flavor the kit's ACTUAL content — BC cell (melee-BRUISER vs ranged-GLASS-CANNON), element signature (the finalist labels give physical+X / fire+X), tempo/amplitude. Do NOT promise mechanics the kit lacks. Per the finalist caveats: GLASS CANNON fragility is F1-unverified (uniform damage_multiplier ~1.01) — flavor the *ranged spike*, not fragility. Seat-7 kits are physical-ranged martial skirmishers, NOT casters — no caster-fantasy flavor (the whole batch is martial resource-feel).
- Beat B is NOT a cross-seam contract change (fills existing None string fields) → **Round-trip: not applicable for Beat B — no new/renamed field; the Beat-A round-trip covers the envelope.** State this in the MIGRATION note.

## Scope
- [ ] Beat A: 19 envelope fields bridged per F1 map (with per-field triage documented); `role_orientation` NOT fabricated.
- [ ] Beat A: `identity_glyph` stamped on all 700 (300 BRUISER / 400 GLASS CANNON).
- [ ] Beat A: round-trip smoke passes (5 asserts above).
- [ ] Beat A: MIGRATION.md prepended (`export/MIGRATION.md`) — new field `identity_glyph` + 19 populated fields; consumer action for drax (reload bundle at same path; new fields available; element pip render-ready).
- [ ] Beat B: 35 finalists flavored; 665 remain None; resumable checkpointing.
- [ ] AGENT_STATE.md updated (export/output seam).
- [ ] Tag: `star-lord/v-demo-run-f1-glyph-<n>` (Beat A) and, if flavor is a separate commit, `star-lord/v-demo-run-flavor-shortlist-<n>` (Beat B). Seam-prefixed — Matt drops the prefix on milestone.

## Acceptance criteria
- [ ] `dominant_element` non-None + canonical on all 700; `energy_type` doc-48 vocabulary; `identity_glyph` present with 300/400 split.
- [ ] `role_orientation` not fabricated (None or dropped, documented).
- [ ] name/flavor_text/title_completion: None on the 665, populated on exactly the 35.
- [ ] Round-trip smoke: bundle regenerated via `--recover-from-canonical`; 5 field-presence asserts at assembler→consumer boundary pass. (Beat B: not applicable — no new field.)
- [ ] MIGRATION.md written; drax consumer action stated.

## Out of scope (explicit non-goals)
- Flavoring beyond the 35 finalists (the other 665 stay None — Matt's shortlist-first ruling).
- Any generation/simulation change; any gauntlet re-run (bridge is a ~10s regen read-from-canonical).
- Building the summoner/caster gen-path (downstream of Matt's ruling, different dispatch).
- Temperature-glyph computation (hand-tagged at G7a curation, launch-track — glyph spec §6/out-of-scope).
- Glyph ART / silhouette shapes (drax + galadriel — glyph spec §7).
- Populating `role_orientation` (phantom — findings F2).

## Open questions for star-lord to resolve
- Of the ~15 remaining F1 fields, which are demo-bundle-load-bearing vs cycle13-legacy? Document the triage per field in the MIGRATION note (findings F1 leaves this explicitly to you).
- `seasonal_dominant_element` vs `dominant_element` — bridge both or is one derivable from floor_manifest? Document.
- Does the demo/loadout consumer read `identity_glyph` directly or re-derive? (Spec §6: stamped field governs; consumers may re-derive for display fallback.) Note the contract for drax in MIGRATION.

## References
- Glyph spec v1.1: `canonical/reap-die-rise-engine/scouting-glyph-coordinate-mapping-spec-2026-07-03.md` §2/§4/§6
- Findings F1/F2: `agentic_orchestration/gandalf/notes/2026-07-03-glyph-s5-pre-run-findings.md`
- Finalist list: `agentic_orchestration/w3-batch1-flavor-finalists-2026-07-03.md`
- v1.90 bridge precedent: engine `2839caf`; source seam `season_generation_pipeline.py:412` (`to_character_dict`), `one_realm_bundle_assembler.py:283` (`build_kit_record` passthrough), `:1557` (role_orientation hard-code)
- ADR-004 (cross-seam MIGRATION): `agentic_orchestration/GOVERNANCE.md`
- Disciplines #1 (math-before-code), #11 (attribution), #23 (framing-audit) — engineering-disciplines.md

## Completion record

**Completed by:** star-lord, 2026-07-03
**Engine commit:** `62abdc7`
**Tag:** `star-lord/v-demo-run-f1-glyph-1`

### Beat A — COMPLETE

All scope items checked:

- [x] Beat A: 19 envelope fields triaged; 6 bridged (dominant_element, energy_type, archetype_tag, range_profile, engine_version, identity_glyph[new]); role_orientation explicitly NOT bridged (PHANTOM — None); 11 cycle13-legacy fields left None (documented in MIGRATION.md § v2.00 triage table). Name/flavor_text/title_completion None BY RULING.
- [x] Beat A: identity_glyph stamped on all 700 — BRUISER=300, GLASS CANNON=400.
- [x] Beat A: round-trip smoke — all 5 asserts PASS (dominant_element canonical ×700, energy_type doc-48 ×700, glyph 300/400, flavor None ×700, role_orientation None ×700).
- [x] Beat A: MIGRATION.md § v2.00 prepended. Per-field triage documented. identity_glyph read-vs-rederive contract stated. Consumer action for drax noted.
- [x] AGENT_STATE.md updated.
- [x] Tag: `star-lord/v-demo-run-f1-glyph-1` created.

**Open questions resolved:**
- `seasonal_dominant_element` vs `dominant_element`: `dominant_element` bridged from `element`. `seasonal_dominant_element` NOT bridged — no per-kit seasonal assignment in KitCandidate; bundle `floor_manifest` has per-floor element but it is a different concept. Documented in MIGRATION.md triage table.
- `identity_glyph` read-vs-rederive: stamped field governs per spec §6; consumers may re-derive from `bc_target_cell` as display fallback (deterministic). Drax consumer action in MIGRATION.md.

### Beat B — COMPLETE (resumed 2026-07-03)

**Engine commit:** (Beat B commit, this session)
**Tag:** `star-lord/v-demo-run-flavor-shortlist-1`

All scope items checked:

- [x] Beat B: 35 finalists flavored (name / flavor_text / title_completion). 665 remain None.
- [x] Beat B: Script `export/w3_batch1_flavor_writer.py` — per-item resumable, key from env only. Never written to any file.
- [x] Beat B: Post-write validation — all 8 asserts PASS (35/35 populated, 665 None, 35 unique names, Beat-A envelope asserts all hold).
- [x] Beat B: Guardrail scan PASS — no caster-fantasy, no fragility claims, no "glass cannon" in flavor text (2 fixed before commit). Names 2-4 words, unique, diegetic.
- [x] Beat B: NOT a cross-seam contract change (fills existing None string fields; no new/renamed field). MIGRATION.md Beat B note already present.
- [x] AGENT_STATE.md updated.
- [x] Dispatch completion record appended (this section).
- [x] Key appears in no git-tracked content (grep clean before commit).

**Cost:** $0.1289 (28,684 input / 2,857 output tokens, claude-sonnet-4-6). 0 retries.

**5 sample entries for Matt (spanning all glyph types and one seat-7):**
- `S1_endgame_bc_melee_low_spiky_str_none_s39` (BRUISER, physical+shadow): *Void Marrow Breaker* — "Rage pools slow and deliberate — each blow a shadow-laced concussion that waits for bone to answer. One opening. One burst. The fight ends in the dark."
- `S1_endgame_bc_melee_medium_variable_str_none_s30` (BRUISER, physical+shadow): *Shadowmass Ravager* — "Rage pools between strikes, tipping the scale from sustained grind to sudden collapse — physical force and shadow void married in close iron. Variable amplitude means the threat is never fixed."
- `S1_endgame_bc_mid_high_flat_dex_none_s21` (GLASS CANNON mid-range, fire+lightning): *Scorchbolt Fusillade* — "Feeds rage into a sustained barrage of fire-traced lightning — mid-range, high-tempo, output steady as a drum. No spike, no lull; just the flat burn of a fighter who never stops pulling the trigger."
- `S1_endgame_bc_ranged_low_spiky_dex_none_s83` (GLASS CANNON ranged, fire+wind): *Sirocco Detonator* — "Builds combo through measured fire, then releases in a single scorching gust that hits like a hammer from twenty meters out. Wind feeds the ignition; patience feeds the shot."
- `S1_endgame_bc_ranged_low_spiky_str_none_s27` (GLASS CANNON seat-7, physical+lightning): *Stormjavelin Detonator* — "Charges combos between throws, then unloads in a single arc of muscle and shock — javelin meets lightning at the apex of a low-tempo build. The burst does not announce itself; it simply arrives."
</content>
