# E05I source revision2 · retain axial limb orientation

V1 passes footcontact/lift/geometry/jointcontinuity but fails rotated-idle endpoint: maxmatrixerror0.712158 bothdirections. Its legorientation uses shortest rotation fromrestbonevector toIKbonevector, losing bodyyaw/axialroll. V2 firstapplies bodyyaw torestbonevector, then rotates thatvector toIKdirection and composeswithbodyyaw. Atturned-idle endpoint the IK adjustment becomesidentity, retaining fullrotatedrestframe. No footpaths/bodytiming/painting/thresholdchange. Preserve V1source andfailurereceipt; onlytwo source revisions allowed.
