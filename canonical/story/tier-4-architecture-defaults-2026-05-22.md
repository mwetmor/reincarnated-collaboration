# Tier 4 Architecture Defaults — T4-A Design Pass

> **STATUS:** CURRENT (load-bearing as of 2026-05-23) — see `canonical/00-ground-state.md`

**Date:** 2026-05-22
**Author:** gandalf (story-and-design steward; senior designer)
**Status:** v1 defaults adopted under Matt 2026-05-22 pre-authorization C; open questions surface for next design call
**Authority:** Matt 2026-05-22 — pre-authorization C (gandalf adopts the BDI § 6 proposed default architecture)
**Companions:**
- `canonical/story/build-defining-resonance-formula-2026-05-21.md` § 6 — Tier 4 as rank-completer (theoretical foundation)
- `canonical/story/multi-dim-convergence-algorithm-2026-05-21.md` v1.1 § 3.4 — Tier 4 mechanic-altering semantics
- `canonical/story/p5-cohesion-judge-prompt-priorities-2026-05-21.md` § 2 — capstone identity alignment context
- `canonical/story/gear-as-substrate-2026-05-21.md` § 0.5.6 — LITE path (gear-anchored capstone enabled)
- `canonical/story/gear-archetype-rule-table-v1-2026-05-22.md` — G1-LITE rule table (signature_gear_archetype derived-tag)
- `canonical/story/bdi-omega-tau-tables-v1-2026-05-22.md` — BDI ω/τ tables (high-β substrate-pairs for rank-completion)
- `canonical/story/hive-mind-protocol-qd-engine-rebuild-2026-05-21.md` v1.3 § 5 — phase architecture (T4-A through T4-E)
- `agentic_orchestration/hive-mind-state-evening-2026-05-21.md` § 4.3 — open questions 11-14 (Tier 4 hierarchy / authorship / gear-anchoring / catalogue size)

---

## 0. TL;DR

T4-A adopts the BDI § 6 proposed default architecture for Tier 4 keystones as the V1 commitment, leaving four open questions for Matt's return when T4-B catalogue authorship opens:

| Default | Decision |
|---|---|
| **Hierarchy** | 1 signature capstone (rank-3 completer; gear-anchored when `signature_gear_archetype` present in kit context) + 1-3 secondary capstones (rank-2 modulators; identity-secondary) |
| **Authorship pattern** | Hand-authored catalogue v1 (gandalf + Matt for v1; rocket engine-integration). LLM-augmented variants deferred to v2+ |
| **Catalogue size** | ~30-50 keystones v1 (per-element ~4-7 signature + ~5-10 secondary; final number TBD per § 4.3 open question) |
| **Gear-anchoring** | Signature capstone IS gear-anchored when `signature_gear_archetype` is present in the kit's substrate vector (per gear-as-substrate LITE; derived-tag carries identity hint into capstone identity). Mechanical-degradation-without-gear deferred to v1.1/v2 |
| **Development phasing** | T4-A → T4-B → T4-C → T4-D → T4-E (see § 5) |
| **Open questions surfaced for Matt** | (a) catalogue-size precision (~30 vs ~50); (b) signature capstone breakthrough-moment framing for cross-element capstones; (c) hierarchy enforcement at convergence-time (engine treats all T4 same vs distinguishes signature from secondary at SP allocation); (d) skill_power_tier as authorship parameter (LC-011 recovery finding) |

These defaults DO NOT resolve the open questions autonomously — they LOCK the architectural commitments while surfacing the remaining design calls for next session.

---

## 1. Context

### 1.1 Theoretical foundation — Tier 4 as rank-completer

Per BDI § 6 (`canonical/story/build-defining-resonance-formula-2026-05-21.md`):

> A Tier 4 keystone is structurally a *rank-completer*. It takes a kit's rank-2 resonance and promotes it to rank-3 by adding the third leg.
>
> For a kit with substrate vector v and dominant pairwise resonance β_{ab}, the Tier 4 signature capstone introduces a third substrate component s_c (mechanically expressed via the keystone's regime-change) such that γ_{abc} > β_{ab}.
>
> The capstone IS the rank-3 closer. This is why capstones are mechanic-altering (regime-change) rather than scaling — they open a *new dimension of resonance*, not magnitude on an existing dimension.

This is the theoretical grounding for the T4-A architectural defaults. The architecture is NOT "Tier 4 = high-coefficient scaling reward" (the math note v1 pre-correction framing). The architecture IS "Tier 4 = rank-3 completer mechanic-altering keystone authored as the third leg of a known high-β substrate-pair."

### 1.2 Math note v1.1 Tier 4 framing

Per math note v1.1 § 3.4 (`canonical/story/multi-dim-convergence-algorithm-2026-05-21.md`):

- Tier 4 keystone selection is a **DISCRETE CATEGORICAL choice** per chain (pick which keystone if any is invested in this chain)
- Coefficient scaling 1.18-1.25 applies to ranks 1-15 WITHIN a chosen Tier 4 keystone — but the BUILD IDENTITY comes from WHICH keystone is chosen, not from rank investment alone
- Canonical Tier 4 examples (from legolas survey):
  - PoE *Blood Magic*: removes mana entirely, skills cost HP — fundamental resource model change
  - PoE *Resolute Technique*: 100% hit chance, no crits — accuracy/damage trade redefined
  - D3 *Tempest Rush — Run-and-Punch rune*: ground effect targets instead of self — geometry redefined
  - D4 *Lord of Hatred Diamond variant*: skill behavior transformation
  - Last Epoch *Fire Wall persistent variant*: temporal regime change

### 1.3 P5 cohesion-judge prompt priorities — capstone identity alignment

Per p5-prompt-priorities § 2 (`canonical/story/p5-cohesion-judge-prompt-priorities-2026-05-21.md`):

- Priority 2 — capstone identity alignment (the cohesion-judge prompt extensions need to distinguish between signature capstone identity and secondary capstone identity; the prompt must carry the BDI rank structure to align judge naming with kit's resonance)
- Future "breakthrough moment" framing for cross-element capstones (e.g., a fire kit's signature capstone might be a fire-water cross-element keystone like Steam-Wraith bridging the polar pair via volatility trait) — DEFERRED to T4-B authorship pass

### 1.4 Hive-mind state evening open questions (11-14)

Per `agentic_orchestration/hive-mind-state-evening-2026-05-21.md` § 4.3, four open questions surfaced 2026-05-21 evening:

- **Q11:** Hierarchy decision — 1 signature + 1-3 secondaries; vs all-defining; vs only-one-Tier-4
- **Q12:** Authorship pattern — hand-authored catalogue v1; LLM-augmented v2; or hybrid
- **Q13:** Gear-anchoring strength — mechanical-degradation-without-gear vs cosmetic-only
- **Q14:** Catalogue size — ~30-50; final number TBD

T4-A addresses Q11 + Q12 + Q14 with v1 defaults; Q13 is partially addressed (gear-anchored signature when signature_gear_archetype present; mechanical-degradation deferred); Q14 is partially addressed (~30-50 with precision deferred).

---

## 2. Hierarchy commitment — 1 signature + 1-3 secondary capstones

### 2.1 Default adoption

Per Q11 resolution (adopting BDI § 6.2 default per Matt pre-authorization C):

- **1 signature capstone** per kit — rank-3 completer; build-defining; the kit's identity centers on this keystone
- **1-3 secondary capstones** per kit — rank-2 modulators; identity-secondary; deepen primary resonance OR open auxiliary rank-2 resonances

### 2.2 Rationale

The signature carries identity. A kit's rank-3 resonance is the substrate-triple (s_a, s_b, s_c) whose γ-coefficient dominates any of its pairwise β. The signature capstone IS s_c — it is mechanically expressed via a regime-change that opens the third dimension of resonance.

Secondary capstones serve two roles:
1. **Deepen primary resonance** — additional Tier 4 keystones in the same substrate-pair's neighborhood (boost γ via auxiliary mechanic-altering effects that compound on the signature)
2. **Open auxiliary rank-2 resonances** — Tier 4 keystones in different chains that produce rank-2 β-pairs with substrate components not in the primary rank-3 triple (build depth without identity dilution)

The 1+1-3 hierarchy lets builds have **clear identity** (signature) WITH **build depth** (secondaries) WITHOUT dilution (multiple competing signatures would fragment the identity).

### 2.3 Genre canon alignment

- **PoE keystone clusters** typically have 1-2 "build-defining" keystones (Blood Magic, Mind over Matter, Vaal Pact, Iron Reflexes) with 2-4 auxiliary keystones in the cluster
- **D3 set 6-piece bonuses** are typically the signature; set 2/4-piece bonuses are secondary modulators
- **D4 Key Passives** are 1 per class build; Legendary Aspects are secondaries (gear-anchored secondaries — directly aligned with Reincarnated T4-D)
- **Last Epoch passive trees** have 1-2 capstone passives per tree with auxiliary nodes; mastery class adds a second signature layer

The 1+1-3 architecture is canon-aligned across the ARPG genre.

### 2.4 Hierarchy enforcement at convergence-time — open question

**OPEN QUESTION (Q-T4-A-1):** does the convergence engine TREAT all Tier 4 keystones the same at SP allocation OR DISTINGUISH signature from secondary at SP allocation?

Two candidate paths:
- **Path 1 (uniform treatment):** convergence treats all Tier 4 keystones identically; signature-vs-secondary distinction is cohesion-judge-side only (post-convergence naming layer)
- **Path 2 (hierarchical SP allocation):** convergence allocates more SP to signature capstone (e.g., 30-40 SP minimum) and less to secondaries (e.g., 5-15 SP each); the SP allocation enforces hierarchy at generation time

Path 1 is simpler engine-side; Path 2 is more identity-aligned. T4-A defers this resolution to Matt's next design call. FILED AS OPEN QUESTION for T4-B catalogue authorship.

---

## 3. Authorship pattern commitment — hand-authored catalogue v1

### 3.1 Default adoption

Per Q12 resolution (adopting hand-authored v1; LLM-augmented v2+ per Matt pre-authorization C):

- **Hand-authored catalogue v1** — gandalf + Matt design pass for v1; rocket engine-integration
- **LLM-augmented variants** — deferred to v2+
- **Hybrid pattern** — not adopted v1; revisit post-v1 catalogue ship

### 3.2 Rationale

Tier 4 keystones are **rank-3 completers** — each one is authored as the third leg of a known high-β substrate-pair (per BDI § 6.3 "Empirical implication: Tier 4 keystone catalogue authorship should explicitly target rank-3 completion. Each keystone in the catalogue should be designed as the third leg of a known high-β substrate-pair, producing a known rank-3 identity").

LLM-augmented variant generation at v1 risks:
- **Generic regime-change verbiage** without the genre-canonical resonance specificity (PoE keystones are valuable BECAUSE they're each a designed identity)
- **Catalogue dilution** — too many "kind-of-similar" keystones rather than each carrying a distinct identity
- **Naming-identity disconnection** — LLM names without designed-identity-correspondence

Hand-authored catalogue v1 ensures:
- Each keystone has a deliberate substrate-triple identity (rank-3 completer for a known pair)
- Each keystone's regime-change is mechanically specified + thematically anchored
- Catalogue size remains bounded (30-50) — manageable for design review + catalogue mastery by players

### 3.3 Authorship workflow (T4-B; P3-P4 territory)

T4-B catalogue authorship workflow (separate dispatch when T4-B opens):

1. **Identify rank-3 candidate identities** from BDI § 5.1 + § 5.2 + the BDI ω/τ tables v1 (`canonical/story/bdi-omega-tau-tables-v1-2026-05-22.md`) — each known high-β substrate-pair gets ≥1 rank-3 completer keystone
2. **For each candidate identity, author the regime-change mechanic** — what does the keystone DO mechanically? (PoE-style: "removes mana, skills cost HP" / "100% hit chance, no crits" / etc.)
3. **Per-element distribution** — each element should have ~4-7 signature keystones + ~5-10 secondaries (per § 4 catalogue-size commitment)
4. **Cross-element capstones** — some signature capstones bridge two elements (Steam-Wraith bridges fire+water via volatility trait); these are rare-tier and gated to specific substrate-vectors
5. **Sim-viability flag** per keystone — rocket verifies sim-viability before lock (parallels G1-LITE flag pattern)
6. **Gandalf + Matt design pass** — every keystone reviewed; catalogue locks at design call

LLM-augmented v2+ enables **per-season variant generation** of authored archetype keystones (e.g., the canonical Inferno-Knight signature gets a season-specific variant name + regime-change tweak based on substrate-vector specifics) WITHOUT changing the core catalogue.

---

## 4. Catalogue size commitment — ~30-50 keystones v1

### 4.1 Default adoption

Per Q14 resolution (adopting ~30-50; precision deferred to T4-B authorship per Matt pre-authorization C):

- **Range:** ~30-50 keystones v1
- **Per-element allocation (proposed):**
  - Each of 7 canonical elements gets ~4-7 signature keystones (~28-49 signature total)
  - Each element gets ~5-10 secondary keystones (~35-70 secondary; some overlap with signatures via cross-element)
  - Net: ~30-50 distinct keystones across catalogue (overlap via cross-element signature-secondary roles reduces double-counting)

### 4.2 Per-element allocation breakdown (proposed)

| Element | Signature target | Secondary target | Identity examples (per BDI § 5.1 + ω/τ v1) |
|---|---|---|---|
| fire | ~5 signatures | ~7 secondaries | Inferno-Knight, Pyromaniac, Forge-Champion, Phoenix-Reborn, Steam-Wraith (cross-element fire+water) |
| water | ~5 signatures | ~7 secondaries | Storm-Sentinel, Tide-Controller, Frost-Caller, Tide-Marksman, Boiling-Mage (cross-element with fire) |
| earth | ~5 signatures | ~7 secondaries | Crag-Crusher, Stoneshackle, Stone-Sage, Magma-Forge (cross-element with fire), Sandstorm-Strider (cross-element with wind) |
| wind | ~5 signatures | ~7 secondaries | Sky-Hunter, Cyclone-Strider, Wind Sentinel, War-Evangelist, Sandstorm-Strider (cross-element with earth) |
| lightning | ~5 signatures | ~7 secondaries | Stormcaller-Archmage, Storm-Chakram, Voltaic-Assassin, Stormking, Wrath-Bringer (cross-element with holy) |
| holy | ~5 signatures | ~7 secondaries | Templar-Smiter, Aegis-Priest, Exorcist, War-Priest, Holy Pirate Sniper / Powder Hex-Cannon (canonical surprising-pair per BDI § 5.1), Twilight-Judge (cross-element with shadow) |
| shadow | ~5 signatures | ~7 secondaries | Nightshroud, Smoke-Vampire, Necromancer, Voidpiercer, Twilight-Judge (cross-element with holy) |
| **Total v1 target** | **~35 signatures** | **~49 secondaries** | (some keystones serve cross-element signature+secondary roles, reducing net count) |
| **Net distinct v1** | **~30-50 distinct** | — | (catalogue-size range; final precision deferred) |

### 4.3 Open question — precision (~30 vs ~50)

**OPEN QUESTION (Q-T4-A-2):** is the catalogue ~30 (tighter; per-element ~4-5 signatures + ~3-5 secondaries; total ~30-40) or ~50 (richer; per-element ~5-7 signatures + ~7-10 secondaries; total ~40-50)?

The precision depends on:
- **T4-B authorship effort budget** — ~30 keystones is ~30-60 hours of design + review; ~50 keystones is ~50-100 hours
- **Catalogue mastery target** — can players learn 50 keystones over Reincarnated's seasonal arc? D4 Key Passive count: ~25; PoE keystone count: 100+; LE capstone count: ~50; D2 Hellfire Torch + tier-set bonus: ~60 combined
- **Per-season variety target** — how many keystones does a single player encounter per season? Reincarnated's 10-15-node skill tree (per math note § 3.1) limits per-class keystone exposure to ~2-4 per class; over 5-10 classes per season, ~10-40 keystones encountered

T4-A defers this precision to Matt's next design call. FILED AS OPEN QUESTION for T4-B authorship.

---

## 5. Gear-anchoring commitment — signature capstone IS gear-anchored

### 5.1 Default adoption

Per Q13 partial resolution (adopting gear-anchored signature when signature_gear_archetype present; mechanical-degradation-without-gear deferred per Matt pre-authorization C):

- **Signature capstone IS gear-anchored** when `signature_gear_archetype` is present in the kit's substrate vector (per gear-as-substrate LITE; derived-tag carries identity hint into capstone identity)
- **Mechanical-degradation-without-gear handling** deferred to v1.1/v2 with full gear-substrate promotion

### 5.2 Mechanism

The gear-as-substrate LITE path (`canonical/story/gear-as-substrate-2026-05-21.md` § 0.5.6) lands `signature_gear_archetype` as a DERIVED TAG in V1. This derived tag is computed at class generation via the G1-LITE rule table (`canonical/story/gear-archetype-rule-table-v1-2026-05-22.md`).

When a kit has a signature_gear_archetype set, the signature capstone Tier 4 keystone is **gear-anchored**:

- The capstone's identity ALIGNS with the gear-archetype (e.g., a fire+ranged+damage+STR-dom kit gets signature_gear_archetype = Blunderbuss = "Powder Pyromaniac" — the capstone is "Powder Hex-Cannon" or similar canonical rank-3 identity, NOT a generic fire-damage keystone)
- The capstone's regime-change effect REINFORCES the gear-archetype's mechanical signature (scatter geometry, slow tempo, etc.)
- The cohesion-judge's prompt receives both signature_gear_archetype AND signature_capstone as identity hints (per T4-C; P5 workstream)

### 5.3 Mechanical-degradation-without-gear — DEFERRED

The OPEN QUESTION (Q13) about whether mechanical degradation should occur without the matching gear (e.g., the Holy Pirate Sniper capstone refuses to function on a non-blunderbuss kit) is **DEFERRED to v1.1/v2** when gear-substrate is promoted to full substrate (G-PROMOTE-v1.1).

**Rationale:**
- V1 LITE path treats gear-archetype as DERIVED TAG, not generative substrate — the kit's gear-archetype is locked at generation, so mechanical-degradation isn't operationally needed (the kit ALWAYS has its locked archetype)
- V1.1/v2 promotes gear-archetype to generative substrate; at that point, gear-instance-vs-gear-archetype distinction may motivate mechanical-degradation rules (e.g., a Holy Pirate Sniper capstone may require the gear-instance to BE a blunderbuss, not just the archetype to be blunderbuss-family)

T4-A LOCKS the "signature capstone IS gear-anchored when signature_gear_archetype present" rule; T4-D (parallel-to-G1-LITE workstream) extends this with detailed signature_gear_archetype-to-keystone mapping; mechanical-degradation rules wait for v1.1/v2.

### 5.4 Gear-anchored signature in non-gear cases

When the substrate vector does NOT produce a signature_gear_archetype (no_signature outcome from G1-LITE rule table; v1 catalogue has none but v2 may), the signature capstone is gear-AGNOSTIC — the capstone identity comes purely from the substrate-triple without gear-anchoring.

This handles future cases cleanly without requiring T4-A to anticipate.

---

## 6. Development phasing commitment — T4-A → T4-E

### 6.1 Phase phasing

Per Matt 2026-05-22 pre-authorization C + protocol amendments doc § 3:

| Phase | Scope | Owner | Timing | Status |
|---|---|---|---|---|
| **T4-A** | Architecture design call — hierarchy + authorship pattern + gear-coupling + catalogue size DEFAULTS adopted; open questions surfaced | gandalf + Matt | Pre-P3 (this dispatch) | **DONE 2026-05-22** |
| **T4-B** | Catalogue authorship — ~30-50 keystones designed as rank-3 completers per BDI § 6 + ω/τ table v1; per-element distribution + cross-element capstones + sim-viability flags | gandalf + Matt (design); rocket (engine integration) | P3-P4 | Pending T4-A close + Matt T4-B framing approval |
| **T4-C** | Cohesion-judge prompt extension — refines P5 priority 2 prompt-engineering to distinguish signature capstone (rank-3 completer) from secondary capstones (rank-2 modulators) | star-lord + gandalf | P5 | Pending T4-B catalogue lock |
| **T4-D** | Gear-anchored signature capstone extension — detailed signature_gear_archetype-to-keystone mapping; pre-P5 workstream parallel to G1-LITE | gandalf + Matt | Pre-P5 (parallel to G1-LITE) | Pending T4-B catalogue lock |
| **T4-E** | Procedural / LLM-augmented Tier 4 variant generation — per-season variant naming + regime-change tweak based on substrate-vector specifics | Deferred | v2+ | Deferred |

### 6.2 Critical path implications

- **T4-A is a prerequisite for T4-B + T4-D.** Catalogue authorship and gear-anchored extension both depend on T4-A's hierarchy / authorship / catalogue-size commitments
- **T4-C depends on T4-B catalogue lock + P5 cohesion-judge implementation.** The signature-vs-secondary distinction in the prompt needs a concrete catalogue to reference
- **T4-A does NOT block W1.13.** W1.13 implements the convergence engine; the discrete Tier 4 keystone selection works against ANY catalogue (the convergence treats Tier 4 selection as a discrete-categorical choice regardless of catalogue content)

### 6.3 Cross-references with W1.13 rescope

Per the W1.13 rescope disposition (`canonical/story/w1-13-rescope-disposition-2026-05-22.md`), T4-A architecture continues to require W1.13's multi-dim convergence to operate. The rescope under Scenario B (dual-witness + Surface A footnote) does NOT change T4 architectural alignment — if anything, it strengthens it:

- **LC-011 Surface A finding** (skill_power_tier is causally active authorship parameter for mage_controller boundary convergence; Surface_A% = 66.67%) — this is a DESIGN-RELEVANT FINDING for T4-B catalogue authorship: skill_power_tier is a load-bearing authorship parameter for elemental Tier 4 keystone design
- **FILED AS OPEN QUESTION (Q-T4-A-4):** skill_power_tier as Tier 4 keystone authorship parameter for mage/controller archetypes — how does T4-B catalogue authorship encode the empirically-demonstrated coupling between skill_power_tier and convergence stability?

---

## 7. Open questions surfaced (for Matt's return)

The T4-A defaults adopted under pre-authorization C land the architectural commitments BUT explicitly DO NOT resolve four open questions. These surface for Matt's next design call:

### 7.1 Q-T4-A-1: Hierarchy enforcement at convergence-time

Does the convergence engine TREAT all Tier 4 keystones the same at SP allocation OR DISTINGUISH signature from secondary at SP allocation?

- **Path 1 (uniform treatment):** convergence treats all Tier 4 keystones identically; signature-vs-secondary distinction is cohesion-judge-side only (post-convergence)
- **Path 2 (hierarchical SP allocation):** convergence allocates more SP to signature capstone (e.g., 30-40 SP minimum) and less to secondaries (e.g., 5-15 SP each)

Recommended for Matt-discussion. Path 1 simpler; Path 2 identity-aligned.

### 7.2 Q-T4-A-2: Catalogue-size precision (~30 vs ~50)

Range adopted as ~30-50; precision deferred. Matt design call needed for T4-B effort planning.

### 7.3 Q-T4-A-3: Signature capstone "breakthrough moment" framing for cross-element capstones

Per p5-prompt-priorities § 2: cross-element capstones (Steam-Wraith bridging fire+water via volatility trait; Twilight-Judge bridging holy+shadow via trade-off trait) — how does the catalogue handle these vs single-element signatures?

- **Path A:** cross-element signatures are RARE catalogue entries gated by substrate-vector containing the bridge trait
- **Path B:** cross-element signatures are FIRST-CLASS entries available to any kit whose substrate vector matches the cross-element pair (regardless of trait bridge)
- **Path C:** cross-element signatures are LATER expansion (v1.1+); v1 catalogue is single-element only

Recommended for Matt-discussion during T4-B authorship pass.

### 7.4 Q-T4-A-4: skill_power_tier as authorship parameter (LC-011 recovery finding)

Per W0.7 cumulative design close-out + LC-011 recovery: skill_power_tier is empirically demonstrated as causally active authorship parameter for mage_controller boundary convergence (Surface_A% = 66.67%). How does T4-B catalogue authorship encode this coupling?

- **Path A:** each Tier 4 keystone has explicit `skill_power_tier` field; mage/controller catalogue entries calibrated at lower power-tier; physical/rogue catalogue entries at higher power-tier
- **Path B:** skill_power_tier remains a convergence-engine parameter (not per-keystone); T4-B authorship doesn't encode it directly; W1.13 convergence handles per-archetype calibration at SP allocation time
- **Path C:** hybrid — per-keystone skill_power_tier *suggested-default* with convergence-time override

Recommended for Matt-discussion during T4-B authorship pass. This is the design-relevant finding from the LC-011 recovery that the critique-pair surfaced for Matt's return.

---

## 8. What T4-A explicitly does NOT touch

Several Tier 4 commitments are NOT modified by T4-A (preserved per math note v1.1 + BDI formalism):

- **Mechanic-altering semantics** (math note § 3.4; legolas SD-1) — qualitative regime-change, NOT pure scaling. Per-rank coefficient 1.18-1.25 applies WITHIN a chosen keystone; identity comes from WHICH keystone, not from rank investment alone
- **Discrete categorical selection** at convergence (math note § 5; § 3.4) — Tier 4 keystone selection is a discrete choice per chain; multi-dim convergence's Phase 2 step
- **Per-chain catalogue size** — math note v1.1 § 9.4 specifies 3-5 candidate keystones per chain at generation time; T4-A doesn't change this (the 30-50 catalogue-wide count is across all chains × all elements)
- **Tier 4 ranks 1-15 scaling** — per-rank scaling within a chosen Tier 4 keystone preserved per math note § 2.3 (load-bearing for low-modifier kit boss-floor-fix)
- **BDI rank-3 completer framing** — per BDI § 6; preserved as theoretical foundation
- **Cross-element capstone framing** — per p5-prompt-priorities § 2 + BDI § 5.1; framing preserved but specific catalogue policy deferred to T4-B (Q-T4-A-3)

---

## 9. Cross-references

- `canonical/story/build-defining-resonance-formula-2026-05-21.md` § 6 (Tier 4 as rank-completer) + § 5.1 (rank-3 identity examples)
- `canonical/story/multi-dim-convergence-algorithm-2026-05-21.md` v1.1 § 3.4 (Tier 4 mechanic-altering semantics) + § 5 (categorical-discrete convergence)
- `canonical/story/p5-cohesion-judge-prompt-priorities-2026-05-21.md` § 2 (capstone identity alignment)
- `canonical/story/gear-as-substrate-2026-05-21.md` § 0.5.6 (LITE path)
- `canonical/story/gear-archetype-rule-table-v1-2026-05-22.md` (G1-LITE rule table; signature_gear_archetype derivation)
- `canonical/story/bdi-omega-tau-tables-v1-2026-05-22.md` (BDI ω/τ tables; high-β substrate-pair reference)
- `canonical/story/hive-mind-protocol-qd-engine-rebuild-2026-05-21.md` v1.3 § 5 (T4-A through T4-E phase architecture)
- `agentic_orchestration/hive-mind-protocol-amendments-2026-05-21-evening.md` § 3 (amendment 3 Tier 4 architecture open-question)
- `agentic_orchestration/hive-mind-state-evening-2026-05-21.md` § 4.3 (open questions 11-14)
- `canonical/story/w1-13-rescope-disposition-2026-05-22.md` § 3.3 (LC-011 Surface A finding → T4-B catalogue authorship implication)

---

**Signed:** gandalf (story-and-design steward; senior designer)
**For:** v1 Tier 4 architecture defaults adopted under Matt 2026-05-22 pre-authorization C — 1+1-3 hierarchy + hand-authored catalogue + gear-anchored signature; phasing T4-A→T4-E; four open questions surfaced for Matt's next design call (Q-T4-A-1 through Q-T4-A-4).
