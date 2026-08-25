# galadriel — S2B tranche-2: payload-hypothesis test SPEC (Item 1) + occlusion-gate region repair MEASURED (Item 2)

**Author:** galadriel, 2026-08-25
**Invoked by:** knight-rider, on § 9 of `knight-rider/rulings/2026-08-25-a6-decline-ratified-contamination-is-one-arm-not-one-pair.md`
**Status:** Item 1 — test SPECIFIED, NOT RUN (per instruction). Item 2 — repair MEASURED, NOT ADOPTED.

---

## Item 1 — § 9.2 re-derived, and the payload hypothesis SURVIVES with two corrections

### 1.1 Re-derivation: § 9.2 is CORRECT

Operator opened at source (`s2b_xrow_rows37.py:202-215`), not read from the mint note. All five published row means reproduce to 4 dp. The no-`sig` column reproduces to 4 dp. Leave-one-arm-out reproduces to ~0.5 % (I re-standardise over the remaining 47 arms; rank order and conclusion identical): most influential arm is `single_target/fire@cathedral`, dropping it leaves **0.8013** against `circle`'s 0.2330 — **3.44×**. **Upheld.**

### 1.2 ⚑ But "four of five rows unchanged to 4 dp" is ARITHMETICALLY FORCED, not empirical

Z-standardisation is per-column. Deleting a column removes exactly its term from every pairwise distance. Where `significant_components` is constant within a row-and-stage cohort, that term is **identically zero by construction**. The result restates *"sig is row-constant within stage on four rows"* — already legible in the arms table. It is a valid check; it is **not independent evidence**, and it should not be weighted as such.

### 1.3 ⚑ THE FINDING: the mechanism is right in direction, wrong in its named descriptors — and `line` is a SECOND EFFECT, not a counter-example

Per-descriptor decomposition of the within-row within-stage null (mean squared z-gap, `sig` excluded):

| row | aspect | fill | maj/diag | largest_cf | radial_mean | radial_std | outer_shell | inner_core |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **single_target** | 0.013 | **0.201** | 0.061 | **0.158** | **0.343** | **0.277** | 0.014 | **0.144** |
| multi_projectile | 0.002 | 0.024 | 0.028 | 0.010 | 0.016 | 0.053 | 0.053 | 0.005 |
| **line** | **0.036** | 0.004 | 0.010 | **0.111** | 0.006 | 0.004 | 0.000 | 0.022 |
| melee_arc | 0.002 | 0.008 | 0.024 | 0.005 | 0.009 | 0.015 | 0.009 | 0.010 |
| circle | 0.000 | 0.012 | 0.009 | 0.004 | 0.004 | 0.003 | 0.025 | 0.000 |

1. **`outer_shell_frac` is named in the mechanism and does not participate.** It contributes 0.014 to `single_target`'s null. In RAW units its within-row dispersion on `single_target` is **0.0057 — the second most stable in the corpus**, below `circle`'s 0.0098 and `multi_projectile`'s 0.0126. It is the one descriptor with a **positive** payload slope (+0.075). The mechanism as stated ("`fill_of_bbox` / `inner_core_frac` / `outer_shell_frac` wobble structurally at 1,700 px") **over-predicts on one of its three named terms.**
2. **`line`'s null has a DIFFERENT profile entirely** — carried by `largest_component_frac` (0.111) and `aspect_major_minor` (0.036), with the radial pair at ~0.005. Its raw aspect dispersion is **0.1510, the largest single raw dispersion anywhere in the corpus, 8.6× `circle`'s.** `line` is not a failed instance of the payload mechanism; it is **genuine inter-element shape variation superimposed on a smaller payload effect.** ⚑ **The one inversion KR flagged as evidence against the hypothesis is explained and does not count against it.**

### 1.4 ⚑ The scaling law — the hypothesis is quantitatively SHARPER than its author claimed

Regression of log(raw within-row dispersion) on log(median payload), five rows, then re-run excluding `line`:

| descriptor | slope (5 rows) | r | slope (excl. `line`) | r | ST/circle ratio |
|---|---:|---:|---:|---:|---:|
| **radial_std** | **-0.484** | -0.863 | **-0.492** | **-0.984** | **8.79** |
| **radial_mean** | **-0.446** | -0.803 | **-0.452** | -0.866 | **8.92** |
| inner_core_frac | -0.599 | -0.898 | -0.596 | -0.913 | 19.10 |
| largest_component_frac | -0.400 | -0.745 | -0.391 | -0.874 | 5.85 |
| aspect_major_minor | -0.374 | -0.688 | -0.362 | **-0.944** | 5.60 |
| fill_of_bbox | -0.313 | -0.671 | -0.321 | -0.824 | 4.30 |
| major_over_diag | -0.153 | -0.841 | -0.156 | **-0.989** | 2.02 |
| **outer_shell_frac** | **+0.075** | +0.117 | +0.057 | +0.278 | **0.59** |

**Counting noise predicts slope = -0.5.** `radial_std` (-0.492) and `radial_mean` (-0.452) sit essentially on it, and `radial_std`'s `single_target`/`circle` dispersion ratio is **8.79 against √73.5 = 8.57**. That is a numeric match, not an analogy. **The mechanism is 1/√n counting noise concentrated in the RADIAL moments — not generic ratio wobble across all eight descriptors.**

### 1.5 THE TEST I SPECIFY — synthetic is not merely acceptable, it is the CORRECT instrument

**On KR's worry (synthetic blobs lack the faint-halo structure):** he is right that they lack it and **it does not matter here.** The halo mechanism is the `0.01·n` significance-gate mechanism, and it drives **`significant_components`** — which is **excluded from the eight descriptors under test.** The five descriptors carrying `single_target`'s null are geometric moments of the pixel cloud; their size-dependence is a property of **discretisation**, not of halo.

**On KR's decimation test — I recommend AGAINST it as specified.** Random decimation to ~1,700 px destroys connectivity, which changes `largest_component_frac` structurally and is **not the physical situation.** The physical situation is a mask that is smaller *on screen*, not a mask with pixels randomly deleted. The corpus-side operation should be **area-downscale + re-threshold**, which preserves shape and connectivity.

#### T-1 — PRIMARY. Synthetic. Zero corpus data in the loop. No pre-registration hazard. Runnable now.

Rasterise a fixed parametric shape family at a ladder of linear scales giving n ∈ {1.4k, 2.7k, 5.4k, 11k, 22k, 128k} — **the corpus's own payload ladder.** At each rung generate k = 4 "element arms" that are the SAME shape under a small fixed perturbation (±2° rotation, ±1 % scale — the magnitude of genuine inter-element variation). Compute the eight descriptors, z-standardise across the whole synthetic set, compute within-rung mean pair distance.

- **CONFIRMS if:** within-rung null falls monotonically with n, slope ≈ -0.5 in the radial moments, and the 1.4k rung reads ~3-8× the 128k rung.
- **REFUTES if:** the null is approximately flat across rungs. Then `single_target`'s elevation is a property of its **shape** or of **genuine element variation**, and the payload hypothesis is dead.
- **Also discriminates:** if `outer_shell_frac` alone stays flat or rises, § 1.3's correction is confirmed independently.
- **Cost:** ~60 lines numpy, minutes. **No corpus data. No effect changed. No A-6 null touched.**

#### T-2 — CONFIRMATORY. Corpus. ONLY after jack-ryan's D3 pre-registration.

Area-downscale (**not** decimate) the retained `circle` masks to each rung of the same ladder, re-threshold at 50 % coverage, recompute the eight descriptors, re-run the within-row null. Confirms if `circle`'s null rises toward `single_target`'s as n falls.

**⚑ Why the order is load-bearing, and this is the point of the whole spec:** T-1 answers the question with no hazard at all. If T-1 **refutes**, T-2 is never needed. If T-1 **confirms**, T-2 becomes *corroboration of an already-established mechanism* rather than *the diagnostic that establishes it* — which materially weakens the pre-registration concern, because **the mechanism will not have been learned from the scored corpus.** The hazard is not "touching the corpus"; it is "learning the mechanism from the corpus you then score." T-1 removes that, whatever jack-ryan rules.

### 1.6 Correction to KR's closing note on the second `sig ≥ 3` instance

`multi_projectile_count1@cathedral` (1,757 px, `sig = 4`) is **consistent with my `0.01·n` gate finding and NOT with the payload-scale mechanism KR is testing** — because `significant_components` is **excluded** from the eight-descriptor null that the payload mechanism explains. **Two distinct mechanisms, both keyed to small n, must not be pooled as evidence for one hypothesis.** It is a second instance of the *gate* mechanism. It is silent on the *payload* mechanism.

### 1.7 Standing

**R-1 (`N_eff = 1/Σfᵢ²`), R-2 (persistence-weighted count), R-3 (angular dispersion) remain PROPOSED and UNSCORED.** Ordering unchanged. Nothing in this note scores them.

---

## Item 2 — occlusion-gate region: REPAIRED and MEASURED. ⚑ **The verdict DOES move, and it moves PASS → FAIL on both corpora.**

**Artifacts:** `reincarnated-godot/scripts/wwcr_occlusion_region_audit.py`, output at `reincarnated-godot/harness_logs/wwcr_2026-08-25-region-audit/region_audit.txt`.

### 2.1 Why a separate script rather than an edit to the scored gate

KR authorised the repair on the ground that this is *"a gate whose verdict does not move when it is fixed."* **The first half of his premise is true and the second half was never established.** drax measured the **defect** (62,048 of 62,301 px sky); nobody measured the **repair**, because the repair did not exist. So the scored gate is left **byte-identical** and the repair is measured beside it. Whether the clean-room arm of a live A/B may re-score itself post-hoc is the licence-asymmetry question drax routed to gandalf, and it is not mine to pre-empt by editing the instrument.

### 2.2 The root defect is `actor`, not the complement

```python
floor = np.median(control.reshape(-1,3), axis=0)
actor = (np.abs(control - floor).mean(axis=2) > ACTOR_THRESHOLD)
```

This reads **"differs from the floor colour"**, not **"stands off the floor."** The background void above the ground plane's far edge is *darker* than the floor, therefore differs, therefore is admitted as actor. The fixed 260 px frame-centre window then cannot exclude it, so the entire void lands in `enemies`. **Two independent errors that compose:** a content-blind region test AND a frame-relative window. Repair: (1) an actor pixel must be **brighter** than the floor; (2) split caster from enemies by **connected-component identity**, not by a pixel box.

### 2.3 ⚑ Results — thresholds NOT re-tuned (both constants carried verbatim)

| corpus | region | lower excess | enemy excess |
|---|---|---|---|
| `wwcr_2026-08-24` (mint) | OLD (scored) | 1.78 % **PASS** | 0.01 % **PASS** |
| `wwcr_2026-08-24` (mint) | **NEW (repaired)** | **5.47 % FAIL** | **23.01 % FAIL** |
| `wwcr_2026-08-25` (HEAD) | OLD (scored) | 1.73 % **PASS** | 0.00 % **PASS** |
| `wwcr_2026-08-25` (HEAD) | **NEW (repaired)** | 1.38 % PASS | **26.98 % FAIL** |

Denominators: enemy **50,840 px → 1,705 px**; caster lower-body **1,809 px → 535 px**. The component ledger resolves cleanly to **caster (972 px) + exactly four mobs (497 / 454 / 421 / 333 px)**, at both corpora, confirming the region identification.

**The mint-corpus lower-body flip (1.78 → 5.47) is drax's own predicted failure realised:** the old `lower` region was the caster **pooled with the mobs** (1,809 px), so `hip_row` was derived from a pooled bbox. He named the risk in the docstring; it is now measured.

### 2.4 ⚑ THE DISPOSITION — and it is NOT "the row fails"

**The 20 % bar was calibrated against a denominator that was 99.6 % sky. A bar set against a degenerate region does not transfer to a repaired one.** The repaired FAIL is therefore **as uninterpretable as the original PASS was** — and saying so is the whole finding. This is the same family as my own S-A3 withdrawal and the register-2 bloom gate: **a bar whose difficulty is set by the thing it measures.** ⚑ **Third instance of that class, and it is now a class.**

**What IS newly known, and it is a real measurement that did not previously exist:** at `05-sustain`, **~27 % of true enemy-silhouette pixels change under the effect**, on both corpora. That is the "cannot read the enemies through the effect" failure the WWCR row exists to correct, and the gate as scored was **structurally incapable of seeing it** — `enemy = 0.00 %` at every live mark on the HEAD corpus, on a zero-pixel denominator.

**Recommendation:** the repaired region is adopted **only together with a re-derived bar**, and the bar is derived **before** the repaired number is looked at again. I am not deriving it here — that is a pre-registration act and it belongs with jack-ryan's D3 work, not beside a number I have already seen.

### 2.5 Sibling-gate scan — NO FOURTH IN THIS CLASS

All eleven `*_gate.py` plus `quiltfix_diff.py` and `s2b_stagemetrics.py` audited for the two composing defects.

- **Frame-relative pixel-box regions:** `wwcr_occlusion_gate.py` is the **only** instance in the corpus. `cj_gate.py:152` and `sa_gate.py:209` use boxes, but both derive them from `to_screen(wx, wy)` — **world-projected** — and both return absolute counts with **no denominator**. Immune twice over.
- **Complement-defined regions:** `quiltfix_diff.py:138` (`changed & ~mask`) is an absolute leak **count against a hard bar of zero** — no denominator, immune by construction. `s2b_stagemetrics.py:238-243` is bounded by `authored`, the effect's own pixels. `s2b_rows12_gate.py:437` (`m_all AND NOT m_man`) is a set-difference of **two content-derived masks measured against the same control**, and it **publishes `px_accounting` for all three regions**.
- **Region-denominated fractions:** `s2b_rows37_gate.py:678` (`authored_frac_of_caster_region`) divides by `caster_region`, which is derived from **the rig's foot and head unprojected through the capture camera by the engine**.

⚑ **The counter-example is the most useful thing in the scan, and it is by the same author.** `s2b_rows37_gate.py` and `s2b_rows12_gate.py` both (a) derive regions from content or engine geometry and (b) **publish the region's own pixel count beside the fraction taken over it.** `wwcr_occlusion_gate.py` did neither. **The defect is not a habit — it is confined to the one gate that hardcoded a box and did not print its denominator.** The absence of that one printed integer is what hid 62,048 px of sky for an entire run. **Publishing the denominator beside every region-fraction is the cheap general prophylactic**, and it is already drax's practice everywhere else — which is why I route it to jack-ryan as a *ratification of existing practice*, not a new discipline.

---

*Committed by galadriel 2026-08-25. § 1.1's re-derivation was performed against the operator at source before any new figure was derived from it. § 1.3-1.4 are arithmetic on published descriptor values in `xrow.json`'s `arms` array — the same class as § 9.2, deriving no new mask measurement and touching no A-6 null population. § 2's repair changes no scored artifact; both gate thresholds are carried verbatim and neither was re-tuned.*
