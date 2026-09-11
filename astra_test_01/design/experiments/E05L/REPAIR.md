# E05L revision2 · interpolate bend directions, not knee positions

V1 preserves contacts and endpoints but phases0/24 jump a Shin joint by48.65cm. The interpolated reference knee point crosses the current hip/ankle line, reversing its projected bend direction. Read-only pole-diagnosis.json locates the affected joints/frames. V2 derives normalized bend directions from the initial and idle leg planes, interpolates those directions, and projects onto the current leg plane. Foot trajectories, timing, body interpolation, art and frozen bars remain unchanged. Preserve V1source/phase failure receipt. Two source revisions maximum.

Full V1 preflight fails joint continuity in14phases:0,1,2,3,4,5,23,24,25,26,27,28,29,47. The read-only diagnosis focuses on0/24 as large representative failures. V2 checks everyphase, not only those two.
