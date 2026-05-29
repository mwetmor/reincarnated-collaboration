# Experiential Cascade Architecture — Recognition Record

> **STATUS:** CURRENT (recognition record as of 2026-05-29) — Architectural commitments DEFERRED per § 3 empirical-evidence gates. Synthesis captured NOW; canonical promotion to load-bearing architecture (doc 38 amendment + possible new doc 52) gated on empirical validation per recognition-validate-commit discipline. NOT a load-bearing canonical doc until gates resolve.

**Date:** 2026-05-29
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-05-29 in-session synthesis (paste-conversation surfaced during Phase A2 cascade-fire offline-work window) + Matt 2026-05-29 ratification of canonicalization path (recognition record now; legolas Mode A research authored; doc 38 amendment + doc 52 promotion DEFERRED to empirical-evidence gates)

## 0.1 Amendment-pass-record

| # | Date | Author | Amendment scope | Empirical trigger |
|---|---|---|---|---|
| Initial | 2026-05-29 | gandalf | Recognition record authored per Matt 2026-05-29 paste-conversation synthesis + canonicalization-path ratification (commit `346075e`) | (initial authoring) |
| Amendment 1 | 2026-05-29 | gandalf | **Wave B finding amendment** — KR empirical refutation at cascade-resumption-2 Step 4 (commit `fd48cab`): `grep -rE 'wave_b\|WaveB\|run_wave_b' reincarnated-engine/src/` returns ZERO matches engine-wide. Wave B per-kit identity LLM is NOT BUILT in production code. § 2.1 cascade chain Step C component status corrected from "Built; UNTESTED" → "NOT BUILT; phantom component"; § 2.3 unbuilt seams expanded; § 3 gate (i) disposition refined to PARTIAL PASS (Wave A + F-C verified coherent; Wave B refuted as built component; full gate (i) PASS requires Wave B operational). Captures Disc #42a Instance-6 case-type (component-existence-context propagation across artifacts without empirical verification) — recognition record IS one of the propagation surfaces (parallel to 5+ dispatches + 4 completion records + orchestrator docstring `wave5_season_orchestrator.py:12`). | KR empirical grep finding 2026-05-29 commit `fd48cab` |
| Amendment 2 | 2026-05-29 | gandalf | **ENDGAME_ENCOUNTER_CATALOG class-taxonomy ROOT-CAUSE finding** — Matt 2026-05-29 intuition: "the labels you listed look like a vestigial hand-crafted naming convention from either cycle 13 or cycle 12 which this cycle 14 was specifically designed to counteract." Empirical verification: `reincarnated-engine/src/reincarnated/generation/endgame_encounter_catalog.py` is Cycle 13 SC-6 hand-crafted artifact (file header line 2: "WU-R2 — 18 endgame-reference encounter definitions for **Cycle 13 SC-6**"). All 18 entries use class names in `archetype_name` field ("Heavy Barbarian", "Standard Wizard", "Channeling Cleric", "Holy Knight", "Storm Caller", "Monk", "Dagger Assassin", etc.); `encounter_id` embeds class names; `intent` descriptions reference "the class" throughout; `cohort_notes` make class-bound assignments. **No-classes architectural recommitment** (Matt 2026-05-27 verbatim per `agentic_orchestration/gandalf/notes/2026-05-27-no-classes-architectural-recommitment.md`) landed at player-architecture layer (doc 48 VESTIGIAL'd; engine commit `0a5a4f2` reverted at `c9fcb1d`) but NOT at substrate-input layer. **Cascade architecture's substrate-led emergence promise is operating against pre-imposed class-taxonomy substrate** — this is the ROOT CAUSE of degenerate PM-1 fallback clustering + shallow gauntlet variant enumeration + downstream-collapse-to-base-character; Wave B phantom (Amendment 1) and other findings are downstream symptoms. Matt 2026-05-29 elected (per CLAUDE.md Engine > Game > Phase orientation): "erase class concept at all levels, then construct the Wave 2 [Wave B] LLM naming, then fire the full engine gen again with Wave 2 [Wave B] LLM entity naming." Cascade-resumption-3 authorization at `agentic_orchestration/gandalf/notes/2026-05-29-cascade-resumption-3-class-eradication-authorization.md` operationalizes the eradication + Wave B + cascade-architecture completion (Streams S1-S6; ~6-10d engine + LLM + Gate-2 before A2-1 RE-FIRE-3). § 2.3 unbuilt seams expanded: class-free substrate-input layer + gauntlet variant enumeration expansion + Phase 4 archive variant preservation now load-bearing prerequisites for cascade architecture substrate-led emergence promise. Cycle 14 v1 trajectory: ~5-9d additional wall-clock vs prior cascade-resumption-2 path; Engine > Phase per CLAUDE.md. | Matt 2026-05-29 empirical intuition + KR + gandalf catalog file inspection commit (this batch) |

**Companion docs:**
- `canonical/38-downstream-delivery-strategy-2026-05-23.md` — keystone delivery strategy (D1-D10); engine commercial framing refinement DEFERRED to this recognition record's gate (iv)
- `canonical/39-qd-engine-end-to-end-workflow-2026-05-24.md` — production canonical engine architecture (Phase 2-7 pipeline; cascade architecture this record names rests on doc 39's pipeline)
- `canonical/47-damage-scaling-architecture-2026-05-27.md` — damage scaling architecture; experiential archetype dimension extends from T4 capstone work this doc canonicalized
- `canonical/50-bounded-viability-with-specialization-design-directive-2026-05-28.md` — bounded-viability-with-specialization design directive; experiential archetype dimension composes orthogonally with bounded-viability design targets
- `canonical/51-investment-scaling-6-pattern-architecture-2026-05-28.md` — investment scaling architecture; per-archetype investment patterns may emerge as Pattern 6+ candidates in Cycle 15+
- `canonical/story/skill-system-2026-05-24.md` — skill composition pattern (element × geometry × tempo × amplitude × tier_coefficient); experiential archetype is the orthogonal dimension this composition lacks
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` — 8 BC axes operational truth; experiential archetype dimension is the THIRD coordinate space orthogonal to BC + cultural-tradition
- `canonical/story/ab-comparison-protocol-cycle-14-close-2026-05-27.md` — A/B comparison protocol; consumes cascade outputs; this record gates on protocol verdict
- `canonical/story/fate-genre-recognition-and-mobile-alignment-trajectory-2026-05-23.md` — Fate-genre recognition record; faction emergence + Rift cross-cultural merge composes with cascade
- `agentic_orchestration/gandalf/notes/2026-05-29-legolas-mode-a-arpg-archetype-vocabulary-research-brief.md` — legolas Mode A research brief; gate (ii) primary instrument
- `agentic_orchestration/gandalf/notes/2026-05-27-path-1-phase-4-5-7-cycle-14-scope-expansion.md` — Path 1 scope; antagonist/contrast-faction generation seam scoped as Cycle 15+ candidate per this record's gate (iii)

---

## 0. TL;DR

A synthesis emerged in Matt's offline-work design session 2026-05-29 that ties together architectural layers we've been building separately. The synthesis (Matt's verbatim sentence):

> **"Cohesion judge labels the magic find rogue as a pirate; clustering builds the pirate faction; playing the pirate faction auto-selects for colonial militia/privateers as major enemy factions. This is the differentiated experience, automated."**

This recognition record:
- **Captures** the cascade architecture this sentence reveals
- **Names** the experiential archetype dimension as the third coordinate space (orthogonal to BC mechanical + cultural-tradition)
- **Defers** architectural commitments per recognition-validate-commit discipline; ALL canonical promotion gated on empirical evidence per § 3
- **Registers** predictions for future empirical validation per § 4
- **Surfaces** antagonist/contrast-faction generation as Cycle 15+ engine seam candidate (NOT a v1 commitment)
- **Does NOT** lock the experiential archetype taxonomy (5 Maxroll-style labels); locks DEFERRED to legolas Mode A genre-community-vocabulary research per gate (ii)
- **Does NOT** amend doc 38 (engine commercial framing refinement); amendment DEFERRED to gate (iv)

**Why this is a recognition record, not a load-bearing canonical doc:** the cascade synthesis spans built infrastructure (PM-1 clustering, Phase 5 Wave A + F-C + Wave B) + just-firing-now infrastructure (Wave A first production exercise per Path D flip authorized 2026-05-29) + UNBUILT infrastructure (antagonist/contrast-faction generation; Cycle 15+ scope). Treating the cascade as load-bearing canon NOW would commit doc 38-keystone-class architectural promises against components that haven't been empirically validated. The recognition-validate-commit pattern (Discipline #42a-adjacent) says: recognize the synthesis NOW; validate against empirical evidence per § 3; commit canonical promotion only after gates resolve.

---

## 1. The recognition — what the cascade architecture is

### 1.1 The chain Matt's sentence articulates

| Step | Engine component | What it does | Substrate-led discipline check |
|---|---|---|---|
| **A — Player intent** | (player input layer) | Player expresses experiential archetype preference (Magic Find / Boss Speed Run / Swarm Clear / ...) | Pre-imposed taxonomy candidate — see gate (ii); validated as community-emergent if cross-site vocabulary converges |
| **B — Mechanical generation** | Phase 2 BC discovery | Generates kit with mechanical archetype + BC-axis position; experiential archetype shapes generation toward player intent | Substrate votes — BC axes are operational truth per qd-engine-bc-axes-lock |
| **C — Cohesion-judge labeling** | Phase 5 Wave B (per-kit identity) | LLM reads mechanical kit + experiential archetype position + substrate vocabulary → produces substrate-thematic identity ("pirate") | Substrate vocabulary is the input; LLM is the cohesion judge; identity emerges, NOT imposed |
| **D — Faction clustering** | Phase 3 PM-1 multimodal clustering | Multiple kits sharing substrate-thematic-identity-adjacency cluster into emergent faction | Clusters emerge mathematically; substrate votes; PM-1 is the math hotspot |
| **E — Faction naming** | Phase 5 Wave A (faction-level LLM) | LLM reads cluster reps + substrate evidence → produces faction-level identity label ("Pirate Brethren") | LLM names what emerges; per the existing Discipline #41 |
| **F — Inter-faction relationships** | Phase 5 F-C | LLM judges relationships between player factions (alliance / rivalry / neutrality) | Read-and-judge layer over emergent factions |
| **G — Antagonist generation** | **UNBUILT — Cycle 15+ candidate seam** | Reads player-faction identity → produces contrast/antagonist faction identity ("Colonial Militia", "Privateers") | DOES NOT EXIST in current production code; see § 2 + § 3 gate (iii) |
| **H — Content cascade** | (content pipeline; partial today) | Player-faction + antagonist-faction shape content emphasis: Magic Find treasure-rich zones; Boss Speed Run arena content; Swarm Clear density zones | Partial today via existing content layer; full cascade scope is Cycle 15+ |

### 1.2 What makes this synthesis architecturally significant

**The cascade preserves substrate-led discipline through every layer.** The player makes one experiential-archetype choice. Each downstream layer reads the previous layer's output (substrate-anchored) and produces appropriate next-layer content (substrate-validated). The differentiation is emergent at each step; nothing is pre-authored per-player-choice.

**This is structurally different from procedural generation OR hand-authored content:**
- Procedural generation produces variation within a single cultural frame (one pre-authored world; many variant items)
- Hand-authored content produces fixed cultural frames (one set of factions; one set of antagonists; same for all players)
- **Cascade architecture produces multiple culturally-coherent frames simultaneously**, each appropriate to different player preferences, all generated through substrate-led emergence

**The Court of Forms becomes a multi-dimensional collection.** Players accumulate Spirits across mechanical archetype × cultural-tradition × experiential archetype. A Court dominated by Magic-Find pirates is genuinely different from a Court dominated by Boss-Speed-Run gladiators, even if both Courts have similar mechanical-archetype breadth.

### 1.3 The third coordinate axis — experiential archetype

**The dimension matt's two-day work on T4 capstones revealed:**

Per Matt's session reasoning: BC coordinate space tells the engine HOW the character fights (8 BC axes per `qd-engine-bc-axes-lock-2026-05-20.md`). Cultural-tradition coordinate space tells the engine WHAT cultural identity the character inhabits (substrate-anchored personage layer + thematic-registry). **Experiential archetype coordinate space tells the engine WHAT THE PLAYER IS DOING with the character.**

Two characters can occupy adjacent BC positions and feel like categorically different play experiences if their experiential archetype positions differ:
- Magic Find rogue (BC: stealth-control + low-tempo + flat-amplitude + solo-proxy) vs Boss Speed Run rogue (BC: stealth-burst + high-tempo + high-variance + solo-proxy) — adjacent in some BC dimensions, but the player's activity, goal, and engagement pattern differ categorically
- Specialist fire mage vs generalist multi-element mage — different BC positions, but specialist might still be a Magic Find archetype while generalist is End-Game-Generalist archetype

**Measurable signatures (candidate, pre-substrate-validation):**

| Experiential archetype | Measurable signature (candidate) |
|---|---|
| Magic Find | high loot-drops-per-hour; varied drop-pool engagement; moderate kill-rate; low single-target burst priority |
| Boss Speed Run | high single-target DPS; high movement-speed; low AOE coverage; measurable boss completion time |
| Swarm Clear | high AOE damage; high enemy-density engagement; clear-time-per-pack metric; moderate single-target |
| End Game Generalist | balanced across all metrics; flexible build; varied content competence |
| Build Crafter (candidate) | deep customization space; build-iteration metrics; theorycraft-engagement; community-content participation |

**These archetypes are pre-validation CANDIDATES.** Gate (ii) — legolas Mode A research — validates whether these labels emerge consistently across cross-site ARPG community vocabulary. If convergence emerges, they're substrate-led (community-emergent classification is a kind of substrate vote). If not, the labels need refinement OR the dimension needs different positioning.

### 1.4 What the cascade enables architecturally (LAUNCH-CONTENT-DISCIPLINE implication)

**"5 vectors of differentiated player experience > 5 acts of maps" launch design.**

Traditional ARPG launches focus on world content breadth (number of acts, zones, dungeons). Player engagement is primarily with character optimization + combat loop; world content is consumed once and rarely replayed.

**Under the cascade architecture, launch content should focus on experiential breadth instead.**

| Traditional launch | Cascade-architecture launch |
|---|---|
| 5 acts of campaign content | 3-4 modest regions designed to support all experiential archetypes |
| 30-40 mechanical archetypes (mage / rogue / etc.) | 30-40 mechanical archetypes × 5 experiential archetypes = 150+ distinct play experiences |
| World content scales with launch scope | World content scales with experiential archetype count (bounded) |
| Replay value = replay campaign with different mechanical archetype | Replay value = replay world with different experiential archetype (categorically different activities) |

**This DOES NOT mean v1 launches with 5 fully-supported experiential archetypes.** It means the v1 launch design SHOULD prioritize experiential breadth as the load-bearing differentiation rather than world content quantity. Specific launch archetype count is a separate design call gated on cascade quality + content design capacity per § 3.

---

## 2. Component status — what's built, partial, unbuilt

The cascade synthesis spans components at very different maturity levels. Treating the cascade as canonically locked architecture NOW would over-commit against unbuilt seams.

### 2.1 Built (in production code; firing in current Wave 5 cascade)

| Component | Status | Reference |
|---|---|---|
| Phase 2 BC discovery | Built; firing | `endgame_encounter_catalog.py` + `wave5_season_orchestrator.py` |
| Phase 3 PM-1 multimodal clustering | Built; firing | `rocket a466eb1` (PM-1) + `gandalf 7233e0f` (PM-2 + § 13 G-B math) |
| Phase 4 mechanical archive (MG-1 through MG-5 gates) | Built; firing | `engine 749d5aa` |
| Phase 5 Wave A faction-level LLM | Built; **FIRED in cascade-resumption-2 Step 5; gandalf preliminary verdict PASS** (Wave A outputs coherent + AI-tell-clean per gate (i) preliminary assessment) | `phase5_orchestrator.py` |
| ~~Phase 5 Wave B per-kit identity LLM~~ | ~~Same — first production exercise in current cascade~~ **AMENDED 2026-05-29: NOT BUILT; phantom component** — KR empirical grep finding (commit `fd48cab`): zero `wave_b\|WaveB\|run_wave_b` matches engine-wide. Moved to § 2.3 unbuilt seams. | (no implementation exists) |
| Phase 5 F-C inter-faction relationships | Built; FIRED in cascade-resumption-2 Step 5 under visible mode | `star-lord 6f94ce5` |
| Phase 7 2-layer joint-gate | Built | `gamora eca0aa5` |
| A/B comparison protocol | Authored; awaits Wave 5 close to execute | `canonical/story/ab-comparison-protocol-cycle-14-close-2026-05-27.md` |

### 2.2 Partial (architectural latent today; needs explicit articulation to be cascade-coherent)

| Component | Status | Path to full |
|---|---|---|
| **Experiential archetype as named architectural axis** | Latent in T4 capstone multi-option work (different T4 choices → different play experiences); NOT explicitly named as third coordinate axis | Gate (i)+(ii) → doc 52 promotion (DEFERRED) |
| **Content-cascade routing (player-faction × archetype → content emphasis)** | Partial today via existing content layer; cascade-coherent routing requires explicit archetype-aware content design | Cycle 15+ launch-design work |
| **Spirit-guide archetype awareness** | Latent; spirit guide can be extended to recognize archetype patterns + route content suggestions | Cycle 15+ |
| **Recycling-season archetype targeting** | Latent in deferred-cycle work | Cycle 15+ |

### 2.3 Unbuilt (Cycle 15+ candidate seams)

| Component | Status | Reference |
|---|---|---|
| **Phase 5 Wave B per-kit identity LLM** | **NOT BUILT — empirical finding 2026-05-29 commit `fd48cab`.** Zero `wave_b\|WaveB\|run_wave_b` matches engine-wide via KR grep. Orchestrator docstring `wave5_season_orchestrator.py:12` references Wave B as if built; implementation does not exist. Phase 7 cohesion-judge gate has been effectively pass-through (no per-kit cohesion exclusions; cohesion_data={} hardcode at `wave5_season_orchestrator.py:1169`). Cascade chain Step C ("Cohesion judge labels the magic find rogue as a pirate" — per-kit identity layer) is non-operational. **Path X (implement before A2-1 RE-FIRE-2; ~1d engineering) routing recommended per ambiguity in decisions-log line 3536** | KR commit `fd48cab` (cascade-resumption-2 Step 4 surface) |
| Player-kit-to-faction-coherence routing at per-kit layer | Same — depends on Wave B existence | Same |
| **Antagonist/contrast-faction generation** | **NOT BUILT.** Monster-contrast pattern explicitly DEFERRED to Cycle 15+ per Path 1 scope expansion record | `agentic_orchestration/gandalf/notes/2026-05-27-path-1-phase-4-5-7-cycle-14-scope-expansion.md` |
| Player-faction-to-antagonist-faction routing | Same | Same |
| Antagonist-faction substrate vocabulary | Same | Same |

**The cascade synthesis Matt's sentence describes IS NOT FULLY OPERATIONAL TODAY.** Step G (antagonist generation) is a separable engine seam that does not exist in current production code. **AMENDED 2026-05-29:** Step C (Phase 5 Wave B per-kit identity) is ALSO not in production code (KR empirical refutation; commit `fd48cab`). Path 1 scope expansion record (2026-05-27) explicitly defers monster-contrast (closely related) to Cycle 15+; Wave B implementation routing is being elected at cascade-resumption-2 Matt-surface (Path X recommended). The cascade synthesis is therefore MORE PARTIALLY ASPIRATIONAL than initial authoring represented — the architectural pattern is right; **TWO** implementation components are incomplete (Wave B + antagonist generation), not one.

---

## 3. Architectural commitments DEFERRED — empirical-evidence gates

Per recognition-validate-commit discipline (Discipline #42a-adjacent), ALL canonical promotion of this synthesis is gated on empirical evidence. No keystone canonical doc amendments fire from this recognition record without gate resolution.

### Gate (i) — Phase 5 LLM cohesion judge fires successfully in current Wave 5 cascade

**AMENDED 2026-05-29 per KR Wave B empirical refutation (commit `fd48cab`):** gate (i) disposition is now PARTIAL — Wave A + F-C verified coherent (gandalf preliminary assessment PASS); Wave B refuted as built component (does not exist in production code). Full gate (i) PASS requires Wave B operational. Path X election (implement Wave B before A2-1 RE-FIRE-2) advances toward full gate (i) PASS; Path Y election (ship without Wave B) makes gate (i) PARTIAL-PASS-with-architectural-gap the permanent disposition for v1.

**What it validates:** Cascade steps C, D, E, F (cohesion judge + clustering + faction naming + inter-faction relationships) operate at acceptable quality in production. Wave A produces coherent faction-level labels from PM-1 cluster reps; **Wave B produces coherent per-kit identity from kit content + substrate vocabulary IF AND WHEN BUILT** (per Path X election; currently NOT built per § 2.3 amendment); F-C produces meaningful inter-faction relationships.

**Empirical instrument:** Path D flip authorized 2026-05-29 (FACTION_VISIBILITY=visible). Cascade-resumption-2 A2-1 RE-FIRE-2 produces Wave A + F-C LLM outputs **(Wave B awaits Path X implementation per cascade-resumption-2 Matt election)**. Quality assessment via:
- ExportFactionCluster.faction_label_canonical: are names coherent + substrate-grounded? — **gate (i) Wave A sub-gate: PASS** per gandalf preliminary assessment
- ExportFactionRelationship: do inter-faction relationships make cultural sense? — **gate (i) F-C sub-gate: PASS** per same
- Phase 7 cohesion_judge_confidence: do scores distribute at acceptable level (≥0.75 threshold or systematically below = scaffold-flag-finding)? — **was effectively pass-through pre-amendment** (cohesion_data={} hardcode); becomes meaningful only post-Wave-B-implementation
- **Wave B per-kit identity coherence (gate (i) NEW sub-gate post-Path-X-implementation):** do per-kit substrate-thematic identities ("magic find rogue → pirate") emerge from real LLM judging at coherent quality?

**Expected resolution:** Wave A + F-C sub-gates resolved 2026-05-29 PASS. Wave B sub-gate gated on Path X completion (post A2-1 RE-FIRE-2 if Path X elected; permanently unresolved at v1 if Path Y elected with explicit gap documentation).

**Gate disposition rule (AMENDED):**
- **FULL PASS** — Wave A + F-C + Wave B all produce coherent outputs at expected quality → cascade architecture validated through F; promote experiential archetype dimension recognition to gate (ii) test
- **PARTIAL PASS** (current state pre-Path-X-implementation) — Wave A + F-C verified coherent; Wave B refuted as built component; cascade architecture chain Step C non-operational → gate (i) advances to PARTIAL; gate (ii) opens; full gate (i) deferred to Path X completion OR explicit v1 gap-acceptance per Matt Path Y election
- **FAIL** — Wave A or F-C produce incoherent outputs OR systematic under-0.75 cohesion confidence → cascade architecture has quality issue at Phase 5; surface to Matt Pattern B for design call (NOT a recognition-record failure; an empirical finding for refinement)

### Gate (ii) — Cross-site ARPG community archetype vocabulary research

**What it validates:** The experiential archetype taxonomy (Magic Find / Boss Speed Run / Swarm Clear / End-Game Generalist / Build Crafter) is community-emergent substrate (not pre-authored taxonomy). Matt 2026-05-29 directive: "Increase the sample size to all community ARPG websites... that is community canon when taken across sites and at volume."

**Empirical instrument:** legolas Mode A research brief at `agentic_orchestration/gandalf/notes/2026-05-29-legolas-mode-a-arpg-archetype-vocabulary-research-brief.md`. Cross-site corpus crawl: Maxroll + Icy-Veins + MobaFire + PoE Wiki + Last Epoch Wiki + Grim Dawn Forums + D3 Maxroll + D4 Maxroll + ARPG Reddit subreddits build-guide threads + ARPG Twitch creator vocabulary. Convergence test: do the same player-experience archetype labels emerge consistently across sites?

**Expected resolution:** legolas Mode A dispatch fires post-cascade-close (R48.4 single-seam); ~2-3 days execution + verdict authoring.

**Gate disposition rule:**
- CONVERGENCE PASS (~5-8 archetypes emerge consistently across ≥5 sites) → community canon confirmed; archetype taxonomy substrate-led; doc 52 promotion path opens
- CONVERGENCE MIXED (some archetypes emerge consistently; others vary by site) → refine taxonomy to consistently-emergent labels only; doc 52 promotion path opens for refined set
- CONVERGENCE FAIL (no consistent archetype vocabulary across sites) → experiential archetype dimension may need different positioning OR labels are too genre-specific; refine recognition record + commission Cycle 15+ deeper analysis

### Gate (iii) — Antagonist/contrast-faction generation seam scope decision

**What it validates:** Whether the cascade synthesis's Step G (antagonist generation) is worth committing as Cycle 15+ engine seam expansion.

**Empirical instrument:** Cycle 14 close + cascade quality findings from gates (i) + (ii). If gates (i) + (ii) PASS at acceptable quality, the cascade architecture is validated through F and antagonist generation becomes a natural extension. If gates (i) + (ii) reveal quality issues, antagonist generation may need to wait for further engine refinement.

**Expected resolution:** Cycle 14 close (post Wave 5 + A/B comparison verdict) + Matt Pattern B at re-engage.

**Gate disposition rule:**
- Cycle 14 closes clean + cascade through F at quality → recommend antagonist seam as Cycle 15+ scope-expansion candidate (~3-5 weeks rocket/star-lord engineering); Matt elects scope-expansion or holds
- Cycle 14 closes with cascade quality issues → defer antagonist seam to Cycle 16+; address cascade quality first

### Gate (iv) — Doc 38 amendment (engine commercial framing refinement)

**What it validates:** Whether the engine commercial pitch should be sharpened from "general serial content product" (Variant C) to "experiential cascade engine."

**Empirical instrument:** Gates (i) + (ii) + (iii) PASS at acceptable quality + Matt Pattern B design call.

**Expected resolution:** Cycle 14 close + Cycle 15 entry pre-scope.

**Gate disposition rule:**
- All gates PASS → light doc 38 amendment adding experiential cascade engine framing as engine-pitch refinement; D10 substrate-evidence-gate composition preserved
- Any gate FAIL or partial → no doc 38 amendment; recognition record stands; revisit at next empirical-evidence checkpoint

### Gate (v) — Doc 52 promotion (experiential archetype dimension load-bearing)

**What it validates:** Whether the experiential archetype dimension should be promoted from recognition-record territory to load-bearing canonical doc (`canonical/52-experiential-archetype-dimension-2026-05-29.md`).

**Empirical instrument:** Gates (i) + (ii) + (iii) all PASS + Matt Pattern B design call + content-design-discipline capacity assessment.

**Expected resolution:** Cycle 15 entry or Cycle 15 wave-close.

**Gate disposition rule:**
- All gates PASS + Matt confirms direction → author doc 52; promote experiential archetype dimension to load-bearing canonical
- Any prerequisite gate FAIL → recognition record stands; doc 52 path remains open at next checkpoint

---

## 4. Predictions registered for future empirical validation

Per Discipline #42a-adjacent recognition-validate-commit pattern. Predictions are registered NOW; empirical evidence from gate execution validates or refutes.

| # | Prediction | Empirical gate |
|---|---|---|
| P1 | Phase 5 Wave A + Wave B + F-C LLM produces coherent substrate-grounded outputs in current Wave 5 cascade | Gate (i) |
| P2 | Phase 7 cohesion_judge_confidence distributes around 0.70-0.85 range; scattered under-0.75 acceptable; systematic under-0.75 surfaces scaffold-threshold finding | Gate (i) |
| P3 | PM-1 emergent factions named by Wave A produce labels recognizable as cultural-tradition + experiential-archetype combinations | Gate (i) |
| P4 | Cross-site ARPG community archetype vocabulary research finds ~5-8 archetype labels that emerge consistently across ≥5 sites | Gate (ii) |
| P5 | Magic Find + Boss Speed Run + Swarm Clear emerge in the consistently-occurring set; End Game Generalist + Build Crafter emerge but possibly with site-variant naming | Gate (ii) |
| P6 | Some Maxroll-specific archetype vocabulary does NOT generalize across sites (vocabulary that's PoE-specific or D4-specific); the cross-site canon is narrower than any single site's vocabulary | Gate (ii) |
| P7 | Antagonist/contrast-faction generation seam is scopable for Cycle 15+ at ~3-5 weeks rocket/star-lord engineering (similar effort to Wave A LLM authoring) | Gate (iii) |
| P8 | A/B comparison protocol at Wave 5 close finds Option α substrate-led emergence produces ≥80% archetype-shape coverage of doc 48 baseline + ≥1 surprise-emergence beyond doc 48 (B-PASS verdict) | A/B protocol at Wave 5 close |
| P9 | Cascade-architecture launch design ("5 vectors > 5 acts") becomes load-bearing design discipline for Cycle 15+ launch content design (replacing traditional ARPG content-quantity launch design) | Gate (v) + Cycle 15+ design work |

---

## 5. Discipline composition

| Discipline | How this record honors it |
|---|---|
| **#41 substrate-led vocabulary lock** | Experiential archetype dimension is recognized but NOT locked as named axis until gate (ii) validates; archetype labels are CANDIDATES until cross-site community vocabulary research confirms convergence |
| **#42a framing-audit (Q1-Q6)** | Q1 — what assumptions does the cascade synthesis depend on? Q2 — what evidence could refute? (gates (i) + (ii) + (iii)) Q3 — is the right move to refine framing now, or commit and validate? (this record IS the framing refinement) |
| **#42a Instance-5 pattern** | Pre-imposed-assumption test on the cascade synthesis: synthesis frames cascade as "automated end-to-end" but Step G is unbuilt — explicit recognition this is partial, not full |
| **Recognition → empirical validation → commit** | Recognition NOW (§ 1); validation via gates (i)-(v) (§ 3); commit canonical promotion only after gates resolve |
| **#13 implicit-pillar-drift** | The "engine as experiential cascade engine" pitch is NEW commercial framing; this record preserves the dual-product framing (engine + game per doc 37 + 38) WITHOUT collapsing them |
| **#18 math hotspot consultation** | PM-1 clustering is the cascade's load-bearing math hotspot; existing elrond ownership preserved; legolas Mode A research at gate (ii) is methodology consultation pattern |

---

## 6. Cross-reference to existing canon

| Existing artifact | Composition with this record |
|---|---|
| `canonical/37-engine-and-game-two-products.md` | Engine commercial framing refinement (gate (iv)) composes with two-products framing; preserves separation |
| `canonical/38-downstream-delivery-strategy-2026-05-23.md` (D1-D10) | D10 substrate-evidence-gate is the pattern this recognition record honors; doc 38 amendment DEFERRED to gate (iv) |
| `canonical/39-qd-engine-end-to-end-workflow-2026-05-24.md` | The cascade architecture this record names rests entirely on doc 39's pipeline; doc 39 amendment NOT required at this stage |
| `canonical/47-damage-scaling-architecture-2026-05-27.md` § 4.6 two-layer T4 | Layer 2 T4 cycling is archetype-adjacent latent infrastructure; experiential archetype dimension may absorb Layer 2 strategies into archetype-keyed selections (Cycle 15+ exploration) |
| `canonical/50-bounded-viability-with-specialization-design-directive-2026-05-28.md` | Bounded-viability per-encounter-type composes orthogonally with experiential archetype — Magic Find vs Boss Speed Run aren't bounded-viability bands; they're different game-loops the kit serves |
| `canonical/51-investment-scaling-6-pattern-architecture-2026-05-28.md` Patterns 3-6 | Threshold unlocks + QoL modifiers + synergy bonuses + resource economy modifiers (Patterns 3-6 canonical-locked stubs Cycle 15+) may emerge as archetype-keyed per-pattern strategies |
| `canonical/story/skill-system-2026-05-24.md` skill composition | Skill composition (element × geometry × tempo × amplitude × tier_coefficient) is the BC layer; experiential archetype is the orthogonal third dimension this record names |
| `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` 8 BC axes | BC is coordinate space 1 (mechanical); cultural-tradition is coordinate space 2; experiential archetype is coordinate space 3 (this record) |
| `canonical/story/ab-comparison-protocol-cycle-14-close-2026-05-27.md` | A/B protocol at Wave 5 close measures Option α emergence vs doc 48 baseline; this recognition record's gates compose downstream of A/B verdict |
| `canonical/story/fate-genre-recognition-and-mobile-alignment-trajectory-2026-05-23.md` faction emergence + Rift | Cascade's Step E (faction naming) composes with Rift cross-cultural merge mechanic; Cycle 15+ work |
| `agentic_orchestration/gandalf/notes/2026-05-27-path-1-phase-4-5-7-cycle-14-scope-expansion.md` | Monster-contrast deferred Cycle 15+ per Path 1; antagonist/contrast-faction generation (cascade Step G) composes with monster-contrast as Cycle 15+ scope-expansion candidate |

---

## 7. Cascade-firing dependency on current Wave 5

**The current Wave 5 production cascade IS the empirical-evidence instrument for gate (i).** This recognition record's gate (i) resolves as the cascade executes:
- A2-1 RE-FIRE produces Wave A + F-C + Wave B outputs (Path D flip authorized 2026-05-29)
- Wave A LLM exercises against PM-1 cluster reps → produces faction labels
- Wave B LLM exercises against per-kit content → produces per-kit identity
- F-C produces inter-faction relationships
- Phase 7 cohesion_judge_confidence distributions captured in telemetry

**At Wave 5 close:**
- jack-ryan Gate-2 PASS-with-INFO/WARN assessment includes cohesion quality findings
- A/B comparison protocol fires per `ab-comparison-protocol-cycle-14-close-2026-05-27.md`
- gandalf consumes findings and assesses gate (i) disposition for this recognition record

**This recognition record + the current cascade are mutually validating instruments.** The cascade tests the cascade architecture; this record predicts what the cascade should produce; assessment at Wave 5 close validates or refutes per gate (i).

---

## 8. What this record does NOT do

- Does NOT lock the experiential archetype dimension as named architectural axis (DEFERRED to doc 52 promotion gate (v))
- Does NOT lock the 5 Maxroll-style archetype labels (DEFERRED to legolas Mode A research gate (ii))
- Does NOT amend doc 38 with engine commercial framing refinement (DEFERRED to gate (iv))
- Does NOT commit antagonist/contrast-faction generation as Cycle 15+ scope (FLAGGED as candidate; gate (iii) decides at Cycle 14 close)
- Does NOT collapse engine commercial pitch with game design discipline (preserved as separable canonical commitments per doc 37 + 38)
- Does NOT modify the current Wave 5 cascade execution (cascade fires per Phase A2 resolution plan; this record consumes findings, does not redirect)
- Does NOT lock "5 vectors > 5 acts" launch design discipline as canonical (recognition NOW; canonical promotion at Cycle 15+ launch-design-work)
- Does NOT pre-impose taxonomy in any other dimension (substrate-led discipline preserved across the record)

---

## 9. Sign-off

**Authored:** gandalf (story-and-design steward) during Phase A2 cascade-fire offline-work window per Matt 2026-05-29 paste-conversation surface + Matt 2026-05-29 ratification of canonicalization path (recognition record now; legolas Mode A research authored; doc 38 amendment + doc 52 promotion DEFERRED to empirical-evidence gates)

**Authority:** Matt 2026-05-29 in-session direction:
- "Agree on the artifacts."
- "Increase the sample size to all community ARPG websites... that is community canon when taken across sites and at volume. All we have to do is send legolas out to gather the canon."
- "Author what you can without me. Hold anything you need me for."
- "Your call." (re: contrast/antagonist seam — surfaced here as Cycle 15+ flagged candidate, not committed scope)

**For:** the synthesis capture of cascade architecture (substrate-led player-faction-to-antagonist-faction cascade through Phase 2-7 pipeline + experiential archetype as third coordinate axis) at recognition-record level with explicit empirical-evidence gates; canonical promotion to load-bearing architecture (doc 38 amendment + doc 52 + Cycle 15+ scope expansion) DEFERRED per recognition-validate-commit discipline.

**Next-empirical-evidence-checkpoints:**
- Gate (i) — current Wave 5 cascade close + jack-ryan Gate-2 assessment
- Gate (ii) — legolas Mode A dispatch fires post-cascade-close; verdict at +2-3d
- Gate (iii) — Cycle 14 close + Matt Pattern B at re-engage
- Gate (iv) — Cycle 14 close + Cycle 15 entry pre-scope
- Gate (v) — Cycle 15 entry or Cycle 15 wave-close
