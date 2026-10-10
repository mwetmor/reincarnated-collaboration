# Deferred web arena bugs — 2026-10-10

Matt confirmed that the Vercel preview runs and reported the regressions below relative to the existing native game. Status: OPEN, DEFERRED at Matt's direction until the PC package is complete. Do not treat the startup/control smoke tests as visual or physics parity acceptance.

Preview: https://reincarnated-loadout-5i1cmo8xq-matthew-wetmore-s-projects.vercel.app/playtest/barrow-arena/
Native reference: `godot/scenes/bv2f_arena.tscn` in this Barrow project.

| ID | User-reported regression | Follow-up acceptance |
| --- | --- | --- |
| WEB-01 | Many 3D elements are absent or differ from the native game. | Inventory and compare the native and web scene at matching camera positions; restore the missing elements. Exact objects not yet identified. |
| WEB-02 | Physics behavior/features are missing or differ. | Reproduce against the native build and compare collisions, traversal, and affected effects. Exact interactions not yet identified. |
| WEB-03 | Colors look washed out. | Capture matched native/web views and compare renderer, lighting, color space, materials, and texture conversion; obtain Matt's visual acceptance. |
| WEB-04 | At least one monster group lacks its character art. | Identify the wave/group/kit, verify its packaged files and art binding, and confirm every group renders. Group identity not yet supplied. |
| WEB-05 | Mobile access requires a Vercel login. Matt can sign in, but external playtesters cannot use that flow. | Provide a deliberately shared playtest route/link that works without a tester's Vercel account. Current preview remains protected; no protection settings changed. |
| WEB-06 | The app does not load on Matt's mobile phone, so touch controls could not be tested. | Reproduce on the actual phone/browser, diagnose loading, and verify startup and every touch control on a physical device. Phone model/browser and failure stage are not yet identified; desktop touch emulation is insufficient evidence. |

These are observations from Matt's playtest, not root-cause findings. The web export uses Compatibility rendering and reduced art; the new PC package must start from the existing native game and full-resolution assets. Web investigation/resolution is deliberately deferred, not closed.

Packaging lead for WEB-01/WEB-02: the first PC export omitted raw `.f32` level heightfields/carved geometry, and its isolated scene probe reported empty ground data and no reachable walk cells. The PC preset/audit now include those files. When web work resumes, check the actual web packs for these same inputs; this is a lead, not a confirmed web root cause or a web fix.
