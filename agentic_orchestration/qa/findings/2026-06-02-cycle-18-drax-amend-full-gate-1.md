# Finding — 2026-06-02 — cycle-18-drax-amend-full — Gate-1 pre-fire review

**Reviewer:** jack-ryan
**Mode:** DESIGN-MODE (Gate-1 pre-fire critique-pair)
**Severity:** PASS-with-INFO (no BLOCKs; 2 WARNs; 5 INFOs)
**Target:** cycle-18 dispatches before Phase 1 fire
**Developer(s) receiving this review:** gandalf-as-subagent (Issue 4); star-lord + rocket (Issue 5A); drax (Phase 2)
**Principles applied:** 1, 2, 3, 4, 6
**Disciplines cited:** #53, #56, #57, #59

---

## Overall verdict

**PASS-with-INFO**

Phase 1 fire clearance: **YES** — with WARN-class notes for gandalf and star-lord to read before executing. No BLOCKs found. The dispatch package is structurally sound, well-scoped, and internally coherent. Two WARNs are design-quality concerns that do not block execution but must be addressed during the respective seam's execution (not deferred to Gate-2).

---

## Per-dispatch verdicts

### Wave-open + wave-state

**Verdict: INFO**

- Phase 1 parallelism is well-structured: Issue 4 (gandalf) + Issue 5A (star-lord/rocket) + Gate-1 (jack-ryan) touch entirely different seams and artifacts. No collision risk.
- Phase 2 dependency on Phase 1 outputs is correctly stated: drax consumes renamed kit JSONs from Issue 4 AND `faction_assignments.json` from Issue 5A. Both must be PASS before Phase 2 fires.
- LOCK O canonical amendment 2026-06-02 is well-formed. Captures four discrete constraints: (1) repoint existing pages / no parallel pages; (2) primary element = flag prominence; (3) flavor word = secondary annotation; (4) kit identity names exclude Q18 words and generic archetype labels. All four are enforceable and traceable to QDX-7 surfaced issues.
- Escape clause covers 5 items. Item 4 (cost overrun >2x) is appropriate. No gaps detected.
- **INFO:** Wave-close criterion references "Phase 4 KR fix-forward record + Vercel preview URL + Matt signal." The "Matt signal" here is strategic acknowledgment (not a BLOCK-class escalation). This is correct and consistent with Matt's "no further Matt-touch required before acceptance verification" pattern from QDX chain — but worth noting that Matt's explicit preview review IS load-bearing for Phase 4 close (not just a formality).

---

### Issue 4 dispatch — gandalf-as-subagent LLM rename

**Verdict: WARN**

#### WARN-1 (must address during execution): `gale` is in the Q18 wind allow-list; `kit_wind_000006` ("Galewright") uses it

The Issue 4 dispatch's LLM avoid-list correctly lists `gale` under wind Q18 words. The pre-rename identity for `kit_wind_000006` is "Galewright of the Scattered Pale." "Galewright" contains `gale`, which is a Q18 wind flavor word. This rename pass WILL produce a new name for this kit — the avoid-list will fire correctly if the LLM is consistent. However, the dispatch's top-5 sample-inspection list includes `kit_wind_000006` (§ 4.3), and the gandalf curation artifact treats "Galewright" as a high-quality pick (Rank 3 in `2026-06-02-qdx-5-top-5-character-curation.md`). After renaming, "Galewright" will be REPLACED by a new name that does not use `gale`. Gandalf should be prepared for the top-5 featured-character identity for `kit_wind_000006` to change significantly from what the curation artifact describes.

This is not a BLOCK — the rename is exactly what Issue 4 is for, and the Q18 avoid-list is functioning correctly. But the downstream drax dispatch (Issue 3 featured characters) references `kit_wind_000006` as the wind representative. Gandalf must flag the post-rename identity for this kit prominently in the Issue 4 completion record so drax does not render stale identity in the Featured Characters section.

- Cite: Discipline #13a (implementation-vs-intent drift); the curation artifact was authored against pre-rename identities; drax Issue 3 consumes post-rename identities. The gap is expected and by design — but must be surfaced explicitly in the completion record.
- Action: gandalf's Issue 4 completion record must include the NEW `emergent_kit_concept` for `kit_wind_000006` with a note that the prior "Galewright" identity is superseded.

#### WARN-2 (must address during execution): top-1 `kit_shadow_000007` uses "Penumbra" — an etymological-family AVOID term

The pre-rename identity for `kit_shadow_000007` is "Penumbra Caster of Dusk Meridian." The Issue 4 dispatch explicitly lists `umbra`, `umbral`, `penumbra` as etymological-family AVOID terms (§ 3 Hard Rule 1 final paragraph). This rename pass will correctly produce a new name for the top-1 kit. The gandalf curation artifact (`2026-06-02-qdx-5-top-5-character-curation.md`) explicitly cites "Penumbra" as the reason it selected this kit as top-1: "Penumbra (Latin: partial shadow; astronomical eclipse vocabulary) is sophisticated + sui generis vocabulary."

The new rename will strip "Penumbra." The new name may or may not preserve the evocative quality that made this kit the top-1 pick. This is the highest-stakes rename in the batch.

- This is not a BLOCK — it is the intended behavior. Matt authorized "Remove flavor element names from prefixes" verbatim.
- Action: gandalf must prioritize this kit's rename quality. If the LLM output for `kit_shadow_000007` is flat or loses the sui-generis register, this warrants a manual re-fire or prompt-context enrichment before accepting. The completion record must note the new identity and make an explicit quality assessment against the prior evocative register.
- Cite: LOCK L iteration discipline (1st BLOCK seam-owner re-fires within authority). If the first LLM output is quality-degraded on this specific kit, gandalf has authority to re-fire without Matt escalation.

#### INFO-1: Avoid-list completeness — "Adept" is listed in § 4.3 acceptance criteria but not in § 3 Hard Rule 2 avoid-list

The LLM prompt in § 3 lists the generic-archetype avoid words as: "Caster, Cleric, Mage, Warrior, Knight, Bearer, Fighter, Warden, Champion, Master, Adept, Apprentice." The acceptance criteria in § 4.1 criterion 6 lists: "Caster/Cleric/Mage/Warrior/Knight/Bearer/Fighter/Warden/Champion/Master/Adept" — omitting "Apprentice." This is a minor inconsistency between the prompt and the post-fire verification list.

- Action: no change to the LLM prompt required (the prompt is the more complete version). For the acceptance-criteria verification step, gandalf should check against the PROMPT's avoid-list (which includes Apprentice), not the abbreviated acceptance-criteria list.

#### INFO-2: No explicit "new generic fallback" detection in acceptance criteria

The dispatch notes in § 8 Refutation conditions: "LLM systematically falls back to a different generic word not in the avoid-list (e.g., 'Adept' if Apprentice avoided; new generic emerges → refine avoid-list)." This is a valid risk but there is no acceptance criterion that operationalizes "new generic detection." The current acceptance criteria check against the hardcoded avoid-list; they will pass even if all 37 kits are renamed to "Shadowbound" or another unlisted generic.

- This is not a BLOCK — the Refutation conditions section acknowledges this and routes it to LOCK L iteration if detected.
- Action: gandalf should do a qualitative scan of all 37 renamed identities for pattern-repetition across kits (distinct from the dedup-check which only catches exact-match). If >5 kits share a structural template (e.g., "<Element>-<Verb>er of <Place>"), that is a LOCK L iteration signal even if every individual word passes the avoid-list check.

---

### Issue 5A dispatch — star-lord + rocket faction_assignments emit

**Verdict: INFO**

#### INFO-3: Data-source path (a/b/c) decision is under-specified for Gate-2 verification

The dispatch correctly presents three options for reconstructing event_008 cluster assignments: (a) deterministic re-derivation, (b) log inspection, (c) chronicle reconstruction. The completion record template asks star-lord to document which path was used. This is correct.

However, path (a)'s determinism assumption deserves attention: the chronicle records `pm1_algorithm=GMM_K3`. GMM with K=3 is only deterministic if a fixed `random_state` was used in the original Phase 5a call. If no random_state was set, re-running GMM against the same inputs will produce DIFFERENT cluster assignments, meaning the 3 factions will have different member-kits on re-derivation.

- This is not a BLOCK — it is a technical risk that star-lord/rocket must resolve empirically.
- Action: rocket should inspect `phase5_pm1_multimodal_clustering.py` to confirm whether `random_state` is fixed before choosing path (a). If random_state is NOT fixed, path (b) or (c) is more reliable.
- Cite: Discipline #11 (empirical inspection over assumption) — do not assume GMM is deterministic; verify from the source code before selecting path (a).

#### INFO-4: Faction name sourcing — "Earthen Siege Wardens" vs wave-close record

The Issue 5A dispatch specifies faction names from the QDX-5 Wave A output: "Iron Ground Crushers / Scattered Meridian Cannons / Earthen Siege Wardens." The QDX chain wave-close record (`canonical/story/2026-06-02-qdx-chain-wave-close-record.md` § 0) confirms the same three names. Consistent. No action required — confirming alignment.

#### INFO-5: MIGRATION.md scope — generation-side MIGRATION conditional

The acceptance criteria § 5.3 criterion 10 states: "If generation-side touched (e.g., for clustering re-derivation), MIGRATION.md entry at generation/MIGRATION.md per ADR-004." This is correct as written. However, path (a) re-derivation would constitute touching the generation-side module (`phase5_pm1_multimodal_clustering.py`), triggering ADR-004 dual-MIGRATION. Star-lord should pre-decide whether to produce the generation-side MIGRATION entry even for a read-only execution against existing generation code — re-running a module is not a code change, so generation/MIGRATION.md may not be required under strict ADR-004 reading (which requires code change, not execution).

- Action: star-lord should document in the completion record: "generation-side MIGRATION.md: [required / not required] because [path (a) re-run is read-only execution / path (b)/(c) did not touch generation modules]." Prevents Gate-2 ambiguity.
- Cite: Principle 3 (cross-seam impact called out explicitly) + ADR-004.

---

### Phase 2 drax consolidated dispatch

**Verdict: INFO**

#### INFO-6 (forward note for Gate-2): Top-5 featured card identities will differ from curation artifact

The drax dispatch (§ 2 Issue 3) instructs drax to render the Featured Characters section using "Wave B identity (post-Issue-4 rename) — read from kit JSON's emergent_kit_concept field at render time; do NOT hardcode names." This is correct and the instruction prevents stale-name hardcoding. However, the dispatch also references the gandalf curation artifact for the top-5 list, which was authored against PRE-rename identities. The curation artifact entry for `kit_shadow_000007` names "Penumbra Caster of Dusk Meridian" — a name that will be replaced by Issue 4.

Drax does NOT need to do anything differently — the instruction to read from JSON at render time already handles this. This note is for Gate-2: the jack-ryan Gate-2 reviewer should NOT check whether the rendered names match the curation artifact's pre-rename identities. The correct check is that the rendered names match the post-rename JSON values.

#### Confirmation: 4-issue consolidation in single dispatch is correct

Issues 1 + 2 + 3 + 5B are all within the drax seam (`reincarnated-loadout/`). No cross-seam work required within Phase 2. Consolidation into one dispatch is appropriate per hive-mind decision-routing (drax seam-owner executes all loadout-side work in one session).

#### Confirmation: LOCK O AMENDED compliance is clear and enforceable

The 13-item acceptance criteria (§ 3.3) adds 3 LOCK O AMENDED compliance checks on top of the 10 content/UX criteria. These are specific and enforceable: no new UI component shells, no UI redesign beyond Issue 2 hierarchy fix, repoint EXISTING `/loadout`. Gate-2 can verify these from file additions/deletions in the commit.

#### Confirmation: cross-repo sync workflow is clear

Section 4 specifies the sync workflow explicitly: `engine/data/kit_space/kits/` → `loadout/public/kit-space/kits/` and `engine/data/kit_space/faction_assignments.json` → `loadout/public/kit-space/faction_assignments.json`. Chronicle already synced. No ambiguity.

---

## Cross-dispatch composition

### Phase 1 → Phase 2 dependency: CONFIRMED COHERENT

Drax Phase 2 gates on:
1. Issue 4 completion record showing renamed `emergent_kit_concept` values committed to engine
2. Issue 5A completion record showing `faction_assignments.json` at `data/kit_space/`

Both are correctly specified as prerequisites in the drax dispatch (§ 1 item 4: "Phase 1 completion records"). The dependency chain is sound.

### Discipline composition: CONFIRMED PRESERVED

- **Discipline #53** (ADDITIVE-ONLY): Issue 5A correctly specifies LOCK Q ADDITIVE-ONLY (new file only; no semantic API amendments to existing modules). Gate-2 criterion 6 explicitly checks this.
- **Discipline #56** (generator-path explicit naming): Not directly applicable to this cycle (no new engine gen fire); the generator path (ClassGenerator / Option B) was used at QDX-5 and is preserved as-is. Consistent.
- **Discipline #57** (genre-aligned distribution): Not applicable to this cycle (no distribution change; using existing 37-kit output).
- **Discipline #59** (substrate-coverage as binding quality constraint): Not applicable to this cycle (no generation work).

### Quality criteria + refutation conditions: PRESENT IN ALL DISPATCHES

All three dispatches (Issue 4, Issue 5A, Phase 2 drax) include both a "Quality criterion" section and a "Refutation conditions" list. This is consistent with the Move 1 discipline (Discipline #42 framing-audit operationalization). No gaps.

---

## Common Gate-2 catches (anticipated; for future Gate-2 reviewer)

When Gate-2 reviews land for cycle-18:

**For Issue 4 Gate-2:**
- Verify `kit_wind_000006` new identity does NOT contain `gale` (Q18 avoid-list compliance)
- Verify `kit_shadow_000007` new identity does NOT contain `penumbra`, `umbra`, or `umbral`
- Assess post-rename quality of `kit_shadow_000007` (top-1 pick; was evocative for reasons tied to "Penumbra" — new name must reach similar register)
- Check all 37 for structural-template pattern (not just exact-dedup)
- Check acceptance criteria against PROMPT avoid-list (includes Apprentice), not abbreviated criterion-6 list

**For Issue 5A Gate-2:**
- Verify GMM determinism assumption: star-lord/rocket must document random_state decision
- Verify faction name spelling exactly matches QDX-5 Wave A output
- Verify sum of kit_ids across 3 factions = 37 (no duplicates; no missing)
- Confirm generation-side MIGRATION.md scope was documented in completion record

**For Phase 2 drax Gate-2 (10-criteria verification):**
- Do NOT check rendered names against curation artifact pre-rename identities; check against post-rename JSON values
- LOCK O AMENDED: check for new component shell files specifically (violation would be a new `.tsx` or `.ts` file in `src/components/` beyond what EAA-6/7 precedent permits)
- Faction filter interaction: verify click-to-filter works on EACH of the 3 factions, not just one

---

## Phase 1 fire clearance

**YES — Phase 1 may fire.**

- Issue 4 (gandalf): CLEAR with WARN-1 and WARN-2 acknowledged. Gandalf must read both WARNs before executing.
- Issue 5A (star-lord+rocket): CLEAR with INFO-3 (GMM determinism check) and INFO-5 (MIGRATION.md scope) acknowledged.
- Phase 2 drax: NOT FIRING yet (correctly gates on Phase 1 PASS). Pre-read dispatches now; execute after Phase 1 PASS.

---

## Sign-off

**jack-ryan Gate-1 DESIGN-MODE**
**Date:** 2026-06-02
**Cycle:** cycle-18 Drax QDX-7-AMEND-FULL
**File:** `agentic_orchestration/qa/findings/2026-06-02-cycle-18-drax-amend-full-gate-1.md`

**LOCK L disposition:** 0 BLOCKs at Gate-1. LOCK L not triggered. Phase 1 specialists have authority to resolve all WARNs and INFOs within their seams without Matt escalation.

---

## References

- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/cycle-18-drax-amend-full/wave-state.md`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/dispatches/2026-06-02-cycle-18-drax-amend-full-wave-open.md`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/dispatches/2026-06-02-cycle-18-issue-4-llm-rename-all-37-kits.md`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/dispatches/2026-06-02-cycle-18-issue-5a-faction-assignments-emit.md`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/dispatches/2026-06-02-cycle-18-issues-1-2-3-5b-drax-consolidated.md`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-06-02-qdx-5-top-5-character-curation.md`
- `/Users/admin/Games/reincarnated-collaboration/canonical/story/2026-06-02-qdx-chain-wave-close-record.md`
- `/Users/admin/Games/reincarnated-collaboration/canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md` § 2.4 (wind Q18 allow-list)
- `/Users/admin/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` §§ 11, 13a, 53, 56, 57, 59
