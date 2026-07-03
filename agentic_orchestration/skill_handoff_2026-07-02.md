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

**Held:** B4 (consumes the proxy family) + B5 (curates it) stay HELD — no longer just "gated on B1," now gated on the RE-BASED B1. B2 (gear, `t4_catalog_v2` Set-#6 lane) is largely family-independent but shares the engine working tree → serialized behind the re-base. **Matt ruling needed:** fire a B1-rebase dispatch (rocket re-base execution classes onto ratified six → gamora re-cert) now, or fold. gandalf's §3 map + §6/§7 leans (ASCENSION+FISSION+INVERSION demo-critical) are the ready inputs.

## §20d headline datapoint (surfaced to Matt, not a blocker)

**54 kits → 19 distinct verb signatures (collapse 2.84); refutation did NOT trip (19 ≥ 6).** Distinct verbs are CHEAP to realize (proven — the realizer is a pure projection), BUT the bundle's emitted primitive variety at the primary-attack layer is SHALLOW (2 geometries, 1 composition_mode, uniform strike). The cheapness is proven; the primitive-depth is the thing to watch for the 400-promise — candidate feedback into rocket generation / star-lord emission for bundle-v2 richness.

## Active workstreams + status

- **Lane A (Godot, drax) — CORES LANDED, render rig-blocked:** D5/D6/D8 logic cores DONE (`300d07b`, 3 tags, verified Disc #11). Summon verb plays end-to-end; camera beat validated CAMERA B; grimoire+glyphs honest. Render/capture layer (VFX, floor authoring, G2, UI) QUEUED behind Q7 hero-rig block. Camera awaits Q8. **Lane A is now Matt-gated (Q7/Q8) for the visible layer.**
- **Lane B (engine) — B1 in progress:** B1 Phase 1 (rocket) ✓ DONE (`17d5f80`) — six strategies + 4 dormant revived; A3 shape verified; R2 clean; 73/73 tests. B1 Phase 2 (gamora — magnitudes + A2/A3-fixtures/A5/A6) **FIRING NOW**. Export exit-gate finding routed → B4 (emitter DDA-lock must widen before proxy emission).
- **Lane B queued (authored, sequenced within lane):** B2 gear-pass (star-lord; feeds D8) · B3 six-type flavor completion (star-lord + gandalf curation) · B4 summoner un-gate + demo emission run (**GATED on B1** + export-fold prerequisite) · B5 v2 roster curation (**GATED on B4**).

## Awaiting-Matt blockers

- **Push** (queue #3) — the only hard blocker; everything else is in-flight or seam-owned.
- B4/B5 are gate-HELD on B1/B4 respectively (not Matt-blocked).

## Recent Matt-decisions (this session, where they landed)

- **Two-lane fire order** (relay §4) — EXECUTED: Lane A folded to FIRES; Lane B B1-B5 authored; MASTER §8 board added.
- **Q5 60 FPS min-spec floor** (relay §3.1) — RATIFIED → filed to decisions-log (`787da67`, engine repo).
- **§6.7 serial-content-emission split** — jack-ryan RATIFIED (total-content-supersession-with-pointer-stub); the fourth ledger is canon.
- **Four rulings (relay §2)** — all-six-types demo bundle / zero hand-authored shipped content / proxy-T4 demo-critical / split ratified — carried into the Lane B dispatch scopes.

## Next-session pickup (concrete first action)

1. **RESOLVE the B1 re-base (see HEADLINE above).** gamora Phase 2 landed but B1 is built against the RETIRED v1 S1–S6 family; the ratified catalog-v2 PROXY family governs (`608c120`). Matt ruling: fire a B1-rebase dispatch (rocket re-base `mechanic_alteration.py:986+` strategy classes onto ratified six → gamora re-cert against them) or fold. Do NOT record B1 closed. Do NOT fire B4/B5 until the re-based B1 lands.
2. **B2 (star-lord gear pass)** is family-independent but shares the engine tree → sequences behind the re-base (Lane B serial). Then B3 (flavor). B4 stays HELD until re-based B1 + the export-fold prerequisite both land.
3. **Lane A render layer is Matt-gated:** nothing more fires for drax's visible layer until Q7 (rig retarget) is ruled; Camera B needs Q8. When Q7 lands, drax un-queues D5 VFX / D6 floor authoring + G2 / D8 UI.
4. **Carry the §20d primitive-depth datapoint** as candidate bundle-v2 richness feedback (rocket generation / star-lord emission).
5. **Carry Matt-plate items** (queue #1/#2) to the B4/B5 reports.

## Gate/commit ledger (this session, meta-repo — UNPUSHED)

- `cc0c523` two-lane relay execution (Lane A folds + Lane B B1-B5 authored + MASTER §8)
- `251c03c` Gate-1 folds applied (D5-a/b, D6-1, B1-1/2, B2-1)
- Engine repo: `787da67` Q5-60fps decisions-log entry (jack-ryan)

**Signed:** knight-rider, 2026-07-02 — relay executed end-to-end: authored → Gate-1 → folded → FIRING. Both lanes running; monitor-not-poll.