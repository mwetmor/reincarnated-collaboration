# Reap. Die. Rise. — Godot Agent Contract (Canonical)

**Project:** Reap. Die. Rise. (ARPG / roguelite, Godot 4.7)
**Audience:** the **Godot assembly agent** (works via MCP, live editor open, snap-to-grid + element knowledge) and the **visual Judge agent** (evaluates generations/assemblies at the seam).
**Purpose:** the three **frozen specs** the Godot agent currently lacks — which is why assembly is ad-hoc. This is the **Godot-agent-facing companion to the JSON schema** (which is the content-engine-agent-facing contract). Same philosophy: the seam is a frozen, versioned spec. The Analyst watches conformance at the seam.
**Written in the agent's operational idiom:** grid units, named scene-tree nodes, and canonical editor-camera transforms the agent can snap to via MCP — so each spec line maps to an MCP action, not abstract math.

> **`[SET THIS]`** = a real measured/decided value to fill in (placeholder for now). Several are marked; fill them from the **2 existing assemblies** (mine them for "what the rule should have been") and from one explicit camera/scale decision. Until filled, treat the doc as the skeleton the agent will consume.

Tags: **[CONTRACT]** = frozen once set, do not vary per-assembly. **[TEMPLATE]** = structure to instantiate. **[RUBRIC]** = checkable acceptance criteria. **[CALIBRATE]** = derive from existing assemblies.

---

## 0. How to use this document

The Godot agent reads **§1 (geometry/scale/socket contract)** and **§2 (scene template)** at the top of every assembly task, and assembles **to spec** instead of re-deriving. The Judge reads **§3 (rubric + camera transforms)** as its definition of "done" and renders from the **real** cameras at mobile scale. **§4** is the one-time calibration from the existing assemblies. The whole point: turn *exploratory* agent assembly into *deterministic* agent assembly.

---

## 1. [CONTRACT] Geometry, Scale & Socket Contract

Frozen conventions. The agent snaps/places to these; it never invents them per-assembly.

### 1.1 Coordinate & grid convention
- **Up = +Y, Forward = −Z, right-handed** (Godot native).
- **1 Godot unit = 1 meter.**
- **Editor grid:** 1 grid cell = `[SET THIS: e.g., 1.0 unit]`; snap increment = `[SET THIS: e.g., 0.1 unit]`. Scale values below should land on snappable increments where possible (so the MCP agent's snap-to-grid produces the canonical values rather than approximations).
- **Ground plane = XZ** (Y = 0 is the floor).

### 1.2 Character pivot, scale & orientation
- **Pivot/origin: feet at origin** (character root at Y=0; the soles sit on the ground plane). The agent places the root so feet = world Y 0.
- **Canonical character height = `[SET THIS: units]`** (a "standard soldier"). [CALIBRATE from the 2 existing assemblies — what height did the agent use? Freeze it.] All characters scale relative to this (a giant is N× this; the soldier-mass is exactly this).
- **Facing: −Z** (character faces −Z in its local space; the agent orients accordingly).
- **Scale is uniform** unless a kit explicitly calls for non-uniform (avoid stray non-uniform scale — it breaks attachments and normals).

### 1.3 [CONTRACT] Weapon / item real-cm → units scale function (the "museum dimensions" payoff)
The content engine sometimes emits **real-world dimensions** (museum weapons in cm). These are only meaningful if converted consistently — otherwise they're unused flavor text.
- **Conversion:** `units = real_cm / 100` (since 1 unit = 1 m). A 110 cm sword = **1.10 units** long. The agent scales the weapon mesh so its in-engine length matches.
- **Reference anchor:** a `[SET THIS: e.g., 100]` cm weapon = `[SET THIS: units]` in-engine, seated in the hand socket, must read as correctly-sized **relative to the canonical character height (§1.2)**. [CALIBRATE: check the 2 assemblies — were weapons sized relative to the character, or arbitrary? Freeze the reference.]
- **When no dimension is provided:** fall back to a **per-item-class default length** (`[SET THIS: e.g., dagger 0.3u, sword 1.0u, greatsword 1.5u, warhammer 1.1u, staff 1.8u]`) so generated items without museum data still land at sane relative sizes.
- **Result:** a generated dagger and a historical greatsword on the *same* character read at correct *relative* scale — which is what makes the museum-accuracy *visible* in-game (a differentiator), not just data.

### 1.4 [CONTRACT] Skeleton + named-socket contract (deterministic MCP attachment)
Equipment attaches to **named `BoneAttachment3D` sockets on a canonical `Skeleton3D`** (the Synty Polygon base rig + the Meshy-equipment plan). The agent attaches via MCP by **socket name** — "attach to `Socket_RightHand`" — never by deriving a position.

- **Canonical rig:** `[SET THIS: confirm the Synty/Meshy base skeleton + bone names]`.
- **Canonical socket nodes** (exact names the agent references — confirm/adjust against the rig):
  - `Socket_RightHand` — primary weapon
  - `Socket_LeftHand` — off-hand / shield
  - `Socket_Head` — helmet
  - `Socket_Back` — sheathed weapon / cape / pack
  - `Socket_Hip_R`, `Socket_Hip_L` — sheathed sidearms
  - `Socket_Chest` — amulet / chest-VFX anchor
  - `Socket_Root` (feet/origin) — ground-VFX anchor
- **Armor = skinned mesh-swap on the skeleton** (Synty modular pieces), **not** socket-attach. The agent swaps mesh pieces on the rig; only discrete items (weapons, helmets, shields) socket-attach.
- **[CONTRACT] Each socket has a frozen local offset/rotation** so a given item class seats correctly (a sword grip aligns to the palm). `[SET THIS: per-socket seating offsets]` [CALIBRATE from the assemblies — where did weapons seat? Freeze the offsets so attachment is repeatable.]

---

## 2. [TEMPLATE] Canonical Character-Scene Template

The exact node tree the agent **instantiates via MCP** — so scene creation is *template instantiation*, not exploration. (This is what collapses the "learning scene creation" curve: the agent stops deciding *what* a character scene is and instantiates a *known* one.)

```
CharacterRoot                (Node3D)            # pivot at feet, world Y=0, faces −Z
├── Skeleton3D               (canonical rig)
│   ├── Mesh_Body            (skinned MeshInstance3D)
│   ├── Mesh_Armor_*         (skinned, swappable Synty pieces)
│   ├── Socket_RightHand     (BoneAttachment3D)  # weapon mesh instanced as child
│   ├── Socket_LeftHand      (BoneAttachment3D)
│   ├── Socket_Head          (BoneAttachment3D)
│   ├── Socket_Back          (BoneAttachment3D)
│   ├── Socket_Hip_R / _L    (BoneAttachment3D)
│   ├── Socket_Chest         (BoneAttachment3D)
│   └── Socket_Root          (BoneAttachment3D)  # ground-VFX anchor (feet)
├── VFXAnchors               (Node3D)
│   ├── VFX_Cast             (Node3D, at hands/chest)
│   ├── VFX_Aura             (Node3D, enchant-glow anchor — camera-facing billboard VFX)
│   └── VFX_Ground           (Node3D, at Socket_Root — horizontal/decal ground VFX)
├── CollisionFootprint       (optional, for the gameplay footprint)
└── (metadata)               # reference to the CharacterData Resource (from JSON→Resource import)
```

**Inventory render rig (the dual-viewpoint requirement — see VFX-pipeline §7):**
- A **`SubViewport` with its own front-facing camera** that renders the character/item for the inventory portrait. The agent instantiates the character into this SubViewport (or instances the same CharacterRoot scene) so the **same asset** is shown from the **front** in inventory and at the **2.5D angle** in gameplay. Camera-facing billboard VFX (auras) re-face the SubViewport camera automatically. `[SET THIS: SubViewport resolution + framing]`.

**[CONTRACT] The agent always produces this tree** (omit optional nodes only when truly N/A). Consistency here is what makes downstream systems (the JSON→Resource binding, the Judge's camera framing, the VFX anchors) reliable.

---

## 3. [RUBRIC] Standardized Judge Rubric + Canonical Camera Transforms

The rubric is the **assembly agent's definition of "done"** AND the **Judge's acceptance test** — the shared contract across the seam the Analyst watches. The Judge renders from the **live editor viewport** (editor is open) snapped to the canonical camera transforms below, at **mobile screen scale**.

### 3.1 [CONTRACT] The two canonical camera transforms
The Judge/agent snaps the editor camera to these to score *exactly what the player sees*.

- **Gameplay 2.5D camera** (`[SET THIS]`):
  - Projection: `[SET THIS: orthographic | perspective]` (Diablo-style is typically near-ortho or a low-FOV perspective).
  - Pitch (down-angle): `[SET THIS: e.g., ~50–55°]`.
  - Height / distance from target: `[SET THIS]`. FOV or ortho size: `[SET THIS]`.
  - Rotatable? `[SET THIS: locked-angle | player-rotatable]`. **If locked:** optimize hard for ground-readability/silhouette (one canonical angle). **If rotatable:** the rubric's "reads at angle" check must pass at all permitted yaw angles → all-sides readability (opposite trade-off; see VFX-pipeline §3/§5).
- **Front inventory camera** (`[SET THIS]`):
  - Straight-on (slight down-tilt optional), framing the **full** character/item.
  - Distance / FOV: `[SET THIS]`. Background: neutral portrait backdrop.

- **Mobile screen scale for scoring:** render/evaluate at `[SET THIS: target mobile resolution + in-game zoom]` — an asset reads with far fewer pixels on a phone at gameplay zoom than in a desktop preview. (Ties to build-architecture/VFX perf budget.)

### 3.2 [RUBRIC] Checkable criteria (each pass/fail, with notes)

**A. Scale conformance**
- Character height matches canonical (§1.2) within tolerance `[SET THIS: ±%]`.
- Weapon/item size correct **relative to the character** per §1.3; museum dimensions honored when provided.
- No item arbitrarily over/undersized vs. its class default.

**B. Pivot & orientation**
- Feet at origin (Y=0); character sits on the ground plane (no float/sink).
- Faces −Z.
- Each attached item seated in the **correct named socket** (§1.4), with no clipping into the body and correct grip/seat alignment.

**C. Reads at the 2.5D gameplay angle** (rendered from §3.1 gameplay cam, mobile scale)
- Silhouette is distinct/recognizable from above.
- Ground footprint reads clearly.
- Key detail (the stuff that signals the item/monster's identity) is visible at the angle — not occluded by foreshortening, not mush at mobile scale.

**D. Reads at the front inventory portrait** (rendered from §3.1 inventory cam)
- Detail and silhouette read straight-on; framed fully; palette legible.
- Gear-attached VFX (auras) read in the portrait too.

**E. Palette / StyleProfile conformance**
- Within the season/realm StyleProfile (palette, finish, emission) — tolerance `[SET THIS]`. (The Judge's narrowed StyleProfile-conformance task from the asset-gap pipeline.)

**F. Socket / attachment integrity**
- All expected attachment points populated as specified; no orphan/duplicate attachments; no z-fighting or intersection.

**G. (VFX assemblies only) blend/billboard correctness** — per VFX-pipeline §3/§9: correct billboard mode for the effect type, Alpha-Composite (premul-alpha) blend where specified, ground component present for ground/AoE/impact slots.

### 3.3 [RUBRIC] Scoring & gating
- **Definition of done:** all applicable criteria **pass** at both viewpoints (gear) / the gameplay viewpoint (spell VFX).
- **Fail = specific, actionable feedback** keyed to the criterion (e.g., "C-fail: greatsword silhouette unreadable at angle; widen blade or reposition") so the assembly agent can correct deterministically.
- **The Judge scores the assembled Godot scene** (rendered from the real cameras), not an abstract preview. *The validation viewpoint must equal the runtime viewpoint(s).* `[SET THIS: confirm the Judge renders from the editor viewport at these transforms today, or whether that capability needs wiring.]`

---

## 4. [CALIBRATE] One-time derivation from the 2 existing assemblies

Before freezing, reverse-derive the blanks from what the agent already produced (the reps already happened — mine them):
1. **Measure** the height the agent used → set §1.2 canonical height.
2. **Check** how weapons were scaled (relative to character, or arbitrary?) → set §1.3 reference + per-class defaults; note any inconsistency between the two assemblies (inconsistency = exactly the ad-hoc-ness this contract removes).
3. **Inspect** where weapons seated → set §1.4 per-socket offsets.
4. **Note** what scene structure the agent built → reconcile with §2 template (adopt what worked; standardize the rest).
5. **Record** what camera(s) the Judge used (if any) and from what angle → set §3.1 / confirm §3.3.

Output: the filled-in `[SET THIS]` values. After that, the contract is frozen and versioned (bump a version on change; the Analyst flags drift).

---

## 5. Relationship to the other docs & open items

- **JSON schema** (build-architecture §3) = content-engine-agent-facing contract. **This doc** = Godot-agent-facing contract. The two meet where imported `CharacterData`/`GearData`/`ConduitData` Resources drive the assembly the agent performs to this spec.
- **VFX-pipeline doc** = how VFX assemblies are built/judged; §3.2-G and §3.1 here defer to it for billboard/blend/camera specifics.
- **[OPEN]** Does the content "box" hand its data to the Godot agent yet, or are they two islands? If islands, the immediate bridge is: import box-JSON → `CharacterData` Resource → agent assembles to this contract. If already connected, the immediate need is just filling the `[SET THIS]` values.
- **[OPEN]** Locked vs. rotatable gameplay camera (§3.1) — gates whether ground-readability is optimized for one angle or all permitted angles.
- **[OPEN]** Whether the Judge renders from the editor viewport today (§3.3) — gates whether the dual-viewpoint rubric is live now or needs the camera-snap capability wired via MCP first.

---

## 6. One-paragraph summary

The Godot agent has excellent capability (live editor, MCP, snap-to-grid, element knowledge) but assembles ad-hoc because it lacks a frozen blueprint. This contract supplies three standing specs in the agent's own idiom: a **geometry/scale/socket contract** (grid-aligned units, feet-at-origin, −Z facing, a real-cm→units weapon-scale function that makes museum dimensions *visible*, and named `BoneAttachment3D` sockets the agent attaches to deterministically via MCP); a **canonical character-scene template** the agent instantiates (so scene creation is template-instantiation, not exploration, including the inventory SubViewport rig for the dual viewpoint); and a **standardized Judge rubric** that doubles as the assembly agent's definition-of-done, scored from the **two canonical editor-camera transforms** (2.5D gameplay + front inventory) at **mobile scale**, so content is validated against what the player actually sees. Fill the `[SET THIS]` values by mining the 2 existing assemblies, then freeze and version it — turning exploratory agent assembly into deterministic, spec-driven agent assembly.
