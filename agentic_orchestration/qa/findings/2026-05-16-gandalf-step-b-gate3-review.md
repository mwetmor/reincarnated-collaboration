# Finding — 2026-05-16 — gandalf Step B Gate-3 Review (vendor screening + Q-PRI-2 collapse review)

**Reviewer:** gandalf
**Severity:** **PASS-WITH-AMENDMENTS** (both tracks). Step B HELD gate is released; specific Tier-1 list + Q-PRI-2 verdict + 3 minor amendments to the Step B dispatch spec follow.
**Targets reviewed:**
1. Legolas vendor-discovery sweep output (`research/knowledge/asset-catalogues/2026-05-16-vendor-discovery-sweep.md`)
2. Elrond Step A methodology smoke test (script + observed output at k=8: silhouette=0.277, purity-mech=0.71, purity-reg=0.74, purity-cat=1.00, max-share=0.43, singletons=3)
3. The 7-family `MECHANIC_FAMILIES` collapse decision in `research/scripts/step_a_methodology_smoke_test_2026_05_16.py`

**Tracks:** (a) vendor screening for Step B Tier-1 list; (b) Q-PRI-2 design review on the mechanic-family collapse choice.

---

## Verdict (one line)

**PASS-WITH-AMENDMENTS. Tier-1 list finalized at 9 vendors. All 4 sweep candidates accepted (3 PASS, 1 PASS-WITH-CAVEAT). 7-family mechanic collapse verdict: ACCEPT-WITH-AMENDMENT-TRIGGER — lock for Step B but explicit revision trigger flagged for the post-Step-B emergent-grouping analysis. 3 dispatch-spec amendments recommended (visual inspection deferral for low-quality candidates; explicit per-vendor mechanic-tag harvest; kinetic-VFX-vendor mechanic-family pre-extension).**

---

# TRACK (a) — Vendor candidate screening

## A.1 Per-candidate screening against binding criteria

### Frostwindz (full catalogue, beyond the lightning-only baseline entry) — **PASS**

Inclusion criteria:
1. **Empirical-research-base eligibility:** ✓ now appears in vendor-discovery sweep with substrate-breadth evidence.
2. **Substrate-variance contribution:** ✓✓✓ — triple-qualifies. (a) ships Deathbringer (death/necrotic), Blood Knight (blood/life-drain), Starcaller (cosmic/stellar), Dark Mage + Warlock (dark-arcane / void-adjacent) — five labels distinct from Pimen's 9; (b) 13 packs spanning multi-element breadth; (c) class-archetype packs (Warrior/Paladin/Rogue/Blood Knight) carry weapon-strike/slash kinetic coverage.
3. **License clarity:** ✓ "personal and commercial; no redistribution/resale" confirmed on Deathbringer + Blood Knight pages; "No generative AI" confirmed. Pricing: $6.50/pack; $39 bundle.

Rejection criteria: none triggered.

**Tier-1 inclusion: YES — high-priority.** Closes the necrotic/death substrate gap that has been the largest standing absence in the catalogue. Cosmic substrate is a Tier-3-novelty addition. Class-archetype packs provide kinetic-VFX evidence orthogonal to CodeManu's pure-impact specialization.

**Per-vendor crawl-depth note:** the 13-pack catalogue should receive **exhaustive crawl on all substrate-distinct packs** (Deathbringer, Blood Knight, Starcaller, Dark Mage, Warlock — 5 distinct substrates); sampled on substrate-redundant packs (Fire Mage, Frost Knight, Priest, Paladin overlap Pimen-fire/Pimen-ice/Pimen-holy). The 404 flag (see A.2.1 below) shapes the substrate-distinct list at crawl time.

### Pixogen (AFGameAssets) — **PASS-WITH-CAVEAT**

Inclusion criteria:
1. **Empirical-research-base eligibility:** ✓ Pixi.js-compatible 64x64 PNG spritesheets.
2. **Substrate-variance contribution:** ✓✓ — qualifies on (a) Void as discrete label distinct from Pimen's Dark + Technology VFX as fully novel substrate with no parallel in existing research; and (b) 8 elemental categories + 3 mechanical categories = 11 distinct effect-type labels (>7 threshold). Attack Slash also addresses (c) kinetic.
3. **License clarity:** ⚠ "License of AFGameAssets" — terms in downloadable file, not readable from pack page. "No generative AI" confirmed on tag.

Rejection criteria: none triggered, contingent on license caveat resolving.

**Tier-1 inclusion: YES with license-verify-at-crawl-time gate.** The Void distinction from Dark is **genuinely substrate-load-bearing** — Pimen's "Dark" reads dark-arcane/shadow-magic; Pixogen's "Void" reads spatial-absence (Black Hole, Portal). These are not synonyms; they're different cosmological registers. The Technology substrate is even more novel — no existing source ships it, and it cracks open a substrate category the cipher-width analysis should not assume away (per § 6.2 of strategy doc, the substrate width is *discovered*, not picked).

**Per-vendor crawl-depth note:** all 11 categories appear substrate-distinct given the novelty; recommend **exhaustive crawl across full pack** since the per-pack structure is one monolithic 636-sprite asset (substrate-redundant sampling doesn't apply at sub-pack granularity for a single SKU).

**License-caveat operational handling:** legolas surfaces license terms in crawl JSONL per Pimen schema; if terms prove incompatible (e.g., revealed to forbid commercial use), vendor flips to FAIL post-hoc and the substrate evidence enters the cross-vendor inventory with `license_blocker: true` — the substrate data is still informative for cipher-width analysis even if acquisition is blocked.

### CodeManu — **PASS-WITH-CAVEAT**

Inclusion criteria:
1. **Empirical-research-base eligibility:** ✓ commercial source; Pixi.js-compatible PNG spritesheets.
2. **Substrate-variance contribution:** ✓ — qualifies on (c) kinetic-VFX coverage. 44 impact/hit animations is the deepest single-vendor kinetic catalogue in the sweep. Blood Effects Vol.1 (if available) adds blood/wound substrate evidence parallel to Frostwindz's Blood Knight.
3. **License clarity:** ✓ "personal and commercial purposes; no credit required" confirmed; "No generative AI" confirmed. $4.95/pack.

Rejection criteria: none triggered.

**Tier-1 inclusion: YES.** Directly addresses the Q5 kinetic-VFX inclusion clause from the commission. Pimen's Hit Spark + Buff/Debuff packs are surface-adjacent but not true weapon-trail/slash specialists; CodeManu is the kinetic-VFX-specialist anchor the commission explicitly called for.

**Per-vendor crawl-depth notes:**
- 100x100px canvas is wider than the 64x64 standard. Flag for drax wiring-track at consumption time, **not at crawl time** — substrate-evidence quality is unaffected by canvas size. Legolas should record canvas dimensions per Pimen schema and surface them in the per-vendor findings summary; drax track picks up the atlas-padding question downstream.
- Blood Effects Vol.1 404 (see A.2.2) means blood-substrate evidence may have to lean on Frostwindz's Blood Knight alone if the page is dead.

### Fellor (BitBlast Studio) — **PASS-WITH-CAVEAT**

Inclusion criteria:
1. **Empirical-research-base eligibility:** ✓ commercial source; 64x64 PNG; "No generative AI" confirmed.
2. **Substrate-variance contribution:** ✓ — qualifies on (a) **Crystal substrate is genuinely novel** (gem/mineral magical resonance — no parallel in existing Tier 1-3 vocabulary). Poison addresses palette-register variance from Pimen's Acid (acid = chemical-corrosive; poison = biological-venom registers differently even when mechanically overlapping). Seven distinct substrate packs total.
3. **License clarity:** ✓ "Free for personal and commercial use; no redistribution/resale; credit optional" confirmed on Poison and Crystal pages.

Rejection criteria: none triggered.

**Tier-1 inclusion: YES with quality-floor-verify-at-sample-phase gate.** Crystal substrate is the kind of cosmological-novelty addition that the cipher-width framework (per § 6.2) wants the substrate-layer to discover. A "no-grouping-survives → canonical-four cipher remains operative" outcome would still benefit from Crystal as a per-season vocabulary slot for crystal-themed cosmologies; a "3-5 robust groupings emerge" outcome may bind Crystal into one of those groupings (crystal-mineral substrate could pair with earth/stone in a geological-grouping; or with arcane/aether in a metaphysical-resonance grouping).

**Per-vendor crawl-depth note:** newer creator (~2 years experience); pack-depth of 8 effects/pack vs Pimen's 10-22 means the substrate-evidence-per-pack is thinner. Recommend **exhaustive crawl on substrate-distinct packs (Crystal, Poison, Smoke)** but flag quality-floor uncertainty in the per-vendor findings summary so elrond's downstream coherence analysis can weight Fellor evidence appropriately.

## A.2 Flag triage outcomes

### A.2.1 — 404s on Frostwindz Starcaller / Warlock / Paladin pack pages

**Triage: ACCEPT WITH CRAWL-TIME VERIFY.** The vendor profile page evidence is sufficient for inclusion decisions; substrate claims for the 404'd packs are inferred but plausible (Starcaller as cosmic; Warlock as void-adjacent; Paladin as holy/light — consistent with the vendor's class-archetype packaging pattern).

**Legolas crawl-time instruction (recommend amending to dispatch):** at metadata-only pre-pass for Frostwindz, retry the 404'd pack URLs with alternate slugs (e.g., `frostwindz.itch.io/vfx-starcaller`, `/starcaller-vfx`, etc.) and inspect the vendor's collections/sale pages for current URLs. If pages remain unreachable, record `pack_page_404: true` in the JSONL and treat substrate claims as `unverified_inferred_from_vendor_profile` in the per-vendor findings summary. The substrate evidence is still informative even if pack-level metadata is incomplete.

If Starcaller specifically proves unreachable post-retry, the cosmic substrate falls back to Pimen's holy + per-season vocabulary; not a blocker for cipher-width analysis, but a flag for the post-Step-B inventory.

### A.2.2 — Pixogen license file unreadable from pack page

**Triage: ACCEPT WITH CRAWL-TIME VERIFY.** Already covered in A.1 Pixogen entry. Legolas downloads and reads the 18kB license file at crawl time; records full terms in JSONL. If terms forbid commercial use, vendor flips to license-blocker status post-hoc; substrate evidence stays in the inventory with the blocker flag.

**Dispatch-spec amendment recommendation:** add a per-vendor "license-verification artifact" requirement to the crawl methodology — vendors whose license terms are not readable from public web pages require the actual license artifact (PDF, TXT, license-file download) to be fetched, inspected, and the terms summary recorded in the per-vendor findings summary. Otherwise license-clarity criterion #3 is met only nominally.

### A.2.3 — Psychic / mental / dream substrate gap remains

**Triage: ACCEPT AS-IS; PSYCHIC SUBSTRATE IS A CONFIRMED ABSENCE; DOCUMENT IT.**

Legolas's sweep concluded no specialist psychic-VFX vendor exists in the discoverable pixel-art-VFX community. This is consistent with: (i) the genre-precedent finding from prior research that psychic effects in shipped ARPGs (Diablo IV Necromancer's curse magic; PoE's chaos damage; Last Epoch's Necromancer/Acolyte trees) are typically rendered via **dark-purple-magic VFX with psychic-themed casting animations**, not as a structurally distinct visual substrate; (ii) the cipher-width framework's "substrate is discovered, not picked" principle (per § 6.2 of strategy doc) — if no vendor ships a psychic substrate, the substrate layer doesn't have one, and per-season vocabulary work for psychic-themed seasons (if/when) draws from existing substrates (dark, arcane, void) with per-season-vocabulary naming providing the psychic register.

**Cross-substrate composition path:** psychic-themed per-season vocabulary can compose from Pimen's Dark + Pimen's Buff/Debuff (status-effect surface) + Pixogen's Void (spatial-absence register) + Frostwindz's Dark Mage (dark-arcane). The cosmological register "psychic" is achievable through naming + cosmological framing without a dedicated visual substrate. This is the same pattern by which Diablo IV's Necromancer Curses (a psychic-coded mechanic) ship without a "psychic" VFX substrate — they share visuals with dark/blood-arcane.

**No further action.** Psychic substrate stays on the "confirmed absent at the catalogue layer; addressable at the per-season vocabulary layer" list. If a future post-Phase-0 catalogue sweep surfaces a psychic specialist, treat as Dispatch-1-class candidate at that point.

## A.3 The finalized Tier-1 list

| # | Vendor | Source | Inclusion-criterion satisfied | Substrate contribution headline | Status |
|---|---|---|---|---|---|
| 1 | **Pimen** | baseline (already crawled) | (a)+(b) | Substrate reference: 9-element + status + impact + character/enemy (paid tier-03 hand-drawn-pixel anchor) | ALREADY CRAWLED |
| 2 | **ansimuz** | baseline | (b) | Retro-band complementary; multi-element breadth (Free Magic Pack 9 + Magic Pack 4) | Tier-1 PASS |
| 3 | **Brackeys VFX Bundle** | baseline | (c) | Free baseline; impact/burst general-purpose | Tier-1 PASS |
| 4 | **CraftPix** | baseline | (a)+(b)+(c) | Vector + niche-mechanic (petrification, charm, midas, starfall); weapon-trail/slash coverage | Tier-1 PASS |
| 5 | **CreativeKind** | baseline | (b) | Hand-drawn-pixel different sub-register (paid hand-drawn-pixel spell sets — Water, Earth, Color, Magic) | Tier-1 PASS |
| 6 | **Frostwindz (full catalogue)** | sweep | (a)+(b)+(c) | **Death/necrotic + blood/life-drain + cosmic/stellar** (5 distinct novel substrates); class-archetype kinetic coverage | Tier-1 PASS |
| 7 | **Pixogen (AFGameAssets)** | sweep | (a)+(b)+(c) | **Void (distinct from Dark) + Technology (fully novel)**; 8 elemental + 3 mechanical | Tier-1 PASS-WITH-CAVEAT (license) |
| 8 | **CodeManu** | sweep | (c) | **44 impact/hit kinetic animations**; deepest kinetic-VFX vendor; possibly blood substrate | Tier-1 PASS-WITH-CAVEAT (100x100 canvas; blood 404) |
| 9 | **Fellor (BitBlast Studio)** | sweep | (a) | **Crystal substrate (fully novel)** + Poison palette-register variance | Tier-1 PASS-WITH-CAVEAT (quality-floor newer creator) |

**Total: 9 vendors.** Within the 6-10 expected range from the commission. Pimen is included as substrate reference (already crawled per `research/catalogue/pimen/full-2026-05-16.jsonl`); the 8 remaining vendors are net-new crawl work for Step B.

**Excluded from baseline expected-survivors list:**
- **Pipoya** — baseline lists Time Magic, Warp Portal, HEX Shield, Light Pillar. These are Tier-2 niches per the existing research file. Substrate contribution is the Time/Warp register pair, which IS substrate-distinct from Pimen's 9 (no time/warp coverage in Pimen). **Recommend re-including Pipoya as vendor #10** if knight-rider deems the 10-vendor ceiling acceptable; if 9-vendor list is preferred, Pipoya's Time/Warp substrate can be sampled at consumption-time via existing baseline research without full crawl. **My recommendation: include Pipoya as vendor #10.** Time/Warp is a substrate the cipher-width framework should not assume away — a time-themed grouping is a genre-precedented outcome (PoE has Temporal Chains; D2 had Bone Spirit's gravitational pull; Pipoya's Time Magic gives the visual substrate).
- **Foozle, unTied Games, Elthen, ppeldo, LuizMelo, OpenGameArt** — baseline lists these as single-pack or character-leaning vendors. Either substrate-redundant with already-included vendors or character-only (per Q4 out-of-scope). Recommend addressing at the post-Step-B follow-on character-track sub-commission per the Pimen sample design review's flag.

**Revised final Tier-1 list with Pipoya included: 10 vendors.** Within the commission's 6-10 ceiling.

---

# TRACK (b) — Q-PRI-2 mechanic-family collapse design review

## B.1 The collapse decision under review

`MECHANIC_FAMILIES` in `step_a_methodology_smoke_test_2026_05_16.py:73-81`:

| Family | Members |
|---|---|
| `buff-debuff-status` | buff, debuff, status-effect, magic |
| `ambient-environmental` | ambient, environmental |
| `smoke-dust` | smoke, dust |
| `impact-burst` | impact, explosion, hit-effect, muzzle-flash |
| `projectile-bullet` | projectile, bullet |
| `melee-slash` | slash, thrust, cutting, smear |
| `heal` | heal, healing |

22 fragmented mechanic-leaning tags from the Pimen catalogue collapsed to 7 families.

## B.2 (b.1) — Form-bias strategic-axis context: does the collapse preserve load-bearing distinctions?

**Verdict: MOSTLY YES, with one bordering concern.**

The form-bias work's load-bearing mechanic-family distinctions (per the cipher-width framework + the three-layer model in § 6.1/6.2 of strategy doc) are:

| Form-bias-relevant distinction | Preserved in 7-family collapse? | Notes |
|---|---|---|
| **Kinetic vs spell** | YES — `melee-slash` separated from `impact-burst` separated from `projectile-bullet` separated from `buff-debuff-status` | The kinetic/spell axis is preserved cleanly. Per Q5 inclusion clause, this is the core distinction Step B is set up to surface. |
| **Direct-damage vs ailment (status)** | YES — `buff-debuff-status` is its own family separate from kinetic/impact families | The control-orientation axis (per role-orientation-taxonomy memory note) maps to buff-debuff-status family for control/support skills. |
| **Aura vs instant** | PARTIAL — `ambient-environmental` captures aura-like (sustained-area) effects; `impact-burst` captures instant. **But:** the catalogue's `buff-debuff-status` packs likely include both aura-type buffs (e.g., persistent damage-aura) and instant buffs (e.g., heal). The collapse may merge these. | **Concern flagged below.** |
| **Projectile vs melee vs AOE** | YES — three distinct families (`projectile-bullet`, `melee-slash`, `impact-burst`) | Geometry-palette discussion (per memory note `project_geometry_palette.md`) carries the 16-type active palette; the 3-family kinetic/projectile split maps cleanly to geometry families. |
| **Heal as distinct family** | YES — `heal` is its own family | Heal is mechanically distinct (positive-magnitude resource manipulation) per role-orientation-taxonomy support-class definition. Correct as standalone. |
| **Cipher per-season vocabulary mechanical signatures** (per doc 37 § 6.2 Position (ii)) | INDIRECT — the 7-family vocabulary is upstream of per-season vocabulary; the per-season vocabulary work re-derives mechanical signatures from cipher slot architecture, not from these families directly | Coupling is design-architecturally loose at this layer; the collapse choice doesn't constrain per-season vocabulary derivation. |

**Concerning gap: aura/sustained-area effects.**

The current `buff-debuff-status` family conflates *aura-mechanic* effects (persistent area-of-effect application) with *instant-application* effects (one-shot buff applied at cast time). This is a load-bearing distinction for the form-bias work because:

- Aura effects map to the *support* and *control* role-orientations differently than instant buffs do (per role-orientation-taxonomy: support is gated to multi-actor contexts; auras are how support manifests visually)
- Per § 6.1 of strategy doc, the grouping-layer's role-orientation-coverage filter requires aura vs instant distinction for the "active grouping admits damage / control / hybrid orientations" criterion
- The B14.5 sidecar findings (per memory note) surfaced controllers/mages as highest convergence-iteration archetypes — control mechanics are load-bearing for engine balance work

**However:** the catalogue's Pimen substrate may not yet have enough aura-vs-instant evidence to support the distinction. The pre-inventory shows 9 of 22 mechanic-tagged assets carry buff/debuff/status-effect tags simultaneously (the same set of assets carrying all three tags per § 5.2 Q-SHAPE-3 of pre-inventory). This is a structural indication the Pimen vendor doesn't differentiate aura-vs-instant in their own tagging.

**Recommendation:** keep the 7-family collapse for Step A methodology validation (it has done its job — proven the methodology produces coherent groupings). Flag aura-vs-instant as the **specific revision-trigger condition** for post-Step-B re-collapse. See B.4 below for the trigger condition spec.

## B.3 (b.2) — Forward-compatibility with Step B's 5-10× input

**Verdict: NEEDS PRE-EXTENSION before Step B fires. Two specific gaps.**

The 7 families cover Pimen's 22 fragmented tags. Step B will introduce new mechanic vocabulary that the existing 7 families either don't cleanly absorb or actively misclassify. Specifically:

### Gap 1 — Necrotic/decay/blood substrates are *element-like substrates*, not mechanic-families

Frostwindz's Deathbringer, Blood Knight, Dark Mage; CodeManu's Blood Effects. These are **element-like substrate labels** (per the strategy doc's § 6.1 substrate-layer definition), not mechanic-families.

**Risk:** if legolas/elrond tag these vendors' assets with mechanic-leaning tags like "necrotic-cast", "blood-strike", "death-ray" at extraction time, the family collapse may force them into `buff-debuff-status` (because death/decay reads as a debuff family) or `impact-burst` (because explosions of necrotic energy read as bursts), erasing the substrate-distinct signal.

**Recommendation:** Step B's crawl methodology should explicitly **separate substrate-tags from mechanic-tags at the extraction layer**. The current Pimen catalogue does this for elements (via `pimen-element:` namespace) but doesn't do it for mechanic-vocabulary. New vendors' mechanic-leaning vocabulary should be tagged with a vendor-namespaced prefix (e.g., `frostwindz-substrate:necrotic`, `frostwindz-substrate:blood`) so the substrate-distinct signal survives downstream mechanic-family collapse.

**Dispatch-spec amendment recommendation (see C.1).**

### Gap 2 — Kinetic vendor mechanic-vocabulary likely surfaces sub-types the 7 families don't have

CodeManu's 44 impact/hit animations + Frostwindz's class-archetype slash/impact packs will surface mechanic-vocabulary the Pimen catalogue doesn't have:
- `weapon-trail` (CraftPix has these; CodeManu's Pixel FX Designer source files likely have)
- `dash` (movement-mechanic; surfaces in class-archetype packs)
- `aura` (explicit aura-mechanic VFX in class packs — Paladin auras, Warlock auras)
- `parry` / `block` / `counter` (reactive mechanics — Frostwindz's class-archetype packs likely include these)
- `cast-prep` / `windup` / `channeling` (charge/sustained-cast mechanics)
- `stagger` / `stun` (control mechanic-types per Q5)

The current 7 families absorb `aura` into `ambient-environmental` (acceptable but loses the cast-time-effect vs ambient-decoration distinction), `weapon-trail` into `melee-slash` (acceptable), `dash` into nothing (gap), `parry`/`block`/`counter` into nothing (gap), `cast-prep` into nothing (gap), `stagger`/`stun` into `buff-debuff-status` (acceptable but loses the control-sub-type distinction).

**Recommendation:** pre-extend the 7-family vocabulary with three additional families before Step B's emergent-grouping analysis runs:
- `movement-displacement` (dash, teleport-VFX, knockback-visual, pull, push)
- `reactive-defensive` (parry, block, counter, reflect, shield-cast)
- `cast-prep-sustained` (windup, channeling, charge-effect, cast-circle-buildup)

Total: 10 families instead of 7. The methodology-validation Step A was valid at 7 families because Pimen doesn't surface the additional ~3 families' worth of vocabulary; Step B's vendor mix will.

**This is the (b.2) load-bearing finding: the 7-family collapse needs extension before Step B's emergent-grouping analysis runs.** Not before Step B's crawl runs — the crawl is just data extraction; the family-collapse decision applies at elrond's post-Step-B analysis. So the trigger point for the extension is: when knight-rider authors the post-Step-B elrond emergent-grouping analysis dispatch.

## B.4 (b.3) — Coherence-decision impact: is the collapse load-bearing for GREEN-LIGHT?

**Verdict: ROBUST TO REVISION. The collapse choice is NOT load-bearing for the GREEN-LIGHT verdict.**

Reviewing the smoke test output observed from script execution:

- **silhouette=0.277 at k=8** — above the 0.15 OK threshold; above 0.0 by a comfortable margin
- **purity(mech)=0.71** — depends on the collapse choice (mech labels derived from `MECHANIC_FAMILIES`)
- **purity(reg)=0.74** — independent of collapse; load-bearing for register-axis coherence
- **purity(cat)=1.00** — independent of collapse; trivially high in a vfx-dominant corpus with character/enemy singletons
- **max_share=0.43** — below 0.6 WARN; healthy distribution
- **singletons=3** — at the WARN threshold (>1); but driven by the 3 character/enemy assets (Fantasy Platformer Character; Fantasy Skeleton Enemies; Earth Elemental bundled enemy) which structurally should be singletons given the vfx-dominant corpus

**Sensitivity check:** purity(mech) of 0.71 is the only metric directly affected by the collapse choice. The methodology would pass GREEN-LIGHT at purity-mech down to ~0.55 (the corpus has 22 fragmented mechanic tags collapsed to 7 families; expected baseline purity for a random 7-family clustering on 22 tags is ~0.20-0.30; observed 0.71 is well above baseline).

**If the collapse were re-cast at 10 families** (per B.3 pre-extension): purity-mech might drop slightly (more families means more fine-grained labels means lower per-cluster purity), but the methodology's coherence would still pass. Silhouette and register-purity would be unaffected. Category purity would be unaffected. The GREEN-LIGHT verdict survives any reasonable re-collapse.

**Conclusion:** the 7-family collapse is **methodologically locked-in for Step A but not architecturally locked-in for the post-Step-B analysis.** Elrond can revise the family collapse without re-running Step A. The GREEN-LIGHT verdict stands.

## B.5 Q-PRI-2 verdict: **ACCEPT-WITH-AMENDMENT-TRIGGER**

**Lock the 7-family collapse for Step B's crawl-phase methodology validation.** No revision required before Step B fires.

**Amendment trigger condition (for post-Step-B emergent-grouping analysis):**

When knight-rider authors the elrond emergent-grouping analysis dispatch (post-Step-B), elrond must:

1. **Extend mechanic-family vocabulary** from 7 to ~10 families adding:
   - `movement-displacement`
   - `reactive-defensive`
   - `cast-prep-sustained`
2. **Separate aura-mechanic from instant-buff** within `buff-debuff-status` if Step B's new vendor evidence surfaces enough aura-distinct asset evidence to support the split (Pimen alone does not; Frostwindz class-archetype packs likely will)
3. **Use vendor-namespaced substrate-tags** for novel-substrate vendors (Frostwindz necrotic/blood/cosmic; Fellor crystal; Pixogen void/technology) to prevent substrate-distinct signals from collapsing into existing mechanic-families
4. **Re-run sensitivity analysis** at the revised family vocabulary to verify silhouette + purity metrics still pass

If any of (1)-(3) prove infeasible at post-Step-B data inspection, elrond escalates to gandalf for re-review; the 7-family collapse holds as fallback.

---

# C. Step B dispatch-spec amendments — recommended for knight-rider before un-holding

## C.1 — Add vendor-namespaced mechanic-tag extraction requirement

**Insert into Step B dispatch § "Output format" — Per-pack JSONL row:**

> Mechanic-leaning vocabulary surfaced from vendor pack pages should be tagged with vendor-namespace prefix (e.g., `frostwindz-mechanic:necrotic-cast`, `pixogen-mechanic:portal-summon`, `codemanu-mechanic:weapon-trail`). This preserves substrate-distinct signal through any downstream mechanic-family collapse. Elrond's post-Step-B emergent-grouping analysis will normalize the vendor namespaces; legolas's job is preservation at extraction time.

**Rationale:** prevents the Gap 1 risk in B.3 — necrotic/blood/cosmic substrate signals from new vendors collapsing into existing mechanic-families (buff-debuff-status, impact-burst) and erasing the cipher-width-analysis-relevant variance.

## C.2 — Add explicit license-verification artifact requirement

**Insert into Step B dispatch § "Per-vendor crawl methodology" — Step B.1 or new Step B.4:**

> For any vendor whose license terms are not readable from the public web page (license file is a downloadable artifact only), fetch the actual license artifact, read it, and record the full terms in the per-vendor findings summary. License-clarity criterion #3 from the binding inclusion criteria is met only when the actual terms are inspected, not when the existence of a license file is confirmed.

**Rationale:** addresses the A.2.2 Pixogen flag triage. Operationalizes the license-clarity binding criterion #3 against vendors whose license terms hide behind downloads.

## C.3 — Add 404-retry + inferred-substrate flagging discipline

**Insert into Step B dispatch § "Per-vendor crawl methodology" — Step B.1:**

> When pack pages return 404 during metadata-only pre-pass, retry with alternate URL slugs (vendor's collections / sale pages may have current URLs); record `pack_page_404: true` in the per-pack JSONL and flag inferred substrate claims as `unverified_inferred_from_vendor_profile` in the per-vendor findings summary. Substrate-evidence claims from inferred sources should be marked as such so elrond's cross-vendor inventory can weight evidence quality.

**Rationale:** addresses the A.2.1 Frostwindz 404 flag triage. Preserves substrate-evidence quality through proper provenance flagging.

## C.4 — Pipoya inclusion decision

**Recommend knight-rider re-confirm with Matt:** Pipoya included as vendor #10 OR not? The 10-vendor list keeps the commission's ceiling and adds Time/Warp substrate evidence that the cipher-width framework should not assume away. The 9-vendor list is conservative; sample Time/Warp at consumption time without full Step B crawl coverage.

**My recommendation: include Pipoya as vendor #10.** Time/Warp is a substrate the cipher-width framework's "multiple-groupings emerge" outcome may bind into a temporal-grouping that genre-precedent (PoE Temporal Chains; D2 Bone Spirit) supports. Cipher-width framework benefits from the evidence.

---

# D. What this unblocks

**Step B Tier-1 2D-VFX exhaustive crawl is RELEASED from HELD.** Both gates close:

- **Gate 1 (Step A methodology validation):** GREEN-LIGHT per elrond's smoke test; my Q-PRI-2 review accepts the methodology with the post-Step-B amendment trigger documented in B.5.
- **Gate 2 (vendor-discovery sweep + screening):** finalized Tier-1 list at 9 vendors (10 with Pipoya per C.4); 3 dispatch-spec amendments recommended at C.1-C.3 for knight-rider to integrate before un-holding.

**Knight-rider next steps:**

1. Integrate amendments C.1-C.3 into the Step B dispatch (`agentic_orchestration/dispatches/2026-05-16-legolas-step-b-tier1-2dvfx-crawl.md`) — minor inserts under the existing sections; do not rewrite the dispatch structure
2. Confirm with Matt on the Pipoya inclusion question (C.4) — 5-second decision; either 9 or 10 vendors
3. Flip the Step B dispatch Status field from `HELD` to `PENDING — ACTIVE` and notify legolas
4. Queue the post-Step-B elrond emergent-grouping analysis dispatch authoring task with the amendment-trigger conditions from B.5 carried forward (recommended families: `movement-displacement` + `reactive-defensive` + `cast-prep-sustained`; aura-vs-instant split; vendor-namespace normalization)

## D.1 What this does NOT unblock

- Cipher-width sub-lock resolution — that waits for Step B's full output + the post-Step-B elrond emergent-grouping analysis
- Foundation layer placement decision — joint with cipher-width per § 5.3 of strategy doc
- D1 element-name pool reconsideration — joint with cipher-width per § 5.3
- Per-season vocabulary coupling (α/β/γ) — joint with cipher-width per § 5.3
- Acquisition decisions on any vendor packs — Matt-decision per ADR-006
- Character-only vendor sub-commission — separate track per Q4

---

## Authority boundary note

This finding closes the Step B HELD-gate-3 review per the parent commission's design-track review authority. The 3 dispatch-spec amendments (C.1-C.3) are recommendations to knight-rider; knight-rider has the dispatch-authoring authority per ADR-002 and may choose to integrate, modify, or reject individual amendments. The Q-PRI-2 verdict (ACCEPT-WITH-AMENDMENT-TRIGGER) is design-track binding; the methodology revision condition in B.5 is a design-track requirement for the post-Step-B analysis, not optional.

If knight-rider determines any of the amendments materially expand Step B scope beyond the commission's 2-4 Mode B session estimate, escalate to Matt for re-confirmation before un-holding.

---

— gandalf, 2026-05-16 (Day 4)
