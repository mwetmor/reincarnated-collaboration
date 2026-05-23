# Court of Forms — Reincarnated's End-Game Spine

> **STATUS:** HISTORICAL-INFORMATIVE (pre-Epoch-4; consult for lineage only — not current truth) — see `canonical/00-ground-state.md` for current truth

**Status:** **Canonical.** Locked 2026-05-15 by Matt in Pattern B dialogue with gandalf. Supersedes any prior "form library as gacha-roster" / "gallery" framing.

**Companion docs:**
- `gandalf-phase2-bullet-points.md` § 1.4 + § 4 — the recommendation that produced this lock
- `gandalf-design-lineage.md` — Layer 5 (Solo Leveling studio work) for precedent
- File 29 § "Cross-season meta-progression — Earth Self is the meta-layer spine" — the strategic anchor this doc operationalizes
- File 32 § Section 5 + § Section 11 — form library acquisition rules (one per season; only the form alive at season end ascends)
- File 33 § "Form library acquisition" + § "Earth Self meta-layer" — the prior structural commitments
- `pitch-2026-05-18/one-pager.md` — the commercial framing this lock strengthens

**Pending:**
- knight-rider to draft a decisions-log entry capturing the lock (per ADR-002 tiered authority; cross-seam framing impact — affects engine ascension event design AND eventual loadout/demo Earth-layer hub presentation)
- This doc is the canonical reference until the decisions-log entry lands; afterward, the decisions-log entry is the primary lock and this doc is the design-intent expansion

---

## What the Court is

The Earth Self's hub holds the **Court** — the assembly of forms that have ascended from completed seasons. The Court is not a gallery of icons stacked in a UI grid. The Court is a **navigable assembly of named retainers with stations and (over time) presence.**

The Court is the player's *accumulated record of who they have been willing to become.*

## Why this framing matters

The project's eventual end-game has been structurally identified for some time (file 29's "cross-season meta-progression — Earth Self is the meta-layer spine"; file 32 § Section 11 "form ascension at season end") but its **player-experience weight** was underspecified. Prior framings reached for gacha-language ("accumulation of LLM-generated ascended spirits") which is mechanically accurate but emotionally thin — gacha collections are inventories, not relationships.

Matt's recognition 2026-05-15: *"The court adds weight to the end game that I didn't understand before and I think you were right that it was missing."* The end-game weight problem is the load-bearing one. ARPGs that don't deliver an end-game weight that justifies the seasonal arc lose retention; the genre has many shipped failures of this kind. Reincarnated's seasonal-journey-as-descent + return-to-Earth pattern was always pointing at the Court; the Court framing makes the pointing explicit.

## The meaning-of-the-arc statement

**LOCKED CANONICAL 2026-05-15:**

> *Reincarnated rewards the patient. Each season is a life-lived; each form a self-tried. You ascend the one you chose to live with — and over many seasons, your Court accrues those choices. The depth of the Court is the measure: how many forms have you been willing to become; how many have you ascended through their full journey; how many seasons has the Wheel turned with you still walking. There is no final form because there is no final you; there is only what the Court remembers.*

This statement is the **player-experience answer to "what does winning Reincarnated mean."** It is intended to be referenced (in part or whole) by:

- The pitch one-pager when describing the game's meta-layer
- The eventual Phase-0 season-end ascension cutscene / UI copy
- The eventual Earth Self hub presentation copy
- Spirit Guide voice lines at ascension moments
- LLM prompt context that needs to honor the meta-layer framing
- Any future design conversation about end-game balance, content cadence, or progression weight

The three measurable axes are deliberately stated:

1. **How many forms have you been willing to become** — diversity of ascensions. Honors body-swap pillar; rewards experimentation across seasons.
2. **How many have you ascended through their full journey** — completion quality. Honors the body-swap-path-vs-Mirror-Trial-path-vs-Passage gradient; rewards committed playthroughs.
3. **How many seasons has the Wheel turned with you still walking** — longevity. Honors the seasonal-rotation premise; rewards sustained engagement.

These are not three separate currencies. They are three readings of the same depth. The Court's depth is read on all three axes simultaneously.

## Solo Leveling's Shadow Army — the precedent cited

Per `gandalf-design-lineage.md` Layer 5: A-1 Pictures' adaptation of Solo Leveling features Sung Jin-Woo's Shadow Army as accumulated identity. Five features make it a Court not a Gallery:

1. **Each shadow has a name and the name is load-bearing.** Igris, Iron, Tank, Beru, Bellion. The reader and the protagonist know each by name; names are how shadows are summoned, referenced, remembered. Reincarnated already has this — every LLM-generated form has a name. The work is not generating names; the work is *honoring* the names at the meta-layer.

2. **Each shadow has a rank within the army.** Soldier / Knight / Marshal / Grand Marshal / Monarch. The rank reflects power-tier *and* responsibility hierarchy. (Reincarnated's rank-axis: open question, see § Open below.)

3. **Most shadows are absent until summoned.** They live in the shadow realm; have presence when called; recede when not. (Reincarnated's hub-presentation policy: open question, see § Open below.)

4. **A handful of shadows become intimate characters.** Beru speaks. Iron is loyal beyond reason. Bellion is wise counsel. Most shadows don't speak; they just *are.* (Reincarnated's voice-emergence rule: open question, see § Open below.)

5. **Accumulation is slow and narratively weighted.** Each new shadow is a story moment; the audience remembers when each joined. Reincarnated's "one ascension per season" pace matches this rhythm structurally.

## Fate/Zero / Nasuverse — considered as canonical reference, rejected as substrate-incompatible

The Fate franchise (Fate/Zero, Fate/Stay Night, the wider Nasuverse) was considered as a candidate canonical reference for the Court in dialogue with Matt 2026-05-15. The structural surface is appealing:

- **Throne of Heroes ↔ Court** (accumulated identity repository)
- **Master-Servant bond ↔ Earth Self bond to ascended form** (the player commands; the form acts)
- **Class-role architecture** (Saber / Archer / Lancer / Rider / Caster / Assassin / Berserker) ↔ Reincarnated archetype taxonomy
- **Command Seals** ↔ candidate limited-mandate mechanism for hypothetical rift-event deployment
- **Partial-presence** (Servants manifest when summoned, recede otherwise) ↔ Court members as retainers in residence

The structural surface aligns cleanly with Reincarnated's existing architecture. The Fate frame would have been a tempting canonical reference.

**It was rejected** for one load-bearing reason: **Fate's substrate is intrinsically humanoid.** The Throne of Heroes is a repository of *human historical/mythical figures who once walked the earth as people* — Arturia Pendragon, Iskandar of Macedon, Diarmuid Ua Duibhne, etc. The lore-weight that makes a Servant matter comes from their pre-Servant humanoid life. The architecture is form-agnostic; the *substrate is humanoid-locked.*

Reincarnated is an **isekai** game (per pitch-2026-05-18 § "Game" and per doc 37's structural realignment). The isekai genre's defining feature is the breadth of forms one can reincarnate into — slime, dragonling, cat-human-slave, swarm, construct, beast, plant, cloud-being. A canonical commitment to Fate's Throne substrate would silently teach the player that their non-humanoid forms are *not real Heroes* — they would be displaced from the meta-layer. This is exactly the implicit-pillar drift pattern doc 37 § 9.1 names as the project's primary structural risk.

The decision (Matt, 2026-05-15): **Fate's frame is retained as a design-conversation lens; it is not a canonical reference.** When developing end-game ideas — the role of Court members in eventual rift events, partial-presence dynamics, limited-mandate mechanisms — the Fate frame is a useful working register for dialogue. It does not enter the canonical layer; downstream docs, dispatches, prompts, and UI should not echo Fate-specific vocabulary (Saber, Master, Servant, Command Seal, Throne of Heroes, etc.).

Solo Leveling's Shadow Army remains the canonical-cited precedent (Shadows include non-humanoid forms — Beru the ant-king, Tank the lion — meaning the precedent's substrate already admits the isekai breadth Reincarnated requires).

This is captured here both as canonical decision-archaeology and as a worked instance of Discipline #13 (implicit-pillar drift) operating in real-time design conversation. The form-bias diagnosis (doc 37) surfaced the Fate-substrate problem the moment it would have entered the canonical layer; the project's drift discipline is doing its job.

## Structural commitments — what's locked

The following are **canonical** for any downstream design or implementation work touching the form library / Earth Self hub:

### C1 — Court framing supersedes Gallery / Roster / Gacha framing

The Court is the presentational and narrative frame. Any UI mockup, copy, dispatch, or LLM prompt that refers to the form library as a "gallery," "collection," "inventory," or "roster" should be updated to use Court language. Gacha-mechanics underneath are operationally accepted (the data model can be drop-rate-shaped under the hood); the *presentation* is Court.

### C2 — The form library has a navigable spatial presentation, not a scrollable card list

The Court is **walked through**, not scrolled. Forms occupy **stations** (positions within the hub), not slots (cells in a grid). Drax's eventual Earth-Self-hub work consumes this commitment.

### C3 — Each form's LLM-generated name is preserved through to the Court

The naming pipeline (rocket / star-lord territory) already produces evocative full names (`"Lantern-Keeper of Yomi's Winds"`, `"Trenchwind Pitch-Caster"`, etc.). These names are the **Court-name**, not the "playable class display name with embellishment." No truncation, no slot-icon-only display, no roster-style abbreviation. The Court names its retainers in full.

### C4 — Voiced retainers emerge over time; not all forms are voiced

A subset of ascended forms gain voice — *brief* dialogue presence at the Court. Voiced forms can be referenced by the Spirit Guide in subsequent seasons (*"the Tidecaller you ascended in your Deep Trench season would know this anchor's shape"*). The voice-emergence rule is open (§ Open below). What's locked: **the design admits voiced retainers; the Court is not silent on principle.**

### C5 — Accumulation is paced and commemorated

One ascension per season is the existing lock. Each ascension is a **commemorated event** — not a "form added to library (N/N+1)" notification. The season-end ascension UI/cutscene treats the form's arrival at the Court as a moment. Drax's eventual end-of-season work consumes this commitment.

### C6 — The Court is the player's, not the Wheel's

The Wheel turns; it does not own. The Earth Self holds the Court; the Spirit Guide announces forms to it; but **the Court belongs to the player.** Naming, station arrangement, and (where applicable) which form is currently in residence-of-honor — these are player-affordances, not engine-determined.

### C7 — The depth-of-the-Court is the meta-measure

Per the meaning-of-the-arc statement: diversity × completion-quality × longevity. These three axes are what future telemetry, achievement design, and player-facing-progression-feedback should measure. NOT raw form count alone.

### C8 — Court class-roles use the dual-label pattern (function tag + embodiment-flavored name)

**Added 2026-05-15 in dialogue with Matt, after the Fate-frame substrate rejection (above).**

Each Court member carries a **class-role** that names their function. The class-role is implemented as a **dual-label**, parallel to doc 37 § 4 Position C's slot-as-functional-mechanic + embodiment-as-narrative-skin pattern:

- **Universal function tag** — form-agnostic, mechanical. Names the role in combat-function terms (candidate vocabulary: *Front-Line / Ranged / Control / Sustain / Burst / Mobility / Specialist* — to be finalized in `embodiment-narrative-layer.md`). This is what the data carries; what the eventual rift-event combat logic reads; what cross-embodiment Court structural queries operate on.
- **Embodiment-flavored class-name** — narrative skin. Names the role in embodiment-appropriate vocabulary. Examples (illustrative; canonical lookups in `embodiment-narrative-layer.md` when authored):
  - Humanoid Front-Line → *Knight*
  - Slime Front-Line → *Bulwark* or *Coagulant*
  - Swarm Front-Line → *Phalanx*
  - Dragonling Front-Line → *Warden* or *Wyrm-guard*
  - Crystalline Front-Line → *Resonance-pillar*
  - Cloud-being Ranged → *Stormcaller* or *Distance-keeper*
  - (etc., per embodiment × function combination)

**Why dual-label and not single-label:**

- A **single humanoid-coded label set** (Knight / Berserker / Archer / Rider / Assassin / Caster / Sage) was initially proposed in dialogue 2026-05-15 and rejected for the same substrate-incompatibility reason that rejected the Fate frame: those labels are humanoid-coded and would re-import the bias at the class-role layer instead of the substrate layer.
- A **single universal-mechanical label set** (Front-Line / Ranged / etc.) is form-agnostic but dulls the narrative register — a Court of "Front-Lines" and "Rangeds" reads as tactical inventory, not retainers.
- The **dual-label pattern** preserves both: the universal tag is what the system commits to; the embodiment-flavored name is what the Court presents to the player. Same architecture as gear slots (doc 37 § 4 Position C); same discipline; same upward-compatibility with the cipher work.

**Cross-dependency:** the canonical authoritative source for both the universal function-tag vocabulary AND the per-embodiment label lookup is `embodiment-narrative-layer.md` (Phase 2 work-queue item #6). That doc is now load-bearing for both gear-slot embodiment-skinning AND Court class-role naming — one canonical source, two consuming surfaces. When `embodiment-narrative-layer.md` is authored, C8 here gets cross-referenced into it; until then, C8 commits the *pattern* and defers the *vocabulary*.

**What this protects against:** the same drift the Fate-frame rejection protected against, at one resolution finer. A future LLM prompt that says "this Court member is a Knight" silently presupposes humanoid embodiment. A future LLM prompt that says "this Court member is a Front-Line *(embodiment: slime → Bulwark)*" is honest about what the data means and what the player sees.

## Open questions surfaced by this lock

These are not blocking the canonical lock above. They become explicit when implementation work on the Earth-Self hub begins (post-Phase-0; Track C/D territory). Capturing them now so they don't have to be re-derived.

### Q1 — Court rank structure

Solo Leveling's Shadow Army uses rank as power-tier-plus-responsibility. Reincarnated's equivalent would be **ascension-quality marker** rather than power-tier (the forms don't operate as a deployable army — they're static records). Candidate rank dimensions:

- Path taken (body-swap-path / doppelganger-path / Mirror-Trial-victory / etc.)
- Acts cleared cleanly before ascension
- Whether the doppelganger end-game-quest was reclaimed
- Whether the season's seasonal set was completed before ascension

Rank could be a **multi-dimensional marker** rather than a linear hierarchy. Open for design conversation when hub work nears.

### Q2 — Voice-emergence rule

Which ascended forms gain voice? Candidates:

- **Pivotal seasons:** forms ascended after particularly long / hard / completionist seasons gain voice
- **Player-favored:** forms the player has explicitly stationed in residence-of-honor become voiced through use
- **Random over time:** voice surfaces slowly across the Court regardless of which form
- **All forms voiced lightly; few forms voiced deeply:** the Beatrice-vs-Subaru pattern applied — every form has *some* presence; only a few have *deep* presence

My instinct: the fourth option, but this needs design conversation closer to implementation.

### Q3 — Hub presentation breadth

Solo Leveling's Shadow Army surfaces 2-3 shadows at any time (the most recently summoned, the currently-relevant, the protagonist's favored). Reincarnated equivalent for the Earth-Self hub: how many forms are visibly present at the Court at once? Options:

- Always-show-all (UI scales; risk of clutter past 30 forms)
- Show-recent-N (most recent N ascensions)
- Show-favored-plus-recent (player-pinned + recent)
- Show-rotating (deliberate rotation through the Court; reveals less-recent forms)
- Show-all-but-with-zoom (full Court visible; player can zoom into stations)

My instinct: the fifth option — *all-present-but-zoom-able*, like a vast hall the player walks through. Drax dispatch territory when hub work nears.

### Q4 — Court interaction surface

Beyond looking at the Court, what does the player DO at the Court? Candidates:

- Pure presentation (look, walk through, read names)
- Pin a form as currently-favored (affects what surfaces in Earth-Self hub)
- Set rotation (which form is in residence-of-honor)
- Speak to voiced forms (Beatrice-register brief dialogue)
- Equip the seasonal set of an ascended form (cosmetic/transmog at the Earth-Self layer)
- Begin a next-season descent from the Court (entry-point to a new seasonal journey)

The Court is the hub between seasons; it likely needs at least the last option (descent-entry-point) plus pure presentation. Other interactions are design candidates.

### Q5 — What happens to the Court at very-late-game (50+ seasons)?

A player who plays Reincarnated for two years could accumulate 50-100 forms in the Court. Solo Leveling's Shadow Army has dozens; the manhwa handles it with rank hierarchy and selective surfacing. Reincarnated needs a graceful answer for very-late-game density. Likely the answer is some combination of Q3 + Q1 (rotation + rank filtering). Worth knowing now even though it's far-future.

## What this lock unblocks

- **Phase 2 work plan item #7** (`court-of-forms.md`) — *this doc.* Item #7 is therefore now COMPLETE in initial-draft form.
- **Phase 2 work plan item #1** (`cosmology-reincarnated.md`) — the meaning-of-the-arc statement is now canonical-ready for inclusion. The Court framing is now canonical-ready for inclusion. The cosmology doc has one fewer open question to resolve before authoring.
- **Pitch readiness for 2026-05-18** — Matt can reference the locked meaning-of-the-arc statement when describing the game's meta-layer to the listener. The Court framing also gives the pitch a *visualizable* end-game ("imagine a court of accumulated retainers from each season's journey, growing across years of play") that the prior gacha-framing did not.
- **Drax's eventual Earth-Self-hub presentation work** — has a target. The hub is a Court. Drax dispatches when that work opens can reference this canonical lock.
- **Star-lord's eventual LLM prompt-template work** — has Court language locked. LLM prompts that touch the meta-layer can use Court vocabulary deliberately.
- **Spirit Guide voice doc (Phase 2 work plan item #3)** — can now reference Court interactions as a venue for Spirit Guide voice presence.
- **Embodiment-narrative-layer doc (Phase 2 work plan item #6)** — newly load-bearing for TWO consuming surfaces: gear-slot per-embodiment narrative skinning (doc 37 § 4 Position C) AND Court class-role labels (C8 above). One canonical source, two consumers. Raises this item's priority within the work queue — it is now upstream of both Court implementation and gear-slot embodiment work.

## What this lock does NOT do

- It does **not** specify implementation of the Earth-Self hub. That remains post-Phase-0 work.
- It does **not** specify the rank, voice-emergence, breadth, interaction, or density rules. See § Open above.
- It does **not** affect Phase-0 in-season body-swap mechanics. Those are file 32 § 11 + doc 37 § 8.
- It does **not** mandate any new LLM cost in Phase 0. The Court is a presentation/data-model framing; the LLM cost lives where it already lives (form name + flavor at generation time).

## Maintenance protocol

When implementation work on the Earth-Self hub begins:

1. Re-read this doc with the implementer (likely drax).
2. Convert the structural commitments (C1-C7) into specific UI/UX/data-model decisions.
3. Resolve the open questions (Q1-Q5) with Matt before implementation locks.
4. Update this doc with the resolved decisions; preserve the canonical-lock-date history.

When LLM prompt work needs to reference the Court:

1. Use Court language (not gallery / library / collection / inventory / roster).
2. Refer to forms as *retainers*, *the ascended*, *those who joined the Court*, *forms in residence*.
3. The Spirit Guide can refer to specific Court members by their full LLM-generated name when context warrants.

When future canonical design docs touch the meta-layer:

1. Cross-reference this doc.
2. The meaning-of-the-arc statement is the canonical answer to "what does winning Reincarnated mean."
3. Court framing supersedes Gallery framing in all design language.

— gandalf, with Matt's canonical approval 2026-05-15
