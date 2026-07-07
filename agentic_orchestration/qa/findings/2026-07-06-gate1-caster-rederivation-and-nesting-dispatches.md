# Gate-1 Finding — 2026-07-06 — caster-bar-rederivation (step 1) + carried_gear-nesting (step 2)

**Reviewer:** jack-ryan (DESIGN-MODE, peer collaborator)
**Mode:** Gate-1 pre-dispatch, two Pattern-B dispatches
**Targets:**
- `agentic_orchestration/dispatches/2026-07-07-gamora-caster-bar-re-derivation.md`
- `agentic_orchestration/dispatches/2026-07-07-rocket-gamora-carried-gear-nesting-unification.md`
**Source read:** gandalf finding §8 CORRECTION (`9fb3467`); gamora ledger §7/§2; engine grep of `carried_gear` producers/readers + `combatant.py:874-903` + `season_generation_pipeline.py:465-475`.

---

## Verdict

- **Dispatch 1 (bar re-derivation):** RATIFY-WITH-CONDITIONS (2 conditions, both foldable into text).
- **Dispatch 2 (nesting unification):** RATIFY-WITH-CONDITIONS (1 correction + 1 condition; the correction makes the fix *more* correct).

Neither is a BLOCK. Both are methodologically sound. Sequencing (parallel/independent) is CONFIRMED correct.

---

## Dispatch 1 — pre-registration integrity: PASSES

- The validity check is genuinely pre-registered and back-fit-proof: Q1 is a binary YES/NO with the branch *consequences named in advance*, and the NO branch is explicitly labeled "a finding, not a failure" — no goalpost to move. Sound.
- The NOT-F-d framing is airtight AS WRITTEN. The distinction "C2 principle stands; only its instrument is re-matched" is load-bearing and correctly carried in three places (context, out-of-scope, acceptance). The step measures MARTIALS on the matched instrument to *establish* a target, not casters against a lowered one — structurally cannot be bar-lowering because no bar edit is in scope and the caster is not even in the fight. Good.
- The distribution-not-floor requirement (finding §7.2) is correctly wired via Q2 + acceptance criterion "distributions (min/median/spread/max), not just a floor," and the re-pilot GO criterion is pre-named as yield-rate comparability. Prevents floor-scraping. Good.
- The §7.1 two-shell-structure fence (never whole-encounter median) is present and correct in both scope and out-of-scope.

### Condition 1a (WARN → fold in): pin the clearing definition as a step-1 OUTPUT, not just an open question.
Right now the "exact clearing definition to freeze" sits in *Open questions* (line 67) AND acceptance requires "same clearing definition" (line 7). That is a soft loop: step 3 inherits the definition step 1 *chooses*, but nothing forces step 1 to emit it as a frozen artifact. Add an acceptance checkbox: **"The clearing/kill definition (fraction-of-wall vs absolute-kills-in-window) is written into the completion record as a frozen string; step-3 re-pilot MUST cite it verbatim."** This closes the metrology hole you flagged — otherwise step 3 can silently re-pick and reintroduce the exact units-mismatch this whole step exists to kill.

### Condition 1b (INFO → fold in): pin the Q1 metric normalization explicitly.
gamora's own §7 shows the failure was a mob-count normalization mismatch (bar of 9.90 on an 8-mob cap). Q1 as written ("can martials reach 9.90 on THIS 8-mob wall") is correct, but add one clause: **"report the raw mobs-killed AND any normalization applied; if the answer requires a metric other than absolute-kills-in-window to be comparable to the original 9.90 derivation, name that metric and flag the mismatch explicitly."** This prevents an accidental YES produced by a silent re-normalization — the subtle way a NO could get dressed as a YES.

Discipline check, Dispatch 1: #1 (math-before-code) satisfied — the pre-fire documentation of both instruments is required before the fire. #11 (attribution) required and cited. #19 (detached) correctly conditional on run time. #12 (semantic-shift) — a bar re-derivation is measurement, not a semantic shift itself; it FEEDS step 3 which IS the re-pilot. The chain is intact: no constant moves here, so no re-pilot is triggered BY this step; step 3 is the re-pilot and is correctly held separate. Confirmed.

---

## Dispatch 2 — one factual correction (strengthens the fix) + one condition

### Correction 2a (fold into Context + Scope): the reader is NOT purely top-level; it is a three-key or-chain, and the nested decl shape misses it for a DIFFERENT reason than the dispatch states.

The dispatch says (line 14) "combatant reads `spell_damage_modifier` at top level and finds nothing." Verified against `combatant.py:893-901`, the reader is:
```
_weapon_data = _carried.get("main_hand") or _carried.get("weapon") or _carried.get("main_weapon")
...
_weapon_spell_mod = float(_weapon_data.get("spell_damage_modifier", 0.0))
```
So the reader first resolves a **weapon-slot dict** (via a 3-key alias chain), THEN reads `spell_damage_modifier` off THAT dict. The decl path (`season_generation_pipeline.py:472`) writes `gear_representative["main_weapon"]["substrate_binding"] = <binding>`. That means:
1. `_carried.get("main_weapon")` on the decl shape returns `{"substrate_binding": {...}}` — a dict whose `spell_damage_modifier` key does NOT exist at that level (it's one deeper, under `substrate_binding`). Reader gets 0.0. **Bug confirmed, exactly as flagged.**
2. BUT the decl `gear_representative` is keyed by `GearSlot.MAIN_WEAPON.value == "main_weapon"` — the SAME alias the reader's or-chain resolves. So the divergence is purely the extra `substrate_binding` nesting LEVEL, not a key-name mismatch. The pilot builder (`:1604`) writes `{"main_weapon": <binding>}` (binding directly, no `substrate_binding` wrapper), which the reader consumes correctly.

Net: "fix the producer, not the reader" is the RIGHT call, and it's even cleaner than the dispatch implies — the fix is to make `:472/:475` write the binding **directly** under the slot (matching `:1604`), dropping the `substrate_binding` sub-key wrapper. **Fold this precision into the canonical-shape decision** so rocket unifies on "binding-directly-under-slot," not on some new third shape. Also correct the Context bullet: it's a nesting-LEVEL mismatch (extra `substrate_binding` wrapper), not a top-level-key-absence.

### Correction 2b (WARN → this is the real scope gap): there is a SECOND reader that consumes the nested shape, and it must be reconciled or it breaks.

`season_generation_pipeline.py:1885-1890` and `:2308-2322` READ the nested shape back:
```
main_weapon_rep.get("substrate_binding", {})   # :1890, :2311
```
This is the reconstruction path (`_reconstruct_kit_from_...` and the substrate-field validator at `:2308`). It expects the `substrate_binding` wrapper that `:472` writes. **If rocket un-nests `:472` to match the pilot builder, these two readers break** — they'll look for `["substrate_binding"]` and find the binding fields sitting directly on the slot instead. Dispatch 2's open question ("other producers/consumers beyond the two known sites — grep both") gestures at this, but given the inversion finding (casters depend entirely on this pool), a silent break in the reconstruction/validation path is exactly the class of regression the round-trip smoke might NOT catch if the smoke only exercises the decl→combatant leg.

**Condition:** make the "grep all producers AND consumers" step a REQUIRED scope item (not an open question), and add to acceptance: **"the gear_representative reconstruction reader (`:1885-1890`) and the substrate-field validator (`:2308-2322`) are reconciled to the chosen canonical shape; a round-trip through the reconstruction path is part of the smoke."** Otherwise the unification fixes one consumer and breaks two.

### Principle-6 round-trip clause: SUFFICIENT for the decl→combatant leg, INSUFFICIENT as specified.
The specified smoke (decl-built reads non-zero + pilot path unchanged) correctly covers the two legs the dispatch names. Given 2b, extend it to cover the reconstruction/validator leg. With that extension the round-trip is sufficient. MIGRATION.md is correctly REQUIRED (ADR-004) — `carried_gear` / `gear_representative.main_weapon.substrate_binding` is the generation→sim boundary shape, and there is ALREADY a MIGRATION contract describing the `substrate_binding` sub-key (`generation/MIGRATION.md:287`, `simulation/MIGRATION.md:4126-4130`); those entries MUST be updated in lockstep or the MIGRATION lies. Add: **"update the existing MIGRATION `substrate_binding` contract entries, don't just append a new one."**

Discipline check, Dispatch 2: #1 satisfied (canonical-shape decision + exhaustive producer/consumer enumeration required before edit — 2b makes this teeth-bearing). #11 required/cited. #12 (semantic-shift) — this changes a cross-seam dict SHAPE, which is a semantic shift at the boundary; the round-trip smoke + MIGRATION are the correct discipline response and no re-pilot is triggered because the pilot VALUE is unchanged (0.0→non-zero only on the decl path, which no pilot uses). Confirmed. Cross-seam → correctly ESCALATE-class (Matt-approved sequencing already covers it) with jack-ryan Gate-2 on the tagged output.

---

## Sequencing — CONFIRMED independent/parallel

gamora's ledger §1 + the engine read confirm: the pilot/gauntlet martial kits get their physical pool from `gear_set` ability_modifiers (`damage_resolver.py:758-760`), which is `{}` in the pilot — NOT from `carried_gear`/`substrate_weapon_binding`. So the nesting bug (which only affects the *spell* pool on the *decl* path) cannot touch the martial bar re-derivation in step 1. The martial kits in step 1 flow through the un-nested pilot builder (`:1604`), which is already correct. **No hidden dependency. Parallel is safe.** The one thing to keep clean: step 1 must NOT be run through the decl path (it isn't — it re-runs batch-1 martial kits on the existing Leg-B shells via the pilot/gauntlet builder). Dispatch 1 line 35 already pins the `from_player_class` → bounded-pool production path. Good.

---

## Summary of conditions to fold in before fire

**Dispatch 1:**
1. Add acceptance checkbox: clearing/kill definition frozen as a string in the completion record; step-3 cites it verbatim.
2. Add to Q1: report raw mobs-killed + any normalization; flag any metric change needed for comparability to the original 9.90.

**Dispatch 2:**
3. Correct Context: nesting-LEVEL mismatch (extra `substrate_binding` wrapper at `:472`), not top-level-key-absence; canonical shape = binding directly under slot (matching `:1604`).
4. Promote "grep all producers/consumers" from open-question to REQUIRED scope; add acceptance that `:1885-1890` reconstruction reader + `:2308-2322` validator are reconciled and round-tripped (they read the `substrate_binding` wrapper today and WILL break on un-nesting).
5. Add acceptance: update the EXISTING MIGRATION `substrate_binding` contract entries (`generation/MIGRATION.md:287`, `simulation/MIGRATION.md:4126-4130`), not just append.

No BLOCK. Conditions 1-2 close metrology-inheritance holes; 3 is precision; 4 is the one genuine scope gap (a second/third consumer that breaks on the fix); 5 keeps MIGRATION honest.

**Signed:** jack-ryan, 2026-07-06, Gate-1 DESIGN-MODE.
