# KING-TWIN — Playable Synty-Dressed Auto-Battle Scene Run (charter)

> **STATUS:** RATIFIED + **LAUNCHED at KT-1** (E1–E5 Matt-ruled 2026-07-23; conductor DRIFT-CRITIC
> launch-gate pass complete — KTL-1: HEAD re-verified `df7857e`, three authoring tensions
> dispositioned, T2 decidability fix + T3 overlap fix applied).

**Conductor:** gandalf `RUN-CONDUCTOR`. **Chartered:** 2026-07-23, on Matt's "All leans approved for
E1-E5" ruling (KIT-FIDELITY ledger KFL-7(a)). **Chains from:** KIT-FIDELITY
(`agentic_orchestration/gandalf/notes/2026-07-23-kit-fidelity-run-charter.md`) — that run compiles the
mechanically-real fighters + the fidelity-gauge window; **this run DRESSES that same window in Synty
assets to the king-scene exemplar's fidelity.** Neither run blocks the other (E1 overlap-start).
**Substrate evidence:** `agentic_orchestration/gandalf/notes/2026-07-23-synty-census-evidence.md`
(commit `5ad6805f` — NO-BLOCKER verdict; the king-rig grammar decomposed; the quill-rat gap named).
**Desirable-run-pattern fit:** §2 (all four questions YES). **Charter author conducts** (intent
residency): the elicitation forks were drained into Matt's E1–E5 rulings (§0.1), embedded verbatim.

---

## §0 Why this run exists — a PLAYABLE TWIN of the king exemplar (Matt's verbatim intent)

The KIT-FIDELITY window is a *diagnostic instrument* — proxies + procedural HP bars + damage floaters,
faithful to the sim but visually a debug read-out. Matt named the desired-end-state for the *player-
facing* form of that same battle:

> **(verbatim, 2026-07-23):** *"rendering these kits, monsters and floors/walls with all synty assets
> in a playable (can press play, but it will be an auto battle) scene in godot. Our exemplar/canonical
> king scene (with aura and sword) would be the desirable end state twin."*

**This run's thesis:** take the KIT-FIDELITY pilot-5 fighters + their harvested starter-set monsters +
a Synty arena, and instantiate each at the **king-exemplar rig grammar** (census §7): body mesh scaled
~1.85m via GeneralSkeleton retarget · weapon prop on a hand socket · element-keyed aura (Binbun VFX +
interior-clip shader) · king lighting + camera register · Synty floors + walls. The end-state is a
scene where **press-play runs the auto-battle** and every fighter looks like it belongs in the same
world as `scenes/probe_king_mcp.tscn`. "Twin achieved" is **five checkable criteria per fighter + the
arena** (§4) — not a taste feeling. This run **DRESSES** the fight; it adds no mechanics, no content
systems, no UI beyond what the parent run's KF-6 already renders into the same scene.

**What this run is NOT:** it does not compute damage, roll hits, select targets, or fork the playback
scene — the zero-derivation law is inherited whole (§8). The sim (KIT-FIDELITY) owns every number; this
run makes the fight **look like the game.** The pilot-5 (d2-firewall-sorc · d2-fire-sorc ·
gd-flames-of-ignaffar-purifier · poe2-bonestorm · poe1-cyclone) are the parent run's ratified roster
(KFL-4(b)); the monsters are their harvested starter sets (KIT-FIDELITY KF-3).

### §0.1 Matt's E1–E5 rulings (verbatim ratification — the charter's spine)

Matt, 2026-07-23: **"All leans approved for E1-E5."** The five leaned forks, now RATIFIED:

- **E1 — CHAINED charter (this document), not a tack-on; OVERLAP-START authorized.** KING-TWIN work
  begins NOW against existing REPLICA-1 frame data + the existing `replica_playback` window; the
  parent's compiled-kit frames (KF-5/KF-6) swap in when they land. Neither run gates the other.
- **E2 — ONE asset-mapping-table brief** covering ALL pilot kits + ALL harvested mobs. Each row:
  entity → proposed Synty asset + one named alternate. Delivered self-contained in-chat; a **single
  Matt ruling pass** = the KT-1 exit. Commitment-boundary (§7).
- **E3 — ONE arena**, assembled from the king-scene environment grammar (census §5 `polygon-dungeon-
  pack` modular pieces). The existing arena / ravine / crypt scenes are *references*, not the
  deliverable.
- **E4 — the FIVE-ELEMENT twin decomposition is the decidable core** (§4). Per fighter: (1) Synty mesh,
  no capsule proxies; (2) weapon prop in hand socket; (3) element-keyed aura; (4) king lighting +
  camera grammar; (5) Synty floors + walls. Checkable per fighter + arena against the census §7 recipe.
- **E5 — the parent's KF-7 watch venue = best-available:** the assembled KING-TWIN scene if ready, the
  plain playback fallback otherwise. **KF-7 never blocks on KING-TWIN** (the parent's fidelity-gauge
  watch stands on its own instrument).

---

## §1 Substrate facts (PINNED — from the census, commit `5ad6805f`; re-verified at DRIFT-CRITIC before launch)

All in `/Users/admin/Games/reincarnated-godot` (drax's repo). READ-ONLY reconnaissance; assembly
writes land in that repo under drax.

- **54 Synty POLYGON pack directories · 24,560+ FBX/GLTF · 707 Synty `.tscn`** (census §1). Scale is
  not a constraint — the run is a *selection + assembly* problem, not an acquisition one.
- **Character mesh pool (census §2):** `polygon-fantasy-characters` (King, Wizard, Sorcerer, Baird,
  Female Witch, Female Druid, Male Rogue, Female Queen) + `polygon-dark-fantasy` (DarkLord, Witch,
  Priest, Hunter, PlagueDoctor) + `polygon-modular-fantasy-hero-characters` (retargetable modular).
  **~60–80 humanoid meshes** — caster ×2 distinct fire identities, gunner/rogue, heavy melee, bone-
  witch all covered.
- **Creature pool (census §3):** ~25–30 skins — skeletons ×8–9, zombies ×4, goblins ×6, ghosts ×2,
  werewolf ×2, demon-kin ×3. Recolor/rescale/retarget covers a 15–20 mob roster.
  **NAMED GAP:** no `*rat*`/`*quill*` mesh; farm animals static-only. D2 starter Spike Fiend/Quill Rat
  has no direct mesh (§5 fallback (a)).
- **Weapons + props (census §4):** 250+ meshes — staves/wands/druid-staff (caster kits), the king's
  `SF_Wep_Elven_Greatsword_01`, `SM_Wep_Crossbow_01` (rigged; purifier-gunner candidate). **All five
  pilot-kit hand-props coverable.**
- **Environments (census §5):** `polygon-dungeon-pack` = **463 modular pieces** (7 floor families,
  wall/archway/trim, pillars, bone/macabre deco) — the E3 arena source. Plus dark-fortress, dwarven-
  dungeon, elven-realm (the king's architecture).
- **VFX families (census §6):** Binbun fire / beam (channel-cone) / magic_projectiles / impact /
  poison / ice / muzzle_flash / `basic_area_vfx_01` (the king's golden aura). Custom juiced shaders ×4
  + `aura_clip` / `king_clip` interior-scissor shaders in `/scripts/`. **Element-keyed auras
  coverable for every pilot element** (fire ×3, physical/bone, cold).

### §1.1 The king-rig recipe (PINNED — census §7, the E4 twin-criteria substrate)

`scenes/probe_king_mcp.tscn` · `scripts/king_rig.gd` (`KingRig`). The reusable per-kit recipe:

- **Body** — mesh scaled to ~1.85m via **GeneralSkeleton retarget** (the import plugin pre-exists).
- **HandSocket** (`BoneAttachment3D "hand_r"`) — weapon prop; pose lives in the hand LOCAL frame,
  re-solves per animation frame.
- **Element-keyed aura** — Binbun area VFX + `aura_clip` interior-scissor shader + tuned OmniLight
  (bloom-washout tuning, Matt 2026-06-22).
- **Retargeted locomotion** — anim-base idle/walk, 0.18s crossfade.
- **Scene register** — Camera FOV 30° · Key DirectionalLight (−22°,28°,0°) E2.4 · ambient E0.8 · glow ON.
- **Verified constraints:** armor/cape BAKED into body (no dress-up slots — the twin dresses by mesh
  *choice*, not slot-assembly); exactly four attachments on the king; cape is an unskinned static
  extract (bind-pose-leak fix — a known assembly hazard, §5).

### §1.2 Playback substrate (PINNED — census §8; the reason KT-4 is a SWAP, not a build)

`scenes/replica_playback.tscn` + `scripts/replica_playback.gd` **already build procedurally:** arena,
camera, lights, entity proxies, HP bars, floaters, telegraphs, aim-line, scrubber — interactive +
headless-smoke modes, external frames via `--frames-dir`. **KT-4 is a proxy→rig swap inside a working
window, never a scene-from-scratch.** Godot HEAD carries drax's playback commits (parent §1.1: `90d79c5`
+ `df7857e`, pushed KFL-4(a)).

---

## §2 Desirable-pattern fit test (all four YES — pattern doc:
`agentic_orchestration/operating-procedures/desirable-run-pattern.md`)

- **F1 — Enumerable?** **YES.** Bounded substrate = **the on-disk Synty catalogue** (census §1–§6,
  frozen at KT-1 entry: 54 packs, ~60–80 humanoids, ~25–30 creatures, 250+ props, 463 dungeon pieces,
  25 VFX sets) **× the fixed target roster** (5 pilot fighters + the KIT-FIDELITY starter-set mobs +
  1 arena). Every element countable, listable, diffable. The mapping table (KT-1) IS the enumeration
  made explicit.
- **F2 — Decidable?** **YES.** Every gate KT-2..KT-4 has a **decidable exit predicate the run checks
  without Matt** (§3): rigs load headless without error; twin criteria 1–5 hold per fighter + arena
  (mesh-not-capsule, prop-on-socket, aura-present, king-register-applied, Synty-floor/wall) —
  each a boolean the headless harness + galadriel capture confirm. Where "does it look right" needs
  judgment, that judgment is the **KT-5 Matt watch** commitment-boundary (§6), not an in-run quality
  loop.
- **F3 — Pre-drainable?** **YES — already drained.** The elicitation forks became Matt's E1–E5 rulings
  (§0.1); the ONE genuine per-entity commitment-boundary (which Synty asset dresses which entity) is
  converted pre-launch into the **single KT-1 mapping-brief ruling pass** (§3). Residual forks are
  **reasoning-boundaries** (retarget parameters, aura-family selection, arena piece layout, recolor
  choices) — ruled in-run veto-open (§7).
- **F4 — Authority-resident?** **YES.** The conductor holds design authority for the residual
  reasoning-boundaries (they are *presentation* calls against the census + the king grammar — squarely
  SCENEWRIGHT/SPEC-AUTHOR territory); drax executes all Godot assembly in his repo; galadriel verifies
  captures; Matt holds KT-1 mapping ratification + the KT-5 twin verdict (§7). No engine diff is
  expected (godot-repo-only) — jack-ryan Gate-2 rides only if one occurs.

---

## §3 Gates KT-1..KT-5 (decidable exit predicates + executor seams)

Sub-agent routing per the conductor-economics corollary (pattern §2.1): pieces route to **NAMED**
agents in their seams; the conductor writes no production code and no Godot scenes.

### KT-1 — Asset-mapping brief (conductor compiles from the census; **Matt rules** — commitment-boundary)

The conductor assembles ONE table (E2) from the census (§1) covering **every pilot-kit fighter + every
KIT-FIDELITY starter-set mob**. Each row: **entity → proposed Synty asset (mesh + hand-prop +
element-keyed aura family) → one named alternate.** The arena's environment-piece family is proposed in
the same brief. The five element→aura bindings are named (fire ×3 → Binbun fire family; bonestorm →
magic_projectiles/bone tint; cyclone → physical/impact or wind-tinted beam). **The quill-rat gap
(§1, §5a) is surfaced here as a decision-shaped fallback fork**, not silently substituted. **Mob rows
carry their own prop + aura columns, which may read "none"** (a zombie is unarmed; starter trash
carries no aura) — and the brief proposes a **default mob-aura policy: none for starter-set mobs,
aura reserved as elite/boss marking** (the D2 champion/unique idiom: the aura signals SPECIAL, and
the king reads as singular because the room does not glow with him) — Matt rules the policy in the
same pass.

**Exit predicate:** every pilot-kit fighter + every harvested starter-set mob has a **Matt-ruled Synty
asset row** (mesh + prop + aura), the arena piece-family is ruled, and the quill-rat disposition is
ruled. **Output = the self-contained in-chat mapping brief** (§6) — options + one-alternate-each +
consequence, readable in-chat (RL-6 binding: no doc-spelunking to rule). Matt sees the full dress plan
before assembly spends.

### KT-2 — Fighter rig assembly (drax)

Per ruled row, drax instantiates the census §7 king-rig recipe: body mesh → **GeneralSkeleton retarget
scaled ~1.85m** + hand prop on the `hand_r` socket + element-keyed aura (Binbun VFX + `aura_clip`
shader) + retargeted anim-base locomotion. Applies to the 5 player fighters AND the ruled starter-mob
rigs (mobs at their own scale, with prop + aura **per their ruled KT-1 mapping row** — a row may rule
"none"; residual visual detail stays a drax reasoning-boundary).

**Exit predicate:** the **5 player rigs + all ruled starter-mob rigs load headless without error**;
**twin criteria 1–3 hold per rig AS RULED IN ITS KT-1 MAPPING ROW** — (1) Synty mesh present, no
capsule proxy (every rig, no exceptions); (2) weapon prop parented to the hand socket where the row
rules a prop; (3) element-keyed aura instantiated where the row rules an aura (player-5: always). A
rig that fails retarget routes to its named **alternate** (§5b), never to a capsule fallback.

### KT-3 — Arena assembly (drax)

ONE arena (E3) from the census §5 `polygon-dungeon-pack` modular grammar + the king lighting/camera
register (§1.1: FOV 30°, Key DirectionalLight −22°/28° E2.4, ambient E0.8, glow ON). The existing arena
scenes are layout references only.

**Exit predicate:** the **arena scene loads headless**; **twin criteria 4–5 hold** — (4) king lighting
+ camera grammar applied (glow ON, the named light/ambient/FOV values); (5) Synty floors + walls
present (dungeon-pack pieces, no procedural-flat placeholder floor).

### KT-4 — Scene integration (drax assembles; galadriel verifies)

The proxy→rig swap **inside** `replica_playback.tscn` (census §8 — the scene ALREADY builds arena /
camera / lights / HP bars / floaters / scrubber procedurally; this gate swaps proxies for KT-2 rigs +
the KT-3 arena, **not** a new scene). Press-play runs the auto-battle from frame data (REPLICA-1 frames
now; KF-5/KF-6 compiled-kit frames when they land — E1). **galadriel** takes verification captures
confirming visual assembly (rigs render, auras visible, arena dressed, floaters present; the parent's
KF-6 globes + hot-bar confirmed **if landed** — E1 overlap means they may not have; that check defers
to KF-6's landing, the §7/§8 no-fork law binding from launch either way).

**Exit predicate:** **headless smoke GREEN** (0 errors / 0 leaks); a pilot fight loads and plays with
dressed rigs in the dressed arena; **galadriel capture on record** confirming the assembly. The
parent's KF-6 surfaces (globes + hot-bar), **whenever they land**, render in this SAME scene —
KING-TWIN did not fork it (§7/§8).

### KT-5 — Matt watch: twin verdict (commitment-boundary)

Matt watches the dressed auto-battle and delivers the **twin verdict against the king exemplar**
(`scenes/probe_king_mcp.tscn`): does each fighter belong in the king's world? Is the five-criteria
decomposition (§4) satisfied to his eye?

**Exit predicate:** Matt watches and rules — **acceptance is his own inspection verdict** (twin
achieved / named deviations). **Output = a self-contained watch brief + side-by-side pointer** (§6):
what he's seeing, the king exemplar to compare against, the five criteria as a read-checklist,
scrubber controls — readable in-chat (RL-6 binding).

---

## §4 The five twin-criteria (E4 — the decidable core; NOT pending pins)

Unlike the parent run (whose PINS A/B were definitional taste held for Matt), KING-TWIN's definition of
"done" is **already ruled** (E4). "Twin achieved" is this boolean conjunction, checked per fighter and
for the arena, grounded in the census §7 recipe:

1. **Synty mesh, no capsules** — the fighter is a Synty humanoid mesh (KT-2 crit 1), not a proxy shape.
2. **Weapon prop in hand socket** — a Synty prop parented to `hand_r`, posing in the hand-local frame
   (KT-2 crit 2).
3. **Element-keyed aura** — a Binbun VFX aura + `aura_clip` interior-clip shader keyed to the fighter's
   element (KT-2 crit 3). *Player-5: required. Mobs: per their KT-1 mapping row (default: none for
   starter trash — the aura is elite/boss marking, ruled at KT-1).*
4. **King lighting + camera grammar** — the named register (FOV 30°, Key DirectionalLight, ambient,
   glow ON) applied to the arena scene (KT-3 crit 4).
5. **Synty floors + walls** — dungeon-pack modular floor + wall pieces, no procedural placeholder
   (KT-3 crit 5).

**Twin verdict (KT-5):** all five hold, per fighter and per arena, to Matt's eye against the king
exemplar. The headless harness + galadriel capture pre-confirm 1–5 as *present*; Matt rules whether
present-and-assembled reads as *belonging in the same world*.

---

## §5 Pre-registered honorable fallbacks (pinned before results — the run cannot grow scope silently)

- **(a) Quill-rat / mesh-less mob (NAMED, census §3).** D2's Spike Fiend/Quill Rat has no Synty mesh.
  **Offered as a decision-shaped fork in the KT-1 brief** (Matt rules there, not the conductor
  silently): either **starter-set substitution** (the harvest carried 5 D2 mobs; 4 suffice for the
  encounter) OR **proxy-with-log** (a capsule for that one mob, visibly flagged as a known gap). Never
  a silent substitution.
- **(b) Mesh retarget failure (KT-2).** If a chosen mesh fails GeneralSkeleton retarget, drax uses the
  **named alternate** from the KT-1 mapping table — *that is why every row carries one alternate.*
  Logged in the ledger; never a capsule.
- **(c) VFX element mismatch (KT-2 crit 3).** If no Binbun family cleanly matches a fighter's element,
  use the **nearest family + log** the substitution (e.g. cyclone-as-wind → tinted beam/impact if no
  dedicated wind set). The gauge of "close enough" is the king aura's read (a colored energy field),
  not a specific particle system.
- **(d) Assembly-hazard: cape/bind-pose leak (census §7).** The king's cape is an unskinned static
  extract. If a chosen mesh needs a comparable cloth element, extract it unskinned per the king
  precedent; if that fails, **omit the cloth** (mesh + prop + aura still satisfy criteria 1–3) rather
  than ship a bind-pose leak.
- **(e) Playback stall (inherited).** If live Godot playback stalls at KT-4, batch MP4 renders from the
  same frames via drax's walkthrough harness — Matt still watches the dressed twin (E5 best-available).

**Every discovery beyond the census** (a mesh the census missed, a pack not enumerated, a mob with no
viable dress) is a **next-lap admission** — logged, offered to Matt if it changes the roster, never
silently pulled into scope. This run dresses the fixed roster in the enumerated catalogue; growing
either is a new lap.

---

## §6 Declared Matt interface (RL-6 lesson BINDING: no decision point requires opening a doc)

- **Self-contained in-chat briefs at exactly TWO points:**
  - **KT-1** — the ONE asset-mapping brief (E2): every fighter + mob → proposed Synty asset + one
    alternate; the arena piece-family; the quill-rat fork. Options + consequence, **readable in-chat**;
    a **single ruling pass** closes the gate.
  - **KT-5** — the watch brief: what he's seeing, the king exemplar to compare, the five twin-criteria
    as a read-checklist, scrubber controls.
- **Red-flag pings only** otherwise (a fallback fires, a named gap widens, a seam blocks).
- **Push-as-you-go** (inherited from parent KFL-4(a)): the conductor pushes each **verified** seam
  commit (drax rig/arena/integration commits, galadriel captures) after its DRIFT-CRITIC pass. This
  charter + ledger commit-and-push as produced. **The conductor does NOT push this charter until its
  own DRIFT-CRITIC launch-gate pass** (status banner; KFL-1 precedent).

---

## §7 Halt taxonomy (pattern §4 — the distinction that separates the run histories)

**Commitment-boundary HALT (Matt-reserved / Gate-2 / committed-truth / external danger):**

- **KT-1 mapping ratification** — which Synty asset dresses which entity is Matt's single ruling pass;
  the quill-rat disposition is his call there.
- **KT-5 twin verdict** — whether the assembly reads as a twin of the king exemplar is Matt's eye.
- **Any engine-code diff** — none is expected (godot-repo-only). If assembly surfaces a need to change
  the frame schema or emit new fields, that routes back through the PARENT run's KF-5 additive-schema
  path under **jack-ryan Gate-2**, not an in-run engine touch here.
- **Forking the playback scene** — HALTS. One scene, two runs feed it (§8); a structural fork of
  `replica_playback.tscn` that would break the parent's KF-6 globes/hot-bar is a commitment-boundary.
- **decisions-log / committed-truth contradiction; external-state danger** (writing outside the godot
  repo working tree).

**Reasoning-boundary HALT (conductor rules in-run, veto-open, logged) — the failure this run
eliminates:**

- **Retarget parameters** (scale tuning per mesh, bone-map corrections) — drax call, ruled in-run.
- **Aura-family selection** where the mapping named a family but the exact Binbun set is a choice —
  ruled with drax, veto-open.
- **Arena piece layout** (which dungeon-pack pieces, room shape, deco density) — SCENEWRIGHT call
  against the king register, ruled in-run.
- **Recolor / rescale details** on shared meshes (a goblin reused across two mob roles) — curation
  call, ruled in-run.
- **Which mobs carry auras** beyond the required player-5 — drax judgment, ruled in-run.

The founding exemplar (pattern §4): a presentation-assembly fork that would formerly stall the run is
ruled in-run under the run's own headless-harness + galadriel-capture checks; only the genuine
commitment-boundaries (KT-1 mapping, KT-5 verdict) reach Matt.

## §8 Inherited laws (from KIT-FIDELITY + REPLICA-1 — carried whole)

- **ONE scene, two runs feed it.** KIT-FIDELITY's KF-6 deliverables — health globes + skill hot-bar +
  the `12,500 (87%)` floaters — render in the **SAME** `replica_playback.tscn` that KING-TWIN dresses.
  KING-TWIN **must NOT fork the playback scene** (§7). The parent computes-and-emits; KING-TWIN
  dresses-and-arranges; they compose in one window.
- **Zero-derivation law (REPLICA-1 §7, inherited whole).** The scene **DISPLAYS**, never **COMPUTES.**
  KING-TWIN rigs render frame data (positions, hits, HP, floaters); they never roll damage, select
  targets, or recompute a gauge. If a rig needs a value to show that isn't in the frame, that is a
  PARENT-run additive-schema field + re-emit — never a Godot computation.
- **Push-as-you-go** (parent KFL-4(a)) — verified seam commits push as produced; this charter pushes
  only after its DRIFT-CRITIC launch-gate pass.
- **Seam ownership.** drax owns all Godot assembly (his repo); galadriel owns KT-4 verification
  captures; the conductor (gandalf `RUN-CONDUCTOR`) does course only — no production code, no scenes;
  jack-ryan Gate-2 rides **only** if an engine diff occurs (none expected).

---

## Ruling ledger

*(Format per parent: dated, decidable, veto-open.)*

- **KTL-0 (2026-07-23, Matt in-chat + conductor): ELICITATION RATIFIED — E1–E5 ruled; charter chained;
  substrate evidenced.** Matt (verbatim): **"All leans approved for E1-E5."** Records: **(a)** the five
  rulings — separate CHAINED charter + overlap-start (E1) · ONE mapping-table brief covering all kits +
  mobs, single ruling pass (E2) · ONE arena from the king-scene environment grammar (E3) · five-element
  twin decomposition as the decidable core (E4) · KF-7 watch venue best-available, never blocking on
  KING-TWIN (E5). **(b)** CHAINING: KING-TWIN chains from KIT-FIDELITY (KFL-7(a)); the parent compiles
  the fighters + fidelity window, this run dresses the same window to king-exemplar fidelity; neither
  blocks the other. **(c)** SUBSTRATE EVIDENCE: the Synty census (commit `5ad6805f`) — NO-BLOCKER
  verdict for 5 rigs + 15–20 mob roster + arena + VFX at king-grammar quality; the quill-rat mesh gap
  named as the sole §5(a) fallback fork. **Launch is GATED on the conductor's DRIFT-CRITIC pass**
  (census facts re-verified against `reincarnated-godot` at HEAD + a charter-integrity read; the
  KF-6-presence check is a **KT-4 conditional**, not a launch blocker — E1 overlap-start governs);
  KT-1 fires on that pass with its mapping brief as Matt's first in-chat ruling. Veto-open.
- **KTL-1 (2026-07-23, conductor): DRIFT-CRITIC LAUNCH-GATE PASS COMPLETE — RUN LAUNCHED at KT-1.**
  Census facts re-verified: `reincarnated-godot` HEAD = `df7857e`, unchanged since the census capture
  (§1 stands). The author's three flagged tensions dispositioned: **(T1 ACCEPTED)** §4-as-settled-
  rubric is correct — E4 is Matt-ruled; the taste layer survives at KT-5. **(T2 FIXED — decidability
  hole, wider than flagged):** criteria 2–3 could not hold for unarmed/aura-less mobs (a zombie
  carries no prop), silently failing KT-2's exit as written; fix = mob mapping rows carry prop/aura
  columns that may rule "none," KT-2's exit binds to the ruled row, and the mob-aura DEFAULT (none
  for starter trash; aura = elite/boss marking, the D2 champion/unique idiom) is folded into the KT-1
  brief for Matt's same-pass ruling — promoted from silent drax-judgment to a ruled policy.
  **(T3 FIXED — overlap contradiction):** KF-6-presence-in-scene as a LAUNCH blocker contradicted E1
  overlap-start (the parent is at KF-2/3; KF-6 does not exist yet); demoted to a KT-4 conditional,
  the §7/§8 no-fork law binding from launch. **KT-1 mapping-table compilation FIRED** (named-gandalf;
  census + the four game harvest notes as substrate; brief lands self-contained in-chat for Matt's
  single ruling pass, including per-game starter-set membership confirmation where the harvest left
  it informal — poe2/gd). Veto-open.
- **KTL-2 (2026-07-23, conductor): KT-1 BRIEF COMPILED + CONDUCTOR-VERIFIED — AWAITING MATT'S RULING
  PASS (commitment-boundary HALT per §6/§7).** Brief at
  `agentic_orchestration/gandalf/notes/2026-07-23-kt1-asset-mapping-brief.md` (named-gandalf, commit
  `4f106837`). **Trust-but-verify pass (conductor, on-disk):** every identifier in the brief resolved
  against `reincarnated-godot` — 39 character/prop meshes (all 5 pilot rows + alternates + all 18 mob
  rows), 6 Binbun VFX scenes, 11 dungeon-pack env pieces, host `scenes/boss_arena_30x30.tscn`, and the
  `aura_clip` shader: **zero MISSING.** One surgical DRIFT-CRITIC fix: bonestorm's aura attributed to
  `magic_areas_scene.tscn` — corrected to the **magic_orbs family (assets-14)**,
  `magic_orb_basic_vfx_01.tscn` directly. King-singularity constraint honored (no King mesh / crown /
  `SF_Wep_Elven_Greatsword_01` in any row; cyclone's 2H is `SF_Wep_GreatAxe_01`). T2 decidability fix
  present (mob rows carry prop/aura columns ruling "none"). **Queued to Matt in ONE in-chat bundle:**
  Fork 1 quill-rat (lean OMIT) · Fork 2 mob-aura default (lean none-for-trash/aura-as-elite-marking) ·
  Fork 3 arena family + deco density (lean dungeon-pack spine, bone garnish sparse) · Fork 4 PoE2+GD
  starter-set confirmation + 2 flagged beast proxies — **bundled with the parent run's GD numeric fork
  (KFL-8)** so Matt rules everything in one pass. KT-2 fires on the ruling. Veto-open.
- **KTL-3 (2026-07-23, Matt in-chat): KT-1 RULED — ALL LEANS APPROVED. KT-2 FIRED.** Matt (verbatim):
  **"All KT-1 leans approved."** Records: **Fork 1 → OMIT** (D2 starter set ships 4 honest mobs; quill-rat
  is a next-lap admission when a rodent mesh is sourced) · **Fork 2 → no aura on starter trash**; aura
  RESERVED as elite/boss/unique marking (D2 champion/unique idiom — ruled policy, no longer drax
  judgment) · **Fork 3 → arena as proposed** (dungeon-pack spine, bone deco sparse edges-only, host
  `boss_arena_30x30.tscn`, king camera/light register) · **Fork 4 → all four starter sets CONFIRMED as
  drafted** (D2×4 · PoE1×5 · PoE2×4 · GD×5) including both flagged beast proxies (Rhoa→werewolf,
  Thornback→werewolf). Tables A+B of the KT-1 brief are now **THE ruled mapping** — KT-2's exit binds
  to them row-by-row. **KT-2 rig-assembly lane FIRED** (named-drax, background: 5 pilot rigs at full
  king grammar + 18 mob rigs, headless load-smoke exit, write-as-you-go, commit-never-push, deviations
  logged never silent). **Supplemental pre-elicitation** (avoiding a second HALT): IF the parent run's
  GD fork rules C (kit swap), the replacement kit needs one Table-A row — conductor lean
  `poe1-frost-blades` over `d2-ww-barb` (ww-barb duplicates cyclone's armored-spinner read; frost-blades
  adds the palette's missing ICE element + rebalances roster d2×2/poe1×2/poe2×1); proposed row
  (on-disk-verified): `SK_Chr_Male_Rouge_01` · `SK_Wep_Sword_01` (hand_r, 1H) · `ice_shard_vfx_01`
  orbit + ice-blue `#7FD4FF`. Contingent — rules only if C fires. Veto-open.
- **KTL-4 (2026-07-23, conductor): KT-2 VERIFIED + PUSHED — AURA DEVIATION OVERTURNED — KT-3 FIRED.**
  **Rig assembly PASS:** 23/23 rigs (5 pilots + 18 mobs) headless GREEN (`RIG_SUMMARY passed=23
  failed=0`; retarget `RT_SUMMARY ok=22 bad=0`); zero alternate-mesh fallbacks; every Table A+B row
  shipped **as ruled** (quill-rat OMITTED per Fork 1; zero mob auras per Fork 2; both werewolf beast
  proxies per Fork 4); **king-singularity conductor-grep clean** (no King mesh / crown / elven
  greatsword under `scenes/rigs/`). **Drax deviation OVERTURNED by conductor disk-probe:** drax
  shipped all five pilots on tinted `basic_area_vfx_01`, reporting the ruled aura variants absent —
  but all five EXIST (`fire_area_03`/`_06` → `Binbun_VFX/assets-19` · `beam_vfx_04` → assets-5 +
  assets-12 · `magic_orb_basic_vfx_01` → assets-14 · `pulse_area_vfx_03` → assets-15); drax searched
  empty stub roots (`fire_effects/`/`magic_orbs/` under the wrong pack) and stopped. Grammar was
  preserved (real Binbun scene + ruled tint + light + lift + `aura_clip`), so the fix is surgical —
  the `TODO(drax)` hook in `pilot_rig.gd` swaps five paths. **Swap rides the KT-3 lane head.**
  **Handoff caveat recorded:** the 22 retarget `.fbx.import` edits live under gitignored
  `Assets/Synty/` — any fresh KT-4 host runs `scripts/kt2_apply_retarget.py` + `--headless --import`
  once before rigs build (drax report reproduce step). Commits verified + pushed: godot `4720353`/
  `ae2c40c`/`95f3fc7`/`2321d80`/`b3fd817`/`e17a16f`; collab report `3c9f7629`
  (`drax/notes/2026-07-23-kt2-rig-assembly-report.md`). **KT-3 ARENA LANE FIRED (named-drax):**
  step 1 aura-variant swap to the five on-disk paths above; step 2 arena per §KT-3 (dungeon-pack
  modular spine, bone deco sparse edges-only per Fork 3, king lighting/camera register FOV 30° /
  Key −22°/28° E2.4 / ambient E0.8 / glow ON); exit = arena loads headless + twin criteria 4–5 hold.
  Veto-open.
- **KTL-5 (2026-07-23, conductor): KT-3 VERIFIED + PUSHED — KT-4 FIRED.**
  **Both jobs PASS under conductor re-run:** rig harness `RIG_SUMMARY passed=23 failed=0` + arena
  `ARENA_SUMMARY ok=true (crit4=true crit5=true)`; all five pilots on their RULED Binbun variants
  (tint-exact, spot-checked `fire_area_03` @ #FF6A1A; assets-5 beam per preference); king-singularity
  grep hits resolved = drax's own guard COMMENTS (the ban documenting itself — held); commits
  `6416e1e`/`e607acd` clean of gitignored-Binbun leakage (message-text hits only); arena frame
  eye-verified (144 dungeon-pack floor tiles / 48 walls / 4 pillars + arch / 6 bone deco sparse
  edges-only per Fork 3; long-shadow king rake reads).
  **DEVIATION (drax-flagged, honest): Binbun stale-path defect** — beam/pulse packs carry internal
  `ext_resource` paths from the pack author's layout (`res://assets/BinbunVFX/...`), dead under
  `.gdignore` uid-blocking → `scripts/kt3_fix_aura_variants.py` authored as TRACKED AUTHORITY
  (572 refs / 156 files, idempotent, in-place on the gitignored tree). **Reproduce chain is now:**
  `kt2_apply_retarget.py` → `--headless --import` → `kt3_fix_aura_variants.py` → both harnesses.
  **LOGGED for KT-4 (its exit = 0 errors / 0 leaks):** 3 dummy-shader RID at-exit leaks on the rig
  harness post-swap (arena smoke clean) — KT-4 must resolve or explain before its gate closes.
  **SCENEWRIGHT eye-note (non-blocking; KT-5 is Matt's read):** the captured frame's off-arena void
  renders pale vs the king exemplar's near-black bg (0.10,0.11,0.13) — galadriel's KT-4 captures
  confirm the WorldEnvironment applies in playback; ribcage deco piece is large (count-sparse per
  Fork 3, scale is Matt's taste call at KT-5).
  **KT-4 SCENE-INTEGRATION LANE FIRED (named-drax):** proxy→rig swap INSIDE `replica_playback.tscn`
  (census §8 — same scene, no fork per §7/§8) + KT-3 arena in; press-play auto-battle from
  REPLICA-1 frames; galadriel verification captures follow drax's return. Veto-open.
- **KT-1:** RULED (KTL-3). **KT-2:** VERIFIED (KTL-4). **KT-3:** VERIFIED (KTL-5). **KT-4:** in
  flight (drax swap; galadriel captures follow). **KT-5:** pending.

**Signed:** gandalf (`RUN-CONDUCTOR`), 2026-07-23.
