# Proxy Pairing — Q6 CONVERGENCE Pair-Matrix + Q7 DUAL_PROXY Compatibility Pools

> **STATUS:** CANONICAL DESIGN SPEC — **DRAFT v1** (2026-07-02). Structure, partition, matrix, and pools
> complete; **Legolas Mode-A genre pull IN FLIGHT** (fold pass amends heuristics + anti-pattern checks on
> return). Per the ratified Session-1 process (rulings Q6/Q7, 2026-06-12): gandalf authors offline;
> **Matt reviews §6 EXCEPTION ROWS ONLY.**
> **Feeds:** B1-rebase **Phase 3** (CONVERGENCE + DUAL_PROXY activation) —
> `proxy-t4-suite-spec-2026-07-02.md` v3 §7 names these artifacts as the Phase-2→3 gate.
> **Ratified substrate (GOVERNS):** Session-1 T4 spec §3.1 CONVERGENCE/DUAL_PROXY definitions + exemplars
> (recover: `git show 4313c25^:agentic_orchestration/gandalf/notes/2026-06-12-session-1-t4-architecture-spec.md`) ·
> Session-2 14-type Tier-1 taxonomy (`gandalf/notes/2026-06-12-session-2-proxy-companion-architecture-spec.md` §2) ·
> multi-slot family rule + "Proxies do not summon proxies" (Matt 2026-06-12).
> **Author:** gandalf (SPEC-AUTHOR), 2026-07-02.

---

## 1. The missing formal object — the proxy-TYPE family partition

CONVERGENCE's ratified gate reads *"both must be from different proxy families (e.g., Fighter-family +
Terrain-family)"* — but Session-1 never formalized the partition over the 14 types. The gate cannot be
implemented without it. **This section defines it** (Gate-1 checkable; E0 in §6).

| Family | Members | Shared mechanical identity |
|---|---|---|
| **STRIKER** | Passive Fighter · Autonomous Caster | mobile bodies that deal damage by autonomous action |
| **BULWARK** | Golem/Construct · Bodyguard | pressure-absorbing bodies (taunt / intercept) |
| **BATTERY** | Totem/Turret · Volatile Emitter · Slot-Queue Emitter | stationary continuous/queued output devices |
| **TRIGGER** | Trap/Mine · Charged Threshold Proxy | condition-armed burst (proximity / stack threshold) |
| **ATTENDANT** | Warcry/Buff Spirit · Resource Conduit · Fragile Escort · Terrain Anchor | no-attack benefit projectors (aura / economy / reward / zone) |
| **ECHO** | Delayed Position Shadow | player-state replay (sui generis; one-member family) |

**Verification against ALL six ratified examples** (the partition must reproduce them as legal):
CONVERGENCE exemplars — Fighter+Anchor = STRIKER×ATTENDANT ✓ · Emitter+Conduit = BATTERY×ATTENDANT ✓ ·
Bodyguard+Warcry = BULWARK×ATTENDANT ✓. DUAL pools — Fighter→{Anchor, Warcry, Totem} all cross ✓ ·
Golem→{Conduit, Warcry, Escort} all cross ✓ · Emitter→{Trap, Conduit, Shadow} all cross ✓ (Shadow's
one-member ECHO family is load-bearing here: any 4-family collapse that folds Shadow into BATTERY makes
the *ratified* Emitter pool illegal — the partition is reverse-engineered from ratified law, not taste).

## 2. Q6 — CONVERGENCE pair-matrix

### 2.1 Architecture decision: class semantics, not 79 hand-authored rows

91 total pairs − 12 same-family = **79 cross-family candidates**. Hand-naming 79 merge behaviors is the
minion-soup path (per-pair bespoke rules nobody can hold in their head — the D3 pet-screen problem at the
design layer). Instead: **15 family-pair MERGE CLASSES** carry the semantics; per-pair behavior + name
derive deterministically from (class rule × the two parents' signature mechanics). Genre anchor: SMT/Persona
fusion stays legible across thousands of combinations because results follow CLASS rules, not bespoke
tables. This satisfies the ratified pass criterion — *"each valid pair produces a deterministic named
convergence behavior"* — with 15 rules instead of 79.

### 2.2 The 15 merge classes

| # | Class | Validity | Merge rule (mechanical) | Name template · exemplar |
|---|---|---|---|---|
| 1 | STRIKER×BULWARK | VALID | merged body attacks AND taunts/intercepts | "<X> Juggernaut" · Fighter+Golem → **Juggernaut** |
| 2 | STRIKER×BATTERY | VALID | mobile attacker carries the battery's output cadence | "Barrage <X>" · Caster+Slot-Queue → **Barrage Caster** |
| 3 | STRIKER×TRIGGER | VALID | attacker's own hits arm the threshold; burst at cap | "Threshold <X>" · Fighter+Charged → **Threshold Duelist** |
| 4 | STRIKER×ATTENDANT | VALID **(ratified class)** | attacker projects the attendant benefit while fighting | "Fighting <X>" · **Fighting Anchor** (ratified: +40% amp aura) |
| 5 | STRIKER×ECHO | VALID ⚑ sim-cost (E4) | attacker interleaves replayed player skills | "Mirror <X>" · Fighter+Shadow → **Mirror Blade** |
| 6 | BULWARK×BATTERY | VALID | anchored fortress: taunts/intercepts while firing | "Bastion <X>" · Golem+Totem → **Bastion Colossus** |
| 7 | BULWARK×TRIGGER | VALID | absorbed hits FEED the charge; detonates at threshold | "Retribution <X>" · Bodyguard+Charged → **Retribution Ward** |
| 8 | BULWARK×ATTENDANT | VALID **(ratified class)** | protection + benefit at 70% efficiency each | "Warding <X>" · **Shielded Augmenter** (ratified) |
| 9 | BULWARK×ECHO | **INVALID (E1)** | hold-the-line and replay-from-position contradict — no single readable entity | — |
| 10 | BATTERY×TRIGGER | VALID | continuous output + threshold burst on one emplacement | "Overload <X>" · Totem+Charged → **Overload Turret** |
| 11 | BATTERY×ATTENDANT | VALID **(ratified class)** | output device converts damage into player benefit | "Harvest <X>" · **Harvest Bomb** (ratified: 25% HP-lost → resource) |
| 12 | BATTERY×ECHO | VALID | emplacement fires RECORDED PLAYER SKILLS as its output | "Echo <X>" · Totem+Shadow → **Echo Turret** |
| 13 | TRIGGER×ATTENDANT | VALID | trigger event grants a player benefit window | "Rallying <X>" · Trap+Warcry → **Rallying Snare** |
| 14 | TRIGGER×ECHO | VALID | trigger fires a replayed player skill at the triggering enemy | "Ambush <X>" · Trap+Shadow → **Ambush Shade** |
| 15 | ATTENDANT×ECHO | **CONDITIONAL (E2)** | only Terrain Anchor+Shadow legible: zone replays player skills from within | "Haunted Ground" · others struck |

All exemplar names are WORKING names — flavor rides the phase-5 T4 narration pass (spec v3 convention).

### 2.3 Per-pair strikes within valid classes

**Fragile Escort is struck from CONVERGENCE entirely (E5).** Its mechanic IS the fragility tension
(high reward while alive × very low HP). Merging averages HP up (avg×1.2) — the merge erases the defining
risk (Golem+Escort = reward without fragility, degenerate) or duplicates its ASCENSION upgrade lane
(Protected Escort already exists at §2.2 of the Session-2 taxonomy). Escort remains fully DUAL-legal (§3) —
independence *preserves* the fragility mechanic. The asymmetry is the two capstones' distinct logic made
visible.

**Valid-pair count:** 79 cross-family − 2 (class 9) − 3 (class 15 strikes) − 9 (E5 Escort, net of the
class-15 overlap) = **65 valid CONVERGENCE pairs**, all class-derived, 2 carrying the STRIKER×ECHO
sim-cost flag.

### 2.4 Deterministic derivation rule (rocket implements)

For valid pair (A, B): merged entity inherits (i) the higher behavioral tier of the two parents;
(ii) the class merge rule as its behavior contract; (iii) each parent's SIGNATURE mechanic at the class's
efficiency (default 100%/100% unless the class or ratified exemplar says otherwise — class 8 is 70%/70%
by ratified text); (iv) name = class template instantiated with the non-template parent's noun. Same pair →
same entity, every emission. Magnitudes: HP = avg×1.2, damage = sum×0.8 (ratified, PROVISIONAL — §4).

## 3. Q7 — DUAL_PROXY compatibility pools (14 primaries × 3 members)

**Selection principles** (P1–P5; Legolas fold validates/amends): P1 role coverage — output primaries get
≥1 protective option, support primaries get ≥1 output option; P2 cadence contrast (continuous + burst);
P3 spatial contrast (static primaries get ≥1 mobile option, mobile get ≥1 anchor); P4 trigger interplay
(one generates conditions the other consumes); P5 no strictly-dominant member — options trade off against
kit shapes, not rank (dead-choice guard, AQ3).

**Pool-member constraint:** each member is cross-family vs the PRIMARY (members need not be cross-family
with each other — the pool offers alternatives, exactly one is granted). Pool size fixed at 3 (matches all
ratified examples).

**Selection surface:** the second type is chosen at GENERATION time by decl-shape fit (η axis-match
pattern), deterministic per kit — kits are emitted artifacts; there is no player talent-choice surface in
the current engine spec (a player-facing choice UI is future-product scope).

| Primary (family) | Pool | Rationale |
|---|---|---|
| Passive Fighter (STR) | Terrain Anchor · Warcry · Totem/Turret | **RATIFIED** — amp zone / aura / covering fire behind the fighter |
| Autonomous Caster (STR) | Golem · Resource Conduit · Trap/Mine | front-line cover, cast economy, approach denial (P1/P4) |
| Golem (BUL) | Resource Conduit · Warcry · Fragile Escort | **RATIFIED** — the tank enables economy/aura/reward riders |
| Totem/Turret (BAT) | Golem · Warcry · Trap/Mine | bodyguard-the-gun, amp, approach denial (P1/P3) |
| Bodyguard (BUL) | Totem/Turret · Passive Fighter · Resource Conduit | defense is covered; pool supplies output + economy (P1) |
| Volatile Emitter (BAT) | Trap/Mine · Resource Conduit · Delayed Position Shadow | **RATIFIED** — layered zone denial / economy / replay |
| Terrain Anchor (ATT) | Passive Fighter · Totem/Turret · Charged Threshold | bodies that fight INSIDE the zone (P4 — the un-merged Fighting-Anchor fantasy) |
| Resource Conduit (ATT) | Autonomous Caster · Slot-Queue Emitter · Trap/Mine | pure-economy primary needs output to spend into (P1) |
| Trap/Mine (TRG) | Passive Fighter · Terrain Anchor · Totem/Turret | herding into traps, zone, covering fire (P4) |
| Warcry (ATT) | Passive Fighter · Golem · Slot-Queue Emitter | a buff wants beneficiary bodies (P1) |
| Fragile Escort (ATT) | Golem · Totem/Turret · Trap/Mine | aggro-shield + output while the escort pays out (P1/P3) |
| Slot-Queue Emitter (BAT) | Warcry · Charged Threshold · Passive Fighter | burst-stacking + front-line (P2) |
| Delayed Position Shadow (ECH) | Golem · Terrain Anchor · Trap/Mine | line-holding + zone control while the shadow replays (P3) |
| Charged Threshold (TRG) | Passive Fighter · Golem · Warcry | bodies that attract/generate the hits that feed charge (P4) |

**"No convergence-conflicting pairs" interpretation (E3):** read as an INDEPENDENCE assertion, not an
exclusion — a pair may exist both as a CONVERGENCE merge and a DUAL pool grant; DUAL keeps the two
entities operating independently (ratified: *"Both proxies operate independently. No convergence between
them"*). Nothing in the ratified text removes a pair from DUAL because a merge exists; the two capstones
are different answers to the same pairing.

## 4. Magnitudes + sim notes (PROVISIONAL — gamora certifies, Disc #18/#24)

- **CONVERGENCE:** HP = avg×1.2 / damage = sum×0.8 stand as ratified anchors; class-8's 70%/70% stands.
  All PROVISIONAL-by-ratification; certify against the D3 scaffold.
- **DUAL:** no ratified magnitude — the ratified structure is both entities at base stats, gated by
  ≥3 chains. Two full entities vs one is a power question: gamora certifies the delta vs single-proxy
  baseline (AQ4); a per-entity scalar is the reserved lever if the band breaches. Entity count 2 sits
  inside the R4 ceiling (max_active 3).
- **FISSION interaction:** a DUAL or CONVERGENCE kit cannot also carry FISSION (multi-slot family rule:
  only DUAL_PROXY + one member may pair — and that member's own gate must still pass; FISSION+DUAL is
  legal only if the primary type satisfies FISSION's body-tier gate). R4 total-entity cap 4 governs any
  such stack; gamora asserts.
- **STRIKER×ECHO (⚑ E4):** two skill sources on one merged entity — gamora assesses sim cost before the
  class activates; if deferred, the 2 affected pairs carry a named prerequisite, not a silent skip.

## 5. Acceptance criteria (Phase 3; extends spec v3 §8)

- **AQ1:** every emitted CONVERGENCE kit's pair ∈ the valid-65; merged entity demonstrates BOTH parent
  behaviors in one fight (ratified criterion). *(Rides the Phase-1 named prerequisite: generation can emit
  2-type cross-family decls.)*
- **AQ2:** every DUAL kit's second type ∈ its primary's pool-of-3; drawn at generation, deterministic.
- **AQ3:** dead-choice guard — across an emission run, no pool member exceeds 70% share within its
  primary (P5 enforced empirically, not rhetorically).
- **AQ4:** DUAL power delta vs single-proxy baseline certified in-band; scalar lever documented if used.
- **AQ5:** name derivation deterministic (same pair → same working name; feeds phase-5 narration).

## 6. EXCEPTION ROWS — the Matt-review surface (everything else is process-ruled)

| # | Exception | My call | What review changes |
|---|---|---|---|
| E0 | **The family partition itself** (§1) — incl. the one-member ECHO family | 6 families as tabled; reverse-engineered so all six ratified examples stay legal | re-partitioning re-derives the matrix; everything downstream shifts |
| E1 | BULWARK×ECHO class **INVALID** | the merged entity has no readable job description | overruling adds 2 pairs back with a class rule I'd need from you |
| E2 | ATTENDANT×ECHO **CONDITIONAL** — only Haunted Ground (Anchor+Shadow) valid | Warcry/Conduit/Escort + Shadow have no legible single-entity read | overruling adds up to 3 pairs |
| E3 | "no convergence-conflicting pairs" read as **independence-assertion**, not pair-exclusion | pairs may exist on both surfaces; DUAL never merges | the exclusion reading would strike DUAL pool members that have strong merges (e.g. Fighter→Anchor) |
| E4 | STRIKER×ECHO **valid with sim-cost flag** | fantasy is strong (attacker weaving your own skills); cost is gamora's to price | striking it removes 2 pairs pre-emptively |
| E5 | **Fragile Escort struck from CONVERGENCE** (DUAL-legal stands) | merge erases its defining fragility or duplicates its ASCENSION lane | overruling adds 9 pairs + needs a fragility-conserving merge rule |

## 7. Legolas fold slot — PENDING

Mode-A pull in flight (minion-pairing precedent · fusion/merge legibility · complementarity heuristics ·
anti-patterns; findings land at `agentic_orchestration/legolas/research/proxy-pairing-genre-pull-2026-07-02/`).
Fold pass amends: P1–P5 validation, per-pool adjustments (marked as deltas), any anti-pattern strike this
draft missed. Matt's exception-row review fires AFTER the fold, on the amended v2.

**Signed:** gandalf, 2026-07-02 — draft v1; Legolas fold + Matt exception-row review produce v2.
