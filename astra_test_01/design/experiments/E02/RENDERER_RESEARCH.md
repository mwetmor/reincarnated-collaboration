# Renderer choice for agent-authored painted composition

Research date: 2026-09-11 UTC. User scope: compare the agent's ability to assemble
and revise scenes, characters and VFX. The combat/content JSON is shared input;
an engine's combat feature list is not a selection advantage here. Projection **C**
is independent of renderer choice and remains the selected experiment candidate.

**Shortlist: Godot, Pixi.js, then Phaser 4 as the most useful third test.** This
is a test-order recommendation, not an established quality or productivity winner.
Godot and Pixi have actual E02 renders; the alternatives below have documentation
evidence only. No alternate editor, paid service or skeletal-animation tool was bought.

## Godot — run here, retain in the comparison

Observed: Godot **4.6.3** loaded the existing painted PNG in Sprite2D, rendered the
JSON-derived floor geometry through the selected projection, transformed a child
attachment and saved GPU-rendered evidence on Apple M2. Code-authored scenes were
sufficient for this probe; no manual editor assembly was required. See
[runtime results](evidence/runtime-fixed-v2.json) and [project](runtime/project.godot).

For later composition it provides an animation-track system, 2D skeleton nodes,
and GPU particles. Those are available mechanisms, not evidence that our layered
paintings animate well. [AnimationPlayer](https://docs.godotengine.org/en/stable/classes/class_animationplayer.html),
[Skeleton2D](https://docs.godotengine.org/en/stable/classes/class_skeleton2d.html),
[GPUParticles2D](https://docs.godotengine.org/en/stable/classes/class_gpuparticles2d.html).

Assessment: a strong full-engine baseline, especially for testing masks, layered
objects and complex effect timelines. My actual ability to use those facilities
with the chamber remains to be measured. This small import/attachment proof does
not establish a GPU performance or animation-authoring advantage.

## Pixi.js — run here, retain in the comparison

Observed: isolated **8.20.1** renders the same inputs through WebGL2 / ANGLE Metal
on Apple M2. Camera/position/bad-scale controls passed in a fresh local Chrome
process. The sibling demo uses **7.4.3**; it was read only and was not upgraded.
See [browser results](evidence/runtime-pixi-v2.json) and [interactive probe](pixi/index.html).

Pixi's containers, masks, meshes, blend modes and filters directly support a
compositor-oriented approach. In v8, attach related visual pieces to a Container;
do not rely on nesting children under a Sprite. Its ParticleContainer is a fast
particle representation, not proof that our complete VFX lifecycle is authored.
[Scene objects](https://pixijs.com/8.x/guides/components/scene-objects),
[ParticleContainer](https://pixijs.com/8.x/guides/components/scene-objects/particle-container).

Assessment: a strong candidate for direct code composition and browser inspection
around existing JSON. We still have to author the assembly contract, animation
tracks, attachment rules and effect lifecycle. Its smaller scope does not by
itself make that work cheaper. The demo's loader confirms existing JSON intake;
E02 has not integrated that combat data or replaced its schema.

## Phaser 4 — recommended third test

The official release list shows **4.2.1** dated July 9, 2026. Phaser 4's renderer
was rebuilt around render nodes, with an expanded effects system. Therefore an
assessment based solely on remembered Phaser 3 limitations would be stale.
[Release list](https://phaser.io/download/phaser4),
[renderer changes](https://phaser.io/news/2026/04/phaser-4-renderer-faster-cleaner-and-built-for-modern-games).

Its container composition and configurable particle emitters make it a useful
contrast with Pixi: can supplied scene/effect facilities reduce our custom assembly
code while preserving control over painterly layers and exact timing? Concept
documentation includes historical v3 notes, so pin the tested v4 API and verify it
locally before adapting code. [Containers](https://docs.phaser.io/phaser/concepts/gameobjects/container),
[particles](https://docs.phaser.io/phaser/concepts/gameobjects/particles).

Recommendation is an inference about the most informative next experiment.
Phaser has not rendered this chamber here. The first test should use the same
PNG/layout/projection/events, followed by the same masked prop, attachment and
animated effect. The new Phaser Editor/agent products are not part of this
recommendation; no access to them is assumed.

## Defold — reserve for a native-oriented comparison

Defold has sprite and particle components, scriptable render ordering/projection,
and a command-line project builder. These support a reproducible composition
experiment without making a browser stack mandatory. [Render pipeline](https://defold.com/manuals/render/),
[particles](https://defold.com/manuals/particlefx/),
[command-line builder](https://defold.com/manuals/bob/).

Assessment: credible if our next question concerns a compact native runtime and
scripted render control. It introduces another resource/build model before we
have found a composition failure in the two installed stacks, so it is lower
priority for this particular test. No installed Defold/build capability was verified.

## Cocos Creator — reserve for an editor-oriented comparison

The 3.8 LTS documentation covers scene assets, Spine asset intake, particles and
command-line publishing. It offers another way to structure authored visual
resources. [Spine assets](https://docs.cocos.com/creator/3.8/manual/en/asset/spine.html),
[publishing](https://docs.cocos.com/creator/3.8/manual/en/editor/publish/publish-in-command-line.html),
[particles](https://docs.cocos.com/creator/3.3/manual/en/particle-system/).

Assessment: relevant if editor/resource workflows help the art pipeline. Local
installation and unattended editing are untested, and the particle overview is
older documentation rather than a verified installed API. That uncertainty makes
it a less informative immediate third test than Phaser. Spine support must not
be read as already-owned authoring capability; no licensed workflow is assumed.

## Three.js — conditional 2.5D representation experiment

Three.js sprites face the camera. A renderer's use of perspective does not supply
missing painted viewpoints; a billboard still depicts its source view.
[Sprite documentation](https://threejs.org/docs/pages/Sprite.html).

Assessment: reserve a Three.js plane/mesh prototype for a specific hypothesis
about perspective-correct painted planes, height or occlusion. That changes
representation as well as engine, so keep it a separate experiment. It is not
needed to continue C: both current 2D renderers already project the logical floor.

## What should decide the winner

Use the [shared composition benchmark](RENDERER_BENCHMARK.md). Compare visible
quality and correctness first; then measure the actual edit → render → inspect →
repair cycle. Do not rank engines by line count, generic particle demos or assumed
agent familiarity. Godot was implemented first and Pixi reused its clarified
contract, so their current elapsed effort is order-biased.

Current evidence supports **continuing both Godot and Pixi, testing Phaser next,
and making no production renderer selection yet**. The first genuine discriminator
is the same painted chamber with a tall sortable prop, a gear attachment, and
time-driven VFX; E02 is only the projection/import starting point.
