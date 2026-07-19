# VDM-1 — THE REVIEW BOOK

> **STATUS:** CURRENT (load-bearing as of 2026-07-18) — the single end-of-run Matt review for the VDM-1 verify+dossier+map run (charter R-8b). Supersedes `review-book-accumulators.md` (staging index, now banner-superseded).

**Date:** 2026-07-18 · **Author:** gandalf (run steward · SPEC-AUTHOR/DRIFT-CRITIC) · **Authored on fable-5 per the model-gate (Matt confirmed at the Stage-5 HALT).**
**Authority:** Matt's VDM-1 autonomy mandate (charter, 2026-07-18) — one touchpoint: THIS book. Nothing in it is self-ratified; every ruling below is REQUESTED, not applied.
**Companion artifacts:**
- `REVIEW-BOOK-ROSTER-{EXACT,CLOSE,APPROX,GAPPED}.md` — the full 574-kit roster by grade WITH per-kit deviations (the charter's "every mapping by grade" contract; generated from `kit_mapping` readonly)
- `errata-ledger.md` — the authoritative errata index (55 ERRATA entries + reviews/soft-flags/backfills/annotations)
- `stage5/BLIND-RIDER-DIVERGENCE-REPORT.md` — the final QA gate's full adjudication
- `agentic_orchestration/gandalf/notes/2026-07-18-vdm1-run-state.md` — the run ledger (full lineage)
- DB: `research/curated/corpus.db` (gitignored-local; md5 `4a1ae47c…` post-INGEST-18)

---

## 0. How to read this book

VDM-1 fact-checked, sourced, dossiered, and **engine-mapped every canonical ARPG kit in the corpus** — 574 kits across 21 games, five basins, in one autonomous run. You are the single reviewer. The book is organized so you can rule everything from **§ 2 (THE DECISION SURFACE)** alone; §§ 3–9 are the evidence chapters behind each ruling; the roster appendices are the per-kit ground truth.

Reading order: **§ 1** (one screen) → **§ 2** (the ten rulings, D-1…D-10) → dip into §§ 3–9 as each ruling needs. Nothing was silently applied mid-run except ingest-time errata with anchor citations (all indexed, § 6); everything judgment-shaped waited for this book.

---

## 1. The run in one screen

| Measure | Result |
|---|---|
| **Kits mapped** | **574 / 574** (585 corpus records − 11 `is_system` meta-records, § 9.4) |
| **Grades** | **EXACT 53 (9.2%) · CLOSE 347 (60.5%) · APPROX 88 (15.3%) · GAPPED 86 (15.0%)** — MAPPED 488 / MAPPED_DOCKET 86 (R-M7 biconditional held run-wide, 0 violations) |
| **Verification** | 2,068 verify rows: **CONFIRMED 1,784 (86.3%) · CONTRADICTED 76 (3.7%) · UNSUPPORTED 207 (10.0%) · SNF 1** |
| **Per-axis reliability** | identity **96.2% C** (553C/8X/17U) · mechanics 88.6% (530C/25X/42U/1SNF) · era 80.0% (676C/35X/**134U** — the U mass) · negative_canon 53.2% (25C/8X/14U — weakest family, § 8.2) |
| **Dossier** | 3,444 rows · 597 abstained (**82.7% non-abstained**; honest-abstain discipline held) |
| **Citations** | 1,285 rows · 6 quarantined (commerce/boost-SEO class) — export IP-gated, § 10 |
| **Fact promotion** | **3,727 probe-facts promoted to `verified-v1.1`** · 623 kb-legacy · 430 named-source-unfetched remain unverified |
| **Errata** | 55 numbered ERRATA + 1 mapping erratum (MAP-ERRATA-1) + reviews/soft-flags/backfills — all anchored, all indexed (§ 6) |
| **Blind-rider QA** | 61-kit (10.3%) blind re-projection: element 84% / ailment 77% / grade 51% raw agreement → **~95% / ~97% right-or-defensible after adjudication, ZERO family-swaps, no systematic bias** (§ 7.2) |
| **Docket** | 8 steward-ratified-candidate rows in DB + 87 held mechanism rows consolidating to ~15 families (§ 5) |
| **Mint** | 6 steward-ratified candidates (1 GRADUATED at 3 forcing kits) + accrual families (§ 4) |

**Element census (kit-level attestation, strict D4 name-only law):** 272/574 kits attest ≥1 family; 302 silent. fire 94 · lightning 70 · shadow 60 · water 55 · earth 26 · **holy 6 · wind 2**. The thin tail is a finding, not a failure (§ 8.5).

**Ailment census (16-closed registry):** burn 36 · freeze 34 · poison 32 · chill 29 · sunder 27 · stun 24 · bleed 20 · curse:amplify 19 · curse:sap 16 · drain 15 · knockback 9 · blind 6 · root 4 · execute 4 · curse:weaken 4 · fear 3 · curse:decrepify 3 · consecrate 2 · **shock 1** (the paralysis-prose bar is the registry's strictest — by design). Every registry family exercised at least once.

**Per-game grade matrix (E/C/A/G):**

| game | kits | E | C | A | G | | game | kits | E | C | A | G |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| poe1 | 94 | 2 | 62 | 22 | 8 | | tq | 21 | 3 | 12 | 4 | 2 |
| d2 | 60 | 9 | 33 | 9 | 9 | | hot | 17 | 6 | 8 | 1 | 2 |
| la | 52 | 2 | 41 | 1 | 8 | | chronicon | 16 | 5 | 4 | 2 | 5 |
| d3 | 49 | 0 | 34 | 7 | 8 | | undecember | 12 | 4 | 5 | 0 | 3 |
| d4 | 46 | 4 | 36 | 2 | 4 | | tl2 | 11 | 7 | 2 | 1 | 1 |
| gd | 41 | 9 | 23 | 3 | 6 | | tli | 9 | 0 | 5 | 2 | 2 |
| poe2 | 38 | 0 | 27 | 11 | 0 | | hades1 | 7 | 0 | 0 | 0 | 7 |
| le | 37 | 0 | 22 | 10 | 5 | | hades2 | 5 | 0 | 4 | 1 | 0 |
| di | 24 | 0 | 10 | 7 | 7 | | tq2 | 5 | 0 | 3 | 2 | 0 |
| vs | 23 | 2 | 12 | 2 | 7 | | mcd | 5 | 0 | 3 | 1 | 1 |
| | | | | | | | tl1 | 2 | 0 | 1 | 0 | 1 |

---

## 2. THE DECISION SURFACE — the ten rulings (D-1 … D-10)

Everything below is **requested**, with my lean stated. Rule inline (a margin "yes/no/fork-b" per item is enough); I execute post-ratification as a single errata/ratification pass.

### D-1 — Blind-rider errata (4 kits; § 7.2 evidence)

Confirmed by independent blind re-judgment + steward adjudication against source prose. **Lean: apply all four.**

1. `d2-avenger` — element **+water** (*"Fire, lightning and cold damage are added to each successful attack"* — explicit tri-element).
2. `le-runic-invocation` — element **+fire +water** (outputs *"fire burst, ice storm, lightning fork"*).
3. `d2-ghost-pvp` — element **−shadow** (attestation was the *Shadow Discipline* TREE NAME — a name-only over-attest under the D4 law; moderate confidence).
4. `gd-bwc-demolitionist` — ailment **+burn** (burning-tar DoT explicitly attested; union with existing `blind`, `curse:sap`).

### D-2 — Crosswalk refinements (3 rules; surfaced mid-run, deliberately not patched mid-run)

1. **Paralysis → `shock` vs `stun`** (d3-manald-heal): D3 "Paralysis" sits exactly on the boundary. **Lean:** Paralysis-named mechanics → `shock` (it IS the engine's paralyze); generic "stunned" prose → `stun`.
2. **Cold-damage → `chill`/`freeze` inference** (frost-blades, winter-orb, ice-shard-oracle): L3 forbids element→ailment inference, but genre-canon says cold slows. **Lean:** keep strict — cold status requires explicit prose. The engine's water kits will carry chill natively regardless; the corpus should record only what sources attest.
3. **Minion/pet damage → player element attribution** (skeleton kits): when the DAMAGE belongs to a summon, does the kit attest the element? **Lean:** summoner-class kits stay element-silent (damage is minion-sourced); note the pet element in `delivery_notes` only.

### D-3 — Mint ratifications (the 6 candidates + accrual families; § 4 full detail)

**Lean: ratify #2 now (GRADUATED, 3 forcing kits); hold the rest as evidence-gated candidates for engine-design intake.**

- **#2 stack-parameterizes-geometry (qualitative, GRADUATED)** — crackling-lance + pizza-sticks + venom-gyre. The graduation bar (3 independent forcing kits) was met mid-run. Strongest mint in the book.
- #1 chain fan-out growth >1.0 (quantitative; arc) · #3 out-and-return path (qualitative; spectral-throw **+5 accrued siblings**: aegis, umbral-blades, shield-throw, medea, tli-carino2) · #4 temp-minion swarm ~20 (quantitative; srs) · #5 hexa-totem count (quantitative; totem-hierophant) · #6 enemy-seeking mobile AoE (qualitative; vaal-blade-vortex).
- **Two-tier-accumulator family — the OPEN qual-mint question:** now ~10 evidence kits (shaman-bear, walking-calamity, cadence ×2, tempest-strike ×2-shapes, runic-invocation, raekor/shenlong, vyr-archon, + d3 family-accrual rows). The watch-item fired at 2 kits in basin-1; it kept strengthening every basin. **Lean: mint it** — this is the genre's "build-up → payoff" grammar and the evidence mass is the run's largest.
- Twister roaming-persistent-AoE (the 27th-geometry question) + HoWA attribute-total-as-damage: hold as filed.

### D-4 — Docket ratifications (8 DB rows + 87 held rows → ~15 families; § 5 full detail)

**Lean: ratify all 8 DB rows as the permanent gap record; adopt the § 5 consolidation as the docket taxonomy; route the four "mint-or-declare" forks to engine-design intake rather than ruling them inside this book:** entity-as-consumable-resource-pool (7 kits) · spectre world-capture · stat-as-army-size (siege-ballista) · control-magnitude-as-damage (heavy-strike-stun). The two **intentional-guard collisions** (perma-stunlock floor; MAX_CHAIN_DEPTH=1 vs ward-loop) should be ruled **working-as-intended** — the engine refusing those identities is a design position, not a gap.

### D-5 — Summoner-deferral reaffirmation

The largest single GAPPED driver: **~21 of 86 GAPPED kits** are summoner/pet-core (golemancer, zuni-carnevil, rathma, minion-necro, pet-conjurer, skeleton-necro, wraithlord, liche-king, petmaster, mechanist, pet-warden, bot-engineer, alchemist-summoner, moto-bots, mcd-summoner, master-summoner …). Every one mapped honestly to the deferral (two-lane ruling: placement→totem / follow→null). **Lean: reaffirm Phase-5 deferral; the docket rows are the evidence bank for when summoner work opens.** No engine action now.

### D-6 — Ailment-registry no-homes

Withheld correctly at mapping (never leaked); adjudicated here: GD confusion · GD electrocute · GD frostburn · LE Frostbite · **LE Time Rot** (named, build-defining, stack-capped with dedicated multipliers — the loudest) · **LE Shadow Daggers** (×2 bladedancer kits). **Lean: no registry expansion.** The 16-closed registry held across 574 kits with every family exercised; these six are source-native statuses whose IDENTITY the engine already covers via near-neighbors (Time Rot ≈ drain+chill compound; Shadow Daggers ≈ stack-payoff, which is D-3's two-tier mint territory, not an ailment). Record as permanent crosswalk footnotes.

### D-7 — Kit-level adjudications (7 items)

1. **d2-wl-void-rift** — search-derived seed, harvest FAILED (all four families honest-negative; kit-level ghost). **Fork: keep-as-ghost (annotated) vs excise. Lean: keep-as-ghost** — it documents a kb-hallucination class; deletion is Matt-tier.
2. **di-bombardment** — d3→di misapplication flag. **Lean: annotate, keep** (mapped identity is the attested di one).
3. **d4-spiritborn-vortex** — component-not-archetype (a skill, not a build). **Lean: annotate as component-class; keep mapped.**
4. **d2-spiritform-druid-pvp** — negative-on-mis-specified-mechanic. **Lean: relabel the negative claim, keep kit.**
5. **le-harvest-lich CHIMERA** — kb folk-name conflates Harvest Flay + Death Seal Lich; mapped as-is from the basin-2 dossier. **Fork: split into two kits vs annotate-as-chimera. Lean: annotate now; split only if VDM-2 re-crawls LE.**
6. **poe1-earthshatter REVIEW-1** — phantom alias "Foulborn Ghostwrithe zerker(3.28)" unadjudicated. **Lean: strike the alias.**
7. **poe2-erasure REVIEW-2** — possible-phantom, annotated-not-deleted. **Lean: keep annotation; no deletion** (deletion is yours alone).

### D-8 — DB hygiene (3 deferred normalizations)

1. `corpus_bucket` duplicate Diablo token pairs (d3/diablo-3 · d4/diablo-4 · di/diablo-immortal) → normalize in one migration. **Lean: yes.**
2. REVIEW-numbering collision (basin-1 "REVIEW-2" vs PoE1 "REVIEW-2") → basin-qualify all REVIEW ids. **Lean: yes.**
3. Errata bookkeeping law: `errata-ledger.md` is the authoritative index; DB `errata_applied` counter excludes policy-restamps. **Lean: ratify as standing law.**

### D-9 — Citation export (dependency, not a new ruling)

The devlog citation export is ready to generate from `kit_citations` (1,285 rows, 6 quarantined, author-credit lineage per § 9.6) but **ships only within whatever `canonical/matt_decision_needed/2026-07-13-ip-clearance-devlog-and-hook-surface.md` rules** — that item is still open in your queue. No action here; the book records the gate.

### D-10 — Corpus v1.1 stamp + tracker registration

**Lean: stamp the corpus `v1.1-verified` on your ratification of D-1/D-7/D-8**, then register the delta in `canonical/current-to-end-state/…-serial-content-emission.md` (the corpus is the serial-content substrate) and `…-engine.md` (docket → engine-gap intake). Tracker-delta lines are pre-drafted in § 10.

---

## 3. The corpus by grade

Grade rubric (L6): **EXACT** no material deviation · **CLOSE** minor documented deviation, identity intact · **APPROX** identity bends materially (deviation notes mandatory) · **GAPPED** load-bearing mechanic has no engine primitive → docket (R-M7: GAPPED ⟺ MAPPED_DOCKET, 0 violations run-wide).

**Full per-kit rosters with complete deviation notes:** `REVIEW-BOOK-ROSTER-EXACT.md` (53) · `-CLOSE.md` (347) · `-APPROX.md` (88) · `-GAPPED.md` (86). Every kit carries grade, terminal, attested element/ailment sets, `is_system`/negative flags, and its full deviation text — the charter's "every mapping by grade with deviations," discharged.

**Grade-shape findings:**
- **60.5% CLOSE is the honest center of mass.** The engine substrate reproduces most canonical identities with minor documented bends — neither the optimism of an EXACT-heavy shape (rubber-stamp signal) nor the despair of an APPROX-heavy one.
- **EXACT-rate inversely tracks build-system depth** (§ 8.4): tl2 64% EXACT, hot 35%, chronicon 31% vs poe1 2%, and d3/le/poe2/tli/hades at 0%. Flat-documentation classic-shaped games land exactly; modifier-stack games bend. The engine's substrate is closest to classic-ARPG grammar.
- **GAPPED is dominated by four structural classes, not scattered failures** (indicative keyword split, rows may carry 2 classes): summoner/pet-core ~21 · support/party-scope ~13 · loadout/boon-rotation-absent ~10 (hades1 all 7, mcd, vs) · thin-source/unattested ~5 · remainder = the § 5 mechanism families. hades1 going 7/7 GAPPED is **correct genre behavior**, not failure — boon-rotation identity has no castable-rotation primitive (§ B5 law).
- **The 46 negative-canon trap-kits mapped like normal kits on their ATTESTED identity** (2E/15C/18A/10G): mapping maps what the kit IS; the trap-story rides the negative flag (§ 8.2).

---

## 4. Mints — all six candidates + accruals (mint_ledger, status `steward-ratified-candidate`)

| # | class | mechanism | forced by | status |
|---|---|---|---|---|
| 1 | quant | chain fan-out decay override permitting **>1.0** (per-hop GROWTH; engine `_CHAIN_DEFAULT_DECAY=0.7` is decay-only) | poe1-arc | candidate |
| 2 | qual | **stack-parameterizes-geometry** — stacks reshape LIVE geometry/emission, not just damage (beam narrow+intensify / placed-arc morph / catch-count → release projectile count) | crackling-lance · pizza-sticks · venom-gyre | **GRADUATED (3 kits)** |
| 3 | qual | **out-and-return** projectile path (outward → return pass, per-enemy re-hit) — no 26-geometry member returns | spectral-throw (+aegis · umbral-blades · shield-throw-time-rot · medea · tli-carino2 accrued) | candidate, 6-kit family |
| 4 | quant | temp-minion swarm count (~20 short-lived proxies, cast-cadence sustained) | poe1-srs | candidate |
| 5 | quant | placed-proxy (totem) count → 6 w/ per-proxy cast-rate penalty | poe1-totem-hierophant (+forge-turrets · mortar · moto-bots · trap-magician · bot-engineer · le-bomb accrued to the family) | candidate |
| 6 | qual | autonomous enemy-SEEKING mobile AoE (chase ≠ R-M6 drift) | poe1-vaal-blade-vortex | candidate |

**Accrual families steward-held (not yet minted):** **two-tier-accumulator (~10 kits — D-3 lean: MINT)** · roaming-persistent-AoE (twister; 27th-geometry question) · HoWA/gemling attribute-total-as-flat-damage · GD wandering-emitter (wind-devil) / enemy-attached-emitter (stormbox) / proximity-armed-trigger (rune-of-hagarrad) · stat-as-damage-substrate accruals (ride D-4's cluster, not mints).

**R-M5 trigger-enum gaps (greppable, emitted un-negated):** `AUTOCAST_ON_MOVE` · `COMBO_BEAT_NTH` · `MINION_CONSUME`. Everything else fit the existing enum.

---

## 5. Dockets — 8 ratified-candidate rows + the held-row consolidation

### 5.1 The eight DB rows (`mechanic_gap_docket`, full text in-DB)

1. **entity-as-consumable-resource-pool** — 7 kits (animate-weapon, bladefall-bladeblast, dark-pact, detonate-dead, minion-pact-bv, reaper, wormblaster). Dominant PoE1 gap family. Fork: mint an entity-pool substrate lane vs declare permanently approximated.
2. **ally-buff-projection scope boundary** (aurabot) — party-support in a solo engine. NOT a mint request; a permanent-scope record. **Now +5 LA siblings** (liberator-valkyrie, judgment/blessed-aura paladins, desperate-salvation bard, full-bloom artist) — the class is cross-game.
3. **RNG-element-pool identity** (elemental-hit, skeleton-mages, wild-strike) — random-from-pool has no lane; pruning-endpoint distinction must survive any future design (prunable=build, unprunable=trap).
4. **stun-magnitude-as-damage + perma-stunlock** (heavy-strike-stun) — collides with the engine's DELIBERATE anti-stunlock floor. Lean: working-as-intended.
5. **self-damage cost redirected to proxy life-pool** (forbidden-rite) — cost-payer redirection primitive absent.
6. **closed-loop self-damage trigger economy** (ward-loop) — cyclic trigger closure vs MAX_CHAIN_DEPTH=1 LOCKED. Lean: working-as-intended (the guard is the design).
7. **world-entity-capture minion pool** (spectres) — capture-from-world + ability-inheritance lanes absent.
8. **attribute-value → proxy-count coupling** (siege-ballista) — stat-counts-army scaling substrate.

### 5.2 Held-row consolidation (87 rows → the taxonomy)

| family | rows/kits (indicative) | disposition lean |
|---|---|---|
| **summoner-deferral** (incl. army-GAP CotA/garg) | ~23 rows across all basins | D-5: evidence bank; no action |
| **stat-as-damage-substrate** (6 DO-NOT-MERGE mechanisms + accruals: armour-value · armor-conversion · stun-substrate · block-chance · max-Mana→minion · missing-Mana→spell; + retaliation, thorns ×2, reservation-as-scaler, tli-rosa) | ~12 | keep 6-way split; engine-design intake |
| **spatial-consumable-resource-node** (d2-berserker, grim-ward, trapsin, pestilence, infinimist, shadowblight, di-corpse-explosion) | 7 | sibling of DB row 1 — same intake |
| **support/party-scope** (LA cluster) | 5 rows | fold into DB row 2 as siblings |
| **loot-economy-identity** (berserker Find-Item, horker, throw-barb, firebomb) | 4 | permanent out-of-scope record (loot meta ≠ combat kit) |
| **mode-swap-identity** (deadeye, peacemaker, iris2) | 3 | GX-02 form-swap gate adjacents; hold |
| **roguelite-idiom cluster** (hades1: delayed-detonation Doom · deflect · self-cost-contract · duo-boon-pair · finite-ammo-burst · per-arrow-status) | 6 | genre-law records; no engine action |
| **minion-consumption harvest** (wraithlord + zero-dogs) · **recipe/combination-determines-output** (runic-invocation + tli-rosa) · **gear-stat-as-minion-scaling** (manifest-armor + golemancer) | 2 kits each | each reached 2-kit evidence — name as standing families |
| singletons (contact-propagation-DoT rabies · utility-transport teleport-sorc · mosaic inverted-spend · item-count-multiplier lod · mobility-gap blade-shift · placement-barrier bone-wall · link-rune geometry-modifier · cooldown-reset chronomancer · overheal/ES-above-cap [merged 1 class] · density-reactive cadence · throw-retrieve reload · ward-from-missing-health · maintenance-reservation · pet-death-payload · unshipped-content wereforms · fully-unattested snowstorm · element-unresolved moto-bots) | 1 each | hold as filed |

---

## 6. Errata — the authoritative index

**`errata-ledger.md` (1,684 lines) is the errata surface**; the DB `errata_applied` counter is subordinate (D-8.3). Shape of the record:

- **55 numbered ERRATA** across five basins. Dominant classes: **era floor/restamp (D-2a uniform law)** ~25 · content-field (folk_name/core_skills/class) ~8 · probe-fabrication consolidation (ERRATA-46, 13 items) · element/alias fixes · NULL-era backfills (×7, never overwriting non-NULL) · annotation-class (kit-level flags, Unattested Register).
- **MAP-ERRATA-1** (the run's sole mapping-stage erratum): `ud-lightning-vortex` element null→lightning + unattested `shock` removed — steward-audit caught, applied at INGEST-18 with anchor citation, source jsonl preserved as mapper lineage.
- **~20 crawl-stage steward corrections** applied at ingests with anchors (all indexed in the ledger; every one a DB≡file expected-diff verified by the D-2c battery).
- **The 4 blind-rider candidates (D-1) are NOT yet applied** — they await your ratification; they would become ERRATA-56…59.
- Unadjudicated REVIEW items ride D-7 (earthshatter alias, Erasure phantom).

---

## 7. Reliability, calibration + the audit chain

### 7.1 Calibration (V-0 gate, self-adjudicated post-PoE1 per R-8b)
Pre-registered priors vs measured: era **.848 vs .85 prior** (dead-on); identity/mechanics/negative within band; **no mint explosion** (6 distinct / 6.4% rate); grade shape held with **zero optimism creep** (PoE1 final 2E/62C/22A/8G). **Rubber-stamp detector passed:** 3.7% contradiction rate ≠ 0 — the verifier was actually verifying.

### 7.2 The blind rider (stage 5 — the final QA gate)
61 kits (10.3%, grade-stratified, all 21 games) re-judged **blind** by a different agent from dossier+anchors only; steward adjudicated every divergence against source prose. **Element 84% / ailment 77% / grade 51% raw; ~95% / ~97% right-or-defensible after adjudication; ZERO element family-swaps; near-balanced divergence direction ⇒ no run-wide over-silencing or over-attesting bias.** Grade is the honest soft axis (51% inter-rater exact) — but every material grade divergence resolved in the original's favor once engine context was applied. Full adjudication: `stage5/BLIND-RIDER-DIVERGENCE-REPORT.md`.

### 7.3 The audit chain caught errors in EVERY direction (the steward-fallibility register)
- Steward caught mappers: ~40 attestation strikes across basins (element name-only imports dominant mode; ailment leaks; 4 anchor-splices caught by the contiguity battery; 3 over-block RESTORES — the law cuts both ways).
- **elrond + files caught the steward** (×2: W1 rollup arithmetic; basin-3 census correction) — plus steward self-catches (fabricated-census draft; umbral circular-brief; m04 briefing-scope; the basin-5 no-family-list conflation).
- Advisory-drift split: crawl agents 9-for-9 drifted (recount law is the control) · mapping agents 7-for-7 exact · elrond ingests exact throughout. **File-truth recount (D-2c) governs everywhere; advisory numbers were never load-bearing.**

### 7.4 Process findings banked
- **Emission discipline works as MECHANICAL CONTRACT, not stated law** (two monolithic-emission deaths; the ≤2-rows/append + ≥6-calls contract ended them).
- Canary-first wave-firing caught a would-be 13-wave CANTOPEN (brief DB-path bug) for the price of one wave.
- kb **probe-facts are NEVER attestation** (§ 0-UNIVERSAL) — the probe-fabrication series (resource-class instrument, 6-for-6) proved kb resource fields systematically unreliable.

---

## 8. Findings — what the run learned

1. **THE D4 NAME-ONLY LAW is portable — the marquee methodological dividend.** Minted on the Diablo lineage, it held **bidirectionally** on Lost Ark (structurally alien: identity-gauge economy, element-silent prose): name-only rejected ×6, genuine descriptor attested ×1. A law that transfers across engine grammars is a law, not an idiosyncrasy. It then survived the blind rider with zero family-swaps.
2. **kb negative-canon is the least reliable claim family** — the 18-kit trap-skill series closed **44% confirmed / 28% unattested / 28% FALSIFIED**, and the falsifications share ONE root cause: **item-redemption blindness** (kb models base kits, blind to blanket-set/unique/aspect redemption — spectral-blade, wave-of-force, incinerate, kick, wind-shear). Run-wide negative axis: 53% C. **Two-axis frame:** reliability tracks documentation density; failure-COHERENCE tracks churn rate (D2/D3 negatives wrong systematically = learnable; LA negatives wrong randomly = not).
3. **Era is the weak fact-axis (134 of 207 UNSUPPORTED), identity the strong one (96.2% confirmed).** Community sources attest what a build IS far better than WHEN it was. The era-U wall ("guides only attest current season") is structural, not fixable by more crawling.
4. **EXACT-rate inversely tracks build-system depth** (tl2 64% → poe1 2%). The engine's substrate is nearest classic-ARPG grammar; modern modifier-stack identities bend into CLOSE/APPROX. This is the run's clearest signal about where the engine's expressiveness boundary sits TODAY.
5. **The element palette's genre floor is uneven: wind 2 kits, holy 6, shock 1.** The genre rarely damage-types wind (twisters are physical), holy lives only in dedicated paladin kits, and paralysis prose is rare. **Wind/holy identity will have to be engine-AUTHORED, not genre-imported** — the corpus cannot teach what the genre never wrote down. (Direct input to element-identity design work.)
6. **The 16-closed ailment registry SURVIVED 574 kits** — every family exercised, only six no-home statuses encountered (D-6), none forcing expansion. The registry is validated as the project's status vocabulary.
7. **Summoner-deferral is the single largest expressiveness gap by kit-count** (~21 GAPPED kits + army-GAP siblings) — the corpus now quantifies what the Phase-5 deferral costs in genre coverage. Second: party-support scope (solo-only boundary, ~13 kits + the aurabot/LA record).

---

## 9. The honest residue (what this corpus can NOT be trusted for)

1. **207 UNSUPPORTED verify rows stand** (era-dominant). UNSUPPORTED means *no admissible source found*, not false. They are labeled, not laundered.
2. **597 abstained dossier rows (17.3%)** — the mapper saw nothing there; honest-abstain, not thin coverage papered over.
3. **Unverified probe-fact tail:** 623 kb-legacy + 430 named-source-unfetched facts remain below the verified-v1.1 bar. Anything reading `canon_probe_facts` must filter on provenance.
4. **11 unmapped `is_system` records** (zodiac-board, golden-egg-scaling, chaos-dungeon-ladder, gear-well-retrieval, gear-enchant-economy, crown-proc-engine, classless-triad, artifact-stack, link-rune-grammar, privileged-status, monetization-confound) — system/meta records, correctly outside the kit-mapping contract. **8 `is_system` records WERE mapped** (temporalis-blink, low-life-ward, lod-archetype, essence-transfer, omega-magick, resonance-awakening, inferno-ladder, grim-feast) — they carry genuine kit identity despite the system flag; flagged in rosters.
5. **Resource-economy fields for di and d4 Paladin/Warlock are CONTESTED/unreliable** (probe-fabrication series; ERRATA-45/46). Any engine work touching those economies re-verifies first.
6. **Thin-source kits:** the ~5 fully/near-unattested GAPPED kits (snowstorm-frost et al.), the Unattested Register (stun-jacks, shield-bash, soul-feast, grim-ward-U, void-rift ghost), and the open BACKFILL-3 wayback-retry queue.
7. **Grade is judgment, not fact** — 51% inter-rater exact. Treat any single kit's grade as ±1 soft; treat the SHAPE (the § 1 histogram) as reliable.
8. **le-bomb-lance-falconer** was re-keyed mid-run (identity was false); its map reads the re-crawl dossier. le-harvest-lich remains a chimera pending D-7.5.
9. **Author-credit caveats:** Zaodon = question-thread OP, never guide credit; b02 all-unknown; maxroll planner-links are dataset-class, not authored-guide attestation.

---

## 10. Citation export, tracker registration, and what happens next

- **Citation export (charter deliverable):** generation-ready from `kit_citations`; **held at the IP-clearance gate** (`matt_decision_needed/2026-07-13-ip-clearance-devlog-and-hook-surface.md`, still open). Fires within whatever that ruling allows.
- **Tracker-delta (registered on your D-10 go):**
  - `current-to-end-state-serial-content-emission.md` — NEW: VDM-1 corpus complete (574 kits verified/dossiered/mapped, v1.1 pending stamp); the serial-content substrate now has a graded genre-canon reference layer.
  - `current-to-end-state-engine.md` — NEW gaps (from § 5): docket taxonomy → engine-design intake queue (entity-pool, stat-substrate 6-way, out-and-return + two-tier mints, wind/holy element-authoring signal).
- **Post-ratification pass (single batch, on your rulings):** apply D-1 errata (→ ERRATA-56…59) · D-2 crosswalk footnotes · D-7 annotations · D-8 normalizations · v1.1 stamp · tracker writes. One elrond migration + one steward commit.
- **Open forks beyond this run (no action until you say):** VDM-2 (LE re-crawl post-FoA-ship; wayback-retry queue; harvest-lich split) · engine-design intake of ratified mints/dockets · citation export on IP-clearance.

---

## Cross-references
`agentic_orchestration/gandalf/design-inputs/2026-07-18-vdm1-charter.md` (R-8b contract) · `…/2026-07-18-vdm1-crosswalks.md` + basin addenda (the law) · `stage2/poe1/ratified-{docket-rows,mint-candidates}.jsonl` · basin `docket-candidates-*.jsonl` (held rows) · `stage5/` (blind rider) · run-state ledger (full lineage) · `review-book-accumulators.md` (superseded staging index).

Tracker-delta: **held pending D-10** — two NEW-gap lines pre-drafted in § 10; no tracker write until Matt's go (write-authority discipline).

---

**Signed:** gandalf (run steward · SPEC-AUTHOR → DRIFT-CRITIC) — VDM-1 complete: 574/574 kits, 5 basins, 21 games, one autonomous run, zero red-flag pings. The book is the run's single point of truth for your review; every ruling awaits your margin.
