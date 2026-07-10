# E4 Cast-Time Axis — Fork Elicitation (DRAFT — forks await Matt ruling)

**Author:** gandalf. **Status:** DRAFT ONLY — no ledger flip, no self-ratify, no binding acceptance criteria.
This surfaces the design forks Matt must rule so that when E2 lands, the E4 design note can be
authored fast against Matt's rulings (the E2 rhythm: gandalf rules semantics → rocket derives values
math-note-first). **The forks below are the equivalent of E2's Q-E2-1/2/3.**
**Structural template:** `agentic_orchestration/gandalf/notes/2026-07-09-e2-economy-axis-design-note.md`.
**Ledger row:** E4 (`canonical/current-to-end-state/surface-ledger.md`) — OPEN queued.
**Sequence position:** third axis of the full-spec main line — E1 (landed `bfc94eb`) → E2 (in flight) → **E4** → E3.

---

## 0. Scope and boundaries (fixed — do NOT re-litigate)

**E4 IS:** cast-time / wind-up / charge texture. The emitter already stamps
`timing.params.cast_time_seconds` from a tier table `_CAST_TIME = {1:0.3, 2:0.5, 3:0.7, 4:1.0}`
(`per_skill_emitter.py:194, :689, :744-745`). E4 gives that field **mechanical meaning per emitted kit**.

**E4 IS NOT:** economy (per_hit/cooldown/energy_cost = E2, in flight); geometry (E1, landed);
hybrid dual-scaling (E3, queued after E4); resource-model / regen (the **tempo** seam — see the
`bc_tempo`→resource finding in §Fork-4, that coordinate is spoken for).

**The spine is sacred (same discipline as E2).** `TIER_COEFFICIENTS`, `_DAMAGE_MULTIPLIER`,
`BASE_SPELL_DAMAGE_L50`, base `_ENERGY_COST` / `_COOLDOWN` untouched. Any E4 magnitude applies as a
layer at emission, never a table edit. (Whether `_CAST_TIME` itself counts as "spine" or as "the
layer's own table" is a sub-question folded into Fork-4/Fork-5.)

---

## 0b. THE SIM-CONSUMPTION REALITY CHECK — read this before any fork (the E2 amendment-A lesson, materialized)

The brief asked me to flag whether the sim's `cast_time` consumption does what E4 needs. **It does not.
This is the single most consequential finding in this note and it reframes several forks.**

Source-verified (`spatial_gauntlet/spatial_engine.py`):
- The player-cast action cadence is set **from `cooldown_seconds` ALONE** (× E3 `cadence_scale`):
  `cooldown = float(skill.get("cooldown_seconds", 2.0)) * self.player.cadence_scale` (:2414) →
  `self.player.action_available_at = elapsed + cooldown` (:2416). The readiness gate reads that
  field only (`if elapsed < entity.action_available_at` :1281).
- **`cast_time_seconds` is NEVER read by the sim.** `grep` across `simulation/` returns zero live
  consumers — the field is emitted and ignored. There is **no wind-up delay** between skill selection
  and damage application (`_apply_skill_damage` fires at :2402, cadence is set *after*, and cast_time
  gates nothing before it).
- The `max(cd, 0.5)` at `_dps_score` (:1396) is a **skill-SELECTION scoring floor** (0.5s minimum
  cadence for the AI's DPS ranking), NOT a cast_time wind-up. The comment at :2413 ("_CAST_TIME
  floors the true minimum cadence regardless of k") refers to an E3 math-note *constant floor
  concept*, not to live per-skill cast_time consumption.

**Consequence for E4:** unlike E2 (where the sim already consumed per_hit/cooldown/cost, so E2 was a
pure emitter change), **E4 is NOT a free emitter-only change.** For cast_time to have ANY mechanical
meaning, gamora must add a sim-side consumer — a cross-seam change (ADR-004: MIGRATION.md + gamora +
Matt). This is the exact "flag, don't fake" situation E2 amendment-A warned about: `_CAST_TIME`
already emits tier-varying values (0.3→1.0s) that are **presently 100% inert.** E4's real cost is the
sim consumer, not the emitter layer.

**I do NOT resolve the sim-consumer shape here (Disc #18 — rocket/gamora derive it math-note-first).**
But it is load-bearing on Fork-2 and Fork-4, and I flag it as the reason E4 is heavier than "cheapest
of the four" (the ledger's pre-audit lean) suggested.

---

## Q-E4-1 — Modulation scope: which roles/tiers get cast_time modulation?

**The question.** Mirror E2's Q-E2-3 modulation table. Which chains carry an E4 cast-time signature,
which are exempt, and why?

**Candidate answers.**
- **(a) Attack-full + control-cadence-only (E2-parallel).** primary/secondary attack fully modulated;
  control gets cast-time on its cast but the lock magnitude stays untouched ("the lock, not the nuke");
  support exempt; T4 exempt (passive-mode capstones, cooldown 0.0 — a wind-up on a passive is
  meaningless, same as E2). *Genre anchor:* D2 sorc — a Nova (control-ish) has cast-frames like any
  spell; a Warcry (support/aura) does not "wind up."
- **(b) Attack-only.** Only primary/secondary attack chains get cast-time; control/support/T4 all
  exempt. Simpler; keeps cast-time as a pure damage-delivery texture.
- **(c) Full including T4.** T4 capstones ALREADY emit `name="channeled", cast_time_seconds=1.0`
  (:744, :848) — the ONE place cast_time is thematically live in intent today (the summon "deliberate
  act of conjuring", :827). One could argue T4 is where cast-time *belongs* most (the big committed
  cast). *Tension:* T4 cooldown is 0.0 (passive-mode); a channeled-but-instant-refire capstone is a
  contradiction the sim doesn't model, and modulating it re-opens the E2-exempt logic.

**Tension against spine / E2.** T4's exemption in E2 was clean (modulating a 0.0-cooldown passive is
meaningless). Cast-time is subtly different: T4 is *already the only tier carrying a non-instant
timing name*. Ruling (a) or (b) exempts it and leaves that `channeled` label as flavor-only; ruling
(c) tries to make it real and collides with the passive-mode model.

**My LEAN (for Matt to rule):** **(a)**, exactly parallel to E2's Q-E2-3, EXCEPT hold a small
asterisk on T4 — see Fork-3. The player-legibility win of "same scope rules across all four axes" is
worth a lot; divergent scope tables per axis is how ARPG skill systems become unlearnable (the
late-PoE gem-tag sprawl failure). Control cast-time-on-the-cast, lock-magnitude-untouched, is the
direct D2/D3 analog and keeps control's identity ("interrupt-vulnerable but the lock is the lock").

---

## Q-E4-2 — THE LOAD-BEARING FORK: throughput-NEUTRAL or throughput-ACTIVE?

**The question.** E2's elegant core was the single scalar `k` making throughput + cost_rate invariant
*by construction* — a texture layer that moves nothing on the balance sheet. **Does E4 have an
analogous conservation law, or is cast-time a real DPS lever?** This fork decides whether E4 is a
texture layer (E2-style) or a balance lever — and it decides whether the post-E4 band re-fit is a
conservation-law *audit* (bands must NOT lurch) or an *expected re-fit* (bands WILL move; the re-fit
re-certifies them).

**Candidate answers.**
- **(a) Throughput-NEUTRAL (E2-parallel conservation).** A longer cast-time is compensated so effective
  throughput holds at the tier-spine value. Mechanically: the cast-time *replaces part of the cooldown*
  (period = cast_time + recovery; total period held invariant), OR per-hit scales up to pay for the
  wind-up (bigger hit, same DPS). Both preserve `throughput = per_hit / period`. *Genre anchor:* this
  is D2's FCR-breakpoint world abstracted — cast frames are real, but the game is *balanced around*
  them; a slower cast at higher per-hit is the "same build, different feel." *Consequence:* bands must
  NOT lurch (the conservation-law audit, exactly as E2); E4 becomes pure feel.
- **(b) Throughput-ACTIVE (risk/reward lever).** Cast-time is a REAL trade: commit to a wind-up, get a
  bigger hit that is NOT fully compensated — a genuine DPS-up-if-you-land-it, DPS-down-if-interrupted
  gamble. *Genre anchor:* PoE slam wind-ups (Earthquake / Tectonic Slam), Last Epoch's Hammer Throw
  charge, D4 Barbarian's wind-up shouts-into-slam. The wind-up IS the balance knob — big payoff for
  positional/timing commitment. *Consequence:* bands WILL move; the post-E4 re-fit re-certifies rather
  than audits; the sim must model interrupt/whiff risk (see below) or the "risk" half is fictional.
- **(c) Neutral-with-a-twist: cast-time is neutral on paper but the SIM's fight-truncation and
  positional model surfaces a real second-order delta** (a long wind-up that doesn't complete before a
  fight ends, or before the actor must reposition, is real lost throughput). This is the E2 §1.2
  "second-order play" idea taken as the *whole* mechanism: neutral by construction, textured by the
  sim's reality. *Consequence:* bands *may* wobble slightly (like E2's expected small deltas), and the
  wobble is diagnostic, not a re-fit.

**Tension against spine / E2 / the sim.** (b) is the most *ARPG-authentic* — cast-time as risk/reward
is the whole point of slam builds — but it directly requires the sim to model something it does NOT
today: **there is no interrupt, no whiff, no wind-up-that-can-be-canceled** (§0b: cast_time is unread;
damage applies instantly at :2402). Without a sim-side wind-up window during which the cast can fail,
"risk/reward" is a number with no risk — a strictly-worse or strictly-better skill, i.e. a balance
regression dressed as texture. So **(b) is only real if gamora builds an interrupt/whiff model**
(large cross-seam cost). (a) and (c) are buildable against a lighter sim consumer (cast_time consumed
as pure added period, no cancel-window).

**My LEAN (for Matt to rule):** **(a) for v1, with (b) named as the launch-scope re-entry** — the
same shape as E5 (declared-baseline-now, full-envelope-when-the-operator-surface-lands) and E9 (affix
layer now, RIVAL kit-built later). Rationale: (a) gives the *feel* of cast-time (commitment windows,
slower-heavier vs faster-lighter hands on the same spine) at the cost of a modest sim consumer
(cast_time = added period, throughput held), and it keeps the certification story clean (E2-style
conservation audit — bands must not lurch, a lurch = leaked law). (b)'s risk/reward is the truer
fantasy but it is gated on a sim interrupt/whiff model that does not exist and would be a substantial
gamora build — that is a *design pass of its own*, exactly the kind of thing that should re-enter
named, not be smuggled into a texture axis. **This is the fork I most want Matt to rule first** —
everything downstream (sim-consumer shape, band-refit expectation, magnitude constraints) forks on it.

---

## Q-E4-3 — T4 channeled reconciliation (the asterisk from Q-E4-1)

**The question.** T4 already emits `name="channeled", cast_time_seconds=1.0` while carrying
`cooldown=0.0` (passive-mode capstone). Under E4, is that channeled-cast made mechanically real, left
as inert flavor, or reconciled?

**Candidate answers.**
- **(a) Leave T4 exempt + inert (E2-parallel).** The `channeled` label stays flavor; cast_time_seconds
  on T4 stays unread (as it is today for ALL tiers). Clean, consistent with E2's total T4 exemption.
- **(b) Make T4's channel real — a genuine cast-lock on the capstone.** A capstone that must be
  *committed to* (a 1.0s conjure/channel during which the actor is occupied) is thematically strong —
  it is the ONE place cast-time already means something in intent (the summon "deliberate act of
  conjuring", :827). But T4 cooldown 0.0 means it can re-fire every action; a channel-locked 0.0-cd
  skill is a new sim behavior.
- **(c) Defer T4 cast-time to E6/proxy-suite work.** The proxy T4 suite is its own in-flight design
  (`proxy-t4-suite-spec` v3, ledger E6). Cast-time on capstones may belong THERE, not in E4's
  attack-chain axis.

**My LEAN:** **(a) for E4 proper, flag (c) as the right home for any real T4 channel.** E4 is the
attack-chain texture axis; T4's channeled identity is entangled with the proxy/summon activation model
(E6, two-phase activation) and should be reconciled there, not bolted onto E4. Keep E4's scope table
identical to E2's (T4 exempt) and note the T4-channel question as "E6's to own."

---

## Q-E4-4 — Source coordinate: does cast-time map from an existing catalog coordinate, or need a new one?

**The question.** E1 mapped geometry from the rich `_RICH_TO_SPATIAL` vocabulary; E2 mapped economy
from `bc_amplitude`. Does E4 map cast-time from an existing BC coordinate — and if so, is that
coordinate currently v1-inert (as amplitude was pre-E2)?

**Source-verified finding.** The catalog's five BC coordinates are
`bc_range / bc_tempo / bc_amplitude / bc_attribute / bc_proxy_density` (`endgame_encounter_catalog.py:130-134`).
Of these:
- `bc_amplitude` → **spoken for by E2** (spiky/flat/variable → economy).
- `bc_tempo` (low/medium/high) → **spoken for by the resource/regen seam.** It maps to resource model
  via `_BC_TEMPO_TO_RESOURCE` / `_infer_resource_model(bc_tempo)`
  (`season_generation_pipeline.py:250, :681-683`). The brief's boundary ("resource-model/regen = the
  tempo axis, separate seam") is thus **already wired** — tempo is NOT free for E4 to annex.
- `bc_range` → geometry/engagement (E1-adjacent). `bc_attribute` → STR/DEX/INT/WIS (identity).
  `bc_proxy_density` → E6 proxy suite.

**The tension.** `bc_tempo` is *semantically the closest* to cast-time — its own catalog docstrings
describe it in cast-timing language: "Low tempo requires holding cooldowns for the boss spike window"
/ "High tempo requires sustained output with no cooldown windows" (`endgame_encounter_catalog.py:186-187, :227-228`).
But it is **already claimed** by the resource-model seam. So E4 has a genuine coordinate problem that
E1 and E2 did not: **there is no unclaimed BC coordinate that cleanly means cast-time.**

**Candidate answers.**
- **(a) Derive cast-time from the skill KERNEL (role, tier, delivery) — no BC coordinate.** This is
  exactly how E1 assigns geometry (`assign_skill_geometry(role, tier, damage_scaling_type)`,
  :684). Cast-time becomes a function of what the skill IS (a beam_channel winds up; a
  single_target snaps), not of a per-cell BC bin. *Strength:* needs no new coordinate; rides the
  kernel E1 already established; thematically coherent (delivery shape → cast texture). *Weakness:*
  cast-time then does NOT vary cell-to-cell the way amplitude does under E2 — it is a kit-internal
  texture, not a "same cell, three hands" differentiator.
- **(b) A NEW cast-time coordinate on the catalog** (e.g. a `bc_windup` bin snap/wind-up/charge). Gives
  cell-grain cast-time differentiation parallel to E2. *Weakness:* expands the 68,040-cell BC space
  (already large), needs a new bin scheme + D7-named vocabulary, and the catalog is not currently
  crawl-scoped to populate it. Heavy.
- **(c) Couple cast-time to E2's amplitude coordinate** (spiky = winds up to a big committed hit; flat
  = quick snaps). *Strength:* no new coordinate; thematically tight (spiky-slow-heavy vs
  flat-fast-light is the D2 slammer-vs-wand-caster archetype in one axis). *Weakness:* it makes E4 a
  RIDER on E2 rather than an independent axis — see Fork-5's coupling risk; and it collapses two axes
  into one (less design space).

**My LEAN:** **(a) kernel-derived**, i.e. cast-time is a function of (role, tier, delivery), riding
the E1 kernel — because (b) is disproportionately heavy for a texture axis and the catalog isn't
scoped for a new bin, and (c) over-couples to E2 (Fork-5). Kernel-derivation keeps E4 independent,
cheap on the coordinate side, and thematically honest (a beam channels; a bolt snaps). **Note this
also interacts with Q-E4-2:** if E4 is throughput-NEUTRAL (a), kernel-derived cast-time is pure
feel-per-delivery; if throughput-ACTIVE (b), kernel-derived cast-time means delivery-shape becomes a
risk/reward axis, which is a stronger claim rocket/gamora must cost.

---

## Q-E4-5 — Interaction with E2's `k`: multiplicative stack or orthogonal coordinate?

**The question.** A spiky (high-k) skill already has a LONGER period under E2 (`k_spiky ≈ 1.6` scales
cooldown up). If E4 adds cast-time, does cast-time stack multiplicatively on that already-lengthened
period, or is it an orthogonal coordinate that composes additively/independently?

**The coupling risk (named, per brief).** Under E2, spiky skills = longer period, bigger per-hit.
If E4 *also* makes spiky = longer cast-time (the natural thematic coupling — "spiky slams wind up"),
then **spiky skills get hit twice on the tempo axis** (E2 lengthens the cooldown AND E4 adds a
wind-up), compounding into a skill that fires very rarely. Under E2's conservation law that is fine
*if E4 is also neutral* (period grows, per-hit grows to match). But if the two layers compound
multiplicatively on period WITHOUT joint compensation, the effective throughput drifts — the E2
conservation law leaks via the E4 layer. That is precisely the "if the post-E2 band re-fit lurches,
the conservation law leaked somewhere" failure mode, arriving one axis late.

**Candidate answers.**
- **(a) Orthogonal + jointly conservation-preserving.** Cast-time and `k` are independent coordinates,
  but E4's own conservation law (Q-E4-2a) accounts for the E2-lengthened period: cast-time is folded
  INTO the period `k` already sets (period = k·(cast_time + recovery)), so throughput stays invariant
  across BOTH layers. Cleanest if both axes are neutral. *This requires E2 and E4 to share one period
  model* — rocket must build E4's layer aware of E2's `k`, not blind to it.
- **(b) Multiplicative + intentional (only if E4 is throughput-ACTIVE, Q-E4-2b).** Spiky-AND-winds-up
  is a deliberate high-commitment archetype (the PoE slam-slammer: huge hit, rare, positionally
  demanding). The compounding is the FEATURE. Only coherent if E4 is a real lever and the sim models
  the risk.
- **(c) Cast-time is decoupled from amplitude entirely** (Fork-4a kernel-derivation gives this for
  free — cast-time follows delivery, not the spiky/flat bin), so there is no automatic
  spiky↔slow coupling; a flat kit can still have a channeled beam. Reduces the coupling risk by
  construction.

**My LEAN:** **(a) if E4 is neutral (my Q-E4-2 lean) + (c)'s decoupling via kernel-derivation.**
Concretely: cast-time derived from delivery (Fork-4a), folded into the same period `k` governs
(one shared period model), so throughput is invariant across E1+E2+E4 jointly and there is no
double-hit on spiky. **This is a hard instruction for rocket's math note: E4's period math must be
E2-`k`-aware, not layered blindly on top.** If rocket builds E4 blind to `k`, the E2 conservation
audit will lurch and we will have found the leak the hard way. (b) is the throughput-ACTIVE world and
re-enters with the risk model.

---

## Q-E4-6 — Magnitude character (illustrative lean ONLY — rocket derives exact seconds math-note-first)

**Per Disc #18 I do NOT set exact cast_time seconds here.** Illustrative leans for the eventual design
note, to shape rocket's constraints:
- **Felt-difference floor:** a "slow/committed" cast should read as *distinctly heavier* than a "snap"
  cast — genre convention (D2 FCR breakpoints are perceptible at ~200ms deltas; PoE slam wind-ups run
  ~0.6–1.0s vs ~0.2s snaps). A wind-up under ~0.3s is invisible; the existing `_CAST_TIME` T1=0.3 sits
  right at that floor.
- **Fight-completion ceiling:** a wind-up that regularly fails to complete before fight-truncation is a
  dead skill (the Q-E4-2c second-order concern) — the constraint mirrors E2's "≥2 casts inside a
  representative gauntlet fight" cadence-sanity ceiling.
- **Action-cadence floor:** cast-time must not push effective period below the sim's action cadence in
  a way that makes it invisible (the E2 flat-floor analog), nor above a ceiling that starves the
  rotation.

**D7 naming (any new vocabulary I propose for cast-time archetypes).** If a cast-time archetype
vocabulary is needed (parallel to spiky/flat/variable), my lean is **snap / wind-up / channel** —
`snap` (near-instant), `wind-up` (a committed pre-cast delay paying off in a bigger/committed hit),
`channel` (sustained cast, already the T4 label). These are D7-clean (common ARPG vocabulary, no
AI-tell, visualizable, genre-precedented — PoE/D-series all use "channel"; "wind-up" is universal
melee-game vocabulary). **Explicitly reject** obscure coinages. NOTE: this vocabulary is only NEEDED
if Fork-4 lands on (b) a new coordinate OR a labeled kernel-derivation; under my Fork-4a lean the
archetypes are emergent from delivery and may not need a pinned bin vocabulary — Matt/rocket decide at
design-note time.

---

## Sequencing (KR-visible)

E4 fires **after E2 lands + its post-E2 band re-fit (the conservation-law audit) completes** — the
per-axis rhythm (generate → sim → certify, one axis at a time). E4's landing then triggers the next
band re-fit; whether that re-fit is an *audit* (must-not-lurch) or an *expected re-fit* is decided by
Q-E4-2. Sequence lean unchanged: **E2 → E4 → E3.** E4 carries a **cross-seam dependency E2 did not**
(§0b: a gamora sim consumer for cast_time) — KR should anticipate an E4 dispatch that is NOT
emitter-only, likely a rocket-emitter-layer + gamora-sim-consumer PAIR, with a MIGRATION.md.

---

## Player consequence (why this axis exists)

Today every skill fires the instant it is selected — the game has no *weight of commitment* in its
casts. Cast-time is the ARPG feel-axis that separates the snap of a wand-caster from the earth-shaking
wind-up of a slam. After E4, the same tier spine produces hands that feel *heavy* (commit to the cast,
land the big one) vs *light* (snap-snap-snap, reactive, mobile) — the D2 Smiter/PoE slammer vs the
attack-speed wand-caster, in cast-texture. Whether that difference is pure feel (neutral, Q-E4-2a) or
a real risk/reward gamble (active, Q-E4-2b) is Matt's load-bearing ruling — and it is the difference
between a texture layer and a whole new commitment-fantasy in the kit.

---

## Status: DRAFT — forks await Matt ruling

No ledger flip. No self-ratify. No binding acceptance criteria authored. When Matt rules the forks
below, the E4 design note can be authored fast (E2 rhythm) and a rocket+gamora dispatch pair drafted.

**Forks that MUST be ruled before an E4 design note can be authored (in priority order):**
1. **Q-E4-2 — throughput-NEUTRAL vs throughput-ACTIVE (THE load-bearing fork).** Everything downstream
   (sim-consumer shape, band-refit expectation, magnitude constraints, coupling model) forks on it.
   My lean: (a) neutral for v1, (b) active named as launch-scope re-entry.
2. **Q-E4-4 — source coordinate** (kernel-derived vs new BC coordinate vs coupled-to-amplitude). My
   lean: (a) kernel-derived, riding the E1 kernel.
3. **Q-E4-1 — modulation scope** (attack-full + control-cadence-only + support/T4 exempt). My lean:
   (a) E2-parallel.
4. **Q-E4-5 — E2-`k` interaction** (orthogonal-and-jointly-conserved vs multiplicative). My lean: (a)
   orthogonal, one shared period model, E4 math MUST be `k`-aware. (Follows from Q-E4-2.)
5. **Q-E4-3 — T4 channel reconciliation.** My lean: (a) keep T4 exempt in E4; T4-channel belongs to E6.
6. **Q-E4-6 — vocabulary** (only if Fork-4 needs a pinned bin: snap / wind-up / channel). D7-clean;
   may be emergent (no ruling needed) under Fork-4a.

**A rocket/gamora dependency Matt should know now (not a fork — a fact to rule around):** §0b —
`cast_time_seconds` is emitted (tier-varying) but the sim NEVER reads it. E4 is therefore NOT a free
emitter change; it needs a gamora sim consumer (cross-seam, MIGRATION.md). rocket/gamora derive the
consumer shape math-note-first at design-note time; Matt's Q-E4-2 ruling sizes it (neutral consumer =
light; active consumer w/ interrupt/whiff model = heavy).

**Signed:** gandalf, 2026-07-09 (DRAFT — forks await Matt ruling).

---

## RULINGS RECEIVED (Matt, 2026-07-09 — partial; appended same-day)

| Fork | Ruling | Consequence |
|---|---|---|
| **Q-E4-2** | **(b) THROUGHPUT-ACTIVE** — against the registered lean, ruled with the costs on the table | Cast-time is a REAL risk/reward lever. Bands WILL move; the post-E4 re-fit is an **expected re-fit**, not a conservation audit. gamora must build a risk-model sim consumer (heavy). gandalf risk-channel proposal for the design note: **v1 = motion-whiff** (damage applies at cast COMPLETION against positions at that time — the sim has real positions, so wind-ups genuinely whiff vs mobile targets) **+ fight-truncation** (already real) **+ channel-lock exposure** (channel bin); **damage-interrupt = named v1.1 re-entry** (needs a stagger design pass of its own). Premium PRICED from measured completion/whiff rates, math-note-first — mispricing in either direction is the failure (D3-Inferno unpriced wind-ups = dead skills; priced PoE slams = real archetype). |
| **Q-E4-4** | **(b) NEW BC coordinate** — against the kernel-derivation lean | A commitment coordinate joins the catalog. Design note must pin: coordinate name (gandalf lean: `bc_commitment`; D7-clean common vocabulary), bin vocabulary (ruled via Q-E4-6: **snap / wind-up / channel**), CellDef assignments for the 25 named cells (identity-pinned where the name demands it — K1 Heavy Barbarian=wind-up, K7 Archer=snap, K19 Channeling Cleric=channel; rest default/rolled), sampler integration, space-size bookkeeping (68,040 × 3 = 204,120 — the space of record grows), and whether batch-2 samples the coordinate or pins defaults (sequencing with KR). |
| **Q-E4-6** | **Agreed** — snap / wind-up / channel | Vocabulary now REQUIRED (not emergent) since Q-E4-4 landed (b). Consistency law: "channel" is ONE mechanic everywhere it appears — this bin, the rotational family's `while_channeling` persistence mode, the spin-channel re-cert. |
| **Q-E4-1** | NOT RULED — Matt: "unsure of the meaning of the question" | Re-explained in-session (which skill SLOTS of a kit carry cast-time). Reconciled lean under his other rulings: attacks full + control cast-only + **T4 per-capstone bins** (per Q-E4-3 direction) + support exempt. |
| **Q-E4-3** | IN DIALOGUE — Matt reframe: *"the goal of the channeled T4 is inversion from spiky… then it should fall under the same rules"* | gandalf synthesis offered: T4 enters the SAME coordinate rules; the blanket inert `channeled` label DIES; each T4 capstone DECLARES its bin honestly (mode-shift/toggle=snap · conjure-summon=wind-up, the 1.0s deliberate act · sustained-output=channel with real channel-lock). E6 consumes the same vocabulary. Awaiting Matt confirm. |
| **Q-E4-5** | IN DIALOGUE — Matt inclined to agree, asks: *"Could we end up with a scenario where spiky casters are rewarded as their band differs substantially from the rest?"* | Answered in-session: under (b)-ACTIVE yes-by-design UNLESS guarded — the guards are (1) risk-PRICED premium (expected throughput in-band, variance carries the fantasy), (2) regime-mix certification (gauntlet must sample mobile regimes where wind-ups genuinely whiff, else pricing is dishonest), (3) fairness-band gate at cert. Coherent Q-E4-5 form under (b): ONE shared period model, k-aware, with a priced premium term (not full conservation). |

**Status flip: DRAFT → PARTIALLY RULED.** Design note authoring gates on: Q-E4-1 ruling + Q-E4-3 confirm + Q-E4-5 close.

---

## RULINGS RECEIVED — round 2 (Matt, 2026-07-09 — same-day; closes the set)

| Fork | Ruling | Consequence |
|---|---|---|
| **Q-E4-1** | **(b)** — attacks full + control cast-only + support exempt (+ T4 per-capstone per Q-E4-3) | Attack slots carry the kit's bin identity; control skills take a REAL cast time (locking someone down costs a commitment window — the anti-free-Teleport guard) but do not define the kit's coordinate; support/utility fires instantly (no fantasy in a delayed banner); T4 declares per-capstone. |
| **Q-E4-5** | **CLOSED — "agreed with the 3 guards"** | The guards enter the design note as LAW: (1) risk-PRICED premium from measured completion/whiff rates — expected band center stays in tolerance, VARIANCE carries the fantasy; (2) regime-mix certification — the gauntlet MUST sample mobile regimes where wind-ups genuinely whiff (the guard that actually prevents spiky-caster over-reward); (3) fairness-band gate at cert stays the arbiter regardless of bin. One shared period model, k-aware, priced premium term. |
| **Q-E4-3** | **CLOSED — "agreed"** + Matt extension RULED: *"if channeled inverts all main skills … the kit should flip its BC axis coordinates from spiky to flat as well, right?"* → YES | **Capstone coordinate-transform law:** every T4 capstone declares `(commitment_bin, amplitude_delta ∈ {none, flatten, invert})`. A whole-kit rhythm-inverting channel capstone (the mode-shift-into-channel-stance form — all main skills fire through the channel) declares `invert` → the kit's EXPRESSED post-T4 coordinate flips spiky→flat, and certification fires at the expressed coordinate (the measured band must CONFIRM the declaration; mismatch = cert fail — substrate votes). A single sustained-output skill woven among burst skills declares `flatten` or `none` — legal, but it is NOT an "inversion" capstone. Bookkeeping: the kit's GENERATION cell (sampler address, roster K-number) stays stable; the cert record carries native + post-T4 expressed coordinates. Precedent: the K13→K12 artillery fold already works this way (T4 carries a kit across expressed coordinate space without a new cell). E6 consumes this grammar. |

**Status flip: PARTIALLY RULED → FULLY RULED (all six forks closed).** The E4 design note is UNGATED —
it fires next, then the rocket+gamora dispatch pair (cross-seam, MIGRATION.md) goes to KR.
