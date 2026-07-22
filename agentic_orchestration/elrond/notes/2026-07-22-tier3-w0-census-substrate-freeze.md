# Tier-3 Encounter-Geometry Run — W0 CENSUS + SUBSTRATE FREEZE

**STATUS:** W0→W1 HANDOFF ARTIFACT (run law L-2 — no W1 grammar derivation before this file exists on disk).
**Author:** elrond (data steward) · 2026-07-22
**Run:** Tier-3 Encounter-Geometry Run · Wave W0 close · conductor gandalf `RUN-CONDUCTOR`
**Charter:** `agentic_orchestration/gandalf/notes/2026-07-22-tier3-encounter-geometry-run-charter.md` (§4 W0 row · §7 T3-V1..V7)
**Run state:** `agentic_orchestration/gandalf/notes/2026-07-22-tier3-encounter-geometry-run-state.md` (rulings L-2, L-8)
**Substrate governed:** the four legolas harvest files under `agentic_orchestration/legolas/harvests/2026-07-22-tier3-era-family-mob-harvest/` (legolas commits `e1693613` + `f71cc21e`). READ-ONLY to elrond — this census does not edit them (freeze means freeze).
**Expectation authority:** Appendix B (era-act × BUILD-FAMILY presence matrix), `canonical/matt_decision_needed/2026-07-22-tier3-encounter-geometry-charter-grill.md` §§ B1–B3.

> **Discipline note.** This is a census-verify-freeze task, not a re-harvest. Where the harvest surfaces a genre hole (a family present in the kit corpus but absent/thin monster-side), that is a PUBLISHED FINDING per run-state L-8a — NOT a coverage failure, and NOT to be filled with fabricated rows. Section (f) records those findings; Section (b) marks the cells `expected-present-but-EMPTY (finding, hole-respected)`.

---

## (a) PER-ERA ROW COUNTS + QUOTA VERIFICATION

Quota per T3-V3: **[15, 30] rows per era.** All four files PASS.

| Age | Source game(s) | Rows harvested | Quota [15,30] | Source split |
|---|---|---:|:---:|---|
| **Age I** | Diablo II (2000) | 20 | ✅ PASS | D2 20 / 20 |
| **Age II** | Path of Exile 1 (2013) | 20 | ✅ PASS | PoE1 20 / 20 |
| **Age III** | Grim Dawn (2016) | 18 | ✅ PASS | GD 18 / 18 |
| **Age IV** | PoE2 (2024) + Last Epoch (2024) | 22 | ✅ PASS | **PoE2 13 / LE 9** |
| **TOTAL** | — | **80** | — | — |

- Age IV split verified against the file's own SUMMARY line ("Source split: 13 rows PoE2 / 9 rows LE"). Cross-checked against the `**PoE2**` / `**LE**` per-row tags: rows 1–13 tagged PoE2, rows 14–22 tagged LE → **13 PoE2 + 9 LE = 22.** Consistent.
- Row-count corroboration: each file's stated `Row count:` header matches its populated row-table body (I=20, II=20, III=18, IV=22). No off-by-one between declared and populated counts.
- Run-state ledger records "80 rows (I:20 · II:20 · III:18 · IV:22)" — this census **confirms** that tally byte-for-byte.

---

## (b) ERA × FAMILY COVERAGE MATRIX

**Rows = build families. Columns = Ages I–IV. Cell = harvest PRIMARY-mapping row-count for that family in that age** (secondary/candidate co-mappings noted in the legend, not double-counted into the primary cell). Each cell is marked against its Appendix-B expectation.

**Legend (per-cell mark):**
- `✓N` = expected-present-and-covered (Appendix B expects present; harvest supplies N primary rows)
- `∅ FINDING` = expected-present-but-EMPTY (Appendix B expects present; harvest supplies 0 monster-side rows → published finding per L-8a, hole-respected, NO fabrication)
- `— hole` = expected-absent-and-empty (Appendix B records absent; harvest correctly supplies 0 → load-bearing hole respected)
- `THIN` = expected-present but coverage is single-secondary-only (published finding)
- `⚠` = mismatch flag requiring conductor/W1 attention (see notes beneath)

Appendix-B expectation per cell is shown as the parenthetical `(exp: …)` where `—` = absent-hole, a number = ratified/docketed count, `+Np` = τ-propagated hypothesis-tier, `N draft` = fresh-draft.

| Family (tier) | Age I · D2 | Age II · PoE1 | Age III · GD | Age IV · PoE2+LE |
|---|---|---|---|---|
| **WHIRLWIND** (RATIFIED) | ✓2 (exp: 3) `#17,#18` | ⚠ ∅ (exp: 1) | ✓1 (exp: 1) `#6` | ✓2 (exp: 2) `#1,#10` |
| **CHANNELED-BEAM** (RATIFIED) | — hole (exp: —) | ✓2 (exp: 2) `#7,#20` | ✓6 (exp: 3+3p read) `#2,#9,#10,#12,#16,#17` | ✓2 (exp: 1) `#9,#19` |
| **AURA** (RATIFIED) | ✓3 (exp: 1) `#14,#15,#18` | ✓2 (exp: 3+1p) `#6,#16` | — hole (exp: —) `see ⚠A3` | ✓3 (exp: 1) `#13,#16,#21` |
| **TOTEM-SENTRY** (RATIFIED) | ✓2 (exp: 0+3p) `#11,#14` | ✓3 (exp: 8+6p) `#3,#4,#14` | ✓1 (exp: 1+2p) `#11` | ✓5 (exp: 7+5p) `#5,#7,#17,#18,#20` |
| **TRAP-MINE** (RATIFIED) | ✓3 (exp: 2+4p) `#9,#13,#20` | ✓3 (exp: 8+4p) `#10,#12,#17` | ✓2 (exp: 0+5p) `#12,#18` | ✓2 (exp: 2+1p) `#3,#15` |
| **MINION-PET** (RATIFIED) | — hole (exp: —, off-spine) | — hole (exp: —) | — hole (exp: —) | — hole (exp: —) |
| **MELEE-STRIKE** (DOCKETED) | ✓8 (exp: 10) `#1,#2,#3,#6,#7,#10,#12,#16` | ⚠ ∅ (exp: —, genre hole) `see ⚠B` | ✓7 (exp: 5) `#1,#3,#5,#7,#8,#13,#14` | ✓1 (exp: 3) `#4` |
| **DOT-AILMENT** (DOCKETED) | ✓6 (exp: 4) `#8,#13,#15,#16,#17,#20` | ✓3 (exp: 15) `#11,#13,#18` | ✓3 (exp: 4) `#4,#11,#16` | ✓2 (exp: 5) `#8,#21` |
| **MULTI-PROJECTILE-VOLLEY** (DOCKETED) | ✓4 (exp: 3) `#4,#5,#7,#11` | ✓2 (exp: 8) `#9,#15` | — hole (exp: —) `see ⚠C3` | ✓4 (exp: 3) `#2,#6,#12,#22` |
| **SHAPESHIFT** (DOCKETED) | ∅ FINDING (exp: 4) `L-8a` | — hole (exp: —) | ∅ FINDING (exp: 1) `L-8a` | ✓1 (exp: 3) `#11` |
| **IDENTITY-GAUGE** (DOCKETED) | — hole (exp: —, off-spine) | — hole (exp: —) | — hole (exp: —) | — hole (exp: —, off-spine) |
| **CHAIN-BOUNCE** (FRESH-DRAFT) | ✓1 (exp: 3 draft) `#19` | ✓1 (exp: 6 draft) `#19` | ✓1 (exp: 5 draft) `#15` | THIN (exp: 5 draft) `#6 secondary only` |
| **DASH-STRIKER** (FRESH-DRAFT) | ∅ FINDING (exp: 1 draft) `L-8a` | — hole (exp: —, not in deck) | ✓2 (exp: 2 draft) `#7,#8` | — (exp: 1 draft, not harvested — see ⚠D) |

**Secondary / candidate co-mappings (NOT counted into primary cells above, but present in the harvest as within-row notes — flagged for W1 so nothing is lost):**
- Age I: CHAIN-BOUNCE also latent in #19 (primary here); MPV tentative on #5 (Blood Hawk dive — filed-but-UNMAPPED-if-strict); TOTEM-SENTRY flavor on #6; TRAP-MINE secondary on #13.
- Age III: CHAIN-BOUNCE *candidate* notes on #4, #5, #6, #17 (Skeletal Warlock arc / Ghostly Tendrim / Valdaran lightning) — primary CHAIN-BOUNCE is #15 only; DOT-AILMENT secondary on #16; TOTEM-SENTRY candidate on #11 (primary); TRAP-MINE candidate on #14.
- Age IV: CHAIN-BOUNCE secondary on #6 (Scarab arc-bolt) — the ONLY CHAIN-BOUNCE signal in Age IV (see finding f-3); WHIRLWIND secondary on #22 (Storm Sweep); CHAIN-BOUNCE secondary on #22 (Storm Burst); TOTEM-SENTRY+MPV dual on #12; AURA+DOT-AILMENT dual on #21; MPV dual-flagged on #22.

### Mismatch flags vs Appendix B (every deviation stated explicitly)

Two classes of deviation exist: **(i) EXPECTED holes correctly respected** (not mismatches — the harvest did the right thing) and **(ii) genuine mismatches** where harvest coverage diverges from the Appendix-B present/absent call. Only class (ii) is a mismatch for the count.

**⚠-A — WHIRLWIND Age II EMPTY (MISMATCH, count = 1).** Appendix B B1 records WHIRLWIND = 1 for Age II (PoE1). The harvest supplies **zero** WHIRLWIND rows for Age II (Age II file summary lists no WHIRLWIND under "Family coverage check" — WHIRLWIND is named in the file's own "ABSENT in Age II" line). **Divergence:** the harvest treats WHIRLWIND as an Age-II *hole*, but Appendix B B1 records 1 on-spine member. This is a present-but-EMPTY cell that L-8 did NOT enumerate. → **Flagged for conductor.** Candidate dispositions for W1: (1) the single B1 WHIRLWIND record is a player-KIT entry with no PoE1 monster-side analog (same class as SHAPESHIFT-I/III and DASH-STRIKER-I — a genre hole on the monster side despite kit presence) → serve via R-b2 RDR-NATIVE-DERIVED; or (2) a targeted Age-II re-crawl if a PoE1 spin-mob is later attested. Recommend disposition (1) pending conductor ruling; do NOT fabricate.

**⚠-A3 — AURA Age III absent-hole is HONORED, but harvest logs a live tension.** Appendix B B1 records AURA = 0 (—) for Age III → the harvest correctly supplies zero primary AURA rows (`— hole`). NOT a mismatch. Recorded here because the Age III ADMISSIONS explicitly note GD's hero "Supporter" archetype IS structurally an aura-emitter but is unratified into the AURA family — a future-docket signal, not a W0 hole violation. W1 should treat AURA-III as a true load-bearing hole per Appendix-B reading 2.

**⚠-B — MELEE-STRIKE Age II: EXPECTED hole, correctly respected (NOT a mismatch).** Appendix B B2 records MELEE-STRIKE = 0 on-spine for PoE1 ("0 of 36 docket members are poe1" — the famous PoE1 melee deficit, Appendix-B reading 2). The Age II harvest correctly supplies zero MELEE-STRIKE primary rows and explicitly marks row #8 (Blackguard Elite wedge) UNMAPPED "to honor the Age II MELEE-STRIKE zero-record genre hole." This is the harvest doing exactly the right thing. `∅` in the matrix carries `(exp: —, genre hole)` → hole respected, **not counted as a mismatch.**

**⚠-C3 — MPV Age III: EXPECTED hole, correctly respected (NOT a mismatch).** Appendix B B2 records MPV = 0 (—) for Age III. Harvest supplies zero and confirms via the Gunman page that GD ranged fire is single-shot not fan-volley ("use only one-handed ranged weapons") → hole is real. `— hole` → not a mismatch.

**⚠-D — DASH-STRIKER Age IV: EXPECTED present (1 draft) but NOT harvested (MISMATCH, count = 1).** Appendix B B3 records DASH-STRIKER = 1 for Age IV (fresh-draft). The Age IV harvest supplies **zero** DASH-STRIKER rows and does not mention the family in its coverage check. **Divergence:** a fresh-draft-tier expected-present cell with no harvest row and no admission logged. Per T3-V2, FRESH-DRAFT is excluded from *serving* — so a missing DASH-STRIKER-IV row does not block W1 serving. But it is an uncatalogued gap relative to Appendix B. → **Flagged for conductor.** Disposition options: accept as fresh-draft-tier non-obligation (T3-V2 excludes fresh-draft from serving, so no W1 impact); or note as a next-lap admission. Recommend: **accept, log as finding f-5** (no fabrication; no re-crawl obligation given fresh-draft tier).

**Cells where the harvest EXCEEDS the Appendix-B ratified/docketed count** (over-coverage — surplus, not a mismatch, but noted for W1 so the grammar author knows the density): AURA-I (3 vs 1), CHANNELED-BEAM-III (6 vs 3+3p), CHANNELED-BEAM-IV (2 vs 1), AURA-IV (3 vs 1), DOT-AILMENT-I (6 vs 4), MELEE-STRIKE-III (7 vs 5), MPV-I (4 vs 3), MPV-IV (4 vs 3), TRAP-MINE-III (2 vs 0+5p). These are counts *inclusive of secondary-role rows and boss specimens* and reflect the harvest's generous within-quota coverage; Appendix B counts are record-class kit-membership tallies, so exact numeric equality is NOT expected — the meaningful check is present/absent agreement, which holds for all these cells.

### Mismatch count (present/absent-disagreement class only)

**2 genuine mismatches:** ⚠-A (WHIRLWIND-II expected-present, harvest-empty) · ⚠-D (DASH-STRIKER-IV expected-present fresh-draft, harvest-empty).
All other deviations are either **expected holes correctly respected** (MINION-PET ×4, IDENTITY-GAUGE ×4, CHANNELED-BEAM-I, MELEE-STRIKE-II, MPV-III, AURA-III, SHAPESHIFT-II, DASH-STRIKER-II) or **surplus over-coverage** (numeric, present/absent-agreeing) or **the three L-8-pre-enumerated findings** (SHAPESHIFT-I, SHAPESHIFT-III, DASH-STRIKER-I) recorded in Section (f).

---

## (c) PROVENANCE AXIS

Per run-state ruling **L-8b**, the census carries a **two-value provenance axis per row-source**, so W1-derived rows can later join the census carrying the complementary flag.

| Provenance value | Definition | Row-source | Count at FREEZE |
|---|---|---|---:|
| **GENRE-ATTESTED** | The encounter/mob is cited from a shipped genre game (source citation present; behavior reconstructed from wiki/guide/bestiary). | legolas W0 harvest (all 80 rows). | **80** |
| **RDR-NATIVE-DERIVED** | The mob template is DERIVED from a family kit-leader's mechanism verbs (R-b2), for families where the genre has NO monster-side attestation. RESERVED for W1's R-b2-derived templates. | W1 grammar spec (SPEC-AUTHOR, named-gandalf). | **0** |

**Declaration:** at substrate-freeze time, **all 80 harvest rows carry `GENRE-ATTESTED`; ZERO rows carry `RDR-NATIVE-DERIVED`.** The RDR-NATIVE-DERIVED value is reserved and empty. W1 will populate it for the kit-present/monster-absent-or-thin families identified in Section (f) (SHAPESHIFT-I, SHAPESHIFT-III, DASH-STRIKER-I, CHAIN-BOUNCE-IV, and — pending conductor ruling — WHIRLWIND-II per ⚠-A).

**Join key for W1.** Every harvest row is uniquely addressable as `(age ∈ {I,II,III,IV}, source ∈ {D2, PoE1, GD, PoE2, LE}, row_number)`; Age IV disambiguates on the `**PoE2**`/`**LE**` per-row tag. W1-derived rows should carry `(age, family, derivation_source = <kit-leader>, provenance = RDR-NATIVE-DERIVED)` and slot into the same family×age matrix cells that Section (b) marked `∅ FINDING` or `THIN`. The census structure (family × age × provenance) admits the union cleanly — no schema change needed to absorb the RDR-NATIVE-DERIVED rows, because provenance is a TAG column, not encoded into the row identity (Discipline #14 spirit: tag, don't encode).

---

## (d) UNMAPPED LEDGER

**7 UNMAPPED rows** (harvested but not cleanly mapped to a build family). Aggregated across the four files. Each carries what a mapping ruling would need.

| # | Source · Age | Row | The unmapped subject | What a mapping ruling would need |
|---|---|---|---|---|
| U-1 | D2 · I | Age I #5 | Blood Hawk aerial dive-and-scatter | Ruling on whether a melee-DIVE with multi-vector convergence counts as MPV (filed tentatively there) or is its own verb. Strict mechanism-identity would push it out of MPV. Needs: MPV boundary definition (true-ranged-projectile vs converging-dive). |
| U-2 | D2 · I | Age I #1, #12 | Fallen/Fetish Shaman **resurrection anchor** | Resurrection-as-encounter-verb is owned by no current family. Needs: a ruling on whether "revive-the-fallen leader" is (a) a TOTEM-SENTRY variant (emplace-and-sustain), (b) a MINION-PET re-seed candidate, or (c) a new verb. (Recurs in III as U-6 — same mechanism, cross-era.) |
| U-3 | PoE1 · II | Age II #1 | Rhoa physical-charge swarm | Needs: a home for pure physical-charge with no Age-II family match. MELEE-STRIKE is the obvious semantic fit but is a load-bearing PoE1 hole (⚠-B) → cannot map there without violating the hole. Ruling needed: does a charge-swarm map to WHIRLWIND (spin-and-close) or stay UNMAPPED to honor the melee hole? |
| U-4 | PoE1 · II | Age II #2 | Zombie herd slow-melee push | Same as U-3: slow-overwhelm melee with no Age-II family (MELEE-STRIKE absent). Ruling needed: UNMAPPED-to-honor-hole vs derived-mapping. |
| U-5 | PoE1 · II | Age II #5 | Spider-nest environmental mass-spawn | Spawner is ENVIRONMENTAL (egg sac / ceiling anchor), not a placed unit — closest is TOTEM-SENTRY spawn-mechanic but the emplacement is terrain, not a mob. Needs: ruling on whether environmental-spawner nests are a TOTEM-SENTRY sub-type or a distinct "nest/spawner" verb. |
| U-6 | GD · III | Age III #9 | Aetherial Dominator **zombie-resurrection** leader-role | Resurrection-leader role (raises battlefield dead as melee screen); thematically MINION-PET-adjacent but mechanism-distinct (no taunt/tank). Dominator itself is mapped CHANNELED-BEAM for its beam; the resurrection role is orphaned. Needs: same ruling as U-2 (cross-era resurrection-leader verb). |
| U-7 | LE · IV | Age IV #14 | Void Horror **three-body simultaneous-reveal** convergence | Isolation-break / multi-body-aggro-trigger is the primary formation identity; DOT-AILMENT (void proximity) is the closest single-family verb but does not capture the convergence-trigger. Needs: ruling on whether "engage-one-reveals-all" convergence is a FORMATION-tier (MESO) property orthogonal to family, or warrants a family verb. |

**Cross-era pattern for the conductor:** U-2 + U-6 are the **same mechanism in two ages** (Shaman/Dominator resurrection-leader). A single ruling ("resurrection-leader verb") resolves both. Legolas's own summaries independently flag this D2↔GD parallel. Recommend the W1 SPEC-AUTHOR treat resurrection-leader as one candidate MICRO-verb spanning Ages I+III, not two isolated UNMAPPEDs.

---

## (e) ADMISSIONS LEDGER

Aggregated **over-quota / caveat admissions** from the four files into one numbered ledger. Each attributed to its file. (These are T3-V3 next-lap candidates — logged, never silently promoted to rows.)

**Total: 21 admissions** (I: 4 · II: 5 · III: 5 · IV: 7).

**From `age-I-diablo2.md` (4):**
- A-I.1 — DASH-STRIKER Age I: no dedicated dash-teleport mob in D2; Fanatic-enchanted +100% move-speed is the closest (speed-mod, not dash-skill). Age-I DASH-STRIKER presence may be player-kit-only. (→ becomes finding f-2.)
- A-I.2 — SHAPESHIFT Age I: no monster-side shapeshifter at mob-template level; Andariel poison-metamorphosis flavor + Possessed champion modifier are thematically adjacent, mechanically distinct. Player-class origin. (→ becomes finding f-1.)
- A-I.3 — Andariel boss (Act 1 Catacombs L4): poison DoT + charge in small chamber; strong DOT-AILMENT+DASH-STRIKER pattern but single unique boss, not a mob template.
- A-I.4 — Duriel boss (Act 2 Tal Rasha's Chamber): extreme-close-range boss, Holy Freeze aura + charge in tiny room; AURA+DASH-STRIKER; single-boss, not repeatable template.

**From `age-II-poe1.md` (5):**
- A-II.1 — Spinning Doedre (Act 3 Sewers): channels persistent Chaos-Degen DoT pools with spinning direction change; strong DOT-AILMENT boss; excluded to avoid boss over-inflation.
- A-II.2 — Blackguard Mage arc-cast groups (Ebony Barracks): pure arc-chain packs (CHAIN-BOUNCE) distinct from Arcmage beam; rows 7+19 cover the family adequately.
- A-II.3 — Ribbon Spool container mechanics (The Docks): supply containers spawn magic-monster bursts; strong TRAP-MINE pre-seeded spawn, but sourcing thin (secondary description only).
- A-II.4 — Hailrake (Act 1 boss) + Ice Elemental retinue: Ice Nova fan-volley from elementals; MPV specimen; excluded (boss tier over-represents sample).
- A-II.5 — Piety (Act 3) channeled ice-beam sweep with transformation phases: CHANNELED-BEAM boss; row 20 already covers beam; Piety adds a beam+transform note for W1.

**From `age-III-grim-dawn.md` (5):**
- A-III.1 — SHAPESHIFT Age III: GD Shaman enemy (Bloodsworn Summoner Chthonian transforms) is summoner-variant not body-morph; single Appendix-B Shapeshift record likely player-kit. (→ becomes finding f-1.)
- A-III.2 — Ravager boss (optional Celestial, Barrowholm): three-form shapeshifter (Flesh/Soul/Mind) + TOTEM-SENTRY secondary in Mind form; exceptionally strong SHAPESHIFT+TOTEM pattern BUT post-story optional, not a representative mob template.
- A-III.3 — Chthonian Bloodkeeper (Acts 5/6): strong DoT Chthonian in Void areas, but Acts 5/6 are DLC (Ashes of Malmouth / Forgotten Gods), out of base-GD Age III scope.
- A-III.4 — AURA Age III: GD hero "Supporter" archetype (aura for nearby allies) is structurally AURA but unratified into the family; potential future docket candidate. (Relates to ⚠-A3.)
- A-III.5 — MPV Age III: GD Gunman ranged fire is single-shot not fan-volley (confirms the hole per ⚠-C3).

**From `age-IV-poe2-le.md` (7):**
- A-IV.1 — PoE2 Zarokh (Trial of Sekhemas): stationary time-mines + counter-clockwise lightning-beam sweep; dual TRAP-MINE+CHANNELED-BEAM; excluded as ascendancy-system, not act-spine.
- A-IV.2 — PoE2 Rathbreaker (Act 2): hyena swarm + cliff-archer combo; strongest MELEE-STRIKE+MPV split in PoE2 act spine; row 4 covers the family, Rathbreaker adds two-tier simultaneous-pressure refinement.
- A-IV.3 — PoE2 Krutog, Lord of Kin (Act 4): direct WHIRLWIND boss (beetle-body spinning charge); cleanest single-entity WHIRLWIND in PoE2; row 10 covers family.
- A-IV.4 — LE Crystal Lotus (Crystal Mines): SHAPESHIFT crystallized-elemental beast that transforms; adds a non-boss-tier shapeshift patrol; row 11 covers family. (Relevant to f-1 mitigation for Age IV.)
- A-IV.5 — LE Spymaster Zerrick (Imperial Era): DOT poison pool + invulnerability-hide; strong DOT-AILMENT stack-and-retreat boss; row 21 covers family.
- A-IV.6 — LE Osprix swarm (Divine Era Scorched Grove): fire-damage MELEE-STRIKE swarm variant; row 4 covers family; Osprix adds a fire-typed melee swarm.
- A-IV.7 — PoE2 Xyclucian, the Chimera (Act 3 boss): tri-elemental SHAPESHIFT (three-head alternating form); row 11 (Geonor) anchors; Xyclucian would be a second specimen confirming SHAPESHIFT as an Age-IV strength.

> **Reconciliation with the run-state "~20 admissions" estimate:** the run-state ledger records "20 admissions" as an approximation; the exact aggregate is **21** (4+5+5+7). No admission was dropped or double-counted; the delta is the estimate rounding down.

---

## (f) COVERAGE FINDINGS (per run-state L-8a — PUBLISHED FINDINGS, not harvest failures)

Verified against the Section (b) matrix. The three L-8-pre-declared findings are confirmed, plus additional thin/absent cells the matrix surfaced.

**L-8-pre-declared findings — VERIFIED against the matrix:**

- **f-1 — SHAPESHIFT monster-side ABSENT in Ages I + III.** Matrix cells SHAPESHIFT-I and SHAPESHIFT-III both `∅ FINDING`. **CONFIRMED.** Genre history holds SHAPESHIFT as player-kit-origin only (D2 Druid tree; GD player-transmog). Optional post-game bosses (D2 none clean; GD Ravager three-form) excluded as non-representative. Appendix B records 4 (I) and 1 (III) — these are record-class KIT memberships, not monster templates. **W1 serves via R-b2 RDR-NATIVE-DERIVED.** Age IV DOES have monster-side SHAPESHIFT (row #11 Count Geonor human→wolf) — so the finding is I+III-specific, not universal. Zero fabrication.
- **f-2 — DASH-STRIKER ABSENT in Age I.** Matrix cell DASH-STRIKER-I `∅ FINDING`. **CONFIRMED.** No dedicated dash-teleport mob in D2 (Fanatic speed-mod is closest but is a modifier, not a dash-skill — admission A-I.1). Appendix B records 1 (fresh-draft) = player-kit. **W1 serves via R-b2 RDR-NATIVE-DERIVED.** Age III DOES have monster-side DASH-STRIKER (rows #7/#8 Cronley Murderer Shadow Strike) — finding is Age-I-specific.
- **f-3 — CHAIN-BOUNCE Age IV THIN (Scarab secondary only).** Matrix cell CHAIN-BOUNCE-IV `THIN` (row #6 Scarab arc-bolt is a SECONDARY note under an MPV-primary row; no dedicated primary CHAIN-BOUNCE row in PoE2/LE). **CONFIRMED.** The Age IV file's own source-quality note recommends this as a W1 grammar gap (Arc is a PoE2 skill; act-spine CHAIN-BOUNCE encounters would need a poe2db direct pass). Ages I/II/III each have a primary CHAIN-BOUNCE row (#19/#19/#15) — Age IV is the sole thin cell. **W1 serves via R-b2 RDR-NATIVE-DERIVED** (kit corpus carries ~5 CHAIN-BOUNCE record kits in Age IV per Appendix B B3 — Lightning Blast / arc analogs available as derivation leaders).

**ADDITIONAL thin/absent cells surfaced by this census (beyond the three L-8 findings):**

- **f-4 — WHIRLWIND Age II EMPTY (NEW; = ⚠-A).** Matrix cell WHIRLWIND-II `⚠ ∅`. Appendix B B1 records WHIRLWIND = 1 for Age II; harvest supplies zero. This is a **fourth kit-present/monster-empty cell** in the same class as f-1/f-2/f-3, NOT enumerated in L-8. **Escalation-worthy:** L-8 named three findings; the census finds a fourth. Recommend the conductor either (a) fold WHIRLWIND-II into the L-8 finding-set and serve via R-b2 RDR-NATIVE-DERIVED (consistent with f-1/f-2/f-3 treatment), or (b) ratify a targeted Age-II re-crawl. Given PoE1's structural melee/spin deficit (same root as the MELEE-STRIKE-II hole), disposition (a) is the coherent call. **No fabrication pending ruling.** This is a red-flag-class item per Section (h).
- **f-5 — DASH-STRIKER Age IV NOT HARVESTED (NEW; = ⚠-D).** Appendix B B3 records DASH-STRIKER = 1 (fresh-draft) for Age IV; harvest supplies zero and logs no admission. Fresh-draft tier → T3-V2 excludes from serving → **no W1 serving obligation.** Recorded as a finding for completeness (no re-crawl obligation, no fabrication). If W1 wants DASH-STRIKER coverage in Age IV it would derive via R-b2 like f-2.
- **f-6 (informational, NOT a coverage gap) — DOT-AILMENT under-density vs kit mass in Age II.** Appendix B records DOT-AILMENT = 15 for Age II (its largest single-age kit cell — the "attrition act"); harvest supplies 3 primary rows. This is WITHIN quota and present (not a hole), but the harvest sampled DOT-AILMENT at ~1/5 its kit-mass proportion. **Not a failure** — quota is [15,30] total rows/era, not per-family proportional — but the W1 SPEC-AUTHOR should know that Age II's signature family (DOT-AILMENT) is present-but-lightly-sampled if per-family formation richness matters for MESO derivation. Same pattern milder for MPV-II (2 rows vs 8 kits) and TOTEM-II (3 vs 8+6p). Informational only; no action required; no fabrication.

**Findings summary:** 3 L-8-confirmed (f-1, f-2, f-3) + 2 new coverage-empties (f-4 escalation-worthy, f-5 fresh-draft-non-obligation) + 1 informational density note (f-6). **All holes stay load-bearing; zero rows fabricated to fill any finding.**

---

## (g) SUBSTRATE FREEZE STAMP

**Command:** `md5 -q <file>` run 2026-07-22 against the four harvest files at their committed state (legolas commits `e1693613` + `f71cc21e`).

| File | md5 (`md5 -q`) | Rows | Lines |
|---|---|---:|---:|
| `age-I-diablo2.md` | `9b41f22c219c181cc8f395d024174c05` | 20 | 96 |
| `age-II-poe1.md` | `f3ae9f6e9ea69f7f775f7de91c4d72f0` | 20 | 89 |
| `age-III-grim-dawn.md` | `b255680354a314c454ab9712386fc63d` | 18 | 97 |
| `age-IV-poe2-le.md` | `0dcae6ad75977dc10f65014137fc4ce7` | 22 | 103 |

**TOTAL ROW COUNT: 80** (I:20 · II:20 · III:18 · IV:22). **Source split at Age IV: 13 PoE2 / 9 LE.**

**FREEZE DECLARATION:**

> **Substrate FROZEN for W1 derivation as of this stamp.** The four md5 hashes above define the immutable W0 substrate. Any post-freeze edit to a harvest file invalidates the stamp and requires conductor re-freeze (a fresh census pass re-computing the md5s and re-verifying the matrix). W1 grammar derivation proceeds against THIS frozen state only. Per run law L-2, this census file is the W0→W1 handoff artifact; its existence on disk unblocks W1.

---

## (h) DATA-STEWARD OBSERVATIONS (for the W1 grammar SPEC-AUTHOR)

Items the W1 spec-author should know. Where a data ERROR is found, it is LOGGED here and NOT fixed in the harvest files (freeze means freeze).

**Schema-shape drift across the two-agent split (L-5: agent-A did I+III, agent-B did II+IV):**

1. **Column-header casing/structure differs between the pairs.** Files I+III use `| # | Area Archetype | Formation | Pressure Pattern | Faction-Camp Structure | Family Mapping | Source Citation |` (Title Case, hyphen in "Faction-Camp"). Files II+IV use `| # | Area archetype | Formation | Pressure pattern | Faction-camp structure | Family mapping | Source citation |` (sentence case, "Faction-camp"). **Same six-column semantics, different casing.** W1 ingestion must normalize header case; do NOT assume byte-identical headers. No data loss — purely cosmetic drift, exactly the pair-split risk L-5 flagged.

2. **Family-deck preamble format differs.** I+III render the Appendix-B family deck as a prose "PRESENT / ABSENT" bullet block ("## Appendix-B Family Deck"). II+IV render it as a `| family | Tier | Age N count | Notes |` table ("## Families PRESENT"). Both are faithful to Appendix B; the presentation diverges. W1 should read the ROW TABLE + SUMMARY as authoritative, not the preamble format.

3. **Per-row source-game tagging exists ONLY in Age IV** (the `**PoE2**` / `**LE**` bold prefix in the Area column), because Age IV is the only two-game era. Ages I/II/III are single-game and carry the game in the file header only. W1 join logic must branch: Age IV needs the per-row tag for the source dimension; Ages I–III inherit source from the file. **No error** — correct handling of the mixed-source era — but a shape asymmetry to code around.

**Citation gaps (logged, not fixed):**

4. **Age II citation thinning on later rows.** Rows 17, 18 in Age II cite only "Maxroll campaign guide" + a zone-analysis descriptor without a primary wiki URL (poewiki.net was 403/Anubis-blocked per the file's source-quality note; poedb/fandom partial). Rows 1–16 are better-anchored. **Not disqualifying** (Maxroll is an accepted secondary), but Age II has the softest citation floor of the four files. W1 should treat Age II formation details as MEDIUM-confidence where the only cite is the campaign guide.

5. **Age IV LE rows are single-source-dominant.** All 9 LE rows (14–22) lean on vulkk.com + maxroll.gg (LE 1.0 era, Feb 2024). The file flags that LE Season 3 (2026) added enemy-behavior overhauls NOT reflected. **Temporal-staleness note for W1:** LE formation data is 1.0-era; if the encounter grammar is meant to reflect current LE, a Season-3 delta pass is a future-lap item (not a W0 obligation).

**Duplicate-suspect rows (logged, not fixed):**

6. **Age III #13 vs #14 are near-duplicate (Manticore).** #13 = Jagged Waste Manticore *patrol* (MELEE-STRIKE); #14 = Blood Grove Manticore *nest+young-spawner* (MELEE-STRIKE + TRAP-MINE-candidate). The file explicitly distinguishes them by "nest structure and young-spawner presence" — a defensible patrol-vs-nest split, NOT a true duplicate, but they share a creature and a primary family. W1 should keep them as two MESO-formation variants (patrol-line vs nest-defense) of one creature, not two independent family exemplars. Flagged so the density read on MELEE-STRIKE-III (7 rows) accounts for this shared-creature pair.

7. **Age I #11 and Age I #14 both supply the ONLY two TOTEM-SENTRY-I rows AND both also carry MPV/AURA co-mappings.** #11 (Arcane Sanctuary Lightning Spires + Specter volley) and #14 (Council Fire Hydra + aura variants) are legitimately distinct areas, but Age I's entire TOTEM-SENTRY and much of its AURA/MPV coverage concentrates in these two multi-family rows. **Not an error** — but a fragility note: if either row is later re-scoped, three family cells thin at once. W1 should be aware Age-I TOTEM-SENTRY rests on a 2-row base, both multi-family.

**Family-name spelling / label variants:**

8. **No spelling variants of family names found across the four files** — all use the canonical docket labels (WHIRLWIND, CHANNELED-BEAM, AURA, TOTEM-SENTRY, TRAP-MINE, MELEE-STRIKE, DOT-AILMENT, MULTI-PROJECTILE-VOLLEY, SHAPESHIFT, CHAIN-BOUNCE, DASH-STRIKER, MINION-PET, IDENTITY-GAUGE). Consistent. **Reminder (T3-V2 / charter §5):** these remain WORKING LABELS — Matt's names-review is pending; W1 artifacts must NOT serve them as canon.
9. **Minor typo (logged, not fixed): Age II row 10 "wrath forms channel lane"** — appears to be a typo for "wraiths form" (context: "Dockhand Wraiths"). Cosmetic; does not affect the family mapping (TRAP-MINE via Brittle Corsair death-burst). Freeze-preserved as-is.

**RED-FLAG-CLASS observations (elevated for conductor attention):**

- **RF-1 (= f-4 / ⚠-A): WHIRLWIND Age II is an unenumerated kit-present/monster-empty cell.** L-8 declared THREE such findings (SHAPESHIFT-I/III, DASH-STRIKER-I, CHAIN-BOUNCE-IV-thin); this census finds a FOURTH (WHIRLWIND-II). It is directly analogous and almost certainly the same class (PoE1 spin/melee deficit), but it was not in the L-8 disposition. **Per charter §6, in-run reclassification is jack-ryan Gate-2 territory** — this finding should ride to Gate-2 alongside the L-8 set so the finding-count is corrected from 3→4 before W1 derives. Recommended disposition: fold into RDR-NATIVE-DERIVED serving (consistent with the other three). Flagging, not deciding — the reclassification authority is jack-ryan's per §8.
- **RF-2 (informational): the two genuine present/absent mismatches (⚠-A WHIRLWIND-II, ⚠-D DASH-STRIKER-IV) both sit in FRESH-DRAFT-or-single-record cells** — neither threatens a RATIFIED-tier serving obligation. The substrate is sound for W1's serving purpose (RATIFIED + DOCKETED families all have ≥1 covered cell in every era where Appendix B expects them present, EXCEPT the two findings f-1/f-2 which L-8 already dispositioned to RDR-NATIVE-DERIVED). **No substrate-integrity danger** per charter §6 classes.

---

**Census complete. Substrate FROZEN. W0→W1 handoff satisfied (L-2). W1 grammar derivation may proceed against the frozen md5 stamp.**

*Filed by elrond (data steward), 2026-07-22.*
