# Gender axis → KR handoff brief (rocket build + drax parallel)

**From:** gandalf (SPEC-AUTHOR) · **To:** knight-rider (sequencing + dispatch) · **Date:** 2026-07-13
**Full design:** `gender-as-reincarnation-axis-2026-07-13.md` · **Race well:** `canonical/reap-die-rise-engine/bestiary-race-well-design-2026-07-09.md`
**Ratified (Matt 2026-07-13):** design approved; roll = uniform binary 50/50 within the gendered branch (v1); **Orc route (a)** — resolve female-orc reskin, all 5 races roll M/F.

KR: cover-sheet. One primary build target (rocket) + one parallel presentation dependency (drax).

## ⚠ UPSTREAM DEPENDENCY — do NOT dispatch standalone (reconciliation 2026-07-13)
Race reconciliation confirmed the ratified well = exactly 5 (Human/Orc/Elf/Dwarf/Goblin), budget-verified. **BUT the pipeline does not emit race as a per-form coordinate yet** — race is schema-only scaffold (Discipline #40); `mob-affix-system-spec §10.1`: *"mob/kit records carry no race field"*; the well is a build target for **E10 Leg 3**, not yet consumed. Only culture-seeds (§4) are wired (LLM morphology steering), not a discrete emitted race field.

**Consequence:** the gender roll is race-conditional → it has a HARD dependency on race emission. It cannot condition on a race coordinate that isn't on the record. **Bundle gender-axis WITH, or sequence it immediately AFTER, the E10 Leg 3 race-well emission build.** Both are per-form emission fields consuming the same closed well; gender rides in the moment race becomes an emitted coordinate. Do NOT fire gender-axis before race emission exists.

---

## What this is
Add **gender** as a per-form generation-emission attribute on becomable vessel forms — deepens the reincarnation theme, widens form-library variety. NOT an IP device (in-game is already pipeline-named), NOT a balance axis, NOT a population multiplier.

## rocket — the build (generation seam)
1. **Deterministic gender roll at form-emission.** After race is assigned, roll gender conditioned on race. Seed-deterministic + reproducible like every other emission axis. **Roll table (all 5 becomable races → {M, F}, uniform 50/50):** Human, Orc, Elf, Dwarf, Goblin. Mob-only kinds (skeleton/demon/werewolf) are NOT becomable → no roll.
2. **THE LOAD-BEARING CONTRACT — gender is a rolled INPUT to the LLM, never an LLM OUTPUT.** Inject the rolled gender into the flavor-emission prompt as a *fixed constraint* ("this form's gender is {gender}; generate name / portrait direction / flavor consistent with it"). Gender must NOT appear as a choosable field in the LLM output schema. This is the entire anti-stereotype architecture — if the LLM picks gender it reproduces archetype↔gender training correlations (archer→female); rolling upstream decorrelates by construction. (Prompt site is near `src/reincarnated/llm/ws1a4_lite_flavor_judgment.py` — rocket confirms exact seam.)
3. **Persist gender on the per-form record**, fixed for that form's lifetime (the Earth-Self re-encounters an accumulated form with the same gender). rocket confirms the exact per-kit/per-form record where race assignment already lives.
4. **Mechanical-inertness guarantee (verify + assert):** no stat / geometry / economy / balance field reads gender. Gender colors ONLY name, portrait direction, flavor. This keeps the S6 cert set + matchup harness untouched (no 2× population).

## drax — parallel presentation dependency (does NOT block rocket)
- **Female-orc reskin (Orc route a):** female-human modular frame + orc green-skin material + bulk modular pieces on the existing sidekick rig. Zero new rig (Orc is a reskin race). Reskin-cost check → deliver the female-orc asset.
- **Gender presentation for the 4 confirmed races:** hair/silhouette swap at ARPG camera. **No new body art needed** — audit finding: at Camera B′ zoom, Synty gender reads mostly as hair length + silhouette; the LLM emission carries gender identity, the body is a subtle secondary cue.
- drax answers: does a presented form read as portrait or 3D body (sets which surface leads on gender).

## star-lord / elrond — post-build audit hook
Decorrelation audit (Discipline #11): after a generation batch, one query verifying gender distribution is ~uniform across archetype / delivery / element buckets. A per-bucket skew = the LLM smuggling correlation back via flavor → harden the prompt constraint. Run once post-integration, periodically after.

## Sequencing (the call)
- **GATE: race emission (E10 Leg 3 race-well build) must land first** — see the upstream-dependency box above. Gender-axis is NOT independent; it conditions on the emitted race field.
- **rocket gender build** (roll + injection + persistence + inertness) bundles with or follows the race-emission build. It ships the feature once race is an emitted coordinate.
- **drax female-orc reskin runs in parallel** — independent of the emission gate; the asset just needs to exist before orc-female forms render.
- **audit hook lands after** the first batch generates with gender.

## Guardrails to carry into the dispatch (non-negotiable)
1. Rolled input, not LLM output (contract §2 above).
2. Mechanically inert — never a balance field.
3. Per-form roll, not a M/F multiplier — one gender per form, population flat.
4. Roll scope = the 5 becomable vessel races only; mobs excluded.
