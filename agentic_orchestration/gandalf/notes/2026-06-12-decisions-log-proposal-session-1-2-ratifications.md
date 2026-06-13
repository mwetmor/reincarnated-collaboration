# Decisions-Log Entry Proposal — Session 1 + Session 2 § 3 Ratifications (2026-06-12)

**Author:** gandalf (proposer)
**Routed to:** jack-ryan (decisions-log canonical writer) — Matt-directed routing 2026-06-12 ("route the decisions-log proposal to jack-ryan")
**Approval state:** ALL items below are Matt-RATIFIED 2026-06-12 (verbatim: "I like them all. approved" — Session 1 batch; "Confirmed - ratify with all three riders" — Session 2 § 3). This proposal is a capture request, not an approval request.
**Target:** `~/Games/reincarnated-engine/design/decisions/decisions-log.md`

Jack-ryan: entry format, granularity (one omnibus entry vs. several), and cross-reference style are your call. Anchors per item below. Flag back to gandalf if any item's framing looks inconsistent with prior log entries.

---

## Proposed entries

### 1. Session 1 Q1–Q10 rulings (T4 architecture locks)

- **Q1** DEFENSIVE_TRADEOFF mana shield: 50% absorption split; 5 non-immune elements only; spill-to-HP at depletion; always-on; 1:1 mana-per-damage drain, gear-scalable
- **Q2** chain count = generation parameter from {2, 3}; 4-chain row is architecture headroom, not generated
- **Q3** DDA retirement migration: Season 001010 corpus re-evaluated against new catalog, no grandfathering
- **Q4** GEOMETRY_COLLAPSE locked: non-dominant-bin skills convert to dominant bin + 1.4× on converted; no secondary collapse
- **Q5** RESOURCE_CONVERSION locked: all energy types eligible; produces damage; competitive-not-superior ratio vs direct spend
- **Q6/Q7/Q8** process rulings: principles-then-offline-matrices; Q6/Q7 sequenced AFTER proxy-primary empirical gate; Q8 variant-agnostic
- **Q9** charge-stack hold-vs-spend: spend-all + passive per-stack bonus while held; hold-vs-spend becomes a generation parameter (zero lock amendment); un-held gamora Item 4 + rocket Item 10
- **Q10** faction coverage: redraw 8 factions so all 14 lineages have a home; ONE composite ninth only if redraw can't absorb cleanly

**Anchor:** `agentic_orchestration/gandalf/notes/2026-06-12-session-1-rulings-q1-q10-t4-catalog-expansion.md` § 1

### 2. T4 catalog expansion 21 → 25 strategies

Four additions filling the gaps found by the T4-vs-hypothesis cross-matrix audit (root cause: burst-biased catalog — "exciting" answered 21 ways, "enduring" zero):

- **GEOMETRY_PROPAGATION** (`geometry_propagation_cascade` / `geometry_propagation_overkill`) — GEOMETRY family; Matt-originated perpendicular-to-collapse seat
- **RETRIBUTION_ENGINE** — DEFENSE family; fills dead Axis 5 damage-taken-converts bin
- **PERSISTENCE_ENGINE** (`persistence_uptime` / `persistence_saturation`) — COMBAT family; fills missing sustained/even-tempo champion
- **PHASE_MOMENTUM** — DEFENSE family; fills empty dodger shelf

All magnitudes PROVISIONAL (config, not constants). DEFENSE max-1 rule carries unchanged at 4 strategies.

**Anchor:** ruling record §§ 2, 2.5, 2.6

### 3. Validation amendments (Session 5)

- Test 3 dodger divergence criterion (avoidance-event telemetry; non-circular) — dodger bin was previously invisible to validation
- Test 5 three-way comparison (HIGH-with-RESONANCE_LOOP / HIGH-without / LOW) — de-confounds complexity penalty from single-strategy tuning
- Flag 4 generation prior (rocket Item 11): HIGH cognitive-load bin ≥ ~8% of in-band corpus, ≤ 50% carrying RESONANCE_LOOP

**Anchor:** ruling record § 3; Session 5 spec § 5 (amended in-place)

### 4. Proxies-of-proxies ruling

NO — proxy entities do not summon their own proxies. PROXY_FISSION death-split is the sole bounded exception (recursion cap 4 total entities, 30s expiry, kernel-enforced). `"summon"` struck from ProxyThresholdEvent (Session 2 § 3 rider 1).

**Anchor:** ruling record § 4; Session 2 spec § 3 ratification stamp

### 5. Proxy-primary architecture charter (RECOGNITION — commitment deferred)

Canonical ARPG trichotomy (physical / caster / proxy-summoner) chartered as a candidate fourth kit-architecture type. Commitment gated on empirical evidence: gamora Items 1+2 smoke population + `proxy_contribution_pct` ~0.5 reachability check. Do-not-generate guard recorded at Session 4 § 1.1. This entry should capture the GATE, not an architecture commitment.

**Anchor:** `agentic_orchestration/gandalf/notes/2026-06-12-proxy-primary-architecture-recognition.md` (esp. § 5)

### 6. Session 2 § 3 ratification + dispatch firings

- ProxyCombatant interface ratified with three riders (summon-strike; fission bounds as kernel-enforced interface fields; proxy-stacked smoke composition)
- Gamora kernel handoff FIRED (all 5 items); rocket generation handoff FIRED (all 11 items)
- Design-latitude grants recorded in both dispatches: latitude covers HOW, not WHAT; intent-changing calls surface to gandalf pre-implementation; latitude calls recorded at Gate-2

**Anchors:** Session 2 spec § 3 stamp; `dispatches/2026-06-12-gamora-proxy-kernel-handoff.md` + `dispatches/2026-06-12-rocket-generation-handoff.md` STATUS blocks

### 7. Axis 2A deferral retirement (lock-doc consequence)

The BC axes lock marked Axis 2A (Proxy Density) ALWAYS sim-deferred because the sim was solo-only. The ProxyCombatant kernel extension retires that deferral — Axis 2A becomes measurable. Recorded as a lock-doc CONSEQUENCE at Session 2 ratification, NOT an amendment to any locked bin.

**Anchor:** Session 2 spec normalization-pass note ¶ 3; `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` § 3

---

**Commit trail:** `b1e498e` (Session 1 ratification batch), `689fcbe` (Session 2 § 3 + riders, gamora fired), `9bb78f1` (rocket fired + latitude grant) — all pushed to origin/main.

*Sign-off: gandalf, 2026-06-12.*
