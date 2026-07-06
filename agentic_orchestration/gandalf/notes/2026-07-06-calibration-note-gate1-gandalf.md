# Gate-1 (design) — proxy-magnitude calibration math note

> **▶ ROLE: DRIFT-CRITIC — judging a math spec against the summoner class-fantasy it must encode.**
> **Verdict: RATIFY-WITH-CONDITIONS.**
> Reviewer: gandalf (design / experiential dimension). Peer: jack-ryan (technical, parallel).
> Target: `reincarnated-engine/src/reincarnated/simulation/notes/proxy-magnitude-calibration-math-2026-07-06.md` (gamora, `066ba37`).
> Date: 2026-07-06. Authority: Matt required design eyes — "summon strength is class-fantasy surface, not just a balance constant."

---

## The four design charges — findings

### Charge 1 — Does marginal-value PRESERVE the summoner fantasy? YES, with a floor caveat.

The frame is correct at the root and I want to be emphatic about WHY, because it is the strongest
thing in this note. `required_summon_KPM = clear_bar − solo_caster_baseline` is the ONLY frame that
refuses to ship a lie. "Does the pair clear?" would license a caster-with-a-cosmetic-pet. Marginal-
value makes the summon carry a share the caster demonstrably does NOT provide. That is the commander
fantasy stated as arithmetic. Genre precedent: this is exactly the discipline Diablo II's Necromancer
skeleton line got RIGHT (skeletons + skeletal mages were your clear engine; you were a conductor) and
what Diablo III's early Witch Doctor pets got WRONG at launch (pets were a passive DPS tax you ignored
while Acid Cloud / Firebats did the real work — the pet fantasy was decorative until the Zunimassa/
jade reworks made them load-bearing). The frame here structurally forbids the D3 Witch-Doctor-launch
outcome. Good.

**BUT the floor at 0.15 is too low to guarantee the fantasy READS.** 15% of the clear is a number a
player never feels. In ARPG player-perception terms, a contributor below ~⅓ of clear reads as *ambient*,
not *load-bearing* — the player's eye tracks their own casts and the army becomes visual noise. PoE's
own design discourse on minions (the "are my zombies actually doing anything" complaint that drove the
Spectre/Skeleton-mage rebalances) lands right at this threshold. A kit calibrated to sit at exactly
0.15 passes the math and still *feels* like the caster is soloing with pets underfoot. **The floor
being non-degenerate-for-balance is not the same as load-bearing-for-fantasy.** See Condition 1.

### Charge 2 — Is "proxy-dominant hazard" a DESIGN failure, not just a balance number? YES. Fully agree.

Matt is right and the note is right to name it shippably wrong. A kit that clears on its non-summon
remainder while skeletons stand around is a fantasy LIE in the exact mirror of the floor failure — and
it is the WORSE lie, because it's a non-interactive autobattler wearing a summoner costume. The note's
own citation (D2-dominance, "boss dies with player realized damage ≈ 0") is the right detection. This
is not an over-tuned constant; it is a class-identity inversion. The player bought "I command an army"
and received "I press one button and watch." Genre precedent: this is the Diablo III *pre-nerf* Sage's-
journey / early-set autobattler complaint and every "my build plays itself" thread that GGG explicitly
designs against. Ceiling at 0.70 is correct as a WALL. I have no condition against it — I *endorse* the
ceiling as a design gate, not merely a balance clamp.

### Charge 3 — Ranged vs melee summoner: are these DIFFERENT class fantasies? YES — and this is the note's most important open question. STRONGEST CONDITION HERE.

The note flags the caster proxy is RANGED (`autonomous_caster`, projectile, 10m), the two WR=1.0
anchors are MELEE, and the one ranged curated kit (`demo_gravecaller`, spectral archer) FAILED via
nav-borne evaporate. gamora reads this correctly as possibly-structural (a nav/re-engage gap, not a
magnitude shortfall) and correctly refuses to patch it in sim. From the DESIGN chair I go further:

**A melee-summoner and a ranged-summoner are not the same fantasy, and a single f_army band applied to
both is a category error waiting to happen.**

- **Melee summoner = the meat-wall / bone-guard fantasy.** Skeleton warriors, golems, crypt guards.
  The army is a *presence* — it tanks, it walls, it body-blocks the corridor. Its contribution is
  partly DPS and partly *space control and aggro-holding the player can SEE*. D2 Necromancer skeletons,
  Grim Dawn's Cabalist/Necromancer skeletal warriors, Last Epoch's Acolyte skeletons. The fantasy is
  fulfilled even when raw DPS share is modest, because the wall is *doing a legible job*.

- **Ranged summoner = the spectral-artillery / bound-caster fantasy.** Spectral archers, bound wraith-
  casters, phantasm swarms (PoE's Summon Phantasm / Spectral archers, D2's Valkyrie-adjacent ranged,
  Last Epoch's Wraiths). This army's ENTIRE reason to exist is *projected damage from behind the
  player's line*. It has no wall value. If it under-delivers DPS it has failed COMPLETELY — there is no
  "but it tanked" consolation. A ranged summon that evaporates or sits out of range isn't a weak
  summon; it's an ABSENT one.

**Design consequence:** the f_army *floor* should arguably be HIGHER for a ranged summoner than a melee
one, precisely because a ranged summon has no non-DPS job to fall back on for fantasy-fulfillment. A
melee wall at 0.20 DPS-share still reads as load-bearing (you see it tanking). A ranged archer at 0.20
DPS-share reads as decorative — it has no other job. So a single [0.15, 0.70] band mis-serves BOTH:
too-low a floor for ranged, and a DPS-only frame that ignores melee's legible wall-value. The note's
own suggestion — a possible ranged/melee SPLIT in `PROXY_TIER_HP_FACTOR` / count-wall raised to
knight-rider as a generation primitive — is the right escalation. I am converting it from "possible
raise" to a **design condition** (Condition 2). This is a class-fantasy fork, not a tuning knob.

### Charge 4 — Class-fantasy surface at emission. Constraints for when rocket emits varied summoners.

The note is scoped to magnitudes and correctly doesn't cover emission thematics, but Matt's charge 4
asks and I own the answer. When rocket emits varied summoners, the summons must READ as the summoner's
OWN. Constraints (Condition 3, forward-looking, non-blocking for THIS note):

- **Element coherence.** A fire summoner's proxies are fire-themed (flame wisps, cinder-hounds), not
  generic skeletons. The proxy's damage element should inherit or thematically consort with the parent
  kit's element. A water summoner fielding bone acolytes is an emission failure.
- **Weapon/geometry coherence.** A projectile-caster summoner fielding melee golems is a mixed message.
  The summon's geometry (`melee_strike` / `projectile` / `ground_slam`) should read as an EXTENSION of
  the summoner's own combat verb, not an unrelated one. (This is where the ranged/melee split of Charge
  3 and the emission-coherence of Charge 4 CONVERGE: the summon's geometry choice is simultaneously a
  balance-band selector AND a fantasy-coherence selector. They must be decided TOGETHER, not separately.)
- **Name/identity coherence.** The proxy's identity fields (name, description) must derive from the
  parent kit's identity, not a generic proxy pool. "Spectral archer" summoned by a necromancer reads;
  summoned by a storm-mage it reads as an asset-reuse tell — the exact "generic proxy" failure Matt
  names. Genre precedent: this is what makes D2's Necromancer feel authored (skeletons ARE the death-
  mage's craft) versus a summon bolted onto any kit.

---

## Verdict: RATIFY-WITH-CONDITIONS

The marginal-value frame is design-CORRECT and I ratify it enthusiastically as the right architecture.
The ceiling (proxy-dominant hazard as a design gate) I fully endorse. The conditions are about the
FLOOR reading as fantasy and the ranged/melee fantasy split — neither BLOCKS the calibration math from
proceeding (they attach to the re-fight READ and to a downstream generation primitive), so the verdict
is conditions, not BLOCK.

### Design conditions (numbered)

1. **Floor-reads-as-fantasy gate on the re-fight READ (non-blocking to the math, binding on the
   verdict).** When the caster-cell re-fight reads `proxy_realized_damage_dealt` per shell, do NOT grade
   a summoner PASS at the raw 0.15 balance floor without a fantasy-legibility check. A kit landing in
   [0.15, ~0.30) of clear should be FLAGGED as "balance-passing / fantasy-marginal" and surfaced to the
   Gate, NOT silently graded PASS. The design floor for "the army is the build" reads closer to ~⅓ of
   clear for a DPS-only (ranged) summon. Recommendation: report the f_army value alongside the pass/fail
   so the design chair can see WHERE in the band it landed — the band's LOWER third is a yellow zone, not
   a green one.

2. **Ranged/melee fantasy split — escalate as a generation primitive, do NOT collapse into one band.**
   Convert gamora's "possible raise to knight-rider" into a firm design recommendation: a ranged
   summoner and a melee summoner are DIFFERENT class fantasies with different fantasy-fulfillment
   economies (melee has legible wall-value as a fallback; ranged is DPS-or-nothing). A single
   [0.15, 0.70] f_army band mis-serves both. The re-fight should be permitted to conclude that the
   ranged cell needs its OWN floor (likely higher) and/or its own survivability/nav treatment
   (`PROXY_TIER_HP_FACTOR` / count-wall / a nav-aware ranged primitive). If the caster-cell contribution
   zeroes via the documented nav gap, that is STRUCTURAL and must route to knight-rider as a rocket-seam
   ranged-summon primitive — NOT be masked by a magnitude bump. gamora already commits to this in §5.5;
   I am ratifying that commitment AS a binding condition.

3. **Emission-time class-fantasy coherence (forward-looking; non-blocking for this note, binding when
   rocket emits varied summoners).** When varied summoners are emitted, the proxy must READ as the
   summoner's own along three axes — element, weapon/geometry, and name/identity — all inherited from or
   thematically consorting with the parent kit. The summon's geometry choice is simultaneously a
   balance-band selector (Condition 2) and a fantasy-coherence selector (this condition); the two must be
   decided together. This condition attaches to the emission dispatch, not this calibration math.

---

## What I explicitly ENDORSE (not just permit)

- The marginal-value frame as the correct architecture. It structurally forbids the Diablo-III-launch-
  Witch-Doctor decorative-pet failure. This is the single best decision in the note.
- The proxy-dominant-hazard ceiling as a DESIGN gate, not a balance clamp. A summoner that clears on its
  remainder is a class-identity inversion and shippably wrong. Agreed without reservation.
- gamora's refusal to patch a structural nav gap with a magnitude bump. Correct discipline; the honest
  test is the pack-shell re-fight, and structural failures route up, not around.

**Signed:** gandalf, 2026-07-06 (Gate-1 design dimension; RATIFY-WITH-CONDITIONS; to critique pair alongside jack-ryan process review).
