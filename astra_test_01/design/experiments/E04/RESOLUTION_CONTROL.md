# E04 resolution control — registered before capture

Question: does the 3× diagnostic blur survive when the scene is freshly rasterized at the displayed pixel dimensions?

Hold projection C, logical 960×640 framing, actor size in logical units, original textures, masks, state, browser and GPU fixed. Capture backing buffers at resolution 1 (960×640) and 3 (2880×1920). Display equal 720×540 physical-pixel detail windows: the same 240×180 logical region enlarged 3× from the low buffer with browser smooth interpolation, the same low buffer with nearest-neighbor interpolation, and a 720×540 crop from the new high buffer at 1:1. Also retain full untouched canvas PNGs. Browser canvas extraction is a runtime capture, not an edited source painting.

No image-generation calls or source upscaling. High-buffer rendering samples the original textures directly. The floor source is only 1536×1024; its detail ceiling remains visible in the 2880×1920 render. A higher output buffer cannot invent floor detail. Mage source is 1254×1254, with approximately 1026 pixels of body height before runtime reduction. No sharpening, postprocessing or camera zoom change. Nearest-neighbor is a diagnostic control, not the recommended painted-art presentation.

Acceptance: exact buffer dimensions; equal JSON states and logical projected anchors; no runtime errors; smooth-vs-nearest controls visibly differ; high-resolution crop must be visually inspected, with subjective sharpness separated from numerical checks. No whole-scene quality PASS is implied. Native source-game images have not been matched for source resolution, character coverage or display sampling, so no comparative sharpness ranking is claimed.

Use one of E04's remaining capture batches. Zero paid spend; at most five minutes of browser capture. Actual fullscreen aspect ratio, HUD and output targets remain unqualified. Godot is the shipping target; Pixi is the test harness.

Matt additionally reports pale separating edges and absent shared lighting. Add a same-batch diagnostic board: unchanged mage/monster/NPC sources, their current masks and 150px body height on dark, light and saturated blue backgrounds. Inspect inner contour contamination separately from the existing outside-mask check. This is a falsification/review, not a matte-cleanup or lighting pass. Audit wall highlights/face seams against source UVs. Lighting response and shadow ownership stay H08/G3 gaps; a one-pixel contour tolerance cannot overrule the user's cohesion rejection.
