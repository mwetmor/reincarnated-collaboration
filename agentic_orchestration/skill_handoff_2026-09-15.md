# Session hand-off — 2026-09-15 (gandalf, RUN-CONDUCTOR Run C-3 → VFX session next)

> **STATUS:** CURRENT — the latest hand-off (`CLAUDE.md` → "Latest handoff context"). Written at Matt's request (R-C3-123) to close this session and open the **VFX session** in fresh context. Read this, then `canonical/00-ground-state.md`, then the scene-builder canon. Everything below cites its ledger id in `astra_test_01/burst/runs/C-3/ledger.json`.

## 1. What is CANON (done, Matt-confirmed, pushed)

| Item | Where | State |
|---|---|---|
| **Painted-2D scene-builder workflow** — THE scene workflow; 3D scenes + Synty crossed off | `canonical/reap-die-rise-game/painted-2d-pipeline/scene-builder-workflow.md` v1.0 | Matt R-C3-102 → precondition confirmed R-C3-119 ("shadow layer removed meets expectations and is now canon"); jack-ryan Gate-1 BLOCK closed |
| Roles + models, exactly (Matt's note) | same doc § 2 | Astra = Codex `astra-burst` / `gpt-6-astra` / HIGH; Grok = Grok Build 1.0.30 `image_to_video`; step-down goals recorded (Astra → "Sol"; away from Grok video) |
| Decisions-log entry | `reincarnated-engine/design/decisions/decisions-log.md` (`20e778a8`, pushed on Matt's word) | ratified by jack-ryan; SUPERSEDED note on the 2026-05-15 pixel-art lock |
| Game tracker delta | `canonical/current-to-end-state/current-to-end-state-game.md` SESSION-DELTA 2026-09-15 | 3D/Synty crossed off; playtest live; canon confirmed |
| Style-register scene-scope pointer | `canonical/reap-die-rise-story/style-register.md` (top) | scenes: 3D register retired; character/gear scope OPEN |
| **Mobile playtest** | https://reincarnated-loadout.vercel.app/playtest (loadout `fd1e9ab`) | shadow-free scene; iPhone "played exceptionally well" (R-C3-119); now serving the six-kit VFX build web6 (M-C3-web-bakeoff); repeatable via `reincarnated-godot/web/build_playtest.sh` |
| Lane tooling T3g…T3v | `astra_test_01/burst/SPEC.md` § 7 lap 2; freeze `900c02e77ab8`; `00-system.md` § 7 SYNC 10/10 | T3s oracle measurer, T3t effect-kit builder, T3u tint ramp + phase_scale, T3v tinted particles + element_class — all accepted, tests green outside the sandbox (R-C3-104/111/122) |
| Scene-style references | scene-builder doc § 5; plan note | Diablo 2 (scene), **Bastion** (painted-scene pole), Secret of Evermore (feel), **Earthbound = THEME ONLY, never style** (R-C3-113/114/115) |

## 2. What is NOT canon (notes, research, open) — and what the VFX session must not mistake for canon

| Item | Where | State |
|---|---|---|
| VFX style card v0 → v0.1 (nostalgia vector) → v0.2 (measured corrections) | `agentic_orchestration/gandalf/notes/2026-09-14-vfx-style-card-v0.md` | **hypothesis under test**, not canon. v0.2 rules that measurement supports: no white cores (white only as the 0.1 s flash layer), halo + floor light as the default separation (dark duplicate demoted), burst extent 3–6 BH, shape sprites on their own pixel grid, no hue-contrast rule |
| VFX oracle research (Hades numbers) + style atlas (72 samples: Chronicon / Children of Morta / Slormancer added) | `agentic_orchestration/legolas/research/2026-09-14-vfx-oracles/`, `…/2026-09-14-vfx-style-atlas/`, `…/2026-09-15-chronicon-com-slormancer-vfx/`; samples ONLY at `~/Games/vendor/vfx-atlas/` (study-only, never an image-model reference) | filed |
| **Hybrid oracle** (Hades timing bands + CoM/Slormancer legibility bands) | fork R-C3-118 | **UNRULED — deferred by Matt to the VFX session, after the size step** (R-C3-120/123) |
| Video-generation alternatives (20 models priced; $20 six-still bake-off; step-down routes R1–R4) | `…/2026-09-15-video-generation-alternatives/findings.md` | filed; **spend UNRULED** (needs fal.ai + Gemini keys) |
| 3D character/gear mannequin route — retired or kept as motion source? | `canonical/matt_decision_needed/2026-09-15-does-the-3d-retirement-cover-the-character-mannequin-route.md` | **OPEN** (recommendation: retire as asset route, keep a grey mannequin as motion source) — gates the Synty/3D reconciliation sweep |
| Ground shadows | scene-builder doc § 4.1; plan note § OPEN | OPEN research item (Astra paints shadows in; grey-room shadow layer pre-paint + runtime light) |
| Grok video model id; "Sol" model id | scene-builder doc § 2 | OPEN |
| Reconciliation sweep of Synty/3D text (style-register body, tracker A4/B1/B2/B4/C, ensemble spec, pipeline-game, engine specs); scene-reference fold into style-register | listed in scene-builder doc § 1 / § 5 | OWED (in place, never amputate) |

## 3. The six-kit VFX breadth test — what it proved and what it did not (R-C3-123)

**Proved (tooling + register):** greyscale painted-pixel sheet from Astra → cut → tinted kit → Godot picker → public web build works end to end, six times, with measurements per kit (`runs/C-3/artifacts/CS-vfx-*-kit-in/impact_body_measure.json`). Register landed on the sheets that came off true black (Frozen Orb v2 re-drive, Lightning, Zeus): hard edges, 4 bands, no haze.

**Did not prove (Matt):** skill fidelity. **All six are variants of one projectile grammar** — the builder knows only cast → bolt → impact → residual. Frozen Orb (orbiting orb emitting bolts), Blackwater Cocktail (thrown arc → burning pool), Poisonous Concoction (thrown flask → pool), Lightning Blast (instant chain), Zeus (chain that jumps), Healing Hands (self aura) are not that grammar. **No targets or targeting exist** — impacts only happen against the cow. **Effects are likely too small** vertically and horizontally across the screen.

**Findings to carry (ledger notes 2026-09-15):** fire / holy / poison subjects come back on **grey haze** from the image model even under a hard black-void rule (signed-haze cut `runs/C-3/conductor_scripts/cut_signed2.py` recovers light shapes); a **dark-bodied projectile** (glass flask) cannot live in a greyscale tinted-light sheet — it needs its own coloured object sprite; **particles must be tinted at build** (T3v) or they render white; the **first cast in a fresh scene** never registers its impact (warm-up quirk, T3w candidate); the **0.1 s flash layer** at 2× impact scale is a large white disc (alpha knob).

## 4. VFX session — basic concept (to be elicited and chartered in fresh context; NOT a run yet)

Order matters; each step gates the next.

1. **Placeholder monster pack** (static, non-animated dummies). Astra GENERATE on green with the size chart + Keeper scale figures (the dress-then-isolate method, scene-builder § 3 step 6): 6–8 dummies spanning the size classes (rat / hound / humanoid / brute / large) in the H1 register; catalogued as reusable assets; placed via `props.json` with `collide` + a `target` tag; a **targeting rule** in the exporter's keeper (nearest dummy in facing cone, or cast-at-cursor/tap) — a T3w-class TOOLING row.
2. **Size-and-timing estimation by video, before any sheet.** One short clip per skill (six) showing the *source-material* skill shape at screen scale on the cliffside — route options: (a) Grok/i2v from a painted still of the Keeper casting (what we know works), (b) a hand-authored Godot mock (scaled rectangles/ellipses with timing) that costs nothing and is measurable by the oracle, (c) atlas reference clips at our body-height. Output per skill: peak extent (BH), travel speed, phase timings → the per-skill spec the sheets are drawn to. **The hybrid-oracle ruling is taken here**, against these clips.
3. **Skill grammars in the builder** (T3x): beyond the bolt — orbit-emitter (Frozen Orb), thrown-arc + ground field (BWC, PConc), instant chain with jump (Lightning Blast, Zeus), self-aura (Healing Hands). Each grammar = a scene template the kit.json selects (`grammar` field next to `element_class`).
4. **Then the sheets**, one skill at a time, drawn to the size spec; measured; into the picker; web redeploy per batch (`build_playtest.sh`).
5. Open forks to carry into the charter: hybrid oracle (recommend adopt after step 2); video-generation bake-off spend ($20; recommend approve when the character matrix resumes, not for VFX); mannequin route (recommend retire-as-asset / keep-as-motion-source).

## 5. Host + lane facts the next session needs

- Mac mini 8 GB; kernel panic 2026-09-14 from parallel research forks → research sub-agents serial, ≤ 1.5 GB, one decode at a time; watchdog `~/Games/vendor/vfx-atlas/_memwatch.sh`. Scratchpad is wiped by reboots; conductor glue lives in `runs/C-3/conductor_scripts/` (re-seed from there).
- Bursts: `scratchpad/wave.sh <logname> <id:TYPE>…` (log name, not path); TOOLING serial + no conductor writes under `astra_test_01/burst/` while one runs; PACK bursts run concurrently fine; readiness = `out/receipt.json` exists (never `pgrep` on the burst name — it matches your own shell).
- Godot 4.6.3 at `/Applications/Godot.app/Contents/MacOS/Godot`; headless proofs run outside the Codex sandbox; screenshots need `--rendering-method gl_compatibility` without `--headless`.
- Push posture: collaboration repo pushes as work lands (C-3); engine pushed on Matt's word (`20e778a8`); loadout push covered by Matt's playtest ask; godot commits local only.
- Desktop review folders: `~/Desktop/Astra Burst Review - 2026-09-13/` … 82 = v15 (canon scene), 83 = v18 (six-kit bake-off).
- Public web build license rule: only self-authored kits; drax's check now matches exact library names.

— gandalf, 2026-09-15 (R-C3-123)
