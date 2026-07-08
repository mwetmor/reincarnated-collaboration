# Minigame Template Taxonomy — gandalf review

**Date:** 2026-07-07 · **Reviewer:** gandalf (DRIFT-CRITIC on intake, senior-designer voice)
**Reviewing:** `matt_notes_handoff_docs/reap-die-rise-minigame-template-taxonomy.md` (Matt mobile-conversation product)
**Scope frame:** post-launch in-game activity layer ("arcade") — **nothing here gates the One Realm MVP / demo lanes.** Intake precedent: the agnostic-loot mobile draft (2026-07-06 review → Pattern-B rulings → canonical absorption).

---

## 0. Top-line

**SOUND as a taxonomy — adopt with four flags.** The laws are the right laws, the lineage pool is the correct ancestral canon (WC3 customs are *the* precedent for one-runtime/many-rule-packets), and the certification section is more rigorous than minigame specs usually bother to be. The four flags: one vocabulary conflict with retired canon framing, one scope-gravity risk (the strategic finding), one certification gap on T2 templates, and one fiction hook the doc doesn't know it already owns.

## 1. What's strong (keep verbatim on canonization)

1. **LAW 1 (packets, not code) is the project's own spine extended to game modes.** The arcade runtime is to minigames what the kit pipeline is to kits: emission → packet → deterministic interpretation. Deep architectural consistency, not a bolt-on.
2. **LAW 4's membrane is schema-enforced** — "no power category exists in the schema, so the law cannot be violated by content emission" is the strongest form a design law can take. The genre graveyard it fences off: Diablo Immortal's power-crossing resentment; D3's RMAH poisoning the loot thrill. The gray-zone adjudication table is the right governance instrument — a living table, extended per case, exactly like our decisions-log discipline.
3. **Bots-first + rungs 1–3 at zero netcode** is correct for team size, and rung 3's async ladders + score ghosts is the Trackmania/daily-run pattern — human competition without real-time infra. The rung gates are empirical (recognition → validate → commit shape).
4. **Two-tier certification** — *"kits converge on balance; minigame packets converge on fun"* is a real design sentence. Reusing the gauntlet fitness machinery + the loot blacklist for draft pools is the cheap-and-right reuse.
5. **The naming law matches loot canon exactly** (C5: readable compression of function, no opaque flavor; D1 vocabulary-commonness carries over). "Emberline Wars — Double Send" passes the same test "Twinfang" passes.
6. **Kits-not-1v1-tuned is respected structurally:** HLW routes competition *through the hordes*; control zones are taken by AOE-clear and body-mass; Warlock is correctly flagged as the most constraint-sensitive. The taxonomy knows where the sim's certification authority actually extends.

## 2. Canon-coherence findings

1. **Season-vocabulary flag (OP § 3.7(b)).** "Seasonal kit tranches," "season-synchronized tranches" (LAW 3), "packets per season cadence" (§ 9) — the season-N framing was RETIRED 2026-06-02. A live-ops cadence for a *launched* game is a real future need (and may even publicly ship named "seasons" — PoE leagues, D3 seasons are the genre convention), but in-canon the word carries the retired release-model's baggage. **Reframe to "kit tranche / rotation cycle" on canonization; Matt names the live-ops cadence deliberately later.** Flagged, not purged — it's Matt's draft and the underlying concept (synchronized content tranches feeding both surfaces) is sound.
2. **The Grimoire hook is already in canon and the doc doesn't know it.** *"You learn kits by reaping and fighting them"* = the claimed-souls register (gameplay-loop § 11 capture-and-summon; A11 two-register Grimoire). Boss Rush's "bosses ARE scaled kits" lands on the **already-confirmed trial-room boss-gallery design intent.** When the activity board earns a diegetic name, it isn't a new invention — it's the faith's **trial-grounds**, reapers sparring against bound souls. § 8 shelving narrative integration is fine; the note here is that the fiction is half-built and *free*.
3. **Membrane vs. the cleansed-crossing law: compatible by construction.** Arcade rewards are hub/meta-layer objects (banners, skins, titles) — the Grimoire's persistence register, not run-scale loot. Nothing the arcade grants is gear, so § 6 cleansed-crossing (gear stays unless cemented) is never touched. One clarifying line for the gray-zone table: the loot-pet BAN is on the *crossing*, not on pets — the main game's own (deferred) pet system is unaffected by this law.
4. **Solo-only main game stays intact — and the arcade is the pressure valve.** Co-op/PvP demand gets a home that never forces the main loop to compromise its solo certification. Worth stating as a design virtue on canonization, not leaving implicit.

## 3. Gaps / pushback

1. **T2 effort tags under-count the SIM side (certification gap).** LAW 6 says the sim certifies fairness — but the sim cannot certify what it cannot simulate. Warlock's fitness (TTK, ring-out ratio, kingmaker index) needs displacement/collision the battle sim does not model; TD's fitness (leak curves, maze diversity) needs pathing + static entities. So T2 = new **runtime** primitives (drax) AND new **sim** primitives (gamora) — two seams, roughly double the tagged cost. **Recommend: two-axis effort tag (runtime × sim/cert).** This strengthens the doc's own conclusion: defer T2 until traction earns it.
2. **Rung-1 scope-gravity — the strategic finding.** The strategy header calls the arcade a "staged windfall layer," but § 5.1 says horde survival "doubles as main-game endgame content." ARPG law: **the game begins at endgame** (D3 vanilla → RoS is the canonical lesson; Rifts entered as a side mode and became the game). If horde-survival IS the endgame answer, Rung 1 is launch-adjacent, not post-launch, and the packet runtime rides the critical path earlier than the header admits. **Fork for Matt at launch-scope planning (not now):** (a) EMBRACE — design endgame AS arcade-rung-1; packet runtime becomes launch scope; (b) FENCE — endgame is a separate design; arcade debuts strictly later. My lean: (a) — it's where D3/PoE history points, and it's the cheapest possible endgame ("literally the battle sim with a camera on it") — but it must be a deliberate ruling, not drift.
3. **Two missing registers (one-column additions each):**
   - **Session-length register** — WC3 customs lived at 15–45 min; an in-game activity should probably band **5–20 min**. Only HLW carries a game-length fitness band; make it a taxonomy-level column so template params inherit it.
   - **Touch-viability register** — mobile-class specs are a standing target (Q11 contingency language). Warlock (aim) and TD (placement UI) are input-sensitive. A touch column steers sequencing cheaply.
4. **Fitness definitions are a named handoff, not a flaw.** Comeback/snowball/kingmaker indices and hiding-entropy are undefined — correct at taxonomy level. At build time these are design-spec-as-math (gandalf) → gamora, per Discipline #18. Note also: the sim's seeded determinism means **the replay IS the ghost format** — § 9's async-ladder infra question largely answers itself (input-traces + seeds, no video, no server-side replay engine).

## 4. Disposition recommendation

- **Canon home:** `canonical/reap-die-rise-game/arcade-minigame-taxonomy-spec.md`, STATUS: **POST-LAUNCH SCOPE** (explicitly does not gate MVP/demo). It is the *same product* — "activities inside the main game" per its own strategy header — so it belongs in the game spec folder, not a future-product parking lot.
- **On canonization** (fires on Matt's word, cheap): banner the mobile draft superseded-by-canon (loot precedent) · season-vocabulary reframe (§ 2.1) · two-axis effort tags (§ 3.1) · session-length + touch columns (§ 3.3) · trial-grounds fiction note (§ 2.2) · membrane clarifying line (§ 2.3).
- **Tracker:** one PARKED row on the game tracker ("arcade layer — post-launch; spec parked; `gates-on: launch-scope-planning`") so Glance shows it honestly. No matt_decision_needed row — nothing gates current work.
- **What waits:** all build-side work (runtime primitives, packet schema ratification, fitness math) until the § 3.2 endgame fork is ruled at launch-scope planning. That fork is the only load-bearing decision in this layer, and it isn't due yet.

## 5. Additions to the doc's own § 9 (open decisions)

- **The endgame fork** (embrace/fence — § 3.2 above). The load-bearing one.
- **Live-ops cadence naming** (the season-vocabulary successor term).
- **Touch-viability** per template (mobile input).
- **Diegetic frame** for the activity board (trial-grounds hook — one story-session line, nearly free).

---

**Signed:** gandalf, 2026-07-07. *The arcade's first rung is secretly an endgame system wearing a party hat — decide which costume is the real one before launch-scope planning, and the rest of this taxonomy can wait exactly as long as it claims it can.*
