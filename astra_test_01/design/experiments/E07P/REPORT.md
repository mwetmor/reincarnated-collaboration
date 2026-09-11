# E07P — namespace repair passes; actor mask integration fails

The repaired synthetic capability passes all nine checks without GL errors. The chamber source gate fails 480 of 768 witnesses because the actor masks are empty. No visibility aid is promoted; E07J remains the working chamber. Godot is the shipping target; Pixi is the test harness.

Build1 renames custom uColor to uIndicatorTint and audits the installed Pixi local mesh uniform names. The prior GL collision is repaired. Matching multisample depth and alpha/negative controls pass in the simple fixture.

Build2 integrates two camera masks against the actual opaque chamber and current source pilot. All eight initial shader paths compile without GL errors. Twelve source states cover exposed, partition and west-wall positions in both factions at native and fresh3×. All 288 outside samples pass, but all 288 visible and192hidden actor samples fail. Missing-world and always-on controls are insensitive because neither target contains a pilot silhouette. Off/A/B images are retained and do not establish a style choice. Simulation states remain identical.

Live resource introspection identifies the cause. Pixi Shader.resources has non-enumerable accessors: Object.keys returns[], while Object.getOwnPropertyNames returns['params']. Passing the accessor object directly into a new shader silently omits its uniform group. The actual rig collapses with missing bone/position/scale uniforms. Materializing its named resources preserves params and the test value0.75. The installed vendor source confirms the property descriptors.

The earlier rectangle capability did not adequately test uniform transfer: default depth values could still produce the expected front/behind colors through draw order. Preserve those scoped pixel results, but do not treat them as a uniform-transfer pass. Add an inverted-depth control in the next preflight.

Both registered builds are used (cumulative visibility builds four). Next E07Q materializes resource accessors in the clone, verifies depth reversal and actual uniform values, then reruns the unchanged 768 source witnesses and controls. No mask threshold, geometry, source guard or bias change. No generation or paid-service calls occurred.

Two full-viewport MSAA4 masks account for72bytes per physical pixel by color/depth/resolve arithmetic:44.24MBnative and398.13MBfresh3×, before driver overhead. These are allocation estimates, not whole-app residency; a bounded pilot region remains a later optimization candidate after correctness.
