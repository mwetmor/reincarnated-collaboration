# Persistent-layer motion capability check — 2026-09-11

Godot is the shipping target; Pixi is the test harness.

[Bunraku's paper](https://arxiv.org/abs/2607.27348) describes joint RGBA-layer completion, alpha-derived meshes and predicted keypose offsets, with clothing retexturing while retaining motion. Its [public repository](https://github.com/SparcAI-Inc/Bunraku) currently exposes a README and no runnable inference implementation/model release in the inspected root. The paper's Live2D findings motivate a hypothesis; they do not establish our full-body eight-view ARPG gait or an available tool. No inferred weights/API/alpha capability is used.

[Frame Lab](https://github.com/vucinatim/frame-lab) documents BODY_25 pose editing, IP-Adapter/ControlNet conditioning and a ComfyUI workflow running on Replicate. Its setup requires a Replicate API token. No such service authorization is assumed, and it is not installed or invoked. The pose/identity separation is useful design guidance; the README's consistency claim is not our acceptance evidence.

[Spine's mesh documentation](https://esotericsoftware.com/spine-meshes) describes texture-mapped mesh attachments and deformation, providing an established representation reference. No paid editor/runtime access is assumed or newly licensed. The local Pixi probe will use explicitly authored neutral parts, pivots, meshes and time-based tracks; a future Godot adapter can consume that data.

This is ordinary bounded capability research: one primary-source batch, four pages inspected. No models downloaded, no external project uploads/messages, no paid calls. References were checked rather than treated as ready-to-run tools.
