# Companion-generation pass — design-conformance verdict (gandalf, independent)

**Author:** gandalf (story-and-design steward)
**Date:** 2026-06-16
**Authority:** knight-rider autonomous-run dispatch; Matt not in loop. Conclusion-free relative to jack-ryan (who gates the same work technically in parallel).
**Reviewed artifacts:**
- code `52c773d` — `reincarnated-engine/src/reincarnated/generation/companion_generation.py`
- math-note `e5d9c6a` — `.../generation/math/companion-generation-pass-2026-06-16.md`
**Governing canon (mine):**
- `canonical/story/2026-06-13-companion-as-hall-of-heroes-ally-commitment.md` (Path Pure v1.1)
- `agentic_orchestration/gandalf/notes/2026-06-13-q8-companion-convergence-matrix-FINAL.md` (68 valid cells)
- `agentic_orchestration/gandalf/notes/2026-06-12-session-2-proxy-companion-architecture-spec.md` §§ 4, 6.2, 6.3
**Verification:** ran `generate_companion_pass()`; inspected all 8 records; ran negative asserts (season-1 refusal, diagonal-absence, valid-cell-membership); cross-checked RETRIBUTION/PERSISTENCE rows; diffed `NPC_CAPS` against Session-2 §6.2 table line-by-line.

---

## VERDICT: ENDORSE-WITH-NOTE

The pass conforms to the locked T4 companion design. Every load-bearing thematic protection I authored is honored faithfully — not approximated in a way that changes meaning. The single NOTE is a thematic-surfacing observation on the synthetic Hall, not a non-conformance. Nothing in the code re-decides design; it consumes it. Below, the four confirmation points, then the four-park adjudication, then the D4 read.

---

## 1. Path Pure fidelity — CONFORMS

- `MIN_COMPANION_SEASON = 2`; `generate_companion_record` **raises** on `season_index < 2`. I ran it: season-1 request refuses with the correct message. The refusal-as-deliverable framing from commitment §7 ("the absence is *designed*, not a gap") is carried into the docstring verbatim in spirit. **The season-1 refusal guard IS the season-1 deliverable — exactly as ruled.**
- The synthetic Hall draw enforces `originating_season ∈ [1, season_index-1]` — a companion **must** originate in a season *before* the current one. This is the molted-past constraint expressed as arithmetic: you cannot field a self you have not yet been (commitment §1, "drawn from the Hall, never from the sky"). Faithful.
- The "every companion is a self the player used to be" premise is preserved structurally: `HallFormReference` is a *handle* (identity = lookup), never a generated kit. D7 held. See NOTE-A below for the one thematic caveat (synthetic vs real Hall), which is correctly parked, not drifted.

## 2. Q8 convergence-matrix fidelity — CONFORMS (verified at runtime)

- `Q8_VALID_COMPANIONS` is transcribed verbatim. The import-time `assert _CELL_COUNT == 68` is the right guard (Discipline #11). I confirmed the count and spot-checked every row against my FINAL §2.
- **Diagonal rejection:** import-time assert that no `(X,X)` cell exists, PLUS a per-record runtime assert `companion_strategy != player_strategy`. Belt-and-suspenders. Ran clean.
- **The RETRIBUTION/CC anti-synergy cut (my FINAL §5 exception #3 — the call I flagged as "the kind of precision that makes the system feel authored"):** honored exactly. `RETRIBUTION_ENGINE` row = `(ELEMENT_MONO, GEOMETRY_COLLAPSE, PERSISTENCE_ENGINE)` — **MONSTER_PACT absent**, with an inline comment citing the cut. And its mirror — `PERSISTENCE_ENGINE` **keeps** MONSTER_PACT — is present. The sharpest directional moment in the matrix (PERSISTENCE wants CC, RETRIBUTION rejects it, *same companion opposite validity*) survived transcription intact. This was the one cut most vulnerable to being flattened by a careless table; it was not.
- **The PROXY_INVERSION sanctioned summoner-damage exception (#1)** is present with an inline comment. **No dual-damage cells** appear anywhere (offense rows take survivability/control only). The generator draws ONLY from the valid space and a negative assert confirms an invalid request is never produced. Verified: all 8 sample records sit in valid cells.

## 3. §4 convergence-bond / §6.2-cap / §6.3-mapping fidelity — CONFORMS

- **§6.2 caps:** `NPC_CAPS` matches my Session-2 §6.2 table line-for-line (`damage_amp 1.15`, `cc_duration_mult 1.25`, `survivability_mod 0.10`, `resource_gen_mod 0.10`, `aoe_radius_mod 0.15`, `enemy_cc_mult 1.0` — NPC does not debuff enemy). Every emitted modifier is clamped and a `_assert_caps` invariant fires at generation. No modifier in any record exceeds cap. **The companion is a *behavior, not a power bump* — preserved.**
- **§6.3 mapping:** my §6.3 keys on the companion's *measured BC archetype* (Axis-2B, Axis-4, etc.), which does not exist at generation time. rocket substitutes a **role-class projection** keyed on the Q8 matrix's own role-intent headers (anchor/control/finisher/fuel/amp). This does NOT drift the bond's meaning — the Q8 matrix *already encodes* role-complement, so projecting from role-intent is structurally faithful to §6.3's purpose (map role → modifier-dominance). The measured-bin refinement is correctly parked as JC-2. I endorse the substitute as a generation-time stand-in; it must NOT be mistaken for the final §6.3 table (it isn't — the module says so).
- **§4 convergence bond:** named, action-conditional, both-halves-required (`both_halves_required=True` = the D3-Emanate property). The trigger→response pairs map to my §4 exemplar table (on_hp_threshold→interpose_shield, on_cc_applied→accelerate_dot, on_heavy_hit_absorbed→amplify_next_spike, on_overflow→dump_fuel_charge, plus the PROXY_INVERSION on_debuff→execute_range override). The named-bond register is templated-blank (`"Ember-and-Shadow Pact"` family) — **NEVER runtime LLM, D7 held**, with curated N1-N4 naming correctly parked as JC-3. The bond reads as *one past self answering another's danger* — bond-flavor not stat-flavor, as committed.

---

## 4. The four parks — adjudication (mine / Matt's / downstream)

**JC-1 — real-Hall population source. → SPLIT: the wiring is downstream; the Hall-surface AUTHORING is MINE; the bounded synthetic stand-in is ENDORSED as-is.**
- The synthetic Hall (`_SYNTHETIC_HALL`, 5 archetype handles, `is_synthetic=True`) is the correct bounded choice — it proves the record *shape* and the valid-cell draw run end-to-end without faking a real corpus. ENDORSED for the bounded pass.
- Real population has two halves: (a) cross-season Hall-persistence wire-in to emit ascended-form packets = **downstream** (elrond/rocket/gamora seam + the manifestation/Hall spike-wave the commitment §8 flags for the PC seam); (b) **what a real Hall *means* as a player-facing surface — how a past self is introduced as an ally, the molting-return beat, the season-2 tutorialization of the companion system — is MY seam** (commitment §8 explicitly: "gandalf — author the Hall-sourced companion into the player-journey surfaces"). I can begin that authoring now; it does not gate this pass. **Resolvable by me as steward (the authoring); the wiring stays parked for the spike-wave.**

**JC-2 — measured-BC §6.3 mapping. → DOWNSTREAM (gamora). Not mine, not Matt's.**
- §6.3 keys on measured BC bins that exist only after gamora's BC measurement. The role-class projection is the correct generation-time substitute. This is a generation↔measurement handoff. **Stays parked for gamora's Session-5 seam.** No design call required from me.

**JC-3 — convergence-item curated naming. → MINE (eventually), but correctly parked as production polish.**
- §5 of the commitment explicitly allows templated-blanks OR human-curated (N1-N4 stack). The templated `"<element>-and-<element> Pact"` register is conformant and sufficient for the bounded pass. Curated naming is *my* authoring lane (the bond-flavor register is a story surface), but it is **production polish, not pipeline-blocking** — it correctly stays parked until the companion layer is being surfaced. **Resolvable by me later; no urgency; park stands.**

**JC-4 — corpus size / companions-per-player target. → DESIGN CALL, partially MINE, partially Matt's.**
- Neither the commitment nor the Q8 matrix fixes how many companion records a season carries or how many a player may bond. The bounded pass's "one per sampled strategy" is correctly NOT a sized corpus. Two sub-questions: (a) *how many companions a player may field at once* — the commitment is unambiguous: **ONE** (commitment §0/§4 — "a single bonded ally occupying the 4th gear slot"; scarcity is the emotional engine; this is already ruled, not open). (b) *production corpus size* (how many distinct companion records the season generates to draw from) — this is a downstream production-fill number tied to the §4.1 "800-kit NPC season" target, a balance/scale call best made when the real Hall is wired. **I resolve (a) now: companions-per-player = 1, already locked. (b) stays parked — it is a scale call for the production-fill phase, surfaces to Matt only when the production corpus is actually sized.**

**Net:** Nothing in the four parks is mis-parked. JC-1-authoring and JC-3 are mine to pick up when the companion layer is surfaced (neither gates this pass). JC-2 is gamora's. JC-4(a) is already-ruled (one companion); JC-4(b) is a deferred scale call. **No park requires a fresh Matt decision to unblock this bounded pass.**

---

## 5. D4 Axis-2A meaning-shift — short design-meaning read (jack-ryan owns the technical/log call)

On design-meaning grounds only: a soloing kit reporting `solo`/measurable=True on the Proxy-Density axis is a **sound** semantic, and an improvement over `none`/measurable=False. The Proxy-Density axis measures *how much of a kit's combat output flows through proxy bodies*; a kit that fields no proxies has a real, meaningful reading on that axis — it sits at the floor. `solo` is the honest name for that floor (the kit *does its combat itself*), whereas `none`/measurable=False reads as "we couldn't measure this," which is a different and weaker claim — it implies absence-of-data rather than presence-of-a-real-low-density. The axis is not muddied; it is *completed* at its low end. The one thing to keep clean (jack-ryan's lane): `solo` must mean "measured floor density," not become a dumping ground for "axis didn't apply" — but for a genuinely soloing kit, measured-zero IS the floor, so the meaning is exactly right. Flag-gated OFF in production is the correct caution while the measured-floor semantic settles. **Design read: the meaning-shift is sound; endorse on design grounds; defer the technical/log disposition to jack-ryan.**

---

## 6. Surfaces to Matt on design grounds?

**No.** Nothing in this pass requires Matt. The pass faithfully consumes already-ruled design (Path Pure ruled by Matt 2026-06-16; Q8 matrix ratified; §6.2 caps ratified). The four parks are correctly dispositioned without new Matt decisions for the bounded pass. JC-4(b) (production corpus size) will surface to Matt *eventually* — when the production-fill is actually sized — but that is not now and not this pass. The one item I will pick up proactively as steward (no Matt gate needed): JC-1-authoring + JC-3 (the Hall-as-ally player-journey surface + curated bond naming), per commitment §8, when the companion layer reaches surfacing — flagged here as my standing follow-on, not an escalation.

---

## NOTE-A (the one ENDORSE-WITH-NOTE caveat — thematic, non-blocking)

The synthetic Hall pool uses five generic archetype handles (`iron_warden`, `frost_binder`, `ember_lancer`, `storm_caller`, `shade_warden`) with `is_synthetic=True`. This is the correct *bounded* choice and I endorse it. The thematic caveat — for the record, not as an objection: when the real Hall wires in (JC-1), the companion's identity must read as **a specific self the player actually lived**, with its name/deeds/final-form drawn from that player's real molt history — not a draw from a generic archetype menu. The whole emotional weight of "your first ascended hero returns to fight beside you" (the commitment §7 absence→arrival beat) collapses if the season-2 companion feels like a roster pick rather than *the* form the player poured a season into. The synthetic pool must never leak into production as the real source. The module is explicit that it won't (`is_synthetic` flag + JC-1 park), so this is a watch-flag for the wire-in, not a fault in this pass. **This is the seam where my Hall-surface authoring (JC-1) matters most — I will hold the line on it.**

---

**Signed:** gandalf, 2026-06-16. The companion came back as a self the player used to be, the matrix kept every cut I ruled, the bond stayed a story instead of a stat, and season 1 still fights alone exactly as it should. The pass is true to the design. ENDORSE-WITH-NOTE.
