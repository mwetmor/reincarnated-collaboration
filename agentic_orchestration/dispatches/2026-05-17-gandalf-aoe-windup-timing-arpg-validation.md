# 2026-05-17 — gandalf — AOE windup timing ARPG-mean validation

**Authority:** Matt L3 mid-flight playtest feedback (2026-05-17 ~12:10 EDT).
**Type:** Pattern A — ~0.5 day (research + recommendation; no code).
**Predecessor:** gandalf § 3.2 AOE telegraphed combat briefing (substrate-coupled windup values authored).

---

## Why this matters

Matt's playtest: "The skill geometry on floor is really good! Question: is there an advanced timing to allow player and enemy combatants to predict the move and have a bit of time to avoid? It feels like this already exists, but if not we should consult gandalf and attune the announcement floor geometry timing to ARPG standard mean."

The system exists (drax v1.0 ships substrate-coupled windup; engine emits `windup_duration_seconds` via rocket v1.7 schema). What Matt is asking is whether the **current values** are tuned to genre mean — or if they're too short / too long for player anticipation. This is a white-wizard judgment question that's squarely your lane.

---

## Required reading

1. Current substrate windup values (gandalf § 3.2 authored — your prior decision):
   - shadow: **0.2s** (concealment — fastest, indicator appears only in last 0.2s)
   - earth: **0.4s**
   - wind: **0.5s**
   - lightning: **0.5s**
   - fire: **0.6s**
   - holy: **0.7s**
   - water: **0.7s**
2. Range: bounds [0.0, 5.0]s enforced at substrate identity loader (rocket v1.7).
3. `canonical/story/aoe-telegraphed-combat-briefing-2026-05-17.md` § 3.2 — your prior briefing's reasoning chain for these values

---

## Scope

### Item 1 — ARPG genre-mean characterization

Survey your white-wizard knowledge base (Diablo II/III/IV, PoE 1/2, Last Epoch, Grim Dawn, T4ARPG):

- **What's the typical AOE telegraph duration for mob ground effects in the genre?**
  - D4: roughly 0.6-1.2s for telegraphed ground effects
  - PoE: roughly 0.3-0.8s typically
  - Grim Dawn / Last Epoch / others?
- Document the **range** (min-max) and the **mean** (or genre cluster) you'd identify as canon

### Item 2 — Validate current values against the mean

For each substrate, answer:
- Is the current value within genre range? (likely yes for all)
- Is the current value at, above, or below the genre **mean**?
- If a value should shift, propose new value + rationale (e.g., "earth 0.4s feels slightly fast for the 'positional refusal' cosmology; recommend 0.5s — still in fast cluster but allows one extra player reaction frame")

### Item 3 — Special case for shadow

Shadow's 0.2s is intentional concealment (your § 3.2 design). But Matt's question is whether 0.2s allows ANY player reaction. Validate:
- Is 0.2s "fair" by ARPG canon (e.g., D4 cold-blooded mobs)?
- Or should it bump to 0.25-0.3s and rely on the late-appearance pattern (indicator visible only in last 0.2s of a 0.4s windup, for example)?
- Decision is yours; document rationale

### Item 4 — Player AOE telegraph question (revisit)

Your § 3.6 + drax v1.0 dispatch noted: "Player AOEs do NOT telegraph (solo gameplay; player chose the cast)." Matt's playtest framing is monster-focused, but worth revisiting in light of his question:
- Should player AOEs telegraph in any case (e.g., self-damage tells, friendly-fire prevention)?
- Or stays as-is for v1.0 (no player telegraphing)?

Recommendation only; if you stay with status quo, no action item — note the decision and move on.

### Item 5 — Output

Author a brief addendum to `canonical/story/aoe-telegraphed-combat-briefing-2026-05-17.md` (or a new § 5 if cleaner):
- Genre-mean characterization
- Validation result per substrate (KEEP / ADJUST → new value)
- Shadow 0.2s ruling
- Player-AOE telegraphing decision

If any substrate values change, hand off to **rocket** for substrate identity YAML amendment (~5 min Pattern A micro-task; rocket bumps the values in `config/substrate_identities/*.yaml` and re-tests substrate loader).

### Item 6 — Hive log + tag

- STATE entry with summary verdict (all KEEP, or N substrate adjustments)
- Tag `gandalf/v1.6-aoe-windup-arpg-validation-1`

---

## Out of scope (DO NOT)

- ❌ DO NOT redesign the windup system (already shipped; only validate values)
- ❌ DO NOT change the cosmological coupling (each substrate's windup duration is genre-coherent to its identity — shadow fast, water slow)
- ❌ DO NOT modify rocket's YAML files yourself; hand off if changes are warranted
- ❌ DO NOT expand scope to indicator-color tuning (different concern)

---

## Acceptance criteria

- [ ] Genre-mean ARPG windup characterization documented
- [ ] Per-substrate validation: KEEP or ADJUST with rationale
- [ ] Shadow 0.2s ruling documented
- [ ] Player-AOE telegraphing decision (status quo or change)
- [ ] Briefing addendum authored (or new § 5)
- [ ] If adjustments needed → rocket hand-off dispatch authored
- [ ] Tag `gandalf/v1.6-aoe-windup-arpg-validation-1`
- [ ] Hive-log STATE entry

---

## Smoke expectation

Matt reads the addendum; either confirms values are genre-aligned (no further action) or rocket spins a ~5-min YAML amendment + re-test loop, then engine regen consumes new values on next gamora pass.

---

*Dispatched 2026-05-17 by knight-rider per Matt L3 mid-flight playtest. ~0.5 day. Append completion record when done.*

---

## Completion record — 2026-05-17 ~14:00 EDT — gandalf

**Status:** COMPLETE.
**Tag:** `gandalf/v1.6-aoe-windup-arpg-validation-1` (applied at commit landing).
**Actual scope:** ~0.5 day as estimated (research + addendum authoring + hand-off dispatch).

**Verdict:** 5 KEEP, 2 ADJUST.

| Substrate | Locked | Verdict | New |
|---|---|---|---|
| shadow | 0.2 | KEEP (intentional sub-floor for *concealment* cosmology) | — |
| earth | 0.4 | **ADJUST** | **0.5** |
| wind | 0.5 | KEEP | — |
| lightning | 0.5 | KEEP (B13 forward-note: two-stage telegraph) | — |
| fire | 0.6 | KEEP | — |
| holy | 0.7 | **ADJUST** | **0.9** |
| water | 0.7 | KEEP | — |

**Genre-mean characterization (Item 1):** Mob-tier ground-AOE telegraph canon across D3/D4/PoE1/PoE2/LE/GD/Lost Ark — floor ~0.4s, **mean ~0.7s**, ceiling ~1.0s. Locked cluster mean 0.51s sits ~0.2s below genre mean; cluster spread 0.5s narrower than canon ~0.6s.

**Per-substrate validation (Item 2):**

- **Earth ADJUST 0.4 → 0.5:** Earth cosmology is *positional refusal — what does not move and will not be moved*; 0.4s contradicts deliberateness (faster than wind, the kinetic substrate). Genre-canon earth-coded mobs cluster 0.5-0.9s. 0.5s honors cosmology while staying in fast cluster.
- **Holy ADJUST 0.7 → 0.9:** Holy cosmology is *revelation — the substrate that announces itself with light before the strike*; 0.7s collapses holy into "fire with white tint." Genre-canon holy mobs 0.8-1.5s. 0.9s makes holy unambiguously slowest (correct cosmology) AND widens cluster spread from 0.5s to 0.7s (improves D27 discriminability).
- **5 KEEPs:** shadow/wind/lightning/fire/water all read clean against genre canon AND their cosmological identity declarations. Detailed rationale in briefing § 11.3.

**Shadow 0.2s ruling (Item 3):** **KEEP.** Intentional sub-floor for *concealment*; bottom-edge of dodgeable canon (matches D4 Cold-Blooded / PoE Heist / Lost Ark stealth at 0.2-0.4s). Shadow asks the player to *anticipate* (cast-animation read), not *react* (indicator dodge). Trait pool rewards anticipation; the 0.2s makes that reward legible. Documented as intentional difficulty asymmetry, not tuning miss.

**Player-AOE telegraphing (Item 4):** **Status quo preserved — player AOEs do NOT telegraph.** Solo-gameplay convention; cast animation IS the player's own telegraph. Matt's playtest framing interpreted as monster-side (predict enemy AOEs by reading indicators) rather than player-side. No action item.

**Artifacts produced:**

1. **`canonical/story/dodge-plus-telegraphed-combat-l3-briefing-2026-05-17.md` § 11 addendum** — full ARPG genre-mean characterization, per-substrate verdicts with rationale, shadow ruling, player-AOE decision, summary verdict table.
2. **`agentic_orchestration/dispatches/2026-05-17-rocket-aoe-windup-arpg-tuning-yaml-amendment.md`** — Pattern A ~5-10min micro-task to rocket: earth.yaml `0.4 → 0.5`; holy.yaml `0.7 → 0.9`. Acceptance criteria + MIGRATION.md format + downstream consumer notes (gamora reactive-escape + drax opacity-ramp; both consume the field as-is).
3. **Hive log entries** — PRE-SIGNAL (§ 14.1.1 fetch-before-commit discipline satisfied; local 9 ahead of origin, no remote-only commits); STATE summary; HANDOFF → rocket.

**Acceptance criteria** (per dispatch):

- [x] Genre-mean ARPG windup characterization documented (§ 11.2)
- [x] Per-substrate validation: KEEP or ADJUST with rationale (§ 11.3)
- [x] Shadow 0.2s ruling documented (§ 11.4)
- [x] Player-AOE telegraphing decision (§ 11.5; status quo confirmed)
- [x] Briefing addendum authored (§ 11; appended to dodge-plus-telegraphed-combat briefing)
- [x] Rocket hand-off dispatch authored (Pattern A; earth + holy YAML)
- [x] Tag `gandalf/v1.6-aoe-windup-arpg-validation-1` (applied at commit)
- [x] Hive-log STATE entry (PRE-SIGNAL + STATE + HANDOFF)

**Cluster after rocket landing:** shadow 0.2 / earth 0.5 / wind 0.5 / lightning 0.5 / fire 0.6 / water 0.7 / holy 0.9. Mean 0.557s; spread 0.7s. Genre-mean alignment improved; cosmological coherence improved; D27 perception-test discriminability improved.

**Smoke expectation (post-rocket):** Matt's next playtest after gamora's next regen pass will perceive earth ~+6 frames more deliberate (+25% windup) and holy ~+12 frames more announcing (+29% windup). The locked windup system as a whole was already substantially genre-aligned — the playtest question is answered with high-confidence-mostly-keep verdict + two targeted cosmological refinements.

**Forward-notes (out of scope for this dispatch; B13-post-VS2a candidates):**

- Lightning two-stage telegraph (first-arc instant + chain telegraphed) per original § 3.2 design; richness refinement after chain mechanics richen.
- Shadow late-commit indicator pattern (indicator hidden during 0.1-0.3s pre-telegraph; visibly commits at 0.2s before damage) — current implementation may already do this via the 0.2s value alone, or may want drax to add the late-commit ramp pattern explicitly. Worth a drax check after rocket lands.

— gandalf, 2026-05-17
