# Game KillMonsters
`game.killMonsters`: when done with monsters in the screen, they all die instantly

# Game Spawn
`game.Spawn`: produces incorrect argument error > screenshot attached
`game.Spawn records/creatures/monsters/zombie/zombie01.dbr`: produces incorrect argument error
`game.Spawn records\creatures\monsters\zombie\zombie01.dbr`: produces incorrect argument error
`game.Spawn zombie01.dbr`: attempts to spawn zombie but nothing seems to happen > screenshot attached

# Warp Cursor
`character.WarpCursor true`
- [yes] Did you appear where you clicked? Instant, or animated?
- [entire screen in one hop] How far can you click? (whole screen / short hop)
- [yes; it may even trigger monster respawns] Warping PAST a monster — did it aggro you? **(the important one)**

# Game Play Stats
`game.PlayStats true`: screenshot attached
- [ yes - top right quadrant of the screen] Does it show **damage dealt / DPS / HP numbers** anywhere? (yes/no)

# Zombie Anger
**Write down:**
- [yes] The word: `AlertBeforePursue` (I'm expecting `AlertBeforePursue` — prove me wrong)
- [unknown] Does the beat feel LONGER when it spots you from far away vs. up close?

Also I found zombies which were buried or laying on the ground and seemed dead. In the same way that the yelling zombies displayed `AlertBeforePursue`, these unearthing/waking up zombies displayed `Startup` while they rose before they attacked. Startup is very common and I haven't found enough instances of `AlertBeforePursue` to yet determine if the beat is longer when it spots me from further away but so far it doesn't feel different based on range. I did also see `followtheleader` when I fought a boss monster.