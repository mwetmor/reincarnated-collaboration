# Trial Room Mechanic and Class-Count Scoping

## Status

Discussed and agreed in working session 2026-05-08 between project owner and son. Captured here as design intent for engine implementation. Not yet a formal `decisions-log` entry; will be promoted to a formal decision once the architectural option (A/B/C from `04-decision-options.md`) is chosen and the implementing pipeline is clear.

This document refines three things:

1. **The spirit-swap mechanic and form-library framing** (overall player-class relationship model).
2. **How many classes a season produces, and in what shape.**
3. **The trial-room mechanic that turns spirit-swap into a player-facing choice.**

These are connected: the form-library framing motivates the trial-room idea, the trial-room idea presupposes a specific number and kind of generated class, and the class-count decision is shaped by what the trial room needs to display.

## Mechanic framing — spirit-swap and the form library

This document originally used "body-swap" terminology, inherited from earlier discussion. Following clarification on 2026-05-08, the more accurate framing is **spirit-swap**, with these properties:

- The player has a persistent **earth-self** — an anchor identity that does not change through the course of the game.
- Defeated trial bosses contribute their classes/forms to a **form library** that the earth-self can reincarnate into, *temporarily*. Reincarnation is cycling, not replacement.
- The engine's name (*reincarnated*) reflects this: temporary, repeated cycling between forms anchored to a persistent self.
- This is **solo gameplay only** — no party / team mechanics. Pre-existing decision; reaffirmed 2026-05-08. ARPG real-time control of multiple actors is rejected as confounding.

**Why this framing matters architecturally:** the player will shift between collected forms across short timescales — possibly minutes, possibly seconds in combat. Each form's mechanical feel must read **immediately** on entry, not over hours of play. That demand is exactly what Option C (dimensional generation) is structured to deliver: class identity that lands instantly via energy / range / armor / damage dimensions. With form cycling, indistinct classes become an actively bad experience — the player swaps and feels nothing changed. The case for differentiation is therefore stronger here than in a conventional ARPG where you commit to one class for the run.

## Decisions made

### 1. Class count: target ARPG genre average (5–6 playable per season)

The current pipeline generates 11 archetypes per season (e.g., season_000042). The decision is to **scope this down to 5–6 generated playable classes per season**, matching the established ARPG genre average:

| Game | Playable class count |
|---|---|
| Diablo 2 (vanilla / LoD) | 5 / 7 |
| Diablo 3 (vanilla / final) | 5 / 7 |
| Diablo 4 (launch / w/ DLC) | 5 / 6 |
| Path of Exile | 7 |
| Path of Exile 2 | 6 |
| Last Epoch (base) | 5 |
| Grim Dawn (base) | 6 |
| Torchlight 2 | 4 |

The genre median sits around 5–6. **Recommended target: 6**, with 5 as a fallback if generation pressure or pacing argues for it.

**Rationale:**

- A smaller pool fits the trial-room mechanic — the player chooses among visible options, and that choice should be meaningful rather than overwhelming.
- Reduces generation cost per season (LLM calls, balance verification cycles).
- Concentrates balance, naming, and quality effort on fewer combatants per season.

### 2. Act-boss classes: 3 extra generated classes per season

In addition to the playable pool, the season generates a small number of **act-boss classes** that are never added to the player's spirit-swap form library — they exist only as encounter content. These are produced by the same generation pipeline but with different balance targets:

- **Act 1 boss — 1 undertuned class.** Generated with relaxed validity criteria, *allowed to fall below the current 40% balanced threshold*. Buffed to boss tier in the encounter, but the underlying class is intentionally under-balanced (appropriate for early-game challenge).
- **Mid-act / late-act bosses — 2 over-tuned classes.** Generated above the balance threshold:
  - One targeting ~55% of the balance modifier.
  - One targeting ~60%.

**Total per season:** 5–6 playable + 3 act-boss = **8–9 generated combatants**, down from the current 11 archetypes (and with sharper structural roles).

### 3. Trial Room mechanic — boss gallery as spirit-swap entry point

The trial room is the structure where the player adds a new form to their library. It becomes a **visible gallery of frozen / encased bosses**, of which the player chooses one to revive and fight. Defeating the revived boss adds that class to the player's spirit-swap form library.

**Mechanic:**

- Trial room visually presents the season's bosses, each frozen / encased (e.g., in stone, ice — visual treatment TBD).
- Player approaches and chooses one to revive.
- Successful defeat → that class is added to the player's form library; the earth-self can subsequently reincarnate into it.
- **Non-chosen bosses disappear** once a choice is committed. (No "come back later for the others" option.)

**Information visible at choice time:**

- Boss visual / model. (Eventually rendered, e.g., Mixamo-Unity skins or equivalent — far-future phase.)
- Weapon type.
- Armor type.
- **No class name.** Players evaluate by visual + gear silhouette, not by label.

**Failure cost:**

- Not modeled in the balance simulator.
- In the actual game: defeat resets the trial dungeon; player restarts the dungeon and re-attempts (presumably can re-choose).

## Implications for engine work

### Generation pipeline

- Pipeline must produce **5–6 playable classes + 3 act-boss classes per season**.
- Act bosses use different generation parameters: relaxed validity for the undertuned act-1 class, elevated balance targets (~55% and ~60%) for the two later act bosses.
- Naming pipeline likely needs to distinguish playable vs. act-boss outputs (different naming purposes / prompts for "boss" identity).

### Balance simulator

- Existing end-game gauntlet covers playable classes against the ~50% modifier target (as in current Priority 01 work).
- Act bosses need their own balance assessments (under-target for act 1, over-target for later acts).
- **Future work — explicitly out of scope for the current phase, but flagged so it isn't lost:** start-of-game and mid-game gauntlets must be layered in alongside the current end-game gauntlet, to validate class scaling across the whole game arc.

### Trial-room mechanic implementation

- Out of scope for the current phase. Visual rendering, encounter design, dungeon structure, and the spirit-swap activation/duration model are far-future work.
- For now: generation produces the bosses; the choice/encounter loop and the form-library mechanic are future implementations. The current phase only needs to produce the right *kinds* of generated content for the future mechanic to consume.

### Existing season_000042 content

- The 11 archetypes in season_000042 do not match the new structure (5–6 playable + 3 act-boss).
- This intersects with an open question already noted in `03-architectural-proposal.md`: backfill, regenerate, or treat as legacy?
- **Recommended treatment (subject to discussion):** treat season_000042 as legacy reference for the decomposition exercise; the next generated season uses the new structure.

## Implications for the architectural decision (A/B/C)

The trial-room mechanic and the form-library framing both put direct pressure on class differentiation:

- **Trial-room choice point:** side-by-side selection with visible weapon/armor type but **no class name** means players evaluate via mechanical/visual identity.
- **Form-library cycling:** the player will shift between collected forms across short timescales. Each form's feel must read immediately on entry.

That is exactly the value Option C (dimensional generation) is designed to produce — energy type, armor weight, and weapon style become the dimensions the player actually *sees and chooses against, and feels on shift*.

Combined with the son's confirmation that classes should have different energy and feel, this narrows the decision noticeably toward **Option C**. It does not collapse the decision automatically — the decomposition exercise (`05-action-plan.md` step 3) is still warranted to validate that the dimensional approach maps cleanly onto existing generated classes before committing.

## Open questions

### About generation and balance

1. Are act bosses dimensional combatants too (sharing the dimensional generation pipeline), or specially handled outside it?
2. Does the season's playable pool intentionally cover diverse dimensions (so the trial-room gallery spans visibly different combatants), or is variety left emergent?
3. Backfill question for season_000042 (regenerate, leave as legacy, or convert to dimensional descriptions).

### About spirit-swap mechanics (load-bearing for combat / sim scope)

4. **Earth-self as a class, or abstract anchor?** Does the earth-self have its own ability kit and combat identity (a starter form you keep), or is it a non-combat soul / inventory — you must always be in a borrowed form to act?
5. **"Temporary" — what's the duration model?** At-will switching? Time-bound (each form lasts X minutes)? Scarce resource ("reincarnation charges")? Tied to specific events (must reincarnate at a specific altar / before a trial)? This affects combat pacing and possibly whether the simulator must model form-switching mid-fight.
6. **Form-shift cost / friction.** Is changing forms instant and free, or does it require something (animation, vulnerability window, resource cost)? Affects whether players "swap freely, vibe-check each form" or "commit to one form per encounter, choose carefully."
7. **Earth-self vulnerability / state.** Do collected forms share HP / resources with earth-self, or each has its own state? If shared, dying in form A means dying entirely; if separate, forms become semi-disposable.

### Future-phase (flagged, not for current decision)

8. Visual rendering: what's the intended pipeline for "Mixamo-Unity skins or equivalent"?
9. Trial dungeon structure: is the trial room a single fixed location, or does each season's dungeon have its own structure with the gallery somewhere inside?

## Design references and influences

**The 7th Saga (SNES, Enix, 1993).** Project owner cited as exact structural match for the trial-room boss-gallery mechanic — a finite cast of distinct rivals, encountered as choice points, each with strong individual identity. The gallery-of-rivals structure is the inspiration the trial-room design draws on.

Two important divergences from 7th Saga, both already resolved:

- **Genre and pacing:** 7th Saga was turn-based; this engine is real-time ARPG. Real-time control of multiple actors was rejected as confounding for this game.
- **Recruitment vs. spirit-swap:** 7th Saga grew the party 1 → 2 (recruitment / team play). This engine accumulates *forms in a library* for the earth-self to reincarnate into, not allies to control. Solo-character gameplay is a pre-existing constraint; the 7th Saga reference is *retrospective validation of the gallery structure only*, not a directional signal toward team play.

## Recommended placement in the engine repo

I have not directly read the `reincarnated-engine` repo structure (per the working agreement), so this is a recommendation pending confirmation:

**Primary recommendation:** `engine-repo/docs/design/trial-room-and-class-scoping.md`

- Creates a `design/` subfolder under `docs/` if one doesn't exist. This is conventional for separating *design intent* docs (this file) from *implementation specs* (test plans, evolution plan) and *reference docs*.
- Relative to existing structure, this sits alongside `docs/evolution-plan.md` but in a clearly-marked "this is intent, not yet a plan" subfolder.

**Fallback if `docs/` is flat:** `engine-repo/docs/trial-room-and-class-scoping.md`, with a link added from `evolution-plan.md`.

**Cross-cutting:** This is also a *design* decision and arguably belongs in the design subdirectory of the engine repo. Once the architectural decision (A/B/C) is made and this becomes a formal decision, the user should also add a corresponding entry in `engine-repo/design/decisions/decisions-log.md` capturing:

- The class count scoping (5–6 playable + 3 act bosses).
- The trial-room boss-gallery mechanic.
- The spirit-swap and earth-self framing.
- Information visible at choice time.
- The act-boss balance targets (sub-40% / 55% / 60%).

## Cross-references

- `03-architectural-proposal.md` — dimensional generation proposal that this design strengthens.
- `04-decision-options.md` — A/B/C options now informed by this design context.
- `05-action-plan.md` — step 3 (decomposition exercise) is the next action; this doc supplies the design intent that should inform it.
