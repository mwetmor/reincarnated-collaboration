# E05I · Contact-aware turns from idle

**Scoped turn/contact/JSON transition PASS; full pilot open.** Godot shipping target; Pixi harness. Two source revisions, zero generation, three actual capture batches (reserved03unused),~88MB of100MB,60minuteceiling held. Source E05Z corrected gait, E05W immutable paintings, E05N normal contract.

Two0.6s/36frame actions turn±45° with twofootplacements andfixedroot. V1contacts pass but rotated-idle end fails0.712158matrixerror: shortest rest-vector→IK-vector rotation drops limb axialbodyyaw. V2 rotatesrestvector bybodyyaw first, aligns toIKtarget andcomposeswithbodyyaw. No footpath/art/bar changes. V1source andfailure retained.

V2:22/22turn assertions plus immutablegeometry/weights/UV/materialcheck pass. Left/right supportdrift7.281e-7/5.731e-7m; swinglift.0800005m; hipexcursion1.7165/2.6583mm; maximumjoint step3.2252/3.2882cm. Start-idle error8.68e-7, end rotated-idle1.032e-6, below1e-5. Instantrotation slides oldplantedfeet11.715cm, detected against2cmbar. Existing216idle/walk/cast palettes arebyte-exact (SHA1b15b2b5adc8056ca6e6647b4121086589a4ba27d42400b57e10bbeaec95aa3a).

72turnpalettes,74frame/endpoints, sourcecoreclearance andnormalresidualchecks pass. Neutralmanifest includes per-frame footcontacts, socket, fps, duration, relativeheadingdelta andsparse normals. Normalstream5,675,648bytes.1152frame/view/scale bounds pass withminimum42.526px in2400×500native layout. Worldroot/heading staydata values; comparatorusesfixeddiagnostic camera.

23headlessJSON checks: bothdirections/all8headings, unchangedroot,inputimmutability, completiononce, headingcommit, midturnJSONrestore, invalid/nonfinite/nonJSONinput, incompatiblecontent andoverlap rejection. No renderingimports or gameheadingcommit inadapter. Renderer selectsrelativebakedturn withstartheading; idle usescommittedheading. This fixturedoesnotdefine finalcombat responsiveness/steeringpolicy.

1152/1152raster comparisons pass (eightindependentposes×eightviews×twoscales×threeoutfit/headconditions×threebackgrounds), maxMAE.006502396/maxfraction.0001538698. Shiftcontrol29.4346/.58328 andwrongpose27.7588/.78849detected.72nativeframehashaudit andthreeoutfit normal-speed idle→left→idle→right→idle sequences pass. Two completionevents each, initial/finalpixels exact. Overlapping realbuttonclick rejectssecondrequest withoutfreezingfirst; reversebuttonreturnsheading0.6/6savedlocalHTMLchecks pass. Videoendpoints1.78–1.80s, no production60fps or exactencodedframeclaim.

Visual: turnmidpointall8views advanced, base135°nativevideo eighttime samples andfull scripted playback forstarter/helmet/hair. Stablebody, readablefootexchange, no observedgrosslegcrossing/collapse or detachedgear inthese inspectedcases. Stiffcoat/fulloutfitsurfacefit andotheractions remainopen. No roster/fullpilot/styleapproval.

Next E05L: sourcepreflight forphase-aware locomotion stop/start. Direct switching andfullarbitrary-phase runtime behavior areunqualified; test thecontact-preserving recipe before expandingexports. MinimumPC/resolution question(D05)asked asynchronously; noanswerassumed. Independentmotion/art workcontinues.
