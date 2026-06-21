# Dispatch — 2026-06-21 — MULTI-SEAM — defensive-axis recalibration wave, TYPED-RESISTANCE spine (MASTER v2)

**From:** knight-rider
**To:** rocket → gamora → star-lord (sequenced); jack-ryan (Gate-1 this dispatch, Gate-2 each build)
**Approved by:** Matt 2026-06-21 — ruled death a core pillar (disposition B); **LOCKED TYPED RESISTANCES 2026-06-21** (the headline of this wave); authorized the recal as its own wave; authorized close-disposition (b) (offensive bands banked PROVISIONAL, re-rate-pending). This MASTER re-drafts the superseded flat/typeless MASTER (`2026-06-21-recal-wave-defensive-axis-MASTER.md`, HELD) around the typed-resistance corrected spine.
**Estimated effort:** ~4–5 waves across 3 seams (asymmetric). rocket gear-resist generation prerequisite + typed monster skills (~2 waves) BLOCK gamora calibration (~2 waves); star-lord typed telemetry (~0.5 wave) concurrent.
**Acceptance (wave-level):** the death channel routes through the kernel resolver with the kit's REAL per-element defense live; a signature-element boss moves from *"hard but doable"* (unmatched kit) to *"comfortable"* (matched kit) — NEVER unmatched-one-shot or matched-faceroll; the **anti-tax JOINT gate** holds (an under-resisted kit survives by playing well; matching is reward, never a mandatory cap); trash death-rate STRICTLY below boss; offensive bands re-rate ONCE jointly over both axes. **Nothing emits to content until the joint two-axis close.**

> **STATUS GATE:** Stage-0a (gamora resolver spike) PASSED **CLEAN**; Stage-0b (typed-resistance design-half) jack-ryan Gate-1 PASSED **ENDORSE-WITH-CONCERNS** — both required before this re-draft, both met. This re-drafted MASTER is the artifact jack-ryan Gate-1's. **On Gate-1 PASS + Matt publish-go, knight-rider splits this into per-seam pickup files.** Do NOT start the build before Gate-1 PASS + Matt go. The design is ruled; the BUILD is not yet released.

---

## Context (why this re-draft, what the typed spine changes)

The defensive-axis recal restores a real player-death channel (Matt ruled death a core pillar). The first MASTER built it on a FLAT/TYPELESS spine: the bespoke death branch `dmg = raw × (1 − player.armor_factor)` (`spatial_engine.py:1951`), tuned by a per-scenario global constant that OVERRIDES the kit's roll (`:1575-1578`/`:2390`). Under that spine, two kits with identical HP and opposite defensive builds die identically — a defensive axis that is "HP-and-kill-speed wearing a defense costume."

**Matt LOCKED typed resistances.** The corrected spine (gandalf design-half `2026-06-21-typed-resistance-meta-design-half.md`, commit `c85261e`; jack-ryan Gate-1 ENDORSE-WITH-CONCERNS):

1. **Resolver-route spine (§5):** route the monster→player death channel through `damage_resolver.resolve_skill` with the **player as a real DEFENDER** (its real `armor` + per-element `elemental_resistances` off `combatant_state`) and the mob as a real resolver ATTACKER (mobs carry `resolver_skills=[]` today). This is the SAME resolver the player's OFFENSE already uses — collapses the asymmetry onto one damage path. **Stage-0a proved this routes CLEAN, defender-agnostic, differentiation live (fire-resist 0.70 vs 0.05 → damage ratio 0.31579 = analytic to float precision).**
2. **Typed offense (§3):** monster skills carry an `element`; each trial-boss a **signature element** (the fire boss does fire — telegraphed, part of gallery identity).
3. **Resistance is a REWARD-for-matching, never a tax (§3):** a matched kit (high fire-res vs the fire boss) gets a meaningfully easier fight; an unmatched kit survives by playing well (kite the heavy-slow telegraphed slam, kill fast). No hard cap that becomes the floor. This is the D2 resistance *identity* without the PoE *tax*, and it routes through the spirit-swap pillar (bring the right FORM to the known fight).
4. **Gear-resist generation prerequisite (§4):** kits today are UNDIFFERENTIATED on resist (main gear path emits empty; populating paths even-spread). Typed offense into an even-spread surface buys nothing. rocket must mint DIFFERENTIATED per-element resist FIRST — schema/aggregation/sim are already ready (non-lossy), only the roll is missing.

**The design questions are RULED. This dispatch sequences the build; it does NOT re-open them.**

---

## Stage-0 results recorded (the gates that released this re-draft)

- **0a — gamora resolver de-risk spike (CLEAN):** `resolve_skill(skill, attacker, defender)` is defender-agnostic by construction; no production site on the resolver route branches on "attacker is the player"; the mob already gets a full `CombatantState` (used as defender today) carrying every attacker-read field; the 7×7 substrate matrix degrades gracefully (fires only when both substrates ∈ KNOWN, else mult 1.0). Differentiation proven through the PRODUCTION adapter. Production diff = 0 lines. Artifacts: harness `gamora_typed_resistance_resolver_route_2026_06_21_SPIKE_THROWAWAY_.py`, findings `simulation/math/typed-resistance-resolver-route-spike-2026-06-21.md` (commit `621905e`, push held).
- **0b — jack-ryan Gate-1 on the design-half (ENDORSE-WITH-CONCERNS):** all six engine claims re-derived from source; substrate asymmetry confirmed; gear gap confirmed (solder-the-middle, not a rebuild); flat anchor confirmed truly invalid; salvaged guard sound; anti-tax ruling coherent and genuinely distinct from PoE/D2. Finding: `qa/findings/2026-06-21-typed-resistance-meta-gate1-design.md`.

**The six Stage-0 concerns folded into the seam lines below (none block; all carried):**
- (0a-c1) Mob attacker substrate is DEFAULTABLE — per-element resist flows through `defender.elemental_resistances[element]` independent of the 7×7 matrix. Registering a KNOWN mob substrate is content-richness, NOT a route requirement → rocket line (optional richness, not a blocker).
- (0a-c2 / 0b-c1) Flat anchor genuinely invalid; `PLAYER_ARMOR_FACTOR_*` inert on the death channel once routed → gamora re-derives magnitude from scratch. **Numeric-drift note:** the held MASTER's `0.76/4.0` were calibration-grid SEARCH TARGETS, not live state (live: `0.95/0.40`); both are MOOT under the resolver — do NOT carry either as a knob-set.
- (0a-c3) Two engine touches, resolver byte-untouched: emit/project non-empty mob `resolver_skills` (composes with rocket typed-skill emission); swap the death channel (`spatial_engine.py:1951`) from the flat branch to `resolve_spatial_hit` (mob attacker, player defender) → gamora spine line.
- (0b-c2) **The anti-tax headline is CONTINGENT on the §4 generation constraint** — if generation lets a kit cheaply stack high all-resist, §3 silently collapses back into "cap everything" (the exact tax it avoids). **Elevated to a first-class JOINT (gamora+rocket) acceptance gate** below.
- (0b-c3) §4 is the MEDIUM add, not the small fix: neither `PartitionModifier` nor `RolledPartitionModifier` carries an element field (`partition_schema.py:505-546`); element SELECTION must be ADDED to the roll. Downstream bound intact (no schema/aggregation/sim change) → rocket sizes against this.

---

## Required reading before starting (ALL seams)

1. `agentic_orchestration/gandalf/notes/2026-06-21-typed-resistance-meta-design-half.md` — **the corrected design of record.** §3 (signature-element + reward-for-matching), §4 (gear prerequisite DoD), §5 (resolver spine + flat-anchor invalidation), §6 (re-founded guard), §7 (swarm elemental treatment), §8 (per-seam handoff).
2. `agentic_orchestration/qa/findings/2026-06-21-typed-resistance-meta-gate1-design.md` — jack-ryan Gate-1; the three carried concerns.
3. `~/Games/reincarnated-engine/src/reincarnated/simulation/math/typed-resistance-resolver-route-spike-2026-06-21.md` — gamora's 0a spike (the spine proof + the two engine-touch sequencing).
4. `agentic_orchestration/gandalf/notes/2026-06-21-monster-offense-threat-design-spec.md` — threat SHAPE (heavy-slow boss / light-variance swarm) — **UNCHANGED; typing is a property layered on the same shape (§10 amendment reverses only the typeless ruling).**
5. `agentic_orchestration/gandalf/notes/2026-06-21-defensive-axis-recal-encounter-model-ruling.md` — the nine constraints; the ones that SURVIVE the typed re-draft (see salvage below).

---

## SALVAGE vs SUPERSEDE (what carries from the held flat MASTER)

**SURVIVES (carry forward):**
- Threat SHAPE — heavy-slow boss / light-variance swarm (threat-spec §2/§3; typing is layered ON this shape, not instead of it).
- Geometry HARD constraint — only `{point, circle, line, cone}` are wired hit-geometries; `burst/ring/nova/wave/chain/arc` fall through to no-hit (`spatial_engine.py:740-741`). Unwired emit = silent damage-less threat.
- Trash < boss, always.
- Content emission HELD until the two-axis joint close.
- "Skills into skill-less mobs" (`t4_sim_cycling.py:1082`/`:1016`) — sharpened to TYPED resolver-attacker skills.
- star-lord additive telemetry — now RICHER (death-cause-WITH-element / damage-by-type).
- Two-axis joint re-rate (boss gate `survive AND kill`, both graded; bands re-rate ONCE jointly — encounter-model constraints 7/8).
- Full-population validation burden (constraint 9).

**SUPERSEDED (drop):**
- The flat-constant spine (`dmg = raw × (1 − armor_factor)`) → resolver route.
- Constraint-1 anchor knob-set (`MOB_DAMAGE_SCALE=4.0` / `armor 0.76` AND live `0.40/0.95`) → INVALID under the resolver; re-derive from scratch.
- The "tune the flat `armor_factor`" framing throughout.
- The threat-spec typeless ruling (§5b reversed).
- The "typing collides with the homogenization guard" argument (measured on the false flat-mitigation scenario) → dropped; the guard's PRINCIPLE survives, re-founded on typed defense (§6).

---

## The NON-NEGOTIABLE GUARDS (carry verbatim into every seam)

- **G-A — ANTI-TAX (the headline's load-bearing gate):** resistance is REWARD-for-matching, NEVER a mandatory cap. **If the only survival path against the signature boss is match-capping its element, the knob-set FAILS** (that is the PoE tax). Two viable paths — *match the element* OR *out-play the unmatched fight* (kite/kill-fast) — or reject the knob-set. **This is a JOINT gamora+rocket acceptance gate** (0b-c2): gamora's magnitude band AND rocket's gear-resist generation must BOTH respect it — if gear lets a kit cheaply stack high all-resist, "cap everything" dominates "match the fight" and the headline collapses regardless of gamora's band.
- **G-B — Trash < boss, always.** Boss = peak elemental-decision point (signature element, matching matters most). Swarm = minor/mixed elemental (broad resist mildly helps), shallow by design — NOT a per-element resist-check (that re-imports the D4 "every white mob is a threat" tax). Trash death-rate STRICTLY below boss for every kit profile.
- **G-C — Content emission HELD until the two-axis joint close.** No offensively-blessed-but-defensively-fragile kit ships before death is real and re-rated. `_DEFERRED_PROXY_BINS` lift / any 25% emission remain Matt-reserved and SEPARATE.
- **G-D — Flat anchor INVALID.** Do NOT carry `4.0/0.76` or `0.40/0.95` as a knob-set. The resolver uses `armor/(armor+K)` + per-element `(1 − clamp(res,0,0.95))` + the substrate matrix — a different functional form. Re-derive magnitude from scratch under the resolver.

---

## Wave sequencing (the dependency spine)

```
  rocket: §4 gear per-element-resist MINTING (the prerequisite — the payoff is inert without it)
        +  typed resolver-attacker monster skills (signature element per boss; heavy-slow)
                          │  (gen→sim soldered: mob carries resolver_skills + element)
                          ▼
  gamora: resolver-route spine (swap :1951 flat → resolve_spatial_hit; player defender, mob attacker)
        +  RE-DERIVE magnitude from scratch  +  typed band  +  re-founded guard  +  two-axis re-rate
                          │
  star-lord: death-cause-WITH-element / damage-by-type telemetry (additive) ── concurrent
                          ▼
        ANTI-TAX JOINT GATE (gamora band ∧ rocket gear-differentiation)  ──▶  jack-ryan Gate-2 each build
                          ▼
                 joint two-axis re-rate  ──▶  Matt joint-close
```

**Why rocket first (hard block, two reasons):** (1) gamora cannot calibrate a typed death channel the mob doesn't emit (mobs carry `resolver_skills=[]`); (2) the typed payoff is INERT against undifferentiated kits — gamora cannot validate "matching matters" until gear mints differentiated per-element resist. rocket's gear-resist minting + typed monster skills land first; gamora's calibration consumes both.

---

## PER-SEAM SECTIONS (each becomes a pickup file on Gate-1 PASS)

### ROCKET — gear-resist generation prerequisite + typed monster skills — BLOCKS gamora

**Build to design-half §4 + §8 (rocket bullet).**

**(a) Gear per-element-resist MINTING (the prerequisite — §4):**
- [ ] A piece of gear can roll resist toward a **specific element** (e.g. `{"fire": 0.30}`), not an even spread across all four. The `element_resistance` modifier category (`gear_instance_generator.py:66`, range −1.0..0.80) is the magnitude source; mint it onto per-instance `GearStats.elemental_resistances` with the **element key preserved**.
- [ ] **SIZING (jack-ryan 0b-c3 — this is the MEDIUM add, not the small fix):** source-confirmed that neither `PartitionModifier` nor `RolledPartitionModifier` carries an element field (`partition_schema.py:505-546`); projection matches by modifier-id only. So element SELECTION must be **ADDED** to the roll — NOT merely preserved through the per-instance build. Size against that. **The downstream bound is intact** — schema/aggregation/sim are unchanged (non-lossy per `gear_schema.py:252-253` → `combatant.py:575/926`); the blast radius is the roll only.
- [ ] **Differentiation verifiable end-to-end:** a kit built with a fire-weighted loadout shows higher `combatant.elemental_resistances["fire"]` than its other elements. (The 0a spike already proved the sim CONSUMES this differentiation — fire-res 0.70 vs 0.05 → analytic damage ratio. rocket closes the GENERATION half of that path.)
- [ ] **ANTI-TAX generation constraint (G-A — JOINT gate with gamora, 0b-c2):** do NOT make broad all-element resist trivially stackable to where "cap everything" dominates "match the fight." Specializing into the boss's element must be a BETTER defensive return than spreading thin. **gandalf+gamora converge with rocket on the exact shape — this is the single point where the anti-tax headline can quietly fail; it is a first-class acceptance gate, not a footnote.**

**(b) Typed resolver-attacker monster skills (§8 + threat-spec §2):**
- [ ] Give the endgame boss/elite/synthetic mobs (replacing `"skills": []` / `elemental_resistances={}` at `t4_sim_cycling.py:1082`/`:1016`) **typed resolver-attacker skills**: `element` + magnitude + `scaling_stat` + `substrate` (so `resolve_skill` processes them), each trial-boss carrying its **SIGNATURE element**, on the **heavy-slow** boss shape (few big readable hits — threat-spec §2).
- [ ] **Geometry HARD constraint:** emit ONLY wired hit-geometries `{point, circle, line, cone}`. `burst/ring/nova/wave/chain/arc` → no-hit (`spatial_engine.py:740-741`). An unwired geometry mints a damage-less (silent-defect) threat.
- [ ] **Swarm minor/mixed (§7):** swarm/clear-shell mobs carry minor/mixed elemental damage (broad resist mildly helps) — NOT a per-element resist-check (keeps trash<boss, avoids the D4 every-white-mob tax). Plus the per-hit variance field (threat-spec §3a swarm death lever — unchanged).
- [ ] **(optional richness, 0a-c1 — NOT a blocker):** registering a KNOWN mob substrate adds canonical/luminance valence on top of the per-element resist; per-element differentiation flows WITHOUT it. Add only if cheap; the route does not require it.

**Math-before-code:** math-note the emitted per-archetype magnitude SHAPE envelope (heavy-slow boss signature-element ranges; light-variance swarm) BEFORE wiring; gamora tunes exact constants within it.

**Out of scope for rocket:** setting production constants (gamora); changing the 80% resist ceiling / resolver mitigation curve / substrate matrix (§4 out-of-scope); the band finalization/emission (Matt-gated).

**Cross-seam (Principle 6 — round-trip REQUIRED):** TWO contract surfaces change: (1) per-instance `GearStats.elemental_resistances` now element-keyed differentiated; (2) the synthetic-mob dict now carries `resolver_skills` with `element`. Write MIGRATION.md (gen→sim). Round-trip smoke: (1) build a fire-weighted kit → assert `combatant.elemental_resistances["fire"]` > others through the production aggregation; (2) build a signature-element boss → step it through `spatial_engine` one tick, assert the resolver-attacker cast fires and applies TYPED damage the player's per-element resist mediates.

### GAMORA — resolver-route spine + typed calibration — depends on rocket

**Build to design-half §5/§3/§6/§8 (gamora bullet) + the surviving encounter-model constraints.**

- [ ] **(a) Resolver-route spine (§5, 0a-c3 — two engine touches, resolver byte-untouched):** swap the death channel `spatial_engine.py:1951` from the flat branch to `resolve_spatial_hit` (mob ATTACKER, player DEFENDER); ensure the mob projects a non-empty `resolver_skills` (composes with rocket's typed-skill emission). The player's real `combatant_state` mitigation (armor + per-element resist) goes LIVE on defense. `PLAYER_ARMOR_FACTOR_*` becomes inert on the death channel (retire/repurpose — any boss-harder-than-trash scaling moves to the monster attack-magnitude side).
- [ ] **(b) RE-DERIVE magnitude from scratch (G-D, 0a-c2/0b-c1):** the flat anchor is INVALID. Do NOT carry `4.0/0.76` or `0.40/0.95`. Math-before-code the resolver mitigation curves (`armor/(armor+K)`; per-element `(1 − clamp(res,0,0.95))`; substrate matrix) BEFORE the sweep, so the sweep is targeted not blind.
- [ ] **(c) Typed band (§3.3):** tune so the resist lever moves the signature boss from *"hard but doable"* (unmatched kit) to *"comfortable"* (matched kit) — NEVER unmatched-one-shot, NEVER matched-faceroll. Even at the 80% single-element ceiling the boss is a real fight; even at zero matching resist it is survivable-by-skill. This is the typed analog of the glass-0.6–0.8 / bruiser-0.95 spread.
- [ ] **(d) Re-founded homogenization guard on TYPED defense (§6):** at the chosen knob-set, an UNDER-RESISTED kit must survive the signature boss by playing well (kite the heavy-slow telegraphed slam / kill fast — offense+position substitute), while a MATCHED kit survives more comfortably. **Two viable paths — match the element OR out-play the unmatched fight — or reject the knob-set.** Re-run on real typed per-kit defense; do NOT inherit any flat sweep result.
- [ ] **(e) ANTI-TAX JOINT GATE (G-A, 0b-c2):** the chosen band MUST satisfy the anti-tax criterion JOINTLY with rocket's gear differentiation — if matching is mandatory to survive (no out-play path), or if all-resist stacking dominates matching, the knob-set FAILS. Converge with rocket+gandalf on the shape.
- [ ] **(f) Trash<boss + swarm typing (§7, G-B):** boss = signature element peak; swarm = minor/mixed shallow; trash death-rate STRICTLY below boss for every kit profile. Clear-shell death rare-by-design via per-hit variance (NOT coverage-crank — carried Gate-2 concern); boss-only death is the logged fallback if no guard-respecting clear-shell mechanism lands.
- [ ] **(g) Full-population validation (constraint 9):** the typed band + heavy-slow + variance profiles are unmeasured at population scale — validate on a FULL-population sweep, not the single-kit throwaway. Realized band WIDTH at production is the empirical burden.
- [ ] **(h) Two-axis joint re-rate (constraints 7/8):** boss gate is now `survive AND kill`, both graded. Re-rate the banked PROVISIONAL offensive bands ONCE, JOINTLY, over both axes — NOT offense-then-defense in two refits. Output FEEDS the joint band-finalization. **Do NOT finalize/emit — Matt-gated joint close.**

**Single-parameter sweep isolation (Discipline #24):** isolate the swept parameter per run; do not co-vary the spread-target levers and the guard levers in one sweep.
**Seed hygiene (Discipline #3):** prior runs consumed bases through 46M+; the 0a spike used 47M+. Use a DISJOINT base — **assign 48M+** for this wave.

**Out of scope for gamora:** monster-offense content + gear-resist minting (rocket — gamora consumes both); the encounter-model SHAPE + typed-resistance DESIGN (gandalf-ruled — do NOT re-open); band finalization/emission (Matt-gated); any explicit dodge/reaction model (positional avoidance only — §5 of threat-spec UNCHANGED; explicit telegraph-reaction is a named future fork).

**Cross-seam:** the live survive limb + typed death-cause surface new fight_log fields. Coordinate MIGRATION.md with star-lord. Round-trip smoke: a full-population fight producing a typed death → assert survive-rate + death-cause-WITH-element land in the export packet.

### STAR-LORD — typed threat telemetry — concurrent

**Build to design-half §8 (star-lord bullet).**
- [ ] Additive telemetry capturing the now-live TYPED death channel: **death-cause WITH element** and/or **damage-by-type** — richer than the typeless version, NEEDED to tune the typed band and VERIFY matching matters (without it, "matched kit eases" is unobservable). star-lord's call on exact shape at build.
- [ ] **Additive only** — no field renamed/removed; existing consumers byte-identical (keeps the offensive instrument's banked artifacts intact).
- [ ] **MIGRATION.md** (star-lord ↔ gamora boundary, ADR-004).

**Cross-seam (Principle 6 — round-trip REQUIRED):** ADDS fight_log/telemetry fields → YES on the Principle 6 gate. Round-trip smoke: production-path fight that kills the player with a typed skill → assert death-cause-with-element + damage-by-type present and populated through gamora→star-lord into the season JSON.

**Out of scope:** `_DEFERRED_PROXY_BINS` lift / 25% emission (Matt-reserved, separate); any non-additive schema change.

### JACK-RYAN — Gate-1 (this dispatch) + Gate-2 (each build)

- [ ] **Gate-1 DESIGN-MODE on THIS re-drafted MASTER** (before knight-rider publishes the per-seam pickup files): verify the sequencing routes the corrected spine faithfully, the four guards carry verbatim, the **anti-tax JOINT gate** is a first-class acceptance criterion on BOTH the rocket and gamora lines (not a footnote), the §4 gear prerequisite is sized as the MEDIUM add, the flat anchor is dropped (no `4.0/0.76` or `0.40/0.95` carried as a knob-set), the geometry HARD constraint survives, no ruled design question is re-opened, and the cross-seam Principle-6 round-trip clauses are present on all three seam lines.
- [ ] **Gate-2 DEV-MODE on each seam build** in sequence: rocket (does gear mint DIFFERENTIATED per-element resist end-to-end? do typed monster skills fire through the resolver? is the seam soldered?), gamora (is the death channel routed through the resolver with the kit's real defense LIVE? is magnitude re-derived, not flat-anchor-inherited? does the typed band hit hard-but-doable/comfortable with no one-shot/faceroll? does the re-founded guard PASS on typed defense? is the anti-tax JOINT gate satisfied? trash strictly below boss? is the re-rate ONE joint refit?), star-lord (round-trip typed-death telemetry present?).

---

## Cross-seam contract change? (Principle 6 gate — knight-rider completed at authoring)

**YES.** Multiple inter-seam fixture dicts change:
- rocket → sim: per-instance `GearStats.elemental_resistances` now element-keyed differentiated; synthetic-mob dict now carries `resolver_skills` with `element`.
- gamora → star-lord: live typed survive-outcome + death-cause-with-element fields on the fight_log.
- star-lord export: additive typed-threat telemetry on the season JSON.

**Each per-seam section carries its round-trip smoke clause + MIGRATION.md requirement.** No seam tags without its round-trip smoke.

## Out of scope (wave-level explicit non-goals)

- The `_DEFERRED_PROXY_BINS` lift / 25% proxy emission — separate Matt-reserved decision.
- Proxy/summoner Wave-3 — INHERITS this real (now typed) death channel; separate downstream wave.
- An explicit dodge / telegraph-reaction model — positional avoidance only; explicit reaction is a named future fork.
- Changing the 80% resist ceiling / resolver mitigation curve / substrate matrix (§4 out-of-scope).
- Re-opening any ruled design question (typed direction, signature-element + reward-for-matching, the resolver spine, the gear-resist DoD, the guard re-founding, swarm shallow-typing) — all RULED.
- Band FINALIZATION / content emission — Matt-gated joint two-axis close.

## Open questions the build resolves (and documents)

- **gamora:** exact resolver magnitude at which the typed band hits hard-but-doable/comfortable with no one-shot/faceroll — the band-center tuning under the resolver curves. Math-note it.
- **gamora+rocket+gandalf (JOINT):** the exact gear-resist generation SHAPE that makes element-matching a better return than all-resist stacking (the anti-tax gate's load-bearing convergence).
- **gamora:** whether clear-shell death is deliverable via per-hit variance inside the guard+ordering, OR the boss-only fallback fires — log either way.
- **rocket:** the gear-resist roll element-selection mechanism (the MEDIUM add); which mob roles carry the signature-element heavy-slow boss skill vs the swarm minor/mixed.
- **star-lord:** exact additive field shape (death-cause-with-element vs damage-by-type vs both).

## References

- Typed-resistance design-half (design of record): `agentic_orchestration/gandalf/notes/2026-06-21-typed-resistance-meta-design-half.md` (`c85261e`)
- Typed-resistance Gate-1 (three carried concerns): `agentic_orchestration/qa/findings/2026-06-21-typed-resistance-meta-gate1-design.md`
- 0a resolver spike (spine proof + two engine-touches): `~/Games/reincarnated-engine/src/reincarnated/simulation/math/typed-resistance-resolver-route-spike-2026-06-21.md` (`621905e`)
- Threat-design spec (heavy-slow/variance SHAPE, geometry; §5b reversed): `agentic_orchestration/gandalf/notes/2026-06-21-monster-offense-threat-design-spec.md`
- Encounter-model ruling (surviving constraints 7/8/9, trash<boss): `agentic_orchestration/gandalf/notes/2026-06-21-defensive-axis-recal-encounter-model-ruling.md`
- HELD superseded flat MASTER: `agentic_orchestration/dispatches/2026-06-21-recal-wave-defensive-axis-MASTER.md`
- Calibration diagnostic + Gate-2 (flat-model anchor, now invalid): `~/Games/reincarnated-engine/src/reincarnated/simulation/math/defensive-axis-calibration-diagnose-2026-06-21.md`; `qa/findings/2026-06-21-defensive-axis-calibration-diagnose-gate2.md`
- Engine — death channel (flat, to be swapped): `spatial_engine.py:1951`; player flat constant `:1575-1578`/`:2390`; offense resolver route `:533-534`; mob-as-defender `:2454-2460`; mob `resolver_skills=[]` `:2508`; geometry dispatch `:716-741`
- Engine — resolver typed paths: `damage_resolver.py:456/460/478/485/502`
- Gen — resist surface: empty main path `gear_generation.py:943-972`; even-spread `keystone_loadout_materializer.py:275-279`/`gear_catalog.py:188-190`; non-lossy aggregation `gear_schema.py:252-253`; modifier category+range `gear_instance_generator.py:66/487`; NO element field on modifiers `partition_schema.py:505-546`; player combatant resist source `combatant.py:566/575/926`
- Gen — endgame boss empty + skill-less: `t4_sim_cycling.py:1016/1082`
- Disciplines: #1 math-before-code, #3 seed hygiene (48M+), #11 empirical inspection, #12 semantic-shift, #24 single-parameter sweep isolation
