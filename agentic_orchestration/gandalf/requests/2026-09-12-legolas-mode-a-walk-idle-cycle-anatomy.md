# Request → legolas (Mode A, analytical research) — R10: walk & idle cycle anatomy for painted-2D ARPG sprites

> **From:** gandalf (RUN-CONDUCTOR, Run C-1) · **Date:** 2026-09-12 · **Occasioned by:** Matt's K3 first-loop review (HITL run): the idle chest breathes but head/eyes drift; the walk's staff arm is rigid, the eyes dart frame to frame, the head keeps its idle tilt and does not bob/sway with weight transfer. Every frame is a fresh render — anything the prompt does not pin drifts. We need the *rules* that make a cycle read as a cycle, as measurable gates and judge questions.
> **Outside the run** (charter § 1: legolas research only); findings fold into SPEC § 6 T1 (`gait_oracle.py`, `pose_guide.py`, `visibility_table.py`) and the JUDGE question sets.

## Questions (each answered with a graded source and, where possible, a number)

1. **The walk cycle, frame by frame.** The canonical 8-frame in-place walk (Williams: contact / down / passing / up — two per half-cycle): per-frame rules for (a) the planted sole (which foot, where, for how many frames), (b) the vertical body bob (amplitude as a fraction of body height; phase: lowest at down, highest at up), (c) lateral head sway with weight transfer (amplitude, phase), (d) arm counter-swing (phase opposite the same-side leg; amplitude), (e) **weapon-arm behaviour when carrying a staff/polearm upright** — reduced swing vs a rhythmic plant (which do Diablo II's staff classes, Hades, PoE, Grim Dawn do, and at what frame counts?), (f) gaze: locked on the path ahead — does any shipped ARPG animate eyes in a walk?
2. **The idle, frame by frame.** What a base idle contains in shipped ARPGs (D2 NU stance, D3/D4, PoE, Hades, Last Epoch): breath period (seconds) and amplitude (px at what sprite height), what is locked (head, feet, eyes, weapon hand), and how fidget/look-around variants are handled (separate clips, trigger cadence). Frame counts and fps actually used.
3. **QA practice.** How studios check cycles: onion-skin / overlay tests, "the moonwalk test" (foot slip), silhouette-arc tests, the loop-closure pop test, motion-path smoothness. Which are closed-form (we compute from masks/frames) vs judge-only.
4. **Direction and camera.** For an elevated three-quarter camera (projection C): which direction best exposes the stride for QA (profile E/W?), and how the bob/sway rules change per facing.
5. **Deliverable shape:** a table of *gate candidates* — rule · measurable quantity · threshold or range · what input it needs (masks / sole line / head centroid) — and a list of *judge questions* (DSG-shaped, atomic) for the cycles. Mark each VERIFIED / SECONDARY / PRACTITIONER-REPORT per your grading key.

## What NOT to do
No tooling, no code, no prompts. Do not read the burst lane's runs/ or briefs/. Two passes per gap, then record the gap.

— gandalf, 2026-09-12

## R10b — the ORACLE artifacts (Matt 2026-09-12: "We do need to find an oracle… send Legolas out to find an idle and walking video and a companion sprite sheet in the painted style")

Find and grade, with licence and provenance recorded for each:
1. **A frame-accurate walk + idle reference for measurement** — first choice **Eadweard Muybridge's locomotion plates** (public domain; a woman walking, standing), highest-resolution scans available; plus Williams / Blair phase charts. Deliver the plate references and, if a clean scan is obtainable, the per-frame measurements: head-top y, hip y, each sole's x/y (planted vs swinging), shoulder/arm angle — normalised to body height, tabulated against the canonical phase (contact / down / passing / up).
2. **A painted-register sprite sheet with idle AND walk (elevated three-quarter view preferred) and a video/GIF of it looping** — for how a painted cycle at 8–12 frames distributes motion and what stays locked. Prefer CC0 / CC-BY sources (OpenGameArt et al.) that could be registered with provenance; shipped-game sheets (D2-class) are MEASUREMENT-ONLY references, never lane inputs.
3. **Derivations:** (a) a per-phase foot/sole table → our own numbered-foot pose guide (first-party by construction); (b) threshold RANGES for the T1 gait gates (vertical bob amplitude, lateral head sway, arm counter-swing amplitude incl. the reduced weapon-arm case, planted-sole slip tolerance, breath amplitude/period for idle); (c) the DSG-shaped judge questions for a cycle.

**Provenance rule (unchanged, restated):** third-party pixels never condition a mint (`lane/ref_provenance.py`). Whether a licensed reference may serve as a JUDGE ANCHOR (not a generation reference) is a refinement for Matt's ruling — list the candidate and its licence; do not assume.
