# Arcade / Minigame Template Taxonomy — *Reap. Die. Rise.*

> **STATUS:** CANONICAL — **POST-LAUNCH SCOPE** (2026-07-07). **Nothing in this spec gates the One Realm MVP / demo lanes.** It is parked, not pending: all build-side work (runtime primitives, packet-schema ratification, fitness math) waits behind the §9.1 endgame fork, which is due at **launch-scope planning** — `gates-on: launch-scope-planning`. The one exception to "post-launch" is that fork itself: if Matt rules EMBRACE, Rung 1 becomes launch-adjacent endgame scope (see §6 + §9.1).
> **Lineage:** Matt mobile-conversation draft `matt_notes_handoff_docs/reap-die-rise-minigame-template-taxonomy.md` (now bannered superseded-by-canon) · gandalf intake review `agentic_orchestration/gandalf/notes/2026-07-07-minigame-taxonomy-review.md` (verdict: SOUND, four flags — all four absorbed here). Matt ruled "agree on all" 2026-07-07.
> **Author of record:** Matt (draft) · gandalf (canonization + six amendments, marked ⟨AMENDED⟩ inline).
> **Owners at build time:** drax (arcade runtime, Godot) · gamora (sim-side fitness/certification primitives) · star-lord (packet emission) · gandalf (fitness design-spec-as-math, per Discipline #18).

---

## 0. Strategy context (settled)

Minigames debut as **activities inside the main game, vs. bots** — not as a standalone product. The main game must stand alone; the arcade is a staged windfall layer. Kit-vocabulary legibility comes from main-game play (you learn kits by reaping and fighting them — the claimed-souls register, see §8 fiction note); rule legibility comes from the template lattice below. **Kit tranches flow into both surfaces on a shared rotation cycle**, so the kits players learn in the current tranche are the kits the minigames draw from. ⟨AMENDED: the draft's "seasonal tranches" vocabulary reframed per the retired season-N release model (OP §3.7(b)); the live-ops cadence gets a deliberate public name later — §9.2. The underlying concept — synchronized content tranches feeding both surfaces — is unchanged.⟩

**Design virtue worth stating (⟨AMENDED — was implicit⟩):** the main game is certified **solo-only**; the arcade is the pressure valve. Co-op/PvP demand gets a home here that never forces the main loop to compromise its solo certification.

---

## 1. Design Laws (non-negotiable)

**LAW 1 — Minigames are packets, not code.** A minigame is a data packet interpreted by ONE arcade runtime in Godot. Adding a mode = emitting a packet with zero engine changes. If a mode requires engine work, that work is a new *runtime primitive* (§3/§4 effort tags), never a bespoke scene. *(This is the project's own spine — emission → packet → deterministic interpretation — extended to game modes.)*

**LAW 2 — The template lattice.** Generation happens ONLY within the recognized templates in §5. A packet = template + parameters + kit slice + exactly ONE twist. Template = rule legibility; generation = novelty. Free-form rule emission is prohibited.

**LAW 3 — Vocabulary from the main game.** Minigame kit pools draw from kits the player population has met in main-game play (tranche-synchronized rotation ⟨AMENDED vocab⟩). Never front a minigame with a majority-unfamiliar kit slice.

**LAW 4 — The cross-benefit membrane: cosmetic + QoL ONLY, both directions.**
The bright-line test: **if it changes the state of any fight or match, it does not cross.**
- Main game → minigames: cosmetics display in matches (restyle skins, soul-weapon manifestation styles, titles, VFX tints); QoL conveniences (saved loadouts, draft presets). NEVER: soul level, gear operators, stats, consumables.
- Minigames → main game: cosmetic trophies (hub banners, kit skins, death-style recolor variants, titles, emotes); QoL (stash tab, loot-filter presets, extra loadout slots). NEVER: XP/soul-level, gear, power-purchasing currency, drop-rate or magnitude modifiers of any kind.
- **Structural enforcement:** the minigame reward registry contains only `cosmetic` and `qol` reward types. No power category exists in the schema, so the law cannot be violated by content emission.
- Rationale: protects the sim's fairness certification (no external power injection into certified matches) and prevents forced-mode resentment (neither surface is mandatory for the other). Genre graveyard fenced off: Diablo Immortal's power-crossing resentment; D3 RMAH poisoning the loot thrill. Keeps the dependency asymmetric: each surface remains whole without the other.
- **Compatibility with the cleansed-crossing law (⟨AMENDED — clarifying, main-game loot spec §6⟩):** arcade rewards are hub/meta-layer objects (the Grimoire's persistence register), never run-scale loot — so the gear-stays-unless-cemented law is never touched. Compatible by construction.

Gray-zone adjudications (a living table — extend per case, decisions-log discipline):

| Proposal | Ruling | Why |
|---|---|---|
| Cosmetic pet that picks up gold in main game | BANNED | touches in-run economy — **the ban is on the CROSSING, not on pets; the main game's own (deferred) pet system is unaffected by this law** ⟨AMENDED clarification⟩ |
| Alternate announcer/voice pack in minigames | ALLOWED | presentation only |
| Draft-timer extension | BANNED | alters match state/pressure |
| Extra kit-preview slots in draft UI | ALLOWED | out-of-match information layout |
| XP/soul-level "boost weekend" from arcade play | BANNED | power pacing |
| Bot-sparring room unlock in hub | ALLOWED | QoL practice space, no rewards inside |

**LAW 5 — Bots-first.** Every template must be fully playable solo/co-op vs. bots on day one (shared player/AI kit pool + utility-AI controller). Real-time human PvP is a per-template later decision. Rungs 1–3 (§6) require ZERO real-time netcode (bots + async ladders only).

**LAW 6 — Two-tier certification.** The sim certifies **fairness** pre-ship (per-template fitness functions in §5; reuse the degenerate-combo blacklist machinery from the loot system for draft pools and wave compositions). Play data certifies **fun** post-ship (retention/replay/quit-curve per packet feeds back into template fitness weights). *Kits converge on balance; minigame packets converge on fun.* No packet ships uncertified. **Scope caveat (⟨AMENDED⟩): the sim can only certify what it can simulate — see §4 two-axis tags for where certification itself needs new sim primitives.**

---

## 2. Packet Schema (shared core — PROPOSED, ratified at build time)

```json
{
  "packet_type": "minigame",
  "template_id": "horde_survival | hero_line_wars | ...",
  "template_version": "semver",
  "display": { "name": "...", "blurb": "...", "icon_hint": "..." },
  "kit_pool": { "slice_ref": "...", "explicit_kits": [], "draft_rules": {} },
  "arena": { "arena_ref": "...", "params": {} },
  "economy": { "currencies": [], "income": {}, "spend_actions": [] },
  "waves": { "composition_refs": [], "cadence": {}, "scaling": {} },
  "objectives": { "win": {}, "lose": {}, "timers": {} },
  "twist": { "twist_id": "...", "params": {} },
  "bots": { "roles": [], "difficulty_bands": [] },
  "rewards": { "cosmetic_ids": [], "qol_ids": [] },
  "fitness_report": { "certified": false, "band_metrics": {} }
}
```

Fields are nullable per template. `display.name` follows the loot-naming constraint: **the name must signal template + twist** ("Emberline Wars — Double Send"), never opaque flavor — C5 readable-compression + D1 vocabulary-commonness carry over verbatim. Template names are fixed and authored (players learn the ~10); instance names are generated under the constraint.

---

## 3. Runtime Primitives

Templates are combinations of primitives. The arcade runtime implements primitives once; templates reuse them.

- **WAVES** — spawn compositions on cadence with scaling (exists: this is the battle sim's native shape)
- **ECONOMY/SEND** — income, spend actions, including spending to send waves at an opponent
- **DRAFT** — timed selection from a kit/ability slice with pick/ban rules
- **OBJECTIVE** — win/lose conditions: survive, control zone, escort payload, destroy structure, score/time attack
- **ASYMMETRY** — unequal roles (hunter/survivors; heroes/horde-commander)
- **PLACEMENT** — build static entities on a grid/points (towers, fortifications) — *new engine work*
- **PHYSICS/AIM** — knockback, displacement, hazards (shrinking arena) — *new engine work*

---

## 4. Effort Tags — TWO-AXIS ⟨AMENDED⟩

The draft's single tag under-counted the sim side: **LAW 6 says the sim certifies fairness, but the sim cannot certify what it cannot simulate.** Warlock fitness (TTK, ring-out ratio, kingmaker index) needs displacement/collision the battle sim does not model; TD fitness (leak curves, maze diversity) needs pathing + static entities. So a T2 template is new **runtime** primitives (drax seam) AND new **sim/certification** primitives (gamora seam) — two seams, roughly double the single-tag cost. Tags are now `runtime × sim`:

- **T0** = pure reuse of existing machinery (on that axis)
- **T1** = new logic, no new primitives (on that axis)
- **T2** = new primitives required (on that axis)

This strengthens the draft's own conclusion: defer T2×T2 templates until arcade traction earns the double investment.

---

## 5. The Template Taxonomy

### 5.0 Taxonomy-level registers ⟨AMENDED — two new columns + two-axis tags⟩

Session-length: WC3 customs lived at 15–45 min; an *in-game activity* bands at **5–20 min** (taxonomy-wide law; per-template bands below are gandalf initial proposals, ratified per-packet at certification). Touch-viability: mobile-class specs are a standing contingency target (One Realm Q11 language); this column steers sequencing cheaply.

| Template | Effort (runtime × sim) | Session band (initial) | Touch viability |
|---|---|---|---|
| 5.1 Horde Survival | T0 × T0 | 5–15 min (banded endless OK) | HIGH |
| 5.2 Hero Line Wars | T1 × T1 | 10–20 min | MEDIUM (economy UI density) |
| 5.3 Kit-Draft Gauntlet | T1 × T1 | 10–20 min | HIGH (draft is tap-native) |
| 5.4 Footmen Frenzy | T1 × T1 | 10–20 min | MEDIUM |
| 5.5 Boss Rush | T1 × T0 | 5–15 min | HIGH |
| 5.6 Tower/Hero Defense | **T2 × T2** (PLACEMENT + pathing/static sim) | 10–20 min | LOW-MEDIUM (placement UI) |
| 5.7 Warlock Arena | **T2 × T2** (PHYSICS/AIM + displacement/collision sim) | 3–8 min rounds | LOW (aim precision) |
| 5.8 Asymmetric Tag | T1 × T1 (hunter-bot hard) | 5–12 min | MEDIUM |
| 5.9 Payload Escort | T1 × T1 | 8–15 min | HIGH |
| 5.10 Control / KotH | T1 × T1 | 8–15 min | MEDIUM |

### 5.1 HORDE SURVIVAL — **RUNG 1, debut in-game activity**
*Lineage:* Enfo's Team Survival / Sunken Defense.
*Pitch:* co-op/solo waves-vs-you; survive rounds or last as long as possible.
*Structure:* WAVES + OBJECTIVE(survive/score). Players pick or draft kits; waves composed from the kit pool (trash-weighted, elite spikes).
*Why first:* it is literally the battle sim with a camera on it — least new rule logic, proves packet → runtime → feel end to end, and doubles as main-game endgame content. **⚠ That last clause is the §9.1 endgame fork — the only load-bearing decision in this layer. See §6.**
*Bots:* co-op bot allies trivially (shared pool).
*Fitness:* survival-time distribution in band; KPM band; wipe-curve smoothness (difficulty ramp has no cliff); AOE% (density fun signal); kit-viability spread (no dead kits vs. the wave set).

### 5.2 HERO LINE WARS — **RUNG 2, first competitive mode**
*Lineage:* Hero Line Wars / Legion TD adjacency.
*Pitch:* dual-lane economy duel — spend income to SEND waves at the opponent and/or hold your own lane with your kit.
*Structure:* WAVES + ECONOMY/SEND + OBJECTIVE(outlast).
*Why it fits the constraint:* competition flows **through the hordes**, never through hero duels — sidesteps kits-not-1v1-tuned entirely.
*Bots:* opponent = an economy-policy bot (tractable; policy over send/defend spend). Ship competitive with bot opponents FIRST — no netcode.
*Fitness:* send-vs-defend equilibrium (no dominant strategy across the kit slice); game-length band; comeback index; per-kit clear fairness vs. sendable compositions (reuse blacklist for degenerate send-combos).

### 5.3 KIT-DRAFT GAUNTLET — **RUNG 3, the moat showcase**
*Lineage:* Custom Hero Wars / X Hero Siege.
*Pitch:* draft a kit (or composite abilities) from a rotating slice, then run a co-op siege/boss gauntlet; score attack.
*Structure:* DRAFT + WAVES + OBJECTIVE(score/time).
*Competition without netcode:* **async leaderboards + score ghosts** — human competition, zero real-time infra. ⟨AMENDED note: the sim's seeded determinism means **the replay IS the ghost format** — input-traces + seeds, no video, no server-side replay engine; §9.4 largely answers itself.⟩
*Bots:* co-op allies from the pool.
*Fitness:* draft-pool balance via sim self-play pick-rate entropy (no dominant pick); clear-time distribution per draft archetype; outlier-combo detection (blacklist machinery).

### 5.4 FOOTMEN FRENZY
*Lineage:* Footmen Frenzy.
*Pitch:* 3–4 teams; bases auto-spawn armies; you pilot a hero kit and buy spawn-tier upgrades; last team standing.
*Structure:* WAVES(auto) + ECONOMY + OBJECTIVE(elimination).
*Fitness:* elimination pacing band; snowball index (first-advantage → win correlation stays in band); hero-impact share (hero decides neither 0% nor 100% of outcomes).

### 5.5 BOSS RUSH / RAID GAUNTLET
*Lineage:* X Hero Siege finales / ORPG raid rooms.
*Pitch:* co-op sequential generated bosses (bosses ARE scaled kits); time/score attack; async ladder.
*Structure:* WAVES(elite) + optional DRAFT + OBJECTIVE(score/time).
*Synergy:* highest main-game reuse (boss kits, arenas); async-competitive. ⟨AMENDED note: "bosses ARE scaled kits" lands on the already-confirmed trial-room boss-gallery design intent — see §8 fiction note.⟩
*Fitness:* per-boss wipe-rate band; phase-length distribution; kit-viability spread vs. the boss roster.

### 5.6 TOWER / HERO DEFENSE
*Lineage:* Wintermaul / Element TD, with a piloted hero.
*Pitch:* place static defenses + pilot a kit; waves path through.
*Structure:* WAVES + ECONOMY + PLACEMENT + OBJECTIVE(leak limit).
*Fitness:* leak-curve shape; build diversity (no dominant tower line/maze); hero-vs-tower contribution band.
*Sequencing note:* deferred until the PLACEMENT primitive (both axes — runtime AND sim pathing) is justified by arcade traction.

### 5.7 WARLOCK ARENA
*Lineage:* Warlock.
*Pitch:* AOE-knockback last-man-standing on a shrinking hazard arena; FFA or teams.
*Structure:* PHYSICS/AIM + OBJECTIVE(elimination).
*Kit handling:* restrict the slice to displacement/AOE-capable kits (the agnostic-operator search can select for "displacement-capable" — same machinery, new predicate). FFA + physics chaos keeps it party-shaped, not duel-shaped; still the template most sensitive to the no-1v1-tuning constraint — certify hard.
*Fitness:* time-to-kill band; ring-out vs. damage kill ratio; kingmaker index in FFA.

### 5.8 ASYMMETRIC TAG
*Lineage:* Vampirism / Tree Tag / Sheep Tag.
*Pitch:* one hunter converts/kills survivors who fortify and hide; survivors win on timer.
*Structure:* ASYMMETRY + ECONOMY(fortify) + OBJECTIVE(timer).
*Bots:* survivor bots easy; hunter bot needs search behavior — sequence later.
*Fitness:* hunter win-rate band across kit slices; time-to-first-conversion; map hiding-entropy (arena fairness).

### 5.9 PAYLOAD / CARAVAN ESCORT
*Lineage:* escort customs; attack/defend.
*Pitch:* escort a caravan through horde territory; opposition (bots or players) spends to intercept.
*Structure:* OBJECTIVE(moving) + WAVES + ECONOMY.
*Note:* naturally in-world-venue friendly for the activity debut form.
*Fitness:* push-rate band; checkpoint variance; defender comeback index.

### 5.10 CONTROL / KING OF THE HILL
*Lineage:* control customs / Angel Arena adjacency.
*Pitch:* teams contest control zones under neutral horde pressure; zones are taken by AOE clear and body-mass, not duels.
*Structure:* OBJECTIVE(control) + WAVES(neutral).
*Fitness:* zone-flip cadence; stalemate detection; multi-team balance.

### 5.11 (Wrapper, not a template) PARTY COLLECTION
*Lineage:* Uther Party. A rotating playlist of short instances from templates above — the eventual "arcade night" wrapper once ≥5 templates exist. No new machinery; a scheduling layer.

---

## 6. Debut Order & Rung Logic

1. **Rung 1 — Horde Survival** as an in-game activity (solo/co-op vs. bots). Proves the packet runtime; doubles as endgame content. Gate to advance: a new packet variant ships with zero engine changes; fairness certification runs green; players replay it.
2. **Rung 2 — Hero Line Wars** vs. bot opponents. First competitive rules, still zero netcode. Gate: economy fitness holds in live play-data; players choose it repeatedly over Rung 1.
3. **Rung 3 — Kit-Draft Gauntlet** with async ladders/ghosts. Human competition begins, still zero real-time netcode. Gate: draft-pool entropy healthy in the wild; ladder participation.
4. **Then:** Footmen Frenzy, Boss Rush (max reuse) → PLACEMENT/PHYSICS templates (TD, Warlock) only if the arcade surface has earned the two-axis engine investment → Asymmetric Tag, Escort, Control → Party wrapper.
5. **Real-time PvP netcode** is a per-template decision made only after rung 3 proves demand. It is never a prerequisite for shipping the arcade.

**⟨AMENDED — the scope-gravity flag (the strategic finding, review §3.2):** the strategy header calls the arcade a "staged windfall layer," but Rung 1 "doubles as main-game endgame content." ARPG law: **the game begins at endgame** (D3 vanilla → Reaper of Souls is the canonical lesson; Rifts entered as a side mode and became the game). If horde survival IS the endgame answer, Rung 1 is launch-adjacent and the packet runtime rides the critical path earlier than "post-launch" admits. That contradiction is not resolved here — it is the §9.1 fork, due at launch-scope planning, and it must be a deliberate ruling, not drift.⟩

---

## 7. Certification Pipeline (per packet)

1. Emit packet (template + params + kit slice + twist) from the content pipeline.
2. Sim runs the template's fitness function across the kit slice (self-play where the template is competitive). Reuse gauntlet metrics + blacklist.
3. Out-of-band → clamp params / reslice kits / reject twist → re-emit.
4. Stamp `fitness_report.certified = true`; only certified packets reach the activity board.
5. Post-ship: play-data (replay rate, quit curve, session length vs. the §5.0 band) updates template fitness weights — the convergence loop, one level up the stack.

**Fitness definitions are a named handoff, not a flaw:** comeback/snowball/kingmaker indices and hiding-entropy are undefined at taxonomy level — correct. At build time these are design-spec-as-math (gandalf) → gamora, per Discipline #18 (methodology consultation at the hotspot).

---

## 8. Out of Scope (deliberately)

- Story/venue integration for activities (narrative layer is shelved; a placeholder "activity board" hub entry suffices). **⟨AMENDED — fiction note, nearly free when wanted:** the fiction is half-built and already in canon. "You learn kits by reaping and fighting them" = the claimed-souls register (gameplay-loop §11 capture-and-summon; two-register Grimoire). Boss Rush's "bosses ARE scaled kits" = the confirmed trial-room boss-gallery intent. When the activity board earns a diegetic name, it isn't an invention — it's the faith's **trial-grounds**: reapers sparring against bound souls. One story-session line, whenever wanted (§9.5).⟩
- The standalone arcade product decision (deferred until rungs prove out — "future-product scope" in canon vocabulary).
- Real-time netcode architecture.
- Reward *content* design (which cosmetics/QoL items) — only the membrane law (LAW 4) is fixed here.

---

## 9. Open Decisions (⟨AMENDED — expanded from the draft's four⟩)

1. **THE ENDGAME FORK (load-bearing — `gates-on: launch-scope-planning`):** (a) **EMBRACE** — design main-game endgame AS arcade-rung-1; the packet runtime becomes launch scope; or (b) **FENCE** — endgame is a separate design; the arcade debuts strictly post-launch. gandalf lean: (a) — it's where D3/PoE history points, and it's the cheapest possible endgame ("literally the battle sim with a camera on it") — but Matt rules it at launch-scope planning, not before. Everything else in this spec waits behind this fork.
2. **Live-ops cadence naming** — the public-facing successor term for the retired "season" vocabulary (PoE leagues / D3 seasons are the genre convention; may even ship publicly as "seasons" — but Matt names it deliberately, later).
3. **Packets-per-cycle cadence** (weekly instance rotation vs. monthly tranche).
4. **Async-ladder infrastructure** — largely self-answering per §5.3: seeded determinism ⇒ input-traces + seeds ARE the ghost format; remaining question is leaderboard host only.
5. **Diegetic frame** for the activity board (the §8 trial-grounds hook — one story-session line).
6. **Whether Rung 1 debuts inside an existing descent** (an anomaly room) or on a hub activity board.
7. **Whether Warlock's PHYSICS primitives ever justify their two-axis cost**, given it's the most constraint-sensitive template.
8. **Touch-viability per template** — ratify the §5.0 column if/when a mobile-class spec activates (One Realm Q11 contingency).

---

**Sign-off:** gandalf, 2026-07-07 (CANON-STEWARD absorption; Matt "agree on all"). Anchors: Matt mobile draft (lineage above) · intake review 2026-07-07 · gameplay-loop-design.md §11 (claimed souls) · loot spec §6 (cleansed crossing) · OP §3.7(b) (season vocabulary) · Discipline #18 (fitness math handoff). *The arcade's first rung is secretly an endgame system wearing a party hat — §9.1 decides which costume is real; everything else here waits exactly as long as it claims it can.*
