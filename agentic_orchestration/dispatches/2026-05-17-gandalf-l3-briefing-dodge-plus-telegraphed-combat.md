# 2026-05-17 — gandalf — L3 design briefing: dodge mechanic + telegraphed-combat system

**Authority:** Knight-rider auto-dispatch per Matt L3 standing authority + dodge/telegraphed-combat surfaces from focused playtest test 6.

**AMENDMENT 2026-05-17 (post-spawn; Matt-confirmed):** Matt has explicitly delegated the scope-extension decision to gandalf. Quote: *"scope extension is fine if gandalf approves urgency. No need to wait on me. If this is integral to the needs of the hive, just move forward and we will follow."* Your § 7 recommendation is therefore **binding** — not a recommendation pending Matt sign-off. Knight-rider will execute on your decision directly (dispatch gamora simulation + drax-demo render work, OR park to Phase-2, per your § 7).

**Sequencing consideration:** If you decide Phase-1 P1 extension, knight-rider needs to sequence combat-design simulation work relative to gamora's queued D10 code phase. D10 (substrate-coherent generation rules) may need to consume combat-design semantics if telegraphed combat lands canonically. Please address in § 6 (cross-impact map) explicitly: does combat-design simulation need to land BEFORE D10 code, or can it sequence after? Your call on the dependency direction.
**Type:** Pattern B (long task) — ~1-2 days. Design briefing for Matt L3 decision; no code work.
**Trigger:** Matt focused playtest test 6 son feedback:
> *"it would be way more fun if it seemed like the monsters could move out of range of your AOE and vice versa, if you could dodge roll out of the way, or run.. whatever.. but right now it feels like moves can't be escaped and monsters can't escape your moves"*
>
> *"we need a way to dodge attacks with VFX like roll/strafe/sprint whatever"*

These two surfaces are **one design system**: spatial-combat-with-escape-windows. Drax-demo v0.26 ships a cosmetic-only dodge placeholder for next playtest; this briefing authors the canonical engine-side design.

---

## Why this briefing matters

The substrate-identity declarations assume spatial combat matters. `forbidden_mechanics`, `geometry_affinities`, `iconic_register` — all of these presuppose that *where things happen on the battlefield* decides outcomes. `vortex_pull` vs `cone push-out` only feels different if positioning matters. `persistent_zone` only feels different from `burst` if monsters can move into and out of the zone.

If Phase-1 P1 ships without telegraphed combat + escape windows, the D27 perception test may come back as "substrates feel the same because nothing about position changes outcomes." That would invalidate the perception test for the wrong reason — not because substrate identity is wrong, but because the gameplay system that *expresses* substrate identity is missing.

Matt is currently weighing a Phase-1 P1 scope extension (fold this in) vs Phase-2 deferral. This briefing **gives him the design surface** to make that decision and **becomes the implementation contract** if he says "extend Phase-1 P1."

---

## Required reading (in order)

1. `agentic_orchestration/hive-mind/phase-1-p1-log.md` — drax-demo Item 5 + v0.25 polish + v0.26 dispatch (most recent entries; the cosmetic dodge primitive context)
2. `canonical/story/substrate-identity-declarations-2026-05-17.md` — all 7 substrates' `iconic_verbs`, `cosmological_commitment`, `geometry_affinities`, `mechanical_signature` (substrate-coupled design space)
3. `canonical/story/d8-trait-floor-design-phase-1-p1.md` + `canonical/story/d8-canonical-four-trait-pools-2026-05-18.md` — your trait pools (some may already imply telegraph/escape mechanics)
4. `canonical/16-project-roadmap.md` (latest B-series state) — current roadmap; check whether telegraphed combat appears anywhere
5. `reincarnated-engine/src/reincarnated/simulation/` — existing fight resolver; understand what's currently implemented (you're authoring design, but knowing the engine's current spatial-or-non-spatial baseline helps)
6. `reincarnated-engine/design/decisions/decisions-log.md` — latest entries; check for prior ADRs touching combat-mechanics

---

## Scope (single-track design briefing; 3 design surfaces)

### Surface 1 — Canonical dodge mechanic

Author a design proposal for the engine-side dodge mechanic. Surface dimensions to address:

- **Cosmological framing**: is dodge a universal verb (every class can dodge) or class-coupled (some classes have dodge, others have different evasion verb)? D2-D4 + PoE + LE precedent useful here.
- **Substrate coupling**: does dodge behave differently per substrate (e.g., wind dodge = teleport-blink; earth dodge = root-and-tank; holy dodge = brief-invulnerability; shadow dodge = shadow-step into stealth)? Or is dodge substrate-agnostic?
- **Mechanic shape**: i-frames-based (duration window of invulnerability), distance-based (literal teleport bypass), or both?
- **Cooldown structure**: shared global cooldown? Per-class? Charges (like a stamina pool)?
- **Cost**: free? Stamina-gated? Mana-gated? On-hit-charges-up?
- **Cancel rules**: cancels current cast? Cancels current movement order? Cancels enemy debuffs (cleanse-on-dodge)?
- **Animation framing**: roll? strafe? sprint? shadow-step? Should the animation read as substrate-coherent (lightning teleports, water flows, earth braces, etc.)?

Output: a design proposal section in your briefing doc with a clear recommendation + alternatives + cosmological rationale.

### Surface 2 — Telegraphed AOE windup system

Author a design proposal for AOE telegraph mechanics. Surface dimensions to address:

- **Cosmological framing**: do all AOEs telegraph, or only large/dangerous ones? Does windup time vary by substrate (holy slow-build accumulation; lightning instant-strike; water tide-rise)?
- **Substrate-coupled windup characters**:
  - **Fire**: escalation = building-up windup that the player can read (charge animation)
  - **Water**: pervading presence = AOEs that grow/expand from a center over time
  - **Earth**: positional refusal = AOEs that anchor + persist (less windup, more duration)
  - **Wind**: kinetic rearrangement = AOEs that telegraph the *direction of the rearrangement* (pull line; push cone)
  - **Lightning**: instant arc + the *next* arc telegraphs (chain windup)
  - **Holy**: slow radiant build-up = bright ground indicator with cosmological accumulation
  - **Shadow**: hidden until commit = late telegraph, harder to escape but with telegraph still present (fair vs unfair design)
- **Visual language**: ground indicator color/shape per substrate? Indicator semantics (where AOE will hit; not just "something will happen here")?
- **Indicator timing**: how much windup time before AOE resolves? Linear, or substrate-tuned?
- **Indicator-skill coupling**: which D8/D9 trait floors interact with telegraph (e.g., a fire trait that *reduces* windup time for fire AOEs)?

Output: a design proposal section with a recommendation per substrate (or substrate-agnostic if cosmologically warranted), default windup times, and cross-reference to substrate-identity declarations.

### Surface 3 — Monster AI escape behavior

Author a design proposal for monster AI movement during player cast windows. Surface dimensions to address:

- **Should monsters dodge player AOEs?** If yes, all monsters or only some (mini-bosses + bosses; not basic adds)? Telegraphed escape (monster shows intent to move) or instant?
- **Escape coherence with monster substrate**: does a fire monster escape differently from a water monster? (Mirror of the player substrate-coupled dodge question.)
- **Player-monster symmetry**: should the player's experience of "monsters can escape my AOE" mirror "I can escape monster AOE"? Or should asymmetry exist (e.g., bosses can dodge; player can dodge; basic mobs cannot)?
- **AI sophistication tier**: basic add reactive escape (move out when ground indicator appears) vs boss strategic escape (anticipate cast, pre-position) — which tier per monster role?
- **Engagement loop framing**: how does escape behavior change the *rhythm* of combat? (E.g., if monsters always escape, player has to lead targets; if monsters sometimes commit, player has windows for clean hits.)

Output: a design proposal section with tiered AI behavior recommendations per monster role + cross-reference to the substrate-coherent monster generation (D10 incorporates this).

---

## Output deliverable

A single Matt-facing L3 briefing doc:
`canonical/story/dodge-plus-telegraphed-combat-l3-briefing-2026-05-17.md`

Structure:
- § 1 — Why this matters (cosmological + perception-test framing; you have the briefing context)
- § 2 — Surface 1: Canonical dodge mechanic (your recommendation + alternatives + rationale)
- § 3 — Surface 2: Telegraphed AOE windup system (per-substrate proposal + cross-references)
- § 4 — Surface 3: Monster AI escape behavior (tiered proposal + role coupling)
- § 5 — Scope estimate breakdown (gandalf design ~3-5 days [this briefing covers most of it]; gamora simulation ~5-7 days; drax-demo render ~3-5 days; total ~11-17 days as Phase-1 P1 scope extension OR Phase-2 deferral)
- § 6 — Cross-impact map: which existing Phase-1 P1 deliverables this affects (D27 perception test, D14 mirror-match gate, D8/D9 trait floors, D10 substrate-coherent generation, D26 cross-doc updates)
- § 7 — Recommendation: Phase-1 P1 extension or Phase-2? (your judgment with cosmological-vs-pragmatic tension named)
- § 8 — Decision-by window for Matt (suggest ~24-48 hours; the longer he waits the more rework if Phase-1 P1 extension)

---

## Out of scope (DO NOT)

- ❌ DO NOT write engine code, simulation code, or demo code (design briefing only)
- ❌ DO NOT amend gamora's D10 math note (yet — D10 substrate-coherent generation may need to consume this design once Matt L3-decides)
- ❌ DO NOT preempt Matt's scope decision (your briefing's § 7 recommendation, not a unilateral choice)
- ❌ DO NOT extend scope to other gameplay-mechanic design surfaces noticed during this work. Park them as OBSERVATION in hive log.
- ❌ DO NOT touch drax-demo v0.26 cosmetic dodge primitive (that's intentionally minimal; canonical mechanic supersedes it later)

---

## Acceptance criteria

- [ ] L3 briefing doc authored at `canonical/story/dodge-plus-telegraphed-combat-l3-briefing-2026-05-17.md`
- [ ] All 3 design surfaces addressed with explicit recommendations + alternatives + cosmological rationale
- [ ] Scope estimate breakdown per § 5
- [ ] Cross-impact map per § 6 (touches at least D27, D14, D8/D9, D10, D26)
- [ ] Phase-1 P1 extension vs Phase-2 recommendation in § 7
- [ ] Knight-rider notified (via hive-log HANDOFF) when ready to surface to Matt
- [ ] Tag `gandalf/v1.2-dodge-and-telegraphed-combat-l3-briefing-1` at the doc commit
- [ ] Hive-log STATE + HANDOFF entries

---

## Math-before-code requirements

N/A — design briefing; no engine math involved.

---

## Hive log discipline

PRE-SIGNAL before hive-log append (per § 14.1.1 race-condition discipline you authored). `git fetch origin` first; conflict-check; pull-rebase if concurrent commits.

---

## Coordination notes

- **Matt is currently weighing Phase-1 P1 extension vs Phase-2** for this design surface. Your briefing § 7 recommendation will inform his L3 decision.
- **In flight in parallel:** gamora pre-D10 standard-demo regen (~1-2 days); drax-demo v0.26 cosmetic dodge primitive (~1-2 hours). Neither blocks this briefing; this briefing potentially affects both downstream regens + the canonical dodge that supersedes drax's placeholder.
- **D8/D9 trait pools you authored may already imply telegraph/escape mechanics.** If you notice this during the briefing, surface explicitly — some traits may need amendment if telegraphed combat lands canonically.
- **Continuous-availability ramp:** stay LIVE for Matt L3 follow-up Q&A after briefing surfaces.

---

*Dispatched 2026-05-17 by knight-rider per Matt focused-playtest test 6 son feedback + L3 standing authority. Estimated 1-2 days. Append completion record to dispatch file when done.*

---

## Completion record (appended 2026-05-17 by gandalf)

**Status:** COMPLETE.
**Tag:** `gandalf/v1.2-dodge-and-telegraphed-combat-l3-briefing-1`
**Deliverable:** `canonical/story/dodge-plus-telegraphed-combat-l3-briefing-2026-05-17.md` (~775 lines)
**Effort:** ~1 day (within 1-2 day budget; absorbed faster than estimate because canonical 32 § 12.5 had ~80% of B13 design pre-resolved per Matt's 2026-05-11 design conversation; this briefing applies the pre-decided design surface to the Phase-1 P1 context with substrate-identity declaration overlay).

### Acceptance criteria check

- [x] L3 briefing doc authored at `canonical/story/dodge-plus-telegraphed-combat-l3-briefing-2026-05-17.md`
- [x] All 3 design surfaces addressed with explicit recommendations + alternatives + cosmological rationale (§ 2, § 3, § 4)
- [x] Scope estimate breakdown per § 5 (§ 5.1 narrow slice ~11 days; § 5.2 full B13 deferred per existing roadmap; § 5.3 Phase-2 deferral cost analysis)
- [x] Cross-impact map per § 6 (touches D27, D14, D8/D9, D10, D26, drax v0.26)
- [x] Phase-1 P1 extension vs Phase-2 recommendation in § 7 — **PARTIAL Phase-1 P1 extension recommended** (narrow slice only; defer full B13 to existing post-VS2a slot)
- [x] Knight-rider notified via hive-log HANDOFF
- [x] Tag pending at commit landing (atomic with this completion record)
- [x] Hive-log STATE + HANDOFF entries appended (PRE-SIGNAL'd per § 14.1.1)

### Key recommendation

**§ 7 — PARTIAL Phase-1 P1 extension** (narrow slice ~11 days = ~13% scope add):

1. Engine-coupled dodge mechanic (universal `Shift`-key; distance + i-frame hybrid; 4-5s cooldown; substrate-VFX-coupled animation)
2. Enemy-AOE telegraph indicator system (per-substrate windup character; 2 new engine schema fields)
3. Elite-tier reactive escape AI behavior
4. Cross-doc updates (canonical 32 § 12.5 amendment; canonical 16 B13 scope-reduction note; substrate-identity-declarations § 9 amendment-note; decisions-log entry)

**Defer to B13-proper post-VS2a:** 5 defensive mobility geometries as kit-pool, mini-boss/boss strategic + anticipatory escape, substrate-coherent boss escape directions, archetype-emergence observability for kit-mobility.

**Rationale:** The narrow slice exists because D27 perception test requires spatial-combat substrate to produce signal (the substrate identity declarations' `geometry_affinities` + `cosmological_commitment` fields ALL presuppose positioning decides outcomes). Anything more is mission-creep against an existing post-VS2a B13 slot.

### 7 open questions surfaced to Matt (briefing § 9)

1. Universal dodge vs per-class mobility
2. Cooldown structure (4-5s shared vs charges-based)
3. Earth/wind dodge numerical asymmetry
4. Player-AOE telegraph policy
5. Shadow late-commit indicator semantics
6. Narrow slice vs full B13 vs Phase-2 deferral
7. Cross-doc amendment authoring path

### Continuous-availability ramp

Per dispatch coordination note + protocol § 3.3: gandalf stays LIVE for Matt L3 follow-up Q&A.

— gandalf
