"""legolas 2026-10-01 -- dump the Ed-IV Game.dll functions this lap's DECODED claims rest on.
READ-ONLY. Writes one text file of objdump excerpts (intel syntax, VMA = 0x10000000 + RVA).
Usage: python3 dump_decode_evidence.py <out.txt>   (needs pe4_edition_IV.py beside it)"""
import sys, hashlib
from pe4_edition_IV import game, eng
FUNCS = [
 ("Character::EnableSpawnAnimation / GetSpawnAnimationEnabled / JustSpawnedWithAnimation", 0x53550, 0x38),
 ("Monster::EnableSpawnAnimation (sets Character+0x1c64 AND controller+0x4da)", 0x2dded0, 0x26),
 ("ControllerMonster::CanPlayStartupAnim / SetPlayStartupAnim (+0x4da)", 0x6aa30, 0x20),
 ("ControllerMonsterStateStartup::ctor", 0xfe700, 0x24),
 ("ControllerMonsterStateStartup::OnBegin", 0xfe730, 0x1c0),
 ("ControllerMonsterStateStartup::OnEnd (restores visible/invincible/targetable to DB values only)", 0xfe8f0, 0x170),
 ("ControllerMonsterStateStartup::HandleEvent ('End' -> SetState Idle)", 0xfea60, 0x130),
 ("ControllerMonsterStateStartup::RequestAttack / RequestMove", 0xfed30, 0x60),
 ("ControllerBaseCharacter::CharacterHandlerUpdate (JustSpawnedWithAnimation -> SpawnAction else IdleAction)", 0xea480, 0x190),
 ("SpawnAction::ctor (type 0x13) / Execute / GetNetPacket / AnimationCallback", 0x70940, 0x260),
 ("ProxyAmbush::UpdateSelf (Ed IV; offsets identical to Lap V-2)", 0x356040, 0x1c0),
 ("ProxyAmbush::PlaceNextObject (vt+0x318 EnableSpawnAnimation before FastSpawnEntity)", 0x356cdb, 0xf0),
 ("Proxy::PoolComplete (NO vt+0x318 call)", 0x3540a0, 0x150),
 ("Proxy::PlaceObjects (NO vt+0x318 call)", 0x354610, 0x1d0),
 ("Character::Load fragment: startVisible==false -> SetVisible(false)+EnableSpawnAnimation; hiddenFromCombat -> +0x1ba0", 0x43d10, 0x50),
 ("Character::IsHiding (invisible | hiddenFromCombat | lifeState==0)", 0x47330, 0x28),
 ("Character::IsTargetable / IsTargetableInDbr / SetTargetable", 0x47b70, 0x30),
 ("Monster::IsTargetable", 0x2de200, 0x30),
 ("Character::SetInvincible / IsInvincible / IsInvincibleInDbr", 0x571f0, 0x10),
 ("GameEngine::FilterInvalidTargets (radius target filter: initial-update, IsAlive, IsHiding, faction)", 0x26a810, 0x290),
 ("ControllerMonsterStateHidden::OnBegin / OnUpdate / HandleEvent (GD's real dormant ambush; appearDistance + BeginUnDissolve)", 0xfde20, 0x6a0),
 ("Monster::GetAmbushDissolveTexture / GetAmbushDissolveTime (only reader: StateHidden::OnUpdate)", 0xfe4c0, 0x18),
 ("ControllerStationaryMonster: RegisterStates fragment (Pursue/Move/Return/Flee... bound to stationary states)", 0x1295a0, 0x6f0),
 ("ControllerStationaryMonster: Pursue::OnBegin (SetState Attack|Idle; no MoveTo)", 0x129180, 0x270),
 ("ControllerStationaryMonster: null-state OnBegin (SetState Idle) for Move/Return/Flee/FollowLeader/DefendLeader", 0x129480, 0xa0),
]
out = open(sys.argv[1], "w")
out.write("# Ed-IV Game.dll decode evidence, legolas 2026-10-01\n")
out.write("# Game.dll sha256 %s\n# Engine.dll sha256 %s\n\n" % (hashlib.sha256(game.raw).hexdigest(), hashlib.sha256(eng.raw).hexdigest()))
for title, rva, n in FUNCS:
    out.write("=" * 100 + "\n## %s  (RVA 0x%x, %d bytes)\n" % (title, rva, n))
    txt = game.disasm(rva, n)
    out.write("\n".join(l for l in txt.splitlines() if l.strip() and "file format" not in l and "int3" not in l) + "\n\n")
out.close()
