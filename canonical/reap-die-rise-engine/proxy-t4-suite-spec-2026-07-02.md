# Proxy-T4 Suite — Design Spec v2 (demo activation of the RATIFIED catalog-v2 PROXY family)

> **STATUS:** CANONICAL DESIGN SPEC — feeds Lane B1 (rocket: execution-layer strategies · gamora: sim-eval +
> magnitude certification).
> **REVISED IN PLACE 2026-07-02** (same path B1 consumes). The v1 text (earlier same-day) drafted a parallel
> S1–S6 family in ignorance of ratified prior art; Matt's catch — *"didn't we already have these scoped in a
> doc somewhere? I know for a fact we did"* — surfaced the drift. **The ratified family governs;** v1's
> surviving analysis is folded in; the v1 family retires per §3.
> **Mandate (Matt-ruled 2026-07-02, verbatim):** *"Summon-focused kits MUST have a proxy-focused T4… we are
> expecting summon-kits to time out or die to boss if not for their proxy's DPS… will only one T4 work for
> all Proxies? I'm doubtful… We need to make all of the dormant T4 capstones alive in the engine (including
> proxyspawn) and we also need a full suite of proxy-T4's for the demo, so decent proxy kits can be emitted
> for selection."*
> **Author:** gandalf (SPEC-AUTHOR v1; DRIFT-CRITIC re-base v2), 2026-07-02.
> **Denominators:** `one-realm-mvp-scope.md` §5 ask 4 · serial-emission ledger D.1 #9 (this spec gates both).
> **Ratified prior art (GOVERNS):** `agentic_orchestration/gandalf/notes/2026-06-12-session-1-rulings-q1-q10-t4-catalog-expansion.md`
> (authoritative ruling record, live) · decisions-log 2026-06-12 *"Session 1 architecture rulings Q1–Q10"*
> (Matt-ratified verbatim; **all T4 magnitudes PROVISIONAL pending implementation calibration**) ·
> `agentic_orchestration/gandalf/notes/2026-06-12-session-2-proxy-companion-architecture-spec.md` (live;
> 14-type Tier-1 taxonomy + 3-tier entity model) · the Session-1 T4 architecture spec (purged in a notes
> sweep; recover via `git show 4313c25^:agentic_orchestration/gandalf/notes/2026-06-12-session-1-t4-architecture-spec.md`) ·
> `t4_catalog_v2.py:53-58` (PROXY family constants + family map, with 7 live generation-side consumers).
> **Evidence base (verified first-hand):** `mechanic_alteration.py` (η architecture :65/:69/:338; ABC :255;
> v1.1-deferred list :45-46; `sim_prerequisite` :266-271) · `proxy_vocabulary_bridge.py` (four scaffold levers
> :68/:77/:232/:255) · gamora D3 cert (`gamora/v-proxy-fight-calibration-1` @ `abb010d`) · W2 spike (army
> WR 1.000 vs caster-alone 0.000).

---

## 1. The design problem (v1 analysis — stands)

Every T4 strategy the **execution layer** currently runs amplifies **the caster's own body**
(DirectDamageAmplification: 1.75× at preferred-encounter — `mechanic_alteration.py:664`). W2 measured a
summoner's body at **WR 0.000 caster-alone**; the proxies carry 100% of the kill. A summon-bearing kit drawn
under the current execution set receives a capstone that multiplies its *smallest* contribution surface —
mechanically dead weight, and a broken class fantasy at the exact moment (capstone unlock) the genre
promises the fantasy's peak.

**The actual gap is execution-layer activation, not design.** The ratified catalog-v2 PROXY family exists
and is wired into generation-side machinery (`kit_architecture.py`, `layer2_dimensions.py`,
`investment_profile.py`, `corpus_floor_verification.py`, `companion_generation.py`, `charge_stack_generation.py`,
`vestigial_labels.py`) — but `mechanic_alteration.py` still executes the PRE-catalog v1 register: DDA as
universal primary (**retired by ruling Q3**, yet live in code) plus the v1.1 dormant five at `:45-46`.
**B1 = bring the ratified catalog to the execution + sim-eval + emission layers.**

Genre confirms family-not-node: PoE's Necromancer ascendancy is four distinct minion notables; D2 split
Skeleton Mastery from raise-count; Last Epoch splits minion-damage from minion-count. Matt's doubt — *"will
only one T4 work for all Proxies?"* — was answered at ratification: the six members carry **disjoint
eligibility gates over the 14-type taxonomy** (§2), so different decl shapes structurally draw different
capstones.

## 2. The family — the RATIFIED six

Definitions below are the ratified text (Session-1 spec §3.1, recovered; constants `t4_catalog_v2.py:53-58`).
Flavor naming rides the phase-5 T4 narration pass, NOT this spec.

| Member | Ratified eligibility | Ratified capstone mechanic | On-screen read (feeds D5) |
|---|---|---|---|
| **PROXY_ASCENSION** | ≥1 Tier-1 mechanical proxy in chain | proxy upgrades one behavioral tier: Passive Fighter → Autonomous Caster (independent rotation from a subset of player skills); Totem/Turret → Range-Gated Turret (+15% player damage adjacent); Volatile Emitter → Slot-Queue Emitter (passive per-tick + burst-on-evoke); full per-type upgrade table in the Session-2 spec | your servant *changes what it is* |
| **PROXY_SOVEREIGNTY** | Passive Fighter OR Golem; energy ≠ mana; ≥3 chains | proxy becomes a full parallel combatant: own charge-stack pool (10, on-hit), autonomous 3-skill rotation (damage/CC/utility) drawn from player skills, independent timing, 20s re-summon | a second hero fights beside you |
| **PROXY_FISSION** | Golem / Passive Fighter / Bodyguard; HP tracking (mid or full body tier) | on-death split 1→2→4 at 60% parent stats per tier; sub-sub-proxies terminal; 30s expiry; hard cap 4 entities | death multiplies the horde — *Reap. Die. Rise.* made mechanical |
| **PROXY_INVERSION** | defensive types only: Bodyguard / Terrain Anchor / Warcry-Buff Spirit | **role inversion**: Bodyguard → Sacrificial (manually consume for a burst = 150% of remaining HP as direct damage); Terrain Anchor → Damage Amplification Zone (+40% player damage, 8s); Warcry Spirit → Reverse-Buff (equivalent-magnitude enemy debuff: damage reduction + slow) | the shield becomes a sword |
| **PROXY_CONVERGENCE** | exactly 2 distinct Tier-1 types, cross-family | the two merge into one Convergent Proxy (HP = avg × 1.2; damage = sum × 0.8; per-pair merge rules, e.g. Fighter+Anchor → Fighting Anchor) | two servants fuse into one |
| **DUAL_PROXY** | exactly 1 Tier-1 type; ≥3 chains | unlocks a second COMPLEMENTARY type from a per-primary compatibility pool; both operate independently (no convergence) | a second, different servant answers |

**Magnitude status:** every number above is **PROVISIONAL by ratification** (the decisions-log status line
says so explicitly) and predates the spatial sim + D3 calibration. gamora certifies each against the
D3-certified scaffold — math-note-first (Disc #18), single-parameter-isolated sweeps (Disc #24), fresh seeds
53M+, boss anchor FIXED per the D3 harness pattern. This is the gauntlet-metrics discipline applied at T4:
designer-asserted magnitudes are hypotheses until sim-validated.

**Multi-slot rule (ratified, Session-1 §2.2):** no two proxy-family strategies on one kit *unless* the pair
is DUAL_PROXY + one other proxy-family member.

## 3. v1-family retirement map (the S1–S6 drafted earlier this session)

| v1 member (RETIRED) | Disposition |
|---|---|
| S1 ProxyDamageAmplification | **SPLIT:** flat proxy-damage% is the **Set-#6 gear capstone's lane** (Clause B inheritance + set bonuses; `proxy_commander.py:59-70` calibrated layer); *behavioral* output-raising at T4 = ASCENSION / SOVEREIGNTY |
| S2 ProxyBulwark | **RETIRED:** "guardian holds the line" is the **Bodyguard taxonomy TYPE** (Session-2 Tier-1 catalog) — a proxy type, not a T4; its T4 story is INVERSION's Sacrificial |
| S3 ProxyLegion | **RETIRED as T4:** more-bodies = FISSION (death-multiplication) at demo, DUAL_PROXY post-gate; the raw `max_active`/count lever stays a **decl/calibration surface** (D3: count 1→2 halves clear time — certified scaffold territory, not capstone territory) |
| S4 ProxySurge | **RETIRED:** spawn-cadence / attack-interval are Set-#6 set-bonus + decl-field territory — gear and calibration layers, not a T4 strategy |
| S5 ProxyDeathConversion | **RETIRED:** FISSION **is** the ratified on-death conversion; the corpse-burst variant ≈ INVERSION's Sacrificial consume |
| S6 ProxySpawn-revived | **RETIRED as T4:** the Session-2 three-tier table rules non-summoner proxy acquisition = *"summon-first allocation OR low-probability trait"* (generation paths) — not a T4 strategy in the v2 world; the "including proxyspawn" verbatim routes to §6 ruling (a) |

**What v1 contributes forward:** the §1 problem statement + W2/D3 evidence; the η/emission integration
intent (§4); the boundary rulings (§5); the acceptance criteria (§8). Root cause of the drift is logged in
the session record: SPEC-AUTHOR skipped the design-corpus sweep the framing-audit checklist (OP §4.1 Q2)
mandates — the Set-#6 spec cited in v1 says "proxy chain-T4" verbatim and should have triggered it.

## 4. η / emission integration intent (which capstone does THIS summoner draw)

The existing architecture carries everything needed: `η = 0.50·axis_match + W_THEMATIC·thematic +
W_SIM_VIABILITY·sim_viability`, floor 0.35, highest-η commits (`mechanic_alteration.py:338` pattern).

1. **Hard eligibility = the RATIFIED per-member gates (§2)**, implemented in each `opportunity_scan()` →
   0.0 outside eligibility. A non-summoner can never draw a proxy capstone — the mirror image of today's bug.
2. **axis_match keys off DECL SHAPE** within the eligible set — Matt's doubt answered structurally first
   (the gates partition: defensive types → INVERSION; mid/full-HP bodies → FISSION; any mechanical →
   ASCENSION), then by rank: count-N minimal bodies → ASCENSION lean · count-1 full body → INVERSION/FISSION
   lean · ≥3-chain non-mana kits bring SOVEREIGNTY into range.
3. **thematic** follows the element-resonance pattern (blood-magic precedent `:325-334`): shadow/earth
   resonate for FISSION (grave imagery); neutral ~0.05–0.20 elsewhere.
4. **sim_viability → 1.0 on activation** — the `sim_prerequisite` strings (`:266-271`) are the dormancy
   mechanism; clearing them per §6 IS the revival.
5. **Emission bands (measured, not forced):** proxy-heavy kits emit a proxy-family `primary_t4` at **≥90%**;
   proxy-light at **≥60%** (the hybrid caster fantasy legitimately lets self-cast T4s compete there).
   Self-cast T4s stay in `t4_candidates` for summoners — outcompeted at scan-time by design, not banned.
6. **Manifestation ladder holds** (`_manifestation_from_tier`): continuous axes scale down at rank2/rank3;
   FISSION and DUAL_PROXY integer/entity axes are **T4_active-only** (η=0 below tier 3).

## 5. Interaction rulings

- **R1 — Bridge-state no-propagation:** DDA is **retired by ruling Q3** in the v2 catalog but LIVE in the
  execution layer; while it remains live, it does NOT touch proxy damage — player-primary and proxy
  amplification stay separate surfaces. The **sanctioned cross-surface path is Set-#6 Clause B**
  (gear-layer inheritance) — the gear capstone, not the T4 layer, carries player→proxy stat flow. gamora
  asserts separation in tests.
- **R2 — Decl-surface only:** T4 levers write per-kit decl/behavioral fields; bridge module constants
  (`:68/:77/:232/:255`) stay untouched DEFAULTS; the Set-#6 calibrated contribution constants
  (`proxy_commander.py:59-70`) are a hard boundary — T4 multiplies on top of the certified scaffold.
- **R3 — One `primary_t4` per kit** (existing rule holds); the ratified multi-slot family rule (§2) governs
  multi-chain slots; family members enter `t4_candidates` alongside self-cast strategies.
- **R4 — Entity-count integrity:** FISSION hard-caps at 4 (ratified); `max_active` ceiling stays 3 (the
  D3-tested max) until gamora certifies higher; the count-wall lever remains decl/calibration territory (§3 S3).
- **R5 — Solo invariance:** the eligibility gates structurally guarantee zero effect on solo-bin kits;
  asserted anyway (A6).

## 6. Dormant-register reconciliation — ⚑ MATT RULING (a) PENDING

Two registers collide inside the 2026-07-02 ruling's verbatim. The **v1.1 dormant five**
(ResourceBuffer, MechanicReplacement, ZoneControl, ConditionalModifier, ProxySpawn —
`mechanic_alteration.py:45-46`) are a **PRE-catalog register**: none of the five names appears among
catalog-v2's ratified 25 (which also retired DDA, with Q3's no-grandfathering discipline).

- **Reading (i) — literal:** revive the five as named, alongside the catalog family.
- **Reading (ii) — through-successor (gandalf lean):** "make the dormant capstones alive" binds to the
  ratified successor register. rocket runs a **mapping audit** for the four non-proxy names
  (ResourceBuffer / MechanicReplacement / ZoneControl / ConditionalModifier → nearest catalog-v2 member OR
  a **NAMED residual** — no silent re-defer, per the no-deferral-as-disposition discipline). ProxySpawn's
  *capability* (non-summoners can gain a proxy) is satisfied by the Session-2 generation paths
  (low-probability trait; summon-first allocation) and DUAL_PROXY carries the second-proxy grant.
- Because Matt's ruling says **"including proxyspawn" verbatim**, reading (ii) ships only with his explicit
  confirmation that the capability satisfies the intent without the strategy name.

Either way, each disposition clears or re-names its `sim_prerequisite` string with a one-line justification
in the rocket change.

## 7. Demo-critical subset — ⚑ MATT RULING (b) PENDING

**gandalf lean: ASCENSION + FISSION + INVERSION demo-critical.**

- **ASCENSION** — broadest eligibility (any Tier-1 mechanical proxy); the "capstone changes what your
  servant IS" beat is the family's clearest fantasy peak.
- **FISSION** — the *Reap. Die. Rise.* keystone made mechanical; W2's `hp<=0` death event is the trigger it
  needs; covers the many-bodies fantasy at demo.
- **INVERSION** — Matt's remembered keystone; covers the defensive types; the Sacrificial consume is the
  most legible single beat in the family.
- **SOVEREIGNTY** — stretch, not critical: heaviest sim machinery (independent energy pool + autonomous
  3-skill rotation).
- **CONVERGENCE + DUAL_PROXY — post-demo by PRIOR ruling:** Q6/Q7 process-ruled their pair-matrix and
  compatibility pools to fire AFTER the proxy-primary empirical gate; neither artifact exists as live canon
  (the draft note died in the notes purge). Not demo work.

**Descope valve within the subset:** INVERSION's *manual* Sacrificial consume — the sim realizes it as a
consume **policy** (threshold / burst-window automation); the player input hook is a **Godot-layer handoff**
(the legitimate deferral type), not a cut. No member of the leaned three is cuttable without breaking
coverage (ASCENSION carries breadth; FISSION carries theme; INVERSION carries the defensive types).

## 8. Acceptance criteria (testable; Gate-1 checks against these)

- **A1 — Emission:** post-un-gate demo emission run — every proxy-bin kit carries ≥1 family member in
  `t4_candidates`; `primary_t4` family-share meets the §4.5 bands (≥90% heavy / ≥60% light).
- **A2 — Sim delta:** each activated member applied to a D3-certified fixture produces a measurable
  build-floor delta vs no-T4 baseline in its axis direction. No member makes caster-alone viable — the T4
  amplifies the proxy contribution, not the body.
- **A3 — Differentiation (THE Matt-doubt test):** the two D3-certified fixtures draw **different** top
  family members via gates + axis_match. If both draw the same top member, under-differentiated — rework
  before ship.
- **A4 — Legibility:** each member's on-screen read (§2, last column) is distinct enough to name in one
  clause — feeds D5 verb realization and the galadriel benchmark later.
- **A5 — Boundaries asserted:** R1 (bridge-state no-propagation; Set-#6 Clause B is the only sanctioned
  cross-surface) + R2 (calibrated layer untouched) have explicit test assertions.
- **A6 — Solo invariance + no silent re-defer:** family zero-effect on solo-bin kits asserted; every §6
  disposition carries successor-or-named-residual.

## 9. Open Matt-plate items (carried to the next report)

- **(a)** §6 register binding — literal revival vs through-successor.
- **(b)** §7 demo-critical subset — ratify or amend the ASCENSION + FISSION + INVERSION lean.
- **(c)** **INVERSION depth:** the ratified text is proxy-ROLE inversion (per-type). Matt's session memory
  is **KIT-level inversion** — consume the proxy → drastically buff the caster's other skills. If that is a
  distinct wanted mechanic, it is either an INVERSION amendment (a second consume mode) or Q6 merge-matrix
  territory (post-gate). Not folded into B1 without a ruling.

## 10. What this spec does NOT own

Final magnitudes (gamora — certification of the PROVISIONAL ratified numbers, Disc #18/#24, seeds 53M+) ·
implementation architecture and strategy-class code (rocket) · grading thresholds (gamora) · T4 flavor
naming/narration (phase-5 pass) · the Q6/Q7 matrices (post-gate by process ruling) · the ranged-proxy NAV
question (PART E fork — D3 confirmed a decl `count` raise is a content-level mitigation).

**Signed:** gandalf, 2026-07-02 — v1 same-day; v2 re-base after Matt's prior-art catch. **B1 fires against
THIS revision.**
