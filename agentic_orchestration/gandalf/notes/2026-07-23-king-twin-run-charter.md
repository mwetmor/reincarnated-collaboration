# KING-TWIN — Playable Synty-Dressed Auto-Battle Scene Run (charter)

> **STATUS:** RATIFIED-ELICITATION (E1–E5 Matt-ruled 2026-07-23) — **LAUNCH GATED** on the conductor's
> DRIFT-CRITIC pass (KFL-1 precedent from the parent charter; census facts re-verified against
> `reincarnated-godot` at HEAD before KT-1 fires).

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
(§1, §5a) is surfaced here as a decision-shaped fallback fork**, not silently substituted.

**Exit predicate:** every pilot-kit fighter + every harvested starter-set mob has a **Matt-ruled Synty
asset row** (mesh + prop + aura), the arena piece-family is ruled, and the quill-rat disposition is
ruled. **Output = the self-contained in-chat mapping brief** (§6) — options + one-alternate-each +
consequence, readable in-chat (RL-6 binding: no doc-spelunking to rule). Matt sees the full dress plan
before assembly spends.

### KT-2 — Fighter rig assembly (drax)

Per ruled row, drax instantiates the census §7 king-rig recipe: body mesh → **GeneralSkeleton retarget
scaled ~1.85m** + hand prop on the `hand_r` socket + element-keyed aura (Binbun VFX + `aura_clip`
shader) + retargeted anim-base locomotion. Applies to the 5 player fighters AND the ruled starter-mob
rigs (mobs at their own scale; not every mob carries an aura — auras key to the *player* element
identity + boss-tier mobs at drax's judgment, a reasoning-boundary).

**Exit predicate:** the **5 player rigs + all ruled starter-mob rigs load headless without error**;
**twin criteria 1–3 hold per rig** — (1) Synty mesh present, no capsule proxy; (2) weapon prop parented
to the hand socket; (3) element-keyed aura instantiated. A rig that fails retarget routes to its named
**alternate** (§5b), never to a capsule fallback.

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
confirming visual assembly (rigs render, aura visible, arena dressed, floaters + globes + hot-bar from
the parent's KF-6 still present).

**Exit predicate:** **headless smoke GREEN** (0 errors / 0 leaks); a pilot fight loads and plays with
dressed rigs in the dressed arena; **galadriel capture on record** confirming the assembly. The KF-6
health globes + skill hot-bar (parent inheritance, §8) render in the SAME scene — KING-TWIN did not
fork it.

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
   element (KT-2 crit 3). *Mobs: aura optional per drax judgment; player-5: required.*
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
  (census facts re-verified against `reincarnated-godot` at HEAD; the parent's KF-6 globes/hot-bar
  confirmed present in the shared scene so KT-4 remains a swap, not a re-scene); KT-1 fires on that
  pass with its mapping brief as Matt's first in-chat ruling. Veto-open.
- **KT-1..KT-5:** pending (launch-gated on DRIFT-CRITIC).

**Signed:** gandalf (`RUN-CONDUCTOR`), 2026-07-23.
