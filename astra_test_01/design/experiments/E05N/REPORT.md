# E05N · Deformed-surface normal agreement

**Representation PASS; production scale and full pilot unqualified.** Godot shipping target; Pixi harness. No generation, two export/adapter revisions, four capturebatches,~76.5MB of100MB;45minuteceiling held.

Cause probe: originalskin sixFAIL, normal-only sourceoverride48/48PASS (maxMAE.005748,maxfraction.000140925), position-only sixFAIL. The issue is blendedrestnormal vsdeformedsource-surfacenormal, not vertexpositions. All216E05Zpalettebytes, cachedgeometry/indices/materials/UVs and sourcefile remainunchanged.

Engine-neutral sparse correctionstream: uint32vertexindex + float32worldnormalXYZ,16bytes/record, per-framebyteoffset/count, littleendian. Header tiesdata torestmesh andpaletteSHA256. Adapter clearsnormals everyframe and sets onlydeviations>1e-4 from normalizedweightedrestnormal. All219frames/endpoints checked; omittedresidual<=1e-4. Exportednormaluniterror<=1.193e-7. Range3,501–8,341correctedvertices/frame outof63,864. Stream16,736,368bytes for216frames, currentadapterfullattributeupload1,021,824bytes/pose. These are measuredpayload sizes, not actualVRAM/bandwidth/productioncapacity. Importer/Godotpackaging, compression and costscale remainopen.

Nineindependent Blenderoracles idle0/24/72, repairedwalk0/12/36,cast0/18/36; eightviews,two50/150axis scales,threeoutfit/headconditions,threebackgrounds.1296/1296comparisons pass unchangedMAE<=1,fraction>8<=.02. WorstMAE.007239819,worstfraction.0009049774. Missingnormalcorrection atknowncast135cell exactlyreproducesoldMAE.4463078/fraction.021984216;20pxgearshift27.4829/.55462 andwrongpose21.3454/.49509detected. PreviousE05Yfailuresretained, scoped repairedrepresentationnowpasses.

216nativeframehashaudit andnormal-speed startercast eightviewvideo complete. Savedclip2.382936s vsnominaltwo1.2scycles becauseencodedendpoints mayomitfractionofframe; noexactframecoverage/production60fpsclaim. Independentframeaudit coversall216.6/6savedlocalHTMLchecks pass; before/corrected/source native135degree crops visuallyinspect subtle sleeveshading agreement. No shape/artstylechange. Favicon404preserved, noasset/GLerrors.

Next E05I: left/right45degree turn-in-place, geometry-owned footcontacts and pureJSON action/headingboundary. Current cast/idle/walk agreement doesnot prove turns, actiontransitions, fullcloth/outfitsurfacefit, chamberlighting or completepilot. No rosterscaling yet.
