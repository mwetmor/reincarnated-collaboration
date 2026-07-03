# Skill Handoff — 2026-07-02 — One Realm MVP: Godot spine CLOSED + two-lane wave FIRING

**Author:** knight-rider · Matt-facing (per OP §3.1)

---

## Pending Matt-decisions queue

| # | Decision | Gating criterion | Where it surfaces |
|---|---|---|---|
| **Q7** | **Hero-rig retarget approach (BoneMap vs GeneralSkeleton)** — THE big Godot unblock | Blocks ALL Godot render/capture (D5 VFX, D6 floor authoring + G2, D8 UI). Lane A logic cores landed headless; everything visible waits on this. Matt picks approach → drax executes | `matt_decision_needed/` Q7; `reincarnated-godot/AGENT_STATE.md` (2026-06-20 block) |
| **Q8** | **Camera B — G3 sign-off** (FOV=40/pitch=−55°/yaw=47°-fixed/dist=34m) | drax's D6 camera beat caught a bad cam on floor 1 + validated the replacement; G3 is Matt's; ratified EARLY because every descent beat inherits it | `matt_decision_needed/` Q8; `reincarnated-godot/data/camera_floor1_ratification.md` |
| 1 | **Ranged-proxy nav fork** — fix nav (Lane B) vs. EXCLUDE ranged summoners from v2 curation | gandalf lean: EXCLUDE (melee certifies clean; nav fix post-demo). Does NOT gate B4 (run emits; B5 curation chooses). | B5 report (after B4 lands) |
| 2 | **Run-registry schema** — the minimal runs-table write shape | star-lord proposes with B4 → jack-ryan Gate-1 → Matt ratifies | B4 (HELD until B1 lands) |
| 3 | **Push authorization** — engine repo ahead of origin; meta-repo carries this session's relay + fold + wave + tracking commits unpushed; godot repo `300d07b` unpushed | Matt-explicit per ADR-006 (relay §1 confirmed the prior chain is on remote; forward = commits auto-fire, push at wave boundaries Matt-authorized) | Now — awaiting go |

## ⛔ HEADLINE — B1 built against a RETIRED family (Matt ruling needed on re-base path)

**gamora Phase 2 landed (`02d7cd5`) and CLOSES the dispatch mechanically (A2/A3/A5/A6 PASS) — but against the WRONG family.** Timeline: rocket Phase 1 (`17d5f80`, 21:55) + gamora Phase 2 (`02d7cd5`, 22:07) both executed the **drafted v1 S1–S6 register**. At **22:04** — between the two — a parallel gandalf session executed **Matt's own prior-art catch** (*"didn't we already have these scoped in a doc? I know for a fact we did"*) and REVISED the spec in place (`608c120`): v1 S1–S6 **retired**, the **ratified catalog-v2 PROXY family** (ASCENSION/SOVEREIGNTY/FISSION/INVERSION/CONVERGENCE/DUAL_PROXY, already in `t4_catalog_v2.py:53-58` with 7 gen-side consumers) **governs**. The revised spec closes verbatim: *"B1 fires against THIS revision."*

**What this means:** the execution-layer strategy classes rocket built (`mechanic_alteration.py:986+`) are a duplicate parallel register the ratified spec now retires. The ratified six have **different eligibility gates and mechanics** (FISSION = on-death split; INVERSION = role-inversion; SOVEREIGNTY = parallel combatant) — a re-base, not a rename. The A3 "Matt-doubt PASS" (bone→LEGION / crypt→BULWARK, different tops) is a **valid method against the wrong family** — the differentiation machinery works; the members are retired. **Not wasted:** the §1 problem statement, W2/D3 evidence, η/emission machinery, R1–R5 boundary assertions, dormant-five revival, and test scaffolding carry forward per spec §3 retirement map.

**RESOLVED (Matt ruled the re-base, 4 rulings folded into spec v3):** five-name dormant register RETIRED (provenance closed in git — never designed) · ZONE_CONTROL = newly-designed 26th catalog member · demo family = FIVE members, two-phase (P1: ASCENSION+SOVEREIGNTY+FISSION+ZONE_CONTROL; P2: CONVERGENCE+DUAL_PROXY behind gandalf Q6/Q7) · **PROXY_INVERSION DEFERRED WHOLLY** (kit-viability + timing-degeneracy). **B1-REBASE dispatch authored + Gate-1 CLEARED (ENDORSE-WITH-FOLDS ×2) + ✓ CLOSED** (`2026-07-02-rocket-gamora-proxy-t4-suite-REBASE.md`; Phase 1 `rocket/v-proxy-t4-rebase-strategies-1` @ `40e351e` → Phase 2 `gamora/v-proxy-t4-rebase-eval-1` @ `67fc0a9`; both Disc #11-verified). The re-based catalog-v2 PROXY family is the shipping proxy-T4 spine. Two refutation-conditions routed to B4 (A3 fixture-energy designation; F-f enforcement consumer).

**Gate-1 caught a factual correction (both critics converged):** spec §6.1 leaned ZONE_CONTROL into COMBAT, but `GEOMETRY_COLLAPSE` is in the **GEOMETRY** family (`t4_catalog_v2.py:91`) — jack-ryan (delegated family-ruler) ruled **ZONE_CONTROL → GEOMETRY + GEOMETRY max-1 rule**; gandalf corroborated. This resolves both reserved ZONE_CONTROL items as a clean within-family rule. spec §6.1 correction is gandalf-owed (routed). **Carried Matt-plate (not a blocker):** Phase-1 defensive-lane capstone thinness — a pure-defensive non-Bodyguard kit has only ASCENSION at Phase-1 demo (INVERSION deferred, DUAL_PROXY is Phase 2); empirical gate = defensive-proxy-bin count on the B4 run.

**Held:** B4 (consumes the family) + B5 (curates it) gate on the RE-BASED B1. B2 (gear, Set-#6 lane) is family-independent but shares the engine tree → serializes behind the re-base. Phase 3 (CONVERGENCE + DUAL_PROXY) is a LATER dispatch behind gandalf's Q6/Q7 artifacts.

## §20d headline datapoint (surfaced to Matt, not a blocker)

**54 kits → 19 distinct verb signatures (collapse 2.84); refutation did NOT trip (19 ≥ 6).** Distinct verbs are CHEAP to realize (proven — the realizer is a pure projection), BUT the bundle's emitted primitive variety at the primary-attack layer is SHALLOW (2 geometries, 1 composition_mode, uniform strike). The cheapness is proven; the primitive-depth is the thing to watch for the 400-promise — candidate feedback into rocket generation / star-lord emission for bundle-v2 richness.

## Active workstreams + status

- **Lane A (Godot, drax) — CORES LANDED, render rig-blocked:** D5/D6/D8 logic cores DONE (`300d07b`, 3 tags, verified Disc #11). Summon verb plays end-to-end; camera beat validated CAMERA B; grimoire+glyphs honest. Render/capture layer (VFX, floor authoring, G2, UI) QUEUED behind Q7 hero-rig block. Camera awaits Q8. **Lane A is now Matt-gated (Q7/Q8) for the visible layer.**
- **Lane B (engine) — B1-REBASE ✓ CLOSED:** Phase 1 (rocket, `40e351e`) — v1 S1–S6 retired, ratified catalog-v2 PROXY family + ZONE_CONTROL (26th, GEOMETRY) activated. Phase 2 (gamora, `67fc0a9`) — all four members magnitude-HOLD; A3 PASS (bone→FISSION 0.715 / crypt→SOVEREIGNTY 0.704, different tops); A2/A5/A6 + F-d/F-e/F-f PASS; 51 tests. **The re-based family is the shipping proxy-T4 spine.** THREE named pre-emission prerequisites now gate B4 (all folded into the B4 dispatch): (i) export DDA-lock widen; (ii) A3 fixture-energy designation confirm (non-mana/charge-stack necro — mana collapses A3); (iii) F-f enforcement consumer (FAMILY_MAX_ONE is inert data; rocket owes a live chain-builder consumer).
- **Lane B — B2 ✓ DONE** (`star-lord/v-gear-pass-season-001-1` @ `a916632`): gear_pool=150 (season-000001 catalog, 8 base types → 150 of the 200-writer capacity; honest emit), vocab ruling PATH (a) (11-slot canonical, no gen-side change), proxy blocks byte-identical, gear scaffold-flagged, 77/77. **Cross-lane interlock owed:** drax re-runs `bundle_roundtrip_smoke.gd` on the B2 bundle to close the D4 gear leg (headless — NOT Q7-blocked).
- **Lane B queued (authored/next, sequenced within lane):** B3 six-type flavor completion (star-lord + gandalf curation; names the B2 gear pool + weapon descriptors) · B4 summoner un-gate + demo emission run (**GATED on B1** ✓ + THREE pre-emission prerequisites: export DDA-lock widen, F-f enforcement consumer, necro energy designation) · B5 v2 roster curation (**GATED on B4**).

## Awaiting-Matt blockers

- **Push** (queue #3) — the only hard blocker; everything else is in-flight or seam-owned.
- B4/B5 are gate-HELD on B1/B4 respectively (not Matt-blocked).

## Recent Matt-decisions (this session, where they landed)

- **Two-lane fire order** (relay §4) — EXECUTED: Lane A folded to FIRES; Lane B B1-B5 authored; MASTER §8 board added.
- **Q5 60 FPS min-spec floor** (relay §3.1) — RATIFIED → filed to decisions-log (`787da67`, engine repo).
- **§6.7 serial-content-emission split** — jack-ryan RATIFIED (total-content-supersession-with-pointer-stub); the fourth ledger is canon.
- **Four rulings (relay §2)** — all-six-types demo bundle / zero hand-authored shipped content / proxy-T4 demo-critical / split ratified — carried into the Lane B dispatch scopes.

## Next-session pickup (concrete first action)

1. **B1-REBASE ✓ CLOSED (both phases Disc #11-verified on disk).** Phase 1 `40e351e` / Phase 2 `67fc0a9`; completion records committed meta-repo. Certified: all four members magnitude-HOLD; A3 PASS (different tops); F-d/F-e/F-f + A2/A5/A6 PASS. **Two gamora refutation-conditions routed to B4** (NOT self-authorized, both gate B4 not B1): (a) A3 fixture-energy designation must be non-mana/charge-stack (mana → both-top-FISSION → A3 FAIL); (b) F-f enforcement consumer — FAMILY_MAX_ONE is inert data, rocket owes a live chain-builder consumer before B4 emission. Both folded into the B4 dispatch scope + acceptance.
2. **B2 ✓ DONE (Gate-1 cleared ENDORSE-WITH-FOLDS ×4, executed, Disc #11-verified).** Vocab reconcile ruled PATH (a) — no Matt-escalation needed (11-slot `gear_representative` and 10-slot `gear_slot` are distinct fields, not a conflict). **Next in Lane B: B3 (six-type flavor completion — names the B2 gear pool + weapon descriptors; star-lord + gandalf curation).** B4 stays HELD until the re-based B1's THREE pre-emission prerequisites land (export DDA-lock widen + F-f enforcement consumer + necro energy designation). Phase 3 (CONVERGENCE + DUAL_PROXY) is a LATER dispatch — gandalf Q6/Q7 now RATIFIED (`67fe6c0`, all six exception rows as-drafted) so no longer artifact-blocked; residual = the 2 CONVERGENCE named items (proxy_type→family classifier; a 2-summon-skill demo kit).
   - **Cross-lane interlock (owed now, not Q7-blocked):** drax re-runs `bundle_roundtrip_smoke.gd` against the B2-emitted bundle (gear_pool=150) to close the D4 gear leg of the round-trip. Headless data round-trip — does NOT need the hero rig. Requires the B2 bundle to land in the godot `res://data/` dir (drax's seam handles the copy).
3. **Lane A render layer is Matt-gated:** nothing more fires for drax's visible layer until Q7 (rig retarget) is ruled; Camera B needs Q8. When Q7 lands, drax un-queues D5 VFX / D6 floor authoring + G2 / D8 UI.
4. **Carry the §20d primitive-depth datapoint** as candidate bundle-v2 richness feedback (rocket generation / star-lord emission).
5. **Carry Matt-plate items** (queue #1/#2) to the B4/B5 reports.

## Gate/commit ledger (this session, meta-repo — UNPUSHED)

- `cc0c523` two-lane relay execution (Lane A folds + Lane B B1-B5 authored + MASTER §8)
- `251c03c` Gate-1 folds applied (D5-a/b, D6-1, B1-1/2, B2-1)
- Engine repo: `787da67` Q5-60fps decisions-log entry (jack-ryan)

**Signed:** knight-rider, 2026-07-02 — relay executed end-to-end: authored → Gate-1 → folded → FIRING. Both lanes running; monitor-not-poll.