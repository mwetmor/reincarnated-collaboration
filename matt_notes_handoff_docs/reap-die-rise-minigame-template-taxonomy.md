# Reap. Die. Rise. — Minigame Template Taxonomy & Arcade Spec

> **⚠ SUPERSEDED BY CANON (2026-07-07)** — absorbed into `canonical/reap-die-rise-game/arcade-minigame-taxonomy-spec.md` (POST-LAUNCH SCOPE) with six gandalf amendments per the intake review (`agentic_orchestration/gandalf/notes/2026-07-07-minigame-taxonomy-review.md`); Matt ruled "agree on all" 2026-07-07. **The canonical spec governs.** This draft is retained as lineage only (same precedent as the agnostic-loot mobile draft, 2026-07-06).

**Audience:** the build team (Claude agent team on the Mac).
**Status:** ~~design spec for the minigame/arcade layer~~ SUPERSEDED — see banner. Depends on: the existing content-emission pipeline, the battle sim + gauntlet fitness machinery, the shared player/AI kit pool, the serial JSON packet contract, and the agnostic-loot validation machinery (blacklist reuse).
**Strategy context (settled):** minigames debut as **activities inside the main game, vs. bots** — not as a standalone product. The main game must stand alone; the arcade is a staged windfall layer. Kit-vocabulary legibility comes from main-game play (you learn kits by reaping and fighting them); rule legibility comes from the template lattice below. Seasonal kit tranches flow into both surfaces so the kits players learn each season are the kits the minigames draw from.

---

## 1. Design Laws (non-negotiable)

**LAW 1 — Minigames are packets, not code.** A minigame is a data packet interpreted by ONE arcade runtime in Godot. Adding a mode = emitting a packet with zero engine changes. If a mode requires engine work, that work is a new *runtime primitive* (see §4 effort tags), never a bespoke scene.

**LAW 2 — The template lattice.** Generation happens ONLY within the recognized templates in §5. A packet = template + parameters + kit slice + exactly ONE twist. Template = rule legibility; generation = novelty. Free-form rule emission is prohibited.

**LAW 3 — Vocabulary from the main game.** Minigame kit pools draw from kits the player population has met in main-game play (season-synchronized tranches). Never front a minigame with a majority-unfamiliar kit slice.

**LAW 4 — The cross-benefit membrane: cosmetic + QoL ONLY, both directions.**
The bright-line test: **if it changes the state of any fight or match, it does not cross.**
- Main game → minigames: cosmetics display in matches (restyle skins, soul-weapon manifestation styles, titles, VFX tints); QoL conveniences (saved loadouts, draft presets). NEVER: soul level, gear operators, stats, consumables.
- Minigames → main game: cosmetic trophies (hub banners, kit skins, death-style recolor variants, titles, emotes); QoL (stash tab, loot-filter presets, extra loadout slots). NEVER: XP/soul-level, gear, power-purchasing currency, drop-rate or magnitude modifiers of any kind.
- **Structural enforcement:** the minigame reward registry contains only `cosmetic` and `qol` reward types. No power category exists in the schema, so the law cannot be violated by content emission.
- Rationale: protects the sim's fairness certification (no external power injection into certified matches) and prevents forced-mode resentment (neither surface is mandatory for the other). Keeps the dependency asymmetric: each surface remains whole without the other.

Gray-zone adjudications (extend this table as cases arise):

| Proposal | Ruling | Why |
|---|---|---|
| Cosmetic pet that picks up gold in main game | BANNED | touches in-run economy |
| Alternate announcer/voice pack in minigames | ALLOWED | presentation only |
| Draft-timer extension | BANNED | alters match state/pressure |
| Extra kit-preview slots in draft UI | ALLOWED | out-of-match information layout |
| XP/soul-level "boost weekend" from arcade play | BANNED | power pacing |
| Bot-sparring room unlock in hub | ALLOWED | QoL practice space, no rewards inside |

**LAW 5 — Bots-first.** Every template must be fully playable solo/co-op vs. bots on day one (shared player/AI kit pool + utility-AI controller). Real-time human PvP is a per-template later decision. Rungs 1–3 below require ZERO real-time netcode (bots + async ladders only).

**LAW 6 — Two-tier certification.** The sim certifies **fairness** pre-ship (per-template fitness functions in §5; reuse the degenerate-combo blacklist machinery from the loot system for draft pools and wave compositions). Play data certifies **fun** post-ship (retention/replay/quit-curve per packet feeds back into template fitness weights). Kits converge on balance; minigame packets converge on fun. No packet ships uncertified.

---

## 2. Packet Schema (shared core)

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
Fields are nullable per template. `display.name` follows the loot-naming constraint: **the name must signal template + twist** ("Emberline Wars — Double Send"), never opaque flavor. Template names are fixed and authored (players learn the ~10); instance names are generated under the constraint.

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

## 4. Effort Tags

- **T0** = pure reuse of existing sim/kit machinery
- **T1** = new runtime logic, no new engine primitives
- **T2** = requires PLACEMENT or PHYSICS/AIM primitives

---

## 5. The Template Taxonomy

### 5.1 HORDE SURVIVAL — **RUNG 1, debut in-game activity** (T0)
*Lineage:* Enfo's Team Survival / Sunken Defense.
*Pitch:* co-op/solo waves-vs-you; survive rounds or last as long as possible.
*Structure:* WAVES + OBJECTIVE(survive/score). Players pick or draft kits; waves composed from the kit pool (trash-weighted, elite spikes).
*Why first:* it is literally the battle sim with a camera on it — least new rule logic, proves packet → runtime → feel end to end, and doubles as main-game endgame content.
*Bots:* co-op bot allies trivially (shared pool).
*Fitness:* survival-time distribution in band; KPM band; wipe-curve smoothness (difficulty ramp has no cliff); AOE% (density fun signal); kit-viability spread (no dead kits vs. the wave set).

### 5.2 HERO LINE WARS — **RUNG 2, first competitive mode** (T1)
*Lineage:* Hero Line Wars / Legion TD adjacency.
*Pitch:* dual-lane economy duel — spend income to SEND waves at the opponent and/or hold your own lane with your kit.
*Structure:* WAVES + ECONOMY/SEND + OBJECTIVE(outlast).
*Why it fits the constraint:* competition flows **through the hordes**, never through hero duels — sidesteps kits-not-1v1-tuned entirely.
*Bots:* opponent = an economy-policy bot (tractable; policy over send/defend spend). Ship competitive with bot opponents FIRST — no netcode.
*Fitness:* send-vs-defend equilibrium (no dominant strategy across the kit slice); game-length band; comeback index; per-kit clear fairness vs. sendable compositions (reuse blacklist for degenerate send-combos).

### 5.3 KIT-DRAFT GAUNTLET — **RUNG 3, the moat showcase** (T1)
*Lineage:* Custom Hero Wars / X Hero Siege.
*Pitch:* draft a kit (or composite abilities) from a rotating slice, then run a co-op siege/boss gauntlet; score attack.
*Structure:* DRAFT + WAVES + OBJECTIVE(score/time).
*Competition without netcode:* **async leaderboards + score ghosts** — human competition, zero real-time infra.
*Bots:* co-op allies from the pool.
*Fitness:* draft-pool balance via sim self-play pick-rate entropy (no dominant pick); clear-time distribution per draft archetype; outlier-combo detection (blacklist machinery).

### 5.4 FOOTMEN FRENZY (T1)
*Lineage:* Footmen Frenzy.
*Pitch:* 3–4 teams; bases auto-spawn armies; you pilot a hero kit and buy spawn-tier upgrades; last team standing.
*Structure:* WAVES(auto) + ECONOMY + OBJECTIVE(elimination).
*Fitness:* elimination pacing band; snowball index (first-advantage → win correlation stays in band); hero-impact share (hero decides neither 0% nor 100% of outcomes).

### 5.5 BOSS RUSH / RAID GAUNTLET (T1)
*Lineage:* X Hero Siege finales / ORPG raid rooms.
*Pitch:* co-op sequential generated bosses (bosses ARE scaled kits); time/score attack; async ladder.
*Structure:* WAVES(elite) + optional DRAFT + OBJECTIVE(score/time).
*Synergy:* highest main-game reuse (boss kits, arenas); async-competitive.
*Fitness:* per-boss wipe-rate band; phase-length distribution; kit-viability spread vs. the boss roster.

### 5.6 TOWER / HERO DEFENSE (T2 — PLACEMENT)
*Lineage:* Wintermaul / Element TD, with a piloted hero.
*Pitch:* place static defenses + pilot a kit; waves path through.
*Structure:* WAVES + ECONOMY + PLACEMENT + OBJECTIVE(leak limit).
*Fitness:* leak-curve shape; build diversity (no dominant tower line/maze); hero-vs-tower contribution band.
*Sequencing note:* deferred until PLACEMENT primitive is justified by arcade traction.

### 5.7 WARLOCK ARENA (T2 — PHYSICS/AIM)
*Lineage:* Warlock.
*Pitch:* AOE-knockback last-man-standing on a shrinking hazard arena; FFA or teams.
*Structure:* PHYSICS/AIM + OBJECTIVE(elimination).
*Kit handling:* restrict the slice to displacement/AOE-capable kits (the agnostic-operator search can select for "displacement-capable" — same machinery, new predicate). FFA + physics chaos keeps it party-shaped, not duel-shaped; still the template most sensitive to the no-1v1-tuning constraint — certify hard.
*Fitness:* time-to-kill band; ring-out vs. damage kill ratio; kingmaker index in FFA.

### 5.8 ASYMMETRIC TAG (T1, hunter-bot is the hard part)
*Lineage:* Vampirism / Tree Tag / Sheep Tag.
*Pitch:* one hunter converts/kills survivors who fortify and hide; survivors win on timer.
*Structure:* ASYMMETRY + ECONOMY(fortify) + OBJECTIVE(timer).
*Bots:* survivor bots easy; hunter bot needs search behavior — sequence later.
*Fitness:* hunter win-rate band across kit slices; time-to-first-conversion; map hiding-entropy (arena fairness).

### 5.9 PAYLOAD / CARAVAN ESCORT (T1)
*Lineage:* escort customs; attack/defend.
*Pitch:* escort a caravan through horde territory; opposition (bots or players) spends to intercept.
*Structure:* OBJECTIVE(moving) + WAVES + ECONOMY.
*Note:* naturally in-world-venue friendly for the activity debut form.
*Fitness:* push-rate band; checkpoint variance; defender comeback index.

### 5.10 CONTROL / KING OF THE HILL (T1)
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
4. **Then:** Footmen Frenzy, Boss Rush (max reuse) → PLACEMENT/PHYSICS templates (TD, Warlock) only if the arcade surface has earned engine investment → Asymmetric Tag, Escort, Control → Party wrapper.
5. **Real-time PvP netcode** is a per-template decision made only after rung 3 proves demand. It is never a prerequisite for shipping the arcade.

---

## 7. Certification Pipeline (per packet)

1. Emit packet (template + params + kit slice + twist) from the content pipeline.
2. Sim runs the template's fitness function across the kit slice (self-play where the template is competitive). Reuse gauntlet metrics + blacklist.
3. Out-of-band → clamp params / reslice kits / reject twist → re-emit.
4. Stamp `fitness_report.certified = true`; only certified packets reach the activity board.
5. Post-ship: play-data (replay rate, quit curve, session length) updates template fitness weights — the convergence loop, one level up the stack.

---

## 8. Out of Scope (deliberately)

- Story/venue integration for activities (narrative layer is shelved; a placeholder "activity board" hub entry suffices).
- The standalone arcade product decision (deferred until rungs prove out).
- Real-time netcode architecture.
- Reward *content* design (which cosmetics/QoL items) — only the membrane law (§ LAW 4) is fixed here.

## 9. Open Decisions (flag for discussion)

- Packets per season cadence (weekly instance rotation vs. monthly tranche).
- Whether Warlock's PHYSICS primitives ever justify their cost, given it's the most constraint-sensitive template.
- Async-ladder infrastructure choice (ghost data format, leaderboard host).
- Whether Rung 1 debuts inside an existing descent (an anomaly room) or on a hub activity board.
