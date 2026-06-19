# Pre-registered endorse-criteria — the two completion runs (Run A sim / Run B pipeline-spine) + the keystone-ceiling sweep-criteria

**Type:** META design pre-clear (gandalf → knight-rider). The lever that converts the run queue from "needs a live gandalf turn per build" into "an unattended run can close additive builds against gandalf-authored criteria it self-checks." Authored LAST of the three specs (faction-shape, caster-crater, this) so there is something concrete to write criteria against — per the wind-down memo §7.2(5) sequencing.
**Date:** 2026-06-18
**Author:** gandalf (story-and-design steward)
**Authority:** the 2026-06-18 "load both runs" authoring pass (Matt "yes please" to faction-shape + caster-crater + endorse-criteria). This doc pre-registers acceptance criteria + HONEST_FAIL shapes + park triggers; it does NOT execute the runs and does NOT make the Tier-3 Matt calls (it FRAMES them).
**FOLD (Matt 2026-06-18, after authoring):** the two runs are FOLDED INTO ONE sequenced run (overnight cadence — no one present to fire a second run if the two cannot fully parallelize). The per-item criteria below are UNCHANGED by the fold (they are per-item, not per-run); the fold adds a sequencing discipline (§1.5) and accumulates all parks to a single run-close. "Run A" / "Run B" persist below as WORKSTREAM labels within the one run.
**Parents (the items this writes criteria against):**
- Run/tier frame + item list: `agentic_orchestration/gandalf/notes/2026-06-18-pipeline-completion-progression-memo.md` §6 (three-tier envelope), §7.2 (the design pre-clears).
- Run-A caster item: `agentic_orchestration/gandalf/notes/2026-06-18-caster-upper-tier-crater-disposition.md` §3 (the caster-Lever-C probe + its pre-registered verdict rule).
- Run-B faction item: `agentic_orchestration/gandalf/notes/2026-06-18-faction-content-shape-emission-spec.md` (field partition + writer contract).
- Keystone sweep: `agentic_orchestration/gandalf/notes/2026-06-18-three-flip-run-close-band-hold-keystone-park.md` §2 (the park + empirical re-engagement criterion) + memo §7.2(3) (the investigation shape).
- Discipline lineage: the Lever-C pre-registration (criteria fixed BEFORE the run so the verdict is binding, not post-hoc) — `2026-06-15-lever-c-composition-verdict-disposition.md` §1 "the pre-registration that makes this binding."
**Grounded against disk 2026-06-18:** BC Stage-3 legacy machinery still present (`ARCHETYPE_ROLE_PRIORITY` / `legacy_archetype_shim` / `_PLAYER_CONTROLLER_ARCHETYPES` across `simulation/` + `generation/`); three flips ratified (decisions-log 4277/4302/4329); faction writer absent (`_export_season_inner()` never writes `faction_clusters`); monster generator present (`monster_generator.py:389`); gauntlet pass-floor 9-of-18 in-band per cohort (`gauntlet_sim.py:109,158`).

---

## 0. One line + what this doc IS

**This is the gandalf half of the autonomous-run contract: for each Run-A and Run-B item, a pre-registered (a) ACCEPT criterion that encodes the DESIGN-INTENT fidelity the build must preserve, (b) the HONEST_FAIL shapes that make a fail informative rather than just red, and (c) the PARK trigger that bounces the item to gandalf (Tier-2) or Matt (Tier-3) instead of letting the run guess.** Plus the keystone-ceiling sweep's pre-registered interpretation rule. The honest loading verdict (§6): the two runs are NOT uniformly green — three items are fully autonomous-eligible, three carry a named dependency or provisional call, and the keystone CALL + P1 architecture + push are correct Tier-3 Matt parks. Pre-registering that distinction IS the value: the run knows exactly where it may proceed and exactly where it must stop.

**Why gandalf and not jack-ryan writes these:** jack-ryan's Gate-2 checks *engineering* correctness (does it work, does it regress, is the math sound). These criteria check *design-intent* correctness (does the build preserve what the feature is FOR). A build can pass Gate-2 and still betray the design (a faction writer that emits factions as a combat-modifier when the spec ruled them organizing-only would be engineering-correct and design-wrong). The two gates compose; neither substitutes for the other. The run closes a Tier-1 build only when BOTH the jack-ryan Gate-2 critique-pair AND these gandalf endorse-criteria pass.

---

## 1. The three-tier decision envelope (the operating frame — from memo §6, restated as the contract)

- **Tier 1 — AUTONOMOUS.** Additive builds close via the jack-ryan Gate-2 critique-pair + these pre-registered endorse-criteria. No live gandalf turn. The run self-checks against §2–§3 and proceeds on a clean pass.
- **Tier 2 — PARK for gandalf (do NOT decide).** A design-judgment hinge the run must NOT resolve itself: any band-refit past a pre-registered drift threshold, any keystone-ceiling interaction, any schema contradiction, any HONEST_FAIL that lands OUTSIDE the pre-registered shapes (an unanticipated failure is by definition a gandalf-park, because the criteria did not foresee it). The run logs the park, leaves the item un-committed, continues with other items.
- **Tier 3 — PARK for Matt.** Push (ADR-006, unless a run-close push-pattern is pre-authorized); the keystone-ceiling design CALL; the P1 route-through-vs-replace architecture choice; procgen-tool adoption; any locked-decision re-open (MOB_HP 1.5x; the band fit beyond mechanical refit; the BC ACCEPT ruling).

**The cardinal rule for the run:** when in doubt, PARK up a tier, never DOWN. A Tier-2 item the run is unsure about goes to gandalf, not resolved autonomously. A Tier-3 item never gets a Tier-1 rationalization. The cost of an over-park is a deferred build (cheap); the cost of an under-park is a design betrayal committed unattended (expensive, and exactly what this contract exists to prevent).

---

## 1.5 Single-run FOLD (Matt 2026-06-18) — the two runs become one sequenced run

**Directive.** Fold everything unblocked into ONE longer run rather than two, because the overnight cadence means no one is present to fire a second run if the two cannot run in complete parallel.

**Endorsed — and BETTER for the cadence, not a compromise.** Run-A (sim; gamora; `simulation/`) and Run-B (pipeline-spine; star-lord+rocket; `export/output/generation/`) are SEAM-INDEPENDENT — they touch disjoint file trees. KR coordinates across all seams by definition, so one KR invocation sequences both workstreams in a single orchestration. The §2–§4 per-item criteria do not change; the fold changes the container and adds a sequencing discipline.

**Sequencing (the discipline that makes one run safe — diagnostics → additive → destructive-LAST):**
1. **Diagnostics first (zero-commit, zero-risk):** caster-Lever-C probe (§2.1) + keystone sweep (§4). They measure and commit nothing; running them first surfaces any park early and makes findings available to the rest of the run.
2. **Additive emission middle (additive-only, no sim-internal touch):** P2 faction (§3.1), P3 monster (§3.2), P5 weapon (§3.3), P1 emitter scaffolding (§3.4 — NOT assembly).
3. **Destructive LAST — BC Stage-3 prove-then-delete (§2.2):** runs last so (a) its prove-gate sees the FINAL repo state, so the §2.2 "any consumer the deletion would orphan" trigger can fire against any consumer introduced earlier in the run; (b) if it fails its prove-gate and parks, it parks WITHOUT having blocked the additive work that already closed; (c) the destructive blast radius is isolated at the run's end.

**What does NOT fold in (stays parked, by design):** B4 summon (Tier-2 — and an OPEN scope question rides it: summoner is Phase-5-deferred per project memory, so B4 may not be season-1 content at all; resolve scope before it enters any run); P1 top-level assembly (Tier-3 — route-vs-replace, Matt); the keystone-ceiling CALL (Tier-3 — Matt, under sweep-result K-1/K-3). The INVESTIGATIONS still run (caster probe, keystone sweep are diagnostics in step 1); only the design CALLS they tee up are parked.

**Parks accumulate to ONE run-close.** Parks no longer split across two closes — KR collects every Tier-2 (gandalf) + Tier-3 (Matt) park and surfaces the whole stack at a single close. For fire-once overnight this is the right shape: run the unblocked items, park the gated ones, surface the park-stack at one close.

**Push is the highest-leverage overnight input (Tier-3).** An overnight run with no one present to push leaves every committed work-product on LOCAL main until Matt returns — the work is real but invisible to the remote and to any other host. Push is Matt-gated (ADR-006). For the run's value to actually land, Matt should consider PRE-AUTHORIZING a run-close push-pattern (precedent: the PC-seam wave-close standing-push, CLAUDE.md). This is the single input that converts the folded run's on-disk output into pushed, durable value.

---

## 2. RUN A — sim-completion endorse-criteria

### 2.1 Caster-Lever-C probe (the caster-crater Run-A item) — FULLY LOADED, Tier-1

- **ACCEPT criterion.** The probe runs the four caster cells (fire/water/earth/wind) at BOTH M=1.0 (generous) and M=0.30 (the jack-ryan discriminator), with `magic_pack` at NORMAL difficulty (NOT rigged), reusing the existing Lever-C harness, and emits an interpretable per-cell mini_boss/boss win-rate at each M. Design-intent fidelity = it must be a clean composition-vs-suppression discriminator, which means the M=0.30 conservative bound MUST be present (a generous-M-only run could brute-force a false "suppression" read — the exact door jack-ryan closed for the rogue).
- **VERDICT rule (pre-registered in the caster disposition §3, binding):** zero mini_boss/boss kills at M=1.0 → COMPOSITION (same family as the rogue C-2); the caster lacks a boss finisher → the fix path (§4 of the disposition) opens, GATED. Meaningful kills at M=1.0 → SUPPRESSION (the magic_pack over-clear dragged the modifier below boss-killable) → re-opens the caster architecture/loop question on evidence.
- **HONEST_FAIL shapes (all informative, none a true fail):** (i) clean composition verdict; (ii) clean suppression verdict; (iii) split — some cells composition, some suppression (a genuine finding: the element flavors diverge at the boss tier; route to gandalf). All three are SUCCESS outputs of a diagnostic.
- **PARK trigger (Tier-2):** any result the §3 verdict rule does not anticipate (e.g., the harness cannot pin M for caster cells; non-monotonic boss-WR-vs-M; a cell that kills boss at M=0.30 but not M=1.0). Diagnostic only — NEVER commits a fix in this run.

### 2.2 BC-coordinate Stage-3 prove-then-delete — LOADED with a TIGHT prove-gate, Tier-1-conditional

- **Design intent being preserved.** The BC cutover replaces the archetype LABEL with the 8-axis Battle-Coordinate as the pipeline's structural hub. It is a REFACTOR, not a balance change — **the player must feel NOTHING.** Stage-2 already proved behavioral equivalence (16/16 archetypes at `0.00/0.00/0.000`, the one WARN-1a envelope-width flag ruled ACCEPT this session). Stage-3 deletes the now-dead legacy machinery (`ARCHETYPE_ROLE_PRIORITY`, `_PLAYER_CONTROLLER_ARCHETYPES`, `ARCHETYPE_TEMPLATES`, `legacy_archetype_shim`).
- **ACCEPT criterion (the prove-gate, which MUST pass before the delete fires):** the Stage-3 prove step must RE-DEMONSTRATE behavioral equivalence AT THE DELETION BOUNDARY — i.e. the BC-keyed path produces byte-identical (or within the Stage-2 `0.00` tolerance) gauntlet outcomes to the pre-deletion path, on the same seeds. Only on a clean re-prove does the destructive deletion proceed. Design-intent fidelity = equivalence, not "close enough."
- **Non-negotiable invariant (Disc #12/#39):** the tri-state guards (FALLBACK + LOUD-DEFAULT) must SURVIVE the deletion. The tri-state must NOT collapse before Stage-3 — a silent default where a loud one stood is a regression even if WRs are identical. The delete removes the legacy machinery; it does NOT remove the safety rails that catch a future miskey.
- **HONEST_FAIL shapes:** (i) prove re-passes clean → delete proceeds → jack-ryan Gate-2 on the deletion → Tier-1 close. (ii) prove drifts at the boundary (any non-zero equivalence delta beyond Stage-2 tolerance) → DO NOT DELETE → PARK (Tier-2): a drift at the deletion boundary that Stage-2 did not show is a real finding, not a tuning nit.
- **PARK trigger (Tier-2):** any equivalence drift at the prove step; any tri-state guard that would be removed rather than preserved; any consumer of the legacy machinery the deletion would orphan that the prove step did not surface. **The destructive deletion is autonomous-eligible ONLY because the prove-gate fronts it** — the run never deletes on an unproven boundary.

### 2.3 B4 summon calibration — PARTIAL: grounding gap named honestly (NOT yet fully loadable)

- **Honest state.** I do NOT have first-hand grounding on B4's exact current scope. The proxy/summon infrastructure landed recently (proxy-track flip #2 ON; proxy-population re-homed `proxy_population.py`; Proxy-Commander Set #6 calibrated `s_baseline=0.35`), so "summon calibration" may be (a) calibrating summoner-kit gauntlet-band placement now that the proxy machinery is live, or (b) something narrower. Writing detailed criteria against an item I have not grounded would be fabrication — the exact discipline failure (assert-from-memory) this workstream keeps catching.
- **Provisional ACCEPT criterion (conservative, balance-anchored):** IF B4 is summoner-kit band placement: a calibrated summoner kit must clear the gauntlet pass-floor (≥9/18 in-band per cohort; `season_emit` = pass ≥1 of 4 cohorts) WITHOUT the proxy population doing the hard part FOR the player — the Set #6 discipline holds (the army is an EXTENSION of the player's offense, not a clone-multiplier; `proxy_max_active` wall intact; offense-inheritance `s` strictly in (0,1)). Design-intent fidelity = the summoner FEELS like a commander, not an afk-autobattler.
- **PARK trigger (Tier-2, defaulted ON for this item):** B4 PARKS for a gandalf grounding pass BEFORE it is autonomous-eligible, UNLESS the run can confirm B4's scope matches the provisional criterion above against disk. **Stated plainly: B4 is the one Run-A item I am NOT clearing for unattended close sight-unseen.** A ~10-minute gandalf grounding turn (read the summoner-kit gauntlet state + the Set #6 calibration interaction) converts it to Tier-1; until then it is Tier-2.

---

## 3. RUN B — pipeline-spine endorse-criteria

### 3.1 P2 faction writer — FULLY LOADED via the faction content-shape spec, Tier-1

- **ACCEPT criterion.** The faction writer emits the faction block per the faction content-shape spec: the ~14 bundle fields (membership / signature / canonical label / identity-narrative / thematic-tags / the 6-enum relationships + tension-narrative + shared-history-hook), the ~10 telemetry-only fields dropped to telemetry, embedded IN the unified bundle (NOT the loadout sidecar), with faction_visibility = VISIBLE (resolving the stale "v1=invisible" default). Conforms to the spec's §4 concrete bundle shape + §8 writer contract.
- **Design-intent fidelity (the three rulings the writer must preserve):** (1) factions are an ORGANIZING + PRESENTATION layer, NOT a combat mechanic — the writer must NOT emit faction data into any field the fight model reads (the fight model was verified to hold zero faction references; a faction-as-combat-modifier emission betrays the ruling and is a design fail even if it passes Gate-2); (2) season-1 is faction-VISIBLE; (3) bundle-embed, not sidecar.
- **HONEST_FAIL shapes:** (i) the singleton cluster (cluster 4, member_count=1) / the modal_tone="unknown" data-quality flags surface at emit — EXPECTED, handle per the spec §6 (emit with the flag, do not drop, do not fabricate a tone); (ii) a cohesion-judge field the spec did not classify appears → PARK.
- **PARK trigger (Tier-2):** any field whose bundle-vs-telemetry routing the spec did not specify; any pressure to make factions sim-load-bearing (that is a SCHEMA CONTRADICTION against the ruling → Tier-2, possibly Tier-3 if it implies a season-1 scope change).

### 3.2 P3 monster wiring — LOADED, Tier-1

- **ACCEPT criterion.** Monster generation wired into the cycle-14 track (kit-only today), emitting monsters into the unified bundle with full stats + flavor, per the existing monster generator (`monster_generator.py`, 44 monsters w/ stats+flavor) and the monster-design intent (`canonical/historical/34-monster-design-phase0-vs-production.md`). Design-intent fidelity = monsters are season-1 fodder/encounter content (the four-entity-family distinction from the current→end-state doc: monsters ≠ summons ≠ companions ≠ townsfolk).
- **HONEST_FAIL shapes:** (i) cycle-14 monsters carry the phase0 monster shape, not the production shape → acceptable for season-1 IF it matches doc 34's phase0 spec; flag if it silently uses a richer/poorer shape than doc 34 sanctions. (ii) monster flavor_text NULL (the cycle-14 skill-flavor gap pattern) → PARK if flavor is expected but absent.
- **PARK trigger (Tier-2):** any monster-generation interaction with the faction layer (e.g., faction-affiliated monsters) the specs did not anticipate; any divergence from doc 34's sanctioned monster shape.

### 3.3 P5 weapon emission — PROVISIONAL shape call (lightish; clears it for the run)

- **The design question (memo §7.2(2)):** is a weapon a separate content type or a gear-subtype? What does the sim need from a weapon descriptor distinct from its gear entry?
- **PROVISIONAL RULING (made here so the run is not blocked; subject to a Tier-2 bounce if the build hits an ambiguity I did not foresee):** a weapon descriptor is a SEPARATE content slot from gear, because the weapon carries the kit's IDENTITY (the weapon-as-identity generation spec — the weapon-family drives the kit's skill cross-product), not an interchangeable gear-slot roll. The descriptor is emitted as `main_weapon` from the existing `substrate_weapon_binding` (phase2 intermediate), carrying: weapon-family, element-flavor, and the binding→descriptor identity fields the sim needs to render the kit's signature weapon — distinct from the `gear_pool` entries (which are the roll-able stat items). Design-intent fidelity = the weapon is the kit's SIGNATURE, not a cosmetic and not a generic gear slot.
- **ACCEPT criterion.** `main_weapon` populated (no longer None) from `substrate_weapon_binding`, carrying the weapon-as-identity fields, emitted into the bundle as a descriptor distinct from the gear entry.
- **PARK trigger (Tier-2):** if the substrate binding does NOT carry enough to populate the descriptor without inventing fields (do not fabricate weapon identity at emit — narrow blanks per D7, but do not author weapon lore in the writer); if the weapon-vs-gear distinction collides with how the sim actually loads gear (a schema question → Tier-2).

### 3.4 P1 unified driver — ARCHITECTURE parks for Matt (Tier-3); per-type emitters proceed

- **The Tier-3 Matt call (do NOT resolve in the run):** route-through vs replace — does the single driver route cycle-14 content THROUGH the existing `season_exporter`, or REPLACE it? This is an architecture decision with downstream consequence (the existing exporter is kit/monster/gear-only with a deleted CLI; cycle-14 is kit/faction-rich emitting to the loadout app). It parks for Matt.
- **What the run MAY do without the architecture call:** the per-type emitter blocks (P2 faction / P3 monster / P5 weapon) are specified driver-AGNOSTICALLY — each produces a well-formed block (the faction spec §8 writer contract is explicitly assembly-agnostic). The run may build and validate those blocks independently. P1's TOP-LEVEL assembly (where the route-vs-replace seam lives) parks; the blocks it will eventually assemble do not.
- **ACCEPT criterion (for the deferrable scaffolding only):** any P1 scaffolding the run builds must NOT bake in route-vs-replace (no commitment to either the season_exporter path or a replacement until Matt rules). A driver shell that calls the per-type emitters and leaves the assembly-target as a parked seam is acceptable; a driver that picks route-or-replace autonomously is a Tier-3 violation.
- **PARK trigger (Tier-3):** the route-vs-replace choice itself, and any build step that cannot proceed without it.

---

## 4. Keystone-ceiling sweep-criteria (EMBEDDED — pre-registered interpretation so the sweep is binding)

The keystone-ceiling "over-tuned" question is PARKED with an empirical re-engagement criterion (a non-degenerate open_arena reference). The INVESTIGATION (a keystone-magnitude sweep) is autonomous-eligible; the CALL parks for Matt. To make the sweep's result binding rather than post-hoc, I pre-register its interpretation HERE, before it runs (the Lever-C discipline):

- **The sweep.** At fixed MOB_HP 1.5× (locked anchor), on the saturated open_arena faithful reference, vary the keystone magnitude across a descending ladder and measure, per rung: open_arena win-rate, loss-variance, and `spearman_degenerate` / `max_rank_shift`.
- **Pre-registered interpretation rule (binding):**
  - **K-1 (keystone IS the ceiling-holder → over-tuned is a LIVE candidate).** If reducing keystone magnitude DE-SATURATES the reference — open_arena WR drops below 1.000 with non-zero loss-variance and `spearman_degenerate` goes FALSE at some magnitude M_desat — then the keystone was holding the ceiling. The over-tuned question becomes measurable (rank-discrimination restored below M_desat). → The design CALL (how far to reduce, if at all) PARKS for Matt+gandalf, now with a de-saturated reference to measure against.
  - **K-2 (ceiling is SCENARIO-driven → keystone is NOT the culprit).** If NO keystone magnitude de-saturates — open_arena stays at 1.000 with zero variance across the entire descending sweep, even at low keystone — then the ceiling is a property of open_arena being trivially winnable by geared kits REGARDLESS of keystone. The keystone is exonerated; the over-tuned question answers NEGATIVE. → The ceiling, if it is to be addressed at all, relocates to open_arena scenario difficulty (a different ticket; and note open_arena is a BYPASSED gating tier, so the ceiling may simply be cosmetic to the gate — couples to the caster-disposition §5 "does the loop optimize against bypassed tiers?" question).
  - **K-3 (partial).** De-saturation occurs but only at a keystone magnitude so low it would gut the keystone's intended power fantasy → a genuine tension (over-tuned-for-measurement vs right-sized-for-feel) → PARK for Matt+gandalf with both numbers named.
- **HONEST_FAIL = all three are informative.** K-1, K-2, K-3 each resolve the parked question's measurability. There is no "fail" — there is only which branch the data picks.
- **PARK level:** the sweep INVESTIGATION is Tier-1 (autonomous; it is a measurement sweep). The keystone-ceiling design CALL is Tier-3 (Matt) under K-1/K-3, or self-resolves NEGATIVE under K-2.

---

## 5. Cross-cutting PARK triggers (the run consults this list on every build)

**Tier-2 — PARK for gandalf (design-judgment hinges; do NOT auto-resolve):**
- Any band-refit past the pre-registered drift threshold (the three-flip run-close already ruled bands HOLD as-fit; a NEW drift past threshold is the trigger).
- Any keystone-ceiling INTERACTION surfacing mid-build (a build that moves open_arena WR, touches the keystone, or de-saturates the reference as a side-effect).
- Any SCHEMA CONTRADICTION (a field the specs route two ways; a faction field pressured into sim-load-bearing; a weapon-vs-gear collision).
- Any HONEST_FAIL OUTSIDE the pre-registered shapes in §2–§4 (an unanticipated failure is definitionally a gandalf-park).
- Any pressure to re-impose a STRUCK scope item (the phantom season-1 NPC type; do not let a build re-introduce it).

**Tier-3 — PARK for Matt (decisions exceeding seam + gandalf authority):**
- PUSH (ADR-006) unless a run-close push-pattern is pre-authorized for this run.
- The keystone-ceiling design CALL (under sweep-result K-1/K-3).
- The P1 route-through-vs-replace architecture choice.
- The rogue boss-efficacy Matt call ((a) composer efficacy fix vs (b) accept-and-route-via-b6) — and, if the caster probe returns composition, the analogous caster boss-bridge call (these are the boss-bridge family Matt decision points).
- Procgen-tool adoption (Tier-3, off-path).
- Any LOCKED-decision re-open (MOB_HP 1.5x; the band fit beyond mechanical refit; the BC ACCEPT ruling; the six-type season-1 bundle).

---

## 6. Honest loading verdict — which items are TRULY autonomous-eligible

The disciplined survey (what IS, not what I wish were green):

| Item | Run | Loading | Gate |
|---|---|---|---|
| Caster-Lever-C probe | A | **FULLY LOADED** | Tier-1; verdict rule pre-registered |
| BC Stage-3 prove-then-delete | A | **LOADED (prove-gate fronts the delete)** | Tier-1-conditional on clean re-prove |
| B4 summon calibration | A | **PARTIAL — grounding gap** | Tier-2 default; ~10-min gandalf turn → Tier-1 |
| P2 faction writer | B | **FULLY LOADED** | Tier-1 via faction spec |
| P3 monster wiring | B | **LOADED** | Tier-1 vs doc 34 shape |
| P5 weapon emission | B | **LOADED (provisional ruling)** | Tier-1; Tier-2 bounce on shape ambiguity |
| P1 unified driver | B | **ARCHITECTURE PARKS** | Tier-3 Matt; per-type blocks proceed |
| Keystone sweep | (cross) | **INVESTIGATION LOADED** | Tier-1 sweep; CALL Tier-3 |

**The honest headline:** five of eight items are autonomous-eligible NOW (caster probe, BC Stage-3 behind its prove-gate, faction writer, monster wiring, weapon emission, keystone sweep — six counting the sweep). ONE (B4) needs a short gandalf grounding turn I have flagged rather than faked. ONE (P1) correctly parks on a Matt architecture call while its constituent emitters proceed. **That is a genuinely well-loaded run** (folded per §1.5) — not because everything is green, but because every item's gate is named and the parks are in the right tier. The single run executes the green items unattended in the §1.5 sequence and stops cleanly at the named parks.

---

## 7. Routing

- **knight-rider:** these are the gandalf endorse-criteria for the folded run (one sequenced run per §1.5 — diagnostics → additive → BC-Stage-3-destructive-LAST). Compose them with the jack-ryan Gate-2 critique-pair for Tier-1 closes. The cardinal rule (park UP a tier, never down) governs ambiguity. Three items need your sequencing attention: (a) B4 wants a ~10-min gandalf grounding turn before it is Tier-1 (or confirm its scope against disk); (b) P1's architecture parks for Matt while P2/P3/P5 proceed; (c) the keystone sweep can run Tier-1 with the §4 interpretation rule, its CALL parking for Matt. Surface the §5 Tier-3 list to Matt (push pre-authorization is the one input that converts the run's on-disk value into pushed value).
- **gamora:** Run-A sim items — the caster probe (§2.1, reuse Lever-C harness), BC Stage-3 (§2.2, prove-gate fronts the delete), B4 (§2.3, flag scope to gandalf if it exceeds the provisional criterion), the keystone sweep (§4). The §2.2 prove-gate and the §4 interpretation rule are the binding discipline.
- **star-lord + rocket:** Run-B pipeline items — P2 faction writer (§3.1, per the faction spec writer contract), P3 monster wiring (§3.2), P5 weapon emission (§3.3, provisional ruling), P1 scaffolding (§3.4, do NOT bake route-vs-replace). The design-intent fidelity checks (not just "does it run") are the gandalf half each build must clear.
- **jack-ryan:** your Gate-2 composes with these — your gate is engineering-correctness, mine is design-intent-fidelity; a Tier-1 close needs BOTH. The pre-registration discipline (criteria fixed before the result) is the same one your M=0.30 Lever-C pivot established; these criteria inherit it.
- **Matt (RESERVED, Tier-3):** push (or a run-close push-pattern pre-authorization); the keystone-ceiling CALL (under K-1/K-3); the P1 route-vs-replace architecture choice; the boss-bridge family calls. Each is FRAMED here, none decided.

---

**Signed:** gandalf, 2026-06-18.
**For:** pre-registering the gandalf design-intent-fidelity criteria that, composed with the jack-ryan Gate-2 critique-pair, let an unattended run close the additive builds of both completion runs without a live gandalf turn — per item: an ACCEPT criterion encoding what the feature is FOR, the HONEST_FAIL shapes that make a fail informative, and the PARK trigger that bounces design-judgment hinges to gandalf (Tier-2) or Matt (Tier-3); with the keystone-ceiling sweep's interpretation rule embedded (K-1 keystone-holds-ceiling → over-tuned live, CALL parks / K-2 scenario-driven → keystone exonerated / K-3 partial → tension named) so the sweep is binding not post-hoc; and an honest loading verdict that does NOT pretend uniform green — six items autonomous-eligible, B4 flagged for a short grounding turn rather than faked, P1 architecture correctly parked for Matt while its emitters proceed — because the value of a pre-registration is naming where the run may proceed AND exactly where it must stop, with every park in the right tier.
