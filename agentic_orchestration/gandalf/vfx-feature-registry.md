# VFX Feature-Family Registry — governed audit-key

> ## ⛔ ONE-WAY MEMBRANE — READ THIS BEFORE CITING THIS DOCUMENT ANYWHERE
>
> **This registry is NEVER included in, quoted to, summarized for, or hinted at within any blind-extraction or blind-judge context.** It is consumed ONLY by: (a) the conductor's coverage audit, post-extraction; (b) the SPEC step, post-extraction, as implementation precedent; (c) per-skill measurement-probe derivation. Feeding it forward into extraction is the exact defect this document's governance exists to prevent — a checklist from prior exemplars pre-imposes a taxonomy on new skills (Discipline #41 shape; Matt's bias ruling 2026-08-25: *"otherwise we build a skill that can make a whirlwind, not a skill that can faithfully render any skill from a video"*).

**Born:** 2026-08-25, VFX-DEPTH run charter R-14 (Matt-ratified: a *"growing list of feature families that we design, codify and govern with rules for induction"*).
**Proposer/maintainer:** gandalf. **Ratifier:** jack-ryan (governance per `canonical-doc-format.md § 6.7`). **Matt veto-open** on every row.
**Companion:** the Layer-1 medium protocol (lives in the VFX-TWIN-DEV skill when frozen; until then, in the lap briefs). Families live HERE; attention-dimensions live THERE; the two never merge.

---

## § 1 — Rules for induction

| # | Rule |
|---|---|
| **I-1 ENTRY** | A candidate family enters when a **blind pass surfaces a residual** — a phenomenon not describable by any existing family — with evidence frames named. Entry status: **PROVISIONAL**. Conductor drafts the row; no family enters from theory alone. |
| **I-2 PROMOTION** | PROVISIONAL → **ESTABLISHED** when observed in **≥2 skills of different archetypes**, OR when **Matt's eye names it** (the owner's eye is an instrument of record). |
| **I-3 PHRASING LAW** | Families are phrased as **element-agnostic, archetype-agnostic PRINCIPLES** (Tier-1 law: the heat ramp is fire's *instance*; the principle is the intensity gradient). **Litmus: the definition must read sensibly for a healing aura, a laser beam, and a ground slam.** Content-specific phrasings are rejected at entry. |
| **I-4 MERGE/SPLIT** | Families that always co-occur or describe one phenomenon at two scales MERGE; a family doing double duty SPLITS. Conductor proposes; ratifier rules. |
| **I-5 RETIREMENT** | A single-exemplar family that never recurs may be demoted to its exemplar's per-skill notes. Retirement is recorded, not deleted — lineage stays. |
| **I-6 PROTOCOL FEEDBACK** | A family may motivate a Layer-1 protocol amendment, but the amendment must be an **ATTENTION DIMENSION** (*"characterize any changes to the ground plane during and after the effect"*), never **EXPECTED CONTENT** (*"look for scar decals"*). Same litmus as I-3. |

## § 2 — Families

Seeded 2026-08-25 from the whirlwind answer-key case (Matt's HITL frame at 3×, Matt's exemplar rulings, galadriel's forensics). These eight are the **audit key for validation case 1**: the blind method must REDISCOVER them; they are checked *against* the blind sweep (#72's labelled-expectation pattern), never fed into it.

| ID | Family (principle) | Definition | Evidence (exemplars) | Detection route | Status |
|---|---|---|---|---|---|
| FF-01 | **Leading-edge intensity apex** | The effect's brightest/most-saturated point rides its leading edge or point of action | whirlwind HITL (hot white-yellow head; Matt frame 3×) | intensity-field peak tracking vs motion direction | ESTABLISHED (Matt's eye) |
| FF-02 | **Intensity gradient along extent** | Monotonic falloff from apex to trailing extent | whirlwind HITL (head → deep-red tail) | per-arc colour/intensity profile | ESTABLISHED (Matt's eye) |
| FF-03 | **Cross-section variation** | Width/thickness varies along the form and over time — never a uniform stroke | whirlwind HITL | silhouette width profile over time | ESTABLISHED (Matt's eye) |
| FF-04 | **Particulate shedding** | Discrete quanta emitted off the primary form (count, size spread, lifetime, shed direction) | whirlwind HITL (spark shedding) | connected-component census per frame | ESTABLISHED (Matt's eye) |
| FF-05 | **Volumetric embedding** | Primary form sits inside a participating medium (smoke/dust/mist) rather than on clean air | whirlwind HITL (layered smoke volume) | opacity/texture band analysis around the form | ESTABLISHED (Matt's eye) |
| FF-06 | **Environment response** | The effect alters or appears to alter the world: surface distort, dust rise, persistent marks, **brief impact-moment distortion field** | D4 Hammer of the Ancients (ground distort + dust); PoE Demonic Leap (persistent cracks + touchdown distortion flash — Matt's eye, Q5 addenda) | environment-band differencing pre/during/post; impact-frame residuals (a few-frame flash washes out of whole-clip averages — check impact frames) | ESTABLISHED (Matt's eye, 2 archetypes) |
| FF-07 | **Camera somatic response** | Screen-shake/quake — camera-layer impulse coupled to effect events; pixels move because the *viewer* is shaken | Matt's eye (Q5 second addendum: *"We cannot miss these elements!"*) | affine camera-model translation/divergence spikes at event frames; must be modeled by (not defeated by) the pan-null | PROVISIONAL (1 named case; Matt's eye — promotes on second archetype) |
| FF-08 | **Temporal texture** | Event timing is irregular — organic, anti-metronomic; regularity reads as mechanical | galadriel forensics: references CV(interval) 1.107 vs ours 0.102 (spectral tone 2,148× median); lap-1 blind passes reproduced qualitatively (X-1 #7, X-2 #9) | event-interval CV + spectral tone; trip-flag law: CV<0.25 + single tone >1000× median → inspect, never auto-pass | ESTABLISHED (measured across reference corpus) |
| FF-09 | **Recipient state response** | Actors receiving the effect visibly change state — reaction motion, stagger, collapse, terminal state, or recovery | whirlwind reference (lap-1 blind: X-1 rank #1 "enemies burn, collapse, die"; X-2 dim 8 + rank #1); litmus: aura=recovery posture/glow, laser=stagger/scorch, slam=knockdown | actor-region pose/state differencing across effect contact | PROVISIONAL (I-1; both blind passes rank #1) |
| FF-10 | **Effect transfer & attached persistence** | A portion of the effect transfers from the delivery form to recipients/surfaces and persists there with its own lifecycle, outliving the delivery | whirlwind reference (X-2 rank #1 "the reference effect is *on the victims*"; X-1 ember-orb residual, ~5 s post-flame); litmus: aura=lingering regen glow, laser=glowing burn point, slam=debris on targets | per-actor attached-emission tracking post-contact; lifetime census | PROVISIONAL (I-1; I-4 note: split from FF-06 — world-surface vs actor-attached) |
| FF-11 | **Lifecycle phase structure** | The effect passes through visually distinct phases (anticipation / onset accent / sustain / decay / aftermath) rather than one state plus an alpha fade | whirlwind reference (X-1 #7 + flash-halo residual = onset-accent instance; X-2 #3 "degrades through states"); distinct from FF-08 (interval irregularity vs macro state-sequence); litmus: aura bloom-sustain-fade, laser charge-fire-cooldown, slam windup-impact-settle | phase segmentation of effect-region statistics over lifetime | PROVISIONAL (I-1) |
| FF-12 | **Effect-driven illumination** | The effect behaves as a light source — luminance exceeding local ambient, casting light onto nearby actors and surfaces | whirlwind reference (X-1 #6 "never exceeds scene luminance, so it fails to read as energetic"; X-2 dim 4); litmus: aura lights the caster, laser lights its path, slam flash lights the dust | ambient-vs-effect luminance ratio; cast-light differencing on adjacent surfaces | PROVISIONAL (I-1) |

## § 3 — Audit-key datasets (quarantined with this document)

- **W-E1 per-skill matrix** — **LANDED 2026-08-25**: `agentic_orchestration/galadriel/notes/2026-08-25-vfx-depth-feature-matrix-ta.md` (quarantine-stamped at the file head; charter R-17a). Seven-family presence matrix, 26 reference legs + 6 ours. RE-ROLED by charter R-12: audit-key data, never extraction input. **Caveats binding on any consumer:** F4/F5 columns are vacuous (P on 30/32, 27/32 — no bar may be built on them); five operators disqualified by their own controls pre-landing (`f29b7faf`, preregistration checkable in git).
- **FF-08 amendment CANDIDATE (pending jack-ryan, I-6/I-4 governance):** W-E1 measured an UNDER-FIRE of the trip-flag law — `OURS_blink` at CV *exactly* 0.000 escaped the trip by missing the spectral-tone condition by 5.5%. Candidate refinement: CV = 0.000 exactly (a metronome, not merely regular) trips on its own, without the tone conjunct. Evidence: W-E1 matrix § trip rows. Not yet law.
- **Matt eye-words log** — every Matt gate-verdict, verbatim, becomes both judge-calibration data (R-13) and coverage-audit input. Banked at founding: CP#1 *"#1 is far superior to #2 and #3."*

---

- **Lap-1 coverage audit — LANDED 2026-08-25:** `agentic_orchestration/gandalf/vfx-depth-run/lap1-coverage-audit.md` (charter R-20). Validation case 1 PASS: 7/7 applicable families rediscovered by both blind passes + FF-07 true-negatived; the R-19b quarantined colour-register inversion independently discovered by X-2; four residual candidates inducted (FF-09..FF-12, PROVISIONAL). Layer-1 protocol amendment A-1 (contrast-relationship attention dimension) recorded there for the lap-2 brief.

---

**Change log:** 2026-08-25 founded (gandalf, RUN-CONDUCTOR); jack-ryan ratification queued. · 2026-08-25 lap-1 audit: FF-09..FF-12 entered PROVISIONAL per I-1 (blind-residual entry, evidence frames in pass logs); FF-08 evidence column gains lap-1 qualitative reproduction; ratification bundle to jack-ryan now = {FF-08 trip-law refinement, FF-09..FF-12, FF-10/FF-06 split ruling}.
