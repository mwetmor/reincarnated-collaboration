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
| D3 | gamora | demo summoner sim-certification (W3-lite) | ask 3 (ratified) | III.1b | **🔥 FIRING** (D2 landed; Gate-1 CLEARED 2026-07-02 — ENDORSE-WITH-CONCERNS, folds A–D applied) |
| D1 | star-lord | one-realm emission hand-join (single Godot-consumable bundle) | §5.1 | II.3 +1 MVP-CRITICAL | **✓ DONE** (`star-lord/v-one-realm-bundle-handjoin-1` @ `20e5e0f`) — schema note DRAFT-pending-drax-handshake; lock-emit-with-D2-decls is a star-lord follow-on after drax signs |
| D4 | drax | Godot bundle loader | §6.1 | game tracker | **🔥 FIRING** (D1 landed; Gate-1 CLEARED — ENDORSE-WITH-CONCERNS, folds 1–4 applied; single drax session w/ D10) |
| D5 | drax | verb realization incl. summon | §6.2 | game tracker | GATED on D4 + D2 decls |
| D6 | drax | three-beat floors (camera ratifies first floor) | §6.3 | game B1/A′1 | GATED on D4; camera beat EARLY |
| D7 | drax | enemy AI baseline + horde-density RENDERING | §6.4 | III.3 LAUNCH (sim) / Godot render | GATED on D5+D6 |
| D8 | drax | grimoire + scouting UI (minimal) | §6.5 | III.8 MVP-CRITICAL | parallel-safe (UI-independent) |
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

---

**Signed:** knight-rider, 2026-07-02. Two engine asks, seven Godot beats, one standing gate — the loop enacted once, playable from a real bundle.
