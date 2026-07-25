# Discipline candidate — "A presentation run terminates in frames at the play camera"

**Proposed by:** gandalf (`CANON-STEWARD`), 2026-07-24
**Ratifier:** jack-ryan (per `canonical-doc-format.md` § 6.7 — gandalf proposes, jack-ryan ratifies)
**Target:** `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — next free number (#63 at time of writing)
**Origin:** self-diagnosed defect in a gandalf-authored charter. This is not a proposal about someone else's failure.

---

## The proposed rule

> **Any run, dispatch or wave whose SUBJECT is the presentation layer does not meet its exit
> predicate until it produces images rendered at the play camera.**
>
> Cells, matrices, JSON payloads, latency tables and prose are *instrumentation*. They may
> accompany the frames. They may not substitute for them.
>
> Corollaries:
> 1. **The play camera, not a model viewer.** An asset photographed in isolation answers a
>    different question than the same asset at the gameplay camera, and answers it wrongly.
> 2. **Judgeable by the human, unaided.** If Matt must read a table to know whether the run
>    succeeded, the run has not produced its deliverable.
> 3. **The harness is not optional scope.** If no capture harness exists, building one is
>    inside the run, not deferred out of it.

## Why — the evidence

**The failure.** The 2026-07-23 MCP bake-off (charter: `2026-07-23-mcp-bakeoff-run-charter.md`) ran
18 cells across 3 instruments and 6 probes. It produced PASS/FAIL cells, JSON payloads, a latency
table and a verdict recommendation. It produced **zero frames of what the player camera sees.**

Matt, 2026-07-24: *"I cannot interpret these results without anything to judge."*

That is a complete verdict on the run. The subject was the presentation layer; the deliverable was
not presentable.

**The aggravating detail.** Probe P1 was literally an *isolated-asset* capture probe — a model
viewer. Diablo III's team moved monster-silhouette review off the model viewer and onto the gameplay
camera precisely because a creature that reads beautifully at 3 m and eye level can be unreadable at
the ARPG camera. We rebuilt the rejected viewing condition and called it a probe.

**The aggravating detail that stings.** `reincarnated-godot/scripts/shoot_costume_variants.gd` —
drax, 2026-06-21 — is a variants→contact-sheet→human-eye-pick harness. It existed, it worked, and it
had been used a month before the bake-off. **The practice was not missing. The charter regressed
from it.** A discipline is warranted precisely because good practice already existed and a
well-formed charter still walked past it.

**The mechanism, named.** The bake-off charter's rubric law read: *"the owner's question is 'which
instrument serves our **proven** needs'"* — a backward-looking construction. *Proven* needs were
verification-era needs, so the probe set weighted observation over authoring 4:2, and observation
probes naturally terminate in measurements. **The frame requirement is the guard that makes an
instrumentation-shaped charter still deliver a judgeable artifact.**

## The evidence that arrived after filing — and it is much stronger than what this was filed with

**Added 2026-07-24, same day, after laps L1 and L2 closed. jack-ryan: weigh the ratification on THIS,
not on the argument above.** The original case was *"Matt cannot judge a table."* True, but weak. The
real case is empirical:

> **In this stack, failure returns SUCCESS. Five instances, two laps, three instruments — every one
> reported `ok`, and a rendered frame diffed against a control is the only instrument that has ever
> caught a single one of them.**

1. **M2's transpose** — loaded with zero errors, zero warnings; passed a *complete* structural
   inspection (288 MeshInstance3D, correct names, correct origins, correct material overrides); every
   rotation silently mirrored. Caught by a floor patch reading `(12.9, 12.7, 14.5)` against a
   control's `(115, 93.9, 76.8)`.
2. **`aura_tint`** — the host wrote a `tint` uniform the ruled shader variants do not expose. A silent
   no-op **for every pilot, indefinitely**, until someone rendered `--aura=#FF0000` and saw nothing.
3. **The void-cap rainbow** — sampled a tiling texture the pack does not ship; returned a palette
   swatch strip instead of stone, without complaint.
4. **`custom_aabb`** — the most dangerous of the five. Returns a field **shaped exactly like the
   answer**, identically zero, unrelated to the mesh, `ok=true`. An agent that trusts it derives a
   **zero-sized wall** and every downstream call still succeeds.
5. **Pro's own round-trip** — 252 property writes on node paths **Pro itself had just reported**
   returned **255/255 ok** and wrote nothing to disk.

Return codes did not catch these. Structural inspection did not catch these. Property read-back did
not catch these — in case 4 the read-back *was* the lie. **Only pixels.**

That is why the rule is not a courtesy to the human reader. It is the only working detector we have.

## Relation to existing canon

This is the **run-level enforcement** of the A1 presentation law already ruled by Matt in
`canonical/current-to-end-state/current-to-end-state-game.md` PART A:

> *"Only author and judge what the player camera sees."*

A1 governs authoring. It was not read as governing *runs about* authoring, and the gap let a
presentation run ship without a presentable artifact. The proposed discipline closes exactly that
gap and adds nothing else.

## Scope boundary — what this does NOT say

- It does not require frames from runs whose subject is engine math, corpus extraction, telemetry or
  schema. Those have their own exit predicates.
- It does not forbid instrumentation. ~~The bake-off's latency finding (114–180 ms/call → ~2.5 min of
  pure wire time per 1,000 nodes) was genuinely load-bearing and is the reason the wire will never
  carry assembly.~~ **STRUCK 2026-07-24 — that constant was FALSIFIED by TCP-L2: 8.33 ms/call measured
  over 1307 calls. It was one instrument's number generalized to a category, and "the wire will never
  carry assembly" does not follow from it.** The honest version: keep the tables, add the pictures,
  and **do not let a table become a category claim.**
- It does not require *beautiful* frames. It requires *judgeable* ones. A frame showing a failure is
  a passing deliverable.

## ⚠ NECESSARY, NOT SUFFICIENT — added 2026-07-25, and jack-ryan MUST fold this in before ratifying

**Ratify the rule with this clause attached, or canon over-claims.** The evidence above says pixels are
the only detector that has ever caught a silent failure in this stack. **TCP-L4b found the counter-case,
and proved it rather than asserting it.**

Pro's cycle 1 shipped **four exactly-co-located duplicate meshes** — same mesh, same world extents to five
decimals, one dressed and one with a null material — under each FBX prop root. Census on reload:
**318 nodes out against 314 expected, 4 untextured `MeshInstance3D`.** All 37 wire calls returned `ok`.

**A rendered frame is structurally incapable of catching it.** The duplicate is occluded by its own
original at every camera. drax computed the cycle-1 → cycle-2 pixel change mask — cycle 2's only
structural act was deleting the four duplicates — and **both pillar shafts and both braziers appear as
unchanged black silhouettes.** Every changed pixel lay on the platform, the treads, or their shadows: the
triplanar-UV ruling, not the deletion. The `__box` numbers agree independently — the *outside* figure did
not move at all (59 → 59). **Removing four duplicated meshes was worth exactly zero pixels.**

The instrument that caught it was a **reload-from-disk structural census**, and it must reload rather than
parse the `.tscn` text, per the rig's own header: *"whether Godot double-creates it is an engine
behaviour, not a text property."*

> **The corrected rule: a presentation run terminates in frames AND, where the run writes a scene to
> disk, a reload-from-disk structural census. Two instruments, two failure modes, and they do not share
> one.** Frames catch what changes the picture. A census catches what changes the file. A silently
> duplicated co-located node **doubles the draw calls, the file size, and the cost of every later
> reparent, while changing nothing a human or a differ can see.**

**The comparative result this produced is the strongest argument the whole program has made** — and
neither cell could have produced it alone, which is the direct vindication of Matt's TCP-22 overrule:

| instrument | ownership choice | consequence at save | caught by |
|---|---|---|---|
| **W-PRO** (`add_scene_instance`) | own-all | duplicates on reload, materials correct | **census only** |
| **W-MUR** (`node-create`) | own-root-only | correct node count, **materials silently dropped** | **frame only** — white blobs |

**Opposite poles of the same trilemma (TCP-24), each needing a different workaround, each invisible to
the other's detector.** A discipline that mandated only frames would have shipped Pro's defect. A
discipline that mandated only censuses would have shipped Murzak's.

## Already in force downstream

KIT-REPLICA LAP-1 (`2026-07-24-kit-replica-lap1-run-charter.md` §6) was written under this rule
before it was proposed, in the charter's own words: *"No cell, JSON or prose substitutes for a
picture. A presentation run that produces no judgeable frame has not met its exit predicate."* Its
honorable fallback exists so that **every room ships a frame even when its method fails.** That is
the shape the discipline should produce.

---

**Signed:** gandalf, 2026-07-24. Proposed, not ratified. jack-ryan holds the pen on the canonical text.
