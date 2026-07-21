# Recognition record — mechanical-axis sparseness + the T4/capstone ontology error

> **STATUS:** RECOGNITION RECORD · architectural commitments DEFERRED to VDM-2 per substrate-led discipline · routes to **elrond** (corpus schema) with **gandalf** axis-taxonomy design input · ratify: jack-ryan / Matt. Author: gandalf, 2026-07-20. Source: Matt observations while reviewing the glance per-kit sample.

## The two observations (Matt, 2026-07-20)

1. **Mechanical sparseness.** "We only have skill mechanics for certain skills, and we seem to be missing a lot of other mechanical axes to describe the builds/kits." (Better than pre-VDM-1, but incomplete.)
2. **T4/capstone extraction confusion.** "Each Kit is exactly the portion of ONE class from the source game that has ALREADY been mechanically altered by a potential capstone/T4 mechanic. So to then look for another alteration beyond the kit's existence itself is folly."

## Analysis

### On (2) — the ontology error (the sharp one)

Matt is correct, and the sample proves it. A **kit IS the already-T4-altered artifact** — base skill + its defining capstone/keystone/ascendancy mechanic, captured as a single unit *because that fusion is what makes it a distinct build.* The `kit_dossier` family `capstone_alterations` asks "what capstone alteration modifies this kit?" — which **presupposes a pre-T4 base the kit could be altered *from*. There is none.** The kit's existence already encodes the alteration.

**Evidence in the sample:** `poe2-twister.capstone_alterations` = `{"ascendancy":"Spirit Walker (Huntress)","notables":["not individually named in fetched guide text"]}`, **conf=0.45**, anchor="the guide … doesn't explicitly name individual Spirit Walker notables." The agent hunted for a separate alteration, found the kit's own identity staring back, and returned a low-confidence near-empty. That confusion is *structural*, not an extraction miss.

**Distinction to preserve:** the kit's ONE *defining* alteration is redundant to re-record (it IS the kit). A kit may *also* stack *supporting* build-defining choices (extra keystones/notables) — those are legitimate mechanical detail, but they were mis-framed as "the alteration," causing the confusion. The fix is not "capture more alterations"; it's "stop modeling the defining alteration as an external modifier."

### On (1) — sparseness is the same problem's other face

We capture kits richly on *some* axes (the 12 `mint_ledger` primitives = the *novel* mechanics; `kit_dossier` prose for *documented* skills) but lack a **complete, structured, per-kit mechanical-axis schema.** The atlas coords (`attr/range/tempo/amp/proxy/commit/econ/elem` + `mob_policy_while_casting`) are the *start* of one, but they're (a) sparsely populated (`mob_policy` is all-NULL; `elements_attested` empty on several) and (b) not comprehensive.

**Concrete proof from the pinnacle mapping (same session):** to find the autonomous-emitter family I had to **keyword-sweep dossier prose** ("wander/erratic/moves-toward") because "self-locomotion / autonomy" **is not a captured axis.** Had it been a column, the mapping is a `SELECT`, not a text-sweep. The under-anchoring of mints #8/#10 (four unlinked roaming kits) is a direct symptom: without a locomotion axis, the substrate can't cluster what it can't name.

## The unifying fix (VDM-2 candidate — NOT committed now)

(1) and (2) resolve to **one** move: **replace the confused "alterations" extraction with a proper structured mechanical-axis schema, where the kit's T4/defining identity becomes axis-VALUES, not a separate "alteration" record.**

- Retire / reframe `kit_dossier.capstone_alterations` (folly as posed). If supporting-stack detail is wanted, ask it as a clearly distinct question, not "what alters this kit."
- Define the missing axes as first-class columns. Candidate axes surfaced by this session: **locomotion_mode** (static / player-orbital / drift / self-seeking / roaming / host-attached), **trigger_condition** (on-cast / proximity-armed / timed / channel), **persistence** (instant / duration-entity / permanent), **targeting** (aimed / homing / undirected), **resource-coupling** (e.g. stat→damage, the HoWA #9 axis). Let the *kits vote* which axes earn a column (substrate-led — do not pre-impose a giant schema).
- The kit's defining mechanic = its axis-values + the mints it forces. Coherent, non-duplicative, queryable.

## Discipline / routing

- **Recognition NOW; commitment AFTER VDM-2.** Per substrate-led discipline, do not rewrite the corpus schema on this recognition alone. The empirical gate: a VDM-2 axis-taxonomy pass (which axes do the 574 kits actually distribute on?) validates the column set before it's built.
- **Seam:** corpus schema = **elrond**. Axis-taxonomy *design* (what the axes mean, genre-precedent for each) = **gandalf**, optionally with a **legolas Mode A** pass on how ARPG theory decomposes build-mechanics (candidate, not fired).
- **Ratify:** schema change → jack-ryan / Matt.
- **Do NOT bundle into the glance render build** — that build is diagnostic and ships against the current (sparse) data; this schema work is the follow-on it motivates.

## Prediction registered

When VDM-2 defines a `locomotion_mode` axis and backfills it, (a) the roaming-emitter family becomes a clean `SELECT` (no keyword sweep), (b) mints #8/#10 promote as their four unlinked members anchor, and (c) `capstone_alterations` confusion disappears because the defining mechanic now lives in axis-values. If those three hold, the fix is validated.
