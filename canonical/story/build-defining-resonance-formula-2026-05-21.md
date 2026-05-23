# Build-Defining as Resonance — A Mathematical and Mythic Formula

> **STATUS:** HISTORICAL-INFORMATIVE (pre-Epoch-4; consult for lineage only — not current truth) — see `canonical/00-ground-state.md` for current truth

**Date:** 2026-05-21 (evening, post substrate-as-cohesion validation probe)
**Author:** gandalf (story-and-design steward)
**Status:** AUTHORED — proposed mathematical foundation for substrate-architecture work
**Companion to:** `canonical/story/substrate-design-supplement-2026-05-21.md`, `canonical/story/gear-as-substrate-2026-05-21.md`, `canonical/story/multi-dim-convergence-algorithm-2026-05-21.md` v1.1
**Authority:** design-architectural; proposes formalism; empirically testable; hypothesis-tests included

---

## 0. TL;DR

A **build-defining moment** in an ARPG occurs when one or more substrate components in a class kit produce a discontinuous lift in performance AND identity, beyond what additive contributions of those substrates would predict. Mathematically: **the interaction term dominates the linear term.**

This doc proposes:

1. A formal definition (**Build-Defining Index, BDI**) measuring how strongly a substrate-pair or substrate-triple "defines" a build
2. Two scalar fields (**ω** mechanical-overlap, **τ** thematic-resonance) that drive the interaction-term magnitude
3. A **rank-classification** for builds: rank-1 (generic), rank-2 (paired identity), rank-3 (signature build), rank-4+ (degenerate/rare)
4. A connection to the **Tier 4 keystone architecture** — Tier 4 keystones are *rank-completers* that promote a kit's resonance from rank-2 to rank-3
5. A connection to the **cohesion-judge layer** — high-BDI kits produce high cohesion-judge scores; the math model and the narrative model read the same resonance through different sensors
6. **Five empirically-testable hypothesis tests** the hive-mind can run against the QD archive overnight (P1+) without constraining generation behavior

**Scientific posture:** this is a *proposed* formalism, empirically testable. The hypothesis tests are diagnostic — they measure whether BDI/resonance is real in the archive. If they confirm, the substrate composer CAN start preferring high-BDI vectors during P1+ work. If they don't confirm, the formalism is reframed or parked. **No endless-loop risk:** BDI is a metric, never a hard filter; generation never mandates a specific rank.

---

## 1. The phenomenon

In every Diablo-lineage ARPG and every isekai stat-system narrative, certain class configurations produce **outsized identity AND outsized performance** simultaneously. The genre names these:

- **PoE:** Mjölner Discharger, Crown of Eyes Ranger, Pain Attunement Witch
- **D2:** Frozen Orb Sorc, Smiter Pala, Whirlwind Barb
- **D3:** Sunwuko Wave-of-Light Monk, Inna Mystic Ally, Bone Spear Necromancer
- **D4:** Lightning Spear Sorc, Bone Spirit Necro, Pulverize Druid
- **LE:** Aberrant Calling, Falconer Reaper
- **GD:** Templar Cadence, Vindicator Stormbringer
- **Isekai:** Rudeus's silent-casting-precision; Jinwoo's Shadow-Monarch; Subaru's pact-binding

What unites these is not "high damage" or "fancy keystone." What unites them is that **removing one of the substrate components collapses BOTH the identity AND the performance.** A Pain Attunement Witch without Pain Attunement is not "still a witch with lower DPS" — it's a different build entirely.

This is the empirical signature of a build-defining moment: **the substrate components are not additive; they are interactive.**

## 2. The mathematician's framing — interaction-term dominance

Let v = (s_1, s_2, ..., s_n) be a substrate vector. In Reincarnated v1, n = 4 (element, range, role, gear-archetype); v2 extends to n = 5 (+ trait-cluster).

Let WR(v) ∈ [0, 1] be the win rate of the kit generated from v under canonical gauntlet conditions.

### 2.1 The linear model (plain build)

$$WR_{\text{linear}}(v) = \alpha_0 + \sum_i \alpha_i \cdot s_i + \varepsilon$$

Each substrate component contributes additively. Remove one and WR shifts by Δ ≈ α_i. Performance is well-approximated by the sum of parts.

### 2.2 The interaction model (build-defining)

$$WR(v) = \alpha_0 + \sum_i \alpha_i \cdot s_i + \sum_{i<j} \beta_{ij} \cdot s_i s_j + \sum_{i<j<k} \gamma_{ijk} \cdot s_i s_j s_k + \dots + \varepsilon$$

When β or γ terms have magnitude **comparable to or larger than** the linear α terms, the build is **interaction-dominant**. The substrate-pair (or triple) producing the large β (or γ) is **what defines the build.**

### 2.3 The Build-Defining Index (BDI)

For a substrate-pair (s_a, s_b) in vector v:

$$\text{BDI}_2(s_a, s_b \mid v) = \frac{|\beta_{ab}|}{\sum_k |\alpha_k|}$$

For a substrate-triple (s_a, s_b, s_c):

$$\text{BDI}_3(s_a, s_b, s_c \mid v) = \frac{|\gamma_{abc}|}{\max\bigl(|\beta_{ab}|, |\beta_{ac}|, |\beta_{bc}|\bigr)}$$

(Note the rank-3 BDI normalizes against the *dominant pairwise term*, not the linear sum — a true rank-3 build has the triple dominating any pair within it.)

**Thresholds (proposed; empirically calibrate):**
- BDI_2 > 1.0 → pairwise build-defining
- BDI_3 > 1.0 → triple-synergy signature build
- BDI_3 > 2.0 → "rank-3 dominant" (the genre's legendary-tier builds)

### 2.4 The resonance signature

A vector's full resonance structure is the ordered set:

$$R(v) = \bigl\langle \text{rank}(v), \{ \beta_{ij} \text{ above threshold} \}, \{ \gamma_{ijk} \text{ above threshold} \} \bigr\rangle$$

where rank(v) = highest interaction-order with dominant magnitude:
- **rank 1**: no interaction dominates → generic build, no identity center
- **rank 2**: one or more β-pairs dominate → paired-identity build
- **rank 3**: one γ-triple dominates → signature build identity
- **rank 4+**: rare; in the genre, typically either degenerates to rank-3 with strong γ + auxiliary β, or breaks coherence

---

## 3. The wizard's framing — resonance

Strip the formalism. A build-defining moment is when the parts of a thing speak to each other.

When two substrate components share a structural language — when their geometries, tempos, ranges, or thematic stances *agree* — they amplify across the shared dimension. Their power compounds rather than adds. **This is shared-language amplification.**

When two substrate components are in TENSION — when they nominally oppose — they can still resonate IF a third element bridges the opposition, revealing that the apparent contradiction shares a deeper structural mode. **This is tension-resolution synergy.**

When three substrate components share BOTH an amplifying signal AND a thematic axis, they produce **signature resonance** — a build whose identity is *the resonance itself*, not the components.

A class without resonance is a collection of mechanics. A class with resonance is an identity. **The cohesion-judge intuits resonance from mechanical signature because resonance produces an identity-pattern.** When the probe's class_0007 (shadow_mage; drain + silence + zero contamination) scored 5.0, what the cohesion-judge heard was rank-2 resonance — drain (shadow's signature trade-off mechanic) and silence (shadow's signature control mechanic) speaking to each other through the substrate supplement's "shadow = trade-off" axis.

When class_0016 fragmented at 3.5, what the cohesion-judge heard was the *absence* of resonance — three elements that did not share a structural language, no interaction term dominating, just additive substrate without a center.

The cohesion-judge is, in this view, **a resonance-detector.** The probe verdict (4.35 mean coherence on raw mechanical signature) confirms that resonance is detectable from kit data alone — meaning the resonance is structurally present in the kits, not added by naming.

---

## 4. The two field equations of build-defining

For β_{ab} (pairwise interaction) to be large, the substrate-pair must satisfy one of two structural conditions. These are the **two field equations** that drive the interaction-term magnitude.

### 4.1 The ω-field — Mechanical Overlap

$$\omega(s_a, s_b) \in [0, 1]$$

Measures how much two substrate components share **mechanical signals**:
- Geometry signature overlap (scatter, line, arc, sweep, area, beam, point)
- Tempo signature overlap (slow / measured / fast / burst / channeled)
- Range signature overlap (melee, medium, ranged)
- Resource signature overlap (stamina, mana, vigor, ki, fury)
- Effect-category signature overlap (control, damage, sustain, debuff, mobility)

**When ω is high, β tends positive via multiplicative compounding.** Both substrates push the kit's resources/allocations toward the same mechanical pole. The per-tick gain on that pole compounds rather than diversifies.

#### High-ω pair predictions (proposed table; empirically calibrate)

| Substrate-pair | ω (predicted) | Shared signal |
|---|---|---|
| blunderbuss + burst-glass | 0.85 | high-commit single-volley damage |
| greatsword + ground-anchor | 0.80 | stance-and-strike weight |
| censer + sustain-leech | 0.75 | area-aura sustain |
| longbow + swift-strike | 0.75 | fast precision |
| chain + control-overrun | 0.85 | reach-and-disable |
| stamina + physical | 0.95 | resource-element uniquely-bound |
| chill + control | 0.85 | slow-and-disable |
| scatter + AOE | 0.80 | area-coverage geometry |
| channel + ritual-channel | 0.90 | sustained-cast tempo |
| longbow + ranged | 0.95 | range-axis identity |

### 4.2 The τ-field — Thematic Resonance

$$\tau(s_a, s_b) \in [-1, 1]$$

Measures **thematic compatibility** on the substrate-supplement's identity axis:
- Positive τ: canonical pairing (holy + smite; shadow + drain)
- Near-zero τ: neutral (water + longbow)
- Negative τ: polar opposition (holy + shadow; sustain + glass)

**When |τ| is high, β can be large in EITHER direction:**
- Positive-τ pairs produce canonical builds — mid-range β; well-trodden genre territory
- Negative-τ pairs WITH A BRIDGE produce signature tension-builds — high β; genre-legendary territory
- Negative-τ pairs WITHOUT A BRIDGE produce identity-failure — β negative or zero; cohesion collapses

#### τ-field high-magnitude pair predictions (proposed table)

**Strong positive-τ (canonical pairing):**

| Pair | τ | Identity stance |
|---|---|---|
| holy + censer | +0.90 | ritual-cleric |
| shadow + veil | +0.90 | trickster-rogue |
| lightning + wand | +0.85 | precision-mage |
| fire + greatsword | +0.70 | forge-warrior |
| water + focus-orb | +0.75 | tide-elementalist |
| physical + warhammer | +0.85 | smithing-warlord |

**Strong negative-τ (polar; potential bridge-builds):**

| Pair | τ | Bridge substrate | Bridged identity |
|---|---|---|---|
| holy + shadow | -0.90 | trait_cluster = trade-off | **Twilight-Judge** |
| fire + water | -0.85 | trait_cluster = volatility | **Steam-Wraith / Boiling-Mage** |
| earth + wind | -0.70 | trait_cluster = momentum | **Sandstorm-Strider** |
| sustain (role) + glass (defense) | -0.80 | trait_cluster = lifesteal | **Berserker-Reaver** |
| control + aggression | -0.65 | gear_archetype = chain | **Stoneshackle Inquisitor** |
| support + solitary | -0.70 | gear_archetype = trumpet/horn | **War-Evangelist** |

### 4.3 The combined predictor

The proposed relationship between the field values and the interaction coefficient:

$$\beta_{ab} \approx \kappa_1 \cdot \omega(s_a, s_b) + \kappa_2 \cdot \tau(s_a, s_b) \cdot B(s_a, s_b; v) + \text{higher order}$$

where:
- κ_1, κ_2 are empirical scaling constants (to be calibrated)
- B(s_a, s_b; v) ∈ {0, 1} indicates the presence of a bridging substrate in v (1 if bridged, 0 otherwise)
- The τ-term contributes positively when there IS a bridge, and contributes negatively (or to noise) when there is not

**Two distinct routes to high β are captured:** ω-high (Case A) and |τ|-high-with-bridge (Case B).

---

## 5. Rank-3 — the signature build

The deepest builds in the genre are not rank-2; they are **rank-3.** A signature build's identity emerges from a *three-substrate resonance* that no pair alone produces.

### 5.1 Rank-3 examples (proposed; empirically validate)

| Substrate-triple | Predicted identity | Resonance source |
|---|---|---|
| holy + blunderbuss + burst-glass | **Powder Hex-Cannon** | rank-3 γ: holy-judgment moment + blunderbuss-volley moment + burst-glass commit; all three close on "one righteous shot" |
| shadow + censer + sustain-leech | **Smoke-Vampire / Ash-Reaver** | shadow's trade-off + censer's area-aura + sustain-leech's lifesteal close on "drinking the slow-burn aura" |
| fire + greatsword + ground-anchor | **Inferno-Knight / Forge-Champion** | fire's combustion + greatsword's arc + ground-anchor's stance close on "immovable burning column" |
| water + longbow + swift-strike | **Storm-Sentinel / Tide-Marksman** | water's precision + longbow's line + swift-strike's tempo close on "rain-of-arrows" |
| earth + chain + control-overrun | **Stoneshackle / Crag-Binder** | earth's mass + chain's reach + control-overrun's lockdown close on "stone-tether" |
| lightning + wand + ritual-channel | **Stormcaller-Archmage** | lightning's arc + wand's precision + ritual-channel's sustained-cast close on "storm-summoner" |
| holy + horn + support | **War-Evangelist** | holy's blessing + horn's blast-cone + support's amplification close on "battlefield-revival anthem" |
| shadow + twin-daggers + trickster-misdirect | **Nightshroud Assassin** | shadow's misdirection + twin-daggers' multi-hit + trickster's feint close on "vanishing-strike" |

### 5.2 What rank-3 resonance feels like

A rank-3 build has the property that **none of the three components is dispensable.** Strip any one and the build collapses — not just numerically, but identity-wise. The Powder Hex-Cannon without burst-glass is a generic Holy Pirate Sniper; without holy is a Powder Glass-Cannon (rank-2; ok); without blunderbuss is a fragile Holy Inquisitor (rank-2; ok). All three together produce *the rank-3 moment*: a one-shot judgment-volley that IS the build's identity.

The genre treats rank-3 builds as **legendary-tier.** They appear on guide-sites with named labels. Players seek them by name, not by mechanical description.

### 5.3 Rank-4 and above — the genre's frontier

Rank-4+ resonance is rare and structurally unstable. PoE occasionally produces it (4-keystone builds with shared mechanic). D4 paragon-glyph clusters sometimes hit rank-4. But the genre's mass-attention sits at rank-3; rank-4+ is typically either:
- A rank-3 build with a strong γ + auxiliary β-pairs (effectively rank-3-with-decoration)
- A genuine rank-4 that breaks coherence (too many constraints; identity fragments)

**Reincarnated v1 targets rank-2 and rank-3 explicitly. Rank-4+ is post-v2 territory or accepts identity-fragmentation as a known cost.**

---

## 6. The Tier 4 keystone as rank-completer

The math note v1.1 specified Tier 4 keystones as mechanic-altering (qualitative regime change). The BDI formalism completes this picture: **a Tier 4 keystone is structurally a *rank-completer*.** It takes a kit's rank-2 resonance and promotes it to rank-3 by adding the third leg.

### 6.1 The signature capstone

For a kit with substrate vector v and dominant pairwise resonance β_{ab}, the Tier 4 signature capstone introduces a **third substrate component s_c** (mechanically expressed via the keystone's regime-change) such that γ_{abc} > β_{ab}.

The capstone IS the rank-3 closer. This is why capstones are mechanic-altering (regime-change) rather than scaling — they open a *new dimension of resonance*, not magnitude on an existing dimension.

### 6.2 Secondary capstones

Auxiliary Tier 4 keystones in a kit's other chains add **additional rank-2 resonances** (auxiliary β-pairs that don't complete to rank-3 but provide build depth). They modulate the build without owning its identity.

This is the architecture sketched in the Tier 4 discussion (open questions 11-14 of the hive-mind state evening doc):
- 1 signature capstone (rank-3 completer; build-defining; gear-anchored when gear-substrate is live)
- 1-3 secondary capstones (rank-2 modulators; flavor-altering but identity-secondary)

**Empirical implication:** Tier 4 keystone catalogue authorship (T4-B) should explicitly target rank-3 completion. Each keystone in the catalogue should be designed as the third leg of a known high-β substrate-pair, producing a known rank-3 identity.

---

## 7. Empirical predictions and hypothesis tests

The BDI formalism is testable. The following hypothesis tests can be run against the QD archive data during P1+ work, **independent of and non-interfering with substrate-composer behavior** (they're diagnostic, not constraints).

### 7.0 Methodology decisions (lock before tests run)

Three methodological decisions, surfaced via Matt 2026-05-21 evening sharpening pass, must be made before the team executes:

#### 7.0.1 Outcome variable — Damage AND WR (both)

**Decision:** test against BOTH damage output AND win rate as parallel outcome variables.

| Metric | What it measures | Signal cleanliness |
|---|---|---|
| Damage output | Offensive contribution per fight (continuous; from per-fight telemetry) | **Cleaner empirical signal** — single dimension; less gauntlet-balance noise |
| Win Rate | Holistic balance (damage + defense + control + tempo + interactions) | Noisier but reflects whole-build effectiveness across roles |

**Why both:** damage-only would miss build-defining patterns in non-damage roles (e.g., Stoneshackle: earth + chain + control-overrun is rank-3 build-defining via control lockdown, not damage). WR-only would miss damage-specific resonance patterns. Running both gives clean attribution: if a hypothesis confirms on damage only, BDI is damage-specific; if it confirms on both, BDI is universal.

#### 7.0.2 "Synergy" disambiguation — rank, not count

Three plausible interpretations of "synergy" in build-defining context:

| Interpretation | Predicts | BDI mapping |
|---|---|---|
| (a) Synergy **COUNT** | Linear: more pairs above β-threshold = more damage, additive | Multiple rank-2 stacked |
| (b) Synergy **RANK** | Step function: rank-3 >> rank-2 > rank-1, discontinuous | The BDI formalism's prediction |
| (c) Synergy **MAGNITUDE** | Continuous: damage scales smoothly with max-BDI value | Within-rank scaling |

**Decision: H1 tests interpretation (b) — RANK.** The BDI formalism predicts discontinuous step jumps at rank boundaries, not gradual accumulation. A single high-γ rank-3 build is more build-defining than three weakly-positive rank-2 builds, because the genre's signature-build pattern is rank-3-dominance.

Interpretation (a) is implicitly tested by H3 (model-fit comparison); interpretation (c) is implicitly tested by H4 (γ-magnitude dominance). H1 specifically tests (b).

#### 7.0.3 Tier 4 data-availability — three options

The math note v1.1's **mechanic-altering Tier 4 keystone architecture** is a W1.13 design commitment; not yet implemented. Current archive data does NOT have formally-tagged mechanic-altering Tier 4 keystones — only skills at the highest existing tier.

**Decision: run hypothesis tests under three nested options:**

| Option | Approach | Available |
|---|---|---|
| **Option C (run now)** | Generalize: test BDI rank-3 in current archive without Tier 4 framing — does the substrate vector show γ-dominance regardless of Tier 4 implementation state? | ✅ Now |
| **Option A (sensitivity check)** | Use current tier-4-skills as proxy: when a kit's tier-4 skill shares mechanical signal (geometry/tempo/element) with 2-3 other skills in the kit, is damage higher? | ✅ Now (with caveats — current tier-4 skills aren't authored as rank-completers) |
| **Option B (post-W1.13 confirmation)** | Re-run all tests against archive AFTER W1.13 implements true mechanic-altering Tier 4 keystones | ⚠️ P2-P3 territory |

The team should run Options C+A in P1 (immediately available), and Option B as confirmation post-W1.13.

---

### 7.1 Hypothesis tests (for hive-mind execution during P1+)

**Null hypothesis (H0; common to all tests):** Damage output and win rate are **independent of BDI structure** — independent of rank, of ω, of τ, of bridge-presence, of γ-dominance. The substrate vector's mechanical signature explains performance only via additive contributions; interaction terms have variance ≈ 0.

#### H1 (PRIMARY) — Rank-step discontinuity in damage AND WR

**Hypothesis:** Both damage output AND win rate are higher for kits with higher-rank BDI structure than kits with lower-rank structure. The relationship is **discontinuous (step function), not gradual** — rank-3 >> rank-2 > rank-1, with sharp jumps at rank boundaries.

**Predicts:**
- rank-3 kits have mean damage AND mean WR significantly higher than rank-2 kits
- rank-2 kits have mean damage AND mean WR significantly higher than rank-1 (generic) kits
- The differences are **discontinuous** (binned distributions show clear separation; no smooth gradient)
- "Up to rank-3" — rank-4+ kits do NOT continue the monotonic increase (rare; may degenerate)

**Null (H0):** Damage AND WR are independent of rank classification.

**Procedure:**
1. Fit linear + pairwise + triple-interaction WR/damage model: M(v) ~ Σ α_i + Σ β_{ij} + Σ γ_{ijk}
2. Classify each kit in archive by rank (per BDI § 2.4):
   - rank-3: BDI_3 > 1.0 for at least one triple
   - rank-2: BDI_2 > 1.0 for at least one pair AND no rank-3 triple
   - rank-1: neither rank-2 nor rank-3 dominance
3. For each rank bin, compute mean damage + mean WR + variance
4. Statistical test: Kruskal-Wallis (3-group comparison) on damage; same on WR
5. If significant, follow with Mann-Whitney U pairwise: rank-3 vs rank-2; rank-2 vs rank-1

**Success criteria:**
- Kruskal-Wallis p < 0.05 for damage AND for WR
- Pairwise: rank-3 mean ≥ 1.2× rank-2 mean ≥ 1.2× rank-1 mean
- Discontinuity confirmed by visible distribution-separation (binned histogram check)
- **Optional ceiling check:** rank-4+ kits (if any in archive) do NOT continue the monotonic trend

**Stronger signal:** mean damage at rank-3 ≥ 1.5× mean damage at rank-2 → rank structure is dominant

**Tier 4 specific:** For Option A subset (kits where tier-4-skill shares mechanical signal with 2+ other skills), repeat the analysis. The Tier-4-shared-signal kits should preferentially cluster in rank-3 bin.

**Confirms:** the rank-classification structure of BDI is empirically real; build-defining is a discontinuous-step phenomenon, not gradient

**Author credit:** Matt 2026-05-21 evening framing (rank-discontinuity + damage+WR dual outcome)

**Non-interference:** read-only against archive; no impact on substrate composer or convergence loop.

---

#### H2 (PRIMARY) — Bimodal damage distribution for high-|τ| substrate-pair kits

**Hypothesis:** For kits whose substrate vector contains a high-|τ| substrate-pair (polar opposition, |τ| ≥ 0.7), the damage distribution is **bimodal** — one mode at high-damage (bridge-substrate present in vector) and another mode at low-damage / convergence-failure (no bridge present). Kits with no high-|τ| pairs have unimodal damage distributions.

**Predicts:**
- Damage histograms for high-|τ|-pair kits show two distinct peaks
- Damage histograms for no-high-|τ|-pair kits show single peak
- The high-damage mode in bimodal histograms is comparable to or exceeds the unimodal peak of plain kits
- The low-damage mode in bimodal histograms is significantly below the unimodal peak

**Null (H0):** Damage distributions are unimodal regardless of substrate-pair τ-properties.

**Procedure:**
1. Identify high-|τ| substrate-pairs from § 4.2 τ-table (or empirically-refined equivalent)
2. Partition archive kits:
   - Set H+B: contains high-|τ| pair AND bridge-substrate present
   - Set H-noB: contains high-|τ| pair AND NO bridge present
   - Set L: no high-|τ| pair
3. Compute damage histograms for each set
4. Bimodality test: Hartigan's dip test OR Gaussian mixture model fit (compare 2-component vs 1-component AIC)
5. Mean comparison: Mann-Whitney U on Set H+B vs Set L (high-damage mode test); Set H-noB vs Set L (low-damage mode test)

**Success criteria:**
- Bimodality detected in Set H+B ∪ Set H-noB combined (dip-test p < 0.05 OR 2-component GMM beats 1-component AIC by ≥ 10)
- Set H+B mean damage > Set L mean damage at p < 0.05
- Set H-noB mean damage < Set L mean damage at p < 0.05

**Stronger signal:** Set H+B mean ≥ 1.3× Set L mean AND Set H-noB mean ≤ 0.7× Set L mean → bimodality is sharp

**Tier 4 specific:** For Option A subset, the bridge-substrate is typically expressed via a Tier 4 keystone (per § 6.1: Tier 4 is the rank-completer, which often is also the τ-bridge for negative-τ substrate-pairs). Test: do kits with Tier 4 keystones acting as bridges show stronger bimodality than kits without?

**Confirms:** the τ-field's tension-resolution mechanism is empirically real; polar-opposite substrate-pairs are bimodal (legendary-tier OR failure-tier)

**Author credit:** Matt 2026-05-21 evening framing (bimodal sharpening of original τ-bridge hypothesis)

**Non-interference:** read-only against archive + τ-table + bridge-table; no impact on generation.

---

#### H3 (COMPLEMENT) — ω-field predicts β-magnitude

**Hypothesis:** Substrate-pairs with high mechanical-overlap (ω) have higher pairwise interaction coefficients (β) than substrate-pairs with low ω.

**Null (H0):** β-coefficients are uncorrelated with substrate-pair ω scores.

**Procedure:**
1. Compute ω for each substrate-pair in the v1 catalogue (using mechanical-signal-overlap analysis per § 4.1 — initial values from proposed table, refined empirically)
2. Compute empirical β for each substrate-pair from the H1 model fit
3. Compute Pearson correlation coefficient r(ω, β) across all pairs
4. Report r + p-value

**Success criterion:** r ≥ 0.5 with p < 0.05
**Stronger signal:** r ≥ 0.7 → ω is a strong predictor of β
**Confirms:** shared-mechanic amplification hypothesis (Case A from Matt's framing)

**Why this complements H1+H2:** without H3, BDI is descriptive but not predictive. H3 validates that ω-values can be USED to predict β before running the full model fit — i.e., the substrate composer can use ω-tables to bias toward high-BDI vectors without first generating the kits.

**Non-interference:** read-only against archive + ω-table; no impact on generation.

---

#### H4 (COMPLEMENT) — Rank-3 γ-coefficients dominate β-coefficients in signature builds

**Hypothesis:** A subset of substrate-triples have γ_{abc} magnitudes that dominate any of the pairwise β within the triple. These are signature builds.

**Null (H0):** γ-terms are not significantly larger than β-terms; rank-3 structure is absent.

**Procedure:**
1. Fit a model including triple-interaction terms: M(v) ~ Σ α + Σ β + Σ γ (against both damage AND WR)
2. For each substrate-triple, compute BDI_3 (per § 2.3): BDI_3 = |γ_{abc}| / max(|β_{ab}|, |β_{ac}|, |β_{bc}|)
3. Identify triples with BDI_3 > 1.0
4. Report the count + the top-10 highest-BDI_3 triples + their substrate identity

**Success criterion:** at least 5 distinct triples with BDI_3 > 1.0; these triples should correspond to genre-recognizable identities (cross-validate against proposed rank-3 table § 5.1 — e.g., Powder Hex-Cannon, Smoke-Vampire, Inferno-Knight)
**Stronger signal:** at least 10 triples with BDI_3 > 1.5 → rank-3 structure is rich

**Why this complements H1+H2:** H1 classifies kits into rank bins; H4 validates that the rank-3 bin is structurally distinct from rank-2 (γ dominates β within rank-3 triples). Without H4, "rank-3" might just be "rank-2 with extra noise"; H4 confirms genuine rank-3 structure.

**Tier 4 specific:** the top-BDI_3 triples should preferentially contain a Tier-4-keystone-class component (rank-completer per § 6.1). When W1.13 lands and true Tier 4 keystones exist, re-run H4 against the new archive (Option B); expect BDI_3 magnitudes to increase substantially.

**Confirms:** signature-build pattern is rank-3 γ-dominant (not just rank-2-stacked)

**Non-interference:** read-only; model-fit work; no impact on generation.

---

#### H5 (COMPLEMENT) — BDI correlates with cohesion-judge score

**Hypothesis:** Kits with high BDI (rank-2 or rank-3) receive higher cohesion-judge scores than kits with low BDI.

**Null (H0):** BDI and cohesion-judge score are uncorrelated.

**Procedure:**
1. For each kit in archive that has both a cohesion-judge score AND a substrate vector with measurable β/γ from H1/H4 fits:
   - Compute the kit's max-BDI (highest BDI_2 or BDI_3 in its substrate vector)
2. Compute Spearman rank-correlation r(max-BDI, cohesion-judge score)
3. Report r + p-value

**Success criterion:** r ≥ 0.4 with p < 0.05
**Stronger signal:** r ≥ 0.6 → math model and cohesion-judge are reading the same structure

**Data-availability caveat:** Cohesion-judge scores currently exist for the probe sample (N=10), R8 inverted arm (N≈11), S1 first-batch (N=11). Full archive does NOT have cohesion-scores. **H5 runs against this limited sample initially**; expanded execution waits for P5 cohesion-judge integration when production archive accumulates cohesion-scores at scale.

**Why this complements H1-H4:** H5 is the cross-layer validation. Without it, the math model (BDI) and the narrative model (cohesion-judge) are unverified-aligned. H5 confirms they read the same resonance through different sensors.

**Confirms:** mathematical and narrative models converge on substrate-architecture resonance

**Non-interference:** read-only against archive cohesion-judge scores; no impact on generation.

---

### 7.2 What the hive-mind does with the results

**If H1 + H2 confirm (PRIMARY tests pass):**
- Rank-discontinuity and bimodal-tension mechanisms are empirically real
- The substrate composer CAN optionally weight toward high-rank substrate vectors during generation (BDI-aware composer per § 8.2)
- Tier 4 keystone catalogue authorship (T4-B per protocol amendments) proceeds with rank-3-completion as explicit design target

**If H3 + H4 also confirm (complements pass):**
- ω/τ predictor tables (§ 4.1-4.2) are usable for generative biasing
- The full BDI formalism becomes operational at production scale
- P5 cohesion-judge prompt extension informed by BDI hints (priority 4 per p5-prompt-priorities doc) becomes high-confidence work

**If H5 confirms (post-P5 cross-layer):**
- Math model (BDI) and narrative model (cohesion-judge) are aligned
- The cohesion-judge can be informed by BDI predictions without overriding its judgment
- Architectural confidence in substrate-as-cohesion + BDI as a unified framework

**If any test fails:**
- The formalism is reframed or parked at that layer
- Lower-layer tests still inform — e.g., H1 confirm + H3 fail means "rank structure is real but ω is not the predictor" → seek alternate ω formulation
- The substrate composer's existing behavior remains the baseline
- No endless-loop risk: BDI never becomes a hard filter; tests are diagnostic

**Hive-mind teams that benefit from these results:** rocket (substrate composer extension + model-fit infrastructure); star-lord (P5 cohesion-judge prompt informed by BDI hints); gandalf (substrate-architecture work post-attribution; Tier 4 catalogue authorship); jack-ryan (process review on validity-of-empirical-procedure).

### 7.3 Pre-loading for Tier 4 skill-tree testing (the strategic intent)

The hypothesis tests are authored **NOW** so that when the team moves into skill-tree testing (W1.13 implementation territory; P1+ work), they have the measurement framework already specified. They do NOT have to invent the test design under deadline; they execute against this canonical reference.

**Specifically for Tier 4 skills:**
- H1 + H2's Tier-4-specific addenda direct the team to measure damage/WR against Tier 4 substrate-component relationships (Options A + C now; Option B post-W1.13)
- H4's Tier-4-keystone-class-component preference predicts that true mechanic-altering Tier 4 keystones (post-W1.13) will produce strong rank-3 γ-dominance
- The Tier 4 keystone catalogue authorship (T4-B) explicitly targets rank-3 completion (per § 6.1 + § 8.3) — the catalogue is informed by the empirical results

**Net effect:** the skill-tree-testing team enters their work with explicit predictions to validate or refute, not an open-ended "do skills synergize?" exploration. Discipline #11 (empirical inspection) honored at architectural boundary.

---

## 8. Connection to the substrate composer (generative use of BDI)

Once H1-H4 confirm, the substrate composer (W1.2-W1.6 territory) can extend its selection logic:

### 8.1 Plain composer (current behavior)

Selects substrate vectors via diversity-maintaining behavior (BC archive coverage; uniformity across substrate space).

### 8.2 BDI-aware composer (proposed extension; P1+ optional)

Adds an OPTIONAL bias term: substrate vectors with **predicted** high BDI (via ω + τ + bridge tables) receive additional selection weight on top of diversity-maintaining behavior.

**Safety property:** the composer still produces diverse coverage of the substrate space; high-BDI vectors are oversampled but low-BDI vectors are not excluded. **No endless-loop risk** because:
- Diversity maintenance has higher priority than BDI bias
- Vectors that can't converge (via multi-dim convergence per math note v1.1) are rejected via the standard reject-and-recompose pathway, NOT looped infinitely
- BDI bias is a weight, never a filter

### 8.3 Tier 4 catalogue authorship (T4-B; design-side)

The Tier 4 keystone catalogue (~30-50 keystones) is authored by gandalf + Matt with explicit rank-3 completion in mind: **each keystone in the catalogue is designed as the third leg of a known high-β substrate-pair**, producing a known rank-3 identity.

The catalogue authorship references:
- The high-β pair predictions in § 4.1-4.2
- The rank-3 identity predictions in § 5.1
- Genre canon (PoE keystones, D3 set bonuses, D4 capstones, isekai signature-mechanics)

---

## 9. Connection to the cohesion-judge layer

The substrate-as-cohesion validation probe (2026-05-21) returned 4.35 / 5.0 mean coherence, with the highest scores (5.0) on substrate-pairs that — by the BDI formalism — should have the highest β.

| Probe kit | Score | Predicted BDI structure |
|---|---|---|
| class_0007 (shadow_mage; drain + silence; zero contamination) | **5.0** | high BDI_2 on shadow + drain (rank-2 resonance) |
| class_0008 (physical_warrior; bleed + stamina + melee) | **5.0** | high BDI_2 on physical + stamina (uniquely-bound resource); auxiliary BDI on melee + arc geometry |
| class_0012 (earth_controller; root × 6 + totem) | **5.0** | high BDI_2 on earth + root + totem cluster (proto-rank-3) |
| class_0004 (wind_controller; vortex/knockback) | **4.5** | rank-2 BDI on wind + knockback geometry |
| class_0005 (lightning_controller; chain_lightning × 5) | **4.5** | rank-2 BDI on lightning + chain geometry |
| class_0016 (3-element contamination) | **3.5** | LOW BDI — no dominant β; no rank-2 resonance; identity fragments |

**Hypothesis (operationalized in H5):** the cohesion-judge implicitly detects resonance from mechanical signature. The 4.35 mean coherence at small sample is, by this hypothesis, the cohesion-judge measuring resonance present in the kits, not adding it via naming.

**Implication for P5 prompt-engineering:** the cohesion-judge can be *informed* by BDI predictions without being overridden. The P5 prompt extension (from the prompt-priorities doc) can include language like:

> *"When reading a kit's mechanical signature, look first for the dominant pairwise resonance (the substrate-pair whose mechanical signals share the most overlap). If a third substrate component (gear-archetype, trait-cluster, or capstone) closes the pair into a triple resonance, name the build at rank-3. If the pairwise resonance is strong but no triple-closer is present, name the build at rank-2. If no dominant resonance is detectable, return identity-fragmentation warning."*

This sharpens P5 priorities 2 (capstone identity alignment), 4 (gear-archetype recognition), and 5 (gear × element cross-coherence) by anchoring them to a single formal structure.

---

## 10. Implementation phases

| Phase | Scope | Owner | Timing |
|---|---|---|---|
| **BDI-A** | Author this doc (canonical reference) | gandalf | DONE (2026-05-21 evening) |
| **BDI-B** | ω-table + τ-table v1 (refine the proposed tables in § 4) | gandalf + Matt design call | Pre-P1; tomorrow's session if attribution lands clean |
| **BDI-C** | H1-H5 hypothesis test specs (this doc § 7) refined to executable form | gandalf + jack-ryan (process review) | P1 |
| **BDI-D** | Hive-mind executes H1-H5 against archive data | rocket (model fits) + legolas (analytical synthesis) + gandalf (review) | P1+ (overnight runs welcome) |
| **BDI-E** | Result review + decision: adopt BDI-aware composer (BDI-F) or park formalism | gandalf + Matt | post-BDI-D |
| **BDI-F** | (conditional) BDI-aware composer extension | rocket | P2+ |
| **BDI-G** | (conditional) P5 cohesion-judge prompt extension informed by BDI | star-lord | P5 |
| **BDI-H** | Tier 4 catalogue authorship using rank-3 framework | gandalf + Matt | Pre-P5 (parallel to gear-substrate v1 work) |

**Critical-path impact:** BDI-A through BDI-D are non-blocking diagnostic work. BDI-E is the gate; if results confirm, BDI-F/G/H integrate during their natural phase windows. If results don't confirm, the formalism parks and the existing composer + cohesion-judge architectures continue without modification.

---

## 11. Caveats — scientific posture

1. **This formalism is proposed, not derived from data.** The two field equations (ω, τ) and the BDI definition are theoretical scaffolds. The correlation against archive data is the test. Until H1-H5 run, treat this as hypothesis-grade, not theorem-grade.
2. **The ω-table and τ-table in § 4 are starting predictions.** They will need empirical calibration. The proposed values are designer-intuition + genre-precedent informed, not measured.
3. **The functional form (linear + pairwise + triple interaction model) is the simplest plausible model.** The real underlying structure may include log-transforms, hierarchical priors, or substrate-specific functional forms. Refine post-H1.
4. **BDI thresholds (BDI_2 > 1.0; BDI_3 > 1.0) are proposed; empirically calibrate.** The "right" threshold depends on the archive's distribution.
5. **Rank-3 is the practical ceiling for v1.** Rank-4+ may exist in the archive at long-tail; v1 work does not target rank-4 explicitly.
6. **The wizard's framing is metaphorical, not mystical.** "Resonance" is a useful name for "interaction-term dominance in the WR landscape." If the test confirms, the metaphor is empirically grounded. If it doesn't, the metaphor is reframed.
7. **No endless-loop risk** is structural, not just policy. BDI is a metric, not a filter; the composer's diversity-maintenance has priority; the convergence loop's reject-and-recompose pathway handles non-convergence at any substrate vector.

---

## 12. The mythic angle — why this matters beyond optimization

A class without resonance is a collection of mechanics. A class with resonance is an identity.

In every story tradition that touches the genre — Tolkienian fellowship-class identities (Aragorn's ranger-king dualism; Gimli's stoneworker-warrior fusion); isekai stat-system arcs (Rudeus's silent-precision; Jinwoo's shadow-monarch); the Diablo lineage (Frozen Orb Sorc; Pain Attunement Witch) — the build-defining moment is the moment the parts of the spirit speak to each other across the gap of their differences.

It is no accident that the highest-coherence kits in our probe were the kits where two substrate components share a deeper structural mode — physical-warrior's bleed+stamina+melee speak the same language of "fight with what your body is"; shadow-mage's drain+silence speak the same language of "take from the world to gain power." The math model and the narrative model converge on the same recognition: **resonance is identity.**

The formalism in this doc is, in the white wizard's voice, a measurement of what the genre has always known. Tools to count what we already feel. When a class is build-defining, you know. You name it without thinking. The math just gives us a way to point at *what* you knew, and to ask: how do we generate more of this?

**Reincarnated's substrate architecture, if the BDI hypothesis confirms, will be the first ARPG that designs its build-defining moments by formal mathematical structure rather than by accident of skill-tree branch.** The substrate-as-cohesion architecture (probe-validated this evening) is the necessary precondition. The BDI formalism is the next layer.

---

## 13. Cross-references

- `canonical/story/substrate-design-supplement-2026-05-21.md` — substrate identity framework + § 2.1 shadow-trade-off thesis (empirically confirmed by probe)
- `canonical/story/gear-as-substrate-2026-05-21.md` — gear-archetype as 4th substrate axis (timing revised this evening — see protocol amendment doc)
- `canonical/story/multi-dim-convergence-algorithm-2026-05-21.md` v1.1 — math note (§ 4 Tier 4 keystones; § 6 substrate-as-cohesion; § 6.5 probe verdict)
- `canonical/story/p5-cohesion-judge-prompt-priorities-2026-05-21.md` — P5 prompt-engineering work; § 8 above sharpens priorities 2/4/5 with BDI structure
- `agentic_orchestration/dispatches/2026-05-21-legolas-substrate-as-cohesion-empirical-validation-probe.md` — probe verdict 4.35 / 5.0; empirically supports resonance hypothesis at small sample
- `agentic_orchestration/p0-closure-note-2026-05-21.md` — P0 closure context
- `agentic_orchestration/hive-mind-state-evening-2026-05-21.md` — evening state-snapshot (this doc adds to § 3 "new design work landed")
- Genre references: PoE skill-tree keystones (canonical rank-3 examples); D3 set bonuses (canonical rank-3 examples); D4 paragon glyphs (canonical rank-3 examples); LE passive trees + masteries; Mushoku Tensei magic-system signature-builds

---

**Signed:** gandalf (story-and-design steward)
**For:** mathematical foundation of substrate-architecture work; testable formalism; pre-loaded hypothesis tests for hive-mind execution; canonical reference for Tier 4 architecture authorship + P5 cohesion-judge prompt extension + gear-substrate-as-substrate work.
