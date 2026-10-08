# JOIN-1 · P-J2-5 step 2: HALTED at the source pre-check (KP-364)

gamora, 2026-10-08. Prereg engine `756f1098`; instrument `410493bc`.

## Result: nothing computed

Lap O's library reads Grim Dawn **edition III** (2026-08-08) at fixed paths, and both are **absent** from disk:

- `/Users/admin/Games/vendor/grim-dawn-edition-III-20260808/database/database.arz`
- `/Users/admin/Games/vendor/grim-dawn-edition-III-20260808/resources/Text_EN.arc`

`/Users/admin/Games/vendor/` holds only edition II (2026-07-24) and edition IV (2026-09-29). The directory was last modified on 2026-10-01. The extra `.arz` at `/Users/admin/depots/219991/24346246/` is of unrecorded edition.

- **No edition was substituted** (GL-12; conductor KP-364: route, don't substitute).
- **S2-CAL-1 did not run,** so no verdict counts and no E_L exist yet.
- `s2_precheck.json` records the missing paths, the three library FILE sha256s and the table pin (OK).

## Routed to the conductor (for elrond / legolas)

Either **(a)** restore edition III at its path, or **(b)** rule which edition the library reads instead.

Under (b), S2-CAL-1 is exactly the check that detects drift: the library must reproduce Lap O's 2026-08-14 table on 74/74, or step 2 HALTs. Edition IV is newer than the sealed oracle's data, so a game-data change since 2026-08-08 would show there.
