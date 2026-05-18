# 2026-05-17 — gandalf — DoE doc-cascade (Path A): canonical-32 + canonical-17 + mobile-execution-plan portrait-primary amendments (QUEUED — auto-fires after gandalf D11 advisory)

**Authority:** Matt L3 2026-05-17 evening — "Yes, if A makes portrait primary that works." Matt locked Path A (doc-only) for DoE/VS2a alignment, with explicit confirmation that portrait-primary becomes the canonical mobile target via these amendments.
**Type:** Pattern B (short) — three doc amendments cascading from the DoE feel-target lock; ~0.5-1 day; design steward in lane.
**Predecessor (gates auto-fire):** gandalf D11 ARPG-balance advisory (`agentic_orchestration/dispatches/2026-05-17-gandalf-d11-arpg-balance-advisory.md`).
**Status:** 🟡 **QUEUED — DO NOT EXECUTE until D11 advisory ships completion record.** Knight-rider activates when D11 advisory lands.

---

## Why this matters

Your DoE feel-target doc (`canonical/story/mobile-feel-target-doe-2026-05-17.md`, shipped today) locked four design directions and explicitly listed cascade amendments needed downstream:

1. canonical-32 amendments (retire potion-inventory mechanic → cooldown ability; add react-or-auto primitive § 13; mobile-orientation portrait-primary note)
2. canonical-17 amendment (retire potion-interaction affixes; add heal-cooldown / heal-magnitude affixes)
3. mobile-ux-execution-plan § 7.1 amendment (portrait-primary, landscape-secondary tuning)
4. mobile-pc-pixel-sizing-ratios § 3.5 amendment (portrait-primary tuning)

Matt explicitly chose **Path A** (doc-only; no engine refactor; no drax code changes in VS2a) — this dispatch authors all four cascade amendments. The DoE feel-target becomes load-bearing canon for all subsequent mobile work; M2-M7 mobile phases (when they fire VS2b) consume the portrait-primary amended plan.

**Engine-side STAMINA_POTION_USE → heal_ability refactor is explicitly deferred to VS2b.** Your amendments lock the design direction; gamora + star-lord + rocket execute the refactor post-D11.

---

## Required reading (when activated)

1. **Your own DoE feel-target doc** — `canonical/story/mobile-feel-target-doe-2026-05-17.md` (§ 7.1-7.6 enumerates the cascade items)
2. **canonical/32-progression-design.md** — your amendment target (likely new § for react-or-auto + amendment to potion section)
3. **canonical/17-gear-and-spirit-guide-design.md** — your amendment target for affix amendment
4. **canonical/story/mobile-ux-execution-plan-2026-05-17.md** — drax's plan; § 7.1 amendment target (you author the amendment; coordinate with drax if needed but the doc is in your design-steward lane)
5. **canonical/story/mobile-pc-pixel-sizing-ratios-2026-05-17.md** — your own canon; § 3.5 amendment
6. **Engineering disciplines** — particularly Discipline #1 (math-before-code) and Discipline #11 (attribution clarity); your amendments set the design contract that engine-side refactor will honor

---

## Scope — four amendments

### Amendment 1 — canonical-32-progression-design.md

Two amendments:

**1a. Retire potion-inventory; replace with cooldown-gated heal ability.**

- Locate the existing potion-inventory mechanic section (likely under inventory / consumables / progression)
- Amend to: single "Healing" ability, cooldown-gated, on-character (PC + mobile both; consistency lock per § 0 TL;DR of DoE doc)
- Specify cooldown baseline (DoE doc recommends 8-12s; pick a value — gear/trait modifiable per Amendment 2 below)
- Specify magnitude baseline (% HP heal; or flat HP; or hybrid — gear/trait modifiable)
- Note that mana mechanic survives as-is (or document if mana is also being retired to cooldown — your call; gandalf's lane)
- Note inventory-slot impact: freed potion slots are available for build-crafting items

**1b. Add react-or-auto interaction primitive (new § 13).**

Per § 5.3 of DoE doc:
- New canonical section authoring (likely § 13 or wherever fits the existing structure)
- Specify the primitive: every battlefield interaction (chest open / door / lever / NPC dialogue trigger) has an `auto_complete_window` (recommend 0.8-1.5s; let you pick the value)
- Player tap during window = intentional activation
- Window expiry = auto-completion
- Document the design rationale (reduces decision fatigue; preserves agency)
- Document non-applicability cases if any (e.g., combat skill activations are NOT react-or-auto; they're tap-only)
- Specify how this primitive interacts with existing canon (mostly additive; flag any conflicts)

**1c. Portrait-primary orientation note (minimal; mobile-orientation lock).**

- Add a note (probably § 2 or wherever orientation is referenced if at all) that mobile target is portrait-primary; landscape is secondary
- Cross-reference DoE doc § 7.1 for the why

### Amendment 2 — canonical-17-gear-and-spirit-guide-design.md

- Locate gear-affix section
- Retire affixes that interact with potion-inventory (e.g., "+1 potion slot", "potion stack size", "potion drop rate") — list which affixes are retired
- Add affixes that modify the heal cooldown or heal magnitude:
  - `heal_cooldown_reduction` (e.g., -1.5s)
  - `heal_magnitude_bonus` (e.g., +15% HP healed)
  - Possibly `heal_secondary_effect` (e.g., grants 3s damage immunity on cast; gandalf's call)
- Note that spirit-guide's role with potion-affixes (if any) shifts to heal-affixes
- Cross-reference DoE doc § 7.2 for the why
- Flag for jack-ryan: this is a load-bearing canon change; trigger Gate-1 advisory pattern (your amendment goes through doc review before rocket-side affix-system refactor fires in VS2b)

### Amendment 3 — mobile-ux-execution-plan-2026-05-17.md § 7.1

- This is drax's plan but lives in canonical/story/; you can author the amendment as a design-steward edit (or coordinate with drax via handoff)
- Amend § 7.1 (or wherever orientation is documented) to portrait-primary, landscape-secondary
- HUD zone layout (§ 4.2) currently shows landscape diagram; add a parallel portrait diagram (or note that portrait layout is TBD in M5/M6 dispatch)
- Phase M2-M7 dispatches consume the amended plan; their layout positions assume portrait when they fire VS2b
- Note: landscape support is retained as a polish-phase item, not a v1 requirement

### Amendment 4 — mobile-pc-pixel-sizing-ratios-2026-05-17.md § 3.5

- Your own canon; § 3.5 specifies minimap-positioning with portrait/landscape symmetry
- Amend to portrait-primary tuning (DoE's minimap is top-left in portrait; landscape positions remain as fallback notes)
- Touch-target sizing canon stays unchanged (110-125px centroid for action; 88px floor; portrait orientation doesn't change touch ergonomics)

---

## Out of scope (DO NOT)

- ❌ DO NOT author engine-side code or specifications (gamora/rocket/star-lord lanes)
- ❌ DO NOT modify drax's existing mobile code (doc cascade only)
- ❌ DO NOT pre-empt the M2-M7 portrait-layout dispatches (those fire VS2b)
- ❌ DO NOT extend beyond the four amendments listed (scope creep risk)
- ❌ DO NOT modify the DoE feel-target doc itself (it's the source; amendments cascade FROM it, not back to it)
- ❌ DO NOT pre-empt jack-ryan Gate-1 advisory on canonical-17 amendment (note for handoff; don't substitute)

---

## Acceptance criteria (when activated)

- [ ] Amendment 1a authored in canonical-32 (potion-inventory retired; cooldown heal locked with baseline values)
- [ ] Amendment 1b authored in canonical-32 (react-or-auto primitive; new section)
- [ ] Amendment 1c portrait-primary note in canonical-32
- [ ] Amendment 2 authored in canonical-17 (affix retirement + new heal-affixes)
- [ ] Amendment 3 authored in mobile-ux-execution-plan § 7.1 portrait-primary (coordinate with drax if needed)
- [ ] Amendment 4 authored in mobile-pc-pixel-sizing-ratios § 3.5 portrait-primary
- [ ] Cross-references updated (DoE doc § 7.1-7.6 referenced from each amendment; amendments referenced from DoE doc § 11)
- [ ] PRE-SIGNAL § 14.1.1 before hive-log append
- [ ] HANDOFF → jack-ryan (Gate-1 advisory on canonical-17 amendment; gates eventual VS2b affix-system refactor)
- [ ] HANDOFF → gamora + star-lord + rocket (VS2b heal_ability refactor — informational; engine-side refactor is deferred to post-D11)
- [ ] HANDOFF → drax (M2-M7 dispatches will consume portrait-primary amended plan when they fire VS2b)
- [ ] Hive-log STATE entry summarizing what shifted from DoE doc cascade

---

## Coordination

- **AUTO-FIRE TRIGGER:** D11 ARPG-balance advisory ships completion record. Knight-rider monitors and spawns gandalf agent at that time.
- **Parallel-safe with**: D11 sprint (D11 is engine seam; this is canonical/story doc cascade) ; drax loot-pipeline wiring (different concern); legolas-3 catalogue crawl
- **PRE-SIGNAL § 14.1.1** before hive-log appends
- **No tag** (doc cascade; not code)

---

## Engine-side implications (informational; not your work)

Your amendments lock the design contract. The engine-side execution that follows in VS2b:

1. **gamora/star-lord**: refactor `STAMINA_POTION_USE` (or equivalent) in `combatant.py` → cooldown-gated `heal_ability` field with magnitude + cooldown attributes consumed from gear affixes; MIGRATION.md cross-seam entry
2. **rocket**: update gear-affix generation to emit heal_cooldown_reduction / heal_magnitude_bonus / heal_secondary_effect per Amendment 2; retire potion-interaction affix generation
3. **star-lord**: telemetry update (record heal cast events; expected on healability event type)

This sequence runs post-D11 (so D11 hybrid_mage tuning lands first) and likely as its own dispatch chain. You're not authoring these; just making them well-defined.

---

*Dispatched (queued) 2026-05-17 by knight-rider per Matt L3 Path A lock with portrait-primary confirmation. ~0.5-1 day when activated. Append completion record when done.*

---

## Completion record — 2026-05-17 (gandalf)

**Status:** ✅ All four amendments authored. Doc cascade landed. No code touched; engine-side refactor remains deferred to VS2b per Matt L3 lock.

**What landed:**

1. **canonical/32-progression-design.md** — new Section 13 authored (between Section 12.5 and Cross-section integration). Contents:
   - § 13.1 — Healing: cooldown-gated ability (10.0s baseline CD, 35% max-HP magnitude, 0.0s cast, no resource cost; retires potion-inventory; mana mechanic survives unchanged; freed inventory slots noted)
   - § 13.2 — React-or-auto interaction primitive (1.2s `auto_complete_window` baseline; applies to chests/doors/levers/NPC dialogue/shrines/lore-glyphs; does NOT apply to combat skills, loot equip, high-stakes activations, or substrate altars)
   - § 13.3 — Inventory-as-between-combat clarification (cross-ref to DoE § 4.4 + § 7.3)
   - § 13.4 — Portrait-primary mobile orientation note (cross-ref to DoE § 7.1 and the two mobile-doc amendments)
   - 📚 Reference notes — DoE / Diablo Immortal / D3-D4 / PoE / Last Epoch comparison

2. **canonical/17-gear-and-spirit-guide-design.md** — new section "Heal-cooldown affix family — retires potion-interaction affixes (LOCKED 2026-05-17)" added inside the "Updates 2026-05-11/12" zone (after the Auto-pickup rarity filter lock). Contents:
   - Retired affixes enumerated (5 families: potion slot / drop rate / magnitude / kill-grant / type-multiplicity)
   - New affix family table: `heal_cooldown_reduction` (flat -0.5 to -3.0s, magic+); `heal_cooldown_reduction_pct` (-5 to -15%, rare+); `heal_magnitude_bonus_pct` (+5 to +30%, magic+); `heal_magnitude_bonus_flat_hp` (+10 to +100 HP, magic+); `heal_secondary_effect` enum (`brief_invuln_1s|2s` / `cleanse_1_debuff` / `mana_refund_25pct` / `cleanse_all_dots`; epic+/legendary)
   - Stacking caps: CD floor 5.0s; magnitude ceiling 60%; secondary-effect cap 2 concurrent
   - Affix-coherence integration (role-orientation-agnostic; any slot; secondary-effect rides existing legendary-mechanic-tier infrastructure)
   - Spirit Guide interaction (treats heal-affixes as standard `power_score` contributors; no per-affix bias for struggling forms)
   - Engine-side execution map (rocket gen; star-lord telemetry; gamora re-convergence; jack-ryan Gate-1 advisory flag) — all deferred to VS2b

3. **canonical/story/mobile-ux-execution-plan-2026-05-17.md** — three sub-amendments:
   - § 4.3 (Orientation) — replaced with portrait-primary lock; rationale; implications (orientationOverlay logic inversion; HUD diagram TBD; M2-M7 dispatches consume portrait-amended plan; touch-target canon unchanged); pending portrait-diagram contents specified for M5/M6 dispatch
   - § 4.2 (HUD zone layout) — header amended to flag landscape diagram as secondary-orientation reference; portrait diagram TBD pointer added
   - § 7 (Phased execution plan) — preamble amended noting M2-M7 target portrait-primary when they fire VS2b; M1 typography orientation-agnostic; landscape support polish-phase

4. **canonical/story/mobile-pc-pixel-sizing-ratios-2026-05-17.md** — new § 3.5 "Portrait-primary tuning" authored between § 3.4 (Camera framing) and § 4 (Transformation principles). Contents:
   - Canvas + viewport implications table (944×1800 transposed; ~15m × ~28m world-area visible portrait; player ~10-12% viewport-height)
   - HUD element positioning table (portrait positions in canvas-space; landscape fallback parenthetical for polish-phase)
   - Density-preservation invariant restated under portrait (sprite scalar 0.75× holds; PIXELS_PER_METER 48 holds; sim-emitted values orientation-invariant)
   - Why portrait is primary (genre convergence; one-handed thumb-reach; notification overlay coexistence; App Store discovery + sharing)
   - Landscape support polish-phase fallback noted
   - Pivot reversibility forward-flag (architectural commitment: orientation is presentation, not sim)

5. **canonical/story/mobile-feel-target-doe-2026-05-17.md** § 11 (Cross-references) — bidirectional updates marking the four amendments as LANDED 2026-05-17 with pointers to this dispatch.

**Decisions made within gandalf's lane (not L3 escalations):**

- Heal baseline cooldown = 10.0s (center of DoE doc 8-12s recommendation band).
- Heal magnitude = 35% max-HP per cast (DoE-class; significant but doesn't trivialize boss windows).
- Cast time = 0.0s instant; no animation lock; no invuln window by default (invuln available as `heal_secondary_effect` affix).
- React-or-auto window = 1.2s (centroid of DoE 0.8-1.5s band).
- Heal-affix family is role-orientation-agnostic and slot-agnostic (intentional: heal is universal survival floor, not class-flavor).
- Heal-CDR stacking floor at 5.0s effective CD (50% of baseline; prevents zero-CD heal-spam builds).
- Heal magnitude ceiling at 60% max-HP (baseline 35% + 25 percentage-points headroom; preserves multi-cast burst-fight pacing).
- Mana / energy mechanic explicitly preserved unchanged (heal does not consume substrate-energy resources).

**Decisions deferred to subsequent dispatches (not gandalf's lane this round):**

- HP placement on mobile (DoE-pattern top-left attached-to-minimap vs D-series bottom-globe) — flagged in DoE § 7.4; drax M5/M6 portrait-layout dispatch resolves.
- Portrait HUD zone diagram contents — drax authors in M5/M6 dispatch per § 4.3 + § 4.2 amendments.
- Engine-side `STAMINA_POTION_USE` → `heal_ability` refactor in `combatant.py` — VS2b (gamora + star-lord + rocket).
- Gear-affix generation update (retire potion-interaction; emit heal-affix family) — VS2b (rocket).
- Heal-cast telemetry event schema — VS2b (star-lord).
- Convergence re-run with new affix family — VS2b (gamora).

**Cross-references audited (bidirectional):**

- DoE feel-target doc § 11 → updated with LANDED status for all four amendments + this dispatch reference ✓
- canonical-32 § 13 → cites DoE doc § 7.1-7.2 + this dispatch ✓
- canonical-17 amendment → cites canonical-32 § 13.1, DoE doc § 7.2, this dispatch ✓
- mobile-ux-execution-plan § 4.2 + § 4.3 + § 7 → cite this dispatch ✓
- mobile-pc-pixel-sizing-ratios § 3.5 → cites DoE doc § 7.1 + this dispatch ✓

**Out-of-scope honored:**

- ❌ No engine-side code or specifications authored (gamora/rocket/star-lord lanes preserved)
- ❌ No drax mobile code modified (doc cascade only)
- ❌ No M2-M7 portrait-layout pre-emption (those fire VS2b)
- ❌ No DoE feel-target doc content changes beyond the § 11 cross-reference update
- ❌ No jack-ryan Gate-1 advisory pre-emption (flagged for handoff; jack-ryan independently reviews canonical-17 amendment)

**Disciplines observed:**

- **#1 (math-before-code):** baseline cooldown / magnitude / window values specified with rationale before engine refactor begins; gamora + rocket inherit a defined design contract
- **#11 (attribution clarity):** every amendment cites the L3 lock provenance + DoE doc source section + this dispatch; future readers can trace decision lineage
- **#12 (semantic shift):** retired affix family is explicit; canonical-17 amendment lists 5 retired affix-name patterns so rocket's deletion pass is unambiguous; MIGRATION.md entry will follow at VS2b
- **#13 (avoid implicit-pillar drift):** orientation is explicitly a *presentation* concern (per § 3.5 pivot-reversibility note); sim/asset-pipeline/engine code remain orientation-invariant by architectural commitment
- **Survey-mode constraint (gandalf-specific):** descriptive content (what amendments landed) is separated from forward-flagged items (what's deferred); no "should" interleaved with "is"

**No pushback memo filed.** Path A doc-cascade was clean; the DoE feel-target doc had pre-staged the cascade in its § 7. One narrow flag: the heal-affix decision to make `heal_secondary_effect` epic+/legendary-tier mechanical-novelty is the most opinionated call in this dispatch; if rocket's affix-generation convergence work surfaces balance issues with the invuln-window or cleanse effects, that's the most likely lever to revisit. Flagged for awareness, not blocking.

**No tag.** Doc cascade is not code per dispatch direction.

**HANDOFFs:**

- **HANDOFF → jack-ryan:** Gate-1 advisory on canonical-17 heal-cooldown affix family amendment. This is a load-bearing canon change to the gear-affix pool taxonomy (discipline-#12 semantic shift). Your advisory gates the VS2b rocket implementation. Watchpoints: (1) heal-CDR stacking floor of 5.0s — is this the right floor given existing gear-stacking telemetry patterns? (2) `heal_secondary_effect` legendary-tier gating — does this match existing legendary-mechanical-novelty rate budgets (file 17 § "Legendary mechanical novelty")? (3) Spirit Guide marginal-value treatment of defensive expected-value contributions — does this need an explicit `power_score` weighting note before rocket implements? Parallel-safe with gamora D11 math note authoring.

- **HANDOFF → gamora + star-lord + rocket:** VS2b heal_ability refactor (informational; not active until D11 ships completion record). Design contract is now locked in canonical-32 § 13.1 + canonical-17 heal-affix amendment. When VS2b fires, your work consumes those amendments as the contract. Key contract points: cooldown baseline 10.0s; magnitude 35% max-HP + 50 HP floor; instant cast; no resource cost; 5 retired affix patterns; 5 new affix patterns. MIGRATION.md cross-seam entry needed at VS2b execution (Discipline #12).

- **HANDOFF → drax:** M2-M7 portrait-layout dispatches (informational; not active until VS2b fires). When the M5/M6 portrait-layout dispatch fires, you consume the portrait-amended mobile-ux-execution-plan (§ 4.2 + § 4.3 + § 7) and the portrait-tuned sizing canon (§ 3.5 of mobile-pc-pixel-sizing-ratios). Portrait HUD zone diagram contents are specified in mobile-ux-execution-plan § 4.3 (post-amendment) — authoring lives in M5/M6 dispatch. HP placement (DoE top-left attached vs D-series bottom-globe) remains open per DoE § 7.4 — resolve in M5/M6 with Matt L3 if needed.

**Hive-log STATE entry:** appended next.

— gandalf 2026-05-17

---

## Jack-ryan Gate-1 advisory — canonical-17 heal-cooldown affix family amendment

**Reviewer:** jack-ryan
**Date:** 2026-05-17
**Tag:** `jack-ryan/v1.6-doe-cascade-canonical-17-gate1-review-1`
**Verdict:** CONDITIONAL ENDORSE — VS2b rocket implementation may proceed; pre-flags below must be addressed at code-time or resolved by Matt before implementation.

### Pre-flags (addresses at code-time or by Matt)

**WARN-1 — Heal-while-stunned/frozen behavior not specified (contract gap for gamora)**

The canonical-17 amendment and canonical-32 § 13.1 specify: 0s cast time, no resource cost, no default invuln, 10s cooldown. What is NOT specified: whether `heal_ability` is interruptible by status ailments (stun, freeze, silence, root). In the current engine, potion use via `_maybe_use_potions()` is a free action at any point in the fight loop — it is not gated by ailment state. When gamora refactors this to `heal_ability`, the question of ailment-gating must be decided before `combatant.py` is written. Recommend Matt resolve: "instant, unconditional" (fires through stun/freeze — matches D4/DoE pattern) vs "ailment-gated" (cannot fire while silenced/frozen). The canonical-32 § 13.1 instant-cast framing implies unconditional, but this is not explicit. This is a VS2b contract gap.
Cite: Discipline #1 (math-before-code — missing design spec before gamora writes combatant refactor).

**WARN-2 — CDR stacking mechanics between flat and pct reductions not unambiguous**

The amendment specifies both `heal_cooldown_reduction` (flat −0.5s to −3.0s) and `heal_cooldown_reduction_pct` (−5% to −15%), noting they "stack additively with flat reduction." The stacking floor is stated as 5.0s effective cooldown. However, the order-of-operations for mixed flat+pct reduction is ambiguous:
- Option A: `effective_CD = max(5.0, baseline × (1 - sum_pct) - sum_flat)` (pct first, then flat)
- Option B: `effective_CD = max(5.0, (baseline - sum_flat) × (1 - sum_pct))` (flat first, then pct)

These produce different results. Example: baseline 10s, flat -2.0s, pct -10%:
- Option A: 10 × 0.9 − 2.0 = 7.0s
- Option B: (10 − 2.0) × 0.9 = 7.2s

Rocket needs an explicit formula. Recommend Option A (pct reduces baseline first, flat subtracts after) — this is PoE's approach and prevents runaway stacking better. Rocket should confirm with gamora before implementing.
Cite: Discipline #1 (math-before-code); Discipline #12 (semantic shift — new reduction category requires explicit stacking rule).

**WARN-3 — `heal_secondary_effect` legendary-tier enforceability requires new rocket infrastructure**

The amendment states `heal_secondary_effect` rides the "existing legendary-mechanical-novelty infrastructure." Inspection of `gear_generation.py` and the generation seam shows that the existing legendary-mechanical-novelty system (`granted_ability`, `aura`, `on_hit`, `cast_on_attack`) is documented in canonical-17 § "Legendary mechanical novelty" (LOCKED 2026-05-10) but there is no `heal_secondary_effect` enum field in the current gear schema or affix generation code. The `heal_secondary_effect` family is a new affix type — it is not structurally identical to `granted_ability` (which adds a hotbar skill) or `on_hit` (which procs on attack). Rocket must add:
1. `heal_secondary_effect` as a new affix category in `gear_schema.py` / `gear_generation.py`
2. Tier-gating logic that restricts it to epic+/legendary in the affix roller
3. The "cap at 2 concurrent" enforcement rule — this must be a character-state constraint, not just a generation constraint (two separately-generated items can each carry one; the cap is at equip/fight-start resolution, not at drop time)

This is new infrastructure, not a hookup into existing infra. Flagged for rocket awareness.
Cite: ADR-001 (decisions log — load-bearing contract change); Discipline #12 (semantic shift — new affix category requires explicit schema addition).

**INFO-1 — Magnitude ceiling wording: "25 percentage-points" vs "60% of max-HP" — clarify for rocket**

The amendment states: "heal_magnitude_pct_max_hp cannot exceed 60% of max HP (baseline 35% + cap 25 percentage-points of bonuses)." This is internally consistent (35 + 25 = 60) but could be misread as: "bonuses alone are capped at 25pp" vs "total is capped at 60%." Rocket implementing the enforcement should use the total-cap formulation: `effective_heal_pct = min(0.60, base_heal_pct + sum_of_bonus_pct)`. The baseline 35% counts against the 60% ceiling. No ambiguity in the math; just a readability note.
Cite: Discipline #1 (math-before-code — confirm implementation formula).

**INFO-2 — Spirit Guide `power_score` weighting for heal affixes not yet defined**

The amendment states Spirit Guide treats heal-CDR and heal-magnitude affixes "as standard contributors to `power_score` (calibrated as defensive expected-value contributions)." The calibration formula for "defensive expected-value" on a cooldown reduction affix is not specified here or in the gear/Spirit Guide design sections. This is consistent with being deferred to VS2b (it is an implementation-time calibration task for rocket/gamora), but it means rocket cannot implement Spirit Guide heal-affix scoring without a separate math note for the EV formula. Flag for gamora: when VS2b fires, a short math note on heal-CDR EV contribution is needed before rocket implements the power_score weighting.
Cite: Discipline #1 (math-before-code — EV formula needed before Spirit Guide implementation).

**INFO-3 — Retired affixes list does not cover spirit-guide-side potion affixes**

The retired affixes list covers gear-drop-side affix families. The canonical-17 base doc § "Spirit Guide" discusses the Guide's marginal-value math treating gear `power_score` contributions. If any Spirit Guide recommendation logic (or its `power_score` calibration) currently references potion-derived affix contributions, those references must also be retired in the VS2b refactor. The amendment does not explicitly call this out. Rocket/gamora should audit the Spirit Guide's `power_score` calibration code at VS2b time to ensure no potion-affix contribution paths survive. This is a VS2b code-audit item, not a design gap in the amendment itself.
Cite: Discipline #12 (semantic shift — retiring affix family requires audit of all consumers).

### Cross-seam contract verdict for VS2b execution

The design contract is sufficiently specified for gamora to author a math note for the `STAMINA_POTION_USE` → `heal_ability` refactor, with one exception: WARN-1 (heal-while-stunned behavior) must be resolved by Matt before gamora writes the combatant.py spec. All baseline values are locked (10s CD, 35% max-HP, 50 HP floor, 0s cast, no resource). The affix family table, stacking caps, and tier-gating are specific enough for rocket with the WARN-2 stacking formula clarification addressed.

### Gandalf watchpoints — verdict

1. **CDR stacking floor (5.0s):** Acceptable floor. At 50% of baseline, even a heal-stacking build retains meaningful cooldown pacing. The floor is not so high (e.g., 7-8s) as to make CDR affixes feel meaningless, nor so low (e.g., 3s) as to enable spam. No revision recommended.
2. **`heal_secondary_effect` legendary-tier gating:** Correct design call; the invuln window in particular is high-leverage and appropriately gated high. The enforceability gap (WARN-3) is a rocket infrastructure question, not a design question.
3. **Spirit Guide marginal-value treatment of heal affixes:** The "standard power_score contributor" framing is appropriate for launch. An explicit EV formula is needed before implementation (INFO-2) but the design direction is sound.

### Decisions-log entry

Per dispatch direction, the decisions-log entry "Heal mechanic + heal-affix family canonicalization (DoE feel-target lock 2026-05-17)" is authored below and will be appended to the decisions-log. See completion record below.
