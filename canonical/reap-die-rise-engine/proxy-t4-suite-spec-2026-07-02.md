# Proxy-T4 Suite — Design Spec (dormant-T4 revival + the proxy-focused capstone family)

> **STATUS:** CANONICAL DESIGN SPEC — feeds Lane B1 (rocket: strategies · gamora: sim-eval + magnitudes).
> **Mandate (Matt-ruled 2026-07-02, verbatim):** *"Summon-focused kits MUST have a proxy-focused T4… we are
> expecting summon-kits to time out or die to boss if not for their proxy's DPS… will only one T4 work for
> all Proxies? I'm doubtful… We need to make all of the dormant T4 capstones alive in the engine (including
> proxyspawn) and we also need a full suite of proxy-T4's for the demo, so decent proxy kits can be emitted
> for selection."*
> **Author:** gandalf (SPEC-AUTHOR), 2026-07-02.
> **Denominators:** `one-realm-mvp-scope.md` §5 ask 4 · serial-emission ledger D.1 #9 (this spec is the gate on both).
> **Evidence base (verified first-hand):** `mechanic_alteration.py` (η architecture :65/:69/:338; ABC :255;
> v1.1-deferred list :45-46; `sim_prerequisite` :266-271) · `proxy_vocabulary_bridge.py` (four scaffold levers
> :68/:77/:232/:255) · gamora D3 cert (`gamora/v-proxy-fight-calibration-1` @ `abb010d`; AGENT_STATE 2026-07-02) ·
> W2 spike (army WR 1.000 vs caster-alone 0.000).

---

## 1. The design problem

Every live T4 strategy amplifies **the caster's own body** (DirectDamageAmplification: 1.75× at
preferred-encounter, 1.0× elsewhere — `mechanic_alteration.py:664`). W2 measured a summoner's body at
**WR 0.000 caster-alone**; the proxies carry 100% of the kill. A summon-bearing kit drawn under the current
T4 set receives a capstone that multiplies its *smallest* contribution surface — mechanically dead weight,
and a broken class fantasy at the exact moment (capstone unlock) the genre promises the fantasy's peak.

Genre confirms the fix is a **family, not a node**: PoE's Necromancer ascendancy is four distinct minion
notables (offense / defense / on-death / hybrid); D2 ran Skeleton Mastery as a separate investment axis from
raise-count; Last Epoch splits minion-damage from minion-count passives. Matt's doubt — *"will only one T4
work for all Proxies?"* — is answered mechanically in §4: **different decl shapes draw different family
members** via axis-match, so the count-2 horde caller and the count-1 bruiser binder surface different
capstones from the same suite.

## 2. The family — six members

Five summoner-conditional strategies + one crossing strategy (the revived `ProxySpawn`). Mechanical names
follow the existing strategy register; flavor naming rides the phase-5 T4 narration pass
(`phase-5-t4-narration-amendment-2026-05-26.md`), NOT this spec.

| # | Strategy | Fantasy | Mechanical lever (decl-level) | Magnitude shape (intent — gamora owns numbers) | On-screen read (feeds D5) |
|---|---|---|---|---|---|
| S1 | **ProxyDamageAmplification** | the commander whose legion hits harder | per-decl `damage_multiplier` (bridge default 1.0 @ `:232`) | DDA mirror: **conditional ~1.75×** on proxy damage at preferred-encounter, 1.0× elsewhere — same shape, same reference power | same bodies, visibly faster kills |
| S2 | **ProxyBulwark** | the binder whose guardian holds the line | per-decl HP (from `PROXY_REFERENCE_HP` 20000 @ `:68`) + taunt-stance weight | HP ×2.0–3.0 band + aggro amplification; converts kill-speed into survival margin — the build-floor SURVIVE half | ONE conspicuously unkillable wall |
| S3 | **ProxyLegion** | the horde caller | `proxy_max_active` (+N) **AND count floor** `count = max(count, new_max_active)` | +1 (proxy-light) / +2 (proxy-heavy); **empirically the strongest lever** — D3: max_active 1→2 halves clear-time (60→30 s), linear boss-DPS, saturates at decl `count` (hence the count-floor rule) | MORE BODIES — the strongest legibility axis |
| S4 | **ProxySurge** | the relentless tide / grave-engine | per-decl `spawn_cadence_s` + per-decl attack-interval override (default 1.0 s @ `:255`) | ~30–40% cadence reduction; value scales with proxy lethality of the encounter (re-raise dead-time is the tax it removes) | the line replenishes visibly faster; strikes drum quicker |
| S5 | **ProxyDeathConversion** | death feeds death — the *Reap. Die. Rise.* keystone made mechanical | NEW on-proxy-death hook (death event EXISTS — W2 `hp<=0` flip; trigger plumbing is the cost) → corpse-burst AoE at proxy position OR empowered instant re-raise | burst ≈ N seconds of proxy DPS per death (gamora bands N) | corpses detonate / the fallen rise again instantly |
| S6 | **ProxySpawn** (revived, re-scoped) | anyone may bargain with death for one servant; the necromancer commands legions | grants ONE lesser bound proxy to kits **without** native summons | single proxy at sub-summoner magnitudes (e.g. 0.5× damage_multiplier band) | a non-summoner suddenly has a companion |

**S6 eligibility inversion (overlap resolution):** `ProxySpawn` is eligible ONLY for kits with empty proxy
decls; the S1–S5 family is eligible ONLY for kits with non-empty decls. No member competes with another for
the wrong kit. S6 is the *breadth* member — the demo roster may or may not curate one; its demo-critical
obligation is only to be ALIVE (Matt's "including proxyspawn").

**Named descope valve:** if B1 must cut to hold the wave, **S5 is the cut** (only member needing new trigger
plumbing) — defers to launch, the other five stand. KR has this relief valve explicitly.

## 3. Tier-awareness — a 10-cell intent table, not a per-type explosion

Magnitudes are **functions of (proxy bin × strategy), parameterized by decl fields** (count, body tier,
cadence) — never enumerated per `proxy_type`. `PROXY_TIER_MAX_ACTIVE` is already body-tier-keyed
({minimal:3, mid:2, full:1} — D3 certified-HOLD); the suite reads those surfaces, it does not fork on them.

| Strategy | proxy-light (few/hybrid caster) | proxy-heavy (many/dedicated) |
|---|---|---|
| S1 DamageAmp | ~1.75× (proxy damage is *part* of output) | ~1.5× (total-output parity — count already multiplies) |
| S2 Bulwark | HP ×3.0 (one guardian must WALL) | HP ×2.0 (redundancy already defends) |
| S3 Legion | +1 (relatively 2× on count-1 — strongest single cell; gamora may trade cadence against it) | +2 |
| S4 Surge | −30% cadence/interval | −40% (churn is the identity) |
| S5 DeathConv | burst ≈ 4 s proxy-DPS | burst ≈ 2 s (deaths are frequent) |

Starting bands only — **gamora owns final numbers** via math-note-first (Disc #18), single-parameter-isolated
sweeps (Disc #24), fresh seed range 53M+ (D3 consumed 52M), boss anchor FIXED per the D3 harness pattern.

## 4. η integration intent (the "which capstone does THIS summoner draw" mechanism)

The existing architecture carries everything needed: `η = 0.50·axis_match + W_THEMATIC·thematic +
W_SIM_VIABILITY·sim_viability`, floor 0.35, highest-η commits (`mechanic_alteration.py:338` pattern).

1. **Hard eligibility gate:** S1–S5 `opportunity_scan()` returns **0.0** for kits with empty proxy decls
   (the existing "definitively not applicable" convention); S6 inverts. A non-summoner can never draw a
   dead proxy capstone — the mirror image of today's bug.
2. **axis_match keys off DECL SHAPE** — this answers Matt's doubt mechanically:
   `count > max_active` headroom → S3 high · count==1 + full body → S2/S1 high · long cadence → S4 high ·
   high-lethality encounter preference → S5 high. The two D3-certified fixtures MUST rank differently (§7 A3).
3. **thematic** follows the existing element-resonance pattern (blood-magic precedent `:325-334`):
   shadow/earth resonate for S5 (grave imagery); neutral ~0.05–0.20 elsewhere.
4. **sim_viability → 1.0 on revival** — the `sim_prerequisite` strings (`:266-271`) are the dormancy
   mechanism; clearing them per §6 IS the revival.
5. **Selection-outcome intent (measured, not forced):** proxy-heavy kits emit with a proxy-family
   `primary_t4` at **≥90%**; proxy-light at **≥60%** (the hybrid caster fantasy legitimately lets self-cast
   T4s compete there). Self-cast T4s stay in `t4_candidates` for summoners — build diversity, outcompeted at
   scan-time by design, not banned.
6. **Manifestation ladder holds** (`_manifestation_from_tier`): continuous axes (S1/S2/S4/S5) scale down
   linearly at rank2/rank3 passive manifestations; **S3's integer axis is T4_active-only** (η=0 below
   tier 3 — a half-skeleton is not a thing).

## 5. Interaction rulings

- **R1 — NO propagation:** `DirectDamageAmplification` does NOT touch proxy damage; player-primary and
  proxy amplification are **separate surfaces by design** (closes the serial-emission PART E open question
  at the design layer). Rationale: propagation would strictly dominate every family member and erase the
  build fork. gamora asserts separation in tests.
- **R2 — Decl-surface only:** T4 levers write **per-kit decl fields**; the bridge module constants
  (`:68/:77/:232/:255`) stay untouched DEFAULTS, and the **Set-#6 calibrated contribution constants
  (`proxy_commander.py:59-70`) are a hard boundary** — the T4 layer multiplies on top of the certified
  scaffold, never edits the calibrated layer.
- **R3 — One `primary_t4` per kit** (existing rule holds); family members enter `t4_candidates` alongside
  self-cast strategies.
- **R4 — Count-wall integrity:** S3 raises `max_active` and the count floor together (D3: saturation at
  decl `count` makes a lone max_active raise a no-op); ceiling = 3 (the D3-tested max) until gamora
  certifies higher.
- **R5 — G-SOLO invariance for the family:** S1–S5 produce ZERO effect on solo-bin kits (gate in R1 of §4).
  The dormant-four's effects on solo kits are the *intended* change, validated per-strategy (§6).

## 6. Dormant-five revival dispositions (design intent; rocket+gamora own per-strategy feasibility)

The v1.1 "sim-extension-required" labels **predate the spatial sim** — assess each against what NOW exists:

| Strategy | Design intent stands as authored? | Likely post-spatial mapping |
|---|---|---|
| **ProxySpawn** | RE-SCOPED → §2 S6 (non-summoner crossing member) | W1/W2 spawn+allegiance mechanics ARE the extension it named — likely cheapest revival |
| **ZoneControl** | yes | positional grid + AoE event surface exist (AoeCastEvent producer just dispatched) — assess against it |
| **ConditionalModifier** | yes | trigger plumbing exists sim-side; per-trigger audit |
| **ResourceBuffer** | yes | energy system exists; probable loadout-resolution-only now |
| **MechanicReplacement** | yes | decl/mechanic surfaces exist; audit the specific replacements it names |

Each revival clears or re-names its `sim_prerequisite` string with a one-line justification in the rocket
change; any member whose prerequisite genuinely still doesn't exist gets a NAMED residual (not a silent
re-defer — Disc: no deferral-as-disposition).

## 7. Acceptance criteria (testable; Gate-1 checks against these)

- **A1 — Emission:** post-un-gate demo emission run — every proxy-bin kit carries ≥1 family member in
  `t4_candidates`; `primary_t4` family-share meets the §4.5 bands (≥90% heavy / ≥60% light).
- **A2 — Sim delta:** each of S1–S4 applied to a D3-certified fixture produces a measurable build-floor
  delta vs no-T4 baseline in its axis direction (kill-time ↓ for S1/S3/S4; survival margin ↑ for S2). No
  member makes caster-alone viable — the T4 amplifies the proxy contribution, not the body.
- **A3 — Differentiation (THE Matt-doubt test):** on the two certified fixtures, η ranks **different** family
  members top (bone-acolyte count-2 → S3/S4 lean; crypt-lieutenant count-1 full-body → S2/S1 lean). If both
  draw the same top member, axis_match is under-differentiated — rework before ship.
- **A4 — Legibility:** each member's on-screen read (§2 table, last column) is distinct enough to name in
  one clause — feeds D5 verb realization and the galadriel benchmark later.
- **A5 — Boundaries asserted:** R1 (no DDA propagation) + R2 (Set-#6 untouched) have explicit test assertions.
- **A6 — Solo invariance:** S1–S5 zero-effect on solo-bin kits, asserted; dormant-four solo effects
  validated per-strategy as intended changes.

## 8. What this spec does NOT own

Final magnitudes (gamora — math-note-first, Disc #18/#24, seeds 53M+) · implementation architecture and
strategy-class code (rocket) · grading thresholds (gamora) · T4 flavor naming/narration (phase-5 pass) ·
the ranged-proxy NAV question (separate PART E fork — though note D3 confirmed a decl `count` raise
delivers a content-level mitigation: count=2 → 31000 delivered → boss dead).

**Signed:** gandalf, 2026-07-02. Suite design per Matt's proxy-T4 ruling; B1 may fire against this spec.
