# Scouting-Glyph Coordinate-Mapping Spec — the III.8 MVP-critical minimal mapping

> **STATUS:** SPEC-CURRENT v1.1 (2026-07-03) — **five glyph NAMES CONFIRMED (Matt 2026-07-03). §5 gate PRE-RUN over the true W3 batch-1 bundle (700 kits, run_id `cbeb9471`) — v0's `role_orientation` axis was a PHANTOM (hard-coded "damage" population-wide); derivation RE-CUT onto BC coordinates per the §5 re-cut law. Evidence record: `agentic_orchestration/gandalf/notes/2026-07-03-glyph-s5-pre-run-findings.md`. CONTROLLER/WARDEN thresholds remain PROVISIONAL until a role-varied population emits.**
> **Author:** gandalf (SPEC-AUTHOR) · run-window authoring per demo-readiness-run-spec §9 (G10 window; NOT a wave dependency — Gate-1 #8)
> **Serves:** `canonical/reap-die-rise-game/one-realm-mvp-scope.md` §1 step 2 + §3 (Goldilocks lieutenant spread) + §5 IN-list ("scouting glyphs, minimal label→glyph mapping") + the §20a/§20c scale-hook gestures (grimoire pages previewing archetypes the demo never spawns)
> **Closes:** engine-tracker III.8 "scouting glyphs — feasible, vocabulary mismatch" **[MVP-CRITICAL]** (spec side; implementation is a post-run beat, §7)
> **Discipline anchors:** Discipline #41 (presentation vocabulary maps to emergent clusters, never pre-imposes taxonomy) · the BC-coordinate cutover §2.2 smuggling-trap guard (`generation/bc_target_source.py`, rocket 2026-06-14) · `2026-06-14-class-generator-bc-target-cutover-ruling.md` §7.2

---

## 0. What this is

The demo's boss floors offer a **Goldilocks spread** of lieutenants (hot / just-right / cold matchup temperatures vs the current kit). The player scouts them before committing. The scouting surface needs a **glyph vocabulary**: an at-a-glance read of *what each lieutenant is* and *how it sits against you*. The same glyphs stamp grimoire pages — including pages for archetypes the demo never spawns, which is how a ~10-kit demo carries a 400-kit hook honestly.

Engine-tracker III.8 named the gap: engine labels (`fire_mage`, `hunter`…) ≠ the design vocabulary ("glass cannon / bruiser / controller"). This spec defines the mapping — **and corrects the operation's name.**

## 1. The correction: coordinate→glyph, never label→glyph

The tracker's phrase "label→glyph mapping" would be an architectural regression if implemented literally. On 2026-06-14 the generation path went **zero-label** (BC-coordinate cutover Stage 1): kits are *composed from coordinates* — `(role_orientation, range_profile, energy_type, element)` → the BC 8-tuple — and `archetype_tag` is **derived downstream for naming only**. The §2.2 acceptance guard exists precisely to kill the smuggling trap: *compute-label-then-lookup-its-coordinate*.

Mapping glyphs FROM `archetype_tag` would rebuild that trap one layer up, at the presentation seam, immediately after rocket removed it from generation. Therefore:

- **Glyphs read exported COORDINATES** (§2 inputs). The derivation is a pure binning function, same discipline as `bc_target_from_generation_params`.
- **`archetype_tag` is a NAME channel** — it appears on the scouting card as the kit's name/flavor line, and nowhere in glyph derivation.
- The demo UI's current surfacing of raw `archetype_tag` + `role_orientation` strings (tracker III.8 note) is **superseded** on scouting surfaces: glyph + name replaces raw-label text.

## 2. Inputs — exported fields (v1.1: verified against the TRUE W3 bundle, not the retired cycle13 exporter)

> **v1.0 lineage note:** v0 verified its inputs against `export/cycle13_normal_season_export.py` — the retired path. The live W3 population carries **no `role_orientation` coordinate** (hard-coded `"damage"` for all 18 archetypes, `season_generation_pipeline.py:1557`; `KitCandidate` has no such field). The engine's actual coordinate system post-BC-cutover is the BC tuple — which is what §1's own law said to read all along. v1.1 corrects the input table accordingly.

| Field | Values | Derivation role | Availability |
|---|---|---|---|
| `bc_target_cell.range` | melee / mid / ranged | primary axis (damage-family split; range pip) | **populated** (v1.90 bridge) |
| `bc_target_cell.proxy_density` | None (solo) / light / … | summoner test (checked first; `"none"` normalized → None at the bridge) | **populated** |
| `bc_target_cell.tempo` / `.amplitude` | low/medium/high · spiky/flat/variable | reserved texture axes for future re-cuts | **populated** |
| `proxy_dominant` (G4 post-hoc tag, lands W4) | bool | summoner test, preferred when present | W4 |
| per-skill `effect_category` loading | counts over the kit's 12 skills | CONTROLLER / WARDEN tests (above-template loading, §4) | **populated** (uniform 4/4/2/2 in batch-1 → zero variance) |
| `element` → `dominant_element` | 6 elements | element tint pip | **gated on the F1 assembler bridge** (star-lord; findings note F1) |
| `resource_model` → `energy_type` | mana / rage / combo / stamina-as-resource / charge-stack (**doc-48 vocabulary** — the cycle13 enum was stale) | reserved for future boundary re-cuts | gated on F1 bridge |

## 3. Two glyph channels

| Channel | Read | Nature | Demo (MVP) | Launch |
|---|---|---|---|---|
| **Identity glyph** | *what IS this kit* | absolute — pure function of the kit's own coordinates | derived per §4 | same function, full population |
| **Temperature glyph** | *how it sits vs the CURRENT kit* | relational — kit × lieutenant | **hand-tagged at curation** (the Goldilocks spread is hand-picked per one-realm §3; Matt tags each lieutenant during the G7a roster pick) | computed from the matchup matrix (engine-tracker v2 ask; the matchup-coverage reward cashes against it) |

Temperature enum, fixed now so the demo bundle schema is forward-compatible: `too_hot` / `just_right` / `too_cold`. Launch swaps hand-tag → computed with **no schema change**.

## 4. Identity-glyph derivation v1.1 — five glyphs, ordered rules, first match wins

| # | Rule (on exported BC coordinates + skill loading) | Glyph (names CONFIRMED — Matt 2026-07-03) | Batch-1 capture |
|---|---|---|---|
| 1 | `bc_target_cell.proxy_density` is not None (or `proxy_dominant` true) | **SUMMONER** | 0 — **by adjudicated ruling** (Phase-A proxy-emission refutation); the proxies ARE the kit (W2 evidence: caster-alone WR 0.000) |
| 2 | control-category skills > template baseline (>2 of 12) | **CONTROLLER** | 0 — batch-1 template is uniform 4/4/2/2; threshold PROVISIONAL until a role-varied population emits |
| 3 | support-category skills > template baseline (>2 of 12) | **WARDEN** | 0 — same status as rule 2 |
| 4 | `bc_target_cell.range` = melee | **BRUISER** | 300 (42.9%) |
| 5 | `bc_target_cell.range` ∈ {mid, ranged} | **GLASS CANNON** | 400 (57.1%) |

Plus two **modifier pips**, not primary glyphs: **element tint** (from `dominant_element` once the F1 bridge lands — element is the most legible axis via VFX/palette; do not spend a glyph shape on it) and **range pip** (melee/mid/ranged dots — the engine's own BC vocabulary, replacing v0's close/medium/long).

**Rules 2–3 read the kit's own emitted content** (effect_category counts over its 12 exported skills), not a label — above-template loading is a coordinate of the kit, same discipline as the BC bins. In batch-1 they capture 0 *honestly*: role variety is composed INSIDE every kit (each carries exactly 2 control + 2 support skills), not ACROSS kits. The three unpopulated glyphs live where §0/§6 designed them to — **grimoire hook-honesty pages for archetypes this run never spawned.**

**Why five:** the scouting read happens mid-run, pre-boss, in seconds. Hades keeps its per-god iconography legible because primary shapes stay in single digits; PoE's map-mod icon wall is the counter-example — 40+ icons that veteran players read as text anyway because the shapes stopped discriminating. Five shapes + two pips is comfortably inside the at-a-glance budget, and covers the demo roster span (melee / caster / ranged / controller / summoner, one-realm §3) one-to-one.

**What remains provisional in v1.1:** rules 2–3's above-template thresholds (no variance exists yet to cut against) and the >40% ceiling at full-vocabulary scale. The NAMES are Matt-locked; rules 1/4/5 are now de-provisionalized against the batch-1 population. Discipline #41 says the substrate votes: §5 recorded the first vote.

## 5. Validation gate — executed 2026-07-03 over batch-1 (v1.1 results recorded); re-fires on every new emission population

> **Batch-1 note:** survivors landed at 700 (7 whole cells × 100 — cell-level verdicts), above the G2 100–400 band, and STR/DEX-only: **all 10 caster-attribute cells (INT+WIS) failed the gauntlet** (+1 melee-DEX). Full findings: `gandalf/notes/2026-07-03-glyph-s5-pre-run-findings.md`.

0. **Axis-existence (NEW in v1.1 — the check v0 needed):** every derivation input must be a live, *varying* coordinate of the population before boundaries are evaluated. v0 FAILED here (`role_orientation` = hard-coded constant) → re-cut. This is the framing-audit Q2 discipline embedded in the gate.
1. **Coverage (total function):** every survivor maps to exactly one primary glyph. **Batch-1: PASS** — 700/700, no fall-through, computable from `bc_target_cell` alone.
2. **Discrimination — measured against the EMITTED DESIGN SPAN, not the full vocabulary** (v1.1 amendment: with 3 of 5 glyph-populations structurally absent — summoners by ruling, controller/warden by uniform template — a full-vocabulary ceiling is arithmetically void). **Batch-1 within-span: PASS** — 42.9/57.1. Full-vocabulary re-test fires when a role-varied + proxy-viable population emits; if GLASS CANNON then swallows the ceiling, first re-cut candidate is splitting on mid vs ranged, second is `resource_model` tempo.
3. **Cluster fidelity (Disc #41 spot-check):** ~10 kits per populated glyph, read the actual skill trees — does the kit deliver what the glyph promises? gandalf DRIFT-CRITIC beat, **rides the W4 audit as assigned** (the one §5 check still open for batch-1).

Re-cuts happen **at this table** (v0 → v1.1 happened exactly here), never by hand-relabeling kits. Failures here are vocabulary failures, not kit failures.

## 6. Consumer contract + where the stamp lives

- **Stamping point:** the derivation is stamped as one field — `identity_glyph` — at **bundle assembly** (the same join where flavor keys off bundle membership), so demo UI, loadout app, and grimoire read ONE authoritative field and cannot diverge. The function is deterministic from exported fields, so consumers *may* re-derive for display fallback, but the stamped field governs.
- **Explicitly OUT of the live W0–W4 run's scope.** The run is executing; this adds no step to it. Stamping is a **post-run, pre-demo-bundle beat**: one pure function + one field, applied to the run's output. Owner: star-lord (export seam), sequenced by KR after W4 closes. **v1.1 prerequisite riding the same beat: the F1 assembler bridge** (findings note F1 — element→`dominant_element`, `resource_model`→`energy_type`, catalog `archetype_name`→`archetype_tag`; extends the proven v1.90 pattern, ~10s regen, no gauntlet re-run). Primary-glyph derivation needs no bridge (bc_target_cell is live); the element tint pip does. Temperature hand-tags enter at the G7a curation session.
- **Grimoire hook-honesty usage:** grimoire pages for un-spawned archetypes render glyph + page number, no kit data — the vocabulary must therefore cover the full emission space, which is exactly what §5 verifies.

## 7. Out of scope

- **Glyph ART** — shapes, register conformance, G2 gate: drax + galadriel territory. One requirement travels with it: glyphs must discriminate by **silhouette** at scouting-card size AND grimoire-stamp size (D2 rune-legibility standard — the shape reads before any detail).
- **Matchup-matrix math** (launch temperature computation) — gamora seam, launch-track, unchanged by this spec.
- Any change to generation or to the live run.

---

**Sign-off:** gandalf, 2026-07-03 (SPEC-AUTHOR; v1.1 re-cut authored under the §5 re-cut law after DRIFT-CRITIC pass on my own v0). Anchors: one-realm-mvp-scope §1/§3/§5/§20a-c · engine-tracker III.8 · bc_target_source.py §2.2 guard · demo-readiness-run-spec-2026-07-03 §9 · findings note `gandalf/notes/2026-07-03-glyph-s5-pre-run-findings.md` · engine `2839caf` (v1.90 bridge precedent). **The five names are Matt-CONFIRMED (2026-07-03); rules 1/4/5 de-provisionalized against batch-1; rules 2–3 thresholds provisional until a role-varied population emits.**
