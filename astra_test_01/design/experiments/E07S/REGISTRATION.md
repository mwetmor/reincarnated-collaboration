# E07S — painted materials on geometry-owned faction scenes

Changed representation after E07R's closed full-scene branch: generated artwork supplies reusable material surfaces; explicit typed geometry retains doors, character/object identity, scale and state. F01 waystation/F02 reservoir remain Matt-delegated Codex selections. F04 clarity/F03 local light response remain the target. Godot shipping target; Pixi test harness.

Limits:90active minutes,3built-in imagegen calls total (two distinct material plates plus at mostone scoped repair),4capture batches,100MB. No paid services or API fallback. Preserve original source pixels; no enlarging generated artwork. Reuse E04S stone/soil and E05M actor control where applicable; old images/failed E07R scenes remain unchanged.

Export E07R's existing .blend geometry to neutral surface/role JSON, preserving exact C coordinates and typed actors/props. Replace ovoid probes with explicitly mapped existing painted character/monster/NPC assets; never infer identity from generated scenery. Geometry guides are controls, not final painted deliverables. Generate a restrained blackened timber material and low-contrast carved-reservoir stone material, both orthogonal flat lighting. The renderer projects them onto exact surfaces. Do not bake layout, door openings or actors into these material plates.

State proof is scoped to the two boundary exit leaves: open/closed angle and sweep are declared in layout; collision/region changes belong in a JSON-only sim. The interior passage remains open in this unit; E04's locked interactive gate remains separate historical evidence, not silently replaced or re-qualified. Preserve all relevant old tolerances.

Freeze: C world/screen projection residual≤0.5logicalpx; source/adapter gate-corner comparison≤3nativepx; zero reversed interior/exterior region assignments; zero incompatible/missing typed actor/prop substitutions; no blocked forbidden crossing through closed exit. Bad reversed region,40px shifted doorway overlay, stale-open collision and incorrect foreground order must be detected. Test both exits open/closed, inside/outside witnesses and clearance. Source-camera ray results independently constrain screen occlusion.

Light controls: same floor/wall/material under neutral/warm/cool source descriptors; at a source-selected visible receiver an intervening closed leaf must block the point contribution, and opening it must restore it. Bad ignore-leaf-occlusion lights the blocked receiver and fails. Report actual RGB and witness visibility; do not measure an occluding door as the floor. All light data/material semantics engine-neutral, view mapping in named Pixi adapter.

Visual scope: render native960x640 and fresh2880x1920; inspect both factions, doorway controls and multiple backgrounds. No universal white outlines, no generated room geometry drift. Material/architectural cohesion and detail remain independent from numerical geometry passes. This is not all motions/gear/VFX/second-chunk/production pass.

If projected surfaces look too plain or repeat visibly, record that art limitation instead of upgrading blockout geometry to a painted-style pass. Correct only within the registered material/geometry/adapter budget before expanding.
