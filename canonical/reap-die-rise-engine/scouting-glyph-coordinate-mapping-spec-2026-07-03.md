# Scouting-Glyph Coordinate-Mapping Spec — the III.8 MVP-critical minimal mapping

> **STATUS:** SPEC-CURRENT v1.0 (2026-07-03) — **five glyph NAMES CONFIRMED (Matt 2026-07-03); derivation BOUNDARIES remain PROVISIONAL until the W3 emission population validates them (§5)**
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

## 2. Inputs — exported fields (verified against `export/cycle13_normal_season_export.py`)

Every field the derivation reads is already in the per-kit export JSON; **zero new emission work**:

| Field | Values | Derivation role |
|---|---|---|
| `role_orientation` | damage / control / support / hybrid | primary axis |
| `range_profile` | close / medium / long | splits the damage family; range pip |
| `bc_target_cell` (proxy bin) | solo / minimal / mid / full | summoner test (checked first) |
| `proxy_dominant` (G4 post-hoc tag, lands W4) | bool | summoner test, preferred when present |
| `element` (+ `color_palette`) | 6 elements | element tint pip — no new vocabulary; the palette is already exported |
| `energy_type` | mana / rage / focus / combo / stamina | reserved for v1 boundary re-cuts (§5); unused in v0 |

## 3. Two glyph channels

| Channel | Read | Nature | Demo (MVP) | Launch |
|---|---|---|---|---|
| **Identity glyph** | *what IS this kit* | absolute — pure function of the kit's own coordinates | derived per §4 | same function, full population |
| **Temperature glyph** | *how it sits vs the CURRENT kit* | relational — kit × lieutenant | **hand-tagged at curation** (the Goldilocks spread is hand-picked per one-realm §3; Matt tags each lieutenant during the G7a roster pick) | computed from the matchup matrix (engine-tracker v2 ask; the matchup-coverage reward cashes against it) |

Temperature enum, fixed now so the demo bundle schema is forward-compatible: `too_hot` / `just_right` / `too_cold`. Launch swaps hand-tag → computed with **no schema change**.

## 4. Identity-glyph derivation v0 — five glyphs, ordered rules, first match wins

| # | Rule (on exported coordinates) | Glyph (names CONFIRMED — Matt 2026-07-03) | Genre read |
|---|---|---|---|
| 1 | proxy bin ≠ `solo` (or `proxy_dominant` true) | **SUMMONER** | the proxies ARE the kit (W2 evidence: caster-alone WR 0.000); demo-mandated legible |
| 2 | `role_orientation` = control | **CONTROLLER** | control-pure ctrl bin |
| 3 | `role_orientation` ∈ {support, hybrid} | **WARDEN** | the mixed/mitigator bucket |
| 4 | `role_orientation` = damage ∧ `range_profile` = close | **BRUISER** | melee damage |
| 5 | `role_orientation` = damage ∧ range ∈ {medium, long} | **GLASS CANNON** | ranged damage; source map gives damage-role `glass` def bin |

Plus two **modifier pips**, not primary glyphs: **element tint** (from `color_palette` — element is already the most legible axis via VFX/palette; do not spend a glyph shape on it) and **range pip** (close/mid/long dots).

**Why five:** the scouting read happens mid-run, pre-boss, in seconds. Hades keeps its per-god iconography legible because primary shapes stay in single digits; PoE's map-mod icon wall is the counter-example — 40+ icons that veteran players read as text anyway because the shapes stopped discriminating. Five shapes + two pips is comfortably inside the at-a-glance budget, and covers the demo roster span (melee / caster / ranged / controller / summoner, one-realm §3) one-to-one.

**Why these boundaries are provisional:** the AXES are ratified (they're the engine's own coordinates — no imposed taxonomy). The BOUNDARIES and NAMES are v0 guesses about where the emitted population clusters. Discipline #41 says the substrate votes: §5 is the vote.

## 5. Post-W3 validation gate — the empirical criterion that de-provisionalizes v0

When the demo-readiness run's W3 gauntlet survivors land (100–400 in-band kits, G2), run the derivation over the full survivor set and check:

1. **Coverage (total function):** every survivor maps to exactly one primary glyph. No fall-through, no "experimental" bucket on a scouting surface.
2. **Discrimination:** no glyph captures 0 survivors; no glyph captures >~40%. (Expected: SUMMONER ≈ 25% per the G4 composition knob; the other four share the rest.) If GLASS CANNON swallows the ceiling, first re-cut candidate is splitting it on `range_profile` medium vs long, second is `energy_type` tempo.
3. **Cluster fidelity (Disc #41 spot-check):** ~10 kits per glyph, read the actual skill trees — does the kit deliver what the glyph promises? gandalf DRIFT-CRITIC beat, rides beside the W4 audit.

Re-cuts happen **at this table** (v0 → v1 of this spec), never by hand-relabeling kits. Failures here are vocabulary failures, not kit failures.

## 6. Consumer contract + where the stamp lives

- **Stamping point:** the derivation is stamped as one field — `identity_glyph` — at **bundle assembly** (the same join where flavor keys off bundle membership), so demo UI, loadout app, and grimoire read ONE authoritative field and cannot diverge. The function is deterministic from exported fields, so consumers *may* re-derive for display fallback, but the stamped field governs.
- **Explicitly OUT of the live W0–W4 run's scope.** The run is executing; this adds no step to it. The run's output JSON already carries every input, so stamping is a **post-run, pre-demo-bundle beat**: one pure function + one field, applied to the run's output. Owner: star-lord (export seam), sequenced by KR after W4 closes. Temperature hand-tags enter at the G7a curation session.
- **Grimoire hook-honesty usage:** grimoire pages for un-spawned archetypes render glyph + page number, no kit data — the vocabulary must therefore cover the full emission space, which is exactly what §5 verifies.

## 7. Out of scope

- **Glyph ART** — shapes, register conformance, G2 gate: drax + galadriel territory. One requirement travels with it: glyphs must discriminate by **silhouette** at scouting-card size AND grimoire-stamp size (D2 rune-legibility standard — the shape reads before any detail).
- **Matchup-matrix math** (launch temperature computation) — gamora seam, launch-track, unchanged by this spec.
- Any change to generation or to the live run.

---

**Sign-off:** gandalf, 2026-07-03 (SPEC-AUTHOR). Anchors: one-realm-mvp-scope §1/§3/§5/§20a-c · engine-tracker III.8 · bc_target_source.py §2.2 guard · demo-readiness-run-spec-2026-07-03 §9. **The five names are Matt-CONFIRMED (2026-07-03); derivation boundaries remain provisional-until-§5 by construction.**
