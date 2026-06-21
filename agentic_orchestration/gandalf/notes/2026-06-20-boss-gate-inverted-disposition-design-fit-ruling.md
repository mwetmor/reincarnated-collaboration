# Boss-gate inverted-disposition — design-fit ruling (the §5a falsification)

**Type:** gandalf design-fit ruling on a BUILT + Gate-2'd production-gate change, ahead of a Matt approval halt.
**Date:** 2026-06-20
**Author:** gandalf (story-and-design steward)
**Requested by:** knight-rider (instrument-validity workstream; boss-half of the Phase-5 refit).
**Verdict in one line:** the gate is sound and APPROVABLE, **but NOT clean as-reported.** STR's 1.000-flat is a true-and-finally-measured capability (approve it). The caster "drop" headline is a MISREAD of the data — it is not an armor-wall texture, it is a **`mini_boss` categorical cliff** that is a candidate INSTRUMENT DEFECT and must be a named caveat on the halt, not shipped silently as "casters should struggle."

**Read first / composes with:** my boss-gate spec (`gandalf/requests/2026-06-20-boss-gate-implementation-spec.md` §3 the falsified expectation); the doctrine spine §5/§5a (`gandalf/notes/2026-06-19-encounter-measurement-doctrine-spine.md`); gamora math-note §10 (`reincarnated-engine/.../math/boss-gate-2026-06-20.md`); jack-ryan Gate-2 (`qa/findings/2026-06-20-boss-gate-gate2.md`); verification JSON (`cycle-14-wave-5-season-001/boss-gate-verification-2026-06-20.json`).

**Evidence I verified FIRST-HAND (not on report):** I read the 1440-cell verification JSON directly and broke the boss cells down by attribute × shell × cohort. The pooled headline numbers KR was handed (int 0.992→0.750, wis 0.984→0.716) are real averages but they POOL ACROSS SHELLS and hide the actual structure. The structure is the ruling.

---

## The data the pooled headline hides (this is the load-bearing finding)

Boss survive+kill, **split by shell** (720 boss cells; I computed this from the JSON, it is not in the handoff table):

| attr | `boss_with_adds` | `mini_boss` | shape |
|---|---|---|---|
| **str** | **1.000** (n=81, min=max=1.0) | **1.000** (n=27, min=max=1.0) | flat pass everywhere |
| dex | 1.000 (n=81) | 0.667 (n=27, min 0.0 max 1.0) | thin mini_boss margin |
| **int** | **1.000** (n=108) | **0.000** (n=36, EVERY cell, EVERY cohort) | **categorical cliff** |
| **wis** | **0.955** (n=210) | **0.000** (n=90, EVERY cell, EVERY cohort) | **categorical cliff** |

The caster "drop from 0.99 to 0.72" is **not a graded magnitude texture.** It is: casters PASS `boss_with_adds` at ~0.95–1.000 and FAIL `mini_boss` at a flat **0.000 across all 36/90 cells and all three cohorts present.** A 1.000→0.000 step at a shell boundary, uniform across cohorts, is the signature of a **shell-specific structural mismatch (mini_boss HP / timer / scaling / win-condition wiring)** — NOT the signature of "casters eat an armor wall." An armor-wall texture produces a gradient (some kills slower, some fail); a structural mismatch produces a categorical wipe on one shell. This is the latter.

And the tell that makes it a flag rather than identity: **STR is the ONLY attribute that clears `mini_boss` (1.000 flat).** int and wis wipe at 0.000; dex sits at 0.667. If `mini_boss` had become a legitimately harder single-target armored check, STR — the melee with the *weakest* §5a single-target story — would be the LAST to pass it, not the only one to pass it flat. STR passing where the casters categorically fail, on a shell the casters dominate in `boss_with_adds`, is upside-down. Something about `mini_boss` is interacting with the caster damage path in a way that is almost certainly an instrument artifact, not a class-fantasy outcome.

---

## RULINGS (1–4)

### 1. Is the inverted disposition the honest read, or a remaining instrument defect? — SPLIT VERDICT.

**STR 1.000 — HONEST, approve it. NOT a 600@0.3s-style artifact.** I applied the exact saturation skepticism I applied to the timing-floor, and STR survives it:
- The 600@0.3s floor was suspicious because it was a *flat predicate value with no underlying variance* — every cell pinned to the same number because the instrument couldn't see below the floor.
- STR here is the opposite: survival is 1.000 flat **but `tier_2_kpm` VARIES 8.09→12.10** across the cells. The fights resolve *differently* (different kill speeds) and all resolve in a kill. That is a real, repeatable capability hitting its outcome, not an inert predicate pinning to a default. The kills are fast (KPM 8–12, well above the old 3.78 ceiling the doctrine correctly removed). This is the instrument-validity workstream doing precisely its job: the contaminated pre-composed instrument was LYING about STR (fake KPM-reject crater); the composed instrument now shows STR's real rage-economy + rotation focus-firing the boss. **Approve STR's boss-shell pass as a true capability finally measured.** The 1.000-UNIFORMITY (every cohort) is worth one downstream sanity check (below), but it is not disqualifying — STR's whole §5a story was "the lever exists, it just wasn't wired"; Phase R wired it.

**Caster mini_boss 0.000 — candidate DEFECT, do not approve as identity.** The categorical 1.000→0.000 cliff on one shell, uniform across cohorts, with STR uniquely surviving it, is the honest read of a *broken or mis-scaled mini_boss interaction*, not the honest read of caster boss-soloing. This needs a targeted look before it is ratified as "casters struggle on mini_boss."

### 2. The caster drop — identity or defect? — DEFECT (or at minimum, UNDIAGNOSED; not approvable as identity).

It is NOT the intended Phase-4 armor-wall texture. Three reasons, all from the cell data:
- **Wrong shape.** Identity-texture is graded; this is categorical (flat 0.000 on every mini_boss cell).
- **Wrong shell selectivity.** Casters are NEAR-PERFECT on `boss_with_adds` (the *harder* multi-target shell) and ZERO on `mini_boss` (a single mini-boss). If the cause were "casters can't out-damage single-target armor," `boss_with_adds` — which also has a high-HP anchor — would show the same erosion. It does not. The cause is specific to `mini_boss`, which points at that shell's config (HP/timer/scaling/`mini_boss_killed` win-condition wiring), not at caster damage generally.
- **Wrong winner.** STR clears mini_boss flat while casters wipe. There is no class-fantasy world in which the melee with the documented single-target-allocation weakness (§5a) is the only archetype that can solo the mini-boss while the burst casters categorically cannot. That inversion is the artifact's fingerprint.

The magnitude IS the flag. A drop of "int 0.99→0.75" sounds like texture; the truth ("int 1.0 on one shell, 0.0 on the other") is a cliff that texture does not produce.

### 3. What this does to Phase 6's (A)-vs-(B) STR read — SUBSTANTIALLY ANSWERED for the as-is lever; Read-2/anchor-rescale REFRAMED, not dissolved.

My §5a premise ("STR fails boss shells → ships via the clear floor") is **inverted, and that is the workstream's win, not its failure.** The composed instrument resolved the §5a anchor-gap *on its own*: §5a recommended a focus-fire LEVER (bleed DoT) to convert STR's anchor-gap from wall to choice; rocket confirms bleed is STILL inert in the population (2026-06-20), yet STR now ships boss shells anyway — because the **rotation/economy (Phase R) IS the focus-fire lever.** STR builds rage on the adds and spends it on the anchor. That is the §5a lever, delivered by a different mechanism than predicted.

Consequences for Phase 6:
- **Read-1 (STR encounter-segregated, as-is lever):** substantially ANSWERED. STR ships boss shells on the as-is composed lever. The "route-via-floor because STR can't boss-solo" disposition is OBSOLETE — STR can boss-solo on the composed instrument. Read-1 becomes a *confirmation* read, not an open question.
- **Read-2 (mixed-pack focus-fire, the definitive (A)-vs-(B)):** REFRAMED. The original (A) "STR is fine, just KPM-rejected" vs (B) "STR has a real anchor-gap needing a kit-fix" dichotomy is collapsed by the data toward (A)-plus: STR is fine AND the lever it needed is now active via economy/rotation. The anchor-predicate-rescale (Read-2) **still matters but its STAKES dropped** — it is no longer gating whether STR *ships*; it is now a tuning/texture question (does the rotation-driven focus-fire produce the *right-feeling* engagement, or is it too automatic?). Do NOT cancel the anchor-rescale; downgrade it from "shipping-blocker" to "texture-tuning, post-halt."
- **Net:** Phase 6 still asks a question, but a smaller and better one: not "can STR boss-solo at all" (answered: yes) but "is STR's now-automatic focus-fire the *player-agency* version §5a wanted, or did the economy make the lever fire without the player choosing it?" That is a real design question for later, not a halt-blocker.

### 4. §5a / doctrine update + Matt-approvability.

**§5a needs amending — its prediction is falsified, and that must be recorded, not buried.** The amendment is NOT "§5a was wrong"; it is "§5a's premise (STR fails boss shells) held on the pre-composed instrument and was INVERTED by the composed instrument, which delivered §5a's own recommended focus-fire lever via rotation/economy rather than DoT." That is the discipline working: a pre-registered prediction, falsified by named substrate changes, surfaced not smoothed. I will amend the spine §5a with a dated falsification stamp pointing at this note. **Empirical criterion that gates the amendment as final: the mini_boss caster cliff is diagnosed** (see below) — because if the cliff is a defect, the composed instrument is not yet fully honest, and §5a's *new* reading ("STR ships boss shells") is only half-trustworthy until we know the caster numbers aren't also contaminated.

**Is the boss-gate disposition Matt-approvable as-is? — APPROVABLE WITH ONE NAMED CAVEAT, not clean.**
- **The GATE is approvable, full stop.** jack-ryan's Gate-2 PASS-WITH-INFO is correct: the wiring is mechanically sound, boss-only scoped, no clear-shell regression, DPS/TTK measure-not-gate. The win-condition split is built correctly. Approve the gate mechanism.
- **The DISPOSITION the gate produces is approvable for STR and `boss_with_adds`, but the caster `mini_boss` 0.000 cliff is a CAVEAT that must travel WITH the approval.** Matt should approve the gate AND the STR finding, while explicitly holding the caster-mini_boss result as "flagged for diagnosis, not ratified as identity." Shipping the pooled "casters dropped to 0.72" framing without the shell-split would be the instrument lying again — the exact failure mode this workstream exists to kill.

---

## What I recommend KR put in the decisions-log draft + the Matt halt

**Decisions-log draft (KR drafts / jack-ryan reviews):**
- Record: the boss-shell win-condition split is BUILT and Gate-2-sound (survive-and-kill replaces the boss KPM band; DPS/TTK measured, never gates; no over-performance ceiling). This implements the §1/§6 doctrine (Matt-ADOPTED 2026-06-19).
- Record: the build FALSIFIED the spec §3 / spine §5a pre-registered expectation (STR-timeout=1.000). Under the composed instrument STR SHIPS boss shells at 1.000 — the §5a-predicted focus-fire lever is active via Phase-R rotation/economy, NOT DoT (rocket 2026-06-20: bleed still inert in population). This is a pre-registered prediction honestly falsified by named substrate changes — discipline working as designed, NOT a regression.
- Record: the caster pooled-drop headline (int 0.992→0.750, wis 0.984→0.716) is a SHELL-POOLING ARTIFACT. The true structure is a `mini_boss` categorical cliff (casters 1.0 on boss_with_adds, 0.0 on mini_boss, uniform across cohorts; STR uniquely clears mini_boss). Flagged as a candidate instrument defect pending diagnosis; NOT ratified as caster identity.

**Matt halt (the framing — concise):**
> The boss-gate is built and sound (jack-ryan PASS). It produced a design surprise: STR now ships boss shells (it was predicted to fail) — this is the instrument-validity work paying off, the composed instrument finally measuring STR's real focus-fire capability that the old instrument hid. Approve the gate + the STR finding. **One caveat to hold, not approve blind:** the casters' apparent "drop" is, on the cell data, a clean mini_boss-only cliff (perfect on the other boss shell, zero on mini_boss, and STR is the only class that clears mini_boss) — that shape is an instrument defect signature, not "casters struggle on bosses." Recommend approving the gate-and-STR-disposition while authorizing a short targeted diagnosis of the mini_boss caster wipe before the caster boss numbers are treated as truth.

**The diagnosis I recommend (cheap, targeted — for KR to sequence to gamora/rocket, post-approval):**
- Pull 2–3 caster `mini_boss` cells that read 0.000 and one STR `mini_boss` cell that reads 1.000; inspect WHY the caster fights end `winner=timeout` and the STR ones end `winner=player`. Specifically check: (i) the `mini_boss` scenario's `mini_boss_killed` win-condition wiring vs `boss_killed` (the two shells use different win-conditions per arena.py §1.2 of gamora's note — a wiring asymmetry there would produce exactly this cliff); (ii) mini_boss HP/armor/resist scaling vs caster damage path post-Phase-4-symmetry; (iii) whether the caster `mini_boss` timeouts are actually killing the mini-boss but failing a survive/add-clear sub-condition. The empirical criterion that closes the flag: a first-hand explanation of why STR clears mini_boss and casters categorically cannot, that is either (a) a real, defensible difficulty texture, or (b) a fixable instrument/scenario defect.

**Bottom line for KR:** approve the gate + STR; caveat the casters; one cheap mini_boss diagnosis closes the loop. Do not let the pooled "casters dropped" number ship as identity — the shell-split says it is a cliff, and cliffs are bugs until proven to be design.

---

**Signed:** gandalf, 2026-06-20. The instrument stopped lying about STR — that is the win, approve it. But it may have started lying about casters on one shell; the pooled average hid a categorical cliff, and a cliff where the melee out-solos the burst-casters on the single-target mini-boss is upside-down until someone proves otherwise. Honest measurement is the whole point of this workstream; finish it honest.
