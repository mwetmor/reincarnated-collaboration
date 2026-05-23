# P5 Cohesion-Judge Prompt-Engineering Priorities

> **STATUS:** HISTORICAL-INFORMATIVE (pre-Epoch-4; consult for lineage only — not current truth) — see `canonical/00-ground-state.md` for current truth

**Date:** 2026-05-21 (evening, post substrate-as-cohesion validation probe)
**Author:** gandalf (story-and-design steward)
**Status:** AUTHORED — pre-P5 reference doc
**Companion to:** `canonical/story/multi-dim-convergence-algorithm-2026-05-21.md` v1.1 § 6.6
**For:** star-lord (LLM seam) when P5 cohesion-judge integration fires; gandalf when prompt-design review fires

---

## 0. TL;DR

The substrate-as-cohesion validation probe (2026-05-21) returned **4.35 mean coherence at small sample (N=10)** — high-confidence validation per § 3 of the dispatch. But it surfaced **three failure modes** that need explicit prompt-engineering work in P5, plus **two extensions** that land if gear-as-substrate is adopted (per `gear-as-substrate-2026-05-21.md`).

This doc captures all five priorities **before they get rediscovered mid-P5 implementation.** Pre-loading the prompt-engineering surface lets star-lord author P5 prompts with explicit failure-mode handling rather than reactive iteration.

**Priorities (in probe-surfaced order):**
1. Three-element contamination handling
2. Capstone identity alignment
3. Awkward element × role pairing reframing
4. Gear-archetype recognition (if gear-as-substrate adopted)
5. Gear-archetype × element cross-coherence (if gear-as-substrate adopted)

---

## 1. Priority 1 — Three-element contamination handling

### 1.1 The failure mode

**Observed in probe:** class_0016 (s200002, lightning_controller) scored **3.5** — the only kit below the 4.0 threshold. Root cause: secondary-loop element substitution injected skills from three different elements (lightning + shadow + fire) into one kit, including a fire T4 teleport as chain_A capstone. The cohesion-judge could not assemble a unified identity from three substrate signals; the result fragmented.

**Probe finding:** the cohesion-judge handles 2-element contamination cleanly (recovers as "hybrid identity," e.g., volcanic-earth, cold-wind), but breaks at 3-element contamination.

### 1.2 Prompt-engineering options

**Option A — Reject at archive insertion**

Add a pre-coalescence filter: kits with > 2 distinct dominant elements (where "dominant" = canonical_element appearing on ≥ 2 skills, OR appearing as T4 capstone) are rejected before cohesion-judge fires. Failed kits route back to convergence loop for substrate-vector recomposition.

- **Pros:** keeps cohesion-judge load bounded; clean failure mode at insertion
- **Cons:** discards potentially-usable mechanical work; convergence churn increases

**Option B — Dominant-identity + "shadow influence" framing**

Prompt instructs the cohesion-judge: when 3+ elements present, identify the dominant element (most-frequent in mechanical signature), name the second-most as "complementary influence," and name the third as **"shadow influence"** — a residual stylistic note rather than a competing identity signal.

Example prompt-fragment:
> *"If the mechanical signature contains skills from three or more distinct elements, identify ONE dominant element (the element with the most skills, or whose T4 capstone is present), assign the class identity to that element, and treat additional elements as either 'complementary influence' (for the second-most-frequent element, used to enrich flavor prose) or 'shadow influence' (for any third element, mentioned only briefly as a residual stylistic note). Do NOT attempt to assemble three-way hybrid identity."*

- **Pros:** preserves mechanical work; cohesion-judge produces usable output; class_0016 would have scored ≥ 4.0 with this framing
- **Cons:** "shadow influence" is editorial; some kits will have weak attribution for the residual element

**Option C — Hybrid (recommended)**

Apply Option B by default; escalate to Option A only when dominant-element fraction drops below 50% (no element clearly dominates). This handles most cases through prompt; preserves rejection for genuinely-fragmented kits.

### 1.3 Validation

After prompt update, re-probe class_0016 (and any 3+-element kits in the probe sample). Target: ≥ 4.0 mean coherence on previously-failing kits. If achieved, Option B integrates into P5 production prompt.

---

## 2. Priority 2 — Capstone identity alignment

### 2.1 The failure mode

**Observed in probe:** class_0016's most dissonant single signal was **fire T4 teleport as chain_A capstone** on a lightning-controller. Capstones disproportionately weight the cohesion-judge's identity inference — they ARE the highest-power thematic expression. A capstone whose element doesn't match the class's dominant element fragments identity perception.

**Probe finding:** the cohesion-judge implicitly treats capstones as identity-anchors, but the prompt doesn't make this explicit. When element mismatch occurs, the judge has no instruction for how to resolve it.

### 2.2 Prompt-engineering recommendation

Add an explicit capstone-identity instruction to the cohesion-judge prompt:

> *"The capstone (T4 keystone) of each chain carries disproportionate identity weight. If a capstone's element matches the dominant substrate, anchor the chain's thematic name to the capstone's signal. If a capstone's element conflicts with the dominant substrate, EITHER (a) treat the capstone as a 'breakthrough moment' where the spirit's identity transcends its primary element (rare; reserve for narratively-significant kits), OR (b) treat the capstone as evidence the dominant element is misidentified and re-evaluate substrate before naming. Do NOT name the chain after the capstone's element if it conflicts with the dominant substrate."*

This gives the judge explicit decision-handling for the capstone-mismatch case.

### 2.3 Why this matters beyond probe

The capstone-identity weighting is a **general property** of the cohesion-judge, not just an edge-case failure. In the probe, even kits scoring 4.5-5.0 had capstones doing significant identity work (class_0007's drain T4; class_0012's totem T4; class_0008's leap T4). Making the capstone-handling explicit in the prompt **sharpens cohesion across the entire archive**, not just the failing edge.

### 2.4 Validation

Re-probe sample with new capstone-instruction prompt. Compare coherence scores at the kit level. Target: ≥ 0.1 mean coherence lift across kits where capstone element matches dominant; preserved performance where capstone is cross-element.

---

## 3. Priority 3 — Awkward element × role pairing reframing

### 3.1 The failure mode

**Observed in probe:** class_0010 (fire_controller; silence-ring + VIT-tanky) scored **4.0** — passing, but the cohesion-judge struggled. Silence is mechanically/genre-canonically a shadow or wind effect; pairing silence-ring as the *primary control mechanic* on a fire-element kit creates "what is this thing supposed to be?" friction.

**Probe finding:** the cohesion-judge can recover the identity via active editorial reframing ("soundless heat," "voice-quenching pyre"), but the prompt doesn't currently teach it how to. The judge falls back on generic "fire controller" framing, which is weaker than what the mechanical signature could support.

### 3.2 Specific element × role pairings with low cohesion ceiling

The probe surfaced **fire × control** as awkward; the same pattern likely applies to other element × role combinations that genre-precedent doesn't strongly support:

| Element × Role | Canonical comfort | Awkwardness source | Reframing handle |
|---|---|---|---|
| fire × control | low | silence/freeze are core control mechanics; fire's "control" is awkward | "soundless heat," "voice-quenching pyre," "burning-stillness" |
| water × damage | medium | water is canonically supportive/control; pure damage water is genre-rare | "crushing-tide," "blade-of-rain," "frozen-spike" |
| holy × shadow-hybrid | low | holy and shadow are genre-opposed | "twilight-judge," "ash-priest," "fallen-paragon" |
| earth × range | medium | earth is canonically melee/control; range is genre-rare | "stone-launcher," "tectonic-marksman," "soil-flinger" |
| shadow × support | low | shadow is canonically self-trade-off, not party-support | "bond-leech," "shadow-anchor," "silent-warden" |
| lightning × defense | low | lightning is canonically glass-cannon | "stormwall," "charged-bulwark," "aegis-arc" |

These are not all probe-observed; some are predicted-from-genre. Worth empirical verification through a re-probe pass when prompt-update is authored.

### 3.3 Prompt-engineering recommendation

Add a genre-precedent reframing instruction to the cohesion-judge prompt:

> *"When an element × role combination is genre-uncommon (e.g., fire × control, water × damage, holy × shadow-hybrid, earth × range, shadow × support, lightning × defense), you MAY use active editorial reframing to produce a coherent identity. Acceptable reframing patterns: (a) mechanical-inversion framing ('soundless heat' for fire-control; 'crushing-tide' for water-damage), (b) thematic-resolution framing ('twilight-judge' for holy-shadow), (c) physical-realism framing ('stone-launcher' for earth-range). Apply reframing ONLY when needed for cohesion; default to canonical pairings when element × role is genre-typical."*

### 3.4 Reference catalogue

A reference catalogue of awkward-pairing reframings should accompany the prompt. Initial catalogue is § 3.2 above; this should be maintained as a living document as probes surface additional pairings.

---

## 4. Priority 4 — Gear-archetype recognition (if gear-as-substrate adopted)

### 4.1 The expansion

Per `canonical/story/gear-as-substrate-2026-05-21.md`, gear-archetype becomes a fourth substrate axis at coalescence time. The cohesion-judge receives gear-archetype alongside element, range, role, and must recognize it in the mechanical signature.

### 4.2 What "recognition" means

The cohesion-judge must:
1. **Validate** the supplied substrate-vector gear_archetype against the mechanical signature (does this kit's geometry × tempo × range pattern actually match "blunderbuss," or has the substrate vector been mis-applied?)
2. **Weight** gear-archetype as a tie-breaker between near-identity classes (per substrate supplement § 2.1: gear is the disambiguator when element + range + role alone are insufficient)
3. **Flow** gear-archetype's vocabulary signal into the identity name (the blunderbuss surfaces "powder," "scatter," "pirate," "rust-coast" as vocabulary tokens; the censer surfaces "thurible," "smoke-blessing," "incense-vow")
4. **Reject** gear-archetype × mechanical-signature mismatches (a kit with all-melee geometry but blunderbuss as substrate vector is structurally invalid; flag for substrate-recomposition)

### 4.3 Prompt-engineering recommendation

Add a gear-archetype instruction block to the cohesion-judge prompt:

> *"The mechanical signature includes a gear-archetype substrate input (e.g., 'blunderbuss', 'censer', 'kanabō'). You must: (1) verify the mechanical signature is consistent with the gear-archetype's expected geometry/tempo/range signature — flag mismatches with structural-incoherence rather than naming forward; (2) treat gear-archetype as a primary disambiguator when element + range + role alone leave the identity ambiguous; (3) flow gear-archetype's vocabulary into the identity name and prose. Reference: `canonical/story/gear-as-substrate-2026-05-21.md` § 3 for the gear-archetype taxonomy and vocabulary tokens."*

### 4.4 Validation

After gear-as-substrate adoption, run a new probe (similar to 2026-05-21 substrate-as-cohesion probe) with gear_archetype included in the mechanical signature. Target: ≥ 4.0 mean coherence at 4-substrate scale (the probe's 3-substrate baseline being 4.35).

If 4-substrate probe lands < 4.0, this priority becomes a P5 blocker; if ≥ 4.0, it integrates as scheduled refinement.

---

## 5. Priority 5 — Gear-archetype × element cross-coherence (if gear-as-substrate adopted)

### 5.1 The expansion

Some gear-archetype × element pairings carry strong genre-precedent (holy + censer, shadow + veil, lightning + wand); others carry surprising-but-evocative resonance (holy + blunderbuss = Holy Pirate Sniper; shadow + horn = Whispering Evangelist). The cohesion-judge must handle both gracefully.

### 5.2 Pairing categories

| Category | Examples | Cohesion-judge handling |
|---|---|---|
| **Canonical-strong** | holy+censer, shadow+veil, lightning+wand, fire+torch-staff, water+focus-orb | Anchor identity to the canonical pairing; vocabulary flows freely |
| **Canonical-medium** | physical+greatsword, earth+warhammer, wind+longbow | Standard genre-canon; no special handling |
| **Surprising-but-evocative** | holy+blunderbuss, shadow+horn, fire+censer (smoke-cleric), water+kanabō (typhoon-strike) | Apply creative-reframing; flag in prose as "uncommon-but-coherent" identity |
| **Awkward** | shadow+holy-symbol, holy+veil, fire+water-orb | Apply Priority 3 reframing if salvageable; reject at substrate-composition if not |

### 5.3 Prompt-engineering recommendation

Extend the gear-archetype instruction block from Priority 4:

> *"Different gear-archetype × element pairings carry different cohesion ceilings. (a) Canonical pairings (holy+censer, lightning+wand, etc.): anchor identity strongly; flow vocabulary freely. (b) Surprising-but-evocative pairings (holy+blunderbuss, shadow+horn): apply creative reframing; identity name should reflect the surprising pairing as a distinctive feature ('Holy Pirate Sniper,' 'Whispering Evangelist'). (c) Awkward pairings (shadow+holy-symbol, fire+water-orb): apply Priority 3 reframing patterns; if no coherent reframing surfaces, flag for substrate-recomposition rather than producing weak naming."*

### 5.4 Validation

Same probe pattern as Priority 4: re-probe at 4-substrate scale; verify cohesion holds across all four categories. Particular attention to the **surprising-but-evocative** category — this is where gear-as-substrate's design power most directly shines.

---

## 6. Cross-cutting prompt-engineering pattern

All five priorities share a common pattern:

1. **Identify the failure mode** with empirical evidence (probe finding or genre-precedent prediction)
2. **Specify the instruction** the cohesion-judge needs to handle it
3. **Provide reframing handles** when the case is salvageable (vs. rejection at substrate-composition)
4. **Validate via re-probe** at the prompt-update boundary

This pattern is **the canonical prompt-engineering discipline for substrate-as-cohesion**. Future prompt-engineering priorities (e.g., trait-cluster-as-substrate if adopted; v2 substrate-catalogue-expansion) should follow the same pattern.

---

## 7. Integration timing

| Priority | When integrated | Owner |
|---|---|---|
| 1 — Three-element contamination | P5 cohesion-judge prompt v1 (initial integration) | star-lord |
| 2 — Capstone identity alignment | P5 cohesion-judge prompt v1 | star-lord |
| 3 — Awkward element × role | P5 cohesion-judge prompt v1 | star-lord + gandalf (catalogue maintenance) |
| 4 — Gear-archetype recognition | P5 cohesion-judge prompt v1.1 (after G3 gear-archetype generation lands) | star-lord |
| 5 — Gear × element cross-coherence | P5 cohesion-judge prompt v1.1 | star-lord + gandalf (pairing-catalogue maintenance) |

**All five priorities should be addressed in P5 v1.x before v1 ship.** None blocks the existing QD-rebuild critical path; they expand P5 scope by ~2-3 weeks of prompt-engineering work, which is acceptable given the validation gain.

---

## 8. Cross-references

- `canonical/story/multi-dim-convergence-algorithm-2026-05-21.md` v1.1 § 6.6 — probe-surfaced failure modes summary
- `canonical/story/substrate-design-supplement-2026-05-21.md` — substrate identity framework + § 2.1 shadow-trade-off thesis
- `canonical/story/gear-as-substrate-2026-05-21.md` — gear-archetype substrate framing (Priorities 4 + 5 reference)
- `agentic_orchestration/dispatches/2026-05-21-legolas-substrate-as-cohesion-empirical-validation-probe.md` — probe dispatch (verdict 4.35 mean coherence)
- `canonical/story/hive-mind-protocol-qd-engine-rebuild-2026-05-21.md` § 6 — P5 cohesion-judge integration phase
- S1 first-batch season_100001 "The Battlefield Where Nothing Grew Back" (cohesion 4.83) — baseline reference for "what cohesion-judge can produce at its best with full coalescence"
- R8 inverted A/B (cohesion 4.77) — reference baseline for cohesion-judge with coalescence pass applied

---

**Signed:** gandalf (story-and-design steward)
**For:** P5 prompt-engineering preloading; star-lord reference at P5 integration time; gandalf review at prompt-design review boundary.
