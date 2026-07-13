# Gender as a reincarnation axis — pipeline-rolled, LLM-constrained

**Author:** gandalf (SPEC-AUTHOR / STORYWRIGHT) · **Date:** 2026-07-13 · **Status:** DRAFT — awaiting Matt ratification, then routes to rocket (generation) + drax (presentation).
**Ratified inputs (Matt 2026-07-13):** gender is *randomized*; it *supports* the LLM's data-driven flavor rather than being an LLM decision; the failure mode to prevent is the LLM correlating gender to archetype (e.g. "all archers are female").

---

## 1 — Purpose & frame (why this exists)
Add **gender** as a per-form generation attribute that (a) deepens the reincarnation theme and (b) increases the variety of accumulated forms — **not** as an IP-obfuscation device. (In-game kits already carry zero source names — they're pipeline-named element/hybridity/period/culture/race/faction/flavor — so obfuscation is already solved; gender adds nothing on that axis and is not justified by it.)

**Thematic justification — Reap. Die. Rise. is samsara.** The Earth-Self persists and wears accumulated forms across lives. Rising as a woman one season and a man the next *is the death-faith loop made visible* — the form is *dealt* by reincarnation, not chosen to type. Genre-native to isekai: *That Time I Got Reincarnated as a Slime* makes gender-dissolution-on-reincarnation a celebrated beat; the TS/gender-shift subgenre exists because "you rise as something other than what you were" is a core isekai pleasure.

## 2 — THE LOAD-BEARING PRINCIPLE: rolled input, not generated output
**Gender is determined by a pipeline random roll and injected into the LLM emission as a FIXED CONSTRAINT. The LLM never decides gender.**

This is the entire anti-stereotype architecture, and it is non-negotiable:
- **If the LLM picks gender**, it reproduces the archetype↔gender correlations baked into its training corpus — archer/ranged → female (Bowazon, Amazon, Ranger, Deadeye), heavy-melee → male (Barbarian, Marauder). Every generated form re-inscribes the genre's defaults. Failure mode Matt named.
- **If the pipeline rolls gender upstream and hands it over as a locked input**, gender is *decorrelated from archetype by construction.* An archer form is gender-X because the roll said so, and the LLM must generate a name/portrait/flavor *consistent with the given gender*, not select one. The genre's typecasting can't sneak back in through the front door.

**Contract:** `gender` is an input field in the LLM emission prompt, alongside the already-fixed element/hybridity/period/culture/race/faction. The prompt instructs: *"This form's gender is {gender}; generate name, portrait direction, and flavor consistent with it."* Gender is never in the LLM's output schema as a choosable field.

## 3 — The three ratified guardrails
1. **Mechanically inert.** Gender is an emission + presentation attribute (name, portrait, flavor) ONLY. It never touches mechanics, stats, or balance. The moment gender affects a number, the pre-balanced population doubles and S6 certification / the matchup harness run 2× for zero balance reason. Gender rides *on top of* an already-balanced kit.
2. **Per-form ROLL, not a MULTIPLIER.** Each generated form receives *one* rolled gender, fixed at generation and persistent thereafter (part of the form's identity in the accumulated form-library). Kits do NOT exist in dual M/F variants. Population stays flat; art cost stays linear, not 2×.
3. **Decoupled from the balance population.** Because of (1) and (2), the S6 cert set, matchup digraph, and balance substrate are untouched by this feature. Gender is invisible to every mechanical system.

## 4 — Where it enters the pipeline (rocket's seam)
- **Roll site:** generation, at form-emission time, before the LLM call. Deterministic under seed (reproducible), like every other emission axis.
- **Injection:** gender added to the LLM prompt context as a fixed constraint (§2).
- **Persistence:** gender is stored on the generated form record; fixed for that form's lifetime across seasons (the Earth-Self re-encounters the same accumulated form with the same gender).
- **Emission surfaces it may color:** generated *name*, *portrait/visual direction*, *flavor text*. It must NOT color: any stat, geometry, economy, or balance field.

## 5 — Roll table, reconciled against the RATIFIED vessel-race well
The gender roll applies ONLY to **becomable vessel races** — the forms the player rises as. Per the ratified race well (`canonical/reap-die-rise-engine/bestiary-race-well-design-2026-07-09.md`, Matt-ruled 2026-07-09, W1–W4 + Q17), that well is **CLOSED at 5 races: Human, Orc, Elf, Dwarf, Goblin.**

**W2 scope correction:** undeath is a vessel-*state*, not a race — **skeleton / zombie / werewolf / demon are MOB-ONLY kinds, NOT becomable.** They never enter the reincarnation gender roll. (An earlier draft framed "monster/undead → genderless" as a roll branch; that was wrong — those kinds aren't becomable forms at all. Mobs are gender-irrelevant.)

**Roll table (Synty gender-art audit ⋈ the 5 becomable races):**
| Becomable race | Female art (Synty) | Roll |
|---|---|---|
| Human | ✓ full modular M/F | **{M, F}** |
| Elf | ✓ (modular + Elven Realm) | **{M, F}** |
| Dwarf | ✓ (Casual + Soldier F/M) | **{M, F}** |
| Goblin | ✓ (Goblin + Warrior F/M) | **{M, F}** |
| **Orc** | **✗ none off-the-shelf** | **one decision (below)** |

**The single gap — Orc — is soft, because Orc is a RESKIN race.** Orc is admitted as green-skin + robust-musculature material/mesh on the human sidekick rig (zero new rig). So a **female orc is a reskin of the female-human frame** (material swap + bulk modular pieces), not a missing-rig build. Options: **(a)** resolve the female-orc reskin → full M/F parity across all 5 [gandalf lean — cheap material/modular work, no new rig]; **(b)** orc male-default v1, backfill later; **(c)** orc genderless (weak thematically — orcs aren't "beyond gender" like a reaped corpse). Route (a) vs (b) to drax as a reskin-cost check.

**Distribution within the gendered branch:** uniform binary (50/50 M/F) for v1.

## 6 — Presentation dependency (drax / Godot) — cost is LOWER than feared
Key finding from the audit: **at ARPG camera zoom, low-poly Synty gender dimorphism reads mostly as hair length + silhouette** — the body is a *weak* gender signal. Consequences:
- **The LLM emission (name / flavor / portrait) is the primary gender-carrier**, not the 3D body. Gender lands through §4's emission surfaces; the in-scene body is a subtle secondary cue.
- **No new gendered-body art is required for v1.** The modular Human M/F parts + existing Dwarf/Goblin/Elf female variants + hair-length differentiation suffice at camera distance.
- **drax still owns two answers:** (a) does a presented form read as portrait or 3D body (sets which surface carries gender), and (b) the hair/silhouette swap for the gendered humanoid races. Neither requires new asset creation.

## 7 — Empirical guardrail: decorrelation audit
Because the *point* is breaking archetype↔gender correlation, we can verify it cheaply (Discipline #11, empirical inspection over assumption). After a generation batch, telemetry (star-lord / elrond) audits gender distribution **across archetype / delivery / element buckets** — it should be ~uniform per the roll, with no bucket skewing. If a skew appears, the LLM is smuggling correlation back in via flavor selection and the prompt constraint needs hardening. A one-query check, run once post-integration and periodically thereafter.

## 8 — What this is NOT
- NOT an IP/obfuscation mechanism (already solved upstream).
- NOT a balance axis (guardrail 1).
- NOT a population multiplier (guardrail 2).
- NOT an LLM decision (§2).

## 9 — Sequencing (once ratified)
1. Matt: ratify this doc + rule the §5 distribution (A / B).
2. rocket: add the deterministic gender roll at emission; inject as fixed LLM-prompt constraint; persist on the form record. Confirm no mechanical/balance field reads gender.
3. drax: answer the portrait-vs-body cost question (§6); wire gender into the presented form's visual direction.
4. star-lord / elrond: the §7 decorrelation audit query.
5. gandalf: fold ratified guardrails into the generation spec home once built.

## 10 — Player consequence (the test this must pass)
The player should *feel the reincarnation loop deepen* each time they rise as an unexpected form — a male form of an archetype the genre always drew female, a woman where it always drew a man — because the form was *dealt*, not typecast. If instead gender reads as a cosmetic toggle or a diversity checkbox, the feature failed. The rolled-input architecture (§2) is what makes it read as *fate dealing you a form* rather than *a menu selection* — which is the difference between the theme landing and performing.
