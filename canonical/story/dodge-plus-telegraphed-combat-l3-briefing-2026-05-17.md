# L3 Design Briefing — Dodge Mechanic + Telegraphed-Combat System

**Authority:** gandalf (story-and-design steward). L3 briefing per knight-rider dispatch 2026-05-17.
**Audience:** Matt (L3 decision: Phase-1 P1 scope extension vs Phase-2 deferral).
**Trigger:** Focused-playtest test 6 son feedback (2026-05-17) — son captured the missing-substrate from inside the engagement loop, in a single sentence Matt could not have written from outside: *"it would be way more fun if it seemed like the monsters could move out of range of your AOE and vice versa, if you could dodge roll out of the way, or run."*
**Companion artifacts:** `substrate-identity-declarations-2026-05-17.md`, `d8-trait-floor-design-phase-1-p1.md`, `d8-canonical-four-trait-pools-2026-05-18.md`, `canonical/32-progression-design.md` § 12.5, `canonical/16-project-roadmap.md` Stage A2 closeout (B13).

**Reading order:** § 0 TL;DR → § 1 Why this matters → § 2 Surface 1 (player dodge) → § 3 Surface 2 (telegraphed AOE) → § 4 Surface 3 (monster AI escape) → § 5 Scope estimate → § 6 Cross-impact map → § 7 Recommendation → § 8 Decision-by window → § 9 Open questions for Matt.

---

## § 0 — TL;DR

Three design surfaces, one substrate: **spatial combat with escape windows.** Without it, the canonical-7 substrate identities cannot perceptually distinguish themselves in play — `vortex_pull` vs `cone push-out` differ only in *where things go on the battlefield;* `persistent_zone` vs `burst` differ only in whether the monster could have *moved out;* `chain` vs `area_sustain` differ only in whether the player could *break the line.* All seven substrates' `geometry_affinities` assume positioning matters.

**Three surfaces:**

1. **Player dodge (§ 2)** — universal mechanic (Last Epoch precedent, NOT D4 universal Evade-style spam), `Shift`-key, 1-1.5s i-frame window, stamina-gated (4-5s shared cooldown), distance-based with brief i-frames inside, **animation-substrate-coupled** (fire flares forward; wind blinks; earth braces in-place; shadow steps; holy radiates outward; lightning arc-translates; water dissolves-and-reforms). The *mechanic* is universal; the *expression* is substrate-coupled.

2. **Telegraphed AOE (§ 3)** — all enemy AOEs telegraph; player AOEs do NOT telegraph (single-player ARPG convention). Per-substrate windup *character* (fire builds → red; water expands → blue ring growth; earth instant-but-persistent → brown; wind directional → cyan arrow; lightning instant-but-pre-warns-next-arc → yellow; holy slow radiant build → white; shadow late-commit → purple). Indicator geometry mirrors AOE hitbox per existing post-B11 lock (enemy 1.08×, player 0.92×).

3. **Monster AI escape (§ 4)** — tiered. **Trash mobs:** no escape (would clutter screen; D2/PoE precedent). **Elite mobs:** reactive escape on telegraphed-player-AOE (D3 precedent). **Mini-bosses:** strategic reposition + telegraphed enemy AOE. **Bosses:** strategic + anticipatory + substrate-coherent escape direction.

**Recommendation (§ 7):** **PARTIAL Phase-1 P1 extension** — fold a *narrow* slice (player dodge primitive promotion + enemy telegraph indicator + basic elite reactive escape) into Phase-1 P1 *because the D27 perception test depends on it.* Defer the *full* B13 substrate-coupled animation system + monster-AI-tier-stratification + i-frame-rule formalization to **B13-proper post-VS2a per existing roadmap.** Estimated narrow-slice extension: ~9-11 days; full Phase-1 P1 budget cost ~13%. Full B13 (the original scope) stays at ~3-4 weeks per file 16a.

The narrow slice exists because **the D27 perception test will produce false-negatives without it.** That's the only reason to extend Phase-1 P1.

---

## § 1 — Why this matters

### § 1.1 — The son saw the missing substrate

Matt's son's feedback is not a feature request. It is a **substrate identification** — a child sitting in front of the game and naming the thing the engine cannot do that prevents the engine from being what the engine claims to be. *"It feels like moves can't be escaped and monsters can't escape your moves."* That is the language of a player who has noticed that positioning does not decide outcomes. **All seven substrate identity declarations assume positioning decides outcomes.**

This is not a son-feedback dispatch. It is a son-revealed-architectural-gap dispatch.

### § 1.2 — The substrate identity declarations are conditional on this

Re-reading `substrate-identity-declarations-2026-05-17.md` with this gap surfaced:

- **Wind** `mechanical_signature: [displace, knockback, redirect, mobility]` — if monsters cannot be moved out of position by player abilities AND cannot move to evade, wind's identity collapses into "fire with cyan tint."
- **Earth** `cosmological_commitment: "the substrate of unyielding — what does not move and will not be moved"` — if no substrate moves, earth's commitment is unfalsifiable. The substrate cannot claim "I refuse to move" if nothing moves.
- **Fire** `combat_pillar: HIGH_BURST_LOW_PERSIST` vs **Water** `SUSTAINED_PRESENCE_ZONE_DENIAL` — these pillars are mechanically opposite *only if* monsters can move into and out of presence zones. Without movement, both pillars resolve identically into "do damage in a fixed area."
- **Lightning** `mechanical_signature: [chain, propagate, arc, discharge]` — chain only matters if monsters spread; if they cannot reposition, chain is identical to flat AOE.
- **Holy/shadow** — consecrate zones only matter if targets can enter or leave them. Concealment only matters if perception decides hit/miss windows.

**The substrate identity Layer-1 declarations are dependent on a Layer-0 spatial-combat substrate** that does not yet exist. The substrate-identity-declaration-spec deliberately does not specify this Layer-0 — it presupposes ARPG conventions. Son discovered the presupposition has not been honored.

### § 1.3 — The D27 perception test will report false negatives without it

Per `perception-test-experiment-scoping-2026-05-17.md` § 2: H1 tests whether *mechanically-distinct archetypes feel distinct in play.* The perception test puts a player in a 60-90 second fight against a fixed reference monster and asks "did Build A feel different from Build B?"

If positioning does not decide outcomes:

- Two fire_damage archetypes with statistically distinct `geometry_affinities` distributions will play identically (the geometry doesn't matter; the AOE hits regardless).
- A fire_damage vs water_controller archetype pair will feel distinguishable only at the LLM-flavor-vocabulary surface, not the mechanical-play surface.
- The perception-test's PRIMARY hypothesis (H1: pair-recovery accuracy) is testing whether the Layer-3 mirror-match diversity gate should ground on mechanical-parameter vector distance. **Without spatial combat, the player cannot perceive the very axis the gate gates against.**

The perception test as currently designed will likely fail H1 — and the failure mode will be **false-negative for the wrong reason**: not because substrate identity is wrong, but because the engagement loop cannot express it.

This is exactly the Phase-1 P1a perception-test risk § 7.2 anticipated ("90-second fight is too short for perception"). But the risk is not duration — the risk is **the engagement loop has no positional grammar for the substrate to speak.**

### § 1.4 — B13 was always going to ship — the question is *when*

Per `canonical/16a-roadmap-shipped-log.md` line 86: **B13 is queued.** Active mobility + telegraphs + i-frames + 5 defensive mobility geometries (roll/defensive_dash/strafe_mode/blink/dodge_stance) + cast_time + damage_resolution_time + i_frame_window fields + demo telegraphs + asymmetric indicator scaling. ~3-4 weeks engine + demo + regen. Originally scheduled for **Stage A2 closeout (post-VS2a)**.

Per `canonical/32-progression-design.md` § 12.5 (added 2026-05-11): the design is **mostly resolved.** 5 geometries locked. Last Epoch model adopted (per-class, not D4 universal). Statistical dodge stays. Active mobility layers on top. Telegraph indicator shape vs hitbox already discussed (player 0.92×, enemy 1.08×).

The engine substrate is also partially present: `damage_resolver.py` line 88 reserves `i_frame_window` as a registered parameter (currently metadata-only, does not affect VS2a damage). `fight_engine.py` line 436 already consumes `cast_time_seconds` from skill timing params. The plumbing is laid.

**This briefing is not new design. It is a question of acceleration — pull part of B13 forward into Phase-1 P1 because D27 depends on it, defer the rest to its existing B13 slot.**

---

## § 2 — Surface 1: Canonical dodge mechanic

### § 2.1 — Recommendation: universal mechanic, substrate-coupled animation

**Mechanic shape (universal across all classes):**

| Dimension | Recommended | Alternative considered | Rationale |
|---|---|---|---|
| **Universality** | Every class has dodge (input: `Shift` key) | Per-class mobility (Last Epoch model — only some classes) | Son's feedback specifically named dodge-roll as a player verb. Universal floor reduces "did I roll the wrong class" friction. The *expression* varies per substrate; the *availability* does not. |
| **i-frames vs distance** | **Both** — short distance (~3-4m) + brief i-frame window (~0.4s) inside | i-frames only (Smoke Screen-style stationary invuln) | Distance gives positional agency (the substrate son named: *"dodge roll out of the way"*). i-frames make the dodge feel decisive (Dark Souls/Elden Ring lineage). Distance-only would feel like Sprint (D3 Wizard); i-frames-only would feel like Smoke Screen (D3 DH). The hybrid is the genre-default (D4 Evade, Last Epoch Shift, PoE Dash). |
| **Cooldown** | **4-5s shared cooldown.** No charges. | Charges (2-3 charges, 4s recharge each — D4 Evade model) | Charges encourage spam and dilute the *decision* moment. Single-cooldown means "is this the moment to dodge?" stays load-bearing. Son's feedback was about *escape windows*, not *constant evasion.* |
| **Resource cost** | **Free** (cooldown only); does not consume stamina, mana, or energy | Stamina-gated (engine has `STAMINA_DODGE_COST = 15.0` per `combatant.py:40`) | Stamina-gated dodge has historical engine wiring but: (a) stamina is a hidden simulation stat not currently surfaced to players; (b) gating evasion behind a hidden stat punishes players for not seeing it; (c) the cooldown alone enforces rate-limiting. **The existing `STAMINA_DODGE_COST` constant tracks *statistical* dodge-roll cost, not *active* dodge — keep it for statistical evasion, do not extend to active dodge.** |
| **Cancel rules** | Cancels current cast (interrupts skill mid-windup); cancels LMB move/attack orders; **does NOT cleanse ailments** | Cleanse-on-dodge | Drax v0.26 cosmetic primitive already cancels cast; this is the right rule (genre-canonical D3/D4/Last Epoch). Cleanse-on-dodge is a *holy* mechanic per `substrate-identity-declarations-2026-05-17.md` § 6 (`cleanse` is holy's `mechanical_signature` verb) — it should be a trait reward, not a universal dodge feature. |
| **Direction** | Input-direction priority: LMB move-target direction → WASD direction → fallback (face primary actor) | Always away-from-nearest-enemy | Drax v0.26 cosmetic primitive already implements this; correct. Player intent must dictate direction. Auto-direction punishes intentional positioning. |

### § 2.2 — Substrate-coupled animation (NOT substrate-coupled mechanic)

The *animation* and *VFX* layer substrate identity onto a mechanically-universal dodge:

| Substrate | Dodge animation | Particle/VFX register | Cosmological coherence |
|---|---|---|---|
| **Fire** | Forward-flare dash; brief afterimage trailing flame | Red/orange trail particles; sparks at start/end | `escalation` — the dodge IS the spark cascading; brief consequence-accumulating motion |
| **Water** | Dissolve-and-reform; brief loss-of-form mid-dodge | Blue droplet/mist trail; subtle ripple at endpoint | `suffusion` — the substrate that fills a space briefly *unfills* this one to refill another |
| **Earth** | Brace-and-shoulder-roll; short ground-trail; *slightly slower than other substrates* | Brown dust kick-up; faint ground-crack at endpoint | `positional refusal` — earth dodges *grudgingly*, with the body of the world resisting. Earth dodge is shorter distance (~3m vs default ~4m) but slightly longer i-frame (~0.45s vs default ~0.4s) — the substrate that holds its ground takes evasion seriously when it does evade. |
| **Wind** | Long horizontal blink-step; brief in-between non-rendering | Cyan streaks; trail of motion-blur lines | `kinetic rearrangement` — wind dodge is *the substrate's signature.* Wind dodge is *slightly longer distance* (~5m vs default ~4m); the substrate that moves things moves itself best. |
| **Lightning** | Instant arc-translate; player vanishes at start position, materializes at end | Yellow/white branching streaks between start and end | `sudden traversal` — lightning dodge is the substrate's iconic verb made movement. Same distance as default; i-frame is the *entire* dodge duration (no in-between body). |
| **Holy** | Radiant-step-forward; brief outward-radiance pulse at endpoint | White/gold glow; faint cone-shaft trail | `revelation` — the substrate that exposes itself does not hide-to-evade; it *shines through* the moment of evasion. The dodge is visible from a distance. |
| **Shadow** | Step-into-and-out-of shadow; brief invisibility | Purple/dark trail; muted edge-bloom at endpoint | `occlusion` — shadow dodge is the substrate's `conceal` verb realized as movement. **The only substrate where the dodge animation includes the player going briefly invisible.** Cosmologically perfect; tactically interesting (player loses self-perception of position for 0.4s; enforces input commitment). |

**Engineering note:** The mechanical-universal + animation-substrate-coupled split means **the engine ships a single dodge mechanic with substrate-tagged animation/VFX hooks.** No per-substrate dodge logic in `damage_resolver.py`; only per-substrate dodge VFX registration in the demo's VFX-pipeline (drax seam). This keeps the engine clean and shifts the substrate-coupling to the presentation layer where it belongs.

**Earth and wind get small numerical tweaks** to make the substrate coherence load-bearing (earth shorter+more-iframe, wind longer; the rest identical mechanically). This is the minimum amount of mechanical substrate-coupling that *honors* the cosmological commitments without making dodge a balance-sensitive system. If earth-dodge-different proves problematic, those tweaks can come out and the substrate-coupling lives purely in animation.

### § 2.3 — Alternatives rejected

- **Per-class mobility (no universal dodge).** Rejected: son's feedback was framed as a universal verb ("dodge roll out of the way" — not "a mobility skill on some classes"). Universal dodge as a *floor* + per-class mobility *abilities* on top (as B13 already designs) is the right pairing. The 5 defensive mobility geometries (roll/defensive_dash/strafe_mode/blink/dodge_stance per file 32 § 12.5) become *kit-pool additions* that some classes get — augmenting, not replacing, the universal floor.

- **D4-style charges-based dodge.** Rejected per § 2.1: dilutes decision moment.

- **Stamina-gated dodge.** Rejected per § 2.1: hidden stat gating active mechanic = player confusion.

- **Substrate-coupled dodge mechanic (different cooldowns/distances/i-frames per substrate).** Rejected as primary direction (kept as small tweaks for earth/wind only): making dodge cooldown 4s for wind and 6s for earth would force players-of-different-substrates into different muscle-memory loops, which fragments the universal-input grammar son's feedback assumed. Keep mechanical surface uniform; vary the *expression.*

### § 2.4 — Drax v0.26 cosmetic-primitive supersession

The v0.26 cosmetic dodge is *correctly minimal* — it ships the input grammar (`Shift` key) + direction-priority + animation cancel + trail VFX without engine integration. **It supersedes naturally when canonical dodge lands** because the input grammar and trail VFX are identical; only the i-frame engine wiring + substrate-VFX-coupling need to be added. **Do not amend v0.26.** It is the right placeholder.

---

## § 3 — Surface 2: Telegraphed AOE windup system

### § 3.1 — Recommendation: enemy AOEs telegraph; player AOEs do not

**Asymmetric telegraph rule per single-player ARPG convention** (D2/D3/D4/PoE/Last Epoch all converge on this):

- **Enemy AOEs telegraph** (player needs to read the battlefield to make positioning decisions)
- **Player AOEs do NOT telegraph** (player knows their own kit; telegraph would clutter screen and slow feel)

This is reinforced by the existing post-B11 lock per `canonical/16-project-roadmap.md` line 90 and `canonical/32-progression-design.md` § 12.5 item #4: enemy AOE indicator ~1.08× hitbox (dodges feel narrow); player AOE indicator ~0.92× hitbox (generous edges when displayed for visual feedback, but no windup).

### § 3.2 — Per-substrate windup character

Each substrate's `cosmological_commitment` informs how its enemy-cast AOE telegraphs. The mechanical parameters (windup duration; indicator color; indicator shape evolution) carry substrate identity into the read-the-battlefield surface:

| Substrate | Windup duration | Indicator color | Indicator evolution | Cosmological coherence |
|---|---|---|---|---|
| **Fire** | 0.8-1.2s | Red, escalating opacity | Indicator *brightens* over windup (escalation) | `escalation` — the spark cascading into total. The longer you stand in the indicator before it fires, the more the indicator visually warns you. |
| **Water** | 1.0-1.5s | Blue, fills outward from center | Indicator *grows* from center (suffusion) | `pervading presence` — the substrate that fills a space; the indicator literally fills the space before damaging it. |
| **Earth** | 0.4-0.7s (shorter) but indicator *persists* after damage for ~1.5s extra | Brown/tan, sharp-edged from start | Indicator appears *fully-formed* (no growth); persists after AOE resolves | `positional refusal` — earth claims a piece of ground and refuses to leave it. The post-damage persistence visually IS earth holding the ground. |
| **Wind** | 0.5-0.8s (short — wind is fast) | Cyan, *directional indicator* (arrow shape, not circle) | Indicator points *where you will be pushed* — escape direction is the indicator | `kinetic rearrangement` — the player reads not just *where damage hits* but *where wind will move me*. This is the only substrate whose telegraph encodes outcome-direction. |
| **Lightning** | 0.0-0.2s on first arc (near-instant); 0.4-0.6s telegraph on *next* arc | Yellow/white, branching | First arc damages with brief flash; chain to next target gets normal telegraph window | `sudden traversal` — the substrate's identity is interruption. *The first arc lands without telegraph (interrupting),* but the chain visibly threatens the next target. Honors substrate while staying *fair* (the next strike is dodgeable). |
| **Holy** | 1.5-2.0s (longest) | White/gold, slow radiant build | Indicator *radiates outward* during build; nova-shape | `revelation` — the substrate of slow exposure; the longest windup of any substrate, and the most visible. Holy AOEs are dodgeable but not stealthy. |
| **Shadow** | 0.3-0.5s, but indicator only *appears* in last 0.2s | Purple/dark, late-commit | Indicator hidden during 0.1-0.3s pre-telegraph; visibly commits at 0.2s before damage | `concealment` — the substrate of "arrives without warning." **Still telegraphed (fair play)** but with the shortest pre-warning window of any substrate. Shadow asks the player to *commit-perceive late.* Tactically demanding; cosmologically authentic. |

### § 3.3 — Indicator language standardization

**Two indicator dimensions universal across substrates:**

1. **Shape:** indicator shape matches AOE geometry (circle for `ground_targeted_circle`; cone for `cone`; line for `bolt_line`; ring for `radiant_aura`; etc. — geometry types per substrate `geometry_affinities`).
2. **Opacity ramp:** indicator opacity ramps 0 → 1 over windup duration (except shadow per § 3.2). Player reads "how close to firing" by opacity.

**Per-substrate dimension:**

3. **Color** and **growth-evolution pattern** per § 3.2 table.

**Player-AOE indicators (no windup, but show post-cast):**

Player AOEs show their hit zone *after* cast for ~0.3s (so the player learns what hit) but at *0.92× hitbox* (generous edges — see existing post-B11 lock). No windup; no escape window from your own AOE.

### § 3.4 — Trait/skill interaction surface

Per existing D8 lightning trait `lightning_t12_static_threading` (cooldown reduction on multi-target discharge) and similar patterns, the windup-system creates **new trait surface** for future canonical-four trait pools (D8 follow-up Phase-1 P2 work):

- **Fire trait candidates:** "shorten own windup on consecutive casts" (escalation rewards rhythm)
- **Wind trait candidates:** "windup grants brief player movement-speed bonus" (the substrate that moves rewards being-in-motion)
- **Lightning trait candidates:** "first-arc telegraphs visibly" (player-side counter-build — trade off speed-of-cast for ally readability; not relevant in solo but consonant with substrate)
- **Holy trait candidates:** "shorter own windup in own consecrate zones" (zone-conditional)
- **Shadow trait candidates:** "indicator stays hidden for full duration on isolated targets" (rewards positioning to isolate)

**These traits are not in current D8 design.** They become design surface for Phase-1 P2 trait-pool extensions or B13-proper post-VS2a. **Surface as forward-work, not Phase-1 P1 scope.**

### § 3.5 — What this requires engine-side

- Engine emits `cast_time_seconds` (already exists per `fight_engine.py:436`) ✓
- Engine emits `windup_duration_seconds` per AOE skill (NEW field; defaults per substrate per § 3.2)
- Engine emits `indicator_color_hex` per substrate (could derive from substrate.iconic_register or be substrate-keyed lookup)
- Engine emits `indicator_geometry` from skill geometry already (✓ existing)

**Schema additions:** 2 new fields (windup_duration_seconds, indicator_color_hex). Trivial extension to skill schema. Rocket micro-task (~1 day).

### § 3.6 — Player AOE-windup question (open)

File 32 § 12.5 item #3: *"Should player abilities have telegraphs (other players see them coming) or only enemy abilities?"*

**Recommendation:** **Player AOEs do NOT telegraph** in solo play. If multiplayer ever ships (per `project_design_intent.md`: "solo gameplay only"), this is a multiplayer-only re-evaluation. The Reincarnated solo-play context makes player-AOE telegraphs *worse* (information overload on the player who already knows what they cast).

**This is now a soft-lock recommendation for Phase-1 P1.** If Matt accepts it, file 32 § 12.5 item #3 can be marked CLOSED.

---

## § 4 — Surface 3: Monster AI escape behavior

### § 4.1 — Recommendation: tiered AI per monster role

Monster movement-during-player-cast behavior stratifies by encounter tier (per `canonical/34-monster-design-phase0-vs-production.md` and Diablo/PoE genre convention):

| Monster tier | Player-AOE escape behavior | Telegraph-own-AOE? | Cost (engine + AI) |
|---|---|---|---|
| **Trash mob** (1-shot fodder; high density) | **None** — moves toward player, attacks, dies | No telegraph; instant melee/projectile resolution | Existing AI ✓ |
| **Elite mob** (1-3 per pack; reinforced) | **Reactive only** — when player-AOE indicator visible AND elite is inside indicator, AI biases toward perpendicular-escape with 50-70% probability | Telegraphs own AOEs (per § 3) | NEW AI behavior (~3-5 days engine) |
| **Mini-boss** (1 per gauntlet room; named) | **Reactive + strategic** — reactive escape (as elite) + pre-cast repositioning (moves to maintain optimal-range with the player every 2-3 seconds) | Telegraphs own AOEs with longer windup (substrate-default + 0.3s) | NEW AI behavior + repositioning loop (~3-5 days engine) |
| **Boss** (1 per act-end; spectacle) | **Strategic + anticipatory + substrate-coherent** — anticipates player-AOE based on player's last 3 casts; repositions proactively; escape direction follows substrate iconic motion (wind boss escapes laterally; earth boss roots-in-place and absorbs; lightning boss arc-blinks; etc.) | Telegraphs own AOEs with substrate-coherent windup | NEW AI behavior + substrate-AI hooks (~5-7 days engine, B13 territory) |

### § 4.2 — Why tiered (the density vs telegraph trade)

Per file 32 § 12.5 reference notes: *"The denser the mob count, the less individual telegraphing (would clutter screen). Trade-off: telegraphs scale inversely with density."*

The same applies to escape behavior. If 12 trash mobs all evade your AOE, the AOE is functionally useless and the screen becomes unreadable. If 1 mini-boss evades while 12 trash mobs commit, the player has *clean hits* on the easy targets and *a positioning puzzle* with the priority target. **Density discipline is what makes substrate identity legible in play.**

This is also the answer to son's feedback. *"Monsters can't escape your moves"* is correct at the trash tier (and should stay correct); it is *wrong* at the elite/mini-boss/boss tier where the absence creates the deterministic feel. Fix the tier where escape behavior is missing; do not over-fix the tier where its absence is correct.

### § 4.3 — Substrate-coherent escape direction (B13 territory; defer)

The substrate-coherent boss escape (wind boss escapes laterally; earth boss roots; lightning boss arc-blinks) is rich design surface but **not Phase-1 P1.** It is exactly B13 substrate-coupled-AI work. Defer to B13-proper post-VS2a.

**Phase-1 P1 scope of monster-escape:** elite-tier reactive escape only. That is the minimum-viable monster-escape behavior that makes son's feedback land AND makes substrate-keyed AOE meaningful in the D27 perception test.

### § 4.4 — Player-monster symmetry question

The dispatch asked: *"should the player's experience of 'monsters can escape my AOE' mirror 'I can escape monster AOE'? Or should asymmetry exist?"*

**Recommendation: asymmetry, intentionally.** Player gets universal dodge + reads-enemy-telegraphs. Elites/mini-bosses/bosses get reactive/strategic/anticipatory escape (no need for them to dodge-roll because their movement IS their escape verb). Trash mobs have neither — they commit and die.

This asymmetry is genre-standard (D3/D4/PoE) and **necessary for game feel**: if monsters could dodge-roll, the player's burst-damage skills become unreliable in ways the player cannot read. Asymmetry = legibility = player agency.

### § 4.5 — Engagement-loop rhythm change

If Phase-1 P1 ships with the narrow slice (§ 7):

- **Trash mobs:** rhythm unchanged. AOE → kill → next pack. Son's feedback for *"monsters cant escape your AOE"* preserved at trash tier (correctly — trash should not escape).
- **Elite mobs:** rhythm shifts to "lead the AOE" — drop the AOE *where the elite is moving to*, not where they are. Same player input, different positioning judgement.
- **Mini-bosses/bosses:** unchanged in Phase-1 P1 (defer to B13-proper).

The engagement-loop change at the elite tier is **exactly enough** to validate D27 perception test against substrate identity. Substrates with different `geometry_affinities` (wind PREFER cone+vortex_pull; fire PREFER burst+ground_targeted_circle; lightning PREFER chain+branching) will produce *different elite-pursuit and -evasion patterns,* which the player can perceive even if they cannot articulate.

---

## § 5 — Scope estimate breakdown

### § 5.1 — Narrow-slice Phase-1 P1 extension (recommended per § 7)

| Item | Owner | Effort |
|---|---|---|
| **Promote drax v0.26 cosmetic dodge to engine-coupled** (i-frame wiring; cooldown shared state; remove damage during i-frames) | drax + rocket (i-frame field consumer + schema field) | 2-3 days |
| **Engine `windup_duration_seconds` + `indicator_color_hex` schema fields** + per-substrate defaults loader (substrate.yaml extension) | rocket | 1 day |
| **Demo enemy-AOE ground-indicator rendering** (per § 3.3 indicator language; uses existing geometry geometry-painter) | drax | 2-3 days |
| **Elite-tier reactive escape AI** (perpendicular-escape on visible player-AOE indicator; 50-70% probability) | gamora (sim AI) | 3-5 days |
| **Substrate-VFX-coupling for dodge animation** (per § 2.2 substrate table; 7 substrate animation hooks) | drax | 1-2 days |
| **Gandalf design review pass + cross-doc updates** (canonical 32 § 12.5 amendment; substrate-identity-declarations § 9 amendment; this briefing → decisions-log) | gandalf | ~1 day (mostly absorbed by this briefing) |

**Subtotal: ~10-15 days.** Median ~11-12 days. Within dispatch estimate of 11-17 days.

### § 5.2 — Full B13 (deferred to post-VS2a per existing roadmap)

Per `canonical/16a-roadmap-shipped-log.md` line 86: ~3-4 weeks engine + demo + regen. Includes:

- 5 defensive mobility geometries (roll/defensive_dash/strafe_mode/blink/dodge_stance) added to geometry palette
- Mini-boss + boss strategic + anticipatory escape AI
- Substrate-coherent boss escape directions
- Full asymmetric indicator scaling (already partially designed)
- Substrate-AI hooks for boss-tier substrate-coherent escape verbs
- Archetype-emergence observability (kit-mobility per-class per-season telemetry)
- Player-side mobility ability generator-pool extension

**Scope after narrow slice lands: ~2.5-3 weeks remaining** (5-7 day reduction from original B13 because narrow-slice covers ~25% of B13 scope).

### § 5.3 — If Phase-2 deferral chosen instead

If Matt chooses Phase-2 deferral, all of § 5.1 work moves to B13-proper post-VS2a. **Phase-1 P1 ships on schedule** but D27 perception test runs against current spatial-combat substrate (positioning-doesn't-decide-outcomes). Expected D27 outcome:

- Pair-recovery accuracy likely ≤2/4 → H1 rejected → Layer-3 metric must ground in play-trace features → extra 1-2 weeks Phase-1 P1 scope for feature-extraction spec
- Alternative interpretation: result reads as "substrates don't feel distinct" → re-litigation of substrate-identity declarations or expansion decision

**Phase-2 deferral cost: ~1-2 weeks of false-negative cleanup OR re-litigation.** Saved cost from skipping narrow slice: ~11 days. **Net wash to slightly negative** if D27 returns ambiguous.

---

## § 6 — Cross-impact map

### § 6.1 — D27 perception test (`perception-test-experiment-scoping-2026-05-17.md`)

**Impact: LOAD-BEARING.** Per § 1.3 above: without narrow-slice, D27 likely false-negative reports.

**Resolution:** narrow slice lands first; D27 runs against telegraphed-combat-enabled engine. Expected better signal quality. **D27 effort unchanged; just lands later in Phase-1 P1.**

### § 6.2 — D14 mirror-match diversity gate

**Impact: METRIC-CHOICE-INFORMING.** D14 implementation per `scope-of-work-phase-1-p1.md` line 144 was blocked on D27. Narrow slice landing makes D27 productive. If D27 then passes (mechanical-parameter metric perceptually valid), D14 stays at original scope. If D27 still fails after narrow slice (mechanical-parameter metric perceptually invalid), D14 needs play-trace feature spec (was always the contingent risk; narrow slice reveals it correctly).

### § 6.3 — D8/D9 trait floor designs (`d8-trait-floor-design-phase-1-p1.md` + canonical-four pools)

**Impact: TRAIT-INTERACTION-SURFACE.** Per § 3.4 above: telegraphed-combat creates new trait surface (windup-modulating traits; indicator-modulating traits; escape-modulating traits). **Existing D8 traits do NOT assume telegraphed combat** — they all reference `mechanical_signature` and `iconic_verbs` from the substrate identity declarations, not the engagement-loop substrate.

**D8 traits read clean against the narrow-slice extension.** No amendment needed.

**D8 trait *additions* (Phase-1 P2 candidate per § 3.4):** future traits that interact with windup/escape become design surface AFTER B13-proper ships. Not Phase-1 P1.

### § 6.4 — D10 substrate-coherent generation rules

**Impact: GEOMETRY-AFFINITY-VALIDATED.** D10 per `scope-of-work-phase-1-p1.md` line 124 generates archetypes based on substrate `geometry_affinities`. With narrow-slice extension, the `geometry_affinities` declarations finally *matter at play time* — fire's `burst PREFER` produces visibly-different combat behavior from wind's `cone PREFER` because positioning decides outcomes.

**D10 design unchanged; D10 *validates* better against narrow-slice-enabled engine.** Gamora may want to add D10 acceptance criterion: "substrate-coherent generation produces archetypes whose play-feel reads substrate-distinct in 90sec-fight perception" — which is exactly what D27 measures.

### § 6.5 — D26 cross-doc updates

**Impact: SMALL.** Narrow slice triggers:

- `canonical/32-progression-design.md` § 12.5 amendment — items #2 (i-frame durations), #3 (player-cast telegraphs), #4 (indicator hitbox), #6 (cadence) update to reflect narrow-slice locks. Item #1 (5-geometry roster) and #5 (mobility role-tagging) stay open for B13-proper.
- `canonical/16-project-roadmap.md` — B13 scope-reduction note (narrow slice partial-completion ~25%; ~2.5-3 weeks remaining at Stage A2 closeout instead of 3-4 weeks).
- `canonical/story/substrate-identity-declarations-2026-05-17.md` § 9 — new amendment-note acknowledging narrow-slice spatial-combat substrate underwrites the declarations.
- New decisions-log entry (knight-rider drafts; jack-ryan reviews) capturing the L3 decision.

**Estimated: ~0.5 day gandalf.** Absorbed into § 5.1 budget.

### § 6.6 — Drax v0.26 cosmetic dodge

**Impact: SUPERSEDED.** v0.26 cosmetic primitive becomes engine-coupled. The v0.26 visual treatment (trail particles; ease-out interpolation; direction-priority) is the *baseline* the substrate-VFX-coupling extends. No work thrown away.

### § 6.7 — Engine MIGRATION.md surface

Schema additions (`windup_duration_seconds`, `indicator_color_hex`, possibly per-substrate-dodge-tweak fields) trigger `simulation/MIGRATION.md` entries. Rocket + gamora co-author per cross-seam discipline.

---

## § 7 — Recommendation

### § 7.1 — Recommend: PARTIAL Phase-1 P1 extension (narrow slice per § 5.1)

**Fold into Phase-1 P1:**

1. Engine-coupled dodge mechanic (universal; substrate-VFX-coupled animation)
2. Enemy-AOE telegraph indicator system (per-substrate windup character per § 3.2)
3. Elite-tier reactive escape AI behavior
4. Cross-doc updates

**Defer to B13-proper post-VS2a:**

1. 5 defensive mobility geometries as kit-pool additions (NOT universal dodge — those are *additional* mobility skills)
2. Mini-boss + boss strategic/anticipatory escape AI
3. Substrate-coherent boss escape directions
4. Archetype-emergence observability for kit-mobility composition
5. Full B13 trait-pool extension surface (windup-modulating traits per § 3.4)

### § 7.2 — Why partial, not full Phase-1 P1 extension

**The narrow slice exists because D27 needs it.** Anything more is mission-creep. The full B13 ships beautifully in its existing post-VS2a slot — there is no story reason to accelerate the substrate-coherent boss-AI work or the 5-geometry-mobility-pool work into Phase-1 P1. **Those are richness; the narrow slice is necessity.**

The cosmological-vs-pragmatic tension named explicitly:

- **Cosmological argument (more):** the substrate identity declarations want every player encounter to feel substrate-distinct from session one; full B13 in Phase-1 P1 maximizes this; ship the perfect-game-thesis as a unit.
- **Pragmatic argument (less):** Phase-1 P1 already has 27 deliverables and a 6-8 week critical path; adding 3-4 weeks of B13 doubles the risk surface; the narrow slice is the *minimum* that prevents D27 false-negatives.

**I weight pragmatic at 70/30 here.** The reason: the substrate identity declarations are *load-bearing for D27*; the boss-AI substrate-coherence is *load-bearing for the eventually-shipped game.* These have different urgencies. Phase-1 P1 needs the perception test to land cleanly. The eventual game needs the boss-AI work. Sequencing matters.

The narrow slice IS the load-bearing fix. The full B13 is the eventually-shippable polish. Do not conflate.

### § 7.3 — Why NOT Phase-2 deferral

Phase-2 deferral risks D27 reporting false-negatives (per § 1.3 + § 5.3). The "saved" time (~11 days) is plausibly burned in either:

- Re-running D27 after B13-proper at Stage A2 closeout (wasting one D27 cycle)
- Re-litigating substrate-identity declarations if D27 ambiguity gets interpreted as "substrates don't feel different"
- Authoring Layer-3 play-trace feature spec on top of Layer-3 mechanical-parameter spec if D27 returns false-negative-but-architecture-team-doesn't-realize-it's-false-negative

**Net pragmatic argument: narrow slice is cheaper in expectation than Phase-2 deferral.** Deferral *looks* free but isn't.

### § 7.4 — What I would tell the team if I were Matt

> "Pull the narrow slice into Phase-1 P1. Ship it as Deliverable 28 (new). Spec it to land before D27 runs — D27 cannot produce signal without it. Defer the rest of B13 to its existing slot. Gandalf authors the design package for the narrow slice; gamora picks up the AI and i-frame wiring; drax picks up the dodge engine-coupling and indicator rendering; rocket adds schema fields. Total scope add: ~11 days. Total risk reduction on D27: large. The son saw the gap correctly; let's close exactly the gap he saw and not more."

---

## § 8 — Decision-by window for Matt

**Recommended decision-by: 48 hours from briefing surface.**

The longer the L3 decision delays, the more rework risk grows on:

- **Drax v0.26 cosmetic dodge:** stable as-is; no rework risk.
- **D27 perception test execution:** drax session-runner readiness work is already in flight (per scope-of-work). If narrow slice extension is chosen, drax dovetails session-runner work with dodge engine-coupling work — fastest path. If deferred, drax ships session-runner alone but D27 results may need re-running post-B13.
- **Gamora D10 implementation:** D10 substrate-coherent generation rules are landing now (per hive log gamora STATE entries 2026-05-18). D10 testing benefits from telegraphed-combat substrate. If narrow slice chosen, D10 acceptance criterion can include spatial-perception validation.
- **D14 mirror-match diversity gate:** D14 depends on D27 result. Narrow slice landing cleanly → D14 metric choice is informed. Phase-2 deferral → D14 has to commit to a metric before knowing which one is perceptually valid.

**Hard latest decision-by: ~5 days** (before drax session-runner ships and D27 runs). After D27 runs without narrow slice, the perception test will need to be re-run, which is more expensive than deciding now.

**No decision-required-now:** if Matt wants to think on this longer, the dispatch can be amended to a soft-park; gandalf stays in continuous-availability ramp for follow-up Q&A (per dispatch).

---

## § 9 — Open questions for Matt

These are decision-surfacing questions, NOT pre-emptive design choices. Matt's answer to these clarifies the L3 disposition:

1. **Universal dodge vs per-class mobility (§ 2.3)** — comfortable with universal-dodge-floor + per-class-mobility-additions? Or prefer Last-Epoch-pure per-class-only model?

2. **Dodge cooldown (§ 2.1)** — 4-5s shared cooldown OK? Or do you prefer the D4 charges-based model (2-3 charges, 4s recharge) for higher per-second evasion frequency?

3. **Earth/wind dodge numerical asymmetry (§ 2.2)** — comfortable with earth-dodge slightly shorter+more-iframe and wind-dodge slightly longer? Or prefer fully-uniform mechanics with substrate-coupling at animation layer only?

4. **Player-AOE telegraph (§ 3.6)** — agree player AOEs do NOT telegraph in solo? Or want player-AOE windup as a *self-discipline* mechanic (read your own kit's commitment-windows)?

5. **Shadow late-commit indicator (§ 3.2)** — comfortable with shadow AOEs having 0.2s pre-warning (shortest of any substrate, but still telegraphed)? Or should shadow AOEs telegraph at standard 0.5s like everything else (less substrate-coherent, more "fair")?

6. **Narrow-slice vs full B13 vs Phase-2 deferral** — § 7 recommendation is narrow slice. Confirm or counter.

7. **Decision-log + canonical-32 § 12.5 amendment authoring** — if narrow slice approved, gandalf authors the canonical updates next; OK with Pattern B (gandalf drafts; knight-rider sequences; jack-ryan reviews) for the cross-doc amendment package?

---

## § 10 — Cross-references

- `canonical/story/substrate-identity-declarations-2026-05-17.md` — the seven substrate identity declarations whose `geometry_affinities` and `cosmological_commitment` fields require this engagement-loop substrate to be expressible
- `canonical/story/substrate-identity-declaration-spec-2026-05-17.md` — the spec the declarations instantiate (Layer-0 spatial-combat assumed; explicitly not specified)
- `canonical/story/perception-test-experiment-scoping-2026-05-17.md` — the D27 test that depends on spatial-combat substrate to produce signal
- `canonical/story/d8-trait-floor-design-phase-1-p1.md` + `canonical/story/d8-canonical-four-trait-pools-2026-05-18.md` — trait pools that anchor against substrate identity but do not yet reference engagement-loop substrate
- `canonical/32-progression-design.md` § 12.5 — the B13 design surface (active mobility + telegraphs + i-frames + 5 defensive mobility geometries; ~80% pre-decided)
- `canonical/16-project-roadmap.md` Stage A2 closeout — current B13 slot (post-VS2a)
- `canonical/16a-roadmap-shipped-log.md` line 86 — original B13 scope and estimate
- `canonical/34-monster-design-phase0-vs-production.md` — monster tier hierarchy that informs § 4 escape-behavior stratification
- `reincarnated-engine/src/reincarnated/simulation/damage_resolver.py:88` — existing `i_frame_window` field reserved as metadata
- `reincarnated-engine/src/reincarnated/simulation/fight_engine.py:436` — existing `cast_time_seconds` consumed from skill timing params
- `reincarnated-engine/src/reincarnated/simulation/combatant.py:40` — existing `STAMINA_DODGE_COST` for statistical evasion (preserved; not extended to active dodge)
- `reincarnated-demo/src/main.ts:591-758` — drax v0.26 cosmetic dodge primitive (the placeholder the engine-coupled version supersedes)
- `agentic_orchestration/dispatches/2026-05-17-gandalf-l3-briefing-dodge-plus-telegraphed-combat.md` — the knight-rider dispatch this briefing answers
- `agentic_orchestration/hive-mind/scope-of-work-phase-1-p1.md` — current 27-deliverable Phase-1 P1 scope; narrow slice proposes Deliverable 28

---

*Authored 2026-05-17 by gandalf. L3 briefing for Matt's Phase-1 P1 extension vs Phase-2 deferral decision on dodge + telegraphed-combat substrate. Recommendation: narrow-slice extension (§ 5.1; ~11 days) folded into Phase-1 P1 as new Deliverable 28; defer full B13 to existing post-VS2a slot. The son saw the missing substrate correctly; close exactly the gap he named, nothing more.*
