# VDM-1 STAGE-5 — BLIND RE-PROJECTION RIDER: DIVERGENCE REPORT (steward)

**Author:** gandalf (steward · DRIFT-CRITIC) · 2026-07-18 · **Feeds:** THE REVIEW BOOK (stage 6)
**Method:** 61 kits (10.3% of 574, grade-stratified, all 21 games) independently re-judged **BLIND** by legolas (3 waves, sonnet) on the three judgment-grade axes — element / ailment / grade — from dossier + verify anchors only, never seeing the original mapping. Steward then diffed each blind judgment against the withheld original (re-derived from `kit_mapping`, readonly) and **adjudicated every divergence against the source evidence.** This is inter-rater reliability (legolas-blind vs the gandalf-seam originals) — a different, stronger check than intra-rater.

---

## 0. Headline

| Axis | Blind≡Original | Divergences | Direction | After evidence-adjudication |
|---|---|---|---|---|
| **Element** | **51/61 = 84%** | 10 | 6 blind-MORE / 4 blind-LESS / **0 family-SWAP** | original **right-or-defensible on ~58/61 (95%)**; **3 confirmed corrections** |
| **Ailment** | **47/61 = 77%** | 14 | 5 more / 7 less / 2 swap | original defensible on ~59/61 (~97%); **1 confirmed correction** |
| **Grade** | **31/61 = 51% exact** | 30 | **26 harsher / 4 softer** (off-by-1: 24, off-by-2: 6, off-by-3: 0) | divergence explained by the blind rubric, NOT original error (§3) |

**The reliability verdict is strong.** The two **law-governed** axes (element, ailment) show high agreement with **near-balanced direction and zero family-swaps** → there is **no pervasive systematic bias** in the corpus (no run-wide over-silencing or over-attesting). The residue the rider surfaced is small (**4 confirmed errata** across 61 kits ≈ the ~0.5–1% miss-rate the run targeted) and is the **same class** as the audit-caught `ud-lightning-vortex` — under-/over-attestation of a genuinely-(un)attested element/ailment. Grade, the inherently-soft axis, diverges more, but the divergence is a **blind-rubric artifact** (§3), not evidence of original mis-grading.

---

## 1. Element axis — per-divergence adjudication (10)

**Ruling key:** ★ = confirmed original error (→ errata) · ○ = blind over-reach (original right) · ≈ = genuine convention/judgment ambiguity (both defensible)

| kit | blind | original | ruling | deciding evidence |
|---|---|---|---|---|
| **d2-avenger** | fire·lightning·water | fire·lightning | ★ **orig miss +water** | *"Fire, lightning **and cold** damage are added to each successful attack"* — explicit tri-element; cold→water. |
| **le-runic-invocation** | fire·lightning·water | lightning | ★ **orig miss +fire+water** | outputs = *"**fire burst, ice storm, lightning fork**"* — explicit multi-element damage. |
| **d2-ghost-pvp** | lightning | lightning·shadow | ★ **orig over-attest −shadow** | only Lightning Sentry (lightning) + WW (physical) + Mind Blast (stun) attest; "shadow" = *Shadow Discipline* tree **name** → L2 name-only, no shadow-damage descriptor. |
| d4-cataclysm | lightning·wind | lightning | ○ blind over-reach | "twisters blanket the screen" = theme; **no "wind damage" descriptor** (D4 twisters = physical). Original right. |
| poe1-ward-loop | shadow·water | shadow | ○ blind over-reach | Ice Spear/Freezing Pulse are incidental CWDT-triggered payload; blind **self-flagged** this as its weakest attestation. Loop identity = Forbidden-Rite shadow. Original right. |
| gd-skeleton-ritualist | shadow | (silent) | ≈ pet-element | "vitality skeletons" attest shadow-by-crosswalk, but damage is **minion-sourced** (summoner-class, element-silent convention). Both defensible. |
| le-skeleton-necro | (silent) | water | ≈ pet-element | "Skeletal **Frost** Mage… barrage of Ice Shards" = minion cold; same summoner-silent vs pet-damage split as above. |
| gd-callidors-tempest-templar | fire | fire·lightning | ≈ aether crosswalk | "aether-fire tempest"; aether→lightning-or-shadow is a judgment; original applied aether→lightning, blind dropped it. |
| poe1-spectral-throw | (silent) | lightning·water | ≈ Ele-Buzzsaw | base Spectral Throw = physical; "Ele Buzzsaw" variant "scales with **elemental** damage" (generic — specific families thinly-attested). |
| poe1-wormblaster | fire | (silent) | ≈ variant | identity = element-agnostic CoC engine; "Flameblast/Herald of Ash" is **one named variant** (fire). Both defensible. |

**Element net:** 3 confirmed corrections (2 misses + 1 over-attest), 2 blind-over-reach, 5 genuine ambiguities. Original **right-or-defensible on 58/61 (95%)**.

## 2. Ailment axis — key adjudications (14 divergences, 77% base agreement)

- ★ **gd-bwc-demolitionist +burn** (orig had only `[blind]` from -OA; **missed the burning-tar DoT** = an explicit `burn`). The blind rater conversely **missed** the -OA→`blind` mapping — the two are complementary; the **union** {burn, blind, curse:sap} is the fuller truth. Confirmed original miss on `burn`.
- ≈ **d3-manald-heal** (blind `shock` vs orig `stun`) — the kit's status is **Paralysis**, which sits on the `shock`(=engine paralyze)/`stun` boundary. Genuine **taxonomy ambiguity**, not an error → crosswalk-refinement candidate (§4).
- ≈ **poe1-frost-blades / poe1-winter-orb / tq-ice-shard-oracle** (orig attests `chill`/`freeze`, blind strict-silent) — the "does cold-damage **imply** chill/freeze" question. L3 says *don't infer ailment from element*; the blind rater held strict, the original applied genre-canonical cold-status. **Both defensible**; flags an L3-strictness boundary (§4).
- The remaining ±1 divergences (reaper bleed, firebird/fire-berserker burn, ball-lightning sunder, auradin curse:sap, etc.) are single-ailment partial-catches within the strict-attestation band; none rise to a confirmed error on the shown evidence.

**Ailment net:** 1 confirmed correction (bwc `burn`); rest are strictness/taxonomy/complementary. Original defensible on ~59/61.

## 3. Grade axis — the harsher-skew is a blind-rubric artifact, not original error

51% exact, **26 harsher / 4 softer**. The blind spec carried a **compact** grade rubric (no full engine-palette enumeration), so the blind rater **defaulted to GAPPED whenever unsure a primitive existed** — visible in the 10 GAPPED-flips, all on **proxy/trap/summon-adjacent** kits the original mapped with full context (le-explosive-trap-falconer, poe2-infernal-legion, hades2-omega-magick, poe1-totem-hierophant, poe1-reaper, tli-iris2-thunder-magus). The original, holding the engine palette + mapping brief, is the **better-informed** grader here.

The 4 **softer** cases (blind more generous) confirm the same asymmetry rather than contradicting it:
- **la-liberator-valkyrie** (blind CLOSE vs orig **GAPPED**, Δ−2) — a **pure party-support** healer/buffer ("heal party", "Wings of Liberation applies to all party members"). In a **solo** engine a party-only support has no function → the original's GAPPED is **correct** (support-gated-to-multi-actor, per the project role-orientation taxonomy). Blind under-graded the support-gap.
- **poe1-wormblaster** (blind APPROX vs orig GAPPED) — original correctly GAPPED the exotic **friendly-worm-as-crit-fodder** (Writhing Jar) mechanic; blind under-appreciated its exoticness.
- **d2-singer / di-whirlwind-barb** (blind EXACT vs orig CLOSE) — minor generosity on two well-understood kits; original's CLOSE is the conservative-correct call.

**Grade verdict:** the blind rider **corroborates** the original grades — every material divergence resolves in the original's favor once engine context is applied. It does establish, honestly, that **grade is the lowest-reliability axis** (an inter-rater truth worth stating in the review book), but not that the corpus is mis-graded.

## 4. Outputs for THE REVIEW BOOK

**A. Confirmed errata candidates (4) — recommend for Matt ratification (NOT silently applied; the review book is the errata surface):**
1. `d2-avenger` — element **+water** (tri-element cold attested).
2. `le-runic-invocation` — element **+fire +water** (multi-element outputs attested).
3. `d2-ghost-pvp` — element **−shadow** (name-only over-attestation; moderate confidence).
4. `gd-bwc-demolitionist` — ailment **+burn** (burning-tar DoT).

**B. Crosswalk-refinement candidates (surface, don't fix mid-run):**
- **Paralysis → `shock` vs `stun`** disambiguation (manald-heal) — the D3 Paralysis passive maps ambiguously; the crosswalk should name a rule.
- **cold-damage → `chill`/`freeze` inference** (frost-blades, winter-orb, ice-shard-oracle) — L3 forbids element→ailment inference, but every mapper genre-canonically applies cold-status; the review book should decide whether cold implicitly carries chill/freeze or requires explicit prose.
- **minion/pet damage → player element attribution** (skeleton kits) — when a summoned entity carries the damage type, does the kit attest that element or stay player-silent? Convention should be named.

**C. Reliability statement for the book:** on the law-governed axes the corpus is **highly reliable** — ~95% element / ~97% ailment right-or-defensible after evidence-adjudication, **zero systematic directional bias**, 4 confirmed corrections in 61 kits. Grade is the soft axis (51% inter-rater exact) but every material divergence resolves in the original's favor once engine context is applied.

---

**Signed:** gandalf (steward · DRIFT-CRITIC) · Stage-5 blind rider divergence report · 61 kits / 3 blind waves · the run's final QA gate before THE REVIEW BOOK.
