# Dispatch — 2026-09-26 — gandalf — Run C-9: Illuminated Archive STYLE GATE

**From:** Matt's session (drafted with Claude, standing in for knight-rider)
**To:** gandalf (RUN-CONDUCTOR)
**Approved by:** Matt, 2026-09-26: *"Ok, go."*
**Estimated effort:** one HITL session. About 8 GENERATE images plus CHECK and JUDGE bursts. Cap: 16 images.
**Acceptance:** Matt rules GO, ITERATE or ADD-ASTRA-ARM on a side-by-side packet (below). Nothing downstream fires before that ruling.

## Context

Matt is testing a challenger register, **ART-1 "Illuminated Archive"**: medieval and early-Renaissance painted-book **subjects** (characters and scenes) rendered in **FFT-watercolor technique**. Neither source has ever lived in a game: FFT watercolor was only portraits and cinematics, and the painted-book scenes were never places. The painted book supplies subject, composition, iconography and palette; FFT supplies the rendering (wash handling, pale highlights, ink and hatching, uneven wash).

The full plan is a 2×2 A/B (cliffside and cathedral, each in H1 and in Illuminated), then a playtest with a style toggle. **This dispatch is only step 1, the style gate:** can Astra produce the merge at all? The FFT references may never be attached, so the FFT half must come from **text alone**.

## Required reading

1. `matt_notes_handoff_docs/rdr-art-illuminated-archive-brief.md`: the brief. **Where it conflicts with the refs README, the README governs** (Matt's rulings of 2026-09-26).
2. `matt_notes_handoff_docs/rdr-art-illuminated-archive-refs/README.md`: picks, the merge rule, the arena→cathedral mapping.
3. `…/rdr-art-illuminated-archive-refs/metrics-2026-09-26.md` (revision 2 with corrections): figure band, scene rule, line question, caveats.
4. `…/rdr-art-illuminated-archive-refs/ledger.jsonl`: **only rows with `attach_to_generator: true` may be passed to a burst.** The FFT Steam frames and the FFTA page are `false`: copyrighted, look-only. They must never enter a brief, a workdir or an `-i`.
5. `canonical/reap-die-rise-game/painted-2d-pipeline/00-system.md` and `mechanical-process.md` (lane invariants), and `scene-builder-workflow.md` § 3 (camera grammar, style-anchor mechanism).

## Rulings from Matt, 2026-09-26, to carry into the charter

- **Characters:** A = **the Keeper** (H1; Matt's favourite animation). B = **the Lalaing knight**: Getty Ms. 114 fol. 129v, the right-hand knight, **skirt removed** (tabard to the hip, plate legs as on fol. 123's right-hand knight), **poleaxe**. **The EoR Warlord is dropped** (Matt: unhappy with it in the chibi style).
- **Cathedral:** the Belles Heures Office of the Dead choir is the **style** anchor; Spinola Hours fol. 185 is **architecture only** (vault, height, details); **Antwerp Cathedral** is the building, laid over the **Crucible arena** footprint (drax builds the grey room in parallel: see the companion dispatch).
- **Cliffside scenery:** *Très Riches Heures* calendar (June meadow and Sainte-Chapelle; July bridge; September Saumur as the Keeper's-domain tower castle; March valley; August hills; May forest), plus Belles Heures meadow, forest and tower castle. Scenery and horizons, not cliffs.
- **Brief amendments:**
  - (a) Pigment: **rich mineral colour at a moderate value, vivid only on accents; the floor stays calm.** This replaces "faded everywhere".
  - (b) **The hatching rule is suspended.** FFT shades with hatching; it becomes a variable in the later imperfection test.
  - (c) Imperfection is **designed, not random** (a three-way test later: clean / carried by the video model / designed boil at 8–12 fps).
  - (d) Background: `#00ff00`, not the brief's magenta.

## Scope

- [ ] **Charter C-9** (small; ARCHITECT gate per your OP). Register card variant `REGISTER_CARD_ILLUMINATED` rendered through `render_brief.py`; **no hand-written prompts.** The brief's § 10 texts are input to the card, not prompts.
- [ ] **Pre-flight:** H-C7-1 (Codex usage limit) is still OPEN. The reset date (Sep 22) has passed. Confirm the quota with the first burst; if it is still exhausted, HALT and route to Matt. Grok is **not** used in this gate.
- [ ] **Texture patches (conductor):** cut two or three crops from `cathedral-look/belles-heures-office-of-the-dead-choir-detail.jpg` (1800×2400) showing the tempera and vellum surface. Ledger them as derived rows with `attach_to_generator: true`.
- [ ] **(a) Scene arm: re-paint the chunk that set the current register.** Geometry guide = `astra_test_01/burst/runs/C-3/artifacts/CS-guides/chunk_A_guide.png` (the exact guide `chunk_A` was painted from). Attach: the guide; TRH July and June (palette and composition only); one texture patch. **Scale figure: a flat grey silhouette at the Keeper's 130 px, not `keeper_rest_S.png`**, which would import H1. FFT treatment in text. **Two line arms:** FFT near-black ink vs the painted book's lifted, warm line. Two images per arm.
- [ ] **(b) Character arm: the knight master still.** Subject = `character/lalaing-f129v-knight-PRIMARY.jpg` plus the fol. 123 no-skirt reference; facing south-east in the ratified camera (yaw 47°, pitch 52.95°); flat `#00ff00`; FFT treatment in text; the same two line arms; two images per arm.
- [ ] **CHECK and JUDGE through the lane:** the O1 palette oracle against the metrics bands (figure: L\* 95th ≈ 83–92, dark ink allowed; scene: painted-book palette, walkable floor brightest and calmest); JUDGE with a known-bad control.
- [ ] **Milestone packet** (`review.html`, Desktop): the merged chunk beside `chunk_A`, and the knight beside the Keeper; each **at game scale** (the chunk at its in-game crop; the knight at 130 px) **and** at full size; the numbers alongside.
- [ ] **Matt's ruling:** GO (the full cliffside and cathedral runs follow) / ITERATE (text changes) / ADD-ASTRA-ARM (re-run with one of Matt's two Astra FFT-pole images attached: the moth mage or the landscape, from his 2026-09-26 session).
- [ ] **KC2-PLAY record:** log against KC2-PLAY that the EoR Warlord player body (KP-50) is superseded by Matt's 2026-09-26 statement. That run is in your seat, and per CLAUDE.md's conflict rule, a posture change is recorded against the run, not only spoken.

**Round-trip: not applicable.** No cross-seam contract change: this is lane art, not engine data.

## Out of scope

The full scene paints, the cathedral paint, Grok clips, the imperfection test and the playtest build. Each waits on Matt's GO.

## Push

Commit as work lands. **No push without Matt's word.** C-9 is not covered by a standing push pattern.
