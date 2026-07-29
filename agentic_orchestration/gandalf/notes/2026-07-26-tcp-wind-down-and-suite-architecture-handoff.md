# TCP wind-down + hand-off — 2026-07-26

**Author:** gandalf (`RUN-CONDUCTOR`) · **For:** the next session's cold start
**Next session's job (Matt, verbatim):** *"begin next session by architecting the suite of planned
tests to determine the process and tools needed for the remaining godot game generation process,
including characters, monsters, VFX, 'beautiful corner' room, procedurally generated maps,
procedurally generated 'beautiful corners', biomes, lighting, complete UI (both in-game and menu
selection), etc."*

**Program charter (governing doc):** `agentic_orchestration/gandalf/notes/2026-07-24-tool-capability-program-charter.md`
— **exceeds the Read token limit; grep or read by offset.** Laws §3, lap table ~line 336, ledger rows
`| **TCP-NN** | … |` ending at **TCP-55** (~line 668). Standing program intent (Matt): *breadth-then-depth
until we find the end of the capability of each tool; a ceiling is a PASS.*

---

## §0 — Cold-start protocol for the architecture session

1. Charter-freshness gate (OP §1.0) — role file + OP §2 + `desirable-run-pattern.md` from disk if compacted.
2. This document, in full. It supersedes nothing; it indexes everything.
3. Charter lap table (~line 336) + ledger rows TCP-51/43/53/54/55 for the load-bearing evidence.
4. `agentic_orchestration/legolas/notes/2026-07-26-plugin-provisioning-menu.md` — the 45-row menu §1 table + §1.1.
5. Only as needed: the drax reports indexed in §7.

The session's first move is **§5 (the decision queue)** — every planned cell is gated on rulings that
are one message from Matt away. The session's substance is **§6 (the suite grid)**.

---

## §1 — What closed this session

### L8 UI lap — CLOSED. Five arms, all method H, full dark-fantasy HUD arrived.

- **Arm 3b (TCP-53):** glass health-drain + six-candle socket VFX. **Matt ratified the candles
  verbatim** (*"now that I've seen the candle VFX, I really like it!!"*). Component-family cost law
  confirmed additive-weak as pre-registered. The glass sprite is a **thickness map** (alpha 0.364→0.525
  toward the rim), reversing arm 3's rejection. UI-scale VFX sit **below the ms instrument's floor**
  (count 64× / area 256× sweeps never cleared 0.03 ms on a 6.34 ms frame).
- **Arm 3c v1 → stopped (L-R's first deliberate use):** my dispatch framed Matt's hotbar ruling as a
  *deletion*; his mid-flight second ruling (*"the darker metallic grey design behind the boxes. We
  really do need one of them"*) named the failure mode in advance. Stopped at minute 31 (not the
  "~6 minutes" I reported — **L-Q clock corollary born**: a conductor may confirm a timestamp, never
  infer a duration not measured from both ends). The forbidden zero-backing stills were **already on
  disk** one minute before the stop (TCP-54 ①).
- **Arm 3c-R (TCP-54): PASS.** The backing was never missing — **present but tinted to a shadow**
  (Y 0.054 vs Matt's exemplars 0.144/0.156). Fork resolved **CANDLES** on structure (batwings' globes
  carry no candles; choosing wings = dropping ratified work); wings built anyway behind `--tray=wings`.
  Assembly ink −32.1%; backing ratio B1 0.912 → **1.020**, on the exemplars' own 1.021/1.014.
  **Zero-backing measured BETTER on every ratio in the cell — only Matt's advance prohibition rejected
  it.** Standing (TCP-54 ⑩): *a conductor may not put a thumb on the scale; an owner may take an
  outcome off the table.*
- **L8's tool verdict, honestly:** it was **never a bake-off** — all five arms ran method H (arm 1's
  R-14 measured the wire out: 1.19 s/cycle, ~0.2% saving; W-PRO parked under L-J throughout). The
  tool axis competes over only ~26% of a UI lap's cost. Drift acknowledged as mine; the axis gets its
  genuine shot where the difference is **capability**, not speed (→ §2).

### The program's largest structural finding, now on its third confirmation

**Build cost is a MINORITY of lap cost** (arm 3c: build 26% · everything else 74% · instrument alone
28%; same shape in 3b and 3). The component-family law governs BUILD only. **For serial content
emission the dominant cost is the instrument that proves the content right — not the content.**
Every §6 architecture decision should be made with this in front of it: **shared instruments, built
once in prep cells, amortized across arms.**

### Laws born/amended this session

- **L-R** — a dispatch is delivered once; an amendment authored after launch does not exist; a
  changed ruling is a new cell, never an edited file. (Twice-confirmed; the runtime advertises a
  SendMessage channel to running cells that does not exist.)
- **L-Q clock corollary** — timestamps may be confirmed; durations must be measured from both ends.
- **TCP-54 ⑩ standing** — owner-prohibition ≠ conductor-steer; stop calling both "constraint."
- **TCP-55 ⑧ standing** — **provision-first**: freeze the full plugin environment before cell 1,
  pin versions, attribute by declared surface; non-use of an installed helper is itself a finding.

---

## §2 — The two bake-offs, designed and ratification-ready

Full design in this session's transcript; the shape is stable and Matt has seen it. Both follow the
desirable-run pattern; both are **sequential under L-J** (one wire live at a time); both are judged
**blind** (strips labelled A/B/C, tool identity revealed after Matt's read — attribution becomes part
of the verdict, permanently fixing L8's "which tool built this?" gap).

### L7 VFX bake-off — H · W-PRO · W-MUR × {CAST, AURA, AMBIENT}

| Cell | Content |
|---|---|
| **V-PREP** (drax, H) | Provision the ruled menu (pinned, frozen, sha'd); fix-or-freeze the stage (fork #1); R-6 camera locked (dist 34, fov 24, yaw 47, pitch −50 — the camera is the judge); SDFGI OFF / glow ON determinism regime; caster body (fork #4); meters validated on synthetic cases. **Plus three one-call probes:** ① can Murzak's `node-modify` assign a `ProcessMaterial` (TCP-55 ① — decides whether W-MUR has an L7 capability at all); ② live-manifest enumeration to reconcile 58-vs-63 (L-B); ③ per-extension load-verify on 4.6.3 (no Murzak extension is CI-tested past 4.5.1). |
| **V-H → V-PRO → V-MUR** | Same frozen mode-(i) contract, three briefs each: **CAST** (flash at `prop_r` → travel → impact; event lifecycle), **AURA** (persistent loop on the character; survives motion; must not eat the silhouette at 12.5% frame height), **AMBIENT** (room-owned; ground-plane rule R-10 binding; area×layers budget — TCP-51: area is the entire cost). Contracts state what must be TRUE, never how (L-K). Per cell: TCP-32 clocks, declared surfaces, **W-PRO vs W×H strictly split** (TCP-50 — `create_particles`-family = W-PRO; `execute_editor_script` = W×H). |

Registered suspicion (qualitative, refutable): the discriminator is the **iteration loop** — H reads
its own file; W-MUR can't read back what it made; Pro round-trips screenshots. A VFX pass is a
parameter search (L7-V: six judged iterations in ~40 min).

### L6 animation — capability LADDER on the Synty corpus (3,386 FBX, six rigs)

**TCP-43 (L6-PREP) inverted the fork:** headless import PASS (2.78 s, 11/11), `.glb` round-trip
carries animation + root motion, Sidekick swings a sword with **0.000000000 m weapon drift** —
*"the wires do not own rigged content."* **H is proven; the WIRES are the unproven side.**
A-PREP freezes the corpus slice (idle · walk · sword attack · directional death; each ships in-place
+ `_RM_` twin), two bodies (Sidekick + one **modular** assembly off `ModularSyntyCharacter.fbx`),
and the meters (weapon-drift at `prop_*`; **foot-lock** variance under retarget). Each tool climbs:

**① import → ② RETARGET (the boss: name-match ≠ rig-match, mean rest Δ 27.69°, max 180°;
`SkeletonProfileHumanoid` both sides, per-clip `.import` patch) → ③ modular assembly →
④ walk (root-motion regime re-proven POST-retarget) → ⑤ fight + death → ⑥ AnimationTree
walk→attack transition.** Rung-reached is the headline metric; ceilings are PASSes (L-G).
Runs on **humanoids** — needs no Q44 story ruling. Monster content stays gated (goblin motion ≠
goblin mesh; **monster BODY existence unverified**).

**Order per Matt:** L7 first, then L6.

---

## §3 — The provisioning menu (TCP-55) — landed, awaiting Matt's rule

`agentic_orchestration/legolas/notes/2026-07-26-plugin-provisioning-menu.md` — **45 rows** (29 Godot
addons: 14 L7 / 15 L6 · Murzak's ten-package extension family, read for the first time · 5 CLI tools),
unranked, all pinned, telemetry-audited from source. Highest-consequence:

1. ★ **`Godot-AI-Particles` is NOT `create_particles`' counterpart** — emitter-count layer only,
   **zero `ProcessMaterial`/gradient/draw-pass access** (source-read at `69bdcdf4`). The charter's L7
   pairing was false; corrected. W-MUR's VFX reach now hangs on the V-PREP `node-modify` probe.
2. **Q46's scope grew:** all ten Murzak extensions are intrinsically clean but **cannot load without
   the core addon**, whose compiled-in Cloud default transmits machine/project identity to
   `ai-game.dev`. Q46 gates the entire family.
3. **Pro has nothing to provision** (175 tools is the ceiling); public addon audited CLEAN (loopback
   only); paid server closed/unaudited.
4. **New FLAG:** Godot Shaders Library fetches godotshaders.com inside the editor (lean: vendor
   static shaders instead). **Five rows carry no license** (= all rights reserved; Matt's call).
5. **L6 windfall:** Mixamo Animation Batcher (MIT, 4.6.2-tested) implements the R4 per-clip retarget
   patch in 312 lines — minus mandatory `rest_fixer/fix_silhouette`, hardcoded key: adaptation
   reference, not drop-in.
6. **Fairness rule adopted (L-H):** editor-only L6 tooling goes to ALL THREE cells or NONE.

**Proposed ruling shape (fits Matt's "download ALL helpful"):** bulk-install everything CLEAN +
licensed; exceptions held for his eye — the 5 unlicensed rows, the Shaders-Library live-fetch, the
Murzak family riding Q46, plus strike-on-sight. Audit evidence (4.9 MB source clones) stays at
`legolas/research/2026-07-26-plugin-audit-scratch/` until ruled; drax removes it in V-PREP.

---

## §4 — The decision queue (everything awaiting Matt, with leans)

**Gates on V-PREP (the next cell to fire):**

| # | Fork | Lean |
|---|---|---|
| 1 | Stage daylight defect (CEILING-1: crypt lit as daylit court, 4.66× contrast) — fix in V-PREP or hold constant | **Fix — and run the fix as a measured lighting-authoring datum** (see §6: lighting is on Matt's suite list and has never been a lap's *subject*, only its obstacle; the repair is the program's first lighting datum, free) |
| 2 | **Q46** Murzak cloud telemetry — local-only config / accept / park | (Matt's; now gates the whole extension family) |
| 3 | Menu bulk-ruling + 4 named exceptions (§3) | Bulk-install CLEAN+licensed |
| 4 | Caster body for L7 | The proven Sidekick `.glb` over a capsule |
| 5 | Wire mode-(ii) arrival arms | Not now; mode (i) settles the tool question first |

**Standing open items (not blocking V-PREP):**

- **18 open HALTs** (game-systems decisions, conductor may not resolve): arm 1 — escape clock,
  critical threshold, `primary_attack` in 7/10 kits · arm 2 — 6 missing glyphs (purchase fork),
  `Down_01` serving stun+knockback, Ice-with-no-Water · arm 3 — H-7…H-12 (report
  `…-tcp-l8u3-compositional-depth-report.md`) · arm 3b — H-14 (R-5/glass monotonicity), H-15, H-16 ·
  arm 3c — **H-17** (exemplar proportions carry 5-6 slots vs our 9+utility: grow tray to ~75% width /
  shrink socket 130→~104 tex px / fewer slots), **H-18** (crest-as-mount), **H-19** (utility slot).
  H-13 discharged.
- **L7-V rulings R-1…R-14 un-vetoed** at Matt's eye (campfire, warm-not-green fire, five fires, motes-flagged-weakest).
- **Q44 act-register → the story session** — still the highest-value unfired item on the board; gates
  monster CONTENT, biomes/register work, Q43's seven persistence rulings. Does NOT gate L7 or L6-capability.
- **Monster-mesh existence check** (one `ls`-scale recon against the Synty packs).
- **L5 SEAM in flight** (`2026-07-25-tcp-l5-seam-lap-charter.md`); its exit — recipe extraction +
  room #3 emitted from the recipe — is the bridge to everything procedural in §6.
- **jack-ryan Gate-2 BLOCK** on the emission-demo wave (`8321a6cc`) — his to walk Matt through.
- **19 commits unpushed on `main`** (this session's nine: `4a715ce4 d2b9865d caae8606 e57bbce5
  657190d6 b35ccc4c 7f6519e0` + legolas `2bdf9fca` + gandalf `73bc8da1`; plus prior sessions'). Push is Matt-gated.

---

## §5 — ★ THE SUITE GRID — pre-work for the architecture session

Matt's list, mapped onto what the program has PROVEN, what is OPEN, and the test shape each surface
earns. Three proven shapes: **LADDER** (capability, rung-reached — L6 shape) · **RACE** (frozen
mode-(i) contract, cost — L4/L8 shape) · **ARRIVAL** (mode-(ii) design — L5/L7-V shape). The list
forces a fourth: **GENERATOR (T6)** — author the *emitter* of content, score the emitter's output
and the authoring-minutes curve (the L5 exit metric, room-2 vs room-3, is its founding datum).

| Surface (Matt's list) | Class | Banked evidence | Open residue | Shape | Gate |
|---|---|---|---|---|---|
| **Characters** (modular, walk+fight) | T5 | TCP-43: H proven end-to-end; sockets; `_RM_` twins; `sidekick_creator` addon precedent | Wires untested; retarget at corpus scale; modular assembly | **LADDER** (L6, §2) | menu rule; A-PREP |
| **Monsters** | T5+content | goblin motion set (417 clips, shared rigs) | **Mesh existence unverified**; non-humanoid retarget; act-register | LADDER rungs reuse L6; content = ARRIVAL | **Q44 story session** + mesh check |
| **VFX** (cast/aura/ambient) | T4-VFX | TCP-51: area-is-cost, ground-plane, SDFGI-not-glow, R-6 camera; L7-V arrival banked | The three-tool RACE itself; W-MUR ProcessMaterial probe | **RACE** (L7, §2) | forks #1–#4 |
| **In-game UI (HUD)** | T4-UI | **L8 CLOSED**: full HUD, method H; family law; 18 HALTs | HALT rulings; H-17 proportions | — (verdict candidate: **tool axis SETTLED for HUD = H**) | Matt ratifies verdict |
| **Menu/selection UI** | T4-UI-M (new) | Dark-fantasy kit inventoried (arm 2); L8 grammar + instruments reusable | Screens ≠ HUD: navigation, focus, controller input, state machines; **inventory screen Matt-flagged "VERY useful"** | RACE-lite or H-direct per L8 verdict | none — free-standing |
| **"Beautiful corner" room** (hand) | T3 | L5's mode-(ii) room arrivals; L7-V stage derivation discipline | A showcase room is register-driven — is it act-gated or only style-register-gated? (elicit) | **ARRIVAL** | register ruling (story session) |
| **Proc-gen maps** | **T6** | L5 exit (recipe → room #3; authoring-minutes curve); instrument-dominance law | ★ **THE KEYSTONE FORK: where does generation live — Godot-side generators (drax) or engine-side emission (reincarnated-engine emits, Godot consumes)?** Engine-first orientation says this is an ENGINE-SEAM question pulling rocket/star-lord + the serial-content-emission tracker | **GENERATOR** | **L5 exit** + the seam ruling |
| **Proc-gen beautiful corners** | T6+T3 | — | Genre precedent to weigh: Diablo's answer is handcrafted set-pieces *stitched into* procedural layouts, not generated set-pieces. Test should compare emit-vs-stitch honestly | GENERATOR (late) | proc-gen maps first |
| **Biomes** | T6 bundle | element palettes; style-register (consumption-time filter, `reap-die-rise-story/style-register.md`) | Biome = tileset + lighting + ambient VFX + palette as ONE coherent bundle; register-driven | GENERATOR + ARRIVAL | story session (register) |
| **Lighting** | cross-cut → own surface | CEILING-1/2; R-4/R-5 additive discipline; SDFGI determinism; glow-free facts | Never yet a lap's SUBJECT. First datum free if fork #1 = "fix, measured" | ARRIVAL-lite per room/biome | fork #1 |

**Elicitation candidates Matt did not list** (flag, do not add unilaterally): audio/SFX; navigation +
monster behaviour (pulls the GD instrumentation workstream, CHANGELOG 2026-07-25); persistence/save
(Q43, story-gated); trailer capture (TRAILER-CUT dormant).

### Proposed wave sequencing (for the architecture session to amend, not obey)

- **Wave α — now, pending §4 forks:** V-PREP → V-H → V-PRO → V-MUR → **L7 verdict**.
- **Wave β — after α:** A-PREP → ladder ×3 → **L6 capability verdict** (humanoid).
- **Wave γ — free-standing filler:** menu-UI / inventory screen (no gates).
- **Wave δ — on L5 exit:** the **T6 GENERATOR** lap design + the engine-seam ruling (the architecture
  session's deepest question; *Engine first. Game second.*).
- **Wave ε — on the story session:** monster content · biomes · corner register · Q43/Q44.
- **Wave ζ — T7-FORGE (Matt-ruled 2026-07-28, SOFT):** author **our own package** on the race-verdicted substrate — the GENERATOR shape applied to tooling itself. **Ruling shape: terminal-LEAN, not terminal-LOCK** (Matt verbatim: *"I agree, but not a hard-fast rule. I still want the race to show us what's possible"*). The race retains its exploratory purpose; T7-FORGE is where its verdicts are expected to land, and the evidence can re-vote the destination. Founding fork (ELICITOR treatment, answered partly by banked evidence): substrate = **H-formalized** (versioned GDScript harness package; full control, zero telemetry/churn; we build the manifest layer) vs **Murzak-extension** (`Godot-AI-Tools-Template`, Apache-2.0 — `[AiTool]` auto-discovery + MCP wire + skill generation free; costs dotnet toolchain, the Q46-ruled telemetry surface, and upstream churn — two version bumps in one day, PC-W1-B). **Pro is eliminated as substrate by the framing itself** (closed server, no extension mechanism — it can win races and still lose the war). Composes with the T6 seam fork: under engine-side emission, the package's truest candidate shape is **the consumer** — the trace-loader/renderer the REPLAY capstone prototypes. Sequenced after Waves α/β (nothing jumps the queue — the L8 lesson); the bake-off's terminal artifact upgrades from verdict table to **the requirements spec for this package**, every VERDICT row a priced ingredient. Evidence lineage: PROVISION-CAL R-PC-9 (third-party uplift smaller than advertised) + the PC-T3 prize (both plugins failed their probes; we kept our tools and took the one load-bearing ingredient).

### The five agenda items for the architecture session

1. **Rule §4** (five forks + menu) — unblocks Wave α the same session.
2. **Adopt/amend the suite grid** — surfaces, shapes, gates; elicit the unlisted candidates.
3. **Tool-axis retirement policy** — per surface, a standing VERDICT line ("settled: H" / "open:
   ladder pending"), so the program *converges* instead of re-testing; ends-of-capability get written
   down, which is the standing intent's finish line.
4. **The T6 seam fork** — Godot-side vs engine-side generation. Biggest consequence, least evidence;
   deserves ELICITOR treatment (decision-shaped options, genre precedent, Matt rules).
5. **Charter V-PREP** under the desirable-run pattern and fire Wave α.

---

## §6 — Session discipline record (for the ledger's conscience)

Conductor defects this session, already codified: the 5× clock error (TCP-54 ②, L-Q corollary); the
deletion-steer Matt caught in advance (TCP-54 ①/⑩); the "bare Murzak first" lean that re-created
L-C's error and was inverted by Matt (TCP-55 ⑧) — **second and third instances this lap of the
owner's ruling out-judging the conductor's frame.** The architecture session should treat conductor
leans accordingly: stated, never pre-loaded.

## §7 — Artifact index

| What | Where |
|---|---|
| Program charter (laws L-A…L-R; ledger →TCP-55; lap table) | `agentic_orchestration/gandalf/notes/2026-07-24-tool-capability-program-charter.md` |
| Provisioning menu (45 rows) | `agentic_orchestration/legolas/notes/2026-07-26-plugin-provisioning-menu.md` (+ scratch clones, evidence) |
| L8 arm reports (1, 2, 3, 3b, 3c) | `agentic_orchestration/drax/notes/2026-07-25-tcp-l8u*-report.md` |
| L7-V VFX arrival (TCP-51) | `agentic_orchestration/drax/notes/2026-07-25-tcp-l7v-vfx-arrival-report.md` |
| L6-PREP animation probe (TCP-43) | `agentic_orchestration/drax/notes/2026-07-25-tcp-l6prep-animation-probe-report.md` |
| L5 SEAM charter (in flight) | `agentic_orchestration/dispatches/2026-07-25-tcp-l5-seam-lap-charter.md` |
| Lab floors | `~/Games/mcp-lab/` — `project/` (substrate, sha `d45db0f5…`, 0444) · `l5*` via evidence · `l6prep/` · `l7vfx/` · `l8ui/` (ui…ui3c, out3b/out3c, ref3c) · `harness/` (borrows nothing) |
| Synty animation corpus | `matt_notes_handoff_docs/recent-synty-packs/synty-animations/` (3,386 FBX; 6 rigs) |

**Signed:** gandalf, 2026-07-26 (`RUN-CONDUCTOR`). Veto-open, as always.
