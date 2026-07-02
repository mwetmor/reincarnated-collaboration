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
| D1 | star-lord | one-realm emission hand-join (single Godot-consumable bundle) | §5.1 | II.3 +1 MVP-CRITICAL | READY — first fire |
| D2 | rocket | hand-authored proxy decls for 2–3 demo summoner kits | §5.2 | III.1b MVP-SPLIT | READY — first fire (concurrent, feeds D1) |
| D3 | gamora | demo summoner sim-certification (W3-lite) | (proposed ask 3) | III.1b "Open Matt ruling" | **HELD — pending Matt ratification** (see §3) |
| D4 | drax | Godot bundle loader | §6.1 | game tracker | GATED on D1 contract |
| D5 | drax | verb realization incl. summon | §6.2 | game tracker | GATED on D4 + D2 decls |
| D6 | drax | three-beat floors (camera ratifies first floor) | §6.3 | game B1/A′1 | GATED on D4; camera beat EARLY |
| D7 | drax | enemy AI baseline + horde-density RENDERING | §6.4 | III.3 LAUNCH (sim) / Godot render | GATED on D5+D6 |
| D8 | drax | grimoire + scouting UI (minimal) | §6.5 | III.8 MVP-CRITICAL | parallel-safe (UI-independent) |
| D9 | drax | king-rig → descent stitch (Binding-Rite-LITE) | §6.6 | game A′2 | GATED on D6 + king-rig (LIVE) |
| D10 | drax | min-spec verification cadence (GTX-1650-class) | §6.7 | standing gate | STANDING — established early, applied to D4–D9 |

## 2. Sequencing rationale + dependency graph

```
WAVE 1 (engine asks — bounded; §5)         WAVE 2 (Godot foundation)
  D1 star-lord bundle  ──contract──┐         D4 drax bundle-loader  ◄── D1
  D2 rocket proxy decls ──feeds──► D1        D10 drax min-spec cadence (standing; est. w/ D4)
  [D3 gamora cert — HELD]                     │
                                              ▼
WAVE 3 (Godot verbs + floors)              WAVE 4 (integration)
  D5 verb realization (incl summon) ◄─ D4+D2   D7 enemy AI + horde ◄─ D5+D6
  D6 three-beat floors (camera EARLY) ◄─ D4    D9 king-rig→descent stitch ◄─ D6
  D8 grimoire/scouting UI (parallel)           D10 min-spec applies to all
```

**Why this order:**
- **D1 is the root.** The entire §6 Godot critical path is un-runnable until a real engine bundle exists. D4's contract handshake is *with star-lord*. So D1 unblocks the program.
- **D2 fires concurrent with D1** and *feeds* it: the summoner kits in the bundle need real `proxies` payloads (D2's output), so rocket emits decls slightly ahead and star-lord's hand-join consumes them. Both are bounded, self-contained engine asks.
- **D4 + D10 open Wave 2.** Bundle-loader proves engine-emitted content plays in Godot (§20d condition under test). Min-spec cadence stands up *now* so GTX-1650-class checks are a build gate from the first Godot commit, not a launch surprise (§6.7).
- **D6 camera-ratification sequences EARLY** (game-tracker B1/A′1): the camera ratifies on the *first* floor, so that beat leads the three-beat authoring rather than trailing it.
- **D8 is parallel-safe** — grimoire/scouting UI consumes the III.8 label→glyph mapping and doesn't block on combat.
- **D7 + D9 are integration** — they need verbs (D5) and floors (D6) to exist first.
- **D10 is a STANDING gate**, not a one-shot: every Godot dispatch (D4–D9) carries a min-spec acceptance checkbox.

**First dispatch to fire: D1 (star-lord one-realm emission hand-join)**, concurrent with **D2 (rocket proxy decls)**. D2's decls are an input to D1's bundle, so rocket emits first-or-concurrent; star-lord hand-joins with real summoner payloads.

## 3. D3 is HELD — the scope-boundary flag for Matt

The ratified denominator (§5.3) scopes **exactly two engine asks** and states "**Nothing else.**" The demo-certification slice (D3) is gandalf-recommended as "one-realm engine ask 3" but the tracker (III.1b) marks it an **"Open Matt ruling ... pending Matt's ruling,"** and it *partially supersedes the W3 PARK's "no proxy build" clause* (ruled 2026-06-30, two days pre-One-Realm-mandate). This is a **scope-amendment beyond the ratified two-ask scope** → requires fresh Matt-authorization per CLAUDE.md.

**D3 is authored and staged (BLOCKED banner) so it can fire the moment Matt rules.** Until then it does not fire. See `2026-07-02-gamora-demo-summoner-cert-HELD.md`.

**The question for Matt:** ratify the demo-certification slice (D3) as a third engine ask, or hold summoner certification to launch-track and let the demo hand-tune summoner feel by playtest (§5.3 posture)? Empirical note: the summoner FIGHT mechanism is BUILT (W1+W2); D3 only calibrates the four scaffold magnitudes + grades at the build-floor — the dodge-ceiling stays Godot-gated regardless.

## 4. Gate discipline (REVIEW_PROCESS)

- Each Pattern-B dispatch clears **Gate-1 critique-pair** before its agent executes: jack-ryan DESIGN-MODE (all — process/cross-seam) + gandalf design-fit (design-track: D5 verb realization, D6 floors register, D8 grimoire-fantasy).
- **Cross-seam contract (Principle 6):** D1⟷D4 is the bundle-schema contract → MIGRATION.md required (star-lord authors the bundle schema; drax consumes). D2→D1 is intra-engine (rocket decl surface already exists on `PlayerClassV2.to_dict()` `proxies`).
- **Wave-entry discipline (§3.10):** a wave is not entered until sub-agents FIRE. This MASTER is authored; D1+D2 fire on Matt's go.

**Gate-1 status (2026-07-02):** first-fire wave cleared jack-ryan DESIGN-MODE Gate-1 — **D2 ENDORSE (fire as-authored); D1 ENDORSE-WITH-CONCERNS**, three contract-hygiene folds applied (a: schema note reframed as mandatory pre-emit artifact per Discipline #1; b: drax handshake gates the schema LOCK, not the round-trip; c: bundle schema emission-path-sourced only, no telemetry-boundary widening). D3-HELD call ENDORSED (ADR-002 tiered approval / Principle 4 — scope-amendment needs fresh Matt-auth). D4–D10 carry Gate-1-before-fire; design-track dispatches (D5 verbs, D6 floors register, D8 grimoire-fantasy) also draw gandalf design-fit as they approach firing.

## 5. In-flight work continues (§9)

This program re-prioritizes **new starts** only. In-flight engine instrument work (perception-asymmetry producer, deferral un-gates) proceeds and does NOT gate the demo. The demo is itself the validation instrument (§8) for the currently-unfalsifiable claims.

---

**Signed:** knight-rider, 2026-07-02. Two engine asks, seven Godot beats, one standing gate — the loop enacted once, playable from a real bundle.
