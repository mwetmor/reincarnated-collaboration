# Arcade (Machine-Run Mode Factory) — End-to-End Product Pipeline (desired end state, current-state stamped)

> **STATUS:** MATT-FACING · LIVING — born 2026-07-10, FIFTH member of the product-pipeline family
> (Matt: *"may also be worthwhile adding a 5th workflow… Warcraft 3 and Starcraft mini games using
> our kits and synty assets and procedural assembly process"*; authorized same session).
>
> **PURGE-EXEMPT:** Matt-consumption surface — NEVER folded, retired, or purged without Matt's
> explicit ruling. Form-precedent: doc 39 §1 (2026-05-24).
>
> **SCOPE RIDER — POST-LAUNCH:** nothing in this pipeline gates the One-Realm demo or launch. The
> taxonomy's §9.1 endgame fork + game-tracker B6 stay PARKED; business-strategy §9 gates govern all
> exposure. The ONLY present-tense obligations are the four free architecture laws in the
> NOW-obligations box below. The strategy doc's own words govern this doc too: **scope is the
> existential risk** — this pipeline exists so the arcade is buildable LATER because four cheap
> habits held NOW.
>
> **Maintenance law — SAME-COMMIT (Matt condition 2026-07-10: "updated immediately and always"):**
> gandalf owns the doc; the commit that lands stage-changing work UPDATES that stage's stamp
> (**LIVE / PARTIAL / GAP / GATED**) in the SAME commit — the §2.7 FLOW-maintenance rule extended
> (owning agents: gandalf A0 · star-lord A1–A2 · gamora A3 · drax A4/A6 · elrond A5 · Matt A7).
> A build landed without its stamp update is an incomplete commit. Glance **`/minigames`** page
> (6th tab, Matt-ruled 2026-07-10: *"let's make it a 6th tab called minigames"*) renders this doc —
> contract v1.8 §7.6; same §2.7 FLOW parse, zero new parse shapes.

**Siblings:** `pipeline-serial-content-emission.md` · `pipeline-battle-sim.md` · `pipeline-game.md` ·
`pipeline-story.md`. **Composition law (why this is the FIFTH member, not a fork of one):** the
arcade pipeline is the COMPOSITION POINT of the other four — it consumes certified kits (E-chain),
certification machinery + the shared player/AI pool (S-chain), bodies/scenes/band-dressed actors
(G-chain), and certified text register (N-chain), and arranges them into MODES. **Kits are nouns;
modes are sentences** (content-visibility LAW, `../reap-die-rise-game/business-platform-strategy.md`
§3): this pipeline makes sentences, never new nouns. Spec homes:
`../reap-die-rise-game/arcade-minigame-taxonomy-spec.md` (the lattice — 11 templates, 6 laws) ·
`business-platform-strategy.md` (gates, laws, monetization) · `wc3-sc-custom-game-compendium.md`
(REFERENCE lineage: every template's WC3/BW/SC2 ancestor named).

---

## FLOW (end-to-end at a glance — Glance shape, contract § 2.7)

1. **A0 Template lattice** ← A0
2. **A1 Packet authoring** ← A1
3. **A2 Schema validation** ← A2
4. **A3 Range certification** ← A3
5. **A4 Runtime assembly + bots** ← A4
6. **A5 Registry & rotation curation** ← A5
7. **A6 Player arcade surface** ← A6
8. **A7 Creator exposure gates** ← A7

## The visual flow

```
┌──────────────────────────────────────────────────────────────────────────┐
│ A0 · TEMPLATE LATTICE (the pre-implemented mode grammar)                  │
│  11 WC3-lineage templates (5.1 Horde Survival … 5.11 Party wrapper) ·    │
│  6 design laws (packet-not-code · cosmetic+QoL membrane · shared         │
│  player/AI pool · certification) · rung ladder · candidate 5.12          │
│  tug/auto-battle + 5.9 watch flag (Matt ruling pending)                  │
└───────────────────────────────┬──────────────────────────────────────────┘
                                ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ A1 · PACKET AUTHORING (a mode is a packet, not code)                      │
│  three doors, one contract: internal tooling (Rule of Three: CLI →       │
│  crude form → preview → cert-submit) · agent copilot (constrained LLM    │
│  parse → packet ~5–10 s) · creator editor (Stage-4 gate; the World       │
│  Editor path, not the Roblox path)                                       │
└───────────────────────────────┬──────────────────────────────────────────┘
                                ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ A2 · SCHEMA VALIDATION (instant)                                          │
│  versioned + documented packet contract · registry-ID indirection —      │
│  packets reference nouns, never carry assets · lattice-edge asks fail    │
│  gracefully ("not in the vocabulary yet; closest I can do is X")         │
└───────────────────────────────┬──────────────────────────────────────────┘
                                ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ A3 · RANGE CERTIFICATION (gamora — certified by construction)             │
│  sim pre-validates each template's PARAMETER SPACE offline ("wave        │
│  scaling X–Y in-band for composition class Z"); runtime packets CLAMP    │
│  to certified ranges → instant AND Law-6-compliant · fairness-band       │
│  architecture, one level up · cert callable as a service                 │
└───────────────────────────────┬──────────────────────────────────────────┘
                                ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ A4 · RUNTIME ASSEMBLY + BOTS (drax — the 60-second demo lives here)       │
│  template load + registry pulls (kits E8 · scenes/bands G-chain · text   │
│  register N-chain) · shared player/AI pool pilots empty seats — works    │
│  at 11pm with no friends online · 15–30 s in-lattice, 60 s with margin   │
└───────────────────────────────┬──────────────────────────────────────────┘
                                ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ A5 · REGISTRY & ROTATION CURATION (elrond — own the registry)             │
│  every packet (internal · agent-made · community) lives in OUR registry, │
│  in OUR game · assets travel as registry references, never raw files ·   │
│  best community modes curate into the official rotation · the DotA       │
│  lesson from the platform-owner's side                                   │
└───────────────────────────────┬──────────────────────────────────────────┘
                                ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ A6 · PLAYER ARCADE SURFACE (drax — visible novelty)                       │
│  browsable catalog — "the agent is a fast hand over a browsable          │
│  catalog, never the only door" · FREE kit tranches land as new nouns +   │
│  new rotation sentences from ONE emission, announced together · patch    │
│  notes, trailer beats · never paywall your own advantage                 │
└───────────────────────────────┬──────────────────────────────────────────┘
                                ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ A7 · CREATOR EXPOSURE GATES (Matt — nothing auto-advances)                │
│  Stage 4 creator editor (retention healthy AND players asking) · Stage   │
│  4.5 prompt front-end public (a marketing beat) · Stage 5 content        │
│  modding (mature style-cert) · Tier-3 code modding: NEVER               │
└──────────────────────────────────────────────────────────────────────────┘
```

## Stage detail (Consumes / Does / Emits / State)

## A0 · Template lattice — **PARTIAL (spec canonized; zero templates implemented; build PARKED)**
- **Is:** `../reap-die-rise-game/arcade-minigame-taxonomy-spec.md` — 11 templates (5.1–5.11), 6
  design laws, rung ladder (in-run activities → arcade surface), two-tier certification. Lineage
  evidence: `wc3-sc-custom-game-compendium.md` §6 — every template's BW/WC3/SC2 ancestor named
  (5.10 Zone Control + 5.11 Uther Party existed VERBATIM; Custom Hero Line Wars = kit-drafting
  proven by teenagers two decades early).
- **Open:** template **5.12 tug-of-war/auto-battle candidate** (compendium's strongest uncovered
  genre — "Legion TD-shaped and sim-native"; gandalf lean ADMIT) + **5.9 thin-ancestry watch flag**
  (earns its slot with playtest data or yields it to 5.12). Matt ruling at next taxonomy edit.
- **State:** **PARTIAL** — the lattice is SPEC'D; zero templates implemented; build PARKED behind
  taxonomy §9.1 endgame fork (game-tracker B6).

## A1 · Packet authoring — **GAP (Rule of Three governs)**
- **Does:** produces mode-packets against the versioned contract through three doors: (1)
  **internal tooling** — build-as-you-go thin layers (packet-validation CLI → crude local form →
  preview-with-bots → cert-submit), each layer pulled forward only when the manual version has hurt
  three times, zero creator-grade polish before the Stage-4 demand signal; (2) **agent copilot** —
  constrained LLM parse → packet in ~5–10 s ("gentler early waves, brutal bosses" → parameter
  patch — dissolves the JASS learning curve); (3) **creator editor** — Stage-4-gated (A7): template
  picker → kit slicer → parameter forms → one twist.
- **State:** **GAP** — no packet contract drafted yet, deliberately: the Mac team + packet schemas
  already IS the editor wearing a conversational UI; no tool until the manual version hurts ×3.

## A2 · Schema validation — **GAP (its seeds are NOW-obligations #1–#2)**
- **Does:** instant structural validation against the **versioned + documented packet contract**;
  **registry-ID indirection** for every NEW reference authored from here forward (a forward habit,
  not a retrofit on existing references) — packets reference nouns, never carry raw assets (the
  licensing question dissolves permanently); lattice-edge asks fail gracefully ("not in the
  vocabulary yet; closest I can do is X" — parameter fills succeed in seconds, new primitives are
  engine work).
- **State:** **GAP** — the validation surface is unbuilt; its two seeds are free present-tense laws.

## A3 · Range certification — **GAP (architecture named; gamora seam when it fires)**
- **Does:** the sim pre-validates each template's PARAMETER SPACE offline ("wave scaling X–Y
  in-band for composition class Z"); runtime packets clamped to certified ranges are **certified by
  construction** — instant AND Law-6-compliant. Same architecture as gear fairness bands, one level
  up. Certification callable as a service (NOW-obligation #3) keeps this reachable by A1's three
  doors.
- **State:** **GAP** — machinery precedent LIVE on the battle-sim side (gauntlet, bands); the
  parameter-space generalization is a gamora design note owed at arcade-build time, NOT before
  (Discipline #18 timing: extension methodology after baseline empirics, not in the dark).

## A4 · Runtime assembly + bots — **GAP**
- **Consumes:** certified packet (A3) + registry nouns: kits (emission E8) · scenes / actors /
  band-dressed bodies (game G-chain) · certified text register (story N-chain).
- **Does:** template load (~5–15 s) + bot seats from the shared player/AI pool — every mode
  playable solo at 11pm with no friends online. The **60-second describe-a-mode-play-it-with-bots
  demo** is this stage composed with A1's copilot door and A3's clamps: 15–30 s in-lattice, 60 s
  with margin. Moat shape: shallow at runtime BECAUSE deep at build time — uncopyable without the
  substrate; a marketing beat, not a feature war.
- **State:** **GAP** — POST-LAUNCH.

## A5 · Registry & rotation curation — **GAP (its seed is NOW-obligation #2)**
- **Does:** every packet — internal, agent-made, community — lives in **our registry, in our
  game**; assets travel as registry references, never raw files; the best community modes curate
  into the official rotation. The DotA lesson from the platform-owner's side: Blizzard shipped the
  editor and captured none of DotA's value; this architecture captures it by construction.
- **State:** **GAP** — the indirection habit starts NOW at zero cost; the registry product is
  POST-LAUNCH. elrond seam (feed-2 registry snapshot is the machine-truth precedent).

## A6 · Player arcade surface — **GAP**
- **Does:** browsable in-game arcade catalog under the **content-visibility LAW**: prompts arrange
  content into modes, they never unlock content; kits are nouns, modes are sentences, every noun
  visible in the catalog. Each tranche feeds both surfaces from ONE emission — new kits for
  players + new vocabulary for creators, announced together (patch notes, trailer beats).
- **State:** **GAP** — POST-LAUNCH. Monetization-ladder position: **FREE** (the retention engine —
  tranches are nearly free to produce; that is the structural edge; never paywall your own
  advantage).

## A7 · Creator exposure gates — **GATED (Matt; nothing auto-advances)**
- **Is:** business-strategy §9 — **Stage 4** creator editor exposed (arcade retention healthy AND
  players ASKING to make modes) · **Stage 4.5** prompt front-end public (editor proven internally;
  used as a marketing beat) · **Stage 5** tier-2 content modding (active creator scene AND mature
  style-certification pipeline) · **tier-3 code modding NEVER** (arbitrary scripts break
  certification by definition; primitives stay authored — standing architecture law; GUI triggers
  vs. JASS, reborn).
- **State:** **GATED** — these are ruling-gates, not build-gaps; they never open by default.

## NOW-obligations box (the ONLY present-tense work this pipeline levies)

| # | Free architecture law (business-strategy §7) | Where it bites | Status |
|---|---|---|---|
| 1 | **Versioned + documented packet contract** | any mode/packet schema star-lord or drax authors from here on | flagged → jack-ryan "genuinely free" sanity pass |
| 2 | **Registry-ID indirection for NEW references** (forward habit, NOT a retrofit) | every NEW template/kit/scene/packet reference authored from here forward, engine + Godot — existing references are NOT in scope; this law binds only what is written next, which is where it costs zero | flagged → jack-ryan sanity pass |
| 3 | **Certification callable as a service** | gamora's cert entry points (no CLI-only burial) | flagged → jack-ryan sanity pass |
| 4 | **No hardcoded arcade template/kit/scene IDs** — engine **Discipline #40** (no hardcoded defaults in production-output paths) applied to the arcade ID surface; a citation/extension of #40, not a freestanding law | all seams (as #40 already governs) | flagged → jack-ryan sanity pass (folds under #40) |

Precedent: Rimworld and Factorio matured mod ecosystems AFTER earning audiences; the World Editor
shipped inside a finished RTS. These four habits preserve every future option at zero present
cost — they enter engineering-disciplines only after jack-ryan confirms each is genuinely free.

## Gates at a glance

| Stage | Gate | Owner | Home |
|---|---|---|---|
| A0 build | taxonomy §9.1 endgame fork (PARKED) + launch-scope planning | Matt ↔ gandalf | game tracker B6 |
| A1–A6 build | POST-LAUNCH; Rule of Three per tooling layer | KR sequences | business-strategy §6 |
| A7 Stage 4 / 4.5 / 5 | retention + demand signals per §9 table | Matt | business-strategy §9 |

**Signed:** gandalf, 2026-07-10. Blizzard shipped the editor and captured none of DotA's value. We
hold the registry from the first packet — the nouns stay certified, and this is the room where they
learn to make sentences.
