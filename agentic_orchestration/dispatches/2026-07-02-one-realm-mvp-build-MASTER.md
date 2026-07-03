# MASTER — 2026-07-02 — One Realm MVP build program (§5/§6 → dispatches)

**From:** knight-rider (orchestrator)
**Authority:** Matt-authorized 2026-07-02 — "CONVERT the One Realm MVP scope's asks into dispatches, per `canonical/reap-die-rise-game/one-realm-mvp-scope.md` §5/§6/§9. Sequencing authority is KR's (§9)."
**Denominator:** `canonical/reap-die-rise-game/one-realm-mvp-scope.md` (Matt-ratified 2026-07-02).
**Tracker anchors:** `current-to-end-state-engine.md` II.3 first bullet · III.1b [MVP-SPLIT] · IV.2 MVP-lens blockquote.

---

## 0. What this program is

The One Realm demo is the denominator: a free Steam demo, one ~25–27 min realm-run, ~8–10 hand-curated becomable kits (≥1 summoner mandatory), authored floors, wishlist end-card. §5 pulls **exactly two engine asks** (bounded); §6 is the **drax-heavy Godot critical path** ("this IS the demo"). The §20d parametric-verb condition — *can ~10 kits become 10 distinct playable verbs cheaply* — is THE test this build runs.

**The load-bearing dependency (root of the whole program):** engine-emitted content must be playable in Godot. Hand-building kits Godot-side is FORBIDDEN (the engine is the product; §20d is the condition under test). So the star-lord bundle (D1) ⟷ drax bundle-loader (D4) **contract handshake is the program's spine.** Everything Godot hangs off a real bundle.

## 1. The ten dispatches

| # | Agent | Task | §ref | Tracker | Status |
|---|---|---|---|---|---|
| D2 | rocket | hand-authored proxy decls for 2–3 demo summoner kits | §5.2 | III.1b MVP-SPLIT | **🔥 FIRING** (Matt-fired 2026-07-02; no deps) |
| D3 | gamora | demo summoner sim-certification (W3-lite) | ask 3 (ratified) | III.1b | **✓ DONE** (`gamora/v-proxy-fight-calibration-1` @ `abb010d`) — 4 magnitudes certified-HOLD; 2 melee summoners PASS; gravecaller ranged-nav §20d finding → DEFERRED (see §6) |
| D1 | star-lord | one-realm emission hand-join (single Godot-consumable bundle) | §5.1 | II.3 +1 MVP-CRITICAL | **✓ DONE + LOCKED** (`star-lord/v-one-realm-bundle-LOCKED-2` @ `08e6f24`) — schema LOCKED (drax handshake signed); bundle emitted w/ 2 summoner kits carrying non-empty scaffold-flagged proxies; MIGRATION §v1.83 LOCKED. See §7. |
| D4 | drax | Godot bundle loader | §6.1 | game tracker | **✓ DONE** (`drax/v-godot-bundle-loader-2` @ godot `7e9a57a`) — §20d round-trip PASS against real LOCKED bundle; 54/54 kits resolve non-degenerate primary_attack; 2 summoners' proxies resolve; SCAFFOLD boundary held; zero hand-built kits. See §7 recovery chain. |
| D5 | drax | verb realization incl. summon | §6.2 | game tracker | **✓ CORE DONE** (`drax/v-godot-verb-realization-1` @ godot `300d07b`) — summon verb PLAYS end-to-end (spawn→AI→fight→death→re-summon), mirrors sim §Q1; SCAFFOLD held; allegiance-legibility PASS. **VFX/meshes QUEUED (rig-blocked Q7)** |
| D6 | drax | three-beat floors (camera ratifies first floor) | §6.3 | game B1/A′1 | **◑ CAMERA BEAT DONE** (`drax/v-godot-three-beat-floors-1` @ `300d07b`) — camera beat caught a bad cam on floor 1, validated CAMERA B (**awaits Q8 G3**). **Floor authoring + G2 QUEUED (rig-blocked Q7)** |
| D7 | drax | enemy AI baseline + horde-density RENDERING | §6.4 | III.3 LAUNCH (sim) / Godot render | GATED on D5+D6 (next Lane-A wave; pre-D7 perf spike + density-per-area spec slotted). Note: drax flags a spatial-broadphase need before full-horde on real GTX-1650 (current allegiance targeting is O(n²)) |
| D8 | drax | grimoire + scouting UI (minimal) | §6.5 | III.8 MVP-CRITICAL | **✓ CORE DONE** (`drax/v-godot-grimoire-scouting-ui-1` @ `300d07b`) — numbered pages honest ("N of 400+"); 5-cluster→5-glyph map (#41 respected). **On-screen UI QUEUED (rig-blocked Q7)** |
| D9 | drax | king-rig → descent stitch (Binding-Rite-LITE) | §6.6 | game A′2 | GATED on D6 + king-rig (LIVE) |
| D10 | drax | min-spec verification cadence (GTX-1650-class) | §6.7 | standing gate | **🔥 FIRING** (stood up alongside D4, single drax session; Gate-1 ENDORSE) |

## 2. Sequencing rationale + dependency graph (Matt-ruled fire order, 2026-07-02)

```
ENGINE ASKS (ordered by Matt 2026-07-02)     GODOT (drax; KR-sequenced)
  D2 rocket decls  🔥 FIRE NOW (no deps)       D4 bundle-loader  ◄── D1 contract
        │                                       D10 min-spec cadence (standing; est. w/ D4)
        ▼ (lands)                               │
  D3 gamora calibration  ◄── consumes D2 decls  ▼
        (Gate-1 before build)                 D5 verbs incl summon ◄─ D4+D2
                                              D6 three-beat floors (camera EARLY) ◄─ D4
  D1 star-lord bundle  ◄── emission inspection D8 grimoire/scouting UI (parallel)
        (in-flight; feeds D1 schema note)      ─────────────────────
        │                                       D7 enemy AI + horde ◄─ D5+D6
        ▼ (unblocks this window)                  ▲ density-per-area spec + min-spec
      unblocks D4                                 │ PERF SPIKE ahead of/with D7 (Matt)
                                              D9 king-rig→descent stitch ◄─ D6
```

**Matt's ruled fire order (2026-07-02):**
1. **D2 fires NOW** — no dependencies; the fastest real content in the program.
2. **D3 after D2 lands** — calibration wants real decls as fixtures; D2's hand-authored decls beat synthetics and arrive fast. (Gate-1 before build — it's a SIM wave.)
3. **D1 after the emission inspection lands** — the inspection (in-flight) feeds D1's mandatory schema note, which the Gate-1 fold made a hard pre-emit artifact. Inspection is running; D1 likely unblocks within this working window.
4. **D4–D10 KR-sequenced** — with the **density-per-area spec + min-spec perf spike slotted ahead of/with D7** (Matt directive): de-risk 50+ enemies at min-spec BEFORE committing D7's full AI+horde build (folded into D7 + D10 below).

**Why the Godot order holds:** D1's bundle is still the root of the Godot path (D4's handshake is with star-lord); once D1 unblocks, D4+D10 open the Godot foundation, D5/D6/D8 build verbs+floors (camera ratifies on floor 1 — EARLY), and D7/D9 integrate. D10 is a STANDING gate on every Godot dispatch (D4–D9), and its first real application is the pre-D7 perf spike.

**First dispatch fired: D2 (rocket proxy decls)** — Matt-fired 2026-07-02, running in background.

## 3. D3 — RATIFIED (Matt 2026-07-02)

The demo-certification slice was authored HELD (scope-amendment beyond the ratified two-ask scope — §5.3 "Nothing else"). **Matt ratified it 2026-07-02** as a third engine ask, sequenced **after D2 lands** (calibration consumes D2's real decls as fixtures — better than synthetics, arrive fast). The HELD banner on the D3 dispatch is discharged. **Gate-1 before build** (SIM wave). Scope unchanged: calibrate the four scaffold magnitudes + grade at the build-floor; the dodge-ceiling stays Godot-gated per the W3 PARK. Tag resolved to `gamora/v-proxy-fight-calibration-1` (avoids the W2-tag collision). See `2026-07-02-gamora-demo-summoner-cert.md`.

## 4. Gate discipline (REVIEW_PROCESS)

- Each Pattern-B dispatch clears **Gate-1 critique-pair** before its agent executes: jack-ryan DESIGN-MODE (all — process/cross-seam) + gandalf design-fit (design-track: D5 verb realization, D6 floors register, D8 grimoire-fantasy).
- **Cross-seam contract (Principle 6):** D1⟷D4 is the bundle-schema contract → MIGRATION.md required (star-lord authors the bundle schema; drax consumes). D2→D1 is intra-engine (rocket decl surface already exists on `PlayerClassV2.to_dict()` `proxies`).
- **Wave-entry discipline (§3.10):** a wave is not entered until sub-agents FIRE. This MASTER is authored; D1+D2 fire on Matt's go.

**Gate-1 status (2026-07-02):** first-fire wave cleared jack-ryan DESIGN-MODE Gate-1 — **D2 ENDORSE (fire as-authored); D1 ENDORSE-WITH-CONCERNS**, three contract-hygiene folds applied (a: schema note reframed as mandatory pre-emit artifact per Discipline #1; b: drax handshake gates the schema LOCK, not the round-trip; c: bundle schema emission-path-sourced only, no telemetry-boundary widening). D3-HELD call ENDORSED (ADR-002 tiered approval / Principle 4 — scope-amendment needs fresh Matt-auth); **Matt then ratified D3, which cleared jack-ryan Gate-1 2026-07-02 — ENDORSE-WITH-CONCERNS, four hygiene folds applied (A: `src/reincarnated/`-relative path note; B: #24 isolation phrasing — leverage-primary ≠ sweep-exclusive; C: rocket un-scaffold apply named as a KR follow-on micro-dispatch with Gate-2; D: bespoke-fixture need → scope-amendment escalation, not self-authorize). None block build; D3 FIRING.** D4–D10 carry Gate-1-before-fire; design-track dispatches (D5 verbs, D6 floors register, D8 grimoire-fantasy) also draw gandalf design-fit as they approach firing.

## 5. In-flight work continues (§9)

This program re-prioritizes **new starts** only. In-flight engine instrument work (perception-asymmetry producer, deferral un-gates) proceeds and does NOT gate the demo. The demo is itself the validation instrument (§8) for the currently-unfalsifiable claims.

## 6. D3 disposition — gravecaller DEFERRED, ranged-nav §20d finding logged (KR 2026-07-02)

D3 landed a **certified-HOLD** on the four proxy fight-magnitudes and graded the two MELEE demo summoners (`demo_bone_acolyte`, `demo_crypt_lieutenant`) survive-and-kill PASS — the §3 summoner mandate (floor + ideal) is met. The FLEX third kit `demo_gravecaller` (ranged caster-summoner) **could not be certified** on a **ranged-proxy navigation gap, not a magnitude** (archer parks 38.9 m from a boss it hits at 10 m).

**Critique-pair convergence (both consulted):**
- **gandalf (design):** melee raise is the *establishing* necromancer verb (genre convention); ranged summon is a second-tier reveal, NOT demo-load-bearing. Defer-and-log is the honest §20d disposition; count-masking is "a lie the demo exists specifically to not tell" (§8 + #40).
- **jack-ryan (process):** deferring the flex kit is a **clean KR orchestration call, not a scope-amendment** (§3 met). Nav gap → launch tracker III.1b/§20d as a narrowing of the W2 "complete" claim; option (b) W2 nav amendment is launch-scope. Count-edit mask violates #11 + #1 + Principle 4/§8. The rocket un-scaffold is a no-op-magnitude confirm (lightweight INFO, not a full Gate-2).

**Enacted (KR authority; both stewards concurred):** gravecaller DEFERRED from the demo roster; ranged-ally boss-focus nav amendment (option b) logged on `current-to-end-state-engine.md` III.1b as a launch-track §20d residual. **Surfaced to Matt as awareness** (a real §20d datapoint — melee-summon parametrizes cheaply, ranged-summon does not) with the single product override available: keep gravecaller as a knowingly-count-masked demo shim (NOT recommended) vs. defer (enacted).

**Follow-on queued:** rocket un-scaffold no-op-confirm (fold C) + gandalf's cheap content-differentiation check (the two melee summoners must read distinctly on-screen — horde vs. bruiser).

## 7. D1→D4 lock-emit recovery chain (KR 2026-07-02) — the Godot spine closed

The bundle-schema contract (D1⟷D4, the program's spine) closed through a five-link recovery after the first lock-emit surfaced a skipped sequencing decision. Discipline #11 (empirical inspection over sub-agent report) caught it at every seam.

**The catch:** the first star-lord lock-emit (`LOCKED-1`, `5b92c68`) hit a stream-idle timeout mid-finish — the doc was flipped to LOCKED + claimed "emitted," but the JSON was absent and MIGRATION still read DRAFT. A fresh star-lord finished the emit + fixed 3 real pre-existing bugs (engine-root path off-by-one; two faction-JSON unwrap bugs). The emitted bundle then validated clean **but carried ZERO non-empty proxies** — the D2 summoner spec-labels (`demo_bone_acolyte`/`demo_crypt_lieutenant`) were never mapped to real emitted kit IDs. drax's §20d WAIT-guard (fold-1) correctly refused to close on an empty-proxies bundle rather than paper over it.

**Root cause (skipped decision, not a bug):** D2 authored the summon *verb* proxies with spec-labels; D3 certified the proxies; D1 emitted 54 real `S1_endgame_bc_...` kits. Nobody designated WHICH two kits become the demo's summoners — a design-curation call the dispatch chain never assigned.

**The recovery chain (each link verified by KR before the next fired):**
1. **gandalf** (design designation, in-scope curation): chose `...int_none_s2` (*Shadow Warden*) = bone-acolyte [clean attach — the 1-of-54 kit already flavored necromancer] + `...int_none_s1` (*Tidewarden*) = crypt-lieutenant [attach + restyle owed]. Legibility PASS (horde vs bruiser lives on the proxies). **§20d honest datapoint:** the emitted palette has ZERO death element (earth 33/fire 12/physical 9) — mechanism-attach is free, theme-attach is a per-kit flavor tax when the palette doesn't natively cover the theme. Recorded as a post-demo engine open question (finding `1937ce4`); does NOT block the demo.
2. **rocket** (bounded restyle): Tidewarden→*Crypt-Lieutenant of the Grounded Reach* (name+title+flavor; water→grave imagery; mechanics untouched). Source: `reincarnated-loadout/data/cycle-14-wave-5-season-001/classes/`. `rocket/v-demo-crypt-lieutenant-restyle-1` @ loadout `4d5def2`. Element rotation PARKED pending drax color-key answer.
3. **star-lord** (re-emit): remapped proxies to gandalf's real kit IDs (gravecaller excluded), picked up the restyle. 2 kits non-empty scaffold-flagged proxies; validate PASS with `enforce_nonempty_proxies=True`. `star-lord/v-one-realm-bundle-LOCKED-2` @ `08e6f24`.
4. **drax** (§20d round-trip close): ROUND-TRIP PASS on real content; 54/54 kits resolve non-degenerate primary_attack; 2 summoners' proxies resolve; SCAFFOLD boundary held; zero hand-built. **Color-key answer: loader keys off `kit.dominant_element` (earth) → rocket's parked water→dark rotation NOT owed.** `drax/v-godot-bundle-loader-2` @ godot `7e9a57a`.

**Two residuals routed (neither a D4 blocker):**
- `gear_pool=0` (source season has no `gear_instances` table) — needs a gear-source decision → **Matt** (`canonical/matt_decision_needed/`-adjacent). Loader handles empty gear gracefully.
- 11-slot `gear_representative` gen-vocab divergence (`main_weapon`~=`main_hand` etc.) — drax consumes non-fatally (deduped WARN) → folded into the gear-source resolution (star-lord reconciles vocab when gear content lands; academic while `gear_pool=0`).

**Parked follow-on DISMISSED:** rocket's water→dark element rotation — the color-key answer resolved it as not-owed.

---

**Signed:** knight-rider, 2026-07-02. Two engine asks, seven Godot beats, one standing gate — the loop enacted once, playable from a real bundle. **The Godot spine (D1⟷D4) is closed: §20d demonstrated on real engine-emitted content, zero hand-built kits.**

---

## 8. TWO-LANE fire order (KR relay execution 2026-07-02) — bundle-v2 wave opened

Per Matt's ratified relay (`gandalf/notes/2026-07-02-kr-relay-two-lane-fire-order.md`): ONE KR session, TWO parallel lanes, this MASTER continues. **Lane A** (Godot, drax repo) fires now against bundle-v1 (the development bridge). **Lane B** (engine bundle-v2, engine repo) authored now; serial within lane (same-repo → one engine agent at a time, concurrent with drax's separate Godot repo). bundle-v2 is the SHIPPING roster source — Godot builds *capability* against v1; v2 swaps *content* through the D4-proven loader (no Godot rework).

**Lane B — engine bundle-v2 wave:**

| # | Dispatch file | Owner | Gate / dep | Status |
|---|---|---|---|---|
| B1 | `2026-07-02-rocket-gamora-proxy-t4-suite.md` | rocket (strategies) + gamora (eval+magnitudes) | gandalf spec **REVISED `608c120`** (v1 spec `c764f40` retired mid-flight) | **⛔ BLOCKED — REBASE (both phases built against RETIRED v1 family).** Phase 1 (`rocket/v-proxy-t4-suite-strategies-1` @ `17d5f80`, 21:55) + Phase 2 (`gamora/v-proxy-t4-suite-eval-1` @ `02d7cd5`, 22:07) executed the drafted **v1 S1–S6** register (ProxyDamageAmplification/Bulwark/Legion/Surge/DeathConversion/Spawn). At 22:04 gandalf's Matt-prior-art-catch revision retired v1 and ratified the **catalog-v2 PROXY family** (ASCENSION/SOVEREIGNTY/FISSION/INVERSION/CONVERGENCE/DUAL_PROXY — already in `t4_catalog_v2.py:53-58` w/ 7 gen-side consumers). **Execution-layer strategy classes (`mechanic_alteration.py:986+`) must re-base onto the ratified six; A3 (LEGION/BULWARK) is a valid-but-wrong-family PASS.** Surfaced to Matt. |
| B2 | `2026-07-02-star-lord-gear-pass-season-001.md` | star-lord | Gate-1 (cross-seam schema); feeds D8 | **AUTHORED** — fires after B1 in the star-lord window (or concurrent-repo scheduling) |
| B3 | `2026-07-02-star-lord-six-type-flavor-completion.md` | star-lord + gandalf curation | Gate-1; D7 AI-tell line (curate) | **AUTHORED** — after B2 (star-lord session) |
| B4 | `2026-07-02-rocket-star-lord-summoner-ungate-emission-run.md` | rocket (un-gate) + star-lord (run) | **GATED on B1**; run-registry schema → Gate-1 → Matt | **AUTHORED — HELD until B1 lands** |
| B5 | `2026-07-02-gandalf-v2-roster-curation.md` | gandalf | **GATED on B4** | **AUTHORED — HELD until B4 lands** |

**Cross-lane interlock:** B4 lands → drax content-swaps v2 + re-runs `bundle_roundtrip_smoke.gd` (the §20d proof repeats on shipping content).

**B1 Phase-1 findings routed (KR 2026-07-02):**
- **Export exit-gate (B1-1 fold answer = YES) → folded into B4 as a star-lord PRE-EMISSION prerequisite.** The emitter `cycle14_wave5_emitter.py` hard-locks `primary_t4` to DDA (`_PRIMARY_T4_REQUIRED` :698; `PRIMARY_T4` :388) — a proxy-family `primary_t4` raises ValueError. star-lord widens the validator + emit shape before B4 emits any proxy kit. Verified on disk (Disc #11). rocket documented in generation MIGRATION; star-lord authors the export change.
- **NAMED residual (no silent re-defer): MechanicReplacement replacement CATALOG** is un-authored CONTENT (not a sim gate) — the strategy is ALIVE + selectable with a conservative axis_match + `_named_residual` marker; the catalog rides gamora Phase-2 audit + a later content pass. Carried; not a B1 blocker.
- **Five dormant `sim_prerequisite` → all None** (revived cleanly — the v1.1 labels predated the spatial sim, as gandalf's spec §6 anticipated). **S5 descope valve NOT taken** — all six family members stand (S5's on-death trigger-hook is a small named residual, not a wave cut).

**Same-repo serialization note:** Lane B is all engine-repo (rocket/gamora/star-lord) → serial (one engine agent at a time to avoid working-tree collision). Lane A (drax, Godot repo) runs concurrent with the active Lane-B agent. Lane-B lead = B1-rocket (gate open + critical path).

**Matt-plate items carried forward (relay §5):**
- **Ranged-proxy nav fork** — fix nav (Lane B) vs. exclude ranged summoners from v2 curation (gandalf lean: exclude; nav fix post-demo). Does NOT gate B4 (run emits; B5 curation chooses). Surfaces for Matt's ruling at B5.
- **Run-registry schema** — star-lord proposes with B4 → jack-ryan Gate-1 → Matt ratifies.

**gandalf owed artifacts (relay §6):** proxy-T4 suite spec ✓ DONE (`c764f40`, gated B1 — now open) · density-per-area spec (feeds D7, owed when D6 approaches D7) · Gate-1 design-fit on D5/D6/D8 as they fire.

**Lane A landed (KR 2026-07-02) — logic cores in, render layer rig-blocked:**

drax executed D5/D6/D8 (+ D10) against bundle-v1, landing the headless-verified LOGIC CORES (`300d07b`, three tags, verified on disk Disc #11). The render/capture layer (VFX, floor authoring, on-screen UI, G2 CV) is QUEUED behind the **2026-06-20 hero-rig retarget block → surfaced as Matt decision Q7** (the single biggest Godot unblock). Camera B awaits **Q8 G3**.

- **§20d cost datapoint (THE headline validation, §8):** **54 kits → 19 distinct verb signatures (collapse 2.84); refutation did NOT trip (19 ≥ 6 floor).** Honest read: distinctness is carried by primitive combinatorics (element×range×shape), NOT skill-level variety — **distinct verbs are CHEAP to REALIZE (the realizer is a pure projection; marginal cost = one table row per novel primitive tuple), but the bundle's emitted primitive variety at the PRIMARY-ATTACK layer is SHALLOW** (2 geometries, 1 composition_mode `single` despite `chain_mage` tags, uniform `strike` intent across all 54). The cheapness is proven; **the primitive-variety depth is the thing to watch for the 400-promise** — a candidate feedback into generation (rocket) / emission (star-lord) for bundle-v2 richness. Surfaced to Matt as a datapoint, not a blocker.
- **gamora feedback routed (#40 — drax fed back, did NOT re-tune Godot-side):** both summoners carry `proxy_max_active=1 SCAFFOLD`, so the "streaming horde" MAGNITUDE read is blocked at loaded values (can't see a horde at cap 1). The horde-vs-bruiser *difference* reads (geometry/cadence); the horde *magnitude* needs the cap raised. **This is exactly what S3 ProxyLegion (B1) delivers** (+1/+2 max_active + count floor) — carried into gamora Phase-2 review + the B4 emission: confirm the emitted horde-caller draws S3 and reads as a horde on bundle-v2. Not a bundle-v1 bug (v1 is the pre-T4 bridge).
- **D10 min-spec:** verb+summon density PASS the proxy budget on the Mac (124 entities = 0.567ms; 218-peak = 1.43ms). Absolute-frame-floor cert stays the `matt_to_do/` T2 hardware item.

**Signed (§8):** knight-rider, 2026-07-02 — two-lane relay executed end-to-end. Lane A logic cores landed (render layer → Q7); Lane B B1 Phase-1 done, Phase-2 (gamora) firing. §20d: distinct-verbs-are-cheap PROVEN; primitive-depth flagged to watch.
