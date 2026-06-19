# KR autonomous run-prompt — FOLDED season-1 completion run (sim + pipeline-spine, one sequence)

**To:** knight-rider (orchestrator)
**From:** gandalf (authored at Matt's request, 2026-06-18)
**Mode:** ONE folded, sequenced, autonomous run. Matt fires it and is NOT present mid-run.
**Push:** PRE-AUTHORIZED (Matt 2026-06-18) — run-close push-pattern. Push the run's accumulated commits at run-close; no return-ask.
**Pull first:** `git pull origin main` at run-start (capture any cross-host commits) before reading the specs below.

---

## 0. What this run is — and why ONE run, not two

Two seam-independent workstreams, FOLDED into one sequence:
- **Run-A (sim):** gamora · `reincarnated-engine/src/reincarnated/simulation/` (+ `spirit_guide/`).
- **Run-B (pipeline-spine):** star-lord + rocket · `export/` · `output/` · `generation/`.

**Why folded, not two parallel runs** (Matt offered the split; gandalf ruled ONE):
1. **Shared commit target.** Both workstreams auto-commit to `main`. Two concurrent KR sessions would race on commits — a real hazard, not theoretical.
2. **Destructive-last ordering.** The one destructive item (BC Stage-3 prove-then-delete) must run AFTER all additive work so its prove-gate sees the FINAL tree (it can only catch a consumer of the legacy archetype machinery introduced earlier in the run if it runs last). A single sequence guarantees this; two parallel runs cannot.
3. **Fire-once cadence.** No one is present to fire a second run.

Parallelism buys nothing here (the bottleneck is the firing + the commit target, not CPU). One sequenced run is strictly safer.

---

## 1. The binding contract — READ THESE FIRST (in order)

1. **Endorse-criteria (the gandalf design-intent gate; per-item ACCEPT / HONEST_FAIL / PARK + the keystone K-1/K-2/K-3 rule + §1.5 sequencing):**
   `agentic_orchestration/gandalf/notes/2026-06-18-pre-registered-endorse-criteria-two-runs-and-keystone-sweep.md`
2. **Faction content-shape spec (P2's full field-partition + writer contract):**
   `agentic_orchestration/gandalf/notes/2026-06-18-faction-content-shape-emission-spec.md`
3. **Caster-crater disposition (the caster-Lever-C probe + its pre-registered verdict rule):**
   `agentic_orchestration/gandalf/notes/2026-06-18-caster-upper-tier-crater-disposition.md`

The endorse-criteria doc is the master; the other two are its referenced sources. **Compose them with jack-ryan Gate-2** (engineering-correctness, BLOCK authority). A Tier-1 close requires BOTH gates: jack-ryan Gate-2 (does it work / regress / hold) AND the gandalf endorse-criteria (does it preserve what the feature is FOR).

---

## 2. Gate composition + the three-tier decision envelope

- **Tier-1 — AUTONOMOUS close.** jack-ryan Gate-2 PASS **and** the item's gandalf endorse-criterion (§2–§4 of the master) PASS. Commit the work-product. No live gandalf turn.
- **Tier-2 — PARK for gandalf.** Log the park, leave the item UNCOMMITTED, continue with other items. Triggers (master §5): any band-refit past the pre-registered threshold; any keystone-ceiling interaction; any schema contradiction; **any HONEST_FAIL that lands OUTSIDE the pre-registered shapes** (an unanticipated failure is definitionally a gandalf-park); any pressure to re-impose a STRUCK scope item (the phantom season-1 NPC type — do NOT let any build re-introduce it).
- **Tier-3 — PARK for Matt.** Frame, do NOT decide: the P1 route-vs-replace architecture choice; the keystone-ceiling design CALL (under sweep-result K-1/K-3); the boss-bridge family calls (rogue (a)/(b); caster if the probe returns composition); any LOCKED-decision re-open (MOB_HP 1.5×; the band fit beyond mechanical refit; the BC ACCEPT ruling; the six-type season-1 bundle).

**CARDINAL RULE: when in doubt, PARK UP a tier, never DOWN.** An over-park is a deferred build (cheap); an under-park is a design betrayal committed unattended (the exact thing this contract prevents).

---

## 3. THE SEQUENCE — execute in this order (master §1.5)

### Step 1 — Diagnostics first (zero-commit, zero-risk; surface any park early)
- **Caster-Lever-C probe** (gamora) — master §2.1. Reuse the existing Lever-C harness. Run the four caster cells at BOTH M=1.0 and M=0.30, magic_pack at NORMAL difficulty. Verdict rule (binding, caster-disposition §3): zero mini_boss/boss kills at M=1.0 → COMPOSITION; meaningful kills → SUPPRESSION. Diagnostic only — commits NO fix.
- **Keystone sweep** (gamora) — master §4. Descending keystone-magnitude ladder at fixed MOB_HP 1.5× on the saturated open_arena faithful reference. Interpret per the pre-registered K-1 / K-2 / K-3 rule. The sweep (investigation) is Tier-1; the keystone-ceiling CALL is Tier-3 (Matt) under K-1/K-3, self-resolves NEGATIVE under K-2.

### Step 2 — Additive + calibration (commit per item on joint-gate PASS; no destructive touch)
- **P2 faction writer** (star-lord + rocket) — master §3.1 + the faction spec. Emit the ~14 bundle fields, ~10 to telemetry, embedded IN the unified bundle (NOT the loadout sidecar), `faction_visibility = VISIBLE`. **Design-intent guard: factions are ORGANIZING + PRESENTATION, never a combat mechanic** — do NOT emit faction data into any field the fight model reads.
- **P3 monster wiring** (rocket + star-lord) — master §3.2. Wire `monster_generator.py` into the cycle-14 unified bundle vs the doc-34 sanctioned monster shape.
- **P5 weapon emission** (star-lord + rocket) — master §3.3. Populate `main_weapon` from `substrate_weapon_binding` as a SEPARATE descriptor from gear (weapon = kit's signature/identity, not a roll-able gear slot). Provisional ruling — Tier-2 bounce on shape ambiguity; do NOT fabricate weapon identity at emit.
- **P1 emitter scaffolding ONLY** (star-lord + rocket) — master §3.4. Build the per-type emitter blocks driver-agnostically. **Do NOT bake route-vs-replace** (that seam parks Tier-3 — see Step 4).
- **B4 summon-construct calibration** (gamora) — master §2.3. Calibrate `proxy_power_per` + `proxy_max_active` (`generation/skill_schema.py:185,198`) off scaffold-1.0 to band, against the §7 proxy budget math. **Discipline-bounded:** `proxy_max_active` hard wall intact, `s ∈ (0,1)`, army = extension of offense (not an afk-autobattler). PARK Tier-2 if seating the summoner would force a BAND refit or breach the wall / `s` bound.

### Step 3 — Destructive LAST
- **BC Stage-3 prove-then-delete** (gamora) — master §2.2. **The prove-gate FRONTS the delete:** re-demonstrate behavioral equivalence at the deletion boundary (byte-identical / within Stage-2 0.00 tolerance, same seeds) BEFORE the destructive deletion of the legacy machinery (`ARCHETYPE_ROLE_PRIORITY`, `_PLAYER_CONTROLLER_ARCHETYPES`, `ARCHETYPE_TEMPLATES`, `legacy_archetype_shim`). **Non-negotiable (Disc #12/#39): the tri-state guards (FALLBACK + LOUD-DEFAULT) must SURVIVE the deletion.** If the prove drifts → DO NOT DELETE → PARK Tier-2. The destructive step is autonomous-eligible ONLY because the prove-gate fronts it.

---

## 4. The Tier-3 seam that parks WITHOUT blocking the run

- **P1 top-level assembly — route-through-vs-replace** (Matt, Tier-3). Does the single driver route cycle-14 content THROUGH `season_exporter` or REPLACE it? Park it. **The run still proceeds:** the per-type emitter blocks (Step 2) are specified driver-agnostically, so they build and validate independently; only the final stitch waits for Matt's architecture call.

---

## 5. Run-close deliverable (for Matt's return)

A single run-close report containing:
1. **Per-item status table:** each item → CLOSED (both gates passed, committed) / PARKED (tier + one-line reason) / HONEST_FAIL finding (which pre-registered shape).
2. **The park-stack:** every Tier-2 (gandalf) and Tier-3 (Matt) park, each FRAMED — especially the design CALLs the diagnostics teed up (caster probe verdict → boss-bridge call; keystone sweep K-branch → keystone CALL; P1 architecture).
3. **Push confirmation:** accumulated commits pushed at run-close per the pre-auth.
4. **jack-ryan Gate-2 record** for each Tier-1 close (the engineering half of the joint gate).

---

## 6. Stop conditions (the run halts an item rather than guess)

- A **Tier-3** item is NEVER auto-resolved (frame it, park it, continue).
- A **destructive step** NEVER proceeds on an unproven boundary (BC Stage-3 prove-gate must pass clean).
- A **locked decision** is NEVER re-opened autonomously (MOB_HP 1.5×; bands HOLD as-fit; six-type bundle; BC ACCEPT).
- The **struck NPC type** is NEVER re-introduced (season-1 is six types: kits / monsters / factions / gear / weapons / flavortext).
- When in doubt → **PARK UP**.

---

**Authored:** gandalf, 2026-06-18, at Matt's request. **Fire-readiness:** the three specs are committed (`904c43b` faction · `8d0859b` caster-crater · `5056ec7`+`81b571c` endorse-criteria); push is pre-authorized; B4 is grounded; seven of eight items are autonomous-eligible; only P1's top-level assembly parks for Matt while its emitters proceed. This prompt is self-contained for an unattended fire.
