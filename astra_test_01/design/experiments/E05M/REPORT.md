# E05M — one-view source-action and release-socket mechanisms pass

[Browser playback](review.html). Native96idle,48walk and72cast frames are driven by a fixed source rig with persistent painted material textures. Walk adds torso counter-rotation; idle avoids scaling the torso/book; cast extends the right hand and returns to idle. This is one-view evidence, not a full eight-view/turn/gear or painted-style pass.

Sixteen source assertions pass. Walk contact drift is0.000003047m; idle/cast stance drift0; minimum sole penetration is below0.000001m. Source bone residuals remain below1mm, book-size variation below1%, idle/walk pose endpoints match exactly and cast returns to idle-start pose exactly. Static geometry is unchanged. The full saved-action render replays the hand socket within1e-5m of source authoring data.

Fourteen headless JSON checks pass, including preservation of world root across action changes (the earlier E05P fixture reset it), exactly one release per cast at.6s, unique event identity, automatic cast completion, invalid-input rejection and immutable JSON state. This remains a fixture boundary, not integration with the serial combat pipeline. Walk-to-idle/cast foot-placement transitions and directional turning are still owed.

Five browser action/socket checks and four final delivery checks pass. Actual native-buffer red-marker centroids lie0.070px/0.151px from the independently projected source hand socket at50/150px, below.5px. The deliberately offset marker is detected at6.507px/19.556px. This qualifies the declared hand socket and timing mechanism; no spell artwork or damage/hit correspondence was tested.

Failure preserved: the first DOM element screenshots were1000×461 although the canvas is1000×460, creating apparent1.06–1.14px errors. The last capture reads the actual canvas buffer; no sprite/camera/threshold changed. The original invalid measurements remain in socket-raster.json and batch03; use socket-raster-native.json and batch04 for pixel acceptance.

Normal-speed video and time samples show opposite leg leads, exposed support boots and a distinct cast. Shape/material side stretching, overall F04 art fidelity, action transitions, all8views, advanced outfit and held-out reuse remain unqualified. The simpler source character is not silently promoted to the final target.

Limits used:one source-authoring revision,4/4capture batches,zero imagegen/paid calls. Raw216512RGBA frames imply216MiB base-level texture storage if all uploaded independently; actual GPU residency was not measured. Apply the proven neutral-atlas method before representative-scale profiling.

Next: separately bounded modular gear/occlusion composition proof can use the now-measured action/socket mechanism; complete directional/action transitions and art/UV quality before declaring the full pilot passed. Reusable paintedVFX may begin only on the relevant qualified attachment path, keeping each behavior independently bounded.

Subsequent correction: [E05Z erratum](E05Z_ERRATUM.md) retracts the old usable-gait visual inference after a proven stance-duration variable collision. Original evidence above remains historical.
