# Dispatch — 2026-06-15 — rocket (+ gamora) — bake the guaranteed-intrinsic dodge into glass-close-ST

**Status:** ✅ FIRE-READY — jack-ryan Gate-1 (DESIGN-MODE) CLEAR-WITH-AMENDMENTS 2026-06-15 (A2-1, A2-2, A2-3, CL-1 folded); fire-able on Matt's go. Parallel with dispatch 1.
**From:** knight-rider
**To:** rocket (primary) + gamora (coupled no-op verification, B′)
**Pre-fire gate:** jack-ryan Gate-1 (DESIGN-MODE) on this dispatch BEFORE it fires.
**Estimated effort:** Pattern B (multi-session — a composition semantic addition + a coupled sim-boundary verification).
**Parent ruling (STEP 0):** `canonical/story/telegraph-dodge-temporal-decoupling-2026-06-15.md` § 5 (Move 2).

## What this is — Move 2 of the telegraph/dodge bridge

glass-close-ST is the fragile close-range single-target coordinate that walls against bosses on raw stats — **correctly** (ruling § 3). The genre-correct cure is not a stat buff; it is a **mechanism** the coordinate earns boss-capability through. This dispatch bakes that mechanism in: a **guaranteed-intrinsic movement skill — a dodge (short i-frame roll/dash)** — on **every** glass-close-ST kit.

The dodge is INERT in the sim (the autobattle cannot time it — § 7.2) and ACTIVE in Godot (the player times it against the rendered telegraph). This dispatch only puts the dodge *in the kit*; its value is realized downstream (dispatches 3–5).

## THE GOVERNING RULE + THE TRAP (ruling § 5 — non-negotiable)

> **The movement skill must solve survivability WITHOUT removing the player from the close-range fight.**

- **Dodge (short i-frame roll/dash) — design-correct, FIRST choice.** Keeps you in close range; makes boss-viability a timing skill check.
- **Blink — acceptable ONLY IF** tuned as a gap-closer / around-the-target reposition (keeps you on the boss).
- **Teleport — THE TRAP. Forbidden here.** A long reposition pulls you to range and dissolves the coordinate (glass-close-ST wearing a glass-medium tag). If the implementation reaches for teleport, that is a design failure — HALT and surface.

**Two further constraints:**
- **GUARANTEED, not rolled.** "By design" = **archetype-intrinsic**: every glass-close-ST kit carries the dodge. It must NOT be a generation probability — a probabilistic floor will eventually mint a glass-close-ST kit *without* it and the dead coordinate returns. Bake it in deterministically.
- **Coordinate-derived, not label-driven** (inherits the weapon-as-identity spine): the dodge is guaranteed by the bc-cell's own coordinates (the close/single-target/glass 8-tuple), NEVER by a re-introduced archetype label. No "rogue" label returns.

## ⚠ RECONCILE WITH THE JUST-LANDED ROLE-FLOOR FIX (KR coordination — load-bearing)

The role-floor dispatch (`2026-06-15-rocket-envelope-role-floor-fix.md`) **already added a coordinate-derived mobility floor** (`eng_bin=*-fast` → mobility ≥1–2; `mobility` emits on `geometry=="defensive_dash"`). The guaranteed dodge and the mobility floor **overlap and must be reconciled** — do NOT emit two competing movement instruments or double-count the slot. Resolve, in the math-note, ONE of:
- (a) the guaranteed i-frame **dodge** SUBSUMES / specializes the mobility-floor slot for glass-close-ST (the dodge IS the mobility-floor instrument, now a deterministic i-frame roll rather than a probabilistic ≥1 floor); or
- (b) they are distinct (mobility floor = generic repositioning; dodge = the i-frame survivability instrument) — justify why both, without bloating the kit_size band or starving distinctness.
**Lean (a)** per the ruling's "guaranteed, not a floor" language — but rocket decides and states. If ambiguous on a thematic/identity axis, route the reconciliation to **gandalf** (do not guess the design intent).

## Spirit-guide option (ruling § 5 — weigh, don't assume)
The ruling flags granting the dodge via the **spirit guide** (future-self teaches you to evade) — placing the survivability instrument on the project's load-bearing differentiator (spirit-swap) rather than a generic skill slot. **This is a design fork, not a rocket implementation call.** Surface it as an open question; if Matt/gandalf want the spirit-guide path, the dodge's HOME changes (spirit_guide seam, gamora-adjacent) and this dispatch re-scopes. Default for THIS dispatch: bake into composition; flag the spirit-guide alternative for the design call.

## Cross-seam contract change? (Principle 6 gate — KR assessment; rocket resolves)
**Assessment: CONDITIONAL — rocket resolves (Principle-6 silence = Gate-1 BLOCK).**
- The dodge is a **Skill** on the kit. If it reuses the existing shared `Skill` dict shape (a movement skill is a skill — like the role-floor's `defensive_dash`), **no new field** → `Round-trip: not applicable because the dodge reuses the existing shared Skill dict; no field added/renamed/removed.`
- BUT note the **downstream dependency (dispatch 5):** Godot must SEE the dodge in the kit to wire its input. The dodge skill MUST survive sim→export→Godot via the existing skill-list export. Confirm the dodge skill is not stripped/filtered by any export-side skill filter (e.g., a "sim-usable only" filter would drop an inert movement skill — that would silently break Move 2). State explicitly whether the existing skill-list export carries the dodge through; if a filter drops it, that is a contract gap to flag (→ star-lord dispatch 4).
- **B′ (gamora no-op verification) exercises the sim boundary regardless.**

## B′ — coupled gamora no-op verification (ruling § 7.2 operational corollary)
The sim must treat a movement skill it cannot use as a **clean no-op** — not crash, not mis-cost the kit for carrying it. gamora verifies (small, coupled):
- A glass-close-ST kit carrying the dodge runs the autobattle without error.
- The kit is NOT penalized or amped for carrying an unusable skill (no phantom cost, no action-economy distortion).
- The sim STILL walls the kit at the boss tier (the dodge being present does NOT improve sim boss-survivability — if it does, the sim is illegally "modeling" the dodge; § 7.2 violation → HALT).
- **(A2-3, jack-ryan Gate-1) Double-instrument guard:** IF the mobility-floor reconciliation lands on (b)-distinct (the kit carries BOTH the mobility-floor `defensive_dash` AND the i-frame dodge), B′ verifies the sim no-ops BOTH movement instruments WITHOUT compounded mis-cost or action-economy distortion. (Under (a)-subsume this is moot — itself an argument for (a).)
KR fires B′ as a short gamora check once rocket's dodge-carrying kit exists; B′ is a PASS-gate before this dispatch closes.

## Required reading before starting
- STEP-0 ruling § 5, § 7.2 — the spec + the no-op corollary.
- `2026-06-15-rocket-envelope-role-floor-fix.md` — the mobility-floor overlap to reconcile (REQUIRED — this is the collision surface).
- `weapon_envelope_composer.py` (`_role_for_geometry`, the mobility/`defensive_dash` path), `ability_grammar.py`, `b6_archetype_templates.py` (the intent being re-encoded, NOT called).
- `bc_target_source.py` — the glass-close-ST coordinates (`def_bin=glass`, `geo_bin=single-target`, `eng_bin=close-fast`).
- Genre anchors for the dodge shape: Souls i-frame roll, Hades dash, D3 Demon Hunter Vault, PoE Whirling Blades (the blink-as-gap-closer reference).
- Disciplines #1, #1.2 (code-cite), #11, #12 (semantic-shifting — this is one).

## Math-before-code (Discipline #1) — MANDATORY math-note; produce FIRST, HALT for Gate-1
A composition semantic addition (Discipline #12) → math-note Gate-1 is MANDATORY. Document, code-cited:
1. **The guaranteed-dodge emission** — how the close/ST/glass 8-tuple deterministically forces the dodge skill, label-free; which geometry/role carries it; why it is i-frame-dodge-shaped (in-range, timing-gated), not teleport.
2. **The mobility-floor reconciliation** (subsume vs distinct — § "RECONCILE" above) with the kit_size 10–13 band + distinctness re-proof (no regression of the role-floor fix's gains).
3. **The no-op contract** for gamora (B′): the skill carries no sim cost it cannot pay back.
4. **Principle-6 resolution** + the export-survival confirmation (does the dodge ride the existing skill-list export through to Godot).

## Scope
- [ ] Math-note FIRST; **HALT, MANDATORY jack-ryan Gate-1.**
- [ ] Bake the guaranteed-intrinsic dodge into glass-close-ST composition (coordinate-derived, deterministic, label-free).
- [ ] Reconcile with the mobility floor (no double-instrument; no kit_size/distinctness regression).
- [ ] B′: gamora verifies the sim no-ops the dodge (no crash, no mis-cost, still walls boss). [coupled — KR fires]
- [ ] Smoke-test passes (Discipline #2).
- [ ] MIGRATION.md IF Principle-6 resolves YES (else the not-applicable justification + export-survival confirmation).
- [ ] AGENT_STATE.md updated; tag `rocket/v1.x-dodge-intrinsic-glass-close-st`.

## Acceptance criteria
- [ ] EVERY glass-close-ST kit carries the dodge (guaranteed, not probabilistic) — proven across the 6 DEX geometries (mirror the role-floor audit method).
- [ ] No teleport; dodge keeps the kit in close range (in-range/timing-gated shape).
- [ ] No archetype label re-introduced (the spine).
- [ ] Mobility-floor overlap reconciled; kit_size 10–13 band + distinctness held.
- [ ] B′: sim no-ops the dodge cleanly AND still walls glass-close-ST at the boss tier.
- [ ] The dodge survives sim→export (rides the existing skill-list export to Godot).
- [ ] **(A2-2, jack-ryan Gate-1 — load-bearing handoff) Export-survival finding routed BEFORE dispatch 4 fires:** rocket's carries-through-vs-filter-drops finding is recorded in the math-note AND surfaced to KR as a dispatch-4 (star-lord) input. IF filter-drops, KR confirms dispatch 4's scope includes the fix BEFORE dispatch 4 fires — the dodge-export-survival handoff is made EXPLICIT, not left to land after star-lord's scope is set. (This closes the one seam where the dodge could silently fail to reach Godot — CL-3 chain-finding.)
- [ ] Round-trip smoke / not-applicable per the Principle-6 gate.

## Out of scope (explicit non-goals)
- **NO telegraph combat-model, NO export work, NO Godot work** — those are dispatches 3–5.
- **NO modeling the dodge as a sim survivability buff** (§ 7.2) — inert in sim.
- **NO spirit-guide implementation** unless Matt/gandalf select that fork (default: composition-baked; flag the alternative).
- **NO re-introduction of any archetype label.**
- **NO push** (Matt-gated).

## Open questions for the agent to resolve (document in the math-note)
- Subsume-vs-distinct on the mobility-floor overlap (lean subsume; route to gandalf if design-ambiguous).
- Spirit-guide-grant vs composition-grant (a design fork — surface for Matt/gandalf; do not unilaterally pick the spirit-guide path).
- Does the existing skill-list export carry an inert movement skill through, or does a filter drop it (→ star-lord dispatch 4 contract).

## Sequence
jack-ryan Gate-1 on this dispatch → rocket math-note → **HALT, MANDATORY Gate-1** → rocket implement → gamora B′ no-op check (KR fires) → jack-ryan Gate-2 → lands. Parallel with dispatch 1; independent of the critical-path telegraph chain EXCEPT for the export-survival confirmation that feeds dispatch 5.

## References
- STEP-0 ruling § 5, § 7.2; role-floor dispatch `2026-06-15-rocket-envelope-role-floor-fix.md`; reframe doc b23dce3.
