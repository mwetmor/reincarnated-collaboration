# 2026-05-17 — gandalf — AOE tuning + monster density genre-canon validation briefing

**Authority:** Knight-rider auto-dispatch per Matt L3 standing delegation 2026-05-17 (validation routing while gandalf has continuous-availability cycles).
**Type:** Pattern B (long task) — ~1 day. Design briefing; no code work.
**Trigger:** Matt focused-playtest test 6 son feedback: *"more monsters and more AOE moves"* (currently task #48; queued for post-D10 regen tuning by gamora; needs design grounding BEFORE gamora hardcodes parameters).

---

## Why this briefing matters

Matt's son's "more monsters + more AOE" feedback is currently staged as a parameter-tuning task for the post-D10 regen. Without design grounding, gamora's parameter choices would be uninformed guesses against a load-bearing dimension — the **density-vs-AOE-radius coupling** is one of the deepest design knobs in the ARPG genre, and getting it wrong creates well-known failure modes:

- **Under-tuned AOE × under-dense monsters** → boring; "tagging single mobs"
- **Over-tuned AOE × under-dense monsters** → trivial; "one button clears the screen"
- **Under-tuned AOE × over-dense monsters** → punishing; "I die before I clear"
- **Over-tuned AOE × over-dense monsters** → screen-spam; "I can't see what's happening"

Your white-wizard knowledge of ARPG history (D2 / D3 / D4 / PoE / Last Epoch / Grim Dawn / Lost Ark / FFXIV elemental schools) is the right grounding. The post-D10 regen will lock the parameter envelope for the perception-test build; once it lands, re-tuning costs another regen cycle. Doing this design pass FIRST means gamora ships parameters that fit established canon, not first-guess.

---

## Required reading (in order)

1. `agentic_orchestration/hive-mind/phase-1-p1-log.md` — Matt's focused-playtest test 6 son feedback (captured ~13:30Z); drax v0.25-v0.33 ship trajectory (the demo state that produced the feedback)
2. `canonical/story/substrate-identity-declarations-2026-05-17.md` — all 7 substrate declarations; `geometry_affinities` per substrate is the AOE-character grounding (fire burst-PREFER vs earth ground_slam vs wind cone vs water persistent_zone etc.)
3. `canonical/story/d8-trait-floor-design-phase-1-p1.md` + `canonical/story/d8-canonical-four-trait-pools-2026-05-18.md` — your trait pools per substrate; many traits implicitly assume specific AOE-frequency or density assumptions
4. Your own L3 briefing `canonical/story/dodge-plus-telegraphed-combat-l3-briefing-2026-05-17.md` § 3 — telegraphed-AOE-windup design; this informs how AOE density interacts with player-perception-load
5. `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` — current monster spawn / pack composition logic (read-only; gamora's seam; gives you the implementation envelope to design within)
6. `canonical/16-project-roadmap.md` — current roadmap; check whether monster-density / AOE-balance appears anywhere as a B-series item

---

## Scope (single-track design briefing; 4 design surfaces)

### Surface 1 — ARPG genre canon for AOE skill distribution in player kits

Author a design proposal anchored in established ARPG dev history. Surface dimensions to address:

- **Late-game kit composition baseline**: in established ARPGs at end-game (where Matt's perception test runs), what's the typical ratio of AOE-flavor skills to single-target skills per build?
  - D2: 6-skill bar; varies wildly by class; sorc has lots of AOE; assassin has more single-target
  - D3: 6-skill bar; usually 1-2 generators (single-target) + 3-4 spenders (often AOE-flavored)
  - D4: 6-skill bar similar
  - PoE: variable; map farmers favor AOE; bossing favors single-target; build flexibility is the canon
  - Last Epoch: 5-skill bar; specialized per build
  - Grim Dawn: 2-class hybrid; varies
  - Lost Ark: 8-skill class roster; class-determined
- **Phase-1 P1 implication**: our generation already produces 5-8 skills per class kit. What target proportion should be AOE?
- **Substrate-coupled answer**: does the answer vary per substrate? (Fire ignition = burst-AOE-heavy seems cosmologically right; earth = anchor + single-target seems right; wind = wide-cone-AOE; lightning = chain-AOE; etc.)
- **AOE-character-coupled**: not all AOE is the same — burst-AOE (instant + small radius) vs persistent-zone (large + DoT-style) vs cone (medium + directional) play very differently. What's the genre-canon mix of AOE characters?

Output: § with specific per-substrate AOE-frequency recommendations + per-substrate AOE-character recommendations + cosmological rationale anchored to substrate-identity declarations.

### Surface 2 — ARPG genre canon for monster density per encounter

Address:

- **Pack size baseline**: established ARPGs typically spawn 3-8 monsters per "pack" in normal encounters; elite/champion packs may be smaller (1-3) but tougher; mini-boss encounters are 1 boss + 0-3 adds
- **Pack frequency**: how often packs appear in a 5-10 min play session
- **Total-monsters-per-minute**: this is what feeds KPM. What's the genre-canon TMPM in established games?
  - D3 rifts: very dense; designed for ~100-200 kills/min at high tiers
  - PoE maps: variable but ~50-150 KPM at clear difficulty
  - D4 dungeons: ~30-80 KPM in current state
  - Last Epoch monoliths: ~40-100 KPM
- **Phase-1 P1 implication**: Matt's son wants "more monsters" — what's the target TMPM? Should it be a single number or substrate-coupled (e.g., shadow areas spawn fewer-but-tougher monsters than fire areas)?
- **Pack-composition character**: should packs lean substrate-homogeneous (all-fire pack vs all-water pack) or substrate-heterogeneous (mixed substrate per pack)?

Output: § with specific monster-density recommendations (packs/min, monsters/pack, TMPM target) + substrate-coupling judgment if applicable.

### Surface 3 — AOE-radius vs monster-spacing coupling

This is the load-bearing math that's usually invisible to players but determines whether AOE feels good:

- **The geometric relationship**: if AOE radius is R and average monster spacing is S, then AOE hits ~ (R/S)² monsters. If R = 2S, AOE hits ~4 monsters. If R = 0.5S, AOE hits ~0.25 monsters (sometimes 0, sometimes 1).
- **Genre canon**: established ARPGs tune so player AOE comfortably hits 2-5 monsters per cast for medium-AOE skills, and 6-12 for big-AOE skills. This requires monster spacing tuned against AOE radius.
- **Phase-1 P1 implication**: gamora's monster spawn logic should respect this coupling. The post-D10 regen tuning should set monster spacing in packs such that the substrate's geometry_affinities produce expected per-cast hits.
- **Substrate-coupled answer**: fire burst-PREFER (small radius, high frequency) vs earth ground_slam (medium radius, anchored cast) vs wind cone (directional, medium radius) — each implies different optimal monster-spacing.

Output: § with target AOE-hit-per-cast values per substrate, plus monster-spacing implications.

### Surface 4 — Telegraphed-AOE-density interaction with narrow-slice work

This briefing connects to your prior L3 briefing on dodge + telegraphed combat. Address:

- **Player cognitive load**: too many simultaneous AOE telegraphs = visual overwhelm. If 3 enemies cast AOE simultaneously and the player has 0.5s windup per substrate, that's 3 ground indicators to read AND escape from in a half-second window. Genre canon caps this somehow (PoE map mods like "Magic Find" creates this exact failure; D4 nightmare dungeons too).
- **Phase-1 P1 implication**: monster density target should be tuned against simultaneous-AOE-telegraph budget. What's the max simultaneous indicators reasonable for player cognition?
- **Substrate-coupled answer**: shadow's 0.2s windup vs holy's 0.7s — does substrate-mixing in monster packs need to respect telegraph-time variance to keep player cognition manageable?

Output: § with per-encounter simultaneous-AOE-telegraph budget + substrate-mixing recommendations.

---

## Output deliverable

A single Matt-facing design briefing:
`canonical/story/aoe-tuning-and-monster-density-genre-canon-validation-2026-05-17.md`

Suggested structure:
- § 0 — TL;DR (gamora-implementable parameter envelope in 5-10 lines)
- § 1 — Why this matters
- § 2 — Surface 1: AOE skill distribution (genre canon + per-substrate recommendation)
- § 3 — Surface 2: Monster density (genre canon + per-substrate recommendation)
- § 4 — Surface 3: AOE-radius vs spacing coupling (genre canon + per-substrate target)
- § 5 — Surface 4: Telegraphed-AOE cognition budget
- § 6 — Cross-impact map (D10 generation rules; D14 calibration; D27 perception test; post-D10 regen)
- § 7 — Specific implementation parameters for gamora (extracted into a numerical table she can implement directly without re-deriving from the briefing prose)
- § 8 — Open questions for Matt (if any — non-blocking; § 7 should be implementable without Matt input)

---

## Out of scope (DO NOT)

- ❌ DO NOT write engine code, simulation code, or demo code
- ❌ DO NOT modify D8 / D9 trait pools (any trait-AOE interaction is briefing-level commentary, not amendment)
- ❌ DO NOT pre-empt the narrow-slice work in flight (this briefing INFORMS post-D10 regen tuning; doesn't displace narrow-slice)
- ❌ DO NOT modify substrate-identity declarations beyond commentary
- ❌ DO NOT extend scope to other gameplay tuning (drop rates, XP curves, etc.) — surface as OBSERVATION
- ❌ DO NOT respond to your prior briefing's open questions in § 9 (still parked for Matt)

---

## Acceptance criteria

- [ ] Briefing authored at `canonical/story/aoe-tuning-and-monster-density-genre-canon-validation-2026-05-17.md`
- [ ] All 4 design surfaces addressed with genre-canon citations + cosmological rationale
- [ ] § 7 contains specific numerical parameters gamora can implement directly (per-substrate where applicable)
- [ ] Cross-impact map present (§ 6)
- [ ] Tag `gandalf/v1.4-aoe-tuning-and-monster-density-canon-1`
- [ ] Hive-log STATE + HANDOFF → gamora (post-D10 regen consumer; she'll consume this when the regen dispatch fires after D10 code phase)
- [ ] Hive-log HANDOFF → knight-rider (briefing ready; surface to Matt summary on his return)

---

## Math-before-code requirements

N/A — design briefing; no code work.

---

## Hive log discipline

PRE-SIGNAL before hive-log append (per § 14.1.1 you authored). Apply broader pull-rebase discipline before engine-repo commits if needed (per your own 2026-05-17 OBSERVATION). Collab repo commits should still PRE-SIGNAL.

---

## Continuous-availability ramp

After this briefing ships, stay LIVE for:
- Matt L3 follow-up Q&A on this briefing AND your prior dodge/telegraphed-combat briefing (§ 9 open questions still parked)
- Gamora design-direction Q&A when post-D10 regen dispatch fires
- Drax design-direction Q&A on AOE-indicator visual character (narrow slice render work in flight)

---

*Dispatched 2026-05-17 by knight-rider per Matt L3 standing delegation. Estimated 1 day. Append completion record when done.*

---

## Completion record — 2026-05-17 (gandalf)

**Status:** SHIPPED.
**Briefing:** `canonical/story/aoe-tuning-and-monster-density-genre-canon-validation-2026-05-17.md`
**Tag intent:** `gandalf/v1.4-aoe-tuning-and-monster-density-canon-1`

**Acceptance criteria pass:**

- [x] Briefing authored at `canonical/story/aoe-tuning-and-monster-density-genre-canon-validation-2026-05-17.md`
- [x] All 4 design surfaces addressed with genre-canon citations + cosmological rationale
  - § 2 (Surface 1): AOE skill distribution — D2/D3/D4/PoE/LE/GD/LA citations; per-substrate AOE-share + character-mix tables
  - § 3 (Surface 2): Monster density — D2-LA range citations; TMPM 30-50 recommendation; 70/30 pack composition; substrate region-density modifier
  - § 4 (Surface 3): AOE-radius vs spacing — (R/S)² math; per-substrate radius targets; chain/vortex exceptions
  - § 5 (Surface 4): Telegraph cognition budget — 600ms/telegraph load; 2-simultaneous cap; mixed-windup-cadence rule
- [x] § 7 contains specific numerical parameters gamora can implement directly (per-substrate where applicable) — 24-row master parameter table + acceptance criteria + smoke-test guidance
- [x] Cross-impact map present (§ 6) — 8 cross-impact assessments (D10, post-D10 regen, D14, D27, narrow-slice, D8/D9, drax indicator render, roadmap)
- [x] Tag `gandalf/v1.4-aoe-tuning-and-monster-density-canon-1` — to be cut at commit
- [x] Hive-log STATE + HANDOFF → gamora (post-D10 regen consumer) appended
- [x] Hive-log HANDOFF → knight-rider (Matt-summary surface on return) appended

**Out-of-scope confirmed not touched:**

- No engine, simulation, or demo code
- No D8/D9 trait pool amendments
- No narrow-slice pre-emption (briefing INFORMS post-D10 regen tuning; doesn't displace narrow-slice work)
- No substrate-identity-declarations amendments beyond commentary
- No scope creep to other gameplay tuning (drop rates, XP curves)
- No response to prior briefing's § 9 open questions (still parked for Matt)

**Continuous-availability ramp:** gandalf stays LIVE for Matt L3 follow-up Q&A on BOTH this briefing AND the prior dodge/telegraphed-combat briefing (§ 9 open questions still parked). Gamora design-direction Q&A when post-D10 regen dispatch fires; drax design-direction Q&A on AOE-indicator visual character as needed.

— gandalf
