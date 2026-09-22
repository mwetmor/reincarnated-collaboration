# The Commission Rule — at a knowledge boundary in the referent, buy the knowledge; do not choose a value

> **Status: STANDING POLICY, Matt ruling, 2026-09-21.** Issued as the resolution of the KC2-PLAY energy fork (KP-68 → KP-70), and deliberately generalized by him beyond that fork. Recorded HERE and not only in the session that received it, per the `CLAUDE.md` conflict rule's own mandate — *a posture communicated to one session is not a posture the wave has.*
>
> Conductor/author: gandalf (ARCHITECT). **Discipline-form ratification routed to jack-ryan;** this note is the policy of record until a number is minted.

## 1. The ruling, in Matt's words

> *"I want to match the oracle by commissioning recovery mechanisms whenever and wherever it is noticed that we do not have a relatively complete understanding of the oracle (have the mechanism be research into the build guide or the game itself on disk or the save file, etc)."*

And the reason, which is the part that governs everything below:

> *"Getting this right will allow us to put a line in the sand that we have a referent battle system so that we can decide to tweak it before joining other kits into it and eventually other games, so that this game becomes a join key and also its own game."*

## 2. What it changes

**Law 3 said: no fitted constants, no invented rules, an absence is declared.** That is a rule about what you must NOT do at a knowledge boundary. It is correct and it is *passive* — under it, a declared absence acquires a row, a grade, and then sits, permanently and honestly, unresolved.

**The Commission Rule adds the positive limb: a declared absence is a RESEARCH COMMISSION WAITING TO BE ISSUED.** The registry stops being a graveyard of things we honourably did not know and becomes **a backlog of things we have not yet bought.**

The two limbs compose into one posture at every boundary:

| | |
|---|---|
| **Never** | choose a value that closes the gap |
| **Always** | declare the gap — *(Law 3, unchanged)* |
| **Now also** | issue a commission against the declared gap — *(this rule)* |

⚑ **The distinction that makes it operable: a commission is warranted by the ABSENCE OF KNOWLEDGE, not by the presence of a symptom.** The energy defect was noticed because Matt felt it while playing. That is the *worst* available detector and we should not build on it. The registry already names boundaries nobody has felt yet; those are commissionable the moment they are written, without waiting for a play session to surface them.

## 3. The named research surfaces

Matt named three, and the list is open (*"etc"*):

1. **The build guide** — the community/author documentation of the referent build.
2. **The game itself on disk** — DBRs, the ARZ/ARC archives, and the binary. *We have already decoded semantics byte-exact from `Game.dll` once (the `invincible` gates at `Character+0x1844`), so this surface is proven, not speculative.*
3. **The save file** — `player.gdc`. *Already the basis for the summon finding: blocks 8 and 14 gave allocation, ranks, item-skill provenance and bar ordinals.*
4. **The footage** — measured referent behaviour. *Already load-bearing: the energy drawdown band `(86.0, 117.0)` was read off the energy globe and is what convicted the port.*

**Routing:** `legolas` (UNKNOWN-RESEARCHER) for external and primary-source work; `elrond` for curation of what returns; `gamora` / `star-lord` to fold a returned finding into oracle and pack respectively. **The conductor identifies the boundary and issues; no seam fills a gap on its own authority.**

## 4. What a commission must carry

A commission that cannot fail is not a commission. Each one states:

- **The boundary**, precisely — the row, the grade, and what is unknown about it.
- **The surfaces to search**, and in what order.
- ⚑ **What a NEGATIVE result looks like, and that a negative result is a RESULT.** *"Searched the build guide, the DBRs and the save; the value is not recoverable from any of them"* upgrades a `SOURCE-UNLOCATED` grade to a **searched** `SOURCE-UNLOCATED`, which is strictly more knowledge than we had. A commission that can only succeed will manufacture a success.
- **What must NOT be done:** no fit, no plausible reconstruction, no "the community says roughly." Law 3 governs inside a commission exactly as it governs outside one.

## 5. The strategic frame, and the two ways it fails

The referent battle system is a **line in the sand**: a fully-provenanced baseline from which divergence becomes *deliberate* rather than accidental, and onto which other kits — and eventually other games — can be joined.

**⚑ FAILURE MODE 1 — the referent becomes the target by gravity.** The moment a perfect referent exists there is enormous pull toward treating it as *correct* rather than as *known*. Grim Dawn's combat math is twelve years of accretion in the Diablo-2 lineage: conversion chains, resist-reduction stacking, flat-vs-percent ordering that even depth-seeking players find opaque. **What makes it an excellent REFERENT — real, complete, measurable — is not what would make it a good FOUNDATION.**

*Matt has already named the guard* (**"decide to tweak it before joining other kits"**). The discipline that enforces it: **write down which parts we intend to KEEP and which we are only reproducing to prove we understood them — now, while the referent is being built, not after it is finished.** Precedent: Diablo III shipped an itemization faithful to a specification nobody had stress-tested against play — the fidelity was to the *spec*, not to the *experience*. Path of Exile's manifesto tradition exists precisely because GGG kept having to make its deliberateness explicit rather than let complexity read as intent.

**⚑ FAILURE MODE 2 — a join key needs a SCHEMA, not a correct instance.** We have one character, one build, one game. The join-key claim requires that the *abstractions* survive contact with a game that has no energy, or three resources, or cooldowns in place of a resource entirely. **The v3.x pack shape is Grim-Dawn-shaped**, and nothing has yet tested whether its concepts generalize or merely fit. That is the next architectural question, and it is better asked while the second kit is hypothetical than after it has been forced into a schema built for the first.

## 6. Standing queue at issue (2026-09-21)

Open boundaries that are commissionable **today** under this rule. Named here so the policy has a population on the day it is written, not a promise of one.

| # | Boundary | Grade / state | Surfaces |
|---|---|---|---|
| **C-1** | **Off-channel energy recovery rate** | no row, no grade — a runtime construct; the oracle has NO off-channel branch, yet the referent demonstrably returns to the ceiling (1594/2576 at four timestamps across 830 s) | build guide · DBRs · footage |
| **C-2** | **Per-cast energy cost, all four bound skills** | not in the pack, **not in the 42-entry absence registry either** | DBRs (`skillManaCost`) · save |
| **C-3** | `energy.cost_factor` **0.90** | `MEASURED-EXACT-SOURCE-UNLOCATED` — **the one back-solved value in the energy stack**, graded honestly | gear/devotion sheet · DBRs · build guide |
| **C-4** | `TIP_THE_SCALES_TRIGGER_CHANCE` **0.33** | `DB-CITED` and **consumed by nothing** — referenced once, at its own definition; the envelope row credits a *bound* ("up to 100/s") as a *realized* rate where the sibling row distinguishes the two | spec §9.3 · DBRs · footage |
| **C-5** | Guardian of Empyrion's `IMPL` cell — permission or refusal? | **UNDECIDED**, 0 casts / 2,567 undecided (`B3-P17`); `MD-B3-2` is the lap that lifts it | binary · footage |
| **C-6** | `OPEN-UNKILLABLE` | named thread at ~30×, first cause found and three excluded | oracle · pack · DBRs |

**C-1 is issued.** The rest are enumerated and unissued; issuing them is sequencing, not a fresh ruling.

---

**Signed:** gandalf (ARCHITECT), for the run and beyond it.
**Ratification:** discipline-form to jack-ryan; the policy binds from the ruling date regardless.
