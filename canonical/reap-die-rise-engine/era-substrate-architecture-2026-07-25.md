# Era-Substrate Architecture — One Substrate, Many Masks

**STATUS:** CANON — **Matt-ruled in-session 2026-07-25** (GD grill-session reframe dialogue;
Matt posed the two reframe questions verbatim, gandalf's ultra-think answered, Matt: *"yes,
please write this up"*). Governs the cross-era battle architecture and re-frames the
Grim Dawn three-goal program as its first execution.
**Author:** gandalf (ELICITOR/SPEC-AUTHOR). **Ruling record:** this doc + the session
transcript; companion analysis `agentic_orchestration/gandalf/notes/2026-07-25-gd-three-goal-end-state-and-twin-analysis.md`.
**Supersedes:** the informal "join all 4 games exactly for a precise battle through the
ages" imagining — **retired as incoherent, not merely expensive** (§2).

---

## 1. The ruling, in one paragraph

The cross-era battle ("battle through the ages" — characters from different ARPG eras
fighting in one arena) is built on **ONE combat substrate — the GD-validated one — worn
with era-masks.** Characters are converted **faithfully per game** (conversion keys against
each game's best anchors); monsters and combat-feel are **NOT converted per game** — the
sim's monster AI substrate, tuned and validated against Grim Dawn's live oracle, is
**re-parameterized into era profiles**. We deliberately skip the other games' AI/combat-feel
joins. Matt's two reframe questions, both ruled YES:

1. **Q1 — anchor-join for the other lanes:** tune the battle sim on GD (per taste), use
   GD-derived monsters exclusively as the AI models, and join D2/PoE1/PoE2 via their metric
   anchors + kit data (D2 game files, Path of Building, banked corpus anchors) — skipping
   their live combat-feel entirely.
2. **Q2 — eras as parameter profiles:** represent eras by **tweaking the validated monster
   AI's parameters** (+ statline scaling), not by full per-game monster/AI conversion keys.

## 2. Why the full 4-way exact join is retired (incoherent, not just costly)

A cross-era fight needs ONE set of combat rules or it adjudicates nothing: if the D2 era
brings D2's AI and the PoE era brings PoE's, "my Hammerdin vs your Occultist" is being
judged by two different games at once. Any version of the original vision would eventually
have forced a common substrate; the only real choice was **which one and how validated**.
Genre precedent: **Super Smash Bros.** — franchises are not simulated in their own physics;
every character is converted into one physics engine with franchise-flavored kits. That is
why the crossover feels fair. GD's substrate wins the seat because it is the only lane with
a **live oracle** (offline console: spawn / PlayStats / LogData / anger overlay /
contamination-free custom-game container — established T8/T9, 2026-07-24/25).

## 3. The three-layer decomposition (the load-bearing structure)

| Layer | What it is | Per-game? | Source / validation |
|---|---|---|---|
| **1 — Player kit** | The character: stats, skills, damage math | **YES — mandatory per game** (no D2 Sorceress without it) | Conversion key per lane (G2 pattern), verified against that lane's best anchor (§4) |
| **2 — Monster statlines** | HP/damage/defense numbers per era | YES — but **data-only, cheap** | monstats.txt, `.arz` bio formulas, banked `monster_numeric` rows; no oracle needed for numbers |
| **3 — Monster AI / combat feel** | State machines, aggro, telegraphs, attack budgets, leash | **NO — built ONCE** on the GD-validated substrate; eras are parameter profiles (§5) | The GD three-goal program: census-scoped build (G1), live L0–L5 fixtures (G3) |

## 4. The two fidelity grades — a canon law

> **LAW (fidelity labeling):** *Measured fidelity* and *authored homage* are different
> claims and canon must never blur them. Every era-related artifact states its grade.

| Grade | Definition | Where it applies |
|---|---|---|
| **MEASURED** | verified against a live game oracle (fixtures, L0–L5 ladder) | GD lane only — kit key AND monster/AI substrate |
| **MODEL-VERIFIED** | verified against a maintained external model/calculator | D2 kit keys (20 years of community-documented formulas/breakpoints) · PoE1/2 kit keys (**Path of Building** — a community-maintained conversion key we validate ours against) |
| **AUTHORED** | designed for feel, data-seeded, playtest-tuned — no fidelity claim | Era profiles (§5); all non-GD monster/combat-feel |

Each lane is verified at the grade its oracle supports — PoE is online-only,
server-authoritative, consoleless: a PoE L0 trial *cannot be run*, so claiming more than
MODEL-VERIFIED there would be dishonest. Roster status per `MIGRATION-le-park-2026-07-24.md`:
LE is PARKED (fails both roster-rule disjuncts) with its reactivation trigger intact.

## 5. Era profiles (Q2 mechanics)

An era profile = **a parameter dial-set + statline scaling on the validated substrate.**
Profiles turn dials (`ViewDistance`, `numAttackSlots`, `EmoteBeforePursuingChance`, leash
radii, telegraph beats, pack size/composition, resist textures, on-death payload rates…);
they **never fork the state machine** — that is what keeps the GD validation covering every
era. Two disciplines make profiles rigorous instead of vibes:

1. **Data-seeded:** dial values are seeded from the era's real data where held (D2 monstats
   carries AI delays, velocities, pack compositions) — then feel-tuned in playtest.
2. **Signature-feel checklist:** before authoring, each era names its **3–5 signature feel
   elements** (e.g. D2: immunity walls forcing build diversity, big dumb relentless packs;
   PoE: dense fast low-HP screens, on-death punishment) and checks them against the
   substrate's parameter space. Gaps become **small targeted build items**, never join
   programs.

Illustrative (NOT ratified dial values): **D2 era** — larger packs, straight-line pursuit,
no telegraphs, high attack-slot budgets, immunity-flavored resists · **PoE era** — dense
fast low-HP packs, on-death payloads, sharp burst telegraphs · **GD era** — the baseline,
as measured.

## 6. What this changes for the GD three-goal program

**Nothing in the six grill forks changes; the program's stakes RISE:** the substrate being
built and validated is now *every era's* substrate. Specifically:

- **G-2(a)** (player-side corpus = GD-lane kits, ruled 2026-07-25 same session) is the
  **on-ramp**, not a limit: when D2/PoE kits enter the eras roster, their P-side attested
  mechanisms re-enter the build queue via the census re-entry tags — informed by their
  lane's anchors, not built blind now. The census principle stays **per-program**.
- **G-3 hard-CC**: whatever payload is ruled becomes the control archetype's payload in
  every era.
- **G-5 key-domain rulings** become the template for future D2/PoE conversion keys —
  which are now **Layer-1-only programs** (no behavior lane), an order of magnitude
  cheaper than the GD program.

## 7. Open forks — named so nothing haunts (deferred, non-blocking)

| Fork | Question | Re-entry trigger |
|---|---|---|
| **E-1 Cross-era power normalization** | What does level-90-PoE vs level-99-D2 mean in one arena? (Anchor candidates: normalized-TTK-vs-reference-monsters, percentile-within-lane) | First cross-era arena design session; gates nothing before it |
| **E-2 Per-era signature-feel checklists** | The 3–5 elements per era + parameter-space coverage check (§5.2) | First era-profile authoring session (after GD program's L0-CLOSE) |

## 8. Thematic ratification

This is the version *Reap. Die. Rise.*'s own fiction wants: the spirit crosses the ages;
the underworld is one road wearing era-masks. The characters are faithfully reincarnated —
the world stays one world. The player-visible fantasy of the original vision survives
intact; only the machinery beneath it got honest.

**Consumers:** gamora (substrate build + era-profile dials) · gandalf (era-profile design,
signature-feel checklists) · elrond (per-lane anchor curation; fixture bank) · rocket
(kit-emission interactions at key boundaries) · jack-ryan (fidelity-grade labeling at
Gate 1/2) · knight-rider (sequencing: GD program first, Layer-1 key programs after).
