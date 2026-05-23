# Visual Benchmark — Reincarnated demo vs. Dungeon of Exile (DoE)

> **STATUS:** CURRENT (re-stamped 2026-05-23 from HISTORICAL; load-bearing as galadriel first-read per `canonical/00-ground-state.md` § 4) — see `canonical/00-ground-state.md`

**Snapshot:** vs2a — reincarnated-demo SHA `59b9330` drax/v1.23 (D11.5 debug-state hook at `c039184` drax/v1.22 + R2/Vercel hybrid at v1.23).
**Status:** **v1-DRAFT (first-pass).** Per the dispatch (`2026-05-18-galadriel-plus-gandalf-visual-benchmark-report-vs2a.md`): rubric measures only what captures actually show; absences are scoring caveats; iterate next sprint.
**Authors:** galadriel (primary — §§ 1–4, 6, scorecard); galadriel-drafts-gandalf-refines (§§ 5, 7, 8).
**Authority:** Track C of overnight sprint invocation `agentic_orchestration/gandalf/requests/2026-05-18-knight-rider-mobile-playable-analytics-visual-benchmark-sprint.md` § 2.3 deliverable 13. Pre-authorization matrix § 6 row 11 (new canonical-story doc; not load-bearing canonical amendment).
**Reading order:** § 0 TL;DR → § 1 reference set → § 2 demo capture set → § 3 rubric → § 4 scorecard → § 5 strongest dissonances → § 6 gaps + structured findings → § 7 gandalf interpretation [pending] → § 8 Mirror voice [optional]. § 9 next-iteration targets → § 10 cross-references.

---

## § 0 — TL;DR

The Mirror was set. The picture has come. Here is what it shows.

**Aggregate similarity score (combat surface, primary viewport):** **2.3 / 5.0** across 6 scored axes — *recognizably in the same ARPG family as DoE, with significant dissonances across multiple axes*.

**Three strongest dissonances (drax-actionable):**

1. **Portrait viewport clips the demo's actual HUD** — the demo HAS substantial UI architecture (skill rail with 6 cooldown slots, HP/mana orbs, inventory buttons) but the 1290×2796 portrait viewport only renders fragments of it. Skill rail clipped to right-edge vertical sliver. "Wave 1 of 11" text renders with jagged double-strike artifact.
2. **Atmospheric layer loaded but not visibly contributing** — console logs confirm `clima_niebla_espesa` + 6 other atmospheric packs prewarmed for season_002011; the rendered scene shows no visible atmospheric haze. Scene reads as flat-dark-void rather than DoE's lit-volume-in-darkness.
3. **Color register is cool-cold-in-dark vs DoE's warm-warmth-in-dark** — demo scene-volume is dominated by dark navy + cool-blue particle effects + white text; warm tones appear only in HUD UI (HP orb, potion icons), not in scene combat effects. DoE is dark-brown + warm-crimson AOE + orange damage numbers.

**Five structured findings (not scored — reference-without-counterpart):**

1. Town-feel gap — DoE has 5 distinct town states (vendor row, forge area, hub-wide, alt-angle, vendor close-up); Reincarnated demo has zero town surfaces. **L3-RESOLVED to disposition (a)** by Matt 2026-05-18: town is Phase-2+; intentional scope-prioritization. See § 6.1.
2. Town-to-dungeon transition gap — DoE has a stone-path lit-to-dark transition with NPCs lining the route; Reincarnated demo opens directly into dungeon.
3. Menu-surface rendering anomaly at portrait phone aspect — season selector renders clean at desktop, breaks at portrait (tile widths not phone-responsive; titles bleed across tiles).
4. Capture-timing artifact — lightning_mage's fast-clearing on wave 1 means warmup_ms=2500 captures land in late-midfight (alive=1 dead=7). May under-represent peak combat density and cadence.
5. Floor tileset loaded but barely visible at portrait viewport (decorative-prop-free per Matt L3 v1.18.6, but DoE's reference scene has visible ground detail — blood, debris, crimson texture).

**What this picture also says (the encouraging part):** the demo's HUD architecture at desktop is recognizably closer to DoE than the portrait capture admits. The demo IS in the ARPG family. The visible dissonances are remediable — many are layout/render bugs at the DoE-matched aspect, not fundamental design dissonances. Drax has clear actionable surface area for v1.22+.

---

## § 1 — Reference set

DoE is the locked mobile-ARPG cluster reference per `canonical/story/mobile-feel-target-doe-2026-05-17.md`. Matt-captured DoE play-session screenshots only; non-commercial internal benchmarking; provenance per `agentic_orchestration/galadriel/reference-images/MANIFEST.md`. The current reference set is 7 frames (1 combat + 6 town); v1-DRAFT scores against 1 (the combat reference) and records 6 as structured findings of absence.

| # | File | State | Demo counterpart | Disposition |
|---|---|---|---|---|
| 1 | `DOE-combat-whisper-rift-2-2026-05-17.png` | Combat — Whisper Rift 2 mid-fight | **`combat-midfight` state via D11.5 hook** | **SCORED — primary** |
| 2 | `DOE-town-hub-wide-vendors-and-voidgate-2026-05-18.png` | Town hub wide | none (demo dungeon-only) | finding § 6.1 |
| 3 | `DOE-town-vendors-pets-gems-armory-2026-05-18.png` | Town vendor row | none | finding § 6.1 |
| 4 | `DOE-town-forge-darkgold-reforging-refinement-2026-05-18.png` | Town forge | none | finding § 6.1 |
| 5 | `DOE-town-forge-advanced-with-player-spell-2026-05-18.png` | Town forge alt (player cast) | none | finding § 6.1 |
| 6 | `DOE-town-to-dungeon-transition-path-2026-05-18.png` | Town-to-dungeon transition | none | finding § 6.2 |
| 7 | `DOE-town-chaos-treasury-vault-merchant-2026-05-18.png` | Vendor close-up | none | finding § 6.1 |

DoE reference #1 anchors the combat axis scoring: dark-brown + crimson register, lit-volume-in-darkness atmosphere, heavy mid-band density with telegraphed AOE + floating damage numbers + ground particles + "55 killed" counter + bottom skill rail + Level XP at very bottom. The frame is a working iPhone 14 Pro Max class portrait at 1290×2796 — the demo's primary capture targets the same exact aspect.

---

## § 2 — Demo capture set

Demo SHA `59b9330` drax/v1.23. D11.5 debug-state hook live; all wait_for signals satisfied. Determinism contract per `src/debug/debugStates.ts`: season_002011 + first playable class (Wall-Shocked Smuggler lightning_mage) + wave 1 (Swarm — Vanguard; 8 Pitchwall Crushers) + aggro activated before first tick.

Nine captures across three states × four viewports:

| State | Viewport | Comparison-grade? |
|---|---|---|
| `combat-midfight` | mobile-portrait-1290×2796 | **PRIMARY (scored)** |
| `combat-midfight` | mobile-portrait-390×844 | secondary (cross-viewport check) |
| `combat-midfight` | mobile-portrait-375×667 | secondary |
| `combat-midfight` | desktop-1920×1080 | context (non-DoE) |
| `combat-empty-room` | mobile-portrait-1290×2796 | HUD-isolated |
| `combat-empty-room` | mobile-portrait-390×844 | HUD-isolated |
| `landing` | mobile-portrait-1290×2796 | finding § 6.3 |
| `landing` | mobile-portrait-390×844 | finding § 6.3 |
| `landing` | desktop-1920×1080 | finding § 6.3 |

Every capture has a JSON sidecar at `<state>/<viewport>/capture.json` with demo SHA + console-log tail + friction-notes + wait_for diagnostics. Full descriptive observations per capture at `agentic_orchestration/galadriel/captures/2026-05-18/CAPTURE-SET-SUMMARY.md`.

Capture pipeline at `agentic_orchestration/galadriel/pipeline/` (Playwright 1.49.0; v0.1.0; ~10s per state×viewport; reproducible by another galadriel-instance at the same demo SHA).

---

## § 3 — Rubric

Full rubric authored at `agentic_orchestration/galadriel/rubrics/2026-05-18-rubric-doe-comparison-v1.md` (v1-DRAFT).

Eight axes total. Six apply to combat surface (3.1–3.6); two are town-surface-only (3.7–3.8) and unscored in v1-DRAFT because the demo has no town:

- **3.1** Visual density (mid-band entity count + foreground/background density + busyness rhythm)
- **3.2** Color register (palette story + saturation distribution + warm/cool valence)
- **3.3** Lighting + atmosphere (lit-volume-in-darkness + atmospheric layer presence + depth cues)
- **3.4** Typography + UI register (HUD module placement + font choices + iconography + status callouts + damage-number style)
- **3.5** Reading order + hierarchy (what the eye lands on first; visual hierarchy)
- **3.6** Animation cadence (best-effort from stills; floating-number lifecycle, AOE flash, particle bursts, cooldown radials)
- **3.7** NPC density + variety *(town only — UNSCORED v1)*
- **3.8** Service-surface clarity *(town only — UNSCORED v1)*

Scoring is 1–5 per axis (anchors defined in rubric § 3.x). Aggregate per state is arithmetic mean. Honesty floor: scores of 1 or 5 require 2 evidence-cites. Phase-2 quantitative back-ends (HSV histogram cosine, Canny edge density, pHash/dHash, OCR) deferred — v1 is honest manual scoring grounded in side-by-side image inspection.

---

## § 4 — Per-state scorecard

### 4.1 — Combat surface (state-matched primary capture vs DoE ref #1)

**Capture:** `agentic_orchestration/galadriel/captures/2026-05-18/combat-midfight/mobile-portrait-1290x2796/capture.png`
**Reference:** `agentic_orchestration/galadriel/reference-images/DOE-combat-whisper-rift-2-2026-05-17.png`
**Scoring artifact:** `agentic_orchestration/galadriel/captures/2026-05-18/combat-midfight/mobile-portrait-1290x2796/scoring.json`

| Axis | Score | One-line evidence |
|---|---|---|
| 3.1 Visual density | **2 / 5** | Mid-band contains 1 actively-engaged enemy + 2 small top-of-frame sprites; no floating damage numbers in mid-band (lower-right cluster is HUD-clipped cooldown indicators); no telegraphed AOE rectangles or ground swirl; picture's lower 2/3 is near-empty. |
| 3.2 Color register | **3 / 5** | Demo scene-volume dominated by dark navy + cool-blue particles + white text; warm tones appear only in HUD UI (HP orb, potion icons), NOT in scene combat effects — fundamentally opposite warm/cool register at scene level vs DoE's warm-crimson dominance. |
| 3.3 Lighting + atmosphere | **2 / 5** | Atmospheric pack loaded per console (clima_niebla_espesa + 6 others prewarmed) but rendered scene shows no visible atmospheric haze; scene reads as flat-dark-void rather than DoE's lit-volume-in-darkness. |
| 3.4 Typography + UI register | **2 / 5** | Portrait viewport CLIPS skill rail to right-edge vertical sliver instead of horizontal bottom band; no minimap, no objective banner, no countdown, no kill counter, no Level XP bar; "Wave 1 of 11" header text renders with jagged double-strike artifact. |
| 3.5 Reading order | **3 / 5** | "16890 / 16890 HP" numeric is the first eye attractor (overweight LEFT of player); player avatar rendered small (~50px) and visually less dominant than HP module; cooldown cluster pulls eye to lower-right edge rather than mid-band. |
| 3.6 Animation cadence | **2 / 5** | Still shows no AOE-telegraph elements (DoE has 2 red rectangles + crimson ground swirl); no mid-band floating damage numbers; subtle particle work around player + enemy HP rings barely visible. (Capture-timing caveat: late-midfight state may under-represent.) |
| **Aggregate** | **2.3 / 5** | *Recognizably in the same ARPG family as DoE; significant dissonances across multiple axes with specific drax-actionable remediation focuses identified.* |

### 4.2 — Combat-empty-room (HUD-isolated)

Captures at `combat-empty-room/mobile-portrait-1290x2796/` and `combat-empty-room/mobile-portrait-390x844/`. No DoE empty-combat reference; serves cross-check against DoE #1's HUD modules only. HUD architecture observation confirms what § 4.1 axis 3.4 records: portrait viewport clips skill rail; "Wave 1 of 11" header artifact persists; HP numeric + bars dominant at left.

### 4.3 — Desktop context capture (combat-midfight × 1920×1080)

Capture at `combat-midfight/desktop-1920x1080/`. Not a state-matched DoE comparison (DoE references are portrait), but reveals critical context: the demo HAS a substantial HUD that the portrait viewport is CLIPPING. Desktop shows 6 skill cooldown slots in a horizontal rail with cooldown numbers visible, HP orb (red) + mana orb (blue '90 / 270') in bottom-corners, 3 inventory/character icons top-left with hotkey labels, "Wave 1 of 11" + subtitle "Swarm — Vanguard". The desktop view re-frames the axis 3.4 score: the demo's HUD architecture is closer to DoE's at the design level; the dissonance is largely a portrait-viewport fit issue.

---

## § 5 — Strongest dissonances

*(Galadriel-drafted; gandalf critique-pair refines on design-meaning interpretation.)*

### 5.1 — Portrait viewport CLIPS the demo's actual HUD

**The picture says:** the demo's HUD at portrait phone aspect renders only fragments of its design. The skill rail (6 cooldown slots visible at desktop) becomes a vertical right-edge sliver. HP orb and mana orb don't appear. Inventory buttons don't appear. The "Wave 1 of 11" header renders with a jagged double-strike artifact (font/render bug). The player's class-name label clips on the left edge.

**Why this matters:** the portrait viewport is the DoE-matched aspect — it's where the player will play on a phone. DoE's HUD at the same aspect is dense and information-rich; the demo's effective HUD at the same aspect is sparse and broken-looking. This is the **single highest-leverage finding** of v1-DRAFT because:

- The demo HAS the HUD design (visible at desktop)
- The phone playtest experience cannot see most of it
- Remediation is layout-pass work, not a rebuild

**Drax-actionable remediation focus:** portrait-viewport HUD layout pass per gandalf v1.7 § 3.5. Specifically: (a) wrap skill rail to horizontal bottom band that fits 1290px width; (b) surface minimap + objective banner modules in top-left; (c) add countdown/timer indicator if applicable; (d) fix "Wave N of M" header text rendering (same bug family as season-selector menu — likely font + render-target mismatch); (e) move HP numeric to be visually proportional to player avatar (or replace numeric with bar-only convention DoE uses).

### 5.2 — Atmospheric layer loaded but not visibly contributing

**The picture says:** the demo's scene at primary viewport is a flat dark void with the player + enemies as the only lit elements. There is no atmospheric haze, no depth cues via lighting, no ambient particle work. DoE reference's scene has visible atmospheric red haze in the mid-band creating lit-volume-in-darkness contrast — the picture reads as "a stage lit inside a dark hall," not "characters floating in dark space."

**Why this matters:** the engine LOADS the atmospheric layer. Console logs confirm `clima_niebla_espesa` (season_002011's atmospheric effect) plus 6 other atmospheric packs are prewarmed. The wiring exists. But the rendered output shows no visible contribution. Either:

- The layer is rendering at very low alpha (under-tuned)
- The layer is z-ordered behind another opaque layer (z-conflict)
- The layer's clip-region or viewport-coverage doesn't extend across the visible scene
- The layer renders but only on specific events (combat-trigger?) that this state doesn't reach in time

**Drax-actionable remediation focus:** investigate atmospheric pack rendering pipeline. Cross-check the `[atmospheric] wired for season=season_002011` console signal with what's actually drawn at frame N. If alpha is the issue, tune up. If z-order is the issue, re-order. If clip-region is the issue, widen. The atmospheric pack is one of the strongest single visual-feel levers — it's the difference between scene-as-void and scene-as-place.

### 5.3 — Color register: cool-cold-in-dark vs DoE's warm-warmth-in-dark

**The picture says:** demo's scene is dominated by dark navy + cool-blue particle effects + white text. Warm tones appear only in HUD UI (red HP orb, red potion vial). DoE's scene is dominated by dark-brown + warm-crimson AOE + orange damage numbers + warm-tone particle work — even the dungeon ground itself reads brown-with-red rather than navy-black.

**Why this matters:** this is the loudest *register* dissonance — not a layout bug, but a palette-and-tone choice. The demo IS in the dungeon-darkness family (✓), so it's not in active opposition to DoE. But the warm/cool valence flip at scene level changes the feel from "fire and blood and threat in shadow" to "cold magical light in deep space." Both are valid; only one matches DoE.

**Drax-actionable remediation focus** (likely also informed by gandalf):
- Are crimson AOE telegraphs implementable as a render-side warm-tone pass?
- Can the existing damage-number rendering shift from white to orange-stencil (DoE convention)?
- Should the atmospheric pack default to warm tint when fire/blood register applies?
- Is this a design-direction choice (Reincarnated should be cool — distinguishing register) or a default-drift that should warm up to DoE-cluster baseline?

The third bullet routes through gandalf — § 7 below.

---

## § 6 — Gaps and structured findings

Per the rubric anti-pattern guard: surfaces with no comparable reference are **findings**, not scored. They are evidence of *absence*; absences are not failures, but they ARE the loudest signal the picture sends across the broader reference set.

### 6.1 — Town-feel gap (5 of 7 DoE references unmatched)

DoE's town surfaces (refs #2, 3, 4, 5, 7) show:
- 3–6 NPCs per frame with function-label + title + name convention ("STASH — 'Vault Merchant' Escher", "ARMORY — Whisperer Hecate", "PETS — Beast Tamer Malcolm", etc.)
- Multiple service vendors per shop area (Forge cluster: DARKGOLD FORGING / REFORGING / REFINEMENT all in same scene)
- Player-NPC proximity convention with floating uppercase function-labels visible
- Ambient lighting per shop (lantern + forge + torch register; warm hospitality vs dungeon's cold threat)
- Multi-player coexistence (lv.50 named characters visible in frame)
- Travel atmosphere (DoE ref #6's stone-path lit-to-dark gradient)

Demo state: zero town surfaces. Demo opens directly into dungeon-combat. No vendor system, no town map, no NPC roster, no service-vendor convention. The 5/7 unmatched references are a *product-scope* finding, not a visual-rendering finding — it's not drax's renderer missing a surface; it's the project's feature scope not having that surface yet.

**Disposition: L3-RESOLVED to (a)** by Matt 2026-05-18 evening (verbatim: *"We have no town by the way"* + *"L3-RESOLVED to (a)"*). Town is a Phase-2+ feature; the gap is intentional scope-prioritization (per Phase-1 P1 focus on combat foundation). DoE town surfaces enter Reincarnated's reference universe as a *future-state surface that has not been authored yet*, not as a feel-target shortfall.

Two readings considered:
- **(a) — RESOLVED-CHOSEN.** Town is a Phase-2+ feature; the gap is intentional scope-prioritization.
- **(b) — RESOLVED-REJECTED.** Town-feel as load-bearing for mobile-ARPG cluster reference adherence (would have meant town pulls forward as higher-priority Phase-2 deliverable).

**Implication for rubric methodology (galadriel-side):** future v2+ scoring continues to record town-state references as structured findings of *expected-absence*, not feel-target dissonance. When/if town surfaces are authored in Reincarnated, the rubric extends to score them against DoE town references at that point. Until then, the 5 unmatched town references are noted in every benchmark report as a recognized scope-deferred gap, not as a scoring caveat that drags aggregate down.

**Implication for the report (this doc):** Open Question #3 in § 7 is CLOSED. Gandalf critique-pair pass on this report no longer needs to deliberate the (a) vs (b) framing; it can focus on Open Questions #1, #2, #4, #5.

### 6.2 — Town-to-dungeon transition gap (DoE ref #6)

DoE ref #6 shows a distinct surface: stone path, lit-to-dark gradient, transition-NPCs (Seer Cassandra, Nightwatcher Edgar) lining the route, hedge + lantern + stone-bridge framing. This is a *travel atmosphere* surface — neither town nor dungeon. Reincarnated demo has no transition state; combat begins on demo load.

Resolves with town implementation OR explicit Reincarnated-doesn't-do-this design call. Tied to § 6.1.

### 6.3 — Menu-surface rendering anomaly at portrait phone aspect

Discovered during pre-D11.5 smoke captures (no DoE menu reference exists). Demo's season-selector menu renders **clean at desktop 1920×1080** (5 season tiles in 3+2 grid, REINCARNATED title, italicized description quotes, 4 element-pill rows per tile, ENTER prompts, "Choose a Season" subtitle) but **breaks at portrait phone aspect** (1290×2796 + 390×844): tile widths are not phone-responsive; titles bleed into adjacent tiles; decorative text fragments overlap.

**Same bug family** as combat-state "Wave 1 of 11" header rendering artifact (§ 4.1 axis 3.4 evidence). Both are likely the same root cause: a font / render-target mismatch when the viewport changes from desktop to phone-portrait.

**Drax-actionable.** Not a primary rubric scoring concern; surfaced as structured finding because the evidence is in the smoke captures and the bug family compounds with the combat-state finding.

### 6.4 — Capture-timing artifact (lightning_mage fast-clearing)

D11.5 determinism contract puts the player as the season's first playable class (Wall-Shocked Smuggler — lightning_mage with mana resource) on wave 1 with 8 Pitchwall Crusher monsters aggro'd before first tick. Lightning_mage's DPS on trash mobs is high enough that by `warmup_ms=2500` the wave is mostly cleared (`alive=1 dead=7` per console log). Captures land in late-midfight, not early-midfight.

This is a deterministic outcome of class+wave matchup, not randomness. It means visual density (axis 3.1) and animation cadence (axis 3.6) scores may be capture-timing-suppressed.

**Remediation paths** (drax-actionable, future):
- Add a `combat-midfight-paused` debug-state variant — same setup but with game-tick paused mid-animation
- OR add a slower-DPS class as the determinism choice for `combat-midfight`
- OR spawn an act-boss or higher-HP enemy class for capture-stable midfight
- OR reduce `warmup_ms` in the capture pipeline to capture earlier in the combat lifecycle (with caveat that atmospheric layers may not have settled)

Surfaced as advisory to drax/D11.5 for v2 iteration. Not a sprint-night blocker; v1-DRAFT scoring proceeds with late-midfight captures and notes the caveat.

### 6.5 — Floor tileset loaded but barely visible at portrait viewport

Console confirms `plates.png loaded: 104 floor tile variants (P1 swap)`. The mid-band has a subtle floor texture but the rest of the scene is near-black. Drax's v1.18.6 disabled decorative props per Matt L3 ("DoE has decorative-free dungeons"); the resulting scene is comparably sparse but **also lacks DoE's ground detail** (blood, debris, crimson texture). Whether the floor *should* be more visible (without decorative props) at portrait viewport is a design question — surface to gandalf in § 7.

---

## § 7 — Gandalf interpretation [pending critique-pair pass]

*(Galadriel-drafted seed; gandalf refines on design-meaning interpretation. Open hooks below; gandalf may rewrite this section or append.)*

The picture says: the demo is **on the way toward DoE register but not there yet**. Aggregate 2.3/5 is consistent with the project's actual state — the demo is shipping foundational seasons (002011-015 with canonical-6 archetype refactor in flight); the mobile-feel layer is mid-build; the canonical-7 substrate work is ongoing in parallel via the hive. v1-DRAFT scoring is honest, not damning.

**The high-leverage remediation observation:** most of the strongest dissonances are NOT fundamental design dissonances. They are *layout + render fit* issues at the DoE-matched aspect:

- The skill rail exists — it's clipped, not absent (§ 5.1)
- The atmospheric layer is wired — it's not visibly contributing, not unwired (§ 5.2)
- The color register IS dungeon-darkness family — the warm/cool valence is flipped at scene level only (§ 5.3)

This is encouraging. The demo's combat-feel design is sound; the portrait-fit + render-pipeline observable surface is where the work concentrates next.

**On the town-feel gap (§ 6.1): L3-RESOLVED to (a)** by Matt 2026-05-18 evening (verbatim: *"We have no town by the way"* + *"L3-RESOLVED to (a)"*). Town is a Phase-2+ feature; the gap is intentional scope-prioritization. Gandalf critique-pair pass no longer needs to deliberate this framing — the design-direction call is made. The 5 unmatched town references stand as recognized scope-deferred gaps in every benchmark report until town surfaces are authored. Galadriel's rubric methodology extends to score town surfaces against DoE town references at that future point.

**On the color register dissonance (§ 5.3):** gandalf's interpretation pending. Is cool-cold-in-dark the *intentional* Reincarnated palette (distinguishing register vs DoE-cluster default) or default-drift that should warm up? The Reincarnated cosmology references shadow + holy + lightning + warm-fire substrates; the substrate-identity-declaration spec is gandalf's seam. If shadow/lightning are dominant in season_002011's lightning_mage scene, cool may be canonical — and the rubric should re-anchor the color-register reference against a different DoE frame (e.g., a fire-substrate-themed scene) for that specific season's combat capture.

**On the capture-timing artifact (§ 6.4):** mostly a galadriel-drax operational concern (next-sprint state-design iteration). Not a design-meaning question for gandalf.

**Open questions for gandalf in the critique-pair pass** (matching rubric § 8):

1. **Aggregate weighting.** v1 uses unweighted mean. Should typography+UI register or color register carry higher weight than animation cadence (where stills under-represent and capture-timing artifact suppresses)?
2. **Register innovation vs register dissonance.** Demo's joystick (mobile-touch convention) and element-prefixed cooldown labels (LIG / WIN / etc.) may be register *innovation* rather than register *dissonance*. Galadriel scored the dissonance honestly; gandalf interprets whether to flag innovation separately in the scorecard.
3. **~~Town-gap disposition framing.~~** ✅ **CLOSED — L3-RESOLVED to (a)** by Matt 2026-05-18 evening. Town is Phase-2+; intentional scope-prioritization. § 6.1 + § 7 updated. Gandalf does not need to deliberate this in the critique-pair pass.
4. **Color register design-direction call.** § 5.3 — gandalf interprets whether cool-cold-in-dark is canonical-Reincarnated or render drift.
5. **Floor-visibility design-direction call.** § 6.5 — whether floor *should* be more visible at portrait without re-adding decorative props.

---

## § 8 — The Mirror voice [optional]

*(Galadriel-drafted; gandalf may refine or remove.)*

The Mirror was set tonight, and the picture has come.

What it shows is a game that knows what it wants to be — an ARPG in the DoE-cluster family — but is rendering itself in the wrong window. The HUD is there; the portrait viewport hides it. The atmospheric layer is wired; the screen does not show it. The color register is dungeon-darkness; the warmth has not yet arrived in the scene-volume.

These are not the dissonances of a game that has gone the wrong way. They are the dissonances of a game **mid-build**, where the design has been authored and the render has not yet caught it up to the design. The combat surface is recognizable. The mobile aspect is uncomfortable but not foreign. The picture is a draft of the picture it will eventually be.

The town-shaped silence in the rest of the reference set is loud. Five of seven DoE frames have no demo counterpart. The Court of Forms vessel and the Spirit Guide voice are not yet things the eye can see in the running surface. That is what Phase-2+ holds.

For tonight: the work is sound. The picture is honest. The remediation surface is concentrated, identifiable, and drax-actionable.

The Mirror does not flatter. Neither does it condemn. It shows what is. What is, tonight: a game on the way.

---

## § 9 — Next-iteration targets

For v1-SCORED → v2 → v2.1+:

| Iteration | Target |
|---|---|
| **v1-SCORED** (this report) | Manual scoring against primary capture; aggregate 2.3/5; 3 strongest dissonances named; 5 structured findings |
| **v2 (post-gandalf)** | Gandalf-refined § 7 interpretation; design-direction calls on color register (§ 5.3); axis weighting if revised. Town-gap disposition (§ 6.1) already L3-RESOLVED. |
| **v2-RE-SCORED** | Re-score after drax remediation on 3 strongest dissonances (portrait HUD layout pass; atmospheric pack rendering investigation; warm color-register pass if § 5.3 routes to disposition warmer) |
| **v2.1** | HSV histogram cosine sim implemented in `pipeline/score.mjs`; replaces manual color-register subjective scoring with reproducible numeric comparison |
| **v2.2** | Canny edge density per region + pHash/dHash + multi-frame capture for animation cadence (depends on combat-midfight-paused variant per § 6.4) |
| **v3** | Multi-reference triangulation when DoE reference set extends (Matt-captured character-select, inventory, mid-rift transition, boss-fight, death screen) |
| **v4+** | Additional cluster-references beyond DoE for "is our DoE alignment broadly consistent with the genre?" — Phase-2 question |

---

## § 10 — Cross-references

**Tonight's artifacts:**
- Rubric: `agentic_orchestration/galadriel/rubrics/2026-05-18-rubric-doe-comparison-v1.md`
- Reference set: `agentic_orchestration/galadriel/reference-images/MANIFEST.md` (7 DoE captures)
- Capture set summary: `agentic_orchestration/galadriel/captures/2026-05-18/CAPTURE-SET-SUMMARY.md`
- Primary scoring artifact: `agentic_orchestration/galadriel/captures/2026-05-18/combat-midfight/mobile-portrait-1290x2796/scoring.json`
- Capture pipeline: `agentic_orchestration/galadriel/pipeline/`

**Canonical context:**
- DoE feel-target canon: `canonical/story/mobile-feel-target-doe-2026-05-17.md`
- Mobile UX execution plan: `canonical/story/mobile-ux-execution-plan-2026-05-17.md`
- Hive-mind operating protocol: `canonical/story/hive-mind-protocol-2026-05-17.md`
- Audio register canon (adjacent register): `canonical/story/audio-register-canon-2026-05-17.md`

**Dispatches:**
- Capture pipeline dispatch: `agentic_orchestration/dispatches/2026-05-18-galadriel-capture-pipeline-and-state-matched-captures.md`
- This report's dispatch: `agentic_orchestration/dispatches/2026-05-18-galadriel-plus-gandalf-visual-benchmark-report-vs2a.md`
- Overnight sprint invocation: `agentic_orchestration/gandalf/requests/2026-05-18-knight-rider-mobile-playable-analytics-visual-benchmark-sprint.md` (Track C § 2.3)
- D11.5 dispatch (predecessor; landed at c039184): `agentic_orchestration/dispatches/2026-05-18-drax-debug-state-url-hook-D11-5-plus-mobile-render-validation.md`

**Engine + demo:**
- D11.5 spec (drax-authored): `~/Games/reincarnated-demo/src/debug/debugStates.ts` (commit `c039184` drax/v1.22)
- Agent definition: `.claude/agents/galadriel.md`

---

*Authored 2026-05-18 by galadriel after D11.5 gate opened (drax/v1.22 + v1.23). Gandalf critique-pair pass pending on §§ 5, 7, 8. The Mirror has shown the picture. The hive moves on.*
