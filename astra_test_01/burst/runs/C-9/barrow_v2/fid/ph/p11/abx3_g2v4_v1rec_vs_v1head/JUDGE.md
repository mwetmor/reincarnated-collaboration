# Image matching test

There are 58 images, `trial_01.png` .. `trial_58.png`. Each shows three square crops side by side, separated by white
gaps. From left to right they are **A**, **B** and **X**.

Every crop comes from one of several versions ("builds") of the same hand-painted 3D game level, seen from the same
fixed high camera at the same zoom. In each image, A and B come from two different builds. X comes from the same build
as either A or B, but from a different place in the level.

For each image, answer only: **is X from the same build as A, or from the same build as B?** Base the answer on how
the images are painted and rendered, not on what objects they show. Every image needs an answer, A or B; if you
cannot tell, give your best guess.

Return a JSON object {"trial_01": "A" or "B", ..., "trial_58": "A" or "B"}. For each trial, add one short sentence
naming the visual evidence for the answer.
