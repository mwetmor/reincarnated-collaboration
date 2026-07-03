# Proxy-T4 Suite — Design Spec v3 (demo activation of the RATIFIED catalog-v2 PROXY family)

> **STATUS:** CANONICAL DESIGN SPEC — feeds the B1-REBASE dispatch (rocket: execution-layer strategies ·
> gamora: sim-eval + magnitude certification).
> **v3 AMENDED 2026-07-02 — Matt rulings folded:** five-name dormant register **RETIRED** (§6, provenance
> verified: never designed, shortlist-tail); **ZONE_CONTROL enters as a newly DESIGNED 26th catalog member**
> (§6.1, COMBAT-family lean); **PROXY_INVERSION DEFERRED WHOLLY** (§7.1, named disposition); demo family =
> **five ratified members, two-phase activation** (§7). **The B1-rebase fires against THIS version.**
> **v2 (same-day):** re-based on the ratified family after Matt's prior-art catch — *"didn't we already have
> these scoped in a doc somewhere? I know for a fact we did"* — v1's parallel S1–S6 family retired per §3.
> **Mandate (Matt-ruled 2026-07-02, verbatim):** *"Summon-focused kits MUST have a proxy-focused T4… we are
> expecting summon-kits to time out or die to boss if not for their proxy's DPS… will only one T4 work for
> all Proxies? I'm doubtful… we also need a full suite of proxy-T4's for the demo, so decent proxy kits can
> be emitted for selection."* (The "dormant capstones alive" clause of the same ruling is RESOLVED by the §6
> retirement ruling — it reads as: activate the ratified catalog.)
> **Author:** gandalf (SPEC-AUTHOR v1; DRIFT-CRITIC re-base v2; rulings-fold v3), 2026-07-02.
> **Denominators:** `one-realm-mvp-scope.md` §5 ask 4 · serial-emission ledger D.1 #9 (this spec gates both).
> **Ratified prior art (GOVERNS):** `agentic_orchestration/gandalf/notes/2026-06-12-session-1-rulings-q1-q10-t4-catalog-expansion.md`
> (authoritative ruling record, live) · decisions-log 2026-06-12 *"Session 1 architecture rulings Q1–Q10"*
> (Matt-ratified verbatim; **all T4 magnitudes PROVISIONAL pending implementation calibration**) ·
> `agentic_orchestration/gandalf/notes/2026-06-12-session-2-proxy-companion-architecture-spec.md` (live;
> 14-type Tier-1 taxonomy + 3-tier entity model) · the Session-1 T4 architecture spec (purged in a notes
> sweep; recover via `git show 4313c25^:agentic_orchestration/gandalf/notes/2026-06-12-session-1-t4-architecture-spec.md`) ·
> `t4_catalog_v2.py:53-58` (PROXY family constants + family map, with 7 live generation-side consumers).
> **Evidence base (verified first-hand):** `mechanic_alteration.py` (η architecture :65/:69/:338; ABC :255;
> the now-retired v1.1 docstring register :45-46; `sim_prerequisite` :266-271) · `proxy_vocabulary_bridge.py`
> (four scaffold levers :68/:77/:232/:255) · gamora D3 cert (`gamora/v-proxy-fight-calibration-1` @ `abb010d`) ·
> W2 spike (army WR 1.000 vs caster-alone 0.000) · provenance trail for §6 (`f9762a8` → `d6bca67`).

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
universal primary (**retired by ruling Q3**, yet live in code) plus a v1.1 docstring register now
**retired by ruling** (§6). **The B1-rebase = bring the ratified catalog to the execution + sim-eval +
emission layers.**

Genre confirms family-not-node: PoE's Necromancer ascendancy is four distinct minion notables; D2 split
Skeleton Mastery from raise-count; Last Epoch splits minion-damage from minion-count. Matt's doubt — *"will
only one T4 work for all Proxies?"* — was answered at ratification: the members carry **disjoint
eligibility gates over the 14-type taxonomy** (§2), so different decl shapes structurally draw different
capstones.

## 2. The family — the RATIFIED six (five active + one deferred)

Definitions below are the ratified text (Session-1 spec §3.1, recovered; constants `t4_catalog_v2.py:53-58`).
Flavor naming rides the phase-5 T4 narration pass, NOT this spec.

| Member | Ratified eligibility | Ratified capstone mechanic | On-screen read (feeds D5) |
|---|---|---|---|
| **PROXY_ASCENSION** | ≥1 Tier-1 mechanical proxy in chain | proxy upgrades one behavioral tier: Passive Fighter → Autonomous Caster (independent rotation from a subset of player skills); Totem/Turret → Range-Gated Turret (+15% player damage adjacent); Volatile Emitter → Slot-Queue Emitter (passive per-tick + burst-on-evoke); full per-type upgrade table in the Session-2 spec | your servant *changes what it is* |
| **PROXY_SOVEREIGNTY** | Passive Fighter OR Golem; energy ≠ mana; ≥3 chains | proxy becomes a full parallel combatant: own charge-stack pool (10, on-hit), autonomous 3-skill rotation (damage/CC/utility) drawn from player skills, independent timing, 20s re-summon | a second hero fights beside you |
| **PROXY_FISSION** | Golem / Passive Fighter / Bodyguard; HP tracking (mid or full body tier) | on-death split 1→2→4 at 60% parent stats per tier; sub-sub-proxies terminal; 30s expiry; hard cap 4 entities | death multiplies the horde — *Reap. Die. Rise.* made mechanical |
| **PROXY_INVERSION** — **⛔ DEFERRED WHOLLY (Matt 2026-07-02, §7.1)** | *(ratified text preserved for lineage)* defensive types only: Bodyguard / Terrain Anchor / Warcry-Buff Spirit | role inversion: Bodyguard → Sacrificial (consume for 150% remaining-HP burst); Terrain Anchor → Damage Amp Zone (+40%, 8s); Warcry → Reverse-Buff | *(deferred)* |
| **PROXY_CONVERGENCE** | exactly 2 distinct Tier-1 types, cross-family | the two merge into one Convergent Proxy (HP = avg × 1.2; damage = sum × 0.8; per-pair merge rules, e.g. Fighter+Anchor → Fighting Anchor) | two servants fuse into one |
| **DUAL_PROXY** | exactly 1 Tier-1 type; ≥3 chains | unlocks a second COMPLEMENTARY type from a per-primary compatibility pool; both operate independently (no convergence) | a second, different servant answers |

**Magnitude status:** every number above is **PROVISIONAL by ratification** (the decisions-log status line
says so explicitly) and predates the spatial sim + D3 calibration. gamora certifies each against the
D3-certified scaffold — math-note-first (Disc #18), single-parameter-isolated sweeps (Disc #24), fresh seeds
53M+, boss anchor FIXED per the D3 harness pattern.

**Multi-slot rule (ratified, Session-1 §2.2):** no two proxy-family strategies on one kit *unless* the pair
is DUAL_PROXY + one other proxy-family member. **Proxies do not summon proxies** (Matt-ruled 2026-06-12);
FISSION's death-split is the sole bounded exception (replication-on-death, not autonomous summoning).

## 3. v1-family retirement map (the S1–S6 drafted earlier this session)

| v1 member (RETIRED) | Disposition |
|---|---|
| S1 ProxyDamageAmplification | **SPLIT:** flat proxy-damage% is the **Set-#6 gear capstone's lane** (Clause B inheritance + set bonuses; `proxy_commander.py:59-70` calibrated layer); *behavioral* output-raising at T4 = ASCENSION / SOVEREIGNTY |
| S2 ProxyBulwark | **RETIRED:** "guardian holds the line" is the **Bodyguard taxonomy TYPE** (Session-2 Tier-1 catalog) — a proxy type, not a T4 |
| S3 ProxyLegion | **RETIRED as T4:** more-bodies = FISSION (death-multiplication) at demo, DUAL_PROXY phase 2; the raw `max_active`/count lever stays a **decl/calibration surface** (D3: count 1→2 halves clear time — certified scaffold territory, not capstone territory) |
| S4 ProxySurge | **RETIRED:** spawn-cadence / attack-interval are Set-#6 set-bonus + decl-field territory — gear and calibration layers, not a T4 strategy |
| S5 ProxyDeathConversion | **RETIRED:** FISSION **is** the ratified on-death conversion (the corpse-burst variant ≈ INVERSION's Sacrificial consume, itself now deferred) |
| S6 ProxySpawn-revived | **RETIRED as T4:** the Session-2 three-tier table rules non-summoner proxy acquisition = *"summon-first allocation OR low-probability trait"* (generation paths); the name's register entry retired with the §6 ruling |

**What v1 contributes forward:** the §1 problem statement + W2/D3 evidence; the η/emission integration
intent (§4); the boundary rulings (§5); the acceptance criteria (§8). Root cause of the drift is logged
here: SPEC-AUTHOR skipped the design-corpus sweep the framing-audit checklist (OP §4.1 Q2) mandates — the
Set-#6 spec cited in v1 says "proxy chain-T4" verbatim and should have triggered it.

**Rework note (B1-rebase):** rocket's Phase-1 commit (`17d5f80`) built the v1 S1–S6 classes + improvised
revival classes for the retired register; gamora's Phase 2 (`02d7cd5`) certified against them. Both retire
in the rebase. The A3 differentiation METHOD is proven and carries forward; it re-runs on ratified members.

## 4. η / emission integration intent (which capstone does THIS summoner draw)

The existing architecture carries everything needed: `η = 0.50·axis_match + W_THEMATIC·thematic +
W_SIM_VIABILITY·sim_viability`, floor 0.35, highest-η commits (`mechanic_alteration.py:338` pattern).

1. **Hard eligibility = the RATIFIED per-member gates (§2)**, implemented in each `opportunity_scan()` →
   0.0 outside eligibility. A non-summoner can never draw a proxy capstone — the mirror image of today's bug.
2. **axis_match keys off DECL SHAPE** within the eligible set — Matt's doubt answered structurally first
   (mid/full-HP bodies → FISSION; any mechanical type → ASCENSION; exactly-2 cross-family types →
   CONVERGENCE; 1-type ≥3-chain kits → DUAL_PROXY, with SOVEREIGNTY in range for Fighter/Golem non-mana
   kits), then by rank: count-N minimal bodies → ASCENSION lean · count-1 full body → FISSION/SOVEREIGNTY
   lean. **Coverage note (INVERSION deferred):** defensive-type kits retain ASCENSION + DUAL_PROXY
   (Bodyguard additionally FISSION) — no eligible-kit class is left with zero family members (asserted, A6).
3. **thematic** follows the element-resonance pattern (blood-magic precedent `:325-334`): shadow/earth
   resonate for FISSION (grave imagery); neutral ~0.05–0.20 elsewhere.
4. **sim_viability → 1.0 on activation** — the `sim_prerequisite` mechanism retires with the register (§6);
   activated members carry None.
5. **Emission bands (measured, not forced):** proxy-heavy kits emit a proxy-family `primary_t4` at **≥90%**;
   proxy-light at **≥60%** (the hybrid caster fantasy legitimately lets self-cast T4s compete there).
   Self-cast T4s stay in `t4_candidates` for summoners — outcompeted at scan-time by design, not banned.
6. **Manifestation ladder holds** (`_manifestation_from_tier`): continuous axes scale down at rank2/rank3;
   FISSION and DUAL_PROXY integer/entity axes are **T4_active-only** (η=0 below tier 3).

## 5. Interaction rulings

- **R1 — Bridge-state no-propagation:** DDA is **retired by ruling Q3** in the v2 catalog but LIVE in the
  execution layer; while it remains live, it does NOT touch proxy damage — player-primary and proxy
  amplification stay separate surfaces. The **sanctioned cross-surface path is Set-#6 Clause B**
  (gear-layer inheritance). gamora asserts separation in tests.
- **R2 — Decl-surface only:** T4 levers write per-kit decl/behavioral fields; bridge module constants
  (`:68/:77/:232/:255`) stay untouched DEFAULTS; the Set-#6 calibrated contribution constants
  (`proxy_commander.py:59-70`) are a hard boundary — T4 multiplies on top of the certified scaffold.
- **R3 — One `primary_t4` per kit** (existing rule holds); the ratified multi-slot family rule (§2) governs
  multi-chain slots; family members enter `t4_candidates` alongside self-cast strategies.
- **R4 — Entity-count integrity:** FISSION hard-caps at 4 (ratified); `max_active` ceiling stays 3 (the
  D3-tested max) until gamora certifies higher; the count-wall lever remains decl/calibration territory (§3 S3).
- **R5 — Solo invariance:** the eligibility gates structurally guarantee zero effect on solo-bin kits;
  asserted anyway (A6).

## 6. Dormant register — ⚖ RULED 2026-07-02: RETIRED (five names)

**Provenance (verified in git, closed the question):** the five names — ResourceBuffer, MechanicReplacement,
ZoneControl, ConditionalModifier, ProxySpawn — are the **below-the-cut tail of a scored candidate shortlist**
(`f9762a8` legolas Mode-A algorithm-§8 methodology consult, 2026-05-25). The registry commit (`d6bca67`,
same day) implemented the top six as real classes and parked the remainder as ONE DOCSTRING LINE
(*"v1.1 deferred (sim-extension-required): …"*). **They were never designed** — no mechanics, no magnitudes,
no eligibility, zero canonical-doc presence — and were **not carried into the ratified catalog-v2** (Session-1,
2026-06-12, which also retired DDA with no-grandfathering). What followed was **register-by-accretion**: the
docstring line got cited by the deferral audit → the engine tracker → the no-deferral directive, until a
shortlist tail had become a ruling noun. (The vestigial-ontology pattern; flagged for jack-ryan as a
disciplines datapoint.)

**Ruling (Matt 2026-07-02):** the five-name register is **RETIRED**. The B1-rebase removes the four
improvised revival classes (`17d5f80`) and the `:45-46` docstring line; lineage preserved in the commit
message and this section. The 2026-07-02 "dormant capstones alive" mandate is **satisfied by activating the
ratified catalog** — there was never designed content behind the names. ProxySpawn's *capability*
(non-summoners can gain a proxy) is owned by the Session-2 generation paths (low-probability trait;
summon-first allocation) and DUAL_PROXY.

### 6.1 ZONE_CONTROL — newly DESIGNED catalog member (Matt-ruled 2026-07-02)

The one fantasy from the retired list with **no catalog-v2 owner and real genre precedent** enters as the
**26th catalog member through the ratified register** (`t4_catalog_v2.py` constant + family map). The NAME
survives; the register entry is new — this section is its design authority, superseding rocket's improvised
revival class (code salvage permitted where it matches this design).

- **Family:** COMBAT (lean — jack-ryan Gate-1 confirms; see conflict check below).
- **Fantasy:** the battlefield itself becomes the weapon — persistent area-denial. Genre precedent: D2
  Bone Wall/Prison build identity; PoE totem-zone control archetypes; Grim Dawn ground-effect devotions.
- **Eligibility:** the kit's dominant surface is control/AoE — gate derived from bc axes (control
  orientation OR AoE-geometry dominance), mirroring GEOMETRY_COLLAPSE's dominance-gate pattern; rocket
  derives the exact threshold in the dispatch.
- **Capstone mechanic (decl-level intent):** T4 anchors ONE persistent zone at the kit's control/AoE cast
  signature. Enemies inside suffer the kit's signature control effect continuously (element-appropriate
  slow/root/ailment) and the kit's damage against zone-standing enemies is amplified — **start modest**
  (the doc-47 Phase-4 DDA lesson). Zone lifetime/radius parameterized; no zone stacking.
- **Sim surfaces:** the original "sim-extension-required" blocker is BUILT — positional grid exists;
  AoeCastEvent producer just dispatched. The zone binds to those surfaces; gamora validates the binding.
- **Acceptance intent:** measurable build-floor delta on control-heavy fixtures (the boss must fight
  *through* the zone); zero effect on non-eligible kits; magnitudes gamora-owned, math-note-first.
- **Conflict check (Gate-1 item):** ZONE_CONTROL and GEOMETRY_COLLAPSE both reward AoE dominance — Gate-1
  rules whether COMBAT needs a max-1 multi-slot rule (Session-1 §2.2 currently restricts only ELEMENT and
  DEFENSE) and confirms family assignment.

## 7. Demo family — ⚖ RULED 2026-07-02: five members, two-phase activation

**Matt's ruling supersedes the v2 §7 lean:** *all* ratified members ship for the demo **except INVERSION**
(§7.1). Activation is two-phase because CONVERGENCE and DUAL_PROXY consume design artifacts that do not yet
exist as live canon:

- **Phase 1 (matrix-independent):** ASCENSION + SOVEREIGNTY + FISSION — plus ZONE_CONTROL (§6.1) riding the
  same dispatch.
- **Phase 2 (behind gandalf artifacts):** CONVERGENCE + DUAL_PROXY. The Q6 pair-matrix and Q7 compatibility
  pools are **gandalf-owed next artifacts**, authored per the ratified process (offline drafting + Legolas
  Mode-A genre pull; **Matt reviews exception rows only**). Their sequencing gate (proxy-primary empirical)
  resolved its kernel sub-question 2026-06-12 (`proxy_contribution_pct` 0.556, cheap branch); the
  corpus-population sub-question validates on the B4 emission run's telemetry.
- **Phase-1 prerequisite check (named, not silent):** CONVERGENCE requires kits with exactly two
  cross-family proxy types — rocket confirms generation can EMIT 2-type decls, or files it as a named
  prerequisite on phase 2.

### 7.1 PROXY_INVERSION — ⚖ DEFERRED WHOLLY (Matt 2026-07-02; named disposition)

**Matt's design finding (session verbatim, paraphrase-anchored):** a proxy kit is built around the proxy —
mostly ailments/buffs, timing out on the boss without proxy DPS; post-inversion, *"a bit of burst damage and
HP won't make the kit viable as a (now) non-proxy."* Sharpened in review: the Sacrificial leg is also
**timing-degenerate** — 150% of *remaining* HP pays maximum at full HP, so the optimal play is
consume-at-fight-open (you built a Bodyguard kit in order to never use the Bodyguard).

- **Disposition:** the catalog constant STANDS (ratified membership; lineage); the execution layer carries a
  **deferred-by-ruling exclusion** — η never offers INVERSION (no kit may draw a dead or degenerate
  capstone). rocket implements the exclusion with a ruling-cite comment, not a bare skip.
- **Named re-entry criterion:** the **INVERSION-v2 kit-level redesign** — consume the proxy → its
  D3-calibrated contribution **transfers into the caster's skills** as persistent amplification
  (conservation across the inversion; timing degeneracy dies because the transfer rides *base* contribution,
  not remaining HP). Requires its own design amendment + math note + gamora calibration. No demo or launch
  commitment attached; re-engages when Matt calls it.

## 8. Acceptance criteria (testable; Gate-1 checks against these)

- **A1 — Emission:** post-un-gate demo emission run — every proxy-bin kit carries ≥1 family member in
  `t4_candidates`; `primary_t4` family-share meets the §4.5 bands (≥90% heavy / ≥60% light).
- **A2 — Sim delta:** each ACTIVATED member applied to a certified fixture produces a measurable build-floor
  delta vs no-T4 baseline in its axis direction (ZONE_CONTROL on control-heavy fixtures per §6.1). No
  member makes caster-alone viable — the T4 amplifies the proxy contribution, not the body.
- **A3 — Differentiation (THE Matt-doubt test):** the two D3-certified fixtures draw **different** top
  family members via gates + axis_match. If both draw the same top member, under-differentiated — rework
  before ship. (Method proven in the pre-rebase run; re-certify on ratified members.)
- **A4 — Legibility:** each activated member's on-screen read (§2, last column) is distinct enough to name
  in one clause — feeds D5 verb realization and the galadriel benchmark later.
- **A5 — Boundaries asserted:** R1 (bridge-state no-propagation; Set-#6 Clause B is the only sanctioned
  cross-surface) + R2 (calibrated layer untouched) have explicit test assertions.
- **A6 — Rulings enforced:** register retirement executed (revival classes + docstring line REMOVED);
  INVERSION exclusion asserted (no kit draws it); solo-bin zero-effect asserted; no eligible-kit class left
  with zero family members (§4.2 coverage note).

## 9. Ruling log (this spec's Matt-plate items — ALL RESOLVED 2026-07-02)

- **(a) Register binding → RULED:** five-name register RETIRED (§6); ZONE_CONTROL enters newly designed (§6.1).
- **(b) Demo subset → RULED:** all ratified members demo-critical except INVERSION; two-phase per §7.
- **(c) INVERSION depth → RULED:** deferred wholly; kit-level INVERSION-v2 is the named re-entry (§7.1).

## 10. What this spec does NOT own

Final magnitudes (gamora — certification of the PROVISIONAL ratified numbers, Disc #18/#24, seeds 53M+) ·
implementation architecture and strategy-class code (rocket) · grading thresholds (gamora) · T4 flavor
naming/narration (phase-5 pass) · the Q6/Q7 artifacts' CONTENT (gandalf-owed, separate deliverable) · the
INVERSION-v2 redesign (parked, §7.1) · the ranged-proxy NAV question (PART E fork — D3 confirmed a decl
`count` raise is a content-level mitigation).

**Signed:** gandalf, 2026-07-02 — v1 same-day; v2 re-base after Matt's prior-art catch; v3 rulings-fold.
**The B1-rebase fires against THIS version.**
